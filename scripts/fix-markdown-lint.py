#!/usr/bin/env python3
"""
fix-markdown-lint.py — markdownlint auto-fix 스크립트

지원 규칙:
  MD031 — Fenced code blocks should be surrounded by blank lines
  MD032 — Lists should be surrounded by blank lines
  MD034 — Bare URL used (autolink `<url>` 으로 감싸기)
  MD060 — Table column style (separator row 에 spaces 추가)

사용법:
    python3 scripts/fix-markdown-lint.py <path> [options]

인자:
    <path>   파일 또는 디렉토리 (디렉토리면 재귀적으로 `*.md` 처리)

옵션:
    --dry-run    변경 내용만 출력하고 파일 수정 안 함
    --rules <csv> 적용할 규칙 (기본 전체)
    --help       사용법 출력
"""

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

FENCE_RE = re.compile(r"^(\s*)```")
LIST_RE = re.compile(r"^(\s*)[-*+] ")
URL_RE = re.compile(r"(?<![\[<(`])(https?://[^\s)>\]]+)(?!\])")
TABLE_SEP_RE = re.compile(r"^\|[-|]+\|\s*$")


def fix_md060_line(line: str) -> str:
    """Table separator row: convert |----|----| to | ---- | ---- |"""
    if not TABLE_SEP_RE.match(line.strip()):
        return line
    stripped = line.rstrip("\n")
    parts = stripped.split("|")
    new_parts = []
    for i, p in enumerate(parts):
        if p == "":
            new_parts.append("")
        else:
            n = max(len(p), 3)
            new_parts.append(" " + "-" * n + " ")
    return "|".join(new_parts) + "\n"


def fix_md034_line(line: str) -> str:
    """Wrap bare URLs as <url> autolinks.

    Skip URLs already inside [text](url) or <url> or `code`.
    """
    # Guard: if the line is inside a table cell or contains markdown links,
    # be conservative and only wrap raw URLs.
    def wrap(match: re.Match) -> str:
        url = match.group(1)
        start = match.start()
        # Look at character immediately before the URL
        if start > 0 and line[start - 1] in "(<`":
            return url  # already inside link/code
        return f"<{url}>"

    return URL_RE.sub(wrap, line)


def fix_markdown(text: str, rules: set[str]) -> str:
    lines = text.splitlines(keepends=True)
    out: list[str] = []

    in_fence = False

    i = 0
    while i < len(lines):
        line = lines[i]

        fence_match = FENCE_RE.match(line)

        # MD060: table separator
        if "md060" in rules and TABLE_SEP_RE.match(line.strip()):
            line = fix_md060_line(line)

        # MD034: bare URLs
        if "md034" in rules and not in_fence:
            line = fix_md034_line(line)

        # MD031: blank line before opening fence
        if "md031" in rules and fence_match:
            if not in_fence:
                # Opening fence — ensure previous output is blank
                if out and out[-1].strip() != "":
                    out.append("\n")
            in_fence = not in_fence
            out.append(line)
            # After closing fence, ensure next non-empty line has a blank line before it
            if "md031" in rules and not in_fence:
                # Peek ahead
                if i + 1 < len(lines):
                    next_line = lines[i + 1]
                    if next_line.strip() != "":
                        out.append("\n")
            i += 1
            continue

        # MD032: blank line before list
        if "md032" in rules and LIST_RE.match(line) and not in_fence:
            if out and out[-1].strip() != "" and not LIST_RE.match(out[-1]):
                out.append("\n")

        out.append(line)
        i += 1

    # Join
    result = "".join(out)

    # Collapse triple+ blank lines to double
    result = re.sub(r"\n{3,}", "\n\n", result)

    return result


def iter_md_files(path: Path) -> list[Path]:
    if path.is_file():
        return [path] if path.suffix == ".md" else []
    if path.is_dir():
        return sorted(path.rglob("*.md"))
    return []


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", default=".", help="파일 또는 디렉토리")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--rules",
        default="md031,md032,md034,md060",
        help="적용할 규칙 (csv)",
    )
    args = parser.parse_args()

    target = Path(args.path)
    if not target.exists():
        print(f"ERROR: {target} 없음", file=sys.stderr)
        return 2

    rules = {r.strip().lower() for r in args.rules.split(",") if r.strip()}

    files = iter_md_files(target)
    if not files:
        print(f"no .md files under {target}")
        return 0

    changed = 0
    for f in files:
        original = f.read_text(encoding="utf-8")
        fixed = fix_markdown(original, rules)
        if fixed != original:
            if args.dry_run:
                print(f"[DRY] would fix: {f}")
            else:
                f.write_text(fixed, encoding="utf-8")
                print(f"fixed: {f}")
            changed += 1

    print(f"\nTotal: {changed} / {len(files)} files fixed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
