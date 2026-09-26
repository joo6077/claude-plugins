#!/usr/bin/env bash
# 커밋 안전 훅 판정 아홉 경우를 임시 저장소에서 돌려 기대와 맞대 MATCH/MISMATCH 를 낸다.
# 사용: guard_probe.sh <훅 경로>   마지막 줄: mismatch=<N>/9 mismatch_sc=<G1~G7 중>/7 mismatch_er=<G8~G9 중>/2
hook=${1:?}
[ -f "$hook" ] || { echo "STOP 훅 없음 $hook"; exit 2; }
command -v jq >/dev/null || { echo "STOP jq 없음"; exit 2; }
unset HARNESS_COMMIT_GUARD GIT_INDEX_FILE GIT_DIR GIT_WORK_TREE
export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1
export GIT_AUTHOR_NAME=t GIT_AUTHOR_EMAIL=t@example.com GIT_COMMITTER_NAME=t GIT_COMMITTER_EMAIL=t@example.com
w=$(mktemp -d "${TMPDIR:-/tmp}/guard-probe.XXXXXX"); trap 'rm -rf "$w"' EXIT
mis=0; mis_sc=0; mis_er=0
mk() { local r=$1 k; mkdir -p "$r/d1"; git -C "$r" init -q -b main
  for ((k = 1; k <= 60; k++)); do printf 'line %d\n' "$k" >"$r/d1/$(printf 'f%03d' "$k")"; done
  echo a >"$r/a.txt"; git -C "$r" add -A && git -C "$r" commit -qm init; }
run() { jq -nc --arg c "$2" --arg d "$1" '{hook_event_name:"PreToolUse",tool_name:"Bash",tool_input:{command:$c},cwd:$d}' \
  | bash "$hook" pre >"$w/out" 2>"$w/err"; rc=$?; }
chk() {  # chk <이름> <기대 rc> <있어야 할 글자|-> <없어야 할 글자|->
  local ok=1
  [ "$rc" = "$2" ] || ok=0
  [ "$2" = 0 ] && [ -s "$w/out" ] && ok=0
  [ "$3" != - ] && ! grep -qF -- "$3" "$w/err" && ok=0
  [ "${5:-}" != "" ] && [ "$5" != - ] && ! grep -qF -- "$5" "$w/err" && ok=0
  [ "$4" != - ] && grep -qF -- "$4" "$w/err" && ok=0
  if [ "$ok" = 1 ]; then v=MATCH; else v=MISMATCH; mis=$((mis + 1)); case $1 in G8-*|G9-*) mis_er=$((mis_er + 1)) ;; *) mis_sc=$((mis_sc + 1)) ;; esac; fi
  printf '%s %s rc=%s err=[%s]\n' "$v" "$1" "$rc" "$(head -1 "$w/err")"
}
r=$w/g1; mk "$r"; mv "$r/d1" "$r/d2"; git -C "$r" add d2
run "$r" 'git commit -a -m x'; chk G1-이동·새경로올림·commit-a 0 - -
r=$w/g2; mk "$r"; mv "$r/d1" "$r/d2"
run "$r" 'git add -A && git commit -m x'; chk G2-이동·add-A 0 - -
r=$w/g3; mk "$r"; mv "$r/d1" "$r/d2"; git -C "$r" add d2
run "$r" 'git add -u && git commit -m x'; chk G3-이동·새경로올림·add-u 0 - -
r=$w/g4; mk "$r"; mv "$r/d1" "$r/d2"
run "$r" 'git add . && git commit -m x'; chk G4-이동·add-점 0 - -
r=$w/g5; mk "$r"; mv "$r/d1" "$r/d2"
run "$r" 'git commit -am x'; chk G5-이동·새경로안올림·commit-am 2 '삭제 60 개' -
r=$w/g6; mk "$r"; for ((k = 1; k <= 60; k++)); do rm -f "$r/d1/$(printf 'f%03d' "$k")"; done
run "$r" 'git commit -a -m x'; chk G6-진짜삭제60·commit-a 2 '삭제 60 개' - '작업 폴더 삭제 포함'
r=$w/g7; mk "$r"; mkdir -p "$r/d3"; for ((k = 1; k <= 60; k++)); do printf 'o %d\n' "$k" >"$r/d3/$(printf 'g%03d' "$k")"; done
git -C "$r" add d3 && git -C "$r" commit -qm d3; mv "$r/d1" "$r/d2"; rm -rf "$r/d3"
run "$r" 'git add -A && git commit -m x'; chk G7-이동60+진짜삭제60·add-A 2 '삭제 60 개' -
r=$w/g8; mk "$r"; git -C "$r" rm -q -- $(for ((k = 1; k <= 10; k++)); do printf 'd1/f%03d ' "$k"; done)
for ((k = 11; k <= 55; k++)); do rm -f "$r/d1/$(printf 'f%03d' "$k")"; done
run "$r" 'git commit -i d1 -m x'; chk G8-i·목록10+작업폴더45 2 '삭제 55 개' - '작업 폴더 삭제 포함'
r=$w/g9; mk "$r"; git -C "$r" rm -q -- $(for ((k = 1; k <= 51; k++)); do printf 'd1/f%03d ' "$k"; done)
run "$r" 'git commit -i d1 -m x'; chk G9-i·목록51만 2 '삭제 51 개' '작업 폴더 삭제 포함'
echo "mismatch=$mis/9 mismatch_sc=$mis_sc/7 mismatch_er=$mis_er/2"
