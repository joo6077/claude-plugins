# Flutter Toolkit · v0.5.0

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
| `flutter-screen` | Screen 또는 Page 위젯을 생성하고 라우터에 등록한다. |
| `flutter-skeleton` | 화면/페이지의 로딩 상태를 스켈레톤 shimmer로 구현한다. |
| `flutter-test` | 대상 파일/클래스를 분석하여 테스트 코드를 자동 생성한다. |
| `flutter-transition` | GoRouter, auto_route, Navigator 기반 커스텀 페이지 전환 애니메이션을 적용한다. |
| `flutter-widget` | 프로젝트 컨벤션에 맞는 새 위젯을 생성한다. |
<!-- /AUTO:skills -->

## 에이전트 목록

<!-- AUTO:agents -->
| 에이전트 | 설명 |
|----------|------|
| `widget-inspector` | 프로젝트 코드에서 재사용 가능한 위젯 패턴을 감지하고 리포팅한다. |
<!-- /AUTO:agents -->

## 레퍼런스

| 파일 | 용도 |
|------|------|
| `references/project-detection.md` | FVM 래퍼, 아키텍처 패턴, 의존성 등 프로젝트 환경 자동 감지 로직 |
| `references/flutter-ai-rules.md` | Flutter AI 코딩 규칙 (코드 생성 품질 가이드) |

## 요구사항

- FVM 설치 (Windows: `fvm.bat`)
- `.harness/project.yaml`의 `stack: flutter` 설정 (harness 플러그인 연동 시)
