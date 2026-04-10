---
feature: "react-kit Phase 8: G6 Build & Audit Skills (4종) + react-reviewer 에이전트"
created: "2026-04-10T21:00:00+09:00"
complexity: "복잡"
conditions: 19
scope: "react-kit/skills/ 에 4개 G6 스킬 (/react-run, /react-build, /react-preflight, /react-audit) + react-kit/agents/react-reviewer.md. 소스: docs/react/kit-design/g6-build-audit.md"
---

## Skill
- [ ] SK-01: `react-kit/skills/react-run/SKILL.md` 존재 + frontmatter 유효 + name=react-run
- [ ] SK-02: `react-kit/skills/react-build/SKILL.md` 존재 + frontmatter 유효 + name=react-build
- [ ] SK-03: `react-kit/skills/react-preflight/SKILL.md` 존재 + frontmatter 유효 + name=react-preflight
- [ ] SK-04: `react-kit/skills/react-audit/SKILL.md` 존재 + frontmatter 유효 + name=react-audit
- [ ] SK-05: 각 스킬 description 에 트리거 키워드 3+ (기존 17개 스킬과 겹치지 않음)
- [ ] SK-06: 각 스킬의 Gotchas 섹션이 g6-build-audit.md 의 §X.4 (run) / §2.6 (build) / §3.5 (preflight) / §4.7 (audit) 반영
- [ ] SK-07: 각 스킬의 Process 섹션이 g6-build-audit.md 의 §X.2~§X.6 반영

## Audit 특별 요구사항
- [ ] AU-01: `/react-audit` 이 quick/deep 두 모드 지원 + 파일 수 기반 자동 선택 규칙 명시
- [ ] AU-02: `/react-audit` Deep 모드가 **4개 에이전트 병렬 축** (g6 §4.4) 을 명시
- [ ] AU-03: `/react-audit` 이 **6개 카테고리 감사 체크리스트** 를 모두 커버 — Architecture / Strict TypeScript / Performance / Accessibility / Anti-patterns / **Library Policy (빌드 게이트급)**

## Agent
- [ ] AG-01: `react-kit/agents/react-reviewer.md` 존재. frontmatter (name=react-reviewer, description, tools, model) 유효
- [ ] AG-02: 에이전트 본문이 §5.1 react-reviewer 역할 + 읽기 전용 선언 포함

## Script
- [ ] SC-01: 5개 파일 frontmatter YAML parse 가능
- [ ] SC-02: `python3 scripts/sync-docs.py --check-only react-kit` 실행 시 AUTO:skills 21개 + AUTO:agents 3개 포함

## Architecture
- [ ] AR-01: `/react-build` 가 wasm-pack → tsc → vite 순서 명시 (g6 §2.2)
- [ ] AR-02: `/react-preflight` 가 fix → codegen → lint → tsc → test → wasm-build → vite-build 순서 명시 (g6 §3.2)

## Anti-patterns (Library Policy)
- [ ] AP-01: `/react-audit` Library Policy 카테고리가 애니메이션 라이브러리 (Motion/dnd-kit/react-spring/react-transition-group 등) 사용을 **빌드 실패 레벨** 로 검출
- [ ] AP-02: `/react-preflight` 가 실패 시 롤백 규칙 명시

## Reusability
- [ ] RE-01: SKILL.md + agent.md 구조 기존과 일관
- [ ] RE-02: Phase 2~8 총 21개 스킬 + 3개 에이전트 트리거 키워드 상호 배타적

## Diagnostics
- [ ] DG-01: 5개 파일 TODO/TBD/FIXME 0건
- [ ] DG-02: 모든 fenced code block 언어 힌트
