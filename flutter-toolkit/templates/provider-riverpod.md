# provider / state 골격 — Riverpod

Riverpod notifier 와 파생 상태 번들 골격.

**적용 조건:** `@riverpod` codegen 을 쓰는 프로젝트. 골격 2(freezed 뷰 번들)는 프로젝트가 **freezed State 컨벤션** 일 때만 쓴다 — `flutter-provider` 의 State 클래스 패턴 감지 결과를 따른다. manual `copyWith` 컨벤션 프로젝트는 `flutter-provider` 의 State 규칙이 우선한다.

`{...}` 자리는 프로젝트 파라미터다.

## 골격 1 — notifier

```dart
import 'package:riverpod_annotation/riverpod_annotation.dart';

part '{snake_case_name}.g.dart';

@Riverpod(keepAlive: true)
class {Domain}{Role} extends _${Domain}{Role} {
  @override
  {T} build() => {초기값};

  /// {한 줄 요약}
  ///
  /// - [{param}]: {설명}
  void set{Something}({T} {param}) {
    if (state == {param}) {
      return;
    }

    state = {param};
  }
}
```

## 골격 2 — 파생 / 뷰 번들 (freezed State 컨벤션 프로젝트 한정)

파생값을 여러 개 묶어 위젯에 넘길 때 익명 Record 대신 이름 있는 클래스를 쓴다. 필드에 이름이 없으면 호출부마다 위치로 읽게 되고, 필드가 늘면 전부 깨진다.

```dart
@freezed
abstract class {Domain}ViewState with _${Domain}ViewState {
  const factory {Domain}ViewState({
    @Default(false) bool isLoading,
    @Default(<{Item}>[]) List<{Item}> items,
    String? errorMessage,
  }) = _{Domain}ViewState;
}
```

manual `copyWith` 컨벤션 프로젝트는 이 골격 대신 `flutter-provider` 의 State 클래스 규칙을 따른다 — nullable clear 파라미터 때문에 두 방식이 호환되지 않는다.

## 규칙

- notifier 가 커지면 쪼갠다. 한 notifier 안에 상태 모델과 알림 헬퍼 수십 개를 몰아넣지 않는다.
- 상태 변경 경로를 하나로 모은다. 필드마다 개별 setter 를 만드는 대신 단일 reducer 를 두고 그것을 통과시킨다.
- 보일러플레이트 getter(단순 필드 위임)를 만들지 않는다.
- provider 안에서 `BuildContext` 를 잡지 않는다.
- 비동기 진행 상태는 provider 상태 + `ref.listen` 으로 표현한다.
