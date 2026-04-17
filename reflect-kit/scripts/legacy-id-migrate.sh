#!/usr/bin/env bash
# reflect-kit: 레거시 basename-only project_id → basename-<hash6> 형식 마이그레이션.
#
# 초기 버전은 project_id 가 git root 의 basename 뿐이었고,
# 이후 basename 충돌 방지를 위해 <basename>-<6자 md5 hex> 로 변경됨.
# 기존 로그(해시 없는 디렉토리)를 새 포맷으로 이동 + 신규 디렉토리와 충돌 시 concat merge.
#
# 사용법:
#   --scan      해시 없는 레거시 디렉토리 리스트 + basename 별 후보 git repo 경로 검색
#   --dry-run   rename/merge 계획만 stdout 출력 (실제 파일 변경 없음)
#   --execute   실제 rename + concat merge 실행 (파일명 오름차순: 레거시 → 신규 순 concat)
#   --help      사용법
#
# 동작 원칙:
#   - concat merge 순서: 레거시(과거 멈춘 로그) 먼저 → 신규(현재 쌓이는 로그) 뒤
#     따라서 파일 내부 타임스탬프 헤더는 오름차순 (최신 엔트리가 파일 말미에 위치).
#   - basename 기반 후보 repo 탐색: ~/Hub, ~/Projects, ~/Development, ~/Documents,
#     ~/Workspace, ~/dev, ~/src 중 존재하는 루트에서 maxdepth 4 search.
#   - 자동 매핑 실패 시 SKIP — 사용자 수동 처리 여지.

set +e

LOGS_DIR="$HOME/.claude/logs"
HASH_PATTERN='-[0-9a-f]{6}$'

# 사용자 홈 아래 흔히 쓰는 코드 루트 (필요 시 수정)
SEARCH_ROOTS=(
  "$HOME/Hub"
  "$HOME/Projects"
  "$HOME/Development"
  "$HOME/Documents"
  "$HOME/Workspace"
  "$HOME/dev"
  "$HOME/src"
)

# project_id 계산 헬퍼 로드
source_project_id_lib() {
  local lib
  lib="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/../hooks/_lib-project-id.sh"
  if [ -f "$lib" ]; then
    # shellcheck disable=SC1090
    source "$lib"
  else
    echo "ERROR: _lib-project-id.sh 찾을 수 없음 — $lib" >&2
    exit 2
  fi
}

# basename이 주어지면 SEARCH_ROOTS에서 git repo 후보 경로 검색
find_candidate_repos() {
  local name="$1"
  for root in "${SEARCH_ROOTS[@]}"; do
    [ -d "$root" ] || continue
    find "$root" -maxdepth 4 -type d -name "$name" 2>/dev/null | while read -r dir; do
      if [ -d "$dir/.git" ]; then
        printf '%s\n' "$dir"
      fi
    done
  done
}

print_help() {
  sed -n '2,24p' "$0"
}

# --scan: 레거시 디렉토리 + 후보 경로 목록
scan_legacy() {
  source_project_id_lib
  echo "== 레거시 project_id 디렉토리 스캔 =="
  echo "   (해시 없는 basename-only 디렉토리)"
  echo ""
  local found=0
  for d in "$LOGS_DIR"/*/; do
    [ -d "$d" ] || continue
    local pid
    pid=$(basename "$d")
    if [[ ! "$pid" =~ $HASH_PATTERN ]]; then
      found=$((found + 1))
      echo "[$pid] (레거시)"
      local candidates
      candidates=$(find_candidate_repos "$pid")
      if [ -n "$candidates" ]; then
        while IFS= read -r c; do
          local new_pid
          new_pid=$(compute_project_id "$c")
          echo "  → 후보 repo: $c"
          echo "    신규 ID:  $new_pid"
        done <<< "$candidates"
      else
        echo "  (자동 매핑 실패 — SEARCH_ROOTS 아래에 해당 basename 의 git repo 없음)"
      fi
      echo ""
    fi
  done
  if [ "$found" -eq 0 ]; then
    echo "(레거시 디렉토리 없음)"
  else
    printf 'total: %d legacy directories\n' "$found"
  fi
}

# --dry-run: 이동 계획 출력
plan_migration() {
  source_project_id_lib
  echo "== Migration 계획 (dry-run) =="
  echo ""
  for d in "$LOGS_DIR"/*/; do
    [ -d "$d" ] || continue
    local pid
    pid=$(basename "$d")
    [[ "$pid" =~ $HASH_PATTERN ]] && continue

    local candidates
    candidates=$(find_candidate_repos "$pid")
    if [ -z "$candidates" ]; then
      echo "[$pid] SKIP (자동 매핑 실패)"
      continue
    fi
    local target_path
    target_path=$(printf '%s\n' "$candidates" | head -1)
    local new_pid
    new_pid=$(compute_project_id "$target_path")
    local new_dir="$LOGS_DIR/$new_pid"

    if [ -d "$new_dir" ]; then
      echo "[$pid] → [$new_pid] (MERGE — 기존 디렉토리 존재)"
      echo "  레거시: $(ls "$d" 2>/dev/null | tr '\n' ' ')"
      echo "  신규:   $(ls "$new_dir" 2>/dev/null | tr '\n' ' ')"
      echo "  concat 순서: 레거시(과거) 먼저 → 신규(현재) 뒤 (타임스탬프 오름차순)"
    else
      echo "[$pid] → [$new_pid] (RENAME — 신규 디렉토리 생성)"
    fi
    echo ""
  done
}

# --execute: 실제 수행
execute_migration() {
  source_project_id_lib
  echo "== Migration 실행 =="
  echo ""
  for d in "$LOGS_DIR"/*/; do
    [ -d "$d" ] || continue
    local pid
    pid=$(basename "$d")
    [[ "$pid" =~ $HASH_PATTERN ]] && continue

    local candidates
    candidates=$(find_candidate_repos "$pid")
    if [ -z "$candidates" ]; then
      echo "[$pid] SKIP (자동 매핑 실패)"
      continue
    fi
    local target_path
    target_path=$(printf '%s\n' "$candidates" | head -1)
    local new_pid
    new_pid=$(compute_project_id "$target_path")
    local new_dir="$LOGS_DIR/$new_pid"

    if [ ! -d "$new_dir" ]; then
      mv "$d" "$new_dir"
      echo "[$pid] → [$new_pid] RENAMED"
      continue
    fi

    # 충돌 — 각 파일 merge
    echo "[$pid] → [$new_pid] MERGING"
    local moved=0 merged=0
    # Markdown 로그 + .errors.log 전부 처리
    for oldfile in "$d"*.md "$d".errors.log; do
      [ -e "$oldfile" ] || continue
      local fname
      fname=$(basename "$oldfile")
      local target="$new_dir/$fname"
      if [ -e "$target" ]; then
        # concat: 레거시(과거) → 신규(현재). 타임스탬프 오름차순 보장.
        local tmp
        tmp=$(mktemp)
        cat "$oldfile" "$target" > "$tmp"
        mv "$tmp" "$target"
        rm "$oldfile"
        merged=$((merged + 1))
        echo "  MERGED: $fname"
      else
        mv "$oldfile" "$target"
        moved=$((moved + 1))
        echo "  MOVED:  $fname"
      fi
    done
    # 빈 디렉토리 정리
    if rmdir "$d" 2>/dev/null; then
      echo "  RMDIR:  $pid"
    fi
    echo "  요약: moved=$moved merged=$merged"
    echo ""
  done
}

case "${1:---help}" in
  --scan)     scan_legacy ;;
  --dry-run)  plan_migration ;;
  --execute)  execute_migration ;;
  --help|-h|"") print_help ;;
  *)
    echo "알 수 없는 옵션: $1"
    print_help
    exit 1
    ;;
esac
