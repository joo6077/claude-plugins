---
name: flutter-widget
description: >
  프로젝트 컨벤션에 맞는 새 위젯을 생성한다.
  디자인 시스템 감지, variant 패턴, size enum, 적절한 base class 적용.
  커스텀 위젯, UI 컴포넌트를 만들 때 사용.
  "위젯 만들어줘", "컴포넌트 생성", "widget 추가", "new widget",
  "UI 컴포넌트", "custom widget", "버튼 만들어줘" 같은 요청 시 트리거.
argument-hint: "<feature>_<name>"
user-invocable: true
---

## Gotchas

- 탭 가능한 커스텀 위젯은 반드시 `Pressable`로 래핑 — GestureDetector, InkWell 직접 사용 금지
- 색상은 `context.colors.xxx` (시맨틱 토큰) 사용 — `Palette.xxx` 직접 참조하면 다크 모드에서 깨짐
- 위젯 variant는 private 기본 생성자 `const Widget._({...})` + named constructor 패턴 — 기본 생성자에 variant 로직 넣지 마라
- 수치값은 `AppRadii.sm`, `AppPadding.h20` 등 디자인 토큰 사용 — `BorderRadius.circular(8)` 같은 하드코딩 금지
- Flutter 3.38+에서 `MaterialState`가 `WidgetState`로 마이그레이션됨 — `MaterialStateProperty` 대신 `WidgetStateProperty` 사용. `dart fix --apply`로 자동 변환 가능
- 헬퍼 메서드(`_buildHeader()`)가 아닌 private Widget 클래스로 추출해라 — Flutter 공식 AI rules 권장 패턴. 합성(composition)이 메서드 분리보다 성능·재사용성 모두 우수
- Flutter 3.41에서 `FontWeight`가 variable font의 weight axis도 제어함 — `FontVariation('wght', 700)` 별도 설정이 불필요해짐. 기존 코드에 중복 설정이 있으면 제거 필요
- 외부 라이브러리 위젯을 래핑할 때는 라이브러리 기본값을 반드시 명시적으로 오버라이드하라 — 기본 생성자(`LibWidget()`)로 넘기면 라이브러리 내부 기본값이 적용되어 원하지 않는 동작이 나온다. 예: html_editor_enhanced의 `defaultToolbarButtons`는 InsertButtons를 포함한 전체 버튼이 기본값 — 원하는 버튼 목록만 `HtmlToolbarOptions(defaultToolbarButtons: [...])` 로 명시 전달해야 한다
- **Flutter 3.41 신규 위젯** — `RepeatingAnimationBuilder` (반복 애니메이션 간편 생성), `DeviceOrientationBuilder` (기기 방향에 반응하는 위젯), `CarouselView.builder` (lazy 캐러셀), `Navigator.popUntilWithResult` (결과 전달 + 다중 pop). 새 위젯 생성 시 이 빌트인 위젯이 요구사항을 충족하는지 먼저 확인하라 — 이미 제공되는 기능을 재구현하면 유지보수 부담만 늘어난다 (출처: <https://blog.flutter.dev/whats-new-in-flutter-3-41-302ec140e632>)
- **content-sized Flutter views (3.41)** — 하이브리드 앱에서 Flutter view 가 콘텐츠 크기에 맞게 자동 리사이즈됨. 고정 치수 요구가 제거됐으므로, 하이브리드 앱 내 위젯을 만들 때 `SizedBox` 로 강제 크기를 지정하지 않아도 된다 (출처: <https://docs.flutter.dev/release/release-notes/release-notes-3.41.0>)
- **Primitive Substitution Gate (E2 · `HAS_DS = true` 일 때만)** — `references/primitive-substitution-gate.md` §게이트 대상 에 열거된 **의미 있는 Flutter 기본 UI 위젯**을 새 코드에 넣기 전에, 같은 의미의 프로젝트 컴포넌트를 먼저 검색하고 **대체 후보 표**를 응답에 채워서 남긴다. 대상 목록 · 검색 명령 · 표 서식 · 면제 목록은 전부 그 파일이 SSOT 다 — **여기서 목록을 다시 세지 마라** (두 곳에서 관리하면 한쪽만 갱신되어 어긋난다). 생성 스킬이므로 §quick 검색(대상 1 종 1 회)만 하면 된다. 실측 REJECT `RE-02` (2026-08-12): "구분선이 Flutter 기본 `Divider` 사용, 기존 `IFDivider` 컴포넌트 미재사용". SSOT 의 **면제 목록(layout primitive)** 을 반드시 함께 읽어라 — 이 게이트를 "기본 위젯 전면 금지" 로 확대 해석하는 것이 대표적 오적용이다
- **Enumerate-before-Act (low-freedom 영역 · skill-design-guide §5.5)** — 새 위젯 제작이나 기존 위젯 리팩터링 전에 (a) 프로젝트의 기존 디자인 토큰(컬러 · 타이포 · 스페이싱 · 라디우스)을 **Grep 으로 전수 나열** 하고, (b) 같은 카테고리의 기존 위젯을 `grep -r "extends.*Widget" lib/shared/ lib/features/*/presentation/widgets/` 로 전수 파악하고, (c) 재사용 후보가 있으면 "새로 만들까 / 기존을 확장할까" 선택지를 **1..N 인덱스** 로 명시해 사용자 또는 자기 자신에게 지목시킨다. 근사치 추정 · "아마 이 토큰이 맞을 것" 은 3+ iteration 재작업의 주범 (insights-report #2 Wrong approach & false dichotomies 대응)
- **신규 enum / 카탈로그 / 공용 헬퍼는 만들기 전에 기존 것을 Grep 하라 (`/insights` 2026-07-27 Friction #3)** — 화면 목록·모드·타입을 나열하는 enum 이나 카탈로그 위젯을 새로 만들기 전에 `grep -rn "^enum \|enum .* {" lib/` 로 기존 enum 을 전수 확인한다. 같은 항목 집합을 정의하는 enum 이 이미 있으면 **그것을 재사용**하고, 새로 만들어야 하는 이유를 한 줄로 근거화한다. 실측 사례: 동일한 14 개 화면을 정의하는 `UserModeScreen` enum 이 이미 있는데 `_SkinScreen` 중복 카탈로그를 생성 → 전면 되돌림
- **기존 위젯 수정이 기본값이다 — 교체는 사전 승인 사항 (`/insights` 2026-07-27 Friction #1 · digest `preserve-original-colors`)** — 시각 변경 요청을 받으면 편집 전에 세 줄을 남긴다: (1) 대상 위젯을 `파일:라인` 으로 지목, (2) **유지할 속성**(색상 체계 · 크기 · 모션 · 레이아웃) 을 열거, (3) 기존 위젯을 Flutter 기본 위젯(`CircularProgressIndicator` 등)이나 다른 컴포넌트로 **교체**하려면 승인을 먼저 받는다. 실측 사례: "play 아이콘이 회전했으면 좋겠다" 에 Material `CircularProgressIndicator` 를 새로 만들어 전면 재작업 / "보더만" 요청에 배경까지 어둡게 변경. 요청하지 않은 색상·배경 변경은 그 자체로 회귀다. 절차 전문: `references/visual-evidence-protocol.md` Step 0
- **TextStyle / 레거시 타이포 토큰 마이그레이션 전수 체크 (insights #1 대응)** — 프로젝트에 타이포 토큰 마이그레이션 규칙(예: `bodyMSemiBold` → 신규 `bodyM + FontWeight.w600`)이 있으면, 위젯 수정 전에 `grep -rn "bodyMSemiBold\|<마이그레이션 대상 토큰>" lib/` 로 대상 줄을 **전수 나열 후 체크리스트** 로 만들고, 완료 선언 전에 같은 Grep 을 재실행해 0 건 확인. "몇 개 고쳤다" 같은 서술로 끝내면 나머지 잔존분이 남아 반복 지적을 유발 (`/insights` 30d Friction Point #1 "legacy bodyMSemiBold 미처리" 실제 사례 기반)
- **Stack vs Column 선택 근거 명시 (insights #2 대응)** — 자식 위젯이 수직·수평 나열 외 **겹치거나 Positioned 로 절대 배치해야 할 때만** `Stack` 을 사용. 단순 나열에 Stack 을 쓰면 레이아웃 디버깅 비용이 커지고 피그마 대조에서 드리프트 발생. 의사결정 트리: (1) 자식이 겹치지 않고 동일 axis 면 Row/Column, (2) `Expanded`/`Flexible` 로 비율 조정이 필요하면 Flex 계열, (3) 하나가 다른 자식 위에 오버레이(배지, 플로팅 버튼, Gradient 오버레이)되어야 할 때만 Stack. Stack 사용 시 선택 근거를 **코드 주석 한 줄** 로 기록(`// Stack: 좋아요 배지가 카드 우측 상단에 오버레이`)
- **현재 stable 은 Flutter 3.47.0** — 릴리스 인덱스 stable 목록 최상단이 3.47.0 이다. 아래 3.41 / 3.44 항목은 그 버전에서 도입된 변경을 정리한 것이지 "최신" 이 아니다. 3.47 은 Android 의존성 매트릭스를 **Java 17 · KGP 2.4.0 · AGP 9.1.0 · Gradle 9.3.1** 로 제시한다 — Android 빌드 설정을 건드리는 위젯 작업이면 이 매트릭스를 먼저 확인하라 (출처: <https://docs.flutter.dev/release/release-notes>, <https://flutter.dev/blog/whats-new-in-flutter-3-47>)
- **Flutter 3.44 위젯 변경** — 새 위젯을 만들기 전에 빌트인이 요구를 충족하는지 먼저 확인하라. 신규: `CarouselView` 무한 스크롤 + `CarouselView.onItemChanged` + `CarouselController.leadingIndex`, `AnimatedCrossFade.onEnd`, `Hero` 애니메이션 curve 커스터마이징, `RoundedSuperellipseInputBorder`, `Overlay.alwaysSizeToContent`, `ScrollCacheExtent`(PageView 등 캐시 범위). Deprecated: `ReorderableListView.onReorder` → `onReorderStart` / `onReorderEnd`. 제거: `ExtendSelectionByPageIntent` (출처: <https://docs.flutter.dev/release/release-notes/release-notes-3.44.0>, <https://docs.flutter.dev/release/release-notes>)
- **Riverpod 3.4.1 (2026-07-27 실측 최신, pub.dev)** — `(Async)Notifier` 에는 `mounted` 프로퍼티가 **없다**. async gap 후 `ref` 재사용 시 `context.mounted` 로 가드하거나 `CancelToken` · `Completer` 로 작업 자체를 취소하라. `ref.state` · `ref.listenSelf` · `ref.future` 는 Notifier 내부에서는 `state` / `listenSelf` / `future` (prefix 없음) 로 접근한다. 3.2.0 부터 `family.overrideWith` 가 deprecated (→ `family.overrideWith2`, 4.0 에서 rename 예정), 3.4.0 부터 `SyncProviderTransformerMixin` deprecated (출처: <https://pub.dev/packages/flutter_riverpod>, <https://pub.dev/packages/flutter_riverpod/changelog>)

프로젝트의 스타일 가이드와 컨벤션에 맞는 새 위젯을 생성한다.

## 0. 프로젝트 감지

`references/project-detection.md`의 절차를 실행하여 프로젝트 환경을 파악한다.
이후 단계에서 감지 결과(`$FLUTTER`, `$DART`, `$PACKAGE`, `HAS_RIVERPOD`, `HAS_HOOKS`, `HAS_DS` 등)를 사용한다.

## Input

`$ARGUMENTS`: widget name in snake_case (e.g., `home_carousel`, `settings_theme_selector`)

feature는 첫 번째 세그먼트에서 추론한다 (e.g., `home` from `home_carousel`).
prefix가 `lib/features/` 내 기존 feature와 일치하면 해당 feature에 배치한다.
일치하지 않으면 shared 위젯 경로에 배치한다.

## Steps

### 1. 배치 경로 결정

- **Feature widget**:
  - `ARCH = clean` → `lib/features/<feature>/presentation/widgets/$ARGUMENTS.dart`
  - `ARCH = feature_first` → `lib/features/<feature>/widgets/$ARGUMENTS.dart`
  - `ARCH = flat` → `lib/src/<feature>/widgets/$ARGUMENTS.dart` 또는 프로젝트 관습
- **Shared widget** → 프로젝트의 공유 위젯 디렉토리에 배치:
  - 기존 shared 위젯 디렉토리를 감지한다 (e.g., `lib/shared/presentation/widgets/`, `lib/core/widgets/`, `lib/widgets/`)
  - shared 디렉토리에 하위 분류 폴더가 있으면 (e.g., `buttons/`, `cards/`, `inputs/`) 적절한 폴더에 배치
  - 분류가 모호하면 사용자에게 확인

shared 디렉토리의 일반적인 분류 구조 (프로젝트에 이미 있는 분류를 우선 따른다):

| 카테고리 | 위젯 유형 |
|---------|----------|
| `animated/` | 애니메이션 유틸 (StaggeredList, AnimatedClip 등) |
| `buttons/` | 버튼, Pressable 래퍼 등 터치 인터랙션 |
| `cards/` | 컨테이너, 카드, 정보 박스 |
| `chips/` | Chip, Tag, SegmentedControl |
| `dialogs/` | Dialog, Alert |
| `dropdowns/` | Dropdown, PopupMenu |
| `empty/` | EmptyState, Placeholder |
| `feedback/` | Toast, Snackbar, Shimmer, SuccessFeedback |
| `inputs/` | TextField, Input, SearchBar |
| `lists/` | ListItem, ListTile |
| `navigation/` | AppBar, BottomNav, Scaffold |
| `pickers/` | DatePicker, TimePicker, 커스텀 Picker |
| `progress/` | ProgressBar, CircularProgress, Stepper |
| `sheets/` | BottomSheet, ModalSheet |
| `toggles/` | Toggle, Switch, Checkbox |

프로젝트에 위 분류가 없으면 기존 디렉토리 구조를 따른다.
위 경로 중 어느 것도 존재하지 않으면 `lib/widgets/`를 기본 shared 위젯 경로로 생성한다.
분류가 모호하면 사용자에게 확인한다.

### 2. 기존 패턴 분석

같은 디렉토리의 기존 위젯을 읽어 로컬 패턴을 파악한다:
- Widget base class 관습
- Import 패턴
- 디자인 토큰 사용 방식
- Variant/size 패턴
- 탭 인터랙션 래핑 방식

### 3. Widget Base Class 결정

| 조건 | Base Class |
|------|-----------|
| `HAS_HOOKS` | `HookWidget` (provider 접근 불필요 시) |
| `HAS_HOOKS` + provider 접근 필요 | `HookConsumerWidget` |
| `HAS_RIVERPOD` + provider 접근 필요 | `ConsumerWidget` |
| 기본 | `StatelessWidget` |

기존 코드에서 다른 base class를 주로 사용하고 있으면 그것을 따른다.

### 4. 위젯 생성

#### 기본 템플릿

```dart
import 'package:flutter/material.dart';

class <WidgetName> extends <BaseClass> {
  const <WidgetName>({
    super.key,
    // required parameters
  });

  @override
  Widget build(BuildContext context) {
    return /* widget tree */;
  }
}
```

#### Variant 패턴 (여러 스타일이 필요한 경우)

프로젝트에서 variant 패턴을 사용하고 있으면 동일한 방식을 적용한다.

private 기본 생성자 `._()` 패턴의 이유: 외부에서 variant를 직접 지정하지 못하게 강제하여 named constructor만 사용하도록 한다. 이를 통해 variant 추가/삭제 시 컴파일 타임에 사용처를 추적할 수 있고, 각 variant의 기본값을 named constructor에서 캡슐화한다.

```dart
enum <WidgetName>Variant { primary, secondary, outline }

class <WidgetName> extends StatelessWidget {
  const <WidgetName>._({
    super.key,
    required this.variant,
    required this.child,
    this.onTap,
  });

  /// Primary variant
  const <WidgetName>.primary({Key? key, required Widget child, VoidCallback? onTap})
    : this._(key: key, variant: <WidgetName>Variant.primary, child: child, onTap: onTap);

  /// Secondary variant
  const <WidgetName>.secondary({Key? key, required Widget child, VoidCallback? onTap})
    : this._(key: key, variant: <WidgetName>Variant.secondary, child: child, onTap: onTap);

  final <WidgetName>Variant variant;
  final Widget child;
  final VoidCallback? onTap;

  @override
  Widget build(BuildContext context) {
    final (bgColor, fgColor) = switch (variant) {
      <WidgetName>Variant.primary => (Colors.blue, Colors.white),
      <WidgetName>Variant.secondary => (Colors.grey, Colors.black),
      <WidgetName>Variant.outline => (Colors.transparent, Colors.blue),
    };
    // ...
  }
}
```

#### Variant 토큰 분리

variant별 색상, 사이즈, 스타일 값이 복잡해지면 위젯 클래스 내부가 아닌 별도 토큰 클래스로 분리한다:

```dart
abstract final class MyWidgetTokens {
  static const primaryBg = Color(0xFF...);
  static const secondaryBg = Color(0xFF...);
  // HAS_DS면 프로젝트 토큰 참조, 아니면 직접 정의
}
```

프로젝트에 이미 이 패턴이 있으면 동일한 방식을 따른다 (예: `abstract final class`, `class _Tokens` 등).

#### Size 패턴 (여러 크기가 필요한 경우)

```dart
enum <WidgetName>Size { small, medium, large }

// size enum으로 padding/font/height 연동
final (padding, fontSize, height) = switch (size) {
  <WidgetName>Size.small => (EdgeInsets.symmetric(horizontal: 8, vertical: 4), 12.0, 28.0),
  <WidgetName>Size.medium => (EdgeInsets.symmetric(horizontal: 12, vertical: 8), 14.0, 36.0),
  <WidgetName>Size.large => (EdgeInsets.symmetric(horizontal: 16, vertical: 12), 16.0, 44.0),
};
```

### 5. 디자인 시스템 규칙 적용 (HAS_DS = true인 경우만)

`HAS_DS`가 감지되면 프로젝트의 디자인 시스템 토큰을 사용한다:

- **색상**: 프로젝트의 semantic token 패턴을 사용 (e.g., `context.colors.xxx`, `Theme.of(context).colorScheme.xxx`). 하드코딩 색상 금지 — 테마 전환(다크/라이트) 시 적용되지 않는다
- **Border radius**: 프로젝트에 radius 토큰이 있으면 사용. 하드코딩 값 지양
- **Padding/Spacing**: 프로젝트에 spacing 토큰/프리셋이 있으면 사용
- **Opacity**: 프로젝트에 opacity 토큰이 있으면 사용. 색상에 투명도를 적용할 때 `color.withOpacity(0.5)` 대신 `color.withValues(alpha: 0.5)`를 사용한다 — `withOpacity`는 deprecated

`HAS_DS`가 false이면 이 섹션을 스킵하고 일반 Flutter 스타일로 생성한다.

### 6. 탭 인터랙션 처리

프로젝트에 커스텀 Pressable/Tappable 위젯이 있는지 감지한다:
- 있으면: 해당 위젯으로 래핑 (e.g., `Pressable`, `Tappable`). `GestureDetector`, `InkWell` 직접 사용 지양
- 없으면: `GestureDetector` 또는 `InkWell` 사용

`onTap == null`이면 비활성화 처리가 자동인지 수동인지 기존 코드에서 확인한다.

Pressable/Tappable 위젯이 감지되면 해당 위젯의 소스를 읽어 지원하는 옵션을 파악한다:

**흔한 Pressable 옵션 패턴:**
- gradient 배경 위 highlight → `foregroundHighlight: true` (background highlight는 gradient 아래에 그려져 안 보임)
- 원형 위젯의 highlight → `highlightShape: BoxShape.circle`
- 누르면 아래로 이동하는 효과 → `pressOffset` (예: `Offset(0, 4)`)
- press 상태에 따른 커스텀 시각 효과 → press progress 값 접근 (예: `PressableData.of(context)?.pressProgress`)
- 자체 Semantics가 있는 위젯(toggle 등) → Pressable의 기본 Semantics 비활성 (스크린 리더 중복 방지)
- `onTap == null` → 자동 비활성화 처리(Opacity 감소 + IgnorePointer + Semantics disabled) — 별도 비활성 로직 불필요

### 7. Widgetbook/Storybook 등록

프로젝트에 위젯 카탈로그 도구가 있는지 감지한다:
- `widgetbook/` 디렉토리 → Widgetbook use case 등록
- `storybook/` 또는 `.storybook/` → Storybook entry 등록
- 없으면 → 스킵

**Overlay 위젯 등록 시 주의:**
`Overlay.of(context).insert()` 또는 `showGeneralDialog`를 사용하는 위젯은 Widgetbook use case에서 자체 `MaterialApp` 래핑이 필요하다 — OverlayEntry 컨텍스트에 Theme/Token이 없으면 null 크래시 발생.
`showModalBottomSheet` 기반은 Flutter가 caller Theme을 캡처하므로 래핑 불필요.

## Code Rules

- **MUST** `package:$PACKAGE/...` import만 사용 (상대경로 금지). 순서: `dart:` → `package:` (그룹 사이 빈 줄, 알파벳순)
- **MUST** 클래스명은 `$ARGUMENTS`의 PascalCase (e.g., `home_carousel` → `HomeCarousel`)
- **MUST NOT** 파일명과 클래스명에 `_widget` 접미사를 붙이지 않는다 — Flutter에서는 모든 것이 위젯이므로 중복
- **MUST** 최신 Dart 문법(patterns, records, switch expressions) 적극 활용
- **MUST** nullable slot은 조건부 렌더링: `if (slot != null) ...[slot!]`
- **MUST** overflow 가능성이 있는 콘텐츠는 스크롤 컨테이너로 래핑
- **MUST** 기존 코드에서 관찰된 패턴과 일관성을 유지한다
- **MUST NOT** 프로젝트에 없는 패키지를 import하는 코드를 생성하지 않는다

## Rules

- **MUST** 기존 위젯 코드를 읽어 프로젝트 패턴을 일치시킨다
- **MUST** `HAS_DS`가 false이면 디자인 시스템 규칙을 스킵한다
- **MUST** Pressable/Tappable 등 커스텀 인터랙션 위젯은 프로젝트에 있을 때만 사용한다
- **MUST** Widgetbook/Storybook 등록은 프로젝트에 해당 도구가 있을 때만 수행한다
- **MUST** variant/size 패턴은 프로젝트의 기존 패턴을 따른다. 기존 패턴이 없으면 위 기본 템플릿 사용

## Post-Creation: Widget Inspector

생성 완료 후 `widget-inspector` 에이전트를 quick 모드로 실행하여 변경 파일 주변의 재사용 가능한 위젯 패턴을 스캔한다. 추출 후보가 있으면 리포팅하고, 없으면 조용히 넘어간다.

## Post-Creation: Visual Evidence (완료 선언 전 필수)

`references/visual-evidence-protocol.md` 를 실행하고 **Visual Evidence Block 을 응답에 채워서 보고**한다.
시각 검증 채널이 없거나 캡처가 실패하면 `[미검증]` 마커와 사유를 남기고 **부분 완료**로 보고한다 —
"정상 렌더링됩니다" 같은 서술로 완료를 대체하지 않는다. 빈 캡처는 PASS 증거가 아니라 검증 실패 신호다.

## Related Skills

- Feature 디렉토리가 없으면 → `flutter-feature`
- Screen/Page 생성 → `flutter-screen`
- Provider 생성 → `flutter-provider`
- 위젯 추출 → `flutter-extract`
- codegen 실행 → `flutter-run codegen`
