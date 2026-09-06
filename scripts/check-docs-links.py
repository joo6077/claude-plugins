#!/usr/bin/env python3
"""check-docs-links.py — docs/ 의 내부 링크와 내비게이션 등록 상태를 확인한다.

세 가지를 본다.

1. **내부 상대링크** — `href`/`src` 가 실재하는 파일을 가리키는가.

문서 사이트는 iframe 으로 페이지를 갈아끼우고 페이지끼리 상대경로로 서로를 인용한다.
경로가 죽으면 화면에는 아무 표시도 안 나고 클릭했을 때만 드러나므로, 사람 눈으로는 안 잡힌다.

2. **고아 페이지** — `docs/` 에 있는데 `docs/index.html` 의 `categories` 에 없는 페이지.
   내비게이션에서 도달할 수 없으니 아무도 못 본다.
3. **유령 등록 · 아이콘 누락** — 등록됐는데 파일이 없거나, 등록됐는데 `getIcon()` 에 아이콘이 없는 id.

2·3 이 왜 필요한가 (실측 2026-09-06): `docs/harness/` 에 2026-03-31 판 요약 페이지 4 개가
소스 `.md` 도 없이 남아 있었고 내비에도 없었다. 그런데 살아있는 `feedback-system.html` 이
그 죽은 페이지들을 링크하고 있었고, 사실 감사의 수정 하나가 **아무도 못 보는 그 페이지로 들어갔다.**
링크만 검사해서는 이 상태가 안 보인다 — 링크 자체는 멀쩡했기 때문이다.

외부 URL(http/https)·앵커(#)·mailto·data: 는 대상이 아니다. 이건 **레포 안에서 대조 가능한
경로만** 본다 — 레포 밖 값을 추측으로 판정하지 않는다는 같은 원칙이다.

Usage:
    python3 scripts/check-docs-links.py
    python3 scripts/check-docs-links.py --json

exit 0 = 깨진 링크 없음, 1 = 있음.
"""
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DOCS = REPO / "docs"

SKIP = ("http://", "https://", "//", "#", "mailto:", "data:", "javascript:", "tel:")


class LinkCollector(HTMLParser):
    """실제 태그의 속성만 모은다.

    정규식으로 `href="..."` 를 훑으면 **코드 예제 안의 이스케이프된 마크업**까지 잡힌다.
    실측: `&lt;img src="hero.webp" ...&gt;` 같은 설명용 예제가 "깨진 링크" 로 보고됐다.
    예제를 고치라고 시키는 게이트는 쓸모가 없으므로 파서로 진짜 속성만 본다.
    """

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links = []

    def handle_starttag(self, tag, attrs):
        for name, value in attrs:
            if name in ("href", "src") and value:
                self.links.append((self.getpos()[0], value))


def main() -> int:
    broken = []
    checked = 0
    for f in sorted(DOCS.rglob("*.html")):
        text = f.read_text(encoding="utf-8", errors="replace")
        c = LinkCollector()
        try:
            c.feed(text)
        except Exception as e:  # 파싱 실패는 조용히 넘기지 않는다
            print(f"WARN {f.relative_to(REPO)}: 파싱 실패 {e}", file=sys.stderr)
            continue
        for lineno, raw in c.links:
            if raw.startswith(SKIP) or not raw.strip():
                continue
            path = raw.split("#", 1)[0].split("?", 1)[0]
            if not path:
                continue
            checked += 1
            target = (f.parent / path).resolve()
            if not target.exists():
                broken.append({
                    "file": str(f.relative_to(REPO)),
                    "line": lineno,
                    "href": raw,
                    "resolved": str(target),
                })

    # ── 내비게이션 등록 상태 ──
    idx = (DOCS / "index.html").read_text(encoding="utf-8")
    registered = set(re.findall(r"file: '([^']+)'", idx))
    ids = re.findall(r"\{ id: '([^']+)'", idx)
    icons = set(re.findall(r"'([a-z0-9-]+)':\s*'<svg", idx))
    pages = {str(p.relative_to(DOCS)) for p in DOCS.rglob("*.html") if p.name != "index.html"}
    orphans = sorted(pages - registered)
    ghosts = sorted(f for f in registered if not (DOCS / f).exists())
    no_icon = [i for i in ids if i not in icons]

    if "--json" in sys.argv:
        print(json.dumps({"checked": checked, "broken": broken, "orphans": orphans,
                          "ghosts": ghosts, "missing_icons": no_icon}, ensure_ascii=False, indent=1))
    else:
        print(f"내부 상대링크 {checked} 개 검사")
        if broken:
            print(f"깨진 링크 {len(broken)} 개:\n")
            for b in broken:
                print(f"  {b['file']}:{b['line']}  href=\"{b['href']}\"")
        else:
            print("깨진 링크 없음")
        print(f"\n내비 등록: 페이지 {len(pages)} · 등록 {len(registered)}")
        for o in orphans:
            print(f"  고아 (내비 미등록): {o}")
        for g in ghosts:
            print(f"  유령 (등록됐으나 파일 없음): {g}")
        for i in no_icon:
            print(f"  아이콘 누락: {i}")
        if not (orphans or ghosts or no_icon):
            print("  고아 · 유령 · 아이콘 누락 없음")
    return 1 if (broken or orphans or ghosts or no_icon) else 0


if __name__ == "__main__":
    sys.exit(main())
