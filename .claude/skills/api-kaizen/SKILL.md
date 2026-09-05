---
name: api-kaizen
description: >
  api-kit 스킬 5종과 references 를 docs/api/ 리서치 문서 기준으로 점진 개선한다.
  이 레포 개발용 스킬이며 api-kit 플러그인에 포함되지 않는다.
  tone-kaizen, rust-kaizen 과 동일한 패턴.
  "/api-kaizen", "API 킷 카이젠", "api-kit 스킬 개선" 같은 요청 시 트리거.
  리서치 문서 자체의 갱신에는 트리거하지 않는다 — /api-research 를 사용한다.
argument-hint: "[skill-name]"
user-invocable: true
---

# Gotchas

1. **문서가 먼저다** — `docs/api/` 가 SSOT 다. 스킬에만 있고 문서에 없는 규칙을 발견하면
   스킬을 고치는 게 아니라 **먼저 문서에 근거가 있는지 확인**한다. 없으면 `/api-research` 를 돌린다.
2. **`pin` 의 의미를 되돌리지 마라** — '값 고정' 이 아니라 '경로별 명시 assertion' 이다.
   2026-09-04 에 두 번 틀린 뒤 리서치로 확정했다. 되돌리려면 설계문서 §9.2 · UI 시안 ·
   `CLAUDE.md` Skills Reference 를 **함께** 고쳐야 한다.
3. **Phase 선별부터** — 신선도가 곧 새 신호는 아니다. 직전 사이클과 중복되면 고신호 스킬만 고른다.
   `.harness/.meta/` 의 직전 판정을 먼저 읽어라.
4. **자기 산출물을 자기가 통과시키지 마라** — 개선 후 측정할 때 지표가 **실패를 실제로 잡는지**
   먼저 확인한다(음성 대조). 범위가 빈 grep 이 0 건을 돌려주는 것을 "위반 없음" 으로 읽은 사고가 있다.
5. **트리거 키워드 배타성** — 스킬 description 을 손대면 5 종 전체의 트리거 키워드를
   set intersection **과** substring containment 양쪽으로 재검사한다. 한쪽만 보면 놓친다.

# Process

## Step 0: 트리거 판정

인자로 스킬명을 주면 그 스킬만, 없으면 5 종 전체를 대상으로 한다.

```text
api-init · api-probe · api-contract · api-verify · api-ui  + agents/api-reviewer.md
```

## Step 1: 사전 측정

개선 전 상태를 **명령 출력으로** 기록한다. 서술로 대체하지 마라.

```bash
# 스킬별 Gotchas 수 · Process 단계 수 · references 참조 실재 여부
for s in api-init api-probe api-contract api-verify api-ui; do
  f="api-kit/skills/$s/SKILL.md"
  printf '%-14s gotchas=%s steps=%s\n' "$s" \
    "$(grep -c '^- \*\*' "$f")" "$(grep -cE '^## [0-9]+\.' "$f")"
done
```

## Step 2: 문서 대조 (격차 분석)

`docs/api/` 12 문서의 원칙·안티패턴·Gotchas 중 **스킬에 반영되지 않은 것**을 찾는다.
반대로 스킬에만 있고 문서에 근거가 없는 규칙도 찾는다 — 그건 근거 없는 규칙이다.

| 축 | 확인 |
|---|---|
| 누락 | 문서 원칙 중 스킬 Gotchas·Process 어디에도 없는 것 |
| 무근거 | 스킬 규칙 중 `docs/api/` 에 대응 원칙이 없는 것 |
| 드리프트 | 같은 규칙이 스킬마다 다른 표현·다른 임계값으로 적힌 것 |

## Step 3: 실측 신호 수집

- `~/.harness/feedback/` 의 api-kit 관련 REJECT
- `docs/api/research-log.md` 의 미검증 항목 — 특히 Hurl 실측 대조
- 사용자가 실제로 쓰다가 막힌 지점

## Step 4: 개선 적용

Gotchas 는 **반복 실수만** 담는다. 일반 지식을 넣지 마라. 각 항목은
"왜 일어나는지 + 어떻게 피하는지" 2 요소를 갖는다.

## Step 5: 사후 측정 + 음성 대조

Step 1 과 같은 명령을 다시 돌리고 차이를 표로 낸다.
새로 넣은 규칙에 검사 지표가 있다면, **그 지표를 일부러 깨뜨렸을 때 실패하는지** 확인한다.

## Step 6: QA

`harness:qa-evaluator` 를 spawn 해 판정받는다. 매번 새로 spawn 한다 — 기존 컨텍스트의 편향을 막는다.

# References

- `../../../docs/api/` — 리서치 SSOT 12 종
- `../../../docs/superpowers/specs/2026-09-02-api-kit-design.md` — 확정 결정
- `../../../harness/docs/guides/skill-design-guide.md` — 9 가지 아키타입 · Gotchas 패턴
