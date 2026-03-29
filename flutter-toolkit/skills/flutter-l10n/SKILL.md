---
name: flutter-l10n
description: >
  i18n 파일에 번역 문자열을 추가/수정하고 codegen을 재생성한다.
  slang, easy_localization, intl(ARB), flutter_localizations 등 프로젝트의 i18n 라이브러리를 자동 감지하여 적용한다.
  다국어, 번역, 로컬라이제이션, localization, 문자열 추가, i18n 키,
  "번역 추가해줘", "다국어 지원", "l10n", "i18n key" 같은 요청 시 사용한다.
argument-hint: "<feature.key> | <text> [| <text2>]"
user-invocable: true
---

## Gotchas

- i18n 라이브러리를 자동 감지한다(slang, easy_localization, intl 등) — 감지 결과를 무시하고 특정 라이브러리를 가정하면 안 된다
- 번역 키 추가 후 반드시 codegen 재실행 — slang은 `fvm dart run slang`, intl은 `fvm flutter gen-l10n`
- 키 네이밍은 프로젝트 기존 패턴을 따른다 — 새 네이밍 규칙을 임의로 만들지 마라

i18n 파일에 번역 문자열을 추가/수정하고 codegen을 재생성한다.

## 0. 프로젝트 감지

`references/project-detection.md`의 절차를 실행하여 프로젝트 환경을 파악한다.
이후 단계에서 감지 결과(`$FLUTTER`, `$DART`, `$PACKAGE`, `HAS_SLANG`, `HAS_EASY_L10N`, `HAS_BUILD_RUNNER` 등)를 사용한다.

### i18n 라이브러리 감지

| 감지 키 | 패키지 | 파일 패턴 | 키 포맷 | 접근 패턴 |
|---------|--------|----------|---------|----------|
| `HAS_SLANG` | `slang` / `slang_flutter` | `lib/**/i18n/*.i18n.json` | camelCase | `t.<feature>.<key>` |
| `HAS_EASY_L10N` | `easy_localization` | `assets/translations/*.json` | snake_case | `'feature.key'.tr()` |
| `HAS_INTL` | `flutter_localizations` + `intl` | `lib/l10n/*.arb` | camelCase | `AppLocalizations.of(context).<key>` |

**i18n 라이브러리가 없으면:**
> "i18n 라이브러리가 pubspec.yaml에 없습니다. 다국어 지원을 추가하려면 먼저 설치해주세요:
> - Slang: `$FLUTTER pub add slang_flutter && $FLUTTER pub add dev:slang_build_runner`
> - easy_localization: `$FLUTTER pub add easy_localization`
> - Flutter intl: `$FLUTTER pub add flutter_localizations --sdk=flutter && $FLUTTER pub add intl`"

### i18n 파일 위치

#### Slang
- **일반적 경로**: `lib/i18n/`, `lib/core/i18n/`, `lib/l10n/`
- **파일 패턴**: `{locale}.i18n.json` (예: `en.i18n.json`, `ko.i18n.json`)
- **감지**: `slang.yaml` 또는 `build.yaml`의 slang 설정에서 `input_directory` 확인

#### easy_localization
- **일반적 경로**: `assets/translations/`, `assets/lang/`
- **파일 패턴**: `{locale}.json` (예: `en.json`, `ko.json`)

#### intl/ARB
- **일반적 경로**: `lib/l10n/`
- **파일 패턴**: `app_{locale}.arb` (예: `app_en.arb`, `app_ko.arb`)

### 지원 언어 감지

기존 i18n 파일들에서 언어 코드를 추출한다:
- Slang: `{locale}.i18n.json` 파일명에서 추출 (예: `en.i18n.json`, `ko.i18n.json`)
- easy_localization: `{locale}.json` 파일명에서 추출 (예: `en.json`, `ko.json`)
- intl/ARB: `app_{locale}.arb` 파일명에서 추출 (예: `app_en.arb`, `app_ko.arb`)

## Input

`$ARGUMENTS` format -- 구분자 `|`를 사용하여 key와 각 언어 텍스트를 분리:
- `<feature.key> | <text1> | <text2>` -- 감지된 언어 순서대로 번역 제공
- `<feature.key> | <text1>` -- 첫 번째 언어만 제공, 나머지는 사용자에게 질문
- (no args) -- interactive mode: 추가할 문자열을 사용자에게 질문

Examples:
- `/flutter-l10n workout.title | Workouts | 운동`
- `/flutter-l10n common.save | Save | 저장`
- `/flutter-l10n home.welcomeUser | Welcome, ${name} | ${name}님, 환영합니다`

> 파싱 규칙: `|`로 split하고 각 부분을 trim한다. `|`가 없으면 첫 토큰을 key로, 나머지를 첫 번째 언어 텍스트로 취급하되 나머지 언어는 사용자에게 질문한다.

## Steps

### 1. i18n 파일 읽기

감지된 라이브러리에 따라 파일을 읽는다:

| 라이브러리 | 읽을 파일 |
|-----------|----------|
| Slang | `lib/**/i18n/{locale}.i18n.json` (모든 감지된 locale) |
| easy_localization | `assets/translations/{locale}.json` (모든 감지된 locale) |
| intl/ARB | `lib/l10n/app_{locale}.arb` (모든 감지된 locale) |

### 2. Key 파싱 및 삽입

`$ARGUMENTS`에서 key를 파싱한다.

**Slang / easy_localization (JSON)**:
- `.`으로 분리하여 JSON 중첩 경로 결정 (예: `workout.title` -> `{"workout": {"title": "..."}}`)
- 최상위 키가 없으면 생성
- 키가 이미 있으면 사용자에게 덮어쓸지 확인
- **MUST** 최상위 키를 알파벳순으로 유지

**intl/ARB**:
- flat 키로 삽입: `workout.title` -> `"workoutTitle": "..."` (dot을 camelCase로 변환)
- `@workoutTitle` 메타데이터 항목도 함께 추가

### 3. 키 네이밍 규칙

| 라이브러리 | 네이밍 규칙 | 예시 |
|-----------|-----------|------|
| Slang | camelCase | `welcomeUser`, `itemCount` |
| easy_localization | snake_case | `welcome_user`, `item_count` |
| intl/ARB | camelCase | `welcomeUser`, `itemCount` |

### 4. 보간(interpolation) 문법

| 라이브러리 | 문법 | 예시 |
|-----------|------|------|
| Slang | `${varName}` | `"Welcome, ${name}"` |
| easy_localization | `{varName}` | `"Welcome, {name}"` |
| intl/ARB | `{varName}` | `"Welcome, {name}"` |

### 5. 모든 locale 파일에 키 추가

감지된 모든 언어 파일에 키를 추가한다. 제공되지 않은 언어의 텍스트는 사용자에게 질문한다.

### 6. Codegen 실행

| 라이브러리 | 명령 |
|-----------|------|
| Slang | `$DART run build_runner build --delete-conflicting-outputs --build-filter="lib/**/i18n/**"` |
| easy_localization | codegen 불필요 (런타임 로드) |
| intl/ARB | `$FLUTTER gen-l10n` |

### 7. 보고

- 추가/수정된 키
- 사용 예시 (라이브러리별):
  - Slang: `t.<feature>.<key>` 또는 `t.<feature>.<key>(name: value)`
  - easy_localization: `'<feature>.<key>'.tr()` 또는 `'<feature>.<key>'.tr(namedArgs: {'name': value})`
  - intl/ARB: `AppLocalizations.of(context).<key>` 또는 `AppLocalizations.of(context).<key>(value)`

## Rules

- **MUST** 모든 locale 파일의 키를 항상 동기화한다 -- 한쪽에만 키가 있으면 해당 언어로 전환 시 키 이름이 그대로 노출되거나 빌드가 실패한다
- **MUST** 유효한 JSON/ARB 포맷을 유지한다 (trailing comma 금지) -- codegen이 파싱에 실패하면 전체 빌드가 중단된다
- **MUST** 라이브러리별 키 네이밍 규칙을 따른다 -- 생성 코드의 접근 패턴이 네이밍 규칙에 의존한다
- **MUST** 키는 feature 이름과 일치하는 그룹 아래에 중첩한다 (JSON 기반) -- feature별로 번역 키가 분리되어야 충돌 없이 독립 관리할 수 있다
- **MUST** 최상위 키를 알파벳순으로 유지한다 -- diff 충돌을 최소화하고 키를 찾기 쉽게 한다
- **MUST** codegen이 필요한 라이브러리는 키 추가 후 반드시 codegen을 실행한다
- **MUST** `$DART` / `$FLUTTER` 변수를 사용한다. 하드코딩된 `fvm dart`, `dart`, `flutter` 직접 사용 금지
