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

# Phase 이름 + 슬러그 매핑
# 슬러그는 Phase 번호 + kit 이름에서 결정론적으로 도출한다.
# Phase 를 병렬로 돌려도 계약 파일이 겹치지 않도록 Phase 마다 고유 슬러그를 발급한다.
case "$PHASE_NUM" in
    1) PHASE_NAME="설계 가이드"; PHASE_KIT="design-guides" ;;
    2) PHASE_NAME="Contract"; PHASE_KIT="contract" ;;
    3) PHASE_NAME="Evaluator"; PHASE_KIT="evaluator" ;;
    4) PHASE_NAME="Harness"; PHASE_KIT="harness" ;;
    5) PHASE_NAME="flutter-toolkit"; PHASE_KIT="flutter" ;;
    6) PHASE_NAME="design-kit"; PHASE_KIT="design" ;;
    7) PHASE_NAME="backend-kit"; PHASE_KIT="backend" ;;
    8) PHASE_NAME="infra-kit"; PHASE_KIT="infra" ;;
    9) PHASE_NAME="rust-kit"; PHASE_KIT="rust" ;;
    10) PHASE_NAME="react-kit"; PHASE_KIT="react" ;;
esac

SPRINT_SLUG="kaizen-phase${PHASE_NUM}-${PHASE_KIT}"

# 슬러그 형식 가드 (contract-schema 규약: ^[a-z0-9][a-z0-9-]{0,47}$)
if ! [[ "$SPRINT_SLUG" =~ ^[a-z0-9][a-z0-9-]{0,47}$ ]]; then
    echo "ERROR: 도출된 슬러그가 규약을 위반합니다: $SPRINT_SLUG" >&2
    exit 3
fi

# 계약 / QA 산출물 / amendment 경로 (CONTRACT_ROOT = 이 레포 루트)
CONTRACT_PATH="$REPO_ROOT/.harness/sprint-contract-${SPRINT_SLUG}.md"
FEEDBACK_PATH="$REPO_ROOT/.harness/sprint-feedback-${SPRINT_SLUG}.md"
AMENDMENT_PATH="$REPO_ROOT/.harness/sprint-amendments-${SPRINT_SLUG}.md"

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
**스프린트 슬러그:** \`$SPRINT_SLUG\` (Phase 전용 — 병렬 실행 시 다른 Phase 계약을 덮어쓰지 않는다)
**계약 경로:** \`$CONTRACT_PATH\`

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

### 계약 경로 (병렬 안전 — 고정 경로 금지)
이 Phase 의 스프린트 슬러그는 \`$SPRINT_SLUG\` 다. 산출물은 반드시 아래 슬러그 경로에 쓴다.

- 계약: \`$CONTRACT_PATH\`
- QA 산출물: \`$FEEDBACK_PATH\`
- amendment: \`$AMENDMENT_PATH\`

슬러그 없는 공용 경로(\`.harness/sprint-contract\` + \`.md\`)에 쓰지 마라 — 다른 Phase 가 동시에
같은 파일을 덮어쓰고, 그 Phase 의 qa-evaluator 가 남의 계약을 평가하게 된다.
계약 frontmatter 에 \`slug: $SPRINT_SLUG\` 와 \`status: active\` 를 명시하고, Phase 종료 시 \`status: done\` 으로 바꾼다.

### 공통 실행 패턴
1. Triage: 데이터 풀 + 리서치
2. GAP 분석
3. 예방적 분석
4. Sprint Contract DRAFT → \`$CONTRACT_PATH\`
5. Edit 로 적용
6. Self-audit L3
7. git commit (\`kaizen(phase${PHASE_NUM}-research): ...\`)
8. Regression: \`python3 scripts/validate-plugin.py\` 7 OK + \`bash scripts/finalize-phase.sh $PHASE_NUM pass\` 또는 \`fail\`

### QA 호출 시 (필수)
qa-evaluator 를 spawn 할 때 계약 경로를 **명시적으로 전달**한다 (계약 선택 ladder 1 단계 = 명시 경로).
프롬프트에 \`평가 대상 계약: $CONTRACT_PATH\` 를 적고, 환경변수로도 넘길 수 있으면
\`HARNESS_CONTRACT=$CONTRACT_PATH\` 를 함께 지정한다. 경로를 생략해 평가자가 스스로 고르게 두지 마라.

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
