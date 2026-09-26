#!/usr/bin/env bash
# 레포 시험 commit-guard-test.sh 를 기준 판 훅과 지금 훅으로 각각 돌려 PASS · FAIL 줄 수를 낸다.
# 사용: guard_test_neg.sh <레포 또는 워크트리> <기준 커밋>
repo=${1:?}; base=${2:?}
t=$(mktemp -d "${TMPDIR:-/tmp}/guard-neg.XXXXXX"); trap 'rm -rf "$t"' EXIT
git -C "$repo" show "$base:harness/scripts/commit-guard.sh" >"$t/old.sh" || { echo "STOP 기준 훅을 못 꺼냄"; exit 2; }
test_sh=$repo/harness/evals/hooks/commit-guard-test.sh
COMMIT_GUARD_HOOK=$t/old.sh bash "$test_sh" >"$t/old.out" 2>&1; old_rc=$?
bash "$test_sh" >"$t/new.out" 2>&1; new_rc=$?
grep '^FAIL' "$t/old.out" | sed 's/^/  old /'
grep '^FAIL' "$t/new.out" | sed 's/^/  new /'
printf 'old_fail=%s old_rc=%s new_pass=%s new_fail=%s new_rc=%s\n' \
  "$(grep -c '^FAIL' "$t/old.out")" "$old_rc" "$(grep -c '^PASS' "$t/new.out")" "$(grep -c '^FAIL' "$t/new.out")" "$new_rc"
