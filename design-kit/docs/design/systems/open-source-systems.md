---
title: 오픈소스 디자인 시스템 분석
version: 0.3.0
last_updated: 2026-03-30
---

# 오픈소스 디자인 시스템 분석

Radix UI, Shadcn/ui, Tailwind CSS에 더해 Ant Design, Chakra UI, Mantine의 비교 분석을 포함한다.

---

## Radix UI

Radix UI는 접근성 중심의 비스타일(unstyled) React 프리미티브 라이브러리다. Node.js, Vercel, Supabase 팀이 사용하며, Shadcn/ui의 기반 레이어로 채택되었다.

### 핵심 철학: 접근성 우선 (Accessibility-First)

Radix Primitives는 WAI-ARIA 저작 관행 가이드라인을 준수하며, 접근성 구현의 어려운 세부사항을 라이브러리가 자체 처리한다.

- **ARIA 속성**: `aria-*`, `role` 속성을 자동 관리
- **포커스 관리**: 컴포넌트 열림/닫힘 시 프로그래밍 방식으로 포커스 이동 (예: AlertDialog가 열리면 Cancel 버튼으로 포커스 자동 이동)
- **키보드 내비게이션**: Tab, Arrow, Enter, Escape 등 WAI-ARIA에 정의된 키보드 인터랙션 패턴 내장
- **스크린 리더 테스트**: 최신 브라우저와 주요 보조 기술에서 테스트 완료

> **출처:** [Radix Primitives — Accessibility](https://www.radix-ui.com/primitives/docs/overview/accessibility)

### 비스타일 / 헤드리스 (Unstyled / Headless)

컴포넌트는 **스타일 없이** 제공되어, 개발자가 시각적 표현을 완전히 제어할 수 있다.

- CSS, Tailwind CSS, CSS-in-JS 등 어떤 스타일링 솔루션이든 적용 가능
- 디자인 시스템의 순수한 구조적 토대(structural foundation)로 기능
- "스타일이 아닌 행동"을 제공하는 것이 핵심 가치

```jsx
// Radix는 구조와 동작만 제공, 스타일은 자유롭게 적용
import * as Dialog from '@radix-ui/react-dialog';

<Dialog.Root>
  <Dialog.Trigger className="my-custom-button">열기</Dialog.Trigger>
  <Dialog.Portal>
    <Dialog.Overlay className="my-overlay" />
    <Dialog.Content className="my-dialog">
      <Dialog.Title>제목</Dialog.Title>
      <Dialog.Description>설명</Dialog.Description>
      <Dialog.Close>닫기</Dialog.Close>
    </Dialog.Content>
  </Dialog.Portal>
</Dialog.Root>
```

> **출처:** [Radix Primitives — Introduction](https://www.radix-ui.com/primitives/docs/overview/introduction)

### 개방형 컴포넌트 아키텍처

Radix는 각 컴포넌트의 **개별 파트에 대한 세밀한 접근**을 제공하는 개방형 아키텍처를 채택한다.

- **`asChild` prop**: 렌더링되는 요소를 완전히 교체할 수 있어, 기존 컴포넌트를 래핑하거나 커스텀 요소를 사용 가능
- **이벤트 리스너 부착**: 각 파트에 커스텀 이벤트 핸들러, props, refs를 자유롭게 추가
- **비제어 기본값**: 내부적으로 상태를 관리하되, 필요 시 제어(controlled) 모드로 전환 가능
- **트리 셰이킹**: `radix-ui` 통합 패키지 또는 `@radix-ui/react-*` 개별 패키지로 설치, 사용하는 컴포넌트만 번들에 포함

**주요 프리미티브 컴포넌트:**

| 카테고리 | 컴포넌트 |
|---------|---------|
| 오버레이 | Dialog, AlertDialog, Popover, Tooltip, HoverCard |
| 네비게이션 | NavigationMenu, Menubar, DropdownMenu, ContextMenu |
| 입력/선택 | Checkbox, RadioGroup, Select, Slider, Switch, Toggle, ToggleGroup |
| 표시 | Accordion, Collapsible, Tabs, Avatar, AspectRatio, Progress |
| 유틸리티 | Label, Separator, ScrollArea, VisuallyHidden |

> **출처:** [Radix Primitives](https://www.radix-ui.com/primitives)

---

## Shadcn/ui

Shadcn/ui는 전통적인 npm 패키지 방식을 거부하고, **소스 코드를 직접 복사**하여 프로젝트에 소유하는 새로운 컴포넌트 배포 모델이다. 공식 슬로건: "이것은 컴포넌트 라이브러리가 아니다. 당신이 컴포넌트 라이브러리를 만드는 방법이다."

### 5가지 기본 원칙

**1. Open Code (개방형 코드)**
- 컴포넌트 구현의 완전한 투명성과 소유권을 개발자에게 부여
- LLM이 코드를 직접 읽고 개선할 수 있는 AI 친화적 구조

**2. Composition (조합)**
- 모든 컴포넌트가 Radix UI 프리미티브를 기반으로 예측 가능하고 균일한 인터페이스를 공유
- 하나의 컴포넌트 API를 배우면 전체 시스템의 사용법을 이해

**3. Distribution (배포)**
- 플랫 파일 스키마와 CLI 도구로 프로젝트 간 컴포넌트 공유를 민주화
- npm 버전 관리의 제약 없이 자유로운 배포

**4. Beautiful Defaults (아름다운 기본값)**
- Tailwind CSS로 프리스타일된 프로덕션 레디 컴포넌트 제공
- 기본값이 아름답되, 완전한 커스터마이징 가능

**5. AI-Ready (AI 대응)**
- 일관된 API의 오픈소스 코드는 AI 도구가 이해하고 새 컴포넌트를 생성하기에 최적

> **출처:** [Shadcn/ui — Documentation](https://ui.shadcn.com/docs)

### Copy-Paste 컴포넌트 모델

| 관점 | 전통 라이브러리 | Shadcn/ui |
|------|-------------|-----------|
| **설치** | npm install | CLI로 소스 코드 복사 |
| **커스터마이징** | 스타일 오버라이드, 래핑 | 소스 코드 직접 편집 |
| **소유권** | 외부 유지보수자 | 내 코드베이스 |
| **버전 관리** | 시맨틱 버전 (npm) | Git 히스토리 |
| **AI 통합** | 블랙박스 코드 | 투명하고 읽기 쉬운 코드 |
| **의존성** | node_modules 비대화 | 의존성 없음 (소스 직접 포함) |

**CLI 도구 (`shadcn-cli`):**

```bash
# 프로젝트 초기화 — Tailwind, 경로 별칭 등 설정
npx shadcn-ui@latest init

# 개별 컴포넌트 추가 — 소스 코드가 프로젝트로 복사됨
npx shadcn-ui@latest add button
npx shadcn-ui@latest add dialog
npx shadcn-ui@latest add form
```

복사된 파일은 `components/ui/` 디렉토리에 저장되며, 개발자가 자유롭게 수정한다.

> **출처:** [Shadcn/ui — Documentation](https://ui.shadcn.com/docs)

### Tailwind 통합 및 커스터마이징

Shadcn/ui의 모든 스타일링은 Tailwind CSS 유틸리티 클래스로 구현된다.

- **테마 변수**: CSS 변수 기반 색상 체계로, `globals.css`에서 라이트/다크 테마를 한 곳에서 관리
- **cn() 유틸리티**: `clsx` + `tailwind-merge`로 조건부 클래스 결합과 충돌 해결
- **Radix + Tailwind**: Radix 프리미티브가 구조/접근성을 담당, Tailwind가 시각적 표현을 담당하는 명확한 역할 분리

```tsx
// cn() 유틸리티로 조건부 스타일 결합
import { cn } from "@/lib/utils"

<button className={cn(
  "px-4 py-2 rounded-md font-medium",
  variant === "destructive" && "bg-red-500 text-white",
  variant === "outline" && "border border-input bg-background",
  disabled && "opacity-50 cursor-not-allowed"
)}>
  {children}
</button>
```

**프레임워크 지원**: Next.js, Vite, Remix, Astro, Laravel 등 다양한 프레임워크별 CLI 설정 제공.

> **출처:** [Shadcn/ui — Documentation](https://ui.shadcn.com/docs)

---

## Tailwind CSS

Tailwind CSS는 유틸리티 우선(utility-first) CSS 프레임워크로, 미리 정의된 단일 목적 클래스를 HTML에서 직접 조합하여 스타일링한다.

### 유틸리티 우선 철학 (Utility-First)

전통적인 시맨틱 클래스 작성 대신, 프레젠테이션 목적의 유틸리티 클래스를 마크업에서 직접 조합한다.

```html
<!-- 전통 방식: 커스텀 클래스 작성 후 별도 CSS 파일에서 스타일 정의 -->
<div class="chat-notification">...</div>

<!-- Tailwind: 유틸리티 클래스를 직접 조합 -->
<div class="mx-auto flex max-w-sm items-center gap-x-4 rounded-xl bg-white p-6 shadow-lg">
  ...
</div>
```

**핵심 장점:**

| 장점 | 설명 |
|------|------|
| **빠른 개발** | 클래스 이름을 고민하거나 HTML↔CSS 전환 불필요 |
| **안전한 변경** | 유틸리티 수정은 해당 요소에만 영향, 다른 곳의 스타일이 깨지지 않음 |
| **쉬운 유지보수** | 요소를 찾아서 클래스를 변경 — 스타일시트 전체를 추적할 필요 없음 |
| **CSS 성장 억제** | 유틸리티 클래스는 재사용률이 높아 CSS 파일이 비대해지지 않음 |
| **이식성** | 구조와 스타일이 함께 있어, UI 청크를 통째로 복사/이동 가능 |

**인라인 스타일과의 차이:**

| 측면 | 인라인 스타일 | 유틸리티 클래스 |
|------|-----------|-------------|
| 디자인 제약 | 임의 값(매직 넘버) | 사전 정의된 디자인 시스템 |
| Hover/Focus | 불가능 | `hover:bg-sky-700` |
| 미디어 쿼리 | 불가능 | `sm:grid-cols-3` |
| 전역 변경 | 개별 수정 필요 | 테마 설정 1회 변경 |

> **출처:** [Tailwind CSS — Utility-First Fundamentals](https://tailwindcss.com/docs/utility-first)

### 디자인 토큰으로서의 설정 (Design Tokens as Config)

Tailwind는 하드코딩된 값 대신 `tailwind.config.js`(또는 CSS 변수 기반 테마)에서 정의된 **디자인 토큰**을 참조한다.

```js
// tailwind.config.js — 디자인 토큰 정의
module.exports = {
  theme: {
    colors: {
      primary: '#3B82F6',
      secondary: '#10B981',
    },
    spacing: {
      '1': '4px',
      '2': '8px',
      '4': '16px',
      '8': '32px',
    },
    borderRadius: {
      'sm': '4px',
      'md': '8px',
      'lg': '12px',
      'full': '9999px',
    }
  }
}
```

- 제한된 팔레트에서 선택하므로 시각적 일관성 보장
- 임의 값이 필요할 때는 대괄호 표기법: `bg-[#316ff6]`, `top-[calc(100%-2rem)]`
- CSS 변수로 런타임 테마 전환 가능

> **출처:** [Tailwind CSS — Utility-First Fundamentals](https://tailwindcss.com/docs/utility-first)

### 반응형 디자인 (Responsive)

**모바일 퍼스트 브레이크포인트**를 접두사 변형으로 제공한다. 접두사 없는 클래스가 모바일(최소 너비)에 적용되고, 접두사가 붙으면 해당 브레이크포인트 이상에서 적용된다.

```html
<!-- 모바일: 1열, sm: 2열, md: 3열, lg: 4열 -->
<div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4">
  ...
</div>
```

**기본 브레이크포인트:**

| 접두사 | 최소 너비 | CSS |
|--------|----------|-----|
| `sm` | 640px (40rem) | `@media (min-width: 640px)` |
| `md` | 768px (48rem) | `@media (min-width: 768px)` |
| `lg` | 1024px (64rem) | `@media (min-width: 1024px)` |
| `xl` | 1280px (80rem) | `@media (min-width: 1280px)` |
| `2xl` | 1536px (96rem) | `@media (min-width: 1536px)` |

### 상태 변형 (State Variants)

다양한 상태와 조건에 대한 스타일링을 접두사로 지원한다.

```html
<button class="bg-sky-500 hover:bg-sky-700 focus:outline-2 active:scale-95 disabled:opacity-50">
  저장
</button>
```

**주요 변형:**

| 변형 | 용도 |
|------|------|
| `hover:`, `focus:`, `active:` | 인터랙션 상태 |
| `disabled:` | 비활성 상태 |
| `group-hover:` | 부모 상태에 따른 자식 스타일 |
| `dark:` | 다크 모드 |
| `aria-current:`, `data-*:` | 속성 기반 스타일 |
| `sm:`, `md:`, `lg:` | 반응형 |
| `first:`, `last:`, `odd:` | 목록 내 위치 기반 |

복합 변형도 가능: `dark:lg:hover:bg-indigo-600`

### CSS 생성 최적화

Tailwind는 소스 파일을 스캔하여 **실제 사용된 클래스의 CSS만 생성**한다. 사용하지 않는 유틸리티는 번들에 포함되지 않아, 프로덕션 CSS 파일 크기를 최소화한다.

> **출처:** [Tailwind CSS — Utility-First Fundamentals](https://tailwindcss.com/docs/utility-first)

---

## Ant Design

Alibaba 그룹이 개발한 엔터프라이즈급 React UI 라이브러리다. 중국 시장에서 압도적 점유율을 가지며, 관리자 패널(admin panel)과 B2B 대시보드에 특화되어 있다.

### 핵심 특성

| 항목 | 내용 |
|------|------|
| **철학** | 자연스럽고(Natural), 확실하고(Certain), 의미있고(Meaningful), 성장하는(Growing) |
| **컴포넌트 수** | **60개 이상** — 가장 풍부한 기본 컴포넌트 세트 |
| **스타일링** | CSS-in-JS (v5에서 Less → CSS-in-JS 전환), 테마 토큰 기반 |
| **TypeScript** | 완전한 TS 지원 (소스 코드가 TS로 작성됨) |
| **npm 주간 다운로드** | 약 150만+ (2025 기준) |
| **번들 크기** | 전체 import 시 1MB+ — **트리 셰이킹 필수** |

### Ant Design 5.x 토큰 체계

3계층 토큰: Seed Token → Map Token → Alias Token

```tsx
<ConfigProvider
  theme={{
    token: {
      colorPrimary: '#1677ff',
      borderRadius: 6,
      fontSize: 14,
    },
    components: {
      Button: { colorPrimary: '#00b96b' },  // 컴포넌트별 독립 오버라이드
    },
  }}
>
  <App />
</ConfigProvider>
```

### 장단점

| 장점 | 단점 |
|------|------|
| 관리자 패널에 필요한 거의 모든 컴포넌트 기본 제공 | 번들 크기가 크다 — 트리 셰이킹 필수 |
| 풍부한 중국어/영어 이중 문서 | 디자인 톤이 획일적 — "Ant Design 냄새" |
| 대규모 팀에서 검증된 안정성 | 소비자향 앱에는 시각적으로 무겁다 |
| ProComponents로 복잡한 폼/테이블 로우코드 구현 | CSS-in-JS 런타임 오버헤드 (SSR 주의) |

> **출처:** [Ant Design — Official Documentation](https://ant.design/)

---

## Chakra UI

접근성 중심의 React 컴포넌트 라이브러리다. 직관적인 스타일 Props API가 최대 차별점이다.

### 핵심 특성

| 항목 | 내용 |
|------|------|
| **철학** | 접근성 우선, 개발자 친화적, 커스터마이즈 가능 |
| **컴포넌트 수** | 약 **50개** |
| **스타일링** | 스타일 Props (`bg="red.500"`, `p={4}`) |
| **접근성** | WAI-ARIA 준수, 키보드 네비게이션 기본 내장 |
| **npm 주간 다운로드** | 약 50만+ (2025 기준) |

### 스타일 Props 비교

```tsx
// Tailwind
<div className="bg-blue-500 p-4 rounded-lg text-white">Hello</div>

// Chakra
<Box bg="blue.500" p={4} borderRadius="lg" color="white">Hello</Box>

// Chakra 반응형
<Box fontSize={{ base: "sm", md: "md", lg: "lg" }}>반응형 텍스트</Box>
```

### Chakra UI v3

- **Ark UI 기반 재구축**: Zag.js 상태 머신으로 헤드리스 로직 분리
- **레시피 (Recipes)**: cva 패턴과 유사한 스타일 변형 조합 시스템

| 장점 | 단점 |
|------|------|
| 스타일 Props가 직관적 | JSX가 길어진다 (Props 수 많음) |
| 접근성 기본 내장 | 복잡한 데이터 컴포넌트 부족 |
| 테마 커스터마이징 용이 | Tailwind와 역할 중복 |

> **출처:** [Chakra UI — Official Documentation](https://chakra-ui.com/)

---

## Mantine

풀스택 React 컴포넌트 라이브러리 + 훅 컬렉션이다. 컴포넌트, 폼, 날짜, 차트, 알림을 하나의 생태계에서 제공한다.

### 핵심 특성

| 항목 | 내용 |
|------|------|
| **철학** | 풀스택 UI 툴킷 |
| **컴포넌트 수** | **100개 이상** (코어 + 확장 패키지) |
| **스타일링** | CSS Modules + CSS 변수 (v7에서 Emotion → PostCSS 전환) |
| **npm 주간 다운로드** | 약 40만+ (2025 기준) |

### 패키지 생태계

| 패키지 | 용도 |
|--------|------|
| `@mantine/core` | 핵심 UI 컴포넌트 |
| `@mantine/hooks` | 200+ 커스텀 훅 |
| `@mantine/form` | 폼 상태 관리 + 유효성 검증 |
| `@mantine/dates` | 날짜/시간 피커, 캘린더 |
| `@mantine/charts` | Recharts 래핑 차트 |
| `@mantine/notifications` | 토스트/알림 시스템 |
| `@mantine/spotlight` | Cmd+K 스타일 글로벌 검색 |

### 장단점

| 장점 | 단점 |
|------|------|
| 하나의 생태계에서 대부분의 UI 요구사항 해결 | 생태계 락인 위험 |
| CSS Modules 기반 — 런타임 오버헤드 없음 | 커뮤니티 규모가 상대적으로 작다 |
| 훅 라이브러리가 독립적으로 유용 | 한국어 문서 없음 |
| SSR/RSC 친화적 | 학습 곡선 존재 |

> **출처:** [Mantine — Official Documentation](https://mantine.dev/)

---

## 비교 매트릭스

| 기준 | Radix UI | Shadcn/ui | Tailwind | Ant Design | Chakra UI | Mantine |
|------|---------|-----------|---------|-----------|-----------|---------|
| **유형** | 헤드리스 | 복사형 | CSS 프레임워크 | 풀 UI 라이브러리 | 스타일 Props | 풀스택 툴킷 |
| **스타일링** | 없음 | Tailwind | Tailwind | CSS-in-JS | Emotion | CSS Modules |
| **접근성** | WAI-ARIA 완전 | Radix 상속 | 없음 | 부분 | WAI-ARIA 내장 | 부분 |
| **번들 크기** | 매우 작음 | 0 (소스 복사) | 작음 | 큼 | 중간 | 중간 |
| **적합한 프로젝트** | 커스텀 DS | AI 친화적 | 모든 프로젝트 | 관리자 패널 | 중소규모 SaaS | 풀스택 앱 |

### 선택 가이드

```
디자인 시스템을 처음부터 만드는가?
├─ Yes → Radix UI + Tailwind, 또는 Shadcn/ui
└─ No
    ├─ 관리자 패널 / B2B 대시보드?
    │   └─ Yes → Ant Design
    ├─ 접근성 최우선?
    │   └─ Yes → Chakra UI 또는 Radix UI
    └─ 폼/날짜/차트까지 한 생태계?
        └─ Yes → Mantine
```

> **출처:** [npm trends — UI Library Comparison](https://npmtrends.com/)
