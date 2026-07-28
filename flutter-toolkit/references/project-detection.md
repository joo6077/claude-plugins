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

### Step 2b. Makefile 기반 monorepo 감지

프로젝트 루트에 `Makefile` 이 존재하고 Flutter 관련 타겟 (`app-run`, `app-test`, `app-analyze`, `app-codegen`, `app-preflight` 등) 이 정의되어 있으면 `HAS_MAKEFILE = true`. 이 경우 flutter-preflight / flutter-run 스킬은 `$FLUTTER` 직접 호출 대신 `make <target>` 을 우선 사용한다.

이유: Makefile 기반 monorepo (예: fit-pal) 는 `dart-define-from-file=.dart_defines.json`, `--observatory-port=8181`, launch.json/tasks.json 연동 설정을 Makefile 타겟 한 곳에 집중 관리한다. `fvm flutter run` 을 직접 호출하면 이 설정들이 누락되어 앱이 다른 환경으로 기동되거나 디버거가 연결되지 않는다 (fit-pal sprint-feedback iter 2 AC-6 기반).

감지 절차:

1. 프로젝트 루트에서 `Makefile` 존재 확인
2. Makefile 본문에 다음 타겟 중 하나 이상 존재하면 `HAS_MAKEFILE = true`:
   - `app-run`, `app-run-staging`, `app-run-prod`, `app-run-profile`
   - `app-test`, `app-analyze`, `app-fix`, `app-clean`
   - `app-codegen`, `app-codegen-filter`
   - `app-build`, `app-preflight`
3. `$MAKE = make` 변수를 제공 (Windows 에서는 `gmake` 또는 프로젝트 관습 우선)

`HAS_MAKEFILE = true` 일 때 주요 스킬 매핑:

| 스킬 | 기본 동작 | Makefile 우선 동작 |
|------|----------|-------------------|
| flutter-run codegen | `$DART run build_runner build --delete-conflicting-outputs` | `$MAKE app-codegen` (또는 `app-codegen-filter FILTER=...`) |
| flutter-run analyze | `$FLUTTER analyze` | `$MAKE app-analyze` |
| flutter-run fix | `$DART fix --apply lib/ && $DART format lib/` | `$MAKE app-fix` |
| flutter-run test | `$FLUTTER test` | `$MAKE app-test` |
| flutter-preflight | fix → codegen → analyze → test | `$MAKE app-preflight` |
| flutter-build | codegen → analyze | `$MAKE app-build` |

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
| `lib/features/*/ui/`, `lib/features/*/view_models/` 또는 `lib/*/views/`, `lib/*/view_models/` | `ARCH = mvvm` (MVVM — Flutter 공식 권장) |
| `lib/features/*/` (data/domain/presentation 없음) | `ARCH = feature_first` |
| `lib/src/` 또는 flat 구조 | `ARCH = flat` |

Clean Architecture 감지 시 레이어별 규칙 적용:
- `domain/` → `data/`, `presentation/` import 금지
- `data/` → `presentation/` import 금지
- Repository: interface(domain) + impl(data) 분리

MVVM 감지 시 레이어별 규칙 적용 ([Flutter 공식 아키텍처 가이드](https://docs.flutter.dev/app-architecture/guide)):
- **View** ↔ **ViewModel** 1:1 관계
- ViewModel: Repository에서 데이터를 받아 UI 상태로 변환, Command 패턴으로 액션 노출
- **Repository**: 도메인 모델 제공, 캐싱/에러처리/재시도 담당
- **Service**: 최하위 레이어, 외부 데이터 소스 래핑 (API, 파일, 플랫폼 코드)

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

### Step 8. 시각 검증 채널 감지 (UI 스킬 전용)

UI 를 만들거나 고치는 스킬(`flutter-widget` · `flutter-screen` · `flutter-skeleton` ·
`flutter-transition` · `flutter-responsive`)은 완료 선언 전에 렌더 결과를 대조해야 한다
(`references/visual-evidence-protocol.md`). 사용 가능한 채널을 아래 순서로 감지한다.

| 우선 | 채널 | 감지 방법 | 결과 |
|------|------|----------|------|
| 1 | golden test | `grep -rl "matchesGoldenFile" test/` 또는 `test/**/*golden*` 존재 | `VISUAL_CHANNEL = golden` |
| 2 | integration_test 스크린샷 | `integration_test/` 디렉토리 존재 | `VISUAL_CHANNEL = integration_test` |
| 3 | 프로젝트 등록 MCP | `.mcp.json` · `.claude/settings.json` · `.claude/settings.local.json` 의 `mcpServers` 키를 **읽어서** 서버명을 확인 | `VISUAL_CHANNEL = mcp:<서버명>` |
| 4 | 없음 | 위 3 개 모두 부재 | `VISUAL_CHANNEL = none` (degraded 모드) |

`HAS_VISUAL_CHANNEL` = `VISUAL_CHANNEL != none`.

**MCP 도구 이름을 추측하지 마라.** 프로젝트마다 등록된 서버와 도구 이름이 다르다. 설정 파일을
읽어 확인된 이름만 사용하고, 확인되지 않으면 그 채널은 없는 것으로 취급한다 — 존재하지 않는
도구를 호출한 뒤 실패를 "검증 완료" 로 넘기는 것이 `/insights` 2026-07-27 Friction #2 의 실제
사고 경로였다.

`HAS_VISUAL_CHANNEL = false` 이면 UI 스킬은 완료가 아니라 **부분 완료 + `[미검증]`** 으로 보고한다.

## 감지 결과 요약 템플릿

스킬이 내부적으로 사용하는 감지 결과 형식:

```text
Package: {name}
SDK Manager: {fvm|asdf|system}
Flutter: {$FLUTTER}
Dart: {$DART}
Makefile: {true|false}  # HAS_MAKEFILE — true 면 $MAKE <target> 우선
Architecture: {clean|feature_first|flat|mvvm}
Dependencies: {감지된 패키지 목록}
Design System: {true|false}
Widget Base: {HookWidget|StatelessWidget|ConsumerWidget}
State Management: {riverpod_codegen|riverpod_legacy|bloc|provider}
Router: {go_router_builder|go_router|auto_route|none}
i18n: {slang|easy_localization|intl|none}
Visual Channel: {golden|integration_test|mcp:<서버명>|none}  # HAS_VISUAL_CHANNEL — UI 스킬 전용
```

## 스킬에서 참조하는 방법

각 스킬의 첫 번째 단계:

```markdown
### 0. 프로젝트 감지

`references/project-detection.md`의 절차를 실행하여 프로젝트 환경을 파악한다.
이후 단계에서 감지 결과($FLUTTER, $DART, ARCH, HAS_* 등)를 사용한다.
```

의존성이 필요한 스킬은 해당 `HAS_*` 플래그를 확인하고, 없으면 안내 메시지를 출력한다.
