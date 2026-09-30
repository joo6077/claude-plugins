#!/bin/bash
# h2 (B10) 병렬 세션 훅이 못 잡던 커밋 모양 시험. 사용법: h2-cases.sh <훅 폴더>
# 줄마다 "<경우> pre=<커밋 전 경고에 shared.txt 가 든 수> post=<커밋 뒤 알림 수>" 를 찍는다. 판정은 계약이 한다.
# D 줄은 커밋 뒤 알림이 어느 저장소의 HEAD 를 보였는지(r=세션 저장소, r2=명령이 가리킨 저장소)도 찍는다.
# 훅이 읽는 공용 도우미는 시험 대상 폴더의 것을 쓴다. 그 폴더에 없으면 설치본을 쓴다.
H=${1:?훅 폴더}
LIBDIR=$H
[ -f "$LIBDIR/_lib-hook-payload.sh" ] || LIBDIR=$HOME/.claude/hooks
export CLAUDE_HOOK_LIB="$LIBDIR/_lib-hook-payload.sh"
F=${H2_FX:-/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/bda55d45-296c-491f-89ba-b52042d58e72/scratchpad/h2-fx}
rm -rf "$F"; mkdir -p "$F"
export GIT_CONFIG_GLOBAL=/dev/null GIT_AUTHOR_NAME=t GIT_AUTHOR_EMAIL=t@t GIT_COMMITTER_NAME=t GIT_COMMITTER_EMAIL=t@t
unset GIT_INDEX_FILE

# R: 워크트리 2 개, 공용 인덱스에 shared.txt. R2: 따로 선 저장소, HEAD 제목이 r2-head
R=$F/repo
git init -q -b main "$R"
( cd "$R" && echo a > a.txt && git add . && git commit -qm r-head \
  && git worktree add -q "$F/wt2" -b wt2 && echo s > shared.txt && git add shared.txt )
R2=$F/repo2
git init -q -b main "$R2"
( cd "$R2" && echo b > b.txt && git add . && git commit -qm r2-head )

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
dir_line() {  # dir_line <경우> <명령>
  local pre c
  pre=$(pg PreToolUse "$2" | grep -c .)
  c=$(pg PostToolUse "$2")
  printf '%s pre=%s post=%s r=%s r2=%s\n' "$1" "$pre" \
    "$(printf '%s\n' "$c" | grep -cF '방금 커밋에 실제로 들어간 것')" \
    "$(printf '%s\n' "$c" | grep -c 'r-head')" "$(printf '%s\n' "$c" | grep -c 'r2-head')"
}

# 잡아야 하는 것 — 진짜로 커밋이 도는 모양
case_line K01 'echo "`echo "it'"'"'s"`"; git commit -m x'
case_line K02 'out=$(git commit -m x)'
case_line K03 'echo "$(git commit -m x)"'
case_line K04 'out=`git commit -m x`'
case_line K05 'echo "`git commit -m x`"'
case_line K06 'git -c user.name=t commit -m x'
case_line K07 'git -c a.b=c -c d.e=f commit -m x'
case_line K08 '( git commit -m x )'
case_line K09 '(git commit -m x)'
case_line K10 '{ git commit -m x; }'
case_line K11 'if true; then git commit -m x; fi'
case_line K12 'time git commit -m x'
case_line K13 'command git commit -m x'
case_line K14 "bash -c 'git commit -m x'"
case_line K15 'sh -c "git commit -m x"'
case_line K16 'for i in 1; do git commit -m x; done'
case_line K17 'if false; then :; else git commit -m x; fi'
# 경로를 한정한 커밋은 모양이 바뀌어도 커밋 전 경고가 없다 (커밋 뒤 알림은 있다)
case_line K18 '(git commit -o a.txt -m x)'
case_line K19 "bash -c 'git commit -o a.txt -m x'"

# 글자일 뿐인 것 — 조용해야 한다
case_line N01 "echo '\`git commit -m x\`'"
case_line N02 'echo "\`git commit -m x\`"'
case_line N03 "echo '\$(git commit -m x)'"
case_line N04 'echo "\$(git commit -m x)"'
case_line N05 'echo "( git commit -m x )"'
case_line N06 "echo '{ git commit -m x; }'"
case_line N07 'echo "then git commit -m x"'
case_line N08 'echo time git commit -m x'
case_line N09 "printf '%s' command git commit -m x"
case_line N10 "echo bash -c 'git commit -m x'"
case_line N11 'grep -e "git -c x commit" a.txt'
case_line N12 "echo 'bash -c \"git commit -m x\"'"
case_line N13 "bash -c 'echo \"git commit -m x\"'"

# 대상 저장소 — 풀 수 없는 경로는 조용히, 서브셸 안 cd 는 그쪽 저장소로
dir_line D01 'git -C "$W" commit -m x'
dir_line D02 'cd "$X" && git commit -m x'
dir_line D03 "git -C $R2 commit -m x"
dir_line D04 "(cd $R2 && git commit -m x)"
dir_line D05 'git commit -m x'

# 닫히지 않은 입력 — 조용히 지나가되 비정상 종료하지 않는다
en=0
for c in "bash -c 'git commit -m x" 'echo "`git commit -m x' '( git commit -m x'; do
  en=$((en + 1))
  for ev in PreToolUse PostToolUse; do
    jq -nc --arg c "$c" --arg d "$R" --arg e "$ev" \
      '{tool_name:"Bash",tool_input:{command:$c},cwd:$d,hook_event_name:$e}' \
      | bash "$H/parallel-session-guard.sh" "$ev" >"$F/e.out" 2>"$F/e.err"
    printf 'E%02d-%s rc=%s out=%s err=%s\n' "$en" "$ev" "$?" "$(grep -c . "$F/e.out")" "$(grep -c . "$F/e.err")"
  done
done
