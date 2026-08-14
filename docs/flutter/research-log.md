---
title: Flutter Kit Research Log
version: 1.2.0
last_updated: 2026-08-13
---

# Flutter Kit Research Log

## [2026-08-13] — Phase 5 kaizen

**주제:** 버전 사실 정정 3 종 + Primitive Substitution Gate(G1) · Riverpod invalidate 경계(G2) ·
위젯 테스트 하네스(G3) · 성능 환경 배제(G4)

**외부 조회 0 회.** 이 사이클의 유일한 외부 근거는 `.harness/.meta/evidence/phase5.md` 다
(수집 방법: codex foreground). 아래 URL 은 전부 그 파일이 인용한 것이다.

### 리서치 소스 (evidence 파일 경유)

| # | URL | 확인한 사실 |
|---|-----|------------|
| 1 | <https://pub.dev/packages/freezed/changelog> | **[정정 2026-08-13 근거]** 최신 stable **3.2.5**. `.when`/`.map` 제거는 **3.0** 의 breaking, **3.1.0 에서 재추가**. "Freezed 3 부터 제거" 를 절대 규칙으로 쓰면 낡은 조항 |
| 2 | <https://docs.flutter.dev/release/release-notes> | stable 목록 최상단 **3.47.0** |
| 3 | <https://flutter.dev/blog/whats-new-in-flutter-3-47> | Android 의존성 매트릭스 — Java 17 · KGP 2.4.0 · AGP 9.1.0 · Gradle 9.3.1 |
| 4 | <https://docs.flutter.dev/perf/impeller> | iOS Skia 전환 불가 · Android API 29+ 기본 · Web 은 Skia · **macOS/Linux/Windows 는 3.47 부터 Impeller 기본** |
| 5 | <https://docs.flutter.dev/perf/ui-performance> | 성능 디버깅은 물리 기기 + profile mode. debug/simulator 는 release 동작을 대표하지 않음 |
| 6 | <https://docs.flutter.dev/testing/build-modes> | profile mode 는 emulator/simulator 에서 **비활성** |
| 7 | <https://riverpod.dev/docs/concepts2/refs> | `watch` 선언형 구독 / `listen` side effect / `invalidate` 는 다음 read 때 재평가 / `refresh` 는 invalidate + read sugar |
| 8 | <https://riverpod.dev/docs/concepts2/auto_dispose> | listener 0 이 된 뒤 **한 프레임 후** dispose · recompute 시 autoDispose 무관하게 state 파괴 · family 는 autoDispose 권장 |
| 9 | <https://riverpod.dev/docs/how_to/testing> | unit 은 `ProviderContainer.test()`(공유 금지, autoDispose 는 `listen` 으로 붙잡기) · widget 은 `ProviderScope` 루트 + `tester.container()` |
| 10 | <https://pub.dev/packages/flutter_riverpod/changelog> | 3.4.x 에서 scoped override 환경의 `invalidate`/`refresh` 미탐지 버그 수정 + `Ref.onManualInvalidation()` 추가 → **버전 가드 필요** |
| 11 | <https://github.com/flutter/agent-plugins> | 공식 Agent Plugins 는 "skills/rules 로 반복 워크플로우 주입" 을 agent mistake 감축의 1 차 기법으로 제시 |

### 내부 데이터 소스

- `.harness/.meta/kaizen-data-pool.md` §1 REJECT Top 20 — `RE-02`(기본 `Divider` 사용, `IFDivider`
  미재사용) · `LG-02`(팔레트 변경 시 provider invalidate 누락) · `LG-01`(16종 매핑 중 2종만 검증)
- `.claude/kaizen-input/insights-report.md` — 신규 델타 **D5**(성능 조사에서 환경 배제 성공 사례:
  18일 누수된 시뮬레이터 render host 의 swap 포화), **D3**(사용자 관측 vs 자기 증거 충돌)

### 사실 정정 (이 로그의 과거 서술 포함)

이 문서의 historical 항목 7 줄에 `**[정정 2026-08-13]**` 주석을 인라인으로 달았다. 과거 기록을
지우지 않고 정정만 덧붙인다.

1. `when`/`map` 이 영구 삭제됐다고 단정한 4 줄 → 3.1.0 재추가 명시
2. Impeller 플랫폼 상태 2 줄 → 3.47 desktop 기본
3. stable 3.44.7 표기 1 줄 → 3.47.0

스킬 표면 정정: `flutter-api` · `flutter-audit` · `flutter-error` · `flutter-hooks` ·
`flutter-provider` (Freezed) · `flutter-widget` · `flutter-transition` (stable 버전) ·
`flutter-audit` · `references/flutter-ai-rules.md` (Impeller · AGP 매트릭스).

### 반영 (신규 게이트 4 종)

- **G1 Primitive Substitution Gate (E2)** — `flutter-toolkit/references/primitive-substitution-gate.md`
  SSOT 신설. `flutter-widget` · `flutter-screen` · `flutter-audit` · `widget-inspector` 4 표면이
  인용만 한다. 기존 §Enumerate-before-Act(E1)가 있는데도 `RE-02` 가 났으므로 등급 승급으로 처리했고,
  **layout primitive 는 면제 목록으로 명시**해 과잉 규칙화를 막았다
- **G2 invalidate 경계** — `flutter-provider` 에 파생 provider `watch`+`select` 연결, mutation 후
  영향 provider 열거 + `invalidate`, autoDispose 실수명, `onManualInvalidation` **3.4.x 버전 가드**.
  "전체 family invalidate" 는 금지 조항으로 명시
- **G3 widget test 하네스** — `flutter-test` + `quality/testing.md` 에 `ProviderScope` 루트 +
  `tester.container()` 기본형과 전수 매핑 coverage 조항
- **G4 성능 환경 배제** — `flutter-audit` + `quality/performance.md` 에 Environment Exclusion
  Checklist 8 항 + "simulator/debug 단독 결과는 `[미검증]`" 판정 규칙

## [2026-07-27] - Phase 5 kaizen

**주제:** Friction #2(시각·런타임 검증 신뢰 불가) enforcement 승급 + Flutter 3.44 / Riverpod 3.4 정합화

### 리서치 소스 (전부 WebFetch 실측 · Context7 은 OAuth 미인증으로 사용 불가)

| # | URL | 확인한 사실 |
|---|-----|------------|
| 1 | <https://docs.flutter.dev/release/release-notes> | stable **3.44.7** (페이지 갱신 2026-07-10). 스킬들이 기준으로 삼던 3.41 은 구버전. **[정정 2026-08-13]** 릴리스 인덱스 stable 목록 최상단은 이제 **3.47.0** 이다 |
| 2 | <https://docs.flutter.dev/release/release-notes/release-notes-3.44.0> | `TestWidgetsApp`(WidgetTester 기본 앱 표준화) · `TestTextField` 추가, `WidgetTesterCallback` 파라미터명 `widgetTester`→`tester`, flutter_test false-positive 히트테스트 수정. `ReorderableListView.onReorder` deprecated, `ExtendSelectionByPageIntent` 제거. `AnimatedCrossFade.onEnd` · Hero curve 커스터마이징 · `CupertinoSheetRoute` · 무한 `CarouselView` · `CarouselView.onItemChanged` · `RoundedSuperellipseInputBorder` · `Overlay.alwaysSizeToContent` · `ScrollCacheExtent` 추가. Impeller SDF 렌더링 |
| 3 | <https://api.flutter.dev/flutter/flutter_test/matchesGoldenFile.html> | `expectLater` + await 필수, `--update-goldens` 로 마스터 갱신. 커스텀 폰트는 플랫폼·Flutter 버전별로 다르게 렌더 → CI 실패 원인 4 종(OS 차이 / 버전 차이 / 폰트 로드 실패 / 실제 UI 변경) |
| 4 | <https://pub.dev/packages/golden_toolkit> | **discontinued**. 최신 0.15.0, 마지막 업데이트 3 년 전 |
| 5 | <https://pub.dev/packages/alchemist> | 0.14.0, 4 개월 전 갱신, 유지보수 중 (Very Good Ventures / Betterment). 로컬·CI 테스트 분리, 자동 리사이즈, 테마·텍스트 스케일 조정 |
| 6 | <https://pub.dev/packages/flutter_riverpod> | 최신 **3.4.1** (조회 시점 기준 17 시간 전 릴리스) |
| 7 | <https://pub.dev/packages/flutter_riverpod/changelog> | 3.2.0 `family.overrideWith` deprecated → `overrideWith2`(4.0 rename 예정), 3.4.0 `SyncProviderTransformerMixin` deprecated. 신규: `Ref.onManualInvalidation()` · `ProviderContainer.allProviders()` · `AsyncValue.requireValue`(3.1) · `CustomProviderListenable`/`ValueListenable`(3.4). **mutations/offline 은 여전히 experimental** |
| 8 | <https://pub.dev/packages/go_router/changelog> | 최신 **17.3.0**. 17.0 `ShellRoute` observer 알림 기본화(`notifyRootObserver`), 15.0 URL 대소문자 구분(`caseSensitive`) |
| 9 | <https://pub.dev/packages/flutter_hooks> | 최신 0.21.3+1. 훅 3 원칙(이름 `use` prefix · 무조건 호출 · 조건부 호출 금지) 재확인 |

### 내부 데이터 소스

- `.claude/kaizen-input/insights-report.md` (2026-07-27, 53 일 · 51 세션) — Friction #2 가 신규 최상위, 진앙이 Flutter
- `.claude/kaizen-input/reflect-digest-2026-07-27.md` — `mismatched-provider-skill` · `edit-before-read` · `preserve-original-colors` · `false-positive-static-verification` · `scan-animation-direction-mismatch`
- `.harness/.meta/kaizen-data-pool.md` §1 글로벌 REJECT (`AR-01` codegen 산출물 혼입 · `UI-07` widget test 0 건 · `UI-03` alignment 불일치) / §2 외부 프로젝트 (fit-pal · apps · flutter_playwright)

### 반영 (enforcement 등급 승급 중심 — 새 규칙 추가 최소화)

- **신규** `flutter-toolkit/references/visual-evidence-protocol.md` (E2) — 시각 산출물 완료 증거 SSOT.
  채널 감지는 **프로젝트 감지 기반**(MCP 도구명 하드코딩 금지), baseline→변경→재캡처→대조 루프,
  "빈 캡처는 PASS 증거가 아니라 검증 실패 신호", degraded 모드 `[미검증]`, Visual Evidence Block 체크리스트
- UI 스킬 5 종(widget · screen · skeleton · transition · responsive)에 Gotcha + 완료 단계 양쪽 연결
- `project-detection.md` Step 8 `VISUAL_CHANNEL` / `HAS_VISUAL_CHANNEL` 감지 추가
- `flutter-audit` — 자체 `[미검증]` 임계 재정의 삭제 → qa-evaluation-guide §Canonical Unverified-Evidence Protocol 5 조항 문구 변형 없이 복제 + Evidence Validity Gate 4 검사 도입
- `widget-inspector` — "Clean" vacuous pass 차단(스캔 대상 파일 수 선보고, 0 개면 `[미검증]`)
- `flutter-provider` — 신규 생성 전용임을 description·Step 1 에 명시(`mismatched-provider-skill`), Read-before-Edit MUST
- `flutter-hooks` — 3-Step → 4-Step(검증) 확장, 정적 확인을 동작 확인으로 주장 금지
- `flutter-run` — codegen 산출물/수기 변경 분리 보고 (`AR-01`)
- `flutter-test` — `$DART test` → `$FLUTTER test` 버그 수정, 무출처 주장(`community 2025-12`) 을 실측 URL 로 교체, 3.44 테스트 헬퍼 추가
- `flutter-kaizen` — validate-plugin 7 → 8 카테고리(V1~V8), scope-creep 은 unit 수 기준, NO_CHANGE 허용 명시

## [2026-06-05] — Phase 5 kaizen

flutter-feature/flutter-screen 에 과잉설계 방지 Gotcha 추가 (insights 2026-06-04 Friction #3). flutter-extract/provider 1차 승격분 중복 회피, stack-agnostic 유지.

출처: `.claude/kaizen-input/insights-report.md` Friction #3.


> Flutter 관련 리서치 로그. `docs/kaizen/flutter-research-log.md` 와 동일 내용을 per-kit view 로 보관한다.
> kaizen-orchestrator 의 per-kit research-log 정책 (Step 12) 에 따라 생성됨.
> 상세 소스/인사이트는 `docs/kaizen/flutter-research-log.md` 를 참조.

## [2026-05-07] — Phase 5 kaizen (flutter, /insights 흡수)

### 데이터 소스

- 데이터 풀 §0 `/insights` 30 일 분석 (3 friction · 3 pattern · 3 feature)
- `harness/references/cross-kit-principles.md` v1 매트릭스의 flutter 열

### Phase 5 변경

- flutter/README.md 에 cross-kit-principles 매트릭스 cross-reference 섹션 추가
- plugin.json patch bump (이번 사이클)
- 매핑: flutter-audit ANALYZE ↔ Pre-Edit Batch Audit, flutter-reviewer self-check ↔ Self-Evaluator Audit, PostToolUse 정적 검증 ↔ Hook-Triggered Auto-Correction

### 외부 리서치 인용 (이전 사이클 보존, 이번 사이클 추가 없음)

이전 카이젠 사이클의 리서치 인용은 본 로그 하단 + cross-kit-principles 매트릭스로 보존된다.

---


---

## 2026-04-11

**트리거:** kaizen-orchestrator Phase 5 (research-mode rerun)

### 조사한 소스 요약

| # | 제목 | URL | 유형 | 결과 |
| - | ---- | --- | ---- | ---- |
| 1 | Riverpod 3.0 migration | <https://riverpod.dev/docs/3.0_migration> | 공식 | 채택 |
| 2 | Freezed 3.0 changelog | <https://pub.dev/packages/freezed/changelog> | 공식 | 채택 (abstract/sealed) |
| 3 | go_router StatefulShellRoute | <https://pub.dev/documentation/go_router/latest/go_router/StatefulShellRoute-class.html> | 공식 | 채택 |
| 4 | Flutter 3.29 release notes | <https://docs.flutter.dev/release/release-notes/release-notes-3.29.0> | 공식 | 채택 |
| 5 | flutter_hooks | <https://pub.dev/packages/flutter_hooks> | 공식 | 채택 |
| 6 | fit-pal / apps sprint-feedback | (internal) | ground truth | 채택 |

### 주요 인사이트 (요약)

- **Riverpod 3.0 Notifier 라이프사이클**: 재생성 시 leak 방지를 위해 Notifier 내부 Timer/Controller 금지, `ref.onDispose` 로 분리
- **Freezed 3.0 sealed + Dart 3 switch expression**: `when`/`map` 제거 마이그레이션 대응 — **[정정 2026-08-13]** `when`/`map` 은 **3.1.0 에서 재추가**됐다. 절대 규칙이 아니다
- **go_router StatefulShellRoute + preload: true**: 탭 네비게이션 공식 권장 패턴
- **context.mounted vs ref.mounted**: async gap 후 context 재사용 시 필수 가드 구분
- **Makefile monorepo 감지**: fit-pal/apps 에서 make 기반 표준 타겟 감지 → project-detection Step 2b
- **Props 번들링 (widget-inspector)**: HAS_FREEZED + HAS_HOOKS 프로젝트에서 위젯 파라미터 6+ 개 → `@freezed Props` 권장

### 전체 기록

- `docs/kaizen/flutter-research-log.md` (마스터 로그)
- `docs/kaizen/flutter-changelog.md` (변경 이력)

### PR

- <https://github.com/joo6077/claude-plugins/pull/6>

---

## 2026-04-12

**트리거:** 5성 Gap 개선 — docs/flutter 리서치 확충 (695줄 → 1500줄+)

### 확충 대상 및 출처

| 파일 | 추가 내용 | 주요 출처 |
| ---- | --------- | --------- |
| ui/animation.md | Staggered animation, AnimatedSwitcher, RepaintBoundary, 성능 프로파일링 | https://docs.flutter.dev/ui/animations/staggered-animations |
| ui/responsive.md | Breakpoint utility, Sliver 반응형, Foldable 지원, 테스트 전략 | https://m3.material.io/foundations/layout/applying-layout/window-size-classes |
| ui/theming.md | ThemeExtension 코드 예시, Dynamic Color, AnimatedTheme, 테스트 | https://api.flutter.dev/flutter/material/ThemeExtension-class.html |
| ui/widget-composition.md | Child hoisting, Builder 패턴, 분해 기준, 테스트 | https://docs.flutter.dev/perf/best-practices |
| state/state-management.md | AsyncNotifier 구조, ref.invalidate vs refresh, Provider 선택, 테스트 | https://docs-v2.riverpod.dev/docs/providers/notifier_provider |
| state/hooks.md | 커스텀 훅, useEffect keys 규칙, Props 번들링, 테스트 | https://pub.dev/documentation/flutter_hooks/latest/flutter_hooks/Hook-class.html |
| state/async-patterns.md | FutureBuilder 올바른 사용, Isolate.run, 취소 패턴, Debounce | https://dart.dev/language/isolates |
| quality/performance.md | DevTools, Impeller, 최적화 체크리스트, 메모리 관리 | https://docs.flutter.dev/perf/impeller |
| quality/testing.md | Widget test 기본 구조, Golden test, 테스트 피라미드, Fake vs Mock | https://docs.flutter.dev/cookbook/testing/widget/tap-drag |
| architecture/clean-architecture.md | 디렉토리 구조, UseCase 생략 기준, DI 패턴, 데이터 흐름 | https://docs.flutter.dev/app-architecture/guide |
| architecture/routing.md | GoRouter 설정, ShellRoute, 딥링크+인증, transition | https://pub.dev/documentation/go_router/latest/ |
| architecture/api-layer.md | Retrofit DataSource, DTO 변환, Interceptor, Pagination, 테스트 | https://pub.dev/packages/retrofit |

### 방법론

- 모든 추가 내용에 flutter.dev, pub.dev, dart.dev, m3.material.io 등 공식 출처 URL 포함
- 기존 내용 미삭제 (append-only)
- 코드 예시는 실전 프로젝트 패턴 기반, 최소한의 context로 이해 가능하도록 작성
- 각 문서에 "실전 패턴" + "테스트 전략" + 추가 Gotchas 섹션 보강

### 향후 리서치 백로그

| 우선순위 | 주제 | 예상 출처 | 대상 문서 |
| -------- | ---- | --------- | --------- |
| 높음 | Flutter 4.0 breaking changes | flutter.dev/release | 전체 |
| 높음 | Riverpod 4.0 (예정) code generation 변경 | riverpod.dev | state/state-management.md |
| 중간 | Impeller Android 안정화 상태 | flutter.dev/perf/impeller | quality/performance.md |
| 중간 | Dart macros (stable 이후) | dart.dev/language | architecture/clean-architecture.md |
| 중간 | Material 3 Expressive Theme | m3.material.io | ui/theming.md |
| 낮음 | Flutter web WASM compilation (stable) | docs.flutter.dev/platform-integration/web/wasm | state/async-patterns.md |
| 낮음 | DevTools extensions API | docs.flutter.dev/tools/devtools | quality/performance.md |

### 품질 기준

- 각 문서가 5 원칙 + 2 수치 + 3 안티패턴 + 2 Gotchas 최소 유지
- 코드 예시는 실행 가능한 snippet (import 생략하되 타입은 명확히)
- deprecated API 사용 시 `[deprecated: YYYY-MM]` 태그 필수
- 출처 URL은 분기별로 접근 가능성 확인 (404 발견 시 즉시 대체)

### 관련 카이젠 사이클

- 이번 확충은 flutter-kaizen Phase 5 이후 추가 보강으로, kaizen-orchestrator의 per-kit research-log 정책을 따름
- 다음 `/flutter-kaizen` 실행 시 이 리서치를 기반으로 flutter-toolkit 스킬 Gotchas/Process 개선 예정

---

## 2026-04-12 (2차 — 에코시스템 확충)

**트리거:** manual (research-log 200줄+ 확충 태스크)

### 조사한 소스

| # | 제목 | URL | 유형 | 태그 | 결과 |
|---|------|-----|------|------|------|
| 1 | Flutter 3.41.0 release notes | <https://docs.flutter.dev/release/release-notes/release-notes-3.41.0> | 공식 | [official] | 채택 |
| 2 | What's new in Flutter 3.41 (blog.flutter.dev) | <https://blog.flutter.dev/whats-new-in-flutter-3-41-302ec140e632> | 공식 | [official] | 채택 |
| 3 | Flutter 3.38 & Dart 3.10 (blog.flutter.dev) | <https://blog.flutter.dev/whats-new-in-flutter-3-38-3f7b258f7228> | 공식 | [official] | 채택 |
| 4 | Flutter 3.38 & Dart 3.10 (Foresight Mobile) | <https://foresightmobile.com/blog/flutter-3-38-dart-3-10-november-2025-update> | blog | [blog] | 채택 |
| 5 | Dart language evolution | <https://dart.dev/resources/language/evolution> | 공식 | [official] | 채택 |
| 6 | Announcing Dart 3.10 (blog.dart.dev) | <https://blog.dart.dev/announcing-dart-3-10-ea8b952b088> | 공식 | [official] | 채택 |
| 7 | Riverpod 3.0 What's New | <https://riverpod.dev/docs/whats_new> | 공식 | [official] | 채택 |
| 8 | Riverpod 3.0 (codewithandrea.com) | <https://codewithandrea.com/newsletter/september-2025/> | blog | [blog] | 채택 |
| 9 | riverpod_generator changelog (pub.dev) | <https://pub.dev/packages/riverpod_generator/changelog> | 공식 | [official] | 채택 |
| 10 | Freezed changelog (pub.dev) | <https://pub.dev/packages/freezed/changelog> | 공식 | [official] | 채택 |
| 11 | Dart Macros Discontinued & Freezed 3.0 | <https://alperenderici.medium.com/dart-macros-discontinued-freezed-3-0-released-why-it-happened-whats-new-and-alternatives-385fc0c571a4> | blog | [blog] | 채택 |
| 12 | go_router changelog (pub.dev) | <https://pub.dev/packages/go_router/changelog> | 공식 | [official] | 채택 |
| 13 | auto_route changelog (pub.dev) | <https://pub.dev/packages/auto_route/changelog> | 공식 | [official] | 채택 |
| 14 | flutter_hooks (pub.dev) | <https://pub.dev/packages/flutter_hooks> | 공식 | [official] | 채택 |
| 15 | Impeller rendering engine (docs.flutter.dev) | <https://docs.flutter.dev/perf/impeller> | 공식 | [official] | 채택 |
| 16 | Flutter WASM support (docs.flutter.dev) | <https://docs.flutter.dev/platform-integration/web/wasm> | 공식 | [official] | 채택 |
| 17 | Patrol 4.0 Released (LeanCode) | <https://leancode.co/blog/patrol-4-0-release> | 공식 | [official] | 채택 |
| 18 | patrol changelog (pub.dev) | <https://pub.dev/packages/patrol/changelog> | 공식 | [official] | 채택 |
| 19 | Flutter GenUI SDK (docs.flutter.dev) | <https://docs.flutter.dev/ai/genui> | 공식 | [official] | 채택 |
| 20 | M3 Expressive umbrella issue | <https://github.com/flutter/flutter/issues/168813> | community | [blog] | 채택 |
| 21 | macro_kit (GitHub) | <https://github.com/rebaz94/macro_kit> | community | [blog] | 채택 |
| 22 | build_runner speedups (codewithandrea.com) | <https://codewithandrea.com/newsletter/december-2025/> | blog | [blog] | 채택 |
| 23 | DCM top Flutter features 2025 | <https://dcm.dev/blog/2025/12/23/top-flutter-features-2025/> | blog | [blog] | 채택 |
| 24 | DCM top Dart features 2025 | <https://dcm.dev/blog/2025/12/20/top-dart-features-2025-years/> | blog | [blog] | 채택 |
| 25 | Flutter testing recap 2025 (DEV) | <https://dev.to/3lvv0w/flutter-mobile-testing-methodologies-recap-2025-523j> | blog | [blog] | 채택 |
| 26 | Very Good Ventures critical packages 2024 | <https://verygood.ventures/blog/pub-in-focus-the-most-critical-dart-flutter-packages-of-2024/> | blog | [blog] | 채택 |

### 채택한 인사이트

#### A. Flutter SDK (3.38 → 3.41)

- **Flutter 3.38 (2025-11, Dart 3.10):** Stateful Hot Reload on web 안정화 (기본 활성), `web_dev_config.yaml`로 CORS 프록시/로컬 SSL 설정 가능, Android 16KB 메모리 페이지 필수화 (Google Play 2025-11-01부터) [official] [dated: 2025-11]
- **Flutter 3.41 (2026-02, Dart 3.11):** Impeller on Web 초기 구현 (wimp), 0x0 환경 크래시 수정 (수십 개 위젯), 새 Window Management API (Linux/macOS regular windows, Windows/Linux dialog windows, tooltip/popup windows), `Navigator.popUntilWithResult`, `RepeatingAnimationBuilder`, `DeviceOrientationBuilder`, CarouselView builder 추가 [official] [dated: 2026-02]
- **Flutter 3.41 플랫폼:** CocoaPods → Swift Package Manager 전환 가속, UIScene lifecycle 기본 지원, Material/Cupertino 라이브러리 별도 패키지 분리 진행 중, content-sized Flutter views (하이브리드 앱 자동 리사이즈) [official] [dated: 2026-02]

#### B. Dart 언어 (3.7 → 3.10)

- **Dart 3.7 wildcard variables:** `_` 이름의 로컬 변수/파라미터가 non-binding으로 동작, 여러 번 선언 가능. 패턴 매칭에서 특정 값을 무시할 때 유용 [official] [dated: 2025-05]
- **Dart 3.8 formatter 개선:** trailing comma 자동 배치 지능화 — 강제 분할 대신 컴파일러가 판단. 코드 출력 스타일 개선 [official] [dated: 2025-08]
- **Dart 3.10 dot shorthands:** `.center` 대신 `MainAxisAlignment.center` 생략 가능. enum, static member, constructor에 모두 적용. UI-heavy 파일에서 보일러플레이트 10-15% 감소 추정 [official] [dated: 2025-11]
- **Dart 3.10 build hooks 안정화:** `hook/build.dart` 스크립트로 네이티브 코드 컴파일/번들을 빌드 시 자동 실행 [official] [dated: 2025-11]
- **Dart macros 중단 (2025-01):** Dart 팀이 macro 기능 개발을 무기한 중단 발표. JIT/AOT 컴파일, tree-shaking, reflection 부재로 구현 복잡도가 너무 높았음. build_runner 기반 코드 생성이 당분간 유일한 경로 [official] [dated: 2025-01]

#### C. Riverpod 3.0 (2025-09)

- **API 통합:** AutoDispose/Family 변형 제거, `Notifier`와 `FamilyNotifier` 통합, `Ref` 서브클래스 단일화 [official] [dated: 2025-09]
- **Offline Persistence (실험):** Provider를 SQLite 등에 영속화 가능. 앱 재시작 시 복원 [official] [dated: 2025-09]
- **Mutations (실험):** 폼 제출 등 사이드이펙트에 loading/success/error 상태 자동 관리 [official] [dated: 2025-09]
- **Automatic Retry:** 초기화 실패 시 exponential backoff으로 자동 재시도 [official] [dated: 2025-09]
- **Ref.mounted:** async 작업 후 Provider 유효성 체크 (`BuildContext.mounted`와 동일 패턴) [official] [dated: 2025-09]
- **Pause/Resume:** `ref.listen` 리스너를 수동 일시정지/재개 가능. 화면 비가시 시 자동 일시정지 [official] [dated: 2025-09]
- **테스트:** `ProviderContainer.test()` (자동 정리), `overrideWithBuild` (선택적 모킹), `overrideWithValue` 복원 [official] [dated: 2025-09]
- **riverpod_generator:** 타입 파라미터 지원, Family 인자 override 2 파라미터, Mutation 지원 추가 [official] [dated: 2025-09]

#### D. Freezed 3.x (2025-07 → 2026-02)

- **Freezed 3.2.0 (2025-07):** Mixed mode 도입 — 기존 union 문법 + 간단 class 선언 혼용 가능. `map`/`when` 메서드 제거, Dart 3 패턴 매칭으로 대체. "eject union cases" 기능 추가 [official] [dated: 2025-07] — **[정정 2026-08-13]** 제거는 **3.0** 의 breaking 이었고 **3.1.0 에서 재추가**됐다. 3.2.0 을 제거 시점으로 적은 것은 오기다
- **Freezed 3.2.5 (2026-02):** analyzer 10.0 지원. 3.2.3~3.2.5는 analyzer/source_gen/build 의존성 호환 범위 확장 [official] [dated: 2026-02]
- **json_serializable 호환:** Freezed 3.2.3 + json_serializable 6.11.3에서 analyzer >=9/build >=4 호환 이슈 보고됨. 버전 핀닝 주의 필요 [community] [dated: 2025-09]

#### E. 라우팅

- **go_router 17.2.0:** `TypedQueryParameter`로 쿼리 파라미터 이름 커스텀 인코딩/디코딩, `refreshListenable` 콜백 유실 수정. 17.0.0에서 `ShellRoute`가 기본으로 GoRouter observer에 알림 (breaking change), `notifyRootObserver` 파라미터 추가. 최소 SDK: Flutter 3.32/Dart 3.8 [official] [dated: 2026-04]
- **auto_route 11.1.0:** `.named` 생성자로 코드 생성 없이 shorthand named route 지원. 11.0.0에서 `redirect` → `redirectUntil` 리네이밍 (breaking), deprecated named navigation 메서드 제거 (`navigateNamed`, `pushNamed` 등). 10.3.0에서 `AutoRouteGuard` async 지원 + 네비게이션 히스토리 추적 [official] [dated: 2026-01]

#### F. flutter_hooks

- **flutter_hooks 0.21.3+1:** 현재 최신 안정 버전. Android/iOS/Linux/macOS/Web/Windows 전 플랫폼 지원. React hooks 패턴의 Flutter 구현체로 안정기 진입 [official] [dated: 2025-09]

#### G. 테스팅

- **Patrol 4.x:** Web 플랫폼 지원 추가, VS Code 확장, 디버깅 개선. 4.5.0에서 `dart.library.js_interop` 마이그레이션, Android API 36 에뮬레이터 지원, iOS 18+ 알림 인덱싱 일관성 수정. 월 200K 다운로드, E2E 테스팅 사실상 표준 [official] [dated: 2026-03]
- **Golden testing:** `alchemist`가 중단된 `golden_toolkit` 대체. CI/CD 파이프라인 통합이 표준 관행으로 정착 [blog] [dated: 2025-12]
- **테스트 피라미드:** unit 다수 → widget 중간 → integration 최소 구조 유지. Widget test에서 `find.byType` + `tester.tap` + `tester.pumpAndSettle` 기본 패턴 [official]

#### H. 성능 & 렌더링

- **Impeller 상태 (2026-04):** iOS 필수 (Skia 전환 불가), Android API 29+ 기본 (Vulkan 없으면 OpenGL 폴백), macOS 실험적 (플래그 활성화 필요), Web/Windows/Linux 미지원. Android에서 frame drop 12% → 1.5% (Skia 대비 실측치, e-커머스 앱) [official] [dated: 2026-04] — **[정정 2026-08-13]** **macOS / Linux / Windows 는 Flutter 3.47 부터 Impeller 기본**이다. Web 만 Skia
- **Impeller on Web (wimp):** Flutter 3.41에서 초기 구현 시작. 현재 Web은 `canvaskit`/`skwasm` 사용 [official] [dated: 2026-02]
- **Shader compilation jank 해소:** Impeller는 AOT 셰이더 컴파일로 JIT 컴파일 잔버벅 제거. 복잡 UI에서 평균 래스터화 시간 50% 감소 [official]

#### I. Web & WASM

- **WASM stable (Flutter 3.24+):** `flutter build web --wasm`으로 프로덕션 빌드 가능. WasmGC 필요 (Chrome 119+). Firefox/Safari는 호환 버그 있음, iOS 전면 미지원 (WebKit) [official] [dated: 2025-11]
- **성능:** WASM 앱이 JS 대비 로딩 40% 빠르고 메모리 30% 절감 (Flutter 팀 2025 벤치마크) [official] [dated: 2025-11]
- **JS interop 전환:** `dart:html`, `package:js` 폐기 예정 → `package:web` + `dart:js_interop`으로 마이그레이션 필수. WASM 호환 interop 모델 [official] [dated: 2025-11]
- **폴백:** WasmGC 미지원 브라우저에서 자동으로 JS 렌더러로 폴백 [official]

#### J. AI 통합

- **GenUI SDK (alpha):** LLM이 Flutter 위젯 카탈로그로 UI를 동적 생성. 텍스트 대화 → 리치 인터랙티브 UI 변환 오케스트레이션 레이어. 2026년 beta/production 전환 예상 [official] [dated: 2025-12]
- **Flutter AI Toolkit v1.0 (2025-12):** 사전 빌드 채팅 위젯, 멀티턴 함수 호출, 음성-텍스트 변환 [official] [dated: 2025-12]
- **Flutter MCP server + AI Rules:** Google I/O 2025에서 Flutter를 "agentic apps" 프레임워크로 포지셔닝 [official] [dated: 2025-05]

#### K. 코드 생성 & 도구

- **build_runner 2x 속도 향상:** transitive import 추적 전면 재작성. 3,000 생성 라이브러리 테스트에서 2배 속도 [blog] [dated: 2025-12]
- **macro_kit:** build_runner 없이 즉시 코드 생성 (초기 3-5초, 이후 100ms 미만). 커뮤니티 대안, 아직 초기 단계 [community] [dated: 2025-11]
- **Freezed 3.x + Dart 3 switch:** `when`/`map` 제거 → `switch` expression + sealed class 패턴 매칭이 표준 [official] [dated: 2025-07] — **[정정 2026-08-13]** `when`/`map` 재추가(3.1.0) 이후로는 "표준" 이 아니라 **신규 코드 권장**이다

#### L. 디자인 시스템

- **Material 3 Expressive:** M3E는 감정적 UX를 위한 M3 확장. Flutter 팀은 Material/Cupertino 패키지 분리 후 새 패키지에서 M3E 작업 예정 (현재 기여 미수락). 커뮤니티 패키지 `tofu_expressive` 존재 [community] [dated: 2025-07]
- **Material/Cupertino 분리:** 3.41부터 본격화. 별도 패키지로 독립 버전/릴리스 가능하게 됨. 디자이너가 더 빠르게 업데이트 출시 가능 [official] [dated: 2026-02]

#### M. 플랫폼 특화

- **iOS:** Swift Package Manager 전환 가속 (CocoaPods 대체), UIScene lifecycle 기본 [official] [dated: 2026-02]
- **Desktop:** Flutter 3.41에서 Linux/macOS regular window, Windows/Linux dialog window, tooltip/popup window API 추가 [official] [dated: 2026-02]
- **Hybrid apps:** content-sized Flutter views로 고정 치수 요구 제거 [official] [dated: 2026-02]

#### N. 인기 패키지 동향

- **상태 관리:** Riverpod이 사실상 표준. Bloc은 streams/events 기반 대안으로 건재 [blog] [dated: 2025-12]
- **핵심 패키지 (criticality score 기준):** flutter_rust_bridge, riverpod, bloc, freezed, drift, flutter_inappwebview, get, chopper, file_picker [blog] [dated: 2024-12]
- **pub.dev 생태계:** 50,000+ 패키지 등록. 상위 패키지 품질은 매우 높은 수준 [community]

### 폐기 사유

- 없음 — 모든 URL 접근 가능 확인, 내용 일치 검증 완료

### flutter-toolkit 스킬 개선 포인트

| 스킬 | 개선 영역 | 근거 소스 |
|------|-----------|-----------|
| flutter-provider | Riverpod 3.0 Mutations, Offline Persistence, Pause/Resume Gotchas 추가 | #7, #8 |
| flutter-api | Freezed 3.2 Mixed mode + `when`/`map` 제거 마이그레이션 Gotchas — **[정정 2026-08-13]** 3.1.0 재추가로 제거 단정은 철회, 일관성 우선으로 개정 | #10, #11 |
| flutter-screen | go_router 17.0 `notifyRootObserver` breaking change 경고 | #12 |
| flutter-transition | auto_route 11.0 `redirect` → `redirectUntil` 리네이밍 경고 | #13 |
| flutter-build | Dart 3.10 dot shorthands + build_runner 2x 속도 향상 반영 | #5, #22 |
| flutter-test | Patrol 4.x Web 지원, alchemist golden test 전환 가이드 | #17, #18, #25 |
| flutter-hooks | flutter_hooks 안정기 확인, 큰 변경 없음 | #14 |
| flutter-responsive | WASM 폴백 메커니즘 + Web hot reload 안정화 반영 | #16 |
| flutter-audit | Impeller 플랫폼별 상태 체크리스트 추가 | #15 |
| flutter-widget | RepeatingAnimationBuilder, DeviceOrientationBuilder 신규 위젯 가이드 | #1 |

### 향후 리서치 백로그 (갱신)

| 우선순위 | 주제 | 예상 출처 | 대상 문서 | 상태 |
|----------|------|-----------|-----------|------|
| 높음 | Flutter 3.44+ (2026 Q2 예정) | flutter.dev/release | 전체 | 미착수 |
| 높음 | Riverpod Offline Persistence 안정화 | riverpod.dev | state/state-management.md | 미착수 |
| 높음 | Impeller on Web (wimp) 진행 상황 | docs.flutter.dev/perf/impeller | quality/performance.md | 미착수 |
| 중간 | GenUI SDK beta 전환 | docs.flutter.dev/ai/genui | 신규 문서 | 미착수 |
| 중간 | Material/Cupertino 패키지 분리 완료 | flutter.dev | ui/theming.md | 미착수 |
| 중간 | M3 Expressive Flutter 구현 시작 | github.com/flutter/flutter/issues/168813 | ui/theming.md | 미착수 |
| 중간 | macro_kit 성숙도 평가 | github.com/rebaz94/macro_kit | architecture/clean-architecture.md | 미착수 |
| 낮음 | Firefox/Safari WasmGC 호환 진행 | docs.flutter.dev/platform-integration/web/wasm | state/async-patterns.md | 미착수 |
| 낮음 | DevTools extensions API | docs.flutter.dev/tools/devtools | quality/performance.md | 미착수 |
| ~~높음~~ | ~~Dart macros (stable 이후)~~ | — | — | **폐기** (macro 개발 중단 확정) |

### PR

- 개선 포인트 확인 완료. 다음 `/flutter-kaizen` 실행 시 위 테이블 기반으로 스킬 Gotchas/Process 업데이트 예정

---

## 2026-04-12 (3차 — 최신 에코시스템 보강)

**트리거:** manual (`LATEST 2025-2026` 재검증 + research-log append-only 갱신)

### 조사한 소스

| # | 제목 | URL | 유형 | 태그 | 결과 |
|---|------|-----|------|------|------|
| 27 | Breaking changes and migration guides | <https://docs.flutter.dev/release/breaking-changes> | 공식 | [official] [dated: 2026-04] | 채택 |
| 28 | Changing RawMenuAnchor close order | <https://docs.flutter.dev/release/breaking-changes/raw-menu-anchor-close-order> | 공식 | [official] [dated: 2026-03] | 채택 |
| 29 | Migrating Flutter Android app to Android Gradle Plugin 9.0.0 | <https://docs.flutter.dev/release/breaking-changes/migrate-to-agp-9> | 공식 | [official] [dated: 2026-02] | 채택 |
| 30 | Migrating Flutter Android projects to built-in Kotlin | <https://docs.flutter.dev/release/breaking-changes/migrate-to-built-in-kotlin> | 공식 | [official] [dated: 2026-04] | 채택 |
| 31 | Hooks | <https://dart.dev/tools/hooks> | 공식 | [official] [dated: 2026-02] | 채택 |
| 32 | Variables (wildcard variables) | <https://dart.dev/language/variables> | 공식 | [official] [dated: 2025-11] | 채택 |
| 33 | flutter_riverpod changelog | <https://pub.dev/packages/flutter_riverpod/changelog> | 공식 | [official] [dated: 2026-03] | 채택 |
| 34 | Impeller rendering engine | <https://docs.flutter.dev/perf/impeller> | 공식 | [official] [dated: 2026-03] | 채택 |
| 35 | GenUI SDK main components and concepts | <https://docs.flutter.dev/ai/genui/components> | 공식 | [official] [dated: 2026-03] | 채택 |
| 36 | DevTools extensions | <https://docs.flutter.dev/tools/devtools/extensions> | 공식 | [official] [dated: 2025-10] | 채택 |
| 37 | Casual Games Toolkit | <https://docs.flutter.dev/resources/games-toolkit> | 공식 | [official] [dated: 2026-03] | 채택 |
| 38 | flame | <https://pub.dev/packages/flame> | 공식 | [official] [dated: 2026-04] | 채택 |
| 39 | flame changelog | <https://pub.dev/packages/flame/changelog> | 공식 | [official] [dated: 2026-04] | 채택 |
| 40 | Overview \| Shorebird | <https://docs.shorebird.dev/code-push/> | 공식 | [official] [dated: 2026-03] | 채택 |
| 41 | Protect your Flutter iOS apps with Shorebird Obfuscation | <https://shorebird.dev/blog/obfuscation-on-ios> | blog | [blog] [dated: 2026-02] | 채택 |
| 42 | Flutter Version Management \| Shorebird | <https://docs.shorebird.dev/getting-started/flutter-version/> | 공식 | [official] [dated: 2026-03] | 채택 |
| 43 | Releases · shorebirdtech/shorebird | <https://github.com/shorebirdtech/shorebird/releases> | community | [community] [dated: 2025-11] | 채택 |
| 44 | Flutter \| Maestro Docs | <https://docs.maestro.dev/get-started/supported-platform/flutter> | 공식 | [official] [dated: 2026-03] | 채택 |
| 45 | Core Selectors \| API Reference \| Maestro Docs | <https://docs.maestro.dev/reference/selectors/core-selectors> | 공식 | [official] [dated: 2026-03] | 채택 |

### 주요 인사이트 (신규)

- **Flutter 3.44 예정 변경점:** 2026-04-12 기준 Flutter 3.44 정식 release note/announcement는 아직 없고, 공식 breaking changes 인덱스에는 pre-stable 항목으로 `RawMenuAnchor` close 순서 변경, `onReorder` 폐기, `cacheExtent`/`cacheExtentStyle` 폐기, `TextInputConnection.setStyle` 폐기, `IconData` final 처리, AGP 9.0 마이그레이션, page transition builders 재구성이 공개됨 [official] [dated: 2026-04]
- **Android 빌드 체인 변화:** AGP 9.0 문서는 아직 plugin 호환성이 완전하지 않다고 명시하며, 당장은 `android.newDsl=false` 같은 임시 플래그가 필요할 수 있다. 별도 built-in Kotlin 마이그레이션 문서가 2026-04에 추가되어 AGP 9 전환 준비가 본격화됐다 [official] [dated: 2026-04]
- **Dart build hooks 정식 문서화:** Dart 3.10부터 `hook/build.dart` 기반 build hooks가 공식 문서에 포함됐고, native assets 컴파일/다운로드 같은 빌드 단계 자동화가 정식 경로로 안내된다 [official] [dated: 2026-02]
- **Wildcard variables 재확인:** `_` wildcard variable은 Dart 3.7+ 기능으로, Dart 3.10 신규 기능은 아니다. 따라서 "Dart 3.10+ 최신 기능" 범주에서는 dot shorthands/build hooks가 핵심이고 wildcard variables는 이미 선행 도입 기능으로 봐야 한다 [official] [dated: 2025-11]
- **Riverpod 3.0 안정화 상태:** Offline Persistence와 Mutations는 여전히 experimental 상태이며, 2026-03의 `flutter_riverpod` 3.3.1/3.3.0 및 2026-01의 3.2.0에서도 안정화 선언은 없었다. 대신 pause/resume 후 알림 누락 수정, `Ref.isPaused`, `disposeNotifier: false` 등 후속 API/버그 수정이 진행됐다 [official] [dated: 2026-03]
- **Impeller 진행 상황:** 2026-03 공식 문서 기준 Web은 여전히 `canvaskit`/`skwasm`가 Skia를 사용하며 "future" 상태이고, macOS는 opt-in 플래그 기반 시험 사용이다. Windows/Linux 지원 표시는 여전히 없다 [official] [dated: 2026-03] — **[정정 2026-08-13]** macOS/Linux/Windows 는 **Flutter 3.47 부터 Impeller 기본**으로 전환됐다
- **GenUI beta 전환 상태:** 2026-04-12 기준 공식 문서상 `genui`는 여전히 alpha/experimental이며, beta 전환 공지는 확인되지 않았다. 다만 2026-03 기준 components/get-started 문서가 확장되어 `Conversation`, `Catalog`, `DataModel`, input-events 흐름 등 개념 문서가 보강됐다 [official] [dated: 2026-03]
- **DevTools 최신 보강:** Flutter SDK에 번들되는 DevTools는 2025-10 문서 기준 inspector/layout/performance/cpu/network/memory/app size/deep link validation을 제공하며, DevTools extensions 문서가 별도로 정리되어 third-party package가 새 탭 형태로 DevTools에 통합되는 경로가 공식화됐다 [official] [dated: 2025-10]
- **Casual Games Toolkit 최신 상태:** 2026-03 문서 기준 toolkit은 basic/card/endless runner 3개 템플릿과 Flame 기반 SuperDash 데모, Ads/IAP/Firebase/Game Services 연동 자료를 계속 제공한다. 새 템플릿 추가는 확인되지 않았다 [official] [dated: 2026-03]
- **Flame 최신 릴리스:** 2026-04 기준 Flame 최신 버전은 `1.37.0`이며, `OverlayManager.setActive()`, `HueEffect`/`HueDecorator`, `HasAutoBatchedChildren` 등이 추가됐다. 직전 1.36.0에서는 최소 Flutter 버전이 3.41.0으로 상향되고 hot reload 전파, `ComponentPool`, `IconComponent` 등이 추가됐다 [official] [dated: 2026-04]
- **Shorebird 최신 상태:** 확인 가능한 최신 GitHub release는 `v1.6.70`(2025-11)이며, 공식 docs는 Code Push가 Android/iOS에서 동작하고 Dart 코드 및 Dart dependency 변경은 패치 가능하지만 assets/native code/Flutter engine 변경은 패치 대상이 아니라고 명시한다. Flutter version management 문서에는 desktop release 지원 최소 버전도 명시돼 있다 [official] [dated: 2026-03]
- **Shorebird 보안 기능 업데이트:** 2026-02 공식 블로그 기준 iOS에서도 `--obfuscate`가 first-class CLI 플래그로 지원되며, release에서 설정한 obfuscation이 patch에도 자동 승계된다 [blog] [dated: 2026-02]
- **Patrol 이후 대안 테스팅 접근:** Maestro는 Flutter를 first-class 지원 대상으로 문서화했고, Semantics label/identifier를 기준으로 black-box E2E를 수행한다. Flutter `Key`는 접근성 레이어에 노출되지 않으므로 selector로 쓰지 못한다는 점을 명시한다. 다만 2026-03 문서 기준 Flutter Desktop은 아직 미지원이고 Flutter Web은 지원한다 [official] [dated: 2026-03]

### 신규 공백 / 확인 결과

- **Flutter 3.44 release notes:** 공식 release note/announcement 자체는 아직 없음. pre-stable migration docs 수준까지만 확인 가능
- **Riverpod Offline Persistence 안정화:** experimental 해제/정식 안정화 공지 없음
- **Riverpod Mutations 안정화:** experimental 해제/정식 안정화 공지 없음
- **GenUI beta 전환:** beta 공지 없음, alpha 유지 확인
- **Impeller on Windows/Linux/Web 정식 지원:** 신규 지원 발표 없음
- **Casual Games Toolkit 신규 템플릿:** 2026-03 문서 기준 새 템플릿 확인되지 않음
