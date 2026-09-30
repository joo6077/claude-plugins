#!/usr/bin/env bash
# 완료 검사(SKILL.md 4.3) 시험 파일을 따로 돌린다 — 음성 대조 표의 기대와 (2) 실행 줄을 SKILL.md 에서 읽어 원본 완료 검사로 판정한다.
# 시험 파일 이름과 기대는 SKILL.md 한 곳에만 적는다. 이 스크립트에 이름을 다시 적으면 둘이 어긋난다.
# 다른 사본을 잴 때: BAMBU_GATE_SKILL=<SKILL.md 사본> bash run-gate-fixtures.sh
# 표가 `[미검증]` 줄 수를 적은 행은 그 수까지 맞아야 일치다 — FAIL 줄과 종료 코드만 보면 못 읽은 칸 알림이 빠지거나 늘어도 모른다.
# 슬라이서가 없는 기계(리눅스 CI)에서는 설치본이 있어야 판정되는 FAIL 기대 파일과, 판정은 맞았는데 `[미검증]` 줄 수만 잴 수 없는 경우를 「건너뜀」 으로 적는다 — 일치로 세지 않는다. 판정이 틀리면 슬라이서가 없어도 불일치다.
# 같은 시험 파일의 표 행이나 실행 줄이 둘 이상이면 불일치다 — 표는 첫 행만 읽혀 나머지 기대가 한 번도 안 재진다.
# 종료 코드: 0 불일치 없음 · 1 불일치 있음 · 2 완료 검사 · 표 · 실행 줄을 못 읽음
set -u
HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
KIT=$(cd "$HERE/.." && pwd)
SKILL=${BAMBU_GATE_SKILL:-$KIT/skills/bambu-print-profile/SKILL.md}
FX=$HERE/gate-fixtures
export SKILL_DIR=$KIT/skills/bambu-print-profile
# 설치본이 있어야 돌아가는 검사 — 옵션 목록을 쓰는 셋과 시스템 부모값을 쓰는 여섯. 표 기대 칸의 첫 낱말과 맞춘다
NEEDS_SLICER='^(모르는 키|키 스코프 불일치|받지 않는 값|허공 위 속도|thin 라우팅|벽 예산|유량비|소재 부모값|카메라 준비 블록 없음)$'

T=$(mktemp -d "${TMPDIR:-/tmp}/rgf.XXXXXX") || exit 2
trap 'rm -rf "$T"' EXIT

A=$(grep -n '^TARGET_SLICER=.* python3 - ' "$SKILL" 2>/dev/null | head -1 | cut -d: -f1)
B=""
[ -n "$A" ] && B=$(awk -v s="$A" 'NR>s && $0=="PY" {print NR; exit}' "$SKILL")
if [ -n "$A" ] && [ -n "$B" ]; then sed -n "$((A+1)),$((B-1))p" "$SKILL" > "$T/gate.py"; else : > "$T/gate.py"; fi
# 빈 파일을 python3 로 돌리면 종료 코드 0 이라 모든 PASS 기대가 일치처럼 보인다
grep -q 'RESULT' "$T/gate.py" || { echo "STOP 완료 검사를 못 뽑았다 — $SKILL"; exit 2; }

# 표 → 이름 · 슬라이서 · 기대(fail|pass) · 검사 종류 · `[미검증]` 줄 수 기대(적지 않았으면 -)
awk -F'|' '/^\| `evals\/gate-fixtures\/[^`]+\.json` \|/ {
  name = $2; gsub(/^ *`evals\/gate-fixtures\/|` *$/, "", name)
  slicer = $3; gsub(/ /, "", slicer)
  kind = $4
  unv = "-"
  if (match(kind, /`\[미검증\]` [0-9]+ 줄/)) { unv = substr(kind, RSTART, RLENGTH); gsub(/[^0-9]/, "", unv) }
  if (kind ~ /FAIL 1 건/) { expect = "fail"; sub(/ *\*\*FAIL 1 건.*$/, "", kind); gsub(/^ +/, "", kind) }
  else if (kind ~ /PASS|FAIL 0 건/) { expect = "pass"; kind = "-" }
  else { expect = "?"; kind = "-" }
  print name "\t" slicer "\t" expect "\t" kind "\t" unv
}' "$SKILL" > "$T/table.tsv"
# (2) 실행 줄 → 이름 · 슬라이서
# shellcheck disable=SC2016  # $GATE · $FX 는 SKILL.md 실행 줄의 글자 그대로다
grep -E '^TARGET_SLICER=[a-z]+ +python3 "\$GATE" \$FX/[^;]+;' "$SKILL" \
  | sed -E 's/^TARGET_SLICER=([a-z]+) +python3 "\$GATE" \$FX\/([^;]+);.*/\2 \1/' > "$T/runs.txt"
if [ ! -s "$T/table.tsv" ] || [ ! -s "$T/runs.txt" ]; then
  echo "STOP 음성 대조 표 $(awk 'END{print NR}' "$T/table.tsv") 행 · 실행 줄 $(awk 'END{print NR}' "$T/runs.txt") 개 — 둘 다 있어야 잰다"; exit 2
fi

n=0; bad=0; skip=0
miss() { n=$((n + 1)); bad=$((bad + 1)); echo "불일치 $1"; }

# 폴더 · 표 · 실행 줄이 서로 맞는지 — 한쪽에만 있으면 그 시험 파일은 한 번도 안 돈다
find "$FX" -maxdepth 1 -name '*.json' -exec basename {} \; | sort > "$T/folder.txt"
cut -f1 "$T/table.tsv" | sort -u > "$T/in-table.txt"
awk '{print $1}' "$T/runs.txt" | sort -u > "$T/in-runs.txt"
while read -r name; do miss "표에 없음 $name"; done < <(comm -23 "$T/folder.txt" "$T/in-table.txt")
while read -r name; do miss "실행 줄에 없음 $name"; done < <(comm -23 "$T/folder.txt" "$T/in-runs.txt")
while read -r name; do miss "폴더에 없음 $name"; done < <(sort -u "$T/in-table.txt" "$T/in-runs.txt" | comm -23 - "$T/folder.txt")
while read -r count name; do miss "$name — 표 행 중복 $count 줄"; done < <(cut -f1 "$T/table.tsv" | sort | uniq -c | awk '$1 > 1')
while read -r count name; do miss "$name — 실행 줄 중복 $count 줄"; done < <(awk '{print $1}' "$T/runs.txt" | sort | uniq -c | awk '$1 > 1')

while read -r name slicer; do
  [ -f "$FX/$name" ] || continue
  row=$(awk -F'\t' -v x="$name" '$1 == x' "$T/table.tsv" | head -1)
  [ -n "$row" ] || continue
  IFS=$'\t' read -r _ want_slicer expect kind want_unv <<< "$row"
  if [ "$slicer" != "$want_slicer" ]; then miss "$name — 실행 줄 슬라이서 $slicer 가 표의 $want_slicer 와 다르다"; continue; fi
  if [ "$expect" = "?" ]; then miss "$name — 표의 기대 칸을 못 읽었다"; continue; fi
  out=$(TARGET_SLICER="$slicer" python3 "$T/gate.py" "$FX/$name" 2>&1); rc=$?
  fails=$(printf '%s\n' "$out" | grep -c '^FAIL ')
  passed=$(printf '%s\n' "$out" | grep -c '^RESULT: PASS$')
  unv=$(printf '%s\n' "$out" | grep -c '^\[미검증\] ')
  no_slicer=$(printf '%s\n' "$out" | grep -c '^\[미검증\] .*설치본 경로 없음')
  n=$((n + 1))
  verdict_ok=0
  if { [ "$expect" = fail ] && [ "$fails" = 1 ] && [ "$rc" = 1 ]; } || { [ "$expect" = pass ] && [ "$passed" = 1 ] && [ "$rc" = 0 ]; }; then verdict_ok=1; fi
  if [ "$verdict_ok" = 1 ] && { [ "$want_unv" = - ] || [ "$unv" = "$want_unv" ]; }; then
    echo "일치 $name"
  elif [ "$no_slicer" -gt 0 ] && [ "$expect" = fail ] && printf '%s\n' "$kind" | grep -qE "$NEEDS_SLICER"; then
    skip=$((skip + 1)); echo "건너뜀 $name — $slicer 설치본이 없어 「${kind}」 검사가 안 돈다"
  elif [ "$verdict_ok" = 1 ] && [ "$no_slicer" -gt 0 ] && [ "$want_unv" != - ]; then
    skip=$((skip + 1)); echo "건너뜀 $name — $slicer 설치본이 없어 \`[미검증]\` $want_unv 줄 기대를 잴 수 없다 (나온 \`[미검증]\` $unv 줄)"
  elif [ "$verdict_ok" = 1 ]; then
    bad=$((bad + 1)); echo "불일치 $name — \`[미검증]\` 기대 $want_unv 줄 · 결과 $unv 줄"
  else
    bad=$((bad + 1)); echo "불일치 $name — 기대 $expect · 결과 FAIL $fails 줄 · 종료 코드 $rc"
  fi
done < "$T/runs.txt"

if [ "$skip" -gt 0 ]; then echo "결과: $n 경우 중 불일치 $bad · 건너뜀 $skip"; else echo "결과: $n 경우 중 불일치 $bad"; fi
[ "$bad" = 0 ]
