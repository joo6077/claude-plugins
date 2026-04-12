---
name: create-skill
description: >
  설계 가이드 기반으로 새 스킬을 생성한다.
  ../../docs/guides/skill-design-guide.md의 9가지 아키타입, Gotchas 패턴, 폴더 구조,
  description 작성법을 따라 SKILL.md + 폴더를 스캐폴딩한다.
  "스킬 만들어줘", "새 스킬", "create skill", "skill 생성",
  "스킬 추가" 같은 요청 시 트리거.
  기존 스킬 수정이나 Gotchas 추가에는 트리거하지 않는다.
argument-hint: "<skill-name>"
user-invocable: true
---

# Create Skill

`../../docs/guides/skill-design-guide.md`를 기반으로 설계 원칙에 맞는 스킬을 생성한다.

## Gotchas

- description 을 사람용 요약으로 쓰면 트리거 정확도가 떨어진다 — "언제 이 스킬을 켜라" + 트리거 키워드 + **negative trigger (비트리거 조건)** 까지 명시해라. negative trigger 는 "X 같은 요청에는 트리거하지 않는다" 형식으로 최소 1 개 이상 포함한다 (리서치 근거: skills-best-practices, mgechev — "React skill should specify: Don't use for Vue, Svelte, or vanilla CSS").
- description 은 **3 인칭 일관성** 을 유지해라 — "이 스킬은 ~한다" 또는 명령형 ("~해라") 중 하나로 통일. 1 인칭 ("나는 ~할 수 있다") 이나 2 인칭 ("당신의 ~") 은 Anthropic 공식 best practice 위반이다. description 은 system prompt 에 injection 되므로 관점 불일치가 discovery 문제를 유발한다.
- description 은 "무엇을 하는 스킬인가" + "언제 사용하는가" 양쪽을 모두 포함해야 한다 — Anthropic 공식 예시: "Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction."
- Gotchas 없이 스킬을 만들면 안 된다 — 최소 1 개, "처음엔 모르더라도 빈 Gotchas 섹션은 만들어 둬라"
- 메인 SKILL.md 에 모든 내용을 넣으면 컨텍스트 과부하 — 100 줄 넘으면 references/ 분리 검토. 전체 SKILL.md 본문 1500-2000 words 타깃 (Anthropic best practices 기준).
- 뻔한 내용(일반 코딩 지식)을 넣으면 가치 없다 — Claude 가 추론만으로 절대 알 수 없는 정보만 넣어라
- 스킬 생성 직후 반드시 `python3 scripts/validate-plugin.py <plugin-name>` 으로 V1 frontmatter / V4 trigger 중복 / V5 placeholder / V6 bare code fence 검증을 돌려라. 생성만 하고 검증 안 하면 frontmatter drift 로 스킬이 Claude 에게 invisible 처리된다.
- **아키타입 미선정 상태로 구조 작성 금지** — skill-design-guide의 9가지 아키타입(Generator, Guide, Runner 등) 중 하나를 먼저 확정하고 그에 맞는 Process 구조를 따라라. 아키타입 없이 자유 형식으로 쓰면 Process 단계 순서가 비논리적이 되고 QA Evaluator가 재현 불가 판정한다.
- **argument-hint 누락은 discovery 실패** — user-invocable 스킬이면서 인자를 받는 경우 `argument-hint`를 반드시 작성해라. 빈 문자열이면 Claude가 인자 전달 가능성 자체를 인지하지 못해 사용자가 매번 수동으로 입력해야 한다.
- **스킬 이름에 프레임워크/언어 접두사 필수** — 범용(harness, design-kit)이 아닌 스택 종속 스킬은 반드시 `flutter-`, `rust-`, `react-` 같은 접두사를 붙여라. 접두사 없으면 다른 킷의 동명 스킬과 충돌하거나 트리거 우선순위가 모호해진다.
- **references/ 분리 판단 기준** — Process 본문에서 3회 이상 참조되는 정보(감지 로직, 템플릿 코드, 체크리스트)는 references/로 분리해라. 인라인으로 남기면 SKILL.md가 2000 words를 초과하여 Claude 컨텍스트 효율이 떨어진다.

## Process

### 1. 설계 가이드 읽기

`../../docs/guides/skill-design-guide.md`를 읽어 최신 설계 원칙을 확인한다.
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

```text
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

- [ ] frontmatter 4 개 필드 존재 (name, description, argument-hint, user-invocable)
- [ ] description 에 트리거 키워드 + negative trigger (비트리거 조건) 포함
- [ ] description 관점 일관성 (3 인칭 또는 명령형 통일, 혼용 금지)
- [ ] Gotchas 섹션 존재 (최소 1 개)
- [ ] Process 에 검증 기준 포함
- [ ] 9 가지 아키타입 중 해당 유형 확인
- [ ] **validate-plugin 연동**: `python3 scripts/validate-plugin.py <plugin-name>` 실행하여 아래 7 카테고리 중 V1/V4/V5/V6 최소 4 개가 OK 인지 확인. 기준은 `harness/docs/guides/plugin-validation-guide.md §3` 참조.
  - V1 frontmatter — 필수 필드 (name/description/user-invocable) 모두 존재
  - V4 triggers — description 키워드가 기존 스킬과 중복되지 않음 (또는 kit-context 로 disambiguated)
  - V5 placeholders — 미완성 마커 (할일/보류/수정요망 세 종류) 0 건
  - V6 code-fence — bare fence 0 건 (언어 힌트 필수)

### 6. 사용자에게 결과 제시

생성된 파일 구조와 SKILL.md 내용을 보여주고 확인받는다.
수정 요청 시 반영 후 재제시.
