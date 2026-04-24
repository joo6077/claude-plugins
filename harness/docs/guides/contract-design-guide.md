# Contract Design Guide

> sprint-contract 스킬이 참조하는 계약 작성 원칙.
> contract-kaizen이 리서치 기반으로 이 문서를 갱신한다.
>
> **참조 스키마**: `harness/references/contract-schema.md`
>
> **최근 갱신: 2026-04-24 (Phase 2 kaizen · v3)** — Cross-Surface Parity 섹션 신설
> (skill-design-guide §11 / agent-design-guide §12 원칙 전수), Binary Decidability
> 계약 작성자 의무 서브섹션, Scope Range 인라인 명시 (SK-02 대응), Verification
> Method Required / Unverifiable Policy (mcp_server=null 대응), Sibling Consistency
> 조건 패턴 (rust-kit H-01/H-03 대응) 추가. 스키마 v3 bump.
>
> 이전: 2026-04-12 — 경계값 조건 작성법, 스코프 세분화 (granularity) 서브섹션.
> 2026-04-11 — 숫자 레벨 네이밍 충돌 해결, Aggregation Mode / 태그 선택 기준,
> AAA·LLM-as-Judge 연구 인용 추가.

---

## 핵심 원칙

### 검증 가능성 (Verifiability)

모든 조건은 제3자가 코드만 보고 PASS/FAIL을 판정할 수 있어야 한다. 이는
Agile Alliance 의 INVEST 원칙 중 **Testable** 과 동일한 요구이다 — "제3자가
objectively 확인 가능해야 하며, 측정 가능한 값과 구체 행동으로 기술한다"
([Agile Alliance INVEST](https://www.agilealliance.org/glossary/invest/)).
주관적 언어 ("잘 동작한다", "적절히", "충분히") 는 금지.

- **좋은 예**: "로그인 실패 시 HTTP 401을 반환한다"
- **나쁜 예**: "로그인이 적절히 처리된다"

> **LLM-as-Judge 연구 보강 (2026-04-24)**: 평가 criteria 의 **극단값 (PASS/FAIL 양끝)**
> 정의가 중간값 설명보다 judge alignment 에 더 큰 영향을 준다
> ([arxiv 2506.13639](https://arxiv.org/html/2506.13639v1)). 즉 "이 조건이 PASS
> 인 상태" 와 "이 조건이 FAIL 인 상태" 를 각각 한 문장으로 구체화하는 것이 중간
> 정도 서술을 풍부하게 하는 것보다 중요하다. 계약 작성 시 각 조건의 FAIL 이미지를
> 먼저 떠올리고 그 부정으로 PASS 를 기술하면 이진 판정 가능성이 올라간다.

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

### 계약 작성자 의무 — 이진 판정 가능성 (Binary Decidability)

> **대응:** `agent-design-guide.md §3.5 "Binary Decidability Pre-Check"` (평가자 의무 측)

계약 **작성자** 는 조건을 제출하기 전, 각 조건이 **PASS 또는 FAIL 중 정확히 하나**
로 귀결 가능한지 자체 점검한다. 평가자의 Binary Decidability Pre-Check 는 계약이
이미 이진 판정 가능하다는 전제 위에서 동작하며, 계약 작성 단계에서 모호성이 남으면
평가 iteration 이 낭비된다 ([arxiv 2506.13639](https://arxiv.org/html/2506.13639v1)
— criteria 명확화가 추가 CoT 보강보다 ROI 높음).

**작성자 체크리스트 (조건 제출 전):**

- [ ] 이 조건에 정성적 수식어 (충분히 / 상당한 / 적절히 / 대부분 / 거의) 가 없는가?
- [ ] 이 조건의 FAIL 상태가 1 문장으로 기술 가능한가? 불가능하면 조건이 모호하다
- [ ] 이 조건의 태그 (`[exact]`/`[structural]`/`[goal]`) 가 부여되어 있는가?
- [ ] 이 조건을 읽고 2 명의 평가자가 서로 다른 판정에 도달할 가능성이 있는가?
      있다면 모호성 원인 (어휘 / 구문 / 의미 / 범위 / 측정 방법) 을 제거하라

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

### 경계값 조건 (Boundary Conditions)

수량·길이·크기 등 **임계값을 포함하는 조건**은 측정 방법을 함께 명시한다.
측정 방법이 없으면 QA Evaluator 가 다른 도구·기준으로 측정하여 판정이 엇갈린다.

**필수 요소:**

1. **임계값**: 구체적 숫자 (`>= 1500`, `== 0`, `<= 3`)
2. **측정 대상**: 무엇을 세는가 (줄 수, 파일 수, 바이트 수, 항목 수)
3. **측정 방법**: 어떻게 세는가 (명령어, 도구, 계산식)

**좋은 예:**

```text
- [ ] AR-03: docs/flutter/ 하위 .md 파일의 총 줄 수가 1500 이상이다
      (측정: `wc -l docs/flutter/*.md | tail -1`) [exact]
```

**나쁜 예:**

```text
- [ ] AR-03: docs/flutter/ 문서가 충분한 분량이다 [goal]
- [ ] AR-03: docs/flutter/ 문서가 1500줄 이상이다 [exact]
      ← 측정 방법 미명시: wc -l vs grep -c vs 에디터 줄 수 중 무엇?
```

> **실제 발생 사례 (AR-03 REJECT)**: 계약이 ">= 1500줄" 을 요구했으나 측정
> 방법을 명시하지 않아, 구현이 1498줄 (2줄 부족) 로 REJECT. 측정 명령이
> 사전에 합의되었다면 구현 중 즉시 확인이 가능했던 케이스.

### 스코프 세분화 (Scope Granularity)

조건이 **포맷·구조·패턴**의 적용을 요구할 때, 적용 단위를 명시한다.
"일관된 포맷" 같은 표현은 파일 단위인지, 섹션 단위인지, 컬럼 단위인지
해석이 갈린다.

**세분화 수준:**

| 수준 | 의미 | 예시 |
|------|------|------|
| **file-level** | 파일 전체가 동일 포맷 | "모든 .md 파일이 YAML frontmatter 를 포함한다" |
| **section-level** | 특정 섹션 내부 구조 통일 | "각 섹션의 소스 테이블이 동일 컬럼 구성이다" |
| **field-level** | 개별 필드/컬럼까지 명시 | "소스 테이블에 `번호`, `제목`, `URL`, `태그` 4개 컬럼이 존재한다" |

**적용 규칙:**

- 포맷 일관성을 요구하는 조건은 **최소 section-level** 까지 명시한다
- field-level 까지 명시하면 가장 정확하지만, 조건이 길어지므로 핵심 필드만 열거한다
- "일관된 포맷" 단독 사용 금지 — 어떤 수준에서 일관적인지 반드시 부연한다

> **실제 발생 사례 (ER-02 / AR-03 REJECT)**: 계약이 "6개 파일의 일관된 포맷" 을
> 요구했으나 컬럼 구성까지 명시하지 않아, 한 파일만 태그 컬럼이 누락된 채 통과하려
> 했고 QA 가 REJECT. field-level 로 "소스 테이블에 `[official]`/`[blog]` 태그
> 컬럼 포함" 을 명시했다면 사전에 해소 가능했던 케이스.

### 스코프 범위 인라인 명시 (Scope Range)

조건에 "주요", "모든", "대부분", "핵심" 같은 **범위어** 가 등장하면 그 범위가
무엇을 포함하고 무엇을 제외하는지 **조건 내부에 인라인 enumerate** 해야 한다.
그렇지 않으면 평가자가 범위를 자체 해석하여 동일 구현이 PASS 또는 REJECT 로
갈린다.

**Bad (범위 모호):**

```text
- [ ] UI-02: 주요 interactive element 의 box-shadow offset 이 >= 4px 이다 [exact]
```

"주요 interactive element" 가 버튼·카드·입력만 의미하는지, badge 와 decoration
까지 포함하는지 불명확. 실제 SK-02 REJECT 사례 — Neubrutalism 시안에서 badge
box-shadow offset 3px 가 범위 내라고 간주되어 REJECT.

**Good (범위 인라인 명시):**

```text
- [ ] UI-02: 버튼·카드·입력 요소 의 box-shadow offset 이 >= 4px 이다
      (badge, decoration, 장식용 icon 은 범위 외) [exact, enumerated]
```

**규칙:**

- 범위어가 포함된 조건은 **반드시** 괄호나 "예외: ..." 형태로 포함/제외 목록을
  인라인 기술한다
- 범위가 5 개 이상이면 `applies_to: <pattern>` 로 대체 (예외 조항 포맷 참조)
- "주요 / 모든 / 대부분" 단독 사용 금지 — 작성자가 직접 열거 책임

> **실제 발생 사례 (SK-02 REJECT)**: "Neubrutalism 모달의 .ms-card-action box-shadow
> offset 3px, .ms-badge box-shadow offset 2px" 로 구현되었으나 계약이 "주요 interactive
> element" 로만 서술되어 badge/decoration 이 범위에 포함되는지 해석이 갈려 REJECT.
> "버튼·카드·입력" 처럼 인라인 enumerate 했다면 사전에 해소 가능했던 케이스.

### 검증 수단 명시 의무 (Verification Method Required)

모든 조건은 **어떻게 판정할지** 를 인라인으로 명시해야 한다. 측정 명령 (`wc -l`,
`grep`, `cargo build`), 도구 (MCP Figma, Playwright, IDE Problems 패널), 관찰
대상 (파일 경로 · 섹션명 · 상태 코드) 중 하나 이상을 조건에 적어라.

**금지 — 검증 수단 없음:**

```text
- [ ] DG-04: 런타임 에러가 없다 [goal]
```

이 조건은 누가 어떻게 판정하는지 불명확. 앱을 구동해야 하는지, 로그를 읽어야
하는지, MCP 서버가 필요한지 아무도 모른다.

**허용 — 측정 도구 명시:**

```text
- [ ] DG-04: 앱 구동 시 console 에 ERROR 레벨 로그 0 건
      (측정: MCP Figma read-back 또는 `flutter run` 직접 실행 후 stdout 확인) [goal]
```

#### MCP / 외부 도구 의존 조건의 3 단계 fallback

MCP 서버, 외부 API, 로컬 실행 환경에 의존하는 조건은 다음 3 단계를 조건에
명시한다:

| 단계 | 의미 | 작성 방식 |
|------|------|----------|
| 1. 기본 검증 | 선호하는 도구·명령 | "측정: MCP Figma read-back" |
| 2. Fallback | 기본 도구 미가용 시 대체 정적 검증 | "미가용 시: 파일 내 CSS 변수 값 Grep 으로 대조" |
| 3. 미검증 수용 | 둘 다 불가능 시 | "둘 다 불가능 시 `[미검증]` 마커 허용 (계약 전체에서 1 건까지)" |

**규칙:**

- 평가 시점에 MCP 서버가 `null` 이거나 로컬 환경 제약으로 1~2 단계가 불가능하면
  조건에 기술된 **3 단계 fallback** 이 적용된다
- **계약 작성 단계에서 `[미검증]` 허용 건수가 2 건 이상 예상되면 조건을 재설계하라.**
  qa-evaluation-guide 의 "미검증 2 건 이상 REJECT" 정책과 맞물려 작성 단계에서
  REJECT 가 예측 가능하다
- 조건에 fallback 을 명시하지 않으면 평가자가 도구를 임의 선택하여 판정이 엇갈림

> **실제 발생 사례 (fit-pal LG-02/DG-04, fit-pal-flutter 2026-04-17)**: 시각 검증
> 조건 3 건이 `mcp_server=null` 로 미검증 처리되어 "미검증 2 건 이상 REJECT"
> 규칙으로 REJECT. 계약이 3 단계 fallback 을 기술했다면 정적 대체 검증으로
> PASS 가능했던 케이스.

### 형제 스킬 일관성 (Sibling Consistency)

동일 플러그인 내 여러 스킬이 **공통 원칙** 을 요구할 때 (예: 헥사고날 패턴, 에러
처리 규칙, 코드 생성 템플릿), 계약은 "이 원칙이 sibling 스킬 **전부** 에 적용되어
있다" 를 **enumerated** 형태로 명시해야 한다. 한 스킬에만 적용되었는지 전체에
적용되었는지 해석 여지를 없앤다.

**Bad (sibling cross-check 누락):**

```text
- [ ] SK-03: rust-api 핸들러 예시가 domain event + outbox 원칙을 따른다 [structural]
```

rust-init, rust-feature, rust-service, rust-api 4 스킬 중 rust-api 만 점검하게
됨. 실제로 rust-service 에는 원칙이 있고 rust-init/rust-feature/rust-api 에는
누락된 상태로 통과 (H-01/H-03 REJECT).

**Good (sibling enumerated):**

```text
- [ ] SK-03: domain event + outbox 원칙이 rust-init, rust-feature, rust-service,
      rust-api 4 개 스킬의 Gotchas 섹션 **전부** 에 적용되어 있다 [exact, enumerated]
```

**규칙:**

- 공통 원칙 조건은 반드시 `[exact, enumerated]` 또는 `[structural, enumerated]`
  aggregation mode 를 사용한다 (`collective` 금지 — 한 개만 통과하면 PASS 되므로)
- sibling 스킬 개수를 조건에 **숫자로** 명시한다 ("4 개 스킬 전부")
- 적용 대상 스킬을 빠짐없이 열거한다 (생략 금지)

> **실제 발생 사례 (rust-kit H-01/H-03 REJECT, 2026-04)**: "domain event + outbox"
> 원칙이 rust-service Gotchas 에만 있고 rust-init/rust-feature/rust-api 에는
> 누락. 계약이 단일 스킬 기준으로 작성되어 sibling gap 을 잡지 못함. enumerated
> mode 로 "4 개 스킬 전부" 를 요구했다면 작성자가 스킬 편집 시 전파를 강제할
> 수 있었던 케이스.

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
| 경계값 측정 방법 미명시 | ">= N" 조건에 측정 명령/도구 없음 → 구현자와 평가자가 다른 방법으로 측정하여 판정 엇갈림 | 임계값 + 측정 대상 + 측정 방법(명령어)을 조건에 인라인으로 명시 |
| 포맷 세분화 수준 미명시 | "일관된 포맷" 요구에 파일/섹션/필드 중 어느 수준인지 불명확 → 부분 불일치를 간과하거나 과잉 REJECT | 최소 section-level 까지 명시, 핵심 필드는 field-level 로 열거 |
| 스코프 범위어 미명시 | "주요", "모든", "대부분" 같은 범위어가 인라인 enumerate 없이 등장 → 평가자가 범위를 자체 해석하여 PASS/REJECT 엇갈림 | 범위 포함/제외 목록을 조건 내부에 괄호 또는 "예외: ..." 형태로 명시 (SK-02 재발 방지) |
| 검증 수단 미명시 | 조건이 어떤 명령·도구·관찰로 판정되는지 기술 없음 → 평가자가 도구를 임의 선택 (특히 MCP `null` 시 미검증 급증) | 측정 명령/도구/관찰 대상을 조건에 인라인 기술, 외부 도구 의존 시 3 단계 fallback 명시 |
| Sibling 스킬 커버리지 누락 | 공통 원칙이 plugin 내 여러 스킬에 적용돼야 하지만 계약이 단일 스킬만 점검 → 일부 스킬에만 적용된 상태 통과 | `[exact, enumerated]` + 스킬 숫자/이름 전부 열거로 sibling 전수 요구 (rust-kit H-01/H-03 재발 방지) |
| 정성적 수식어 사용 | "충분히", "상당한", "적절히", "대부분" 등 binary 판정 불가 수식어 | 구체 수치/기준값으로 대체 또는 조건 분리 (Binary Decidability Pre-Check 실패 1 순위) |

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
| boundary_without_measurement | 경계값(>=, <=, ==) 조건에 측정 방법이 누락되었는가? |
| format_granularity_missing | 포맷 일관성 조건에 적용 수준(file/section/field)이 명시되었는가? |

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

---

## 원칙 전수성 · Cross-Surface Parity Checklist

> **대응:** [`skill-design-guide.md §11`](skill-design-guide.md) · [`agent-design-guide.md §12`](agent-design-guide.md)
>
> **배경 (meta-issue):** 지난 kaizen 사이클에서 skill-design-guide §3.5 "계약
> 모호성 방지" 원칙이 이 가이드에 전수되지 않아 design-kit PH-01 REJECT 가
> 발생했다. Phase 2 (2026-04-24) 에서 계약 설계 레이어에 **대응 섹션을 구조적으로
> 고정** 하여 원칙 전수 공백을 메운다.

### 원칙

계약 설계 가이드가 개정되면, 상위 **skill-design-guide · agent-design-guide** 와
하위 **qa-evaluation-guide · sprint-contract SKILL.md · qa-evaluator 에이전트** 에
대응 원칙이 존재하는지 자동 체크한다. 전파 필요성 판정 → 즉시 복제.

### 계약 설계에 전수된 parity items (3 개)

| # | Parity Item | skill-design-guide 위치 | agent-design-guide 위치 | **contract-design-guide 대응 위치 (이 가이드)** |
|---|-------------|------------------------|------------------------|------------------------------------------------|
| 1 | 계약 모호성 방지 / Binary Decidability | §3.5 (QA 계약과 1:1 매칭) | §3.5 (Binary Decidability Pre-Check) | **§조건 작성법 > "계약 작성자 의무 — 이진 판정 가능성"** |
| 2 | 트리거 키워드 배타성 (substring 포함) | §4 (set intersection + substring) | §3 + §10 (sibling agent 검사) | **§sprint-contract SKILL.md Process Step (키워드 검사 의무)** |
| 3 | 미검증 항목 정책 | — (스킬 전용 아님) | §10 Unverifiable 조건 정책 | **§조건 작성법 > "검증 수단 명시 의무" (3 단계 fallback)** |

> 두 가이드의 item 1 · item 4 (rule-by-rule audit) 는 contract 가이드에
> 해당 위치 없이 qa-evaluation-guide 로 위임된다 (중복 배제).

### 개정 시 체크리스트

contract-design-guide.md 를 편집할 때:

- [ ] 새 원칙을 추가했는가? → skill-design-guide §11 / agent-design-guide §12 Parity Table 에 contract 대응 위치 컬럼을 갱신
- [ ] 원칙 네이밍 (카테고리 ID, 섹션명) 을 변경했는가? → sprint-contract SKILL.md · qa-evaluator.md · qa-evaluation-guide 에서 동일 네이밍 사용 중인지 Grep 하여 동기화
- [ ] Bad/Good 예시를 추가했는가? → 해당 원칙이 있는 skill/agent 가이드에도 동일 구조의 예시 존재 여부 확인
- [ ] contract-schema.md 스키마 버전을 bump 해야 하는가? → 조건 태그/필드 변경 시 필수

### 실패 패턴 (이 원칙 없이 발생한 실제 REJECT)

- **SK-02 (harness, 2026-04)**: 범위어 "주요 interactive element" 가 인라인 enumerate 되지 않아 badge/decoration 해석 엇갈림 → 범위 명시 원칙이 contract-design-guide 에 없어 계약 작성자가 원칙을 몰랐음 (현 사이클에서 SR 섹션 신설로 해소)
- **미검증 항목 2 건 REJECT (fit-pal, fit-pal-flutter)**: mcp_server=null 상태에서 시각 검증 불가 조건이 2 건 이상 → 계약이 fallback 을 사전 기술하지 않아 REJECT (현 사이클 UV 섹션 신설로 해소)
- **H-01/H-03 (rust-kit)**: sibling 스킬 커버리지 조건이 계약에 enumerate 되지 않아 일부 스킬만 적용된 상태가 PASS (현 사이클 SC 섹션 신설로 해소)

### Downstream 전파 범위

본 가이드 개정이 영향 줄 수 있는 하위 surface:

- `harness/skills/sprint-contract/SKILL.md` — Process Step, Gotchas
- `harness/references/contract-schema.md` — 스키마 버전 및 필드
- `harness/docs/guides/qa-evaluation-guide.md` — 평가 방법론 (대응 원칙)
- `harness/agents/qa-evaluator.md` — 평가 절차

### 버전 정보

- **Guide version**: 2026-04-24 (Phase 2 kaizen · v3)
- **Schema version**: v3 (contract-schema.md)
- **Parity with**: skill-design-guide v1.2.0, agent-design-guide v1.2.0
