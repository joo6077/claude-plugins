---
name: flutter-run
description: >
  Flutter 빌드 프리미티브 실행 (codegen, analyze, fix, test).
  "코드 생성해줘", "분석 돌려줘", "테스트 실행", "포맷팅",
  "build_runner", "freezed 생성", "린트 확인", "codegen", "analyze",
  "dart fix", "flutter test" 같은 요청 시 사용한다.
  상위 워크플로우 스킬(flutter-build, flutter-preflight 등)에서 내부적으로도 호출된다.
  코드를 직접 수정하거나 새 파일을 생성하는 작업에는 사용하지 않는다.
  Makefile 기반 프로젝트(dart-define, observatory-port, launch.json)에서도 동작한다.
argument-hint: "<codegen|analyze|fix|test> [args]"
user-invocable: true
---

## Gotchas

- Windows에서 `fvm.bat` 사용 — `fvm` 직접 호출은 PATH 이슈 발생
- partial codegen `--build-filter="lib/features/auth/**"`는 필터 밖 의존성을 재생성하지 않는다 — 새 import/타입 추가 시 full codegen 사용
- `dart fix --apply` 후 반드시 `analyze` 실행 — fix가 새 워닝을 만들 수 있다
- **codegen 후 변경 보고 시 `.g.dart` / `.freezed.dart` 를 수기 변경과 섞지 마라** — 산출물 수십 개가 `git diff --stat` 에 섞이면 "변환 헬퍼만 변경" 같은 스코프 조건이 위반으로 판정된다 (글로벌 REJECT `AR-01` 실제 사례). codegen 서브커맨드 섹션의 exclude pathspec 명령을 사용해 두 목록을 나눠 보고하라
- Makefile 기반 monorepo(fit-pal 등)에서는 `fvm flutter run` 직접 호출 대신 `make app-run` 사용 — dart-define, observatory-port, launch.json 설정이 Makefile에 집중 관리된다. 직접 호출하면 dart-define 환경변수 누락으로 앱이 다른 환경으로 기동됨

Flutter 빌드 프리미티브. 첫 번째 인자로 서브커맨드를 지정한다.

## 0. 프로젝트 감지

`references/project-detection.md`의 절차를 실행하여 프로젝트 환경을 파악한다.
이후 단계에서 감지 결과(`$FLUTTER`, `$DART`, `$PACKAGE`, `HAS_BUILD_RUNNER`, `HAS_CUSTOM_LINT` 등)를 사용한다.

## Subcommands

### codegen [feature]

`build_runner`로 코드를 생성한다. Freezed, Retrofit, Riverpod, GoRouter, Envied, slang 등 프로젝트에 설정된 코드 생성기를 실행한다. `.g.dart`와 `.freezed.dart` 파일이 소스 변경에 맞게 갱신되지 않으면 컴파일 에러가 발생하므로, 모델이나 프로바이더를 수정한 뒤에는 반드시 실행해야 한다.

**전제 조건**: `HAS_BUILD_RUNNER`가 true여야 한다. 없으면:
> "build_runner가 pubspec.yaml에 없습니다. codegen을 사용하려면 먼저 설치해주세요:
> `$FLUTTER pub add dev:build_runner`"

feature 인자가 있으면 해당 feature만 빌드:

```bash
$DART run build_runner build --delete-conflicting-outputs --build-filter="lib/features/$FEATURE/**"
```

인자가 없으면 전체 빌드:

```bash
$DART run build_runner build --delete-conflicting-outputs
```

**codegen 산출물과 수기 변경을 분리해 보고한다** (글로벌 REJECT `AR-01` 대응). codegen 은
`.g.dart` / `.freezed.dart` / `.gr.dart` 를 대량 갱신하므로, 이후 "무엇을 바꿨는지" 를 보고할 때
`git diff --stat` 을 그대로 붙이면 "변환 헬퍼만 변경" 같은 스코프 주장이 산출물 때문에 깨진다.
codegen 실행 후에는 두 목록을 나눠서 제시한다:

```bash
# 수기 변경 (스코프 판정의 기준)
git diff --stat -- . ':(exclude)*.g.dart' ':(exclude)*.freezed.dart' ':(exclude)*.gr.dart'
# codegen 산출물 (건수만 보고)
git diff --stat -- '*.g.dart' '*.freezed.dart' '*.gr.dart'
```

### analyze

정적 분석을 실행한다. `analysis_options.yaml`에 설정된 린트 규칙(very_good_analysis, flutter_lints, 커스텀 린트 등)을 기반으로 코드 스타일 일관성과 아키텍처 위반을 조기에 잡는다.

`HAS_CUSTOM_LINT`가 true이면 custom_lint도 함께 실행:

```bash
$FLUTTER analyze
$DART run custom_lint
```

`HAS_CUSTOM_LINT`가 false이면:

```bash
$FLUTTER analyze
```

### fix

자동 수정 가능한 린트 이슈를 먼저 고치고, 포맷을 통일한다. 수동 수정을 줄여주므로 커밋 전에 항상 돌리는 것이 좋다.

```bash
$DART fix --apply lib/
$DART format lib/
```

### test [path]

변경 후 회귀를 방지하기 위해 실행한다.

path 인자가 있으면 해당 경로만 테스트:

```bash
$FLUTTER test $PATH
```

인자가 없으면 전체 테스트:

```bash
$FLUTTER test
```

## Report Format

성공 시:

```text
/flutter-run <subcommand> 완료
  결과: <success/N issues/N failed>
```

실패 시:

```text
/flutter-run <subcommand> 실패
  [에러 내용]
```

## Rules

- **MUST** 프로젝트 감지에서 결정된 `$FLUTTER` / `$DART` prefix를 사용한다. 하드코딩된 `fvm flutter`, `flutter`, `dart` 직접 사용 금지
- **MUST** codegen은 항상 `--delete-conflicting-outputs` 플래그 포함
- **MUST** 이 스킬은 실행만 담당한다. 코드 수정은 별도 스킬에서 수행
- **MUST** 서브커맨드 없이 호출하면 사용 가능한 서브커맨드 목록을 출력한다
