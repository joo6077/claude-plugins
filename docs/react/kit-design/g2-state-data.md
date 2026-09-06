# G2 — State & Data Skills

```yaml
last_updated: 2026-04-10
group: G2
scope: react-kit 상태 관리 + 데이터 계층 스킬 4종
skills: [/react-store, /react-api, /react-query, /react-form]
depends_on: [G1 /react-init, G1 /react-feature]
research_sources:
  - Zustand 공식 문서 (zustand.docs.pmnd.rs, pmndrs/zustand README)
  - TanStack Query v5 공식 문서 (tanstack.com/query/v5/docs)
  - React Hook Form 공식 문서 (react-hook-form.com)
  - "@hookform/resolvers (react-hook-form/resolvers GitHub)"
  - neverthrow 공식 문서 (supermacro/neverthrow)
  - 2026-04 WebSearch 검증
```

## 문서 목적

react-kit **G2 그룹** 은 프로젝트의 상태 계층을 담당하는 4개 스킬의 설계 스펙이다. **Zustand (클라이언트 상태)**, **TanStack Query (서버 상태)**, **Clean Architecture 기반 데이터 레이어**, **React Hook Form + Zod (폼)** 가 유기적으로 맞물려 있다. 이 문서는 네 스킬이 서로 어떻게 협력하며 어디까지 생성을 자동화하는지 규정한다.

**스킬**: `/react-store`, `/react-api`, `/react-query`, `/react-form`  
**전제**: G1 `/react-init` 으로 초기화된 프로젝트 (Zustand, TanStack Query, RHF, Zod, neverthrow 모두 설치됨)

## 공통 설계 원칙 (4개 스킬 공통)

- **Result 타입 기반 에러 경로**: 모든 경계 (datasource, repository, usecase, form submit) 에서 `throw` 대신 `neverthrow` 의 `Result<T, Failure>` 를 반환한다. React 경계에 도달한 에러만 UI 가 `isErr()` 체크로 분기 처리.
- **Zod 경계 검증 필수**: 외부 데이터 (API 응답, 폼 입력, localStorage 읽기, WASM 결과) 는 **첫 진입 시점에** `Schema.parse()` 로 검증한 뒤 도메인 타입으로 변환. 내부 레이어에선 재검증 없이 타입을 신뢰.
- **Strict TypeScript 정책**: G1 에서 정의한 strict 규칙 (no `any`, no `!`, no `as`) 을 모든 생성 코드가 준수. `z.infer` 로 파생된 타입만 사용, 수동 중복 정의 금지.
- **project-detection 공유**: G1 의 `react-kit/references/project-detection.md` 를 재사용. 설치된 패키지 버전을 감지해 v5+ / v4+ 등 메이저 범위에 맞게 코드 생성.
- **G1 `/react-feature` 협력**: G2 스킬은 `/react-feature` 가 이미 생성한 skeleton (features/<name>/) 위에서 동작. feature 가 없으면 먼저 `/react-feature` 실행을 안내.

## 의존성 설치 (G1 `/react-init` 미사용 시 수동 설치)

G1 `/react-init` 스캐폴딩이 모든 의존성을 자동 설치하지만, 기존 프로젝트에 수동 추가하려면 아래 명령을 사용한다. 모든 명령은 2026-04 기준 공식 문서 준수:

```sh
# 상태 관리 + 서버 상태
pnpm add zustand @tanstack/react-query

# 폼 + 런타임 검증
pnpm add react-hook-form @hookform/resolvers zod

# 타입 안전 에러 처리
pnpm add neverthrow
```

**메이저 버전 범위**: Zustand v5+, TanStack Query v5+, React Hook Form v7+, Zod v3+ (또는 v4, 단 RHF resolver 의 v4 TypeScript 이슈 주의 — 섹션 4.6 Gotchas 참조), neverthrow v7+. 특정 패치 버전 고정 없이 최신 메이저 태그 설치.

**출처**:
- Zustand: https://github.com/pmndrs/zustand
- TanStack Query v5: https://tanstack.com/query/v5/docs/framework/react/installation
- React Hook Form + resolvers: https://react-hook-form.com/get-started , https://github.com/react-hook-form/resolvers
- neverthrow: https://github.com/supermacro/neverthrow

## 상태 분리 원칙 — Zustand vs TanStack Query

이 원칙은 G2 전체의 **핵심 아키텍처 결정**이다. 두 상태의 경계가 흐릿하면 버그와 중복이 폭증한다.

### 역할 분리

| 축 | Zustand | TanStack Query |
|----|---------|----------------|
| **도메인** | 클라이언트 상태 (UI, 로컬 선호도, feature toggle, 편집 중 임시 데이터) | 서버 상태 (REST/GraphQL 응답, 캐시, 동기화) |
| **수명** | 세션 또는 persist 설정에 따름 | staleTime/gcTime 에 따라 자동 만료 |
| **변경** | `setState` 로 직접 | mutation → invalidation → 자동 refetch |
| **직렬화** | `persist` 미들웨어로 localStorage 연동 가능 | `persistQueryClient` 로 offline 캐시 |
| **React 외부 접근** | 가능 (`useStore.getState()`, `useStore.setState()`) | QueryClient 직접 조작 가능하지만 권장 안 됨 |

### 교차 지점 패턴

**Mutation 성공 후 로컬 상태 갱신**이 가장 흔한 교차 지점이다. 패턴은 하나:

```
useMutation({
  mutationFn: ...,
  onSuccess: (data) => {
    // 1. 서버 쿼리 무효화 (TanStack Query 쪽)
    queryClient.invalidateQueries({ queryKey: ['user', userId] })
    // 2. 필요하면 Zustand 쪽도 갱신
    useUserStore.setState({ lastMutatedAt: Date.now() })
  },
})
```

**절대 하지 말 것**:
- 서버 응답을 **Zustand 에 복사 저장** → 두 소스가 동기화 안 돼 버그 유발. 서버 상태는 TanStack Query 가 단일 진실 공급원
- Zustand store 안에 `async fetchUser()` 함수 → TanStack Query 의 역할. store 는 순수 상태만
- TanStack Query 로 UI 토글 관리 → Zustand 의 역할

## 1. /react-store — Zustand 스토어 생성

feature 별 또는 전역 Zustand 스토어를 생성하고 selector hook 까지 자동 생성한다.

### 1.1 트리거

- 키워드: "스토어 만들어줘", "react-store", "zustand store", "state management"
- 조건: G1 초기화 완료 (`zustand` dependency 존재)

### 1.2 입력

- `store_name` (필수): kebab-case (예: `auth-store`, `cart-store`)
- `scope`: `feature` (기본) 또는 `shared`. feature 면 `presentation/features/<feature>/store.ts`, shared 면 `presentation/shared/stores/<name>.ts`
- `--with-persist` (기본 false): persist 미들웨어 포함
- `state_shape` (선택): 초기 상태 shape (예: `{ user: User | null; isLoading: boolean }`)

### 1.3 생성 파일 구조

```ts
// src/presentation/features/auth/store.ts
import { create } from 'zustand'
import { persist } from 'zustand/middleware'  // --with-persist 옵션 시만
import type { User } from '@/domain/entities/user'

type AuthState = {
  user: User | null
  accessToken: string | null
  isAuthenticated: boolean
}

type AuthActions = {
  setUser: (user: User | null) => void
  setToken: (token: string | null) => void
  clear: () => void
}

type AuthStore = AuthState & AuthActions

const initialState: AuthState = {
  user: null,
  accessToken: null,
  isAuthenticated: false,
}

export const useAuthStore = create<AuthStore>()((set) => ({
  ...initialState,
  setUser: (user) => set({ user, isAuthenticated: user !== null }),
  setToken: (accessToken) => set({ accessToken }),
  clear: () => set(initialState),
}))

// Selector hooks (렌더 최적화 + 타입 안전)
export const useAuthUser = () => useAuthStore((s) => s.user)
export const useIsAuthenticated = () => useAuthStore((s) => s.isAuthenticated)
```

### 1.4 Zustand TypeScript 패턴 (v5+)

- `create<State>()(...)` — 제네릭 파라미터를 먼저 적용한 뒤 **괄호를 한 번 더** 열어 store creator 를 전달. 이게 v4+ 이후 권장 형태
- **State 와 Actions 분리**: 타입 두 개로 분할하면 state shape 만 별도 타입 추출 (예: `initialState: AuthState`) 이 쉬워짐
- **Selector hooks 자동 생성**: `useAuthStore((s) => s.user)` 같은 selector 를 래핑한 커스텀 훅을 기본 제공. 직접 `useAuthStore()` 호출 금지 — 전체 스토어 구독으로 불필요한 리렌더 발생

### 1.5 React 외부 접근 (WASM 콜백용)

이게 Jotai 대신 Zustand 를 선택한 핵심 이유. WASM 비동기 콜백이나 Worker 메시지가 React 트리 바깥에서 상태를 갱신해야 할 때:

```ts
// src/data/datasources/wasm/image-worker-setup.ts
import { useUploadStore } from '@/presentation/features/upload/store'

// Worker 메시지 리스너. React 컴포넌트 트리 밖에서 직접 setState 호출
wasmWorker.addEventListener('message', (event) => {
  if (event.data.type === 'progress') {
    useUploadStore.setState({ progress: event.data.value })
  }
})

// 현재 상태 읽기 (구독 없이 스냅샷)
const currentProgress = useUploadStore.getState().progress
```

`useUploadStore.getState()` 와 `useUploadStore.setState()` 는 React 훅 규칙 밖에서 자유롭게 호출 가능. 이 점은 Zustand 의 구조적 이점이며 `/react-wasm` 스킬이 생성하는 Worker 래퍼와 자연스럽게 연동된다.

### 1.6 Gotchas

- **`create()` vs `createStore()` 혼동**: 글로벌 훅 기반 사용은 `create`. React Context 로 여러 인스턴스 제공하거나 SSR 시에는 `createStore`. react-kit 기본은 `create` (대부분 client-only + Tauri).
- **selector 없이 전체 구독 금지**: `const store = useAuthStore()` 처럼 인자 없이 호출하면 state 모든 키에 구독되어 리렌더 폭탄. 반드시 selector 경유.
- **Actions 안에서 `get()` 사용 주의**: 이전 상태 읽어서 다음 상태 계산할 땐 `set((state) => ({ ... }))` 형태가 안전. `get()` 은 race condition 위험.
- **immer 는 선택**: 단순 상태면 안 쓰는 게 번들 이득. 중첩 깊이가 2+ 이면 `zustand/middleware/immer` 추가 고려.
- **Strict TS**: `create<Store>()` 제네릭을 생략하면 타입이 `unknown` 으로 추론. 항상 명시.
- **persist 직렬화 실패**: `Map`, `Set`, Date 객체는 기본 JSON 직렬화 안 됨. persist 사용 시 `storage: createJSONStorage(...)` 로 커스터마이즈하거나 primitive 만 저장.

### 1.7 Clean Architecture 배치

- **feature store**: `src/presentation/features/<feature>/store.ts`
- **shared store**: `src/presentation/shared/stores/<name>.ts`
- **절대 금지**: `domain/` 이나 `data/` 에 Zustand import. 도메인/데이터 레이어는 상태 관리 라이브러리를 몰라야 함

## 2. /react-api — Clean Architecture 4계층 생성

REST/GraphQL 엔드포인트를 **datasource → model → repository → usecase** 4 단계로 일괄 또는 개별 생성한다. flutter-toolkit 의 `/flutter-api` 와 동일 철학.

### 2.1 트리거

- 키워드: "API 연동", "엔드포인트 추가", "react-api", "API 만들어줘"
- 서브커맨드: `--only model`, `--only repository`, `--only usecase` 로 개별 레이어만

### 2.2 입력

- `resource_name` (필수): PascalCase 단수 (예: `User`, `Product`, `Order`)
- `operations` (선택): `list`, `get`, `create`, `update`, `delete` 중 택 (복수 허용, 기본 `list + get`)
- `--base-url` (선택): API base URL (프로젝트 `.env` 의 `VITE_API_URL` 감지해 자동 채움)
- `--schema` (선택): Zod 스키마 파일 경로 (없으면 인터랙티브로 shape 물어봄)

### 2.3 4계층 생성 순서

G1 `/react-feature` 의 의존성 그래프와 동일. 안쪽 (도메인) 부터 바깥쪽 (presentation) 으로:

```
1. domain/entities/<resource>.ts        (Zod 스키마 + z.infer 타입)
2. domain/failures/<resource>-failures.ts  (Failure discriminated union)
3. domain/usecases/<resource>-usecases.ts  (함수 시그니처, 인터페이스)
4. data/models/<resource>-dto.ts          (API DTO 스키마 + 변환)
5. data/datasources/remote/<resource>-api.ts  (fetch + Zod parse)
6. data/repositories/<resource>-repository.ts  (UseCase 구현)
7. (선택) presentation/features/<feature>/hooks/use-<resource>.ts  (TanStack Query 훅)
```

### 2.4 각 레이어의 역할

**domain/entities** — 순수 도메인 모델. Zod 스키마 + `z.infer` 로 타입 파생. 외부 의존성 0개. 예:

```ts
// src/domain/entities/user.ts
import { z } from 'zod'

export const UserSchema = z.object({
  id: z.string().uuid(),
  email: z.string().email(),
  name: z.string().min(1),
  createdAt: z.coerce.date(),
})

export type User = z.infer<typeof UserSchema>
```

**domain/failures** — Result 의 에러 채널을 타입 안전하게. discriminated union:

```ts
// src/domain/failures/user-failures.ts
export type UserFailure =
  | { kind: 'user/not-found'; userId: string }
  | { kind: 'user/network-error'; cause: string }
  | { kind: 'user/validation-failed'; issues: string[] }
  | { kind: 'user/unauthorized' }
```

**domain/usecases** — 함수 시그니처만. 구현은 data 레이어가 담당. neverthrow Result 반환:

```ts
// src/domain/usecases/user-usecases.ts
import type { Result } from 'neverthrow'
import type { User } from '@/domain/entities/user'
import type { UserFailure } from '@/domain/failures/user-failures'

export type UserUseCases = {
  fetchUser: (id: string) => Promise<Result<User, UserFailure>>
  listUsers: () => Promise<Result<User[], UserFailure>>
  updateUser: (user: User) => Promise<Result<User, UserFailure>>
}
```

**data/models** — API 의 raw DTO 스키마 + 도메인 변환. API 스키마가 도메인과 달라지면 여기서 흡수:

```ts
// src/data/models/user-dto.ts
import { z } from 'zod'
import { UserSchema, type User } from '@/domain/entities/user'

export const UserDtoSchema = z.object({
  id: z.string(),
  email_address: z.string(),  // API 는 snake_case
  display_name: z.string(),
  created_at: z.string(),
})

export type UserDto = z.infer<typeof UserDtoSchema>

export function toUserDomain(dto: UserDto): User {
  return UserSchema.parse({
    id: dto.id,
    email: dto.email_address,
    name: dto.display_name,
    createdAt: dto.created_at,
  })
}
```

**data/datasources/remote** — fetch 실행 + Zod parse + Result 변환. 첫 경계 검증:

```ts
// src/data/datasources/remote/user-api.ts
import { ok, err, ResultAsync } from 'neverthrow'
import { UserDtoSchema } from '@/data/models/user-dto'
import type { UserFailure } from '@/domain/failures/user-failures'

const BASE = import.meta.env.VITE_API_URL

export function fetchUserDto(id: string): ResultAsync<unknown, UserFailure> {
  return ResultAsync.fromPromise(
    fetch(`${BASE}/users/${id}`).then(async (r) => {
      if (r.status === 404) throw { kind: 'user/not-found', userId: id }
      if (r.status === 401) throw { kind: 'user/unauthorized' }
      if (!r.ok) throw { kind: 'user/network-error', cause: r.statusText }
      return r.json()
    }),
    (e) => (typeof e === 'object' && e !== null && 'kind' in e
      ? (e as UserFailure)
      : { kind: 'user/network-error', cause: String(e) }),
  )
}
```

**data/repositories** — UseCase 를 구현. datasource 호출 → DTO parse → 도메인 변환 → Result 반환:

```ts
// src/data/repositories/user-repository.ts
import { fetchUserDto } from '@/data/datasources/remote/user-api'
import { UserDtoSchema, toUserDomain } from '@/data/models/user-dto'
import type { UserUseCases } from '@/domain/usecases/user-usecases'

export const userRepository: UserUseCases = {
  fetchUser: async (id) => {
    const result = await fetchUserDto(id)
    return result.andThen((raw) => {
      const parsed = UserDtoSchema.safeParse(raw)
      if (!parsed.success) {
        return err({
          kind: 'user/validation-failed' as const,
          issues: parsed.error.issues.map((i) => i.message),
        })
      }
      return ok(toUserDomain(parsed.data))
    })
  },
  listUsers: async () => { /* ... */ },
  updateUser: async (user) => { /* ... */ },
}
```

### 2.5 Zod parse 실패 처리 흐름

- **첫 검증 시점**: `data/datasources/remote/` 가 fetch 응답의 raw JSON 을 받는 순간
- **실패 시 변환**: `z.safeParse()` 가 `success: false` 면 `UserFailure` 의 `kind: 'user/validation-failed'` 로 감싸서 Result 로 반환
- **이후 레이어는 재검증 안 함**: repository, usecase, hook, component 모두 이미 검증된 도메인 타입을 신뢰
- **절대 금지**: `as` 단언으로 Zod 우회, 여러 레이어에서 중복 parse, try/catch 로 Zod 에러 감추기

### 2.6 Gotchas

- **`z.infer` 단일 소스**: 수동 interface 재정의 금지. 스키마와 타입이 어긋나면 strict TS 위반.
- **`fetch` 직접 사용은 datasource 안에서만**: infrastructure/http/client.ts 에 공용 wrapper 를 두고 통일하는 것도 허용. repository 에서 직접 fetch 금지.
- **DTO 와 Domain 분리**: API 스키마가 도메인과 같아 보여도 반드시 DTO 를 따로 정의. 나중에 API 가 바뀌면 domain 재작성 없이 DTO 만 수정.
- **HTTP 상태 코드 → Failure kind 매핑**: 404 → not-found, 401 → unauthorized, 기타 → network-error. 스킬 템플릿에 매핑 표 내장.
- **Strict TS**: `ResultAsync.fromPromise` 의 두 번째 인자 (에러 변환) 에서 `as` 사용 금지, 타입 가드로 처리.

### 2.7 Clean Architecture 배치

- domain: `src/domain/entities/`, `src/domain/failures/`, `src/domain/usecases/`
- data: `src/data/models/`, `src/data/datasources/remote/`, `src/data/repositories/`
- presentation hook: `src/presentation/features/<feature>/hooks/` (선택, `/react-query` 가 담당)

## 3. /react-query — TanStack Query v5 훅 생성

`/react-api` 가 생성한 repository 를 감싸는 TanStack Query v5 훅을 생성한다.

### 3.1 트리거

- 키워드: "TanStack Query 훅", "useQuery 만들어줘", "react-query", "서버 상태 훅"
- 조건: `/react-api` 가 생성한 repository 가 존재 (없으면 먼저 `/react-api` 실행 안내)

### 3.2 입력

- `resource_name` (필수): PascalCase
- `operations`: `list`, `get`, `create`, `update`, `delete` — repository 의 것과 매칭
- `feature` (선택): feature 디렉토리 이름. 없으면 `presentation/shared/hooks/` 에 생성

### 3.3 queryKey 네이밍 규칙

queryKey 는 TanStack Query 의 캐시 기본 단위다. 일관된 규칙이 없으면 invalidation 이 꼬인다.

**3-레벨 배열 규칙**: `[domain, subject, params]`

```ts
// 단건
['user', 'detail', { id: userId }]
// 목록
['user', 'list', { page, pageSize }]
// 관계
['user', 'posts', { userId }]
```

- **0번째 (domain)**: 리소스 이름 단수형. 'user', 'product', 'order'
- **1번째 (subject)**: 쿼리의 서브젝트. 'detail', 'list', 'stats', 'children'
- **2번째 (params)**: 파라미터 객체. 없으면 생략 가능

**invalidation 경로**:
- `queryClient.invalidateQueries({ queryKey: ['user'] })` → 모든 user 관련 쿼리
- `queryClient.invalidateQueries({ queryKey: ['user', 'detail', { id }] })` → 특정 detail 만

### 3.4 useQuery 패턴

```ts
// src/presentation/features/user/hooks/use-user.ts
import { useQuery } from '@tanstack/react-query'
import { userRepository } from '@/data/repositories/user-repository'
import type { User } from '@/domain/entities/user'
import type { UserFailure } from '@/domain/failures/user-failures'

export function useUser(userId: string) {
  return useQuery<User, UserFailure>({
    queryKey: ['user', 'detail', { id: userId }],
    queryFn: async () => {
      const result = await userRepository.fetchUser(userId)
      if (result.isErr()) throw result.error  // TanStack Query 가 error 로 잡음
      return result.value
    },
    staleTime: 1000 * 60,  // 1분
    enabled: userId !== '',
  })
}
```

**중요**: queryFn 은 Promise 를 반환해야 하므로 Result 를 여기서만 throw 로 언래핑. TanStack Query 의 `error` 가 `UserFailure` 타입이 됨.

### 3.5 useMutation + invalidation 패턴

```ts
// src/presentation/features/user/hooks/use-update-user.ts
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { userRepository } from '@/data/repositories/user-repository'
import type { User } from '@/domain/entities/user'

export function useUpdateUser() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: async (user: User) => {
      const result = await userRepository.updateUser(user)
      if (result.isErr()) throw result.error
      return result.value
    },
    onSuccess: (updated) => {
      // 세밀한 무효화 — detail 캐시 직접 교체 + list 재조회
      queryClient.setQueryData(['user', 'detail', { id: updated.id }], updated)
      queryClient.invalidateQueries({ queryKey: ['user', 'list'] })
    },
  })
}
```

### 3.6 Cache invalidation 전략

**세 가지 레벨**:

1. **setQueryData** — 서버 응답 그대로 캐시에 주입. 추가 네트워크 호출 없음. 리소스가 작을 때 사용
2. **invalidateQueries** — 캐시를 stale 마킹 + 활성 쿼리 자동 refetch. 기본 전략
3. **removeQueries** — 캐시에서 완전 제거. 로그아웃 같은 상황에 전역 리셋용

**권장 조합**:
- 업데이트: `setQueryData(detail) + invalidateQueries(list)` — detail 즉시 반영 + list 는 서버 기준으로 다시
- 생성: `invalidateQueries(list)` — 새 데이터는 서버에서
- 삭제: `removeQueries(detail) + invalidateQueries(list)` — detail 제거 + list 재조회
- 로그아웃: `queryClient.clear()` — 전체 초기화

### 3.7 Gotchas

- **queryFn 안에서 Result throw**: TanStack Query 는 throw 를 기대. Result 를 반환하면 TS 타입이 `Result<T, E>` 가 되어 `data` 가 Result 로 꼬임. throw 로 풀어주는 게 정답.
- **queryKey 에 객체 직접 삽입 시 주의**: 객체 참조 동등성이 아니라 값 동등성을 본다. 인자로 받은 객체를 그대로 넣으면 렌더마다 새 객체가 되어도 내용이 같으면 같은 쿼리로 인식 — 안전.
- **enabled 로 조건부 실행**: userId 가 빈 문자열인 초기 상태에 fetch 되면 안 됨. `enabled: userId !== ''` 같은 가드 필수.
- **staleTime vs gcTime**: staleTime (기본 0) 은 "신선함" 기준, gcTime (기본 5분) 은 캐시 유지. 자주 바뀌지 않는 데이터는 staleTime 을 길게.
- **Optimistic update**: `onMutate` 에서 이전 캐시 백업 + 낙관적 업데이트, `onError` 에서 롤백. 생성 템플릿은 보수적 기본 (non-optimistic) — optimistic 은 옵션 플래그.
- **Strict TS**: useQuery 제네릭은 `useQuery<TData, TError>` 로 명시. v5 는 TError 를 `Error` 기본값으로 잡는데 우리는 Failure union 이 필요해서 명시 필수.

### 3.8 Clean Architecture 배치

- **feature 훅**: `src/presentation/features/<feature>/hooks/use-<resource>.ts`
- **공용 훅**: `src/presentation/shared/hooks/` (여러 feature 가 공유할 때)
- **절대 금지**: `domain/` 이나 `data/` 에 TanStack Query import. 데이터/도메인은 TanStack Query 를 모름. 훅은 presentation 레이어의 얇은 래퍼.

## 4. /react-form — React Hook Form + Zod

### 4.1 트리거

- 키워드: "폼 만들어줘", "form 생성", "react-form", "useForm"
- 조건: G1 초기화 완료 (`react-hook-form`, `@hookform/resolvers`, `zod` 설치됨)

### 4.2 입력

- `form_name` (필수): PascalCase (예: `LoginForm`, `UserEditForm`)
- `schema_ref` (선택): 이미 있는 domain entity Zod 스키마 경로. 없으면 인라인 정의
- `submit_action`: submit 시 호출할 usecase 함수 경로 또는 mutation 훅

### 4.3 useForm + zodResolver 통합

```tsx
// src/presentation/features/auth/components/login-form.tsx
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { ok, err, type Result } from 'neverthrow'

const LoginSchema = z.object({
  email: z.string().email('올바른 이메일을 입력하세요'),
  password: z.string().min(8, '비밀번호는 8자 이상이어야 합니다'),
})

type LoginFormValues = z.infer<typeof LoginSchema>

type LoginFailure =
  | { kind: 'login/invalid-credentials' }
  | { kind: 'login/network-error'; cause: string }

type Props = {
  onSubmit: (values: LoginFormValues) => Promise<Result<void, LoginFailure>>
}

export function LoginForm({ onSubmit }: Props) {
  const form = useForm<LoginFormValues>({
    resolver: zodResolver(LoginSchema),
    defaultValues: { email: '', password: '' },
  })

  const handleSubmit = form.handleSubmit(async (values) => {
    const result = await onSubmit(values)
    if (result.isErr()) {
      if (result.error.kind === 'login/invalid-credentials') {
        form.setError('root', { message: '이메일 또는 비밀번호가 올바르지 않습니다' })
      } else {
        form.setError('root', { message: '네트워크 오류. 다시 시도해주세요' })
      }
    }
  })

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label htmlFor="email">이메일</label>
        <input id="email" type="email" {...form.register('email')} />
        {form.formState.errors.email && (
          <p className="text-sm text-destructive">{form.formState.errors.email.message}</p>
        )}
      </div>
      <div>
        <label htmlFor="password">비밀번호</label>
        <input id="password" type="password" {...form.register('password')} />
        {form.formState.errors.password && (
          <p className="text-sm text-destructive">{form.formState.errors.password.message}</p>
        )}
      </div>
      {form.formState.errors.root && (
        <p className="text-sm text-destructive">{form.formState.errors.root.message}</p>
      )}
      <button type="submit" disabled={form.formState.isSubmitting}>
        {form.formState.isSubmitting ? '로그인 중…' : '로그인'}
      </button>
    </form>
  )
}
```

### 4.4 에러 표시 규칙

- **필드별 에러**: `form.formState.errors.<field>?.message` 를 바로 아래 `<p>` 에 표시
- **root 에러**: 제출 실패 (서버 에러, 네트워크 에러 등) 는 `form.setError('root', { message })` 로 폼 최상단에 표시
- **disabled 상태**: `form.formState.isSubmitting` 으로 submit 중 중복 제출 차단
- **접근성**: label 의 `htmlFor` ↔ input 의 `id` 매칭 필수. 에러 메시지는 `aria-describedby` 로 연결 권장

### 4.5 Submit 은 Result 반환

- submit 핸들러는 `Promise<Result<T, Failure>>` 를 반환받아 성공/실패 분기
- **절대 throw 금지**: 폼 제출 로직은 try/catch 대신 Result 체인. 상위 useCase 에서 이미 Result 로 변환되어 있어야 함
- **성공 후 처리**: 라우팅 (`navigate('/dashboard')`), 토스트, store 갱신 등은 `if (result.isOk()) { ... }` 블록에서

### 4.6 Gotchas

- **Zod v4 TypeScript 이슈**: React Hook Form + Zod v4 조합에서 `z.infer` 가 `unknown` 으로 잡히는 제네릭 타입 이슈가 있음 (react-hook-form/resolvers#781, #813 참조). `/react-form` 스킬은 Zod 스키마를 직접 `z.object(...)` 로 정의하고 `z.infer<typeof Schema>` 로 타입 파생하는 **직접 패턴** 만 생성. 제네릭 래퍼 (`type FormValues<T extends z.ZodType> = z.infer<T>`) 는 만들지 않음 (출처: https://github.com/react-hook-form/resolvers/issues/781).
- **resolver 와 수동 validate 병용 주의**: `zodResolver` 를 쓰면 resolver 쪽 검증이 우선. 필드별 `validate` 옵션은 resolver 통과 후에만 동작. 중복 검증 피할 것 (출처: https://github.com/orgs/react-hook-form/discussions/10153).
- **controlled 컴포넌트 (shadcn Select 등) 는 `Controller`**: `register()` 는 uncontrolled input 전용. shadcn 의 Select, Checkbox 같은 컨트롤드 컴포넌트에는 `Controller` 로 래핑 필수.
- **defaultValues 필수**: 초기값 없이 시작하면 uncontrolled → controlled 전환 경고. 빈 문자열이라도 명시.
- **`mode` 옵션**: 기본은 `onSubmit` (제출 시 검증). `onBlur`, `onChange`, `onTouched` 로 조절 가능. UX 요구에 따라 선택.
- **Strict TS**: `useForm<Values>()` 제네릭 명시 필수. `register('<field>')` 의 필드명은 Values 의 키로 타입 체크됨.

### 4.7 Clean Architecture 배치

- **폼 컴포넌트**: `src/presentation/features/<feature>/components/<name>-form.tsx`
- **스키마**: 폼 전용이면 같은 파일 인라인. 도메인 엔티티와 공유하면 `src/domain/entities/` 에서 import
- **submit 로직**: 컴포넌트 안에서 직접 호출하지 말고 `hooks/use-<action>.ts` (mutation 훅) 를 props 로 주입
- **절대 금지**: 폼 컴포넌트 안에서 직접 fetch, direct repository 호출. 반드시 hook 또는 UseCase 경유

## 5. 4개 스킬의 협력 흐름

```
사용자가 "사용자 프로필 편집 기능" 요청
         │
         ▼
/react-feature user-profile  (G1) — skeleton 생성
         │
         ▼
/react-api User                  (G2.2) — 4계층 생성
  └─ domain/entities/user.ts, failures, usecases
  └─ data/models/user-dto.ts, datasources, repository
         │
         ▼
/react-query User                (G2.3) — useQuery + useUpdateUserMutation 생성
  └─ presentation/features/user-profile/hooks/use-user.ts
  └─                           /hooks/use-update-user.ts
         │
         ▼
/react-store user-profile        (G2.1) — 클라이언트 상태 store 생성 (편집 중 dirty flag 등)
  └─ presentation/features/user-profile/store.ts
         │
         ▼
/react-form UserEditForm         (G2.4) — RHF 폼 컴포넌트 생성
  └─ presentation/features/user-profile/components/user-edit-form.tsx
  └─ submit 은 useUpdateUserMutation 의 mutationFn 을 props 로 주입
         │
         ▼
/react-screen UserProfile        (G1) — 화면에 폼 배치 + 라우트 등록
```

4개 스킬이 같은 feature 이름을 공유하며 순차적으로 호출되면 파일이 서로 맞물려 바로 동작한다. 각 스킬은 **G1 `/react-feature` 가 만든 skeleton 이 존재한다고 가정** 하므로, 없으면 먼저 실행을 안내한다.

## 6. 공유 Helpers 및 Cross-group 관계

- **Project detection**: G1 의 `react-kit/references/project-detection.md` 재사용
- **Clean Arch 레이아웃**: G1 의 `react-kit/references/clean-arch-layout.md` 재사용
- **Result 헬퍼**: `react-kit/references/result-patterns.md` 공용 레퍼런스 (G2 에서 신규 작성)

**Cross-group 관계**:
- G2 출력물은 **G3 `/react-wasm`** 이 WASM 호출을 data/datasources/wasm/ 로 추가할 때 확장됨
- **G4 `/react-test`** 가 G2 의 repository, hook, store 에 대한 Vitest + Testing Library 테스트 생성
- **G5 `/react-skeleton`** 이 useQuery 의 `isPending` 상태를 shimmer 로 표시
- **G6 `/react-audit`** 가 G2 산출물에서 Zod parse 누락, Result throw 대체 누락, Zustand 전체 구독 같은 안티패턴 검출

## 7. 출처 요약

1. Zustand 공식 문서: https://zustand.docs.pmnd.rs/
2. Zustand GitHub README: https://github.com/pmndrs/zustand
3. Zustand Auto Generating Selectors: https://zustand.docs.pmnd.rs/guides/auto-generating-selectors
4. TanStack Query v5 Query Invalidation: https://tanstack.com/query/v5/docs/react/guides/query-invalidation
5. TanStack Query v5 Invalidations from Mutations: https://tanstack.com/query/v5/docs/react/guides/invalidations-from-mutations
6. TanStack Query v5 useQuery Reference: https://tanstack.com/query/v5/docs/framework/react/reference/useQuery
7. TanStack Query v5 Mutations: https://tanstack.com/query/v5/docs/react/guides/mutations
8. TanStack Query v5 Migration Guide: https://tanstack.com/query/v5/docs/framework/react/guides/migrating-to-v5
9. React Hook Form useForm: https://react-hook-form.com/docs/useform
10. React Hook Form Resolvers: https://github.com/react-hook-form/resolvers
11. React Hook Form Resolvers Issue #781 (Zod v4 coerce TypeScript): https://github.com/react-hook-form/resolvers/issues/781
12. React Hook Form Resolvers Issue #813 (Zod v4 Type error): https://github.com/react-hook-form/resolvers/issues/813
13. neverthrow GitHub: https://github.com/supermacro/neverthrow
14. neverthrow README: https://github.com/supermacro/neverthrow/blob/master/README.md

## 8. 변경 이력

- **2026-04-10** — 초판. G2 4개 스킬 (`/react-store`, `/react-api`, `/react-query`, `/react-form`) 상세 설계. WebSearch fallback 으로 Zustand v5, TanStack Query v5, React Hook Form + Zod resolver, neverthrow 공식 문서 및 알려진 이슈 (#781, #813) 검증.
