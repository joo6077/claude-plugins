---
feature: "세션 전체 빡센 종합 QA — react-kit + plugin-validation + simplify 리팩터"
created: "2026-04-11T17:00:00+09:00"
complexity: "매우 복잡"
conditions: 30
scope: "이번 세션 전체 67 commits 의 모든 변경 사항 — react-kit v0.1.0 (21 스킬 + 3 에이전트), docs/react-kit/ 9 HTML 페이지, plugin-validation 인프라 (가이드 + validate-plugin.py + plugin_utils.py), kaizen-orchestrator 확장 (Phase 10 + 9 kaizen 스킬 plugin-validation Step 통합), simplify 리팩터 (CheckContext dispatch + SSOT 통합). 빡세게 실행 검증 + 구조적 무결성 + 교차 참조 + 회귀 + 문서 정합성 전수 검사."
---

## Execution (E) — 실제 실행 결과 검증
- [ ] E-01: `python3 scripts/validate-plugin.py --help` 실행 시 usage 출력 정상, exit 0
- [ ] E-02: `python3 scripts/validate-plugin.py backend-kit` 실행 시 7 체크 모두 PASS, exit 0 (backend-kit 은 이번 세션 최종 상태에서 유일한 ALL-OK 킷)
- [ ] E-03: `python3 scripts/validate-plugin.py` (전체) 실행 시 "Total: 7 plugins, 1 OK, 6 ERROR" 출력, exit 2
- [ ] E-04: `python3 scripts/validate-plugin.py --check=frontmatter` 실행 시 flutter-hooks `user-invocable` 누락 FAIL 감지, exit 2
- [ ] E-05: `python3 scripts/validate-plugin.py backend-kit --check=frontmatter,templates` 실행 시 2 체크만 실행되고 exit 0
- [ ] E-06: `python3 scripts/validate-plugin.py backend-kit --json` 출력이 `python -c "import json, sys; json.load(sys.stdin)"` 로 파싱 성공
- [ ] E-07: `python3 scripts/sync-docs.py --check-only` 실행 시 "모든 README가 동기화 상태입니다" + exit 0
- [ ] E-08: `python3 scripts/sync-docs.py --check-only react-kit` (단일 kit) 실행 성공
- [ ] E-09: `python3 -c "from plugin_utils import load_marketplace, list_kits, read_text, parse_frontmatter, parse_frontmatter_raw, iter_skills, iter_agents, REPO_ROOT; print(list_kits())"` 시 7 kits 출력

## Structural Correctness (S) — 구조적 올바름
- [ ] S-01: `CheckContext` dataclass 가 `validate-plugin.py` 에 정의, 필드 `kit_path, marketplace_data, fix, all_keywords, _file_cache` 5개
- [ ] S-02: `CHECK_REGISTRY` dict 가 정확히 7 entries — frontmatter, templates, refs, triggers, placeholders, code-fence, plugin-json
- [ ] S-03: 7 check 함수 모두 시그니처 `check_vN(ctx: CheckContext) -> CheckResult` 통일
- [ ] S-04: `validate_kit()` 가 for-loop 기반 dispatch 사용 (if-chain 없음) — `grep "if \"frontmatter\" in" scripts/validate-plugin.py` → 0 hit
- [ ] S-05: V5 `check_v5_placeholders` 와 V6 `check_v6_code_fence` 가 `--fix` 모드에서 `path.write_text(...)` 직후 `ctx.invalidate(path)` 호출 (cache stale 방지 필수)
- [ ] S-06: `plugin_utils.parse_frontmatter` (pyyaml) 와 `parse_frontmatter_raw` (line-based) 두 함수 모두 export, sync-docs 는 `parse_frontmatter_raw`, validate-plugin 은 `parse_frontmatter` 사용

## Cross-reference Integrity (X) — 교차 참조 무결성
- [ ] X-01: `react-kit/skills/` 하에 21 개 SKILL.md 존재 (`find react-kit/skills -name SKILL.md | wc -l` = 21)
- [ ] X-02: `react-kit/agents/` 하에 3 개 에이전트 .md 존재 (widget-inspector-react, animation-architect-react, react-reviewer)
- [ ] X-03: `.claude-plugin/marketplace.json` 에 7 plugins 등록 (harness, flutter-toolkit, design-kit, backend-kit, infra-kit, rust-kit, react-kit)
- [ ] X-04: `git tag -l "react-kit/v0.1.0"` 출력 존재 + `git ls-remote origin refs/tags/react-kit/v0.1.0` 으로 origin push 확인
- [ ] X-05: `docs/react-kit/` 하에 9 HTML 파일 존재 (scaffolding, state-data, performance, quality, ui-patterns, animation, build-audit, wasm-catalog, integration)
- [ ] X-06: `docs/index.html` 의 categories 배열에 `react-` prefix 9 entries 존재 (`grep "id: 'react-" docs/index.html | wc -l` = 9)
- [ ] X-07: 9 kaizen 스킬 (react-kaizen, rust-kaizen, backend-kaizen, infra-kaizen, design-kaizen, flutter-kaizen, harness-kaizen, contract-kaizen, evaluator-kaizen) 모두에 `plugin-validation-guide.md §7` 링크 존재
- [ ] X-08: `harness/docs/guides/plugin-validation-guide.md` 에 §7.1 ~ §7.5 subsection 5 개 존재 (실행 패턴/우선순위 매핑/통합 규칙/참조 방식/갱신 기준)
- [ ] X-09: `.claude/skills/kaizen-orchestrator/SKILL.md` description + Phase 의존성 다이어그램에 react-kit Phase 10 포함

## Regression (R) — 이전 기능 보존
- [ ] R-01: `react-kit/skills/react-animation/SKILL.md` 의 Library Policy 금지 목록에 Motion/framer-motion/dnd-kit/react-spring/react-transition-group 5개 모두 여전히 명시
- [ ] R-02: `react-kit/agents/animation-architect-react.md` 에도 동일 금지 목록 유지
- [ ] R-03: `react-kit/skills/react-audit/SKILL.md` 의 Library Policy 6 카테고리에 동일 금지 라이브러리 빌드 게이트 명시
- [ ] R-04: Simplify 리팩터 전후 `validate-plugin.py` 출력 회귀 없음 (git show 2613f6a 기반 비교 또는 동등)

## Integrity (I) — 무결성
- [ ] I-01: Working tree clean (`git status --short` 결과에 `scripts/__pycache__/` 같은 untracked 외 실제 수정 0건)
- [ ] I-02: Local main 과 `origin/main` 동기화 (`git log origin/main..main` empty)
- [ ] I-03: 67 개 이번 세션 commits 가 모두 linear history (no merge commits 또는 merge 가 의도된 경우만)
- [ ] I-04: `marketplace.json` valid JSON parse 성공
- [ ] I-05: 21 react-kit SKILL.md + 3 agent.md + 9 kaizen SKILL.md 모두 YAML frontmatter parse 성공

## Documentation (D) — 문서 완결성
- [ ] D-01: `CLAUDE.md` Skills Reference 섹션에 react-kit 21 스킬 + 3 에이전트 표 존재
- [ ] D-02: `CLAUDE.md` Commands 섹션에 `python3 scripts/validate-plugin.py` 사용법 4가지 명령 예시 + 가이드 경로
- [ ] D-03: `docs/superpowers/followup-2026-04-11-plugin-validation-findings.md` 존재 (7 kit 검증 리포트)
