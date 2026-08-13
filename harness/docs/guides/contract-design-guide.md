# Contract Design Guide

> sprint-contract 스킬이 참조하는 계약 작성 원칙.
> contract-kaizen이 리서치 기반으로 이 문서를 갱신한다.
>
> **참조 스키마**: `harness/references/contract-schema.md`
>
> **최근 갱신: 2026-08-13 (Phase 2 kaizen · v5.0)** — 글로벌 REJECT/improvement
> 2026-08-11~12 (`AR-04` 4 건 · `ER-02` · `LG-01` · `UI-04`) 를 근거로 **write-once 를
> 서술에서 결정론적 봉인(E3)으로 승급**했다. 직전 사이클이 amendment 사이드카를 도입했는데도
> 같은 위반이 재발했으므로, 이번에는 문장을 추가하지 않고 **근본원인 3 개**(규칙이 읽기 측
> 문서에만 존재 · 준수 경로의 기대 보상이 위반 경로보다 낮음 · 위반을 재는 오라클 부재)를
> 각각 막았다. 주요 변경:
> (a) **§계약 봉인 (Write-Once Seal)** 신설 — E1 → E3 승급.
> (b) **§Amendment 방향 판정** 신설 — direction × consent 2 축 분리 (RC2 해소).
> (c) **§측정 커버리지** 신설 — 산문↔측정 대상 대조 검출기 (E2, 오탐률 실측 기록).
> (d) **§인자 매트릭스** 신설 — 조합 케이스 수 수기 오류 + variant 축 중복을 한 패턴으로.
> (e) **§음성 대조** 신설 — "구현을 지워도 통과하는 측정문" 차단.
> (f) 조건 작성 preflight 에 QA 모호성 태그 6 종 되먹임.
> 스키마 v5.2 → v5.3 (`conditions_digest` / `locked_at` · amendment 2 축 · 조건 패턴 3 종).
>
> 이전: 2026-07-27 (Phase 2 kaizen · v4.0) — `/insights` 2026-07-27 (51 세션)
> Friction #4 + reflect-digest 760 엔트리 + 글로벌 REJECT 89 건 분석. 이번 사이클의
> 방침은 **새 문장 추가가 아니라 enforcement 등급 승급** 이다 (Phase 1
> skill-design-guide §3.7 등급 사다리 준용). 주요 변경:
> (a) **Counterpart Conditions** 신설 — Phase 1 §5.5 Counterpart Enumeration 을
> 계약 조건으로 흡수 (parity item 12 의 계약 측 착지점).
> (b) **Diff-Scope Oracle 표준형** — AR-01 3 회 재발로 E1 → E3 승급.
> (c) **Preamble–Condition Consistency** 신설 (RE-02).
> (d) **증거 아티팩트 존재 의무** 신설 (UI-06).
> (e) `[exact]` 산출물 동반 제출 규칙 (UI-07).
> (f) **§원칙별 Enforcement 등급** 표 신설 — 재발 규칙 4 건 승급 기록.
> 스키마 v3 → v4 (헤더 2 계층 분류 · Counterpart 조건 패턴).
>
> 이전: 2026-06-05 (Phase 2 kaizen · v3.2) — global feedback REJECT 패턴
> 분석. LG-07 (gitignore 의도에 `test ! -f` oracle 불일치) · AR-01 (커밋 전
> `git diff` 상태 전제 누락) 두 REJECT 를 근거로 "측정 명령 타당성 · 상태 전제
> (Measurement Validity & Precondition)" 서브섹션 신설 (§검증 수단 명시 의무 하위).
> 기존 "측정 방법을 명시하라" 원칙이 oracle 의 **존재** 만 다루고 oracle 의 **의미·
> 전제 타당성** 은 다루지 않던 공백을 메움. 안티패턴 테이블 1 행 추가. parity item
> 신설 없음 (계약 작성자 고유 의무 — Verification Method 절의 하위 보강).
>
> 이전: 2026-05-07 (Phase 2 kaizen · v3.1) — `/insights` 30 일 세션
> 분석 흡수. Friction #1 (proactive quality gap) 은 본 문서의 "다수 대상 인라인
> enumerate" + "Sibling Consistency" 절이 이미 강제하고 있어 신규 절 없음.
> Friction #2 (false-dichotomy) 은 Phase 1 신규 skill-design-guide §3.6
> "Pre-Edit Batch Audit" (v1.3.0) 가 계약 **작성 단계** 에서 옵션 enumerate →
> 사용자 합의를 강제하므로, 본 가이드 사용 시 해당 절을 cross-reference 한다.
> Friction #3 (truncation) 은 계약 자체와 무관 (스킬 Process 책임).
>
> 이전 (2026-04-24, v3): Cross-Surface Parity 섹션 신설 (skill-design-guide §11
> / agent-design-guide §12 원칙 전수), Binary Decidability 계약 작성자 의무
> 서브섹션, Scope Range 인라인 명시 (SK-02 대응), Verification Method Required
> / Unverifiable Policy (mcp_server=null 대응), Sibling Consistency 조건 패턴
> (rust-kit H-01/H-03 대응) 추가. 스키마 v3 bump.
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

## 원칙별 Enforcement 등급 (E1 / E2 / E3)

> **규약 출처:** [`skill-design-guide.md §3.7`](skill-design-guide.md) — 등급 정의, 승급 규칙,
> 초기 등급 선택 기준, 그리고 **설계 가이드 원칙의 등급 원장**은 그쪽이 SSOT 다. 본 절은
> **계약 레이어 고유 원칙이 현재 어느 등급에 있는지**만 기록한다. 용어를 재정의하거나 동의어를
> 만들지 마라.
>
> **§3.7 등급 원장을 이 표에 복제하지 마라.** 같은 원칙이 두 곳에서 서로 다른 등급을 갖게 되는
> 순간 승급 판정이 불가능해진다. 아래 표는 **계약 레이어 고유 원칙만** 담고, §3.7 원장에 이미
> 있는 원칙의 등급값을 행으로 다시 적지 않는다. 원장 원칙의 계약 측 착지점은 아래 대응만 알면
> 된다 — Pre-Edit Batch Audit → 본 표의 "Pre-Edit Audit (계약 시점)" 행, Counterpart Enumeration
> → "Counterpart Conditions" 행, Variant Budget → §인자 매트릭스의 variant 용법,
> User-Reported Failure Gate → 계약 측 착지 없음(평가자 소관 · Phase 3). **이 대응 관계에서
> 등급을 정하는 쪽은 언제나 §3.7 원장이다.**

계약 원칙도 "문장으로 적었으니 지켜지겠지" 가 통하지 않는다. 실측(reflect-digest 760 엔트리)에서
`skipped-pre-edit-audit` · `config-command-mismatch` · `complexity-by-file-count` ·
`parser-incompatible-contract-section` 은 **모두 이미 문장 규칙이 존재하는데도 재위반**했고,
전부 `user_stated_constraint=true`(사용자가 명시한 규칙을 다시 어김) 로 분류됐다.

| 등급 | 계약 레이어에서의 형태 |
| ---- | ---------------------- |
| **E1** | contract-design-guide 의 서술 원칙 · SKILL.md Gotcha 한 줄 |
| **E2** | 계약 파일에 남는 아티팩트 — 조건 그 자체, 인라인 `측정:` 절, DRAFT 제시 전 출력하는 대조표 |
| **E3** | LLM 판단 없이 실행되는 결정론적 검사 — 표준형 측정 명령, 저장 직후 헤더 검사 |

### 현재 등급표 (2026-08-13 기준)

| 원칙 | 등급 | 근거 · 승급 이력 |
| ---- | ---- | ---------------- |
| 이진 판정 가능성 (Binary Decidability) | E1 | 작성자 체크리스트 — 재발 이력 없음 |
| 조건 구체성 태그 · aggregation mode | E2 | 태그가 계약 본문에 남는 아티팩트 |
| 검증 수단 인라인 명시 | E2 | `측정:` 절이 계약에 남음 |
| **Pre-Edit Audit (계약 시점)** | **E1 → E2 승급** | digest `skipped-pre-edit-audit` (usc) — Gotcha 문장만 있어 재위반. 감사 결과 표를 DRAFT 전 산출물로 요구 |
| **설정 리터럴 전사 (project.yaml)** | **E1 → E2 승급** | digest `config-command-mismatch` + `ignored-project-commands` (2 건) — 대조표를 DRAFT 전 산출물로 요구 |
| **복잡도 판정 (영향 범위)** | **E1 → E2 승급** | digest `complexity-by-file-count` (usc) — Gotcha + 안티패턴 2 곳이 다 E1 이었음. 4 축 판정 표를 요구 |
| **Diff-Scope Oracle** | **E1 → E3 승급** | REJECT AR-01 2026-06-11 · AR-01 2026-06-29 · Improvement 2026-07-21 — **3 회 재발**. 표준형 명령 + 작성 시점 baseline 실행 |
| **허용 섹션 헤더** | **E1 → E3 승급** | digest `parser-incompatible-contract-section` (usc) — 저장 직후 결정론적 헤더 검사 |
| `CONTRACT_ROOT` 경로 고정 | E2 (신규) | digest `cwd-contract-path-drift` — 확정한 절대경로를 출력해 남김 |
| Counterpart Conditions | E2 (신규) | insights Friction #4 — 조건 2 개로 계약에 박힘 |
| Preamble–Condition Consistency | E2 (신규) | REJECT RE-02 — DRAFT 자가 대조 |
| 증거 아티팩트 존재 의무 | E2 (신규) | REJECT UI-06 — 증거 경로가 조건에 남음 |
| **계약 봉인 (Write-Once Seal)** | **E1 → E3 승급** | REJECT AR-04 2026-08-11 (*"계약 write-once 위반 — 생성자가 자신이 만든 산출물을 사후에 허용하려 계약 AR-04 조건 문구를 직접 편집(5→7 경로)"*). 사이드카(E1 서술)를 도입한 **다음 사이클에 바로 재발**했고 위반을 재는 오라클이 없었다 → `conditions_digest` 결정론적 검사 |
| Amendment 방향 판정 (direction × consent) | E2 (신규) | REJECT *"amendment A-01은 prompt-log 앵커 부재로 unknown 분류, PASS 근거 불가"* — 두 축이 뭉쳐 있어 준수 경로가 무력화됐다. 집합형은 direction 을 계산해 사이드카에 남김 |
| 측정 커버리지 대조 | E2 (신규 · **검출기**) | Improvement *"[AR-04] 계약-측정-불일치 — 조건 프로즈(화이트리스트 12항목)와 측정 필드(5개 무관 디렉토리 grep)의 커버리지 갭"*. 실측 오탐률 때문에 blocking 게이트로 올리지 않는다 |
| 인자 매트릭스 — 조합 케이스 수 산출 | E2 (신규) | REJECT LG-01 (*"3 visibility x 6 relation = 18 케이스 중 15케이스만 재현"*) · LG-01 (*"16종 매핑 … 2종만 검증"*). `cases_total` 수기 입력 금지 |
| 음성 대조 (Negative Control) | E2 (신규) | REJECT ER-02 — *"mutation test로 확정 — 실제 코드에서 동시성 가드를 완전히 삭제해도 이 테스트는 여전히 통과한다"* |
| 조건 작성 preflight (QA 모호성 태그) | E1 (신규) | improvement 태그 6 종 반복 (`측정-수단-부재` · `측정-방식-불일치` · `측정-환경-오염` · `측정-산출물-부재` · `검증경로-미기재` · `측정-중복`). 판정에 문맥 해석이 필요하므로 자문 목록으로 시작 |

**개정 규칙:** 같은 결함이 다시 관측되면 이 표의 문구를 다듬지 말고 **등급을 한 칸 올려라.**
등급을 올릴 수 없으면(이미 E3) 조건 설계 자체가 잘못된 것이므로 원칙을 재작성한다.

**E3 로 올렸다고 끝이 아니다.** 봉인은 조건 문구의 **불변성**만 보장하고 조건이 옳았는지는
보장하지 않는다. 게이트를 올리면 과차단 비용과 우회 유인이 함께 생기며, **우회된 게이트는 없는
게이트보다 나쁘다** — 통과 기록이 안전을 오해하게 만들기 때문이다 (skill-design-guide §3.7
"E3 의 한계"). 그래서 봉인은 체크박스 토글과 서술 편집을 **일부러 통과시킨다.**

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

### 양면 조건 — Counterpart Conditions

> **출처:** `/insights` 2026-07-27 Friction #4 (풀스택 변경에서 클라이언트 누락) ·
> [Pact — Contract tests are not functional tests](https://docs.pact.io/consumer/contract_tests_not_functional_tests) ·
> [Pact — What is Pact good for](https://docs.pact.io/getting_started/what_is_pact_good_for) ·
> 대응: [`skill-design-guide.md §5.5 Counterpart Enumeration`](skill-design-guide.md) (생성 측)
>
> **설계 결정:** Counterpart Enumeration 은 qa-evaluation-guide 에 대응 절을 두지 않는다.
> 평가자는 **계약에 박힌 조건**으로 이 원칙을 수용한다 (parity item 12). 따라서 이 원칙이
> 실제로 작동하려면 **계약 작성자가 조건을 넣어야만 한다** — 안 넣으면 아무도 안 잡는다.

계약·직렬화·공유 모델을 바꾸는 스프린트는 본질적으로 **양면 작업**이다. 서버 응답 형태를 바꾸고
클라이언트를 다음 스프린트로 미루면, 그 스프린트는 계약상 완료가 아니라 **절반 완료**다. 실측에서
사용자가 "당연히 그러면 클라까지 바꿔야지" 로 매번 개입해야 했고, UTC 직렬화 버그도 같은 계열이다.

계약 테스트의 표준 관점도 동일하다 — consumer 측 검증만 하면 provider 가 예고 없이 바뀌고,
provider 측만 검증하면 consumer 가 잘못된 요청을 보낸다. **양쪽을 다 검증해야 통합 실패가 잡힌다**
(소스: Pact).

**적용 대상 (아래 중 하나라도 건드리면 Counterpart 조건 필수):**

- API 계약 · 엔드포인트 시그니처 · 상태 코드 (빈 상태 204/200/404 포함)
- 직렬화 포맷 — JSON 스키마, 날짜·타임존 표현, enum 값, null 허용 여부
- 공유 모델 · 공용 타입 · 생성 코드 (OpenAPI, protobuf, codegen 산출물)
- 공개 함수 시그니처 · 이벤트 페이로드 · DB 스키마

**작성 규칙:**

1. **producer 면과 consumer 면을 각각 별도 조건으로 쓴다.** 한 조건에 양면을 묶으면 복합 조건이라
   부분 통과가 PASS 로 새어 나간다 (Gherkin one When-Then pair 규칙과 동일 이유).
2. 각 조건은 해당 면의 **파일 경로를 enumerate** 한다 — `[exact, enumerated]` 필수.
   `collective` 금지 (한쪽만 바뀌어도 PASS 되므로).
3. consumer 면을 찾지 못하면 grep 으로 탐색하고, 그래도 없으면 **"소비자 없음" 을 근거와 함께
   조건에 명시**한다. 추측으로 생략하지 않는다.
4. **소비면의 내부 구현을 조건화하지 마라.** Pact 가 경고하는 과잉 계약(over-specified contract)
   이 된다 — 열거 대상은 파일 경로와 외부 관찰 가능한 동작까지다. "클라이언트가 어떤 함수로
   파싱하는가" 는 조건이 아니다.
5. 한 스프린트에서 양면을 다 못 바꾸면, 남는 쪽은 `[미검증]` 이 아니라 **명시적 미완 조건**으로
   남긴다 (`[미검증]` 은 검증 도구 부재에만 쓰는 마커다 — 의미를 섞지 마라).

**조건 패턴:**

```text
- [ ] AR-04: 응답 필드 rename 이 producer 면 파일 `server/src/handler/schedule.rs` 에 반영된다
      [exact, enumerated] (측정: 해당 파일에 신규 필드명 존재 · 구 필드명 0 건)
- [ ] AR-05: 같은 rename 이 consumer 면 파일 `app/lib/data/model/schedule_model.dart`,
      `app/lib/data/model/schedule_model.g.dart` 2 개에 반영된다 [exact, enumerated]
      (측정: 두 파일에 신규 필드명 존재 · 구 필드명 0 건)
```

```text
Bad:  - [ ] AR-04: 필드 rename 이 서버와 클라이언트에 반영된다 [goal]
      ← 복합 조건 + collective. 서버만 바뀌어도 판정이 갈린다
Good: producer 조건 1 개 + consumer 조건 1 개, 각각 파일 경로 enumerated
```

**부적합:** 소비자가 존재할 수 없는 순수 내부 리팩터링(private 함수 본문, 로컬 변수명).
이 경우 Counterpart 조건은 noise 다.

### 계약 서두–조건 정합성 (Preamble–Condition Consistency)

> **출처:** 글로벌 REJECT RE-02 (fit-pal, 2026-07-22) ·
> [AI Spec Template](https://www.augmentcode.com/guides/ai-spec-template)

계약에 배경·설계 의도 서술(preamble)이 있으면, 그것은 장식이 아니라 **구현자가 읽는 지시**다.
서술과 조건이 어긋나면 에이전트는 물어보지 않고 **조용히 한쪽을 골라** 구현한다
("agents resolve the conflict silently by picking one instruction over the other" — 소스 5).

**실제 발생 사례 (RE-02, 2026-07-22)**: 계약 preamble 은 **단방향** 차단 조회를 설계 의도로
서술했는데, 조건 RE-02 는 **양방향** 함수 `batch_blocked_among` 의 재사용을 literal 로 열거했다.
구현자는 preamble 을 따라 단방향 `batch_blocking_out` 을 새로 만들었고, 평가자는 조건의 literal
enumeration 미충족으로 REJECT. 어느 쪽도 틀리지 않았고 **계약이 자기모순**이었다.

**작성자 점검 (DRAFT 제시 전, E2):**

- [ ] 서술 절에 쓴 설계 의도와 각 조건이 같은 방향을 가리키는가? 어긋나면 **조건이 아니라
      서술을 고칠지, 서술이 아니라 조건을 고칠지 먼저 정하고 사용자에게 알린다**
- [ ] 조건이 **기존 식별자**(함수·클래스·파일명)를 literal 로 열거한다면, 그 식별자가 지금 코드에
      실제 존재하는지 grep 으로 확인했는가? 존재하지 않는 이름을 열거하면 자동 REJECT 다
- [ ] 열거한 식별자의 **의미**(단방향/양방향, 동기/비동기, 단수/복수)가 설계 의도와 일치하는가?
- [ ] 재사용을 요구하는 조건이라면 "이 이름이어야만 하는가"(`[exact]`) 인지 "같은 목적을 달성하면
      되는가"(`[goal]`) 인지 태그로 구분했는가?

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
| ------ | ------ | ----------- | ------------- |
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

##### 산출물 동반 제출 규칙 — `[exact]` 는 "그 산출물도 이번에 낸다" 는 뜻이다

조건 문장에 **테스트·문서·스크린샷 같은 부산출물**이 등장하고 태그가 `[exact]` 이면, 그 산출물은
구현과 **같은 스프린트에 제출해야 하는 대상**이 된다. 평가자는 "구현은 됐지만 테스트가 없다" 를
조건 미충족으로 읽는다.

- 산출물까지 이번에 낼 생각이면 → `[exact]` 로 두고 산출물 경로까지 조건에 적는다
- 구현만 이번에 내고 산출물은 다음 스프린트면 → **조건을 `[goal]` 로 낮추거나 산출물 문구를
  조건에서 뺀다**. 둘 다 안 하고 그대로 두면 REJECT 가 예정된 것이다

```text
Bad:  - [ ] UI-07: 설정 화면에서 차단 목록 화면으로 이동한다 (widget test 포함) [exact]
      ← 테스트를 안 내면 REJECT. 낼 생각이 없었다면 조건이 틀린 것
Good: - [ ] UI-07: 설정 화면에서 차단 목록 화면으로 이동한다 [goal]
      - [ ] UI-08: 위 이동을 검증하는 widget test 가 `test/settings/blocks_nav_test.dart` 에
            존재하고 통과한다 [exact] (측정: `flutter test test/settings/blocks_nav_test.dart`)
```

> **실제 발생 사례 (UI-07 REJECT, fit-pal-app 2026-07-13)**: `[exact]` 조건에 widget test 가
> 명시됐는데 테스트 0 건으로 제출되어 REJECT. 평가자 Improvement 도 "`[exact]` 에 test 를 명시하면
> 구현과 함께 테스트도 제출해야 함 — 테스트 우선 작성 권장" / "조건을 `[goal]` 로 변경 권장" 두 갈래로
> 나왔다. 둘 중 무엇을 원하는지는 **작성 시점에** 정해야 한다.

#### Aggregation Mode — 다수 대상 조건의 형식

조건이 **다수의 대상** (파일·모듈·키워드·경로) 에 적용될 때, 계약 작성자는
**개별 명시 (enumerated)** 모드와 **포괄 경로 (collective)** 모드 중 어느 쪽을
요구하는지 명시해야 한다. 형식을 정하지 않으면 QA Evaluator 가 한쪽 해석으로
기울어 평가가 엇갈린다.

| 모드 | 의미 | 판정 방법 | 조건 작성 예 |
| ------ | ------ | ----------- | ------------- |
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
| ------ | ------ | ------ |
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
| ------ | ------ | ---------- |
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

#### 측정 명령 타당성 · 상태 전제 (Measurement Validity & Precondition)

검증 수단을 명시하는 것만으로는 부족하다. 명시된 측정 명령 자체가 곧 **test
oracle** 이므로, oracle 이 조건의 의도와 다른 것을 측정하면 false REJECT / false
PASS 가 발생한다 ([Test Oracle 정의](https://testrigor.com/blog/what-is-test-oracle-in-software-testing/)).
계약 작성자는 측정 명령을 적은 뒤, 다음 두 가지를 추가로 자체 점검한다.

**(1) 의미 일치 (semantic match)** — 측정 명령이 조건이 의도하는 **대상** 을
정확히 측정하는가? 동일 결과를 내는 듯 보이는 명령도 의미가 다르면 경계 사례에서
엇갈린다.

| 조건 의도 | 잘못된 oracle | 의미 일치 oracle |
| ----------- | -------------- | ----------------- |
| "파일이 git 추적 대상이 아니다 (gitignore 됨)" | `test ! -f <path>` (물리적 부재만 검사 — gitignored 인데 파일은 존재하면 FAIL) | `git ls-files --error-unmatch <path>` 가 비어 있음 (추적 여부를 직접 측정) |
| "변경된 N 개 파일이 모두 머지 대상에 포함됨" | `git diff main...HEAD` (커밋 안 된 변경은 보이지 않음) | "커밋 완료 후 `git diff main...HEAD` 실행" — 전제를 조건에 명시 |

**(2) 상태 전제 (precondition)** — 측정 명령이 특정 **상태** (커밋 완료, 빌드 산출물
생성, 서버 기동) 위에서만 올바른 값을 내는 경우, 그 전제를 조건에 인라인으로
명시한다. Given-When-Then 의 **Given** 절이 이 전제를 담는다 — 전제 없이 명령만
적으면 평가자가 다른 상태에서 실행하여 판정이 엇갈린다.

```text
- [ ] AR-01: Sprint B 변경 6 개 파일이 머지 대상에 모두 포함된다
      (Given: Sprint B 커밋 완료 후 / 측정: `git diff --name-only main...HEAD`
       결과에 6 개 파일이 모두 등장) [exact, enumerated]
```

**규칙:**

- 측정 명령을 적은 직후 "이 명령이 조건 의도를 측정하는가?" 를 자문하라.
  `test`/`grep`/`git diff` 처럼 **존재·부재·차이** 를 보는 명령은 의도(추적 여부 ·
  커밋 포함 여부 등)와 어긋나기 쉽다
- 명령이 상태 의존적이면 `Given:` 또는 "(... 완료 후)" 로 전제를 조건에 박는다
- 의미 일치 oracle 이 명확하지 않으면 조건을 재설계하거나 측정 가능한 다른
  관찰점으로 바꾼다

> **실제 발생 사례 (fit-pal LG-07 / AR-01, 2026-05-29)**: LG-07 은 "`.dart_defines.json`
> 이 gitignore 됨" 의도였으나 측정이 `test ! -f` (물리적 부재) 로 작성되어, gitignore
> 등록은 됐지만 파일이 존재하는 상태에서 REJECT. AR-01 은 `git diff main...HEAD` 가
> 커밋 전 상태로 실행되어 6 개 중 2 개만 보여 REJECT. 두 건 모두 oracle 의 의미·전제를
> 조건에 명시했다면 사전에 해소 가능했던 케이스 (Improvement Suggestion: "측정을
> `git ls-files` 로 변경", "커밋 완료 전제 명시").

##### Diff-Scope Oracle 표준형 (E3 — 자유 서술 금지)

> **승급 사유:** 같은 결함이 **3 회 재발**했다. AR-01 (fit-pal-app 2026-06-11, 계약이 `lib/` 단일
> 파일을 요구했는데 `git diff --stat HEAD` 에 다른 파일이 잡힘) · AR-01 (2026-06-29, 미커밋 codegen
> 산출물 `realtime_connection_controller.g.dart` 가 diff 에 섞여 "변환 헬퍼만 변경" 조건 불충족) ·
> Improvement (2026-07-21, "AR-01/AR-02 는 unstaged working tree 에서 측정이 모호 — `git diff --cached`
> 기준 권고"). E1 문장을 세 번 다듬었으므로 **표준형을 강제**한다 (skill-design-guide §3.7 승급 규칙).

"변경 범위" 를 조건으로 쓸 때 `git diff` 를 자유 서술로 적지 마라. 아래 **4 요소를 모두 채운
표준형**만 허용한다. 하나라도 빠지면 조건을 다시 써라.

| # | 요소 | 이유 |
| - | ---- | ---- |
| 1 | **상태 전제** — `Given: 커밋 직전 working tree` 또는 `Given: 스테이징 완료 후` 중 하나를 명시 | `HEAD` / `--cached` / `main...HEAD` 는 서로 다른 집합을 본다. 평가자가 다른 상태에서 실행하면 판정이 뒤집힌다 |
| 2 | **경로 한정 pathspec** — `-- <path>` 로 대상 디렉토리를 좁힌다 | 병렬 세션·무관 변경이 섞여 들어온다 |
| 3 | **생성물 제외** — `':(exclude)*.g.dart'` 처럼 codegen·락파일·빌드 산출물을 pathspec 으로 뺀다 | 미커밋 codegen 이 scope 조건을 깨뜨린 것이 2026-06-29 REJECT 의 직접 원인 |
| 4 | **기대 집합** — 결과가 "정확히 N 행" 인지 "이 목록과 일치" 인지 명시 | "포함한다" 와 "일치한다" 는 다른 판정이다 |

```text
Good:
- [ ] AR-01: 이번 스프린트 변경이 변환 헬퍼 2 개 파일로 한정된다 [exact, enumerated]
      (Given: 커밋 직전 working tree ·
       측정: `git diff --name-only HEAD -- app/lib ':(exclude)*.g.dart' ':(exclude)*.freezed.dart'`
       결과가 `app/lib/data/mapper/schedule_mapper.dart`,
       `app/lib/data/mapper/group_mapper.dart` 2 행과 정확히 일치)

Bad:
- [ ] AR-01: lib/ 단일 파일만 변경된다 (측정: `git diff --stat HEAD`) [exact]
      ← 상태 전제 없음 · 경로 한정 없음 · 생성물 제외 없음 · "일치/포함" 불명확
```

**추가 규칙:**

- 계약 작성 시점에 **그 명령을 실제로 1 회 실행**하고 현재 출력(baseline)을 계약 서술 절에 붙인다.
  실행해보지 않은 측정 명령은 oracle 이 아니라 추측이다
- 커밋 후 판정이 전제라면 조건에 `Given: 스테이징 완료 후` 를 쓰고 `--cached` 를 사용한다.
  구현 중 자가 확인이 목적이면 `HEAD` 기준 working tree 를 쓰되 전제를 그렇게 적는다
- 브랜치 비교(`main...HEAD`) 는 **커밋이 끝난 뒤**에만 유효하다 (LG-07/AR-01 절 참조)
- **경로 목록은 "기대 집합" 한 곳에서만 관리한다.** 같은 경로 집합을 산문과 측정 명령 양쪽에
  적으면 한쪽만 고쳐지는 순간 계약이 자기모순에 빠진다. 산문에는 **개수만** 쓰고
  (`정확히 N 경로로 한정된다`) 열거는 요소 4 에서만 한다 (스키마 §측정 커버리지 표기 의
  화이트리스트 예외 규정)
- **판정 기준(working tree / staged / branch diff)을 전역으로 하나 고정하지 않는다.** 실측
  REJECT 4 건 중 2 건은 커밋 후(`git show --name-only`), 2 건은 미커밋 상태에서 측정됐다 —
  하나를 강제하면 반대편이 항상 어긋난다. 대신 **조건마다 요소 1(`Given:`)이 상태를 고정하고,
  그 상태에 맞는 명령을 정확히 1 개만 둔다.**

##### 증거 아티팩트 존재 의무 (Evidence Artifact Availability)

> **출처:** 글로벌 REJECT UI-06 (fit-pal-app 2026-07-13 — "시안 승인 기록 artifact 부재 — goal
> 조건의 측정 근거 확인 불가") · 대응: [`skill-design-guide.md §3.7`](skill-design-guide.md)
> Completion Evidence Gate 의 계약 측 짝

측정 방법을 적었는데 **그 측정이 읽을 대상이 세상에 없으면** 조건은 판정 불가다. 특히 승인 기록,
합의 로그, 실측 수치처럼 **사람이 남겨야만 생기는 증거**에 의존하는 `[goal]` 조건이 위험하다.

**규칙:**

- 조건이 참조하는 증거가 코드·파일·명령 출력이 아니라 **기록물**이면, 그 기록물이 평가 시점에
  존재할 **경로를 조건에 적는다**. 경로를 적을 수 없으면 그 조건을 만들지 마라
- 기록물은 계약과 같은 곳(`.harness/` 하위) 또는 소스 주석에 남긴다 — 대화 로그는 증거가 아니다
- "사용자가 승인했다" 를 조건으로 쓰고 싶으면, 승인 **행위**가 아니라 승인 **기록 파일의 존재**를
  조건으로 쓴다

```text
Bad:  - [ ] UI-06: 최종 시안이 사용자 승인을 받았다 [goal]
      ← 평가 시점에 확인할 대상이 없음 → 판정 불가 → REJECT
Good: - [ ] UI-06: 채택 시안 ID 와 승인 일시가 `.harness/design-approval.md` 에 기록되어 있다
            [structural] (측정: 해당 파일 존재 + 시안 ID 1 건 이상)
```

### 계약 봉인 — Write-Once Seal (E3)

> **출처:** 글로벌 REJECT `AR-04` 4 건 (fit-pal 2026-08-11) · improvement `[LG-02, LG-04]
> write-once 계약 원문이 amendment 로 대체된 채 남아있다` (2026-08-12) ·
> 포맷 정의는 [`contract-schema.md`](../../references/contract-schema.md) §계약 봉인 이 SSOT 다.
>
> **현재 등급: E3** (§원칙별 Enforcement 등급 참조)

**계약은 write-once 다.** 사용자 승인 후에는 조건 문구를 고치지 않는다. 바꿔야 하면 사이드카에
쓴다. 이 규칙 자체는 새 것이 아니다 — 직전 사이클(2026-07-28)이 이미 amendment 사이드카를
도입했다. 그런데도 **다음 사이클에 바로 재발**했다.

#### 재발한 이유 — 근본원인 3 개

문장을 한 줄 더 추가하면 6 번째 재발이 난다. 실측으로 규명한 원인은 셋이고, **셋을 다 막아야
끊긴다.**

| # | 근본원인 | 실측 |
| ------ | ------ | ------ |
| RC1 | 규칙이 **읽기 측 문서에만** 있었다 | `grep -rn 'write-once'` — `qa-evaluator.md` · `qa-evaluation-guide.md` 에는 있고 **본 가이드와 `sprint-contract/SKILL.md` 에는 0 건**이었다. 본문을 편집한 주체는 REJECT 문구 그대로 "생성자" 인데, 생성자가 읽는 문서에 규칙이 없었다 |
| RC2 | 준수 경로의 **기대 보상이 위반 경로보다 낮았다** | 같은 날 *"amendment A-01은 prompt-log 앵커 부재로 unknown 분류, PASS 근거 불가"* — 사이드카를 실제로 썼는데 효력이 0 이었다. 다음 시도에서 본문 직접 편집으로 전환됐다 |
| RC3 | 위반이 **탐지되지 않았다** | 저장 검사 게이트는 헤더와 조건 **개수**만 본다. 문구를 바꿔도 개수가 같으면 통과한다 |

RC1 은 **Cross-Surface Parity 결손**이다 — 이 레포가 이미 이름을 가진 실패 모드다. RC2 는
§Amendment 방향 판정 이 해소한다. RC3 이 본 절의 대상이다.

#### 규칙

- 사용자 승인 직후 계약을 **봉인**한다: 조건 체크박스 줄만 정규화 해시해 frontmatter
  `conditions_digest` 와 `locked_at` 에 기록한다 (계산식은 스키마 §계약 봉인).
- **봉인 이후 조건 줄을 편집하지 마라.** 자신이 만든 산출물을 사후에 허용하려고 조건 문구를
  넓히는 것이 실측된 위반 형태다.
- 체크박스 토글과 서술 섹션 보강은 봉인을 깨지 않는다 — **일부러 그렇게 설계했다.** 정상 작업을
  막는 게이트는 우회되고, 우회된 게이트는 통과 기록으로 안전을 오해하게 만든다.
- `SEAL_BROKEN` 을 만나면 **조용히 다시 봉인하지 마라.** 그것은 위반을 지우는 행위다.
  `recorded` / `actual` 두 값과 함께 보고하고, 변경 의도가 정당하면 사이드카로 기록한다.
- 레거시 계약(봉인 필드 없음)은 `SEAL_ABSENT` 이며 **경고이지 실패가 아니다.** 소급 봉인 금지 —
  원문이 무엇이었는지 증명할 수 없는 봉인은 봉인이 아니다.

**트레이드오프:** 봉인은 조건 문구의 **불변성**만 보장한다. 조건이 애초에 옳았는지는 보장하지
않으며, 계약이 실제로 잘못됐을 때 수정 비용을 사이드카 쪽으로 밀어낸다. 그 비용을 감당 가능하게
만드는 것이 다음 절이다.

### Amendment 방향 판정 — Direction × Consent

> **출처:** REJECT *"amendment A-01은 prompt-log 앵커 부재로 unknown 분류, PASS 근거 불가"*
> (fit-pal 2026-08-11) · 포맷은 [`contract-schema.md`](../../references/contract-schema.md)
> §Amendment 사이드카 가 SSOT 다.
>
> **현재 등급: E2** — direction 판정 결과가 사이드카에 아티팩트로 남는다.

v5 의 amendment `유형` 은 **강화/완화 방향**과 **사용자 동의 유무**를 한 축에 뭉쳐 놓았다.
그래서 앵커가 없다는 이유만으로 방향 판정까지 `unknown` 이 되었고, 사이드카를 성실히 쓴
스프린트가 아무 효력도 얻지 못했다. **준수 경로의 보상이 0 이면 사람은 위반 경로를 택한다** —
이것이 RC2 다. 두 축을 분리한다.

- **direction 은 PASS 집합의 증감으로 판정한다.** "범위 축소" 라는 말로 판정하지 마라 — 무엇의
  범위인지에 따라 정반대가 된다. 허용 경로를 줄이면 PASS 집합이 줄어 `narrowing`, 요구 대상을
  줄이면 PASS 집합이 늘어 `relaxing` 이다.
- **집합형 조건(경로 화이트리스트 · 파일 열거 · 대상 목록)의 direction 은 자기신고하지 말고
  계산한다.** 실측 위반(3 경로 → 5 경로)은 계산상 `relaxing added=2 removed=0` 이다 — "범위
  조정" 이라고 부를 여지가 사라진다.
- `narrowing` 은 consent 와 무관하게 PASS 근거가 된다. 제약을 **강화**하는 방향이라 남용이
  구조적으로 불가능하다.
- `relaxing` 은 사용자 앵커가 있을 때만 PASS 근거다. 승인 주체는 사용자뿐이며 reviewer 확인을
  추가 요건으로 두지 않는다 (§Cross-Surface Parity item 12 의 착지 구조 — 평가자는 계약에 없는
  요구를 만들지 않는다).
- **앵커가 없으면 `unanchored` 라고 쓰는 것이 정답이다.** 앵커를 지어내면 `narrowing` 까지 함께
  무효가 된다.

**트레이드오프:** `narrowing · unanchored` 를 PASS 근거로 허용하면, 방향 판정을 잘못한
amendment 가 통과할 여지가 생긴다. 그래서 집합형은 **계산**을 요구하고, 계산이 불가능한
서술형 amendment 는 `unknown` 으로 남겨 표면화한다.

### 측정 커버리지 — 산문이 요구한 것과 측정이 훑는 것 (E2 검출기)

> **출처:** improvement *"[AR-04] 계약-측정-불일치 — 조건 프로즈(화이트리스트 12항목)와 측정
> 필드(5개 무관 디렉토리 grep)의 커버리지 갭. 측정 필드에 화이트리스트 개별 대조를
> 포함시켜라"* (2026-08-12). 요구사항마다 검증 접근을 식별하고 trace 가 parent requirement 를
> "fully addresses" 하는지 **독립 평가**하라는
> [NASA verification matrix](https://www.nasa.gov/reference/appendix-d-requirements-verification-matrix/)
> · [NASA 요구사항 관리](https://www.nasa.gov/reference/6-2-requirements-management/) 규약과 같은 문제다.
>
> **현재 등급: E2 (검출기)** — 자동 FAIL 판정기가 아니다.

검증 수단을 적었는지(§검증 수단 명시 의무)와 그 수단이 **조건이 요구한 대상 전부를 훑는지**는
다른 문제다. 후자를 재지 않으면 "측정 방법을 명시하고도 엉뚱한 것을 잰" 계약이 통과한다.

**규칙** — `enumerated` 조건은 산문 측 대상과 측정 측 대상을 **같은 표기**(백틱 · 공백 없는
토큰)로 적는다. 상위 패턴 하나로 여러 대상을 덮을 때는 **작성 시점에 그 명령을 1 회 실행해
확장 결과를 측정 절에 열거**한다. 실행하지 않은 커버리지 주장은 추측이다. 표기 규약과 검출기
스니펫은 스키마 §측정 커버리지 표기 가 SSOT 다.

**왜 blocking 게이트가 아닌가 (실측)** — 2026-08-13 에 이 레포 계약 109 개(`enumerated` 조건
114 개)에 검출기를 걸었다.

| 검출기 변형 | flagged |
| ------ | ------ |
| 나이브 (백틱 토큰 전부 · 1 개 이상) | **76 / 114** |
| 경로형 토큰 · 2 개 이상 | **29 / 114** |

표본을 열어 보면 상당수가 "상위 명령이 실제로 덮는" 정당 케이스이거나, 백틱 토큰이 대상이
아니라 조건의 **주어**(대상 파일 자체)인 경우다. 오탐이 이 정도면 자동 FAIL 은 정상 계약을
막는다. lexical ambiguity linter 를 자동 판정기가 아니라 **"검출기 + 사람의 해소 기록"** 으로
써야 한다는 [SREE 의 접근](https://cs.uwaterloo.ca/~dberry/ambig.in.RSs.html)과 같은 결론이다 —
lexical scope 에서 recall 을 높이고 false positive 는 사람이 판단한다.

따라서 `UNCOVERED` 1 건마다 **(a) 조건을 고치거나 (b) 서술 절에 해소 기록 한 줄**을 남긴다.

### 인자 매트릭스 — Factor Matrix

> **출처:** REJECT `LG-01` *"3 visibility x 6 relation = 18 케이스 중 15케이스(5 relation)만
> 재현. GroupMemberAndFollower 관계가 전체 누락"* · `LG-01` *"16종 매핑 단위 테스트 커버리지
> 부족 (2종만 검증)"* · `UI-04` *"B3(단일 컬럼)과 B6(조밀 로그)이 계약 지정 4축 전부에서
> 동일값"* (전부 2026-08-11~12) ·
> [NIST Combinatorial Testing](https://csrc.nist.gov/Projects/automated-combinatorial-testing-for-software/faqs)
> · [Combinatorial coverage measurement](https://www.nist.gov/publications/combinatorial-coverage-measurement)
>
> **현재 등급: E2** (조합 케이스 수 산출). variant 용법의 등급은 `skill-design-guide.md`
> §3.7 등급 원장의 Variant Budget 행이 정한다 — 여기서 재정의하지 않는다.

축이 **2 개 이상**이고 그 곱이 조건의 의미를 결정할 때만 쓴다. 축 하나짜리 조건이나 작은
변경에 강요하면 과잉 절차다.

- 축과 축 값을 조건에 열거하고, 값의 **출처를 코드의 공유 상수/enum** 으로 지정한다. 테스트가
  값을 재입력하면 다시 어긋난다 (improvement: *"audience_matrix.rs 의 6 relation 을
  feed_integration.rs 가 상수/enum 으로 재사용해 … 기계적으로 순회하게 만들면 수 불일치 재발
  방지"*).
- **`cases_total` 을 손으로 적지 마라.** 곱을 산출하는 명령을 조건에 적고 그 출력을 쓴다.
  사람이 옮겨 적는 숫자 필드는 이 가이드가 이미 `conditions:` 에서 3 회 연속 틀린 형태다.
- 기본은 **full Cartesian**. pairwise 로 낮추려면 곱셈 결과와 사유를 서술 절에 적고 사용자
  승인을 받는다. 임계 숫자를 지어내지 않는다. combinatorial coverage 는 statement/branch
  coverage 와 **다른** 정적 test-set 속성이므로, 기존 커버리지 수치로 대체할 수 없다.

**두 번째 용법 — variant 구별성.** 탐색형 스프린트(시안 · 목업 · 변주)는 같은 매트릭스를
variant 쪽에 쓴다. variant 마다 축 값 조합을 `[exact, enumerated]` 로 열거하고 **동일 조합이
2 개 이상이면 FAIL** 이다. 축을 지정하는 것만으로는 부족하다 — `UI-04` 는 계약이 4 축을
지정했는데도 두 variant 가 4 축 전부 동일값이었다. 스킬 측 짝은 `skill-design-guide.md`
§5.6 Variant Budget 의 Variant Matrix 이며, 계약은 그 매트릭스를 **조건으로** 받는다.

### 음성 대조 — Negative Control

> **출처:** REJECT `ER-02` *"신규 통합 테스트가 실제 바이너리를 호출하지 않고 독립적으로
> 재작성한 SQL로 낙관적 동시성의 일반 동작만 검증한다. **mutation test로 확정 — 실제 코드에서
> 동시성 가드(WHERE exercises = $3::jsonb)를 완전히 삭제해도 이 테스트는 여전히 통과한다**"*
> (2026-08-12) · 동형 `LG-01` · `LG-03`.
>
> **근거의 성격:** 이 조항의 근거는 **이 레포의 실측 REJECT 코퍼스**다. 외부 문헌 앵커는 이번
> 사이클에 확보하지 못했으므로 인용하지 않는다.
>
> **현재 등급: E2** — 음성 대조 절이 조건에 아티팩트로 남는다.

측정 명령이 존재하고(§검증 수단 명시 의무) 의미도 맞는데(§측정 명령 타당성) **구현과 결합되어
있지 않은** 경우가 있다. 구현을 통째로 지워도 측정이 통과하면 그것은 oracle 이 아니다.

**적용 범위 (한정)** — 조건이 **테스트·실행 산출물로 판정**될 때만 필수다. 파일·섹션 존재를
보는 `[structural]` 조건에는 적용하지 않는다 — 대상을 지우면 자명하게 실패하므로 무의미하고,
전 조건에 강요하면 계약 작성 비용만 오른다.

**규칙:**

- 조건에 `음성 대조:` 절을 넣고 **어느 구현 지점을 무력화하면 그 측정이 FAIL 하는지** 적는다.
- 측정이 구현을 **직접** 호출하는지 확인한다. 테스트가 로직을 재작성해 검증하면 결합이 없다 —
  바이너리·함수·쿼리를 그대로 호출하는 경로로 바꾼다 (improvement: *"UPDATE 호출부를 main()에서
  별도 함수로 추출해 … 실제 스킵 카운터가 증가하는 것을 관찰하는 형태로 재작성하라"*).
- 작성 시점에 음성 대조를 실제로 돌릴 수 없으면 **그 사실을 조건에 적는다.** "돌렸다" 고 적지 마라.

```text
Bad:  - [ ] ER-02: 낙관적 동시성 가드에 대한 테스트가 존재하고 통과한다 [structural]
      ← 구현을 지워도 통과하는 테스트가 이 조건을 만족시킨다
Good: - [ ] ER-02: 낙관적 동시성 가드가 conflict 경로를 실제로 막는다 [goal]
            (측정: 대상 행을 사전 변형한 뒤 실제 바이너리를 호출해 skipped 카운터 증가 관찰 ·
             음성 대조: 가드 술어를 제거하면 이 측정이 FAIL 해야 한다)
```

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

### 계약 파일 헤더 2 계층 — 조건 섹션 / 서술 섹션

> **출처:** reflect-digest `parser-incompatible-contract-section` (usc=true) ·
> 스키마 정의: [`contract-schema.md §허용 섹션 헤더`](../../references/contract-schema.md)

기존 규칙은 "허용 헤더는 카테고리 + Anti-patterns / Reusability / Diagnostics 뿐" 이었는데,
실제 계약(특히 카이젠 계약)은 배경·리서치 소스·GAP 분석·범위 경계를 상시 사용해 왔다.
**규칙이 실사용과 어긋나 있었기 때문에** 재위반이 반복됐다. 그래서 규칙을 강화하는 대신
**헤더를 두 계층으로 분류**한다.

| 계층 | 허용 헤더 | 조건 체크박스 |
| ---- | --------- | ------------- |
| **조건 섹션 (parsed)** | `project.yaml.contract_categories` 의 각 `id` + `Anti-patterns` + `Reusability` + `Diagnostics` | **여기에만** `- [ ] {PREFIX}-{NN}:` 형태로 존재 |
| **서술 섹션 (non-parsed)** | `배경` · `리서치 소스` · `GAP 분석` · `범위 경계` · `회귀 게이트` | 조건 체크박스 **금지** (일반 불릿만) |

- **조건 섹션 헤더는 정확히 일치**해야 한다 (괄호 부연 금지). **서술 섹션 헤더는 위 5 개 중
  하나로 시작**하면 되고 뒤에 부연을 붙일 수 있다 (`## GAP 분석 (리서치 vs 현재 가이드)` 허용)
- 위 두 목록 밖의 헤더(`Notes`, `Appendix`, `메모` 등)는 **금지**다 — 평가자 파서가 조건 섹션인지
  서술인지 판정할 수 없다
- 서술 섹션에 `- [ ]` 를 쓰면 평가자가 조건으로 오인해 존재하지 않는 조건을 판정하려 든다
- 이 규칙은 E3 다 — sprint-contract 는 저장 직후 결정론적 헤더 검사를 실행한다

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
| ---------- | ------ | ----------- |
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
| 측정 oracle 의미·전제 불일치 | 측정 명령은 적었으나 그 명령이 조건 의도와 다른 것을 측정하거나(예: gitignore 의도에 `test ! -f`) 상태 전제 누락(커밋 전 `git diff`) → false REJECT/PASS | 의미 일치 oracle 선택 + 상태 의존 시 `Given:` 전제를 조건에 인라인 명시 (LG-07/AR-01 재발 방지) |
| Sibling 스킬 커버리지 누락 | 공통 원칙이 plugin 내 여러 스킬에 적용돼야 하지만 계약이 단일 스킬만 점검 → 일부 스킬에만 적용된 상태 통과 | `[exact, enumerated]` + 스킬 숫자/이름 전부 열거로 sibling 전수 요구 (rust-kit H-01/H-03 재발 방지) |
| 정성적 수식어 사용 | "충분히", "상당한", "적절히", "대부분" 등 binary 판정 불가 수식어 | 구체 수치/기준값으로 대체 또는 조건 분리 (Binary Decidability Pre-Check 실패 1 순위) |
| 한쪽 면만 계약 | 계약·직렬화·공유 모델을 바꾸는데 producer 조건만 있고 consumer 조건이 없음 → 서버만 고치고 클라이언트는 다음 스프린트로 밀림 | producer/consumer 를 **별도 조건 2 개**로 분리하고 각 면의 파일 경로를 `[exact, enumerated]` 로 열거 (insights Friction #4 재발 방지) |
| preamble–조건 모순 | 계약 서두의 설계 의도와 조건이 서로 다른 것을 요구 → 구현자가 조용히 한쪽만 따르고 평가자는 다른 쪽으로 판정 | DRAFT 제시 전 서술↔조건 방향 대조 + 열거한 기존 식별자 grep 존재 확인 (RE-02 재발 방지) |
| diff-scope oracle 자유 서술 | `git diff` 를 상태 전제·경로 한정·생성물 제외·기대 집합 없이 적음 → 미커밋 codegen 혼입, working tree/staged 해석 차이로 판정 뒤집힘 | Diff-Scope Oracle **표준형 4 요소**를 전부 채우고 작성 시점에 명령을 1 회 실행해 baseline 첨부 (AR-01 3 회 재발 방지) |
| `[exact]` 산출물 오분류 | 조건 문장에 테스트·문서 산출물이 등장하는데 이번 스프린트에 낼 생각이 없음 | 낼 것이면 산출물 경로까지 조건화, 아니면 `[goal]` 로 낮추거나 산출물 문구 제거 (UI-07 재발 방지) |
| 증거 없는 goal 조건 | 승인 기록·합의 로그처럼 사람이 남겨야 생기는 증거에 의존하는데 그 기록물이 존재하지 않음 → 판정 불가 | 증거 기록물의 **경로**를 조건에 명시하고, 경로를 못 적으면 조건을 만들지 않음 (UI-06 재발 방지) |
| 미분류 섹션 헤더 | 조건 섹션도 서술 섹션도 아닌 헤더(`Notes` 등) 추가, 또는 서술 섹션에 `- [ ]` 조건 배치 → 평가자 파서 오작동 | 헤더 2 계층 허용 목록만 사용 + 저장 직후 결정론적 헤더 검사 (`parser-incompatible-contract-section` 재발 방지) |

---

## 자기개선 메커니즘

### 구조화 진단 체크리스트

sprint-contract 실행 완료 후 다음 항목을 자가 점검한다:

| 항목 | 점검 내용 |
| ------ | ----------- |
| ambiguous_conditions | 모호한 표현이 포함된 조건이 있는가? (아래 모호성 분류 참조) |
| missing_error_paths | 에러/예외 경로에 대한 조건이 누락되었는가? |
| untestable_conditions | 코드만으로 검증 불가능한 조건이 있는가? |
| category_coverage_gap | project.yaml 카테고리 중 커버하지 못한 것이 있는가? |
| complexity_underestimate | 복잡도를 과소평가하여 조건 수가 부족한가? |
| implementation_leakage | 조건에 내부 구현 용어(클래스명, 메서드명, DB명)가 포함되었는가? |
| nfr_coverage | 해당 기능의 비기능 요구사항(성능/보안/접근성)이 조건에 반영되었는가? |
| boundary_without_measurement | 경계값(>=, <=, ==) 조건에 측정 방법이 누락되었는가? |
| format_granularity_missing | 포맷 일관성 조건에 적용 수준(file/section/field)이 명시되었는가? |
| counterpart_missing | 계약·직렬화·공유 모델 변경인데 consumer 면 조건이 누락되었는가? |
| preamble_condition_conflict | 서술 절의 설계 의도와 조건이 서로 다른 것을 요구하는가? |
| diff_oracle_nonstandard | 변경 범위 조건이 Diff-Scope Oracle 표준형 4 요소(상태 전제/경로 한정/생성물 제외/기대 집합)를 다 채웠는가? |
| evidence_artifact_missing | `[goal]` 조건이 참조하는 증거 기록물의 경로가 조건에 명시되었는가? |
| section_header_unclassified | 조건 섹션도 서술 섹션도 아닌 헤더가 있거나, 서술 섹션에 `- [ ]` 조건이 들어갔는가? |
| contract_seal_missing | 사용자 승인 후 `conditions_digest` / `locked_at` 을 기록하고 검증 출력을 인용했는가? |
| measurement_coverage_gap | `enumerated` 조건에서 검출기가 `UNCOVERED` 를 낸 건마다 수정 또는 해소 기록을 남겼는가? |
| factor_matrix_missing | 2 개 이상 축의 곱이 의미를 결정하는 조건에 축·축 값·`cases_total` 산출 명령이 있는가? |
| negative_control_missing | 테스트 통과를 요구하는 조건에 `음성 대조:` 절이 있는가? |
| amendment_direction_uncomputed | 집합형 amendment 의 direction 을 자기신고하지 않고 집합 비교로 계산했는가? |

### 모호성 분류 (Ambiguity Taxonomy)

조건 검토 시 다음 3가지 유형의 모호성을 구분하여 점검한다:

| 유형 | 설명 | 예시 | 수정 |
| ------ | ------ | ------ | ------ |
| 어휘적 (Lexical) | 단어 자체가 여러 의미 | "처리한다", "관리한다" | 구체 동사로 대체 ("반환한다", "저장한다") |
| 구문적 (Syntactic) | 문장 구조가 여러 해석 허용 | "A와 B를 포함하는 C" | 분리하여 각각 명시 |
| 의미적 (Semantic) | 도메인 맥락 없이 해석 불가 | "적절한 응답" | 구체적 상태 코드/값으로 명시 |

이 3 분류는 **조건 문장**의 모호성을 본다.
[Tjong/Berry 의 lexical / syntactic / semantic 분류](https://cs.uwaterloo.ca/~dberry/FTP_SITE/tech.reports/TjongThesis.pdf)
는 이 guiding rules 를 inspection checklist 로 쓸 수 있다고 본다. **자동 판정기로 쓰지 마라** —
LLM 에게 "이 조건 모호한가?" 만 묻는 게이트는 판정 근거를 남기지 않는다.

#### 측정 모호성 — QA 태그의 되먹임 (v5.0 추가)

평가자가 improvement 에 반복해 붙이는 태그는 **작성 단계에서 미리 잡을 수 있는 결함 목록**이다.
문장이 아니라 **측정** 쪽 모호성을 본다는 점에서 위 3 분류와 다르다. 6 항의 자문 목록과 예시는
[`contract-schema.md`](../../references/contract-schema.md) §조건 작성 preflight 가 SSOT 다 —
여기서 표를 복제하지 않는다. 실측 태그: `측정-수단-부재` · `측정-방식-불일치` ·
`측정-환경-오염` · `측정-산출물-부재` · `검증경로-미기재` · `측정-중복`.

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

### 계약 설계에 전수된 parity items (7 개)

| # | Parity Item | skill-design-guide 위치 | agent-design-guide 위치 | **contract-design-guide 대응 위치 (이 가이드)** |
| --- | ------------- | ------------------------ | ------------------------ | ------------------------------------------------ |
| 1 | 계약 모호성 방지 / Binary Decidability | §3.5 (QA 계약과 1:1 매칭) | §3.5 (Binary Decidability Pre-Check) | **§조건 작성법 > "계약 작성자 의무 — 이진 판정 가능성"** |
| 2 | 트리거 키워드 배타성 (substring 포함) | §4 (set intersection + substring) | §3 + §10 (sibling agent 검사) | **§sprint-contract SKILL.md Process Step (키워드 검사 의무)** |
| 3 | 미검증 항목 정책 | — (스킬 전용 아님) | §10 Unverifiable 조건 정책 | **§조건 작성법 > "검증 수단 명시 의무" (3 단계 fallback)** |
| 11 | Enforcement 등급 (E1/E2/E3) | §3.7 (등급 정의 · 승급 규칙 — SSOT) | §6 패턴 7 (훅 = E3 게이트) | **§원칙별 Enforcement 등급 (계약 원칙 현재 등급표)** |
| 12 | Counterpart Enumeration | §5.5 (변경의 반대편 열거) | — (평가자는 계약 조건으로 수용) | **§조건 작성법 > "양면 조건 — Counterpart Conditions"** |
| 13 | Variant Budget ↔ Exploration Budget | §5.6 (산출물 개수·축 고정) | §7 (탐색 turn 예산) — **구분 대상** | **§조건 작성법 > "인자 매트릭스" 의 variant 용법** (축 값 조합 중복 = FAIL) |
| 14 | User-Reported Failure Gate | §3.8 (사용자 관측은 재현 대상) | §10 (사용자 보고 우선 — 평가자 측) | — (계약 측 착지 없음. 완료 판정 시점의 규약이라 **평가 레이어 소관** — Phase 3) |

> 두 가이드의 item 1 · item 4 (rule-by-rule audit) 는 contract 가이드에
> 해당 위치 없이 qa-evaluation-guide 로 위임된다 (중복 배제).
>
> **item 12 의 착지 구조**: skill-design-guide §5.5 는 생성 측(편집 전 열거)을, 본 가이드는
> 계약 측(조건화)을 담당한다. qa-evaluation-guide 에는 대응 절을 두지 **않는다** — 평가자는
> 계약에 박힌 Counterpart 조건을 일반 조건으로 판정하면 되고, 별도 평가 규칙을 두면 계약에
> 없는 요구를 평가자가 만들어내게 된다. 따라서 이 원칙의 유일한 강제 지점은 **계약 작성자**다.
>
> **item 11 의 착지 구조**: 등급 정의·승급 규칙·**등급 원장**은 skill-design-guide §3.7 이
> SSOT 이고, 본 가이드는 **계약 레이어 고유 원칙의 등급 목록**만 유지한다. 등급 어휘(E1/E2/E3)를
> 재정의하거나 동의어를 만들지 말고, 원장에 있는 원칙의 등급값을 계약 등급표에 다시 적지 마라.
>
> **item 13 의 착지 구조**: skill-design-guide §5.6 은 **생성 측**(산출물 개수 상한 · 축 고정 ·
> Variant Matrix 아티팩트)을, 본 가이드 §인자 매트릭스는 **계약 측**(축 값 조합을 조건으로 열거 ·
> 중복 조합 FAIL)을 담당한다. agent-design-guide §7 "Exploration Budget" 은 이름만 비슷한 **다른
> 개념**(탐색 turn 예산)이며 계약 측 대응이 없다 — 두 이름을 섞지 마라.
>
> **item 14 는 계약 측 착지가 없다.** `REOPENED` 는 **완료 판정 시점**의 상태어이므로 계약 작성
> 레이어가 아니라 평가 레이어(qa-evaluator · qa-evaluation-guide)에 착지한다. 계약에
> "사용자가 깨졌다고 하면 REOPENED" 같은 조건을 만들면, 평가 시점에 읽을 대상이 없는
> 조건이 되어 §증거 아티팩트 존재 의무 위반이 된다.

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
- **RE-02 (fit-pal, 2026-07-22)**: 계약 preamble 이 단방향 설계를 서술했는데 조건은 양방향 함수를 literal 로 열거 → 구현은 preamble 을, 평가는 조건을 따라 REJECT (v4 Preamble–Condition Consistency 로 해소)
- **AR-01 (fit-pal-app, 2026-06-11 / 2026-06-29 / 2026-07-21)**: 변경 범위 조건의 `git diff` oracle 이 상태 전제·경로 한정·생성물 제외 없이 작성되어 3 회 REJECT/재확인 권고 (v4 Diff-Scope Oracle 표준형으로 해소 · E1 → E3 승급)
- **UI-06 / UI-07 (fit-pal-app, 2026-07-13)**: goal 조건의 증거 기록물이 존재하지 않아 판정 불가 / `[exact]` 조건에 명시된 widget test 미제출 (v4 증거 아티팩트 존재 의무 · 산출물 동반 제출 규칙으로 해소)
- **AR-04 (fit-pal, 2026-08-11 · 4 건)**: 경로 화이트리스트 위반이 연속 발생하고, 그중 1 건은 **생성자가 계약 조건 문구를 사후 편집**(5→7 경로)해 위반을 소거하려 한 write-once 위반. 직전 사이클의 사이드카(E1 서술) 도입 **다음 사이클에 재발** (v5.0 계약 봉인 E3 로 해소 — 근본원인 3 개를 각각 차단)
- **amendment A-01 (fit-pal, 2026-08-11)**: 사이드카를 성실히 썼는데 prompt-log 앵커가 없어 `unknown` 으로 분류되어 PASS 근거가 되지 못했다. 준수 경로의 보상이 0 이 되어 다음 시도의 본문 직접 편집을 유발 (v5.0 direction × consent 2 축 분리로 해소)
- **LG-01 (fit-pal, 2026-08-11~12)**: `3 visibility x 6 relation = 18` 중 15 케이스만 재현 / 16 종 매핑 중 2 종만 검증 — 조합 케이스 수를 사람이 옮겨 적었다 (v5.0 인자 매트릭스로 해소)
- **UI-04 (fit-pal, 2026-08-12)**: 계약이 4 축을 지정했는데도 두 variant 가 4 축 전부 동일값 — 축 지정만으로는 구별성이 보장되지 않는다 (v5.0 인자 매트릭스 variant 용법으로 해소)
- **ER-02 (fit-pal, 2026-08-12)**: 측정문은 통과하는데 **구현을 완전히 삭제해도 통과**하는 테스트였다 (mutation test 로 확정). 측정 수단·의미·전제를 다 갖춰도 구현과 결합되지 않으면 oracle 이 아니다 (v5.0 음성 대조로 해소)

### Downstream 전파 범위

본 가이드 개정이 영향 줄 수 있는 하위 surface:

- `harness/skills/sprint-contract/SKILL.md` — Process Step, Gotchas
- `harness/references/contract-schema.md` — 스키마 버전 및 필드
- `harness/docs/guides/qa-evaluation-guide.md` — 평가 방법론 (대응 원칙)
- `harness/agents/qa-evaluator.md` — 평가 절차

**2026-08-13 시점 미착지 (Phase 3 소관):** 계약 봉인의 **평가 시점 검사**와 amendment 의
**2 축 해석**은 위 두 평가자 표면에 아직 반영되지 않았다. 계약 작성 측(본 가이드 ·
`sprint-contract/SKILL.md` · `contract-schema.md`)만 이번 사이클 scope 였다. 평가자가
`verify_seal` 을 돌리지 않으면 봉인은 **작성·이어작업 시점에만** 검사되며, `SEAL_BROKEN` 이
verdict 에 반영되지 않는다.

### 버전 정보

값을 손으로 옮겨 적지 마라 — 아래 3 행은 원본 파일에서 추출해 채운다 (drift 실측: 2026-08-13
시점에 Schema version 이 `v4` 로 남아 있었고 실제 스키마는 v5.2 였다).

| 항목 | 값 | 원본 |
| ------ | ------ | ------ |
| Guide version | 2026-08-13 (Phase 2 kaizen · v5.0) | 이 문서 |
| Schema version | v5.3 | `harness/references/contract-schema.md` §스키마 버전 > `현재:` |
| Parity with | skill-design-guide 1.5.0 · agent-design-guide 1.6.0 | 두 가이드 frontmatter `version` |
