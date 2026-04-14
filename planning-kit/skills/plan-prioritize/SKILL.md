---
name: plan-prioritize
description: >
  스토리 또는 기능 후보를 받아 RICE/Kano/WSJF/MoSCoW 중 컨텍스트에 맞는 프레임워크를 선택해 스코어링한다.
  "우선순위", "prioritization", "RICE", "Kano", "WSJF", "MoSCoW",
  "뭐부터 할까", "백로그 정렬", "priority scoring" 같은 요청 시 트리거.
  프레임워크 선택이 편향되지 않도록 상황 기반으로 추천하고 근거를 제시.
argument-hint: "[스토리 파일 또는 항목 목록]"
user-invocable: true
---

# Gotchas

1. **단일 프레임워크 강요 금지** — RICE 가 만능이 아니다. 기능 성격에 따라 Kano / WSJF / MoSCoW 가 더 적합할 수 있다. 선택 근거 명시.
2. **Confidence 를 임의로 100% 두지 마라** — RICE 의 Confidence 가 50% 이하면 discovery/실험 먼저. 100% 로 셋팅하면 가중치가 사라진다.
3. **Effort 추정을 엔지니어 없이 금지** — 기획자 혼자 추정한 Effort 는 편향된다. 최소 "엔지니어 리뷰 대기" 플래그 붙이기.
4. **선형 합산의 함정** — RICE score 가 비슷한 두 항목이면 숫자 차이로 결정하지 말고 리스크/의존성 확인.
5. **Kano 의 Basic 무시 금지** — Delighter 에 집중하다가 Basic(당연 기능) 누락하면 NPS 즉시 붕괴. Basic 이 먼저 채워져야 한다.
6. **WSJF 는 SAFe 컨텍스트에서만** — Job size 가 의미 있는 조직(아지일 트레인) 밖에서는 RICE 가 낫다.
7. **스코어 결과를 신탁처럼 믿지 마라** — 스코어는 토론 시작점이지 결정이 아니다. Top 3 는 반드시 사람이 재검토.
8. **RICE 의 Reach 가 허술하면 정밀한 척 숫자놀이** — 같은 기간 단위/같은 추정 규칙을 강제해야 한다. 전략 필수 과제나 dependency work 는 점수만으로 설명 안 된다. 출처: [Intercom — RICE](https://www.intercom.com/blog/rice-simple-prioritization-for-product-managers/).
9. **ICE 는 Ease 편향 경계** — Ease 가 높은 것만 고르다 보면 전략적으로 중요한 어려운 과제가 밀린다. 같은 목표를 향한 아이템끼리만 비교. 출처: [Workshop Weaver — ICE Scoring](https://workshopweaver.com/facilitation-methods/ice-scoring).
10. **MoSCoW — Must 가 전부면 무력화** — 모두가 Must 주장하면 협상 도구로 기능하지 못한다. 가치/리스크/학습 우선순위보다는 범위 합의 도구임을 명시. 출처: [Agile Business — DSDM/MoSCoW](https://www.agilebusiness.org/businessagility/what-is-dsdm.html).
11. **Kano 분류는 시간에 따라 변한다** — Delighter 는 곧 Basic expectation 이 된다. 정성/정량 조사 없이 직감 분류하면 왜곡. 세그먼트별 재분류 필요. 출처: [Qualtrics — Kano Model](https://www.qualtrics.com/fr/articles/strategy-research/modele-kano/).
12. **WSJF 는 SAFe 문맥이 없으면 형식주의** — Job size 와 CoD 상대 추정에 정치 개입되기 쉬움. portfolio/program 수준이 아니면 RICE 가 낫다. 출처: [SAFe — WSJF](https://scaledagileframework.com/wsjf/).
13. **Opportunity Scoring 은 research quality 에 민감** — 정성 감으로만 점수화하면 ODI 장점 사라진다. 중요도↑+만족도↓ 구간에 집중. 출처: [Strategyn ODI](https://strategyn.com/lp/outcome-driven-innovation/).

# Process

## Step 0: 리서치 문서 로드

`docs/planning/prioritization.md` (RICE, Kano, WSJF, MoSCoW, Opportunity Scoring) 로드.

## Step 1: 프레임워크 선택

상황 → 추천:

| 상황 | 프레임워크 | 이유 | 출처 |
|------|-----------|------|------|
| 기능 많고 유사한 성격 | RICE | 선형 비교에 강함 | [Intercom](https://www.intercom.com/blog/rice-simple-prioritization-for-product-managers/) |
| Growth 실험 triage | ICE | 속도 우선 | [Workshop Weaver](https://workshopweaver.com/facilitation-methods/ice-scoring) |
| 사용자 만족도 중심 | Kano | 기본/성능/매력 구분 | [Qualtrics](https://www.qualtrics.com/fr/articles/strategy-research/modele-kano/) |
| 대규모 아지일 (팀 5+) | WSJF | Cost of Delay 포함 | [SAFe](https://scaledagileframework.com/wsjf/) |
| 출시 직전 스코프 조정 | MoSCoW | Must/Should/Could/Won't 명확 | [DSDM](https://www.agilebusiness.org/businessagility/what-is-dsdm.html) |
| 문제 공간 탐색 | Opportunity Scoring | Importance vs Satisfaction gap | [Strategyn ODI](https://strategyn.com/lp/outcome-driven-innovation/) |

사용자에게 추천 + 근거 제시 후 선택받는다. 강요 금지.

## Step 2: 스코어링

### RICE

| 항목 | 정의 | 단위 |
|------|------|------|
| Reach | 분기당 영향받을 유저/이벤트 수 | 숫자 |
| Impact | 0.25 / 0.5 / 1 / 2 / 3 중 선택 | 이산값 |
| Confidence | 0-100% | 근거 링크 필수 |
| Effort | person-month | 추정값 |

`Score = (Reach × Impact × Confidence) / Effort`

### Kano

각 항목에 Functional/Dysfunctional 질문 쌍으로 분류:
- Must-be (Basic)
- One-dimensional (Performance)
- Attractive (Delighter)
- Indifferent
- Reverse

Basic 미충족은 순위 무관 즉시 선행.

### WSJF (SAFe)

`WSJF = Cost of Delay / Job Size`
`Cost of Delay = User Value + Time Criticality + Risk Reduction`

피보나치 수열(1/2/3/5/8/13)로 각 항목 추정.

### MoSCoW

- **Must have**: 출시 차단 (없으면 릴리스 불가)
- **Should have**: 중요하지만 없어도 릴리스 가능
- **Could have**: 여유 있으면
- **Won't have**: 이번엔 안 함 (명시적 제외)

Must 가 전체의 60% 넘으면 스코프 재검토.

## Step 3: 정렬 + 검토

스코어 표 생성:

```markdown
| ID | 제목 | Reach | Impact | Confidence | Effort | Score |
|----|------|-------|--------|------------|--------|-------|
```

Top 3 에 대해:
- 의존성 체크
- 리스크(`/plan-risks` 연계) 점검
- 엔지니어 Effort 검증 플래그

## Step 4: 저장

`.planning/priorities-<slug>.md` 저장. 포맷:

```markdown
# Priorities: <기능 그룹>

## Framework: RICE
## Scores
| ... |
## Top 3 (human review)
## Decision
## Next review date
```

## Step 5: 다음 단계

- 리스크 상세 → `/plan-risks`
- GitHub Milestone 동기화 → `/plan-sync-github`
- 완성도 감사 → `/plan-audit`

# References

- `docs/planning/prioritization.md` — RICE, ICE, Kano, WSJF, MoSCoW, Opportunity Scoring

주요 1차 출처:
- [Intercom — RICE](https://www.intercom.com/blog/rice-simple-prioritization-for-product-managers/)
- [Workshop Weaver — ICE](https://workshopweaver.com/facilitation-methods/ice-scoring)
- [Agile Business — DSDM/MoSCoW](https://www.agilebusiness.org/businessagility/what-is-dsdm.html)
- [Qualtrics — Kano](https://www.qualtrics.com/fr/articles/strategy-research/modele-kano/)
- [SAFe — WSJF](https://scaledagileframework.com/wsjf/)
- [Strategyn — ODI/Opportunity Scoring](https://strategyn.com/lp/outcome-driven-innovation/)
