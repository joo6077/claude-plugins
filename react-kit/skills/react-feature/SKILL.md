---
name: react-feature
description: >
  하나의 feature를 구성하는 domain/data/presentation/infrastructure 4계층 파일을 한 번에 생성한다.
  "기능 추가", "feature 만들어줘", "API 연동 화면", "새 기능 구현", "react-feature" 같은 요청 시 트리거.
  화면 파일만 추가할 때는 트리거하지 않는다 — /react-screen 사용.
  재사용 컴포넌트만 필요할 때는 트리거하지 않는다 — /react-widget 사용.
argument-hint: "<feature-name> [--with-api] [--with-route] [--schema=<path>]"
user-invocable: true
---

# Gotchas

1. **의존성 역순으로 생성** — Clean Architecture 규칙상 domain → data → presentation 순으로 생성해야 참조 에러가 없다. presentation 먼저 만들면 import가 존재하지 않는 파일을 참조해 tsc 오류 발생.
2. **경계에서 Zod parse 필수** — datasource는 raw response를 그대로 return하지 않는다. 반드시 `Schema.parse(json)`으로 검증 후 domain 타입으로 변환한다.
3. **Store는 feature 내부에서만 import** — 다른 feature가 이 feature의 store를 직접 참조하면 feature 간 결합이 생긴다. cross-feature 상태는 `src/presentation/shared/stores/`로 승격한다.
4. **Result 타입 일관** — 모든 UseCase는 `neverthrow`의 `Result<T, Failure>`를 반환한다. `throw` 금지.
5. **Zod `z.infer` 신뢰** — `z.infer`로 파생된 타입을 쓴다. 수동 `interface` 재정의 금지 (중복 + 불일치 위험).
6. **`export default` 금지** — named export로 통일한다 (Clean Arch 규칙 + tree-shaking 최적화).
7. **기존 파일 overwrite 금지** — 같은 경로 파일이 이미 존재하면 거부한다. `--force` 플래그가 있을 때만 덮어쓴다.
8. **실패 시 전체 롤백** — 5개 파일 중 하나라도 생성 실패 시 스킬 실행으로 생성된 파일을 모두 삭제하고 원상복구한다.
9. **Strict TS 통과 필수** — `tsc --noEmit`과 `eslint --max-warnings=0`을 통과해야 한다. `any`, `as` 단언, `!` non-null 단언 포함 금지.
10. **`@tauri-apps/*` 직접 import 금지** — presentation/data 레이어에서 Tauri API를 직접 import하면 레이어 경계 위반이다. 반드시 `src/infrastructure/tauri/`를 경유한다.

# Process

## 1. 프로젝트 환경 감지

`references/project-detection.md` 절차를 실행한다. shadcn 초기화 여부, TanStack Router 설치 여부, strict TS 설정을 확인한다. 미초기화 시 `/react-init`을 먼저 실행하도록 안내한다.

## 2. 입력 수집

- `feature_name` (필수): kebab-case (예: `user-profile`, `payment-history`)
- `--with-api` (기본 true): 백엔드 API 연동 코드 포함
- `--with-route` (기본 true): 라우트 등록
- `--schema` (선택): Zod 스키마 파일 경로 또는 인라인 정의

PascalCase 변형 계산: `user-profile` → `UserProfile`. kebab-case 유지: `user-profile`.

## 3. 중복 확인

아래 경로가 이미 존재하는지 확인한다:
- `src/domain/entities/<feature>.ts`
- `src/domain/failures/<feature>-failures.ts`
- `src/domain/usecases/<feature>-usecases.ts`
- `src/data/datasources/remote/<feature>-api.ts` (`--with-api` true 시)
- `src/data/models/<feature>-dto.ts`
- `src/data/repositories/<feature>-repository.ts`
- `src/presentation/features/<feature>/`

존재하면 `--force` 없이 거부하고 사용자에게 알린다.

## 4. 4계층 생성 (의존성 역순)

### 4-1. Domain — Entity + Failure

`src/domain/entities/<feature>.ts`:

```ts
import { z } from 'zod'

export const <Feature>Schema = z.object({
  id: z.string(),
  // TODO: feature에 맞는 필드 추가
})

export type <Feature> = z.infer<typeof <Feature>Schema>
```

`src/domain/failures/<feature>-failures.ts`:

```ts
export type <Feature>Failure =
  | { readonly type: 'not-found'; readonly id: string }
  | { readonly type: 'network-error'; readonly message: string }
  | { readonly type: 'validation-error'; readonly issues: string[] }
```

### 4-2. Domain — UseCase 인터페이스

`src/domain/usecases/<feature>-usecases.ts`:

```ts
import type { Result } from 'neverthrow'
import type { <Feature> } from '@/domain/entities/<feature>'
import type { <Feature>Failure } from '@/domain/failures/<feature>-failures'

export interface <Feature>Usecases {
  fetch<Feature>(id: string): Promise<Result<<Feature>, <Feature>Failure>>
  // TODO: feature에 맞는 유스케이스 추가
}
```

### 4-3. Data — DTO + Datasource + Repository (`--with-api` true 시)

`src/data/models/<feature>-dto.ts`:

```ts
import { z } from 'zod'
import type { <Feature> } from '@/domain/entities/<feature>'

export const <Feature>DtoSchema = z.object({
  id: z.string(),
  // TODO: API 응답 필드 추가
})

export type <Feature>Dto = z.infer<typeof <Feature>DtoSchema>

export function dto<Feature>(dto: <Feature>Dto): <Feature> {
  return {
    id: dto.id,
    // TODO: 변환 로직
  }
}
```

`src/data/datasources/remote/<feature>-api.ts`:

```ts
import { ok, err } from 'neverthrow'
import type { Result } from 'neverthrow'
import { <Feature>DtoSchema, dto<Feature> } from '@/data/models/<feature>-dto'
import type { <Feature> } from '@/domain/entities/<feature>'
import type { <Feature>Failure } from '@/domain/failures/<feature>-failures'

export async function fetch<Feature>Api(
  id: string,
): Promise<Result<<Feature>, <Feature>Failure>> {
  try {
    const res = await fetch(`/api/<feature>/${id}`)
    if (!res.ok) {
      return err({ type: 'network-error', message: res.statusText })
    }
    const json: unknown = await res.json()
    const parsed = <Feature>DtoSchema.safeParse(json)
    if (!parsed.success) {
      return err({
        type: 'validation-error',
        issues: parsed.error.issues.map((i) => i.message),
      })
    }
    return ok(dto<Feature>(parsed.data))
  } catch (e) {
    return err({ type: 'network-error', message: String(e) })
  }
}
```

`src/data/repositories/<feature>-repository.ts`:

```ts
import type { Result } from 'neverthrow'
import { fetch<Feature>Api } from '@/data/datasources/remote/<feature>-api'
import type { <Feature> } from '@/domain/entities/<feature>'
import type { <Feature>Failure } from '@/domain/failures/<feature>-failures'
import type { <Feature>Usecases } from '@/domain/usecases/<feature>-usecases'

export const <Feature>Repository: <Feature>Usecases = {
  async fetch<Feature>(id: string): Promise<Result<<Feature>, <Feature>Failure>> {
    return fetch<Feature>Api(id)
  },
}
```

### 4-4. Presentation — Store + Hook + Screen

`src/presentation/features/<feature>/store.ts`:

```ts
import { create } from 'zustand'
import type { <Feature> } from '@/domain/entities/<feature>'

type <Feature>State = {
  data: <Feature> | null
  isLoading: boolean
  set<Feature>: (data: <Feature>) => void
  reset: () => void
}

export const use<Feature>Store = create<<Feature>State>()((set) => ({
  data: null,
  isLoading: false,
  set<Feature>: (data) => set({ data }),
  reset: () => set({ data: null, isLoading: false }),
}))
```

`src/presentation/features/<feature>/hooks/use<Feature>.ts`:

```ts
import { useQuery } from '@tanstack/react-query'
import { <Feature>Repository } from '@/data/repositories/<feature>-repository'

export function use<Feature>(id: string) {
  return useQuery({
    queryKey: ['<feature>', id],
    queryFn: async () => {
      const result = await <Feature>Repository.fetch<Feature>(id)
      if (result.isErr()) throw result.error
      return result.value
    },
  })
}
```

`src/presentation/features/<feature>/screens/<Feature>Screen.tsx`:

```tsx
import * as React from 'react'
import { use<Feature> } from '../hooks/use<Feature>'

type Props = {
  id: string
}

export function <Feature>Screen({ id }: Props): React.JSX.Element {
  const { data, isLoading, isError } = use<Feature>(id)

  if (isLoading) return <div>Loading...</div>
  if (isError || !data) return <div>Error</div>

  return (
    <div>
      <h1><Feature></h1>
      {/* TODO: feature UI */}
    </div>
  )
}
```

`src/presentation/features/<feature>/index.ts` (public API):

```ts
export { <Feature>Screen } from './screens/<Feature>Screen'
export { use<Feature> } from './hooks/use<Feature>'
```

### 4-5. Route 등록 (`--with-route` true 시)

`/react-screen` 스킬 로직을 내부적으로 위임하여 `src/presentation/routes/<feature>.tsx`를 생성한다.

## 5. Strict TS 검증

```bash
pnpm tsc --noEmit
pnpm eslint src/domain/entities/<feature>.ts \
  src/domain/failures/<feature>-failures.ts \
  src/domain/usecases/<feature>-usecases.ts \
  src/data/models/<feature>-dto.ts \
  src/data/datasources/remote/<feature>-api.ts \
  src/data/repositories/<feature>-repository.ts \
  src/presentation/features/<feature>/ \
  --max-warnings=0
```

오류가 있으면 수정 후 재확인한다.

## 6. 완료 후 안내

생성 파일 목록 출력. 다음 단계:
- 스토어/쿼리 심화 설정: `/react-store`, `/react-query`, `/react-form`
- 테스트 생성: `/react-test`
- 추가 컴포넌트: `/react-widget`

# References

- `references/project-detection.md` — 프로젝트 감지
- `references/clean-arch-layout.md` — 4계층 배치 규칙 및 금지 import 방향
- `references/result-patterns.md` — neverthrow Result 패턴 상세
- `docs/react/kit-design/g1-scaffolding.md` §3 — 이 스킬의 상세 설계
