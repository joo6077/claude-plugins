# Result Patterns (neverthrow)

react-kit 의 모든 에러 경계는 `neverthrow` 의 `Result<T, E>` 를 사용. `throw` 금지.

## 기본 사용

```ts
import { ok, err, Result, ResultAsync } from 'neverthrow'

// 동기
function parse(raw: unknown): Result<User, UserFailure> {
  const parsed = UserSchema.safeParse(raw)
  if (!parsed.success) return err({ kind: 'user/validation-failed', issues: parsed.error.issues.map(i => i.message) })
  return ok(parsed.data)
}

// 비동기
function fetchUser(id: string): ResultAsync<User, UserFailure> {
  return ResultAsync.fromPromise(
    fetch(`/users/${id}`).then(r => r.json()),
    (e) => ({ kind: 'user/network-error', cause: String(e) })
  ).andThen(parse)
}
```

## Failure discriminated union

```ts
export type UserFailure =
  | { kind: 'user/not-found'; userId: string }
  | { kind: 'user/unauthorized' }
  | { kind: 'user/network-error'; cause: string }
  | { kind: 'user/validation-failed'; issues: string[] }
```

`kind` 필드로 switch/match 분기. 모든 케이스를 다뤘는지 TypeScript `never` 타입 exhaustiveness 검증.

## 레이어별 사용 규칙

| 레이어 | 사용 |
|--------|------|
| domain/usecases | **시그니처** `Promise<Result<T, Failure>>` 로 선언만 |
| data/datasources/remote | `ResultAsync.fromPromise(fetch(...), e => Failure)` 로 경계 변환 |
| data/repositories | datasource 호출 + Zod parse → Result 체인 |
| presentation/hooks | TanStack Query `queryFn` 안에서만 `throw result.error` (TanStack 이 error 로 포획) |
| presentation/components | `result.isErr()` / `isOk()` 로 분기, throw 금지 |

## 안티패턴

- ❌ `try/catch` 로 Failure 감추기 — 항상 Result 로 변환
- ❌ `throw new Error(JSON.stringify(failure))` — 타입 정보 손실
- ❌ `any` 로 에러 타입 우회
- ❌ domain 레이어에서 throw

## 관련 문서

- `docs/react/kit-design/g2-state-data.md` §2 `/react-api` — Clean Arch 4계층 + Result 체인
- `docs/react/kit-design/g4-quality.md` §2 `/react-error` — Severity 매핑 + UI 표시
