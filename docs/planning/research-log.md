---
title: Planning Kaizen Research Log
version: 1.0.0
last_updated: 2026-06-05
---

# Planning Kaizen Research Log

## [2026-07-27] - Phase 11 kaizen

신호 농도 LOW (외부 프로젝트 planning-kit 사용 흔적 0건, reflect-digest 760 엔트리 중 planning 결함 0건).
research-only 모드로 조회했고 **외부 방법론 drift 는 발견되지 않았다** — 변경은 전부 내부 정합화다.

### 조회 소스 (WebFetch 6건 · Context7 는 OAuth 미인증이라 미사용)

- [Cucumber Gherkin Reference](https://cucumber.io/docs/gherkin/reference) — "An outcome should be on an
  observable output ... not a behaviour deeply buried inside the system", "we recommend 3-5 steps per example",
  `Then` 은 actual 결과와 expected 결과를 비교하는 단계
- [Agile Alliance — INVEST](https://agilealliance.org/glossary/invest/) — Testable 은
  "in principle, even if there isn't a test for it yet" = 원리적 반증가능성 기준
- [Basecamp Shape Up §6](https://basecamp.com/shapeup/1.5-chapter-06) — pitch 는 구두 아이디어가 아니라
  "posting the write-up ... somewhere that stakeholders can read it on their own time" 인 기록 아티팩트
- [GitHub Docs — Projects Best Practices](https://docs.github.com/en/issues/planning-and-tracking-with-projects/learning-about-projects/best-practices-for-projects)
  — sub-issue, issue dependencies(blocked by/blocking), "Have a single source of truth", 자동화는 GraphQL API
- [Marty Cagan — Four Big Risks](https://www.svpg.com/four-big-risks/) — 4 risks 정의 유지, "Tackle the big risks early"
- [Teresa Torres — Opportunity Solution Tree](https://www.producttalk.org/glossary-discovery-opportunity-solution-tree/)
  — 4 노드(Desired Outcome / Opportunity / Solution / Assumption Tests), "makes implicit assumptions explicit"

### 확인 결과 — 무변경 판정

- plan-sync-github Gotcha 4(Projects v2 = GraphQL) · Gotcha 10(sub-issue + dependency) · Gotcha 9(single
  source of truth) 는 현행 GitHub 공식 문서와 일치. 변경 없음
- plan-audit 카테고리 6(Gherkin 3-5 step, 관찰 가능한 결과) · 카테고리 10(4-risks) 도 출처와 일치
- plan-prd 는 Shape Up 의 "write-up 아티팩트" 요구와 기준선 있는 success metric 체크리스트로 이미
  falsifiable + committed-artifact 를 충족. 변경 없음

### 변경 (내부 정합화만)

- `planning-reviewer.md`: Canonical Unverified-Evidence Protocol 5 조항을 정본에서 **문구 변형 없이** 복제
  (`qa-evaluation-guide.md` §Canonical Unverified-Evidence Protocol). Phase 3 v4.0 이 지목한
  "planning-reviewer 만 미검증 0 건 요구" drift 해소 → 임계 2 로 통일. verdict 를 FAIL 축 / `[미검증]` 축
  2 축 합성으로 분리. `N/A`(선택 카테고리 비적용) 가 `[미검증]` 동의어가 아님을 정본 밖 주석으로 명시
- `plan-audit/SKILL.md`: Step 5 verdict 규칙을 reviewer 와 Sibling Consistent 하게 갱신
  (`NEEDS_VERIFICATION` 추가), 미검증 건별 집계 형식 도입, 공허한 산출물 PASS 금지 Gotcha 추가
  (skill-design-guide §3.7 조항 4 · canonical 조항 2 의 "증거 무효" 분기)
- `plan-stories/SKILL.md`: INVEST T 행을 반증가능성 판정으로 강화, 계약 경계를 넘는 스토리에
  양면(producer/consumer) 열거 요구 + 저장 템플릿 `## Surfaces` 섹션 (E2 아티팩트, §5.5 Counterpart
  Enumeration · insights Friction #4 의 기획 레벨 대응)
- `.claude/skills/planning-kaizen/SKILL.md`: validate-plugin "7 카테고리" → 8 (V1~V8) 정정,
  임계값 SSOT 재정의 금지 규칙 추가

### 명시적 비범위

- 스테일 핸드오프 git 재검증(insights Friction #5) 은 insights-report 가 Phase 4 Harness 로 배정 — 중복 승격 회피
- Counterpart Enumeration 의 평가자 측 대응 절은 만들지 않음 (skill-design-guide §11 parity item 12 —
  "생성 측 전용, 평가자는 계약 조건으로 수용")
- plan-data-model PlantUML 옵션 / Projects REST→GraphQL 마이그레이션 가이드: 이전 사이클 백로그이나
  이번 신호 농도 LOW + 사용 흔적 0 → 착수 근거 없음, 백로그 유지

## [2026-06-05] — Phase 11 kaizen

생성형 8스킬에 scope-discipline 가드 추가(요청 안 한 섹션/스토리/엔티티 임의 추가 금지). plan-sync-github 는 기존 보유로 SKIP.

출처: basecamp.com/shapeup Ch.6, agilealliance.org/glossary/invest, skill-design-guide §5.5.


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
