---
name: react-audit
description: >
  코드 품질 감사. quick 모드(단일 에이전트, 빠른 로컬 검토)와 deep 모드(최대 4 에이전트 병렬 감사)를 지원한다.
  "감사", "코드 감사", "리뷰 돌려줘", "audit", "품질 검사", "커밋 전 감사",
  "코드 검토", "안티패턴 검출", "아키텍처 확인", "code review", "quality check" 같은 요청 시 사용한다.
  변경 파일 수에 따라 자동으로 모드를 선택하며 명시적으로 지정할 수도 있다.
  단순 탐색, 코드 읽기, 질문 응답만 할 때는 사용하지 않는다.
argument-hint: "[quick|deep] [path]"
user-invocable: true
---

## Gotchas

- **Library Policy 는 빌드 게이트급**: `motion`, `framer-motion`, `@dnd-kit/*`, `react-spring`, `react-transition-group`, `react-dnd`, `react-beautiful-dnd`, `gsap`, `lottie-react`, `@formkit/auto-animate`, `animate.css` import 는 ��� 실패 — 경고가 아니라 즉각 REJECT
- **WASM 렌더 안 호출**: JSX return 블록 안에서 useMemo 없이 WASM 함수를 직접 호출하면 매 렌더마다 WASM boundary 를 건넘. ❌ 실패
- **False positive 관리**: `// react-audit-ignore: <rule>` 주석으로 해당 라인 제외 가능
- **Baseline 모드**: 기존 대형 프로젝트에 처음 도입 시 `.react-audit-baseline.json` 으로 "현재 이하로 악화되지 않음" 만 감지하는 모드 지원
- **quick vs deep**: quick 은 변경 파일 ≤ 5 가 기본. deep 은 4개 에이전트 병렬 — 비용/시간이 크므로 대규모 변경에만 사용
- **export default 금지**: Architecture 카테고리에서 `export default` 를 ⚠️ 경고로 검출. named export 만 허용하는 프로젝트 정책 반영

React 프로젝트의 6개 카테고리 코드 품질 감사.

## 0. 프로젝트 감지

`references/project-detection.md` 의 절차를 실행하여 프로젝트 환경을 파악한다.

| 감지 키 | 영향받는 검사 |
|---------|-------------|
| `crates/core/` 존재 | Performance — WASM boundary 검사 활성화 |
| `lingui.config.ts` 존재 | Accessibility — 하드코딩 i18n 문자열 검사 활성화 |
| `src-tauri/` 존재 | Library Policy — Tauri API 가드 검사 활성화 |
| Clean Arch 구조 감지 | Architecture — 레이어 경계 검사 활성화 |

## Input

`$ARGUMENTS` 파싱:

- `quick [path]` — quick 모드 강제
- `deep [path]` — deep 모드 강제
- `[path]` 또는 (인자 없음) — auto 모드: 변경 파일 수로 자동 선택

## Auto 모드

인자에 `quick` / `deep` 키워드가 없으면 변경 파일 수를 기준으로 모드를 결정한다.

```bash
git diff --name-only HEAD
git diff --name-only --cached
```

| 변경 파일 수 | 모드 | 예상 소요 시간 |
|-------------|------|--------------|
| 1~20 | Quick | 10초~2분 |
| 21~50 | Deep 권장 (사용자 확인 후 실행) | 3~8분 |
| 51+ | Deep 강제 | 5~15분 |

---

## Quick 모드

단일 `react-reviewer` 에이전트 호출. 변경 파일(또는 지정 경로)을 6개 카테고리 체크리스트로 직접 검사한다.

### 1. Architecture

Clean Architecture 레이어 경계 위반을 검출한다. domain 이 data/presentation 을 알면 도메인 로직이 인프라에 오염된다.

- [ ] **Clean Arch 경계 위반** (`domain` 이 `data`/`presentation` import) → ❌ 실패
  - grep: `^import .* from ['"]@/(data|presentation|infrastructure)/`
  - scope: `src/domain/**/*.ts`
- [ ] **Feature 간 직접 import** (`features/a` → `features/b` 직접 참조) → ❌ 실패
  - grep: `^import .* from ['"]@/presentation/features/(?!<currentFeature>)`
- [ ] **Infrastructure 역참조** (`domain` 이 `infrastructure/*` import) → ❌ 실패
  - grep: `^import .* from ['"]@/infrastructure/`
  - scope: `src/domain/**/*.ts`
- [ ] **상대 경로 3단계 이상** (`'../../../'`) → ⚠️ 경고
  - grep: `^import .* from ['"]\.\./\.\./\.\./`
- [ ] **`export default` 사용** → ⚠️ 경고
  - grep: `^export default `

### 2. Strict TypeScript

타입 안전성을 저해하는 패턴을 검출한다. `any` 와 `!` 는 런타임 오류를 정적 분석으로 잡을 수 없게 만든다.

- [ ] **`any` 사용** → ❌ 실패
  - grep: `: any\b|<any>|as any\b`
  - ESLint rule: `@typescript-eslint/no-explicit-any`
- [ ] **`!` non-null 단언** → ❌ 실패
  - grep: `\w+!\.\w+|\w+!\[|\w+!\s*[,)]`
  - ESLint rule: `@typescript-eslint/no-non-null-assertion`
- [ ] **`as` 타입 단언** (`as const` 제외) → ⚠️ 경고
  - grep: ` as [A-Z][a-zA-Z]+\b` (exclude `as const`)
  - ESLint rule: `@typescript-eslint/consistent-type-assertions`
- [ ] **`React.FC` 사용** → ⚠️ 경고
  - grep: `React\.FC<|: FC<`
- [ ] **public API return type 누락** → ⚠️ 경고
  - ESLint rule: `@typescript-eslint/explicit-module-boundary-types`

### 3. Performance

WASM boundary 오용과 불필요한 렌더 비용을 검출한다.

- [ ] **WASM 함수를 렌더 안에서 직접 호출** (useMemo 없이) → ❌ 실패
  - 검사: JSX return 블록 안에서 `@/data/datasources/wasm/` 심볼 직접 호출 + 상위 `useMemo` 없음
- [ ] **WASM 카탈로그 위반** (비권장 이식 패턴) → ❌ 실패
  - 판정: `docs/react/wasm-catalog.md` §2 카테고리 테이블 기준
- [ ] **문자열 마샬링 과다** (고빈도 string 인자 반복) → ⚠️ 경고
  - 검사: `@/data/datasources/wasm/` 함수에 `string` 타입 인자 + 고빈도 호출 추정
- [ ] **WASM Worker 누락** (직접 import, Worker 경유 안 함) → ⚠️ 경고
  - grep: `from ['"]@/wasm/` (직접 import)
- [ ] **번들 크기** 단일 chunk > 500KB gzip → ⚠️ 경고
  - 검사: `vite build --mode production` 후 `dist/assets/*.js` 크기
- [ ] **TanStack Query `staleTime` 누락** → ⚠️ 경고
  - 검사: `useQuery({ ... })` 호출에 `staleTime` 필드 없음

### 4. Accessibility

사용자 접근성 원칙을 검출한다. 누락된 ARIA 와 keyboard 경로는 보조 기술 사용자를 배제한다.

- [ ] **하드코딩 i18n 문자열** (한국어/영어를 매크로 미경유로 렌더) → ⚠️ 경고
  - grep: `>[^<{]*[가-힣A-Za-z][^<{]*<` (in .tsx), `<Trans>` / `` t`...` `` 내부 제외
- [ ] **`aria-*` 누락** (인터랙티브 요소) → ⚠️ 경고
  - ESLint rule: `jsx-a11y/accessible-name`
- [ ] **keyboard 경로 누락** (드래그 가능 요소에 onKeyDown / tabIndex 없음) → ⚠️ 경고
  - 검사: `useDrag` 사용 컴포넌트에 `onKeyDown` 또는 `role="button"` + `tabIndex` 없음
- [ ] **`prefers-reduced-motion` 가드 누락** → ⚠️ 경고
  - grep: `animate-` 또는 `transition-` 클래스 있는데 `motion-reduce:` 또는 `@media (prefers-reduced-motion` 없음
- [ ] **최상위 Error Boundary 없음** → ❌ 실패
  - grep: `src/main.tsx` 또는 `src/app.tsx` 에 `ErrorBoundary` 없음
- [ ] **WCAG 2.2 SC 2.5.8 Target Size (Minimum) AA — 24×24 미만** → ⚠️ 경고
  - 검사: 인터랙티브 요소(`<button>`, `<a>`, `<input type="button|submit|checkbox|radio">`, `[role="button"]`, `[role="link"]`) 의 Tailwind size 유틸에서 `h-*` / `w-*` / `size-*` / `min-h-*` / `min-w-*` 가 6(24px) 미만인 경우
  - grep: `(?:h|w|size|min-h|min-w)-[0-5]\b` (Tailwind scale 0~5 = 0~20px)
  - 예외: inline 텍스트 링크, user-agent 기본 컨트롤 (no class override), `pointer: coarse` 미디어 쿼리로 터치 디바이스에서만 확장하는 패턴
  - 근거: WCAG 2.2 (2023-10 공식 발효) — Phase 6 design-kit 정합 기준
- [ ] **WCAG 2.2 SC 2.4.11 Focus Not Obscured (Minimum) AA** → ⚠️ 경고
  - 검사: `position: sticky` 또는 `fixed` 가 있는 컨테이너 (header, footer, bottom-sheet) 에 focus ring 이 가려질 때, 대상 요소가 스크롤 영역이라면 `scroll-mt-*` / `scroll-padding-top` 선언 필요
  - 권장: `scroll-mt-16` 이상 또는 `:focus-visible { scroll-margin-top: 4rem; }`

### 5. Anti-patterns

코드 설계상 바람직하지 않은 일반 패턴. Library Policy 와 별도 카테고리.

- [ ] **빈 try/catch** → ❌ 실패
  - grep: `catch\s*\([^)]*\)\s*\{\s*\}`
- [ ] **`console.log` / `console.error` (production 코드)** → ⚠️ 경고
  - grep: `console\.(log|error|warn|debug)\(`
  - ESLint rule: `no-console`
- [ ] **domain 레이어에서 `throw new Error`** → ❌ 실패
  - grep: `throw new`
  - scope: `src/domain/**/*.ts`
- [ ] **`useState` + `useEffect` 로 서버 상태 관리** → ⚠️ 경고
  - 검사: `useState` 초기화 후 `useEffect` 안에서 fetch 패턴
- [ ] **컴포넌트 파일 400줄 초과** → ⚠️ 경고
  - 검사: 파일 line count
- [ ] **package.json patch 버전 고정** (캐럿/틸드 없음) → ⚠️ 경고
  - grep: `"[^"]+": "\d+\.\d+\.\d+"` (scope: `package.json`)

### 6. Library Policy (빌드 게이트급)

react-kit 이 금지하는 라이브러리. 위반 시 ❌ 실패 — 경고 없이 즉각 REJECT.

- [ ] **금지 애니메이션/인터랙션 라이브러리** → ❌ 실패
  - grep: `^import .* from ['"](motion|framer-motion|react-spring|@dnd-kit\/[^'"]*|react-dnd[^'"]*|react-beautiful-dnd|react-transition-group|gsap|lottie-react|@formkit\/auto-animate[^'"]*|animate\.css)['"]`
  - scope: `src/**/*.{ts,tsx}`
  - 금지 목록: `motion`, `framer-motion`, `@dnd-kit/*`, `react-spring`, `react-dnd`, `react-beautiful-dnd`, `react-transition-group`, `gsap`, `lottie-react`, `@formkit/auto-animate`, `animate.css`
  - 근거: react-kit 은 라이브러리 0개 원칙 고수 — `references/common-gotchas.md` G2 의 금지 목록과 정합. 추가는 가능, 삭제 금지.
- [ ] **deprecated shadcn 패키지** (`shadcn-ui`) → ❌ 실패
  - grep: `from ['"]shadcn-ui['"]` 또는 `package.json` 의 `"shadcn-ui"` dependency
- [ ] **deprecated MSW v1 API** (`rest.get` 등) → ⚠️ 경고
  - grep: `import \{[^}]*\brest\b[^}]*\} from ['"]msw['"]`
- [ ] **deprecated Lingui macro 경로** (`@lingui/macro`) → ⚠️ 경고
  - grep: `from ['"]@lingui/macro['"]`
  - 교체: JSX 매크로(`Trans`, `Plural`, `Select`, `SelectOrdinal`) → `from '@lingui/react/macro'`, core 매크로(`t`, `plural`, `select`, `selectOrdinal`, `defineMessage`, `msg`) → `from '@lingui/core/macro'`
  - 근거: Lingui v5 (2024-11 stable) 에서 `@lingui/macro` 단일 엔트리는 분리됐고 v5 에서도 alias 유지되지만 새 코드에서 사용 금지
- [ ] **Tauri API 직접 import** (isTauri 가드 없이, `src/infrastructure/tauri/` 외부에서) → ❌ 실패
  - grep: `^import .* from ['"]@tauri-apps/`
  - scope: `src/` 중 `src/infrastructure/tauri/` 제외
- [ ] **TanStack Query 외 서버 상태 라이브러리** → ⚠️ 경고
  - grep: `from ['"](swr|@apollo/client|react-query|urql)['"]`
- [ ] **비권장 상태 관리 라이브러리** (Redux, Jotai, Recoil) → ⚠️ 경고
  - grep: `from ['"](redux|react-redux|@reduxjs/toolkit|jotai|recoil)['"]`

---

## Deep 모드

4개 독립 서브에이전트를 병렬로 spawn. 각 에이전트는 특정 관점만 책임진다.

인자 없을 때 파일 목록 수집:

```bash
git diff --name-only HEAD
git diff --name-only --cached
```

Agent 도구를 사용하여 아래 4개 에이전트를 **동시에** 실행한다:

### Agent 1: react-reviewer (Architecture + Strict TS)

```text
다음 파일들의 Architecture 및 Strict TypeScript 규칙 준수 여부를 검사한다.

- Architecture: Clean Arch 레이어 경계 (domain/data/presentation), feature 간 직접 import, 상대 경로 3단계 이상, export default
- Strict TypeScript: any/!단언/as단언/React.FC/public API return type 누락

대상 파일: [파일 목록]
프로젝트 루트: [루트 경로]

각 위반마다 파일:라인, 규칙 ID, 심각도(error/warning), 수정 제안을 출력한다.
```

### Agent 2: react-reviewer (Performance + Anti-patterns)

```text
다음 파일들의 Performance 및 Anti-patterns 규칙 준수 여부를 검사한다.

- Performance: WASM 렌더 안 직접 호출, WASM 카탈로그 위반, 문자열 마샬링, Worker 누락, 번들 크기, staleTime 누락
- Anti-patterns: 빈 try/catch, console.log, domain throw, useState+fetch 패턴, 파일 400줄 초과, 버전 고정

대상 파일: [파일 목록]
wasm-catalog 경로: docs/react/wasm-catalog.md

각 위반마다 파일:라인, 규칙 ID, 심각도(error/warning), 수정 제안을 출력한다.
```

### Agent 3: react-reviewer (Accessibility + Library Policy)

```text
다음 파일들의 Accessibility 및 Library Policy 규칙 준수 여부를 검사한다.

- Accessibility: 하드코딩 i18n 문자열, aria-* 누락, keyboard 경로, prefers-reduced-motion, Error Boundary
- Library Policy: 금지 라이브러리(motion/framer-motion/dnd-kit/react-spring/react-transition-group/react-dnd/react-beautiful-dnd/gsap/lottie-react/@formkit/auto-animate), deprecated API

Library Policy 위반은 경고가 아닌 실패(error)로 분류한다.
대상 파일: [파일 목록]

각 위반마다 파일:라인, 규칙 ID, 심각도(error/warning), 수정 제안을 출력한다.
```

### Agent 4: widget-inspector-react (재사용 패턴)

G5 에서 정의된 에이전트를 병렬 5번째 축으로 실행한다.

```text
다음 파일들에서 재사용 가능한 컴포넌트 패턴을 감지한다.

- 구조적 중복: 비슷한 JSX 트리가 2곳 이상 반복
- 비대한 컴포넌트: 400줄 초과, 분리 가능한 서브트리 존재
- 범용 private 컴포넌트: feature 특화 로직 없는 _ComponentName 이 shared 추출 가능

대상 파일: [파일 목록]
shared 컴포넌트 경로: src/presentation/components/

각 후보마다 파일:라인, 감지 기준, 추출 제안(컴포넌트명 + 배치 경로)을 출력한다.
```

4개 에이전트 결과를 병합하여 최종 리포트를 생성한다. 같은 파일에 대한 중복 언급은 파일 기준으로 병합 후 카테고리별 그룹화한다.

---

## Report Format

```markdown
## /react-audit 리포트 (<날짜> <시각>)

**모드**: <quick|deep>
**변경 파일**: <N> 개
**판정**: **<APPROVE|REJECT>** (<N> 실패, <N> 경고)

### ❌ 실패 (<N>)
1. `<file>:<line>` — <설명> (<카테고리>)
...

### ⚠️ 경고 (<N>)
1. `<file>:<line>` — <설명> (<카테고리>)
...

### ✅ 통과 카테고리
- <카테고리명>: <간단한 이유>
...

### 권장 후속 작업
- <후속 작업 목록>
```

이슈가 없는 카테고리는 "통과 카테고리" 에만 표시한다. 감사 결과만 보고한다. 코드를 직접 수정하지 않는다.

## Rules

- **MUST** 6개 카테고리(Architecture, Strict TypeScript, Performance, Accessibility, Anti-patterns, Library Policy) 를 모두 검사한다
- **MUST** Library Policy 위반은 ⚠️ 경고가 아닌 ❌ 실패로 분류한다 (빌드 게이트급, 완화 금지)
- **MUST** 감사 결과만 보고한다. 코드를 직접 수정하지 않는다
- **MUST** 위반 보고 시 파일:라인, 규칙 ID, 심각도, 수정 제안을 포함한다. 위치 없는 보고 금지
- **MUST** `// react-audit-ignore: <rule>` 주석이 있는 라인은 해당 규칙 검사에서 제외한다
- **MUST** deep 모드에서 4개 에이전트를 순차가 아닌 병렬로 실행한다
- **MUST NOT** 카테고리별 독립 리포트 외에 "overview" / "종합 요약" 섹션을 생성한다 — 카테고리 경계를 흐리면 FAIL 심각도가 희석된다 (Phase 8 infra-kit 전수 원칙)
- **MUST NOT** 판정 사유에 "대체로", "거의", "대부분", "충분히" 같은 모호 표현을 사용한다 — `파일:라인`·`건수`·`규칙 ID` 로 서술 (Phase 2 contract-design-guide 정합)
- **MUST** Library Policy 금지 목록 확장 시 `react-kit/references/common-gotchas.md` G2 동기화 필수. 삭제는 빌드 게이트 훼손으로 금지 (Phase 10 LP-01)

## References

- `react-kit/references/project-detection.md` — 환경 감지 로직
- `react-kit/references/clean-arch-layout.md` — Architecture 카테고리 기준
- `react-kit/references/style-guide.md` — Strict TypeScript 카테고리 기준
- `docs/react/wasm-catalog.md` — Performance WASM 카탈로그 위반 판정 기준
- `react-kit/agents/react-reviewer.md` — quick 모드 단일 에이전트
- `react-kit/agents/widget-inspector-react.md` — deep 모드 재사용 패턴 에이전트
