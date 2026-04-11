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

## Step 6: Plugin Validation 결과 반영

이 카이젠 세션을 시작하기 전과 끝낼 때 모두 `scripts/validate-plugin.py` 를 실행하여 backend-kit 의 7가지 품질 카테고리 상태를 확인한다.

### 실행

```bash
# 세션 시작 시 현재 상태 파악
python3 scripts/validate-plugin.py backend-kit

# 자동 수정 가능한 항목 먼저 (V5 placeholders, V6 code-fence)
python3 scripts/validate-plugin.py backend-kit --fix --check=placeholders,code-fence

# 세션 종료 시 회귀 없음 확인
python3 scripts/validate-plugin.py backend-kit
```

### 우선순위 반영 규칙

- **ERROR** (V1~V7 중 실패): 카이젠 Step 3 (개선 적용) 의 "높음" 레벨에 자동 편입. 이 카이젠 세션에서 반드시 수정.
- **WARNING**: "중간" 레벨. V4 trigger 키워드 중복은 description 보강으로 처리.
- **PASS**: 해당 카테고리 skip.

### 통합 규칙

- `--fix` 자동 모드는 V5 placeholders 와 V6 code-fence 만 수정한다. 다른 체크는 수동 수정.
- V3 refs BROKEN 은 수동으로 링크 경로 확인 후 수정.
- V1 frontmatter 누락은 1줄 수정이라 즉시 처리.
- V7 plugin-json 불일치는 release.sh 흐름 문제라면 카이젠이 아닌 릴리스 스킬에서 다룬다.

# References

- backend-kit/skills/backend-guide/SKILL.md
- backend-kit/skills/backend-audit/SKILL.md
- backend-kit/skills/backend-system/SKILL.md
- backend-kit/agents/backend-reviewer.md
- docs/backend/ — 리서치 SSOT
- `harness/docs/guides/plugin-validation-guide.md` — 플러그인 품질 7 카테고리 기준 (SSOT)
- `scripts/validate-plugin.py` — 플러그인 검증 자동화 도구
