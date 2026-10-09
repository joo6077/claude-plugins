#!/bin/bash
# cx3 (3) 기존 동작 유지 — 큰따옴표 안 $( 가 없는 무작위 명령에서 두 판의 안내문이 같은지 맞댄다.
# 사용법: guard-random.sh <기준 훅 폴더> <새 훅 폴더> <시드> [개수=40]
# 출력: "seed=<시드> cases=<개수> has_dq_subst=<0 이어야 함> warned=<새 판이 커밋 전 경고를 낸 경우 수> diff=<다른 경우 수>" 와 다른 경우의 명령
A=${1:?기준 훅 폴더}; B=${2:?새 훅 폴더}; SEED=${3:?시드}; N=${4:-40}
export CLAUDE_HOOK_LIB=$HOME/.claude/hooks/_lib-hook-payload.sh
F=${CX3_FX:-/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/bda55d45-296c-491f-89ba-b52042d58e72/scratchpad/cx3-rand}-$SEED
rm -rf "$F"; mkdir -p "$F"
export GIT_CONFIG_GLOBAL=/dev/null GIT_AUTHOR_NAME=t GIT_AUTHOR_EMAIL=t@t GIT_COMMITTER_NAME=t GIT_COMMITTER_EMAIL=t@t
unset GIT_INDEX_FILE
R=$F/repo
git init -q -b main "$R"
( cd "$R" && echo a > a.txt && git add . && git commit -qm init \
  && git worktree add -q "$F/wt2" -b wt2 && echo s > shared.txt && git add shared.txt )

run() {  # run <훅 폴더> <이벤트> <명령>
  jq -nc --arg c "$3" --arg d "$R" --arg e "$2" \
    '{tool_name:"Bash",tool_input:{command:$c},cwd:$d,hook_event_name:$e}' \
    | bash "$1/parallel-session-guard.sh" "$2" 2>&1
}

python3 - "$SEED" "$N" > "$F/cases.bin" <<'PY'
import random, sys
seed, n = int(sys.argv[1]), int(sys.argv[2])
rnd = random.Random(seed)
pool = ["echo", "git commit -m x", "'a b'", '"c d"', ";", "&&", "|", "it\\'s", "# c\n",
        "$'q\\'r'", "\n", "GIT_INDEX_FILE=x", "git -C /tmp commit", "-o a.txt",
        '"e; git commit -m z"', "'f && git commit'", "printf %s", "don't", '"g\\"h"', "$(echo i)"]
for _ in range(n):
    words = [rnd.choice(pool) for _ in range(rnd.randint(2, 7))]
    sys.stdout.write(" ".join(words) + "\0")
PY

total=0; differ=0; dq=0; warned=0
while IFS= read -r -d '' c; do
  total=$((total + 1))
  case $c in *'"$('*) dq=$((dq + 1)) ;; esac
  [ -n "$(run "$B" PreToolUse "$c")" ] && warned=$((warned + 1))
  for ev in PreToolUse PostToolUse; do
    if [ "$(run "$A" $ev "$c")" != "$(run "$B" $ev "$c")" ]; then
      differ=$((differ + 1)); printf '  differ %s: %q\n' "$ev" "$c"
    fi
  done
done < "$F/cases.bin"
printf 'seed=%s cases=%s has_dq_subst=%s warned=%s diff=%s\n' "$SEED" "$total" "$dq" "$warned" "$differ"
