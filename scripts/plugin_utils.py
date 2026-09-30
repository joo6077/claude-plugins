#!/usr/bin/env python3
"""플러그인 공통 유틸리티.

validate-plugin.py · sync-docs.py · sync-orchestrator.py · 사본 검사 둘 · 문서 쪽 검사 둘이 공유하는 헬퍼 함수와 표.
표준 라이브러리(pathlib, json) + pyyaml 만 의존한다.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).parent.parent
_MARKETPLACE_JSON = REPO_ROOT / ".claude-plugin" / "marketplace.json"

# 킷 → 그 킷 카이젠이 읽는 리서치 원본 폴더. validate-plugin V10 과 sync-orchestrator 가 함께 읽는다 —
# 두 스크립트가 따로 두면 한쪽만 늘어나 V10 이 새 킷의 원본을 조용히 빠뜨린다
KIT_RESEARCH_DOCS: dict[str, str] = {
    "backend-kit": "docs/backend/",
    "infra-kit": "docs/infra/",
    "rust-kit": "docs/rust/",
    "react-kit": "docs/react/",
    "flutter-toolkit": "docs/flutter/",
    "design-kit": "design-kit/docs/design/",
    "planning-kit": "docs/planning/",
    "tone-kit": "docs/tone/",
    "api-kit": "docs/api/",
    "howto-kit": "docs/howto/",
}


def load_marketplace(path: Path | None = None) -> dict:
    """marketplace.json 을 파싱하여 dict 반환."""
    target = path or _MARKETPLACE_JSON
    return json.loads(target.read_text(encoding="utf-8"))


def list_kits(marketplace_data: dict | None = None) -> list[Path]:
    """marketplace.json 의 plugins 배열에서 킷 디렉토리 경로 목록 생성."""
    data = marketplace_data or load_marketplace()
    return [
        REPO_ROOT / p["source"].lstrip("./")
        for p in data.get("plugins", [])
    ]


def read_text(path: Path) -> str:
    """UTF-8 로 파일 읽기, 실패 시 빈 문자열."""
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return ""


def parse_frontmatter(text: str) -> tuple[dict | None, str]:
    """마크다운 YAML frontmatter 와 본문 분리 파싱. pyyaml 기반."""
    if not text.startswith("---"):
        return None, text
    end = text.find("\n---", 3)
    if end == -1:
        return None, text
    fm_text = text[3:end].strip()
    body = text[end + 4:].lstrip("\n")
    try:
        data = yaml.safe_load(fm_text)
        return data if isinstance(data, dict) else None, body
    except yaml.YAMLError:
        return None, body


def parse_frontmatter_raw(text: str) -> dict[str, str] | None:
    """Line-based frontmatter parser (no yaml decoding).

    pyyaml 과 달리 block scalar (`>`) 를 접지 않고 description 필드는
    첫 indent 줄만 추출한다. README 테이블 같은 "한 줄 요약" 용도에 사용.

    name 필드가 없으면 None 을 반환한다.
    """
    m = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return None

    block = m.group(1)
    data: dict[str, str] = {}
    lines = block.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]

        # key: > (block scalar) — description 은 첫 indent 줄만 추출
        bm = re.match(r"^(\w[\w-]*):\s*>\-?\s*$", line)
        if bm:
            key = bm.group(1)
            parts: list[str] = []
            i += 1
            while i < len(lines) and re.match(r"^\s{2}", lines[i]):
                parts.append(lines[i].strip())
                i += 1
            if key == "description" and parts:
                data[key] = parts[0]
            else:
                data[key] = " ".join(parts)
            continue

        # key: value (inline)
        km = re.match(r"^(\w[\w-]*):\s*(.+)$", line)
        if km:
            key = km.group(1)
            val = km.group(2).strip().strip("\"'")
            data[key] = val

        i += 1

    return data if "name" in data else None


def iter_skills(kit_path: Path) -> list[Path]:
    """kit_path/skills/*/SKILL.md 정렬 목록."""
    return sorted(kit_path.glob("skills/*/SKILL.md"))


def iter_agents(kit_path: Path) -> list[Path]:
    """kit_path/agents/*.md 정렬 목록 (.gitkeep 제외)."""
    return sorted(
        p for p in kit_path.glob("agents/*.md")
        if p.name != ".gitkeep"
    )


def normalized(lines: list[str]) -> list[str]:
    """사본 대조용 — 줄 앞 공백과 인용 표식 `>` · 끝 공백을 떼고 빈 줄을 버린다."""
    stripped = (re.sub(r"^[\s>]*", "", line).rstrip() for line in lines)
    return [line for line in stripped if line]


def contains_block(lines: list[str], block: list[str]) -> bool:
    """block 이 lines 안에 끊김 없이 나오면 참."""
    width = len(block)
    return any(lines[start:start + width] == block for start in range(len(lines) - width + 1))


# 문서 쪽이 공통 CSS 를 화면 스타일로 불러오는지 — check-api-kit-docs · check-docs-common-css 가 함께 쓴다.
# 둘이 판정을 따로 들고 있다가 한쪽은 preload 를, 다른 쪽은 data-rel 을 연결로 셌다(2026-09-29)
_HTML_COMMENT = re.compile(r"<!--.*?-->", re.S)
_LINK_TAG = re.compile(r"<link\b[^>]*>", re.I | re.S)
_SCREEN_MEDIA = {"", "all", "screen"}


def _attr_value(tag: str, name: str) -> str | None:
    # 앞에 글자나 `-` 가 붙은 이름(data-rel · data-href)은 다른 속성이다
    found = re.search(r"(?<![-\w])" + name + r"""\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s"'>]+))""", tag, re.I)
    return "".join(found.groups("")) if found else None


def site_css_stylesheet_links(text: str) -> int:
    """HTML 주석 밖 `<link>` 가운데 `assets/site.css` 를 화면 스타일로 불러오는 것의 수.

    rel 낱말에 stylesheet 가 있고 alternate 가 없으며, media 가 없거나 all · screen 이고,
    주소가 물음표 값을 뗀 뒤 `assets/site.css` 로 끝나야 센다.
    """
    count = 0
    for tag in _LINK_TAG.findall(_HTML_COMMENT.sub("", text)):
        rel_words = (_attr_value(tag, "rel") or "").lower().split()
        href = _attr_value(tag, "href")
        media = _attr_value(tag, "media")
        if "stylesheet" not in rel_words or "alternate" in rel_words or href is None:
            continue
        if not href.split("?", 1)[0].endswith("assets/site.css"):
            continue
        if media is not None and media.strip().lower() not in _SCREEN_MEDIA:
            continue
        count += 1
    return count
