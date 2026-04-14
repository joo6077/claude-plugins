---
name: discovery
description: 제품 발견 단계에서 문제 정의, 기회 탐색, 가설 검증을 구조화하는 핵심 방법론 모음
last_updated: 2026-04-14
version: 0.1.0
---

# Discovery

## 개요
제품 기획의 discovery는 "무엇을 만들까"보다 먼저 "어떤 문제를 누구를 위해 왜 풀어야 하는가"를 다루는 단계다. 이 단계의 산출물은 아이디어 목록이 아니라, 고객의 맥락과 미충족 기회(opportunity), 그리고 그 기회를 해결하는 과정에서 반드시 검증해야 할 가정(assumption)에 대한 구조화된 이해다.

강한 discovery는 인터뷰 메모를 많이 쌓는 것만으로 성립하지 않는다. JTBD(Jobs to Be Done), Continuous Discovery, 5 Whys, Inversion, Lean Canvas, RAT(Riskiest Assumption Test), Marty Cagan의 4-risks 같은 도구를 조합해 문제 정의, 우선 리스크, 실험 설계를 연결해야 한다. 핵심은 "해답을 서둘러 고정하지 않는 것"과 "가장 위험한 가정을 가장 빨리 드러내는 것"이다.

## 원칙/방법론별 섹션

### JTBD (Jobs to Be Done)
**요약**: JTBD는 고객이 제품을 "구매"하는 것이 아니라 특정 상황에서 어떤 진전(progress)을 이루기 위해 제품을 "고용(hire)"한다는 관점이다. Alan Klement는 제품 범주보다 고객이 바꾸고 싶은 삶의 상태를 먼저 보라고 강조하고, Strategyn/Tony Ulwick 계열은 job step과 desired outcome을 분리해 문제를 더 측정 가능하게 다룬다.

JTBD를 discovery에 쓰는 이유는 요구사항 수집을 기능 선호 조사로 축소하지 않기 위해서다. 인터뷰의 초점은 "무엇이 필요하세요?"가 아니라 "무슨 상황에서 기존 방식이 더 이상 충분하지 않았는가?"로 옮겨간다. 이 관점은 대체재를 넓게 보고, 경쟁을 카테고리 밖까지 확장하게 만든다.

**핵심 질문/포맷/체크리스트**:
- 고객은 어떤 상황 변화 때문에 행동을 시작했는가?
- 기존 대안은 무엇이었고, 왜 충분하지 않았는가?
- 고객이 이루고 싶었던 progress는 무엇인가?
- 구매/전환을 당긴 힘(push/pull)과 막는 힘(anxiety/habit)은 무엇인가?
- 기능 요구를 바로 적지 말고 상황, 제약, 원하는 진전으로 재서술했는가?

**적용 시점**: 신규 제품 탐색, 포지셔닝 재정의, 대체재 분석, 메시지/온보딩 개선 전.
**한계/주의사항**: JTBD를 "페르소나 대체재"처럼 쓰면 빈약해진다. 인터뷰를 일반론으로 받지 말고 실제 전환 사례(switching moments) 중심으로 수집해야 한다. ODI(Outcome-Driven Innovation) 스타일로 정량화하지 않으면 우선순위 연결이 약해질 수 있다.
**출처**:
- https://www.alanklement.com/
- https://strategyn.com/about-us/ [dated: 2025-10]
- https://strategyn.com/what-customers-want/ [dated: 2025-10]

### Continuous Discovery (Teresa Torres) / Opportunity Solution Tree
**요약**: Teresa Torres의 Continuous Discovery는 팀이 고객과 매주 접촉하며 작은 조사와 실험을 반복하는 운영 습관이다. 핵심은 product trio가 직접 고객을 만나고, 결과물을 큰 리서치 보고서 대신 작고 잦은 학습 루프로 유지하는 것이다.

Opportunity Solution Tree(OST)는 이 discovery 흐름을 시각적으로 고정하는 도구다. 원하는 outcome을 루트에 두고, 그 outcome에 영향을 주는 opportunity를 분기시키며, 각 opportunity 아래에 solution과 assumption test를 연결한다. 그래서 discovery가 "좋은 아이디어 회의"가 아니라 "결과와 가설의 연결 구조"가 된다.

**핵심 질문/포맷/체크리스트**:
- 우리가 추적하는 desired outcome은 무엇인가?
- 고객 인터뷰에서 반복적으로 드러난 opportunity는 무엇인가?
- 각 opportunity 아래에 최소 2개 이상의 solution을 놓았는가?
- 각 solution의 숨은 가정은 무엇이며, 어떤 assumption test로 검증할 것인가?
- 팀이 최근 데이터 포인트 없이 의사결정하고 있지 않은가?

**적용 시점**: discovery 운영체계 구축, 고객 인터뷰 정례화, 아이디어 과잉 상태에서 구조화가 필요할 때.
**한계/주의사항**: OST는 시각화 도구이지 진실 보증 장치가 아니다. 얕은 인터뷰를 체계적으로 정리해도 통찰이 깊어지지는 않는다. outcome 정의가 흐리면 전체 트리가 기능 분류표로 붕괴한다.
**출처**:
- https://www.producttalk.org/glossary-discovery-continuous-discovery/
- https://www.producttalk.org/glossary-discovery-opportunity-solution-tree/
- https://www.producttalk.org/2023/11/benefits-of-opportunity-solution-trees/ [dated: 2023-11]

### 5 Whys
**요약**: 5 Whys는 표면 증상에서 멈추지 않고 반복적으로 "왜?"를 물어 근본 원인(root cause)에 도달하려는 문제 분석 기법이다. 중요한 것은 숫자 5 자체가 아니라, 재발을 막는 countermeasure가 가능한 수준까지 인과 사슬을 추적하는 태도다.

제품 discovery에서는 특히 KPI 하락, 온보딩 이탈, 사용 저하 같은 현상을 기능 추가로 바로 해석하지 않도록 막는 데 유용하다. "사용자가 이 기능을 안 쓴다"를 종착점으로 두지 않고, 채택되지 않는 맥락과 제약을 더 깊게 판다.

**핵심 질문/포맷/체크리스트**:
- 문제를 관찰 가능한 현상으로 한 문장에 적었는가?
- 각 why의 답변이 추측이 아니라 데이터/관찰에 근거하는가?
- 사람 탓으로 끝나지 않고 시스템/프로세스 원인까지 내려갔는가?
- 해결책(solution) 대신 countermeasure를 설계했는가?
- 복합 원인 문제에서 단일 인과로 과도 단순화하지 않았는가?

**적용 시점**: 특정 실패 현상 원인 분석, 품질/전환 저하, 반복 장애 회고.
**한계/주의사항**: 다변량 문제에는 단독 사용이 약하다. 유도 질문이나 정치적 방어가 개입되면 가짜 원인을 강화한다. 인터뷰 문제 탐색과 운영 장애 분석을 같은 깊이로 취급하지 말아야 한다.
**출처**:
- https://www.lean.org/lexicon-terms/5-whys/ [dated: 2025-10]
- https://www.lean.org/the-lean-post/articles/five-whys-animation/ [dated: 2018-07]

### Inversion
**요약**: Inversion은 "성공하려면 무엇을 할까?" 대신 "실패하려면 무엇이 일어나야 할까?"를 먼저 묻는 사고법이다. Charlie Munger 계열의 정신모형으로 널리 알려져 있으며, discovery에서는 낙관적 해답 생성보다 실패 조건과 금지 조건(no-go)을 더 명확히 만드는 데 강하다.

제품 팀은 대개 비전과 해법을 말하는 데 익숙하지만, inversion을 적용하면 시장 오판, 채널 미스매치, 규제 위반, 온보딩 마찰, 데이터 부재 같은 실패 메커니즘을 더 빨리 열거할 수 있다. 이는 pre-mortem, RAT, 4-risks와 특히 궁합이 좋다.

**핵심 질문/포맷/체크리스트**:
- 이 제품이 12개월 뒤 실패했다면 무엇 때문인가?
- 고객이 시도조차 하지 않게 만드는 조건은 무엇인가?
- 우리가 꼭 검증해야 하는 "치명적 반증"은 무엇인가?
- 성공 조건보다 실패 조건이 더 구체적으로 기술되어 있는가?
- no-go 기준을 사전에 합의했는가?

**적용 시점**: 아이디어 초반, 투자/개발 착수 전, 의사결정 편향이 강한 팀 정렬.
**한계/주의사항**: 지나치면 보수주의로 흐른다. 모든 리스크를 동일하게 취급하지 말고 치명도와 가역성을 분리해야 한다.
**출처**:
- https://fs.blog/inversion/ [dated: 2018-10]

### Lean Canvas
**요약**: Lean Canvas는 Ash Maurya가 Business Model Canvas를 스타트업/신규 제품 탐색용으로 재구성한 1페이지 모델이다. 문제, 고객 세그먼트, 고유 가치 제안, 해결책, 채널, 수익, 비용, 핵심 지표, unfair advantage를 한 화면에 정리해 아이디어를 가설 묶음으로 바꾼다.

Discovery에서 Lean Canvas의 강점은 아이디어를 설명 문서가 아니라 검증 대상 가정 체계로 바꾸는 데 있다. 특히 팀이 문제-고객-해결책을 섞어 말하고 있을 때 분해력이 좋다. 이후 RAT와 연결해 어떤 블록이 가장 위험한지 고르는 데 쓴다.

**핵심 질문/포맷/체크리스트**:
- 고객 세그먼트와 문제를 분리해 적었는가?
- 문제 1~3개가 실제로 빈번하고 중요한가?
- UVP(Unique Value Proposition)가 기능 설명이 아니라 차별적 가치 설명인가?
- 핵심 지표가 vanity metric이 아닌가?
- 한 canvas에 여러 사업모델을 섞지 않았는가?

**적용 시점**: 신규 아이디어 초기 구조화, 팀 합의 초안, 투자/실험 준비.
**한계/주의사항**: 문서 완성도가 높아도 검증이 끝난 것이 아니다. 한 페이지에 맞추느라 중요한 제약을 과도 단순화할 수 있다.
**출처**:
- https://leanstack.com/
- https://leanstack.com/articles/3-mental-models-for-continuous-innovation
- https://leanstack.com/articles/the-lean-canvas-diagnostic-part-2-of-7---structure

### RAT (Riskiest Assumption Test)
**요약**: RAT는 제품/비즈니스 모델의 핵심 가정 중 가장 위험한 가정을 먼저 식별하고, 그것을 가장 싼 방식으로 검증하는 접근이다. "무엇을 더 만들까"보다 "무엇이 틀리면 전체가 무너지는가"를 먼저 묻는다.

Ash Maurya 계열의 실무에서는 Lean Canvas의 블록들을 훑으며 desirability, viability, feasibility 관점에서 가장 큰 취약 가정을 찾고, 그에 맞는 실험을 설계한다. RAT의 목적은 certainty를 얻는 것이 아니라, 값비싼 잘못을 싼 비용으로 빨리 드러내는 것이다.

**핵심 질문/포맷/체크리스트**:
- 이 아이디어가 실패한다면 가장 그럴듯한 이유는 무엇인가?
- 현재 단계에서 가장 위험한 가정은 desirability, viability, feasibility 중 어디에 있는가?
- 그 가정을 문서 문장 대신 관찰 가능한 형태로 바꿨는가?
- 가장 싼 실험은 무엇인가: 인터뷰, 클릭 테스트, smoke test, concierge, prototype?
- 학습 기준과 kill criteria를 미리 정했는가?

**적용 시점**: Lean Canvas 작성 직후, discovery backlog 정렬, MVP 범위 조정 전.
**한계/주의사항**: 팀이 "쉽게 검증 가능한 가정"만 고르면 RAT가 아니라 comfort test가 된다. 여러 리스크를 섞어 한 실험에 우겨 넣으면 해석력이 떨어진다.
**출처**:
- https://leanstack.com/articles/the-lean-canvas-diagnostic---part-3-of-7-identify-riskiest-assumptions
- https://leanstack.com/articles/the-lean-canvas-diagnostic---part-4-of-7-desirability-stress-testing
- https://leanstack.com/articles/the-lean-canvas-diagnostic---part-6-of-7-feasibility

### Marty Cagan 4-risks
**요약**: Marty Cagan은 discovery의 핵심을 네 가지 리스크, 즉 value, usability, feasibility, viability로 정리한다. 좋은 아이디어보다 중요한 것은 이 네 축에서 "왜 실패할 수 있는지"를 조기에 파악하는 것이다.

이 프레임은 PM이 value/viability, 디자이너가 usability, 엔지니어가 feasibility를 주도적으로 다루게 만든다. 그래서 discovery가 PM 문서 작업이 아니라 cross-functional risk reduction 활동이 된다.

**핵심 질문/포맷/체크리스트**:
- 고객이 실제로 원하고 사용할 것인가? (value)
- 사용자가 이해하고 수행할 수 있는가? (usability)
- 주어진 기술/시간/역량으로 구현 가능한가? (feasibility)
- 판매, 법무, 수익, 브랜드, 운영 측면에서 성립하는가? (viability)
- 네 리스크 중 현재 가장 큰 축은 무엇이고, 왜 그런가?

**적용 시점**: discovery 전체의 기본 리스크 분류, prototype/experiment 설계, go/no-go 리뷰.
**한계/주의사항**: 리스크 taxonomy는 우선순위 판단 도구이지 점수놀이 도구가 아니다. 모든 축을 똑같이 조사하려 하면 속도가 죽는다.
**출처**:
- https://www.svpg.com/four-big-risks/ [dated: 2017-12]
- https://www.svpg.com/product-risk-taxonomies/ [dated: 2023-07]
- https://www.svpg.com/discovery-judgement/ [dated: 2020-09]

## 참고 링크 (전체)
- https://www.alanklement.com/
- https://strategyn.com/about-us/ [dated: 2025-10]
- https://strategyn.com/what-customers-want/ [dated: 2025-10]
- https://www.producttalk.org/glossary-discovery-continuous-discovery/
- https://www.producttalk.org/glossary-discovery-opportunity-solution-tree/
- https://www.producttalk.org/2023/11/benefits-of-opportunity-solution-trees/ [dated: 2023-11]
- https://www.lean.org/lexicon-terms/5-whys/ [dated: 2025-10]
- https://www.lean.org/the-lean-post/articles/five-whys-animation/ [dated: 2018-07]
- https://fs.blog/inversion/ [dated: 2018-10]
- https://leanstack.com/
- https://leanstack.com/articles/3-mental-models-for-continuous-innovation
- https://leanstack.com/articles/the-lean-canvas-diagnostic-part-2-of-7---structure
- https://leanstack.com/articles/the-lean-canvas-diagnostic---part-3-of-7-identify-riskiest-assumptions
- https://leanstack.com/articles/the-lean-canvas-diagnostic---part-4-of-7-desirability-stress-testing
- https://leanstack.com/articles/the-lean-canvas-diagnostic---part-6-of-7-feasibility
- https://www.svpg.com/four-big-risks/ [dated: 2017-12]
- https://www.svpg.com/product-risk-taxonomies/ [dated: 2023-07]
- https://www.svpg.com/discovery-judgement/ [dated: 2020-09]
