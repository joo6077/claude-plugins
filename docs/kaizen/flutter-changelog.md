---
title: Flutter Kaizen Changelog
version: 1.1.0
last_updated: 2026-04-11
---

# Flutter Kaizen Changelog

> flutter-kaizen에 의한 flutter-toolkit 변경 이력을 기록한다.

## [2026-04-11] - Phase 5 research-mode kaizen

### 변경 유형: patch (2026 Flutter 생태계 최신 패턴 반영)

### 변경 범위 (flutter-toolkit v0.5.0 → v0.5.1)

- **flutter-provider**: Riverpod 3.0 Notifier 재생성 라이프사이클 Gotcha 4건 추가 — Notifier 내부 Timer/Controller 금지, legacy provider 분류, `==` 기반 알림 필터링 (StreamProvider/StreamNotifier 영향), Freezed sealed Result → switch expression 병행 권장
- **flutter-hooks**: `context.mounted` async gap 체크 필수 Gotcha 추가 — showDialog / Navigator.push / `Future<T>` 반환 후 context 재사용 시 필수 검사, `ref.mounted` vs `context.mounted` 구분 설명, build() 100줄 이하 권장 노트 (금지 아님)
- **flutter-screen**: go_router `StatefulShellRoute.indexedStack` + `StatefulShellBranch` + `preload: true` 패턴 섹션 신규 — 2026 기준 go_router 공식 권장 패턴, 완전한 코드 예시 포함
- **flutter-error**: Freezed 3.0 sealed Result → switch expression 패턴 C' 코드 예시 추가 — `when`/`map` 제거 마이그레이션 대응
- **flutter-audit**: State Management 체크리스트 3건 확장 — Notifier 내부 Timer/StreamSubscription/TextEditingController 금지, Freezed sealed Result switch expression 병기, freezed changelog 링크
- **widget-inspector** 에이전트: Props 번들링 위반 감지 기준 5번 신규 — HAS_FREEZED + HAS_HOOKS 동시 조건, Named constructor variant 면제
- **references/project-detection.md**: Step 2b Makefile 기반 monorepo 감지 섹션 신규 — 타겟 목록 (app-run / app-preflight 포함), `$MAKE` 변수, HAS_MAKEFILE 스킬 매핑 테이블, fit-pal monorepo 출처
- **references/flutter-ai-rules.md**: 2026 생태계 노트 섹션 신규 6 서브섹션 — Riverpod 3.0 / Freezed 3.0 / go_router / Flutter 3.29 / flutter_hooks / Makefile, 전 항목 공식 출처 URL 명시

### QA 결과

Phase 5 sprint-contract 16 조건 모두 L3 PASS, iter 1 APPROVE. 독립 qa-evaluator 서브에이전트 평가로 검증. validate-plugin 7 OK, bare fence 0 건.

### 주요 리서치 소스

- [Riverpod 3.0 migration](https://riverpod.dev/docs/3.0_migration) — Notifier 재생성 라이프사이클 변경
- [Freezed changelog](https://pub.dev/packages/freezed/changelog) — 3.0 abstract/sealed 필수, when/map 제거
- [go_router StatefulShellRoute](https://pub.dev/documentation/go_router/latest/go_router/StatefulShellRoute-class.html) — preload 파라미터
- [Flutter 3.29 release notes](https://docs.flutter.dev/release/release-notes/release-notes-3.29.0) — context.mounted / breaking changes
- [flutter_hooks](https://pub.dev/packages/flutter_hooks) — 2026 권장 패턴
- Hub apps (iter 2 22/22) + fit-pal (iter 2 33/33) sprint-feedback 실무 검증

### Before/After 요약

| 영역 | Before | After |
| ---- | ------ | ----- |
| Riverpod Gotchas | 기본 `@Riverpod` codegen 안내 | 3.0 Notifier 라이프사이클 + 4건 경고 추가 |
| Hooks | context.mounted 언급 없음 | async gap 후 필수 체크 + ref.mounted 구분 |
| Screen Router | 기본 go_router 예시 | StatefulShellRoute + preload 패턴 섹션 |
| Widget Inspector | 4 감지 기준 | 5 감지 기준 (Props 번들링 포함) |
| project-detection | Makefile 감지 없음 | Step 2b Makefile monorepo 감지 |

---

---

## [0.5.0] - 2026-03-30

### 변경 유형: minor (skill-prompt, new-skill, eval)

### 연구 기반
- [Flutter 3.41 Breaking Changes](https://docs.flutter.dev/release/breaking-changes) — semantics 매처 변경, variable font weight
- [AToMIC 논문](https://arxiv.org/abs/2510.18861) — LLM 기반 Flutter 테스트 자동 생성
- [Flutter AI Rules](https://raw.githubusercontent.com/flutter/flutter/refs/heads/main/docs/rules/rules.md) — Arrange-Act-Assert, Fake/Stub 우선

### 변경 내역
- **flutter-audit Gotcha**: containsSemantics → isSemantics 테스트 매처 변경
- **flutter-widget Gotcha**: FontWeight가 variable font weight axis 제어
- **flutter-test 신규 생성**: unit/widget/integration 테스트 자동 생성 스킬 v0.1
- **evals.json**: flutter-test eval 케이스 추가 (id: 18)

### 버전 판단 근거
> 신규 스킬 초안 생성 + 스킬 프롬프트 변경 = minor

## [0.4.0] - 2026-03-30

### 변경 유형: minor (skill-prompt, reference, detection)

### 연구 기반
- [Flutter Official Architecture Guide](https://docs.flutter.dev/app-architecture/guide) — MVVM 패턴 공식 권장
- [Riverpod 3.0 Newsletter](https://codewithandrea.com/newsletter/september-2025/) — `.valueOrNull` → `.value`, offline persistence
- [Flutter 3.38 Release Notes](https://docs.flutter.dev/release/release-notes/release-notes-3.38.0) — WidgetState 마이그레이션, PredictiveBack 기본 전환
- [Flutter Official AI Rules](https://raw.githubusercontent.com/flutter/flutter/refs/heads/main/docs/rules/rules.md) — LLM 코드 생성 공식 가이드라인

### 변경 내역
- **flutter-toolkit/references/flutter-ai-rules.md**: 신규 생성 — Flutter 공식 AI rules 핵심 요약
  - Before: 공식 AI rules 참조 없음
  - After: 위젯 패턴, 상태관리, 아키텍처, Do's/Don'ts 요약 문서
  - 근거: [Flutter AI Rules](https://raw.githubusercontent.com/flutter/flutter/refs/heads/main/docs/rules/rules.md)

- **flutter-toolkit/skills/flutter-provider/SKILL.md**: Gotchas 2개 추가
  - Before: Riverpod 버전 변경 미언급
  - After: `.valueOrNull` → `.value` 마이그레이션, offline persistence experimental 경고
  - 근거: [Riverpod 3.0](https://codewithandrea.com/newsletter/september-2025/)

- **flutter-toolkit/skills/flutter-widget/SKILL.md**: Gotchas 2개 추가
  - Before: MaterialState → WidgetState 마이그레이션 미언급
  - After: WidgetState 마이그레이션 안내, private Widget 클래스 합성 패턴 강조
  - 근거: [Flutter 3.38](https://docs.flutter.dev/release/release-notes/release-notes-3.38.0), [AI Rules](https://raw.githubusercontent.com/flutter/flutter/refs/heads/main/docs/rules/rules.md)

- **flutter-toolkit/skills/flutter-screen/SKILL.md**: Gotcha 1개 추가
  - Before: PredictiveBack 기본 전환 미언급
  - After: Android에서 PredictiveBack 기본 전환과 커스텀 전환 충돌 가능성 경고
  - 근거: [Flutter Breaking Changes](https://docs.flutter.dev/release/breaking-changes)

- **flutter-toolkit/references/project-detection.md**: MVVM 패턴 추가
  - Before: clean, feature_first, flat 3가지만
  - After: mvvm 패턴 추가 (View ↔ ViewModel 1:1, Repository, Service)
  - 근거: [Flutter Architecture Guide](https://docs.flutter.dev/app-architecture/guide)

### 버전 판단 근거
> 스킬 프롬프트 변경(Gotchas) + 새 reference + detection 로직 변경 = minor
