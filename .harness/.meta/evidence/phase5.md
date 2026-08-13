---
phase: 5
title: "Phase 5 flutter-toolkit — 확보된 외부 근거"
collected: 2026-08-13
method: codex (foreground, 직접 호출)
note: 이 파일이 이 Phase 의 유일한 외부 근거다. 바깥 자료를 새로 찾지 마라. 여기 없는 URL·수치를 지어내지 마라.
---

출처 유형: Codex

검색 6/10회 사용. 파일은 읽기 전용으로만 확인했다.

**1. 관찰 사실**

G1. 기존 컴포넌트 미재사용  
공식 Flutter Agent Plugins는 “skills/rules로 반복 가능한 워크플로우를 주입해 agent mistake를 줄인다”는 형태를 1차 기법으로 제시한다. 즉 “기존 컴포넌트 우선 탐색”은 프레임워크 API 문제가 아니라 agent skill의 강제 절차 문제다. 출처: https://github.com/flutter/agent-plugins  
추론: 확립된 기법은 “Enumerate-before-Act + 파일 본문 Read + 후보 선택”이다. 로컬 `flutter-widget`에는 유사 조항이 이미 있지만, `Divider`, `Button`, `Chip`, `ListTile` 같은 Flutter 기본 위젯 사용 전 “DS 컴포넌트 검색”을 직접 강제하지 않는다. 특히 `flutter-screen` 템플릿은 기본 `Scaffold/AppBar/Text` 생성 중심이라 DS 재사용 게이트가 약하다.

G2. Riverpod invalidate 누락  
Riverpod 현행 문서는 `ref.watch`를 기본 선언형 구독으로, `ref.listen`을 dialog/navigation/logging 같은 side effect용으로 구분한다. `ref.invalidate`는 현재 state를 버리고 다음 read 때 재평가, `ref.refresh`는 invalidate 후 read의 sugar다. 출처: https://riverpod.dev/docs/concepts2/refs  
`autoDispose`는 listener가 0이 된 뒤 한 프레임 후 dispose되며, provider가 recompute되면 autoDispose 여부와 무관하게 기존 state가 파괴된다. family/parameter provider는 autoDispose 권장이다. 출처: https://riverpod.dev/docs/concepts2/auto_dispose  
중요: flutter_riverpod 3.4.x changelog에는 scoped `ProviderScope/ProviderContainer` override 환경에서 `invalidate/refresh`가 provider/family를 못 찾던 버그 수정과, `Ref.onManualInvalidation()` 추가가 있다. 수동 invalidation 전파 패턴을 공식 changelog가 예시로 제시한다. 출처: https://pub.dev/packages/flutter_riverpod/changelog  
로컬 결함: `flutter-provider`는 invalidate/refresh 차이를 짧게만 설명하고, “파생 provider가 어떤 source를 watch해야 stale cache가 안 나는지”와 “write 메서드 후 어떤 provider를 invalidate해야 하는지”를 체크리스트화하지 않는다.

G3. Riverpod + widget test 하네스  
Riverpod 공식 testing 문서는 unit test에서 `ProviderContainer.test()`를 쓰고 컨테이너를 테스트 간 공유하지 말라고 한다. autoDispose provider는 `container.read`만 하면 중간에 dispose될 수 있어 `container.listen`으로 붙잡으라고 한다. 출처: https://riverpod.dev/docs/how_to/testing  
widget test는 `tester.pumpWidget(ProviderScope(child: ...))`가 기본이고, provider 접근이 필요하면 `tester.container()`를 쓴다. override는 `ProviderScope`나 `ProviderContainer`의 `overrides` 파라미터로 한다. 출처: https://riverpod.dev/docs/how_to/testing  
로컬 결함: `flutter-test`는 `ProviderContainer`와 `ProviderScope`를 언급하지만 “화면 상태 반영 하네스”, “override + action + pump + assertion”, “16종 매핑이면 대표 2종만 검증 금지” 같은 coverage 기준이 없다.

G4. 성능 조사 전 환경 배제  
Flutter 공식 성능 문서는 “거의 모든 성능 디버깅은 물리 Android/iOS 기기 + profile mode에서” 하며, debug mode나 simulator/emulator 성능은 release behavior를 대표하지 않는다고 명시한다. 출처: https://docs.flutter.dev/perf/ui-performance  
build modes 문서도 profile mode는 emulator/simulator에서 disabled이며 실제 성능 대표성이 없다고 한다. 출처: https://docs.flutter.dev/testing/build-modes  
Impeller 문서는 iOS는 Skia 전환 불가, Android API 29+ 기본, Web은 Skia, macOS/Linux/Windows는 Flutter 3.47부터 Impeller 기본이라고 한다. 출처: https://docs.flutter.dev/perf/impeller  
로컬 결함: `docs/flutter/quality/performance.md`는 profile/DevTools는 말하지만 “실기기 우선, simulator 결과로 앱 최적화 시작 금지”가 약하고, Impeller 상태도 2026-04 기준으로 낡았다.

현행 버전에서 낡은 지점  
Flutter 릴리스 인덱스는 현재 stable 목록 최상단을 3.47.0으로 표시한다. 로컬 스킬 일부는 3.44/3.41 기준이다. 출처: https://docs.flutter.dev/release/release-notes  
3.47 발표는 Android dependency matrix를 Java 17, KGP 2.4.0, AGP 9.1.0, Gradle 9.3.1로 제시한다. 출처: https://flutter.dev/blog/whats-new-in-flutter-3-47  
Freezed 최신 stable은 3.2.5이고, 3.0에서 `.when/.map` 제거가 breaking이었지만 3.1.0에서 `when/map`이 다시 추가됐다. 따라서 “Freezed 3부터 when/map 제거”를 절대 규칙으로 쓰면 낡은 조항이다. 권장 문구는 “Dart switch 우선, 기존 프로젝트가 Freezed 3.1+ generated when/map을 이미 쓰면 일관성 고려”가 맞다. 출처: https://pub.dev/packages/freezed/changelog

**2. 권장안**

G1 조항  
스킬에 넣을 문구: “Flutter 기본 UI 위젯을 쓰기 전, 같은 의미의 프로젝트 컴포넌트를 전수 검색한다. 검색 대상: `lib/**/design_system`, `lib/**/components`, `lib/**/widgets`, `lib/**/ui`. 예: `Divider`를 쓰기 전 `rg -n "class .*Divider|IFDivider|Divider\\(" lib/` 결과를 확인하고, 기존 DS 컴포넌트가 있으면 그것을 우선 사용한다.”  
추가: `flutter-screen`, `flutter-widget`, `flutter-audit`, `widget-inspector`에 “Primitive Substitution Gate”를 공통 규칙으로 넣는다. `Divider/Button/Chip/Card/ListTile/Switch/TextField/CircularProgressIndicator` 직접 사용은 HAS_DS=true에서 감사 대상.  
넣지 말 것: “모든 기본 위젯 금지.” `Text`, `Row`, `Column`, `Padding`, `SizedBox` 같은 layout primitive까지 금지하면 과잉 규칙이 된다.

G2 조항  
스킬에 넣을 문구: “파생 provider는 source state를 반드시 `ref.watch(sourceProvider.select(...))`로 선언형 연결한다. 파생값을 `ref.read`로 계산해 캐시하지 않는다.”  
쓰기 메서드 규칙: “색상/테마/멤버십/권한처럼 화면 캐시에 영향을 주는 mutation 후에는 영향 provider 목록을 작성하고 `ref.invalidate(affectedProvider)`를 호출한다. 즉시 새 값이 필요할 때만 `ref.refresh`를 사용한다.”  
Riverpod 3.4.x 보강: “manual invalidation을 감춰야 하는 파생 provider는 `ref.onManualInvalidation`으로 source invalidation을 전파할 수 있다. 단 이 API 사용은 changelog 기준으로 확인하고 프로젝트 Riverpod 버전이 지원할 때만.”  
넣지 말 것: “모든 mutation 후 전체 family invalidate.” stale은 줄지만 네트워크 재요청과 UX 흔들림이 커진다.

G3 조항  
스킬에 넣을 문구: “Riverpod widget test 하네스 기본형은 `ProviderScope(overrides: [...], child: MaterialApp(...page))`; test 내부에서 `final container = tester.container();`; action 후 `await tester.pump()` 또는 필요한 duration pump; UI와 provider state를 함께 assert한다.”  
coverage 조항: “매핑/variant가 N종이면 최소 happy path 1개가 아니라 boundary/representative set를 정한다. 16종 mapping은 2종만 검증 금지, 최소 all mapping table test 또는 generated fixture loop로 전수 검증.”  
넣지 말 것: “위젯 테스트에서 ProviderContainer만 단독 사용.” 화면 렌더링 검증은 `ProviderScope` 루트가 필요하다.

G4 조항  
스킬에 넣을 문구: “성능 최적화 전 Environment Exclusion Checklist 필수: profile mode 여부, physical device 여부, simulator/emulator 사용 여부, OS uptime/swap/memory pressure, DevTools trace export, renderer(Impeller/Skia), target refresh rate, slowest target device를 기록한다.”  
판정 규칙: “simulator/emulator/debug 결과만 있으면 앱 코드 성능 병목으로 확정하지 말고 `[미검증]` 처리한다.”  
넣지 말 것: “iOS simulator jank = 앱 버그.” 공식 문서 기준으로 대표성이 없다.

**3. 트레이드오프**

DS 컴포넌트 전수 검색은 생성 시간이 늘지만, RE-02 같은 재작업 비용을 줄인다. 빠른 생성 스킬에는 quick search, audit에는 deep search로 나누는 편이 현실적이다.

Riverpod invalidation을 명시화하면 stale cache는 줄지만 dependency graph 문서화 부담이 생긴다. 대신 mutation 메서드 옆에 affected providers를 짧게 유지하면 리뷰 가능성이 올라간다.

테스트 전수 매핑은 초기 작성량이 늘지만, 16종 중 2종만 검증하는 false confidence를 줄인다. table-driven test로 비용을 낮출 수 있다.

성능 환경 배제는 앱 코드 최적화 착수를 늦추지만, simulator/render host/swap 같은 외부 원인을 먼저 걸러 불필요한 리팩터를 막는다.

**4. 열린 질문**

fit-pal의 DS 컴포넌트 네이밍 규칙이 `IF*`로 안정적인가? 그렇다면 `IFDivider`, `IFButton` 같은 allowlist를 스킬에 박아도 된다.

`groupDetailDataProvider`가 palette provider를 `watch`할 수 있는 순수 파생 provider인가, 아니면 repository fetch cache인가? 전자는 watch 연결, 후자는 mutation 후 invalidate 경계가 맞다.

Riverpod 최소 버전이 3.4.x 이상으로 고정되어 있는가? `onManualInvalidation` 조항은 버전 가드가 필요하다.

성능 QA에서 실기기 확보가 항상 가능한가? 불가능하면 simulator 결과는 “환경 의심” 등급으로만 쓰고, profile trace export와 시스템 메모리 상태를 함께 보관해야 한다.
