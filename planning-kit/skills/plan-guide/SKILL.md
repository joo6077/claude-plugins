---
name: plan-guide
description: >
  기획 문서나 아이디어에 대해 가벼운 원칙 기반 피드백을 제공한다.
  docs/planning/ 의 방법론 문서를 참조하여 해당 영역의 원칙만 집중 설명.
  "기획 피드백", "이 PRD 괜찮아?", "스토리 리뷰", "우선순위 의견",
  "plan guide", "기획 리뷰" (가벼운) 같은 요청 시 트리거.
  체계적 전수 감사에는 트리거하지 않는다 — plan-audit 사용.
argument-hint: "[파일 경로 또는 설명]"
user-invocable: true
---

# Gotchas

1. **주관적 표현 금지** — "좋다", "깔끔하다" 같은 주관 평가 금지. 반드시 출처 있는 원칙을 근거로 제시.
2. **카테고리 과잉 방지** — 한 번에 모든 영역 언급 금지. 사용자가 물어본 맥락의 원칙만 집중.
3. **리서치 문서 없이 답변 금지** — `docs/planning/` 문서를 먼저 읽고 답변. 학습 데이터 기반 답변 금지.
4. **Fix 없이 원칙만 나열 금지** — "INVEST 를 지키라" 만 말하면 교과서다. 사용자 문서의 구체 위치를 짚고 개선 방향 제시.
5. **트레이드오프 없는 단언 금지** — "Shape Up 으로 바꿔라" 대신 "현재 크기면 Shape Up 이 적합하지만 외부 고객 발표가 필요하면 PR/FAQ 가 낫다" 처럼 양면 제시.
6. **전수 감사로 확장 금지** — 사용자가 가볍게 물으면 가볍게 답한다. 10개 카테고리 점검이 필요하면 `/plan-audit` 로 안내.
7. **원칙 인용 시 출처 URL 필수** — "INVEST" 한 단어만 던지지 말고 [Agile Alliance — INVEST](https://agilealliance.org/glossary/invest/) 처럼 1차 출처 링크 포함. 출처 없는 원칙 언급은 학습 데이터 재생산으로 간주.

# Process

## Step 1: 맥락 파악

사용자 질문에서 영역 식별:

| 영역 | 키워드 | 주요 1차 출처 |
|------|--------|--------------|
| discovery | 문제, 가정, JTBD, user, 인터뷰, 가치 | [Klement](https://www.alanklement.com/), [Torres](https://www.producttalk.org/glossary-discovery-opportunity-solution-tree/), [Cagan](https://www.svpg.com/four-big-risks/) |
| prd | PRD, 기획서, spec, Shape Up, PR/FAQ, appetite | [Amazon](https://www.aboutamazon.com/news/workplace/an-insider-look-at-amazons-culture-and-processes), [Shape Up](https://basecamp.com/shapeup/1.5-chapter-06), [Linear](https://linear.app/docs/issue-templates) |
| stories | 스토리, user story, INVEST, AC, Gherkin | [Agile Alliance INVEST](https://agilealliance.org/glossary/invest/), [Cucumber Gherkin](https://cucumber.io/docs/gherkin/reference), [Patton](https://jpattonassociates.com/story-mapping/) |
| prioritization | 우선순위, RICE, Kano, WSJF, MoSCoW, priority | [Intercom RICE](https://www.intercom.com/blog/rice-simple-prioritization-for-product-managers/), [SAFe WSJF](https://scaledagileframework.com/wsjf/), [Strategyn ODI](https://strategyn.com/lp/outcome-driven-innovation/) |
| flow | 플로우, 다이어그램, sequence, state, journey | [NN/g Journey](https://www.nngroup.com/articles/journey-mapping-101/), [NN/g Blueprint](https://www.nngroup.com/articles/service-blueprints-definition/), [Mermaid](https://mermaid.js.org/syntax/flowchart.html) |
| data-modeling | 데이터 모델, ERD, 도메인, aggregate, event | [DDD Reference](https://www.domainlanguage.com/ddd/reference/), [EventStorming](https://www.eventstorming.com/), [Mermaid ER](https://mermaid.js.org/syntax/entityRelationshipDiagram.html) |
| risks | 리스크, pre-mortem, 편향, inversion, 실패 | [HBR Pre-mortem](https://hbr.org/2007/09/performing-a-project-premortem), [Inversion](https://fs.blog/inversion/), [The Decision Lab](https://thedecisionlab.com/biases/confirmation-bias) |
| github-integration | Issue, milestone, project board, 동기화 | [GitHub Projects](https://docs.github.com/issues/planning-and-tracking-with-projects/learning-about-projects/best-practices-for-projects), [gh CLI](https://cli.github.com/manual/gh_issue) |

## Step 2: 해당 리서치 문서 로드

`docs/planning/<area>.md` 열람. 없으면 `/planning-research` 권고 후 중단.

## Step 3: 원칙 적용

- 사용자 문서/설명 읽기
- 해당 원칙이 위반된 **구체 위치** 찾기 (섹션/문장 지정)
- 개선 방향 제시 (트레이드오프 포함)

## Step 4: 응답 포맷

```markdown
## 관찰
(원문 인용 또는 섹션 레퍼런스)

## 원칙
(관련 원칙 1-2개, 출처 링크)

## 적용
(구체 개선 방향, 트레이드오프)

## 다음 단계 (선택)
(심화하려면 어떤 스킬 사용)
```

## Step 5: 확장 안내

사용자가 "전체 점검" 원하면 `/plan-audit` 로 유도. 가볍게 계속 묻는다면 계속 가이드 모드 유지.

# References

- `docs/planning/` 전체 — discovery, prd-patterns, stories, prioritization, flows, data-modeling, risks, cognitive-biases, github-integration

각 영역 1차 출처는 위 Step 1 테이블의 "주요 1차 출처" 컬럼 참조.
