---
version: 1.0.0
last_updated: 2026-04-11
---

# Flutter Kit Research Log

> Flutter 관련 리서치 로그. `docs/kaizen/flutter-research-log.md` 와 동일 내용을 per-kit view 로 보관한다.
> kaizen-orchestrator 의 per-kit research-log 정책 (Step 12) 에 따라 생성됨.
> 상세 소스/인사이트는 `docs/kaizen/flutter-research-log.md` 를 참조.

---

## 2026-04-11

**트리거:** kaizen-orchestrator Phase 5 (research-mode rerun)

### 조사한 소스 요약

| # | 제목 | URL | 유형 | 결과 |
| - | ---- | --- | ---- | ---- |
| 1 | Riverpod 3.0 migration | <https://riverpod.dev/docs/3.0_migration> | 공식 | 채택 |
| 2 | Freezed 3.0 changelog | <https://pub.dev/packages/freezed/changelog> | 공식 | 채택 (abstract/sealed) |
| 3 | go_router StatefulShellRoute | <https://pub.dev/documentation/go_router/latest/go_router/StatefulShellRoute-class.html> | 공식 | 채택 |
| 4 | Flutter 3.29 release notes | <https://docs.flutter.dev/release/release-notes/release-notes-3.29.0> | 공식 | 채택 |
| 5 | flutter_hooks | <https://pub.dev/packages/flutter_hooks> | 공식 | 채택 |
| 6 | fit-pal / apps sprint-feedback | (internal) | ground truth | 채택 |

### 주요 인사이트 (요약)

- **Riverpod 3.0 Notifier 라이프사이클**: 재생성 시 leak 방지를 위해 Notifier 내부 Timer/Controller 금지, `ref.onDispose` 로 분리
- **Freezed 3.0 sealed + Dart 3 switch expression**: `when`/`map` 제거 마이그레이션 대응
- **go_router StatefulShellRoute + preload: true**: 탭 네비게이션 공식 권장 패턴
- **context.mounted vs ref.mounted**: async gap 후 context 재사용 시 필수 가드 구분
- **Makefile monorepo 감지**: fit-pal/apps 에서 make 기반 표준 타겟 감지 → project-detection Step 2b
- **Props 번들링 (widget-inspector)**: HAS_FREEZED + HAS_HOOKS 프로젝트에서 위젯 파라미터 6+ 개 → `@freezed Props` 권장

### 전체 기록

- `docs/kaizen/flutter-research-log.md` (마스터 로그)
- `docs/kaizen/flutter-changelog.md` (변경 이력)

### PR

- <https://github.com/joo6077/claude-plugins/pull/6>

---

## 2026-04-12

**트리거:** 5성 Gap 개선 — docs/flutter 리서치 확충 (695줄 → 1500줄+)

### 확충 대상 및 출처

| 파일 | 추가 내용 | 주요 출처 |
| ---- | --------- | --------- |
| ui/animation.md | Staggered animation, AnimatedSwitcher, RepaintBoundary, 성능 프로파일링 | https://docs.flutter.dev/ui/animations/staggered-animations |
| ui/responsive.md | Breakpoint utility, Sliver 반응형, Foldable 지원, 테스트 전략 | https://m3.material.io/foundations/layout/applying-layout/window-size-classes |
| ui/theming.md | ThemeExtension 코드 예시, Dynamic Color, AnimatedTheme, 테스트 | https://api.flutter.dev/flutter/material/ThemeExtension-class.html |
| ui/widget-composition.md | Child hoisting, Builder 패턴, 분해 기준, 테스트 | https://docs.flutter.dev/perf/best-practices |
| state/state-management.md | AsyncNotifier 구조, ref.invalidate vs refresh, Provider 선택, 테스트 | https://docs-v2.riverpod.dev/docs/providers/notifier_provider |
| state/hooks.md | 커스텀 훅, useEffect keys 규칙, Props 번들링, 테스트 | https://pub.dev/documentation/flutter_hooks/latest/flutter_hooks/Hook-class.html |
| state/async-patterns.md | FutureBuilder 올바른 사용, Isolate.run, 취소 패턴, Debounce | https://dart.dev/language/isolates |
| quality/performance.md | DevTools, Impeller, 최적화 체크리스트, 메모리 관리 | https://docs.flutter.dev/perf/impeller |
| quality/testing.md | Widget test 기본 구조, Golden test, 테스트 피라미드, Fake vs Mock | https://docs.flutter.dev/cookbook/testing/widget/tap-drag |
| architecture/clean-architecture.md | 디렉토리 구조, UseCase 생략 기준, DI 패턴, 데이터 흐름 | https://docs.flutter.dev/app-architecture/guide |
| architecture/routing.md | GoRouter 설정, ShellRoute, 딥링크+인증, transition | https://pub.dev/documentation/go_router/latest/ |
| architecture/api-layer.md | Retrofit DataSource, DTO 변환, Interceptor, Pagination, 테스트 | https://pub.dev/packages/retrofit |

### 방법론

- 모든 추가 내용에 flutter.dev, pub.dev, dart.dev, m3.material.io 등 공식 출처 URL 포함
- 기존 내용 미삭제 (append-only)
- 코드 예시는 실전 프로젝트 패턴 기반, 최소한의 context로 이해 가능하도록 작성
- 각 문서에 "실전 패턴" + "테스트 전략" + 추가 Gotchas 섹션 보강

### 향후 리서치 백로그

| 우선순위 | 주제 | 예상 출처 | 대상 문서 |
| -------- | ---- | --------- | --------- |
| 높음 | Flutter 4.0 breaking changes | flutter.dev/release | 전체 |
| 높음 | Riverpod 4.0 (예정) code generation 변경 | riverpod.dev | state/state-management.md |
| 중간 | Impeller Android 안정화 상태 | flutter.dev/perf/impeller | quality/performance.md |
| 중간 | Dart macros (stable 이후) | dart.dev/language | architecture/clean-architecture.md |
| 중간 | Material 3 Expressive Theme | m3.material.io | ui/theming.md |
| 낮음 | Flutter web WASM compilation (stable) | docs.flutter.dev/platform-integration/web/wasm | state/async-patterns.md |
| 낮음 | DevTools extensions API | docs.flutter.dev/tools/devtools | quality/performance.md |

### 품질 기준

- 각 문서가 5 원칙 + 2 수치 + 3 안티패턴 + 2 Gotchas 최소 유지
- 코드 예시는 실행 가능한 snippet (import 생략하되 타입은 명확히)
- deprecated API 사용 시 `[deprecated: YYYY-MM]` 태그 필수
- 출처 URL은 분기별로 접근 가능성 확인 (404 발견 시 즉시 대체)

### 관련 카이젠 사이클

- 이번 확충은 flutter-kaizen Phase 5 이후 추가 보강으로, kaizen-orchestrator의 per-kit research-log 정책을 따름
- 다음 `/flutter-kaizen` 실행 시 이 리서치를 기반으로 flutter-toolkit 스킬 Gotchas/Process 개선 예정
