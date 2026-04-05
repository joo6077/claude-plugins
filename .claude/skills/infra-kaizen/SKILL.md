---
name: infra-kaizen
description: >
  infra-kit 스킬 품질을 docs/infra/ 리서치 문서 기준으로 주기적으로 개선한다.
  이 레포 개발용 스킬이며, infra-kit 플러그인에 포함되지 않는다.
  "/infra-kaizen", "인프라 카이젠", "infra-kit 개선" 같은 요청 시 트리거.
  단순 버그 수정이나 기능 구현 요청에는 트리거하지 않는다.
argument-hint: ""
user-invocable: true
---

# Gotchas

1. **추측성 Gotchas 추가 금지** — 실제 실패 근거 없이 추가하지 마라.
2. **리서치 문서 기반만** — docs/infra/ 문서에 없는 원칙을 스킬에 추가하지 마라.
3. **스킬 범위 변경 금지** — description 변경은 사용자 승인 필수.

# Process

## Step 1: 현재 상태 읽기

infra-kit 스킬 3개 + infra-reviewer 에이전트:
- infra-kit/skills/infra-guide/SKILL.md
- infra-kit/skills/infra-audit/SKILL.md
- infra-kit/skills/infra-init/SKILL.md
- infra-kit/agents/infra-reviewer.md

## Step 2: 격차 분석

docs/infra/ 원칙 vs 스킬 반영 상태:
- audit-criteria.md 누락 항목
- Gotchas 추가 필요 패턴
- 글로벌 피드백 (~/.harness/feedback/)

## Step 3: 개선 적용

- SKILL.md Gotchas 추가/수정
- audit-criteria.md 체크리스트 갱신
- principle-index.md 매핑 갱신
- init-checklist.md 카테고리 갱신

## Step 4: 검증

- description 트리거 조건 유지 확인
- 리서치 문서 ↔ 스킬 references 경로 정합성

## Step 5: 커밋

```
kaizen(infra-kit): [개선 내용 요약]
```

# References

- infra-kit/skills/infra-guide/SKILL.md
- infra-kit/skills/infra-audit/SKILL.md
- infra-kit/skills/infra-init/SKILL.md
- infra-kit/agents/infra-reviewer.md
- docs/infra/ — 리서치 SSOT
