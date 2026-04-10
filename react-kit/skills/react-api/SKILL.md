---
name: react-api
description: >
  REST/GraphQL 엔드포인트를 domain → data → datasource → repository → usecase 4계층으로 일괄 또는 개별 생성한다.
  "API 연동", "엔드포인트 추가", "useCase 만들어줘", "repository 추가", "4계층 API", "react-api" 같은 요청 시 트리거.
  화면/컴포넌트만 필요할 때는 트리거하지 않는다 — /react-screen 또는 /react-widget 사용.
  TanStack Query 훅만 필요할 때는 트리거하지 않는다 — /react-query 사용.
argument-hint: "<ResourceName> [list,get,create,update,delete] [--only model|repository|usecase] [--schema=<path>]"
user-invocable: true
---

# Gotchas

1. **domain 레이어에서 throw 금지** — UseCase 시그니처는 반드시 `Promise<Result<T, Failure>>`를 반환한다. `throw`는 datasource 경계에서 `ResultAsync.fromPromise`로 포획한 뒤 Result로 변환하고, 이후 레이어는 Result 체인만 사용한다.
2. **Zod parse는 datasource 경계에서만** — `data/datasources/remote/`에서 raw JSON을 받는 순간 `Schema.safeParse()`로 검증한다. repository·usecase·컴포넌트에서 재검증하지 않는다. 검증된 도메인 타입을 신뢰한다.
3. **`z.infer` 단일 소스** — 수동 `interface` 재정의 금지. 도메인 타입은 항상 `z.infer<typeof Schema>`로 파생한다. 스키마와 타입이 어긋나면 strict TS 위반.
4. **DTO와 Domain 분리 필수** — API 응답 스키마(snake_case, 다른 필드명)가 도메인 모델과 같아 보여도 반드시 DTO를 따로 정의한다. API가 바뀌면 DTO만 수정하고 domain은 건드리지 않는다.
5. **서버 상태는 TanStack Query가 담당** — repository, usecase에서 직접 React state를 건드리지 않는다. 훅 레이어(`/react-query`)가 TanStack Query를 감싸 presentation에 제공한다.
6. **`fetch` 직접 사용은 datasource 안에서만** — repository에서 직접 fetch 금지. 공용 HTTP 클라이언트가 있으면 `src/infrastructure/http/client.ts`를 경유한다.
7. **HTTP 상태 코드 → Failure kind 매핑 필수** — 404 → `not-found`, 401 → `unauthorized`, 그 외 → `network-error`. 매핑 없이 단일 에러 타입으로 묶지 않는다.
8. **생성 순서 고정** — 반드시 domain → data 순으로 생성한다. presentation 먼저 만들면 존재하지 않는 import로 tsc 오류 발생.
9. **기존 파일 overwrite 금지** — 같은 경로 파일이 이미 존재하면 `--force` 없이 거부한다.
10. **`@tauri-apps/*` 직접 import 금지** — datasource에서 Tauri API를 직접 import하면 레이어 경계 위반. 반드시 `src/infrastructure/tauri/`를 경유한다.

# Process

## 1. 프로젝트 환경 감지

`references/project-detection.md` 절차를 실행한다. `neverthrow`, `zod` 패키지 설치 여부를 확인한다. 미설치 시 `/react-init`을 먼저 실행하도록 안내한다.

## 2. 입력 수집

- `resource_name` (필수): PascalCase 단수 (예: `User`, `Product`, `Order`)
- `operations` (선택): `list`, `get`, `create`, `update`, `delete` 중 복수 허용 (기본 `list,get`)
- `--only` (선택): `model`, `repository`, `usecase` 중 하나 — 개별 레이어만 생성
- `--base-url` (선택): API base URL. 없으면 `.env`의 `VITE_API_URL` 감지
- `--schema` (선택): 기존 Zod 스키마 파일 경로. 없으면 인터랙티브로 shape 수집

kebab-case 변형: `User` → `user`, `ProductCategory` → `product-category`.

## 3. 중복 확인

아래 경로가 이미 존재하는지 확인한다:

- `src/domain/entities/<resource>.ts`
- `src/domain/failures/<resource>-failures.ts`
- `src/domain/usecases/<resource>-usecases.ts`
- `src/data/models/<resource>-dto.ts`
- `src/data/datasources/remote/<resource>-api.ts`
- `src/data/repositories/<resource>-repository.ts`

존재하면 `--force` 없이 거부하고 사용자에게 알린다.

## 4. 4계층 생성 (domain → data 순)

### 4-1. Domain — Entity

`src/domain/entities/<resource>.ts`:

```ts
import { z } from 'zod'

export const <Resource>Schema = z.object({
  id: z.string().uuid(),
  // 도메인 필드를 여기에 추가
  createdAt: z.coerce.date(),
})

export type <Resource> = z.infer<typeof <Resource>Schema>
```

### 4-2. Domain — Failure

`src/domain/failures/<resource>-failures.ts`:

```ts
export type <Resource>Failure =
  | { readonly kind: '<resource>/not-found'; readonly id: string }
  | { readonly kind: '<resource>/unauthorized' }
  | { readonly kind: '<resource>/network-error'; readonly cause: string }
  | { readonly kind: '<resource>/validation-failed'; readonly issues: string[] }
```

`kind` 필드의 네이밍 규칙: `'<resource>/<reason>'` (소문자 kebab).

### 4-3. Domain — UseCase 인터페이스

`src/domain/usecases/<resource>-usecases.ts`:

```ts
import type { Result } from 'neverthrow'
import type { <Resource> } from '@/domain/entities/<resource>'
import type { <Resource>Failure } from '@/domain/failures/<resource>-failures'

export type <Resource>UseCases = {
  fetch<Resource>: (id: string) => Promise<Result<<Resource>, <Resource>Failure>>
  list<Resource>s: () => Promise<Result<<Resource>[], <Resource>Failure>>
  // operations 입력에 따라 create, update, delete 추가
}
```

UseCase는 시그니처만 선언한다. 구현은 repository가 담당.

### 4-4. Data — DTO

`src/data/models/<resource>-dto.ts`:

```ts
import { z } from 'zod'
import { <Resource>Schema, type <Resource> } from '@/domain/entities/<resource>'

// API 응답 스키마 (snake_case, API 필드명 기준)
export const <Resource>DtoSchema = z.object({
  id: z.string(),
  // API 응답 필드를 여기에 추가 (예: email_address, display_name)
  created_at: z.string(),
})

export type <Resource>Dto = z.infer<typeof <Resource>DtoSchema>

export function to<Resource>Domain(dto: <Resource>Dto): <Resource> {
  return <Resource>Schema.parse({
    id: dto.id,
    // DTO → Domain 필드 매핑
    createdAt: dto.created_at,
  })
}
```

### 4-5. Data — Datasource

`src/data/datasources/remote/<resource>-api.ts`:

```ts
import { ResultAsync } from 'neverthrow'
import type { <Resource>Failure } from '@/domain/failures/<resource>-failures'

const BASE = import.meta.env.VITE_API_URL

export function fetch<Resource>Dto(id: string): ResultAsync<unknown, <Resource>Failure> {
  return ResultAsync.fromPromise(
    fetch(`${BASE}/<resources>/${id}`).then(async (r) => {
      if (r.status === 404) throw { kind: '<resource>/not-found', id } as <Resource>Failure
      if (r.status === 401) throw { kind: '<resource>/unauthorized' } as <Resource>Failure
      if (!r.ok) throw { kind: '<resource>/network-error', cause: r.statusText } as <Resource>Failure
      return r.json() as Promise<unknown>
    }),
    (e) =>
      typeof e === 'object' && e !== null && 'kind' in e
        ? (e as <Resource>Failure)
        : { kind: '<resource>/network-error', cause: String(e) },
  )
}
```

Zod parse는 datasource가 아니라 repository에서 수행한다 (raw unknown → DTO parse → domain 변환 분리).

### 4-6. Data — Repository

`src/data/repositories/<resource>-repository.ts`:

```ts
import { err, ok } from 'neverthrow'
import { fetch<Resource>Dto } from '@/data/datasources/remote/<resource>-api'
import { <Resource>DtoSchema, to<Resource>Domain } from '@/data/models/<resource>-dto'
import type { <Resource>UseCases } from '@/domain/usecases/<resource>-usecases'

export const <resource>Repository: <Resource>UseCases = {
  fetch<Resource>: async (id) => {
    const result = await fetch<Resource>Dto(id)
    return result.andThen((raw) => {
      const parsed = <Resource>DtoSchema.safeParse(raw)
      if (!parsed.success) {
        return err({
          kind: '<resource>/validation-failed' as const,
          issues: parsed.error.issues.map((i) => i.message),
        })
      }
      return ok(to<Resource>Domain(parsed.data))
    })
  },

  list<Resource>s: async () => {
    // list 구현 (operations에 포함 시)
    return err({ kind: '<resource>/network-error', cause: 'not implemented' })
  },
}
```

## 5. Strict TS 검증

```bash
pnpm tsc --noEmit
pnpm eslint src/domain/entities/<resource>.ts \
  src/domain/failures/<resource>-failures.ts \
  src/domain/usecases/<resource>-usecases.ts \
  src/data/models/<resource>-dto.ts \
  src/data/datasources/remote/<resource>-api.ts \
  src/data/repositories/<resource>-repository.ts \
  --max-warnings=0
```

## 6. 완료 후 안내

생성 파일 목록 출력. 다음 단계:
- TanStack Query 훅 생성: `/react-query`
- 폼 연동: `/react-form`
- 스토어 연동: `/react-store`

# References

- `references/project-detection.md` — 프로젝트 환경 감지
- `references/clean-arch-layout.md` — 4계층 배치 규칙 및 금지 import 방향
- `references/result-patterns.md` — neverthrow Result 패턴 (ResultAsync.fromPromise, andThen, Failure discriminated union)
- `docs/react/kit-design/g2-state-data.md` §2 — 이 스킬 상세 설계 (각 레이어 역할, Zod parse 흐름, Gotchas)
