---
feature: "카이젠 2026-09-24 Phase 11 계약 — 폐기한 결정을 PRD 비범위 절 한 곳에 · 뒤 단계가 되살리지 않게 · Mermaid 12 현행화"
slug: kaizen-0924-p11-planning-kit
created: "2026-09-25 08:39"
complexity: "복잡"
conditions: 28
status: active
owner_session: de8c7935-a5b6-4df5-9106-fafa73c288a0
conditions_digest: sha256:4a38762119ffd6a8
locked_at: "2026-09-25 09:13"
---

## 배경

이 Phase 의 외부 근거는 `.harness/.meta/evidence/phase11.md` 하나다. 처리 배정표(`.claude/kaizen-input/insights-report.md`)에서 `배정` 칸이
`Phase 11` 인 행은 `F20` 과 `backend-family:P1` 둘이다. 적용 힌트는 「폐기한 결정을 제품 요구 문서(PRD)에 남기되, 기록 자리를 하나로 정한 뒤에 넣는다」 다.
러닝북 `Phase 별 추가 과제` 에 Phase 11 줄은 없다. 앞 Phase notes 가 Phase 11 로 넘긴 줄은 셋이다(Phase 4 · 6 · 7). 오케스트레이터 Step 11 은 「Phase 1 에서
설계 가이드가 변경되었으면 planning-kit 전 스킬을 전수 감사한다」 고 적는다 — 그 감사 결과는 `GAP 분석` 절 끝 표에 있다.

| 키 · 출처 | 내용 | 이번 처리 |
| --- | --- | --- |
| `F20` | 이미 폐기한 시간대 · 국가 항목을 되살림, 한 나라 우선으로 거듭 판단. 비고: 폐기 결정 기록 자리가 design:P5 · backend-family:P1 · user-setup:P2 · user-setup:P6 네 곳 — 하나로 정한다 | 반영 — 결정 1 (기록 자리) · SK-01 · SK-02. 「한 나라 우선 판단」 은 처리 배정표가 user-setup:P10(킷 밖)으로, 시간대를 설정값으로 다루는 일은 backend-family:P2(Phase 7)로 보냈다 — 이 Phase 몫이 아니다. notes 미반영 절에 적는다(ER-03) |
| `backend-family:P1` | plan-prd 에 폐기 결정 Non-goals 세 칸 (무엇 · 왜 · 남은 흔적) | 반영 — SK-02 ~ SK-08. 칸은 넷으로 한다(결정 2) |
| `phase4-notes.md` 넘김 표 | 「`F20` — 폐기 결정 기록 자리를 하나로 정한 뒤 `/sprint` 재검증 블록에 그 자리를 읽는 줄을 둔다」 | 자리는 이 Phase 가 정한다(결정 1). `/sprint` 는 harness 파일이라 이 Phase 범위 밖 — 다음 사이클 Phase 4 로 넘긴다(ER-03) |
| `phase6-notes.md` 넘김 표 · 결정 3 | 「제품 수준 폐기 결정 자리는 Phase 11 이 정한다. 정해지면 design-kit 승인 기록 폐기 칸이 그 경로를 적는다(규약 §4 규칙 둘째 줄)」 | 규약 §4 는 이미 「결정이 적힌 파일 경로를 폐기 칸에 적는다」 로 되어 있다. 그 경로가 PRD 비범위 절이 된다 — design-kit 은 고치지 않고, 그 문장이 그대로인지 AR-02 가 잰다 |
| `phase7-notes.md` 넘김 표 | 「`F20` — 폐기 결정 기록 자리를 하나로 정한다」 | 결정 1 |
| 근거 파일 §3 현행화 | Mermaid 최신 안정판 12.0.0 · ERD 기본 배치 Dagre → ELK · GitHub 문서 버전 날짜 `2026-03-10` · gh 2.101.0 · Cucumber | Mermaid 둘은 반영(SK-09). GitHub 날짜는 미반영 — 옛 호출이 깨지는 변경이 있고 킷은 문서 링크에만 날짜를 쓴다(근거 파일 §3 「날짜만 기계적으로 교체해서는 안 된다」). gh · Cucumber 는 바뀐 것이 없다. 근거 파일 §3 셋째 행이 함께 짚은 `plan-data-model/SKILL.md:24`(Gotcha 8, Mermaid 버전 적지 않음)는 고치지 않는다 — 그 스킬 Step 0 이 `data-modeling.md` 를 읽으니 버전 사실은 문서 한 곳에 둔다 |

사고 경위(데이터 풀 §0-b `9a0d4163`, 2026-09-14): 「Claude re-introduced previously-discarded timezone/country settings ('내가 분명히 폐기처리햇는데')」.
그 프로젝트에는 `.planning/` 이 없다(`ls` 로 확인 — 앱 이름은 킷 파일에 넣지 않는다). 그래서 이 Phase 의 변경은 planning-kit 으로 기획하는 프로젝트에서 같은 사고를
막는다. PRD 가 없는 프로젝트의 기록 자리는 이 결정이 답하지 않는다 — `/sprint` 재검증 줄과 함께 다음 사이클 Phase 4 로 넘긴다.

관심사는 둘이다 — (1) 폐기한 결정의 기록 자리와 뒤 단계 확인(SK-01 ~ SK-08, 한 관심사 안의 형제 대칭) (2) Mermaid 12 현행화(SK-09). research-log(SK-10)는 둘을 기록한다.
planning-kaizen Gotcha 4 는 「1-2개씩 개선」 이라고 하는데, 고치는 킷 파일은 여섯이라 그 수를 넘는다. 뒤 단계 셋과 감사 둘은 규칙 본문 없이 한두 줄만 더하고(RE-02),
근거 파일 §2 가 감사 두 파일을 함께 바꾸라고 해서 나누지 않았다. 글로벌 평가 피드백(`~/.harness/feedback/evaluator/`)에서 planning-kit 을 문제로 가리킨 기록은 0 건이다
(`grep -rl 'planning-kit\|plan-prd\|plan-audit'` 로 찾은 넷은 모두 다른 계약의 교차 진단 문장에 킷 이름이 나온 것이다).

## 리서치 소스

외부 조회 0 회. 아래 URL 은 전부 근거 파일 `.harness/.meta/evidence/phase11.md` 에서 가져왔다. Context7 은 이 세션에서 인증되지 않아 쓰지 않았다 — 라이브러리 코드를 쓰지 않는다.

- [Basecamp Shape Up §Chapter 6](https://basecamp.com/shapeup/1.5-chapter-06) — pitch 다섯 요소 가운데 No-gos. 「appetite 에 맞추거나 문제를 다루기 쉽게 하려고 일부러 뺀 기능 또는 사용 사례」 — 하지 않는 것 · 이유 칸의 근거 (SK-01 · SK-02)
- [Agile Alliance — INVEST](https://agilealliance.org/glossary/invest/) — Negotiable 은 특정 기능의 고정 계약이 아니다 — 폐기를 영구 금지로 넓히지 않고 「먼저 묻는다」 로 두는 근거 (SK-01 · SK-02 · SK-04)
- [GitHub — Best practices for Projects](https://docs.github.com/issues/planning-and-tracking-with-projects/learning-about-projects/best-practices-for-projects) — 정보를 여러 필드에 겹쳐 두지 말고 한 곳을 기준으로. 예는 출시 목표일 — 폐기 결정에 옮긴 것은 추론이라고 적는다 (SK-01)
- [Mermaid — Entity Relationship Diagram](https://mermaid.js.org/syntax/entityRelationshipDiagram.html) · [Mermaid 12.0.0 release](https://github.com/mermaid-js/mermaid/releases/tag/mermaid%4012.0.0) — 12.0.0 (2026-09-10), ERD 기본 배치 Dagre → ELK · 기본 모양 변경. 논리 모델에서는 FK(다른 표를 가리키는 열) 속성을 빼도 된다 — 코드 · 데이터베이스 흔적을 개념 모델에 그대로 옮기지 않는 근거 (SK-05 · SK-09)
- [GitHub — REST API Versions](https://docs.github.com/en/rest/about-the-rest-api/api-versions) · [Breaking Changes](https://docs.github.com/en/rest/about-the-rest-api/breaking-changes) — 버전 날짜 `2022-11-28` 은 2028-03-10 까지 지원, 최신 `2026-03-10` 에는 옛 호출이 깨지는 변경 (SK-09 `sync_same` · SK-10)
- [GitHub CLI 2.101.0](https://github.com/cli/cli/releases/tag/v2.101.0) · [Cucumber Gherkin Reference](https://cucumber.io/docs/gherkin/reference) — 무변경 확인 (SK-10)

근거 파일이 스스로 밝힌 한계를 그대로 옮긴다(§5). `무엇 · 왜 · 코드에 남은 흔적` 세 칸을 요구하는 공식 기획 방법론은 없다. 흔적을 「되살릴 근거가 아닌 정리 목록」 으로
나누는 1 차 출처도 없다. 「Non-goals 3 개 이상」 은 Shape Up 규칙이 아니라 이 킷의 기준이다. PRD 와 별도 결정 기록(ADR) 가운데 어디가 나은지 비교한 자료는 조회하지 않았다.
Mermaid 12 에서 기존 예시가 실제로 렌더되는지는 실행 검증하지 않았다 — 로컬에 Mermaid 가 없다(`command -v mmdc` 없음, 스크래치 `node_modules` 에 `mermaid` 없음).
그래서 새 문장은 흔적 칸과 「치울 목록」 을 **이 킷의 운영 규칙**이라고 밝히고(SK-01 · SK-02), 12 에서 렌더해 보지 않았다고 적는다(SK-09).

내부 입력: 데이터 풀 §0 처리 배정표 · §0-b `9a0d4163` · §0.5 [planning] 두 건(`feedback-brainstorm-one-question` 은 `user_correction` 이나 이번 두 키와 무관, 나머지 하나는
`미분류` 라 배경으로만 읽었다) · §1 글로벌 평가 피드백(위 배경).

## GAP 분석 · 개선안 초안

### 1.1 복잡도 4 축

| 축 | 물음 | 값 |
| -- | ---- | -- |
| 레이어 수 | 몇 개 계층을 관통하는가 | 3 — 원칙 문서(`docs/planning/`) · 만드는 스킬 넷(plan-prd · plan-stories · plan-data-model · plan-flow) · 감사 스킬과 평가 에이전트(plan-audit · planning-reviewer) |
| 공개 API·계약 변경 | 외부에 노출된 형태가 바뀌는가 | 예 — PRD 산출물(`.planning/prd-<slug>.md`)의 비범위 절이 네 칸 표가 된다. 뒤 단계 스킬과 감사가 그 형태를 읽는다 |
| 소비면 존재 | 이 형태를 받아 쓰는 반대편이 있는가 | 예 — 아래 Counterpart 표 |
| 회귀 위험 | 기존 동작이 깨질 수 있는가 | 예 — plan-audit · planning-reviewer 의 12 카테고리 짝(planning-kaizen Gotcha 7 · 9), 문구를 바꾸면 안 되는 미검증 기준 원본 사본(Gotcha 7), Step 0 은 로드만 한다는 규칙(Gotcha 8) |

네 축이 모두 「예」 이고 공개 형태 변경과 소비면이 둘 다 「예」 라 **복잡**이다. Step 2.5 Counterpart 조건을 넣는다(SK-04 ~ SK-08 · AR-02).
기능 조건은 18 개다 — 복잡 9 ~ 20 안이다(sprint-contract Step 6.2 둘째 명령으로 이 파일을 세면 18).

### 1.2 설정 리터럴 대조표

| config key | project.yaml 에서 읽은 값 | 계약에 쓴 값 |
| ---------- | ------------------------- | ------------ |
| `commands.analyze` | `bash -n scripts/release.sh` | DG-01 N/A 사유에 그대로 |
| `commands.test` | `bash scripts/release.sh 2>&1 \|\| true` | DG-03 N/A 사유에 그대로 |
| `diagnostics.ide_exclude` | `[]` | DG-02 에 그대로 |
| `contract_categories[].id` / `prefix` | `Skill`/`SK` · `Script`/`SC` · `Error`/`ER` · `Architecture`/`AR` | 조건 절 제목과 접두 그대로 |
| `anti_patterns[].id` / `message` | AP-01 · AP-02 · AP-03 · AP-04 | AP-01 · AP-03 · AP-04 를 고르고 message 원문 그대로. AP-02(force push)는 이 Phase 가 밀어 넣지 않아 뺀다 |

### 1.4 편집 전 감사 (실제로 읽은 줄 — 시작 커밋 `d88c35a` 판)

| 대상 파일 | 실제 Read 증거 (`파일:라인`) | 발견한 기존 갭·위반 | 계약 조건화 |
| --------- | ---------------------------- | ------------------- | ----------- |
| `planning-kit/skills/plan-prd/SKILL.md` | `:13-27` (Gotcha 1 ~ 13, `:19` Gotcha 5 「최소 3개의 non-goal 필수」) · `:31-39` (Step 0) · `:50-55` (Step 2 표 — PR/FAQ `:52` · Linear `:54` 산출물 구조에 Non-goals 없음) · `:59-85` (PR/FAQ 틀 — 비범위 절 없음) · `:87-110` (Shape Up 틀 `:108-109` `## No-gos` / `- (명시적 제외)`) · `:112-122` (Linear 틀 — 비범위 절 없음) · `:124-134` (Step 4 `:130` 「Non-goals 가 3개 이상인가」) | 폐기한 결정을 적을 칸 0 건. Gotcha 5 · Step 4 는 모든 형식에 Non-goals 3 개를 요구하는데 PR/FAQ · Linear 틀에 그 절이 없다(근거 파일 §2 (2) 「내부 불일치」) | SK-02 · SK-03 |
| `planning-kit/skills/plan-stories/SKILL.md` | `:31-39` (Step 0 — `:36` PRD 로드) · `:41-45` (Step 1) | PRD 를 읽지만 비범위 절과 겹치는지 보는 줄 0 건 | SK-04 |
| `planning-kit/skills/plan-data-model/SKILL.md` | `:33-35` (Step 0 — 원칙 문서만) · `:37-47` (Step 1 Event Storming) · `:163-171` (Step 7) | PRD 를 읽지 않는다. 폐기한 필드가 모델에 다시 들어가도 막는 줄 0 건 | SK-05 |
| `planning-kit/skills/plan-flow/SKILL.md` | `:29-31` (Step 0 — 원칙 문서만) · `:43-45` (Step 2 머리) | PRD 를 읽지 않는다 | SK-06 |
| `planning-kit/skills/plan-audit/SKILL.md` | `:21` (Gotcha 6 · 12 카테고리) · `:24` (Gotcha 9 · 미검증) · `:64-79` (Step 3 표 — `:72` 카테고리 3 「최소 3개 명시」 뿐) · `:119-135` (Step 5) | 폐기한 결정의 칸과 뒤 단계 재등장을 보지 않는다 | SK-07 · AR-03 |
| `planning-kit/agents/planning-reviewer.md` | `:22-48` (미검증 기준 원본 사본) · `:56-60` (Step 2 · 공허한 증거 분기) · `:84-99` (원칙 매핑 — `:92` Non-goals 행) · `:127-158` (사용자 보고 사본 — `:151` 이 이 파일에 없는 「4 요건」 을 가리킨다) · `:160-170` (Gotcha) | Non-goals 는 출처 매핑만 있고 뒤 단계 재등장을 검사하지 않는다. `:151` 의 빈 가리킴과 기준 원본 사본이 2026-08-13 개정 전 판인 것은 판정 규칙 변경이라 이번 범위 밖(ER-03 넘김) | SK-08 · AR-03 |
| `docs/planning/prd-patterns.md` | `:1-6` (머리 설정 0.1.0) · `:10-13` (개요 — 범위/비범위 분리) · `:35-52` (Shape Up — No-gos) · `:107-123` (Design Sprint — 마지막 절) · `:125-139` (참고 링크) | 폐기한 결정 원칙 0 건. planning-kaizen Gotcha 2 가 원칙 문서 없는 스킬 개선을 막는다 | SK-01 |
| `docs/planning/flows.md` | `:1-6` · `:50-64` (`:53` 「공식 문법 10.x+ / 11.x 계열에서 유효한 형태다」) · `:154-161` | 버전 설명이 한 판 뒤처짐(근거 파일 §3). 2026-08-13 사이클이 근거 없는 Mermaid 버전 고정을 지웠는데 이 줄이 남았다 | SK-09 |
| `docs/planning/data-modeling.md` | `:1-6` · `:69-81` (erDiagram 절 · `:78` 한계/주의사항) · `:158-166` | Mermaid 12 의 ERD 배치 변경이 없다(근거 파일 §3) | SK-09 |
| `docs/planning/research-log.md` | `:1-9` (1.0.0 · 2026-08-13 · 첫 항목) · `:47-68` (2026-08-13 부수 정정 · 비범위) | 이번 항목 없음 | SK-10 |
| `planning-kit/skills/plan-sync-github/SKILL.md` | `:18` · `:171` (`?apiVersion=2022-11-28` 문서 링크) · `:33` (`gh --version` 확인) | 날짜가 한 판 뒤지만 2028-03-10 까지 지원되고 헤더로 보내지 않는다 — 고치지 않는다 | SK-09 (`sync_same`) |
| `design-kit/references/visual-change-protocol.md` | `:196-222` (§4 승인 기록 · 규칙 — `:221-222` 제품 요구 수준 폐기 결정은 경로만) | 없음 — Phase 6 결정 3. 읽기만 | AR-02 |
| `.claude/skills/planning-kaizen/SKILL.md` | Gotcha 1 ~ 9 · Step 1 ~ 6 | 레포 전용 파일이라 이 Phase 범위 밖. Gotcha 7 · 8 · 9 는 AR-03 이, Gotcha 5 는 DG-05 가 잰다 | AR-03 · DG-05 |

후보 옵션이 둘 이상이었던 곳:

- **기록 자리** — (가) PRD 비범위 절 (나) 별도 결정 기록 파일(`.planning/decisions.md` 같은 새 파일) (다) 기록 자리 넷을 그대로 두고 서로 가리키기. (가)를 고른다(결정 1).
  (나)는 새 파일 · 새 스킬 흐름이 필요하고 근거 파일이 PRD 와 결정 기록을 비교한 자료를 조회하지 않았다(§5). (다)는 원문이 여러 곳이라 한쪽만 고쳐진다(근거 파일 §2 GitHub 한 곳 기준)
- **뒤 단계 확인 자리** — Step 0 에 규칙까지 넣을지, Step 0 은 로드만 하고 규칙은 첫 작업 단계에 둘지. 뒤를 고른다 — planning-kaizen Gotcha 8 이 Step 0 에 작성 로직을 섞지 말라고 한다.
  plan-stories 는 Step 0 이 이미 PRD 를 읽어 Step 1 에만 한 줄을 더한다
- **감사 쪽** — plan-audit 만 고칠지, planning-reviewer 까지 고칠지. 둘 다 고친다 — 한쪽만 바꾸면 스킬과 평가자 판정 기준이 갈린다(근거 파일 §2 선택 사항 · planning-kaizen Gotcha 7).
  reviewer Gotcha 8(카테고리마다 따로 판정)과는 부딪히지 않는다 — 새 확인은 다른 카테고리의 판정 결과를 쓰지 않고 뒤 단계 산출물 파일을 읽을 뿐이다

### Counterpart — 바뀌는 형태를 받아 쓰는 반대편

| 면 | 파일 | 바뀌는 것 | 이번 처리 |
| --- | --- | --- | --- |
| producer | `docs/planning/prd-patterns.md` §폐기한 결정 | 원칙 — 기록 자리 · 네 칸 · 먼저 묻기 | SK-01 |
| producer | `planning-kit/skills/plan-prd/SKILL.md` | 세 틀의 비범위 표 · Gotcha 14 · Step 4 | SK-02 · SK-03 |
| consumer | `planning-kit/skills/plan-stories/SKILL.md` · `plan-data-model/SKILL.md` · `plan-flow/SKILL.md` | 비범위 절을 읽고 겹치면 만들기 전에 묻는다 | SK-04 · SK-05 · SK-06 |
| consumer | `planning-kit/skills/plan-audit/SKILL.md` · `planning-kit/agents/planning-reviewer.md` | 카테고리 3 판정 기준 | SK-07 · SK-08 — 같은 기준을 두 곳에 |
| consumer (Phase 6) | `design-kit/references/visual-change-protocol.md` §4 | 폐기 칸에 결정 경로만 적는다 | 고치지 않는다 — 그 문장이 그대로인지 AR-02 가 잰다 |
| consumer (다음 사이클) | `harness/skills/sprint/SKILL.md` | 재검증 블록이 PRD 비범위 절 경로를 읽는 줄 · PRD 없는 프로젝트의 자리 | 명시적 미완 — ER-03 넘김 (Phase 4 범위) |
| consumer (Final) | `docs/planning-kit/prd-patterns.html` · `flows.html` · `data-modeling.html` | 새 절 · 현행화 문장이 없다 | 명시적 미완 — Final F2 재생성(ER-03 넘김) |
| 소비자 없음 | `planning-kit/skills/plan-prioritize` · `plan-risks` · `plan-sync-github` · `plan-guide` · `plan-discover` · `plan-ideate` · `plan-reference` | 비범위 표를 읽지 않는다 — PRD 에서 새 요구를 만들어 내는 스킬이 아니거나(plan-guide 는 가벼운 피드백, plan-sync-github 는 스토리를 이슈로 옮기기만 한다), PRD 보다 앞 단계다 | 조건 없음 |

### 결정 둘

1. **폐기한 결정의 원문 자리 — 그 기능 PRD 의 비범위 절 한 곳.** PR/FAQ · Linear-style 은 `## Non-goals (폐기한 결정 포함)`, Shape Up 은 원문 용어 `## No-gos`. 후보 넷
   가운데 design:P5(design-kit 승인 기록)는 Phase 6 이 「경로만」 으로 이미 바꿨고, user-setup:P2(`/sprint`)는 다음 사이클 Phase 4 가 이 경로를 읽게 하고, user-setup:P6(핸드오프
   틀)은 킷 밖이라 카이젠 뒤 사용자 설정 목록에서 이 경로를 가리키게 한다. PRD 를 쓴 뒤에 나온 폐기 결정도 새 파일이 아니라 그 표에 한 줄 더한다.
   PRD 가 없는 프로젝트의 자리는 이 결정이 정하지 않는다 — Gotcha 1(Discovery 없이 PRD 금지)과 부딪혀 「폐기 기록만 담은 PRD」 를 만들게 할 수 없다
2. **칸은 넷 — 하지 않는 것 · 이유 · 범위 · 코드에 남은 흔적.** 처리 배정표 제안은 세 칸이다. 근거 파일 §4 권장 8 이 범위(`이번 PRD` · `이번 사이클` · `제품 전체`)를
   더하라고 한다 — Shape Up No-gos 는 그 pitch 와 appetite 안의 결정이고 INVEST Negotiable 은 영구 금지와 부딪힌다. 그래서 흔적과 겹치면 「되살리지 않는다」 가 아니라
   「되살리지 말고 먼저 묻는다」 로 쓴다(근거 파일 §2 「절대 되살리지 않는다까지 강화할 근거는 없다」)

### 개선안 초안

27 치환을 글자 그대로 적은 모의 스크립트가
`/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/de8c7935-a5b6-4df5-9106-fafa73c288a0/scratchpad/p11d/mock.py` 에 있다(sha256 앞 16 자리는 `회귀 게이트` 절).
옛 문자열이 정확히 한 번 있어야 바꾸고, 시작 커밋 판 새 사본에 돌리면 `mock applied 27` 을 낸다. BUILD 는 이 치환을 작업 폴더에 그대로 돌린다 — 조건이 문장을 글자 그대로 센다.
파일마다 요지:

1. `docs/planning/prd-patterns.md` — `### 폐기한 결정 — 비범위 절 한 곳에 적는다` 절(요약 · 근거 두 문단 · 체크 넷 · 적용 시점 · 한계 · 출처 셋)을 Design Sprint 절 뒤에, 참고 링크 둘, 머리 설정 0.2.0 · 2026-09-25
2. `planning-kit/skills/plan-prd/SKILL.md` — Gotcha 14, Step 2 표 PR/FAQ · Linear 두 행에 Non-goals, 세 틀에 같은 네 칸 표(Shape Up 은 `## No-gos` 제목 유지, 옛 `- (명시적 제외)` 대신), Step 4 두 항목
3. `planning-kit/skills/plan-stories/SKILL.md` — Step 1 한 줄
4. `planning-kit/skills/plan-data-model/SKILL.md` — Step 0 PRD 비범위 절 로드 한 줄(그리지 않는다), Step 1 규칙 한 줄(이벤트 나열 앞)
5. `planning-kit/skills/plan-flow/SKILL.md` — Step 0 로드 한 줄, Step 2 규칙 한 줄(User Flow 앞)
6. `planning-kit/skills/plan-audit/SKILL.md` — Step 3 카테고리 3 행
7. `planning-kit/agents/planning-reviewer.md` — 원칙 매핑 Non-goals 행, Step 3 끝 `### Non-goals 카테고리 — 폐기한 항목이 다시 들어갔는지`(같은 낱말이 PRD 표에도 걸려야 0 매치를 믿는다 — 공허한 증거 분기와 맞춤)
8. `docs/planning/flows.md` — 「10.x+ / 11.x 계열에서 유효」 → 12.0.0 사실과 렌더하지 않았다는 말(「최신 안정판」 은 시간이 지나면 틀리므로 근거 파일 `collected: 2026-09-24` 를 확인 날짜로 붙인다), 출처 · 참고 링크, 머리 설정 0.1.1
9. `docs/planning/data-modeling.md` — erDiagram 절 한계에 ERD 배치 Dagre → ELK · 모양 변경, 출처 · 참고 링크, 머리 설정 0.1.1
10. `docs/planning/research-log.md` — `## [2026-09-24] — Phase 11 kaizen (폐기한 결정 기록 자리)` 항목(결정 · 현행화 · 명시적 비범위), 머리 설정 1.1.0 · 2026-09-25

새 규칙의 강도: plan-prd Gotcha 14 에 enforcement 등급을 적지 않는다 — 같은 파일 다른 Gotcha 도 적지 않고, 강도를 올릴 재발 근거가 한 번(F20)뿐이다. 새 URL 은 전부 `<…>`
꼴로 적는다 — `docs/planning/` 은 원래 맨 URL 을 쓰지만 새 줄에 편집기 경고(MD034)를 더하지 않으려는 것이다(DG-02). 같은 이유로 새 절 제목 아래와 목록 앞에 빈 줄을 둔다.

### Phase 1 가이드 변경 셋 (오케스트레이터 Step 11 전수 감사)

| 가이드 변경 | 이 킷 | 자리 |
| --- | --- | --- |
| `[미검증]` 에 네 칸 (skill-design-guide §3.7 3 항 · agent-design-guide §10) | 해당 — 미반영 | planning-kit 의 `[미검증]` 은 전부 평가 쪽(plan-audit Gotcha 9 · Step 4 · Step 5, planning-reviewer)이고 기준 원본 사본을 따른다. 사본을 2026-08-13 개정 판으로 옮기는 일은 plan-audit 판정 규칙(READY · NEEDS_VERIFICATION 문턱)을 바꾼다 — 처리 배정표 밖의 별도 관심사라 Phase 6 이 design-kit 에서 같은 이유로 넘겼고, Phase 8 notes 가 일곱 킷 reviewer 를 다음 사이클 Phase 3 이 기준 원본을 먼저 정리한 뒤 같이 옮기라고 넘겼다(ER-03 넘김). Phase 9 는 Phase 1 넘김이 rust-reviewer 를 이름으로 짚어 옮겼다 — planning-reviewer 를 짚은 넘김은 없다. 만드는 쪽 스킬(plan-prd 등)에는 `[미검증]` 이 0 건 |
| 작업 자체를 못 한다고 결론 내리기 전 네 칸 (§3.7 5 조항 3 항) | 해당 없음 | `grep -rn '불가능하다고\|못 한다\|할 수 없다고\|불가 선언' planning-kit` 0 건. Step 0 의 「원칙 문서 없으면 `/planning-research` 권고 후 중단」 다섯 곳은 설계된 앞 조건 멈춤이고 다시 돌릴 명령을 적는다 |
| 0 이 아닌 값을 내는 새 측정 — 알려진 답 대조 (§3.7) | 해당 없음 | 이 킷 스킬은 값을 세는 측정 스크립트를 새로 만들지 않는다 |

## 범위 경계

- 이 Phase 시작 HEAD: `d88c35a70ccb88faf7bea3f57cf1f8c5f51b0279`. 범위 상한은 개정 파일 `.harness/sprint-amendments-kaizen-0924-p11-planning-kit.md` 의
  `end_sha:` 마지막 값이다. 여러 Phase 가 같은 가지 `kaizen/2026-09-24` 에 동시에 커밋하므로 `HEAD` 로 재지 않는다
- 고치는 파일은 열이다 — 아래 블록이 그 목록이다(`harness/README.md` §커밋 안전 훅 이 정한 범위 선언 자리). 새 파일은 없다. `.harness/` 쪽은 이 계약 · 개정 파일 ·
  QA 피드백 · `.harness/.meta/kaizen-0924/phase11-notes.md` · `.harness/.meta/kaizen-0924/phase11-review.md` 를 쓴다 — 슬러그를 나열하지 않고 AR-01 셋째 값 `verify_seal` 로 잰다.
  AR-01 다섯째 값이 이 블록과 측정 공통 정의의 `FILES` 가 같은지 잰다

```text
# sprint-scope
docs/planning/prd-patterns.md
docs/planning/flows.md
docs/planning/data-modeling.md
docs/planning/research-log.md
planning-kit/skills/plan-prd/SKILL.md
planning-kit/skills/plan-stories/SKILL.md
planning-kit/skills/plan-data-model/SKILL.md
planning-kit/skills/plan-flow/SKILL.md
planning-kit/skills/plan-audit/SKILL.md
planning-kit/agents/planning-reviewer.md
.harness/
```

- **이 Phase 의 커밋 메시지에는 전부 `Co-Authored-By` 줄 바로 위에 서명 줄 `Kaizen-Phase: kaizen-0924-p11-planning-kit` 한 줄을 넣는다** (봉인 커밋 포함).
  AR-01 · ER-03 · SC-00 · DG-01 · DG-03 · DG-04 · DG-06 이 이 줄로 이 Phase 커밋을 가린다(`harness/references/contract-schema.md` §여러 주체가 한 가지에 커밋할 때 선택지 B).
  서명을 빠뜨린 커밋은 서명 줄 목록에 안 보이므로 AR-01 첫째 값과 ER-03 마지막 값은 경로로 직접 센다.
  FIX 가 커밋을 더할 때도 넣고, 개정 파일에 `end_sha:` 줄을 덧붙인다(옛 줄은 지우지 않는다). notes 커밋도 이 Phase 커밋이다 — notes 를 커밋한 뒤 그 sha 로
  `end_sha:` 줄을 하나 더 덧붙여 커밋한다
- 구현 커밋은 `git add -- <파일…> && git commit -o -- <파일…>` 로 열 파일만 싣는다. `docs/planning/` 넷과 `planning-kit/` 여섯을 두 커밋으로 나눈다 —
  둘 다 이 킷 몫이라 `validate-post-kaizen.py` scope-isolation 에 걸리지 않는다(예행에서 두 커밋으로 확인)
- 측정이 기대는 제목 · 줄 머리는 이름을 바꾸지 않는다: `### Google Design Sprint 산출물` · `## 참고 링크 (전체)` (prd-patterns) · `# Gotchas` · `### PR/FAQ 템플릿` ·
  `### Shape Up Pitch 템플릿` · `### Linear-style Spec 템플릿` · `## Step 4: 체크리스트 검증` · `| **PR/FAQ** (Amazon) |` · `| **Linear-style Spec** |` (plan-prd) ·
  `## Step 0: 자동 로드 (독립 단계)` · `## Step 1: 입력 파싱` (plan-stories) · `## Step 0: 리서치 문서 로드` · `## Step 1: Event Storming (사건 먼저)` (plan-data-model) ·
  `## Step 0: 리서치 문서 로드` · `## Step 2: 작성` · `### User Flow (flowchart)` (plan-flow) · `## Step 3: 12 카테고리 평가 기준` · `| # | 카테고리 |` · `## Step 5: Verdict 결정` ·
  `9. **[미검증] 표기 의무**` (plan-audit) · `# Canonical Unverified-Evidence Protocol (정본 복제)` · `## Canonical User-Reported Failure Protocol` · `## Step 3: 카테고리별 Rule-by-Rule 판정` ·
  `### 카테고리별 원칙 매핑` · `## Step 4: 최종 Verdict (합성)` (planning-reviewer) · `### Mermaid Flowchart 공식 패턴` (flows) · `### Mermaid erDiagram 공식 패턴` (data-modeling) ·
  `## [2026-08-13]` (research-log) · 읽기만 하는 `design-kit/references/visual-change-protocol.md` 의 대조 문장
- 공유 파일(`.claude-plugin/marketplace.json` · `planning-kit/.claude-plugin/plugin.json` 버전 · `planning-kit/README.md` · 루트 `README.md` · 루트 `CLAUDE.md` · `docs/` HTML ·
  처리 배정표 · 감사 로그 · 실패 횟수 파일 · `.github/workflows/ci.yml` · `.harness/stale-values.yaml`)과 다른 Phase · 레포 전용 파일(`design-kit/` · `harness/` · `scripts/` ·
  `.claude/skills/`)은 건드리지 않는다 — ER-03 마지막 값. planning-kit README AUTO 구간은 스킬 · 에이전트 frontmatter 만 읽는데 그 줄이 그대로다(AP-04 · DG-05).
  문서 사이트 재생성은 Final F2 몫이라 DG-06 에서 `docs-site-regen` 을 뺀다
- QA(`harness:qa-evaluator`)는 설치본이다 — 이 Phase 가 고치는 파일에 qa-evaluator 는 없다
- 사용자 승인(Step 5) 대체: 사용자가 「자동으로 끝까지 알아서 진행해 내 허락이 필요한건 코덱스로 리서치나 검토받고」라고 위임했다(세션
  `de8c7935-a5b6-4df5-9106-fafa73c288a0` 기록 queued_command `2026-09-24T04:04:16.964Z`). Codex 사용량 한도가 소진돼(오류 원문 「You've hit your usage limit … try
  again at 11:05 PM」, 2026-09-24) 독립 Claude 검토자(REVIEW 에이전트)가 대신한다. 이어 사용자가 「코덱스 대신에 그냥 너가 알아서 진행하라고」라고 명시했다(같은 세션
  기록 user `2026-09-24T11:54:58.940Z`). 검토 결과 파일: `.harness/.meta/kaizen-0924/phase11-review.md` — 1 회차 `VERDICT: CHANGES`, 필수 둘(AR-03 (c) 지운 줄 · 사라진 제목도 세기,
  ER-03 (c) `user-setup:P10` 미반영 줄)과 권고 일곱을 이 초안에 반영했다(DRAFT 검토 반영, 2026-09-25). 권고 7 의 확인 날짜는 검토가 적은 2026-09-25 가 아니라
  근거 파일 `collected: 2026-09-24` 로 적었다 — 조회한 날이 그날이다. 같은 파일 `## 2 회차`(따로 띄운 검토자)가 아홉 자리 반영을 확인하고 새 결함 없이
  `VERDICT: APPROVE` 를 냈다 — 이 계약은 그 판정 뒤에 봉인했다(BUILD, 2026-09-25)
- 판정 한계: 뒤 단계 스킬 셋과 planning-reviewer 가 실제로 비범위 표를 읽고 겹치는 항목 앞에서 묻는지는 LLM 동작이라 결정론 측정이 없다 — 조건은 그 지시 문장이
  정해진 절 · 정해진 순서에 글자 그대로 있는지를 잰다(SK-04 ~ SK-08). planning-kit 에는 평가 사례 파일(`evals/`)이 없어 사례를 더하지 않는다. Mermaid 12 렌더는
  로컬에 Mermaid 가 없어 재지 않는다 — 그래서 새 문장이 「렌더해 보지 않았다」 고 적는다(SK-09)
- 판정 근거: SK-01 ~ SK-10 · RE-02 — 산출물이 문서 문장 자체라 정해진 절 · 줄에 정해진 문장이 있는지가 판정이다. `sect` 가 코드 펜스를 건너뛰고 절을 자르고, `gline` 이 한 줄짜리
  Gotcha · 표 행을 고르고, `run4` 가 틀의 네 줄(제목 · 표 머리 · 구분선 · 예시 행)이 붙어 있는지 본다. 시작 커밋 판에서 새 문장 0 을 봉인 전에 확인했고, 문장 하나만 지운
  사본에서 그 값이 떨어졌다(`회귀 게이트` 절)
- 판정 근거: ER-01 · ER-02 · AP-01 · AP-03 · DG-02 — 편집 전 판과 파일마다 비교한 더한 줄 계산이다. 각각 양성 대조가 붙어 있다
- 판정 근거: ER-03 · AR-01 · SC-00 · DG-01 · DG-04 · DG-06 — 커밋 기록과 봉인 검증 함수를 실제로 돌린 출력이다. 예행 저장소 변형 넷이 양성 대조다
- 판정 근거: AR-02 · AR-03 · AP-04 · DG-05 — 가리키는 제목 · 편집 전과 같아야 하는 절 · 저장소 검사 도구를 실제로 돌린 출력이다. 각각 한 군데를 깬 사본이 대조다
- 커버리지 해소: SK-01 ~ SK-10 · AR-02 · AR-03 · RE-02 · AP-04 — 산문의 파일 이름은 측정 `m <조건 ID>` 가 공통 정의의 변수(`$PP` · `$FL` · `$DM` · `$RL` · `$PRD` · `$ST` · `$MO` · `$FW` · `$AU` · `$RV`)로
  연다(파일과 변수의 대응은 `common.sh` 머리). 토큰은 `m.sh` 의 같은 ID 갈래에 글자 그대로 있다. 읽기만 하는 `design-kit/references/visual-change-protocol.md` 와
  `planning-kit/skills/plan-sync-github/SKILL.md` 는 `m.sh` 가 `$E/` 뒤 경로로 연다. `0.2.0` · `0.1.1` · `1.1.0` · `2026-09-25` 는 머리 설정 값이라 `fm_get` 이 읽는다.
  `mock.py` · `common.sh` · `m.sh` 는 측정 도구 자체의 이름, `phase4-notes.md` 등은 넘김 출처 설명이다. SK-02 · AR-02 의 `docs/planning/prd-patterns.md` 는 새 Gotcha 가
  가리키는 문자열이라 `m.sh` 의 `SK-02)` 갈래 토큰과 `AR-02)` 갈래 `$PP` 가 잰다
- 커버리지 해소: ER-01 · ER-03 — `.harness/.meta/kaizen-0924/phase11-notes.md` · `.harness/.meta/evidence/phase11.md` 는 공통 정의의 `$NOTES` · `$EVID` 다. ER-03 의 넘김 경로
  (`harness/skills/sprint/SKILL.md` · `planning-kit/agents/planning-reviewer.md` · `docs/planning-kit/prd-patterns.html` · `plugin.json`)는 `m.sh` `ER-03)` 갈래 `toks` 의 인자이고,
  공유 경로는 `not_other` 의 인자다
- 커버리지 해소: AR-01 — `planning-kit` · `docs/planning` 은 `unsigned_on` 의 인자, `.harness/` 는 `scope` 블록 줄과 `verify_seal` 이 도는 폴더다.
  `harness/references/contract-schema.md` 는 셋째 값 권장 형태의 출처다
- 검출기는 공백 든 코드 조각 안의 인자를 읽지 못한다 — 위 해소 줄이 전부 그 경우다
- 편집 전부터 있던 경고(`docs/planning/` 의 MD022 · MD032 · MD034 등 — 이 폴더는 원래 제목 아래 빈 줄 없이, 맨 URL 로 쓴다)는 범위 밖이다. DG-02 는 더한 줄의 새 경고만 잰다.
  그래서 새 줄은 빈 줄과 `<…>` URL 로 쓴다 — 같은 파일 안에서 꼴이 섞이지만 새 경고는 0 이다
- notes 에 함께 적는다(조건으로는 재지 않는다): `GAP 분석` 절의 Phase 1 가이드 변경 셋 표, 「그대로 둔 곳」 — plan-prd Gotcha 5 · plan-audit 카테고리 3 행의 「최소 3 개」(이 킷의
  기준이라는 표시는 research-log 새 항목에만 적었다 — plan-audit 행은 Shape Up §9 를 출처로 달고 있다), Design Sprint 산출물에 틀이 없는 것,
  planning-reviewer `:151` 의 빈 「4 요건」 가리킴. ER-03 마지막 값이 0 이 아니면 QA 가 그 커밋 목록부터 보고 판정한다는 한 줄
- 기능 조건 18 · 전체 조건 줄 28
- 사용자가 할 일: 없음

## 회귀 게이트 — 측정 공통 정의와 봉인 전 실측

모든 조건의 측정은 아래 `common.sh` 와 `m.sh` 를 차례로 `.` 으로 읽은 **bash** 셸에서 돈다 — `common.sh` 는 bash 가 아니면 `NOT_BASH` 를 찍고 종료 코드 2 로 끝난다
(zsh 는 따옴표 없는 변수를 쪼개지 않고 배열 첨자가 1 부터다). `m` 은 도우미 함수와 두 판 폴더가 없으면 `HELPER_MISSING` · `SNAPSHOT_MISSING` 을 내고 멈춘다 —
그래서 조건마다 `type m` 하나로 정의 확인을 대신한다. 두 판 풀기가 끊기거나 열 파일 가운데 하나라도 비면 `common.sh` 가 `SNAPSHOT_FAIL` 을 내고 종료 코드 2 로 끝난다.
셸이 끝나면 두 판 폴더를 지운다. `END_UNRESOLVED` 가 찍히면 셸이 종료 코드 2 로 끝난다.
`m` 의 종료 코드는 판정하지 않는다 — 판정은 출력 값으로 한다. 갈래 마지막 명령이 `grep -c` 이고 그 값이 0 이면 종료 코드가 1 이라, 0 을 기대하는 조건은 PASS 값에서 1 을 낸다
(예행 판에서 ER-01 · ER-03 · AP-03 이 PASS 값을 내고 종료 코드 1 로 끝났다). `m` 이 스스로 멈출 때(`HELPER_MISSING` · `SNAPSHOT_MISSING` · `UNKNOWN` · DG-05 사본 저장소를 못 만들 때)만 2 다.
세 블록을 각 블록 첫 `#` 주석 줄(셔뱅 다음)의 이름 그대로 한 폴더에 저장하고 그 폴더를 `K` 에 넣는다. `new-warnings.sh` 옆에는 `node_modules` 를
`/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/de8c7935-a5b6-4df5-9106-fafa73c288a0/scratchpad/p1build/node_modules` 로 잇고
`cfg.markdownlint-cli2.jsonc` = `{ "config": { "MD013": false } }` 를 둔다 — 준비 단계 실측(2026-09-25): 그 자리의 `.bin/markdownlint-cli2 --version` 첫 줄이
`markdownlint-cli2 v0.23.2 (markdownlint v0.41.1)`. 없으면 그 폴더에서 `npm install --no-save markdownlint-cli2@0.23.2` 부터 돌린다.
그 밖의 준비 단계 실측(2026-09-25): `command -v bash` → `/opt/homebrew/bin/bash` (5.3.9) · `/bin/bash --version` 3.2.57 · `python3` 있음 · `shasum` 있음.
`common.sh` 의 `R` 은 예행 저장소를 가리킬 때만 쓴다 — 비우면 작업 폴더다. 두 판을 `${TMPDIR:-/tmp}/p11m.XXXXXX` 에 푸니 `TMPDIR` 를 스크래치 폴더로 두고 읽는다.
예행 도구(스크래치 `p11d/`): `mock.py`(sha256 앞 16 자리 `593fb476788192fb`) · `rehearse.sh`(시작 커밋에서 예행 저장소를 만들어 봉인 · 다른 Phase 커밋 · 구현 두 커밋 · `end_sha` ·
notes · `end_sha` 를 흉내 낸다. 변형 `base` · `unsigned-mine` · `unsigned-shared` · `signed-outside` · `cross-phase`) · `runm.sh` · `del.sh`(문장 삭제 대조) · `ctl.sh` · `ctl2.sh`(양성 · 음성 대조) · `na.sh`.

```bash
# common.sh — 측정 공통 정의. bash 로 읽는다 (zsh 는 배열 첨자가 1 부터이고 따옴표 없는 변수를 쪼개지 않는다)
[ -n "${BASH_VERSION:-}" ] || { echo "NOT_BASH — bash -c 안에서 다시 읽는다"; exit 2; }
export LC_ALL=C.UTF-8   # 번역투 정규식이 글자 단위로 돌아야 한다
cd "${R:-/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/kaizen-0924}" || exit 2
B=d88c35a70ccb88faf7bea3f57cf1f8c5f51b0279                  # 이 Phase 시작 HEAD
SIG='Kaizen-Phase: kaizen-0924-p11-planning-kit'
CF=.harness/sprint-contract-kaizen-0924-p11-planning-kit.md
AM=.harness/sprint-amendments-kaizen-0924-p11-planning-kit.md
NOTES=.harness/.meta/kaizen-0924/phase11-notes.md
EVID=.harness/.meta/evidence/phase11.md
END=$( [ -f "$AM" ] && sed -n 's/^end_sha:[[:space:]]*//p' "$AM" | tail -1 )
if [ -z "$END" ] || ! git rev-parse -q --verify "$END^{commit}" >/dev/null; then
  echo "END_UNRESOLVED — 측정을 멈춘다. HEAD 로 바꿔 재지 않는다"; exit 2
fi
: "${K:?도우미 폴더를 K 에 넣는다}"
PP=docs/planning/prd-patterns.md
FL=docs/planning/flows.md
DM=docs/planning/data-modeling.md
RL=docs/planning/research-log.md
PRD=planning-kit/skills/plan-prd/SKILL.md
ST=planning-kit/skills/plan-stories/SKILL.md
MO=planning-kit/skills/plan-data-model/SKILL.md
FW=planning-kit/skills/plan-flow/SKILL.md
AU=planning-kit/skills/plan-audit/SKILL.md
RV=planning-kit/agents/planning-reviewer.md
FILES=("$PP" "$FL" "$DM" "$RL" "$PRD" "$ST" "$MO" "$FW" "$AU" "$RV")
TH='| 하지 않는 것 | 이유 | 범위 | 코드에 남은 흔적 |'
TS='|---|---|---|---|'
TR='| (명시적 제외 · 폐기한 결정) | (왜 뺐나) | 이번 PRD / 이번 사이클 / 제품 전체 | (서버 필드 · 화면 파일 — 없으면 `없음`) |'
LOADP='이전 단계 산출물 `.planning/prd-*.md` 가 있으면 비범위 절(`## Non-goals (폐기한 결정 포함)` · Shape Up `## No-gos`)의 폐기한 결정을 함께 로드한다.'
MM=https://github.com/mermaid-js/mermaid/releases/tag/mermaid%4012.0.0
T=$(mktemp -d "${TMPDIR:-/tmp}/p11m.XXXXXX") || exit 2; mkdir -p "$T/B" "$T/E"
trap 'rm -rf "$T"' EXIT
# 두 판을 풀어 둔 폴더에서 잰다 — 작업 폴더에 남은 다른 Phase 의 미커밋 변경이 끼지 않는다
# 풀기가 도중에 끊기면 0 을 기대하는 값이 통과로 읽힌다 — 여기서 멈춘다
git archive "$B" | tar -x -C "$T/B" && git archive "$END" | tar -x -C "$T/E" || { echo "SNAPSHOT_FAIL — 측정을 멈춘다"; exit 2; }
for f in "${FILES[@]}"; do [ -s "$T/B/$f" ] && [ -s "$T/E/$f" ] || { echo "SNAPSHOT_FAIL $f"; exit 2; }; done
# sect <파일> <제목 앞부분> — 그 제목부터 같은 깊이 이하의 다음 제목 전까지. 코드 펜스 안의 `#` 줄은 제목으로 보지 않는다
sect() { awk -v h="$2" '
  /^[[:space:]]*(```|~~~)/ { fence = !fence }
  !f && !fence && index($0, h) == 1 { f = 1; lvl = match($0, /[^#]/) - 1; print; next }
  f && !fence && /^#+ / { l = match($0, /[^#]/) - 1; if (l <= lvl) exit }
  f' "$1"; }
# gline <파일> <줄 앞부분> — 그 앞부분으로 시작하는 줄. Gotcha 와 표 행은 한 줄이다
gline() { awk -v p="$2" 'index($0, p) == 1' "$1"; }
# toks <글> <토큰…> — 토큰마다 글 안에서 그 토큰이 든 줄 수
toks() { local s="$1"; shift; for t in "$@"; do printf '%s ' "$(printf '%s\n' "$s" | grep -cF -- "$t")"; done; echo; }
# run4 <글> <줄1> <줄2> <줄3> <줄4> — 네 줄이 글자 그대로 이어서 나오는 횟수 (비범위 틀의 제목 · 표 머리 · 구분선 · 예시 행)
run4() { printf '%s\n' "$1" | awk -v a="$2" -v b="$3" -v c="$4" -v d="$5" '{l[NR]=$0} END{n=0; for(i=1;i+3<=NR;i++) if(l[i]==a && l[i+1]==b && l[i+2]==c && l[i+3]==d) n++; print n}'; }
# fmb <파일> — 첫 frontmatter 블록 본문
fmb() { awk 'NR==1&&/^---/{fm=1;next} fm&&/^---/{exit} fm' "$1"; }
url()   { grep -oE 'https?://[^ )>"`]+' | sed -E 's/[.,;:]+$//' | sort -u; }
added() { for f in "${FILES[@]}"; do git diff --no-index -U0 "$T/B/$f" "$T/E/$f"; done | grep '^+' | grep -v '^+++'; }
mine() { git log --format= --name-only "${1}..${2}" --grep="^${3}\$" | grep . | LC_ALL=C sort -u; }
unsigned_on() { _b=${1}; _u=${2}; _s=${3}; shift 3
  git log --format=%H "${_b}..${_u}" -- "$@" | while read -r _c; do git log -1 --format=%B "$_c" | grep -qxF "$_s" || echo "$_c"; done; }
# not_other <base> <상한> <서명> <경로…> — 경로를 건드린 구간 안 커밋 가운데 다른 Phase 서명이 없는 커밋 (0 줄이어야 한다)
not_other() { _b=${1}; _u=${2}; _s=${3}; shift 3
  git log --format=%H "${_b}..${_u}" -- "$@" | while read -r _c; do
    _m=$(git log -1 --format=%B "$_c")
    if printf '%s\n' "$_m" | grep -qE '^Kaizen-Phase: ' && ! printf '%s\n' "$_m" | grep -qxF "$_s"; then continue; fi
    echo "$_c"; done; }
my() { mine "$B" "$END" "$SIG"; }
# scope <계약> — `## 범위 경계` 절 안, 첫 줄이 `# sprint-scope` 인 text 블록의 경로 줄
scope() { awk '/^## /{s=$0} s ~ /^## 범위 경계/ && /^```text$/{b=1; n=0; next} b && /^```$/{b=0; next} b{n++; if (n==1 && $0 != "# sprint-scope") b=0; else if (n>1) print}' "$1"; }
fm_get() { awk -v k="^$2:[[:space:]]*" 'NR==1 && /^---[[:space:]]*$/ { fm=1; next } fm && /^---[[:space:]]*$/ { exit } fm && $0 ~ k { sub(k, "", $0); print; exit }' "$1" | sed -e "s/[[:space:]]*$//" -e "s/^['\"]//" -e "s/['\"]\$//"; }
sha256_16() { if command -v sha256sum >/dev/null 2>&1; then sha256sum; elif command -v shasum >/dev/null 2>&1; then shasum -a 256; else python3 -c 'import hashlib,sys; print(hashlib.sha256(sys.stdin.buffer.read()).hexdigest())'; fi | cut -c1-16; }
contract_digest() { grep -E '^- \[[ x]\] [A-Z]{2,}-[0-9]{2}' "$1" | sed -E 's/^- \[[ x]\]/- [ ]/' | sha256_16; }
verify_seal() { rec=$(fm_get "$1" conditions_digest); rec=${rec#sha256:}; if [ -z "$rec" ]; then echo "SEAL_ABSENT $1"; return 0; fi
  act=$(contract_digest "$1"); if [ "$rec" = "$act" ]; then echo "SEAL_OK $1"; else echo "SEAL_BROKEN $1 recorded=$rec actual=$act"; fi; }
K02='(을|를) ?(처리|관리)(합니다|한다)|에 대해서?|하도록 (합니다|한다)|에 의(해|하여)|되어 있(는 경우|을 때)|(표시|적용|호출|생성|반환)(됩니다|된다)'
```

```bash
# m.sh — 조건마다 재는 값을 한 줄씩 낸다. common.sh 를 읽은 bash 에서 `m <조건 ID>` 로 부른다
m() {
  local E=$T/E S L f h fn
  # 도우미가 하나라도 없으면 grep -c 가 조용히 0 을 낸다 — 멈춘다
  for fn in sect gline toks run4 fmb url added mine unsigned_on not_other my scope fm_get verify_seal; do
    type "$fn" >/dev/null 2>&1 || { echo "HELPER_MISSING $fn"; return 2; }; done
  [ -n "${T:-}" ] && [ -d "$T/B" ] && [ -d "$E" ] || { echo "SNAPSHOT_MISSING"; return 2; }
  case "$1" in
  SK-01)  # prd-patterns §폐기한 결정 — 문장 · 자리 · 참고 링크 · 머리 설정
    S=$(sect "$E/$PP" '### 폐기한 결정 — 비범위 절 한 곳에 적는다')
    toks "$S" '### 폐기한 결정 — 비범위 절 한 곳에 적는다' \
      'PR/FAQ · Linear-style 스펙은 `## Non-goals (폐기한 결정 포함)`, Shape Up pitch 는 원문 용어대로 `## No-gos` 다.' \
      '결정 원문은 이 한 곳에만 둔다.' '같은 결정을 다시 언급하는 문서는 이 PRD 경로를 가리키고 결정을 다시 쓰지 않는다' \
      '폐기 결정에 옮겨 쓴 것은 이 킷의 추론이다' \
      '- 비범위 표가 네 칸(하지 않는 것 · 이유 · 범위 · 코드에 남은 흔적)을 갖는가?' \
      '- 범위 칸이 `이번 PRD` · `이번 사이클` · `제품 전체` 가운데 하나인가?' \
      '- PRD 를 쓴 뒤에 나온 폐기 결정을 새 문서가 아니라 이 표에 한 줄 더했는가?' \
      '- 뒤 단계 산출물(스토리 · 흐름 · 데이터 모델)이 표의 항목을 다시 만들지 않았는가?' \
      '**한계/주의사항**: 폐기는 영구 금지가 아니다.' '외부 방법론에서 온 것이 아니라 이 킷의 운영 규칙이다' \
      'PRD 가 없는 프로젝트의 기록 자리는 이 절이 정하지 않는다.' \
      '- <https://basecamp.com/shapeup/1.5-chapter-06>' '- <https://agilealliance.org/glossary/invest/>' \
      '- <https://docs.github.com/issues/planning-and-tracking-with-projects/learning-about-projects/best-practices-for-projects>'
    awk '/^### Google Design Sprint 산출물/{a=NR} /^### 폐기한 결정 — /{b=NR} /^## 참고 링크 \(전체\)/{c=NR} END{print (a && b && c && a<b && b<c) ? 1 : 0}' "$E/$PP"
    toks "$(sect "$E/$PP" '## 참고 링크 (전체)')" '- <https://agilealliance.org/glossary/invest/>' \
      '- <https://docs.github.com/issues/planning-and-tracking-with-projects/learning-about-projects/best-practices-for-projects>'
    echo "$(fm_get "$E/$PP" version) $(fm_get "$E/$PP" last_updated)" ;;
  SK-02)  # plan-prd Gotcha 14 · 번호
    L=$(gline "$E/$PRD" '14. **폐기한 결정은 비범위 절 한 곳에 네 칸으로 적는다**')
    toks "$L" '14. **폐기한 결정은' \
      '`## Non-goals (폐기한 결정 포함)` 표(Shape Up 은 `## No-gos`)에 `하지 않는 것 · 이유 · 범위 · 코드에 남은 흔적` 한 줄로 적는다' \
      '결정 원문은 여기 하나다 — 디자인 승인 기록 · 작업 계약 · 핸드오프는 이 PRD 경로를 가리키고 결정을 다시 쓰지 않는다' \
      'PRD 를 쓴 뒤에 나온 폐기 결정도 새 파일을 만들지 말고 이 표에 한 줄 더한다' \
      '`코드에 남은 흔적` 칸(서버 필드 · 호출되지 않는 화면 파일 등)은 채울 빈틈이 아니라 치울 목록이다' \
      '되살려야 할 것 같으면 사용자에게 먼저 묻는다' '폐기는 영구 금지가 아니다' \
      '하지 않는 것 · 이유 칸은 Shape Up No-gos 가 근거이고 범위 · 흔적 칸은 이 킷의 운영 규칙이다' \
      '실측(`/insights` 2026-09-24 F20)' '`docs/planning/prd-patterns.md` §폐기한 결정' \
      'https://basecamp.com/shapeup/1.5-chapter-06' 'https://agilealliance.org/glossary/invest/'
    sect "$E/$PRD" '# Gotchas' | grep -oE '^[0-9]+\. \*\*' | tr -dc '0-9\n' | paste -sd' ' - ;;
  SK-03)  # plan-prd 세 틀의 비범위 표 · Step 2 표 두 행 · Step 4 두 항목
    S=$(sect "$E/$PRD" '### PR/FAQ 템플릿')
    echo "prfaq=$(run4 "$S" '## Non-goals (폐기한 결정 포함)' "$TH" "$TS" "$TR")"
    S=$(sect "$E/$PRD" '### Shape Up Pitch 템플릿')
    echo "shapeup=$(run4 "$S" '## No-gos' "$TH" "$TS" "$TR") old=$(printf '%s\n' "$S" | grep -cxF -- '- (명시적 제외)')"
    S=$(sect "$E/$PRD" '### Linear-style Spec 템플릿')
    echo "linear=$(run4 "$S" '## Non-goals (폐기한 결정 포함)' "$TH" "$TS" "$TR") $(printf '%s\n' "$S" | awk '/^## Proposal$/{a=NR} /^## Non-goals \(폐기한 결정 포함\)$/{b=NR} /^## Milestones$/{c=NR} END{print (a&&b&&c&&a<b&&b<c)?1:0}')"
    echo "rows=$(gline "$E/$PRD" '| **PR/FAQ** (Amazon) |' | grep -cF '| 보도자료(1p) + 내부 FAQ + 외부 FAQ + Non-goals |') $(gline "$E/$PRD" '| **Linear-style Spec** |' | grep -cF '| Problem + Solution + Non-goals + Open questions + Milestones |') heads=$(grep -cxF -- "$TH" "$E/$PRD")"
    toks "$(sect "$E/$PRD" '## Step 4: 체크리스트 검증')" '- [ ] Non-goals 가 3개 이상인가' \
      '- [ ] 폐기한 결정마다 이유 · 범위 · 코드에 남은 흔적 칸이 채워졌는가 (흔적이 없으면 `없음`)' \
      '- [ ] 코드에 남은 흔적을 Solution · Proposal · Milestones · FAQ 에 새 요구로 옮겨 적지 않았는가' ;;
  SK-04)  # plan-stories — Step 1 에 규칙, Step 0 은 PRD 로드 그대로
    S=$(sect "$E/$ST" '## Step 1: 입력 파싱')
    toks "$S" '- PRD 비범위 절(`## Non-goals (폐기한 결정 포함)` · Shape Up `## No-gos`)의 폐기한 결정과 겹치는 스토리는 만들지 않는다.' \
      '코드에 흔적이 남아 있어도 요구로 읽지 않는다 — 필요해 보이면 스토리를 쓰기 전에 사용자에게 묻는다 (plan-prd Gotcha 14)'
    toks "$(sect "$E/$ST" '## Step 0: 자동 로드 (독립 단계)')" '2. **이전 단계 산출물**: `.planning/prd-*.md` 가 있으면 로드 (최신 우선).' '겹치는' ;;
  SK-05)  # plan-data-model — Step 0 로드 문장, Step 1 규칙과 그 자리
    toks "$(sect "$E/$MO" '## Step 0: 리서치 문서 로드')" "$LOADP" '이 단계에서 모델을 그리지 않는다.' '겹치는'
    S=$(sect "$E/$MO" '## Step 1: Event Storming (사건 먼저)')
    toks "$S" 'Step 0 에서 읽은 폐기한 결정과 겹치는 이벤트 · 엔티티 · 필드는 모델에 넣지 않는다.' \
      '코드 · 데이터베이스에 흔적이 남아 있어도 요구로 읽지 않는다 — 필요해 보이면 그리기 전에 사용자에게 묻는다 (plan-prd Gotcha 14).'
    printf '%s\n' "$S" | awk '/^Step 0 에서 읽은 폐기한 결정과 겹치는/{a=NR} /^PRD\/플로우에서 \*\*과거형 이벤트\*\*/{b=NR} END{print (a&&b&&a<b)?1:0}' ;;
  SK-06)  # plan-flow — Step 0 로드 문장, Step 2 규칙과 그 자리
    toks "$(sect "$E/$FW" '## Step 0: 리서치 문서 로드')" "$LOADP" '이 단계에서 다이어그램을 그리지 않는다.' '겹치는'
    S=$(sect "$E/$FW" '## Step 2: 작성')
    toks "$S" 'Step 0 에서 읽은 폐기한 결정과 겹치는 화면 · 분기 · 단계는 그리지 않는다.' \
      '코드에 흔적이 남아 있어도 요구로 읽지 않는다 — 필요해 보이면 그리기 전에 사용자에게 묻는다 (plan-prd Gotcha 14).'
    printf '%s\n' "$S" | awk '/^Step 0 에서 읽은 폐기한 결정과 겹치는/{a=NR} /^### User Flow \(flowchart\)/{b=NR} END{print (a&&b&&a<b)?1:0}' ;;
  SK-07)  # plan-audit 카테고리 3 행
    L=$(gline "$E/$AU" '| 3 | Non-goals |')
    toks "$L" '최소 3개 명시 (Shape Up 의 no-gos / rabbit holes 포함)' '+ 폐기한 결정마다 이유 · 범위 · 코드에 남은 흔적 칸' \
      '+ stories · flow · data-model 산출물에 폐기한 항목이 다시 들어가지 않음 (planning-reviewer Step 3 확인)' \
      '| prd-patterns.md §Shape Up / §폐기한 결정 |' '[Shape Up §6](https://basecamp.com/shapeup/1.5-chapter-06)'
    echo "cols=$(gline "$E/$AU" '| # | 카테고리 |' | awk -F'|' '{print NF}') $(printf '%s\n' "$L" | awk -F'|' '{print NF}') rows=$(printf '%s\n' "$L" | grep -c .)" ;;
  SK-08)  # planning-reviewer — 원칙 매핑 행 · 다시 들어갔는지 확인 절과 그 자리
    toks "$(gline "$E/$RV" '| Non-goals |')" '| prd-patterns.md §Shape Up (rabbit holes/no-gos), §폐기한 결정 |' \
      '[Shape Up §6](https://basecamp.com/shapeup/1.5-chapter-06)'
    S=$(sect "$E/$RV" '### Non-goals 카테고리 — 폐기한 항목이 다시 들어갔는지')
    toks "$S" '### Non-goals 카테고리 — 폐기한 항목이 다시 들어갔는지' '`stories-*.md` · `flow-*.md` · `data-model-*.md` 를 Grep 한다' \
      '걸린 줄이 그 항목을 스토리 · 화면 · 필드로 다시 넣었으면 Non-goals 카테고리는 FAIL 이고' '제외나 질문으로 적은 줄이면 PASS 근거다' \
      '같은 낱말이 PRD 비범위 표의 그 줄에도 걸려야 한다' '뒤 단계 산출물의 0 매치를 PASS 근거로 쓰지 않는다 (Step 2 공허한 증거 분기)' \
      '세 산출물이 인벤토리에 없으면 이 확인을 건너뛰고 근거에 그렇게 적는다'
    awk '/^### 카테고리별 원칙 매핑/{a=NR} /^### Non-goals 카테고리 — /{b=NR} /^## Step 4: 최종 Verdict/{c=NR} END{print (a&&b&&c&&a<b&&b<c)?1:0}' "$E/$RV"
    grep -cxF 'tools: Read, Grep, Glob' "$E/$RV" ;;
  SK-09)  # 현행화 — flows.md 버전 문장 · data-modeling.md ERD 배치 · 출처 · 머리 설정 · plan-sync-github 그대로
    echo "old=$(grep -cF '아래 예시는 공식 문법 10.x+ / 11.x 계열에서 유효한 형태다.' "$E/$FL")"
    toks "$(sect "$E/$FL" '### Mermaid Flowchart 공식 패턴')" '아래 예시는 flowchart 공식 문서의 문법을 따른다.' \
      '2026-09-24 에 확인한 Mermaid 최신 안정판은 12.0.0(2026-09-10 공개)이고, 이 예시를 12 에서 렌더해 보지는 않았다.' "- <$MM>"
    toks "$(sect "$E/$FL" '## 참고 링크 (전체)')" "- <$MM>"
    toks "$(sect "$E/$DM" '### Mermaid erDiagram 공식 패턴')" \
      'Mermaid 12.0.0(2026-09-10 공개)부터 ERD 의 기본 배치가 Dagre 에서 ELK 로, 기본 모양(theme · look)도 바뀌었다' \
      '렌더 결과를 비교할 때는 렌더러 버전을 함께 적는다' "- <$MM>"
    toks "$(sect "$E/$DM" '## 참고 링크 (전체)')" "- <$MM>"
    f=planning-kit/skills/plan-sync-github/SKILL.md
    echo "$(fm_get "$E/$FL" version) $(fm_get "$E/$FL" last_updated) $(fm_get "$E/$DM" version) $(fm_get "$E/$DM" last_updated) sync_same=$(cmp -s "$T/B/$f" "$E/$f" && echo 1 || echo 0)" ;;
  SK-10)  # research-log 새 항목 · 맨 위 자리 · 옛 항목 그대로 · 머리 설정
    S=$(sect "$E/$RL" '## [2026-09-24] — Phase 11 kaizen (폐기한 결정 기록 자리)')
    toks "$S" '## [2026-09-24] — Phase 11 kaizen (폐기한 결정 기록 자리)' '처리 배정표 `F20` · `backend-family:P1` 두 행을 받았다' \
      '### 결정 — 폐기한 결정의 원문은 PRD 비범위 절 한 곳' '처리 배정표 제안은 세 칸이었고, 근거 파일 §4 권장 8 에 따라' '### 현행화' \
      '`2022-11-28` 은 2028-03-10 까지 지원되고' 'https://github.com/mermaid-js/mermaid/releases/tag/mermaid%4012.0.0' '### 명시적 비범위' \
      'Design Sprint 산출물은 plan-prd 에 틀이 없다' '다음 사이클 Phase 3 이 정본을 정리한 뒤'
    echo "first=$(grep -m1 '^## \[' "$E/$RL" | grep -cxF '## [2026-09-24] — Phase 11 kaizen (폐기한 결정 기록 자리)') old_same=$(diff <(sed -n '/^## \[2026-08-13\]/,$p' "$T/B/$RL") <(sed -n '/^## \[2026-08-13\]/,$p' "$E/$RL") >/dev/null && echo 1 || echo 0) $(fm_get "$E/$RL" version) $(fm_get "$E/$RL" last_updated)" ;;
  ER-01)  # 새로 생긴 URL 이 근거 파일에 있다 — 열 파일은 파일마다 편집 전 판과 비교, notes 는 URL 전부
    for f in "${FILES[@]}"; do comm -13 <(url < "$T/B/$f") <(url < "$E/$f"); done | sort -u | comm -23 - <(url < "$E/$EVID") | grep -c .
    if [ -f "$E/$NOTES" ]; then url < "$E/$NOTES" | comm -23 - <(url < "$E/$EVID") | grep -c .; else echo NOTES_MISSING; fi ;;
  ER-02)  # 더한 줄의 번역투 6 종 · 특정 앱 · 도구 서버 이름
    echo "added=$(added | grep -c .) k02=$(added | grep -cE "$K02") names=$(added | grep -ciE 'fit-?pal|fit_pal|flutter[-_]playwright|playwright-mcp|chrome-devtools-mcp')" ;;
  ER-03)  # notes 문자열 · 넘김 · 미반영 사유 · 공유 파일과 다른 Phase 파일을 건드린 커밋
    git cat-file -e "$END:$NOTES" 2>/dev/null && echo notes_committed=1 || echo notes_committed=0
    toks "$(cat "$E/$NOTES" 2>/dev/null)" '`F20`' '`backend-family:P1`' '## 바꾼 파일' '## 반영한 처리 배정표 키' '## 미반영 키와 사유' \
      '## 넘기는 것' '## changelog 한 단락' '## 킷 로그 한 단락' '## 다음 사이클 메모'
    # 넘김 · 미반영 사유는 그 절 안에서 센다 — 낱말은 다른 절에도 나와 넘김 줄을 빠뜨려도 1 이 된다
    toks "$(sect "$E/$NOTES" '## 넘기는 것' 2>/dev/null)" 'harness/skills/sprint/SKILL.md' 'planning-kit/agents/planning-reviewer.md' \
      'docs/planning-kit/prd-patterns.html' 'plugin.json' 'user-setup:P6'
    toks "$(sect "$E/$NOTES" '## 미반영 키와 사유' 2>/dev/null)" '2026-03-10' 'Design Sprint' 'user-setup:P10'
    not_other "$B" "$END" "$SIG" .claude-plugin/marketplace.json planning-kit/.claude-plugin/plugin.json planning-kit/README.md README.md CLAUDE.md \
      .harness/.meta/orchestrator-audit-log.md .harness/.meta/kaizen-failure-count.yaml .claude/kaizen-input/insights-report.md \
      .github/workflows/ci.yml .harness/stale-values.yaml .claude/skills harness scripts design-kit docs/planning-kit docs/index.html | grep -c . ;;
  AR-01)  # 허용 경로 · 서명 · 봉인 · 범위 선언 블록
    unsigned_on "$B" "$END" "$SIG" planning-kit docs/planning | grep -c .
    echo "$(my | grep -v '^\.harness/' | grep -vxF -f <(printf '%s\n' "${FILES[@]}") | grep -c .) $(my | grep -cxF -f <(printf '%s\n' "${FILES[@]}"))"
    find .harness -type f -name 'sprint-contract*.md' -print0 | while IFS= read -r -d '' f; do verify_seal "$f"; done \
      | awk '$1=="SEAL_BROKEN"{print $2}' | sed 's#^\./##' | sort -u | comm -12 - <( { my; echo "$CF"; } | sort -u) | grep -c .
    verify_seal "$E/$CF" | cut -d' ' -f1
    diff <(scope "$E/$CF" | grep -vxF '.harness/' | sort) <(printf '%s\n' "${FILES[@]}" | sort) >/dev/null && echo "scope_same=1" || echo "scope_same=0"
    scope "$E/$CF" | grep -cxF '.harness/' ;;
  AR-02)  # 새 문장이 가리키는 자리가 실제로 있다 (Counterpart — design-kit 쪽 한 문장 포함)
    echo "$(grep -c '^### 폐기한 결정 — ' "$E/$PP") $(grep -c '^14\. \*\*폐기한 결정' "$E/$PRD") $(cat "$E/$ST" "$E/$MO" "$E/$FW" | grep -cF '(plan-prd Gotcha 14)') $(sect "$E/$RV" '## Step 3: 카테고리별 Rule-by-Rule 판정' | grep -cxF '### Non-goals 카테고리 — 폐기한 항목이 다시 들어갔는지') $(grep -cF '**공허한 증거 분기' "$E/$RV") $(grep -lF '§폐기한 결정' "$E/$PRD" "$E/$AU" "$E/$RV" | grep -c .) $(grep -cF '제품 요구 수준의 폐기 결정(기능·설정 항목을 없앤다는 결정)은 이 기록에서 새로 정하지 않는다' "$E/design-kit/references/visual-change-protocol.md")" ;;
  AR-03)  # 정본 복제 · 카테고리 수 · Step 0 은 로드만 (planning-kaizen Gotcha 7 · 8 · 9)
    for h in '# Canonical Unverified-Evidence Protocol (정본 복제)' '## Canonical User-Reported Failure Protocol'; do
      diff <(sect "$T/B/$RV" "$h") <(sect "$E/$RV" "$h") >/dev/null && printf '1 ' || printf '0 '; done
    diff <(gline "$T/B/$AU" '9. **[미검증] 표기 의무**') <(gline "$E/$AU" '9. **[미검증] 표기 의무**') >/dev/null && printf '1 ' || printf '0 '
    diff <(sect "$T/B/$AU" '## Step 5: Verdict 결정') <(sect "$E/$AU" '## Step 5: Verdict 결정') >/dev/null && echo 1 || echo 0
    echo "$(sect "$E/$AU" '## Step 3: 12 카테고리 평가 기준' | grep -cE '^\| (0a|0b|[0-9]+) \|') $(sect "$E/$RV" '### 카테고리별 원칙 매핑' | grep -E '^\| ' | grep -vE '^\| 카테고리 \||^\|-' | grep -c .)"
    # 더한 줄(>)만 세면 지운 줄과 제목이 바뀌어 비어 버린 절이 0 으로 통과한다 — 양쪽을 다 센다
    for f in "$PRD" "$ST" "$AU"; do printf '%s ' "$(diff <(sect "$T/B/$f" '## Step 0: 자동 로드 (독립 단계)') <(sect "$E/$f" '## Step 0: 자동 로드 (독립 단계)') | grep -c '^[<>] .')"; done
    for f in "$MO" "$FW"; do printf '%s ' "$(diff <(sect "$T/B/$f" '## Step 0: 리서치 문서 로드') <(sect "$E/$f" '## Step 0: 리서치 문서 로드') | grep -c '^[<>] .')"; done; echo ;;
  RE-02)  # 규칙 본문은 plan-prd 한 곳 — 치울 목록 설명 · 표 머리는 plan-prd 에만, 뒤 단계 셋과 reviewer 의 더한 줄은 칸을 다시 적지 않는다
    echo "$(grep -rlF '치울 목록' "$E/planning-kit" | sed "s#^$E/##" | sort | paste -sd' ' -) | $(grep -rlF -- "$TH" "$E/planning-kit" | sed "s#^$E/##" | sort | paste -sd' ' -) | $(for f in "$ST" "$MO" "$FW" "$RV"; do git diff --no-index -U0 "$T/B/$f" "$E/$f"; done | grep '^+' | grep -v '^+++' | grep -cE '이유 · 범위|치울 목록')" ;;
  AP-01)  # 더한 줄에 이 킷 플러그인 버전 값 — 값은 plugin.json 에서 읽는다
    L=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["version"])' "$E/planning-kit/.claude-plugin/plugin.json")
    echo "version=$L $(added | grep -cF -- "$L")" ;;
  AP-03)  # 펜스 — 더한 줄에 펜스 줄 (docs/planning 은 V6 가 읽지 않는다)
    added | grep -cE '^\+[[:space:]]*(```|~~~)' ;;
  AP-04)  # frontmatter — 고친 SKILL.md 다섯과 reviewer 의 첫 블록이 편집 전과 같고 name 줄이 이름과 같다
    for f in "$PRD" "$ST" "$MO" "$FW" "$AU" "$RV"; do
      case "$f" in */SKILL.md) L=$(basename "$(dirname "$f")") ;; *) L=$(basename "$f" .md) ;; esac
      printf '%s/%s ' "$(diff <(fmb "$T/B/$f") <(fmb "$E/$f") >/dev/null && echo 1 || echo 0)" "$(fmb "$E/$f" | grep -cxF "name: $L")"; done; echo ;;
  DG-02)  # markdownlint — 더한 줄의 새 경고
    for f in "${FILES[@]}"; do L=$(printf '%s' "$f" | tr '/' '_'); cp "$T/B/$f" "$T/$L.0.md"; cp "$E/$f" "$T/$L.md"; bash "$K/new-warnings.sh" "$T/$L.0.md" "$T/$L.md"; done ;;
  DG-05)  # 저장소 검사 — $END 판을 git 저장소로 만든 사본에서 돈다 (작업 폴더의 다른 Phase 미커밋 변경이 끼지 않는다)
    local G=$T/G; rm -rf "$G"; cp -R "$E" "$G"
    git -C "$G" init -q && git -C "$G" add -A && git -C "$G" -c user.name=m -c user.email=m@m commit -qm snap || return 2
    # V 줄 머리에는 FAIL 이 안 찍힌다(아래 들여쓴 줄에 찍힌다) — `— OK` · `— SKIP (no templates/)` 로 끝나지 않는 V 줄을 센다
    ( cd "$G" && python3 scripts/validate-plugin.py planning-kit > "$T/vp.txt" 2>&1; echo $? > "$T/vp.rc" )
    echo "$(grep -cE '^  V([1-9]|10) ' "$T/vp.txt") $(grep -E '^  V([1-9]|10) ' "$T/vp.txt" | grep -cvE -- '— (OK|SKIP \(no templates/\))$') rc=$(cat "$T/vp.rc")"
    ( cd "$G" && python3 scripts/sync-docs.py --check-only > "$T/sd.txt" 2>&1 ); echo "sync_docs_rc=$? $(grep -cxF '  planning-kit/README.md: 동기화됨' "$T/sd.txt")"
    ( cd "$G" && python3 scripts/check-stale-values.py > "$T/sv.txt" 2>&1 ); echo "stale_rc=$? ran=$(grep -c '^검사 범위: 소스 디렉토리 ' "$T/sv.txt") $(grep -cF -f <(printf '%s\n' "${FILES[@]}") "$T/sv.txt")" ;;
  DG-06)  # 사이클 검사 — 이 Phase 몫 줄만 본다. docs-site-regen 은 Final F2 몫
    python3 scripts/validate-post-kaizen.py --since "$B" --verbose > "$T/vpk.txt" 2>&1
    grep -E '\] . (scope-isolation|doc-contracts): ' "$T/vpk.txt" | awk '{print $5, $2}'
    python3 scripts/validate-doc-contracts.py -v 2>&1 | awk -F' → ' '/^ *검사: /{a=$1; sub(/^ *검사: /,"",a); sub(/:[0-9]+$/,"",a); print a; print $2}' | sort -u > "$T/dc.txt"
    echo "doc_checked=$(grep -c . "$T/dc.txt") doc_mine=$(comm -12 "$T/dc.txt" <(my) | grep -c .)"
    # 위반 커밋 목록을 읽은 수와 그 가운데 이 Phase 서명 커밋 수. 목록을 못 읽으면 둘째 값이 조용히 0 이 되므로 첫 값을 함께 본다
    awk '/ scope-isolation: /{f=1;next} /^\[ /{f=0} f&&/^ +[0-9a-f]{7,40}$/{print $1}' "$T/vpk.txt" > "$T/viol.txt"
    echo "violators=$(grep -c . "$T/viol.txt") mine=$(while read -r c; do git log -1 --format=%B "$c" | grep -qxF "$SIG" && echo "$c"; done < "$T/viol.txt" | grep -c .)" ;;
  *) echo "UNKNOWN $1"; return 2 ;;
  esac
}
```

```bash
#!/usr/bin/env bash
# new-warnings.sh <옛 파일> <새 파일> — 새 파일에서 더한 줄에 걸린 경고만 센다. 줄이 밀리므로 전체 수 차이로 세지 않는다
# 줄 번호는 경로 뒤 첫 번째 숫자다. 탐욕 매치(^[^ ]*:)로 뽑으면 열 번호가 줄 번호로 둔갑한다 (실측 2026-09-24)
# 린터가 안 돌면 경고 0 이 조용히 나온다 — 돌았다는 줄(Linting: 1 file)이 없으면 멈춘다 (실측 2026-09-25: 옆에 node_modules 가 없어 0)
set -u
DIR=$(cd "$(dirname "$0")" && pwd)
ADDED=$(git diff --no-index -U0 -- "$1" "$2" | awk '/^@@/{split($3,a,","); s=substr(a[1],2)+0; n=(a[2]==""?1:a[2]+0); for(i=0;i<n;i++) print s+i}' | sort -u)
OUT=$("$DIR/node_modules/.bin/markdownlint-cli2" --config "$DIR/cfg.markdownlint-cli2.jsonc" "$2" 2>&1)
printf '%s\n' "$OUT" | grep -q '^Linting: 1 file' || { echo "LINT_NOT_RUN $2"; exit 2; }
LINES=$(printf '%s\n' "$OUT" | grep -E ':[0-9]+(:[0-9]+)? (error|warning) ' | sed -E 's#^([^:]*):([0-9]+).*#\2#' | sort -u)
NEWW=$(comm -12 <(printf '%s\n' "$ADDED" | grep . | sort) <(printf '%s\n' "$LINES" | grep . | sort) | wc -l | tr -d ' ')
echo "total_warning_lines=$(printf '%s\n' "$LINES" | grep -c .) added_lines=$(printf '%s\n' "$ADDED" | grep -c .) new_warnings=$NEWW"
```

### 봉인 전 실측 — 예행 판 · 시작 커밋 판

예행 판은 이 계약 초안을 봉인해 커밋하고 `mock.py` 를 적용한 두 커밋 · notes 모의본까지 올린 예행 저장소(변형 없음)다. 시작 커밋 판은 `end_sha` 를 시작 커밋으로 둔 예행 저장소다.
두 해석기(bash 5.3.9 · `/bin/bash` 3.2.57)에서 같은 값이 나왔다(끝 판 출력은 바이트 단위로 같고, 시작 커밋 판은 임시 폴더 이름만 다르다).
검토 반영 뒤(2026-09-25) 예행 저장소 여섯을 새로 만들어 조건 스물셋 · 변형 넷 · 대조 전부를 다시 쟀다 — 스크래치 `p11d2/`(`runall.sh` · `ctl3.sh` · `ctl4.sh`, 도우미는 이 계약에서 새로 뽑은 `p11d/k5`).
바뀐 값은 ER-03 둘째 · 넷째 줄과 AR-03 · SK-09 대조뿐이다.

| 조건 | 예행 판 (`m` 출력) | 시작 커밋 판 | 대조 |
| --- | --- | --- | --- |
| SK-01 | `1` 열다섯 · `1` · `1 1` · `0.2.0 2026-09-25` | `0` 열다섯 · `0` · `0 0` · `0.1.0 2026-04-14` | 문장 삭제 16 가운데 16 이 바뀜 |
| SK-02 | `1` 열둘 · `1 2 3 4 5 6 7 8 9 10 11 12 13 14` | `0` 열둘 · `1 … 13` | 문장 삭제 15 가운데 14 (나머지 하나는 첫 자리가 Gotcha 10) |
| SK-03 | `prfaq=1` · `shapeup=1 old=0` · `linear=1 1` · `rows=1 1 heads=3` · `1 1 1` | `prfaq=0` · `shapeup=0 old=1` · `linear=0 0` · `rows=0 0 heads=0` · `1 0 0` | 문장 삭제 18 가운데 15 (첫 자리가 Gotcha 14 인 제목 둘 · 0 기대 옛 줄 하나) |
| SK-04 | `1 1` · `1 0` | `0 0` · `1 0` | 문장 삭제 6 가운데 6 |
| SK-05 | `1 1 0` · `1 1` · `1` | `0 0 0` · `0 0` · `0` | 문장 삭제 7 가운데 7 |
| SK-06 | `1 1 0` · `1 1` · `1` | `0 0 0` · `0 0` · `0` | 문장 삭제 7 가운데 7 |
| SK-07 | `1 1 1 1 1` · `cols=7 7 rows=1` | `1 0 0 0 0` · `cols=7 7 rows=1` | 문장 삭제 7 가운데 6 (나머지 하나는 첫 자리가 카테고리 2 행) |
| SK-08 | `1 1` · `1` 일곱 · `1` · `1` | `0 0` · `0` 일곱 · `0` · `1` | 문장 삭제 11 가운데 11 |
| SK-09 | `old=0` · `1 1 1` · `1` · `1 1 1` · `1` · `0.1.1 2026-09-25 0.1.1 2026-09-25 sync_same=1` | `old=1` · `0 0 0` · `0` · `0 0 0` · `0` · `0.1.0 2026-04-14 0.1.0 2026-04-14 sync_same=1` | 문장 삭제 12 가운데 11 (0 기대 옛 문장 하나) · flows 버전 문장에서 「2026-09-24 에 확인한 」 만 지움 → 둘째 줄 `1 0 1` · plan-sync-github 에 빈 줄 → `sync_same=0` |
| SK-10 | `1` 열 · `first=1 old_same=1 1.1.0 2026-09-25` | `0` 열 · `first=0 old_same=1 1.0.0 2026-08-13` | 문장 삭제 10 가운데 10 · 2026-08-13 항목 한 줄 고침 → `old_same=0` |
| ER-01 | `0` · `0` | `0` · `NOTES_MISSING` | 문서에 가짜 URL → `1` · notes 에 가짜 URL → 둘째 `1` · notes 지움 → `NOTES_MISSING` |
| ER-02 | `added=104 k02=0 names=0` | `added=0 k02=0 names=0` | 「이 값이 적용된다」 → `k02=1` · 「fit-pal 에서 본 일」 → `names=1` |
| ER-03 | `notes_committed=1` · `2 1 1 1 1 1 1 1 1` · `1` 다섯 · `1 1 1` · `0` | `notes_committed=0` · `0` … (notes 없음) | 변형 넷 다섯째 줄 `1` · 넘김 줄을 다른 절로 옮긴 사본 셋째 줄 첫 값 `0` · 미반영 절의 `user-setup:P10` 줄을 지우거나 `## 다음 사이클 메모` 로만 옮긴 사본 넷째 줄 `1 1 0` |
| AR-01 | `0` · `0 10` · `0` · `SEAL_OK` · `scope_same=1` · `1` | 계약이 없는 판이라 재지 않음 | `unsigned-mine` ① `1` · `signed-outside` ② `1 10` · `cross-phase` ② `2 10` · 작업 폴더 계약 한 글자 ③ `1` · 끝 판 계약 한 글자 ④ `SEAL_BROKEN` |
| AR-02 | `1 1 3 1 1 3 1` | `0 0 0 0 1 0 1` | prd-patterns 제목 바꿈 → 첫 값 `0` · design-kit 문장 바꿈 → 끝 값 `0` |
| AR-03 | `1 1 1 1` · `12 12` · `0 0 0 1 1` | `1 1 1 1` · `12 12` · `0 0 0 0 0` | 기준 원본 사본 한 구절 지움 → `0 1 1 1` · plan-prd Step 0 3 번 항목 자리에 한 줄 끼움 → `3 0 0 1 1` · plan-prd Step 0 제목 바꿈 → `6 0 0 1 1` · plan-audit Step 0 3 번 줄 지움 → `0 0 1 1 1` · plan-audit 행 하나 → `13 12` |
| RE-02 | `planning-kit/skills/plan-prd/SKILL.md \| planning-kit/skills/plan-prd/SKILL.md \| 0` | ` \|  \| 0` | plan-flow 「치울 목록」 → 첫 칸 두 파일 · plan-stories 「이유 · 범위」 → 셋째 `1` · plan-flow 표 머리 → 둘째 칸 두 파일 |
| AP-01 | `version=0.5.1 0` | `version=0.5.1 0` | 「버전 0.5.1」 → `1` |
| AP-03 | `0` | `0` | 펜스 한 줄 → `1` |
| AP-04 | `1/1` 여섯 | `1/1` 여섯 | plan-flow description 한 글자 → 넷째 `0/1` |
| DG-02 | 열 줄 모두 `new_warnings=0` | 열 줄 모두 `new_warnings=0` (더한 줄 0) | `#bad heading` → 그 줄 `new_warnings=1` |
| DG-05 | `10 0 rc=0` · `sync_docs_rc=0 1` · `stale_rc=0 ran=1 0` | 같음 | `nam:` → `10 1 rc=2` · 옛 값 `1m30s` → `stale_rc=1 ran=1 1` |
| DG-06 | `scope-isolation: PASS` · `doc-contracts: PASS` · `doc_checked=2 doc_mine=0` · `violators=0 mine=0` | 같음 | `cross-phase` → `scope-isolation: FAIL` · `violators=1 mine=1` |
| N/A 줄 | `SC-00=0 DG-01=0 DG-04=0 RE-01=0` (`na.sh`) | — | `signed-outside` → `SC-00=1` · DG-04 의 `grep -cE` 에 `a/b.rs` · `c.sh` · `d.md` → `2` |

### 대조 — 문장 삭제 · 양성 · 음성

- 문장 삭제 대조(`del.sh`): SK-01 ~ SK-10 갈래의 토큰 109 개를 끝 판 사본에서 하나씩 한 번 지우고 그 조건을 다시 쟀다 — 103 개는 출력이 바뀌었고(DROP), 4 개는 그대로(NODROP), 2 개는 끝 판에 없었다(MISSING).
  달라지지 않은 넷은 지운 첫 자리가 다른 줄이었던 경우다: SK-02 의 맨 Shape Up URL 은 첫 자리가 Gotcha 10 이다(Gotcha 14 안의 같은 URL 을 겨눈 토큰은 떨어진다),
  SK-03 의 `## Non-goals (폐기한 결정 포함)` · `## No-gos` 는 첫 자리가 Gotcha 14 문장이다(틀마다 제목과 표 머리를 붙여 겨눈 토큰 넷은 떨어진다), SK-07 의 `[Shape Up §6](…)` 는
  첫 자리가 카테고리 2 행이다(카테고리 3 행을 겨눈 토큰은 떨어진다). 없던 둘은 0 을 기대하는 토큰이다(SK-03 옛 `- (명시적 제외)` · SK-09 옛 버전 문장 — 시작 커밋 판 값이 1)
- 양성 · 음성 대조(`ctl.sh` · `ctl2.sh` · `na.sh`, 끝 판 사본 한 군데를 바꾸고 되돌림):

  위 표의 「대조」 칸이 전부다. 조건마다 기대값에서 벗어난 값이 나왔다 — 0 을 기대하는 조건은 1 이상이, 1 을 기대하는 조건은 0 이, 같아야 하는 두 판 비교는 `0` · `SEAL_BROKEN` 이 나왔다.
  예행 변형 넷(`unsigned-mine` · `unsigned-shared` · `signed-outside` · `cross-phase`)은 `rehearse.sh` 가 만든 서명 없는 커밋 · 범위 밖 서명 커밋 · 두 킷 한 커밋이다.
  같은 측정을 `/bin/bash` 3.2.57 로 돌린 출력은 bash 5.3.9 출력과 한 글자도 다르지 않았다(두 판 폴더 이름이 든 오류 줄만 빼고 — 시작 커밋 판에는 이 계약이 없어 AR-01 이 파일을 못 연다)

## Skill

- [ ] SK-01: `docs/planning/prd-patterns.md` 에 `### 폐기한 결정 — 비범위 절 한 곳에 적는다` 절이 `### Google Design Sprint 산출물` 뒤 · `## 참고 링크 (전체)` 앞에 있고, 그 절이 열다섯 토큰(제목 · 두 형식의 절 이름 문장 · 원문 한 곳 · 다른 문서는 PRD 경로만 가리킴 · GitHub 예를 옮긴 것은 추론 · 체크 네 줄 · 「폐기는 영구 금지가 아니다」 · 흔적 칸은 이 킷의 운영 규칙 · PRD 없는 프로젝트는 정하지 않음 · `<…>` 출처 URL 셋)을 각 1 줄 담고, `## 참고 링크 (전체)` 에 새 URL 둘이 더해지고, 머리 설정이 `version: 0.2.0` · `last_updated: 2026-09-25` 다 (F20 · backend-family:P1 — 원칙 문서 먼저, planning-kaizen Gotcha 2) [exact, enumerated]
      (Given: 개정 파일 `end_sha:` 마지막 값이 정해진 뒤 · When: `type m >/dev/null || exit 2;` 뒤 `m SK-01` · Then: 네 줄이 `1` 열다섯 · `1` · `1 1` · `0.2.0 2026-09-25`.
       토큰은 `회귀 게이트` 절 `m.sh` 의 `SK-01)` 갈래에 글자 그대로 있다. 시작 커밋 판은 `0` 열다섯 · `0` · `0 0` · `0.1.0 2026-04-14`. 문장 삭제 대조: 토큰 열여섯 모두 출력이 바뀐다)
- [ ] SK-02: `planning-kit/skills/plan-prd/SKILL.md` 가 Gotcha 14 「**폐기한 결정은 비범위 절 한 곳에 네 칸으로 적는다**」 한 줄로 열두 토큰(번호 머리 · 두 형식의 표 자리와 네 칸 · 원문은 여기 하나이고 디자인 승인 기록 · 작업 계약 · 핸드오프는 경로만 · PRD 뒤에 나온 폐기도 이 표에 한 줄 · 흔적 칸은 치울 목록 · 되살려야 할 것 같으면 먼저 묻기 · 영구 금지 아님 · 어느 칸이 외부 근거이고 어느 칸이 킷 규칙인지 · 실측 `F20` · `docs/planning/prd-patterns.md` §폐기한 결정 가리킴 · 출처 URL 둘)을 담고, `# Gotchas` 번호가 1 ~ 14 로 이어진다 (F20 · backend-family:P1 (1)) [exact, enumerated]
      (측정: `type m >/dev/null || exit 2;` 뒤 `m SK-02` 두 줄이 `1` 열둘 · `1 2 3 4 5 6 7 8 9 10 11 12 13 14`. 시작 커밋 판은 `0` 열둘 · `1 2 3 4 5 6 7 8 9 10 11 12 13`.
       문장 삭제 대조: 토큰 열다섯 가운데 열넷이 떨어진다 — 나머지 하나(맨 Shape Up URL)는 첫 자리가 Gotcha 10 이라 그 자리가 지워졌고, Gotcha 14 안을 겨눈 토큰은 떨어진다)
- [ ] SK-03: plan-prd 의 세 틀이 같은 비범위 표를 갖는다 — (a) `### PR/FAQ 템플릿` 틀 안에 `## Non-goals (폐기한 결정 포함)` · 표 머리 `| 하지 않는 것 | 이유 | 범위 | 코드에 남은 흔적 |` · 구분선 · 예시 행 네 줄이 이어서 1 번 (b) `### Shape Up Pitch 템플릿` 틀 안에 `## No-gos` 와 같은 세 줄이 이어서 1 번 · 옛 줄 `- (명시적 제외)` 0 (c) `### Linear-style Spec 템플릿` 틀 안에 (a) 의 네 줄이 1 번이고 그 제목이 `## Proposal` 과 `## Milestones` 사이 (d) Step 2 표의 PR/FAQ 행 산출물 구조가 `보도자료(1p) + 내부 FAQ + 외부 FAQ + Non-goals`, Linear-style 행이 `Problem + Solution + Non-goals + Open questions + Milestones` 이고 파일 전체의 표 머리 줄이 3 (e) `## Step 4: 체크리스트 검증` 에 기존 「Non-goals 가 3개 이상인가」 와 새 두 항목(폐기한 결정마다 이유 · 범위 · 흔적 칸 · 흔적을 Solution · Proposal · Milestones · FAQ 에 새 요구로 옮기지 않음)이 각 1 (backend-family:P1 (2) · 근거 파일 §2 「내부 불일치」) [exact, enumerated]
      (Given: 개정 파일 `end_sha:` 마지막 값이 정해진 뒤 · When: `type m >/dev/null || exit 2;` 뒤 `m SK-03` · Then: 다섯 줄이 `prfaq=1` · `shapeup=1 old=0` · `linear=1 1` · `rows=1 1 heads=3` · `1 1 1`.
       표 네 줄은 `common.sh` 의 `TH` · `TS` · `TR` 이다. 시작 커밋 판은 `prfaq=0` · `shapeup=0 old=1` · `linear=0 0` · `rows=0 0 heads=0` · `1 0 0`.
       문장 삭제 대조: 틀마다 겨눈 토큰 넷을 포함해 열다섯이 떨어진다 — 제목 두 낱말만 첫 자리가 Gotcha 14 라 그대로다)
- [ ] SK-04: `planning-kit/skills/plan-stories/SKILL.md` `## Step 1: 입력 파싱` 에 「PRD 비범위 절(…)의 폐기한 결정과 겹치는 스토리는 만들지 않는다.」 와 「코드에 흔적이 남아 있어도 요구로 읽지 않는다 — 필요해 보이면 스토리를 쓰기 전에 사용자에게 묻는다 (plan-prd Gotcha 14)」 가 각 1 이고, `## Step 0: 자동 로드 (독립 단계)` 의 PRD 로드 줄이 그대로 1 · 그 절에 규칙 낱말 「겹치는」 이 0 이다 (backend-family:P1 (4) · Counterpart 소비면 · planning-kaizen Gotcha 8) [exact, enumerated]
      (측정: `type m >/dev/null || exit 2;` 뒤 `m SK-04` 두 줄이 `1 1` · `1 0`. 시작 커밋 판은 `0 0` · `1 0`. 문장 삭제 대조: 토큰 여섯 모두 출력이 바뀐다)
- [ ] SK-05: `planning-kit/skills/plan-data-model/SKILL.md` 의 `## Step 0: 리서치 문서 로드` 에 PRD 비범위 절 로드 문장(`common.sh` 의 `LOADP`)과 「이 단계에서 모델을 그리지 않는다.」 가 각 1 · 규칙 낱말 「겹치는」 이 0 이고(두 문장은 한 줄에 둔다 — AR-03 (c) 가 그 절에서 바뀐 줄을 1 로 센다), `## Step 1: Event Storming (사건 먼저)` 에 「Step 0 에서 읽은 폐기한 결정과 겹치는 이벤트 · 엔티티 · 필드는 모델에 넣지 않는다.」 와 「코드 · 데이터베이스에 흔적이 남아 있어도 요구로 읽지 않는다 — 필요해 보이면 그리기 전에 사용자에게 묻는다 (plan-prd Gotcha 14).」 가 각 1 이며 그 규칙 줄이 이벤트 나열 줄(「PRD/플로우에서 **과거형 이벤트**」)보다 앞이다 (backend-family:P1 (3) · Counterpart 소비면 · planning-kaizen Gotcha 8) [exact, enumerated]
      (측정: `type m >/dev/null || exit 2;` 뒤 `m SK-05` 세 줄이 `1 1 0` · `1 1` · `1`. 시작 커밋 판은 `0 0 0` · `0 0` · `0`. 문장 삭제 대조: 토큰 일곱 모두 출력이 바뀐다)
- [ ] SK-06: `planning-kit/skills/plan-flow/SKILL.md` 의 `## Step 0: 리서치 문서 로드` 에 같은 로드 문장과 「이 단계에서 다이어그램을 그리지 않는다.」 가 각 1 · 「겹치는」 이 0 이고(두 문장은 한 줄에 둔다 — AR-03 (c) 가 그 절에서 바뀐 줄을 1 로 센다), `## Step 2: 작성` 에 「Step 0 에서 읽은 폐기한 결정과 겹치는 화면 · 분기 · 단계는 그리지 않는다.」 와 「코드에 흔적이 남아 있어도 요구로 읽지 않는다 — 필요해 보이면 그리기 전에 사용자에게 묻는다 (plan-prd Gotcha 14).」 가 각 1 이며 그 규칙 줄이 `### User Flow (flowchart)` 보다 앞이다 (backend-family:P1 (3) · Counterpart 소비면 · planning-kaizen Gotcha 8) [exact, enumerated]
      (측정: `type m >/dev/null || exit 2;` 뒤 `m SK-06` 세 줄이 `1 1 0` · `1 1` · `1`. 시작 커밋 판은 `0 0 0` · `0 0` · `0`. 문장 삭제 대조: 토큰 일곱 모두 출력이 바뀐다)
- [ ] SK-07: `planning-kit/skills/plan-audit/SKILL.md` Step 3 표의 카테고리 3 행(`| 3 | Non-goals |` 로 시작하는 줄, 1 줄)이 기존 「최소 3개 명시 (Shape Up 의 no-gos / rabbit holes 포함)」 에 더해 「+ 폐기한 결정마다 이유 · 범위 · 코드에 남은 흔적 칸」 · 「+ stories · flow · data-model 산출물에 폐기한 항목이 다시 들어가지 않음 (planning-reviewer Step 3 확인)」 · 참조 문서 칸 `| prd-patterns.md §Shape Up / §폐기한 결정 |` · `[Shape Up §6](https://basecamp.com/shapeup/1.5-chapter-06)` 을 담고, 그 행의 칸 수가 표 머리와 같다 (backend-family:P1 선택 사항 · Counterpart 소비면) [exact, enumerated]
      (측정: `type m >/dev/null || exit 2;` 뒤 `m SK-07` 두 줄이 `1 1 1 1 1` · `cols=7 7 rows=1`. 시작 커밋 판은 `1 0 0 0 0` · `cols=7 7 rows=1`.
       문장 삭제 대조: 토큰 일곱 가운데 여섯이 떨어진다 — 맨 `[Shape Up §6](…)` 은 첫 자리가 카테고리 2 행이고, 카테고리 3 행을 겨눈 토큰은 떨어진다)
- [ ] SK-08: `planning-kit/agents/planning-reviewer.md` 원칙 매핑의 `| Non-goals |` 행이 `| prd-patterns.md §Shape Up (rabbit holes/no-gos), §폐기한 결정 |` 과 `[Shape Up §6](https://basecamp.com/shapeup/1.5-chapter-06)` 을 담고, `### Non-goals 카테고리 — 폐기한 항목이 다시 들어갔는지` 절이 `### 카테고리별 원칙 매핑` 뒤 · `## Step 4: 최종 Verdict (합성)` 앞에 있으며 일곱 토큰(제목 · 뒤 단계 세 산출물을 Grep · 다시 넣었으면 FAIL · 제외나 질문이면 PASS 근거 · 같은 낱말이 PRD 비범위 표에도 걸려야 함 · 뒤 단계 0 매치를 그것만으로 PASS 근거로 쓰지 않음(Step 2 공허한 증거 분기) · 세 산출물이 없으면 건너뛰고 적음)을 각 1 줄 담고, `tools: Read, Grep, Glob` 줄이 그대로다 (backend-family:P1 선택 사항 · Counterpart 소비면 · 근거 파일 §2 「두 파일을 반드시 함께」) [exact, enumerated]
      (측정: `type m >/dev/null || exit 2;` 뒤 `m SK-08` 네 줄이 `1 1` · `1` 일곱 · `1` · `1`. 시작 커밋 판은 `0 0` · `0` 일곱 · `0` · `1`. 문장 삭제 대조: 토큰 열하나 모두 출력이 바뀐다)
- [ ] SK-09: Mermaid 12 현행화 — (a) `docs/planning/flows.md` 에 옛 문장 「아래 예시는 공식 문법 10.x+ / 11.x 계열에서 유효한 형태다.」 가 0 이고 `### Mermaid Flowchart 공식 패턴` 에 「아래 예시는 flowchart 공식 문서의 문법을 따른다.」 · 「2026-09-24 에 확인한 Mermaid 최신 안정판은 12.0.0(2026-09-10 공개)이고, 이 예시를 12 에서 렌더해 보지는 않았다.」 (확인 날짜는 근거 파일 `collected:` 값) · 출처 `- <https://github.com/mermaid-js/mermaid/releases/tag/mermaid%4012.0.0>` 이 각 1, `## 참고 링크 (전체)` 에 같은 URL 줄 1 (b) `docs/planning/data-modeling.md` `### Mermaid erDiagram 공식 패턴` 에 「Mermaid 12.0.0(2026-09-10 공개)부터 ERD 의 기본 배치가 Dagre 에서 ELK 로, 기본 모양(theme · look)도 바뀌었다」 · 「렌더 결과를 비교할 때는 렌더러 버전을 함께 적는다」 · 같은 URL 줄이 각 1, 참고 링크에 1 (c) 두 파일 머리 설정이 `0.1.1` · `2026-09-25` (d) `planning-kit/skills/plan-sync-github/SKILL.md` 가 편집 전과 글자 그대로 — GitHub 문서 버전 날짜는 바꾸지 않는다 (근거 파일 §3 · §4 권장 9) [exact, enumerated]
      (측정: `type m >/dev/null || exit 2;` 뒤 `m SK-09` 여섯 줄이 `old=0` · `1 1 1` · `1` · `1 1 1` · `1` · `0.1.1 2026-09-25 0.1.1 2026-09-25 sync_same=1`.
       시작 커밋 판은 `old=1` · `0 0 0` · `0` · `0 0 0` · `0` · `0.1.0 2026-04-14 0.1.0 2026-04-14 sync_same=1`. 양성 대조: plan-sync-github 끝에 빈 줄 하나를 더한 사본에서 `sync_same=0` · flows 버전 문장에서 확인 날짜 「2026-09-24 에 확인한 」 만 지운 사본에서 둘째 줄 `1 0 1`.
       문장 삭제 대조: 토큰 열둘 가운데 열하나(틀마다 겨눈 URL 넷 포함)가 떨어진다 — 나머지 하나는 0 을 기대하는 옛 문장이라 끝 판에 없다)
- [ ] SK-10: `docs/planning/research-log.md` 맨 위 항목이 `## [2026-09-24] — Phase 11 kaizen (폐기한 결정 기록 자리)` 이고 그 절이 열 토큰(제목 · 처리 배정표 두 키 · 결정 소제목 · 세 칸에서 넷으로 늘린 까닭 · `### 현행화` · `2022-11-28` 지원 기한 · Mermaid 12.0.0 URL · `### 명시적 비범위` · Design Sprint 틀 없음 · 미검증 사본은 다음 사이클 Phase 3 뒤)을 각 1 줄 담고, `## [2026-08-13]` 부터 끝까지가 편집 전과 글자 그대로이며, 머리 설정이 `version: 1.1.0` · `last_updated: 2026-09-25` 다 (planning-kaizen Step 5 기록 · 러닝북 킷 전용 로그) [exact, enumerated]
      (측정: `type m >/dev/null || exit 2;` 뒤 `m SK-10` 두 줄이 `1` 열 · `first=1 old_same=1 1.1.0 2026-09-25`. 시작 커밋 판은 `0` 열 · `first=0 old_same=1 1.0.0 2026-08-13`.
       양성 대조: 2026-08-13 항목 한 줄을 고친 사본에서 `old_same=0`. 문장 삭제 대조: 토큰 열 모두 출력이 바뀐다)

## Script

- [ ] SC-00: N/A (Script 카테고리는 `release.sh` 연동 · 버전 올림 · `marketplace.json` 갱신이다. 이 Phase 는 그 파일을 건드리지 않는다 — 공유 파일은 Final 몫. 측정: `type my >/dev/null || exit 2;` 뒤 `my | grep -cE '^(scripts/release\.sh|\.claude-plugin/marketplace\.json|[^/]+/\.claude-plugin/plugin\.json)$'` 이 0. 양성 대조: 예행 변형 `signed-outside` 에서 1)

## Error

- [ ] ER-01: 열 파일에 새로 생긴 URL 과 `.harness/.meta/kaizen-0924/phase11-notes.md` 의 URL 이 전부 이 Phase 의 외부 근거 파일 `.harness/.meta/evidence/phase11.md` 에 있다 — 열 파일은 파일마다 편집 전 판과 비교한다 (러닝북 — 근거 파일에 없는 URL 을 지어내지 않는다 · notes 킷 로그의 출처 URL 은 근거 파일에서만) [exact, enumerated]
      (측정: `type m >/dev/null || exit 2;` 뒤 `m ER-01` 두 줄이 `0` · `0`. notes 가 `$END` 판에 없으면 둘째 줄이 `NOTES_MISSING` 이라 FAIL 이다.
       양성 대조: 끝 판 prd-patterns 끝에 `https://example.invalid/x` 를 더한 사본에서 첫 줄 `1`, notes 끝에 더한 사본에서 둘째 줄 `1`, notes 를 지운 사본에서 둘째 줄 `NOTES_MISSING`)
- [ ] ER-02: 열 파일에 더한 줄에 번역투 6 종(`tone-kit/references/locale-korean.md` §2 치환표의 grep 열)이 0 건이고, 특정 앱 이름 · 특정 화면 도구 서버 이름(`fit-?pal` · `fit_pal` · `flutter[-_]playwright` · `playwright-mcp` · `chrome-devtools-mcp`, 대소문자 무시)이 0 건이다 (러닝북 말투 · 문서 규칙) [exact]
      (측정: `type m >/dev/null || exit 2;` 뒤 `m ER-02` 가 `added=N k02=0 names=0` 이고 N 이 1 이상. 예행 판 `added=104 k02=0 names=0`.
       양성 대조: plan-flow 끝에 「이 값이 적용된다」 를 더한 사본에서 `k02=1`, 「fit-pal 에서 본 일」 을 더한 사본에서 `names=1`)
- [ ] ER-03: 이 Phase 범위 밖 반대편을 명시적 미완으로 넘기고 건드리지 않는다 — `.harness/.meta/kaizen-0924/phase11-notes.md` 가 `$END` 에 커밋돼 있고 (a) 처리 배정표 키 `F20` · `backend-family:P1` 과 러닝북이 적게 한 절 머리 일곱(`## 바꾼 파일` · `## 반영한 처리 배정표 키` · `## 미반영 키와 사유` · `## 넘기는 것` · `## changelog 한 단락` · `## 킷 로그 한 단락` · `## 다음 사이클 메모`)이 각각 1 줄 이상 (b) `## 넘기는 것` 절 안에 넘김 다섯 — `harness/skills/sprint/SKILL.md` (다음 사이클 Phase 4 — 재검증 블록이 PRD 비범위 절 경로를 읽는 줄 · PRD 없는 프로젝트의 자리) · `planning-kit/agents/planning-reviewer.md` (다음 사이클 Phase 3 뒤 — 미검증 사본을 2026-08-13 개정 판으로 · `:151` 빈 가리킴) · `docs/planning-kit/prd-patterns.html` (Final F2 — flows · data-modeling 페이지 포함) · `plugin.json` (Final — planning-kit 버전) · `user-setup:P6` (카이젠 뒤 사용자 설정 — 핸드오프 틀은 PRD 경로만 가리킨다) 가 각각 1 줄 이상 (c) `## 미반영 키와 사유` 절 안에 `2026-03-10` (GitHub 문서 버전 날짜) · `Design Sprint` (틀 없음) · `user-setup:P10` (F20 의 한 나라 우선 판단 — 처리 배정표가 킷 밖으로 보냈다) 이 각각 1 줄 이상이고, (d) 구간 안에서 공유 파일 · 다른 Phase 파일을 건드린 커밋 가운데 다른 Phase 서명이 없는 커밋이 0 개다 [exact, enumerated]
      (Given: BUILD 가 notes 를 커밋하고 개정 파일에 그 sha 로 `end_sha:` 를 덧붙인 뒤 · When: `type m >/dev/null || exit 2; type not_other >/dev/null || exit 2;` 뒤 `m ER-03` · Then: 다섯 줄이 `notes_committed=1` · 아홉 값 모두 `1` 이상 · 다섯 값 모두 `1` 이상 · 세 값 모두 `1` 이상 · `0`.
       (d) 의 경로는 `m.sh` `ER-03)` 갈래의 `not_other` 인자 열여섯이다 — 서명 줄 목록이 아니라 경로로 직접 세므로 서명을 빠뜨린 커밋도 보인다. 다른 Phase 서명이 달린 커밋은 그 Phase 몫이라 뺀다.
       봉인 전 실측: notes 모의본을 커밋한 예행 판 `notes_committed=1` · `2 1 1 1 1 1 1 1 1` (`F20` 이 반영 표와 미반영 절 두 줄에 있다) · `1` 다섯 · `1 1 1` · `0`. 음성 대조: 넘김 표의 `harness/skills/sprint/SKILL.md` 줄을 지우고 같은 경로를 `## 반영한 처리 배정표 키` 절 문장에만 남긴 사본 → 셋째 줄 첫 값 `0` ·
       미반영 절의 `user-setup:P10` 줄을 지운 사본 → 넷째 줄 `1 1 0` · 그 줄을 `## 다음 사이클 메모` 절로만 옮긴 사본 → 넷째 줄 `1 1 0`.
       양성 대조: 변형 `unsigned-mine` · `unsigned-shared` · `signed-outside` · `cross-phase` 모두 다섯째 줄 `1`)

## Architecture

- [ ] AR-01: 이 Phase 의 변경이 허용 경로 안에 머물고, 범위 선언 블록이 그 경로와 같으며, 이 계약이 봉인돼 있다 [exact, enumerated]
      (Given: BUILD 가 개정 파일에 `end_sha:` 를 적은 뒤 · 이 Phase 커밋 메시지마다 서명 줄 `Kaizen-Phase: kaizen-0924-p11-planning-kit` · When: `type m >/dev/null || exit 2; type unsigned_on >/dev/null || exit 2; type verify_seal >/dev/null || exit 2;` 뒤 `m AR-01` · Then: 여섯 줄이 —
       ① `0` — `planning-kit/` · `docs/planning/` 를 건드린 구간 안 커밋이 전부 서명했다(이 구간에 두 폴더를 고칠 수 있는 Phase 는 11 하나다)
       ② `0 10` — 서명 커밋이 건드린 `.harness/` 밖 경로 가운데 열 파일 밖이 0 개, 열 파일이 전부 있다
       ③ `0` — `harness/references/contract-schema.md` §`.harness/` 범위 조건 의 권장 형태로 `.harness/` 의 계약 전부에 `verify_seal` 을 돌려 이 Phase 몫 `SEAL_BROKEN` 이 0 개
       ④ `SEAL_OK` — `$END` 판의 이 계약이 봉인돼 있다(`SEAL_ABSENT` 는 봉인을 건너뛴 것이라 FAIL)
       ⑤ `scope_same=1` — `## 범위 경계` 절 `# sprint-scope` 블록의 `.harness/` 밖 줄이 `FILES` 열 줄과 같다 ⑥ `1` — 그 블록에 `.harness/` 줄이 하나 있다.
       봉인 전 실측: 예행 판 `0` · `0 10` · `0` · `SEAL_OK` · `scope_same=1` · `1`. 양성 대조: 변형 `unsigned-mine` ① `1` · 변형 `signed-outside` ② `1 10` · 변형 `cross-phase` ② `2 10` ·
       예행 작업 폴더 계약의 조건 줄 한 글자를 바꾼 사본 ③ `1` · 끝 판 계약의 조건 줄 한 글자를 바꾼 사본 ④ `SEAL_BROKEN`)
- [ ] AR-02: 새 문장이 가리키는 자리가 실제로 있다 — (a) plan-prd Gotcha 14 가 가리키는 `docs/planning/prd-patterns.md` 에 `### 폐기한 결정 — ` 제목 1 (b) 뒤 단계 세 스킬이 가리키는 plan-prd 에 `14. **폐기한 결정` 줄 1 (c) plan-stories · plan-data-model · plan-flow 세 파일의 `(plan-prd Gotcha 14)` 가 합쳐 3 (d) plan-audit 행이 가리키는 「planning-reviewer Step 3 확인」 — reviewer `## Step 3: 카테고리별 Rule-by-Rule 판정` 안에 새 소제목 1 (e) reviewer 새 절이 가리키는 Step 2 「**공허한 증거 분기」 1 (f) `§폐기한 결정` 을 적은 파일이 plan-prd · plan-audit · reviewer 셋 (g) Counterpart — Phase 6 가 넣은 `design-kit/references/visual-change-protocol.md` 문장 「제품 요구 수준의 폐기 결정(기능·설정 항목을 없앤다는 결정)은 이 기록에서 새로 정하지 않는다」 가 그대로 1 [exact, enumerated]
      (측정: `type m >/dev/null || exit 2;` 뒤 `m AR-02` 가 `1 1 3 1 1 3 1`. 알려진 답: 시작 커밋 판은 새로 생기는 자리((a) · (b) · (c) · (d) · (f))만 없어 `0 0 0 0 1 0 1`.
       양성 대조: prd-patterns 제목을 `### 폐기 — ` 로 바꾼 사본에서 첫 값 `0` · design-kit 문장을 「제품 수준 폐기 결정」 으로 바꾼 사본에서 마지막 값 `0`)
- [ ] AR-03: 킷 안 짝과 복제본이 그대로다 (planning-kaizen Gotcha 7 · 8 · 9) — (a) planning-reviewer 의 `# Canonical Unverified-Evidence Protocol (정본 복제)` 절 · `## Canonical User-Reported Failure Protocol` 절, plan-audit Gotcha 9 줄 · `## Step 5: Verdict 결정` 절이 각각 편집 전과 글자 그대로 (b) plan-audit Step 3 표의 카테고리 행과 reviewer 원칙 매핑 행이 둘 다 12 (c) Step 0 절에서 바뀐(더하거나 지운) 비지 않은 줄이 plan-prd · plan-stories · plan-audit 는 0, plan-data-model · plan-flow 는 1 (로드 문장 하나 — SK-05 · SK-06 이 그 문장을 잰다). 제목이 바뀌어 절을 못 찾으면 편집 전 줄이 전부 지운 줄로 세어져 0 이 되지 않는다 [exact, enumerated]
      (측정: `type m >/dev/null || exit 2;` 뒤 `m AR-03` 세 줄이 `1 1 1 1` · `12 12` · `0 0 0 1 1`. 시작 커밋 판은 `1 1 1 1` · `12 12` · `0 0 0 0 0`.
       양성 대조: reviewer 기준 원본 사본 조항 1 의 한 구절을 지운 사본에서 첫 줄 `0 1 1 1` · plan-prd Step 0 의 3 번 항목 자리에 한 줄을 끼운 사본에서 셋째 줄 `3 0 0 1 1` · plan-prd Step 0 제목을 `## Step 0: 로드` 로 바꾼 사본에서 셋째 줄 `6 0 0 1 1` · plan-audit Step 0 의 3 번 줄을 지운 사본에서 셋째 줄 `0 0 1 1 1` · plan-audit 표에 행을 하나 더한 사본에서 둘째 줄 `13 12`)

## Anti-patterns

- [ ] AP-01: 버전을 하드코딩하지 않는다 — plugin.json에서 읽어야 한다. 이번 변경에 적용: 열 파일에 더한 줄에 planning-kit `plugin.json` 의 `version` 값(`$END` 판에서 읽는다)이 0 건이다 — 이 Phase 는 킷 버전을 적지 않고 Final 이 올린다 [exact]
      (측정: `type m >/dev/null || exit 2;` 뒤 `m AP-01` 이 `version=0.5.1 0`. 양성 대조: plan-prd 끝에 「버전 0.5.1」 을 더한 사본에서 둘째 값 `1`. 문서 머리 설정의 새 값(0.2.0 · 0.1.1 · 1.1.0)은 이 문자열을 담지 않는다 — 봉인 전 실측 0)
- [ ] AP-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수 (```` ```text, ```bash, ```yaml ```` 등). 판정 권위는 validate-plugin V6 상태기계다 — 여는/닫는 fence 가 동형이라 줄 단위 정규식으로는 판정 불가. 이번 변경에 적용: 이 Phase 는 펜스 줄을 더하지 않는다 — 열 파일에 더한 줄에 펜스 줄(```` ``` ```` · `~~~`)이 0 이고, planning-kit 쪽은 DG-05 의 V6 가 함께 본다(`docs/planning/` 은 V6 가 읽지 않는다) [exact]
      (측정: `type m >/dev/null || exit 2;` 뒤 `m AP-03` 이 `0`. 양성 대조: prd-patterns 끝에 `` ``` `` 한 줄을 더한 사본에서 `1`)
- [ ] AP-04: SKILL.md / agents/*.md frontmatter 에서 name 필드 누락 — validate-plugin V1 FAIL. 이번 변경에 적용: 고친 SKILL.md 다섯(plan-prd · plan-stories · plan-data-model · plan-flow · plan-audit)과 planning-reviewer 의 첫 frontmatter 블록이 편집 전과 글자 그대로 같고 `name: <폴더 또는 파일 이름>` 줄이 1 개씩이다 — 그래서 README AUTO 구간과 트리거 설명(planning-kaizen Gotcha 3)이 읽는 값도 바뀌지 않는다 [exact]
      (측정: `type m >/dev/null || exit 2;` 뒤 `m AP-04` 가 `1/1` 여섯. 음성 대조: plan-flow `description` 첫 줄 한 글자를 바꾼 사본에서 넷째 값 `0/1`)

## Reusability

- [ ] RE-01: N/A (재사용 단위 코드 — 컴포넌트 · 함수 · 모듈 — 가 없다. 변경 파일이 문서뿐이다. 측정: `printf '%s\n' "${FILES[@]}" | grep -cv '\.md$'` 이 0)
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다. 이번 변경에 적용: 규칙 본문은 킷 안에서 plan-prd 한 곳이다. 단 plan-audit 카테고리 3 행은 판정 기준이라 칸 이름을 적으므로(SK-07) (c) 에서 뺀다. (a) 「치울 목록」 설명을 담은 planning-kit 파일이 plan-prd 하나 (b) 비범위 표 머리 `| 하지 않는 것 | 이유 | 범위 | 코드에 남은 흔적 |` 를 담은 planning-kit 파일이 plan-prd 하나 (c) plan-stories · plan-data-model · plan-flow · planning-reviewer 에 더한 줄이 칸 목록(「이유 · 범위」)이나 「치울 목록」 을 다시 적지 않고 `(plan-prd Gotcha 14)` · `§폐기한 결정` 을 가리킨다 [exact, enumerated]
      (측정: `type m >/dev/null || exit 2;` 뒤 `m RE-02` 가 `planning-kit/skills/plan-prd/SKILL.md | planning-kit/skills/plan-prd/SKILL.md | 0`. 시작 커밋 판은 ` |  | 0`.
       양성 대조: plan-flow 에 「흔적은 치울 목록이다」 를 더한 사본에서 첫 칸에 plan-flow 가 더해지고, plan-stories 에 「이유 · 범위 칸」 을 더한 사본에서 셋째 값 `1`, plan-flow 에 표 머리를 더한 사본에서 둘째 칸에 plan-flow 가 더해진다)

## Diagnostics

- [ ] DG-01: N/A (`commands.analyze` 는 `bash -n scripts/release.sh` 라 `scripts/release.sh` 만 잰다 — 이번 변경 파일과 교집합 0 개. 측정: `type my >/dev/null || exit 2;` 뒤 `my | grep -c '^scripts/release.sh$'` 이 0. 실제 검사는 DG-02 · DG-05)
- [ ] DG-02: IDE diagnostics 워닝/인포 0개 (`diagnostics.ide_exclude` 값 `[]`) — 이번 변경에 적용: 편집기 마크다운 확장과 같은 조건(markdownlint-cli2 0.23.2 · MD013 끔)으로 열 파일의 **더한 줄**에 걸린 경고가 0 이다. 편집 전부터 있던 경고는 `범위 경계` 절에 적은 대로 범위 밖이다 [exact]
      (측정: `type m >/dev/null || exit 2;` 뒤 `m DG-02` 의 열 줄이 모두 `new_warnings=0` 으로 끝나고 `LINT_NOT_RUN` 줄 0.
       봉인 전 실측: `회귀 게이트` 절 표. 첫 초안은 이 폴더의 원래 꼴(제목 아래 빈 줄 없음 · 맨 URL)을 따라 새 경고 18 을 냈고, 빈 줄과 `<…>` URL 로 고쳐 0 이 됐다.
       양성 대조: prd-patterns 끝에 `#bad heading` 을 더한 사본에서 그 줄 `new_warnings=1`)
- [ ] DG-03: N/A (`commands.test` 는 `bash scripts/release.sh 2>&1 || true` 라 `scripts/release.sh` 만 잰다 — 교집합 0 개. 측정: DG-01 과 같은 명령 `type my >/dev/null || exit 2;` 뒤 `my | grep -c '^scripts/release.sh$'` 이 0. 실제 검사는 DG-05)
- [ ] DG-04: N/A (구동할 앱 · 서버가 없다 — 변경이 문서뿐이다. 측정: `type my >/dev/null || exit 2;` 뒤 `my | grep -cE '\.(dart|ts|tsx|js|rs|go|py|sh)$'` 이 0. 양성 대조: 같은 `grep -cE` 에 `a/b.rs` · `c.sh` · `d.md` 세 줄을 넣으면 2)
- [ ] DG-05: 저장소 검사가 이 킷을 문제로 가리키지 않는다 — `$END` 판을 git 저장소로 만든 사본에서 (a) `scripts/validate-plugin.py planning-kit` 출력에 `V1` ~ `V10` 열 줄이 있고 `— OK` · `— SKIP (no templates/)` 로 끝나지 않는 줄이 0 이며 종료 코드 0 (planning-kaizen Gotcha 5) (b) `scripts/sync-docs.py --check-only` 출력에 `  planning-kit/README.md: 동기화됨` 줄이 1 (c) `scripts/check-stale-values.py` 가 소스 폴더를 읽었고(`검사 범위:` 줄 1) 종료 코드 0 또는 1 이며 출력에 열 파일 경로가 0 건이다. 킷 전체를 보는 검사는 이 킷 몫의 줄만 센다 — 같은 구간에 다른 Phase 가 올린 변경 때문에 떨어지지 않게 한다 [exact]
      (측정: `type m >/dev/null || exit 2;` 뒤 `m DG-05` 세 줄이 `10 0 rc=0` · `sync_docs_rc=R 1` (R 은 판정하지 않는다 — 다른 킷 README 몫) · `stale_rc=S ran=1 0` (S 는 0 또는 1).
       봉인 전 실측: 예행 판 `10 0 rc=0` · `sync_docs_rc=0 1` · `stale_rc=0 ran=1 0`. 음성 대조: plan-flow 의 `name: plan-flow` 를 `nam:` 으로 깬 사본에서 첫 줄 `10 1 rc=2`.
       양성 대조: flows.md 끝에 등록된 옛 값 `1m30s` 를 더한 사본에서 셋째 줄 `stale_rc=1 ran=1 1`)
- [ ] DG-06: `python3 scripts/validate-post-kaizen.py --since d88c35a70ccb88faf7bea3f57cf1f8c5f51b0279` 출력의 `scope-isolation` · `doc-contracts` 줄이 `FAIL` · `ERROR` 가 아니다. `docs-site-regen` 은 Final F2 몫이라 판정에서 뺀다. 다른 Phase 커밋 때문에 `scope-isolation` 이 FAIL 이면 `--verbose` 위반 커밋 목록을 1 개 이상 읽었고 그 가운데 서명 줄 커밋이 0 개일 때, `doc-contracts` 가 FAIL · ERROR 이면 `validate-doc-contracts.py -v` 가 검사한 경로를 1 개 이상 읽었고 그 가운데 이 Phase 서명 커밋이 건드린 경로가 0 개일 때 이 조건은 PASS 다 — 둘 다 근거에 다른 Phase 몫이라고 적는다 [exact]
      (Given: 작업 폴더에서 `$END` 이후 커밋이 있어도 된다 — 검사는 `HEAD` 까지 보지만 판정은 이 Phase 서명 커밋만 센다 · When: `type m >/dev/null || exit 2;` 뒤 `m DG-06` · Then: 네 줄이 `scope-isolation: PASS` · `doc-contracts: PASS` · `doc_checked=N doc_mine=0` · `violators=V mine=0` 이고 N 이 1 이상. 위 가르기로 PASS 를 줄 때만 첫 두 줄에 `FAIL` 이 있어도 되며, scope-isolation 이 `FAIL` 이면 V 가 1 이상이어야 한다(목록을 못 읽으면 mine 이 조용히 0 이 되므로).
       봉인 전 실측: 예행 판 `scope-isolation: PASS` · `doc-contracts: PASS` · `doc_checked=2 doc_mine=0` · `violators=0 mine=0`. 양성 대조: 변형 `cross-phase` 에서 `scope-isolation: FAIL` · `violators=1 mine=1`)
