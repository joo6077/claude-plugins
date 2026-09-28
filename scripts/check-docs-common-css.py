#!/usr/bin/env python3
"""문서 사이트 쪽마다 공통 CSS 링크가 하나인지, 이름을 숫자 글자 참조로 쪼개 적지 않았는지 잰다.

글자 수로 재면 본문에 `site.css` 라는 이름을 적은 것까지 링크로 세고, 그걸 피하려고 쪽 글에서
`site&#46;css` 처럼 쪼개 적는 우회가 생겼다. 이 검사는 `<link>` 요소를 세므로 본문 글은 원래 글자로 적어도 된다.

사용법:
    python3 scripts/check-docs-common-css.py            # git 이 추적하는 docs/ 아래 HTML 전부
    python3 scripts/check-docs-common-css.py <파일...>  # 준 파일만

쪽마다 어긋나면 한 줄로 적는다:
  - `assets/site.css` 를 가리키는 `<link>` 가 1 개가 아니다 (HTML 주석 안은 세지 않는다)
  - `site.css` · `prefers-reduced-motion` 을 숫자 글자 참조(`&#46;` · `&#45;` · `&#x2e;` · `&#x2d;`)로 쪼갠 자리가 있다

종료 코드는 harness/evals/gate-exit-codes.md 를 따른다 — 0 통과 · 1 어긋남 · 2 못 읽음 · 3 대상 없음.
못 읽은 쪽과 어긋난 쪽이 함께 있으면 2 를 내고 둘 다 적는다.
"""

import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

COMMENT_RE = re.compile(r"<!--.*?-->", re.S)
LINK_RE = re.compile(r"<link\b[^>]*>", re.I | re.S)
SITE_CSS_HREF_RE = re.compile(r"""\bhref\s*=\s*(?:"[^"]*assets/site\.css[^"]*"|'[^']*assets/site\.css[^']*'|[^\s"'>]*assets/site\.css[^\s"'>]*)""", re.I)
DOT = r"(?:\.|&#0*46;|&#x0*2e;)"
DASH = r"(?:-|&#0*45;|&#x0*2d;)"
SPLIT_NAME_RE = re.compile(rf"site{DOT}css|prefers{DASH}reduced{DASH}motion", re.I)


def tracked_pages() -> list[Path] | None:
    result = subprocess.run(
        ["git", "-C", str(REPO_ROOT), "ls-files", "docs/*.html"],
        capture_output=True, text=True, encoding="utf-8",
    )
    if result.returncode != 0:
        print(f"ERROR: git ls-files 실패 — {result.stderr.strip()}")
        return None
    return [REPO_ROOT / line for line in result.stdout.splitlines() if line.strip()]


def site_css_links(text: str) -> int:
    return sum(1 for tag in LINK_RE.findall(COMMENT_RE.sub("", text)) if SITE_CSS_HREF_RE.search(tag))


def split_names(text: str) -> int:
    return sum(1 for match in SPLIT_NAME_RE.finditer(text) if "&#" in match.group(0))


def shown(page: Path) -> str:
    try:
        return str(page.resolve().relative_to(REPO_ROOT))
    except ValueError:
        return str(page)


def main(argv: list[str]) -> int:
    if argv:
        pages = [Path(arg) for arg in argv]
    else:
        pages = tracked_pages()
        if pages is None:
            return 2
    if not pages:
        print("검사할 쪽이 없다 — 추적하는 docs/*.html 0 개")
        return 3

    checked, mismatched, unreadable = 0, 0, 0
    for page in pages:
        try:
            text = page.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as error:
            unreadable += 1
            print(f"UNREADABLE {shown(page)}: {error}")
            continue
        checked += 1
        links, splits = site_css_links(text), split_names(text)
        if links != 1 or splits:
            mismatched += 1
            print(f"BAD {shown(page)} site_css_links={links} split_names={splits}")

    print(f"검사한 쪽 {checked} · 어긋난 쪽 {mismatched} · 못 읽은 쪽 {unreadable}")
    if unreadable:
        return 2
    return 1 if mismatched else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
