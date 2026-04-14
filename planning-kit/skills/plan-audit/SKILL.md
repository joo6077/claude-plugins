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
6. **평가 카테고리 생략 금지** — 아래 10개 카테고리 모두 평가. 해당 없으면 "N/A (reason)" 명시.
7. **원칙 위반 기록 시 출처 인용 필수** — FAIL 판정 시 `principle_violated` 필드에 docs/planning/*.md 섹션 + 1차 출처 URL 둘 다 명시. 예: "INVEST §Small (출처: [Agile Alliance](https://agilealliance.org/glossary/invest/))".

# Process

## Step 1: 입력 확인

- 기본 경로 `.planning/`
- 존재하는 기획 산출물 파일 인벤토리:
  - `discover-*.md`
  - `prd-*.md`
  - `stories-*.md`
  - `priorities-*.md`
  - `flow-*.md`
  - `data-model-*.md`
  - `risks-*.md`

누락 파일은 해당 카테고리를 자동 FAIL.

## Step 2: planning-reviewer 에이전트 호출

Agent 도구로 `planning-reviewer` 서브에이전트 spawn. 프롬프트에 평가 대상 파일 경로 + 10 카테고리 체크리스트 전달.

## Step 3: 10 카테고리 평가 기준

| # | 카테고리 | PASS 조건 | 참조 문서 | 1차 출처 |
|---|---------|-----------|----------|----------|
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

```markdown
# Plan Audit: <프로젝트>
Date: <YYYY-MM-DD>
Auditor: planning-reviewer agent

## Summary
- PASS: X / 10
- FAIL: Y / 10
- N/A: Z / 10
- Verdict: **READY_FOR_SPRINT_CONTRACT** | **NEEDS_REVISION** | **BLOCKED**

## Findings
### 1. Discovery — PASS
- Evidence: .planning/discover-xxx.md:12-45
- Notes: ...

### 5. Stories INVEST — FAIL
- Evidence: .planning/stories-xxx.md US-003
- Problem: Estimable 실패 — "여러 화면 변경" 모호
- Fix: 구체 화면 수 명시 또는 Epic 으로 승격 후 재분해

## Next Actions
- [ ] US-003 재분해
- [ ] R1 mitigation 추가
```

## Step 5: Verdict 결정

- **READY**: 10개 모두 PASS 또는 명시적 N/A. → sprint-contract 진행 가능
- **NEEDS_REVISION**: 1-3 FAIL, 모두 수정 가능 범위. → 보완 후 재감사
- **BLOCKED**: 4+ FAIL 또는 discovery 자체 누락. → plan-discover 부터 재시작

## Step 6: 저장 + 안내

`.planning/audit-<timestamp>.md` 저장.

Verdict 가 READY 가 아니면 **sprint-contract 진행 차단**하고 보완 항목 명시.

# References

- `planning-reviewer` 에이전트 — 10 카테고리 독립 평가
- `docs/planning/` 전체 원칙 문서 (discovery, prd-patterns, stories, prioritization, flows, data-modeling, risks, cognitive-biases, github-integration)

주요 1차 출처 (10 카테고리 대응):
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
