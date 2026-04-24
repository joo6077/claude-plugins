---
feature: "kaizen-phase3-evaluator-kaizen"
created: "2026-04-24 11:35"
complexity: "medium"
conditions: 18
branch: "kaizen/2026-04-24"
phase: 3
---

# Sprint Contract — Phase 3: Evaluator Kaizen

Generated: 2026-04-24
Feature: kaizen-phase3-evaluator-kaizen
Scope (수정 허용): `harness/docs/guides/qa-evaluation-guide.md`, `harness/agents/qa-evaluator.md` (2 files only)
Branch: kaizen/2026-04-24

## Context

Phase 1 (skill/agent-design-guide v1.2.0) + Phase 2 (contract-design-guide v3 · contract-schema v3) 에서 승격된 원칙을 **평가자 레이어**에 전수한다. qa-evaluation-guide 와 qa-evaluator 에이전트가 Phase 1/2 의 Binary Decidability · Scope Range · `[미검증]` 마커 · Sibling Consistency · 3 단계 fallback · Rule-by-Rule Audit · Cross-Surface Parity 를 평가 프로토콜로 흡수한다.

Diagnosis 패턴 대응:
- l3_unreached (13회) — L3 샘플링 시 미검증 명시 의무 규칙 추가
- contract_misinterpret (7회) — Binary Decidability Pre-Check 평가자 프로토콜 반영
- perspective_gap (5회) — User-Value / Business-Intent 관점 체크리스트 추가

## Categories

### Cross-Surface Parity (CP)

- [ ] CP-01: qa-evaluation-guide.md 에 "Cross-Surface Parity Checklist" 섹션이 존재하고, skill-design-guide §11 + agent-design-guide §12 + contract-design-guide §원칙 전수성 과의 parity table 을 포함한다 [structural]
- [ ] CP-02: qa-evaluation-guide.md Parity Table 이 아래 4 개 parity item 을 모두 명시한다: (1) Binary Decidability, (2) Rule-by-Rule Audit, (3) Unverifiable / `[미검증]` 정책, (4) Sibling Consistency (측정: Grep 으로 각 용어 literal 매칭) [exact, enumerated]

### Binary Decidability Pre-Check (BD)

- [ ] BD-01: qa-evaluation-guide.md 에 "Binary Decidability Pre-Check" 섹션이 존재하고, 평가 시작 전 (Step 2 이전) 수행할 4 개 이상 체크 항목을 나열한다 [structural]
- [ ] BD-02: BD 섹션에 "이 조건의 FAIL 상태를 1 문장으로 기술 가능한가?" 테스트 항목이 명시된다 (측정: Grep "FAIL 상태" 또는 "1 문장") [exact]
- [ ] BD-03: BD 섹션에 "범위어(주요/모든/대부분/핵심) 발견 시 포함/제외 목록이 인라인 enumerated 되어 있는지 확인" 규칙이 명시된다 [exact]
- [ ] BD-04: qa-evaluator.md Process 에 "Step 1.5: Binary Decidability Pre-Check" 또는 동급 단계가 Step 1 과 Step 2 사이에 존재한다 (측정: Step 순서 Read) [structural]

### Rule-by-Rule Audit (RA)

- [ ] RA-01: qa-evaluation-guide.md 에 "Rule-by-Rule Audit" 섹션이 존재하고, 평가자가 판정 완료 전에 모든 계약 조건을 1 회 더 전수 점검하는 절차를 기술한다 [structural]
- [ ] RA-02: RA 섹션이 insights 마찰점 #1 (Proactive quality gaps) 을 참조하고, 부분 점검 → 전수 점검 전환 의무를 명시한다 [exact]

### `[미검증]` 마커 평가 프로토콜 (UV)

- [ ] UV-01: qa-evaluation-guide.md 에 "`[미검증]` 마커 평가 프로토콜" 섹션이 존재하고, 카운팅 로직 (1 건까지 PASS / 2 건 이상 자동 REJECT) 을 명시한다 [structural]
- [ ] UV-02: UV 섹션에 3 단계 fallback 수행 의무 (단계 2 → 단계 3 순서, 2 단계 미가용 시 3 단계 `[미검증]` 마커) 가 명시된다 [exact]
- [ ] UV-03: qa-evaluator.md 의 "기본 엄격도 규칙" 또는 Process Step 에 `[미검증]` 건수 집계 규칙이 "2 건 이상 자동 REJECT" 로 명시된다 (측정: Grep "2 건 이상" + "미검증") [exact]

### Sibling Enumerated Verification (SE)

- [ ] SE-01: qa-evaluation-guide.md 에 `[exact, enumerated]` 또는 `[structural, enumerated]` 조건에 대한 "Sibling Enumerated 전수 Grep" 절차가 존재한다. N 개 대상 전부 확인 + 하나라도 빠지면 FAIL + 누락 대상명 나열 [structural]
- [ ] SE-02: SE 섹션에 rust-kit H-01/H-03 REJECT 사례가 실패 예시로 인용된다 [exact]

### L3 Coverage Honesty (LC)

- [ ] LC-01: qa-evaluation-guide.md 에 "L3 샘플링 시 미검증 명시 의무" 규칙이 존재한다. 시간 제약으로 전수 L3 도달 불가면 샘플링 대상과 미검증 대상 목록을 명시적으로 분리 보고 [structural]
- [ ] LC-02: qa-evaluator.md 의 "얕은 검증 감지" 또는 동급 섹션에 "L3 샘플링 후 미검증 샘플 명시 없이 전체 PASS 금지" 규칙이 추가된다 [exact]

### Multi-Perspective Evaluation (MP)

- [ ] MP-01: qa-evaluation-guide.md "다관점 평가" 섹션에 기존 4 관점(기능/엣지/성능/보안) 외 "User-Value" 또는 "Business-Intent" 관점 1 개 이상이 추가된다 [exact]
- [ ] MP-02: MP 섹션이 perspective_gap 5 회 diagnosis 에 대응하여 "구현자 관점만으로 평가 금지" 규칙을 명시한다 [exact]

### Anti-patterns

- [ ] AP-01: qa-evaluator.md "Rationalization Table" 에 "미검증 2 건 누적 시 PASS 로 뭉뚱그림" 변명 행이 추가된다 [exact]
- [ ] AP-02: qa-evaluator.md Red Flags 에 "범위어 enumerated 없음에도 범위를 자체 해석" 변명 감지 항목이 추가된다 [exact]

## Anti-patterns
- [ ] 범위 밖 파일 수정 — scope 2 개 파일 외 변경 금지
- [ ] 장황한 reasoning — 증거(섹션명) 기반 간결 서술

## Diagnostics
- [ ] DG-01: 커밋이 `chore(kaizen-phase3):` prefix 를 사용한다
- [ ] DG-02: 커밋이 Phase 1/2 parity 를 명시적으로 언급한다 (Cross-Surface Parity, Binary Decidability 중 하나 이상)
