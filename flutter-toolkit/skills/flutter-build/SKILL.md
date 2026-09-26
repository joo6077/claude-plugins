---
name: flutter-build
description: >
  코드 생성(build_runner) + 정적 분석(flutter analyze)을 순서대로 실행한다.
  내부적으로 flutter-run 스킬의 codegen + analyze를 호출한다.
  "빌드해줘", "코드 생성 + 분석", "codegen 돌리고 analyze까지",
  "build", "빌드", "코드생성+분석" 같은 요청 시 사용한다.
argument-hint: "[feature]"
user-invocable: true
---

## Gotchas

- 반드시 FVM 경유: `fvm flutter`, `fvm dart` — bare `flutter`/`dart` 명령은 SDK 버전 불일치로 codegen 실패 가능
- Windows에서는 `fvm.bat` 사용 — `fvm` 직접 호출하면 PATH 이슈
- **`--delete-conflicting-outputs` 로 생성물이 안전하다고 믿지 마라** — build_runner 2.16 부터 잘못되거나 고쳐진 생성물을 기본으로 고치고, 이 플래그는 제거된 호환 옵션 목록으로 옮겨졌다(2.16.1 · 2026-09-24 조회). 플래그를 빼도 생성물이 고쳐지거나 지워질 수 있으니 전후 삭제 수를 센다 (출처: <https://raw.githubusercontent.com/dart-lang/build/master/build_runner/CHANGELOG.md>). 그래도 명령에서 빼지 않는다 — 2.7.0 부터는 이 플래그를 무시하고 늘 지우지만(pub 설치본 `build_runner-2.13.1/CHANGELOG.md:150`), 2.7.0 미만(2.3.3 · 2.4.x 가 쓰는 `build_runner_core` 7.3.2 · 8.0.0 의 `build_definition.dart:564-570`)은 이 플래그가 없으면 대화 없이 도는 실행에서 충돌하는 생성물 앞에서 빌드를 멈춘다
- `.dart_defines.json` 파일 없으면 앱 실행 불가 — codegen 전에 존재 여부 확인
- **Dart macros 개발 중단 (2025-01)** — Dart 팀이 macro 기능 개발을 무기한 중단했다. JIT/AOT 컴파일, tree-shaking, reflection 부재로 구현 복잡도가 너무 높았음. `build_runner` 기반 코드 생성이 당분간 유일한 공식 경로이므로 build_runner 의존을 제거하려는 계획은 보류하라 (출처: <https://dart.dev/resources/language/evolution>)
- **build_runner 2x 속도 향상 (2025-12)** — transitive import 추적 전면 재작성으로 3,000 생성 라이브러리 테스트에서 2배 속도 개선. 최신 `build_runner` 버전을 사용하면 codegen 시간이 크게 단축된다 (출처: codewithandrea.com/newsletter/december-2025)
- **Dart 3.10 dot shorthands** — `.center` 처럼 타입 이름을 생략하고 enum / static member / constructor 에 dot shorthand 사용 가능. UI-heavy 파일에서 보일러플레이트 10-15% 감소. analyze 에서 새 lint 가 활성화될 수 있으므로 `dart fix --apply` 로 자동 적용 권장 (출처: <https://dart.dev/resources/language/evolution>)

# Build (codegen + analyze)

`flutter-run` 스킬의 `codegen`과 `analyze`를 순서대로 실행하는 thin wrapper.

## 0. 프로젝트 감지

`references/project-detection.md`의 절차를 실행하여 프로젝트 환경을 파악한다.
이후 단계에서 감지 결과(`$FLUTTER`, `$DART`, `HAS_BUILD_RUNNER`)를 사용한다.

## Input

`$ARGUMENTS`: feature 이름 (optional, e.g., `auth`, `workout`) — 보고에 적기만 하고 codegen 범위를 좁히지 않는다

## Steps

### 1. codegen [feature]

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

`new` 가 0 이 아니면 analyze 로 가지 않고 멈춰서 `늘어난 삭제` 목록을 보고한다 — 맞는 삭제일 수 있으니 되돌리지 말고 목록을 보인다.
생성물을 git 에 올리지 않는 프로젝트에서는 이 세기가 생성물 삭제를 보지 못해 늘 0 이다 — `git ls-files -- '*.g.dart' '*.freezed.dart'` 가 비면 `new=0` 을 통과로 쓰지 말고 보고 줄 뒤에 `추적된 생성물 0 개 — 삭제를 셀 수 없다` 를 붙인다.

`HAS_BUILD_RUNNER = false`이면 이 단계를 건너뛴다.

codegen이 실패하면 analyze를 실행하지 않고 즉시 중단한다 — 생성 파일이 깨진 상태에서 분석해봐야 의미 없기 때문.

### 2. analyze

codegen 성공 시 (또는 codegen 스킵 시) 정적 분석 실행:

```bash
$FLUTTER analyze
```

### 3. Report

두 단계 결과를 통합 요약:

```text
build 완료
  1. codegen : success · 삭제 before=N after=N new_first=N new=0 codegen_exit=0 (또는 skipped)
  2. analyze : clean (0 issues)
```

실패 시:

```text
build 실패 (step N)
  1. codegen : success / failed / skipped · 삭제 before=N after=N new_first=N new=N codegen_exit=N (skipped 면 없음)
     [늘어난 삭제 — new 가 0 이 아니면 그 목록]
  2. analyze : success / failed / skipped
  [에러 내용]
```
