#!/usr/bin/env bash
# 훅 공용 — stdin 페이로드 파싱 + 출력 JSON 방출.
# harness 플러그인 훅 lint-contract-oracle.sh (PostToolUse) · qa-pending-check.sh (Stop) 가 같은 폴더에서 불러 쓴다.
# 개인 훅 block-dirwide-autofixer.sh · parallel-session-guard.sh 는 ~/.claude/hooks/ 의 사본을 쓴다 — hook_deny · strip_heredoc_bodies 는 그쪽 몫이다.
#
# fail-open 이 이 파일의 하드 규칙이다. jq 부재·빈 stdin·깨진 JSON 어느 경우에도
# 비정상 종료하지 않는다 — 훅이 죽어서 정상 작업을 막는 것이 훅이 없는 것보다 나쁘다.
# 그래서 여기서는 `set -e` 를 절대 쓰지 않는다 (errexit 는 fail-open 을 깨뜨린다).

# 페이로드에서 스칼라 1 개를 꺼낸다. jq 가 없거나 파싱 실패면 빈 문자열.
hook_field() {  # hook_field <payload> <jq-path>
  command -v jq >/dev/null 2>&1 || return 0
  printf '%s' "$1" | jq -r "$2 // \"\"" 2>/dev/null || true
}

# Bash 명령에서 heredoc 본문을 지운다. 본문은 파일에 써 넣을 «데이터»다.
#
# grep 은 줄 단위라 `^` 가 매 줄 시작에 걸려, 본문 속 명령 글자가 명령 위치로 읽힌다.
# 실측: 검증 하네스에 테스트 케이스를 써 넣는 호출이 dirwide 훅에 차단됐고, 커밋 메시지나
# 문서를 쓰는 heredoc 속 "git commit" 에 병렬 세션 훅이 반응했다.
# heredoc «밖»의 줄바꿈은 진짜 명령 구분자라 그대로 둔다 — `cd foo` 다음 줄의 명령은 계속 잡는다.
#
# 이 함수가 없으면 부르는 쪽의 명령 문자열이 비어 검사가 통째로 꺼진다 (fail-open 이라 조용하다).
# 이름을 바꾸거나 지우지 마라.
strip_heredoc_bodies() {  # stdin 명령 → stdout 명령 (heredoc 본문 제외)
  awk '
    !inhd {
      if (match($0, /<<-?[[:space:]]*["'"'"']?[A-Za-z_][A-Za-z0-9_]*["'"'"']?/)) {
        m = substr($0, RSTART, RLENGTH)
        sub(/^<<-?[[:space:]]*/, "", m)
        gsub(/["'"'"']/, "", m)
        marker = m; inhd = 1
      }
      print; next
    }
    {
      t = $0
      sub(/^[[:space:]]+/, "", t); sub(/[[:space:]]+$/, "", t)
      if (t == marker) inhd = 0
      next
    }
  ' 2>/dev/null
}

# PreToolUse 차단. 사유 문자열 1 개를 받아 permissionDecision=deny 를 내고 종료한다.
hook_deny() {  # hook_deny <reason>
  if command -v jq >/dev/null 2>&1; then
    jq -nc --arg r "$1" '{
      hookSpecificOutput: {
        hookEventName: "PreToolUse",
        permissionDecision: "deny",
        permissionDecisionReason: $r
      }
    }' 2>/dev/null
  fi
  exit 0
}

# Stop 되돌리기. 사유 1 개를 받아 «답변을 내보내지 말고 다시 쓰라» 고 되돌린다.
# hook_deny(도구 쓰기 전 막기) · hook_notice(도구 쓴 뒤 알리기) 와 같은 자리에 둔다 —
# 셋의 차이는 어느 시점에 끼어드느냐일 뿐이라 한 파일에 모여 있어야 다음 훅이 찾는다.
#
# 부르는 쪽이 반드시 stop_hook_active 를 먼저 보고, true 면 이 함수를 «부르지 마라».
# 되돌린 답변이 또 걸리면 무한히 돈다.
hook_stop_block() {  # hook_stop_block <reason>
  if command -v jq >/dev/null 2>&1; then
    jq -nc --arg r "$1" '{ decision: "block", reason: $r }' 2>/dev/null
  fi
  exit 0
}

# Stop 이어가기. 안내문 1 개를 모델에 넣어 답을 한 번 더 잇게 한다.
# hook_stop_block 과 효과는 같지만 기록에 오류(hook_blocking_error)가 아니라 안내(hook_additional_context)로
# 남고, 같은 Stop 에 훅이 여럿이어도 안내문이 전부 전달된다 (hooks 문서 Stop decision control, 2.1.268 실측).
# stop_hook_active 가 true 면 부르지 마라 — hook_stop_block 과 같은 이유다.
hook_stop_context() {  # hook_stop_context <context>
  if command -v jq >/dev/null 2>&1; then
    jq -nc --arg c "$1" '{ hookSpecificOutput: { hookEventName: "Stop", additionalContext: $c } }' 2>/dev/null
  fi
  exit 0
}

# PostToolUse 경고. 차단하지 않는다 — additionalContext 로 모델 컨텍스트에만 주입한다.
# permissionDecision 은 PreToolUse 전용이므로 여기서 쓰지 않는다 (v2.1.232 훅 문서).
hook_notice() {  # hook_notice <context> [user-facing message]
  if command -v jq >/dev/null 2>&1; then
    if [ -n "${2:-}" ]; then
      jq -nc --arg c "$1" --arg m "$2" '{
        systemMessage: $m,
        hookSpecificOutput: { hookEventName: "PostToolUse", additionalContext: $c }
      }' 2>/dev/null
    else
      jq -nc --arg c "$1" '{
        hookSpecificOutput: { hookEventName: "PostToolUse", additionalContext: $c }
      }' 2>/dev/null
    fi
  fi
  exit 0
}
