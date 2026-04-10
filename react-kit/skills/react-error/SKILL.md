---
name: react-error
description: >
  데이터 경계의 예외를 Failure로 변환하고, React Error Boundary로 렌더 에러를 포획하며, Severity에 따라 UI 표시를 분기하는 3단계 에러 처리 패턴을 세팅한다.
  "에러 처리", "error handling", "Failure 패턴", "에러 다이얼로그", "ErrorBoundary", "Severity 매핑", "에러 표시" 같은 요청 시 트리거.
  Result/Failure 타입 정의가 필요할 때도 트리거한다.
argument-hint: "[global|feature <FeatureName>]"
user-invocable: true
---

## Gotchas

1. **비동기 에러는 Error Boundary 가 못 잡음** — `useEffect` 안의 throw, Promise reject 는 Error Boundary 에 도달하지 않는다. 반드시 Result 로 감쌀 것. Error Boundary 는 **렌더 중 throw** 만 포획한다.
2. **Error Boundary 는 클래스 컴포넌트 필수** — React 19 에서도 hooks 로 구현 불가. `react-error-boundary` 라이브러리 사용도 가능하지만 기본은 자체 클래스 컴포넌트.
3. **Failure 를 Error 로 감싸지 말 것** — `new Error(JSON.stringify(failure))` 같은 변환은 TypeScript 타입 정보를 잃고 stack trace 를 의미 없게 만든다. Failure 는 그 자체가 타입 안전 값.
4. **fatal 분기는 Zustand store 경유** — `fatal` severity 에서 직접 `window.location.reload()` 하지 말고 Zustand store 의 `fatalError` 필드를 설정해 최상위 컴포넌트가 렌더 분기하게 한다.
5. **Vite dev 모드에서 Error Boundary 동작 주의** — React 는 dev 에서 에러를 re-throw 해 개발자가 볼 수 있게 한다. Error Boundary 가 동작 안 하는 것처럼 보이면 프로덕션 빌드로 확인.
6. **Toast 라이브러리 하나만** — shadcn/ui 는 `sonner` 를 권장. Radix 기반 `<Toaster />` 와 `sonner` 를 동시에 쓰면 중복 렌더. 하나를 선택하고 통일한다.
7. **exhaustiveness 검증 필수** — Failure discriminated union 의 switch 에서 모든 kind 를 다뤘는지 `never` 타입으로 검증하라. 새 Failure kind 추가 시 컴파일 에러로 누락을 잡는다.
8. **domain 레이어에 i18n import 금지** — `severityOf()` 와 Failure 타입은 `src/domain/failures/` 에 위치한다. 사용자용 메시지 매핑은 presentation 레이어의 `display-failure.ts` 에서 처리한다.

## Process

### 1. 환경 감지

`references/project-detection.md` 절차를 실행하여 `neverthrow` 설치 여부를 확인한다. 미설치 시 `/react-init` 을 먼저 실행하도록 안내한다.

기존 에러 인프라 탐색:

| 탐색 대상 | 경로 |
|----------|------|
| Failure 타입 | `src/domain/failures/` |
| Severity 매핑 함수 | 같은 파일의 `severityOf()` |
| UI 표시 유틸 | `src/presentation/shared/lib/display-failure.ts` |
| Error Boundary | `src/presentation/shared/components/root-error-boundary.tsx` |
| Fatal store | `src/presentation/shared/stores/app-store.ts` |

이미 존재하면 패턴을 읽고 확장한다. 없으면 새로 생성한다.

### 2. scope 결정

- **`global`** (기본): 앱 전체 Error Boundary + toast/snackbar 시스템 + fatal store 세팅
- **`feature <FeatureName>`**: 특정 feature 의 Failure 타입 + `severityOf()` + UI 매핑 추가

### 3. 에러 처리 3단계 흐름

```text
[Step 1: 데이터 경계]             [Step 2: 전파 + Severity]        [Step 3: UI 표시]
throw / reject          ──────►   Result<T, Failure>    ──────►   Severity → UI 선택
(fetch, WASM, Tauri)              (neverthrow chain)               (toast / dialog / page)
                                         │
                                         ▼
                                  [렌더 중 예외적 탈출]
                                   React Error Boundary
                                         │
                                         ▼
                                      Fallback UI
```

### 4. Step 1 — 데이터 경계에서 throw → Failure 변환

`src/data/datasources/remote/<feature>-api.ts` 에서 `ResultAsync.fromPromise` 로 경계 변환.

```ts
// src/data/datasources/remote/user-api.ts
import { ResultAsync } from 'neverthrow'
import type { UserFailure } from '@/domain/failures/user-failures'

const BASE = import.meta.env.VITE_API_BASE_URL

export function fetchUserDto(id: string): ResultAsync<unknown, UserFailure> {
  return ResultAsync.fromPromise(
    fetch(`${BASE}/users/${id}`).then(async (r) => {
      if (r.status === 404) throw { kind: 'user/not-found', userId: id } satisfies UserFailure
      if (r.status === 401) throw { kind: 'user/unauthorized' } satisfies UserFailure
      if (!r.ok) throw { kind: 'user/network-error', cause: r.statusText } satisfies UserFailure
      return r.json()
    }),
    (e) => (isUserFailure(e)
      ? e
      : { kind: 'user/network-error', cause: String(e) }),
  )
}

function isUserFailure(e: unknown): e is UserFailure {
  return typeof e === 'object' && e !== null && 'kind' in e && typeof (e as UserFailure).kind === 'string'
}
```

**규칙:**
- throw 는 datasource 내부에서만. 즉시 두 번째 인자에서 Failure 로 변환
- Failure 는 discriminated union (`kind` 필드 필수)
- `cause` 필드에 원본 에러 메시지 보존 (디버깅용)

### 5. Step 2 — Failure 타입 정의 + Severity 매핑

`src/domain/failures/<feature>-failures.ts` 에 생성.

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
      return 'info'       // 사용자 인지로 충분
    case 'user/rate-limited':
      return 'warning'    // 일시적, 재시도 안내
    case 'user/unauthorized':
    case 'user/validation-failed':
      return 'error'      // 사용자 액션 필요
    case 'user/network-error':
      return 'fatal'      // 네트워크 자체 문제
    default: {
      // exhaustiveness 검증 — 새 kind 추가 시 컴파일 에러
      const _: never = failure
      return _
    }
  }
}
```

**Severity 정의 — 사용자 관점의 심각도:**

| Severity | 의미 | 예시 |
|----------|------|------|
| `info` | 인지만 해도 충분, 자동 dismiss | 리소스 not-found |
| `warning` | 일시적 문제, 재시도 가능 | rate-limit, 일시 장애 |
| `error` | 사용자 액션 필요 | 인증 오류, 유효성 실패 |
| `fatal` | 앱 흐름 중단, 즉각 대응 필요 | 네트워크 완전 단절, 서버 500 |

### 6. Step 3 — UI 표시 매핑

**Severity → UI 매핑 테이블:**

| Severity | 표시 형태 | 위치 | 상호작용 |
|----------|----------|------|---------|
| `info` | Toast (자동 dismiss) | 화면 우하단 | 없음 |
| `warning` | Snackbar (action 포함) | 화면 하단 | "다시 시도" 버튼 |
| `error` | Inline error 또는 Dialog | 관련 위치 | 사용자 액션 유도 |
| `fatal` | Full page error 또는 Modal | 전체 | 새로고침 / 로그아웃 안내 |

`src/presentation/shared/lib/display-failure.ts` 에 생성:

```ts
// src/presentation/shared/lib/display-failure.ts
import { toast } from 'sonner'
import { useAppStore } from '../stores/app-store'
import type { Severity } from '@/domain/failures/user-failures'

type FailureLike = { kind: string; cause?: string }

export function displayFailure(failure: FailureLike, severity: Severity): void {
  switch (severity) {
    case 'info':
      toast.info(toUserMessage(failure))
      break
    case 'warning':
      toast.warning(toUserMessage(failure), {
        action: { label: '다시 시도', onClick: () => window.location.reload() },
      })
      break
    case 'error':
      toast.error(toUserMessage(failure))
      break
    case 'fatal':
      // Zustand store 에 fatal 플래그 설정 → 최상단 FullPageError 렌더
      useAppStore.getState().setFatalError(failure)
      break
  }
}

function toUserMessage(failure: FailureLike): string {
  // Failure kind → 사용자용 번역 키. Lingui 로 i18n 화 (/react-l10n 참조)
  const messages: Record<string, string> = {
    'user/not-found': '요청한 사용자를 찾을 수 없습니다.',
    'user/unauthorized': '로그인이 필요합니다.',
    'user/network-error': '네트워크 연결을 확인해주세요.',
    'user/validation-failed': '입력값을 다시 확인해주세요.',
    'user/rate-limited': '잠시 후 다시 시도해주세요.',
  }
  return messages[failure.kind] ?? '알 수 없는 오류가 발생했습니다.'
}
```

### 7. React Error Boundary 생성

`src/presentation/shared/components/root-error-boundary.tsx` 에 생성:

```tsx
// src/presentation/shared/components/root-error-boundary.tsx
import * as React from 'react'

type Props = { children: React.ReactNode; fallback?: React.ReactNode }
type State = { hasError: boolean; error: Error | null }

export class RootErrorBoundary extends React.Component<Props, State> {
  state: State = { hasError: false, error: null }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error }
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo): void {
    console.error('[RootErrorBoundary]', error, errorInfo)
    // 프로덕션: Sentry.captureException(error, { extra: errorInfo }) 등
  }

  render(): React.ReactNode {
    if (this.state.hasError) {
      if (this.props.fallback) return this.props.fallback
      return (
        <div role="alert" className="flex min-h-screen items-center justify-center">
          <div className="space-y-4 text-center">
            <h1 className="text-2xl font-semibold">예기치 못한 오류</h1>
            <p className="text-muted-foreground">{this.state.error?.message}</p>
            <button
              type="button"
              className="rounded bg-primary px-4 py-2 text-primary-foreground"
              onClick={() => window.location.reload()}
            >
              새로고침
            </button>
          </div>
        </div>
      )
    }
    return this.props.children
  }
}
```

**Error Boundary 배치 규칙:**
- `<RootErrorBoundary>` 는 `src/presentation/app.tsx` 또는 라우터 루트에서 **한 번만** 감싼다
- feature 단위 Error Boundary 가 필요하면 `fallback` prop 을 활용한다
- Error Boundary 를 자주 열린다면 Result 패턴에 구멍이 있다는 신호

### 8. Fatal error Zustand store

`src/presentation/shared/stores/app-store.ts` 에 `fatalError` 필드 추가:

```ts
// src/presentation/shared/stores/app-store.ts
import { create } from 'zustand'

type FailureLike = { kind: string; cause?: string }

interface AppState {
  fatalError: FailureLike | null
  setFatalError: (failure: FailureLike) => void
  clearFatalError: () => void
}

export const useAppStore = create<AppState>((set) => ({
  fatalError: null,
  setFatalError: (failure) => set({ fatalError: failure }),
  clearFatalError: () => set({ fatalError: null }),
}))
```

`src/presentation/app.tsx` 에서 fatalError 렌더 분기:

```tsx
// src/presentation/app.tsx (발췌)
import { useAppStore } from './shared/stores/app-store'
import { RootErrorBoundary } from './shared/components/root-error-boundary'

export function App() {
  const fatalError = useAppStore((s) => s.fatalError)

  if (fatalError) {
    return (
      <div role="alert" className="flex min-h-screen items-center justify-center">
        <p>심각한 오류: {fatalError.kind}</p>
        <button type="button" onClick={() => window.location.reload()}>새로고침</button>
      </div>
    )
  }

  return (
    <RootErrorBoundary>
      {/* 라우터 또는 앱 트리 */}
    </RootErrorBoundary>
  )
}
```

### 9. presentation 에서 Failure 표시

컴포넌트 또는 훅에서 Result 를 받아 `displayFailure` 호출:

```tsx
// presentation/features/user/components/user-profile.tsx (발췌)
import { displayFailure } from '@/presentation/shared/lib/display-failure'
import { severityOf } from '@/domain/failures/user-failures'

async function handleSave() {
  const result = await updateUserUseCase({ id, name })
  if (result.isErr()) {
    displayFailure(result.error, severityOf(result.error))
    return
  }
  // 성공 처리
}
```

### 10. 파일 생성 요약

| 파일 | 내용 |
|------|------|
| `src/domain/failures/<feature>-failures.ts` | Failure discriminated union + `severityOf()` |
| `src/presentation/shared/lib/display-failure.ts` | Severity → UI 표시 라우터 |
| `src/presentation/shared/components/root-error-boundary.tsx` | React Error Boundary 클래스 컴포넌트 |
| `src/presentation/shared/stores/app-store.ts` | fatalError Zustand store |

## References

- `references/result-patterns.md` — neverthrow Result/Failure 패턴 (핵심)
- `references/clean-arch-layout.md` — 레이어별 경로 규칙
- `references/project-detection.md` — 환경 감지
- 소스 문서: `docs/react/kit-design/g4-quality.md` §2
