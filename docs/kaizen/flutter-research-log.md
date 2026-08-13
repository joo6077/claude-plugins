---
title: Flutter Kaizen Research Log
version: 1.3.0
last_updated: 2026-08-13
---

# Flutter Kaizen Research Log

## [2026-08-13] — Phase 5

**외부 조회 0 회.** 이 Phase 의 유일한 외부 근거는 `.harness/.meta/evidence/phase5.md` 다.
오케스트레이터가 codex 를 foreground 로 호출해 근거를 파일로 고정한 뒤 Phase 서브에이전트가 그
파일만 읽는 방식이었다 (백그라운드 실행 중 네트워크 조회 금지). 아래 URL 은 전부 그 파일이 인용한
것이고, evidence 에 없는 출처는 쓰지 않았다.

| # | URL | 확인한 사실 |
|---|-----|------------|
| 1 | <https://pub.dev/packages/freezed/changelog> | 최신 stable **3.2.5**. `.when`/`.map` 제거는 **3.0** 의 breaking 이고 **3.1.0 에서 재추가** — "3 부터 제거" 를 절대 규칙으로 쓰면 낡은 조항 |
| 2 | <https://docs.flutter.dev/release/release-notes> | stable 목록 최상단 **3.47.0** |
| 3 | <https://flutter.dev/blog/whats-new-in-flutter-3-47> | Android 의존성 매트릭스 — Java 17 · KGP 2.4.0 · AGP 9.1.0 · Gradle 9.3.1 |
| 4 | <https://docs.flutter.dev/perf/impeller> | iOS 는 Skia 전환 불가 · Android API 29+ 기본 · Web 은 Skia · **macOS/Linux/Windows 는 3.47 부터 Impeller 기본** |
| 5 | <https://docs.flutter.dev/perf/ui-performance> | 성능 디버깅은 물리 기기 + profile mode. debug/simulator 는 release 동작을 대표하지 않음 |
| 6 | <https://docs.flutter.dev/testing/build-modes> | profile mode 는 emulator/simulator 에서 **비활성** |
| 7 | <https://riverpod.dev/docs/concepts2/refs> | `watch` 는 선언형 구독 / `listen` 은 side effect / `invalidate` 는 다음 read 때 재평가 / `refresh` 는 invalidate + read sugar |
| 8 | <https://riverpod.dev/docs/concepts2/auto_dispose> | listener 0 이 된 뒤 **한 프레임 후** dispose · recompute 시 autoDispose 무관하게 state 파괴 · family 는 autoDispose 권장 |
| 9 | <https://riverpod.dev/docs/how_to/testing> | unit 은 `ProviderContainer.test()`(공유 금지, autoDispose 는 `listen` 으로 붙잡기) · widget 은 `ProviderScope` 루트 + `tester.container()` |
| 10 | <https://pub.dev/packages/flutter_riverpod/changelog> | 3.4.x 에서 scoped override 환경의 `invalidate`/`refresh` 미탐지 버그 수정 + `Ref.onManualInvalidation()` 추가 → 버전 가드 필요 |
| 11 | <https://github.com/flutter/agent-plugins> | 공식 Agent Plugins 는 "skills/rules 로 반복 워크플로우를 주입" 을 agent mistake 감축의 1 차 기법으로 제시 — 즉 기존 컴포넌트 재사용은 API 문제가 아니라 강제 절차 문제 |

### 내부 데이터 소스

- `.harness/.meta/kaizen-data-pool.md` §1 — `RE-02`(기본 `Divider` 사용, `IFDivider` 미재사용) ·
  `LG-02`(팔레트 변경 시 provider invalidate 누락) · `LG-01`(16종 매핑 중 2종만 검증)
- `.claude/kaizen-input/insights-report.md` — 신규 델타 **D5**(18 일 누수된 시뮬레이터 render host 가
  swap 을 포화시킨 것을 앱 최적화 전에 규명한 성공 사례) · **D3**(사용자 관측 vs 자기 증거 충돌)

### 채택한 인사이트

- 1~4 는 **사실 정정**으로 소비했다. 우리 문서가 틀렸던 쪽이라 새 조항을 얹은 게 아니라 기존 서술을
  교체했다 (Freezed 10 줄 → 0, Flutter stable 3 줄, Impeller 5 줄).
- 11 + `RE-02` → G1 Primitive Substitution Gate. 프레임워크 API 가 아니라 절차 문제라는 진단을 받아
  **E1 → E2 승급**(대체 후보 표 아티팩트)으로 처리했고, 정의는 references SSOT 1 곳에만 뒀다.
- 7 · 8 · 10 + `LG-02` → G2 invalidate 경계. `onManualInvalidation` 은 3.4.x 하한 가드를 달았다 —
  evidence 의 열린 질문("Riverpod 최소 버전이 3.4.x 이상으로 고정되어 있는가")이 미해결이기 때문이다.
- 9 + `LG-01` → G3 위젯 테스트 하네스 + 매핑 전수 coverage 조항.
- 5 · 6 · 4 + D5 → G4 Environment Exclusion Checklist 8 항, "simulator/emulator/debug 단독 결과는
  `[미검증]`" 판정 규칙.

### 넣지 않은 것 (evidence §2 "넣지 말 것" + §4 열린 질문)

- **"모든 기본 위젯 금지"** — layout primitive 까지 막으면 게이트가 우회된다. 면제 목록을 명시했다.
- **"모든 mutation 후 전체 family invalidate"** — stale 은 줄지만 네트워크 재요청과 UX 흔들림이 커진다.
- **"widget test 에서 `ProviderContainer` 단독 사용"** — 화면 렌더링 검증에는 `ProviderScope` 루트가 필요하다.
- **"iOS simulator jank = 앱 버그"** — 공식 문서 기준 대표성이 없다.
- **`IF*` allowlist 하드코딩** — evidence 열린 질문 1 번(fit-pal DS 네이밍이 `IF*` 로 안정적인가)이
  미확인이고, 특정 프로젝트 네이밍을 스택 무관 게이트에 박으면 다른 프로젝트에서 노이즈가 된다.
  게이트는 대체물을 "프로젝트 구분선/버튼 컴포넌트" 처럼 일반명으로만 적었다.

### 산출물

kit 레벨 리서치 로그(`docs/flutter/research-log.md`)에도 같은 근거를 기록했고, 그쪽에는 과거
서술의 인라인 정정 주석까지 달았다 — 과거 기록을 지우지 않고 정정만 덧붙이는 방식이다.

## [2026-07-27] — Phase 5

Context7 OAuth 미인증으로 전부 WebFetch 직접 조회. 조회 결과 기준으로만 서술(학습 데이터 미사용):
docs.flutter.dev release-notes (stable **3.44.7**, 페이지 갱신 2026-07-10) ·
pub.dev flutter_riverpod **3.4.1** · go_router **17.3.0** · flutter_hooks **0.21.3+1** ·
api.flutter.dev matchesGoldenFile · pub.dev alchemist **0.14.0**(유지보수 중) ·
golden_toolkit(**discontinued**, 3년 전).

골든 테스트 선택지 조사 결과 golden_toolkit 은 discontinued 이고 alchemist 가 현행 유지보수
대상이라, 시각 증거 규약은 특정 패키지에 종속시키지 않고 감지 ladder(golden → integration_test →
설정의 mcpServers → none)로 설계했다. E3(훅)을 선택하지 않은 이유는 시각 채널 유무가 프로젝트마다
달라 §3.7 의 E3 정의(LLM 미호출 순수 함수)를 만족시킬 수 없기 때문이다.

## [2026-06-05] — Phase 5

insights 2026-06-04 Friction #3(과잉설계)의 Flutter 도메인 발현 대응. flutter-feature 는 clean arch 풀스택을 까는 스킬이라 과잉설계 취약 → 최소 구현 우선 Gotcha.


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
