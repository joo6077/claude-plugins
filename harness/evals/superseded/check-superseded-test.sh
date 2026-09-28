#!/usr/bin/env bash
# harness/scripts/check-superseded.sh 를 손으로 답을 아는 폴더 둘과 없는 폴더에 돌려 기대 출력과 맞댄다.
# 계약 after-0928-harness-checks 의 SC-02 를 따른다. CHECK_SUPERSEDED 로 대상 스크립트를 바꿀 수 있다.

here=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
root=$(cd "$here/../../.." && pwd)
target=${CHECK_SUPERSEDED:-$root/harness/scripts/check-superseded.sh}
[ -f "$target" ] || { echo "대상 스크립트가 없다: $target" >&2; exit 2; }

work=$(mktemp -d "${TMPDIR:-/tmp}/superseded-test.XXXXXX") || exit 2
trap 'rm -rf "$work"' EXIT
fails=0

check() {  # check <이름> <기대> <실제>
  if [ "$2" = "$3" ]; then echo "PASS $1"; else printf 'FAIL %s\n기대:\n%s\n실제:\n%s\n' "$1" "$2" "$3"; fails=$((fails + 1)); fi
}
contract() {  # contract <폴더> <슬러그> <머리 줄…>
  folder=$1 slug=$2; shift 2
  { printf -- '---\nslug: %s\n' "$slug"; printf '%s\n' "$@"; printf -- '---\n\n## Skill\n- [ ] SK-01: x\n'; } >"$folder/sprint-contract-$slug.md"
}

# 폴더 A — superseded 넷 가운데 a 만 옳다. f 는 active 라 세지 않는다
dir_a=$work/a/.harness; mkdir -p "$dir_a"
contract "$dir_a" a 'status: superseded   # 새 판 있음' 'superseded_by: b'
contract "$dir_a" b 'status: active'
contract "$dir_a" c 'status: superseded'
contract "$dir_a" d 'status: superseded' 'superseded_by: no-such'
contract "$dir_a" e 'status: superseded' 'superseded_by: a'
contract "$dir_a" f 'status: active'
out=$(bash "$target" "$dir_a" 2>&1); rc=$?
check A-넷중셋위반 "$(printf '%s\n' \
  "OK $dir_a/sprint-contract-a.md -> b" \
  "MISSING_BY $dir_a/sprint-contract-c.md" \
  "MISSING_TARGET $dir_a/sprint-contract-d.md -> no-such" \
  "CHAIN $dir_a/sprint-contract-e.md -> a" \
  "checked=4 violations=3" \
  "rc=1")" "$out
rc=$rc"

# 폴더 B — 하나를 재고 위반 없음
dir_b=$work/b/.harness; mkdir -p "$dir_b"
contract "$dir_b" x 'status: superseded' 'superseded_by: y'
contract "$dir_b" y 'status: done'
out=$(bash "$target" "$dir_b" 2>&1); rc=$?
check B-위반없음 "$(printf '%s\n' "OK $dir_b/sprint-contract-x.md -> y" "checked=1 violations=0" "rc=0")" "$out
rc=$rc"

# 없는 폴더 — 위반 0 으로 통과시키면 안 된다
bash "$target" "$work/no-such/.harness" >/dev/null 2>&1; rc=$?
check 없는폴더 "rc=2" "rc=$rc"

echo "실패 $fails 건"
[ "$fails" = 0 ]
