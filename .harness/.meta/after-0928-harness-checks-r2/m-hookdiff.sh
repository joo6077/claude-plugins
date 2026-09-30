#!/usr/bin/env bash
# m-hookdiff.sh <고치기 전 사본> <지금 훅> — 두 파일에서 value() 함수(`function value(line…) {` 줄부터 처음 나오는 `}` 줄까지)를
# 뺀 나머지가 같은지 본다. 함수 밖을 건드리지 않았는지(최소 변경) 재는 것이다.
# 출력 한 줄: `outside_diff=<함수 밖 차이 줄 수> fn=<두 파일 모두 함수가 있으면 1> syntax=<지금 훅 bash -n 종료 코드>`
A=${1:?사본}; B=${2:?훅}
[ -f "$A" ] && [ -f "$B" ] || { echo "STOP 파일이 없다"; exit 2; }
strip() { awk '/^[[:space:]]*function value\(line[^)]*\) \{/{s=1} !s{print} s && /^[[:space:]]*\}[[:space:]]*$/{s=0}' "$1"; }
fn=1; for f in "$A" "$B"; do grep -qE '^[[:space:]]*function value\(line[^)]*\) \{' "$f" || fn=0; done
n=$(diff <(strip "$A") <(strip "$B") | grep -c .)
bash -n "$B" 2>/dev/null; s=$?
echo "outside_diff=$n fn=$fn syntax=$s"
