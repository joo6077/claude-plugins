#!/usr/bin/env python3
"""
detect-docs-drift.py — docs-site HTML 재생성 필요 manifest 생성

`git diff --since <ref>..HEAD` 기준으로 변경된 `.md` / `.yaml` 소스 파일을 찾아
대응하는 `docs/<plugin>/*.html` 경로를 매핑하여 stdout 에 출력한다.

kaizen-orchestrator Step 11.5 (docs-site 재생성) 에서 서브에이전트에게
"어느 HTML 을 재생성해야 하는지" 를 정확히 알려주기 위한 manifest 역할이다.

사용법:
    python3 scripts/detect-docs-drift.py [--since <ref>] [--json]

옵션:
    --since <ref>    기준 git ref (기본: main)
    --json           JSON array 형식으로 출력
    --verbose        변경된 소스 전체 목록 포함
    --help           사용법 출력
"""

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


# 소스 경로 prefix → 출력 HTML 디렉토리 매핑
SOURCE_TO_HTML: list[tuple[str, str]] = [
    ("harness/docs/guides/", "docs/harness/"),
    ("harness/references/", "docs/harness/"),
    ("docs/backend/", "docs/backend-kit/"),
    ("docs/infra/", "docs/infra-kit/"),
    ("docs/rust/", "docs/rust-kit/"),
    ("docs/react/", "docs/react-kit/"),
    ("docs/flutter/", "docs/flutter-toolkit/"),
    ("flutter-toolkit/references/", "docs/flutter-toolkit/"),
    ("design-kit/docs/design/", "docs/design-kit/"),
]


# docs-site 페이지는 소스 basename 과 1:1 이 아니다.
# 예: harness/docs/guides/plugin-validation-guide.md → docs/harness/plugin-validation.html
# (등록 페이지에는 `-guide` suffix 가 없다). 파일명 규칙을 추측하지 말고
# `docs/index.html` 의 페이지 레지스트리를 SSOT 로 삼아 대조한다.
INDEX_HTML = REPO_ROOT / "docs/index.html"
REGISTRY_FILE_RE = re.compile(r"file:\s*'([^']+\.html)'")

# 후보 target 이 레지스트리에 없을 때 시도할 stem 변형 (앞에서부터 순서대로)
STEM_VARIANTS: list[tuple[str, str]] = [
    ("-guide", ""),   # plugin-validation-guide → plugin-validation
    ("", "-guide"),   # skill-design → skill-design-guide
]


@dataclass
class DriftEntry:
    source: str
    target: str
    registered: bool = False
    exists: bool = False

    def to_dict(self) -> dict:
        return {
            "source": self.source,
            "target": self.target,
            "registered": self.registered,
            "exists": self.exists,
        }


def load_registry() -> set[str]:
    """docs/index.html 에 등록된 HTML 경로 집합 (docs/ 기준 상대경로 → repo 상대경로)."""
    if not INDEX_HTML.exists():
        return set()
    text = INDEX_HTML.read_text(encoding="utf-8")
    return {f"docs/{m}" for m in REGISTRY_FILE_RE.findall(text)}


def resolve_target(candidate: str, registry: set[str]) -> tuple[str, bool, bool]:
    """후보 경로를 레지스트리/파일시스템과 대조해 실제 target 을 결정한다.

    Returns (target, registered, exists).
    """
    def probe(path: str) -> tuple[bool, bool]:
        return path in registry, (REPO_ROOT / path).is_file()

    registered, exists = probe(candidate)
    if registered or exists:
        return candidate, registered, exists

    directory, _, filename = candidate.rpartition("/")
    stem = filename[: -len(".html")]
    for old, new in STEM_VARIANTS:
        if old and not stem.endswith(old):
            continue
        variant_stem = (stem[: -len(old)] if old else stem) + new
        if variant_stem == stem:
            continue
        variant = f"{directory}/{variant_stem}.html"
        v_registered, v_exists = probe(variant)
        if v_registered or v_exists:
            return variant, v_registered, v_exists

    # 대응 페이지가 아직 없다 — 신규 생성 대상
    return candidate, False, False


def run_git(args: list[str]) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if result.returncode != 0:
        return ""
    return result.stdout


def changed_files(since: str) -> list[str]:
    out = run_git(["diff", "--name-only", f"{since}..HEAD"])
    return [line for line in out.splitlines() if line.strip()]


def map_source_to_html(source: str) -> str | None:
    """Given a changed source file, return the corresponding HTML target.

    Returns None if the source has no HTML mapping.
    """
    if not (source.endswith(".md") or source.endswith(".yaml") or source.endswith(".yml")):
        return None

    for prefix, html_dir in SOURCE_TO_HTML:
        if source.startswith(prefix):
            # Extract relative path after prefix
            rel = source[len(prefix):]
            # Convert name.md → name.html (strip all extensions)
            name = re.sub(r"\.(md|yaml|yml)$", "", Path(rel).name)
            # Preserve subdirectories only for design-kit (many subfolders)
            if prefix == "design-kit/docs/design/":
                subdir = str(Path(rel).parent) + "/" if Path(rel).parent != Path(".") else ""
                return f"{html_dir}{subdir}{name}.html"
            return f"{html_dir}{name}.html"
    return None


def detect_drift(since: str) -> list[DriftEntry]:
    sources = changed_files(since)
    registry = load_registry()
    entries: list[DriftEntry] = []
    seen: set[tuple[str, str]] = set()
    for src in sources:
        candidate = map_source_to_html(src)
        if candidate is None:
            continue
        target, registered, exists = resolve_target(candidate, registry)
        key = (src, target)
        if key in seen:
            continue
        seen.add(key)
        entries.append(
            DriftEntry(
                source=src, target=target, registered=registered, exists=exists
            )
        )
    return entries


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--since",
        default="main",
        help="비교 기준 git ref (기본: main)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="JSON array 형식으로 출력",
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Verbose logs"
    )
    args = parser.parse_args()

    entries = detect_drift(args.since)

    if args.json:
        print(json.dumps([e.to_dict() for e in entries], ensure_ascii=False, indent=2))
    else:
        if not entries:
            print(f"no docs drift since {args.since}")
        else:
            for e in entries:
                if not e.exists:
                    mark = "  [NEW — 대응 HTML 없음, 신규 생성 + index.html 등록 필요]"
                elif not e.registered:
                    mark = "  [UNREGISTERED — 파일은 있으나 index.html 미등록]"
                else:
                    mark = ""
                print(f"{e.source} → {e.target}{mark}")
            if args.verbose:
                new_count = sum(1 for e in entries if not e.exists)
                print(f"\nTotal: {len(entries)} HTML pages need regeneration"
                      f" ({new_count} new)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
