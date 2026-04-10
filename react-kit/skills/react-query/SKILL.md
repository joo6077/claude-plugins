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
