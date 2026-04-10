# react-kit

React + Vite + Tauri 2 + Rust WASM 전용 개발 워크플로우 플러그인.

## 개요

성능 우선 Clean Architecture React 모노레포를 스캐폴딩하고,
상태/데이터/UI 패턴/테스트/감사까지 21개 스킬 + 3 에이전트로 자동화.
Motion/dnd-kit 등 외부 애니메이션 라이브러리를 0개 사용하는 pure 구현 원칙.

핵심 기술: Vite 5+, Tauri 2, TypeScript strict, Tailwind v4, shadcn/ui,
TanStack Router, TanStack Query v5, Zustand, React Hook Form + Zod,
neverthrow, Lingui v5, Vitest + Testing Library + Playwright, wasm-pack.

<!-- AUTO:skills -->
| 스킬 | 설명 |
|------|------|
| `react-animation` | React 컴포넌트에 애니메이션을 추가한다. 외부 라이브러리 없이 |
| `react-api` | REST/GraphQL 엔드포인트를 domain → data → datasource → repository → usecase 4계층으로 일괄 또는 개별 생성한다. |
| `react-audit` | 코드 품질 감사. quick 모드(단일 에이전트, 빠른 로컬 검토)와 deep 모드(최대 4 에이전트 병렬 감사)를 지원한다. |
| `react-build` | 전체 빌드 파이프라인을 실행한다. wasm-pack → tsc → vite build 순서. |
| `react-error` | 데이터 경계의 예외를 Failure로 변환하고, React Error Boundary로 렌더 에러를 포획하며, Severity에 따라 UI 표시를 분기하는 3단계 에러 처리 패턴을 세팅한다. |
| `react-extract` | feature 내부에 사유화되거나 중복된 컴포넌트를 감지하여 presentation/shared/components/로 추출한다. |
| `react-feature` | 하나의 feature를 구성하는 domain/data/presentation/infrastructure 4계층 파일을 한 번에 생성한다. |
| `react-form` | React Hook Form + Zod를 통합한 폼 컴포넌트를 생성한다. |
| `react-init` | Vite + Tauri 2 + React + TypeScript strict + Tailwind v4 + shadcn/ui + TanStack Router 스택으로 |
| `react-l10n` | Lingui v5 매크로 기반으로 번역 문자열을 추가하고 codegen 흐름을 자동화한다. |
| `react-preflight` | Pre-commit quality gate. 커밋 전 전체 검증을 순서대로 실행한다. |
| `react-query` | /react-api가 생성한 repository를 감싸는 TanStack Query v5 훅(useQuery·useMutation)을 생성한다. |
| `react-responsive` | 기존 화면/컴포넌트에 반응형 레이아웃을 적용한다. |
| `react-run` | React 빌드 프리미티브를 개별 실행한다. |
| `react-screen` | 기존 React 프로젝트에 새 화면(Page)을 추가하고 TanStack Router 파일 기반 라우트를 등록한다. |
| `react-skeleton` | TanStack Query isPending 상태에 맞춰 실 레이아웃 모양의 shadcn Skeleton shimmer를 구현한다. |
| `react-store` | feature별 또는 전역 Zustand 스토어와 selector 훅을 생성한다. |
| `react-tauri` | Tauri 2 Rust command를 정의하고 TS invoke 래퍼 + capabilities 등록까지 3-tier로 자동 생성한다. |
| `react-test` | 대상 파일/클래스를 분석하여 테스트 코드를 자동 생성한다. |
| `react-wasm` | Rust 함수를 WebAssembly로 컴파일하고 Comlink Worker + Clean Architecture 데이터 레이어 바인딩까지 자동 생성한다. |
| `react-widget` | shadcn/ui 컴포넌트를 기반으로 cva variant + Container Queries를 갖춘 재사용 UI 컴포넌트를 생성한다. |
<!-- /AUTO:skills -->

<!-- AUTO:agents -->
| 에이전트 | 설명 |
|----------|------|
| `animation-architect-react` | React 애니메이션 구현 전에 Tier 판정, 권장 전략, 접근성 검토를 자문한다. |
| `react-reviewer` | React 코드베이스를 6개 카테고리 기준으로 독립 평가한다. |
| `widget-inspector-react` | React 프로젝트 코드에서 재사용 가능한 컴포넌트 패턴을 감지하고 리포팅한다. |
<!-- /AUTO:agents -->

## Quickstart

```bash
# 1. 새 프로젝트 초기화
/react-init my-app

# 2. harness 세팅
cd my-app
/harness init

# 3. 첫 feature 생성
/react-feature user-profile

# 4. API 연동
/react-api User

# 5. 고성능 이미지 처리 (WASM)
/react-wasm "이미지 리사이즈"

# 6. 커밋 전 검증
/react-preflight
```

## Architecture

이 플러그인이 생성하는 프로젝트는 Clean Architecture 를 따른다:

```
src/
├── domain/              # entities, usecases, failures (순수)
├── data/                # datasources, models, repositories
├── presentation/        # features, shared, routes, styles
└── infrastructure/      # tauri, storage, http, i18n

crates/core/             # Rust 코어 (WASM + Tauri 네이티브 공유)
src-tauri/               # Tauri 백엔드
```

상세 설계는 `docs/react/kit-design/g1-scaffolding.md` ~ `g6-build-audit.md` 참조.

## 주요 철학

1. **성능 우선**: 번들 크기와 런타임 성능을 모든 결정의 1순위 판단 기준
2. **라이브러리 0개 애니메이션**: Motion/dnd-kit/react-spring 금지, 네이티브 브라우저 API + 커스텀 primitives
3. **Clean Architecture**: flutter-toolkit, rust-kit 과 일관된 레이어 분리
4. **Strict TypeScript**: any/as/! 금지, Zod 경계 검증 필수
5. **Result 타입**: throw 금지, neverthrow Result<T, Failure> 로 타입 안전 에러
6. **WASM 결정은 카탈로그 기반**: 측정 없이도 research-backed 판정 (G0 wasm-catalog.md)
