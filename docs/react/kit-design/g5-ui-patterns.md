# G5 — UI Patterns Skills

```yaml
last_updated: 2026-04-10
group: G5
scope: react-kit UI 패턴 스킬 3종
skills: [/react-responsive, /react-skeleton, /react-extract]
depends_on: [G1 /react-widget, G2 /react-query]
agents: [widget-inspector-react]
sibling_skill: "/react-animation 은 별도 전용 문서 docs/react/kit-design/g5b-animation.md 에서 설계"
research_sources:
  - Tailwind v4 공식 문서 (tailwindcss.com) — container queries 내장
  - shadcn/ui Skeleton 컴포넌트 문서
  - TanStack Query v5 isPending 상태
  - 2026-04 WebSearch 검증
```

## 문서 목적

react-kit **G5 그룹** 은 기존 컴포넌트 위에 **UI 품질 레이어**를 얹는 세 스킬이다.

- **`/react-responsive`** — 반응형 레이아웃 적용. Tailwind v4 의 페이지 breakpoint 와 container queries 를 상황에 맞게 혼용.
- **`/react-skeleton`** — 로딩 상태를 CircularProgressIndicator 대신 실 레이아웃 모양의 shimmer skeleton 으로 표시.
- **`/react-extract`** — feature 내부에 중복·사유화된 위젯을 감지하여 `presentation/shared/components/` 로 추출하고 import 경로 자동 정리.

**의존**: G1 `/react-widget` 이 만든 cva + forwardRef 구조를 전제. G2 `/react-query` 의 `isPending` / `isError` 상태를 skeleton 분기에 사용.

## 공통 설계 원칙

- **기존 구조 비파괴**: 3개 스킬 모두 기존 컴포넌트를 **래핑하거나 변환**하지, 처음부터 다시 만들지 않는다. 이미 잘 동작하는 코드를 건드려서 회귀를 내지 않도록.
- **Strict TS 유지**: 추출된 공용 컴포넌트도 G1 의 strict 규칙 (`any` 금지, `forwardRef`, Props 타입 명시) 을 그대로 준수.
- **디자인 시스템 호환**: `design-kit` 의 토큰 (컬러, 스페이싱, 라디우스) 을 그대로 쓰는 Tailwind 클래스만 사용. 하드코딩된 픽셀값 금지.
- **project-detection 공유**: Tailwind 메이저 버전 감지 — v4 면 `@container` 내장 사용, v3 이면 `@tailwindcss/container-queries` 플러그인 필요.

## 1. /react-responsive — 반응형 레이아웃 적용

기존 화면/컴포넌트를 반응형으로 전환하거나 새로 반응형 레이아웃을 적용한다.

### 1.1 트리거

- 키워드: "반응형", "responsive", "태블릿 대응", "2컬럼", "breakpoint", "container queries"
- 조건: Tailwind v4 설치된 프로젝트

### 1.2 입력

- `target_path` (필수): 적용할 컴포넌트/화면 경로
- `breakpoints` (선택): 활성화할 breakpoint 목록 (기본 `['sm', 'md', 'lg', 'xl']`)
- `--container-query`: 컨테이너 쿼리 우선 사용 (컴포넌트 단위)
- `--page-query`: 페이지 breakpoint 우선 사용 (화면 단위, 기본)

### 1.3 Tailwind v4 breakpoint 체계

Tailwind v4 의 기본 페이지 breakpoint:

| 키 | min-width | 용도 |
|----|-----------|------|
| `sm:` | 640px | 큰 모바일 / 세로 태블릿 |
| `md:` | 768px | 세로 태블릿 |
| `lg:` | 1024px | 가로 태블릿 / 작은 노트북 |
| `xl:` | 1280px | 노트북 |
| `2xl:` | 1536px | 큰 데스크탑 |

**적용 예시** — 그리드 반응형:

```tsx
<div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
  {items.map((item) => <Card key={item.id} {...item} />)}
</div>
```

### 1.4 Container Queries (`@container`)

Tailwind v4 는 `@container` 유틸리티가 **내장** — 별도 플러그인 불필요. 컴포넌트를 컨테이너로 선언하면 그 안의 자식들이 컨테이너 크기에 반응한다.

```tsx
<div className="@container">
  <div className="grid grid-cols-1 @md:grid-cols-2 @xl:grid-cols-3">
    <!-- 부모 @container 의 너비가 @md (28rem) 이상이면 2컬럼 -->
  </div>
</div>
```

**기본 컨테이너 크기**:

| 키 | min-width |
|----|-----------|
| `@xs` | 20rem (320px) |
| `@sm` | 24rem (384px) |
| `@md` | 28rem (448px) |
| `@lg` | 32rem (512px) |
| `@xl` | 36rem (576px) |
| `@2xl` | 42rem (672px) |
| `@3xl` ~ `@7xl` | 더 큼 |

**네임드 컨테이너** — 여러 컨테이너가 중첩될 때 이름으로 타겟:

```tsx
<div className="@container/sidebar">
  <aside>
    <div className="@md/sidebar:text-lg">
      <!-- sidebar 컨테이너가 @md 이상일 때만 -->
    </div>
  </aside>
</div>
```

### 1.5 "페이지 크기 기반" vs "컨테이너 크기 기반" 결정 규칙

| 시나리오 | 선택 | 이유 |
|----------|------|------|
| **앱 최상위 레이아웃** (사이드바 펼침/접힘, 상단 네비 분기) | **페이지 (sm/md/lg)** | 뷰포트 전체가 레퍼런스. 전체 앱 구조 결정 |
| **그리드 아이템 재배치** (카드 목록 1→2→3 컬럼) | **페이지 (sm/md/lg)** | 유저가 "화면 크기" 로 기대하는 경험 |
| **사이드바 안의 카드** (같은 카드가 전체 화면에도, 모달 안에도) | **컨테이너 (`@container`)** | 부모 영역 크기에 따라 적응해야 재사용 가능 |
| **재사용 컴포넌트 내부 레이아웃** (Card 안의 header/meta 배치) | **컨테이너 (`@container`)** | 컴포넌트가 어디에 들어가도 올바르게 보임 |
| **모달/드로어 내부** | **컨테이너 (`@container`)** | 모달 너비 기준, 페이지 너비가 아니라 |
| **인쇄/PDF 출력** | 페이지 | 고정 폭 매체 |

**원칙**: 컴포넌트의 **재사용 범위가 어디까지인가** 가 판단 기준. 화면 전체에서만 쓰이면 페이지, 여러 컨텍스트에서 쓰이면 컨테이너.

`/react-responsive` 는 대상 파일 경로를 보고 자동 판단:
- `routes/*.tsx` 또는 `features/<feature>/screens/*.tsx` → 페이지 쿼리
- `shared/components/**/*.tsx` 또는 `features/<feature>/components/**/*.tsx` → 컨테이너 쿼리 우선 (fallback 페이지)
- 명시적 플래그 (`--container-query` / `--page-query`) 로 override

### 1.6 Fallback 규칙

- **breakpoint 미대응 상태**: 가장 작은 너비에서 가장 안전한 레이아웃이 **기본값** — 즉 `grid-cols-1` 을 먼저 선언하고 `sm:grid-cols-2` 로 확장. 모바일 퍼스트 원칙
- **`@container` 미지원 구형 브라우저**: Tailwind v4 container queries 는 Chrome 105+, Safari 16+, Firefox 110+ 에서 동작. 구형 타겟이 필요하면 `--page-query` fallback
- **이미지/미디어 aspect-ratio**: `aspect-video`, `aspect-square` 같은 Tailwind 유틸로 breakpoint 독립적으로 비율 유지

### 1.7 변환 예시 — 기존 컴포넌트에 적용

**Before** (고정 레이아웃):

```tsx
export function ProductGrid({ products }: { products: Product[] }) {
  return (
    <div className="grid grid-cols-3 gap-4">
      {products.map((p) => <ProductCard key={p.id} {...p} />)}
    </div>
  )
}
```

**After** (`/react-responsive` 실행 후):

```tsx
export function ProductGrid({ products }: { products: Product[] }) {
  return (
    <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
      {products.map((p) => <ProductCard key={p.id} {...p} />)}
    </div>
  )
}
```

재사용 컴포넌트 (예: 사이드바 안에도 쓰이는 카드 목록) 라면 `@container` 로 변환:

```tsx
export function ProductList({ products }: { products: Product[] }) {
  return (
    <div className="@container">
      <div className="grid grid-cols-1 gap-3 @md:grid-cols-2 @xl:grid-cols-3">
        {products.map((p) => <ProductCard key={p.id} {...p} />)}
      </div>
    </div>
  )
}
```

### 1.8 Gotchas

- **컨테이너 쿼리가 페이지 쿼리를 대체하지 않음**: 둘은 서로 다른 문제를 푼다. 앱 최상위 구조 결정에는 페이지 쿼리가 맞다. 모든 것을 `@container` 로 감쌀 필요 없음
- **`@container` 컨텍스트 손실**: `display: contents` 같은 스타일이 중간에 끼면 컨테이너 선언이 자식에게 전달 안 될 수 있음
- **Tailwind v3 에서 container queries**: v3 프로젝트는 `@tailwindcss/container-queries` 플러그인 설치 + `tailwind.config.ts` 에 등록 필요. `/react-responsive` 가 감지해서 안내
- **텍스트 크기 반응형 과용**: `text-sm md:text-base lg:text-lg` 같은 다단 변경은 타이포 리듬 깨짐. 디자인 시스템의 정해진 scale 만 사용
- **Strict TS 영향 없음**: Tailwind 클래스는 문자열이라 TS 영향 밖. 하지만 `cn()` 유틸 경유로 조건부 클래스 합성 권장

### 1.9 Clean Architecture 배치

- 변경 대상: `src/presentation/features/**/*.tsx`, `src/presentation/shared/components/**/*.tsx`
- 새 파일 생성 없음 — 기존 파일의 className 을 수정하는 스킬

## 2. /react-skeleton — 로딩 상태 shimmer 구현

TanStack Query `isPending` 중에 실 레이아웃 모양의 shadcn Skeleton 조각을 표시한다. 스피너 대신 "곧 이런 콘텐츠가 나올 거예요" 라는 **구조 예고**를 한다.

### 2.1 트리거

- 키워드: "로딩 화면", "스켈레톤", "shimmer", "loading UI", "스피너 교체"
- 조건: shadcn Skeleton 컴포넌트 설치됨 (`pnpm dlx shadcn@latest add skeleton`). 없으면 먼저 설치 안내

### 2.2 입력

- `target_path` (필수): 로딩 상태를 추가할 컴포넌트 경로
- `query_hook` (선택): 매칭되는 TanStack Query 훅 이름 (예: `useUser`). 없으면 자동 탐지

### 2.3 shadcn Skeleton 컴포넌트 기본

shadcn Skeleton 은 `animate-pulse` 기반의 단순 `<div>` 래퍼:

```tsx
// src/presentation/shared/components/ui/skeleton.tsx (shadcn 원본)
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

**핵심**: `bg-muted` 가 필수 (배경색 없으면 안 보임), `animate-pulse` 가 Tailwind 내장 애니메이션.

### 2.4 TanStack Query isPending 연동 패턴

`/react-skeleton` 이 생성하는 로딩 분기 패턴:

```tsx
// src/presentation/features/user/components/user-profile-card.tsx
import { Skeleton } from '@/presentation/shared/components/ui/skeleton'
import { useUser } from '../hooks/use-user'

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

function UserProfileCardSkeleton() {
  return (
    <div className="rounded-lg border p-6 space-y-4">
      <Skeleton className="h-7 w-48" />          {/* 제목 자리 */}
      <Skeleton className="h-5 w-64" />          {/* 부제목 자리 */}
    </div>
  )
}

function UserProfileCardError({ error }: { error: unknown }) {
  return (
    <div className="rounded-lg border border-destructive/50 p-6">
      <p className="text-sm text-destructive">불러오는 중 오류가 발생했습니다.</p>
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

### 2.5 Skeleton 설계 원칙

- **실 레이아웃과 1:1 매핑**: skeleton 조각의 크기·위치가 실제 콘텐츠와 거의 같아야 "깜빡임" 없는 전환
- **개수 제한**: 너무 많은 skeleton 은 산만. 카드 하나 당 2~4 개 블록이 적당
- **텍스트는 `h-4`~`h-7`, 버튼은 `h-9`~`h-10`, 이미지는 `aspect-square`/`aspect-video`** — Tailwind 유틸로 높이 고정
- **`rounded-md` 기본**: 사각형 skeleton 은 아이콘이나 이미지 영역에만. 텍스트 skeleton 은 rounded

### 2.6 로딩 / 에러 / 빈 상태 구분

3가지 상태를 **명확히 구분해서 분기**한다. 혼동하면 UX 가 나빠진다:

| 상태 | 조건 | 표시 | 사용자 액션 |
|------|------|------|-----------|
| **Loading** | `isPending === true` | Skeleton | 기다림 (자동) |
| **Error** | `isError === true` | Error 메시지 + "다시 시도" 버튼 | 재시도 |
| **Empty** | `data === undefined` 또는 빈 배열 | "표시할 데이터 없음" + 주요 액션 안내 | CTA 클릭 |
| **Success** | data 있음 | 실제 콘텐츠 | — |

**Skeleton 이 쓰이는 건 오직 Loading 뿐**. Empty 상태에 Skeleton 을 써서 "곧 뭐가 나올 것 같다" 는 오해를 주지 말 것. Error 도 마찬가지 — Error 는 Error UI, Empty 는 Empty UI.

### 2.7 Gotchas

- **`animate-pulse` 미동작**: shadcn Skeleton 이 `bg-muted` 또는 명시적 배경색이 없으면 투명해서 애니메이션이 안 보임 (shadcn-ui/ui#5809 참조). 생성 템플릿은 항상 배경색 포함
- **Layout shift**: skeleton 과 실제 콘텐츠의 크기가 다르면 전환 시 깜빡. 정확한 width/height 매칭 필요
- **`<Suspense>` vs 조건 분기**: React Suspense 로 TanStack Query 를 래핑할 수도 있지만 기본 패턴은 **조건 분기** — suspense 는 옵션
- **Empty state 를 loading state 로 혼동**: 네트워크 성공인데 배열이 비었으면 loading 이 아니라 empty. `isPending === false && data.length === 0` 체크
- **반응형 skeleton**: 실제 레이아웃이 반응형이면 skeleton 도 동일 breakpoint 로 변환. `/react-responsive` 와 병용 가능
- **Strict TS**: `data` 의 `undefined` 체크 잊지 말 것 (`isPending === false` 라도 TanStack Query 타입상 `data` 는 `T | undefined`). TS 가 엄격히 강제

### 2.8 Clean Architecture 배치

- **Skeleton 컴포넌트**: 대상 컴포넌트와 **같은 파일 하단** 에 private 으로 정의 (예: `UserProfileCardSkeleton`)
- **여러 화면이 공유하는 skeleton**: `src/presentation/shared/components/skeletons/<name>-skeleton.tsx` 로 승격
- **shadcn Skeleton 원본**: `src/presentation/shared/components/ui/skeleton.tsx`

## 3. /react-extract — 재사용 컴포넌트 추출

feature 내부에 사유화된 위젯 (private component) 또는 여러 feature 에 중복된 유사 위젯을 `presentation/shared/components/` 로 추출하고 기존 import 경로를 자동 정리한다.

### 3.1 트리거

- 키워드: "위젯 추출", "공통으로 빼줘", "shared 로 이동", "extract widget", "중복 위젯 정리"
- 또는: **`widget-inspector-react` 에이전트 리포트 승인 후 자동 트리거**

### 3.2 widget-inspector-react 에이전트 연동

react-kit 은 에이전트 `widget-inspector-react` 를 제공. 이 에이전트는 주기적 또는 수동 실행으로 프로젝트 전체 컴포넌트를 스캔하여:

- **중복 위젯 감지**: 다른 feature 에 같은 이름/구조의 컴포넌트 발견
- **과도한 사유화 감지**: private 이지만 재사용 가능해 보이는 컴포넌트
- **복잡도 임계값 초과**: 컴포넌트 하나가 너무 커진 경우 (300줄+)
- 결과를 리포트로 사용자에게 제시

사용자가 리포트 중 일부를 "추출하자" 고 승인하면 `/react-extract` 가 자동 트리거되어 실제 이동 + import 정리 수행.

### 3.3 입력

- `source_path` (필수): 추출할 컴포넌트 현재 경로 (예: `src/presentation/features/auth/components/logo-banner.tsx`)
- `destination` (선택): 이동 경로 (기본: `src/presentation/shared/components/<kebab-name>.tsx`)
- `--dry-run`: 실제 파일 이동 없이 변경 내역만 보고

### 3.4 추출 흐름

1. **Import 참조 스캔**: 전체 프로젝트에서 대상 컴포넌트를 import 하는 파일 목록 수집 (TypeScript AST 또는 grep 기반)
2. **파일 이동**: `source_path` → `destination` 으로 물리 이동
3. **컴포넌트 이름 확인**: kebab-case 파일명 ↔ PascalCase 컴포넌트명 일관성 검증
4. **Props 타입 노출 확인**: 이동 대상이 `export type SomethingProps` 를 함께 export 하는지 (없으면 추가)
5. **Import 경로 일괄 수정**: 참조하는 모든 파일의 import 구문을 새 경로로 업데이트. `@/presentation/shared/components/...` 형태
6. **Unused import 정리**: 원본 feature 에 남아있던 import 중 안 쓰는 것 제거
7. **tsc --noEmit + eslint 검증**: 이동 후 타입 에러 / 린트 에러 없는지 확인. 에러가 생기면 **전체 롤백** 후 에러 보고
8. **결과 리포트**: 변경된 파일 수, 이동된 경로, 업데이트된 import 개수 요약

### 3.5 Import 경로 자동 업데이트 규칙

- **Before**: `import { LogoBanner } from './logo-banner'` (feature 내부 상대 경로)
- **After**: `import { LogoBanner } from '@/presentation/shared/components/logo-banner'` (absolute)

**규칙**:
- 항상 **absolute import** (`@/...`) 로 업데이트. 상대 경로 유지 금지
- **named export 만 지원**: `export default` 인 컴포넌트는 먼저 named export 로 리팩터 후 이동
- **Type-only import 는 `import type`** 으로 분리 (strict TS `verbatimModuleSyntax: true` 정책)
- 이동 후 원본 파일은 삭제. "re-export 남기기" 금지 (간접 경로 누적)

### 3.6 TypeScript AST 기반 안전 변환

단순 grep + sed 로는 "함수 내부 문자열에 같은 패턴" 이 있으면 오염될 수 있다. `/react-extract` 는 `ts-morph` 또는 TypeScript Compiler API 기반으로 AST 수준에서 import 노드를 식별하여 변환.

**최소 요구사항**:
- Import 경로 변환은 반드시 AST 노드 기반
- Rename 시 `export` / `import` / `type` 모두 일관 업데이트
- 순환 참조 감지 — 이동으로 새 순환이 생기면 경고 + 롤백

### 3.7 Gotchas

- **상대 경로 ↔ absolute 혼용**: 기존 코드가 상대 경로면 이동 후 경로 계산 실패. `/react-extract` 는 무조건 `@/...` 로 통일
- **default export 추출**: `export default function ...` 인 컴포넌트는 이름이 없어서 import 시 임의 이름 지정 가능 — 일관성 깨짐. named export 로 먼저 리팩터 권장
- **동일 이름 충돌**: 다른 feature 에도 `LogoBanner` 가 있으면 shared 로 이동 시 이름 충돌. 이 스킬은 더 구체적 이름으로 rename 을 제안 (예: `AuthLogoBanner`, `HeaderLogoBanner`)
- **테스트 파일 동반**: 이동 대상에 해당하는 `tests/component/LogoBanner.test.tsx` 가 있으면 테스트도 같이 이동하고 import 경로 업데이트
- **Storybook 이 있다면**: `.stories.tsx` 파일도 동반 이동
- **widget-inspector 리포트 신뢰하되 검증**: 에이전트 판단이 100% 정확하지 않을 수 있음. 사용자 승인 단계 필수
- **Strict TS 재검증**: 이동 후 `tsc --noEmit` 통과 실패 시 즉시 롤백. 부분 적용 상태 방치 금지

### 3.8 Clean Architecture 배치

- **이동 대상**: `src/presentation/features/**/*.tsx` → `src/presentation/shared/components/*.tsx`
- **추출 후 규칙**: 공용 위젯은 feature 를 몰라야 함. 특정 feature 의 domain 타입을 import 하면 그 자체로 "잘못 추출됨" 신호 — 추출 불가능, 혹은 Props generic 으로 느슨하게 분리 필요

## 4. 3개 스킬의 상호작용

```
[컴포넌트 작성] (G1 /react-widget, /react-screen)
         │
         ▼
/react-responsive    ←── breakpoint 또는 @container 쿼리 추가
         │
         ▼
/react-skeleton      ←── TanStack Query isPending 분기로 로딩 UI 삽입
         │
         ▼
widget-inspector-react 에이전트   ←── 주기 실행 또는 수동
         │
         ▼
/react-extract       ←── 에이전트 리포트 승인 후 사유화 컴포넌트 공용으로 이동
         │
         ▼
(/react-test 가 변경된 컴포넌트에 대해 테스트 재생성)
```

## 5. 공유 helpers 및 Cross-group 관계

- **G1 `/react-widget`**: cva + forwardRef 패턴은 G5 의 모든 스킬이 전제. 추출된 공용 컴포넌트도 같은 형식 유지
- **G2 `/react-query`**: `/react-skeleton` 이 `isPending/isError/empty` 분기의 기반으로 사용
- **G4 `/react-test`**: G5 변경 후 테스트 자동 갱신. 특히 skeleton 분기는 "loading state" 테스트 케이스 자동 추가
- **G6 `/react-audit`**: G5 출력물 감사 — 하드코딩된 breakpoint 값, Skeleton 없는 loading 경로, shared 로 승격되지 않은 중복 위젯 검출

## 6. 출처 요약

1. Tailwind v4 container queries (내장): https://tailwindcss.com/docs/hover-focus-and-other-states#container-queries
2. Tailwind v4.0 릴리스 노트: https://tailwindcss.com/blog/tailwindcss-v4
3. Tailwind v4 container 논의 (v4 에서 container plugin 통합): https://github.com/tailwindlabs/tailwindcss/discussions/14801
4. tailwindcss-container-queries (v3 플러그인, v4 에서는 불필요): https://github.com/tailwindlabs/tailwindcss-container-queries
5. shadcn/ui Skeleton 컴포넌트: https://ui.shadcn.com/docs/components/skeleton
6. shadcn Skeleton animate-pulse 이슈: https://github.com/shadcn-ui/ui/issues/5809
7. TanStack Query v5 useQuery 반환 (isPending, isError 등): https://tanstack.com/query/v5/docs/framework/react/reference/useQuery

## 7. 변경 이력

- **2026-04-10** — 초판. G5 3개 스킬 (`/react-responsive`, `/react-skeleton`, `/react-extract`) 상세 설계. WebSearch fallback 으로 Tailwind v4 container queries 내장 전환, shadcn Skeleton bg-muted 요구사항, TanStack Query isPending 상태 검증.
