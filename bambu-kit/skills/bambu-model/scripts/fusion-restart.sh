# fusion-job.sh · fusion-fillet/fillet-job.sh 가 source 해서 쓰는 퓨전 끄기 · 켜기 (직접 실행하지 않는다)
# 끌 때 TERM 을 보내지 않는다. 퓨전은 TERM 을 충돌로 받아 충돌 보고 장치가 기록하다가 자기 잠금을 다시 잡아 죽고,
# 그동안 1~2 분 프로세스가 남는다 (2026-11-09 실측 — 껐다 켤 때마다 충돌 보고 하나, `Trying to recursively lock an os_unfair_lock`).
# 그래서 정상 종료 요청(Apple 이벤트 quit)을 보내고, 퓨전과 충돌 보고 장치가 모두 사라질 때까지 기다린다.
# 꺼지는 중에 다시 켜면 macOS 가 `Operation already in progress` 로 거부하므로 켜기는 몇 번 다시 시도한다.
# 환경 변수: BAMBU_FUSION_QUIT_WAIT(종료 요청 뒤 기다림, 기본 90 초) · BAMBU_FUSION_OPEN_TRIES(켜기 시도 수, 기본 6) · BAMBU_FUSION_OPEN_GAP(시도 간격, 기본 5 초)
# shellcheck shell=bash

fusion_process='MacOS/Autodesk Fusion'
fusion_bundle='com.autodesk.fusion360'

fusion_running() {
  pgrep -f "$fusion_process" >/dev/null
}

fusion_stop() {  # 0 꺼짐(또는 원래 안 켜짐) · 1 정상 종료 요청 뒤에도 남음
  fusion_running || return 0
  osascript -e "quit app id \"$fusion_bundle\"" >/dev/null 2>&1
  local waited=0 limit=${BAMBU_FUSION_QUIT_WAIT:-90}
  while fusion_running && [ "$waited" -lt "$limit" ]; do sleep 1; waited=$((waited + 1)); done
  fusion_running && return 1
  waited=0
  while pgrep -f 'cer_dialog|cer_service' >/dev/null && [ "$waited" -lt "$limit" ]; do sleep 1; waited=$((waited + 1)); done
  return 0
}

fusion_clear_stale() {  # 죽은 퓨전의 실행 기록이 launchd 에 남으면 모든 실행이 `Operation already in progress` 로 거부된다
  # (2026-11-09 실측 — 충돌로 -9 종료한 기록이 15 분 넘게 남았다). 퓨전 프로세스가 없을 때만, pid 칸이 「-」인 기록을 지운다
  fusion_running && return 0
  launchctl list 2>/dev/null | awk -v b="application.$fusion_bundle." '$1 == "-" && index($3, b) == 1 {print $3}' \
    | while IFS= read -r job; do launchctl remove "$job"; done
}

fusion_start() {  # fusion_start <앱 경로> — 0 켜짐 · 1 끝내 못 켬
  local try tries=${BAMBU_FUSION_OPEN_TRIES:-6} gap=${BAMBU_FUSION_OPEN_GAP:-5}
  for try in $(seq 1 "$tries"); do
    open "$1" && return 0
    fusion_clear_stale
    [ "$try" -lt "$tries" ] && sleep "$gap"
  done
  return 1
}

fusion_restart() {  # fusion_restart <앱 경로> — 실패하면 안내를 찍고 종료 코드 4 · 5 로 끝낸다
  if ! fusion_stop; then
    echo "퓨전이 꺼지지 않는다 — 종료 요청에도 남았다. 저장 확인 창 같은 창이 떠 있는지 보고 퓨전을 직접 끈 뒤 다시 돌린다" >&2
    exit 4
  fi
  if ! fusion_start "$1"; then
    echo "퓨전을 켜지 못했다 — ${BAMBU_FUSION_OPEN_TRIES:-6} 번 시도. 퓨전이 아직 꺼지는 중인지 보고 잠시 뒤 다시 돌린다: $1" >&2
    exit 5
  fi
}
