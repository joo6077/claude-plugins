# Flutter 공식 AI Rules 요약

> 출처: [flutter/flutter/docs/rules/rules.md](https://raw.githubusercontent.com/flutter/flutter/refs/heads/main/docs/rules/rules.md)
> 최종 확인: 2026-04-11

Flutter 공식 AI rules는 LLM이 Flutter 코드를 생성할 때 따라야 할 패턴을 정의한다.
flutter-toolkit 스킬은 이 규칙과 정합성을 유지해야 한다.

## 위젯 패턴

- **Composition Over Inheritance** — 복잡한 위젯은 상속이 아닌 합성으로 구성
- **Private Widget Class** — 헬퍼 메서드(`_buildHeader()`)가 아닌 private Widget 클래스로 추출
- **Const Constructor** — 가능한 모든 곳에 `const` 사용하여 리빌드 최소화
- **Build 분리** — 큰 `build()` 메서드는 작은 private 위젯으로 분해

## State Management (서드파티 패키지 없을 때)

공식 우선순위:
1. `ValueNotifier` + `ValueListenableBuilder` — 단일 값
2. `Stream` + `StreamBuilder` — 비동기 이벤트 시퀀스
3. `Future` + `FutureBuilder` — 일회성 비동기
4. `ChangeNotifier` + `ListenableBuilder` — 복합/다중 위젯 상태
5. MVVM 패턴 — 복잡한 앱

> 프로젝트에 Riverpod/Bloc이 있으면 해당 패키지 패턴을 따른다.

## 아키텍처

- **레이어 분리:** Presentation → Domain → Data → Core
- **대규모 프로젝트:** Feature-first 구조 (feature 내 presentation/domain/data)
- **MVVM:** View ↔ ViewModel (1:1) ↔ Repository ↔ Service

## Do's

- `go_router` 네비게이션 (딥링크, 웹 지원)
- SOLID 원칙
- `dart:developer.log` 사용 (`print()` 금지)
- `compute()` 사용 (비용 큰 연산은 Isolate)
- 모든 public API에 `///` 문서화
- `dart_format`, `dart_fix` 도구 활용
- 다양한 화면 크기 테스트

## Don'ts

- `print()` 사용 금지 → `dart:developer.log`
- `build()` 내 네트워크 호출 금지
- 같은 Row/Column에 `Flexible` + `Expanded` 혼용 금지
- `!` 연산자 남용 금지 (non-null 보장된 경우만)
- 깊은 위젯 트리 중첩 금지 → 합성으로 분해

## 코드 생성

- JSON 직렬화: `json_serializable` + `json_annotation`
- `fieldRename: FieldRename.snake` 사용
- `build_runner`: `dart run build_runner build --delete-conflicting-outputs`

## 테스팅

- Arrange-Act-Assert 구조
- Mock보다 Fake/Stub 선호
- Unit → Widget → Integration 순서
- 높은 테스트 커버리지 목표

## 라인 길이

- 최대 80자

## 2026 생태계 노트 (Riverpod 3.0 / Freezed 3.0 / go_router / Flutter 3.29+)

> 최종 리서치: 2026-04-11 (WebSearch)

Flutter 공식 rules 외에 2026 기준으로 flutter-toolkit 이 추가로 정합해야 하는 생태계 변화 요약. 모든 항목에 출처 URL 포함.

### Riverpod 3.0

- `Ref.mounted` 공식 패턴 — disposed Notifier 접근 시 에러 throw. async 메서드 끝에 `if (!ref.mounted) return;` 필수. 출처: <https://riverpod.dev/docs/whats_new>
- Notifier 재생성 라이프사이클 — 2.x pseudo-singleton 폐기. Timer/StreamSubscription/Controller 를 Notifier 필드로 유지하면 리소스 누수. 별도 provider + `ref.onDispose` 로 분리. 출처: <https://riverpod.dev/docs/3.0_migration>
- `StateNotifierProvider` / `StateProvider` / `ChangeNotifierProvider` 는 legacy. 신규 코드는 `@riverpod` / `Notifier` 기반. 출처: <https://pub.dev/packages/flutter_riverpod/changelog>
- Ref 의 타입 파라미터 제거 — `FutureProviderRef` 등 subclass 전부 삭제, `Ref` 직접 사용
- `==` 기반 알림 필터링 — `StreamProvider`/`StreamNotifier` 동등성 이벤트가 listener 에 전달되지 않음. 모델의 `operator ==` / `hashCode` 정의가 알림 동작을 결정
- `.valueOrNull` → `.value` 로 변경. `dart fix --apply` 로 자동 마이그레이션 가능

### Freezed 3.0

- `@freezed abstract class` (단일) / `@freezed sealed class` (union) 필수. factory 생성자만 있는 class 는 이제 abstract 또는 sealed 여야 한다. 출처: <https://pub.dev/packages/freezed/changelog>
- union 분기는 Dart pattern matching (switch expression) 을 신규 코드에서 권장. **단 `.when` / `.map` 이 영구 제거된 것은 아니다** — 3.0 에서 제거됐다가 **3.1.0 에서 다시 추가**됐고 최신 stable 은 3.2.5 다. 기존 코드가 generated `when`/`map` 을 쓰면 일관성을 유지한다. 출처: <https://pub.dev/packages/freezed/changelog>
- List / Map / Set 은 `UnmodifiableListView` / `UnmodifiableMapView` / `UnmodifiableSetView` 로 자동 변환됨
- `@With` / `@Implements` 문법이 generic annotation 기반으로 변경

### go_router (2026)

- `StatefulShellRoute.indexedStack` + `StatefulShellBranch` 로 바텀 네비 스테이트풀 네스티드 네비게이션 구현 (각 탭 독립 스택). 출처: <https://pub.dev/documentation/go_router/latest/go_router/StatefulShellRoute-class.html>
- `StatefulShellBranch.preload: true` 로 탭 최초 진입 전 preload 지원 추가
- `notifyRootObserver` 로 ShellRoute 전환 이벤트를 root observer 에 전달 가능. 출처: <https://pub.dev/packages/go_router/changelog>

### Flutter 3.29 / 3.27 breaking changes

- Flutter 3.29: 웹 HTML 렌더러 제거. 출처: <https://docs.flutter.dev/release/release-notes/release-notes-3.29.0>
- Flutter 3.29: 스크립트 기반 Flutter Gradle plugin 제거 (3.19 부터 deprecated 였음). 기존 Android 프로젝트 migration 필요
- Flutter 3.27: DisplayP3 색공간 지원 추가, 일부 `Color` 메서드 deprecation
- Impeller OpenGL ES 백엔드 확장 (3.29 기준 거의 전 디바이스 커버). 출처: <https://docs.flutter.dev/release/breaking-changes>
- **Impeller 플랫폼 상태 (2026-08 기준)**: iOS 필수(Skia 전환 불가) · Android API 29+ 기본 · **macOS/Linux/Windows 는 Flutter 3.47 부터 Impeller 기본** · Web 은 Skia. 출처: <https://docs.flutter.dev/perf/impeller>
- **현재 stable 은 3.47.0** (릴리스 인덱스 stable 목록 최상단). 3.47 Android 의존성 매트릭스: Java 17 · KGP 2.4.0 · AGP 9.1.0 · Gradle 9.3.1. 출처: <https://docs.flutter.dev/release/release-notes>, <https://flutter.dev/blog/whats-new-in-flutter-3-47>

### flutter_hooks

- `HookConsumerWidget` 로 hooks + Riverpod provider 통합. 출처: <https://riverpod.dev/docs/concepts/about_hooks>
- `useMemoized` + `useEffect` 조합으로 데이터 페칭 중복 방지
- `useEffect` cleanup 은 반환 함수로 등록 — 위젯 dispose / 의존성 변경 시 호출. 출처: <https://pub.dev/packages/flutter_hooks>

### Makefile 기반 monorepo 관습 (fit-pal / apps)

- `dart-define-from-file=.dart_defines.json`, `--observatory-port=8181` 등 실행 옵션을 Makefile 타겟에 집중. 직접 `fvm flutter run` 호출 시 환경 누락으로 다른 플레이버 기동 위험
- flutter-preflight / flutter-run 스킬은 `HAS_MAKEFILE = true` 감지 시 `make <target>` 우선
