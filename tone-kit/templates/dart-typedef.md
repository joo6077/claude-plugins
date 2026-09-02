# 시맨틱 typedef (Dart/Flutter)

콜백 prop 의 함수 타입에 이름을 붙이는 템플릿. 실측 51 선언 / 32 파일.

**채우는 주체:** `tone-scaffold` · **어댑터:** dart-flutter

## 골격

```dart
typedef {widget_prefix}{Meaning}{Event} = void Function({T} value);
typedef {widget_prefix}{Meaning}{Event} = void Function();
typedef {widget_prefix}{Meaning}Of<T> = String Function(T item);
```

## 소유권 규칙

typedef 는 **그 의미가 생겨난 위젯의 파일** 에 top-level 로 선언한다.

- 공유 typedef 파일을 만들지 않는다. 만들면 어느 위젯의 계약인지 추적이 끊긴다.
- 다른 위젯이 같은 시그니처를 쓴다고 해서 재사용하지 않는다. 시그니처가 같아도 의미가 다르면 다른 typedef 다.
- 의미 원천이 옮겨가면 typedef 도 같이 옮긴다.

## 이름 짓기

`{widget_prefix}` + 의미 + 이벤트 형태.

**이벤트 형태는 새로 만들지 말고 프레임워크 어휘를 쓴다.** Flutter 는 제스처 생명주기에 `on<제스처><단계>` 를 이미 정의해 뒀고(`onTapDown` · `onLongPressStart` · `onPanUpdate` …), 폼·선택 계열도 `onChanged` · `onSubmitted` · `onSelected` · `onPressed` 로 고정돼 있다. 전체 목록은 어댑터 `adapter-dart-flutter.md` §3.11.

자체 어휘를 만들면 공식 어휘가 갈라 놓은 단계를 도로 합치게 된다 — `Press` 하나로는 tap 인지 long press 인지 갈리지 않는다.

공식 어휘에 대응이 없는 **도메인 이벤트만** 프로젝트가 이름 짓는다.

```dart
// 권장 — 프레임워크 어휘 + 무엇이 바뀌었는지
typedef {widget_prefix}SwitchChanged = void Function(bool value);
typedef {widget_prefix}EventVisibleChanged = void Function(bool value);

// 권장 — 공식 단계 어휘와 정렬
typedef {widget_prefix}PressableTapDown = void Function(TapDownDetails details);

// 권장 — 공식 어휘에 없는 도메인 이벤트
typedef {widget_prefix}PairingModeEntered = void Function();

// 금지 — 시그니처를 이름으로 옮기기만 함
typedef BoolCallback = void Function(bool value);
typedef VoidCb = void Function();

// 금지 — 자체 어휘. 어느 제스처의 어느 단계인지 안 갈린다
typedef {widget_prefix}PressStart = void Function();
```

## 제네릭

선택 항목의 타입이 호출부마다 다르면 제네릭을 쓴다.

```dart
typedef {widget_prefix}SelectChanged<T> = void Function(T value);
typedef {widget_prefix}SelectLabelOf<T> = String Function(T item);
```

## 규칙

- FFI 바인딩용 함수 시그니처는 이 규칙의 대상이 아니다. 실측 90 선언 중 26건이 FFI 이며 별도 관례를 따른다.
- `Props` 필드 타입에 `void Function(bool)` 을 직접 쓰지 않는다. 그 자리가 typedef 를 만들 자리다.
- typedef 를 만들었으면 Props 필드 타입과 위젯 콜백 호출부가 모두 그 이름을 쓰는지 확인한다.
- 같은 개념에 두 어휘를 섞지 않는다 — `…SelectTap` 과 `…Selected` 를 함께 두지 마라. 하나로 고정한다.
