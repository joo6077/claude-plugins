---
name: design-kaizen
description: >
  design-kit 스킬 품질을 docs/design/ 리서치 문서 기준으로 주기적으로 개선한다.
  이 레포 개발용 스킬이며, design-kit 플러그인에 포함되지 않는다.
  harness-kaizen, flutter-kaizen과 동일한 패턴.
  "/design-kaizen", "디자인 카이젠", "design-kit 개선" 같은 요청 시 트리거.
argument-hint: "[skill-name]"
user-invocable: true
---

# Gotchas

1. **리서치 문서 먼저 확인** — 스킬을 수정하기 전에 docs/design/ 문서가 최신인지 확인하라. 오래된 리서치를 기반으로 스킬을 개선하면 잘못된 원칙이 반영된다.
2. **Gotchas 추가 시 실패 근거 필수** — "이런 실수를 할 수 있다"가 아니라 "실제로 이런 실패가 발생했다"는 근거가 있어야 한다. 추측성 Gotchas는 추가하지 않는다.
3. **기존 스킬 구조 유지** — SKILL.md의 섹션 구조(Gotchas → Process → References)를 변경하지 마라. 내용만 개선한다.

# Process

## Step 1: 현재 상태 파악

design-kit 스킬 3개 + 에이전트 1개의 현재 Gotchas, Process, references 내용을 읽는다.

## Step 2: 리서치 문서 대비 격차 분석

docs/design/ 문서의 원칙 중 스킬에 반영되지 않은 항목을 식별한다:
- audit-criteria.md에 누락된 체크리스트 항목
- Gotchas에 추가할 반복 실패 패턴
- references에 추가할 새 원칙 문서

## Step 3: 개선 적용

격차 항목별로:
1. Gotchas 추가 — 실패 근거가 있는 항목만
2. references 갱신 — 새 원칙 추가
3. Process 보완 — 누락된 단계 추가

## Step 4: evals 갱신

개선 사항에 맞춰 evals/evals.json에 assertion 추가 또는 수정.

## Step 5: 커밋

```bash
git add design-kit/ .claude/skills/design-kaizen/
git commit -m "kaizen(design-kit): [개선 요약]"
```

# References

- 기존 카이젠 패턴: `.claude/skills/kaizen-orchestrator/SKILL.md`
- harness-kaizen: `harness/skills/harness-kaizen/SKILL.md`
- flutter-kaizen: `flutter-toolkit/skills/flutter-kaizen/SKILL.md`
