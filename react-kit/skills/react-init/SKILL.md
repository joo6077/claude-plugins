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
2. **Tailwind v4 설치 방식 변경** — v3 문서의 `npx tailwindcss init`은 v4에서 없어짐. `@tailwindcss/vite` 플러그인과 `@import "tailwindcss";` 만 사용한다.
3. **shadcn 패키지 리네임 (2024-08)** — `shadcn-ui` npm 패키지는 deprecated. 현재는 `pnpm dlx shadcn@latest init --template vite`를 사용한다.
4. **shadcn + Tailwind v4 + React 19 조합** — 초기 설치 직후 `pnpm tsc --noEmit`으로 타입 오류 점검 필수. 업스트림 이슈(shadcn-ui/ui#6585) 주시.
5. **next-themes + Vite** — SSR 경고 발생 가능. client-only 모드로 사용하고 초기 테마를 `<html class="dark">`로 inline script로 설정.
6. **TanStack Router codegen** — `routeTree.gen.ts`는 플러그인이 자동 생성하므로 수동 수정 금지. 기본적으로 `.gitignore` 제외 권장(merge conflict 최소화).
7. **Strict TS 위반 거부** — 생성된 초기 파일에 `any`, `as`, `!`가 포함되면 생성 실패로 간주하고 롤백. `pnpm tsc --noEmit`으로 검증 필수.
8. **`eslint-plugin-react-hooks` flat config 수동 와이어링** — `eslint.config.js`에서 `plugins: { 'react-hooks': reactHooks }` + `rules: reactHooks.configs.recommended.rules` 형태로 수동 구성 필요(facebook/react#28313).
9. **Rust WASM crate-type** — `crates/core/Cargo.toml`에 `crate-type = ["cdylib", "rlib"]` 둘 다 있어야 WASM 빌드와 Tauri 네이티브 재사용이 동시에 가능하다.
10. **기존 파일 overwrite 금지** — 같은 이름의 파일/디렉토리가 이미 존재하면 생성을 거부한다. `--force` 플래그가 있을 때만 덮어쓴다.
11. **실패 시 전체 롤백** — 복수 파일 생성 중 하나라도 실패하면 스킬 실행으로 생성된 파일을 모두 삭제하고 원상복구한다.
12. **하드코딩된 버전 번호 금지** — 의존성 설치 시 `pnpm add <package>@latest`로 최신 버전을 받는다. 특정 패치 버전을 고정하지 않는다.

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

### 단계 3 — Tailwind CSS v4 (Vite 플러그인)

```bash
pnpm add -D tailwindcss @tailwindcss/vite
```

`src/presentation/styles/globals.css` 생성:
```css
@import "tailwindcss";
```

`vite.config.ts`에 `tailwindcss()` 플러그인 추가.

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

### 단계 7 — i18n (Lingui)

```bash
pnpm add @lingui/react @lingui/core
pnpm add -D @lingui/cli @lingui/vite-plugin @lingui/macro
```

`lingui.config.ts` 작성.

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

### 단계 10 — Tauri 2 (`--with-tauri` true 시)

```bash
pnpm add -D @tauri-apps/cli
pnpm tauri init
# devUrl: http://localhost:5173, frontendDist: ../dist
# src-tauri/capabilities/default.json 최소 권한 세팅
```

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

```
/harness init 호출 → .harness/project.yaml 자동 생성
```

### 단계 14 — git 초기 커밋

```bash
git init && git add -A && git commit -m "chore: initial scaffold"
```

## 4. 산출 파일 구조

```
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
