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
## 스킬 (21종)

### G1 — 스캐폴딩 & 생성
| 스킬 | 용도 |
|------|------|
| `/react-init` | Vite + Tauri + WASM + shadcn + TanStack Router + Zustand 풀 스캐폴딩 |
| `/react-screen` | 화면 + TanStack Router 파일 기반 라우트 등록 |
| `/react-feature` | 복합 (화면 + 스토어 + UseCase + API) 4계층 skeleton |
| `/react-widget` | shadcn/ui 기반 cva + forwardRef 재사용 컴포넌트 |

### G2 — 상태 & 데이터
| 스킬 | 용도 |
|------|------|
| `/react-store` | Zustand 스토어 + selector hooks + WASM 외부 접근 |
| `/react-api` | Clean Arch 4계층 (datasource → model → repo → usecase) |
| `/react-query` | TanStack Query v5 useQuery/useMutation + invalidation |
| `/react-form` | React Hook Form + Zod resolver + Result 반환 |

### G3 — 고성능 레이어
| 스킬 | 용도 |
|------|------|
| `/react-wasm` | Rust → wasm-pack → Comlink Worker → Clean Arch 바인딩 (G0 카탈로그 기반 자동 판정) |
| `/react-tauri` | Tauri command + invoke + capabilities + isTauri 가드 |

### G4 — 품질 & 패턴
| 스킬 | 용도 |
|------|------|
| `/react-test` | Vitest unit + Testing Library + Playwright 생성 |
| `/react-error` | throw → Failure → Severity → UI 매핑 + Error Boundary |
| `/react-l10n` | Lingui v5 매크로 + codegen + locale 전환 |

### G5 — UI 패턴
| 스킬 | 용도 |
|------|------|
| `/react-responsive` | Tailwind breakpoint + container queries 자동 판정 |
| `/react-skeleton` | shadcn Skeleton shimmer + TanStack Query isPending 분기 |
| `/react-extract` | 중복 위젯 감지 → shared 추출 → import 자동 수정 |

### G5b — 애니메이션 (pure, no-library)
| 스킬 | 용도 |
|------|------|
| `/react-animation` | Tailwind / View Transitions API / 커스텀 pointer primitives 3-tier 자동 판정 |

### G6 — 빌드 & 감사
| 스킬 | 용도 |
|------|------|
| `/react-run` | 빌드 프리미티브 개별 실행 (dev, build, lint, tsc, test, wasm-build, codegen, format) |
| `/react-build` | 전체 빌드 파이프라인 (wasm-pack → tsc → vite) |
| `/react-preflight` | pre-commit quality gate (fix → codegen → lint → tsc → test → wasm → build → audit) |
| `/react-audit` | quick/deep 모드 + 4 병렬 에이전트 축 + 34 규칙 grep/AST 검사 |
<!-- /AUTO:skills -->

<!-- AUTO:agents -->
## 에이전트 (3종)

| 에이전트 | 용도 |
|---------|------|
| `react-reviewer` | `/react-audit` 에서 호출되는 독립 평가 에이전트 (Architecture/Performance/Accessibility/LibraryPolicy 4축) |
| `widget-inspector-react` | 중복 위젯 / 사유화 재사용 가능 컴포넌트 감지 |
| `animation-architect-react` | 복잡 애니메이션 설계 자문 (Tier 1/2/3 판정 + 엣지케이스) |
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
