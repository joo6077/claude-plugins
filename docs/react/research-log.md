---
version: 1.0.0
last_updated: 2026-04-11
---

# React Kit Research Log

> react-kaizen 실행 시 리서치한 외부 소스와 채택 여부를 누적 기록한다.

---

## 2026-04-11

**트리거:** kaizen-orchestrator Phase 10 (research-mode rerun)

### 조사한 소스

| # | 제목 | URL | 유형 | 신뢰도 | 결과 |
| - | ---- | --- | ---- | ------ | ---- |
| 1 | React v19 blog (2024-12-05) | <https://react.dev/blog/2024/12/05/react-19> | 공식 | 높음 | 채택 (stable) |
| 2 | React 19 new hooks deep dive | <https://medium.com/@rohitkuwar/deep-dive-into-react-19-s-latest-hooks-use-useactionstate-useoptimistic-and-useformstatus-849395af9c11> | blog | 중간 | 채택 |
| 3 | Tauri 2.0 stable blog | <https://v2.tauri.app/blog/tauri-20/> | 공식 | 높음 | 채택 |
| 4 | Tauri v1 → v2 migration | <https://v2.tauri.app/start/migrate/from-tauri-1/> | 공식 | 높음 | 채택 |
| 5 | Tauri v2 beta → stable migration | <https://v2.tauri.app/start/migrate/from-tauri-2-beta/> | 공식 | 높음 | 채택 |
| 6 | Tauri capabilities (ACL) | <https://v2.tauri.app/security/capabilities/> | 공식 | 높음 | 채택 (core:default) |
| 7 | Tailwind v4 announcement | <https://tailwindcss.com/blog/tailwindcss-v4> | 공식 | 높음 | 채택 |
| 8 | Tailwind v4 theme directive | <https://tailwindcss.com/docs/theme> | 공식 | 높음 | 채택 (@theme + OKLCH) |
| 9 | Tailwind v4 container queries | <https://www.sitepoint.com/tailwind-css-v4-container-queries-modern-layouts/> | blog | 중간 | 채택 |
| 10 | shadcn Tailwind v4 integration | <https://ui.shadcn.com/docs/tailwind-v4> | 공식 | 높음 | 채택 |
| 11 | shadcn components.json | <https://ui.shadcn.com/docs/components-json> | 공식 | 높음 | 채택 |
| 12 | Vite 8 Rolldown blog | <https://vite.dev/blog/announcing-vite8> | 공식 | 높음 | 채택 |
| 13 | Vite 6 Environment API | <https://vite.dev/blog/announcing-vite6> | 공식 | 높음 | 참조 |
| 14 | Zustand v5 announcement | <https://pmnd.rs/blog/announcing-zustand-v5/> | 공식 | 높음 | 채택 |
| 15 | Zustand v5 migration | <https://zustand.docs.pmnd.rs/reference/migrations/migrating-to-v5> | 공식 | 높음 | 채택 (useShallow 강제) |
| 16 | TanStack Query v5 migration | <https://tanstack.com/query/v5/docs/react/guides/migrating-to-v5> | 공식 | 높음 | 채택 (object-form) |
| 17 | TanStack Query v5 Query Invalidation | <https://tanstack.com/query/v5/docs/react/guides/query-invalidation> | 공식 | 높음 | 채택 |
| 18 | TanStack queryOptions+select type issue | <https://github.com/TanStack/query/issues/5436> | github | 중간 | 채택 (3 제네릭 명시) |
| 19 | Lingui v5 migration | <https://lingui.dev/releases/migration-5> | 공식 | 높음 | 채택 (macro split) |
| 20 | Lingui v5 macro reference | <https://lingui.dev/ref/macro> | 공식 | 높음 | 채택 |
| 21 | RHF resolvers Zod v4 issue #813 | <https://github.com/react-hook-form/resolvers/issues/813> | github | 중간 | 채택 (zod/v3 workaround) |
| 22 | WCAG 2.2 TR | <https://www.w3.org/TR/WCAG22/> | 공식 | 높음 | 채택 (SC 2.5.8 24x24) |

### 채택한 인사이트

- **React 19 stable (2024-12-05)**: `useActionState`, `useOptimistic`, `useFormStatus`, `use()` hook 이 production stable. 2026-04 현재 19.2 가 표준. Actions 패러다임으로 폼 제출 / mutation 재정의. `forwardRef` deprecation 예고 — 새 코드는 **ref-as-prop** 패턴 (`ref?: Ref<X>`). 기존 `forwardRef` 컴포넌트는 하위호환 유지. 적용: react-init, react-widget Gotchas + 템플릿.
- **Tauri 2 GA (2024-10-08)**: 1.x 코어 기능 대부분이 **개별 플러그인**으로 분리 (plugin-fs, plugin-dialog, plugin-shell 등). v1 allowlist → **ACL (capability)** 체계로 완전 전환. `src-tauri/capabilities/*.json` 에 identifier / description / windows / permissions 선언. Beta → Stable 마이그레이션: 모든 core permission identifier 앞에 `core:` prefix 필수 (예: `core:default`, `core:event:default`) 또는 `core:default` 단일 permission 로 통합. v1 → v2 `cargo tauri migrate` 자동 파싱 지원. 적용: react-init Tauri 섹션.
- **Tailwind v4 (2025-01 stable → v4.1 2025-04 → 2026-Q1 표준)**: CSS-first 설정 (`tailwind.config.js` 대체), `@import "tailwindcss";` + `@theme { --color-primary: oklch(...); }` directive. **OKLCH P3 컬러 팔레트가 기본값**. Container Queries 내장 (`@container` + `@sm:`/`@md:` 유틸, 플러그인 불필요). Oxide engine (Rust 기반) 10배 빠른 빌드. `@tailwindcss/vite` 플러그인 필수. 적용: react-init globals.css 템플릿 재작성.
- **shadcn/ui v2 + Tailwind v4 + React 19 (CLI v4 2026-03)**: CLI 완전 개편, `components.json` 의 `tailwind.config` v4 에서 공란, `registry:base` 타입 추가 (디자인 시스템 전체 단일 페이로드 배포), fonts first-class, `--dry-run`/`--diff`/`--view` 플래그, **React 19 ref-as-prop 반영**. 적용: react-init shadcn init 명령.
- **Vite 8 (Rolldown, 2026-03-12)**: Vite 6 Environment API → Vite 7 → **Vite 8 Rolldown 단일 Rust 번들러**. 10~30배 빠른 빌드. `pnpm create vite@latest` 템플릿이 Vite 8 을 받음. Environment API 는 framework authors 전용. 적용: react-init.
- **Zustand v5 (2024-11 stable)**: React 18 최소 (use-sync-external-store shim 제거, native `useSyncExternalStore` 사용). **객체 selector trap 심각화** — selector 가 매번 새 객체 반환하면 `Maximum update depth exceeded` 로 컴포넌트 트리 unmount. **해결: `useShallow` 강제**. equality function 커스터마이징 불가 — 필요 시 `createWithEqualityFn` (from `zustand/traditional`). 적용: react-store Gotchas + 템플릿 (`useShallow` + `use<Feature>Slice` 패턴).
- **TanStack Query v5 (2023-10 stable, 2026 현재 5.6x)**: `invalidateQueries`, `cancelQueries`, `removeQueries`, `resetQueries`, `getQueriesData`, `setQueriesData`, `ensureQueryData`, `isFetching` 모두 **`{ queryKey, ...filters }` 단일 object 인자** 강제. `queryOptions()` 유틸로 queryKey / queryFn / select 재사용 객체. `select` 타입 추론 이슈 → `useQuery<TData, TError, TSelected>` 3 제네릭 명시가 안전. 적용: react-query Gotchas + 템플릿.
- **Lingui v5 (2024-11 stable)**: `@lingui/macro` 패키지 분리 — core 매크로 (`t`, `plural`, `select`, `selectOrdinal`, `defineMessage`, `msg`) 는 `@lingui/core/macro`, React 매크로 (`Trans`, `Plural`, `Select`, `SelectOrdinal`) 는 `@lingui/react/macro`. 기존 `@lingui/macro` deprecated. `<Trans id="custom" />` 빈 자식 패턴 behavior change → `message` prop 명시 필수. 적용: react-l10n (이미 반영) + react-audit 감지 룰 유지.
- **React Hook Form v7.71 + Zod v4 호환성 경고**: `@hookform/resolvers` 가 Zod v4 `ZodType` 시그니처 변경과 충돌 → `zodResolver` 타입 에러. **공식 workaround: `import { z } from 'zod/v3'`**. 제네릭 래퍼 (`type FormValues<T extends z.ZodType> = z.infer<T>`) 는 Zod v4 에서 unknown 추론 회귀. 직접 `z.infer<typeof Schema>` 만 허용. 적용: react-init Zod v4 Gotcha.
- **WCAG 2.2 SC 2.5.8 (24×24 CSS px)**: Target Size Minimum AA 기준. Phase 6 design-kit 정합성. 적용: react-widget / react-responsive / react-audit.
- **라이브러리 0개 원칙 강화**: Motion / framer-motion / dnd-kit / react-spring / react-transition-group **+ animate.css** 추가 금지. 기존 금지 목록 완화 없음. 적용: common-gotchas G2, react-audit Library Policy.

### 신규 스킬 갭 분석

| 제안 스킬 | 아키타입 | 근거 | 우선순위 | 상태 |
| --------- | -------- | ---- | -------- | ---- |
| `react-migrate` | 런북 | React 18 → 19 ref-as-prop 마이그레이션, Zustand v4 → v5 | 중간 | backlog |
| `react-view-transitions` | 코드 스캐폴딩 | Browser View Transitions API + React 통합 | 낮음 | backlog |

### 폐기 사유

- Context7 monthly quota 소진 → WebSearch fallback. 공식 URL 은 모두 확보.

### PR

- <https://github.com/joo6077/claude-plugins/pull/6>
