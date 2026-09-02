---
title: Dart / Flutter 어댑터 관용구
version: 0.1.0
last_updated: 2026-09-02
---

# Dart / Flutter 어댑터 관용구

**이 문서가 잡는 것**

- 문법이 이미 답을 가진 자리를 손으로 채운 코드 — `!` 강제 캐스트, 수동 `SizedBox` 나열, `.expand().skip()` 체이닝
- 화면 밖까지 전부 빌드하는 eager 리스트와, 부모가 쥐고 있어 subtree 를 통째로 흔드는 leaf 토글 상태
- 의미가 지워진 표면 — 익명 레코드 파생 뷰, 프리미티브로 뭉개진 콜백 typedef, 자명한 필드 `///`

```dart
// before
SingleChildScrollView(
  child: Column(
    children: [
      Row(children: [icon, SizedBox(width: {TokenClass}.w10), title]),
      ...devices.map((d) => _buildDeviceRow(d)),
    ],
  ),
)

// after
CustomScrollView(
  slivers: [
    SliverToBoxAdapter(
      child: Row(spacing: {TokenClass}.w10, children: [icon, title]),
    ),
    SliverList.builder(
      itemCount: devices.length,
      itemBuilder: (context, i) =>
          {widget_prefix}DeviceItemWidget(device: devices[i]),
    ),
  ],
)
```

한 블록에 세 가지가 걸렸다 — eager 렌더(원칙 4), 수동 간격(원칙 3), `_build*` 헬퍼(어댑터 슬롯 `helper_prefix_forbidden`). 목표는 프레임워크가 이미 제공하는 표현을 쓰는 것이고, 톤 개선은 그 부산물이다.

**읽는 법** — 각 원칙은 결론 → before/after → 왜 → 강도·출처 순이다. `MUST` / `SHOULD` / `관측 컨벤션` 3등급의 판정 방법론은 [ai-code-stylometry.md](ai-code-stylometry.md) 가 소유하며, 여기서는 규칙마다 맨 뒤에 붙여만 둔다.

- **관측 컨벤션**(공개 출처 없이 프로젝트 실측만 있는 규칙 — 준수 강도가 낮다는 뜻이 아니라 근거가 국지적이라는 뜻이다)
- **축**(규칙이 속한 판정 영역. 제목 뒤 `[어댑터:dart-flutter]` · `[한국어]` 가 축 라벨이고, 축이 다르면 규칙의 소유 문서가 다르다)
- **어댑터 슬롯**(`tone-guide` 와 `tone-scaffold` 가 읽어 가는 스택별 값 칸 — 주석 기호, doc 라벨, 금지 접두사, 완료 게이트 grep)

이 문서는 코어(스택 무관) 원칙을 Dart/Flutter 에 결속하는 **이 킷의 유일한 어댑터 근거 문서** 이며, 다른 스택은 위반 실측이 없으므로 어댑터를 만들지 않는다. 추출 판단은 `extraction-thresholds.md`, 한국어 문체와 doc 라벨 상수는 `korean-technical-writing.md`, A~J 위반 판정은 `antipattern-catalog.md` 가 SSOT 이므로 여기서 다시 정의하지 않고 가리킨다.

---

## 원칙

### 1. null 은 `??` · `?.` · early return · 패턴 매칭으로 다룬다 `[어댑터:dart-flutter]`

`!` 는 non-null 이 이미 증명된 경계부에만 쓴다. 흐름 중간의 `if (x != null) f(x!)` 는 패턴 매칭으로 바꾼다.

```dart
// before
final label = props.label;
if (label != null) {
  return Text(label!);
}
return const SizedBox.shrink();

// after
if (props.label case final label?) return Text(label);
return const SizedBox.shrink();
```

```dart
// before — 호출부 전수가 값을 채우는데 타입만 열려 있다
class {widget_prefix}CardWidgetProps {
  const {widget_prefix}CardWidgetProps({this.title});
  final String? title;
}
Text(props.title!)

// after
class {widget_prefix}CardWidgetProps {
  const {widget_prefix}CardWidgetProps({required this.title});
  final String title;
}
Text(props.title)
```

기본 도구는 넷이다 — `??`, `?.`, early return, 패턴 매칭. 경계부란 `assert` 직후, JSON 파싱 직후처럼 non-null 이 이미 증명된 자리이고, 흐름 중간의 `!` 는 컴파일러가 아는 사실을 사람이 다시 단언하는 것이다. nullable 로 열어 두고 호출부 전수가 값을 채우는 상태는 타입이 실제 계약보다 넓은 것이므로 `required` 로 좁힌다.

**강도:** SHOULD

> **출처:** [Dart null safety](https://dart.dev/null-safety) · [Dart patterns](https://dart.dev/language/patterns) · [Effective Dart — design](https://dart.dev/effective-dart/design)

### 2. nullable 삽입 문법은 위치가 정한다 — `?element` 와 `if case` 는 쓸 수 있는 자리가 다르다 `[어댑터:dart-flutter]`

같은 "null 이면 넣지 않는다"도 문법 위치마다 답이 다르다. 위치를 틀리면 컴파일이 안 되고, 그래서 `!` 로 회귀한다.

```dart
// before
style: if (custom case final s?) s else defaultStyle,  // expression 위치 — 문법 성립 안 함
children: [header, if (trailing != null) trailing!],   // ! 로 회귀
final view = switch (isOn) {                           // 2분기에 switch
  true => onView,
  false => offView,
};

// after
style: custom ?? defaultStyle,              // expression 위치 — ?? 또는 삼항
children: [header, ?trailing],              // 컬렉션 리터럴 — null-aware element (Dart 3.8+)
if (label case final text?) Text(text),     // statement / collection element — non-null 바인딩
final view = switch (state) { ... };        // 3분기 이상 — switch expression
```

`if case` 는 statement 와 collection element 위치에서만 쓸 수 있다. **2분기 null 체크에 `switch` expression 을 쓰지 않는다** — 삼항이 더 짧고 `switch` 는 분기 3개부터 이득이 난다. 같은 기준이 sealed class 에도 적용돼 variant 가 2개면 `if` 로 충분하다.

**강도:** SHOULD

> **출처:** [Dart collections](https://dart.dev/language/collections) · [Dart branches](https://dart.dev/language/branches) · [Dart class modifiers](https://dart.dev/language/class-modifiers) · [prefer_spread_collections](https://dart.dev/tools/linter-rules/prefer_spread_collections)

### 3. 간격은 `spacing:` 파라미터로 표현한다 — 수동 `SizedBox` 를 끼워 넣지 않는다 `[어댑터:dart-flutter]`

고정 gap 은 `Row` / `Column` 의 `spacing:`, 리스트 separator 는 `ListView.separated` 의 `separatorBuilder` 가 담당한다.

```dart
// before
Row(
  children: [icon, SizedBox(width: {TokenClass}.w10), label],
)

// after
Row(
  spacing: {TokenClass}.w10,
  children: [icon, label],
)
```

```dart
// before — 트릭성 체이닝
children: sections.map(_body).expand((w) => [divider, w]).skip(1).toList()
children: sections.indexed.expand((r) { ... }).toList()

// after
ListView.separated(
  itemCount: sections.length,
  separatorBuilder: (context, index) => divider,
  itemBuilder: (context, index) => _body(sections[index]),
)
```

`SizedBox` 를 children 사이에 손으로 나열하는 것은 프레임워크가 이미 가진 파라미터의 수동 재구현이고, 항목이 늘 때마다 삽입 위치를 사람이 관리해야 한다. 체이닝 쪽은 의도가 코드 형태에서 읽히지 않아 인지 비용이 크다. 루프마다 동일하게 생성되는 위젯(divider 등)은 로컬 변수로 한 번 만들어 재사용한다.

**강도:** 관측 컨벤션

> **출처:** [Dart collections](https://dart.dev/language/collections) · [Cognitive Complexity (SonarSource)](https://www.sonarsource.com/resources/cognitive-complexity/) · 프로젝트 실측 (리스트 빌딩 패턴 6종 비교, 2026-04-18)

### 4. 반복 렌더는 builder delegate 로 — children 리스트를 즉시 채우지 않는다 `[어댑터:dart-flutter]`

반복 렌더는 보이는 만큼만 만드는 delegate(`SliverChildBuilderDelegate` · `ListView.builder` · `ListView.separated`)로 쓴다.

```dart
// before — 화면 밖 항목까지 전부 즉시 빌드된다
SingleChildScrollView(
  child: Column(
    children: [
      header,
      for (final item in items) {widget_prefix}RowWidget(item: item),
    ],
  ),
)

// after — 고정 영역은 SliverToBoxAdapter, 목록은 builder sliver
CustomScrollView(
  slivers: [
    SliverToBoxAdapter(child: header),
    SliverList.builder(
      itemCount: items.length,
      itemBuilder: (context, index) =>
          {widget_prefix}RowWidget(item: items[index]),
    ),
  ],
)
```

```dart
// before — shrinkWrap 을 lazy 수단으로 오해한 중첩
ListView(
  shrinkWrap: true,
  children: items.map(_row).toList(),
)

// after
ListView.builder(
  itemCount: items.length,
  itemBuilder: (context, index) => _row(items[index]),
)
```

`SingleChildScrollView` + `Column` 과 `ListView(children: [...])` 은 eager 다. `shrinkWrap: true` 는 lazy 가 아니라 크기 맞춤 옵션이며, `.builder` 와 같이 써도 전체 높이를 재느라 모든 아이템을 빌드해 laziness 를 깬다. **화면당 스크롤 컨테이너는 하나** 이고 중첩 `shrinkWrap` 리스트로 쌓지 않는다.

예외는 하나다 — 콘텐츠가 전부 화면에 들어와 스크롤이 실제로 불필요하면 off-screen 이 없어 lazy 이득이 0 이므로 plain `ListView` 를 쓸 수 있다. **이 예외는 사람이 명시적으로 허락한 건에만 적용한다.** "다 보이니까 괜찮다"를 스스로 판정하지 않는다.

**강도:** 관측 컨벤션 (성능 근거는 SHOULD 수준)

> **출처:** [Flutter performance best practices](https://docs.flutter.dev/perf/best-practices) · [Flutter architectural overview](https://docs.flutter.dev/resources/architectural-overview) · 프로젝트 실측 (2026-06-09 lazy 렌더링 전면 강제)

### 5. leaf 토글은 상태를 자기가 소유한다 — `useState` + `useEffect` 동기화 `[어댑터:dart-flutter]`

체크박스·스위치·슬라이더·세그먼트 탭은 자기 값을 `useState` 로 소유하고 `onChanged` 로 부모에 통지한다. 부모의 외부 override 는 `useEffect` 로 받는다.

```dart
// before — 부모가 상태를 쥐어 토글 한 번에 subtree 가 다시 그려진다
class _ParentState extends State<Parent> {
  bool visible = false;

  @override
  Widget build(BuildContext context) => {widget_prefix}SwitchWidget(
        value: visible,
        onChanged: (v) => setState(() => visible = v),
      );
}

// after — leaf 가 값을 소유하고, override 는 useEffect 로 동기화한다
final value = useState(props.value);
useEffect(() {
  if (value.value != props.value) value.value = props.value;
  return null;
}, [props.value]);

return {widget_prefix}SwitchWidget(
  value: value.value,
  onChanged: (v) {
    value.value = v;
    props.onChanged(v);
  },
);
```

탭할 때 자기만 rebuild 되므로 상위 트리가 흔들리지 않는다. `setState` 는 "possibly triggering rebuilds for the entire subtree rooted at this widget" 이므로, 상태를 상위에 둔 채 하위만 쪼개면 격리 효과가 상쇄된다. `useState` 만으로는 부모의 외부 override(전체 선택 등)가 반영되지 않는데, 초기값이 첫 build 에만 쓰이기 때문이다.

**판정 세부**

- hook 은 `items.isEmpty` 같은 early return **위** 에 둔다(rules of hooks).
- `useEffect` 는 post-frame 이라 부모 override 시 한 프레임 stale 후 반영되며, 이 지연은 수용된 trade-off 다.
- 그룹형 선택자(라디오)는 형제 해제에 부모 rebuild 가 필수라 격리 이득이 없으므로 controlled `StatelessWidget` 으로 남긴다. 내부 토글 상태가 없는 표시 위젯과 외부 controller 입력은 이 원칙의 대상이 아니다.
- 정확성(override 반영)과 격리(perf)는 별개 축이라, 격리까지 원하면 상태를 provider 로 올리고 행 단위 `ref.watch(provider.select(...))` 로 구독을 좁힌다.

**강도:** 관측 컨벤션

> **출처:** [State.setState](https://api.flutter.dev/flutter/widgets/State/setState.html) · [Element.rebuild](https://api.flutter.dev/flutter/widgets/Element/rebuild.html) · 프로젝트 실측 (2026-06-22 `useValueChanged` → `useEffect` 번복 확정)

### 6. 파생 뷰 번들은 freezed state 클래스로 — 익명 Record 금지 `[어댑터:dart-flutter]`

provider 나 VM 이 노출하는 파생값 묶음은 이름 있는 freezed state 로 반환한다.

```dart
// before — 익명 레코드 반환
({int count, bool done, List<Device> items}) deviceView(Ref ref) => (
      count: ref.watch(deviceListProvider).length,
      done: ref.watch(syncProvider).isDone,
      items: ref.watch(deviceListProvider),
    );

// after — 파생 뷰 전용 freezed state
@freezed
class {widget_prefix}DeviceViewState with _${widget_prefix}DeviceViewState {
  const factory {widget_prefix}DeviceViewState({
    required int count,
    required bool done,
    required List<Device> items,
  }) = _{widget_prefix}DeviceViewState;
}

// 화면에서
final state = ref.watch(deviceViewProvider);
final notifier = ref.read(deviceListProvider.notifier);
```

타입명이 없으면 의미와 재사용성이 약하고, 프로젝트 전역이 freezed state 컨벤션이라 표기가 갈린다. 결정적으로 레코드의 `==` 는 List 필드를 identity 로 비교해 freezed 의 깊은 컬렉션 비교와 rebuild 결과가 달라진다.

**판정 세부**

- raw 상태와 파생 상태는 분리한다. 선택·입력 같은 raw 는 Notifier state(`{widget_prefix}XxxState`), 그로부터 계산된 뷰 번들은 derived provider 가 반환하는 별도 freezed state(`{widget_prefix}XxxViewState`) 다.
- 위젯이나 provider 표면에 노출되지 않는 함수 내부 국소 튜플은 레코드로 둬도 된다.
- 화면이 `ref.watch` 로 받는 로컬 변수명은 반환 타입과 무관하게 `state` 로 통일하고, notifier 를 함께 잡으면 `ref.read(...notifier)` 를 별도 변수로 분리한다.

**강도:** 관측 컨벤션

> **출처:** [freezed](https://pub.dev/packages/freezed) · [Riverpod code generation](https://riverpod.dev/ko/docs/concepts/about_code_generation) · 프로젝트 실측 (2026-06-23 파생 provider 레코드 반환 지적)

### 7. 콜백 typedef 는 위젯별 시맨틱으로 로컬 정의한다 `[어댑터:dart-flutter]`

각 콜백 prop 은 자기 의미를 드러내는 typedef 로 선언한다. generic 프리미티브 typedef 를 prop 타입으로 직접 재사용하지 않는다.

```dart
// before — 세 콜백이 같은 타입이라 타입에서 의미를 읽을 수 없다
class {widget_prefix}DeviceItemWidgetProps {
  final {widget_prefix}SwitchChanged onVisibleChanged;
  final {widget_prefix}SwitchChanged onFwUpdateChanged;
  final {widget_prefix}SwitchChanged onPairingChanged;
}

// after — 의미 원천 위젯이 같은 파일 top-level 에 소유한다
typedef {widget_prefix}DeviceVisibleChanged = void Function(bool isVisible);
typedef {widget_prefix}DeviceFwUpdateChanged = void Function(bool isEnabled);
typedef {widget_prefix}DevicePairingChanged = void Function(bool isPaired);

class {widget_prefix}DeviceItemWidgetProps {
  final {widget_prefix}DeviceVisibleChanged onVisibleChanged;
  final {widget_prefix}DeviceFwUpdateChanged onFwUpdateChanged;
  final {widget_prefix}DevicePairingChanged onPairingChanged;
}
```

소유권 규칙은 하나다. **typedef 는 그 콜백의 의미 원천 위젯이 같은 파일 top-level 에 정의하고, 상위 컴포지트와 화면은 import 해서 쓴다.** 의미 원천은 그 콜백이 제어하는 실제 UI 를 그리는 위젯이며, forward 만 하는 상위는 새로 정의하지 않는다.

**판정 세부**

- 프리미티브 위젯(switch/button/checkbox/radio/slider)은 자기 base typedef 를 계속 소유한다.
- 시맨틱 typedef 는 함수 시그니처가 같아 base prop 으로 forward 할 때 구조적으로 대입된다.
- 공유 typedef 파일(`*_typedef.dart` 류)은 만들지 않으며, 같은 이름 typedef 를 co-import 되는 두 파일에 각각 정의하는 것도 금지다.

**강도:** 관측 컨벤션

> **출처:** [Effective Dart — design](https://dart.dev/effective-dart/design) · 프로젝트 실측 (2026-06-25 개정, 프리미티브 재사용 조항 폐기)

### 8. `///` 는 계약이 있을 때만 — 로직 있는 메서드는 레이어 무관하게 단다 `[어댑터:dart-flutter][한국어]`

주석 문법의 기본값은 `//` 다. `///` 는 public 메서드의 파라미터·반환값 블록, 진짜 계약과 제약, 파일 헤더 관례 세 자리에만 쓴다.

```dart
// before — 이름을 옮기기만 한 필드 doc + 본문 섹션 헤더
class {widget_prefix}CardWidgetProps {
  /// 버튼 텍스트
  final String? text;
}

/// 길게 누르기를 처리합니다.
/// 정책: 200ms 마다 반복
/// 참고: interval 이 0 이면 1회만
void handleLongPress(Duration interval) { ... }

// after — 자명한 필드 doc 은 삭제, 계약은 라벨 표기로
class {widget_prefix}CardWidgetProps {
  final String? text;
}

/// 길게 누르기 반복을 시작한다.
/// - [interval]: 반복 간격. 0 이면 1회만 호출한다
/// - 반환값: 없음
void startLongPressRepeat(Duration interval) { ... }
```

`///` 는 dartdoc 이 수집하는 API 문서용이라 자명한 필드에 붙으면 생성 코드까지 오염된다 — freezed 는 constructor parameter 의 `///` 를 property 와 class 레벨로 전파한다. 이름을 한국어로 옮기기만 하는 필드 doc 은 금지이며 `antipattern-catalog.md` 의 A 카테고리다.

**판정 세부**

- 커버리지 판정은 레이어가 아니라 **로직 유무** 로 한다. provider · model · service · repository · util 뿐 아니라 화면·뷰의 핸들러·리스너 헬퍼도 로직이 있으면 doc 을 단다. 면제되는 것은 `build` 와 자명한 getter 뿐이고, private 도 자명하지 않으면 단다. 화면·VM 메서드 doc 을 "화면이니까"라는 이유로 떼는 것은 컨벤션 이탈이다.
- 진짜 계약이란 `textStyle` 을 지정하면 `textColor` 가 무시되는 식의 오용 유발 규칙이다.
- 본문은 한두 문장으로 끝낸다. `정책:` · `참고:` · `주의:` 같은 본문 내 섹션 헤더와 알고리즘 단계 나열은 doc 이 아니라 설계 문서의 몫이다.
- `[]` 대괄호 링크는 파라미터 선언부에서 의무이고 본문에서는 식별자 언급이 꼭 필요할 때만 쓴다.
- **라벨 표기(`- [param]:` · `- 반환값:` · void 는 `없음`)와 본문 문체는 한국어 축이므로** `korean-technical-writing.md` 를 참조한다 — 이 문서는 표기를 다시 정의하지 않는다.

**강도:** SHOULD

> **출처:** [Effective Dart — documentation](https://dart.dev/effective-dart/documentation) · [freezed](https://pub.dev/packages/freezed) · [Material.surfaceTintColor](https://api.flutter.dev/flutter/material/Material/surfaceTintColor.html)

### 9. expression body 를 기본값으로, 1회용 로컬 변수는 인라인한다 `[어댑터:dart-flutter]`

단일 expression 함수는 `=>` 로 쓰고, 한 곳에서만 쓰이는 로컬 변수는 사용처에 인라인한다.

```dart
// before
Widget _thumbnail() {
  return Image.asset(props.path);
}

@override
Widget build(BuildContext context) {
  final thumbnail = _thumbnail();
  return Center(child: thumbnail);
}

// after
Widget _thumbnail() => Image.asset(props.path);

@override
Widget build(BuildContext context) => Center(child: _thumbnail());
```

block body 는 분기가 있거나 statement 가 둘 이상일 때만이다. 로컬 변수가 한 곳에서만 쓰이면 선언 자체가 노이즈이므로, 한 번 쓰고 마는 `final thumbnail = _thumbnail();` 보다 호출을 그 자리에 두는 편이 읽기 경로가 짧다. cascade(`..`)는 같은 참조에 연속 호출할 때만 쓰고, extension 은 짧고 명확한 도메인 어휘만 붙여 formatter·helper dumping ground 로 만들지 않는다.

**강도:** SHOULD

> **출처:** [Effective Dart — style](https://dart.dev/effective-dart/style) · [cascade_invocations](https://dart.dev/tools/linter-rules/cascade_invocations) · [Dart extension methods](https://dart.dev/language/extension-methods)

### 10. Notifier 비대화를 막는다 — 상태 전이는 단일 reducer 로 `[어댑터:dart-flutter]`

status 별 헬퍼 다발을 만들지 않고 파라미터를 받는 reducer 하나로 통합한다.

```dart
// before — status 5종 × sub-state 3종이면 헬퍼가 15개로 늘어난다
void _notifyUpdateStarted() =>
    state = state.copyWith(status: UpdateStatus.running, percent: 0);
void _notifyUpdateProgress(double percent) =>
    state = state.copyWith(percent: percent);
void _notifyUpdateCompleted(UpdateResult result) =>
    state = state.copyWith(status: UpdateStatus.completed, result: result);
void _notifyUpdateFailed(String message) =>
    state = state.copyWith(status: UpdateStatus.failed, message: message);
void _notifyUpdateCancelled() =>
    state = state.copyWith(status: UpdateStatus.cancelled);

// after
void _setUpdateState({
  required UpdateStatus status,
  double? percent,
  String? message,
  UpdateResult? result,
}) =>
    state = state.copyWith(
      status: status,
      percent: percent ?? state.percent,
      message: message,
      result: result,
    );
```

```dart
// before — 다이얼로그 progress 용 ValueNotifier 신설
final progress = ValueNotifier<double>(0);
showDialog(
  context: context,
  builder: (_) => ValueListenableBuilder<double>(
    valueListenable: progress,
    builder: (_, value, __) => {widget_prefix}ProgressDialogWidget(percent: value),
  ),
);

// after — progress 는 provider state 에 두고 ref.listen 으로 push/pop 한다
ref.listen(updateProvider, (previous, next) {
  if (next.status == UpdateStatus.running && previous?.status != next.status) {
    showDialog(context: context, builder: (_) => const {widget_prefix}ProgressDialogWidget());
  }
  if (next.status == UpdateStatus.completed) Navigator.of(context).pop();
});
```

비대화의 실제 원인은 줄 수가 아니라 조합 폭발이다. Notifier 파일 하나에 enum + freezed 모델 + extension + Notifier 본체 + 헬퍼를 다 넣지 않고, 1000줄을 넘으면 state 모델 · helper extension · Notifier 본체(실행 흐름과 reducer 만) 세 파일로 분할한다.

**판정 세부**

- `isIdle` · `isRunning` · `isCompleted` 같은 extension getter 를 sub-state 마다 양산하지 않는다. 호출부에서 enum 을 직접 비교하는 편이 명확하고, 정말 자주 쓰이는 1~2개만 추출한다.
- 호출자가 쓰지 않는 저수준 메서드를 public 으로 노출하지 않고, 미래 확장을 가정한 boilerplate 도 만들지 않는다. 통합 실행 흐름만 public 이고 그 안의 단계는 private 이거나 service 다.

**강도:** 관측 컨벤션

> **출처:** [Riverpod code generation](https://riverpod.dev/ko/docs/concepts/about_code_generation) · [Riverpod — what's new](https://riverpod.dev/docs/whats_new) · [Yagni (Fowler)](https://martinfowler.com/bliki/Yagni.html) · 프로젝트 실측 (2026-06 Notifier 분할)

### 11. Props 규칙은 두 벌이다 — 신규 설계와 기존 위젯 제거는 스코프가 다르다 `[어댑터:dart-flutter]`

신규 위젯에는 설계 기준(`required` · 미사용 Props 금지)을, 기존 위젯 리팩토링에는 제거 판정 기준을 적용한다. 두 규칙을 합치지 않는다.

```dart
// before — (a) 신규 설계: 항상 넘기는 필드가 nullable, 아무도 안 쓰는 Props, 추측 레이아웃
class {widget_prefix}DeviceItemWidgetProps {
  final Device? device;        // 호출부 전수가 채운다
  final bool? isDense;         // 호출자 0곳
  final Color? borderColor;    // 호출자 1곳이 매번 {TokenClass}.line 고정
  final double? width;
}

Widget build(BuildContext context) => Stack(  // 소비자 레이아웃을 추측해 미리 감쌌다
      children: [ClipRRect(child: props.child)],
    );

// after
class {widget_prefix}DeviceItemWidgetProps {
  const {widget_prefix}DeviceItemWidgetProps({required this.device, this.width});
  final Device device;   // required 핵심 데이터
  final double? width;   // 치수 표준 옵션 — 호출자 0건이어도 유지
}

Widget build(BuildContext context) => props.child;  // child 슬롯은 그대로 전달

// (b) 제거된 borderColor 는 build 에 인라인
decoration: BoxDecoration(border: Border.all(color: {TokenClass}.line)),
```

**(a) 신규 위젯 Props 설계 시** — 항상 넘기는 필드는 `required` 로 선언하고 nullable + `!` 강제 캐스트 조합을 만들지 않는다. 미사용 Props 는 처음부터 만들지 않으며 "나중에 쓸 수 있으니까"는 보존 사유가 아니다. 프로젝트에 이미 있는 장식 위젯이 있으면 Props 로 노출하지 말고 위젯 내부에서 직접 쓴다. 래퍼 위젯은 child 슬롯을 그대로 전달하고, 소비자가 어떤 레이아웃을 쓸지 추측해 `Stack` 이나 클리핑을 미리 감싸지 않는다.

**(b) 기존 위젯 리팩토링 시 Props 제거 판정** — 제거 후보는 실제 화면 호출자가 0곳인 스타일 Props, **또는** 호출자가 1곳뿐인데 매번 고정 장식값(색·radius·배경·fit)을 넘기는 Props 다. 후자는 범용성이 0이므로 build 에 값을 인라인하고 Props 에서 뺀다. 유지 대상은 치수 표준 옵션(width/height/size), slider 의 min/max, 동적값, required 핵심 데이터, 호출자 2곳 이상이며, 치수는 호출자 0건에 기본값과 중복이어도 제거하지 않는다. 사용 여부 판정에 공통 위젯 pass-through 와 dev 쇼케이스를 포함하지 않는다. 보고는 카운트가 아니라 **각 호출자가 실제로 넘기는 값을 코드 그대로** 인용한다 — "호출자 2곳"만 적으면 유지·제거·통일 판단이 불가능해 되묻게 된다.

**강도:** 관측 컨벤션

> **출처:** [Effective Dart — design](https://dart.dev/effective-dart/design) · [Yagni (Fowler)](https://martinfowler.com/bliki/Yagni.html) · 프로젝트 실측 (2026-06-12 · 2026-06-16 · 2026-06-17 3회 보정)

### 12. bare `catch (e)` 는 이 코퍼스의 의도된 컨벤션이다 `[어댑터:dart-flutter]`

`on` 절 없는 catch 는 실수가 아니라 선택이다. `on Exception` 으로 좁히지 않는다.

```dart
// before — 좁힌 catch 가 비-Exception throw 를 놓쳐 동작이 깨진다
try {
  await repository.fetchDevices();
} on Exception catch (e) {
  state = state.copyWith(error: e.toString());
}

// after — 모든 throwable 을 상태·로그로 흡수한다
try {
  await repository.fetchDevices();
} catch (e, st) {
  logger.e('fetchDevices 실패', error: e, stackTrace: st);
  state = state.copyWith(error: e.toString());
}
```

목적은 Dart 의 모든 throwable(`Object` 루트 — `Exception` · `Error` · 임의 객체)을 전부 잡아 상태나 로그로 흡수하는 것이고, provider·VM 의 에러 싱크가 대표 사례다. 비-`Exception` 객체를 던지는 경로(예: 응답 에러 필드 타입이 `Object?` 인 HTTP 레이어)가 있으면 좁힌 catch 가 그 throw 를 놓친다 — 커버리지가 줄 뿐 늘지 않는다.

**리뷰나 QA 가 bare catch 를 지적하면 무효 판정으로 처리한다.** 이 규칙은 코퍼스 실측에 근거하며 **공개 1차 출처가 없다.** 다른 코퍼스로 옮길 때는 그 코퍼스에서 같은 비율이 관측되는지 먼저 확인하고, 확인 없이 이관하지 않는다.

**강도:** 관측 컨벤션

> **출처:** 프로젝트 실측 (bare `catch (e)` 27건 vs `on Exception` 3건, 2026-06-26). 공개 1차 출처 없음

---

## 어댑터 슬롯

`tone-guide` 와 `tone-scaffold` 가 이 표에서 값을 읽는다.

| 슬롯 | dart-flutter 값 |
|---|---|
| `comment_syntax` | 기본 `//`. `///` 는 dartdoc 전용이며 원칙 8 의 3개 용도에만. 블록 주석 `/* */` 미사용 |
| `doc_param_format` | `/// - [param]: 설명` — 파라미터 선언부에서 `[]` 링크 의무, 본문에서는 필요할 때만 |
| `doc_return_label` | `/// - 반환값: 설명`, void 는 `- 반환값: 없음` (`N/A` 신규 도입 금지). **한국어 축 — 표기 상수의 소유자는 `korean-technical-writing.md` 다** |
| `helper_prefix_forbidden` | `_build*` (위젯 반환 private 헬퍼 접두사). 판정·처리 방침은 `antipattern-catalog.md` I 카테고리, 추출 임계는 `extraction-thresholds.md` |
| `separator_pattern` | 고정 gap → `Row`/`Column` 의 `spacing:`. 리스트 separator → `ListView.separated` 의 `separatorBuilder`. `.expand().skip()` 체이닝과 수동 `SizedBox` 나열 금지 |
| `fallback_identifier_pattern` | `\b(effective\|resolved)[A-Z]` — 금지 접두사. 처리는 삭제가 아니라 도메인·역할명으로 개명 |
| `naming_suffix` | 위젯 클래스 `{widget_prefix}...Widget` · Props `...WidgetProps` · raw 상태 `...State` · 파생 뷰 `...ViewState` · 콜백 typedef `...Changed` / `...Tap`. 클래스 UpperCamelCase, 파일 snake_case |
| `state_lib` | Riverpod(`@riverpod` Notifier + `select`) + flutter_hooks(`HookConsumerWidget`, `useState`/`useEffect`) + freezed state 클래스 |
| `codegen_cmd` | **프로젝트 감지 — 상수 아님.** 버전 매니저 래퍼(`fvm` 등) 유무와 `dart` / `flutter` 선택이 프로젝트마다 다르다. 형태는 `<래퍼> <dart\|flutter> run build_runner build --delete-conflicting-outputs` |
| `audit_greps` | 아래 10종. 전부 bash·zsh 양쪽에서 실행 검증했고 각각 양성 케이스 1건 이상을 실제로 잡는 것을 확인했다 |

완료 게이트 grep 목록(`audit_greps`):

```text
grep -rnE 'shrinkWrap:[[:space:]]*true' --include='*.dart' <src>
grep -rn  'SingleChildScrollView' --include='*.dart' <src>
grep -rnE '\b_build[A-Z][A-Za-z0-9]*\(' --include='*.dart' <src>
grep -rnE '\b(effective|resolved)[A-Z]' --include='*.dart' <src>
grep -rnE '\.expand\(' --include='*.dart' <src>
grep -rnE '\b(ValueNotifier|ValueListenableBuilder)\b' --include='*.dart' <src>
grep -rnE '\}[[:space:]]*on[[:space:]]+[A-Z][A-Za-z0-9_]*[[:space:]]+catch' --include='*.dart' <src>
grep -rnE 'if[[:space:]]*\([[:space:]]*[A-Za-z_.]+[[:space:]]*!=[[:space:]]*null[[:space:]]*\)' --include='*.dart' <src>
grep -rnE '\(\{[^)]*\}\)[[:space:]]+[a-z][A-Za-z0-9_]*[[:space:]]*\(' --include='*.dart' <src>
grep -rnE '^[[:space:]]*//[[:space:]]*[-=]{5,}' --include='*.dart' <src>
```

### grep 판정표 — 히트가 곧 위반인가

| # | 잡는 것 | 히트 = 위반? | 판정 방법 |
|---|---|---|---|
| 1 | `shrinkWrap: true` | 조건부 | lazy 수단으로 쓴 자리는 위반이다(원칙 4). 히트마다 판정을 적는다 |
| 2 | `SingleChildScrollView` | 조건부 | eager 다. 스크롤이 실제로 불필요한 건은 사람이 명시 허락한 경우에만 유지 |
| 3 | `_build*` 헬퍼 | **아니다** | 금지 접두사이되 인라인/위젯 승격 판정은 `extraction-thresholds.md` 와 `antipattern-catalog.md` I 카테고리에 있다 |
| 4 | `effective*` / `resolved*` | 예 | 삭제가 아니라 도메인·역할명으로 개명한다 |
| 5 | `.expand(` | 조건부 | separator 체이닝이면 위반(원칙 3). 그 외 용도는 트릭성 여부를 따로 판정한다 |
| 6 | `ValueNotifier` / `ValueListenableBuilder` | 조건부 | 다이얼로그 progress 신설이면 위반(원칙 10). provider state + `ref.listen` 으로 옮긴다 |
| 7 | `} on Xxx catch` | **아니다** | 위반이 아니라 원칙 12 의 컨벤션 이탈 후보다 |
| 8 | `if (x != null)` | **아니다** | 과수집되므로 경계부 `!` 를 걸러 낸 뒤 판정한다 |
| 9 | 익명 레코드 반환 함수 | 예 | 준수 상태에서는 0건이 정상이다(원칙 6) |
| 10 | `// =====` 구분선 주석 | 예 | 지운다. 카테고리 판정은 `antipattern-catalog.md` |

---

## 수치 기준

| 항목 | 값 | 출처 |
|------|-----|------|
| `?element` (null-aware element) 최소 버전 | Dart 3.8 | 원본 규칙 문서 기록 (2026-04-18) |
| `if case` 사용 가능 위치 | statement · collection element 2곳 | [Dart patterns](https://dart.dev/language/patterns) |
| `switch` expression 전환 분기 수 | 3분기 이상 (2분기는 삼항 / `if`) | 프로젝트 실측 |
| 화면당 스크롤 컨테이너 | 1개 | 프로젝트 실측 (2026-06-09) |
| Notifier 파일 분할 하한 | 1000줄 | 프로젝트 실측 (2026-06) |
| status 헬퍼 통합 대상 규모 | 5종 × 3 sub-state = 15개 → reducer 1개 | 프로젝트 실측 |
| state extension getter 허용 개수 | 1~2개 | 프로젝트 실측 |
| bare `catch (e)` vs `on Exception` | 27건 vs 3건 | 프로젝트 실측 (2026-06-26) |
| `useEffect` 동기화 지연 | 1프레임 (post-frame, 수용됨) | 프로젝트 실측 (2026-06-22) |
| 공유 typedef 파일 허용 개수 | 0개 | 프로젝트 실측 (2026-06-25) |
| doc 라벨 표기 상수 | `- [param]:` / `- 반환값:` | `korean-technical-writing.md` (한국어 축 SSOT) |
| `audit_greps` 실행 검증 | 10종 전부, bash·zsh 양쪽 + 양성 케이스 확인 | 본 문서 |

---

## 안티패턴

| 안티패턴 | 문제 |
|----------|------|
| `if (x != null) Widget(x!)` | 컴파일러가 이미 아는 사실을 `!` 로 재단언한다. `if case final v?` 로 바인딩하면 `!` 가 사라진다 |
| 2분기 null 체크에 `switch` expression | `switch` 는 분기 3개부터 이득이 난다. 2분기에서는 삼항보다 길기만 하다 |
| expression 위치에 `if case` 시도 | named parameter 자리에서는 문법이 성립하지 않는다. 컴파일 실패 후 `!` 로 회귀한다 |
| `children` 사이 수동 `SizedBox` 나열 | `spacing:` 파라미터의 수동 재구현. 항목이 늘 때마다 삽입 위치를 사람이 관리해야 한다 |
| `.expand((w) => [div, w]).skip(1)` | 트릭성 체이닝. 의도가 코드 형태에서 읽히지 않는다 |
| `for-in` / `.map().toList()` 로 children 채우기 | 화면 밖 항목까지 즉시 빌드된다. 반복 렌더는 builder delegate 가 담당한다 |
| `shrinkWrap: true` 를 lazy 수단으로 사용 | shrinkWrap 은 크기 맞춤이다. `.builder` 와 함께 써도 전체 높이 측정이 laziness 를 깬다 |
| 부모가 leaf 토글 상태를 소유 | 토글 한 번에 subtree 전체가 rebuild 된다. 상태를 leaf 로 내리는 것이 추출보다 먼저다 |
| `useState` 만 두고 `useEffect` 동기화 생략 | 초기값은 첫 build 에만 쓰인다. 부모의 외부 override 가 화면에 반영되지 않는다 |
| provider 가 익명 레코드 반환 | 타입명이 없어 의미가 약하고, List 필드 `==` 가 identity 비교라 rebuild 동작이 freezed 와 달라진다 |
| 프리미티브 typedef 를 컴포지트 prop 타입으로 재사용 | 서로 다른 콜백이 같은 타입이 되어 타입에서 의미를 읽을 수 없다 |
| 자명한 필드에 `///` doc | freezed 가 property·class 레벨로 전파해 생성 코드까지 오염된다. A 카테고리 위반 |
| status 별 `_notifyXxx*` 헬퍼 다발 | 조합 폭발로 헬퍼가 15개까지 늘어난다. 단일 reducer 하나로 대체된다 |
| 다이얼로그 progress 용 `ValueNotifier` 신설 | provider state 에 있어야 할 상태가 UI 레이어에 따로 생겨 화면 간 패턴이 갈린다 |
| Props 제거 판정에 dev 쇼케이스 포함 | 실사용이 아닌 코드가 유지 근거로 둔갑한다 |
| `on Exception` 으로 catch 좁히기 | 비-`Exception` throw 를 놓쳐 동작이 깨진다. 커버리지가 줄 뿐 늘지 않는다 |

---

## Gotchas

- **리스트 빌딩 규칙은 개정 이력이 뒤집혀 있다** — 원본 규칙 세트의 리스트 빌딩 절은 `for-in` 과 `.indexed.map().toList()` 로 children 을 채우는 것을 권장했지만, 이후 lazy 렌더링 절이 이를 전면 금지했다. **뒤의 것이 승** 이다. 옛 절에서 살아남은 것은 `spacing:` 사용과 함수형 체이닝 금지뿐이고, children 을 어떻게 만드는가는 builder delegate 가 지배한다. 옛 예시를 다시 끌어오지 마라.
- **`useValueChanged` 인용도 폐기됐다** — 상태 동기화 훅으로 `useValueChanged` 를 권고한 조항은 2026-06-22 에 `useEffect` 로 번복됐다. 근거는 성능이 아니라 프로젝트 일관성이며, 1프레임 stale 은 수용된 비용이다. 두 훅을 코퍼스에 섞어 두면 동기화 패턴이 파일마다 갈린다.
- **`- 반환값: 없음` 을 노이즈로 보고 지우지 마라** — 삭제 지시가 남아 있는 옛 문서를 보고 정리하면 "doc 이 없는 것"과 "반환값이 없는 것"을 구분할 수 없게 된다. 유지가 확정된 판정이고, 표기 규칙 자체는 `korean-technical-writing.md` 가 소유한다.
- **`_build*` grep 히트는 위반 건수가 아니다** — 이 문서는 접두사를 금지 목록에 올리지만, 인라인할지 위젯으로 승격할지의 판정식은 `extraction-thresholds.md` 와 `antipattern-catalog.md` I 카테고리에 있다. 히트를 세어 그대로 보고하면 추출이 정당한 건까지 위반으로 집계된다.
- **위젯 클래스로 뺐다고 rebuild 가 끊기지 않는다** — 격리 조건(동일 인스턴스, `runtimeType` + `key`)은 `extraction-thresholds.md` 원칙 5 에 있다. 상태 소유를 안 고친 채 파일만 늘리면 프레임 비용은 그대로다.
- **bare catch 컨벤션은 이 코퍼스 한정이다** — 실측 비율(27 vs 3)이 근거의 전부이고 공개 1차 출처가 없다. 다른 프로젝트에 그대로 옮기면 실측 없는 규칙을 강제하는 것이 된다. 킷이 이 규칙을 켤 때는 대상 코퍼스에서 같은 grep 을 먼저 돌린다.
- **다른 스택 어댑터를 이 문서에서 복제하지 마라** — Rust 나 TypeScript 어댑터가 필요해지면 그 스택에서 위반이 실제로 관측된 뒤에 만든다. 코어 원칙은 `extraction-thresholds.md` 와 `antipattern-catalog.md` 가 이미 스택 무관으로 들고 있으므로, 어댑터는 문법 관용구와 슬롯 값만 갖는다.
