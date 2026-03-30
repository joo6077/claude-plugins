---
title: design-kit 플러그인 설계 스펙
version: 0.1.0
last_updated: 2026-03-30
status: draft
---

# design-kit 플러그인 설계 스펙

## 1. 개요

디자인적으로 검증된 레퍼런스(Apple HIG, Material Design, NNGroup 등)를 리서치/분석하여 UI/UX 지식을 스킬과 에이전트에 녹여넣는 **스택 무관 범용 디자인 플러그인**.

개발 전(디자인 시스템 세팅) → 개발 중(실시간 가이드) → 개발 후(디자인 감사) 전 단계를 커버한다.

## 2. 원칙

- **플러그인 간 의존성 없음** — design-kit, flutter-toolkit, harness는 서로 참조하지 않는다. 연동은 사용자 프로젝트 레벨에서 설정한다.
- **스킬 = 지식 베이스** — 리서치 결과가 별도 저장소가 아니라 스킬의 Gotchas/references/Process에 직접 반영된다.
- **스택 무관** — 디자인 원칙/패턴 레벨에서 가이드하고, 스택별 구현은 각 toolkit 플러그인에 위임한다.

## 3. 플러그인 구조

```
design-kit/
├── .claude-plugin/plugin.json
├── skills/
│   ├── design-system/
│   │   ├── SKILL.md
│   │   ├── references/                  # 토큰 설계 원칙, 스케일 체계
│   │   │   └── token-principles.md
│   │   └── templates/
│   │       └── design-tokens.md         # 토큰 포맷 템플릿
│   ├── design-guide/
│   │   ├── SKILL.md
│   │   └── references/                  # 리서치 결과가 원칙별로 정리
│   │       └── principle-index.md
│   └── design-audit/
│       ├── SKILL.md
│       ├── references/                  # 감사 기준, 체크리스트
│       │   └── audit-criteria.md
│       └── templates/
│           └── audit-report.md          # 감사 리포트 포맷
├── agents/
│   └── design-reviewer.md
├── hooks/
│   └── hooks.json                       # SessionStart 환경 체크
├── scripts/
│   └── env-check.sh                     # 디자인 토큰 파일 존재 여부 등 환경 검증
├── evals/
│   └── evals.json                       # 스킬별 assertion 테스트 케이스
└── README.md
```

**templates/ 배치 근거:** 플러그인 루트가 아닌 스킬 폴더 내부에 배치한다. design-system과 design-audit의 산출물 포맷이 서로 다르므로 각 스킬이 자체 템플릿을 소유하는 것이 적합하다.

## 4. 스킬 설계

### 4.1 design-system (Code Scaffolding)

> **트리거:** "디자인 시스템 세팅", "디자인 토큰", "컬러 팔레트 만들어줘", "design system init", "토큰 체계"
>
> **안티트리거:** 단순 색상 변경, 기존 토큰 값 수정

**하는 일:**
1. 프로젝트의 기존 디자인 시스템 유무 감지
2. 없으면: 리서치 문서 기반으로 토큰 체계 제안 (컬러, 타이포, 스페이싱, 라디우스 등)
3. 있으면: 현재 토큰을 분석해서 리서치 기준과 비교, 개선점 제안
4. 스택 무관 — 원칙만 정의하고, 구체적 코드 생성은 해당 toolkit에 위임

**산출물:** 디자인 토큰 명세 문서 (또는 기존 시스템 분석 리포트)

**초기 Gotchas:**
- 토큰 네이밍에 구체적 값을 넣지 마라 (`blue-500` ✗ → `primary` ✓). 값이 바뀌면 이름과 괴리가 생긴다.
- 스페이싱 스케일은 4px 베이스가 아니면 반드시 근거를 명시하라. 임의 값(5px, 7px)은 시스템을 깨뜨린다.
- 다크 모드를 고려하지 않고 컬러 토큰을 설계하면 나중에 전면 재작업이 필요하다. semantic 토큰(surface, on-surface)을 먼저 정의하라.

### 4.2 design-guide (Library Reference)

> **트리거:** "디자인 가이드", "이 레이아웃 괜찮아?", "UX 조언", "디자인 리뷰해줘" (가벼운 리뷰)
>
> **안티트리거:** 체계적 전수 검사 (→ design-audit 사용)

**하는 일:**
1. 현재 작업 중인 UI 코드/설명을 받아서 관련 디자인 원칙을 참조
2. 리서치 문서에서 해당되는 원칙을 찾아 적용 방법 안내
3. 예: "이 간격은 Apple HIG 기준 최소 터치 타겟 44pt를 충족하지 않습니다"

**design-audit과의 차이:** guide는 개발 중 가벼운 조언, audit은 완성된 UI의 체계적 감사

**초기 Gotchas:**
- 스택별 구현 코드를 직접 제시하지 마라. 원칙과 이유만 설명하고 구현은 해당 toolkit에 맡겨라.
- "보기 좋다", "깔끔하다" 같은 주관적 피드백은 금지. 반드시 출처가 있는 원칙을 근거로 제시하라.
- 한 번에 모든 카테고리를 다 언급하지 마라. 사용자가 물어본 맥락과 관련된 원칙만 집중해서 답하라.

### 4.3 design-audit (Product Verification)

> **트리거:** "디자인 감사", "UI 검수", "design audit", "디자인 품질 검사"
>
> **안티트리거:** 코드 품질/아키텍처 검사 (→ 각 toolkit의 audit 사용)

**하는 일:**
1. 대상 코드/화면을 전체 카테고리 기준으로 체계적 검사
2. 카테고리별 PASS/FAIL 판정 (타이포, 컬러, 스페이싱, 접근성, 인터랙션, 모션)
3. `design-reviewer` 에이전트를 호출해서 독립 평가 (Agent 도구로 서브에이전트 위임)

**산출물:** 감사 리포트 (카테고리별 판정 + 구체적 개선 사항 + 근거 출처)

**호출 패턴:** design-audit 스킬이 메인 대화에서 실행되므로 Agent 도구를 통해 design-reviewer 서브에이전트를 생성한다. 에이전트가 읽기 전용으로 분석 후 결과를 반환하면, 스킬이 이를 리포트로 포맷팅한다.

**초기 Gotchas:**
- 코드 구현 품질(아키텍처, 성능)을 평가하지 마라. 디자인 원칙 준수 여부만 판정한다.
- 디자인 토큰이 없는 프로젝트에서 "토큰 미사용" FAIL을 남발하지 마라. 토큰 체계가 없으면 design-system 스킬 사용을 권장하는 선에서 그쳐라.
- 접근성(a11y) 카테고리를 생략하지 마라. 시각적으로 문제없어 보여도 contrast ratio, 터치 타겟 크기는 반드시 검사한다.

## 5. 에이전트 설계

### 5.1 design-reviewer

> **역할:** design-audit 스킬이 Agent 도구를 통해 호출하는 독립 평가 에이전트

**frontmatter:**
```yaml
---
name: design-reviewer
description: >
  UI 코드를 디자인 원칙 기준으로 독립 평가한다.
  design-audit 스킬에서 Agent 도구로 위임받아 실행된다.
  카테고리별 PASS/FAIL 판정과 근거를 반환한다.
  단독 실행하지 않는다 — 반드시 design-audit을 통해 호출.
tools: Read, Grep, Glob
model: sonnet
---
```

- **평가 카테고리:** typography, color, spacing, accessibility, interaction, motion
- **판정 규칙:** 1 FAIL = REJECT, 모든 판정에 근거 필수 (파일:라인 + 출처)
- **harness qa-evaluator와 동일한 패턴** — 문제를 찾는 것이 유일한 역할, 칭찬 없음

## 6. docs/ 구조 개편

### 6.1 현재 → 변경 후

```
# 현재
docs/
├── skill-design-guide.md
├── agent-design-guide.md
├── kaizen/
└── superpowers/specs/

# 변경 후
docs/
├── guides/                          # 기존 가이드 이동
│   ├── skill-design-guide.md
│   └── agent-design-guide.md
├── design/                          # 디자인 리서치 문서
│   ├── foundations/                  # 기초 원칙
│   │   ├── typography.md
│   │   ├── color.md
│   │   ├── spacing-layout.md
│   │   ├── iconography.md
│   │   └── motion.md
│   ├── interaction/                  # 인터랙션 패턴
│   │   ├── navigation.md
│   │   ├── forms.md
│   │   ├── data-display.md
│   │   └── feedback.md
│   ├── accessibility/
│   │   └── accessibility.md
│   └── systems/                     # 레퍼런스 디자인 시스템 분석
│       ├── apple-hig.md
│       ├── material-design.md
│       └── open-source-systems.md   # Radix, Shadcn 등
├── kaizen/
└── superpowers/specs/
```

### 6.2 문서 frontmatter 표준

`docs/` 하위 **모든** 문서에 공통 적용 (guides/, design/, kaizen/, superpowers/specs/ 포함):

```yaml
---
title: 문서 제목
version: 1.0.0
last_updated: 2026-03-30
---
```

- `version`: 내용이 크게 바뀔 때 semver bump
- `last_updated`: 마지막 수정 날짜
- 출처는 기존 패턴대로 본문 인라인 `> **출처:** [이름](URL)`

## 7. 개발용 스킬 (플러그인에 포함 안 됨)

이 레포의 `.claude/skills/`에 배치. design-kit 플러그인 패키지에는 포함되지 않는다.

### 7.1 design-research

- 레퍼런스 소스 크롤링/분석 → `docs/design/` 문서 갱신
- **크롤링 대상:** 공식 디자인 가이드라인 (Apple HIG, Material Design, Fluent Design), 디자인 리서치 (NNGroup, Baymard, Laws of UX), 실제 제품 분석 (Dribbble/Behance 수상작, 유명 앱 UI 패턴), 오픈소스 디자인 시스템 (Radix, Shadcn, Tailwind)
- 결과를 `docs/design/` 카테고리별 문서에 인라인 출처와 함께 반영

### 7.2 design-kaizen

- design-kit 스킬 품질을 주기적으로 개선
- `docs/design/` 리서치 문서 기준으로 스킬의 Gotchas/references 갱신
- 기존 harness-kaizen, flutter-kaizen과 동일한 패턴

## 8. 리서치 소스 범위

| 카테고리 | 소스 예시 |
|----------|-----------|
| 공식 가이드라인 | Apple HIG, Material Design 3, Fluent Design System |
| 디자인 리서치/논문 | NNGroup, Baymard Institute, Laws of UX |
| 실제 제품 분석 | Dribbble/Behance 수상작, Apple 소프트웨어 제품 UI 패턴 |
| 오픈소스 디자인 시스템 | Radix UI, Shadcn/ui, Tailwind CSS |

## 9. marketplace 등록

`.claude-plugin/marketplace.json`에 design-kit 추가:

```json
{
  "name": "design-kit",
  "source": "./design-kit",
  "description": "[v0.1.0 · 2026-03-30] 스택 무관 UI/UX 디자인 가이드 + 감사 플러그인"
}
```

`design-kit/.claude-plugin/plugin.json`:

```json
{
  "name": "design-kit",
  "description": "스택 무관 UI/UX 디자인 시스템 세팅, 실시간 가이드, 디자인 감사 플러그인",
  "version": "0.1.0",
  "author": { "name": "Jackson Kim" },
  "repository": "https://github.com/joo6077/claude-plugins",
  "license": "MIT",
  "keywords": ["design", "ui", "ux", "design-system", "audit", "accessibility"]
}
```
