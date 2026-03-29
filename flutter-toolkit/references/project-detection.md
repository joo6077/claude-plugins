# Project Detection (SSOT)

모든 flutter-toolkit 스킬은 코드 생성/명령 실행 전에 이 문서의 절차로 프로젝트 환경을 감지한다.
감지 결과를 기반으로 스킬 동작을 분기한다.

## 감지 절차

스킬 실행 시 아래 순서로 프로젝트 환경을 파악한다.

### Step 1. Flutter 프로젝트 확인

`pubspec.yaml`을 찾는다. 없으면 에러:
> "Flutter 프로젝트가 아닙니다. pubspec.yaml이 있는 디렉토리에서 실행해주세요."

pubspec.yaml에서 추출:
- `name` → **패키지명** (import 경로에 사용: `package:{name}/...`)
- `environment.sdk` → Dart SDK 버전

### Step 2. SDK 매니저 감지

| 파일 | SDK 매니저 | 명령 prefix |
|------|-----------|------------|
| `.fvmrc` 또는 `.fvm/fvm_config.json` | FVM | `fvm flutter`, `fvm dart` |
| `.tool-versions` (asdf flutter 항목) | asdf | `flutter`, `dart` |
| 없음 | 시스템 | `flutter`, `dart` |

감지 결과를 `$FLUTTER`, `$DART` 변수로 참조:
- FVM: `$FLUTTER = fvm flutter`, `$DART = fvm dart`
- 기타: `$FLUTTER = flutter`, `$DART = dart`

### Step 3. 의존성 감지

`pubspec.yaml`의 `dependencies` + `dev_dependencies`에서 감지:

| 패키지 | 감지 키 | 영향받는 스킬 |
|--------|---------|-------------|
| `flutter_riverpod` 또는 `hooks_riverpod` | `HAS_RIVERPOD` | flutter-provider |
| `go_router` | `HAS_GO_ROUTER` | flutter-screen, flutter-transition |
| `go_router_builder` | `HAS_GO_ROUTER_BUILDER` | flutter-screen (TypedGoRoute codegen) |
| `freezed` | `HAS_FREEZED` | flutter-api, flutter-feature |
| `retrofit` | `HAS_RETROFIT` | flutter-api |
| `build_runner` | `HAS_BUILD_RUNNER` | flutter-run (codegen) |
| `slang` 또는 `slang_flutter` | `HAS_SLANG` | flutter-l10n |
| `easy_localization` | `HAS_EASY_L10N` | flutter-l10n |
| `flutter_hooks` 또는 `hooks_riverpod` | `HAS_HOOKS` | flutter-hooks, flutter-widget |
| `custom_lint` | `HAS_CUSTOM_LINT` | flutter-audit |
| `auto_route` | `HAS_AUTO_ROUTE` | flutter-screen, flutter-transition |
| `auto_route_generator` | (auto_route와 같이 감지) | flutter-screen |
| `flutter_bloc` 또는 `bloc` | `HAS_BLOC` | flutter-provider, flutter-audit |
| `dio` | `HAS_DIO` | flutter-api |

의존성이 없는 기능을 요청하면:
> "{패키지}가 pubspec.yaml에 없습니다. 이 기능을 사용하려면 먼저 설치해주세요:
> `$FLUTTER pub add {패키지}`"

### Step 4. 아키텍처 패턴 감지

`lib/` 디렉토리 구조를 분석:

| 패턴 | 감지 결과 |
|------|----------|
| `lib/features/*/data/`, `lib/features/*/domain/`, `lib/features/*/presentation/` | `ARCH = clean` (Clean Architecture) |
| `lib/features/*/` (data/domain/presentation 없음) | `ARCH = feature_first` |
| `lib/src/` 또는 flat 구조 | `ARCH = flat` |

Clean Architecture 감지 시 레이어별 규칙 적용:
- `domain/` → `data/`, `presentation/` import 금지
- `data/` → `presentation/` import 금지
- Repository: interface(domain) + impl(data) 분리

### Step 5. 코드 컨벤션 감지

기존 코드에서 패턴을 읽어 생성 코드에 적용:

| 항목 | 감지 방법 | 기본값 |
|------|----------|--------|
| Import 스타일 | 기존 `.dart` 파일의 import 패턴 | `package:{name}/...` (절대경로) |
| 위젯 베이스 | `HookWidget` vs `StatelessWidget` 사용 비율 | `StatelessWidget` |
| State 관리 | `@riverpod` vs `StateNotifierProvider` 사용 | codegen(`@riverpod`) |
| 네이밍 | `Screen` vs `Page` vs `View` 접미사 관행 | `Screen`/`Page` |
| 라우트 패턴 | `TypedGoRoute` vs `GoRoute()` | 프로젝트에서 감지 |

### Step 6. 분석 도구 감지

`analysis_options.yaml`에서:
- `include:` → 린트 패키지 (very_good_analysis, flutter_lints, 커스텀)
- `analyzer.plugins:` → custom_lint 사용 여부

### Step 7. 디자인 시스템 감지

| 패턴 | 감지 결과 |
|------|----------|
| `lib/*/design_system/` 또는 `lib/*/theme/` 또는 `lib/*/tokens/` | `HAS_DS = true`, 경로 기록 |
| `context.colors.` 패턴이 기존 코드에 있음 | Semantic Token 사용 |
| 없음 | `HAS_DS = false`, 디자인 시스템 규칙 스킵 |

## 감지 결과 요약 템플릿

스킬이 내부적으로 사용하는 감지 결과 형식:

```
Package: {name}
SDK Manager: {fvm|asdf|system}
Flutter: {$FLUTTER}
Dart: {$DART}
Architecture: {clean|feature_first|flat}
Dependencies: {감지된 패키지 목록}
Design System: {true|false}
Widget Base: {HookWidget|StatelessWidget|ConsumerWidget}
State Management: {riverpod_codegen|riverpod_legacy|bloc|provider}
Router: {go_router_builder|go_router|auto_route|none}
i18n: {slang|easy_localization|intl|none}
```

## 스킬에서 참조하는 방법

각 스킬의 첫 번째 단계:

```markdown
### 0. 프로젝트 감지

`references/project-detection.md`의 절차를 실행하여 프로젝트 환경을 파악한다.
이후 단계에서 감지 결과($FLUTTER, $DART, ARCH, HAS_* 등)를 사용한다.
```

의존성이 필요한 스킬은 해당 `HAS_*` 플래그를 확인하고, 없으면 안내 메시지를 출력한다.
