---
name: design-kaizen
description: >
  design-kit 스킬 품질을 design-kit/docs/design/ 리서치 문서 기준으로 주기적으로 개선한다.
  이 레포 개발용 스킬이며, design-kit 플러그인에 포함되지 않는다.
  harness-kaizen, flutter-kaizen과 동일한 패턴.
  "/design-kaizen", "디자인 카이젠", "design-kit 개선" 같은 요청 시 트리거.
argument-hint: "[skill-name]"
user-invocable: true
---

# Gotchas

1. **리서치 문서 먼저 확인** — 스킬을 수정하기 전에 design-kit/docs/design/ 문서가 최신인지 확인하라. 오래된 리서치를 기반으로 스킬을 개선하면 잘못된 원칙이 반영된다.
2. **Gotchas 추가 시 실패 근거 필수** — "이런 실수를 할 수 있다"가 아니라 "실제로 이런 실패가 발생했다"는 근거가 있어야 한다. 추측성 Gotchas는 추가하지 않는다.
3. **기존 스킬 구조 유지** — SKILL.md의 섹션 구조(Gotchas → Process → References)를 변경하지 마라. 내용만 개선한다.
4. **audit-criteria.md와 스킬 Gotchas 중복 금지** — audit-criteria.md는 체크리스트 항목, Gotchas는 반복 실수 방지 지침이다. 같은 내용을 양쪽에 복사하지 마라. 역할이 다르다.
5. **validate-plugin.py 실행 없이 완료 선언 금지** — 카이젠 세션 종료 시 반드시 `scripts/validate-plugin.py design-kit`을 실행하라. **8 카테고리 (V1~V8: frontmatter / templates / refs / triggers / placeholders / code-fence / plugin-json / hook-exec)** 중 하나라도 FAIL이면 수정 후 재검증한다. 실행 출력을 인용하지 않은 "검증 통과" 보고는 증거가 아니다 (skill-design-guide §3.7 Completion Evidence Gate).
6. **Cross-Surface Parity Checklist (skill-design-guide §11 · agent-design-guide §12 대응)** — 스킬 개선 시 아래 sibling group 간 공통 원칙(Gotcha · Process Step · 자동 로드 로직) 의 누락을 **1:1 Grep 대조** 로 확인한다. 누락된 sibling 이 있으면 즉시 동일 표현을 복제하여 비대칭 지식 상태를 제거한다 (2026-04 design-kit SK-05 REJECT 재발 방지 — design-concept 에 Step 0 자동 로드는 있었지만 design-component 에는 Gotcha 외부의 Process Step 형태로만 있어 평가자 판정 갈렸던 사례).

   | Sibling Group | 공통 원칙 검증 항목 |
   |---------------|---------------------|
   | design-concept · design-component · design-mockup · design-reference | **Step 0 = 자동 감지 및 로드** 독립 Process 단계 존재 (Gotchas 외부, 이름 정확히 일치) |
   | design-audit · design-reviewer (agent) | **Binary Decidability Pre-Check · Rule-by-Rule Audit · 미검증 임계 2 (canonical) · Evidence Validity Gate 4 검사 · Before/After 의도 외 영역 FAIL · L3 Coverage Honesty** 6 항목 동시 존재. 임계값·마커 의미는 `harness/docs/guides/qa-evaluation-guide.md` §Canonical Unverified-Evidence Protocol 이 정본이며 킷에서 재정의 금지 |
   | design-mockup · design-concept | **승인 기록 아티팩트(`.design/approvals/`) 생성 Process Step** 존재 (글로벌 REJECT UI-06 대응) |
   | design-system · design-mockup · design-guide | **Visual Source of Truth Precedence · Partial Visual Change Isolation** 인용 (`design-kit/references/visual-change-protocol.md` SSOT) |
   | design-guide · design-system | **가이드형 스킬 Process Step 순서 고정 (탐색→진단→처방) · Enumerate-before-Act** |
   | design-mockup · design-reference | **HTML 산출물 의도 설계 명시 (AR-01 예외 선언)** |
   | design-system · design-component | **DTCG v1 · OKLCH · 다크모드 토큰 매핑** 공통 원칙 정합성 |

7. **I-02 예외 목록 명시화** — 카이젠 세션 커밋 직전 `git status --short` 점검 시 modified/untracked 허용 예외는 고정 목록이다: `.harness/sprint-contract.md` (생성 대상) · `.harness/history/*-sprint-contract.md` (오케스트레이터 병렬 실행 시 Phase 별 계약 경로) · `.harness/sprint-feedback.md` (QA 산출물) · `.harness/.meta/kaizen-data-pool.md` (auto-regenerated) · `.vscode/` (untracked) · sync-docs 자동 갱신 README/HTML. 이 외 modified 0 건이어야 한다 (2026-04 design-kit/infra-kit I-02 REJECT 재발 방지).

   **오케스트레이터 병렬 실행 중에는 git add/commit/tag 를 직접 실행하지 마라** — 다른 Phase 서브에이전트와 index.lock 이 충돌한다. 커밋은 오케스트레이터가 직렬 처리한다 (Step 5 참조).

8. **Phase 1~5 신규 원칙 감사 (kaizen 시작 시 전수 확인)** — skill §3.5 QA 계약 1:1 매칭 / §3.6 Rule-by-Rule Audit / §3.7 Completion Evidence Gate + Enforcement 등급 / §5.5 Enumerate-before-Act · Counterpart Enumeration / §8.7 Code Examples / §8.8 Sibling Consistency / §11 Cross-Surface Parity · agent §3.5 Binary Decidability / §10 Unverifiable / §12 Parity 전수 확인. 각 원칙에 대해 반영 스킬 목록을 리포트에 명시.

9. **scope-creep 판정은 파일 수가 아니라 unit(관심사) 수 기준** — "3 파일 이상 변경 = 과잉" 같은 파일 카운트 휴리스틱을 쓰지 마라. 하나의 원칙을 sibling parity 로 5 개 스킬에 복제하는 것은 1 unit 이고, 무관한 개선 2 건을 한 스킬에 넣는 것은 2 unit 이다. 판정 기준은 **이번 사이클 신호에 대응하는 서로 다른 관심사가 몇 개인가** 다 (Phase 4 harness-kaizen 전달 · contract-design-guide `complexity-by-file-count` 결함 대응).

10. **NO_CHANGE 도 유효한 결과다** — 데이터 풀과 §0 인사이트를 다 뒤졌는데 design 도메인 신규 신호가 0 건이면 **NO_CHANGE 로 보고하라**. 직전 사이클 승격분의 문장을 다시 다듬는 것은 개선이 아니다. 같은 위반이 재발했다면 문장 수정이 아니라 **enforcement 등급 상향**(E1 문장 → E2 체크리스트 아티팩트 → E3 결정론적 게이트)이 정답이다 (skill-design-guide §3.7 등급 승급 규칙).

# Process

## Step 1: 현재 상태 파악

design-kit 스킬 8개(design-audit · design-component · design-concept · design-guide · design-mockup · design-reference · design-system · design-test) + 에이전트 1개(design-reviewer) + 공유 references(`design-kit/references/`)의 현재 Gotchas, Process, 참조 내용을 읽는다.

## Step 2: 리서치 문서 대비 격차 분석

design-kit/docs/design/ 문서의 원칙 중 스킬에 반영되지 않은 항목을 식별한다:
- audit-criteria.md에 누락된 체크리스트 항목
- Gotchas에 추가할 반복 실패 패턴
- references에 추가할 새 원칙 문서

## Step 3: 개선 적용

격차 항목별로:
1. Gotchas 추가 — 실패 근거가 있는 항목만
2. references 갱신 — 새 원칙 추가
3. Process 보완 — 누락된 단계 추가

## Step 4: evals 갱신

개선 사항에 맞춰 evals/evals.json에 assertion 추가 또는 수정.

## Step 5: 커밋

리서치 로그(`docs/design/research-log.md`)도 이 스킬의 산출물이므로 함께 스테이징한다 — 빠뜨리면
개선 근거 출처가 커밋에서 누락된다.

```bash
git add design-kit/ .claude/skills/design-kaizen/ docs/design/research-log.md
git commit -m "kaizen(design-kit): [개선 요약]"
```

**오케스트레이터가 Phase 로 호출한 경우 이 Step 을 실행하지 마라** (Gotcha 7) — 병렬 서브에이전트와
index.lock 이 충돌한다. 변경 파일 목록만 리포트하고 커밋은 오케스트레이터에 넘긴다.

## Step 6: Plugin Validation 결과 반영

카이젠 세션 시작/종료 시 `scripts/validate-plugin.py design-kit` 을 실행하여 8 카테고리(V1~V8) 상태를 확인하고 결과를 개선 우선순위에 반영한다.

**실행 패턴, 우선순위 매핑, 통합 규칙**은 `harness/docs/guides/plugin-validation-guide.md §7` 에서 정의한다 (SSOT) — 해당 섹션을 그대로 따른다.

# References

- 기존 카이젠 패턴: `.claude/skills/kaizen-orchestrator/SKILL.md`
- harness-kaizen: `harness/skills/harness-kaizen/SKILL.md`
- flutter-kaizen: `flutter-toolkit/skills/flutter-kaizen/SKILL.md`
- `harness/docs/guides/plugin-validation-guide.md` — 플러그인 품질 8 카테고리(V1~V8) 기준 (SSOT)
- `scripts/validate-plugin.py` — 플러그인 검증 자동화 도구
- `harness/docs/guides/qa-evaluation-guide.md` — §Canonical Unverified-Evidence Protocol · §Evidence Validity Gate (design-reviewer 복제 원본)
- `harness/docs/guides/skill-design-guide.md` — §3.7 Completion Evidence Gate · Enforcement 등급 E1/E2/E3 (SSOT)
- `design-kit/references/visual-change-protocol.md` — 시각 변경 우선순위 · 부분 변경 격리 · 증거 블록 · 승인 기록 (킷 내 SSOT)
