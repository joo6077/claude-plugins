---
title: 추출 임계 — 언제 쪼개고 언제 두는가
version: 0.1.0
last_updated: 2026-08-28
---

# 추출 임계 — 언제 쪼개고 언제 두는가

메서드 추출 · 클래스 추출 · 인라인 유지 중 무엇을 고를지의 판단 기준. 과잉 추출(pass-through 래퍼, 헬퍼 체인)과 과소 추출(비대한 단일 build) 양방향을 같은 잣대로 다룬다.

---

## 원칙

### 1. 관심사가 다르면 분리한다 — 줄 수는 트리거일 뿐 기준이 아니다 `[코어]`

책임이 다른 것이 한 함수·클래스·파일에 섞여 있으면 분리한다. 줄 수·헬퍼 개수 임계치는 "이미 늦었다"를 알리는 **하한 알람**이지 분리 여부의 판정식이 아니다. 임계치 미만이어도 관심사가 다르면 분리하고, 임계치를 넘겨도 관심사가 하나면 쪼개지 않는다.

Fowler 는 함수 길이 자체를 기준으로 삼지 않는다. 기준은 "의도와 구현을 분리할 수 있는가"다. 길이는 냄새를 알아채는 신호이지 규칙이 아니다.

> **출처:** [Function Length (Fowler)](https://martinfowler.com/bliki/FunctionLength.html) · [Code Smell (Fowler)](https://martinfowler.com/bliki/CodeSmell.html)

**강도: SHOULD.** 공개 1차 출처는 길이 기준을 명시적으로 부정하지만, 대체 판정식을 기계적으로 제시하지는 않는다.

### 2. 이름이 본문보다 의미를 더하지 않으면 인라인한다 `[코어]`

추출은 "의도를 드러내는 이름"을 붙일 수 있을 때만 이득이다. 이름이 본문을 읽는 것과 같은 수준의 정보만 준다면 가독성이 오른 게 아니라 **읽기 비용이 호출부에서 정의부로 이동**한 것이다. 이 경우 Inline Function 대상이다.

over-decomposition 은 실재하는 실패 모드다. Clean Code 저자 본인도 공개 토론에서 이를 인정했다.

> **출처:** [Inline Function (Fowler)](https://refactoring.com/catalog/inlineFunction.html) · [Extract Function (Fowler)](https://refactoring.com/catalog/extractMethod.html) · [aposd-vs-clean-code (Ousterhout · Martin 공개 토론)](https://github.com/johnousterhout/aposd-vs-clean-code)

**강도: SHOULD.**

### 3. 큰 build() 는 분리한다 — 기준은 LOC 가 아니라 rebuild 빈도다 `[어댑터:dart-flutter]`

Flutter 공식 성능 문서는 "Avoid overly large single widgets with a large `build()` function" 과 "Split them into different widgets" 를 권고한다. 다만 **공식 문서에 LOC 임계값은 없다.** 분리 기준은 줄 수가 아니라 encapsulation 과 "how they change" 다.

같은 문서군의 반대편도 읽어야 한다. `StatefulWidget` 문서는 "built once then never update" 하는 위젯에 대해 "somewhat complicated and deep build methods" 를 문제 삼지 않는다. 즉 라우트 최상단처럼 사실상 rebuild 되지 않는 위젯의 큰 build 는 공식적으로 용인되는 영역이다. 반대로 build 는 "potentially as often as once per rendered frame" 호출될 수 있으므로, 프레임마다 재실행되는 큰 subtree 는 분리 우선순위가 높다.

> **출처:** [Flutter performance best practices](https://docs.flutter.dev/perf/best-practices) · [StatefulWidget class](https://api.flutter.dev/flutter/widgets/StatefulWidget-class.html) · [Flutter architectural overview](https://docs.flutter.dev/resources/architectural-overview)

**강도: SHOULD.** 성능 핫스팟이거나 자주 rebuild 되는 큰 subtree 에 한해 프로젝트 규칙으로 MUST 승격할 수 있다. 승격하는 경우 **승격 사유(프로파일링 결과 또는 rebuild 빈도)를 규칙 옆에 명시**해야 한다. 사유 없는 전역 MUST 는 킷의 창작이다.

### 4. 헬퍼 메서드보다 위젯 클래스를 선호한다 — 그러나 금지는 아니다 `[어댑터:dart-flutter]`

`StatelessWidget` 문서는 "prefer using a widget rather than a helper method" 라고 쓴다. 이유는 스타일이 아니라 메커니즘이다. 위젯으로 분리하면 프레임워크가 "short-circuit most of the rebuild work" 를 할 수 있는 지점이 생긴다. 헬퍼 메서드가 반환한 위젯은 그 지점이 없어 부모와 항상 함께 재실행된다.

**반대 방향도 같이 알아야 한다.** Flutter 는 클래스 추출을 우회하는 공식 API 를 스스로 제공한다. `Builder` 문서는 자신을 "inline alternative to defining a `StatelessWidget` subclass" 라고 정의한다. 공식 마이그레이션 문서에는 `Widget _getToggleChild()` 같은 위젯 반환 함수 예시가 실려 있다. 프레임워크 이슈 트래커에도 "reevaluate if we are making the right trade-off here between naginess and performance" 라는 논의가 남아 있다.

> **출처:** [StatelessWidget class](https://api.flutter.dev/flutter/widgets/StatelessWidget-class.html) · [Builder class](https://api.flutter.dev/flutter/widgets/Builder-class.html) · [Flutter for Xamarin.Forms developers](https://docs.flutter.dev/flutter-for/xamarin-forms-devs) · [flutter/flutter#149932](https://github.com/flutter/flutter/issues/149932)

**강도: SHOULD.** 공식 문구가 `prefer` 이고 공식 반례가 존재한다. 단순 조건 분기나 아주 작은 local glue 까지 `MUST NOT` 으로 금지할 공개 근거는 없다.

### 5. rebuild 격리를 노렸다면 격리 조건까지 확인하라 `[어댑터:dart-flutter]`

위젯 클래스로 뺐다는 사실만으로 rebuild 가 끊기지 않는다. Element 는 "the same instance is returned each time" 인 경우에만 "the element skips updating itself" 한다. 매 build 마다 새 인스턴스를 만들어 넘기면 타입만 늘고 격리는 0 이다. 그리고 위젯 교체 판정은 `runtimeType and key` 로 이뤄지므로, 같은 타입에 다른 인자를 넘기면 element 는 갱신된다.

```dart
// 격리 안 됨 — 부모 build 마다 새 인스턴스
Column(children: [SectionHeader(title: title)])

// 격리 됨 — 동일 인스턴스 (const)
const Column(children: [SectionHeader(title: '설정')])
```

상태 소유 위치가 추출보다 먼저다. `setState` 는 "possibly triggering rebuilds for the entire subtree rooted at this widget" 이므로, 상태를 상위에 둔 채 하위만 쪼개면 분리 효과가 상쇄된다.

> **출처:** [Element.rebuild](https://api.flutter.dev/flutter/widgets/Element/rebuild.html) · [Widget.canUpdate](https://api.flutter.dev/flutter/widgets/Widget/canUpdate.html) · [State.setState](https://api.flutter.dev/flutter/widgets/State/setState.html)

**강도: SHOULD.**

### 6. 헬퍼가 헬퍼를 부르는 체인은 만들지 않는다 `[코어]`

`build() → _buildA() → _buildB()` 식 체인은 주 흐름을 읽기 위해 왕복 이동을 강제한다. 허용 깊이는 0 단 — 헬퍼가 다른 헬퍼를 호출하면 인라인하거나 별도 위젯으로 승격한다. 각 단계의 이름이 본문보다 의미를 더하는지 개별 판정하면, 체인 중간 단계는 대개 원칙 2 의 Inline 대상으로 떨어진다.

> **출처:** 공개 1차 출처 없음 — 관측 프로젝트 규칙(2026-04-17 제정, 위젯 리팩토링 세션 피드백). 보조 근거: [Inline Function (Fowler)](https://refactoring.com/catalog/inlineFunction.html) · [Cognitive Complexity (SonarSource)](https://www.sonarsource.com/resources/cognitive-complexity/)

**강도: 관측 컨벤션.** 체인 깊이 임계값을 명시한 공개 1차 출처는 없다.

### 7. "모든 sub-widget 은 별도 *파일*" 은 관측 컨벤션이다 `[어댑터:dart-flutter]`

관측 프로젝트는 위젯 조각을 같은 파일 인라인 클래스로도 두지 않고 예외 없이 별도 파일로 뺀다. thin wrapper 도 예외가 아니며, 파일이 private 접두사를 못 쓰므로 public 클래스 + 프로젝트 접두사(`{widget_prefix}`) 규칙과 짝을 이룬다. 이유는 성능이 아니라 탐색성이다 — 화면 파일이 길어지면 로직을 찾기 어렵다.

**공개 1차 출처는 "different widgets" 까지만 지지하고 "different files" 는 지지하지 않는다.** 파일 분리를 성능 문서로 정당화하지 마라. 파일 단위 규칙을 쓰려면 근거를 프로젝트 탐색성으로 밝혀야 한다.

> **출처:** 공개 1차 출처 없음 — 관측 프로젝트 실측(Props 골격 보유 110 파일에 일관 적용 — `^abstract class *Props` 선언 파일, 코드 생성물 제외, 2026-08-31 재측정). 공식 문서가 지지하는 범위는 위젯 단위까지: [Flutter performance best practices](https://docs.flutter.dev/perf/best-practices)

**강도: 관측 컨벤션.**

### 8. 발생하지 않는 분기는 추출 대상이 아니라 제거 대상이다 `[코어]`

실사용 조합이 하나인데 null 조합 4가지를 방어하면, 그 복잡도는 실제 복잡도가 아니라 가상 복잡도다. "현재 요구를 이해하기 어렵게 만드는 추상화는 presumed guilty" 다. 이런 코드는 헬퍼로 빼서 감출 게 아니라 지운다.

조합 제약은 흐름이 아니라 경계에서 표현한다. Flutter 자체 위젯도 build 안에서 모든 조합을 방어하지 않고 생성자 assert 로 유효 조합을 강제한다 — `Tab` 은 `text`/`child` 동시 사용을 막고, `Positioned` 는 `left + right + width` 동시 지정을 막는다. Dart 의 `assert` 는 debug 에서만 살아 있으므로 내부 호출자 대상 제약에 적합하고, 외부 입력 경계에는 명시적 검증을 쓴다.

> **출처:** [Yagni (Fowler)](https://martinfowler.com/bliki/Yagni.html) · [Tab constructor](https://api.flutter.dev/flutter/material/Tab/Tab.html) · [Positioned constructor](https://api.flutter.dev/flutter/widgets/Positioned/Positioned.html) · [Dart constructors](https://dart.dev/language/constructors)

**강도: SHOULD.**

### 9. pass-through 래퍼는 과분할이다 `[코어]`

받은 것을 그대로 넘기기만 하는 래퍼 레이어는 형제 위젯 유무와 무관하게 추가 간접층이다. 클래스가 제 몫의 책임을 갖지 못하면 Inline Class 대상이다. 추출의 유일한 실효인 rebuild 격리조차, 형제가 싼 위젯이면 정당화되지 않는다.

같은 이유로 "재사용 가능성" 하나만으로 1회성 로직을 클래스로 승격하지 않는다. 실사용처가 1~2곳이면 인라인이 적정이고, 같은 패턴이 3곳 이상 반복될 때 추출을 검토한다.

> **출처:** [Inline Class (Fowler)](https://refactoring.com/catalog/inlineClass.html) · [Yagni (Fowler)](https://martinfowler.com/bliki/Yagni.html)

**강도: SHOULD.** 반복 3회 임계값 자체는 관측 컨벤션이다.

---

## 수치 기준

| 항목 | 값 | 출처 |
|------|-----|------|
| 공식 build() LOC 임계값 | 없음 | [Flutter performance best practices](https://docs.flutter.dev/perf/best-practices) |
| build() 호출 빈도 상한 | 렌더 프레임당 1회까지 | [Flutter architectural overview](https://docs.flutter.dev/resources/architectural-overview) |
| 위젯 교체 판정 기준 | `runtimeType` + `key` 2개 | [Widget.canUpdate](https://api.flutter.dev/flutter/widgets/Widget/canUpdate.html) |
| `setState` rebuild 범위 | 해당 위젯 루트의 subtree 전체 | [State.setState](https://api.flutter.dev/flutter/widgets/State/setState.html) |
| 인라인 유지 상한 | 100줄 이하 + 주 경로 1개 | 관측 컨벤션 |
| 분할 하한 트리거 | 파일 500줄 초과 또는 위젯 반환 헬퍼 8개 이상 | 관측 컨벤션 |
| 헬퍼 체인 허용 깊이 | 0단 (헬퍼→헬퍼 호출 금지) | 관측 컨벤션 |
| 추출 검토 반복 임계 | 같은 패턴 3곳 이상 | 관측 컨벤션 |
| 서브폴더 그룹화 트리거 | 관련 파일 3쌍 이상 | 관측 컨벤션 |
| 파일 분리 컨벤션 실측 범위 | Props 골격 보유 110 파일 | 관측 컨벤션 (2026-08-31 재측정) |

---

## 안티패턴

| 안티패턴 | 문제 |
|----------|------|
| 줄 수 임계치를 분리 여부의 판정식으로 사용 | 관심사가 하나인 긴 코드를 쪼개고 관심사가 섞인 짧은 코드는 방치한다 |
| 공식 문서의 `prefer` 를 전역 `MUST` 로 승격 | 승격분이 근거로 둔갑한다. 승격하려면 rebuild 빈도·프로파일링 사유를 병기해야 한다 |
| 파일 분리 규칙을 성능 문서로 정당화 | 공개 1차 출처는 "different widgets" 까지만 지지한다. 파일 단위 근거는 탐색성이다 |
| 이름이 본문과 같은 수준인 헬퍼 추출 | 가독성이 오르지 않고 읽기 비용이 정의부로 이동만 한다 |
| 헬퍼가 헬퍼를 부르는 다단 체인 | 주 흐름을 읽는 데 왕복 이동이 강제된다 |
| 발생하지 않는 null 조합을 헬퍼로 감싸 은닉 | 가상 복잡도를 구조화해 영구화한다. 제거 대상을 추출 대상으로 오인한 것 |
| pass-through 래퍼 레이어 추가 | 책임 없는 간접층. rebuild 격리 효과도 형제가 싼 위젯이면 없다 |
| "재사용 가능성" 만으로 1회성 로직 클래스 승격 | 실사용처가 1곳이면 타입 수만 늘어난다 |
| 위젯 추출 후 매 build 마다 새 인스턴스 전달 | 격리를 노린 추출인데 element 가 skip 하지 못해 효과가 0 이다 |

---

## Gotchas

- **위젯 클래스로 뺀다고 paint boundary 가 생기지 않는다** — 리페인트 격리는 `RepaintBoundary` 라는 별도 메커니즘이고, 클래스 추출은 rebuild(위젯 재구성) 축이다. "쪼갰으니 다시 그리지 않는다"는 두 축을 섞은 오해다. 리페인트가 문제면 추출이 아니라 `RepaintBoundary` 를 검토하고, 경계 자체도 비용이 있으므로 남발하지 마라. ([RepaintBoundary](https://api.flutter.dev/flutter/widgets/RepaintBoundary-class.html))
- **"과분할 금지"와 "관심사 분리 의무"는 충돌하지 않는다** — 판정 순서가 다르다. 먼저 "관심사가 실제로 다른가"를 묻고, 다르면 분리한다(원칙 1). 같은데 길이만 길면 쪼개지 않는다. pass-through 래퍼 금지(원칙 9)는 후자에만 적용되며, 관심사가 다른 sub-widget 추출 의무를 취소하지 않는다.
- **분리 강도를 프로젝트 규칙으로 올릴 때 사유를 같이 적어라** — 공식 근거는 SHOULD 까지다. rebuild 빈도나 프로파일링 결과 없이 MUST 로 쓰면, 나중에 그 규칙이 왜 있는지 아무도 재구성하지 못하고 규칙만 남는다.
- **상태 소유 위치를 안 고치고 하위만 쪼개면 격리가 없다** — `setState` 는 subtree 전체를 rebuild 시킨다. 추출 전에 상태를 leaf 로 내릴 수 있는지 먼저 본다. 순서를 뒤집으면 파일만 늘고 프레임 비용은 그대로다.
- **`const` 는 추출의 목적이 아니라 조건이다** — 클래스로 빼는 이유가 `const` 라면, 실제로 `const` 로 생성되는지까지 확인해야 이득이 발생한다. 동적 인자를 받는 위젯은 `const` 가 되지 않으므로 그 경우 추출 근거를 rebuild 격리가 아닌 관심사 분리로 다시 세워야 한다.
- **폐기 이력** — 원본 규칙 세트의 "메서드 추출 vs 클래스 추출" 판단표(2026-04-17 제정)와 "헬퍼 이름이 명확하면 1단 헬퍼 허용" 조항은 2026-06-09 개정으로 폐기됐다. 본문은 이관하지 않는다. 이관 대상은 개정 후 위치(원칙 4·6·7)뿐이다.
- **인용 금지 출처를 다시 끌어오지 마라** — 이 규칙군의 원본 근거였던 비공개 사내 가이드라인 문서는 공개 킷에서 인용할 수 없다. 위 원칙 3·4 의 공개 URL 이 대체 근거이며, 규칙 강도도 그 URL 의 문구 강도를 넘지 않는다.
