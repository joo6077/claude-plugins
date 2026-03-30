---
name: flutter-test
description: >
  대상 파일/클래스를 분석하여 테스트 코드를 자동 생성한다.
  unit test, widget test, integration test를 프로젝트 패턴에 맞게 생성.
  "테스트 만들어줘", "unit test", "widget test", "테스트 코드 생성",
  "test 추가", "테스트 작성" 같은 요청 시 트리거.
  테스트 실행만 할 때는 flutter-run을 사용한다.
argument-hint: "<file-or-class> [unit|widget|integration]"
user-invocable: true
---

## Gotchas

- Mock보다 Fake/Stub을 선호해라 — Flutter 공식 AI rules 권장. `mockito`/`mocktail`은 인터페이스가 복잡할 때만 사용
- 테스트 파일 위치는 소스 파일과 미러링해라 — `lib/features/auth/auth_service.dart` → `test/features/auth/auth_service_test.dart`
- `HAS_RIVERPOD` 프로젝트에서 Provider 테스트 시 `ProviderContainer`를 사용해라 — `ProviderScope`는 widget test 전용

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
$DART test {생성된_테스트_파일}
```
실행하여 에러가 없는지 확인한다.

### 5. 결과 제시

생성된 테스트 파일과 테스트 결과를 사용자에게 보여준다.
