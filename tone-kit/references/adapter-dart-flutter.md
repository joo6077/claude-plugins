# dart-flutter 어댑터

코어 규칙을 Dart/Flutter 문법에 결속하는 슬롯 값·판정표·완료 게이트 grep. 스킬이 런타임에 Read 해서 판정에 쓰는 운영 문서다.

`tone-guide` 와 `tone-scaffold` 는 §1 슬롯 표에서 값을 읽고, `tone-audit` 은 §4 grep 10종을 실행한 뒤 같은 절의 판정표로 히트를 해석한다. 로드 조건은 `project-detection.md` 가 어댑터를 `dart-flutter` 로 확정한 프로젝트다.

## 목차

- [1. 어댑터 슬롯 값](#1-어댑터-슬롯-값)
- [2. 규칙표](#2-규칙표)
- [3. 영역별 판정](#3-영역별-판정)
- [4. 완료 게이트 grep 10종](#4-완료-게이트-grep-10종)
- [5. 수치 상수](#5-수치-상수)
- [6. 이 파일이 소유하지 않는 것](#6-이-파일이-소유하지-않는-것)
- [7. Gotchas](#7-gotchas)

## 1. 어댑터 슬롯 값

| 슬롯 | 값 |
|---|---|
| `comment_syntax` | 라인 `//` 가 기본값. `///` 는 dartdoc 전용이며 D-07 의 3개 용도에만. 블록 주석 `/* */` 미사용 |
| `doc_param_format` | `/// - [param]: 설명` — 파라미터 선언부에서 `[]` 링크 의무, 본문에서는 식별자 언급이 꼭 필요할 때만 |
| `doc_return_label` | `/// - 반환값: 설명`, void 는 `- 반환값: 없음`. **한국어 축 소유 — 표기 상수의 SSOT 는 `locale-korean.md` 다.** 이 파일은 라벨 문자열을 재정의하지 않는다 |
| `helper_prefix_forbidden` | `_build*` — 위젯을 반환하는 private 헬퍼 접두사. 접두사 금지만 이 파일 소관이고, 인라인·승격 판정식은 `core-structure.md` |
| `separator_pattern` | 고정 gap → `Row`/`Column` 의 `spacing:`. 리스트 구분자 → `ListView.separated` 의 `separatorBuilder`. `.expand().skip()` 체이닝과 수동 `SizedBox` 나열 금지 |
| `fallback_identifier_pattern` | `\b(effective\|resolved)[A-Z]` — 금지 접두사. 처리는 삭제가 아니라 도메인·역할명으로 개명 |
| `naming_suffix` | 위젯 `{widget_prefix}...Widget` · Props `...WidgetProps` · raw 상태 `...State` · 파생 뷰 `...ViewState` · 콜백 typedef `...Changed` / `...Tap`. 클래스 UpperCamelCase, 파일 snake_case |
| `event_vocabulary` | Flutter 공식 제스처 어휘 `on<제스처><단계>` (§3.11). 도메인 이벤트만 프로젝트가 명명 |
| `state_lib` | Riverpod(`@riverpod` Notifier + `select`) + flutter_hooks(`HookConsumerWidget` · `useState` · `useEffect`) + freezed state 클래스 |
| `codegen_cmd` | **프로젝트 감지값 — 상수가 아니다.** 버전 매니저 래퍼(`fvm` 등) 유무와 `dart`/`flutter` 선택이 프로젝트마다 다르므로 `project-detection.md` 의 감지 결과를 쓴다. 형태는 `<래퍼> <dart\|flutter> run build_runner build --delete-conflicting-outputs` |
| `audit_greps` | §4 의 10종. bash·zsh 양쪽에서 실행 검증 완료 |

## 2. 규칙표

| ID | 규칙 | 강도 |
|---|---|---|
| D-01 | null 은 `??` · `?.` · early return · 패턴 매칭으로 다룬다. 강제 `!` 는 경계부에만 | SHOULD |
| D-02 | nullable 삽입 문법은 위치가 정한다 — `?element` · `if case` · 삼항 · `switch` expression | SHOULD |
| D-03 | 고정 gap 은 `spacing:`, 리스트 구분자는 `separatorBuilder`. 수동 `SizedBox` 나열과 함수형 체이닝 금지 | 관측 컨벤션 |
| D-04 | 반복 렌더는 builder delegate 로. children 리스트를 즉시 채우지 않는다 | 관측 컨벤션 (성능 근거는 SHOULD 수준) |
| D-05 | leaf 토글은 상태를 자기가 소유한다 — `useState` + `useEffect` 동기화 | 관측 컨벤션 |
| D-06 | 파생 뷰 번들은 freezed state 클래스로. provider·위젯 표면에 익명 Record 금지 | 관측 컨벤션 |
| D-07 | `///` 는 계약이 있을 때만. 커버리지는 레이어가 아니라 로직 유무로 판정 | SHOULD |
| D-08 | 콜백 typedef 는 의미 원천 위젯이 같은 파일 top-level 에 소유한다 | 관측 컨벤션 |
| D-09 | expression body 가 기본값, 1회용 로컬 변수는 인라인 | SHOULD |
| D-10 | Notifier 비대화 방지 — status 별 헬퍼 다발을 단일 reducer 로 | 관측 컨벤션 |
| D-11 | bare `catch (e)` 는 의도된 컨벤션. `on Exception` 으로 좁히지 않는다 | 관측 컨벤션 |
| D-12 | 위젯을 반환하는 헬퍼보다 위젯 클래스를 선호한다 | SHOULD |
| D-13 | 큰 `build` 는 나눈다 | SHOULD |
| D-14 | 하위 위젯을 별도 파일에 둔다 | 관측 컨벤션 |
| D-15 | 제스처·입력 콜백은 프레임워크 공식 어휘를 쓴다. 자체 이벤트 어휘를 만들지 않는다 | SHOULD |

D-12~D-14 는 강도만 이 파일이 고정하고 **판정식은 `core-structure.md` 가 소유한다.** 공식 문구가 `prefer` 이고 공식 반례(`Builder` API, 위젯을 반환하는 함수 예시)가 존재하므로 D-12 를 MUST 로 올리지 않는다. D-13 은 공식 문서에 줄 수 임계값이 없다. D-14 의 공개 근거는 "다른 위젯으로 나눈다"까지이고 "별도 파일"은 이 코퍼스의 관측 컨벤션이다.

## 3. 영역별 판정

### 3.1 null 처리 관용구 (D-01 · D-02)

| 문법 위치 | 도구 |
|---|---|
| 컬렉션 리터럴 | `?element` — `children: [header, ?trailing]` (Dart 3.8 이상) |
| statement · collection element | `if (label case final text?) Text(text)` |
| expression (named parameter 등) | `style: custom ?? defaultStyle`. `if case` 는 문법이 성립하지 않는다 |
| 3분기 이상 | `switch` expression. 2분기는 삼항 또는 `if` |

강제 `!` 는 경계부(assert 직후, 파싱 직후처럼 non-null 이 이미 증명된 자리)에만. `if (x != null) f(x!)` 는 경계부가 아니다. Props 에서 항상 넘기는 필드는 nullable + `!` 조합이 아니라 `required` 로 선언한다.

### 3.2 리스트 빌딩 (D-03)

```dart
children: sections.map(_body).expand((w) => [divider, w]).skip(1).toList()  // 금지
children: sections.indexed.expand((r) { ... }).toList()                     // 금지
```

루프마다 동일하게 생성되는 위젯(divider 등)은 로컬 변수로 한 번 만들어 재사용한다.

### 3.3 lazy 렌더링 (D-04)

| 형태 | 판정 |
|---|---|
| `SingleChildScrollView` + `Column` | eager — 위반 |
| `ListView(children: [...])` | eager — 위반 |
| `for-in` · `.map().toList()` 로 children 채우기 | eager — 위반 |
| `shrinkWrap: true` | lazy 가 아니라 크기 맞춤. `.builder` 와 같이 써도 전체 높이 측정이 laziness 를 깬다 |
| `ListView.builder` · `.separated` · `SliverChildBuilderDelegate` | 준수 |
| 헤더 + 섹션 + 목록 혼합 | `CustomScrollView` 하나에 `SliverToBoxAdapter`(고정 영역) + builder sliver(목록) |

화면당 스크롤 컨테이너는 1개이고 중첩 `shrinkWrap` 리스트로 쌓지 않는다. 예외는 콘텐츠가 전부 화면에 들어와 스크롤이 실제로 불필요한 경우 하나뿐이며, **사람이 명시적으로 허락한 건에만 적용한다.** "다 보이니까 괜찮다"를 스스로 판정하지 않는다.

### 3.4 리빌드 범위와 상태 소유 (D-05)

```dart
final value = useState(props.value);
useEffect(() {
  if (value.value != props.value) value.value = props.value;
  return null;
}, [props.value]);
```

| 구분 | 대상 |
|---|---|
| 적용 | 체크박스 · 스위치 · 슬라이더 · 세그먼트 탭 등 자기 상태를 가진 leaf |
| 비적용 | 그룹형 라디오(형제 해제에 부모 rebuild 필수) · 표시 전용 위젯 · 외부 controller 입력 |

hook 은 `items.isEmpty` 같은 early return **위** 에 둔다. `useEffect` 는 post-frame 이라 부모 override 시 1프레임 stale 후 반영되며 이 지연은 수용된 trade-off 다. 정확성(override 반영)과 격리(perf)는 별개 축이라, 격리까지 원하면 상태를 provider 로 올리고 `ref.watch(provider.select(...))` 로 구독을 좁힌다.

### 3.5 freezed state vs 익명 Record (D-06)

| 자리 | 타입 |
|---|---|
| Notifier 의 raw 상태 (선택·입력) | freezed `{widget_prefix}XxxState` |
| derived provider 가 반환하는 파생 뷰 번들 | freezed `{widget_prefix}XxxViewState` |
| 위젯·provider 표면에 노출되지 않는 함수 내부 국소 튜플 | Record 허용 |

익명 Record 를 provider 반환 타입으로 쓰지 않는 이유는 셋이다. 타입명이 없어 의미와 재사용성이 약하고, 프로젝트 전역 freezed 컨벤션과 표기가 갈리며, Record 의 `==` 가 List 필드를 identity 로 비교해 freezed 의 깊은 컬렉션 비교와 rebuild 결과가 달라진다. 화면이 `ref.watch` 로 받는 로컬 변수명은 반환 타입과 무관하게 `state` 로 통일하고, notifier 를 함께 잡으면 `ref.read(...notifier)` 를 별도 변수로 분리한다.

### 3.6 시맨틱 typedef 소유권 (D-08)

| 항목 | 규칙 |
|---|---|
| 정의 위치 | 의미 원천 위젯의 같은 파일 top-level |
| 의미 원천 | 그 콜백이 제어하는 실제 UI 를 그리는 위젯 |
| forward 만 하는 상위 컴포지트·화면 | 새로 정의하지 않고 import |
| 프리미티브 위젯(switch/button/checkbox/radio/slider) | 자기 base typedef 를 계속 소유. 시맨틱 typedef 는 시그니처가 같아 base prop 으로 구조적 대입 |
| 공유 typedef 파일(`*_typedef.dart` 류) | 0개 |
| 같은 이름 typedef 를 co-import 되는 두 파일에 각각 정의 | 금지 |

한 아이템의 `onVisibleChanged` · `onFwUpdateChanged` · `onPairingChanged` 가 전부 같은 타입이면 타입에서 의미를 읽을 수 없다 — 그것이 위반 증상이다.

### 3.7 doc 커버리지 판정 (D-07)

| 대상 | 판정 |
|---|---|
| 로직이 있는 public 메서드 | 필수 |
| 자명하지 않은 private 메서드 | 필수 |
| 화면·뷰의 핸들러·리스너 헬퍼 | 필수 — "화면이니까"는 면제 사유가 아니다 |
| `build` | 면제 |
| 자명한 getter | 면제 |
| 필드 `///` | 비자명한 계약이 있을 때만. 이름을 한국어로 옮기기만 하는 doc 은 금지 |

커버리지는 레이어가 아니라 로직 유무로 판정한다. 본문은 한두 문장으로 끝내고, `정책:` · `참고:` · `주의:` 같은 본문 내 섹션 헤더와 알고리즘 단계 나열은 넣지 않는다. freezed 는 constructor parameter 의 `///` 를 property 와 class 레벨로 전파하므로 자명한 필드에 붙이면 생성 코드까지 오염된다. 라벨 표기와 문체는 `locale-korean.md` 소관이다.

### 3.8 expression body (D-09)

| 상황 | 형태 |
|---|---|
| 단일 expression 함수·콜백 | `=>` expression body |
| 분기가 있거나 statement 가 둘 이상 | block body |
| 한 곳에서만 쓰이는 로컬 변수 | 사용처에 인라인 (`final thumbnail = _thumbnail();` 후 1회 사용은 인라인) |
| 같은 참조에 연속 호출 | cascade `..` |
| extension | 짧고 명확한 도메인 어휘만. formatter·helper dumping ground 로 만들지 않는다 |

### 3.9 provider 비대화 방지 (D-10)

- `_notifyXxxStarted/Progress/Completed/Failed/Cancelled` 류 status 별 헬퍼 다발은 `_setXxxState({required status, double? percent, String? message, T? result})` 단일 reducer 로 통합한다. status 5종 × sub-state 3종이면 헬퍼가 15개로 늘어난다.
- `isIdle` · `isRunning` · `isCompleted` 같은 extension getter 를 sub-state 마다 양산하지 않는다. 정말 자주 쓰이는 1~2개만 남기고 나머지는 호출부에서 enum 을 직접 비교한다.
- 호출자가 쓰지 않는 저수준 메서드를 public 으로 노출하지 않는다. 통합 실행 흐름만 public 이고 그 안의 단계는 private 이거나 service 다.
- 파일이 1000줄을 넘으면 state 모델 · helper extension · Notifier 본체 세 파일로 분할한다. 다만 비대화의 실제 원인은 줄 수가 아니라 조합 폭발이다.
- 다이얼로그 progress 용으로 `ValueNotifier` 를 새로 만들어 `ValueListenableBuilder` 를 중첩하지 않는다. provider state 에 progress 를 넣고 `ref.listen` 으로 다이얼로그를 push/pop 한다.

### 3.10 bare catch 컨벤션 (D-11)

| 형태 | 판정 |
|---|---|
| `} catch (e) {` · `} catch (e, st) {` | 준수 — 의도된 컨벤션 |
| `} on SomeType catch (e) {` | 컨벤션 이탈 후보. 위반이 아니다 |

목적은 Dart 의 모든 throwable(`Object` 루트)을 전부 잡아 상태나 로그로 흡수하는 것이다. 좁히면 커버리지가 줄 뿐 늘지 않는다 — 비-`Exception` 객체를 던지는 경로가 있으면 좁힌 catch 가 그 throw 를 놓쳐 동작이 깨진다. **리뷰나 QA 가 bare catch 를 지적하면 무효 판정으로 처리한다.** 이 규칙은 코퍼스 실측에 근거하며 공개 1차 출처가 없으므로, 다른 코퍼스로 옮길 때는 G-07 을 먼저 돌려 같은 비율이 관측되는지 확인한다.

### 3.11 이벤트 콜백 어휘 (D-15)

Flutter 는 제스처 생명주기에 `on<제스처><단계>` 어휘를 이미 정의해 뒀다. 자체 어휘를 만들면 공식 어휘가 갈라 놓은 단계를 도로 합치게 된다.

**단계 축** — 프레임워크가 쓰는 순서다.

```text
Down  →  Start  →  Update / MoveUpdate  →  End / Up  →  Cancel
```

**제스처별 공식 콜백** (`gesture_detector.dart` 실측, Flutter 3.38.4 기준 **58개**)

세는 기준: 제스처 접두사(`Tap` · `SecondaryTap` · `TertiaryTap` · `DoubleTap` · `LongPress` · `SecondaryLongPress` · `TertiaryLongPress` · `VerticalDrag` · `HorizontalDrag` · `Pan` · `Scale` · `ForcePress`)를 가진 `on*` 고유 이름만 센다. 재현 명령은 아래와 같다.

```bash
grep -v '^\s*///' "$FLUTTER_SDK/packages/flutter/lib/src/widgets/gesture_detector.dart" \
  | grep -oE 'on(Tap|SecondaryTap|TertiaryTap|DoubleTap|LongPress|SecondaryLongPress|TertiaryLongPress|VerticalDrag|HorizontalDrag|Pan|Scale|ForcePress)[A-Za-z]*' \
  | sort -u | wc -l
```

**`grep -v '^\s*///'` 가 필수다.** 주석을 포함해 세면 59 가 나오는데, 그 차이 1건은 `onForcePress` 이고 실제 API 필드가 아니라 `RawGestureDetector` doc-comment 안의 예시 위젯 필드다. force press 계열의 실제 콜백은 `onForcePressStart` · `onForcePressPeak` · `onForcePressUpdate` · `onForcePressEnd` 4개다.

제스처 접두사가 없는 내부 recognizer 콜백 8종(`onDown` · `onStart` · `onUpdate` · `onEnd` · `onCancel` · `onPeak` · `onPointerDown` · `onPointerPanZoomStart`)은 제외한다. 주석까지 포함하면 67이 되는데 그것은 소비자가 이름을 따를 대상이 아니다.

| 제스처 | 콜백 |
|---|---|
| tap | `onTapDown` · `onTapMove` · `onTapUp` · `onTap` · `onTapCancel` |
| double tap | `onDoubleTapDown` · `onDoubleTap` · `onDoubleTapCancel` |
| long press | `onLongPressDown` · `onLongPressStart` · `onLongPressMoveUpdate` · `onLongPressUp` · `onLongPressEnd` · `onLongPress` · `onLongPressCancel` |
| pan | `onPanDown` · `onPanStart` · `onPanUpdate` · `onPanEnd` · `onPanCancel` |
| vertical drag | `onVerticalDragDown` · `onVerticalDragStart` · `onVerticalDragUpdate` · `onVerticalDragEnd` · `onVerticalDragCancel` |
| horizontal drag | `onHorizontalDrag…` (같은 단계 축) |
| scale | `onScaleStart` · `onScaleUpdate` · `onScaleEnd` |
| force press | `onForcePressStart` · `onForcePressPeak` · `onForcePressUpdate` · `onForcePressEnd` |

`Secondary` · `Tertiary` 변형도 같은 규칙으로 존재한다 (`onSecondaryTapDown` · `onTertiaryLongPressStart` 등).

**폼·선택 계열** — 위젯 API 가 쓰는 이름을 따른다: `onChanged` · `onSubmitted` · `onEditingComplete` · `onSelected` · `onPressed` · `onHover` · `onFocusChange`.

**판정**

```dart
// before — Press 가 tap 인지 long press 인지 이름에서 안 갈린다
void handlePressStart() { ... }
void handlePressEnd() { ... }

// after — 어느 제스처의 어느 단계인지 이름에 있다
void onTapDown(TapDownDetails details) { ... }
void onTapUp(TapUpDetails details) { ... }
```

typedef 이름도 같은 어휘를 따른다.

```dart
// before — 자체 접미사
typedef {widget_prefix}PressableTap = void Function();

// after — 공식 단계 어휘와 정렬
typedef {widget_prefix}PressableTapDown = void Function(TapDownDetails details);
```

**예외** — 공식 어휘에 대응이 없는 도메인 이벤트는 프로젝트가 이름 짓는다. `onPairingModeEntered` · `onLightStickMounted` 는 정당하다. 판정식은 "이 이벤트를 프레임워크가 이미 알고 있는가" 다.

**주의** — 같은 개념에 두 어휘를 섞지 마라. 코퍼스에 `…SelectTap` 과 `…Selected` 가 공존한 사례가 있다. 하나로 고정한다.

> **출처:** Flutter SDK `packages/flutter/lib/src/widgets/gesture_detector.dart` (3.38.4 실측 — 콜백 58개). 코어 원칙은 `core-naming.md` N-12.

## 4. 완료 게이트 grep 10종

`<src>` 는 `project-detection.md` 가 확정한 스코프 경로다. 10종 전부 bash·zsh 양쪽에서 실행 검증했고 각각 양성 케이스 1건 이상을 실제로 잡는 것을 확인했다.

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

| # | 잡는 것 | 히트 = 위반인가 | 판정 절차 |
|---|---|---|---|
| G-01 | `shrinkWrap: true` | 예 (D-04) | 즉시 위반. builder sliver 또는 `CustomScrollView` 로 전환. 예외는 사람이 명시적으로 허락한 건만 |
| G-02 | `SingleChildScrollView` | 예 (D-04) | eager 스크롤 컨테이너다. 반복 렌더를 감싸고 있으면 즉시 위반, 고정 콘텐츠 단독이어도 `CustomScrollView` + `SliverToBoxAdapter` 전환 대상 |
| G-03 | 위젯 반환 `_build*` 헬퍼 | **아니오 — 히트 수 ≠ 위반 수** | 접두사 금지는 확정이지만 인라인할지 위젯으로 승격할지는 `core-structure.md` 판정식이 정한다. 히트를 세어 그대로 보고하면 추출이 정당한 건까지 위반으로 집계된다 |
| G-04 | `effective`/`resolved` 접두 식별자 | 예 (`fallback_identifier_pattern`) | 삭제가 아니라 도메인·역할명으로 개명한다 |
| G-05 | `.expand(` | 후보 (D-03) | separator 삽입 체이닝(`.expand((w) => [div, w]).skip(1)`)이면 위반. 단순 평탄화 용법은 대상이 아니다 |
| G-06 | `ValueNotifier` · `ValueListenableBuilder` | 예 (D-10) | provider state + `ref.listen` 으로 이전한다 |
| G-07 | `} on <Type> catch` | **아니오 — 컨벤션 이탈 후보** | D-11 기준으로 bare catch 로 되돌릴지 판단한다. 위반 건수에 합산하지 않는다 |
| G-08 | `if (x != null)` | **과수집 — 걸러 낸 뒤 판정** | 히트 중 본문이 같은 식별자에 `!` 를 다시 쓰는 건만 위반이고 `if case final v?` 로 바꾼다. 경계부 `!`(assert 직후·파싱 직후)는 제외한다 |
| G-09 | 익명 Record 반환 함수 | 예 (D-06). **준수 상태에서 0건이 정상** | 0건이 아니면 freezed state 로 전환한다 |
| G-10 | `// -----` 구분선 주석 | 예 | 코어 주석 규칙 소관이며 어댑터는 grep 만 제공한다 |

## 5. 수치 상수

| 항목 | 값 |
|---|---|
| `?element` (null-aware element) 최소 버전 | Dart 3.8 |
| 화면당 스크롤 컨테이너 | 1개 |
| Notifier 파일 분할 하한 | 1000줄 |
| status 헬퍼 통합 대상 규모 | 5종 × 3 sub-state = 15개 → reducer 1개 |
| state extension getter 허용 개수 | 1~2개 |
| `useEffect` 동기화 지연 | 1프레임 (post-frame, 수용됨) |
| 공유 typedef 파일 허용 개수 | 0개 |
| bare `catch (e)` vs `on Exception` 관측 비율 | 27건 vs 3건 |

## 6. 이 파일이 소유하지 않는 것

| 사안 | 소유 |
|---|---|
| doc 라벨 표기(`- [param]:` · `- 반환값:` · `없음`)와 한국어 문체 | `locale-korean.md` |
| 추출 판단 일반 원칙 — 헬퍼 인라인 vs 위젯 승격, 파일 분리 임계, rebuild 격리 조건 | `core-structure.md` |
| `codegen_cmd` · `<src>` 스코프 경로 · `{widget_prefix}` · `{TokenClass}` 실제 값 | `project-detection.md` |
| 주석 톤·구분선·번역투 등 스택 무관 위반 카테고리 | 코어 안티패턴 카탈로그 |

## 7. Gotchas

- **리스트 빌딩 규칙은 개정 이력이 뒤집혀 있다.** 옛 절이 권장하던 `for-in` · `.indexed.map().toList()` children 채우기는 lazy 렌더링 절이 전면 금지했고 뒤의 것이 승이다. 살아남은 것은 `spacing:` 사용과 함수형 체이닝 금지뿐이다. 옛 예시를 다시 끌어오지 마라.
- **`useValueChanged` 인용도 폐기됐다.** 동기화 훅은 `useEffect` 하나다. 근거는 성능이 아니라 프로젝트 일관성이며 1프레임 stale 은 수용된 비용이다. 두 훅을 섞어 두면 동기화 패턴이 파일마다 갈린다.
- **`- 반환값: 없음` 을 노이즈로 보고 지우지 마라.** 지우면 "doc 이 없는 것"과 "반환값이 없는 것"을 구분할 수 없게 된다. 표기 규칙 자체는 `locale-korean.md` 가 소유한다.
- **강도를 임의로 올리지 마라.** D-12·D-13 은 SHOULD, D-14 는 관측 컨벤션이다. 공식 문구는 `prefer` 까지이고 줄 수 임계값은 없으며, "별도 파일"까지 요구하는 공개 근거도 없다. 이 셋을 MUST 로 적어 두면 감사 리포트가 근거 없는 위반을 양산한다.
- **위젯 클래스로 뺐다고 rebuild 가 끊기지 않는다.** 격리 조건(동일 인스턴스, `runtimeType` + `key`)은 `core-structure.md` 소관이다. 상태 소유를 안 고친 채 파일만 늘리면 프레임 비용은 그대로다.
- **다른 스택 어댑터를 이 파일에서 복제하지 마라.** Rust 나 TypeScript 어댑터는 그 스택에서 위반이 실제로 관측된 뒤에 만든다. 코어 원칙은 이미 스택 무관으로 있으므로 어댑터는 문법 관용구와 슬롯 값만 갖는다.
