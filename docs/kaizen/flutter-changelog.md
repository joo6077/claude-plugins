---
title: Flutter Kaizen Changelog
version: 1.0.0
last_updated: 2026-03-30
---

# Flutter Kaizen Changelog

> flutter-kaizen에 의한 flutter-toolkit 변경 이력을 기록한다.

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
