#!/usr/bin/env python3
"""norm.py <옛 폴더> <새 폴더> <목록 파일> — 목록의 md 마다 모양 표식을 떼고 낱말 순서가 같은지 잰다.

떼는 것: 빈 줄 · 줄 앞뒤 공백, 코드 블록 여는 줄의 언어 이름, 줄 머리의 번호 목록 숫자,
문자 # * | < >, 표 구분처럼 - 와 : 로만 된 낱말, 새 판의 좁힌 끄기 주석 줄
(<!-- markdownlint-disable-next-line MDnnn ... --> 한 줄 전체).
출력: 다른 파일마다 `MISMATCH <경로> at=<낱말 위치> old=[..] new=[..]`, 끝에 요약 한 줄
`files=<목록 수> changed=<바이트가 바뀐 파일 수> mismatch=<낱말 순서가 다른 파일 수> disables=<새 판 좁힌 끄기 주석 수> missing=<못 읽은 파일 수>`.
종료 코드: 0 = mismatch 0 · missing 0, 1 = 그 밖.
"""
import re
import sys
from pathlib import Path

DISABLE = re.compile(r"^\s*<!-- markdownlint-disable-next-line( MD\d{3})+ -->\s*$")
FENCE = re.compile(r"^(\s*)(`{3,}|~{3,})\s*[A-Za-z0-9_+#.-]*\s*$")
OL = re.compile(r"^\s*\d+[.)](?=\s)")
MARKS = re.compile(r"[#*|<>]")
RULE = re.compile(r"^[-:]+$")


def tokens(text: str) -> tuple[list[str], int]:
    out: list[str] = []
    disables = 0
    for line in text.splitlines():
        if DISABLE.match(line):
            disables += 1
            continue
        m = FENCE.match(line)
        if m:
            line = m.group(2)
        line = OL.sub("N.", line)
        line = MARKS.sub(" ", line)
        out.extend(t for t in line.split() if not RULE.match(t))
    return out, disables


def main() -> int:
    old_dir, new_dir, listing = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    paths = [p for p in listing.read_text(encoding="utf-8").splitlines() if p.strip()]
    changed = mismatch = disables = missing = 0
    for p in paths:
        a, b = old_dir / p, new_dir / p
        if not a.is_file() or not b.is_file():
            missing += 1
            print(f"MISSING {p}")
            continue
        ra, rb = a.read_bytes(), b.read_bytes()
        if ra != rb:
            changed += 1
        ta, _ = tokens(ra.decode("utf-8"))
        tb, nb = tokens(rb.decode("utf-8"))
        disables += nb
        if ta != tb:
            mismatch += 1
            i = next((k for k in range(min(len(ta), len(tb))) if ta[k] != tb[k]), min(len(ta), len(tb)))
            print(f"MISMATCH {p} at={i} old={ta[i:i + 4]} new={tb[i:i + 4]}")
    print(f"files={len(paths)} changed={changed} mismatch={mismatch} disables={disables} missing={missing}")
    return 0 if mismatch == 0 and missing == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
