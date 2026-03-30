---
title: Flutter Kaizen Research Log
version: 1.0.0
last_updated: 2026-03-30
---

# Flutter Kaizen Research Log

> flutter-kaizen 스킬 실행 시 연구 결과를 누적 기록한다.
> 형식: `flutter-toolkit/skills/flutter-kaizen/templates/research-log-entry.md`

---

## 2026-03-30

**트리거:** manual (전체)

### 조사한 소스

| # | 제목 | URL | 유형 | 신뢰도 | 결과 |
|---|------|-----|------|--------|------|
| 1 | Flutter Official Architecture Guide | https://docs.flutter.dev/app-architecture/guide | 공식 | 높음 | 채택 |
| 2 | Riverpod 3.0 (codewithandrea) | https://codewithandrea.com/newsletter/september-2025/ | blog | 중간 | 채택 |
| 3 | Flutter 3.38 Release Notes | https://docs.flutter.dev/release/release-notes/release-notes-3.38.0 | 공식 | 높음 | 채택 |
| 4 | Flutter 3.41 Breaking Changes | https://docs.flutter.dev/release/breaking-changes | 공식 | 높음 | 채택 |
| 5 | AToMIC: LLM Test Gen for Flutter | https://arxiv.org/abs/2510.18861 | preprint | 중간 | 채택 |
| 6 | Flutter Official AI Rules (rules.md) | https://raw.githubusercontent.com/flutter/flutter/refs/heads/main/docs/rules/rules.md | 공식 | 높음 | 채택 |
| 7 | Flutter AI Development Guide | https://docs.flutter.dev/ai/create-with-ai | 공식 | 높음 | 채택 |
| 8 | skills.sh (flutter-animations) | https://skills.sh | skills.sh | 중간 | 폐기 |

### 채택한 인사이트

- **MVVM 공식 권장:** Flutter가 View ↔ ViewModel 1:1 + Repository + Service 패턴을 공식 아키텍처로 권장 — 적용 영역: detection
- **Riverpod 3.0 변경:** `.valueOrNull` → `.value`, offline persistence experimental — 적용 영역: skill (flutter-provider)
- **WidgetState 마이그레이션:** MaterialState → WidgetState (Flutter 3.38) — 적용 영역: skill (flutter-widget)
- **PredictiveBack 기본 전환:** Android에서 PredictiveBackPageTransitionBuilder가 기본값 — 적용 영역: skill (flutter-screen)
- **Flutter 공식 AI Rules:** LLM 코드 생성용 공식 가이드라인 존재, 합성 패턴/const 생성자 강조 — 적용 영역: reference 신규
- **AToMIC 논문:** LLM 기반 Flutter 수락 테스트 자동 생성, BMW 실증 — 적용 영역: 향후 flutter-test 스킬 참고

### 신규 스킬 갭 분석

| 제안 스킬 | 아키타입 | 근거 | 우선순위 | Issue |
|-----------|---------|------|---------|-------|
| `flutter-test` | 제품 검증 + 코드 스캐폴딩 | AToMIC 논문(BMW 실증), Flutter AI Rules(테스팅 패턴) | 높음 | #3 → **v0.5.0에서 초안 생성됨** |
| `flutter-migrate` | 런북 | Flutter 3.38/3.41 breaking changes, Riverpod 3.0 마이그레이션 | 중간 | #4 |

미충족 아키타입: 데이터 조회(#3), CI/CD(#7), 인프라 운영(#9) — Flutter 개발 특성상 해당 없거나 우선순위 낮음.

### 폐기 사유 (해당 시)

- **소스 8 (skills.sh):** Flutter 관련 스킬이 1개(flutter-animations)뿐이라 참고 가치 낮음

### PR

- https://github.com/joo6077/claude-plugins/pull/2
