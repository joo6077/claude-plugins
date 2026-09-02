---
title: 역할 기반 컴포넌트 네이밍 taxonomy
version: 0.2.0
last_updated: 2026-09-02
---

# 역할 기반 컴포넌트 네이밍 taxonomy

**이 문서가 잡는 것**

- 외형을 담은 이름 — `BlueRoundedBox` 처럼 색·모서리·크기가 박혀 시안이 바뀌면 거짓이 되는 이름
- 표 어휘를 세로 리스트에 쓴 이름, 임의 묶음에 붙인 `...Bar` — `DeviceRow`, `FilterBar`
- 역할이 아니라 계산 과정을 담은 이름 — `effectiveGradient` 같은 fallback 접두사
- 프레임워크가 이미 이름을 정해 둔 이벤트에 새로 만든 어휘 — `handlePressStart`

```dart
// before
class {widget_prefix}BlueDeviceRowWidget extends StatelessWidget { ... }
// after
class {widget_prefix}DeviceItemWidget extends StatelessWidget { ... }
```

이름 하나에 두 가지가 걸렸다 — 외형(`Blue`)과 표 어휘(`Row`). 세로 리스트 한 장의 기본값은 `Item` 이다.

접미사 taxonomy 는 **합성 규칙**(6개 디자인 시스템의 어휘를 대조해 만든 규칙 — 어느 한 시스템이 표준으로 문서화한 것이 아니다)이다. 각 원칙 끝의 `MUST` / `SHOULD` / `관측 컨벤션` 3등급과 그 판정 근거는 [근거 등급](#근거-등급) 절에 있다.

**합성이 필요한 자리와 그렇지 않은 자리는 다르다.** 컴포넌트 접미사(`Item` / `Tile` / `Cell`)는 단일 권위가 없어서 여섯 시스템을 대조해 합성했다. 반면 **이벤트 콜백 어휘는 프레임워크가 이미 정해 뒀다** — 합성할 자리가 아니다. 정해진 자리에서는 그것을 따르고, 비어 있는 자리만 taxonomy 가 메운다. 원칙 0 이 나머지 원칙보다 앞에 있는 이유다.

---

## 결정표 — 그래서 뭘 어떻게 지으라는 건가

**0단계 — 프레임워크가 이미 이름을 정했는가?** 정했으면 그 이름을 그대로 쓰고 이 표를 건너뛴다 (원칙 0). 아래 표는 프레임워크가 어휘를 정해 두지 **않은** 자리에서만 돈다.

| 이 요소는 | 이름 | 예 |
|---|---|---|
| 탭이 그 요소의 존재 이유다 | `...Button` | `{widget_prefix}RetryButtonWidget` |
| 세로 리스트 한 장 (형태 미특정) | `...Item` — 기본값 | `{widget_prefix}DeviceItemWidget` |
| leading/trailing 을 가진 고정 높이 행 | `...Tile` | `{widget_prefix}NotificationTileWidget` |
| 표의 한 행 / 교차 칸 | `...Row` / `...Cell` | `{widget_prefix}OrderTableRowWidget` |
| 하나의 객체·개념을 담는 독립 표면 | `...Card` (Carbon 계열은 `Tile`) | `{widget_prefix}ProfileCardWidget` |
| 화면 최상단 앱 컨테이너 | `...AppBar` | `{widget_prefix}HomeAppBarWidget` |
| 현재 작업과 관련된 액션 묶음 | `...Toolbar` | `{widget_prefix}EditorToolbarWidget` |
| 콘텐츠·섹션·카드의 제목부 | `...Header` | `{widget_prefix}DetailHeaderWidget` |
| 의미 구획 | `...Section` | `{widget_prefix}SummarySectionWidget` |
| 보조 작업·설정면 | `...Panel` | `{widget_prefix}SettingsPanelWidget` |
| 역할이 아직 확정 안 된 저수준 래퍼 | `...Container` | `{widget_prefix}ScrollContainerWidget` |
| 위 어디에도 구체어가 없다 | `...Bar` — 마지막 수단 | `{widget_prefix}ProgressBarWidget` |

역할이 겹치면 `실제 인터랙션 > 컬렉션 요소 > 화면 구획 > 상단 영역` 순으로 끊는다 (원칙 6).

**라벨 읽는 법.** 각 원칙 제목의 `[코어]` · `[어댑터:dart-flutter]` 는 **축**(규칙이 어디에 묶이는지 — 스택·언어·프로젝트 세 갈래. `[코어]` 는 스택 무관, `[어댑터:...]` 는 특정 스택 문법에 묶인다)이고, 원칙 끝의 `관측 컨벤션`(공개 출처 없이 프로젝트 실측만 있는 규칙 — 준수 강도가 낮다는 뜻이 아니다)은 강도다. **어댑터 슬롯**(코어 규칙을 특정 스택 문법에 결속하는 자리)은 현재 `dart-flutter` 하나뿐이라 아래 코드 예시도 전부 Dart 다.

---

## 어휘 대조표 (2026-08-28 확인)

| 시스템 | 화면 상단 | 리스트의 한 행 | 탭 가능한 그룹 표면 |
|---|---|---|---|
| Material Design 3 | `Top app bar` / `App bars` | `List item` (정의문 확인 실패) | `Card` (정의문 확인 실패) |
| Apple HIG | `Toolbars` (`navigation-bars` 가 여기로 리다이렉트) | `Lists and tables` (행 용어 확인 실패) | 독립 `Cards` 페이지 확인 실패 |
| MUI | `AppBar` + `Toolbar` 둘 다 export | `ListItem` / `TableRow` / `TableCell` | `Card` / `CardActionArea` |
| Fluent 2 | `Toolbar` (`Header`/`AppBar` 없음) | `List item` | `Card` |
| Ant Design | `Header` / `Layout.Header` | `row` 와 `list item` 혼용 | `Card` |
| IBM Carbon | `UI shell header` / `Header` | `List item` | `Tile` (core 에 card 패턴 없음) |

> **출처:** [M3 components](https://m3.material.io/components) · [Apple HIG components](https://developer.apple.com/design/human-interface-guidelines/components) · [MUI AppBar](https://mui.com/material-ui/react-app-bar/) · [Fluent 2 Web React](https://fluent2.microsoft.design/components/web/react) · [Ant Design components](https://ant.design/components/overview/) · [Carbon components](https://carbondesignsystem.com/components/overview/components/)

Material 은 `Top app bar`, Apple 은 `Toolbar`, Ant·Carbon 은 `Header`, Fluent 는 `Toolbar`, MUI 는 `AppBar` 와 `Toolbar` 를 동시에 둔다. Carbon 은 표면에 `Card` 대신 `Tile` 을 쓴다. **불일치가 규칙이다.** 그래서 프로젝트는 자기 taxonomy 를 한 번 정하고 그것을 SSOT 로 삼아야 한다.

M3 와 Apple HIG 페이지는 본문이 JS 로만 렌더링돼 정의문을 직접 인용할 수 없다. 두 시스템은 **어휘 존재 확인용으로만** 인용하고 원문 인용은 붙이지 마라.

---

## 원칙

### 0. 프레임워크가 이미 정한 어휘를 따른다 `[코어][어댑터:dart-flutter]`

이벤트·상태 어휘를 새로 만들지 않는다. 프레임워크가 이름을 정해 둔 개념에는 그 이름을 쓴다.

```text
프레임워크 공식 어휘  >  프로젝트 관례  >  새로 만든 말
```

```dart
// before — 자체 어휘. 어느 제스처의 어느 단계인지 이름에서 안 갈린다
void handlePressStart() { ... }
void handlePressEnd() { ... }
// after — 제스처와 단계가 이름에 있다
void onTapDown(TapDownDetails details) { ... }   // 또는 onLongPressStart
void onTapUp(TapUpDetails details) { ... }       // 또는 onLongPressEnd
```

```dart
// before — 같은 개념을 두 어휘로 부른다
typedef {widget_prefix}ServerSelectTap = void Function(Server server);
void handleServerSelectTap(Server server) { ... }
// after — 공식 어휘 하나로 고정
typedef {widget_prefix}ServerSelected = void Function(Server server);
void onServerSelected(Server server) { ... }
```

Flutter SDK `packages/flutter/lib/src/widgets/gesture_detector.dart` (3.38.4) 에서 콜백 58개를 확인했다. 단계 축은 `Down → Start → Update/MoveUpdate → End/Up → Cancel` 이고 제스처마다 일관되게 붙는다.

| 제스처 | 콜백 |
|---|---|
| tap | `onTapDown` · `onTapMove` · `onTapUp` · `onTap` · `onTapCancel` |
| double tap | `onDoubleTapDown` · `onDoubleTap` · `onDoubleTapCancel` |
| long press | `onLongPressDown` · `onLongPressStart` · `onLongPressMoveUpdate` · `onLongPressUp` · `onLongPressEnd` · `onLongPress` · `onLongPressCancel` |
| pan | `onPanDown` · `onPanStart` · `onPanUpdate` · `onPanEnd` · `onPanCancel` |
| drag | `onVerticalDrag…` · `onHorizontalDrag…` (같은 단계 축) |
| scale | `onScaleStart` · `onScaleUpdate` · `onScaleEnd` |
| force press | `onForcePressStart` · `onForcePressPeak` · `onForcePressUpdate` · `onForcePressEnd` |

`Secondary` · `Tertiary` 변형도 같은 규칙으로 존재한다. 폼·선택 계열은 `onChanged` · `onSubmitted` · `onEditingComplete` · `onSelected` · `onPressed` · `onHover` · `onFocusChange` 다.

코퍼스 실측에서 `handlePressStart` 7건 · `handlePressEnd` 8건이 나왔고, 같은 개념에 `…SelectTap` 과 `…Selected` 가 공존했다. `Press` 하나로는 tap 인지 long press 인지 이름에서 안 갈린다 — 프레임워크는 갈라 놨는데 프로젝트가 도로 합친 것이다. 자동완성·검색·문서가 전부 공식 이름 기준으로 움직이므로 자체 어휘는 그 경로에서 빠진다.

**예외.** 공식 어휘에 대응이 없는 **도메인 이벤트**는 프로젝트가 이름 짓는다. `onPairingModeEntered` · `onLightStickMounted` · `onLibraryDownloadCancel` 는 정당하다. 판정식은 "이 이벤트를 프레임워크가 이미 알고 있는가" 다.

이 원칙은 아래 접미사 taxonomy 보다 **앞선다.** taxonomy 는 프레임워크가 어휘를 정해 두지 않은 자리를 메우는 합성 규칙이고, 공식 어휘가 있으면 그게 먼저다. 로케일 축의 "공식 API 이름은 번역하지 않는다"(`korean-technical-writing.md`)와 같은 원리다 — 주석에서는 공식 이름을 지키면서 코드에서 자체 어휘를 만드는 것은 앞뒤가 맞지 않는다.

공식 문서가 "소비자 코드도 이 이름을 쓰라" 고 명시하지는 않는다. 근거는 어휘가 실재한다는 사실이지 지침 문장이 아니므로 `MUST` 로 올리지 마라.

**강도:** SHOULD

> **출처:** Flutter SDK `packages/flutter/lib/src/widgets/gesture_detector.dart` (3.38.4 실측 — 콜백 58개) · 프로젝트 실측 (`handlePressStart` 7건 · `handlePressEnd` 8건, `…SelectTap`/`…Selected` 혼재). 코어 규칙 ID 는 `core-naming.md` N-12, 어댑터 판정은 `adapter-dart-flutter.md` D-15 · §3.11 (슬롯 `event_vocabulary`)

### 1. 이름은 외형이 아니라 역할을 담는다 `[코어]`

색·모서리·크기를 이름에서 빼고, 사용자가 그것으로 무엇을 하거나 이해하는지를 넣는다.

```dart
// before — 시안이 바뀌면 거짓이 되는 이름
class {widget_prefix}BlueRoundedBoxWidget extends StatelessWidget { ... }
class {widget_prefix}Gray12CardWidget extends StatelessWidget { ... }
// after
class {widget_prefix}ProfileCardWidget extends StatelessWidget { ... }
class {widget_prefix}NoticeCardWidget extends StatelessWidget { ... }
```

```dart
// before — 프로퍼티가 동사구, 메서드가 파라미터를 서술
Duration get computeAnimationDuration => ...;
void updateStateWithNewIndex(int index) { ... }
// after
Duration get animationDuration => ...;
void selectIndex(int index) { ... }
```

판단 기준은 "사용자가 이것으로 무엇을 하거나 이해하는가" 이지 "이것이 어떻게 생겼는가" 가 아니다. 색·모서리·크기는 시안이 바뀌면 따라 바뀌므로 이름에 들어가면 이름이 거짓이 된다. Dart 공식 스타일 가이드는 같은 방향을 문법 층위에서 규정한다: 비-boolean 프로퍼티는 명사구, 부수효과가 있는 메서드는 명령형 동사구, 메서드 이름에 파라미터를 서술하지 않는다.

**강도:** SHOULD

> **출처:** [Effective Dart: Style](https://dart.dev/effective-dart/style)

### 2. 레이아웃 모양어를 컴포넌트 이름에 쓰지 않는다 `[코어]`

`Row` · `Bar` · `Box` 는 레이아웃 용어다. 한정 용법(진짜 표의 행, 확립된 바 종류)에만 허용한다.

```dart
// before
class {widget_prefix}DeviceRowWidget extends StatelessWidget { ... }   // 세로 목록 한 장
class {widget_prefix}FilterBarWidget extends StatelessWidget { ... }   // 임의 컨트롤 묶음
class {widget_prefix}ProfileBoxWidget extends StatelessWidget { ... }  // 역할이 이미 확정됨
// after
class {widget_prefix}DeviceItemWidget extends StatelessWidget { ... }
class {widget_prefix}FilterHeaderWidget extends StatelessWidget { ... }
class {widget_prefix}ProfileCardWidget extends StatelessWidget { ... }
```

```dart
// 허용 — 진짜 표의 행, 확립된 바 종류
class {widget_prefix}OrderTableRowWidget extends StatelessWidget { ... }
class {widget_prefix}HomeAppBarWidget extends StatelessWidget { ... }
class {widget_prefix}UploadProgressBarWidget extends StatelessWidget { ... }
```

세로 리스트의 한 장을 `...Row` 로 부르면 그것이 표의 행인지 세로 목록의 항목인지 이름만으로 구분되지 않는다. 나중에 진짜 표가 생기면 두 이름이 같은 어휘를 놓고 충돌한다.

**강도:** 관측 컨벤션 / 합성

> **출처:** 합성 규칙 — 위 어휘 대조표의 6개 시스템 중 어느 곳도 이 금지를 문서화하지 않는다 (2026-08-28 확인)

### 3. 컬렉션 요소: `Item` / `Tile` / `Cell` / `Row` `[코어]`

**세로 리스트 요소에 `Row`/`Cell` 을 쓰지 마라. 둘은 표 전용이다.** 세로 리스트 한 장은 `Item`, 단순한 행이면 `Tile`, 독립 표면이면 `Card`.

```dart
// before — 세로 목록 한 장을 표 어휘로
class {widget_prefix}DeviceRowWidget extends StatelessWidget { ... }
class {widget_prefix}NotificationCellWidget extends StatelessWidget { ... }
// after
class {widget_prefix}DeviceItemWidget extends StatelessWidget { ... }        // 형태 미특정 기본값
class {widget_prefix}NotificationTileWidget extends StatelessWidget { ... }  // leading/trailing 고정 높이
```

```dart
// 표 안이라면 원래 어휘가 맞다 — 여기서 Item 으로 바꾸면 반대 방향 오류다
class {widget_prefix}OrderTableRowWidget extends StatelessWidget { ... }
class {widget_prefix}OrderTableCellWidget extends StatelessWidget { ... }
```

| 접미사 | 언제 |
|---|---|
| `Item` | UI 형태를 특정하지 않는 일반 데이터 단위. 세로 리스트 한 장의 기본값 |
| `Tile` | leading/trailing 을 가진 고정 높이 리스트 행 |
| `Cell` | 표·그리드의 교차 칸 |
| `Row` | 표의 한 행. 수평 구조가 의미상 본질일 때만 |

각 시스템의 실제 어휘는 이 구분을 부분적으로만 지지한다. MUI 는 `ListItem`/`TableRow`/`TableCell` 로 갈라 쓰고, Fluent 와 Carbon 은 `List item` 으로 통일하며, Ant 는 `row` 와 `list item` 을 혼용한다.

**강도:** 관측 컨벤션 / 합성

> **출처:** [MUI ListItem API](https://mui.com/material-ui/api/list-item/) · [Fluent 2 List](https://fluent2.microsoft.design/components/web/react/core/list/usage) — "A list is a collection of like items" · [Carbon List](https://carbondesignsystem.com/components/list/usage/) — "Represents an individual entry within a list"

### 4. 상단·구획: `AppBar` / `Toolbar` / `Header` / `Bar` `[코어]`

**임의의 컨트롤 묶음이나 콘텐츠 상단 구획에 `Bar` 를 쓰지 마라 — `Header` 다.** 묶음이 현재 작업의 액션이면 `Toolbar`, 화면 최상단 앱 컨테이너면 `AppBar` 다.

```dart
// before
class {widget_prefix}FilterBarWidget extends StatelessWidget { ... }   // 콘텐츠 상단 구획
class {widget_prefix}EditorBarWidget extends StatelessWidget { ... }   // 현재 작업 액션 묶음
class {widget_prefix}HomeHeaderWidget extends StatelessWidget { ... }  // 실제로는 화면 최상단 앱 컨테이너
// after
class {widget_prefix}FilterHeaderWidget extends StatelessWidget { ... }
class {widget_prefix}EditorToolbarWidget extends StatelessWidget { ... }
class {widget_prefix}HomeAppBarWidget extends StatelessWidget { ... }
```

| 접미사 | 언제 |
|---|---|
| `AppBar` | 화면 최상단 앱 컨테이너 (제목·내비게이션·주요 액션) |
| `Toolbar` | 현재 작업과 관련된 액션 묶음 |
| `Header` | 콘텐츠·섹션·카드의 제목부 또는 시작부 |
| `Bar` | 구체어가 없을 때만 쓰는 포괄 fallback |

Carbon 의 `Header` 는 최상위 내비게이션이고 Ant 의 `Header` 는 레이아웃 상단이다. 같은 단어가 시스템마다 다른 층위를 가리킨다. 프로젝트가 하나를 골라 고정해야 하는 이유다.

**강도:** 관측 컨벤션 / 합성

> **출처:** [MUI AppBar](https://mui.com/material-ui/react-app-bar/) — "The App Bar displays information and actions relating to the current screen." · [Fluent 2 Toolbar](https://fluent2.microsoft.design/components/web/react/core/toolbar/usage) — "A toolbar gives access to frequently used actions" · [Ant Design Layout](https://ant.design/components/layout) — "Header: The top layout" · [Carbon UI shell header](https://carbondesignsystem.com/components/UI-shell-header/usage/) — "Header: The highest level of navigation."

### 5. 표면·구획: `Section` / `Panel` / `Container` / `Card` `[코어]`

역할이 확정된 표면에 `Container` · `Box` · `Wrapper` · `View` 를 쓰지 않는다.

```dart
// before — 의미가 약한 래퍼 어휘
class {widget_prefix}SettingsContainerWidget extends StatelessWidget { ... }
class {widget_prefix}NoticeWrapperWidget extends StatelessWidget { ... }
class {widget_prefix}SummaryViewWidget extends StatelessWidget { ... }
// after
class {widget_prefix}SettingsPanelWidget extends StatelessWidget { ... }   // 보조 작업·설정면
class {widget_prefix}NoticeCardWidget extends StatelessWidget { ... }      // 독립 표면
class {widget_prefix}SummarySectionWidget extends StatelessWidget { ... }  // 의미 구획
```

`Section` 은 의미 구획, `Panel` 은 보조 작업·설정면, `Container` 는 저수준 레이아웃 래퍼, `Card` 는 하나의 객체나 개념을 담는 독립 표면이다. `Container` · `Box` · `Wrapper` · `View` 는 저수준 유틸이거나 역할이 아직 확정되지 않은 내부 위젯에만 쓴다. Carbon 은 이 자리에 `Card` 가 아니라 `Tile` 을 쓰고 "Tiles versus cards" 를 따로 비교한다 — 어휘가 시스템에 종속된다는 증거다.

**강도:** 관측 컨벤션 / 합성

> **출처:** [Carbon Tile](https://carbondesignsystem.com/components/tile/usage/) · [Fluent 2 Card](https://fluent2.microsoft.design/components/web/react/core/card/usage) — "A card is a container" · [Ant Design Card](https://ant.design/components/card) — "A container for displaying information."

### 6. 역할이 겹치면 우선순위로 끊는다 `[코어]`

```text
실제 인터랙션  >  컬렉션 요소  >  화면 구획  >  상단 영역
```

```dart
// before — 목록을 보여주는 것이 본질인데 탭이 된다는 이유로 Button
class {widget_prefix}DeviceButtonWidget extends StatelessWidget { ... }
// after — 탭은 부가, 존재 이유는 목록 한 장
class {widget_prefix}DeviceItemWidget extends StatelessWidget { ... }
// 탭이 존재 이유일 때만 Button 이 이긴다
class {widget_prefix}RetryButtonWidget extends StatelessWidget { ... }
```

탭하면 `Button`, 리스트 한 칸이면 `Item`/`Tile`, 구획이면 `Section`/`Card`, 상단이면 `Header`/`Toolbar`. 리스트 안에 있으면서 탭도 되는 요소는 "탭이 그 요소의 존재 이유인가" 로 끊는다. 목록을 보여주는 것이 본질이고 탭이 부가면 `Item` 이다.

**강도:** 관측 컨벤션 / 합성

> **출처:** 합성 규칙 — 6개 시스템 중 우선순위를 문서화한 곳 없음 (2026-08-28 확인)

### 7. fallback 접두사를 이름으로 쓰지 않는다 `[코어]`

`effective` · `resolved` 접두사를 도메인·역할어로 바꾼다.

```dart
// before — ?? 가 이미 표현한 fallback 을 이름에 중복
final effectiveGradient = props.gradient ?? defaultGradient;
final resolvedChildren = props.children ?? const [];
final resolvedBgColor = props.background ?? {TokenClass}.surfaceDisabled;
// after
final toolbarGradient = props.gradient ?? defaultGradient;
final visibleChildren = props.children ?? const [];
final disabledBackground = props.background ?? {TokenClass}.surfaceDisabled;
```

접두사는 역할이 아니라 계산 과정을 드러낸다. 기본값 연산자가 이미 그 계산을 말하고 있으므로 이름이 같은 말을 두 번 한다. 이 접두사가 LLM 생성 코드에 통계적으로 과대표집된다는 **공개 근거는 없다** — 논문 각주를 붙이지 마라.

**강도:** 관측 컨벤션 (실측 9건 / 4파일)

> **출처:** 프로젝트 실측 (57파일 스캔 중 9건 / 4파일). 공개 통계는 확인 실패 — 상세는 `ai-code-stylometry.md` 원칙 5

### 8. 한 글자 이름과 무역할 파일명을 피한다 `[코어]`

축약 대신 온전한 단어를, 파일명에는 역할어 대신 도메인을 쓴다.

```dart
// before
void onTapDown(TapDownDetails e) {
  final p = widget.props;
  final s = ref.watch(deviceProvider);
}
// after
void onTapDown(TapDownDetails event) {
  final props = widget.props;
  final state = ref.watch(deviceProvider);
}
```

```text
// before — 무엇이 들어 있는지 알 수 없어 무한히 자란다
lib/features/device/utils.dart
lib/features/device/helper.dart
lib/features/device/common_widget.dart
// after
lib/features/device/device_pairing_formatter.dart
lib/features/device/device_status_mapper.dart
lib/features/device/device_item_widget.dart
```

`p` · `s` · `e` 는 선언부에서 세 글자를 아끼고 사용부 전체에서 추론 비용을 만든다. `utils` · `helper` · `common` 은 배제 기준이 없어서 새 함수가 갈 곳이 없을 때마다 여기로 모인다.

**강도:** SHOULD

> **출처:** [Effective Dart: Style](https://dart.dev/effective-dart/style)

### 9. 컴포넌트 이름과 그 데이터 타입 이름을 정렬한다 `[코어][어댑터:dart-flutter]`

컴포넌트가 `...Item` 이면 그것이 받는 상태도 `...Item` 이다.

```dart
// before — 같은 것을 두 이름으로 부른다
class {widget_prefix}DeviceItemWidget extends StatelessWidget {
  final {widget_prefix}DeviceRowViewState state;
}
// after
class {widget_prefix}DeviceItemWidget extends StatelessWidget {
  final {widget_prefix}DeviceItemViewState state;
}
```

접미사가 어긋나면 검색이 한쪽만 잡고, 다음 사람이 두 이름이 같은 개념인지 매번 확인해야 한다. 클래스만 리네임하지 말고 `snake_case` 파일명까지 함께 옮긴다.

**강도:** 관측 컨벤션

> **출처:** 프로젝트 실측 — 컴포넌트/상태 타입 접미사 불일치가 리네이밍 작업의 반복 원인

### 10. prefix 와 suffix 는 프로젝트 파라미터다 `[코어]`

조립 형식만 킷이 정하고 값은 프로젝트가 소유한다.

```dart
// before — 한 프로젝트 안에서 조립 형식이 파일마다 다르다
class DeviceItemWidget extends StatelessWidget { ... }        // 접두사 없음
class {widget_prefix}ItemDeviceWidget extends StatelessWidget { ... }  // 역할이 도메인 앞
class {widget_prefix}DeviceItem extends StatelessWidget { ... }        // 접미사 없음
// after — 조립 형식: {widget_prefix} + 도메인/대상 + 역할 + {widget_suffix}
class {widget_prefix}DeviceItem{widget_suffix} extends StatelessWidget { ... }
// 파일: device_item_widget.dart — 클래스 UpperCamelCase · 파일 snake_case
```

```dart
// 접두사·접미사를 안 쓰기로 한 프로젝트도 유효하다. 전 파일이 같기만 하면 된다
class DeviceItem extends StatelessWidget { ... }
// 파일: device_item.dart
```

`{widget_prefix}`(스코프 구분자)와 `{widget_suffix}`(예: `Widget`)는 **프로젝트마다 다르며 킷이 값을 정하지 않는다.** 감지 규칙은 `project-detection` 이 소유한다. 이 문서가 강제하는 것은 접미사의 존재가 아니라 **taxonomy 의 일관성** 이다.

**강도:** 관측 컨벤션

> **출처:** [Effective Dart: Style](https://dart.dev/effective-dart/style) (casing 규약만 해당)

---

## 수치 기준

| 항목 | 값 | 출처 |
|------|-----|------|
| 조사한 디자인 시스템 | 6 | 2026-08-28 확인 |
| 상단 영역 어휘가 일치하는 시스템 수 | 0 (6개가 4가지 용어로 갈림) | 어휘 대조표 |
| 커스텀 컴포넌트 명명 지침을 발행하는 시스템 | 0 | 확인 실패 |
| 정의문을 인용 가능한 시스템 | 4 (M3·Apple HIG 는 JS 렌더링) | 어휘 대조표 |
| fallback 접두사 실측 | 9건 / 4파일 (57파일 스캔) | 프로젝트 실측 |
| 컬렉션 요소 접미사 후보 | 5 (`Item`/`Tile`/`Cell`/`Row`/`Card`) | 합성 taxonomy |
| Flutter 제스처 콜백 | 58개 (`gesture_detector.dart` 3.38.4) | 프레임워크 실측 |
| 자체 이벤트 어휘 실측 | 15건 (`handlePressStart` 7 · `handlePressEnd` 8) | 프로젝트 실측 |

---

## 안티패턴

| 안티패턴 | 문제 |
|----------|------|
| 세로 리스트 요소를 `...Row` / `...Cell` 로 명명 | 표의 행·칸과 구분되지 않는다. 나중에 진짜 표가 생기면 이름이 충돌한다 |
| 임의 컨트롤 묶음에 `...Bar` | `Bar` 는 구체어가 없을 때의 fallback 이다. 콘텐츠 상단 구획은 `Header` 다 |
| 역할이 확정됐는데 `...Box` / `...View` / `...Container` / `...Wrapper` | 의미가 없는 이름은 검색도 안 되고 다음 사람이 역할을 다시 추론해야 한다 |
| 외형(색·모양·둥글기) 기반 이름 | 시안이 바뀌면 이름이 거짓이 된다. 리네임 비용이 시안 변경마다 발생한다 |
| 컴포넌트 접미사와 데이터 타입 접미사 불일치 | 같은 개념을 두 이름으로 부르게 되고, 검색이 한쪽만 잡는다 |
| 디자인 시스템을 taxonomy 의 **권위** 로 인용 | 6개 시스템이 서로 어긋난다. 인용은 어휘 원천까지만 유효하다 |
| M3·Apple HIG 페이지 문구를 인용 | 본문이 JS 로만 렌더링돼 인용문을 검증할 수 없다. 어휘 존재 확인용으로만 써라 |
| 프레임워크가 이미 정의한 이벤트에 자체 어휘 신설 (`handlePressStart`) | 공식 어휘가 갈라 놓은 단계를 도로 합친다. tap 인지 long press 인지 이름에서 안 갈리고, 자동완성·검색이 공식 이름 기준이라 자체 어휘는 그 경로에서 빠진다 |
| 같은 개념에 공식 어휘와 자체 어휘를 섞어 씀 (`…SelectTap` ↔ `…Selected`) | 한 개념이 두 이름을 갖는다. 어느 쪽이 정본인지 호출부에서 판단할 수 없다 |
| `{widget_prefix}` 를 킷이 고정 | prefix 는 프로젝트 소유 파라미터다. 킷이 값을 정하면 다른 프로젝트에서 전부 오탐이 된다 |

---

## 근거 등급

2026-08-28 조사 결과, Material Design 3 · Apple HIG · MUI · Fluent 2 · Ant Design · IBM Carbon 어느 곳도 `Item`/`Tile`/`Cell`/`Row` 구분이나 `AppBar`/`Toolbar`/`Header`/`Bar` 구분을 **공통 taxonomy 로 문서화하지 않는다.** 각 시스템은 자기 플랫폼 어휘를 쓸 뿐이고 서로 어긋난다.

또한 여섯 시스템 중 어느 곳도 **소비자 앱의 커스텀 컴포넌트 명명 지침**("역할로 이름 지어라")을 발행하지 않는다 (확인 실패). MUI 에 API·prop·CSS 클래스 명명 가이드가 있으나 그것은 라이브러리 내부 규약이다.

따라서 이 문서의 접미사 규칙은 전부 `관측 컨벤션 / 합성` 이며, 디자인 시스템은 **어휘 원천** 으로만 인용한다. 권위로 인용하지 마라. 원칙 1 과 8 만 공식 스타일 가이드에 걸려 `SHOULD` 다.

원칙 0 도 `SHOULD` 지만 근거의 종류가 다르다. 접미사 규칙에 없는 것이 여기에는 있다 — **어휘가 프레임워크 API 표면에 실재한다.** 컴포넌트 접미사에는 단일 권위가 없어 합성이 불가피했지만, 이벤트 콜백에는 `gesture_detector.dart` 라는 대조 가능한 원본이 있다. 다만 그 원본도 "소비자 코드가 이 이름을 쓰라" 고 지시하지는 않으므로 `MUST` 가 아니다. 두 경우를 섞어 "우리 규칙에 근거가 있다" 고 뭉뚱그리지 마라.

---

## Gotchas

- **taxonomy 를 "업계 표준" 이라고 소개하지 마라** — 조사 결과는 정반대다. 6개 시스템이 상단 영역 하나를 4가지 용어로 부른다. 표준이라고 소개하면 첫 반박에 규칙 전체의 신뢰가 무너진다. "합성이고, 그래서 프로젝트가 하나를 골라 고정한다" 가 정확한 서술이다.
- **`Header` 는 시스템마다 층위가 다르다** — Carbon 에서는 최상위 내비게이션이고 Ant 에서는 레이아웃 상단이다. 외부 문서를 근거로 팀을 설득하려다 오히려 반대 사례를 들려주게 된다. 근거는 "우리 프로젝트 일관성" 이지 외부 권위가 아니다.
- **`Card` 가 없는 시스템이 있다** — Carbon core 에는 card 패턴이 없고 `Tile` 이 그 자리를 대신한다. `Card` 를 보편 어휘로 가정하면 Carbon 기반 프로젝트에서 규칙이 헛돈다.
- **접미사를 바꾸면 파일명·데이터 타입·테스트 경로가 같이 움직인다** — 클래스만 리네임하면 `snake_case` 파일명과 대응 상태 타입이 뒤처진다. 원칙 9와 10을 한 번에 적용하라.
- **우선순위 규칙은 "탭 가능성" 이 아니라 "탭이 존재 이유인가" 로 끊는다** — 리스트 항목은 대부분 탭이 되지만 그렇다고 `Button` 이 아니다. 이 구분을 놓치면 목록 요소가 전부 `...Button` 이 된다.
- **원칙 0 을 `MUST` 로 올리지 마라** — 근거는 어휘가 실재한다는 사실이지 "이 이름을 쓰라" 는 지침 문장이 아니다. `MUST` 로 적어 두면 감사 리포트가 근거 없는 위반을 양산한다.
- **모든 이벤트를 공식 어휘로 바꾸려 들지 마라** — 도메인 이벤트는 원칙 0 의 대상이 아니다. `onPairingModeEntered` 를 억지로 제스처 어휘에 맞추면 오히려 이름이 거짓이 된다. 판정식은 "이 이벤트를 프레임워크가 이미 알고 있는가" 하나다.
- **fallback 접두사 규칙에 논문을 붙이고 싶어진다** — AI 코드 탐지 문헌이 identifier 신호를 다루긴 하지만 접두사별 통계는 없다. 각주를 붙이는 순간 검증 불가능한 주장이 된다. 실측 건수만 쓴다.
