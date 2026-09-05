#!/usr/bin/env python3
"""api-kit docs-site 페이지 검증 — 소스 .md 의 출처 URL 이 HTML 에 모두 옮겨졌는지 대조한다.

`> **출처:** [이름](URL)` 형태의 인용을 소스에서 뽑고, HTML 의 `href="URL"` 집합과 비교한다.
QA 최다 반려 사유(출처 링크 누락)를 커밋 전에 잡는 것이 목적이다.

대조는 양방향이다. 소스→HTML 누락은 **실패**, HTML→소스 초과는 **보고만** 한다.
초과분은 저자가 본문에서 직접 든 비교 대상 문서일 수 있어 그 자체로 결함이 아니지만,
단방향으로만 보면 소스에 근거가 없는 URL 이 페이지에 새로 들어와도 영원히 안 걸린다
(2026-09-05 QA 지적). 초과분은 출처를 사람이 한 번 확인하라는 신호다.

Usage:
    python3 scripts/check-api-kit-docs.py            # 전체 검사
    python3 scripts/check-api-kit-docs.py --json     # 기계 판독용
"""
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SRC_DIR = REPO / "docs" / "api"
OUT_DIR = REPO / "docs" / "api-kit"

MIN_LINES = 450
ACCENT = "#A3E635"

# 소스 .md 의 출처 인용에서 URL 만 뽑는다. `> **출처:**` 한 줄에 여러 링크가 올 수 있다.
SOURCE_LINE = re.compile(r"^>\s*\*\*출처[^\n]*", re.MULTILINE)
MD_URL = re.compile(r"\]\((https?://[^)\s]+)\)")
HTML_HREF = re.compile(r'href="(https?://[^"]+)"')

# 외부 리소스 — standalone 위반
EXTERNAL = re.compile(r'<link\s|<script[^>]+src=|@import\s|url\(\s*[\'"]?https?://')
# 오버플로 억제 — 내용 손실이므로 금지 (overflow-x:auto 는 허용)
SUPPRESS = re.compile(r"overflow\s*:\s*hidden|overflow-x\s*:\s*hidden")


def sources_of(md: Path) -> set[str]:
    text = md.read_text(encoding="utf-8")
    urls: set[str] = set()
    for line in SOURCE_LINE.findall(text):
        urls.update(MD_URL.findall(line))
    return urls


def check(md: Path, html: Path) -> dict:
    r = {"src": str(md.relative_to(REPO)), "html": str(html.relative_to(REPO)), "fail": []}
    if not html.exists():
        r["fail"].append("HTML 없음")
        return r

    body = html.read_text(encoding="utf-8")
    r["lines"] = body.count("\n") + 1
    if r["lines"] < MIN_LINES:
        r["fail"].append(f"줄 수 {r['lines']} < {MIN_LINES}")

    want = sources_of(md)
    have = set(HTML_HREF.findall(body))
    missing = sorted(want - have)
    r["src_urls"] = len(want)
    r["missing_urls"] = missing
    r["extra_urls"] = sorted(have - want)
    if missing:
        r["fail"].append(f"출처 URL 누락 {len(missing)} 건")

    if ACCENT not in body:
        r["fail"].append(f"accent {ACCENT} 없음")
    if EXTERNAL.search(body):
        r["fail"].append("외부 리소스 참조")
    if SUPPRESS.search(body):
        r["fail"].append("overflow 억제")
    if "prefers-reduced-motion" not in body:
        r["fail"].append("prefers-reduced-motion 없음")
    if "dk-theme" not in body:
        r["fail"].append("테마 키 dk-theme 없음")
    return r


def main() -> int:
    results = []
    for md in sorted(SRC_DIR.rglob("*.md")):
        if md.name == "research-log.md":
            continue
        results.append(check(md, OUT_DIR / (md.stem + ".html")))

    if "--json" in sys.argv:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        for r in results:
            mark = "OK  " if not r["fail"] else "FAIL"
            extra = f" lines={r.get('lines','-')} src_urls={r.get('src_urls','-')}"
            print(f"{mark} {r['html']}{extra}")
            for f in r["fail"]:
                print(f"       └ {f}")
            for u in r.get("missing_urls", []):
                print(f"       └ 누락: {u}")
            for u in r.get("extra_urls", []):
                print(f"       · 소스에 없는 인용(확인 필요): {u}")

    bad = [r for r in results if r["fail"]]
    print(f"\n{len(results) - len(bad)}/{len(results)} PASS")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
