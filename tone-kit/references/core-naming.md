# 역할 기반 네이밍 — 운영 규칙

> **근거 등급 경고 (규칙보다 먼저 읽어라).** 이 문서의 접미사 taxonomy 는 **합성 규칙**이다.
> Material Design 3 · Apple HIG · MUI · Fluent 2 · Ant Design · IBM Carbon 여섯 시스템의 어휘를 대조해
> 만든 것이지 어느 한 시스템이 표준으로 발행한 것이 아니다. 여섯 중 상단 영역 어휘가 일치하는 곳은
> 0곳(4가지 용어로 갈린다), 커스텀 컴포넌트 명명 지침을 발행하는 곳도 0곳이다.
> **"업계 표준" 이라고 소개하지 마라.** 유일하게 유효한 근거는 **"이 프로젝트의 일관성"** 이고,
> 디자인 시스템은 어휘 원천으로만 인용한다.

## 목차

1. [규칙표](#1-규칙표)
2. [역할 접미사 taxonomy](#2-역할-접미사-taxonomy)
3. [헷갈리는 구분 3종](#3-헷갈리는-구분-3종)
4. [역할 충돌 우선순위](#4-역할-충돌-우선순위)
5. [이름 조립 형식 — 프로젝트 파라미터](#5-이름-조립-형식--프로젝트-파라미터)
6. [프레임워크 어휘 우선](#6-프레임워크-어휘-우선)
7. [이름 결정 절차 5단계](#7-이름-결정-절차-5단계)
8. [완료 전 대조 grep](#8-완료-전-대조-grep)
9. [어휘 원천](#9-어휘-원천)

---

## 1. 규칙표

강도 3등급: `SHOULD`(외부 스타일 가이드 지지) · `관측 컨벤션`(프로젝트 실측) · `합성`(어휘 대조로 만든 규칙, 단일 권위 없음).

| ID | 규칙 | 강도 | 축 |
| --- | --- | --- | --- |
| N-01 | 이름은 외형이 아니라 역할을 담는다. 색·모서리·크기를 이름에 넣지 않는다 | SHOULD | 역할성 |
| N-02 | 레이아웃 모양어(`Row` · `Bar` · `Box`)는 한정 용법에만 쓴다 | 합성 | 어휘 |
| N-03 | 세로 리스트 요소에 `Row` / `Cell` 을 쓰지 않는다 — 둘은 표 전용 | 합성 | 어휘 |
| N-04 | 임의 컨트롤 묶음·콘텐츠 상단 구획에 `Bar` 를 쓰지 않는다 — `Header` 다 | 합성 | 어휘 |
| N-05 | 역할이 확정됐으면 `Box` · `View` · `Container` · `Wrapper` 를 쓰지 않는다 | 합성 | 어휘 |
| N-06 | 역할이 겹치면 우선순위(§4)로 끊는다 | 합성 | 결정 |
| N-07 | fallback 접두사(`effective*` · `resolved*`)를 이름으로 쓰지 않는다 | 관측 컨벤션 | 식별자 |
| N-08 | 한 글자 이름을 쓰지 않는다 (`p` → `props`, `s` → `state`, `e` → `event`) | SHOULD | 식별자 |
| N-09 | 무역할 파일명(`utils` · `helper` · `common_*`)을 만들지 않는다 | SHOULD | 파일명 |
| N-10 | 컴포넌트 이름과 그것이 받는 데이터 타입 이름을 같은 도메인 용어로 정렬한다 | 관측 컨벤션 | 정렬 |
| N-11 | 조립 형식의 prefix / suffix 는 킷이 아니라 프로젝트가 소유한다 | 관측 컨벤션 | 조립 |
| N-12 | 이벤트·상태 어휘는 프레임워크가 이미 정의했으면 그것을 따른다 — 새로 만들지 않는다 | SHOULD | 어휘 |

N-07 은 **`관측 컨벤션` 이다.** 이 접두사가 LLM 생성 코드에 과대표집된다는 공개 통계는 없다.
논문·연구 각주를 붙이지 마라 — 붙이는 순간 검증 불가능한 주장이 된다. 근거는 코퍼스 실측 건수뿐이다.

---

## 2. 역할 접미사 taxonomy

| 분류 | 접미사 | 언제 쓰는가 |
| --- | --- | --- |
| 인터랙션 | `Button` · `Field` / `Input` · `Switch` · `Checkbox` · `Radio` · `Slider` · `Chip` | 탭·입력·토글·선택·범위 등 직접 조작 |
| 컬렉션 요소 | `Item` · `Tile` · `Cell` · `Row` · `Card` | 컬렉션의 한 단위 — 구분은 §3 (a) |
| 구획·컨테이너 | `List` · `Grid` · `Section` · `Panel` · `Group` · `Container` | 반복 / 2D 배치 / 의미 구획 / 보조면 / 묶음 / 저수준 래퍼 |
| 상단·바 | `AppBar` · `Toolbar` · `NavigationBar` · `Bar` · `Header` · `Footer` | 상단·하단 영역 — 구분은 §3 (b) |
| 오버레이 | `Dialog` · `Modal` · `Sheet` / `BottomSheet` · `Menu` · `Popover` · `Snackbar` | 임시 표면 |
| 표시 | `Badge` · `Avatar` · `Tag` · `Label` | 동적 표식 · 식별 · 토큰 · 이름표 |

접미사의 **존재**를 강제하는 문서가 아니다. 프로젝트가 접미사를 안 쓰기로 했다면 그것도 유효한 선택이고,
강제하는 것은 **taxonomy 의 일관성** — 한 프로젝트 안에서 같은 역할이 항상 같은 단어로 불리는가 — 하나다.

---

## 3. 헷갈리는 구분 3종

### (a) `Item` / `Tile` / `Cell` / `Row` / `Card`

| 접미사 | 판정 기준 |
| --- | --- |
| `Item` | UI 형태를 특정하지 않는 일반 데이터 단위. **세로 리스트 한 장의 기본값** |
| `Tile` | leading / trailing 을 가진 고정 높이 리스트 행 |
| `Cell` | 표·그리드의 교차 칸 |
| `Row` | 표의 한 행. 수평 구조가 의미상 본질일 때만 |
| `Card` | 하나의 객체·개념을 담는 독립 표면 |

**세로 리스트 요소에 `Row` / `Cell` 금지 (N-03).** 지금 표가 없어도 나중에 진짜 표가 생기면 이름이 충돌한다.
Carbon 은 이 자리에 `Card` 대신 `Tile` 을 쓴다 — `Card` 를 보편 어휘로 가정하지 마라.

### (b) `AppBar` / `Toolbar` / `Header` / `Bar`

| 접미사 | 판정 기준 |
| --- | --- |
| `AppBar` | 화면 최상단 앱 컨테이너 (제목 · 내비게이션 · 주요 액션) |
| `Toolbar` | 현재 작업과 관련된 액션 묶음 |
| `Header` | 콘텐츠 · 섹션 · 카드의 제목부 또는 시작부 |
| `Bar` | 구체어가 없을 때만 쓰는 포괄 fallback |

**임의 컨트롤 묶음·콘텐츠 상단 구획에 `Bar` 금지 (N-04) — `Header` 다.**
`Header` 는 시스템마다 층위가 다르다(Carbon 은 최상위 내비게이션, Ant 는 레이아웃 상단).
외부 문서를 근거로 팀을 설득하려 들면 반대 사례를 스스로 들려주게 된다.

### (c) `Section` / `Panel` / `Container` / `Card`

| 접미사 | 판정 기준 |
| --- | --- |
| `Section` | 의미 구획 |
| `Panel` | 보조 작업 · 설정면 |
| `Container` | 저수준 레이아웃 래퍼 |
| `Card` | 하나의 객체 · 개념을 담는 독립 표면 |

`Container` · `Box` · `Wrapper` · `View` 는 의미가 약하다. 저수준 유틸이거나 역할이 아직 확정되지 않은
내부 컴포넌트에만 허용한다 (N-05).

---

## 4. 역할 충돌 우선순위

```text
실제 인터랙션  >  컬렉션 요소  >  화면 구획  >  상단 영역
```

탭하면 `Button`, 리스트 한 칸이면 `Item` / `Tile`, 구획이면 `Section` / `Card`, 상단이면 `Header` / `Toolbar`.

**판정 기준은 "탭 가능한가" 가 아니라 "탭이 이 요소의 존재 이유인가" 다.**
리스트 항목은 대부분 탭이 되지만 그렇다고 `Button` 이 아니다. 목록을 보여주는 것이 본질이고 탭이 부가면 `Item` 이다.
이 구분을 놓치면 목록 요소가 전부 `...Button` 이 된다.

---

## 5. 이름 조립 형식 — 프로젝트 파라미터

```text
{widget_prefix} + 도메인/대상 + 역할 + {widget_suffix}
```

클래스는 `UpperCamelCase`, 파일은 `snake_case` 로 대응시킨다.

**`{widget_prefix}`(스코프 구분자)와 `{widget_suffix}`(예: `Widget`)의 값은 킷이 정하지 않는다.**
두 값은 프로젝트마다 다르며 감지·확인 규칙은 같은 킷의 `project-detection.md` 가 소유한다. 킷이 값을
고정하면 다른 프로젝트에서 이 문서의 모든 판정이 오탐이 된다. prefix / suffix 를 안 쓰는 프로젝트는
두 자리가 빈 문자열이고 나머지 규칙은 그대로 적용된다.

접미사를 바꾸면 클래스명만 움직이지 않는다 — 파일명 · 대응 데이터 타입 · 테스트 경로가 같이 움직이므로 N-10 과 N-11 을 한 번에 적용하라.

---

## 6. 프레임워크 어휘 우선

**N-12 · SHOULD · 어휘 축**

이 문서의 접미사 taxonomy 는 프레임워크가 어휘를 정해 두지 **않은** 자리를 메우는 합성 규칙이다. 프레임워크가 이미 이름을 정한 개념에는 그 이름을 쓴다. 킷의 taxonomy 가 공식 어휘를 덮지 않는다.

### 우선순위

```text
프레임워크 공식 어휘  >  프로젝트 관례  >  새로 만든 말
```

- 대응하는 공식 콜백·상태 이름이 있으면 **그 이름과 단계 구분을 그대로** 쓴다.
- 공식 어휘에 없는 **도메인 이벤트만** 프로젝트가 이름 짓는다.
- 같은 개념에 두 어휘를 섞지 않는다.

### 왜

공식 어휘는 이미 단계를 갈라 놨는데 자체 어휘가 그걸 도로 합치는 일이 생긴다. 이름 하나가 두 개념을 덮으면 호출부에서 어느 쪽인지 알 수 없고, 문서·자동완성·검색이 전부 공식 이름 기준으로 움직이므로 자체 어휘는 그 경로에서 빠진다.

이 규칙은 로케일 축의 "공식 API 이름은 번역하지 않는다" 와 같은 원리다. 주석에서 공식 이름을 지키면서 코드에서 자체 어휘를 만드는 것은 앞뒤가 맞지 않는다.

### before / after

```text
// before — 자체 어휘. 어느 제스처의 어느 단계인지 이름에서 안 갈린다
handlePressStart()
handlePressEnd()

// after — 공식 어휘. 제스처와 단계가 이름에 있다
onTapDown()          // 또는 onLongPressStart() — 어느 제스처인지 확정해서
onTapUp()            // 또는 onLongPressEnd()
```

```text
// before — 같은 개념에 두 어휘가 섞였다
{widget_prefix}EventServerSelectTap
{widget_prefix}EventServerSelected

// after — 하나로 고정
{widget_prefix}EventServerSelected
```

### 적용 범위

공식 어휘가 없는 도메인 이벤트는 이 규칙 대상이 아니다. 아래는 정당하다.

```text
onPairingModeEntered
onLightStickMounted
onLibraryDownloadCancel
```

스택별 공식 어휘 목록은 어댑터가 소유한다 — Dart/Flutter 는 `adapter-dart-flutter.md`.

> **출처:** 프레임워크 API 표면 — 대상 스택의 공식 이벤트 어휘. 강도가 `SHOULD` 인 이유는 공식 문서가 "소비자 코드도 이 이름을 쓰라" 고 명시하지는 않기 때문이다. 근거는 어휘가 실재한다는 사실이지 지침 문장이 아니다.

## 7. 이름 결정 절차 5단계

**0단계 — 프레임워크가 이미 이름을 정했는가?** 정했으면 그것을 쓰고 아래 절차를 건너뛴다 (N-12).

1. **역할을 한 단어로 판정한다.** 탭·입력인가 / 리스트 한 칸인가 / 구획인가 / 표면인가 / 상단인가 / 표인가 / 오버레이인가.
2. **§2 taxonomy 에서 접미사를 고른다.** 역할이 둘 이상 겹치면 §4 우선순위로 끊는다.
3. **§5 형식으로 조립한다.** prefix / suffix 는 `project-detection.md` 감지값을 쓴다. 파일명은 클래스명의 `snake_case` 대응으로 만든다.
4. **기존 이름에 모양어가 있으면 교체한다.** 비-표 `Row` / `Cell` → `Item` / `Tile` / `Card`, 임의 `Bar` → `Header` / `Toolbar`, 역할 확정된 `Box` / `View` / `Container` / `Wrapper` → 역할어.
5. **데이터 타입 이름을 정렬한다.** 컴포넌트가 `...Item` 이면 그것이 받는 상태·Props 타입도 `...Item...` 이다. `...Item` 컴포넌트에 `...Row` 상태 타입을 물리면 같은 것을 두 이름으로 부르게 되고 검색이 한쪽만 잡는다.

---

## 8. 완료 전 대조 grep

아래 블록은 `bash` · `zsh` 양쪽에서 실행 검증했다. `SRC` 와 `INC` 를 프로젝트 값으로 바꿔 쓴다.
매치 0건이면 grep 종료 코드가 1 이다 — 실패가 아니라 통과다.

```bash
SRC=src                # 소스 루트 — 프로젝트 값으로 교체
INC="--include=*.dart" # 대상 확장자 — 프로젝트 값으로 교체
```

| ID | 대응 규칙 | 명령 |
| --- | --- | --- |
| G-1 | N-07 | `grep -rnE '\b(effective\|resolved)[A-Z]' "$SRC" $INC` |
| G-2 | N-03 | `grep -rnE 'class [A-Za-z]*(Row\|Cell)[A-Za-z]*' "$SRC" $INC` |
| G-3 | N-04 | 아래 블록 |
| G-4 | N-05 | 아래 블록 |
| G-5 | N-01 | `grep -rnE 'class [A-Za-z]*(Blue\|Red\|Green\|Yellow\|Gray\|Grey\|Rounded\|Circle\|Square\|Big\|Small\|Large\|Thin\|Thick)[A-Z]' "$SRC" $INC` |
| G-6 | N-08 | `grep -rnE '\b(final\|const\|var\|let)\s+[a-z]\s*=' "$SRC" $INC \| grep -vE 'for \('` |
| G-7 | N-09 | `find "$SRC" -type f \( -name 'utils.*' -o -name 'helper*' -o -name 'common_*' \)` |
| G-8 | N-10 | 아래 블록 |

```bash
# G-3 — 확립된 바 종류를 제외한 나머지 Bar. 남은 건 전부 Header/Toolbar 후보다.
grep -rnE 'class [A-Za-z]+Bar[A-Za-z]*' "$SRC" $INC \
  | grep -vE '(AppBar|Toolbar|ToolBar|NavigationBar|SnackBar|TabBar|StatusBar|SearchBar|ProgressBar|ScrollBar|SideBar|TitleBar|BottomBar)'

# G-4 — 의미 약한 접미사. 확립된 합성어는 제외한다.
grep -rnE 'class [A-Za-z]+(Box|View|Container|Wrapper)[A-Za-z]*' "$SRC" $INC \
  | grep -vE '(MessageBox|CheckBox|Checkbox|ComboBox|TextBox|ListView|GridView|PageView|WebView|ScrollView)'

# G-8 — 같은 도메인 어간이 두 개 이상의 역할어로 불리는 경우를 뽑는다.
grep -rhoE '[A-Za-z]+(Item|Tile|Cell|Row|Card)' "$SRC" $INC \
  | sed -E 's/(Item|Tile|Cell|Row|Card)$/ &/' \
  | sort -u \
  | awk '{c[$1]=c[$1]" "$2} END{for(k in c) if(split(c[k],a," ")>1) print k" ->"c[k]}'
```

### 오탐 triage

grep 결과는 위반 후보이지 위반 판정이 아니다. 아래는 **정당한 매치**이므로 세지 않는다.

- G-2 — 진짜 표의 행·칸(`...TableBodyCell` · `...HourlyStatsRow`)은 정당하다. 세로 리스트의 한 장만 위반이다.
- G-4 — `MessageBox` 처럼 `Box` 가 확립된 오버레이 합성어의 일부인 경우는 위반이 아니다. 제외 목록에 없는 도메인 합성어를 만나면 목록에 추가하지 말고 그 자리에서 판정하라.
- G-6 — `catch (e)` 와 for 루프 인덱스 `i` 는 관용이다. 파이프의 `grep -vE 'for \('` 가 후자를 걸러내지만 전자는 육안 판정이 필요하다.
- G-7 — `common_` 으로 시작하지만 도메인이 이름에 있는 파일(`common_preset_provider`)은 무역할 파일명이 아니다. 도메인 없는 `common_widget` 류만 위반이다.
- G-8 — `Table -> Cell Row` 처럼 표가 셀과 행을 동시에 갖는 경우는 정당하다. 같은 대상이 두 역할어로 불릴 때만 위반이다.

## 9. 어휘 원천

권위가 아니라 **어휘 존재 확인용**이다. 여섯 시스템이 서로 어긋난다는 사실 자체가 §1 경고의 근거다.

- 문법·casing 층위의 유일한 외부 지지: [Effective Dart: Style](https://dart.dev/effective-dart/style)
- 컬렉션 요소 어휘: [MUI ListItem API](https://mui.com/material-ui/api/list-item/) · [Fluent 2 List](https://fluent2.microsoft.design/components/web/react/core/list/usage) · [Carbon List](https://carbondesignsystem.com/components/list/usage/)
- 상단 영역 어휘: [MUI AppBar](https://mui.com/material-ui/react-app-bar/) · [Fluent 2 Toolbar](https://fluent2.microsoft.design/components/web/react/core/toolbar/usage) · [Ant Design Layout](https://ant.design/components/layout) · [Carbon UI shell header](https://carbondesignsystem.com/components/UI-shell-header/usage/)
- 표면 어휘: [Carbon Tile](https://carbondesignsystem.com/components/tile/usage/) · [Fluent 2 Card](https://fluent2.microsoft.design/components/web/react/core/card/usage) · [Ant Design Card](https://ant.design/components/card)
- 어휘 존재만 확인 가능(본문이 JS 렌더링이라 문구 인용 불가): [M3 components](https://m3.material.io/components) · [Apple HIG components](https://developer.apple.com/design/human-interface-guidelines/components)
