# G5b — Animation (pure, no-library)

```yaml
last_updated: 2026-04-10
group: G5b
scope: react-kit 애니메이션 전용 설계 — 라이브러리 0개 원칙
skills: [/react-animation]
agents: [animation-architect-react]
depends_on: [G1 /react-widget, G5 /react-responsive, G5 /react-skeleton]
principle: "NO THIRD-PARTY ANIMATION LIBRARY"
banned_libraries:
  - motion (구 framer-motion)
  - framer-motion
  - react-spring
  - "@formkit/auto-animate"
  - "@dnd-kit/core / @dnd-kit/sortable"
  - react-dnd
  - gsap
  - lottie-react
  - animate.css (필요 시 Tailwind 로 직접 구현)
allowed_sources:
  - Tailwind v4 animate-* / transition-* utilities
  - tailwindcss-animate 플러그인 (shadcn 기본 페어)
  - CSS @keyframes 직접 선언
  - View Transitions API (네이티브 브라우저 API)
  - Pointer Events API (네이티브 브라우저 API)
  - requestAnimationFrame / Web Animations API (네이티브)
  - SVG + 직접 path 계산
research_sources:
  - MDN View Transition API (developer.mozilla.org/en-US/docs/Web/API/View_Transition_API)
  - MDN Pointer Events (developer.mozilla.org/en-US/docs/Web/API/Pointer_events)
  - MDN setPointerCapture (developer.mozilla.org/en-US/docs/Web/API/Element/setPointerCapture)
  - MDN touch-action (developer.mozilla.org/en-US/docs/Web/CSS/touch-action)
  - Chrome Developers View Transitions 2025 update
  - W3C ARIA Authoring Practices Guide
  - tailwindcss-animate (github.com/jamiebuilds/tailwindcss-animate)
  - 2026-04 WebSearch 검증 (View Transitions Baseline 2026-01 확정)
```

## 문서 목적

react-kit 의 애니메이션은 **외부 라이브러리를 일절 쓰지 않는다**. Motion / framer-motion / react-spring / dnd-kit / auto-animate 같은 대중적 선택지를 의도적으로 배제하고, **Tailwind CSS + 네이티브 브라우저 API + 커스텀 pointer event primitives** 만으로 모든 애니메이션 시나리오를 커버한다.

**왜 라이브러리 0개인가?**

1. **성능 우선**: react-kit 의 최상위 원칙. 번들 크기에 +50KB (Motion) 또는 +30KB (dnd-kit) 를 허용하지 않는다
2. **커스텀 최대화**: 라이브러리가 강제하는 API 와 추상화에 묶이지 않고, 요구사항에 정확히 맞는 구현만 생성
3. **브라우저 진화 활용**: 2026-01 기준 View Transitions API 가 Chrome/Safari/Firefox 144+ 에 Baseline 으로 안착. 과거에 라이브러리가 해결하던 문제를 네이티브가 더 빠르게 푼다
4. **디버깅 단순**: 스택 트레이스가 라이브러리 내부로 들어가지 않음. 모든 애니메이션 코드가 사용자 소유

**금지 라이브러리**: `motion`, `framer-motion`, `react-spring`, `@formkit/auto-animate`, `@dnd-kit/*`, `react-dnd`, `gsap`, `lottie-react`. 이들 패키지의 `import` 구문은 `/react-audit` 이 자동 검출 + 빌드 실패.

**허용**: Tailwind v4 + `tailwindcss-animate` (shadcn 기본 페어), CSS `@keyframes` 직접, View Transitions API, Pointer Events API, `requestAnimationFrame`, Web Animations API (`element.animate()`), SVG + 삼각함수 직접.

## 3-Tier 구조

애니메이션 요구는 **티어** 로 분류된다. 낮은 티어로 해결되는 건 높은 티어를 쓰지 않는다.

| Tier | 도구 | 적용 시나리오 | 구현 난이도 |
|------|------|--------------|----------|
| **T1** | Tailwind `animate-*` + `transition-*` + CSS `@keyframes` | 상태 변화 (fade/slide/scale/rotate/opacity), hover 효과, 단순 loop 애니메이션 | 낮음 |
| **T2** | View Transitions API (`document.startViewTransition` + `view-transition-name`) | 그리드 ↔ 보드 뷰 전환, shared element, 라우트 전환, DOM 구조 변경 시 부드러운 FLIP | 중 |
| **T3** | 커스텀 pointer primitives + FSM + requestAnimationFrame | 드래그앤드롭, 제스처, 드래그 momentum, SVG 연결선, 복잡 시퀀스 | 높음 |

`/react-animation` 스킬은 요청을 받으면 **자동으로 가장 낮은 티어부터 시도** — 라이브러리의 "무조건 Motion" 접근과 다르다.

## 1. Tier 1 — Tailwind + CSS

단순 상태 변화는 99% 이 단계에서 끝난다.

### 1.1 Tailwind 내장 유틸리티

| 카테고리 | 유틸 | 예시 |
|----------|------|------|
| **Transition** | `transition-all`, `transition-colors`, `transition-transform`, `transition-opacity` | `hover:scale-105 transition-transform duration-200` |
| **Duration** | `duration-75`~`duration-1000` | — |
| **Easing** | `ease-linear`, `ease-in`, `ease-out`, `ease-in-out` | — |
| **Animation (내장)** | `animate-spin`, `animate-ping`, `animate-pulse`, `animate-bounce` | 로딩, 알림, shimmer |
| **Delay** | `delay-75`~`delay-1000` | stagger 효과 |

### 1.2 tailwindcss-animate 플러그인 (shadcn 기본)

shadcn/ui 설치 시 함께 들어오는 `tailwindcss-animate` 가 추가 유틸리티 제공:
- `animate-in` / `animate-out` — enter/exit 애니메이션
- `fade-in-*`, `fade-out-*` — 페이드
- `slide-in-from-top/bottom/left/right-*`, `slide-out-to-*` — 슬라이드
- `zoom-in-*`, `zoom-out-*` — 스케일
- `spin-in-*` — 회전 진입
- `duration-*`, `ease-*` 와 조합 가능

**예시 — 드로어 열기/닫기**:

```tsx
<div
  data-state={open ? 'open' : 'closed'}
  className="
    data-[state=open]:animate-in data-[state=closed]:animate-out
    data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0
    data-[state=closed]:slide-out-to-left data-[state=open]:slide-in-from-left
    duration-300
  "
>
  드로어 내용
</div>
```

`data-[state=...]` 속성 선택자로 상태 기반 애니메이션. React 측은 state 를 `data-state` 속성으로 반영만 하면 끝.

### 1.3 CSS @keyframes 직접 선언

Tailwind 유틸로 커버 안 되는 custom 애니메이션은 Tailwind v4 의 `@theme` 블록 안에 `@keyframes` 정의:

```css
/* src/presentation/styles/globals.css */
@import "tailwindcss";

@theme {
  --animate-wiggle: wiggle 1s ease-in-out infinite;

  @keyframes wiggle {
    0%, 100% { transform: rotate(-3deg); }
    50%      { transform: rotate(3deg); }
  }
}
```

사용: `<div className="animate-wiggle">...</div>`

Tailwind v4 는 `@theme` 블록을 파싱해 `--animate-*` 변수 + `@keyframes` 를 자동 출력한다.

### 1.4 Tier 1 시나리오 예시

**Fade-in 진입**:

```tsx
<div className="animate-in fade-in-0 duration-500">
  페이지 로드 시 페이드 진입
</div>
```

**Hover scale**:

```tsx
<button className="transition-transform duration-200 hover:scale-105 active:scale-95">
  버튼
</button>
```

**스태거 리스트 진입**:

```tsx
{items.map((item, i) => (
  <div
    key={item.id}
    className="animate-in slide-in-from-bottom-4 fade-in-0"
    style={{ animationDelay: `${i * 50}ms`, animationFillMode: 'backwards' }}
  >
    {item.name}
  </div>
))}
```

### 1.5 Tier 1 Gotchas

- **`transition-*` 는 **변화하는 속성**에 걸 것**: `transition-all` 은 편하지만 예상 못 한 속성 전환으로 성능 저하. `transition-transform` / `transition-colors` 처럼 명시
- **`will-change` 남용 금지**: 성능을 위해 GPU 레이어로 올리는 힌트지만 남용하면 오히려 메모리 낭비. hover 시작 시 JS 로 동적 추가/제거가 더 정확
- **Reduced motion 존중**: `@media (prefers-reduced-motion: reduce)` 에서 애니메이션 disable. Tailwind 는 `motion-reduce:transition-none` 같은 variant 제공. `/react-audit` 이 reduced-motion 가드 누락 검출
- **data-state 변경은 React 렌더마다**: 너무 자주 바뀌면 애니메이션이 재시작. 상태 머신으로 전환 타이밍 제어

## 2. Tier 2 — View Transitions API

**2026-01 부터 Baseline** (Chrome/Safari/Firefox 144+). 같은 문서 SPA 내 DOM 변경 시 자동 FLIP 애니메이션. 라이브러리가 하던 "shared element transition" 을 네이티브로 해결.

### 2.1 기본 사용법

```ts
// src/presentation/shared/lib/view-transition.ts
export function withViewTransition(updateDOM: () => void): void {
  if (typeof document.startViewTransition !== 'function') {
    // Fallback: 구형 브라우저는 즉시 DOM 업데이트
    updateDOM()
    return
  }
  document.startViewTransition(updateDOM)
}
```

`document.startViewTransition(callback)` 이 핵심. callback 이 실행되기 전의 스냅샷과 이후 상태를 자동 보간.

### 2.2 `view-transition-name` CSS 로 공유 요소

DOM 구조가 바뀌어도 "같은 요소" 로 식별되어 부드럽게 이동:

```css
/* 카드가 어디에 있든 "user-avatar-{id}" 이름으로 연결 */
.user-avatar[data-user-id="123"] {
  view-transition-name: user-avatar-123;
}
```

또는 React 측에서 동적으로:

```tsx
<img
  src={user.avatarUrl}
  alt={user.name}
  className="h-10 w-10 rounded-full"
  style={{ viewTransitionName: `user-avatar-${user.id}` }}
/>
```

### 2.3 그리드 ↔ 보드 뷰 전환 (대표 시나리오)

```tsx
// src/presentation/features/tasks/components/task-switcher.tsx
import { withViewTransition } from '@/presentation/shared/lib/view-transition'
import { useTaskStore } from '../store'

export function TaskViewSwitcher() {
  const viewMode = useTaskStore((s) => s.viewMode)  // 'grid' | 'board'
  const setViewMode = useTaskStore((s) => s.setViewMode)

  return (
    <button
      onClick={() => {
        withViewTransition(() => {
          setViewMode(viewMode === 'grid' ? 'board' : 'grid')
        })
      }}
    >
      {viewMode === 'grid' ? '보드 뷰로' : '그리드 뷰로'}
    </button>
  )
}

// TaskList 컴포넌트 내부
export function TaskList({ tasks }: { tasks: Task[] }) {
  const viewMode = useTaskStore((s) => s.viewMode)
  return (
    <div className={viewMode === 'grid' ? 'grid grid-cols-3 gap-4' : 'flex gap-4 overflow-x-auto'}>
      {tasks.map((task) => (
        <div
          key={task.id}
          className="rounded-lg border p-4"
          style={{ viewTransitionName: `task-${task.id}` }}
        >
          {task.title}
        </div>
      ))}
    </div>
  )
}
```

**동작**: 사용자가 버튼을 클릭하면 `startViewTransition` 이 현재 그리드 레이아웃 스냅샷을 찍고, state 업데이트 후 새 보드 레이아웃을 찍은 뒤, `view-transition-name` 이 일치하는 각 task 카드를 FLIP 애니메이션으로 부드럽게 이동시킨다. 그리드→보드 전환이 "카드들이 날아다니는" 효과로 자동 표시.

### 2.4 CSS 로 전환 애니메이션 세부 조정

```css
/* 기본 전환 duration + easing 변경 */
::view-transition-group(*) {
  animation-duration: 0.4s;
  animation-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
}

/* 특정 요소만 다르게 */
::view-transition-group(user-avatar-123) {
  animation-duration: 0.6s;
}

/* 진입하는 요소 (old 없음, new 만 있음) */
::view-transition-new(root):only-child {
  animation: fade-in 0.3s ease-out;
}
```

### 2.5 2025~2026 신규 기능

- **`view-transition-class`** — 여러 요소를 하나의 클래스로 묶어 일괄 스타일링
- **`view-transition-name: match-element`** — 자동 네이밍 (같은 DOM 노드로 식별)
- **`:active-view-transition` / `:active-view-transition-type()`** pseudo-class — 전환 진행 중인 요소 선택
- **View transition types** — `document.startViewTransition({ update, types: ['slide-forward'] })` 로 CSS 가 타입별 분기

**2026-01 Baseline 이후 제약**: Firefox 의 초기 구현은 types 파라미터를 지원 안 함. 기본 전환만 쓰고 types 는 Chromium 계열에서만 사용 권장.

### 2.6 Firefox / Safari 구버전 Fallback

```ts
export function withViewTransition(
  updateDOM: () => void,
  options?: { types?: string[] },
): void {
  // Feature detection
  if (typeof document.startViewTransition !== 'function') {
    updateDOM()
    return
  }
  // types 미지원 브라우저 대응
  try {
    if (options?.types && options.types.length > 0) {
      document.startViewTransition({ update: updateDOM, types: options.types })
    } else {
      document.startViewTransition(updateDOM)
    }
  } catch {
    // 혹시 API 가 있어도 런타임 에러면 즉시 업데이트
    updateDOM()
  }
}
```

### 2.7 Tier 2 Gotchas

- **`view-transition-name` 은 고유해야 함**: 같은 이름을 가진 요소가 동시에 2개 이상이면 "duplicate name" 콘솔 에러. 동적 id 로 고유화
- **`contain: layout` 필요**: 복잡한 요소는 `contain: layout` CSS 를 추가해야 정확히 전환됨
- **scroll position 보존**: 전환 후 스크롤 위치가 의도치 않게 리셋될 수 있음. `scroll-behavior` 와 함께 조정
- **Firefox 144+ types 미지원**: 위 fallback 필수
- **Reduced motion**: `prefers-reduced-motion: reduce` 에서 startViewTransition 을 건너뛰는 로직 추가 권장

## 3. Tier 3 — 커스텀 Pointer Primitives

드래그앤드롭, 제스처, 복잡한 gesture-driven 애니메이션은 Pointer Events API + 상태 머신으로 직접 구현한다.

### 3.1 왜 Pointer Events 인가

- **단일 API 로 mouse/touch/pen 통합** — 각각 다른 이벤트 핸들러 필요 없음
- **`setPointerCapture`** — 요소 밖으로 포인터가 나가도 이벤트 계속 수신 (드래그 핵심)
- **`touch-action: none`** — 드래그 중 브라우저의 기본 스크롤/줌 동작 차단

### 3.2 useDrag 커스텀 훅

```tsx
// src/presentation/shared/hooks/use-drag.ts
import { useCallback, useReducer, useRef } from 'react'

// FSM 3 상태: idle / dragging / dropping
// - idle:      포인터 interaction 없음
// - dragging:  포인터 캡처 중, 위치 추적 중
// - dropping:  pointerup 발생 후, drop handler (async mutation) 실행 중
//              이 상태에서 UI 는 "드롭 중..." 피드백 + 원 위치 복원 애니메이션 가능
type DragState =
  | { kind: 'idle' }
  | { kind: 'dragging'; startX: number; startY: number; offsetX: number; offsetY: number; pointerId: number }
  | { kind: 'dropping'; offsetX: number; offsetY: number }

type DragAction =
  | { type: 'start'; x: number; y: number; pointerId: number }
  | { type: 'move'; x: number; y: number }
  | { type: 'drop' }       // pointerup on valid target → enter dropping
  | { type: 'resolved' }   // drop handler 완료 → return to idle
  | { type: 'cancel' }     // pointercancel, ESC, unmount → return to idle immediately

function dragReducer(state: DragState, action: DragAction): DragState {
  switch (action.type) {
    case 'start':
      return {
        kind: 'dragging',
        startX: action.x,
        startY: action.y,
        offsetX: 0,
        offsetY: 0,
        pointerId: action.pointerId,
      }
    case 'move':
      if (state.kind !== 'dragging') return state
      return {
        ...state,
        offsetX: action.x - state.startX,
        offsetY: action.y - state.startY,
      }
    case 'drop':
      if (state.kind !== 'dragging') return state
      return { kind: 'dropping', offsetX: state.offsetX, offsetY: state.offsetY }
    case 'resolved':
    case 'cancel':
      return { kind: 'idle' }
  }
}

type DragHandlers = {
  onPointerDown: (e: React.PointerEvent) => void
  onPointerMove: (e: React.PointerEvent) => void
  onPointerUp: (e: React.PointerEvent) => void
  onPointerCancel: (e: React.PointerEvent) => void
}

export function useDrag(): {
  state: DragState
  handlers: DragHandlers
  ref: React.RefObject<HTMLElement | null>
  resolve: () => void   // drop handler 완료 시 dropping → idle 전환
} {
  const [state, dispatch] = useReducer(dragReducer, { kind: 'idle' })
  const ref = useRef<HTMLElement | null>(null)

  const onPointerDown = useCallback((e: React.PointerEvent) => {
    e.currentTarget.setPointerCapture(e.pointerId)
    dispatch({ type: 'start', x: e.clientX, y: e.clientY, pointerId: e.pointerId })
  }, [])

  const onPointerMove = useCallback((e: React.PointerEvent) => {
    if (!e.currentTarget.hasPointerCapture(e.pointerId)) return
    dispatch({ type: 'move', x: e.clientX, y: e.clientY })
  }, [])

  const onPointerUp = useCallback((e: React.PointerEvent) => {
    if (e.currentTarget.hasPointerCapture(e.pointerId)) {
      e.currentTarget.releasePointerCapture(e.pointerId)
    }
    // dragging → dropping 전환 (async drop handler 실행 중)
    dispatch({ type: 'drop' })
  }, [])

  const onPointerCancel = useCallback((e: React.PointerEvent) => {
    if (e.currentTarget.hasPointerCapture(e.pointerId)) {
      e.currentTarget.releasePointerCapture(e.pointerId)
    }
    dispatch({ type: 'cancel' })
  }, [])

  // drop handler (async mutation) 가 완료되면 호출 → dropping 상태 해제
  const resolve = useCallback(() => {
    dispatch({ type: 'resolved' })
  }, [])

  return {
    state,
    handlers: { onPointerDown, onPointerMove, onPointerUp, onPointerCancel },
    ref,
    resolve,
  }
}
```

**사용**:

```tsx
export function DraggableCard() {
  const { state, handlers } = useDrag()
  const translate = state.kind === 'dragging'
    ? `translate(${state.offsetX}px, ${state.offsetY}px)`
    : 'none'

  return (
    <div
      {...handlers}
      className="touch-none rounded-lg border p-4 cursor-grab active:cursor-grabbing"
      style={{ transform: translate }}
    >
      드래그하세요
    </div>
  )
}
```

`touch-none` (Tailwind) = `touch-action: none` CSS 로 브라우저 기본 터치 동작 차단.

### 3.3 useDrop 커스텀 훅

드롭 타겟이 "지금 포인터가 내 위에 있는지" 를 알아야 하이라이트, validation, drop 처리가 가능하다. `useDrop` 훅은 Zustand drag store 와 연동되어 전역 drag state 를 구독한다.

```tsx
// src/presentation/shared/hooks/use-drop.ts
import { useCallback, useRef, useState } from 'react'
import { useDragStore } from '@/presentation/shared/stores/drag-store'

type DropHandlers = {
  onPointerEnter: (e: React.PointerEvent) => void
  onPointerLeave: (e: React.PointerEvent) => void
  onPointerUp: (e: React.PointerEvent) => void
}

type UseDropOptions<T> = {
  dropZoneId: string
  canAccept?: (active: { id: string; sourceColumnId: string }) => boolean
  onDrop: (active: { id: string; sourceColumnId: string }) => void
}

export function useDrop<T>(options: UseDropOptions<T>): {
  isOver: boolean
  canDrop: boolean
  handlers: DropHandlers
  ref: React.RefObject<HTMLElement | null>
} {
  const active = useDragStore((s) => s.active)
  const hoverColumnId = useDragStore((s) => s.hoverColumnId)
  const setHover = useDragStore((s) => s.hover)
  const endDrag = useDragStore((s) => s.end)
  const ref = useRef<HTMLElement | null>(null)

  const isOver = hoverColumnId === options.dropZoneId
  const canDrop = active !== null && (options.canAccept?.(active) ?? true)

  const onPointerEnter = useCallback(() => {
    if (active === null) return
    if (options.canAccept && !options.canAccept(active)) return
    setHover(options.dropZoneId)
  }, [active, options, setHover])

  const onPointerLeave = useCallback(() => {
    if (hoverColumnId === options.dropZoneId) setHover(null)
  }, [hoverColumnId, options.dropZoneId, setHover])

  const onPointerUp = useCallback(() => {
    if (active === null) return
    if (hoverColumnId !== options.dropZoneId) return
    if (options.canAccept && !options.canAccept(active)) return
    options.onDrop(active)
    endDrag()
  }, [active, hoverColumnId, options, endDrag])

  return {
    isOver,
    canDrop,
    handlers: { onPointerEnter, onPointerLeave, onPointerUp },
    ref,
  }
}
```

**사용**:

```tsx
export function Column({ columnId, items }: { columnId: string; items: Card[] }) {
  const { isOver, canDrop, handlers } = useDrop({
    dropZoneId: columnId,
    canAccept: (active) => active.sourceColumnId !== columnId,
    onDrop: (active) => moveCard(active.id, columnId),
  })

  return (
    <div
      {...handlers}
      className={`
        rounded-lg border p-4 min-h-64 transition-colors
        ${isOver && canDrop ? 'bg-primary/10 border-primary' : 'bg-background'}
      `}
    >
      {items.map((card) => <Card key={card.id} card={card} />)}
    </div>
  )
}
```

**핵심**:
- `useDrop` 은 **자체 pointer capture 를 하지 않는다** — 드래그 상태는 `useDrag` 쪽이 소유. `useDrop` 은 단지 "지금 내 영역에 들어왔는가" 만 판단
- `onPointerEnter` / `onPointerLeave` 는 pointer capture 상태에서도 target 을 가로채지 않고 정상 발화
- `canAccept` 로 validation — 같은 컬럼 내 드롭 금지, 타입 제한 등
- drop 성공 시 `options.onDrop` 호출 + Zustand drag store `end()` 로 전역 상태 리셋

### 3.4 useSortable — 정렬 가능 리스트

```ts
// src/presentation/shared/hooks/use-sortable.ts
// 핵심 아이디어: 드래그 중 각 아이템의 bounding rect 를 측정,
// 포인터 위치와 비교해서 목표 index 계산, 배열 재정렬 후 re-render

export function useSortable<T>(
  items: T[],
  getId: (item: T) => string,
  onReorder: (next: T[]) => void,
) {
  // ... dragReducer + itemsRef + pointer handlers
  // move 이벤트에서 clientY 로 target index 찾고
  // end 이벤트에서 onReorder(reordered) 호출
}
```

실전 구현은 200~300줄. 이 문서의 목적은 **패턴 명시** — 전체 구현은 `/react-animation` 스킬이 생성.

### 3.4 Pointer cancel 처리

드래그 중에 발생할 수 있는 cancel 시나리오:
- 브라우저 탭 전환 (`visibilitychange`)
- 다른 앱으로 포커스 전환
- ESC 키 (사용자가 명시적으로 취소)
- 요소가 unmount 됨
- 포인터가 "lost" 상태가 됨

각 경우 `pointercancel` 이벤트가 발생하거나, 수동으로 FSM 을 `idle` 로 리셋해야 한다:

```ts
useEffect(() => {
  function handleEscape(e: KeyboardEvent) {
    if (e.key === 'Escape') dispatch({ type: 'cancel' })
  }
  window.addEventListener('keydown', handleEscape)
  return () => window.removeEventListener('keydown', handleEscape)
}, [])
```

### 3.5 Zustand 전역 drag state

여러 컴포넌트에 걸친 드래그 (예: 칸반 보드의 카드가 컬럼 A 에서 컬럼 B 로) 는 훅 로컬 state 로는 부족. Zustand store 에 승격:

```ts
// src/presentation/shared/stores/drag-store.ts
import { create } from 'zustand'

type DragStore = {
  active: { id: string; sourceColumnId: string } | null
  hoverColumnId: string | null
  start: (id: string, sourceColumnId: string) => void
  hover: (columnId: string | null) => void
  end: () => void
}

export const useDragStore = create<DragStore>()((set) => ({
  active: null,
  hoverColumnId: null,
  start: (id, sourceColumnId) => set({ active: { id, sourceColumnId }, hoverColumnId: null }),
  hover: (columnId) => set({ hoverColumnId: columnId }),
  end: () => set({ active: null, hoverColumnId: null }),
}))
```

G2 `/react-store` 원칙 그대로 — 외부 접근 가능 (`useDragStore.getState()`), 훅 외부에서도 setState 가능.

### 3.6 SVG 화살표 / 연결선

**핵심**: 두 DOM 요소의 `getBoundingClientRect()` 로 좌표 계산 → SVG `<path d="M x1 y1 L x2 y2" />` 또는 베지어 곡선.

```tsx
// src/presentation/shared/components/connector.tsx
import { useEffect, useState } from 'react'

type Point = { x: number; y: number }

export function Connector({
  fromRef,
  toRef,
}: {
  fromRef: React.RefObject<HTMLElement | null>
  toRef: React.RefObject<HTMLElement | null>
}) {
  const [from, setFrom] = useState<Point | null>(null)
  const [to, setTo] = useState<Point | null>(null)

  useEffect(() => {
    function update() {
      const a = fromRef.current?.getBoundingClientRect()
      const b = toRef.current?.getBoundingClientRect()
      if (!a || !b) return
      setFrom({ x: a.right, y: a.top + a.height / 2 })
      setTo({ x: b.left, y: b.top + b.height / 2 })
    }
    update()
    // 요소 크기/스크롤 변화 추적
    const observer = new ResizeObserver(update)
    if (fromRef.current) observer.observe(fromRef.current)
    if (toRef.current) observer.observe(toRef.current)
    window.addEventListener('scroll', update, { capture: true })
    window.addEventListener('resize', update)
    return () => {
      observer.disconnect()
      window.removeEventListener('scroll', update, { capture: true })
      window.removeEventListener('resize', update)
    }
  }, [fromRef, toRef])

  if (!from || !to) return null

  // 베지어 곡선 control point
  const midX = (from.x + to.x) / 2
  const d = `M ${from.x} ${from.y} C ${midX} ${from.y}, ${midX} ${to.y}, ${to.x} ${to.y}`

  return (
    <svg className="pointer-events-none fixed inset-0 h-full w-full">
      <path d={d} stroke="currentColor" strokeWidth="2" fill="none" />
      <circle cx={to.x} cy={to.y} r="4" fill="currentColor" />
    </svg>
  )
}
```

`pointer-events-none` 으로 SVG 가 마우스 이벤트를 차단하지 않게. `fixed inset-0` 로 전체 뷰포트 overlay.

## 4. 복잡 시나리오 통합 예시

### 4.1 그리드 ↔ 보드 뷰 전환

§2.3 에서 제시. Tier 2 (View Transitions API) 로 해결. 추가 라이브러리 0.

### 4.2 칸반 드래그앤드롭

Tier 3 의 `useDrag` + `useDrop` + Zustand `useDragStore` 를 조립한 전체 예시. 라이브러리 0개.

```tsx
// src/presentation/features/kanban/components/kanban-board.tsx
import { useDrag } from '@/presentation/shared/hooks/use-drag'
import { useDrop } from '@/presentation/shared/hooks/use-drop'
import { useDragStore } from '@/presentation/shared/stores/drag-store'
import { useMoveCard } from '../hooks/use-move-card'

type Card = { id: string; title: string; columnId: string }
type Column = { id: string; title: string }

type KanbanBoardProps = {
  columns: Column[]
  cards: Card[]
}

export function KanbanBoard({ columns, cards }: KanbanBoardProps) {
  return (
    <div className="flex gap-4 overflow-x-auto p-4">
      {columns.map((column) => (
        <KanbanColumn
          key={column.id}
          column={column}
          cards={cards.filter((c) => c.columnId === column.id)}
        />
      ))}
    </div>
  )
}

function KanbanColumn({ column, cards }: { column: Column; cards: Card[] }) {
  const moveCardMutation = useMoveCard()  // G2 /react-query useMutation
  const { isOver, canDrop, handlers } = useDrop({
    dropZoneId: column.id,
    canAccept: (active) => active.sourceColumnId !== column.id,
    onDrop: (active) => {
      moveCardMutation.mutate({ cardId: active.id, targetColumnId: column.id })
    },
  })

  return (
    <div
      {...handlers}
      className={`
        flex w-72 flex-col gap-2 rounded-lg border p-3 transition-colors
        ${isOver && canDrop ? 'border-primary bg-primary/10' : 'border-border bg-muted/30'}
      `}
    >
      <h3 className="font-semibold">{column.title}</h3>
      {cards.map((card) => (
        <KanbanCard key={card.id} card={card} />
      ))}
    </div>
  )
}

function KanbanCard({ card }: { card: Card }) {
  const startDrag = useDragStore((s) => s.start)
  const endDrag = useDragStore((s) => s.end)
  const { state, handlers: dragHandlers, resolve } = useDrag()

  const onPointerDown = (e: React.PointerEvent) => {
    dragHandlers.onPointerDown(e)
    startDrag(card.id, card.columnId)
  }

  const onPointerUp = (e: React.PointerEvent) => {
    dragHandlers.onPointerUp(e)  // dragging → dropping
    endDrag()                    // Zustand store 리셋 (useDrop.onDrop 이 mutation 호출)
    // 실제 앱에서는 mutation.onSuccess 콜백에서 resolve() 호출하여
    // dropping 상태를 유지한 채 async 작업이 끝난 뒤 idle 로 전환.
    // 최소 데모는 즉시 resolve:
    resolve()
  }

  const translate =
    state.kind === 'dragging' || state.kind === 'dropping'
      ? `translate(${state.offsetX}px, ${state.offsetY}px)`
      : 'none'
  const isDragging = state.kind === 'dragging'
  const isDropping = state.kind === 'dropping'

  return (
    <div
      onPointerDown={onPointerDown}
      onPointerMove={dragHandlers.onPointerMove}
      onPointerUp={onPointerUp}
      onPointerCancel={(e) => { dragHandlers.onPointerCancel(e); endDrag() }}
      className={`
        touch-none rounded border bg-card p-3 cursor-grab
        ${isDragging ? 'opacity-50 shadow-lg cursor-grabbing z-10 relative' : ''}
        ${isDropping ? 'opacity-70 pointer-events-none' : ''}
      `}
      style={{ transform: translate }}
    >
      {card.title}
    </div>
  )
}
```

**동작 흐름**:
1. 사용자가 카드를 pointerdown → `useDrag` 이 로컬 FSM 에 dragging 등록 + `useDragStore.start(cardId, sourceColumnId)` 로 전역 등록
2. pointermove → 카드 transform 업데이트 (로컬), 각 컬럼의 `useDrop` 이 pointerenter 로 `useDragStore.hover(columnId)` 호출, 해당 컬럼만 isOver 로 하이라이트
3. pointerup 이 드롭 타겟 컬럼 위에서 발생 → `useDrop.onDrop` 콜백이 mutation 호출 (`useMoveCard` = G2 `/react-query` mutation), `useDragStore.end()` 로 전역 리셋
4. mutation onSuccess → queryClient.invalidateQueries(['cards']) 로 서버 상태 재조회, UI 자동 반영 (G2 패턴)

**라이브러리**: 0개. `useDrag`, `useDrop`, `useDragStore` 는 react-kit 이 스캐폴딩한 커스텀 hook/store. 접근성은 §5 경고 참조.

### 4.3 SVG 화살표로 노드 연결 (플로우차트)

§3.6 의 `Connector` 컴포넌트 재사용. 노드 위치는 Zustand 로 관리, 연결선은 ref 기반으로 동적 계산. React Flow 같은 라이브러리 없음.

## 5. 접근성 경고 (⚠ 트레이드오프)

**라이브러리 0개 접근의 가장 큰 약점**: 드래그앤드롭의 키보드 / ARIA / 스크린리더 접근성이 사용자 책임이다.

`@dnd-kit` 같은 라이브러리는 기본적으로:
- Tab 으로 포커스, Space/Enter 로 pickup
- 화살표 키로 이동
- Space/Enter 로 drop, Esc 로 cancel
- `aria-live` 영역에 상태 방송 ("Item moved to position 3")
- Screen reader 에 각 단계 설명 전달

react-kit 은 이걸 **자동 제공하지 않는다**. 대신 W3C ARIA Authoring Practices Guide (APG) 의 패턴을 따라 사용자가 직접 구현할 수 있도록 **패턴 템플릿 + 문서** 를 제공한다.

### 최소 구현 체크리스트 (`/react-animation` 스킬이 스캐폴딩)

- [ ] 드래그 가능한 요소에 `tabIndex={0}` + `role="button"` (또는 `role="listitem"`)
- [ ] `aria-grabbed` 는 deprecated — 대신 `aria-describedby` 로 상태 안내
- [ ] Space/Enter 로 pickup, 화살표 키로 이동, Esc 로 cancel 구현
- [ ] `aria-live="polite"` 영역에 "아이템 이동 중", "완료" 메시지 업데이트
- [ ] `prefers-reduced-motion` 대응 — 애니메이션 없이 즉시 이동
- [ ] 포커스 관리 — drop 후 포커스가 새 위치의 아이템에 머무르도록

### 출처

- W3C ARIA Authoring Practices Guide (APG): https://www.w3.org/WAI/ARIA/apg/
- W3C Keyboard Interface 가이드: https://www.w3.org/WAI/ARIA/apg/practices/keyboard-interface/
- MDN WAI-ARIA basics: https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Accessibility/WAI-ARIA_basics

**솔직한 경고**: 완전한 스크린리더 접근성을 원하면 `@dnd-kit` 같은 라이브러리가 더 빠르게 문제를 푼다. react-kit 의 "no-library" 선택은 **번들 / 커스텀 / 성능** 을 얻는 대신 **접근성 구현 책임** 을 사용자가 진다는 트레이드오프다. 이 문서는 패턴을 제공하지만 완벽한 a11y 를 보장하지 않는다.

## 6. /react-animation 스킬 자동 티어 판정

사용자 요청을 분석해 가장 낮은 티어로 해결 가능한 방안을 선택:

```
/react-animation "버튼 hover 시 살짝 커지게"
  → 분석: 단순 scale 변화, 단일 요소, 상태 없음
  → T1 (Tailwind): hover:scale-105 transition-transform duration-200
  → 코드 삽입 + 끝

/react-animation "카드 클릭 시 상세 페이지로 shared element 전환"
  → 분석: DOM 구조 변경, shared element, 라우트 전환
  → T2 (View Transitions): view-transition-name 설정 + startViewTransition 래핑
  → withViewTransition 호출부 자동 삽입

/react-animation "칸반 보드 드래그앤드롭"
  → 분석: 포인터 기반 드래그, 여러 컬럼, 상태 관리 필요
  → T3 (Pointer primitives): useDrag + useSortable + useDragStore 스캐폴딩
  → 접근성 경고 + W3C APG 패턴 안내

/react-animation "노드 간 화살표 연결"
  → 분석: 두 요소의 좌표 기반, ResizeObserver 필요
  → T3 (SVG): Connector 컴포넌트 생성
```

**판정 규칙**:
- 상태 변화 / transition 키워드 → T1
- "shared element", "뷰 전환", "라우트 전환", "DOM 구조 변경" 키워드 → T2
- "드래그", "드롭", "정렬", "gesture", "화살표", "연결선", "커스텀 제어" 키워드 → T3

## 7. 아키텍처 배치

- **Tier 1 스타일**: `src/presentation/styles/globals.css` (@theme @keyframes), 컴포넌트 내 Tailwind 클래스
- **Tier 2 유틸**: `src/presentation/shared/lib/view-transition.ts`
- **Tier 3 훅**: `src/presentation/shared/hooks/use-drag.ts`, `use-drop.ts`, `use-sortable.ts`
- **Tier 3 컴포넌트**: `src/presentation/shared/components/connector.tsx`, `draggable-item.tsx`
- **전역 drag state**: `src/presentation/shared/stores/drag-store.ts` (Zustand)
- **절대 금지**: `domain/`, `data/` 에 pointer event / view transition / Zustand drag store import. 애니메이션은 presentation 전용.

## 8. animation-architect-react 에이전트

### 8.1 역할

복잡한 애니메이션 요구를 받아 **설계 자문** 을 제공하는 읽기 전용 에이전트. 코드를 직접 작성하지 않고, 사용자에게 다음을 제시:

- 가능한 구현 전략 (어느 티어로 접근할지)
- 각 전략의 트레이드오프 (성능, 접근성, 복잡도)
- 잠재 엣지케이스 (pointer cancel, reduced motion, feature detection)
- 권장 구현 순서 (단계별 마일스톤)

그 뒤 사용자가 "이 전략으로 구현해줘" 로 승인하면 `/react-animation` 스킬이 실제 파일을 생성한다.

### 8.2 트리거 조건

- 사용자가 "애니메이션 어떻게 하지", "이거 어떻게 구현할까", "드래그앤드롭 설계 봐줘" 같은 **자문 요청**
- `/react-animation` 스킬이 요청을 분석했지만 **티어가 애매한 경우** (T2 / T3 경계)
- 여러 feature 에 걸친 **복잡한 gesture 설계** — 단일 스킬 실행으로 해결 불가

### 8.3 도구 스코프

**읽기 전용**:
- `Read` — 기존 코드 확인
- `Grep` — 패턴 검색
- `Glob` — 파일 찾기

**쓰기 권한 없음**: 에이전트는 조언만. 실제 구현은 메인 Claude 또는 `/react-animation` 스킬이 담당.

### 8.4 출력 포맷

```markdown
## 자문 요약
대상: {사용자 요청}

## 권장 전략
- **1순위**: Tier {N} — {이유}
- **2순위 (fallback)**: Tier {M} — {언제}

## 구현 단계
1. {단계 1}
2. {단계 2}
...

## 엣지케이스
- {pointer cancel 처리}
- {reduced motion}
- {브라우저 호환}

## 잠재 접근성 이슈
- {키보드 대응 필요}
- {ARIA 라이브 영역}
```

### 8.5 에이전트 ↔ 스킬 흐름

```
사용자 요청
     │
     ▼
animation-architect-react  (분석 + 자문)
     │
     ▼
사용자 승인
     │
     ▼
/react-animation  (스캐폴딩 + 코드 생성)
     │
     ▼
/react-test       (자동 테스트 생성)
     │
     ▼
/react-audit      (접근성 + no-library 정책 검증)
```

## 9. 다른 그룹과의 관계

- **G1 `/react-widget`**: cva / forwardRef 구조를 그대로 확장. 애니메이션 훅은 shared/hooks/, 컴포넌트는 shared/components/
- **G2 `/react-store`**: 전역 drag state 는 Zustand store. 서버 상태 (TanStack Query) 와 섞이지 않음
- **G4 `/react-test`**: pointer event 테스트는 `@testing-library/user-event` 의 `user.pointer()` API 사용. Vitest + jsdom 환경에서 동작
- **G5 `/react-responsive`**: 애니메이션도 breakpoint 별 분기 가능 (`md:animate-in lg:slide-in-from-right`)
- **G5 `/react-skeleton`**: 로딩 → 완료 전환은 Tier 1 `fade-in` 또는 Tier 2 `startViewTransition` 으로 자연스럽게
- **G6 `/react-audit`**: 금지 라이브러리 import 검출 (`motion`, `dnd-kit` 등), reduced-motion 가드 누락 검출, `view-transition-name` 중복 검출

## 10. 안티패턴 감사 규칙

`/react-audit` 이 검출해야 하는 G5b 관련 안티패턴:

- **금지 라이브러리 import**: `^import .* from ['"](motion|framer-motion|react-spring|@dnd-kit/.*|@formkit/auto-animate.*|react-dnd.*|gsap|lottie-react)['"]` 정규식 매칭 → 빌드 실패
- **`view-transition-name` 중복**: 같은 이름이 여러 요소에 동시 할당 → 경고
- **`touch-action` 누락된 드래그**: pointer event 핸들러가 있는 요소에 `touch-action` CSS 가 없음 → 경고
- **`setPointerCapture` 누락**: `onPointerMove` 핸들러가 있는데 `onPointerDown` 에서 캡처 안 함 → 경고
- **reduced-motion 가드 없음**: 애니메이션이 있는데 `@media (prefers-reduced-motion: reduce)` 또는 `motion-reduce:*` 가 없음 → 경고
- **Error Boundary 없는 최상위 `Connector`**: SVG 좌표 계산 중 에러 발생 가능 → 경고

## 11. 출처 요약

1. MDN View Transition API: https://developer.mozilla.org/en-US/docs/Web/API/View_Transition_API
2. MDN Document.startViewTransition(): https://developer.mozilla.org/en-US/docs/Web/API/Document/startViewTransition
3. MDN ViewTransition interface: https://developer.mozilla.org/en-US/docs/Web/API/ViewTransition
4. MDN view-transition-name CSS: https://developer.mozilla.org/en-US/docs/Web/CSS/view-transition-name
5. MDN :active-view-transition pseudo-class: https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Selectors/:active-view-transition
6. MDN :active-view-transition-type() pseudo-class: https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Selectors/:active-view-transition-type
7. Chrome Developers — View Transitions 2025 update: https://developer.chrome.com/blog/view-transitions-in-2025
8. MDN Pointer events: https://developer.mozilla.org/en-US/docs/Web/API/Pointer_events
9. MDN Element.setPointerCapture(): https://developer.mozilla.org/en-US/docs/Web/API/Element/setPointerCapture
10. MDN touch-action CSS: https://developer.mozilla.org/en-US/docs/Web/CSS/touch-action
11. W3C Pointer Events Level 3: https://www.w3.org/TR/pointerevents3/
12. W3C ARIA Authoring Practices Guide: https://www.w3.org/WAI/ARIA/apg/
13. W3C Keyboard Interface 가이드: https://www.w3.org/WAI/ARIA/apg/practices/keyboard-interface/
14. Tailwind CSS Animation utilities: https://tailwindcss.com/docs/animation
15. tailwindcss-animate 플러그인: https://github.com/jamiebuilds/tailwindcss-animate

## 12. 변경 이력

- **2026-04-10** — 초판. `/react-animation` 스킬 + `animation-architect-react` 에이전트 상세 설계. 라이브러리 0개 원칙 선언 (Motion/dnd-kit/react-spring 등 전면 금지). Tier 1 (Tailwind), Tier 2 (View Transitions API, 2026-01 Baseline), Tier 3 (Pointer Events + FSM + SVG) 3단 구조. 복잡 시나리오 3종 (그리드↔보드 / 칸반 DnD / SVG 화살표). 접근성 트레이드오프 명시 경고. Codex 리서치 3차 시도 연속 정체로 WebSearch fallback 사용 (MDN View Transitions / Pointer Events, Chrome Developers 2025 update, W3C APG, tailwindcss-animate 검증).
