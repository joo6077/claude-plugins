---
title: tone-kit 개요 — 무엇을 잡는 킷인가
version: 0.1.0
last_updated: 2026-09-02
---

# tone-kit 개요 — 무엇을 잡는 킷인가

**이 문서가 잡는 것**

- 코드를 다시 읽어 준 주석 — 이름 번역, 템플릿 마커, 구분선, 프레임워크 기본 설명
- 역할이 아니라 외형·계산 과정을 담은 이름 — `BlueDeviceRow`, `effectiveGradient`, `BoolCallback`
- 번역투 한국어 doc 과 표기가 갈린 doc 라벨

```dart
// before
// ------------------------------------------------
// 위젯 구현부
class {widget_prefix}BlueDeviceRowWidget extends StatelessWidget {
  final String? text;   // 버튼 텍스트
  /// 눌림 시작을 처리합니다.
  void handlePressStart() {
    final effectiveGradient = props.gradient ?? defaultGradient;
  }
}
// after
class {widget_prefix}DeviceItemWidget extends StatelessWidget {
  final String? text;
  /// 길게 누르기 반복을 시작한다.
  void startLongPressRepeat() {
    final toolbarGradient = props.gradient ?? defaultGradient;
  }
}
```

한 번에 다섯 가지가 걸렸다 — 템플릿 마커, 구분선, 이름 번역 주석, fallback 접두사, 번역투 doc. 목표는 **읽고 고치기 쉬운 코드**이고 톤 개선은 그 부산물이다. 이 킷은 AI 탐지 회피 도구가 아니며, 규칙마다 붙는 `MUST` / `SHOULD` / `관측 컨벤션` 3등급의 판정 방법론은 [ai-code-stylometry.md](ai-code-stylometry.md) 가 소유한다.

## 용어 3개

- **관측 컨벤션** — 공개 출처 없이 프로젝트 실측만 있는 규칙. 준수 강도가 낮다는 뜻이 아니라 근거가 국지적이라는 뜻이다. 논문 각주를 붙이지 않는다.
- **어댑터** — 코어 규칙을 특정 스택 문법에 결속하는 파일. 주석 기호, doc 라벨 구조, 금지 접두사, 완료 게이트 grep 을 채운다. 현재 `dart-flutter` 하나뿐이다.
- **완료 게이트** — 완료를 선언하기 전에 돌리는 grep·awk 묶음. 통과 기준은 "돌렸다"가 아니라 "히트마다 판정을 적었다" 다.

## 스킬 3종 — 언제 쓰는가

| 스킬 | 쓰는 때 | 하는 일 |
|---|---|---|
| `tone-guide` | 코드를 쓰기 직전 · 리뷰할 때 | 규칙을 로드하고 완료 선언 전에 전수 대조한다. 요청 범위 밖으로 번지지 않는다 |
| `tone-scaffold` | 새 파일을 만들 때 | 파일 헤더 · doc 주석 · 시맨틱 typedef 를 프로젝트 파라미터로 채워 생성하고 자기 감사한다 |
| `tone-campaign` | 기존 코드 수십~수백 파일을 정리할 때 | 의존순 배치, 파일당 승인 게이트, 재개용 원장으로 굴린다. 일괄 편집하지 않는다 |

## 대표 before/after 10쌍

`→` 가 있는 블록은 왼쪽이 before, 오른쪽이 after 다.

### 1. 이름을 옮기기만 한 주석은 지운다

```dart
String? text,      // 버튼 텍스트   →   String? text,
bool isChecked,    // 체크 여부     →   bool isChecked,
```

이름과 타입이 이미 같은 말을 한다. 지워도 정보 손실이 0이다. 이름이 약해서 주석이 필요했던 경우가 유일한 예외이고, 그때는 주석이 아니라 이름을 고친다.

**강도** MUST · **출처** [Effective Dart: Documentation](https://dart.dev/effective-dart/documentation) · 실측 48파일 약 85건 (전체 안티패턴의 30%)

### 2. 기계가 남긴 흔적은 지운다 — 마커 · 구분선 · 디자인 툴 참조

```dart
// before
// ------------------------------------------------
// 상태
// 카드 배경 그라데이션 상단 (노드 12159:8715 Frame/Card)
static const cardBevelTop = ...;
// after
static const cardBevelTop = ...;
```

파일이 무엇인지는 선언부가 이미 말하고, 구분선은 여러 개 쌓이는 순간 구분 기능을 잃는다. 코드는 디자인 소스의 참조가 아니라 구현물이므로 노드 ID·변수 경로·CSS 원문을 남기지 않는다. 대체 수단은 빈 줄과 의미 있는 이름이다.

**강도** MUST · **출처** [Microsoft Code with Engineering Playbook](https://microsoft.github.io/code-with-engineering-playbook/documentation/guidance/code/) · [Google Engineering Practices](https://google.github.io/eng-practices/review/reviewer/looking-for.html)

### 3. 기본 동작 설명은 지우되 이유는 남긴다

```dart
// before — 프레임워크 문서 첫 문단에 이미 있는 내용
// surfaceTintColor 는 Material 3 에서 표면에 색조를 입힌다.
surfaceTintColor: Colors.transparent,
// after — 코드만 읽어서는 복원할 수 없는 정보
// M3 surface tint 가 배경을 덮어 지정색이 밝아진다. 그래서 tint 를 끈다.
surfaceTintColor: Colors.transparent,
```

기본 동작 서술은 정보량이 0일 뿐 아니라 버전이 오르면 거짓이 되므로 유지 비용이 음수다. 반대로 함정·제약·실패 모드를 담은 주석은 **보존 대상**이고, 안티패턴 목록만 보고 일괄 삭제하면 이쪽이 함께 날아간다. 보존 표시가 삭제 후보 선정보다 먼저다.

**강도** 삭제 MUST / 보존 MUST · **출처** [Material.surfaceTintColor](https://api.flutter.dev/flutter/material/Material/surfaceTintColor.html) · [Google Engineering Practices](https://google.github.io/eng-practices/review/reviewer/looking-for.html)

### 4. 이름에 외형과 표 어휘를 넣지 않는다

```dart
class {widget_prefix}BlueDeviceRowWidget ...   →   class {widget_prefix}DeviceItemWidget ...
class {widget_prefix}BlueDeviceRowState ...    →   class {widget_prefix}DeviceItemState ...
```

색은 테마가 바뀌면 거짓이 되고, `Row` 와 `Cell` 은 표 전용 어휘라 진짜 표가 생기면 이름이 충돌한다. 세로 리스트 한 장의 기본값은 `Item` 이다. 컴포넌트와 그것이 받는 데이터 타입은 같은 역할어로 정렬한다 — 어긋나면 검색이 한쪽만 잡는다.

**강도** 외형 금지 SHOULD · 표 어휘 금지는 합성 규칙(6개 디자인 시스템의 어휘를 대조해 만든 규칙 — 단일 권위가 없다) · **출처** [Effective Dart: Style](https://dart.dev/effective-dart/style) · [Carbon Tile](https://carbondesignsystem.com/components/tile/usage/) · [MUI ListItem](https://mui.com/material-ui/api/list-item/)

### 5. fallback 접두사를 이름으로 쓰지 않는다

```dart
final effectiveGradient = props.gradient ?? defaultGradient;   →   final toolbarGradient = ...
final resolvedChildren = props.children ?? const [];           →   final visibleChildren = ...
```

기본값 연산자가 이미 fallback 을 표현한다. 접두사는 역할이 아니라 계산 과정을 드러낸다. 삭제가 아니라 개명이고, 선언만 고치면 컴파일이 깨지므로 호출부 전수를 함께 바꾼다.

**강도** 관측 컨벤션 (실측 9건 / 4파일) · **출처** 프로젝트 실측만. 접두사별 공개 통계는 확인되지 않았으므로 논문 각주를 붙이지 않는다

### 6. 콜백 타입에는 시그니처가 아니라 의미를 붙인다

```dart
typedef BoolCallback = void Function(bool value);   →   typedef {widget_prefix}EventVisibleChanged = void Function(bool value);
final void Function(bool) onVisibleChanged;         →   final {widget_prefix}EventVisibleChanged onVisibleChanged;
```

`BoolCallback` 은 타입에서 의미를 읽을 수 없다. 한 아이템의 콜백 세 개가 전부 같은 타입이면 그것이 증상이다. typedef 는 의미가 생겨난 위젯의 파일에 top-level 로 두고 공유 typedef 파일은 만들지 않는다 — 모아 두면 어느 컴포넌트의 계약인지 추적이 끊긴다.

**강도** 관측 컨벤션 (실측 51선언 / 32파일) · **출처** 프로젝트 실측

### 7. 위젯을 반환하는 헬퍼 대신 위젯을 만든다

```dart
// before
Widget build(BuildContext context) => Column(children: [_buildHeader(), _buildBody()]);
Widget _buildHeader() => ...;
// after
Widget build(BuildContext context) =>
    const Column(children: [{widget_prefix}SettingsHeaderWidget(), {widget_prefix}SettingsBodyWidget()]);
```

헬퍼는 호출 단계만 늘리고 rebuild 는 끊지 못한다. 분리 조건은 넷이다 — 관심사가 다른가 / 같은 패턴이 3곳 이상인가 / 독립 테스트 대상인가 / 본문이 파일 오버헤드보다 큰가. 하나라도 성립하면 위젯으로 빼고 넷 다 아니면 인라인한다. 줄 수는 판정식이 아니라 알람이다.

**강도** SHOULD (공식 문구가 `prefer` 이고 `Builder` 라는 공식 인라인 대안이 있다) · **출처** [StatelessWidget](https://api.flutter.dev/flutter/widgets/StatelessWidget-class.html) · [Builder](https://api.flutter.dev/flutter/widgets/Builder-class.html) · [flutter#149932](https://github.com/flutter/flutter/issues/149932)

### 8. 간격은 프레임워크 파라미터로 표현한다

```dart
// before
Row(children: [icon, SizedBox(width: {TokenClass}.w10), label])
children: sections.map(_body).expand((w) => [divider, w]).skip(1).toList()
// after
Row(spacing: {TokenClass}.w10, children: [icon, label])
ListView.separated(itemCount: sections.length, separatorBuilder: (_, __) => divider, itemBuilder: _body)
```

프레임워크가 이미 가진 파라미터를 손으로 재구현한 것이고, 항목이 늘 때마다 삽입 위치를 사람이 관리해야 한다. 체이닝은 짧아 보이지만 읽는 비용을 올린다.

**강도** 관측 컨벤션 · **출처** [Dart collections](https://dart.dev/language/collections) · [Cognitive Complexity (SonarSource)](https://www.sonarsource.com/resources/cognitive-complexity/)

### 9. 번역투를 능동 단문으로 바꾼다

```text
/// 눌림 시작을 처리합니다.              →   // 길게 누르기 반복을 시작한다.
// 배경색이 오버레이에 의해 변경됩니다.   →   // Material 3 surface tint 가 배경색을 덮어 실제 색이 더 밝아 보인다.
```

종결어미만 `한다`체로 바꿔도 문장 구조가 그대로면 번역투는 남는다. 주체를 되살리고 원인과 결과를 구체로 잇는다. 둘째 줄은 번역투와 음역이 같이 걸린 사례다 — 공식 API 이름은 영어 원문(`surface tint`), 일반 명사는 한국어로 쓴다.

**강도** SHOULD · **출처** [국립국어원 공공언어 자료](https://korean.go.kr/front/etcData/etcDataView.do?etc_seq=663) · [Effective Dart: Documentation](https://dart.dev/effective-dart/documentation)

### 10. doc 라벨은 자유 서술이 아니라 상수다

```dart
// before
/// 네트워크 상태를 확인합니다.
/// - [ctx]: 컨텍스트
/// - 리턴: N/A
// after
/// 네트워크가 끊겨 있으면 안내 다이얼로그를 띄운다.
///
/// - [context]: 다이얼로그 표시용 빌드 컨텍스트
/// - 반환값: 없음
```

실측 규모가 `- 반환값:` 577건 / 80파일, `- [param]:` 788건이다. 이 규모에서 표기가 둘로 갈리면 커버리지 측정과 완료 게이트가 동시에 깨진다. `- 반환값: 없음` 을 노이즈로 보고 지우면 "doc 이 없는 것"과 "반환값이 없는 것"을 구분할 수 없다. 표기를 바꾸려면 전수 치환을 같은 커밋에서 끝낸다.

**강도** 관측 컨벤션 · **출처** [Effective Dart: Documentation](https://dart.dev/effective-dart/documentation) · 프로젝트 실측 (2026-08-28 전수 감사)

## 3축 레이어

규칙은 세 축이 직교한다 — 스택(코어 / 어댑터), 언어(중립 / 로케일), 프로젝트(공통 / 파라미터). 구분선 주석 금지는 스택 무관 코어이고 `_build*` 접두사 금지는 dart-flutter 어댑터다. `- 반환값:` 라벨은 Dart 가 아니라 한국어에 묶여 있어서 영어 프로젝트에서는 `- Returns:` 가 되지만 골격과 커버리지 기준은 그대로 남는다. `{widget_prefix}` 나 `{TokenClass}` 같은 값은 킷이 정하지 않고 프로젝트가 소유하며, 확정값은 프로젝트의 `.claude/tone-project.md` 에 남는다. 한 규칙이 세 축에 동시에 걸릴 수 있다 — `- 반환값: 없음` 은 어댑터 × 한국어 × 공통이다.

## 완료 게이트는 이렇게 생겼다

```bash
SRC=lib; INC="--include=*.dart"                               # 프로젝트 값으로 교체

grep -rnE '^[[:space:]]*//[[:space:]]*[-=]{5,}' "$SRC" $INC   # 구분선 블록 — 히트 = 위반
grep -rnE '\b(effective|resolved)[A-Z]' "$SRC" $INC           # fallback 접두사 — 히트 = 개명 후보
grep -rnE '\b_build[A-Z][A-Za-z0-9]*\(' "$SRC" $INC           # 위젯 반환 헬퍼 — 히트 ≠ 위반
```

**히트가 곧 위반은 아니다.** 세 번째 패턴은 추출이 정당한 건까지 잡으므로 히트 수를 위반 수로 보고하면 근거 없는 지적이 된다. 각 패턴에는 "히트가 위반인지" 판정이 병기돼 있고, 최종 판정은 파일을 열어야 나온다. 0건도 그 자체로는 통과가 아니다 — "위반이 없는 것"과 "패턴이 죽은 것"을 구분하지 못하므로, 준수 상태에서 0건이 정상인 패턴은 합성 양성 케이스로 살아 있음을 따로 증명한다.

## 다음에 읽을 것

| 무엇이 궁금한가 | 문서 |
|---|---|
| 주석 하나를 지울지 남길지 판정하고 싶다 | [comment-economy.md](comment-economy.md) |
| 위반을 카테고리로 나누고 grep 후보를 뽑고 싶다 | [antipattern-catalog.md](antipattern-catalog.md) |
| 컴포넌트 이름의 접미사를 못 고르겠다 | [naming-taxonomy.md](naming-taxonomy.md) |
| 쪼갤지 그냥 둘지 판단이 안 선다 | [extraction-thresholds.md](extraction-thresholds.md) |
| 한국어 주석 문체와 doc 라벨 규칙 | [korean-technical-writing.md](korean-technical-writing.md) |
| Dart/Flutter 문법 관용구와 어댑터 슬롯 값 | [dart-flutter-idioms.md](dart-flutter-idioms.md) |
| 수십~수백 파일을 순차로 정리하는 운영법 | [campaign-methodology.md](campaign-methodology.md) |
| 이 킷이 무엇을 목표로 삼지 않는가 · 근거 등급 체계 | [ai-code-stylometry.md](ai-code-stylometry.md) |

어떤 1차 출처를 언제 확인했는지는 [research-log.md](research-log.md) 에 사이클별로 쌓인다. 스킬이 런타임에 Read 하는 운영 규칙은 이 문서들이 아니라 `tone-kit/references/` 9종이다 — 리서치 문서가 근거를 갖고, references 가 판정표와 실행 가능한 게이트를 갖는다.
