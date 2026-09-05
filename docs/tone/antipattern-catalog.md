---
title: AI 톤 안티패턴 카탈로그 A~J
version: 0.1.0
last_updated: 2026-09-02
---

# AI 톤 안티패턴 카탈로그 A~J

**이 문서가 잡는 것**

- 코드가 이미 말한 것을 다시 말하는 주석 — 이름 번역, 템플릿 마커, 구분선, 프레임워크 기본 설명
- 계산 과정을 이름에 박은 변수 — `effectiveGradient`, `resolvedChildren`
- 정리하다가 **함께 지워지면 안 되는 주석** — 함정·제약·실패 모드를 적은 줄 (H 카테고리)

```dart
// before — F 구분선 · B 마커 · C 번역투 doc · A 이름 번역 · E 접두사가 한 화면에 다 있다
// ------------------------------------------------------------
//위젯 구현부
// ------------------------------------------------------------
/// 눌림 시작 상태를 처리합니다.
void handlePressStart() {
  final effectiveGradient = props.gradient ?? {TokenClass}.defaultGradient; // 기본 그라디언트
  // 안 끄면 M3 tonal overlay 가 이 색 위에 덧칠돼 더 밝아진다
  _tint = Colors.transparent;
}

// after — 5종은 지웠고 마지막 한 줄은 남았다. 그 줄이 H 다
void handlePressStart() {
  final toolbarGradient = props.gradient ?? {TokenClass}.defaultGradient;
  // 안 끄면 M3 tonal overlay 가 이 색 위에 덧칠돼 더 밝아진다
  _tint = Colors.transparent;
}
```

`tone-guide` 와 `tone-campaign` 이 위반을 판정할 때 참조하는 카탈로그 SSOT. 10개 카테고리 중 **H 는 위반이 아니라 보존 대상** 이며, 나머지 9개를 지울 때 함께 지워지는 것을 막는 방어 카테고리다.

규칙마다 강도(`MUST` / `SHOULD` / `관측 컨벤션`)와 축(그 규칙이 스택 무관 코어인지 특정 스택 전용인지 표시하는 라벨)을 각 절 맨 뒤에 붙인다. 정의는 [강도와 축](#강도와-축) 절에 있다. `관측 컨벤션`(공개 출처 없이 프로젝트 실측만 있는 규칙 — 준수 강도가 낮다는 뜻이 아니다)은 E 하나뿐이다.

---

## 카테고리 한눈에

| 카테고리 | 한 줄 결론 | 처리 |
|---|---|---|
| A 이름 번역 주석 | 이름이 이미 담은 의미를 되풀이하는 주석은 지운다 | 삭제 또는 개명 |
| B 템플릿 마커 | 파일마다 같은 자리에 박히는 고정 라벨은 지운다 | 삭제 |
| C 메서드명 반복 doc | 메서드 이름을 한국어 문장으로 푼 doc 은 지운다 | 삭제 |
| D 프레임워크 기본 설명 | 공식 문서 첫 문단에 있는 내용은 코드 옆에 옮겨 적지 않는다 | 삭제 |
| E 접두사 fallback 변수명 | `effective*` · `resolved*` 는 역할명으로 바꾼다 | 개명 |
| F 구분선 블록 | `// ---` 배너는 빈 줄과 이름으로 대체한다 | 삭제 |
| G 자명 구조 라벨 | 바로 아래 코드가 말하는 라벨은 이름으로 흡수한 뒤 지운다 | 흡수 |
| **H 좋은 주석** | **위반이 아니다. 코드로 복원 불가능한 정보는 남긴다** | **보존** |
| I 과도한 빌더 분할 | `_build*` 호출 체인은 인라인하거나 위젯으로 뺀다 | 재구성 |
| J 중복 구현 | 공통 위젯이 있는데 저수준 조합을 다시 조립하지 않는다 | 수렴 |

---

## 원칙

### A — 이름 번역 주석

**식별자 이름과 타입이 이미 담고 있는 의미를 한국어로 되풀이하는 주석은 지운다.**

```dart
// before
const {widget_prefix}SliderWidget({
  String? text,   // 버튼 텍스트
  bool isChecked, // 체크 여부
  double v,       // 최소 눈금 값
  Color bg,       // 0x66 = alpha 40%
});

// after — 되풀이는 삭제, 약한 이름은 개명, 값에서 못 읽는 메타는 유지
const {widget_prefix}SliderWidget({
  String? text,
  bool isChecked,
  double minTick,
  Color bg,       // 0x66 = alpha 40%
});
```

**왜** — 주석을 지워도 정보 손실이 0이다. `v` 처럼 이름이 약해서 주석이 필요했던 자리는 주석이 아니라 이름을 고쳐야 하며, 주석만 지우고 이름을 그대로 두면 원래보다 나빠진다.

**예외** — hex 값의 alpha 퍼센트처럼 값에서 사람이 곧바로 읽어낼 수 없는 메타 정보는 A 가 아니다.

**판정 신호** — 선언 뒤에 붙은 한국어 인라인 주석:

```text
grep -rnE '^[[:space:]]*[A-Za-z_].*[a-zA-Z0-9_?],[[:space:]]*//[[:space:]]*[가-힣]' --include='*.dart' .
```

강도 `MUST` 삭제 · 축 `[코어]` `[한국어]`. Effective Dart 의 등급은 `AVOID` 이고 이 카탈로그는 이를 `MUST` 로 승격했다. 승격 사유는 실측 상위 빈도(48파일 전역, 약 85건 — 템플릿 마커 약 90건 다음)와 제거 시 손실 0 이다.

> **출처:** [Effective Dart — documentation](https://dart.dev/effective-dart/documentation) · 프로젝트 실측 (57 파일 / 약 85건, 2026-04~06)

### B — 템플릿 마커

**파일마다 같은 위치에 기계적으로 반복되는 고정 라벨은 지운다.**

```dart
// before
class {widget_prefix}DeviceRowWidget extends StatelessWidget {
  //상태
  final {widget_prefix}DeviceRowWidgetProps props;

  //위젯 구현부
  @override
  Widget build(BuildContext context) => Row(children: [...]);
}

// after
class {widget_prefix}DeviceRowWidget extends StatelessWidget {
  final {widget_prefix}DeviceRowWidgetProps props;

  @override
  Widget build(BuildContext context) => Row(children: [...]);
}
```

**왜** — 그 파일이 무엇인지는 클래스 선언이 이미 말한다. 파일 구조를 알려주는 역할이 필요하면 그것은 파일 분할이나 이름으로 해결할 문제이지 마커로 해결할 문제가 아니다.

**예외** — 없다.

**판정 신호** — 동일 주석 줄의 코퍼스 전역 빈도. 생성 파일을 반드시 제외하고, 빈도 상위에 뜨는 짧은 라벨을 후보로 본다:

```text
grep -rhoE '^[[:space:]]*//[[:space:]]*[^[:space:]/*].*$' --include='*.dart' \
  --exclude='*.g.dart' --exclude='*.freezed.dart' . \
  | sed 's/^[[:space:]]*//' | sort | uniq -c | sort -rn | head -20
```

강도 `MUST` 삭제 · 축 `[코어]`

> **출처:** [Google Engineering Practices — what to look for in a code review](https://google.github.io/eng-practices/review/reviewer/looking-for.html) · 프로젝트 실측 (57 파일 / 약 90건, 2026-04~06)

### C — 메서드명 반복 doc

**메서드 이름을 한국어 문장으로 풀어 쓴 doc 주석은 지운다. 남길 이유가 있으면 이름 대신 계약을 쓴다.**

```dart
// before
/// 눌림 시작 상태를 처리합니다.
void handlePressStart() { ... }

/// 값을 초기화하도록 합니다.
void reset() { ... }

// after — 이름의 반복은 삭제
void handlePressStart() { ... }

// after — public API 는 doc 을 남기되 이름이 아니라 계약을 적는다
/// 진행 중인 반복 타이머를 취소하고 오프셋을 0 으로 되돌린다.
/// 취소 시점에 `onChanged` 가 마지막 값으로 한 번 더 불린다.
void reset() { ... }
```

**왜** — 번역투 종결형(`~을 처리합니다`, `~하도록 합니다`)이 따라붙는 doc 은 이름을 두 번 읽게 만들 뿐이다. 호출자가 코드를 열지 않고 알아야 하는 것은 이름이 아니라 계약과 부수효과 순서다.

**예외** — public API 계약, 그리고 부수효과 순서가 호출자에게 중요한 경우. 파라미터·반환값 블록의 표기 형식(`- 반환값: 없음` 을 유지할지 등)은 이 카탈로그가 아니라 어댑터 슬롯(코어 규칙을 특정 스택 문법에 결속하는 값 — 주석 기호, doc 라벨 형식 등)이 정한다. 어댑터가 유지를 지시하면 C 로 판정하지 않는다.

**판정 신호** — 번역투 doc 후보 필터. 과수집되므로 히트를 위반으로 세지 말고 후보 목록으로만 쓴다:

```text
grep -rnE '^[[:space:]]*///.*(합니다|됩니다|하도록)' --include='*.dart' .
```

강도 `SHOULD` 삭제 · 축 `[코어]`

> **출처:** [Effective Dart — documentation](https://dart.dev/effective-dart/documentation)

### D — 프레임워크 기본 설명

**프레임워크 공식 문서에 이미 적힌 기본 동작을 코드 옆에 옮겨 적지 않는다.**

```dart
// before
// 크기 지정
const SizedBox(height: 12),
// borderRadius 클리핑
ClipRRect(borderRadius: BorderRadius.circular(8), child: child),
// 배경색 지정
Material(color: {TokenClass}.surface, child: child),

// after — 기본 동작 서술은 삭제하고 "왜 이 선택을 했는가"만 남긴다
const SizedBox(height: 12),
ClipRRect(borderRadius: BorderRadius.circular(8), child: child),
// 안 끄면 M3 tonal overlay 가 이 색 위에 덧칠돼 더 밝아진다
Material(
  color: {TokenClass}.surface,
  surfaceTintColor: Colors.transparent,
  child: child,
),
```

**왜** — 프레임워크 기본 동작 서술은 정보량이 0일 뿐 아니라 버전이 오르면 거짓이 되므로 유지 비용이 음수다. 남는 한 줄, 즉 그 선택을 한 이유는 D 가 아니라 H 로 승격된다.

**판정 신호** — 정규식으로 분리되지 않는다. 판정은 리뷰로 한다: **주석이 설명하는 내용이 그 API 문서 첫 문단에 있으면 D 다.**

강도 `MUST` 삭제 · 축 `[코어]`

> **출처:** [Google Engineering Practices — what to look for in a code review](https://google.github.io/eng-practices/review/reviewer/looking-for.html) · [Flutter `Material.surfaceTintColor`](https://api.flutter.dev/flutter/material/Material/surfaceTintColor.html)

### E — 접두사 fallback 변수명

**`effective*` / `resolved*` 접두사는 지우는 게 아니라 도메인·역할명으로 개명한다.**

```dart
// before
final effectiveGradient = props.gradient ?? {TokenClass}.defaultGradient;
final resolvedChildren = props.children.isNotEmpty ? props.children : fallback;

// after — 그 값이 무엇인지로 바꾼다. 호출부 전수도 함께 바꾼다
final toolbarGradient = props.gradient ?? {TokenClass}.defaultGradient;
final visibleChildren = props.children.isNotEmpty ? props.children : fallback;
```

**왜** — `??` 연산자가 이미 fallback 을 표현하므로 접두사는 역할이 아니라 계산 과정을 드러낸다. 읽는 사람이 알아야 하는 것은 "기본값이 적용됐다"가 아니라 "이게 툴바 그라디언트다"다.

**판정 신호:**

```text
grep -rnE '\b(effective|resolved)[A-Z]' --include='*.dart' .
```

강도 `관측 컨벤션` (실측 9건 / 4파일) · 축 `[코어]`. 이 카테고리는 **공개 통계 근거가 없다.** 2026-08 조사에서 접두사별 LLM 과대표집 통계는 공개 1차 문헌 어디에도 확인되지 않았다. 그래서 강도를 `관측 컨벤션` 으로 낮춰 표기하고 각주를 붙이지 않는다. 실측은 유효한 국지 근거이므로 규칙을 지우지도 않는다.

> **출처:** 프로젝트 실측 (57 파일 / 9건 · 4파일, 2026-04~06)

### F — 구분선 블록

**`// ---` 를 늘여 만든 시각적 구획은 지우고 빈 줄과 이름으로 대체한다.**

```dart
// before
// ------------------------------------------------------------
// 빌드
// ------------------------------------------------------------
@override
Widget build(BuildContext context) => Row(children: [...]);

// ============================================================
// 핸들러
// ============================================================
void handleTap() { ... }

// after
@override
Widget build(BuildContext context) => Row(children: [...]);

void handleTap() { ... }
```

**왜** — 한 파일에 14개까지 쌓이면 구분 기능 자체가 사라진다. 구분선이 필요하다고 느껴진다면 그것은 파일이 너무 길다는 신호이지 선이 필요하다는 신호가 아니다.

**예외** — 코드 생성기가 만드는 배너. 생성 파일은 대상에서 제외한다.

**판정 신호:**

```text
grep -rnE '^[[:space:]]*//[[:space:]]*[-=]{5,}' --include='*.dart' .
```

강도 `MUST` 삭제 · 축 `[코어]`

> **출처:** [Microsoft Code with Engineering Playbook — code comments](https://microsoft.github.io/code-with-engineering-playbook/documentation/guidance/code/) · 프로젝트 실측 (57 파일 / 약 28건 · 4파일, 2026-04~06)

### G — 자명 구조 라벨

**바로 아래 코드가 그대로 말하는 라벨은 이름으로 흡수한 뒤 지운다. 지우기만 하면 안 된다.**

```dart
// before
Column(children: [
  // 제목
  Text(props.title, style: {TokenClass}.titleM),
  // 서버 이름
  Text(state.name),
]),

// after — 라벨이 담던 의미를 이름으로 옮긴 뒤 라벨을 지운다
Column(children: [
  Text(props.title, style: {TokenClass}.titleM),
  Text(serverNameText),
]),

// 남는 예외 — 선언 2개 이상을 묶고 그 묶음의 축을 이름으로 못 쓰는 섹션 라벨
// 좌측: leading 또는 기본 뒤로가기
final leading = props.leading ?? const {widget_prefix}BackButtonWidget();
final leadingWidth = props.leadingWidth ?? 48.0;
```

**왜** — 라벨을 그냥 지우면 구획 정보가 이름으로 옮겨가지 않고 그냥 없어진다. 라벨이 담던 의미는 변수명이나 추출한 위젯 이름이 받아야 한다.

**예외** — 섹션 라벨의 경제성 규칙. 라벨이 **2개 이상의 선언을 묶고** 그 묶음의 축을 이름으로 표현할 수 없을 때만 남긴다. 선언 1개짜리 섹션 라벨, 그리고 라벨과 변수명이 같은 뜻인 경우는 G 다.

**판정 신호** — 단독 줄의 짧은 한국어 명사구:

```text
grep -rnE '^[[:space:]]*//[[:space:]]*[가-힣][가-힣 ]{0,8}$' --include='*.dart' .
```

강도 `SHOULD` 코드 구조로 흡수 · 축 `[코어]` `[한국어]`

> **출처:** [Effective Dart — style](https://dart.dev/effective-dart/style) · 프로젝트 실측 (57 파일 / 약 35건 · 15파일 이상, 2026-04~06)

---

### H — 좋은 주석 (위반 아님 · 보존 대상)

> **H 만 방향이 반대다.** A~G 는 after 에서 주석이 **줄어드는** 것이 정답이고, H 는 after 에서 주석이 **남아 있는** 것이 정답이다. H 를 위반 목록에 넣는 것이 이 카탈로그의 최대 오용이다.

**코드만 읽어서는 복원할 수 없는 정보는 남긴다.**

```dart
// before — A~G 일괄 삭제에 휩쓸린 결과. 컴파일은 되고 정보만 사라졌다
Material(color: {TokenClass}.surface, surfaceTintColor: Colors.transparent),
IconButton(iconSize: 24, onPressed: onTap, icon: icon),
if (isEditing) TextField(controller: c) else Text(value),

// after — 셋 다 코드로 복원되지 않는다. 남긴다
// 안 끄면 M3 tonal overlay 가 이 색 위에 덧칠돼 실제로 더 밝게 보인다
Material(color: {TokenClass}.surface, surfaceTintColor: Colors.transparent),
// 위젯 내부가 아이콘 크기를 상수로 박아 외부에서 축소 불가 — 24 고정
IconButton(iconSize: 24, onPressed: onTap, icon: icon),
// 삼항으로 합치면 TextField 가 재마운트돼 매 키입력마다 포커스가 날아간다
if (isEditing) TextField(controller: c) else Text(value),
```

**왜** — H 가 이 카탈로그에 들어 있는 이유는 A~G 를 일괄 삭제할 때 함께 지워지는 사고를 막기 위해서다. 위 세 줄은 각각 프레임워크 함정 · 제약 · 실패 모드에 대응한다.

보존 기준은 셋이고, 하나에 해당하면 남긴다.

| 기준 | 판정 질문 | 예 |
|---|---|---|
| 프레임워크 함정 | 프레임워크가 문서화하지 않았거나 직관에 반하는 동작을 설명하는가 | 테마의 tonal overlay 가 지정한 배경색을 덧칠해 실제로 더 밝게 보인다 |
| 제약·trade-off | 대안을 못 쓴 이유, 값이 그 값인 이유를 남기는가 | 위젯 내부가 아이콘 크기를 상수로 박아 외부에서 축소 불가 |
| 실패 모드 | 이 코드를 "단순화" 하면 무엇이 깨지는지 알려주는가 | 조건에 따라 트리를 바꾸면 입력 위젯이 재마운트돼 매 키입력마다 포커스가 날아간다 |

원본 규칙 문서의 "좋은 주석 기준" 절은 4줄짜리 빈 스텁이었다. 이관 시 확정된 판정은 **H 판정 기준을 그 절에 흡수** 하는 것이고, 위 3종이 그 채워진 내용이다.

**판정 신호** — 인과 접속이 들어간 주석은 **삭제 금지 후보** 로 먼저 표시한다:

```text
grep -rnE '//.*(때문|안 하면|버그|무시되|제약|하드코딩)' --include='*.dart' .
```

강도 `MUST` 보존 (위반 아님) · 축 `[코어]`

> **출처:** [Kent Beck, *Tidy First?*](https://www.oreilly.com/library/view/tidy-first/9781098151232/ch14.html) · [Flutter `Border.all`](https://api.flutter.dev/flutter/painting/Border/Border.all.html) · 프로젝트 실측 (57 파일 / 약 30건 · 10파일 이상, 2026-04~06)

---

### I — 과도한 빌더 분할

**`build()` 가 `_build*` 다단 호출 체인으로 흩어지면 인라인하거나 별도 위젯으로 뺀다.**

```dart
// before
@override
Widget build(BuildContext context) => _buildIconTextLayout();

Widget _buildIconTextLayout() => Row(children: [_buildIcon(), _buildContent()]);
Widget _buildIcon() => Icon(props.icon, size: 20);
Widget _buildContent() => _buildTextBlock();
Widget _buildTextBlock() => Text(props.label);

// after — 의미 경계·재사용·독립 테스트 셋 다 아니면 인라인
@override
Widget build(BuildContext context) => Row(
      children: [
        Icon(props.icon, size: 20),
        Text(props.label),
      ],
    );

// after — 셋 중 하나라도 해당하면 헬퍼 메서드가 아니라 별도 위젯으로 뺀다
class {widget_prefix}DeviceBadgeWidget extends StatelessWidget { ... }
```

**왜** — 이름이 본문보다 정보를 더 주지 못하는데 호출 단계만 늘어난다. "무조건 인라인" 도 "무조건 분할" 도 답이 아니고, 분할이 정당한 조건은 셋이다 — **의미 경계가 실제로 다른가 / 재사용되는가 / 독립 테스트 대상인가.**

구체적 임계치(줄 수, 헬퍼 개수, 추출 위치)는 이 카탈로그가 아니라 어댑터가 정한다.

**판정 신호:**

```text
grep -rnE '\b_build[A-Z][A-Za-z0-9]*\(' --include='*.dart' .
```

강도 `SHOULD` 재구성 · 축 `[어댑터:dart-flutter]`. 이 카테고리는 코어로 올리지 않는다. 다른 스택으로 옮기려면 그 스택에서 위반이 실제로 관측된 뒤에 어댑터를 추가한다.

> **출처:** [flutter/flutter `checkbox.dart`](https://github.com/flutter/flutter/blob/master/packages/flutter/lib/src/material/checkbox.dart) · 프로젝트 실측 (57 파일 / 3파일, 2026-04~06)

### J — 중복 구현

**공통 컴포넌트가 이미 있는데 그것이 감싸던 저수준 조합을 호출부에서 다시 조립하지 않는다.**

```dart
// before — 눌림 애니메이션 공통 위젯이 있는데 제스처와 스케일을 직접 엮었다
GestureDetector(
  onTapDown: (_) => _controller.forward(),
  onTapUp: (_) => _controller.reverse(),
  onTap: onTap,
  child: ScaleTransition(scale: _scale, child: child),
)

// after — 공통 위젯으로 수렴. 호출부 6곳을 위젯에 맞춘다
{widget_prefix}PressableWidget(onTap: onTap, child: child)

// 예외 — 의도된 divergence 는 이유를 남긴다. 그 줄은 H 이므로 나중에 삭제 대상이 아니다
// 공통 위젯은 탭 취소 시 원복하지만 여기선 드래그 중 축소를 유지해야 한다
GestureDetector(...)
```

**왜** — 수렴 방향을 뒤집지 마라. 호출부 6곳을 공통 위젯에 맞추는 것이 원칙이고, 공통 위젯에 파라미터를 6개 늘려 호출부를 수용하는 것이 아니다.

**판정 신호** — **판정에 프로젝트 파라미터가 필요하다.** 공통 위젯 목록과 각 위젯이 감싸는 저수준 요소를 모른 채로는 판정할 수 없다. grep 은 그 목록을 채운 뒤에만 만들어진다:

```text
grep -rnE '{공통 위젯이 감싸는 저수준 요소}' --include='*.dart' <소스 경로> \
  | grep -v '{공통 위젯 파일 경로}'
```

강도 `SHOULD` 공통 요소로 수렴 · 축 `[코어]` + 프로젝트 파라미터

> **출처:** [Google Engineering Practices — what to look for in a code review](https://google.github.io/eng-practices/review/reviewer/looking-for.html) · 프로젝트 실측 (57 파일 / 6건 · 6파일, 2026-04~06)

---

## 강도와 축

규칙 강도는 세 등급이다.

| 강도 | 뜻 | 해당 |
|---|---|---|
| `MUST` | 공식 문서가 금지·강제하거나 예외가 없음 | A B D F H(보존) |
| `SHOULD` | 권고 수준, 명시 예외 존재 | C G I J |
| `관측 컨벤션` | 공개 근거 없음, 실측만 존재 | E |

축 분포는 이렇다.

| 축 | 카테고리 | 근거 |
|---|---|---|
| `[코어]` — 스택 무관 | A B C D E F G H | 주석·네이밍 규칙이라 언어 문법에 묶이지 않는다 |
| `[어댑터:dart-flutter]` | I | 위젯 `build()` 트리 분할은 Flutter 고유 국면이다 |
| `[코어]` + 프로젝트 파라미터 | J | 규칙은 스택 무관이나 판정에 그 프로젝트의 공통 위젯 목록이 필요하다 |

`[한국어]` 는 코어 규칙 중 **판정 신호가 한국어 주석 관행에 얹힌** 경우 병기한다 (A, G). 규칙 자체는 언어 무관이고, grep 패턴만 한국어에 결속된다.

---

## 수치 기준

| 항목 | 값 | 출처 |
|------|-----|------|
| 스캔 규모 | 57 파일 / 약 275건 | 프로젝트 실측 (2026-04~06) |
| A 이름 번역 주석 | 약 85건 / 48파일 | 프로젝트 실측 |
| B 템플릿 마커 | 약 90건 / 48파일 | 프로젝트 실측 |
| C 메서드명 반복 doc | 약 7건 / 2파일 | 프로젝트 실측 |
| D 프레임워크 기본 설명 | 약 20건 / 8파일 | 프로젝트 실측 |
| E 접두사 fallback 변수명 | 9건 / 4파일 | 프로젝트 실측 (관측 컨벤션) |
| F 구분선 블록 | 약 28건 / 4파일 | 프로젝트 실측 |
| G 자명 구조 라벨 | 약 35건 / 15파일 이상 | 프로젝트 실측 |
| H 좋은 주석 (보존) | 약 30건 / 10파일 이상 · 전체의 약 11% | 프로젝트 실측 |
| I 과도한 빌더 분할 | 3파일 | 프로젝트 실측 |
| J 중복 구현 | 6건 / 6파일 | 프로젝트 실측 |
| 코어 : 어댑터 분포 | 8 : 1 (+ J 는 코어 + 프로젝트 파라미터) | 이 카탈로그 |
| `effective*`/`resolved*` 공개 통계 | 없음 (확인 실패) | 2026-08 조사 |
| 본 문서 grep 패턴 실행 검증 | 7종 전부 실행 확인 (Dart 트리 517 파일) | 2026-08-28 실행 |

---

## 안티패턴

| 안티패턴 | 문제 |
|----------|------|
| H 를 위반 목록에 넣고 A~J 를 일괄 삭제 | 코드로 복원 불가능한 정보가 사라진다. H 는 방어 카테고리다 |
| 이름은 그대로 두고 A 주석만 삭제 | 약한 이름 + 주석 없음이 되어 원래보다 나빠진다. A 의 처리는 "삭제 또는 개명"이다 |
| G 라벨을 흡수 없이 삭제 | 구획 정보가 이름으로 옮겨가지 않고 그냥 없어진다 |
| grep 히트 수를 위반 건수로 보고 | A 패턴은 H 를 함께 잡고, C 패턴은 정상 doc 을 함께 잡는다. 히트는 후보지 판정이 아니다 |
| grep 결과를 확인 없이 `sed` 로 일괄 치환 | 같은 정규식에 걸린 H 가 조용히 삭제된다. 파일 단위 확인이 캠페인 루프의 존재 이유다 |
| E 에 논문 각주를 붙여 근거를 격상 | 접두사별 공개 통계는 존재하지 않는다. 국지 실측을 문헌 근거로 위장하게 된다 |
| I 를 코어로 취급해 비-Flutter 스택에 적용 | 위반 실측이 없는 스택에 추측 규칙을 적용하는 것이다. 어댑터가 관측 후 추가된다 |
| J 를 공통 위젯 목록 없이 판정 | 무엇이 중복인지 정의하는 입력이 빠져 있어 판정 자체가 성립하지 않는다 |
| 카테고리 라벨만 붙이고 처리 방침을 구분하지 않음 | 삭제(B·D·F) / 개명(A·E) / 흡수(G) / 보존(H) / 재구성(I·J)이 서로 다른 작업이다 |

---

## Gotchas

- **A 의 grep 은 H 를 같이 잡는다** — 실행 검증에서 `surfaceTintColor: ..., // 안 끄면 M3가 배경색 위에 tint 덮음` 이 A 패턴에 그대로 걸렸다. 형태(선언 뒤 한국어 주석)가 동일하고 내용만 다르기 때문이다. A 패턴 결과는 반드시 사람이 한 줄씩 읽는다.
- **B 의 빈도 집계는 생성 파일에서 폭증한다** — 제외하지 않으면 상위 전부가 코드 생성기 배너로 채워져 실제 마커가 안 보인다. `*.g.dart` · `*.freezed.dart` 류를 반드시 제외한다.
- **C 의 처리는 어댑터 정책 상수와 충돌할 수 있다** — 파라미터·반환값 블록 표기를 유지하라고 어댑터가 정했다면 그 형식은 C 가 아니다. 카탈로그가 어댑터를 이기지 않는다.
- **E 는 선언만 고치면 컴파일이 깨진다** — 개명이므로 호출부 전수를 함께 바꾼다. 삭제 카테고리와 작업 형태가 다르다.
- **`[한국어]` 라벨은 규칙이 아니라 신호에 붙는다** — A 와 G 의 규칙은 언어 무관이고, 한국어에 묶인 것은 grep 패턴뿐이다. 다른 언어 코퍼스에서는 패턴을 다시 만들어야 하며, 규칙이 적용 불가해지는 것은 아니다.
- **"위반 0" 과 "규칙 적용 불가" 는 다르다** — 어떤 스택에서 실측이 0이라고 해서 코어 규칙이 그 스택에 안 맞는 것이 아니다. 이 카탈로그는 기존 코드 정리용이 아니라 새 코드 작성 표준이다.
- **카테고리 경계에서는 D 가 H 로 승격된다** — 프레임워크 기본 동작 서술은 D 지만, 그 동작 때문에 이 코드를 이렇게 쓸 수밖에 없었다는 이유는 H 다. 같은 API 를 언급한다고 같은 카테고리가 아니다.
