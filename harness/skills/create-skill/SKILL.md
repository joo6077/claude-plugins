---
name: create-skill
description: >
  설계 가이드 기반으로 새 스킬을 생성한다.
  docs/guides/skill-design-guide.md의 9가지 아키타입, Gotchas 패턴, 폴더 구조,
  description 작성법을 따라 SKILL.md + 폴더를 스캐폴딩한다.
  "스킬 만들어줘", "새 스킬", "create skill", "skill 생성",
  "스킬 추가" 같은 요청 시 트리거.
  기존 스킬 수정이나 Gotchas 추가에는 트리거하지 않는다.
argument-hint: "<skill-name>"
user-invocable: true
---

# Create Skill

`docs/guides/skill-design-guide.md`를 기반으로 설계 원칙에 맞는 스킬을 생성한다.

## Gotchas

- description을 사람용 요약으로 쓰면 트리거 정확도가 떨어진다 — "언제 이 스킬을 켜라" + 트리거 키워드 + 비트리거 조건까지 명시해라
- Gotchas 없이 스킬을 만들면 안 된다 — 최소 1개, "처음엔 모르더라도 빈 Gotchas 섹션은 만들어 둬라"
- 메인 SKILL.md에 모든 내용을 넣으면 컨텍스트 과부하 — 100줄 넘으면 references/ 분리 검토
- 뻔한 내용(일반 코딩 지식)을 넣으면 가치 없다 — Claude가 추론만으로 절대 알 수 없는 정보만 넣어라

## Process

### 1. 설계 가이드 읽기

`docs/guides/skill-design-guide.md`를 읽어 최신 설계 원칙을 확인한다.
특히 아래 섹션을 참조:
- 섹션 2: 9가지 스킬 유형 체크리스트
- 섹션 3: Gotchas 작성법
- 섹션 3.5: 검증 가능한 성공 기준
- 섹션 4: description은 트리거 조건
- 섹션 5: 점진적 공개 (폴더 구조)
- 섹션 8: 크로스 플랫폼 호환 (SKILL.md 형식이 Codex CLI 등에서도 동작)

### 2. 요구사항 분석

사용자의 요청에서:
- **스킬 이름** (snake_case, 하이픈)
- **목적** — 무엇을 하는 스킬인가
- **아키타입** — 9가지 중 어디에 속하는가 (복수 가능하면 주된 것 1개)
- **대상 위치** — 어떤 플러그인/프로젝트에 생성하는가
- **트리거 키워드** — 사용자가 어떤 말을 할 때 활성화되는가
- **비트리거 조건** — 어떤 경우에는 활성화하면 안 되는가

사용자에게 확인이 필요한 항목이 있으면 질문한다.

### 3. 폴더 구조 생성

```
{대상}/skills/{스킬명}/
├── SKILL.md              # 메인 (frontmatter + Gotchas + Process)
└── references/           # 필요 시에만 (100줄 초과 예상 시)
```

### 4. SKILL.md 작성

**frontmatter:**
```yaml
---
name: {스킬명}
description: >
  {목적 1줄}.
  {트리거 키워드 나열}.
  {비트리거 조건}.
argument-hint: "{인자 힌트}"
user-invocable: true
---
```

**본문 구조:**
1. **Gotchas** — 최소 1개. 알려진 주의사항이 없으면 빈 섹션으로 남기되 주석 추가:
   ```markdown
   ## Gotchas

   <!-- 사용하면서 발견되는 실수 패턴을 여기에 추가 -->
   - (아직 없음 — 사용 후 점진적으로 추가)
   ```

2. **Process** — 핵심 단계만 (v0.1 수준)
   - 스킬이 참조할 외부 파일이 있으면 명시
   - 검증 가능한 성공 기준 포함 (섹션 3.5)

### 5. 검증

- [ ] frontmatter 4개 필드 존재 (name, description, argument-hint, user-invocable)
- [ ] description에 트리거 키워드 + 비트리거 조건 포함
- [ ] Gotchas 섹션 존재
- [ ] Process에 검증 기준 포함
- [ ] 9가지 아키타입 중 해당 유형 확인

### 6. 사용자에게 결과 제시

생성된 파일 구조와 SKILL.md 내용을 보여주고 확인받는다.
수정 요청 시 반영 후 재제시.
