#!/usr/bin/env bash
# bambu-nosl.sh <레포 폴더> — 완료 검사 시험을 두 번 돈다: 이 기계 그대로 · 슬라이서 설치본 경로를 없는 경로로 바꾼 SKILL.md 사본.
# 그리고 시험 파일 process-thin-unreadable-slot.json 하나를 원본 완료 검사로 돌려 `[미검증]` 줄 수와 벽 예산 미기록 줄 수를 찍는다.
# 줄: here <결과 끝 줄> rc=<n> · noslicer <결과 끝 줄> rc=<n> · thin-unreadable fails=<n> unv=<n> wall=<n> rc=<n>
repo=${1:?레포 폴더}
kit=$repo/bambu-kit
skill=$kit/skills/bambu-print-profile/SKILL.md
[ -f "$skill" ] || { echo "SKILL.md 가 없다: $skill" >&2; exit 2; }
t=$(mktemp -d "${TMPDIR:-/tmp}/bambu-nosl.XXXXXX") || exit 2
trap 'rm -rf "$t"' EXIT

out=$(bash "$kit/evals/run-gate-fixtures.sh" 2>&1); rc=$?
echo "here $(printf '%s\n' "$out" | tail -1) rc=$rc"

sed -e 's#/Applications/BambuStudio\.app#/nonexistent/BambuStudio.app#g' \
    -e 's#/Applications/OrcaSlicer\.app#/nonexistent/OrcaSlicer.app#g' "$skill" > "$t/SKILL.md"
left=$(grep -c '/Applications/\(BambuStudio\|OrcaSlicer\)\.app' "$t/SKILL.md")
out=$(BAMBU_GATE_SKILL="$t/SKILL.md" bash "$kit/evals/run-gate-fixtures.sh" 2>&1); rc=$?
echo "noslicer $(printf '%s\n' "$out" | tail -1) rc=$rc left_paths=$left"
printf '%s\n' "$out" | grep '^불일치' | sed 's/^/  /'

a=$(grep -n '^TARGET_SLICER=.* python3 - ' "$skill" | head -1 | cut -d: -f1)
b=$(awk -v s="$a" 'NR>s && $0=="PY" {print NR; exit}' "$skill")
sed -n "$((a+1)),$((b-1))p" "$skill" > "$t/gate.py"
g=$(SKILL_DIR=$kit/skills/bambu-print-profile TARGET_SLICER=bambu python3 "$t/gate.py" "$kit/evals/gate-fixtures/process-thin-unreadable-slot.json" 2>&1); rc=$?
echo "thin-unreadable fails=$(printf '%s\n' "$g" | grep -c '^FAIL ') unv=$(printf '%s\n' "$g" | grep -c '^\[미검증\] ') wall=$(printf '%s\n' "$g" | grep -c '_wall_budget_short_share 미기록') rc=$rc"
