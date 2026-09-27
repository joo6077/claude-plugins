#!/bin/bash
# 사용: lint.sh <저장소 폴더> <파일 목록 파일>
# 편집기와 같은 설정(markdownlint-cli2 0.23.2 · MD013 끔)으로 목록 파일만 잰다.
# 경고 줄을 그대로 내고, 끝에 LINTED=<검사한 파일 수> WARNINGS=<경고 줄 수> 한 줄을 낸다.
# 검사기가 돌지 않으면 LINTED 가 비어 STOP 을 내고 종료 코드 2 로 멈춘다.
S=/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/bda55d45-296c-491f-89ba-b52042d58e72/scratchpad/mdlint
R=${1:?저장소}; L=${2:?목록}
cd "$R" || exit 2
[ -s "$L" ] || { echo "STOP 목록 파일 없음: $L"; exit 2; }
out=$("$S/node_modules/.bin/markdownlint-cli2" --config "$S/cfg.jsonc" $(cat "$L") 2>&1)
linted=$(printf '%s\n' "$out" | sed -E -n 's/^Linting: ([0-9]+) file.*/\1/p')
[ -n "$linted" ] || { printf '%s\n' "$out" | tail -5; echo "STOP 검사기가 돌지 않았다"; exit 2; }
warn=$(printf '%s\n' "$out" | grep -E '^[^ ]+:[0-9]+' )
printf '%s\n' "$warn" | grep .
echo "LINTED=$linted WARNINGS=$(printf '%s\n' "$warn" | grep -c .)"
exit 0
