#!/usr/bin/env bash
# harness/scripts/check-superseded.sh 를 손으로 답을 아는 폴더 둘과 없는 폴더에 돌려 기대 출력과 맞댄다.
# 계약 after-0928-harness-checks 의 SC-02 와 after-0929-codex-silent-pass 의 스크립트-05 를 따른다. CHECK_SUPERSEDED 로 대상 스크립트를 바꿀 수 있다.

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
  "checked=4 violations=3 unreadable=0" \
  "rc=1")" "$out
rc=$rc"

# 폴더 B — 하나를 재고 위반 없음
dir_b=$work/b/.harness; mkdir -p "$dir_b"
contract "$dir_b" x 'status: superseded' 'superseded_by: y'
contract "$dir_b" y 'status: done'
out=$(bash "$target" "$dir_b" 2>&1); rc=$?
check B-위반없음 "$(printf '%s\n' "OK $dir_b/sprint-contract-x.md -> y" "checked=1 violations=0 unreadable=0" "rc=0")" "$out
rc=$rc"

# 못 읽는 계약 — 가리킨 새 판이든 superseded 계약 자신이든 OK 로 치지 않고 2.
# fm_get 이 내는 읽기 오류는 표준 오류로 가니 표준 출력만 맞댄다. root 로 돌면 권한을 빼도 읽혀 이 경우를 만들 수 없다
dir_c=$work/c/.harness; mkdir -p "$dir_c"
contract "$dir_c" a 'status: superseded' 'superseded_by: b'
contract "$dir_c" b 'status: active'
chmod 000 "$dir_c/sprint-contract-b.md"
[ -r "$dir_c/sprint-contract-b.md" ] && { echo "권한을 빼도 파일이 읽힌다 (root 로 도는가)" >&2; exit 2; }
out=$(bash "$target" "$dir_c" 2>"$work/err-c"); rc=$?
chmod 644 "$dir_c/sprint-contract-b.md"
check C-새판못읽음 "$(printf '%s\n' "UNREADABLE $dir_c/sprint-contract-a.md -> b" "checked=1 violations=0 unreadable=1" "rc=2")" "$out
rc=$rc"

dir_d=$work/d/.harness; mkdir -p "$dir_d"
contract "$dir_d" a 'status: superseded' 'superseded_by: b'
contract "$dir_d" b 'status: active'
chmod 000 "$dir_d/sprint-contract-a.md"
out=$(bash "$target" "$dir_d" 2>"$work/err-d"); rc=$?
chmod 644 "$dir_d/sprint-contract-a.md"
check D-계약못읽음 "$(printf '%s\n' "UNREADABLE $dir_d/sprint-contract-a.md" "checked=0 violations=0 unreadable=1" "rc=2")" "$out
rc=$rc"

# 없는 폴더 — 위반 0 으로 통과시키면 안 된다
bash "$target" "$work/no-such/.harness" >/dev/null 2>&1; rc=$?
check 없는폴더 "rc=2" "rc=$rc"

echo "실패 $fails 건"
[ "$fails" = 0 ]
