#!/usr/bin/env bash
# ── Kaizen Event Trigger Check ──
# Usage: bash trigger-check.sh <harness-dir> <skills-dir>
# Exit codes:
#   0 = 트리거 발생 (stdout에 사유 출력)
#   1 = 트리거 없음
#   2 = 에러

set -eo pipefail

HARNESS_DIR="${1:-.harness}"
SKILLS_DIR="${2:-harness/skills}"
HISTORY_DIR="$HARNESS_DIR/history"

# ── 유틸리티 ──
trigger_found() {
  echo "TRIGGER: $1"
  exit 0
}

# ── Check 1: REJECT 2회 연속 ──
check_consecutive_rejects() {
  [ -d "$HISTORY_DIR" ] || return 0

  local reject_count=0

  # history 디렉토리에서 최근 feedback 파일 확인
  local recent_feedbacks
  recent_feedbacks=$(find "$HISTORY_DIR" -name "*sprint-feedback*" -type f 2>/dev/null | sort -r | head -2)

  [ -z "$recent_feedbacks" ] && return 0

  while IFS= read -r file; do
    if grep -qi "Verdict:.*REJECT" "$file" 2>/dev/null; then
      reject_count=$((reject_count + 1))
    fi
  done <<< "$recent_feedbacks"

  # 현재 sprint-feedback.md도 확인
  if [ -f "$HARNESS_DIR/sprint-feedback.md" ]; then
    if grep -qi "Verdict:.*REJECT" "$HARNESS_DIR/sprint-feedback.md" 2>/dev/null; then
      reject_count=$((reject_count + 1))
    fi
  fi

  [ "$reject_count" -ge 2 ] && trigger_found "QA Evaluator REJECT ${reject_count}회 연속"
}

# ── Check 2: Anti-pattern 3회 이상 반복 ──
check_repeated_antipatterns() {
  [ -d "$HISTORY_DIR" ] || return 0

  local all_feedbacks=""

  # history 내 feedback 파일 수집
  while IFS= read -r file; do
    [ -n "$file" ] && all_feedbacks="$all_feedbacks $file"
  done < <(find "$HISTORY_DIR" -name "*sprint-feedback*" -type f 2>/dev/null)

  # 현재 feedback도 포함
  [ -f "$HARNESS_DIR/sprint-feedback.md" ] && all_feedbacks="$all_feedbacks $HARNESS_DIR/sprint-feedback.md"

  [ -z "$all_feedbacks" ] && return 0

  # Anti-pattern ID 추출 후 3회 이상 반복 감지
  # shellcheck disable=SC2086
  local repeated
  repeated=$(grep -h "AP-[0-9]*.*FAIL" $all_feedbacks 2>/dev/null \
    | grep -oE 'AP-[0-9]+' \
    | sort | uniq -c | sort -rn \
    | awk '$1 >= 3 { print $2 " (" $1 "회)" }') || true

  [ -n "$repeated" ] && trigger_found "Anti-pattern 반복: $repeated"
}

# ── Check 3: 신규 스킬 추가 (7일 이내) ──
check_new_skills() {
  [ -d "$SKILLS_DIR" ] || return 0

  local new_skills
  new_skills=$(git log --diff-filter=A --name-only --since="7 days ago" -- "$SKILLS_DIR/*/SKILL.md" 2>/dev/null | grep "SKILL.md" || true)

  [ -n "$new_skills" ] && trigger_found "신규 스킬 추가: $new_skills"
}

# ── 실행 ──
check_consecutive_rejects
check_repeated_antipatterns
check_new_skills

# 트리거 없음
exit 1
