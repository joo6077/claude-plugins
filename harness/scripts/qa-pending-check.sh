#!/usr/bin/env bash
# 이 세션의 QA 가 빠졌으면, 답을 끝내려는 순간 한 번 붙잡아 qa-evaluator 를 띄우라고 안내한다.
#
# 왜 훅인가: ~/.claude/CLAUDE.md 에 "구현 후 반드시 qa-evaluator" 가 있었는데도 묻는 말 한 줄로
# 끝내고 넘어가는 일이 반복됐다. 글로만 있는 규칙은 빠뜨려도 아무것도 막지 않는다.
#
# 붙잡는 경우는 둘이다.
#   1. 이 세션 소유(owner_session == session_id) 진행 중 계약의 QA 결과가 없거나, 계약 봉인보다
#      오래됐거나, 판정이 REJECT · BLOCKED 다. 남의 계약까지 세면 그 레포의 모든 세션이 매번 걸린다.
#   2. 이 세션 소유 계약이 하나도 없는데 프로젝트 안 코드 파일을 2 개 이상 고쳤다. 세션당 한 번.
#      Bash 로 고친 파일은 세지 못한다.
#
# decision:block 이 아니라 additionalContext 로 안내한다 — 기록에 오류로 남지 않고, 같은 Stop 의
# 다른 훅 안내와 함께 전부 전달된다. 구현 도중 사용자에게 묻고 멈출 때도 걸리므로 막는 게 아니라
# 한 번 다시 보게 하는 수준이다.
#
# 실패해도 통과시킨다 — 훅이 죽어서 모든 세션을 막는 것이 훅이 없는 것보다 나쁘다.
# 그래서 errexit 를 쓰지 않는다 (_lib-hook-payload.sh 와 같은 규칙).
set -uo pipefail

# 도우미는 이 파일 옆(플러그인 scripts/)에 있다. 다른 사람 기계에는 ~/.claude/hooks/ 가 없다
LIB="${CLAUDE_HOOK_LIB:-$(dirname "${BASH_SOURCE[0]}")/_lib-hook-payload.sh}"
# shellcheck source=/dev/null
. "$LIB" 2>/dev/null || exit 0

command -v jq >/dev/null 2>&1 || exit 0

payload="$(cat 2>/dev/null || true)"
[ -n "$payload" ] || exit 0
[ "$(hook_field "$payload" '.stop_hook_active')" = "true" ] && exit 0

session="$(hook_field "$payload" '.session_id')"
dir="$(hook_field "$payload" '.cwd')"
transcript="$(hook_field "$payload" '.transcript_path')"
[ -n "$session" ] || exit 0

# 상대 경로면 dirname 이 "." 에서 멈추지 않아 아래 루프가 끝없이 돈다.
case "$dir" in /*) ;; *) exit 0 ;; esac

# sprint-contract 스킬과 같은 규칙 — 조상 중 처음 만나는 .harness/ 가 계약 위치다.
# 규칙이 갈라지면 계약을 쓴 곳과 다른 곳을 보고 "QA 없음" 을 놓친다.
while [ ! -d "$dir/.harness" ]; do
  [ "$dir" = / ] && exit 0
  dir="$(dirname "$dir")"
done
project="$dir"
harness="$dir/.harness"

# 첫 머리말 블록만 읽는다. 본문에 실린 머리말 예시를 값으로 읽으면 남의 계약을 내 것으로 센다.
# 옛 계약은 값에 따옴표가 붙어 있어 벗기지 않으면 세션 번호가 영영 일치하지 않는다.
# 이 기계의 find 는 -exec 인자에 {} 글자가 둘 이상이면 명령을 거부하므로 awk 코드에 그 글자를 쓰지 않는다.
owned="$(find "$harness" -maxdepth 1 -type f -name 'sprint-contract*.md' -exec awk -v session="$session" '
  function value(line,  first, closing) {
    sub(/^[^:]*:[[:space:]]*/, "", line)
    first = substr(line, 1, 1); closing = index(substr(line, 2), first)
    if ((first == "\"" || first == "\047") && closing > 0) return substr(line, 2, closing - 1)
    if (first == "#") return ""
    if (match(line, /[ \t]#/)) line = substr(line, 1, RSTART - 1)
    sub(/[[:space:]]+$/, "", line)
    return line
  }
  FNR == 1 { fm = ($0 ~ /^---[[:space:]]*$/); status = ""; owner = ""; locked = ""; next }
  !fm { nextfile }
  /^---[[:space:]]*$/ { if (owner == session) print FILENAME "\t" status "\t" locked; nextfile }
  /^status:/ { status = value($0) }
  /^owner_session:/ { owner = value($0) }
  /^locked_at:/ { locked = value($0) }
' {} + 2>/dev/null)"

# 시각이 있으면 "YYYY-MM-DD HH:MM", 날짜뿐이면 "YYYY-MM-DD" 까지만 남긴다.
stamp() { printf '%s' "$1" | grep -oE '^[0-9]{4}-[0-9]{2}-[0-9]{2}( [0-9]{2}:[0-9]{2})?' | head -1; }

pending=""
while IFS=$'\t' read -r contract status locked; do
  [ "$status" = active ] || continue
  name="${contract##*/}"
  feedback="${name/#sprint-contract/sprint-feedback}"
  if [ ! -f "$harness/$feedback" ]; then
    pending="${pending}- ${name}: 결과 파일 ${feedback} 없음"$'\n'
    continue
  fi

  IFS=$'\t' read -r verdict evaluated < <(awk '
    /^Verdict:/ && verdict == "" { verdict = $2 }
    /^Evaluated:/ && evaluated == "" { sub(/^Evaluated:[[:space:]]*/, ""); evaluated = $0 }
    END { print verdict "\t" evaluated }
  ' "$harness/$feedback" 2>/dev/null)
  case "${verdict:-}" in
    REJECT|BLOCKED)
      pending="${pending}- ${name}: ${feedback} 의 판정이 ${verdict} 인 채 다시 판정받지 않았음"$'\n'
      continue ;;
    APPROVE) ;;
    # 빈 파일이나 판정 줄이 없는 결과 파일을 완료로 치면 평가가 중간에 죽은 것을 놓친다 (2026-09-29 Codex 점검)
    *)
      pending="${pending}- ${name}: ${feedback} 에 Verdict: 판정 줄이 없음"$'\n'
      continue ;;
  esac

  # 같은 슬러그를 다시 쓰면 지난 스프린트의 결과 파일이 남아 있다. 봉인보다 엄격히 이전일 때만 옛 결과로 본다.
  # 한쪽이 날짜뿐이면 날짜끼리 비교한다 — 같은 날이면 앞뒤를 알 수 없으니 넘어간다.
  judged="$(stamp "${evaluated:-}")"
  sealed="$(stamp "$locked")"
  if [ -n "$judged" ] && [ -n "$sealed" ]; then
    [ ${#judged} -eq ${#sealed} ] || { judged="${judged:0:10}"; sealed="${sealed:0:10}"; }
    [[ "$judged" < "$sealed" ]] && pending="${pending}- ${name}: ${feedback} 이 계약 봉인(${locked})보다 오래됨"$'\n'
  fi
done <<< "$owned"

if [ -n "$pending" ]; then
  hook_stop_context "이 세션이 연 계약의 QA 가 끝나지 않았습니다. 위치: ${harness}
${pending}구현이 끝났다면 사용자에게 묻지 말고 지금 harness:qa-evaluator 에이전트를 띄워 판정받으세요.
아직 구현 중이거나 사용자 답을 기다리는 중이면 그 사실을 한 줄로 밝히고 끝내면 됩니다."
fi

[ -z "$owned" ] || exit 0
[ -r "$transcript" ] || exit 0

marker='[qa-pending:no-contract]'
grep -F "$marker" "$transcript" 2>/dev/null \
  | jq -e -R 'fromjson? | select(.attachment.type? == "hook_additional_context")' >/dev/null 2>&1 \
  && exit 0

# 입력 칸 순서가 호출마다 달라 글자로 찾지 않고 JSON 으로 읽는다. NotebookEdit 은 경로 칸 이름이 다르다.
edited="$(grep -E '"name":"(Edit|Write|MultiEdit|NotebookEdit)"' "$transcript" 2>/dev/null \
  | jq -r -R 'fromjson? | .message.content[]? | select(.type? == "tool_use" and (.name | test("^(Edit|Write|MultiEdit|NotebookEdit)$"))) | .input.file_path // .input.notebook_path // empty' 2>/dev/null \
  | awk -v root="$project/" '
      index($0, root) != 1 { next }
      index($0, root ".harness/") == 1 { next }
      /\.(md|markdown|txt|json|jsonc|yaml|yml|toml|ini|cfg|conf|lock|env|csv|log)$/ { next }
      !seen[$0]++ { print substr($0, length(root) + 1) }
    ')"
count="$(printf '%s' "$edited" | grep -c .)"
[ "$count" -ge 2 ] || exit 0

hook_stop_context "${marker} 이 세션에서 계약 없이 코드 파일 ${count}개를 고쳤습니다. 위치: ${project}
$(printf '%s\n' "$edited" | head -5 | sed 's/^/- /')
기능 구현이면 지금 harness:sprint-contract 로 완료 조건을 정하고 harness:qa-evaluator 로 판정받으세요.
단순 수정(1파일 버그, 설정·문구 수정 등)이면 그 사실을 한 줄로 밝히고 끝내면 됩니다. 이 안내는 세션당 한 번입니다."
