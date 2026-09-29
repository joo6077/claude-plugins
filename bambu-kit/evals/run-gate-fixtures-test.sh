#!/usr/bin/env bash
# run-gate-fixtures.sh 가 음성 대조 표의 같은 시험 파일 행 중복과 실행 줄 중복을 불일치로 잡는지 본다.
# 계약 after-0929-codex-silent-pass 의 스크립트-08 을 따른다. RUN_GATE_FIXTURES 로 대상 스크립트를 바꿀 수 있다.
# SKILL.md 사본은 대상 스크립트 옆 킷의 것을 떠서 행 하나 · 실행 줄 하나를 겹친다. 원본 SKILL.md 는 불일치 0 이어야 한다.
# 종료 코드: 0 통과 · 1 실패 · 2 준비 실패 (사본에 중복을 못 넣음)

here=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
target=${RUN_GATE_FIXTURES:-$here/run-gate-fixtures.sh}
[ -f "$target" ] || { echo "대상 스크립트가 없다: $target" >&2; exit 2; }
skill=$(cd "$(dirname "$target")/.." && pwd)/skills/bambu-print-profile/SKILL.md
[ -f "$skill" ] || { echo "SKILL.md 가 없다: $skill" >&2; exit 2; }

work=$(mktemp -d "${TMPDIR:-/tmp}/rgf-test.XXXXXX") || exit 2
trap 'rm -rf "$work"' EXIT
fails=0
name=process-bambu-only-key-in-orca.json

check() {  # check <이름> <맞으면 1> <설명>
  if [ "$2" = 1 ]; then echo "PASS $1"; else echo "FAIL $1 — $3"; fails=$((fails + 1)); fi
}

# shellcheck disable=SC2016  # 실행 줄의 $GATE · $FX 는 SKILL.md 글자 그대로다
awk -v n="$name" '{ print } index($0, "| `evals/gate-fixtures/" n "` |") == 1 && !done { print "| `evals/gate-fixtures/" n "` | orca | **PASS** | x | y |"; done = 1 }' "$skill" >"$work/dup-row.md"
# shellcheck disable=SC2016
awk -v n="$name" '{ print } index($0, "python3 \"$GATE\" $FX/" n ";") > 0 && !done { print; done = 1 }' "$skill" >"$work/dup-run.md"
rows=$(grep -cF "| \`evals/gate-fixtures/$name\` |" "$work/dup-row.md")
# shellcheck disable=SC2016
runs=$(grep -cE '^TARGET_SLICER=[a-z]+ +python3 "\$GATE" \$FX/'"${name//./\\.}"';' "$work/dup-run.md")
[ "$rows" = 2 ] && [ "$runs" = 2 ] || { echo "사본에 중복을 못 넣었다 (표 행 $rows · 실행 줄 $runs)" >&2; exit 2; }

for kind in dup-row dup-run; do
  out=$(BAMBU_GATE_SKILL=$work/$kind.md bash "$target" 2>&1); rc=$?
  dup=$(printf '%s\n' "$out" | grep '^불일치 ' | grep -F "$name" | grep -c '중복')
  ok=0; [ "$rc" = 1 ] && [ "$dup" -ge 1 ] && ok=1
  check "$kind" "$ok" "rc=$rc 중복 불일치 줄 $dup"
done

out=$(bash "$target" 2>&1); rc=$?
last=$(printf '%s\n' "$out" | tail -1)
ok=0
case $last in "결과: "*" 경우 중 불일치 0"*) [ "$rc" = 0 ] && ok=1 ;; esac
check 원본 "$ok" "rc=$rc 끝 줄 $last"

echo "실패 $fails 건"
[ "$fails" = 0 ]
