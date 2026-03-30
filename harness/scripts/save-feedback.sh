#!/usr/bin/env bash
set -eo pipefail

# 피드백 YAML을 스키마 검증 후 글로벌 경로에 저장한다.
# LLM이 생성한 draft YAML을 받아서 검증 + 복사 + 정리한다.
#
# Usage: bash save-feedback.sh <contract|evaluator> <draft-yaml-path>
# Output: 저장된 파일의 절대경로 (stdout)
# Exit: 0=성공, 1=검증실패, 2=인자오류

SKILL_TYPE="${1:?Usage: save-feedback.sh <contract|evaluator> <draft-yaml-path>}"
DRAFT_PATH="${2:?Usage: save-feedback.sh <contract|evaluator> <draft-yaml-path>}"

if [[ "$SKILL_TYPE" != "contract" && "$SKILL_TYPE" != "evaluator" ]]; then
  echo "ERROR: skill type must be 'contract' or 'evaluator'" >&2
  exit 2
fi

if [[ ! -f "$DRAFT_PATH" ]]; then
  echo "ERROR: draft file not found: $DRAFT_PATH" >&2
  exit 2
fi

# --- Python 명령 감지 (Windows Store 스텁 회피) ---
PYTHON_CMD=""
if command -v python3 &>/dev/null && python3 -c "pass" &>/dev/null; then
  PYTHON_CMD="python3"
elif command -v python &>/dev/null && python -c "pass" &>/dev/null; then
  PYTHON_CMD="python"
fi

# --- 스키마 검증 ---
validate_yaml() {
  local file="$1"

  # yq 또는 python으로 YAML 파싱 + 필수 필드 검증
  # 검증 대상: feedback-schema.yaml의 공통 필수 필드 + diagnosis
  if command -v yq &>/dev/null; then
    local fields=("schema_version" "skill" "timestamp" "project_hash" "project_name" "skill_version" "outcome" "diagnosis")
    for field in "${fields[@]}"; do
      local val
      val=$(yq ".$field" "$file" 2>/dev/null)
      if [[ "$val" == "null" || -z "$val" ]]; then
        echo "FAIL: $field 필드 누락" >&2; return 1
      fi
    done

  elif [[ -n "$PYTHON_CMD" ]]; then
    $PYTHON_CMD -c "
import yaml, sys
with open(sys.argv[1], encoding='utf-8') as f:
    d = yaml.safe_load(f)
required = ['schema_version', 'skill', 'timestamp', 'project_hash', 'project_name', 'skill_version', 'outcome', 'diagnosis']
missing = [k for k in required if k not in d or d[k] is None]
if missing:
    print(f'FAIL: 누락 필드: {missing}', file=sys.stderr)
    sys.exit(1)
" "$file" || return 1

  else
    echo "ERROR: yq 또는 python 필수 — 스키마 검증 불가" >&2
    return 1
  fi

  return 0
}

if ! validate_yaml "$DRAFT_PATH"; then
  echo "ERROR: 스키마 검증 실패" >&2
  exit 1
fi

# --- 글로벌 경로 결정 ---
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GLOBAL_DIR="$(bash "$SCRIPT_DIR/feedback-path.sh")/$SKILL_TYPE"

# --- 파일명 생성 (ISO8601 타임스탬프) ---
TIMESTAMP=$(date +"%Y-%m-%dT%H%M%S")

if command -v yq &>/dev/null; then
  PROJ_HASH=$(yq '.project_hash' "$DRAFT_PATH")
elif [[ -n "$PYTHON_CMD" ]]; then
  PROJ_HASH=$($PYTHON_CMD -c "import yaml, sys; print(yaml.safe_load(open(sys.argv[1], encoding='utf-8'))['project_hash'])" "$DRAFT_PATH")
else
  PROJ_HASH="unknown"
fi

FILENAME="${PROJ_HASH}-${TIMESTAMP}.yaml"

# --- 저장 시도 (글로벌 → 로컬 fallback) ---
SAVED_PATH=""

if mkdir -p "$GLOBAL_DIR" 2>/dev/null && cp "$DRAFT_PATH" "$GLOBAL_DIR/$FILENAME" 2>/dev/null; then
  SAVED_PATH="$GLOBAL_DIR/$FILENAME"
else
  echo "WARNING: 글로벌 저장 실패 — 로컬 fallback" >&2
  LOCAL_DIR="$(pwd)/.harness/feedback/$SKILL_TYPE"
  mkdir -p "$LOCAL_DIR"
  cp "$DRAFT_PATH" "$LOCAL_DIR/$FILENAME"
  SAVED_PATH="$LOCAL_DIR/$FILENAME"
fi

# --- draft 정리 ---
rm -f "$DRAFT_PATH"

# --- 결과 출력 ---
echo "$SAVED_PATH"
