#!/usr/bin/env bash
set -eo pipefail

# 피드백 저장 시스템 통합 테스트
# 가짜 YAML을 생성하고 save → verify 파이프라인 검증
#
# 종료 코드 의미는 harness/evals/gate-exit-codes.md 를 따른다 (SSOT — 여기서 재정의하지 않는다).
#
# ⚠ 네거티브 테스트는 stderr 를 버리지 않는다. "실패했다" 만 보면 **왜** 실패했는지 모르므로
#   엉뚱한 이유(경로 오타·권한 오류)로 실패해도 통과로 집계된다. 캡처 후 에러 문자열을 assert 한다.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HARNESS_SCRIPTS="${SCRIPT_DIR}/../../../scripts"

echo "=== Feedback System Test ==="

# 실패해야 하는 명령을 돌리고 (rc, 합쳐진 출력) 을 돌려준다.
# set -e 는 조건문 안에서 무력화되므로 (BashFAQ/105 · SC2310) 호출을 분리해 rc 를 직접 본다.
NEG_OUT=""
NEG_RC=0
run_expecting_failure() { # run_expecting_failure <명령...>
  set +e
  NEG_OUT="$("$@" 2>&1)"
  NEG_RC=$?
  set -e
}

# 네거티브 3 요건: (1) 비-0 종료 (2) 기대 에러 문자열 존재 (3) 그 문자열이 stderr 경로로 나왔다
assert_rejected() { # assert_rejected <라벨> <기대문자열>
  if [[ "${NEG_RC}" -eq 0 ]]; then
    echo "FAIL: $1 — 거부돼야 하는데 exit 0 이었다"
    echo "      출력: ${NEG_OUT}"
    exit 1
  fi
  if [[ "${NEG_OUT}" != *"$2"* ]]; then
    echo "FAIL: $1 — 거부는 됐지만 기대 사유가 아니다 (rc=${NEG_RC})"
    echo "      기대 문자열: $2"
    echo "      실제 출력: ${NEG_OUT}"
    exit 1
  fi
  echo "PASS: $1 (rc=${NEG_RC} · 사유 '$2' 확인)"
}

# 1. 테스트용 draft 생성
DRAFT="/tmp/test-feedback-draft.yaml"
cat > "${DRAFT}" <<'YAML'
schema_version: 1
timestamp: "2026-03-30T10:00:00+09:00"
project_hash: "testtest"
project_name: "test-project"
skill: sprint-contract
skill_version: "0.3.3"
outcome: completed
contract:
  condition_count: 5
  category_count: 3
  category_coverage: 0.75
  anti_pattern_count: 2
  complexity: simple
diagnosis:
  checklist:
    ambiguous_conditions: false
    missing_error_paths: false
    untestable_conditions: false
    category_coverage_gap: false
    complexity_underestimate: false
  cross_diagnosis_by: qa-evaluator
  cross_diagnosis_notes: "테스트 — 문제 없음"
  improvement_suggestions: []
user_rating: null
user_comment: null
YAML

# 2. save 실행
echo "--- save-feedback.sh ---"
SAVED_PATH=$(bash "${HARNESS_SCRIPTS}/save-feedback.sh" contract "${DRAFT}")
echo "Saved to: ${SAVED_PATH}"

if [[ -z "${SAVED_PATH}" ]]; then
  echo "FAIL: save-feedback.sh returned empty path"
  exit 1
fi

# 3. verify 실행
echo "--- verify-feedback.sh ---"
RESULT=$(bash "${HARNESS_SCRIPTS}/verify-feedback.sh" "${SAVED_PATH}")
echo "Result: ${RESULT}"

if [[ "${RESULT}" != *"PASS"* ]]; then
  echo "FAIL: verify returned '${RESULT}' instead of PASS"
  rm -f "${SAVED_PATH}"
  exit 1
fi

# 4. 정리
rm -f "${SAVED_PATH}"

# --- 네거티브 테스트 ---
echo ""
echo "--- Negative Tests ---"

# 5. 잘못된 YAML (파싱 불가) — 스키마 검증에서 막혀야 한다
BAD_DRAFT="/tmp/test-bad-yaml.yaml"
echo "invalid: [yaml: {{broken" > "${BAD_DRAFT}"
run_expecting_failure bash "${HARNESS_SCRIPTS}/save-feedback.sh" contract "${BAD_DRAFT}"
rm -f "${BAD_DRAFT}"
assert_rejected "invalid YAML rejected" "스키마 검증 실패"

# 6. 필수 필드 누락 — 어느 필드가 없는지까지 보고돼야 한다
INCOMPLETE_DRAFT="/tmp/test-incomplete.yaml"
cat > "${INCOMPLETE_DRAFT}" <<'YAML'
schema_version: 1
skill: sprint-contract
YAML
run_expecting_failure bash "${HARNESS_SCRIPTS}/save-feedback.sh" contract "${INCOMPLETE_DRAFT}"
rm -f "${INCOMPLETE_DRAFT}"
assert_rejected "incomplete YAML rejected" "누락 필드"

# 7. verify on non-existent file — 파일 부재 사유로 실패해야 한다
run_expecting_failure bash "${HARNESS_SCRIPTS}/verify-feedback.sh" "/tmp/nonexistent-file.yaml"
assert_rejected "non-existent file rejected" "파일이 존재하지 않음"

echo ""
echo "=== ALL TESTS PASSED ==="
