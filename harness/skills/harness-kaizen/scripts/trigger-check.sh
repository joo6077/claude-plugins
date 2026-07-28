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

# 현재 .harness 의 sprint-feedback 파일을 모두 나열한다.
# plain `sprint-feedback.md` 와 슬러그 접미형 `sprint-feedback-<slug>.md` 를 함께 잡는다 —
# 병렬 스프린트에서는 접미형만 존재할 수 있어, plain 고정 경로만 보면 REJECT 이력을 통째로 놓친다.
current_feedback_files() {
  [ -d "$HARNESS_DIR" ] || return 0
  find "$HARNESS_DIR" -maxdepth 1 -type f \
    \( -name 'sprint-feedback.md' -o -name 'sprint-feedback-*.md' \) \
    2>/dev/null | sort
}

# history 아카이브의 feedback 파일. 글로브가 이미 `*sprint-feedback*` 이라 접미형도 함께 잡힌다.
history_feedback_files() {
  [ -d "$HISTORY_DIR" ] || return 0
  find "$HISTORY_DIR" -name "*sprint-feedback*" -type f 2>/dev/null | sort -r
}

# ── Check 1: REJECT 2회 연속 ──
check_consecutive_rejects() {
  local reject_count=0

  # history 최근 2건 + 현재 .harness 의 feedback (plain + 접미형)
  # HISTORY_DIR 부재로 조기 return 하지 않는다 — 병렬 스프린트는 history 없이 접미형만 갖는다.
  local recent_feedbacks
  recent_feedbacks=$( { history_feedback_files | head -2; current_feedback_files; } | grep -v '^$' || true )

  [ -z "$recent_feedbacks" ] && return 0

  while IFS= read -r file; do
    if grep -qi "Verdict:.*REJECT" "$file" 2>/dev/null; then
      reject_count=$((reject_count + 1))
    fi
  done <<< "$recent_feedbacks"

  if [ "$reject_count" -ge 2 ]; then
    trigger_found "QA Evaluator REJECT ${reject_count}회 연속"
  fi
  return 0
}

# ── Check 2: Anti-pattern 3회 이상 반복 ──
check_repeated_antipatterns() {
  # 파일 목록은 **배열**로 모은다. 문자열에 모아 `grep ... $files` 로 넘기면 zsh 에서
  # 워드분할이 일어나지 않아 (SH_WORD_SPLIT 기본 off) 목록 전체가 파일명 하나로 넘어가고,
  # grep 이 매치 0 으로 끝나 Check 2 가 조용히 미발동한다 (bash 에서만 동작하는 코드).
  local file
  local -a all_feedbacks
  all_feedbacks=()

  # history 내 feedback 파일 + 현재 .harness 의 feedback (plain + 접미형) 수집
  # HISTORY_DIR 부재로 조기 return 하지 않는다 — 접미형만 있는 병렬 스프린트를 놓친다.
  while IFS= read -r file; do
    [ -n "$file" ] && all_feedbacks+=("$file")
  done < <( { history_feedback_files; current_feedback_files; } || true )

  [ "${#all_feedbacks[@]}" -eq 0 ] && return 0

  # Anti-pattern ID 추출 후 3회 이상 반복 감지
  local repeated
  repeated=$(grep -h "AP-[0-9]*.*FAIL" "${all_feedbacks[@]}" 2>/dev/null \
    | grep -oE 'AP-[0-9]+' \
    | sort | uniq -c | sort -rn \
    | awk '$1 >= 3 { print $2 " (" $1 "회)" }') || true

  if [ -n "$repeated" ]; then
    trigger_found "Anti-pattern 반복: $repeated"
  fi
  return 0
}

# ── Check 3: 신규 스킬 추가 (7일 이내) ──
check_new_skills() {
  [ -d "$SKILLS_DIR" ] || return 0

  local new_skills
  new_skills=$(git log --diff-filter=A --name-only --since="7 days ago" -- "$SKILLS_DIR/*/SKILL.md" 2>/dev/null | grep "SKILL.md" || true)

  if [ -n "$new_skills" ]; then
    trigger_found "신규 스킬 추가: $new_skills"
  fi
  return 0
}

# ── 실행 ──
check_consecutive_rejects
check_repeated_antipatterns
check_new_skills

# 트리거 없음
exit 1
