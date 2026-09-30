#!/usr/bin/env bash
# m-qapending.sh <훅 파일> — 레포 밖 qa-pending-check.sh 의 머리 값 읽개 value() 를 떼어 일곱 입력에 돌린다.
# 입력과 기대값은 1 회차 SK-01 과 같다 (계약 형식 문서 §값 따옴표 규약의 fm_get 규칙).
# 함수는 `function value(line…) {` 줄(지역 변수를 더해도 된다)부터 처음 나오는 `  }` 줄까지 뗀다 — 못 떼면 STOP 과 2.
# 출력: 입력마다 `<번호> got=[…] want=[…] <OK|NG>`, 끝 줄 `ng=<수> total=7`. ng 가 0 이 아니면 1.
H=${1:?훅 파일}
T=$(mktemp -d "${TMPDIR:-/tmp}/mqap.XXXXXX") || exit 2
trap 'rm -rf "$T"' EXIT
awk '/^[[:space:]]*function value\(line[^)]*\) \{/ { on = 1 } on { print } on && /^[[:space:]]*\}[[:space:]]*$/ { exit }' "$H" > "$T/fn.awk"
grep -q 'function value(line' "$T/fn.awk" && [ "$(tail -1 "$T/fn.awk" | tr -d ' \t')" = "}" ] || { echo "STOP value() 를 떼지 못했다"; exit 2; }
TAB=$(printf '\t')
{
  printf '%s\n' 'status: superseded   # 새 판 있음' 'superseded'
  printf '%s\n' 'status: "active" # 주석' 'active'
  printf '%s\n' 'status: active' 'active'
  printf '%s\n' 'owner_session: abc#def' 'abc#def'
  printf '%s\n' 'feature: "a # b"' 'a # b'
  printf '%s\n' "status: 'done'${TAB}# 탭 앞 주석" 'done'
  printf '%s\n' 'status: active #' 'active'
} > "$T/cases"
ng=0; i=0
while IFS= read -r line && IFS= read -r want; do
  i=$((i + 1))
  got=$(printf '%s\n' "$line" | awk "$(cat "$T/fn.awk")"' { print value($0) }')
  if [ "$got" = "$want" ]; then r=OK; else r=NG; ng=$((ng + 1)); fi
  echo "$i got=[$got] want=[$want] $r"
done < "$T/cases"
echo "ng=$ng total=$i"
[ "$ng" = 0 ]
