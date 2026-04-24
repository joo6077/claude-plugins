---
feature: "kaizen-phase7-backend-kit-kaizen"
created: "2026-04-24"
complexity: "high"
conditions: 20
branch: "kaizen/2026-04-24"
phase: 7
---

# Sprint Contract — Phase 7: Backend-kit Kaizen

Generated: 2026-04-24
Feature: Phase 1~6 신규 원칙을 backend-kit 4 스킬(backend-guide · backend-audit · backend-system · backend-test) + backend-reviewer 에이전트 + `.claude/skills/backend-kaizen` 에 전수하고, backend-kit 5 REJECT reasons(AR-03 · AR-04 · SK-07 · SK-13 · ER-01) 을 전수 해소 또는 회귀 방지 검증한다. Phase 7 리서치 테이블 6 건 중 최소 3 건(OAuth 2.1 draft-15 · Transactional Outbox · Pact v4 + Testcontainers) 의 URL 을 변경 근거로 인용한다.

Scope (수정 허용): `backend-kit/skills/*/SKILL.md`, `backend-kit/agents/backend-reviewer.md`, `backend-kit/skills/*/references/*.md`, `backend-kit/README.md`, `backend-kit/evals/evals.json`, `.claude/skills/backend-kaizen/SKILL.md`, `scripts/run-evals.py` (ER-01 수정 한정), `.harness/sprint-contract.md` (본 파일).
범위 외 금지: harness/, flutter-toolkit/, design-kit/, infra-kit/, rust-kit/, react-kit/, reflect-kit/, planning-kit/, `docs/backend/` 리서치 문서 (backend-research 영역), 기타 최상위 파일.

Branch: kaizen/2026-04-24

## Research (R)

- [ ] R-01 [structural]: Phase 7 리서치 테이블 6 건 중 최소 3 건의 URL 이 변경된 SKILL.md/audit-criteria.md Gotchas 또는 본 문서 Context 섹션에 인용된다.
- [ ] R-02 [structural]: backend-kit 5 REJECT reasons (AR-03 · AR-04 · SK-07 · SK-13 · ER-01) 각각에 대해 반영 파일 + 변경 내용 + 회귀 방지 근거가 커밋 메시지에 매핑된다.

## REJECT Reason Resolution (AR)

- [ ] AR-03 [regression-guard]: `backend-kit/README.md` 존재 + 스킬 테이블에 backend-test 포함 + 에이전트 테이블 포함 + 리서치 문서 카테고리 요약 포함.
- [ ] AR-04 [regression-guard]: `backend-kit/evals/evals.json` 존재 + 4 스킬 전수 커버(backend-guide × 2 · backend-audit × 1 · backend-system × 1 · backend-test × 2) + 엔트리 수 >= 7 + placeholder 텍스트 0 건.

## Skill (SK)

- [ ] SK-07 [L2]: `backend-kit/skills/backend-audit/SKILL.md` Step 3 "리포트 생성" 이 10 카테고리 표(판정/파일:라인/근거/출처 열) 가 모두 채워진 실효 체크리스트 + CONDITIONAL APPROVE 규칙 + Rule-by-Rule Audit 앵커를 포함한다. 표 자리 표시자(`...`) 금지.
- [ ] SK-13 [L2]: `.claude/skills/backend-kaizen/SKILL.md` References 섹션이 존재하고 최소 6 항목(backend-guide/audit/system/test · reviewer · docs/backend · plugin-validation-guide · validate-plugin.py) 을 포함한다.
- [ ] SK-14 [L3]: `.claude/skills/backend-kaizen/SKILL.md` Gotchas 에 Cross-Surface Parity Checklist (§11) + I-02 예외 목록 (design-kaizen 과 동일 포맷) + Phase 1~6 신규 원칙 감사 Gotcha 가 존재한다.
- [ ] SK-15 [L2]: `backend-kit/skills/backend-audit/SKILL.md` Gotchas 에 Binary Decidability Pre-Check + Rule-by-Rule Audit 2 항목이 존재하고 각 항목이 REJECT/PASS 판정 근거를 명확히 지시한다.

## Principle Reflection (PR)

- [ ] PR-01 [L3]: skill §3.5 QA 계약 1:1 매칭 / §3.6 Rule-by-Rule Audit / §5.5 Enumerate-before-Act / §8.7 Code Examples 품질 / §8.8 Sibling Consistency / §11 Cross-Surface Parity 6 항목이 backend-kit 스킬/에이전트 중 최소 1곳씩에 모두 반영된다.
- [ ] PR-02 [L3]: agent §3.5 Binary Decidability / §10 Unverifiable / §12 L3 Coverage Honesty 3 항목이 backend-reviewer.md 에 모두 존재한다.
- [ ] PR-03 [L2]: 가이드형 3-Step (탐색→진단→처방) 원칙이 backend-guide Process 구조에 반영된다 (Phase 5 Flutter parity).

## Error (ER)

- [ ] ER-01 [L3]: `scripts/run-evals.py` 의 `load_evals` 에서 `JSONDecodeError` 시 `sys.exit(2)` 로 즉시 종료 (exit code 1 ≠ 2 구분 명확화). 변경 후 `python3 scripts/run-evals.py backend-kit` 정상 실행 + 의도적 파싱 오류 입력 시 exit 2 확인 [L3 검증].

## Integrity (II)

- [ ] II-01 [L3]: `scripts/validate-plugin.py backend-kit` 7 카테고리 전수 결과 0 건 regression. 변경 후 실행 결과 커밋 메시지에 수록.
- [ ] II-02 [L3]: `python3 scripts/run-evals.py backend-kit` PASS (전수 assertions OK).
- [ ] II-03 [structural]: 커밋 직전 `git status --short` 기준 modified/untracked 허용 예외 = `.harness/sprint-contract.md` (본 contract) · `.harness/sprint-feedback.md` (QA 산출물) · `.harness/.meta/kaizen-data-pool.md` (auto-regen) · `.vscode/` (untracked) · sync-docs 자동 갱신 README/HTML. 이 외 0 건.

## Anti-Pattern (AP)

- [ ] AP-01 [L2]: backend-kit 스킬 본문에 `(placeholder)` / `TODO:` / `TBD` / `FIXME` 문자열 0 건 (validate-plugin 의 `placeholders` 체크 통과).
- [ ] AP-02 [L2]: code fence 에 언어 힌트 누락(bare ```) 0 건 (validate-plugin code-fence 체크 통과).
- [ ] AP-03 [L3]: backend-reviewer.md 평가 카테고리 번호 `1 ~ 10` 이 `audit-criteria.md` 섹션 번호와 1:1 일치 (Architecture → API Design → Database → Auth → Error → Security → Caching → Event-Driven → Testing → Observability).

## Research Context (Phase 7 Sources)

필수 리서치 소스 (min 3 인용):

1. **IETF OAuth 2.1 Draft-15** (2026-03-02, expires 2026-09-03) — https://datatracker.ietf.org/doc/draft-ietf-oauth-v2-1/ · RFC 9700 BCP 를 통합, Implicit/ROPC 제거, PKCE 필수, 엄격 redirect URI 매칭.
2. **Transactional Outbox Pattern** — https://microservices.io/patterns/data/transactional-outbox.html · Dual-write 문제 해결, outbox 테이블 + message relay 컴포넌트, idempotency/ordering/dev accountability 함정.
3. **Pact v4 + Testcontainers** — https://prgrmmng.com/contract-testing-with-testcontainers-and-pact · Consumer-driven contract, Pact Broker coordinator, v4 는 gRPC/async messaging/GraphQL 지원 확장.
4. (optional) **Hexagonal vs Clean vs Onion 2026** — https://dev.to/dev_tips/hexagonal-vs-clean-vs-onion-which-one-actually-survives-your-app-in-2026-273f
5. (optional) **Azure Circuit Breaker + Rate Limiter 조합** — https://learn.microsoft.com/en-us/azure/architecture/patterns/circuit-breaker
6. (optional) **RFC 9457 problem+json** — https://www.rfc-editor.org/rfc/rfc9457.html

## Sibling Group Parity (Phase 6 Template)

| Sibling Group | 공통 원칙 검증 항목 |
|---------------|---------------------|
| backend-guide · backend-system | 가이드형 Process 3-Step (탐색→진단→처방) · Enumerate-before-Act · 트레이드오프 제시 |
| backend-audit · backend-reviewer (agent) | Binary Decidability Pre-Check · Rule-by-Rule Audit · 미검증 3항 · L3 Coverage Honesty 4 항목 동시 존재 |
| backend-guide · backend-audit · backend-system · backend-test | 10 카테고리 명명 규칙 일치 (Architecture · API Design · Database · Auth · Error · Security · Caching · Event-Driven · Testing · Observability) |
| backend-test · infra-test (Phase 8) | Step 0 스택 감지 독립 단계 + 기존 테스트 패턴 탐색 + 외부 실환경 강제 금지 |

## HTML 산출물 예외

backend-kit 는 HTML 산출물이 없으므로 design-kit AR-01 패턴의 예외 선언은 불필요. 단, `openapi.yaml`/`migrations`/스택별 파일(Dockerfile 등)은 `.md` 패턴과 구조적으로 다르므로 audit 시 별도 산출물 범주로 식별한다.
