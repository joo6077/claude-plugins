---
name: risks
description: 제품 기획 단계에서 실패 가능성을 구조적으로 드러내고 줄이는 리스크 분석 패턴 정리
last_updated: 2026-04-14
version: 0.1.0
---

# Risks

## 개요
제품 기획에서 리스크 관리는 delivery 리스크 추적표를 만드는 일이 아니라, 실패 메커니즘을 설계 초기에 드러내는 일이다. 대부분의 제품 실패는 "몰랐다"보다 "일찍 알 수 있었는데 묻지 않았다"에 가깝다. 그래서 리스크 문서는 의사결정을 늦추기 위한 방어 문서가 아니라, 더 빨리 배울 수 있게 만드는 문서여야 한다.

Pre-mortem, Inversion, Failure Modes(FMEA 계열), Marty Cagan의 4-risks는 서로 다른 질문을 한다. Pre-mortem은 팀이 상상된 실패에서 역으로 원인을 말하게 만들고, Inversion은 실패 조건을 먼저 정의하게 하며, Failure Modes는 고장 형태와 영향을 체계적으로 나열한다. 4-risks는 제품 탐색 리스크를 분류해 실험 우선순위를 정하게 만든다.

## 원칙/방법론별 섹션

### Pre-mortem (Gary Klein)
**요약**: Gary Klein의 pre-mortem은 "프로젝트가 이미 실패했다"고 가정하고, 팀원 각자가 그 실패의 그럴듯한 원인을 적게 하는 기법이다. 목적은 planning phase에서 말하기 어려운 reservations를 안전하게 드러내는 데 있다.

실무적으로 pre-mortem은 낙관 편향과 집단 순응을 깨는 데 특히 좋다. launch 직전보다 discovery 후반, commitment가 커지기 전에 돌릴수록 가치가 크다.

**핵심 질문/포맷/체크리스트**:
- 6~12개월 뒤 이 제품이 실패했다면 가장 그럴듯한 이유는 무엇인가?
- 고객, 시장, UX, 기술, 운영, 법무, go-to-market 중 어디서 무너졌는가?
- 개인별로 먼저 쓰고, 그 다음 공유하는 구조인가? (절차 세부는 [미확인] — 아래 주의사항 참조)
- 나온 원인 중 조기 경보 지표를 정의할 수 있는가?

**적용 시점**: 큰 bets 착수 전, roadmap lock 직전, exec sign-off 전.
**한계/주의사항**: 원인 나열만 하고 대응 실험/지표로 연결하지 않으면 효과가 적다. 위계가 센 조직에서는 퍼실리테이션이 특히 중요하다.

**[미확인] (2026-08-13 확인)**: "개별 기록 → 공유" 같은 절차 세부는 접근 가능한 HBR 본문에서 확인되지 않았다. HBR 로 확인되는 것은 premortem 기법과 저자·발행 시점(Gary Klein · 2007-09)까지이며, 절차 세부는 planning-kit 내부 운영 팁으로 취급한다.
**출처**:
- https://hbr.org/2007/09/performing-a-project-premortem [dated: 2007-09]
- https://store.hbr.org/product/performing-a-project-premortem/F0709A [dated: 2007-09]

### Inversion
**요약**: Inversion은 성공 조건보다 실패 조건을 먼저 정의해 blind spot을 줄이는 사고법이다. 리스크 문맥에서는 "이 결정을 망하게 만드는 조건"을 사전에 명시하는 데 탁월하다.

이 방법은 리스크 레지스터를 채우는 것보다 팀의 판단 프레임을 바꾸는 데 더 유용하다. 특히 확신이 과도한 product review에서 효과가 크다.

**핵심 질문/포맷/체크리스트**:
- 반드시 피해야 할 실패 상태는 무엇인가?
- 어떤 신호가 보이면 즉시 중단/수정해야 하는가?
- no-go 조건과 rollback 조건을 사전 정의했는가?
- 낙관적 가정의 반대편을 충분히 검토했는가?

**적용 시점**: 전략 선택, 투자 판단, launch gating.
**한계/주의사항**: 과도한 방어로만 흐르면 실험 자체를 못 하게 된다. 리스크의 치명도와 회복 가능성을 분리해 보아야 한다.
**출처**:
- https://fs.blog/inversion/ [dated: 2018-10]

### Failure Modes / FMEA
**요약**: FMEA(Failure Mode and Effects Analysis)는 시스템, 제품, 프로세스가 어떤 방식으로 실패할 수 있는지와 그 영향을 구조적으로 분석하는 접근이다. ASQ 설명 기준으로 severity, occurrence, detection 관점이 핵심이다.

제품 기획에 적용할 때는 제조업 형식을 그대로 복제할 필요는 없다. 대신 onboarding, permissions, billing, migration, notification 같은 핵심 흐름의 failure mode를 나열하고, 사용자/운영 영향과 조기 탐지 방법을 적는 식으로 경량화하면 된다.

**핵심 질문/포맷/체크리스트**:
- failure mode: 무엇이 어떤 방식으로 실패하는가?
- effect: 사용자/운영/매출에 어떤 영향을 주는가?
- cause: 왜 그런가?
- detection: 언제, 어떻게 감지할 수 있는가?
- mitigation: 사전 예방 또는 완화 조치는 무엇인가?

**적용 시점**: 결제/권한/데이터 이전 등 치명적 흐름 설계, release readiness review.
**한계/주의사항**: 지나치게 무거우면 문서만 남는다. 점수화보다 치명적 failure chain을 빨리 드러내는 데 집중하는 편이 낫다.
**출처**:
- https://asq.org/learn-about-quality/process-analysis-tools/overview/fmea.html
- https://asq.org/training/failure-mode-and-effects-analysis---managing-risk-fmeaasq

### 4-risks Matrix (Value / Usability / Feasibility / Viability)
**요약**: Marty Cagan의 4-risks는 제품 discovery 리스크를 네 축으로 분류한다. value는 고객이 원할지, usability는 실제로 사용할 수 있을지, feasibility는 우리가 만들 수 있을지, viability는 비즈니스로 성립할지를 본다.

이 분류를 리스크 문서에 넣으면 "리스크 많음"이라는 막연한 표현 대신 어떤 리스크를 누가 줄여야 하는지 더 분명해진다. product/design/engineering의 책임 분담도 자연스럽다.

**핵심 질문/포맷/체크리스트**:
- 현재 가장 큰 리스크 축은 어디인가?
- 각 리스크를 줄이기 위한 실험/프로토타입/분석은 무엇인가?
- 어떤 리스크는 launch 후에, 어떤 리스크는 launch 전에만 검증 가능한가?
- 리스크 축별 owner가 있는가?

**적용 시점**: discovery review, initiative kick-off, go/no-go 판단.
**한계/주의사항**: taxonomy만 있고 테스트 계획이 없으면 빈 틀이다. viability를 value에 묻어버리면 다시 맹점이 생긴다.
**출처**:
- https://www.svpg.com/four-big-risks/ [dated: 2017-12]
- https://www.svpg.com/value-and-viability/ [dated: 2022-02]
- https://www.svpg.com/product-risk-taxonomies/ [dated: 2023-07]

## 참고 링크 (전체)
- https://hbr.org/2007/09/performing-a-project-premortem [dated: 2007-09]
- https://store.hbr.org/product/performing-a-project-premortem/F0709A [dated: 2007-09]
- https://fs.blog/inversion/ [dated: 2018-10]
- https://asq.org/learn-about-quality/process-analysis-tools/overview/fmea.html
- https://asq.org/training/failure-mode-and-effects-analysis---managing-risk-fmeaasq
- https://www.svpg.com/four-big-risks/ [dated: 2017-12]
- https://www.svpg.com/value-and-viability/ [dated: 2022-02]
- https://www.svpg.com/product-risk-taxonomies/ [dated: 2023-07]
