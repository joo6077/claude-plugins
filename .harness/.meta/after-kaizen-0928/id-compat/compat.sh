#!/bin/bash
# 옛 계약 목록의 조건 수 · 두 지문 · 봉인 판정을 한 줄씩 낸다. 레포 뿌리에서 돌린다.
# 쓰는 법: bash .harness/.meta/after-kaizen-0928/id-compat/compat.sh [규약 문서] > 결과
# 조건 수는 규약 문서 contract_digest 의 정규식으로 센다 — 규약이 바뀌면 그 정규식으로 잰다.
here=$(cd "$(dirname "$0")" && pwd)
schema=${1:-harness/references/contract-schema.md}
MEASURE_SCHEMA="$schema" . harness/scripts/measure-common.sh || exit 2
rx=$(awk '/^contract_digest\(\)/ { getline; print; exit }' "$schema" | sed -E "s/.*grep -E '([^']*)'.*/\1/")
[ -n "$rx" ] || { echo "정규식을 못 찾았다: $schema" >&2; exit 2; }
while IFS= read -r f; do
  printf '%s %s %s %s %s %s\n' "$f" "$(grep -cE "$rx" "$f")" "$(contract_digest "$f")" \
    "$(measurement_digest "$f")" "$(verify_seal "$f" | cut -d' ' -f1)" "$(verify_measurement "$f" | cut -d' ' -f1)"
done < "$here/old-contracts.txt"
