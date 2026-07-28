---
name: react-animation
description: >
  React 컴포넌트에 애니메이션을 추가한다. 외부 라이브러리 없이
  Tailwind+CSS(Tier 1) / View Transitions API(Tier 2) / 커스텀 Pointer Primitives(Tier 3)
  3단 구조로 구현한다.
  "애니메이션 추가", "애니메이션 구현", "드래그 앤 드롭", "정렬 리스트",
  "view transition", "page transition 애니메이션", "shared element",
  "fade in", "slide up", "드래그", "드롭", "sortable", "칸반", "kanban",
  "hover 효과", "페이지 전환" 같은 요청 시 트리거.
argument-hint: "<target_path|scenario> [--tier=1|2|3]"
user-invocable: true
---

# Gotchas

1. **라이브러리 0개 원칙 — 절대 예외 없음**: Motion(framer-motion) / dnd-kit / react-spring / react-transition-group / @formkit/auto-animate / react-dnd / gsap / lottie-react / react-beautiful-dnd / animate.css 는 **설치 및 import 금지**. 이들의 import 구문이 코드베이스에 존재하면 `/react-audit` 이 빌드 실패를 발행한다. 사용자가 요청하더라도 대안 구현을 제시하고 라이브러리 사용을 거부한다.

2. **가장 낮은 Tier부터 시도**: "animation" 요청을 받으면 무조건 Tier 3부터 쓰는 실수가 잦다. 판정 규칙을 따라 Tier 1로 해결 가능한지 먼저 확인하고, 불가능할 때만 더 높은 Tier로 올라간다.

3. **`tailwindcss-animate` 플러그인 확인**: `animate-in`, `fade-in-*`, `slide-in-from-*` 같은 확장 유틸리티는 `tailwindcss-animate` 가 있어야 동작한다. shadcn 설치 프로젝트에는 기본 포함되지만, 없으면 `pnpm add -D tailwindcss-animate` 후 `tailwind.config.ts` 에 플러그인 등록을 안내한다.

4. **`view-transition-name` 고유성**: 같은 이름을 두 요소가 동시에 가지면 "duplicate name" 오류가 발생한다. 반드시 동적 id (`view-transition-name: task-${item.id}`)를 사용해 고유성을 보장한다.

5. **Pointer cancel 처리 필수**: `pointercancel` 이벤트를 처리하지 않으면 탭 전환, 다른 앱 포커스, 요소 unmount 시 드래그 상태가 leak된다. `onPointerCancel` 핸들러에서 반드시 FSM을 `idle`로 리셋한다.

6. **`touch-action: none` 빠뜨리면 모바일 드래그 불가**: pointer event 기반 드래그 요소에 Tailwind `touch-none` 클래스를 반드시 추가해야 브라우저 기본 스크롤/줌이 차단된다.

7. **Zustand drag store는 전역 단일 인스턴스**: feature마다 별도 drag store를 만들지 않는다. `src/presentation/shared/stores/drag-store.ts` 하나를 모든 feature가 공유한다.

8. **`prefers-reduced-motion` 미적용**: 모든 Tier에서 `@media (prefers-reduced-motion: reduce)` 또는 Tailwind `motion-reduce:*` variant로 애니메이션을 비활성화해야 한다. `/react-audit` 이 누락 시 경고를 발행한다.

9. **애니메이션은 presentation 전용**: `domain/`, `data/` 레이어에 pointer event / view transition / Zustand drag store를 import하지 않는다. 애니메이션 관련 코드는 `src/presentation/` 에만 위치한다.

10. **Firefox types 파라미터 미지원**: `document.startViewTransition({ update, types: [...] })` 의 `types` 옵션은 2026년 기준 Chromium 계열에서만 안정적으로 지원된다. `withViewTransition` 래퍼에서 try/catch로 fallback을 처리한다.

11. **scroll-driven animation 브라우저 지원 확인**: `animation-timeline: scroll()` / `view()` 는 Chrome 안정이지만 Firefox 는 2026-Q2 기준 플래그 필요. 브라우저 지원 범위가 충분하지 않으면 `@supports (animation-timeline: scroll())` 로 감싸고, 미지원 시 정적 스타일로 fallback 한다.

12. **`view-transition-name: match-element` 활용 (Chrome 137+)**: 수십 개 요소에 수동으로 고유 이름을 부여하는 대신 `view-transition-name: match-element` CSS 값을 사용하면 브라우저가 자동으로 요소를 매칭한다. 단, 2026-Q2 기준 Chromium 전용이므로 fallback 경로를 유지한다.

13. **모션은 정적 코드로 입증되지 않는다 — 완료 선언 전 증거 필수 (E2)**: 이 스킬의 산출물은 **재생되어야만 존재를 확인할 수 있다**. `animate-*` 클래스가 붙어 있다는 사실, `startViewTransition` 이 호출된다는 사실은 R3(정적) 증거이며 애니메이션이 실제로 재생됐다는 증거가 아니다 — keyframe 미정의, `prefers-reduced-motion` 상시 적중, 부모의 `overflow: hidden` 클리핑, 미지원 브라우저 fallback 진입은 전부 조용히 "아무 일도 안 일어남" 으로 끝난다. 완료 직전에 `react-kit/references/render-evidence-protocol.md` §4 체크리스트를 채운다. 스냅샷 비교로 검증할 때는 **전/후 두 시점을 지목**한다 — 정지 프레임 1 장은 어떤 모션에도 같은 결과를 내므로 oracle 이 아니다 (§3 d). 증거를 못 얻으면 `[미검증]` 마커와 사유를 붙이고 부분 완료로 보고한다.

    **증거 확보를 위해 애니메이션 라이브러리를 도입하지 않는다.** Library Policy (Gotcha #1) 는 이 규약보다 상위이며 어떤 검증 편의로도 완화되지 않는다.

# Process

## 1. 자동 티어 판정

`--tier` 플래그가 없으면 사용자 요청을 분석해 가장 낮은 티어를 선택한다.

| 키워드 / 시나리오 | 판정 Tier |
|------------------|-----------|
| "fade in", "slide up", "scale", "pulse", "bounce", "hover 효과", "opacity", "shimmer", "진입 애니메이션" | **T1** |
| "skeleton 로딩 → 완료 전환", "버튼 hover", "accordion", "모달 open/close", "상태 변화" | **T1** |
| "스크롤 애니메이션", "scroll-driven", "parallax", "스크롤 진행 바", "스크롤 기반" | **T1** |
| "페이지 전환", "shared element", "grid to board", "뷰 전환", "라우트 전환", "DOM 구조 변경" | **T2** |
| "scroll-triggered", "스크롤 교차 시 트리거", "특정 위치에서 애니메이션 시작" | **T2** |
| "드래그앤드롭", "정렬 리스트", "sortable", "kanban", "드래그", "드롭", "gesture", "화살표 연결선" | **T3** |

T2/T3 경계가 애매하면 `animation-architect-react` 에이전트에 자문을 요청한다.

**3-Tier 요약:**

| Tier | 도구 | 적용 시나리오 | 난이도 |
|------|------|--------------|--------|
| **T1** | Tailwind `animate-*` + CSS `@keyframes` + scroll-driven | 상태 변화, hover, 단순 loop, 스크롤 연동 | 낮음 |
| **T2** | View Transitions API | 뷰/라우트 전환, shared element, FLIP | 중 |
| **T3** | Pointer Events + FSM + requestAnimationFrame | 드래그앤드롭, 제스처, SVG 연결선 | 높음 |

## 2. Tier 1 — Tailwind + CSS 구현

### 2.1 Tailwind 내장 유틸리티

| 카테고리 | 유틸 | 예시 |
|----------|------|------|
| Transition | `transition-transform`, `transition-colors`, `transition-opacity` | `hover:scale-105 transition-transform duration-200` |
| Duration | `duration-75`~`duration-1000` | `duration-300` |
| Easing | `ease-linear`, `ease-in`, `ease-out`, `ease-in-out` | `ease-in-out` |
| Animation (내장) | `animate-spin`, `animate-ping`, `animate-pulse`, `animate-bounce` | 로딩, 알림 |
| Delay | `delay-75`~`delay-1000` | stagger 효과 |

### 2.2 tailwindcss-animate 확장 유틸

`tailwindcss-animate` 플러그인이 제공하는 enter/exit 애니메이션:
- `animate-in` / `animate-out`
- `fade-in-*`, `fade-out-*`
- `slide-in-from-top/bottom/left/right-*`, `slide-out-to-*`
- `zoom-in-*`, `zoom-out-*`

`data-[state=...]` 속성 선택자와 조합해 상태 기반 애니메이션을 구현한다:

```tsx
// 드로어 open/close 예시
<div
  data-state={open ? 'open' : 'closed'}
  className="
    data-[state=open]:animate-in data-[state=closed]:animate-out
    data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0
    data-[state=closed]:slide-out-to-left data-[state=open]:slide-in-from-left
    duration-300
    motion-reduce:transition-none motion-reduce:animate-none
  "
>
  드로어 내용
</div>
```

### 2.3 CSS @keyframes 직접 선언

Tailwind 유틸로 커버 안 되는 커스텀 애니메이션은 `globals.css` 의 `@theme` 블록에 선언한다:

```css
/* src/presentation/styles/globals.css */
@import "tailwindcss";

@theme {
  --animate-wiggle: wiggle 1s ease-in-out infinite;
  --animate-shimmer: shimmer 2s linear infinite;

  @keyframes wiggle {
    0%, 100% { transform: rotate(-3deg); }
    50%      { transform: rotate(3deg); }
  }

  @keyframes shimmer {
    from { background-position: -200% 0; }
    to   { background-position: 200% 0; }
  }
}

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

사용: `<div className="animate-wiggle">...</div>`

### 2.4 Tier 1 시나리오 예시

**Fade-in 진입:**

```tsx
<div className="animate-in fade-in-0 duration-500 motion-reduce:animate-none">
  페이지 로드 시 페이드 진입
</div>
```

**Hover scale 버튼:**

```tsx
<button className="transition-transform duration-200 hover:scale-105 active:scale-95 motion-reduce:transition-none">
  버튼
</button>
```

**스태거 리스트 진입:**

```tsx
{items.map((item, i) => (
  <div
    key={item.id}
    className="animate-in slide-in-from-bottom-4 fade-in-0 motion-reduce:animate-none"
    style={{ animationDelay: `${i * 50}ms`, animationFillMode: 'backwards' }}
  >
    {item.name}
  </div>
))}
```

### 2.5 Scroll-driven Animations (CSS 네이티브)

스크롤 위치에 연동되는 애니메이션을 JS 없이 CSS `animation-timeline` 으로 구현한다. Chrome 안정, Firefox 플래그 필요 (2026-Q2 기준). `@supports` 로 감싸 미지원 브라우저에서 graceful fallback 한다.

**스크롤 진행 바:**

```css
/* globals.css */
@keyframes progress-grow {
  from { transform: scaleX(0); }
  to   { transform: scaleX(1); }
}
```

```tsx
<div
  className="fixed top-0 left-0 h-1 w-full origin-left bg-primary motion-reduce:hidden"
  style={{
    animation: 'progress-grow linear',
    animationTimeline: 'scroll(root block)',
  }}
/>
```

**요소 진입 시 fade-in (view timeline):**

```css
@keyframes fade-slide-in {
  from { opacity: 0; transform: translateY(2rem); }
  to   { opacity: 1; transform: translateY(0); }
}

@supports (animation-timeline: view()) {
  .scroll-reveal {
    animation: fade-slide-in linear both;
    animation-timeline: view();
    animation-range: entry 0% entry 100%;
  }
}
```

```tsx
<section className="scroll-reveal motion-reduce:opacity-100">
  스크롤 시 등장하는 콘텐츠
</section>
```

> **주의**: scroll-triggered animations (Chrome 145, 2026) 는 특정 스크롤 오프셋 교차 시 시간 기반 애니메이션을 트리거하는 별개 개념이다. scroll-driven 과 혼동하지 않는다. scroll-triggered 는 Tier 2 후보로 분류한다.

## 3. Tier 2 — View Transitions API 구현

2026-04 기준 Baseline Newly Available (Chrome/Safari/Firefox 144+). SPA 내 DOM 변경 시 자동 FLIP 애니메이션.

### 3.1 withViewTransition 래퍼 생성

파일이 없으면 생성한다:

```ts
// src/presentation/shared/lib/view-transition.ts
export function withViewTransition(
  updateDOM: () => void,
  options?: { types?: string[] },
): void {
  // prefers-reduced-motion 존중
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    updateDOM()
    return
  }
  // Feature detection (구형 브라우저 fallback)
  if (typeof document.startViewTransition !== 'function') {
    updateDOM()
    return
  }
  // types 파라미터 지원 여부 분기 (Firefox 초기 구현 미지원)
  try {
    if (options?.types && options.types.length > 0) {
      document.startViewTransition({ update: updateDOM, types: options.types })
    } else {
      document.startViewTransition(updateDOM)
    }
  } catch {
    updateDOM()
  }
}
```

### 3.2 view-transition-name CSS 공유 요소

DOM 구조가 바뀌어도 "같은 요소"로 식별해 부드럽게 이동시킨다:

```tsx
// 동적 id로 고유성 보장 (중복 이름 금지)
<div
  className="rounded-lg border p-4"
  style={{ viewTransitionName: `task-${task.id}` }}
>
  {task.title}
</div>
```

### 3.3 그리드 ↔ 보드 뷰 전환 (대표 시나리오)

```tsx
// src/presentation/features/tasks/components/task-switcher.tsx
import { withViewTransition } from '@/presentation/shared/lib/view-transition'
import { useTaskStore } from '../store'

export function TaskViewSwitcher() {
  const viewMode = useTaskStore((s) => s.viewMode)
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

### 3.4 CSS 전환 세부 조정

```css
/* globals.css — 전환 duration + easing */
::view-transition-group(*) {
  animation-duration: 0.4s;
  animation-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
}

/* 특정 요소 개별 조정 */
::view-transition-group(hero-image) {
  animation-duration: 0.6s;
}

/* reduced-motion 에서 즉시 전환 */
@media (prefers-reduced-motion: reduce) {
  ::view-transition-group(*) {
    animation-duration: 0.01ms;
  }
}
```

## 4. Tier 3 — 커스텀 Pointer Primitives 구현

라이브러리 없이 Pointer Events API + 상태 머신(FSM)으로 직접 구현한다.

### 4.1 useDrag 훅 생성

```ts
// src/presentation/shared/hooks/use-drag.ts
import { useCallback, useEffect, useReducer, useRef } from 'react'

// FSM 3 상태: idle / dragging / dropping
type DragState =
  | { kind: 'idle' }
  | { kind: 'dragging'; startX: number; startY: number; offsetX: number; offsetY: number; pointerId: number }
  | { kind: 'dropping'; offsetX: number; offsetY: number }

type DragAction =
  | { type: 'start'; x: number; y: number; pointerId: number }
  | { type: 'move'; x: number; y: number }
  | { type: 'drop' }
  | { type: 'resolved' }
  | { type: 'cancel' }

function dragReducer(state: DragState, action: DragAction): DragState {
  switch (action.type) {
    case 'start':
      return { kind: 'dragging', startX: action.x, startY: action.y, offsetX: 0, offsetY: 0, pointerId: action.pointerId }
    case 'move':
      if (state.kind !== 'dragging') return state
      return { ...state, offsetX: action.x - state.startX, offsetY: action.y - state.startY }
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
  resolve: () => void
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
    dispatch({ type: 'drop' })
  }, [])

  // pointercancel: 탭 전환, 앱 포커스 이탈, 요소 unmount 시 상태 리셋 필수
  const onPointerCancel = useCallback((e: React.PointerEvent) => {
    if (e.currentTarget.hasPointerCapture(e.pointerId)) {
      e.currentTarget.releasePointerCapture(e.pointerId)
    }
    dispatch({ type: 'cancel' })
  }, [])

  const resolve = useCallback(() => {
    dispatch({ type: 'resolved' })
  }, [])

  // ESC 키로 드래그 취소
  useEffect(() => {
    function handleEscape(e: KeyboardEvent) {
      if (e.key === 'Escape') dispatch({ type: 'cancel' })
    }
    window.addEventListener('keydown', handleEscape)
    return () => window.removeEventListener('keydown', handleEscape)
  }, [])

  return { state, handlers: { onPointerDown, onPointerMove, onPointerUp, onPointerCancel }, ref, resolve }
}
```

**사용 예시:**

```tsx
export function DraggableCard() {
  const { state, handlers } = useDrag()
  const translate = state.kind === 'dragging'
    ? `translate(${state.offsetX}px, ${state.offsetY}px)`
    : 'none'

  return (
    <div
      {...handlers}
      // touch-none = touch-action: none — 브라우저 기본 터치 동작 차단
      className="touch-none rounded-lg border p-4 cursor-grab active:cursor-grabbing"
      style={{ transform: translate }}
    >
      드래그하세요
    </div>
  )
}
```

### 4.2 Zustand drag store 생성

여러 컴포넌트에 걸친 드래그 상태는 전역 단일 Zustand store로 관리한다:

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

### 4.3 useDrop 훅 생성

```ts
// src/presentation/shared/hooks/use-drop.ts
import { useCallback } from 'react'
import { useDragStore } from '@/presentation/shared/stores/drag-store'

type UseDropOptions<T> = {
  dropZoneId: string
  canAccept?: (active: { id: string; sourceColumnId: string }) => boolean
  onDrop: (active: { id: string; sourceColumnId: string }) => void
}

export function useDrop<T>(options: UseDropOptions<T>): {
  isOver: boolean
  canDrop: boolean
  handlers: {
    onPointerEnter: (e: React.PointerEvent) => void
    onPointerLeave: (e: React.PointerEvent) => void
    onPointerUp: (e: React.PointerEvent) => void
  }
} {
  const active = useDragStore((s) => s.active)
  const hoverColumnId = useDragStore((s) => s.hoverColumnId)
  const setHover = useDragStore((s) => s.hover)
  const endDrag = useDragStore((s) => s.end)

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
    if (active === null || hoverColumnId !== options.dropZoneId) return
    if (options.canAccept && !options.canAccept(active)) return
    options.onDrop(active)
    endDrag()
  }, [active, hoverColumnId, options, endDrag])

  return { isOver, canDrop, handlers: { onPointerEnter, onPointerLeave, onPointerUp } }
}
```

### 4.4 useSortable 훅 생성

```ts
// src/presentation/shared/hooks/use-sortable.ts
// 핵심 아이디어: drag 중 각 아이템의 bounding rect 측정 →
// 포인터 위치 비교 → 목표 index 계산 → 배열 재정렬 후 re-render
// 전체 구현은 요청 시 생성 (200~300줄)

export function useSortable<T>(
  items: T[],
  getId: (item: T) => string,
  onReorder: (next: T[]) => void,
): {
  orderedItems: T[]
  getDragHandlers: (id: string) => {
    onPointerDown: (e: React.PointerEvent) => void
    onPointerMove: (e: React.PointerEvent) => void
    onPointerUp: (e: React.PointerEvent) => void
    onPointerCancel: (e: React.PointerEvent) => void
  }
  draggingId: string | null
} {
  // Pointer Events + bounding rect 기반 정렬 로직
  // 구현체는 useDrag 패턴 확장 + itemsRef(배열 ref) 사용
  throw new Error('useSortable stub — /react-animation 스킬이 전체 구현을 생성합니다')
}
```

### 4.5 칸반 드래그앤드롭 통합 예시

```tsx
// src/presentation/features/kanban/components/kanban-board.tsx
import { useDrag } from '@/presentation/shared/hooks/use-drag'
import { useDrop } from '@/presentation/shared/hooks/use-drop'
import { useDragStore } from '@/presentation/shared/stores/drag-store'

type Card = { id: string; title: string; columnId: string }
type Column = { id: string; title: string }

export function KanbanBoard({ columns, cards }: { columns: Column[]; cards: Card[] }) {
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
  const { isOver, canDrop, handlers } = useDrop({
    dropZoneId: column.id,
    canAccept: (active) => active.sourceColumnId !== column.id,
    onDrop: (active) => {
      // G2 /react-query mutation 패턴 — 서버에 카드 이동 반영
      moveCard(active.id, column.id)
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
      {cards.map((card) => <KanbanCard key={card.id} card={card} />)}
    </div>
  )
}

function KanbanCard({ card }: { card: Card }) {
  const startDrag = useDragStore((s) => s.start)
  const endDrag = useDragStore((s) => s.end)
  const { state, handlers: dragHandlers, resolve } = useDrag()

  const isDragging = state.kind === 'dragging'
  const isDropping = state.kind === 'dropping'
  const translate =
    state.kind === 'dragging' || state.kind === 'dropping'
      ? `translate(${state.offsetX}px, ${state.offsetY}px)`
      : 'none'

  return (
    <div
      onPointerDown={(e) => { dragHandlers.onPointerDown(e); startDrag(card.id, card.columnId) }}
      onPointerMove={dragHandlers.onPointerMove}
      onPointerUp={(e) => { dragHandlers.onPointerUp(e); endDrag(); resolve() }}
      onPointerCancel={(e) => { dragHandlers.onPointerCancel(e); endDrag() }}
      // tabIndex + role: 키보드 접근성 필수
      tabIndex={0}
      role="button"
      aria-describedby={`drag-instructions-${card.id}`}
      className={`
        touch-none rounded border bg-card p-3 cursor-grab
        ${isDragging ? 'opacity-50 shadow-lg cursor-grabbing z-10 relative' : ''}
        ${isDropping ? 'opacity-70 pointer-events-none' : ''}
        motion-reduce:transition-none
      `}
      style={{ transform: translate }}
    >
      <span id={`drag-instructions-${card.id}`} className="sr-only">
        스페이스 또는 엔터로 집기, 화살표 키로 이동, 다시 스페이스로 내려놓기
      </span>
      {card.title}
    </div>
  )
}
```

### 4.6 SVG 화살표 / 연결선 (Connector)

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

  const midX = (from.x + to.x) / 2
  const d = `M ${from.x} ${from.y} C ${midX} ${from.y}, ${midX} ${to.y}, ${to.x} ${to.y}`

  return (
    // pointer-events-none: SVG가 마우스 이벤트를 차단하지 않게
    <svg className="pointer-events-none fixed inset-0 h-full w-full" aria-hidden="true">
      <path d={d} stroke="currentColor" strokeWidth="2" fill="none" />
      <circle cx={to.x} cy={to.y} r="4" fill="currentColor" />
    </svg>
  )
}
```

## 5. 접근성 (a11y)

라이브러리 0개 접근에서 접근성은 **사용자 책임**이다. `/react-animation` 스킬은 최소 체크리스트를 스캐폴딩한다.

### 5.1 prefers-reduced-motion 처리

- **Tier 1**: Tailwind `motion-reduce:animate-none`, `motion-reduce:transition-none` variant 적용
- **Tier 2**: `withViewTransition` 래퍼에서 `window.matchMedia('(prefers-reduced-motion: reduce)')` 가드 적용
- **Tier 3**: CSS transform 애니메이션 대신 즉시 이동

### 5.2 드래그앤드롭 키보드 대안

```tsx
// 키보드 드래그 대안: Space 집기 → 화살표 이동 → Space 내려놓기
function KanbanCard({ card }: { card: Card }) {
  const [isKeyboardDragging, setIsKeyboardDragging] = useState(false)

  function handleKeyDown(e: React.KeyboardEvent) {
    if (e.key === ' ' || e.key === 'Enter') {
      setIsKeyboardDragging((prev) => !prev)
    }
    if (isKeyboardDragging && e.key === 'ArrowRight') {
      // 오른쪽 컬럼으로 이동 로직
    }
    if (e.key === 'Escape') {
      setIsKeyboardDragging(false)
    }
  }

  return (
    <div
      tabIndex={0}
      role="button"
      onKeyDown={handleKeyDown}
      aria-pressed={isKeyboardDragging}
      // ...
    />
  )
}
```

### 5.3 ARIA live region (드래그 상태 알림)

```tsx
// 드래그 상태를 스크린리더에 알리는 live region
export function DragAnnouncer({ message }: { message: string }) {
  return (
    <div
      aria-live="polite"
      aria-atomic="true"
      className="sr-only"
    >
      {message}
    </div>
  )
}

// 사용: 드래그 시작/이동/완료/취소 시 message 업데이트
```

### 5.4 접근성 트레이드오프 고지

> 라이브러리 0개 접근은 번들 크기·커스텀·성능을 얻는 대신, 드래그앤드롭의 완전한 스크린리더 접근성 구현 책임이 사용자에게 있다. 완전한 a11y를 최우선으로 한다면 W3C APG 드래그앤드롭 패턴(https://www.w3.org/WAI/ARIA/apg/)을 직접 구현하거나, 접근성이 내장된 라이브러리 사용을 고려한다.

## 6. 아키텍처 배치 규칙

| 산출물 | 위치 |
|--------|------|
| CSS @keyframes | `src/presentation/styles/globals.css` |
| View Transition 래퍼 | `src/presentation/shared/lib/view-transition.ts` |
| useDrag, useDrop, useSortable | `src/presentation/shared/hooks/` |
| drag-store (Zustand) | `src/presentation/shared/stores/drag-store.ts` |
| Connector, DraggableItem | `src/presentation/shared/components/` |
| feature 전용 drag 컴포넌트 | `src/presentation/features/<name>/components/` |
| **금지** | `domain/`, `data/` 에 pointer/transition/drag-store import |

## 7. 완료 후 안내

구현 완료 후 사용자에게 다음을 안내한다:

- Tier 1: 확인된 Tailwind 클래스 목록 + globals.css 변경 사항
- Tier 2: 생성된 파일 목록 (`view-transition.ts` 등) + 브라우저 지원 현황
- Tier 3: 생성된 훅/store 목록 + 접근성 체크리스트

다음 단계 제안:
- 접근성 검증: `/react-audit` (reduced-motion, ARIA 가드 검사)
- 테스트 생성: `/react-test` (pointer event 테스트는 `@testing-library/user-event` `user.pointer()` API)
- 컴포넌트 감지: `widget-inspector-react` 에이전트

# References

- `references/clean-arch-layout.md` — 레이어 배치 규칙 (presentation 전용)
- `references/project-detection.md` — 프로젝트 감지 (Tailwind 버전, tailwindcss-animate 설치 여부)
- `docs/react/kit-design/g5b-animation.md` — 이 스킬의 전체 설계 문서
