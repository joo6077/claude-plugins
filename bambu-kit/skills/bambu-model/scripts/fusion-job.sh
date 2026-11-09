#!/usr/bin/env bash
# 작업 파일(JSON)대로 퓨전 360 이 f3d 를 열어 매개변수를 바꾸고 STL · report.txt 를 내게 한다
# usage: fusion-job.sh <job.json>
#   job.json: {"source": "<f3d 절대 경로>", "out_dir": "<출력 폴더>", "params": {"<이름>": "<식>"}, "holes_under_mm": 40}
# 퓨전은 명령줄로 부를 수 없어서, 켜질 때 저절로 도는 추가 기능을 깔고 퓨전을 다시 켠 뒤 끝 표시를 기다린다.
# 추가 기능은 성공 · 실패 · 시간 초과 어느 길로 끝나도 걷어 낸다 — 남기면 퓨전을 켤 때마다 다시 돈다.
# 환경 변수: BAMBU_FUSION_TIMEOUT(기본 600 초) · BAMBU_FUSION_ADDINS(AddIns 폴더) · BAMBU_FUSION_APP(퓨전 앱 경로) · fusion-restart.sh 의 BAMBU_FUSION_QUIT_WAIT · BAMBU_FUSION_OPEN_TRIES · BAMBU_FUSION_OPEN_GAP
# 끄기 · 켜기는 fusion-restart.sh 가 한다 — TERM 대신 정상 종료 요청, 켜기 실패는 다시 시도
# 종료 코드: 0 DONE · 1 추가 기능이 FAIL · 2 작업 파일 오류 · 3 시간 초과 · 4 퓨전이 안 꺼짐 · 5 퓨전을 못 켬
set -uo pipefail

job=${1:-}
[ -n "$job" ] && [ -f "$job" ] || { echo "작업 파일이 없다: ${job:-<인자 없음>}" >&2; exit 2; }
job=$(cd "$(dirname "$job")" && pwd)/$(basename "$job")

fields=$(python3 - "$job" <<'PY'
import json, sys
job = json.load(open(sys.argv[1], encoding="utf-8"))
print(job.get("source", ""))
print(job.get("out_dir", ""))
PY
) || { echo "작업 파일을 JSON 으로 읽지 못했다: $job" >&2; exit 2; }
source_path=$(printf '%s\n' "$fields" | sed -n 1p)
out_dir=$(printf '%s\n' "$fields" | sed -n 2p)
[ -f "$source_path" ] || { echo "원본 f3d 가 없다: ${source_path:-<source 비어 있음>}" >&2; exit 2; }
[ -n "$out_dir" ] || { echo "out_dir 이 비어 있다: $job" >&2; exit 2; }

here=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
addins=${BAMBU_FUSION_ADDINS:-$HOME/Library/Application Support/Autodesk/Autodesk Fusion 360/API/AddIns}
app=${BAMBU_FUSION_APP:-$HOME/Library/Application Support/Autodesk/webdeploy/production/Autodesk Fusion.app}
limit=${BAMBU_FUSION_TIMEOUT:-600}
installed="$addins/BambuKitFusionJob"
log="$out_dir/fusion-job.log"

mkdir -p "$out_dir" "$addins"
rm -f "$log"
trap 'rm -rf "$installed"' EXIT
rm -rf "$installed"
cp -R "$here/fusion-addin" "$installed"
printf '%s\n' "$job" > "$installed/job-path.txt"

# shellcheck source=/dev/null
source "$here/fusion-restart.sh"
fusion_restart "$app"
echo "퓨전을 다시 켰다 — 끝 표시를 최대 ${limit} 초 기다린다 ($log)"

started=$SECONDS
while [ $((SECONDS - started)) -lt "$limit" ]; do
  if grep -q '^[0-9:]* DONE' "$log" 2>/dev/null; then
    echo "DONE — $(find "$out_dir" -maxdepth 1 -name '*.stl' | wc -l | tr -d ' ') 개 STL, 보고: $out_dir/report.txt"
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
