#!/usr/bin/env bash
# 가지 역사 검사 — 원래 가지 커밋이 들어왔는지, 커밋마다 맨 위 폴더 하나 · 새 서명인지, 원래 커밋을 누가 밝혔는지 센다.
# 사용: bash hist.sh <레포> <시작 판> <끝 판>
# 출력: `anc <원래 커밋 앞 8 자> yes|no` 두 줄 · `merges=<수>` · 문제 커밋마다 `MANY <커밋>` · `NOSIG <커밋>` ·
#       `cite <원래 커밋 앞 8 자> folders=<쉼표로 이은 맨 위 폴더> subj=<원래 제목을 적은 커밋 수>` 두 줄 ·
#       `cover <원래 커밋 앞 8 자> files=<실린 수>/<원래 파일 수> harness_same=<같은 수>/<.harness 파일 수>` 두 줄 · 끝 줄 `commits=<수>`
set -u
REPO=${1}; FROM=${2}; TO=${3}
SIG='Claude Opus 5.5 (1M context) <noreply@anthropic.com>'
IMPL=e55e8b3655eb2656a1a3298808664954d1e16785
QA=42209beb9c1bd86de374cdd3cf87e98e2a992843
IMPL_SUBJ='feat(bambu-kit): 오르카 · H2S 출력 피드백 반영 — 프린터 설정 검사와 실패 레시피 4종'
QA_SUBJ='chore(harness): bambu-kit 오르카 · H2S 피드백 스프린트 QA 승인 기록'
g() { git -C "$REPO" "$@"; }
g rev-parse --verify -q "$FROM^{commit}" >/dev/null && g rev-parse --verify -q "$TO^{commit}" >/dev/null \
  || { echo "STOP 판 없음 $FROM · $TO"; exit 2; }
for c in $IMPL $QA; do
  if g merge-base --is-ancestor "$c" "$TO"; then echo "anc ${c:0:8} yes"; else echo "anc ${c:0:8} no"; fi
done
echo "merges=$(g rev-list --merges "$FROM..$TO" | grep -c .)"
n=0
for c in $(g rev-list "$FROM..$TO"); do
  n=$((n+1))
  [ "$(g show --name-only --format= "$c" | cut -d/ -f1 | LC_ALL=C sort -u | grep -c .)" = 1 ] || echo "MANY $c"
  s=$(g log -1 --format='%(trailers:key=Co-Authored-By,valueonly)' "$c" | grep -c .)
  v=$(g log -1 --format='%(trailers:key=Co-Authored-By,valueonly)' "$c" | sed -n 1p)
  [ "$s" = 1 ] && [ "$v" = "$SIG" ] || echo "NOSIG $c"
done
cite() {  # cite <원래 커밋> <원래 제목>
  f=""; k=0
  for c in $(g rev-list "$FROM..$TO"); do
    b=$(g log -1 --format=%B "$c")
    printf '%s\n' "$b" | grep -qF "${1}" || continue
    f="$f $(g show --name-only --format= "$c" | cut -d/ -f1 | LC_ALL=C sort -u | tr '\n' ' ')"
    printf '%s\n' "$b" | grep -qxF "${2}" && k=$((k+1))
  done
  echo "cite ${1:0:8} folders=$(printf '%s\n' $f | grep . | LC_ALL=C sort -u | paste -sd, -) subj=$k"
}
cover() {  # cover <원래 커밋> — 원래 커밋 파일이 그 커밋을 밝힌 커밋들에 다 실렸는지, .harness 파일은 원래와 같은 내용인지
  orig=$(g show --name-only --format= "${1}" | grep .); tot=$(printf '%s\n' "$orig" | grep -c .); got=0; hn=0; hs=0
  cs=$(for c in $(g rev-list "$FROM..$TO"); do g log -1 --format=%B "$c" | grep -qF "${1}" && echo "$c"; done)
  for p in $orig; do
    hit=0
    for c in $cs; do g show --name-only --format= "$c" | grep -qxF "$p" && { hit=1; last=$c; }; done
    [ "$hit" = 1 ] && got=$((got+1))
    case "$p" in .harness/*) hn=$((hn+1)); [ "$hit" = 1 ] && [ "$(g rev-parse "$last:$p")" = "$(g rev-parse "${1}:$p")" ] && hs=$((hs+1));; esac
  done
  echo "cover ${1:0:8} files=$got/$tot harness_same=$hs/$hn"
}
cite "$IMPL" "$IMPL_SUBJ"
cite "$QA" "$QA_SUBJ"
cover "$IMPL"
cover "$QA"
echo "commits=$n"
