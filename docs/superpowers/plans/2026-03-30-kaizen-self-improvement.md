# 카이젠 Core QA 셀프 개선 시스템 구현 계획

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** sprint-contract와 qa-evaluator를 리서치 기반으로 자기개선하는 카이젠 시스템 구축 + 오케스트레이터 6 Phase 재구성

**Architecture:** 가이드 문서(contract-design-guide, qa-evaluation-guide) → 카이젠 스킬(contract-kaizen, evaluator-kaizen) → 글로벌 피드백 시스템(save/verify scripts) → 기존 스킬 수정(자기진단 + hard gate) → 오케스트레이터 재구성(6 Phase + triage + regression)

**Tech Stack:** Bash scripts, YAML, Markdown (SKILL.md), Claude Code plugin system

**Design Spec:** `docs/superpowers/specs/2026-03-30-kaizen-self-improvement-design.md`

---

## File Structure

### 신규 생성

```
harness/references/                          # NEW directory
├── contract-schema.md                       # 계약 포맷 공유 정의
└── feedback-schema.yaml                     # 피드백 YAML 스키마

docs/guides/
├── contract-design-guide.md                 # 계약 작성 원칙 가이드
└── qa-evaluation-guide.md                   # 평가 방법론 가이드

harness/scripts/
├── feedback-path.sh                         # OS별 글로벌 경로 해결
├── save-feedback.sh                         # 피드백 저장 + 스키마 검증
└── verify-feedback.sh                       # 피드백 존재/유효성 검증

harness/skills/contract-kaizen/
├── SKILL.md                                 # contract 카이젠 스킬
├── references/
│   ├── search-sources.md                    # 계약 설계 + 자기개선 리서치 소스
│   └── pr-template.md                       # PR 템플릿
├── scripts/
│   └── trigger-check.sh                     # 피드백 기반 트리거 감지
└── templates/
    └── research-log-entry.md                # 리서치 로그 포맷

harness/skills/evaluator-kaizen/
├── SKILL.md                                 # evaluator 카이젠 스킬
├── references/
│   ├── search-sources.md                    # 평가 방법론 + 자기개선 리서치 소스
│   └── pr-template.md                       # PR 템플릿
├── scripts/
│   └── trigger-check.sh                     # 피드백 기반 트리거 감지
└── templates/
    └── research-log-entry.md                # 리서치 로그 포맷

harness/evals/kaizen/
├── contract-kaizen/
│   ├── fixture-feedback-data/
│   │   ├── ambiguous-conditions.yaml
│   │   ├── category-bias.yaml
│   │   └── low-coverage.yaml
│   ├── expected-improvements.md
│   └── assertions.json
├── evaluator-kaizen/
│   ├── fixture-feedback-data/
│   │   ├── l3-miss.yaml
│   │   ├── false-approve.yaml
│   │   └── reject-loop.yaml
│   ├── expected-improvements.md
│   └── assertions.json
└── feedback-system/
    ├── save-test.sh
    └── aggregation-test.sh
```

### 수정

```
harness/skills/sprint-contract/SKILL.md      # 자기진단 + 피드백 hard gate + 가이드 참조
harness/agents/qa-evaluator.md               # 자기진단 + 피드백 hard gate + 가이드 참조
.claude/skills/kaizen-orchestrator/SKILL.md  # 6 Phase 재구성
```

---

## Task 1: 공유 참조 파일 생성 (harness/references/)

**Files:**
- Create: `harness/references/contract-schema.md`
- Create: `harness/references/feedback-schema.yaml`

- [ ] **Step 1: harness/references/ 디렉토리 생성 확인**

```bash
ls harness/
```

Expected: `references/` 디렉토리가 없음. 파일 생성 시 자동 생성됨.

- [ ] **Step 2: contract-schema.md 작성**

```markdown
# Sprint Contract 스키마

> sprint-contract와 qa-evaluator가 공유하는 계약 포맷 정의.
> contract-kaizen이 변경 제안 가능, evaluator-kaizen이 읽어서 평가 루브릭에 반영.

## 계약 파일

**경로**: `.harness/sprint-contract.md`

## 메타데이터 (YAML frontmatter)

```yaml
feature: "{기능명}"
created: "{YYYY-MM-DD HH:mm}"
complexity: "{단순|중간|복잡}"
conditions: {총 조건 수}
```

## 필수 섹션

### 1. 카테고리별 조건

```markdown
## {CategoryID}
- [ ] {PREFIX}-{NN}: {PASS/FAIL 이진 판정 가능한 조건문}
```

- `CategoryID`와 `PREFIX`는 `project.yaml.contract_categories`에서 가져온다
- 조건문은 능동태, 단일 조건, 측정 가능해야 한다
- "잘 동작한다", "적절히 처리한다" 같은 모호 표현 금지

### 2. Anti-patterns

```markdown
## Anti-patterns
- [ ] {id}: {message}
```

- `project.yaml.anti_patterns`에서 최소 2개 선별
- 해당 구현에서 발생 가능성이 높은 것을 우선 선택

### 3. Reusability (자동 포함)

```markdown
## Reusability
- [ ] RE-01: private 일회용 컴포넌트가 없다
- [ ] RE-02: 기존 공용 컴포넌트를 재사용한다
```

### 4. Diagnostics (자동 포함)

```markdown
## Diagnostics
- [ ] DG-01: analyze 경고 0건
- [ ] DG-02: analyze 에러 0건
- [ ] DG-03: 테스트 전체 통과
- [ ] DG-04: 콘솔 에러 0건
```

## 복잡도별 조건 수 가이드

| 복잡도 | 파일 영향 | 조건 수 |
|--------|----------|--------|
| 단순 | 1-3 | 4-6 |
| 중간 | 4-8 | 8-12 |
| 복잡 | 9+ | 12-20 |

## 스키마 버전

현재: v1
```

- [ ] **Step 3: feedback-schema.yaml 작성**

```yaml
# 피드백 스키마 v1
# sprint-contract와 qa-evaluator 실행 후 글로벌 저장되는 피드백 파일 포맷
# save-feedback.sh가 이 스키마로 검증한다

schema_version: 1

# --- 공통 필수 ---
# timestamp: ISO-8601 (예: "2026-03-30T14:00:00+09:00")
# project_hash: string(8) — 프로젝트 경로 SHA-256 앞 8자
# project_name: string — 사람이 읽을 수 있는 프로젝트 식별자
# skill: enum [sprint-contract, qa-evaluator]
# skill_version: semver (예: "1.3.0")
# outcome: enum [completed, failed, blocked]

# --- contract 전용 (skill=sprint-contract일 때) ---
# contract:
#   condition_count: int
#   category_count: int
#   category_coverage: float (0.0-1.0)
#   anti_pattern_count: int (>= 2)
#   complexity: enum [simple, medium, complex]

# --- evaluator 전용 (skill=qa-evaluator일 때) ---
# evaluation:
#   verdict: enum [APPROVE, REJECT, BLOCKED]
#   conditions_total: int
#   conditions_passed: int
#   l3_coverage: float (0.0-1.0)
#   reject_reasons: list[string]

# --- 자기진단 (공통) ---
# diagnosis:
#   checklist: map[string, bool|int|float|string]
#   cross_diagnosis_by: enum [sprint-contract, qa-evaluator]
#   cross_diagnosis_notes: string
#   improvement_suggestions: list[string]

# --- 사용자 시그널 (optional) ---
# user_rating: enum [good, bad] | null
# user_comment: string | null

# 예시:
example:
  schema_version: 1
  timestamp: "2026-03-30T14:00:00+09:00"
  project_hash: "a1b2c3d4"
  project_name: "my-flutter-app"
  skill: sprint-contract
  skill_version: "0.3.3"
  outcome: completed
  contract:
    condition_count: 8
    category_count: 4
    category_coverage: 0.8
    anti_pattern_count: 3
    complexity: medium
  diagnosis:
    checklist:
      ambiguous_conditions: false
      missing_error_paths: true
      untestable_conditions: false
      category_coverage_gap: false
      complexity_underestimate: false
    cross_diagnosis_by: qa-evaluator
    cross_diagnosis_notes: "조건 3번 경계값 누락 가능성"
    improvement_suggestions:
      - "에러 경로 조건을 별도 카테고리로 분리"
  user_rating: null
  user_comment: null
```

- [ ] **Step 4: 커밋**

```bash
git add harness/references/contract-schema.md harness/references/feedback-schema.yaml
git commit -m "feat(harness): 공유 참조 파일 생성 — contract-schema + feedback-schema"
```

---

## Task 2: 가이드 문서 생성

**Files:**
- Create: `docs/guides/contract-design-guide.md`
- Create: `docs/guides/qa-evaluation-guide.md`

- [ ] **Step 1: contract-design-guide.md 작성**

```markdown
# Contract Design Guide

> sprint-contract 스킬이 참조하는 계약 작성 원칙.
> contract-kaizen이 리서치 기반으로 이 문서를 갱신한다.
>
> **참조 스키마**: `harness/references/contract-schema.md`

---

## 핵심 원칙

### 검증 가능성 (Verifiability)

모든 조건은 제3자가 코드만 보고 PASS/FAIL을 판정할 수 있어야 한다.

- **좋은 예**: "로그인 실패 시 HTTP 401을 반환한다"
- **나쁜 예**: "로그인이 적절히 처리된다"

### 단일 해석 (Unambiguity)

조건은 단 하나의 해석만 가능해야 한다. IEEE 29148 기반 품질 기준:

- 능동태 사용 ("시스템이 반환한다" not "반환되어야 한다")
- 단일 조건 ("A이고 B이다" → 조건 2개로 분리)
- 모호 형용사 금지 ("빠르게", "적절히", "충분히" → 구체 수치)

### 측정 가능성 (Measurability)

조건의 충족 여부를 파일, 코드, 실행 결과로 증명할 수 있어야 한다.

---

## 조건 작성법

### NASA Requirements Writing Standards 기반

1. 각 조건은 하나의 "shall" (또는 한국어 "~한다")만 포함
2. 부정 조건보다 긍정 조건 선호 ("에러가 없다" → "정상 응답을 반환한다")
3. "and/or" 사용 금지 — 각각 별도 조건으로

### Precondition / Postcondition / Invariant 모델

Design by Contract (Meyer, 1992) 구조를 참고:

- **Precondition**: 구현 시작 전 충족되어야 하는 조건 (환경, 의존성)
- **Postcondition**: 구현 완료 후 반드시 참이어야 하는 조건 (핵심 기능)
- **Invariant**: 구현 전후로 변하지 않아야 하는 조건 (기존 기능 보전)

### Given-When-Then 구조화

BDD(Behavior-Driven Development) 패턴으로 조건을 구조화할 수 있다:

```
Given {전제 조건}
When {동작}
Then {기대 결과}
```

모든 조건에 강제는 아니지만, 복잡한 조건일수록 이 구조가 모호성을 줄인다.

### Property 기반 vs Example 기반

- **Example 기반**: "입력 'abc'에 대해 'ABC'를 반환한다" — 구체적이지만 범위 좁음
- **Property 기반**: "모든 입력에 대해 출력 길이가 입력 길이와 같다" — 범위 넓음

단순 기능은 Example 기반, 복잡한 로직은 Property 기반을 혼용한다.

---

## 카테고리 설계

### GQM (Goal-Question-Metric) Framework

1. **Goal**: 이 기능이 달성하려는 목표는 무엇인가?
2. **Question**: 목표 달성을 어떻게 확인하는가?
3. **Metric**: 어떤 구체적 지표로 측정하는가?

카테고리는 Goal에서 도출한다. project.yaml의 `contract_categories`가 이미 정의되어 있으면 그것을 따른다.

### Consumer-Driven 원칙

계약의 "소비자"는 qa-evaluator이다. 평가자가 독립적으로 검증할 수 없는 조건은 나쁜 조건이다.

자기 점검: "이 조건을 코드와 실행 결과만으로 PASS/FAIL 판정할 수 있는가?"
- YES → 유효한 조건
- NO → 재작성 필요

---

## 안티패턴

| 안티패턴 | 문제 | 수정 방법 |
|----------|------|-----------|
| 모호한 조건 | "적절히 처리한다" → 해석이 여러 개 | 구체적 행동과 결과로 재작성 |
| 단일 카테고리 편중 | 모든 조건이 UI에만 집중 | GQM으로 카테고리 균형 확인 |
| 복합 조건 | "A이고 B이며 C이다" | 각각 독립 조건으로 분리 |
| 과소 안티패턴 | 0-1개 안티패턴 | 최소 2개 필수 |
| 테스트 불가 조건 | "사용자 경험이 좋다" | 측정 가능한 지표로 변환 |
| 복잡도 과소평가 | 파일 수로만 판단 | 영향 범위(레이어, 공개 API)로 판단 |

---

## 자기개선 메커니즘

### 구조화 진단 체크리스트

sprint-contract 실행 완료 후 다음 항목을 자가 점검한다:

| 항목 | 점검 내용 |
|------|-----------|
| ambiguous_conditions | 모호한 표현이 포함된 조건이 있는가? |
| missing_error_paths | 에러/예외 경로에 대한 조건이 누락되었는가? |
| untestable_conditions | 코드만으로 검증 불가능한 조건이 있는가? |
| category_coverage_gap | project.yaml 카테고리 중 커버하지 못한 것이 있는가? |
| complexity_underestimate | 복잡도를 과소평가하여 조건 수가 부족한가? |

### 교차 진단 프로토콜

sprint-contract 실행 후 Agent tool로 qa-evaluator 서브에이전트를 호출한다.

- **전달 내용**: 생성된 계약 조건 (출력만)
- **미전달**: 의사결정 과정, 사용자 대화 내용
- **핵심 질문**: "이 조건을 독립적으로 검증할 수 있는가?"
- **결과**: 피드백 YAML의 `cross_diagnosis` 필드에 기록

### 피드백 수집 지표

- `condition_count`: 조건 총 개수
- `category_count`: 사용된 카테고리 수
- `category_coverage`: project.yaml 카테고리 대비 커버 비율
- `anti_pattern_count`: 선택된 안티패턴 수
- `complexity`: 판단된 복잡도
```

- [ ] **Step 2: qa-evaluation-guide.md 작성**

```markdown
# QA Evaluation Guide

> qa-evaluator 에이전트가 참조하는 평가 방법론.
> evaluator-kaizen이 리서치 기반으로 이 문서를 갱신한다.
>
> **참조 스키마**: `harness/references/contract-schema.md`

---

## 핵심 원칙

### Test Oracle로서의 역할

qa-evaluator는 "정답을 아는 존재"(test oracle)로서 계약 조건 대비 구현을 판정한다. 계약이 oracle specification이며, evaluator는 이를 기계적으로 적용한다.

- 계약에 없는 기준으로 판단하지 않는다
- 계약 조건의 "의도"가 아닌 "문자 그대로"를 적용한다
- "아마 이런 뜻일 것이다"는 해석을 하지 않는다

### LLM-as-a-Judge 편향 완화

LLM이 판정자 역할을 할 때 발생하는 알려진 편향:

| 편향 | 설명 | 완화 전략 |
|------|------|-----------|
| 위치 편향 (Position bias) | 먼저 본 항목에 호의적 | 조건 순서를 무작위로 평가 |
| 장황함 편향 (Verbosity bias) | 긴 코드/설명에 호의적 | 조건 충족 여부만 판단, 코드 양 무시 |
| 자기강화 편향 (Self-enhancement) | 자기가 생성한 것에 호의적 | generator와 evaluator 컨텍스트 분리 |

### IV&V 독립성 보장

Independent Verification & Validation (IV&V) 원칙:

- evaluator는 generator의 의도나 과정을 알지 않는다
- 계약과 산출물만으로 판정한다
- "커밋 메시지에 완료라고 썼다" ≠ 증거
- "TODO: 추후 수정" ≠ 현재 PASS

---

## 검증 방법론

### 3-Level 검증

| Level | 검증 방법 | 도구 | 목적 |
|-------|----------|------|------|
| L1: 구조 | 파일/디렉토리 존재 확인 | Glob, ls | 산출물이 있는가? |
| L2: 내용 | 파일 내용에 기대 요소 존재 | Read, Grep | 코드가 작성되었는가? |
| L3: 의미 | 코드 경로 추적, 행동 검증 | Read + 논리 추적 | 코드가 의도대로 동작하는가? |

**모든 조건은 L3까지 도달해야 한다.** L1/L2에서 PASS해도 L3에서 FAIL이면 전체 FAIL.

학술적 근거: 3계층 모델은 industry code review의 lint → semantic → AI 모델과 대응한다.

### Rubric 기반 분해

각 계약 조건을 boolean 서브체크로 분해한다 (CheckEval 패턴):

```
조건: "로그인 실패 시 HTTP 401을 반환한다"
├── 서브체크 1: 로그인 실패 경로가 존재하는가? (L1)
├── 서브체크 2: 해당 경로에서 401을 반환하는 코드가 있는가? (L2)
└── 서브체크 3: 잘못된 credential 입력 시 실제로 401 경로를 타는가? (L3)
```

서브체크 하나라도 FAIL이면 해당 조건은 FAIL.

### 다관점 평가 (Perspective-Based Reading)

각 조건을 최소 2개 관점에서 평가한다:

| 관점 | 초점 | 예시 질문 |
|------|------|-----------|
| 기능 | 명시된 행동이 구현되었는가? | "버튼 클릭 시 API 호출되는가?" |
| 엣지 케이스 | 경계 조건에서 올바른가? | "빈 입력, null, 최대 길이에서?" |
| 성능 | 비효율이나 병목이 있는가? | "N+1 쿼리, 불필요한 리렌더링?" |
| 보안 | 취약점이 있는가? | "SQL 인젝션, XSS 가능성?" |

---

## 판정 기준

### Evidence-Based 판정

모든 PASS/FAIL에는 증거가 필요하다:

- **PASS 증거**: `{파일}:{라인}` — 해당 코드가 조건을 충족하는 이유
- **FAIL 증거**: `{파일}:{라인}` — 해당 코드가 조건을 충족하지 않는 이유, 또는 코드 부재

"확인했다", "문제 없다" 같은 self-assertion은 증거가 아니다.

### Metamorphic Testing 원칙

절대 정답을 모를 때 관계 기반으로 검증한다:

- "입력을 2배로 하면 출력도 2배인가?" (비례 관계)
- "같은 입력을 2번 넣으면 같은 결과인가?" (멱등성)
- "A를 추가해도 B에 영향 없는가?" (독립성)

계약 조건으로 직접 판정 가능한 경우 metamorphic testing은 불필요.

---

## 자기개선 메커니즘

### 구조화 진단 체크리스트

qa-evaluator 실행 완료 후 다음 항목을 자가 점검한다:

| 항목 | 점검 내용 |
|------|-----------|
| l3_unreached | L3 검증에 도달하지 못한 조건이 있는가? |
| bias_detected | 편향 징후가 감지되었는가? (너무 관대, 증거 없이 PASS) |
| evidence_missing | 증거 없이 판정한 조건이 있는가? |
| contract_misinterpret | 계약 조건을 원래 의도와 다르게 해석했을 가능성이 있는가? |
| perspective_gap | 단일 관점에서만 평가한 조건이 있는가? |

### 교차 진단 프로토콜

qa-evaluator 실행 후 Agent tool로 sprint-contract 서브에이전트를 호출한다.

- **전달 내용**: 평가 판정 결과 (출력만)
- **미전달**: 평가 과정의 추론, 중간 메모
- **핵심 질문**: "계약 조건의 원래 의도를 정확히 해석했는가?"
- **결과**: 피드백 YAML의 `cross_diagnosis` 필드에 기록

### Mutation Testing (테스터를 테스트)

evaluator-kaizen이 주기적으로 수행:

1. 기존 fixture에 의도적 결함 삽입
2. qa-evaluator 실행
3. 결함을 잡으면 PASS, 놓치면 evaluator에 약점 존재
4. 약점을 Gotchas나 검증 로직에 반영

### 피드백 수집 지표

- `verdict`: APPROVE/REJECT/BLOCKED
- `conditions_total`: 전체 조건 수
- `conditions_passed`: PASS 조건 수
- `l3_coverage`: L3 검증 도달 비율
- `reject_reasons`: REJECT 시 사유 목록
```

- [ ] **Step 3: 커밋**

```bash
git add docs/guides/contract-design-guide.md docs/guides/qa-evaluation-guide.md
git commit -m "docs(guides): 계약 설계 가이드 + QA 평가 가이드 생성"
```

---

## Task 3: 피드백 인프라 스크립트 생성

**Files:**
- Create: `harness/scripts/feedback-path.sh`
- Create: `harness/scripts/save-feedback.sh`
- Create: `harness/scripts/verify-feedback.sh`

- [ ] **Step 1: feedback-path.sh 작성**

```bash
#!/usr/bin/env bash
set -eo pipefail

# OS별 글로벌 피드백 경로를 stdout으로 출력한다.
# 항상 Unix 스타일 forward-slash 경로를 출력한다.
#
# TODO: 향후 Claude Code 플러그인 데이터 저장 공식 컨벤션이 정해지면
#       그에 맞춰 경로를 마이그레이션해야 한다. 마이그레이션 스크립트 필요.
#
# Usage: bash feedback-path.sh
# Output: /c/Users/user/AppData/Roaming/harness/feedback (Windows)
#         /home/user/.harness/feedback (Linux/Mac)

resolve_path() {
  local raw_path="$1"
  # 백슬래시를 forward-slash로 변환
  echo "$raw_path" | sed 's|\\|/|g'
}

case "$(uname -s)" in
  MINGW*|MSYS*|CYGWIN*|Windows_NT)
    if [ -n "$APPDATA" ]; then
      echo "$(resolve_path "$APPDATA")/harness/feedback"
    else
      echo "$(resolve_path "$HOME")/.harness/feedback"
    fi
    ;;
  *)
    echo "$HOME/.harness/feedback"
    ;;
esac
```

- [ ] **Step 2: save-feedback.sh 작성**

```bash
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

# --- 스키마 검증 ---
validate_yaml() {
  local file="$1"

  # yq 또는 python으로 YAML 파싱 + 필수 필드 검증
  if command -v yq &>/dev/null; then
    # yq로 필수 필드 확인
    local schema_ver
    schema_ver=$(yq '.schema_version' "$file" 2>/dev/null)
    local skill
    skill=$(yq '.skill' "$file" 2>/dev/null)
    local timestamp
    timestamp=$(yq '.timestamp' "$file" 2>/dev/null)
    local project_hash
    project_hash=$(yq '.project_hash' "$file" 2>/dev/null)
    local outcome
    outcome=$(yq '.outcome' "$file" 2>/dev/null)

    if [[ "$schema_ver" == "null" || -z "$schema_ver" ]]; then
      echo "FAIL: schema_version 필드 누락" >&2; return 1
    fi
    if [[ "$skill" == "null" || -z "$skill" ]]; then
      echo "FAIL: skill 필드 누락" >&2; return 1
    fi
    if [[ "$timestamp" == "null" || -z "$timestamp" ]]; then
      echo "FAIL: timestamp 필드 누락" >&2; return 1
    fi
    if [[ "$project_hash" == "null" || -z "$project_hash" ]]; then
      echo "FAIL: project_hash 필드 누락" >&2; return 1
    fi
    if [[ "$outcome" == "null" || -z "$outcome" ]]; then
      echo "FAIL: outcome 필드 누락" >&2; return 1
    fi

  elif command -v python3 &>/dev/null; then
    python3 -c "
import yaml, sys
with open('$file') as f:
    d = yaml.safe_load(f)
required = ['schema_version', 'skill', 'timestamp', 'project_hash', 'outcome']
missing = [k for k in required if k not in d or d[k] is None]
if missing:
    print(f'FAIL: 누락 필드: {missing}', file=sys.stderr)
    sys.exit(1)
print('OK')
" || return 1

  elif command -v python &>/dev/null; then
    python -c "
import yaml, sys
with open('$file') as f:
    d = yaml.safe_load(f)
required = ['schema_version', 'skill', 'timestamp', 'project_hash', 'outcome']
missing = [k for k in required if k not in d or d[k] is None]
if missing:
    print('FAIL: missing fields: %s' % missing, file=sys.stderr)
    sys.exit(1)
print('OK')
" || return 1

  else
    echo "WARNING: yq/python 없음 — 스키마 검증 건너뜀" >&2
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
elif command -v python3 &>/dev/null; then
  PROJ_HASH=$(python3 -c "import yaml; print(yaml.safe_load(open('$DRAFT_PATH'))['project_hash'])")
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
  LOCAL_DIR=".harness/feedback/$SKILL_TYPE"
  mkdir -p "$LOCAL_DIR"
  cp "$DRAFT_PATH" "$LOCAL_DIR/$FILENAME"
  SAVED_PATH="$LOCAL_DIR/$FILENAME"
fi

# --- draft 정리 ---
rm -f "$DRAFT_PATH"

# --- 결과 출력 ---
echo "$SAVED_PATH"
```

- [ ] **Step 3: verify-feedback.sh 작성**

```bash
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
  SCHEMA_VER=$(yq '.schema_version' "$SAVED_PATH" 2>/dev/null)
  SKILL=$(yq '.skill' "$SAVED_PATH" 2>/dev/null)
  DIAGNOSIS=$(yq '.diagnosis' "$SAVED_PATH" 2>/dev/null)

  if [[ "$SCHEMA_VER" == "null" || -z "$SCHEMA_VER" ]]; then
    echo "FAIL: schema_version 누락"; exit 1
  fi
  if [[ "$SKILL" == "null" || -z "$SKILL" ]]; then
    echo "FAIL: skill 누락"; exit 1
  fi
  if [[ "$DIAGNOSIS" == "null" || -z "$DIAGNOSIS" ]]; then
    echo "FAIL: diagnosis 섹션 누락"; exit 1
  fi

elif command -v python3 &>/dev/null; then
  python3 -c "
import yaml, sys
with open('$SAVED_PATH') as f:
    d = yaml.safe_load(f)
for k in ['schema_version', 'skill', 'diagnosis']:
    if k not in d or d[k] is None:
        print(f'FAIL: {k} 누락')
        sys.exit(1)
print('PASS')
" && exit 0 || exit 1

else
  # yq/python 없으면 기본 검증만 (파일 존재 + 비어있지 않음 = PASS)
  echo "WARNING: yq/python 없음 — 기본 검증만 수행"
fi

echo "PASS"
exit 0
```

- [ ] **Step 4: 실행 권한 부여 및 테스트**

```bash
chmod +x harness/scripts/feedback-path.sh harness/scripts/save-feedback.sh harness/scripts/verify-feedback.sh
bash harness/scripts/feedback-path.sh
```

Expected: OS에 맞는 경로 출력 (예: `/c/Users/khjoo/AppData/Roaming/harness/feedback`)

- [ ] **Step 5: 커밋**

```bash
git add harness/scripts/feedback-path.sh harness/scripts/save-feedback.sh harness/scripts/verify-feedback.sh
git commit -m "feat(harness): 글로벌 피드백 인프라 스크립트 — path/save/verify"
```

---

## Task 4: contract-kaizen 스킬 생성

**Files:**
- Create: `harness/skills/contract-kaizen/SKILL.md`
- Create: `harness/skills/contract-kaizen/references/search-sources.md`
- Create: `harness/skills/contract-kaizen/references/pr-template.md`
- Create: `harness/skills/contract-kaizen/scripts/trigger-check.sh`
- Create: `harness/skills/contract-kaizen/templates/research-log-entry.md`

- [ ] **Step 1: SKILL.md 작성**

```markdown
---
name: contract-kaizen
description: >
  sprint-contract 스킬을 학술 논문·공식 문서·커뮤니티 리서치·글로벌 피드백 기반으로 점진적으로 개선하는 카이젠 스킬.
  계약 설계 원칙(contract-design-guide)과 계약 스키마(contract-schema)도 개선 대상에 포함.
  오케스트레이터 Phase 2로 자동 호출, 피드백 임계치 이벤트 트리거, 또는 수동 호출로 동작한다.
  "/contract-kaizen", "계약 카이젠", "contract 개선" 요청에 사용.
  단순 버그 수정이나 기능 구현 요청에는 트리거하지 않는다.
argument-hint: "[config|skills|guide]"
user-invocable: true
---

# Contract Kaizen

sprint-contract의 계약 작성 품질을 리서치 + 실행 피드백 기반으로 점진적으로 개선한다.

## 이 스킬 폴더의 파일

- `references/search-sources.md` — 검색 소스 + 신뢰도 기준 (계약 설계 11개 + 자기개선 6개 도메인)
- `references/pr-template.md` — PR 본문 + changelog 템플릿
- `scripts/trigger-check.sh` — 피드백 기반 이벤트 트리거 감지
- `templates/research-log-entry.md` — 연구 로그 엔트리 형식

## Gotchas

- 피드백이 0건이면 triage에서 SKIP하지 마라. 리서치 전용 모드로 진행한다 (패턴 분석 생략, search-sources.md 우선순위 상위 3개 도메인만 리서치).
- 리서치 도메인 전체(17개)를 한 번에 검색하지 마라. 피드백 패턴 분석 결과에서 3-5개만 선정한다. 피드백 0건이면 search-sources.md 우선순위 상위 3개만.
- WebFetch로 URL 접근 시 arXiv PDF 직접 접근은 실패할 수 있다. `arxiv.org/abs/` (abstract 페이지)를 사용해라.
- contract-schema.md를 변경하면 evaluator-kaizen(Phase 3)에 영향을 준다. 스키마 변경은 반드시 PR 본문에 명시해라.
- Draft → QA → Apply 순서를 지켜라. 개선안을 파일에 적용하기 전에 QA Evaluator가 DRAFT를 평가해야 한다.
- Regression Smoke Test가 FAIL이면 git revert하고 BLOCKED로 기록한다. 연속 2회 FAIL이면 Phase를 중단하고 사용자에게 알린다.

## 개선 대상

| 영역 | 대상 파일 | 인자 필터 |
|------|----------|----------|
| 가이드 | `docs/guides/contract-design-guide.md` | `guide` |
| 스킬 프롬프트 | `harness/skills/sprint-contract/SKILL.md` | `skills` |
| 계약 스키마 | `harness/references/contract-schema.md` | `config` |

## 트리거 조건

| 트리거 | 조건 |
|--------|------|
| 오케스트레이터 | Phase 2로 자동 호출 |
| 피드백 임계치 | 최근 피드백 10건 중 동일 진단 항목 3회 이상 반복 |
| 수동 | `/contract-kaizen`, `/contract-kaizen guide`, `/contract-kaizen skills` |

## Process

### Step 1: 상태 확인

1. `docs/kaizen/research-log.md`에서 마지막 contract-kaizen 엔트리 확인
2. 트리거 사유 파악 (오케스트레이터 호출 / 피드백 임계치 / 수동)
3. 현재 sprint-contract SKILL.md + contract-design-guide.md 상태 스캔

### Step 2: Triage (피드백 분석)

1. `bash harness/scripts/feedback-path.sh`로 글로벌 피드백 경로 확인
2. `contract/` 하위 YAML 파일 읽기
3. 패턴 분석:
   - 반복 실패 패턴 (동일 diagnosis.checklist 항목이 true인 빈도)
   - 카테고리 편중 (category_coverage가 일관되게 낮은 영역)
   - 복잡도 과소평가 빈도
   - 교차 진단에서 반복 지적되는 문제
4. 피드백이 0건이면 패턴 분석 생략 → 리서치 전용 모드로 Step 3 진행
5. 피드백이 있지만 개선 포인트가 없으면 SKIP + `docs/kaizen/research-log.md`에 "개선 포인트 없음" 기록 후 종료

### Step 3: COLLECT (리서치)

1. `references/search-sources.md` 읽기
2. 피드백 패턴에서 식별된 문제 영역 → 관련 도메인 3-5개 선정
   - 피드백 0건이면: 우선순위 상위 3개 (BDD/Gherkin, Requirements Engineering, Design by Contract)
3. 선정된 도메인별 WebSearch 실행
4. 결과 URL 수집

### Step 4: VERIFY (3-gate 검증)

| Gate | 검증 | 실패 시 |
|------|------|---------|
| GATE 1 | 모든 주장에 URL이 있는가? | URL 없는 주장 폐기 |
| GATE 2 | WebFetch로 URL 접근 + 내용 일치? | 접근 불가 URL 폐기 |
| GATE 3 | PR에 출처 URL + 인용 포함? | PR 작성 시 강제 |

arXiv preprint은 `[preprint]`, 비공식 블로그는 `[blog]`, 6개월 이상은 `[dated: YYYY-MM]` 태그.

### Step 5: GAP 분석 + 예방적 분석

1. **GAP 분석**: 리서치 결과 + 피드백 패턴 + 현재 sprint-contract SKILL.md + contract-design-guide.md 대조
   - 리서치에서 권장하지만 현재 스킬에 없는 것
   - 피드백에서 반복되지만 Gotchas에 없는 패턴
2. **예방적 분석**: 리서치 anti-pattern을 현재 프롬프트에 대조
   - 아직 발생하지 않았지만 발생할 수 있는 취약점
3. 개선점 목록 작성 (가이드 개선 / 스킬 프롬프트 개선 / Gotchas 추가 / 스키마 변경)

### Step 6: Sprint Contract (DRAFT) + 개선안 작성

1. 현재 버전의 sprint-contract로 이번 카이젠의 Sprint Contract 작성
2. 개선안을 DRAFT로 작성 — **파일에 적용하지 않는다**
3. DRAFT를 대화에 출력하여 QA 대상으로 제시

### Step 7: QA + 적용 + Regression

1. 현재 버전의 qa-evaluator로 DRAFT 평가
2. APPROVE:
   - `kaizen-phase-2-pre` git tag 생성
   - 파일에 적용 + 커밋
   - Regression Smoke Test (`harness/evals/kaizen/contract-kaizen/` 활용)
   - Regression PASS → 완료
   - Regression FAIL → `git revert` + BLOCKED
3. REJECT:
   - 피드백 반영 → DRAFT 수정 → 재QA (최대 3회)
   - 3회 REJECT → 사용자 에스컬레이션

### Step 8: 기록

1. `docs/kaizen/research-log.md`에 엔트리 추가 (`templates/research-log-entry.md` 형식)
2. `docs/kaizen/changelog.md`에 변경 기록
3. 버전 bump 판단:
   - patch: docs, Gotchas 추가
   - minor: 스킬 프롬프트 변경, 스키마 변경
   - major: 아키텍처 변경

## 버전 bump 판단 가이드

| 변경 유형 | bump |
|-----------|------|
| contract-design-guide.md만 수정 | patch |
| Gotchas 추가/수정 | patch |
| Process 단계 변경 | minor |
| contract-schema.md 변경 | minor |
| sprint-contract 아키텍처 변경 | major |
```

- [ ] **Step 2: search-sources.md 작성**

```markdown
# 검색 소스 및 신뢰도 기준

> contract-kaizen 전용 리서치 소스. 계약 설계 11개 + 자기개선 6개 도메인.

## 소스 분류

### 학술 (계약 설계)

- **검색 대상:** arXiv, ACL Anthology, IEEE Xplore, Semantic Scholar
- **키워드:** behavior-driven development BDD, acceptance test driven development ATDD, specification by example, design by contract DbC, formal specification TLA+ Alloy, requirements engineering IEEE 29148, LLM formal specification, property-based testing QuickCheck, GQM goal question metric, checklist defect prevention Fagan, consumer-driven contract testing Pact, NASA requirements writing
- **우선순위:** BDD/Gherkin(1), Requirements Engineering(2), Design by Contract(3) — 피드백 0건 시 이 상위 3개만 리서치

### 학술 (자기개선)

- **검색 대상:** arXiv, NeurIPS/ICLR/ACL proceedings
- **키워드:** LLM self-refine reflection, meta-learning learning to learn, retrospective post-mortem analysis, PDCA continuous improvement, LLM self-correction limits, experience replay feedback reuse
- **범위:** 2024-현재

### 공식

- **검색 대상:** Anthropic (docs, blog, research), OpenAI (cookbook, blog), Google (research, Vertex docs)
- **키워드:** prompt engineering best practices, specification, acceptance criteria, quality gates, agentic workflow
- **후속:** 변경 로그 / 릴리스 노트 확인

### 커뮤니티

- **검색 대상:** GitHub trending, Simon Willison blog, Lilian Weng blog, Eugene Yan blog
- **키워드:** contract testing, specification driven development, BDD tooling, requirement quality
- **후속:** star 수 + 최근 커밋으로 신뢰도 판단

## 신뢰도 기준

| 유형 | 신뢰도 | 태그 | 비고 |
|------|--------|------|------|
| 학회 논문 (peer-reviewed) | 높음 | — | NeurIPS, ICLR, ACL, EMNLP, ICSE, FSE |
| 공식 블로그/문서 | 높음 | — | Anthropic, OpenAI, Google |
| arXiv preprint | 중간 | `[preprint]` | 인용 수 확인 |
| 엔지니어 블로그 | 중간 | `[blog]` | 저자 신뢰도 확인 |
| GitHub trending | 중간 | `[community]` | star + 활동성 확인 |
| 일반 블로그/포럼 | 낮음 | `[unverified]` | 교차 검증 필수 |

## 최신성 기준

- 6개월 이내: 현행
- 6-12개월: `[dated: YYYY-MM]` 태그 부착
- 12개월 초과: 기본 원칙이 아니면 폐기

## 중복 방지

- `docs/kaizen/research-log.md`에서 이미 조사한 URL 확인
- 동일 URL은 재조사하지 않음 (6개월 이상 경과 시 예외)
```

- [ ] **Step 3: pr-template.md 작성**

harness-kaizen의 `references/pr-template.md`와 동일 형식. contract-kaizen 컨텍스트에 맞게 영역명만 변경.

```markdown
# Contract Kaizen PR 본문 템플릿

> SKILL.md에서 PR 생성 시 이 템플릿을 따른다.

## PR 본문 템플릿

~~~markdown
## Research Summary
> {One-line summary of contract design improvement}

### 조사한 소스
- [Title](URL) `[Type]` — {Brief summary}

### 핵심 발견
- Finding: {Specific description + citation}

---

## Changes

### 1. [Change Name]

**영역:** guide / skills / config
**버전 영향:** patch / minor / major

**Before:**
```
{현재 코드/설정}
```

**After:**
```
{변경된 코드/설정}
```

**왜 개선인가:**
- 장점: ...
- 단점/트레이드오프: ...
- 근거: [출처](URL)

---

## Impact Summary

| 항목 | 영향도 | 리스크 | 근거 |
|------|--------|--------|------|

---

## Version Bump

**유형:** patch / minor / major
**현재:** vX.Y.Z → **다음:** vX.Y.Z
**판단 근거:** ...

---

## Source Reliability

| 출처 | 유형 | 신뢰도 | 최신성 |
|------|------|--------|--------|
~~~

## changelog.md 엔트리 형식

~~~markdown
## [X.Y.Z] - YYYY-MM-DD

### 변경 유형: patch/minor/major (contract-kaizen)

### 연구 기반
- [제목](URL) — {Insight}

### 변경 내역
- **파일경로**: {Description}
  - Before: {Old}
  - After: {New}
  - 근거: [출처](URL)

### 버전 판단 근거
> {Why this bump type}
~~~
```

- [ ] **Step 4: trigger-check.sh 작성**

```bash
#!/usr/bin/env bash
set -eo pipefail

# contract-kaizen 이벤트 트리거 감지.
# 글로벌 피드백에서 반복 패턴을 확인한다.
#
# Usage: bash trigger-check.sh
# Exit: 0 = 트리거 발견, 1 = 트리거 없음, 2 = 에러

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FEEDBACK_DIR="$(bash "$SCRIPT_DIR/../../scripts/feedback-path.sh")/contract"

trigger_found() {
  echo "TRIGGER: $1"
  exit 0
}

# 피드백 디렉토리 존재 확인
if [[ ! -d "$FEEDBACK_DIR" ]]; then
  echo "NO_FEEDBACK_DIR"
  exit 1
fi

# 최근 10개 파일
RECENT_FILES=$(ls -t "$FEEDBACK_DIR"/*.yaml 2>/dev/null | head -10)
if [[ -z "$RECENT_FILES" ]]; then
  echo "NO_FEEDBACK_FILES"
  exit 1
fi

FILE_COUNT=$(echo "$RECENT_FILES" | wc -l)
if [[ "$FILE_COUNT" -lt 3 ]]; then
  echo "INSUFFICIENT_DATA: ${FILE_COUNT} files (need 3+)"
  exit 1
fi

# 진단 체크리스트에서 반복 패턴 확인
# 동일 항목이 3회 이상 true이면 트리거
if command -v yq &>/dev/null; then
  for field in ambiguous_conditions missing_error_paths untestable_conditions category_coverage_gap complexity_underestimate; do
    COUNT=0
    for f in $RECENT_FILES; do
      VAL=$(yq ".diagnosis.checklist.${field}" "$f" 2>/dev/null)
      if [[ "$VAL" == "true" ]]; then
        COUNT=$((COUNT + 1))
      fi
    done
    if [[ "$COUNT" -ge 3 ]]; then
      trigger_found "진단 항목 '${field}'가 최근 ${FILE_COUNT}건 중 ${COUNT}건 반복"
    fi
  done
fi

echo "NO_TRIGGER"
exit 1
```

- [ ] **Step 5: research-log-entry.md 작성**

```markdown
# 연구 로그 엔트리 템플릿

> SKILL.md에서 research-log.md에 contract-kaizen 엔트리 추가 시 이 형식을 따른다.

## 형식

~~~markdown
## YYYY-MM-DD (contract-kaizen)

**트리거:** orchestrator-phase-2 / feedback-threshold (사유) / manual (영역)
**피드백 분석:** {분석된 피드백 건수}건, 주요 패턴: {패턴 요약}

### 조사한 소스

| # | 제목 | URL | 유형 | 신뢰도 | 결과 |
|---|------|-----|------|--------|------|
| 1 | Title | URL | peer-reviewed/공식/blog/community | 높음/중간/낮음 | 채택/폐기 |

### 채택한 인사이트

- **인사이트 1:** {Description} — 적용 영역: guide/skills/config

### 폐기 사유 (해당 시)

- **소스 N:** {Reason}

### 개선 적용

- 대상: {파일 경로}
- 변경: {요약}
- 버전: vX.Y.Z → vX.Y.Z

### PR

- PR URL 또는 "개선 포인트 없음"
~~~
```

- [ ] **Step 6: 커밋**

```bash
git add harness/skills/contract-kaizen/
git commit -m "feat(harness): contract-kaizen 스킬 생성 — 계약 설계 리서치 기반 자기개선"
```

---

## Task 5: evaluator-kaizen 스킬 생성

**Files:**
- Create: `harness/skills/evaluator-kaizen/SKILL.md`
- Create: `harness/skills/evaluator-kaizen/references/search-sources.md`
- Create: `harness/skills/evaluator-kaizen/references/pr-template.md`
- Create: `harness/skills/evaluator-kaizen/scripts/trigger-check.sh`
- Create: `harness/skills/evaluator-kaizen/templates/research-log-entry.md`

- [ ] **Step 1: SKILL.md 작성**

```markdown
---
name: evaluator-kaizen
description: >
  qa-evaluator 에이전트를 학술 논문·공식 문서·커뮤니티 리서치·글로벌 피드백 기반으로 점진적으로 개선하는 카이젠 스킬.
  평가 방법론 가이드(qa-evaluation-guide)도 개선 대상에 포함.
  오케스트레이터 Phase 3으로 자동 호출, 피드백 임계치 이벤트 트리거, 또는 수동 호출로 동작한다.
  "/evaluator-kaizen", "평가자 카이젠", "evaluator 개선" 요청에 사용.
  단순 버그 수정이나 기능 구현 요청에는 트리거하지 않는다.
argument-hint: "[skills|guide]"
user-invocable: true
---

# Evaluator Kaizen

qa-evaluator의 평가 품질을 리서치 + 실행 피드백 기반으로 점진적으로 개선한다.

## 이 스킬 폴더의 파일

- `references/search-sources.md` — 검색 소스 + 신뢰도 기준 (평가 방법론 12개 + 자기개선 6개 도메인)
- `references/pr-template.md` — PR 본문 + changelog 템플릿
- `scripts/trigger-check.sh` — 피드백 기반 이벤트 트리거 감지
- `templates/research-log-entry.md` — 연구 로그 엔트리 형식

## Gotchas

- 피드백이 0건이면 triage에서 SKIP하지 마라. 리서치 전용 모드로 진행한다 (패턴 분석 생략, search-sources.md 우선순위 상위 3개 도메인만 리서치).
- 리서치 도메인 전체(18개)를 한 번에 검색하지 마라. 피드백 패턴 분석 결과에서 3-5개만 선정한다. 피드백 0건이면 search-sources.md 우선순위 상위 3개만.
- WebFetch로 URL 접근 시 arXiv PDF 직접 접근은 실패할 수 있다. `arxiv.org/abs/` (abstract 페이지)를 사용해라.
- Phase 2(contract-kaizen)에서 contract-schema.md가 변경되었는지 확인해라. 변경 시 평가 루브릭에 새 필드 반영 필수.
- Draft → QA → Apply 순서를 지켜라. 개선안을 파일에 적용하기 전에 QA Evaluator가 DRAFT를 평가해야 한다.
- qa-evaluator 자체를 개선하는 Phase에서 QA는 **현재(구) 버전** evaluator로 수행한다. 개선된 버전으로 자기 자신을 QA하지 마라.
- Regression Smoke Test가 FAIL이면 git revert하고 BLOCKED로 기록한다. 연속 2회 FAIL이면 Phase를 중단하고 사용자에게 알린다.

## 개선 대상

| 영역 | 대상 파일 | 인자 필터 |
|------|----------|----------|
| 가이드 | `docs/guides/qa-evaluation-guide.md` | `guide` |
| 에이전트 프롬프트 | `harness/agents/qa-evaluator.md` | `skills` |

## 트리거 조건

| 트리거 | 조건 |
|--------|------|
| 오케스트레이터 | Phase 3으로 자동 호출 |
| 피드백 임계치 | 최근 피드백 10건 중 동일 진단 항목 3회 이상 반복 |
| 수동 | `/evaluator-kaizen`, `/evaluator-kaizen guide`, `/evaluator-kaizen skills` |

## Process

### Step 1: 상태 확인

1. `docs/kaizen/research-log.md`에서 마지막 evaluator-kaizen 엔트리 확인
2. 트리거 사유 파악
3. 현재 qa-evaluator.md + qa-evaluation-guide.md 상태 스캔
4. `harness/references/contract-schema.md` 최근 변경 여부 확인 (Phase 2에서 변경되었을 수 있음)

### Step 2: Triage (피드백 분석)

1. `bash harness/scripts/feedback-path.sh`로 글로벌 피드백 경로 확인
2. `evaluator/` 하위 YAML 파일 읽기
3. 패턴 분석:
   - L3 미도달 빈도 (l3_coverage가 일관되게 낮은 패턴)
   - REJECT 반복 패턴 (동일 reject_reasons)
   - False APPROVE 징후 (APPROVE 후 관련 영역에서 버그 보고)
   - 편향 감지 빈도
   - 교차 진단에서 반복 지적되는 문제
4. 피드백이 0건이면 패턴 분석 생략 → 리서치 전용 모드로 Step 3 진행
5. 피드백이 있지만 개선 포인트가 없으면 SKIP + 로그 기록 후 종료

### Step 3: COLLECT (리서치)

1. `references/search-sources.md` 읽기
2. 피드백 패턴에서 식별된 문제 영역 → 관련 도메인 3-5개 선정
   - 피드백 0건이면: 우선순위 상위 3개 (LLM-as-a-Judge, Rubric-Based Evaluation, Test Oracle Problem)
3. contract-schema.md 변경이 있으면: 해당 변경에 관련된 도메인 우선 추가
4. 선정된 도메인별 WebSearch 실행
5. 결과 URL 수집

### Step 4: VERIFY (3-gate 검증)

| Gate | 검증 | 실패 시 |
|------|------|---------|
| GATE 1 | 모든 주장에 URL이 있는가? | URL 없는 주장 폐기 |
| GATE 2 | WebFetch로 URL 접근 + 내용 일치? | 접근 불가 URL 폐기 |
| GATE 3 | PR에 출처 URL + 인용 포함? | PR 작성 시 강제 |

### Step 5: GAP 분석 + 예방적 분석

1. **GAP 분석**: 리서치 결과 + 피드백 패턴 + 현재 qa-evaluator.md + qa-evaluation-guide.md 대조
2. **예방적 분석**: 리서치 anti-pattern을 현재 에이전트 프롬프트에 대조
3. **스키마 변경 반영**: contract-schema.md에 새 필드가 추가되었으면 평가 루브릭에 반영 포인트 추가
4. 개선점 목록 작성

### Step 6: Sprint Contract (DRAFT) + 개선안 작성

1. 현재 버전의 sprint-contract로 Sprint Contract 작성
2. 개선안을 DRAFT로 작성 — **파일에 적용하지 않는다**
3. DRAFT를 대화에 출력하여 QA 대상으로 제시

### Step 7: QA + 적용 + Regression

1. **현재(구) 버전**의 qa-evaluator로 DRAFT 평가
2. APPROVE:
   - `kaizen-phase-3-pre` git tag 생성
   - 파일에 적용 + 커밋
   - Regression Smoke Test (`harness/evals/kaizen/evaluator-kaizen/` 활용)
   - Regression PASS → 완료
   - Regression FAIL → `git revert` + BLOCKED
3. REJECT: 피드백 반영 → 재QA (최대 3회) → 3회 시 에스컬레이션

### Step 8: 기록

1. `docs/kaizen/research-log.md`에 엔트리 추가
2. `docs/kaizen/changelog.md`에 변경 기록
3. 버전 bump 판단

## 버전 bump 판단 가이드

| 변경 유형 | bump |
|-----------|------|
| qa-evaluation-guide.md만 수정 | patch |
| Gotchas 추가/수정 | patch |
| 검증 레벨/루브릭 변경 | minor |
| 판정 로직 구조 변경 | major |
```

- [ ] **Step 2: search-sources.md 작성**

```markdown
# 검색 소스 및 신뢰도 기준

> evaluator-kaizen 전용 리서치 소스. 평가 방법론 12개 + 자기개선 6개 도메인.

## 소스 분류

### 학술 (평가 방법론)

- **검색 대상:** arXiv, ACL Anthology, IEEE Xplore, ACM Digital Library, Semantic Scholar
- **키워드:** test oracle problem LLM, LLM-as-a-judge evaluation bias, rubric-based LLM evaluation CheckEval, multi-agent verification consensus, metamorphic testing oracle, mutation testing LLM, independent verification validation IV&V, Fagan inspection perspective-based reading, symbolic execution concolic testing LLM, N-version programming diverse redundancy, evidence-based software engineering, automated code review AI-assisted
- **우선순위:** LLM-as-a-Judge(1), Rubric-Based Evaluation(2), Test Oracle Problem(3) — 피드백 0건 시 이 상위 3개만 리서치

### 학술 (자기개선)

- **검색 대상:** arXiv, NeurIPS/ICLR/ACL proceedings
- **키워드:** LLM self-refine reflection, meta-learning learning to learn, retrospective post-mortem analysis, PDCA continuous improvement, LLM self-correction limits, experience replay feedback reuse
- **범위:** 2024-현재

### 공식

- **검색 대상:** Anthropic (docs, blog, research), OpenAI (cookbook, blog), Google (research, Vertex docs)
- **키워드:** LLM evaluation, judge model, automated review, code verification, quality assurance
- **후속:** 변경 로그 / 릴리스 노트 확인

### 커뮤니티

- **검색 대상:** GitHub trending, Simon Willison blog, Lilian Weng blog, Eugene Yan blog
- **키워드:** LLM judge, automated QA, code review tools, evaluation frameworks
- **후속:** star 수 + 최근 커밋으로 신뢰도 판단

## 신뢰도 기준

| 유형 | 신뢰도 | 태그 | 비고 |
|------|--------|------|------|
| 학회 논문 (peer-reviewed) | 높음 | — | NeurIPS, ICLR, ACL, EMNLP, ICSE, FSE |
| 공식 블로그/문서 | 높음 | — | Anthropic, OpenAI, Google |
| arXiv preprint | 중간 | `[preprint]` | 인용 수 확인 |
| 엔지니어 블로그 | 중간 | `[blog]` | 저자 신뢰도 확인 |
| GitHub trending | 중간 | `[community]` | star + 활동성 확인 |
| 일반 블로그/포럼 | 낮음 | `[unverified]` | 교차 검증 필수 |

## 최신성 기준

- 6개월 이내: 현행
- 6-12개월: `[dated: YYYY-MM]` 태그 부착
- 12개월 초과: 기본 원칙이 아니면 폐기

## 중복 방지

- `docs/kaizen/research-log.md`에서 이미 조사한 URL 확인
- 동일 URL은 재조사하지 않음 (6개월 이상 경과 시 예외)
```

- [ ] **Step 3: pr-template.md 작성**

contract-kaizen의 pr-template.md와 동일 구조. 제목만 "Evaluator Kaizen PR 본문 템플릿"으로 변경, 영역을 `guide / skills`로 변경.

- [ ] **Step 4: trigger-check.sh 작성**

contract-kaizen의 trigger-check.sh와 동일 구조. 변경점:
- `FEEDBACK_DIR` 경로: `contract` → `evaluator`
- 체크 필드: `l3_unreached`, `bias_detected`, `evidence_missing`, `contract_misinterpret`, `perspective_gap`

```bash
#!/usr/bin/env bash
set -eo pipefail

# evaluator-kaizen 이벤트 트리거 감지.
#
# Usage: bash trigger-check.sh
# Exit: 0 = 트리거 발견, 1 = 트리거 없음, 2 = 에러

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FEEDBACK_DIR="$(bash "$SCRIPT_DIR/../../scripts/feedback-path.sh")/evaluator"

trigger_found() {
  echo "TRIGGER: $1"
  exit 0
}

if [[ ! -d "$FEEDBACK_DIR" ]]; then
  echo "NO_FEEDBACK_DIR"
  exit 1
fi

RECENT_FILES=$(ls -t "$FEEDBACK_DIR"/*.yaml 2>/dev/null | head -10)
if [[ -z "$RECENT_FILES" ]]; then
  echo "NO_FEEDBACK_FILES"
  exit 1
fi

FILE_COUNT=$(echo "$RECENT_FILES" | wc -l)
if [[ "$FILE_COUNT" -lt 3 ]]; then
  echo "INSUFFICIENT_DATA: ${FILE_COUNT} files (need 3+)"
  exit 1
fi

if command -v yq &>/dev/null; then
  for field in l3_unreached bias_detected evidence_missing contract_misinterpret perspective_gap; do
    COUNT=0
    for f in $RECENT_FILES; do
      VAL=$(yq ".diagnosis.checklist.${field}" "$f" 2>/dev/null)
      if [[ "$VAL" == "true" ]]; then
        COUNT=$((COUNT + 1))
      fi
    done
    if [[ "$COUNT" -ge 3 ]]; then
      trigger_found "진단 항목 '${field}'가 최근 ${FILE_COUNT}건 중 ${COUNT}건 반복"
    fi
  done
fi

echo "NO_TRIGGER"
exit 1
```

- [ ] **Step 5: research-log-entry.md 작성**

contract-kaizen의 research-log-entry.md와 동일 형식. 제목 라인만 `(evaluator-kaizen)`으로 변경.

- [ ] **Step 6: 커밋**

```bash
git add harness/skills/evaluator-kaizen/
git commit -m "feat(harness): evaluator-kaizen 스킬 생성 — 평가 방법론 리서치 기반 자기개선"
```

---

## Task 6: sprint-contract 수정 (자기진단 + 피드백 hard gate)

**Files:**
- Modify: `harness/skills/sprint-contract/SKILL.md`

- [ ] **Step 1: 현재 sprint-contract SKILL.md 읽기**

```bash
# 현재 파일 전체 확인 — Gotchas 위치, 마지막 Process 단계 번호, References 섹션 확인
```

- [ ] **Step 2: Gotchas 최상단에 hard gate 추가**

기존 Gotchas 섹션의 첫 번째 항목 앞에 추가:

```markdown
- verify-feedback.sh가 PASS를 반환하지 않으면 절대 완료를 선언하지 마라. 이것은 선택이 아니다.
```

- [ ] **Step 3: References 섹션에 가이드 추가**

기존 References 목록에 추가:

```markdown
- `docs/guides/contract-design-guide.md` — 계약 작성 원칙 가이드
- `harness/references/contract-schema.md` — 계약 포맷 공유 정의
- `harness/references/feedback-schema.yaml` — 피드백 YAML 스키마
```

- [ ] **Step 4: Process 마지막에 자기진단 + 피드백 단계 추가**

기존 마지막 Step (계약 저장) 이후에 추가:

```markdown
### Step {N+1}: 자기진단

1. 구조화 체크리스트 실행:
   - `ambiguous_conditions`: 모호한 표현이 포함된 조건이 있는가?
   - `missing_error_paths`: 에러/예외 경로에 대한 조건이 누락되었는가?
   - `untestable_conditions`: 코드만으로 검증 불가능한 조건이 있는가?
   - `category_coverage_gap`: project.yaml 카테고리 중 커버하지 못한 것이 있는가?
   - `complexity_underestimate`: 복잡도를 과소평가하여 조건 수가 부족한가?
2. 각 항목에 대해 true/false 판정

### Step {N+2}: 교차 진단

1. Agent tool로 qa-evaluator 서브에이전트를 호출한다
2. 전달 내용: 생성된 계약 조건 전문 (`.harness/sprint-contract.md` 내용)
3. 미전달: 사용자 대화 내용, 의사결정 과정
4. 핵심 질문: "이 조건들을 독립적으로 검증할 수 있는가? 모호하거나 해석이 갈리는 조건이 있는가?"
5. 서브에이전트 응답을 `cross_diagnosis_notes`로 기록

### Step {N+3}: 피드백 저장

1. 자기진단 + 교차 진단 결과를 합쳐 피드백 YAML을 `.harness/feedback-draft.yaml`에 작성한다
   - `harness/references/feedback-schema.yaml`의 스키마를 따른다
   - `skill: sprint-contract`
   - `project_hash`: 현재 프로젝트 경로의 SHA-256 앞 8자 (`echo -n "$(pwd)" | sha256sum | cut -c1-8`)
   - `diagnosis.checklist`: Step {N+1}의 결과
   - `diagnosis.cross_diagnosis_by: qa-evaluator`
   - `diagnosis.cross_diagnosis_notes`: Step {N+2}의 결과
2. `bash harness/scripts/save-feedback.sh contract .harness/feedback-draft.yaml` 실행
3. 출력된 저장 경로를 기록한다

### Step {N+4}: 피드백 검증

1. `bash harness/scripts/verify-feedback.sh {Step N+3에서 출력된 경로}` 실행
2. PASS → 스킬 완료
3. FAIL → 피드백 YAML 수정 후 Step {N+3}부터 재시도
```

- [ ] **Step 5: 커밋**

```bash
git add harness/skills/sprint-contract/SKILL.md
git commit -m "feat(sprint-contract): 자기진단 + 교차 진단 + 글로벌 피드백 hard gate 추가"
```

---

## Task 7: qa-evaluator 수정 (자기진단 + 피드백 hard gate)

**Files:**
- Modify: `harness/agents/qa-evaluator.md`

- [ ] **Step 1: 현재 qa-evaluator.md 읽기**

```bash
# 현재 파일 전체 확인 — Gotchas 위치 (또는 Red Flags), 마지막 Process 단계, References 확인
```

- [ ] **Step 2: Gotchas/Red Flags 섹션 최상단에 hard gate 추가**

```markdown
- verify-feedback.sh가 PASS를 반환하지 않으면 절대 완료를 선언하지 마라. 이것은 선택이 아니다.
```

- [ ] **Step 3: References에 가이드 추가**

```markdown
- `docs/guides/qa-evaluation-guide.md` — 평가 방법론 가이드
- `harness/references/contract-schema.md` — 계약 포맷 공유 정의
- `harness/references/feedback-schema.yaml` — 피드백 YAML 스키마
```

- [ ] **Step 4: Process 마지막에 자기진단 + 피드백 단계 추가**

기존 마지막 Step (판정 출력) 이후에 추가:

```markdown
### Step {N+1}: 자기진단

1. 구조화 체크리스트 실행:
   - `l3_unreached`: L3 검증에 도달하지 못한 조건이 있는가?
   - `bias_detected`: 편향 징후가 감지되었는가? (너무 관대, 증거 없이 PASS)
   - `evidence_missing`: 증거 없이 판정한 조건이 있는가?
   - `contract_misinterpret`: 계약 조건을 원래 의도와 다르게 해석했을 가능성이 있는가?
   - `perspective_gap`: 단일 관점에서만 평가한 조건이 있는가?
2. 각 항목에 대해 true/false 판정

### Step {N+2}: 교차 진단

1. Agent tool로 sprint-contract 서브에이전트를 호출한다
2. 전달 내용: 평가 판정 결과 전문 (APPROVE/REJECT + 각 조건별 PASS/FAIL + 증거)
3. 미전달: 평가 과정의 추론, 중간 메모
4. 핵심 질문: "계약 조건의 원래 의도를 정확히 해석했는가? 잘못 해석하여 PASS/FAIL을 오판한 조건이 있는가?"
5. 서브에이전트 응답을 `cross_diagnosis_notes`로 기록

### Step {N+3}: 피드백 저장

1. 자기진단 + 교차 진단 결과를 합쳐 피드백 YAML을 `.harness/feedback-draft.yaml`에 작성한다
   - `skill: qa-evaluator`
   - `evaluation.verdict`: 이번 판정 결과
   - `evaluation.conditions_total`: 전체 조건 수
   - `evaluation.conditions_passed`: PASS 조건 수
   - `evaluation.l3_coverage`: L3 검증 도달 비율
   - `evaluation.reject_reasons`: REJECT 시 사유 목록
   - `diagnosis.checklist`: Step {N+1}의 결과
   - `diagnosis.cross_diagnosis_by: sprint-contract`
2. `bash harness/scripts/save-feedback.sh evaluator .harness/feedback-draft.yaml` 실행
3. 출력된 저장 경로를 기록한다

### Step {N+4}: 피드백 검증

1. `bash harness/scripts/verify-feedback.sh {Step N+3에서 출력된 경로}` 실행
2. PASS → 에이전트 완료
3. FAIL → 피드백 YAML 수정 후 Step {N+3}부터 재시도
```

- [ ] **Step 5: 커밋**

```bash
git add harness/agents/qa-evaluator.md
git commit -m "feat(qa-evaluator): 자기진단 + 교차 진단 + 글로벌 피드백 hard gate 추가"
```

---

## Task 8: 카이젠 오케스트레이터 재구성

**Files:**
- Modify: `.claude/skills/kaizen-orchestrator/SKILL.md`

- [ ] **Step 1: 현재 오케스트레이터 SKILL.md 읽기**

- [ ] **Step 2: Phase 의존성 재구성**

기존 Phase 의존성 섹션을 다음으로 교체:

```markdown
## Phase 의존성

```
Phase 1: 설계 가이드 카이젠
    ↓
Phase 2: Contract 카이젠 (contract-kaizen)
    ↓
Phase 3: Evaluator 카이젠 (evaluator-kaizen)
    ↓
Phase 4: Harness 카이젠 (harness-kaizen)
    ↓
Phase 5: Flutter-toolkit 카이젠 (flutter-kaizen)
    ↓
Phase 6: Design-kit 카이젠 (design-kaizen)
    ↓
Final: 전체 정합성 검증
```

### Phase 순서 논리

1. 설계 가이드가 최상위 — 모든 스킬/에이전트 설계의 기준
2. Contract 카이젠 — 계약 작성 원칙 개선 (contract-design-guide + sprint-contract)
3. Evaluator 카이젠 — 평가 방법론 개선 (qa-evaluation-guide + qa-evaluator). Phase 2에서 contract-schema 변경 시 반영.
4. Harness 카이젠 — sprint-contract, qa-evaluator **제외**한 나머지 harness 스킬/설정 (sprint-feedback, init, project.yaml, procedures)
5. Flutter-toolkit 카이젠 — Flutter 스킬 개선
6. Design-kit 카이젠 — UI/UX 디자인 스킬 개선
```

- [ ] **Step 3: 공유 리서치 Step 0 제거 + 각 Phase 자체 리서치로 교체**

기존 "Step 0: RESEARCH" 섹션을 제거하고, 각 Phase 실행 패턴을 다음으로 교체:

```markdown
## 각 Phase 공통 실행 패턴

각 Phase는 **새 서브에이전트**로 실행한다 (Agent tool). 이전 Phase의 변경사항이 디스크에 커밋되어 있으므로 fresh load로 반영된다.

```
1. Triage: 피드백 읽기 → 개선 필요? → 불필요 시 SKIP + 로그
   ⚠ 피드백이 0건이면 SKIP하지 않고 리서치 전용 모드로 진행
2. 자체 리서치: 해당 스킬의 search-sources.md 기반, 3-5개 도메인만
3. GAP 분석: 리서치 + 피드백 + 현재 스킬/가이드 대조
4. 예방적 분석: 리서치 anti-pattern을 현재 프롬프트에 대조
5. Sprint Contract (DRAFT): 현재 버전 sprint-contract 사용
6. 개선안 DRAFT 작성 (파일 미적용)
7. QA Evaluator: 현재 버전으로 DRAFT 평가
8. APPROVE → kaizen-phase-N-pre 태그 생성 → 파일 적용 + 커밋 → Regression Smoke Test
9. Regression 실패 → git revert (kaizen-phase-N-pre 태그) → BLOCKED
10. 다음 Phase → 새 서브에이전트 (fresh load)
```
```

- [ ] **Step 4: Gotchas 업데이트**

기존 Gotchas에서 "리서치는 Phase 1에서 한 번만 수행하고 전 Phase에서 공유" 제거. 다음 추가:

```markdown
- 각 Phase의 리서치는 해당 카이젠 스킬이 자체 수행한다. 오케스트레이터는 순서만 관리한다.
- Phase 4(harness-kaizen)는 sprint-contract와 qa-evaluator를 개선 대상에서 제외한다. 이 둘은 Phase 2, 3에서 처리한다.
- 피드백이 0건인 Phase도 SKIP하지 않는다. 리서치 전용 모드로 진행한다.
- Regression 실패 카운터는 `.harness/.meta/kaizen-failure-count.yaml`에 Phase별로 영속화한다. 연속 2회 FAIL 시 해당 Phase를 일시 중단하고 사용자에게 알린다.
- 정리 정책(6개월 초과 삭제, 500개 제한)은 모든 Phase 완료 후 Final 단계에서 실행한다. 분석 중 데이터 손실을 방지한다.
```

- [ ] **Step 5: Final 단계에 정리 정책 추가**

기존 Final 단계에 추가:

```markdown
### 글로벌 피드백 정리

1. `bash harness/scripts/feedback-path.sh`로 경로 확인
2. 6개월 초과 파일 삭제 (oldest-first)
3. 500개 초과 시 oldest-first로 삭감
4. 정리 로그를 `.meta/cleanup-log.yaml`에 기록
```

- [ ] **Step 6: 커밋**

```bash
git add .claude/skills/kaizen-orchestrator/SKILL.md
git commit -m "refactor(orchestrator): 6 Phase 재구성 + 자체 리서치 분산 + triage/regression"
```

---

## Task 9: 메타 Eval Fixture 생성

**Files:**
- Create: `harness/evals/kaizen/contract-kaizen/fixture-feedback-data/ambiguous-conditions.yaml`
- Create: `harness/evals/kaizen/contract-kaizen/fixture-feedback-data/category-bias.yaml`
- Create: `harness/evals/kaizen/contract-kaizen/fixture-feedback-data/low-coverage.yaml`
- Create: `harness/evals/kaizen/contract-kaizen/expected-improvements.md`
- Create: `harness/evals/kaizen/contract-kaizen/assertions.json`
- Create: `harness/evals/kaizen/evaluator-kaizen/fixture-feedback-data/l3-miss.yaml`
- Create: `harness/evals/kaizen/evaluator-kaizen/fixture-feedback-data/false-approve.yaml`
- Create: `harness/evals/kaizen/evaluator-kaizen/fixture-feedback-data/reject-loop.yaml`
- Create: `harness/evals/kaizen/evaluator-kaizen/expected-improvements.md`
- Create: `harness/evals/kaizen/evaluator-kaizen/assertions.json`
- Create: `harness/evals/kaizen/feedback-system/save-test.sh`
- Create: `harness/evals/kaizen/feedback-system/aggregation-test.sh`

- [ ] **Step 1: contract-kaizen fixture — ambiguous-conditions.yaml**

```yaml
schema_version: 1
timestamp: "2026-03-15T10:00:00+09:00"
project_hash: "test0001"
project_name: "fixture-project-a"
skill: sprint-contract
skill_version: "0.3.3"
outcome: completed
contract:
  condition_count: 6
  category_count: 3
  category_coverage: 0.6
  anti_pattern_count: 2
  complexity: medium
diagnosis:
  checklist:
    ambiguous_conditions: true
    missing_error_paths: false
    untestable_conditions: true
    category_coverage_gap: false
    complexity_underestimate: false
  cross_diagnosis_by: qa-evaluator
  cross_diagnosis_notes: "조건 2, 5번이 모호함 — '적절히 표시한다' 표현 사용"
  improvement_suggestions:
    - "모호 조건 탐지 규칙을 Gotchas에 추가"
user_rating: null
user_comment: null
```

- [ ] **Step 2: contract-kaizen fixture — category-bias.yaml, low-coverage.yaml**

category-bias.yaml: `category_coverage: 0.4`, `category_coverage_gap: true` 3건 반복 패턴
low-coverage.yaml: `condition_count: 3`, `complexity_underestimate: true` 패턴

(동일 스키마, checklist 값만 변경)

- [ ] **Step 3: contract-kaizen expected-improvements.md**

```markdown
# Contract-Kaizen Expected Improvements

## fixture: ambiguous-conditions

ambiguous_conditions가 반복될 때 기대하는 개선:

- [ ] sprint-contract SKILL.md Gotchas에 모호 조건 감지 규칙이 추가되어야 한다
- [ ] contract-design-guide.md에 모호 표현 목록(적절히, 충분히, 잘)이 명시되어야 한다

## fixture: category-bias

category_coverage_gap가 반복될 때 기대하는 개선:

- [ ] sprint-contract Process에 카테고리 균형 검증 단계가 추가되어야 한다
- [ ] contract-design-guide.md에 GQM 기반 카테고리 도출 절차가 구체화되어야 한다

## fixture: low-coverage

complexity_underestimate가 반복될 때 기대하는 개선:

- [ ] sprint-contract Gotchas에 복잡도 판단 기준 강화가 추가되어야 한다
- [ ] 최소 조건 수 하한선이 복잡도별로 명시되어야 한다
```

- [ ] **Step 4: contract-kaizen assertions.json**

```json
{
  "ambiguous-conditions": [
    {"type": "file_contains", "file": "harness/skills/sprint-contract/SKILL.md", "pattern": "모호.*감지|ambiguous.*detect"},
    {"type": "file_contains", "file": "docs/guides/contract-design-guide.md", "pattern": "적절히|충분히|잘"}
  ],
  "category-bias": [
    {"type": "file_contains", "file": "harness/skills/sprint-contract/SKILL.md", "pattern": "카테고리.*균형|category.*balance"}
  ],
  "low-coverage": [
    {"type": "file_contains", "file": "harness/skills/sprint-contract/SKILL.md", "pattern": "복잡도.*판단|complexity.*judge"}
  ]
}
```

- [ ] **Step 5: evaluator-kaizen fixture 3개 + expected-improvements.md + assertions.json**

l3-miss.yaml: `l3_unreached: true` 반복
false-approve.yaml: `bias_detected: true` 반복
reject-loop.yaml: `contract_misinterpret: true` 반복

expected-improvements.md: 각 fixture별 기대 개선 체크리스트
assertions.json: 각 fixture별 파일 내용 검증 규칙

- [ ] **Step 6: feedback-system/save-test.sh**

```bash
#!/usr/bin/env bash
set -eo pipefail

# 피드백 저장 시스템 통합 테스트
# 가짜 YAML을 생성하고 save → verify 파이프라인 검증

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HARNESS_SCRIPTS="$SCRIPT_DIR/../../../scripts"

echo "=== Feedback System Test ==="

# 1. 테스트용 draft 생성
DRAFT="/tmp/test-feedback-draft.yaml"
cat > "$DRAFT" <<'YAML'
schema_version: 1
timestamp: "2026-03-30T10:00:00+09:00"
project_hash: "testtest"
project_name: "test-project"
skill: sprint-contract
skill_version: "0.3.3"
outcome: completed
contract:
  condition_count: 5
  category_count: 3
  category_coverage: 0.75
  anti_pattern_count: 2
  complexity: simple
diagnosis:
  checklist:
    ambiguous_conditions: false
    missing_error_paths: false
    untestable_conditions: false
    category_coverage_gap: false
    complexity_underestimate: false
  cross_diagnosis_by: qa-evaluator
  cross_diagnosis_notes: "테스트 — 문제 없음"
  improvement_suggestions: []
user_rating: null
user_comment: null
YAML

# 2. save 실행
echo "--- save-feedback.sh ---"
SAVED_PATH=$(bash "$HARNESS_SCRIPTS/save-feedback.sh" contract "$DRAFT")
echo "Saved to: $SAVED_PATH"

if [[ -z "$SAVED_PATH" ]]; then
  echo "FAIL: save-feedback.sh returned empty path"
  exit 1
fi

# 3. verify 실행
echo "--- verify-feedback.sh ---"
RESULT=$(bash "$HARNESS_SCRIPTS/verify-feedback.sh" "$SAVED_PATH")
echo "Result: $RESULT"

if [[ "$RESULT" != *"PASS"* ]]; then
  echo "FAIL: verify returned '$RESULT' instead of PASS"
  # 테스트 파일 정리
  rm -f "$SAVED_PATH"
  exit 1
fi

# 4. 정리
rm -f "$SAVED_PATH"
echo "=== ALL TESTS PASSED ==="
```

- [ ] **Step 7: feedback-system/aggregation-test.sh**

```bash
#!/usr/bin/env bash
set -eo pipefail

# 피드백 수집 + 패턴 분석 통합 테스트
# fixture 데이터를 글로벌 경로에 복사하고 trigger-check.sh가 감지하는지 확인

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HARNESS_SCRIPTS="$SCRIPT_DIR/../../../scripts"
CONTRACT_TRIGGER="$SCRIPT_DIR/../../../skills/contract-kaizen/scripts/trigger-check.sh"

echo "=== Aggregation Test ==="

# 1. 글로벌 경로 확인
FEEDBACK_DIR="$(bash "$HARNESS_SCRIPTS/feedback-path.sh")/contract"
echo "Feedback dir: $FEEDBACK_DIR"

# 2. fixture 데이터 복사 (3개 — ambiguous-conditions 패턴)
FIXTURE_DIR="$SCRIPT_DIR/../contract-kaizen/fixture-feedback-data"
mkdir -p "$FEEDBACK_DIR"

for i in 1 2 3; do
  cp "$FIXTURE_DIR/ambiguous-conditions.yaml" "$FEEDBACK_DIR/testtest-2026-03-${i}0T100000.yaml"
done

# 3. trigger-check 실행
echo "--- trigger-check.sh ---"
if bash "$CONTRACT_TRIGGER"; then
  echo "PASS: trigger detected (expected)"
else
  echo "FAIL: trigger not detected (ambiguous_conditions should trigger at 3+)"
  # 정리
  rm -f "$FEEDBACK_DIR"/testtest-*.yaml
  exit 1
fi

# 4. 정리
rm -f "$FEEDBACK_DIR"/testtest-*.yaml
echo "=== ALL TESTS PASSED ==="
```

- [ ] **Step 8: 실행 권한 부여**

```bash
chmod +x harness/evals/kaizen/feedback-system/save-test.sh harness/evals/kaizen/feedback-system/aggregation-test.sh
```

- [ ] **Step 9: 커밋**

```bash
git add harness/evals/kaizen/
git commit -m "test(harness): 카이젠 메타 eval fixture + 피드백 시스템 테스트"
```

---

## Task 10: 통합 검증

- [ ] **Step 1: 피드백 스크립트 테스트 실행**

```bash
bash harness/evals/kaizen/feedback-system/save-test.sh
```

Expected: `=== ALL TESTS PASSED ===`

- [ ] **Step 2: 트리거 감지 테스트 실행**

```bash
bash harness/evals/kaizen/feedback-system/aggregation-test.sh
```

Expected: `PASS: trigger detected (expected)` + `=== ALL TESTS PASSED ===`

- [ ] **Step 3: 스킬 파일 구조 확인**

```bash
find harness/skills/contract-kaizen -type f
find harness/skills/evaluator-kaizen -type f
```

Expected:
```
harness/skills/contract-kaizen/SKILL.md
harness/skills/contract-kaizen/references/search-sources.md
harness/skills/contract-kaizen/references/pr-template.md
harness/skills/contract-kaizen/scripts/trigger-check.sh
harness/skills/contract-kaizen/templates/research-log-entry.md
(evaluator도 동일 구조)
```

- [ ] **Step 4: 수정된 파일 확인**

```bash
# sprint-contract에 자기진단 단계가 추가되었는지 확인
grep -c "자기진단\|verify-feedback" harness/skills/sprint-contract/SKILL.md

# qa-evaluator에 자기진단 단계가 추가되었는지 확인
grep -c "자기진단\|verify-feedback" harness/agents/qa-evaluator.md

# 오케스트레이터에 6 Phase가 있는지 확인
grep -c "Phase [1-6]" .claude/skills/kaizen-orchestrator/SKILL.md
```

- [ ] **Step 5: 최종 커밋 (필요 시)**

누락된 파일이 있으면 추가 후:

```bash
git add -A
git commit -m "chore: 카이젠 셀프 개선 시스템 최종 정리"
```
