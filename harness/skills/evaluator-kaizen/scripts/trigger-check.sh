#!/usr/bin/env bash
# evaluator-kaizen 이벤트 트리거 감지.
# 공통 로직은 trigger-check-common.sh에 위임한다.
#
# Usage: bash trigger-check.sh
# Exit: 0 = 트리거 발견, 1 = 트리거 없음, 2 = 에러

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec bash "$SCRIPT_DIR/../../../scripts/trigger-check-common.sh" evaluator \
  l3_unreached bias_detected evidence_missing \
  contract_misinterpret perspective_gap
