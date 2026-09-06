#!/usr/bin/env python3
"""check-external-links.py — 문서가 인용한 외부 URL 이 아직 살아 있는지 확인한다.

이 레포의 문서는 "원칙 하나당 출처 하나" 를 규약으로 삼는다. 그 링크가 404 면 규약이
빈 껍데기가 된다 — 독자가 「출처」를 눌렀을 때 없는 페이지가 뜨기 때문이다.

**CI 게이트가 아니다.** 네트워크와 상대 서버 상태에 의존해서 CI 에 넣으면 남의 사이트가
느린 날 빌드가 깨진다. 주기적으로 손으로 돌리고 결과를 보고 고치는 용도다.

실측 2026-09-06: 고유 URL 1361 개 중 **40 개가 404/410** 이었다. 대부분 사이트 개편으로
경로가 바뀐 것이고(m3.material.io · nngroup · tailwind · tokio · redis 등), 하나는
GitHub 계정명 오타였다.

판정 주의:
- `403` 은 죽은 게 아니라 봇 차단인 경우가 많다 (실측 41 건). 실패로 세지 않는다.
- `429` 는 rate limit 이므로 재시도 대상이다.
- 마크다운 `](url)` 추출은 첫 `)` 에서 끊긴다. `Nudge_(book)` 처럼 URL 안에 괄호가 있으면
  잘려서 가짜 404 가 된다 — 괄호 균형을 맞춰 복원한다.

Usage:
    python3 scripts/check-external-links.py               # 전수 검사
    python3 scripts/check-external-links.py --list        # URL 목록만 출력 (검사 안 함)
    python3 scripts/check-external-links.py --jobs 24     # 동시 요청 수

exit 0 = 404/410 없음, 1 = 있음.
"""
import argparse
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
KIT_DIRS = ["docs", "design-kit", "harness", "api-kit", "tone-kit", "flutter-toolkit",
            "backend-kit", "infra-kit", "rust-kit", "react-kit", "planning-kit",
            "reflect-kit", "bambu-kit", "onboarding-kit"]
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/125 Safari/537.36")
DEAD = {"404", "410"}


class LinkCollector(HTMLParser):
    """실제 태그 속성만 모은다 — 코드 예제 안의 이스케이프된 마크업을 링크로 세지 않는다."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.urls = set()

    def handle_starttag(self, tag, attrs):
        for name, value in attrs:
            if name in ("href", "src") and value and value.startswith(("http://", "https://")):
                self.urls.add(value)


def balance(url: str) -> str:
    """마크다운 추출이 잘라낸 닫는 괄호를 복원하고 문장부호를 떼어낸다."""
    url = url.rstrip(".,;")
    while url.endswith(")") and url.count("(") < url.count(")"):
        url = url[:-1]
    return url


def collect() -> set[str]:
    urls: set[str] = set()
    for html in (REPO / "docs").rglob("*.html"):
        c = LinkCollector()
        try:
            c.feed(html.read_text(encoding="utf-8", errors="replace"))
        except Exception:
            continue
        urls |= c.urls
    md_link = re.compile(r"\]\((https?://[^)\s]+\)?)")
    for d in KIT_DIRS:
        for md in (REPO / d).rglob("*.md"):
            urls |= set(md_link.findall(md.read_text(encoding="utf-8", errors="replace")))
    return {balance(u) for u in urls}


def probe(url: str, timeout: int) -> tuple[str, str]:
    r = subprocess.run(
        ["curl", "-sSL", "-o", "/dev/null", "-w", "%{http_code}",
         "--max-time", str(timeout), "-A", UA, url],
        capture_output=True, text=True)
    return (r.stdout.strip() or "000"), url


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--jobs", type=int, default=16)
    ap.add_argument("--timeout", type=int, default=20)
    ap.add_argument("--list", action="store_true")
    args = ap.parse_args()

    urls = sorted(collect())
    if args.list:
        print("\n".join(urls))
        return 0

    print(f"고유 외부 URL {len(urls)} 개 검사 (동시 {args.jobs})")
    with ThreadPoolExecutor(max_workers=args.jobs) as ex:
        results = list(ex.map(lambda u: probe(u, args.timeout), urls))

    # 429 는 rate limit — 한 번 더 준다
    retry = [u for c, u in results if c == "429"]
    if retry:
        print(f"  429 {len(retry)} 건 재시도")
        with ThreadPoolExecutor(max_workers=4) as ex:
            again = {u: c for c, u in ex.map(lambda u: probe(u, args.timeout), retry)}
        results = [(again.get(u, c), u) for c, u in results]

    buckets: dict[str, list[str]] = {}
    for code, u in results:
        buckets.setdefault(code, []).append(u)
    for code in sorted(buckets, key=lambda c: -len(buckets[c])):
        note = ""
        if code == "403":
            note = "  (봇 차단일 수 있음 — 실패로 세지 않는다)"
        elif code == "000":
            note = "  (연결 실패 — 네트워크 또는 상대 서버)"
        print(f"  {code}: {len(buckets[code])}{note}")

    dead = sorted(u for c, u in results if c in DEAD)
    if dead:
        print(f"\n죽은 링크 {len(dead)} 개:")
        for u in dead:
            print(f"  {u}")
    else:
        print("\n죽은 링크 없음")
    return 1 if dead else 0


if __name__ == "__main__":
    sys.exit(main())
