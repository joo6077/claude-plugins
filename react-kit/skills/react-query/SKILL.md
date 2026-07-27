---
name: react-query
description: >
  /react-api가 생성한 repository를 감싸는 TanStack Query v5 훅(useQuery·useMutation)을 생성한다.
  "TanStack Query", "useQuery 만들어줘", "서버 상태", "캐싱 훅", "query hook", "react-query" 같은 요청 시 트리거.
  클라이언트 UI 상태(토글, 편집 중 데이터)를 관리할 때는 트리거하지 않는다 — /react-store 사용.
  API 계층(datasource, repository)이 없을 때는 /react-api를 먼저 실행하도록 안내한다.
argument-hint: "<ResourceName> [list,get,create,update,delete] [--feature=<name>] [--optimistic]"
user-invocable: true
---

# Gotchas

1. **TanStack Query = 서버 상태 전용** — API 응답, 캐시, 동기화가 TanStack Query 도메인. UI 토글·임시 편집 상태·WASM 진행 상태는 Zustand(react-store)가 담당. 서버 응답을 Zustand에 복사하면 두 개의 진실 공급원이 생겨 동기화 버그가 발생한다.
2. **queryFn 안에서 Result throw 필수** — TanStack Query는 queryFn이 throw 해야 에러를 `error` 필드로 잡는다. repository가 반환한 `Result`를 그대로 return하면 `data`가 `Result<T, E>` 타입으로 꼬인다. `if (result.isErr()) throw result.error` 로 언래핑한다.
3. **queryKey 3-레벨 배열 규칙 필수** — `[domain, subject, params]` 형태. `['user', 'detail', { id }]`, `['user', 'list', { page }]`. 일관성 없는 queryKey는 invalidation이 꼬인다.
4. **`domain/`·`data/` 레이어에서 TanStack Query import 금지** — 훅은 presentation 레이어의 얇은 래퍼다. 도메인·데이터 레이어는 TanStack Query를 몰라야 한다.
5. **`useQuery` 제네릭 명시 필수** — `useQuery<User, UserFailure>({...})`. v5 기본 TError는 `Error`인데, Failure discriminated union이 필요하므로 반드시 명시한다.
6. **`enabled` 가드 필수** — 파라미터가 아직 확정되지 않은 상태(빈 문자열, undefined)에서 fetch되지 않도록 `enabled: !!userId` 같은 조건을 항상 추가한다.
7. **staleTime vs gcTime 구분** — `staleTime` (기본 0): "데이터가 신선한 동안 재요청 안 함". `gcTime` (기본 5분): "비활성 캐시 보존 기간". 자주 바뀌지 않는 데이터는 staleTime을 길게 설정한다.
8. **invalidation 전략 선택** — 업데이트: `setQueryData(detail) + invalidateQueries(list)`. 생성: `invalidateQueries(list)`. 삭제: `removeQueries(detail) + invalidateQueries(list)`. 로그아웃: `queryClient.clear()`. 상황에 맞게 선택한다.
9. **TanStack Query v5 QueryClient 메서드 시그니처 object-form 강제** — v5 에서 `invalidateQueries`, `cancelQueries`, `removeQueries`, `resetQueries`, `getQueriesData`, `setQueriesData`, `ensureQueryData`, `isFetching` 가 모두 **`{ queryKey, ...filters }` 단일 object 인자**로 통일됐다. 복수 인자 형태는 v5 에서 제거 (TanStack Query v5 migration).

    나쁜 예 — v4 레거시 시그니처:

    ```ts
    queryClient.invalidateQueries(userKeys.list({ page: 1 }))
    queryClient.removeQueries(userKeys.detail(id), { exact: true })
    ```

    좋은 예 — v5 object form:

    ```ts
    queryClient.invalidateQueries({ queryKey: userKeys.list({ page: 1 }) })
    queryClient.removeQueries({ queryKey: userKeys.detail(id), exact: true })
    ```

10. **`queryOptions()` 유틸 + 3제네릭 명시로 select 타입 회귀 회피** — `queryOptions()` 로 queryKey/queryFn/select 를 재사용 가능한 객체로 묶으면 타입 안정성이 올라가지만, v5 초기에 **`queryOptions` + `select` 조합에서 `TData` 타입 추론이 `unknown` 으로 회귀하는 이슈**가 보고된 적 있다 (TanStack Query #5436). 방어책으로 `useQuery<TData, TError, TSelected>` 3 제네릭을 명시한다.

    권장 패턴:

    ```ts
    import { queryOptions, useQuery } from '@tanstack/react-query'

    export const userQueryOptions = (id: string) =>
      queryOptions({
        queryKey: userKeys.detail(id),
        queryFn: async () => {
          const result = await userRepository.fetchUser(id)
          if (result.isErr()) throw result.error
          return result.value
        },
        staleTime: 1000 * 60,
        enabled: id !== '',
      })

    // 기본 사용 — 3 제네릭 불필요 (Pass-through)
    const { data } = useQuery(userQueryOptions(id))

    // select 사용 시에만 3 제네릭 명시
    const { data: userName } = useQuery<User, UserFailure, string>({
      ...userQueryOptions(id),
      select: (u) => u.name,
    })
    ```

11. **Optimistic Updates — 두 가지 접근법 구분** — (1) `onMutate` 에서 캐시 직접 수정 + `onError` rollback: 서버 실패 시 이전 상태 복원. 복잡하지만 캐시 즉시 반영. (2) `useMutation` 의 `variables` 반환값으로 UI 낙관적 표시: 캐시를 건드리지 않아 무결성 유지에 유리하고 코드가 단순하다. **v5 에서 추가된 방식 (2) 를 기본으로 권장**하고, 다수 컴포넌트가 같은 캐시를 구독할 때만 방식 (1) 을 사용한다.

12. **`ensureQueryData` 로 중복 fetch 방지** — `queryClient.prefetchQuery()` 와 달리 `ensureQueryData()` 는 캐시에 데이터가 이미 있으면 fetch 를 건너뛴다. TanStack Router `loader` 에서 라우트 전환 전 데이터를 미리 가져올 때 `ensureQueryData` + `queryOptions()` 조합이 타입 안전하고 효율적이다.

    ```ts
    // route loader 에서 prefetch
    export const Route = createFileRoute('/users/$userId')({
      loader: ({ params }) =>
        queryClient.ensureQueryData(userQueryOptions(params.userId)),
    })
    ```

13. **Enumerate-before-Act (skill-design-guide §5.5)** — 쿼리 훅을 생성하기 전에 기존 `src/presentation/features/*/hooks/use*.ts` 와 queryKey 팩토리를 `Glob`/`Grep` 으로 전수 스캔하여 (a) 동일/유사 훅 명, (b) 같은 엔드포인트를 이미 구독하는 기존 훅, (c) 중복되는 queryKey prefix 를 먼저 **모두 열거**한다. 열거 결과를 체크리스트로 사용자에게 보이고 합의한 뒤에만 파일을 생성한다. queryKey 가 중복되면 invalidation 이 의도치 않은 쿼리까지 무효화한다 (insights-report #2 wrong_approach 대응). 출처: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices#set-appropriate-degrees-of-freedom

14. **요청한 쿼리만 — 임의 mutation·prefetch 확장 금지** — "조회 훅 추가" 요청에 mutation·optimistic update·prefetch·infinite query 를 요청 없이 임의로 덧붙이지 마라. 관련 mutation 이 필요해 보이면 그 사실을 **먼저 알리고** 추가 여부를 확인한다 (insights-report #3 excessive_changes 대응).

15. **Counterpart Enumeration — queryKey 를 바꾸면 무효화 쪽을 편집 전에 열거한다 (skill-design-guide §5.5 · E2)** — Gotcha #13 Enumerate-before-Act 가 **새 훅을 만들기 전 중복 스캔**이라면, 이 규칙은 **기존 queryKey 팩토리를 수정할 때의 반대편 열거**다. TanStack Query 공식 문서상 `invalidateQueries` 는 **prefix 매칭이 기본**이며 `['todos']` 무효화는 `['todos', { page: 1 }]` 까지 함께 무효화한다. 따라서 key 배열의 **앞부분을 바꾸거나 세그먼트를 삽입하면** mutation 쪽 무효화 blast radius 가 타입 오류 없이 조용히 달라진다 — 너무 많이 무효화되거나(과다 refetch), 아예 매칭되지 않아 **스테일 데이터가 화면에 남는다**. 공식 문서는 팩토리 정합성 가이드를 제공하지 않으므로 이 규칙이 그 자리를 메운다.

    **열거 대상 (Grep 으로 전수)**: `invalidateQueries` / `setQueryData` / `getQueryData` / `removeQueries` / `cancelQueries` 호출부 · `prefetchQuery` 지점 · `useQuery` 의 `enabled` 조건에서 같은 key 를 참조하는 곳 · `exact: true` 를 쓰는 호출부(세그먼트 추가에 가장 먼저 깨진다).

    열거 결과는 **체크리스트 아티팩트로 제출**한다 — "확인했다" 는 문장으로 대체하지 않는다. 한 스프린트에서 양쪽을 다 못 바꾸면 남는 쪽을 **명시적 미완 항목**으로 보고한다.

    ```text
    Bad:  userKeys.detail(id) 의 key 를 ['user', id] → ['users', 'detail', id] 로 변경
          → 훅 파일만 수정 → 뮤테이션의 invalidateQueries({ queryKey: ['user'] }) 가
             더 이상 매칭되지 않아 수정 후에도 옛 데이터가 계속 표시됨
    Good: 변경 전 Grep 'invalidateQueries|setQueryData|removeQueries' → 호출부 5 곳 열거
          → 팩토리 1 + 호출부 5 체크리스트 합의 → 6 곳 일괄 수정
    ```

    **부적합**: 아직 아무도 참조하지 않는 신규 팩토리 추가. 이 경우 열거 단계는 noise 다.

# Process

## 1. 프로젝트 환경 감지

`references/project-detection.md` 절차를 실행한다. `@tanstack/react-query` 패키지 설치 여부와 `QueryClientProvider` 설정 여부를 확인한다. 미설치 시 `/react-init`을 먼저 실행하도록 안내한다.

## 2. 입력 수집

- `resource_name` (필수): PascalCase (예: `User`, `Product`)
- `operations` (선택): `list`, `get`, `create`, `update`, `delete` 중 복수 허용 (기본 `list,get`)
- `--feature` (선택): feature 디렉토리 이름. 없으면 `src/presentation/shared/hooks/`에 생성
- `--optimistic` (기본 false): mutation에 optimistic update 패턴 포함

kebab-case 변형: `User` → `user`.

## 3. repository 존재 확인

`src/data/repositories/<resource>-repository.ts`가 없으면 `/react-api`를 먼저 실행하도록 안내한다.

## 4. 훅 생성

### 4-1. queryKey 상수

훅 파일 상단에 queryKey 팩토리를 정의한다:

```ts
const <resource>Keys = {
  all: ['<resource>'] as const,
  lists: () => [...<resource>Keys.all, 'list'] as const,
  list: (params: { page?: number }) => [...<resource>Keys.lists(), params] as const,
  details: () => [...<resource>Keys.all, 'detail'] as const,
  detail: (id: string) => [...<resource>Keys.details(), { id }] as const,
}
```

### 4-2. useQuery 훅 (`get` operation)

`src/presentation/features/<feature>/hooks/use-<resource>.ts`:

```ts
import { useQuery } from '@tanstack/react-query'
import { <resource>Repository } from '@/data/repositories/<resource>-repository'
import type { <Resource> } from '@/domain/entities/<resource>'
import type { <Resource>Failure } from '@/domain/failures/<resource>-failures'

export function use<Resource>(id: string) {
  return useQuery<<Resource>, <Resource>Failure>({
    queryKey: <resource>Keys.detail(id),
    queryFn: async () => {
      const result = await <resource>Repository.fetch<Resource>(id)
      if (result.isErr()) throw result.error
      return result.value
    },
    staleTime: 1000 * 60,  // 1분 — 리소스 특성에 맞게 조정
    enabled: id !== '',
  })
}
```

### 4-3. useQuery 훅 (`list` operation)

```ts
export function use<Resource>List(params: { page?: number } = {}) {
  return useQuery<<Resource>[], <Resource>Failure>({
    queryKey: <resource>Keys.list(params),
    queryFn: async () => {
      const result = await <resource>Repository.list<Resource>s()
      if (result.isErr()) throw result.error
      return result.value
    },
    staleTime: 1000 * 30,  // 30초 — 목록은 단건보다 짧게
  })
}
```

### 4-4. useMutation 훅 (`update` operation)

`src/presentation/features/<feature>/hooks/use-update-<resource>.ts`:

```ts
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { <resource>Repository } from '@/data/repositories/<resource>-repository'
import type { <Resource> } from '@/domain/entities/<resource>'

export function useUpdate<Resource>() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: async (<resource>: <Resource>) => {
      const result = await <resource>Repository.update<Resource>(<resource>)
      if (result.isErr()) throw result.error
      return result.value
    },
    onSuccess: (updated) => {
      // detail 캐시 직접 교체 (추가 네트워크 호출 없음)
      queryClient.setQueryData(<resource>Keys.detail(updated.id), updated)
      // list는 서버 기준으로 재조회
      queryClient.invalidateQueries({ queryKey: <resource>Keys.lists() })
    },
  })
}
```

### 4-5. useMutation 훅 (`create` operation)

```ts
export function useCreate<Resource>() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: async (input: Omit<<Resource>, 'id' | 'createdAt'>) => {
      const result = await <resource>Repository.create<Resource>(input)
      if (result.isErr()) throw result.error
      return result.value
    },
    onSuccess: () => {
      // 생성 후 list 재조회
      queryClient.invalidateQueries({ queryKey: <resource>Keys.lists() })
    },
  })
}
```

### 4-6. useMutation 훅 (`delete` operation)

```ts
export function useDelete<Resource>() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: async (id: string) => {
      const result = await <resource>Repository.delete<Resource>(id)
      if (result.isErr()) throw result.error
    },
    onSuccess: (_data, id) => {
      // detail 캐시 제거 + list 재조회
      queryClient.removeQueries({ queryKey: <resource>Keys.detail(id) })
      queryClient.invalidateQueries({ queryKey: <resource>Keys.lists() })
    },
  })
}
```

### 4-7. Optimistic update (`--optimistic` 옵션)

```ts
export function useUpdate<Resource>Optimistic() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: async (<resource>: <Resource>) => {
      const result = await <resource>Repository.update<Resource>(<resource>)
      if (result.isErr()) throw result.error
      return result.value
    },
    onMutate: async (updated) => {
      // 진행 중인 refetch 취소
      await queryClient.cancelQueries({ queryKey: <resource>Keys.detail(updated.id) })
      // 이전 캐시 스냅샷 저장
      const previous = queryClient.getQueryData<<Resource>>(<resource>Keys.detail(updated.id))
      // 낙관적 업데이트
      queryClient.setQueryData(<resource>Keys.detail(updated.id), updated)
      return { previous }
    },
    onError: (_err, updated, context) => {
      // 실패 시 롤백
      if (context?.previous) {
        queryClient.setQueryData(<resource>Keys.detail(updated.id), context.previous)
      }
    },
    onSettled: (updated) => {
      if (updated) {
        queryClient.invalidateQueries({ queryKey: <resource>Keys.detail(updated.id) })
      }
    },
  })
}
```

## 5. Strict TS 검증

```bash
pnpm tsc --noEmit
pnpm eslint src/presentation/features/<feature>/hooks/ --max-warnings=0
```

## 6. 완료 후 안내

생성 파일 목록 출력. 다음 단계:
- 폼 연동: `/react-form`
- 스켈레톤 로딩 UI: `/react-skeleton` (G5)
- 테스트 생성: `/react-test` (G4)

# References

- `references/project-detection.md` — 프로젝트 환경 감지
- `references/clean-arch-layout.md` — 레이어 배치 규칙 및 금지 import 방향
- `references/result-patterns.md` — neverthrow Result 패턴 (queryFn에서 throw로 언래핑)
- `docs/react/kit-design/g2-state-data.md` §3 — 이 스킬 상세 설계 (queryKey 규칙, invalidation 전략, Gotchas)
