---
name: backend-kaizen
description: >
  backend-kit 스킬 품질을 docs/backend/ 리서치 문서 기준으로 주기적으로 개선한다.
  이 레포 개발용 스킬이며, backend-kit 플러그인에 포함되지 않는다.
  harness-kaizen, flutter-kaizen, design-kaizen과 동일한 패턴.
  "/backend-kaizen", "백엔드 카이젠", "backend-kit 개선" 같은 요청 시 트리거.
  단순 버그 수정이나 기능 구현 요청에는 트리거하지 않는다.
argument-hint: ""
user-invocable: true
---

# Gotchas

1. **추측성 Gotchas 추가 금지** — 실제 실패 근거 없이 "이럴 수 있다"는 Gotchas를 추가하지 마라.
2. **리서치 문서 기반만** — docs/backend/ 문서에 없는 원칙을 스킬에 추가하지 마라. 먼저 backend-research로 문서를 갱신하라.
3. **스킬 범위 변경 금지** — 스킬의 description(트리거 조건)을 변경하려면 사용자 승인 필수.
4. **한 번에 전체 스킬 수정 금지** — backend-kit 스킬 4개(guide · audit · system · test) + 에이전트를 동시에 대량 수정하면 품질이 떨어진다. 1~2개씩 개선하라.
5. **validate-plugin.py 실행 없이 완료 선언 금지** — 카이젠 세션 종료 시 반드시 `scripts/validate-plugin.py backend-kit`을 실행하여 7 카테고리 상태를 확인하라. 회귀가 발생하면 즉시 수정한다.
6. **Cross-Surface Parity Checklist (skill-design-guide §11 · agent-design-guide §12 대응)** — 스킬 개선 시 아래 sibling group 간 공통 원칙(Gotcha · Process Step · 자동 로드 로직) 의 누락을 **1:1 Grep 대조** 로 확인한다. 누락된 sibling 이 있으면 즉시 동일 표현을 복제하여 비대칭 지식 상태를 제거한다 (2026-04 backend-kit Phase 7 에서 Phase 5 디자인 반영 때 반복 드리프트 차단).

   | Sibling Group | 공통 원칙 검증 항목 |
   |---------------|---------------------|
   | backend-guide · backend-system | **3-Step Process (탐색→진단→처방)** + Enumerate-before-Act + 트레이드오프 제시 |
   | backend-audit · backend-reviewer (agent) | **Binary Decidability Pre-Check · Rule-by-Rule Audit · 미검증 3항 · L3 Coverage Honesty** 4 항목 동시 존재 |
   | backend-guide · backend-audit · backend-system · backend-test | **10 카테고리 명명 규칙** 일치 (Architecture · API Design · Database · Auth · Error · Security · Caching · Event-Driven · Testing · Observability) |
   | backend-test · infra-test (Phase 8) | **Step 0 스택 감지 독립 단계 + 기존 패턴 탐색 + 외부 실환경 강제 금지** |
   | backend-system · rust-service (Phase 9) | **Outbox · Circuit Breaker + Rate Limiter 조합 · OAuth 2.1 draft 명시** |

7. **I-02 예외 목록 명시화** — 카이젠 세션 커밋 직전 `git status --short` 점검 시 modified/untracked 허용 예외는 고정 목록이다: `.harness/sprint-contract.md` (생성 대상) · `.harness/sprint-feedback.md` (QA 산출물) · `.harness/.meta/kaizen-data-pool.md` (auto-regenerated) · `.vscode/` (untracked) · sync-docs 자동 갱신 README/HTML. 이 외 modified 0 건이어야 한다 (2026-04 design-kit/infra-kit I-02 REJECT 재발 방지 — Phase 6 design-kaizen 패턴 계승).
8. **Phase 1~6 신규 원칙 감사 (kaizen 시작 시 전수 확인)** — skill §3.5 QA 계약 1:1 매칭 / §3.6 Rule-by-Rule Audit / §5.5 Enumerate-before-Act / §8.7 Code Examples / §8.8 Sibling Consistency / §11 Cross-Surface Parity · agent §3.5 Binary Decidability / §10 Unverifiable / §12 L3 Coverage Honesty 9 항목 전수 확인. 각 원칙에 대해 반영 스킬 목록을 리포트에 명시.
9. **README.md + evals/evals.json 생성 회귀 방지 (AR-03 · AR-04 대응)** — 카이젠 세션 종료 시 `ls backend-kit/README.md backend-kit/evals/evals.json` 확인. 둘 다 존재해야 하며 README 의 스킬 테이블은 4 스킬(guide · audit · system · test) 전수 + 에이전트 테이블 + 리서치 문서 카테고리 요약을 포함해야 한다. evals.json 은 4 스킬 커버 + entry 수 >= 7 + placeholder 0 건.
10. **run-evals.py ER-01 회귀 방지** — `scripts/run-evals.py` 의 `load_evals` 에서 `JSONDecodeError` 시 `sys.exit(2)` 로 즉시 종료하는 구조 유지. exit code 0(PASS) / 1(assertion FAIL) / 2(structural) 구분이 깨지면 CI 가 파싱 실패를 감지 못 함.

# Process

## Step 1: 현재 상태 읽기

backend-kit 스킬 3개 + backend-reviewer 에이전트의 Gotchas/Process/references 전체 읽기:
- backend-kit/skills/backend-guide/SKILL.md
- backend-kit/skills/backend-audit/SKILL.md
- backend-kit/skills/backend-system/SKILL.md
- backend-kit/agents/backend-reviewer.md

## Step 2: 격차 분석

docs/backend/ 문서의 원칙 중 스킬에 반영되지 않은 항목 식별:
- audit-criteria.md에 누락된 체크리스트 항목
- Gotchas에 추가할 반복 실패 패턴
- references에 추가할 새 원칙 문서

글로벌 피드백도 확인:
- ~/.harness/feedback/ 에서 backend-kit 관련 피드백 검색

## Step 3: 개선 적용

- SKILL.md Gotchas 추가/수정
- audit-criteria.md 체크리스트 갱신
- principle-index.md 매핑 갱신
- system-principles.md 카테고리 갱신

## Step 4: 검증

- 변경된 스킬의 description이 원래 트리거 조건과 일치하는지 확인
- 리서치 문서와 스킬 references 경로 정합성 확인

## Step 5: 커밋

```text
kaizen(backend-kit): [개선 내용 요약]
```

## Step 6: Plugin Validation 결과 반영

카이젠 세션 시작/종료 시 `scripts/validate-plugin.py backend-kit` 을 실행하여 7 카테고리 상태를 확인하고 결과를 개선 우선순위에 반영한다.

**실행 패턴, 우선순위 매핑, 통합 규칙**은 `harness/docs/guides/plugin-validation-guide.md §7` 에서 정의한다 (SSOT) — 해당 섹션을 그대로 따른다.

# References

- backend-kit/skills/backend-guide/SKILL.md
- backend-kit/skills/backend-audit/SKILL.md
- backend-kit/skills/backend-system/SKILL.md
- backend-kit/agents/backend-reviewer.md
- docs/backend/ — 리서치 SSOT
- `harness/docs/guides/plugin-validation-guide.md` — 플러그인 품질 7 카테고리 기준 (SSOT)
- `scripts/validate-plugin.py` — 플러그인 검증 자동화 도구
