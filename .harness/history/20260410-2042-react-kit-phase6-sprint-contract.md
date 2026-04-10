---
feature: "react-kit Phase 6: G5 UI Patterns Skills (3종) + widget-inspector-react 에이전트"
created: "2026-04-10T20:30:00+09:00"
complexity: "복잡"
conditions: 17
scope: "react-kit/skills/ 에 3개 G5 스킬 (/react-responsive, /react-skeleton, /react-extract) + react-kit/agents/ 에 widget-inspector-react 에이전트. 소스: docs/react/kit-design/g5-ui-patterns.md"
---

## Skill
- [ ] SK-01: `react-kit/skills/react-responsive/SKILL.md` 존재. frontmatter 유효 + name=react-responsive
- [ ] SK-02: `react-kit/skills/react-skeleton/SKILL.md` 존재. frontmatter 유효 + name=react-skeleton
- [ ] SK-03: `react-kit/skills/react-extract/SKILL.md` 존재. frontmatter 유효 + name=react-extract
- [ ] SK-04: 각 스킬 description 에 트리거 키워드 3개 이상
- [ ] SK-05: 각 스킬 Gotchas 가 g5-ui-patterns.md 의 §1.8 / §2.7 / §3.7 반영
- [ ] SK-06: 각 스킬 Process 가 g5-ui-patterns.md 의 §X.3~§X.7 반영

## Agent
- [ ] AG-01: `react-kit/agents/widget-inspector-react.md` 존재. frontmatter 에 name=widget-inspector-react, description (트리거 + "use proactively"), tools (Read, Grep, Glob), model=sonnet 명시
- [ ] AG-02: widget-inspector-react 의 본문이 flutter-toolkit 의 widget-inspector.md 와 유사한 구조 (모드 quick/deep, 감지 기준, 출력 형식)
- [ ] AG-03: `/react-extract` 스킬이 widget-inspector-react 에이전트와 연동한다는 설명 포함

## Script
- [ ] SC-01: 모든 SKILL.md + agent.md frontmatter YAML parse 가능
- [ ] SC-02: `python3 scripts/sync-docs.py --check-only react-kit` 실행 시 AUTO:skills 16개 + AUTO:agents 1개 포함

## Architecture
- [ ] AR-01: `/react-responsive` 가 "page-size (breakpoint) vs container-size (@container)" 결정 규칙 명시 (g5 §1.5 반영)
- [ ] AR-02: `/react-skeleton` 이 TanStack Query `isPending` 연동 패턴 명시 (g5 §2.4 반영)

## Anti-patterns
- [ ] AP-01: `/react-skeleton` 에 "CircularProgressIndicator / 스피너 사용 금지, 실제 레이아웃 매칭 skeleton" 규칙 명시
- [ ] AP-02: `/react-extract` 에 "TypeScript AST 기반 안전 변환, grep/regex 치환 금지" 규칙 명시 (g5 §3.6 반영)
- [ ] AP-03: `/react-responsive` 에 "breakpoint 하드코딩 금지, Tailwind 토큰 경유" 규칙 명시

## Reusability
- [ ] RE-01: SKILL.md 구조 기존 스킬과 일관 + agent 구조 flutter-toolkit widget-inspector 와 일관
- [ ] RE-02: Phase 2~6 총 16개 스킬 트리거 키워드 상호 배타적

## Diagnostics
- [ ] DG-01: SKILL.md + agent.md 파일 내 TODO/TBD/FIXME 0건
- [ ] DG-02: 모든 fenced code block 에 언어 힌트
