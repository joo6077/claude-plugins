---
name: prd-patterns
description: PRD와 제품 기획 문서를 작성할 때 참고할 수 있는 대표 패턴과 공개 템플릿 정리
last_updated: 2026-04-14
version: 0.1.0
---

# PRD Patterns

## 개요
PRD(Product Requirements Document)는 더 이상 한 가지 형식으로 고정되지 않는다. 어떤 조직은 narrative-first 문서를 쓰고, 어떤 조직은 Shape Up pitch처럼 appetite와 no-go를 강조하며, 어떤 조직은 issue/document template 중심의 lightweight spec을 선호한다. 중요한 것은 형식보다 의사결정 구조다.

강한 PRD 패턴은 최소한 다섯 가지를 분리한다. 문제 정의, 대상 사용자/고객, 성공 기준, 범위/비범위, 그리고 남아 있는 리스크다. 아래 패턴들은 각기 다른 조직 문화를 반영하지만, 공통적으로 "실행팀이 독립적으로 좋은 판단을 내릴 수 있는 정보 밀도"를 높이는 데 초점이 있다.

## 원칙/방법론별 섹션

### Amazon Working Backwards (PR/FAQ)
**요약**: Amazon의 Working Backwards는 내부 아이디어를 고객 관점의 보도자료(Press Release)와 FAQ로 먼저 표현하는 방식으로 유명하다. 핵심은 기능 명세보다 고객 효익과 고객이 느끼는 변화, 그리고 어려운 질문에 대한 선제 답변을 먼저 쓰는 것이다.

PR/FAQ의 장점은 팀이 고객 언어로 사고하도록 강제한다는 데 있다. 보도자료는 "출시 후 세상"을 가정하고, FAQ는 내부 실행 리스크와 까다로운 반대 질문을 드러낸다. 그래서 아이디어의 모호함과 과장된 기대를 초기에 깎아낸다.

**핵심 질문/포맷/체크리스트**:
- 보도자료 첫 문단에서 고객 가치가 분명한가?
- 누구를 위한 출시인지가 명시되어 있는가?
- FAQ가 칭찬용 질문이 아니라 실제 반대 질문을 다루는가?
- 고객 혜택, 운영 영향, 가격/정책, 롤아웃 제약이 포함되어 있는가?
- 문서만 읽고도 "왜 지금 이걸 하는지"가 이해되는가?

**적용 시점**: 신규 제품 제안, 큰 bets 검토, exec review 전 narrative 정렬.
**한계/주의사항**: narrative가 강해도 실행 세부는 별도 artifact가 필요하다. 조직이 문서 토론 훈련이 약하면 슬로건 문서로 전락하기 쉽다.
**출처**:
- https://www.aboutamazon.com/news/workplace/an-insider-look-at-amazons-culture-and-processes [dated: 2025-10]
- https://www.amazon.jobs/en/landing_pages/about-amazon%20

### Shape Up Pitch (Basecamp / Ryan Singer)
**요약**: Shape Up의 pitch는 problem, appetite, solution, rabbit holes, no-gos를 핵심 구성요소로 삼는다. 이는 전통적 PRD처럼 세부 요구사항을 완결적으로 적는 문서가 아니라, 팀이 6주 cycle 안에서 자율적으로 마무리할 수 있는 경계(boundary)를 설계하는 문서다.

Shape Up은 범위를 약속하지 않고 appetite를 약속한다. 따라서 pitch는 "무엇을 다 만들 것인가"보다 "이 시간 상자 안에서 어떤 문제를 어느 정도 해상도로 풀 것인가"를 명확히 한다. rabbit holes와 no-gos는 함정과 비범위를 문서 수준에서 먼저 드러낸다는 점에서 특히 실무적이다.

**핵심 질문/포맷/체크리스트**:
- Problem: 지금 해결해야 할 문제는 무엇인가?
- Appetite: 이 문제에 얼마의 시간을 쓸 의향이 있는가?
- Solution: 팀이 출발할 수 있을 만큼 구체적인가?
- Rabbit holes: 빠지기 쉬운 함정은 무엇인가?
- No-gos: 이번 사이클에 하지 않을 것은 무엇인가?

**적용 시점**: 시간 상자형 delivery, 불확실성 높은 개선 과제, scope creep 방지 필요 시.
**한계/주의사항**: Shape Up은 shaping 역량이 약하면 지나치게 모호해질 수 있다. appetite가 있지만 성공 기준이 약하면 결과 평가가 흐려진다.
**출처**:
- https://basecamp.com/shapeup/1.5-chapter-06 [dated: 2025-10]
- https://basecamp.com/shapeup/2.3-chapter-09 [dated: 2025-10]
- https://basecamp.com/shapeup/4.0-appendix-01

### Linear 공개 문서 패턴
**요약**: Linear은 전통적 장문 PRD 템플릿보다 issue template, project template, issue document 중심의 경량 문서 구조를 공개한다. 이는 spec을 planning system 내부에 붙여 두고, issue/project 상태와 분리되지 않게 만드는 방식이다.

실무적으로는 "문서가 따로 있고 실행 보드가 따로 있는" 이중 관리 비용을 줄이는 패턴으로 해석할 수 있다. 특히 템플릿을 통해 필수 필드와 placeholder를 강제하고, project template에 milestone과 issue를 미리 포함시키는 방식은 반복 계획에 강하다.

**핵심 질문/포맷/체크리스트**:
- issue 생성 시 반드시 채워야 할 컨텍스트 필드가 있는가?
- project template에 milestone/issue 구조가 사전 정의되어 있는가?
- spec 문서가 이슈/프로젝트와 링크된 단일 작업면(single workspace) 안에 있는가?
- 템플릿이 triage와 보고 체계까지 고려하는가?

**적용 시점**: 빠른 반복 팀, planning과 execution 통합, 템플릿 기반 운영 정착 시.
**한계/주의사항**: 문서가 지나치게 경량이면 복잡한 전략 문맥을 잃기 쉽다. 템플릿만 복제하고 사고 구조를 복제하지 못하면 품질이 들쭉날쭉해진다.
**출처**:
- https://linear.app/docs/issue-templates
- https://linear.app/docs/project-templates
- https://linear.app/docs/issue-documents

### Notion 공개 Product Spec / PRD 템플릿
**요약**: Notion의 공개 Product Spec/PRD 템플릿은 context, goals/KPI, constraints, assumptions, dependencies, tasks처럼 범용적이지만 실제 협업에 바로 쓸 수 있는 섹션 구조를 제공한다. 특징은 문서 안에서 관련 DB와 페이지를 relation으로 연결하기 쉽다는 점이다.

이 패턴은 깊이 있는 전략 문서보다는 협업형 living document에 적합하다. 개요 문서와 세부 리서치, 사용자 페르소나, task 분해를 링크 구조로 묶어 PRD를 허브 문서로 운영할 수 있다.

**핵심 질문/포맷/체크리스트**:
- Context: 배경을 1~2문장으로 요약했는가?
- Goals/KPI: 성공을 어떻게 측정하는가?
- Constraints: 기술/정책/리소스 제약은 무엇인가?
- Assumptions: 아직 사실이 아닌 전제가 무엇인가?
- Dependencies/Tasks: 선행조건과 실행 항목이 연결돼 있는가?

**적용 시점**: 문서 허브형 운영, cross-functional 협업, linked database 기반 추적.
**한계/주의사항**: 자유도가 높아 표준화가 약해질 수 있다. relation 설계 없이 문서만 늘어나면 탐색 비용이 커진다.
**출처**:
- https://www.notion.so/notion/Product-spec-1cd083403f64437e86631e60c64218d2 [dated: 2025-08]
- https://www.notion.so/Product-Requirement-Document-PRD-143ab0de8afc4ffd9656084c019e0671 [dated: 2025-11]

### Stripe 공개 문서형 spec 패턴
**요약**: 2026-04-14 기준 검증 가능한 Stripe의 공식 "PRD 템플릿" URL은 확인하지 못했다. 대신 Stripe는 제품 가이드와 문서 페이지에서 목적, 핵심 개념, 요구 필드, 예시, 운영 규칙을 매우 구조적으로 제시한다. 공개 산출물 관점에서는 이것이 사실상 spec-like artifact로 기능한다.

이 패턴의 실무적 시사점은 분명하다. 고객-facing 또는 developer-facing 제품은 내부 PRD가 아니라도 공개 문서에서 요구사항 구조가 드러난다. 즉 PM 문서는 배경과 의사결정, 공개 문서는 계약과 사용법으로 분화될 수 있다.

**핵심 질문/포맷/체크리스트**:
- 제품 개념과 스키마가 분리돼 설명되는가?
- 필드별 requirement 수준(required/recommended/optional)이 명확한가?
- 예시 값, validation rule, update rule이 있는가?
- 문서가 integration contract 역할을 수행하는가?

**적용 시점**: API/플랫폼 제품, 외부 개발자 대상 기능, 문서가 곧 제품 계약인 경우.
**한계/주의사항**: 이는 PRD 대체재가 아니라 공개 계약 문서 패턴이다. 내부 의사결정 근거, trade-off, 비범위는 별도 문서가 필요하다.
**출처**:
- https://docs.stripe.com/products-prices/how-products-and-prices-work
- https://docs.stripe.com/agentic-commerce/product-catalog

### Google Design Sprint 산출물
**요약**: Google/GV Design Sprint는 긴 PRD 대신 짧은 기간에 map, sketches, decision, storyboard, prototype, test라는 연속 산출물을 만든다. 이 산출물은 "문서로 합의"보다 "가설을 시각화하고 검증"하는 데 특화되어 있다.

즉 sprint 산출물은 PRD를 대체한다기보다 discovery-to-spec 브리지 역할을 한다. 팀이 문제 공간과 해법 공간을 좁히는 과정 자체가 문서가 되며, 테스트 결과를 바탕으로 뒤늦게 요구사항을 굳힌다.

**핵심 질문/포맷/체크리스트**:
- Map: 사용자와 핵심 흐름이 한 장에 정리됐는가?
- Sketch: 각자 해법을 시각적으로 제안했는가?
- Decide: 어떤 접근을 선택했는가?
- Storyboard: 테스트 가능한 end-to-end 흐름이 있는가?
- Prototype/Test: 실제 사용자 반응으로 검증했는가?

**적용 시점**: 불확실성이 큰 신규 흐름, cross-functional alignment, 빠른 prototype 검증.
**한계/주의사항**: sprint는 실행 결정까지 빠르게 도달하지만, 후속 상세 spec을 자동으로 만들어주진 않는다. 반복 운영 체계 없이 1회성 워크숍으로 끝나면 효과가 급감한다.
**출처**:
- https://www.thesprintbook.com/
- https://www.gv.com/sprint/

## 참고 링크 (전체)
- https://www.aboutamazon.com/news/workplace/an-insider-look-at-amazons-culture-and-processes [dated: 2025-10]
- https://www.amazon.jobs/en/landing_pages/about-amazon%20
- https://basecamp.com/shapeup/1.5-chapter-06 [dated: 2025-10]
- https://basecamp.com/shapeup/2.3-chapter-09 [dated: 2025-10]
- https://basecamp.com/shapeup/4.0-appendix-01
- https://linear.app/docs/issue-templates
- https://linear.app/docs/project-templates
- https://linear.app/docs/issue-documents
- https://www.notion.so/notion/Product-spec-1cd083403f64437e86631e60c64218d2 [dated: 2025-08]
- https://www.notion.so/Product-Requirement-Document-PRD-143ab0de8afc4ffd9656084c019e0671 [dated: 2025-11]
- https://docs.stripe.com/products-prices/how-products-and-prices-work
- https://docs.stripe.com/agentic-commerce/product-catalog
- https://www.thesprintbook.com/ [dated: 2025-10]
- https://www.gv.com/sprint/
