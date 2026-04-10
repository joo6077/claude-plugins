# react-kit Plugin — Phase 1 Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create the `react-kit/` plugin directory skeleton with `plugin.json`, README, references, templates, evals, and register it in the repo's marketplace. This produces a **testable plugin skeleton** that loads correctly but has no skills yet — skills are delivered in Phase 2~9 (separate future plans).

**Architecture:** Follow the existing `flutter-toolkit/`, `rust-kit/`, `harness/` plugin layout exactly. Mirror their `plugin.json` shape, README AUTO marker conventions, and directory structure. Source all content from the already-approved design docs in `docs/react/kit-design/`.

**Tech Stack:** pnpm, Claude Code plugin manifest (JSON), Markdown, YAML, TypeScript config templates, bash.

**Scope boundary:**
- ✅ This plan: plugin directory + metadata + reference docs + templates + marketplace registration + evals scaffolding
- ❌ Not this plan: SKILL.md files (Phases 2~8, one plan per skill group), agent .md files (Phase 7, 8, 9), release tagging (Phase 10)

**Spec reference:** `docs/superpowers/specs/2026-04-10-react-kit-design.md` §2, §3, §7 → `docs/react/kit-design/final-integration.md`

---

## File Structure

Files created in this plan (all paths relative to repo root):

```
react-kit/
├── .claude-plugin/
│   └── plugin.json                        # NEW — plugin metadata
├── README.md                              # NEW — overview + AUTO markers
├── references/
│   ├── project-detection.md               # NEW — project environment detection rules
│   ├── clean-arch-layout.md               # NEW — layer placement rules
│   ├── result-patterns.md                 # NEW — neverthrow Result usage
│   ├── wasm-catalog.md                    # NEW — link/copy of docs/react/wasm-catalog.md
│   └── style-guide.md                     # NEW — strict TS + ESLint + Prettier
├── templates/
│   ├── tsconfig.template.json             # NEW
│   ├── eslint.config.template.js          # NEW
│   ├── vite.config.template.ts            # NEW
│   ├── tailwind.config.template.ts        # NEW
│   ├── package.json.template              # NEW
│   ├── pnpm-workspace.yaml.template       # NEW
│   ├── Cargo.toml.template                # NEW
│   ├── lingui.config.ts.template          # NEW
│   └── harness-project.yaml.template      # NEW — sourced from final-integration.md §1.1
├── skills/                                # NEW (empty; dirs will be added per skill in later phases)
│   └── .gitkeep
├── agents/                                # NEW (empty; agent files added in later phases)
│   └── .gitkeep
├── evals/
│   ├── evals.json                         # NEW — empty test array (skills populate later)
│   └── test-fixtures/
│       ├── empty-project/.gitkeep         # NEW
│       ├── clean-arch-project/.gitkeep    # NEW
│       ├── wasm-project/.gitkeep          # NEW
│       ├── tauri-project/.gitkeep         # NEW
│       └── audit-target-project/.gitkeep  # NEW
└── scripts/
    └── project-detect.sh                  # NEW — bash helper for project detection

Modify:
.claude-plugin/marketplace.json            # ADD react-kit entry after rust-kit
```

No existing files are modified except `.claude-plugin/marketplace.json` (1 add-only edit).

---

## Conventions

- **Commit cadence**: one commit per task (17 commits total). Each commit message follows `feat(react-kit): <topic>` or `docs(react-kit): <topic>` format.
- **Verification after every task**: run `python3 scripts/sync-docs.py --check-only react-kit` (allow it to fail gracefully — the skill list will be empty in Phase 1).
- **Source content from existing docs**: all content in references/, templates/, and README should be extracted from the approved `docs/react/kit-design/*.md` and `docs/react/wasm-catalog.md` — do not rewrite content, copy/link.
- **No SKILL.md yet**: skills/ gets a `.gitkeep` only. Attempting to add SKILL.md in this phase would bleed scope.

---

### Task 1: Create `react-kit/` root directory and `.claude-plugin/plugin.json`

**Files:**
- Create: `react-kit/.claude-plugin/plugin.json`

- [ ] **Step 1.1: Create the plugin root directory**

Run:
```bash
mkdir -p react-kit/.claude-plugin
```

- [ ] **Step 1.2: Write plugin.json**

Create `react-kit/.claude-plugin/plugin.json` with this exact content:

```json
{
  "name": "react-kit",
  "description": "React + Vite + Tauri 2 + Rust WASM 전용 개발 워크플로우 플러그인 — 21종 스킬 + 3 에이전트, 라이브러리 0개 애니메이션, Clean Architecture, Strict TypeScript 강제",
  "version": "0.1.0",
  "author": {
    "name": "Jackson Kim"
  },
  "repository": "https://github.com/joo6077/claude-plugins",
  "license": "MIT",
  "keywords": [
    "react",
    "vite",
    "tauri",
    "wasm",
    "rust",
    "typescript",
    "tailwind",
    "shadcn",
    "zustand",
    "tanstack-query",
    "clean-architecture",
    "pure-animation",
    "no-library"
  ]
}
```

- [ ] **Step 1.3: Verify JSON is valid**

Run:
```bash
python3 -c "import json; json.load(open('react-kit/.claude-plugin/plugin.json')); print('OK')"
```

Expected: `OK`

- [ ] **Step 1.4: Commit**

```bash
git add react-kit/.claude-plugin/plugin.json
git commit -m "feat(react-kit): add plugin.json scaffold v0.1.0"
```

---

### Task 2: Create `react-kit/README.md`

**Files:**
- Create: `react-kit/README.md`

Content is sourced from `docs/react/kit-design/final-integration.md` §4 (lines 323–449). Use the full README block from that section verbatim.

- [ ] **Step 2.1: Extract README content**

Run:
```bash
sed -n '/^```markdown$/,/^```$/p' docs/react/kit-design/final-integration.md | sed '1d;$d' | head -130
```

Inspect the output — it should be the README block starting with `# react-kit`.

- [ ] **Step 2.2: Write `react-kit/README.md`**

Copy the README markdown block from `docs/react/kit-design/final-integration.md` (lines 325–449) into `react-kit/README.md`. The file begins with `# react-kit` and includes the `<!-- AUTO:skills -->` and `<!-- AUTO:agents -->` markers.

**Important:** do not modify the content. The AUTO markers will be populated by `scripts/sync-docs.py` after skills are added in later phases.

- [ ] **Step 2.3: Verify AUTO markers present**

Run:
```bash
grep -c "AUTO:" react-kit/README.md
```

Expected: `4` (opening + closing for skills + opening + closing for agents)

- [ ] **Step 2.4: Commit**

```bash
git add react-kit/README.md
git commit -m "docs(react-kit): add initial README with AUTO markers"
```

---

### Task 3: Create `references/project-detection.md`

**Files:**
- Create: `react-kit/references/project-detection.md`

- [ ] **Step 3.1: Create the references directory**

Run:
```bash
mkdir -p react-kit/references
```

- [ ] **Step 3.2: Write project-detection.md**

Create `react-kit/references/project-detection.md` with the following content:

```markdown
# Project Detection Rules

All react-kit skills read this file to determine the current project environment before generating code. Mirrors the `flutter-toolkit/references/project-detection.md` pattern.

## Detection Order

1. **Node version** — read `.nvmrc` first, fallback to `package.json` `engines.node`
2. **pnpm version** — read `packageManager` field in `package.json`
3. **React version** — read `dependencies.react` in `package.json`
4. **Vite install** — check `devDependencies.vite` + `vite.config.ts` exists
5. **Tailwind version** — read `devDependencies.tailwindcss`. v4 vs v3 has different install paths
6. **shadcn initialization** — check `components.json` exists at project root
7. **TanStack Router plugin** — check `devDependencies.@tanstack/router-plugin`
8. **Cargo workspace** — check root `Cargo.toml` with `[workspace]` table
9. **Tauri install** — check `src-tauri/` directory exists and has `tauri.conf.json`
10. **Lingui config** — check `lingui.config.ts` exists
11. **strict TypeScript** — read `tsconfig.json` for `strict: true` and related options

## Detection Outputs

A detection result is a JSON object shaped like:

\`\`\`json
{
  "node": "22.14.1",
  "pnpm": "9.15.0",
  "react": "19.0.0",
  "vite": "6.0.1",
  "tailwind": "4.0.0",
  "shadcn": true,
  "tanstackRouter": true,
  "cargoWorkspace": true,
  "tauri": true,
  "lingui": true,
  "strictTS": true
}
\`\`\`

## Skill Behavior Based on Detection

- Tailwind v3 detected → `/react-init` refuses, suggests upgrade. Existing skills use v3 syntax
- shadcn missing → `/react-widget` suggests `pnpm dlx shadcn@latest init --template vite` first
- Cargo workspace missing → `/react-wasm` refuses, suggests `/react-init --with-wasm` first
- Tauri missing → `/react-tauri` refuses, suggests `/react-init --with-tauri` first
- strict TS missing → all generation skills inject the strict compilerOptions

## Caching

Detection result is computed once per skill invocation and cached. Long-running sessions may re-detect on demand.

## Related Documents

- `docs/react/kit-design/g1-scaffolding.md` §1 — `/react-init` scaffolding details
- `docs/react/kit-design/g6-build-audit.md` §1.3 — `/react-run` subcommand enabling based on detection
```

- [ ] **Step 3.3: Commit**

```bash
git add react-kit/references/project-detection.md
git commit -m "docs(react-kit): add project-detection reference"
```

---

### Task 4: Create `references/clean-arch-layout.md`

**Files:**
- Create: `react-kit/references/clean-arch-layout.md`

- [ ] **Step 4.1: Write clean-arch-layout.md**

Create `react-kit/references/clean-arch-layout.md`:

```markdown
# Clean Architecture Layer Layout

react-kit 의 모든 스킬이 공유하는 레이어 배치 + 의존성 방향 규칙.

## 레이어 정의

| 레이어 | 경로 | 의존성 방향 |
|--------|------|------------|
| **domain** | `src/domain/` | 외부 의존성 **0개**. 오직 순수 TS + Zod |
| **data** | `src/data/` | `domain/` 만 알고, `presentation/`, `infrastructure/` 모름 |
| **presentation** | `src/presentation/` | `domain/`, `data/repositories/`, `shared/`, `infrastructure/` 알 수 있음 |
| **infrastructure** | `src/infrastructure/` | 브라우저/Tauri/OS API 래퍼. `domain/` 만 참조 가능 |

## 하위 디렉토리

### domain
- `entities/` — Zod 스키마 + `z.infer` 파생 타입
- `usecases/` — 함수 시그니처 (`Promise<Result<T, Failure>>`)
- `failures/` — `<Feature>Failure` discriminated union
- `types/` — 공유 타입 (WASM 경계 포함)

### data
- `datasources/remote/` — fetch + Zod parse (boundary 검증)
- `datasources/local/` — localStorage, IndexedDB
- `datasources/wasm/` — Comlink Worker 래퍼 + WASM 바인딩
- `models/` — DTO 스키마 + 도메인 변환 함수
- `repositories/` — UseCase 구현 (의존성 주입)

### presentation
- `features/<feature>/` — components/, hooks/, store.ts, screens/, index.ts
- `shared/components/ui/` — shadcn 원본 (수정 금지)
- `shared/components/` — 공용 위젯
- `shared/components/skeletons/` — 공용 skeleton
- `shared/hooks/` — useDrag, useDrop, useSortable, 기타 공용 훅
- `shared/stores/` — cross-feature Zustand 스토어 (drag-store 등)
- `shared/lib/` — cn 유틸, display-failure, view-transition 래퍼
- `routes/` — TanStack Router 파일 기반 라우트
- `styles/` — globals.css (@theme @keyframes)

### infrastructure
- `tauri/` — `@tauri-apps/*` 유일한 import 위치, `isTauri()` 가드 래퍼
- `storage/` — localStorage 어댑터
- `http/` — fetch 클라이언트 (Zod 검증 + Result 반환)
- `i18n/` — Lingui setup + locale catalog

## 금지 import 방향

- ❌ `domain/` 이 `data/`, `presentation/`, `infrastructure/` 중 아무거나 import
- ❌ `data/` 가 `presentation/` 또는 `infrastructure/tauri/` import
- ❌ `presentation/features/a` 가 `presentation/features/b` 직접 import
- ❌ `presentation/` 이나 `data/` 에서 `@tauri-apps/*` 직접 import (`infrastructure/tauri/` 경유 필수)
- ❌ 모든 상대 경로 (`'../../../'`) — absolute `@/` import 만 허용
- ❌ `export default` 컴포넌트 — named export 로 통일

## `/react-audit` 감사 규칙

이 레퍼런스의 금지 규칙은 G6 `/react-audit` 의 Architecture 카테고리 grep 패턴으로 번역되어 빌드 게이트급 실패로 강제된다. 상세 패턴은 `docs/react/kit-design/g6-build-audit.md` §4.5 Architecture 섹션 참조.

## 관련 문서

- `docs/react/kit-design/g1-scaffolding.md` — 스캐폴딩 시 디렉토리 생성
- `docs/react/kit-design/g2-state-data.md` — 데이터 레이어 패턴
- `docs/react/kit-design/g6-build-audit.md` — 경계 위반 감사
```

- [ ] **Step 4.2: Commit**

```bash
git add react-kit/references/clean-arch-layout.md
git commit -m "docs(react-kit): add clean-arch-layout reference"
```

---

### Task 5: Create `references/result-patterns.md`

**Files:**
- Create: `react-kit/references/result-patterns.md`

- [ ] **Step 5.1: Write result-patterns.md**

Create `react-kit/references/result-patterns.md`:

````markdown
# Result Patterns (neverthrow)

react-kit 의 모든 에러 경계는 `neverthrow` 의 `Result<T, E>` 를 사용. `throw` 금지.

## 기본 사용

```ts
import { ok, err, Result, ResultAsync } from 'neverthrow'

// 동기
function parse(raw: unknown): Result<User, UserFailure> {
  const parsed = UserSchema.safeParse(raw)
  if (!parsed.success) return err({ kind: 'user/validation-failed', issues: parsed.error.issues.map(i => i.message) })
  return ok(parsed.data)
}

// 비동기
function fetchUser(id: string): ResultAsync<User, UserFailure> {
  return ResultAsync.fromPromise(
    fetch(`/users/${id}`).then(r => r.json()),
    (e) => ({ kind: 'user/network-error', cause: String(e) })
  ).andThen(parse)
}
```

## Failure discriminated union

```ts
export type UserFailure =
  | { kind: 'user/not-found'; userId: string }
  | { kind: 'user/unauthorized' }
  | { kind: 'user/network-error'; cause: string }
  | { kind: 'user/validation-failed'; issues: string[] }
```

`kind` 필드로 switch/match 분기. 모든 케이스를 다뤘는지 TypeScript `never` 타입 exhaustiveness 검증.

## 레이어별 사용 규칙

| 레이어 | 사용 |
|--------|------|
| domain/usecases | **시그니처** `Promise<Result<T, Failure>>` 로 선언만 |
| data/datasources/remote | `ResultAsync.fromPromise(fetch(...), e => Failure)` 로 경계 변환 |
| data/repositories | datasource 호출 + Zod parse → Result 체인 |
| presentation/hooks | TanStack Query `queryFn` 안에서만 `throw result.error` (TanStack 이 error 로 포획) |
| presentation/components | `result.isErr()` / `isOk()` 로 분기, throw 금지 |

## 안티패턴

- ❌ `try/catch` 로 Failure 감추기 — 항상 Result 로 변환
- ❌ `throw new Error(JSON.stringify(failure))` — 타입 정보 손실
- ❌ `any` 로 에러 타입 우회
- ❌ domain 레이어에서 throw

## 관련 문서

- `docs/react/kit-design/g2-state-data.md` §2 `/react-api` — Clean Arch 4계층 + Result 체인
- `docs/react/kit-design/g4-quality.md` §2 `/react-error` — Severity 매핑 + UI 표시
````

- [ ] **Step 5.2: Commit**

```bash
git add react-kit/references/result-patterns.md
git commit -m "docs(react-kit): add result-patterns reference"
```

---

### Task 6: Create `references/wasm-catalog.md` (link to docs/react/wasm-catalog.md)

**Files:**
- Create: `react-kit/references/wasm-catalog.md`

- [ ] **Step 6.1: Create as a pointer (not symlink — portability)**

Create `react-kit/references/wasm-catalog.md`:

```markdown
# WASM Decision Catalog — Pointer

The authoritative WASM decision catalog lives at the repo-level development doc:

**`docs/react/wasm-catalog.md`** (521 lines)

Contents:
- §1 WASM 권장 카테고리 9 항목 (이미지, 압축, ML, SQL, 파서, 수치, 집계, 암호화)
- §2 WASM 비권장 카테고리 10 항목 (UI, 폼, JSON, 문자열, Web Crypto small, 고빈도 콜백, tiny 함수, 애니메이션, 네트워크, event bus)
- §3 Boundary cost 수치 (JS↔WASM call ~50-100ns, 문자열 마샬링 600-2500ns)
- §4 SIMD + Threads 브라우저 지원 현황
- §5 카탈로그 미스 시 5개 휴리스틱
- §6 5 가지 오해 교정
- §10 Rust 크레이트 매핑
- §11 마이그레이션 체크리스트

## 사용처

- `/react-wasm` 스킬 — 이식 판정의 1차 소스
- `/react-audit` Performance 카테고리 — 안티패턴 검출 기준
- `/react-kaizen` dev 스킬 — 카탈로그 주기 갱신

## 동기화 정책

`react-kit/` 은 배포 대상, `docs/react/` 는 레포 개발용. 두 위치의 sync 는 향후 `/react-kaizen` 스킬이 담당. 초판은 이 포인터 문서만 두고, 스킬 실행 시 런타임에 `docs/react/wasm-catalog.md` 경로를 읽어오는 방식으로 처리 (user repo 가 아니라 claude-plugins 레포 내부 참조).

**주의**: 이 파일은 플러그인 사용자가 아니라 스킬 내부 로직의 참조 포인터다. 플러그인이 설치된 사용자 프로젝트에서는 이 파일이 읽을 일이 없다.
```

- [ ] **Step 6.2: Commit**

```bash
git add react-kit/references/wasm-catalog.md
git commit -m "docs(react-kit): add wasm-catalog pointer reference"
```

---

### Task 7: Create `references/style-guide.md`

**Files:**
- Create: `react-kit/references/style-guide.md`

- [ ] **Step 7.1: Write style-guide.md**

Create `react-kit/references/style-guide.md`:

````markdown
# Style Guide

react-kit 이 생성하는 모든 코드가 준수해야 할 스타일 규칙. `/react-audit` 가 이 규칙을 검증한다.

## Strict TypeScript (`tsconfig.json`)

```jsonc
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "noImplicitOverride": true,
    "verbatimModuleSyntax": true,
    "isolatedModules": true,
    "skipLibCheck": true,
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "Bundler",
    "jsx": "react-jsx",
    "paths": { "@/*": ["./src/*"] }
  }
}
```

## 금지 사항 (ESLint error 레벨)

- `any` 사용 금지 (`@typescript-eslint/no-explicit-any`)
- `as` 타입 단언 제한 (`as const` 만 허용)
- `!` non-null 단언 금지 (`@typescript-eslint/no-non-null-assertion`)
- `export default` 금지 (`no-default-export`)
- `React.FC` 사용 경고 — 대신 `(props: Props) => JSX.Element` 또는 `forwardRef`
- `console.log` production 경고 (`no-console`)
- `throw new` in `src/domain/` — Result 타입 사용
- 상대 경로 `'../../../'` — absolute `@/` 만 허용

## Naming

- **File**: kebab-case (`user-profile-card.tsx`, `use-drag.ts`)
- **Component**: PascalCase (`UserProfileCard`)
- **Hook**: `use` prefix (`useDrag`, `useUser`)
- **Type**: PascalCase (`User`, `UserFailure`)
- **Zod schema**: PascalCase + `Schema` suffix (`UserSchema`)
- **Store**: `use<Name>Store` 형태 (`useAuthStore`)

## Prettier 설정

```json
{
  "semi": false,
  "singleQuote": true,
  "trailingComma": "all",
  "printWidth": 100,
  "tabWidth": 2
}
```

## ESLint flat config 최소 구성

`docs/react/kit-design/g1-scaffolding.md` §1.6 Gotchas 의 "eslint-plugin-react-hooks flat config 수동 와이어링" 경고를 반드시 지킬 것.

## 관련 문서

- `docs/react/kit-design/g1-scaffolding.md` — `/react-init` 이 생성하는 초기 설정
- `docs/react/kit-design/g6-build-audit.md` §4.5 — `/react-audit` 의 Strict TS 카테고리 grep 패턴
````

- [ ] **Step 7.2: Commit**

```bash
git add react-kit/references/style-guide.md
git commit -m "docs(react-kit): add style-guide reference"
```

---

### Task 8: Create `templates/` directory with 9 template files

**Files:**
- Create: `react-kit/templates/tsconfig.template.json`
- Create: `react-kit/templates/eslint.config.template.js`
- Create: `react-kit/templates/vite.config.template.ts`
- Create: `react-kit/templates/tailwind.config.template.ts`
- Create: `react-kit/templates/package.json.template`
- Create: `react-kit/templates/pnpm-workspace.yaml.template`
- Create: `react-kit/templates/Cargo.toml.template`
- Create: `react-kit/templates/lingui.config.ts.template`
- Create: `react-kit/templates/harness-project.yaml.template`

- [ ] **Step 8.1: Create templates directory**

```bash
mkdir -p react-kit/templates
```

- [ ] **Step 8.2: Write `tsconfig.template.json`**

Source: `react-kit/references/style-guide.md` Strict TypeScript section (just written in Task 7). Copy the compilerOptions exactly:

```json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "noImplicitOverride": true,
    "verbatimModuleSyntax": true,
    "isolatedModules": true,
    "skipLibCheck": true,
    "target": "ES2022",
    "lib": ["ES2023", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "moduleResolution": "Bundler",
    "jsx": "react-jsx",
    "paths": { "@/*": ["./src/*"] },
    "allowImportingTsExtensions": false,
    "resolveJsonModule": true,
    "noEmit": true
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
```

- [ ] **Step 8.3: Write `vite.config.template.ts`**

Source: `docs/react/kit-design/g1-scaffolding.md` §1 `/react-init` (lines 133-184) installation commands.

```ts
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react-swc'
import tailwindcss from '@tailwindcss/vite'
import { tanstackRouter } from '@tanstack/router-plugin/vite'
import wasm from 'vite-plugin-wasm'
import topLevelAwait from 'vite-plugin-top-level-await'
import { lingui } from '@lingui/vite-plugin'
import path from 'node:path'

export default defineConfig({
  plugins: [
    tanstackRouter({ target: 'react', autoCodeSplitting: true }),
    react({ plugins: [['@lingui/swc-plugin', {}]] }),
    tailwindcss(),
    wasm(),
    topLevelAwait(),
    lingui(),
  ],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    port: 5173,
  },
})
```

- [ ] **Step 8.4: Write `tailwind.config.template.ts`**

```ts
import type { Config } from 'tailwindcss'

// Tailwind v4 uses CSS-first config via @theme in globals.css.
// This file is mainly for tool compatibility; theme extensions live in globals.css.
const config: Config = {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  darkMode: 'class',
}

export default config
```

- [ ] **Step 8.5: Write `eslint.config.template.js`**

ESLint 9 flat config with `eslint-plugin-react-hooks` manually wired per G1 Gotchas:

```js
import js from '@eslint/js'
import tseslint from 'typescript-eslint'
import react from 'eslint-plugin-react'
import reactHooks from 'eslint-plugin-react-hooks'

export default [
  js.configs.recommended,
  ...tseslint.configs.strict,
  {
    files: ['src/**/*.{ts,tsx}'],
    languageOptions: {
      ecmaVersion: 2023,
      sourceType: 'module',
      parserOptions: { ecmaFeatures: { jsx: true } },
    },
    plugins: {
      react,
      'react-hooks': reactHooks,
    },
    rules: {
      ...reactHooks.configs.recommended.rules,
      '@typescript-eslint/no-explicit-any': 'error',
      '@typescript-eslint/no-non-null-assertion': 'error',
      '@typescript-eslint/consistent-type-imports': 'error',
      '@typescript-eslint/no-floating-promises': 'error',
      'no-console': ['warn', { allow: ['warn', 'error'] }],
    },
  },
  { ignores: ['dist/', 'src/wasm/', 'src-tauri/target/', 'node_modules/'] },
]
```

- [ ] **Step 8.6: Write `package.json.template`**

```json
{
  "name": "APP_NAME_PLACEHOLDER",
  "version": "0.1.0",
  "private": true,
  "type": "module",
  "packageManager": "pnpm@9.15.0",
  "scripts": {
    "dev": "vite",
    "build": "pnpm run wasm:build && pnpm tsc --noEmit && vite build",
    "preview": "vite preview",
    "tsc": "tsc --noEmit",
    "lint": "eslint . --max-warnings=0",
    "lint:fix": "eslint . --fix",
    "format": "prettier --write .",
    "format:check": "prettier --check .",
    "test": "vitest run",
    "test:watch": "vitest",
    "test:coverage": "vitest run --coverage",
    "e2e": "playwright test",
    "wasm:build": "wasm-pack build crates/core --target web --release --out-dir ../../src/wasm/core",
    "codegen": "tsr generate && lingui extract && lingui compile",
    "tauri:dev": "tauri dev",
    "tauri:build": "tauri build"
  },
  "dependencies": {
    "react": "^19.0.0",
    "react-dom": "^19.0.0",
    "@tanstack/react-router": "^1.0.0",
    "@tanstack/react-query": "^5.0.0",
    "zustand": "^5.0.0",
    "react-hook-form": "^7.0.0",
    "@hookform/resolvers": "^3.0.0",
    "zod": "^3.0.0",
    "neverthrow": "^8.0.0",
    "@lingui/react": "^5.0.0",
    "@lingui/core": "^5.0.0",
    "next-themes": "^0.4.0",
    "lucide-react": "^0.400.0",
    "sonner": "^1.0.0",
    "class-variance-authority": "^0.7.0",
    "clsx": "^2.0.0",
    "tailwind-merge": "^2.0.0",
    "date-fns": "^4.0.0"
  },
  "devDependencies": {
    "@vitejs/plugin-react-swc": "^3.0.0",
    "vite": "^6.0.0",
    "vite-plugin-wasm": "^3.0.0",
    "vite-plugin-top-level-await": "^1.0.0",
    "@tanstack/router-plugin": "^1.0.0",
    "tailwindcss": "^4.0.0",
    "@tailwindcss/vite": "^4.0.0",
    "@lingui/cli": "^5.0.0",
    "@lingui/vite-plugin": "^5.0.0",
    "@lingui/macro": "^5.0.0",
    "@lingui/swc-plugin": "^5.0.0",
    "typescript": "^5.5.0",
    "typescript-eslint": "^8.0.0",
    "eslint": "^9.0.0",
    "eslint-plugin-react": "^7.0.0",
    "eslint-plugin-react-hooks": "^5.0.0",
    "prettier": "^3.0.0",
    "vitest": "^2.0.0",
    "@vitest/ui": "^2.0.0",
    "@testing-library/react": "^16.0.0",
    "@testing-library/jest-dom": "^6.0.0",
    "@testing-library/user-event": "^14.0.0",
    "jsdom": "^25.0.0",
    "@playwright/test": "^1.0.0",
    "@tauri-apps/cli": "^2.0.0",
    "msw": "^2.0.0"
  }
}
```

**Note**: All version pins use caret ranges (`^X.0.0`) — major version lock with minor/patch updates allowed. No hardcoded patch versions per spec AP-01.

- [ ] **Step 8.7: Write `pnpm-workspace.yaml.template`**

```yaml
packages:
  - '.'
  - 'crates/*'
```

- [ ] **Step 8.8: Write `Cargo.toml.template`**

```toml
[workspace]
resolver = "2"
members = [
  "src-tauri",
  "crates/core",
]

[workspace.package]
edition = "2021"
```

- [ ] **Step 8.9: Write `lingui.config.ts.template`**

```ts
import { defineConfig } from '@lingui/cli'

export default defineConfig({
  sourceLocale: 'en',
  locales: ['en', 'ko'],
  catalogs: [
    {
      path: 'src/infrastructure/i18n/locales/{locale}',
      include: ['src'],
    },
  ],
})
```

- [ ] **Step 8.10: Write `harness-project.yaml.template`**

Source: `docs/react/kit-design/final-integration.md` §1.1 (lines 27-154). Copy the entire YAML block into `react-kit/templates/harness-project.yaml.template`. The template is the full 130-line `.harness/project.yaml` config with contract_categories, anti_patterns, commands, etc.

- [ ] **Step 8.11: Verify all templates exist**

```bash
ls react-kit/templates/ | wc -l
```

Expected: `9`

- [ ] **Step 8.12: Verify JSON/YAML templates parse**

```bash
python3 -c "import json; json.load(open('react-kit/templates/tsconfig.template.json')); print('tsconfig OK')"
python3 -c "import json; json.load(open('react-kit/templates/package.json.template')); print('package OK')"
python3 -c "import yaml; yaml.safe_load(open('react-kit/templates/pnpm-workspace.yaml.template')); print('pnpm OK')"
python3 -c "import yaml; yaml.safe_load(open('react-kit/templates/harness-project.yaml.template')); print('harness OK')"
```

Expected: 4 × `OK`

- [ ] **Step 8.13: Commit all templates**

```bash
git add react-kit/templates/
git commit -m "feat(react-kit): add 9 scaffolding templates (tsconfig, vite, tailwind, eslint, package, pnpm, cargo, lingui, harness)"
```

---

### Task 9: Create empty `skills/` and `agents/` directories with `.gitkeep`

**Files:**
- Create: `react-kit/skills/.gitkeep`
- Create: `react-kit/agents/.gitkeep`

- [ ] **Step 9.1: Create directories with .gitkeep**

```bash
mkdir -p react-kit/skills react-kit/agents
touch react-kit/skills/.gitkeep react-kit/agents/.gitkeep
```

- [ ] **Step 9.2: Commit**

```bash
git add react-kit/skills/.gitkeep react-kit/agents/.gitkeep
git commit -m "chore(react-kit): scaffold empty skills/ and agents/ dirs"
```

---

### Task 10: Create `evals/evals.json` and fixture directories

**Files:**
- Create: `react-kit/evals/evals.json`
- Create: `react-kit/evals/test-fixtures/empty-project/.gitkeep`
- Create: `react-kit/evals/test-fixtures/clean-arch-project/.gitkeep`
- Create: `react-kit/evals/test-fixtures/wasm-project/.gitkeep`
- Create: `react-kit/evals/test-fixtures/tauri-project/.gitkeep`
- Create: `react-kit/evals/test-fixtures/audit-target-project/.gitkeep`

- [ ] **Step 10.1: Create evals directories**

```bash
mkdir -p react-kit/evals/test-fixtures/empty-project
mkdir -p react-kit/evals/test-fixtures/clean-arch-project
mkdir -p react-kit/evals/test-fixtures/wasm-project
mkdir -p react-kit/evals/test-fixtures/tauri-project
mkdir -p react-kit/evals/test-fixtures/audit-target-project
touch react-kit/evals/test-fixtures/empty-project/.gitkeep
touch react-kit/evals/test-fixtures/clean-arch-project/.gitkeep
touch react-kit/evals/test-fixtures/wasm-project/.gitkeep
touch react-kit/evals/test-fixtures/tauri-project/.gitkeep
touch react-kit/evals/test-fixtures/audit-target-project/.gitkeep
```

- [ ] **Step 10.2: Write `evals/evals.json`**

Create `react-kit/evals/evals.json`:

```json
{
  "version": 1,
  "plugin": "react-kit",
  "description": "react-kit skill evaluations. Skills are added in Phase 2~9. Currently empty scaffold.",
  "tests": []
}
```

- [ ] **Step 10.3: Verify JSON parses**

```bash
python3 -c "import json; json.load(open('react-kit/evals/evals.json')); print('OK')"
```

Expected: `OK`

- [ ] **Step 10.4: Commit**

```bash
git add react-kit/evals/
git commit -m "feat(react-kit): scaffold evals.json and 5 test-fixture dirs"
```

---

### Task 11: Create `scripts/project-detect.sh`

**Files:**
- Create: `react-kit/scripts/project-detect.sh`

- [ ] **Step 11.1: Create scripts directory**

```bash
mkdir -p react-kit/scripts
```

- [ ] **Step 11.2: Write `project-detect.sh`**

Create `react-kit/scripts/project-detect.sh`:

```bash
#!/usr/bin/env bash
# project-detect.sh — react-kit project environment detection
# Reads the current working directory and prints a JSON detection result.
# Used by skills that need quick bash-callable detection (outside of Claude).

set -euo pipefail

# ── Helpers ─────────────────────────────────────────────
read_json_field() {
  # Usage: read_json_field <file> <field-path>
  local file="$1"
  local path="$2"
  if [ ! -f "$file" ]; then
    echo "null"
    return
  fi
  if command -v jq >/dev/null 2>&1; then
    jq -r "$path // \"null\"" "$file" 2>/dev/null || echo "null"
  else
    python3 -c "
import json, sys
try:
    with open('$file') as f:
        data = json.load(f)
    path = '$path'.lstrip('.').split('.')
    for p in path:
        if p.startswith('\"') and p.endswith('\"'):
            p = p[1:-1]
        data = data.get(p) if isinstance(data, dict) else None
    print(data if data else 'null')
except Exception:
    print('null')
"
  fi
}

# ── Detection ───────────────────────────────────────────
NODE_VERSION="null"
if [ -f ".nvmrc" ]; then
  NODE_VERSION=$(tr -d '\n' < .nvmrc)
fi

PNPM_VERSION=$(read_json_field "package.json" ".packageManager")
REACT_VERSION=$(read_json_field "package.json" ".dependencies.react")
VITE_VERSION=$(read_json_field "package.json" ".devDependencies.vite")
TAILWIND_VERSION=$(read_json_field "package.json" ".devDependencies.tailwindcss")

SHADCN=false
[ -f "components.json" ] && SHADCN=true

TANSTACK_ROUTER=false
[ -n "$(read_json_field 'package.json' '.devDependencies.\"@tanstack/router-plugin\"')" ] && TANSTACK_ROUTER=true

CARGO_WORKSPACE=false
if [ -f "Cargo.toml" ] && grep -q '\[workspace\]' Cargo.toml 2>/dev/null; then
  CARGO_WORKSPACE=true
fi

TAURI=false
[ -d "src-tauri" ] && [ -f "src-tauri/tauri.conf.json" ] && TAURI=true

LINGUI=false
[ -f "lingui.config.ts" ] && LINGUI=true

STRICT_TS=false
if [ -f "tsconfig.json" ] && grep -q '"strict"[[:space:]]*:[[:space:]]*true' tsconfig.json 2>/dev/null; then
  STRICT_TS=true
fi

# ── Output JSON ─────────────────────────────────────────
cat <<EOF
{
  "node": "$NODE_VERSION",
  "pnpm": "$PNPM_VERSION",
  "react": "$REACT_VERSION",
  "vite": "$VITE_VERSION",
  "tailwind": "$TAILWIND_VERSION",
  "shadcn": $SHADCN,
  "tanstackRouter": $TANSTACK_ROUTER,
  "cargoWorkspace": $CARGO_WORKSPACE,
  "tauri": $TAURI,
  "lingui": $LINGUI,
  "strictTS": $STRICT_TS
}
EOF
```

- [ ] **Step 11.3: Make executable**

```bash
chmod +x react-kit/scripts/project-detect.sh
```

- [ ] **Step 11.4: Smoke test on current repo (it's a monorepo, results will be mostly null)**

```bash
cd react-kit && bash scripts/project-detect.sh && cd ..
```

Expected: JSON output with all fields, most will be `"null"` or `false` since we're in the claude-plugins repo, not a user project.

- [ ] **Step 11.5: Commit**

```bash
git add react-kit/scripts/project-detect.sh
git commit -m "feat(react-kit): add project-detect.sh bash helper"
```

---

### Task 12: Register `react-kit` in `.claude-plugin/marketplace.json`

**Files:**
- Modify: `.claude-plugin/marketplace.json`

- [ ] **Step 12.1: Inspect current marketplace.json**

```bash
cat .claude-plugin/marketplace.json
```

Note the position of the `rust-kit` entry — react-kit goes right after it.

- [ ] **Step 12.2: Add react-kit entry**

Open `.claude-plugin/marketplace.json` and add this entry to the `plugins` array after the `rust-kit` entry:

```json
    {
      "name": "react-kit",
      "source": "./react-kit",
      "description": "[v0.1.0 · 2026-04-10] React + Vite + Tauri 2 + Rust WASM 전용 개발 워크플로우 플러그인 — 21종 스킬 + 3 에이전트, 라이브러리 0개 애니메이션"
    }
```

Ensure trailing comma is correct — rust-kit's entry will need a trailing comma added if it's currently the last entry.

- [ ] **Step 12.3: Verify JSON parses**

```bash
python3 -c "import json; d = json.load(open('.claude-plugin/marketplace.json')); names = [p['name'] for p in d['plugins']]; print(names); assert 'react-kit' in names, 'react-kit missing'"
```

Expected: list of plugin names including `'react-kit'`.

- [ ] **Step 12.4: Commit**

```bash
git add .claude-plugin/marketplace.json
git commit -m "feat(react-kit): register in marketplace.json as v0.1.0"
```

---

### Task 13: Run `sync-docs.py --check-only` and fix any issues

**Files:**
- Potentially modify: `react-kit/README.md` (if sync-docs reports issues)

- [ ] **Step 13.1: Run sync-docs in check mode**

```bash
python3 scripts/sync-docs.py --check-only react-kit 2>&1
```

Expected: either "all in sync" or a list of AUTO marker sections that need population.

- [ ] **Step 13.2: If README AUTO markers are empty and sync-docs wants content**

Since skills/ and agents/ directories only contain `.gitkeep`, sync-docs should produce empty tables or a "no skills" message in the AUTO:skills block. If it fails entirely, inspect `scripts/sync-docs.py` for its handling of empty skill lists.

If a fix is needed, manually edit the AUTO:skills block in `react-kit/README.md` to contain a placeholder row:

```markdown
<!-- AUTO:skills -->
## 스킬

| 스킬 | 용도 |
|------|------|
| _(Phase 2~9 에서 21개 스킬 추가 예정)_ | — |
<!-- /AUTO:skills -->
```

And similarly for agents:

```markdown
<!-- AUTO:agents -->
## 에이전트

| 에이전트 | 용도 |
|---------|------|
| _(Phase 7, 8, 9 에서 3개 에이전트 추가 예정)_ | — |
<!-- /AUTO:agents -->
```

- [ ] **Step 13.3: Re-run check**

```bash
python3 scripts/sync-docs.py --check-only react-kit 2>&1
```

Expected: no errors.

- [ ] **Step 13.4: Commit any fixes**

Only commit if README was actually modified:

```bash
git status --short react-kit/README.md
# If modified:
git add react-kit/README.md
git commit -m "docs(react-kit): align README with sync-docs check"
```

---

### Task 14: Harness project.yaml update for this repo (add react-kit trigger keywords)

**Files:**
- Modify: `.harness/project.yaml` (optional — if kit-design keywords are not already in trigger.always)

- [ ] **Step 14.1: Check current trigger keywords**

```bash
grep -A5 "always:" .harness/project.yaml
```

- [ ] **Step 14.2: If 'react-kit' is not in trigger.always, add it**

This is a meta-update: tell the repo harness that `react-kit` file changes should trigger contract processing. Only add if missing. Open `.harness/project.yaml` and ensure the `trigger.always` list includes:

```yaml
always:
  - "릴리스"
  - "release"
  - "버전"
  - "react-kit"
  - "react"
```

- [ ] **Step 14.3: Commit if modified**

```bash
git status --short .harness/project.yaml
# If modified:
git add .harness/project.yaml
git commit -m "chore(harness): add react-kit trigger keywords"
```

---

### Task 15: Verify full file tree

**Files:**
- None modified.

- [ ] **Step 15.1: Verify directory layout**

```bash
find react-kit -type f -not -path '*/.*' | sort
```

Expected output (19+ files):
```
react-kit/.claude-plugin/plugin.json
react-kit/README.md
react-kit/evals/evals.json
react-kit/evals/test-fixtures/audit-target-project/.gitkeep
react-kit/evals/test-fixtures/clean-arch-project/.gitkeep
react-kit/evals/test-fixtures/empty-project/.gitkeep
react-kit/evals/test-fixtures/tauri-project/.gitkeep
react-kit/evals/test-fixtures/wasm-project/.gitkeep
react-kit/references/clean-arch-layout.md
react-kit/references/project-detection.md
react-kit/references/result-patterns.md
react-kit/references/style-guide.md
react-kit/references/wasm-catalog.md
react-kit/scripts/project-detect.sh
react-kit/templates/Cargo.toml.template
react-kit/templates/eslint.config.template.js
react-kit/templates/harness-project.yaml.template
react-kit/templates/lingui.config.ts.template
react-kit/templates/package.json.template
react-kit/templates/pnpm-workspace.yaml.template
react-kit/templates/tailwind.config.template.ts
react-kit/templates/tsconfig.template.json
react-kit/templates/vite.config.template.ts
react-kit/agents/.gitkeep
react-kit/skills/.gitkeep
```

(The find output will be alphabetical; match the count — at least 19 files excluding .gitkeep, or 25 with .gitkeep.)

- [ ] **Step 15.2: Verify plugin.json loads via Claude Code**

```bash
ls react-kit/.claude-plugin/plugin.json && echo "plugin.json present"
```

- [ ] **Step 15.3: Verify marketplace registration**

```bash
python3 -c "
import json
with open('.claude-plugin/marketplace.json') as f:
    d = json.load(f)
names = [p['name'] for p in d['plugins']]
assert 'react-kit' in names, f'react-kit missing from {names}'
print(f'Registered plugins: {names}')
"
```

Expected: list includes `react-kit`.

- [ ] **Step 15.4: Verify no files are missing from any reference document**

```bash
grep -l "react-kit/" docs/react/kit-design/*.md | head
```

Expected: multiple files reference react-kit/ paths. The plan itself is the source of truth for these paths.

---

### Task 16: Run harness sprint-contract + qa-evaluator on Phase 1 delivery

This task follows the user policy: every implementation phase gets a sprint-contract + qa-evaluator cycle.

**Files:**
- None additional.

- [ ] **Step 16.1: Archive any existing sprint-contract**

```bash
if [ -f .harness/sprint-contract.md ]; then
  mv .harness/sprint-contract.md ".harness/history/$(date +%Y%m%d-%H%M)-before-react-kit-phase1-sprint-contract.md"
fi
```

- [ ] **Step 16.2: Write sprint-contract for Phase 1 delivery**

Create `.harness/sprint-contract.md` with conditions matching Phase 1 deliverables:

```markdown
---
feature: "react-kit Phase 1 Foundation"
created: "<current timestamp>"
complexity: "중간"
conditions: 12
scope: "react-kit/ 플러그인 디렉토리 스캐폴드 + marketplace.json 등록. 스킬 0개 (Phase 2~9 에서 추가)"
---

## Skill
- [ ] SK-01: react-kit/.claude-plugin/plugin.json 이 존재하고 유효한 JSON 이며 name=react-kit, version=0.1.0 을 포함한다
- [ ] SK-02: react-kit/README.md 가 존재하고 AUTO:skills, AUTO:agents 마커 4개를 포함한다
- [ ] SK-03: react-kit/references/ 에 project-detection.md, clean-arch-layout.md, result-patterns.md, wasm-catalog.md, style-guide.md 5개 파일이 존재한다
- [ ] SK-04: react-kit/templates/ 에 9개 템플릿 파일이 존재한다 (tsconfig, eslint, vite, tailwind, package.json, pnpm-workspace, Cargo, lingui, harness-project)
- [ ] SK-05: react-kit/evals/evals.json 이 존재하고 유효한 JSON 이며 test-fixtures/ 아래 5개 fixture 디렉토리가 존재한다
- [ ] SK-06: react-kit/scripts/project-detect.sh 가 존재하고 실행 권한이 있으며 bash 구문이 유효하다 (bash -n 통과)

## Script
- [ ] SC-01: 모든 템플릿의 JSON/YAML 파일이 parse 가능하다
- [ ] SC-02: 모든 템플릿의 라이브러리 버전이 caret range (^X.0.0) 로 표기되고 특정 패치 버전 하드코딩 없음

## Architecture
- [ ] AR-01: react-kit/ 의 폴더 구조가 기존 flutter-toolkit/, rust-kit/ 과 일관된다 (.claude-plugin/, skills/, agents/, references/, templates/, evals/)
- [ ] AR-02: .claude-plugin/marketplace.json 에 react-kit 엔트리가 rust-kit 뒤에 추가되어 있고 name/source/description 3개 필드를 포함한다

## Anti-patterns
- [ ] AP-01: 특정 패치 버전 하드코딩 없음 (plugin.json version 0.1.0 은 초기 버전 선언이므로 예외)

## Reusability
- [ ] RE-01: references/ 의 내용이 docs/react/kit-design/ 설계 문서들과 일관된다
- [ ] RE-02: 이 Phase 에서 SKILL.md 를 추가하지 않았다 (스킬은 Phase 2~9 에서 추가 예정)

## Diagnostics
- [ ] DG-01: N/A (마크다운 + 템플릿, 빌드 대상 아님)
- [ ] DG-02: N/A (IDE diagnostics 대상 아님)
- [ ] DG-03: 문서 내 placeholder (TODO, TBD, FIXME) 0건
- [ ] DG-04: 모든 외부 URL 이 http(s):// 형식
```

- [ ] **Step 16.3: Invoke harness:qa-evaluator via Agent tool**

Use the Agent tool to spawn `harness:qa-evaluator` with a prompt similar to:

```
Evaluate react-kit Phase 1 Foundation against the sprint contract.

Target: react-kit/ directory + .claude-plugin/marketplace.json entry
Sprint contract: .harness/sprint-contract.md

Verify each condition SK-01 through DG-04 and return APPROVE/REJECT with line/file evidence.
```

- [ ] **Step 16.4: If REJECT, fix the specific failures and re-run**

Address each FAIL individually with targeted edits. Re-dispatch qa-evaluator until APPROVE.

- [ ] **Step 16.5: If APPROVE, commit the sprint-contract**

```bash
# Archive the contract into history as proof of completion
mv .harness/sprint-contract.md ".harness/history/$(date +%Y%m%d-%H%M)-react-kit-phase1-sprint-contract.md"
git add .harness/history/
git commit -m "chore(harness): archive react-kit Phase 1 sprint-contract (APPROVE)"
```

---

### Task 17: Final commit + summary

**Files:**
- None.

- [ ] **Step 17.1: Verify no uncommitted changes**

```bash
git status --short
```

Expected: clean working tree.

- [ ] **Step 17.2: View git log for Phase 1**

```bash
git log --oneline -20
```

Expected: at least 13 new commits starting with `feat(react-kit)`, `docs(react-kit)`, `chore(react-kit)`.

- [ ] **Step 17.3: Print summary**

```bash
echo "=== react-kit Phase 1 Foundation — Complete ==="
echo "Plugin registered: react-kit v0.1.0"
echo "Files created: $(find react-kit -type f -not -path '*/.*' | wc -l)"
echo "Next: Phase 2 (G1 scaffolding skills) — write a new plan via writing-plans"
```

---

## Self-Review Checklist

After implementation, verify:

**1. Spec coverage**:
- ✅ Spec §2 (Tech Stack) → `templates/` files pin versions
- ✅ Spec §3 (Clean Arch monorepo) → `references/clean-arch-layout.md`
- ✅ Spec §4 (21 skills) → **explicitly deferred** to Phase 2~9 (skills/ empty)
- ✅ Spec §5 (WASM catalog) → `references/wasm-catalog.md` pointer
- ✅ Spec §6 (library-zero animation) → deferred to Phase 7 (G5b plan)
- ✅ Spec §7 (harness integration) → `templates/harness-project.yaml.template`
- ✅ Spec §11 Phase 1 → fully covered by this plan
- ❌ Spec §11 Phase 2~10 → each gets its own plan (not this one)

**2. Placeholder scan**: no "TODO", "TBD", "implement later" in this plan. Only intentional Phase 2~9 deferrals, clearly labeled.

**3. Type consistency**: template file contents match version ranges and API usage verified in design docs. `package.json.template` caret ranges match `docs/react/kit-design/g1-scaffolding.md` §1.4 installation commands.

**4. Commit count**: ~14 commits expected. Each step is 2-5 minutes of mechanical work — no deep thinking required because all content was decided in the design phase.

## Execution Handoff

**Plan complete and saved to `docs/superpowers/plans/2026-04-10-react-kit-phase1-foundation.md`.**

Two execution options:

**1. Subagent-Driven (recommended)** — I dispatch a fresh subagent per task (each task is mostly file-creation, so cheap and fast), review between tasks, surface any drift.

**2. Inline Execution** — Execute tasks in this session using `superpowers:executing-plans`, batch execution with checkpoints for review.

**What about Phases 2~10?** Those will each get their own plan written via `writing-plans` in future sessions. Each subsequent plan will be scoped to a single skill group (G1, G2, etc.) producing 3~4 `SKILL.md` files + relevant agent files. Running all 10 plans would produce the complete 21-skill + 3-agent plugin ready for v0.1.0 release.

**Which approach for Phase 1?**
