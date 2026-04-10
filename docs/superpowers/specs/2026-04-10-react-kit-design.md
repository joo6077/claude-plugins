# react-kit 플러그인 설계 Spec

```yaml
created: 2026-04-10
status: approved (6/6 sections APPROVE via qa-evaluator)
author: Jackson Kim
brainstormed_with: Claude (session 2026-04-10)
scope: claude-plugins 모노레포에 추가할 신규 플러그인 react-kit 의 전체 설계
```

## 1. 배경 & 목표

이 레포 (`claude-plugins`) 에 **React 전용 개발 워크플로우 플러그인** `react-kit` 을 추가한다. 기존 `flutter-toolkit`, `rust-kit` 과 같은 패턴 — Clean Architecture, Strict 타입, 풍부한 스킬 + 감사 사이클 — 이지만 React 생태계 고유 특성 (Vite, Tauri 2, WASM, TypeScript) 에 맞춰 재설계.

**핵심 요구사항** (사용자 최우선 순위):

1. **성능 우선** — 번들 크기, 런타임 속도가 모든 결정의 1순위 판단 기준
2. **WebAssembly 통합** — "WASM 으로 처리할 수 있는 건 WASM 으로" 원칙. Rust → wasm-pack → React 바인딩 전체 파이프라인 자동화
3. **반응형** — 페이지 breakpoint + 컴포넌트 container queries 조합
4. **데스크탑 앱 + 웹** 동시 타겟 — 같은 React 소스가 웹 배포와 Tauri 데스크탑 양쪽에서 동작
5. **Strict TypeScript** — `any`, `as`, `!` non-null 단언 금지. Zod 경계 검증 필수
6. **라이브러리 0개 애니메이션** — Motion / framer-motion / dnd-kit / react-spring 전면 금지. Tailwind + View Transitions API + 커스텀 pointer primitives 만 사용 (커스텀 유연성 최대화)
7. **다크모드 기본 포함** (Tailwind v4 `dark:` + shadcn/ui CSS variables)

## 2. 기술 스택 (확정)

| 영역 | 선택 | 근거 |
|------|------|------|
| 빌드 도구 | **Vite 5+** + `@vitejs/plugin-react-swc` | 가장 빠른 개발 서버, Tauri 와 자연 통합 |
| 데스크탑 런타임 | **Tauri 2.10+** (2024-10 stable) | 번들 ~3MB, rust-kit 과 Rust 코어 공유 가능 |
| UI 프레임워크 | **React 19** | Server Components 미사용 (Tauri 호환) |
| 타입 | **TypeScript strict 최대치** (7개 옵션 + ESLint 엄격) | 사용자 요구사항 |
| 스타일 | **Tailwind CSS v4** + `@tailwindcss/vite` | Rust 기반 엔진, container queries 내장 |
| 컴포넌트 | **shadcn/ui** (CLI: `pnpm dlx shadcn@latest init --template vite`) | 코드 소유 모델, 다크모드 기본 |
| 라우팅 | **TanStack Router** + `@tanstack/router-plugin` | 타입 안전, 파일 기반, autoCodeSplitting |
| 상태 (클라이언트) | **Zustand v5** (`create<T>()(...)` 패턴) | 경량, React 외부 접근 가능 (WASM 콜백) |
| 상태 (서버) | **TanStack Query v5** | 캐시 + invalidation 표준 |
| 폼 | **React Hook Form** + **Zod resolver** | 사실상 독점 |
| 에러 | **neverthrow Result<T, Failure>** + Error Boundary | throw 금지, 타입 안전 |
| i18n | **Lingui v5** 매크로 (`@lingui/react/macro`) | 타입 안전, 번들 작음 |
| 테스트 | **Vitest** (unit) + **Testing Library** (component) + **Playwright** (e2e) | Vite 네이티브 |
| 패키지 매니저 | **pnpm** workspace | 단일 선택, monorepo 관리 |
| Rust 코어 | **crates/core/** (`crate-type = ["cdylib", "rlib"]`) | WASM + Tauri 네이티브 양쪽 재사용 |
| WASM 파이프라인 | **wasm-pack** + **Menci/vite-plugin-wasm** + `vite-plugin-top-level-await` | Vite 2~7 호환, `--target web` |
| 애니메이션 | **Tailwind + View Transitions API + 커스텀 pointer primitives** | **라이브러리 0개 원칙** |

## 3. 아키텍처 — Clean Architecture 모노레포

```
my-app/
├── package.json                       # pnpm workspace root
├── pnpm-workspace.yaml
├── Cargo.toml                          # Rust workspace root (crates/core + src-tauri)
├── tsconfig.json                       # strict: true + 7개 엄격 옵션
├── vite.config.ts                      # React + Tailwind v4 + TanStack Router + WASM 플러그인
├── tailwind.config.ts                  # design tokens
├── eslint.config.js                    # flat config v9+
├── lingui.config.ts
│
├── src/
│   ├── domain/                         # entities, usecases, failures, types (순수 TS + Zod)
│   ├── data/                           # datasources/{remote,local,wasm}/, models, repositories
│   ├── presentation/
│   │   ├── features/<feature>/         # components/ hooks/ store.ts screens/
│   │   ├── shared/components/ui/       # shadcn 원본
│   │   ├── shared/components/          # 공용 위젯
│   │   ├── shared/hooks/               # useDrag, useDrop, useSortable, use-view-transition
│   │   ├── shared/stores/              # drag-store 등
│   │   ├── shared/lib/utils.ts         # cn 헬퍼
│   │   ├── routes/                     # TanStack Router 파일 라우트
│   │   └── styles/globals.css          # @import "tailwindcss";
│   ├── infrastructure/
│   │   ├── tauri/                      # invoke 래퍼 (isTauri 가드)
│   │   ├── storage/
│   │   ├── http/
│   │   └── i18n/
│   └── wasm/                           # wasm-pack 산출물 (gitignored)
│
├── src-tauri/                          # Tauri 백엔드
│   ├── Cargo.toml
│   ├── tauri.conf.json
│   ├── capabilities/default.json
│   └── src/commands/                   # Tauri commands
│
├── crates/core/                        # 고성능 Rust 코어 (WASM + 네이티브 공유)
│   ├── Cargo.toml
│   └── src/lib.rs
│
├── tests/
│   ├── unit/ component/ e2e/
│
└── .harness/project.yaml               # /react-init 이 자동 생성
```

**Clean Arch 엄격 규칙**:
- `domain/` → 외부 의존성 0개. `data/`, `presentation/`, `infrastructure/`, WASM, Tauri 모두 모름
- `data/` → `domain/` 만 알고, `presentation/` 을 모름
- `presentation/features/a` → `features/b` 직접 참조 금지 (공유는 `shared/` 나 `domain/` 경유)
- `infrastructure/tauri/` → 유일한 `@tauri-apps/*` import 위치 (나머지는 `isTauri()` 가드 통과 필수)
- `/react-audit` 이 이 경계 위반을 grep/AST 로 검출 + 빌드 게이트

## 4. 스킬 인벤토리 — 21 스킬 + 3 에이전트

6개 그룹으로 조직. 각 그룹은 sprint-contract → WebSearch 리서치 → 상세 설계 문서 → qa-evaluator APPROVE 사이클로 설계 완료.

| 그룹 | 스킬 수 | 스킬 | 상세 문서 |
|------|--------|------|----------|
| **G1 스캐폴딩 & 생성** | 4 | `/react-init`, `/react-screen`, `/react-feature`, `/react-widget` | [g1-scaffolding.md](../../react/kit-design/g1-scaffolding.md) (525 줄) |
| **G2 상태 & 데이터** | 4 | `/react-store`, `/react-api`, `/react-query`, `/react-form` | [g2-state-data.md](../../react/kit-design/g2-state-data.md) (653 줄) |
| **G3 고성능 레이어** | 2 | `/react-wasm`, `/react-tauri` | [g3-performance.md](../../react/kit-design/g3-performance.md) (519 줄) |
| **G4 품질 & 패턴** | 3 | `/react-test`, `/react-error`, `/react-l10n` | [g4-quality.md](../../react/kit-design/g4-quality.md) (665 줄) |
| **G5 UI 패턴** | 3 | `/react-responsive`, `/react-skeleton`, `/react-extract` | [g5-ui-patterns.md](../../react/kit-design/g5-ui-patterns.md) (418 줄) |
| **G5b 애니메이션 (pure)** | 1 | `/react-animation` | [g5b-animation.md](../../react/kit-design/g5b-animation.md) (983 줄) |
| **G6 빌드 & 감사** | 4 | `/react-run`, `/react-build`, `/react-preflight`, `/react-audit` | [g6-build-audit.md](../../react/kit-design/g6-build-audit.md) (527 줄) |

**에이전트 3종** (읽기 전용):

| 에이전트 | 소속 | 역할 |
|---------|------|------|
| `widget-inspector-react` | G5 | 중복 위젯 / 사유화 재사용 가능 컴포넌트 감지. G6 deep 모드의 5번째 병렬 축으로도 재사용 |
| `animation-architect-react` | G5b | 복잡 애니메이션 설계 자문. Tier 1/2/3 판정 + 엣지케이스 리포트 |
| `react-reviewer` | G6 | `/react-audit` 의 독립 평가 에이전트. Deep 모드에서 4개 축 (architecture / performance / accessibility / library-policy) 으로 병렬 spawn |

**총 줄수**: 약 4,790+ 줄 상세 설계 문서

## 5. WASM 결정 프레임워크 (G0)

별도 단일 문서: [docs/react/wasm-catalog.md](../../react/wasm-catalog.md) (521 줄)

`/react-wasm` 스킬은 사용자에게 벤치마크를 요구하지 않는다. 대신 **리서치 기반 카탈로그** 로 카테고리별 사전 판정:

- **§1 WASM 권장 9개 카테고리** — 이미지, 비디오 코덱, 압축 (lz4 2.9x~25x), ML 추론 (SIMD 2.6x), SQL/DB (DuckDB-Wasm), 복잡 파서, 수치/FFT, 대용량 집계, bulk 암호화. 각 항목에 프로덕션 사례 (Figma 29s→8s, Squoosh, ffmpeg.wasm 등) 와 primary source URL
- **§2 WASM 비권장 10개 카테고리** — UI 상태, 폼 검증, JSON 파싱, 문자열 처리, Web Crypto 소규모, 고빈도 콜백, tiny 함수, 애니메이션, 네트워크, event bus
- **§3 Boundary cost** — JS↔WASM 호출 50~100 ns, 문자열 마샬링 600~2500 ns, ArrayBuffer transfer zero-copy
- **§4 SIMD + Threads** 2026-04 현황 (Chrome/Safari/Firefox 144+ Baseline)
- **§5 5개 휴리스틱** — 카탈로그 미스 시 판정 (데이터 크기 / 호출 빈도 / 반복 루프 / 외부 접근 / SIMD 활용성)
- **§6 5가지 오해 교정** — "React 로직 WASM 이면 빠르다" 등
- **§10 Rust 크레이트 매핑** — `image`, `lz4_flex`, `pulldown-cmark`, `tract`, `prost` 등

`/react-wasm` 은 이 카탈로그를 1차 소스로 사용. `/react-audit` Performance 카테고리도 참조.

## 6. 애니메이션 철학 — 라이브러리 0개 (G5b)

별도 단일 문서: [docs/react/kit-design/g5b-animation.md](../../react/kit-design/g5b-animation.md) (983 줄)

**금지 라이브러리**: `motion`, `framer-motion`, `react-spring`, `@formkit/auto-animate`, `@dnd-kit/*`, `react-dnd`, `gsap`, `lottie-react`, `animate.css`

**3-Tier 구조**:

- **Tier 1 — Tailwind + CSS** (0KB) — fade/slide/scale/transition, `tailwindcss-animate` (shadcn 기본)
- **Tier 2 — View Transitions API** (2026-01 Baseline) — `document.startViewTransition`, `view-transition-name`, 그리드↔보드 뷰 전환, shared element, 라우트 전환
- **Tier 3 — 커스텀 pointer primitives** — `useDrag` (FSM: idle/dragging/dropping), `useDrop` (Zustand drag-store 연동), `useSortable`, `Connector` (SVG 화살표). Pointer Events API + setPointerCapture + `touch-action: none`

**복잡 시나리오 커버**:
- 그리드 ↔ 보드 뷰 전환 (Tier 2)
- 칸반 드래그앤드롭 전체 코드 (Tier 3)
- SVG 화살표 노드 연결 (Tier 3)

**트레이드오프 명시**: 키보드 / ARIA / 스크린리더 접근성은 **사용자 책임**. `/react-animation` 이 W3C APG 기반 패턴 템플릿을 제공하지만 완벽한 a11y 를 자동 보장하지 않음.

## 7. harness 통합 & 플러그인 deliverables

별도 단일 문서: [docs/react/kit-design/final-integration.md](../../react/kit-design/final-integration.md) (490 줄)

**주요 산출물**:

- **`.harness/project.yaml` 템플릿** — stack: react, commands (pnpm tsc/eslint/vitest/prettier/codegen), 6개 contract_categories (Architecture / StrictType / Performance / Accessibility / LibraryPolicy / Testing), 9개 anti_patterns (grep 패턴), runtime_inspection (vm_port 5173)
- **`react-kit/.claude-plugin/plugin.json`** — name, version 0.1.0, author, description, keywords
- **react-kit/ 폴더 구조** — skills/(21), agents/(3), references/(5), templates/(9), evals/(5 fixtures), scripts/
- **`.claude-plugin/marketplace.json`** 엔트리 — `[v0.1.0 · 2026-04-10] ...` 접두사 포맷
- **`scripts/release.sh`** 수정 불필요 — 기존 sed 패턴 재사용
- **`react-kit/README.md`** — 기존 flutter-toolkit/rust-kit README 구조 모방, `<!-- AUTO:skills -->` 마커로 sync-docs.py 호환

**docs/react/ vs react-kit/ 역할 분리**:
- `react-kit/` → 배포 대상 (플러그인 이용자가 받음)
- `docs/react/` → 레포 개발용 내부 문서 (리서치 + 설계). `/react-kaizen` 이 주기 갱신
- 두 위치의 동기화는 카이젠 루프가 담당

## 8. 모든 6개 그룹의 QA 판정

| 설계 문서 | QA 판정 | Iterations | 조건 |
|----------|--------|------------|------|
| wasm-catalog.md (G0) | ✅ APPROVE | 2 | 14 + 4 |
| g1-scaffolding.md | ✅ APPROVE | 1 | 13 + 4 |
| g2-state-data.md | ✅ APPROVE | 2 | 14 + 4 |
| g3-performance.md | ✅ APPROVE | 1 | 15 + 4 |
| g4-quality.md | ✅ APPROVE | 1 | 14 + 4 |
| g5-ui-patterns.md | ✅ APPROVE | 1 | 13 + 4 |
| g5b-animation.md | ✅ APPROVE | 3 | 16 + 4 |
| g6-build-audit.md | ✅ APPROVE | 2 | 16 + 4 |
| final-integration.md | ✅ APPROVE | 1 | 16 + 4 |

**총 조건**: 131 + 36 (Diagnostics) = 167 개, 전부 PASS. 세 번의 iteration 을 거친 것은 g5b-animation (FSM `dropping` 상태 + useDrop 패턴 + Kanban 통합 코드 보강).

## 9. 결정 근거 — 주요 판단들

### 왜 Tauri 2 인가 (Electron 아님)

- 번들 ~3MB vs Electron ~100MB+
- Rust 백엔드 → rust-kit 의 스킬 + crates/core/ 재사용
- WASM 에서 같은 Rust 코드 공유 가능 (고성능 코드 중복 제거)
- 성능 우선 원칙에 정렬

### 왜 Vite 인가 (Next.js 아님)

- Tauri 가 정적 dist/ 를 로드 → SSR 불필요
- 웹 배포도 정적 배포면 SEO/서버 없이 가능
- WASM 번들링 공식 지원 (`vite-plugin-wasm`)
- Next.js 의 SSR / Server Components 는 Tauri 호환성 떨어뜨림

### 왜 Zustand 인가 (Jotai/Redux 아님)

- React 외부 접근 (`useStore.getState()`, `setState()`) → WASM Worker 콜백에서 직접 상태 갱신 가능
- 경량 (~1KB), 보일러플레이트 최소
- 2025~2026 커뮤니티 1순위

### 왜 Clean Architecture 인가 (Feature-sliced 아님)

- flutter-toolkit, rust-kit 과 일관된 멘탈 모델 — 킷 간 점프 시 인지 부하 최소
- `domain/` 이 WASM 공유 타입을 자연스럽게 배치하는 곳
- 사용자 선택 (사용자가 "flutter/rust 와 같은 구조" 를 명시적 선호)

### 왜 라이브러리 0개 애니메이션인가

- 성능 우선 원칙에 완벽히 정렬 (번들 0KB)
- 사용자가 커스텀 유연성 강조
- View Transitions API (2026-01 Baseline) 이 과거 라이브러리 역할의 상당 부분을 네이티브로 해결
- 드래그앤드롭 a11y 는 사용자 책임으로 명시 트레이드오프 수용

## 10. 알려진 트레이드오프 / 리스크

- **드래그앤드롭 접근성**: `@dnd-kit` 같은 라이브러리 없이 완벽한 키보드 + 스크린리더 a11y 구현은 사용자 책임. `/react-animation` 이 W3C APG 패턴 템플릿 제공하지만 자동 보장 안 함
- **View Transitions API 의 Firefox 제약**: 2026-04 기준 Firefox 144+ 의 `types` 파라미터 미지원. Feature detection + try/catch fallback 으로 처리
- **WASM + Tauri 2 + React 19 조합의 알려진 이슈**: shadcn + Tailwind v4 + React 19 조합은 shadcn-ui/ui#6585 에서 논의 진행 중. `/react-init` 설치 직후 `pnpm tsc --noEmit` 검증 권장
- **pnpm + Cargo workspace 혼합 pitfall**: 공식 pitfall 문서 부재 (unverified), 커뮤니티 사례 기반 — `crates/core` 를 양쪽 workspace 모두 등재
- **shadcn 패키지 리네임 (2024-08)**: `shadcn-ui` → `shadcn`, 구 명령 `npx shadcn-ui@latest init` 은 더 이상 동작 안 함
- **Codex 리서치 환경 이슈** (설계 과정): 이 레포에서 Codex 웹 검색이 특정 세션에서 stall 되는 현상 확인. WebSearch fallback 으로 전환하여 모든 리서치 완료 — 설계 산출물 품질에는 영향 없음

## 11. 다음 단계

1. **사용자 Spec 최종 검토** — 이 문서와 세부 설계 문서들 (`docs/react/kit-design/*.md`, `docs/react/wasm-catalog.md`) 를 검토
2. **writing-plans 스킬 호출** — 이 spec 을 구현 계획으로 분해:
   - Phase 1: 레포 내 `react-kit/` 디렉토리 scaffolding (plugin.json, README, 폴더 구조)
   - Phase 2: G1 스킬 4종 구현 (`/react-init` 이 가장 복잡)
   - Phase 3: G2 스킬 4종
   - Phase 4: G3 스킬 2종
   - Phase 5: G4 스킬 3종
   - Phase 6: G5 스킬 3종 + widget-inspector-react 에이전트
   - Phase 7: G5b `/react-animation` + animation-architect-react 에이전트
   - Phase 8: G6 스킬 4종 + react-reviewer 에이전트
   - Phase 9: `.claude-plugin/marketplace.json` 등록 + release 준비
   - Phase 10: evals/ fixtures 작성 + eval 실행 검증
3. **각 Phase 마다 harness 사이클** — sprint-contract → implementation → qa-evaluator (사용자 정책)
4. **초판 릴리스** — `bash scripts/release.sh react-kit patch` 로 `react-kit v0.1.0` 마켓플레이스 등록
5. **/react-kaizen** dev-only 스킬 추가 (`docs/react/` 리서치 → react-kit 개선 루프) — 다른 킷 카이젠 패턴 모방

## 12. 참조 문서 (이 spec 의 소스)

- [docs/react/wasm-catalog.md](../../react/wasm-catalog.md) — G0 WASM 결정 카탈로그 (521 줄)
- [docs/react/kit-design/g1-scaffolding.md](../../react/kit-design/g1-scaffolding.md) (525 줄)
- [docs/react/kit-design/g2-state-data.md](../../react/kit-design/g2-state-data.md) (653 줄)
- [docs/react/kit-design/g3-performance.md](../../react/kit-design/g3-performance.md) (519 줄)
- [docs/react/kit-design/g4-quality.md](../../react/kit-design/g4-quality.md) (665 줄)
- [docs/react/kit-design/g5-ui-patterns.md](../../react/kit-design/g5-ui-patterns.md) (418 줄)
- [docs/react/kit-design/g5b-animation.md](../../react/kit-design/g5b-animation.md) (983 줄)
- [docs/react/kit-design/g6-build-audit.md](../../react/kit-design/g6-build-audit.md) (527 줄)
- [docs/react/kit-design/final-integration.md](../../react/kit-design/final-integration.md) (490 줄)

**스프린트 계약 이력**: `.harness/history/2026-04-10-*-sprint-contract.md` (8개 그룹 각각의 완료 계약)

## 13. 승인 상태

- [x] 섹션 1~6 사용자 대화 승인
- [x] G0 WASM Catalog 문서 작성 + qa-evaluator APPROVE
- [x] G1~G6 + G5b 스킬 설계 문서 7개 작성 + qa-evaluator APPROVE
- [x] Final Integration Spec 작성 + qa-evaluator APPROVE
- [x] 이 통합 Spec 문서 작성
- [ ] 사용자 최종 검토 (대기 중)
- [ ] writing-plans 스킬 호출 (다음 단계)
