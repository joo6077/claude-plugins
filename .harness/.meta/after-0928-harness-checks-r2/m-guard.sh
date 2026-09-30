#!/usr/bin/env bash
# m-guard.sh <레포> <판> — 가지 끝(작업 폴더)의 commit-guard 시험을 <판> 의 commit-guard.sh 에 돌린다.
# 훅은 `git show <판>:harness/scripts/commit-guard.sh` 로 임시 사본을 떠서 COMMIT_GUARD_HOOK 으로 넘긴다.
# 출력 한 줄: `guard <판> rc=<시험 종료 코드> fails=<실패 수> s24=<PASS|FAIL|none> s25=… s26=…`
R=${1:?레포}; REV=${2:?판}
T=$(mktemp -d "${TMPDIR:-/tmp}/mguard.XXXXXX") || exit 2
trap 'rm -rf "$T"' EXIT
cd "$R" || exit 2
git show "$REV:harness/scripts/commit-guard.sh" > "$T/commit-guard.sh" 2>/dev/null || { echo "STOP $REV 에 commit-guard.sh 없음"; exit 2; }
chmod +x "$T/commit-guard.sh"
TMPDIR="$T" COMMIT_GUARD_HOOK="$T/commit-guard.sh" bash harness/evals/hooks/commit-guard-test.sh > "$T/out" 2>&1
rc=$?
st() { l=$(grep -E "^(PASS|FAIL) SCOPE-$1-" "$T/out" | head -1); [ -n "$l" ] && echo "${l%% *}" || echo none; }
fails=$(sed -n -E 's/^실패 ([0-9]+) 건$/\1/p' "$T/out" | tail -1)
echo "guard $REV rc=$rc fails=${fails:-?} s24=$(st s24) s25=$(st s25) s26=$(st s26)"
