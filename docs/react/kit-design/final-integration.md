# react-kit Final Integration Spec

```yaml
last_updated: 2026-04-10
scope: react-kit 플러그인의 최종 산출물 통합 명세
covers:
  - harness .harness/project.yaml 스키마
  - 플러그인 파일 구조
  - marketplace.json 등록
  - plugin.json 템플릿
  - README 섹션 구조
  - 에이전트 배치
references:
  - flutter-toolkit/ 구조 (모방 대상)
  - rust-kit/ 구조 (모방 대상)
  - .claude-plugin/marketplace.json (기존 등록 형식)
  - docs/react/kit-design/g1~g6 (세부 설계 소스)
```

## 1. Harness 통합 — `.harness/project.yaml`

react-kit 으로 생성된 사용자 프로젝트에서 `/harness init` 이 자동 생성할 템플릿. flutter-toolkit 과 rust-kit 의 project.yaml 구조를 모방하며, react-kit 특화 카테고리와 안티패턴을 추가.

### 1.1 전체 템플릿

```yaml
# ── Harness Project Config: react-kit ──

stack: "react"

# ── 빌드/분석 명령 ──
commands:
  analyze: "pnpm tsc --noEmit && pnpm eslint . --max-warnings=0"
  test: "pnpm vitest run"
  lint: "pnpm eslint . --max-warnings=0"
  format: "pnpm prettier --write ."
  codegen: "pnpm tsr generate && pnpm lingui extract && pnpm lingui compile"
  build: "pnpm run wasm:build && pnpm tsc --noEmit && pnpm vite build"

# ── 계약 카테고리 ──
contract_categories:
  - id: Architecture
    prefix: "AR"
    description: "Clean Architecture 레이어 경계, feature 분리, import 방향"
  - id: StrictType
    prefix: "ST"
    description: "Strict TypeScript 준수 — any/as/! 금지, Zod 경계 검증, Result 타입"
  - id: Performance
    prefix: "PF"
    description: "WASM 카탈로그 준수, render 경로 최적화, 번들 크기"
  - id: Accessibility
    prefix: "A11Y"
    description: "i18n, ARIA, 키보드 경로, reduced-motion, Error Boundary"
  - id: LibraryPolicy
    prefix: "LP"
    description: "금지 라이브러리 (motion/dnd-kit 등), deprecated API 사용 금지"
  - id: Testing
    prefix: "TS"
    description: "Vitest unit, Testing Library component, Playwright e2e, 에러 경로 검증"

# ── 안티패턴 (G6 감사 규칙 핵심 재수록) ──
anti_patterns:
  # Library Policy
  - id: AP-01
    pattern: "^import .* from ['\"](motion|framer-motion|react-spring|@dnd-kit/[^'\"]*|@formkit/auto-animate[^'\"]*|react-dnd[^'\"]*|gsap|lottie-react)['\"]"
    message: "금지 애니메이션 라이브러리 import — react-kit 은 라이브러리 0개 원칙 (G5b)"
    scope: "src/**/*.{ts,tsx}"
  - id: AP-02
    pattern: "^import .* from ['\"]@tauri-apps/"
    message: "Tauri API 직접 import — infrastructure/tauri/ 래퍼 경유 필수 (isTauri 가드)"
    scope: "src/**/*.{ts,tsx}"
    exclude: "src/infrastructure/tauri/"
  - id: AP-03
    pattern: "from ['\"]@lingui/macro['\"]"
    message: "deprecated Lingui macro 경로 — @lingui/react/macro 또는 @lingui/core/macro 사용"
  - id: AP-04
    pattern: "^import .* from ['\"](redux|react-redux|@reduxjs/toolkit|jotai|recoil|swr|@apollo/client|react-query|urql)['\"]"
    message: "react-kit 은 Zustand (클라이언트) + TanStack Query (서버) 조합만 허용"

  # Strict TypeScript
  - id: AP-10
    pattern: ": any\\b|<any>|as any\\b"
    message: "any 사용 금지 — Strict TS 정책"
  - id: AP-11
    pattern: "\\w+!\\.\\w+"
    message: "non-null 단언 ! 금지 — optional chaining ?. 또는 Zod parse 사용"

  # Performance
  - id: AP-20
    pattern: "^import .* from ['\"]@/wasm/"
    message: "WASM 모듈 직접 import — Comlink Worker 경유 필수 (G3)"
    scope: "src/presentation/"

  # Architecture
  - id: AP-30
    pattern: "^import .* from ['\"]@/(data|presentation|infrastructure)/"
    message: "domain/ 레이어가 하위 레이어 import — Clean Arch 경계 위반"
    scope: "src/domain/"

  # Accessibility
  - id: AP-40
    pattern: "throw new"
    message: "domain/ 에서 throw — Result 타입 반환 필수 (G2 패턴)"
    scope: "src/domain/"

# ── 재사용성 ──
reusability:
  shared_path: "src/presentation/shared/"
  check_duplicate: true

# ── Diagnostics ──
diagnostics:
  ide_exclude: []
  console_errors:
    - "Failed to load module"
    - "Uncaught TypeError"
    - "Hydration failed"
  console_exclude:
    - "React Router Future Flag Warning"

# ── 런타임 검증 ──
runtime_inspection:
  mcp_server: null  # 필요 시 "playwright" 설정
  vm_port: 5173
  launch_script: "pnpm dev"

# ── 트리거 조건 ──
trigger:
  min_files: 2
  always:
    - "화면 추가"
    - "react-screen"
    - "react-feature"
    - "API 연동"
    - "react-api"
    - "WASM"
    - "react-wasm"
    - "Tauri command"
    - "react-tauri"
  never:
    - "읽어줘"
    - "설명해줘"
    - "리포트만"

# ── 검증 절차 ──
verification:
  procedures_dir: ".harness/procedures/"

# ── 변명 차단 ──
rationalization_overrides:
  - "WASM 카탈로그 §2 비권장인데 '그래도 빠를 것 같아서' → 금지"
  - "드래그앤드롭 접근성 '나중에' → 금지, 최소 키보드 경로 필수"
  - "any '임시로' → 금지, Zod parse 또는 unknown + 가드"
```

### 1.2 contract_categories 설계 근거

react-kit 은 **6개 카테고리** 를 사용 — flutter-toolkit 의 4개 (UI/Logic/Error/Architecture) 보다 세분화. Clean Arch + Strict TS + Performance + Accessibility 가 각각 독립 판정 축이기 때문.

- **Architecture (AR)**: Clean Arch 경계, feature 분리
- **StrictType (ST)**: TypeScript 엄격성 — any/as/! 금지, Zod 경계 검증
- **Performance (PF)**: WASM 카탈로그 준수, render 최적화
- **Accessibility (A11Y)**: 이 축은 react-kit 이 특히 강조 (G5b 드래그앤드롭 접근성, i18n, Error Boundary)
- **LibraryPolicy (LP)**: 금지 라이브러리 정책 전용 (react-kit 만의 특징)
- **Testing (TS)**: 테스트 커버리지 + 에러 경로 검증

### 1.3 anti_patterns ↔ G6 감사 규칙 매핑

`.harness/project.yaml` 의 anti_patterns 는 `/react-audit` 의 전체 규칙 (34개) 중 **빌드 게이트급 실패 규칙** 만 선별하여 등록. 경고급 규칙은 `/react-audit` 리포트에만 남고 harness trigger 대상은 아님.

## 2. 플러그인 파일 구조

### 2.1 react-kit/ 폴더 트리

```
react-kit/
├── .claude-plugin/
│   └── plugin.json
├── README.md
│
├── skills/                                  # 21개 스킬
│   ├── react-init/SKILL.md                  # G1
│   ├── react-screen/SKILL.md
│   ├── react-feature/SKILL.md
│   ├── react-widget/SKILL.md
│   │
│   ├── react-store/SKILL.md                 # G2
│   ├── react-api/SKILL.md
│   ├── react-query/SKILL.md
│   ├── react-form/SKILL.md
│   │
│   ├── react-wasm/SKILL.md                  # G3
│   ├── react-tauri/SKILL.md
│   │
│   ├── react-test/SKILL.md                  # G4
│   ├── react-error/SKILL.md
│   ├── react-l10n/SKILL.md
│   │
│   ├── react-responsive/SKILL.md            # G5
│   ├── react-skeleton/SKILL.md
│   ├── react-extract/SKILL.md
│   │
│   ├── react-animation/SKILL.md             # G5b (라이브러리 0개)
│   │
│   ├── react-run/SKILL.md                   # G6
│   ├── react-build/SKILL.md
│   ├── react-preflight/SKILL.md
│   └── react-audit/SKILL.md
│
├── agents/                                  # 3개 에이전트
│   ├── react-reviewer.md                    # G6 — /react-audit 공용 리뷰 에이전트
│   ├── widget-inspector-react.md            # G5 — 위젯 중복/사유화 감지
│   └── animation-architect-react.md         # G5b — 애니메이션 설계 자문
│
├── references/                              # 공유 레퍼런스 문서
│   ├── project-detection.md                 # 모든 스킬이 공유 (flutter-toolkit 패턴 모방)
│   ├── clean-arch-layout.md                 # 레이어 배치 규칙
│   ├── result-patterns.md                   # neverthrow Result 사용 패턴
│   ├── wasm-catalog.md                      # 이 레포 docs/react/wasm-catalog.md 의 링크
│   └── style-guide.md                       # strict TS + Prettier + ESLint 규칙 요약
│
├── templates/                               # 스캐폴딩 템플릿
│   ├── tsconfig.template.json
│   ├── eslint.config.template.js
│   ├── vite.config.template.ts
│   ├── tailwind.config.template.ts
│   ├── package.json.template
│   ├── pnpm-workspace.yaml.template
│   ├── Cargo.toml.template
│   ├── lingui.config.ts.template
│   └── harness-project.yaml.template        # §1.1 의 project.yaml 템플릿
│
├── evals/                                   # 스킬 테스트 픽스처
│   ├── evals.json                           # 각 스킬별 assertion
│   └── test-fixtures/
│       ├── empty-project/                   # /react-init 대상
│       ├── clean-arch-project/              # /react-api, /react-feature 대상
│       ├── wasm-project/                    # /react-wasm 대상
│       ├── tauri-project/                   # /react-tauri 대상
│       └── audit-target-project/            # /react-audit 대상
│
└── scripts/                                 # 유틸리티
    └── project-detect.sh                    # project-detection 로직의 bash 구현
```

### 2.2 plugin.json 템플릿

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

### 2.3 에이전트 파일 경로 및 모델

| 에이전트 | 파일 | 기본 모델 | 도구 스코프 |
|---------|------|---------|----------|
| `react-reviewer` | `react-kit/agents/react-reviewer.md` | Sonnet (deep 모드 Performance 축은 Opus 옵션) | Read / Grep / Glob |
| `widget-inspector-react` | `react-kit/agents/widget-inspector-react.md` | Sonnet | Read / Grep / Glob |
| `animation-architect-react` | `react-kit/agents/animation-architect-react.md` | Sonnet | Read / Grep / Glob |

모든 에이전트는 **읽기 전용** — 쓰기 도구 (Edit/Write/NotebookEdit) 는 제외하여 독립성 보장.

### 2.4 references/ 공유 문서

- **project-detection.md**: 모든 스킬이 읽는 프로젝트 감지 규칙. Node 버전, pnpm 버전, React 버전, Tailwind v3 vs v4, shadcn 초기화 여부, Cargo workspace 존재 여부, TanStack Router 플러그인 설치 여부 등
- **clean-arch-layout.md**: 도메인/데이터/프레젠테이션/인프라 레이어 배치 규칙 + 금지 import 방향
- **result-patterns.md**: neverthrow `Result` / `ResultAsync` 사용 패턴, Failure 타입 설계, queryFn throw 규칙
- **wasm-catalog.md**: 이 레포 `docs/react/wasm-catalog.md` 를 심볼릭 링크 또는 사본 (카이젠 루프가 동기화)
- **style-guide.md**: strict TS 옵션, ESLint 규칙, Prettier 설정, 네이밍 컨벤션

## 3. Marketplace 등록

### 3.1 marketplace.json 엔트리

이 레포의 `.claude-plugin/marketplace.json` 에 아래 엔트리를 **기존 rust-kit 다음에** 추가:

```json
{
  "name": "react-kit",
  "source": "./react-kit",
  "description": "[v0.1.0 · 2026-04-10] React + Vite + Tauri 2 + Rust WASM 전용 개발 워크플로우 플러그인 — 21종 스킬 + 3 에이전트, 라이브러리 0개 애니메이션"
}
```

`description` 의 `[vX.Y.Z · YYYY-MM-DD]` 접두사는 `scripts/release.sh` 가 자동 갱신하는 포맷. 초판은 수동 추가.

### 3.2 scripts/release.sh 갱신 대상

release 스크립트는 아래 파일들을 자동 갱신한다:

- `react-kit/.claude-plugin/plugin.json` — `version` 필드
- `.claude-plugin/marketplace.json` — react-kit 엔트리의 `description` 의 `[v... · ...]` 부분

기존 release.sh 가 sed + 플러그인 이름으로 파일을 찾는 방식이므로, react-kit 을 새로 추가할 때 **release.sh 자체는 수정 불필요**. 기존 패턴을 그대로 재사용한다 (BSD/GNU sed 크로스 플랫폼 호환 이미 처리됨).

## 4. README 섹션 구조

`react-kit/README.md` 는 기존 rust-kit, flutter-toolkit README 의 구조를 모방:

```markdown
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
```

### 4.1 문서 위치 구분

| 위치 | 역할 |
|------|------|
| `react-kit/README.md` | 플러그인 사용자 대상 — 스킬 목록, 퀵스타트, 철학 |
| `react-kit/references/*.md` | 스킬 내부가 읽는 공유 레퍼런스 (사용자 직접 안 봄) |
| `docs/react/*.md` (이 레포) | **레포 개발용 리서치 문서** — 카이젠 루프가 갱신. `wasm-catalog.md` 등 |
| `docs/react/kit-design/*.md` (이 레포) | **레포 개발용 설계 문서** — react-kit 의 스킬별 상세 스펙. 실제 SKILL.md 작성의 소스 |

**구분 원칙**: `react-kit/` 안은 **배포 대상** (플러그인 이용자가 받음), `docs/react/` 는 **개발 내부 문서** (플러그인 품질 관리). 두 위치의 동기화는 `/react-kaizen` 카이젠 스킬이 담당.

## 5. 에이전트 설계 가이드 연동

`harness/docs/guides/agent-design-guide.md` (이 레포 내부 문서) 의 6개 디자인 패턴 중 `react-kit` 의 에이전트 3종이 사용하는 패턴:

- **react-reviewer** — *Independent Reviewer* 패턴. 메인 Claude 컨텍스트 편향 배제를 위해 새 세션 spawn, 읽기 전용 도구로 판정만
- **widget-inspector-react** — *Codebase Scanner* 패턴. 전체 스캔 → 리포트 → 사용자 승인 후 다른 스킬이 실행
- **animation-architect-react** — *Design Consultant* 패턴. 자문 → 사용자 승인 → 스킬이 구현

각 에이전트 파일은 `harness/create-agent` 스킬로 생성. 설계 가이드의 tool 스코핑, 모델 선택, description 작성법을 따름.

## 6. 기존 플러그인과의 구조 일관성

아래 구조 원칙을 flutter-toolkit / rust-kit 과 동일하게 유지:

- **`.claude-plugin/plugin.json`**: 동일 필드 (name, description, version, author, repository, license, keywords)
- **`skills/<name>/SKILL.md`**: frontmatter + process 구조, Gotchas 섹션 포함
- **`agents/<name>.md`**: frontmatter (name, description, tools, model) + 본문
- **`references/`, `templates/`, `evals/`**: 선택적이지만 react-kit 은 모두 사용
- **README.md `<!-- AUTO:xxx -->` 마커**: `scripts/sync-docs.py` 가 자동 갱신할 수 있도록 같은 마커 사용

한 가지 차이점: flutter-toolkit, rust-kit 은 `scripts/` 를 사용 안 하지만 react-kit 은 `project-detect.sh` 같은 bash 헬퍼를 둘 수 있음. 이는 스킬 내부 구현 선택.

## 7. 스캐폴딩 시 생성되는 .harness/project.yaml 의 커스터마이징

`/react-init` 이 `/harness init` 을 함께 호출할 때, `templates/harness-project.yaml.template` (§1.1 전체) 를 사용자 프로젝트의 `.harness/project.yaml` 로 복사. 사용자는 필요 시 수정 가능 (예: `runtime_inspection.vm_port` 를 다른 포트로, 특정 anti_pattern 을 disable).

## 8. 변경 이력

- **2026-04-10** — 초판. react-kit 의 harness 통합, 플러그인 파일 구조, marketplace 등록, plugin.json, README 구조를 통합 명세. flutter-toolkit / rust-kit / harness 의 기존 플러그인 레이아웃과 100% 일관성 유지. 21 스킬 + 3 에이전트 모두 파일 경로 확정. scripts/release.sh 는 기존 패턴 재사용 (수정 불필요). 레포 docs/react/ vs react-kit/ 디렉토리 역할 구분 명시.
