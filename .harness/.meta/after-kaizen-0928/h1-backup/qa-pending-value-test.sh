#!/usr/bin/env bash
# qa-pending-value-test.sh <훅 파일> — ~/.claude/hooks/qa-pending-check.sh 의 머리 값 읽개 value() 시험.
# 입력 일곱과 기대값은 계약 형식 문서 fm_get 의 줄 끝 주석 규칙을 따른다. 모두 맞으면 0, 하나라도 틀리면 1, 함수를 못 떼면 2.
hook=${1:?훅 파일}
work=$(mktemp -d "${TMPDIR:-/tmp}/qapv.XXXXXX") || exit 2
trap 'rm -rf "$work"' EXIT
awk '/^[[:space:]]*function value\(line[^)]*\) \{/ { on = 1 } on { print } on && /^[[:space:]]*\}[[:space:]]*$/ { exit }' "$hook" > "$work/value.awk"
grep -q 'function value(line' "$work/value.awk" || { echo "STOP value() 를 떼지 못했다: $hook"; exit 2; }
tab=$(printf '\t')
{
  printf '%s\n' 'status: superseded   # 새 판 있음' 'superseded'
  printf '%s\n' 'status: "active" # 주석' 'active'
  printf '%s\n' 'status: active' 'active'
  printf '%s\n' 'owner_session: abc#def' 'abc#def'
  printf '%s\n' 'feature: "a # b"' 'a # b'
  printf '%s\n' "status: 'done'${tab}# 탭 앞 주석" 'done'
  printf '%s\n' 'status: active #' 'active'
} > "$work/cases"
failed=0
while IFS= read -r line && IFS= read -r want; do
  got=$(printf '%s\n' "$line" | awk "$(cat "$work/value.awk")"' { print value($0) }')
  [ "$got" = "$want" ] && continue
  echo "FAIL [$line] got=[$got] want=[$want]"
  failed=$((failed + 1))
done < "$work/cases"
echo "failed=$failed total=7"
[ "$failed" = 0 ]
