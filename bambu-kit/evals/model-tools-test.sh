#!/usr/bin/env bash
# bambu-model 스크립트(ensure-cadquery.sh · render.py · fusion-job.sh)가 약속한 대로 도는지 본다
# 퓨전 명령(open · pkill · pgrep)과 python3 는 임시 폴더의 가짜로 바꿔 진짜 퓨전 · 진짜 파이썬 설치를 건드리지 않는다
# --fusion 을 주면 진짜 퓨전을 한 번 껐다 켜서 옷걸이 원본을 32 mm 로 다시 뽑는다 (계약 bambu-kit-modeling-tools 스크립트-03)
# 마감 시험(fillet-*)은 fusion-fillet/fillet-job.sh 를 자기 가짜 명령으로 잰다. --fusion 이면 fillet-real 이 진짜 퓨전으로 정육면체를 둥글린다
# 종료 코드: 0 통과 · 1 실패 · 2 준비 실패
set -uo pipefail

here=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
scripts=$(cd "$here/../skills/bambu-model/scripts" && pwd) || { echo "스크립트 폴더가 없다" >&2; exit 2; }
real_python=$(command -v python3) || { echo "python3 가 없다" >&2; exit 2; }
work=$(mktemp -d "${TMPDIR:-/tmp}/model-tools.XXXXXX") || exit 2
trap 'rm -rf "$work"' EXIT
fails=0

check() {  # check <이름> <맞으면 1> <설명>
  if [ "$2" = 1 ]; then echo "PASS $1"; else echo "FAIL $1 — $3"; fails=$((fails + 1)); fi
}

fake_bin() {  # fake_bin <폴더> <이름> <본문>
  mkdir -p "$1"
  printf '#!/usr/bin/env bash\n%s\n' "$3" > "$1/$2"
  chmod +x "$1/$2"
}

# python3 가 실제로 쓰는 쪽(-m pip 가 아닌 호출)은 진짜로 넘기고 pip 호출만 기록한다
watch="$work/watch"
fake_bin "$watch" python3 "if [ \"\${1:-}\" = -m ] && [ \"\${2:-}\" = pip ]; then echo \"\$*\" >> '$work/pip-present.log'; exit 0; fi
exec '$real_python' \"\$@\""
PATH="$watch:$PATH" bash "$scripts/ensure-cadquery.sh" > "$work/present.out" 2>&1
code=$?
check ensure-present "$([ "$code" = 0 ] && [ ! -s "$work/pip-present.log" ] && grep -q '^있음' "$work/present.out" && echo 1)" \
  "종료 $code, pip 기록 $(cat "$work/pip-present.log" 2>/dev/null | wc -l | tr -d ' ') 줄"

broken="$work/broken"
fake_bin "$broken" python3 "if [ \"\${1:-}\" = -m ] && [ \"\${2:-}\" = pip ]; then echo \"\$*\" >> '$work/pip-missing.log'; exit 0; fi
exit 1"
PATH="$broken:$PATH" bash "$scripts/ensure-cadquery.sh" > "$work/missing.out" 2>&1
code=$?
calls=$(grep -c 'install' "$work/pip-missing.log" 2>/dev/null || echo 0)
check ensure-missing "$([ "$code" != 0 ] && [ "$calls" = 1 ] && echo 1)" "종료 $code, pip 설치 호출 $calls 번"

# import 확인을 지운 사본은 있을 때도 pip 를 불러야 한다 — 위 ensure-present 가 그 차이를 잡는지 본다
sed -n '1,/^echo "없음/p' "$scripts/ensure-cadquery.sh" | grep -q '^if can_import; then$' || { echo "음성 대조 사본을 못 만든다 — 확인 줄 모양이 바뀌었다" >&2; exit 2; }
awk 'BEGIN{skip=0} /^if can_import; then$/ && !done {skip=1} skip && /^fi$/ {skip=0; done=1; next} !skip' "$scripts/ensure-cadquery.sh" > "$work/ensure-nocheck.sh"
rm -f "$work/pip-present.log"
PATH="$watch:$PATH" bash "$work/ensure-nocheck.sh" > /dev/null 2>&1
check ensure-negative-control "$([ -s "$work/pip-present.log" ] && echo 1)" "확인 줄을 지워도 pip 호출이 없다 — ensure-present 가 확인 줄을 못 잰다"

(cd "$work" && "$real_python" -c "import cadquery as cq; cq.exporters.export(cq.Workplane().box(10, 10, 10), 'cube.stl')") \
  || { echo "정육면체 STL 을 못 만든다" >&2; exit 2; }
"$real_python" "$scripts/render.py" "$work/cube.stl" "$work/cube.png" 20 -60 > /dev/null 2>&1
code=$?
picture=$("$real_python" - "$work/cube.png" <<'PY' 2>/dev/null
import sys
import matplotlib.image as image
import numpy as np
with open(sys.argv[1], "rb") as png_file:
    signature = png_file.read(8) == b"\x89PNG\r\n\x1a\n"
pixels = image.imread(sys.argv[1])
colors = len(np.unique(pixels.reshape(-1, pixels.shape[2]), axis=0))
print(1 if signature and pixels.shape[0] >= 200 and pixels.shape[1] >= 200 and colors >= 2 else 0)
PY
)
check render-cube "$([ "$code" = 0 ] && [ "$picture" = 1 ] && echo 1)" "종료 $code, 그림 검사 ${picture:-읽기 실패}"

"$real_python" "$scripts/render.py" "$work/nope.stl" "$work/nope.png" > /dev/null 2>&1
code=$?
check render-missing "$([ "$code" != 0 ] && echo 1)" "없는 STL 인데 종료 $code"

fusion_fakes="$work/fusion-bin"
for tool in open pkill pgrep; do
  fake_bin "$fusion_fakes" "$tool" "echo $tool \"\$*\" >> '$work/fusion-calls.log'; exit 1"
done
printf '{"source": "%s/없는-원본.f3d", "out_dir": "%s/out-missing"}\n' "$work" "$work" > "$work/job-missing.json"
PATH="$fusion_fakes:$PATH" BAMBU_FUSION_ADDINS="$work/addins" bash "$scripts/fusion-job.sh" "$work/job-missing.json" > /dev/null 2> "$work/missing-source.err"
code=$?
check fusion-missing-source "$([ "$code" != 0 ] && [ ! -s "$work/fusion-calls.log" ] && grep -qF "$work/없는-원본.f3d" "$work/missing-source.err" && echo 1)" \
  "종료 $code, 퓨전 명령 기록 $(cat "$work/fusion-calls.log" 2>/dev/null | wc -l | tr -d ' ') 줄"

: > "$work/fake.f3d"
printf '{"source": "%s/fake.f3d", "out_dir": "%s/out-timeout"}\n' "$work" "$work" > "$work/job-timeout.json"
started=$SECONDS
PATH="$fusion_fakes:$PATH" BAMBU_FUSION_ADDINS="$work/addins" BAMBU_FUSION_TIMEOUT=3 \
  bash "$scripts/fusion-job.sh" "$work/job-timeout.json" > "$work/timeout.out" 2>&1
code=$?
elapsed=$((SECONDS - started))
check fusion-timeout "$([ "$code" != 0 ] && [ "$elapsed" -le 10 ] && grep -q '시간 초과' "$work/timeout.out" && [ ! -e "$work/addins/BambuKitFusionJob" ] && echo 1)" \
  "종료 $code, ${elapsed} 초, 추가 기능 남음=$([ -e "$work/addins/BambuKitFusionJob" ] && echo 예 || echo 아니오)"

# 마감(fillet-job.sh) 시험 — 위 퓨전 시험과 섞이지 않게 자기 가짜 명령 폴더 · 기록 · AddIns 를 쓴다
fillet="$scripts/fusion-fillet"
fillet_fakes="$work/fillet-bin"
fillet_addins="$work/fillet-addins"
fillet_installed="$fillet_addins/BambuKitFusionFillet"
for tool in pkill pgrep; do
  fake_bin "$fillet_fakes" "$tool" "echo $tool \"\$*\" >> '$work/fillet-calls.log'; exit 1"
done
# 가짜 open: 불린 순간 추가 기능 세 파일이 깔려 있는지 적고, 퓨전 대신 끝 표시를 남긴다
fake_bin "$fillet_fakes" open "echo open \"\$*\" >> '$work/fillet-calls.log'
for f in BambuKitFusionFillet.py BambuKitFusionFillet.manifest job-path.txt; do [ -f '$fillet_installed'/\$f ] && echo \"있음 \$f\" >> '$work/fillet-installed.log'; done
echo '00:00:00 DONE' >> '$work/out-fillet/fillet-job.log'"
: > "$work/part.step"
printf '{"out_dir": "%s/out-fillet", "parts": [{"name": "part", "step": "%s/part.step"}]}\n' "$work" "$work" > "$work/job-fillet.json"
PATH="$fillet_fakes:$PATH" BAMBU_FUSION_ADDINS="$fillet_addins" BAMBU_FUSION_TIMEOUT=3 \
  bash "$fillet/fillet-job.sh" "$work/job-fillet.json" > "$work/fillet-installs.out" 2>&1
code=$?
seen=$(grep -c '^있음 ' "$work/fillet-installed.log" 2>/dev/null || echo 0)
check fillet-installs "$([ "$code" = 0 ] && [ "$seen" = 3 ] && [ ! -e "$fillet_installed" ] && echo 1)" \
  "종료 $code, open 때 깔린 파일 $seen/3, 끝난 뒤 남음=$([ -e "$fillet_installed" ] && echo 예 || echo 아니오)"

rm -f "$work/fillet-calls.log"
printf '{"out_dir": "%s/out-fillet-missing", "parts": [{"name": "nope", "step": "%s/없는-부품.step"}]}\n' "$work" "$work" > "$work/job-fillet-missing.json"
PATH="$fillet_fakes:$PATH" BAMBU_FUSION_ADDINS="$fillet_addins" BAMBU_FUSION_TIMEOUT=3 bash "$fillet/fillet-job.sh" "$work/job-fillet-missing.json" > /dev/null 2> "$work/fillet-missing.err"
code=$?
check fillet-missing-step "$([ "$code" != 0 ] && [ ! -s "$work/fillet-calls.log" ] && grep -qF "$work/없는-부품.step" "$work/fillet-missing.err" && echo 1)" \
  "종료 $code, 가짜 명령 기록 $(cat "$work/fillet-calls.log" 2>/dev/null | wc -l | tr -d ' ') 줄"

# 시간 초과: open 이 끝 표시를 안 남기는 가짜 폴더
fillet_silent="$work/fillet-silent-bin"
for tool in open pkill pgrep; do
  fake_bin "$fillet_silent" "$tool" "exit 1"
done
printf '{"out_dir": "%s/out-fillet-timeout", "parts": [{"name": "part", "step": "%s/part.step"}]}\n' "$work" "$work" > "$work/job-fillet-timeout.json"
started=$SECONDS
PATH="$fillet_silent:$PATH" BAMBU_FUSION_ADDINS="$fillet_addins" BAMBU_FUSION_TIMEOUT=3 \
  bash "$fillet/fillet-job.sh" "$work/job-fillet-timeout.json" > "$work/fillet-timeout.out" 2>&1
code=$?
elapsed=$((SECONDS - started))
check fillet-timeout "$([ "$code" != 0 ] && [ "$elapsed" -le 10 ] && grep -q '시간 초과' "$work/fillet-timeout.out" && [ ! -e "$fillet_installed" ] && echo 1)" \
  "종료 $code, ${elapsed} 초, 추가 기능 남음=$([ -e "$fillet_installed" ] && echo 예 || echo 아니오)"

# 걷어 내는 trap 줄을 뺀 사본은 같은 상황에서 추가 기능을 남겨야 한다 — 위 fillet-timeout 이 trap 을 재는지 본다
nc="$work/fillet-nc"
mkdir -p "$nc"
cp -R "$fillet/addin" "$nc/addin"
grep -q "^trap 'rm -rf \"\$installed\"' EXIT$" "$fillet/fillet-job.sh" || { echo "음성 대조 사본을 못 만든다 — trap 줄 모양이 바뀌었다" >&2; exit 2; }
grep -v "^trap 'rm -rf \"\$installed\"' EXIT$" "$fillet/fillet-job.sh" > "$nc/fillet-job.sh"
PATH="$fillet_silent:$PATH" BAMBU_FUSION_ADDINS="$fillet_addins" BAMBU_FUSION_TIMEOUT=3 \
  bash "$nc/fillet-job.sh" "$work/job-fillet-timeout.json" > /dev/null 2>&1
check fillet-negative-control "$([ -e "$fillet_installed" ] && echo 1)" "trap 을 빼도 추가 기능이 안 남는다 — fillet-timeout 이 걷어 내기를 못 잰다"
rm -rf "$fillet_installed"

if [ "${1:-}" = --fusion ]; then
  base="$HOME/Hub/60_3D Print/Settings/modular-coat-hanger"
  addins="$HOME/Library/Application Support/Autodesk/Autodesk Fusion 360/API/AddIns"
  printf '{"source": "%s", "out_dir": "%s", "params": {"dowel_size": "32 mm"}}\n' \
    "$base/source/MasterCoatHanger2.f3d" "$work/out-real" > "$work/job-real.json"
  bash "$scripts/fusion-job.sh" "$work/job-real.json"
  code=$?
  stl_count=$(find "$work/out-real" -maxdepth 1 -name '*.stl' 2>/dev/null | wc -l | tr -d ' ')
  holes=$(grep -cE '^HOLE d=3[23]\.' "$work/out-real/report.txt" 2>/dev/null || echo 0)
  same=$("$real_python" - "$work/out-real/LegsForCoatHanger_v7_1__Body8.stl" "$base/stl-32mm/LegsForCoatHanger_v7_1__Body8.stl" <<'PY' 2>/dev/null
import sys
from stl import mesh
new, old = (mesh.Mesh.from_file(path) for path in sys.argv[1:3])
gaps = abs((new.max_ - new.min_) - (old.max_ - old.min_))
print(1 if (gaps <= 0.1).all() else 0, " ".join(f"{gap:.3f}" for gap in gaps))
PY
)
  left=$([ -e "$addins/BambuKitFusionJob" ] && echo 1 || echo 0)
  check fusion-real "$([ "$code" = 0 ] && [ "$stl_count" -ge 1 ] && [ "$holes" -ge 1 ] && [ "${same%% *}" = 1 ] && [ "$left" = 0 ] && echo 1)" \
    "종료 $code, STL $stl_count 개, 막대 구멍 $holes 줄, 다리 받침 차이 ${same:-비교 실패}, 추가 기능 남음 $left"

  # 마감: 20 mm 정육면체 STEP 을 퓨전이 둥글리면 삼각형이 12 개보다 많고 부피가 8000 mm³ 보다 작다
  (cd "$work" && "$real_python" -c "import cadquery as cq; cq.exporters.export(cq.Workplane().box(20, 20, 20), 'cube20.step')") \
    || { echo "정육면체 STEP 을 못 만든다" >&2; exit 2; }
  printf '{"out_dir": "%s/out-fillet-real", "parts": [{"name": "cube20", "step": "%s/cube20.step", "radii": [3, 2, 1]}]}\n' "$work" "$work" > "$work/job-fillet-real.json"
  bash "$fillet/fillet-job.sh" "$work/job-fillet-real.json"
  code=$?
  out="$work/out-fillet-real"
  mesh_check=$("$real_python" - "$out/cube20.stl" <<'PY' 2>/dev/null
import sys
from stl import mesh
part = mesh.Mesh.from_file(sys.argv[1])
volume = abs(part.get_mass_properties()[0])
print(1 if len(part.vectors) > 12 and 0 < volume < 8000 else 0, len(part.vectors), f"{volume:.0f}")
PY
)
  pictures=0
  for view in iso front side top; do [ -s "$out/cube20_$view.png" ] && pictures=$((pictures + 1)); done
  part_line=$(grep -cE 'PART cube20 fillet=[0-9]' "$out/fillet-job.log" 2>/dev/null || echo 0)
  left=$([ -e "$addins/BambuKitFusionFillet" ] && echo 1 || echo 0)
  check fillet-real "$([ "$code" = 0 ] && [ "${mesh_check%% *}" = 1 ] && [ "$pictures" = 4 ] && [ "$part_line" -ge 1 ] && [ "$left" = 0 ] && echo 1)" \
    "종료 $code, 삼각형 · 부피 ${mesh_check:-읽기 실패}, 그림 $pictures/4, PART 줄 $part_line, 추가 기능 남음 $left"
fi

[ "$fails" = 0 ]
