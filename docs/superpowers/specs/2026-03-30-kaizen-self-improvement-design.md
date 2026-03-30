# 카이젠 Core QA 셀프 개선 시스템 디자인 스펙

> **작성일**: 2026-03-30
> **상태**: 승인 대기
> **범위**: sprint-contract / qa-evaluator 리서치 기반 자기개선 + 카이젠 오케스트레이션 재구성

---

## 1. 배경 및 동기

현재 카이젠 오케스트레이션은 설계 가이드, Harness 스킬, Flutter-toolkit을 개선하지만, 전체 QA 파이프라인의 핵심 엔진인 **sprint-contract**(계약 정의)와 **qa-evaluator**(계약 평가)를 체계적으로 자기개선하는 프로세스가 없다.

### 현재 문제

1. **리서치 품질 저하** — 모든 Phase의 리서치를 한번에 몰아서 수행. 질과 양 모두 부족.
2. **Core QA 개선 부재** — sprint-contract와 qa-evaluator는 harness-kaizen이 이론적으로 커버하지만, 전문 리서치 도메인(contract-based testing, test oracle problem 등)이 없음.
3. **자기개선 데이터 없음** — 플러그인이 다른 프로젝트에서 실행되므로 실행 이력이 플러그인 레포에 축적되지 않음.
4. **계약 정의자와 평가자 미분리** — 성격이 완전히 다른 두 컴포넌트가 하나의 카이젠 스킬에 묶여 있음.

---

## 2. 설계 원칙

1. **계약 정의자와 평가자는 독립** — 리서치 도메인, 가이드 문서, 카이젠 스킬 모두 분리. 독립성은 목적의 분리이지 정보 차단이 아님.
2. **리서치는 스킬별 자체 수행** — 오케스트레이터는 순서만 관리. 각 스킬이 자기 도메인의 search-sources.md와 전문 키워드를 갖고 자체 리서치.
3. **글로벌 피드백은 필수** — 선택이 아닌 hard gate. 저장 안 되면 스킬 실행 완료 불가.
4. **자기개선은 3중 구조** — (A) 글로벌 피드백 수집 + (B) 실행 시 자기진단 내장 + (C) 리서치 기반 예방적 개선.
5. **Draft → QA → Apply** — 순환 의존성 방지. QA는 항상 변경 전 버전으로 판단.

---

## 3. 오케스트레이터 Phase 순서

### 변경 전

```
Step 0: 공유 리서치 (전체 몰아서)
Phase 1: 설계 가이드
Phase 2: Harness
Phase 3: Flutter-toolkit
```

### 변경 후

```
Phase 1: 설계 가이드 카이젠 (design-guide-kaizen)
Phase 2: Contract 카이젠 (contract-kaizen)        ← NEW
Phase 3: Evaluator 카이젠 (evaluator-kaizen)      ← NEW
Phase 4: Harness 카이젠 (harness-kaizen)
Phase 5: Flutter-toolkit 카이젠 (flutter-kaizen)
Phase 6: Design-kit 카이젠 (design-kaizen)        ← NEW
```

**Phase 순서 논리:**
- 설계 가이드가 최상위 → contract 설계 원칙이 바뀌면 → evaluator가 그 변경을 반영 → harness 나머지 스킬들이 갱신된 contract/evaluator 기준에 맞춰 개선 → flutter-toolkit → design-kit 순서.

**구조 변경:**
- 공유 리서치 Step 0 **제거**
- 각 Phase는 새 서브에이전트로 실행 (fresh load로 이전 Phase 변경사항 반영)
- Phase 시작 시 **triage** → 개선 불필요 시 SKIP + 로그
- Phase 완료 시 **Regression Smoke Test**

### 각 Phase 공통 실행 패턴

```
1. Triage: 피드백 읽기 → 개선 필요? → 불필요 시 SKIP + 로그
   ⚠ 부트스트랩: 피드백이 0건이면 SKIP하지 않고 리서치 전용 모드로 진행 (패턴 분석 생략, 리서치→예방적 분석만 실행)
2. 자체 리서치: 자기 search-sources.md 기반, 피드백에서 식별된 3-5개 도메인만 (0건 시 search-sources.md 전체에서 우선순위 상위 3개)
3. GAP 분석: 리서치 + 피드백 + 현재 스킬/가이드 대조
4. 예방적 분석: 리서치 anti-pattern을 현재 프롬프트에 대조
5. Sprint Contract (DRAFT): 현재 버전 sprint-contract 사용
6. 개선안 DRAFT 작성 (파일 미적용)
7. QA Evaluator: 현재 버전으로 DRAFT 평가
8. APPROVE → 파일 적용 + 커밋 + Regression Smoke Test
9. Regression 실패 → git revert + BLOCKED
10. 다음 Phase → 새 서브에이전트 (fresh load)
```

---

## 4. 가이드 문서

### 4.1 contract-design-guide.md

**경로**: `docs/guides/contract-design-guide.md`

**목적**: sprint-contract 스킬이 참조하는 계약 작성 원칙. contract-kaizen이 리서치 기반으로 갱신.

**구성:**

| 섹션 | 내용 |
|------|------|
| 핵심 원칙 | 좋은 계약 조건의 기준 (검증 가능, 단일 해석, 측정 가능), precondition/postcondition/invariant 모델, Given-When-Then 구조화 패턴 |
| 조건 작성법 | NASA 스타일 요구사항 작성 규칙 (능동태, 단일 조건, 모호 형용사 금지), IEEE 29148 기반 품질 체크리스트, Property 기반 vs Example 기반 조건 사용 시점 |
| 카테고리 설계 | GQM(Goal-Question-Metric) 기반 카테고리 도출, Consumer-Driven 원칙: 평가자가 검증 가능한 조건만 작성 |
| 안티패턴 | 모호한 조건, 단일 카테고리 편중, 복합 조건 등 |
| 자기개선 메커니즘 | 구조화 진단 체크리스트 항목 정의, 교차 진단 프로토콜, 피드백 수집 지표 정의 |

### 4.2 qa-evaluation-guide.md

**경로**: `docs/guides/qa-evaluation-guide.md`

**목적**: qa-evaluator가 참조하는 평가 방법론. evaluator-kaizen이 리서치 기반으로 갱신.

**구성:**

| 섹션 | 내용 |
|------|------|
| 핵심 원칙 | Test Oracle로서의 evaluator 역할, LLM-as-a-Judge 편향 완화 (위치/장황함/자기강화), IV&V 독립성 보장 |
| 검증 방법론 | 3-Level 검증의 학술적 근거 (lint→semantic→AI 3계층 모델), Rubric 기반 분해: 계약 항목→boolean 서브체크, 다관점 평가 (Fagan/PBR: 기능/엣지/성능/보안) |
| 판정 기준 | Metamorphic Testing: 절대 정답 없을 때 관계 기반 검증, Evidence-Based 판정: 감사 가능한 증거 체인 |
| 자기개선 메커니즘 | 구조화 진단 체크리스트 항목 정의, 교차 진단 프로토콜, Mutation Testing: 의도적 결함 감지율 측정, 피드백 수집 지표 정의 |

### 4.3 공유 참조: contract-schema.md

**경로**: `harness/references/contract-schema.md`

**목적**: 계약 포맷 정의. 양쪽 가이드와 카이젠 스킬이 참조. 소유권은 어느 한쪽에 없음.

- contract-kaizen이 스키마 변경 제안 가능
- evaluator-kaizen이 스키마를 읽어서 평가 루브릭에 반영

---

## 5. 글로벌 피드백 시스템

### 5.1 경로 구조

```
$HOME/.harness/feedback/
├── contract/
│   ├── {project-hash}-{date}.yaml
│   └── ...
├── evaluator/
│   ├── {project-hash}-{date}.yaml
│   └── ...
└── .meta/
    └── cleanup-log.yaml
```

- **project-hash**: 프로젝트 디렉토리 절대경로의 SHA-256 앞 8자
- **파일명**: `{project-hash}-{ISO8601-timestamp}.yaml` (예: `a1b2c3d4-2026-03-30T143022.yaml`) — 같은 날 다중 실행 시 충돌 방지
- **경로 해결**: `scripts/feedback-path.sh`가 OS별 분기. **항상 Unix 스타일 forward-slash 경로 출력** (`$APPDATA` 백슬래시 자동 변환).
  - Windows: `$APPDATA/harness/feedback/`
  - Linux/Mac: `$HOME/.harness/feedback/`
- **fallback**: 글로벌 쓰기 실패 시 `.harness/feedback/`에 로컬 저장 + 경고. 카이젠은 양쪽 다 읽음.
- **정리 정책**: 6개월 초과 파일 자동 삭제, 최대 500개 제한 (oldest-first 삭제). **정리는 모든 카이젠 Phase 완료 후 실행** — 분석 중 데이터 손실 방지.

> **TODO**: 글로벌 경로 전략은 현재 안으로 우선 구현하되, 향후 Claude Code 플러그인 데이터 저장 공식 컨벤션이 정해지면 그에 맞춰 마이그레이션 필요. 마이그레이션 스크립트 포함할 것.

### 5.2 피드백 스키마 (v1)

**정의 파일**: `harness/references/feedback-schema.yaml`

```yaml
schema_version: 1
timestamp: "2026-03-30T14:00:00+09:00"
project_hash: "a1b2c3d4"
project_name: "my-flutter-app"
skill: sprint-contract              # enum: sprint-contract | qa-evaluator
skill_version: "1.3.0"
outcome: completed                  # enum: completed | failed | blocked

# --- contract 전용 ---
contract:
  condition_count: 8
  category_count: 4
  category_coverage: 0.8
  anti_pattern_count: 3
  complexity: medium                # enum: simple | medium | complex

# --- evaluator 전용 ---
evaluation:
  verdict: APPROVE                  # enum: APPROVE | REJECT | BLOCKED
  conditions_total: 8
  conditions_passed: 8
  l3_coverage: 1.0
  reject_reasons: []

# --- 자기진단 ---
diagnosis:
  checklist:
    ambiguous_conditions: false
    missing_error_paths: true
    untestable_conditions: false
  cross_diagnosis_by: qa-evaluator
  cross_diagnosis_notes: "조건 3번 경계값 누락 가능성"
  improvement_suggestions:
    - "에러 경로 조건을 별도 카테고리로 분리"

# --- 사용자 시그널 (optional) ---
user_rating: null                   # enum: good | bad | null
user_comment: null
```

### 5.3 Hard Gate 시행

sprint-contract / qa-evaluator 실행 흐름 마지막:

```
Step N-2: LLM이 자기진단 결과를 포함한 피드백 YAML을 `.harness/feedback-draft.yaml`에 작성
  → 피드백 스키마(harness/references/feedback-schema.yaml) 준수

Step N-1: bash scripts/save-feedback.sh {contract|evaluator} .harness/feedback-draft.yaml
  → yq 또는 python -c 'import yaml'로 스키마 검증 (필수 필드 존재 + 타입 체크)
  → 검증 통과 시 글로벌 경로에 복사 + draft 파일 삭제
  → 실패 시 로컬 fallback (.harness/feedback/)
  → 저장된 파일 절대경로 stdout 출력

Step N: bash scripts/verify-feedback.sh {저장된 파일 절대경로}
  → 파일 존재 + 스키마 valid + 내용 비어있지 않음
  → PASS → 스킬 완료 가능
  → FAIL (exit 1) → 스킬 완료 불가

의존성: yq 또는 Python 3 (yaml 모듈) — save-feedback.sh가 가용한 도구를 자동 감지하여 사용.

Gotchas 최상단:
  "verify-feedback.sh가 PASS를 반환하지 않으면 절대 완료를 선언하지 마라.
   이것은 선택이 아니다."
```

---

## 6. 카이젠 스킬

### 6.1 contract-kaizen

**경로**: `harness/skills/contract-kaizen/`

```
harness/skills/contract-kaizen/
├── SKILL.md
├── references/
│   ├── search-sources.md
│   └── pr-template.md
├── scripts/
│   └── trigger-check.sh
└── templates/
    └── research-log-entry.md
```

**리서치 도메인:**

| 카테고리 | 도메인 |
|----------|--------|
| 계약 설계 | BDD/Gherkin, ATDD/Specification by Example, Design by Contract (DbC), Formal Specification (TLA+/Alloy), Requirements Engineering (IEEE 29148), LLM-Assisted Formal Specification, Property-Based Testing, GQM Framework, Checklist-Based Defect Prevention, Consumer-Driven Contract Testing (Pact), NASA Requirements Writing Standards |
| 자기개선 | Reflection/Self-Refine, Meta-Learning, Retrospective/Post-Mortem, PDCA/Kaizen Cycle, LLM Self-Correction, Experience Replay |

**실행 흐름:**

1. **Triage**: 글로벌 피드백 `contract/` 읽기 → 패턴 분석 (반복 실패, 모호 조건 빈도, 카테고리 편중 등) → 개선 필요 여부 판단 → 불필요 시 SKIP + 로그
2. **리서치**: 피드백에서 식별된 문제 영역 → 관련 도메인 3-5개 선정 → WebSearch + WebFetch + 3-gate 검증
3. **GAP 분석**: 리서치 + 피드백 + 현재 sprint-contract SKILL.md + contract-design-guide.md 대조 → 개선점 목록
4. **예방적 분석**: 리서치 anti-pattern을 현재 프롬프트에 대조 → 잠재적 취약점 식별
5. **Sprint Contract (DRAFT)** → 개선안 DRAFT → QA → APPROVE → 적용
6. **Regression Smoke Test**: `evals/kaizen/contract-kaizen/` 활용

**개선 대상:**
- `docs/guides/contract-design-guide.md` (가이드 원칙 갱신)
- `harness/skills/sprint-contract/SKILL.md` (스킬 프롬프트, Gotchas 갱신)
- `harness/references/contract-schema.md` (계약 스키마 변경 제안)

### 6.2 evaluator-kaizen

**경로**: `harness/skills/evaluator-kaizen/`

```
harness/skills/evaluator-kaizen/
├── SKILL.md
├── references/
│   ├── search-sources.md
│   └── pr-template.md
├── scripts/
│   └── trigger-check.sh
└── templates/
    └── research-log-entry.md
```

**리서치 도메인:**

| 카테고리 | 도메인 |
|----------|--------|
| 평가 방법론 | Test Oracle Problem/LLM-as-Oracle, LLM-as-a-Judge, Rubric-Based LLM Evaluation, Multi-Agent Verification/Consensus, Metamorphic Testing, Mutation Testing, IV&V (Independent V&V), Fagan Inspection/PBR, Symbolic Execution/Concolic Testing, N-Version Programming, Evidence-Based Software Engineering, Automated Code Review (AI-assisted) |
| 자기개선 | Reflection/Self-Refine, Meta-Learning, Retrospective/Post-Mortem, PDCA/Kaizen Cycle, LLM Self-Correction, Experience Replay |

**실행 흐름:** contract-kaizen과 동일 패턴. 대상만 다름:
- 피드백: `evaluator/` 읽기
- 대조 대상: `harness/agents/qa-evaluator.md` + `docs/guides/qa-evaluation-guide.md`
- 추가: `harness/references/contract-schema.md` 변경 여부 확인 → 변경 시 평가 루브릭 갱신 포함

**개선 대상:**
- `docs/guides/qa-evaluation-guide.md` (가이드 원칙 갱신)
- `harness/agents/qa-evaluator.md` (에이전트 프롬프트, 검증 로직 갱신)

### 6.3 트리거 조건 (양쪽 공통)

| 트리거 | 조건 |
|--------|------|
| 오케스트레이터 호출 | Phase 순서에 따라 자동 |
| 피드백 임계치 | 최근 피드백 10건 중 동일 진단 항목 3회 이상 반복 |
| 수동 | `/contract-kaizen`, `/evaluator-kaizen` |

---

## 7. 기존 스킬 수정

### 7.1 sprint-contract

**추가 사항:**

1. **References 추가**:
   - `docs/guides/contract-design-guide.md`
   - `harness/references/contract-schema.md`
   - `harness/references/feedback-schema.yaml`

2. **프로세스 추가 단계** (기존 마지막 단계 이후):
   - Step N+1: 자기진단 — 구조화 체크리스트 실행
   - Step N+2: 교차 진단 — Agent tool로 qa-evaluator 서브에이전트를 호출하여 계약 품질 진단 (출력만 전달, 의사결정 과정 미전달)
   - Step N+3: 피드백 YAML을 `.harness/feedback-draft.yaml`에 작성 (자기진단 + 교차 진단 결과 포함)
   - Step N+4: `bash scripts/save-feedback.sh contract .harness/feedback-draft.yaml`
   - Step N+5: `bash scripts/verify-feedback.sh {save-feedback.sh가 출력한 경로}` → PASS 필수

3. **Gotchas 최상단 추가**:
   - `verify-feedback.sh가 PASS를 반환하지 않으면 절대 완료를 선언하지 마라. 이것은 선택이 아니다.`

### 7.2 qa-evaluator

**추가 사항:**

1. **References 추가**:
   - `docs/guides/qa-evaluation-guide.md`
   - `harness/references/contract-schema.md`
   - `harness/references/feedback-schema.yaml`

2. **프로세스 추가 단계** (판정 출력 이후):
   - Step N+1: 자기진단 — 구조화 체크리스트 실행
   - Step N+2: 교차 진단 — Agent tool로 sprint-contract 서브에이전트를 호출하여 판정 품질 진단 (출력만 전달, 의사결정 과정 미전달)
   - Step N+3: 피드백 YAML을 `.harness/feedback-draft.yaml`에 작성 (자기진단 + 교차 진단 결과 포함)
   - Step N+4: `bash scripts/save-feedback.sh evaluator .harness/feedback-draft.yaml`
   - Step N+5: `bash scripts/verify-feedback.sh {save-feedback.sh가 출력한 경로}` → PASS 필수

3. **Gotchas 최상단 추가**:
   - `verify-feedback.sh가 PASS를 반환하지 않으면 절대 완료를 선언하지 마라. 이것은 선택이 아니다.`

### 7.3 kaizen-orchestrator

**변경 사항:**

1. 공유 리서치 Step 0 **제거**
2. Phase 2(contract-kaizen), Phase 3(evaluator-kaizen) **삽입**
3. 기존 Phase 2 → Phase 4, Phase 3 → Phase 5
4. Phase 6(design-kaizen) **추가** — 기존 `design-kit/skills/design-kaizen/` 스킬을 오케스트레이터에 통합. 상세 스펙은 기존 스킬 정의를 따르며, 자체 리서치 분산 원칙만 적용.
5. **Phase 4(harness-kaizen) 스코프 재정의**: sprint-contract와 qa-evaluator는 Phase 2, 3에서 처리하므로 harness-kaizen은 **이를 제외한** 나머지 harness 스킬/에이전트/설정을 대상으로 함 (sprint-feedback, init, project.yaml, procedures, 향후 추가 스킬 등)
6. 각 Phase는 새 서브에이전트로 실행 (Draft → QA → Apply 패턴)
7. Phase 시작 시 triage → SKIP 가능 (단, 피드백 0건 시 리서치 전용 모드로 진행)
8. Phase 완료 시 Regression Smoke Test
9. Regression 실패 → git revert + BLOCKED + 다음 Phase로 진행
10. **Regression 실패 카운터**: `.harness/.meta/kaizen-failure-count.yaml`에 Phase별 연속 실패 횟수 영속화. 연속 2회 시 해당 Phase 일시 중단.
11. **git tag**: DRAFT 적용 직전에 `kaizen-phase-N-pre` 태그 생성 → revert 시 이 태그로 복원

---

## 8. 안전장치

### 8.1 Draft → QA → Apply 패턴 (순환 의존성 방지)

```
Phase N:
1. Sprint Contract 작성 (현재 버전 사용)
2. 개선안 DRAFT 작성 (파일에 적용하지 않음)
3. QA Evaluator가 DRAFT를 평가 (현재 버전 evaluator 사용)
4. APPROVE → 파일 적용 + 커밋
5. 다음 Phase → 새 서브에이전트 (디스크에서 fresh load)
```

QA는 항상 변경 전 버전으로 판단. 변경은 QA 통과 후에만 적용.

**알려진 제한**: Phase 2(contract-kaizen)의 변경은 구버전 evaluator로 승인됨. Phase 3에서 evaluator가 강화되면 Phase 2 결과가 새 기준을 통과 못할 수 있음. 이 교차 검증은 **다음 카이젠 사이클**에서 수행됨 — 현재 사이클에서는 각 Phase가 자기 시점의 도구로 판단받는 것을 원칙으로 함.

### 8.2 Regression Smoke Test

```
각 Phase 완료 후:
1. 개선된 스킬을 fixture 시나리오에 실행
2. expected-improvements.md와 대조
3. PASS → 다음 Phase
4. FAIL → git revert (kaizen-phase-N-pre 태그) + BLOCKED 로그
5. 연속 2회 FAIL (.harness/.meta/kaizen-failure-count.yaml 참조) → 해당 Phase 일시 중단 + 사용자 알림
```

**Fixture 구조:**

```
harness/evals/kaizen/contract-kaizen/
├── fixture-feedback-data/
│   ├── ambiguous-conditions.yaml    # 모호 조건 반복 패턴 피드백
│   ├── category-bias.yaml           # 카테고리 편중 패턴 피드백
│   └── low-coverage.yaml            # 커버리지 낮은 패턴 피드백
├── fixture-projects/
│   ├── simple-crud/                 # 단순 CRUD 프로젝트 mock
│   └── complex-api/                 # 복잡 API 프로젝트 mock
├── expected-improvements.md         # 각 fixture-feedback 대비 기대 개선 체크리스트
│   # 예: "ambiguous-conditions.yaml → Gotchas에 모호 조건 감지 규칙 추가"
│   # 예: "category-bias.yaml → 카테고리 균형 검증 단계 추가"
├── baseline/                        # 개선 전 스킬의 fixture 실행 결과 스냅샷
│   └── sprint-contract-output.md
└── assertions.json                  # 자동화 검증 규칙
    # 예: {"type": "file_contains", "file": "SKILL.md", "pattern": "모호.*감지"}
    # 예: {"type": "gotcha_count_gte", "min": N}
```

**PASS/FAIL 기준**: assertions.json의 모든 assertion 통과 = PASS. 하나라도 실패 = FAIL. assertion은 파일 존재, 내용 포함, Gotchas 개수, 특정 패턴 존재 등 구체적 규칙.

### 8.3 메타 Eval 구조

```
harness/evals/kaizen/
├── contract-kaizen/
│   ├── fixture-feedback-data/
│   ├── expected-improvements.md
│   └── assertions.json
├── evaluator-kaizen/
│   ├── fixture-feedback-data/
│   ├── expected-improvements.md
│   └── assertions.json
└── feedback-system/
    ├── save-test.sh
    └── aggregation-test.sh
```

### 8.4 교차 진단 프로토콜

| 시점 | 진단자 | 진단 대상 | 핵심 질문 |
|------|--------|-----------|-----------|
| sprint-contract 실행 후 | qa-evaluator 서브에이전트 | 계약 조건 | "이 조건을 독립적으로 검증할 수 있는가?" |
| qa-evaluator 실행 후 | sprint-contract 서브에이전트 | 평가 판정 | "계약 조건의 원래 의도를 정확히 해석했는가?" |

**구조적 분리**: 교차 진단은 같은 LLM이 관점만 바꾸는 것이 아닌, Agent tool로 상대 에이전트를 **별도 컨텍스트**에서 호출하여 수행. 호출 시 진단 대상 출력만 전달하고, 원래 세션의 의사결정 과정은 전달하지 않음. 결과는 피드백 YAML의 `cross_diagnosis` 필드에 기록.

### 8.5 자기진단 3중 구조

| 계층 | 방법 | 신뢰도 |
|------|------|--------|
| 구조화 체크리스트 | 구체적 항목 체크 (동시성, 에러 경로, 경계값 등) | 중 |
| 교차 진단 (서브에이전트) | qa-evaluator 에이전트를 실제 서브에이전트로 호출하여 contract 품질 진단 (역방향도 동일). 같은 LLM의 관점 전환이 아닌 별도 에이전트 컨텍스트에서 실행하여 구조적 분리 확보. | 상 |
| 사용자 시그널 | `user_rating` + `user_comment` (optional) | 최상 |

### 8.6 롤백 체인

| 실패 시나리오 | 대응 |
|--------------|------|
| QA REJECT 3회 | Phase 중단, 사용자 에스컬레이션 |
| Regression FAIL | git revert + BLOCKED 로그 + 다음 Phase 진행 |
| Regression 2연속 FAIL | 해당 Phase 일시 중단 + 사용자 알림 |
| 피드백 저장 실패 | 로컬 fallback 저장 + 경고 |
| 글로벌 경로 접근 불가 | `.harness/feedback/` 로컬 저장 + 카이젠 시 양쪽 탐색 |

---

## 9. 자기개선 리서치 도메인 (양쪽 공통)

contract-kaizen과 evaluator-kaizen 모두 자기 도메인별 리서치 외에 다음 자기개선 도메인을 공통으로 포함:

| # | 도메인 | 핵심 가치 |
|---|--------|-----------|
| 1 | Reflection / Self-Refine | LLM 자기 출력 평가 후 반복 개선 |
| 2 | Meta-Learning / Learning to Learn | 과거 태스크에서 전략을 추출해 미래에 적용 |
| 3 | Retrospective / Post-Mortem | 실행 이력 회고에서 체계적 교훈 도출 방법론 |
| 4 | PDCA / Kaizen Cycle | Plan-Do-Check-Act 사이클의 학술적 프레임 |
| 5 | LLM Self-Correction | 자기 수정의 한계와 조건 연구 |
| 6 | Experience Replay | 강화학습의 경험 재사용 — 과거 피드백 재활용 패턴 |

---

## 10. 파일 인벤토리

### 신규 생성

| 경로 | 목적 |
|------|------|
| `docs/guides/contract-design-guide.md` | 계약 작성 원칙 가이드 |
| `docs/guides/qa-evaluation-guide.md` | 평가 방법론 가이드 |
| `harness/references/contract-schema.md` | 계약 포맷 공유 정의 |
| `harness/references/feedback-schema.yaml` | 피드백 YAML 스키마 |
| `harness/skills/contract-kaizen/SKILL.md` | contract 카이젠 스킬 |
| `harness/skills/contract-kaizen/references/search-sources.md` | contract 리서치 소스 |
| `harness/skills/contract-kaizen/references/pr-template.md` | PR 템플릿 |
| `harness/skills/contract-kaizen/scripts/trigger-check.sh` | 트리거 감지 |
| `harness/skills/contract-kaizen/templates/research-log-entry.md` | 리서치 로그 포맷 |
| `harness/skills/evaluator-kaizen/SKILL.md` | evaluator 카이젠 스킬 |
| `harness/skills/evaluator-kaizen/references/search-sources.md` | evaluator 리서치 소스 |
| `harness/skills/evaluator-kaizen/references/pr-template.md` | PR 템플릿 |
| `harness/skills/evaluator-kaizen/scripts/trigger-check.sh` | 트리거 감지 |
| `harness/skills/evaluator-kaizen/templates/research-log-entry.md` | 리서치 로그 포맷 |
| `harness/scripts/save-feedback.sh` | 피드백 저장 + 스키마 검증 |
| `harness/scripts/verify-feedback.sh` | 피드백 존재/유효성 검증 |
| `harness/scripts/feedback-path.sh` | OS별 글로벌 경로 해결 |
| `harness/evals/kaizen/contract-kaizen/` | contract-kaizen 메타 eval |
| `harness/evals/kaizen/evaluator-kaizen/` | evaluator-kaizen 메타 eval |
| `harness/evals/kaizen/feedback-system/` | 피드백 시스템 테스트 |

### 수정

| 경로 | 변경 내용 |
|------|-----------|
| `harness/skills/sprint-contract/SKILL.md` | 자기진단 + 피드백 hard gate + 가이드 참조 추가 |
| `harness/agents/qa-evaluator.md` | 자기진단 + 피드백 hard gate + 가이드 참조 추가 |
| `.claude/skills/kaizen-orchestrator/SKILL.md` | 6 Phase 재구성 + 공유 리서치 제거 + triage/regression 추가 |
