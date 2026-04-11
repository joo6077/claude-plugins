# Contract Design Guide

> sprint-contract 스킬이 참조하는 계약 작성 원칙.
> contract-kaizen이 리서치 기반으로 이 문서를 갱신한다.
>
> **참조 스키마**: `harness/references/contract-schema.md`
>
> **최근 갱신: 2026-04-11 (Phase 2 kaizen research)** — 숫자 레벨 네이밍 충돌 해결
> (문자 태그 exact/structural/goal 로 교체), Aggregation Mode / 태그 선택 기준
> 서브섹션 신설, AAA·LLM-as-Judge 연구 인용 추가.

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

### Given-When-Then / Arrange-Act-Assert 구조화

BDD (Behavior-Driven Development) 의 **Given-When-Then** 또는 테스트 패턴
**AAA (Arrange-Act-Assert)** 로 조건을 구조화한다. 두 패턴은 동일 개념
(사전 상태 → 행동 → 관찰) 을 다른 어휘로 표현한 것이므로 상황에 맞게 선택한다.

```text
Given {전제 조건}      |  Arrange {사전 세팅}
When  {동작}           |  Act     {행동 1회}
Then  {기대 결과}      |  Assert  {관찰 1회}
```

**적용 기준:**

- 복잡도 "중간" 이상: 모든 핵심 조건에 GWT 또는 AAA 구조 **필수**
- 복잡도 "단순": 선택 사항이나 권장
- 반구조화된 (semi-structured) 조건이 비구조화된 자연어보다 LLM 의 추론 정확도를 높이고 할루시네이션을 줄인다 (Thoughtworks, 2025)
- **Gherkin one When-Then pair 규칙**: 한 조건에 When-Then 쌍은 1 개만 — 2 개 이상이면 복합 조건이므로 분리한다 ([Gherkin Best Practices](https://github.com/andredesousa/gherkin-best-practices))
- **AAA blueprint 패턴**: LLM 코드 에이전트 벤치마크 연구는 PRD 를 evaluation blueprint 로 쓰고 GPT-4.1 이 Arrange-Act-Assert 형식으로 테스트 케이스를 생성하는 파이프라인을 제시했다 ([arxiv 2510.24358](https://arxiv.org/html/2510.24358v1)). 계약 조건을 AAA 로 작성하면 그 자체가 실행 가능한 spec 에 가까워진다.

### 외부 관찰 가능성 (External Observables Only)

조건은 시스템이 **무엇을** 하는지(외부 행동)만 기술한다. **어떻게** 하는지(내부 구현)는 기술하지 않는다.

**금지 요소:**
- 클래스명, 메서드명, 함수명
- DB 테이블, 컬럼, API 엔드포인트 경로
- 프레임워크 용어 (controller, service, repository, provider, notifier)
- 내부 상태 변수, 플래그

**나쁜 예**: "UserService의 userRepository가 비어있을 때"
**좋은 예**: "등록된 사용자가 없을 때"

**나쁜 예**: "POST /api/users 호출 시 201을 반환한다"
**좋은 예**: "신규 사용자 등록 요청 시 성공 응답을 반환한다"

이 규칙을 위반하면 "구현 누수(implementation leakage)"라 한다. 구현이 변경되면 조건도 깨지므로, 조건의 수명이 짧아진다.

### 조건 구체성 태그 (Specificity Tag)

계약 작성 시 각 조건이 어느 수준으로 판정될지를 명시한다. 수준이 불명확하면 QA Evaluator 가 해석을 달리하여 판정이 엇갈린다.

> **중요 — 네이밍 규칙**: 숫자 레벨 (L-one, L-two, L-three) 은 **QA 평가 깊이 전용**
> 으로 예약되어 있다 (skill-design-guide §5.5 Degrees of Freedom 참조). 계약의 조건
> 태그는 반드시 아래 **문자 태그** (`[exact]`, `[structural]`, `[goal]`) 만 사용하고,
> 숫자 레벨을 계약 조건에 재사용하지 마라. 숫자 레벨을 혼용하면 QA 깊이와 조건
> 구체성이 구분되지 않아 평가 판정이 엇갈린다.

| 태그 | 정의 | 판정 기준 | 적합한 상황 |
|------|------|-----------|-------------|
| `[exact]` | 특정 이름/값/구조를 문자 그대로 매칭 | 해당 식별자가 코드에 존재하는지 직접 검색 | 함수명 계약, 파일명 계약, 특정 클래스 구조 |
| `[structural]` | 섹션/필드/파일의 존재 여부 및 필수 서브구조 | 지정된 섹션·필드가 존재하는지 확인 | "X 섹션을 포함한다", "Y 필드가 있다" |
| `[goal]` | 수단 무관, 목표 달성 여부만 판정 | 기능이 의도한 결과를 산출하는지 확인 | "SSOT 달성", "회귀 없음", "파싱 성공" |

**사용 방법**: 조건 끝에 문자 태그를 붙인다.

```markdown
- [ ] PU-01: 문서 파싱이 pyyaml 기반으로 동작한다 [goal]
- [ ] SK-01: References 섹션에 7개 문서가 각각 파일명으로 명시된다 [structural]
- [ ] CD-01: compare-bad/compare-good 클래스를 사용하는 비교 블록이 2쌍 이상 존재한다 [exact]
```

**태그 미명시 시 기본값**: `[structural]` 로 간주한다.

> **실제 발생 사례 (PU-04 REJECT)**: 계약이 "pyyaml 기반 파싱 함수 사용"을 요구했으나
> exact/goal 어느 수준인지 불명확해, 같은 목표를 달성한 구현이 "함수명 불일치" 로 REJECT 됨.
> 계약에 `[goal]` 을 명시했다면 PASS 처리 가능했던 케이스.

#### 태그 선택 기준

어떤 태그를 붙일지 결정하는 기준:

- **`[exact]` 선택**: 이름·값·구조가 **그것이어야만** 의미가 있을 때. 예) 공개 API 의 정확한 함수 시그니처, 파일 경로 그 자체, 정규표현식 문자열 리터럴. "이름이 달라지면 계약 실패" 가 성립하면 `[exact]`.
- **`[structural]` 선택**: "해당 구조가 존재한다" 만 검증하고 싶을 때. 예) "References 섹션이 있다", "3개의 카테고리가 정의되어 있다". 내부 세부는 다른 조건으로 검증하거나 판정 대상이 아님.
- **`[goal]` 선택**: 구현 방법은 자유이고 **결과만** 보고 싶을 때. 예) "SSOT 유지", "파싱 성공", "중복 제거". 함수명·라이브러리·접근법이 달라도 목표만 달성하면 PASS.

> **경험칙**: 판정 시 "구현이 X 라서 REJECT 할 것인가?" 라고 자문했을 때
> REJECT 가 부당하다고 느끼면 태그가 `[exact]` 일 가능성이 높다 — `[goal]` 로 완화하라.
> 반대로 "이름이 달라도 상관없다" 고 했다가 실제로는 특정 이름을 강제하고 싶은
> 경우였다면 `[exact]` 로 강화하라.
>
> 출처: LLM-as-Judge 신뢰성 연구는 "명확한 평가 criteria 가 있을 때 CoT 추론의
> 효과가 최소화되며, criteria 품질이 곧 평가 품질" 이라고 보고한다
> ([arxiv 2506.13639](https://arxiv.org/html/2506.13639v1)). 태그는 criteria
> 명확화의 핵심 수단이다.

#### Aggregation Mode — 다수 대상 조건의 형식

조건이 **다수의 대상** (파일·모듈·키워드·경로) 에 적용될 때, 계약 작성자는
**개별 명시 (enumerated)** 모드와 **포괄 경로 (collective)** 모드 중 어느 쪽을
요구하는지 명시해야 한다. 형식을 정하지 않으면 QA Evaluator 가 한쪽 해석으로
기울어 평가가 엇갈린다.

| 모드 | 의미 | 판정 방법 | 조건 작성 예 |
|------|------|-----------|-------------|
| **enumerated** | 각 대상을 하나씩 이름으로 명시해야 PASS | 모든 개별 이름이 문서에 직접 등장하는지 확인 | "References 에 `g1`, `g2`, `g3`, `g4`, `g5`, `g5b`, `g6` 7 개 파일이 각각 파일명으로 명시된다 [exact, enumerated]" |
| **collective** | 포괄 경로/패턴 하나로 지정해도 PASS | 경로·디렉토리 지정이 전체를 커버하는지 확인 | "References 에 `docs/react/kit-design/` 경로가 명시된다 [structural, collective]" |

**사용 규칙:**

- 모드를 명시하려면 태그 뒤에 콤마로 이어 쓴다: `[exact, enumerated]`, `[structural, collective]`
- 모드 미명시 시 기본값은 `collective` (포괄) 이다 — 더 관대한 해석
- 모드는 태그가 `[exact]` / `[structural]` 일 때만 의미가 있다. `[goal]` 은 aggregation 개념 자체가 적용되지 않음

> **실제 발생 사례 (KZ-04 REJECT)**: 계약이
> "react-kaizen References 섹션에 `docs/react/kit-design/` 7 개 그룹 문서가 명시된다"
> 로 작성되었는데, 구현자는 포괄 경로 하나로 처리했고 QA 는 개별 명시를 요구해 REJECT.
> 계약이 `[exact, enumerated]` 또는 `[structural, collective]` 중 하나를 명시했다면
> 사전에 해소 가능했던 케이스.

#### 한·영 표현 변형 처리

한국어 + 영어가 혼용되는 도메인 (프론트엔드 성능 지표, React/Flutter 생태계 등)
에서는 동일 개념이 여러 표현으로 등장한다. 계약 조건에 표현 변형이 존재하면
판정이 엇갈린다.

- **좋은 예 1 (병기)**: "Layout shift (레이아웃 shift) 발생 0 건 [goal]"
- **좋은 예 2 (통일 선언)**: "Layout shift 발생 0 건 — 본 계약에서는 영어 표기 Layout shift 로 통일 [goal]"
- **나쁜 예**: "레이아웃 shift 발생 0 건" — 구현 코드가 `layout-shift` 로 작성되면 키워드 매칭이 어긋남

> 표현 변형이 있는 조건은 **한·영 병기 또는 한쪽으로 통일** 중 하나를 명시적으로 선택하라.

### 예외 조항 포맷 (Exception Clause)

조건이 특정 파일·상황·타입에는 적용되지 않을 경우, 조건 내부에 인라인으로 예외를 명시한다. 별도 문서로 분리하거나 구두로 합의하면 QA 시점에 예외가 반영되지 않는다.

**포맷:**

```markdown
- [ ] CD-02: 모든 docs 페이지에 compare-bad/compare-good 비교 블록이 2쌍 이상 존재한다.
      예외: (a) integration.html — Final 통합 페이지로 개별 비교보다 전체 조합을 다루므로 제외,
            (b) index.html — 목록 페이지로 콘텐츠 조건 비적용
```

**규칙:**
- 예외는 "왜 제외하는가"를 한 줄로 설명한다 (이유 없는 예외 금지)
- 예외 항목이 3개를 초과하면 조건 자체를 범위 한정(`applies_to`)으로 재작성한다
- 예외 없이 작성된 조건은 해당 카테고리의 **모든** 파일에 적용된다고 간주한다

**applies_to 범위 한정 (예외 3개 초과 시):**

조건 적용 범위를 파일 패턴이나 성격으로 한정한다.

```markdown
- [ ] CD-02: `docs/react/` 하위 콘텐츠 페이지(integration.html, index.html 제외)에
      compare-bad/compare-good 비교 블록이 2쌍 이상 존재한다
```

> **실제 발생 사례**: CD-02 REJECT 다수 — integration.html이 Final 통합 페이지임에도 일반 콘텐츠 조건이 동일하게 적용되어 REJECT. 예외 조항 없이 작성된 조건의 전형적 실패 패턴.

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

계약의 "소비자" 는 qa-evaluator 이다. 평가자가 독립적으로 검증할 수 없는 조건은 나쁜 조건이다.

자기 점검: "이 조건을 코드와 실행 결과만으로 PASS/FAIL 판정할 수 있는가?"

- YES → 유효한 조건
- NO → 재작성 필요

> **LLM-as-Judge 연구 요지** ([arxiv 2506.13639](https://arxiv.org/html/2506.13639v1)):
> "Evaluation criteria are critical for reliability. Non-deterministic sampling
> improves alignment with human preferences over deterministic evaluation,
> and CoT reasoning offers minimal gains when clear evaluation criteria are
> present." — 즉 **criteria 품질이 평가 품질을 결정**하며, 추가적인 CoT 로 모호한
> criteria 를 보완하는 것은 한계가 있다. 계약 작성 단계에서 criteria 를
> 명확히 하는 것이 가장 ROI 높은 개입이다.
>
> 관련: LLM agent 를 software engineering 벤치마크로 평가한 survey 는 unit test 가
> "a detailed, executable specification that provides a formal contract" 역할을
> 한다고 보고한다 ([arxiv 2510.09721](https://arxiv.org/html/2510.09721v3)).
> 계약 조건은 실행 가능한 테스트에 최대한 가깝게 작성하라.

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
| 구현 누수 | 조건에 클래스명/메서드명/DB명 포함 | 외부 관찰 가능한 행동으로 재작성 |
| NFR 누락 | 기능 조건만 있고 비기능 조건 없음 | 성능/보안/접근성 중 해당 항목 추가 |
| 판정 기준 범주 미명시 | "함수명으로 교체한다" 가 exact (이름 일치) 요구인지 goal (동작 목표) 허용인지 불명확 → QA 해석 엇갈림 | 조건 끝에 `[exact]` / `[structural]` / `[goal]` 태그로 구체성 명시 |
| 예외 없는 전체 적용 | 조건이 특정 파일 타입·성격에는 부적합한데 예외 없이 전 범위에 적용 → 불필요한 REJECT | 예외 조항을 조건 내부에 인라인으로 명시하거나 `applies_to` 로 범위 한정 |
| Aggregation mode 미명시 | 다수 대상 (파일/모듈/키워드) 조건에서 개별 명시 vs 포괄 경로 중 무엇을 요구하는지 불명확 → 구현자·평가자 해석 엇갈림 | `[exact, enumerated]` 또는 `[structural, collective]` 로 aggregation 모드 명시 |
| 한·영 표현 변형 비통일 | "Layout shift" vs "레이아웃 shift" 같은 변형이 조건에 혼재 → 키워드 매칭·의미 해석 불일치 | 한·영 병기 또는 한쪽으로 통일 선언을 조건 내부에 명시 |
| 숫자 레벨 태그 혼용 | 계약 조건 태그에 QA 평가 깊이용 숫자 레벨을 재사용 → QA 검증 깊이와 충돌 | 반드시 문자 태그 `[exact]` / `[structural]` / `[goal]` 만 사용 (skill-design-guide §5.5 참조) |

---

## 자기개선 메커니즘

### 구조화 진단 체크리스트

sprint-contract 실행 완료 후 다음 항목을 자가 점검한다:

| 항목 | 점검 내용 |
|------|-----------|
| ambiguous_conditions | 모호한 표현이 포함된 조건이 있는가? (아래 모호성 분류 참조) |
| missing_error_paths | 에러/예외 경로에 대한 조건이 누락되었는가? |
| untestable_conditions | 코드만으로 검증 불가능한 조건이 있는가? |
| category_coverage_gap | project.yaml 카테고리 중 커버하지 못한 것이 있는가? |
| complexity_underestimate | 복잡도를 과소평가하여 조건 수가 부족한가? |
| implementation_leakage | 조건에 내부 구현 용어(클래스명, 메서드명, DB명)가 포함되었는가? |
| nfr_coverage | 해당 기능의 비기능 요구사항(성능/보안/접근성)이 조건에 반영되었는가? |

### 모호성 분류 (Ambiguity Taxonomy)

조건 검토 시 다음 3가지 유형의 모호성을 구분하여 점검한다:

| 유형 | 설명 | 예시 | 수정 |
|------|------|------|------|
| 어휘적 (Lexical) | 단어 자체가 여러 의미 | "처리한다", "관리한다" | 구체 동사로 대체 ("반환한다", "저장한다") |
| 구문적 (Syntactic) | 문장 구조가 여러 해석 허용 | "A와 B를 포함하는 C" | 분리하여 각각 명시 |
| 의미적 (Semantic) | 도메인 맥락 없이 해석 불가 | "적절한 응답" | 구체적 상태 코드/값으로 명시 |

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
