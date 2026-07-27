---
name: flutter-test
description: >
  대상 파일/클래스를 분석하여 Flutter 테스트 코드를 자동 생성한다.
  WidgetTester 기반 widget test, Riverpod ProviderContainer unit test,
  integration_test 패키지를 프로젝트 패턴에 맞게 생성.
  "테스트 만들어줘", "unit test", "widget test", "테스트 코드 생성",
  "test 추가", "테스트 작성" 같은 Flutter 프로젝트 요청 시 트리거.
  테스트 실행만 할 때는 flutter-run을 사용한다.
argument-hint: "<file-or-class> [unit|widget|integration]"
user-invocable: true
---

## Gotchas

- Mock보다 Fake/Stub을 선호해라 — Flutter 공식 AI rules 권장. `mockito`/`mocktail`은 인터페이스가 복잡할 때만 사용
- 테스트 파일 위치는 소스 파일과 미러링해라 — `lib/features/auth/auth_service.dart` → `test/features/auth/auth_service_test.dart`
- `HAS_RIVERPOD` 프로젝트에서 Provider 테스트 시 `ProviderContainer`를 사용해라 — `ProviderScope`는 widget test 전용
- widget test에서 `pumpAndSettle()`은 타임아웃 될 수 있다 — 무한 애니메이션(CircularProgressIndicator 등)이 있으면 `pump(Duration)` 사용
- `HAS_BLOC` 프로젝트에서 `blocTest`를 사용해라 — `build`, `act`, `expect` 패턴으로 Bloc 상태 변화를 테스트
- 테스트에서 `containsSemantics`는 deprecated(Flutter 3.41) — `isSemantics`(부분 매칭) 또는 `matchesSemantics`(완전 매칭) 사용
- **Patrol 4.x Web 플랫폼 지원** — Patrol 4.0+ 부터 Web E2E 테스트 지원이 추가됐다. VS Code 확장 + 디버깅 개선, `dart.library.js_interop` 마이그레이션, Android API 36 에뮬레이터 지원 포함. 월 200K+ 다운로드로 Flutter E2E 테스팅 사실상 표준 (출처: <https://pub.dev/packages/patrol/changelog>)
- **Golden test: `golden_toolkit` 은 discontinued — `alchemist` 를 쓰라** — `golden_toolkit` 은 pub.dev 에 **discontinued** 로 표시돼 있고 마지막 릴리스가 0.15.0(3년 전)이다. `alchemist` 는 0.14.0(4개월 전 갱신)으로 유지보수 중이며 로컬/CI 테스트 분리, 자동 이미지 리사이즈, 테마·텍스트 스케일 커스터마이징을 제공한다 (출처: <https://pub.dev/packages/golden_toolkit>, <https://pub.dev/packages/alchemist>)
- **golden 파일은 플랫폼·폰트·Flutter 버전에 종속된다** — `matchesGoldenFile` 은 `expectLater` 와 함께 await 해야 하며, 마스터 이미지는 `$FLUTTER test --update-goldens` 로 갱신한다. 커스텀 폰트는 플랫폼과 Flutter 버전에 따라 다르게 렌더되므로 **로컬과 CI 의 OS · Flutter 버전을 일치시키지 않으면 CI 에서만 실패**한다. golden 실패를 "환경 탓" 으로 넘기지 말고 원인을 이 4 가지(OS 차이 / 버전 차이 / 폰트 로드 실패 / 실제 UI 변경) 중 하나로 특정하라 (출처: <https://api.flutter.dev/flutter/flutter_test/matchesGoldenFile.html>)
- **Flutter 3.44 신규 테스트 헬퍼** — `TestWidgetsApp` 이 `WidgetTester` 의 기본 앱으로 표준화됐고(라우트 지정 가능), Material 텍스트 필드용 `TestTextField` 가 추가됐다. `WidgetTesterCallback` 의 파라미터명이 `widgetTester` → `tester` 로 변경됐고, flutter_test 의 false-positive 히트테스트 미스가 수정됐다. 기존 테스트를 손볼 때 이 헬퍼로 보일러플레이트를 줄일 수 있다 (출처: <https://docs.flutter.dev/release/release-notes/release-notes-3.44.0>)
- **Maestro (대안 E2E)** — Semantics label/identifier 기반 black-box E2E 도구. Flutter Web 지원, Flutter Desktop 미지원 (2026-03). Flutter `Key` 는 접근성 레이어에 노출되지 않으므로 selector 로 사용 불가. Patrol 과 달리 언어 무관 YAML 기반 시나리오 (출처: <https://docs.maestro.dev/get-started/supported-platform/flutter>)

## 0. 프로젝트 감지

`references/project-detection.md`의 절차를 실행하여 프로젝트 환경을 파악한다.
이후 단계에서 감지 결과(`$FLUTTER`, `$DART`, `HAS_RIVERPOD`, `HAS_BLOC` 등)를 사용한다.

## Process

### 1. 대상 분석

`$ARGUMENTS`에서 대상 파일/클래스와 테스트 유형을 파싱한다.
- 유형 미지정 시: 클래스 종류로 자동 판단
  - Repository/Service/UseCase → unit test
  - Widget/Screen/Page → widget test
  - 전체 플로우 → integration test

대상 파일을 읽어 public API를 파악한다.

### 2. 기존 테스트 패턴 분석

`test/` 디렉토리에서 기존 테스트 파일을 읽어 프로젝트 관습을 파악:
- import 패턴 (package import vs relative)
- setUp/tearDown 사용 여부
- Mock/Fake 패턴 (mocktail, mockito, 수동 fake)
- group/test 네이밍 컨벤션
- `HAS_RIVERPOD` → ProviderContainer 패턴 확인
- `HAS_BLOC` → BlocTest 패턴 확인

### 3. 테스트 코드 생성

**Arrange-Act-Assert 구조:**
```dart
test('should {expected behavior} when {condition}', () {
  // Arrange
  final sut = ...;

  // Act
  final result = sut.method();

  // Assert
  expect(result, ...);
});
```

**생성 규칙:**
- 각 public 메서드에 최소 1개 테스트 (정상 케이스)
- 에러/엣지 케이스 테스트 추가 (nullable 파라미터, 빈 리스트 등)
- widget test 시 `pumpWidget` + `find.byType` 패턴 사용
- async 메서드는 `async` test + `await` 사용

### 4. 검증

생성된 테스트 파일에 대해:

```bash
$FLUTTER test {생성된_테스트_파일}
```

실행하여 에러가 없는지 확인한다. `flutter_test` 에 의존하는 widget/integration 테스트는 Flutter
SDK 러너가 필요하므로 `$DART test` 로는 실행되지 않는다. 순수 Dart 패키지(`test` 만 의존)라면
`$DART test` 를 써도 된다.

### 5. 결과 제시

생성된 테스트 파일과 **테스트 실행 출력을 그대로 인용**하여 사용자에게 보여준다.

- 실행 결과가 `+0 -0` (0 개 실행) 이면 그것은 "통과" 가 아니라 **"검사되지 않음"** 이다. 테스트가
  수집되지 않은 원인(파일 경로 · `main()` 누락 · group 필터)을 먼저 찾는다
- 테스트를 실행하지 못했으면 `[미검증]` 마커와 사유를 남긴다. "테스트를 작성했습니다" 로 완료를
  대체하지 않는다 (`harness/docs/guides/qa-evaluation-guide.md` §Evidence Validity Gate 검사 2)
