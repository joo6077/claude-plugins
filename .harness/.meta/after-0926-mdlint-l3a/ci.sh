#!/bin/bash
# 사용: ci.sh <저장소 폴더>
# ci-local.sh 를 이 실행만의 임시 폴더로 돌리고(다른 묶음과 요약 파일을 나눠 쓰지 않게), ci.yml 에만 있는 세 단계를 더 돌린다.
# ci-local.sh 의 종료 코드는 판정에 쓰지 않는다 — 마지막 줄이 `grep -v 'rc=0'` 이라 실패 줄이나 SKIP 줄이 있을 때 0 을 낸다.
# 판정은 요약 줄로 한다: 끝 줄 `CI_OK=<n> CI_BAD=<n> CI_SKIP=<n>` — CI_BAD 는 rc=0 도 yq SKIP 도 아닌 줄 수.
R=${1:?저장소}
cd "$R" || exit 2
T=$(mktemp -d "${TMPDIR:-/tmp}/l3a-ci.XXXXXX") || exit 2
TMPDIR=$T bash /Users/jackson/Hub/10_Dev/claude-plugins/.harness/handoff/2026-09-26-tools/ci-local.sh "$R" > "$T/ci-local.out" 2>&1
S=$T/ci-local/summary.txt
[ -s "$S" ] || { echo "STOP ci-local 요약 없음 — $T"; exit 2; }
extra() { name=$1; shift; "$@" > "$T/$name.log" 2>&1; printf '%-28s rc=%s\n' "$name" "$?" >> "$S"; }
extra cause-table-copies  python3 scripts/check-cause-table-copies.py
extra docs-drift-table    python3 scripts/detect-docs-drift.py --check-table
extra measure-helpers     bash harness/evals/measure/measure-helpers-test.sh
cat "$S"
ok=$(grep -c 'rc=0$' "$S")
skip=$(grep -c '^feedback-agg-test SKIP (yq 없음)$' "$S")
bad=$(grep -v 'rc=0$' "$S" | grep -vc '^feedback-agg-test SKIP (yq 없음)$')
echo "LOGS=$T"
echo "CI_OK=$ok CI_BAD=$bad CI_SKIP=$skip"
exit 0
