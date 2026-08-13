---
title: 테스트
version: 0.2.0
last_updated: 2026-08-13
---

<!-- 코드 펜스 규약: 이 문서의 fenced code block 은 백틱 4 개로 연다/닫는다.
     닫는 펜스를 백틱 3 개 단독 줄로 되돌리지 마라 — bare-fence 검사 오라클이
     닫는 펜스를 언어 힌트 없는 여는 펜스로 오탐한다 (Phase 5 AP-03). -->

# 테스트

## 요약

Flutter 테스트는 Unit / Widget / Integration 3계층 피라미드를 따른다. mockito와 mocktail 중 팀 규칙에 맞는 하나를 골라 통일하고, widget test는 `testWidgets` + `WidgetTester.pumpWidget` + `Finder`로 구성하며, UI 회귀가 중요한 지점만 golden test로 보호한다. 실 디바이스 상호작용은 `integration_test` 패키지로 검증한다.

## 원칙

### 1. 테스트 피라미드 — unit → widget → integration

빠르고 안정적인 unit 테스트가 바닥, 느리고 깨지기 쉬운 integration 테스트가 꼭대기에 있는 피라미드 형태를 유지한다. 느리고 flaky한 검증을 위로 밀어 올리지 말고, 가능한 한 아래 층에서 원인을 국소화한다.

출처: https://docs.flutter.dev/testing/overview

### 2. widget test의 기본 단위

`testWidgets`, `WidgetTester`, `pumpWidget`, `Finder`, `Matcher`가 widget test의 기본 구성 요소다. `pumpWidget`으로 트리를 렌더링하고 `find.byType` / `find.text` / `find.byKey`로 대상을 잡은 뒤 `expect`로 Matcher를 통해 검증한다.

출처: https://docs.flutter.dev/cookbook/testing/widget/introduction

### 3. Finder는 명확히, pump는 명시적으로

Finder는 text / type / key 기준으로 모호하지 않게 잡아야 한다. 스크롤, 애니메이션, 비동기 상태 갱신은 `pump(Duration)` 또는 `pumpAndSettle`로 명시적으로 프레임을 진행시킨다. 단, `pumpAndSettle`을 만능 대기 함수처럼 쓰면 무한 애니메이션에서 타임아웃이 난다.

출처: https://docs.flutter.dev/cookbook/testing/widget/finders

### 4. Golden test는 환경 고정이 전제

Golden(스크린샷) 테스트는 UI 회귀 방지에 강력하지만 theme, font, platform, device pixel ratio에 민감하다. 렌더 환경을 고정(폰트 로더, 테마 강제 지정, 고정 크기)하지 않으면 CI/로컬 간 깨짐이 반복된다. 모든 화면에 일괄 적용하지 말고 회귀 비용이 큰 화면에만 적용한다.

출처: https://docs.flutter.dev/cookbook/testing/widget/introduction

### 5. Integration test는 `integration_test` 패키지로

실제 디바이스·에뮬레이터에서 앱 전체 플로우를 검증할 때는 `integration_test` 패키지를 사용한다. `flutter_driver`는 더 이상 권장되지 않는다. 사용자 시나리오(로그인 → 목록 → 상세) 같은 end-to-end 검증에 적합하다.

출처: https://docs.flutter.dev/cookbook/testing/integration/introduction

## 수치

| 항목 | 값 |
|------|-----|
| Unit / Widget 실행 속도 | Quick (ms 단위) |
| Integration 실행 속도 | Slow (초~분 단위) |
| 테스트 의존성 복잡도 | unit < widget < integration |
| mockito 최신 버전 | 5.6.3 |
| mocktail 최신 버전 | 1.0.4 |

## 안티패턴

- Widget test에서 실제 네트워크 호출이나 실제 DB 접근을 수행한다. 외부 의존은 fake/mock으로 격리해야 한다.
- `pumpAndSettle`을 모든 비동기 대기의 만능 해결책처럼 사용한다. 무한 애니메이션이 있으면 타임아웃이 발생한다.
- Golden test를 모든 화면에 무차별 적용한다. 사소한 디자인 변경마다 대량의 diff가 발생해 팀이 golden을 기계적으로 수락하게 된다.
- mockito와 mocktail을 팀 규칙 없이 혼용한다. Mock 스타일이 섞이면 테스트 코드 가독성과 유지보수성이 동시에 떨어진다.
- Integration test로 유닛 단위 버그까지 잡으려 한다. 실패 원인 localization이 어려워 디버깅 비용이 폭증한다.

## Gotchas

- **Mockito vs Mocktail 선택**: Mockito는 `build_runner` codegen이 필요하지만 타입 안전성이 명시적이다. Mocktail은 codegen이 없고 null-safety에 더 잘 맞지만, 타입 검증이 런타임에 일어난다. 팀 관습과 codegen 파이프라인 유무로 하나를 선택하고 일관되게 사용한다.
- **Integration test의 한계**: 동작은 검증할 수 있지만 실패 원인을 특정 레이어로 좁히기 어렵다. 원인 localization은 unit/widget test에 맡기고, integration은 "사용자 관점 시나리오가 끝까지 통과하는가"만 확인한다.
- **Golden test의 플랫폼 의존**: macOS에서 통과한 golden이 Linux CI에서 깨지는 경우가 흔하다. CI 환경의 폰트·렌더러를 기준으로 golden을 관리하거나, 플랫폼별 golden을 분리한다.
- **`pumpWidget` 후 `pump()` 한 번 더**: `FutureBuilder`, `StreamBuilder`, 초기 animation 프레임은 `pumpWidget` 직후 한 프레임 더 `pump()`해야 반영된다. 이 누락이 widget test flake의 흔한 원인이다.

## 실전 패턴

### Widget Test 기본 구조

````dart
testWidgets('로그인 버튼 클릭 시 provider에 로그인 요청', (tester) async {
  final mockAuth = MockAuthRepository();
  when(() => mockAuth.login(any(), any())).thenAnswer((_) async => Right(user));

  await tester.pumpWidget(
    ProviderScope(
      overrides: [authRepositoryProvider.overrideWithValue(mockAuth)],
      child: const MaterialApp(home: LoginPage()),
    ),
  );

  await tester.enterText(find.byKey(Key('email')), 'test@test.com');
  await tester.enterText(find.byKey(Key('password')), 'pass123');
  await tester.tap(find.byKey(Key('loginBtn')));
  await tester.pump();

  verify(() => mockAuth.login('test@test.com', 'pass123')).called(1);
});
````

- 출처: https://docs.flutter.dev/cookbook/testing/widget/tap-drag

### Riverpod widget test 하네스 — "화면이 provider 변화를 반영하는가"

unit test 는 provider 값만 본다. **화면이 그 값을 반영하는지**는 `ProviderScope` 루트로 띄운
widget test 로만 잡힌다. provider 접근은 별도 컨테이너를 만들지 말고 `tester.container()` 를 쓴다.

````dart
testWidgets('설정 변경이 상세 화면에 반영된다', (tester) async {
  await tester.pumpWidget(
    ProviderScope(
      overrides: [groupRepositoryProvider.overrideWithValue(fakeRepo)],
      child: const MaterialApp(home: GroupDetailPage(groupId: 'g1')),
    ),
  );
  await tester.pump();

  final container = tester.container();
  await container.read(groupPreferencesProvider.notifier).updatePalette('g1', newPalette);
  await tester.pump();

  expect(container.read(groupDetailDataProvider('g1')).value?.palette, newPalette);
  expect(find.text(newPalette.label), findsOneWidget);   // 렌더 결과도 함께 본다
});
````

- **unit test 는 `ProviderContainer.test()`** 를 쓰고 컨테이너를 테스트 간 공유하지 않는다.
  `autoDispose` provider 는 `container.read` 만 하면 도중에 dispose 될 수 있으므로
  `container.listen` 으로 붙잡는다
- **widget test 에서 `ProviderContainer` 단독 사용 금지** — 화면 렌더 검증에는 `ProviderScope`
  루트가 필요하다. override 는 `ProviderScope` / `ProviderContainer` 의 `overrides` 로만 준다
- provider state 만 assert 하고 끝내면 "값은 바뀌었는데 화면은 캐시된 상태" 를 놓친다
- 출처: https://riverpod.dev/docs/how_to/testing

### 매핑·조합 coverage — 대표 몇 종만 검증하지 않는다

매핑/variant/조합이 N 종이면 대표 1~2 종 통과를 커버리지로 착각하기 쉽다. 실측 사례로
"16종 매핑 중 2종만 검증", "3 visibility x 6 relation = 18 케이스 중 15케이스만 재현" 이 있었다.

- 축 값의 출처를 **프로덕션 코드의 공유 상수/enum** 으로 고정하고 테스트가 그것을 import 해 순회
- 케이스 수는 손으로 적지 말고 **축 값 개수의 곱**으로 산출해 실행 케이스 수와 대조
- table-driven test 또는 generated fixture loop 로 작성 비용을 낮춘다

### Golden Test 실전

````dart
testWidgets('ProductCard golden', (tester) async {
  await tester.pumpWidget(
    MaterialApp(
      theme: appLightTheme,
      home: Scaffold(body: ProductCard(product: mockProduct)),
    ),
  );
  await expectLater(
    find.byType(ProductCard),
    matchesGoldenFile('goldens/product_card_light.png'),
  );
});
````

CI에서 golden update: `flutter test --update-goldens`

- 출처: https://api.flutter.dev/flutter/flutter_test/matchesGoldenFile.html

### 테스트 피라미드 비율 권장

| 레이어 | 비율 | 대상 |
|--------|------|------|
| Unit | 70% | Repository, UseCase, Notifier 로직 |
| Widget | 20% | 개별 위젯, 화면 단위 상호작용 |
| Integration | 10% | 핵심 사용자 시나리오 E2E |

### Fake vs Mock 선택

- **Fake**: 인터페이스의 간단한 인메모리 구현. 로직 검증에 적합
- **Mock**: 호출 여부/횟수/인자 검증. 상호작용 검증에 적합
- Repository 계층은 Fake 선호 (실제 로직 흐름 검증), Notifier에서 Repository 호출 검증은 Mock 선호

### 비동기 테스트 패턴

````dart
testWidgets('AsyncNotifier loading → data 전이', (tester) async {
  await tester.pumpWidget(testApp);
  // loading 상태
  expect(find.byType(CircularProgressIndicator), findsOneWidget);
  // data 도착 대기
  await tester.pump(const Duration(milliseconds: 100));
  await tester.pump(); // FutureBuilder 갱신
  expect(find.text('Product Name'), findsOneWidget);
});
````
