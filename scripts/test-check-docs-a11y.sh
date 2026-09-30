#!/usr/bin/env bash
# scripts/check-docs-a11y.js 를 답을 아는 docs/ 둘에 돌려 종료 코드와 끝 줄을 맞댄다.
# 계약 after-0929-codex-silent-pass 의 스크립트-07 을 따른다. A11Y_TOOL 로 대상 스크립트를,
# NODE_MODULES 로 playwright-core 를 찾을 폴더를 바꿀 수 있다 (기본: 레포 node_modules — npm ci 뒤).
# 종료 코드는 harness/evals/gate-exit-codes.md — 0 통과 · 1 실패 · 2 준비 실패

here=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
root=$(cd "$here/.." && pwd)
target=${A11Y_TOOL:-$root/scripts/check-docs-a11y.js}
modules=${NODE_MODULES:-$root/node_modules}
[ -f "$target" ] || { echo "대상 스크립트가 없다: $target" >&2; exit 2; }
[ -d "$modules/playwright-core" ] || { echo "playwright-core 가 없다 (npm ci 를 먼저): $modules" >&2; exit 2; }

work=$(mktemp -d "${TMPDIR:-/tmp}/a11y-test.XXXXXX") || exit 2
trap 'rm -rf "$work"' EXIT
fails=0

check() {  # check <이름> <기대> <실제>
  if [ "$2" = "$3" ]; then echo "PASS $1"; else printf 'FAIL %s\n기대:\n%s\n실제:\n%s\n' "$1" "$2" "$3"; fails=$((fails + 1)); fi
}

# HTML 이 0 개인 docs/ — 0/0 PASS 로 통과시키면 안 된다
mkdir -p "$work/empty/docs"
printf '# md 만 있다\n' >"$work/empty/docs/readme.md"
out=$(cd "$work/empty" && NODE_PATH=$modules node "$target" 2>&1); rc=$?
pass_lines=$(printf '%s\n' "$out" | grep -c 'PASS$')
check HTML없음 "rc=2 pass_lines=0" "rc=$rc pass_lines=$pass_lines"

# 대비 · 넘침 모두 괜찮은 페이지 하나 — 1/1 PASS
mkdir -p "$work/one/docs"
printf '<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>t</title></head><body style="background:#fff;color:#000"><p>본문</p></body></html>\n' >"$work/one/docs/a.html"
out=$(cd "$work/one" && NODE_PATH=$modules node "$target" 2>&1); rc=$?
check 페이지하나 "rc=0 last=1/1 PASS" "rc=$rc last=$(printf '%s\n' "$out" | tail -1)"

echo "실패 $fails 건"
[ "$fails" = 0 ]
