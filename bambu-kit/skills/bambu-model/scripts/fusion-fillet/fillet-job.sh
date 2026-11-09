#!/usr/bin/env bash
# 작업 파일(JSON)대로 퓨전 360 이 STEP 을 열어 모서리를 둥글리고 STL · 그림을 내게 한다 (f3d 용 ../fusion-job.sh 와 같은 흐름)
# usage: fillet-job.sh <job.json>
#   job.json: {"out_dir": "<출력 폴더>", "parts": [{"name": "<이름>", "step": "<STEP 절대 경로>", "radii": [3, 2, 1.5]}]}
#   붙는 부품: "step" 대신 "join": ["<바탕 STEP>", "<붙일 STEP>"] 와 선택 "seam_radii" — 붙일 것만 둥글리고 합친 뒤 이음매만 둥글린다
# 퓨전은 명령줄로 부를 수 없어서, 켜질 때 저절로 도는 추가 기능을 깔고 퓨전을 다시 켠 뒤 끝 표시를 기다린다.
# 추가 기능은 성공 · 실패 · 시간 초과 어느 길로 끝나도 걷어 낸다 — 남기면 퓨전을 켤 때마다 다시 돈다.
# 환경 변수: BAMBU_FUSION_TIMEOUT(기본 600 초) · BAMBU_FUSION_ADDINS(AddIns 폴더) · BAMBU_FUSION_APP(퓨전 앱 경로) · fusion-restart.sh 의 BAMBU_FUSION_QUIT_WAIT · BAMBU_FUSION_OPEN_TRIES · BAMBU_FUSION_OPEN_GAP
# 끄기 · 켜기는 fusion-restart.sh 가 한다 — TERM 대신 정상 종료 요청, 켜기 실패는 다시 시도
# 종료 코드: 0 DONE · 1 추가 기능이 FAIL · 2 작업 파일 오류 · 3 시간 초과 · 4 퓨전이 안 꺼짐 · 5 퓨전을 못 켬
set -uo pipefail

job=${1:-}
[ -n "$job" ] && [ -f "$job" ] || { echo "작업 파일이 없다: ${job:-<인자 없음>}" >&2; exit 2; }
job=$(cd "$(dirname "$job")" && pwd)/$(basename "$job")

# 첫 줄 out_dir, 다음 줄부터 없는 STEP 경로 (parts 가 비면 <parts 비어 있음>) — 퓨전을 건드리기 전에 전부 확인한다
fields=$(python3 - "$job" <<'PY'
import json, os, sys
job = json.load(open(sys.argv[1], encoding="utf-8"))
print(job.get("out_dir", ""))
parts = job.get("parts") or []
if not parts:
    print("<parts 비어 있음>")
for part in parts:
    paths = part.get("join") or [part.get("step", "")]
    if "join" in part and len(paths) < 2:
        print(f"<{part.get('name', '?')}: join 은 STEP 이 둘 이상이어야 한다>")
    for path in paths:
        if not path or not os.path.isfile(path):
            print(path or f"<{part.get('name', '?')}: STEP 경로 없음>")
PY
) || { echo "작업 파일을 JSON 으로 읽지 못했다: $job" >&2; exit 2; }
out_dir=$(printf '%s\n' "$fields" | sed -n 1p)
missing=$(printf '%s\n' "$fields" | sed -n '2,$p')
[ -z "$missing" ] || { echo "STEP 이 없다:" >&2; printf '%s\n' "$missing" >&2; exit 2; }
[ -n "$out_dir" ] || { echo "out_dir 이 비어 있다: $job" >&2; exit 2; }

here=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
addins=${BAMBU_FUSION_ADDINS:-$HOME/Library/Application Support/Autodesk/Autodesk Fusion 360/API/AddIns}
app=${BAMBU_FUSION_APP:-$HOME/Library/Application Support/Autodesk/webdeploy/production/Autodesk Fusion.app}
limit=${BAMBU_FUSION_TIMEOUT:-600}
installed="$addins/BambuKitFusionFillet"
log="$out_dir/fillet-job.log"

mkdir -p "$out_dir" "$addins"
rm -f "$log"
trap 'rm -rf "$installed"' EXIT
rm -rf "$installed"
cp -R "$here/addin" "$installed"
printf '%s\n' "$job" > "$installed/job-path.txt"

# shellcheck source=/dev/null
source "$here/../fusion-restart.sh"
fusion_restart "$app"
echo "퓨전을 다시 켰다 — 끝 표시를 최대 ${limit} 초 기다린다 ($log)"

started=$SECONDS
while [ $((SECONDS - started)) -lt "$limit" ]; do
  if grep -q '^[0-9:]* DONE' "$log" 2>/dev/null; then
    echo "DONE — $(grep -c '^[0-9:]* PART' "$log") 개 부품"; grep '^[0-9:]* PART' "$log"
    exit 0
  fi
  if grep -q '^[0-9:]* FAIL' "$log" 2>/dev/null; then
    echo "추가 기능이 실패했다:" >&2
    cat "$log" >&2
    exit 1
  fi
  sleep 2
done
echo "시간 초과 — ${limit} 초 안에 끝 표시가 없다. 퓨전이 로그인 창에서 멈췄는지 본다" >&2
exit 3
