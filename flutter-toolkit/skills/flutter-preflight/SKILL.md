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

`$ARGUMENTS`: feature 이름 (optional, e.g., `auth`). 지정하면 codegen에 해당 feature만 적용.

## Steps

순서의 이유: fix로 자동 수정 → codegen으로 생성 파일 갱신 → analyze로 남은 이슈 확인 → test로 동작 검증. 이 순서가 아니면 fix가 codegen 결과를 덮어쓰거나, analyze가 outdated 생성 파일을 검사하게 된다.

### 1. fix

자동 수정 가능한 린트 이슈를 고치고 포맷을 통일한다:

```bash
$DART fix --apply lib/
$DART format lib/
```

실패 시 즉시 중단.

### 2. codegen [feature]

`HAS_BUILD_RUNNER`이면 실행:

```bash
$DART run build_runner build --delete-conflicting-outputs
```

feature 인자가 있으면:

```bash
$DART run build_runner build --delete-conflicting-outputs --build-filter="lib/features/$FEATURE/**"
```

`HAS_BUILD_RUNNER = false`이면 skip. 실패 시 즉시 중단.

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

```
Preflight passed

  1. fix     : success
  2. codegen : success (또는 skipped)
  3. analyze : clean
  4. test    : N passed (또는 skipped)

Ready to commit.
```

하나라도 실패하면:

```
Preflight failed at step N

  1. fix     : success
  2. codegen : success
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
