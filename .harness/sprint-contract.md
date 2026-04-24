---
feature: "kaizen-phase5-flutter-toolkit-kaizen"
created: "2026-04-24"
complexity: "medium-high"
conditions: 18
branch: "kaizen/2026-04-24"
phase: 5
---

# Sprint Contract — Phase 5: Flutter Toolkit Kaizen

Generated: 2026-04-24
Feature: Phase 1~4 신규 원칙(skill §3.5/§3.6/§5.5/§8.7/§8.8/§11 + agent §3.5/§12 + contract Scope Range + qa-eval Rule-by-Rule) 을 flutter-toolkit 18 스킬 + widget-inspector 에 전수하고, insights-report 의 Flutter 마찰점 3종(TextStyle 마이그레이션, Stack vs Column, Figma 토큰 enumerate) 을 반영한다. Riverpod 3.0.2 / Freezed 3 / go_router 17.2.2 최신 Context7 리서치 결과를 Gotchas 에 반영.

Scope (수정 허용): `flutter-toolkit/skills/*/SKILL.md`, `flutter-toolkit/agents/widget-inspector.md`, `flutter-toolkit/references/*.md` (범위 외 금지: harness/, design-kit/, backend-kit/, infra-kit/, rust-kit/, react-kit/, reflect-kit/, planning-kit/, 기타 최상위 파일)
Branch: kaizen/2026-04-24

## Research (R)
- [ ] R-01 [structural]: Context7 조회 결과(Riverpod 3.0.2 / Freezed 3 / go_router 17.2.2) 가 본 문서 Context 섹션 또는 변경된 SKILL.md Gotchas 에 버전과 함께 기록된다
- [ ] R-02 [structural]: insights-report Flutter 마찰점 3종(TextStyle 마이그레이션, Stack vs Column, Figma 토큰 enumerate) 이 최소 2개 스킬(flutter-widget 필수 + flutter-screen 또는 flutter-feature) 의 Gotchas 에 구체적 문구로 반영된다
- [ ] R-03 [structural]: Phase 1~4 신규 원칙 8건이 반영된 스킬을 매핑하는 표가 커밋 메시지 또는 본 문서 하단에 명시된다

## Skill Content (SK)
- [ ] SK-01 [exact]: flutter-widget, flutter-screen, flutter-feature 세 SKILL.md Gotchas 에 **동일한 "Enumerate-before-Act"** 표현(또는 한글 대응 "편집 전 전수 나열") 이 모두 존재한다 (Sibling Consistency — skill §8.8 대응)
- [ ] SK-02 [exact]: flutter-widget SKILL.md Gotchas 에 TextStyle / 레거시 타이포 토큰 **마이그레이션 누락 방지** (리팩터링 시 전수 확인) 원칙이 추가된다
- [ ] SK-03 [exact]: flutter-widget SKILL.md Gotchas 에 **Stack vs Column 선택 근거 enumerate** 원칙이 추가된다 (insights #2 대응)
- [ ] SK-04 [exact]: flutter-audit SKILL.md 에 **Rule-by-Rule Audit 완료 선언 전 전수 대조** 섹션 또는 Gotcha 가 추가된다 (skill §3.6 대응)
- [ ] SK-05 [exact]: flutter-audit SKILL.md 에 **Binary Decidability Pre-Check** 가 체크리스트 형태로 포함된다 (agent §3.5 대응 — 감사 시작 전 각 항목의 이진 판정 가능성 확인)
- [ ] SK-06 [exact]: flutter-hooks, flutter-error SKILL.md 에 **가이드형 스킬도 Process Step 순서 고정** (탐색→진단→처방) 명확성 선언이 있다
- [ ] SK-07 [exact]: flutter-kaizen SKILL.md 에 **Cross-Surface Parity Checklist** 섹션이 추가되어 flutter-toolkit 내 sibling group(widget/screen/feature, audit/preflight/build, l10n/responsive, transition/skeleton, error/hooks) 의 공통 원칙 누락 검사 절차를 정의한다 (skill §11 대응)

## Agent (AG)
- [ ] AG-01 [exact]: widget-inspector.md Gotchas 에 **Binary Decidability** 원칙 (후보/non-후보 판정 기준이 이진임을 명시) 이 추가된다
- [ ] AG-02 [exact]: widget-inspector.md Rules 에 **정적 Grep 만으로 후보 확정 금지 — Read 로 내용 확인 후 보고** 항목이 추가된다 (L3 Honesty · agent §10)

## Version Update (V)
- [ ] V-01 [exact]: flutter-toolkit/skills 내 최소 1개 파일 Gotchas 에 `Riverpod 3` / `Freezed 3` / `go_router 17` 중 하나 이상의 버전이 2026-04 Context7 리서치 기준으로 언급된다
- [ ] V-02 [exact]: flutter-hooks Gotchas 의 Freezed 관련 마이그레이션 설명이 "Freezed 3 부터 `.when`/`.map` 제거 → Dart switch expression" 로 명확히 서술된다 (중복되거나 이미 있으면 그대로 유지)

## Diagnostics (DG)
- [ ] DG-01 [goal]: 18 SKILL.md + widget-inspector.md 전 파일에서 bare opening fence (```만 있고 언어 힌트 없음) 0건 (python 스크립트 검증)
- [ ] DG-02 [goal]: 18 SKILL.md + widget-inspector.md 전 파일에서 TODO / FIXME placeholder 0건 (Grep 검증)
- [ ] DG-03 [structural]: flutter-widget, flutter-screen, flutter-feature Gotchas 에서 "Enumerate-before-Act" 문구 3건 이상 Grep 매칭 (Sibling parity 검증)

## Integrity (I)
- [ ] I-01 [goal]: 커밋 완료 후 `git status` 출력에 범위 외 파일(harness/, design-kit/, backend-kit/, infra-kit/, rust-kit/, react-kit/, reflect-kit/, planning-kit/, .claude/, docs/, scripts/) 0건
- [ ] I-02 [goal]: 커밋 SHA 1건, 메시지는 `chore(kaizen-phase5): ...` prefix
- [ ] I-03 [goal]: push 는 Phase 11 최종 통합 단계에서 수행하므로 본 Phase 에서는 로컬 커밋 1건 으로 충분

## 원칙 매핑 표

| 원칙 | 출처 가이드 | 반영 스킬 |
|------|-------------|-----------|
| Binary Decidability Pre-Check | skill §3.5, agent §3.5 | flutter-audit, widget-inspector |
| Rule-by-Rule Audit Before Completion | skill §3.6 | flutter-audit, flutter-preflight |
| Enumerate-before-Act | skill §5.5 | flutter-widget, flutter-screen, flutter-feature |
| Code Examples 품질 (fence 언어힌트, TODO 금지) | skill §8.7 | 전수 유지 검증 |
| Sibling-Skill Principle Consistency | skill §8.8 | flutter-widget/screen/feature 공통 Gotcha |
| Cross-Surface Parity Checklist | skill §11, agent §12 | flutter-kaizen |
| L3 Honesty / `[미검증]` 마커 | qa-eval / agent §10 | widget-inspector Rules |
| Scope Range / Verification Method | contract-design v3 | flutter-audit 감사 범위 |
