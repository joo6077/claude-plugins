# Sprint Feedback
Feature: flutter-toolkit 18개 스킬 + widget-inspector + references 2026 최신 Flutter/Riverpod/Freezed/go_router 트렌드 반영 카이젠 (Phase 5 research mode)
Evaluated: 2026-04-11 21:30
Verdict: APPROVE
Iteration: 1

## Results

### Provider — Riverpod 3.0 (4/4)

- [x] PR-01: Riverpod 3.0 Notifier 재생성 라이프사이클 경고 추가 — PASS (L3)
  - 근거: `flutter-toolkit/skills/flutter-provider/SKILL.md:19` — "Riverpod 3.0 Notifier 재생성 라이프사이클 — 2.x의 pseudo-singleton 동작이 폐기됐다. provider 가 rebuild 될 때마다 Notifier 도 재생성되므로 Timer/StreamSubscription/TextEditingController 등 생명주기 객체를 Notifier 의 필드로 직접 유지하면 리소스 누수가 발생한다. 해결: 해당 객체를 별도 provider 로 분리하고 ref.onDispose(() => controller.dispose()) 로 바인딩한다. (출처: https://riverpod.dev/docs/3.0_migration, https://riverpod.dev/docs/whats_new)"
- [x] PR-02: StateNotifierProvider / StateProvider / ChangeNotifierProvider legacy 분류 명시 — PASS (L3)
  - 근거: `flutter-toolkit/skills/flutter-provider/SKILL.md:20` — "Riverpod 3.0 legacy provider — StateNotifierProvider, StateProvider, ChangeNotifierProvider 는 3.0 에서 legacy 로 분류됐다. 신규 코드는 @riverpod / Notifier / AsyncNotifier 기반으로 작성한다. (출처: https://pub.dev/packages/flutter_riverpod/changelog)"
- [x] PR-03: == 기반 알림 필터링 + StreamProvider/StreamNotifier 영향 경고 추가 — PASS (L3)
  - 근거: `flutter-toolkit/skills/flutter-provider/SKILL.md:21` — "Riverpod 3.0 == 기반 알림 필터링 — 3.0 부터 모든 provider 가 상태 알림을 == 비교로 필터링한다. 특히 StreamProvider/StreamNotifier 에서 값 동등성이 있는 이벤트는 listener 에 전달되지 않는다. ... (출처: https://riverpod.dev/docs/whats_new)"
- [x] PR-04: Freezed sealed Result 기반이면 switch expression 사용 가이드 추가 — PASS (L3)
  - 근거: `flutter-toolkit/skills/flutter-provider/SKILL.md:17` — "프로젝트 Result 타입이 Freezed sealed class 기반이면 .when 대신 Dart pattern matching (switch expression) 사용 — Freezed 3.0부터 .when/.map 메서드가 제거되었다 (출처: https://pub.dev/packages/freezed/changelog)"

### Hooks — flutter_hooks + context.mounted (2/2)

- [x] HK-01: async gap 후 context.mounted 체크 필수 명시 추가 — PASS (L3)
  - 근거: `flutter-toolkit/skills/flutter-hooks/SKILL.md:21` — "async 메서드에서 showDialog / Navigator.push / Future<T> 결과 수신 후 같은 BuildContext 를 재사용하기 전에는 반드시 if (!context.mounted) return; — async gap 동안 위젯이 dispose 되면 context.pop, ScaffoldMessenger.of(context), Theme.of(context) 호출이 크래시로 이어진다. ref.mounted 는 Notifier 생명주기, context.mounted 는 Widget 생명주기이므로 둘은 별개다 (apps sprint-feedback iter 2, UI-06 / AR-01 FIX 패턴 기반)"
- [x] HK-02: build() 100줄 이하 권장 노트 추가 — PASS (L3)
  - 근거: `flutter-toolkit/skills/flutter-hooks/SKILL.md:25` — "build() 메서드는 100줄 이하 권장 — 그 이상이면 private Widget 클래스로 분리하여 composition 을 적용하라. 합성이 메서드 분리보다 성능·재사용성·테스트 가능성 모두 우수하다 (Flutter 공식 AI rules + apps CG-12 관습)" — 금지가 아닌 권장 표현으로 정확히 반영됨

### Screen / Router — go_router 2026 (2/2)

- [x] SC-01: StatefulShellRoute + StatefulShellBranch 분기 추가 — PASS (L3)
  - 근거: `flutter-toolkit/skills/flutter-screen/SKILL.md:188-221` — "#### StatefulShellRoute (바텀 네비 탭 + 탭별 독립 스택)" 섹션이 신규로 추가됨. StatefulShellRoute.indexedStack builder + branches: [StatefulShellBranch(routes: [GoRoute(...)])] 완전한 코드 예시 포함. "2026 기준 go_router 공식 권장 패턴" 명시
- [x] SC-02: StatefulShellBranch.preload 파라미터 언급 추가 — PASS (L3)
  - 근거: `flutter-toolkit/skills/flutter-screen/SKILL.md:208-209` — 코드 예시 내 `// preload: true → 탭 최초 진입 전에 미리 빌드 (go_router 최신 지원)`, `preload: true,` 명시

### Error Handling — Freezed 3.0 대응 (1/1)

- [x] ER-01: Result.when 패턴 예시에 "Freezed sealed 기반이면 switch expression" 주석 추가 — PASS (L3)
  - 근거: `flutter-toolkit/skills/flutter-error/SKILL.md:20` (Gotcha) — "프로젝트 Result 타입이 Freezed sealed class 기반이면 .when(success:, failure:) 가 아니라 Dart pattern matching (switch expression) 으로 분기하라 — Freezed 3.0 부터 .when/.map 메서드가 제거됐다. (출처: https://pub.dev/packages/freezed/changelog)"
  - `flutter-toolkit/skills/flutter-error/SKILL.md:209-220` — 패턴 C' 예시: `switch (result) { case Success(:final data): ... case Failure(:final failure): ... }` 코드 추가됨

### Audit — Riverpod 3.0 + Freezed 3.0 (2/2)

- [x] AU-01: State Management 체크리스트에 Notifier 내부 Timer/Controller 금지 항목 추가 — PASS (L3)
  - 근거: `flutter-toolkit/skills/flutter-audit/SKILL.md:101` — "Riverpod 3.0: Notifier 내부 필드로 Timer / StreamSubscription / TextEditingController 등 생명주기 객체를 직접 유지하지 않음 — 2.x pseudo-singleton 동작이 폐기되어 provider rebuild 마다 Notifier 가 재생성되므로 리소스 누수 발생. 이런 객체는 별도 provider 로 분리 후 ref.onDispose 로 바인딩"
- [x] AU-02: Result.when 체크 항목에 "Freezed sealed 기반이면 switch expression" 병기 — PASS (L3)
  - 근거: `flutter-toolkit/skills/flutter-audit/SKILL.md:103` — "프로젝트에 Result 타입이 있으면 Result.when(success:, failure:) 분기 사용. 단 Result 가 Freezed sealed class 기반이면 Freezed 3.0 에서 .when/.map 이 제거됐으므로 Dart pattern matching (switch expression) 사용 ([Freezed changelog](https://pub.dev/packages/freezed/changelog))"

### Widget Inspector (1/1)

- [x] WI-01: HookWidget + @freezed Props 번들링 준수 여부 감지 기준 추가 — PASS (L3)
  - 근거: `flutter-toolkit/agents/widget-inspector.md:85-99` — "### 5. Props 번들링 위반 (HAS_FREEZED + HAS_HOOKS)" 섹션 신규 추가. HAS_FREEZED = true 와 HAS_HOOKS = true 동시 감지 시 HookWidget/HookConsumerWidget 의 개별 파라미터 나열 패턴 탐지. 판단 기준(2개 초과 파라미터, Named constructor variant 면제), Step 2에 "Props 번들링 위반 (HAS_FREEZED + HAS_HOOKS 프로젝트에서만)" 추가됨

### References — Project Detection + flutter-ai-rules (3/3)

- [x] RD-01: project-detection.md 에 Makefile 기반 monorepo 감지 추가 — PASS (L3)
  - 근거: `flutter-toolkit/references/project-detection.md:32-46` — "### Step 2b. Makefile 기반 monorepo 감지" 신규 섹션. Makefile 존재 확인 후 app-run, app-run-staging, app-run-prod, app-run-profile, app-test, app-analyze, app-fix, app-clean, app-codegen, app-codegen-filter, app-build, app-preflight 타겟 중 하나 이상 있으면 HAS_MAKEFILE = true. $MAKE = make 변수 제공. fit-pal sprint-feedback iter 2 AC-6 출처 명시
- [x] RD-02: HAS_MAKEFILE 스킬 매핑 테이블 추가 + flutter-preflight/flutter-run 우선 사용 연동 — PASS (L3)
  - 근거: `flutter-toolkit/references/project-detection.md:48-57` — "HAS_MAKEFILE = true 일 때 주요 스킬 매핑" 테이블. flutter-run codegen / analyze / fix / test / flutter-preflight / flutter-build 모두 Makefile 우선 동작 명시. `flutter-toolkit/references/project-detection.md:136-147` — 감지 결과 요약 템플릿에 "Makefile: {true|false}" 필드 추가
- [x] RD-03: flutter-ai-rules.md 2026 생태계 노트 + 최종 확인 날짜 2026-04-11 갱신 — PASS (L3)
  - 근거: `flutter-toolkit/references/flutter-ai-rules.md:4` — "최종 확인: 2026-04-11" / `:70` — "최종 리서치: 2026-04-11 (WebSearch)" / `:68` — "## 2026 생태계 노트 (Riverpod 3.0 / Freezed 3.0 / go_router / Flutter 3.29+)" / Lines 74-113 — Riverpod 3.0, Freezed 3.0, go_router, Flutter 3.29, flutter_hooks, Makefile monorepo 각 서브섹션 모두 출처 URL 포함

### Anti-patterns (3/3)

- [x] AP-01: hardcoded version 없음 — PASS (L1)
- [x] AP-02: git push --force 없음 — PASS (L1)
- [x] AP-03: bare code fence 0건 — PASS (L3)
  - 검증: `python3` 스크립트로 개방 bare fence (`^\`\`\`\s*$` 이 opening 위치에 해당하는 것) 탐지 결과 0건. 나타나는 `\`\`\`` 라인은 모두 닫힘 fence(closing)임을 in_block 상태 추적으로 확인
- [x] AP-04: 모든 SKILL.md / agents/*.md frontmatter에 name 필드 존재 — PASS (L2)

### 스프린트 전용 규칙 (4/4)

- [x] Phase 1~4 파일(harness/**) 수정 금지 — PASS (L3)
  - 근거: `git show 515b66a --name-only` 결과에 harness/ 경로 파일 없음. eb88cc2 commit도 flutter-toolkit/agents/widget-inspector.md 1파일만 변경
- [x] flutter-toolkit plugin.json 버전 bump 없음 (Final Phase 대기) — PASS (L3)
  - 근거: `flutter-toolkit/.claude-plugin/plugin.json` version: "0.5.0" 유지. 515b66a 변경 파일 목록에 plugin.json 없음
- [x] 리서치 소스 URL 인용 — PASS (L3)
  - Riverpod: riverpod.dev/docs/3.0_migration, riverpod.dev/docs/whats_new, pub.dev/packages/riverpod/changelog, pub.dev/packages/flutter_riverpod/changelog
  - Freezed: pub.dev/packages/freezed/changelog
  - go_router: pub.dev/documentation/go_router/latest/go_router/StatefulShellRoute-class.html, pub.dev/packages/go_router/changelog
  - Flutter 3.29+: docs.flutter.dev/release/release-notes/release-notes-3.29.0, docs.flutter.dev/release/breaking-changes
  - flutter_hooks: pub.dev/packages/flutter_hooks, riverpod.dev/docs/concepts/about_hooks

### Regression 검증 (3/3)

- [x] VG-01: python3 scripts/validate-plugin.py 7 OK — PASS (L3)
  - 근거: 실행 결과 "Total: 7 plugins, 7 OK / Exit: 0" — flutter-toolkit 포함 전 킷 OK
- [x] VG-02: python3 scripts/sync-docs.py --check-only — 동기화 완료 — PASS (L3)
  - 근거: 실행 결과 "모든 README가 동기화 상태입니다."
- [x] VG-03: 변경된 markdown 파일에 bare code fence 0건 — PASS (L3)
  - 근거: 8개 파일 전수 검사, 개방 bare fence 없음

## Summary

- Total: 16/16 conditions passed
- Verdict: **APPROVE**

모든 13개 기능 조건 + 3개 검증 조건 전부 PASS. Phase 1~4 파일 미수정 확인, plugin.json 버전 bump 없음 확인, bare code fence 0건 확인.

리서치 출처 URL이 모든 핵심 Gotcha에 직접 인라인으로 포함되어 있어 계약 요구사항의 "공식 출처 URL 인용" 조건을 L3 수준으로 충족함.

Runtime inspection: MCP 서버 미설정 — 정적 검증만으로 판정. 정적 분석으로 16/16 PASS 달성.
