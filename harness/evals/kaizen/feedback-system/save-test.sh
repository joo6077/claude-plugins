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
# save-feedback.sh 가 저장 뒤 초안을 지우므로 아래 경우에 쓸 원본을 남긴다
DRAFT_SRC="/tmp/test-feedback-draft-src.yaml"
cp "${DRAFT}" "${DRAFT_SRC}"

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

# 8. project_hash · project_name 이 없는 초안 — 스크립트가 CONTRACT_ROOT 로 다시 계산해 채우므로 저장된다
NOID_DRAFT="/tmp/test-noid-draft.yaml"
NOID_ERR="/tmp/test-noid-draft.err"
grep -vE '^project_(hash|name):' "${DRAFT_SRC}" > "${NOID_DRAFT}"
set +e
NOID_SAVED=$(bash "${HARNESS_SCRIPTS}/save-feedback.sh" contract "${NOID_DRAFT}" 2>"${NOID_ERR}")
NOID_RC=$?
set -e
if [[ "${NOID_RC}" -ne 0 ]]; then
  echo "FAIL: identity 없는 초안이 거부됐다 (rc=${NOID_RC}) — $(cat "${NOID_ERR}")"
  rm -f "${NOID_DRAFT}" "${NOID_ERR}" "${DRAFT_SRC}"
  exit 1
fi
NOID_RESULT=$(bash "${HARNESS_SCRIPTS}/verify-feedback.sh" "${NOID_SAVED}")
if [[ "${NOID_RESULT}" != *"PASS"* ]] || ! grep -q '^project_hash:' "${NOID_SAVED}" || ! grep -q '^project_name:' "${NOID_SAVED}"; then
  echo "FAIL: identity 없는 초안 — verify '${NOID_RESULT}', 저장본에 재계산 project_hash · project_name 이 있어야 한다"
  rm -f "${NOID_SAVED}" "${NOID_ERR}" "${DRAFT_SRC}"
  exit 1
fi
rm -f "${NOID_SAVED}" "${NOID_ERR}"
echo "PASS: identity 없는 초안 저장 (재계산 project_hash · project_name 확인)"

# 9. 워크트리에서 저장해도 project_name 은 본 레포 폴더 이름이다 — reflect-kit project_root 와 같은 규칙.
#    --show-toplevel 로 구하면 워크트리 이름(wt-x)이 적혀 같은 레포 피드백이 워크트리마다 갈린다
WT_BASE="$(mktemp -d)"
WT_BASE="$(cd "${WT_BASE}" && pwd -P)"
WT_MAIN="${WT_BASE}/projmain"
if ! (
  export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1
  export GIT_AUTHOR_NAME=t GIT_AUTHOR_EMAIL=t@example.com GIT_COMMITTER_NAME=t GIT_COMMITTER_EMAIL=t@example.com
  mkdir -p "${WT_MAIN}/.harness" && : > "${WT_MAIN}/.harness/.keep" &&
    git -C "${WT_MAIN}" init -q -b main && git -C "${WT_MAIN}" add -A && git -C "${WT_MAIN}" commit -qm init &&
    git -C "${WT_MAIN}" worktree add -q -b wt "${WT_MAIN}/.claude/worktrees/wt-x"
) >/dev/null 2>&1; then
  echo "FAIL: 워크트리 시험 저장소를 만들지 못했다"
  rm -rf "${WT_BASE}" "${DRAFT_SRC}"
  exit 1
fi
WT_DRAFT="/tmp/test-wt-draft.yaml"
cp "${DRAFT_SRC}" "${WT_DRAFT}"
set +e
WT_SAVED=$(cd "${WT_MAIN}/.claude/worktrees/wt-x" &&
  REFLECT_KIT_LOGS_ROOT="${WT_BASE}/logs" bash "${HARNESS_SCRIPTS}/save-feedback.sh" contract "${WT_DRAFT}" 2>/dev/null)
WT_RC=$?
WT_NAME=$(sed -n 's/^project_name:[[:space:]]*//p' "${WT_SAVED}" 2>/dev/null | head -1 | tr -d "'\"")
set -e
rm -f "${WT_SAVED}" "${WT_DRAFT}"
rm -rf "${WT_BASE}"
if [[ "${WT_RC}" -ne 0 || "${WT_NAME}" != "projmain" ]]; then
  echo "FAIL: 워크트리 저장본 project_name — 기대 projmain, 실제 '${WT_NAME}' (rc=${WT_RC})"
  rm -f "${DRAFT_SRC}"
  exit 1
fi
echo "PASS: 워크트리 저장본 project_name (projmain)"

# 10. 초안 누락 보고에 재계산 필드를 섞지 않는다 — timestamp 만 빠졌으면 timestamp 만 적는다
NOTS_DRAFT="/tmp/test-nots-draft.yaml"
grep -vE '^(project_hash|project_name|timestamp):' "${DRAFT_SRC}" > "${NOTS_DRAFT}"
rm -f "${DRAFT_SRC}"
run_expecting_failure bash "${HARNESS_SCRIPTS}/save-feedback.sh" contract "${NOTS_DRAFT}"
rm -f "${NOTS_DRAFT}"
assert_rejected "draft missing timestamp only" "누락 필드: ['timestamp']"

echo ""
echo "=== ALL TESTS PASSED ==="
