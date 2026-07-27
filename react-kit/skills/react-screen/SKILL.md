---
name: react-screen
description: >
  기존 React 프로젝트에 새 화면(Page)을 추가하고 TanStack Router 파일 기반 라우트를 등록한다.
  "화면 추가", "페이지 추가", "라우트 등록", "react screen", "new page", "new screen", "route 추가" 같은 요청 시 트리거.
  새 프로젝트 초기화가 필요하면 트리거하지 않는다 — /react-init 사용.
  feature 4계층 전체 생성이 필요하면 트리거하지 않는다 — /react-feature 사용.
argument-hint: "<ScreenName> [route-path] [--lazy] [--with-loader]"
user-invocable: true
---

# Gotchas

1. **`routeTree.gen.ts` 수동 수정 금지** — TanStack Router 플러그인이 덮어쓴다. 수정이 필요하면 플러그인 옵션을 조정한다.
2. **라우트 파라미터는 `$` prefix** — TanStack Router는 `$userId` 형태 사용. Next.js의 `[userId]`와 다르다.
3. **라우트 파일명 `-` prefix 제외** — TanStack Router 플러그인 기본 설정이 `-` prefix 파일을 무시한다. 특수 파일 네이밍 시 주의.
4. **`as any` 타입 우회 금지** — `createFileRoute`의 params 타입은 자동 추론된다. 수동 `as any` 캐스팅 코드 생성 금지.
5. **기존 파일 overwrite 금지** — 같은 경로의 파일이 이미 존재하면 거부한다. `--force` 플래그가 있을 때만 덮어쓴다.
6. **실패 시 전체 롤백** — 라우트 파일과 화면 파일 중 하나라도 생성 실패 시 스킬 실행으로 생성한 파일을 모두 삭제하고 원상복구한다.
7. **Strict TS 통과 필수** — 생성한 모든 TS 파일은 `tsc --noEmit`과 `eslint --max-warnings=0`을 통과해야 한다. `any`, `as` 단언, `!` non-null 단언 포함 금지.
8. **화면 컴포넌트는 features 하위에** — 라우트 파일은 얇게 위임만 한다. 실제 컴포넌트는 `src/presentation/features/<feature>/screens/`에 배치한다.
9. **`export default` 금지** — Clean Arch 규칙에 따라 named export로 통일한다.
10. **TanStack Router flat route 기본** — 파일 기반 라우팅에서 flat route (점 표기법 `posts.$postId.edit.tsx`) 를 기본으로 사용한다. 디렉토리 기반과 혼합도 지원되지만, flat route 가 파일 탐색이 간편하고 코드 스플리팅이 자동 적용된다. 특수 규칙: `__root.tsx` (루트 레이아웃), `_` prefix (pathless layout wrapper), `$` (동적 파라미터).
11. **React 19.2 `<Activity />` 로 탭/패널 pre-render** — `<Activity mode="visible|hidden">` 컴포넌트로 비활성 탭/패널을 낮은 우선순위로 pre-render 할 수 있다. hidden 모드에서 자식은 렌더되지만 Effect 는 mount 되지 않는다. 탭 전환 시 즉시 표시가 필요한 화면에 적합. 단, React 19.2+ 에서만 사용 가능하며 canary 채널에서 안정화 중이므로 적용 전 버전을 확인한다.
12. **Enumerate-before-Act (skill-design-guide §5.5)** — 화면을 생성하기 전에 기존 `src/presentation/routes/*` 와 `src/presentation/features/*/screens/*` 를 `Glob`/`Grep` 으로 전수 스캔하여 (a) 정확히 같은 경로뿐 아니라 (b) 유사 네이밍 라우트(`/user` vs `/users`)·중복 화면, (c) 같은 feature 에 이미 등록된 화면을 먼저 **모두 열거**한다. 열거 결과를 체크리스트로 사용자에게 보이고 합의한 뒤에만 파일을 생성한다. 단일 경로 존재 체크(Gotcha #5)만으로는 유사 네이밍 충돌을 못 잡아 라우트 트리가 오염된다 (insights-report #2 wrong_approach 대응 — "근사치 추정" 후 재작업 차단). 출처: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices#set-appropriate-degrees-of-freedom
13. **요청한 화면만 생성 — 임의 스캐폴딩 금지** — "화면 1개 추가" 요청에 store·provider·API 훅·테스트·레이아웃 래퍼를 요청 없이 덧붙이지 마라. 화면이 데이터를 필요로 하면 그 사실을 **먼저 알리고** `/react-query`·`/react-api` 별도 실행 여부를 확인한다. 풀 스택 자동 생성이 필요하면 `/react-feature` 를 안내한다 (insights-report #3 excessive_changes 대응 — 최소 viable 산출물 default).
14. **렌더 증거 없이 완료 선언 금지 (E2)** — `tsc` 통과는 화면이 실제로 그려진다는 증거가 아니다. 라우트가 등록됐고 타입이 맞아도 빈 화면이 렌더될 수 있다. 완료 직전에 `react-kit/references/render-evidence-protocol.md` 의 §4 체크리스트를 응답에 채운다. 증거를 얻을 수 없으면 해당 항목에 `[미검증]` 마커와 사유를 붙이고 **부분 완료로 보고**한다 — 조용히 넘기지 않는다. 임계값·마커 정의는 그 문서가 인용하는 상위 SSOT 를 따르며 여기서 재정의하지 않는다.

# Process

## 1. 프로젝트 환경 감지

`references/project-detection.md` 절차를 실행한다. TanStack Router 플러그인(`@tanstack/router-plugin`) 설치 여부를 확인한다. 미설치 시 `/react-init`을 먼저 실행하도록 안내한다.

## 2. 입력 수집

- `screen_name` (필수): PascalCase (예: `Dashboard`, `UserProfile`)
- `route_path` (선택): 기본값 = screen_name을 kebab-case로 변환 (예: `/dashboard`, `/users/$userId`)
- `--lazy` (기본 true): 동적 import 코드 스플리팅 적용
- `--with-loader` (기본 false): TanStack Router loader 함수 포함

feature 이름은 screen_name에서 추론한다 (예: `UserProfile` → feature `user-profile`).

## 3. 중복 확인

아래 경로가 이미 존재하는지 확인한다:
- `src/presentation/routes/<route-path>.tsx`
- `src/presentation/features/<feature>/screens/<ScreenName>Screen.tsx`

존재하면 `--force` 플래그 없이 거부하고 사용자에게 알린다.

## 4. 화면 컴포넌트 생성

`src/presentation/features/<feature>/screens/<ScreenName>Screen.tsx` 생성:

```tsx
import * as React from 'react'

export function <ScreenName>Screen(): React.JSX.Element {
  return (
    <div>
      <h1><ScreenName></h1>
    </div>
  )
}
```

`--with-loader` 플래그가 있으면 loader 데이터 타입과 `useLoaderData` 훅 호출을 추가한다.

## 5. 라우트 파일 생성

`src/presentation/routes/<route-path>.tsx` 생성. `--lazy` true(기본)이면 `lazyRouteComponent` 패턴 사용:

```tsx
import { createFileRoute, lazyRouteComponent } from '@tanstack/react-router'

export const Route = createFileRoute('<route-path>')({
  component: lazyRouteComponent(() =>
    import('@/presentation/features/<feature>/screens/<ScreenName>Screen').then(
      (m) => ({ default: m.<ScreenName>Screen }),
    ),
  ),
})
```

`--lazy false`이면 직접 import:

```tsx
import { createFileRoute } from '@tanstack/react-router'
import { <ScreenName>Screen } from '@/presentation/features/<feature>/screens/<ScreenName>Screen'

export const Route = createFileRoute('<route-path>')({
  component: <ScreenName>Screen,
})
```

`--with-loader` 플래그가 있으면 `loader` 함수를 추가하고 domain UseCase를 호출한다.

## 6. codegen 트리거 안내

Vite dev server가 실행 중이면 TanStack Router 플러그인이 `routeTree.gen.ts`를 자동 재생성한다. 수동 실행이 필요하면:

```bash
pnpm tsr generate
```

## 7. Strict TS 검증

```bash
pnpm tsc --noEmit
pnpm eslint src/presentation/routes/<route-path>.tsx src/presentation/features/<feature>/screens/<ScreenName>Screen.tsx --max-warnings=0
```

오류가 있으면 수정 후 재확인한다.

## 8. 완료 후 안내

생성 파일 목록 출력:
- `src/presentation/routes/<route-path>.tsx`
- `src/presentation/features/<feature>/screens/<ScreenName>Screen.tsx`

다음 단계:
- 이 화면에 데이터 연동이 필요하면: `/react-feature`
- 재사용 컴포넌트 추가: `/react-widget`

# References

- `references/project-detection.md` — 프로젝트 감지
- `references/clean-arch-layout.md` — 레이어 배치 (라우트는 `presentation/routes/`, 화면은 `presentation/features/<feature>/screens/`)
- `references/result-patterns.md` — loader에서 Result 패턴 활용 시
- `docs/react/kit-design/g1-scaffolding.md` §2 — 이 스킬의 상세 설계
