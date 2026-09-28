#!/bin/sh
# run-gate-fixtures.sh 를 SKILL.md 사본 다섯 개로 돌린다 (B5). 쓰임: sh b5-controls.sh <레포 뿌리>
#   noinst — 슬라이서 설치 경로를 없는 경로로 바꾼 사본 (리눅스 CI 흉내)
#   m1 — 모든 출력에 가짜 [미검증] 줄 하나를 더한 사본
#   m2 — 소재 슬롯 못 읽음 알림 줄을 지운 사본
#   m3 — 외벽 속도 슬롯 못 읽음 알림 줄을 지운 사본
#   m4 — 벽 예산 미기록 알림 줄을 지운 사본
# 사본마다 「변이 <이름> 차이줄=<n>」 과 러너의 마지막 두 줄 · 종료 코드 · 불일치/건너뜀 줄을 찍는다.
R=${1}
S=$R/bambu-kit/skills/bambu-print-profile/SKILL.md
D=$(mktemp -d "${TMPDIR:-/tmp}/b5c.XXXXXX") || exit 2
sed 's#/Applications/#/nonexistent-apps/#g' "$S" > "$D/noinst.md"
sed -E 's/^for u in unverified: print\(f"\[미검증\] \{u\}"\)$/unverified.append("가짜 미검증 줄")\
&/' "$S" > "$D/m1.md"
sed -E 's/^( *)unverified\.append\(f"\{f\}: \{k\} 슬롯 .*$/\1pass/' "$S" > "$D/m2.md"
sed -E 's/^( *)unverified\.append\(f"\{f\}: outer_wall_speed 슬롯 .*$/\1pass/' "$S" > "$D/m3.md"
sed -E 's/^( *)unverified\.append\(f"\{f\}: _wall_budget_short_share 미기록.*$/\1pass/' "$S" > "$D/m4.md"
for v in noinst m1 m2 m3 m4; do
  n=$(diff "$S" "$D/$v.md" | grep -cE '^[<>]')
  echo "변이 $v 차이줄=$n"
  out=$(BAMBU_GATE_SKILL="$D/$v.md" bash "$R/bambu-kit/evals/run-gate-fixtures.sh" 2>&1); rc=$?
  printf '%s\n' "$out" | grep -E '^(불일치|건너뜀|결과|STOP)' | sed 's/^/  /'
  echo "  rc=$rc"
done
rm -rf "$D"
