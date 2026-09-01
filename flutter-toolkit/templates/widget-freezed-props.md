# 위젯 골격 — freezed Props + Hook

`typedef` + freezed Props + 위젯 클래스 3요소를 한 파일에 담는 골격.

**적용 조건:** 프로젝트가 `freezed` + `flutter_hooks` 를 쓰고 Props 번들링 컨벤션을 따를 때. 감지는 `flutter-widget` / `flutter-hooks` 의 프로젝트 감지 단계가 한다. plain 생성자 파라미터를 쓰는 프로젝트는 `flutter-widget` 의 기본 골격을 쓴다.

`{...}` 자리는 프로젝트 파라미터다. `{widget_prefix}` · `{widget_suffix}` · `{TokenClass}` 는 프로젝트 컨벤션에서 확정한다.

## 골격

```dart
import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:freezed_annotation/freezed_annotation.dart';

part '{snake_case_name}.freezed.dart';

typedef {widget_prefix}{Domain}Changed = void Function({T} value);

@freezed
abstract class {widget_prefix}{Domain}{Role}{widget_suffix}Props
    with _${widget_prefix}{Domain}{Role}{widget_suffix}Props {
  const factory {widget_prefix}{Domain}{Role}{widget_suffix}Props({
    @Default(false) bool value,
    {widget_prefix}{Domain}Changed? onChanged,
    @Default(false) bool isDisabled,
  }) = _{widget_prefix}{Domain}{Role}{widget_suffix}Props;
}

class {widget_prefix}{Domain}{Role}{widget_suffix} extends HookWidget {
  const {widget_prefix}{Domain}{Role}{widget_suffix}(this._props, {super.key});

  final {widget_prefix}{Domain}{Role}{widget_suffix}Props _props;

  @override
  Widget build(BuildContext context) {
    final value = useState(_props.value);

    // 부모가 값을 바꾸면 내부 값 동기화
    useEffect(() {
      if (value.value != _props.value) {
        value.value = _props.value;
      }
      return null;
    }, [_props.value]);

    final size = _props.size ?? {TokenClass}.defaultSize;

    return const Placeholder();
  }
}
```

## 요소별 규칙

| 요소 | 규칙 |
|---|---|
| `typedef` | 콜백 prop 마다 시맨틱 typedef. **의미 원천 위젯이 소유** 하고 그 파일에 top-level 로 둔다. 공유 typedef 파일 금지 |
| Props | `@freezed abstract class ...Props with _$...Props`. `const factory` + `@Default` |
| 위젯 | 위치 인자 `this._props` + `final ...Props _props;` |
| base class | 로컬 상태가 있으면 `HookWidget`, provider 를 읽으면 `HookConsumerWidget` |

## 기본값 해소

`??` 로 토큰 기본값을 푼다. 이때 **`effective` / `resolved` 접두사를 붙이지 않는다** — `??` 가 이미 fallback 을 표현한다. 도메인·역할 이름을 쓴다.

```dart
// 금지
final effectiveSize = _props.size ?? {TokenClass}.defaultSize;
// 권장
final size = _props.size ?? {TokenClass}.defaultSize;
```

## 규칙

- `build()` 는 조립만 한다. 계산은 `useMemoized` · 파생 provider · 모델 getter 로 뺀다.
- 리프 토글은 `useState` + `useEffect([_props.value])` 로 부모 값과 동기화한다.
- controlled 컴포넌트(외부가 값을 소유)는 내부 상태를 두지 않는다 — 이 골격의 `useState`/`useEffect` 부분을 지운다.
- Props 에 쓰지 않는 필드를 미리 만들지 않는다. 실제 호출부에서 전달되는 값만 남긴다.
- 생성 후 codegen 을 돌려야 `.freezed.dart` 가 생긴다 — `flutter-run codegen`.
