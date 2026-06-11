#!/usr/bin/env bash
# ── SDK 커맨드 가드 (PreToolUse hook) ──
# exit 0 = 허용, exit 2 = 차단

ENV_SH=""
for dir in "." ./*/; do
  [ -f "$dir/.harness/env.sh" ] && { ENV_SH="$dir/.harness/env.sh"; break; }
done
[ -z "$ENV_SH" ] && exit 0
source "$ENV_SH"
[ -z "${SDK_CMD_NAME:-}" ] && exit 0

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | sed -n 's/.*"command"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | tail -1)
[ -z "$COMMAND" ] && exit 0

HAS_SDK=false
echo "$COMMAND" | grep -qE "(^|[&|; (])${SDK_CMD_NAME} " && HAS_SDK=true
if [ -n "${SDK_CMD_WINDOWS:-}" ] && [ "$SDK_CMD_WINDOWS" != "$SDK_CMD_NAME" ]; then
  echo "$COMMAND" | grep -qE "(^|[&|; (])${SDK_CMD_WINDOWS} " && HAS_SDK=false
fi
[ "$HAS_SDK" = false ] && exit 0

case "$(uname -s)" in
  MINGW*|MSYS*|CYGWIN*)
    echo "${SDK_GUARD_MSG:-SDK 명령을 OS에 맞게 변경하세요.}" >&2
    exit 2 ;;
esac

# 역방향 가드: Unix에서 Windows용 명령(예: fvm.bat) 사용 차단
if [ -n "${SDK_CMD_WINDOWS:-}" ] && [ "$SDK_CMD_WINDOWS" != "$SDK_CMD_NAME" ]; then
  HAS_WIN_CMD=false
  echo "$COMMAND" | grep -qE "(^|[&|; (])${SDK_CMD_WINDOWS} " && HAS_WIN_CMD=true
  if [ "$HAS_WIN_CMD" = true ]; then
    echo "Unix 환경에서는 '${SDK_CMD_WINDOWS}' 대신 '${SDK_CMD_UNIX:-$SDK_CMD_NAME}'을 사용하세요." >&2
    exit 2
  fi
fi
exit 0
