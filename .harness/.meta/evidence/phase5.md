---
phase: 5
title: "Phase 5 flutter-toolkit — 확보된 외부 근거"
collected: 2026-09-24
method: codex (foreground, 직접 호출 · gpt-5.6-sol · 조회는 curl/gh)
inputs: 처리 배정표(.claude/kaizen-input/insights-report.md)의 Phase 5 행 · phase-research-templates.md Phase 5 필수 출처 · 현행화 점검
note: 이 파일이 이 Phase 의 유일한 외부 근거다. 바깥 자료를 새로 찾지 마라. 여기 없는 URL·수치를 지어내지 마라. 없으면 미반영으로 남긴다.
---

읽기 전용으로 조사했으며 파일은 수정하지 않았다. Context7 도구는 이 세션에 없어 표의 fallback대로 공식 문서·pub.dev API·공식 GitHub 저장소를 `curl`·`gh`로 조회했다.

## 1. 출처 목록

외부 1차 출처:

- Flutter stable 배포 메타데이터: [releases_macos.json](https://storage.googleapis.com/flutter_infra_release/releases/releases_macos.json)
- Flutter 국제화: [Internationalizing Flutter apps](https://docs.flutter.dev/ui/accessibility-and-internationalization/internationalization)
- Flutter locale 결정 규칙: [WidgetsApp.locale](https://api.flutter.dev/flutter/widgets/WidgetsApp/locale.html), [TestPlatformDispatcher.locale](https://api.flutter.dev/flutter/flutter_test/TestPlatformDispatcher/locale.html)
- Flutter 스크롤: [ListView](https://api.flutter.dev/flutter/widgets/ListView-class.html), [ScrollView.shrinkWrap](https://api.flutter.dev/flutter/widgets/ScrollView/shrinkWrap.html), [NestedScrollView](https://api.flutter.dev/flutter/widgets/NestedScrollView-class.html)
- Riverpod: [DO/DON’T](https://riverpod.dev/docs/root/do_dont), [pub.dev API](https://pub.dev/api/packages/flutter_riverpod), [공식 CHANGELOG](https://raw.githubusercontent.com/rrousselGit/riverpod/master/packages/flutter_riverpod/CHANGELOG.md)
- flutter_hooks: [pub.dev API](https://pub.dev/api/packages/flutter_hooks), [useEffect API](https://pub.dev/documentation/flutter_hooks/latest/flutter_hooks/useEffect.html), [공식 CHANGELOG](https://raw.githubusercontent.com/rrousselGit/flutter_hooks/master/packages/flutter_hooks/CHANGELOG.md)
- go_router: [pub.dev API](https://pub.dev/api/packages/go_router), [공식 CHANGELOG](https://raw.githubusercontent.com/flutter/packages/main/packages/go_router/CHANGELOG.md)
- auto_route: [pub.dev API](https://pub.dev/api/packages/auto_route), [공식 CHANGELOG](https://raw.githubusercontent.com/Milad-Akarie/auto_route/master/auto_route/CHANGELOG.md)
- Freezed: [pub.dev API](https://pub.dev/api/packages/freezed), [공식 CHANGELOG](https://raw.githubusercontent.com/rrousselGit/freezed/master/packages/freezed/CHANGELOG.md)
- build_runner: [pub.dev API](https://pub.dev/api/packages/build_runner), [공식 CHANGELOG](https://raw.githubusercontent.com/dart-lang/build/master/build_runner/CHANGELOG.md), [CLI 옵션 소스](https://github.com/dart-lang/build/blob/master/build_runner/lib/src/build_runner_command_line.dart), [build-filter 통합시험](https://github.com/dart-lang/build/blob/master/build_runner/test/integration_tests/build_command_build_filter_test.dart)
- Git 상태 형식: [git-status 공식 문서](https://git-scm.com/docs/git-status)

내부 1차 출처:

- [인사이트 처리표](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/.claude/kaizen-input/insights-report.md:35)
- [fit-pal 카탈로그 피드백](</Users/jackson/Hub/10_Dev/fit-pal/app/.harness/sprint-feedback-statistics-catalog.md:149>)

## 2. 항목별 관찰 사실

### flutter:P-F06-codegen-delete-count

확인된 사실:

- build_runner의 `--build-filter`는 “일치하는 경로만 빌드”하는 공식 옵션이며, 공식 통합시험도 필터에 맞는 산출물만 생성됨을 검사한다. 따라서 옵션 자체가 비공식이거나 무조건 잘못된 것은 아니다. [CLI 소스](https://github.com/dart-lang/build/blob/master/build_runner/lib/src/build_runner_command_line.dart), [통합시험](https://github.com/dart-lang/build/blob/master/build_runner/test/integration_tests/build_command_build_filter_test.dart)
- 다만 공식 자료에서 “필터 밖의 기존 source-tree 산출물을 절대로 보존한다”는 보장은 찾지 못했다.
- build_runner 2.16.0부터 잘못되거나 수정된 생성물을 기본으로 고치며, `--delete-conflicting-outputs`는 제거된 호환 옵션 목록으로 이동했다. 즉 최신판에서는 그 플래그를 빼도 생성물 수정·삭제가 일어날 수 있다. [CHANGELOG](https://raw.githubusercontent.com/dart-lang/build/master/build_runner/CHANGELOG.md), [CLI 소스](https://github.com/dart-lang/build/blob/master/build_runner/lib/src/build_runner_command_line.dart)
- 267개 삭제는 내부 관측 사실이다. 인사이트 보고서는 F06을 “build-filter 한 번이 생성물 267개를 지움”으로 기록한다. [insights-report.md:63](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/.claude/kaizen-input/insights-report.md:63)

반대 근거:

- 공식 build_runner는 build-filter를 명시적으로 지원한다. 따라서 “모든 프로젝트에서 필터가 항상 위험하다”까지 일반화할 외부 근거는 없다.
- 그러나 범용 킷이 프로젝트별 builder graph와 보존 동작을 증명하지 못한 채 자동으로 필터를 붙일 근거도 없다.

추론: 범용 기본값에서는 필터를 제거하는 편이 안전하다. 프로젝트 전용 필터 명령은 사용자가 명시적으로 선택했을 때만 허용하되, 자동 매핑에서는 제외해야 한다.

삭제 계수에는 `git status --porcelain=v1`을 쓰는 것이 맞다. 이 형식은 스크립트용 안정 형식이고 XY 두 자리 중 어느 쪽의 `D`도 삭제를 뜻한다. [git-status](https://git-scm.com/docs/git-status)

주의: 제안된 `grep -c '^ D\|^D '`는 0건일 때 종료 코드 1을 돌려 `set -e` 흐름을 끊을 수 있다. 계약 예시는 0건에도 성공하는 `awk` 계수가 더 안전하다.

```sh
git status --porcelain=v1 --untracked-files=no |
  awk 'substr($0,1,1)=="D" || substr($0,2,1)=="D" {n++} END {print n+0}'
```

### user-setup:P1 / F06

방향은 **범용 자동 build-filter 전면 제거**로 정하는 것이 근거에 가장 잘 맞는다.

- `flutter-run`, `flutter-build`, `flutter-preflight`, `flutter-l10n`에서 feature 인자를 받아 필터를 자동 구성하지 않는다.
- `project-detection.md`도 `app-codegen-filter`를 자동 우선 명령으로 선택하지 않는다.
- feature 인자는 호환성을 위해 받아도 codegen 범위를 좁히지 않는다.
- 모든 codegen 전후 삭제 수를 비교한다.
- 삭제 수가 늘면 필터 없는 전체 codegen을 한 번 실행한다. 이후 삭제 수가 기준 이하로 돌아왔을 때만 “복구”라고 보고한다. 그렇지 않으면 실패로 멈춘다.

반대 근거는 위와 같이 build_runner가 필터를 공식 지원한다는 점이다. 따라서 “필터 사용 자체 금지”보다는 “킷이 자동 선택하지 않음”이 정확한 계약 문구다.

### flutter:P-INSPECTOR-convention / F02

확인된 사실:

- 이 항목은 Flutter API 문제가 아니라 프로젝트 UI 의미·관례 문제다. Flutter 공식 문서에서 “줄/칩/뱃지/아이콘 뜻을 기존 화면 N개와 대조하라”는 직접 근거는 찾지 못했다.
- 내부 처리표에는 기존 화면 수가 2개와 3개로 충돌한다고 명시돼 있다. [insights-report.md:59](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/.claude/kaizen-input/insights-report.md:59)

권장 해석:

- Inspector가 별도로 화면 수를 정하거나 검색 범위를 넓히지 않는다.
- 호출 스킬이 이미 만든 관례 표만 입력으로 받는다.
- 표의 각 경로를 실제로 읽고 `맞음/어긋남 + 파일:라인`을 쓴다.
- 표가 없거나 경로를 읽지 못하면 `[미검증] 관례 표 없음/경로 확인 실패`로 쓴다.
- 이 방식이면 2개/3개 충돌을 Inspector 계약에서 재결정하지 않아도 된다.

반대 근거: 외부 공식 근거는 없으며, 이는 전적으로 프로젝트 관례 기반 규칙이다.

### flutter:P-TEST-locale-buildmod / F24

로캘:

- Flutter가 기본 제공하는 로컬라이제이션은 US English뿐이다. [Flutter 국제화 문서](https://docs.flutter.dev/ui/accessibility-and-internationalization/internationalization)
- 하지만 “모든 widget test가 무조건 영어로 돈다”는 표현은 너무 강하다. `WidgetsApp.locale`이 null이면 시스템 locale을 사용하고, 지원하지 않는 locale이면 `supportedLocales`의 첫 항목을 사용한다. 테스트의 platform locale도 override될 수 있다. [WidgetsApp.locale](https://api.flutter.dev/flutter/widgets/WidgetsApp/locale.html), [TestPlatformDispatcher.locale](https://api.flutter.dev/flutter/flutter_test/TestPlatformDispatcher/locale.html)

따라서 Gotcha는 다음처럼 쓰는 편이 정확하다.

> 위젯 시험의 로캘을 고정하지 않으면 테스트 플랫폼 locale과 앱의 locale resolution 결과에 의존한다. 한 언어의 문자열 리터럴을 단언하지 말고 생성된 번역 접근자에서 기대값을 만들거나 시험 하네스에서 locale을 명시한다.

provider/build 수정:

- Riverpod는 위젯이 provider를 초기화하지 말고 provider가 스스로 초기화해야 한다고 명시한다. 위젯 `initState`에서 `ref.read(provider).init()`하는 예도 잘못된 패턴으로 든다. [Riverpod DO/DON’T](https://riverpod.dev/docs/root/do_dont)
- `useEffect`는 build 중 동기적으로 호출된다. 따라서 그 본문에서 provider 상태를 곧바로 변경하면 widget lifecycle 중 provider flush/rebuild가 발생할 수 있다. [useEffect API](https://pub.dev/documentation/flutter_hooks/latest/flutter_hooks/useEffect.html)
- Riverpod 3.4.0 CHANGELOG에도 widget lifecycle 중 provider flush에서 발생하는 `markNeedsBuild` 예외 수정 이력이 있다. [Riverpod CHANGELOG](https://raw.githubusercontent.com/rrousselGit/riverpod/master/packages/flutter_riverpod/CHANGELOG.md)

추론: `initState`·`build`·`useEffect`에서 provider 상태를 직접 쓰지 않는다는 규칙은 타당하다. 파생값은 선언형 `ref.watch` 또는 로컬 `useMemoized`로 계산하고, provider 초기화는 provider 내부로 옮긴다.

### flutter:P-CATALOG-tile-height / F22

확인된 사실:

- `ListView`는 자체 scrollable이다. 일반적인 외부 ScrollView와 내부 ScrollView는 자동으로 하나처럼 협조하지 않으며, Flutter는 이를 조정해야 하는 경우 `NestedScrollView`를 별도로 제공한다. [ListView](https://api.flutter.dev/flutter/widgets/ListView-class.html), [NestedScrollView](https://api.flutter.dev/flutter/widgets/NestedScrollView-class.html)
- `shrinkWrap`은 스크롤 방향 크기를 내용으로 정하지만 비용이 더 크다. 따라서 무조건적인 해결책은 아니다. [ScrollView.shrinkWrap](https://api.flutter.dev/flutter/widgets/ScrollView/shrinkWrap.html)
- fit-pal 피드백에는 실제 내용보다 작은 고정 높이 `88→96`, `92→96` 수정 후 렌더 시험이 실패에서 통과로 바뀐 사례가 있다. [sprint-feedback-statistics-catalog.md:149](</Users/jackson/Hub/10_Dev/fit-pal/app/.harness/sprint-feedback-statistics-catalog.md:149>)

추론: 내용보다 낮은 타일 안의 목록이 별도 scrollable이 되면 포인터 스크롤을 내부가 처리해 바깥 카탈로그가 멈춘 것처럼 보일 수 있다.

반대 근거:

- 외부 공식 문서에서 “고정 높이가 낮으면 반드시 휠을 먹는다”는 정확한 문장은 찾지 못했다.
- 모든 중첩 스크롤을 높이 확대만으로 해결할 수는 없다. 실제로 독립 스크롤이 필요한 UI라면 controller/physics/NestedScrollView 설계가 필요하다.

계약은 “카탈로그 미리보기는 독립 내부 스크롤을 의도하지 않는 경우”로 범위를 제한해야 한다.

### F25

- “시안 21종”의 적정 개수는 Flutter 라이브러리나 공식 표준이 결정할 사안이 아니다.
- 내부 보고서도 이번 Phase에 대응 제안이 없고, “여러 개 다 만들어 나란히”라는 프로젝트 기억과 반대될 수 있어 사용자 확인이 필요하다고 명시한다. [insights-report.md:82](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/.claude/kaizen-input/insights-report.md:82)

권장: 이번 Phase에서 새 규칙을 만들지 않는다. 별도 결정 없이는 시안 개수 상한·축소 규칙을 계약에 넣지 않는다.

## 3. 현행화 — 낡은 곳

2026-09-24 조회 기준 최신 안정 버전:

| 대상 | 최신 안정 | 주요 변화 |
|---|---:|---|
| Flutter | 3.47.5 / Dart 3.13.4 | 2026-09-18 stable 배포. [공식 배포 JSON](https://storage.googleapis.com/flutter_infra_release/releases/releases_macos.json) |
| flutter_riverpod | 3.4.3 | 3.4.0의 `SyncProviderTransformerMixin` deprecated, 3.2.0의 `family.overrideWith` deprecated가 계속 유효. [pub API](https://pub.dev/api/packages/flutter_riverpod), [CHANGELOG](https://raw.githubusercontent.com/rrousselGit/riverpod/master/packages/flutter_riverpod/CHANGELOG.md) |
| flutter_hooks | 0.21.3+1 | `useExpansionTileController` deprecated → `useExpansibleController`. [pub API](https://pub.dev/api/packages/flutter_hooks), [CHANGELOG](https://raw.githubusercontent.com/rrousselGit/flutter_hooks/master/packages/flutter_hooks/CHANGELOG.md) |
| go_router | 18.0.1 | 최소 Flutter 3.44/Dart 3.12, material_ui/cupertino_ui로 이동. [pub API](https://pub.dev/api/packages/go_router), [CHANGELOG](https://raw.githubusercontent.com/flutter/packages/main/packages/go_router/CHANGELOG.md) |
| auto_route | 11.2.0 | 11.1에서 `animatePageTransition` deprecated; 11.0 named-navigation 제거/rename. [pub API](https://pub.dev/api/packages/auto_route), [CHANGELOG](https://raw.githubusercontent.com/Milad-Akarie/auto_route/master/auto_route/CHANGELOG.md) |
| Freezed | 4.0.2 | Dart 3.13/Analyzer 14, primary constructors; constructor parameter의 `final` 미지원 breaking. [pub API](https://pub.dev/api/packages/freezed), [CHANGELOG](https://raw.githubusercontent.com/rrousselGit/freezed/master/packages/freezed/CHANGELOG.md) |
| build_runner | 2.16.1 | 기본적으로 잘못된 생성물을 수정; `--delete-conflicting-outputs` 제거된 호환 옵션. [pub API](https://pub.dev/api/packages/build_runner), [CHANGELOG](https://raw.githubusercontent.com/dart-lang/build/master/build_runner/CHANGELOG.md) |

낡거나 빠진 곳:

- Flutter `3.47.0 → 3.47.5`
  - [flutter-widget/SKILL.md:31](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/flutter-toolkit/skills/flutter-widget/SKILL.md:31)
  - [flutter-transition/SKILL.md:19](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/flutter-toolkit/skills/flutter-transition/SKILL.md:19)
  - [flutter-ai-rules.md:103](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/flutter-toolkit/references/flutter-ai-rules.md:103)

- Riverpod `3.4.1 → 3.4.3`
  - [flutter-provider/SKILL.md:29](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/flutter-toolkit/skills/flutter-provider/SKILL.md:29)
  - [flutter-widget/SKILL.md:33](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/flutter-toolkit/skills/flutter-widget/SKILL.md:33)
  - 기존 deprecation 내용은 여전히 유효하고 버전·날짜만 낡았다.

- Freezed `3.2.5 → 4.0.2`
  - [flutter-hooks/SKILL.md:28](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/flutter-toolkit/skills/flutter-hooks/SKILL.md:28)
  - [flutter-provider/SKILL.md:21](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/flutter-toolkit/skills/flutter-provider/SKILL.md:21)
  - [flutter-api/SKILL.md:20](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/flutter-toolkit/skills/flutter-api/SKILL.md:20)
  - [flutter-error/SKILL.md:20](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/flutter-toolkit/skills/flutter-error/SKILL.md:20)
  - [flutter-audit/SKILL.md:179](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/flutter-toolkit/skills/flutter-audit/SKILL.md:179)
  - [flutter-ai-rules.md:83](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/flutter-toolkit/references/flutter-ai-rules.md:83)
  - `.when/.map`이 3.1에서 돌아왔다는 내용은 여전히 사실이지만 “최신 3.2.5”는 틀렸고 Freezed 4의 breaking 항목이 빠졌다.

- go_router `17.2.2 → 18.0.1`
  - [flutter-screen/SKILL.md:18](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/flutter-toolkit/skills/flutter-screen/SKILL.md:18)
  - 17.0 breaking 설명은 역사적으로 맞지만 최신 요구조건 Flutter 3.44/Dart 3.12와 18.0 migration이 빠졌다.

- auto_route 현행화 누락
  - [flutter-transition/SKILL.md:18](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/flutter-toolkit/skills/flutter-transition/SKILL.md:18)
  - 11.0 설명은 맞지만 최신 11.2.0 및 11.1의 `animatePageTransition` deprecation이 빠졌다.

- build_runner 2.16과 충돌하는 “플래그 필수”:
  - [flutter-run/SKILL.md:44](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/flutter-toolkit/skills/flutter-run/SKILL.md:44), [50](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/flutter-toolkit/skills/flutter-run/SKILL.md:50), [139](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/flutter-toolkit/skills/flutter-run/SKILL.md:139)
  - [flutter-build/SKILL.md:16](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/flutter-toolkit/skills/flutter-build/SKILL.md:16), [42](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/flutter-toolkit/skills/flutter-build/SKILL.md:42), [48](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/flutter-toolkit/skills/flutter-build/SKILL.md:48)
  - [flutter-preflight/SKILL.md:73](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/flutter-toolkit/skills/flutter-preflight/SKILL.md:73), [79](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/flutter-toolkit/skills/flutter-preflight/SKILL.md:79)
  - [flutter-l10n/SKILL.md:125](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/flutter-toolkit/skills/flutter-l10n/SKILL.md:125)
  - [project-detection.md:52](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/flutter-toolkit/references/project-detection.md:52)
  - [flutter-ai-rules.md:55](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/flutter-toolkit/references/flutter-ai-rules.md:55)
  - 동일 명령이 있는 `flutter-screen:272`, `flutter-transition:303`, `flutter-feature:151`, `flutter-api:336`도 버전 적응이 필요하다.
  - 권장 현재값: build_runner `>=2.16`에서는 플래그 없이 전체 build; 구버전 lock 지원이 필요하면 버전을 확인해 조건부로만 플래그를 붙인다.

- eval도 최신 계약과 반대:
  - [evals.json:8](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/flutter-toolkit/evals/evals.json:8)
  - [evals.json:12](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/flutter-toolkit/evals/evals.json:12)
  - [evals.json:13](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/flutter-toolkit/evals/evals.json:13)

## 4. 권장 계약안

1. **build-filter 방향**
   - 범용 스킬은 `--build-filter`와 `app-codegen-filter`를 자동 선택하지 않는다.
   - feature 인자가 있어도 전체 codegen을 실행한다.
   - 프로젝트 전용 필터 target은 사용자의 명시적 호출일 때만 허용한다.
   - 필터 사용 여부와 무관하게 전후 삭제 수를 기록한다.

2. **codegen 삭제 게이트**
   - `before_deleted`, `after_deleted`, 복구 후 `recovered_deleted`를 보고한다.
   - `after_deleted > before_deleted`이면 필터 없는 전체 codegen을 실행한다.
   - 복구 후에도 기준보다 많으면 실패하고 삭제 경로를 열거한다.
   - “전체 생성 실행”만으로 복구 성공을 선언하지 않는다.
   - 최신 build_runner에서 제거된 `--delete-conflicting-outputs`를 MUST로 두지 않는다.

3. **Inspector 관례 대조**
   - quick 모드 전용 기준 7로 추가한다.
   - 호출 스킬이 전달한 관례 표만 사용한다.
   - 줄 모양, 칩·뱃지 모양, 아이콘 뜻을 각각 `맞음/어긋남/미검증 + 파일:라인`으로 기록한다.
   - 관례 표 밖의 화면으로 범위를 넓히지 않는다.

4. **테스트 함정**
   - “기본 로캘은 항상 영어” 대신 “고정하지 않으면 플랫폼 locale과 locale resolution에 의존”으로 쓴다.
   - 문자열 리터럴 대신 생성 번역 접근자를 쓰거나 locale을 명시한다.
   - `initState`·`build`·`useEffect`에서 provider 상태를 직접 변경하지 않는다.
   - provider는 스스로 초기화하고 파생값은 선언형으로 계산한다.

5. **카탈로그 높이**
   - 독립 내부 스크롤을 의도하지 않는 카탈로그 타일에 한해 `내용 높이 ≤ 타일 높이`를 시험한다.
   - 고정 숫자만 올리는 시험보다 실제 콘텐츠의 bottom과 타일 bounds를 비교하는 시험을 우선한다.
   - 실제 중첩 스크롤 요구라면 높이 확대 규칙 대신 스크롤 조정 설계를 적용한다.

6. **F25**
   - 이번 Phase에서 규칙화하지 않는다.
   - 시안 개수는 별도 사용자 결정 없이는 기존 요청을 따른다.

## 5. 못 가져온 것 / 열린 질문

- Context7은 현재 도구 목록에 없어 조회하지 못했다. 공식 Flutter/Riverpod/pub.dev/GitHub 자료로 fallback했다.
- build_runner 공식 자료에서 “필터가 source tree의 필터 밖 기존 생성물을 삭제한다”는 직접 문장은 찾지 못했다. 267개 삭제는 내부 실측이며, 최신 2.16의 기본 생성물 정정·삭제 동작은 공식 확인됐다.
- 카탈로그의 “휠을 내부 목록이 먹는다”는 정확한 공식 문장은 찾지 못했다. 중첩 ScrollView가 자동 협조하지 않는다는 공식 설명과 fit-pal 실측을 결합한 추론이다.
- F02의 관례 대조와 F25의 시안 개수에는 외부 표준 근거가 없다. 프로젝트 계약·사용자 의도 문제다.
- 삭제 수만으로는 삭제된 파일의 정당성까지 판정할 수 없다. 계약에는 증가 시 경로 열거와 복구 후 재계수가 함께 필요하다.
