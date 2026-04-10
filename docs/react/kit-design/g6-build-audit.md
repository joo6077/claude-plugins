# G6 — Build & Audit Skills

```yaml
last_updated: 2026-04-10
group: G6
scope: react-kit 빌드 자동화 + 품질 감사 스킬 4종 + 에이전트 2종
skills: [/react-run, /react-build, /react-preflight, /react-audit]
agents: [react-reviewer, widget-inspector-react]
depends_on: [G1 project-detection, G2~G5b 산출물, G0 wasm-catalog.md]
research_sources:
  - Vitest CLI 문서 (vitest.dev/guide/cli)
  - wasm-pack build 문서 (rustwasm.github.io/docs/wasm-pack)
  - Vite build 문서 (vitejs.dev)
  - Playwright test CLI 문서 (playwright.dev)
  - TypeScript compiler (typescriptlang.org)
  - ESLint v9 flat config (eslint.org)
  - 2026-04 WebSearch 검증
```

## 문서 목적

react-kit **G6 그룹** 은 다른 그룹이 생성한 산출물을 **실행 가능하게 만들고 품질을 검증** 하는 마지막 단계 스킬들이다.

- **`/react-run`** — 빌드 프리미티브 (dev, build, lint, test, wasm-build, format, codegen) 을 개별 실행. 다른 상위 워크플로우 스킬들의 빌딩 블록
- **`/react-build`** — 전체 빌드 파이프라인. `wasm-pack → tsc → vite build` 순서로 실행하고 산출물을 검증
- **`/react-preflight`** — pre-commit quality gate. 커밋 전에 전체 검증을 돌려 문제 조기 발견
- **`/react-audit`** — 코드 품질 감사. quick 모드 (단일 에이전트) 와 deep 모드 (최대 4 에이전트 병렬) 지원. G0~G5b 의 모든 안티패턴을 통합 검출

**의존**: G1 이 세팅한 npm scripts + Cargo workspace + .harness/project.yaml. 모든 G6 스킬이 G1 `project-detection.md` 를 읽어 현재 환경을 감지한다.

## 공통 설계 원칙

- **모든 명령은 `pnpm`**: npm / yarn 직접 호출 금지. `pnpm` 이 react-kit 의 유일한 패키지 매니저
- **Exit code 존중**: 각 빌드/테스트 도구의 exit code 를 파이프라인 제어에 사용. `set -e` 유사 동작 — 한 단계라도 실패하면 즉시 중단
- **Strict TS 는 빌드 게이트**: `tsc --noEmit` 실패 = 빌드 실패. `skipLibCheck: true` 는 허용하지만 소스 코드 타입 에러는 용납 안 됨
- **ESLint `--max-warnings=0`**: 경고도 실패로 취급. warning 을 방치하면 점진적 품질 저하 유발
- **project-detection 공유**: 스킬마다 재감지하지 않고 한 번 로드 후 캐싱

## 1. /react-run — 빌드 프리미티브

개별 빌드 명령을 실행하는 저수준 스킬. 상위 워크플로우 스킬 (`/react-build`, `/react-preflight`) 이 내부적으로 호출.

### 1.1 트리거

- 키워드: "빌드 돌려", "테스트 실행", "코드 생성", "lint", "format", "wasm 빌드"
- 서브커맨드: `dev`, `build`, `lint`, `tsc`, `test`, `wasm-build`, `format`, `codegen`

### 1.2 서브커맨드 목록

| 서브커맨드 | 명령 | 용도 |
|----------|------|------|
| **dev** | `pnpm vite dev` | Vite dev 서버 시작 (포트 5173) |
| **build** | `pnpm vite build` | 프로덕션 빌드 → `dist/` |
| **preview** | `pnpm vite preview` | 프로덕션 빌드 결과 로컬 서빙 |
| **tsc** | `pnpm tsc --noEmit` | TypeScript 타입 체크만 |
| **lint** | `pnpm eslint . --max-warnings=0` | ESLint 검사 (경고 = 실패) |
| **lint-fix** | `pnpm eslint . --fix` | 자동 수정 가능한 것만 수정 |
| **format** | `pnpm prettier --write .` | Prettier 포매팅 적용 |
| **format-check** | `pnpm prettier --check .` | 포매팅 검사만 |
| **test** | `pnpm vitest run` | Vitest 1회 실행 (watch 없음) |
| **test-watch** | `pnpm vitest` | Vitest watch 모드 |
| **test-coverage** | `pnpm vitest run --coverage` | 커버리지 수집 포함 실행 |
| **e2e** | `pnpm playwright test` | Playwright e2e 테스트 |
| **wasm-build** | `pnpm wasm-pack build crates/core --target web --release --out-dir ../../src/wasm/core` | Rust → WASM 빌드 |
| **codegen** | `pnpm tsr generate && pnpm lingui extract && pnpm lingui compile` | TanStack Router 라우트 트리 + Lingui catalog 생성 |
| **tauri-dev** | `pnpm tauri dev` | Tauri 데스크탑 dev |
| **tauri-build** | `pnpm tauri build` | Tauri 데스크탑 프로덕션 빌드 |

### 1.3 감지 로직

`/react-run` 은 project-detection 결과를 보고 적용 가능한 서브커맨드만 노출:

- `crates/core/` 존재 안 함 → `wasm-build` 비활성
- `src-tauri/` 존재 안 함 → `tauri-dev`, `tauri-build` 비활성
- `lingui.config.ts` 존재 안 함 → `codegen` 이 `tsr generate` 만 실행
- Playwright 미설치 → `e2e` 비활성

### 1.4 Gotchas

- **`pnpm vitest` vs `pnpm vitest run`**: 전자는 watch 모드 기본, 후자는 1회 실행. CI/preflight 에서는 반드시 `run`
- **`--max-warnings=0`**: ESLint 기본은 warning 허용. 빌드 게이트 의도면 명시 필수
- **wasm-pack 출력 경로**: `--out-dir ../../src/wasm/core` 는 `crates/core/` 기준 상대 경로. `crates/core/` 디렉토리 안에서 실행해야 경로 해석 정확
- **`tsc --noEmit`**: 컴파일 없이 타입 검사만. 산출물 만들면 dist 와 충돌
- **Strict TS**: `pnpm tsc --noEmit` 은 프로젝트 전체 검사. incremental 빌드는 `--incremental` 로 가속 가능하지만 CI 에서는 clean 빌드 권장

### 1.5 Clean Architecture 배치

`/react-run` 은 파일을 생성하지 않고 명령만 실행. project root 에서 동작.

## 2. /react-build — 전체 빌드 파이프라인

3단계 빌드를 순서대로 실행하고, 한 단계라도 실패하면 즉시 중단.

### 2.1 트리거

- 키워드: "빌드", "build", "프로덕션 빌드"
- 조건: 프로젝트 초기화 완료

### 2.2 빌드 순서

```
[1. WASM 빌드]   crates/core → wasm-pack build → src/wasm/core/
        │ (실패 시 중단)
        ▼
[2. TypeScript 검사]   pnpm tsc --noEmit
        │ (실패 시 중단, 타입 에러 파일 리스트 출력)
        ▼
[3. Vite 빌드]   pnpm vite build → dist/
        │ (실패 시 중단, 빌드 에러 출력)
        ▼
[4. 산출물 검증]   dist/index.html 존재 + src/wasm/core/ 파일 크기 체크
        │
        ▼
완료 — dist/ 크기, wasm gzip 크기, 빌드 시간 리포트
```

### 2.3 옵션

- `--mode production` (기본) / `--mode development` / `--mode staging`
- `--skip-wasm`: WASM 빌드 건너뛰기 (WASM 없는 프로젝트)
- `--skip-tsc`: 타입 검사 건너뛰기 (비권장 — CI 실패 시 디버깅용)
- `--analyze`: 번들 분석 (rollup-plugin-visualizer)

### 2.4 실패 처리

- **WASM 빌드 실패**: Rust 컴파일 에러를 그대로 출력. `cargo check --target wasm32-unknown-unknown` 으로 재시도 안내
- **tsc 실패**: 타입 에러 파일 리스트 + 첫 5개 에러만 요약. 전체 출력은 로그 파일로
- **Vite 빌드 실패**: 의존성 resolve 실패 / ESBuild 에러 대부분. 명확한 에러 메시지가 나옴

### 2.5 산출물 검증

- `dist/index.html` 존재 확인 (Vite 빌드 성공 최소 지표)
- `dist/assets/*.js` gzip 크기 리포트 (사용자 awareness)
- `src/wasm/core/*.wasm` 존재 + gzip 크기 리포트
- 크기 임계값 초과 시 경고 (예: 단일 chunk > 1MB gzip)

### 2.6 Gotchas

- **WASM 은 반드시 먼저**: tsc 와 Vite 가 `src/wasm/core/` 를 import 하므로 WASM 산출물이 먼저 존재해야 함
- **Vite 는 tsc 를 하지 않음**: Vite 의 내장 ESBuild 는 type stripping 만 함. 타입 체크는 `tsc --noEmit` 별도 필수
- **환경 변수**: `VITE_*` prefix 만 브라우저 번들에 포함. 다른 prefix 는 런타임에 undefined
- **`base` 설정**: `vite.config.ts` 의 `base` 옵션이 Tauri (기본 `/`) 와 웹 배포 (예: `/my-app/`) 에서 다를 수 있음. build mode 별 분기 가능

## 3. /react-preflight — Pre-commit Quality Gate

커밋 전에 전체 검증을 돌리는 종합 게이트. 실패하면 커밋 불가 수준의 엄격함.

### 3.1 트리거

- 키워드: "preflight", "프리플라이트", "커밋 전 검사", "pre-commit"
- 조건: git 저장소 + 스테이징된 파일 또는 working directory 변경 있음
- 자동 호출: husky `pre-commit` 훅에서 실행 (옵션)

### 3.2 실행 순서

```
1. fix               prettier --write . && eslint . --fix
        ↓ 자동 수정 후에도 해결 안 된 포맷/린트 → 다음 단계에서 검출
2. codegen           tsr generate + lingui extract/compile
        ↓ 실패 → 설정 파일 오류 출력
3. lint              eslint . --max-warnings=0
        ↓ 실패 → 위반 파일 + 규칙 리스트 (fix 단계에서 해결되지 않은 것)
4. tsc               pnpm tsc --noEmit
        ↓ 실패 → 타입 에러 파일 리스트
5. test              pnpm vitest run
        ↓ 실패 → 실패 테스트 목록
6. wasm-build        pnpm wasm-pack build (crates/core 존재 시)
        ↓ 실패 → Rust 컴파일 에러
7. vite-build        pnpm vite build
        ↓ 실패 → 빌드 에러
8. audit (quick 모드)  /react-audit --quick (변경 파일만)
        ↓ 실패 → 안티패턴 리포트
```

**1단계 fix 의도**: 커밋 전에 prettier/eslint 자동 수정 가능한 것은 **미리 수정**한 뒤 파이프라인 진입. 3단계 `lint` 는 여전히 `--max-warnings=0` 로 엄격 검사 — 자동 수정 불가능한 규칙 위반이 남아 있으면 여기서 실패한다.

각 단계에서 **실패 시 즉시 중단**. 후속 단계 실행하지 않음 — fail-fast.

### 3.3 실패 시 롤백 / 복구

- **format-check 실패**: 자동 수정 명령 (`pnpm run format`) 안내. 사용자가 수락하면 자동 수행
- **codegen 실패**: `routeTree.gen.ts` 또는 Lingui `.po` 파일이 손상되었을 가능성. 재생성 시도
- **lint 실패**: `--fix` 로 자동 수정 가능한 것과 수동 수정 필요한 것 분리 표시
- **tsc 실패**: 수동 수정 필수. 파일 리스트 + 첫 5개 에러
- **test 실패**: 실패 테스트 명 + 스냅샷 변경 여부 표시. `--update-snapshots` 옵션 안내
- **wasm/vite-build 실패**: 로그 전체 출력 + 컴파일러 제안 메시지

### 3.4 부분 실행 (--files 플래그)

전체가 아니라 변경 파일만 대상 실행할 수 있다:

```sh
pnpm react-preflight --files "src/presentation/features/auth/**"
```

- lint: 지정 파일만
- tsc: 변경 영향 범위 자동 추적 (`tsc --noEmit` 은 전체 검사이므로 이 옵션은 lint/test 에만 적용)
- test: 관련 테스트 파일만 (Vitest `--related` 옵션)
- audit: 변경 파일만

### 3.5 Gotchas

- **cached 파일과 working tree 불일치**: `git add` 된 파일과 수정 후 add 안 한 파일이 섞이면 혼란. `git stash` 로 정리 후 실행 권장
- **husky + lint-staged 충돌**: lint-staged 가 이미 lint/format 을 돌리고 있으면 preflight 와 중복. react-kit 기본은 lint-staged 미사용 — preflight 한 번에 처리
- **codegen 파일 충돌**: `routeTree.gen.ts` 가 매번 regenerate 되면 git diff 노이즈. gitignore 하거나 stable hash 사용
- **TauriCI 환경**: Tauri 빌드는 preflight 에 포함 안 함 (너무 오래 걸림). 별도 `/react-tauri-build` 또는 CI 의 release 단계에서

## 4. /react-audit — 코드 품질 감사

Quick 모드 (단일 에이전트, 빠른 로컬 검토) 와 Deep 모드 (최대 4 에이전트 병렬 감사) 를 지원.

### 4.1 트리거

- 키워드: "감사", "audit", "코드 검토", "품질 검사", "리뷰", "안티패턴 검출"
- 조건: 변경 파일 존재
- 자동 호출: `/react-preflight` 의 마지막 단계 (quick 모드만)

### 4.2 모드 자동 선택 규칙

| 변경 파일 수 | 모드 | 실행 시간 (대략) |
|--------------|------|----------|
| 1~5 | Quick | 10~30초 |
| 6~20 | Quick | 30초~2분 |
| 21~50 | **Deep 권장** (사용자 확인) | 3~8분 |
| 51+ | Deep 강제 | 5~15분 |

플래그: `--quick` 또는 `--deep` 으로 명시적 override.

### 4.3 Quick 모드

단일 Claude 서브에이전트 (`react-reviewer`) 를 한 번 호출. 가벼운 카테고리 (lint 수준) 의 체크리스트만 돌림.

### 4.4 Deep 모드 — 4개 에이전트 병렬 축

Claude `Agent` 도구로 **4개의 독립 서브에이전트를 병렬 spawn**. 각 에이전트는 특정 관점만 책임:

```
[Deep Audit]
     │
     ├──► architecture-reviewer   (Clean Arch 경계 위반, Feature 간 직접 import)
     ├──► performance-reviewer    (WASM 오용, render 안 WASM 호출, 문자열 마샬링, 고빈도 콜백)
     ├──► accessibility-reviewer  (aria 누락, keyboard 경로, reduced-motion, 하드코딩 i18n)
     └──► library-policy-reviewer (금지 라이브러리 import, 패치 버전 하드코딩, deprecated API)
```

각 에이전트는 관점이 달라 **독립적으로 PASS/FAIL 판정**. 4개 결과를 병합해 최종 리포트 생성.

추가로 **widget-inspector-react** 에이전트 (G5 에서 정의) 를 5번째 축으로 포함 가능 — 중복 위젯 / 사유화된 재사용 가능 컴포넌트 감지.

### 4.5 감사 체크리스트 (카테고리별)

각 규칙에 **grep 패턴** 또는 **AST 검사 기준** 이 명시된다. `grep_pattern` 은 ripgrep 호환 정규식, `ast_check` 는 TypeScript Compiler API / ESLint 룰 ID.

#### Architecture

- **Clean Arch 경계 위반** (`domain` 이 `data`/`presentation` import) → ❌ 실패
  - grep_pattern: `^import .* from ['"]@/(data|presentation|infrastructure)/`
  - scope: `src/domain/**/*.ts`
- **Feature 간 직접 import** (`features/a` 가 `features/b` 직접 참조) → ❌ 실패
  - grep_pattern: `^import .* from ['"]@/presentation/features/(?!\k<currentFeature>)`
  - ast_check: 현재 파일의 feature 이름 추출 후 다른 feature import 검출
- **Infrastructure 역참조** (`domain` 이 `infrastructure/*` import) → ❌ 실패
  - grep_pattern: `^import .* from ['"]@/infrastructure/`
  - scope: `src/domain/**/*.ts`
- **상대 경로 사용** (`'../../../shared/...'`) → ⚠️ 경고
  - grep_pattern: `^import .* from ['"]\.\./\.\./\.\./`
- **`export default` 사용** → ⚠️ 경고
  - grep_pattern: `^export default `
  - ast_check: `@typescript-eslint/no-default-export` 또는 `import/no-default-export`

#### Strict TypeScript

- **`any` 사용** → ❌ 실패
  - grep_pattern: `: any\b|<any>|as any\b`
  - ast_check: `@typescript-eslint/no-explicit-any` (error level)
- **`as` 타입 단언** (일반) → ⚠️ 경고 (Zod parse 권고)
  - grep_pattern: ` as [A-Z][a-zA-Z]+\b` (타입 단언), exclude `as const`
  - ast_check: `@typescript-eslint/consistent-type-assertions`
- **`!` non-null 단언** → ❌ 실패
  - grep_pattern: `\w+!\.\w+|\w+!\[|\w+!\s*,|\w+!\s*\)`
  - ast_check: `@typescript-eslint/no-non-null-assertion`
- **`React.FC` 사용** → ⚠️ 경고
  - grep_pattern: `React\.FC<|: FC<`
- **Missing return type** (public API) → ⚠️ 경고
  - ast_check: `@typescript-eslint/explicit-module-boundary-types`

#### Performance

- **WASM render 안 호출** (`useMemo` 없이 매 렌더) → ❌ 실패 (G0 §8)
  - ast_check: JSX return 안에서 `@/data/datasources/wasm/` 심볼 직접 호출, 상위 `useMemo` 없음
- **문자열 마샬링 과다** (KB 단위 String 인자 반복) → ⚠️ 경고
  - ast_check: `@/data/datasources/wasm/` 함수 호출의 첫 인자 타입이 `string` 이면서 호출 빈도 추정 높음
- **WASM Worker 누락** (100ms+ 작업이 main thread) → ⚠️ 경고
  - grep_pattern: `from ['"]@/wasm/` (직접 import, Worker 경유 안 함)
  - 정확한 검출은 런타임 프로파일 필요 → 정적 힌트만
- **WASM 카탈로그 위반** (`/react-wasm` 이 §2 비권장 이식) → ❌ 실패 (G0 `wasm-catalog.md`)
  - 판정 소스: G0 카탈로그 §2 카테고리 테이블 + 스킬 매타데이터
- **번들 크기** (단일 chunk > 500KB gzip) → ⚠️ 경고
  - check: `vite build --mode production` 후 `dist/assets/*.js` 파일 크기 측정
- **TanStack Query staleTime 0 빈번** → ⚠️ 경고
  - ast_check: `useQuery({ ... })` 호출에 `staleTime` 필드 없음

#### Accessibility

- **하드코딩된 i18n 문자열** (매크로 미경유 한국어/영어) → ⚠️ 경고 (G4)
  - grep_pattern: `>[^<{]*[가-힣A-Za-z][^<{]*<|["'][^"']*[가-힣][^"']*["']` (in .tsx)
  - exclude: `<Trans>`, `t\`...\``, `msg\`...\`` 내부
- **`aria-*` 누락** (인터랙티브 요소) → ⚠️ 경고
  - ast_check: `eslint-plugin-jsx-a11y/accessible-name`
- **keyboard 경로 누락** (드래그앤드롭) → ⚠️ 경고 (G5b §5)
  - ast_check: `useDrag` 훅 호출하는 컴포넌트에 `onKeyDown` 또는 `role="button"` + tabIndex 없음
- **`prefers-reduced-motion` 가드 누락** → ⚠️ 경고
  - grep_pattern: 파일에 `animate-` 또는 `transition-` 클래스 있는데 `motion-reduce:` 또는 `@media (prefers-reduced-motion` 없음
- **Error Boundary 없음** (최상위) → ❌ 실패
  - grep_pattern: `src/main.tsx` 또는 `src/app.tsx` 에 `ErrorBoundary` 없음
  - ast_check: RouterProvider 또는 App 루트에 Error Boundary 컴포넌트 있는지

#### Anti-patterns

스택 중립적 부패 패턴. Library Policy 와 분리하여 "코드 설계상 바람직하지 않은 일반적 패턴" 만 포함.

- **빈 try/catch** → ❌ 실패
  - grep_pattern: `catch\s*\([^)]*\)\s*\{\s*\}`
- **console.log / console.error (production)** → ⚠️ 경고
  - grep_pattern: `console\.(log|error|warn|debug)\(`
  - ast_check: `no-console` ESLint rule
- **throw new Error(...) 도메인 레이어** → ❌ 실패 (G2 Result 패턴)
  - grep_pattern: `throw new`
  - scope: `src/domain/**/*.ts`
- **useState 로 서버 상태 관리** → ⚠️ 경고 (G2 TanStack Query 권고)
  - ast_check: `useState` 호출 후 `useEffect` 로 fetch → 안티패턴
- **컴포넌트 파일 길이 > 400줄** → ⚠️ 경고
  - check: 파일 line count
- **patch 버전 하드코딩** (package.json) → ⚠️ 경고
  - grep_pattern: `"[^"]+": "\d+\.\d+\.\d+"` (캐럿/틸드 없는 고정 버전)
  - scope: `package.json`

#### Library Policy

react-kit 이 강제하는 **라이브러리 허용/금지** 정책. 위반 시 즉시 실패.

- **금지 애니메이션 라이브러리 import** (G5b) → ❌ 실패
  - grep_pattern: `^import .* from ['"](motion|framer-motion|react-spring|@dnd-kit/[^'"]*|@formkit/auto-animate[^'"]*|react-dnd[^'"]*|gsap|lottie-react)['"]`
  - scope: `src/**/*.{ts,tsx}`
- **deprecated shadcn 패키지명** (`shadcn-ui`) → ❌ 실패 (G1)
  - grep_pattern: `^import .* from ['"]shadcn-ui['"]` 또는 `package.json` 의 `"shadcn-ui"` dependency
- **deprecated MSW v1 API** (`rest.get` 등) → ⚠️ 경고 (G4)
  - grep_pattern: `import \{[^}]*\brest\b[^}]*\} from ['"]msw['"]`
- **deprecated Lingui macro 경로** (`@lingui/macro`) → ⚠️ 경고 (G4)
  - grep_pattern: `from ['"]@lingui/macro['"]`
  - 교체: `from '@lingui/react/macro'` 또는 `from '@lingui/core/macro'`
- **Tauri API 직접 import (isTauri 가드 없이)** → ❌ 실패 (G3)
  - grep_pattern: `^import .* from ['"]@tauri-apps/`
  - scope: `src/` 중 `src/infrastructure/tauri/` 제외
- **TanStack Query 외 서버 상태 관리 라이브러리** → ⚠️ 경고
  - grep_pattern: `from ['"](swr|@apollo/client|react-query|urql)['"]`
- **외부 상태 관리 라이브러리** (Redux, Jotai, Recoil) → ⚠️ 경고
  - grep_pattern: `from ['"](redux|react-redux|@reduxjs/toolkit|jotai|recoil)['"]`
  - 권장: Zustand (G2 정책)

### 4.6 감사 리포트 포맷

```markdown
## /react-audit 리포트 (2026-04-10 19:00)

**모드**: deep
**변경 파일**: 27 개
**판정**: **REJECT** (2 실패, 8 경고)

### ❌ 실패 (2)
1. `src/presentation/features/gallery/thumb-card.tsx:14` — WASM 함수를 useMemo 없이 렌더에서 호출 (Performance)
2. `src/presentation/features/kanban/card.tsx:3` — 금지 라이브러리 import `@dnd-kit/core` (Library Policy)

### ⚠️ 경고 (8)
...

### ✅ 통과 카테고리
- Architecture: 모든 경계 정상
- Strict TS: any/as/! 위반 없음
- Accessibility: 최상위 Error Boundary 존재

### 권장 후속 작업
- `/react-wasm` 의 useMemo 래핑 Gotcha 문서 참조
- G5b 라이브러리 0개 원칙 재확인
```

### 4.7 Gotchas

- **False positive 관리**: AST 기반 정적 분석이 완벽하지 않음. `// react-audit-ignore: <rule>` 주석으로 개별 라인 제외 허용
- **Baseline 지원**: 기존 대형 프로젝트에 처음 도입 시 모든 경고를 한 번에 고치기 어려움. `.react-audit-baseline.json` 로 "현재 상태 이하로 악화되지 않음" 만 감지하는 모드 지원
- **성능**: 대규모 프로젝트에서 deep 모드가 오래 걸릴 수 있음. 파일 수 제한 + 증분 감사 권장
- **Agent 결과 병합**: 4개 에이전트 결과가 같은 파일 다른 카테고리로 중복 언급할 수 있음. 파일 기준 병합 후 카테고리별 그룹화

### 4.8 Clean Architecture 배치

`/react-audit` 는 파일 생성 없음. 읽기 전용 + 리포트 출력.

## 5. Agents

### 5.1 react-reviewer

범용 리뷰 에이전트. Quick 모드에서 단독 실행, Deep 모드에서 카테고리별 인스턴스로 분화.

**역할**: 읽기 전용 독립 평가. 변경 파일 집합을 받아 해당 카테고리의 체크리스트에 따라 PASS/FAIL 판정.

**트리거**: `/react-audit` 스킬이 Agent 도구로 호출. 사용자가 직접 호출 금지 (독립성 보장).

**입력**:
- 변경 파일 경로 리스트
- 감사 카테고리 (Architecture / Strict TS / Performance / Accessibility / Anti-patterns)
- 프로젝트 루트 경로
- G0 `wasm-catalog.md` 및 G5b 금지 라이브러리 목록 참조

**출력**:
```yaml
verdict: APPROVE | REJECT
category: <카테고리명>
failures:
  - file: <path>
    line: <n>
    rule: <규칙 id>
    message: <한글 설명>
warnings:
  - file: <path>
    line: <n>
    rule: <규칙 id>
    message: <한글 설명>
suggestions:
  - <후속 작업 권장>
```

**도구 스코프**: `Read`, `Grep`, `Glob` — **쓰기 권한 없음**. 파일 수정 금지, 리포트 반환만.

**모델**: Sonnet 기본. Deep 모드의 고난도 카테고리 (Performance with WASM 판정) 는 Opus 옵션.

### 5.2 widget-inspector-react (G5 재사용)

G5 에서 정의된 에이전트. G6 Deep 모드에서 5번째 축으로 병렬 실행.

**역할**: 프로젝트 전체 컴포넌트 스캔 → 중복 위젯 감지, 사유화된 재사용 가능 컴포넌트 감지, 복잡도 임계값 초과 감지.

**재사용 방식**: `/react-audit --deep` 이 `widget-inspector-react` 를 spawn 하여 5번째 병렬 축으로 실행. 결과는 메인 감사 리포트의 "Refactoring 권장" 섹션에 병합.

**연결**: 에이전트 리포트 중 "추출 권장" 항목은 사용자 승인 후 G5 `/react-extract` 스킬을 통해 자동 실행 가능.

## 6. 모든 스킬의 실행 위치 & npm scripts

`/react-init` 이 `package.json` 에 기본 scripts 를 추가:

```json
{
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
    "tauri:build": "tauri build",
    "preflight": "react-preflight",
    "audit": "react-audit"
  }
}
```

G6 스킬들은 내부적으로 이 npm scripts 를 호출 (`pnpm run <script>`) — 사용자가 수동으로도 같은 명령을 쓸 수 있게 일관성 유지.

## 7. Reusability & Cross-group 관계

- **G1 project-detection**: 모든 G6 스킬이 재사용. Vite / Tailwind / shadcn / TanStack Router 설치 여부, pnpm 버전, Cargo workspace 존재 여부 감지 결과를 npm scripts 구성과 감사 규칙에 반영
- **G0 `wasm-catalog.md`**: `/react-audit` 의 Performance 카테고리가 참조. WASM 권장/비권장 판정 규칙을 여기서 읽어와 코드에 적용
- **G5b 금지 라이브러리**: `/react-audit` 의 Library Policy 카테고리가 직접 grep 패턴으로 사용
- **G1~G5 모든 스킬**: 생성한 파일을 `/react-audit` 이 검사 대상으로 삼음. 특히 `/react-audit` 의 안티패턴 목록은 각 그룹의 Gotchas 섹션을 종합한 것

## 8. 다른 그룹과 G6 의 관계도

```
G0 wasm-catalog.md         ─┐
G1 Scaffolding             ─┤
G2 State & Data            ─┤   ─► 생성물 생성 ─►  /react-audit  ─► 품질 리포트
G3 Performance             ─┤                        │
G4 Quality                 ─┤                        ├─► react-reviewer (4 병렬 축)
G5 UI Patterns             ─┤                        └─► widget-inspector-react (5번째 축)
G5b Animation              ─┘

각 그룹의 Gotchas    ─► G6 /react-audit 의 안티패턴 목록 자동 반영
```

## 9. 출처 요약

1. Vitest CLI: https://vitest.dev/guide/cli
2. Vitest Coverage: https://vitest.dev/guide/coverage
3. Vite build: https://vitejs.dev/guide/build
4. wasm-pack build command: https://rustwasm.github.io/docs/wasm-pack/commands/build.html
5. wasm-pack GitHub: https://github.com/rustwasm/wasm-pack
6. Playwright test CLI: https://playwright.dev/docs/test-cli
7. ESLint v9 flat config: https://eslint.org/docs/latest/use/configure/configuration-files
8. TypeScript compiler options (tsc --noEmit): https://www.typescriptlang.org/docs/handbook/compiler-options.html
9. Prettier CLI: https://prettier.io/docs/en/cli
10. Tauri 2 CLI: https://v2.tauri.app/reference/cli/
11. TanStack Router codegen: https://tanstack.com/router/latest/docs/api/file-based-routing
12. Lingui CLI: https://lingui.dev/ref/cli

## 10. 감사 규칙 중요도 레벨

각 카테고리의 규칙은 **중요도** 가 있다. 기본 규칙은 아래 3 레벨:

| 레벨 | 기호 | 의미 | CI 행동 |
|------|------|------|---------|
| **error** | ❌ | 반드시 고쳐야 함. 빌드 게이트 | exit 1 (preflight 실패) |
| **warn** | ⚠️ | 권장 사항. 고치지 않아도 빌드는 통과 | exit 0 + 경고 리포트 |
| **info** | ℹ️ | 참고용. 설계 개선 힌트 | 리포트에 섹션으로 추가 |

`.react-audit.config.ts` 로 규칙별 레벨 override 가능. 예: 레거시 마이그레이션 중인 프로젝트는 일부 `error` 를 `warn` 으로 완화 후 점진 수정.

## 11. 변경 이력

- **2026-04-10** — 초판. G6 4 스킬 (`/react-run`, `/react-build`, `/react-preflight`, `/react-audit`) + 2 에이전트 (`react-reviewer`, `widget-inspector-react` G5 재사용) 상세 설계. Deep 모드 4 병렬 축 (Architecture / Performance / Accessibility / Library Policy) + 5번째 축 (widget-inspector-react). G0~G5b 모든 그룹의 안티패턴 통합 감사 규칙 수록. 중요도 레벨 (error/warn/info) 정책 추가. WebSearch fallback 으로 Vitest CLI, wasm-pack build 옵션 검증.
