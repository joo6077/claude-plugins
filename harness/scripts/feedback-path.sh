#!/usr/bin/env bash
set -eo pipefail

# OS별 글로벌 피드백 경로를 stdout으로 출력한다.
# 항상 Unix 스타일 forward-slash 경로를 출력한다.
#
# TODO: 향후 Claude Code 플러그인 데이터 저장 공식 컨벤션이 정해지면
#       그에 맞춰 경로를 마이그레이션해야 한다. 마이그레이션 스크립트 필요.
#
# Usage: bash feedback-path.sh
# Output: /c/Users/user/AppData/Roaming/harness/feedback (Windows)
#         /home/user/.harness/feedback (Linux/Mac)

resolve_path() {
  local raw_path="$1"
  # 백슬래시를 forward-slash로 변환
  echo "$raw_path" | sed 's|\\|/|g'
}

case "$(uname -s)" in
  MINGW*|MSYS*|CYGWIN*|Windows_NT)
    if [ -n "$APPDATA" ]; then
      echo "$(resolve_path "$APPDATA")/harness/feedback"
    else
      echo "$(resolve_path "$HOME")/.harness/feedback"
    fi
    ;;
  *)
    echo "$HOME/.harness/feedback"
    ;;
esac
