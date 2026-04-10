---
feature: "react-kit Phase 10: 카이젠 스킬 + 최종 전체 정합성 검증"
created: "2026-04-10T21:30:00+09:00"
complexity: "중간"
conditions: 16
scope: ".claude/skills/react-kaizen + react-research 추가 + CLAUDE.md 갱신 + react-kit 전체 (21 스킬 + 3 에이전트) 정합성 최종 검증"
---

## Kaizen Skills
- [ ] KZ-01: `.claude/skills/react-kaizen/SKILL.md` 존재. frontmatter 유효 + name=react-kaizen + description ("React 카이젠", "react-kit 개선" 키워드 포함)
- [ ] KZ-02: `.claude/skills/react-research/SKILL.md` 존재. frontmatter 유효 + name=react-research + description ("React 리서치", "React 문서 갱신" 키워드 포함)
- [ ] KZ-03: 두 카이젠 스킬이 rust-kaizen / rust-research 와 동일한 구조 (Gotchas + Process + References) 따름
- [ ] KZ-04: react-kaizen 의 References 가 `docs/react/kit-design/` 7개 그룹 문서 + wasm-catalog 모두 명시

## Documentation
- [ ] DC-01: `CLAUDE.md` 의 "Skills Reference" 섹션에 react-kit 21 스킬 + 3 에이전트 표가 추가됨 (rust-kit 표 직후)
- [ ] DC-02: `CLAUDE.md` 의 Repository Overview 에 react-kit 항목이 존재 (이미 line 16)

## Plugin Final State
- [ ] PF-01: `react-kit/skills/` 하에 정확히 21개 스킬 디렉토리 존재 (각 SKILL.md 포함)
- [ ] PF-02: `react-kit/agents/` 하에 정확히 3개 에이전트 .md 존재 (widget-inspector-react, animation-architect-react, react-reviewer)
- [ ] PF-03: `react-kit/.claude-plugin/plugin.json` version=0.1.0
- [ ] PF-04: `.claude-plugin/marketplace.json` 의 react-kit 엔트리 description 에 v0.1.0 + 2026-04-10 + "21종 스킬 + 3 에이전트" 포함
- [ ] PF-05: git tag `react-kit/v0.1.0` 존재

## Library Policy (전 플러그인 일관)
- [ ] LP-01: `react-kit/skills/react-animation/SKILL.md` 와 `react-kit/agents/animation-architect-react.md` 모두에 Motion/framer-motion/dnd-kit/react-spring/react-transition-group 금지 명시
- [ ] LP-02: `react-kit/skills/react-audit/SKILL.md` Library Policy 카테고리가 동일 라이브러리 목록을 빌드 게이트로 명시

## Sync Docs
- [ ] SD-01: `python3 scripts/sync-docs.py --check-only react-kit` 실행 시 "동기화됨" 상태 (AUTO:skills 21개 + AUTO:agents 3개)

## Diagnostics
- [ ] DG-01: `react-kit/` 디렉토리 전체 placeholder (TODO/TBD/FIXME) 0건
- [ ] DG-02: 21개 SKILL.md + 3개 agent.md frontmatter YAML 모두 parse 가능
