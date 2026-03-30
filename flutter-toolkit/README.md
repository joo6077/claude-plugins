# Flutter Toolkit · v0.5.0

Flutter 프로젝트 공통 개발 스킬 모음. 프로젝트의 아키텍처, 의존성, 컨벤션을 자동 감지하여 적용한다.

## 스킬 목록 (18개)

| 스킬 | 설명 |
|------|------|
| `flutter-api` | Clean Architecture 전 레이어 일괄/개별 생성 (DataSource(Retrofit) → Model(Freezed) → Repository → UseCase) |
| `flutter-audit` | 코드 품질 감사 — quick 모드(단일 에이전트, 빠른 로컬 검토) / deep 모드(최대 4에이전트 병렬 감사) |
| `flutter-build` | 코드 생성(build_runner) + 정적 분석(flutter analyze) 순서 실행 |
| `flutter-error` | Flutter 에러 처리 패턴 가이드 (예외 → 도메인 Failure → Provider/State → UI 관심사 분리) |
| `flutter-extract` | 재사용 가능한 위젯 추출 (private→shared 이동, 인라인 위젯 트리 분리, 중복 통합) |
| `flutter-feature` | 새 feature 모듈을 프로젝트 아키텍처에 맞는 디렉토리 구조 + 보일러플레이트로 스캐폴딩 |
| `flutter-hooks` | Flutter Hooks 패턴 가이드 + StatefulWidget → HookWidget 마이그레이션 + 커스텀 Hook 작성 |
| `flutter-kaizen` | Flutter 스킬을 학술 논문·공식 문서·커뮤니티 리서치 기반으로 점진적으로 개선하는 카이젠 스킬 |
| `flutter-l10n` | i18n 번역 문자열 추가/수정 + codegen (slang / easy_localization / intl ARB / flutter_localizations 자동 감지) |
| `flutter-preflight` | Pre-commit quality gate — fix → codegen → analyze → test 순서 실행 후 결과 요약 보고 |
| `flutter-provider` | Riverpod Notifier + State 클래스 생성 (@Riverpod codegen, copyWith, ref.mounted 체크, Result.when 분기 패턴 포함) |
| `flutter-responsive` | 반응형 레이아웃 적용/전환 (태블릿 대응, 2컬럼, 반응형 그리드, breakpoint 분기) |
| `flutter-run` | Flutter 빌드 프리미티브 실행 (codegen, analyze, fix, test, format) |
| `flutter-screen` | Screen/Page 위젯 생성 + 라우터 등록 (GoRouter / auto_route / Navigator 자동 감지) |
| `flutter-skeleton` | 로딩 스켈레톤 shimmer 구현 — 실제 레이아웃과 동일한 구조의 shimmer 블록 생성 |
| `flutter-test` | 대상 파일/클래스 분석하여 테스트 코드 자동 생성 (unit / widget / integration) |
| `flutter-transition` | GoRouter · auto_route · Navigator 기반 커스텀 페이지 전환 애니메이션 (fade-slide, scale-fade 등) |
| `flutter-widget` | 프로젝트 컨벤션에 맞는 위젯 생성 (디자인 시스템 감지, variant 패턴, size enum, base class 자동 선택) |

## 에이전트 목록 (1개)

| 에이전트 | 설명 |
|----------|------|
| `widget-inspector` | 프로젝트 코드에서 재사용 가능한 위젯 패턴 감지 + 리포팅 (읽기 전용, flutter-audit deep 모드 축으로 포함) |

## 레퍼런스

| 파일 | 용도 |
|------|------|
| `references/project-detection.md` | FVM 래퍼, 아키텍처 패턴, 의존성 등 프로젝트 환경 자동 감지 로직 |
| `references/flutter-ai-rules.md` | Flutter AI 코딩 규칙 (코드 생성 품질 가이드) |

## 요구사항

- FVM 설치 (Windows: `fvm.bat`)
- `.harness/project.yaml`의 `stack: flutter` 설정 (harness 플러그인 연동 시)
