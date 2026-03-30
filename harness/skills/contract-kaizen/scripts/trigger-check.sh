#!/usr/bin/env bash
set -eo pipefail

# contract-kaizen 이벤트 트리거 감지.
# 글로벌 피드백에서 반복 패턴을 확인한다.
#
# Usage: bash trigger-check.sh
# Exit: 0 = 트리거 발견, 1 = 트리거 없음, 2 = 에러

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FEEDBACK_DIR="$(bash "$SCRIPT_DIR/../../scripts/feedback-path.sh")/contract"

trigger_found() {
  echo "TRIGGER: $1"
  exit 0
}

# 피드백 디렉토리 존재 확인
if [[ ! -d "$FEEDBACK_DIR" ]]; then
  echo "NO_FEEDBACK_DIR"
  exit 1
fi

# 최근 10개 파일 (경로에 공백 있어도 안전하게 처리)
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

# 참고: 이 스크립트는 피드백 임계치 이벤트 트리거 전용이다.
# 오케스트레이터가 Phase 실행 여부를 결정할 때 사용하지 않는다.
# 오케스트레이터는 항상 모든 Phase를 실행하며, 각 Phase 내부의 triage가 SKIP 여부를 판단한다.

# 진단 체크리스트에서 반복 패턴 확인
# 동일 항목이 3회 이상 true이면 트리거
if command -v yq &>/dev/null; then
  for field in ambiguous_conditions missing_error_paths untestable_conditions category_coverage_gap complexity_underestimate; do
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
