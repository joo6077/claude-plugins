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
- 스킬 생성 직후 반드시 `python3 scripts/validate-plugin.py <plugin-name>` 으로 V1 frontmatter / V4 trigger 중복 / V5 placeholder / V6 bare code fence 검증을 돌려라. 생성만 하고 검증 안 하면 frontmatter drift 를 다음 사이클까지 못 잡는다.
- **공식 스펙 필수 필드와 이 레포 정책을 섞지 마라.** SKILL.md frontmatter 의 **공식 필수는 `name` 과 `description` 2 종**이다 (`../../docs/guides/skill-design-guide.md` §frontmatter 규칙). `argument-hint` · `user-invocable` 은 Claude Code 전용 선택 필드로 다른 플랫폼에서는 무시된다. 다만 **이 레포는 `user-invocable` 을 추가로 요구**한다 — `scripts/validate-plugin.py` 의 V1 이 skills 에 대해 `name`/`description`/`user-invocable` 3 종을 강제하므로, 누락하면 공식 스펙이 아니라 **레포 게이트에서** FAIL 난다.
- **아키타입 미선정 상태로 구조 작성 금지** — skill-design-guide의 9가지 아키타입(Generator, Guide, Runner 등) 중 하나를 먼저 확정하고 그에 맞는 Process 구조를 따라라. 아키타입 없이 자유 형식으로 쓰면 Process 단계 순서가 비논리적이 되고 QA Evaluator가 재현 불가 판정한다.
- **argument-hint 누락은 discovery 실패** — user-invocable 스킬이면서 인자를 받는 경우 `argument-hint`를 반드시 작성해라. 빈 문자열이면 Claude가 인자 전달 가능성 자체를 인지하지 못해 사용자가 매번 수동으로 입력해야 한다.
- **스킬 이름에 프레임워크/언어 접두사 필수** — 범용(harness, design-kit)이 아닌 스택 종속 스킬은 반드시 `flutter-`, `rust-`, `react-` 같은 접두사를 붙여라. 접두사 없으면 다른 킷의 동명 스킬과 충돌하거나 트리거 우선순위가 모호해진다.
- **references/ 분리 판단 기준** — Process 본문에서 3회 이상 참조되는 정보(감지 로직, 템플릿 코드, 체크리스트)는 references/로 분리해라. 인라인으로 남기면 SKILL.md가 2000 words를 초과하여 Claude 컨텍스트 효율이 떨어진다.
- **Binary Decidability 검증 가능 성공 기준** — Process의 각 Step은 QA 계약과 1:1로 매칭 가능한 "측정 가능한 완료 기준"을 포함해야 한다 (skill-design-guide §3.5). "적절히 처리한다", "필요 시 추가한다" 같은 모호 표현은 금지. Grep 가능한 키워드, 파일 경로, 라인 수, boolean 조건으로만 기술해라. 모호 조건은 평가자 단계에서 자동 REJECT 대상이 된다 (PH-01 / design-kit 2026-04 REJECT 사례).
- **Cross-Surface Parity 체크 필수** — 새 Gotcha를 추가하거나 원칙을 도입할 때 skill-design-guide §11의 5개 parity item (Binary Decidability / 트리거 배타성 / 검증 기준 / Rule-by-Rule Audit / Unverifiable 정책) 중 하나에 해당하는지 판정해라. 해당하면 agent-design-guide · contract-design-guide · qa-evaluation-guide에 동일 용어로 존재하는지 Grep 하여 전파 필요성을 사용자에게 보고해라 (없으면 PH-01 / SK-13 같은 cascade REJECT 가 발생한다).
- **Sibling-Skill 원칙 일관성** — 동일 plugin 내 형제 스킬이 이미 존재하면 생성 전에 `grep -n "^- " <sibling>/SKILL.md` 로 기존 Gotchas 목록을 enumerated 수집하고, 공통 원칙(예: rust-init/rust-feature/rust-api의 domain event + outbox 원칙, Composition Root 단일화) 누락이 없는지 set intersection 으로 대조해라. 하나라도 누락되면 H-01/H-03 패턴 REJECT 가 재발한다 (skill-design-guide §8.8).
- **Code Examples 품질 규칙** — SKILL.md에 포함하는 fenced code block은 (1) 언어 힌트 필수 (```bash, ```yaml, ```text 등 — bare fence 는 V6 FAIL), (2) 미완성 마커(대문자 3글자 작업 마커, `<할일>`, `<보류>`, `<수정요망>`) 금지 (V5 FAIL), (3) 변수 치환은 `{변수명}` 중괄호 표기 일관 사용. DG-01/DG-02 (react-kit REJECT) 재발 방지 (skill-design-guide §8.7).
- **Enumerate-before-Act (low-freedom 영역)** — 스캐폴딩/생성/대량 수정처럼 자유도가 낮은 스킬은 Process Step 초반에 "편집 전 enumerated 목록 작성 + 사용자 승인" 단계를 두어라 (skill-design-guide §5.5). 이 단계가 없으면 /insights 마찰점 1번(Proactive quality gaps — Claude가 규칙 위반을 놓침)이 재발한다. 예: "먼저 target 파일 전부 Read → 위반 체크리스트 → 승인 → 일괄 편집".
- **Trigger 키워드 substring 검사** — description 트리거 키워드는 기존 스킬과 (1) 정확 중복 금지, (2) substring containment 금지 (예: "API 연동" ⊂ "API 연동 화면" 위반). `python3 scripts/validate-plugin.py <plugin> --check=triggers` 로 검증되며 RE-02 (react-kit 2026-04) REJECT 재발 방지 (skill-design-guide §4).
- **Rule-by-Rule Audit Before Completion** — 스킬 Process의 마지막 Step은 반드시 "완료 선언 전 규칙 전수 대조 패스" 를 포함해야 한다 (skill-design-guide §3.6). create-skill이 만드는 스킬도 이 패턴을 상속하도록 Gotchas 섹션에 "완료 전 rule-by-rule audit" 항목을 기본 포함시켜라.

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

- [ ] frontmatter 필드 존재 — **공식 필수는 `name` · `description` 2 종**, 이 레포 정책(`scripts/validate-plugin.py` V1)은 `user-invocable` 을 더해 **3 종**을 요구한다. `argument-hint` 는 인자를 받는 user-invocable 스킬에 권장(레포 관례)이다 — 셋을 구분해서 보고해라
- [ ] description 에 트리거 키워드 + negative trigger (비트리거 조건) 포함
- [ ] description 관점 일관성 (3 인칭 또는 명령형 통일, 혼용 금지)
- [ ] Gotchas 섹션 존재 (최소 1 개)
- [ ] Process 에 검증 기준 포함
- [ ] 9 가지 아키타입 중 해당 유형 확인
- [ ] **Cross-Surface Parity 5 개 item 확인** (skill-design-guide §11): Binary Decidability / 트리거 배타성 (substring 포함) / 검증 가능한 성공 기준 / Rule-by-rule audit / Unverifiable 정책 (에이전트 전용, 해당 시) — 새 Gotcha 가 이 중 하나에 해당하면 형제 surface 로의 전파 필요성을 사용자에게 보고
- [ ] **Sibling Enumerated 비교**: 형제 스킬이 있으면 `grep -n "^- " <sibling>/SKILL.md` 로 기존 Gotchas 목록 나열 후 공통 원칙 누락 여부 대조
- [ ] **Code Examples 품질** (§8.7): 모든 fenced block 에 언어 힌트 존재 + 미완성 마커(V5 placeholder 3종) 0 건
- [ ] **validate-plugin 연동**: `python3 scripts/validate-plugin.py <plugin-name>` 실행하여 8 카테고리 (V1~V8) 중 V1/V4/V5/V6 최소 4 개가 OK 인지 확인. 기준은 `harness/docs/guides/plugin-validation-guide.md §3` 참조 (카테고리 수의 SSOT 는 이 가이드다).
  - V1 frontmatter — **레포 정책** 필드 (name/description/user-invocable) 모두 존재 (공식 스펙의 필수는 앞의 2 종뿐이다 — V1 은 그보다 엄격한 레포 규약이다)
  - V4 triggers — description 키워드가 기존 스킬과 중복되지 않음 (substring containment 도 금지)
  - V5 placeholders — 미완성 마커 (할일/보류/수정요망 세 종류) 0 건
  - V6 code-fence — bare fence 0 건 (언어 힌트 필수)

### 6. 사용자에게 결과 제시

생성된 파일 구조와 SKILL.md 내용을 보여주고 확인받는다.
수정 요청 시 반영 후 재제시.
