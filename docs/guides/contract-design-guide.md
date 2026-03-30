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

BDD(Behavior-Driven Development) 패턴으로 조건을 구조화한다:

Given {전제 조건}
When {동작}
Then {기대 결과}

**적용 기준:**
- 복잡도 "중간" 이상: 모든 핵심 조건에 GWT 구조 **필수**
- 복잡도 "단순": 선택 사항이나 권장
- 반구조화된(semi-structured) 조건이 비구조화된 자연어보다 LLM의 추론 정확도를 높이고 할루시네이션을 줄인다 (Thoughtworks, 2025)

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
| 구현 누수 | 조건에 클래스명/메서드명/DB명 포함 | 외부 관찰 가능한 행동으로 재작성 |
| NFR 누락 | 기능 조건만 있고 비기능 조건 없음 | 성능/보안/접근성 중 해당 항목 추가 |

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
