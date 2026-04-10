# G4 — Quality & Patterns Skills

```yaml
last_updated: 2026-04-10
group: G4
scope: react-kit 품질 보증 + 에러 처리 + i18n 스킬 3종
skills: [/react-test, /react-error, /react-l10n]
depends_on: [G1 /react-init, G2 전체, G3 /react-wasm /react-tauri]
research_sources:
  - Vitest 공식 가이드 (vitest.dev/guide)
  - Testing Library React 문서 (testing-library.com)
  - Playwright Component Testing (playwright.dev/docs/test-components)
  - Lingui Macros + React 문서 (lingui.dev/ref/macro, lingui.dev/tutorials/react)
  - neverthrow 공식 (supermacro/neverthrow)
  - 2026-04 WebSearch 검증
```

## 문서 목적

react-kit **G4 그룹** 은 프로젝트의 품질을 보장하는 세 스킬이다.

- **`/react-test`** — Vitest (unit) + React Testing Library (component) + Playwright (e2e) 3단 테스트 피라미드. Clean Architecture 레이어별로 다른 테스트 전략을 자동 생성.
- **`/react-error`** — 데이터 경계의 예외를 `Failure` 로 변환, React 렌더 경계의 에러를 Error Boundary 로 포획, UI 표시를 Severity 에 따라 분기.
- **`/react-l10n`** — Lingui v5 매크로 기반 번역. `Trans` / `t` macro, Vite 플러그인, 자동 codegen, locale 파일 관리까지.

**의존**: G1 으로 설치된 Vitest, Testing Library, Playwright, Lingui, neverthrow 전제. G2 의 Result/Failure 패턴을 그대로 상속.

## 공통 설계 원칙

- **레이어 인식**: 모든 G4 스킬은 Clean Architecture 레이어를 의식한다. domain 순수 함수는 노드 환경에서, presentation hook/component 는 jsdom 환경에서, 전체 플로우는 Playwright 브라우저에서 — 계층별로 적합한 도구.
- **Result 친화**: 에러 경로 테스트는 throw 가 아니라 `Result.isErr()` 로 검증. UI 의 Error Boundary 는 최후의 안전망일 뿐 1차 에러 처리가 아님.
- **Strict TS 유지**: 테스트 코드도 `any` 금지. `expect(...).toBe(...)` 의 타입 추론을 활용해 strict 하게.
- **project-detection 재사용**: G1 의 project-detection 을 재사용해 Vitest / Playwright / Lingui 설치 여부, 버전, 설정 파일 위치를 감지.
- **i18n 커버리지**: 모든 presentation 레이어 문자열은 기본적으로 Lingui macro 경유. 하드코딩된 한국어 / 영어 문자열은 `/react-audit` 이 검출.

## 1. /react-test — 테스트 코드 자동 생성

대상 파일/클래스를 분석해 Vitest unit, Testing Library component, Playwright e2e 중 적합한 유형의 테스트를 자동 생성한다.

### 1.1 트리거

- 키워드: "테스트 만들어줘", "react-test", "unit test", "component test", "e2e test"
- 조건: G1 초기화 완료, 대상 파일 경로 제공

### 1.2 입력

- `target_path` (필수): 테스트 대상 파일 경로 (예: `src/domain/usecases/user-usecases.ts`)
- `test_type` (선택): `unit` / `component` / `e2e`. 없으면 대상 파일의 레이어에 따라 자동 선택
- `--coverage`: 커버리지 수집 활성화

### 1.3 Clean Architecture 레이어별 테스트 전략

| 레이어 | 테스트 유형 | 도구 | 특징 |
|--------|-----------|------|------|
| **domain/** (entities, usecases, failures) | Unit | Vitest (node 환경) | 순수 함수. 외부 의존성 없음. 빠르고 독립적. MSW 불필요 |
| **data/** (datasources, models, repositories) | Unit + integration | Vitest + MSW (fetch 모의) | fetch 모의, Zod parse 실패, Result 변환 경로 검증 |
| **presentation/hooks** (TanStack Query, Zustand) | Component test | Vitest + Testing Library + QueryClient wrapper | `renderHook`, `waitFor`, store 초기화 |
| **presentation/components** (위젯, 폼) | Component test | Vitest + Testing Library + jsdom | 렌더, 사용자 이벤트 (userEvent), 접근성 (getByRole) |
| **presentation/routes** (화면 전체) | E2E | Playwright | 실제 브라우저, 실 네트워크 또는 MSW, 라우팅·폼 제출 |
| **infrastructure/** (Tauri, WASM) | Integration | Vitest + mock or Playwright (Tauri 환경) | isTauri() 가짜, invoke 모의 |

### 1.4 Vitest Unit 테스트 패턴

`/react-test` 가 생성하는 domain usecase 테스트 예시:

```ts
// tests/unit/domain/usecases/user-usecases.test.ts
import { describe, it, expect } from 'vitest'
import { UserSchema } from '@/domain/entities/user'

describe('UserSchema', () => {
  it('accepts valid user shape', () => {
    const parsed = UserSchema.safeParse({
      id: '550e8400-e29b-41d4-a716-446655440000',
      email: 'jane@example.com',
      name: 'Jane',
      createdAt: '2026-04-10T00:00:00Z',
    })
    expect(parsed.success).toBe(true)
  })

  it('rejects missing email', () => {
    const parsed = UserSchema.safeParse({
      id: '550e8400-e29b-41d4-a716-446655440000',
      name: 'Jane',
      createdAt: '2026-04-10T00:00:00Z',
    })
    expect(parsed.success).toBe(false)
  })
})
```

Repository 테스트 — MSW 로 fetch 모의:

```ts
// tests/unit/data/repositories/user-repository.test.ts
import { describe, it, expect, beforeAll, afterEach, afterAll } from 'vitest'
import { setupServer } from 'msw/node'
import { http, HttpResponse } from 'msw'
import { userRepository } from '@/data/repositories/user-repository'

const server = setupServer()
beforeAll(() => server.listen())
afterEach(() => server.resetHandlers())
afterAll(() => server.close())

describe('userRepository.fetchUser', () => {
  it('returns ok(User) on 200', async () => {
    server.use(
      http.get('*/users/123', () =>
        HttpResponse.json({
          id: '123',
          email_address: 'jane@example.com',
          display_name: 'Jane',
          created_at: '2026-04-10T00:00:00Z',
        }),
      ),
    )
    const result = await userRepository.fetchUser('123')
    expect(result.isOk()).toBe(true)
    if (result.isOk()) {
      expect(result.value.email).toBe('jane@example.com')
    }
  })

  it('returns err(not-found) on 404', async () => {
    server.use(http.get('*/users/999', () => new HttpResponse(null, { status: 404 })))
    const result = await userRepository.fetchUser('999')
    expect(result.isErr()).toBe(true)
    if (result.isErr()) {
      expect(result.error.kind).toBe('user/not-found')
    }
  })
})
```

### 1.5 Testing Library Component 테스트 패턴

컴포넌트는 jsdom 환경 + Testing Library queries + user-event 로:

```ts
// tests/component/LoginForm.test.tsx
import { describe, it, expect, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { ok, err } from 'neverthrow'
import { LoginForm } from '@/presentation/features/auth/components/login-form'

describe('LoginForm', () => {
  it('shows validation error when email is empty', async () => {
    const user = userEvent.setup()
    const onSubmit = vi.fn().mockResolvedValue(ok(undefined))
    render(<LoginForm onSubmit={onSubmit} />)

    await user.click(screen.getByRole('button', { name: /로그인/i }))
    expect(await screen.findByText(/올바른 이메일/i)).toBeInTheDocument()
    expect(onSubmit).not.toHaveBeenCalled()
  })

  it('calls onSubmit with values and shows server error on Result.err', async () => {
    const user = userEvent.setup()
    const onSubmit = vi.fn().mockResolvedValue(err({ kind: 'login/invalid-credentials' as const }))
    render(<LoginForm onSubmit={onSubmit} />)

    await user.type(screen.getByLabelText(/이메일/i), 'jane@example.com')
    await user.type(screen.getByLabelText(/비밀번호/i), 'password123')
    await user.click(screen.getByRole('button', { name: /로그인/i }))

    expect(onSubmit).toHaveBeenCalledWith({ email: 'jane@example.com', password: 'password123' })
    expect(await screen.findByText(/이메일 또는 비밀번호가 올바르지 않습니다/i)).toBeInTheDocument()
  })
})
```

**핵심 규칙**:
- **`getByRole` 우선** — `getByTestId` 는 마지막 수단. 접근성 기반 쿼리가 실제 사용자 경험에 가깝다
- **`userEvent` 사용** — `fireEvent` 대신. 실제 키보드/마우스 이벤트에 가까움
- **`findBy*` 는 비동기** — `await` 필수. `getBy*` 는 동기 (없으면 즉시 throw)

### 1.6 Playwright E2E 패턴

화면 전체 플로우는 Playwright 로 실제 브라우저에서:

```ts
// tests/e2e/login.spec.ts
import { test, expect } from '@playwright/test'

test('user can log in and see dashboard', async ({ page }) => {
  await page.goto('/login')
  await page.getByLabel('이메일').fill('jane@example.com')
  await page.getByLabel('비밀번호').fill('password123')
  await page.getByRole('button', { name: '로그인' }).click()
  await expect(page).toHaveURL(/\/dashboard/)
  await expect(page.getByRole('heading', { name: /환영합니다/ })).toBeVisible()
})
```

**Tauri e2e**: `@playwright/experimental-ct-react` 또는 Tauri webdriver 로 데스크탑 앱까지 커버 가능. 기본 템플릿은 웹 타겟만 — Tauri e2e 는 옵션.

### 1.7 에러 경로 테스트 패턴

Result 패턴은 throw 가 없기 때문에 전통적인 `expect(() => ...).toThrow()` 가 아니라 **`isErr()` 체크** 로 검증한다:

```ts
it('returns invalid-format Failure when API returns bad shape', async () => {
  server.use(
    http.get('*/users/123', () => HttpResponse.json({ wrong: 'shape' })),
  )
  const result = await userRepository.fetchUser('123')
  expect(result.isErr()).toBe(true)
  if (result.isErr()) {
    expect(result.error.kind).toBe('user/validation-failed')
    expect(result.error.issues.length).toBeGreaterThan(0)
  }
})
```

Error Boundary 테스트 — 의도적으로 throw 하는 자식으로 경계를 트리거:

```ts
it('Error Boundary catches render-time error and shows fallback', () => {
  const Boom = () => {
    throw new Error('render boom')
  }
  render(
    <RootErrorBoundary>
      <Boom />
    </RootErrorBoundary>,
  )
  expect(screen.getByText(/예기치 못한 오류/i)).toBeInTheDocument()
})
```

### 1.8 Gotchas

- **vitest.config 에 jsdom 환경 명시**: component 테스트 파일은 jsdom, unit 테스트는 node. `environmentMatchGlobs` 로 경로별 분리 권장
- **`setupFiles` 필수**: `@testing-library/jest-dom` matchers 를 전역 등록하려면 setup 파일에서 `expect.extend(matchers)` 실행
- **`cleanup()` 자동**: Testing Library 는 각 테스트 후 자동 DOM 정리하지만 글로벌 모드에서는 `afterEach(cleanup)` 명시 권장
- **Playwright 과 Vitest 병존**: 둘 다 "test" 라는 이름을 쓴다. Playwright 는 `playwright.config.ts`, Vitest 는 `vitest.config.ts` 로 분리. 테스트 파일 확장자도 `.spec.ts` (Playwright) vs `.test.ts` (Vitest) 로 구분 권장
- **fetch 모의는 MSW 우선**: `vi.stubGlobal('fetch', ...)` 같은 저수준 목은 피하고 MSW 로. 요청 shape 을 문서로 남기는 효과
- **MSW v2 API 변경**: 구 `rest.get(...)` 가 아니라 `http.get(...)` + `HttpResponse`. deprecated API 사용 금지
- **비동기 assertion 까먹기 쉬움**: `findBy*` 는 반드시 await. 까먹으면 pending Promise 로 테스트가 false positive
- **Strict TS**: `vi.mocked(...)` 로 모킹한 객체의 타입 안전성 유지. `as any` 금지

### 1.9 Clean Architecture 배치

- **unit 테스트**: `tests/unit/<layer>/<module>.test.ts`
- **component 테스트**: `tests/component/<Name>.test.tsx`
- **e2e 테스트**: `tests/e2e/<flow>.spec.ts`
- **MSW 서버 설정**: `tests/__mocks__/server.ts` (shared)

## 2. /react-error — 에러 처리 패턴 생성

데이터 경계의 throw → Failure 변환, React 렌더 경계의 Error Boundary, UI 표시 매핑을 세팅한다.

### 2.1 트리거

- 키워드: "에러 처리", "Failure", "Error Boundary", "react-error", "에러 표시"
- 조건: G1 초기화 완료 (`neverthrow` 설치됨)

### 2.2 입력

- `scope`: `global` (앱 전체 ErrorBoundary + toast/snackbar 시스템) 또는 `feature` (특정 feature 의 Failure 타입 + UI 매핑)
- `feature_name` (scope = feature 일 때 필수)

### 2.3 3단계 에러 처리 흐름

```
[데이터 경계]             [도메인/프레젠테이션 전파]         [사용자 표시]
throw / reject  ──────►   Result<T, Failure>   ──────►     Severity → UI 선택
(fetch, WASM, Tauri)      (neverthrow chain)                (snackbar / dialog / page)

                                 │
                                 ▼
                          [예외적으로 탈출한 에러]
                            React Error Boundary
                                 │
                                 ▼
                              Fallback UI
```

### 2.4 Step 1 — 데이터 경계에서 throw → Failure 변환

G2 `/react-api` 가 이미 이 패턴을 생성한다. 복습:

```ts
// src/data/datasources/remote/user-api.ts
export function fetchUserDto(id: string): ResultAsync<unknown, UserFailure> {
  return ResultAsync.fromPromise(
    fetch(`${BASE}/users/${id}`).then(async (r) => {
      if (r.status === 404) throw { kind: 'user/not-found', userId: id }
      if (!r.ok) throw { kind: 'user/network-error', cause: r.statusText }
      return r.json()
    }),
    (e) => (isUserFailure(e)
      ? e
      : { kind: 'user/network-error', cause: String(e) }),
  )
}
```

**규칙**:
- throw 는 datasource 내부에서만. 즉시 `ResultAsync.fromPromise` 의 두 번째 인자에서 Failure 로 변환
- Failure 는 discriminated union. `kind` 필드로 분기
- cause 필드에 원본 에러 메시지 보존 (디버깅용)

### 2.5 Step 2 — Failure 전파 + Severity 매핑

`/react-error` 가 생성하는 Failure 확장 패턴:

```ts
// src/domain/failures/user-failures.ts
export type Severity = 'info' | 'warning' | 'error' | 'fatal'

export type UserFailure =
  | { kind: 'user/not-found'; userId: string }
  | { kind: 'user/unauthorized' }
  | { kind: 'user/network-error'; cause: string }
  | { kind: 'user/validation-failed'; issues: string[] }
  | { kind: 'user/rate-limited'; retryAfterSec: number }

export function severityOf(failure: UserFailure): Severity {
  switch (failure.kind) {
    case 'user/not-found':
      return 'info'       // 사용자 인지 충분
    case 'user/rate-limited':
      return 'warning'    // 일시적, 재시도 안내
    case 'user/unauthorized':
    case 'user/validation-failed':
      return 'error'      // 사용자 액션 필요
    case 'user/network-error':
      return 'fatal'      // 네트워크 자체 문제
  }
}
```

Severity 는 **사용자 관점의 심각도** 이지 기술적 에러 레벨이 아니다. "네트워크 없음" 은 기술적으로 warning 급이지만 사용자에겐 fatal.

### 2.6 Step 3 — UI 표시 매핑

Severity → 표시 위치/형태 매핑 규칙:

| Severity | 표시 형태 | 위치 | 상호작용 |
|----------|----------|------|---------|
| `info` | Toast (자동 dismiss) | 화면 우하단 | 없음 |
| `warning` | Snackbar (action 포함) | 화면 하단 | "다시 시도" 버튼 등 |
| `error` | Inline error (필드 옆 / 폼 최상단) or Dialog | 관련 위치 | 사용자 액션 유도 |
| `fatal` | Full page error or Modal | 전체 | 새로고침 / 로그아웃 안내 |

**구현 예시** — shadcn `Toaster` 기반:

```ts
// src/presentation/shared/lib/display-failure.ts
import { toast } from 'sonner'   // shadcn/ui 권장 toast 라이브러리

type FailureLike = { kind: string; cause?: string }

export function displayFailure(failure: FailureLike, severity: Severity): void {
  switch (severity) {
    case 'info':
      toast.info(toUserMessage(failure))
      break
    case 'warning':
      toast.warning(toUserMessage(failure), {
        action: { label: '다시 시도', onClick: () => { /* retry */ } },
      })
      break
    case 'error':
      toast.error(toUserMessage(failure))
      break
    case 'fatal':
      // Zustand store 에 fatal 플래그 설정 → 최상단 FullPageError 가 렌더
      useAppStore.getState().setFatalError(failure)
      break
  }
}

function toUserMessage(failure: FailureLike): string {
  // Failure kind → 사용자용 번역 키. Lingui 로 i18n 화 (G4 /react-l10n 참조)
  // ...
  return '...'
}
```

### 2.7 React Error Boundary

**Result 패턴이 커버 못 하는 것**: React 렌더 중 throw. 이걸 Error Boundary 가 잡는다.

```tsx
// src/presentation/shared/components/root-error-boundary.tsx
import * as React from 'react'

type Props = { children: React.ReactNode }
type State = { hasError: boolean; error: Error | null }

export class RootErrorBoundary extends React.Component<Props, State> {
  state: State = { hasError: false, error: null }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error }
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo): void {
    console.error('RootErrorBoundary:', error, errorInfo)
    // 프로덕션: Sentry 같은 서비스로 전송
  }

  render(): React.ReactNode {
    if (this.state.hasError) {
      return (
        <div role="alert" className="flex min-h-screen items-center justify-center">
          <div className="space-y-4 text-center">
            <h1 className="text-2xl font-semibold">예기치 못한 오류</h1>
            <p className="text-muted-foreground">{this.state.error?.message}</p>
            <button onClick={() => window.location.reload()}>새로고침</button>
          </div>
        </div>
      )
    }
    return this.props.children
  }
}
```

Error Boundary 는 **최후의 안전망**. 1차 에러 처리는 Result 로. Error Boundary 가 자주 열리면 그건 Result 패턴에 구멍이 있다는 신호.

### 2.8 Gotchas

- **비동기 에러는 Error Boundary 가 못 잡음**: `useEffect` 안의 throw, Promise reject 는 Error Boundary 에 도달 안 함. Result 로 반드시 감쌀 것
- **Error Boundary 는 클래스 컴포넌트 필수**: React 19 에서도 아직 hooks 로 구현 불가. `react-error-boundary` 같은 라이브러리 사용은 옵션 (하지만 기본은 자체 구현)
- **Toast 라이브러리 선택**: shadcn/ui 는 `sonner` 를 권장. Radix 기반 `<Toaster />` 와 겹치지 않게 하나만 선택
- **fatal 상태 관리**: Zustand store 에 `fatalError: Failure | null` 필드를 두고 최상위 컴포넌트에서 렌더 분기
- **개발 환경 Boundary 우회**: Vite dev 모드에서 Error Boundary 가 렌더 에러를 잡지 못하는 것처럼 보일 수 있음 (React 는 dev 에서 에러를 re-throw 해서 개발자가 볼 수 있게 함). 프로덕션 빌드로 확인 필요
- **Failure 를 Error 로 감싸지 말 것**: Failure 는 그 자체가 타입 안전 값. `new Error(JSON.stringify(failure))` 같은 변환은 stack trace 를 의미 없게 만들고 타입 정보 손실
- **Strict TS**: Failure discriminated union 의 모든 kind 를 switch 에서 다뤘는지 `never` 타입으로 exhaustiveness 검증

### 2.9 Clean Architecture 배치

- **Failure 타입**: `src/domain/failures/<resource>-failures.ts`
- **Severity 매핑 함수**: 같은 파일 (`severityOf(failure)`)
- **UI 표시 유틸**: `src/presentation/shared/lib/display-failure.ts`
- **Error Boundary**: `src/presentation/shared/components/root-error-boundary.tsx`
- **Fatal error store**: `src/presentation/shared/stores/app-store.ts` (Zustand)

## 3. /react-l10n — Lingui 기반 i18n

Lingui v5 의 매크로 기반 번역 문자열 추가, 자동 codegen, locale 전환 흐름을 자동화한다.

### 3.1 트리거

- 키워드: "다국어", "번역 추가", "i18n", "react-l10n", "l10n key"
- 조건: G1 초기화로 Lingui 가 설치되어 있고 `lingui.config.ts` 존재

### 3.2 입력

- `message` (필수): 번역할 원본 문자열 (영어 또는 한국어)
- `context` (선택): 번역자용 컨텍스트 (예: "로그인 버튼 레이블")
- `component_path` (선택): 문자열을 삽입할 컴포넌트 파일 경로

### 3.3 Lingui 기본 구조 (G1 생성)

```
src/
├── infrastructure/i18n/
│   ├── setup.ts             # i18n.loadAndActivate 초기화
│   └── locales/
│       ├── en.po            # 영어 catalog (원본)
│       ├── ko.po            # 한국어 catalog
│       └── ja.po            # 일본어 catalog (선택)
├── presentation/
│   └── features/
│       └── auth/
│           └── components/login-form.tsx   # macro 사용
```

`lingui.config.ts`:

```ts
import { defineConfig } from '@lingui/cli'

export default defineConfig({
  sourceLocale: 'en',
  locales: ['en', 'ko', 'ja'],
  catalogs: [
    {
      path: 'src/infrastructure/i18n/locales/{locale}',
      include: ['src'],
    },
  ],
})
```

Vite 플러그인 (`vite.config.ts`):

```ts
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react-swc'
import { lingui } from '@lingui/vite-plugin'

export default defineConfig({
  plugins: [
    react({ plugins: [['@lingui/swc-plugin', {}]] }),
    lingui(),
  ],
})
```

### 3.4 번역 매크로 사용 패턴

Lingui v5 는 매크로 import 경로를 구분한다. JSX 는 `@lingui/react/macro` (Trans), 문자열 / 함수 호출은 `@lingui/react/macro` 의 `useLingui` (v5 신규) 또는 `@lingui/core/macro` (msg).

**JSX 내부 — `Trans` 컴포넌트**:

```tsx
import { Trans } from '@lingui/react/macro'

export function Welcome({ name }: { name: string }) {
  return (
    <h1>
      <Trans>안녕하세요, {name}님!</Trans>
    </h1>
  )
}
```

컴파일 시 `<Trans id="abc123" message="안녕하세요, {name}님!" values={{ name }} />` 로 변환됨. id 는 해시 자동 생성.

**문자열 / 동적 함수 — `useLingui` 의 `t`**:

```tsx
import { useLingui } from '@lingui/react/macro'

export function SubmitButton({ disabled }: { disabled: boolean }) {
  const { t } = useLingui()
  return (
    <button disabled={disabled} aria-label={t`제출`}>
      {t`로그인`}
    </button>
  )
}
```

**매크로 규칙**:
- `<Trans>` → JSX 내부의 선언적 번역
- `t` macro (`useLingui` 경유) → 속성 값, 동적 문자열, 함수 반환값
- `msg` macro → 컴포넌트 밖 (상수 정의, reducer message 등)

### 3.5 번역 추가 + codegen 흐름

`/react-l10n` 이 "로그인" 이라는 한국어 문자열을 추가할 때:

1. 대상 컴포넌트에 매크로 삽입 (`<Trans>로그인</Trans>` 또는 `t\`로그인\``)
2. 소스 import 추가 (`import { Trans } from '@lingui/react/macro'`)
3. 추출 명령 실행: `pnpm lingui extract` — 코드에서 매크로를 스캔해 `en.po` 에 새 키 추가
4. 각 locale 파일 (`ko.po`, `ja.po`) 에 빈 번역 엔트리 자동 생성
5. 사용자에게 "ko.po 에 번역 추가하세요" 안내 — **번역 자체는 사람이 입력**
6. compile: `pnpm lingui compile` — `.po` → `.js` 컴파일된 catalog 생성 (Vite 플러그인이 자동 수행)

**CLI 명령**:

```sh
pnpm lingui extract                   # 소스 → .po 동기화
pnpm lingui compile                   # .po → runtime catalog
pnpm lingui extract --clean           # 삭제된 키 정리
```

### 3.6 Locale 전환

```ts
// src/infrastructure/i18n/setup.ts
import { i18n } from '@lingui/core'
import { messages as en } from './locales/en'
import { messages as ko } from './locales/ko'

export async function activateLocale(locale: 'en' | 'ko' | 'ja'): Promise<void> {
  i18n.load(locale, locale === 'en' ? en : ko)   // 필요 시 동적 import 로 lazy
  i18n.activate(locale)
}

// 초기화
activateLocale(navigator.language.startsWith('ko') ? 'ko' : 'en')
```

`<I18nProvider i18n={i18n}>` 로 App 최상단 래핑 (Lingui React API). 이 Provider 가 없으면 매크로가 동작 안 함.

**Lazy load** (번들 크기 최적화):

```ts
export async function activateLocale(locale: string): Promise<void> {
  const { messages } = await import(`./locales/${locale}.po`)
  i18n.load(locale, messages)
  i18n.activate(locale)
}
```

### 3.7 Gotchas

- **매크로 import 경로 혼동**: v5 에서 `@lingui/macro` (구버전) 가 `@lingui/react/macro` (JSX/React) 와 `@lingui/core/macro` (core) 로 분리됨. 잘못 import 하면 컴파일 단계에서 매크로가 적용 안 됨
- **`msgid` 대신 해시 id 기본**: v5 는 코드에서 원본 문자열을 자동 해시해 id 생성. 직접 id 지정하려면 `<Trans id="custom.id" />` 명시
- **translation 누락**: `extract` 후 `ko.po` 에 빈 msgstr 로 남은 키는 런타임에 원본 (en) 으로 fallback. `/react-audit` 이 "빈 번역 키" 카운트로 경고
- **plurals, interpolation**: `<Plural>`, `<Select>` 같은 전용 macro 사용. `{count} 개` 처럼 단순 치환은 `<Trans>` 안에서 `{count}` 그대로
- **Vite 플러그인 순서**: `react({ plugins: [['@lingui/swc-plugin', {}]] })` 가 반드시 lingui plugin 앞. SWC 가 매크로를 transpile 한 뒤에 lingui plugin 이 catalog 를 주입
- **Strict TS**: 매크로는 타입을 잘 추론하지만, 동적 key 는 `msg\`...\`` 로 감싸고 `i18n._(msg)` 로 호출. `any` 사용 금지
- **서버 컴포넌트는 쓰지 않음**: react-kit 기본 구성 (Vite + TanStack Router) 은 SSR 없음. Lingui RSC 지원은 관련 없음

### 3.8 Clean Architecture 배치

- **번역 매크로 사용**: `src/presentation/**/*.tsx` — presentation 레이어만
- **locale catalog**: `src/infrastructure/i18n/locales/<locale>.po` + compiled `.ts`
- **i18n setup**: `src/infrastructure/i18n/setup.ts`
- **config**: `lingui.config.ts` (프로젝트 루트)
- **절대 금지**: `domain/` 에 매크로 import. 도메인 레이어는 i18n 을 모른다. Failure 의 사용자 메시지는 presentation 레이어 (`display-failure.ts`) 에서 매핑

## 4. 3개 스킬의 상호작용

```
컴포넌트 생성 (G1 /react-widget, /react-screen)
         │
         ▼
/react-l10n              ←── 하드코딩된 문자열을 매크로로 교체
         │
         ▼
/react-error             ←── Failure 타입 정의 + severity 매핑 + Error Boundary
         │
         ▼
/react-test              ←── unit + component + e2e 테스트 생성
         │                    └─ 에러 경로 (isErr) + 번역 렌더 포함
         ▼
/react-preflight (G6)    ←── 전체 quality gate (tsc + eslint + vitest + playwright)
```

## 5. 공유 helpers 및 Cross-group 관계

- **G1 project-detection** 재사용: Vitest / Playwright / Lingui 설치 여부, 설정 파일 위치 감지
- **G2 Result/Failure** 패턴을 G4 `/react-error` 가 확장 (severity, UI 매핑 추가)
- **G3 WASM/Tauri** 테스트: `/react-test` 가 infrastructure 레이어 테스트 케이스로 WASM mock, Tauri invoke mock 템플릿 제공
- **G5 UI 패턴** (`/react-skeleton`) 의 로딩 상태 테스트 케이스 자동 생성
- **G6 `/react-audit`** 가 G4 출력물에서:
  - `toBe()` 없이 `findBy*` 대기 없는 assertion 누락
  - Failure switch 의 exhaustiveness 위반
  - 하드코딩된 i18n 문자열 (매크로 미사용)
  - Error Boundary 없는 최상위 컴포넌트
  - 이 모든 것을 검출

## 6. 출처 요약

1. Vitest 공식 가이드: https://vitest.dev/guide/
2. Vitest — Component Testing: https://vitest.dev/guide/browser/component-testing
3. Vitest GitHub: https://github.com/vitest-dev/vitest
4. Testing Library React 문서: https://testing-library.com/docs/
5. Playwright Component Testing (experimental): https://playwright.dev/docs/test-components
6. Playwright Fixtures: https://playwright.dev/docs/test-fixtures
7. Playwright Migrating from Testing Library: https://playwright.dev/docs/testing-library
8. Lingui 공식 사이트: https://lingui.dev/
9. Lingui Macros 레퍼런스: https://lingui.dev/ref/macro
10. Lingui Vite 셋업: https://lingui.dev/tutorials/setup-vite
11. Lingui React API: https://lingui.dev/ref/react
12. Lingui Vite Plugin: https://lingui.dev/ref/vite-plugin
13. Lingui React 튜토리얼: https://lingui.dev/tutorials/react
14. js-lingui GitHub: https://github.com/lingui/js-lingui
15. neverthrow GitHub: https://github.com/supermacro/neverthrow

## 7. 변경 이력

- **2026-04-10** — 초판. G4 3개 스킬 (`/react-test`, `/react-error`, `/react-l10n`) 상세 설계. WebSearch fallback 으로 Vitest v2, Testing Library React, Playwright Component Test, Lingui v5 매크로 (v5 에서 `@lingui/react/macro` 경로 분리) 검증. G2 Result/Failure 패턴을 severity + UI 매핑으로 확장.
