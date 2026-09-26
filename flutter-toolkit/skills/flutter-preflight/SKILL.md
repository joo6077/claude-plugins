---
name: flutter-preflight
description: >
  Pre-commit quality gate. fix → codegen → analyze → test 순서로 실행하고
  결과를 요약 보고한다. 커밋 전 코드 품질 검증, pre-commit 체크,
  린트+포맷+빌드+테스트 일괄 실행할 때 사용한다.
  "preflight", "프리플라이트", "커밋 전 검사", "pre-commit",
  "린트+포맷+빌드+테스트", "quality gate", "품질 게이트" 같은 요청 시 사용한다.
argument-hint: "[feature]"
user-invocable: true
---

## Gotchas

- anti-pattern 5개가 자동 체크된다: StatefulWidget, bare catch(e), 상대 import, GestureDetector/InkWell, Palette 직접 참조 — 하나라도 걸리면 preflight FAIL
- FVM 미설치 환경에서 preflight 실행하면 모든 단계가 실패한다 — 먼저 FVM 존재를 확인해라
- test 단계에서 콘솔 에러 패턴 4개를 체크한다: "EXCEPTION CAUGHT BY", "RenderFlex overflowed", "setState() called after dispose", "Null check operator" — 테스트 통과해도 이 패턴 있으면 FAIL
- Makefile 기반 프로젝트에서는 단계마다 그 타겟(`app-fix` · `app-codegen` · `app-analyze` · `app-test`)이 Makefile 에 있을 때만 `make` 로 돌린다 — `references/project-detection.md` Step 2b 4 번의 타겟별 확인으로 한 타겟씩 보고, 타겟이 없는 단계는 기본 명령을 쓴다. `Makefile` 이 있다는 것만 보고 `make app-test` 를 부르면 `app-preflight` 묶음 타겟만 있는 Makefile 에서 없는 타겟을 불러 멈춘다. 타겟이 있으면 `make` 를 먼저 쓰는 까닭은 dart-define · observatory-port 설정이 그 타겟에 모여 있어서다

# Preflight (Pre-commit Quality Gate)

커밋 전 품질 게이트. `flutter-run` 스킬의 프리미티브를 순서대로 호출하는 thin wrapper.

## 0. 프로젝트 감지

`references/project-detection.md`의 절차를 실행하여 프로젝트 환경을 파악한다.
이후 단계에서 감지 결과(`$FLUTTER`, `$DART`, `HAS_BUILD_RUNNER`)를 사용한다.

### 사용 가능한 단계 감지

| 단계 | 조건 | 없으면 |
|------|------|--------|
| fix | 항상 사용 가능 | — |
| codegen | `HAS_BUILD_RUNNER = true` | skip |
| analyze | 항상 사용 가능 | — |
| test | `test/` 디렉토리에 `*_test.dart` 파일 존재 | skip |

## Input

`$ARGUMENTS`: feature 이름 (optional, e.g., `auth`). 보고에 적기만 하고 codegen 범위를 좁히지 않는다.

## Steps

순서의 이유: fix로 자동 수정 → codegen으로 생성 파일 갱신 → analyze로 남은 이슈 확인 → test로 동작 검증. 이 순서가 아니면 fix가 codegen 결과를 덮어쓰거나, analyze가 outdated 생성 파일을 검사하게 된다.

### 1. fix

자동 수정 가능한 린트 이슈를 고치고, 이번에 바뀐 .dart 파일만 포맷한다 (`flutter-run` fix 절과 같은 명령):

```bash
# dart fix 는 경로를 하나만 받는다. 파일을 여럿 주면 exit 64
$DART fix --apply lib/
CHANGED=$( { git diff --name-only --relative --diff-filter=ACMR HEAD -- '*.dart'
             git ls-files --others --exclude-standard -- '*.dart'; } \
           | grep -vE '\.(g|freezed|gr|mocks|config|gen)\.dart$' )
if [ -n "$CHANGED" ]; then
  printf '%s\n' "$CHANGED" | tr '\n' '\0' | xargs -0 $DART format --
else
  echo "포맷 건너뜀 — 이번에 바뀐 .dart 파일 없음"
fi
```

`lib/` 를 통째로 포맷하지 않는다 — 이번에 손대지 않은 파일까지 바뀌어 커밋 범위가 흐려진다.
목록이 비면 포맷을 건너뛰고 Report 의 fix 줄에 `포맷 건너뜀 (바뀐 .dart 없음)` 을 적는다.

실패 시 즉시 중단.

### 2. codegen [feature]

`HAS_BUILD_RUNNER`이면 필터 없이 전체 codegen 을 돌리고 전후 삭제 수를 센다 (`flutter-run` codegen 절과 같은 블록).
feature 인자가 와도 `--build-filter` 를 붙이지 않는다 — 인자는 보고에 적기만 하고 범위를 좁히지 않는다:

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

`HAS_BUILD_RUNNER = false`이면 skip. 실패 시 즉시 중단. `new` 가 0 이 아니면 그것도 실패다 — 멈춰서 `늘어난 삭제` 목록을 보고하고,
맞는 삭제일 수 있으니 되돌리지 말고 목록을 보인다.
생성물을 git 에 올리지 않는 프로젝트에서는 이 세기가 생성물 삭제를 보지 못해 늘 0 이다 — `git ls-files -- '*.g.dart' '*.freezed.dart'` 가 비면 `new=0` 을 통과로 쓰지 말고 보고 줄 뒤에 `추적된 생성물 0 개 — 삭제를 셀 수 없다` 를 붙인다.

### 3. analyze

정적 분석 실행:

```bash
$FLUTTER analyze
```

에러 발생 시 즉시 중단. warning은 보고만 하고 계속 진행.

### 4. test

테스트 파일이 존재하면 실행:

```bash
$FLUTTER test
```

테스트 파일이 없으면 skip.

### 5. Report

모든 단계 결과를 수집하여 최종 요약:

```text
Preflight passed

  1. fix     : success (포맷 N 파일 또는 포맷 건너뜀 (바뀐 .dart 없음))
  2. codegen : success · 삭제 before=N after=N new_first=N new=0 codegen_exit=0 (또는 skipped)
  3. analyze : clean
  4. test    : N passed (또는 skipped)

Ready to commit.
```

하나라도 실패하면:

```text
Preflight failed at step N

  1. fix     : success
  2. codegen : success / failed / skipped · 삭제 before=N after=N new_first=N new=N codegen_exit=N (skipped 면 없음)
     [늘어난 삭제 — new 가 0 이 아니면 그 목록]
  3. analyze : failed (N errors)
     [에러 목록]
  4. test    : skipped

Fix the issues above before committing.
```

## Rules

- **MUST** 순서 엄수: fix → codegen → analyze → test
- **MUST** 어느 단계든 에러 발생 시 즉시 중단하고 보고
- **MUST** warning은 보고하되 중단하지 않음 (error만 중단)
- **MUST** 사용 불가능한 단계(build_runner 없음, 테스트 없음)는 skip으로 표시
