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

# --revert 처리
if [[ "$RESULT" == "fail" ]] && [[ "$REVERT_FLAG" == "--revert" ]]; then
    TAG="kaizen-phase-${PHASE_NUM}-pre"
    if git rev-parse --verify "$TAG" >/dev/null 2>&1; then
        echo
        echo "📝 revert 명령 (수동 실행):"
        echo "   git revert $TAG..HEAD"
        echo
        echo "⚠ 이 명령은 자동 실행되지 않습니다. revert 는 히스토리를 보존하며 Phase $PHASE_NUM 이후 커밋들을 되돌리는 새 커밋을 만듭니다."
        echo "   히스토리 파괴형 reset 이 필요하면 대신: git reset --hard $TAG (주의: 복구 불가)"
    else
        echo "⚠ tag $TAG 없음 — revert 불가" >&2
    fi
fi

echo
echo "$FAILURE_FILE 업데이트 완료 (last_updated: $TODAY)"
