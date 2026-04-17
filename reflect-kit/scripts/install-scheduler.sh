#!/usr/bin/env bash
# reflect-kit: /reflect-digest (주간) + /reflect-kaizen (월간) crontab 자동 등록 스크립트.
#
# 동작:
#   --dry-run   등록 예정 cron 라인만 stdout 출력 (실제 crontab 변경 없음).
#   --install   crontab에 라인 추가. 이미 동일 라인이 존재하면 건너뜀 (멱등).
#   --uninstall 이전 --install 로 추가된 라인을 crontab에서 제거.
#   --help      사용법 출력.
#
# 주간 cron:   매주 월요일 09:00 KST → /reflect-digest period=7d
# 월간 cron:   매월 1일 09:00 KST   → /reflect-kaizen window=30d
#
# Claude Code CLI를 `claude exec "<slash-command>"` 형태로 호출한다.
# 로컬 머신에 `claude` CLI가 PATH에 있어야 한다.

set +e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_DIR="$HOME/.claude/logs/_cron"
TAG="# reflect-kit:"

# 출력 경로는 사용자 홈 아래 로그 디렉토리. 없으면 --install 시 생성.

WEEKLY_LINE="0 9 * * 1 claude exec \"/reflect-digest period=7d\" > $LOG_DIR/digest-\$(date +\\%Y\\%m\\%d).log 2>&1 $TAG digest-weekly"
MONTHLY_LINE="0 9 1 * * claude exec \"/reflect-kaizen window=30d\" > $LOG_DIR/kaizen-\$(date +\\%Y\\%m\\%d).log 2>&1 $TAG kaizen-monthly"

print_help() {
  sed -n '2,20p' "$0"
}

dry_run() {
  echo "# 주간 (매주 월요일 09:00)"
  echo "$WEEKLY_LINE"
  echo ""
  echo "# 월간 (매월 1일 09:00)"
  echo "$MONTHLY_LINE"
}

ensure_log_dir() {
  mkdir -p "$LOG_DIR" 2>/dev/null
}

append_if_absent() {
  local line="$1"
  local current
  current=$(crontab -l 2>/dev/null || true)

  # 멱등성: 동일 라인(태그 기준)이 이미 존재하면 건너뜀
  if printf '%s\n' "$current" | grep -qF -- "$line"; then
    echo "SKIP (이미 등록됨): $line"
    return 0
  fi

  # 기존 crontab + 새 라인으로 덮어쓰기
  { printf '%s\n' "$current"; printf '%s\n' "$line"; } | crontab -
  echo "INSTALLED: $line"
}

install_all() {
  ensure_log_dir
  append_if_absent "$WEEKLY_LINE"
  append_if_absent "$MONTHLY_LINE"
  echo ""
  echo "== 현재 crontab (reflect-kit 항목) =="
  crontab -l 2>/dev/null | grep "$TAG" || echo "(none)"
}

uninstall_all() {
  local current
  current=$(crontab -l 2>/dev/null || true)
  if [ -z "$current" ]; then
    echo "(crontab empty)"
    return 0
  fi
  local filtered
  filtered=$(printf '%s\n' "$current" | grep -v "$TAG")
  printf '%s\n' "$filtered" | crontab -
  echo "UNINSTALLED: 모든 reflect-kit 항목 제거됨"
}

case "${1:---help}" in
  --dry-run)
    dry_run
    ;;
  --install)
    install_all
    ;;
  --uninstall)
    uninstall_all
    ;;
  --help|-h|"")
    print_help
    ;;
  *)
    echo "알 수 없는 옵션: $1"
    print_help
    exit 1
    ;;
esac
