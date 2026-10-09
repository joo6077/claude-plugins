#!/usr/bin/env bash
# hs5.sh <풀어 둔 판> — 종료 코드 정의 파일을 인용하는 스크립트 집합과 「소비처」 표 행 집합을 맞댄다
R=${1:?}; cd "$R" || exit 2
G=harness/evals/gate-exit-codes.md
[ -f "$G" ] || exit 2
cite=$(grep -rl --include='*.py' --include='*.sh' --include='*.js' 'gate-exit-codes' scripts harness/scripts harness/evals | grep -vxF "$G" | LC_ALL=C sort -u)
rows=$(awk '/^## 소비처/{f=1;next} f&&/^## /{exit} f&&/^\| `/{s=$0; sub(/^\| `/,"",s); sub(/`.*/,"",s); print s}' "$G" | LC_ALL=C sort -u)
miss=$(LC_ALL=C comm -23 <(printf '%s\n' "$cite") <(printf '%s\n' "$rows") | grep -c .)
extra=$(LC_ALL=C comm -13 <(printf '%s\n' "$cite") <(printf '%s\n' "$rows") | grep -c .)
echo "cite=$(printf '%s\n' "$cite" | grep -c .) rows=$(printf '%s\n' "$rows" | grep -c .) missing=$miss extra=$extra"
LC_ALL=C comm -23 <(printf '%s\n' "$cite") <(printf '%s\n' "$rows") | sed 's/^/  missing /'
awk '/^## 소비처/{f=1;next} f&&/^## /{exit} f&&/^\| `/' "$G"
