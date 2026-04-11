# Sprint Contract — Phase 10 Kaizen Research Mode (react-kit)

Feature: react-kit 21 스킬 + 3 에이전트 + references 를 2026 React 19 stable / TanStack Query v5 / Tauri 2 GA / Tailwind v4 (OKLCH) / shadcn v2 / Vite 8 (Rolldown) / Zustand v5 / Lingui v5 / Zod v4 / RHF 호환성 생태계 반영 카이젠
Created: 2026-04-11
Branch: kaizen/2026-04-11-research
Iteration: 1

## Context

Phase 1~9 완료 (commit 4587154 → 6cb8701). Phase 10은 react-kit 플러그인의 21개 스킬, 3 에이전트(widget-inspector-react, animation-architect-react, react-reviewer), 플러그인 references(common-gotchas, clean-arch-layout, result-patterns, project-detection, style-guide, wasm-catalog)를 2026 React 생태계 현실에 맞춰 갱신한다.

데이터 풀 §5 validate-plugin 스냅샷 — react-kit v0.1.0, 21 skills + 3 agents, V1~V7 OK. 회귀 금지 기준선.

§3 followup-2026-04-11 — react-kit 구 V6 1건은 이전 세션에서 해결됨. 이번 Phase는 description/triger 수준의 P2(V4 cross-kit) 는 Phase 5~9 결과와 이미 결합되어 추가 작업 없음.

Phase 6 (design-kit) 에서 도입된 **OKLCH 컬러(Tailwind v4 기본) / WCAG 2.2 신규 SC / DTCG / Container Queries / MD3 Expressive** 기준이 react-kit의 UI 스킬(react-widget / react-responsive / react-form / react-skeleton / react-animation)에도 정합적으로 반영되어야 한다.

외부 리서치 (2026-04-11, Context7 쿼터 소진으로 WebSearch fallback):

- **React 19 stable (2024-12-05)**: `useActionState`, `useOptimistic`, `useFormStatus`, `use()` hook 이 **production stable**. 2026-04 현재 19.2가 표준. Actions 패러다임으로 폼 제출/mutation이 재정의됨. **`forwardRef` deprecated 예고 — React 19에서 `ref`가 일반 prop으로 전달 가능**. 기존 `forwardRef` 컴포넌트는 warning 없이 동작하지만 새 코드는 `ref as prop` 패턴 권장. ([React v19 블로그](https://react.dev/blog/2024/12/05/react-19), [React 19 Actions vs Redux 2026](https://www.zignuts.com/blog/react-19-actions-vs-redux-2026), [React 19 new hooks deep dive](https://medium.com/@rohitkuwar/deep-dive-into-react-19-s-latest-hooks-use-useactionstate-useoptimistic-and-useformstatus-849395af9c11))

- **Tauri 2 GA (2024-10-02/08)**: Tauri 2.0 stable 출시 2024-10-08. 1.x 코어 기능 대부분이 **개별 플러그인으로 분리** (plugin-fs, plugin-dialog, plugin-shell, plugin-clipboard-manager, plugin-notification 등). 모바일 네이티브 API 1급 지원 (notifications, dialogs, NFC, barcode, biometric, clipboard, deep link). **v1 allowlist → ACL (capability) 체계**로 완전 전환. `src-tauri/capabilities/*.json` 에 identifier/description/windows/permissions 선언. **Beta→Stable 마이그레이션: 모든 core permission identifier 앞에 `core:` prefix 필수** (예: `core:default`, `core:event:default`) 또는 `core:default` 단일 permission 로 통합. v1→v2 `cargo tauri migrate` CLI 자동 파싱 지원. ([Tauri 2.0 stable 블로그](https://v2.tauri.app/blog/tauri-20/), [v1→v2 migration](https://v2.tauri.app/start/migrate/from-tauri-1/), [v2 beta→stable migration](https://v2.tauri.app/start/migrate/from-tauri-2-beta/), [Tauri capabilities](https://v2.tauri.app/security/capabilities/))

- **Tailwind CSS v4 (2025-01 stable → v4.1 2025-04 → 2026-Q1 표준)**: (1) **CSS-first 설정**: `tailwind.config.js` 대체. `@import "tailwindcss";` + `@theme { --color-primary: oklch(...); }` directive 로 토큰 정의. (2) **OKLCH P3 컬러 팔레트가 기본값** — 생성 CSS 변수가 OKLCH. `oklch()` 함수 직접 사용 가능. (3) **Container Queries 내장** — `@container` + `@sm:`/`@md:`/`@lg:` 유틸. 플러그인 불필요. (4) **Oxide engine** (Rust 기반) — 10배 빠른 빌드, `@tailwindcss/vite` 플러그인 필수. (5) 기존 `tailwind.config.ts` 는 `@config "./tailwind.config.ts"` directive 로 legacy bridge. ([Tailwind v4 announcement](https://tailwindcss.com/blog/tailwindcss-v4), [Tailwind v4 theme variables](https://tailwindcss.com/docs/theme), [Tailwind v4 container queries](https://www.sitepoint.com/tailwind-css-v4-container-queries-modern-layouts/), [Tailwind v4 complete guide 2026](https://devtoolbox.dedyn.io/blog/tailwind-css-v4-complete-guide))

- **shadcn/ui v2 + Tailwind v4 + React 19 (CLI v4 2026-03)**: (1) **CLI 완전 개편** — `pnpm dlx shadcn@latest init --template vite` 로 Vite 템플릿 스캐폴딩. (2) **components.json 의 `tailwind.config` 는 v4 에서 공란** 유지. (3) **registry:base** 타입 추가 — 디자인 시스템 전체(컴포넌트+토큰+폰트+CSS 변수)를 단일 페이로드로 배포. (4) **fonts 가 first-class registry type**. (5) `--dry-run`/`--diff`/`--view` 플래그 — 설치 전 미리보기. (6) **React 19 ref-as-prop** 반영 — 새 컴포넌트는 `forwardRef` 없이 `ref?: Ref<X>` prop 으로 설계. 기존 컴포넌트는 하위호환 유지. ([shadcn Tailwind v4](https://ui.shadcn.com/docs/tailwind-v4), [shadcn CLI v4 changelog 2026-03](https://ui.shadcn.com/docs/changelog/2026-03-cli-v4), [shadcn components.json](https://ui.shadcn.com/docs/components-json))

- **Vite 8 (Rolldown, 2026-03-12)**: Vite 6 (2024-11) Environment API 도입 → Vite 7 (2025-Q2) → **Vite 8 (2026-03-12) Rolldown 단일 Rust 번들러 통합**. 10~30배 빠른 빌드, 기존 플러그인 호환성 유지. 2026-04 현재 Vite 8 stable 이 권장. react-kit 은 **현재 `pnpm create vite@latest` 사용 — 해당 템플릿이 Vite 8 을 받음**. 기존 프로젝트 업그레이드 시 `pnpm add -D vite@latest` 만 필요. Environment API 는 framework authors 대상 — 일반 앱은 신경 쓸 필요 없음. ([Vite 8 blog](https://vite.dev/blog/announcing-vite8), [Vite 6 Environment API](https://vite.dev/blog/announcing-vite6), [What's new in ViteLand Jan 2026](https://voidzero.dev/posts/whats-new-jan-2026))

- **Zustand v5 (2024-11 stable)**: (1) **React 18 최소** — v5 는 use-sync-external-store shim 제거, 네이티브 `useSyncExternalStore` 사용. (2) **객체 selector trap 심각화** — v5 는 React 기본 동작에 맞춤. selector 가 매번 새 객체를 반환하면 `Maximum update depth exceeded` 로 컴포넌트 트리 unmount. **해결: `useShallow` 강제**. (3) **equality function 커스터마이징 불가** — `create()` 로는 커스텀 equality 설정 불가. 필요 시 `createWithEqualityFn` (from `zustand/traditional`) 사용. (4) **`createStore` vs `create` 혼동 금지** 유지. ([Zustand v5 announce](https://pmnd.rs/blog/announcing-zustand-v5/), [Zustand v5 migration](https://zustand.docs.pmnd.rs/reference/migrations/migrating-to-v5))

- **TanStack Query v5 (2023-10 stable, 2026 현재 5.6x)**: (1) **QueryClient 메서드 시그니처 통일** — `invalidateQueries`, `cancelQueries`, `removeQueries`, `resetQueries`, `getQueriesData`, `setQueriesData`, `ensureQueryData`, `isFetching` 모두 **`{ queryKey, ...filters }` 단일 object 인자**. 이전 복수 인자 형태 폐지. (2) **`queryOptions()` 유틸**로 queryKey/queryFn/select 를 재사용 가능한 객체로 분리 — `useQuery(userQueryOptions(id))`. (3) `select` 타입 추론 회귀 이슈 발생 이력(v5 초기) — `useQuery<TData, TError, TSelected>` 3개 제네릭 명시가 안전. (4) v4 codemod 제공 — 완전 자동화는 아니므로 수동 확인 권장. ([TanStack Query v5 migration](https://tanstack.com/query/v5/docs/react/guides/migrating-to-v5), [Query Invalidation v5](https://tanstack.com/query/v5/docs/react/guides/query-invalidation), [queryOptions+select type issue](https://github.com/TanStack/query/issues/5436))

- **Lingui v5 (2024-11 stable)**: **`@lingui/macro` 패키지 분리** — core 매크로(`t`, `plural`, `select`, `selectOrdinal`, `defineMessage`, `msg`)는 `@lingui/core/macro`, React 매크로(`Trans`, `Plural`, `Select`, `SelectOrdinal`)는 `@lingui/react/macro` 에서 import. 기존 `@lingui/macro` 는 deprecated (v5 에서도 alias 유지 but warning). JSX에서 `<Trans id="custom" />` 빈 자식 패턴은 v5 에서 behavior change — `message` prop 명시 필수 또는 fallback 처리. **react-audit 의 `@lingui/macro` deprecated 검출 룰은 유지/강화**. ([Lingui v5 migration](https://lingui.dev/releases/migration-5), [Lingui macro ref](https://lingui.dev/ref/macro), [Lingui v5 Trans 이슈](https://github.com/lingui/js-lingui/discussions/2220))

- **React Hook Form v7.71 + Zod v4 호환성 경고**: 2026-04 현재 `react-hook-form@7.71.x`, `zod@4.3.x` 기준. **`@hookform/resolvers` 는 Zod v4 TypeScript 타입 호환성 미해결** — `@hookform/resolvers/zod` 의 `zodResolver` 가 Zod v4 의 `ZodType` 시그니처 변경과 충돌해 타입 에러 발생 가능. **공식 workaround: `import { z } from 'zod/v3'`** (Zod v4 패키지에서 v3 알리아스 노출) 또는 `@hookform/resolvers` 의 resolver 업데이트 대기. v4 beta 에서 `ZodError`가 `formState.errors` 경유 없이 throw 되던 이슈는 stable 4.1.x+ 에서 수정됨. **제네릭 래퍼(`type FormValues<T extends z.ZodType> = z.infer<T>`)는 Zod v4 에서 unknown 으로 추론되는 회귀 이슈 — 직접 `z.infer<typeof Schema>`만 허용**. RHF setError 패턴: `setError('root.serverError', { type: 'server', message })`, 필드 단위는 `setError(field, { type: 'server', message })`. ([@hookform/resolvers Zod v4 이슈 #813](https://github.com/react-hook-form/resolvers/issues/813), [RHF Zod v4 resolver 요청 #12829](https://github.com/react-hook-form/react-hook-form/issues/12829), [ZodError not captured in formState #12816](https://github.com/react-hook-form/react-hook-form/issues/12816))

- **WCAG 2.2 신규 SC (Phase 6 정합)**: (1) **SC 2.5.8 Target Size (Minimum) Level AA** — 인터랙티브 타겟 최소 24×24 CSS 픽셀 (예외: inline 텍스트, `user-agent` 기본 컨트롤). 기존 AAA 44×44 SC 2.5.5 와 별개. (2) **SC 2.4.11 Focus Not Obscured (Minimum) AA** / **SC 2.4.12 Focus Not Obscured (Enhanced) AAA** — sticky header, 모달, 툴팁에 의해 focus ring 이 완전히 가려지면 FAIL. Tailwind `scroll-mt-*` / `scroll-padding-top` 처리 필요. (3) **SC 2.5.7 Dragging Movements AA** — 드래그 동작에 대안 single-pointer 경로 필수 (드래그로만 도달 가능한 기능 금지). react-animation Tier 3 드래그 컴포넌트에 직접 적용됨. (4) **SC 3.3.8 Accessible Authentication AA** — cognitive function test (퍼즐, 캡차) 없이 로그인 가능해야 함. react-form 로그인 패턴 관련.

## Contract Conditions

각 조건은 APPROVE 판정을 위한 필수 항목이다. 구현 중 조건을 수정해야 하면 Iteration 을 증가시키고 사용자에게 알린다.

### A. react-init 스킬 업데이트 (A-01 ~ A-06)

- **A-01**: `react-init/SKILL.md` Gotchas 섹션에 Vite 8 Rolldown 관련 항목 추가 — "pnpm create vite@latest 는 2026-04 기준 Vite 8 템플릿을 받는다"는 사실과 기존 vite 6/7 프로젝트 업그레이드 명령(`pnpm add -D vite@latest`) 명시.
- **A-02**: `react-init/SKILL.md` Gotchas 섹션에 React 19 stable (2024-12, 2026 19.2+) + forwardRef deprecation 예고 항목 추가. 새 컴포넌트는 `ref as prop` 패턴, 기존 컴포넌트는 하위호환 명시.
- **A-03**: `react-init/SKILL.md` 단계 3 (Tailwind v4) 에 `@theme` directive + OKLCH 예시 포함한 `globals.css` 템플릿 확장. 최소 예시:

  ```css
  @import "tailwindcss";

  @theme {
    --color-primary: oklch(0.72 0.19 250);
    --color-accent: oklch(0.78 0.15 60);
  }
  ```

  한국어/영어 주석으로 "OKLCH 는 Tailwind v4 기본이며 Phase 6 design-kit 토큰과 정합"을 명시.

- **A-04**: `react-init/SKILL.md` 단계 10 (Tauri 2) 에 Tauri 2 GA (2024-10) + v1→v2 `cargo tauri migrate` CLI + `core:default` permission prefix 규칙 명시. `src-tauri/capabilities/default.json` 예시는 `"core:default"` 포함.
- **A-05**: `react-init/SKILL.md` 단계 7 (Lingui) 에 v5 매크로 split 명시 — `@lingui/core/macro` vs `@lingui/react/macro`, `@lingui/macro` deprecated. 설치 명령도 `@lingui/core` + `@lingui/react` 는 runtime, `@lingui/cli` + `@lingui/vite-plugin` + `@lingui/swc-plugin` 은 devDependency 임을 분리.
- **A-06**: `react-init/SKILL.md` Gotchas 섹션에 **Zod v4 + @hookform/resolvers TS 호환성 이슈** 항목 추가 — workaround (`zod/v3` 알리아스 임포트 또는 resolver 업데이트 확인), 영향 범위(`/react-form` 에서 발생), 감지 방법(`pnpm tsc --noEmit` 시 zodResolver 타입 에러) 명시.

### B. react-store 스킬 업데이트 (B-01 ~ B-02)

- **B-01**: `react-store/SKILL.md` Gotchas 에 **Zustand v5 객체 selector trap + `useShallow` 강제** 항목 추가. bad/good 예시 포함:
  - bad: `const { user, token } = useAuthStore((s) => ({ user: s.user, token: s.token }))`
  - good: `import { useShallow } from 'zustand/react/shallow'` / `const [user, token] = useAuthStore(useShallow((s) => [s.user, s.token]))`
- **B-02**: `react-store/SKILL.md` Process 단계에 `useShallow` import 경로(`zustand/react/shallow`) 와 다중 필드 구독 패턴 생성 규칙 추가. Zustand v5 최소 React 18 요건 명시.

### C. react-query 스킬 업데이트 (C-01 ~ C-02)

- **C-01**: `react-query/SKILL.md` Gotchas 에 **TanStack Query v5 QueryClient 메서드 시그니처 object-form 강제** 항목 추가. bad/good:
  - bad: `queryClient.invalidateQueries(userKeys.list)`
  - good: `queryClient.invalidateQueries({ queryKey: userKeys.list })`
- **C-02**: `react-query/SKILL.md` Gotchas 에 **`queryOptions()` 유틸 + `select` 제네릭 3개 명시 권장** 항목 추가. v5 초기 type inference 회귀 이슈를 피하기 위해 `useQuery<TData, TError, TSelected>` 3제네릭 명시 + `queryOptions` 사용 시에는 `const opts = queryOptions({...})` 패턴 명시.

### D. react-widget 스킬 업데이트 (D-01 ~ D-03)

- **D-01**: `react-widget/SKILL.md` Gotchas 에 **React 19 `ref as prop` 권장** 항목 추가. `forwardRef` 사용은 허용(하위호환) 하되, **신규 생성 컴포넌트 템플릿은 `ref?: Ref<X>` prop 패턴**으로 교체. bad/good:
  - bad (legacy): `React.forwardRef<HTMLButtonElement, Props>((props, ref) => ...)`
  - good (React 19+): `function Button({ ref, ...props }: Props & { ref?: Ref<HTMLButtonElement> }) { ... }`
- **D-02**: `react-widget/SKILL.md` Process 단계 5 의 코드 템플릿을 `ref as prop` 패턴으로 갱신. 기존 forwardRef 템플릿은 "React 18 이하 호환이 필요할 때만" 주석 추가.
- **D-03**: `react-widget/SKILL.md` Gotchas 에 **WCAG 2.2 SC 2.5.8 터치타겟 최소 24×24** 항목 추가. 인터랙티브 variant(button, icon-button) 는 `min-h-6 min-w-6` 또는 `h-10`(40px) 이상 권장, `size: 'sm'` 도 24px 미만 금지.

### E. react-responsive 스킬 업데이트 (E-01)

- **E-01**: `react-responsive/SKILL.md` Gotchas 에 **breakpoint 전환 시 터치타겟 24×24 유지 (WCAG 2.2 SC 2.5.8)** 항목 추가. 좁은 화면에서 icon-only 로 축소할 때 `min-w-6 min-h-6` 가드 필수.

### F. react-audit 스킬 업데이트 (F-01 ~ F-03)

- **F-01**: `react-audit/SKILL.md` Library Policy 카테고리 금지 라이브러리 목록에 **`animate.css`** 추가 (common-gotchas G2 정합). grep 패턴도 갱신:

  ```text
  ^import .* from ['"](motion|framer-motion|react-spring|@dnd-kit\/[^'"]*|react-dnd[^'"]*|react-beautiful-dnd|react-transition-group|gsap|lottie-react|@formkit\/auto-animate[^'"]*|animate\.css)['"]
  ```

- **F-02**: `react-audit/SKILL.md` Accessibility 카테고리에 **WCAG 2.2 SC 2.5.8 터치타겟 24×24 검사** 항목 추가 (⚠️ 경고 수준). 인터랙티브 요소(button, a, input[type=button], [role=button])의 Tailwind size 유틸(`h-*`, `w-*`, `size-*`, `min-h-*`, `min-w-*`)에서 6(24px) 미만이면 경고.
- **F-03**: `react-audit/SKILL.md` Library Policy 카테고리에 **`@lingui/macro` 직접 import 는 ⚠️ 경고 (v5 split 에서 deprecated)** 항목 추가. 기존 항목이 있으면 유지/강화.

### G. references/common-gotchas.md 업데이트 (G-01)

- **G-01**: `references/common-gotchas.md` G2 Library Policy 금지 목록을 Phase 10 리서치 결과와 정합화 — `animate.css` 포함 유지, `@formkit/auto-animate` 유지, 리스트 끝에 `<!-- Phase 10 재확인: 2026-04-11 -->` 주석 추가.

### H. 회귀/빌드 안전 (H-01 ~ H-04)

- **H-01**: `python3 scripts/validate-plugin.py` 전체 실행 결과 **7개 킷 모두 OK** (이전 baseline 유지).
- **H-02**: `python3 scripts/sync-docs.py --check-only` 실행 시 변경 필요 없음 또는 sync-docs 스크립트가 자동 재기록 후 commit 에 포함.
- **H-03**: Phase 1~9 소유 파일 (harness/, flutter-toolkit/, design-kit/, backend-kit/, infra-kit/, rust-kit/) 수정 0건. 오직 react-kit/** 만 수정.
- **H-04**: **react-kit/skills/react-animation/SKILL.md / agents/animation-architect-react.md / skills/react-audit/SKILL.md 의 라이브러리 0개 원칙 완화 0건** — 기존 금지 라이브러리 삭제/약화 금지. 추가만 허용. Gotcha 본문에서 "허용" 또는 "예외" 키워드 새로 등장하면 REJECT.

### I. 리서치 출처 추적 (I-01 ~ I-02)

- **I-01**: 수정하는 각 Gotcha/주석에 리서치 출처가 드러나도록 짧은 notation 포함 — 예: `(Zustand v5 announce)`, `(Tauri 2 stable 2024-10)`, `(Tailwind v4 theme)`. Sprint Contract context 의 URL 리스트와 매칭 가능해야 한다.
- **I-02**: commit message 에 최소 5개 리서치 URL 포함. 형식: `kaizen(phase10-research): react-kit 2026 React 19/TanStack v5/Tauri 2 GA/Tailwind v4/Zustand v5/Lingui v5 반영` 본문에 URL.

## Scope

### 수정 대상 (react-kit 만)

- `react-kit/skills/react-init/SKILL.md` — A-01~A-06
- `react-kit/skills/react-store/SKILL.md` — B-01~B-02
- `react-kit/skills/react-query/SKILL.md` — C-01~C-02
- `react-kit/skills/react-widget/SKILL.md` — D-01~D-03
- `react-kit/skills/react-responsive/SKILL.md` — E-01
- `react-kit/skills/react-audit/SKILL.md` — F-01~F-03
- `react-kit/references/common-gotchas.md` — G-01

### 수정 금지

- `harness/**`, `flutter-toolkit/**`, `design-kit/**`, `backend-kit/**`, `infra-kit/**`, `rust-kit/**`
- `react-kit/.claude-plugin/plugin.json` (Final Phase 에서 버전 bump)
- `.harness/project.yaml`, `.harness/.meta/**`
- `.claude/skills/**`, `docs/**`

## Rollback

조건 불충족 시 수정 파일 전부 rollback:

```bash
git checkout react-kit/skills/react-init/SKILL.md react-kit/skills/react-store/SKILL.md react-kit/skills/react-query/SKILL.md react-kit/skills/react-widget/SKILL.md react-kit/skills/react-responsive/SKILL.md react-kit/skills/react-audit/SKILL.md react-kit/references/common-gotchas.md
```

## Self-audit

QA Evaluator(L3) 기준 자기진단:

1. 각 조건 A~I 를 수정 파일 grep 으로 검증
2. validate-plugin.py 전체 실행 — 7 OK 확인
3. sync-docs.py --check-only — 무변경 또는 auto-sync commit
4. git log --oneline -n 3 — 본 Phase commit 만 추가됐는지 확인
5. git diff --stat main..HEAD — Phase 1~9 소유 파일 0건 확인

판정 기준: 22개 조건 중 20개 이상 PASS → APPROVE. 18개 이하 PASS → REJECT iter+1.
