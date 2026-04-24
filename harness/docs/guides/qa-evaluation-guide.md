# QA Evaluation Guide

> qa-evaluator 에이전트가 참조하는 평가 방법론.
> evaluator-kaizen이 리서치 기반으로 이 문서를 갱신한다.
>
> **참조 스키마**: `harness/references/contract-schema.md`
>
> **최근 갱신: 2026-04-24 (Phase 3 kaizen · v3 흡수)** — Phase 1/2 Cross-Surface Parity 흡수. Binary Decidability Pre-Check, Rule-by-Rule Audit, `[미검증]` 마커 평가 프로토콜 (1/2건 임계), Sibling Enumerated 전수 Grep 절차, L3 Coverage Honesty 규칙, User-Value/Business-Intent 관점을 평가자 프로토콜로 흡수. 이전: 2026-04-12 수량/경계값 조건 검증 프로토콜 추가 · LLM-as-judge 2026 최신 연구 반영 + contract-schema v2 소비 규칙.

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
| ---- | ---- | --------- |
| 위치 편향 (Position bias) | 먼저 본 항목에 호의적 — IJCNLP 2025 연구에서 Response A 가 68% 선호되는 사례 보고 | **Swap Test**: 조건을 `(A, B)` 순서로 1 회, `(B, A)` 순서로 1 회 총 2 회 평가하고, 두 결과가 일치할 때만 판정 확정. 불일치 시 `[low-confidence]` 강등 + 재검증 ([arxiv 2406.07791](https://arxiv.org/abs/2406.07791), [arxiv 2602.02219](https://arxiv.org/html/2602.02219)) |
| 자기 선호 편향 (Self-preference bias) | LLM 이 자기와 "친숙한"(낮은 perplexity) 출력에 호의적 | generator 와 evaluator 의 컨텍스트를 **물리적으로 분리**(별도 서브에이전트 실행) + 구현자가 쓴 주석·커밋 메시지는 증거에서 제외 ([arxiv 2410.21819](https://arxiv.org/abs/2410.21819)) |
| 장황함 편향 (Verbosity bias) | 긴 코드/설명에 호의적 | 조건 충족 여부만 판단, 코드 양 무시 |
| 점수 분포 편향 (Scoring bias) | 특정 점수대(중간값)에 판정이 몰리는 경향 | 이진 PASS/FAIL 만 사용 — Likert 스케일 금지. 서브체크 단위로 분해하여 모호 영역 제거 ([arxiv 2506.22316](https://arxiv.org/html/2506.22316v1)) |
| 구체성 편향 (Concreteness bias) | 구체적 코드에 추상적 코드보다 호의적 | 계약 조건 충족만 판단, 구현 스타일 무시 |
| 구현 추종 편향 (Implementation-following bias) | 실제 구현을 "정답"으로 간주하는 경향 | 계약 조건(specification)을 먼저 읽고, 코드는 증거 수집용으로만 사용 |
| 지시 해석 불일치 (Instruction-following misalignment) | 평가 기준을 일관되지 않게 해석 | 조건별 boolean 체크리스트 분해로 해석 여지 최소화 |

> **종합 편향 survey**: [A Survey on LLM-as-a-Judge — arxiv 2411.15594](https://arxiv.org/html/2411.15594v6), [Justice or Prejudice? Quantifying Biases in LLM-as-a-Judge — arxiv 2410.02736](https://arxiv.org/html/2410.02736v1) 에서 12 개 이상의 편향을 분류. 본 가이드는 계약 기반 검증 맥락에서 영향이 큰 6 개에 집중한다.
>
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

## Binary Decidability Pre-Check (평가 시작 전 필수)

> **대응:** `agent-design-guide.md §3.5` · `contract-design-guide.md §Binary Decidability` · `skill-design-guide.md §3.5`
>
> **배경:** Phase 1/2 에서 계약 작성자에게 "이진 판정 가능한 조건을 작성하라" 를 강제했지만, 평가자 역시 **조건을 검증하기 전에** 그 조건이 실제로 이진 판정 가능한지 자체 점검해야 한다. 조건이 모호하면 검증 도중 해석이 갈려 오판·재평가 루프가 발생한다 (contract_misinterpret: 7회 진단).

### 원칙

Sprint Contract 의 각 조건에 대해 Step 2 (조건별 정적 검증) 을 시작하기 **전** 에 아래 체크리스트를 전수 실행한다. 모호 조건은 `[미검증]` 또는 REJECT 사유로 명시하고, 평가자가 해석 여지를 임의로 메우지 않는다.

### 사전 체크리스트 (평가 시작 전)

각 조건에 대해 아래 항목을 모두 점검한다:

1. **FAIL 상태 1 문장 테스트** — "이 조건이 FAIL 인 상태를 1 문장으로 기술 가능한가?" 자문. 기술 불가면 조건 모호. 예: "로그인이 잘 동작한다" → FAIL 상태를 1 문장으로 쓸 수 없음 → 모호. 반면 "로그인 실패 시 HTTP 401 반환" → FAIL: "401 이 아닌 응답이 반환됨" 명확
2. **구체성 태그 확인** — 조건 끝에 `[exact]` / `[structural]` / `[goal]` 태그 존재 여부. 미명시면 `[structural]` 로 간주하되 REJECT 사유에 "태그 누락" 플래그
3. **범위어 enumerate 확인** — 조건에 "주요 / 모든 / 대부분 / 핵심 / 일부" 같은 **범위어**가 있으면 포함/제외 목록이 인라인 enumerate 되어 있는지 확인한다. 없으면 평가자가 범위를 자체 해석하지 말고 REJECT 사유에 "범위 미명시" 명시 (SK-02 재발 방지)
4. **검증 수단 존재 확인** — 조건에 "측정: ...", 도구명, 관찰 대상 중 하나가 명시되었는가? 없으면 `[structural]` 기본 fallback 적용하되 REJECT 사유에 "검증 수단 미명시" 명시
5. **`[exact, enumerated]` / `[structural, enumerated]` 대상 목록 확인** — 태그가 enumerated 이면 나열된 대상 N 개가 계약에 실제로 쓰여 있는지 확인. N 이 애매하면 REJECT 사유에 "enumerated 대상 수 불분명"

### 모호 조건 발견 시 대응

- **평가자가 해석을 메우지 않는다.** Phase 1/2 의 one-time rubric refinement 패턴 ([arxiv 2511.10865](https://arxiv.org/abs/2511.10865)) 적용: 해석 차이가 있으면 평가는 문자 그대로 진행 (엄격 쪽), Sprint Feedback 에 계약 수정 권장 명시
- 위 5 개 항목 중 하나라도 미충족이면 해당 조건은 **FAIL 쪽으로 기운 엄격 해석** + Sprint Feedback 의 `contract_ambiguity_notes` 에 "조건 ID — 모호 유형 — 제안 구체화" 기록

### 실패 사례

- **PH-01 (design-kit, 2026-04)**: 평가자가 모호 조건을 자체 해석 → 해석 충돌 → REJECT 반복
- **SK-02 (harness, 2026-04)**: "주요 interactive element" 범위어가 enumerate 되지 않아 평가자가 badge/decoration 포함 여부를 자체 판단 → 구현과 해석 불일치

---

## Rule-by-Rule Audit Before Completion (판정 완료 전 필수)

> **대응:** `skill-design-guide.md §3.6` · `/insights` 마찰점 #1 (Proactive quality gaps)
>
> **배경:** 평가자가 조건 일부만 검증하고 "나머지는 비슷하니까 PASS" 로 뭉뚱그리는 패턴. /insights 리포트에서 "Claude consistently fails to spot obvious improvements that your rules already cover" 로 지적됨. 부분 점검의 유혹을 구조적으로 차단하기 위해 전수 점검 단계를 명문화한다.

### 원칙

Step 4 (판정) 직전에 **모든 계약 조건을 1 회 더 전수 스캔** 한다. 평가 도중 "자명하다"고 넘긴 조건이라도 판정 직전 체크리스트 형식으로 되돌아온다.

### 전수 점검 절차

1. Sprint Contract 의 모든 조건 ID 를 번호순으로 나열한다
2. 각 조건 ID 에 대해:
   - 증거(파일:라인) 가 기록되어 있는가?
   - 검증 깊이 (L1/L2/L3) 가 명시되어 있는가?
   - 구체성 태그 (`[exact]` / `[structural]` / `[goal]`) 에 맞는 검증 방식을 적용했는가?
   - enumerated 조건이면 N 개 대상 전부 개별 증거 수집했는가?
3. 하나라도 결여되어 있으면 해당 조건을 재검증한다. "비슷한 조건이 PASS 했으니 이것도 PASS" 는 금지

### 왜 필요한가 (insights 마찰점 #1)

> "Batch-identify refactor opportunities up front. Before editing any file in a refactoring sweep, have Claude enumerate every applicable rule violation first." — /insights 추천 패턴 #1

평가 역시 같다. 조건별 "생각나는 대로" 점검하면 커버리지 구멍이 생긴다. 판정 직전 **rule-by-rule** 로 1 회 더 돌리면 커버리지 공백이 자동으로 드러난다.

---

## `[미검증]` 마커 평가 프로토콜

> **대응:** `contract-design-guide.md §미검증 마커` · `contract-schema.md v3 §SCH-02` · `agent-design-guide.md §10`
>
> **배경:** mcp_server=null, 런타임 미실행, 외부 도구 미가용 등으로 정적 검증이 불가능한 조건의 **일관된 처리** 를 위해 도입. fit-pal LG-02/DG-04 · fit-pal-flutter 2026-04-17 REJECT 의 근본 원인이었다.

### 마커 부착 절차

외부 도구·MCP·런타임 등으로 검증 불가 시 평가자는 아래 순서를 따른다:

1. **단계 1 (기본 검증)** 시도 — 계약에 기술된 1차 검증 도구 실행
2. 단계 1 실패 시 **단계 2 (Fallback 정적 검증)** 시도 — 계약에 명시된 대체 정적 검증 수행 (예: 파일 Grep, CSS 변수 대조, log 파일 tail)
3. 단계 2 도 실패 시 **단계 3 (`[미검증]` 마커)** 부착 — 근거 블록에 "검증 불가 사유 한 줄 + 사용한 단계 기록"
4. 계약에 fallback 기술이 없으면 **계약 작성자가 누락** 한 것이므로 REJECT 사유에 "fallback 미기술" 플래그

### 카운팅 및 자동 REJECT 임계 (v3 규정)

`[미검증]` 건수는 평가 종료 시 집계하고 아래 규칙으로 판정:

| 미검증 건수 | 평가 결과 |
|------------|----------|
| 0 건 | 통상 판정 |
| 1 건 | PASS 허용 (단, Sprint Feedback 에 "미검증 1 건" 경고 명시) |
| 2 건 이상 | **자동 REJECT** — 개별 조건은 FAIL 이 없어도 전체 verdict 는 REJECT |

### 집계 의무

Step 4 판정 시 평가자는 Sprint Feedback 에 다음을 기록:

```text
## Unverifiable Summary
- 총 미검증 건수: N
- 건 목록: [조건 ID, 사유, 시도한 fallback 단계]
- Verdict 영향: {PASS 허용 | 자동 REJECT}
```

### 실패 사례 (이 프로토콜 없이 발생)

- **fit-pal-flutter 2026-04-17**: 미검증 3 건 (LG-02, DG-03, DG-04) 발생했으나 평가자가 카운팅 규칙을 명시하지 않아 partial PASS 처리 → 추후 REJECT 재판정
- **fit-pal 2026-04-21**: UI-04/LG-04 미검증에도 3 단계 fallback 미수행 → 단계 2 대체 정적 검증 가능했음에도 건너뛰고 바로 [미검증]

---

## Sibling Enumerated Verification (전수 Grep 절차)

> **대응:** `contract-design-guide.md §Sibling Consistency` · `contract-schema.md §Sibling Consistency enumerated`
>
> **배경:** 플러그인 내 여러 스킬에 공통 원칙을 요구하는 조건 (`[exact, enumerated]` / `[structural, enumerated]`) 에서 평가자가 1~2 개 샘플만 확인하고 PASS 처리하는 패턴 방지. rust-kit H-01/H-03 REJECT 의 직접 원인이었다.

### 절차

`[*, enumerated]` 태그 발견 시:

1. **대상 목록 파싱** — 조건 문장에서 나열된 sibling 스킬/파일 이름을 모두 추출. N 개 정확히 센다
2. **N 개 전수 Grep** — 각 대상에 대해 개별 Grep 수행. 한 대상당 한 줄 증거(`파일:라인 매칭 문자열`) 기록
3. **누락 대상명 나열** — 하나라도 Grep 증거가 없으면 해당 조건은 **FAIL**. 누락된 대상명을 모두 나열 (샘플 한두 개만 기재 금지)
4. **카운트 보고** — Sprint Feedback 에 "N 개 중 M 개 충족 (누락: X, Y, Z)" 형태로 집계

### PASS/FAIL 기준

- 모든 N 개 대상에 증거 확보 시 PASS
- 한 개라도 누락 시 FAIL + 누락 대상 전체 명시
- 샘플 1~2 개만 확인하고 "나머지도 비슷할 것" 이라는 PASS 금지

### 실패 사례

- **rust-kit H-01/H-03 (2026-04)**: "domain event + outbox 원칙이 rust-init, rust-feature, rust-service, rust-api 4 개 스킬 Gotchas 에 있다" 조건에서 rust-service 만 확인하고 PASS → 실제로 rust-init/rust-feature/rust-api 3 개 누락 → REJECT
- **react-kit KZ-04 (2026-04)**: References 에 `docs/react/kit-design/` 7 개 그룹 문서 (g1~g6, g5b) 개별 명시 요구였는데 포괄 경로로 처리 → REJECT

---

## 용어 구분 — L1/L2/L3 기호 충돌 주의

> 이 가이드의 **L1/L2/L3**는 **evaluator 검증 깊이**를 의미한다.
> sprint-contract 계약서의 `[L1]/[L2]/[L3]` 태그는 **조건 구체성 레벨**로, 동일 기호지만 의미가 다르다.

| 체계 | 기호 | 의미 | 위치 |
| ---- | ---- | ---- | ---- |
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

> **Phase 2 (2026-04) 이후 권장 표기**: contract-schema v2 부터 계약 조건은 숫자 레벨 `[L1]`/`[L2]`/`[L3]` 대신 문자 태그 `[exact]`/`[structural]`/`[goal]` 을 사용한다. 기존 프로젝트에 남아 있는 `[L1]`/`[L2]`/`[L3]` 태그는 아래 매핑으로 해석한다: `[L1]` ≡ `[exact]`, `[L2]` ≡ `[structural]`, `[L3]` ≡ `[goal]`.

---

## Specificity Tag 소비 규칙

> 근거: Phase 2 contract-schema v2 (2026-04-11). 계약 조건 끝의 `[exact]` / `[structural]` / `[goal]` 태그는 **검증 방식**을 지정한다.

| 태그 | 의미 | evaluator 검증 방식 | 증거 형식 |
| ---- | ---- | ------------------- | --------- |
| `[exact]` | 이름/값/구조 문자 그대로 매칭 | Grep 으로 literal 매칭 → Read 로 맥락 확인 | `파일:라인` + 매칭된 literal 문자열 인용 |
| `[structural]` | 섹션/필드/파일 존재 확인 | Glob/Grep 으로 섹션·필드 존재 확인 → Read 로 구조 검증 (필드 타입, 하위 항목 수 등) | `파일:라인` + 섹션 헤더 또는 필드명 |
| `[goal]` | 목표 달성 여부만 판정, 수단 무관 | Read 로 코드 경로 전체 추적 → 의미 분석 + **다관점 평가** 필수 (기능/엣지/성능/보안 중 최소 2 개) | `파일:라인` + 목표 달성 논증 (왜 이 코드가 목표를 달성하는가) |

**공통 규칙:**

- 모든 태그는 evaluator 검증 깊이 **L3 까지 도달**해야 한다. 태그가 `[exact]` 라고 해서 L1 존재 확인에서 멈추지 않는다.
- `[goal]` 태그는 가장 해석 여지가 크므로 **Recursive Rubric Decomposition (RRD)** 을 적극 적용한다.
- 태그가 명시되지 않은 조건은 `[structural]` 로 간주한다 (contract-schema v2 기본값).
- 태그가 `[L1]`/`[L2]`/`[L3]` 로 남아있는 legacy 계약은 위의 네이밍 충돌 매핑을 따라 해석한다.

**판정 예시:**

조건 `CG-01 [exact]: "조건 구체성 레벨" 표에서 컬럼 이름이 [exact]/[structural]/[goal] 로 교체됨`
→ evaluator 는 해당 파일을 Grep 으로 `[exact]`, `[structural]`, `[goal]` literal 매칭 확인 후 Read 로 맥락 (표 헤더인가? 예시 코드인가?) 까지 검증한다.

조건 `LO-01 [goal]: 로그인 실패 시 사용자에게 실패 원인이 전달된다`
→ evaluator 는 로그인 실패 코드 경로 (datasource → repository → provider → UI) 를 Read 로 추적하고, UI 에서 실제로 사용자에게 전달되는지 렌더 로직까지 확인한다. RRD 적용: ① 실패 감지 ② 원인 분류 ③ 메시지 생성 ④ UI 전달 로 분해.

## Aggregation Mode 소비 규칙

> 근거: Phase 2 contract-schema v2. 다수 대상(파일/모듈/키워드)에 적용되는 조건은 `[enumerated]` 또는 `[collective]` 태그를 가진다.

| 모드 | 의미 | evaluator 검증 방식 | PASS 기준 |
| ------ | ------ | --------------------- | ----------- |
| `[enumerated]` | 각 대상을 개별 이름으로 명시 요구 | 계약 조건에서 대상 목록을 먼저 파싱 → 각 대상별로 개별 Grep/Read → 개별 증거 수집 | 모든 대상에 대해 각각 증거 확보 시 PASS. 하나라도 누락되면 FAIL + 누락 대상명 나열 |
| `[collective]` | 포괄 경로/패턴 하나로 지정 가능 (기본값) | 포괄 경로·패턴 1 건을 Grep/Glob 으로 확인 | 포괄 매칭 1 건 증거로 PASS |

**실패 사례 참고**: KZ-04 REJECT (2026-04-10) — `react-kaizen` References 섹션에 `docs/react/kit-design/` 7 개 그룹 문서 (g1~g6, g5b) 개별 미명시. 계약이 `[enumerated]` 요구였는데 포괄 경로로 처리되어 REJECT. 현재 가이드에서는 계약 작성 시점에 `[enumerated]` / `[collective]` 를 명시하도록 Phase 2 에서 contract-design-guide 에 강제했고, evaluator 는 태그에 따라 검증 방식을 분기한다.

**태그 조합 예시:**

- `[exact, enumerated]` — 이름 목록을 개별 literal 매칭 (가장 엄격)
- `[structural, enumerated]` — 섹션/필드 목록을 개별 구조 검증
- `[structural, collective]` — 포괄 경로 1 건 구조 검증 (기본값)
- `[goal, collective]` — 포괄 패턴 하나가 목표 달성에 기여하는지 의미 검증

---

## 검증 방법론

### 3-Level 검증

| Level | 검증 방법 | 도구 | 목적 |
| ------- | ---------- | ------ | ------ |
| L1: 구조 | 파일/디렉토리 존재 확인 | Glob, ls | 산출물이 있는가? |
| L2: 내용 | 파일 내용에 기대 요소 존재 | Read, Grep | 코드가 작성되었는가? |
| L3: 의미 | 코드 경로 추적, 행동 검증 | Read + 논리 추적 | 코드가 의도대로 동작하는가? |

**모든 조건은 L3까지 도달해야 한다.** L1/L2에서 PASS해도 L3에서 FAIL이면 전체 FAIL.

학술적 근거: 3계층 모델은 industry code review의 lint → semantic → AI 모델과 대응한다.

**L3 검증 심층화 절차:**

단순 Grep 매칭은 L2에서 멈추는 함정이다. L3 도달을 위해 아래 2단계를 반드시 수행한다:

1. **Grep 존재 확인** — 기대 요소가 파일에 있는지 검색 (L2)
2. **Read 전체 내용 확인 → 의미 추적** — 해당 요소가 포함된 파일을 Read로 열어 맥락(호출 흐름, 조건 분기, 반환 경로)을 확인하고 조건의 의도와 실제 구현이 일치하는지 추적 (L3)

```text
# L3 도달 예시
# ❌ L2에서 멈춤: Grep으로 'design-tokens.md' 언급 확인 → PASS
# ✅ L3 도달: Read로 design-tokens.md 전체 내용 확인 → 토큰 구조가
#            조건이 요구하는 카테고리(color/spacing/typography)를 모두 포함하는지 의미 매칭
```

- audit-report.md, design-tokens.md 같은 산출 문서는 Grep으로 존재만 확인하지 말고 **Read로 내용까지 확인**해야 L3 커버리지를 충족한다.
- 파일이 크면 핵심 섹션을 Read(offset/limit)로 부분 읽기하되, 판정에 필요한 구체적 증거(파일:라인)를 확보한다.

**Markdown 전수 검사 조건 (CD-02, DG-02 계열) L3 절차:**

"모든 HTML 파일에 card 섹션이 있다" 나 "모든 SKILL.md 의 fenced code block 에 언어 힌트가 있다" 같은 **전수 검사 조건**은 샘플 1~2 건만 확인하면 L2 에서 멈추는 함정에 빠진다. L3 도달 절차:

1. **Glob 으로 대상 파일 목록 수집** — 예: `**/*.html`, `**/SKILL.md`
2. **각 파일을 Read 또는 Grep** — Grep 으로 위반 패턴 (언어 힌트 없는 ` ``` `) 을 파일별 카운트
3. **FAIL 파일명:라인 나열** — 위반 건이 있으면 파일명과 라인 번호를 모두 피드백에 기재. 샘플만 기재하지 않는다
4. **전체 카운트 보고** — "N 개 파일 중 M 개 위반" 형태로 집계. 집계 없이 "몇 건 발견" 같은 표현 금지

실제 실패 사례: DG-02 REJECT (2026-04-10) — react-run (2 개), react-build (3 개), react-preflight (3 개), react-audit (4 개+), react-reviewer (6 개+) 등 5 개 파일에서 언어 힌트 누락. evaluator 가 1 개 파일만 샘플 확인하고 PASS 처리한 case. 전수 검사로 전환 시 FAIL 로 재판정된 사례다.

### L3 Coverage Honesty — 샘플링 시 미검증 명시 의무

> **배경:** l3_unreached 진단이 13 회 누적. 시간 제약으로 대상이 많을 때 평가자가 샘플링으로 끝내고 전체 PASS 로 뭉뚱그리는 패턴. 부분 검증을 감추면 다음 세션의 평가자가 구멍을 찾지 못한다.

**규칙:**

- L3 전수 검증이 시간 제약으로 불가능하면 **샘플링 대상** 과 **미검증 대상** 을 명시적으로 분리하여 보고한다
- 샘플링으로 검증한 조건은 `[샘플링-N개/전체-M개]` 태그를 증거에 붙인다
- 미검증 대상은 `[미검증]` 마커 집계에 합산된다 (상기 카운팅 로직 적용)
- "20 개 중 2 개만 확인 + 나머지는 비슷하니까 PASS" 는 금지 — 나머지 18 개는 미검증으로 분류

**보고 형식:**

```text
- [x] AR-01: ... — PASS [L3, 샘플링-3/전체-20]
  - 근거: rust-api (파일:라인), rust-service (파일:라인), rust-middleware (파일:라인) — 3 개 L3 확인
  - [미검증-17] rust-init/-feature/-model/-auth 등 17 개 스킬: 시간 제약으로 L3 미도달 → 미검증 카운터 +17
```

> **실제 사례**: infra-kit 2026-04 — 리서치 문서 20 개 중 2 개만 L3 검증, 18 개는 L1/L2 수준. 평가자가 "시간 제약으로 샘플링" 을 Sprint Feedback 에 명시해 다음 iteration 에서 전수 검증을 추적 가능했다. 명시하지 않았다면 잠재 구멍이 영원히 묻혔을 case.

### Rubric 기반 분해 (CheckEval 프로토콜)

각 계약 조건을 boolean 서브체크로 분해한다 ([CheckEval](https://arxiv.org/abs/2403.18771) 패턴).
CheckEval은 Likert 스케일 대신 boolean 분해로 평가자 간 일치도를 0.45 향상시켰다 (EMNLP 2025).

> **Recursive Rubric Decomposition (RRD)**: 고수준 루브릭 항목이 여전히 모호하면 한 번 더 서브포인트로 재귀 분해한다 ([arxiv 2602.05125](https://arxiv.org/html/2602.05125v1/)). 예: "로그인 화면이 정상 동작한다" → ① 필드 존재 ② 유효성 검사 ③ 서버 호출 ④ 에러 표시 로 1 차 분해 후, ②를 다시 ②a 빈 입력, ②b 잘못된 이메일 형식, ②c 비밀번호 최소 길이 로 재귀 분해. RRD 는 계약 조건이 `[goal]` 태그인 경우 특히 유용하며, 한 번 분해했는데도 서브체크 1 개가 10+ 라인을 Read 해야 판정 가능하면 재귀 분해 신호다.
>
> **Chain-of-Thought 효용 한계**: 루브릭이 잘 정의되어 있으면(이 문서의 L3 검증 + 서브체크 분해 적용 시) CoT 가 판정 신뢰도에 주는 이득은 미미하다 ([arxiv 2506.13639](https://arxiv.org/html/2506.13639v1)). 장황한 reasoning 을 작성하지 말고, **증거(파일:라인) + 서브체크 boolean 결과**에 집중한다. CoT 는 계약이 불명확할 때의 임시방편일 뿐, 본 가이드의 우선 전략은 계약을 선명히 쓰고(Phase 2 contract-design-guide) 서브체크로 분해하는 것이다.

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

### 수량/경계값 조건 검증 (Quantitative Verification)

수량이나 경계값이 포함된 조건(">= N줄", "<= M개", "정확히 K건")은 측정 → 비교 → 보고 3단계를 반드시 수행한다. "대략 맞는 것 같다"는 L2에서 멈추는 함정이다.

**검증 절차:**

1. **측정** — 조건의 대상을 실제로 카운트한다. 파일 줄 수는 `wc -l`, 항목 수는 Grep 카운트, 파일 수는 Glob 결과 카운트 등
2. **즉시 출력** — 측정값을 Sprint Feedback 근거에 명시한다. 예: `측정값: 1498줄 (기준: >= 1500)`
3. **비교 판정** — 측정값과 기준값을 비교하여 PASS/FAIL 판정. 경계값 미달은 무조건 FAIL (1498 >= 1500 → FAIL)

**카운팅 시 패턴 주의사항:**

항목을 카운트할 때 Grep 패턴이 대상의 모든 변형을 포함하는지 확인한다:
- Markdown 헤더: `##` 뿐 아니라 `###`, `####` 등 하위 레벨도 고려
- 번호 매기기: `1.` 형식과 `- ` 불릿 형식 모두 고려
- Gotchas 항목 카운트: H2(`## Gotchas`) 하위의 H3(`### 항목`) 또는 불릿(`- **항목**`) 형태 모두 매칭하는 범용 정규식 사용

```text
# 실패 사례: AR-03 REJECT
# 조건: docs/flutter/ >= 1500줄
# 측정값: 1498줄 → 2줄 부족 → FAIL
# 교훈: "거의 1500줄"이라고 PASS 처리하면 안 된다
```

> **실제 사례**: AR-03 REJECT (2026-04-12) — `docs/flutter/` 파일 총 줄 수가 1498줄로 기준 1500줄에 2줄 부족. 경계값 미달을 "거의 충족"으로 PASS 처리하지 않고 FAIL로 정확히 판정한 사례.

### 스킬 트리거 키워드 배타성 검증 (Set Intersection)

스킬 간 트리거 키워드 중복은 Claude가 잘못된 스킬을 실행하는 직접 원인이다. 키워드 배타성 조건이 계약에 포함된 경우 아래 절차를 따른다.

**검증 절차:**

1. **키워드 추출** — 대상 SKILL.md의 `description` frontmatter에서 트리거 키워드 목록을 Grep으로 추출한다
2. **비교 대상 수집** — 같은 플러그인 내 모든 SKILL.md 파일 목록을 Glob으로 수집한다
3. **Set Intersection 비교** — 각 SKILL.md의 description을 Read하여 키워드를 추출하고, 대상 스킬의 키워드와 교차 비교한다
4. **부분 포함 관계 판정** — 완전 일치뿐 아니라 **부분 문자열 포함 관계**도 배타성 위반으로 판정한다

**부분 포함 관계 판정 기준:**

```text
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

각 조건을 최소 2개 관점에서 평가한다. 구현자 시점만으로 평가하면 사용자 가치나 비즈니스 의도가 누락된다 (perspective_gap: 5회 diagnosis).

| 관점 | 초점 | 예시 질문 |
| ------ | ------ | ----------- |
| 기능 | 명시된 행동이 구현되었는가? | "버튼 클릭 시 API 호출되는가?" |
| 엣지 케이스 | 경계 조건에서 올바른가? | "빈 입력, null, 최대 길이에서?" |
| 성능 | 비효율이나 병목이 있는가? | "N+1 쿼리, 불필요한 리렌더링?" |
| 보안 | 취약점이 있는가? | "SQL 인젝션, XSS 가능성?" |
| **User-Value** | 사용자가 이 동작으로 무엇을 얻는가? | "에러 메시지가 사용자에게 실제로 도움이 되는가?", "로딩 상태가 인지 가능한가?" |
| **Business-Intent** | 계약의 상위 의도에 부합하는가? | "규제 준수·데이터 일관성·SLA 달성 측면에서 의도를 실현하는가?" |

**구현자 관점만으로 평가 금지.** "코드가 동작한다" 만 확인하고 끝내지 마라. 조건이 사용자/비즈니스 의도를 어떻게 실현하는지 한 문장으로 서술 가능해야 한다. 서술 불가면 `[goal]` 조건에서 관점 부족 플래그.

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
| -------- | ------ | ------ |
| 높음 | L3 검증 완료 + 명확한 증거(파일:라인) | — |
| 중간 | L2까지 검증 + 정황 증거 | `[medium-confidence]` |
| 낮음 | L1만 검증 또는 정적 분석 한계 | `[low-confidence]` |

### 판정 확신도 규칙

- 낮은 확신도 PASS는 `[미검증]`과 동일 취급한다
- 낮은 확신도 조건이 3개 이상이면 Sprint Feedback에 `⚠️ 낮은 확신도 조건 다수` 경고를 명시한다
- 확신도는 판정을 뒤집지 않는다 — FAIL은 확신도와 무관하게 FAIL이다
- **Swap Test 불안정 강등 규칙**: 동일 조건을 `(A, B)` 와 `(B, A)` 순서로 평가했을 때 PASS/FAIL 이 다르면 자동으로 `[low-confidence]` 로 강등한다. 2 회 재검증해도 일치하지 않으면 `[미검증]` 으로 처리하고 Sprint Feedback 에 position bias 의심 명시

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
| ------ | ----------- |
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

> **Human-in-the-loop rubric refinement 연결**: 계약 조건의 해석 차이가 발견되면 evaluator 는 **계약 수정 권장**을 Sprint Feedback 에 명시한다 — 단, 실제 수정은 사용자 권한이다. 이는 [arxiv 2511.10865](https://arxiv.org/abs/2511.10865) 의 "one-time rubric refinement" 패턴과 동일하다: LLM 이 1 차 평가 → 해석 충돌 발견 시 rubric 개선 제안 → 사용자가 승인·수정 → 이후 평가는 refined rubric 기준. evaluator 가 계약을 무단으로 재해석하거나 "의도를 미루어" PASS 처리하지 않는다.

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

---

## References

LLM-as-a-Judge 2026 최신 연구 (Phase 3 kaizen 인용):

- [Judging the Judges: A Systematic Study of Position Bias in LLM-as-a-Judge — arxiv 2406.07791](https://arxiv.org/abs/2406.07791) (IJCNLP 2025) — Swap Test 표준화
- [Am I More Pointwise or Pairwise? Revealing Position Bias in Rubric-Based LLM-as-a-Judge — arxiv 2602.02219](https://arxiv.org/html/2602.02219) — rubric 기반 판정에서도 position bias 발생
- [Self-Preference Bias in LLM-as-a-Judge — arxiv 2410.21819](https://arxiv.org/abs/2410.21819) — perplexity 기반 familiarity, 컨텍스트 분리 근거
- [Justice or Prejudice? Quantifying Biases in LLM-as-a-Judge — arxiv 2410.02736](https://arxiv.org/html/2410.02736v1) — 12 개 편향 분류
- [Evaluating Scoring Bias in LLM-as-a-Judge — arxiv 2506.22316](https://arxiv.org/html/2506.22316v1) — scoring bias 측정
- [An Empirical Study of LLM-as-a-Judge: How Design Choices Impact Evaluation Reliability — arxiv 2506.13639](https://arxiv.org/html/2506.13639v1) — CoT minimal gain when rubric well-defined
- [Rethinking Rubric Generation for Improving LLM Judge and Reward Modeling — arxiv 2602.05125](https://arxiv.org/html/2602.05125v1/) — Recursive Rubric Decomposition (RRD)
- [A Survey on LLM-as-a-Judge — arxiv 2411.15594](https://arxiv.org/html/2411.15594v6) — 종합 bias 분류
- [Towards a Human-in-the-Loop Framework for Reliable Patch Evaluation — arxiv 2511.10865](https://arxiv.org/abs/2511.10865) — one-time rubric refinement 패턴

기존 참조 (Phase 1 이전):

- [Understanding LLM-Driven Test Oracle Generation — arxiv 2601.05542](https://arxiv.org/abs/2601.05542) — 구현 추종 편향, specification-first
- [A Statistical Approach to Model Evaluations — Anthropic](https://www.anthropic.com/research/statistical-approach-to-model-evals) — 판정 확신도
- [CheckEval — arxiv 2403.18771](https://arxiv.org/abs/2403.18771) — boolean 서브체크 분해
- [CodeBERTScore — arxiv 2302.05527](https://arxiv.org/abs/2302.05527) — 코드 유사도 메트릭 (본 가이드는 계약 기반 검증이 우선이므로 보조 참고용으로만 언급)

관련 스키마:

- `harness/references/contract-schema.md` — Sprint Contract v3 스키마 (specificity tag + aggregation mode + 검증 수단 + `[미검증]` 마커 + sibling enumerated)
- `harness/references/feedback-schema.yaml` — 피드백 YAML 스키마

---

## Cross-Surface Parity Checklist

> **대응:** `skill-design-guide.md §11` · `agent-design-guide.md §12` · `contract-design-guide.md §원칙 전수성`
>
> **배경:** Phase 1/2 에서 Cross-Surface Parity 가 설계 가이드 · 계약 가이드 레이어에 고정되었다. Phase 3 는 동일 parity 를 **평가자 레이어** 에 흡수하고, 향후 본 가이드가 개정될 때 상·하위 surface 로의 전파를 자동 체크한다.

### 원칙

qa-evaluation-guide 가 개정되면 다음 파일에 대응 원칙이 존재하는지 자동 체크한다:

- 상위: `skill-design-guide.md`, `agent-design-guide.md`, `contract-design-guide.md`
- 동급: `harness/references/contract-schema.md`
- 하위: `harness/agents/qa-evaluator.md`, `*-kit/agents/*-reviewer.md`

### Parity Table (4 개 parity item)

| # | Parity Item | skill-design-guide | agent-design-guide | contract-design-guide | **qa-evaluation-guide (이 가이드)** |
|---|-------------|-------------------|-------------------|----------------------|-------------------------------------|
| 1 | Binary Decidability | §3.5 (계약 모호성 방지) | §3.5 (Pre-Check) | §Binary Decidability | **§Binary Decidability Pre-Check** |
| 2 | Rule-by-Rule Audit | §3.6 | §10 (reviewer audit) | — (평가 위임) | **§Rule-by-Rule Audit Before Completion** |
| 3 | Unverifiable / `[미검증]` 정책 | — (스킬 전용 아님) | §10 Unverifiable | §미검증 마커 | **§`[미검증]` 마커 평가 프로토콜** |
| 4 | Sibling Consistency | §8.8 | §3 (sibling agent) | §Sibling Consistency | **§Sibling Enumerated Verification** |

### 개정 시 체크리스트

qa-evaluation-guide.md 편집 시:

- [ ] 새 평가 원칙을 추가했는가? → 상위 skill/agent/contract 가이드에 원천 원칙이 있는지 Grep 확인
- [ ] 원칙 네이밍 (섹션명, 용어) 을 변경했는가? → qa-evaluator.md · contract-schema.md 에서 동일 네이밍 사용 중인지 Grep 하여 동기화
- [ ] 실패 사례를 추가했는가? → 해당 REJECT 가 발생한 프로젝트의 feedback YAML 에 연결 링크 포함
- [ ] parity table 의 컬럼을 추가/삭제했는가? → 상위 3 개 가이드의 parity table 도 동일하게 갱신

### 실패 사례 (이 원칙 없이 발생)

- **PH-01 (design-kit, 2026-04)**: skill-design-guide §3.5 가 agent-design-guide 와 qa-evaluation-guide 에 전수되지 않아 평가자가 모호 조건을 그대로 평가 → REJECT
- **SK-13 (backend-kit/infra-kit)**: 상위 가이드 원칙이 하위 스킬 SKILL.md 로 전수되지 않은 meta-gap

### 버전 정보

- **Guide version**: 2026-04-24 (Phase 3 kaizen · v3 흡수)
- **Parity with**: skill-design-guide v1.2.0, agent-design-guide v1.2.0, contract-design-guide v3 (2026-04-24)
- **Schema link**: contract-schema.md v3
