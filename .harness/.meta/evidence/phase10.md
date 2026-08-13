---
phase: 10
title: "Phase 10 react-kit — 확보된 외부 근거"
collected: 2026-08-13
method: codex (foreground, 직접 호출)
note: 이 파일이 이 Phase 의 유일한 외부 근거다. 바깥 자료를 새로 찾지 마라. 여기 없는 URL·수치를 지어내지 마라.
---

출처 유형: WebSearch fallback

Read-only로 확인했고 파일 수정은 하지 않았습니다. 웹 검색은 10/10회 사용했습니다.

**관찰 사실**

| 항목 | 현행 stable | breaking change / 현행성 판정 | 출처 URL |
|---|---:|---|---|
| React | `react@19.2.8` | React 19 자체는 18 대비 breaking changes 있음. `use()`와 ref-as-prop는 React 19 stable 기능. react-kit의 React 19 전제는 현행과 맞음. | https://registry.npmjs.org/react/latest, https://react.dev/blog/2024/12/05/react-19, https://react.dev/blog/2024/04/25/react-19-upgrade-guide |
| TanStack Query | `@tanstack/react-query@5.101.4` | 현행 major는 v5. object-form 단일 시그니처와 `invalidateQueries({ queryKey })`는 계속 맞음. | https://www.npmjs.com/package/%40tanstack/react-query?activeTab=versions, https://tanstack.com/query/v5/docs/framework/react/guides/migrating-to-v5, https://tanstack.com/query/v5/docs/framework/react/guides/query-invalidation |
| Tauri 2 | `@tauri-apps/cli v2.11.4` | v2 전환 breaking: v1 allowlist 제거, permissions/scopes/capabilities ACL. `core:default`는 현행 유효. | https://v2.tauri.app/release/%40tauri-apps/cli/, https://v2.tauri.app/blog/tauri-20/, https://v2.tauri.app/security/capabilities/, https://v2.tauri.app/reference/acl/core-permissions/ |
| Tailwind CSS | `tailwindcss@4.3.3` | 현행 major는 v4. `@theme`와 OKLCH 기본 팔레트 인용은 유효. | https://www.npmjs.com/package/tailwindcss?activeTab=versions, https://tailwindcss.com/blog/tailwindcss-v4, https://tailwindcss.com/docs/theme |
| Zustand | `zustand@5.0.14` | 현행 major는 v5. v5 migration의 `useShallow` 권장은 유효. 단 “항상 강제”라기보다 객체/배열 selector에 필수로 해석하는 게 정확함. | https://www.npmjs.com/package/zustand, https://zustand.docs.pmnd.rs/reference/migrations/migrating-to-v5 |
| Lingui | `@lingui/core@6.6.0` | react-kit의 “Lingui v5” 인용은 현행 major와 어긋남. v6는 ESM-only, Node.js `22.19+`, `@lingui/macro`는 더 이상 maintained 아님. | https://www.npmjs.com/package/%40lingui/core, https://lingui.dev/releases/migration-6 |
| react-hook-form + zod | `react-hook-form@7.85.0`, `@hookform/resolvers@5.5.7`, Zod v4 stable, Zod patch는 미확인 | 과거 Zod v4 resolver 이슈는 현재 기본 전제로 유지하면 낡음. `@hookform/resolvers` v5.1.0에서 Zod 4 지원이 들어갔고 현 npm 문서도 `zod` 또는 `zod/v4` 예시를 제시함. | https://github.com/react-hook-form/react-hook-form/releases, https://www.npmjs.com/package/%40hookform/resolvers?activeTab=versions, https://github.com/react-hook-form/resolvers/releases/tag/v5.1.0, https://zod.dev/v4 |
| Vite | `vite@8.2.0` | 현행 major는 v8. Rolldown 단일 번들러/Oxc 전환은 stable. react-kit 문서의 Vite 8 설명은 맞지만 템플릿의 `vite: ^6.0.0`은 stale. | https://www.npmjs.com/package/vite?activeTab=versions, https://vite.dev/blog/announcing-vite8, https://vite.dev/guide/migration.html |

**애니메이션 원칙 검증**

View Transitions API: same-document View Transitions는 MDN 기준 Baseline 2025, Can I Use 기준 전역 90.2%, Chrome/Edge 111+, Safari 18+, Firefox 144+ 지원입니다. 다만 `@view-transition` 기반 cross-document/MPA 전환과 일부 세부 기능은 limited availability로 봐야 합니다.  
출처: https://developer.mozilla.org/en-US/docs/Web/API/ViewTransition, https://caniuse.com/view-transitions, https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/%40view-transition

CSS scroll-driven animations: `animation-timeline: scroll()`/`scroll-timeline`은 Can I Use 기준 전역 85.43%, Chrome/Edge 115+, Safari/iOS 26+, Firefox 156+ 지원입니다. MDN의 `view()`는 아직 “not Baseline”입니다. react-kit의 `@supports` fallback 방침은 유지가 맞지만, “Firefox는 플래그 필요” 문구는 최신 지원표로 갱신하는 편이 정확합니다.  
출처: https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/animation-timeline/view, https://caniuse.com/mdn-css_properties_animation-timeline_scroll, https://caniuse.com/mdn-css_properties_scroll-timeline

추론: 라이브러리 0개 원칙은 유지 가능하지만, 표준만으로 자동 커버되지 않는 공백은 있습니다. 복잡한 physics/spring, inertia, collision, accessible sortable DnD, keyboard reorder, live-region announcement, Lottie JSON 직접 재생, cross-document shared transition의 균일 지원은 직접 구현·fallback·사전 렌더 자산으로 처리해야 합니다.

**권장안**

1. [package.json.template](/Users/jackson/Hub/10_Dev/claude-plugins/react-kit/templates/package.json.template:25)의 `vite ^6`, `@hookform/resolvers ^3`, `zod ^3`, `@lingui/macro ^5`는 갱신 후보입니다.
2. [react-init/SKILL.md](/Users/jackson/Hub/10_Dev/claude-plugins/react-kit/skills/react-init/SKILL.md:19)의 Zod v4 workaround는 “legacy resolver용”으로 낮추고, 기본은 resolver v5.1+ / Zod v4 호환으로 갱신하는 게 맞습니다.
3. Lingui는 v6 현행성을 반영하되, Node 22.19+ 요구가 react-kit 기준과 충돌하면 “v5 compatibility pin”으로 명시해야 합니다.
4. [react-animation/SKILL.md](/Users/jackson/Hub/10_Dev/claude-plugins/react-kit/skills/react-animation/SKILL.md:37)의 scroll-driven 지원 문구만 최신 브라우저 표로 갱신하면 됩니다. 새 규칙 추가는 불필요합니다.

**트레이드오프**

라이브러리 0개 원칙은 번들·의존성·감사 표면을 줄입니다. 대신 복잡한 gesture와 a11y 품질은 우리 코드와 테스트 책임이 됩니다.

Lingui v6를 “현행 stable”로 따라가면 Node 기준이 올라갑니다. Vite 8은 Node 20.19+도 허용하므로, 전체 킷 Node floor를 올릴지 별도 판단이 필요합니다.

**열린 질문**

- react-kit이 Node 20.19+를 유지해야 하나, Lingui v6에 맞춰 Node 22.19+로 올릴 수 있나?
- Vite 8/Rolldown에서 기존 WASM 보조 플러그인 조합을 계속 보장할 수 있는지는 별도 실측 필요합니다.
- Zod 최신 patch 번호는 이번 검색 안에서 확인 못 했습니다. Major v4 stable만 확인했습니다.
