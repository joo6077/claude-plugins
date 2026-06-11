#!/usr/bin/env bash
# ── 환경 진단 (SessionStart hook) ──
# cwd에서 .harness/env.sh를 찾아 source한다.

set -eo pipefail
LOCALAPPDATA="${LOCALAPPDATA:-}"

ENV_SH=""
APP_DIR=""
for dir in "." ./*/; do
  if [ -f "$dir/.harness/env.sh" ]; then
    ENV_SH="$dir/.harness/env.sh"; APP_DIR="$dir"; break
  fi
done

if [ -z "$ENV_SH" ]; then
  echo "=== Environment Check ==="; echo "⚠️ .harness/env.sh not found"; exit 0
fi
source "$ENV_SH"

ISSUES=(); WARNINGS=()
OS="unknown"; SDK_CMD="${SDK_CMD_UNIX:-}"
case "$(uname -s)" in
  MINGW*|MSYS*|CYGWIN*) OS="windows"; SDK_CMD="${SDK_CMD_WINDOWS:-$SDK_CMD_UNIX}" ;;
  Darwin*) OS="macos" ;; Linux*) OS="linux" ;;
esac

SDK_OK=false
if [ -n "$SDK_CMD" ]; then
  command -v "$SDK_CMD" &>/dev/null && SDK_OK=true || ISSUES+=("SDK '$SDK_CMD' not found")
fi

for i in "${!REQUIRED_FILES[@]}"; do
  [ ! -f "$APP_DIR/${REQUIRED_FILES[$i]}" ] && WARNINGS+=("${REQUIRED_FILES_MSG[$i]:-${REQUIRED_FILES[$i]} missing}")
done

for cmd in "${REQUIRED_COMMANDS[@]}"; do
  command -v "$cmd" &>/dev/null || ISSUES+=("필수 명령 없음: $cmd")
done

echo "=== Environment Check ==="
echo "OS: $OS"
[ -n "${SDK_CMD_NAME:-}" ] && echo "SDK: ${SDK_CMD:-none} (available: $SDK_OK)"
for i in "${!REQUIRED_FILES[@]}"; do
  F="${REQUIRED_FILES[$i]}"; [ -f "$APP_DIR/$F" ] && echo "$F: true" || echo "$F: false"
done
# 외부 도구 확인
for i in "${!EXTERNAL_TOOLS_NAME[@]}"; do
  TOOL="${EXTERNAL_TOOLS_NAME[$i]}"
  TOOL_OK=false
  if command -v "$TOOL" &>/dev/null; then
    TOOL_OK=true
  elif [ -n "${EXTERNAL_TOOLS_WINDOWS_FALLBACK[$i]:-}" ]; then
    FALLBACK=$(eval echo "${EXTERNAL_TOOLS_WINDOWS_FALLBACK[$i]}")
    [ -f "$FALLBACK" ] && TOOL_OK=true
  fi
  OPT="${EXTERNAL_TOOLS_OPTIONAL[$i]:-true}"
  if [ "$TOOL_OK" = true ]; then
    echo "$TOOL: available"
  elif [ "$OPT" = true ]; then
    WARNINGS+=("$TOOL not found (optional)")
    echo "$TOOL: not found (optional)"
  else
    ISSUES+=("$TOOL not found (required)")
    echo "$TOOL: not found (required)"
  fi
done

[ ${#ISSUES[@]} -gt 0 ] && echo "" && echo "❌ ISSUES:" && printf '  - %s\n' "${ISSUES[@]}"
[ ${#WARNINGS[@]} -gt 0 ] && echo "" && echo "⚠️ WARNINGS:" && printf '  - %s\n' "${WARNINGS[@]}"
[ ${#ISSUES[@]} -eq 0 ] && [ ${#WARNINGS[@]} -eq 0 ] && echo "" && echo "✅ All checks passed"
