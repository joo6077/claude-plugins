---
feature: "kaizen-phase8-infra-kit-kaizen"
created: "2026-04-24"
complexity: "high"
conditions: 20
branch: "kaizen/2026-04-24"
phase: 8
---

# Sprint Contract — Phase 8: Infra-kit Kaizen

Generated: 2026-04-24
Feature: Phase 1~7 신규 원칙을 infra-kit 4 스킬(infra-guide · infra-audit · infra-init · infra-test) + infra-reviewer 에이전트 + `.claude/skills/infra-kaizen` 에 전수하고, infra-kit 5 REJECT reasons(AR-03 · AR-04 · SK-07 · SK-08 · SK-13) 을 전수 해소 또는 회귀 방지 검증한다. Phase 8 리서치 테이블 6 건 중 최소 3 건(Kubernetes PSA · Terraform 1.10+ ephemeral · OpenTelemetry 3 signals) 의 URL 을 변경 근거로 인용한다. backend-kit Phase 7 해결책을 infra-kit 에 이식하는 것이 핵심.

Scope (수정 허용): `infra-kit/skills/*/SKILL.md`, `infra-kit/agents/infra-reviewer.md`, `infra-kit/references/*.md`, `infra-kit/README.md`, `infra-kit/evals/evals.json`, `.claude/skills/infra-kaizen/SKILL.md`, `.harness/sprint-contract.md` (본 파일), `.harness/history/` (Phase 7 아카이브).
범위 외 금지: harness/, flutter-toolkit/, design-kit/, backend-kit/, rust-kit/, react-kit/, reflect-kit/, planning-kit/, `docs/infra/` 리서치 문서 (infra-research 영역), 기타 최상위 파일.

Branch: kaizen/2026-04-24

## Research (R)

Phase 8 리서치 테이블 (phase-research-templates.md §Phase 8) 소스 6 건 중 최소 3 건의 URL 을 변경 근거로 인용한다:

1. [Kubernetes Pod Security Admission](https://kubernetes.io/docs/concepts/security/pod-security-admission/) — `baseline`/`restricted` 라벨 세팅
2. [Terraform 1.10+ ephemeral values](https://developer.hashicorp.com/terraform/language/ephemeral) — state 비저장 시크릿
3. [OpenTofu state encryption](https://opentofu.org/docs/v1.11/language/state/encryption/) — 1.7+ native encryption
4. [SLSA provenance](https://slsa.dev/provenance) — L3 목표 in-toto attestation
5. [Sigstore Cosign verifying attestation](https://docs.sigstore.dev/cosign/verifying/attestation/) — v3 번들 포맷
6. [OpenTelemetry spec status](https://opentelemetry.io/docs/specs/status/) — Logs stable 2025

Phase 1~7 누적 원칙은 `.claude/kaizen-input/MASTER.md` 및 Phase 4~7 커밋 메시지에서 발췌하여 매핑한다.

## Goals (G)

- G1: infra-kit 5 REJECT reasons(AR-03 · AR-04 · SK-07 · SK-08 · SK-13) 전수 해소 또는 회귀 방지 검증
- G2: Phase 1~7 누적 원칙 9 항목(skill §3.5/§3.6/§5.5/§8.7/§8.8/§11 · agent §3.5/§10/§12) 을 infra-kit 스킬·에이전트에 전수
- G3: Phase 8 리서치 6 건 중 최소 3 건의 URL 을 변경 근거로 인용
- G4: Sibling Group Parity — infra-test ↔ backend-test Step 0 스택 감지·기존 테스트 패턴 탐색·외부 실환경 강제 금지 3 항목 동기화
- G5: I-02 예외 목록을 infra-kaizen Gotcha 에 명시 (HTML/비-.md 산출물 — Dockerfile, .tf, .yml 예외 포함)

## Conditions (C · 20 건)

### G1 — REJECT reason 회귀 방지 (5)

- C1: `infra-kit/README.md` 가 존재하고 스킬 테이블에 4 스킬(infra-guide · infra-audit · infra-init · infra-test) + 에이전트 테이블 + 리서치 문서 요약 + "Phase 8 kaizen" 섹션을 포함한다 (AR-03 회귀 방지)
- C2: `infra-kit/evals/evals.json` 이 존재하고 4 스킬 전수 커버 + entry 수 >= 5 + placeholder(`TODO` · `FIXME` · `...`) 0 건이다 (AR-04 회귀 방지)
- C3: `infra-kit/skills/infra-audit/SKILL.md` Step 3 가 Rule-by-Rule 20-row 단위 표(#/카테고리/체크항목/판정/근거/출처) + CONDITIONAL APPROVE 규칙 + 자리표시자 0 건을 포함한다 (SK-07 해소)
- C4: `infra-kit/skills/infra-init/SKILL.md` Step 3 가 카테고리별 규격 출력 포맷(현재/권장/개선) + 최소 1 개 예시 + 자리표시자 0 건을 포함한다 (SK-08 해소)
- C5: `.claude/skills/infra-kaizen/SKILL.md` References 섹션이 존재하고 스킬 4 + 에이전트 1 + docs/infra SSOT + validation 도구 참조를 포함한다 (SK-13 회귀 방지)

### G2 — Phase 1~7 누적 원칙 전수 (9)

- C6: `infra-audit` Gotchas 에 Binary Decidability Pre-Check (agent-design-guide §3.5) 항목 존재
- C7: `infra-audit` Gotchas 에 Rule-by-Rule Audit 프로토콜 (skill-design-guide §3.6) 항목 존재
- C8: `infra-audit` Gotchas 에 미검증 마커 프로토콜 (evaluator v3 · agent-design-guide §10) 항목 존재 + Step 4 에 CONDITIONAL APPROVE 규칙 명시
- C9: `infra-guide` Gotchas 에 Enumerate-before-Act (skill-design-guide §5.5) 항목 존재
- C10: `infra-guide` Process 가 3-Step (탐색 → 진단 → 처방) 순서 고정 구조로 재정렬되어 있다
- C11: `infra-init` Gotchas 에 Enumerate-before-Act (skill-design-guide §5.5) 항목 존재
- C12: `infra-init` Process 가 3-Step (탐색 → 진단 → 처방) 순서 고정 구조로 재정렬되어 있다
- C13: `infra-reviewer.md` 에 Binary Decidability + Rule-by-Rule + 미검증 3항 + L3 Coverage Honesty 4 항목 전수 존재
- C14: `.claude/skills/infra-kaizen` Gotchas 에 Cross-Surface Parity Checklist (skill §11) Sibling Group 표 존재

### G3 — Phase 8 리서치 인용 (3)

- C15: infra-audit Step 3 Rule-by-Rule 표에 Kubernetes PSA URL(`https://kubernetes.io/docs/concepts/security/pod-security-admission/`) 인용 >= 1 row
- C16: infra-audit Step 3 Rule-by-Rule 표에 Terraform ephemeral URL(`https://developer.hashicorp.com/terraform/language/ephemeral`) 인용 >= 1 row
- C17: infra-audit Step 3 Rule-by-Rule 표에 OpenTelemetry spec status URL(`https://opentelemetry.io/docs/specs/status/`) 인용 >= 1 row

### G4 — Sibling Parity (2)

- C18: `infra-test` Gotchas 에 "Sibling Consistency (backend-test parity)" 항목 존재 (Step 0 스택 감지 + 기존 테스트 탐색 + 외부 실환경 금지 3 항목 언급)
- C19: `.claude/skills/infra-kaizen` Sibling Group 표에 `infra-test · backend-test` row 가 존재

### G5 — I-02 예외 목록 (1)

- C20: `.claude/skills/infra-kaizen` Gotchas 에 I-02 예외 목록 고정 명시 (`.harness/sprint-contract.md` · `.harness/sprint-feedback.md` · `.harness/.meta/kaizen-data-pool.md` · `.vscode/` · sync-docs 자동 갱신 README/HTML) + HTML/비-.md 산출물 예외(Dockerfile/.tf/.yml) 주석

## Verification Method

- L3 실행 검증: `scripts/run-evals.py infra-kit` exit 0 (evals.json 5 assertion 전수 PASS)
- L2 구조 검증: `scripts/validate-plugin.py infra-kit` 7 카테고리 결과 확인
- L1 정적 검증: Grep `'Binary Decidability'`, `'Rule-by-Rule'`, `'미검증'`, `'Enumerate-before-Act'`, `'L3 Coverage Honesty'` 키워드 각 스킬/에이전트별 존재 개수 카운트
- 커밋 메시지: `chore(kaizen-phase8): ...` 형식 + REJECT reason 매핑 5 건 전수 포함

## Anti-patterns (금지)

- 범위 외 파일 수정 (docs/infra/, 다른 플러그인)
- Gotcha 추가 시 Phase 1~7 용어 변경 (backend-kit 과 동일 표현 유지 — sibling drift 차단)
- Rule-by-Rule 표에 자리표시자(`...`) 또는 bare code fence 포함
- Phase 8 리서치 URL 인용 없이 "2026 최신" 같은 모호 표현 사용
