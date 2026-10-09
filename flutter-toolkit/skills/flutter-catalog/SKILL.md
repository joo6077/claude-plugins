---
name: flutter-catalog
description: >
  앱의 진짜 공용 위젯을 생성자에서 자동으로 읽어 놀이터 화면과 기본기 검사를 만든다.
  위젯 목록 파일(catalog/widgets.yaml)이 기준이고, 목록에 빠진 위젯 · 조절 못 하는 속성이 있으면 생성이 실패한다.
  놀이터는 왼쪽 위젯 목록 · 가운데 실제 위젯(휴대폰 화면 / 내용 크기 보기, 영역 선과 크기 숫자) · 오른쪽 종류 고르기와 속성 한 줄씩.
  기본기 검사는 넘침 · 안쪽 여백 · 크기 동작 · 상태 불변 · 아이콘 정렬 · 터치 크기 · 글꼴 등록을 실제로 띄워 잰다.
  "공용 위젯 카탈로그", "위젯 놀이터", "위젯 목록 화면", "속성 바꿔 보기", "위젯북 대신",
  "위젯 기본기 검사", "넘침 검사", "여백 검사", "catalog", "playground" 같은 요청 시 트리거.
argument-hint: "[init | gen | check | open]"
user-invocable: true
---

<!-- markdownlint-disable MD041 -->

## Gotchas

<!-- markdownlint-enable MD041 -->

- **위젯북처럼 별도 패키지에 놀이터를 두지 마라.** 별도 패키지는 앱 글꼴 이름이 `packages/<앱>/KIMM` 으로 바뀌어 앱 글꼴이 아니라 기본 글꼴로 그린다. 놀이터는 앱 안 진입 파일(`lib/main_catalog_kit.dart`)로 띄워 앱과 같은 글꼴 · 테마를 쓴다 (2026-10-08 핏팰 위젯북 4판 비교에서 확인).
- **웹으로 띄워 사용자에게 보일 때는 `--pwa-strategy=none` 으로 배포용 빌드를 하고 매번 새 포트를 써라.** 배포용 빌드는 서비스 워커가 옛 화면을 붙잡아 고친 판이 안 보이고, 디버그 웹 서버는 사용자 탭에서 멈춘다. 「안 보인다」 는 말을 들으면 새로고침을 시키지 말고 이 둘부터 의심한다.
- **기본기 검사는 `testWidgets` 하나에 경우 하나다.** 한 시험에서 여러 번 띄우면 넘침 예외가 앞 경우에 겹쳐 붙어 결과가 흔들린다. 시험 수가 천 개를 넘어도 묶지 마라 — 결과 표가 경우별로 남는 것이 목적이다.
- **글꼴 등록을 먼저 본다.** 시험은 기본으로 시험 글꼴로 글자 폭을 재서 넘침이 실제와 다르게 나온다. 시험 틀이 pubspec 글꼴을 실제로 불러오고, `글꼴` 검사가 테마의 모든 글자 단계가 쓰는 글꼴이 등록됐는지 잰다. 이 검사가 실패하면 나머지 넘침 결과를 믿지 마라.
- **흉내 낸 시안 카드는 목록에 넣지 마라.** 앱 위젯을 쓰지 않고 모양만 따라 그린 카드(예: 「Submit Disabled A」)는 진짜 위젯과 따로 낡아 같은 이름으로 다른 것을 보여 준다. 목록에는 앱이 실제로 쓰는 클래스만 넣는다.
- 그리기가 실패하고 결과 표 `measured` 에 「감싸개」 가 보이면 위젯 탓이 아니다 — 위젯이 상태 저장소 · 번역을 찾는데 `test/catalog_kit/catalog_kit_host.dart` 에 없다. 감싸개에 붙이고 다시 돌린다.

## 무엇을 만드나

프로젝트 안에 깔리는 파일이다. 틀은 이 스킬 폴더 `templates/` 에 있고 `scripts/install.sh` 가 깐다.

| 파일 | 하는 일 |
| --- | --- |
| `catalog/widgets.yaml` | 올릴 위젯 목록과 위젯마다 크기 동작 · 최소 안쪽 여백 · 첫 보기 · 상태 속성 · 예시 값 |
| `tool/catalog_gen.dart` | `analyzer` 로 목록 위젯의 생성자를 읽어 `lib/catalog_kit/generated/catalog_entries.g.dart` 를 만든다 |
| `tool/catalog_lint.dart` | 토큰 밖 여백 숫자와 직접 쓴 글꼴 이름을 찾는다 |
| `lib/catalog_kit/` | 놀이터 화면(`CatalogPlayground`) · 속성 칸 · 크기 재는 틀 · 항목 모델(`PlaygroundEntry`) · 놀이터 감싸개 |
| `lib/main_catalog_kit.dart` | 놀이터 진입 파일 |
| `test/catalog_kit/` | 기본기 검사와 시험 감싸개 |

규칙과 검사 기준은 `../../references/widget-fundamentals.md` 가 기준이다. 여기서 다시 적지 않는다.

## Process

### `init` — 깔기

1. 프로젝트가 `flutter_hooks` 를 직접 의존하는지 본다. 놀이터 화면이 쓴다.
2. `bash <이 스킬 폴더>/scripts/install.sh --add-deps <프로젝트>` 를 돌린다. 깔 파일이 하나라도 이미 있으면 아무것도 쓰지 않고 1 로 끝난다 — 지우거나 옮긴 뒤 다시 돌린다. `--add-deps` 는 `analyzer` · `yaml` 이 직접 의존성에 없을 때만 잠긴 판 그대로 개발 의존성에 넣는다.
3. 두 감싸개를 앱에 맞게 고친다 — `test/catalog_kit/catalog_kit_host.dart` (`hostLocales` · `setUpHost` · `wrap`), `lib/catalog_kit/catalog_kit_app_host.dart` (`appWrap`). 앱 테마 · 상태 저장소 · 번역을 붙인다.
4. `catalog/widgets.yaml` 에 `shared_dir` 와 위젯을 적는다. 칸 설명은 그 파일 주석에 있다.

### `gen` — 항목 만들기

`fvm dart run tool/catalog_gen.dart`. 생성자를 읽어 매개변수마다 조절 칸을 붙인다 — 참거짓은 스위치, 글자와 `Widget` 은 글 입력(`Widget` 은 `Text` 로 감싼다), 숫자는 미끄럼 막대, enum · 색 · 아이콘은 고르기, 함수는 빈 함수로 고정. 아래면 무엇이 걸렸는지 찍고 1 로 끝나며 생성물을 쓰지 않는다.

- 조절할 방법이 없는 타입 (`EdgeInsetsGeometry` 등) — `samples.<속성>` 에 Dart 식 예시 값을 적는다
- `shared_dir` 안 화면 위젯(`StatelessWidget` · `StatefulWidget` 후손, `InheritedWidget` 제외)이 목록에 없음
- 목록에 있는데 코드에 없는 클래스

공용 위젯을 새로 만들거나 생성자를 바꾸면 매번 다시 돌린다. 생성물은 손으로 고치지 않는다.

### `check` — 기본기 검사와 코드 검사

1. `fvm flutter test test/catalog_kit/widget_fundamentals_test.dart` — 결과 표는 `build/widget_fundamentals.csv` (머리말 `widget,variant,check,case,result,measured`). 실패한 경우만 보려면 `result` 가 `FAIL` 인 줄을 거른다.
2. `fvm dart run tool/catalog_lint.dart` — 위반 한 건에 한 줄 `<경로>:<줄>: <규칙> <값>`. 기존 위반을 한 번에 다 못 고치면 `--report` 로 찍기만 한다.
3. 실패를 보고할 때 결과 표 줄을 그대로 인용하고, 규칙 번호를 `widget-fundamentals.md` 표에서 찾아 붙인다.

### `open` — 놀이터 띄우기

- 기기 · 시뮬레이터: `fvm flutter run -t lib/main_catalog_kit.dart`
- 웹으로 사용자에게 보일 때: `fvm flutter build web -t lib/main_catalog_kit.dart --release --pwa-strategy=none` 뒤 `build/web` 을 새 포트로 정적 서버에 올린다. 진입 파일이 접근성 트리를 켜 두어 브라우저 자동 점검이 화면 글자를 읽을 수 있다.
- 띄운 뒤 직접 본다 — 왼쪽 목록에서 위젯을 누르고, 오른쪽 위 「종류」 에서 생성자를 바꾸고, 속성을 바꿔 「기본값으로」 가 생기는지, 「휴대폰 화면」 · 「내용 크기」 보기에서 영역 선과 크기 숫자가 맞는지.

## 다른 스킬과의 연결

- `/flutter-widget` — 새 공용 위젯을 만들면 `catalog/widgets.yaml` 에 항목을 넣고 `gen` · `check` 를 돌린다
- `/flutter-extract` — 공용으로 뽑아낸 위젯도 같다
- `/flutter-preflight` — 커밋 전 묶음에 `gen` 과 `check` 를 넣는다
- `/flutter-audit` — 결과 표의 `FAIL` 줄을 감사 근거로 쓴다

## References

- `../../references/widget-fundamentals.md` — 규칙 15 개 · 검사 기준 · 코드 검사
- `templates/catalog/widgets.yaml` — 목록 파일 칸 설명
- `scripts/install.sh` — 깔기
