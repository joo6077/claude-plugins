#!/usr/bin/env bash
# 공통 헬퍼: 안정적인 프로젝트 ID 계산
# 사용법: source 후 `project_id=$(compute_project_id "$cwd")`
# 출력: <basename>-<6자 hash>  (예: fit-pal-a3b4f9)
# hash 재료: git root 절대경로 (git 아니면 cwd 절대경로)

compute_project_id() {
  local cwd="$1"
  [ -z "$cwd" ] && cwd="$PWD"

  local repo_root
  repo_root=$(git -C "$cwd" rev-parse --show-toplevel 2>/dev/null)
  [ -z "$repo_root" ] && repo_root="$cwd"

  local hash_input="$repo_root"
  local id_hash
  if command -v md5 >/dev/null 2>&1; then
    id_hash=$(printf '%s' "$hash_input" | md5 2>/dev/null)
  elif command -v md5sum >/dev/null 2>&1; then
    id_hash=$(printf '%s' "$hash_input" | md5sum 2>/dev/null | awk '{print $1}')
  else
    id_hash=$(printf '%s' "$hash_input" | cksum 2>/dev/null | awk '{print $1}')
  fi
  id_hash=${id_hash:0:6}
  [ -z "$id_hash" ] && id_hash="noid00"

  printf '%s-%s' "$(basename "$repo_root")" "$id_hash"
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
