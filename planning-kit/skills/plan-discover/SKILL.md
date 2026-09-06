---
name: plan-discover
description: >
  아이디어를 받아 소크라테스식 질문으로 문제·사용자·가정·성공기준을 드러낸다.
  JTBD(Jobs-To-Be-Done), 5 Whys, Riskiest Assumption Test 를 조합한다.
  "기획 시작", "새 기능 아이디어", "이거 만들까?", "문제 정의",
  "discovery", "JTBD", "why needed", "가정 점검" 같은 요청 시 트리거.
  이미 PRD 작성 단계면 plan-prd 사용. 단순 기능 수정에는 트리거하지 않는다.
argument-hint: "[아이디어 한 줄 설명]"
user-invocable: true
---

# Gotchas

1. **바로 해결책으로 점프 금지** — 사용자가 "X 만들고 싶다" 하면 What/How 가 아니라 Why/Who/When 부터 묻는다. 해결책 수렴은 PRD 단계에서 한다.
2. **한 번에 모든 질문 금지** — 질문 묶음을 단계별로 제시하고 답을 받은 뒤 다음 단계로 넘어간다. 10개 질문을 한꺼번에 던지면 사용자가 지친다.
3. **답변 누락 시 진행 거부** — Problem / User / Job / Success Metric 중 하나라도 비어 있으면 PRD 로 넘어가지 마라. "이 정보 없이 PRD 쓰면 추측이 된다"를 명시하고 재질문.
4. **가정을 사실로 오인 금지** — 사용자가 "사용자는 X 를 원합니다" 라고 하면 "어떻게 확인했는가?" 로 되물어라. 미검증 가정은 Riskiest Assumption 섹션으로 분리한다.
5. **추상 질문 금지** — "타깃은 누구인가?" 보다 "최근에 이 문제를 겪은 구체적 인물 한 명을 묘사해줘 (역할/맥락/감정)" 가 낫다. Teresa Torres 의 "specific story" 원칙.
6. **JTBD 오용 주의** — Job 은 "제품 기능" 이 아니라 "사용자가 해결하려는 상황" 이다. "버튼을 누른다" 는 Job 이 아니다. "주말에 가족과 영화를 보기로 했는데 뭘 볼지 모른다" 가 Job.
7. **성공 지표 없이 진행 금지** — "좋아지면 좋겠다" 는 지표가 아니다. 반드시 관찰 가능한 leading/lagging 지표 각 1개 이상을 받아낸다.
8. **Codex/Context7 조회 생략 금지** — JTBD 프레임워크 적용 시 `docs/planning/discovery.md` 의 최신 정의를 반드시 참조하라.
9. **JTBD 를 페르소나 대체재로 쓰지 마라** — 일반론 인터뷰 금지, 실제 전환 사례(switching moments) 중심으로 수집. ODI 스타일 정량화가 없으면 우선순위 연결이 약해진다. 출처: [Alan Klement](https://www.alanklement.com/), [Strategyn](https://strategyn.com/what-customers-want/).
10. **OST 는 통찰을 보증하지 않는다** — Opportunity Solution Tree 는 시각화일 뿐, outcome 정의가 흐리면 전체 트리가 기능 분류표로 붕괴한다. 매주 고객 접촉 + 작은 실험 루프 없이 OST 만 그리지 마라. 출처: [Teresa Torres — Continuous Discovery](https://www.producttalk.org/glossary-discovery-continuous-discovery/), [Opportunity Solution Tree](https://www.producttalk.org/glossary-discovery-opportunity-solution-tree/).
11. **5 Whys 단독 사용 금지 (다변량 문제)** — 숫자 5 가 아니라 countermeasure 수준까지 인과 사슬을 추적한다. 유도 질문/정치적 방어가 개입되면 가짜 원인을 강화한다. 사람 탓으로 끝내지 말고 시스템/프로세스 원인까지 내려갈 것. 출처: [Lean Enterprise Institute — 5 Whys](https://www.lean.org/lexicon-terms/5-whys/).
12. **RAT 가 comfort test 로 전락하지 않게** — "쉽게 검증 가능한 가정"만 고르면 RAT 가 아니다. desirability / viability / feasibility 중 실패 시 전체가 무너지는 가정을 고르고, kill criteria 를 미리 정해라. 출처: [Leanstack RAT 가이드](https://newsletter.leanstack.com/p/the-lean-canvas-diagnostic-3-identify).
13. **편향 완화는 개인 의지가 아니라 장치로** — 확증편향/매몰비용/계획오류는 pre-mortem, kill criteria, reference class forecasting, red team review 같은 운영 장치로만 억제된다. "반대 의견도 들었다"만으로는 부족 — decision memo 에 pro/con 명시 구조를 강제하라. 출처: [The Decision Lab — Confirmation Bias](https://thedecisionlab.com/biases/confirmation-bias), [Commitment Bias](https://thedecisionlab.com/biases/commitment-bias).
14. **discovery 단계 범위 유지 — 다음 단계로 임의 진주 금지 (skill-design-guide §5.5 Scope-Bound)** — discovery 의 산출물은 Problem/User/Job/Success Metric/Riskiest Assumption 이다. 사용자가 discovery 만 요청했는데 PRD·솔루션·스토리·우선순위를 임의로 작성해 진행하지 마라 (Gotcha 1 의 "해결책 점프 금지" 와 짝). 다음 단계로 넘어갈 준비가 됐으면 plan-prd 인계 여부를 **먼저 묻고** 진행한다. 요청하지 않은 추가 인터뷰 질문 라운드도 임의 확장이다 (insights-report #1 excessive_changes / over-exploration 대응). 출처: [Teresa Torres — Continuous Discovery](https://www.producttalk.org/glossary-discovery-continuous-discovery/).

# Process

## Step 0: 전단계 확인

아이디어가 아직 모호하다면 `/plan-ideate` 먼저 권고한다. plan-discover 는 "탐색할 문제 후보 하나" 가 정해진 상태를 전제한다.

## Step 0.5: 리서치 문서 로드

`docs/planning/discovery.md` + (있으면) `docs/planning/ideation.md` 로드. 없으면 `/planning-research` 권고.

## Step 1: Problem (3문항)

다음을 순서대로 질문한다:

1. **현재 상황에서 누가 / 언제 / 어떤 맥락에서 불편을 겪는가?** (specific story 요구)
2. **그 사람은 지금 그 문제를 어떻게 해결하고 있는가?** (workaround · competing solution)
3. **해결 못 하면 어떤 결과가 생기는가?** (urgency 확인)

답이 추상적이면 구체 사례로 되묻는다.

## Step 2: Job To Be Done (JTBD 포맷)

다음 템플릿으로 작성을 요청 — 출처: [Alan Klement JTBD](https://www.alanklement.com/), [Strategyn ODI](https://strategyn.com/what-customers-want/):

```text
When <상황>,
I want to <동기/욕구>,
so I can <기대 결과>.
```

Job 은 제품 독립적이어야 한다 — 우리 앱이 없어도 존재하는 동기여야 한다. 인터뷰는 "무엇이 필요한가" 가 아니라 "무슨 상황에서 기존 방식이 더 이상 충분하지 않았는가" 로 묻는다.

## Step 3: User / Persona

- 주 사용자 1명을 구체적으로 묘사 (직무, 하루 루틴에서 이 문제의 위치, 기술 수준)
- Non-user: 누가 쓰지 않을 것인가 (scope 축소)
- Jobs per persona 가 2개 이상이면 persona 분리 검토

## Step 4: Riskiest Assumption (가정 추출)

"이 기획이 실패한다면, 어떤 가정이 틀렸기 때문인가?" 질문. Inversion 사고법 (출처: [Farnam Street — Inversion](https://fs.blog/inversion/)) 으로 실패 조건을 먼저 기술.

3가지 범주로 분류 — 출처: [Marty Cagan — Four Big Risks](https://www.svpg.com/four-big-risks/), [Product Risk Taxonomies](https://www.svpg.com/product-risk-taxonomies/):
- **Desirability** — 사용자가 정말 원하는가 (value + usability)
- **Viability** — 비즈니스적으로 말이 되는가 (판매/법무/수익/브랜드/운영)
- **Feasibility** — 기술적으로 가능한가

각 범주당 가장 위험한 가정 1개씩 명시. 실험 설계는 [Leanstack RAT](https://newsletter.leanstack.com/p/the-lean-canvas-diagnostic-3-identify) 기준으로 kill criteria 포함.

## Step 5: Success Metric

- **Leading**: 1주일 내 관찰 가능한 행동 지표 (예: 기능 사용률, 세션당 이벤트 수)
- **Lagging**: 1-3개월 후 결과 지표 (예: 리텐션, 전환율, NPS)

각 지표에 "이 숫자가 X 가 되면 성공" 기준선 포함.

## Step 6: 산출물 저장

`.planning/discover-<slug>.md` 에 저장. 포맷:

```markdown
# Discovery: <제목>
## Problem
## JTBD
## User
## Assumptions (3 risks)
## Success Metrics
## Open Questions
```

Open Questions 이 5개 이상이면 "다음 세션에서 /plan-discover 재실행" 권고.

## Step 7: 다음 단계 제안

- 충분히 수렴됐으면 `/plan-prd` 권고
- 가정이 너무 많으면 "간단한 실험/인터뷰 먼저" 권고
- 우선순위 고민이면 `/plan-prioritize`

# References

- `docs/planning/discovery.md` — JTBD, Continuous Discovery, Marty Cagan 4-risks 정리
- `docs/planning/cognitive-biases.md` — 발견 단계의 편향 목록

주요 1차 출처:
- [Alan Klement — JTBD](https://www.alanklement.com/)
- [Teresa Torres — Continuous Discovery / OST](https://www.producttalk.org/glossary-discovery-opportunity-solution-tree/)
- [Marty Cagan — Four Big Risks](https://www.svpg.com/four-big-risks/)
- [Leanstack — RAT](https://newsletter.leanstack.com/p/the-lean-canvas-diagnostic-3-identify)
- [Lean Enterprise Institute — 5 Whys](https://www.lean.org/lexicon-terms/5-whys/)
- [Farnam Street — Inversion](https://fs.blog/inversion/)
- [The Decision Lab — Confirmation Bias](https://thedecisionlab.com/biases/confirmation-bias)
