---
feature: "flutter-toolkit 공용 위젯 놀이터와 기본기 검사"
slug: flutter-catalog
created: "2026-10-09 13:38"
complexity: "복잡"
conditions: 31
status: active
owner_session: 85aff6fc-39c9-4668-852b-7307fe63e954
conditions_digest: sha256:c3c81b07c9108d77
measurement_digest: sha256:433e47f4c1d51cf6
locked_at: "2026-10-09 14:03"
---

## 배경

- 설계: `docs/superpowers/specs/2026-10-09-flutter-widget-playground-design.md`, 계획: `docs/superpowers/plans/2026-10-09-flutter-widget-playground.md`.
- 사용자 요구(2026-10-08~09 대화): 진짜 위젯으로 값을 바꿔 보는 놀이터(코드 칸 없음, 종류는 드롭다운, 뒤로 가기 없는 왼쪽 목록), 위젯 기본기(안쪽 여백 · 크기 동작 · 아이콘 정렬 · 넘침)를 자동으로 막기. 사용자가 「끝까지 진행해」 라고 했다.
- 시험 대상은 핏팰 **복사본**이다. 측정 묶음 `.harness/.meta/flutter-catalog/measure.sh` 가 원본 `/Users/jackson/Hub/10_Dev/fit-pal/app` 을 새로 복사하고(`setup`), 그 안에서만 쓴다. 원본은 읽기만 한다. 판정 사례는 끝 줄에 `VERDICT PASS` 또는 `VERDICT FAIL <사유>` 를 찍는다.
- 측정 순서: `setup` → `gen-ok` · `gen-unsupported` · `gen-missing` · `gen-unknown` · `analyze` · `analyze-pos` · `lint` · `install` · `tmpl-hosts` · `font` → `fund-run`(판정 아님, 결과 표를 만든다. `IFButton` 처럼 원래 실패하는 시험이 있어 종료 코드가 0 이 아닌 것이 정상) → `sizing` · `overflow` · `icon-touch` · `wrapper` → `web`.
- 시험용 위젯 `fixtures/probes.dart`(측정이 복사본 `lib/catalog_probe/` 에 넣음): `OverflowProbe`(폭 120 줄에 글자를 감싸지 않음), `IconProbeBad`(글자만 8 아래), `IconProbeGood`, `StateProbe`(켜지면 높이 30 → 40), `TapSmallProbe`(20 × 20 누를 칸), `TapBigProbe`(48 × 48).
- 알려진 답(2026-10-09 복사본 실측): `IFButton` 기본 생성자는 폭 한계 390 의 느슨한 자리에서 390 × 54, 내용 크기 33 × 54(안쪽 여백 0). `IFToggle` 은 꺼짐 · 켜짐 모두 52 × 28. 버튼 폴더(`lib/shared/presentation/widgets/buttons`)의 화면 위젯은 `GlassPressBox` · `IFButton` · `IFMiniButton` · `IFSpotButton` · `IFStatusMark` · `IconTapTarget` · `Pressable` · `SplitPill` 이고 `PressableData` 는 `InheritedWidget` 이라 화면 위젯이 아니다. 코드 검사 대상: `if_chip.dart:332` 의 `14.5`, `:333` 의 `5.5`, `if_button.dart:299` 의 `fontFamily`, `if_toggle.dart` 는 위반 0.
- 핏팰 의존성(봉인 전 확인): `flutter_hooks` · `hooks_riverpod` 직접 의존, `analyzer` · `yaml` 은 직접 의존이 아님(다른 패키지에 딸려 옴). 분석 규칙 `very_good_analysis` 는 직접 의존하지 않은 패키지를 가져오면 경고한다 → 설치 스크립트 `--add-deps` 가 이미 해석된 판 그대로 개발 의존성에 넣는다.
- 기능 조건 수(23)가 「복잡」 지침 상한 20 을 넘는다. 생성기 · 검사 · 설치 · 화면 동작을 실제로 돌려 보는 조건이 대부분이라 묶으면 부분 통과가 PASS 로 샌다 — 나누지 않는다.
- 측정 준비 단계 실측(봉인 전): `setup` 이 원본 복사 · 의존성 받기까지 통과하고 설치 스크립트가 없어 `SETUP_FAIL install` 로 멈춘다(예상). `fvm` · `rsync` · `stat` · `node` · 구글 크롬 실행 파일 · playwright-core(scratchpad `shot/node_modules`) 존재.
- 기존 검사 기준(봉인 전 실측): `python3 scripts/validate-plugin.py flutter-toolkit` 종료 0, `python3 scripts/sync-docs.py flutter-toolkit --check-only` 「동기화 상태」, `flutter-toolkit/evals/evals.json` 의 `evals` 24 개(케이스마다 `skill` 칸이 있다).

- 진단-02 기준(봉인 전 3차 검토 실측): 이미 커밋된 `docs/superpowers/` 설계 · 계획 문서 두 개에 MD013 을 뺀 마크다운 경고 13 건(MD032 등)이 있다. 이번 구현에서 두 문서도 고친다.
- 시험 실행 수는 `flutter test -r json` 출력을 한 줄씩 JSON 으로 읽어 숨김 아닌 `testDone` 사건을 센다(줄 안 키 순서가 `"hidden"` 먼저라 글자 순서로 세면 늘 0).

### 측정 묶음이 기대하는 이름

| 자리 | 이름 · 모양 |
| --- | --- |
| 생성물 | `lib/catalog_kit/generated/catalog_entries.g.dart`. 항목마다 줄 머리 두 칸 들여쓴 `PlaygroundEntry(` 로 시작하고, 그 안에 `widget: '<클래스>'` · `variant: '<생성자 이름, 기본은 new>'` · 속성마다 `key: '<속성 이름>'` 이 있다 |
| 글자 속성 | 타입이 `String` · `String?` · `Widget` · `Widget?` 인 속성. 생성물에서 `TextControl(` 로 나온다. 넘침 검사의 글자 표본 3 가지가 여기에 들어간다 |
| 결과 표 | `build/widget_fundamentals.csv`, 머리말 `widget,variant,check,case,result,measured`, 시험 하나에 한 줄, `result` 는 `PASS` 또는 `FAIL`, `measured` 에 쉼표 없음 |
| `measured` 모양 | 크기 동작 `w=<폭> h=<높이>`, 여백 `left=<값> right=<값>`, 상태 불변 `<폭>x<높이> → <폭>x<높이>`(소수 첫째 자리), 아이콘 정렬 `dy=<값>`, 그리기 실패 시 `감싸개` 를 포함한 안내 |
| 검사 이름 | `넘침` · `여백` · `크기 동작` · `상태 불변` · `아이콘 정렬` · `터치 크기`, 그리고 전체 한 번 `글꼴` |
| 시험 이름 | `<위젯>.<종류> \| <검사> \| <조건>`, 글꼴은 `catalog_kit \| 글꼴 \| 등록` |
| 시험 감싸개 | `test/catalog_kit/catalog_kit_host.dart` 가 `hostLocales` · `Future<void> setUpHost(Locale)` · `Widget wrap(Widget child, {required double textScale, required Locale locale})` 를 내놓는다 |
| 놀이터 감싸개 | `lib/catalog_kit/catalog_kit_app_host.dart` 가 `Widget appWrap(Widget child)` 를 내놓는다. 진입 파일은 `lib/main_catalog_kit.dart` |
| 코드 검사 출력 | 위반 한 건에 한 줄 `<경로>:<줄>: <규칙> <값>` |
| 목록 파일 모양 | `catalog/widgets.yaml` — 칸 이름은 `fixtures/widgets.ok.yaml` 이 기준(`spacing_tokens` · `shared_dir` · `theme_dir` · 위젯마다 `class` · `file` · `sizing` · `min_padding` · `view` · `state_keys` · `labels` · `ranges` · `samples`) |
| 놀이터 화면 이름(접근성 트리) | 왼쪽 목록 항목 글자는 클래스 이름 그대로(`IFMiniButton`), 열린 위젯 제목은 `<클래스>.<종류 표시 이름>`(`IFMiniButton.primary`), 종류 드롭다운은 이름에 `종류` 가 든 버튼, 참거짓 속성은 이름에 속성 이름이 든 스위치(`held`), 되돌리기는 이름에 `기본값으로` 가 든 버튼, 보기 바꾸기는 이름에 `휴대폰 화면` 이 든 버튼, 크기 글자는 `<가로> × <세로>` 정수(휴대폰 화면 폭 320 · 375 · 390 · 430). 진입 파일이 접근성 트리를 켠다. 목록 파일의 `view` 가 `content` 인 위젯은 내용 크기 보기로 열린다 |
| 공개 클래스 | 놀이터 화면 `CatalogPlayground`, 목록 항목 `PlaygroundEntry` |
| 터치 크기 기준 | 44 × 44 이상(`iOSTapTargetGuideline`) |

## 범위 경계

```text
# sprint-scope
flutter-toolkit/references/widget-fundamentals.md
flutter-toolkit/skills/flutter-catalog/
flutter-toolkit/skills/flutter-widget/SKILL.md
flutter-toolkit/skills/flutter-extract/SKILL.md
flutter-toolkit/skills/flutter-preflight/SKILL.md
flutter-toolkit/skills/flutter-audit/SKILL.md
flutter-toolkit/README.md
flutter-toolkit/evals/evals.json
CLAUDE.md
README.md
docs/superpowers/
.harness/
```

- 범위 밖: 원본 핏팰 수정(2단계), 플러그인 버전 올리기 · 릴리스, 위젯북 연동, 화면 단위 넘침(키보드 · 긴 목록).
- 이번에 자동 검사를 만들지 않는 규칙: 4(크기 단계 높이), 7(아이콘 크기 토큰), 14(바깥 여백 구분), 15(읽어 줄 이름 · 대비). 규칙 문서에 「자동 검사: 아니오」 로 적고 이유를 붙인다.
- 아이콘 정렬 기준 고르기는 측정 캡처까지 만들고 사용자 선택은 받지 않는다. 검사 기본값은 줄 상자 가운데(1px 허용).
- 오라클 해소: 스킬-01 — 산출물이 규칙 문서 자체다. 규칙이 실제로 쓰이는지는 스킬-04 와 스크립트-04 · 05 · 09 가 잰다.
- 오라클 해소: 구조-02 · 재사용-01 · 재사용-02 — 정적 코드의 부재 · 이름 확인이라 실행할 동작이 없다. 0 기대 측정에는 양성 대조를 붙였다.
- 오라클 해소: 스킬-02 — 스킬 문서의 frontmatter · 소제목 구조를 재는 조건이고, 서브커맨드가 실제로 하는 일(설치 · 생성 · 검사 · 띄우기)은 구조-04 · 스크립트-01 · 스크립트-04 · 구조-05 가 실행해서 잰다.

## Skill

- [ ] 스킬-01: `flutter-toolkit/references/widget-fundamentals.md` 의 규칙 표가 열 순서 `| # | 규칙 | 강도 | 자동 검사 | 검사 이름 |` 이고, 번호 1~15 를 한 번씩 가지며, 모든 행의 강도가 `MUST` 또는 `SHOULD`, 자동 검사가 `예` 또는 `아니오` 이고, 4 · 7 · 14 · 15 번은 `아니오`, `예` 인 행의 검사 이름은 결과 표 검사 이름 일곱 가지나 `코드 검사` 중 하나다 [exact]
    측정: `F=flutter-toolkit/references/widget-fundamentals.md; grep -cE '^\| *# *\| *규칙 *\| *강도 *\| *자동 검사 *\| *검사 이름 *\|' $F` 이 1, `awk -F'|' '/^\| *[0-9]+ *\|/{gsub(/ /,"",$(2)); print $(2)}' $F | sort -n | paste -sd' ' -` 출력이 `1 2 3 4 5 6 7 8 9 10 11 12 13 14 15`, `awk -F'|' '/^\| *[0-9]+ *\|/{gsub(/^ +| +$/,"",$(4)); gsub(/^ +| +$/,"",$(5)); if ($(4) !~ /^(MUST|SHOULD)$/ || $(5) !~ /^(예|아니오)$/) n++} END{print n+0}' $F` 이 0, `awk -F'|' '/^\| *(4|7|14|15) *\|/{gsub(/^ +| +$/,"",$(5)); print $(5)}' $F | sort -u` 출력이 `아니오` 한 줄, `awk -F'|' '/^\| *[0-9]+ *\|/ && $(5) ~ /예/{gsub(/^ +| +$/,"",$(6)); print $(6)}' $F | grep -cvE '^(넘침|여백|크기 동작|상태 불변|아이콘 정렬|터치 크기|글꼴|코드 검사)$'` 이 0
    음성 대조: 번호 하나를 중복시킨 사본에서 둘째 출력이 달라지고, 강도 칸 하나를 `MAY` 로 바꾼 사본에서 셋째 출력이 1
- [ ] 스킬-02: `flutter-toolkit/skills/flutter-catalog/SKILL.md` frontmatter 에 `name: flutter-catalog` · `description` · `user-invocable: true` 가 있고, 서브커맨드 `init` · `gen` · `check` · `open` 이 각각 자기 소제목(`###`)을 갖는다 [exact, enumerated]
    측정: `grep -cE '^user-invocable: true' flutter-toolkit/skills/flutter-catalog/SKILL.md` 1, `grep -cE '^name: flutter-catalog$' <같은 파일>` 1, `for c in init gen check open; do grep -cE "^### .*\`$c\`" <같은 파일>; done` 네 줄 모두 1 이상
- [ ] 스킬-03: `flutter-catalog/SKILL.md` 의 `## Gotchas` 절 목록 항목이 5 개 이상이고, 다섯 함정이 서로 다른 항목에 하나씩 있다 — `별도 패키지`(글꼴이 바뀜), `서비스 워커`(옛 화면), `testWidgets`(경우마다 따로), `글꼴 등록`(앱 글꼴을 실제로), `시안`(흉내 낸 시안은 목록 밖) [structural, enumerated]
    측정: `awk '/^## Gotchas/{f=1;next} /^## /{f=0} f && /^- /{n++; print n": "$(0)}' flutter-toolkit/skills/flutter-catalog/SKILL.md` 출력에서 다섯 낱말이 각각 1 건 이상이고, 다섯 낱말이 걸린 항목 번호가 서로 다르다(같은 항목에 둘 이상이면 FAIL)
- [ ] 스킬-04: 기존 4 스킬 `flutter-widget` · `flutter-extract` · `flutter-preflight` · `flutter-audit` 의 SKILL.md 가 모두 경로 형태로 `skills/flutter-catalog` 또는 `/flutter-catalog` 와 `references/widget-fundamentals.md` 를 가리킨다 [exact, enumerated]
    측정: `for s in flutter-widget flutter-extract flutter-preflight flutter-audit; do f=flutter-toolkit/skills/$s/SKILL.md; echo "$s $(grep -cE 'skills/flutter-catalog|/flutter-catalog' $f) $(grep -c 'references/widget-fundamentals.md' $f)"; done` 네 줄 모두 두 수가 1 이상
- [ ] 스킬-05: 루트 `CLAUDE.md` 의 flutter-toolkit 스킬 표 구간에 `/flutter-catalog` 행이 있고 flutter-toolkit 문서 동기화가 깨끗하다 [exact]
    측정: `awk '/^#### flutter-toolkit/{f=1;next} /^#### /{f=0} f' CLAUDE.md | grep -cF '/flutter-catalog'` 이 1 이상(봉인 전 0), `python3 scripts/sync-docs.py flutter-toolkit --check-only` 출력에 「동기화」 포함하고 「필요」 없음
    양성 대조: 같은 awk 를 `#### harness` 구간에 돌리면 `/sprint-contract` 가 1 (봉인 전 실측)
- [ ] 스킬-06: `flutter-toolkit/evals/evals.json` 이 올바른 JSON 이고 `evals` 가 25 개이며 그중 정확히 하나의 `skill` 칸이 `flutter-catalog` 다 [exact]
    측정: `python3 -c "import json;c=json.load(open('flutter-toolkit/evals/evals.json'))['evals'];print(len(c), sum(1 for x in c if x.get('skill')=='flutter-catalog'))"` 출력이 `25 1`

## Script

- [ ] 스크립트-01: Given `setup` 이 `SETUP_OK`, When 목록 위젯으로 생성기를 돌리면, Then 종료 코드 0 이고 `IFButton` 기본 생성자 항목 안에 속성 일곱 개 `onTap` · `child` · `height` · `width` · `radius` · `refractionStrength` · `held` 가 모두 있다 [exact, enumerated]
    측정: `bash .harness/.meta/flutter-catalog/measure.sh gen-ok` 끝 줄 `VERDICT PASS`
    음성 대조: 속성 순회가 첫 속성 뒤에서 멈추게 하면 `MISSING` 6 줄과 `VERDICT FAIL`
- [ ] 스크립트-02: Given 목록에 여백 타입 속성(`padding`)을 가진 `IFChipContainer` 를 예시 값 없이 넣으면, When 생성기를 돌리면, Then 종료 코드 1 이고 출력에 `IFChipContainer` 와 `padding` 이 나오며, 직전 성공 때 쓴 생성물의 수정 시각이 바뀌지 않는다 [exact]
    측정: `measure.sh gen-unsupported` 끝 줄 `VERDICT PASS` (사전 생성물 존재 · 시각 같음 · 종료 1 · 두 낱말을 모두 확인)
    음성 대조: 실패 판정 전에 파일을 쓰게 바꾸면 시각이 달라져 FAIL, 이름을 출력하지 않고 종료 1 만 하면 FAIL
- [ ] 스크립트-03: 목록 파일에 `shared_dir: lib/shared/presentation/widgets/buttons` 를 두고 일부만 적으면 생성기가 종료 1 로 끝나며 빠진 화면 위젯 여섯 개 `GlassPressBox` · `IFSpotButton` · `IFStatusMark` · `IconTapTarget` · `Pressable` · `SplitPill` 을 모두 출력하고 `PressableData` 는 출력하지 않는다. 목록에 코드에 없는 `NoSuchWidget` 을 적으면 종료 1 과 그 이름을 출력한다 [exact, enumerated]
    측정: `measure.sh gen-missing` 와 `measure.sh gen-unknown` 끝 줄 모두 `VERDICT PASS`
- [ ] 스크립트-04: Given 목록 위젯으로 `fund-run`, Then 결과 표에서 `IFButton.new` 의 `크기 동작` 은 한 줄이고 FAIL 이며 `w` ≥ 389, `여백` 은 한 줄이고 FAIL 이며 좌우 중 작은 값 < 16, `IFToggle.new` 의 `크기 동작` 은 PASS, `상태 불변` 은 PASS 이고 `52.0x28.0` 이 찍히며, `StateProbe.new` 의 `상태 불변` 은 FAIL 이다 [exact]
    측정: `measure.sh fund-run` 다음 `measure.sh sizing` 끝 줄 `VERDICT PASS`
    알려진 답: 390 × 54 · 내용 33 × 54, `IFToggle` 꺼짐 · 켜짐 52 × 28
    음성 대조: 크기 동작 검사의 비교를 항상 참으로 바꾸면 `IFButton.new` 행이 PASS 가 되어 FAIL, 여백 검사의 하한 비교를 항상 참으로 바꾸면 FAIL, 상태 불변 검사가 상태를 뒤집지 않으면 `StateProbe` 가 PASS 가 되어 FAIL
- [ ] 스크립트-05: 넘침 검사 경우 수가 `IFToggle.new` 24 · `IFButton.new` 72 이고, 모든 항목에서 폭 3(320 · 360 · 393) × 배율 4(1.0 · 1.3 · 1.6 · 2.0) × 언어 2(ko · en) × 글자 표본(글자 속성이 있으면 3, 없으면 1) 과 같고, 생성물 항목이 15 개 이상이며 `IFButton.new` · `IFMiniButton.primary` · `IFToggle.new` · `AppErrorWidget.new` · `OverflowProbe.new` · `IFBadge` 항목이 있고, `OverflowProbe` 의 넘침 행에 FAIL 이 하나 이상, `IFToggle` 의 넘침 행은 모두 PASS 다 [exact]
    측정: `measure.sh fund-run` 다음 `measure.sh overflow` 끝 줄 `VERDICT PASS`
    알려진 답: `IFToggle.new` 는 글자 속성이 없어 24, `IFButton.new` 는 `child` 가 있어 72 — 측정이 이 두 수를 생성물과 따로 박아 둔 값으로 비교한다
    음성 대조: 넘침 예외를 삼키는 구현이면 `OverflowProbe` FAIL 0 건으로 FAIL
- [ ] 스크립트-06: 앱 테마가 쓰는 글꼴이 등록되지 않으면 기본기 검사의 `catalog_kit | 글꼴 | 등록` 시험이 실패하고, 정상 pubspec 에서는 통과한다 [exact]
    측정: `measure.sh font` 끝 줄 `VERDICT PASS` (정상 실행 종료 0 · 실행된 시험 1 개 이상 · pubspec 에서 `KIMM` 글꼴 선언 항목을 실제로 뺐음(차이 1 줄 이상) · 뺀 실행 종료 0 아님 · 출력에 `글꼴` · 측정 뒤 pubspec 원복(차이 0))
- [ ] 스크립트-07: 코드 검사 스크립트가 `if_chip.dart:332` 줄의 `14.5`, `:333` 줄의 `5.5`, `if_button.dart:299` 줄의 `fontFamily` 를 찾고, 위반 없는 `if_toggle.dart` 는 출력하지 않으며, 종료 1 · `--report` 로는 종료 0 이다 [exact, enumerated]
    측정: `measure.sh lint` 끝 줄 `VERDICT PASS`
- [ ] 스크립트-08: 깐 틀 · 생성물 · 시험용 위젯 · 감싸개가 복사본에서 `fvm flutter analyze --no-fatal-infos` 종료 0 이고 `No issues found` 다 [exact]
    측정: `measure.sh analyze` 끝 줄 `VERDICT PASS` (대상 경로를 첫 줄에 찍음)
    양성 대조: `measure.sh analyze-pos` (틀 폴더에 오류 한 줄을 넣은 실행) 끝 줄 `VERDICT PASS` — 같은 명령이 오류를 1 건 이상 잡는다
- [ ] 스크립트-09: 터치 크기 기준 44 × 44 로, 결과 표에서 `IconProbeBad` 의 `아이콘 정렬` 은 FAIL, `IconProbeGood` 은 PASS, `TapSmallProbe` 의 `터치 크기` 는 FAIL, `TapBigProbe` 는 PASS 다(각각 한 줄) [exact, enumerated]
    측정: `measure.sh fund-run` 다음 `measure.sh icon-touch` 끝 줄 `VERDICT PASS`
    음성 대조: 아이콘 정렬 허용 오차를 무한으로 바꾸면 `IconProbeBad` 가 PASS 가 되어 FAIL

## Error

- [ ] 오류-01: 정상 감싸개 실행에서 `AppErrorWidget` 행에 「감싸개」 안내가 0 건이고, 상태 저장소 · 번역을 뺀 감싸개(`fixtures/catalog_kit_host.bare.dart`)로 돌리면 `AppErrorWidget` 행이 하나 이상 FAIL 이며 그 `measured` 에 「감싸개」 가 있고, `IFToggle` 행 결과는 두 실행에서 같다 [exact]
    측정: `measure.sh fund-run` 다음 `measure.sh wrapper` 끝 줄 `VERDICT PASS` (측정 뒤 감싸개 원복 차이 0 포함)

## Architecture

- [ ] 구조-01: 틀 파일이 `flutter-toolkit/skills/flutter-catalog/templates/` 아래 정확히 이 열한 개다 — `catalog/widgets.yaml` · `lib/catalog_kit/catalog_kit_app_host.dart.tmpl` · `lib/catalog_kit/catalog_kit_models.dart.tmpl` · `lib/catalog_kit/measured_box.dart.tmpl` · `lib/catalog_kit/property_panel.dart.tmpl` · `lib/catalog_kit/widget_playground.dart.tmpl` · `lib/main_catalog_kit.dart.tmpl` · `test/catalog_kit/catalog_kit_host.dart.tmpl` · `test/catalog_kit/widget_fundamentals_test.dart.tmpl` · `tool/catalog_gen.dart.tmpl` · `tool/catalog_lint.dart.tmpl`. 레포 안 `flutter-catalog` 폴더에 확장자 `.dart` 파일은 0 개다 [exact, enumerated]
    측정: `(cd flutter-toolkit/skills/flutter-catalog/templates && find . -type f | sed 's#^\./##' | LC_ALL=C sort)` 출력이 위 열한 경로를 같은 순서로 정렬한 것과 같다, `find flutter-toolkit/skills/flutter-catalog -name '*.dart' | wc -l` 이 0
    양성 대조: 같은 `find -name '*.dart'` 를 `.harness/.meta/flutter-catalog/fixtures` 에 돌리면 4 (봉인 전 실측)
- [ ] 구조-02: 틀 Dart 코드에 새 `StatefulWidget` · `StatefulBuilder` · `setState` · `ValueNotifier` 가 0 건이다. 상태는 `flutter_hooks` 로 둔다 [exact]
    측정: `grep -rhoE 'extends StatefulWidget|StatefulBuilder|setState\(|ValueNotifier' flutter-toolkit/skills/flutter-catalog/templates | wc -l` 이 0, `grep -rl 'flutter_hooks' flutter-toolkit/skills/flutter-catalog/templates | wc -l` 이 1 이상
    양성 대조: 첫 grep 을 Flutter 설치본 `~/fvm/versions/3.47.2/packages/flutter/lib/src/material/checkbox.dart` 에 돌리면 1 이상 (봉인 전 실측 2)
- [ ] 구조-03: 틀 Dart 코드가 특정 프로젝트 패키지를 가져오지 않는다(감싸개 틀 두 개도 일반 `ThemeData` 만 쓴다) [exact]
    측정: `grep -rlE "package:app/" flutter-toolkit/skills/flutter-catalog/templates | wc -l` 이 0
    양성 대조: 같은 grep 을 `.harness/.meta/flutter-catalog/fixtures` 에 돌리면 3 (봉인 전 실측)
- [ ] 구조-04: 설치 스크립트 `flutter-toolkit/skills/flutter-catalog/scripts/install.sh [--add-deps] <프로젝트>` 가 틀을 `.tmpl` 을 뗀 이름으로 깔고, 깔 파일 중 하나라도 이미 있으면 아무것도 쓰지 않고 종료 1 로 알린다. `--add-deps` 는 `analyzer` · `yaml` 이 직접 의존성에 없을 때만 개발 의존성으로 넣는다 [exact]
    측정: `measure.sh setup` 이 `SETUP_OK`, 이어서 `measure.sh install` 끝 줄 `VERDICT PASS` (두 번째 설치 종료 1 · 기존 파일 표식 유지 · 일부만 있는 폴더에서 종료 1 이고 파일 수 그대로 2 · 복사본 pubspec 개발 의존성에 `analyzer` · `yaml` 두 줄)
    음성 대조: 덮어쓰기 확인을 빼면 두 번째 설치가 종료 0 이 되어 FAIL
- [ ] 구조-05: 복사본에서 놀이터 진입 파일을 배포용으로 빌드해 실제 구글 크롬으로 띄우면 화면 오류 0 건이고 여섯 단계가 모두 통과한다 — (1) 첫 화면에 위젯 목록(`IFButton`)과 종류 칸, (2) 코드 칸 없음, (3) 누르기 전에는 `IFMiniButton.` 으로 시작하는 제목이 없고 목록에서 `IFMiniButton` 을 누른 뒤 생김, (4) 종류 드롭다운에서 `secondary` 를 고르면 `IFMiniButton.secondary`, (5) 속성 `held` 스위치를 바꾸면 「기본값으로」 버튼이 생김, (6) 휴대폰 화면 보기로 바꾸면 크기 글자가 바뀌고 그 가로가 휴대폰 폭 중 하나. 화면 이름은 배경의 「놀이터 화면 이름」 행을 따른다 [goal]
    측정: `measure.sh web` 출력에 `steps 6 failed 0` · `errors 0`, 끝 줄 `VERDICT PASS`(스크립트가 단계 수 6 을 직접 확인). 캡처 다섯 장 `.harness/.meta/flutter-catalog/shots/1-first.png` · `2-widget.png` · `3-variant.png` · `4-prop.png` · `5-view.png`(1 번 캡처가 단계 1 · 2 를 함께 보인다), 기록은 `chrome.log`. 평가자가 캡처 다섯 장을 열어 단계 이름과 화면이 맞는지 본다
- [ ] 구조-06: 설치 스크립트가 깐 시험 감싸개 · 놀이터 감싸개 틀을 고치지 않은 채로 쓰면, 두 파일에 `package:app/` 가져오기가 0 건이고 분석 종료 0, 글꼴 시험이 1 개 이상 돌아 종료 0, 놀이터 배포용 빌드 종료 0 이다 [exact]
    측정: `measure.sh setup`(설치 직후 틀 감싸개를 `fixtures` 판으로 덮기 전에 따로 보관한다) 다음 `measure.sh tmpl-hosts` 끝 줄 `VERDICT PASS` (측정 뒤 `fixtures` 판 원복 차이 0 포함)
    음성 대조: 틀 감싸개에 `wrap` 이나 `appWrap` 이 없으면 분석이나 빌드가 실패해 FAIL
- [ ] 구조-07: 플러그인 검증 전체가 통과한다 [exact]
    측정: `python3 scripts/validate-plugin.py flutter-toolkit` 종료 0 (봉인 전 실측 종료 0)

## Anti-patterns

- [ ] 금지-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수
    측정: `python3 scripts/validate-plugin.py --check=code-fence flutter-toolkit` 종료 0
- [ ] 금지-04: SKILL.md frontmatter 에서 name 필드 누락 금지 (flutter-toolkit 의 SKILL.md 전부)
    측정: `python3 scripts/validate-plugin.py --check=frontmatter flutter-toolkit` 종료 0

## Reusability

- [ ] 재사용-01: 다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다
    측정: `grep -rhoE 'class (CatalogPlayground|PlaygroundEntry)\b' flutter-toolkit/skills/flutter-catalog/templates | sort -u | wc -l` 이 2, `grep -rhoE 'class _(CatalogPlayground|PlaygroundEntry)\b' <같은 폴더> | wc -l` 이 0
- [ ] 재사용-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다 — flutter-toolkit 에 생성자를 읽어 카탈로그를 만드는 기존 스킬이 없었다
    측정: 봉인 전 `grep -rlE 'ConstructorElement|생성자를 읽' flutter-toolkit/skills --include=SKILL.md` 0 개(실측), 구현 뒤 같은 명령이 `flutter-catalog/SKILL.md` 하나뿐(새 스킬 본문은 생성자를 읽는다고 적는다)

## Diagnostics

- [ ] 진단-01: N/A (commands.analyze 는 scripts/release.sh 만 잰다 — 이번 범위와 교집합 0 개. 측정: Given 이 스프린트 커밋 뒤, `git diff --name-only origin/main...feat/flutter-catalog -- scripts/release.sh | wc -l` 이 0, 브랜치 존재는 `git rev-parse --verify feat/flutter-catalog` 로 먼저 찍는다. 분석은 스크립트-08 이 잰다)
- [ ] 진단-02: IDE diagnostics 워닝/인포 0개 — Given 이 스프린트 커밋 뒤, `flutter-toolkit/` · `CLAUDE.md` · `README.md` · `docs/superpowers/` 안에서 바뀐 .md 파일, 줄 길이 MD013 제외
    측정: `L=$(git diff --name-only origin/main...feat/flutter-catalog -- '*.md' ':(exclude).harness/*'); printf '%s\n' "$L" | grep -c .` 이 4 이상(새 규칙 문서 · 새 스킬 · 연결한 스킬 넷 중 일부 · CLAUDE.md), 이어서 `printf '%s\n' "$L" | xargs npx --yes markdownlint-cli2 2>&1 | grep -v MD013 | grep -c 'error MD'` 이 0 (목록을 따옴표로 넘겨 zsh 에서도 파일마다 나뉜다)
    양성 대조: 같은 markdownlint 를 이 계약 파일에 돌리면 1 (MD041, 봉인 전 실측)
- [ ] 진단-03: N/A (commands.test 는 scripts/release.sh 실행 — 진단-01 과 같은 측정으로 교집합 0 개. 시험은 스크립트-04 · 05 · 06 · 09 가 잰다)
- [ ] 진단-04: 실제 앱/서버 구동 시 에러 0개
    측정: 구조-05 의 `measure.sh web` 결과 `chrome.log` 의 `errors 0` (그 사례가 스스로 센 값)
