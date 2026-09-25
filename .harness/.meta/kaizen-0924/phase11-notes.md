# 카이젠 2026-09-24 Phase 11 (planning-kit) — notes

- 계약: `.harness/sprint-contract-kaizen-0924-p11-planning-kit.md` (조건 28 · 기능 조건 18, 봉인 `sha256:4a38762119ffd6a8` · `locked_at` 2026-09-25 09:13)
- 개정: `.harness/sprint-amendments-kaizen-0924-p11-planning-kit.md` (조건 변경 0 건, `end_sha` 만)
- 검토: `.harness/.meta/kaizen-0924/phase11-review.md` (1 회차 CHANGES 필수 둘 · 권고 일곱은 초안이 반영, 2 회차 APPROVE. 2 회차 「새로 본 것」 1 번 — 범위 경계에 APPROVE 적기 — 은 BUILD 가 봉인 전에 넣었다)
- 시작 커밋 `d88c35a70ccb88faf7bea3f57cf1f8c5f51b0279`
- 계약 피드백: `~/.harness/feedback/contract/5a24cc99-2026-09-25T091602-de8c7935-34207.yaml` (`verify-feedback.sh` PASS). 초안은 `.harness/feedback-draft-p11.yaml` 로 갈라 썼다

## 커밋

| 커밋 | 내용 | 파일 |
| --- | --- | --- |
| `32f08a2` | 봉인 커밋 | 계약 1 개 |
| `bbdebaf` | 폐기한 결정 원칙 · Mermaid 12 현행화 · research-log 항목 | `docs/planning/` 넷 |
| `7de513b` | plan-prd 비범위 표 · 뒤 단계 셋 · 감사 둘 | `planning-kit/` 여섯 |
| `efa13d6` | 개정 파일에 `end_sha` (`7de513b`) | 개정 1 개 |
| 이 파일의 커밋 | notes · 검토 기록 | `.harness/` 두 개 |
| 그다음 커밋 | 개정 파일에 notes 커밋 sha 로 `end_sha` 한 줄 더 | 개정 1 개 |

모든 커밋 메시지 끝 문단에 `Kaizen-Phase: kaizen-0924-p11-planning-kit` 줄이 있다. 구현 커밋은 `git add -- <파일…> && git commit -o -- <파일…>` 로 내 경로만 실었다.
**FIX 가 커밋을 더할 때도 서명 줄을 넣고, 개정 파일에 `end_sha:` 줄을 덧붙인다.**

구현은 초안의 모의 치환(스크래치 `p11d/mock.py`, 지문 앞 16 자리 `593fb476788192fb`)을 작업 폴더에 그대로 돌렸다. 돌리기 전에 열 파일이 시작 커밋과 `HEAD` 사이에 바뀌지 않았고
미커밋 변경도 없는 것을 봤다. 같은 스크립트를 `HEAD` 판 새 사본에 먼저 돌려 `mock applied 27` 을 본 뒤 작업 폴더에서도 `mock applied 27` · 종료 코드 0 이 나왔고,
열 파일이 새 사본 결과와 `cmp` 로 같았다.
28 조건 측정은 봉인 커밋 판 계약에서 뗀 묶음으로 돌렸다 — 스크래치 `p11b/ks/`(`common.sh` · `m.sh` · `new-warnings.sh`, 2 회차 검토가 자기 추출본과 같다고 확인한 DRAFT 의 `p11d/k5/` 와 `cmp` 로 같다) ·
`p11b/run.sh`(공통 정의를 `.` 로 읽고 `TMPDIR` 를 스크래치로 둔 뒤 `type` 으로 도우미 다섯을 확인하고 `m <조건 ID>`, N/A 넷은 계약 괄호의 명령). QA 가 같은 묶음을 다시 돌릴 수 있다.

## 바꾼 파일

- `docs/planning/prd-patterns.md` 0.1.0 → 0.2.0 — `### 폐기한 결정 — 비범위 절 한 곳에 적는다` 절(요약 · 근거 두 문단 · 체크 넷 · 적용 시점 · 한계 · 출처 셋)을 Design Sprint 절 뒤에, 참고 링크 둘
- `docs/planning/flows.md` 0.1.0 → 0.1.1 — 「10.x+ / 11.x 계열에서 유효」 문장을 2026-09-24 확인 기준 Mermaid 12.0.0 사실과 「12 에서 렌더해 보지는 않았다」 로, 출처 · 참고 링크
- `docs/planning/data-modeling.md` 0.1.0 → 0.1.1 — erDiagram 절 한계에 ERD 기본 배치 Dagre → ELK · 기본 모양 변경과 렌더러 버전을 함께 적으라는 말, 출처 · 참고 링크
- `docs/planning/research-log.md` 1.0.0 → 1.1.0 — `## [2026-09-24] — Phase 11 kaizen (폐기한 결정 기록 자리)` 항목(결정 · 현행화 · 명시적 비범위)
- `planning-kit/skills/plan-prd/SKILL.md` — Gotcha 14, Step 2 표 PR/FAQ · Linear-style 두 행에 Non-goals, 세 틀에 같은 네 칸 비범위 표(Shape Up 은 `## No-gos` 제목 유지), Step 4 두 항목
- `planning-kit/skills/plan-stories/SKILL.md` — Step 1 한 줄(겹치는 스토리는 만들지 않고 먼저 묻는다)
- `planning-kit/skills/plan-data-model/SKILL.md` — Step 0 로드 한 줄(그리지 않는다), Step 1 규칙 한 줄(이벤트 나열 앞)
- `planning-kit/skills/plan-flow/SKILL.md` — Step 0 로드 한 줄, Step 2 규칙 한 줄(User Flow 앞)
- `planning-kit/skills/plan-audit/SKILL.md` — Step 3 카테고리 3 행(폐기한 결정의 칸 · 뒤 단계 재등장 · §폐기한 결정 · Shape Up §6)
- `planning-kit/agents/planning-reviewer.md` — 원칙 매핑 Non-goals 행, Step 3 끝 `### Non-goals 카테고리 — 폐기한 항목이 다시 들어갔는지`

스킬 · 에이전트 머리 설정은 여섯 모두 그대로다(AP-04). planning-kit README 는 건드리지 않았다 — `sync-docs.py --check-only` 는 「모든 README가 동기화 상태입니다」.
planning-kit 에는 평가 사례 파일(`evals/`)과 시험 스크립트가 없어 더한 시험이 없다 — `.github/workflows/ci.yml` 에 넣을 줄도 없다.

## 반영한 처리 배정표 키

| 키 | 반영 |
| --- | --- |
| `F20` | 폐기한 결정의 원문 자리를 그 기능 PRD 의 비범위 절 하나로 정했다(PR/FAQ · Linear-style `## Non-goals (폐기한 결정 포함)`, Shape Up `## No-gos`). 나머지 자리(디자인 승인 기록 · 작업 계약 · 핸드오프)는 이 경로를 가리킨다 (SK-01 · SK-02). 한 나라 우선 판단은 아래 미반영 절 |
| `backend-family:P1` | plan-prd Gotcha 14 · 세 틀 · Step 2 표 · Step 4 (SK-02 · SK-03), 뒤 단계 셋 plan-stories · plan-data-model · plan-flow (SK-04 ~ SK-06), 선택 사항이던 감사 둘 plan-audit · planning-reviewer (SK-07 · SK-08). 칸은 세 칸 제안에 범위 칸을 더해 넷 — 근거 파일 §4 권장 8 |
| Phase 4 · 6 · 7 넘김 (`F20`) | 기록 자리를 이 Phase 가 정했다. design-kit 규약 §4 는 이미 「결정이 적힌 파일 경로를 폐기 칸에 적는다」 라 고치지 않았고, 그 문장이 그대로인지 AR-02 가 잰다. `/sprint` 재검증 줄은 아래 넘김 |
| 근거 파일 §3 현행화 | Mermaid 12.0.0 — flows 버전 문장 · data-modeling ERD 배치 변경 (SK-09). gh 2.101.0 · Cucumber 는 바뀐 것이 없다고 research-log 에 적었다 (SK-10) |

## 미반영 키와 사유

- `F20` 의 한 나라 우선 판단 — 처리 배정표가 `user-setup:P10`(킷 밖, 카이젠 뒤 사용자 설정 처리 목록)으로 보냈다. 이 Phase 는 폐기 결정 기록 자리만 맡았다
- `F20` 의 시간대를 설정값으로 다루는 일 — 처리 배정표가 `backend-family:P2`(Phase 7)로 보냈다
- GitHub 문서 버전 날짜 `2026-03-10` — `plan-sync-github` 의 문서 링크는 `2022-11-28` 그대로 뒀다. `2022-11-28` 은 2028-03-10 까지 지원되고, `2026-03-10` 에는 옛 호출이 깨지는 변경이 있어 날짜만 바꾸면 안 된다(근거 파일 §3). 킷은 버전 헤더를 보내지 않는다
- `Design Sprint` 산출물 — plan-prd 에 틀이 없어 비범위 표를 넣을 자리가 없다. 그대로 뒀다
- Mermaid 12 렌더 확인 — 로컬에 Mermaid 가 없어(`command -v mmdc` 없음) 기존 예시를 12 에서 렌더해 보지 않았다. 문서에 그렇게 적었다
- PRD 와 별도 결정 기록(ADR) 가운데 어디가 나은지 — 근거 파일이 비교 자료를 조회하지 않았다(§5). PRD 를 고른 이유는 새 파일 · 새 흐름이 필요 없다는 것뿐이다
- 근거 파일 §4 권장 9 의 「Mermaid 12 ERD 배치 변경을 스냅샷 · 시각 검증 대상으로」 — 킷에 렌더 검증 절차가 없다. 문서에 렌더러 버전을 함께 적으라는 말만 넣었다

그대로 둔 곳과 이유:

- plan-prd Gotcha 5 · plan-audit 카테고리 3 행의 「최소 3 개」 — Shape Up 규칙이 아니라 이 킷의 기준이다(근거 파일 §5). 그 표시는 research-log 새 항목에만 적었다. plan-audit 행은 여전히 Shape Up §9 를 출처로 단다
- `plan-data-model/SKILL.md:24`(Gotcha 8, Mermaid 버전 적지 않음) — 그 스킬 Step 0 이 `data-modeling.md` 를 읽으니 버전 사실은 문서 한 곳에 둔다
- planning-reviewer `:151` 이 이 파일에 없는 「미검증 프로토콜의 4 요건」 을 가리킨다 — 기준 원본 사본을 옮기는 일과 같이 한다(아래 넘김)

Phase 1 가이드 변경 셋(오케스트레이터 Step 11 전수 감사):

| 가이드 변경 | 이 킷 | 자리 |
| --- | --- | --- |
| `[미검증]` 네 칸 (skill-design-guide §3.7 3 항 · agent-design-guide §10) | 해당 — 미반영 | planning-kit 의 `[미검증]` 은 전부 평가 쪽(plan-audit Gotcha 9 · Step 4 · Step 5, planning-reviewer)이고 기준 원본 사본을 따른다. 사본을 옮기면 READY · NEEDS_VERIFICATION 문턱이 바뀐다. 만드는 쪽 스킬에는 `[미검증]` 이 0 건 |
| 작업 자체를 못 한다고 결론 내리기 전 네 칸 (§3.7 5 조항 3 항) | 해당 없음 | 그런 결론 문장이 킷에 0 건. Step 0 의 「원칙 문서 없으면 `/planning-research` 권고 후 중단」 은 설계된 앞 조건 멈춤이다 |
| 0 이 아닌 값을 내는 새 측정 — 알려진 답 대조 (§3.7) | 해당 없음 | 이 킷 스킬은 값을 세는 측정 스크립트를 만들지 않는다 |

ER-03 (d)(공유 파일 · 다른 Phase 파일을 건드린 커밋 가운데 다른 Phase 서명이 없는 커밋 수)가 0 이 아니면 QA 가 그 커밋 목록부터 보고 판정한다 —
그 값은 다른 Phase 가 서명 줄을 단다는 전제에 기댄다.

## 넘기는 것

| 대상 | 누가 | 할 일 |
| --- | --- | --- |
| `harness/skills/sprint/SKILL.md` | 다음 사이클 Phase 4 | 재검증 블록이 PRD 비범위 절(`## Non-goals (폐기한 결정 포함)` · `## No-gos`) 경로를 읽는 줄. PRD 가 없는 프로젝트에서 폐기 결정을 적을 자리도 거기서 정한다 — plan-prd Gotcha 1(Discovery 없이 PRD 금지) 때문에 이 킷이 「폐기 기록만 담은 PRD」 를 만들게 할 수 없다 |
| `planning-kit/agents/planning-reviewer.md` | 다음 사이클 Phase 3 뒤 planning | 미검증 기준 원본 사본(`# Canonical Unverified-Evidence Protocol (정본 복제)`)을 2026-08-13 개정 판으로 옮기고, `:151` 의 「4 요건」 빈 가리킴을 고친다. plan-audit Gotcha 9 · Step 4 · Step 5 문턱을 같이 본다. 킷 reviewer 일곱을 한 번에 옮긴다는 Phase 8 넘김과 같은 일이다 |
| `docs/planning-kit/prd-patterns.html` | Final F2 | 새 절 「폐기한 결정」 이 없다. `docs/planning-kit/flows.html` · `data-modeling.html` 도 Mermaid 12 문장이 없다 — 세 페이지를 다시 만든다 |
| `planning-kit/.claude-plugin/plugin.json` | Final | planning-kit 버전(지금 0.5.1). PRD 산출물 틀(비범위 표)과 뒤 단계 스킬 동작이 바뀌었다 |
| `user-setup:P6` | 카이젠 뒤 사용자 설정 | 핸드오프 틀의 「폐기 · 거절한 결정」 절은 결정을 다시 쓰지 말고 PRD 비범위 절 경로만 가리킨다 |

Final 이 더 할 것: 이 Phase 는 공유 파일(marketplace · `plugin.json` · 루트 README · 루트 CLAUDE.md · `docs/` HTML · 감사 기록 · 실패 횟수 파일 · 처리 배정표 ·
`.github/workflows/ci.yml` · `.harness/stale-values.yaml`)을 건드리지 않았다.

## changelog 한 단락

planning-kit 이 사용자가 버린 기능 · 설정 항목을 그 기능 PRD 의 비범위 절 한 곳에 적게 한다. PR/FAQ · Linear-style 틀에 없던 `## Non-goals (폐기한 결정 포함)` 절이 생기고,
Shape Up 은 `## No-gos` 제목 그대로 세 틀이 같은 네 칸 표(하지 않는 것 · 이유 · 범위 · 코드에 남은 흔적)를 쓴다. 흔적 칸은 채울 빈틈이 아니라 치울 목록이고,
폐기는 영구 금지가 아니라 범위 칸이 그 폭을 적는다 — 되살려야 할 것 같으면 먼저 묻는다. plan-stories · plan-data-model · plan-flow 는 비범위 절을 읽고 겹치는 스토리 ·
필드 · 화면을 만들기 전에 묻는다(Step 0 은 로드만). plan-audit 카테고리 3 과 planning-reviewer 가 뒤 단계 산출물에 폐기한 항목이 다시 들어갔는지 본다 —
뒤 단계 0 매치는 같은 낱말이 PRD 표에도 걸릴 때만 PASS 근거다. 원칙 문서 `prd-patterns.md` 에 근거와 한계를 적었고, `flows.md` · `data-modeling.md` 를 Mermaid 12.0.0 기준으로 현행화했다.

## 킷 로그 한 단락

2026-09-25 planning-kit (카이젠 2026-09-24 Phase 11) — 처리 배정표 Phase 11 행 둘(`F20` · `backend-family:P1`)과 Phase 4 · 6 · 7 넘김을 두 관심사(폐기한 결정의 기록 자리와
뒤 단계 확인 · Mermaid 12 현행화)로 받았다. 기록은 `docs/planning/research-log.md` 1.1.0 항목이다.
근거: [Basecamp Shape Up §Chapter 6](https://basecamp.com/shapeup/1.5-chapter-06) · [Agile Alliance — INVEST](https://agilealliance.org/glossary/invest/) ·
[GitHub — Best practices for Projects](https://docs.github.com/issues/planning-and-tracking-with-projects/learning-about-projects/best-practices-for-projects) ·
[Mermaid — Entity Relationship Diagram](https://mermaid.js.org/syntax/entityRelationshipDiagram.html) · [Mermaid 12.0.0 release](https://github.com/mermaid-js/mermaid/releases/tag/mermaid%4012.0.0) ·
[GitHub — REST API Versions](https://docs.github.com/en/rest/about-the-rest-api/api-versions) · [GitHub — Breaking Changes](https://docs.github.com/en/rest/about-the-rest-api/breaking-changes) ·
[GitHub CLI 2.101.0](https://github.com/cli/cli/releases/tag/v2.101.0) · [Cucumber Gherkin Reference](https://cucumber.io/docs/gherkin/reference).

## 다음 사이클 메모

- 뒤 단계 스킬이 실제로 비범위 표를 읽고 겹치는 항목 앞에서 묻는지는 LLM 동작이라 이번 계약이 재지 않았다(문장이 정해진 절 · 순서에 있는지만 쟀다). planning-kit 에 평가 사례 파일이 생기면 「폐기한 항목이 코드에 남은 PRD → plan-data-model 이 그 필드를 넣지 않고 묻는다」 사례를 먼저 넣는다
- 새 비범위 표의 머리 · 예시 행은 plan-prd 한 곳에만 있다(RE-02). 뒤 단계 셋 · 감사 둘은 `(plan-prd Gotcha 14)` · `§폐기한 결정` 으로 가리킨다 — 표 칸을 바꾸면 plan-prd 와 `prd-patterns.md` 두 곳만 고친다
- 이 계약 AR-03 (c) 는 Step 0 절 diff 에서 더한 줄과 지운 줄을 함께 센다. 더한 줄만 세면 절 제목이 바뀌어 끝 판이 비었을 때 0 으로 통과한다(1 회차 검토가 사본 둘로 실측). 다른 킷 계약의 「절이 편집 전과 같다」 측정도 같은 구멍이 있는지 본다
- Mermaid 13 이 나오면 `flows.md` 버전 문장의 확인 날짜와 값을 다시 적는다. 렌더 확인 도구가 생기면 「렌더해 보지 않았다」 를 지운다
- `plan-sync-github` 의 GitHub 문서 버전 날짜는 `2022-11-28` 지원 기한(2028-03-10) 전에 `2026-03-10` 변경 목록을 보고 옮긴다
