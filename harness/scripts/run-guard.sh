#!/usr/bin/env bash
# ── Run 가드 (PreToolUse hook) ──
# exit 0 = 허용, exit 2 = 차단

ENV_SH=""
APP_DIR=""
for dir in "." ./*/; do
  [ -f "$dir/.harness/env.sh" ] && { ENV_SH="$dir/.harness/env.sh"; APP_DIR="$dir"; break; }
done
[ -z "$ENV_SH" ] && exit 0
source "$ENV_SH"

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | sed -n 's/.*"command"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | tail -1)
CWD=$(echo "$INPUT" | sed -n 's/.*"cwd"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -1)
[ -z "$COMMAND" ] && exit 0

for guard in "${RUN_GUARDS[@]}"; do
  IFS='|' read -r CMD_PATTERN REQ_FLAG REQ_FILE WARN_MSG <<< "$guard"

  echo "$COMMAND" | grep -qE "$CMD_PATTERN" || continue

  # 필수 플래그 없으면 경고만
  if [ -n "$REQ_FLAG" ] && ! echo "$COMMAND" | grep -q "$REQ_FLAG"; then
    [ -n "$REQ_FILE" ] && [ -f "$APP_DIR/$REQ_FILE" ] && echo "⚠️ $WARN_MSG" >&2
    exit 0
  fi

  # 플래그 있으면 — 명령에서 지정한 실제 파일 확인
  if [ -n "$REQ_FLAG" ]; then
    ACTUAL_FILE=$(echo "$COMMAND" | sed -n "s/.*${REQ_FLAG}=\([^ \"]*\).*/\1/p")
    CHECK_FILE="${ACTUAL_FILE:-$REQ_FILE}"

    FOUND=false
    [ -f "$CHECK_FILE" ] && FOUND=true
    [ "$FOUND" = false ] && [ -n "$CWD" ] && [ -f "$CWD/$CHECK_FILE" ] && FOUND=true
    [ "$FOUND" = false ] && [ -f "$APP_DIR/$CHECK_FILE" ] && FOUND=true

    if [ "$FOUND" = false ]; then
      for i in "${!REQUIRED_FILES[@]}"; do
        if [ "${REQUIRED_FILES[$i]}" = "$REQ_FILE" ]; then
          echo "${REQUIRED_FILES_MSG[$i]:-$REQ_FILE 없음}" >&2
          [ -n "${REQUIRED_FILES_RESOLVE[$i]:-}" ] && echo "해결: ${REQUIRED_FILES_RESOLVE[$i]}" >&2
          break
        fi
      done
      exit 2
    fi
  fi
done
exit 0
