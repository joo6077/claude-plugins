#!/bin/bash
# h2 독립 검토가 찾은 모양 시험. 사용법: h2-review-cases.sh <훅 폴더>
# 줄마다 "<경우> pre=<커밋 전 경고에 shared.txt 가 든 수> post=<커밋 뒤 알림 수> head=<알림이 보인 HEAD 제목>" 을 찍는다.
# 기대 출력은 h2-review-expected.txt. 줄마다 정답은 진짜 bash 에서 그 커밋이 어느 저장소에서 도는지다.
H=${1:?훅 폴더}
LIBDIR=$H
[ -f "$LIBDIR/_lib-hook-payload.sh" ] || LIBDIR=$HOME/.claude/hooks
export CLAUDE_HOOK_LIB="$LIBDIR/_lib-hook-payload.sh"
F=${H2_FX:-/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/bda55d45-296c-491f-89ba-b52042d58e72/scratchpad/h2-review-fx}
rm -rf "$F"; mkdir -p "$F"
export GIT_CONFIG_GLOBAL=/dev/null GIT_AUTHOR_NAME=t GIT_AUTHOR_EMAIL=t@t GIT_COMMITTER_NAME=t GIT_COMMITTER_EMAIL=t@t
unset GIT_INDEX_FILE
R=$F/repo
git init -q -b main "$R"
( cd "$R" && echo a > a.txt && git add . && git commit -qm r-head \
  && git worktree add -q "$F/wt2" -b wt2 && echo s > shared.txt && git add shared.txt )
R2=$F/repo2
git init -q -b main "$R2"
( cd "$R2" && echo b > b.txt && git add . && git commit -qm r2-head )

pg() {  # pg <이벤트> <명령>
  jq -nc --arg c "$2" --arg d "$R" --arg e "$1" \
    '{tool_name:"Bash",tool_input:{command:$c},cwd:$d,hook_event_name:$e}' \
    | bash "$H/parallel-session-guard.sh" "$1" \
    | jq -r '.hookSpecificOutput.additionalContext // empty' 2>/dev/null
}
case_line() {  # case_line <경우> <명령>
  local post
  post=$(pg PostToolUse "$2")
  printf '%s pre=%s post=%s head=%s\n' "$1" "$(pg PreToolUse "$2" | grep -cF shared.txt)" \
    "$(printf '%s\n' "$post" | grep -cF '방금 커밋에 실제로 들어간 것')" \
    "$(printf '%s\n' "$post" | grep -oE 'r2?-head' | head -1)"
}

# 괄호 치환 뒤에 띄어쓰기 없이 붙은 커밋
case_line C1 'h=$(git rev-parse HEAD);git commit -m y'
case_line C2 'h=$(git rev-parse --short HEAD)&&git commit -m y'
case_line C3 'n=$(ls | wc -l);git commit -m y'
case_line C4 'h=`git rev-parse HEAD`;git commit -m y'
case_line C5 'x=$(echo "(");git commit -m y'
case_line C6 'echo ${x:-(}; git commit -m y'
# `$` 가 든 cd · -C 가 커밋 대상과 무관하거나 글자일 뿐인 것 — 세션 저장소로 경고한다
case_line A1 'git -C "$W" add x && git commit -m y'
case_line A2 "cd \"\$TMP\" && ls; cd $R && git commit -m y"
case_line A3 "git commit -m 'fix (cd \$X) case'"
case_line A4 'git commit -m "git -C \$W 처리"'
case_line A5 'git add a && git commit -m "use git -C $PWD"'
# 대상 저장소 — 커밋보다 앞의 마지막 cd 와 커밋 자신의 -C 를 본다
case_line T1 "cd $R2 && git commit -m y"
case_line T2 "git commit -m y; cd $R2"
case_line T3 "cd $R2; cd \"\$X\" && git commit -m y"
case_line T4 "cd \"\$X\"; cd $R2 && git commit -m y"
case_line T5 "git -c a=b -C $R2 commit -m y"
case_line T6 "if true; then cd $R2; fi; git commit -m y"
case_line T7 "cd \"$R2\" && git commit -m y"
