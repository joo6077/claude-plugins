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
| 구체성 편향 (Concreteness bias) | 구체적 코드에 추상적 코드보다 호의적 | 계약 조건 충족만 판단, 구현 스타일 무시 |
| 구현 추종 편향 (Implementation-following bias) | 실제 구현을 "정답"으로 간주하는 경향 | 계약 조건(specification)을 먼저 읽고, 코드는 증거 수집용으로만 사용 |
| 지시 해석 불일치 (Instruction-following misalignment) | 평가 기준을 일관되지 않게 해석 | 조건별 boolean 체크리스트 분해로 해석 여지 최소화 |

> **구현 추종 편향 경고**: LLM은 코드를 읽을 때 구현된 로직을 "의도된 행동"으로 추종하는 경향이 있다
> ([Understanding LLM-Driven Test Oracle Generation](https://arxiv.org/abs/2601.05542)).
> qa-evaluator는 반드시 계약 조건을 먼저 읽고 "기대 행동"을 확립한 뒤 코드를 검증해야 한다.
> 코드를 먼저 읽으면 구현이 곧 정답이라는 착각에 빠진다.

### IV&V 독립성 보장

Independent Verification & Validation (IV&V) 원칙:

- evaluator는 generator의 의도나 과정을 알지 않는다
- 계약과 산출물만으로 판정한다
- "커밋 메시지에 완료라고 썼다" ≠ 증거
- "TODO: 추후 수정" ≠ 현재 PASS

---

## 용어 구분 — L1/L2/L3 기호 충돌 주의

> 이 가이드의 **L1/L2/L3**는 **evaluator 검증 깊이**를 의미한다.
> sprint-contract 계약서의 `[L1]/[L2]/[L3]` 태그는 **조건 구체성 레벨**로, 동일 기호지만 의미가 다르다.

| 체계 | 기호 | 의미 | 위치 |
|------|------|------|------|
| **Evaluator 검증 깊이** (이 가이드) | L1 | 파일/디렉토리 존재 확인 | qa-evaluation-guide, qa-evaluator |
| **Evaluator 검증 깊이** (이 가이드) | L2 | 파일 내용에 기대 요소 존재 확인 | qa-evaluation-guide, qa-evaluator |
| **Evaluator 검증 깊이** (이 가이드) | L3 | 코드 경로 추적, 의미·의도 검증 | qa-evaluation-guide, qa-evaluator |
| **계약 구체성 레벨** (contract-design-guide) | [L1] / exact | 특정 이름·값을 문자 그대로 매칭 | sprint-contract 조건 끝 태그 |
| **계약 구체성 레벨** (contract-design-guide) | [L2] / structural | 섹션·필드 존재 여부 확인 | sprint-contract 조건 끝 태그 |
| **계약 구체성 레벨** (contract-design-guide) | [L3] / goal | 목표 달성 여부만 판정 (수단 무관) | sprint-contract 조건 끝 태그 |

**혼동 방지 규칙:**
- 계약서의 `[L1]` 태그를 보고 "존재 확인(Glob)만 하면 된다"고 해석하지 않는다. 계약의 `[L1]`은 exact 이름 매칭 요구이지 evaluator의 검증 깊이 L1(존재 확인)과 무관하다.
- evaluator 검증 깊이 L1~L3는 계약 조건의 구체성 레벨과 무관하게 **항상 L3까지 도달**해야 한다.
- Sprint Feedback에서 `[L2]`를 근거 태그로 쓸 때는 evaluator 검증 깊이 L2(내용 확인)를 의미한다. 계약의 구체성 레벨과 혼용하지 않는다.

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

**L3 검증 심층화 절차:**

단순 Grep 매칭은 L2에서 멈추는 함정이다. L3 도달을 위해 아래 2단계를 반드시 수행한다:

1. **Grep 존재 확인** — 기대 요소가 파일에 있는지 검색 (L2)
2. **Read 전체 내용 확인 → 의미 추적** — 해당 요소가 포함된 파일을 Read로 열어 맥락(호출 흐름, 조건 분기, 반환 경로)을 확인하고 조건의 의도와 실제 구현이 일치하는지 추적 (L3)

```
# L3 도달 예시
# ❌ L2에서 멈춤: Grep으로 'design-tokens.md' 언급 확인 → PASS
# ✅ L3 도달: Read로 design-tokens.md 전체 내용 확인 → 토큰 구조가
#            조건이 요구하는 카테고리(color/spacing/typography)를 모두 포함하는지 의미 매칭
```

- audit-report.md, design-tokens.md 같은 산출 문서는 Grep으로 존재만 확인하지 말고 **Read로 내용까지 확인**해야 L3 커버리지를 충족한다.
- 파일이 크면 핵심 섹션을 Read(offset/limit)로 부분 읽기하되, 판정에 필요한 구체적 증거(파일:라인)를 확보한다.

### Rubric 기반 분해 (CheckEval 프로토콜)

각 계약 조건을 boolean 서브체크로 분해한다 ([CheckEval](https://arxiv.org/abs/2403.18771) 패턴).
CheckEval은 Likert 스케일 대신 boolean 분해로 평가자 간 일치도를 0.45 향상시켰다 (EMNLP 2025).

**3단계 분해 프로토콜:**

1. **Aspect Selection** — 조건에서 검증해야 할 핵심 측면(aspect)을 식별한다
2. **Checklist Generation** — 각 측면을 Yes/No로 답할 수 있는 boolean 질문으로 변환한다. 질문당 하나의 검증 포인트만 다룬다
3. **Boolean Evaluation** — 각 질문에 L1/L2/L3 레벨로 답한다. PASS 비율이 아닌 **전체 PASS**가 조건 충족 기준이다

**예시:**

조건: "로그인 실패 시 HTTP 401을 반환한다"
├── 서브체크 1: 로그인 실패 경로가 존재하는가? (L1)
├── 서브체크 2: 해당 경로에서 401을 반환하는 코드가 있는가? (L2)
└── 서브체크 3: 잘못된 credential 입력 시 실제로 401 경로를 타는가? (L3)

**복잡한 조건의 분해 예시:**

조건: "대시보드에서 실시간 알림을 표시한다"
├── Aspect A: 알림 데이터 수신
│   ├── A-1: WebSocket/SSE 연결 코드가 존재하는가? (L1)
│   ├── A-2: 서버에서 보낸 메시지를 파싱하는 로직이 있는가? (L2)
│   └── A-3: 파싱된 데이터가 UI 상태로 전달되는 경로가 있는가? (L3)
├── Aspect B: UI 표시
│   ├── B-1: 알림을 렌더링하는 컴포넌트가 존재하는가? (L1)
│   ├── B-2: 알림 데이터가 해당 컴포넌트에 바인딩되어 있는가? (L2)
│   └── B-3: 새 알림 수신 시 UI가 자동 갱신되는가? (L3)

서브체크 하나라도 FAIL이면 해당 조건은 FAIL.

> **적용 기준**: 단순 조건(파일 존재, 설정값 확인)은 분해 없이 직접 L3 검증. 복합 조건(여러 시스템 간 상호작용, 다단계 흐름)은 반드시 Aspect 분해 후 서브체크 수행.

### 스킬 트리거 키워드 배타성 검증 (Set Intersection)

스킬 간 트리거 키워드 중복은 Claude가 잘못된 스킬을 실행하는 직접 원인이다. 키워드 배타성 조건이 계약에 포함된 경우 아래 절차를 따른다.

**검증 절차:**

1. **키워드 추출** — 대상 SKILL.md의 `description` frontmatter에서 트리거 키워드 목록을 Grep으로 추출한다
2. **비교 대상 수집** — 같은 플러그인 내 모든 SKILL.md 파일 목록을 Glob으로 수집한다
3. **Set Intersection 비교** — 각 SKILL.md의 description을 Read하여 키워드를 추출하고, 대상 스킬의 키워드와 교차 비교한다
4. **부분 포함 관계 판정** — 완전 일치뿐 아니라 **부분 문자열 포함 관계**도 배타성 위반으로 판정한다

**부분 포함 관계 판정 기준:**

```
# 위반 예시
스킬 A: "API 연동"
스킬 B: "API 연동 화면"
→ "API 연동"이 "API 연동 화면"의 부분 문자열 → 배타성 위반 FAIL

# 비위반 예시
스킬 A: "컴포넌트 추출"
스킬 B: "화면 추출"
→ 부분 문자열 관계 없음 → PASS
```

**판정 기준:**
- 완전 일치 키워드: FAIL (명백한 중복)
- 부분 포함 관계 키워드: FAIL (사용자 입력에 따라 의도치 않은 스킬이 실행됨)
- 비슷한 의미의 다른 단어: 문맥 분석 후 판정 (FAIL이 불확실하면 `[medium-confidence]` 태그)

> **실제 사례**: SK-05/RE-02 REJECT — `react-run`의 'wasm-pack 빌드'와 `react-wasm`의 'wasm-pack 빌드' 완전 중복, `react-api`의 '"API 연동"'이 `react-feature`의 '"API 연동 화면"'과 부분 포함 관계. Grep 기반 단순 존재 확인으로는 부분 포함 관계를 잡지 못해 Iter 1에서 놓쳤던 케이스.

### 코드블록 언어 힌트 검증 (DG-02) — HTML 파일 적용 기준

Markdown SKILL.md 파일의 fenced code block 언어 힌트 누락(DG-02) 조건이 계약에 포함된 경우:

- **Markdown 파일** (`.md`): ` ```언어명 ` 형식의 언어 힌트 필수. 힌트 없는 ` ``` ` 블록은 FAIL
- **HTML 파일** (`.html`): fenced code block 문법이 없으므로 DG-02 조건 **적용 제외**. 대신 `<pre><code class="language-xxx">` 형식의 언어 클래스 또는 syntax highlight 마커 사용 여부를 확인한다
- HTML 파일에 DG-02를 적용하는 계약 조건은 범위를 `*.md` 파일로 한정했는지 확인하고, 한정하지 않았다면 HTML 파일은 PASS 처리 + 피드백에 "HTML 파일은 DG-02 적용 제외" 명시

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

## 판정 신뢰도 평가

> 근거: [A Statistical Approach to Model Evaluations](https://www.anthropic.com/research/statistical-approach-to-model-evals) (Anthropic)

### 조건별 판정 확신도

각 조건의 PASS/FAIL 판정에 확신도를 부여한다:

| 확신도 | 기준 | 태그 |
|--------|------|------|
| 높음 | L3 검증 완료 + 명확한 증거(파일:라인) | — |
| 중간 | L2까지 검증 + 정황 증거 | `[medium-confidence]` |
| 낮음 | L1만 검증 또는 정적 분석 한계 | `[low-confidence]` |

### 판정 확신도 규칙

- 낮은 확신도 PASS는 `[미검증]`과 동일 취급한다
- 낮은 확신도 조건이 3개 이상이면 Sprint Feedback에 `⚠️ 낮은 확신도 조건 다수` 경고를 명시한다
- 확신도는 판정을 뒤집지 않는다 — FAIL은 확신도와 무관하게 FAIL이다

### 검증 순서 원칙 (Specification-First)

> 근거: [Understanding LLM-Driven Test Oracle Generation](https://arxiv.org/abs/2601.05542)

1. **먼저** Sprint Contract를 읽고 각 조건의 "기대 행동"을 확립한다
2. **그 다음** 코드를 검증한다 — 코드는 증거 수집 대상이지, 기대 행동의 출처가 아니다
3. 코드를 먼저 읽으면 구현 추종 편향에 빠진다

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
