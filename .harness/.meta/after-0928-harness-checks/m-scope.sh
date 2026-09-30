#!/usr/bin/env bash
# m-scope.sh <레포> <기준 판> <가지> — 커밋이 끝난 뒤 이 가지가 바꾼 경로(.harness 밖)와 커밋마다의 맨 위 폴더 · 서명 줄을 잰다.
# 상한은 가지 이름을 풀어 쓴다. 풀리지 않으면 STOP 과 2.
# 출력: `changed=<경로, 글자 차례>` · 커밋마다 `commit <해시> tops=<맨 위 폴더 수> sig=<서명 줄 수>` · 끝 줄 `commits=<수> bad=<tops!=1 또는 sig!=1 인 커밋 수> dirty=<커밋 안 된 .harness 밖 변경 수>`
R=${1:?레포}; BASE=${2:?기준 판}; BR=${3:?가지}
cd "$R" || exit 2
TIP=$(git rev-parse --verify -q "refs/heads/$BR^{commit}") || { echo "STOP $BR 가 풀리지 않는다"; exit 2; }
printf 'changed=%s\n' "$(git diff --name-only "$BASE" "$TIP" -- . ':(exclude).harness' | LC_ALL=C sort | tr '\n' ',' | sed 's/,$//')"
n=0; bad=0
for c in $(git rev-list --no-merges "$BASE..$TIP"); do
  n=$((n + 1))
  tops=$(git show --name-only --format= "$c" | grep . | sed -E 's#/.*##' | LC_ALL=C sort -u | grep -c .)
  # 서명 줄은 모델 이름을 박지 않는다 — 모델이 바뀌어도 「Claude … <noreply@anthropic.com>」 한 줄이면 된다
  sig=$(git log -1 --format='%(trailers:key=Co-Authored-By,valueonly)' "$c" | grep -cxE 'Claude [^<>]+ <noreply@anthropic\.com>')
  { [ "$tops" = 1 ] && [ "$sig" = 1 ]; } || bad=$((bad + 1))
  printf 'commit %s tops=%s sig=%s\n' "$(git rev-parse --short "$c")" "$tops" "$sig"
done
dirty=$({ git diff --name-only HEAD; git ls-files --others --exclude-standard; } | grep -v '^\.harness/' | grep -c .)
echo "commits=$n bad=$bad dirty=$dirty"
