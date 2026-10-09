#!/usr/bin/env bash
# 파일 2000 개 폴더를 옮긴 저장소에서 훅 한 번의 판정 시간을 잰다.
# 사용: perf.sh <훅> <명령> <add|noadd>   add = 새 경로를 미리 git add, noadd = 올리지 않음
hook=${1:?}; cmd=${2:?}; mode=${3:?}
[ -f "$hook" ] || { echo "STOP 훅 없음 $hook"; exit 2; }
command -v jq >/dev/null || { echo "STOP jq 없음"; exit 2; }
unset HARNESS_COMMIT_GUARD GIT_INDEX_FILE GIT_DIR GIT_WORK_TREE
export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1
export GIT_AUTHOR_NAME=t GIT_AUTHOR_EMAIL=t@example.com GIT_COMMITTER_NAME=t GIT_COMMITTER_EMAIL=t@example.com
w=$(mktemp -d "${TMPDIR:-/tmp}/cg-perf.XXXXXX"); trap 'rm -rf "$w"' EXIT
r=$w/r; mkdir -p "$r/d1"; git -C "$r" init -q -b main
for ((k = 1; k <= 2000; k++)); do printf 'line %d\n' "$k" >"$r/d1/f$k"; done
git -C "$r" add -A && git -C "$r" commit -qm init
mv "$r/d1" "$r/d2"; [ "$mode" = add ] && git -C "$r" add d2
p=$(jq -nc --arg c "$cmd" --arg d "$r" '{hook_event_name:"PreToolUse",tool_name:"Bash",tool_input:{command:$c},cwd:$d}')
s=$(python3 -c 'import time;print(time.time())')
printf '%s' "$p" | bash "$hook" pre >/dev/null 2>"$w/err"; rc=$?
e=$(python3 -c 'import time;print(time.time())')
python3 -c "print(f'rc=$rc sec={$e-$s:.2f}')"
