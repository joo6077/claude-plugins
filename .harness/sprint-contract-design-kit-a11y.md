---
feature: "design-kit docs 페이지 접근성·반응형 실패 5건 수정 (기준 완화 없이 페이지를 고친다)"
created: "2026-07-28 16:10"
complexity: "중간"
conditions: 12
slug: design-kit-a11y
status: done
owner_session: 8a9c2ebc-8d41-48fb-9586-496555a22b30
---

## 배경

`main` 의 Playwright Visual Tests 가 **2026-06-09 부터 계속 red** 다 (5 회 연속, PR #15 의 base 포함).
실패 5 건은 전부 `design-kit/evals/visuals.spec.js` 가 `docs/design-kit/*.html` 을 검사한 것이다.

미머지 브랜치 `kaizen/2026-06-05` 에 이 실패를 green 으로 만드는 커밋(`f546388`)이 있으나,
방식이 **기준 완화**다 — 오버플로 허용 80→120px, `iconography.html` 을 known-overflow 에 추가,
터치타겟 38→36. 테스트 이름이 `touch targets >= 44px` 인데 단정이 이미 38 이고 그걸 36 으로 더 내린다.
이번 카이젠이 도입한 relaxing 규칙(제약 완화는 PASS 근거로 쓸 수 없다)에 걸리는 유형이라
**테스트를 낮추지 않고 페이지를 고치는** 방향을 택했다.

## 리서치 소스

- 로컬 재현 완료 (`@playwright/test` 1.58.2 + chromium-headless-shell 1208). CI 와 동일한 5 건 실패.
- **플랫폼별 수치 차이 실측**: microinteraction 터치타겟 CI 36 / 로컬 37, iconography 오버플로 CI 11 / 로컬 7.
  → 단정 경계에 딱 맞추면 다시 흔들린다. **여유를 두고 고쳐야 한다.**
- 참조 구현: `docs/design-kit/visual-styles.html:1717` (`<button class="theme-toggle" onclick="toggleTheme()">`)
  + `:2379` (`function toggleTheme()`). `design-template.html:306` 도 동일 패턴.

## GAP 분석 (전부 실측)

| # | 페이지 | 실패 | 실측 | 근본원인 |
|---|---|---|---|---|
| G1 | color-palette | touch targets (**30s 타임아웃**) | `.theme-toggle` DOM 부재 | `.theme-toggle` **CSS 만 있고 `<button>` 요소가 없다**. `<html data-theme="dark">` 와 `[data-theme="light"]` 규칙은 있어 테마 인식 페이지인데 토글을 잃었다 |
| G2 | color-palette | dark/light toggle (**30s 타임아웃**) | 동일 | G1 과 동일 원인 |
| G3 | grid-alignment | overflow 375px | **106px** (허용 80) | div 2 개가 `right=481` (w=440) |
| G4 | microinteraction | touch target | 첫 버튼 **37px** (요구 ≥38) | 버튼 높이 부족 |
| G5 | iconography | overflow 375px | **7px** (허용 2) | div `right=382`, `.icon-box` 48px |

참고: microinteraction 의 문서 오버플로 13px 는 이미 KNOWN_OVERFLOW_PAGES 에 있어 통과한다 (허용 80).

## 범위 경계

- 대상: `docs/design-kit/{color-palette,grid-alignment,microinteraction,iconography}.html` 4 개.
- **비대상**: `design-kit/evals/visuals.spec.js` (기준 완화 금지 — 이 스프린트의 존재 이유),
  `kaizen/2026-06-05` 브랜치 머지, 나머지 29 개 docs 페이지, design-kit 스킬·에이전트.
- 브랜치: `main` 에서 새 브랜치. 직접 push 하지 않는다.

## 회귀 게이트

`npx playwright test design-kit/evals/visuals.spec.js --project=chromium` 가 **0 failed** 이고,
`python3 scripts/validate-plugin.py` 가 11 plugins / 11 OK / Exit 0 이어야 한다.

## Architecture

- [x] AR-01: `docs/design-kit/color-palette.html` 에 `.theme-toggle` 버튼이 DOM 에 렌더되고 클릭이 테마를 전환한다. 측정: Playwright 로 375px 뷰포트에서 `.theme-toggle` 의 `boundingBox().height >= 28` 이고(타임아웃 없이 즉시 해소), 클릭 전후 `<html>` 의 `data-theme` 값이 서로 다르다. [exact]
- [x] AR-02: `grid-alignment.html` 과 `iconography.html` 의 375px 문서 오버플로가 **2px 이하**다. 측정: `document.documentElement.scrollWidth - clientWidth` 를 375px 뷰포트에서 측정 (현재 106px / 7px). 플랫폼 차이(CI 11 vs 로컬 7)를 감안해 경계에 붙이지 말고 **0px 를 목표로** 한다. [exact, enumerated]
- [x] AR-03: `microinteraction.html` 의 모든 `<button>` 높이가 **44px 이상**이다. 테스트가 첫 버튼만 검사하더라도 첫 버튼만 고치지 않는다. 측정: 375px 뷰포트에서 모든 `button` 의 `getBoundingClientRect().height` 최소값 ≥ 44 (현재 첫 버튼 37px). 기준을 44 로 잡는 근거: 테스트 이름이 `touch targets >= 44px` 로 선언하고 있고, 38 에 맞추면 CI 36 / 로컬 37 차이로 재발한다. [exact, collective]
- [x] AR-04: 4 개 페이지의 768px 오버플로와 기존 통과 테스트가 깨지지 않는다. 측정: 회귀 게이트의 전체 스위트 실행에서 이번에 고친 5 건 외 **신규 실패 0 건** (현재 138 passed 기준). [exact]

## Skill

- [x] SK-01: design-kit 의 기준 문서(`design-kit/references/audit-criteria.md` 등)에 명시된 터치타겟·반응형 기준을 **낮추지 않는다**. 측정: `git diff` 에서 해당 파일들의 수치 기준이 완화된 변경 0 건 (문서를 손대지 않는 것이 기본이며, 손댔다면 강화 방향만 허용). [exact]

## Script

- [x] SC-01: `design-kit/evals/visuals.spec.js` 를 **수정하지 않는다.** 임계값 완화·`KNOWN_OVERFLOW_PAGES` 추가·`test.skip` 삽입으로 통과시키지 않는다. 측정: `git diff --name-only <시작커밋>..HEAD` 에 `design-kit/evals/visuals.spec.js` 가 **없다**. [exact]

## Error

- [x] ER-01: 4 개 페이지의 브라우저 콘솔 에러가 0 건이다. 측정: 각 페이지 로드 시 `console` 의 `error` 타입 메시지 0 건 (스위트의 `no console errors on load` 테스트가 이를 커버하므로 그 4 건이 통과해야 한다). [exact, enumerated]

## Anti-patterns

- [x] AP-02: force push 를 사용하지 않는다. 측정: 이 스프린트의 셸 이력에 `git push --force` / `-f` 0 건. [exact]
- [x] AP-03: bare code fence 0 건. 측정: `python3 scripts/validate-plugin.py` 의 V6 가 전 킷에서 `0 bare` 를 보고한다. [exact]

## Reusability

- [x] RE-01: `color-palette.html` 의 theme-toggle 을 새로 발명하지 않고 같은 디렉토리의 기존 패턴(`visual-styles.html:1717` 버튼 + `:2379` `toggleTheme()`)을 재사용한다. 측정: 추가된 버튼의 클래스·`onclick` 규약과 토글 함수의 동작(`data-theme` 속성 토글 + localStorage 유무)이 참조 구현과 동일 계열이다. [structural]

## Diagnostics

- [x] DG-01: `npx playwright test design-kit/evals/visuals.spec.js --project=chromium` 가 **0 failed** 다. 측정: 실행 출력의 `failed` 카운트가 0 (현재 5 failed / 138 passed). [exact]
- [x] DG-02: 레포 게이트가 통과한다. 측정: `python3 scripts/validate-plugin.py` 가 `11 plugins, 11 OK` + Exit 0 을 출력하고, `bash -n scripts/release.sh` 가 Exit 0 이다 (project.yaml `commands.analyze` 리터럴). [exact]
