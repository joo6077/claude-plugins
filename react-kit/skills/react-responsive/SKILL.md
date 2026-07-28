---
name: react-responsive
description: >
  기존 화면/컴포넌트에 반응형 레이아웃을 적용한다.
  Tailwind v4 페이지 breakpoint(sm/md/lg/xl/2xl)와 Container Queries(@container)를 상황에 맞게 혼용.
  "반응형", "responsive", "태블릿 대응", "breakpoint 적용", "Container Queries",
  "데스크탑 레이아웃", "2컬럼", "그리드 반응형" 같은 요청 시 트리거.
  새 컴포넌트 생성이 필요하면 트리거하지 않는다 — /react-widget 사용.
argument-hint: "<target_path> [--container-query | --page-query]"
user-invocable: true
---

# Gotchas

1. **breakpoint 하드코딩 금지** — `min-width: 768px` 같은 인라인 스타일 대신 Tailwind 토큰(`md:`, `lg:`)만 사용. 매직 픽셀값이 코드베이스에 퍼지면 디자인 시스템과 단절된다.
2. **`@container` vs 페이지 breakpoint 혼동** — 재사용 컴포넌트(Card, Modal 내부, 사이드바 아이템)는 `@container`, 앱 최상위 레이아웃(사이드바 펼침, 네비 분기)은 페이지 breakpoint. 둘을 뒤바꾸면 재사용 시 레이아웃이 깨진다.
3. **Tailwind v3에서 `@container` 사용 시도** — Tailwind v3 프로젝트는 `@tailwindcss/container-queries` 플러그인 + `tailwind.config.ts` 등록이 필요하다. v4는 내장. 프로젝트 버전을 먼저 확인한다.
4. **`display: contents` 중간 삽입** — `@container` 선언과 자식 사이에 `display: contents` 요소가 끼면 컨테이너 컨텍스트가 자식에게 전달되지 않는다.
5. **텍스트 크기 다단 반응형 과용** — `text-sm md:text-base lg:text-lg` 같은 3단계 텍스트 크기 변경은 타이포 리듬을 깨뜨린다. 디자인 시스템의 정해진 scale만 사용한다.
6. **모바일 퍼스트 원칙 누락** — 항상 가장 좁은 너비를 기본값으로 선언하고(`grid-cols-1`) 큰 쪽으로 확장(`sm:grid-cols-2`)한다. 데스크탑 레이아웃을 먼저 쓰고 모바일에서 override하는 패턴은 specificity 지옥을 만든다.
7. **`cn()` 없이 조건부 클래스 합성** — `className={isActive ? 'foo' : 'bar'}` 중첩이 복잡해지면 `cn()` 유틸리티로 정리한다. 직접 문자열 합성은 Tailwind Merge와 충돌할 수 있다.
8. **기존 파일 className 이외 변경 금지** — 이 스킬은 className 속성만 수정한다. 컴포넌트 로직, Props 타입, 파일 구조는 건드리지 않는다.
9. **WCAG 2.2 SC 2.5.8 터치타겟 24×24 — breakpoint 전환에서 유지** (Level AA) — 좁은 화면 breakpoint 에서 아이콘 버튼/네비 아이템이 축소될 때도 **최소 24×24 CSS 픽셀** 을 보장해야 한다. Tailwind 기준 `min-w-6 min-h-6` 가드를 상시 걸거나, `size-*` 를 6 미만으로 내리지 않는다. 권장 최솟값은 `size-8`(32px) — 손가락 정확도 여유분. Phase 6 design-kit 정합 (WCAG 2.2 / SC 2.5.8).

    나쁜 예 — md 이하에서 22px 로 축소:

    ```tsx
    <button className="h-10 w-10 md:h-6 md:w-6">
      <Icon />
    </button>
    ```

    좋은 예 — 최소 size-8 가드 유지:

    ```tsx
    <button className="h-10 w-10 md:h-8 md:w-8 min-h-8 min-w-8">
      <Icon />
    </button>
    ```

10. **breakpoint 별 렌더 증거 없이 완료 선언 금지 (E2)** — Tailwind 클래스는 문자열이라 타입 검사를 통과해도 오타(`md:felx`)·Merge 충돌·존재하지 않는 breakpoint 접두사가 그대로 남는다. 즉 "코드에 `md:` 가 있다" 는 정적 확인(R3)일 뿐이고, 그 breakpoint 에서 레이아웃이 실제로 바뀐다는 증거가 아니다. 완료 직전에 `react-kit/references/render-evidence-protocol.md` §4 체크리스트를 채우되, **적용한 breakpoint 마다 최소 1 개씩** 증거를 남긴다 (한 폭에서만 확인하고 나머지를 추정하지 않는다). 증거를 못 얻는 폭은 `[미검증]` 마커와 사유를 붙이고 부분 완료로 보고한다.

# Process

## 1. 프로젝트 환경 감지

`references/project-detection.md` 절차를 실행한다:
- `package.json`에서 Tailwind 버전 확인 (`tailwindcss` 패키지)
  - `^4.x` → `@container` 내장, 플러그인 불필요
  - `^3.x` → `@tailwindcss/container-queries` 설치 여부 확인 (`tailwind.config.ts` 내 plugins 배열)
- `components.json` 존재 여부 (shadcn 초기화 확인)
- `src/presentation/shared/lib/utils.ts`의 `cn` 헬퍼 존재 여부

Tailwind v3에서 `@container` 사용이 필요하고 플러그인이 없으면 설치를 안내한다:
```bash
pnpm add -D @tailwindcss/container-queries
```

## 2. 입력 수집

- `target_path` (필수): 반응형을 적용할 컴포넌트/화면 경로
- `--container-query` (선택 플래그): 컨테이너 쿼리 강제 사용
- `--page-query` (선택 플래그): 페이지 breakpoint 강제 사용
- 플래그 없으면 경로를 보고 자동 판단 (§3 참조)

## 3. 페이지 쿼리 vs 컨테이너 쿼리 자동 판단

명시적 플래그가 없으면 `target_path`로 판단한다:

| 경로 패턴 | 선택 | 이유 |
|-----------|------|------|
| `src/presentation/routes/*.tsx` | 페이지 breakpoint | 뷰포트 전체가 레퍼런스인 최상위 라우트 |
| `src/presentation/features/*/screens/*.tsx` | 페이지 breakpoint | 화면 단위 레이아웃 |
| `src/presentation/shared/components/**/*.tsx` | 컨테이너 쿼리 우선 | 다양한 컨텍스트에서 재사용되는 공용 컴포넌트 |
| `src/presentation/features/*/components/**/*.tsx` | 컨테이너 쿼리 우선 | 컨테이너 크기에 따라 적응해야 하는 기능별 컴포넌트 |

**원칙**: 컴포넌트의 재사용 범위가 판단 기준. 화면 전체에서만 쓰이면 페이지 breakpoint, 여러 컨텍스트(모달, 사이드바, 풀스크린)에서 쓰이면 컨테이너 쿼리.

## 4. 대상 파일 분석

`target_path` 파일을 읽고 현재 레이아웃을 파악한다:
- 고정된 `grid-cols-N` 또는 `flex` 구조 확인
- 반응형으로 전환해야 할 레이아웃 블록 식별
- 이미 적용된 breakpoint 또는 `@container` 확인 (중복 적용 방지)

## 5. Tailwind v4 breakpoint 체계 (페이지 쿼리 선택 시)

| 키 | min-width | 권장 용도 |
|----|-----------|-----------|
| `sm:` | 640px | 큰 모바일 / 세로 태블릿 |
| `md:` | 768px | 세로 태블릿 |
| `lg:` | 1024px | 가로 태블릿 / 작은 노트북 |
| `xl:` | 1280px | 노트북 |
| `2xl:` | 1536px | 큰 데스크탑 |

**그리드 반응형 패턴** (모바일 퍼스트):

```tsx
// 1 → 2 → 3 → 4컬럼 확장
<div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
  {items.map((item) => <Card key={item.id} {...item} />)}
</div>
```

**스택 → 수평 전환 패턴**:

```tsx
<div className="flex flex-col gap-4 md:flex-row md:items-start">
  <aside className="w-full md:w-64 lg:w-80">...</aside>
  <main className="flex-1">...</main>
</div>
```

## 6. Container Queries 패턴 (컨테이너 쿼리 선택 시)

Tailwind v4는 `@container` 유틸리티가 내장되어 있다.

**기본 컨테이너 쿼리**:

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

**기본 컨테이너 크기 기준**:

| 키 | min-width | 설명 |
|----|-----------|------|
| `@xs` | 20rem (320px) | 매우 좁은 패널 |
| `@sm` | 24rem (384px) | 좁은 패널 |
| `@md` | 28rem (448px) | 보통 패널 |
| `@lg` | 32rem (512px) | 넓은 패널 |
| `@xl` | 36rem (576px) | 매우 넓은 패널 |
| `@2xl` | 42rem (672px) | 전체 너비급 |

**네임드 컨테이너** (중첩 컨테이너 구분):

```tsx
<div className="@container/card">
  <div className="flex flex-col @sm/card:flex-row @sm/card:items-center">
    <img className="w-full @sm/card:w-24 @sm/card:flex-none" ... />
    <div className="flex-1">...</div>
  </div>
</div>
```

## 7. Before/After 제시 및 적용

변경 전후를 사용자에게 보여주고 승인받은 후 파일에 적용한다.

**Before → After 예시 (페이지 쿼리)**:

```tsx
// Before
<div className="grid grid-cols-3 gap-4">

// After
<div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
```

**Before → After 예시 (컨테이너 쿼리)**:

```tsx
// Before
<div className="flex gap-4">
  <img className="w-24" />
  <div>...</div>
</div>

// After
<div className="@container">
  <div className="flex flex-col gap-4 @sm:flex-row">
    <img className="w-full @sm:w-24 @sm:flex-none" />
    <div className="flex-1">...</div>
  </div>
</div>
```

## 8. Strict TS 검증

Tailwind 클래스는 문자열이라 TypeScript 영향 밖이지만, 조건부 클래스 합성이 있으면 검증한다:

```bash
pnpm tsc --noEmit
pnpm eslint <target_path> --max-warnings=0
```

## 9. 완료 후 안내

변경된 파일과 적용된 패턴(페이지/컨테이너)을 요약한다.

다음 단계:
- 로딩 상태 skeleton 추가: `/react-skeleton`
- 재사용 컴포넌트 감지: widget-inspector-react 에이전트
- 재사용 컴포넌트 추출: `/react-extract`

# References

- `references/project-detection.md` — 프로젝트 감지 (Tailwind 버전, shadcn 초기화)
- `references/clean-arch-layout.md` — 컴포넌트 배치 경로 규칙
- `docs/react/kit-design/g5-ui-patterns.md` §1 — 이 스킬의 상세 설계
