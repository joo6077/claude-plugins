# Flutter Toolkit

Flutter 프로젝트 공통 개발 스킬 모음. 프로젝트의 아키텍처, 의존성, 컨벤션을 자동 감지하여 적용한다.

## 스킬 목록

<!-- AUTO:skills -->
| 스킬 | 설명 |
|------|------|
| `flutter-api` | Clean Architecture 전 레이어를 일괄 또는 개별 생성한다. |
| `flutter-audit` | 코드 품질 감사. quick 모드(단일 에이전트, 빠른 로컬 검토)와 deep 모드(최대 4에이전트 병렬 감사)를 지원한다. |
| `flutter-build` | 코드 생성(build_runner) + 정적 분석(flutter analyze)을 순서대로 실행한다. |
| `flutter-error` | Flutter 앱의 에러 처리 패턴을 안내한다. 데이터 계층에서 예외를 도메인 Failure로 |
| `flutter-extract` | 재사용 가능한 위젯을 공용 위젯으로 추출한다. |
| `flutter-feature` | 새 feature 모듈을 프로젝트 아키텍처에 맞는 디렉토리 구조와 보일러플레이트 파일로 스캐폴딩한다. |
| `flutter-hooks` | Flutter Hooks 패턴 가이드. HookWidget/HookConsumerWidget 사용 규칙, |
| `flutter-kaizen` | Flutter 스킬을 학술 논문·공식 문서·커뮤니티 리서치·skills.sh 마켓플레이스 |
| `flutter-l10n` | i18n 파일에 번역 문자열을 추가/수정하고 codegen을 재생성한다. |
| `flutter-preflight` | Pre-commit quality gate. fix → codegen → analyze → test 순서로 실행하고 |
| `flutter-provider` | Riverpod Notifier + State 클래스를 생성한다. |
| `flutter-responsive` | 화면에 반응형 레이아웃을 적용하거나 기존 화면을 반응형으로 전환한다. |
| `flutter-run` | Flutter 빌드 프리미티브 실행 (codegen, analyze, fix, test). |
| `flutter-scenario-report` | Flutter 앱을 Flutter Playwright MCP 로 시나리오대로 실행하며 단계마다 캡처하고, 판정과 캡처를 모아 HTML 테스트 기록 보고서로 만든다. |
| `flutter-screen` | Flutter Screen 또는 Page 위젯을 생성하고 GoRouter/auto_route에 등록한다. |
| `flutter-skeleton` | Flutter 화면/페이지의 로딩 상태를 스켈레톤 shimmer로 구현한다. |
| `flutter-test` | 대상 파일/클래스를 분석하여 Flutter 테스트 코드를 자동 생성한다. |
| `flutter-transition` | GoRouter, auto_route, Navigator 기반 커스텀 페이지 전환 애니메이션을 적용한다. |
| `flutter-ui-verify` | Flutter 앱 화면을 실제로 띄워 편집 전·후 캡처를 대조하고 의도와 다르면 스스로 고쳐 다시 찍는다. |
| `flutter-widget` | 프로젝트 컨벤션에 맞는 새 위젯을 생성한다. |
<!-- /AUTO:skills -->

## 에이전트 목록

<!-- AUTO:agents -->
| 에이전트 | 설명 |
|----------|------|
| `widget-inspector` | 프로젝트 코드에서 재사용 가능한 위젯 패턴을 감지하고 리포팅한다. |
<!-- /AUTO:agents -->

## 훅

`format-edited-dart` (`scripts/format-edited-dart.sh`) — `PostToolUse` 훅. 파일을 고치는 도구(Edit · Write)가 끝나면 방금 고친 `.dart` 파일 하나만 `dart format` 한다.

- 대상은 도구 입력의 `tool_input.file_path` 하나뿐이다. 폴더 통째로 포맷하지 않는다 — 같은 작업 폴더를 다른 세션과 나눠 쓰면 남이 고친 파일까지 바뀐다
- `.g.dart` · `.freezed.dart` 같은 생성물과, 조상 폴더에 `pubspec.yaml` 이 없는 `.dart` 파일은 건너뛴다
- 프로젝트에 `.fvmrc` 가 있으면 `fvm dart format` 을 먼저 쓰고, 없으면 `dart format` 을 부른다
- 끄는 법: 환경 변수 `FLUTTER_TOOLKIT_FORMAT_ON_EDIT=off`
- 포맷이 실패해도 편집을 막지 않는다 (항상 exit 0)

## 화면 확인

`flutter-ui-verify` 는 UI 스킬을 거치지 않고 화면 코드를 직접 고친 뒤나 사용자가 화면 확인을 요청할 때, 편집 전·후 캡처를 대조하고 의도와 다르면 스스로 고쳐 다시 찍는다(최대 3 회). 절차는 `references/visual-evidence-protocol.md` 를 번호로 따른다.

## 레퍼런스

| 파일 | 용도 |
|------|------|
| `references/project-detection.md` | FVM 래퍼, 아키텍처 패턴, 의존성 등 프로젝트 환경 자동 감지 로직 |
| `references/flutter-ai-rules.md` | Flutter AI 코딩 규칙 (코드 생성 품질 가이드) |

## 참조 (Cross-Kit Principles)

본 kit 는 **harness/references/cross-kit-principles.md** 의 Phase 1 v1.3.0 신규 원칙 5 건 (Pre-Edit Batch Audit / Pre-Sprint Sync Check / Session Lifecycle / Hook-Triggered Auto-Correction / Self-Evaluator Rule-by-Rule Audit) 을 본 kit 의 audit / reviewer / sprint-entry 흐름에 적용한다. 매트릭스의 flutter-toolkit 열 참조.

## 요구사항

- FVM 설치 (Windows: `fvm.bat`)
- `.harness/project.yaml`의 `stack: flutter` 설정 (harness 플러그인 연동 시)
