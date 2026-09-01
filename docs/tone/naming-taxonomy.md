---
title: 역할 기반 컴포넌트 네이밍 taxonomy
version: 0.1.0
last_updated: 2026-08-28
---

# 역할 기반 컴포넌트 네이밍 taxonomy

UI 컴포넌트 이름을 외형이 아니라 역할로 짓는 규칙. **접미사 taxonomy 자체는 단일 권위가 없는 합성 규칙이다** — 6개 주요 디자인 시스템의 어휘를 대조해 만든 것이지, 어느 한 시스템이 표준으로 문서화한 것이 아니다. 이 사실을 규칙보다 먼저 밝힌다.

---

## 이 문서의 근거 등급

2026-08-28 조사 결과, Material Design 3 · Apple HIG · MUI · Fluent 2 · Ant Design · IBM Carbon 어느 곳도 `Item`/`Tile`/`Cell`/`Row` 구분이나 `AppBar`/`Toolbar`/`Header`/`Bar` 구분을 **공통 taxonomy 로 문서화하지 않는다.** 각 시스템은 자기 플랫폼 어휘를 쓸 뿐이고 서로 어긋난다.

또한 여섯 시스템 중 어느 곳도 **소비자 앱의 커스텀 컴포넌트 명명 지침**("역할로 이름 지어라")을 발행하지 않는다 (확인 실패). MUI 에 API·prop·CSS 클래스 명명 가이드가 있으나 그것은 라이브러리 내부 규약이다.

따라서 이 문서의 접미사 규칙은 전부 `관측 컨벤션 / 합성` 이며, 디자인 시스템은 **어휘 원천** 으로만 인용한다. 권위로 인용하지 마라.

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

### 1. 이름은 외형이 아니라 역할을 담는다 `[코어]`

**강도:** SHOULD

`BlueRoundedBox` 가 아니라 `ProfileCard` 다. 판단 기준은 "사용자가 이것으로 무엇을 하거나 이해하는가" 이지 "이것이 어떻게 생겼는가" 가 아니다. 색·모서리·크기는 시안이 바뀌면 따라 바뀌므로 이름에 들어가면 이름이 거짓이 된다.

Dart 공식 스타일 가이드는 같은 방향을 문법 층위에서 규정한다: 비-boolean 프로퍼티는 명사구, 부수효과가 있는 메서드는 명령형 동사구, 메서드 이름에 파라미터를 서술하지 않는다.

> **출처:** [Effective Dart: Style](https://dart.dev/effective-dart/style)

### 2. 레이아웃 모양어를 컴포넌트 이름에 쓰지 않는다 `[코어]`

**강도:** 관측 컨벤션 / 합성

`Row` · `Bar` · `Box` 는 레이아웃 용어다. 아래 한정 용법(진짜 표의 행, 확립된 바 종류)에만 허용한다. 세로 리스트의 한 장을 `...Row` 로 부르면 그것이 표의 행인지 세로 목록의 항목인지 이름만으로 구분되지 않는다.

> **출처:** 합성 규칙 — 위 어휘 대조표의 6개 시스템 중 어느 곳도 이 금지를 문서화하지 않는다 (2026-08-28 확인)

### 3. 컬렉션 요소: `Item` / `Tile` / `Cell` / `Row` `[코어]`

**강도:** 관측 컨벤션 / 합성

| 접미사 | 언제 |
|---|---|
| `Item` | UI 형태를 특정하지 않는 일반 데이터 단위. 세로 리스트 한 장의 기본값 |
| `Tile` | leading/trailing 을 가진 고정 높이 리스트 행 |
| `Cell` | 표·그리드의 교차 칸 |
| `Row` | 표의 한 행. 수평 구조가 의미상 본질일 때만 |

**세로 리스트 요소에 `Row`/`Cell` 을 쓰지 마라. 둘은 표 전용이다.** 세로 리스트 한 장은 `Item`, 단순한 행이면 `Tile`, 독립 표면이면 `Card`.

각 시스템의 실제 어휘는 이 구분을 부분적으로만 지지한다. MUI 는 `ListItem`/`TableRow`/`TableCell` 로 갈라 쓰고, Fluent 와 Carbon 은 `List item` 으로 통일하며, Ant 는 `row` 와 `list item` 을 혼용한다.

> **출처:** [MUI ListItem API](https://mui.com/material-ui/api/list-item/) · [Fluent 2 List](https://fluent2.microsoft.design/components/web/react/core/list/usage) — "A list is a collection of like items" · [Carbon List](https://carbondesignsystem.com/components/list/usage/) — "Represents an individual entry within a list"

### 4. 상단·구획: `AppBar` / `Toolbar` / `Header` / `Bar` `[코어]`

**강도:** 관측 컨벤션 / 합성

| 접미사 | 언제 |
|---|---|
| `AppBar` | 화면 최상단 앱 컨테이너 (제목·내비게이션·주요 액션) |
| `Toolbar` | 현재 작업과 관련된 액션 묶음 |
| `Header` | 콘텐츠·섹션·카드의 제목부 또는 시작부 |
| `Bar` | 구체어가 없을 때만 쓰는 포괄 fallback |

**임의의 컨트롤 묶음이나 콘텐츠 상단 구획에 `Bar` 를 쓰지 마라 — `Header` 다.**

시스템별 정의는 이렇게 갈린다.

> **출처:** [MUI AppBar](https://mui.com/material-ui/react-app-bar/) — "The App Bar displays information and actions relating to the current screen." · [Fluent 2 Toolbar](https://fluent2.microsoft.design/components/web/react/core/toolbar/usage) — "A toolbar gives access to frequently used actions" · [Ant Design Layout](https://ant.design/components/layout) — "Header: The top layout" · [Carbon UI shell header](https://carbondesignsystem.com/components/UI-shell-header/usage/) — "Header: The highest level of navigation."

Carbon 의 `Header` 는 최상위 내비게이션이고 Ant 의 `Header` 는 레이아웃 상단이다. 같은 단어가 시스템마다 다른 층위를 가리킨다. 프로젝트가 하나를 골라 고정해야 하는 이유다.

### 5. 표면·구획: `Section` / `Panel` / `Container` / `Card` `[코어]`

**강도:** 관측 컨벤션 / 합성

`Section` 은 의미 구획, `Panel` 은 보조 작업·설정면, `Container` 는 저수준 레이아웃 래퍼, `Card` 는 하나의 객체나 개념을 담는 독립 표면이다.

`Container` · `Box` · `Wrapper` · `View` 는 의미가 약하다. 저수준 유틸이거나 역할이 아직 확정되지 않은 내부 위젯에만 쓴다. 역할이 있으면 역할어를 쓴다.

Carbon 은 이 자리에 `Card` 가 아니라 `Tile` 을 쓰고 "Tiles versus cards" 를 따로 비교한다. 어휘가 시스템에 종속된다는 증거다.

> **출처:** [Carbon Tile](https://carbondesignsystem.com/components/tile/usage/) · [Fluent 2 Card](https://fluent2.microsoft.design/components/web/react/core/card/usage) — "A card is a container" · [Ant Design Card](https://ant.design/components/card) — "A container for displaying information."

### 6. 역할이 겹치면 우선순위로 끊는다 `[코어]`

**강도:** 관측 컨벤션 / 합성

```text
실제 인터랙션  >  컬렉션 요소  >  화면 구획  >  상단 영역
```

탭하면 `Button`, 리스트 한 칸이면 `Item`/`Tile`, 구획이면 `Section`/`Card`, 상단이면 `Header`/`Toolbar`. 리스트 안에 있으면서 탭도 되는 요소는 `Item` 이 아니라 인터랙션이 이기는지 판단해야 하는데, 이 우선순위는 "탭이 그 요소의 존재 이유인가"로 끊는다. 목록을 보여주는 것이 본질이고 탭이 부가면 `Item` 이다.

> **출처:** 합성 규칙 — 6개 시스템 중 우선순위를 문서화한 곳 없음 (2026-08-28 확인)

### 7. fallback 접두사를 이름으로 쓰지 않는다 `[코어]`

**강도:** 관측 컨벤션 (실측 9건 / 4파일)

`effectiveGradient` · `resolvedChildren` · `resolvedBgColor` 같은 이름은 `??` 연산자가 이미 표현한 fallback 을 이름에 중복해 넣은 것이다. 도메인·역할로 바꾼다: `toolbarGradient` · `visibleChildren` · `disabledBackground`.

이 접두사가 LLM 생성 코드에 통계적으로 과대표집된다는 **공개 근거는 없다.** 논문 각주를 붙이지 마라 — 근거는 코퍼스 실측뿐이다.

> **출처:** 프로젝트 실측 (57파일 스캔 중 9건 / 4파일). 공개 통계는 확인 실패 — 상세는 `ai-code-stylometry.md` 원칙 5

### 8. 한 글자 이름과 무역할 파일명을 피한다 `[코어]`

**강도:** SHOULD

`p` · `s` · `e` 같은 축약 대신 `props` · `state` · `event` 를 쓴다. 파일·클래스 이름은 역할이 아니라 도메인으로 짓는다 — `utils.dart` · `helper.dart` · `common_widget.dart` 는 무엇이 들어 있는지 알려주지 않으므로 무한히 자란다.

> **출처:** [Effective Dart: Style](https://dart.dev/effective-dart/style)

### 9. 컴포넌트 이름과 그 데이터 타입 이름을 정렬한다 `[코어][어댑터:dart-flutter]`

**강도:** 관측 컨벤션

추출한 컴포넌트가 `...ItemWidget` 인데 그것이 받는 데이터가 `...RowViewState` 이면 같은 것을 두 이름으로 부르는 셈이다. 같은 도메인 용어로 맞춘다.

> **출처:** 프로젝트 실측 — 컴포넌트/상태 타입 접미사 불일치가 리네이밍 작업의 반복 원인

### 10. prefix 와 suffix 는 프로젝트 파라미터다 `[코어]`

**강도:** 관측 컨벤션

조립 형식은 `{widget_prefix}` + 도메인/대상 + 역할 + `{widget_suffix}` 이고, 클래스는 `UpperCamelCase` · 파일은 `snake_case` 다. `{widget_prefix}`(스코프 구분자)와 `{widget_suffix}`(예: `Widget`)는 **프로젝트마다 다르며 킷이 값을 정하지 않는다.** 감지 규칙은 `project-detection` 이 소유한다.

프로젝트가 접미사를 안 쓰기로 했다면 그것도 유효한 선택이다. 이 문서가 강제하는 것은 접미사의 존재가 아니라 **taxonomy 의 일관성** 이다.

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
| `{widget_prefix}` 를 킷이 고정 | prefix 는 프로젝트 소유 파라미터다. 킷이 값을 정하면 다른 프로젝트에서 전부 오탐이 된다 |

---

## Gotchas

- **taxonomy 를 "업계 표준" 이라고 소개하지 마라** — 조사 결과는 정반대다. 6개 시스템이 상단 영역 하나를 4가지 용어로 부른다. 표준이라고 소개하면 첫 반박에 규칙 전체의 신뢰가 무너진다. "합성이고, 그래서 프로젝트가 하나를 골라 고정한다" 가 정확한 서술이다.
- **`Header` 는 시스템마다 층위가 다르다** — Carbon 에서는 최상위 내비게이션이고 Ant 에서는 레이아웃 상단이다. 외부 문서를 근거로 팀을 설득하려다 오히려 반대 사례를 들려주게 된다. 근거는 "우리 프로젝트 일관성" 이지 외부 권위가 아니다.
- **`Card` 가 없는 시스템이 있다** — Carbon core 에는 card 패턴이 없고 `Tile` 이 그 자리를 대신한다. `Card` 를 보편 어휘로 가정하면 Carbon 기반 프로젝트에서 규칙이 헛돈다.
- **접미사를 바꾸면 파일명·데이터 타입·테스트 경로가 같이 움직인다** — 클래스만 리네임하면 `snake_case` 파일명과 대응 상태 타입이 뒤처진다. 원칙 9와 10을 한 번에 적용하라.
- **우선순위 규칙은 "탭 가능성" 이 아니라 "탭이 존재 이유인가" 로 끊는다** — 리스트 항목은 대부분 탭이 되지만 그렇다고 `Button` 이 아니다. 이 구분을 놓치면 목록 요소가 전부 `...Button` 이 된다.
- **fallback 접두사 규칙에 논문을 붙이고 싶어진다** — AI 코드 탐지 문헌이 identifier 신호를 다루긴 하지만 접두사별 통계는 없다. 각주를 붙이는 순간 검증 불가능한 주장이 된다. 실측 건수만 쓴다.
