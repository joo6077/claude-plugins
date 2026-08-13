# QA Evaluation Guide

> qa-evaluator 에이전트가 참조하는 평가 방법론.
> evaluator-kaizen이 리서치 기반으로 이 문서를 갱신한다.
>
> **참조 스키마**: `harness/references/contract-schema.md` (v5.3)
>
> **최근 갱신: 2026-08-13 (Phase 3 kaizen · v5.0)** — 2026-08-11~12 글로벌 REJECT 를 근거로
> **미검증 임계의 오처벌을 정밀화**하고, Phase 2 가 만든 계약 봉인·amendment 2 축의 **소비면**을
> 착지시켰다. 이번 사이클의 전략도 새 문장 추가가 아니라 **분류·카운터의 정밀화**다.
>
> - 개정 **§증거 분류 triage** — 3 분기 → **4 분기**. `UNVERIFIED_ENV`(구현자 통제 밖) 를
>   `UNVERIFIED_INVALID_EVIDENCE`(4 요건 미충족 주장 + 공허한 증거) 와 **다른 장부에 적는다.**
>   자동 REJECT 임계 2 는 후자에만 적용되고, 전자는 `env_gaps` 로 세어 **검증 커버리지 게이트**
>   (`(총수 − env_gaps)/총수 < 0.60` → BLOCKED)에만 쓴다. 회피 경로는 **남용 방지 4 요건** +
>   **2 iteration 연속 ENV 승급**으로 닫는다. 실측 4 건 연속 오처벌이 직접 원인이다
> - 신규 **§Discriminating Evidence Gate** — Evidence Validity Gate 검사 3(반증 가능성)의 집행
>   절차. 적용 범위 9 항으로 **한정**하고 전체 repo mutation score 임계값을 금지한다.
>   실측 `ER-02` (동시성 가드를 삭제해도 테스트 통과) 가 직접 원인
> - 신규 **§Canonical User-Reported Failure Protocol** — 사용자 관측과 자기 증거가 충돌할 때의
>   **우선순위**. 상태어 `REOPENED` · 6 축 대조 · 반박 금지 · 완료 해제 3 택. 기존
>   §Evidence Validity Gate 는 *자기* 증거의 유효성이라 **다른 검사**다
> - 신규 **§계약 봉인 검증** — `verify_seal` 소비면. `SEAL_ABSENT` 는 경고이지 실패가 아니고,
>   미해소 `SEAL_BROKEN` 은 REJECT 다
> - 개정 **§Amendment 소비 규칙** — 1 축 3 값 → **`direction` × `consent` 2 축**.
>   앵커 부재가 방향 판정을 붕괴시키지 않으며 `narrowing · unanchored` 는 PASS 근거가 된다
> - 정정 **scoring bias 출처** — [arxiv 2506.22316] 은 binary PASS/FAIL 을 주장하지 않는다.
>   이진 채점의 직접 근거는 CheckEval 이다
>
> 이전 (2026-07-28, v4.1): 같은 프로젝트에서 세션을 병렬로
> 돌릴 때 A 의 평가자가 B 의 계약을 채점하던 경로를 차단한다 (2026-07-27 카이젠 실측).
>
> - 신규 **§계약 선택 ladder** — 평가 대상 계약을 5 단계 순서로 결정론적으로 특정한다
>   (3.5 레거시 브릿지 포함 — 레거시 전용 프로젝트를 BLOCKED 로 회귀시키지 않는다).
>   판정 근거는 파일 개수가 아니라 frontmatter `status` 이며, `status` 없는 레거시 계약은
>   active 후보에서 제외한다. 모호하면 후보를 나열하고 BLOCKED — 조용한 선택 fallback 없음
> - 신규 **§계약 지문과 TOCTOU** — 선택 시점의 `경로 + sha256 + status` 를 고정하고 verdict
>   저장 직전 재확인. 달라졌으면 verdict 폐기
> - 신규 **§Amendment 소비 규칙** — 스프린트 도중 조건 변경은 계약 본문이 아니라 사이드카에
>   쌓인다 (당시 1 축 3 값 규칙은 **위 v5.0 의 2 축 규칙으로 대체됨**)
> - 신규 **§User Correction Audit** — 반영되지 않은 사용자 교정을 읽기 전용으로 대조해
>   `unreflected_corrections` 로 표면화만 한다 (자동 REJECT 없음)
> - 개정 **§CONTRACT_ROOT** — 조상 체인에서 **먼저 만나는 `.harness` 에서 멈춘다.**
>   `project.yaml` 만 찾으며 올라가면 계약을 실제로 가진 디렉토리를 지나쳐 **조상의 다른 계약을
>   경고 없이 채점**한다 (실측: `apps/apps/app_kiosk`). `project.yaml` 이 없으면
>   `contract_root_unconfigured: true` 경고 + `/harness init` 안내로 처리하고 평가는 계속한다.
>   `CONTRACT_ROOT` 가 끝내 비면 `/.harness` 를 뒤지지 말고 전용 BLOCKED
> - 개정 **§ladder 1** — `HARNESS_CONTRACT` 는 `test -f` 로 존재까지 확인한다. 없는 경로는
>   아래 단계로 흘려보내지 말고 전용 BLOCKED (TOCTOU 오진 차단). 후보 0 건도 `4 BLOCKED` 가
>   아니라 별도 "부재" 사유다
> - 경로·슬러그 규약은 `harness/references/contract-schema.md` §산출물 경로가 SSOT 이며
>   본 가이드는 인용만 한다
>
> 이전 (2026-07-27, v4.0): `/insights` Friction #2 (시각·런타임
> 검증 신뢰 불가) 흡수 + Phase 1·2 정합화. 이번 사이클의 전략은 새 문장 추가가 아니라
> **enforcement 등급 상향**이다 (등급 SSOT: `skill-design-guide.md §3.7`).
>
> - 신규 **§Evidence Validity Gate** — 기존 §Execution-Grounded Evidence 가 증거의 *존재*를
>   요구했다면, 본 절은 증거의 *유효성*을 요구한다. 빈 스냅샷·0 매치 grep·0 개 테스트 실행처럼
>   **아무것도 검사하지 않고 통과한 증거(vacuous pass)** 를 PASS 로 인정하지 않는다
> - 신규 **§증거 분류 triage** — `[미검증]` 은 **검증 도구·환경 부재 전용**으로 축소
>   (contract-schema v4 정합). 미구현·부재를 미검증으로 적어 FAIL 을 1 건 허용 구간으로
>   세탁하는 경로를 차단
> - 신규 **§계약 파싱 범위** — contract-schema v4 의 허용 섹션 헤더 2 계층을 평가자 측에서 소비
> - 신규 **§Canonical Unverified-Evidence Protocol** — 각 kit reviewer 6 종이 그대로 복제할
>   정본 블록. 현재 임계값이 킷마다 2/3/0 으로 갈라져 있어 원본을 한 곳에 고정
> - 신규 **§Recurring Improvement Escalation** — 같은 개선 제안이 반복되면 산문 권고가 아니라
>   계약 결함으로 승급
> - 신규 **§원칙별 Enforcement 등급** 표 · **§안티패턴 스택 정합성** 규칙
>
> 이전 (2026-06-05, v3.2): `/insights` Friction #5 (스킬/도구
> 가짜 호출) 흡수. 신규 **§Execution-Grounded Evidence**: 계약 조건이 동적 실행("실행/호출/
> 생성")을 요구할 때 evaluator 가 narrated 주장이 아닌 실행 산출물(명령 출력·아티팩트·로그)을
> 능동적으로 요구하고, 부재 시 `[미검증]` 처리. 기존 "주석은 증거가 아니다"(generator 주장
> 배제)와 다른 축 — observable artifact 능동 수집. parity item #5 등록 (상위 surface 는
> Phase 1/2 DEFERRED).
>
> 이전 (2026-05-07, v3.1): `/insights` 30 일 분석 흡수.
> Friction #1 (proactive quality gap) 은 본 가이드의 Rule-by-Rule Audit 프로토콜로
> 이미 강제 (skill-design-guide v1.3.0 §3.6 의 평가자 측 짝). Phase 1 신규 원칙
> "Pre-Edit Batch Audit" 의 평가자 측 대응은 본 가이드 "조건 평가 시작 전 전수
> enumerate" 절차에 cross-reference. agent-design-guide v1.3.0 §10 신규
> "Self-Evaluator Rule-by-Rule Audit" gotcha 는 평가자 자기 산출물 self-check 패스의
> 연구적 근거이며, verdict 직전 의무 절차이다.
>
> 이전 (2026-04-24, v3 흡수): Phase 1/2 Cross-Surface Parity 흡수. Binary
> Decidability Pre-Check, Rule-by-Rule Audit, `[미검증]` 마커 평가 프로토콜 (1/2건
> 임계), Sibling Enumerated 전수 Grep 절차, L3 Coverage Honesty 규칙, User-Value/
> Business-Intent 관점을 평가자 프로토콜로 흡수. 이전: 2026-04-12 수량/경계값
> 조건 검증 프로토콜 추가 · LLM-as-judge 2026 최신 연구 반영 + contract-schema
> v2 소비 규칙.

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
| 점수 분포 편향 (Scoring bias) | 채점 rubric 의 순서 · score ID · reference answer 점수 같은 **채점 프롬프트 섭동**에 판정이 흔들리는 경향 | 이진 PASS/FAIL 만 사용 — Likert 스케일 금지. 서브체크 단위로 분해하여 모호 영역 제거 ([arxiv 2403.18771](https://arxiv.org/abs/2403.18771) — decomposed binary questions 로 평가자 일치도 평균 **0.45** 개선) |
| 구체성 편향 (Concreteness bias) | 구체적 코드에 추상적 코드보다 호의적 | 계약 조건 충족만 판단, 구현 스타일 무시 |
| 구현 추종 편향 (Implementation-following bias) | 실제 구현을 "정답"으로 간주하는 경향 | 계약 조건(specification)을 먼저 읽고, 코드는 증거 수집용으로만 사용 |
| 지시 해석 불일치 (Instruction-following misalignment) | 평가 기준을 일관되지 않게 해석 | 조건별 boolean 체크리스트 분해로 해석 여지 최소화 |

> **출처 정정 (2026-08-13)**: 이전 판은 위 scoring bias 행의 완화 전략에
> [arxiv 2506.22316](https://arxiv.org/html/2506.22316v1) 을 달았다. 그 논문은 score rubric order ·
> score IDs · reference answer score 3 종을 정의하고 채점 프롬프트 섭동이 judge robustness 를
> 흔든다는 것을 보일 뿐이며, **binary PASS/FAIL 채점을 주장하지 않는다.** 완화 전략의 직접 근거는
> CheckEval 이므로 인용을 교체했다. 이 논문은 "편향이 무엇인가" 의 출처이지 "그래서 이진으로
> 채점하라" 의 출처가 아니다.
>
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

## 원칙별 Enforcement 등급 (E1 / E2 / E3)

> **등급 정의 SSOT:** [`skill-design-guide.md §3.7`](skill-design-guide.md). 등급 어휘를 여기서
> 재정의하거나 동의어(예: "약한 규칙 / 강한 규칙")를 만들지 마라. 본 절은 **평가자 원칙의 현재
> 등급 목록**만 유지한다 (contract-design-guide §원칙별 Enforcement 등급 과 같은 착지 구조).
>
> **§3.7 등급 원장을 이 표에 복제하지 마라 (2026-08-13).** 같은 원칙이 두 곳에서 서로 다른 등급을
> 갖는 순간 승급 판정이 불가능해진다. 아래 표는 **평가자 레이어 고유 원칙만** 담고, §3.7 원장에
> 이미 있는 원칙의 등급값을 행으로 다시 적지 않는다. 원장 원칙의 평가자 측 착지점은 아래 대응만
> 알면 된다 — Rule-by-Rule Audit → §Rule-by-Rule Audit Before Completion,
> Completion Evidence Gate → §Execution-Grounded Evidence · §Evidence Validity Gate,
> Counterpart Enumeration → 계약 조건으로 흡수(parity item 12 · 평가자 전용 절 없음),
> User-Reported Failure Gate → §Canonical User-Reported Failure Protocol.
> **이 대응 관계에서 등급을 정하는 쪽은 언제나 §3.7 원장이다.**

같은 결함이 다시 관측되면 이 표의 문구를 다듬지 말고 **등급을 한 칸 올려라.** 이미 E3 인데도
재발하면 원칙 자체가 잘못 설계된 것이므로 재작성한다.

| 평가자 원칙 | 등급 | 근거 |
| ---- | ---- | ---- |
| `UNVERIFIED_INVALID_EVIDENCE` 2 건 자동 REJECT | E3 (기존 · 2026-08 대상 축소) | 임계 비교는 LLM 판단이 개입하지 않는 산술 판정 |
| **`UNVERIFIED_ENV` 분리 + 남용 방지 4 요건** | **E2 (신규)** | 4 요건은 근거란에 남는 아티팩트다. 요건 미충족 시 강등 판정 자체는 고정 규칙 |
| **검증 커버리지 게이트** | **E3 (신규)** | `(조건 총수 − env_gaps) / 조건 총수` 를 임계와 비교하는 산술 판정 |
| **Discriminating Evidence Gate** | **E2 (신규)** | 결합 확인 결과와 음성 대조 근거를 근거란에 남긴다. 실행 변형은 안전 조건부라 E3 로 못 올린다 |
| **계약 봉인 검증 (`verify_seal`)** | **E3 (신규)** | sha256 문자열 동일성 비교. 등급 SSOT 는 contract-schema §계약 봉인 이며 본 행은 소비면 기록이다 |
| Execution-Grounded Evidence | E2 (기존) | 실행 산출물 수집 후 근거란에 기록 |
| **Evidence Validity Gate** | **E2 (신규)** | Friction #2 — 증거 존재만 확인하던 축에 유효성 축 추가. 무효 증거는 산술적으로 미검증 카운터에 합산되므로 임계 판정(E3)에 연결됨 |
| **증거 분류 triage (FAIL / 미검증 / 무효)** | **E2 (신규)** | contract-schema v4 마커 의미 축소 정합 |
| **계약 파싱 범위 2 계층** | **E3 (신규)** | 저장된 계약 파일에 대해 `awk` 로 결정론적 판정 가능 |
| **피드백 저장 경로 해석 ladder** | **E3 (신규)** | digest `feedback-script-location-mismatch` — 경로 존재 여부는 `test -f` 로 결정론적 |
| Recurring Improvement Escalation | E1 (2026-07-27) | 최초 도입 — 반복 관측되면 E2 로 올린다 |
| **계약 선택 ladder 5 단계** | **E3 (신규)** | 후보 열거(`find`)와 `status` 판독(`awk`+따옴표 제거)이 결정론적. 유일성 판정은 산술 비교 |
| **계약 `status` → `done` 전환 (APPROVE 시)** | **E2 (신규)** | 전환 자체는 결정론적이나, 실패해도 verdict 를 무효화하지 않으므로 E3 가 아니다 |
| **계약 지문 재확인 (TOCTOU)** | **E3 (신규)** | `sha256` 문자열 동일성 비교 — LLM 판단이 개입하지 않는다 |
| **Amendment 취급 (direction × consent 2 축)** | **E2 (2026-08 개정)** | 사이드카 파싱 후 2 축 분류가 필요하나 취급 규칙 자체는 고정. 집합형 조건의 `direction` 은 `comm` 집합 비교로 **계산**하므로 그 부분만 결정론적 |
| **User Correction Audit** | **E1 (신규)** | 최초 도입 · 표면화 전용(자동 REJECT 없음). 재발 관측 시 E2 로 올린다 |

---

## 계약 선택 ladder — 병렬 세션에서 "어떤 계약을 평가하는가"

> **대응:** `harness/references/contract-schema.md` §산출물 경로 · `harness/agents/qa-evaluator.md`
> Step 1 · 2026-07-28 병렬 스프린트 안전성 스프린트
>
> **배경:** 계약이 단일 고정 경로 하나였을 때는 "평가 대상 선택" 이라는 문제가 없었다. 같은
> 프로젝트에서 세션을 병렬로 돌리면 세션 A 의 계약을 세션 B 가 덮어쓰고, A 의 평가자가 B 의 계약을
> 채점한다. 2026-07-27 카이젠에서 실제로 발생했고, 그때는 각 서브에이전트 프롬프트에 경로를
> 손으로 박아 우회했다.
>
> **경로·슬러그·frontmatter 필드 규약은 contract-schema §산출물 경로가 SSOT 다.** 본 절은 그
> 규약 위에서 **평가자가 대상을 고르는 절차**만 정의한다.

### 판정 근거는 파일 개수가 아니라 `status` 다

후보는 `{CONTRACT_ROOT}/.harness/` 의 plain `sprint-contract.md` + 접미형
`sprint-contract-<slug>.md` 전부다. 여기서 **active 후보**를 가르는 기준:

| frontmatter 상태 | 해석 | active 후보 |
| ------ | ------ | ------ |
| `status: active` 명시 | 진행 중 | **포함** |
| `status: done` | 종료 | 제외 |
| `status:` 필드 없음 | 레거시 | **제외** |
| frontmatter 자체가 없음 | 레거시 | **제외** (파싱 실패로 중단하지 않는다) |

> **레거시 제외는 선택이 아니라 필수다.** 실측 배포본(fit-pal 3 개 `.harness`)의 접미형 계약
> **40 개는 전부 `status` 가 없다.** 이들을 active 로 세면 후보가 27 개가 되어 정상 프로젝트의
> QA 가 영구 BLOCKED 된다. 디렉토리의 파일 수를 세는 구현은 이 지점에서 반드시 깨진다.

### ladder 5 단계 (순서 고정)

성립하는 첫 단계에서 확정하고 아래를 보지 않는다.

| 단계 | 조건 | 결과 |
| ------ | ------ | ------ |
| 1 | 호출 인자 또는 `HARNESS_CONTRACT` 로 경로를 받았고 **`test -f` 통과** | 그 경로를 쓴다 |
| 1x | 경로를 받았는데 **파일이 없다** | **BLOCKED** — 아래 단계로 흘려보내지 않는다 |
| 0 | 후보가 **0 건** | **BLOCKED (부재)** — 모호와 사유가 다르다 |
| 2 | `status: active` + `owner_session == $CLAUDE_CODE_SESSION_ID` 인 계약이 **정확히 1 개** | 그것을 쓴다 |
| 3 | `status: active` 인 계약이 전체에서 **정확히 1 개** | 그것을 쓴다 |
| 3.5-a | active **0 개** + 레거시 중 plain `sprint-contract.md` 가 있다 | 그것을 쓴다 + `legacy_contract_used: true` |
| 3.5-b | active **0 개** + plain 없음 + 레거시가 **정확히 1 개** | 그것을 쓴다 + `legacy_contract_used: true` |
| 4 | 그 외 (active 2 개 이상 · 브릿지 불성립) | **BLOCKED** — 후보 나열 + 복구 방법 |

- **1 단계는 `[ -n "$HARNESS_CONTRACT" ] && [ -f "$HARNESS_CONTRACT" ]` 로 존재까지 본다.**
  `-n` 만 보면 오타·stale 경로가 빈 해시로 굴러가다 저장 직전 지문 재확인에서 "평가 도중 계약이
  변경되었습니다 (TOCTOU)" 로 **오진**한다 — 애초에 없던 파일이지 바뀐 파일이 아니다. 그리고
  없는 경로를 아래 단계로 흘려보내면 "명시했는데 다른 계약이 채점되는" 오귀속이 된다. 없으면
  **전용 BLOCKED**("지정한 계약 경로가 존재하지 않습니다: `<경로>`")다. Step 8 의 경로 해석
  ladder 가 이미 `test -f` 를 결정론적 관용구로 쓰고 있다
- **`CLAUDE_CODE_SESSION_ID` 가 없으면 2 단계를 건너뛰고 3 으로 내려간다.** 식별자 부재는 그
  자체로 중단 사유가 아니다. 3 단계에서 유일 active 로 결정되면 정상 평가다
- **후보 0 건은 `4 BLOCKED` 가 아니다.** 4 단계 문구는 "결정론적으로 특정할 수 없습니다" 이며
  후보 목록을 나열하는데, 0 건이면 빈 목록을 출력하고 사용자는 있지도 않은 계약의 `status` 를
  정리하려 든다. 부재(`/sprint-contract`)와 모호(`status` 정리)는 복구책이 다르므로 분기한다
- **모호할 때 조용히 하나를 고르는 fallback 을 두지 않는다.** mtime 최신순 정렬로 고르거나
  후보 중 그럴듯한 것을 골라 진행하면, 잘못 고른 계약의 verdict 가 다른 세션의 작업을 오판하고
  글로벌 피드백 저장소(`~/.harness/feedback/`)까지 오염시킨다. 오염된 피드백은 이후 카이젠
  사이클의 입력이 되므로 손실이 누적된다
- BLOCKED 보고에는 **후보 목록(경로 · status · owner)** 과 레거시 제외 건수, 그리고 복구 방법
  2 가지(`HARNESS_CONTRACT=<절대경로>` 명시 / 평가 대상에 `status: active` 추가 + 종료 계약을
  `status: done` 으로 전환)를 함께 적는다. **사유만 적은 BLOCKED 는 사용자를 막다른 길에
  세우는 것이다**

### 3.5 레거시 브릿지 — active 0 개를 BLOCKED 로 만들면 회귀다

`status` 필드는 이 스프린트에서 도입됐다. 그 이전 계약은 전부 레거시(= `status` 없음)이며 active
후보에서 빠지므로, 규칙을 그대로 적용하면 **기존 프로젝트 전부가 active 0 개 → BLOCKED** 가 된다.
변경 전 평가자는 plain `sprint-contract.md` 를 조건 없이 읽었으므로 이것은 명백한 회귀다.

**실측 (2026-07-28, `~/Hub/10_Dev` 하위 `CONTRACT_ROOT` 13 개 — 1-a 규칙 개정으로
`project.yaml` 없는 4 개가 후보에 합류했다):**

| CONTRACT_ROOT | `project.yaml` | plain | 접미형 레거시 | active | ladder 결과 |
| ------ | ------ | ------ | ------ | ------ | ------ |
| `claude-plugins` | 있음 | 없음 | 1 | 1 | 2 세션소유 (세션 ID 없으면 3) |
| `fit-pal/app` | 있음 | 있음 | 27 | 0 | 3.5-a |
| `fit-pal/server` | 있음 | 있음 | 12 | 0 | 3.5-a |
| `fit-pal` | 있음 | 있음 | 1 | 0 | 3.5-a |
| `apps` · `iyaki-zip-dev` · `fit-pal-wt` · `fit-pal-wt/app` · `fit-pal-wt/server` | 있음 | 있음 | 0 | 0 | 3.5-a |
| `apps/apps/app_kiosk` · `flutter_playwright` · `purchase-bot` · `_sandbox/flutter_colorpicker` | **없음** | 있음 | 0 | 0 | 3.5-a + `contract_root_unconfigured` |

**레거시 전용 12 개가 전부 plain 을 갖고 있다.** 그래서 브릿지 조건을 "레거시가 정확히 1 개일
때만" 으로 두면 `fit-pal/app`(28) · `fit-pal/server`(13) · `fit-pal`(2) 3 개가 여전히 BLOCKED 로
남아 회귀가 해소되지 않는다. **plain 우선(3.5-a)이 곧 변경 전 동작이므로 회귀가 0 이다.**

**실행 검증 결과 (zsh · bash 각 13 개): OK 13 / BLOCKED 0.** 두 셸의 선택 결과가 경로·sha256
까지 동일했다. `apps/apps/app_kiosk` 는 자기 계약(`e1a45c8b…`)을 고르며, 조상 `apps/` 의
계약(`ac9cd299…`)을 채점하지 않는다.

브릿지로 선택했으면 verdict 에 경고를 노출한다 — 조용히 레거시를 집으면 병렬 세션에서 대상이
어긋나도 사용자가 알 수 없다:

```text
⚠️ legacy_contract_used: true — `status` 필드가 없어 레거시 브릿지(ladder 3.5)로 선택했습니다.
   권장: 계약 frontmatter 에 `status: active` 추가 또는 HARNESS_CONTRACT 로 고정.
```

### 계약 `status` 수명주기 — `done` 전환 주체는 평가자다

`active` 를 `done` 으로 되돌리는 주체가 없으면 스프린트마다 active 가 **단조 증가**한다. 두 번째
스프린트부터 active 2 개가 되어 ladder 3 이 무너지고, 세션 ID 없는 호출은 곧장 4 단계 BLOCKED 다.
계약이 종료되는 시점은 **APPROVE 가 나온 순간**이므로 그 판정을 낸 평가자가 전환한다.

- **APPROVE 일 때만 전환한다.** REJECT 는 수정 후 재평가해야 하므로 `active` 유지
- **`status: active` 가 명시된 계약만 전환한다.** 레거시는 이미 active 후보가 아니고, 레거시에
  `status: done` 을 박으면 다음 호출에서 후보가 0 개가 되어 새 BLOCKED 를 만든다
- **Step 5 지문 재확인이 OK 인 뒤에** 전환한다. 재확인 전에 파일을 바꾸면 평가자가 스스로
  TOCTOU 를 유발한다
- **전환 실패는 verdict 를 무효화하지 않는다** — 경고만 남기고 완료한다. 이 단계는 E2 다

### 계약 지문과 TOCTOU

선택 시점과 verdict 저장 시점 사이에 다른 세션이 같은 파일을 쓸 수 있다. 선택 시점에
**경로 + 내용 sha256 + status** 3 요소를 고정하고, **저장 직전 다시 계산해 대조**한다.

- 3 요소 중 하나라도 다르거나 파일이 사라졌으면 **verdict 를 저장하지 않고 BLOCKED** 다.
  이미 산출한 판정은 다른 계약에 대한 것이므로 무효다
- 지문은 Sprint Feedback 의 `Contract Fingerprint` 블록에 그대로 남긴다. 지문이 없는 피드백은
  "어떤 계약을 채점했는지" 를 사후에 증명할 수 없다
- 이 검사는 E3 다 — 해시 문자열 동일성 비교라 LLM 판단이 개입하지 않는다

### CONTRACT_ROOT — 먼저 만나는 `.harness` 에서 멈춘다

조상 체인을 올라가며 **처음 만나는 `.harness/` 디렉토리에서 멈춘다.** 규칙은 이것 하나뿐이다.
그 디렉토리가 `project.yaml` 을 가지면 정상 `CONTRACT_ROOT` 이고, 조상 체인에 `project.yaml` 이
여러 개 있어도 가장 깊은 것을 골라 그대로 진행한다.

실측상 정상 중첩 배포본이 4 개(`fit-pal/app`, `fit-pal/server`, `fit-pal-wt/app`,
`fit-pal-wt/server` — 각자 `project.yaml` 을 가지면서 조상에도 있음) 존재한다. 중첩 자체를
검출해 평가를 막는 규칙을 넣으면 이 배포본들이 전부 깨진다.

#### `.harness` 는 있고 `project.yaml` 은 없을 때 — 건너뛰면 조용한 오귀속이다

**`project.yaml` 만 찾으며 올라가는 구현은 `.harness/sprint-contract.md` 를 실제로 가진
디렉토리를 지나쳐 조상의 다른 계약을 경고 없이 채점한다.** BLOCKED 는 사용자가 알아채고 고칠 수
있지만, 이 오귀속은 아무 신호도 남기지 않고 **틀린 계약에 대한 verdict 를 글로벌 피드백
저장소에 적재**한다. BLOCKED 보다 나쁘다.

**실측 (2026-07-28, `~/Hub/10_Dev` 하위 `.harness` 13 개):**

| `.harness` 경로 | `project.yaml` | 계약 | 옛 규칙 결과 | 새 규칙 결과 |
| ------ | ------ | ------ | ------ | ------ |
| `apps/apps/app_kiosk` | 없음 | 있음 (`e1a45c8b…`) | 조상 `apps/` 계약(`ac9cd299…`) 채점 — **오귀속** | 자기 계약 (`unconfigured`) |
| `flutter_playwright` | 없음 | 있음 | BLOCKED — **회귀** | 자기 계약 (`unconfigured`) |
| `purchase-bot` | 없음 | 있음 | BLOCKED — **회귀** | 자기 계약 (`unconfigured`) |
| `_sandbox/flutter_colorpicker` | 없음 | 있음 | BLOCKED — **회귀** | 자기 계약 (`unconfigured`) |
| 나머지 9 개 | 있음 | 있음 | 정상 | 정상 (동일) |

`flutter_playwright` 와 `purchase-bot` 은 `sprint-feedback.md` 와 `history/` 를 갖고 있다 —
**실제로 QA 가 돌던 배포본**이다. 이들을 BLOCKED 로 떨어뜨리는 것은 회귀이며, 그 BLOCKED 사유가
"Sprint Contract 가 존재하지 않습니다" 인 것은 **오진**이다. 계약은 존재하고, 실제 원인은
`/harness init` 미실행(= `project.yaml` 부재)이다.

규칙:

- `.harness/` 는 있는데 `project.yaml` 이 없으면 **그 디렉토리를 `CONTRACT_ROOT` 로 채택**하고
  `contract_root_unconfigured: true` 를 `Contract Fingerprint` 블록과 verdict 본문에 노출한다.
  복구책은 `/harness init`. **경고이지 실패가 아니다** — 평가는 정상 진행하고, `commands` /
  `anti_patterns` / `contract_categories` 는 범용 기본값을 쓴다
- **조상의 `project.yaml` 을 대신 읽지 마라.** 그 프로젝트의 설정이 아니다
- `CONTRACT_ROOT` 가 **끝내 비면** `HDIR="$CONTRACT_ROOT/.harness"` 가 `/.harness` 로 접혀
  루트를 뒤진다. 그 상태로 1-b 에 진입하지 말고 즉시 전용 BLOCKED("CONTRACT_ROOT 미확정 —
  `.harness` 를 찾지 못함", 복구책 `/harness init`)를 낸다

```bash
# cwd 가 ~/Hub/10_Dev/fit-pal/app          → ~/Hub/10_Dev/fit-pal/app        (unconfigured=false)
# cwd 가 ~/Hub/10_Dev/apps/apps/app_kiosk  → ~/Hub/10_Dev/apps/apps/app_kiosk (unconfigured=true)
CONTRACT_ROOT=""; CONTRACT_ROOT_UNCONFIGURED=false
d=$PWD
while : ; do
  if [ -d "$d/.harness" ]; then
    CONTRACT_ROOT="$d"
    [ -f "$d/.harness/project.yaml" ] || CONTRACT_ROOT_UNCONFIGURED=true
    break
  fi
  [ "$d" = "/" ] && break
  d=$(dirname "$d")
done
printf 'CONTRACT_ROOT=%s contract_root_unconfigured=%s\n' \
  "${CONTRACT_ROOT:-<none>}" "$CONTRACT_ROOT_UNCONFIGURED"
```

#### BLOCKED 사유를 혼동하지 마라

사유가 3 가지이고 복구책이 서로 다르다. **틀린 사유를 적으면 사용자는 있지도 않은 문제를
고치려 든다.**

| 상태 | 사유 | 복구책 |
| ------ | ------ | ------ |
| `CONTRACT_ROOT` 가 빔 | `.harness` 를 찾지 못함 | `/harness init` |
| `CONTRACT_ROOT` 확정 · 후보 0 건 | 계약 파일이 없음 | `/sprint-contract` |
| `HARNESS_CONTRACT` 지정 경로 부재 | 명시 경로가 없음 | 경로 수정 또는 변수 해제 |

### 산출물도 같은 슬러그를 따른다

접미형 계약을 평가했으면 QA 산출물도 `sprint-feedback-<slug>.md` 에 쓴다. plain 계약을 평가했으면
plain 이 정상 경로이며 슬러그를 지어내지 않는다. **접미형 계약을 평가하고 피드백만 plain 경로에
쓰면 병렬 세션이 서로의 피드백을 덮어쓴다** — 계약 충돌을 고치고 피드백 충돌을 남기는 셈이다.
`Iteration` 카운터도 같은 슬러그의 피드백만 센다.

---

## Amendment 소비 규칙 — 스프린트 도중 조건이 바뀌면

> **대응:** `harness/references/contract-schema.md` §산출물 3 종 (사이드카 경로) ·
> digest `contract-scope-expanded-after-edit` · usc=true 재위반 12 건
>
> **배경:** 계약은 write-once 라 실행 중 사용자 교정을 담을 자리가 없었다. 그 결과 실측에서
> **계약 본문을 구현에 맞춰 넓혀 위반을 소거한 사례**가 나왔다. 계약이 코드를 따라가면 계약은
> oracle 이기를 그만둔다.

### 사이드카에만 기록된다

amendment 는 `{CONTRACT_ROOT}/.harness/sprint-amendments-<slug>.md` (plain 모드면
`sprint-amendments.md`) 에 쌓인다. **계약 본문에 새 `##` 섹션을 만들지 않는다** — contract-schema
의 허용 섹션 헤더 위반이며, digest `parser-incompatible-contract-section` 결함이 재발한다.
계약 본문에 그런 섹션이 있으면 그것은 amendment 가 아니라 **계약 결함**으로 기록한다.

### 두 축으로 읽는다 — `direction` × `consent` (2026-08-13 개정)

**규약 SSOT 는 `harness/references/contract-schema.md` §Amendment 사이드카 다.** 본 절은 그
2 축을 평가에서 어떻게 소비하는지만 정한다. 축 이름과 값 어휘를 바꾸지 마라.

축 1 · **`direction`** — 이 amendment 를 적용하면 **PASS 하는 구현의 집합이 줄어드는가,
늘어나는가.** "범위 축소" 라는 말로 판정하지 마라 — 무엇의 범위인지에 따라 정반대가 된다.

| `direction` | 의미 |
| ------ | ------ |
| `narrowing` | PASS 집합이 **줄어든다** (제약 강화 · 기준 상향 · 허용 범위 축소) |
| `relaxing` | PASS 집합이 **늘어난다** (기준 하향 · 조건 면제 · 허용 범위 확대) |
| `unknown` | PASS 집합의 증감을 판정할 수 없다 |

축 2 · **`consent`** — 사용자 동의 근거가 있는지.

| `consent` | 조건 |
| ------ | ------ |
| `anchored` | 사용자 발언 인용 + **reflect-kit prompt 로그 앵커**(timestamp · session · cwd) |
| `unanchored` | 앵커를 붙일 수 없다 (로그 미설치 · 구두 합의 · 에이전트 자체 판단) |

**2 축 조합표 — 이것이 판정 규칙이다:**

| `direction` \ `consent` | `anchored` | `unanchored` |
| ------ | ------ | ------ |
| `narrowing` | PASS 근거 가능 | **PASS 근거 가능** |
| `relaxing` | PASS 근거 가능 (사용자 재승인 성립) | PASS 근거 **불가** — 표면화 |
| `unknown` | PASS 근거 불가 — 표면화 | PASS 근거 불가 — 표면화 |

**앵커 부재가 `direction` 판정을 무너뜨리지 않는다 — 이것이 이번 개정의 핵심이다.** 직전 판은
두 축이 한 필드에 뭉쳐 있어 앵커가 없다는 이유만으로 방향까지 `unknown` 이 됐다. 실측:
`amendment A-01은 prompt-log 앵커 부재로 unknown 분류, PASS 근거 불가`. 그 결과 **준수 경로
(사이드카)의 기대 보상이 위반 경로보다 낮아졌고**, 같은 스프린트의 다음 시도에서 계약 본문
직접 편집(`AR-04: 계약 write-once 위반`)으로 우회가 일어났다. 두 축을 분리하면
`narrowing · unanchored` 는 정상적으로 PASS 근거가 된다 — 제약을 **강화**하는 방향이라 남용이
불가능하기 때문이다.

**집합형 조건의 `direction` 은 자기신고를 받지 말고 계산한다.** 경로 화이트리스트 · 파일 열거 ·
대상 목록처럼 조건이 집합을 담고 있으면 원 집합과 개정 집합을 `comm` 으로 비교해 계산한다.
계산 함수(`amend_direction`)의 정의는 **contract-schema §Amendment 사이드카 가 SSOT** 이며 여기서
재정의하지 않는다. 실측 위반(3 경로 → 5 경로)은 이 계산에서 `relaxing added=2 removed=0` 이
나온다 — 서술로 "범위 조정" 이라 부를 여지가 사라진다.

**왜 `relaxing · unanchored` 를 PASS 근거로 쓰지 않는가:** 평가자가 그대로 받아들이면
"구현이 조건을 못 맞춤 → 조건을 완화 → PASS" 라는 자기충족 루프가 생긴다. 이것이 정확히
`contract-scope-expanded-after-edit` 의 형태다. 완화가 정당한 경우도 있지만 그 판단은
**사용자 권한**이므로, 평가자는 원 조건으로 판정하고 완화 요청을 표면화한다.
`relaxing` 의 승인 주체는 사용자뿐이며 **reviewer 확인을 추가 요건으로 두지 않는다** — 평가자는
계약에 없는 요구를 만들지 않는다 (parity item 12 착지 구조).

### 기록 규약

- **원 조건을 삭제하지 않는다.** amendment 는 추가만 한다. "이 조건 폐기" 라고 적혀 있어도
  평가자는 원 조건을 계속 판정하고 폐기 요청을 사용자 확인 대상으로 올린다
- 앵커가 없으면 `consent: unanchored` 로 적는다. **앵커 부재를 `direction: unknown` 으로 적지
  마라** — 그것이 준수 경로를 무력화한 옛 결함이다. `direction` 은 PASS 집합의 증감으로만 정한다
- 인용문은 **"redaction 거친 원문"** 이다. reflect-kit 로그는 저장 시점에 민감 패턴을 마스킹하므로
  일부 토큰이 가려져 있어도 위조로 판단하지 않는다. "verbatim" 이라고 표기하지 마라
- 사이드카 부재는 결함이 아니다 — `amendments: 0` 으로 기록하고 진행한다
- **이어작업에서 확정된 `narrowing` 은 다음 계약 원문에 반영되어야 한다.** 사이드카가 원문을
  영구 대체한 채 남아 있으면 Improvement 로 올린다 (실측: `[LG-02, LG-04] write-once 계약 원문이
  amendment 로 대체된 채 남아있다`)

amendment 는 **verdict 를 자동으로 뒤집지 않는다.** PASS 근거로 쓸 수 있는 조합은 조건 판정에
흡수되고, 나머지는 표면화만 된다.

---

## 계약 봉인 검증 — `verify_seal` (E3)

> **대응:** `harness/references/contract-schema.md` v5.3 §계약 봉인 (정의 SSOT) ·
> 2026-08-11 REJECT `AR-04: 계약 write-once 위반 — 생성자가 자신이 만든 산출물을 사후에 허용하려
> 계약 조건 문구를 직접 편집(5→7 경로, 사이드카/사용자 승인 앵커 없음)`
>
> **배경:** write-once 는 오래된 규칙이지만 **위반을 재는 오라클이 없었다.** 저장 검사 게이트는
> 헤더와 조건 **개수**만 본다 — 문구가 바뀌어도 개수가 같으면 통과한다. Phase 2 가 봉인
> (`conditions_digest`)을 도입했고, **이 절이 그 소비면**이다. 소비면이 없으면 봉인은 작성 시점에만
> 검사되고 `SEAL_BROKEN` 이 verdict 에 반영되지 않는다.

### 함수 정의는 여기서 재정의하지 않는다

`sha256_16` · `contract_digest` · `verify_seal` 세 함수의 **정의 SSOT 는 contract-schema
§계약 봉인** 이다. 평가자는 그 절의 코드 블록을 **그대로 붙여넣어** 정의하고 호출만 한다.
평가자 문서에 다른 구현을 적으면 두 게이트가 서로 다른 집합을 해싱하게 된다.

### 3 값의 verdict 영향

| 결과 | 의미 | verdict 영향 |
| ------ | ------ | ------ |
| `SEAL_OK` | 조건 줄이 봉인 시점과 동일 | 없음 — 정상 진행 |
| `SEAL_ABSENT` | `conditions_digest` 필드가 없다 (레거시) | **없음 — 경고이지 실패가 아니다.** 실측 109 개 계약 전부가 이 상태이므로 BLOCKED 로 만들면 전 배포본이 죽는다 |
| `SEAL_BROKEN` | 조건 문구가 변조됐거나 조건이 추가·삭제됐다 | 아래 분기 |

**`SEAL_BROKEN` 분기:**

- 사이드카에 그 변경을 기술한 amendment 가 있고 `consent: anchored` 이면 →
  `contract_seal_broken: reconciled` 로 **경고 + 사용자 확인 목록**에 올린다. verdict 무영향.
  본문 편집은 여전히 규약 위반이지만 의도는 사용자 동의로 뒷받침된다
- 그 외 → `contract_seal_broken: unreconciled` + **verdict 는 REJECT**. `recorded` / `actual`
  두 값을 그대로 인용한다

**왜 BLOCKED 가 아니라 REJECT 인가:** BLOCKED 는 verdict 부재라 글로벌 피드백 코퍼스에 위반이
남지 않는다 — `AR-04` 형태의 write-once 위반이 통계에서 사라지고, 그러면 다음 카이젠이 이 결함을
볼 수 없다. 조건 자체는 현재 본문으로 평가 가능하므로 평가를 끝내고 REJECT 로 기록한다.

**절대 하지 마라:**

- **조용히 다시 봉인하지 마라.** 그것은 위반을 지우는 행위다. 평가자는 계약 본문을 수정하지
  않는다 (APPROVE 시 frontmatter `status` 전환만 예외이며, 봉인은 조건 줄만 해싱하므로 그
  전환으로 깨지지 않는다)
- **레거시 계약에 봉인을 소급해서 써 넣지 마라.** 그 순간 원문이 무엇이었는지 증명할 수 없는
  봉인이 된다

---

## User Correction Audit — 반영되지 않은 사용자 교정 표면화

> **대응:** `harness/agents/qa-evaluator.md` Step 3.4 · reflect-kit prompt 로그 ·
> digest usc(user_said_correction)=true 재위반 12 건
>
> **배경:** 사용자가 스프린트 도중 방향을 교정했는데 그 교정이 계약에도 amendment 에도 남지 않고
> 구현만 바뀌는 경로가 있다. 그러면 계약 기준 평가는 통과하는데 사용자가 실제로 요구한 것은
> 빠진다. 계약만 보는 평가자는 이 구멍을 구조적으로 볼 수 없다.

### 읽기 전용이 절대 조건

QA 는 사용자 로그 저장소를 **변형시키면 안 된다.** 평가 행위가 관측 대상을 바꾸면 그 로그는
이후 어떤 분석에서도 신뢰할 수 없다.

- 새 로그 버킷 디렉토리, `.project-root` 마커, 인덱스 파일 등 **어떤 파일·디렉토리도 만들지
  않는다.** `mkdir` · `touch` · 리다이렉트 쓰기 금지
- reflect-kit 의 `compute_project_id` 는 **write-side 헬퍼**다 — 호출하면 버킷과 마커를
  ensure 한다. **읽기 경로에서 쓰지 마라**
- 경로는 git root basename 기준 **read-union** 으로 해석한다: `basename` 과
  `basename-??????`(6 자 hash suffix) 두 형태를 합집합으로 조회. 어느 쪽도 없으면 로그 부재다

```bash
# 읽기 전용 — 생성 없음. read-union 도 셸 glob 이 아니라 find 로 한다.
BASE=$(basename "$(git -C "$CONTRACT_ROOT" rev-parse --show-toplevel 2>/dev/null || echo "$CONTRACT_ROOT")")
LOGS_ROOT="${REFLECT_KIT_LOGS_ROOT:-$HOME/.claude/logs}"
DIRS=$(find "$LOGS_ROOT" -maxdepth 1 -type d \
  \( -name "$BASE" -o -name "$BASE-??????" \) 2>/dev/null | sort)
[ -n "$DIRS" ] && echo "$DIRS" || echo "correction_log_status: unavailable"
```

> **`ls -d ... "$LOGS_ROOT/$BASE"-??????` 형태를 쓰지 마라.** hash 버킷이 없는 통상 환경에서
> zsh 는 `nomatch` 로 **ls 를 실행조차 하지 않는다** — 버킷이 실재해도 `DIRS` 가 비어
> `unavailable` 로 상시 오판한다. 실측: `~/.claude/logs/claude-plugins` 가 존재하는데
> zsh 는 `no matches found` 후 unavailable, bash 만 정상. `find` 는 패턴을 셸이 아니라 find 가
> 해석하므로 두 셸에서 동일한 결과를 낸다. (exit code 가 아니라 **출력**으로 판정하는 원칙은
> 그대로 유지된다.)

### 대조 절차

1. read-union 으로 나온 디렉토리의 월간 로그 `YYYY-MM.md` 를 읽는다. 항목 형식은
   `## [prompt] {timestamp}` + `- session:` + `- cwd:` + 본문
2. 스프린트 기간(계약 frontmatter `created` ~ 평가 시각)의 사용자 발언만 추린다
3. 교정 성격(방향 변경 · 범위 조정 · 금지 지시 · 재작업 요구)의 발언을 골라 현재 계약 조건 +
   amendment 목록과 대조한다
4. 어느 쪽에도 반영되지 않은 것을 `unreflected_corrections` 로 집계하고 건별
   `[timestamp · session · 한 줄 요약]` 을 남긴다

### verdict 영향은 없다 — 표면화 전용

- **자동 REJECT 를 유발하지 않는다.** `unreflected_corrections` 는 두 미검증 카운터 어디에도
  **합산하지 않으며** 2 건 자동 REJECT 임계와 무관하다
- 대조 결과가 개별 조건의 PASS/FAIL 을 바꾸지 않는다. 평가 기준은 여전히 계약 문자 그대로다
- 로그가 없으면 `correction_log_status: unavailable` 로 기록하고 **기존 QA 를 그대로 계속한다.**
  로그 부재는 BLOCKED 도 FAIL 도 아니다. 있으면 `available`

> **왜 자동 REJECT 하지 않는가:** 사용자 발언에서 "교정" 을 식별하는 것은 LLM 판단이며
> 오탐이 불가피하다. 오탐이 verdict 를 뒤집으면 평가 신뢰도 자체가 무너진다. 이 단계는 E1 —
> 사람이 볼 수 있게 올려놓는 것까지가 역할이다. 재발이 관측되면 등급을 올린다.

---

## 계약 파싱 범위 — 조건 섹션 / 서술 섹션

> **대응:** `contract-schema.md v4 §허용 섹션 헤더` · Phase 2 kaizen (2026-07-27) ·
> digest `parser-incompatible-contract-section`
>
> **배경:** 계약 v4 부터 계약 파일의 `##` 헤더는 **조건 섹션(parsed)** 과 **서술 섹션
> (non-parsed)** 2 계층으로 나뉜다. 서술 섹션(`배경`·`리서치 소스`·`GAP 분석`·`범위 경계`·
> `회귀 게이트`)에는 설명용 불릿이 자유롭게 들어간다. 평가자가 이 불릿을 조건으로 오파싱하면
> **계약에 없는 요구를 스스로 만들어내고**, 반대로 조건 섹션을 놓치면 커버리지 구멍이 생긴다.

### 파싱 규칙

1. **조건은 조건 섹션에서만 읽는다.** 조건 섹션 헤더는 `project.yaml.contract_categories` 의
   각 `id` + `Anti-patterns` + `Reusability` + `Diagnostics` 이며 **정확히 일치**해야 한다
   (괄호 부연이 붙어 있으면 계약 결함 — 아래 4 항)
2. **서술 섹션은 컨텍스트로만 읽는다.** `배경`·`리서치 소스`·`GAP 분석`·`범위 경계`·
   `회귀 게이트` 는 접두 일치(뒤에 부연 허용)로 식별하며, 여기의 불릿은 **조건이 아니다**.
   설계 의도 파악에는 쓰되 PASS/FAIL 판정 대상으로 삼지 않는다
3. **조건 수를 frontmatter 와 대조한다.** 파싱한 `- [ ] {PREFIX}-{NN}` 개수가 frontmatter 의
   `conditions:` 값과 다르면 평가를 시작하지 말고 BLOCKED 로 보고한다 — 조건을 놓친 채 내린
   verdict 는 무효다
4. **허용 목록 밖 헤더 발견 시** 그 섹션의 조건은 평가하되, Sprint Feedback 에 "계약 헤더 규약
   위반 — contract-schema v4 §허용 섹션 헤더" 를 계약 결함으로 기록한다. 평가자가 헤더를
   임의로 재분류하지 않는다

### 결정론적 확인 (E3)

평가 시작 전 1 회 실행하고 출력을 근거에 남긴다:

```bash
# (1) 헤더 2 계층 확인 — 허용 목록 밖 헤더가 있으면 계약 결함
grep -n '^## ' "$CONTRACT"

# (2) 조건 섹션 밖 체크박스 — 출력이 있으면 서술 섹션에 조건이 섞인 것
awk '/^## /{s=$0} /^- \[ \]/{print FNR": "s}' "$CONTRACT"

# (3) 조건 수 대조 — 두 값이 달라야 할 이유는 없다
grep -cE '^- \[[ x]\] [A-Z]{2,}-[0-9]{2}' "$CONTRACT"
grep -E '^conditions:' "$CONTRACT"
```

`$CONTRACT` 는 §계약 선택 ladder 에서 **선택·지문 고정된 계약의 절대경로**다 — plain
`sprint-contract.md` 일 수도, 접미형 `sprint-contract-<slug>.md` 일 수도 있다. `CONTRACT_ROOT` 는
`.harness/project.yaml` 을 가진 가장 가까운 조상의 절대경로이며, 세션 중 cwd 가 바뀌어도 이 값을
기준으로 해석한다 (contract-schema §산출물 경로).

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
6. **상태 의존 측정 명령의 전제 확인** — 측정 명령이 `git diff` / `git status` / 빌드 산출물처럼
   **실행 시점의 상태에 따라 결과가 달라지는** 것이면, 계약이 상태 전제(`Given: 커밋 직전 working
   tree` / `Given: 스테이징 완료 후` / 브랜치 비교)를 명시했는지 확인한다. 명시되지 않았으면
   **평가자가 상태를 임의로 고르지 마라** — Step 1.5 에서 "상태 전제 미명시" 플래그를 세우고,
   실제 판정에 사용한 상태를 근거란에 반드시 기록한다 (`측정 상태: HEAD 대비 working tree`).
   contract-schema v4 §Diff-Scope Oracle 표준형이 계약 측 대응이며, 표준형 4 요소(상태 전제 ·
   경로 한정 · 생성물 제외 · 기대 집합) 중 빠진 것을 REJECT 사유에 열거한다

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

> **대응:** `contract-design-guide.md §미검증 마커` · `contract-schema.md v4 §SCH-02` · `agent-design-guide.md §10`
>
> **배경:** mcp_server=null, 런타임 미실행, 외부 도구 미가용 등으로 정적 검증이 불가능한 조건의 **일관된 처리** 를 위해 도입. fit-pal LG-02/DG-04 · fit-pal-flutter 2026-04-17 REJECT 의 근본 원인이었다.

### 마커 부착 절차

외부 도구·MCP·런타임 등으로 검증 불가 시 평가자는 아래 순서를 따른다:

1. **단계 1 (기본 검증)** 시도 — 계약에 기술된 1차 검증 도구 실행
2. 단계 1 실패 시 **단계 2 (Fallback 정적 검증)** 시도 — 계약에 명시된 대체 정적 검증 수행 (예: 파일 Grep, CSS 변수 대조, log 파일 tail)
3. 단계 2 도 실패 시 **단계 3 (`[미검증:ENV]` 마커)** 부착 — 근거 블록에 "검증 불가 사유 한 줄 + 사용한 단계 기록" + §증거 분류 triage 의 남용 방지 4 요건. 단계 2 를 건너뛰면 4 요건 2 항 미충족이라 `[미검증:INVALID]` 로 강등된다
4. 계약에 fallback 기술이 없으면 **계약 작성자가 누락** 한 것이므로 REJECT 사유에 "fallback 미기술" 플래그

### 증거 분류 triage — `[미검증]` 은 도구 부재 전용이고, 그 안에서 다시 갈린다 (v4 축소 → 2026-08 카운터 분리)

> **대응:** `contract-design-guide.md v4 §양면 조건 5 항` · `contract-schema.md v4` ·
> 2026-08-11~12 글로벌 REJECT 4 건 (`UI-01`/`DG-02`/`DG-04` — 전부 "도구부재로 정당하나 임계 2 건")
>
> **배경:** 계약 v4 부터 `[미검증]` 의 의미가 **검증 도구·환경 부재 전용**으로 축소되었다.
> 양면 작업에서 아직 손대지 않은 쪽은 `[미검증]` 이 아니라 **명시적 미완 조건**으로 계약에
> 남긴다. 평가자가 이 구분을 놓치면 심각한 누수가 생긴다 — **미구현을 미검증으로 분류하면
> FAIL 이어야 할 조건이 "1 건까지 PASS 허용" 구간으로 세탁된다.**

조건을 PASS 로 확정하기 전에 아래 **4 분기** 중 하나로 반드시 분류한다 (2026-08-13 · B 를 두
분류로 쪼갰다):

| 분기 | 판정 | 분류어 | 상태 | 예시 |
| ---- | ---- | ---- | ---- | ---- |
| **A. 대상 부재 / 미구현 / 의도적 미실행** | **FAIL** | — | 검증 대상이 없거나, 있어도 조건을 충족하지 않거나, **수행 자체를 회피·이연**했다 | 조건이 지목한 파일·함수·필드가 없음 · consumer 면 미반영 · 계약이 경로를 명시한 기록물 부재 · `실기 앱 구동 미실행(계획적 이연) — 도구 부재 아님` |
| **B1. 도구·환경 부재 (통제 불가)** | `[미검증:ENV]` | `UNVERIFIED_ENV` | 대상은 존재하고 구현자가 통제할 수 없는 도구·런타임·MCP·시뮬레이터가 없다 | `mcp_server: null` 로 런타임 캡처 불가 · IDE 진단 미가용 · SDK 미설치 · 라이브 DB 접근 불가 |
| **B2. 4 요건 미충족 도구부재 주장** | `[미검증:INVALID]` | `UNVERIFIED_INVALID_EVIDENCE` | 도구 부재라고 적었으나 아래 4 요건 중 하나 이상이 근거란에 없다 | "MCP 없어서 못 봤다" 한 줄 · fallback 시도 기록 없음 · 재검증 명령 없음 |
| **C. 증거 무효 (vacuous)** | `[미검증:INVALID]` | `UNVERIFIED_INVALID_EVIDENCE` | 검증은 실행됐으나 그 출력이 아무것도 입증하지 못한다 | 빈 스냅샷 · 0 매치 grep 을 "위반 없음" 으로 해석 · 0 개 테스트가 실행된 테스트 통과 (§Evidence Validity Gate) |

**마커 어간은 여전히 `[미검증]` 하나다.** `:ENV` / `:INVALID` 는 **동의어가 아니라 분류 접미**이며,
Canonical Unverified-Evidence Protocol 1 항(동의어 금지)과 충돌하지 않는다. **접미가 없는
레거시 `[미검증]` 은 `INVALID` 로 해석한다** — 기존 배포본의 판정이 관대해지는 방향으로 바뀌지
않게 하기 위한 엄격 기본값이다.

**분류 규칙:**

- **A 를 B1 으로 적지 마라.** "구현이 안 돼서 확인할 게 없다" 는 미검증이 아니라 FAIL 이다.
  **"사용자 지시로 이번엔 안 돌렸다" 도 FAIL 이다** — 통제 불가가 아니라 선택이다.
- 분기 판정이 애매하면 **A(FAIL) 쪽으로 기운 엄격 해석**을 적용하고, Sprint Feedback 의
  `contract_ambiguity_notes` 에 사유를 남긴다
- B1 판정에는 **아래 4 요건이 전부** 근거란에 있어야 한다. 하나라도 없으면 B2 로 강등한다

#### `UNVERIFIED_ENV` 남용 방지 4 요건 (하나라도 없으면 B2 강등)

1. **1 차 도구 시도 기록** — 계약이 지정한 기본 검증 도구를 실제로 호출했고 그 결과(에러 메시지·
   타임아웃·미설치 출력)를 근거란에 인용했다
2. **fallback 시도 기록** — 계약의 단계 2(대체 정적 검증)를 수행했다. 계약에 fallback 이 없으면
   "fallback 미기술" 을 **계약 결함**으로 기록하는 것까지가 이 요건이다
3. **실패 로그** — 1·2 의 실패를 서술이 아니라 **출력**으로 남겼다. "확인 불가했다" 는 로그가 아니다
4. **통제 불가 사유 + 재검증 명령** — 왜 이것이 **구현자가 통제할 수 없는** 환경 요인인지 한 문장으로
   적고, 환경이 갖춰졌을 때 이 조건을 통과시킬 **실행 가능한 명령**을 함께 적었다

> **왜 4 요건인가:** 카운터를 분리하면 "미구현을 도구 부재로 세탁" 하는 경로가 열린다. 4 요건은
> 그 세탁을 비싸게 만든다 — 세탁하려면 존재하지 않는 도구 호출 로그와 재검증 명령까지 지어내야
> 하고, 그것은 §Evidence Validity Gate 검사 4(출처)에서 걸린다.

#### 반복 `UNVERIFIED_ENV` 는 환경 문제가 아니라 계약 결함이다

**같은 조건 ID 가 2 iteration 연속 `UNVERIFIED_ENV`** 이면 그것은 일시적 환경 문제가 아니라
**계약이 검증 경로를 적지 않은 결함**이다 (실측 improvement: `[DG-04] 검증경로-미기재 —
2 이터레이션 연속 [미검증]`). 이때는:

- 해당 조건을 `[low-confidence]` 로 강등하고 §Recurring Improvement Escalation 으로 승급한다
- Improvement 를 `[조건 ID] 검증경로-미기재 — {명시할 fallback 오라클 또는 부여할 MCP 바인딩}`
  형식으로 적는다. 산문 권고 금지
- **이 조건은 더 이상 `UNVERIFIED_ENV` 로 세지 않고 `UNVERIFIED_INVALID_EVIDENCE` 로 센다.**
  환경을 두 번 기다려 준 뒤에도 계약이 그대로면 그것은 계약 측 미해결이다

### 카운팅 및 자동 REJECT 임계 (2026-08-13 개정 — 카운터 분리)

**결함은 `[미검증]` 자체가 아니라 "정당한 도구·환경 부재" 와 "회피성 미실행 / 공허한 증거" 를
같은 reject counter 에 넣은 것**이었다. selective prediction 관점에서 abstention 은 failure 가
아니라 **uncovered case** 이므로 따로 집계한다 (근거: 아래 §왜 카운터를 분리하는가).

| 카운터 | 대상 분기 | 판정 |
| ------ | ------ | ------ |
| `invalid_evidence` | B2 + C | 0 건 통상 · **1 건 PASS 허용 + 경고 명시** · **2 건 이상 자동 REJECT** (개별 FAIL 이 없어도 verdict 는 REJECT) |
| `env_gaps` | B1 | 자동 REJECT 카운터에 **합산하지 않는다.** 대신 아래 커버리지 게이트를 적용하고 건수를 verdict 본문에 노출한다 |

#### 검증 커버리지 게이트 (E3)

```text
verified_coverage = (conditions_total − env_gaps) / conditions_total
```

- `verified_coverage` 가 **0.60 미만이면 APPROVE 를 낼 수 없다.** verdict 는 REJECT 가 아니라
  **BLOCKED** (`insufficient_verified_coverage`) 다 — 원인이 구현이 아니라 환경이므로 구현자를
  벌하는 판정으로 기록하면 피드백 코퍼스가 오염된다. 복구책은 4 요건 4 항의 **재검증 명령 목록**을
  실행한 뒤 재호출이다
- **임계 `0.60` 은 증명된 값이 아니라 출발값이다.** selective classification 에서 원하는 risk
  level 을 맞추기 위해 필요한 만큼 abstain 하는 설정의 예시가 coverage 약 60% 였다
  ([arxiv 1705.08500](https://arxiv.org/abs/1705.08500)). **재조정 트리거**: 이 게이트가 BLOCKED 를
  낸 사례가 3 회 누적되면 evaluator-kaizen 이 실측 분포로 임계를 다시 정한다
- verdict 우선순위는 아래 순서로 확정한다. 위에서 성립하는 첫 항에서 멈춘다:
  1. 평가 전제 붕괴(계약 선택 불가 · TOCTOU · 조건 수 불일치) → **BLOCKED**
  2. `SEAL_BROKEN` 미해소 → **REJECT** (§계약 봉인 검증)
  3. FAIL ≥ 1 → **REJECT**
  4. `invalid_evidence` ≥ 2 → **REJECT**
  5. `verified_coverage` < 0.60 → **BLOCKED** (`insufficient_verified_coverage`)
  6. 그 외 → **APPROVE** (`env_gaps: N` 을 본문에 노출)

#### 왜 카운터를 분리하는가 (근거)

- selective classification 은 원하는 risk level 을 정하고 테스트 시점에 필요한 만큼 **reject
  (abstain)** 해서 risk 를 맞춘다. abstention 은 오답이 아니라 **coverage 감소**로 회계된다
  ([arxiv 1705.08500](https://arxiv.org/abs/1705.08500))
- uncertainty 기반 abstention 은 correctness 를 **+2~8%**, unanswerable 질문의 hallucination 을
  **50%** 회피, safety 를 **70%~99%** 개선했다 ([arxiv 2404.10960](https://arxiv.org/abs/2404.10960))
- 다만 abstention 은 미해결 문제다 — 20 dataset / 20 frontier LLM 평가에서 **reasoning
  fine-tuning 이 abstention 을 평균 24% 악화**시켰다 ([AbstentionBench —
  arxiv 2506.09038](https://arxiv.org/abs/2506.09038)). 그래서 abstention 을 **자유롭게 허용하지
  않고** 4 요건 + 커버리지 게이트 + 재발 승급으로 묶는다

> **트레이드오프 (반드시 읽어라):** abstention 완화는 회피 경로가 된다. **4 요건 없이는
> `UNVERIFIED_ENV` 분류를 허용하지 마라.** 이 절은 "미검증을 봐주는 규칙" 이 아니라 "구현자가
> 통제할 수 없는 것과 통제할 수 있는 것을 다른 장부에 적는 규칙" 이다.

### 집계 의무

Step 4 판정 시 평가자는 Sprint Feedback 에 다음을 기록:

```text
## Unverifiable Summary
- invalid_evidence: K   [조건 ID, 분기(B2|C), 사유, 시도한 fallback 단계]
- env_gaps: M           [조건 ID, 1차 도구 시도, fallback 시도, 실패 로그, 통제 불가 사유 + 재검증 명령]
- verified_coverage: (conditions_total - env_gaps) / conditions_total = 0.xx (임계 0.60)
- 연속 ENV 승급: [조건 ID — 2 iteration 연속 → invalid_evidence 로 이관]
- Verdict 영향: {통상 | PASS 허용(경고) | 자동 REJECT | BLOCKED(insufficient_verified_coverage)}
```

### 실패 사례 (이 프로토콜 없이 발생)

- **fit-pal-flutter 2026-04-17**: 미검증 3 건 (LG-02, DG-03, DG-04) 발생했으나 평가자가 카운팅 규칙을 명시하지 않아 partial PASS 처리 → 추후 REJECT 재판정
- **fit-pal 2026-04-21**: UI-04/LG-04 미검증에도 3 단계 fallback 미수행 → 단계 2 대체 정적 검증 가능했음에도 건너뛰고 바로 [미검증]

### 실패 사례 (분리 이전 규칙이 만든 오처벌 — 이번 개정의 직접 원인)

2026-08-11~12 에 같은 형태의 REJECT 가 **4 건 연속** 관측됐다. 네 건 모두 개별 조건 FAIL 이
아니라 임계 규칙만으로 verdict 가 뒤집혔고, 미검증 사유는 전부 구현자 통제 밖이었다:

- `미검증 2건(UI-01, DG-02) — 둘 다 도구부재(런타임 캡처 MCP 미가용, IDE 진단 미가용)로 정당하나 임계 2건 이상이라 자동 REJECT 규칙 적용`
- `미검증 2건(DG-02 IDE lint 도구부재, DG-04 시뮬레이터 미부팅) — 2건 이상 자동 REJECT 규칙`
- `Unverifiable count = 2 (DG-02, DG-04) triggers automatic REJECT per contract v4 rule`
- `DG-02/DG-04 미검증 2건 — 자동 REJECT 임계(2건 이상) 충족 (도구부재/환경충돌, AR-04와 별개 사유)`

**반대 극단은 같은 기간에 정상 작동했다** — `DG-04: 실기 앱 구동 미실행(사용자 지시에 의한
계획적 이연) — 실행 산출물 부재로 FAIL(도구 부재 아님, 의도적 미실행)`. 즉 규칙을 느슨하게 할
문제가 아니라 **두 사유를 다른 장부에 적는 문제**였다. 이 절의 개정은 완화가 아니라 정밀화다.

---

## Execution-Grounded Evidence (실행 주장 조건의 산출물 검증)

> **대응:** `/insights` Friction #5 (스킬/도구 가짜 호출) · §1 글로벌 피드백 "AR-03: 스킬 invoke 파일시스템 아티팩트 없음 (2026-05-17)"
>
> **배경:** 구현자가 도구·스킬·명령을 **실제로 실행하지 않고** "실행했다 / 호출했다 / 생성했다"고 서술만 하는 패턴. /insights 에서 "`/insights` 를 실제 호출하지 않고 기존 파일을 읽은 뒤 호출했다고 주장" 으로 보고됨. 기존 "주석·커밋 메시지는 증거가 아니다" 원칙은 generator 의 **주장**을 배제하지만, 계약 조건이 **동적 실행 자체**를 요구할 때 evaluator 가 실행이 일어났다는 **산출물**을 능동적으로 요구하는 축은 별개다.

### 적용 대상 조건

조건이 "실행 / 호출 / 생성 / 재생성 / 발행 / 빌드 / 마이그레이션 적용" 처럼 **동작이 실제로 수행되었음**을 요구하면(단순 파일 존재·내용이 아니라 행위) 아래 절차를 적용한다.

### 검증 절차 (narrated 주장 대신 observable artifact)

1. **실행 산출물 식별** — 그 동작이 일어났다면 남았어야 할 관찰 가능한 흔적을 먼저 정한다: 명령 출력(exit code·stdout), 생성/수정된 파일·번들, 로그 라인, codegen 결과물, git diff, lockfile 변경 등
2. **산출물 직접 수집** — evaluator 가 직접 Bash/Glob/Grep 으로 그 흔적을 수집한다. 구현자의 "실행했다" 서술이나 대화 로그는 증거가 아니다
3. **부재 시 `[미검증]`** — 흔적이 없으면 "실행되지 않았을 가능성" 으로 본다. 분류는 사유로 갈린다 — 도구·환경 부재로 실행이 불가능했고 4 요건을 남겼으면 `[미검증:ENV]`, 사유 없이 산출물만 없으면 `[미검증:INVALID]`, **실행을 의도적으로 이연했으면 FAIL** 이다. "코드상 호출 경로가 있으니 실행됐을 것" 이라는 추론 PASS 금지 — 호출 경로 존재는 L2 이며, 실제 실행 증거는 별개 축이다
4. **재현 가능하면 직접 실행** — evaluator 도구로 해당 명령을 재실행 가능하면(예: `commands.analyze`, 버전 출력) 직접 돌려 출력으로 판정한다

### 실행 판정 기준

- 실행 산출물 확보 → PASS (근거에 `명령/산출물 → 관찰값` 형식)
- 산출물 부재 + 재현 불가 → `[미검증:ENV]`(4 요건 충족 시) 또는 `[미검증:INVALID]` (둘 다 PASS 아님)
- 구현자가 "실행했다" 서술했으나 산출물 없음 → narrated claim 으로 분류, 증거 불인정

### 근거 (리서치)

- 판정자는 narrated reasoning 이 아니라 **observable evidence 에 대해 reasoning claim 을 검증**해야 한다. CoT/서술을 신뢰하면 fabricated progress signal 에 속아 false positive 가 최대 90% 증가 ([Gaming the Judge — arxiv 2601.14691](https://arxiv.org/abs/2601.14691))
- "실행했다" 주장은 실제 실행 로그(receipt)와 **대조**하여 검증한다. 로그 없는 호출 주장은 fabricated tool reference 로 분류 ([Tool Receipts, Not Zero-Knowledge Proofs — arxiv 2603.10060](https://arxiv.org/pdf/2603.10060))

### 실패 사례

- **fit-pal-app AR-03 (2026-05-17)**: "스킬 invoke" 조건에서 파일시스템 아티팩트가 없어 실행 여부를 구조적으로 검증 불가 → 산출물 부재이므로 `[미검증]` 이 정답. 실행 주장만으로 PASS 처리하면 가짜 호출을 통과시킴

---

## Evidence Validity Gate — 공허한 증거(vacuous pass) 차단

> **대응:** `skill-design-guide.md §3.7` 5 조 4 항 (생성 측 짝) · `agent-design-guide.md §10`
> Unverifiable 정책 4 항 · `/insights` 2026-07-27 Friction #2 (최상위 신규 신호)
>
> **배경:** 앞의 §Execution-Grounded Evidence 는 증거가 **존재하는지**를 요구한다. 실측에서
> 반복된 사고는 그 다음 단계였다 — **증거는 있는데 그 증거가 아무것도 입증하지 않는 경우**.
> 빈 카탈로그 화면의 MCP 스냅샷을 근거로 "정상 렌더링" 을 반복 주장했고, 실제로는
> unbounded-height ListView 가 collapse 한 상태였다. 사용자 신뢰가 손상되어 욕설로 끝난 세션이
> 2 건 발생했고, 사용자가 이 재발 습관 교정만을 위한 전용 세션을 열었다.

### 왜 별도 축인가

- LLM 판정자는 **타당성(validity)이 아니라 그럴듯함(plausibility)** 을 채점한다. 프런티어 판정자
  2 종이 필요한 아티팩트를 **한 번도 가져오지 않은** 답변에 0.90 / 0.85 를 주고 추론이
  "tight and well-structured" 라고 칭찬했다. 실행 trace 를 결정론적으로 대조하자 같은 답변의
  점수는 **0.000** 이었다 ([GroundEval — arxiv 2606.22737](https://arxiv.org/html/2606.22737v2))
- 같은 연구의 실패 분류 중 **invalid absence** — "충분히 탐색하지 않고 없다고 단언" — 이
  Friction #2 의 정확한 형태다. 빈 스냅샷을 "문제 없음" 으로 읽는 것이 곧 invalid absence 다
- 최종 상태만 보는 outcome-only 평가는 절차 위반을 통과시켜 성능을 과대평가한다. 중간 상태와
  행위 시퀀스를 함께 대조해야 한다 ([Corrupt Success — arxiv 2603.03116](https://arxiv.org/pdf/2603.03116))
- 형식 검증 영역에서는 이 현상을 **vacuity** 로 오래 다뤄왔다. LLM 이 생성한 assertion 품질
  연구는 trigger coverage(조건이 실제로 활성화됐는가) · antecedent activation(전제가 한 번이라도
  참이 됐는가) · mutation/negative control(고의 결함을 실제로 잡는가) 3 축으로 "통과했지만
  아무것도 검사하지 않은" assertion 을 걸러낸다
  ([arxiv 2606.21451](https://arxiv.org/pdf/2606.21451))

### 유효성 5 검사 (PASS 확정 전 필수)

증거를 수집한 뒤, 그 증거로 PASS 를 주기 **전에** 아래 5 항을 통과해야 한다. 하나라도 실패하면
그 증거는 무효이며 조건은 PASS 가 아니라 `[미검증:INVALID]` (증거 분류 triage 분기 C) 이다.

| # | 검사 | 질문 | 실패 시 |
| - | ---- | ---- | ---- |
| 1 | **비공백 (non-empty)** | 출력·스냅샷·파일이 실제로 내용을 담고 있는가? 0 바이트·공백만·에러 메시지만 아닌가? | 증거 무효 → `[미검증:INVALID]` |
| 2 | **활성화 (trigger coverage)** | 그 측정이 검사 대상을 **실제로 한 번이라도 통과**했는가? 테스트 0 개 실행 · 스킵된 스위트 · 매치 0 건 grep 은 "위반 없음" 이 아니라 "검사되지 않음" 이다 | 증거 무효 → `[미검증:INVALID]` |
| 3 | **반증 가능성 (negative control)** | 조건이 위반된 상태였다면 **이 측정이 다른 결과를 냈을 것인가?** 어떤 입력에도 같은 출력을 내는 측정은 oracle 이 아니다 | 증거 무효 → `[미검증:INVALID]` + 계약에 측정 수단 재설계 권장. 규칙 12 의 9 항 대상이면 §Discriminating Evidence Gate 의 3 단계를 수행한다 |
| 4 | **출처 (provenance)** | 그 증거를 **평가자가 직접 수집**했는가? 구현자의 서술·주석·커밋 메시지·대화 로그를 인용한 것이 아닌가? | 증거 불인정 → 직접 수집 후 재판정 |
| 5 | **실행 가능성 (executability)** | 산출물이 **셸 스니펫·명령·스크립트를 담은 문서**라면, 그것이 문서에 적혀 있다는 사실이 아니라 **평가자가 직접 실행한 출력**을 근거로 삼았는가? 그리고 **사용자 셸(zsh)과 bash 양쪽**에서 실행했는가? | 증거 무효 → `[미검증:INVALID]` |

### 검사 5 특칙 — 서술은 실행이 아니다 (셸 이식성 포함)

문서가 제시하는 셸 스니펫은 **실행 가능해야 하며, 평가자는 서술의 존재가 아니라 실행 결과로
판정한다.** 스니펫이 조건이 요구하는 문구를 정확히 담고 있어도, 그 스니펫이 런타임에 깨지면
조건은 충족되지 않은 것이다.

- **zsh·bash 양쪽에서 실행한다.** 사용자 셸이 zsh 인 환경에서 bash 전용 코드는 배포 시점에
  파손이다. 대표적으로 zsh 는 기본 `nomatch` 라 **매치 없는 glob 이 명령을 통째로 죽인다** —
  `for f in a.md b-*.md` 는 `b-*.md` 가 없으면 루프에 진입조차 못 하고, `[ -f "$f" ] || continue`
  가드도 무력하다. `ls -d dir/x dir/x-??????` 도 같은 이유로 zsh 에서 실행되지 않는다.
  셸 무관 열거는 `find ... \( -name A -o -name B \)` 로 쓴다
- **의도한 출력이 나오는지까지 본다.** exit 0 은 통과 기준이 아니다. 스니펫이 뽑아낸 값이
  비교 대상과 실제로 일치하는지 확인한다 (예: frontmatter reader 가 따옴표를 벗기지 않으면
  `owner_session: "abc"` 는 `abc` 와 영원히 불일치한다 — 출력은 나오지만 로직은 죽어 있다)
- 실행 결과를 근거에 붙인다. `셸: zsh/bash · 출력: …` 형태로 남긴다

> **이 특칙이 없어서 놓친 실제 사고 (2026-07-28 병렬 스프린트 안전성):** 적대적 검증에서
> **25/25 조건이 문언상 PASS** 였는데 런타임은 깨져 있었다. 후보 열거 루프가 zsh nomatch 로
> 죽어 상시 오탐 BLOCKED 였고, reader 가 따옴표를 안 벗겨 ladder 2 단계가 영구 불성립이었으며,
> correction audit 의 read-union 은 zsh 에서 항상 `unavailable` 이었다. **오라클이 문서 서술만
> 검사했기 때문에 세 결함 모두 PASS 로 통과했다.**

### 0 매치 판정 규칙 — "없음" 은 두 가지다

`grep` 결과 0 건, 목록 0 개, 로그 0 줄 같은 **무활동 출력**은 그 자체로는 의미가 결정되지 않는다.
반드시 아래로 갈라 기록한다:

- **의도된 0** — 조건이 "위반 0 건" 을 요구하고, 그 grep 이 **다른 파일에서는 매치를 낸다는 것을
  확인**한 경우에만 PASS. 즉 패턴이 살아 있다는 증거(positive control)를 같이 수집한다
- **공허한 0** — 대상 경로가 틀렸거나, 파일이 비었거나, 패턴이 절대 매치되지 않는 경우.
  이것은 PASS 증거가 아니라 **측정 실패**다 → `[미검증:INVALID]`

```text
Bad:  grep -c 'unwrap()' src/ → 0 → "안티패턴 없음, PASS"
      ← src/ 에 .rs 파일이 0 개였다면 이 0 은 아무것도 입증하지 않는다
Good: (a) 대상 파일 목록을 먼저 세고(예: 42 개) (b) 패턴이 유효함을 알려진 위치에서 1 회 확인
      (c) 그 위에서 0 매치 → PASS. 근거: "대상 42 파일 · 패턴 유효성 확인 · 매치 0"
```

### 렌더 산출물 특칙 (Friction #2 직결)

UI·문서·차트처럼 렌더 결과를 캡처할 수 있는 산출물은 캡처를 증거로 쓰되:

- **빈 화면·빈 목록·플레이스홀더만 있는 캡처는 PASS 증거가 아니라 검증 실패 신호**다.
  "요소가 안 보이니 문제도 없다" 는 invalid absence 다
- 캡처에서 조건이 요구하는 **구체 요소를 지목**해 근거에 쓴다 (`스냅샷에 항목 3 행 · 헤더 텍스트
  "내 그룹" 확인`). 요소를 지목할 수 없으면 그 캡처는 무효 증거다
- 캡처 자체가 실패했거나 도구가 응답하지 않으면 그것은 분기 B1(`[미검증:ENV]` · 4 요건 충족 시) 이지 PASS 가 아니다

### 보고 형식

Sprint Feedback 의 `Unverifiable Summary` 블록에 무효 증거 건을 함께 집계한다:

```text
## Evidence Validity
- 검사 대상 증거: N 건
- 무효 판정: K 건 [조건 ID — 실패한 검사 번호(1~5) — 사유]
- 셸 스니펫 실행 검증: 실행 N 건 · zsh/bash 양쪽 확인 M 건 · 미실행 K 건 (검사 5)
- 무효 K 건은 미검증 카운터에 합산 (현재 누계: M)
```

### 실패 사례 — 무효 증거로 통과한 판정

- **fit-pal 2026-06~07 (Friction #2)**: 빈 카탈로그를 MCP 스냅샷 근거로 "정상 렌더링" 반복 주장.
  실제로는 unbounded-height ListView collapse. 검사 1(비공백)·검사 2(활성화) 어느 쪽도 통과하지
  못하는 증거였다
- **GroundEval 사례 (2606.22737)**: 판정자 0.85~0.90 vs trace 대조 0.000. 검사 4(출처)가 없으면
  판정자는 그럴듯한 서술을 증거로 착각한다

---

## Canonical Unverified-Evidence Protocol (각 kit reviewer 복제용 정본)

> **이 절이 정본(SSOT)이다.** `*-kit/agents/*-reviewer.md` 는 아래 5 조항을 **문구 변형 없이**
> 복제하고, 자기 문서에서 임계값이나 마커 의미를 다시 정의하지 않는다. 각 kit 의 카이젠 Phase 는
> 이 절을 인용 앵커로 삼는다: `harness/docs/guides/qa-evaluation-guide.md`
> §Canonical Unverified-Evidence Protocol.
>
> **현재 drift (2026-07-27 실측 · 각 kit Phase 가 해소할 것):**
> `design-reviewer` 는 임계 **3 건**("미검증 3항 프로토콜"), `backend-reviewer` ·
> `infra-reviewer` · `rust-reviewer` 는 2 건 + CONDITIONAL APPROVE, `planning-reviewer` 는
> 미검증 0 건 요구, `react-reviewer` 는 조항 없음. 킷마다 다른 임계는 같은 상태를 다른 verdict 로
> 바꾼다.

1. **마커는 `[미검증]` 하나로 통일한다.** 동의어(`미확인`, `N/A`, `TBD`, `unverified`) 를 만들지 않는다.
   `[정적]` 은 "런타임 없이 정적으로만 확인" 을 뜻하는 보조 태그이며 `[미검증]` 을 대체하지 않는다.
2. **`[미검증]` 은 검증 도구·환경 부재 전용이며, 그 안에서 다시 두 분류로 갈린다.** 대상이
   없거나 미구현이거나 **의도적으로 실행하지 않았으면** 그것은 미검증이 아니라 **FAIL** 이다.
   나머지는 `UNVERIFIED_ENV`(구현자 통제 밖 도구·환경 부재 · 남용 방지 4 요건 충족) 와
   `UNVERIFIED_INVALID_EVIDENCE`(4 요건 미충족 주장 + 공허한 증거) 로 나눈다
   (4 분기: FAIL / `UNVERIFIED_ENV` / 4 요건 미충족 / 증거 무효).
   마커 어간은 `[미검증]` 하나이며 접미 `:ENV` / `:INVALID` 는 분류다. **접미 없는 레거시
   `[미검증]` 은 `INVALID` 로 해석한다.**
3. **임계값 2 는 `UNVERIFIED_INVALID_EVIDENCE` 에만 적용된다.** 그 카운터가 0 건이면 통상 판정,
   **1 건은 PASS 허용 + 경고 명시, 2 건 이상은 개별 FAIL 이 없어도 verdict 는 REJECT**.
   "CONDITIONAL APPROVE" 를 쓰는 킷은 그것이 "1 건 + FAIL 0" 인 경우에만 유효하며 2 건 이상에는
   쓸 수 없다. **`UNVERIFIED_ENV` 는 이 카운터에 합산하지 않고** `env_gaps` 로 따로 세어
   검증 커버리지 게이트(`(총수 − env_gaps)/총수 < 0.60` → `BLOCKED`)에만 쓴다. 같은 조건이
   2 iteration 연속 `UNVERIFIED_ENV` 이면 계약 결함으로 승급해 `INVALID` 쪽으로 이관한다.
4. **생성자의 완료 주장은 증거가 아니다.** 구현자가 "동작 확인함 / 실행했음" 이라고 쓴 문장,
   코드 주석, 커밋 메시지의 자기 평가는 상태 검증이 아니다. 명시적 완료 주장을 포함한 자기평가
   에이전트 궤적에서 **실패의 75.8% 가 false success** 였고, LLM 판정자의 AUROC 는 0.54~0.65 에
   그쳤다 ([arxiv 2606.09863](https://arxiv.org/abs/2606.09863)). 근거는 **도구 출력과 상태
   변화**여야 한다.
5. **조용한 PASS 금지 + 집계 의무.** 검증을 건너뛰고 정적 정황만으로 PASS 를 주지 않는다.
   리포트에 `미검증 N 건` 을 반드시 집계하고, 건별로 `[조건/항목 ID, 사유, 시도한 fallback 단계]`
   를 남긴다.

> **2026-08-13 개정 전파:** 2 항·3 항이 4 분기 + 카운터 분리로 바뀌었다. `*-kit/agents/*-reviewer.md`
> 6 종은 이 절을 복제 중이므로 각 kit 카이젠 Phase 가 갱신한다. **본 Phase 는 reviewer 파일을
> 수정하지 않았다** — scope 밖이며, 여기서 손대면 kit Phase 가 두 번째 SSOT 를 만들게 된다.

---

## Canonical User-Reported Failure Protocol (각 kit reviewer 복제용 정본)

> **이 절이 정본(SSOT)이다.** `*-kit/agents/*-reviewer.md` 는 아래 5 조항을 **문구 변형 없이**
> 복제하고 상태어를 바꾸지 않는다. 상위 짝: `skill-design-guide.md` §3.8 (생성 측) ·
> `agent-design-guide.md` §10 "사용자 실패 보고 우선" (평가 측 Gotcha) — **parity item 8/14**.
> 등급은 `skill-design-guide.md` §3.7 등급 원장의 **E1** 을 따른다 (여기서 등급을 새로 정하지 않는다).
>
> **대응:** `/insights` 2026-08-13 신규 델타 D3 — A3 목업 변형이 깨졌다는 사용자 리포트에
> 테스트 증거로 **반박**하다 세션이 에스컬레이션됐고, 빈 카탈로그 세션도 동형이었다
> (MCP 스냅샷으로 사용자 관측을 부정하다 결국 unbounded-height ListView collapse 를 발견).

### §Evidence Validity Gate 와 무엇이 다른가 (혼동 금지)

두 절은 **서로 다른 검사**이며 하나가 다른 하나를 대체하지 않는다.

| | §Evidence Validity Gate | §Canonical User-Reported Failure Protocol (이 절) |
| ---- | ---- | ---- |
| 무엇을 재는가 | **자기 증거의 유효성** — 내가 모은 증거가 실제로 무언가를 입증하는가 | **자기 증거와 사용자 증거의 우선순위** — 둘이 충돌할 때 무엇을 기준으로 삼는가 |
| 언제 도는가 | PASS 확정 **전** | 사용자 실패 보고가 **들어온 시점** (이미 PASS 를 준 뒤일 수 있다) |
| 실패 시 | 증거 무효 → `[미검증:INVALID]` | 상태어 `REOPENED` → 완료 판정 보류 → 재현 절차 |

**순서: 이 절이 먼저다.** 사용자 보고가 있으면 완료 판정을 먼저 보류하고, 그 다음에 유효성
5 검사로 내 오라클을 점검한다. 반대 순서로 하면 "내 증거는 유효하다" 를 근거로 사용자 보고를
기각하게 된다 — 그것이 D3 의 사고 형태다.

### 규약 5 조

1. **상태는 PASS 가 아니라 `REOPENED` 다.** 평가자가 PASS 를 준 항목에 대해 사용자가 "아직 깨져
   있다" 고 보고하면 그 항목의 상태어를 `REOPENED` 로 바꾼다. **이전 PASS 근거는 지우지 말고**
   "그때 그 오라클로는 통과했다" 는 기록으로 보존한다.
2. **자기 테스트·스냅샷은 "내 환경에서의 관측" 이다.** 그것은 사용자 보고의 반박 근거가 아니다.
   상태 검증은 self-report 가 아니라 **target system** 을 봐야 한다. 자기평가 궤적에서 실패의
   **75.8% 가 false success** 였다는 관측이 평가자에게도 그대로 적용된다
   ([arxiv 2606.09863](https://arxiv.org/abs/2606.09863)).
3. **먼저 오라클 유효성부터 의심한다.** 사용자 보고가 틀렸을 가능성을 따지기 전에, 내 오라클이
   **사용자가 보는 것을 재고 있었는지**를 6 축으로 대조한다. **값싼 축부터** 확인하고 비싼 축은
   앞 축이 전부 일치할 때 넘어간다:

   | # | 재현 축 | 확인 질문 |
   | --- | --- | --- |
   | 1 | **URL / 경로** | 사용자가 연 화면과 내가 검사한 화면이 같은 라우트인가 |
   | 2 | **브랜치 / 커밋** | 사용자가 돌린 코드가 내가 검사한 커밋과 같은가 (스테일 빌드 포함) |
   | 3 | **viewport** | 폭·높이가 같은가. 무제한 높이로 잰 결과는 실기 화면을 재지 않는다 |
   | 4 | **디바이스 / 플랫폼** | 실기기·시뮬레이터·브라우저 중 무엇인가 |
   | 5 | **auth · cache** | 로그인 주체, 캐시·서비스워커·핫리로드 잔여 상태가 같은가 |
   | 6 | **데이터 상태** | 같은 레코드·같은 빈 상태·같은 권한으로 보고 있는가 |

4. **반박 금지.** 재현 전에 "정상 동작합니다 / 테스트는 통과합니다" 를 다시 말하지 않는다.
   사용자 교정은 intent anchor 로 보존한다 — 실사용 20,574 세션 관측에서 가시적 해소의
   **91.49% 가 사용자의 명시적 교정**을 필요로 했다 ([arxiv 2605.29442](https://arxiv.org/html/2605.29442)).
5. **완료 선언 해제는 3 택 중 하나가 성립할 때만 한다.**
   - (a) 사용자 관측을 **재현**하고 수정한 뒤, 같은 조건에서 재검증한 출력을 인용한다
   - (b) 재현되지 않는 이유를 **환경 불일치로 특정**한다 (위 6 축 중 어느 축의 어떤 값이 달랐는지
     값으로 제시). "환경 문제인 것 같다" 는 특정이 아니다
   - (c) 사용자가 직접 **수정 확인**을 해준다

**오독 금지:** 이 절은 "사용자 보고를 무조건 사실로 인정하라" 가 **아니다.** 정확한 규약은
**완료 판정을 보류하고 오라클 유효성을 먼저 의심한다** 이며, 원인이 사용자 환경(스테일 빌드,
캐시)으로 밝혀지는 것도 위 (b) 로 정상 종결이다.

### 평가자 측 추가 규칙 (Human Oracle Challenge)

상위 가이드의 5 조는 "무엇을 하지 마라" 를 정한다. 평가자는 그 위에 **판정 매핑**이 필요하다.

- **승격 조건** — 사용자 보고에 **재현 절차 · 환경 · 기대 결과 · 실제 결과** 중 3 개 이상이
  구체적으로 있으면 해당 조건을 즉시 `REOPENED` 로 올린다. 4 개 다 있으면 최우선이다
- **재현되면 FAIL** — 원 PASS 를 취소하고 FAIL 로 재판정한다. 이전 근거는 삭제하지 않고
  "그때 그 오라클로는 통과했다" 로 남긴다
- **재현 불가 원인이 환경이면 `UNVERIFIED_ENV`** — 단 §증거 분류 triage 의 남용 방지 4 요건을
  그대로 적용한다. 6 축 중 어느 축이 달랐는지 값으로 특정하지 못하면 그것은 4 요건 4 항 미충족이라
  `UNVERIFIED_INVALID_EVIDENCE` 다
- **모호하거나 계약 범위 밖이면 자동 REJECT 하지 마라** — 계약에 없는 요구를 평가자가 만들어내는
  것과 같다. `user_report_out_of_contract` 로 표면화하고 **contract amendment 후보**로 기록한다
- **오라클 결함 자체를 환류한다** — 6 축 대조에서 내 오라클이 사용자와 다른 값을 재고 있었음이
  드러나면, 그것은 다음 계약의 개선 제안이다. Improvement 를 `[조건 ID] 측정-방식-불일치 —
  {계약이 지정해야 할 축과 값}` 형식으로 적는다 (실측 improvement `[ER-01] 측정-방식-불일치 —
  테스트가 계약 명시 360x800 뷰포트 대신 폭 320+ListView 무제한 높이로 측정` 과 같은 형태)

### 왜 6 축을 "공유 rubric" 으로 쓰는가 (근거)

자동 oracle 이 불완전하면 최종 oracle 정보원은 human 이다. 다만 human 도 비용·일관성 문제가 있어
그대로 verdict 로 받으면 판정이 흔들린다 ([UCL oracle
survey](https://discovery.ucl.ac.uk/id/eprint/1471263/)). 실제로 APR patch 평가에서 human manual
assessment 의 **Fleiss' Kappa 는 0.307** 로 낮았고, **shared high-quality rubric 이 agreement 를
크게 개선**했다 (48 bugs / 115 patches · human-refined golden rubric 기반 LLM judge 가 human
developer consensus 와 substantial agreement) ([Google
research](https://research.google/pubs/towards-a-human-in-the-loop-framework-for-reliable-patch-evaluation-using-an-llm-as-a-judge/)).
6 축 대조가 바로 그 shared rubric 이다 — 사용자 보고를 "믿는다/안 믿는다" 로 다루지 않고
**어느 축이 달랐는지** 로 정규화한다.

### 계약 측 착지가 없는 이유 (Phase 2 결정 인용)

`contract-design-guide.md` 는 parity item 14 를 **계약 측 착지 없음 — 평가 레이어 소관**으로
명시했다. 계약에 `REOPENED` 조건을 만들면 §증거 아티팩트 존재 의무 위반이 된다 — 계약 조건은
평가 시점에 실재하는 산출물을 가리켜야 하는데, `REOPENED` 는 **완료 판정 시점의 상태 전이**라
계약 작성 시점에 대응 아티팩트가 없다. 따라서 이 규약의 정본은 계약이 아니라 **이 절**이다.

---

## Discriminating Evidence Gate — 측정이 구현을 실제로 재는가

> **대응:** §Evidence Validity Gate 검사 3(반증 가능성)의 **집행 절차** ·
> `contract-schema.md v5.3 §음성 대조` (계약 측 짝) · 2026-08-12 글로벌 REJECT `ER-02`/`LG-01`/`LG-03`
>
> **배경:** 검사 3 은 "조건이 위반된 상태였다면 이 측정이 다른 결과를 냈을 것인가" 를 **묻기만**
> 했다. 실측에서 그 질문에 "예" 라고 답하고 넘어간 뒤 사후 mutation 으로 정반대가 확인됐다 —
> `ER-02: 신규 통합 테스트가 실제 바이너리를 호출하지 않고 독립 재작성한 SQL 로 일반 동작만
> 검증한다. **mutation test 로 확정 — 실제 코드에서 동시성 가드(WHERE exercises = $3::jsonb)를
> 완전히 삭제해도 이 테스트는 여전히 통과한다.**` 같은 날 `LG-01`(18 케이스 중 15 만 재현) ·
> `LG-03`(SQL grep 은 되나 증명 테스트 부재) 도 동형이다. 즉 필요한 것은 새 질문이 아니라
> **답을 강제로 확인하는 절차**다.

### 적용 범위 — 한정이 핵심이다

**아래 9 항 중 하나에 해당하고, 조건이 테스트·실행 산출물로 판정될 때만 필수**다:

1. 동시성 가드 (concurrency guard · 낙관적 락 · 조건부 UPDATE)
2. 인증 / 권한 (auth · permission)
3. 멱등성 (idempotency)
4. 입력 검증 (validation)
5. 데이터 유실 방지 (data-loss)
6. 마이그레이션 안전성 (migration safety)
7. 재시도 / 중복제거 (retry · dedup)
8. 보안 경계 (보안 취약점 차단 · 시크릿 노출 방지)
9. **사용자 결함 보고와 테스트 PASS 가 충돌한 경우** (§Canonical User-Reported Failure Protocol 연동)

**금지 (셋 다 하지 마라):**

- **전체 repo mutation score 임계값을 세우지 마라.** full mutation adequacy 달성은 산업 적용
  보고에서 **"neither practical nor desirable"** 로 결론났다
  ([Google](https://research.google/pubs/an-industrial-application-of-mutation-testing-lessons-challenges-and-research-directions/))
- **모든 조건에 강제하지 마라.** 위 9 항 밖의 조건에 요구하면 평가가 계약에 없는 비용을 만든다
- **cosmetic / doc-only 변경에 요구하지 마라.** 파일·섹션 존재를 보는 `[structural]` 조건은
  대상을 지우면 자명하게 실패하므로 음성 대조가 무의미하다

### 절차 3 단계 (비용 순 — 위에서부터 필수)

1. **결합 확인 (static · 필수)** — 측정이 계약이 지목한 구현을 **직접 경유**하는지 확인한다.
   테스트가 대상 바이너리·함수·쿼리를 호출하는지 Grep 으로 본다. 테스트가 로직을 **독립
   재작성**했으면 결합이 0 이고, 그 측정은 증거가 아니다 → 조건 **FAIL** (계약이 요구한 측정
   산출물이 없는 것과 같다). 근거란에 `결합: {테스트 파일:라인} → {구현 심볼}` 을 남긴다
2. **계약의 `음성 대조:` 절 확인** — contract-schema v5.3 은 테스트로 판정되는 조건에
   "어느 구현 지점을 무력화하면 이 측정이 FAIL 하는지" 를 적게 한다. 기재돼 있으면 그 지점을
   판정 기준으로 삼는다. **기재가 없으면 조건 결함이지 구현 결함이 아니다** — 자동 FAIL 하지 말고
   Improvement 를 `[조건 ID] 측정-판별력-미기재 — {지목해야 할 구현 지점}` 으로 기록한다
3. **실행 음성 대조 (선택 · 안전 조건 3 개를 모두 만족할 때만)** —
   - (a) 대상 파일이 `git status --porcelain` 기준 **clean** 하다 (미커밋 변경을 파괴하지 않는다)
   - (b) 변형 지점이 **1~2 개**이고 이번 스프린트 **diff 범위 안**이다
   - (c) 실행 후 `git diff --exit-code -- <대상 파일>` 로 **원상 복구를 확인**한다

   하나라도 불충족이면 **실행하지 말고** 근거에 `discrimination: static-only` 를 남긴다.
   원본 작업트리를 변형한 채 남기는 것은 평가자가 평가 대상을 오염시키는 행위다.

**판정:**

- 결합 0 (독립 재작성) → 조건 **FAIL** + Improvement `측정-판별력-부재`
- 실행 음성 대조에서 구현을 무력화했는데도 측정이 **통과** → 그 측정은 oracle 이 아니다 →
  조건 **FAIL** + Improvement `측정-판별력-부재`
- 무력화 시 측정이 **FAIL** → 판별력 확인 → 원 판정 유지. 근거에 `음성 대조: {지점} 무력화 시 FAIL 확인`

### 비용 통제 (반드시 지켜라)

mutation 은 비싸다. 대규모 적용 보고는 전통적 방식이 큰 코드베이스에 맞지 않는다고 보고,
**changed code 만 · irrelevant mutant 필터링 · line 당 제한 · operator history 기반 선택**으로
줄여서 24,000+ developers / 1,000+ projects 규모에 적용했다
([Google](https://research.google/pubs/practical-mutation-testing-at-scale-a-view-from-google/)).
본 절의 "diff 범위 안 · 1~2 지점" 제한이 그 축소 규칙의 평가자 판이다.

판별력 요구 자체의 근거는 mutant detection 과 real fault detection 사이의 상관이다 — 5 개 OSS ·
321K LOC · **357 real faults** 에서 통계적으로 유의했고 **code coverage 와 독립적으로도** 성립했다
([Just et al. FSE 2014](https://homes.cs.washington.edu/~mernst/pubs/mutation-effectiveness-fse2014-abstract.html)).
장기 연구(**1,500만 mutants**)에서도 실제 결함을 유발한 변경에서 live mutant 가 보고돼 버그를 막을
수 있었다는 evidence 가 있다
([Google](https://research.google/pubs/long-term-effects-of-mutation-testing/)).

### rubric 측 대응 — 판별력 없는 서브체크는 더 쪼갠다

같은 문제가 rubric 레벨에도 있다. 많은 응답에 동시에 만족되는 rubric 항목은 **판별력이 낮아 더
세분화**해야 한다 ([arxiv 2602.05125](https://arxiv.org/html/2602.05125v1/)). 서브체크가 어떤
구현에서도 통과한다면 그것은 §Rubric 기반 분해 의 재귀 분해 신호다.

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
- 미검증 대상은 `[미검증:INVALID]` 로 집계된다 — 시간 제약은 도구·환경 부재가 아니라 "검사되지 않음" 이므로 `ENV` 가 아니다 (상기 카운팅 로직 적용)
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

### 안티패턴 스택 정합성 (Stack Applicability)

> **배경:** digest `stack-inappropriate-rust-antipatterns` — 셸/compose 작업 계약에 Rust 전용
> 조건(`unwrap()`, `println!`)이 그대로 들어갔고 평가자가 그대로 판정했다. 계약 생성 측 결함이지만
> 평가자도 걸러낼 수 있다.

`project.yaml` 의 `anti_patterns` 나 계약의 안티패턴 조건을 Grep 하기 전에 **패턴의 스택과 대상
파일의 스택이 일치하는지** 확인한다:

- 불일치하면 그 패턴은 `N/A (스택 불일치: 패턴=Rust · 대상=shell/yaml)` 로 기록한다.
  **매치 0 건을 PASS 로 적지 마라** — 애초에 매치될 수 없는 패턴의 0 은 공허한 0 이다
  (§Evidence Validity Gate 검사 2·3)
- 동시에 Sprint Feedback 에 "계약 결함: 대상 스택에 부적합한 안티패턴 조건" 을 기록한다.
  조건 삭제·교체는 사용자 권한이므로 평가자는 권장만 한다
- 대상 파일이 여러 스택에 걸쳐 있으면 스택별로 나누어 판정하고 각각의 대상 파일 수를 기록한다

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
- **Swap Test 불안정 강등 규칙**: 동일 조건을 `(A, B)` 와 `(B, A)` 순서로 평가했을 때 PASS/FAIL 이 다르면 자동으로 `[low-confidence]` 로 강등한다. 2 회 재검증해도 일치하지 않으면 `[미검증:INVALID]` 로 처리하고 Sprint Feedback 에 position bias 의심 명시

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

### Recurring Improvement Escalation — 같은 제안을 반복하면 그것은 권고가 아니라 결함이다

> **배경:** 글로벌 evaluator 피드백 240 건의 improvement suggestion 을 집계하면 **같은 제안이
> 여러 스프린트에 걸쳐 반복**된다. 예: "AR-01/AR-02 는 unstaged working tree 에서 측정이
> 모호 — `git diff --cached` 기준 권고" (3 회 이상), "`[exact]` 조건에 widget test 를 명시하면
> 구현과 함께 테스트도 제출해야 함", "DG-02 IDE diagnostics 는 analyze 와 실질 중복". 매번 산문
> 권고로만 남기면 아무도 처리하지 않고 다음 사이클에 같은 문장이 다시 생성된다.

**규칙:**

1. 개선 제안을 쓸 때 **대상 조건 ID + 결함 유형**을 함께 적는다 (자유 산문 금지).
   유형 예: `측정-상태-모호` · `태그-산출물-불일치` · `측정-중복` · `범위-미명시` · `증거-경로-부재`
2. 같은 프로젝트에서 **같은 유형의 제안이 2 회째**면 그것은 권고가 아니라 **계약 결함**이다.
   Sprint Feedback 의 `contract_ambiguity_notes` 로 승격하고 REJECT 사유 후보에 올린다
3. **3 회째면 조건 자체를 신뢰하지 않는다.** 해당 조건은 `[low-confidence]` 로 강등하고,
   "이 조건은 현 형태로 반복 판정 불가 — 계약 수정 없이는 다음 iteration 도 같은 결과" 를
   피드백 최상단에 명시한다
4. 평가자는 계약을 **직접 수정하지 않는다** (사용자 권한). 대신 제안을 구체 대체 문구로 적는다 —
   "모호하다" 가 아니라 "`Given: 스테이징 완료 후` 를 붙이고 `--cached` 를 쓸 것"

> 이 승급 사다리는 one-time rubric refinement 패턴([arxiv 2511.10865](https://arxiv.org/abs/2511.10865))
> 의 운영 형태다. 반복 관측 자체를 신호로 쓰면 rubric 개선이 사람의 기억에 의존하지 않는다.

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

- [GroundEval: A Deterministic Replacement for LLM-as-Judge in Stateful Agent Evaluation — arxiv 2606.22737](https://arxiv.org/html/2606.22737v2) — 판정자는 validity 가 아니라 plausibility 를 채점한다. 근거를 가져오지 않은 답변에 0.90/0.85 vs trace 대조 0.000. invalid absence / temporal leakage / permission leakage 분류 (§Evidence Validity Gate 근거)
- [Beyond Task Completion: Revealing Corrupt Success in LLM Agents through Procedure-Aware Evaluation — arxiv 2603.03116](https://arxiv.org/pdf/2603.03116) — outcome-only 평가는 절차 위반을 통과시켜 성능을 과대평가. 중간 상태·행위 시퀀스 대조 필요 (§Evidence Validity Gate 근거)
- [Closing the Loop on LLM-Generated RTL Assertions with Quality-Aware Formal Verification — arxiv 2606.21451](https://arxiv.org/pdf/2606.21451) — vacuity: trigger coverage · antecedent activation · mutation(negative control) 3 축으로 "통과했지만 아무것도 검사하지 않은" 검증 걸러내기 (§Evidence Validity Gate 5 검사 중 1~3 근거)
- [From Confident Closing to Silent Failure — arxiv 2606.09863](https://arxiv.org/abs/2606.09863) — 실패의 75.8% 가 false success, LLM 판정자 AUROC 0.54~0.65 (§Canonical Unverified-Evidence Protocol 4 항 근거 · Phase 1 §3.7 공유 출처)
- [Gaming the Judge: Unfaithful Chain-of-Thought Can Undermine Agent Evaluation — arxiv 2601.14691](https://arxiv.org/abs/2601.14691) — narrated reasoning 조작 시 false positive 최대 90% 증가, observable evidence 에 대해 reasoning claim 검증 필요 (§Execution-Grounded Evidence 근거)
- [Tool Receipts, Not Zero-Knowledge Proofs: Practical Hallucination Detection for AI Agents — arxiv 2603.10060](https://arxiv.org/pdf/2603.10060) — 실행 로그(receipt) 대조로 fabricated tool reference 탐지 (§Execution-Grounded Evidence 근거)

- [Judging the Judges: A Systematic Study of Position Bias in LLM-as-a-Judge — arxiv 2406.07791](https://arxiv.org/abs/2406.07791) (IJCNLP 2025) — Swap Test 표준화
- [Am I More Pointwise or Pairwise? Revealing Position Bias in Rubric-Based LLM-as-a-Judge — arxiv 2602.02219](https://arxiv.org/html/2602.02219) — rubric 기반 판정에서도 position bias 발생
- [Self-Preference Bias in LLM-as-a-Judge — arxiv 2410.21819](https://arxiv.org/abs/2410.21819) — perplexity 기반 familiarity, 컨텍스트 분리 근거
- [Justice or Prejudice? Quantifying Biases in LLM-as-a-Judge — arxiv 2410.02736](https://arxiv.org/html/2410.02736v1) — 12 개 편향 분류
- [Evaluating Scoring Bias in LLM-as-a-Judge — arxiv 2506.22316](https://arxiv.org/html/2506.22316v1) — score rubric order / score IDs / reference answer score 3 종 scoring bias 를 정의하고 채점 프롬프트 섭동이 judge robustness 를 흔든다는 것을 측정한다. **이 논문을 이진 채점의 근거로 인용하지 마라** — 원문은 그런 주장을 하지 않는다 (2026-08-13 정정). 이진 채점의 근거는 아래 CheckEval 이다
- [An Empirical Study of LLM-as-a-Judge: How Design Choices Impact Evaluation Reliability — arxiv 2506.13639](https://arxiv.org/html/2506.13639v1) — CoT minimal gain when rubric well-defined
- [Rethinking Rubric Generation for Improving LLM Judge and Reward Modeling — arxiv 2602.05125](https://arxiv.org/html/2602.05125v1/) — Recursive Rubric Decomposition (RRD)
- [A Survey on LLM-as-a-Judge — arxiv 2411.15594](https://arxiv.org/html/2411.15594v6) — 종합 bias 분류
- [Towards a Human-in-the-Loop Framework for Reliable Patch Evaluation — arxiv 2511.10865](https://arxiv.org/abs/2511.10865) — one-time rubric refinement 패턴

기존 참조 (Phase 1 이전):

- [Understanding LLM-Driven Test Oracle Generation — arxiv 2601.05542](https://arxiv.org/abs/2601.05542) — 구현 추종 편향, specification-first
- [A Statistical Approach to Model Evaluations — Anthropic](https://www.anthropic.com/research/statistical-approach-to-model-evals) — 판정 확신도
- [CheckEval — arxiv 2403.18771](https://arxiv.org/abs/2403.18771) — boolean 서브체크 분해. Likert scale + 주관적 기준이 inconsistency 를 만들고 **decomposed binary questions 로 evaluator agreement 를 평균 0.45 개선**. 본 가이드의 이진 PASS/FAIL 원칙과 서브체크 분해의 **직접 근거**다
- [CodeBERTScore — arxiv 2302.05527](https://arxiv.org/abs/2302.05527) — 코드 유사도 메트릭 (본 가이드는 계약 기반 검증이 우선이므로 보조 참고용으로만 언급)

공식 문서:

- [Claude Code — Plugins reference](https://code.claude.com/docs/en/plugins-reference) — `${CLAUDE_PLUGIN_ROOT}` 는 플러그인 설치 디렉토리의 절대경로이며 **skill/agent 본문 어디에서나 치환**된다. 플러그인 업데이트 시 경로가 바뀌므로 그 아래에 상태를 쓰지 않는다 (§피드백 저장 경로 해석 근거)

관련 스키마:

- `harness/references/contract-schema.md` — Sprint Contract v5.3 스키마 (허용 섹션 헤더 2 계층 + `CONTRACT_ROOT` + **계약 봉인** + **Amendment `direction` × `consent`** + Counterpart 조건 패턴 + Diff-Scope Oracle 표준형 + **측정 커버리지 표기** + **인자 매트릭스** + **음성 대조** + specificity tag + aggregation mode + `[미검증]` 마커 + sibling enumerated)
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

### Parity Table (8 개 parity item — 행 수는 계산값이다. 손으로 세지 마라)

| # | Parity Item | skill-design-guide | agent-design-guide | contract-design-guide | **qa-evaluation-guide (이 가이드)** |
| --- | ------------- | ------------------- | ------------------- | ---------------------- | ------------------------------------- |
| 1 | Binary Decidability | §3.5 (계약 모호성 방지) | §3.5 (Pre-Check) | §Binary Decidability | **§Binary Decidability Pre-Check** |
| 2 | Rule-by-Rule Audit | §3.6 | §10 (reviewer audit) | — (평가 위임) | **§Rule-by-Rule Audit Before Completion** |
| 3 | Unverifiable / `[미검증]` 정책 | §3.7 (생성 측 짝) | §10 Unverifiable (4 항) | §미검증 마커 (도구 부재 전용) | **§`[미검증]` 마커 평가 프로토콜 + §증거 분류 triage (4 분기 · 카운터 분리) + §Canonical Unverified-Evidence Protocol** |
| 4 | Sibling Consistency | §8.8 | §3 (sibling agent) | §Sibling Consistency | **§Sibling Enumerated Verification** |
| 5 | Execution-Grounded Evidence / Completion Evidence Gate | §3.7 (2026-07 착지) | §10 4 항 | §증거 아티팩트 존재 의무 | **§Execution-Grounded Evidence + §Evidence Validity Gate** |
| 11 | Enforcement 등급 (E1/E2/E3) | §3.7 (정의 · 승급 규칙 — **SSOT**) | §6 패턴 7 (훅 = E3 게이트) | §원칙별 Enforcement 등급 | **§원칙별 Enforcement 등급 (평가자 원칙 현재 등급표)** |
| 12 | Counterpart Enumeration | §5.5 (편집 전 양면 열거) | — | §양면 조건 — Counterpart Conditions | **대응 절 없음 (의도된 설계 — 아래 참조)** |
| 14 | User-Reported Failure Gate | §3.8 (사용자 관측은 재현 대상) | §10 (사용자 보고 우선 — `REOPENED`) | 계약 측 착지 없음 (평가 레이어 소관) | **§Canonical User-Reported Failure Protocol** |

> **item 14 — 2026-08 사이클 신규.** 계약 측에는 착지가 없다 (contract-design-guide 가 명시:
> `REOPENED` 는 완료 판정 시점의 상태 전이라 계약 작성 시점에 대응 아티팩트가 없어 §증거 아티팩트
> 존재 의무와 충돌한다). 따라서 **정본이 이 가이드에 있고** 각 kit reviewer 가 복제한다.
> 상태어 `REOPENED` · 6 축 · 완료 해제 3 택의 어휘를 바꾸면 parity 가 깨진다.
>
> **item 12 — 평가자 대응 절을 만들지 않는다.** 평가자는 계약에 박힌 Counterpart 조건을
> **일반 조건으로 판정**하면 된다. 별도 평가 규칙을 두면 계약에 없는 요구를 평가자가 만들어내게
> 된다 (contract-design-guide §Cross-Surface Parity item 12 의 설계 결정). 후속 카이젠 Phase 가
> 이 절을 "누락" 으로 오인하고 추가하지 않도록 여기에 명문화한다.
>
> **item 11 — 등급 어휘는 skill-design-guide §3.7 이 SSOT.** 본 가이드는 평가자 원칙의 현재
> 등급 목록만 유지하며 등급을 재정의하거나 동의어를 만들지 않는다.
>
> **item 5 — 2026-07 사이클에서 양면(생성/평가) 으로 전환.** 생성 측이 `[미검증]` 을 표기하지
> 않으면 평가 시점에야 드러나 iteration 이 낭비된다. 마커 표기법과 **2 건 임계**는 양쪽이 동일
> 규약을 쓴다.

### 개정 시 체크리스트

qa-evaluation-guide.md 편집 시:

- [ ] 새 평가 원칙을 추가했는가? → 상위 skill/agent/contract 가이드에 원천 원칙이 있는지 Grep 확인
- [ ] 원칙 네이밍 (섹션명, 용어) 을 변경했는가? → qa-evaluator.md · contract-schema.md 에서 동일 네이밍 사용 중인지 Grep 하여 동기화
- [ ] 실패 사례를 추가했는가? → 해당 REJECT 가 발생한 프로젝트의 feedback YAML 에 연결 링크 포함
- [ ] parity table 의 컬럼을 추가/삭제했는가? → 상위 3 개 가이드의 parity table 도 동일하게 갱신
- [ ] §Canonical Unverified-Evidence Protocol 또는 §Canonical User-Reported Failure Protocol 을 수정했는가? → `*-kit/agents/*-reviewer.md` 6 종이 복제 중이므로 각 kit 카이젠 Phase 에 전파 지시를 남긴다 (여기서 직접 수정하지 않는다 — 각 kit Phase 소관)
- [ ] 새 원칙에 Enforcement 등급을 부여했는가? → §원칙별 Enforcement 등급 표에 행 추가. 등급 정의는 skill-design-guide §3.7 을 인용만 한다

### 실패 사례 (이 원칙 없이 발생)

- **PH-01 (design-kit, 2026-04)**: skill-design-guide §3.5 가 agent-design-guide 와 qa-evaluation-guide 에 전수되지 않아 평가자가 모호 조건을 그대로 평가 → REJECT
- **SK-13 (backend-kit/infra-kit)**: 상위 가이드 원칙이 하위 스킬 SKILL.md 로 전수되지 않은 meta-gap

### 버전 정보

- **Guide version**: 2026-08-13 (Phase 3 kaizen · v5.0 — **미검증 카운터 분리**(`UNVERIFIED_ENV` / `UNVERIFIED_INVALID_EVIDENCE` · 남용 방지 4 요건 · 검증 커버리지 게이트 · 연속 ENV 승급) · **§Discriminating Evidence Gate** · **§Canonical User-Reported Failure Protocol** · **§계약 봉인 검증** · Amendment `direction × consent` 2 축 · scoring bias 출처 정정)
- 이전: 2026-07-28 (병렬 스프린트 안전성 · v4.3 — 계약 선택 ladder 5 단계 + 3.5 레거시 브릿지 · CONTRACT_ROOT 는 먼저 만나는 `.harness` 에서 멈춤 + `contract_root_unconfigured` 경고 · ladder 1 `test -f` 존재 검사 + 부재/모호 BLOCKED 사유 분리 · 계약 `status` 수명주기 · 계약 지문 TOCTOU · Amendment 소비 규칙 · User Correction Audit · Evidence Validity 검사 5 실행가능성)
- 이전: 2026-07-27 (Phase 3 kaizen · v4.0 — Evidence Validity Gate · 증거 분류 triage · 계약 파싱 범위 · Canonical Unverified-Evidence Protocol · Recurring Improvement Escalation · 원칙별 Enforcement 등급)
- **Parity with**: skill-design-guide v1.5.0, agent-design-guide v1.6.0, contract-design-guide v5.0
- **Schema link**: contract-schema.md v5.3 §산출물 경로 · §계약 봉인 · §Amendment 사이드카 (경로·슬러그·frontmatter·봉인·amendment 축 SSOT — 본 가이드는 인용만 한다)
- **하위 전파 대기**: `*-kit/agents/*-reviewer.md` 6 종 (design · backend · infra · rust · react · planning) — §Canonical Unverified-Evidence Protocol (2026-08 개정분 포함) + §Canonical User-Reported Failure Protocol 복제. 각 kit 카이젠 Phase 소관이며 본 Phase 는 수정하지 않았다
