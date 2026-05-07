---
title: Flutter Kaizen Research Log
version: 1.1.0
last_updated: 2026-04-11
---

# Flutter Kaizen Research Log

> flutter-kaizen 스킬 실행 시 연구 결과를 누적 기록한다.
> 형식: `flutter-toolkit/skills/flutter-kaizen/templates/research-log-entry.md`

---

## 2026-04-11

**트리거:** kaizen-orchestrator Phase 5 (research-mode rerun)

### 조사한 소스

| # | 제목 | URL | 유형 | 신뢰도 | 결과 |
| - | ---- | --- | ---- | ------ | ---- |
| 1 | Riverpod 3.0 migration | <https://riverpod.dev/docs/3.0_migration> | 공식 | 높음 | 채택 |
| 2 | Riverpod whats new | <https://riverpod.dev/docs/whats_new> | 공식 | 높음 | 채택 |
| 3 | flutter_riverpod changelog | <https://pub.dev/packages/flutter_riverpod/changelog> | 공식 | 높음 | 채택 |
| 4 | Freezed 3.0 changelog | <https://pub.dev/packages/freezed/changelog> | 공식 | 높음 | 채택 (abstract/sealed 필수, when/map 제거) |
| 5 | go_router StatefulShellRoute | <https://pub.dev/documentation/go_router/latest/go_router/StatefulShellRoute-class.html> | 공식 | 높음 | 채택 |
| 6 | go_router changelog (preload) | <https://pub.dev/packages/go_router/changelog> | 공식 | 높음 | 채택 |
| 7 | Flutter 3.29 release notes | <https://docs.flutter.dev/release/release-notes/release-notes-3.29.0> | 공식 | 높음 | 채택 |
| 8 | Flutter breaking changes | <https://docs.flutter.dev/release/breaking-changes> | 공식 | 높음 | 채택 |
| 9 | flutter_hooks | <https://pub.dev/packages/flutter_hooks> | 공식 | 높음 | 채택 |
| 10 | Riverpod about_hooks | <https://riverpod.dev/docs/concepts/about_hooks> | 공식 | 높음 | 채택 (context.mounted vs ref.mounted) |
| 11 | fit-pal server monorepo (Makefile) | (internal) | ground truth | 높음 | 채택 |
| 12 | apps iter2 sprint-feedback (22/22) | (internal) | ground truth | 높음 | 채택 |
| 13 | fit-pal iter2 sprint-feedback (33/33) | (internal) | ground truth | 높음 | 채택 |

### 채택한 인사이트

- **Riverpod 3.0 Notifier 재생성 라이프사이클**: Notifier 내부에 `Timer`, `StreamSubscription`, `TextEditingController` 선언 금지 — provider 재생성 시 leak. `ref.onDispose(() => timer.cancel())` 로 분리 필요. 적용: flutter-provider, flutter-audit.
- **Freezed 3.0 sealed switch expression**: `when` / `map` 제거, sealed class 필수로 전환 → Dart 3 switch expression `switch (result) { Success(:final value) => ..., Failure(:final error) => ... }` 권장. 적용: flutter-error, flutter-audit.
- **go_router StatefulShellRoute.indexedStack + preload**: 2026 기준 탭 네비게이션 공식 권장 패턴. `preload: true` 로 사용자 첫 방문 전 빌드 완료 → 체감 성능 개선. 적용: flutter-screen.
- **context.mounted vs ref.mounted async gap**: Navigator.push / showDialog / Future<T> 반환 후 context 를 재사용할 때 `if (!context.mounted) return;` 필수. `ref.mounted` 는 Provider 수준, `context.mounted` 는 위젯 수준. 두 가드를 혼동하지 마라. 적용: flutter-hooks.
- **Makefile monorepo 감지**: fit-pal/apps 모노레포에서 `make app-run` / `make app-preflight` 타겟이 표준. flutter-toolkit 스킬이 이를 감지하면 `flutter` / `fvm flutter` 대신 `make` 경로를 제안한다. 적용: references/project-detection.md Step 2b.
- **Props 번들링 감지 (widget-inspector)**: HAS_FREEZED + HAS_HOOKS 동시 프로젝트에서 위젯 파라미터 6+ 개면 `@freezed Props` 클래스로 번들링 권장. Named constructor variant (ex. `Button.primary`) 는 면제. 적용: widget-inspector 감지 기준 5.

### 폐기 사유

없음 (Context7 quota 소진으로 일부 resolve 실패 → WebSearch fallback, 하지만 공식 출처는 모두 확보).

### PR

- <https://github.com/joo6077/claude-plugins/pull/6>

---

## 2026-03-30

**트리거:** manual (전체)

### 조사한 소스

| # | 제목 | URL | 유형 | 신뢰도 | 결과 |
| --- | ------ | ----- | ------ | -------- | ------ |
| 1 | Flutter Official Architecture Guide | <https://docs.flutter.dev/app-architecture/guide> | 공식 | 높음 | 채택 |
| 2 | Riverpod 3.0 (codewithandrea) | <https://codewithandrea.com/newsletter/september-2025/> | blog | 중간 | 채택 |
| 3 | Flutter 3.38 Release Notes | <https://docs.flutter.dev/release/release-notes/release-notes-3.38.0> | 공식 | 높음 | 채택 |
| 4 | Flutter 3.41 Breaking Changes | <https://docs.flutter.dev/release/breaking-changes> | 공식 | 높음 | 채택 |
| 5 | AToMIC: LLM Test Gen for Flutter | <https://arxiv.org/abs/2510.18861> | preprint | 중간 | 채택 |
| 6 | Flutter Official AI Rules (rules.md) | <https://raw.githubusercontent.com/flutter/flutter/refs/heads/main/docs/rules/rules.md> | 공식 | 높음 | 채택 |
| 7 | Flutter AI Development Guide | <https://docs.flutter.dev/ai/create-with-ai> | 공식 | 높음 | 채택 |
| 8 | skills.sh (flutter-animations) | <https://skills.sh> | skills.sh | 중간 | 폐기 |

### 채택한 인사이트

- **MVVM 공식 권장:** Flutter가 View ↔ ViewModel 1:1 + Repository + Service 패턴을 공식 아키텍처로 권장 — 적용 영역: detection
- **Riverpod 3.0 변경:** `.valueOrNull` → `.value`, offline persistence experimental — 적용 영역: skill (flutter-provider)
- **WidgetState 마이그레이션:** MaterialState → WidgetState (Flutter 3.38) — 적용 영역: skill (flutter-widget)
- **PredictiveBack 기본 전환:** Android에서 PredictiveBackPageTransitionBuilder가 기본값 — 적용 영역: skill (flutter-screen)
- **Flutter 공식 AI Rules:** LLM 코드 생성용 공식 가이드라인 존재, 합성 패턴/const 생성자 강조 — 적용 영역: reference 신규
- **AToMIC 논문:** LLM 기반 Flutter 수락 테스트 자동 생성, BMW 실증 — 적용 영역: 향후 flutter-test 스킬 참고

### 신규 스킬 갭 분석

| 제안 스킬 | 아키타입 | 근거 | 우선순위 | Issue |
| ----------- | --------- | ------ | --------- | ------- |
| `flutter-test` | 제품 검증 + 코드 스캐폴딩 | AToMIC 논문(BMW 실증), Flutter AI Rules(테스팅 패턴) | 높음 | #3 → **v0.5.0에서 초안 생성됨** |
| `flutter-migrate` | 런북 | Flutter 3.38/3.41 breaking changes, Riverpod 3.0 마이그레이션 | 중간 | #4 |

미충족 아키타입: 데이터 조회(#3), CI/CD(#7), 인프라 운영(#9) — Flutter 개발 특성상 해당 없거나 우선순위 낮음.

### 폐기 사유 (해당 시)

- **소스 8 (skills.sh):** Flutter 관련 스킬이 1개(flutter-animations)뿐이라 참고 가치 낮음

### PR

- <https://github.com/joo6077/claude-plugins/pull/2>
