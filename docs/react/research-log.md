---
version: 1.2.0
last_updated: 2026-07-27
---

# React Kit Research Log

## [2026-07-27] - Phase 10 kaizen

신호 농도 **LOW** (사용자 외부 프로젝트 React/Tauri 사용 흔적 0건). 억지 개선 대신 **상위 Phase 가
남긴 하위 전파 지시 3 건 + Phase 4 정정 1 건**만 이행했다.

### 조회한 1차 출처

Context7 MCP 가 OAuth 미인증으로 호출 불가 → WebFetch 로 공식 문서 직접 조회.

| # | URL | 확인한 사실 | 반영 위치 |
|---|-----|------------|----------|
| 1 | <https://testing-library.com/docs/queries/about/> | `queryBy*` 는 매치 없을 때 `null`, `queryAllBy*` 는 빈 배열 `[]` 반환하고 throw 하지 않음. 문서가 `queryBy` 를 "asserting an element that is not present" 용도로 권장 | `render-evidence-protocol.md` §3 (a) · `react-test` Gotcha 11 · `react-skeleton` Gotcha 9 |
| 2 | <https://vitest.dev/guide/cli.html> | `--passWithNoTests` = "Pass when no tests are found", 기본 `false`. `allowOnly` 기본값 `!process.env.CI`. `bail` 기본 `0` | `render-evidence-protocol.md` §3 (b)(c) · `react-test` Gotcha 12 |
| 3a | <https://vitest.dev/config/passwithnotests> | `passWithNoTests` — Type `boolean` · **Default `false`** · CLI `--passWithNoTests` · "Vitest will not fail, if no tests will be found." | 위와 동일 (기본값 1차 확인) |
| 3b | <https://vitest.dev/config/allowonly> | `allowOnly` — Type `boolean` · **Default `!process.env.CI`** · "in local development environments, Vitest allows these tests to run" | 위와 동일 (기본값 1차 확인) |
| 4 | <https://playwright.dev/docs/test-snapshots> | `toHaveScreenshot()` 은 baseline 부재 시 실제 화면을 golden 으로 기록. `--update-snapshots` 로 갱신. `maxDiffPixels` / `stylePath` 옵션 | `render-evidence-protocol.md` §3 (d) · `react-test` Gotcha 13 · `react-animation` Gotcha 13 |
| 5 | <https://playwright.dev/docs/test-assertions> | auto-retrying assertion 권장, 복잡한 경우 `expect.poll` / `expect.toPass`. non-retrying assertion 은 flaky 유발 | `render-evidence-protocol.md` §2 증거 등급 R1 |
| 6 | <https://tanstack.com/query/latest/docs/framework/react/guides/query-invalidation> | `invalidateQueries` 는 **prefix 매칭이 기본** — `['todos']` 무효화가 `['todos', { page: 1 }]` 까지 포함. `exact: true` / predicate 로 좁힘. **queryKey 팩토리 정합성 가이드는 공식 문서에 없음** | `react-query` Gotcha 15 (Counterpart Enumeration) |

### 반영 내역

- **CP (Canonical Protocol 전파)** — Phase 3 `qa-evaluation-guide.md` v4.0 이 남긴 하위 전파 지시.
  실측상 `grep -rn "미검증" react-kit/` 이 **0 hit** 이었다 (reviewer 6 종 중 react 만 미이행).
  `react-reviewer` 에 §Canonical Unverified-Evidence Protocol 5 조항을 문구 변형 없이 복제하고,
  §Evidence Validity Gate 4 검사를 react 도구 문맥(0 매치 판정·스코프 파일 수)으로 매핑했다.
  출력 포맷에 `unverified` 집계 필드 추가, `react-audit` 에 수신면(`🔍 미검증` 섹션 + 임계 2 건 규칙) 추가.
- **EV (렌더 증거 규약)** — Phase 3 이 "UI 를 다루는 design/react/flutter 계열이 가장 직접
  매핑된다" 고 지정. react-kit UI 스킬 5 종의 검증 섹션이 `Strict TS 검증` 하나뿐이었다.
  `react-kit/references/render-evidence-protocol.md` 신설(E2) 후 `react-screen` · `react-widget` ·
  `react-skeleton` · `react-responsive` · `react-animation` 5 종 전수 + `react-test` 에 연결.
  Phase 5 flutter `visual-evidence-protocol.md` · Phase 6 design `visual-change-protocol.md` 와
  동일 계열이며 임계값·마커·등급을 재정의하지 않고 상위 SSOT 를 인용만 한다.
- **CE (Counterpart Enumeration)** — Phase 1 `skill-design-guide.md` §5.5. 실측상
  `grep -rn "Counterpart\|양면" react-kit/` 이 **0 hit**. 기존 Enumerate-before-Act 9 스킬은
  producer 자기 레이어 스캔이라 반대 방향을 못 덮는다. `react-api`(스키마·DTO·에러 kind 소비면)와
  `react-query`(queryKey 팩토리 → invalidation 호출부)에 E2 로 추가.
- **KZ** — `.claude/skills/react-kaizen/SKILL.md` 의 "7 카테고리" → 8 (V1~V8) 정정 + 체크 표 추가,
  계약 경로를 병렬 안전한 `.harness/history/` 로 변경, Context7 실패 시 WebFetch fallback 명문화,
  범위 기준을 파일 수 → unit(관심사) 수로 교정.

### Library Policy

**완화 0 건.** 금지 라이브러리 12 항목 언급 수가 작업 전 baseline 이상을 유지하고,
`❌ FAIL` → `⚠️ WARN` 재분류 0 건. `react-animation` Gotcha 13 에는 "증거 확보를 위해
애니메이션 라이브러리를 도입하지 않는다 — Library Policy 가 이 규약보다 상위" 를 명시해
새 규약이 우회 통로가 되지 않도록 막았다.

### 하지 않은 것

- Counterpart Conditions 의 evaluator 측 대응 절 — Phase 3 parity item 12 의 **의도된 부재**.
- 새 스킬/에이전트 신설, `react-audit` 카테고리 7 개 확장 (미검증은 카테고리가 아니라 리포트 축).
- 기존 Enumerate-before-Act 9 스킬 가드 재작성 (직전 사이클 승격분 · 중복 금지).

---

## [2026-06-05] — Phase 10 kaizen

생성형 9스킬에 §5.5 Enumerate-before-Act + scope 가드 전수 보강(0/9→9/9). U+FFFD 4곳 복구. Library Policy 완화 0건.

출처: skill-design-guide §5.5, insights 2026-06-04 Friction #1·#3.


> react-kaizen 실행 시 리서치한 외부 소스와 채택 여부를 누적 기록한다.

## [2026-05-07] — Phase 10 kaizen (react, /insights 흡수)

### 데이터 소스

- 데이터 풀 §0 `/insights` 30 일 분석 (3 friction · 3 pattern · 3 feature)
- `harness/references/cross-kit-principles.md` v1 매트릭스의 react 열

### Phase 10 변경

- react/README.md 에 cross-kit-principles 매트릭스 cross-reference 섹션 추가
- plugin.json patch bump (이번 사이클)
- 매핑: react-audit ANALYZE ↔ Pre-Edit Batch Audit, react-reviewer self-check ↔ Self-Evaluator Audit, PostToolUse 정적 검증 ↔ Hook-Triggered Auto-Correction

### 외부 리서치 인용 (이전 사이클 보존, 이번 사이클 추가 없음)

이전 카이젠 사이클의 리서치 인용은 본 로그 하단 + cross-kit-principles 매트릭스로 보존된다.

---


---

## 2026-04-12

**트리거:** react-research 스킬 (연구 범위 확대 — 15개 카테고리)

### 조사한 소스

| # | 제목 | URL | 유형 | 태그 | 결과 |
| - | ---- | --- | ---- | ---- | ---- |
| 23 | React Compiler v1.0 blog | <https://react.dev/blog/2025/10/07/react-compiler-1> | 공식 | [official] [dated: 2025-10] | 채택 |
| 24 | React 19.2 release blog | <https://react.dev/blog/2025/10/01/react-19-2> | 공식 | [official] [dated: 2025-10] | 채택 |
| 25 | React versions page | <https://react.dev/versions> | 공식 | [official] | 참조 |
| 26 | Vite 8.0 announcement | <https://vite.dev/blog/announcing-vite8> | 공식 | [official] [dated: 2026-03] | 채택 |
| 27 | Vite 8 Beta (Rolldown) announcement | <https://vite.dev/blog/announcing-vite8-beta> | 공식 | [official] [dated: 2026-02] | 참조 |
| 28 | Vite 7.0 announcement | <https://vite.dev/blog/announcing-vite7> | 공식 | [official] [dated: 2025-06] | 참조 |
| 29 | Vite 8 Rolldown 10-30x faster (The Register) | <https://www.theregister.com/2026/03/16/vite_8_rolldown/> | 뉴스 | [blog] [dated: 2026-03] | 참조 |
| 30 | Tauri v2 IPC concept | <https://v2.tauri.app/concept/inter-process-communication/> | 공식 | [official] | 채택 |
| 31 | Tauri v2 security capabilities | <https://v2.tauri.app/security/> | 공식 | [official] | 채택 |
| 32 | TanStack Router file-based routing docs | <https://tanstack.com/router/latest/docs/routing/file-based-routing> | 공식 | [official] | 채택 |
| 33 | TanStack Router file-based routing API ref | <https://tanstack.com/router/latest/docs/api/file-based-routing> | 공식 | [official] | 참조 |
| 34 | TanStack Router vs React Router v7 (2026) | <https://www.pkgpulse.com/blog/tanstack-router-vs-react-router-v7-2026> | 블로그 | [blog] [dated: 2026-01] | 참조 |
| 35 | TanStack Query v5 optimistic updates | <https://tanstack.com/query/v5/docs/react/guides/optimistic-updates> | 공식 | [official] | 채택 |
| 36 | TanStack Query v5 prefetching guide | <https://tanstack.com/query/v5/docs/framework/react/guides/prefetching> | 공식 | [official] | 채택 |
| 37 | Zustand v5 migration guide | <https://zustand.docs.pmnd.rs/reference/migrations/migrating-to-v5> | 공식 | [official] | 채택 (이전 #15 보완) |
| 38 | Zustand devtools middleware docs | <https://zustand.docs.pmnd.rs/reference/middlewares/devtools> | 공식 | [official] | 채택 |
| 39 | Zustand slices pattern (DeepWiki) | <https://deepwiki.com/pmndrs/zustand/7.1-slices-pattern> | 위키 | [blog] | 참조 |
| 40 | shadcn/ui changelog | <https://ui.shadcn.com/docs/changelog> | 공식 | [official] | 참조 |
| 41 | shadcn/ui Luma (March 2026) | <https://ui.shadcn.com/docs/changelog/2026-03-luma> | 공식 | [official] [dated: 2026-03] | 채택 |
| 42 | shadcn/ui October 2025 new components | <https://ui.shadcn.com/docs/changelog/2025-10-new-components> | 공식 | [official] [dated: 2025-10] | 참조 |
| 43 | Tailwind v4 complete guide (DevToolbox) | <https://devtoolbox.dedyn.io/blog/tailwind-css-v4-complete-guide> | 블로그 | [blog] [dated: 2026-01] | 참조 |
| 44 | Tailwind v4 container queries (SitePoint) | <https://www.sitepoint.com/tailwind-css-v4-container-queries-modern-layouts/> | 블로그 | [blog] [dated: 2025-04] | 채택 (이전 #9 재검증) |
| 45 | TypeScript 5.8 announcement | <https://devblogs.microsoft.com/typescript/announcing-typescript-5-8/> | 공식 | [official] [dated: 2025-03] | 채택 |
| 46 | TypeScript 5.9 new features (2026) | <https://www.digitalapplied.com/blog/typescript-5-9-new-features-developer-guide-2026> | 블로그 | [blog] [dated: 2026-01] | 참조 |
| 47 | TS strict mode guide (2026) | <https://www.mariorafaelayala.com/blog/typescript-strict-mode-2026> | 블로그 | [blog] [dated: 2026-02] | 참조 |
| 48 | Sunsetting rustwasm GitHub org | <https://blog.rust-lang.org/inside-rust/2025/07/21/sunsetting-the-rustwasm-github-org/> | 공식 | [official] [dated: 2025-07] | 채택 |
| 49 | Life after wasm-pack (nickb.dev) | <https://nickb.dev/blog/life-after-wasm-pack-an-opinionated-deconstruction/> | 블로그 | [blog] [dated: 2025-09] | 채택 |
| 50 | wasm-bindgen new org (GitHub) | <https://github.com/wasm-bindgen/wasm-bindgen> | github | [official] | 채택 |
| 51 | Rust & WASM in 2026 (DEV Community) | <https://dev.to/dataformathub/rust-wasm-in-2026-a-deep-dive-into-high-performance-web-apps-20c6> | 블로그 | [blog] [dated: 2026-01] | 참조 |
| 52 | Lingui v5 migration guide | <https://lingui.dev/releases/migration-5> | 공식 | [official] | 채택 (이전 #19 보완) |
| 53 | Lingui macro reference | <https://lingui.dev/ref/macro> | 공식 | [official] | 채택 (이전 #20 보완) |
| 54 | View Transitions API (MDN) | <https://developer.mozilla.org/en-US/docs/Web/API/View_Transition_API> | 공식 | [official] | 채택 |
| 55 | View Transitions in 2025 (Chrome blog) | <https://developer.chrome.com/blog/view-transitions-in-2025> | 공식 | [official] [dated: 2025-10] | 채택 |
| 56 | View Transitions in React (Medium) | <https://medium.com/@creolestudios/view-transitions-in-react-how-to-build-smooth-page-transitions-without-spa-headaches-48f1dca22176> | 블로그 | [blog] [dated: 2025-08] | 참조 |
| 57 | CSS scroll-driven animations (MDN) | <https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Scroll-driven_animations> | 공식 | [official] | 채택 |
| 58 | Scroll-driven + @starting-style 조합 (Bram.us) | <https://www.bram.us/2025/11/06/combining-scroll-driven-animations-with-starting-style/> | 블로그 | [blog] [dated: 2025-11] | 채택 |
| 59 | CSS scroll-triggered animations (Chrome blog) | <https://developer.chrome.com/blog/scroll-triggered-animations> | 공식 | [official] [dated: 2026-03] | 채택 |
| 60 | 4 CSS features for 2026 (nerdy.dev) | <https://nerdy.dev/4-css-features-every-front-end-developer-should-know-in-2026> | 블로그 | [blog] [dated: 2026-01] | 참조 |
| 61 | Vitest browser component testing | <https://vitest.dev/guide/browser/component-testing> | 공식 | [official] | 채택 |
| 62 | Vitest vs Jest vs Playwright (2026) | <https://www.pkgpulse.com/blog/testing-libraries-compared> | 블로그 | [blog] [dated: 2026-02] | 참조 |
| 63 | Vitest vs Jest 30: browser-native testing | <https://dev.to/dataformathub/vitest-vs-jest-30-why-2026-is-the-year-of-browser-native-testing-2fgb> | 블로그 | [blog] [dated: 2026-01] | 참조 |
| 64 | RHF + Zod v4 type-safe forms (Tecktol) | <https://tecktol.com/zod-react-hook-form/> | 블로그 | [blog] [dated: 2026-02] | 참조 |
| 65 | RHF resolvers GitHub (Standard Schema) | <https://github.com/react-hook-form/resolvers> | github | [official] | 채택 |
| 66 | neverthrow GitHub | <https://github.com/supermacro/neverthrow> | github | [official] | 참조 |
| 67 | neverthrow tutorial (DJ NUO) | <https://dj-nuo.com/blog/2025/10/08/neverthrow-tutorial/> | 블로그 | [blog] [dated: 2025-10] | 참조 |
| 68 | @vitejs/plugin-react v6 (Oxc transforms) | <https://vite.dev/blog/announcing-vite8> | 공식 | [official] [dated: 2026-03] | 채택 |
| 69 | React `useEffectEvent` reference | <https://react.dev/reference/react/useEffectEvent> | 공식 | [official] | 참조 |
| 70 | React `<Activity />` reference | <https://react.dev/reference/react/Activity> | 공식 | [official] | 참조 |
| 71 | React Compiler incremental adoption | <https://react.dev/learn/react-compiler/incremental-adoption> | 공식 | [official] | 채택 |
| 72 | React Conf 2025 recap | <https://react.dev/blog/2025/10/16/react-conf-2025-recap> | 공식 | [official] [dated: 2025-10] | 채택 |
| 73 | React Compiler and Sanity | <https://www.sanity.io/help/react-compiler> | 공식 | [official] [dated: 2025-11] | 채택 |
| 74 | Sanity v3.65.0 compiler benchmark | <https://www.sanity.io/docs/changelog/839f4b18-788b-4e83-b5d9-8cb838a5be9e> | 공식 | [official] [dated: 2024-11] | 채택 |
| 75 | Vite migration from v7 | <https://vite.dev/guide/migration> | 공식 | [official] | 채택 |
| 76 | Vite Rolldown integration guide | <https://vite.dev/guide/rolldown> | 공식 | [official] | 채택 |
| 77 | Tauri Stronghold plugin | <https://v2.tauri.app/plugin/stronghold/> | 공식 | [official] | 채택 |
| 78 | Tauri Updater plugin | <https://v2.tauri.app/plugin/updater/> | 공식 | [official] | 채택 |
| 79 | Tauri Deep Linking plugin | <https://v2.tauri.app/plugin/deep-linking/> | 공식 | [official] | 채택 |
| 80 | Tauri deep-link JS reference | <https://v2.tauri.app/reference/javascript/deep-link/> | 공식 | [official] | 참조 |
| 81 | TanStack Start overview | <https://tanstack.com/start/docs/docs> | 공식 | [official] | 채택 |
| 82 | TanStack Start homepage stats | <https://tanstack.com/start/> | 공식 | [official] | 참조 |
| 83 | React Router releases/changelog | <https://reactrouter.com/start/start/changelog> | 공식 | [official] | 채택 |
| 84 | Storybook 9.0 release page | <https://storybook.js.org/releases/9.0> | 공식 | [official] [dated: 2025-06] | 채택 |
| 85 | Storybook Autodocs docs | <https://storybook.js.org/docs/writing-docs/autodocs> | 공식 | [official] | 채택 |
| 86 | Astro React integration | <https://docs.astro.build/en/guides/integrations-guide/react/> | 공식 | [official] | 채택 |
| 87 | Astro islands architecture | <https://docs.astro.build/en/concepts/islands/> | 공식 | [official] | 채택 |
| 88 | State of React 2025 component libraries | <https://2025.stateofreact.com/en-US/libraries/component-libraries/> | 공식 | [official] | 채택 |
| 89 | State of CSS 2025 other tools | <https://2025.stateofcss.com/es-ES/other-tools/> | 공식 | [official] | 채택 |
| 90 | Custom Elements Everywhere | <https://custom-elements-everywhere.com/> | 공식 | [official] | 채택 |
| 91 | TC39 proposal-signals | <https://github.com/tc39/proposal-signals> | github | [official] | 채택 |
| 92 | React issue: Signal & Observable | <https://github.com/facebook/react/issues/30570> | github | [official] | 채택 |
| 93 | Waku homepage | <https://waku.gg/> | 공식 | [official] | 채택 |
| 94 | Waku npm package | <https://www.npmjs.com/package/waku> | npm | [official] | 참조 |
| 95 | Deno Fresh 2 beta + Vite | <https://deno.com/blog/fresh-and-vite> | 공식 | [official] [dated: 2025-09] | 채택 |
| 96 | Deno Deploy React app with Vite | <https://docs.deno.com/deploy/tutorials/vite/> | 공식 | [official] | 채택 |
| 97 | Million docs installation | <https://million.dev/docs> | 공식 | [official] | 채택 |
| 98 | Million homepage pivot | <https://million.dev/> | 공식 | [official] | 채택 |
| 99 | Million GitHub repo releases | <https://github.com/aidenybai/million> | github | [official] | 채택 |

### 채택한 인사이트

#### React 19.2 + Compiler v1.0

- **React 19.2 (2025-10-01)**: `<Activity />` 컴포넌트 (visible/hidden 모드로 pre-rendering), `useEffectEvent` hook (Effect 의존성에서 이벤트 로직 분리), `cacheSignal` (Server Components 전용 cleanup), Chrome DevTools Performance Tracks (Scheduler + Components 트랙). `useId` prefix가 `:r:` → `_r_` 로 변경 — View Transitions + XML 1.0 호환성 확보. Suspense boundary reveal 배칭 개선. `eslint-plugin-react-hooks` v6 flat config 기본 + Compiler lint 통합. 적용: react-init, react-widget, react-store Gotchas 갱신.
- **React Compiler v1.0 (2025-10-07)**: 자동 메모이제이션 빌드 타임 도구. React 17+ 호환. Meta 프로덕션 검증 (초기 로드 12% 개선, 특정 인터랙션 2.5배 속도 향상, 메모리 중립). Expo SDK 54+, Vite (`create-vite`), Next.js (`create-next-app`) 에서 기본 활성화. **주의**: 정확한 버전 핀 권장 (`1.0.0`, `^1.0.0` 아님) — 메모이제이션 변경이 `useEffect` 동작에 영향 가능. Oxc/Rolldown 지원 계획 중. 적용: react-init `babel-plugin-react-compiler` 추가, react-build 파이프라인 갱신.

#### Vite 8 Rolldown

- **Vite 8.0 (2026-03-12)**: esbuild + Rollup 이중 번들러 → **Rolldown 단일 Rust 번들러** 통합. 10-30x 빠른 빌드 (Linear 46s→6s, Beehiiv 64% 감소). 내장 DevTools (빌드 분석/디버깅), `.wasm?init` SSR 지원, 브라우저 콘솔 로그 터미널 포워딩 (`server.forwardConsole`). `@vitejs/plugin-react` v6: Babel 제거, Oxc 기반 React Refresh 트랜스폼. Node.js 20.19+ / 22.12+ 필수. 설치 크기 ~15MB 증가 (lightningcss ~10MB + Rolldown ~5MB). 적용: react-init Vite 8 기본, react-build 파이프라인.
- **Vite 7.0 (2025-06-24)**: Node.js 18 드롭, browser target `baseline-widely-available` 기본값 변경. `rolldown-vite` 패키지로 Rolldown 사전 테스트 가능. 적용: 마이그레이션 경로 참조.

#### Tauri 2 IPC 심화

- **IPC Raw Payloads**: v2에서 JSON 직렬화 오버헤드를 제거하는 Raw Request/Response 지원. 대용량 데이터 전송 시 protobuf, bson, avro 등 커스텀 직렬화 사용 가능. Custom Protocol 기반 IPC — HTTP 통신과 유사한 성능. 적용: react-tauri 스킬에 Raw Payload 가이드 추가 권장.
- **IPC 프리미티브**: Commands (요청-응답) + Events (fire-and-forget, 생명주기/상태 변경 알림). 적용: react-tauri Gotchas 보강.

#### TanStack Router 파일 기반 라우팅

- **Directory Routes vs Flat Routes vs Mixed**: 디렉토리 기반 (전통 폴더 계층), 플랫 (점 표기법 `posts.$postId.edit.tsx`), 혼합 모두 지원. 번들러 플러그인 (Vite, Rspack, Webpack, Esbuild) 통합으로 dev/build 시 자동 라우트 설정 생성. 특수 규칙: `__root.tsx` (루트 레이아웃), `_` prefix (pathless layout wrapper), `$` (동적 파라미터). 자동 코드 스플리팅 + 타입 안전성 (path/search params 자동 타입 추론). 적용: react-screen 스킬 flat route 기본, react-init 라우터 설정.

#### TanStack Query v5 고급 패턴

- **Optimistic Updates 2가지 접근**: (1) `onMutate`에서 캐시 직접 수정 + `onError` rollback (서버 실패 시 이전 상태 복원), (2) `useMutation`의 `variables` 반환값으로 UI 낙관적 표시 (캐시 미변경, 더 단순). v5에서 추가된 방식 (2)는 캐시 무결성 유지에 유리. 적용: react-query Gotchas에 두 방식 비교 추가.
- **Prefetching 전략**: `queryClient.prefetchQuery()` + `queryOptions()` 유틸로 타입 안전한 쿼리 정의 공유. 라우터 loader에서 prefetch → 화면 전환 시 즉시 데이터 표시. `ensureQueryData()`로 캐시 있으면 skip. 적용: react-query, react-screen loader 패턴.

#### Zustand v5 심화 패턴

- **Slices Pattern**: 대규모 스토어를 도메인별 슬라이스로 분할 후 `create((...a) => ({ ...createFishSlice(...a), ...createBearSlice(...a) }))` 합성. `set()` 세 번째 인자로 액션 이름 지정 → DevTools에서 추적 가능. 적용: react-store 템플릿에 slices 예시 추가 권장.
- **DevTools 미들웨어**: `zustand/middleware`에서 import (v4의 `zustand/middleware/devtools`와 다름). Redux DevTools 연결, 타임트래블 디버깅. 적용: react-store Gotchas.
- **v5.0.10 (2026-01) persist 미들웨어 버그 수정**: v5.0.9 이하에서 상태 불일치 발생 가능 → 즉시 업그레이드 권장. 초기 상태가 자동 persist 되지 않음 — 동적 초기값은 `setState()` 명시 호출 필요. 적용: react-store Gotchas.

#### shadcn/ui 최신 동향

- **Luma 디자인 시스템 (2026-03)**: 둥근 기하학, 부드러운 elevation, 넉넉한 spacing, macOS Tahoe 영감. "테마를 넘어 geometry, spacing, feel을 바꾸는 새 비주얼 기반". `shadcn/create`에서 Radix UI / Base UI 모두 지원. 적용: react-init에서 Luma preset 옵션 추가 권장.
- **RTL 지원 (2026-01)**: CLI가 logical property (`start`/`end`) 자동 매핑 — 아랍어, 히브리어 등 RTL 언어 즉시 대응. 적용: react-l10n, react-responsive 연동.
- **Base UI 대안 (2026)**: Radix UI 외에 Base UI 프리미티브 선택 가능 — 번들 사이즈 최적화 옵션. 적용: react-init 프리미티브 선택지 추가.
- **2025-10 신규 컴포넌트**: Spinner, Kbd, Button Group, Input Group, Field, Item, Empty. 적용: react-widget 참조.

#### Tailwind CSS v4 컨테이너 쿼리 심화

- **Container Queries 네이티브**: `@container` 부모 요소에 `container-type` 설정 → 자식에서 `@sm:`, `@md:`, `@lg:`, `@xl:` breakpoint prefix 사용. rem 기반 값. 뷰포트가 아닌 **부모 컨테이너 크기** 기준 반응형 — 컴포넌트 수준 반응형에 최적. 플러그인 불필요. 적용: react-responsive `page-size vs container-size` 판정 로직 보강.
- **Zero-config Content Detection**: `content` 배열 불필요 — 템플릿 파일 자동 탐지. `@tailwindcss/vite` 플러그인 필수. 적용: react-init Vite 설정.

#### TypeScript 5.8+ 패턴

- **`--erasableSyntaxOnly` (5.8)**: Node.js `--experimental-strip-types`와 호환 — enum, namespace 같은 런타임 시맨틱 구문 금지. 직접 `.ts` 실행 가능 (Amaro → SWC WASM 기반 타입 스트리핑). 적용: react-init tsconfig strict 옵션에 추가 검토.
- **`--rewriteRelativeImportExtensions` (5.8)**: `.ts` → `.js` 확장자 자동 변환 — 직접 실행 환경과 빌드 환경 양립. 적용: react-run, react-build 파이프라인 참조.
- **`satisfies` 연산자 강화**: 타입 추론 유지하면서 제약 검증. `const` type parameters로 리터럴 타입 보존. 적용: react-store, react-api 타입 패턴 가이드.

#### Rust WASM 생태계 변화

- **rustwasm org 아카이빙 (2025-09)**: wasm-pack, gloo, twiggy, walrus 등 아카이빙. wasm-bindgen만 독립 org (`github.com/wasm-bindgen`)로 이전. 신규 메인테이너: @daxpedda, @guybedford (Cloudflare). 적용: react-wasm, react-init WASM 의존성 경로 업데이트 필수.
- **wasm-pack 대안 (nickb.dev)**: wasm-pack 대신 **wasm-bindgen-cli + wasm-opt + mise** 조합 권장. 커스텀 cargo profile 지원, 병렬 빌드, Linux musl 성능 이슈 해소. 적용: react-wasm 빌드 스크립트 현대화 검토.
- **WASM Threads + SIMD**: 2024 말~2025 초 모든 주요 브라우저에서 128-bit SIMD 지원. SIMD 활용 시 JS 대비 10-15배 성능 향상 (특정 워크로드). 적용: wasm-catalog 벤치마크 데이터 갱신.

#### Lingui v5 매크로 심화

- **`useLingui` 매크로**: `@lingui/react/macro`에서 import — 컴포넌트 내 비-JSX 메시지 처리 간소화. `const { t } = useLingui()` 패턴. 모듈 레벨에서 사용 불가 (함수 스코프 내에서만). 적용: react-l10n Gotchas 보강.
- **매크로 분리 codemod**: `npx @lingui/codemods split-macro-imports <path>` — 기존 `@lingui/macro` → `@lingui/core/macro` + `@lingui/react/macro` 자동 변환. 적용: react-init 마이그레이션 가이드.
- **컴파일 메시지 구조 변경**: 모든 메시지가 배열 형태 (`["Hello, world!"]`). TMS 사용 시 translation memory 활용 권장. 적용: react-l10n 빌드 파이프라인.

#### View Transitions API

- **Baseline Newly Available (2025-10)**: Firefox 144 합류 → Chrome, Edge, Safari, Firefox 모두 지원 (same-document). MPA transition은 Chrome에서만 완전 지원. 적용: react-animation Tier 2 기준 갱신.
- **`match-element` auto-naming (Chrome 137+)**: `view-transition-name: match-element` — 수십 개 요소에 수동 이름 부여 불필요. 적용: react-animation 가이드.
- **Nested view transition groups (Chrome 140+)**: pseudo-element 계층 보존 — 클리핑, 3D 트랜스폼 가능. 적용: react-animation 고급 패턴.
- **Scoped view transitions (Chrome 140, 실험적)**: `element.startViewTransition()` — 여러 전환 동시 실행 (DOM 서브트리 단위). 적용: react-animation 향후 지원.
- **React canary `<ViewTransition>` 컴포넌트**: React 코어에 View Transition 통합 작업 진행 중 (canary 채널). 적용: react-animation backlog — stable 릴리스 대기.

#### CSS 애니메이션 패턴

- **Scroll-driven Animations**: `animation-timeline: scroll()` / `view()` — 스크롤 위치 기반 애니메이션. `scroll(root block)` (뷰포트 수직), `scroll(nearest inline)` (가장 가까운 수평 스크롤러). Chrome 안정, Firefox 플래그 필요. 적용: react-animation Tier 1 확장.
- **Scroll-triggered Animations (Chrome 145, 2026)**: 특정 스크롤 오프셋 교차 시 시간 기반 애니메이션 트리거. scroll-driven과 다른 개념 — 시간 축 기반. 적용: react-animation Tier 2 후보.
- **@starting-style + scroll-driven 조합**: `@property`로 커스텀 속성 등록 → `@starting-style`에서 전환 → 키프레임 `to`에서 참조. Chrome에서 안정 동작, Safari/Firefox 불완전. 적용: react-animation 고급 패턴 (Chrome-first).

#### 테스팅 생태계

- **Vitest 브라우저 모드 컴포넌트 테스팅**: Playwright, WebdriverIO, preview 모드에서 실제 브라우저 환경 테스트. `vitest-browser-react` 패키지. CSS 레이아웃, 브라우저 API 동작, 이벤트 핸들링의 실제 동작 검증. `page.getByRole()`, `.click()`, `.fill()`, `expect.element()` API. 적용: react-test 브라우저 모드 옵션 추가 권장.
- **Vitest = 2026 표준**: Vite ESM-first 철학과 완전 통합. TypeScript, JSX, CSS modules 별도 설정 없이 처리. Jest 30 대비 번들 크기와 설정 복잡도에서 우위. 적용: react-test, react-preflight 파이프라인.
- **MSW v2 네트워크 모킹**: fetch 직접 모킹 대신 네트워크 경계에서 HTTP 요청 가로채기. Vitest + MSW 조합이 React 통합 테스트 표준. 적용: react-test integration 모드.

#### React Hook Form + Zod 최신

- **RHF v8 beta (v8.0.0-beta.1, 2026-01-11)**: breaking changes 포함. 현재 v7.71.x 안정 버전 사용 권장. 적용: react-form 버전 고정 Gotcha.
- **@hookform/resolvers v5.2.2**: Standard Schema 지원 추가. Zod v4 타입 호환성 이슈 여전 — `import { z } from 'zod/v3'` workaround 유지. 적용: react-form Gotchas (이전 #21 보강).
- **고급 패턴**: discriminated union으로 조건부 검증, single hook으로 create/edit 폼 통합, `setError('root.serverError')` 서버 에러 매핑. 적용: react-form 템플릿.

#### React 19.2 / Compiler 보강

- **`useEffectEvent` 운영 가이드 명문화**: Effect Event 함수는 의도적으로 stable identity를 갖지 않으며, Effect 내부/다른 Effect Event 내부에서만 호출 가능. 의존성 배열에서 제외해야 하고, `eslint-plugin-react-hooks`가 이를 강제한다. 적용: react-store/react-api 에서 "lint를 잠재우기 위한 남용 금지" 규칙 명시.
- **`<Activity />` 실전 포인트**: hidden 초기 렌더에서도 자식은 낮은 우선순위로 pre-render 되지만 Effect 는 mount 되지 않는다. 탭/패널 선로딩에 적합하다. 적용: react-screen 에서 route/tab pre-render 패턴 보강.
- **Compiler 도입 운영 패턴 추가**: 공식 incremental adoption 문서가 `compilationMode: 'annotation'`, `"use memo"` / `"use no memo"`, gating, logger 기반 rollout 모니터링을 권장한다. React Conf 2025 recap 에서는 Sanity Studio 사례를 공식 adoption example 로 재차 언급했다. 적용: `react-compiler` 스킬은 전면 도입보다 디렉토리 단위/플래그 기반 rollout 을 기본값으로 설계.
- **Sanity 실제 채택 데이터**: Sanity Studio v3.65.0 은 1,411개 중 1,231개 컴포넌트를 compiler beta 로 precompile 해 render time/latency 를 **20~30%** 줄였고, 2025-11 문서에서는 Studio v3.65.0+ 와 plugin/tool 배포 파이프라인에서 compiler 지원을 공식화했다. 적용: compiler ROI 예시로 Meta 외 Sanity 데이터를 추가.

#### Vite 8 Rolldown 마이그레이션 보강

- **공식 gradual migration 경로 구체화**: Vite 8 migration guide 는 `rolldown-vite` 를 "Vite 7 + Rolldown" 중간 단계로 명시하고, `rolldown-vite@7.2.2` → `vite@^8.0.0` 전환 예시를 제공한다. `optimizeDeps.esbuildOptions` 는 자동 변환되지만 deprecated 이며 `optimizeDeps.rolldownOptions` 로 옮겨야 한다. 적용: react-build/migrate 문서에 two-step migration 경로 추가.
- **플러그인 작성자 영향 범위**: Rolldown guide 기준으로 build, dep optimizer, CommonJS 처리, JS/CSS minification, config bundling 까지 Rolldown/Oxc/Lightning CSS 로 이동했다. `transformWithEsbuild` 사용 플러그인은 이제 `esbuild` 를 직접 설치하거나 `transformWithOxc` 로 갈아타야 한다. 적용: custom Vite plugin audit 체크리스트 추가.

#### Tauri 2 플러그인 생태계

- **Stronghold**: Tauri v2 공식 plugin 으로 승격되어 `tauri add stronghold` 로 설치 가능하고, JS guest binding (`@tauri-apps/plugin-stronghold`) 과 Argon2 helper 를 제공한다. 문서는 upstream bug 우회용으로 `Cargo.toml` 의 `scrypt` dev profile 최적화도 권장한다. 적용: react-tauri 보안 저장소 기본값을 Stronghold 로 명시.
- **Updater**: v2 updater plugin 은 static JSON 또는 update server 기반 자동 업데이트를 공식 지원하며, `bundle.createUpdaterArtifacts` 설정 시 플랫폼별 서명 번들을 생성한다. AppImage/macOS archive/MSI/NSIS 서명 산출물이 자동 생성된다. 적용: react-tauri 배포 템플릿에 서명/업데이트 아티팩트 단계 추가.
- **Deep Link**: deep-link plugin 은 desktop/mobile 공통 문서와 JS API (`getCurrent`, `onOpenUrl`) 를 제공하지만, macOS/Android/iOS 는 런타임 동적 등록이 불가해 config 기반 등록이 필요하다. Windows/Linux 에서는 single-instance plugin 없이 `onOpenUrl` 동작이 제한된다. 적용: react-tauri auth/callback 템플릿에 single-instance + deep-link 조합을 기본 패턴으로 기록.

#### TanStack Start

- **2026-04 현재 RC 유지**: TanStack Start 공식 overview 는 아직 **Release Candidate** 단계지만 API 는 feature-complete/stable 로 설명한다. 풀 문서 SSR, streaming, server routes, server functions, middleware, Vite 기반 full-stack bundling 을 전면 기능으로 내세운다. 적용: react-init 의 "full-stack React" 후보군에 포함 가능하지만 production 기본값으로는 보수적 표기 유지.
- **도입 신호**: Start homepage 는 2026-04 시점에 GitHub stars/dependents/downloads 를 노출하며 생태계 성장 신호를 보여준다. 다만 v1 stable 문구는 아직 확인되지 않았다. 적용: "emerging but credible" 분류가 적절.

#### React Router v7 최신

- **최신 stable release 확인**: 공식 changelog 기준 React Router **v7.13.0 (2026-01-23)** 이 최신이며, `Links` 의 `crossOrigin` prop 추가와 origin/nonce/path normalization 수정이 포함됐다. 적용: react-screen/router 템플릿 버전 상한 재검토.
- **보안 패치 흐름**: v7.12.0 (2026-01-07) 은 보안 취약점 3건을 수정한 release 로 명시되어 있다. 2025-07 부터는 unstable RSC Data Mode API (`unstable_RSCHydratedRouter`, `unstable_RSCStaticRouter`, `unstable_createCallServer`) 도 공개됐다. 적용: React Router v7 채택 시 최신 patch 유지 필요, RSC 는 experimental 로 표기.

#### Million.js / React 성능 최적화

- **프로젝트 포지셔닝 변화**: 공식 docs 는 여전히 `npx million@latest` 기반 **Million Lint** 설치와 React/Vite/Remix/Astro 통합을 안내하지만, 현재 million.dev 메인 홈페이지는 QA/verification 제품 "Expect" 중심으로 재브랜딩되어 있다. GitHub repo 의 최신 visible release 는 **v3.1.0 (2024-05-21)** 이다. 적용: 2026 기준 Million.js 는 적극 채택 추천보다는 "기존 도입 팀 유지보수/실험" 정도로 분류하는 편이 안전.

#### Astro + React 하이브리드 패턴

- **Actions + React 통합 심화**: `@astrojs/react@4.4.0` 부터 `withState()` / `getActionState()` 로 Astro Actions 를 React `useActionState()` 와 직접 연결할 수 있다. JS 비활성 환경에서도 progressive enhancement 메타데이터를 유지한다. 적용: Astro+React 폼 패턴은 bespoke API 대신 Actions 우선.
- **Client/Server islands 조합**: Astro docs 는 React 컴포넌트를 기본적으로 정적 HTML 로 렌더하고, `client:*` 로 hydration 을 opt-in 하며, `server:defer` 로 server islands 를 병렬 렌더링하는 패턴을 명시한다. 적용: React 전체 앱 hydrate 대신 "정적 shell + React island + deferred personalization" 을 2026 기본 패턴으로 기록.

#### Storybook 9 + 컴포넌트 문서화

- **Storybook 9.0 (2025-06)**: 공식 릴리스는 Storybook 9 을 "testing-first" 메이저로 규정하며 interaction/a11y/visual/coverage 테스트, tags 기반 조직화, story globals, 48% lighter bundle 을 핵심 변화로 제시한다. 적용: 컴포넌트 문서 사이트와 테스트 워크플로를 Storybook 하나로 수렴하는 방향이 강화됨.
- **Autodocs 성숙**: Autodocs 는 `tags: ['autodocs']` 로 활성화되며, Doc Blocks 와 MDX 로 문서 템플릿을 커스터마이즈할 수 있다. subcomponents 문서화도 공식 지원한다. 적용: design-system 문서는 "CSF stories + autodocs + MDX 보강" 조합을 기본으로 삼는 것이 합리적.

#### CSS 전략 2026

- **Tailwind 우세, CSS Modules 여전, CSS-in-JS 축소**: State of React 2025 의 styling 질문에서 Tailwind CSS 2,142, CSS Modules 1,794, Styled Components 1,594 응답으로 Tailwind 가 선두다. State of CSS 2025 에서는 CSS-in-JS 라이브러리를 쓰지 않는 응답이 다수이고, CSS Modules (1,037) 가 Styled Components (870) 보다 높다. 적용: 2026 기본 권장치는 Tailwind 또는 CSS Modules, CSS-in-JS 는 선택적/제한적.

#### Web Components interop

- **React 19 이후 상호운용성 개선 완료**: React 19 stable blog 는 custom elements full support 와 SSR/CSR 에서 property-vs-attribute heuristic 을 공식화했다. Custom Elements Everywhere 에서 React ^19 는 **100% (32/32)** 로 표기된다. 적용: Web Components 를 React 앱에 포함하는 선택지는 2026 에 실전 수준.

#### Signals 제안과 React의 반응

- **표준화는 진행 중, React 코어는 별도 채택 신호 없음**: TC39 `proposal-signals` 는 현재 **Stage 1** 설명 단계이며 여러 프레임워크 저자가 협업 중이다. 반면 React repo 의 `[React 19] Signal & Observable` 이슈는 **closed as not planned** 상태다. 적용: React는 2026 시점에 signals-native API 대신 Compiler/Activity/RSC 축을 우선하는 것으로 해석하는 편이 안전.

#### Waku

- **가벼운 React 19 프레임워크로 포지셔닝 명확화**: Waku 공식 사이트는 자신을 "minimal React framework" 로 설명하며 React 19 server components/actions 지원, static/dynamic render 선택, file-based routing, API routes 를 전면에 내세운다. Node.js 요구 버전은 `^24 || ^22.12 || ^20.19` 로 최신 런타임 지향이다. 적용: 소형/중형 React 프로젝트의 경량 RSC 프레임워크 후보로 분류 가능.
- **성숙도 주의**: npm 패키지는 계속 배포되고 있지만 공식 사이트도 non-production 프로젝트 우선 사용을 권한다. 적용: stable-default 프레임워크가 아니라 실험적/선행 평가 트랙으로 두는 것이 적절.

#### Deno 2 + React 패턴

- **Deno 자체가 React+Vite 경로를 공식화**: Deno Deploy tutorial 은 `deno init --npm vite my-react-app --template react-ts` 로 React+Vite 프로젝트를 바로 시작하는 경로를 제공한다. 즉 "Deno 2 = React 직접 실행/배포" 패턴이 문서화됐다. 적용: react-init 의 비-Node 런타임 옵션에 Deno+Vite 조합 추가 가능.
- **Fresh 2 beta 는 Vite 통합으로 도구 격차 축소**: 2025-09 Fresh 2 beta 는 optional Vite plugin, full Vite plugin ecosystem, modern client/server tooling 을 공식 발표했다. Deno 진영의 React-like 풀스택 패턴은 "Fresh(Preact) or React+Vite on Deno" 의 이원화로 보는 편이 정확하다.

### 신규 스킬 갭 분석

| 제안 스킬 | 아키타입 | 근거 | 우선순위 | 상태 |
| --------- | -------- | ---- | -------- | ---- |
| `react-migrate` | 런북 | React 18→19 ref-as-prop, Zustand v4→v5, wasm-pack→wasm-bindgen-cli | 중간 | backlog |
| `react-view-transitions` | 코드 스캐폴딩 | Browser View Transitions API + React canary 통합 | 낮음 | backlog (canary 대기) |
| `react-compiler` | 가이드 | React Compiler v1.0 설정, 점진적 도입, Rules of React lint | 중간 | backlog |

### 폐기 사유

- wasm-pack을 계속 사용하되 `wasm-bindgen/wasm-pack` fork 경로로 참조 업데이트 필요. rustwasm org 아카이빙 확인.

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
