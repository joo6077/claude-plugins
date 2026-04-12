#!/usr/bin/env bash
# finalize-phase.sh — Phase 종료 처리 스크립트
#
# 역할:
#   1. Regression 결과(pass/fail) 를 받아 .harness/.meta/kaizen-failure-count.yaml 업데이트
#   2. fail 이고 --revert 플래그 주어지면 git reset --hard kaizen-phase-N-pre 실행 제안
#   3. failure count 가 2 이상이면 사용자 에스컬레이션 경고 출력
#
# 사용법:
#   bash scripts/finalize-phase.sh <phase-num> <pass|fail> [--revert]
#   bash scripts/finalize-phase.sh --help

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

usage() {
    cat <<'EOF'
finalize-phase.sh — Phase 종료 처리

사용법:
  bash scripts/finalize-phase.sh <phase-num> <pass|fail> [--revert]

인자:
  <phase-num>     1 ~ 10
  <pass|fail>     Regression 결과
  --revert        fail 일 때 kaizen-phase-N-pre tag 로 되돌리는 git 명령 출력 (실행은 수동)

동작:
  pass  →  kaizen-failure-count.yaml 의 phase_N 을 0 으로 리셋
  fail  →  phase_N 을 +1, 2 이상이면 경고 출력

last_updated 필드는 자동으로 오늘 날짜로 갱신된다.
EOF
}

if [[ $# -eq 0 ]] || [[ "${1:-}" == "--help" ]] || [[ "${1:-}" == "-h" ]]; then
    usage
    exit 0
fi

if [[ $# -lt 2 ]]; then
    echo "ERROR: 인자 2 개 필요 (phase-num, pass|fail)" >&2
    usage
    exit 1
fi

PHASE_NUM="$1"
RESULT="$2"
REVERT_FLAG="${3:-}"

if ! [[ "$PHASE_NUM" =~ ^[0-9]+$ ]] || [[ "$PHASE_NUM" -lt 1 ]] || [[ "$PHASE_NUM" -gt 10 ]]; then
    echo "ERROR: phase-num 은 1~10 (받은 값: $PHASE_NUM)" >&2
    exit 1
fi

if [[ "$RESULT" != "pass" ]] && [[ "$RESULT" != "fail" ]]; then
    echo "ERROR: result 는 'pass' 또는 'fail' (받은 값: $RESULT)" >&2
    exit 1
fi

FAILURE_FILE=".harness/.meta/kaizen-failure-count.yaml"
if [[ ! -f "$FAILURE_FILE" ]]; then
    echo "ERROR: $FAILURE_FILE 없음" >&2
    exit 2
fi

TODAY="$(date +%Y-%m-%d)"

# Python 으로 YAML 수정 (최소 yaml 처리 — 단순 key: value 형식)
python3 - "$FAILURE_FILE" "$PHASE_NUM" "$RESULT" "$TODAY" <<'PYEOF'
import sys
import re
from pathlib import Path

path, phase_num, result, today = sys.argv[1:5]
path = Path(path)

text = path.read_text(encoding="utf-8")
key = f"phase_{phase_num}"

# Match `phase_N: <value>` possibly followed by `# comment`
pattern = re.compile(rf"^({re.escape(key)}:\s*)(\d+)([^\n]*)$", re.MULTILINE)

m = pattern.search(text)
if not m:
    # Add the key before `last_updated`
    new_entry = f"{key}: 0\n"
    if "last_updated:" in text:
        text = text.replace("last_updated:", new_entry + "last_updated:")
    else:
        text += "\n" + new_entry
    m = pattern.search(text)

if not m:
    print(f"ERROR: failed to add/find {key}", file=sys.stderr)
    sys.exit(2)

current = int(m.group(2))
trailing = m.group(3)

if result == "pass":
    new_val = 0
    trailing = f"  # reset on pass ({today})"
    print(f"✓ Phase {phase_num} PASS — counter reset (was {current})")
else:
    new_val = current + 1
    trailing = f"  # FAIL (+1) on {today} — total {new_val}"
    print(f"✗ Phase {phase_num} FAIL — counter {current} → {new_val}")
    if new_val >= 2:
        print()
        print(f"⚠  Phase {phase_num} has {new_val} consecutive failures.")
        print(f"⚠  해당 Phase 를 일시 중단하고 사용자에게 에스컬레이션 필요.")

new_line = f"{m.group(1)}{new_val}{trailing}"
text = text[:m.start()] + new_line + text[m.end():]

# Update last_updated
text = re.sub(
    r'(?m)^last_updated:\s*.*$',
    f'last_updated: "{today}"',
    text,
)

path.write_text(text, encoding="utf-8")
PYEOF

# kaizen-state.yaml 자동 갱신
STATE_FILE=".harness/.meta/kaizen-state.yaml"
if [[ -f "$STATE_FILE" ]]; then
    TIMESTAMP="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
    if [[ "$RESULT" == "pass" ]]; then
        # Phase 10 pass = 전체 사이클 완료
        if [[ "$PHASE_NUM" -eq 10 ]]; then
            NEW_STATUS="completed"
        else
            NEW_STATUS="running"
        fi
        python3 - "$STATE_FILE" "$PHASE_NUM" "$TIMESTAMP" "$NEW_STATUS" <<'STATE_PY'
import sys, re
from pathlib import Path
path, phase, ts, status = Path(sys.argv[1]), sys.argv[2], sys.argv[3], sys.argv[4]
text = path.read_text(encoding="utf-8")
text = re.sub(r'(?m)^last_approve_timestamp:.*$', f'last_approve_timestamp: "{ts}"', text)
text = re.sub(r'(?m)^status:.*$', f'status: {status}', text)
path.write_text(text, encoding="utf-8")
STATE_PY
    else
        python3 - "$STATE_FILE" "$TIMESTAMP" <<'STATE_PY'
import sys, re
from pathlib import Path
path, ts = Path(sys.argv[1]), sys.argv[2]
text = path.read_text(encoding="utf-8")
text = re.sub(r'(?m)^last_reject_timestamp:.*$', f'last_reject_timestamp: "{ts}"', text)
text = re.sub(r'(?m)^status:.*$', 'status: running', text)
path.write_text(text, encoding="utf-8")
STATE_PY
    fi
    echo "✓ kaizen-state.yaml 업데이트 (result=$RESULT)" >&2
fi

# --revert / --auto-revert 처리
TAG="kaizen-phase-${PHASE_NUM}-pre"
if [[ "$RESULT" == "fail" ]]; then
    if [[ "$REVERT_FLAG" == "--auto-revert" ]]; then
        if git rev-parse --verify "$TAG" >/dev/null 2>&1; then
            echo
            echo "🔄 Auto-revert 실행: git revert --no-edit $TAG..HEAD"
            git revert --no-edit "$TAG..HEAD" && \
                echo "✓ Auto-revert 완료" || \
                echo "✗ Auto-revert 실패 — 수동 확인 필요" >&2
        else
            echo "⚠ tag $TAG 없음 — auto-revert 불가" >&2
        fi
    elif [[ "$REVERT_FLAG" == "--revert" ]]; then
        if git rev-parse --verify "$TAG" >/dev/null 2>&1; then
            echo
            echo "📝 revert 명령 (수동 실행):"
            echo "   git revert --no-edit $TAG..HEAD"
            echo
            echo "⚠ 이 명령은 자동 실행되지 않습니다."
            echo "   자동 revert 를 원하면: bash scripts/finalize-phase.sh $PHASE_NUM fail --auto-revert"
        else
            echo "⚠ tag $TAG 없음 — revert 불가" >&2
        fi
    else
        echo
        echo "💡 revert 하려면: bash scripts/finalize-phase.sh $PHASE_NUM fail --revert"
        echo "   자동 revert: bash scripts/finalize-phase.sh $PHASE_NUM fail --auto-revert"
    fi
fi

# audit-log 자동 append (스크립트가 존재할 때만)
AUDIT_SCRIPT="$REPO_ROOT/scripts/append-audit-log.py"
if [[ -f "$AUDIT_SCRIPT" ]]; then
    python3 "$AUDIT_SCRIPT" --phase "$PHASE_NUM" --result "$RESULT" --date "$TODAY" 2>/dev/null && \
        echo "✓ audit-log 엔트리 추가됨" || \
        echo "⚠ audit-log append 실패 (무시)" >&2
fi

# changelog 알림
echo
echo "📝 changelog 업데이트 필요: docs/kaizen/changelog.md 에 오늘($TODAY) 엔트리 추가"
echo
echo "$FAILURE_FILE 업데이트 완료 (last_updated: $TODAY)"
