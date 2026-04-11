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


@dataclass
class DriftEntry:
    source: str
    target: str

    def to_dict(self) -> dict:
        return {"source": self.source, "target": self.target}


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
    entries: list[DriftEntry] = []
    seen: set[tuple[str, str]] = set()
    for src in sources:
        target = map_source_to_html(src)
        if target is None:
            continue
        key = (src, target)
        if key in seen:
            continue
        seen.add(key)
        entries.append(DriftEntry(source=src, target=target))
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
                print(f"{e.source} → {e.target}")
            if args.verbose:
                print(f"\nTotal: {len(entries)} HTML pages need regeneration")

    return 0


if __name__ == "__main__":
    sys.exit(main())
