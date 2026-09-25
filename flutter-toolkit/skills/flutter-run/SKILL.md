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
- **codegen 에 `--build-filter` 를 스스로 붙이지 마라** — 필터 한 번에 생성물 267 개가 지워진 적이 있다(2026-09-16). feature 인자가 와도 전체를 돌리고 전후 삭제 수를 센다. 필터는 build_runner 가 공식으로 지원하지만, 필터 밖의 기존 생성물을 남긴다는 보장은 공식 자료에 없다
- `dart fix --apply` 후 반드시 `analyze` 실행 — fix가 새 워닝을 만들 수 있다
- 편집 훅(`scripts/format-edited-dart.sh`)이 Edit·Write 로 고친 .dart 파일을 그때마다 포맷한다(끄기: `FLUTTER_TOOLKIT_FORMAT_ON_EDIT=off`). fix 의 포맷은 훅이 못 본 파일을 뒷정리하는 몫이다 — `lib/` 통째 포맷으로 되돌리지 마라
- **codegen 후 변경 보고 시 `.g.dart` / `.freezed.dart` 를 수기 변경과 섞지 마라** — 산출물 수십 개가 `git diff --stat` 에 섞이면 "변환 헬퍼만 변경" 같은 스코프 조건이 위반으로 판정된다 (글로벌 REJECT `AR-01` 실제 사례). codegen 서브커맨드 섹션의 exclude pathspec 명령을 사용해 두 목록을 나눠 보고하라
- Makefile 기반 monorepo 에서는 `fvm flutter run` 직접 호출 대신 `make app-run` 사용 — dart-define, observatory-port, launch.json 설정이 Makefile에 집중 관리된다. 직접 호출하면 dart-define 환경변수 누락으로 앱이 다른 환경으로 기동됨

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

**필터 없이 전체를 돌리고 전후 삭제 수를 센다 (2026-09-25 추가).** feature 인자가 와도 `--build-filter` 를 붙이지 않는다 — 인자는 보고에 적기만 하고 범위를 좁히지 않는다.
`app-codegen-filter` 같은 프로젝트 전용 필터 명령은 사용자가 그 이름을 직접 부를 때만 쓴다 — 그때는 첫 codegen 줄만 그 명령으로
바꾸고 두 번째 줄은 필터 없는 전체 그대로 둔다. `HAS_MAKEFILE = true` 면 두 줄을 `$MAKE app-codegen` 으로 바꾼다.

```bash
# 코드 생성 전후로 git 이 삭제로 보는 추적 파일을 센다. 0 건에 종료 코드 1 을 내는 grep -c 대신 awk 로 센다
deleted() { git status --porcelain=v1 --untracked-files=no | awk 'substr($(0),1,1)=="D" || substr($(0),2,1)=="D" {print substr($(0),4)}' | sort; }
count() { printf '%s\n' "${1}" | awk 'NF{n++} END{print n+0}'; }
RC=0
BEFORE=$(deleted)
$DART run build_runner build --delete-conflicting-outputs || RC=$?
NEW=$(comm -13 <(printf '%s\n' "$BEFORE") <(deleted))
FIRST=$(count "$NEW")
if [ "$RC" = 0 ] && [ "$FIRST" -gt 0 ]; then
  # 한 번 더 돌린다. 비교 기준은 첫 BEFORE 그대로다 — 다시 재면 늘어난 삭제가 기준에 섞여 0 이 된다
  $DART run build_runner build --delete-conflicting-outputs || RC=$?
  NEW=$(comm -13 <(printf '%s\n' "$BEFORE") <(deleted))
fi
echo "삭제 before=$(count "$BEFORE") after=$(count "$(deleted)") new_first=$FIRST new=$(count "$NEW") codegen_exit=$RC"
[ -z "$NEW" ] || printf '늘어난 삭제:\n%s\n' "$NEW"
# 블록의 종료 코드가 codegen 실패와 남은 삭제를 둘 다 드러낸다 — 마지막 명령이 성공하면 실패가 가려진다
[ "$RC" = 0 ] && [ -z "$NEW" ]
```

블록은 codegen 이 실패했거나 `new` 가 남으면 0 이 아닌 종료 코드로 끝난다. `codegen_exit` 가 0 이 아니면 codegen 실패다 — 다시 돌리지 않고 멈춘다.
`new` 가 0 이면 통과다. `new_first` 가 0 이 아니고 `new` 가 0 이면 두 번째 실행으로 돌아온 것이라 복구로 보고한다 — 전체를 다시
돌렸다는 사실만으로 복구라고 쓰지 않는다. `new` 가 남으면 멈추고 `늘어난 삭제` 목록을 보고한다. 지운 원본의 생성물처럼
맞는 삭제일 수 있으니 되돌리지 말고 목록을 보인다. 보고에는 `삭제 before=… after=… new_first=… new=… codegen_exit=…` 줄을 그대로 붙인다.
생성물을 git 에 올리지 않는 프로젝트에서는 이 세기가 생성물 삭제를 보지 못해 늘 0 이다 — `git ls-files -- '*.g.dart' '*.freezed.dart'` 가 비면 `new=0` 을 통과로 쓰지 말고 보고 줄 뒤에 `추적된 생성물 0 개 — 삭제를 셀 수 없다` 를 붙인다.

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

자동 수정 가능한 린트 이슈를 먼저 고치고, 이번에 바뀐 .dart 파일만 포맷한다. 수동 수정을 줄여주므로 커밋 전에 항상 돌리는 것이 좋다.
`lib/` 를 통째로 포맷하면 이번에 손대지 않은 파일까지 바뀌어 diff 에 섞인다.

```bash
# dart fix 는 경로를 하나만 받는다. 파일을 여럿 주면 "Only one file or directory is expected" 로 exit 64
$DART fix --apply lib/
# 추적 전 새 파일은 git diff 에 안 나와 ls-files 로 더한다. 생성물은 코드 생성기가 다시 쓰므로 뺀다
CHANGED=$( { git diff --name-only --relative --diff-filter=ACMR HEAD -- '*.dart'
             git ls-files --others --exclude-standard -- '*.dart'; } \
           | grep -vE '\.(g|freezed|gr|mocks|config|gen)\.dart$' )
if [ -n "$CHANGED" ]; then
  printf '%s\n' "$CHANGED" | tr '\n' '\0' | xargs -0 $DART format --
else
  echo "포맷 건너뜀 — 이번에 바뀐 .dart 파일 없음"
fi
```

프로젝트 폴더(`pubspec.yaml` 이 있는 곳)에서 실행한다. `--relative` 가 그 폴더 밖 파일을 빼고 경로를 그 폴더 기준으로 바꾼다.
목록이 비면 포맷을 건너뛰고 보고에 `포맷 건너뜀 (바뀐 .dart 없음)` 이라고 적는다.

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
- **MUST** codegen 은 전후 삭제 수를 세어 `삭제 before=… after=… new_first=… new=… codegen_exit=…` 줄을 보고한다 — 필터 · 플래그 유무와 상관없이. `new` 나 `codegen_exit` 가 0 이 아니면 멈춘다
- **MUST** 이 스킬은 실행만 담당한다. 코드 수정은 별도 스킬에서 수행
- **MUST** 서브커맨드 없이 호출하면 사용 가능한 서브커맨드 목록을 출력한다
