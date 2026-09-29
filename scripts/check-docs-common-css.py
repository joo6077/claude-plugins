#!/usr/bin/env python3
"""문서 사이트 쪽마다 공통 CSS 링크가 하나인지, 이름을 글자 참조나 태그로 쪼개 적지 않았는지 잰다.

글자 수로 재면 본문에 `site.css` 라는 이름을 적은 것까지 링크로 세고, 그걸 피하려고 쪽 글에서
`site&#46;css` 처럼 쪼개 적는 우회가 생겼다. 이 검사는 `<link>` 요소를 세므로 본문 글은 원래 글자로 적어도 된다.

사용법:
    python3 scripts/check-docs-common-css.py            # git 이 추적하는 docs/ 아래 HTML 전부
    python3 scripts/check-docs-common-css.py <파일...>  # 준 파일만

쪽마다 어긋나면 한 줄로 적는다:
  - `assets/site.css` 를 가리키는 `<link>` 가 1 개가 아니다 (HTML 주석 안은 세지 않는다)
  - 쪽 `<style>` 에 `prefers-reduced-motion` 규칙을 다시 적었다 — 움직임 줄이기는 공통 파일이 맡는다.
    `<style media="(prefers-reduced-motion: …)">` · `<link media="(prefers-reduced-motion: …)">` 처럼
    태그의 media 속성에 적은 것도 같다. `media="print"` 같은 다른 조건과 HTML · CSS 주석,
    본문 글 · `<script>` 의 `matchMedia` 는 세지 않는다
  - `site.css` · `prefers-reduced-motion` 을 쪼개 적은 자리가 있다 — 숫자 글자 참조(`&#46;` · `&#x2d;`),
    이름 글자 참조(`&period;` · `&dash;` · `&hyphen;`), 태그 끼우기(`site<span>.</span>css`) 모두

종료 코드는 harness/evals/gate-exit-codes.md 를 따른다 — 0 통과 · 1 어긋남 · 2 못 읽음 · 3 대상 없음.
못 읽은 쪽과 어긋난 쪽이 함께 있으면 2 를 내고 둘 다 적는다.
"""

import html
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

COMMENT_RE = re.compile(r"<!--.*?-->", re.S)
LINK_RE = re.compile(r"<link\b[^>]*>", re.I | re.S)
SITE_CSS_HREF_RE = re.compile(r"""\bhref\s*=\s*(?:"[^"]*assets/site\.css[^"]*"|'[^']*assets/site\.css[^']*'|[^\s"'>]*assets/site\.css[^\s"'>]*)""", re.I)
TAG_RE = re.compile(r"(<[^>]*>)")
STYLE_RE = re.compile(r"<style\b[^>]*>(.*?)</style>", re.I | re.S)
MEDIA_TAG_RE = re.compile(r"<(?:style|link)\b[^>]*>", re.I | re.S)
MEDIA_ATTR_RE = re.compile(r"""\bmedia\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s"'>]+))""", re.I)
CSS_COMMENT_RE = re.compile(r"/\*.*?\*/", re.S)
WATCHED_NAMES = ("site.css", "prefers-reduced-motion")
# `&dash;` · `&hyphen;` 은 풀면 `-` 가 아니라 U+2010 이다. 보이는 모양이 같은 글자와 보이지 않는 글자를 맞춰 둔다
LOOKALIKES = str.maketrans({"\u2010": "-", "\u2011": "-", "\u2012": "-", "\u2013": "-", "\u2212": "-",
                            "\u00ad": None, "\u200b": None, "\u200c": None, "\u200d": None, "\u2060": None})


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


def style_motion_rules(text: str) -> int:
    """`<style>` 안이나 `<style>` · `<link>` 의 media 속성에서 `prefers-reduced-motion` 을 쓴 자리 수.
    공통 파일과 겹쳐 적으면 쪽마다 규칙이 갈린다."""
    text = COMMENT_RE.sub("", text)
    blocks = sum(1 for css in STYLE_RE.findall(text)
                 if "prefers-reduced-motion" in html.unescape(CSS_COMMENT_RE.sub("", css)).lower())
    media = sum(1 for tag in MEDIA_TAG_RE.findall(text) for value in MEDIA_ATTR_RE.findall(tag)
                if "prefers-reduced-motion" in html.unescape("".join(value)).lower())
    return blocks + media


def split_names(text: str) -> int:
    """글자 참조를 풀고 태그를 걷어 내면 나타나는데 원문에는 그대로 없는 이름의 수.

    숫자 참조 꼴만 찾으면 `&period;` 나 `site<span>.</span>css` 로 쪼갠 우회가 그대로 지나간다.
    """
    parts = TAG_RE.split(COMMENT_RE.sub("", text).lower())
    texts, tags = parts[0::2], parts[1::2]
    decoded = [chunk.translate(LOOKALIKES) for chunk in (html.unescape("".join(texts)), *map(html.unescape, tags))]
    splits = 0
    for name in WATCHED_NAMES:
        written = sum(part.count(name) for part in parts)
        revealed = sum(chunk.count(name) for chunk in decoded)
        splits += max(revealed - written, 0)
    return splits


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
        links, splits, motion = site_css_links(text), split_names(text), style_motion_rules(text)
        if links != 1 or splits or motion:
            mismatched += 1
            print(f"BAD {shown(page)} site_css_links={links} split_names={splits} style_motion={motion}")

    print(f"검사한 쪽 {checked} · 어긋난 쪽 {mismatched} · 못 읽은 쪽 {unreadable}")
    if unreadable:
        return 2
    return 1 if mismatched else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
