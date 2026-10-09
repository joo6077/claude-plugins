# flutter-toolkit 공용 위젯 놀이터와 기본기 검사 — 구현 계획

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** flutter-toolkit 에 `flutter-catalog` 스킬을 더해, 프로젝트의 공용 위젯을 생성자에서 자동으로 읽어 놀이터 화면에 띄우고, 같은 목록으로 기본기 검사(넘침·여백·크기 동작·상태 불변·아이콘 정렬·터치 크기)를 돌린다.

**Architecture:** 킷은 프로젝트에 깔 틀(템플릿) 파일을 제공한다. 프로젝트 쪽에는 `catalog/widgets.yaml`(목록 한 벌) → `tool/catalog_gen.dart`(analyzer 로 생성자 읽기) → `lib/catalog_kit/generated/catalog_entries.g.dart`(항목 + 검사용 메타) 가 생기고, 놀이터 화면(`lib/catalog_kit/*.dart`)과 검사(`test/catalog_kit/*.dart`)가 그 생성물을 읽는다. 놀이터·검사 틀은 Material 만 쓰고 프로젝트 토큰에 기대지 않는다.

**Tech Stack:** Dart 3 / Flutter 3.47 (fvm), `analyzer` 9.x (프로젝트에 딸려 오는 판), `yaml` 3.x, `flutter_hooks`, `flutter_test`.

**Spec:** `docs/superpowers/specs/2026-10-09-flutter-widget-playground-design.md`

## Global Constraints

- 원본 핏팰(`/Users/jackson/Hub/10_Dev/fit-pal`)은 이 계획에서 고치지 않는다. 검증은 복사본 `<scratchpad>/fp/app` 에서만.
- 생성기는 분류 못 한 속성이 있으면 **파일을 쓰지 않고** 종료 코드 1, 걸린 위젯·생성자·속성 이름을 찍는다.
- 목록에 없는 공용 위젯, 목록에만 있는 이름도 종료 코드 1.
- 놀이터는 반드시 앱 패키지 안에서 띄운다(별도 패키지 금지 — 글꼴 경로가 바뀜).
- 놀이터에 코드 칸 없음. 종류는 드롭다운. 기본 보기 폭 390.
- 검사는 경우마다 `testWidgets` 하나(한 테스트에서 여러 번 펌프 금지).
- 검사는 앱 글꼴을 실제로 불러온다. 못 불러오면 실패.
- 킷 문서·커밋 메시지는 한국어, 쉬운 말.
- 버전 매니저: `fvm flutter`, `fvm dart`.

## Review Focus

1. 혼자 못 띄우는 위젯(상태 저장소·번역 필요) → 검사가 「감싸개 필요」를 알려야 한다. 감싸개는 `catalog_kit_host.dart` 의 `wrap()` 하나로 프로젝트가 채운다. Task 4 에서 감싸개 없이 실패하는 경우를 시험.
2. 기본 글자가 빈 문자열인 위젯 → 여백 검사가 글자 상자 0폭으로 엉뚱하게 통과/실패하면 안 된다. 검사는 `samples` 또는 「가나다 ABC」 표본 글자를 넣고 잰다. Task 4.
3. 앱 글꼴 등록 실패 → 대체 글꼴로 재고 통과하면 안 된다. Task 4 에서 글꼴 경로를 망가뜨려 실패 확인.
4. 제네릭·함수 타입·`Key` → `key` 는 건너뛰고, 함수는 고정값, 나머지 미지원은 실패. Task 2 에서 `EdgeInsets` 로 실패 확인.
5. 생성자 여러 개 중 private(`_`)·factory 리다이렉트 → private 은 건너뛰고 factory 는 일반 생성자처럼 다룬다. Task 2.

---

### Task 1: 위젯 기본 규칙 문서

**Files:**
- Create: `flutter-toolkit/references/widget-fundamentals.md`

**Interfaces:**
- Produces: 규칙 번호 1~15 (설계 3.1 표와 같은 번호). 다른 스킬·검사가 「규칙 N」으로 가리킨다.

- [ ] **Step 1:** 설계 3.1 표를 옮기고 규칙마다 「왜(핏팰 실측 한 줄)」「지키는 방법(Flutter 코드 한두 줄)」「검사 이름」을 붙인다. 출처 URL 은 규칙 끝 한 줄.
- [ ] **Step 2:** 아이콘·글자 정렬(규칙 8)은 「측정 뒤 프로젝트가 고른다」로 두고 세 방법과 한계를 적는다. `height: 1` 일반 적용 금지(배지 윗부분 잘림)를 적는다.
- [ ] **Step 3:** `npx markdownlint-cli2 flutter-toolkit/references/widget-fundamentals.md` → MD013 외 0건.
- [ ] **Step 4:** 커밋 `docs(flutter-toolkit): 위젯 기본 규칙 15개`.

### Task 2: 생성기와 목록 파일 틀

**Files:**
- Create: `flutter-toolkit/skills/flutter-catalog/templates/catalog/widgets.yaml`
- Create: `flutter-toolkit/skills/flutter-catalog/templates/tool/catalog_gen.dart`
- Create: `flutter-toolkit/skills/flutter-catalog/templates/lib/catalog_kit/catalog_kit_models.dart`

**Interfaces:**
- Produces (`catalog_kit_models.dart`):
  - `sealed class PlaygroundControl { String key; String label; Object? defaultValue; String typeLabel; String defaultLabel; String doc; }`
  - `ToggleControl`, `TextControl`, `NumberControl(min, max, step, nullable)`, `DropdownControl(options: List<({String label, Object value})>)`, `FixedControl(display)`
  - `enum WidgetSizing { hug, fill }`, `enum PlaygroundView { phone, content }`
  - `class WidgetSpec { String widget; WidgetSizing sizing; double minPadding; PlaygroundView view; List<String> stateKeys; }`
  - `class PlaygroundEntry { String id; String widget; String variant; String variantLabel; String description; WidgetSpec spec; List<PlaygroundControl> controls; Widget Function(BuildContext, Map<String, Object?>) builder; }`
- Produces (생성물): `lib/catalog_kit/generated/catalog_entries.g.dart` 의 `final List<PlaygroundEntry> catalogEntries`.
- `widgets.yaml` 키: `shared_dir`, `widgets[].class|file|sizing|min_padding|view|state_keys|labels|ranges|samples|skip`.

- [ ] **Step 1:** 시제품 `<scratchpad>/fp/app/tool/catalog_gen.dart` 를 바탕으로 일반화한다: 대상 목록을 `widgets.yaml` 에서 읽고, 출력은 위 모델 타입, 기본 생성자 표시 이름은 `labels.new`, 범위는 `ranges`, 예시는 `samples`(Dart 식 원문). 실패 시 쓰기 전에 종료.
- [ ] **Step 2:** `shared_dir` 아래 공개 `Widget` 하위 클래스를 모두 모아 목록·`skip` 과 대조, 빠진 것·없는 것을 실패로.
- [ ] **Step 3 (검증, 복사본):** 복사본에 틀을 깔고 `IFButton`, `IFMiniButton`, `IFBadge`, `IFToggle` 을 목록에 넣어 `fvm dart run tool/catalog_gen.dart` → 종료 0, 항목 수 출력. `fvm dart analyze lib/catalog_kit` 오류 0.
- [ ] **Step 4 (막는지):** (a) `EdgeInsets` 속성을 가진 시험 위젯을 목록에 넣으면 종료 1 + 생성물 파일 시각 안 바뀜, (b) `shared_dir` 을 실제 폴더로 두고 목록을 4개만 두면 종료 1 + 빠진 위젯 이름 출력, (c) 목록에 없는 이름 `NoSuchWidget` → 종료 1.
- [ ] **Step 5:** 커밋 `feat(flutter-toolkit): 생성자를 읽는 카탈로그 생성기 틀`.

### Task 3: 놀이터 화면 틀

**Files:**
- Create: `flutter-toolkit/skills/flutter-catalog/templates/lib/catalog_kit/widget_playground.dart`
- Create: `flutter-toolkit/skills/flutter-catalog/templates/lib/catalog_kit/property_panel.dart`
- Create: `flutter-toolkit/skills/flutter-catalog/templates/lib/catalog_kit/measured_box.dart`

**Interfaces:**
- Consumes: `PlaygroundEntry`, `catalogEntries`.
- Produces: `class CatalogPlayground extends HookWidget { const CatalogPlayground({required List<PlaygroundEntry> entries}); }` — 왼쪽 목록(위젯 단위로 묶음, 작은 미리보기), 가운데 무대(보기 전환·폭·배경·초기화·영역 선), 오른쪽 종류 드롭다운 + 속성.

- [ ] **Step 1:** 시제품 `widget_playground.dart`·`property_editor.dart`(묶음 표)·`components_screen.dart`(목록)를 프로젝트 토큰 없이 `Theme.of(context)` 만 쓰도록 옮긴다. 상태는 `flutter_hooks` 의 `useState` 로 위젯 안에서만 둔다(새 `StatefulWidget`·`setState`·`ValueNotifier` 금지 규칙). 프로젝트에 `flutter_hooks` 가 없으면 스킬이 의존성을 추가하기 전에 사용자에게 묻는다.
- [ ] **Step 2:** 처음 보기는 `spec.view`, 위젯마다 바꾼 보기·값을 기억.
- [ ] **Step 3 (검증, 복사본):** 복사본 카탈로그에 「놀이터」 경로로 `CatalogPlayground(entries: catalogEntries)` 를 붙이고 `fvm flutter build web -t lib/main_catalog.dart --release --pwa-strategy=none`, 새 포트로 띄워 실제 크롬에서: 위젯 바꾸기, 종류 바꾸기, 값 바꾸기·되돌리기, 보기 전환, 크기 숫자 표시를 캡처로 확인. 화면 오류 0.
- [ ] **Step 4:** 커밋 `feat(flutter-toolkit): 놀이터 화면 틀`.

### Task 4: 기본기 검사 틀

**Files:**
- Create: `flutter-toolkit/skills/flutter-catalog/templates/test/catalog_kit/widget_fundamentals_test.dart`
- Create: `flutter-toolkit/skills/flutter-catalog/templates/test/catalog_kit/catalog_kit_host.dart`

**Interfaces:**
- Consumes: `catalogEntries`, `WidgetSpec`.
- Produces: `Widget wrap(Widget child, {required double width, required double textScale, required Locale locale})`, `Future<void> loadAppFonts()` (pubspec 의 `fonts:` 를 읽어 `FontLoader` 로 등록, 하나라도 못 읽으면 예외), 결과 표 `build/widget_fundamentals.csv`.

검사 (경우마다 `testWidgets` 하나):
- 넘침: 폭 320/360/393 × 배율 1.0/1.3/1.6/2.0 × 글자 표본 3가지(짧게 「확인」, 길게 「결제 수단 변경 및 알림 수신 환경 설정」, 띄어쓰기 없이 「AVeryLongUnbrokenLabelWithoutSpaces」). 글자 속성(TextControl)에 표본을 넣는다. `tester.takeException()` 이 null 이어야 함.
- 여백: 배율 1.0, 표본 「가나다 ABC」. 위젯 루트 상자와 그 안 첫 `RichText` 상자의 좌우 거리 ≥ `minPadding`.
- 크기 동작: 폭 한계 390 의 느슨한 자리. `hug` 면 폭 < 389, `fill` 이면 ≥ 389.
- 상태 불변: `stateKeys` 의 참/거짓을 뒤집어 크기 같음(±0.5).
- 아이콘 정렬: 같은 `Row`/`Flex` 의 직계 자식에 `Icon` 과 `Text` 가 같이 있으면 세로 가운데 차이 ≤ 1.0 (줄 상자 기준. 프로젝트가 다른 기준을 고르면 바꿀 자리 하나).
- 터치 크기: 탭 가능한 위젯이면 `meetsGuideline(iOSTapTargetGuideline)` (프로젝트 하한이 44 가 아니면 사용자 지정 크기로).

- [ ] **Step 1:** 틀 작성. 실패 메시지에 위젯·종류·조건·잰 값을 넣는다.
- [ ] **Step 2 (검증, 복사본):** 복사본 감싸개에 `ProviderScope(overrides: catalogSessionOverrides())`, `TranslationProvider`, `AppTheme.dark()` 를 넣고 `fvm flutter test test/catalog_kit` 실행. 기대: `IFButton` 5종 크기 동작(hug 선언 390) 실패, 여백(0) 실패. `IFBadge`·`IFToggle` 통과. 결과를 오늘 실측(390×54 / 33×54)과 대조.
- [ ] **Step 3 (막는지):** (a) 글꼴 경로 하나를 없는 파일로 → `loadAppFonts` 실패, (b) 감싸개에서 `ProviderScope` 를 빼면 상태 저장소를 읽는 위젯이 「감싸개 필요」 메시지로 실패, (c) `IFToggle` 을 `fill` 로 바꾸면 크기 동작 실패.
- [ ] **Step 4:** 커밋 `feat(flutter-toolkit): 공용 위젯 기본기 검사 틀`.

### Task 5: 코드 검사 스크립트

**Files:**
- Create: `flutter-toolkit/skills/flutter-catalog/templates/tool/catalog_lint.dart`

**Interfaces:**
- Produces: `fvm dart run tool/catalog_lint.dart` — `shared_dir` 안에서 (규칙 9) `fontFamily:` 직접 사용(테마 폴더 제외), (규칙 13) `EdgeInsets`·`SizedBox` 의 숫자 중 `widgets.yaml` 의 `spacing_tokens` 에 없는 값. 파일:줄 출력, 있으면 종료 1. `--report` 면 종료 0 으로 표만.

- [ ] **Step 1:** 작성(정규식, 주석 줄 제외).
- [ ] **Step 2 (검증, 복사본):** `spacing_tokens: [2,4,6,8,10,12,14,16,20,24,32,48]` 로 돌려 `if_chip.dart` 의 5.5·7·14.5 와 `if_button.dart` 의 `fontFamily` 가 잡히는지 확인.
- [ ] **Step 3:** 커밋 `feat(flutter-toolkit): 글꼴·여백 숫자 코드 검사`.

### Task 6: `flutter-catalog` 스킬과 기존 스킬 연결

**Files:**
- Create: `flutter-toolkit/skills/flutter-catalog/SKILL.md`
- Modify: `flutter-toolkit/skills/flutter-widget/SKILL.md` (7절 등록 단계), `flutter-extract/SKILL.md`, `flutter-preflight/SKILL.md`, `flutter-audit/SKILL.md`
- Modify: `CLAUDE.md` (flutter-toolkit 표), `flutter-toolkit/README.md` (sync-docs), `flutter-toolkit/evals/evals.json` (케이스 1개)

- [ ] **Step 1:** SKILL.md — Gotchas(별도 패키지 금지, 디버그 서버·서비스 워커, 경우마다 테스트, 글꼴 등록, 시안은 목록 밖), 단계(감지 → 틀 깔기 → 목록 채우기 → 생성 → 검사 → 놀이터 띄우기), 서브커맨드 `init | gen | check | open`.
- [ ] **Step 2:** 기존 스킬 네 곳에 연결 문단(설계 3.7 표대로).
- [ ] **Step 3:** `python3 scripts/sync-docs.py flutter-toolkit`, `python3 scripts/validate-plugin.py flutter-toolkit` 통과.
- [ ] **Step 4:** 커밋 `feat(flutter-toolkit): flutter-catalog 스킬과 연결`.

### Task 7: 아이콘·글자 정렬 기준 측정

**Files:**
- Create (복사본만): `test/catalog_kit/icon_align_probe_test.dart`

- [ ] **Step 1:** KIMM·WantedSans 로 「가」「A」「1」의 줄 상자와 글자 모양 상자(`getBoxesForSelection(boxHeightStyle: tight)`)를 재서 표로.
- [ ] **Step 2:** 같은 아이콘+글자를 (a) 줄 상자 가운데, (b) 기준선, (c) 글자 모양 가운데로 배치한 캡처 3장을 만든다(`RepaintBoundary` PNG).
- [ ] **Step 3:** 결과를 사용자에게 보여 고르게 한다. 고르기 전까지 검사 기본값은 (a), 규칙 문서에 「프로젝트 선택」으로 남긴다.

### Task 8: 마무리

- [ ] 톤 규칙 전수 대조(`tone-kit:tone-guide` 5단계).
- [ ] `harness:qa-evaluator` 로 계약 판정.
- [ ] 푸시, PR(본문에 핏팰 복사본 검증 수치와 캡처 경로).
