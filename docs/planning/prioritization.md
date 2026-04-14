---
name: prioritization
description: 제품 우선순위 결정을 위한 대표 프레임워크와 각 적용 컨텍스트 및 한계 정리
last_updated: 2026-04-14
version: 0.1.0
---

# Prioritization

## 개요
우선순위 프레임워크는 결정을 대신해 주는 기계가 아니라, 팀이 어떤 trade-off를 어떤 언어로 토론할지 정해 주는 도구다. 따라서 같은 backlog라도 제품 단계, 데이터 밀도, 조직 규모에 따라 다른 프레임워크가 맞다.

RICE, ICE, MoSCoW, Kano, WSJF, Opportunity Scoring은 각각 전제가 다르다. RICE/ICE는 backlog 비교에 빠르고, MoSCoW는 범위 협상에 강하며, Kano는 만족도 비대칭을 설명하고, WSJF는 delay cost와 job size를 강조한다. Opportunity Scoring은 고객 미충족 수요를 정량적으로 포착하는 데 적합하다.

## 원칙/방법론별 섹션

### RICE
**요약**: RICE는 Reach, Impact, Confidence, Effort를 결합해 아이디어를 비교하는 프레임워크다. Intercom이 공개한 설명에 따르면, "총 영향/시간"을 비교하는 의도로 설계되었다. Reach를 따로 분리해 Impact와 혼동하지 않는 점이 특징이다.

제품팀에 유용한 이유는 hard-to-compare backlog를 한 표 안에서 빠르게 재정렬할 수 있기 때문이다. 특히 여러 고객군, funnel stage, lifecycle 개선 아이템을 비교할 때 강하다.

**핵심 질문/포맷/체크리스트**:
- Reach: 일정 기간 동안 몇 명/몇 건에 영향을 미치는가?
- Impact: 1인당 효과 크기는 어느 정도인가?
- Confidence: 추정의 신뢰도는 어느 정도인가?
- Effort: person-month 기준으로 얼마나 드는가?
- 같은 기간 단위와 같은 추정 규칙을 쓰고 있는가?

**적용 시점**: 데이터가 어느 정도 있는 성장/최적화 단계, 다수 backlog 비교, roadmap 정렬.
**한계/주의사항**: Reach 추정이 허술하면 정밀한 척하는 숫자놀이가 된다. 전략적 필수 과제나 dependency work는 점수만으로 설명되지 않는다.
**출처**:
- https://www.intercom.com/blog/rice-simple-prioritization-for-product-managers/ [dated: 2018-01]

### ICE
**요약**: ICE는 Impact, Confidence, Ease를 기준으로 빠르게 점수화하는 lightweight prioritization이다. 일반적으로 Sean Ellis가 대중화한 방식으로 알려져 있으며, growth/experimentation 환경에서 속도가 장점이다.

RICE보다 덜 데이터 집약적이어서 초기 단계나 실험 backlog triage에 유리하다. "잘못된 결정의 비용"보다 "결정 지연의 비용"이 큰 상황에서 특히 쓸 만하다.

**핵심 질문/포맷/체크리스트**:
- Impact: 목표 지표에 얼마나 영향을 줄 것 같은가?
- Confidence: 그 판단을 얼마나 믿을 수 있는가?
- Ease: 구현/실험이 얼마나 쉬운가?
- 동일 목표를 향한 아이템끼리만 비교하고 있는가?

**적용 시점**: growth experiment backlog, 초기 제품, 빠른 triage.
**한계/주의사항**: 주관성이 크다. Ease를 선호하다 보면 전략적으로 중요한 어려운 과제가 밀릴 수 있다.
**출처**:
- https://workshopweaver.com/facilitation-methods/ice-scoring

### MoSCoW
**요약**: MoSCoW는 Must have, Should have, Could have, Won't have로 요구사항을 분류하는 협상 프레임워크다. DSDM/Agile Business Consortium 계열에서 널리 쓰이며, 시간 상자 안에서 무엇을 반드시 지켜야 하는지 명확히 하는 데 강하다.

숫자 점수보다 "이번 릴리스에서의 필수성"을 토론하게 만들기 때문에 delivery 범위 협상에 좋다. 특히 deadline이 고정된 프로그램에서 강력하다.

**핵심 질문/포맷/체크리스트**:
- Must: 이게 없으면 릴리스가 실패인가?
- Should: 중요하지만 임시 우회가 가능한가?
- Could: 있으면 좋지만 없어도 되는가?
- Won't: 이번에는 하지 않는가?
- Must가 과도하게 많아져 timebox를 깨고 있지 않은가?

**적용 시점**: release planning, stakeholder negotiation, fixed time/fixed budget delivery.
**한계/주의사항**: 모두가 Must를 주장하면 무력화된다. 가치/리스크/학습 우선순위보다는 범위 합의 도구에 가깝다.
**출처**:
- https://www.agilebusiness.org/businessagility/what-is-dsdm.html [dated: 2025-10]
- https://learning.agilebusiness.org/ [dated: 2025-10]

### Kano Model
**요약**: Kano Model은 기능이 고객 만족에 미치는 영향이 선형이 아니라는 점을 설명한다. 기본요건(must-be), 성능요건(performance), 매력요건(delighters) 등을 구분해 같은 구현 비용이라도 만족도 효과가 다름을 보여준다.

이 프레임은 특히 "왜 어떤 기능은 해도 티가 안 나고, 어떤 기능은 작은데도 큰 호응을 얻는가"를 설명하는 데 유용하다. 따라서 단순 투표보다 고객 반응 구조를 더 잘 드러낸다.

**핵심 질문/포맷/체크리스트**:
- 없으면 불만이 큰 기본요건인가?
- 있으면 비례적으로 만족이 올라가는 성능요건인가?
- 없을 땐 아쉽지 않지만 있으면 기쁨을 주는 매력요건인가?
- 고객 세그먼트별로 분류가 달라지지 않는가?

**적용 시점**: 기능 만족도 연구, roadmap differentiation, 경쟁 parity vs delight 판단.
**한계/주의사항**: 분류는 시간에 따라 변한다. delighter는 곧 basic expectation이 된다. 정성/정량 조사 없이 직감으로 분류하면 왜곡된다.
**출처**:
- https://www.qualtrics.com/fr/articles/strategy-research/modele-kano/

### WSJF (Weighted Shortest Job First)
**요약**: SAFe의 WSJF는 Cost of Delay를 Job Size로 나눈 값으로 우선순위를 정한다. 공식 설명은 User-Business Value, Time Criticality, Risk Reduction and/or Opportunity Enablement를 합산해 Cost of Delay를 구성한다.

이 프레임의 장점은 "큰 일이라도 delay cost가 크면 먼저 해야 한다"는 경제적 관점을 도입한다는 점이다. 특히 포트폴리오/프로그램 수준에서 sequencing에 유용하다.

**핵심 질문/포맷/체크리스트**:
- User-Business Value는 얼마나 큰가?
- Time Criticality가 높은가?
- Risk Reduction / Opportunity Enablement 효과가 있는가?
- Job Size는 상대적으로 얼마나 큰가?
- 현재 비교가 같은 수준의 work item끼리 이뤄지는가?

**적용 시점**: portfolio prioritization, ART/program increment planning, large-scale coordination.
**한계/주의사항**: SAFe 문맥 없이 기계적으로 점수화하면 형식주의가 된다. Job size와 CoD를 상대 추정할 때 정치가 개입되기 쉽다.
**출처**:
- https://scaledagileframework.com/wsjf/ [dated: 2025-10]

### Opportunity Scoring (Ulwick)
**요약**: Opportunity Scoring은 중요도는 높은데 만족도는 낮은 desired outcome을 기회로 보는 ODI 계열 접근이다. 기능 인기보다 미충족 outcome을 우선적으로 찾는 데 초점을 둔다.

이 방식은 discovery와 prioritization을 직접 연결한다. 즉 backlog 항목이 아니라 customer outcome을 우선순위의 단위로 삼게 만든다. 그래서 solution bias를 줄이는 효과가 있다.

**핵심 질문/포맷/체크리스트**:
- 고객에게 이 outcome은 얼마나 중요한가?
- 현재 대안은 이 outcome을 얼마나 만족시키는가?
- 중요도 대비 만족도가 낮은 영역은 어디인가?
- 특정 세그먼트에서 unmet need가 더 두드러지는가?

**적용 시점**: JTBD/ODI 리서치 이후, problem-space prioritization, innovation portfolio.
**한계/주의사항**: 정성적 감으로만 점수화하면 ODI의 장점이 사라진다. solution backlog보다 research quality에 더 민감하다.
**출처**:
- https://strategyn.com/lp/outcome-driven-innovation/
- https://strategyn.com/lp/outcome-based-segmentation/
- https://strategyn.com/odipro/

## 참고 링크 (전체)
- https://www.intercom.com/blog/rice-simple-prioritization-for-product-managers/ [dated: 2018-01]
- https://workshopweaver.com/facilitation-methods/ice-scoring
- https://www.agilebusiness.org/businessagility/what-is-dsdm.html [dated: 2025-10]
- https://learning.agilebusiness.org/ [dated: 2025-10]
- https://www.qualtrics.com/fr/articles/strategy-research/modele-kano/
- https://scaledagileframework.com/wsjf/ [dated: 2025-10]
- https://strategyn.com/lp/outcome-driven-innovation/
- https://strategyn.com/lp/outcome-based-segmentation/
- https://strategyn.com/odipro/
