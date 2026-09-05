---
title: 주석 경제성
version: 0.1.0
last_updated: 2026-09-02
---

# 주석 경제성

언제 주석을 쓰고 언제 지우는가. 스택·언어에 무관한 코어 원칙과 판정 기준을 정리한다.
주석은 공짜가 아니라 코드와 함께 썩는 자산이므로, 남길 이유를 대지 못하면 지운다.

---

## 이 문서가 잡는 것

1. **지운다** — 코드를 다시 읽어준 문장. 이름 번역, 템플릿 마커, 구분선, 프레임워크 기본 동작 설명, 자명한 구조 라벨.
2. **남긴다** — 코드만 봐서는 복원되지 않는 것. 함정, 외부 API 제약, 재현된 실패 모드.
3. **옮긴다** — 정보는 맞는데 위치가 틀린 것. 이름으로, 함수 경계로, 공개 API 계약 doc으로.

```dart
// Before — 코드가 이미 말하는 문장
final duration = const Duration(milliseconds: 300); // 300ms
await controller.forward();                          // 애니메이션 실행

// After — 코드만으로 복원되지 않는 것만
// 300ms 아래로 내리면 저사양 기기에서 첫 프레임이 잘려 깜빡인다.
final duration = const Duration(milliseconds: 300);
await controller.forward();
```

각 원칙 끝에 준수 강도(`MUST` / `SHOULD` / `관측 컨벤션` — 공개 출처 없이 프로젝트 실측만 근거인 규칙이라는 뜻이지, 지켜도 그만이라는 뜻이 아니다)와 출처를 붙였다. 제목 옆 `[코어]`는 축(그 규칙이 속한 분류 — 여기서는 스택·언어 무관 공통) 라벨이다. 정의는 맨 아래 [강도·축 라벨](#강도축-라벨) 참고.

---

## 원칙

### 1. what이 아니라 why만 남긴다 `[코어]`

**동작 설명은 지우고, 그 선택을 한 이유만 남긴다.**

```dart
// Before — 프레임워크 기본 동작 설명
// setState 를 호출하면 위젯이 다시 빌드된다.
setState(() => _expanded = true);

// Before — 이유가 아니라 절차를 옮겨 적은 주석
// 리스트를 순회하면서 완료된 항목만 걸러낸다.
final done = items.where((e) => e.isDone).toList();

// After
setState(() => _expanded = true);
final done = items.where((e) => e.isDone).toList();
```

동작 설명은 코드가 이미 하고 있다. 주석에 남길 것은 그 선택을 한 이유, 즉 대안을 버린 근거다.
실측에서 안티패턴 275건 중 보존 가치가 있던 주석은 약 30건(11%)뿐이었고, 나머지는 전부 코드를 다시 읽어 준 문장이었다.

**강도:** SHOULD

> **출처:** [Google Engineering Practices](https://google.github.io/eng-practices/review/reviewer/looking-for.html)

### 2. 주변 맥락과 중복되면 삭제한다 `[코어]`

**타입·이름·시그니처가 이미 말하는 것을 문장으로 반복하지 않는다.**

```dart
// Before — 이름 번역 주석
const {widget_prefix}Checkbox({
  required this.text,       // 버튼 텍스트
  required this.isChecked,  // 체크 여부
  this.onChanged,           // 변경 콜백
});

// After
const {widget_prefix}Checkbox({
  required this.text,
  required this.isChecked,
  this.onChanged,
});
```

공식 스타일 가이드가 중복 회피와 간결성을 함께 권고한다(`AVOID redundancy with the surrounding context`, `PREFER brevity`).
실측 두 번째 카테고리가 이름 번역 주석 약 85건 / 48파일이었다 (1위는 템플릿 마커 약 90건).

**강도:** SHOULD

> **출처:** [Effective Dart: Documentation](https://dart.dev/effective-dart/documentation)

### 3. 주석이 필요하면 이름을 먼저 고친다 `[코어]`

**설명을 붙이지 말고 역할명으로 바꾼다. 자명한 구조 라벨은 경계로 흡수한다.**

```dart
// Before — 이름이 약해서 주석이 붙었다
const red = Color(0xFFE53935);      // 에러 상태에 쓰는 빨강
const surface = Color(0xFFF5F5F5);  // 카드 배경

// After — 주석이 아니라 이름을 고친다
const error = Color(0xFFE53935);
const cardBackground = Color(0xFFF5F5F5);
```

```dart
// Before — 자명한 구조 라벨
Column(
  children: [
    // 제목
    Text(title, style: {TokenClass}.headline),
    // 좌측 영역
    _LeftPane(items: items),
  ],
)

// After — 라벨을 위젯 경계가 대신한다
Column(
  children: [
    _Title(title),
    _LeftPane(items: items),
  ],
)
```

주석을 달아야 이해되는 이름은 이름 자체가 결함이다. 라벨을 남겨두면 이름을 고칠 기회가 사라진다.
자명한 구조 라벨은 실측 약 35건 / 15파일이었다.

**강도:** SHOULD

> **출처:** [Microsoft Code with Engineering Playbook](https://microsoft.github.io/code-with-engineering-playbook/documentation/guidance/code/)

### 4. 템플릿 마커와 구분선 블록은 0개 `[코어]`

**파일마다 기계적으로 반복되는 마커·구분선은 전부 지운다.**

```dart
// Before — 템플릿 마커
class _PanelState extends State<{widget_prefix}Panel> {
  // 상태
  bool _loading = false;

  // 구현부
  Future<void> _load() async {
    setState(() => _loading = true);
  }
}

// After
class _PanelState extends State<{widget_prefix}Panel> {
  bool _loading = false;

  Future<void> _load() async {
    setState(() => _loading = true);
  }
}
```

```dart
// Before — 구분선 블록
// ---------------------------------
// 헬퍼
// ---------------------------------
String _countLabel(int count) => '$count건';

// After — 빈 줄과 함수·파일 분리로 대체
String _countLabel(int count) => '$count건';
```

마커는 파일마다 같은 자리에 같은 문장으로 반복되어 정보량이 0이고, 생성기 흔적으로 읽힌다.
실측에서 템플릿 마커 약 90건 / 48파일, 구분선 블록 약 28건이 나왔고 한 파일에만 14개가 몰린 사례가 있었다.

**강도:** 관측 컨벤션

> **출처:** [Effective Dart: Documentation](https://dart.dev/effective-dart/documentation)

### 5. 보존 대상은 함정·제약·실패 모드 세 가지 `[코어]`

**읽다가 "왜 이렇게 했지?"가 생기는 지점만 기록한다. 아래 두 예시는 지우면 안 되는 주석이다.**

```dart
// Before — 주석까지 같이 지운 결과, 다음 사람이 순서를 되돌린다
_subscription.cancel();
await controller.dispose();

// After — 프레임워크의 비직관적 기본 동작을 남긴다
// dispose 이후에도 리스너가 한 번 더 불리는 구간이 있다. 취소가 먼저여야 한다.
_subscription.cancel();
await controller.dispose();
```

```dart
// Before — 헤더가 왜 필요한지 알 수 없어 다음 리팩토링에서 빠진다
final res = await client.post(uri, headers: {'X-Idem-Key': key});

// After — 외부 API 제약 + 재현된 실패 모드를 남긴다
// 결제 게이트웨이가 재시도 응답에도 200 을 그대로 돌려준다.
// 멱등키 없이 재시도하면 중복 승인이 재현된다.
final res = await client.post(uri, headers: {'X-Idem-Key': key});
```

실무에서 이 조건을 통과하는 것은 대체로 셋이다.

- 프레임워크·런타임의 비직관적 기본 동작
- 외부 API가 강제하는 제약(내부 하드코딩 값, 변경 불가 옵션)
- 재현된 실패 모드(이 구조를 바꾸면 특정 버그가 되살아난다)

사전 카테고리를 미리 늘리지 않는다. 새 유형은 실제로 겪은 뒤에 추가한다.

**강도:** SHOULD

> **출처:** [Kent Beck, Tidy First? — Comments](https://www.oreilly.com/library/view/tidy-first/9781098151232/ch14.html)

### 6. 공개 API는 doc, 구현 이유는 라인 주석 `[코어]`

**공개 API에는 계약을 쓴 doc을, 로컬 구현에는 doc 대신 아무것도 두지 않는다.**

```dart
// Before — 메서드명을 문장으로 옮긴 doc, 로컬 세부에까지 번진 doc
/// 아이템을 로드한다.
Future<List<Item>> loadItems({bool force = false}) => _repo.fetch(force);

/// 캐시 키를 만든다.
String _cacheKey(String id) => 'item:$id';

// After — 계약은 doc, 로컬 세부는 무주석
/// 캐시된 목록을 반환한다.
/// [force] 가 true 면 캐시를 무시하고 네트워크를 호출한다 — 이때 ttl 설정은 무시된다.
Future<List<Item>> loadItems({bool force = false}) => _repo.fetch(force);

String _cacheKey(String id) => 'item:$id';
```

doc이 다루는 것은 계약이다 — 파라미터 의미, 반환값, 오용을 유발하는 규칙(옵션 A를 넘기면 옵션 B가 무시됨 등).
공개 API에 문서 주석을 다는 것은 공식 강제 항목(`DO use /// for public APIs` 계열)이다.
반대로 로컬 구현 세부를 문서 주석으로 감싸지 않는 쪽은 `관측 컨벤션`이라 프로젝트별로 완화할 수 있다.

**강도:** MUST

> **출처:** [Effective Dart: Documentation](https://dart.dev/effective-dart/documentation)

### 7. 주석으로 복잡도를 덮지 않는다 `[코어]`

**해설이 3줄을 넘으면 주석이 아니라 구조를 고친다.**

```dart
// Before — 중첩 삼항을 3줄 해설로 덮는다
// state 가 loading 이면 스피너, error 가 있으면 에러 뷰,
// 데이터가 비어 있으면 빈 화면,
// 그 외에는 목록을 그린다.
final child = isLoading
    ? const Spinner()
    : (error != null ? ErrorView(error) : (items.isEmpty ? const EmptyView() : ItemList(items)));

// After — 분기를 코드 구조로 옮기면 해설이 필요 없다
if (isLoading) return const Spinner();
if (error != null) return ErrorView(error);
if (items.isEmpty) return const EmptyView();
return ItemList(items);
```

긴 해설 주석이 필요하다는 것은 흐름이 이미 인지 한계를 넘었다는 신호다. Cognitive Complexity는 선형 흐름을 깨는 구조마다 가산되고 중첩이 깊을수록 더 커진다.
중첩 삼항은 대표 사례로, 주요 린터가 분해를 권고한다. 삼항은 1단까지만 두고 그 이상은 지역 변수나 별도 함수로 뺀다.

**강도:** SHOULD

> **출처:** [Cognitive Complexity (SonarSource)](https://www.sonarsource.com/resources/cognitive-complexity/)
> **출처:** [ESLint no-nested-ternary](https://archive.eslint.org/docs/rules/no-nested-ternary)

### 8. 주석 정책은 파일이 아니라 카테고리 단위로 통일한다 `[코어]`

**같은 디렉토리·같은 역할의 파일은 같은 주석 밀도를 갖는다.**

```text
Before — 같은 디렉토리인데 정책이 갈린다
  features/order/order_card.dart      주석 0건 (정리 완료)
  features/order/order_tile.dart      템플릿 마커 6건 (미정리)
  features/order/order_header.dart    이름 번역 4건 (미정리)

After — 첫 파일에서 확정한 정책을 형제 파일에 일괄 적용
  features/order/order_card.dart      주석 0건
  features/order/order_tile.dart      주석 0건
  features/order/order_header.dart    실패 모드 1건 (보존 대상)
```

일부 파일만 정리하고 형제 파일을 옛 정책으로 두면 다음 작업자가 어느 쪽을 기준으로 삼을지 모른다.
배치 정리 전에 첫 파일에서 정책을 확정하고 나머지에 일괄 적용한다. 대규모 조직이 언어별 가독성 승인자를 두는 이유도 같은 일관성 문제다.

**강도:** 관측 컨벤션

> **출처:** [Software Engineering at Google — Knowledge Sharing](https://abseil.io/resources/swe-book/html/ch03.html)

### 9. 섹션 라벨과 파일 헤더는 고정 필드만 `[코어]`

**섹션 라벨은 항목 2개 이상일 때만. 헤더는 고정 필드 외 금지.**

```dart
// Before — 항목 1개짜리 섹션 라벨
// 컨트롤러
final scrollController = ScrollController();

// After
final scrollController = ScrollController();
```

```dart
// Before — 계산 근거·자화자찬이 섞인 헤더
// order_card.dart
// AI 기반으로 자동 생성된 고성능 주문 카드
// 카드 높이: 440 - 40 = 400
// 상태
const double cardHeight = 400;

// After — 파일명·설명 한 줄·참고 링크만
// order_card.dart — 주문 목록에서 쓰는 카드.
// 참고: docs/tone/comment-economy.md
const double cardHeight = 400;
```

항목 1개짜리 라벨은 이름과 1:1이라 한쪽이 잉여다.
파일 헤더는 파일명·설명 한 줄·작성자·참고 링크·수정이력 같은 고정 필드로 제한한다. 구현 메모, 계산 근거(`440 - 40`), 자화자찬 문구를 헤더에 섞지 않는다. 클래스 내부에서 정의되는 값은 헤더에 중복 기재하지 않는다.

**강도:** 관측 컨벤션

> **출처:** [Microsoft Code with Engineering Playbook](https://microsoft.github.io/code-with-engineering-playbook/documentation/guidance/code/)

---

## 수치 기준

| 항목 | 값 | 출처 |
|------|-----|------|
| 주석 안티패턴 밀도 | 57파일 / 약 275건 (파일당 약 4.8건) | 코어 실측 |
| 보존 대상 비율 | 약 30건 (전체의 약 11%) | 코어 실측 |
| 최다 유형 1 — 템플릿 마커 | 약 90건 / 48파일 | 코어 실측 |
| 최다 유형 2 — 이름 번역 주석 | 약 85건 / 48파일 | 코어 실측 |
| 구분선 블록 한 파일 최대 | 14개 | 코어 실측 |
| 섹션 라벨 유효 최소 묶음 | 항목 2개 | 코어 실측 |
| 중첩 삼항 허용 깊이 | 1단 | [ESLint](https://archive.eslint.org/docs/rules/no-nested-ternary) |
| 한 줄 길이 선호 | 80자 이하 | [Effective Dart: Style](https://dart.dev/effective-dart/style) |
| 자명한 파라미터 주석 | 0개 | 코어 실측 |

---

## 안티패턴

| 안티패턴 | 문제 |
|----------|------|
| 이름 번역 주석 | 이름이 약하다는 신호를 주석이 가려 이름 개선 기회를 없앤다 |
| 템플릿 마커 (`// 상태`, `// 구현부`) | 파일마다 반복되어 정보량 0, 생성기 흔적으로 읽힌다 |
| 구분선 블록 (`// ----`) | 스크롤 비용만 늘린다. 구조는 함수·파일 분리로 표현할 일 |
| 프레임워크 기본 동작 설명 | 공식 문서 복사본이며 버전이 바뀌면 거짓말이 된다 |
| 자명한 구조 라벨 (`// 제목`) | 바로 아래 코드가 같은 말을 반복한다 |
| 메서드명을 문장으로 옮긴 doc | 계약 정보가 0이라 doc 주석의 목적을 못 채운다 |
| 항목 1개짜리 섹션 라벨 | 라벨과 이름이 1:1이면 한쪽이 잉여 |
| 계산 근거 주석 (`// 440 - 40`) | 값이 바뀌는 순간 거짓이 된다. 계산이 중요하면 코드로 표현 |
| 자화자찬 헤더 ("AI 기반", "자동 생성") | 유지보수 정보 0, 파일 신뢰도만 떨어뜨린다 |
| 전면 문서 주석 적용 | 생성 문서 톤이 로컬 구현까지 번져 소음이 된다 |

---

## 강도·축 라벨

| 라벨 | 뜻 |
|------|-----|
| `MUST` | 공식 스타일 가이드가 강제하는 항목. 프로젝트 재량으로 끄지 않는다 |
| `SHOULD` | 공개 출처의 권고. 근거를 남기면 예외를 둘 수 있다 |
| `관측 컨벤션` | 공개 출처 없이 프로젝트 실측만 근거인 규칙. 준수 강도가 낮다는 뜻이 아니라 근거의 출처가 실측이라는 뜻이다 |
| `[코어]` | 축(규칙이 속한 분류) 라벨. 스택·언어에 무관하게 적용된다 |

---

## Gotchas

- **전면 삭제로 과교정** — 안티패턴 목록만 보고 일괄 삭제하면 보존 대상 약 11%가 같이 날아가고, 새 인원이 프레임워크 함정을 코드만으로 추론해야 한다. 삭제 전에 원칙 5의 세 범주에 걸리는지 먼저 판정하라.
- **탐지 회피를 목표로 삼기** — "AI 티 지우기"를 목적으로 두면 문장이 더 인위적으로 꼬인다. 목표는 읽기 쉬움이고 톤 개선은 부산물이다.
- **주석만 지우고 이름은 그대로** — 번역 주석이 붙어 있었다는 것은 이름이 약했다는 증거다. 주석만 지우면 정보가 순삭되고 다음 사람이 같은 주석을 다시 단다. 원칙 3을 먼저 적용하라.
- **정규식 일괄 치환** — 유형별 패턴은 겹쳐 있어서 한 번에 지우면 계약 doc과 실패 모드 주석까지 매칭된다. 파일 단위로 보존 후보를 먼저 표시한 뒤 나머지를 지운다.
- **한 파일만 정리하고 종료** — 형제 파일이 옛 정책으로 남으면 일관성이 깨진 상태가 새 기준이 된다. 카테고리 전체를 범위로 잡거나 아예 착수하지 마라.
- **주석으로 리팩토링을 대체** — "여기 복잡하니 설명을 달자"는 순간이 함수를 쪼갤 순간이다. 해설이 3줄을 넘으면 구조 문제로 간주하라.
- **삭제 대상과 이동 대상을 혼동** — 정보가 실제로 필요한데 위치가 틀린 경우가 있다. 목적지는 셋이다. 이름으로, 함수 경계로, 아니면 공개 API 계약 doc으로 옮긴다.
