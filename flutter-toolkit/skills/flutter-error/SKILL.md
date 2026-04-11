---
name: flutter-error
description: >
  Flutter 앱의 에러 처리 패턴을 안내한다. 데이터 계층에서 예외를 도메인 Failure로
  변환하고, Provider/State에 저장한 뒤, 화면에서 사용자에게 표시하는 관심사 분리
  패턴을 다룬다. Severity 매핑, 디버그 정보 전달, 에지 케이스 처리 포함.
  "에러 처리", "error handling", "Failure", "에러 표시", "에러 다이얼로그",
  "snackbar 에러", "에러 패턴", "실패 처리", "exception handling",
  "에러 인프라", "error infrastructure", "에러 변환", "에러 전파" 같은
  키워드가 등장하면 트리거한다.
user-invocable: true
---

## Gotchas

- `catch (e)` 단독 사용 금지 — 반드시 예외 타입 명시: `catch (DioException e)` 또는 `catch (Object e, StackTrace st)`
- 예외 → Failure 변환은 반드시 경계 계층(Repository/DataSource)에서 수행 — Presentation 레이어까지 예외가 새면 안 된다
- 빈 catch 블록 `catch (e) {}` 금지 — 최소한 `errorProvider.notifier.show(failure)` 호출 필수
- `catch (e) { print(e); }` 로그만 남기고 UI에 표시 안 하면 사용자는 실패를 모른다 — 반드시 UI 피드백
- **프로젝트 Result 타입이 Freezed sealed class 기반이면 `.when(success:, failure:)` 가 아니라 Dart pattern matching (switch expression) 으로 분기**하라 — Freezed 3.0 부터 `.when`/`.map` 메서드가 제거됐다. 자체 정의한 커스텀 Result (수동 `when` 메서드 보유) 일 때만 아래 `.when` 예시를 그대로 사용할 수 있다 (출처: <https://pub.dev/packages/freezed/changelog>)

# Error Handling 패턴 가이드

## 0. 프로젝트 감지

`references/project-detection.md`의 절차를 실행하여 프로젝트 환경을 파악한다.

### 프로젝트 에러 인프라 감지

스킬 실행 시 프로젝트의 기존 에러 인프라를 탐색한다:

| 탐색 대상 | 감지 방법 |
|----------|----------|
| Failure/Error sealed class | `lib/` 내 `failure`, `error`, `exception` 키워드가 포함된 파일 검색 |
| Result/Either 타입 | `dartz`, `fpdart`, 또는 커스텀 `Result` 클래스 존재 여부 |
| 에러 표시 인프라 | 글로벌 에러 notifier/provider/cubit 존재 여부 |
| Severity 분류 | 에러 심각도 enum 존재 여부 |

탐색 경로:
- `lib/core/error/` — Failure sealed class, error notifier, error listener
- `lib/core/utils/` — Result/Either typedef
- `lib/shared/error/` 또는 `lib/shared/domain/`

구체적으로 찾을 것:
- `error_notifier.dart` 또는 유사 파일 → show()/dismiss() 메서드가 있는 notifier
- `error_listener.dart` → severity별 자동 UI 표시 위젯
- `app_error.dart` → Failure + severity + stackTrace를 묶는 객체
- 에러 로그 provider → 히스토리 추적 (dev 디버깅용)
- dev error overlay → 개발 모드 에러 패널

감지된 인프라가 있으면 해당 타입과 패턴을 사용한다.
없으면 이 가이드의 범용 패턴을 적용한다.

감지된 에러 인프라 정리 (감지 후 기록):
- show 메서드: `ref.read(errorProvider.notifier).show(failure)` 또는 유사
- severity override: `severityOverride: ErrorSeverity.critical` 또는 유사
- context 파라미터: `context: 'ScreenName._action'` 으로 발생 위치 전달
- 필수 import 경로: (감지된 파일 경로)

---

## 에러 처리 아키텍처 (관심사 분리)

```text
Repository: Exception → Failure/Error 변환
     ↓
Provider/State: failure 저장 (state.failure 또는 equivalent)
     ↓
Screen/Widget: failure 감지 → 에러 표시 인프라에 전달
     ↓
에러 표시: severity별 UI
  ├─ 경고(warning)  → Snackbar / Toast
  ├─ 치명(critical) → Dialog (확인 필수)
  └─ 인증 만료       → Dialog + 로그아웃 + 리다이렉트
```

---

## 핵심 원칙: 책임 분리

> **Provider/State는 failure를 저장만 한다. 에러 표시 인프라를 직접 호출하지 않는다.**

> **Screen/Widget이 failure를 감지하고, 에러 표시를 담당한다.**

이 분리가 필요한 이유:
- **테스트 가능성**: Provider가 UI 계층을 모르므로 단위 테스트가 쉬워진다
- **재사용성**: 같은 Provider를 다른 UI(snackbar/dialog/인라인)로 재사용할 수 있다
- **중복 방지**: 중첩 호출(Provider A → Provider B)에서 양쪽이 에러를 표시하면 중복된다

---

## 계층별 에러 처리 패턴

### 1. Repository: Exception → Failure 변환

데이터 계층 경계에서 모든 예외를 도메인 Failure 타입으로 변환한다.

```dart
// 프로젝트에 Failure sealed class가 있는 경우
@override
Future<Result<UserEntity>> getUser(String id) async {
  try {
    final model = await _dataSource.getUser(id);
    return Result.success(model.toEntity());
  } on DioException catch (error, st) {
    return Result.failure(_mapFailure(error, st));
  } on Exception catch (error, st) {
    return Result.failure(Failure.unknown(error.toString()));
  }
}

// _mapFailure: DioException → Failure 변환
Failure _mapFailure(Object error, StackTrace st) {
  if (error is DioException) {
    switch (error.type) {
      case DioExceptionType.connectionTimeout:
      case DioExceptionType.connectionError:
        return const Failure.network('네트워크 연결을 확인해주세요.');
      case DioExceptionType.badResponse:
        final statusCode = error.response?.statusCode;
        if (statusCode == 401) return const Failure.unauthorized();
        return Failure.server('서버 오류가 발생했습니다. ($statusCode)');
      default:
        return Failure.unknown(error.message ?? '알 수 없는 오류');
    }
  }
  return Failure.unknown(error.toString());
}
```

프로젝트에 Failure 타입이 없으면 직접 Exception을 throw하되, 타입을 명시한다:
```dart
Future<UserEntity> getUser(String id) async {
  try {
    final model = await _dataSource.getUser(id);
    return model.toEntity();
  } on DioException catch (error) {
    throw _mapException(error);
  }
}
```

### 2. Provider/State: failure 저장

Provider는 결과를 state에 저장만 한다. 에러 표시 인프라를 직접 호출하지 않는다.

```dart
// Result 패턴
result.when(
  success: (data) {
    state = state.copyWith(
      isLoading: false,
      data: data,
      failure: null,  // 성공 시 failure 클리어
    );
  },
  failure: (failure) {
    state = state.copyWith(
      isLoading: false,
      failure: failure,
    );
  },
);
```

### 3. Screen/Widget: failure 감지 → 에러 표시

화면에서 failure를 감지하고 프로젝트의 에러 표시 인프라에 전달한다.

```dart
// 패턴 A: Provider 메서드 반환값으로 판단
Future<void> _doAction() async {
  final result = await ref.read(someProvider.notifier).doAction();
  if (!mounted) return;  // async 후 mounted 체크 필수

  if (result == null) {
    final failure = ref.read(someProvider).failure;
    if (failure != null) {
      // 프로젝트의 에러 표시 인프라 호출
      _showError(failure);
    }
    return;
  }
  // 성공 처리...
}
```

```dart
// 패턴 B: state listen으로 failure 감지 (Riverpod)
ref.listen(someProvider.select((s) => s.failure), (prev, failure) {
  if (failure != null && failure != prev) {
    _showError(failure);
  }
});
```

```dart
// 패턴 C: Result를 직접 받는 경우 (커스텀 Result 에 수동 when 메서드가 있을 때)
final result = await ref.read(someUseCaseProvider)(params);
if (!mounted) return;

result.when(
  success: (data) { /* 성공 처리 */ },
  failure: (failure) { _showError(failure); },
);
```

```dart
// 패턴 C': Result 가 Freezed sealed class 기반 (Freezed 3.0 에서 .when 제거됨)
final result = await ref.read(someUseCaseProvider)(params);
if (!mounted) return;

switch (result) {
  case Success(:final data):
    // 성공 처리
    break;
  case Failure(:final failure):
    _showError(failure);
    break;
}
```

---

## Severity 매핑

에러 심각도를 분류하여 UI 표시 방식을 결정한다.

| 에러 유형 | 권장 Severity | UI | 이유 |
|----------|--------------|-----|------|
| 네트워크 연결 실패 | warning | Snackbar/Toast | 일시적 문제, 자동 복구 가능성 |
| 로컬 저장 실패 | warning | Snackbar/Toast | 핵심 흐름을 차단하지 않음 |
| 서버 오류 (5xx) | critical | Dialog | 데이터 정합성 문제 가능성 |
| 인증 만료 (401) | critical | Dialog + 로그아웃 | 이후 모든 API 실패 |
| 알 수 없는 오류 | critical | Dialog | 최악을 가정 |

프로젝트에 severity enum이 있으면 해당 매핑을 따른다.
없으면 위 표를 기본값으로 사용하되, 상황에 맞게 재정의한다:

```dart
// 기본 severity가 적절하지 않을 때 재정의
// 예: 네트워크 에러지만 결제 중이면 critical
_showError(failure, severity: ErrorSeverity.critical);

// 예: 서버 에러지만 추천 로딩 실패는 warning
_showError(failure, severity: ErrorSeverity.warning);
```

---

## 에러를 표시하지 않아도 되는 경우

모든 failure가 사용자에게 표시될 필요는 없다:

- **사용자 취소**: 로그인 취소 등 (`failure == null`이면 호출 안 함) — 의도적 중단을 에러로 표시하면 혼란
- **Fail-open**: 버전 체크, 추천 로딩 등 실패해도 앱 사용에 지장 없는 경우
- **인라인 피드백**: 입력 필드 바로 아래에 에러를 표시하는 경우 — 글로벌 에러와 중복 방지
- **자동 복구**: 토큰 리프레시 재시도 → 최종 실패 시에만 표시

---

## 엣지 케이스

### 긴 체인 호출 (Provider A → Provider B)

에러는 최종 호출자인 Screen이 한 번만 표시한다. Provider A는 Provider B의 failure를 자신의 state.failure로 전파만 한다.

```dart
// Provider A
final resultB = await ref.read(providerB.notifier).doSomething();
if (!ref.mounted) return;

final failureB = ref.read(providerB).failure;
if (failureB != null) {
  state = state.copyWith(isLoading: false, failure: failureB);
  return; // 에러 표시 호출 안 함 — Screen이 처리
}
```

### 비동기 레이스 (빠른 연속 호출)

사용자가 버튼을 빠르게 연타하면 이전 요청의 failure가 이후 요청을 덮어쓸 수 있다.
`failure != prev` 체크가 이를 방지한다. 추가로 `isLoading` 중 버튼 비활성화를 권장한다.

```dart
// Screen — 중복 방지
ref.listen(someProvider.select((s) => s.failure), (prev, failure) {
  if (failure != null && failure != prev) {
    _showError(failure);
  }
});

// 버튼 — 로딩 중 비활성화
ElevatedButton(
  onPressed: state.isLoading ? null : _doAction,
  child: state.isLoading
      ? const CircularProgressIndicator()
      : const Text('실행'),
),
```

### 중첩 네비게이션 (push 후 에러 표시)

`Navigator.push` 후 결과를 받아 처리하는 경우, pop된 화면의 mounted가 false일 수 있다.
에러 표시는 현재 화면(push를 호출한 화면)에서만 한다.

```dart
final result = await Navigator.push<bool>(context, route);
if (!mounted) return; // push한 화면이 dispose됐을 수 있음

if (result == null || result == false) {
  // push된 화면에서 이미 에러 처리됨 — 여기서 중복 표시 안 함
  return;
}
```

인라인 에러를 사용하면서도 인증 만료만 글로벌로 처리해야 하는 경우:

```dart
result.when(
  success: (data) { /* ... */ },
  failure: (failure) {
    if (_isAuthFailure(failure)) {
      _showGlobalError(failure);  // 글로벌 에러 인프라
      return;
    }
    setState(() {
      _errorMessage = _mapFailureMessage(failure);  // 인라인 에러
    });
  },
);
```

---

## 디버그 정보 전달

dev 환경에서 디버깅을 위해 에러 발생 위치와 stackTrace를 전달한다:

```dart
_showError(
  failure,
  context: 'ProfileScreen._updateProfile',  // 발생 지점
  stackTrace: st,  // 가능하면 전달
);
```

---

## 체크리스트

에러 처리 코드를 작성할 때 확인한다:

- [ ] 비동기 액션 실패 시 에러 표시 인프라를 호출하는가? — 누락 시 사용자에게 아무 피드백 없이 실패가 묻힌다
- [ ] 사용자 취소와 실제 에러를 구분하는가? — 미구분 시 취소도 에러로 표시됨
- [ ] Severity가 상황에 맞는가? — 결제 중 네트워크 에러를 warning으로 두면 실패를 인지 못함
- [ ] 인라인 피드백이 더 적절한 경우는 아닌가? — 입력 검증 에러를 글로벌 snackbar로 보여주면 혼란
- [ ] `mounted` / `ref.mounted` 체크 후에 에러를 표시하는가? — dispose된 위젯에서 접근 시 런타임 에러
- [ ] Provider에서 에러 표시 인프라를 직접 호출하고 있지는 않은가? — 책임 분리 위반
- [ ] `context` 파라미터로 발생 위치를 전달하는가? — 미전달 시 dev 디버깅에서 에러 발생 지점 추적 불가
