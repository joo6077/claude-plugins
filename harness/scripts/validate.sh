#!/usr/bin/env bash
# ── 하네스 config 유효성 검증 스크립트 ──
# exit 0 = 유효, exit 1 = 에러 존재

set -eo pipefail

# harness/scripts/ 또는 .claude/scripts/ 또는 직접 실행 모두 지원
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJ_ROOT=""

# 1) 현재 디렉토리에서 먼저 탐색
for dir in "$(pwd)" "$(pwd)"/*/; do
  if [ -f "$dir/.harness/project.yaml" ]; then
    PROJ_ROOT="$(pwd)"
    break
  fi
done

# 2) 스크립트 위치 기준으로 탐색 (harness/scripts/ → 2단계 위, .claude/scripts/ → 2단계 위)
if [ -z "$PROJ_ROOT" ]; then
  for depth in "../.." ".."; do
    CANDIDATE="$(cd "$SCRIPT_DIR/$depth" 2>/dev/null && pwd)"
    for dir in "$CANDIDATE" "$CANDIDATE"/*/; do
      if [ -f "$dir/.harness/project.yaml" ]; then
        PROJ_ROOT="$CANDIDATE"
        break 2
      fi
    done
  done
fi

HARNESS_DIR=""
if [ -n "$PROJ_ROOT" ]; then
  for dir in "$PROJ_ROOT" "$PROJ_ROOT"/*/; do
    if [ -f "$dir/.harness/project.yaml" ]; then
      HARNESS_DIR="$dir/.harness"
      break
    fi
  done
fi

if [ -z "$HARNESS_DIR" ]; then
  echo "❌ .harness/project.yaml not found"
  exit 1
fi

CONFIG="$HARNESS_DIR/project.yaml"
ERR=0
WARN=0

echo "=== Harness Config Validation ==="
echo "Config: $CONFIG"
echo ""

# ── 필수 필드 ──
for field in stack commands contract_categories anti_patterns; do
  if ! grep -q "^${field}:" "$CONFIG"; then
    echo "❌ 필수 필드 누락: $field"
    ERR=$((ERR + 1))
  fi
done

# commands.analyze, commands.test
for cmd in analyze test; do
  if ! grep -q "${cmd}:" "$CONFIG"; then
    echo "❌ 필수 필드 누락: commands.${cmd}"
    ERR=$((ERR + 1))
  fi
done

# ── anti_patterns 개수 ──
AP_COUNT=$(grep -c "id: AP-" "$CONFIG" 2>/dev/null || echo "0")
if [ "$AP_COUNT" -lt 2 ]; then
  echo "⚠️ anti_patterns ${AP_COUNT}개 — 최소 2개 권장"
  WARN=$((WARN + 1))
fi

# ── prefix 중복 ──
DUP=$(grep "prefix:" "$CONFIG" | sed 's/.*prefix: *"\(.*\)"/\1/' | sort | uniq -d)
if [ -n "$DUP" ]; then
  echo "❌ prefix 중복: $DUP"
  ERR=$((ERR + 1))
fi

# ── procedures 파일 존재 ──
PROC_DIR="$HARNESS_DIR/procedures"
if [ -d "$PROC_DIR" ]; then
  # contract_categories 섹션에서 id 추출
  CATS=$(sed -n '/^contract_categories:/,/^[a-z]/p' "$CONFIG" | grep "id:" | sed 's/.*id: *//' | tr '[:upper:]' '[:lower:]')
  for cat in $CATS; do
    PROC_FILE="$PROC_DIR/${cat}-verification.md"
    if [ ! -f "$PROC_FILE" ]; then
      echo "⚠️ procedures 파일 없음: ${cat}-verification.md (범용 폴백)"
      WARN=$((WARN + 1))
    fi
  done
else
  echo "⚠️ procedures/ 디렉토리 없음"
  WARN=$((WARN + 1))
fi

# ── 결과 ──
echo ""
SCORE=$((100 - ERR * 20 - WARN * 5))
if [ $SCORE -lt 0 ]; then SCORE=0; fi

if [ $ERR -eq 0 ] && [ $WARN -eq 0 ]; then
  echo "✅ All checks passed"
fi

echo "Score: ${SCORE}/100 (errors: ${ERR}, warnings: ${WARN})"

if [ $ERR -gt 0 ]; then exit 1; fi
exit 0
