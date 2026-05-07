---
title: Planning Kaizen Research Log
version: 1.0.0
last_updated: 2026-05-07
---

# Planning Kaizen Research Log

planning-kit 카이젠 사이클별 리서치 인용 + Phase 별 변경 근거 기록.

## [2026-05-07] — Phase 11 kaizen (Phase 1 v1.3.0 신규 원칙 흡수)

### 데이터 소스

- 데이터 풀 §0 `/insights` 30 일 분석 (3 friction · 3 pattern · 3 feature)
- `harness/references/cross-kit-principles.md` v1 매트릭스의 planning-kit 열

### 외부 리서치 인용 (이전 카이젠 사이클 보존)

- Teresa Torres — Continuous Discovery Habits (Opportunity Solution Tree)
- Marty Cagan — INSPIRED (4 risks: value/usability/feasibility/business viability)
- Basecamp Shape Up — appetite, betting table, hill chart, scope hammering
- Alan Klement — Job Stories (JTBD)
- Strategyn ODI — Outcome-Driven Innovation
- Agile Alliance INVEST — Independent/Negotiable/Valuable/Estimable/Small/Testable
- Cucumber Gherkin — Given-When-Then 시나리오
- HBR Pre-mortem — Gary Klein
- Mermaid ER syntax v10
- GitHub Projects v2 REST API
- Lean Stack — Riskiest Assumption Test (RAT)

### Phase 11 변경 (이번 사이클)

- planning-kit/README.md 에 cross-kit-principles 매트릭스 cross-reference 섹션 신규
- plugin.json v0.3.0 → v0.3.1 patch bump
- planning-reviewer self-check ↔ Self-Evaluator Audit 매핑
- plan-audit + plan-discover enumerate 단계 ↔ Pre-Edit Batch Audit 매핑
- plan-prd / plan-stories sprint handoff 시점 ↔ Session Lifecycle (skill-design-guide §2 10번째 유형) 매핑

### 다음 사이클 백로그

- planning-kit 의 plan-data-model 스킬에 Mermaid ER 외 PlantUML 옵션 추가 검토
- plan-sync-github 의 GitHub Projects v2 GraphQL API 도입 (REST → GraphQL 마이그레이션 가이드)
- /insights friction Point 가 기획 단계에서 발견될 때 plan-discover 가 자동 흡수하는 메커니즘
