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
- `build_runner build`에 `--delete-conflicting-outputs` 플래그 필수 — 없으면 `.freezed.dart`/`.g.dart` 충돌로 빌드 실패
- `.dart_defines.json` 파일 없으면 앱 실행 불가 — codegen 전에 존재 여부 확인

# Build (codegen + analyze)

`flutter-run` 스킬의 `codegen`과 `analyze`를 순서대로 실행하는 thin wrapper.

## 0. 프로젝트 감지

`references/project-detection.md`의 절차를 실행하여 프로젝트 환경을 파악한다.
이후 단계에서 감지 결과(`$FLUTTER`, `$DART`, `HAS_BUILD_RUNNER`)를 사용한다.

## Input

`$ARGUMENTS`: feature 이름 (optional, e.g., `auth`, `workout`)

## Steps

### 1. codegen [feature]

`HAS_BUILD_RUNNER`이면 codegen 실행:

```bash
$DART run build_runner build --delete-conflicting-outputs
```

feature 인자가 있으면 해당 feature만 빌드:

```bash
$DART run build_runner build --delete-conflicting-outputs --build-filter="lib/features/$FEATURE/**"
```

`HAS_BUILD_RUNNER = false`이면 이 단계를 건너뛴다.

codegen이 실패하면 analyze를 실행하지 않고 즉시 중단한다 — 생성 파일이 깨진 상태에서 분석해봐야 의미 없기 때문.

### 2. analyze

codegen 성공 시 (또는 codegen 스킵 시) 정적 분석 실행:

```bash
$FLUTTER analyze
```

### 3. Report

두 단계 결과를 통합 요약:

```
build 완료
  1. codegen : success (또는 skipped)
  2. analyze : clean (0 issues)
```

실패 시:

```
build 실패 (step N)
  1. codegen : success / failed / skipped
  2. analyze : success / failed / skipped
  [에러 내용]
```
