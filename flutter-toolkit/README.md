# Flutter Toolkit

Flutter 프로젝트 공통 개발 스킬 모음. 프로젝트의 아키텍처, 의존성, 컨벤션을 자동 감지하여 적용한다.

## 스킬 목록

<!-- AUTO:skills -->
| 스킬 | 설명 |
| --- | --- |
| `flutter-api` | Clean Architecture 전 레이어를 일괄 또는 개별 생성한다. |
| `flutter-audit` | 코드 품질 감사. |
| `flutter-build` | 코드 생성(build_runner) + 정적 분석(flutter analyze)을 순서대로 실행한다. |
| `flutter-catalog` | 앱의 진짜 공용 위젯을 생성자에서 자동으로 읽어 놀이터 화면과 기본기 검사를 만든다. |
| `flutter-error` | Flutter 앱의 에러 처리 패턴을 안내한다. |
| `flutter-extract` | 재사용 가능한 위젯을 공용 위젯으로 추출한다. |
| `flutter-feature` | 새 feature 모듈을 프로젝트 아키텍처에 맞는 디렉토리 구조와 보일러플레이트 파일로 스캐폴딩한다. |
| `flutter-hooks` | Flutter Hooks 패턴 가이드. |
| `flutter-kaizen` | Flutter 스킬을 학술 논문·공식 문서·커뮤니티 리서치·skills.sh 마켓플레이스 기반으로 점진적으로 개선하는 카이젠 스킬. |
| `flutter-l10n` | i18n 파일에 번역 문자열을 추가/수정하고 codegen을 재생성한다. |
| `flutter-preflight` | Pre-commit quality gate. |
| `flutter-provider` | Riverpod Notifier + State 클래스를 생성한다. |
| `flutter-responsive` | 화면에 반응형 레이아웃을 적용하거나 기존 화면을 반응형으로 전환한다. |
| `flutter-run` | Flutter 빌드 프리미티브 실행 (codegen, analyze, fix, test). |
| `flutter-scenario-report` | Flutter 앱을 MCP 로 시나리오대로 실행하며 단계마다 캡처하고, 판정과 캡처를 모아 케이스마다 HTML 테스트 기록 보고서 한 장으로 만든다. |
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
| --- | --- |
| `widget-inspector` | 프로젝트 코드에서 재사용 가능한 위젯 패턴을 감지하고 리포팅한다. |
<!-- /AUTO:agents -->

## 훅

`format-edited-dart` (`scripts/format-edited-dart.sh`) — `PostToolUse` 훅. 파일을 고치는 도구(Edit · Write)가 끝나면 방금 고친 `.dart` 파일 하나만 `dart format` 한다.

- 대상은 도구 입력의 `tool_input.file_path` 하나뿐이다. 폴더 통째로 포맷하지 않는다 — 같은 작업 폴더를 다른 세션과 나눠 쓰면 남이 고친 파일까지 바뀐다
- `.g.dart` · `.freezed.dart` 같은 생성물과, 조상 폴더에 `pubspec.yaml` 이 없는 `.dart` 파일은 건너뛴다
- 프로젝트에 `.fvmrc` 가 있으면 `fvm dart format` 을 먼저 쓰고, 없으면 `dart format` 을 부른다
- 끄는 법: 환경 변수 `FLUTTER_TOOLKIT_FORMAT_ON_EDIT=off`
- 포맷이 실패해도 편집을 막지 않는다 (항상 exit 0)

`lint-edited-dart` (`scripts/lint-edited-dart.sh`) — 두 훅이 한 스크립트를 쓴다.
`PostToolUse`(Edit · Write · MultiEdit) 는 고친 `.dart` 파일 경로를 세션별 기록에
적기만 하고, `Stop` 은 답을 끝내기 직전에 그 기록의 파일만 `dart analyze` 한다.

- 오류·경고가 있으면 종료 코드 2 로 끝내 Claude 가 그 줄을 받아 고치게 한다.
  정보 항목은 돌려보내지 않는다
- 편집마다 분석하지 않는 이유: 큰 프로젝트는 파일 하나 분석에 40 초 넘게 걸렸다
- 다른 세션이 고친 파일은 섞이지 않는다. 같은 세션에서 이미 한 번
  막혔으면(`stop_hook_active`) 그다음은 통과시키고 기록은 남겨 다음 끝내기 때 다시 잰다
- `fvm` · `dart` 를 못 찾거나 분석기가 비정상 종료하면 막지 않고 「검사 못 함」 알림을 띄운다
- 끄는 법: 환경 변수 `FLUTTER_TOOLKIT_LINT_ON_STOP=off`.
  기록 위치는 `CLAUDE_LINT_STATE_DIR` (기본 `$TMPDIR/claude-lint-edited`)

## 화면 확인

`flutter-ui-verify` 는 UI 스킬을 거치지 않고 화면 코드를 직접 고친 뒤나 사용자가 화면 확인을 요청할 때, 편집 전·후 캡처를 대조하고 의도와 다르면 스스로 고쳐 다시 찍는다(최대 3 회). 절차는 `references/visual-evidence-protocol.md` 를 번호로 따른다.

## 레퍼런스

| 파일 | 용도 |
| --- | --- |
| `references/project-detection.md` | FVM 래퍼, 아키텍처 패턴, 의존성 등 프로젝트 환경 자동 감지 로직 |
| `references/flutter-ai-rules.md` | Flutter AI 코딩 규칙 (코드 생성 품질 가이드) |

## 참조 (Cross-Kit Principles)

본 kit 는 **harness/references/cross-kit-principles.md** 의 Phase 1 v1.3.0 신규 원칙 5 건 (Pre-Edit Batch Audit / Pre-Sprint Sync Check / Session Lifecycle / Hook-Triggered Auto-Correction / Self-Evaluator Rule-by-Rule Audit) 을 본 kit 의 audit / reviewer / sprint-entry 흐름에 적용한다. 매트릭스의 flutter-toolkit 열 참조.

## 요구사항

- FVM 설치 (Windows: `fvm.bat`)
- `.harness/project.yaml`의 `stack: flutter` 설정 (harness 플러그인 연동 시)
