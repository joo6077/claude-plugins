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
4. **한 번에 전체 수정 금지** — 12개 스킬 + 에이전트 일괄 수정 시 품질 저하. 1-2개씩 개선.
5. **validate-plugin.py 실행 없이 완료 선언 금지** — 세션 종료 시 `scripts/validate-plugin.py planning-kit` 실행 필수.
6. **Mermaid 문법 예제 붙여넣기만 하지 마라** — 예제 추가 시 실제 mermaid.live 또는 로컬 mermaid-cli 로 렌더 가능 여부 확인.
7. **Sibling Consistency 검증** — plan-audit 의 카테고리 수(12), planning-reviewer 의 카테고리 수, 두 문서의 Summary 분모가 모두 일치해야 한다. 어느 하나만 10/12 로 바꾸면 verdict 신뢰 붕괴. **`[미검증]` 임계값도 같은 축이다 — 임계 숫자는 `harness/docs/guides/qa-evaluation-guide.md` §Canonical Unverified-Evidence Protocol 이 SSOT 이고 planning-reviewer 가 5 조항을 문구 변형 없이 복제 보유한다. 카이젠 중 planning-kit 문서에서 임계값을 새로 쓰거나 조항 문구를 손보지 마라 — 정본을 고치고 재복제하는 것이 유일한 경로다** (2026-07-27 Phase 3 가 "planning-reviewer 미검증 0 요구" drift 를 지목한 원인).
8. **Step 0 자동 로드 독립 단계 유지** — plan-audit/plan-guide/plan-prd/plan-stories 등의 Step 0 은 "원칙 문서 + 이전 단계 산출물 자동 로드" 전용이다. 여기에 작성 로직 섞으면 Phase 7~10 누적 원칙 위반. 수정 시 Step 0 이 자료 수집만 하는지 재확인.
9. **카테고리 수 인벤토리** — 스킬 12개 (plan-ideate + plan-reference 포함). 카이젠 시 10개로 착각하면 두 스킬이 누락된다. 현재 스킬 목록:
   - 필수 워크플로우(1~10): plan-discover, plan-prd, plan-stories, plan-prioritize, plan-flow, plan-data-model, plan-risks, plan-sync-github, plan-guide, plan-audit
   - 선택 전단계(0a/0b): plan-ideate, plan-reference

# Process

## Step 1: 현재 상태 읽기

planning-kit 스킬 12개 + planning-reviewer 에이전트의 Gotchas/Process/references 전체:
- planning-kit/skills/plan-{ideate,reference,discover,prd,stories,prioritize,flow,data-model,risks,sync-github,guide,audit}/SKILL.md (12개)
- planning-kit/agents/planning-reviewer.md

## Step 2: 격차 분석

- docs/planning/ 문서의 원칙 중 스킬에 반영되지 않은 항목
- Gotchas 에 추가할 반복 실패 패턴 (글로벌 피드백 `~/.harness/feedback/` 확인)
- 카테고리 체크리스트(plan-audit 의 12 카테고리: 0a Reference, 0b Ideation, 1~10) 누락 항목
- Phase 1~10 누적 원칙 (Step 0 자동 로드 독립, Sibling Consistency, Rule-by-Rule, [미검증], 가이드형 3-Step, Enumerate-before-Act, Context7 출처 형식) 반영 여부

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

세션 시작/종료 시 `scripts/validate-plugin.py planning-kit` 실행하여 **8 카테고리 (V1 frontmatter / V2 templates / V3 refs / V4 triggers / V5 placeholders / V6 code-fence / V7 plugin-json / V8 hook-exec)** 확인. 실행 패턴·우선순위는 `harness/docs/guides/plugin-validation-guide.md §7` SSOT.

# References

- planning-kit/skills/*/SKILL.md
- planning-kit/agents/planning-reviewer.md
- docs/planning/ — 리서치 SSOT
- harness/docs/guides/plugin-validation-guide.md
- scripts/validate-plugin.py
