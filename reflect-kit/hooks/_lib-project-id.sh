#!/usr/bin/env bash
# reflect-kit: 프로젝트 ID 계산 (v0.3.0 Hybrid)
#
# 기본 출력: <basename>
# 충돌 감지 시: <basename>-<6자 hash> + stderr 1회 경고
#
# "충돌" 정의 — 동일 basename 디렉토리의 .project-root 마커가
# 현재 git root 와 다른 경로를 가리킬 때. 마커는 compute 시점에
# 자동 ensure (basename 반환 경로). read 와 write 경로 모두 안전.
#
# 기존 <basename>-<hash> 디렉토리는 그대로 read 지원 (reflect-digest
# 의 glob union 으로 커버).
#
# 사용법:
#   source 후 project_id=$(compute_project_id "$cwd")
#   또는 query=$(normalize_project_query "<basename>")

LOGS_ROOT_DEFAULT="$HOME/.claude/logs"

_rk_hash6() {
  local input="$1"
  local h
  if command -v md5 >/dev/null 2>&1; then
    h=$(printf '%s' "$input" | md5 2>/dev/null)
  elif command -v md5sum >/dev/null 2>&1; then
    h=$(printf '%s' "$input" | md5sum 2>/dev/null | awk '{print $1}')
  else
    h=$(printf '%s' "$input" | cksum 2>/dev/null | awk '{print $1}')
  fi
  h=${h:0:6}
  [ -z "$h" ] && h="noid00"
  printf '%s' "$h"
}

# 내부 디렉토리 필터: "_", "." prefix 디렉토리는 project bucket 이 아님
# (예: _cron — install-scheduler.sh 가 만든 로그 디렉토리)
is_internal_logs_dir() {
  local name="$1"
  case "$name" in
    .*) return 0 ;;
    _*) return 0 ;;
    *) return 1 ;;
  esac
}

# 단일 프로세스 내에서 동일 basename 충돌 경고를 1회만 출력
# 마커 파일: ${TMPDIR:-/tmp}/.reflect-kit-warn-<basename>-<PID>
_rk_warn_once() {
  local basename="$1"
  local msg="$2"
  local marker="${TMPDIR:-/tmp}/.reflect-kit-warn-${basename}-$$"
  [ -e "$marker" ] && return 0
  : > "$marker" 2>/dev/null
  printf '%s\n' "$msg" >&2
}

compute_project_id() {
  local cwd="$1"
  [ -z "$cwd" ] && cwd="$PWD"

  local repo_root
  repo_root=$(git -C "$cwd" rev-parse --show-toplevel 2>/dev/null)
  [ -z "$repo_root" ] && repo_root="$cwd"

  local base
  base=$(basename "$repo_root")

  local logs_root="${REFLECT_KIT_LOGS_ROOT:-$LOGS_ROOT_DEFAULT}"
  local base_dir="$logs_root/$base"
  local marker="$base_dir/.project-root"

  # 충돌 감지: 기존 basename 디렉토리의 마커가 다른 git root 를 가리킴
  if [ -d "$base_dir" ] && [ -f "$marker" ]; then
    local stored
    stored=$(cat "$marker" 2>/dev/null)
    if [ -n "$stored" ] && [ "$stored" != "$repo_root" ]; then
      local h
      h=$(_rk_hash6 "$repo_root")
      _rk_warn_once "$base" \
        "[reflect-kit] basename collision for '$base' — using '${base}-${h}'. existing: $stored, current: $repo_root"
      printf '%s-%s' "$base" "$h"
      return 0
    fi
  fi

  # 충돌 없음 — basename bucket ensure + 마커 ensure
  # (read 경로에서도 자기 repo 의 bucket 만 생성하므로 안전)
  mkdir -p "$base_dir" 2>/dev/null
  [ ! -f "$marker" ] && printf '%s\n' "$repo_root" > "$marker" 2>/dev/null

  printf '%s' "$base"
}

# digest 용: project 쿼리를 glob pattern union 으로 확장
# 입력이 어느 쪽이든 같은 basename 의 "basename + basename-<hash6>" union 을 반환
# 하여 backward-compat 을 보장한다 (SK-01 동등성 계약).
#
#   basename        → "<basename> <basename>-[0-9a-f]{6}"
#   basename-<hash> → basename 추출 → "<basename> <basename>-[0-9a-f]{6}"
normalize_project_query() {
  local query="$1"
  local base
  case "$query" in
    *-[0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f])
      base="${query%-??????}"
      ;;
    *)
      base="$query"
      ;;
  esac
  printf '%s %s-[0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f]' "$base" "$base"
}

# 에러 메타로깅: .errors.log 에 타임스탬프 + 이유 append
log_hook_error() {
  local log_dir="$1"
  local hook_name="$2"
  local reason="$3"
  [ -z "$log_dir" ] && return 0
  [ ! -d "$log_dir" ] && return 0
  local ts
  ts=$(date '+%Y-%m-%dT%H:%M:%S%z')
  printf '%s [%s] %s\n' "$ts" "$hook_name" "$reason" >> "$log_dir/.errors.log" 2>/dev/null
}
