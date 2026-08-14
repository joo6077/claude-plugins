#!/usr/bin/env bash
set -eo pipefail

# 피드백 수집 + 패턴 분석 통합 테스트
# 임시 디렉토리에 fixture를 복사하여 패턴 감지 로직을 검증한다.
# 글로벌 피드백 경로를 오염시키지 않기 위해 /tmp 하위를 사용
#
# 종료 코드 의미는 harness/evals/gate-exit-codes.md 를 따른다 (SSOT — 여기서 재정의하지 않는다).

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEST_ROOT="/tmp/harness-aggregation-test"

cleanup() { rm -rf "${TEST_ROOT}"; }

echo "=== Aggregation Test ==="

# 1. 임시 테스트 디렉토리 생성 (글로벌 경로 오염 방지)
TEST_FEEDBACK_DIR="${TEST_ROOT}/contract"
mkdir -p "${TEST_FEEDBACK_DIR}"
echo "Test feedback dir: ${TEST_FEEDBACK_DIR}"

# 2. fixture 데이터 복사 (3개 — ambiguous-conditions 패턴, 각각 다른 타임스탬프)
#    AGGREGATION_FIXTURE_DIR 는 음성 대조(가드가 실제로 작동하는지 확인)용 주입 지점이다.
FIXTURE_DIR="${AGGREGATION_FIXTURE_DIR:-${SCRIPT_DIR}/../contract-kaizen/fixture-feedback-data}"

for i in 1 2 3; do
  cp "${FIXTURE_DIR}/ambiguous-conditions.yaml" \
     "${TEST_FEEDBACK_DIR}/test000${i}-2026-03-${i}0T100000.yaml"
done

# 3. 패턴 분석 직접 테스트
#    trigger-check.sh 는 feedback-path.sh 로 경로를 잡으므로 테스트 경로를 주입할 수 없다.
#    따라서 같은 판정 로직(diagnosis.checklist.ambiguous_conditions == true 카운트)을 직접 돌린다.
#
#    ⚠ 도구 부재를 통과로 집계하지 않는다. yq 가 없으면 python3+PyYAML 로 같은 값을 읽고,
#    둘 다 못 쓰면 "검사를 수행하지 못했다"(exit 2) 로 끝낸다 — 절대 PASSED 를 출력하지 않는다.
echo "--- 패턴 분석 직접 테스트 ---"

read_flag() { # read_flag <yaml파일> → "true" | "false" | ""
  if [[ "${READER}" == "yq" ]]; then
    yq '.diagnosis.checklist.ambiguous_conditions' "$1"
  else
    python3 - "$1" <<'PY'
import sys, yaml
with open(sys.argv[1], encoding="utf-8") as fh:
    data = yaml.safe_load(fh) or {}
val = (data.get("diagnosis") or {}).get("checklist", {}).get("ambiguous_conditions")
print("true" if val is True else "false" if val is False else "")
PY
  fi
}

if command -v yq >/dev/null 2>&1; then
  READER="yq"
elif command -v python3 >/dev/null 2>&1 && python3 -c 'import yaml' >/dev/null 2>&1; then
  READER="python3"
else
  echo "NOT RUN: yq 도 python3+PyYAML 도 쓸 수 없어 YAML 을 읽지 못했다 — 검사를 수행하지 못했다." >&2
  echo "         도구 부재는 통과가 아니다 (harness/evals/gate-exit-codes.md · exit 2)." >&2
  cleanup
  exit 2
fi
echo "reader: ${READER}"

TRIGGER_COUNT=0
for f in "${TEST_FEEDBACK_DIR}"/*.yaml; do
  # set -e 는 조건문 안에서 무력화되므로 (BashFAQ/105 · SC2310) 호출을 분리해 rc 를 직접 본다
  set +e
  VAL="$(read_flag "${f}" 2>&1)"
  rc=$?
  set -e
  if [[ "${rc}" -ne 0 ]]; then
    echo "NOT RUN: ${f} 파싱 실패 (rc=${rc}) — ${VAL}" >&2
    cleanup
    exit 2
  fi
  if [[ "${VAL}" == "true" ]]; then
    TRIGGER_COUNT=$((TRIGGER_COUNT + 1))
  fi
done

if [[ "${TRIGGER_COUNT}" -ge 3 ]]; then
  echo "PASS: ambiguous_conditions가 ${TRIGGER_COUNT}건 감지됨 (trigger 조건 충족)"
else
  echo "FAIL: ${TRIGGER_COUNT}건 감지 (3건 이상 필요)"
  cleanup
  exit 1
fi

# 4. 정리
cleanup
echo "=== ALL TESTS PASSED (reader=${READER}) ==="
