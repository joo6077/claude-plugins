---
name: infra-kaizen
description: >
  infra-kit 스킬 품질을 docs/infra/ 리서치 문서 기준으로 주기적으로 개선한다.
  이 레포 개발용 스킬이며, infra-kit 플러그인에 포함되지 않는다.
  "/infra-kaizen", "인프라 카이젠", "infra-kit 개선" 같은 요청 시 트리거.
  단순 버그 수정이나 기능 구현 요청에는 트리거하지 않는다.
argument-hint: ""
user-invocable: true
---

# Gotchas

1. **추측성 Gotchas 추가 금지** — 실제 실패 근거 없이 추가하지 마라.
2. **리서치 문서 기반만** — docs/infra/ 문서에 없는 원칙을 스킬에 추가하지 마라.
3. **스킬 범위 변경 금지** — description 변경은 사용자 승인 필수.
4. **scope-creep 은 파일 수가 아니라 unit(관심사) 수로 센다** — "스킬 4개 중 2개만" 같은 파일 개수 규칙은 무의미하다. 한 사이클에서 다루는 **독립 관심사(concern)** 를 1~2 개로 제한하라. 예: "canonical 프로토콜 정합화" 1 unit 은 reviewer + audit + test 3 파일에 걸쳐도 1 unit 이고, 반대로 한 파일 안에서 "Gotcha 추가 + Process 재구조화 + description 변경" 을 하면 3 unit 이다. 관심사가 3 개를 넘으면 다음 사이클로 미뤄라.
5. **validate-plugin.py 실행 없이 완료 선언 금지** — 카이젠 세션 종료 시 반드시 `scripts/validate-plugin.py infra-kit`을 실행하여 **8 카테고리(V1 frontmatter · V2 templates · V3 refs · V4 triggers · V5 placeholders · V6 code-fence · V7 plugin-json · V8 hook-exec)** 상태를 확인하라. 회귀가 발생하면 즉시 수정한다.
6. **Cross-Surface Parity Checklist (skill-design-guide §11 · agent-design-guide §12 대응)** — 스킬 개선 시 아래 sibling group 간 공통 원칙(Gotcha · Process Step · 자동 로드 로직) 의 누락을 **1:1 Grep 대조** 로 확인한다. 누락된 sibling 이 있으면 즉시 동일 표현을 복제하여 비대칭 지식 상태를 제거한다 (2026-04 infra-kit Phase 8 에서 backend-kit Phase 7 반영 때 반복 드리프트 차단).

   | Sibling Group | 공통 원칙 검증 항목 |
   |---------------|---------------------|
   | infra-guide · infra-init | **3-Step Process (탐색→진단→처방)** + Enumerate-before-Act + 트레이드오프 제시 |
   | infra-audit · infra-reviewer (agent) | **Binary Decidability Pre-Check · Rule-by-Rule Audit · 미검증 3항 · L3 Coverage Honesty** 4 항목 동시 존재 |
   | infra-guide · infra-audit · infra-init · infra-test | **10 카테고리 명명 규칙** 일치 (Container · CI/CD · Kubernetes · IaC · Security · Supply Chain · Backup & DR · Deployment · Observability · Cost Optimization) |
   | infra-test · backend-test | **Step 0 스택 감지 독립 단계 + 기존 패턴 탐색 + 외부 실환경 강제 금지** |
   | infra-init · backend-system (Phase 7) | **Enumerate-before-Act + 3-Step Process + 기존 설정 덮어쓰기 금지** |

7. **I-02 예외 목록 명시화** — 카이젠 세션 커밋 직전 `git status --short` 점검 시 modified/untracked 허용 예외는 고정 목록이다: `.harness/sprint-contract.md` (생성 대상) · `.harness/history/*.md` (**병렬 Phase 실행 시 contract 는 여기 쓴다** — `.harness/sprint-contract.md` 는 Phase 간 충돌하므로 쓰지 마라) · `.harness/sprint-feedback.md` (QA 산출물) · `.harness/.meta/kaizen-data-pool.md` (auto-regenerated) · `.vscode/` (untracked) · sync-docs 자동 갱신 README/HTML. 이 외 modified 0 건이어야 한다 (2026-04 infra-kit I-02 REJECT 재발 방지 — Phase 6/7 design-kit/backend-kit 패턴 계승). **HTML/비-.md 산출물 예외**: infra-kit 의 산출물에 `Dockerfile` · `*.tf` · `*.yml` (docker-compose, GitHub Actions, K8s manifest, helm/kustomize) 이 포함될 경우 placeholder/bare code-fence 규칙의 `.md` 전용 검사에서 제외한다 (파일 포맷상 태그 없는 fence 가 정상).
8. **선행 Phase 신규 원칙 감사 (kaizen 시작 시 전수 확인)** — skill §3.5 QA 계약 1:1 매칭 / §3.6 Rule-by-Rule Audit / **§3.7 Completion Evidence Gate** / §5.5 Enumerate-before-Act + Counterpart Enumeration / §8.7 Code Examples / §8.8 Sibling Consistency / §11 Cross-Surface Parity · agent §3.5 Binary Decidability / §10 Unverifiable / §12 L3 Coverage Honesty 전수 확인. 각 원칙에 대해 반영 스킬 목록을 리포트에 명시. 아래 두 SSOT 는 **인용만 하고 infra-kit 문서에서 재정의하지 마라**:

   | SSOT | 위치 | infra-kit 에서 하는 일 |
   |------|------|------------------------|
   | Enforcement 등급 E1/E2/E3 + 승급 규칙(2 회 재발 → E2, 3 회 → E3) | `harness/docs/guides/skill-design-guide.md` §3.7 | 등급을 **판정**만 한다. 동의어(강/중/약 등) 신설 금지 |
   | Canonical Unverified-Evidence Protocol 5 조항 | `harness/docs/guides/qa-evaluation-guide.md` §Canonical Unverified-Evidence Protocol | `infra-reviewer.md` §9 에 **문구 변형 없이** 복제. 임계값 재정의 금지 |

   ⚠ Counterpart Conditions 의 evaluator 측 대응 절은 **의도된 부재**(parity item 12)다. 만들지 마라.
9. **README.md + evals/evals.json 생성 회귀 방지 (AR-03 · AR-04 대응)** — 카이젠 세션 종료 시 `ls infra-kit/README.md infra-kit/evals/evals.json` 확인. 둘 다 존재해야 하며 README 의 스킬 테이블은 4 스킬(guide · audit · init · test) 전수 + 에이전트 테이블 + 리서치 문서 카테고리 요약을 포함해야 한다. evals.json 은 4 스킬 커버 + entry 수 >= 5 + placeholder 0 건.
10. **SK-07 / SK-08 Step 3 공백 회귀 방지** — infra-audit Step 3 는 Rule-by-Rule 20-row 표(#/카테고리/체크항목/판정/근거/출처) + CONDITIONAL APPROVE 규칙. infra-init Step 3 는 카테고리별 (현재/권장/개선) 포맷 + 최소 1 개 예시. 둘 다 자리표시자(`...`) 0 건.

# Process

## Step 1: 현재 상태 읽기

infra-kit 스킬 4개 + infra-reviewer 에이전트:
- infra-kit/skills/infra-guide/SKILL.md
- infra-kit/skills/infra-audit/SKILL.md
- infra-kit/skills/infra-init/SKILL.md
- infra-kit/skills/infra-test/SKILL.md
- infra-kit/agents/infra-reviewer.md

## Step 2: 격차 분석

docs/infra/ 원칙 vs 스킬 반영 상태:
- audit-criteria.md 누락 항목
- Gotchas 추가 필요 패턴
- 글로벌 피드백 (~/.harness/feedback/)

## Step 3: 개선 적용

- SKILL.md Gotchas 추가/수정
- audit-criteria.md 체크리스트 갱신
- principle-index.md 매핑 갱신
- init-checklist.md 카테고리 갱신

## Step 4: 검증

- description 트리거 조건 유지 확인
- 리서치 문서 ↔ 스킬 references 경로 정합성
- Cross-Surface Parity Grep 대조 (Gotcha 6)

## Step 5: 커밋

```text
chore(kaizen-phase<N>): [개선 내용 요약]
```

## Step 6: Plugin Validation 결과 반영

카이젠 세션 시작/종료 시 `scripts/validate-plugin.py infra-kit` 을 실행하여 8 카테고리(V1~V8) 상태를 확인하고 결과를 개선 우선순위에 반영한다.

**실행 패턴, 우선순위 매핑, 통합 규칙**은 `harness/docs/guides/plugin-validation-guide.md §7` 에서 정의한다 (SSOT) — 해당 섹션을 그대로 따른다.

# References

- infra-kit/skills/infra-guide/SKILL.md
- infra-kit/skills/infra-audit/SKILL.md
- infra-kit/skills/infra-init/SKILL.md
- infra-kit/skills/infra-test/SKILL.md
- infra-kit/agents/infra-reviewer.md
- infra-kit/references/audit-criteria.md — 카테고리별 PASS/FAIL 기준 SSOT
- infra-kit/references/init-checklist.md — init 카테고리 체크리스트 SSOT
- infra-kit/references/principle-index.md — 원칙 인덱스
- docs/infra/ — 리서치 SSOT (platform / operations / security)
- `harness/docs/guides/plugin-validation-guide.md` — 플러그인 품질 8 카테고리(V1~V8) 기준 (SSOT)
- `harness/docs/guides/skill-design-guide.md` §3.7 — Completion Evidence Gate + Enforcement 등급 E1/E2/E3 (SSOT)
- `harness/docs/guides/qa-evaluation-guide.md` §Canonical Unverified-Evidence Protocol — `[미검증]` 마커·임계값 정본 (SSOT)
- `scripts/validate-plugin.py` — 플러그인 검증 자동화 도구
- `scripts/run-evals.py` — 플러그인 evals 자동화 도구
