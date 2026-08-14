---
phase: 6
title: "Phase 6 design-kit — 확보된 외부 근거"
collected: 2026-08-13
method: codex (foreground, 직접 호출)
note: 이 파일이 이 Phase 의 유일한 외부 근거다. 바깥 자료를 새로 찾지 마라. 여기 없는 URL·수치를 지어내지 마라.
---

WebSearch fallback

웹 검색 10/10 사용, 로컬은 read-only로 확인했습니다.

**1. 관찰 사실**
E1. 변형 구별성은 “확립된 자동 UI 표준”이라기보다, 기존 디자인 탐색 방법을 UI에 적용하는 쪽이 맞습니다. Morphological chart는 기능/축별 가능한 수단을 나열하고 조합해 design space를 만드는 방법이며, 조합 폭발과 비실용 해를 제한해야 한다고 설명합니다. UI 변형도 `축 -> 값 -> 조합`으로 다루면 B3/B6 같은 동일 feature vector를 기계적으로 잡을 수 있습니다. 출처: https://www.ifm.eng.cam.ac.uk/research/dmg/tools-and-techniques/morphological-charts/ , https://open.clemson.edu/all_theses/274/

E1 보강. 생성 디자인 연구에는 거리 기반 sampling, clustering, psychophysical distance metric으로 “서로 다르게 지각되는 대안”을 만드는 접근이 있습니다. 추론: design-kit에는 pixel/perceptual diff보다 먼저 구조 feature vector/Hamming distance를 두고, 렌더 후 perceptual diff는 보조 신호로만 두는 것이 적합합니다. 출처: https://strathprints.strath.ac.uk/70009/

E2. Playwright/Chromatic/Percy/BackstopJS는 baseline snapshot과 diff, threshold, ignore/delay/selector/scenario를 제공합니다. 그러나 확인한 공식 문서 범위에서는 `decision_id -> required surface -> golden coverage`를 native 개념으로 강제하는 패턴은 미확인입니다. 이는 시각 회귀 도구의 기본 기능이 아니라 manifest 기반 traceability gate로 얹어야 합니다. 출처: https://playwright.dev/docs/test-snapshots , https://www.chromatic.com/docs/visual/ , https://percy.io/how-it-works , https://github.com/garris/BackstopJS

E2 보강. W3C ACT Rules Format은 테스트 규칙에 requirement mapping, rule input, applicability, expectations, outcome mapping을 요구합니다. 추론: decision manifest는 이 구조를 UI 결정 전파 검증에 옮긴 “요구사항-테스트 traceability” 패턴으로 정당화할 수 있습니다. 출처: https://www.w3.org/TR/act-rules-format/

E3. “스크린샷 파일이 있다”는 “사용자가 보는 상태를 측정했다”가 아닙니다. Playwright도 visual comparison은 첫 실행에서 reference를 만들고 다음 실행부터 비교하며, rendering은 OS/브라우저/폰트/하드웨어 등에 따라 달라질 수 있다고 경고합니다. 실제 관측에는 locator visibility, non-empty bounding box, count/text/in-viewport 같은 assertion이 필요합니다. 출처: https://playwright.dev/docs/test-snapshots , https://playwright.dev/docs/actionability , https://playwright.dev/docs/test-assertions

1차 출처 변경점:
- Tailwind v4: 기본 팔레트가 RGB에서 OKLCH/P3로 전환, CSS-first `@theme`, token을 CSS variables로 노출, container queries core 지원. design-system은 OKLCH primitive를 권장하되 승인값/기존값을 덮으면 안 됩니다. 출처: https://tailwindcss.com/blog/tailwindcss-v4
- DTCG v1 Final 2025.10: stable vendor-neutral token format, `$value`/`$type`/`$extensions`/`$extends`, curly-brace alias, JSON Pointer 참조, modern color spaces/theming 지원. 출처: https://www.w3.org/community/reports/design-tokens/CG-FINAL-format-20251028/ , https://www.w3.org/community/design-tokens/2025/10/28/design-tokens-specification-reaches-first-stable-version/
- WCAG 2.2: SC 2.5.8 AA target minimum은 24x24 CSS px, 44x44는 SC 2.5.5 AAA입니다. 출처: https://www.w3.org/TR/WCAG22/
- MDN container queries: 컴포넌트는 viewport가 아니라 container size/name/style/scroll-state 등에 따라 반응할 수 있고, `container-type: inline-size`와 `@container`가 핵심입니다. 출처: https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Containment/Container_queries
- Material 3 Expressive / Apple HIG: M3 Expressive는 color/shape/size/motion/containment로 주의를 끌고 usability를 높이는 쪽이며, context를 깨면 usability가 떨어진다고 경고합니다. Apple Liquid Glass는 controls/navigation의 기능 레이어에 sparing하게 쓰고 접근성 설정에서 테스트하라고 합니다. 출처: https://design.google/library/expressive-material-design-google-research?pubDate=20250521 , https://developer.apple.com/tutorials/data/documentation/technologyoverviews/adopting-liquid-glass.md

**2. 권장안**
`design-mockup`/`design-concept`에 “Variant Contract Matrix + Distinctiveness Gate”를 넣으십시오.

구체 조항:
- 사용자가 N개를 말하면 정확히 N개, 미지정 기본 3개, 최대 5개. 토큰 파일·surface lane·카탈로그는 명시 요청 없으면 생성 금지.
- 모든 시안은 `variant_id`, `strategy_label`, `axis_vector`, `intended_user_scenario`를 갖는다.
- 사용자가 축을 지정하면 그 축은 필수 계약이다. 예: `bubble_container`, `column_count`, `meta_position`, `grouping_unit`.
- Pairwise gate: 지정 축 전체가 동일한 두 variant는 FAIL. 지정 축이 3개 이상이면 기본 `Hamming distance >= 2`; 단 “micro-variant 비교”라고 명시한 경우만 예외.
- 색상/토큰/카피만 다른 값은 구조 구별성 점수에 넣지 않는다.
- 렌더 후 perceptual/pixel diff는 보조 검사다. 큰 pixel diff가 구조 중복을 면제하지 않는다.

`design-test`/`design-audit`에 “Decision Propagation Manifest Coverage”를 넣으십시오.

권장 schema:
```yaml
decisions:
  - decision_id: DEC-2026-08-13-001
    source: .design/approvals/20260813-dashboard.md
    status: approved
    summary: "SP-G spacing and grouping"
    required_surfaces:
      - surface_id: dashboard.desktop.main
        route_or_entry: /dashboard
        state: populated
        viewport_or_container: desktop-1440
        selectors: ["main", "[data-surface='group-list']"]
        golden: tests/design/goldens/DEC-2026-08-13-001/dashboard.desktop.main.png
        assertions: ["main visible", "group rows >= 1", "container height > 0"]
    excluded_surfaces:
      - surface_id: onboarding.mobile
        reason: "decision does not apply to onboarding flow"
```

Coverage rule:
- `required_surfaces`에 golden 또는 user-visible assertion이 없으면 FAIL.
- golden만 있고 핵심 요소 visible/count/height assertion이 없으면 FAIL.
- snapshot update는 `decision_id`와 approval artifact가 있을 때만 허용.
- 변경 대상 locator snapshot과 주변 영역 snapshot을 분리해 “결정 반영”과 “의도 외 변화 없음”을 따로 판정합니다.

E3용 조항:
- 증거 채널을 명시합니다: `artifact_snapshot`, `dom_snapshot`, `browser_user_visible`, `device_user_visible`.
- `artifact_snapshot`만으로 “사용자가 보는 화면 정상”이라고 말하지 못합니다.
- 사용자 관측과 충돌하면 사용자 관측을 반박하지 말고 동일 route/data/viewport/scroll/accessibility setting으로 재현 측정합니다.
- PASS 문장에는 최소 `viewport`, `route/state`, `visible locator`, `count/height`, `screenshot/golden id`가 있어야 합니다.

넣지 말아야 할 것:
- Playwright/Chromatic/Percy/BackstopJS 중 하나를 design-kit 전체 표준으로 강제하지 마십시오.
- OKLCH, M3 Expressive, Liquid Glass를 기존 승인값보다 상위 규칙으로 두지 마십시오.
- 모든 화면/상태에 golden을 무차별 생성하지 마십시오.
- 44px를 WCAG AA 기준으로 쓰지 마십시오.
- perceptual diff만으로 “서로 다른 시안”이라고 판정하지 마십시오.

**3. 트레이드오프**
Golden 회귀는 유지비가 큽니다. 의도된 디자인 변경마다 baseline review가 필요하고, 브라우저/OS/폰트/anti-aliasing 차이로 잡음이 생기며, threshold를 높이면 실제 회귀를 놓칩니다. 대응은 manifest로 대상 surface를 줄이고, CI 렌더 환경/폰트/브라우저를 고정하고, 동적 데이터·시간·애니메이션을 고정하며, high-risk 결정만 golden으로 보호하는 것입니다.

Feature vector gate는 과도하면 체크박스식 변형을 유도합니다. 그래서 “중복 방지”는 강하게, “좋은 디자인 선택”은 여전히 사용자 판단/리뷰로 남겨야 합니다.

**4. 열린 질문**
- 기본 시안 수를 현행 5개에서 3개로 낮출지.
- `Hamming distance >= 2`를 전역 기본으로 둘지, 지정 축 4개 이상일 때만 둘지.
- `decisions.yaml` 위치를 `.design/decisions.yaml`로 고정할지, toolkit별 manifest를 허용할지.
- golden을 repo에 커밋할지, CI artifact/Chromatic/Percy 외부 baseline으로 둘지.
- surface registry를 수동 작성하게 할지, 라우트/스토리북/스크린 목록에서 자동 생성하게 할지.
