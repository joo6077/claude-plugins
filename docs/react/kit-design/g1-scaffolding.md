# G1 — Scaffolding & Generation Skills

```yaml
last_updated: 2026-04-10
group: G1
scope: react-kit 스캐폴딩 및 코드 생성 스킬 4종
skills: [/react-init, /react-screen, /react-feature, /react-widget]
research_sources:
  - Codex 시도 (task-mnsis4sm 중단, task-b95rx71qo 정체) → WebSearch fallback
  - Tailwind CSS v4 공식 Vite 가이드
  - shadcn/ui 공식 Vite 설치 가이드
  - TanStack Router 공식 Vite 설치 문서
  - Tauri 2 공식 Create Project / Vite 가이드
  - Menci/vite-plugin-wasm README (Vite 2~7 지원)
```

## 문서 목적

이 문서는 react-kit **G1 그룹 스킬 4종**의 상세 설계 스펙이다. 각 스킬의 트리거, 입력, 산출물, 명령 순서, Gotchas, 그리고 Clean Architecture 상의 배치를 규정한다. 실제 SKILL.md 작성 시 이 문서를 기준으로 삼는다.

**범위**: `/react-init` (프로젝트 스캐폴딩), `/react-screen` (화면/라우트 생성), `/react-feature` (복합 4계층 생성), `/react-widget` (shadcn 기반 위젯 생성).

## 공통 설계 원칙 (4개 스킬 공통)

- **프로젝트 감지 공유**: 모든 스킬이 `react-kit/references/project-detection.md` (flutter-toolkit 의 `project-detection.md` 패턴 모방) 를 읽어 프로젝트 환경을 감지한다. pnpm 버전, Node 버전, Vite 설정, Tailwind 설치 여부, shadcn 구성 여부, Cargo workspace 존재 여부 등을 한 곳에서 판정한다.
- **중복 감지 필수**: 이미 같은 이름/경로의 파일이 존재하면 **overwrite 금지**. 사용자 확인 후 `--force` 플래그가 있을 때만 덮어쓴다.
- **Strict TypeScript 강제**: 생성된 모든 TS 파일은 `tsc --noEmit` 과 `eslint --max-warnings=0` 을 통과해야 한다. `any`, `as` 단언, `!` non-null 단언을 포함한 코드 생성 금지.
- **실패 시 롤백**: 복수 파일 생성 중 하나라도 실패하면 그 스킬 실행으로 생성된 파일을 모두 삭제하고 원상복구한다.

## 1. /react-init — 프로젝트 스캐폴딩

Vite + Tauri 2 + React 19 + TypeScript strict + Tailwind v4 + shadcn/ui + TanStack Router + Zustand + TanStack Query + Lingui + Rust WASM 파이프라인을 한 번에 세팅한다.

### 1.1 트리거

- 키워드: "react 프로젝트 초기화", "react-init", "react 스캐폴딩", "새 React 앱", "Vite Tauri 세팅"
- 조건: 현재 디렉토리에 `package.json` 이 없거나, 있어도 React가 아닌 경우 새 프로젝트로 간주. 이미 `src-tauri/` 가 있으면 "기존 Tauri 프로젝트 확장" 모드로 전환.

### 1.2 입력

- `project_name` (필수): npm 패키지명 규칙 (`^[a-z][a-z0-9-]*$`)
- `--with-wasm` (기본 true): `crates/core/` + wasm-pack 파이프라인 포함 여부
- `--with-tauri` (기본 true): Tauri 데스크탑 대상 포함 여부. false면 웹 전용 Vite 앱
- `--package-manager` (기본 `pnpm`): 다른 값은 거부 (workspace 통합 일관성)

### 1.3 산출 파일 트리

`/react-init` 이 생성하는 모노레포 초기 구조 (ASCII 트리):

```
my-app/
├── package.json                    # pnpm workspace root + scripts
├── pnpm-workspace.yaml             # packages: src, src-tauri, crates/*
├── Cargo.toml                      # Rust workspace root (members: src-tauri, crates/core)
├── tsconfig.json                   # strict: true 외 7개 옵션
├── tsconfig.node.json
├── vite.config.ts                  # React + Tailwind v4 + TanStack Router + WASM 플러그인
├── tailwind.config.ts              # content paths + design tokens
├── postcss.config.js               # (Tailwind v4 Vite 플러그인 사용 시 생략 가능)
├── eslint.config.js                # flat config v9+
├── lingui.config.ts                # i18n
├── .prettierrc
├── .gitignore                      # dist, src/wasm, target, node_modules
├── .env.example
│
├── src/
│   ├── domain/
│   │   ├── entities/.gitkeep
│   │   ├── usecases/.gitkeep
│   │   ├── failures/.gitkeep
│   │   └── types/.gitkeep
│   ├── data/
│   │   ├── datasources/{remote,local,wasm}/.gitkeep
│   │   ├── models/.gitkeep
│   │   └── repositories/.gitkeep
│   ├── presentation/
│   │   ├── features/.gitkeep
│   │   ├── shared/
│   │   │   ├── components/ui/         # shadcn 컴포넌트 설치 위치
│   │   │   ├── components/layout/
│   │   │   ├── hooks/
│   │   │   └── lib/utils.ts           # cn 헬퍼 (shadcn 표준)
│   │   ├── routes/
│   │   │   ├── __root.tsx
│   │   │   └── index.tsx
│   │   └── styles/globals.css         # @import "tailwindcss";
│   ├── infrastructure/
│   │   ├── tauri/client.ts            # Tauri API feature detection wrapper
│   │   ├── storage/local.ts
│   │   ├── http/client.ts
│   │   └── i18n/setup.ts
│   ├── wasm/                          # gitignored — wasm-pack 산출물
│   │   └── core/.gitkeep
│   ├── app.tsx
│   ├── main.tsx
│   ├── routeTree.gen.ts               # TanStack Router codegen (gitignored 또는 커밋)
│   └── vite-env.d.ts
│
├── src-tauri/                         # tauri-apps/cli 로 생성
│   ├── Cargo.toml
│   ├── tauri.conf.json                # devUrl, frontendDist, permissions
│   ├── build.rs
│   ├── capabilities/
│   │   └── default.json
│   └── src/
│       ├── lib.rs
│       └── main.rs
│
├── crates/
│   └── core/                          # 고성능 Rust 코어 (WASM 타겟)
│       ├── Cargo.toml                 # wasm-bindgen + lib crate-type = ["cdylib", "rlib"]
│       └── src/lib.rs
│
├── tests/
│   ├── unit/.gitkeep                  # Vitest
│   ├── component/.gitkeep             # Testing Library
│   └── e2e/.gitkeep                   # Playwright
│
└── .harness/
    └── project.yaml                   # harness init 자동 실행
```

### 1.4 생성 명령 순서

아래 순서는 **반드시 지켜야 한다**. 순서가 바뀌면 중간에 실패 누적. 각 단계 실패 시 이전 산출물을 롤백한다.

```
1. pnpm workspace 생성
   └─ mkdir -p my-app && cd my-app
   └─ pnpm init (package.json scaffold)
   └─ pnpm-workspace.yaml 작성 (packages: ['.', 'crates/*'])

2. Vite + React + TypeScript 스캐폴딩
   └─ pnpm create vite@latest . --template react-swc-ts
   └─ tsconfig.json strict 옵션 확장 (아래 1.5 참조)

3. Tailwind CSS v4 (Vite 플러그인)
   └─ pnpm add -D tailwindcss @tailwindcss/vite
   └─ src/presentation/styles/globals.css 생성: @import "tailwindcss";
   └─ vite.config.ts 에 tailwindcss() 플러그인 추가
   └─ (출처: https://tailwindcss.com/docs/guides/vite , https://tailwindcss.com/blog/tailwindcss-v4)

4. shadcn/ui 초기화
   └─ pnpm dlx shadcn@latest init --template vite
   └─ 기본 컴포넌트 설치: pnpm dlx shadcn@latest add button card input label
   └─ src/presentation/shared/components/ui/ 경로 설정
   └─ (출처: https://ui.shadcn.com/docs/installation/vite , https://ui.shadcn.com/docs/cli)

5. TanStack Router 플러그인
   └─ pnpm add @tanstack/react-router
   └─ pnpm add -D @tanstack/router-plugin
   └─ vite.config.ts 에 tanstackRouter({ target: 'react', autoCodeSplitting: true }) 추가
   └─ src/presentation/routes/__root.tsx, index.tsx 생성
   └─ (출처: https://tanstack.com/router/latest/docs/installation/with-vite)

6. 상태 관리 & 데이터
   └─ pnpm add zustand @tanstack/react-query
   └─ pnpm add react-hook-form @hookform/resolvers zod neverthrow

7. i18n (Lingui)
   └─ pnpm add @lingui/react @lingui/core
   └─ pnpm add -D @lingui/cli @lingui/vite-plugin @lingui/macro
   └─ lingui.config.ts 작성

8. 다크모드
   └─ pnpm add next-themes (Vite 호환 확인 필수)

9. Rust WASM 파이프라인 (with-wasm 플래그 true 시)
   └─ cargo new --lib crates/core
   └─ crates/core/Cargo.toml 에 wasm-bindgen + crate-type = ["cdylib", "rlib"] 설정
   └─ pnpm add -D vite-plugin-wasm vite-plugin-top-level-await
   └─ vite.config.ts 에 wasm() + topLevelAwait() 추가
   └─ Cargo.toml (root) workspace members = ["src-tauri", "crates/core"]
   └─ (출처: https://github.com/Menci/vite-plugin-wasm)
   └─ 대안 플러그인: `nshen/vite-plugin-wasm-pack`, `rwasm/vite-plugin-rsw`, `gliheng/vite-plugin-rust` 등이 존재하지만, `Menci/vite-plugin-wasm` 을 기본으로 선택하는 이유는 Vite 2~7 광범위 호환 및 `--target bundler/web` 양쪽 지원 때문 (출처: https://github.com/nshen/vite-plugin-wasm-pack , https://github.com/rwasm/vite-plugin-rsw).

10. Tauri 2 (with-tauri 플래그 true 시)
    └─ pnpm add -D @tauri-apps/cli
    └─ pnpm tauri init (devUrl: http://localhost:5173, frontendDist: ../dist)
    └─ src-tauri/capabilities/default.json 최소 권한 세팅
    └─ (출처: https://v2.tauri.app/start/create-project/ , https://v2.tauri.app/start/frontend/vite/)

11. 테스트 도구
    └─ pnpm add -D vitest @testing-library/react @testing-library/jest-dom jsdom
    └─ pnpm add -D playwright @playwright/test

12. ESLint 9+ flat config + Prettier
    └─ pnpm add -D eslint typescript-eslint eslint-plugin-react eslint-plugin-react-hooks prettier
    └─ eslint.config.js 작성 (flat config 가 v9 기본값. legacy eslintrc 는 deprecated 이지만 여전히 동작)
    └─ (출처: https://eslint.org/blog/2025/05/eslint-v9.0.0-retrospective/ , https://typescript-eslint.io/getting-started/)

13. harness 초기화
    └─ /harness init 호출 → .harness/project.yaml 자동 생성

14. git 초기 커밋
    └─ git init && git add -A && git commit -m "chore: initial scaffold"
```

### 1.5 tsconfig 필수 옵션 (strict TypeScript)

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
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
```

### 1.6 Gotchas

- **pnpm workspace ↔ Cargo workspace 충돌** (커뮤니티 사례 기반, unverified 공식 문서): `pnpm-workspace.yaml` 의 `packages` 목록과 `Cargo.toml` 의 `workspace.members` 를 혼동하지 마라. 전자는 npm 패키지, 후자는 Rust crate. `crates/core` 는 두 파일 모두에 등재되어야 한다 (pnpm 은 Rust crate를 npm 패키지로 취급하지 않지만 경로 해석용). 공식 pitfall 문서는 찾지 못했으며 커뮤니티 사례를 기반으로 작성됨.
- **Tailwind v4 설치**: v3 문서의 `npx tailwindcss init` 은 v4 에서 **없어짐**. `@tailwindcss/vite` 플러그인과 `@import "tailwindcss";` 만 쓴다 (출처: https://tailwindcss.com/docs/upgrade-guide).
- **shadcn 패키지 리네임 (2024-08)**: 과거 `shadcn-ui` npm 패키지는 **2024년 8월부터 deprecated** 되고 `shadcn` 으로 리네임되었다. 과거 명령 `npx shadcn-ui@latest init` 은 더 이상 동작하지 않으며 현재는 `pnpm dlx shadcn@latest init --template vite` 를 사용한다 (출처: https://ui.shadcn.com/docs/changelog/2024-08-npx-shadcn-init).
- **shadcn + Tailwind v4 + React 19 조합**: 2026-04 기준 shadcn 이 Tailwind v4 와 React 19 를 공식 지원하지만, 업스트림 shadcn 이슈 트래커 (shadcn-ui/ui#6585) 에 해당 조합 관련 논의가 진행 중이므로 마이너 이슈 가능성 있음. 초기 설치 직후 `pnpm tsc --noEmit` 으로 타입 오류 점검 필수 (출처: https://github.com/shadcn-ui/ui/issues/6585).
- **next-themes + Vite**: next-themes 는 Next.js 중심 설계라 SSR 경고가 나올 수 있음. Vite 에선 client-only 모드로 쓰고 초기 테마를 `<html class="dark">` 로 SSR 없이 직접 설정하는 inline script 필요.
- **TanStack Router codegen**: `routeTree.gen.ts` 는 플러그인이 자동 생성. **수동 수정 금지** 이며 `.gitignore` 에 올릴지 커밋할지 팀 컨벤션. 기본은 **커밋 대상 제외** 를 권장 (merge conflict 최소화).
- **Strict TS 위반 거부**: 생성된 초기 파일에 `any`, `as`, `!` 가 포함되어 있으면 생성 실패로 간주하고 롤백. shadcn 일부 컴포넌트가 역사적으로 `any` 를 썼던 이력이 있으므로 설치 직후 `pnpm tsc --noEmit` 으로 검증 필수.
- **`eslint-plugin-react-hooks` flat config 수동 와이어링**: 2026-04 기준 `eslint-plugin-react-hooks` 의 flat config 지원이 공식 문서에 완전히 반영되지 않아 (facebook/react#28313 참조), `eslint.config.js` 에서 수동으로 `plugins: { 'react-hooks': reactHooks }` + `rules: reactHooks.configs.recommended.rules` 형태로 와이어링해야 한다. `/react-init` 스캐폴딩 템플릿은 이 수동 구성을 기본 포함한다 (출처: https://github.com/facebook/react/issues/28313).
- **Rust WASM crate-type**: `crates/core/Cargo.toml` 에 `crate-type = ["cdylib", "rlib"]` 둘 다 있어야 WASM 빌드와 네이티브 (Tauri) 재사용이 동시에 가능하다. `cdylib` 만 있으면 Tauri 쪽에서 import 불가.

### 1.7 Clean Architecture 배치

`/react-init` 은 디렉토리 스캐폴딩만 담당하며, 각 디렉토리 자체는 `.gitkeep` 으로 유지. 실제 파일은 다른 스킬들이 해당 레이어에 작성한다.

## 2. /react-screen — 화면 + 라우트 생성

기존 프로젝트에 새 화면 (또는 페이지) 을 추가하고 TanStack Router 파일 기반 라우트를 등록한다.

### 2.1 트리거

- 키워드: "화면 추가", "페이지 추가", "react-screen", "new screen", "route 추가"
- 조건: 이미 `/react-init` 으로 초기화된 프로젝트 (TanStack Router 플러그인 설치 확인)

### 2.2 입력

- `screen_name` (필수): PascalCase (예: `Dashboard`, `UserProfile`)
- `route_path` (선택, 기본값 = screen_name 을 kebab-case 로 변환): 예: `/dashboard`, `/users/$userId`
- `--lazy` (기본 true): 동적 import 로 코드 스플리팅
- `--with-loader` (기본 false): TanStack Router loader 함수 포함

### 2.3 TanStack Router 파일 기반 라우트 등록 절차

TanStack Router 의 플러그인은 `src/presentation/routes/` 아래 파일을 자동 스캔하여 `routeTree.gen.ts` 를 생성한다. 스킬은 다음 순서로 진행한다:

1. `src/presentation/routes/<path>.tsx` 파일 생성
   - `createFileRoute` 를 사용해 라우트 정의
   - 예: `createFileRoute('/dashboard')({ component: DashboardScreen })`
2. 화면 컴포넌트는 `src/presentation/features/<feature>/screens/<Name>Screen.tsx` 에 배치 (Clean Arch)
3. 라우트 파일에서는 screens 경로를 import 하여 얇게 위임
4. Vite dev server 실행 중이면 `tanstackRouter` 플러그인이 자동으로 `routeTree.gen.ts` 재생성
5. 수동 codegen 필요 시 `pnpm tsr generate`

### 2.4 Lazy load 패턴

```tsx
// src/presentation/routes/dashboard.tsx
import { createFileRoute, lazyRouteComponent } from '@tanstack/react-router'

export const Route = createFileRoute('/dashboard')({
  component: lazyRouteComponent(() =>
    import('@/presentation/features/dashboard/screens/DashboardScreen').then(
      (m) => ({ default: m.DashboardScreen }),
    ),
  ),
})
```

`autoCodeSplitting: true` 플러그인 옵션이 켜져 있으면 (`/react-init` 기본값) 수동 lazy 래핑 없이도 자동 분할. 하지만 스킬은 명시적 lazy 를 기본으로 생성한다 — intent 명확성.

### 2.5 Preloading

TanStack Router 는 hover/focus 이벤트에 사전 로드를 지원한다. `/react-init` 이 `<RouterProvider defaultPreload="intent" />` 로 설정 → 사용자가 링크 hover 시 비동기 로딩 시작.

### 2.6 Gotchas

- **라우트 파일명 prefix `-` 는 무시됨**: TanStack Router 플러그인 기본 설정이 `-` prefix 파일을 제외. 특수 파일 네이밍 시 주의.
- **`routeTree.gen.ts` 수동 수정 금지**: 플러그인이 덮어쓴다. 수정 필요하면 플러그인 옵션 조정.
- **route path 파라미터는 `$` prefix**: 예 `$userId` (Next.js 의 `[userId]` 와 다름).
- **중복 생성 방지**: 같은 이름의 파일이 이미 있으면 거부. `--force` 플래그로만 덮어쓴다.
- **strict TS**: `createFileRoute` 의 params 타입은 자동 추론됨. 사용자가 `as any` 로 타입을 우회하는 코드 생성 금지.

### 2.7 Clean Architecture 배치

- 라우트 정의 파일: `src/presentation/routes/`
- 화면 컴포넌트: `src/presentation/features/<feature>/screens/`
- 데이터 로드 (loader) 가 있으면 data 레이어의 UseCase 호출 → Route component 에서 `useLoaderData` 로 수신

## 3. /react-feature — 복합 4계층 생성

하나의 feature (예: auth, dashboard, settings) 를 구성하는 네 개 레이어 파일을 한 번에 생성한다. 화면 + 스토어 + UseCase + API 연동까지.

### 3.1 트리거

- 키워드: "feature 추가", "기능 추가", "react-feature", "새 기능"
- 조건: 프로젝트 초기화 완료 상태, feature 이름 지정 필수

### 3.2 입력

- `feature_name` (필수): kebab-case (예: `user-profile`, `payment-history`)
- `--with-api` (기본 true): 백엔드 API 연동 코드 포함
- `--with-route` (기본 true): 라우트 등록
- `--schema` (선택): Zod 스키마 파일 경로 or 인라인 정의

### 3.3 4계층 생성 순서 (의존성 그래프)

의존성 방향은 Clean Architecture 기본 규칙: **presentation → domain ← data**. 생성 순서는 의존성 역순 (안쪽부터) 으로 진행해야 참조 에러가 없다.

```
        ┌─────────────────────────────────┐
        │  1. domain/entities             │  (순수 TS + Zod 스키마)
        │     domain/failures             │
        └───────────┬─────────────────────┘
                    │  ↑ 의존
        ┌───────────┴─────────────────────┐
        │  2. domain/usecases             │  (인터페이스만)
        └───────────┬─────────────────────┘
                    │  ↑ 구현
        ┌───────────┴─────────────────────┐
        │  3. data/datasources/remote     │  (fetch + Zod parse)
        │     data/models                 │
        │     data/repositories           │
        └───────────┬─────────────────────┘
                    │  ↑ 주입
        ┌───────────┴─────────────────────┐
        │  4. presentation/features/<f>/  │
        │     ├── store.ts (Zustand)       │
        │     ├── hooks/useXxx.ts          │  (TanStack Query)
        │     ├── components/              │
        │     ├── screens/                 │
        │     └── index.ts (public API)    │
        └───────────┬─────────────────────┘
                    │  ↑ 라우트 등록
        ┌───────────┴─────────────────────┐
        │  5. presentation/routes/<f>.tsx │
        └─────────────────────────────────┘
```

### 3.4 세부 생성 흐름

1. **Domain 먼저**: `src/domain/entities/<feature>.ts` 에 Zod 스키마 + `z.infer` 타입 정의. `src/domain/failures/<feature>-failures.ts` 에 `<Feature>Failure` discriminated union.
2. **UseCase 인터페이스**: `src/domain/usecases/<feature>-usecases.ts` 에 함수 시그니처 (예: `fetchUser(id: string): Promise<Result<User, UserFailure>>`)
3. **Data 레이어**: `src/data/datasources/remote/<feature>-api.ts` (fetch), `src/data/models/<feature>-dto.ts` (Zod DTO), `src/data/repositories/<feature>-repository.ts` (UseCase 구현)
4. **Presentation 레이어**: Zustand store + TanStack Query hook + 화면 컴포넌트
5. **Route 등록**: `/react-screen` 내부 호출로 위임

### 3.5 Gotchas

- **경계에서 Zod parse 필수**: datasource 는 raw response 를 바로 return 하지 말고 `Schema.parse(json)` 로 검증 후 domain 타입으로 변환.
- **Store 는 feature 내부에서만 import**: 다른 feature 가 직접 참조하면 feature 간 결합. cross-feature 상태는 `src/presentation/shared/stores/` 로 승격.
- **Result 타입 일관**: 모든 UseCase 는 `neverthrow` 의 `Result<T, Failure>` 를 반환. throw 금지.
- **생성 실패 시 전체 롤백**: 5개 파일 중 하나라도 실패하면 지금까지 생성된 파일 모두 삭제.
- **Strict TS**: Zod `z.infer` 로 파생된 타입을 신뢰하고, 수동 interface 재정의 금지.

### 3.6 Clean Architecture 배치

위 3.3 다이어그램 참조. 각 레이어가 정해진 디렉토리에 배치된다.

## 4. /react-widget — shadcn 기반 재사용 컴포넌트

`src/presentation/shared/components/` 에 재사용 가능한 UI 컴포넌트를 생성한다. shadcn/ui 컴포넌트 위에 프로젝트 고유 variant 를 얹는 패턴.

### 4.1 트리거

- 키워드: "위젯 만들어줘", "컴포넌트 생성", "react-widget", "custom widget"
- 조건: shadcn/ui 가 초기화되어 있고 `components.json` 이 존재하는 프로젝트

### 4.2 입력

- `widget_name` (필수): PascalCase (예: `PrimaryButton`, `MetricCard`)
- `base` (선택): 기반으로 삼을 shadcn 컴포넌트 (예: `button`, `card`). 없으면 순수 컴포넌트 생성.
- `variants` (선택): variant 정의 (예: `{ variant: ['default', 'destructive'], size: ['sm', 'md', 'lg'] }`)

### 4.3 cva (class-variance-authority) variant 패턴

shadcn 컴포넌트는 대부분 `class-variance-authority` 를 써서 variant 를 선언한다. `/react-widget` 이 생성하는 코드는 이 패턴을 준수한다.

```tsx
// src/presentation/shared/components/primary-button.tsx
import * as React from 'react'
import { cva, type VariantProps } from 'class-variance-authority'
import { cn } from '@/presentation/shared/lib/utils'

const primaryButtonVariants = cva(
  'inline-flex items-center justify-center rounded-md font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 disabled:opacity-50 disabled:pointer-events-none',
  {
    variants: {
      variant: {
        default: 'bg-primary text-primary-foreground hover:bg-primary/90',
        destructive: 'bg-destructive text-destructive-foreground hover:bg-destructive/90',
      },
      size: {
        sm: 'h-8 px-3 text-sm',
        md: 'h-10 px-4',
        lg: 'h-12 px-6 text-lg',
      },
    },
    defaultVariants: {
      variant: 'default',
      size: 'md',
    },
  },
)

type PrimaryButtonProps = React.ButtonHTMLAttributes<HTMLButtonElement> &
  VariantProps<typeof primaryButtonVariants> & {
    loading?: boolean
  }

export const PrimaryButton = React.forwardRef<HTMLButtonElement, PrimaryButtonProps>(
  ({ className, variant, size, loading, children, ...props }, ref) => (
    <button
      ref={ref}
      className={cn(primaryButtonVariants({ variant, size }), className)}
      disabled={loading ?? props.disabled}
      {...props}
    >
      {loading ? 'Loading...' : children}
    </button>
  ),
)
PrimaryButton.displayName = 'PrimaryButton'
```

### 4.4 Props 타이핑 규칙

- **`React.FC` 금지**: 제네릭 추론이 약하고 children 이 암묵적으로 포함됨. 대신 `(props: Props) => JSX.Element` 또는 `forwardRef<Ref, Props>` 사용.
- **Props 타입은 `type` 으로 정의** (interface 아님): `VariantProps` 같은 유틸리티 타입과 교차 타입으로 조합하기 쉽다.
- **HTML 속성 확장**: 기본 HTML 속성을 그대로 통과시키려면 `React.ButtonHTMLAttributes<HTMLButtonElement>` 등으로 교차.
- **ref 는 `forwardRef`**: shadcn 표준. React 19 에서는 `ref` 를 prop 으로 받을 수도 있지만 shadcn 생태계 호환을 위해 forwardRef 유지.
- **`any` 금지 + `as` 금지**: strict TS 정책. 제네릭이 추론되지 않으면 명시적 타입 파라미터를 쓴다.

### 4.5 Container Queries 반응형

컴포넌트 단위 반응형은 전역 breakpoint 가 아니라 **container queries** 로 한다. Tailwind v4 에 `@container` 유틸리티 내장.

```tsx
<div className="@container">
  <div className="grid grid-cols-1 @md:grid-cols-2 @lg:grid-cols-3">
    ...
  </div>
</div>
```

`@md`, `@lg` 는 컨테이너 (부모 `@container`) 기준 breakpoint. 페이지 크기가 아니라 컴포넌트가 들어간 박스 크기에 반응. `/react-widget` 은 반응형 레이아웃 생성 시 container queries 를 기본으로 제안.

### 4.6 Gotchas

- **기존 shadcn 컴포넌트 직접 수정 금지**: shadcn 은 "코드 소유 (own your code)" 모델이라 수정이 가능하지만, `/react-widget` 은 래핑해서 확장한다. 직접 수정은 shadcn CLI 업데이트 시 충돌.
- **cn 유틸리티 경로**: `src/presentation/shared/lib/utils.ts` 의 `cn(...classes)` 를 import. `@/lib/utils` 처럼 다른 경로 쓰지 말 것 (Clean Arch 준수).
- **container queries + Tailwind v4 버전**: Tailwind v4 부터 `@container` 내장. v3 에서는 별도 플러그인 필요하므로 프로젝트 Tailwind 메이저 버전 확인 후 사용.
- **displayName 필수**: forwardRef 컴포넌트는 `displayName` 설정 필수 — React DevTools 디버깅 용이성.
- **Props 에 onClick 재정의 금지**: HTML 속성에 이미 `onClick` 이 있으므로 Props 타입에서 덮어쓰면 타입 충돌. 필요하면 `onClick?: (e: React.MouseEvent<HTMLButtonElement>) => void` 명시적으로 다시 선언.
- **Strict TS 위반 거부**: cva 반환 타입을 `any` 로 캐스팅하는 코드 생성 금지.

### 4.7 Clean Architecture 배치

- 재사용 위젯: `src/presentation/shared/components/<kebab-name>.tsx`
- shadcn 원본: `src/presentation/shared/components/ui/` (수정 금지)
- cn 헬퍼: `src/presentation/shared/lib/utils.ts`

## 5. 공유 References — project-detection.md

4개 스킬이 모두 공유하는 프로젝트 감지 규칙. `react-kit/references/project-detection.md` 에 별도 문서로 작성 (G1 스킬 구현 시 생성 대상).

이 문서는 아래 항목을 감지한다:
- Node 버전 (`.nvmrc` 또는 `package.json` `engines.node`)
- pnpm 버전 (`packageManager` 필드)
- React 버전 (`package.json` `dependencies.react`)
- Vite 설치 여부 + 메이저 버전
- Tailwind 메이저 버전 (v3 vs v4 — 설치 명령 다름)
- shadcn 초기화 여부 (`components.json` 존재)
- TanStack Router 플러그인 설치 여부
- Cargo workspace 존재 여부 (`Cargo.toml` 루트)
- strict TypeScript 설정 여부

## 6. 다른 그룹과의 재사용 관계

- **G2 (상태 & 데이터)** 는 `/react-feature` 에서 생성한 skeleton 을 확장. `/react-store`, `/react-api`, `/react-query`, `/react-form` 이 개별 레이어 강화.
- **G3 (고성능)** 의 `/react-wasm` 은 `crates/core/` (G1 `/react-init` 생성) 를 전제로 한다.
- **G4 (품질)** 의 `/react-test` 는 `/react-feature` 산출 파일 전부에 대한 테스트 생성.
- **G5 (UI 패턴)** 의 `/react-responsive`, `/react-skeleton`, `/react-extract` 는 `/react-widget` 생성물 위에서 동작.
- **G6 (빌드 & 감사)** 의 `/react-audit` 은 `/react-init` 설정 (strict TS, eslint flat, Tailwind v4) 을 기준선으로 위반을 검출.

공용 helpers:
- `react-kit/references/project-detection.md` (4개 스킬 공유)
- `react-kit/references/clean-arch-layout.md` (레이어 배치 규칙)
- `react-kit/templates/tsconfig.template.json`, `eslint.config.template.js`, `vite.config.template.ts`

## 7. 출처 요약

1. Tailwind CSS v4 Vite 설치 가이드: https://tailwindcss.com/docs/guides/vite
2. Tailwind CSS v4 릴리스 노트: https://tailwindcss.com/blog/tailwindcss-v4
3. Tailwind CSS v3 → v4 업그레이드 가이드: https://tailwindcss.com/docs/upgrade-guide
4. shadcn/ui Vite 설치 가이드: https://ui.shadcn.com/docs/installation/vite
5. shadcn/ui CLI 문서: https://ui.shadcn.com/docs/cli
6. TanStack Router Vite 설치 가이드: https://tanstack.com/router/latest/docs/installation/with-vite
7. Tauri 2 프로젝트 생성 가이드: https://v2.tauri.app/start/create-project/
8. Tauri 2 + Vite 통합 문서: https://v2.tauri.app/start/frontend/vite/
9. Menci/vite-plugin-wasm (Vite 2~7 지원): https://github.com/Menci/vite-plugin-wasm
10. shadcn/ui 2024-08 CLI 리네임 changelog: https://ui.shadcn.com/docs/changelog/2024-08-npx-shadcn-init
11. shadcn/ui Tailwind v4 + React 19 호환 이슈: https://github.com/shadcn-ui/ui/issues/6585
12. ESLint v9 플랫 컨피그 retrospective: https://eslint.org/blog/2025/05/eslint-v9.0.0-retrospective/
13. typescript-eslint 플랫 컨피그 getting-started: https://typescript-eslint.io/getting-started/
14. eslint-plugin-react-hooks 플랫 컨피그 이슈: https://github.com/facebook/react/issues/28313
15. 대안 Vite WASM 플러그인 비교: https://github.com/nshen/vite-plugin-wasm-pack , https://github.com/rwasm/vite-plugin-rsw

## 8. 변경 이력

- **2026-04-10** — 초판. G1 4개 스킬 (`/react-init`, `/react-screen`, `/react-feature`, `/react-widget`) 상세 설계. Codex 리서치 두 차례 중단/정체로 WebSearch fallback 사용하여 Tailwind v4, shadcn CLI, TanStack Router 플러그인, Tauri 2, vite-plugin-wasm 핵심 명령 및 공식 문서 URL 검증.
- **2026-04-10 (보강)** — G1 문서 vs 추가 WebSearch 비교 결과 6개 보강사항 적용: shadcn 패키지 리네임 2024-08 시점 명시, 대안 WASM 플러그인 3종 언급, ESLint v9 flat config "필수"→"default" 완화, eslint-plugin-react-hooks 수동 와이어링 경고, shadcn+Tailwind v4+React 19 호환 이슈 경고, pnpm+Cargo workspace pitfall unverified 표기. 출처 URL 6개 추가.
