---
name: backend-kaizen
description: >
  backend-kit 스킬 품질을 docs/backend/ 리서치 문서 기준으로 주기적으로 개선한다.
  이 레포 개발용 스킬이며, backend-kit 플러그인에 포함되지 않는다.
  harness-kaizen, flutter-kaizen, design-kaizen과 동일한 패턴.
  "/backend-kaizen", "백엔드 카이젠", "backend-kit 개선" 같은 요청 시 트리거.
  단순 버그 수정이나 기능 구현 요청에는 트리거하지 않는다.
argument-hint: ""
user-invocable: true
---

# Gotchas

1. **추측성 Gotchas 추가 금지** — 실제 실패 근거 없이 "이럴 수 있다"는 Gotchas를 추가하지 마라.
2. **리서치 문서 기반만** — docs/backend/ 문서에 없는 원칙을 스킬에 추가하지 마라. 먼저 backend-research로 문서를 갱신하라.
3. **스킬 범위 변경 금지** — 스킬의 description(트리거 조건)을 변경하려면 사용자 승인 필수.

# Process

## Step 1: 현재 상태 읽기

backend-kit 스킬 3개 + backend-reviewer 에이전트의 Gotchas/Process/references 전체 읽기:
- backend-kit/skills/backend-guide/SKILL.md
- backend-kit/skills/backend-audit/SKILL.md
- backend-kit/skills/backend-system/SKILL.md
- backend-kit/agents/backend-reviewer.md

## Step 2: 격차 분석

docs/backend/ 문서의 원칙 중 스킬에 반영되지 않은 항목 식별:
- audit-criteria.md에 누락된 체크리스트 항목
- Gotchas에 추가할 반복 실패 패턴
- references에 추가할 새 원칙 문서

글로벌 피드백도 확인:
- ~/.harness/feedback/ 에서 backend-kit 관련 피드백 검색

## Step 3: 개선 적용

- SKILL.md Gotchas 추가/수정
- audit-criteria.md 체크리스트 갱신
- principle-index.md 매핑 갱신
- system-principles.md 카테고리 갱신

## Step 4: 검증

- 변경된 스킬의 description이 원래 트리거 조건과 일치하는지 확인
- 리서치 문서와 스킬 references 경로 정합성 확인

## Step 5: 커밋

```
kaizen(backend-kit): [개선 내용 요약]
```

# References

- backend-kit/skills/backend-guide/SKILL.md
- backend-kit/skills/backend-audit/SKILL.md
- backend-kit/skills/backend-system/SKILL.md
- backend-kit/agents/backend-reviewer.md
- docs/backend/ — 리서치 SSOT
