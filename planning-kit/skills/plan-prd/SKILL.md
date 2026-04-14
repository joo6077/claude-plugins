---
name: plan-prd
description: >
  discovery 산출물 또는 충분히 정의된 문제를 받아 PRD(Product Requirements Document)를 작성한다.
  Amazon Working Backwards(PR/FAQ) 또는 Basecamp Shape Up Pitch 중 컨텍스트에 맞는 포맷을 선택한다.
  "PRD 써줘", "기획서 작성", "Shape Up pitch", "PR/FAQ",
  "스펙 문서", "requirements 작성" 같은 요청 시 트리거.
  아이디어만 있는 상태면 plan-discover 먼저. 구현 계약은 sprint-contract 사용.
argument-hint: "[discovery 파일 경로 또는 기능 이름]"
user-invocable: true
---

# Gotchas

1. **Discovery 없이 PRD 금지** — Problem / JTBD / User / Success Metric 이 없으면 `/plan-discover` 먼저 실행. 추측 기반 PRD 는 나중에 전부 재작업된다.
2. **포맷 강제 금지** — PR/FAQ 와 Shape Up Pitch 는 용도가 다르다. 신규 제품/큰 기능은 PR/FAQ, 6주 사이클 단위의 문제해결은 Shape Up. 사용자에게 선택하게 하라.
3. **Solution 을 먼저 쓰지 마라** — PR/FAQ 는 "릴리스 시 보도자료" 부터 쓴다. Shape Up 은 "Problem → Appetite → Solution" 순서. 기술 구현은 마지막.
4. **Appetite 없이 Shape Up 금지** — Shape Up 의 핵심은 "시간 고정, 스코프 유동". 6주/2주 같은 Appetite(fixed time) 를 먼저 받고 거기에 맞춰 스코프 조정.
5. **Non-goals 명시** — 하지 않을 것을 적지 않으면 PRD 는 매주 늘어난다. 최소 3개의 non-goal 필수.
6. **측정 기준 없는 성공 선언 금지** — "사용성이 개선된다" 는 PRD 가 아니다. discovery 의 Leading/Lagging 지표를 옮겨 쓰고 기준선 명시.
7. **Open Questions 섹션 필수** — 모든 불확실성을 강제로 노출한다. 0개면 거짓말이다.
8. **Rabbit holes(함정) 섹션 명시 — Shape Up** — 시간을 먹는 난제를 사전에 적는다. 예: "복잡한 권한 모델은 이번 사이클에서 다루지 않는다".
9. **PR/FAQ 가 슬로건 문서로 전락 금지** — Amazon Working Backwards 의 FAQ 는 칭찬용 질문이 아니라 실제 반대 질문을 다뤄야 한다. 고객 혜택/운영 영향/가격/정책/롤아웃 제약을 포함하지 않으면 narrative 강도가 있어도 실행 세부가 누락된 상태다. 출처: [About Amazon — 문화와 프로세스](https://www.aboutamazon.com/news/workplace/an-insider-look-at-amazons-culture-and-processes).
10. **Shape Up 의 appetite 는 scope 약속이 아니다** — appetite 는 "이 문제에 쓸 의향이 있는 시간" 이며 scope 는 그 안에서 유동. shaping 역량이 약하면 지나치게 모호해져서 성공 기준이 흐려진다. 출처: [Basecamp Shape Up §Chapter 6](https://basecamp.com/shapeup/1.5-chapter-06), [§Chapter 9](https://basecamp.com/shapeup/2.3-chapter-09).
11. **Linear-style 경량 spec 은 전략 문맥을 흘릴 수 있다** — issue/project template 중심 구조는 planning-execution 통합에 강하지만, 복잡한 전략 배경/의사결정 근거는 별도 허브 문서(Notion 등)로 보완 필요. 출처: [Linear Issue Templates](https://linear.app/docs/issue-templates), [Project Templates](https://linear.app/docs/project-templates).
12. **공개 문서형 spec (Stripe 패턴) 은 PRD 대체재가 아니다** — integration contract 로 쓰일 수는 있으나 내부 의사결정 근거, trade-off, 비범위는 반드시 별도 PRD 에 남겨야 한다. 출처: [Stripe Docs — Products & Prices](https://docs.stripe.com/products-prices/how-products-and-prices-work).

# Process

## Step 0: 리서치 문서 로드

`docs/planning/prd-patterns.md` 로드. Amazon PR/FAQ · Shape Up Pitch · Linear/Stripe/Notion 공개 템플릿 참조.

## Step 1: 입력 확인

- discovery 파일 경로가 주어지면 로드
- 없으면 Problem / User / JTBD / Success Metric 4개가 명시적으로 있는지 확인. 없으면 `/plan-discover` 재지시.

## Step 2: 포맷 선택

다음 표로 사용자에게 선택하게 한다:

| 포맷 | 적합 | 산출물 구조 | 출처 |
|------|------|-------------|------|
| **PR/FAQ** (Amazon) | 신규 제품, 큰 기능, 외부 고객 향 | 보도자료(1p) + 내부 FAQ + 외부 FAQ | [About Amazon](https://www.aboutamazon.com/news/workplace/an-insider-look-at-amazons-culture-and-processes) |
| **Shape Up Pitch** (Basecamp) | 6주 이내 해결 가능한 문제 중심 기능 | Problem + Appetite + Solution(스케치) + Rabbit holes + No-gos | [Shape Up §6](https://basecamp.com/shapeup/1.5-chapter-06), [§9](https://basecamp.com/shapeup/2.3-chapter-09) |
| **Linear-style Spec** | 작은 기능, 엔지니어링 중심 | Problem + Solution + Open questions + Milestones | [Linear Issue Templates](https://linear.app/docs/issue-templates) |
| **Design Sprint 산출물** (GV) | 불확실성 큰 신규 흐름, prototype 검증 | Map + Sketch + Decide + Storyboard + Prototype/Test | [GV Sprint](https://www.gv.com/sprint/) |

## Step 3: 작성

### PR/FAQ 템플릿

```markdown
# [제품명] - Press Release (Future-dated)

## Headline
## Sub-headline (who + benefit)
## Summary paragraph
## Problem paragraph
## Solution paragraph
## Quote from company leader
## How to get started
## Customer quote

---

## Internal FAQ
- 왜 지금 만드는가?
- 가장 어려운 문제는?
- 만들지 않으면 어떻게 되는가?
- 측정 지표는?

## External FAQ
- 어떻게 작동하나요?
- 가격은?
- 지원 플랫폼은?
```

### Shape Up Pitch 템플릿

```markdown
# Pitch: [제목]

## Problem
(한 문단 — 구체적 스토리 포함)

## Appetite
- Small Batch (2주) / Big Batch (6주)

## Solution
### Fat marker sketch
(Mermaid flowchart 또는 ASCII 스케치 — 세부 아닌 개념)

### Breadboard
(UI elements + connections, 픽셀 아님)

## Rabbit holes
- (시간 먹을 수 있는 난제)

## No-gos
- (명시적 제외)
```

### Linear-style Spec 템플릿

```markdown
# [제목]
## Problem
## Proposal
## Milestones
- [ ] M1
- [ ] M2
## Open questions
```

## Step 4: 체크리스트 검증

작성 완료 후 스스로 점검:

- [ ] Problem 에 specific user story 가 있는가
- [ ] Success metric 에 기준선이 있는가 (X% → Y%)
- [ ] Non-goals 가 3개 이상인가
- [ ] Rabbit holes / Open questions 가 최소 1개 이상인가
- [ ] 기술 선택을 PRD 에 섞지 않았는가 (구현은 sprint-contract 에서)

하나라도 ✗ 면 그 섹션 재작성.

## Step 5: 저장 + 다음 단계

`.planning/prd-<slug>.md` 저장. 다음 권고:
- 유저 플로우 필요 → `/plan-flow`
- 데이터 구조 필요 → `/plan-data-model`
- 우선순위 → `/plan-prioritize`
- 스토리 분해 → `/plan-stories`
- 리스크 점검 → `/plan-risks`
- 완성도 감사 → `/plan-audit`

# References

- `docs/planning/prd-patterns.md` — Amazon PR/FAQ, Shape Up, Linear, Notion, Stripe, Design Sprint
- `docs/planning/discovery.md`

주요 1차 출처:
- [Amazon Working Backwards](https://www.aboutamazon.com/news/workplace/an-insider-look-at-amazons-culture-and-processes)
- [Basecamp Shape Up §6](https://basecamp.com/shapeup/1.5-chapter-06)
- [Basecamp Shape Up §9](https://basecamp.com/shapeup/2.3-chapter-09)
- [Linear Docs — Issue/Project Templates](https://linear.app/docs/issue-templates)
- [Notion Product Spec Template](https://www.notion.so/notion/Product-spec-1cd083403f64437e86631e60c64218d2)
- [GV Design Sprint](https://www.gv.com/sprint/)
