#!/usr/bin/env bash
set -eo pipefail

# 피드백 저장 시스템 통합 테스트
# 가짜 YAML을 생성하고 save → verify 파이프라인 검증

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HARNESS_SCRIPTS="$SCRIPT_DIR/../../../scripts"

echo "=== Feedback System Test ==="

# 1. 테스트용 draft 생성
DRAFT="/tmp/test-feedback-draft.yaml"
cat > "$DRAFT" <<'YAML'
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
SAVED_PATH=$(bash "$HARNESS_SCRIPTS/save-feedback.sh" contract "$DRAFT")
echo "Saved to: $SAVED_PATH"

if [[ -z "$SAVED_PATH" ]]; then
  echo "FAIL: save-feedback.sh returned empty path"
  exit 1
fi

# 3. verify 실행
echo "--- verify-feedback.sh ---"
RESULT=$(bash "$HARNESS_SCRIPTS/verify-feedback.sh" "$SAVED_PATH")
echo "Result: $RESULT"

if [[ "$RESULT" != *"PASS"* ]]; then
  echo "FAIL: verify returned '$RESULT' instead of PASS"
  # 테스트 파일 정리
  rm -f "$SAVED_PATH"
  exit 1
fi

# 4. 정리
rm -f "$SAVED_PATH"

# --- 네거티브 테스트 ---
echo ""
echo "--- Negative Tests ---"

# 5. 잘못된 YAML (파싱 불가)
BAD_DRAFT="/tmp/test-bad-yaml.yaml"
echo "invalid: [yaml: {{broken" > "$BAD_DRAFT"
if bash "$HARNESS_SCRIPTS/save-feedback.sh" contract "$BAD_DRAFT" 2>/dev/null; then
  echo "FAIL: should reject invalid YAML"
  rm -f "$BAD_DRAFT"
  exit 1
fi
echo "PASS: invalid YAML rejected"
rm -f "$BAD_DRAFT"

# 6. 필수 필드 누락
INCOMPLETE_DRAFT="/tmp/test-incomplete.yaml"
cat > "$INCOMPLETE_DRAFT" <<'YAML'
schema_version: 1
skill: sprint-contract
YAML
if bash "$HARNESS_SCRIPTS/save-feedback.sh" contract "$INCOMPLETE_DRAFT" 2>/dev/null; then
  echo "FAIL: should reject incomplete YAML"
  rm -f "$INCOMPLETE_DRAFT"
  exit 1
fi
echo "PASS: incomplete YAML rejected"
rm -f "$INCOMPLETE_DRAFT"

# 7. verify on non-existent file
if bash "$HARNESS_SCRIPTS/verify-feedback.sh" "/tmp/nonexistent-file.yaml" 2>/dev/null; then
  echo "FAIL: should fail on non-existent file"
  exit 1
fi
echo "PASS: non-existent file rejected"

echo ""
echo "=== ALL TESTS PASSED ==="
