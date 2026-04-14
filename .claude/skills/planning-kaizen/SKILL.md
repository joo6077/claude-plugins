---
name: planning-kaizen
description: >
  planning-kit 스킬 품질을 docs/planning/ 리서치 문서 기준으로 주기적으로 개선한다.
  이 레포 개발용 스킬이며, planning-kit 플러그인에 포함되지 않는다.
  harness-kaizen, flutter-kaizen, design-kaizen, rust-kaizen, react-kaizen 과 동일한 패턴.
  "/planning-kaizen", "기획 카이젠", "planning-kit 개선" 같은 요청 시 트리거.
  단순 버그 수정이나 기능 구현 요청에는 트리거하지 않는다.
argument-hint: ""
user-invocable: true
---

# Gotchas

1. **추측성 Gotchas 추가 금지** — 실제 실패 근거 없이 "이럴 수 있다" 추가 금지.
2. **리서치 문서 기반만** — docs/planning/ 에 없는 원칙을 스킬에 추가 금지. 먼저 planning-research 로 문서 갱신.
3. **스킬 범위 변경 금지** — description(트리거 조건) 변경 시 사용자 승인 필수.
4. **한 번에 전체 수정 금지** — 10개 스킬 + 에이전트 일괄 수정 시 품질 저하. 1-2개씩 개선.
5. **validate-plugin.py 실행 없이 완료 선언 금지** — 세션 종료 시 `scripts/validate-plugin.py planning-kit` 실행 필수.
6. **Mermaid 문법 예제 붙여넣기만 하지 마라** — 예제 추가 시 실제 mermaid.live 또는 로컬 mermaid-cli 로 렌더 가능 여부 확인.

# Process

## Step 1: 현재 상태 읽기

planning-kit 스킬 10개 + planning-reviewer 에이전트의 Gotchas/Process/references 전체:
- planning-kit/skills/plan-{discover,prd,stories,prioritize,flow,data-model,risks,sync-github,guide,audit}/SKILL.md
- planning-kit/agents/planning-reviewer.md

## Step 2: 격차 분석

- docs/planning/ 문서의 원칙 중 스킬에 반영되지 않은 항목
- Gotchas 에 추가할 반복 실패 패턴 (글로벌 피드백 `~/.harness/feedback/` 확인)
- 카테고리 체크리스트(plan-audit 의 10 카테고리) 누락 항목

## Step 3: 개선 적용

- Gotchas 추가/수정
- plan-audit 카테고리 기준 보강
- planning-reviewer 평가 규칙 정교화
- references 경로 정합성 확인

## Step 4: 검증

- description 트리거 조건 원본 유지 확인
- 리서치 문서 ↔ 스킬 references 경로 확인
- `scripts/validate-plugin.py planning-kit` 실행

## Step 5: 커밋

```
kaizen(planning-kit): [개선 내용 요약]
```

## Step 6: Plugin Validation 결과 반영

세션 시작/종료 시 `scripts/validate-plugin.py planning-kit` 실행하여 7 카테고리 확인. 실행 패턴·우선순위는 `harness/docs/guides/plugin-validation-guide.md §7` SSOT.

# References

- planning-kit/skills/*/SKILL.md
- planning-kit/agents/planning-reviewer.md
- docs/planning/ — 리서치 SSOT
- harness/docs/guides/plugin-validation-guide.md
- scripts/validate-plugin.py
