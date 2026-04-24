---
title: Claude Code 스킬 설계 가이드
version: 1.2.0
last_updated: 2026-04-24
---

# Claude Code 스킬 설계 가이드

> Anthropic 공식 문서(2026-04 최신) + 내부 스킬 분석 + 커뮤니티 실전 경험 정리

**이 문서의 용도:** 새 스킬을 만들거나 기존 스킬을 개선할 때 참고한다. 이 프로젝트(`claude-plugins`)의 실제 스킬을 적용 사례로 함께 다룬다.

**주요 출처:**
- [Skill Authoring Best Practices — Claude API Docs](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) (2026-04)
- [Extend Claude with Skills — Claude Code Docs](https://code.claude.com/docs/en/skills)
- [anthropics/skills — skill-creator SKILL.md](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md)
- [Equipping Agents for the Real World — Anthropic Engineering](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)

---

## 1. 핵심 원칙: 파일이 아닌 폴더로 설계하라

스킬은 마크다운 파일 하나가 아니라 **폴더 단위**로 설계한다.

```text
my-skill/
├── my-skill.md          # 메인 지시문 (개요 + 파일 목록)
├── references/          # API 문서, 코드 스니펫
│   └── api.md
├── scripts/             # 헬퍼 함수, 검증 스크립트
│   └── validate.sh
└── templates/           # 출력 템플릿
    └── report.md
```

**왜 폴더인가?**

- Claude는 폴더를 탐색하고 필요한 파일만 선택적으로 읽을 수 있다
- 메인 파일에 모든 정보를 넣으면 컨텍스트가 과부하된다
- 점진적 공개(Progressive Disclosure): 메인 MD에는 개요와 파일 목록만, 상세는 별도 파일로 분리
- 밀키트 비유 — 레시피(지시문)뿐 아니라 재료(레퍼런스)와 도구(스크립트)까지 제공

---

## 2. 스킬 9가지 유형 체크리스트

Anthropic이 내부 스킬 수백 개를 분석하여 발견한 패턴. **좋은 스킬은 하나의 유형에 명확히 속하고, 나쁜 스킬은 여러 유형에 걸친다.**

| # | 유형 | 설명 | 예시 |
|---|------|------|------|
| 1 | **라이브러리 레퍼런스** | 내부 라이브러리 사용법 및 함정 정리 | 사내 SDK 가이드 |
| 2 | **제품 검증** | Playwright 등 도구로 코드 자동 확인 | E2E 테스트 스킬 |
| 3 | **데이터 조회** | 모니터링/분석 스택 연결 | Grafana 대시보드 조회 |
| 4 | **비즈니스 자동화** | 반복 업무 자동화 | 스탠드업 리포트, 위클리 리캡 |
| 5 | **코드 스캐폴딩** | 보일러플레이트 자동 생성 | 프로젝트 초기 설정 |
| 6 | **코드 리뷰** | 스타일 강제 또는 자동 리뷰 | PR 리뷰 스킬 |
| 7 | **CI/CD** | PR 모니터링 및 자동 롤백 | 배포 파이프라인 스킬 |
| 8 | **런북(Runbook)** | 장애 시 자동 조사 및 보고서 | 인시던트 대응 스킬 |
| 9 | **인프라 운영** | 리소스 정리 및 비용 분석 | 미사용 리소스 정리 |

> 이 목록을 체크리스트로 사용하여 팀에 아직 없는 스킬 유형을 점검하라.

---

## 3. 가차스(Gotchas) — 스킬에서 가장 가치 있는 섹션

### 원칙: Claude가 이미 아는 뻔한 내용은 넣지 마라

Claude는 코딩을 이미 잘 안다. 파이썬 API 호출법 같은 일반 지식은 스킬에 불필요하다.
스킬에 담아야 할 것은 **Claude가 추론만으로 절대 알 수 없는 정보**다.

### 가차스란?

Claude가 **반복적으로 실패하는 지점**을 모아 놓은 목록이다.

```markdown
## Gotchas

- 우리 빌딩 립은 이 함수 호출 전에 반드시 tenant_id를 먼저 설정해야 한다
```

### 왜 가차스가 중요한가?

- 완벽한 지시문에도 Claude는 예상치 못한 실수를 한다
- 신입 사원에게 매뉴얼보다 선배의 "이거 조심해" 조언이 더 유용한 것과 같다
- 대부분의 스킬은 **몇 줄의 지시문 + 하나의 가차스**로 시작하여 점진적으로 성장한다

### 가차스 추가 흐름

```text
Claude가 실수 → 실수 패턴 식별 → Gotchas에 한 줄 추가 → 다음부터 같은 실수 방지
```

---

## 3.5. QA 계약과 1:1 매칭되는 이름을 사용하라

스킬이 정의하는 **카테고리, 필드, 섹션 이름**은 QA 계약(Sprint Contract)에서 그대로 재사용된다. 이름이 어긋나면 평가자가 "이 조건이 어느 항목에 해당하는지" 해석해야 하고, 해석이 엇갈리면 REJECT 또는 모호한 PASS가 발생한다.

**원칙:** 스킬 본문에 등장하는 카테고리 ID, 섹션명, 필드명은 해당 스킬로 생성된 Sprint Contract의 조건 항목명과 정확히 일치해야 한다.

**Bad — 스킬과 계약의 이름이 다름:**

```text
스킬 본문: "Anatomy 섹션 — 필수 파트: Header, Body, Footer"
계약 조건: "SK-05: 레이아웃 구조 확인 (헤더/바디/푸터 포함 여부)"
```

평가자가 SK-05를 검증할 때 "레이아웃 구조"가 Anatomy를 가리키는지 불명확하다.

**Good — 스킬과 계약의 이름이 일치:**

```text
스킬 본문: "Anatomy 섹션 — 필수 파트: Header, Body, Footer"
계약 조건: "SK-05: Anatomy 섹션 확인 — Header, Body, Footer 필수 파트 포함 여부"
```

**적용 체크리스트:**
- 스킬에 카테고리 ID(SK-xx, CD-xx 등)를 정의했으면, 계약 조건에도 동일 ID를 사용
- 스킬 본문의 필드명을 계약 작성 시 그대로 복사하여 재해석 여지를 없앰
- 스킬을 수정할 때 이름이 바뀌면 기존 계약 템플릿도 함께 갱신

---

## 3.6. 검증 가능한 성공 기준을 제공하라

> **출처:** [Best Practices for Claude Code](https://code.claude.com/docs/en/best-practices) — "Give Claude a way to verify its work. This is the single highest-leverage thing you can do."

스킬이 산출물을 생성할 때, Claude가 **스스로 결과를 검증할 수 있는 기준**을 포함해야 한다.

### 왜 중요한가?

검증 기준 없이 Claude는 "그럴듯해 보이지만 실제로는 동작하지 않는" 결과를 만든다. 사용자가 유일한 피드백 루프가 되면 모든 실수에 사용자의 주의가 필요하다.

### 적용 방법

| 스킬 유형 | 검증 기준 예시 |
|-----------|---------------|
| 코드 스캐폴딩 | 생성 후 `commands.analyze` 실행, 워닝 0개 확인 |
| 코드 리뷰 | 지적 사항마다 `파일:라인` 근거 필수 |
| 계약 생성 | 모든 조건이 PASS/FAIL 이진 판정 가능한지 자가 검증 |
| 데이터 조회 | 쿼리 결과가 비어 있으면 쿼리 자체를 재검증 |

### 이 프로젝트의 실제 예시

`sprint-contract` 스킬은 계약 작성 후 `references/red-flags.md`로 자가 검증한다.
`qa-evaluator` 에이전트는 L3 깊이까지 코드 경로를 추적해야 PASS를 줄 수 있다.

```text
Claude가 산출물 생성 → 검증 기준으로 자가 확인 → 실패 시 수정 후 재검증
```

### Rule-by-Rule Audit Before Completion — 완료 선언 전 규칙 전수 대조

> **출처:** `/insights` 30일 세션 분석 (Friction Point #1: Proactive quality gaps in refactoring) · Anthropic Skill Authoring Best Practices "Observe how Claude navigates Skills"

Claude 는 리팩터링/대량 편집 시 **규칙에 이미 기재된 위반을 놓치고** 사용자가 지적해야 비로소 고치는 패턴을 반복한다. 이를 방지하려면 스킬이 규칙 리스트(Gotchas, anti-patterns, contract categories, style migrations)를 보유할 경우, 완료 선언 전에 **규칙별 1:1 대조 패스** 를 강제해야 한다.

**원칙:**
- 스킬 산출물 제출 전, Gen 이 자기 스킬의 규칙 리스트를 다시 읽고 각 규칙에 대한 위반 여부를 파일/라인 근거와 함께 보고
- 체크 결과를 리포트(또는 dryrun 출력)로 Gen 자신이 스스로 확인 — 사용자가 첫 피드백 루프가 되면 안 됨
- "그 외에도 혹시 놓친 규칙이 있는가?" 1 회 더 스스로 질문 (meta-audit)

**안티패턴 (insights-report 인용):** "Claude fixes some issues, you point out missed ones, Claude fixes those, you find more." 이 N 회 왕복을 "1 review + 1 execution" 으로 축약하는 것이 본 원칙의 목적이다.

```text
Bad:  Claude 편집 완료 → 사용자가 놓친 규칙 지적 → 반복
Good: Claude 편집 → 규칙 체크리스트 전수 대조 → 위반 목록 발견 → 수정 → 완료 선언
```

---

## 4. 디스크립션은 트리거 조건이다

> **출처:** [Skill Authoring Best Practices — Writing effective descriptions](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices#writing-effective-descriptions)

스킬의 `description` 필드는 사람을 위한 요약이 아니라 **Claude가 스킬을 선택하는 트리거 조건**이다. Claude 는 세션 시작 시 모든 스킬의 메타데이터(name + description)를 시스템 프롬프트에 pre-load 하며, 이 값 하나로 100개 이상의 스킬 중 어느 것을 로드할지 판단한다.

### frontmatter 필드 규칙 (공식 스키마)

> **출처:** [Skill Authoring Best Practices — YAML frontmatter requirements](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices#yaml-frontmatter-requirements)

SKILL.md frontmatter 는 두 개의 필수 필드를 가지며, 각 필드는 엄격한 검증 규칙을 따른다.

**`name` 필드 규칙:**
- 최대 64 자
- 소문자 + 숫자 + 하이픈(`-`) 만 허용
- XML 태그 금지
- 예약어 금지: `anthropic`, `claude` 포함 불가
- **gerund form(동명사) 권장**: `processing-pdfs`, `analyzing-spreadsheets`, `testing-code`
- 허용 대안: 명사구(`pdf-processing`), 동사형(`process-pdfs`)
- **금지:** `helper`, `utils`, `tools`, `documents` 같은 모호한 이름

**`description` 필드 규칙:**
- 최대 1024 자
- 비어 있을 수 없음
- XML 태그 금지
- **3인칭으로 작성한다 (필수).** 1인칭("I can help...") 또는 2인칭("You can use this...")은 시스템 프롬프트에 주입되었을 때 관점 불일치로 인해 discovery 실패를 일으킨다

### 3인칭 작성 규칙

> **출처:** [Skill Authoring Best Practices — Writing effective descriptions](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices#writing-effective-descriptions) — "Always write in third person. The description is injected into the system prompt, and inconsistent point-of-view can cause discovery problems."

**Bad — 1인칭/2인칭 혼용:**

```yaml
description: "I can help you process Excel files"
description: "You can use this to process Excel files"
```

**Good — 3인칭 선언문:**

```yaml
description: Processes Excel files and generates reports. Use when analyzing .xlsx files, pivot tables, or tabular data.
```

### Undertrigger 경향과 "pushy" 디스크립션

> **출처:** [skill-creator SKILL.md — Description Best Practices](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md) — "Claude has a tendency to 'undertrigger' skills — to not use them when they'd be useful. To combat this, please make the skill descriptions a little bit 'pushy'."

Claude 는 구조적으로 스킬을 **undertrigger** (필요한데도 안 쓰는) 하는 경향이 있다. 이를 보정하기 위해 description 은 약간 "pushy" 해야 한다 — 트리거 맥락, 파일 유형, 사용자가 말할 법한 키워드를 명시적으로 나열해라.

**Bad — 무엇을 하는지만 설명 (트리거 약함):**

```yaml
description: How to build a simple fast dashboard to display internal data.
```

**Good — 트리거 맥락까지 나열 (undertrigger 방지):**

```yaml
description: >
  How to build a simple fast dashboard to display internal data.
  Use this skill whenever the user mentions dashboards, data visualization,
  internal metrics, or wants to display any kind of company data,
  even if they don't explicitly ask for a "dashboard".
```

### Bad / Good 기본 예시

**Bad:**

```yaml
description: 배포 관련 스킬
```

**Good:**

```yaml
description: >
  Deploys services to production and verifies deployment status.
  Use when the user requests production deployment, PR merge checks,
  or asks to "deploy", "ship", or "roll out" a service.
```

**"무엇을 하는 스킬인가"뿐 아니라 트리거 키워드와 비트리거 조건까지 명시해야 한다.**

### 이 프로젝트의 실제 예시

`sprint-contract` 스킬의 description:

```yaml
description: >
  기능 구현 전 완료 조건을 정의하고 사용자 합의를 받는다.
  QA Evaluator가 평가할 기준이 되는 Sprint Contract를 생성한다.
  "기능 만들어줘", "화면 추가", "구현해줘", "개발해줘" 같은
  구현 요청에서 /develop보다 먼저 트리거된다.
  단순 수정(색상 변경, 오타 수정, 1파일 변경)에는 트리거하지 않는다.
```

"무엇을 하는 스킬인가"뿐 아니라, **트리거 키워드**("기능 만들어줘", "구현해줘")와 **비트리거 조건**(단순 수정)까지 명시하고 있다.

`init` 스킬도 마찬가지로 비트리거 조건을 명시한다:

```yaml
description: >
  현재 프로젝트에 .harness/ 디렉토리를 생성하고 초기 설정 파일을 세팅한다.
  "harness 초기화", "harness init", "QA 세팅해줘" 같은 요청에 사용.
  이미 .harness/가 존재하면 트리거하지 않는다.
```

### 트리거 키워드 중복 방지 원칙

플러그인이 여러 스킬을 포함할 때, **description에 사용하는 트리거 키워드는 다른 스킬과 두 가지 검사를 모두 통과해야 한다:**

1. **Set intersection 이 공집합** — 동일 키워드가 두 스킬 description 에 동시에 등장하지 않음
2. **Substring containment 도 공집합** — 어느 키워드도 다른 스킬 키워드의 부분문자열(substring)이 아님

같은 키워드(또는 포함 관계의 키워드)가 두 스킬의 description에 모두 등장하면 Claude가 어떤 스킬을 선택할지 예측하기 어렵다. 단순 `Grep` 은 부분문자열 중복을 놓치므로, 키워드 목록을 정규식으로 추출한 뒤 **set intersection + substring 검사** 를 모두 수행해야 한다.

**Bad — substring containment 위반 (실제 REJECT 사례, react-kit RE-02):**

```text
react-feature description: "... API 연동 화면을 한 번에 생성 ..."
react-api     description: "... API 연동 시 Clean Arch 4계층 ..."

키워드 "API 연동" 이 "API 연동 화면" 의 부분문자열 → 배타성 위반 → REJECT
```

또 다른 실제 REJECT 사례 (react-kit SK-05): `react-run` 의 `wasm-pack 빌드` 가 `react-wasm` 의 `wasm-pack 빌드` 와 정확히 일치 → set intersection 위반.

**Bad — 중복 키워드로 충돌 발생:**

```yaml
# 스킬 A
description: "테스트 만들어줘" 요청에 React 컴포넌트 테스트를 생성한다.

# 스킬 B (다른 스킬)
description: "테스트 만들어줘" 요청에 Flutter 위젯 테스트를 생성한다.
```

**Good — 키워드 분리로 명확한 트리거:**

```yaml
# 스킬 A
description: React 컴포넌트 테스트 생성. "React 테스트", "컴포넌트 테스트 만들어줘" 요청에 사용.

# 스킬 B
description: Flutter 위젯 테스트 생성. "Flutter 테스트", "위젯 테스트 만들어줘" 요청에 사용.
```

**예외:** 동일 키워드라도 **플랫폼/스택 컨텍스트로 명확히 구분**되는 경우는 허용된다. 단, description에 구분 조건을 반드시 명시해야 한다:

```yaml
description: >
  Flutter 프로젝트에서 "화면 추가" 요청에 사용.
  React 프로젝트에서는 react-screen 스킬이 우선한다.
```

---

## 5. 점진적 공개(Progressive Disclosure)

> **출처:** [Skill Authoring Best Practices — Progressive disclosure patterns](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices#progressive-disclosure-patterns)

메인 스킬 파일에 모든 정보를 넣지 않는다. 파일을 분리하고 목록만 제공한다.

### 3-레벨 로딩 시스템

스킬은 3 단계로 컨텍스트에 로드된다:

1. **Metadata** (~100 단어, 항상 시스템 프롬프트에 상주): `name` + `description`
2. **SKILL.md body** (스킬이 트리거될 때 로드): 핵심 지침과 워크플로우
3. **Bundled resources** (필요할 때만 읽음): `scripts/`, `references/`, `assets/`

메타데이터만 항상 상주하고 나머지는 on-demand 로 읽는다. 바로 이 구조가 "컨텍스트 절약"의 핵심이다.

### SKILL.md 본문 500 라인 상한 (공식)

> **출처:** [Skill Authoring Best Practices — Token budgets](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices#token-budgets) — "Keep SKILL.md body under 500 lines for optimal performance."

SKILL.md 의 본문은 **500 라인 미만**으로 유지한다. 초과하면:

- `references/` 로 API 레퍼런스, 긴 설명을 분리
- `templates/` 로 출력 포맷 예시 분리
- `scripts/` 로 반복 로직을 실행 가능한 스크립트로 분리

500 라인은 "성능 최적화 한계"이며 강제 제약은 아니지만, 넘으면 스킬이 로드될 때 컨텍스트 사용량이 급격히 증가한다.

### Reference 파일은 1-level deep (필수)

> **출처:** [Skill Authoring Best Practices — Avoid deeply nested references](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices#avoid-deeply-nested-references) — "Keep references one level deep from SKILL.md. All reference files should link directly from SKILL.md to ensure Claude reads complete files when needed."

Claude 는 참조 파일이 **다른 참조 파일에서 다시 링크**되어 있을 때 `head -100` 같은 명령으로 일부만 미리보는 경향이 있어 정보 누락이 발생한다. 모든 reference 는 SKILL.md 에서 직접 링크되어야 한다.

**Bad — 너무 깊음:**

```markdown
# SKILL.md
See [advanced.md](advanced.md)...

# advanced.md
See [details.md](details.md)...

# details.md
Here's the actual information...
```

**Good — 1-level deep:**

```markdown
# SKILL.md
**Basic usage**: [instructions inline]
**Advanced features**: See [advanced.md](advanced.md)
**API reference**: See [reference.md](reference.md)
**Examples**: See [examples.md](examples.md)
```

**추가 규칙:** 100 라인을 넘는 reference 파일에는 상단에 Table of Contents 를 포함한다 (부분 미리보기 상황에서도 전체 스코프를 파악할 수 있도록).

### 메인 스킬 파일 구성 방법

메인 파일에는 개요와 폴더 내 파일 목록만 명시한다:

- API 함수 시그니처는 `references/api.md`에 넣는다
- 출력 템플릿은 `templates/report.md`에 넣는다
- 스킬 MD에 폴더 내 파일 목록을 명시하면, Claude는 필요할 때만 해당 파일을 읽어 컨텍스트를 효율적으로 관리한다

밀키트 상자에 내용물을 명시하여 요리사가 필요한 것만 꺼내 쓰는 것과 같다.

---

## 5.5. Degrees of Freedom — 자유도를 태스크에 맞춰라

> **출처:** [Skill Authoring Best Practices — Set appropriate degrees of freedom](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices#set-appropriate-degrees-of-freedom)

스킬의 구체성 레벨은 태스크의 **취약성(fragility)** 과 **가변성(variability)** 에 맞춰야 한다. Anthropic 공식 문서는 3 단계로 구분한다.

| 자유도 | 형식 | 사용 시점 |
|--------|------|-----------|
| **High freedom** | 텍스트 지침 | 여러 접근이 유효, 문맥에 따라 판단, 경험 기반 heuristic |
| **Medium freedom** | 파라미터 있는 pseudocode/script | 선호 패턴이 있으나 일부 변형 허용 |
| **Low freedom** | 파라미터 없는 정확한 명령 | 취약한 작업, 일관성 필수, 정확한 순서 필요 |

**비유 (공식 문서 인용):** Claude 를 경로를 탐색하는 로봇으로 생각하라.
- 양옆이 낭떠러지인 좁은 다리 → 안전한 길이 하나 → Low freedom (정확한 명령)
- 위험 없는 열린 들판 → 여러 길이 성공 → High freedom (일반 방향만 제시)

### L1/L2/L3 네이밍 충돌 해결 권고

이 프로젝트는 qa-evaluator 의 **검증 깊이 L1/L2/L3** 와 이 자유도 개념을 혼동하면 안 된다:

- **L1/L2/L3** = **QA 평가 깊이** (Glob → Grep → Read/Bash)
- **High/Medium/Low freedom** = **스킬 지침의 구체성 레벨**

스킬 지침의 구체성을 논할 때는 반드시 "high/medium/low freedom" 용어를 사용하고, L1/L2/L3 은 QA 검증 깊이 전용으로 예약한다.

### Enumerate-before-Act — Low-freedom 영역의 고정 규율

> **출처:** `/insights` 30일 세션 분석 (Friction Point #2: Wrong approach and false dichotomies in architecture work)

**토큰 네이밍, Figma 컴포넌트 식별, 스펙 수치, 디자인 시스템 컬러 · 계약 카테고리 ID** 같은 low-freedom 영역은 편집 전 반드시 **enumerate-before-act** 를 적용한다:

1. 편집 시작 전, 기존에 존재하는 토큰/옵션/스펙을 **전부 목록화**
2. 대상 후보를 1-N 인덱스로 나열하여 Gen 스스로 또는 사용자가 지목하게 함
3. 지목된 항목을 최종 확인 후 편집 시작

**실패 사례 (insights-report 인용):** "Claude often commits to an approach (widget choice, contract wording, solution framing) without verifying against Figma tokens, existing code, or your actual intent, leading to rework cycles."

Low-freedom 영역에서 "근사치로 추정" 또는 "아마도 이게 맞을 것 같다" 는 3+ iteration 재작업의 가장 큰 원인이다. 한 번의 enumerate 로 N 번의 왕복이 방지된다.

---

## 6. 스크립트 폴더 — 헬퍼 함수 제공

스킬 안에 스크립트를 넣어 Claude에게 **헬퍼 함수 라이브러리**를 제공한다.

```text
my-skill/
└── scripts/
    ├── fetch_events.py    # 이벤트 조회 함수
    ├── compare_code.sh    # 코드 비교 유틸리티
    └── validate.sh        # 결과 검증 스크립트
```

Claude는 보일러플레이트를 반복 작성하는 대신 **조합에 집중**할 수 있다.

---

## 7. 온 디맨드 훅스(On Demand Hooks) — 상황별 모드 부여

Claude가 도구를 쓰기 직전에 자동으로 검사하는 검문소를 설치하는 기능이다.

### 안전 모드 (`/careful`)

프로덕션 서버 작업 시 위험한 명령을 차단한다:
- `rm -rf`
- `DROP TABLE`
- `git push --force`

### 동결 모드 (`/freeze`)

디버깅 시 특정 폴더만 수정 가능하도록 잠근다:
- 로그 추가 시 다른 파일 수정 방지
- 의도치 않은 변경 차단

### 모드 전환 패턴

```text
평소: 자유 모드 (제한 없음)
  ↓ 위험한 작업
프로덕션: 안전 모드 (위험 명령 차단)
  ↓ 디버깅 필요
디버깅: 동결 모드 (특정 폴더만 수정 가능)
  ↓ 작업 완료
자동 해제: 자유 모드로 복귀
```

필요한 순간에만 가드레일을 올렸다 내렸다 할 수 있다.

---

## 8. 스킬 공유 전략

| 규모 | 방법 |
|------|------|
| 소규모 팀 | `references/` 폴더에 스킬 추가하여 팀원 간 공유 |
| 대규모 팀 | 플러그인 마켓플레이스 방식 — 필요한 스킬만 설치 |
| Anthropic 방식 | 샌드박스 폴더 → Slack 홍보 → 사용량 많으면 공식 마켓 등록 |

### 크로스 플랫폼 호환

> **출처:** [Codex CLI Agent Skills](https://developers.openai.com/codex/skills), [skills.sh](https://skills.sh)

2026년 기준 `SKILL.md` 형식은 Claude Code, Codex CLI, Cursor, Gemini CLI, Antigravity 등에서 호환된다. 스킬을 작성할 때 특정 도구에 종속되지 않도록 하면 여러 플랫폼에서 사용할 수 있다.

**호환성 유지 규칙:**
- frontmatter는 `name`, `description` 필드를 공통으로 사용 (모든 플랫폼 지원)
- `argument-hint`, `user-invocable` 등 Claude Code 전용 필드는 다른 플랫폼에서 무시됨 (호환에 영향 없음)
- 본문의 Process/Gotchas 구조는 마크다운이므로 플랫폼 무관
- 플랫폼 전용 기능(hooks, MCP 서버)은 별도 설정 파일로 분리

---

## 8.5. Evaluation-Driven Development — 평가 먼저, 문서 나중

> **출처:** [Skill Authoring Best Practices — Build evaluations first](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices#build-evaluations-first) — "Create evaluations BEFORE writing extensive documentation."

스킬 작성의 기본 순서는 **문서 먼저가 아니라 평가(eval) 먼저** 다. 존재하지 않는 문제를 문서화하지 않기 위함이다.

### 공식 권장 개발 루프

1. **Gap 식별**: 스킬 없이 대표 태스크를 Claude 로 실행해 실패 지점을 기록
2. **Eval 생성**: 이 gap 을 검증할 **최소 3개 시나리오** 작성
3. **Baseline 측정**: 스킬 없는 상태에서 Claude 의 성능 측정
4. **최소 지침 작성**: gap 을 해결할 만큼의 최소한의 본문만 작성
5. **반복**: eval 실행 → baseline 대비 → 리팩터링

### Eval 구조 예시

```json
{
  "skills": ["pdf-processing"],
  "query": "Extract all text from this PDF file and save it to output.txt",
  "files": ["test-files/document.pdf"],
  "expected_behavior": [
    "Successfully reads the PDF file using an appropriate library or CLI",
    "Extracts text content from all pages without missing any",
    "Saves to output.txt in a clear, readable format"
  ]
}
```

### Trigger Eval Set (description 최적화 시)

> **출처:** [skill-creator SKILL.md — Description Optimization](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md#description-optimization-when-skill-is-ready)

스킬이 준비되면 description 의 트리거 정확도를 측정한다. **20개 쿼리** (should-trigger 8-10개 + should-not-trigger 8-10개) 를 작성하고, 각 쿼리는:

- 구체적이고 현실적 (파일 경로, 회사명, URL, 오타 포함)
- 다양한 표현 (캐주얼/포멀, 간접적 언급)
- near-miss 도 포함 (인접 도메인, 모호한 표현)

**Bad**: "Format this data" (너무 일반적)
**Good**: "ok so my boss just sent me this xlsx file... revenue is in column C..."

이 레포의 `flutter-toolkit/evals/evals.json` 이 이 패턴의 실제 구현이다.

---

## 8.6. MCP 도구 참조 — Fully-Qualified Name 필수

> **출처:** [Skill Authoring Best Practices — MCP tool references](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices#mcp-tool-references) — "If your Skill uses MCP tools, always use fully qualified tool names to avoid 'tool not found' errors."

스킬이 MCP (Model Context Protocol) 도구를 참조할 때는 반드시 **fully-qualified name** 을 사용한다.

**형식:** `ServerName:tool_name`

**Good:**

```markdown
Use the `BigQuery:bigquery_schema` tool to retrieve table schemas.
Use the `GitHub:create_issue` tool to create issues.
```

**Bad — 서버 prefix 누락:**

```markdown
Use the `bigquery_schema` tool to retrieve schemas.
```

여러 MCP 서버가 활성화된 경우 서버 prefix 가 없으면 Claude 가 도구를 찾지 못하거나 잘못된 서버의 도구를 호출할 수 있다.

---

## 8.7. Code Examples — Fenced Block 품질 규칙

> **출처:** plugin QA REJECT 반복 사례 (react-kit DG-01/DG-02, reflect-kit AP-03, infra/backend-kit bare fence)

SKILL.md 안의 코드 예시는 **생성될 실제 코드** 또는 **설명용 의사 코드** 중 하나의 역할을 명확히 해야 한다. 아래 3 원칙을 지킨다:

1. **모든 fenced code block 에 언어 힌트 필수.** bare fence(``` 단독) 금지. 실행 가능한 코드면 `bash`, `python`, `dart`, `typescript`, `yaml`, `json` 등. 설명용이면 `text` 또는 `pseudo`
2. **코드 템플릿 내부에 `TODO` / `FIXME` / 미완성 placeholder 금지.** 스킬이 "생성하라" 고 지시하는 템플릿은 그대로 실행 가능한 상태여야 함 — 사용자가 손으로 채워야 하는 부분은 `// 여기에 비즈니스 로직 구현` 같은 **명시적 주석** 으로 전환
3. **인용/모조 코드와 실행 코드의 구분 명확.** "예시" 블록은 `text` 로, "이 코드를 생성하라" 블록은 해당 언어로

**Bad — bare fence + TODO 잔존 (react-kit DG-01 REJECT 사례):**

````text
```
function handleSubmit(data) {
  // TODO: 유효성 검사
  // TODO: API 호출
}
```
````

**Good — 언어 힌트 + 실행 가능한 템플릿:**

````text
```typescript
function handleSubmit(data: FormData): Result<void, SubmitError> {
  const validated = schema.safeParse(data);
  if (!validated.success) return err(ValidationError.fromZod(validated.error));
  return submitUseCase.execute(validated.data);
}
```
````

**검증법:** SKILL.md 저장 후 `rg -n '^```\s*$' <file>` 로 bare fence 탐지, `rg -n 'TODO|FIXME' <file>` 로 placeholder 잔존 탐지. 둘 다 0건이어야 한다.

---

## 8.8. Sibling-Skill Principle Consistency — 형제 스킬 간 원칙 일관성

> **출처:** plugin QA REJECT 반복 사례 (rust-kit H-01, H-03)

하나의 kit 내 **동일 계열 스킬** (init / feature / api / service 등) 에 공통으로 적용되는 원칙은 **모든 sibling SKILL.md 의 Gotchas 에 동일한 표현으로 등장해야 한다.**

**원칙 (rust-kit H-01/H-03 실제 REJECT 사례):**

- `rust-service` SKILL.md Gotchas 에는 "Composition Root 단일화" 원칙이 있는데 `rust-api` SKILL.md 에는 누락 → H-03 REJECT
- `rust-service` SKILL.md Gotchas 에는 "domain event + outbox" 원칙이 있는데 `rust-init` · `rust-feature` 에는 누락 → H-01 REJECT

이 누락은 "일부 스킬은 원칙을 알고 있지만 다른 스킬은 모른다" 는 **비대칭 지식 상태** 를 만들어, 사용자가 어떤 스킬로 들어오느냐에 따라 완성도가 달라진다.

**Bad — 형제 스킬 간 원칙 비대칭:**

```text
rust-service/SKILL.md  Gotchas: ["Composition Root 단일화 ...", "domain event + outbox ..."]
rust-api/SKILL.md      Gotchas: ["... (Composition Root 누락) ..."]
rust-init/SKILL.md     Gotchas: ["... (domain event 누락) ..."]
```

**Good — 동일 표현으로 전 sibling 에 등장:**

```text
rust-service/SKILL.md  Gotchas: ["Composition Root 단일화 원칙", "domain event + outbox"]
rust-api/SKILL.md      Gotchas: ["Composition Root 단일화 원칙", "domain event + outbox"]
rust-init/SKILL.md     Gotchas: ["Composition Root 단일화 원칙", "domain event + outbox"]
```

**운영 절차:**
- 새 Gotcha 를 sibling 중 한 곳에 추가하면 **전 sibling 스킬 SKILL.md 를 동시에 grep 하여 동일 표현 누락 여부 확인**
- kaizen (플러그인 개선 Phase) 에서 kit 단위 cross-check 필수 — 각 kit 의 sibling group 을 식별한 뒤 공통 원칙 리스트를 생성하고 누락 탐지

---

## 9. 실전 시작 가이드

### 처음부터 완벽하게 만들지 마라

1. **몇 줄의 지시문 + Gotchas 1개**로 시작
2. Claude가 실수할 때마다 Gotchas에 한 줄씩 추가
3. 반복되는 참조 자료가 생기면 `references/` 폴더로 분리
4. 헬퍼 스크립트가 필요하면 `scripts/` 폴더 추가
5. 출력 형식이 정해지면 `templates/` 폴더 추가

### 스킬 성장 사이클

```text
v0.1: 지시문 3줄 + Gotchas 1개
  ↓ Claude가 API 호출 순서 틀림
v0.2: Gotchas에 호출 순서 규칙 추가
  ↓ 같은 API 문서를 매번 설명해야 함
v0.3: references/api.md 분리
  ↓ 반복되는 검증 로직 발생
v0.4: scripts/validate.sh 추가
  ↓ 출력 형식이 매번 다름
v0.5: templates/report.md 추가
```

> 스킬은 문서가 아니라, **에이전트의 실패를 관찰하며 경험치를 쌓는 살아 있는 시스템**이다.

### Long-Running Skills — Checkpoint Commits & SESSION_LOG

> **출처:** `/insights` 30일 세션 분석 (Friction Point #3: Session truncation and tool/infrastructure failures)

긴 멀티페이즈 스킬(`kaizen-orchestrator`, `create-kit`, `/docs-site`, sprint-level refactor 등) 은 **output_token_limit · sandbox 차단 · 백그라운드 에이전트 행업** 등으로 중단될 가능성이 구조적으로 높다. 30일 세션 로그 분석에서 평균 세션 길이가 6시간에 달하고, 5+ 세션이 output 토큰 제한으로 잘렸다.

이런 스킬은 설계 시점부터 **중단 복원 가능성(resumability)** 을 원칙으로 삼는다:

1. **Checkpoint commit** — 각 페이즈 또는 주요 단계 완료 직후 commit & push. 마지막 한 번에 commit 하지 않음
2. **SESSION_LOG.md** — 각 체크포인트마다 3-line 상태를 `SESSION_LOG.md` 에 append (무엇 완료 · 다음 할 일 · 블로커) → 다음 세션이 이 파일만 읽고 resume 가능
3. **응답당 300 라인 제한** — 스킬 지침에 "한 응답에 300 라인 초과하면 분할" 명시
4. **중첩 스킬 호출 간 반환 데이터 최소화** — 토큰 경제 상 요약만 반환

**적용 예시:** `kaizen-orchestrator` 스킬은 Phase 1~10 을 각 Phase 별 sub-agent + 각자 commit 으로 분할하여 어느 Phase 에서 중단되어도 다음 Phase 를 독립적으로 재개할 수 있다.

---

## 10. 적용 사례 — 이 프로젝트의 스킬 분석

이 프로젝트(`claude-plugins`)의 실제 스킬 2개를 가이드 원칙과 대조한다.

### 현재 스킬 구조

```text
harness/skills/
├── init/
│   └── SKILL.md              # 단일 파일
└── sprint-contract/
    └── SKILL.md              # 단일 파일
```

두 스킬 모두 **단일 SKILL.md 파일**로 구성되어 있다. 가이드에서 권장하는 폴더 패턴(references/, scripts/, templates/)은 아직 적용되지 않았다.

### 잘 된 점

**트리거 조건이 구체적이다.** 두 스킬 모두 description에 트리거 키워드와 비트리거 조건을 명시한다 (섹션 4 원칙 충족).

**외부 스크립트와 연동한다.** `init` 스킬은 직접 로직을 품지 않고 `harness/scripts/init.sh`를 호출한다. 스킬은 지시문, 스크립트는 실행 — 역할이 분리되어 있다.

**설정 기반 동작.** `sprint-contract`는 `.harness/project.yaml`에서 카테고리, 안티패턴, 트리거 조건을 읽는다. 스킬에 프로젝트별 지식을 하드코딩하지 않는다.

### 개선 기회

**Gotchas 섹션이 없다.** 두 스킬 모두 Claude가 반복적으로 실패하는 지점을 기록하지 않고 있다. 예를 들어:

- `init`: 스크립트 경로를 못 찾는 경우, Windows 환경에서 bash 경로 차이
- `sprint-contract`: 복잡도 판단 기준 오류, 카테고리 수 과다/과소 생성

이런 실패가 관찰될 때마다 Gotchas에 한 줄씩 추가하면 스킬의 신뢰성이 점진적으로 올라간다.

**폴더 확장 여지.** `sprint-contract`는 현재 SKILL.md 하나에 6단계 프로세스, Red Flags, Rationalization Table까지 모두 담고 있다 (약 160줄). 스킬이 더 성장하면:

```text
sprint-contract/
├── SKILL.md                    # 개요 + 파일 목록 + Gotchas
├── references/
│   └── config-schema.md        # project.yaml 스키마 상세
└── templates/
    ├── simple-contract.md      # 단순 복잡도 예시
    └── complex-contract.md     # 복잡 복잡도 예시
```

### 성장 경로 요약

| 현재 상태 | 다음 단계 | 트리거 |
|-----------|-----------|--------|
| SKILL.md만 있음 | Gotchas 섹션 추가 | Claude가 같은 실수를 2회 이상 반복할 때 |
| 모든 내용이 SKILL.md에 | references/ 분리 | SKILL.md가 200줄을 넘거나, 같은 참조를 매번 읽을 때 |
| 예시 없음 | templates/ 추가 | 출력 형식이 매번 달라질 때 |

---

## 11. 원칙 전수성 · Cross-Surface Parity Checklist

> **배경 (meta-issue):** 지난 kaizen 사이클에서 `skill-design-guide §3.5 "계약 모호성 방지 원칙"` 은 이 가이드에만 추가되었고 `agent-design-guide` 에 전수되지 않아 design-kit PH-01 REJECT 가 발생했다. 가이드 레벨의 변경이 **파생 산출물(계약 설계 가이드, 평가자 가이드, 하위 스킬 Gotchas) 로 자동 전파되지 않는다** 는 구조적 공백이 있었다.

### 원칙

스킬 설계 가이드가 개정되면, **에이전트 설계 가이드 · contract-design-guide · qa-evaluation-guide · 하위 스킬 Gotchas** 에 대응 원칙이 존재하는지 **자동으로 체크** 해야 한다. 전파가 필요한 원칙인지, 스킬 전용인지 판정하고 전자라면 즉시 복제한다.

### 전수 대상 parity items (5개)

두 가이드(skill-design-guide, agent-design-guide)는 아래 5개 항목을 **동일한 개념 · 동일한 용어** 로 공유한다:

| # | Parity Item | skill-design-guide 위치 | agent-design-guide 대응 위치 |
|---|-------------|------------------------|------------------------------|
| 1 | 계약 모호성 방지 / Binary Decidability | §3.5 (QA 계약과 1:1 매칭) | §3.5 (Binary Decidability Pre-Check) |
| 2 | 트리거 키워드 배타성 (substring 포함) | §4 (트리거 키워드 중복 방지) | §3 description 트리거 + §10 sibling agent 검사 |
| 3 | 검증 가능한 성공 기준 | §3.6 (Give a way to verify) | §10 Reviewer L3 커버리지 |
| 4 | Rule-by-rule audit before completion | §3.6 (Rule-by-Rule Audit) | §10 Reviewer 전수 대조 |
| 5 | Unverifiable / degraded-mode 정책 | — (해당 없음 · 에이전트 전용) | §10 Unverifiable 조건 정책 |

Item 5 는 평가자 행동에만 관련되므로 skill-design-guide 에는 존재하지 않는다. 이 예외는 문서화된 상태이며 다른 4개는 **양쪽 모두 존재** 한다.

### 개정 시 체크리스트

skill-design-guide.md 를 편집할 때:

- [ ] 새 원칙을 추가했는가? → agent-design-guide 에 대응 항목이 필요한지 판정
- [ ] 원칙 네이밍(카테고리 ID, 섹션명) 을 변경했는가? → agent-design-guide · contract-design-guide · qa-evaluation-guide · 하위 스킬 SKILL.md 에서 동일 네이밍 사용 중인지 Grep 하여 동기화
- [ ] Bad/Good 예시를 추가했는가? → 대응 원칙이 있는 다른 가이드도 Bad/Good 예시를 포함하도록 업데이트 (일관성)
- [ ] frontmatter `version` 을 bump 했는가? → 대응 파일들도 같은 방향으로 bump

### 실패 패턴 (이 원칙 없이 발생한 실제 REJECT)

- **PH-01 (design-kit, 2026-04)**: skill-design-guide §3.5 "계약 모호성 방지" 가 agent-design-guide 에 누락 → 계약 작성자는 원칙을 알지만 평가자는 몰라 평가 시 혼란 → REJECT
- **SK-13 (backend-kit, infra-kit)**: References 섹션이 skill-design-guide 는 요구하지만 하위 스킬(backend-kaizen, infra-kaizen)의 SKILL.md 에는 누락 → 하위 스킬이 상위 guide 를 참조 안 함

---

## 요약

| 원칙 | 핵심 |
|------|------|
| 폴더로 설계 | 마크다운 하나가 아닌 폴더 하나를 설계한다 |
| 뻔한 말 금지 | Claude가 이미 아는 것은 넣지 않는다 |
| Gotchas 최우선 | 반복 실패 지점을 기록하는 것이 가장 높은 가치 |
| frontmatter 스키마 엄수 | name ≤ 64, description ≤ 1024, 3인칭, XML 금지, 예약어 금지 |
| Undertrigger 방지 | description 은 "pushy" 하게 — 트리거 맥락 나열 |
| 500 라인 상한 | SKILL.md body 는 500 라인 미만 |
| Reference 1-level deep | 참조 파일에서 또 참조하지 마라 |
| 자유도 매칭 | high/medium/low freedom 을 태스크 취약성에 맞춰라 |
| **Enumerate-before-Act** | low-freedom 영역은 선(先) 목록화 · 후(後) 편집 |
| **Rule-by-rule audit** | 완료 선언 전 규칙 전수 대조 패스 의무 |
| Eval 먼저 | 최소 3개 평가를 문서보다 먼저 작성 |
| MCP 도구 풀네임 | `ServerName:tool_name` 필수 |
| **Substring 배타성** | 키워드 set intersection + substring containment 모두 공집합 |
| **Code 예시 품질** | fenced block 언어 힌트 필수 · TODO/placeholder 금지 |
| **Sibling 일관성** | 형제 스킬 간 공통 원칙 누락 없이 동일 표현 |
| **Cross-Surface Parity** | skill/agent/contract/eval 가이드의 원칙 전수 검토 |
| **Checkpoint commits** | Long-running 스킬은 페이즈마다 commit + SESSION_LOG |
| 트리거 조건 명시 | description은 "언제 켜라"를 구체적으로 쓴다 |
| 헬퍼 제공 | 스크립트로 보일러플레이트를 줄인다 |
| 모드 부여 | 온 디맨드 훅스로 상황별 가드레일 설정 |
| 점진적 발전 | 몇 줄로 시작해서 실패를 관찰하며 한 줄씩 추가 |

---

## 출처

- [Skill Authoring Best Practices — Claude API Docs](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) (2026-04)
- [Extend Claude with Skills — Claude Code Docs](https://code.claude.com/docs/en/skills)
- [Agent Skills Overview — Claude API Docs](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
- [anthropics/skills — GitHub](https://github.com/anthropics/skills)
- [skill-creator SKILL.md](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md)
- [Equipping Agents for the Real World with Agent Skills — Anthropic Engineering](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
- [Best Practices for Claude Code](https://code.claude.com/docs/en/best-practices)
- [Codex CLI Agent Skills](https://developers.openai.com/codex/skills)
- [skills.sh](https://skills.sh)
