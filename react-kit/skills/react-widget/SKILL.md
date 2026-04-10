---
name: react-widget
description: >
  shadcn/ui 컴포넌트를 기반으로 cva variant + Container Queries를 갖춘 재사용 UI 컴포넌트를 생성한다.
  "위젯 만들어줘", "컴포넌트 생성", "shadcn 컴포넌트", "react widget", "custom component" 같은 요청 시 트리거.
  새 프로젝트 초기화가 필요하면 트리거하지 않는다 — /react-init 사용.
  feature 4계층 전체 생성이 필요하면 트리거하지 않는다 — /react-feature 사용.
argument-hint: "<WidgetName> [--base=<shadcn-component>] [--variants=<list>]"
user-invocable: true
---

# Gotchas

1. **기존 shadcn 컴포넌트 직접 수정 금지** — shadcn은 "코드 소유" 모델이라 수정이 가능하지만, `/react-widget`은 래핑해서 확장한다. 직접 수정은 shadcn CLI 업데이트 시 충돌.
2. **`cn` 유틸리티 경로 고정** — `@/presentation/shared/lib/utils`의 `cn(...)`을 import한다. `@/lib/utils` 같은 다른 경로 사용 금지 (Clean Arch 준수).
3. **`React.FC` 금지** — 제네릭 추론이 약하고 children이 암묵적으로 포함된다. 대신 `(props: Props) => JSX.Element` 또는 `forwardRef<Ref, Props>` 사용.
4. **Props 타입은 `type`으로 정의** — `interface` 아님. `VariantProps` 같은 유틸리티 타입과 교차 타입으로 조합하기 위함.
5. **`displayName` 필수** — `forwardRef` 컴포넌트는 `displayName` 설정 필수. React DevTools 디버깅 용이성.
6. **`onClick` 재정의 금지** — HTML 속성에 이미 `onClick`이 있으므로 Props 타입에서 덮어쓰면 타입 충돌. 필요하면 명시적으로 다시 선언.
7. **Container Queries는 Tailwind v4 전용** — `@container` + `@md:` 유틸리티는 Tailwind v4 이상에서 내장. v3에서는 별도 플러그인 필요하므로 프로젝트 Tailwind 버전 확인 후 사용.
8. **Strict TS 통과 필수** — `tsc --noEmit`과 `eslint --max-warnings=0`을 통과해야 한다. cva 반환 타입을 `any`로 캐스팅하는 코드 생성 금지.
9. **기존 파일 overwrite 금지** — 같은 경로 파일이 이미 존재하면 거부한다. `--force` 플래그가 있을 때만 덮어쓴다.
10. **실패 시 전체 롤백** — 복수 파일 생성 중 하나라도 실패 시 스킬 실행으로 생성된 파일을 모두 삭제하고 원상복구한다.
11. **`export default` 금지** — named export로 통일한다 (Clean Arch 규칙).

# Process

## 1. 프로젝트 환경 감지

`references/project-detection.md` 절차를 실행한다. 다음을 확인한다:
- `components.json` 존재 여부 (shadcn 초기화 확인). 없으면 `pnpm dlx shadcn@latest init --template vite` 먼저 실행하도록 안내.
- Tailwind 메이저 버전 (Container Queries 내장 여부)
- `src/presentation/shared/lib/utils.ts`의 `cn` 헬퍼 존재 여부

## 2. 입력 수집

- `widget_name` (필수): PascalCase (예: `PrimaryButton`, `MetricCard`)
- `--base` (선택): 기반 shadcn 컴포넌트 (예: `button`, `card`). 없으면 순수 컴포넌트 생성.
- `--variants` (선택): variant 정의 (예: `variant:default,destructive size:sm,md,lg`)

컴포넌트 파일명은 widget_name을 kebab-case로 변환: `PrimaryButton` → `primary-button.tsx`.

## 3. 중복 확인

`src/presentation/shared/components/<kebab-name>.tsx`가 이미 존재하면 `--force` 없이 거부한다.

## 4. base shadcn 컴포넌트 확인 (`--base` 지정 시)

`src/presentation/shared/components/ui/<base>.tsx`가 존재하는지 확인한다. 없으면:

```bash
pnpm dlx shadcn@latest add <base>
```

## 5. 컴포넌트 생성

### variant 있는 경우 (cva 패턴)

`src/presentation/shared/components/<kebab-name>.tsx`:

```tsx
import * as React from 'react'
import { cva, type VariantProps } from 'class-variance-authority'
import { cn } from '@/presentation/shared/lib/utils'

const <widgetName>Variants = cva(
  // base classes
  'inline-flex items-center justify-center rounded-md font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 disabled:opacity-50 disabled:pointer-events-none',
  {
    variants: {
      variant: {
        default: 'bg-primary text-primary-foreground hover:bg-primary/90',
        // TODO: --variants 정의에 따라 추가
      },
      size: {
        sm: 'h-8 px-3 text-sm',
        md: 'h-10 px-4',
        lg: 'h-12 px-6 text-lg',
      },
    },
    defaultVariants: {
      variant: 'default',
      size: 'md',
    },
  },
)

type <WidgetName>Props = React.HTMLAttributes<HTMLDivElement> &
  VariantProps<typeof <widgetName>Variants>

export const <WidgetName> = React.forwardRef<<HTMLDivElement>, <WidgetName>Props>(
  ({ className, variant, size, ...props }, ref) => (
    <div
      ref={ref}
      className={cn(<widgetName>Variants({ variant, size }), className)}
      {...props}
    />
  ),
)
<WidgetName>.displayName = '<WidgetName>'
```

base가 `button`이면 `HTMLDivElement` → `HTMLButtonElement`, `HTMLAttributes` → `ButtonHTMLAttributes`로 교체한다.

### variant 없는 경우 (단순 컴포넌트)

```tsx
import * as React from 'react'
import { cn } from '@/presentation/shared/lib/utils'

type <WidgetName>Props = React.HTMLAttributes<HTMLDivElement> & {
  // TODO: 필요한 props 추가
}

export const <WidgetName> = React.forwardRef<<HTMLDivElement>, <WidgetName>Props>(
  ({ className, ...props }, ref) => (
    <div
      ref={ref}
      className={cn('', className)}
      {...props}
    />
  ),
)
<WidgetName>.displayName = '<WidgetName>'
```

### 반응형 레이아웃이 필요한 경우 (Container Queries)

Tailwind v4 감지 시 `@container` 패턴을 적용한다:

```tsx
<div className="@container">
  <div className="grid grid-cols-1 @md:grid-cols-2 @lg:grid-cols-3">
    {/* 컨테이너 크기 기준 반응형 — 뷰포트 breakpoint 아님 */}
  </div>
</div>
```

v3 감지 시 `@tailwindcss/container-queries` 플러그인 설치 필요 여부를 사용자에게 안내한다.

## 6. Strict TS 검증

```bash
pnpm tsc --noEmit
pnpm eslint src/presentation/shared/components/<kebab-name>.tsx --max-warnings=0
```

오류가 있으면 수정 후 재확인한다.

## 7. 완료 후 안내

생성 파일: `src/presentation/shared/components/<kebab-name>.tsx`

다음 단계:
- 이 컴포넌트를 특정 화면에 배치: `/react-screen`
- 기능 레이어 연동: `/react-feature`
- 스켈레톤 로딩 추가: `/react-skeleton`

# References

- `references/project-detection.md` — 프로젝트 감지 (Tailwind 버전, shadcn 초기화 여부)
- `references/clean-arch-layout.md` — 공용 컴포넌트 배치 (`presentation/shared/components/`, shadcn 원본은 `ui/` 하위)
- `references/result-patterns.md` — 컴포넌트에서 Result 패턴 활용 시
- `docs/react/kit-design/g1-scaffolding.md` §4 — 이 스킬의 상세 설계
