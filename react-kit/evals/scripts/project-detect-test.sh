#!/usr/bin/env bash
# project-detect.sh 시험 — tanstackRouter 값을 답을 아는 세 입력으로 잰다. jq 경로와 jq 를 숨긴 python3 경로 둘 다 돈다.
# 값이 없을 때 스크립트가 "null" 문자열을 내므로 비었는지로 재면 플러그인이 없어도 true 가 나온다 — none · nopkg 경우가 잡는다.
# 경로 따옴표에 역슬래시가 붙으면 jq 경로는 플러그인이 있어도 "null" 을 낸다 — jq · has 경우가 잡는다.
# 다른 사본으로 돌리기: PROJECT_DETECT=<사본 경로> bash project-detect-test.sh
set -u
HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
KIT=$(cd "$HERE/../.." && pwd)
DETECT=${PROJECT_DETECT:-$KIT/scripts/project-detect.sh}
[ -f "$DETECT" ] || { echo "스크립트가 없다 — $DETECT"; exit 2; }
command -v jq >/dev/null 2>&1 || { echo "jq 가 없다 — jq 경로를 잴 수 없다"; exit 2; }
command -v python3 >/dev/null 2>&1 || { echo "python3 가 없다 — 결과를 읽을 수 없다"; exit 2; }

W=$(mktemp -d "${TMPDIR:-/tmp}/pdt.XXXXXX") || exit 2
trap 'rm -rf "$W"' EXIT
# jq 만 빠진 PATH — 스크립트가 부르는 도구만 링크한다. /usr/bin 을 통째로 넣으면 그 안의 jq 가 보인다
mkdir -p "$W/bin"
for t in tr grep cat python3; do ln -s "$(command -v "$t")" "$W/bin/$t" || exit 2; done
if PATH="$W/bin" command -v jq >/dev/null 2>&1; then echo "jq 가 숨겨지지 않았다 — python3 경로를 잴 수 없다"; exit 2; fi

# 입력 셋 — 플러그인 없음 · 있음 · package.json 없음
mkdir -p "$W/none" "$W/has" "$W/nopkg"
cp "$KIT/evals/test-fixtures/empty-project/package.json" "$W/none/package.json" || exit 2
cp "$KIT/templates/package.json.template" "$W/has/package.json" || exit 2

n=0; bad=0
check() {  # check <경로 이름> <PATH> <입력 폴더> <답>
  local out got
  out=$(cd "$W/$3" && PATH="$2" "$BASH" "$DETECT" 2>&1)
  got=$(printf '%s' "$out" | python3 -c 'import json, sys; print(str(json.load(sys.stdin)["tanstackRouter"]).lower())' 2>/dev/null) || got=읽기실패
  n=$((n + 1))
  if [ "$got" = "$4" ]; then echo "일치 $1 $3 tanstackRouter=$got"
  else echo "불일치 $1 $3 tanstackRouter=$got (답 $4)"; bad=$((bad + 1)); fi
}
for mode in jq python3; do
  if [ "$mode" = jq ]; then P=$PATH; else P=$W/bin; fi
  check "$mode" "$P" none false
  check "$mode" "$P" has true
  check "$mode" "$P" nopkg false
done
echo "결과: $n 경우 중 불일치 $bad"
[ "$bad" = 0 ]
