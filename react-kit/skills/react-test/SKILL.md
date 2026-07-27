---
name: react-test
description: >
  대상 파일/클래스를 분석하여 테스트 코드를 자동 생성한다.
  Clean Architecture 레이어별로 Vitest unit, Testing Library component, Playwright e2e 세 가지 전략 중 적합한 유형을 선택해 생성.
  "테스트 만들어줘", "unit test 생성", "vitest 테스트", "component test", "Playwright e2e", "테스트 코드 생성" 같은 요청 시 트리거.
  테스트 실행만 할 때는 /react-run을 사용한다.
argument-hint: "<file-or-class-path> [unit|component|e2e] [--coverage]"
user-invocable: true
---

## Gotchas

1. **domain 테스트에서 직접 fetch/API 호출 금지** — domain 레이어(usecases, entities, failures)는 순수 함수이므로 외부 의존성이 없어야 한다. 네트워크 호출이 필요하면 대상 파일이 data 레이어인지 재확인하고 MSW 로 모킹하라.
2. **에러 경로는 `isErr()` 로 검증** — Result 패턴에서 throw 가 없기 때문에 `expect(() => ...).toThrow()` 대신 `expect(result.isErr()).toBe(true)` + kind 체크로 검증한다.
3. **MSW v2 API 사용 필수** — 구 `rest.get(...)` 가 아니라 `http.get(...)` + `HttpResponse`. deprecated API 사용 금지.
4. **`findBy*` 는 반드시 `await`** — `getBy*` 는 동기(없으면 즉시 throw), `findBy*` 는 비동기(Promise 반환). await 없이 쓰면 pending Promise 를 받아 false positive 발생.
5. **`getByRole` 우선** — `getByTestId` 는 마지막 수단. 접근성 기반 쿼리가 실제 사용자 경험에 가깝고 리팩터링 내성이 높다.
6. **vitest.config `environment` 경로별 분리** — component 테스트는 jsdom, unit 테스트는 node. `environmentMatchGlobs` 로 경로별 분리하지 않으면 node 환경에서 DOM API 호출로 에러 발생.
7. **`setupFiles` 필수** — `@testing-library/jest-dom` matchers 를 전역 등록하려면 setup 파일에서 `import '@testing-library/jest-dom'` 을 실행해야 한다.
8. **Playwright 과 Vitest 파일 확장자 분리** — Playwright 은 `.spec.ts`, Vitest 는 `.test.ts`. 혼용하면 두 러너가 같은 파일을 동시에 실행해 충돌.
9. **`vi.mocked(...)` 로 타입 안전성 유지** — `as any` 로 모킹한 객체의 타입 우회 금지. Strict TS.
10. **Vitest 브라우저 모드 컴포넌트 테스팅 옵션** — CSS 레이아웃, 브라우저 API 동작, 실제 이벤트 핸들링을 검증해야 할 때 `vitest-browser-react` + Playwright provider 로 실제 브라우저 환경에서 테스트할 수 있다. `page.getByRole()`, `.click()`, `.fill()`, `expect.element()` API 제공. jsdom 의 한계(CSS 미지원, 이벤트 불일치)를 넘어야 하는 경우에만 사용하고, 일반 컴포넌트 테스트는 jsdom 이 기본이다.

11. **부재 단정은 양성 대조 없이 쓰지 않는다** — Testing Library 공식 문서상 `queryBy*` 는 매치가 없으면 `null` 을, `queryAllBy*` 는 빈 배열 `[]` 을 반환하고 **throw 하지 않는다**. 따라서 컴포넌트가 아예 렌더 실패해도 부재 단정은 그대로 통과한다. 부재를 주장하는 테스트에는 "무언가는 렌더됐다" 를 증명하는 단정을 **먼저** 둔다.

    나쁜 예 — 렌더 자체가 실패해도 통과한다:

    ```tsx
    render(<UserList users={[]} />)
    expect(screen.queryByRole('listitem')).toBeNull()
    ```

    좋은 예 — 양성 대조로 렌더 사실을 먼저 고정한다:

    ```tsx
    render(<UserList users={[]} />)
    expect(screen.getByRole('list')).toBeInTheDocument()  // 양성 대조
    expect(screen.queryByRole('listitem')).toBeNull()     // 그 위에서만 부재가 의미를 갖는다
    ```

12. **0 테스트·부분 실행 green run 을 통과 증거로 쓰지 않는다** — Vitest CLI 의 `--passWithNoTests` 는 "Pass when no tests are found" 이고 기본값은 `false` 다. 이 플래그가 npm script 에 박혀 있거나 파일 glob 이 어긋나면 **0 개 실행 = 성공** 출력이 나온다. 또 `allowOnly` 의 기본값은 `!process.env.CI` 이므로 **로컬에서는 남아 있는 `it.only` 하나만 돌고 나머지가 전부 스킵된 채 초록불**이 뜬다. 0 개 테스트는 "위반 없음" 이 아니라 "검사되지 않음" 이다.

    나쁜 예 — 실행 수를 확인하지 않은 통과 보고:

    ```text
    pnpm vitest run → exit 0 → "테스트 통과, 완료"
    ```

    좋은 예 — 실행/스킵 카운트를 함께 인용한다:

    ```text
    pnpm vitest run → "Tests 14 passed | 0 skipped (14)" → 근거로 인용
    Tests 0 passed 이거나 skipped > 0 이면 그 범위는 [미검증]
    ```

13. **스냅샷 baseline 을 사유 없이 갱신하지 않는다** — Playwright `toHaveScreenshot()` 은 baseline 이 없으면 현재 화면을 golden 파일로 기록한다. `--update-snapshots` 로 갱신하면 **깨진 화면이 정답으로 고정**되고 이후 실행은 자기 자신과 비교해 영원히 통과한다. baseline 을 만들거나 갱신했으면 (a) 갱신 사유 한 줄, (b) 그 이미지에서 지목한 구체 요소를 남긴다. 통과시킬 목적으로 `maxDiffPixels` / `maxDiffPixelRatio` 를 키우지 않는다 — 어떤 변경에도 같은 결과를 내는 측정은 oracle 이 아니다.

14. **테스트를 만들 수 없는 항목은 조용히 넘기지 않는다** — 대상이 런타임·브라우저·네이티브 의존이라 이 스킬로 measurement 를 만들 수 없으면, "테스트 생성 완료" 로 보고하지 말고 그 항목에 `[미검증]` 마커와 사유를 붙인다. 상세 규약과 완료 전 체크리스트는 `react-kit/references/render-evidence-protocol.md` §3~§4 를 따르며, 임계값·마커 정의는 그 문서가 인용하는 상위 SSOT 를 따른다 (여기서 재정의하지 않는다).

## Process

### 1. 환경 감지

`references/project-detection.md` 절차를 실행하여 Vitest / Testing Library / Playwright / MSW 설치 여부와 설정 파일 위치를 확인한다.

- `vitest.config.ts` 또는 `vite.config.ts` 안의 `test:` 블록 감지
- `playwright.config.ts` 유무 확인
- `tests/` 디렉토리 구조 확인 — `unit/`, `component/`, `e2e/` 분리 여부

미설치 패키지가 있으면 `/react-init` 을 먼저 실행하도록 안내한다.

### 2. 대상 분석

`$ARGUMENTS` 에서 대상 파일 경로와 테스트 유형을 파싱한다.

유형 미지정 시 파일 경로의 레이어로 자동 판단:

| 파일 경로 패턴 | 자동 선택 |
|--------------|---------|
| `src/domain/` | `unit` (Vitest, node 환경) |
| `src/data/` | `unit` (Vitest + MSW) |
| `src/presentation/hooks/` 또는 `hooks/*.ts` | `component` (Vitest + Testing Library + QueryClient wrapper) |
| `src/presentation/components/` 또는 `*.tsx` | `component` (Vitest + Testing Library + jsdom) |
| `src/presentation/routes/` 또는 화면 단위 | `e2e` (Playwright) |
| `src/infrastructure/` | `unit` (Vitest + mock) |

대상 파일을 읽어 public API (함수 시그니처, 컴포넌트 props) 를 파악한다.

### 3. 기존 테스트 패턴 분석

`tests/` 디렉토리에서 같은 레이어의 기존 테스트 파일을 읽어 프로젝트 관습을 파악한다:

- import 경로 패턴 (`@/` 별칭 vs 상대 경로)
- MSW 서버 설정 파일 위치 (`tests/__mocks__/server.ts` 또는 유사)
- `vi.fn()` / `vi.spyOn()` 사용 패턴
- `describe` / `it` 네이밍 컨벤션

### 4. Clean Architecture 레이어별 테스트 생성

**출력 파일 위치:**

| 테스트 유형 | 출력 경로 |
|-----------|---------|
| unit | `tests/unit/<layer>/<module>.test.ts` |
| component | `tests/component/<ComponentName>.test.tsx` |
| e2e | `tests/e2e/<flow>.spec.ts` |
| MSW 공유 설정 | `tests/__mocks__/server.ts` (없으면 생성) |

#### 4-A. domain 레이어 — Vitest unit (node 환경)

외부 의존성 없음. 순수 함수 입출력 검증.

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

#### 4-B. data 레이어 — Vitest + MSW

MSW 로 fetch 모의, Zod parse 실패 / Result 변환 경로 검증.

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

  it('returns err(validation-failed) when API returns bad shape', async () => {
    server.use(http.get('*/users/123', () => HttpResponse.json({ wrong: 'shape' })))
    const result = await userRepository.fetchUser('123')
    expect(result.isErr()).toBe(true)
    if (result.isErr()) {
      expect(result.error.kind).toBe('user/validation-failed')
    }
  })
})
```

#### 4-C. presentation/components — Testing Library (jsdom)

`getByRole` 우선, `userEvent` 로 실제 이벤트 시뮬레이션, `findBy*` 비동기 대기.

```tsx
// tests/component/LoginForm.test.tsx
import { describe, it, expect, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { ok, err } from 'neverthrow'
import { LoginForm } from '@/presentation/features/auth/components/login-form'

describe('LoginForm', () => {
  it('shows validation error when email is empty', async () => {
    const user = userEvent.setup()
    const onSubmit = vi.fn()
    render(<LoginForm onSubmit={onSubmit} />)

    await user.click(screen.getByRole('button', { name: /로그인/i }))
    expect(await screen.findByText(/올바른 이메일/i)).toBeInTheDocument()
    expect(onSubmit).not.toHaveBeenCalled()
  })

  it('calls onSubmit and shows server error on Result.err', async () => {
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

#### 4-D. presentation/hooks — Testing Library + QueryClient wrapper

TanStack Query 훅은 `QueryClient` 래퍼와 함께 `renderHook` 사용.

```tsx
// tests/component/hooks/useUser.test.tsx
import { describe, it, expect, beforeAll, afterEach, afterAll } from 'vitest'
import { renderHook, waitFor } from '@testing-library/react'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { setupServer } from 'msw/node'
import { http, HttpResponse } from 'msw'
import { useUser } from '@/presentation/features/user/hooks/use-user'

const server = setupServer()
beforeAll(() => server.listen())
afterEach(() => server.resetHandlers())
afterAll(() => server.close())

function makeWrapper() {
  const client = new QueryClient({ defaultOptions: { queries: { retry: false } } })
  return ({ children }: { children: React.ReactNode }) => (
    <QueryClientProvider client={client}>{children}</QueryClientProvider>
  )
}

describe('useUser', () => {
  it('returns user data on success', async () => {
    server.use(
      http.get('*/users/123', () =>
        HttpResponse.json({ id: '123', email_address: 'jane@example.com', display_name: 'Jane', created_at: '2026-04-10T00:00:00Z' }),
      ),
    )
    const { result } = renderHook(() => useUser('123'), { wrapper: makeWrapper() })
    await waitFor(() => expect(result.current.isSuccess).toBe(true))
    expect(result.current.data?.email).toBe('jane@example.com')
  })
})
```

#### 4-E. Error Boundary 테스트

의도적으로 throw 하는 자식 컴포넌트로 Error Boundary 를 트리거.

```tsx
// tests/component/RootErrorBoundary.test.tsx
import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import { RootErrorBoundary } from '@/presentation/shared/components/root-error-boundary'

describe('RootErrorBoundary', () => {
  it('catches render-time error and shows fallback', () => {
    const Boom = () => { throw new Error('render boom') }
    // React 18 에서 콘솔 에러 억제
    const consoleSpy = vi.spyOn(console, 'error').mockImplementation(() => {})
    render(
      <RootErrorBoundary>
        <Boom />
      </RootErrorBoundary>,
    )
    expect(screen.getByText(/예기치 못한 오류/i)).toBeInTheDocument()
    consoleSpy.mockRestore()
  })
})
```

#### 4-F. Playwright E2E

화면 전체 플로우를 실제 브라우저에서 검증.

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

test('shows error message on invalid credentials', async ({ page }) => {
  await page.goto('/login')
  await page.getByLabel('이메일').fill('wrong@example.com')
  await page.getByLabel('비밀번호').fill('wrongpassword')
  await page.getByRole('button', { name: '로그인' }).click()
  await expect(page.getByText(/이메일 또는 비밀번호가 올바르지 않습니다/i)).toBeVisible()
})
```

### 5. infrastructure 레이어 — WASM / Tauri mock

```ts
// tests/unit/infrastructure/wasm/image-processor.test.ts
import { describe, it, expect, vi } from 'vitest'

vi.mock('@/infrastructure/wasm/image-processor', () => ({
  processImage: vi.fn().mockResolvedValue(new Uint8Array([1, 2, 3])),
}))

// Tauri invoke 모의
vi.mock('@tauri-apps/api/core', () => ({
  invoke: vi.fn(),
}))
```

### 6. 생성 후 보고

생성된 테스트 파일 경로, 테스트 케이스 목록, 실행 명령을 안내한다:

```bash
# Vitest unit + component
pnpm test

# Vitest coverage
pnpm test --coverage

# Playwright e2e
pnpm exec playwright test
```

## References

- `references/project-detection.md` — 환경 감지
- `references/clean-arch-layout.md` — 레이어별 경로 규칙
- `references/result-patterns.md` — Result/Failure 패턴 (에러 경로 검증)
- 소스 문서: `docs/react/kit-design/g4-quality.md` §1
