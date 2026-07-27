---
name: react-skeleton
description: >
  TanStack Query isPending 상태에 맞춰 실 레이아웃 모양의 shadcn Skeleton shimmer를 구현한다.
  스피너/CircularProgressIndicator 대신 "곧 이런 콘텐츠가 나올 거예요" 구조 예고를 제공.
  "스켈레톤", "shimmer", "로딩 UI", "loading skeleton", "로딩 상태", "skeleton loading",
  "스피너 교체", "로딩 화면" 같은 요청 시 트리거.
  shadcn Skeleton 컴포넌트 설치가 필요하면 먼저 안내한다.
argument-hint: "<target_path> [<query_hook>]"
user-invocable: true
---

# Gotchas

1. **스피너/Spinner 사용 금지** — `<Spinner />`, `<CircularProgressIndicator />` 같은 전통적 로딩 인디케이터 대신 항상 레이아웃 매칭 skeleton을 사용한다. Skeleton이 콘텐츠 구조를 예고하여 체감 로딩 시간을 줄인다.
2. **`bg-muted` 없으면 skeleton이 안 보임** — shadcn Skeleton은 `animate-pulse rounded-md bg-muted`로 구성된다. `bg-muted` 없이 `className`만 덮어쓰면 투명해서 shimmer 효과가 사라진다 (shadcn-ui/ui#5809).
3. **Skeleton 크기를 실제 레이아웃과 맞추지 않으면 레이아웃 shift** — skeleton 조각의 `h-*`, `w-*`이 실제 콘텐츠와 다르면 로딩→콘텐츠 전환 시 화면이 뛴다. 동일한 padding, gap, border-radius 유지.
4. **Empty 상태에 Skeleton 사용 금지** — Skeleton은 오직 `isPending === true`일 때만. 네트워크 성공인데 데이터가 없으면(`data.length === 0`) Empty UI를 보여준다. 혼동하면 "곧 뭔가 나올 것 같은" 잘못된 기대를 준다.
5. **Error 상태에 Skeleton 계속 보임** — `isError`를 분기하지 않으면 에러가 나도 skeleton이 유지된다. 반드시 `isPending → isError → empty → success` 순서로 분기한다.
6. **Strict TS: `data`는 `T | undefined`** — `isPending === false`여도 TanStack Query 타입상 `data`는 `T | undefined`다. `data!.name` 강제 단언 금지, `if (!data) return <Empty />` 체크 필수.
7. **반응형 skeleton 누락** — 실제 레이아웃이 `@container` 또는 breakpoint 반응형이면 skeleton도 동일 클래스로 변환한다. `/react-responsive`와 병용 가능.
8. **공용 skeleton 배치 혼동** — 단일 컴포넌트용 skeleton은 같은 파일 하단 private 함수. 여러 화면/feature가 공유하는 skeleton만 `shared/components/skeletons/`로 승격한다.
9. **"아무것도 안 보인다" 를 성공으로 읽지 마라 (E2)** — 이 스킬의 산출물은 **비어 보이는 것이 정상인 UI** 라서 검증 착오가 가장 쉽게 일어난다. 로딩 분기가 아예 렌더되지 않아 화면이 빈 것과, skeleton 이 정상 표시되어 회색 블록만 있는 것은 캡처상 구분되지 않을 수 있다. 부재 단정(`queryByTestId(...)` → `null`)은 컴포넌트가 렌더 실패했을 때도 통과하므로, **양성 대조(positive control)를 먼저 확보**한다 — pending 상태에서 skeleton 요소를 `getByRole`/`getByTestId` 로 지목하고, resolved 상태에서 실제 콘텐츠를 지목한 **두 증거를 쌍으로** 남긴다. 완료 직전에 `react-kit/references/render-evidence-protocol.md` 의 §3 (a) 와 §4 체크리스트를 채운다. 증거를 못 얻으면 `[미검증]` 마커와 사유를 붙이고 부분 완료로 보고한다.

# Process

## 1. 프로젝트 환경 감지

`references/project-detection.md` 절차를 실행한다:
- `components.json` 존재 여부 (shadcn 초기화 확인)
- `src/presentation/shared/components/ui/skeleton.tsx` 존재 여부
  - 없으면 설치 안내 후 중단:
    ```bash
    pnpm dlx shadcn@latest add skeleton
    ```
- `src/presentation/shared/lib/utils.ts`의 `cn` 헬퍼 확인

## 2. 입력 수집

- `target_path` (필수): 로딩 상태를 추가할 컴포넌트 경로
- `query_hook` (선택): 매칭되는 TanStack Query 훅 이름 (예: `useUser`). 없으면 파일에서 자동 탐지

## 3. 대상 파일 분석

`target_path` 파일을 읽고 다음을 파악한다:
- 현재 사용 중인 TanStack Query 훅 (`useQuery`, `useSuspenseQuery` 등)
- `isPending`, `isError`, `data` 상태를 이미 분기하는지 여부
- 실제 콘텐츠 레이아웃 구조 (container 래퍼, 간격, 텍스트 크기, 이미지 비율)
- 이미 skeleton이 구현되어 있으면 보강이나 수정만 제안한다

## 4. shadcn Skeleton 컴포넌트 기본

shadcn Skeleton은 `animate-pulse` 기반 단순 `<div>` 래퍼다:

```tsx
// src/presentation/shared/components/ui/skeleton.tsx
import { cn } from '@/presentation/shared/lib/utils'

type SkeletonProps = React.HTMLAttributes<HTMLDivElement>

export function Skeleton({ className, ...props }: SkeletonProps) {
  return (
    <div
      className={cn('animate-pulse rounded-md bg-muted', className)}
      {...props}
    />
  )
}
```

`bg-muted`가 기본으로 설정되므로 별도 배경색 추가 없이 `h-*`, `w-*`만 지정하면 된다.

## 5. 로딩 / 에러 / 빈 상태 분기 구조

3가지 상태를 명확히 구분해서 분기한다:

| 상태 | 조건 | 표시 | 액션 |
|------|------|------|------|
| **Loading** | `isPending === true` | Skeleton | 자동 대기 |
| **Error** | `isError === true` | Error UI + 재시도 버튼 | 재시도 |
| **Empty** | `!data` 또는 `data.length === 0` | Empty UI + CTA | CTA 클릭 |
| **Success** | data 있음 | 실제 콘텐츠 | — |

**표준 분기 패턴**:

```tsx
export function UserProfileCard({ userId }: { userId: string }) {
  const { data, isPending, isError, error } = useUser(userId)

  if (isPending) return <UserProfileCardSkeleton />
  if (isError) return <UserProfileCardError error={error} />
  if (!data) return <UserProfileCardEmpty />

  return (
    <div className="rounded-lg border p-6 space-y-4">
      <h2 className="text-xl font-semibold">{data.name}</h2>
      <p className="text-muted-foreground">{data.email}</p>
    </div>
  )
}
```

## 6. Skeleton 컴포넌트 생성

실제 레이아웃과 1:1 매핑하는 skeleton private 함수를 같은 파일 하단에 생성한다.

**크기 가이드**:
- 제목류 텍스트: `h-7 w-48`
- 본문류 텍스트: `h-5 w-64`
- 보조 텍스트: `h-4 w-32`
- 버튼: `h-10 w-24`
- 정사각형 아이콘/아바타: `size-10 rounded-full` (원형), `size-10` (사각형)
- 이미지: `aspect-video w-full` 또는 `aspect-square`

**Skeleton 생성 예시**:

```tsx
function UserProfileCardSkeleton() {
  return (
    <div className="rounded-lg border p-6 space-y-4">
      <Skeleton className="h-7 w-48" />        {/* 이름 자리 */}
      <Skeleton className="h-5 w-64" />        {/* 이메일 자리 */}
    </div>
  )
}

function UserProfileCardError({ error }: { error: unknown }) {
  return (
    <div className="rounded-lg border border-destructive/50 p-6 space-y-2">
      <p className="text-sm text-destructive">불러오는 중 오류가 발생했습니다.</p>
      <button
        onClick={() => void queryClient.invalidateQueries()}
        className="text-sm underline"
      >
        다시 시도
      </button>
    </div>
  )
}

function UserProfileCardEmpty() {
  return (
    <div className="rounded-lg border border-dashed p-6 text-center text-muted-foreground">
      표시할 사용자 정보가 없습니다.
    </div>
  )
}
```

## 7. 리스트 skeleton (반복 아이템)

리스트형 컴포넌트는 skeleton을 N개 반복한다. 실제 개수를 모르므로 3~5개가 적당하다:

```tsx
function PostListSkeleton() {
  return (
    <div className="space-y-4">
      {Array.from({ length: 4 }).map((_, i) => (
        <div key={i} className="rounded-lg border p-4 space-y-3">
          <div className="flex items-center gap-3">
            <Skeleton className="size-10 rounded-full" />
            <div className="space-y-1.5">
              <Skeleton className="h-4 w-32" />
              <Skeleton className="h-3 w-24" />
            </div>
          </div>
          <Skeleton className="h-5 w-3/4" />
          <Skeleton className="h-4 w-full" />
          <Skeleton className="h-4 w-2/3" />
        </div>
      ))}
    </div>
  )
}
```

## 8. 공용 skeleton 승격 조건

여러 feature나 화면이 같은 skeleton 형태를 공유하면 `shared/components/skeletons/`로 승격한다:

```text
src/presentation/shared/components/skeletons/
├── post-card-skeleton.tsx
├── user-profile-skeleton.tsx
└── data-table-skeleton.tsx
```

단일 컴포넌트 전용 skeleton은 같은 파일 하단 private 함수로 유지한다.

## 9. Strict TS 검증

```bash
pnpm tsc --noEmit
pnpm eslint <target_path> --max-warnings=0
```

## 10. 완료 후 안내

변경된 파일과 추가된 skeleton 컴포넌트를 요약한다.

다음 단계:
- 반응형 skeleton이 필요하면: `/react-responsive`
- 컴포넌트 재사용 패턴 감지: widget-inspector-react 에이전트
- 컴포넌트 품질 감사: `/react-audit`

# References

- `references/project-detection.md` — 프로젝트 감지 (shadcn 초기화 여부)
- `references/clean-arch-layout.md` — skeleton 배치 경로 (`shared/components/skeletons/`)
- `docs/react/kit-design/g5-ui-patterns.md` §2 — 이 스킬의 상세 설계
