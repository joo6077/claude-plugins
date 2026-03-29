# Flutter Toolkit

Flutter 프로젝트 공통 개발 스킬 모음. 프로젝트의 아키텍처, 의존성, 컨벤션을 자동 감지하여 적용한다.

## 스킬 목록 (16개)

| 스킬 | 설명 |
|------|------|
| `flutter-api` | Clean Architecture 전 레이어 일괄/개별 생성 (DataSource → Model → Repository → UseCase) |
| `flutter-audit` | 코드 품질 감사 (quick/deep 모드) |
| `flutter-build` | 코드 생성(build_runner) + 정적 분석(flutter analyze) |
| `flutter-error` | 에러 처리 패턴 가이드 (예외 → Failure → UI) |
| `flutter-extract` | 재사용 가능한 위젯 추출 (private→shared, 인라인 분리, 중복 통합) |
| `flutter-feature` | 새 feature 모듈 스캐폴딩 |
| `flutter-hooks` | Flutter Hooks 패턴 가이드 + StatefulWidget 마이그레이션 |
| `flutter-l10n` | i18n 번역 문자열 추가/수정 + codegen |
| `flutter-preflight` | Pre-commit quality gate (fix → codegen → analyze → test) |
| `flutter-provider` | Riverpod Notifier + State 생성 |
| `flutter-responsive` | 반응형 레이아웃 적용/전환 |
| `flutter-run` | Flutter 빌드 프리미티브 실행 (codegen, analyze, fix, test) |
| `flutter-screen` | Screen/Page 위젯 생성 + 라우터 등록 |
| `flutter-skeleton` | 로딩 스켈레톤 shimmer 구현 |
| `flutter-transition` | 커스텀 페이지 전환 애니메이션 |
| `flutter-widget` | 프로젝트 컨벤션에 맞는 위젯 생성 |

## 에이전트 목록 (1개)

| 에이전트 | 설명 |
|----------|------|
| `widget-inspector` | 재사용 가능한 위젯 패턴 감지 + 리포팅 (읽기 전용, quick/deep 모드) |

## 요구사항

- FVM 설치 (Windows: `fvm.bat`)
- `.harness/project.yaml`의 `stack: flutter` 설정 (harness 플러그인 연동 시)
