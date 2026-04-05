# Kaizen Skill Templates

각 kit는 리서치 SSOT를 갱신하는 research 스킬과, 스킬 품질을 점진 개선하는 kaizen 스킬을 쌍으로 갖는다.

## 위치

카이젠 스킬은 **플러그인이 아닌 `.claude/skills/`**에 생성한다. 이유:
- 이 레포 개발용 스킬이라 외부 사용자에게 노출되면 안 됨
- 플러그인 카이젠은 레포 상태(git history, 다른 스킬)에 의존

```
.claude/skills/
├── {kit-name}-research/SKILL.md
└── {kit-name}-kaizen/SKILL.md
```

## 템플릿 1: research 스킬

**역할:** 외부 소스(공식 문서, RFC, 커뮤니티)를 크롤링하여 docs/{kit-name}/ 문서를 갱신.

```yaml
---
name: {kit-name}-research
description: >
  {도메인} 레퍼런스 소스를 크롤링/분석하여 docs/{kit-name}/ 문서를 갱신한다.
  이 레포 개발용 스킬이며, {kit-name} 플러그인에 포함되지 않는다.
  "{도메인} 리서치", "{kit-name} research", "{도메인} 문서 갱신" 같은 요청 시 트리거.
argument-hint: "[category]"
user-invocable: true
---

# Gotchas

1. **할루시네이션 출처 금지** — 모든 원칙에 검증된 URL 출처 필수. URL 존재 확인 후 인용.
2. **기존 문서 덮어쓰기 금지** — 기존 docs/{kit-name}/ 문서를 읽고, 새 정보만 추가/갱신. 기존 검증된 내용 삭제 금지.
3. **블로그 단독 인용 금지** — 일반 블로그는 공식 문서/RFC와 교차 검증 후에만 인용.
4. **6개월 이상 된 정보 태그** — `[dated: YYYY-MM]` 태그 필수.

# Process

## Step 1: 리서치 범위 결정

사용자가 카테고리를 지정하면 해당 문서만, 미지정이면 전체 docs/{kit-name}/ 갱신.

현재 문서 목록:
- {category-1}/: {doc1}, {doc2}, ...
- {category-2}/: {doc3}, ...

## Step 2: 현재 문서 읽기

대상 문서의 현재 원칙·출처·수치를 파악한다.

## Step 3: 외부 리서치

Codex(codex:rescue)에 리서치 태스크를 위임한다:
- 공식 문서 업데이트 확인
- 새 RFC/표준 발행 여부
- 주요 엔지니어링 블로그 신규 사례

## Step 4: 문서 갱신

- 새 원칙 추가 (출처 필수)
- 수치 업데이트 (변경 시 이전 값 주석)
- deprecated 정보 표시
- version bump (patch)
- last_updated 갱신

## Step 5: 변경 커밋

```
research({kit-name}): [카테고리] 문서 갱신
```
```

## 템플릿 2: kaizen 스킬

**역할:** 리서치 문서(SSOT) 기준으로 kit의 스킬/에이전트 격차를 분석하고 개선.

```yaml
---
name: {kit-name}-kaizen
description: >
  {kit-name} 스킬 품질을 docs/{kit-name}/ 리서치 문서 기준으로 주기적으로 개선한다.
  이 레포 개발용 스킬이며, {kit-name} 플러그인에 포함되지 않는다.
  harness-kaizen, flutter-kaizen, design-kaizen과 동일한 패턴.
  "/{kit-name}-kaizen", "{도메인} 카이젠", "{kit-name} 개선" 같은 요청 시 트리거.
  단순 버그 수정이나 기능 구현 요청에는 트리거하지 않는다.
argument-hint: ""
user-invocable: true
---

# Gotchas

1. **추측성 Gotchas 추가 금지** — 실제 실패 근거 없이 "이럴 수 있다"는 Gotchas를 추가하지 마라.
2. **리서치 문서 기반만** — docs/{kit-name}/ 문서에 없는 원칙을 스킬에 추가하지 마라. 먼저 {kit-name}-research로 문서를 갱신하라.
3. **스킬 범위 변경 금지** — 스킬의 description(트리거 조건)을 변경하려면 사용자 승인 필수.

# Process

## Step 1: 현재 상태 읽기

{kit-name} 스킬 3개 + reviewer 에이전트의 Gotchas/Process/references 전체 읽기:
- {kit-name}/skills/{kit-name}-guide/SKILL.md
- {kit-name}/skills/{kit-name}-audit/SKILL.md
- {kit-name}/skills/{kit-name}-{system|init}/SKILL.md
- {kit-name}/agents/{kit-name}-reviewer.md

## Step 2: 격차 분석

docs/{kit-name}/ 문서의 원칙 중 스킬에 반영되지 않은 항목 식별:
- audit-criteria.md에 누락된 체크리스트 항목
- Gotchas에 추가할 반복 실패 패턴 (추측성 추가 금지 — 실제 실패 근거 필수)
- references에 추가할 새 원칙 문서

글로벌 피드백도 확인:
- ~/.harness/feedback/ 에서 {kit-name} 관련 피드백 검색

## Step 3: 개선 적용

- SKILL.md Gotchas 추가/수정
- audit-criteria.md 체크리스트 갱신
- principle-index.md 매핑 갱신

## Step 4: 검증

- 변경된 스킬의 description이 원래 트리거 조건과 일치하는지 확인
- 리서치 문서와 스킬 references 경로 정합성 확인

## Step 5: 커밋

```
kaizen({kit-name}): [개선 내용 요약]
```

# References

- {kit-name}/skills/{kit-name}-guide/SKILL.md
- {kit-name}/skills/{kit-name}-audit/SKILL.md
- {kit-name}/skills/{kit-name}-{system|init}/SKILL.md
- {kit-name}/agents/{kit-name}-reviewer.md
- docs/{kit-name}/ — 리서치 SSOT
```

## 카이젠 오케스트레이터 통합

`.claude/skills/kaizen-orchestrator/SKILL.md`의 Phase 목록에 새 kit의 카이젠을 추가할지 사용자에게 확인한다.

현재 Phase 순서:
1. 설계 가이드 (harness)
2. contract-kaizen
3. evaluator-kaizen
4. harness-kaizen
5. flutter-kaizen
6. design-kaizen
7. backend-kaizen (추가됨)
8. infra-kaizen (추가됨)
9. → 새 kit 카이젠 위치

## 기존 참고

- `.claude/skills/design-research/SKILL.md`
- `.claude/skills/design-kaizen/SKILL.md`
- `.claude/skills/backend-research/SKILL.md`
- `.claude/skills/backend-kaizen/SKILL.md`
- `.claude/skills/infra-research/SKILL.md`
- `.claude/skills/infra-kaizen/SKILL.md`
