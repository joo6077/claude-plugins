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

Given {전제 조건}
When {동작}
Then {기대 결과}

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
