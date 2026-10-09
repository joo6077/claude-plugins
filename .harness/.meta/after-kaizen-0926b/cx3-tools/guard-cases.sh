#!/bin/bash
# cx3 (3) 병렬 세션 훅 시험. 사용법: guard-cases.sh <훅 폴더>
# 줄마다 "<경우> pre=<커밋 전 경고 여부> post=<커밋 뒤 알림 여부>" 를 찍는다. 판정은 계약이 한다.
# 고치기 전 : guard-cases.sh <통합 폴더>/.harness/.meta/after-kaizen-0926b/us-backup
# 지금 판   : guard-cases.sh <통합 폴더>/.harness/.meta/after-kaizen-0926b/us-after
# 고친 뒤   : guard-cases.sh ~/.claude/hooks
H=${1:?훅 폴더}
LIBDIR=${CX3_LIB_DIR:-$H}
[ -f "$LIBDIR/_lib-hook-payload.sh" ] || LIBDIR=$HOME/.claude/hooks
export CLAUDE_HOOK_LIB="$LIBDIR/_lib-hook-payload.sh"
F=${CX3_FX:-/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/bda55d45-296c-491f-89ba-b52042d58e72/scratchpad/cx3-fx}
rm -rf "$F"; mkdir -p "$F"
export GIT_CONFIG_GLOBAL=/dev/null GIT_AUTHOR_NAME=t GIT_AUTHOR_EMAIL=t@t GIT_COMMITTER_NAME=t GIT_COMMITTER_EMAIL=t@t
unset GIT_INDEX_FILE

R=$F/repo
git init -q -b main "$R"
( cd "$R" && echo a > a.txt && git add . && git commit -qm init \
  && git worktree add -q "$F/wt2" -b wt2 && echo s > shared.txt && git add shared.txt )

pg() {  # pg <이벤트> <명령> — 안내문 원문
  jq -nc --arg c "$2" --arg d "$R" --arg e "$1" \
    '{tool_name:"Bash",tool_input:{command:$c},cwd:$d,hook_event_name:$e}' \
    | bash "$H/parallel-session-guard.sh" "$1" \
    | jq -r '.hookSpecificOutput.additionalContext // empty' 2>/dev/null
}
case_line() {  # case_line <경우> <명령>
  local pre post
  pre=$(pg PreToolUse "$2" | grep -cF shared.txt)
  post=$(pg PostToolUse "$2" | grep -cF '방금 커밋에 실제로 들어간 것')
  printf '%s pre=%s post=%s\n' "$1" "$pre" "$post"
}

# 재현 — 큰따옴표 안 $( ) 속 따옴표 뒤의 진짜 커밋
case_line X1 'echo "$(echo "it'"'"'s")"; git commit -m x'
case_line X2 'echo "$(echo "a")" && git commit -m x'
case_line X3 'echo "$(printf '"'"'%s'"'"' "b")"; git commit -m x'
case_line X4 'v="$(echo "$(echo "it'"'"'s")")"; git commit -m x'
# 글자로만 남아야 하는 것 — 안쪽 따옴표 · 바깥 큰따옴표 안의 "git commit"
case_line T1 'echo "$(echo "a; git commit -m y")"'
case_line T2 'echo "$(echo x) ; git commit -m y"'
case_line T3 'echo "$(echo '"'"'a; git commit -m y'"'"')"'
# 산술 확장 $(( )) 는 명령 치환이 아니다 — 뒤의 진짜 커밋을 잡는다
case_line X5 'echo "$((1+2))"; git commit -m x'
# 닫히지 않은 입력 — 조용히 지나가되 비정상 종료하지 않는다
for ev in PreToolUse PostToolUse; do
  jq -nc --arg c 'echo "$(echo "a' --arg d "$R" --arg e "$ev" \
    '{tool_name:"Bash",tool_input:{command:$c},cwd:$d,hook_event_name:$e}' \
    | bash "$H/parallel-session-guard.sh" "$ev" >"$F/e1.out" 2>"$F/e1.err"
  printf 'E1-%s rc=%s out=%s err=%s\n' "$ev" "$?" "$(grep -c . "$F/e1.out")" "$(grep -c . "$F/e1.err")"
done
