#!/usr/bin/env python3
"""check-api-kit-docs.py 시험 — 공통 CSS 연결 판정을 임시 폴더의 원본 · 쪽 짝 다섯 경우로 돌린다. 레포 파일은 건드리지 않는다.

  1. `<link rel="stylesheet" href="../assets/site.css">` → 연결 있음
  2. `<link href='../assets/site.css' rel=stylesheet>` → 연결 있음
  3. `<link rel="preload" as="style" href="../assets/site.css">` 만 → 연결 없음
  4. `<link rel="stylesheet" href="../assets/site.css.bak">` 만 → 연결 없음
  5. 연결이 HTML 주석 안에만 → 연결 없음

검사 파일의 `check(원본, 쪽)` 을 불러 실패 목록에 「공통 CSS」 줄이 있는지 본다. 다른 검사(줄 수 · accent · 테마 키)는
통과하게 쪽을 만든다.

사용법:
    python3 scripts/test-check-api-kit-docs.py [--check <검사 사본 경로>]

--check 는 음성 대조용이다 — 시작 판(ab637374) 검사처럼 rel 을 안 보고 주소 끝을 `\\b` 로 자르는 사본은 경우 3 · 4 가 실패해야 한다.
종료 코드는 harness/evals/gate-exit-codes.md 를 따른다 (0 통과 · 1 실패 · 2 준비 실패).
"""

import argparse
import importlib.util
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

CASES = [
    ("1 큰따옴표 stylesheet 링크", '<link rel="stylesheet" href="../assets/site.css">', True),
    ("2 작은따옴표 주소 · 따옴표 없는 rel", "<link href='../assets/site.css' rel=stylesheet>", True),
    ("3 preload 링크만", '<link rel="preload" as="style" href="../assets/site.css">', False),
    ("4 site.css.bak 링크만", '<link rel="stylesheet" href="../assets/site.css.bak">', False),
    ("5 주석 안 링크만", '<!-- <link rel="stylesheet" href="../assets/site.css"> -->', False),
]


def load(check: Path):
    spec = importlib.util.spec_from_file_location("check_api_kit_docs", check)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def page(head: str, accent: str) -> str:
    filler = "\n".join("<p>본문</p>" for _ in range(460))
    return (f"<!DOCTYPE html>\n<html><head>{head}<style>:root{{--accent:{accent}}}</style></head>\n"
            f"<body>\n{filler}\n<script>localStorage.getItem('dk-theme')</script></body></html>\n")


def linked(module, tmp: Path, name: str, head: str) -> bool:
    module.REPO = tmp
    md = tmp / "docs/api" / f"{name}.md"
    html = tmp / "docs/api-kit" / f"{name}.html"
    md.parent.mkdir(parents=True, exist_ok=True)
    html.parent.mkdir(parents=True, exist_ok=True)
    md.write_text("# 제목\n\n본문\n", encoding="utf-8")
    html.write_text(page(head, module.ACCENT), encoding="utf-8")
    return not any("공통 CSS" in fail for fail in module.check(md, html)["fail"])


def main() -> int:
    parser = argparse.ArgumentParser(description="check-api-kit-docs.py 시험")
    parser.add_argument("--check", type=Path, default=REPO_ROOT / "scripts/check-api-kit-docs.py")
    args = parser.parse_args()
    if not args.check.is_file():
        print(f"ERROR: 검사가 없다 — {args.check}")
        return 2
    module = load(args.check.resolve())
    passed = 0
    with tempfile.TemporaryDirectory() as tmp:
        for number, (label, head, want) in enumerate(CASES, 1):
            got = linked(module, Path(tmp), f"case{number}", head)
            passed += got == want
            print(f"{'PASS' if got == want else 'FAIL'} 경우 {label} (연결 기대 {want} · 판정 {got})")
    print(f"경우 {len(CASES)} 개 중 통과 {passed}")
    return 0 if passed == len(CASES) else 1


if __name__ == "__main__":
    sys.exit(main())
