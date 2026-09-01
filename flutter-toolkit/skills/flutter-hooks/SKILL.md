---
name: flutter-hooks
description: >
  Flutter Hooks 패턴 가이드. HookWidget/HookConsumerWidget 사용 규칙,
  StatefulWidget → HookWidget 마이그레이션 패턴, 커스텀 Hook 작성법,
  @freezed Props 번들링 규칙을 안내한다.
  "훅", "hooks", "useState", "useEffect", "HookWidget", "HookConsumerWidget",
  "커스텀 훅", "custom hook", "Props 번들링", "hook 사용법",
  "useAnimationController", "StatefulWidget 전환", "hook migration" 같은
  키워드가 나오면 이 스킬을 참조한다.
  /flutter-widget 스킬에서 위젯을 생성할 때도 이 스킬의 규칙을 따른다.
  HAS_HOOKS 감지 시에만 활성화된다.
user-invocable: true
---

## Gotchas

- StatefulWidget/ConsumerStatefulWidget 신규 작성 금지 — HookWidget/HookConsumerWidget만 사용. `hooks_riverpod` 패키지에서 import한다 (`flutter_riverpod` 아님)
- PageController 등 컨트롤러를 build() 안에서 직접 생성하면 리빌드마다 메모리 누수 — `useMemoized(() => PageController())`로 감싸라
- async 작업 후 상태 변경 전에 반드시 `ref.mounted` 확인 — 안 하면 "setState() called after dispose" 크래시
- **`async` 메서드에서 `showDialog` / `Navigator.push` / `Future<T>` 결과 수신 후 같은 `BuildContext` 를 재사용하기 전에는 반드시 `if (!context.mounted) return;`** — async gap 동안 위젯이 dispose 되면 `context.pop`, `ScaffoldMessenger.of(context)`, `Theme.of(context)` 호출이 크래시로 이어진다. `ref.mounted` 는 Notifier 생명주기, `context.mounted` 는 Widget 생명주기이므로 둘은 별개다 (apps sprint-feedback iter 2, UI-06 / AR-01 FIX 패턴 기반)
- AnimationController는 반드시 `useAnimationController()`로 생성. dispose 자동 관리됨
- `HAS_FREEZED = true` 프로젝트에서 HookWidget 생성 시 파라미터를 개별 필드로 받지 말고 반드시 `@freezed Props` 클래스로 번들링 — 개별 파라미터 나열은 Props 패턴 위반. 디자인 시스템 Named constructor variant 위젯만 면제
- `HAS_FREEZED = true` + `HAS_HOOKS = true`가 모두 true인 프로젝트에서는 `HookWidget` + `@freezed Props` 조합이 프로젝트 표준 — ConsumerWidget이나 StatelessWidget으로 만들면 일관성 깨짐
- `build()` 메서드는 **100줄 이하 권장** — 그 이상이면 private Widget 클래스로 분리하여 composition 을 적용하라. 합성이 메서드 분리보다 성능·재사용성·테스트 가능성 모두 우수하다 (Flutter 공식 AI rules + apps CG-12 관습)
- **가이드형 스킬도 Process Step 순서 고정 (agent §3.5 Binary Decidability 대응)** — 본 스킬은 "가이드" 이지만 적용 시 **탐색 → 진단 → 처방 → 검증** 4-Step 순서를 반드시 지킨다. (1) 탐색: 대상 파일을 `Read` 로 읽고 현재 사용 중인 pattern(StatefulWidget / HookWidget / ConsumerWidget / HookConsumerWidget) 과 HAS_HOOKS/HAS_FREEZED 감지값을 확인. (2) 진단: Gotchas 의 각 규칙에 대한 위반 여부를 파일:라인 근거와 함께 이진(위반/준수) 으로 판정. (3) 처방: 위반 항목별 마이그레이션 diff 또는 새 작성 템플릿 제시. (4) 검증: 아래 Gotcha 참조. 단계를 건너뛰고 "이렇게 하면 됩니다" 로 바로 넘어가면 사용자가 상태 파악을 재수행해야 한다
- **정적 확인은 "동작 확인" 이 아니다 (digest `false-positive-static-verification`)** — hook 마이그레이션은 컴파일이 통과해도 런타임 생명주기가 바뀐다 (`useMemoized` 캐시 키 · `useEffect` dispose 타이밍 · `useAnimationController` 자동 dispose). 처방 후 검증 단계에서 (a) `$FLUTTER analyze` 를 **실행하고 출력을 인용**하고, (b) 대상에 테스트가 있으면 `$FLUTTER test <경로>` 를 실행해 출력을 인용한다. 실행하지 않았으면 "정상 동작합니다" 대신 `[미검증]` 마커와 사유를 남긴다. 코드를 읽고 "문제 없어 보인다" 고 쓰는 것은 증거가 아니다 (`harness/docs/guides/qa-evaluation-guide.md` §Canonical Unverified-Evidence Protocol 4 항). UI 가 함께 바뀌었으면 `references/visual-evidence-protocol.md` 도 실행한다
- **Freezed 3 union 분기 (2026-08 정정)** — `@freezed sealed class` 로 선언한 뒤 Dart 3 `switch` expression 또는 `if case` 로 pattern matching 하는 것이 **신규 코드 권장 형태**다. 다만 `.when` / `.map` 이 **영구 제거된 것은 아니다** — 3.0 에서 제거됐다가 **3.1.0 에서 다시 추가**됐고 최신 stable 은 3.2.5 다. 레거시 `.when(success:, failure:)` 를 **일괄 교체 대상으로 삼지 마라.** 프로젝트가 이미 그 형태를 쓰고 있으면 일관성이 우선이고, 교체는 해당 파일을 어차피 손볼 때만 한다 (출처: <https://pub.dev/packages/freezed/changelog>)

# Flutter Hooks + Props 패턴 가이드

## 0. 프로젝트 감지

`references/project-detection.md`의 절차를 실행하여 프로젝트 환경을 파악한다.
이후 단계에서 감지 결과(`$FLUTTER`, `$DART`, `$PACKAGE`, `HAS_HOOKS`, `HAS_FREEZED`, `HAS_RIVERPOD`)를 사용한다.

### 활성화 조건

- **`HAS_HOOKS = true`** 필수. `flutter_hooks` 또는 `hooks_riverpod`가 pubspec.yaml에 없으면:
  > "flutter_hooks가 pubspec.yaml에 없습니다. Hooks 패턴을 사용하려면 먼저 설치해주세요:
  > `$FLUTTER pub add flutter_hooks`"
- `@freezed Props` 섹션은 `HAS_FREEZED = true`일 때만 적용

---

## 위젯 타입 선택

```text
Riverpod ref 필요? (HAS_RIVERPOD = true)
  ├─ Yes → HookConsumerWidget (build(context, ref))
  └─ No  → HookWidget (build(context))

HAS_RIVERPOD = false
  └─ 항상 HookWidget (build(context))
```

---

## 사용 규칙

### 반드시 지켜야 하는 것

| 기존 패턴 (StatefulWidget) | Hooks 패턴 |
|---------------------------|-----------|
| `StatefulWidget` | `HookWidget` |
| `ConsumerStatefulWidget` | `HookConsumerWidget` |
| `AnimationController` + `SingleTickerProviderStateMixin` | `useAnimationController(duration: ...)` |
| `Timer` + `dispose` | `useEffect(() { final t = Timer(...); return t.cancel; }, [deps])` |
| `FocusNode` + `addListener` + `dispose` | `useFocusNode()` |
| `ScrollController` + `dispose` | `useScrollController()` |
| `TextEditingController` + `dispose` | `useTextEditingController()` |
| `setState(() => _x = v)` | `final x = useState(initialValue)` → `x.value = v` |
| `didUpdateWidget(old) { if (widget.x != old.x) ... }` | `useEffect(() { ... }, [x])` |
| 갱신 없이 참조만 유지하는 객체 | `useRef<T>(initialValue)` |
| `CurvedAnimation` / `Tween` (재생성 불필요) | `useMemoized(() => CurvedAnimation(...), [controller])` |

`HAS_RIVERPOD`인 프로젝트에서 `hooks_riverpod` 패키지를 사용 중이면:
- `import 'package:hooks_riverpod/hooks_riverpod.dart'` 사용
- `flutter_riverpod` import 금지

### 금지 사항

- `StatefulWidget` / `ConsumerStatefulWidget` 신규 작성 금지
- `SingleTickerProviderStateMixin` / `TickerProviderStateMixin` 사용 금지
- `GlobalKey<State>`로 자식 위젯 메서드 호출 금지 — 콜백 + `useState`로 대체
- `useEffect` 의존성 배열 누락 금지 (빈 배열 `[]`은 mount-only에만 허용)

---

## 프로젝트 커스텀 Hook 스캔

위젯에서 Hook을 사용하기 전에 프로젝트에 이미 만들어진 커스텀 Hook이 있는지 확인한다.
이 단계를 거치지 않으면 이미 존재하는 Hook을 중복 구현하게 된다.

탐색 위치:
- `lib/core/hooks/`
- `lib/shared/hooks/`
- `lib/utils/hooks/`
- `lib/` 내 `use_*.dart` 패턴 파일

발견된 커스텀 Hook이 있으면:
1. 각 Hook의 시그니처와 doc comment를 읽는다
2. 현재 작업에 사용할 수 있는 Hook이 있으면 새로 만들지 않고 사용한다
3. 비슷한 기능의 Hook이 있으면 확장을 제안한다

---

## 커스텀 Hook 작성법

프로젝트에서 반복되는 상태 패턴이 2회 이상 나타나면 커스텀 Hook으로 추출한다.

### 커스텀 Hook 작성 규칙

1. **함수명**: `use` prefix 필수 (예: `useDebounced`, `usePaginationScroll`)
2. **위치**: `lib/core/hooks/` 또는 프로젝트 구조에 맞는 공용 위치
3. **반환타입**: 단일 값이면 해당 타입, 복합 값이면 Record `({Type a, Type b})`
4. **의존성**: 외부 값에 의존하면 파라미터로 받고, `useEffect`의 `keys`에 포함
5. **이름 충돌 주의**: 커스텀 Hook 이름이 `flutter_hooks` 패키지의 표준 Hook과 겹칠 수 있다 (예: `useDebounced`). 이 경우 import 시 `hide`로 충돌을 해결해야 한다:
   ```dart
   import 'package:flutter_hooks/flutter_hooks.dart' hide useDebounced;
   import 'package:my_app/core/hooks/use_debounced.dart';
   ```

### 커스텀 Hook 템플릿

```dart
/// [설명] — [용도]를 위한 커스텀 Hook.
T useMyHook<T>(T value, {Duration duration = const Duration(milliseconds: 400)}) {
  final state = useState(value);

  useEffect(() {
    final timer = Timer(duration, () => state.value = value);
    return timer.cancel;
  }, [value, duration]);

  return state.value;
}
```

### Record 반환 패턴 (복합 상태)

```dart
/// 카운트다운 타이머 Hook.
({int remaining, VoidCallback reset}) useCountdown({
  required int totalSeconds,
  VoidCallback? onComplete,
}) {
  final remaining = useState(totalSeconds);

  useEffect(() {
    if (remaining.value <= 0) {
      onComplete?.call();
      return null;
    }
    final timer = Timer(const Duration(seconds: 1), () {
      remaining.value--;
    });
    return timer.cancel;
  }, [remaining.value]);

  return (
    remaining: remaining.value,
    reset: () => remaining.value = totalSeconds,
  );
}
```

### 흔한 커스텀 Hook 패턴

| 패턴 | 시그니처 예시 | 용도 | 핵심 Hook 조합 |
|------|-------------|------|---------------|
| useDebounced\<T\> | `T useDebounced<T>(T value, {Duration duration = const Duration(milliseconds: 400)})` | 검색 입력, 가용성 체크 디바운스 | `useState` + `useEffect` + `Timer` |
| usePaginationScroll | `ScrollController usePaginationScroll({required VoidCallback onFetchMore, double threshold = 200})` | 무한 스크롤 (threshold 도달 시 다음 페이지 fetch) | `useScrollController` + `useEffect` (listener) |
| useFocusState | `({FocusNode node, bool hasFocus}) useFocusState()` | 포커스 여부에 따른 UI 스타일 전환 | `useFocusNode` + `useState` + `useEffect` (listener) |
| useHandleAvailability | `({bool isAvailable, bool isChecking}) useHandleAvailability(String value, {required Future<bool> Function(String) checker, Duration debounce})` | 닉네임/핸들 등 비동기 중복 체크 (디바운스 + stale 방지) | `useState` + `useEffect` + debounce + stale 방지 |
| useStaggerController | `AnimationController useStaggerController({required Duration duration, bool autoForward = true})` | 화면 진입 시 순차 등장 애니메이션 | `useAnimationController` + 자동 `forward()` |
| useOverlayAnimation | `({AnimationController controller, Animation<double> fade, Animation<Offset> slide}) useOverlayAnimation({Duration duration, Curve curve})` | 오버레이/바텀시트/다이얼로그 등장 애니메이션 (fade + slide 조합) | `useAnimationController` + `useMemoized` (CurvedAnimation, Tween) |
| useCountdown | `({int remaining, VoidCallback reset}) useCountdown({required int totalSeconds, VoidCallback? onComplete})` | 인증번호 재전송 대기, 타이머 UI | `useState` + `useEffect` + `Timer` |

---

## @freezed Props 규칙

> 이 섹션은 `HAS_FREEZED = true`일 때만 적용한다.

### 적용 기준

| 위젯 유형 | Props | 이유 |
|-----------|-------|------|
| 디자인 시스템 위젯 (Named constructor variant 패턴) | **면제** | Named constructor variant가 추가될 수 있으므로 현행 유지 |
| 그 외 모든 위젯 | **적용** | `@freezed Props` 번들링 |

프로젝트에 디자인 시스템 위젯이 있고, Named constructor + `this._()` 리다이렉트 패턴을 사용하는 경우 해당 위젯은 Props 면제.

### Props 적용 패턴

```dart
@freezed
abstract class MyWidgetProps with _$MyWidgetProps {
  const factory MyWidgetProps({
    required String title,
    @Default(false) bool isActive,
    VoidCallback? onTap,
  }) = _MyWidgetProps;
}

class MyWidget extends HookWidget {
  const MyWidget(this._props, {super.key});
  final MyWidgetProps _props;

  @override
  Widget build(BuildContext context) {
    // _props.title, _props.isActive 등으로 접근
  }
}
```

---

## 전환 레퍼런스 패턴

### Before (StatefulWidget)

```dart
class MyWidget extends StatefulWidget {
  const MyWidget({required this.title, super.key});
  final String title;

  @override
  State<MyWidget> createState() => _MyWidgetState();
}

class _MyWidgetState extends State<MyWidget>
    with SingleTickerProviderStateMixin {
  late final AnimationController _ctrl;
  bool _isExpanded = false;

  @override
  void initState() {
    super.initState();
    _ctrl = AnimationController(vsync: this, duration: const Duration(milliseconds: 300));
  }

  @override
  void didUpdateWidget(MyWidget old) {
    super.didUpdateWidget(old);
    if (widget.title != old.title) _ctrl.forward(from: 0);
  }

  @override
  void dispose() {
    _ctrl.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: () => setState(() => _isExpanded = !_isExpanded),
      child: Text(widget.title),
    );
  }
}
```

### After (HookWidget)

```dart
class MyWidget extends HookWidget {
  const MyWidget({required this.title, super.key});
  final String title;

  @override
  Widget build(BuildContext context) {
    final ctrl = useAnimationController(duration: const Duration(milliseconds: 300));
    final isExpanded = useState(false);

    useEffect(() {
      ctrl.forward(from: 0);
      return null;
    }, [title]);

    return GestureDetector(
      onTap: () => isExpanded.value = !isExpanded.value,
      child: Text(title),
    );
  }
}
```

**핵심 변경:**
- `State` 클래스 제거 → `build`를 위젯 클래스로 이동
- `initState` + `dispose` → `useAnimationController()` (자동 dispose)
- `didUpdateWidget` → `useEffect([title])` (의존성 변경 시 실행)
- `setState` → `useState` (자동 리빌드)
- `widget.title` → `title` (직접 참조)
- `SingleTickerProviderStateMixin` → 불필요 (Hook이 내부 Ticker 제공)

## Templates

- `../../templates/widget-freezed-props.md` — freezed Props + Hook 위젯 골격 (Props 번들링 컨벤션 프로젝트용). plain 생성자 파라미터 프로젝트는 `flutter-widget` 기본 골격을 쓴다
