#!/usr/bin/env bash
# spawn-kaizen-phase.sh — Phase N 실행용 부트스트랩
#
# 역할:
#   1. git tag kaizen-phase-{N}-pre 생성 (Regression 실패 시 되돌릴 지점)
#   2. .harness/.meta/kaizen-data-pool.md 에서 해당 Phase 의 §N 섹션 추출
#   3. 해당 Phase subagent 에게 전달할 프롬프트 템플릿 stdout 출력
#
# 사용법:
#   bash scripts/spawn-kaizen-phase.sh <phase-num>
#   bash scripts/spawn-kaizen-phase.sh --help
#
# 예:
#   bash scripts/spawn-kaizen-phase.sh 5    # Phase 5 (flutter-toolkit) 부트스트랩

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

usage() {
    cat <<'EOF'
spawn-kaizen-phase.sh — Phase N 실행 부트스트랩

사용법:
  bash scripts/spawn-kaizen-phase.sh <phase-num>
  bash scripts/spawn-kaizen-phase.sh --help

인자:
  <phase-num>  1 ~ 10 사이의 Phase 번호

동작:
  1. git tag kaizen-phase-{N}-pre 생성
  2. data pool §N 섹션 추출 및 stdout 출력
  3. subagent 프롬프트 템플릿 생성

Phase 번호 매핑:
  1 = 설계 가이드 (skill/agent-design-guide)
  2 = Contract (contract-design-guide, sprint-contract)
  3 = Evaluator (qa-evaluation-guide, qa-evaluator)
  4 = Harness (init, create-skill, create-agent, kaizen 스킬)
  5 = flutter-toolkit
  6 = design-kit
  7 = backend-kit
  8 = infra-kit
  9 = rust-kit
  10 = react-kit
EOF
}

if [[ "${1:-}" == "--help" ]] || [[ "${1:-}" == "-h" ]]; then
    usage
    exit 0
fi

if [[ $# -eq 0 ]]; then
    echo "ERROR: phase-num 인자가 필요합니다" >&2
    usage
    exit 1
fi

PHASE_NUM="$1"

if ! [[ "$PHASE_NUM" =~ ^[0-9]+$ ]] || [[ "$PHASE_NUM" -lt 1 ]] || [[ "$PHASE_NUM" -gt 10 ]]; then
    echo "ERROR: phase-num 은 1~10 사이여야 합니다 (받은 값: $PHASE_NUM)" >&2
    usage
    exit 1
fi

# Phase 이름 매핑
case "$PHASE_NUM" in
    1) PHASE_NAME="설계 가이드" ;;
    2) PHASE_NAME="Contract" ;;
    3) PHASE_NAME="Evaluator" ;;
    4) PHASE_NAME="Harness" ;;
    5) PHASE_NAME="flutter-toolkit" ;;
    6) PHASE_NAME="design-kit" ;;
    7) PHASE_NAME="backend-kit" ;;
    8) PHASE_NAME="infra-kit" ;;
    9) PHASE_NAME="rust-kit" ;;
    10) PHASE_NAME="react-kit" ;;
esac

TAG="kaizen-phase-${PHASE_NUM}-pre"

# Step 1: git tag 생성 (이미 있으면 skip)
if git rev-parse --verify "$TAG" >/dev/null 2>&1; then
    echo "⚠ tag $TAG 이미 존재 — skip" >&2
else
    git tag "$TAG"
    echo "✓ tag $TAG 생성" >&2
fi

DATA_POOL=".harness/.meta/kaizen-data-pool.md"
if [[ ! -f "$DATA_POOL" ]]; then
    echo "ERROR: $DATA_POOL 없음. 먼저 \`python3 scripts/collect-kaizen-data.py\` 실행." >&2
    exit 2
fi

# Step 2: data pool §N 추출 (해당 Phase 섹션만)
# kaizen-data-pool.md 의 §1 ~ §5 섹션을 Phase 별 참조 테이블에 따라 매핑
# 모든 Phase 는 §1 (feedback) + §5 (validate-plugin) 공통 참조
COMMON_SECTIONS="§1 §5"
case "$PHASE_NUM" in
    5|6|7|8|9|10) PHASE_SECTIONS="$COMMON_SECTIONS §2 §3" ;;
    *) PHASE_SECTIONS="$COMMON_SECTIONS" ;;
esac

# Step 2.5: kaizen-state.yaml 자동 갱신
STATE_FILE=".harness/.meta/kaizen-state.yaml"
if [[ -f "$STATE_FILE" ]]; then
    TIMESTAMP="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
    python3 - "$STATE_FILE" "$PHASE_NUM" "$TIMESTAMP" <<'PYEOF'
import sys, re
from pathlib import Path
path, phase, ts = Path(sys.argv[1]), sys.argv[2], sys.argv[3]
text = path.read_text(encoding="utf-8")
text = re.sub(r'(?m)^current_phase:.*$', f'current_phase: {phase}', text)
text = re.sub(r'(?m)^status:.*$', 'status: running', text)
text = re.sub(r'(?m)^cycle_id:.*$', f'cycle_id: "kaizen-{ts[:10]}"', text)
path.write_text(text, encoding="utf-8")
PYEOF
    echo "✓ kaizen-state.yaml 업데이트 (phase=$PHASE_NUM, status=running)" >&2
fi

# Step 3: 프롬프트 템플릿 출력 (stdout)
cat <<EOF
## Phase $PHASE_NUM — $PHASE_NAME 부트스트랩 완료

**Pre-tag:** \`$TAG\` 생성됨. Regression 실패 시 \`git reset --hard $TAG\` 로 되돌릴 수 있음.

**데이터 풀 경로:** \`$DATA_POOL\`
**참조 섹션:** $PHASE_SECTIONS
**리서치 템플릿:** \`.claude/skills/kaizen-orchestrator/references/phase-research-templates.md\` Phase $PHASE_NUM 섹션

---

## Subagent 프롬프트 (복사해서 Agent tool 에 전달)

너는 kaizen-orchestrator Phase $PHASE_NUM 서브에이전트다. 현재 디렉토리는 \`$REPO_ROOT\`, 브랜치는 현재 체크아웃된 브랜치다.

### 미션
Phase $PHASE_NUM ($PHASE_NAME) 범위를 **research-mode** 로 카이젠 개선한다.

### 데이터 풀 (반드시 먼저 읽기)
\`$DATA_POOL\` 의 $PHASE_SECTIONS 섹션을 우선 참조.

### 리서치 (필수)
\`.claude/skills/kaizen-orchestrator/references/phase-research-templates.md\` 의 Phase $PHASE_NUM 섹션에 명시된 필수 소스를 전부 조회.
Context7 quota 소진 시 Codex (codex-rescue) 로 fallback.

### 공통 실행 패턴
1. Triage: 데이터 풀 + 리서치
2. GAP 분석
3. 예방적 분석
4. Sprint Contract DRAFT → \`.harness/sprint-contract.md\`
5. Edit 로 적용
6. Self-audit L3
7. git commit (\`kaizen(phase${PHASE_NUM}-research): ...\`)
8. Regression: \`python3 scripts/validate-plugin.py\` 7 OK + \`bash scripts/finalize-phase.sh $PHASE_NUM pass\` 또는 \`fail\`

### 제약
- 브랜치 / push 금지
- Phase 1~$((PHASE_NUM - 1)) 파일 수정 금지
- bare code fence 0 건
- 리서치 URL commit message 에 명시
- REJECT 재평가 최대 3 회

### 리포트 형식
\`\`\`text
## Phase $PHASE_NUM 결과
- 리서치 소스: [URL]
- 개선 파일: [목록]
- commit: [hash]
- Self-QA: [PASS / FAIL]
- Regression: [7 OK / FAIL]
\`\`\`

시작.
EOF
