#!/bin/bash
# regions.txt 의 모든 범위에 lone-ids.sh 를 돌려 한 줄씩 낸다. 레포 뿌리에서 돌린다.
# 끝 줄 not_clean 은 범위를 못 찾았거나 · 홀로 남은 줄이 있거나 · 한국어 번호가 한 줄도 없는 범위 수다.
here=$(cd "$(dirname "$0")" && pwd); total=0; bad=0
while IFS=$'\t' read -r f start stop; do
  out=$(bash "$here/lone-ids.sh" "$f" "$start" "$stop" 2>/dev/null); rc=$?
  printf '%s\t%s\t%s\n' "$f" "$start" "$out"
  total=$((total + 1)); lone=$(printf '%s' "$out" | sed -nE 's/.*lone=([0-9]+).*/\1/p'); ko=$(printf '%s' "$out" | sed -nE 's/.*ko=([0-9]+).*/\1/p')
  { [ "$rc" != 0 ] || [ "${lone:-x}" != 0 ] || [ "${ko:-0}" = 0 ]; } && bad=$((bad + 1))
done < "$here/regions.txt"
echo "regions=$total not_clean=$bad"
