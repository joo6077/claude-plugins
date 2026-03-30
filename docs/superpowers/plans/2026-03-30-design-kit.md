# design-kit 플러그인 구현 계획

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 스택 무관 UI/UX 디자인 플러그인(design-kit)을 생성하고, docs/ 구조를 개편하며, 개발용 스킬을 배치한다.

**Architecture:** design-kit은 3개 스킬(design-system, design-guide, design-audit) + 1개 에이전트(design-reviewer)로 구성. docs/를 guides/, design/ 하위로 재구조화하고 모든 문서에 frontmatter를 도입. 개발용 스킬(design-research, design-kaizen)은 .claude/skills/에 배치.

**Tech Stack:** Claude Code plugins, SKILL.md, agents, markdown, bash

---

## 파일 구조

| 액션 | 파일 | 역할 |
|------|------|------|
| Move | `docs/skill-design-guide.md` → `docs/guides/skill-design-guide.md` | 가이드 이동 |
| Move | `docs/agent-design-guide.md` → `docs/guides/agent-design-guide.md` | 가이드 이동 |
| Modify | `docs/guides/skill-design-guide.md` | frontmatter 추가 |
| Modify | `docs/guides/agent-design-guide.md` | frontmatter 추가 |
| Create | `docs/design/foundations/typography.md` | 타이포그래피 리서치 문서 (초기 스켈레톤) |
| Create | `docs/design/foundations/color.md` | 컬러 리서치 문서 |
| Create | `docs/design/foundations/spacing-layout.md` | 스페이싱/레이아웃 리서치 문서 |
| Create | `docs/design/foundations/iconography.md` | 아이코노그래피 리서치 문서 |
| Create | `docs/design/foundations/motion.md` | 모션 리서치 문서 |
| Create | `docs/design/interaction/navigation.md` | 네비게이션 패턴 |
| Create | `docs/design/interaction/forms.md` | 폼 패턴 |
| Create | `docs/design/interaction/data-display.md` | 데이터 표시 패턴 |
| Create | `docs/design/interaction/feedback.md` | 피드백 패턴 |
| Create | `docs/design/accessibility/accessibility.md` | 접근성 |
| Create | `docs/design/systems/apple-hig.md` | Apple HIG 분석 |
| Create | `docs/design/systems/material-design.md` | Material Design 분석 |
| Create | `docs/design/systems/open-source-systems.md` | 오픈소스 디자인 시스템 분석 |
| Create | `design-kit/.claude-plugin/plugin.json` | 플러그인 메타데이터 |
| Create | `design-kit/skills/design-system/SKILL.md` | 디자인 시스템 세팅 스킬 |
| Create | `design-kit/skills/design-system/references/token-principles.md` | 토큰 설계 원칙 |
| Create | `design-kit/skills/design-system/templates/design-tokens.md` | 토큰 포맷 템플릿 |
| Create | `design-kit/skills/design-guide/SKILL.md` | 실시간 디자인 가이드 스킬 |
| Create | `design-kit/skills/design-guide/references/principle-index.md` | 원칙 인덱스 |
| Create | `design-kit/skills/design-audit/SKILL.md` | 디자인 감사 스킬 |
| Create | `design-kit/skills/design-audit/references/audit-criteria.md` | 감사 기준 |
| Create | `design-kit/skills/design-audit/templates/audit-report.md` | 감사 리포트 템플릿 |
| Create | `design-kit/agents/design-reviewer.md` | 디자인 평가 에이전트 |
| Create | `design-kit/hooks/hooks.json` | SessionStart 훅 |
| Create | `design-kit/scripts/env-check.sh` | 환경 검증 스크립트 |
| Create | `design-kit/evals/evals.json` | 스킬별 테스트 케이스 |
| Create | `design-kit/README.md` | 플러그인 문서 |
| Modify | `.claude-plugin/marketplace.json` | design-kit 등록 |
| Create | `.claude/skills/design-research/SKILL.md` | 개발용 리서치 스킬 |
| Create | `.claude/skills/design-kaizen/SKILL.md` | 개발용 카이젠 스킬 |
| Modify | `CLAUDE.md` | design-kit 플러그인 설명 추가 |

---

### Task 1: docs/ 구조 개편 — 가이드 이동 + frontmatter 추가

**Files:**
- Move: `docs/skill-design-guide.md` → `docs/guides/skill-design-guide.md`
- Move: `docs/agent-design-guide.md` → `docs/guides/agent-design-guide.md`
- Modify: `docs/guides/skill-design-guide.md` (frontmatter 추가)
- Modify: `docs/guides/agent-design-guide.md` (frontmatter 추가)

- [ ] **Step 1: guides 디렉토리 생성 및 파일 이동**

```bash
mkdir -p docs/guides
git mv docs/skill-design-guide.md docs/guides/skill-design-guide.md
git mv docs/agent-design-guide.md docs/guides/agent-design-guide.md
```

- [ ] **Step 2: skill-design-guide.md frontmatter 추가**

파일 최상단에 추가:

```yaml
---
title: Claude Code 스킬 설계 가이드
version: 1.0.0
last_updated: 2026-03-30
---

```

기존 `# Claude Code 스킬 설계 가이드` 제목은 유지.

- [ ] **Step 3: agent-design-guide.md frontmatter 추가**

파일 최상단에 추가:

```yaml
---
title: Claude Code 에이전트 설계 가이드
version: 1.0.0
last_updated: 2026-03-30
---

```

기존 `# Claude Code 에이전트 설계 가이드` 제목은 유지.

- [ ] **Step 4: 레포 내 참조 경로 업데이트**

`docs/skill-design-guide.md`와 `docs/agent-design-guide.md`를 참조하는 파일을 검색하고 경로를 `docs/guides/`로 수정:

```bash
grep -r "docs/skill-design-guide" --include="*.md" --include="*.json" .
grep -r "docs/agent-design-guide" --include="*.md" --include="*.json" .
```

찾은 파일마다 경로를 `docs/guides/skill-design-guide.md`, `docs/guides/agent-design-guide.md`로 수정.

- [ ] **Step 5: 기존 docs/ 문서에 frontmatter 추가**

`docs/kaizen/` 및 `docs/superpowers/specs/` 내 기존 문서에도 frontmatter 추가. 각 파일 최상단에:

```yaml
---
title: [기존 문서 제목]
version: 1.0.0
last_updated: 2026-03-30
---
```

대상 파일을 모두 찾아서 처리:

```bash
find docs/kaizen -name "*.md" -type f
find docs/superpowers/specs -name "*.md" -type f
```

각 파일의 첫 번째 `#` 헤더에서 제목을 추출하여 `title` 필드에 사용.

- [ ] **Step 6: 커밋**

```bash
git add docs/guides/ docs/kaizen/ docs/superpowers/specs/
git add -u  # 이동된 파일 + 수정된 참조
git commit -m "refactor: docs/ 구조 개편 — guides/ 이동 + 전체 문서 frontmatter 도입"
```

---

### Task 2: docs/design/ 리서치 문서 스켈레톤 생성

**Files:**
- Create: `docs/design/foundations/typography.md`
- Create: `docs/design/foundations/color.md`
- Create: `docs/design/foundations/spacing-layout.md`
- Create: `docs/design/foundations/iconography.md`
- Create: `docs/design/foundations/motion.md`
- Create: `docs/design/interaction/navigation.md`
- Create: `docs/design/interaction/forms.md`
- Create: `docs/design/interaction/data-display.md`
- Create: `docs/design/interaction/feedback.md`
- Create: `docs/design/accessibility/accessibility.md`
- Create: `docs/design/systems/apple-hig.md`
- Create: `docs/design/systems/material-design.md`
- Create: `docs/design/systems/open-source-systems.md`

- [ ] **Step 1: 디렉토리 생성**

```bash
mkdir -p docs/design/foundations
mkdir -p docs/design/interaction
mkdir -p docs/design/accessibility
mkdir -p docs/design/systems
```

- [ ] **Step 2: foundations/ 문서 생성**

각 파일은 동일한 스켈레톤 구조를 따른다. 내용은 design-research 스킬이 추후 채운다.

`docs/design/foundations/typography.md`:
```markdown
---
title: 타이포그래피
version: 0.1.0
last_updated: 2026-03-30
---

# 타이포그래피

> 이 문서는 design-research 스킬로 채워진다.

## 원칙

## 스케일 체계

## 가독성

## 반응형 타이포그래피
```

`docs/design/foundations/color.md`:
```markdown
---
title: 컬러
version: 0.1.0
last_updated: 2026-03-30
---

# 컬러

> 이 문서는 design-research 스킬로 채워진다.

## 원칙

## 컬러 시스템 구조

## 시맨틱 토큰

## 다크 모드

## 접근성 (Contrast Ratio)
```

`docs/design/foundations/spacing-layout.md`:
```markdown
---
title: 스페이싱 & 레이아웃
version: 0.1.0
last_updated: 2026-03-30
---

# 스페이싱 & 레이아웃

> 이 문서는 design-research 스킬로 채워진다.

## 원칙

## 스페이싱 스케일

## 그리드 시스템

## 터치 타겟
```

`docs/design/foundations/iconography.md`:
```markdown
---
title: 아이코노그래피
version: 0.1.0
last_updated: 2026-03-30
---

# 아이코노그래피

> 이 문서는 design-research 스킬로 채워진다.

## 원칙

## 크기 체계

## 스타일 일관성
```

`docs/design/foundations/motion.md`:
```markdown
---
title: 모션
version: 0.1.0
last_updated: 2026-03-30
---

# 모션

> 이 문서는 design-research 스킬로 채워진다.

## 원칙

## 듀레이션 체계

## 이징 커브

## 트랜지션 패턴
```

- [ ] **Step 3: interaction/ 문서 생성**

`docs/design/interaction/navigation.md`:
```markdown
---
title: 네비게이션 패턴
version: 0.1.0
last_updated: 2026-03-30
---

# 네비게이션 패턴

> 이 문서는 design-research 스킬로 채워진다.

## 원칙

## 네비게이션 구조

## 탭/사이드바/드로어

## 뎁스 관리
```

`docs/design/interaction/forms.md`:
```markdown
---
title: 폼 패턴
version: 0.1.0
last_updated: 2026-03-30
---

# 폼 패턴

> 이 문서는 design-research 스킬로 채워진다.

## 원칙

## 입력 필드

## 유효성 검사 표시

## 폼 레이아웃
```

`docs/design/interaction/data-display.md`:
```markdown
---
title: 데이터 표시 패턴
version: 0.1.0
last_updated: 2026-03-30
---

# 데이터 표시 패턴

> 이 문서는 design-research 스킬로 채워진다.

## 원칙

## 리스트/그리드

## 테이블

## 빈 상태/로딩 상태
```

`docs/design/interaction/feedback.md`:
```markdown
---
title: 피드백 패턴
version: 0.1.0
last_updated: 2026-03-30
---

# 피드백 패턴

> 이 문서는 design-research 스킬로 채워진다.

## 원칙

## 토스트/스낵바

## 다이얼로그/모달

## 에러 상태
```

- [ ] **Step 4: accessibility/ 문서 생성**

`docs/design/accessibility/accessibility.md`:
```markdown
---
title: 접근성
version: 0.1.0
last_updated: 2026-03-30
---

# 접근성

> 이 문서는 design-research 스킬로 채워진다.

## 원칙

## 색상 대비 (WCAG)

## 터치 타겟 크기

## 스크린 리더

## 키보드 네비게이션
```

- [ ] **Step 5: systems/ 문서 생성**

`docs/design/systems/apple-hig.md`:
```markdown
---
title: Apple Human Interface Guidelines 분석
version: 0.1.0
last_updated: 2026-03-30
---

# Apple Human Interface Guidelines 분석

> 이 문서는 design-research 스킬로 채워진다.

## 핵심 원칙

## 플랫폼별 가이드

## 주요 컴포넌트 패턴
```

`docs/design/systems/material-design.md`:
```markdown
---
title: Material Design 분석
version: 0.1.0
last_updated: 2026-03-30
---

# Material Design 분석

> 이 문서는 design-research 스킬로 채워진다.

## 핵심 원칙

## Material 3 토큰 체계

## 주요 컴포넌트 패턴
```

`docs/design/systems/open-source-systems.md`:
```markdown
---
title: 오픈소스 디자인 시스템 분석
version: 0.1.0
last_updated: 2026-03-30
---

# 오픈소스 디자인 시스템 분석

> 이 문서는 design-research 스킬로 채워진다.

## Radix UI

## Shadcn/ui

## Tailwind CSS
```

- [ ] **Step 6: 커밋**

```bash
git add docs/design/
git commit -m "docs: design/ 리서치 문서 스켈레톤 13개 생성"
```

---

### Task 3: design-kit 플러그인 스캐폴딩

**Files:**
- Create: `design-kit/.claude-plugin/plugin.json`

- [ ] **Step 1: 디렉토리 구조 생성**

```bash
mkdir -p design-kit/.claude-plugin
mkdir -p design-kit/skills/design-system/references
mkdir -p design-kit/skills/design-system/templates
mkdir -p design-kit/skills/design-guide/references
mkdir -p design-kit/skills/design-audit/references
mkdir -p design-kit/skills/design-audit/templates
mkdir -p design-kit/agents
mkdir -p design-kit/hooks
mkdir -p design-kit/scripts
mkdir -p design-kit/evals
```

- [ ] **Step 2: plugin.json 작성**

`design-kit/.claude-plugin/plugin.json`:
```json
{
  "name": "design-kit",
  "description": "스택 무관 UI/UX 디자인 시스템 세팅, 실시간 가이드, 디자인 감사 플러그인",
  "version": "0.1.0",
  "author": {
    "name": "Jackson Kim"
  },
  "repository": "https://github.com/joo6077/claude-plugins",
  "license": "MIT",
  "keywords": ["design", "ui", "ux", "design-system", "audit", "accessibility"]
}
```

- [ ] **Step 3: 커밋**

```bash
git add design-kit/
git commit -m "feat: design-kit 플러그인 디렉토리 스캐폴딩"
```

---

### Task 4: design-system 스킬 작성

**Files:**
- Create: `design-kit/skills/design-system/SKILL.md`
- Create: `design-kit/skills/design-system/references/token-principles.md`
- Create: `design-kit/skills/design-system/templates/design-tokens.md`

- [ ] **Step 1: SKILL.md 작성**

`design-kit/skills/design-system/SKILL.md`:
```markdown
---
name: design-system
description: >
  프로젝트에 디자인 토큰 체계(컬러, 타이포, 스페이싱, 라디우스 등)를 세팅한다.
  기존 디자인 시스템이 있으면 리서치 기준과 비교하여 개선점을 제안한다.
  스택 무관 — 원칙만 정의하고, 구체적 코드 생성은 해당 toolkit에 위임한다.
  "디자인 시스템 세팅", "디자인 토큰", "컬러 팔레트 만들어줘",
  "design system init", "토큰 체계" 같은 요청 시 트리거.
  단순 색상 변경, 기존 토큰 값 수정에는 트리거하지 않는다.
argument-hint: "[project-path]"
user-invocable: true
---

# Gotchas

1. **토큰 네이밍에 구체적 값 금지** — `blue-500` ✗ → `primary` ✓. 값이 바뀌면 이름과 괴리가 생긴다. semantic 네이밍만 사용하라.
2. **스페이싱 스케일 근거 필수** — 4px 베이스가 아니면 반드시 근거를 명시하라. 임의 값(5px, 7px)은 시스템을 깨뜨린다.
3. **다크 모드 선행 설계** — 다크 모드를 고려하지 않고 컬러 토큰을 설계하면 전면 재작업이 필요하다. semantic 토큰(surface, on-surface)을 먼저 정의하라.
4. **스택별 코드 생성 금지** — 이 스킬은 원칙과 토큰 명세만 출력한다. Flutter/React/CSS 코드를 직접 생성하지 마라. 해당 toolkit 플러그인에 위임하라.

# Process

## Step 1: 프로젝트 디자인 시스템 감지

프로젝트 루트에서 디자인 토큰/테마 파일을 탐색한다:

```
# 탐색 패턴 (스택 무관)
**/theme/**
**/tokens/**
**/design/**
**/styles/**
**/colors.*
**/typography.*
```

- 발견되면: HAS_DS=true, 기존 토큰 구조를 분석
- 미발견: HAS_DS=false, 신규 토큰 체계 제안 모드

## Step 2: 토큰 카테고리 정의

references/token-principles.md를 참조하여 카테고리별 토큰을 정의한다:

| 카테고리 | 필수 여부 | 예시 |
|----------|-----------|------|
| Color | 필수 | primary, secondary, surface, on-surface, error |
| Typography | 필수 | display-lg, heading-md, body-sm, label-xs |
| Spacing | 필수 | xs(4), sm(8), md(16), lg(24), xl(32) |
| Radius | 필수 | none(0), sm(4), md(8), lg(16), full(9999) |
| Elevation | 선택 | level-0, level-1, level-2, level-3 |
| Motion | 선택 | duration-fast, duration-normal, easing-standard |

## Step 3: HAS_DS=true → 기존 시스템 분석

기존 토큰을 리서치 기준과 비교하여 리포트 출력:
- 누락된 카테고리
- semantic 네이밍 미준수 항목
- 다크 모드 미대응 토큰
- 스케일 일관성 위반

## Step 4: HAS_DS=false → 토큰 명세 생성

templates/design-tokens.md 포맷으로 토큰 명세를 생성한다.
사용자에게 각 카테고리별 선택지를 제시하고 합의를 받는다.

## Step 5: 산출물 확인

- 토큰 명세 문서가 생성/분석되었는지 확인
- 모든 필수 카테고리가 포함되었는지 확인
- semantic 네이밍 규칙이 준수되었는지 확인

# References

- `references/token-principles.md` — 토큰 설계 원칙 상세
- `templates/design-tokens.md` — 토큰 명세 출력 포맷
```

- [ ] **Step 2: token-principles.md 작성**

`design-kit/skills/design-system/references/token-principles.md`:
```markdown
# 토큰 설계 원칙

## 1. 3계층 토큰 구조

> **출처:** [Material Design 3 — Design Tokens](https://m3.material.io/foundations/design-tokens)

| 계층 | 역할 | 예시 |
|------|------|------|
| Reference (원시) | 값 자체 | `blue-500: #2196F3` |
| System (시맨틱) | 역할 기반 매핑 | `primary: ref.blue-500` |
| Component | 컴포넌트별 오버라이드 | `button-bg: sys.primary` |

스킬이 출력하는 토큰 명세는 **System 계층**이다. Reference는 구현 레벨에서 정의하고, Component는 필요 시 toolkit이 생성한다.

## 2. 네이밍 규칙

- semantic 이름만 사용: `primary`, `surface`, `on-primary` ✓
- 값 기반 이름 금지: `blue-500`, `gray-100` ✗
- 크기 스케일은 t-shirt 사이징 또는 숫자 스케일: `sm/md/lg` 또는 `100/200/300`

## 3. 스페이싱 스케일

> **출처:** [Space, Subtraction — Designing Spacing Systems](https://medium.com/eightshapes-llc/space-in-design-systems-188bcbae0d62)

4px 베이스 스케일을 기본으로 한다:
- `xs: 4px`, `sm: 8px`, `md: 16px`, `lg: 24px`, `xl: 32px`, `2xl: 48px`

8px 베이스를 선택할 경우 근거를 명시해야 한다.

## 4. 컬러 시스템

> **출처:** [Apple HIG — Color](https://developer.apple.com/design/human-interface-guidelines/color)

필수 시맨틱 컬러:
- `primary`, `secondary`, `tertiary` — 브랜드/강조
- `surface`, `on-surface` — 배경/텍스트
- `error`, `on-error` — 에러 상태
- `outline`, `outline-variant` — 테두리

다크 모드는 별도 값이 아닌 **동일 토큰의 다크 변형**으로 정의한다.

## 5. 타이포그래피 스케일

> **출처:** [Material Design 3 — Typography](https://m3.material.io/styles/typography)

최소 5단계 스케일:
- `display` — 히어로, 대형 제목
- `heading` — 섹션 제목
- `title` — 카드/리스트 제목
- `body` — 본문
- `label` — 버튼, 캡션

각 단계에 lg/md/sm 서브 사이즈를 둔다.
```

- [ ] **Step 3: design-tokens.md 템플릿 작성**

`design-kit/skills/design-system/templates/design-tokens.md`:
```markdown
# 디자인 토큰 명세

> 생성일: {{date}}
> 프로젝트: {{project-name}}

## Color

### Light Mode

| 토큰 | 역할 | 값 |
|------|------|-----|
| `primary` | 주요 강조 | |
| `on-primary` | primary 위의 텍스트/아이콘 | |
| `secondary` | 보조 강조 | |
| `on-secondary` | secondary 위의 텍스트/아이콘 | |
| `surface` | 기본 배경 | |
| `on-surface` | surface 위의 텍스트 | |
| `error` | 에러 상태 | |
| `on-error` | error 위의 텍스트 | |
| `outline` | 테두리 | |

### Dark Mode

| 토큰 | 역할 | 값 |
|------|------|-----|
| `primary` | | |
| `on-primary` | | |
| `surface` | | |
| `on-surface` | | |

## Typography

| 토큰 | 크기 | 행간 | 두께 |
|------|------|------|------|
| `display-lg` | | | |
| `display-md` | | | |
| `heading-lg` | | | |
| `heading-md` | | | |
| `title-lg` | | | |
| `title-md` | | | |
| `body-lg` | | | |
| `body-md` | | | |
| `body-sm` | | | |
| `label-lg` | | | |
| `label-md` | | | |
| `label-sm` | | | |

## Spacing

| 토큰 | 값 |
|------|-----|
| `xs` | 4px |
| `sm` | 8px |
| `md` | 16px |
| `lg` | 24px |
| `xl` | 32px |
| `2xl` | 48px |

## Radius

| 토큰 | 값 |
|------|-----|
| `none` | 0 |
| `sm` | 4px |
| `md` | 8px |
| `lg` | 16px |
| `full` | 9999px |

## Elevation (선택)

| 토큰 | 설명 |
|------|------|
| `level-0` | 그림자 없음 |
| `level-1` | 미세한 그림자 |
| `level-2` | 카드/시트 |
| `level-3` | 모달/다이얼로그 |
```

- [ ] **Step 4: 커밋**

```bash
git add design-kit/skills/design-system/
git commit -m "feat(design-kit): design-system 스킬 — 토큰 체계 세팅"
```

---

### Task 5: design-guide 스킬 작성

**Files:**
- Create: `design-kit/skills/design-guide/SKILL.md`
- Create: `design-kit/skills/design-guide/references/principle-index.md`

- [ ] **Step 1: SKILL.md 작성**

`design-kit/skills/design-guide/SKILL.md`:
```markdown
---
name: design-guide
description: >
  개발 중 UI 코드/설명을 받아 관련 디자인 원칙을 참조하여 가이드한다.
  스택 무관 — 원칙과 이유만 설명하고 구현은 해당 toolkit에 위임한다.
  "디자인 가이드", "이 레이아웃 괜찮아?", "UX 조언",
  "디자인 리뷰해줘" (가벼운 리뷰) 같은 요청 시 트리거.
  체계적 전수 검사에는 트리거하지 않는다 — design-audit 사용.
argument-hint: "[file-path or description]"
user-invocable: true
---

# Gotchas

1. **스택별 코드 제시 금지** — 원칙과 이유만 설명하라. Flutter/React/CSS 코드를 직접 제시하지 마라. "44pt 이상의 터치 타겟이 필요합니다"는 ✓, "SizedBox(height: 44)"는 ✗.
2. **주관적 피드백 금지** — "보기 좋다", "깔끔하다" 같은 표현 금지. 반드시 출처가 있는 원칙을 근거로 제시하라.
3. **카테고리 과잉 방지** — 한 번에 모든 카테고리를 언급하지 마라. 사용자가 물어본 맥락과 관련된 원칙만 집중해서 답하라. 질문이 타이포그래피에 관한 것이면 컬러 원칙은 언급하지 않는다.

# Process

## Step 1: 맥락 파악

사용자가 제공한 코드/설명에서 관련 디자인 카테고리를 식별한다:

| 카테고리 | 키워드 |
|----------|--------|
| typography | 글꼴, 크기, 행간, 텍스트, font |
| color | 컬러, 색상, 팔레트, 다크모드 |
| spacing | 간격, 패딩, 마진, 정렬 |
| interaction | 버튼, 탭, 스와이프, 제스처 |
| accessibility | 접근성, a11y, 대비, 터치 타겟 |
| motion | 애니메이션, 전환, transition |

## Step 2: 원칙 참조

references/principle-index.md에서 해당 카테고리의 원칙 파일을 찾아 읽는다. 프로젝트에 `docs/design/` 디렉토리가 있으면 해당 리서치 문서를 우선 참조한다.

## Step 3: 가이드 제시

각 피드백 항목은 반드시 이 포맷을 따른다:

```
### [카테고리] 항목 제목

**원칙:** [원칙 이름]
**출처:** [출처 URL 또는 문서명]
**현재:** [현재 구현 상태 설명]
**권장:** [권장 사항]
**이유:** [왜 이렇게 해야 하는지]
```

## Step 4: 요약

- 관련 원칙 수 / 적용 권장 수 요약
- 우선순위가 높은 항목 표시 (접근성 > 사용성 > 미관)

# References

- `references/principle-index.md` — 카테고리별 원칙 문서 인덱스
```

- [ ] **Step 2: principle-index.md 작성**

`design-kit/skills/design-guide/references/principle-index.md`:
```markdown
# 디자인 원칙 인덱스

design-guide 스킬이 참조하는 원칙 문서 매핑. 프로젝트에 `docs/design/`이 있으면 해당 경로를 우선 사용한다.

## 카테고리별 참조 파일

| 카테고리 | 플러그인 내부 | 프로젝트 docs/design/ |
|----------|-------------|----------------------|
| Typography | (SKILL.md Gotchas) | `foundations/typography.md` |
| Color | (SKILL.md Gotchas) | `foundations/color.md` |
| Spacing & Layout | (SKILL.md Gotchas) | `foundations/spacing-layout.md` |
| Iconography | (SKILL.md Gotchas) | `foundations/iconography.md` |
| Motion | (SKILL.md Gotchas) | `foundations/motion.md` |
| Navigation | (SKILL.md Gotchas) | `interaction/navigation.md` |
| Forms | (SKILL.md Gotchas) | `interaction/forms.md` |
| Data Display | (SKILL.md Gotchas) | `interaction/data-display.md` |
| Feedback | (SKILL.md Gotchas) | `interaction/feedback.md` |
| Accessibility | (SKILL.md Gotchas) | `accessibility/accessibility.md` |

## 참조 우선순위

1. 프로젝트의 `docs/design/` (리서치로 채워진 문서)
2. SKILL.md의 Gotchas (최소한의 내장 원칙)
3. 에이전트의 일반 지식 (출처 표기 불가 시 명시)

## 디자인 시스템 레퍼런스

| 시스템 | 프로젝트 docs/design/ |
|--------|----------------------|
| Apple HIG | `systems/apple-hig.md` |
| Material Design | `systems/material-design.md` |
| 오픈소스 시스템 | `systems/open-source-systems.md` |
```

- [ ] **Step 3: 커밋**

```bash
git add design-kit/skills/design-guide/
git commit -m "feat(design-kit): design-guide 스킬 — 실시간 디자인 가이드"
```

---

### Task 6: design-audit 스킬 작성

**Files:**
- Create: `design-kit/skills/design-audit/SKILL.md`
- Create: `design-kit/skills/design-audit/references/audit-criteria.md`
- Create: `design-kit/skills/design-audit/templates/audit-report.md`

- [ ] **Step 1: SKILL.md 작성**

`design-kit/skills/design-audit/SKILL.md`:
```markdown
---
name: design-audit
description: >
  완성된 UI를 디자인 원칙 기준으로 체계적으로 감사한다.
  카테고리별 PASS/FAIL 판정과 근거를 포함한 리포트를 생성한다.
  design-reviewer 에이전트를 Agent 도구로 호출하여 독립 평가한다.
  "디자인 감사", "UI 검수", "design audit", "디자인 품질 검사" 같은 요청 시 트리거.
  코드 품질/아키텍처 검사에는 트리거하지 않는다 — 각 toolkit의 audit 사용.
argument-hint: "<target-path>"
user-invocable: true
---

# Gotchas

1. **코드 품질 평가 금지** — 아키텍처, 성능, 코드 스타일을 평가하지 마라. 디자인 원칙 준수 여부만 판정한다.
2. **토큰 미사용 FAIL 남발 금지** — 디자인 토큰이 없는 프로젝트에서 "토큰 미사용"으로 FAIL을 남발하지 마라. 토큰 체계가 없으면 design-system 스킬 사용을 권장하는 NOTE로 남겨라.
3. **접근성 생략 금지** — 시각적으로 문제없어 보여도 contrast ratio(WCAG AA 4.5:1), 터치 타겟 크기(최소 44×44pt)는 반드시 검사한다.

# Process

## Step 1: 대상 범위 결정

사용자가 지정한 경로를 기준으로 감사 대상을 결정한다:
- 파일 경로 → 해당 파일만
- 디렉토리 경로 → 하위 UI 관련 파일 전체
- 미지정 → 최근 변경된 UI 파일 (git diff 기준)

## Step 2: design-reviewer 에이전트 호출

Agent 도구를 사용하여 design-reviewer 서브에이전트를 생성한다:

```
Agent 도구 호출:
- subagent_type: design-reviewer
- prompt: "다음 파일을 디자인 원칙 기준으로 평가하라: [대상 파일 목록]"
```

에이전트가 읽기 전용으로 분석 후 카테고리별 PASS/FAIL 결과를 반환한다.

## Step 3: 리포트 포맷팅

에이전트 결과를 templates/audit-report.md 포맷으로 정리한다.

## Step 4: 최종 판정

- 모든 카테고리 PASS → **APPROVE**
- 1개 이상 FAIL → **REJECT** + 개선 사항 목록

REJECT 시 각 FAIL 항목에 대해:
- 파일:라인 위치
- 위반한 원칙 (출처 포함)
- 구체적 개선 방향 (스택 무관 수준)

# References

- `references/audit-criteria.md` — 카테고리별 감사 기준 상세
- `templates/audit-report.md` — 리포트 출력 포맷
```

- [ ] **Step 2: audit-criteria.md 작성**

`design-kit/skills/design-audit/references/audit-criteria.md`:
```markdown
# 디자인 감사 기준

design-reviewer 에이전트가 참조하는 카테고리별 체크리스트.

## Typography

| 기준 | PASS 조건 | 출처 |
|------|-----------|------|
| 스케일 일관성 | 정의된 타이포 스케일 외 임의 크기 미사용 | Material Design 3 Typography |
| 행간 비율 | line-height가 font-size의 1.2~1.6배 | WCAG 1.4.12 |
| 최소 크기 | 본문 텍스트 14px(모바일) / 16px(웹) 이상 | Apple HIG Typography |

## Color

| 기준 | PASS 조건 | 출처 |
|------|-----------|------|
| 대비 비율 | 텍스트/배경 대비 WCAG AA (4.5:1 이상) | WCAG 2.1 SC 1.4.3 |
| 시맨틱 사용 | 하드코딩된 컬러값 대신 시맨틱 토큰 사용 | Material Design 3 Color |
| 다크 모드 | 다크 모드에서도 대비 비율 유지 | Apple HIG Dark Mode |

## Spacing

| 기준 | PASS 조건 | 출처 |
|------|-----------|------|
| 스케일 일관성 | 정의된 스페이싱 스케일 외 임의 값 미사용 | EightShapes Space in DS |
| 터치 타겟 | 인터랙티브 요소 최소 44×44pt | Apple HIG Accessibility |
| 여백 일관성 | 같은 레벨의 요소는 동일 간격 | Gestalt 근접성 원칙 |

## Accessibility

| 기준 | PASS 조건 | 출처 |
|------|-----------|------|
| 색상 대비 AA | 일반 텍스트 4.5:1, 대형 텍스트 3:1 | WCAG 2.1 SC 1.4.3 |
| 터치 타겟 | 최소 44×44pt | Apple HIG, WCAG 2.5.8 |
| 포커스 표시 | 인터랙티브 요소에 포커스 인디케이터 존재 | WCAG 2.4.7 |

## Interaction

| 기준 | PASS 조건 | 출처 |
|------|-----------|------|
| 피드백 존재 | 사용자 액션에 시각적 피드백 존재 | NNGroup Feedback |
| 로딩 상태 | 비동기 작업에 로딩 인디케이터 존재 | NNGroup Response Times |
| 에러 표시 | 에러 상태가 명확히 표시됨 | NNGroup Error Messages |

## Motion

| 기준 | PASS 조건 | 출처 |
|------|-----------|------|
| 목적성 | 장식용 애니메이션이 아닌 기능적 목적 존재 | Material Design 3 Motion |
| 듀레이션 | 200~500ms 범위 (너무 빠르거나 느리지 않음) | Apple HIG Motion |
| reduced-motion | prefers-reduced-motion 대응 | WCAG 2.3.3 |
```

- [ ] **Step 3: audit-report.md 템플릿 작성**

`design-kit/skills/design-audit/templates/audit-report.md`:
```markdown
# 디자인 감사 리포트

> 일시: {{date}}
> 대상: {{target-path}}
> 판정: **{{verdict}}**

## 요약

| 카테고리 | 판정 | 항목 수 |
|----------|------|---------|
| Typography | {{pass/fail}} | {{count}} |
| Color | {{pass/fail}} | {{count}} |
| Spacing | {{pass/fail}} | {{count}} |
| Accessibility | {{pass/fail}} | {{count}} |
| Interaction | {{pass/fail}} | {{count}} |
| Motion | {{pass/fail}} | {{count}} |

## FAIL 상세

### [카테고리] 항목 제목

- **위치:** `파일경로:라인`
- **위반 원칙:** [원칙명]
- **출처:** [출처 URL/문서명]
- **현재:** [현재 상태]
- **권장:** [개선 방향]

## NOTE

{{토큰 미사용 등 감사 범위 외 참고 사항}}
```

- [ ] **Step 4: 커밋**

```bash
git add design-kit/skills/design-audit/
git commit -m "feat(design-kit): design-audit 스킬 — 디자인 품질 감사"
```

---

### Task 7: design-reviewer 에이전트 작성

**Files:**
- Create: `design-kit/agents/design-reviewer.md`

- [ ] **Step 1: design-reviewer.md 작성**

`design-kit/agents/design-reviewer.md`:
```markdown
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

# Design Reviewer

UI 코드를 디자인 원칙 기준으로 평가하는 읽기 전용 에이전트.
코드를 수정하지 않는다. 결함을 찾는 것이 유일한 역할이다.

## 핵심 규칙

1. **디자인 원칙만 판정** — 코드 품질, 아키텍처, 성능은 평가 대상이 아니다.
2. **이진 판정** — PASS 또는 FAIL만 존재한다. "부분적 준수", "거의 통과" 없음.
3. **근거 필수** — 모든 FAIL에 `파일:라인` + 출처(원칙명, URL)를 명시한다.
4. **칭찬 금지** — "잘 되어 있다", "깔끔하다" 같은 긍정적 평가는 하지 않는다.
5. **1 FAIL = REJECT** — 하나라도 FAIL이면 전체 판정은 REJECT.

## 평가 카테고리

6개 카테고리를 순서대로 평가한다:

### 1. Typography
- 타이포 스케일 일관성
- 행간 비율 (1.2~1.6배)
- 최소 폰트 크기

### 2. Color
- 대비 비율 (WCAG AA 4.5:1)
- 시맨틱 컬러 사용
- 다크 모드 대응

### 3. Spacing
- 스페이싱 스케일 일관성
- 터치 타겟 크기 (44×44pt)
- 여백 일관성

### 4. Accessibility
- 색상 대비 AA
- 터치 타겟
- 포커스 인디케이터

### 5. Interaction
- 액션 피드백 존재
- 로딩 상태
- 에러 표시

### 6. Motion
- 목적성
- 듀레이션 범위 (200~500ms)
- reduced-motion 대응

## 판정 불가 항목

코드만으로 판정할 수 없는 항목은 `[미검증]` 태그를 붙인다:
- 실제 렌더링 결과가 필요한 시각적 검증
- 런타임에서만 확인 가능한 인터랙션

`[미검증]`은 PASS가 아니다 — 수동 확인이 필요함을 명시한다.

## 편향 감지 (Red Flags)

다음 패턴이 나타나면 자기 판정을 재검토하라:
- "이 정도면 괜찮다" → 기준에 미달하면 FAIL이다
- "의도적인 디자인 선택일 수 있다" → 코드에 근거가 없으면 FAIL이다
- "사소한 문제다" → 기준 위반은 크기와 무관하게 FAIL이다

## 출력 형식

```
## [카테고리명]

### PASS: [항목명]
- 근거: [확인한 내용]

### FAIL: [항목명]
- 위치: `파일:라인`
- 위반 원칙: [원칙명]
- 출처: [URL/문서명]
- 현재: [현재 상태]
- 권장: [개선 방향]

### [미검증]: [항목명]
- 사유: [판정 불가 이유]
```

## 최종 판정

```
---
**판정: {{APPROVE|REJECT}}**
PASS: {{n}}개 / FAIL: {{n}}개 / 미검증: {{n}}개
---
```
```

- [ ] **Step 2: 커밋**

```bash
git add design-kit/agents/
git commit -m "feat(design-kit): design-reviewer 에이전트 — 디자인 독립 평가"
```

---

### Task 8: hooks, scripts, evals 작성

**Files:**
- Create: `design-kit/hooks/hooks.json`
- Create: `design-kit/scripts/env-check.sh`
- Create: `design-kit/evals/evals.json`

- [ ] **Step 1: hooks.json 작성**

`design-kit/hooks/hooks.json`:
```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/env-check.sh",
            "timeout": 10,
            "statusMessage": "디자인 환경 확인 중..."
          }
        ]
      }
    ]
  }
}
```

- [ ] **Step 2: env-check.sh 작성**

`design-kit/scripts/env-check.sh`:
```bash
#!/usr/bin/env bash
set -euo pipefail

echo "=== Environment Check ==="

# OS 감지
case "$(uname -s 2>/dev/null || echo Windows)" in
  Darwin*)  OS="macOS" ;;
  Linux*)   OS="linux" ;;
  MINGW*|MSYS*|CYGWIN*) OS="windows" ;;
  *)        OS="windows" ;;
esac
echo "OS: $OS"

echo ""
echo "✅ All checks passed"
```

- [ ] **Step 3: evals.json 작성**

`design-kit/evals/evals.json`:
```json
{
  "skill_name": "design-kit",
  "evals": [
    {
      "id": 1,
      "skill": "design-system",
      "prompt": "이 프로젝트에 디자인 토큰 세팅해줘",
      "expected_output": "프로젝트 디자인 시스템 유무 감지 후 토큰 체계 제안 또는 기존 시스템 분석",
      "assertions": [
        {"text": "기존 디자인 시스템 유무를 먼저 감지한다", "type": "behavior"},
        {"text": "컬러, 타이포, 스페이싱, 라디우스 카테고리를 포함한다", "type": "output"},
        {"text": "시맨틱 네이밍을 사용한다 (blue-500 같은 값 기반 이름 미사용)", "type": "output"},
        {"text": "스택별 코드를 직접 생성하지 않는다", "type": "behavior"}
      ]
    },
    {
      "id": 2,
      "skill": "design-system",
      "prompt": "기존 디자인 시스템이 있는 프로젝트에서 토큰 분석해줘",
      "expected_output": "기존 토큰을 리서치 기준과 비교하여 개선점 리포트",
      "assertions": [
        {"text": "기존 토큰 구조를 분석한다", "type": "behavior"},
        {"text": "누락된 카테고리를 식별한다", "type": "output"},
        {"text": "다크 모드 대응 여부를 확인한다", "type": "output"}
      ]
    },
    {
      "id": 3,
      "skill": "design-guide",
      "prompt": "이 레이아웃 간격이 괜찮은지 봐줘",
      "expected_output": "스페이싱 관련 디자인 원칙 기반 피드백",
      "assertions": [
        {"text": "출처가 있는 원칙을 근거로 제시한다", "type": "output"},
        {"text": "스택별 구현 코드를 직접 제시하지 않는다", "type": "behavior"},
        {"text": "관련 카테고리(spacing)만 집중하여 답한다", "type": "behavior"}
      ]
    },
    {
      "id": 4,
      "skill": "design-guide",
      "prompt": "이 버튼 색상이 접근성 기준에 맞는지 확인해줘",
      "expected_output": "WCAG 대비 비율 기준 피드백",
      "assertions": [
        {"text": "WCAG AA 기준(4.5:1)을 언급한다", "type": "output"},
        {"text": "주관적 피드백('보기 좋다') 없이 원칙만 제시한다", "type": "behavior"}
      ]
    },
    {
      "id": 5,
      "skill": "design-audit",
      "prompt": "이 화면 디자인 감사해줘",
      "expected_output": "6개 카테고리 PASS/FAIL 판정 리포트",
      "assertions": [
        {"text": "design-reviewer 에이전트를 Agent 도구로 호출한다", "type": "behavior"},
        {"text": "typography, color, spacing, accessibility, interaction, motion 카테고리를 포함한다", "type": "output"},
        {"text": "FAIL 항목에 파일:라인 위치를 명시한다", "type": "output"},
        {"text": "코드 품질/아키텍처는 평가하지 않는다", "type": "behavior"}
      ]
    },
    {
      "id": 6,
      "skill": "design-audit",
      "prompt": "디자인 토큰이 없는 프로젝트에서 design audit 실행",
      "expected_output": "토큰 미사용을 FAIL이 아닌 NOTE로 처리",
      "assertions": [
        {"text": "토큰 미사용을 FAIL로 판정하지 않는다", "type": "behavior"},
        {"text": "design-system 스킬 사용을 NOTE로 권장한다", "type": "output"}
      ]
    }
  ]
}
```

- [ ] **Step 4: 커밋**

```bash
git add design-kit/hooks/ design-kit/scripts/ design-kit/evals/
git commit -m "feat(design-kit): hooks, scripts, evals 추가"
```

---

### Task 9: README.md + marketplace 등록

**Files:**
- Create: `design-kit/README.md`
- Modify: `.claude-plugin/marketplace.json`
- Modify: `CLAUDE.md`

- [ ] **Step 1: README.md 작성**

`design-kit/README.md`:
```markdown
# design-kit

스택 무관 UI/UX 디자인 플러그인. 디자인 시스템 세팅, 실시간 가이드, 디자인 감사를 제공한다.

## 스킬

| 스킬 | 아키타입 | 설명 |
|------|----------|------|
| `/design-system` | Code Scaffolding | 프로젝트에 디자인 토큰 체계 세팅 |
| `/design-guide` | Library Reference | 개발 중 디자인 원칙 기반 실시간 가이드 |
| `/design-audit` | Product Verification | 완성된 UI를 디자인 원칙 기준으로 감사 |

## 에이전트

| 에이전트 | 모델 | 설명 |
|----------|------|------|
| `design-reviewer` | sonnet | design-audit이 호출하는 독립 디자인 평가 에이전트 |

## 사용 흐름

```
1. /design-system     → 프로젝트 디자인 토큰 세팅
2. (개발 중) /design-guide  → 실시간 디자인 조언
3. (개발 후) /design-audit  → 디자인 품질 감사
```

## 원칙

- **스택 무관** — 디자인 원칙만 다루고, 구체적 코드 생성은 각 toolkit에 위임
- **플러그인 간 의존성 없음** — 다른 플러그인과 독립적으로 동작
- **출처 기반** — 모든 가이드/판정에 출처 명시 (Apple HIG, Material Design, WCAG 등)

## 설치

```bash
claude plugin add github:joo6077/claude-plugins/design-kit
```
```

- [ ] **Step 2: marketplace.json에 design-kit 추가**

`.claude-plugin/marketplace.json`의 `plugins` 배열 마지막에 추가:

```json
{
  "name": "design-kit",
  "source": "./design-kit",
  "description": "[v0.1.0 · 2026-03-30] 스택 무관 UI/UX 디자인 가이드 + 감사 플러그인"
}
```

- [ ] **Step 3: CLAUDE.md 업데이트**

`CLAUDE.md`의 Repository Overview 섹션에 design-kit 설명 추가:

```markdown
- **design-kit** — 스택 무관 UI/UX 디자인 플러그인 (디자인 시스템 세팅 + 실시간 가이드 + 감사)
```

- [ ] **Step 4: 커밋**

```bash
git add design-kit/README.md .claude-plugin/marketplace.json CLAUDE.md
git commit -m "feat(design-kit): README + marketplace 등록 + CLAUDE.md 업데이트"
```

---

### Task 10: 개발용 스킬 배치 (design-research, design-kaizen)

**Files:**
- Create: `.claude/skills/design-research/SKILL.md`
- Create: `.claude/skills/design-kaizen/SKILL.md`

- [ ] **Step 1: design-research 스킬 작성**

`.claude/skills/design-research/SKILL.md`:
```markdown
---
name: design-research
description: >
  디자인 레퍼런스 소스를 크롤링/분석하여 docs/design/ 문서를 갱신한다.
  이 레포 개발용 스킬이며, design-kit 플러그인에 포함되지 않는다.
  "디자인 리서치", "레퍼런스 크롤링", "design research",
  "디자인 문서 갱신" 같은 요청 시 트리거.
argument-hint: "[category or source]"
user-invocable: true
---

# Gotchas

1. **출처 없는 원칙 금지** — 모든 원칙에 인라인 출처 `> **출처:** [이름](URL)`를 반드시 남겨라. 출처가 없는 내용은 작성하지 않는다.
2. **frontmatter 갱신 필수** — 문서 내용을 수정하면 `last_updated`와 `version`을 반드시 업데이트하라.
3. **기존 내용 보존** — 이전 리서치 내용을 덮어쓰지 마라. 업데이트/보완만 한다. 삭제가 필요하면 근거를 커밋 메시지에 명시하라.

# Process

## Step 1: 대상 카테고리 결정

사용자가 카테고리를 지정하면 해당 문서만, 미지정이면 전체 docs/design/ 순회.

## Step 2: 소스 크롤링

카테고리별 관련 소스를 WebSearch + WebFetch로 조사한다:

| 카테고리 | 우선 소스 |
|----------|-----------|
| foundations/ | Apple HIG, Material Design 3, Fluent Design |
| interaction/ | NNGroup, Baymard Institute |
| accessibility/ | WCAG 2.1/2.2, Apple HIG Accessibility |
| systems/ | 각 디자인 시스템 공식 문서 |

추가 소스: Laws of UX, Dribbble/Behance 수상작 분석, Radix/Shadcn/Tailwind 문서.

## Step 3: 분석 및 정리

크롤링 결과를 해당 docs/design/ 문서에 반영:
- 각 원칙에 `> **출처:**` 인라인 태그
- 섹션 구조는 기존 스켈레톤을 따름
- 수치/기준값은 명확하게 (예: "4.5:1", "44pt", "200~500ms")

## Step 4: frontmatter 업데이트

수정한 문서의 frontmatter에서:
- `last_updated` → 오늘 날짜
- `version` → patch bump (내용 추가) 또는 minor bump (구조 변경)

## Step 5: 커밋

```bash
git add docs/design/
git commit -m "docs(design): [카테고리] 리서치 갱신 — [소스 요약]"
```

# References

- 크롤링 대상 소스 목록은 Process Step 2 테이블 참조
- 기존 docs/design/ 문서의 섹션 구조를 따를 것
```

- [ ] **Step 2: design-kaizen 스킬 작성**

`.claude/skills/design-kaizen/SKILL.md`:
```markdown
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
```

- [ ] **Step 3: 커밋**

```bash
git add .claude/skills/design-research/ .claude/skills/design-kaizen/
git commit -m "feat: design-research, design-kaizen 개발용 스킬 추가"
```

---

## Self-Review 완료

**Spec coverage:** 스펙 9개 섹션 모두 태스크에 매핑됨.
- 섹션 1(개요) + 2(원칙) → 전체 태스크에 반영
- 섹션 3(구조) → Task 3
- 섹션 4(스킬) → Task 4, 5, 6
- 섹션 5(에이전트) → Task 7
- 섹션 6(docs/) → Task 1, 2
- 섹션 7(개발용 스킬) → Task 10
- 섹션 8(리서치 소스) → Task 10 design-research에 포함
- 섹션 9(marketplace) → Task 9

**Placeholder scan:** TBD/TODO 없음. 모든 코드 블록에 실제 내용 포함.

**Type consistency:** 파일명, 카테고리명, frontmatter 필드명이 전체 태스크에서 일관됨.
