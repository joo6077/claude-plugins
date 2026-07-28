---
name: plan-audit
description: >
  완성된 기획 산출물을 카테고리별 PASS/FAIL 로 체계적 감사한다.
  sprint-contract 로 넘어갈 수 있는 수준인지 판정한다.
  planning-reviewer 에이전트를 호출하여 독립 평가 수행.
  "기획 감사", "plan audit", "기획 완성도", "sprint 전 검수",
  "기획 검수", "PRD 품질 확인" 같은 요청 시 트리거.
  가벼운 리뷰는 plan-guide 사용.
argument-hint: "[기획 디렉토리 경로, 기본: .planning/]"
user-invocable: true
---

# Gotchas

1. **단일 에이전트 판정에 의존 금지** — planning-reviewer 에이전트를 Agent 도구로 호출하여 **독립 평가** 수행. 본 스킬은 오케스트레이션만 담당.
2. **산출물 없는 항목을 FAIL 로 처리** — 해당 파일이 없으면 "NOT_FOUND" 가 아니라 "FAIL (missing)" 로 기록. discovery 가 없는 PRD 는 기반이 없다.
3. **주관 평가 금지** — 모든 항목은 docs/planning/ 원칙 문서 기준 객관 검증. "좋다/나쁘다" 금지, "포함됨/누락됨" 만.
4. **FAIL 이면 sprint-contract 진행 차단** — 1개라도 FAIL 이면 사용자에게 보완 요청. "PASS 로 간주하고 진행" 우회 금지.
5. **리포트 경로 고정** — `.planning/audit-<timestamp>.md` 로 저장하여 추적 가능하게.
6. **평가 카테고리 생략 금지** — 아래 **12 카테고리 (0a/0b + 1~10)** 모두 평가. 해당 없으면 "N/A (reason)" 명시. 카테고리 수가 요약표와 본문에서 다르면 Sibling Consistency 위반 — verdict 신뢰 붕괴.
7. **원칙 위반 기록 시 출처 인용 필수** — FAIL 판정 시 `principle_violated` 필드에 docs/planning/*.md 섹션 + 1차 출처 URL 둘 다 명시. 예: "INVEST §Small (출처: [Agile Alliance](https://agilealliance.org/glossary/invest/))".
8. **Enumerate-before-Act** — Step 2 에서 reviewer 호출 전, Step 1 에서 **존재하는 모든 .planning/ 파일을 인벤토리로 나열**하고 사용자에게 보여준다. 비인벤토리 상태에서 reviewer 를 spawn 하면 누락 파일이 FAIL 로 잡히지 않는다.
9. **[미검증] 표기 의무** — reviewer 가 자체 검증 불가능한 항목(예: Mermaid 렌더 결과, 외부 URL 유효성, GitHub sync 실제 결과)은 FAIL 이 아니라 `[미검증]` 으로 표기하고 사용자에게 수동 확인 요청. 관측 못 한 것을 FAIL 처리하면 평가 의미 상실. **마커 의미·임계값·집계 형식의 SSOT 는 `harness/docs/guides/qa-evaluation-guide.md` §Canonical Unverified-Evidence Protocol 이며 `planning-reviewer` 가 이를 복제 보유한다 — 본 스킬에서 임계 숫자를 재정의하지 마라.**
10. **산출물이 있어도 공허하면 PASS 금지** — 파일이 존재하는데 해당 섹션이 비어 있거나 템플릿 헤더만 남은 경우(항목 0개), 존재 자체를 충족으로 읽지 마라. canonical 조항 2 의 3 분기(FAIL / 도구 부재 / 증거 무효)를 적용한다. 빈 결과를 "문제 없음" 으로 읽는 것이 skill-design-guide §3.7 조항 4 가 지적한 실제 사고 형태다.

# Process

## Step 0: 자동 로드 (독립 단계)

**이 단계에서 산출물을 건드리지 않는다.** 평가에 필요한 배경만 로드한다:

1. `docs/planning/` 전체 원칙 문서 존재 확인:
   - discovery.md, prd-patterns.md, stories.md, prioritization.md, flows.md, data-modeling.md, risks.md, cognitive-biases.md, github-integration.md, reference.md, ideation.md
2. 없는 문서가 있으면 `/planning-research <주제>` 권고 후 중단. 원칙 없는 감사는 학습 데이터 기반이 되어 신뢰 0.
3. 이전 단계 산출물이 있을 수 있는 디렉토리 확인: `.planning/` (기본) 또는 사용자 지정 경로.

이 Step 을 건너뛰고 바로 reviewer 를 호출하면 원칙 인용 없는 주관 판정으로 귀결된다.

## Step 1: 입력 확인 · 파일 인벤토리

- 기본 경로 `.planning/` (인수로 다른 경로 가능)
- 존재하는 기획 산출물 파일을 **모두 나열** (glob 기반):
  - `ideate-*.md` (선택)
  - `reference-*.md` (선택)
  - `discover-*.md`
  - `prd-*.md`
  - `stories-*.md`
  - `priorities-*.md`
  - `flow-*.md`
  - `data-model-*.md`
  - `risks-*.md`
  - 기타 `.planning/` 하위 .md 파일

인벤토리를 사용자에게 **리스트로 먼저 보여주고**, 누락된 파일이 있으면 해당 카테고리가 자동 FAIL 처리됨을 안내한다 (Enumerate-before-Act).

## Step 2: planning-reviewer 에이전트 호출

Agent 도구로 `planning-reviewer` 서브에이전트 spawn. 프롬프트에 다음 전달:
- Step 1 인벤토리 (파일 경로 목록)
- Step 0 에서 확인한 `docs/planning/` 원칙 문서 경로
- 아래 **12 카테고리** 체크리스트 (0a Reference, 0b Ideation 은 선택 — 해당 산출물 없으면 N/A)

## Step 3: 12 카테고리 평가 기준

| # | 카테고리 | PASS 조건 | 참조 문서 | 1차 출처 |
|---|---------|-----------|----------|----------|
| 0a | Reference | (선택) 레퍼런스 제품이 존재하면 Lightning Demo 5+ 제품 + Feature Matrix + Positioning Statement 존재. "X 같은 앱" 류 요청이 아니면 N/A | reference.md | [GV Sprint Lightning Demo](https://www.gv.com/sprint/), [Strategyzer VPC](https://www.strategyzer.com/library/the-value-proposition-canvas), [April Dunford](https://www.aprildunford.com/) |
| 0b | Ideation | (선택) 발산(HMW/Crazy 8s 등) + 정리(Affinity/Mindmap) + 수렴(Dot/Impact-Effort) 흔적 존재. 단일 아이디어에서 바로 discovery 진입한 경우 N/A | ideation.md | [Stanford d.school](https://dschool.stanford.edu/resources), [GV Sprint](https://www.gv.com/sprint/), [Design Council Double Diamond](https://www.designcouncil.org.uk/our-resources/the-double-diamond/) |
| 1 | Discovery | Problem/User/JTBD/Assumption/Metric 모두 존재 + switching moments 인터뷰 증거 | discovery.md §JTBD / §Continuous Discovery | [Klement](https://www.alanklement.com/), [Torres](https://www.producttalk.org/glossary-discovery-continuous-discovery/) |
| 2 | PRD Format | PR/FAQ 또는 Shape Up 또는 Linear 스펙 포맷 완결 (Problem + Appetite/Solution + Rabbit holes/No-gos 또는 PR + FAQ) | prd-patterns.md §Amazon Working Backwards / §Shape Up | [Amazon](https://www.aboutamazon.com/news/workplace/an-insider-look-at-amazons-culture-and-processes), [Shape Up §6](https://basecamp.com/shapeup/1.5-chapter-06) |
| 3 | Non-goals | 최소 3개 명시 (Shape Up 의 no-gos / rabbit holes 포함) | prd-patterns.md §Shape Up | [Shape Up §9](https://basecamp.com/shapeup/2.3-chapter-09) |
| 4 | Success Metrics | Leading + Lagging + 기준선 숫자 (vanity metric 아님) | discovery.md §Lean Canvas | [Leanstack](https://leanstack.com/articles/3-mental-models-for-continuous-innovation) |
| 5 | Stories INVEST | 모든 스토리가 Independent/Negotiable/Valuable/Estimable/Small/Testable 6개 항목 통과 | stories.md §INVEST | [Agile Alliance INVEST](https://agilealliance.org/glossary/invest/) |
| 6 | Acceptance Criteria | Gherkin Given-When-Then 3-5 step + happy path + edge case 2+ (관찰 가능한 결과) | stories.md §Gherkin / §AC | [Cucumber Reference](https://cucumber.io/docs/gherkin/reference) |
| 7 | Prioritization | 프레임워크 선택 근거 + Confidence < 100% + Top 3 의존성/리스크 검토 | prioritization.md §RICE / §WSJF | [Intercom RICE](https://www.intercom.com/blog/rice-simple-prioritization-for-product-managers/), [SAFe WSJF](https://scaledagileframework.com/wsjf/) |
| 8 | Flow | Mermaid 공식 문법 유효 + edge case 경로 (에러/취소/권한/빈상태) + 다이어그램 타입이 목적과 일치 (flowchart≠sequence≠state≠journey) | flows.md §User Flow vs Journey vs Blueprint | [NN/g Journey](https://www.nngroup.com/articles/journey-mapping-101/), [Mermaid Flowchart](https://mermaid.js.org/syntax/flowchart.html) |
| 9 | Data Model | Bounded Context 식별 + Aggregate Root 명시 + Domain Event 과거형 + ERD cardinality 정확 + Data Dictionary 필드별 정의 | data-modeling.md §DDD / §Event Storming | [DDD Reference](https://www.domainlanguage.com/ddd/reference/), [EventStorming](https://www.eventstorming.com/) |
| 10 | Risks | 4-risks (value/usability/feasibility/viability) 모두 커버 + Pre-mortem 10 시나리오 + score ≥15 에 mitigation/early signal + 인지편향 체크 | risks.md §Pre-mortem / §4-risks, cognitive-biases.md | [HBR Pre-mortem](https://hbr.org/2007/09/performing-a-project-premortem), [SVPG 4 Risks](https://www.svpg.com/four-big-risks/), [The Decision Lab](https://thedecisionlab.com/biases/confirmation-bias) |

## Step 4: 리포트 생성

분모는 **항상 12** 다. 0a/0b 를 N/A 로 처리해도 카테고리는 사라지지 않고 `N/A` 라는 판정을 받은 채 남는다 — 분모를 10 으로 줄이면 `planning-reviewer` Gotcha 9(분모 항상 12) 와 어긋나고 아래 템플릿의 `/ 12` 표기와도 모순된다. **PASS + FAIL + N/A + [미검증] 합이 12 와 일치**해야 한다 (Sibling Consistency). 합이 12 가 아니면 리포트를 쓰지 말고 reviewer 에 재산정을 요구한다.

```markdown
# Plan Audit: <프로젝트>
Date: <YYYY-MM-DD>
Auditor: planning-reviewer agent

## Summary
- 평가 카테고리: 12 (0a Reference, 0b Ideation, 1~10)
- PASS: X / 12
- FAIL: Y / 12
- N/A: Z / 12
- [미검증]: W 건
  - <카테고리 ID> — 사유: ... / 시도한 fallback: ...
- Verdict: **READY_FOR_SPRINT_CONTRACT** | **NEEDS_REVISION** | **NEEDS_VERIFICATION** | **BLOCKED**

## Findings
### 1. Discovery — PASS
- Evidence: .planning/discover-xxx.md:12-45
- Notes: ...

### 5. Stories INVEST — FAIL
- Evidence: .planning/stories-xxx.md US-003
- Problem: Estimable 실패 — "여러 화면 변경" 모호
- Principle: stories.md §INVEST §Estimable (출처: https://agilealliance.org/glossary/invest/)
- Fix: 구체 화면 수 명시 또는 Epic 으로 승격 후 재분해

### 8. Flow — [미검증]
- Evidence: .planning/flow-xxx.md
- Reason: Mermaid 실제 렌더 결과 reviewer 에이전트가 확인 불가 — 사용자가 mermaid.live 에서 검증 요청.

## Next Actions
- [ ] US-003 재분해
- [ ] R1 mitigation 추가
```

## Step 5: Verdict 결정

reviewer 가 FAIL 축과 `[미검증]` 축을 각각 판정해서 돌려준다. 본 스킬은 그 결과를 그대로 옮기고, 두 축 중 더 강한 제약을 최종 verdict 로 기록한다.

**FAIL 축:**

- **READY_FOR_SPRINT_CONTRACT**: FAIL 0 (12 카테고리 모두 PASS 또는 명시적 N/A). → sprint-contract 진행 가능
- **NEEDS_REVISION**: 1-3 FAIL, 모두 수정 가능 범위. → 보완 후 재감사. (CONDITIONAL — 기획 기반 자체는 유효하지만 일부 산출물 품질 부족)
- **BLOCKED**: 4+ FAIL 또는 discovery / prd 자체 누락. → plan-discover 부터 재시작

**`[미검증]` 축** — 임계값을 여기서 다시 정의하지 않는다. SSOT 는 `harness/docs/guides/qa-evaluation-guide.md` §Canonical Unverified-Evidence Protocol 조항 3 (임계 2) 이고, `planning-reviewer` 가 그것을 복제 보유한다:

- 0 건 → FAIL 축 결과 그대로
- 1 건 → FAIL 축 결과 유지 + 리포트 최상단 경고 명시 (FAIL 0 이면 READY 가능)
- 2 건 이상 → **NEEDS_VERIFICATION** (READY 아님). FAIL 0 이어도 sprint-contract 진행 차단

[미검증] 항목은 FAIL 로 counting 하지 않되(두 축 별개), 조항 5 에 따라 `미검증 N 건` 을 반드시 집계하고 건별로 `[카테고리 ID, 사유, 시도한 fallback 단계]` 를 기록한다. Next Actions 에 "검증 후 재평가" 를 반드시 포함.

## Step 6: 저장 + 안내

`.planning/audit-<timestamp>.md` 저장.

Verdict 가 READY 가 아니면 **sprint-contract 진행 차단**하고 보완 항목 명시. 사용자가 "이번에는 READY 로 간주하고 진행" 요청해도 차단 — Gotcha 4 우회 금지.

# References

- `planning-reviewer` 에이전트 — 12 카테고리 독립 평가 (0a Reference, 0b Ideation, 1~10)
- `docs/planning/` 전체 원칙 문서 (discovery, prd-patterns, stories, prioritization, flows, data-modeling, risks, cognitive-biases, github-integration, reference, ideation)

주요 1차 출처 (12 카테고리 대응):
- [Alan Klement — JTBD](https://www.alanklement.com/)
- [Teresa Torres — Continuous Discovery](https://www.producttalk.org/glossary-discovery-continuous-discovery/)
- [Amazon Working Backwards](https://www.aboutamazon.com/news/workplace/an-insider-look-at-amazons-culture-and-processes)
- [Basecamp Shape Up](https://basecamp.com/shapeup/1.5-chapter-06)
- [Agile Alliance — INVEST](https://agilealliance.org/glossary/invest/)
- [Cucumber Gherkin Reference](https://cucumber.io/docs/gherkin/reference)
- [Intercom — RICE](https://www.intercom.com/blog/rice-simple-prioritization-for-product-managers/)
- [NN/g — Journey Mapping](https://www.nngroup.com/articles/journey-mapping-101/)
- [Eric Evans — DDD Reference](https://www.domainlanguage.com/ddd/reference/)
- [Gary Klein — HBR Pre-mortem](https://hbr.org/2007/09/performing-a-project-premortem)
- [Marty Cagan — Four Big Risks](https://www.svpg.com/four-big-risks/)
