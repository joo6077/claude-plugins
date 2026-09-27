#!/usr/bin/env bash
# 완료 검사(SKILL.md 4.3) 시험 파일을 따로 돌린다 — 음성 대조 표의 기대와 (2) 실행 줄을 SKILL.md 에서 읽어 원본 완료 검사로 판정한다.
# 시험 파일 이름과 기대는 SKILL.md 한 곳에만 적는다. 이 스크립트에 이름을 다시 적으면 둘이 어긋난다.
# 다른 사본을 잴 때: BAMBU_GATE_SKILL=<SKILL.md 사본> bash run-gate-fixtures.sh
# 슬라이서가 없는 기계(리눅스 CI)에서는 설치본이 있어야 판정되는 FAIL 기대 파일을 「건너뜀」 으로 적는다 — 일치로 세지 않는다.
# 종료 코드: 0 불일치 없음 · 1 불일치 있음 · 2 완료 검사 · 표 · 실행 줄을 못 읽음
set -u
HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
KIT=$(cd "$HERE/.." && pwd)
SKILL=${BAMBU_GATE_SKILL:-$KIT/skills/bambu-print-profile/SKILL.md}
FX=$HERE/gate-fixtures
export SKILL_DIR=$KIT/skills/bambu-print-profile
# 설치본이 있어야 돌아가는 검사 — 옵션 목록을 쓰는 셋과 시스템 부모값을 쓰는 다섯. 표 기대 칸의 첫 낱말과 맞춘다
NEEDS_SLICER='^(모르는 키|키 스코프 불일치|받지 않는 값|허공 위 속도|thin 라우팅|벽 예산|유량비|소재 부모값)$'

T=$(mktemp -d "${TMPDIR:-/tmp}/rgf.XXXXXX") || exit 2
trap 'rm -rf "$T"' EXIT

A=$(grep -n '^TARGET_SLICER=.* python3 - ' "$SKILL" 2>/dev/null | head -1 | cut -d: -f1)
B=""
[ -n "$A" ] && B=$(awk -v s="$A" 'NR>s && $0=="PY" {print NR; exit}' "$SKILL")
if [ -n "$A" ] && [ -n "$B" ]; then sed -n "$((A+1)),$((B-1))p" "$SKILL" > "$T/gate.py"; else : > "$T/gate.py"; fi
# 빈 파일을 python3 로 돌리면 종료 코드 0 이라 모든 PASS 기대가 일치처럼 보인다
grep -q 'RESULT' "$T/gate.py" || { echo "STOP 완료 검사를 못 뽑았다 — $SKILL"; exit 2; }

# 표 → 이름 · 슬라이서 · 기대(fail|pass) · 검사 종류
awk -F'|' '/^\| `evals\/gate-fixtures\/[^`]+\.json` \|/ {
  name = $2; gsub(/^ *`evals\/gate-fixtures\/|` *$/, "", name)
  slicer = $3; gsub(/ /, "", slicer)
  kind = $4
  if (kind ~ /FAIL 1 건/) { expect = "fail"; sub(/ *\*\*FAIL 1 건.*$/, "", kind); gsub(/^ +/, "", kind) }
  else if (kind ~ /PASS|FAIL 0 건/) { expect = "pass"; kind = "-" }
  else { expect = "?"; kind = "-" }
  print name "\t" slicer "\t" expect "\t" kind
}' "$SKILL" > "$T/table.tsv"
# (2) 실행 줄 → 이름 · 슬라이서
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

while read -r name slicer; do
  [ -f "$FX/$name" ] || continue
  row=$(awk -F'\t' -v x="$name" '$1 == x' "$T/table.tsv" | head -1)
  [ -n "$row" ] || continue
  IFS=$'\t' read -r _ want_slicer expect kind <<< "$row"
  if [ "$slicer" != "$want_slicer" ]; then miss "$name — 실행 줄 슬라이서 $slicer 가 표의 $want_slicer 와 다르다"; continue; fi
  if [ "$expect" = "?" ]; then miss "$name — 표의 기대 칸을 못 읽었다"; continue; fi
  out=$(TARGET_SLICER="$slicer" python3 "$T/gate.py" "$FX/$name" 2>&1); rc=$?
  fails=$(printf '%s\n' "$out" | grep -c '^FAIL ')
  passed=$(printf '%s\n' "$out" | grep -c '^RESULT: PASS$')
  n=$((n + 1))
  if { [ "$expect" = fail ] && [ "$fails" = 1 ] && [ "$rc" = 1 ]; } || { [ "$expect" = pass ] && [ "$passed" = 1 ] && [ "$rc" = 0 ]; }; then
    echo "일치 $name"
  elif [ "$expect" = fail ] && printf '%s\n' "$kind" | grep -qE "$NEEDS_SLICER" \
      && printf '%s\n' "$out" | grep -q '^\[미검증\] .*설치본 경로 없음'; then
    skip=$((skip + 1)); echo "건너뜀 $name — $slicer 설치본이 없어 「${kind}」 검사가 안 돈다"
  else
    bad=$((bad + 1)); echo "불일치 $name — 기대 $expect · 결과 FAIL $fails 줄 · 종료 코드 $rc"
  fi
done < "$T/runs.txt"

if [ "$skip" -gt 0 ]; then echo "결과: $n 경우 중 불일치 $bad · 건너뜀 $skip"; else echo "결과: $n 경우 중 불일치 $bad"; fi
[ "$bad" = 0 ]
