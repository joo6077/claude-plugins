#!/usr/bin/env bash
# 원래 스프린트(bambu-kit-orca-h2s-feedback) 조건 중 합친 뒤에도 성립해야 하는 것을 한 번에 잰다.
# 사용: bash orig-conds.sh <레포 트리>
# 출력: 조건마다 `<ID> ok|NG <세부>` 한 줄, 끝 줄 `orig_ok=<수>/<전체>`.
set -u
cd "${1}" || exit 2
S=bambu-kit/skills/bambu-print-profile/SKILL.md
R=bambu-kit/skills/bambu-print-profile/references
FX=bambu-kit/evals/gate-fixtures
export SKILL_DIR=bambu-kit/skills/bambu-print-profile
cut_sec() { awk -v a="${2}" -v b="${3}" 'index($(0),a)==1{f=1;print;next} f&&index($(0),b)==1{exit} f' "${1}"; }
T=$(mktemp -d "${TMPDIR:-/tmp}/oc.XXXXXX"); trap 'rm -rf "$T"' EXIT
A=$(grep -n '^TARGET_SLICER=.* python3 - ' "$S" | head -1 | cut -d: -f1)
B=$(awk -v s="$A" 'NR>s && $(0)=="PY" {print NR; exit}' "$S")
sed -n "$((A+1)),$((B-1))p" "$S" > "$T/gate.py"
grep -q RESULT "$T/gate.py" || { echo "STOP gate"; exit 2; }
ok=0; all=0
chk() { all=$((all+1)); if [ "${2}" = 1 ]; then ok=$((ok+1)); echo "${1} ok"; else echo "${1} NG ${3:-}"; fi; }
toks() { # toks <ID> <file> <from> <to> <tok>...
  id=${1}; f=${2}; a=${3}; b=${4}; shift 4; miss=""
  for t in "$@"; do [ "$(cut_sec "$f" "$a" "$b" | grep -cF -- "$t")" -ge 1 ] || miss="$miss [$t]"; done
  [ -z "$miss" ] && chk "$id" 1 || chk "$id" 0 "없음:$miss"; }
toks SK-01 "$S" "### Phase 1.95" "### Phase 2" '권한 제어' 'Export plate sliced file' '다시 슬라이스' 'Bambu Connect' 'USB' 'Developer Mode'
toks SK-02 "$S" "### Phase 3" "### Phase 4" 'machine/' '§11.5'
toks SK-03 "$S" "#### 4.1" "#### 4.2" 'machine/'
toks SK-04 "$S" "#### 4.4" "### Phase 5" '더블클릭' 'Transfer' '프로젝트 열기' 'BS start'
toks SK-05 "$S" "## Gotcha 체크리스트" "## MakerWorld" 'M1028' 'brim_ears' '가로 구멍' '다림질'
run() { TARGET_SLICER=${1} python3 "$T/gate.py" "${2}" > "$T/out" 2>&1; echo $? > "$T/rc"; }
run orca "$FX/machine-orca-h2s-bs-start.json"
chk SC-01 "$( [ "$(cat "$T/rc")" = 0 ] && [ "$(tail -1 "$T/out")" = 'RESULT: PASS' ] && [ "$(grep -c '^\[미검증\]' "$T/out")" = 0 ] && echo 1)" "rc=$(cat "$T/rc") last=$(tail -1 "$T/out") unv=$(grep -c '^\[미검증\]' "$T/out")"
run orca "$FX/machine-orca-h2s-no-camera-prep.json"
chk SC-02 "$( [ "$(cat "$T/rc")" = 1 ] && [ "$(grep -c '^FAIL' "$T/out")" = 1 ] && [ "$(grep '^FAIL' "$T/out" | grep -cF M1028)" = 1 ] && echo 1)" "rc=$(cat "$T/rc") fails=$(grep -c '^FAIL' "$T/out")"
run orca "$FX/machine-orca-h2s-cooling-filter-var.json"
chk SC-03 "$( [ "$(cat "$T/rc")" = 1 ] && [ "$(grep -c '^FAIL' "$T/out")" = 1 ] && [ "$(grep '^FAIL' "$T/out" | grep -cF cooling_filter_enabled)" = 1 ] && echo 1)" "rc=$(cat "$T/rc") fails=$(grep -c '^FAIL' "$T/out")"
run orca "$FX/machine-orca-x1c.json"
chk SC-04 "$( [ "$(grep '^FAIL' "$T/out" | grep -cF M1028)" = 0 ] && echo 1)"
U1="/Users/jackson/Hub/60_3D Print/Settings/fly-catcher/orca/process/fly-catcher - PLA Basic 0.12mm ORCA.json"
U2="/Users/jackson/Hub/60_3D Print/Settings/fly-catcher/orca/machine/Bambu Lab H2S 0.4 nozzle - BS start 2026-04.json"
TARGET_SLICER=orca python3 "$T/gate.py" "$U2" > "$T/out" 2>&1; rc=$?
chk SC-06a "$( [ "$rc" = 0 ] && [ "$(tail -1 "$T/out")" = 'RESULT: PASS' ] && echo 1)" "rc=$rc last=$(tail -1 "$T/out")"
# process 파일은 main 쪽 새 규칙(허공 위 속도)에 걸린다 — 그 한 줄만 FAIL 이어야 한다
TARGET_SLICER=orca python3 "$T/gate.py" "$U1" > "$T/out" 2>&1; rc=$?
chk SC-06b "$( [ "$rc" = 1 ] && [ "$(grep -c '^FAIL' "$T/out")" = 1 ] && [ "$(grep '^FAIL' "$T/out" | grep -cF '허공 위 속도')" = 1 ] && echo 1)" "rc=$rc fails=$(grep -c '^FAIL' "$T/out")"
env -u TARGET_SLICER python3 "$T/gate.py" "$FX/machine-orca-h2s-bs-start.json" > "$T/out" 2>&1
chk ER-01 "$( [ "$(grep -c '^\[미검증\]' "$T/out")" -ge 1 ] && echo 1)"
python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); d.pop("printer_settings_id",None); json.dump(d,open(sys.argv[2],"w"))' "$FX/machine-orca-h2s-bs-start.json" "$T/noid.json"
TARGET_SLICER=orca python3 "$T/gate.py" "$T/noid.json" > "$T/out" 2>&1; rc=$?
chk ER-02 "$( [ "$rc" = 1 ] && [ "$(grep '^FAIL' "$T/out" | grep -cF printer_settings_id)" -ge 1 ] && echo 1)" "rc=$rc"
toks ER-03 "$R/failure-recipes.md" "### 3.5" "## 4." '가로 구멍' '4.1' '0.1'
toks AR-01 "$R/bambu-fields-baseline.md" "### 11.5" "## " '2025/08/06' '2026/04/21' 'M104 S0 T0' 'M562 P1 E0 B1' 'M18 E' 'M1028 S1' 'M1028 S0' '50bb6ab' '#14947' 'cooling_filter_enabled'
toks AR-02a "$R/tolerance.md" "## 1.3" "## 2." '_shrink_contour_holes' '가로 구멍' 'ISO 273' '4.3' '4.5' '4.8' '눈물방울' '#7744'
toks AR-02b "$R/tolerance.md" "### 3.2" "### 3.3" '§1.3'
toks AR-03a "$R/failure-recipes.md" "### 3.5" "## 4." '0.38' '0.44' 'layer_config_ranges.xml' 'make_overhang_printable' 'brim_ears' 'Brim.cpp' 'bambu-02.08.02.61.tsv'
toks AR-03b "$R/failure-recipes.md" "### 3.1" "### 3.2" '§3.5'
toks AR-04 "$R/surface-recipes.md" "### 5.3" "## 6." '층 높이 × 흐름' '솟은' '홈' 'top_surface_acceleration' 'zig-zag' 'rectilinear' 'Fill.cpp'
chk AR-05a "$( [ "$(grep -cF '기본값이 `1` 이므로' "$R/seam-recipes.md")" = 0 ] && echo 1)"
toks AR-05b "$R/seam-recipes.md" "### 6.5.4" "### 6.5.5" 'true' 'false' 'PrintConfig.cpp'
toks AR-06 "$R/seam-recipes.md" "## 6.6" "## 7." '485' '466' '580' 'aligned_back' 'back'
chk AR-07 "$( f=.harness/.meta/evidence/bambu-orca-h2s-feedback.md; [ -f "$f" ] && for t in 50bb6ab _shrink_contour_holes Brim.cpp Fill.cpp 0.21; do grep -qF "$t" "$f" || exit; done && echo 1)"
chk AR-08 "$( h=docs/bambu-kit/bambu-print-profile.html; [ "$(grep -cF '시험용 파일 4 종' "$h")" = 0 ] && [ "$(grep -cF '카메라 준비' "$h")" -ge 1 ] && echo 1)"
echo "orig_ok=$ok/$all"
[ "$ok" = "$all" ]
