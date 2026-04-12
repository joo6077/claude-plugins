---
name: react-init
description: >
  Vite + Tauri 2 + React + TypeScript strict + Tailwind v4 + shadcn/ui + TanStack Router 스택으로
  모노레포 프로젝트를 처음부터 스캐폴딩한다.
  "react 프로젝트 초기화", "새 React 앱", "Vite Tauri 세팅", "react init", "react 스캐폴딩" 같은 요청 시 트리거.
  기존 프로젝트에 모듈을 추가할 때는 트리거하지 않는다 — 화면 추가는 /react-screen, 기능 추가는 /react-feature 사용.
argument-hint: "[project-name] [--with-wasm] [--with-tauri] [--package-manager=pnpm]"
user-invocable: true
---

# Gotchas

1. **pnpm workspace ↔ Cargo workspace 혼동 금지** — `pnpm-workspace.yaml`의 `packages` 목록과 `Cargo.toml`의 `workspace.members`는 별개다. 전자는 npm 패키지, 후자는 Rust crate. `crates/core`는 두 파일 모두에 등재한다.
2. **Tailwind v4 설치 방식 변경 (2025-01 stable)** — v3 문서의 `npx tailwindcss init`은 v4에서 없어짐. `@tailwindcss/vite` 플러그인과 `@import "tailwindcss";` 만 사용한다. **CSS-first 설정**: `tailwind.config.ts` 대신 CSS 파일의 `@theme { --color-*: oklch(...); }` directive 로 토큰을 정의한다 (Tailwind v4 announcement).
3. **shadcn 패키지 리네임 + CLI v4 (2026-03)** — `shadcn-ui` npm 패키지는 deprecated. 현재는 `pnpm dlx shadcn@latest init --template vite`를 사용한다. v4 CLI 는 `--dry-run`/`--diff`/`--view` 플래그로 설치 전 미리보기 가능, `components.json` 의 `tailwind.config` 필드는 **Tailwind v4 에서 공란으로 둔다** (shadcn tailwind-v4 docs).
4. **shadcn + Tailwind v4 + React 19 조합** — 초기 설치 직후 `pnpm tsc --noEmit`으로 타입 오류 점검 필수. shadcn v4 컴포넌트는 React 19 `ref as prop` 패턴으로 생성되므로 기존 `forwardRef` 와 혼재 가능 — 둘 다 허용.
5. **React 19 stable (2024-12) + forwardRef deprecation 예고** — 2026-04 현재 `react@19.2+` 가 production standard. **`forwardRef` 는 deprecation 예고** 상태로 경고 없이 동작하지만, **새 컴포넌트는 `ref` 를 일반 prop 으로 받는 패턴** 권장: `function Button({ ref, ...props }: Props & { ref?: Ref<HTMLButtonElement> }) { ... }`. 기존 컴포넌트는 하위호환 유지 (React v19 블로그).
6. **Zod v4 + @hookform/resolvers TS 호환성 이슈** — 2026-04 현재 `zod@4.3.x` + `@hookform/resolvers` 의 `zodResolver` 는 Zod v4 `ZodType` 시그니처 변경과 충돌해 타입 에러 가능. **workaround**: (a) `import { z } from 'zod/v3'` (Zod v4 가 노출하는 v3 alias 사용) 또는 (b) `@hookform/resolvers` 업데이트 릴리스 확인. 감지 방법: `pnpm tsc --noEmit` 실행 시 zodResolver 호출부 타입 에러. 영향 범위는 `/react-form` 이 생성하는 컴포넌트 (hookform resolvers#813, RHF#12829).
7. **next-themes + Vite** — SSR 경고 발생 가능. client-only 모드로 사용하고 초기 테마를 `<html class="dark">`로 inline script로 설정.
8. **TanStack Router codegen** — `routeTree.gen.ts`는 플러그인이 자동 생성하므로 수동 수정 금지. 기본적으로 `.gitignore` 제외 권장(merge conflict 최소화).
9. **Strict TS 위반 거부** — 생성된 초기 파일에 `any`, `as`, `!`가 포함되면 생성 실패로 간주하고 롤백. `pnpm tsc --noEmit`으로 검증 필수.
10. **`eslint-plugin-react-hooks` v6 flat config 기본** — v6 (React 19.2+) 부터 flat config 가 기본이며 React Compiler lint 룰이 통합됐다. `eslint.config.js` 에서 `plugins: { 'react-hooks': reactHooks }` + `rules: reactHooks.configs.recommended.rules` 형태로 구성한다.
11. **Rust WASM crate-type** — `crates/core/Cargo.toml`에 `crate-type = ["cdylib", "rlib"]` 둘 다 있어야 WASM 빌드와 Tauri 네이티브 재사용이 동시에 가능하다.
12. **Vite 8 (Rolldown) 2026-03-12 stable** — `pnpm create vite@latest` 는 2026-04 기준 **Vite 8 템플릿**을 받는다. Vite 8 은 Rust 기반 Rolldown 단일 번들러로 통합되어 10~30배 빠른 빌드 + 기존 플러그인 호환성 유지. 기존 Vite 6/7 프로젝트는 `pnpm add -D vite@latest` 로 단순 업그레이드. Environment API 는 framework authors 대상이므로 일반 앱은 신경 쓸 필요 없음 (Vite 8 announce).
13. **기존 파일 overwrite 금지** — 같은 이름의 파일/디렉토리가 이미 존재하면 생성을 거부한다. `--force` 플래그가 있을 때만 덮어쓴다.
14. **실패 시 전체 롤백** — 복수 파일 생성 중 하나라도 실패하면 스킬 실행으로 생성된 파일을 모두 삭제하고 원상복구한다.
15. **하드코딩된 버전 번호 금지** — 의존성 설치 시 `pnpm add <package>@latest`로 최신 버전을 받는다. 특정 패치 버전을 고정하지 않는다.
16. **React Compiler v1.0 (2025-10) 기본 활성화** — Vite `create-vite` 템플릿에서 기본 포함. `babel-plugin-react-compiler` 로 자동 메모이제이션 적용. **정확한 버전 핀 권장** (`1.0.0`, `^1.0.0` 아님) — 메모이제이션 변경이 `useEffect` 동작에 영향 가능. 점진적 도입은 `compilationMode: 'annotation'` + `"use memo"` directive 로 디렉토리 단위 rollout. Meta 프로덕션 검증: 초기 로드 12% 개선, 특정 인터랙션 2.5배 속도 향상.
17. **`@vitejs/plugin-react` v6 — Babel 제거, Oxc 기반** — Vite 8 과 함께 출시. React Refresh 트랜스폼을 Oxc 로 처리하여 Babel 의존성 제거. 기존 Babel 플러그인을 사용하는 프로젝트는 별도 `babel.config.js` 와 `@vitejs/plugin-react` 의 `babel` 옵션으로 유지 가능하지만, 새 프로젝트는 Oxc 기본 경로를 따른다.
18. **shadcn Luma 디자인 시스템 (2026-03)** — `shadcn/create` 에서 Luma preset 선택 가능. 둥근 기하학, 부드러운 elevation, 넉넉한 spacing. Radix UI 외에 Base UI 프리미티브도 선택 가능하여 번들 사이즈 최적화 옵션이 열렸다. 초기화 시 사용자에게 프리미티브 선택지(Radix/Base UI) 를 제시한다.

# Process

## 1. 입력 수집

다음을 확인한다:
- `project_name` (필수): npm 패키지명 규칙 (`^[a-z][a-z0-9-]*$`). 미지정 시 사용자에게 요청.
- `--with-wasm` (기본 true): `crates/core/` + wasm-pack 파이프라인 포함 여부
- `--with-tauri` (기본 true): Tauri 데스크탑 대상 포함 여부. false면 웹 전용 Vite 앱
- `--package-manager` (기본 `pnpm`): pnpm 외의 값은 거부 (workspace 통합 일관성)

현재 디렉토리에 `package.json`이 없거나 React가 아니면 새 프로젝트로 진행. 이미 `src-tauri/`가 있으면 "기존 Tauri 프로젝트 확장" 모드로 전환.

## 2. 프로젝트 환경 감지

`references/project-detection.md` 절차를 실행하여 기존 환경을 파악한다.

## 3. 생성 명령 순서

아래 순서를 **반드시 지켜야** 한다. 순서가 바뀌면 중간에 실패 누적. 각 단계 실패 시 이전 산출물을 롤백한다.

### 단계 1 — pnpm workspace 생성

```bash
mkdir -p <project_name> && cd <project_name>
pnpm init
# pnpm-workspace.yaml 작성: packages: ['.', 'crates/*']
```

### 단계 2 — Vite + React + TypeScript 스캐폴딩

```bash
pnpm create vite@latest . --template react-swc-ts
```

`tsconfig.json`에 아래 strict 옵션을 추가한다:

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

### 단계 3 — Tailwind CSS v4 (Vite 플러그인, @theme + OKLCH)

```bash
pnpm add -D tailwindcss @tailwindcss/vite
```

`src/presentation/styles/globals.css` 생성 — **CSS-first 설정** (v4). `@theme` directive 에 **OKLCH 컬러**로 프로젝트 토큰을 정의한다. OKLCH 는 Tailwind v4 의 기본 색 공간이며 Phase 6 design-kit 토큰 체계(OKLCH / DTCG) 와 1:1 정합된다:

```css
@import "tailwindcss";

/*
 * Tailwind v4 @theme directive — CSS-first 설정.
 * 값은 OKLCH (Oklab Lightness Chroma Hue) — Tailwind v4 기본 색 공간.
 * design-kit 의 디자인 토큰이 있으면 그 값을 그대로 복사한다.
 */
@theme {
  --color-primary: oklch(0.72 0.19 250);
  --color-primary-foreground: oklch(0.98 0 0);
  --color-accent: oklch(0.78 0.15 60);
  --color-destructive: oklch(0.62 0.24 27);
  --color-background: oklch(1 0 0);
  --color-foreground: oklch(0.15 0 0);

  --font-sans: "Inter", ui-sans-serif, system-ui, sans-serif;

  --breakpoint-sm: 40rem;
  --breakpoint-md: 48rem;
  --breakpoint-lg: 64rem;
  --breakpoint-xl: 80rem;
}

/* dark 모드 토큰 — next-themes 의 .dark 클래스 기준 */
.dark {
  --color-background: oklch(0.15 0 0);
  --color-foreground: oklch(0.98 0 0);
}
```

`vite.config.ts`에 `tailwindcss()` 플러그인 추가. v4 는 **Container Queries 내장** (`@container` + `@sm:`/`@md:`/`@lg:` 유틸) — 별도 플러그인 불필요 (Tailwind v4 theme docs, Tailwind v4 container queries).

### 단계 4 — shadcn/ui 초기화

```bash
pnpm dlx shadcn@latest init --template vite
pnpm dlx shadcn@latest add button card input label
```

컴포넌트 경로: `src/presentation/shared/components/ui/`

### 단계 5 — TanStack Router 플러그인

```bash
pnpm add @tanstack/react-router
pnpm add -D @tanstack/router-plugin
```

`vite.config.ts`에 `tanstackRouter({ target: 'react', autoCodeSplitting: true })` 추가.
`src/presentation/routes/__root.tsx`, `index.tsx` 생성.

### 단계 6 — 상태 관리 & 데이터

```bash
pnpm add zustand @tanstack/react-query
pnpm add react-hook-form @hookform/resolvers zod neverthrow
```

### 단계 7 — i18n (Lingui v5, 매크로 패키지 split)

```bash
# runtime
pnpm add @lingui/react @lingui/core
# devDependency (매크로는 v5 에서 @lingui/core/macro + @lingui/react/macro 서브경로로 분리됨)
pnpm add -D @lingui/cli @lingui/vite-plugin @lingui/swc-plugin
```

**중요 — Lingui v5 매크로 패키지 분리 (2024-11 stable)**: 기존 `@lingui/macro` 는 deprecated. 실제 사용 시 import 경로는:

- JSX 매크로(`Trans`, `Plural`, `Select`, `SelectOrdinal`) → `@lingui/react/macro`
- core 매크로(`t`, `plural`, `select`, `selectOrdinal`, `defineMessage`, `msg`) → `@lingui/core/macro`

`@lingui/swc-plugin` 을 Vite config 의 `react({ plugins: [...] })` 가장 앞에 등록해 SWC 가 매크로를 먼저 transpile 하도록 한다. `lingui.config.ts` 작성 — `locales: ['ko', 'en']`, `catalogs: [{ path: '<rootDir>/src/infrastructure/i18n/locales/{locale}', include: ['src'] }]` (Lingui v5 migration).

### 단계 8 — 다크모드

```bash
pnpm add next-themes
```

Vite client-only 모드 구성. 초기 테마 inline script 추가.

### 단계 9 — Rust WASM 파이프라인 (`--with-wasm` true 시)

```bash
cargo new --lib crates/core
# crates/core/Cargo.toml: wasm-bindgen + crate-type = ["cdylib", "rlib"]
pnpm add -D vite-plugin-wasm vite-plugin-top-level-await
# vite.config.ts: wasm() + topLevelAwait() 추가
# Cargo.toml(root): workspace members = ["src-tauri", "crates/core"]
```

### 단계 10 — Tauri 2 GA (`--with-tauri` true 시, 2024-10-08 stable)

```bash
pnpm add -D @tauri-apps/cli
pnpm tauri init
# devUrl: http://localhost:5173, frontendDist: ../dist
# src-tauri/capabilities/default.json 최소 권한 세팅
```

**Tauri 2 stable 주요 변경** (Tauri 2.0 blog, v1→v2 migration):

- v1 의 allowlist 는 완전 제거 → **Capability (ACL) 체계**. `src-tauri/capabilities/*.json` 파일에 `identifier` / `description` / `windows` / `permissions` 를 선언.
- 기존 1.x 코어 기능(fs, dialog, shell, clipboard, notification 등)은 **개별 플러그인 크레이트**로 분리. 필요한 것만 `pnpm add @tauri-apps/plugin-fs` 등으로 추가.
- **permission identifier prefix**: beta→stable 마이그레이션에서 core permission 은 모두 `core:` prefix 필수. `"default"` 는 더 이상 없음 → `"core:default"` 사용.
- 기존 v1 프로젝트 마이그레이션은 `cargo tauri migrate` CLI 가 allowlist 를 파싱해 capability 파일을 자동 생성.

`src-tauri/capabilities/default.json` 최소 예시:

```json
{
  "$schema": "../gen/schemas/desktop-schema.json",
  "identifier": "default",
  "description": "react-kit 기본 capability — 최소 권한",
  "windows": ["main"],
  "permissions": [
    "core:default"
  ]
}
```

추가 권한이 필요할 때는 `/react-tauri` 스킬이 개별 permission identifier (`fs:allow-read-text-file`, `dialog:allow-open` 등) 를 capability 파일에 append 한다.

### 단계 11 — 테스트 도구

```bash
pnpm add -D vitest @testing-library/react @testing-library/jest-dom jsdom
pnpm add -D playwright @playwright/test
```

디렉토리 생성: `tests/unit/`, `tests/component/`, `tests/e2e/`

### 단계 12 — ESLint 9+ flat config + Prettier

```bash
pnpm add -D eslint typescript-eslint eslint-plugin-react eslint-plugin-react-hooks prettier
```

`eslint.config.js` 작성 (flat config v9+). `eslint-plugin-react-hooks` 수동 와이어링 포함.

### 단계 13 — harness 초기화

```text
/harness init 호출 → .harness/project.yaml 자동 생성
```

### 단계 14 — git 초기 커밋

```bash
git init && git add -A && git commit -m "chore: initial scaffold"
```

## 4. 산출 파일 구조

```text
<project>/
├── package.json                  # pnpm workspace root + scripts
├── pnpm-workspace.yaml           # packages: ['.', 'crates/*']
├── Cargo.toml                    # Rust workspace root
├── tsconfig.json                 # strict: true 포함 7개 옵션
├── tsconfig.node.json
├── vite.config.ts
├── tailwind.config.ts
├── eslint.config.js
├── lingui.config.ts
├── .prettierrc
├── .gitignore
├── .env.example
├── src/
│   ├── domain/entities/ data/ failures/ types/
│   ├── data/datasources/{remote,local,wasm}/ models/ repositories/
│   ├── presentation/
│   │   ├── features/
│   │   ├── shared/components/ui/  # shadcn 컴포넌트
│   │   ├── shared/components/layout/
│   │   ├── shared/hooks/
│   │   ├── shared/lib/utils.ts    # cn 헬퍼
│   │   ├── routes/__root.tsx, index.tsx
│   │   └── styles/globals.css
│   ├── infrastructure/tauri/ storage/ http/ i18n/
│   ├── wasm/core/                 # gitignored
│   ├── app.tsx, main.tsx, vite-env.d.ts
├── src-tauri/                     # --with-tauri 시
├── crates/core/                   # --with-wasm 시
├── tests/unit/ component/ e2e/
└── .harness/project.yaml
```

## 5. 검증

생성 완료 후 반드시 실행:

```bash
pnpm tsc --noEmit    # Strict TS 확인
pnpm eslint . --max-warnings=0
```

오류가 있으면 수정 후 재확인한다.

## 6. 완료 후 안내

생성된 파일/디렉토리 목록 출력 후 다음 단계 안내:
- 화면 추가: `/react-screen`
- 기능 구현: `/react-feature`
- 재사용 컴포넌트: `/react-widget`

# References

- `references/project-detection.md` — 프로젝트 감지
- `references/clean-arch-layout.md` — 레이어 배치
- `references/result-patterns.md` — Result 패턴 (neverthrow)
- `docs/react/kit-design/g1-scaffolding.md` §1 — 이 스킬의 상세 설계
