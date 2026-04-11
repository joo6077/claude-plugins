---
name: react-store
description: >
  feature별 또는 전역 Zustand 스토어와 selector 훅을 생성한다.
  "Zustand 스토어", "스토어 만들어줘", "클라이언트 상태", "상태 관리", "global state", "store 만들어줘" 같은 요청 시 트리거.
  서버 데이터(API 응답, 캐시)를 관리할 때는 트리거하지 않는다 — /react-query 사용.
  화면/컴포넌트만 필요할 때는 트리거하지 않는다 — /react-screen 또는 /react-widget 사용.
argument-hint: "<store-name> [feature|shared] [--with-persist]"
user-invocable: true
---

# Gotchas

1. **Zustand = 클라이언트 상태 전용** — UI 토글, 편집 중 임시 데이터, WASM 진행 상태, 사용자 선호도가 Zustand 도메인. 서버 응답을 Zustand에 복사하면 두 개의 진실 공급원이 생겨 동기화 버그가 발생한다. 서버 상태는 TanStack Query(react-query)가 단일 진실 공급원.
2. **`create<Store>()(...)` 이중 괄호 필수** — `create()` 안에 제네릭을 넣는 Zustand v5+ 권장 패턴. `create<Auth>(...)` 단일 괄호는 타입 추론이 깨진다.
3. **selector 없이 전체 구독 금지** — `const store = useAuthStore()` 처럼 인자 없이 호출하면 모든 state 키에 구독되어 불필요한 리렌더가 폭증한다. 반드시 selector 경유: `useAuthStore((s) => s.user)`.
4. **selector hook 자동 생성 필수** — `useAuthUser`, `useIsAuthenticated` 같은 이름의 selector 래퍼를 함께 생성한다. 컴포넌트에서 `useAuthStore((s) => ...)` 직접 호출을 막기 위한 캡슐화.
5. **`domain/`·`data/` 레이어에서 Zustand import 금지** — 도메인/데이터 레이어는 UI 상태 라이브러리를 몰라야 한다. `presentation/` 레이어에서만 import.
6. **Actions 안에서 `get()` 주의** — 이전 상태로부터 다음 상태를 계산할 때는 `set((state) => ({ ... }))` 함수 형태가 안전하다. `get()` 은 동시 업데이트 시 race condition 위험.
7. **persist 직렬화 주의** — `Map`, `Set`, `Date` 객체는 기본 JSON 직렬화가 안 된다. `--with-persist` 옵션 사용 시 `createJSONStorage` 커스터마이즈 또는 primitive 값만 저장.
8. **`createStore` vs `create` 혼동 금지** — `create`는 전역 훅 기반 (react-kit 기본). `createStore`는 React Context로 여러 인스턴스를 제공하거나 SSR 할 때만 사용.
9. **Zustand v5 객체/배열 selector trap — `useShallow` 강제** — v5(2024-11 stable)는 use-sync-external-store shim 을 제거하고 React 18+ 네이티브 `useSyncExternalStore` 를 사용한다. selector 가 매번 새 객체/배열을 반환하면 React 가 "Maximum update depth exceeded" 를 throw 하며 컴포넌트 트리 unmount — 성능 문제가 아니라 **크래시**다. v5 에서는 반드시 `zustand/react/shallow` 의 `useShallow` 로 감싼다 (Zustand v5 announce, v5 migration).

    나쁜 예 — 매 렌더마다 새 객체:

    ```ts
    const { user, token } = useAuthStore((s) => ({ user: s.user, token: s.token }))
    // → Maximum update depth exceeded
    ```

    좋은 예 — useShallow 로 얕은 비교:

    ```ts
    import { useShallow } from 'zustand/react/shallow'

    const [user, token] = useAuthStore(
      useShallow((s) => [s.user, s.token] as const),
    )
    ```

    단일 필드 구독은 `useAuthStore((s) => s.user)` 그대로 괜찮다 — primitive/reference equality 로 이미 안전.

10. **v5 에서 커스텀 equality function 은 `createWithEqualityFn` 로** — `create()` 는 v5 에서 equality customizing 을 지원하지 않는다. 특수한 비교가 필요하면 `zustand/traditional` 의 `createWithEqualityFn` 을 쓰고, 일반적으로는 `useShallow` 로 충분하다.
11. **최소 React 버전 18+** — v5 는 React 17 이하 미지원. react-kit 은 React 19 가 기본이므로 이슈 없음, 단 공용 라이브러리 프로젝트에서 v4→v5 마이그레이션 시 피어 의존성을 사전 확인한다.

# Process

## 1. 프로젝트 환경 감지

`references/project-detection.md` 절차를 실행한다. `zustand` 패키지 설치 여부를 `package.json`에서 확인한다. 미설치 시 `/react-init`을 먼저 실행하도록 안내한다.

## 2. 입력 수집

- `store_name` (필수): kebab-case (예: `auth-store`, `cart-store`, `upload-store`)
- `scope` (기본 `feature`): `feature`이면 `src/presentation/features/<feature>/store.ts`, `shared`이면 `src/presentation/shared/stores/<name>.ts`
- `--with-persist` (기본 false): persist 미들웨어 포함 여부
- `state_shape` (선택): 초기 상태 shape를 인터랙티브로 또는 인라인으로 입력

PascalCase 변형 계산: `auth-store` → `Auth`, `useAuthStore`.

## 3. 중복 확인

대상 경로에 이미 파일이 있으면 `--force` 없이 거부하고 사용자에게 알린다.

## 4. 스토어 파일 생성

### 4-1. feature 스토어 (`scope: feature`)

`src/presentation/features/<feature>/store.ts`:

```ts
import { create } from 'zustand'
import { useShallow } from 'zustand/react/shallow'
import type { <Entity> } from '@/domain/entities/<entity>'

type <Feature>State = {
  // 클라이언트 상태 필드 (UI, 편집 중 임시 데이터 등)
  <field>: <Type> | null
}

type <Feature>Actions = {
  set<Field>: (<field>: <Type>) => void
  clear: () => void
}

type <Feature>Store = <Feature>State & <Feature>Actions

const initialState: <Feature>State = {
  <field>: null,
}

export const use<Feature>Store = create<<Feature>Store>()((set) => ({
  ...initialState,
  set<Field>: (<field>) => set({ <field> }),
  clear: () => set(initialState),
}))

// Selector hooks — 컴포넌트에서 직접 useFeatureStore((s) => ...) 대신 사용
// 단일 primitive 는 selector 직접, 다중 필드는 useShallow 필수 (Zustand v5)
export const use<Feature><Field> = () => use<Feature>Store((s) => s.<field>)

// 다중 필드 구독 — useShallow 로 감싸 객체 selector trap 을 회피한다
export const use<Feature>Slice = () =>
  use<Feature>Store(
    useShallow((s) => ({ <field>: s.<field> })),
  )
```

### 4-2. 전역 shared 스토어 (`scope: shared`)

`src/presentation/shared/stores/<name>.ts` 에 동일 패턴으로 생성. feature 이름 대신 도메인 이름 사용.

### 4-3. persist 포함 (`--with-persist`)

```ts
import { create } from 'zustand'
import { persist, createJSONStorage } from 'zustand/middleware'

export const use<Feature>Store = create<<Feature>Store>()(
  persist(
    (set) => ({
      ...initialState,
      set<Field>: (<field>) => set({ <field> }),
      clear: () => set(initialState),
    }),
    {
      name: '<feature>-store',       // localStorage 키
      storage: createJSONStorage(() => localStorage),
      partialize: (state) => ({ <persistedField>: state.<persistedField> }),
    },
  ),
)
```

`partialize`로 persist 할 필드를 명시한다. 민감 정보나 임시 UI 상태는 제외.

### 4-4. React 외부 접근 (WASM 콜백, Worker 메시지용)

스토어 파일 하단에 사용 예시 주석 형태로 포함:

```ts
// React 컴포넌트 트리 밖에서 직접 상태 갱신 (예: WASM 콜백, Worker 메시지)
//   use<Feature>Store.setState({ progress: 0.8 })
//
// 현재 상태 읽기 (훅 규칙 없이 스냅샷)
//   const current = use<Feature>Store.getState().<field>
```

## 5. Strict TS 검증

```bash
pnpm tsc --noEmit
pnpm eslint src/presentation/features/<feature>/store.ts --max-warnings=0
```

## 6. 완료 후 안내

생성 파일 목록 출력. 다음 단계:
- 서버 데이터 페칭 훅: `/react-query`
- 폼 상태 연동: `/react-form`
- 화면 배치: `/react-screen`

# References

- `references/project-detection.md` — 프로젝트 환경 감지
- `references/clean-arch-layout.md` — 레이어 배치 규칙 및 금지 import 방향
- `docs/react/kit-design/g2-state-data.md` §1 — 이 스킬 상세 설계 (Zustand TypeScript 패턴, WASM 접근, Gotchas)
