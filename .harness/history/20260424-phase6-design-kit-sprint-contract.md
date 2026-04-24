---
feature: "kaizen-phase6-design-kit-kaizen"
created: "2026-04-24"
complexity: "high"
conditions: 20
branch: "kaizen/2026-04-24"
phase: 6
---

# Sprint Contract — Phase 6: Design-kit Kaizen

Generated: 2026-04-24
Feature: Phase 1~5 신규 원칙을 design-kit 8 스킬 + design-reviewer 에 전수하고, design-kit 5 REJECT reasons(SK-05 × 2, PH-01, I-02, AR-01, AR-06) 을 전수 해소한다. Phase 6 리서치 테이블 5 건(Tailwind v4 OKLCH · W3C DTCG v1 · WCAG 2.2 · MDN Container Queries · Material 3 Expressive) 을 최소 3 건 조회하고 변경 근거로 명시한다.

Scope (수정 허용): `design-kit/skills/*/SKILL.md`, `design-kit/agents/design-reviewer.md`, `design-kit/references/*.md`, `.claude/skills/design-kaizen/SKILL.md` (범위 외 금지: harness/, flutter-toolkit/, backend-kit/, infra-kit/, rust-kit/, react-kit/, reflect-kit/, planning-kit/, `design-kit/docs/design/` (리서치 문서는 design-research 영역), 기타 최상위 파일)
Branch: kaizen/2026-04-24

## Research (R)
- [ ] R-01 [structural]: Phase 6 리서치 테이블 5 건 중 최소 3 건의 URL 이 변경된 SKILL.md Gotchas 또는 본 문서 Context 섹션에 인용된다
- [ ] R-02 [structural]: design-kit 5 REJECT reasons(SK-05 × 2 · PH-01 · I-02 · AR-01 · AR-06) 각각에 대해 반영 파일 + 변경 내용이 커밋 메시지에 매핑된다
- [ ] R-03 [structural]: Phase 1~5 신규 원칙 8 건(skill §3.5/§3.6/§5.5/§8.7/§8.8/§11 · agent §3.5/§12) 의 design-kit 반영 스킬 목록 표가 커밋 메시지에 포함된다

## Skill Content — REJECT reason 전수 해소 (RR)
- [ ] RR-01 [exact]: `design-kit/skills/design-concept/SKILL.md` Process 에 **Step 0 = 자동 로드 (독립 단계)** 가 존재하며 제목이 "자동 로드" 또는 "자동 감지 및 로드" 로 명확히 표기되어 Gotchas 외부의 Process Step 으로 분류된다 (SK-05 대응, 현재 "Step 0: 기존 컨셉 감지" 를 design-component 와 동일한 표기로 sibling-align)
- [ ] RR-02 [exact]: `design-kit/skills/design-component/SKILL.md` Process 에 **Step 0: 자동 감지 및 로드** 가 독립 단계로 존재한다 (현재 존재함 — 유지 조건, sibling parity 보장)
- [ ] RR-03 [exact]: `design-kit/skills/design-mockup/SKILL.md` Gotchas 또는 계약 주석에 **HTML 산출물 예외 조항** 이 명시되어 `.design/mockups/*.html` 이 `.md` 계약 패턴과 구조적 차이를 갖는 것이 의도된 설계임을 선언한다 (AR-01 대응, 이미 Gotcha #10 존재 — 유지 + 정합성 확인)
- [ ] RR-04 [exact]: `design-kit/skills/design-system/SKILL.md` Gotcha #10 (HTML :root CSS 변수 정합성) 이 AR-06 재발을 명시적으로 언급하며 "기존 HTML 파일 과 값 일치 확인" 조건을 담는다 (AR-06 대응, 현재 존재 — 유지)
- [ ] RR-05 [exact]: `design-kit/agents/design-reviewer.md` 에 **Binary Decidability Pre-Check** 섹션이 존재한다 (PH-01 대응 — agent §3.5 전수)

## Skill Content — Phase 1~5 원칙 전수 (SK)
- [ ] SK-01 [exact]: `design-kit/skills/design-guide/SKILL.md` Gotchas 또는 Process Step 1 에 **가이드형 스킬 Process Step 순서 고정** (탐색→진단→처방) 선언이 있다 (Phase 5 principle, flutter-error/flutter-hooks 패턴 parity)
- [ ] SK-02 [exact]: `design-kit/skills/design-system/SKILL.md` Gotchas 에 **Enumerate-before-Act** (토큰 수정 전 전체 토큰 목록 + 위반 리스트업 후 편집) 원칙이 추가된다 (insights #1 · skill §5.5)
- [ ] SK-03 [exact]: `design-kit/skills/design-audit/SKILL.md` Gotchas 에 **Rule-by-Rule Audit 완료 선언 전 10 카테고리 전수 대조** 원칙이 명시된다 (skill §3.6)
- [ ] SK-04 [exact]: `design-kit/skills/design-audit/SKILL.md` Gotchas 에 **Binary Decidability Pre-Check** (감사 시작 전 각 FAIL 항목의 이진 판정 가능성 확인) 이 추가된다 (agent §3.5 skill 측 반영)
- [ ] SK-05 [exact]: `design-kit/agents/design-reviewer.md` "핵심 규칙" 또는 전용 섹션에 **Rule-by-Rule Audit · 미검증 3항 프로토콜 · L3 Coverage Honesty** 세 항목이 모두 존재한다
- [ ] SK-06 [exact]: `.claude/skills/design-kaizen/SKILL.md` 에 **Cross-Surface Parity Checklist** 섹션이 추가되어 design-kit sibling group(concept/component/mockup 자동로드 · audit/reviewer Rule-by-Rule · guide/system 가이드형 3-Step · reference/mockup HTML 출력) 의 공통 원칙 누락 검사 절차를 정의한다 (skill §11)
- [ ] SK-07 [exact]: `design-kit/skills/design-reference/SKILL.md` Gotchas 에 **Context7 / 공식 문서 출처 기재 형식 통일** (출처 URL 인라인, `출처:` 접두사) 원칙이 Phase 6 sibling Gotcha 표기법으로 통일된다 (Phase 5 원칙 4)

## I-02 명시화 (II)
- [ ] II-01 [exact]: 본 Sprint Contract 내 **I-02 조건** 에 예외 목록이 명시적 enumeration 으로 포함된다: `.harness/sprint-contract.md` (생성 대상) · `.harness/sprint-feedback.md` (QA 산출물) · `.harness/.meta/kaizen-data-pool.md` (auto-regenerated) · README 자동 동기화 파일. 이 외 modified 0 건.

## Implementation (I)
- [ ] I-01 [exact]: 모든 Phase 6 변경을 **단일 커밋** 으로 제출하고 메시지 prefix 는 `chore(kaizen-phase6):` 이다. 커밋 본문에 (a) REJECT reason 5 건 매핑 표, (b) Phase 1~5 원칙 반영 스킬 목록 표, (c) Context7/리서치 출처 URL 이 포함된다
- [ ] I-02 [exact]: 커밋 완료 후 `git status --short` 출력에서 다음 예외 외 modified / untracked 항목이 0 건이다 — 예외: `.harness/sprint-contract.md`, `.harness/sprint-feedback.md`, `.harness/.meta/kaizen-data-pool.md`, `.vscode/` (untracked), sync-docs 자동 갱신 README/HTML
- [ ] I-03 [exact]: `scripts/validate-plugin.py design-kit` 실행 시 7 카테고리 중 `refs` / `placeholders` / `code-fence` 카테고리에서 새로 FAIL 이 증가하지 않는다 (기존 FAIL 유지는 허용하되 새 FAIL 0 건)

## Evidence (E)
- [ ] E-01 [structural]: 각 RR / SK 조건에 대해 평가자가 `grep -n` 으로 즉시 검증 가능한 문자열 패턴이 존재한다 (본 문서 §Verification Commands 섹션)

## Verification Commands

```bash
# RR-01 design-concept Step 0
grep -nE '^## Step 0:' design-kit/skills/design-concept/SKILL.md   # → 1 line ≥ 1

# RR-02 design-component Step 0
grep -nE '^## Step 0:' design-kit/skills/design-component/SKILL.md  # → 1 line

# RR-03 design-mockup HTML 예외 조항
grep -nE 'HTML 형식이 정상 산출물|False positive|AR-01' design-kit/skills/design-mockup/SKILL.md  # → ≥1

# RR-04 design-system AR-06 언급
grep -nE 'AR-06|기존 HTML 파일' design-kit/skills/design-system/SKILL.md  # → ≥1

# RR-05 design-reviewer Binary Decidability
grep -nE 'Binary Decidability|이진 판정 가능성' design-kit/agents/design-reviewer.md  # → ≥1

# SK-01 design-guide 가이드형 3-Step
grep -nE '탐색.*진단.*처방|가이드형 스킬.*Process Step' design-kit/skills/design-guide/SKILL.md  # → ≥1

# SK-02 design-system Enumerate-before-Act
grep -nE 'Enumerate-before-Act|편집 전 전수 나열' design-kit/skills/design-system/SKILL.md  # → ≥1

# SK-03 design-audit Rule-by-Rule
grep -nE 'Rule-by-Rule|전수 대조' design-kit/skills/design-audit/SKILL.md  # → ≥1

# SK-04 design-audit Binary Decidability
grep -nE 'Binary Decidability|이진 판정' design-kit/skills/design-audit/SKILL.md  # → ≥1

# SK-05 design-reviewer Rule-by-Rule + 미검증 + L3 Coverage Honesty
grep -nE 'Rule-by-Rule|L3 Coverage|미검증' design-kit/agents/design-reviewer.md  # → ≥3 lines collectively

# SK-06 design-kaizen Cross-Surface Parity
grep -nE 'Cross-Surface Parity|Sibling Group' .claude/skills/design-kaizen/SKILL.md  # → ≥1

# SK-07 design-reference 출처 형식 통일
grep -cE '출처:' design-kit/skills/design-reference/SKILL.md  # → ≥1

# I-03 validate-plugin
python3 scripts/validate-plugin.py design-kit
```

## Phase 6 Research Sources (사전 조회 · ≥3 필수)

| # | 소스 | 유형 | 조회 상태 |
|---|------|------|----------|
| 1 | [Tailwind CSS v4 blog](https://tailwindcss.com/blog/tailwindcss-v4) | 공식 | 기존 design-system Gotcha #11 에 인용됨 ✓ |
| 2 | [W3C DTCG v1 Final Report 2025-10-28](https://www.w3.org/community/reports/design-tokens/CG-FINAL-format-20251028/) | 표준 | 기존 design-system Gotcha #12, design-component Gotcha #3 에 인용됨 ✓ |
| 3 | [W3C WCAG 2.2](https://www.w3.org/TR/WCAG22/) | 표준 | 기존 design-audit Gotcha #3, design-reviewer #3-#4 에 인용됨 ✓ |
| 4 | [MDN Container Queries](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_container_queries) | 공식 | 기존 design-audit 8, design-mockup Gotcha #10 에 인용됨 ✓ |
| 5 | Material 3 Expressive (2025-05) | 공식 | 기존 design-system Step 2 참고 섹션에 인용됨 ✓ |

결과: 5 / 5 기 인용 상태로 R-01 충족.
