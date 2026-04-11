#!/usr/bin/env python3
"""플러그인 공통 유틸리티.

validate-plugin.py 와 sync-docs.py 가 공유하는 헬퍼 함수 모음.
표준 라이브러리(pathlib, json) + pyyaml 만 의존한다.
"""
from __future__ import annotations

import json
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).parent.parent
_MARKETPLACE_JSON = REPO_ROOT / ".claude-plugin" / "marketplace.json"


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


def iter_skills(kit_path: Path) -> list[Path]:
    """kit_path/skills/*/SKILL.md 정렬 목록."""
    return sorted(kit_path.glob("skills/*/SKILL.md"))


def iter_agents(kit_path: Path) -> list[Path]:
    """kit_path/agents/*.md 정렬 목록 (.gitkeep 제외)."""
    return sorted(
        p for p in kit_path.glob("agents/*.md")
        if p.name != ".gitkeep"
    )
