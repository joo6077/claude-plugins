#!/usr/bin/env bash
set -eo pipefail

# evaluator-kaizen 이벤트 트리거 감지.
#
# Usage: bash trigger-check.sh
# Exit: 0 = 트리거 발견, 1 = 트리거 없음, 2 = 에러

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FEEDBACK_DIR="$(bash "$SCRIPT_DIR/../../scripts/feedback-path.sh")/evaluator"

trigger_found() {
  echo "TRIGGER: $1"
  exit 0
}

if [[ ! -d "$FEEDBACK_DIR" ]]; then
  echo "NO_FEEDBACK_DIR"
  exit 1
fi

RECENT_FILES=$(ls -t "$FEEDBACK_DIR/" 2>/dev/null | grep '\.yaml$' | head -10)
if [[ -z "$RECENT_FILES" ]]; then
  echo "NO_FEEDBACK_FILES"
  exit 1
fi

FILE_COUNT=$(echo "$RECENT_FILES" | wc -l)
if [[ "$FILE_COUNT" -lt 3 ]]; then
  echo "INSUFFICIENT_DATA: ${FILE_COUNT} files (need 3+)"
  exit 1
fi

# 참고: 오케스트레이터 Phase 실행 여부 결정용이 아닌, 피드백 임계치 이벤트 트리거 전용.

if command -v yq &>/dev/null; then
  for field in l3_unreached bias_detected evidence_missing contract_misinterpret perspective_gap; do
    COUNT=0
    while IFS= read -r fname; do
      VAL=$(yq ".diagnosis.checklist.${field}" "$FEEDBACK_DIR/$fname" 2>/dev/null)
      if [[ "$VAL" == "true" ]]; then
        COUNT=$((COUNT + 1))
      fi
    done <<< "$RECENT_FILES"
    if [[ "$COUNT" -ge 3 ]]; then
      trigger_found "진단 항목 '${field}'가 최근 ${FILE_COUNT}건 중 ${COUNT}건 반복"
    fi
  done
fi

echo "NO_TRIGGER"
exit 1
