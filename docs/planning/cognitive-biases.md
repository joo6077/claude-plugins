---
name: cognitive-biases
description: PM가 의사결정에서 자주 맞닥뜨리는 대표 인지편향과 실무적 완화 전략 정리
last_updated: 2026-04-14
version: 0.1.0
---

# Cognitive Biases

## 개요
제품 기획은 불완전한 정보로 반복적으로 판단하는 일이라서, 좋은 프레임워크를 알아도 편향을 피하기 어렵다. 확증편향, 매몰비용, 계획 오류, 가용성 편향, 권위 편향, 서바이벌십 편향은 PM 조직에서 특히 자주 나타난다. 문제는 편향 자체보다, 그것이 "데이터 기반 판단"처럼 위장된다는 점이다.

편향 대응은 개인의 의지보다 팀 운영 장치에 의존해야 한다. 반증 질문, pre-mortem, confidence calibration, red team review, reference class forecasting, kill criteria 같은 메커니즘을 프로세스에 심어야 한다. 아래 편향들은 제품 planning 문맥에서 특히 주의할 만한 것들이다.

## 원칙/방법론별 섹션

### 확증편향 (Confirmation Bias)
**요약**: 확증편향은 기존 믿음에 맞는 증거에 더 주목하고 반대 증거를 덜 다루는 경향이다. 제품팀에서는 "우리가 원래 믿던 방향"에 맞는 인터뷰 인용이나 metric만 채택하는 형태로 자주 나타난다.

초기 solution preference가 강한 팀일수록 위험하다. discovery를 해도 사실상 정답 확인 절차로 전락하기 쉽다.

**핵심 질문/포맷/체크리스트**:
- 이 가설을 반박할 수 있는 증거는 무엇인가?
- 인터뷰/데이터에서 불편한 신호를 별도 섹션으로 기록했는가?
- decision memo에 pro/con이 모두 들어 있는가?

**적용 시점**: discovery synthesis, experiment readout, roadmap review.
**한계/주의사항**: 팀이 "반대 의견도 들었다"고 말하는 것만으로는 부족하다. 실제 결정에 반영되는 구조가 필요하다.
**출처**:
- https://thedecisionlab.com/biases/confirmation-bias

### 매몰비용 / Escalation of Commitment
**요약**: 매몰비용 편향은 이미 들인 시간, 돈, 정치적 자본 때문에 나쁜 결정을 계속 밀어붙이게 만든다. The Decision Lab의 commitment bias 설명처럼, 공개적으로 커밋한 아이디어일수록 접기 어려워진다.

제품팀에서는 특히 "이미 3개월 만들었으니 출시라도 해보자" 같은 논리로 나타난다. 하지만 sunk cost는 미래 가치의 근거가 아니다.

**핵심 질문/포맷/체크리스트**:
- 오늘 처음 본 아이템이라면 같은 결정을 하겠는가?
- kill criteria가 사전에 정의되어 있었는가?
- continuation cost와 opportunity cost를 비교했는가?

**적용 시점**: 장기 프로젝트 중간 점검, MVP 이후 pivot 여부 판단.
**한계/주의사항**: 완화 전략 없이 "유연해지자"는 구호만으로는 효과 없다.
**출처**:
- https://thedecisionlab.com/biases/commitment-bias

### 계획 오류 (Planning Fallacy)
**요약**: 계획 오류는 작업 기간, 비용, 리스크를 과소추정하는 경향이다. Kahneman/Tversky 계열에서 알려졌고, 제품팀에서는 roadmap 낙관주의의 기본 편향이다.

특히 처음 해보는 통합, migration, 조직 간 coordination 작업에서 심해진다. 내부 계획은 best-case narrative를 좋아하지만, 실제로는 대기시간과 의존성이 대부분의 지연을 만든다.

**핵심 질문/포맷/체크리스트**:
- 비슷한 과거 사례(reference class)를 봤는가?
- 낙관/기준/비관 3점 추정을 했는가?
- delivery risk와 coordination risk를 분리했는가?

**적용 시점**: 일정 산정, milestone planning, external commitment 전.
**한계/주의사항**: 개인 경험에만 기대면 반복된다. 팀 차원의 reference class database가 있으면 가장 좋다.
**출처**:
- https://thedecisionlab.com/biases/planning-fallacy

### 가용성 편향 (Availability Bias)
**요약**: 최근 본 사례나 인상 강한 사례가 실제 빈도보다 더 중요해 보이는 편향이다. 제품 planning에서는 가장 최근 VOC, 가장 큰 고객의 불만, 가장 극적인 장애 사례가 roadmap를 과도하게 지배하는 식으로 나타난다.

이 편향은 데이터가 없어서가 아니라, 데이터보다 기억이 더 생생해서 발생한다. 그래서 anecdote와 pattern을 의도적으로 분리해야 한다.

**핵심 질문/포맷/체크리스트**:
- 이 이슈는 반복 패턴인가, 단일 강한 사례인가?
- 최근성(recency)과 빈도(frequency)를 분리해서 보고 있는가?
- 표본 편향이 큰 source를 과대평가하고 있지 않은가?

**적용 시점**: VOC triage, urgent request 대응, incident aftermath planning.
**한계/주의사항**: 정량 데이터가 있어도 스토리텔링이 강한 사례에 끌리기 쉽다.
**출처**:
- https://thedecisionlab.com/biases/availability-heuristic

### 권위 편향 (Authority Bias)
**요약**: 권위 편향은 직급, 전문성, 명성 때문에 주장의 근거보다 발화자를 더 신뢰하는 경향이다. PM 조직에서는 창업자/임원/큰 고객의 의견이 discovery 결과를 압도할 때 나타난다.

권위자 의견은 무시 대상이 아니라 가설 우선순위 입력값이다. 문제는 검증 면제권을 주는 순간 발생한다.

**핵심 질문/포맷/체크리스트**:
- 이 제안은 증거 기반인가, 지위 기반인가?
- 권위자 의견도 동일한 가설 검증 규칙을 적용하는가?
- 회의 구조상 junior dissent가 가능한가?

**적용 시점**: exec review, founder-led product culture, enterprise sales pressure 대응.
**한계/주의사항**: 공개 회의에서 반론이 어려운 조직은 문서 기반 비동기 검토가 더 유리할 수 있다.
**출처**:
- https://thedecisionlab.com/biases/authority-bias

### 서바이벌십 편향 (Survivorship Bias)
**요약**: 서바이벌십 편향은 살아남은 사례만 보고 전체를 오판하는 경향이다. 제품 planning에서는 성공한 경쟁사 사례, 유명한 growth playbook, "그 팀은 이렇게 해서 컸다" 같은 사례를 그대로 일반화할 때 자주 나타난다.

성공 사례에는 보이지 않는 실패 사례와 환경 조건이 빠져 있다. 따라서 벤치마킹은 복제보다 조건 비교로 접근해야 한다.

**핵심 질문/포맷/체크리스트**:
- 같은 시도를 했다가 실패한 사례는 무엇인가?
- 성공 사례의 맥락 조건(시장/채널/브랜드/자본)은 같은가?
- 눈에 보이지 않는 base rate를 확인했는가?

**적용 시점**: 경쟁사 벤치마킹, AI/신기술 adoption, go-to-market copycat 전략.
**한계/주의사항**: 유명 회사의 패턴일수록 더 위험하다. 보이는 사례가 전부가 아니다.
**출처**:
- https://thedecisionlab.com/fr-CA/biases/survivorship-bias

## 참고 링크 (전체)
- https://thedecisionlab.com/biases/confirmation-bias
- https://thedecisionlab.com/biases/commitment-bias
- https://thedecisionlab.com/biases/planning-fallacy
- https://thedecisionlab.com/biases/availability-heuristic
- https://thedecisionlab.com/biases/authority-bias
- https://thedecisionlab.com/fr-CA/biases/survivorship-bias
