# Primitive Substitution Gate

> **SSOT.** 이 파일이 "Flutter 기본 위젯 대신 프로젝트 디자인 시스템 컴포넌트를 써야 하는가" 를
> 판정하는 유일한 정의다. `flutter-widget` · `flutter-screen` · `flutter-audit` · `widget-inspector`
> 는 이 파일을 **인용만** 하고 아래 목록을 자기 문서에 복제하지 않는다.
>
> **현재 등급: E2** (`harness/docs/guides/skill-design-guide.md` §3.7 Enforcement 3 등급).
> 문장 규칙(E1)만으로는 재발했다 — 아래 §왜 E2 인가 참조. 이 게이트는 **대체 후보 표**라는
> 아티팩트를 남기게 한다.

## 왜 이 게이트가 있는가

실측 REJECT (2026-08-12 · fit-pal):

> `RE-02`: B5(클러스터 묶음) 구분선이 Flutter 기본 `Divider` 사용, 기존 `IFDivider` 컴포넌트 미재사용

`flutter-widget` 은 이미 §Enumerate-before-Act (디자인 **토큰** 전수 나열)와 "기존 위젯 수정이
기본값" 조항을 갖고 있었다. 그런데도 재발한 이유는 두 조항 모두 **"프로젝트 위젯을 고칠 때"** 를
전제하고, **"Flutter 기본 위젯을 새로 꺼내 쓸 때"** 를 막지 않기 때문이다. `Divider` 는 토큰이
아니고 기존 위젯 수정도 아니다 — 규칙 사이의 빈틈으로 빠져나간다.

공식 Flutter Agent Plugins 도 agent mistake 감축의 1 차 기법을 "skills/rules 로 반복 가능한
워크플로우를 주입" 으로 제시한다. 즉 이것은 프레임워크 API 문제가 아니라 **강제 절차** 문제다
(출처: <https://github.com/flutter/agent-plugins>).

## 적용 조건

`HAS_DS = true` (`references/project-detection.md` 감지 결과) 일 때만 발동한다.
디자인 시스템이 없는 프로젝트에 이 게이트를 걸면 대체 후보가 존재하지 않아 노이즈만 생긴다.

## 게이트 대상 — 의미 있는 UI 위젯 8 종

아래 Flutter 기본 위젯을 **새로 작성하는 코드에 넣기 전에** 프로젝트 컴포넌트를 먼저 검색한다.

| 기본 위젯 | 흔한 DS 대체물 |
| --- | --- |
| `Divider` | 프로젝트 구분선 컴포넌트 |
| `Button` 계열 (`ElevatedButton` · `TextButton` · `OutlinedButton` · `IconButton`) | 프로젝트 버튼 컴포넌트 |
| `Chip` 계열 | 프로젝트 태그/칩 컴포넌트 |
| `Card` | 프로젝트 카드/서피스 컴포넌트 |
| `ListTile` | 프로젝트 리스트 아이템 컴포넌트 |
| `Switch` | 프로젝트 토글 컴포넌트 |
| `TextField` / `TextFormField` | 프로젝트 입력 컴포넌트 |
| `CircularProgressIndicator` / `LinearProgressIndicator` | 프로젝트 로딩/스켈레톤 컴포넌트 |

## 게이트 대상이 **아닌** layout primitive — 금지하지 않는다

`Text` · `Row` · `Column` · `Padding` · `SizedBox` 같은 layout primitive 는 **이 게이트의 대상이
아니다.** 이들까지 금지하면 과잉 규칙이 되어 게이트가 통째로 무시된다 — 우회된 게이트는 없는
게이트보다 나쁘다. `Stack` · `Expanded` · `Flexible` · `Align` · `Center` · `Spacer` 도 같다.

예외 하나: 프로젝트가 `Text` 를 감싸는 타이포 컴포넌트(예: `AppText`)를 **이미 전면 사용 중**이라
`Text(` 직접 호출이 코드베이스에 사실상 없으면, 그때만 프로젝트 관습을 따른다. 그 판정은 이
게이트가 아니라 기존 코드 관찰로 한다.

## 절차

### quick 검색 (생성 스킬 — `flutter-widget` · `flutter-screen`)

생성 시간을 늘리지 않도록 대상 위젯 **한 종에 대해서만** 1 회 검색한다.

```bash
# 예: Divider 를 쓰려 한다
rg -n "class .*Divider|Divider\(" lib/ --glob '!**/*.g.dart' | head -20
```

검색 경로 우선순위: `lib/**/design_system` → `lib/**/components` → `lib/**/widgets` → `lib/**/ui`.

### deep 검색 (`flutter-audit` deep 모드 · `widget-inspector` deep 모드)

변경 파일 전체를 훑어 게이트 대상 8 종의 직접 사용을 열거하고, 각 사용처마다 DS 대체 후보가
실재하는지 확인한다.

```bash
# 게이트 대상 직접 사용 열거 (zsh · bash 동일)
grep -rnE '\b(Divider|ElevatedButton|TextButton|OutlinedButton|IconButton|Chip|Card|ListTile|Switch|TextField|TextFormField|CircularProgressIndicator|LinearProgressIndicator)\(' \
  lib/ --include='*.dart' | grep -v '\.g\.dart:'
```

**0 매치 판정** — 대상 `.dart` 파일 수를 먼저 세고(예: `42 개`), 그 패턴이 알려진 위치에서 최소
1 회 매치한다는 것을 확인한 뒤의 0 만 "위반 없음" 이다. 경로가 틀려서 나온 0 은 `[미검증]` 이다.

## E2 아티팩트 — 대체 후보 표

게이트가 발동하면 아래 표를 **응답에 채워서** 남긴다. 채우지 않고 진행하지 않는다.

```text
## Primitive Substitution Gate
검색 경로: <실제로 검색한 경로>
| 사용하려는 기본 위젯 | 검색 명령 | DS 후보 | 결정 |
| --- | --- | --- | --- |
| Divider | rg -n "Divider" lib/ | IFDivider (lib/design_system/…) | IFDivider 사용 |
| Card    | rg -n "Card" lib/    | 없음                          | 기본 Card 사용 (근거: DS 미제공) |
```

- **후보가 있는데 기본 위젯을 쓰려면 근거 한 줄이 필수다.** "스타일이 달라서" 는 근거가 아니다 —
  DS 컴포넌트의 파라미터로 표현 가능한지 먼저 소스를 읽는다.
- **후보가 없으면 "없음" 이라고 적고 진행한다.** 게이트는 기본 위젯 사용을 금지하는 것이 아니라
  **검색 없이 쓰는 것**을 금지한다.

## 왜 E2 인가 (등급 근거)

`skill-design-guide.md` §3.7 승급 규칙: **같은 위반이 2 회 이상 재발하면 E1 → E2**. 기존 E1 조항
(§Enumerate-before-Act · "기존 위젯 수정이 기본값")이 있는 상태에서 `RE-02` 가 발생했으므로 문장을
또 다듬지 않고 아티팩트를 남기는 등급으로 올린다. 표 없이 완료 선언이 반복되면 다음 사이클에
게이트 대상 grep 을 실행하는 E3 스크립트로 승급한다.
