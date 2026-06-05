---
name: plan-risks
description: >
  기획 산출물에 Pre-mortem, Inversion thinking, 인지 편향 체크리스트를 적용하여
  실패 가능성을 사전에 드러낸다. Marty Cagan 의 4-risks(value/usability/feasibility/viability)와
  Gary Klein 의 Pre-mortem 기법 사용.
  "리스크", "pre-mortem", "위험", "failure modes", "편향 체크",
  "inversion", "실패 시나리오", "risk assessment" 같은 요청 시 트리거.
argument-hint: "[기획 파일 경로 또는 기능명]"
user-invocable: true
---

# Gotchas

1. **낙관적 시나리오만 확인 금지** — 기획자는 본능적으로 성공을 가정한다. Pre-mortem 은 의도적으로 "6개월 후 실패했다. 왜?" 로 시작한다.
2. **일반론 금지** — "시장이 바뀔 수 있다" 는 리스크가 아니다. 구체적이고 검증 가능한 시나리오만 기록.
3. **확률/영향 없는 리스크 목록 무의미** — 각 리스크에 Probability(1-5) × Impact(1-5) 점수 필수.
4. **완화책 없는 리스크 나열 금지** — 식별만 하고 액션 없으면 문서로만 남는다. 각 리스크에 Mitigation 또는 Early Signal 명시.
5. **인지 편향 자기진단** — 기획자 자신의 확증편향/매몰비용/계획 오류를 점검. 이건 스킬이 Claude 에게 강제해야 함.
6. **4-risks 카테고리 누락 금지** — Marty Cagan: value(원하는가) / usability(쓸 수 있는가) / feasibility(만들 수 있는가) / viability(비즈니스/법적으로 OK 인가). 4개 모두 답해야 한다.
7. **Inversion 1회 강제** — "성공하려면 무엇을 해야 하나" 가 아니라 "실패하지 않으려면 무엇을 피해야 하나" 로 재구성. Charlie Munger 원칙. 출처: [Farnam Street — Inversion](https://fs.blog/inversion/).
8. **Pre-mortem 은 개별 기록 → 공유 순서** — Gary Klein 의 원래 설계는 각자 먼저 쓰고 그 다음 공유. 즉석 집단 브레인스토밍은 낙관 편향/집단 순응을 못 깬다. commitment 커지기 전 (discovery 후반) 에 돌릴수록 가치 큼. 출처: [HBR — Performing a Project Premortem](https://hbr.org/2007/09/performing-a-project-premortem).
9. **FMEA 는 점수화보다 failure chain 이 먼저** — failure mode × effect × cause × detection × mitigation 5개를 모두 채우지 않으면 문서만 남는다. 제조업 형식 복제는 불필요. 출처: [ASQ — FMEA Overview](https://asq.org/learn-about-quality/process-analysis-tools/overview/fmea.html).
10. **4-risks 는 taxonomy + 테스트 계획이 쌍** — value/usability/feasibility/viability 각 축에 owner 와 실험/프로토타입/분석이 없으면 빈 틀. viability 를 value 에 묻어버리면 맹점 재발. 출처: [Marty Cagan — Four Big Risks](https://www.svpg.com/four-big-risks/), [Value and Viability](https://www.svpg.com/value-and-viability/), [Product Risk Taxonomies](https://www.svpg.com/product-risk-taxonomies/).
11. **편향 완화는 장치 기반** — 확증편향은 decision memo pro/con 강제, 매몰비용은 kill criteria 사전 정의, 계획 오류는 reference class forecasting. "반대 의견도 들었다" 로 부족. 출처: [The Decision Lab — Confirmation Bias](https://thedecisionlab.com/biases/confirmation-bias), [Commitment Bias](https://thedecisionlab.com/biases/commitment-bias), [Planning Fallacy](https://thedecisionlab.com/biases/planning-fallacy), [Availability Heuristic](https://thedecisionlab.com/biases/availability-heuristic), [Authority Bias](https://thedecisionlab.com/biases/authority-bias), [Survivorship Bias](https://thedecisionlab.com/fr-CA/biases/survivorship-bias).
12. **리스크 식별까지만 — 임의 대응 구현/범위 확장 금지 (skill-design-guide §5.5 Scope-Bound)** — 이 스킬의 산출물은 리스크 식별 + 점수 + Mitigation/Early Signal **기술**까지다. 식별된 리스크를 해소하겠다고 요청하지 않은 PRD 수정·재우선순위화·구현 작업으로 임의 진주하지 마라. 4-risks 4축은 모두 답해야 하지만(Gotcha 6), 사용자가 준 기획 범위를 넘어선 인접 기능의 리스크까지 임의로 끌어오는 것은 scope 확장이다. 후속 액션이 필요하면 **먼저 제안하고** 별도 단계로 인계한다 (insights-report #1 excessive_changes 대응). 출처: [Marty Cagan — Four Big Risks](https://www.svpg.com/four-big-risks/).

# Process

## Step 0: 리서치 문서 로드

`docs/planning/risks.md` + `docs/planning/cognitive-biases.md` 로드.

## Step 1: Pre-mortem

출처: [Gary Klein — HBR Pre-mortem](https://hbr.org/2007/09/performing-a-project-premortem).

"6개월 후 이 기능이 처참히 실패했다고 상상하자. 어떤 일이 있었을 것 같은가?"

답변을 브레인스토밍 (최소 10개 시나리오). **개인별로 먼저 쓰고 그 다음 공유** — 즉석 집단 논의는 순응 편향을 못 깬다. 이때 판단 보류 — 황당해 보여도 일단 적는다.

## Step 2: 4-Risks 분류 (Marty Cagan)

출처: [SVPG — Four Big Risks](https://www.svpg.com/four-big-risks/), [Product Risk Taxonomies](https://www.svpg.com/product-risk-taxonomies/).

각 시나리오를 4 카테고리로 분류:

| Risk | 질문 | 예시 시나리오 |
|------|------|--------------|
| **Value** | 사용자가 정말 원하는가 | 출시했는데 아무도 안 씀 |
| **Usability** | 사용자가 쓸 수 있는가 | UI 너무 복잡해서 이탈 |
| **Feasibility** | 기술적으로 만들 수 있는가 | 실시간 요구사항 못 맞춤 |
| **Viability** | 비즈니스·법·정책적으로 OK 한가 | 규제 위반, 단가 안 맞음 |

4개 중 빈 카테고리가 있으면 해당 영역 시나리오 강제 추가.

## Step 3: Probability × Impact 스코어링

```markdown
| ID | Risk | Category | P(1-5) | I(1-5) | Score | Mitigation | Early Signal |
|----|------|----------|--------|--------|-------|------------|--------------|
| R1 | 출시 후 사용률 <5% | Value | 4 | 5 | 20 | 사전 랜딩 페이지 + waitlist | waitlist 신청 수 |
| R2 | 온보딩 이탈률 40%+ | Usability | 3 | 4 | 12 | Figma prototype user test | task completion rate |
```

Score = P × I. 15 이상은 반드시 완화책 + Early Signal 필수.

## Step 4: Inversion

핵심 의사결정 3개를 뒤집어 본다:

| 결정 | Inversion 질문 |
|------|---------------|
| "A 기능을 추가한다" | "A 를 추가하면 무엇이 망가질 수 있는가?" |
| "B 기술 스택을 쓴다" | "B 로 인해 못 하게 되는 것은?" |
| "C 유저를 타깃한다" | "C 유저 외 모두를 쫓아내는 결과가 나오면?" |

## Step 5: 인지 편향 체크리스트

기획자 자신에게:

- [ ] **확증편향**: 이 기획을 지지하는 증거만 모으지 않았는가
- [ ] **매몰비용**: "이미 투자했으니 계속" 논리가 있는가
- [ ] **계획 오류**: Effort 추정이 과거 유사 프로젝트 대비 낙관적이지 않은가
- [ ] **가용성 휴리스틱**: 최근 본 사례에 과도하게 의존하지 않는가
- [ ] **권위편향**: "CEO 가 원해서" 로 프레이밍되지 않았는가
- [ ] **Survivorship**: 성공 사례만 참조하고 실패 사례 안 봤는가

하나라도 ✓ 가 없으면 다시 점검. "없다"고 단정하는 것 자체가 편향 신호.

## Step 6: 저장

`.planning/risks-<slug>.md` 저장:

```markdown
# Risks: <기능>

## Pre-mortem (10 scenarios)
## 4-Risks Matrix
## Scored Risks (table)
## Inversion
## Bias Check
## Decision
- Accept / Mitigate / Kill / Defer
## Review date
```

## Step 7: 다음 단계

- 리스크 Score 합계가 100 넘으면 기획 재작업 권고
- 특정 리스크 검증 실험 필요 → discovery 사이클 재진입
- 감사 → `/plan-audit`

# References

- `docs/planning/risks.md` — Pre-mortem, Inversion, FMEA, 4-risks
- `docs/planning/cognitive-biases.md` — 편향 목록 + PM 실패 사례

주요 1차 출처:
- [HBR — Performing a Project Premortem (Gary Klein)](https://hbr.org/2007/09/performing-a-project-premortem)
- [Farnam Street — Inversion](https://fs.blog/inversion/)
- [ASQ — FMEA](https://asq.org/learn-about-quality/process-analysis-tools/overview/fmea.html)
- [Marty Cagan — Four Big Risks](https://www.svpg.com/four-big-risks/)
- [The Decision Lab — Confirmation Bias](https://thedecisionlab.com/biases/confirmation-bias)
- [The Decision Lab — Planning Fallacy](https://thedecisionlab.com/biases/planning-fallacy)
