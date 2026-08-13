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

# --- help path (side-effect free) ------------------------------------------
# `--help` 는 인자 처리 최상단에서 즉시 끝낸다. mktemp · cd · marketplace.json 읽기 같은
# 환경 의존은 전부 이 아래로 내린다 (harness/evals/gate-exit-codes.md §규칙).
# 실측 (2026-08-13): 쓰기 불가 환경에서 `mktemp` 가 먼저 돌아 `--help` 가 usage 를 한 줄도
# 내지 못하고 exit 1 했다. help 가 환경에 따라 죽으면 docs-as-code 검증 대상이 될 수 없다.
usage() {
    cat <<'EOF'
finalize-phase.sh — Phase 종료 처리

사용법:
  bash scripts/finalize-phase.sh <phase-num> <pass|fail> [--revert]

인자:
  <phase-num>     1 ~ MAX_PHASE. MAX_PHASE 는 .claude-plugin/marketplace.json 의
                  harness 제외 킷 수 + 4 로 자동 유도된다 (하드코드하지 않는다)
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

# --- 여기부터 환경 의존 ------------------------------------------------------
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${REPO_ROOT}"

# MAX_PHASE — orchestrator 의 마지막 Phase 번호.
# sync-orchestrator.py 와 동일한 규칙으로 유도한다: harness 메타 Phase 1~4 +
# marketplace.json 의 harness 제외 플러그인 수 (FIRST_PLUGIN_PHASE = 5).
# 킷이 늘어나면 자동으로 따라간다 — 하드코드 금지 (Phase 11~14 거부 회귀 재발 방지).
# 진단 출력은 임시 파일 대신 **변수**로 캡처한다 — 쓰기 가능한 TMP 에 의존하지 않기 위해서다
# (구판은 `mktemp` 를 썼고, 그것이 read-only 환경에서 `--help` 까지 죽였다).
# stdout+stderr 를 함께 받아 숫자가 아니면 그 내용을 그대로 원인으로 보여준다 —
# `2>/dev/null` 로 원인을 지우지 않는다 (harness/evals/gate-exit-codes.md §규칙).
MAX_PHASE="$(python3 - 2>&1 <<'MAXPY' || true
import json
from pathlib import Path
data = json.loads(Path(".claude-plugin/marketplace.json").read_text(encoding="utf-8"))
kits = [p for p in data.get("plugins", []) if p.get("name") != "harness"]
print(4 + len(kits))
MAXPY
)"
if ! [[ "${MAX_PHASE}" =~ ^[0-9]+$ ]]; then
    echo "⚠ MAX_PHASE 유도 실패 — 기본값 14 사용. 원인:" >&2
    printf '%s\n' "${MAX_PHASE}" | head -2 >&2
    MAX_PHASE=14
fi

if [[ $# -lt 2 ]]; then
    echo "ERROR: 인자 2 개 필요 (phase-num, pass|fail)" >&2
    usage
    exit 1
fi

PHASE_NUM="$1"
RESULT="$2"
REVERT_FLAG="${3:-}"

if ! [[ "${PHASE_NUM}" =~ ^[0-9]+$ ]] || [[ "${PHASE_NUM}" -lt 1 ]] || [[ "${PHASE_NUM}" -gt "${MAX_PHASE}" ]]; then
    echo "ERROR: phase-num 은 1~${MAX_PHASE} (받은 값: ${PHASE_NUM})" >&2
    echo "       MAX_PHASE 는 marketplace.json 의 harness 제외 킷 수 + 4 로 유도된다." >&2
    exit 1
fi

if [[ "${RESULT}" != "pass" ]] && [[ "${RESULT}" != "fail" ]]; then
    echo "ERROR: result 는 'pass' 또는 'fail' (받은 값: ${RESULT})" >&2
    exit 1
fi

FAILURE_FILE=".harness/.meta/kaizen-failure-count.yaml"
if [[ ! -f "${FAILURE_FILE}" ]]; then
    echo "ERROR: ${FAILURE_FILE} 없음" >&2
    exit 2
fi

TODAY="$(date +%Y-%m-%d)"

# Python 으로 YAML 수정 (최소 yaml 처리 — 단순 key: value 형식)
python3 - "${FAILURE_FILE}" "${PHASE_NUM}" "${RESULT}" "${TODAY}" <<'PYEOF'
import sys
import re
from pathlib import Path

path, phase_num, result, today = sys.argv[1:5]
path = Path(path)

text = path.read_text(encoding="utf-8")
key = f"phase_{phase_num}"

# Match `phase_N: <value>` possibly followed by `# comment`.
# 선행 공백을 그룹에 포함시켜야 한다 — 이 파일의 카운터는 `phases:` 매핑 하위에
# 2칸 들여쓰기로 존재한다. `^phase_N:` (열 0 고정) 으로 찾으면 항상 실패하여
# 최상위에 중복 키를 새로 만들고, 중첩된 실제 값은 갱신되지 않는다.
pattern = re.compile(rf"^([ \t]*{re.escape(key)}:[ \t]*)(\d+)([^\n]*)$", re.MULTILINE)

m = pattern.search(text)
if not m:
    # 키가 진짜 없으면 `phases:` 매핑 안에 같은 들여쓰기로 추가한다.
    phases_m = re.search(r"(?m)^phases:[ \t]*$", text)
    if phases_m:
        insert_at = phases_m.end() + 1  # skip the newline after `phases:`
        text = text[:insert_at] + f"  {key}: 0\n" + text[insert_at:]
    elif "last_updated:" in text:
        text = text.replace("last_updated:", f"{key}: 0\n" + "last_updated:")
    else:
        text += f"\n{key}: 0\n"
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
if [[ -f "${STATE_FILE}" ]]; then
    TIMESTAMP="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
    if [[ "${RESULT}" == "pass" ]]; then
        # 마지막 Phase pass = 전체 사이클 완료 (하드코드 금지 — MAX_PHASE 유도값 사용)
        if [[ "${PHASE_NUM}" -eq "${MAX_PHASE}" ]]; then
            NEW_STATUS="completed"
        else
            NEW_STATUS="running"
        fi
        python3 - "${STATE_FILE}" "${PHASE_NUM}" "${TIMESTAMP}" "${NEW_STATUS}" <<'STATE_PY'
import sys, re
from pathlib import Path
path, phase, ts, status = Path(sys.argv[1]), sys.argv[2], sys.argv[3], sys.argv[4]
text = path.read_text(encoding="utf-8")
text = re.sub(r'(?m)^last_approve_timestamp:.*$', f'last_approve_timestamp: "{ts}"', text)
text = re.sub(r'(?m)^status:.*$', f'status: {status}', text)
path.write_text(text, encoding="utf-8")
STATE_PY
    else
        python3 - "${STATE_FILE}" "${TIMESTAMP}" <<'STATE_PY'
import sys, re
from pathlib import Path
path, ts = Path(sys.argv[1]), sys.argv[2]
text = path.read_text(encoding="utf-8")
text = re.sub(r'(?m)^last_reject_timestamp:.*$', f'last_reject_timestamp: "{ts}"', text)
text = re.sub(r'(?m)^status:.*$', 'status: running', text)
path.write_text(text, encoding="utf-8")
STATE_PY
    fi
    echo "✓ kaizen-state.yaml 업데이트 (result=${RESULT})" >&2
fi

# --revert / --auto-revert 처리
TAG="kaizen-phase-${PHASE_NUM}-pre"
if [[ "${RESULT}" == "fail" ]]; then
    if [[ "${REVERT_FLAG}" == "--auto-revert" ]]; then
        if git rev-parse --verify "${TAG}" >/dev/null 2>&1; then
            echo
            echo "🔄 Auto-revert 실행: git revert --no-edit ${TAG}..HEAD"
            git revert --no-edit "${TAG}..HEAD" && \
                echo "✓ Auto-revert 완료" || \
                echo "✗ Auto-revert 실패 — 수동 확인 필요" >&2
        else
            echo "⚠ tag ${TAG} 없음 — auto-revert 불가" >&2
        fi
    elif [[ "${REVERT_FLAG}" == "--revert" ]]; then
        if git rev-parse --verify "${TAG}" >/dev/null 2>&1; then
            echo
            echo "📝 revert 명령 (수동 실행):"
            echo "   git revert --no-edit ${TAG}..HEAD"
            echo
            echo "⚠ 이 명령은 자동 실행되지 않습니다."
            echo "   자동 revert 를 원하면: bash scripts/finalize-phase.sh ${PHASE_NUM} fail --auto-revert"
        else
            echo "⚠ tag ${TAG} 없음 — revert 불가" >&2
        fi
    else
        echo
        echo "💡 revert 하려면: bash scripts/finalize-phase.sh ${PHASE_NUM} fail --revert"
        echo "   자동 revert: bash scripts/finalize-phase.sh ${PHASE_NUM} fail --auto-revert"
    fi
fi

# audit-log 자동 append (스크립트가 존재할 때만)
# 실패를 조용히 삼키지 마라 — 이 호출은 CLI 계약 불일치로 3 사이클 동안 무증상 실패했고,
# `2>/dev/null` 이 원인 진단을 막았다. 실패하면 stderr 를 그대로 노출한다
# (근거: Glite ARF — "rules ... fail loudly when violated" arxiv 2606.27416).
AUDIT_SCRIPT="${REPO_ROOT}/scripts/append-audit-log.py"
if [[ -f "${AUDIT_SCRIPT}" ]]; then
    AUDIT_ERR="$(mktemp)"
    if python3 "${AUDIT_SCRIPT}" --phase "${PHASE_NUM}" --result "${RESULT}" --date "${TODAY}" 2>"${AUDIT_ERR}"; then
        echo "✓ audit-log 엔트리 추가됨"
    else
        echo "⚠ audit-log append 실패 — 원인:" >&2
        head -3 "${AUDIT_ERR}" >&2
        echo "   (Phase 결과는 ${FAILURE_FILE} 에 기록됨. 위 원인을 고치기 전까지 audit-log 는 비어 있다)" >&2
    fi
    rm -f "${AUDIT_ERR}"
fi

# changelog 알림
echo
echo "📝 changelog 업데이트 필요: docs/kaizen/changelog.md 에 오늘(${TODAY}) 엔트리 추가"
echo
echo "${FAILURE_FILE} 업데이트 완료 (last_updated: ${TODAY})"
