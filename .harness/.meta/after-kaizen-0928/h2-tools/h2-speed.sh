#!/bin/bash
# h2 훅 속도 — 긴 명령 하나(따옴표 · 치환 · 괄호가 섞인 조각 300 번 + 끝에 진짜 커밋)를 커밋 전 이벤트로 5 번 돌려 가장 느린 값을 밀리초로 찍는다.
# 사용법: h2-speed.sh <훅 폴더>. 출력: "chars=<명령 글자 수> warned=<5 번 모두 경고했으면 1> max_ms=<가장 느린 한 번>"
H=${1:?훅 폴더}
LIBDIR=$H
[ -f "$LIBDIR/_lib-hook-payload.sh" ] || LIBDIR=$HOME/.claude/hooks
export CLAUDE_HOOK_LIB="$LIBDIR/_lib-hook-payload.sh"
F=${H2_FX:-/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/bda55d45-296c-491f-89ba-b52042d58e72/scratchpad/h2-speed}
rm -rf "$F"; mkdir -p "$F"
export GIT_CONFIG_GLOBAL=/dev/null GIT_AUTHOR_NAME=t GIT_AUTHOR_EMAIL=t@t GIT_COMMITTER_NAME=t GIT_COMMITTER_EMAIL=t@t
unset GIT_INDEX_FILE
R=$F/repo
git init -q -b main "$R"
( cd "$R" && echo a > a.txt && git add . && git commit -qm init \
  && git worktree add -q "$F/wt2" -b wt2 && echo s > shared.txt && git add shared.txt )
piece='echo "$(printf "%s" "a b")" '"'"'c d'"'"' `echo e` ( echo f ) { echo g; } ; '
cmd=""
for _ in $(seq 300); do cmd="$cmd$piece"; done
cmd="${cmd}git commit -m x"
jq -nc --arg c "$cmd" --arg d "$R" '{tool_name:"Bash",tool_input:{command:$c},cwd:$d,hook_event_name:"PreToolUse"}' > "$F/in.json"
max=0; ok=1
for _ in 1 2 3 4 5; do
  s=$(python3 -c 'import time; print(int(time.time()*1000))')
  out=$(bash "$H/parallel-session-guard.sh" PreToolUse < "$F/in.json")
  e=$(python3 -c 'import time; print(int(time.time()*1000))')
  [ $((e - s)) -gt "$max" ] && max=$((e - s))
  printf '%s' "$out" | grep -qF shared.txt || ok=0
done
printf 'chars=%s warned=%s max_ms=%s\n' "${#cmd}" "$ok" "$max"
