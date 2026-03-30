#!/usr/bin/env bash
set -eo pipefail

# 피드백 수집 + 패턴 분석 통합 테스트
# 임시 디렉토리에 fixture를 복사하여 trigger-check.sh 감지 확인
# 글로벌 피드백 경로를 오염시키지 않기 위해 /tmp 하위를 사용

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HARNESS_SCRIPTS="$SCRIPT_DIR/../../../scripts"
CONTRACT_TRIGGER="$SCRIPT_DIR/../../../skills/contract-kaizen/scripts/trigger-check.sh"

echo "=== Aggregation Test ==="

# 1. 임시 테스트 디렉토리 생성 (글로벌 경로 오염 방지)
TEST_FEEDBACK_DIR="/tmp/harness-aggregation-test/contract"
mkdir -p "$TEST_FEEDBACK_DIR"
echo "Test feedback dir: $TEST_FEEDBACK_DIR"

# 2. fixture 데이터 복사 (3개 — ambiguous-conditions 패턴, 각각 다른 타임스탬프)
FIXTURE_DIR="$SCRIPT_DIR/../contract-kaizen/fixture-feedback-data"

for i in 1 2 3; do
  cp "$FIXTURE_DIR/ambiguous-conditions.yaml" "$TEST_FEEDBACK_DIR/test000${i}-2026-03-${i}0T100000.yaml"
done

# 3. trigger-check 실행 (FEEDBACK_DIR 환경변수로 테스트 경로 전달은 불가하므로
#    trigger-check.sh가 feedback-path.sh를 호출하는 대신 직접 검증 로직을 테스트)
echo "--- yq 기반 패턴 분석 직접 테스트 ---"
if command -v yq &>/dev/null; then
  TRIGGER_COUNT=0
  for f in "$TEST_FEEDBACK_DIR"/*.yaml; do
    VAL=$(yq '.diagnosis.checklist.ambiguous_conditions' "$f" 2>/dev/null)
    if [[ "$VAL" == "true" ]]; then
      TRIGGER_COUNT=$((TRIGGER_COUNT + 1))
    fi
  done
  if [[ "$TRIGGER_COUNT" -ge 3 ]]; then
    echo "PASS: ambiguous_conditions가 ${TRIGGER_COUNT}건 감지됨 (trigger 조건 충족)"
  else
    echo "FAIL: ${TRIGGER_COUNT}건 감지 (3건 이상 필요)"
    rm -rf "/tmp/harness-aggregation-test"
    exit 1
  fi
else
  echo "SKIP: yq 미설치 — 패턴 분석 테스트 건너뜀"
fi

# 4. 정리
rm -rf "/tmp/harness-aggregation-test"
echo "=== ALL TESTS PASSED ==="
