#!/usr/bin/env bash
# ── Flutter Kaizen Event Trigger Check ──
# Usage: bash trigger-check.sh <evals-dir> <skills-dir>
# Exit codes:
#   0 = 트리거 발생 (stdout에 사유 출력)
#   1 = 트리거 없음
#   2 = 에러

set -eo pipefail
trap 'echo "ERROR: unexpected failure" >&2; exit 2' ERR

EVALS_DIR="${1:-flutter-toolkit/evals}"
SKILLS_DIR="${2:-flutter-toolkit/skills}"

# ── 유틸리티 ──
trigger_found() {
  echo "TRIGGER: $1"
  exit 0
}

# ── Check 1: Eval 실패 2회 연속 ──
check_consecutive_eval_failures() {
  local results_dir="$EVALS_DIR/results"
  [ -d "$results_dir" ] || return 0

  local fail_count=0

  # 최근 eval 결과 파일 확인
  local recent_results
  recent_results=$(find "$results_dir" -name "*.json" -type f 2>/dev/null | sort -r | head -2)

  [ -z "$recent_results" ] && return 0

  while IFS= read -r file; do
    if grep -qi '"status".*"fail"' "$file" 2>/dev/null; then
      fail_count=$((fail_count + 1))
    fi
  done <<< "$recent_results"

  [ "$fail_count" -ge 2 ] && trigger_found "Eval 실패 ${fail_count}회 연속"
}

# ── Check 2: 신규 스킬 추가 (7일 이내) ──
check_new_skills() {
  [ -d "$SKILLS_DIR" ] || return 0

  local new_skills
  new_skills=$(git log --diff-filter=A --name-only --since="7 days ago" -- "$SKILLS_DIR/*/SKILL.md" 2>/dev/null | grep "SKILL.md" || true)

  [ -n "$new_skills" ] && trigger_found "신규 스킬 추가: $new_skills"
}

# ── 실행 ──
check_consecutive_eval_failures
check_new_skills

# 트리거 없음
exit 1
