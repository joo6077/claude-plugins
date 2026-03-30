#!/usr/bin/env bash
set -eo pipefail

# 피드백 파일이 존재하고 유효한지 검증한다.
#
# Usage: bash verify-feedback.sh <saved-yaml-path>
# Output: PASS 또는 FAIL (with reason)
# Exit: 0=PASS, 1=FAIL

SAVED_PATH="${1:?Usage: verify-feedback.sh <saved-yaml-path>}"

# 1. 파일 존재 확인
if [[ ! -f "$SAVED_PATH" ]]; then
  echo "FAIL: 파일이 존재하지 않음 — $SAVED_PATH"
  exit 1
fi

# 2. 파일 비어있지 않음
if [[ ! -s "$SAVED_PATH" ]]; then
  echo "FAIL: 파일이 비어있음 — $SAVED_PATH"
  exit 1
fi

# 3. YAML 파싱 가능 + 필수 필드 존재
if command -v yq &>/dev/null; then
  for field in schema_version skill skill_version project_hash project_name outcome diagnosis; do
    VAL=$(yq ".$field" "$SAVED_PATH" 2>/dev/null)
    if [[ "$VAL" == "null" || -z "$VAL" ]]; then
      echo "FAIL: $field 누락"; exit 1
    fi
  done

elif command -v python3 &>/dev/null; then
  python3 -c "
import yaml, sys
with open(sys.argv[1]) as f:
    d = yaml.safe_load(f)
for k in ['schema_version', 'skill', 'skill_version', 'project_hash', 'project_name', 'outcome', 'diagnosis']:
    if k not in d or d[k] is None:
        print(f'FAIL: {k} 누락')
        sys.exit(1)
print('PASS')
" "$SAVED_PATH" && exit 0 || exit 1

else
  echo "FAIL: yq 또는 python3 필수 — 스키마 검증 불가"
  exit 1
fi

echo "PASS"
exit 0
