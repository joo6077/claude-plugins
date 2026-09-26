# U 판 api-kit/README.md 의 MD060 경고를 AUTO:evals 블록 안 · 밖으로 나눠 센다. 인자: 판(커밋)
W=/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak-c4a
MDL=${MDL:-/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/bda55d45-296c-491f-89ba-b52042d58e72/scratchpad/c4a/mdlint}
T=$(mktemp -d) || exit 2
git -C "$W" show "${1}:api-kit/README.md" > "$T/README.md" || exit 2
range=$(awk '/<!-- AUTO:evals -->/{a=NR} /<!-- \/AUTO:evals -->/{b=NR} END{print a" "b}' "$T/README.md")
(cd "$T" && "$MDL/node_modules/.bin/markdownlint-cli2" --config "$MDL/.markdownlint-cli2.jsonc" README.md 2>&1) \
  | grep -E '^README.md:[0-9]+' | awk -v r="$range" 'BEGIN{split(r,x," ")} {split($1,p,":"); rule=$0; sub(/.* MD/,"MD",rule); sub(/\/.*/,"",rule); inb=(p[2]>x[1] && p[2]<x[2]); k=rule (inb?"_in":"_out"); c[k]++} END{printf "block=%s-%s", x[1], x[2]; for (k in c) printf " %s=%d", k, c[k]; print ""}'
rm -rf "$T"
