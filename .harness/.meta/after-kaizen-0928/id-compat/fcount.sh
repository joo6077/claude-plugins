#!/bin/bash
# 문서에 적힌 기능 조건 세기 awk 첫 번째를 꺼내 계약 하나에 돌린다.
# 쓰는 법: bash fcount.sh <문서.md> <계약>
prog=$(python3 - "$1" <<'PY'
import re, sys
t = open(sys.argv[1], encoding="utf-8").read()
m = re.search(r"awk '(/\^## /\{s=\$\(0\)\}[^']*)'", t)
print(m.group(1) if m else "", end="")
PY
)
[ -n "$prog" ] || { echo "NO_PROGRAM"; exit 2; }
awk "$prog" "$2"
