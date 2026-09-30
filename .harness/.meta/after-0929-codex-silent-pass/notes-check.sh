#!/usr/bin/env bash
# notes-check.sh <notes 파일> <고치기 전 훅 폴더> <지금 훅 폴더> <레포 폴더>
# 레포 밖 훅 둘의 고친 줄과 훅 시험 출력 끝 줄이 notes 에 그대로 옮겨졌는지 잰다.
# 훅마다 한 줄: hook=<이름> diff_lines=<고친 줄 수> missing=<notes 에 없는 줄 수>
# 시험마다 한 줄: test=<이름> rc=<시험 종료 코드> last_in_notes=<시험 출력 끝 줄이 notes 에 있으면 1>
set -u
notes=${1:?notes 파일}; old=${2:?고치기 전 훅 폴더}; new=${3:?지금 훅 폴더}; repo=${4:?레포 폴더}
[ -f "$notes" ] || { echo "notes 가 없다: $notes" >&2; exit 2; }
for h in lint-contract-oracle.sh qa-pending-check.sh; do
  lines=$(diff -u "$old/$h" "$new/$h" | grep -E '^[-+]' | grep -vE '^(---|\+\+\+) ')
  n=$(printf '%s\n' "$lines" | grep -c .)
  missing=0
  while IFS= read -r line; do
    [ -n "$line" ] || continue
    grep -qF -- "$line" "$notes" || missing=$((missing + 1))
  done <<EOF
$lines
EOF
  echo "hook=$h diff_lines=$n missing=$missing"
done
for t in lint-contract-oracle-test.sh qa-pending-check-test.sh; do
  out=$(bash "$repo/harness/evals/hooks/$t" 2>&1); rc=$?
  last=$(printf '%s\n' "$out" | grep . | tail -1)
  in=0; [ -n "$last" ] && grep -qxF -- "$last" "$notes" && in=1
  echo "test=$t rc=$rc last_in_notes=$in"
done
