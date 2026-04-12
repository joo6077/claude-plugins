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
- **Dart macros 개발 중단 (2025-01)** — Dart 팀이 macro 기능 개발을 무기한 중단했다. JIT/AOT 컴파일, tree-shaking, reflection 부재로 구현 복잡도가 너무 높았음. `build_runner` 기반 코드 생성이 당분간 유일한 공식 경로이므로 build_runner 의존을 제거하려는 계획은 보류하라 (출처: <https://dart.dev/resources/language/evolution>)
- **build_runner 2x 속도 향상 (2025-12)** — transitive import 추적 전면 재작성으로 3,000 생성 라이브러리 테스트에서 2배 속도 개선. 최신 `build_runner` 버전을 사용하면 codegen 시간이 크게 단축된다 (출처: codewithandrea.com/newsletter/december-2025)
- **Dart 3.10 dot shorthands** — `.center` 처럼 타입 이름을 생략하고 enum / static member / constructor 에 dot shorthand 사용 가능. UI-heavy 파일에서 보일러플레이트 10-15% 감소. analyze 에서 새 lint 가 활성화될 수 있으므로 `dart fix --apply` 로 자동 적용 권장 (출처: <https://dart.dev/resources/language/evolution>)

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

```text
build 완료
  1. codegen : success (또는 skipped)
  2. analyze : clean (0 issues)
```

실패 시:

```text
build 실패 (step N)
  1. codegen : success / failed / skipped
  2. analyze : success / failed / skipped
  [에러 내용]
```
