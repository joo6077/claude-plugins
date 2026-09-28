#!/bin/bash
# .harness 계약 봉인 상태 세기 — 사용: bash seal-count.sh <저장소>
# 함수 정의는 harness/references/contract-schema.md §값 따옴표 규약 · §계약 봉인 블록을 그대로 떼어 쓴다. 출력은 상태별 수(uniq -c).
cd "${1:?저장소}" || exit 2
D=harness/references/contract-schema.md
eval "$(awk '/^fm_get\(\) \{/,/^\}/' "$D")"
eval "$(awk '/^sha256_16\(\) \{/,/^\}/' "$D")"
eval "$(awk '/^contract_digest\(\) \{/,/^\}/' "$D")"
eval "$(awk '/^verify_seal\(\) \{/,/^\}/' "$D")"
type verify_seal fm_get contract_digest sha256_16 >/dev/null 2>&1 || { echo "STOP 함수 정의 없음" >&2; exit 2; }
find .harness -type f -name 'sprint-contract*.md' -print0 | while IFS= read -r -d '' f; do verify_seal "$f"; done | awk '{print $1}' | sort | uniq -c
