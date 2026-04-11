---
feature: "카이젠 전체 오케스트레이트 + V4 context disambiguation 종합 QA"
created: "2026-04-11T18:00:00+09:00"
complexity: "매우 복잡"
conditions: 26
scope: "이번 세션 카이젠 14 commits (Step 0 pre-flight + Phase 1~10 + Final + V4 disambiguation) 전체. 실행 검증 + 구조적 무결성 + 회귀 + 문서-코드 정합성 빡세게 검사."
---

## Execution (E) — 실제 실행 결과
- [ ] E-01: `python3 scripts/validate-plugin.py` 전체 실행 시 **"Total: 7 plugins, 7 OK"** + Exit 0
- [ ] E-02: `python3 scripts/validate-plugin.py backend-kit` Exit 0 (카이젠 전후 유지)
- [ ] E-03: `python3 scripts/validate-plugin.py react-kit` Exit 0 (V6 1→0 + V4 disambiguation 적용)
- [ ] E-04: `python3 scripts/validate-plugin.py flutter-toolkit` Exit 0 (V1 1→0 + V6 26→0 + V4 disambiguation)
- [ ] E-05: `python3 scripts/validate-plugin.py rust-kit` Exit 0 (V5 7→0 + V6 11→0)
- [ ] E-06: `python3 scripts/validate-plugin.py harness` Exit 0 (V5 1→0 + V6 8→0)
- [ ] E-07: `python3 scripts/sync-docs.py --check-only` → "모든 README가 동기화 상태입니다"
- [ ] E-08: `python3 scripts/collect-kaizen-data.py --skip-validate` 실행 성공 (Step 0 pre-flight 스크립트 정상 동작)

## Step 0 Pre-flight Infrastructure (P)
- [ ] P-01: `scripts/collect-kaizen-data.py` 존재, Python 표준 lib + pyyaml 만 의존
- [ ] P-02: `.harness/.meta/kaizen-data-pool.md` 존재 (collect-kaizen-data 생성물)
- [ ] P-03: `.claude/skills/kaizen-orchestrator/SKILL.md` 에 **"Step 0: Pre-flight"** 섹션 존재 + Phase 의존성 다이어그램에 Step 0 포함

## V4 Context Disambiguation (VD) — 이번 응답의 핵심
- [ ] VD-01: `scripts/validate-plugin.py` 에 `KIT_CONTEXT_TOKENS` 상수 정의, 7 kit 각각 고유 단어 집합 포함
- [ ] VD-02: `CheckContext` 에 `all_context_hits: dict[str, bool]` 필드 추가
- [ ] VD-03: `_collect_cross_kit_keywords` 가 `(keywords, context_hits)` tuple 반환하도록 변경
- [ ] VD-04: `check_v4_triggers` cross-kit 분기에서 양쪽 `context_hit=True` 시 WARN 제거
- [ ] VD-05: `harness/docs/guides/plugin-validation-guide.md §3.4` 에 "Cross-kit context disambiguation" 예외 규칙 명시 + PASS 예시 포함
- [ ] VD-06: V4 적용 후 cross-kit WARN 이 0 건 (validate-plugin 출력에서 "WARN ... cross-kit" 0건 검증)

## Phase 결과 반영 (PH)
- [ ] PH-01: Phase 1 — `harness/docs/guides/skill-design-guide.md` 및 `agent-design-guide.md` 에 트리거 키워드 배타성/계약 모호성 방지/L3 검증 원칙 3종 추가
- [ ] PH-02: Phase 2 — `harness/docs/guides/contract-design-guide.md` 에 `[L1]`/`[L2]`/`[L3]` 구체성 레벨 + 예외 조항 포맷 추가
- [ ] PH-03: Phase 3 — `harness/docs/guides/qa-evaluation-guide.md` 에 "용어 구분" 섹션 존재 (Phase 2 `[L1/L2/L3]` vs evaluator 검증 깊이 L1~L3 분리)
- [ ] PH-04: Phase 10 — `react-kit/references/common-gotchas.md` 신규 생성 (6개 Gotchas: 키워드 유일성, Library Policy, placeholder, card-source, References 개별 명시, bad-good 예시)
- [ ] PH-05: Phase 8 — `infra-kit/references/` 디렉토리 생성 + 3 파일 (principle-index, audit-criteria, init-checklist)

## Integrity (I) — 무결성
- [ ] I-01: Local main 과 `origin/main` 동기 (`git log origin/main..main` 비어있음)
- [ ] I-02: 카이젠 구현 자체는 clean. QA 평가 과정의 side effect 는 예외: (a) `.harness/sprint-contract.md` (이 계약 파일 자체), (b) `.harness/.meta/kaizen-data-pool.md` (E-08 실행으로 재생성), (c) `scripts/__pycache__/` (Python 바이트코드 캐시). 이 3 항목 외에는 modified 0 건
- [ ] I-03: 카이젠 14 commits 모두 linear history (0 merge commits)
- [ ] I-04: `validate-plugin.py` 자체가 Python 문법 유효 (`python3 -m py_compile scripts/validate-plugin.py` 성공)

## Library Policy 회귀 검증 (LP)
- [ ] LP-01: `react-kit/skills/react-animation/SKILL.md` Gotcha 1 금지 목록에 Motion/framer-motion/dnd-kit/react-spring/react-transition-group 5 건 유지
- [ ] LP-02: `react-kit/agents/animation-architect-react.md` 절대 금지 라이브러리 목록에 동일 5 건 유지
