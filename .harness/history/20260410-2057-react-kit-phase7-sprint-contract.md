---
feature: "react-kit Phase 7: G5b /react-animation 스킬 + animation-architect-react 에이전트"
created: "2026-04-10T20:45:00+09:00"
complexity: "복잡"
conditions: 17
scope: "react-kit/skills/react-animation/SKILL.md + react-kit/agents/animation-architect-react.md. 소스: docs/react/kit-design/g5b-animation.md (980+ lines). **핵심 원칙: 라이브러리 0개 (Motion/dnd-kit/react-spring 절대 금지)**"
---

## Skill
- [ ] SK-01: `react-kit/skills/react-animation/SKILL.md` 존재. frontmatter 유효 + name=react-animation, user-invocable=true, argument-hint 명시
- [ ] SK-02: description 에 트리거 키워드 3개 이상 (한국어/영어) + "라이브러리 0개" 원칙 언급
- [ ] SK-03: Gotchas 섹션에 각 Tier 의 주요 실수 방지 규칙 (§1.5 / §2.7 / §3.x) 반영
- [ ] SK-04: Process 섹션에 3-Tier 구조 (Tier 1 Tailwind+CSS / Tier 2 View Transitions / Tier 3 Pointer Primitives) 명시
- [ ] SK-05: 자동 티어 판정 로직 (g5b §6) 반영 — 사용자 요청을 분석해 적절한 Tier 선택

## Agent
- [ ] AG-01: `react-kit/agents/animation-architect-react.md` 존재. frontmatter 에 name=animation-architect-react, description (트리거), tools (Read, Grep, Glob), model 명시
- [ ] AG-02: 에이전트 본문이 §8.1 역할 / §8.2 트리거 조건 / §8.4 출력 포맷 반영 (자문 요약, 권장 전략, 구현 단계, 엣지케이스, 접근성 이슈)
- [ ] AG-03: 에이전트가 읽기 전용 (코드 수정 없음) 임을 명시

## Script
- [ ] SC-01: SKILL.md + agent.md frontmatter YAML parse 가능
- [ ] SC-02: `python3 scripts/sync-docs.py --check-only react-kit` 실행 시 AUTO:skills 17개 + AUTO:agents 2개 포함

## Architecture
- [ ] AR-01: 스킬이 3-Tier 구조 전체를 커버 (Tier 1 Tailwind, Tier 2 View Transitions, Tier 3 Pointer Primitives)
- [ ] AR-02: Tier 3 Pointer Primitives 훅들 (useDrag/useDrop/useSortable) 의 파일 위치 명시 (`src/presentation/shared/hooks/`) + Zustand drag state 는 `src/presentation/shared/stores/drag-store.ts`

## Anti-patterns (빌드 게이트급)
- [ ] AP-01: **Motion/framer-motion 금지** 명시 — Gotchas 또는 Rules 섹션
- [ ] AP-02: **dnd-kit 금지** 명시
- [ ] AP-03: **react-spring / react-transition-group 금지** 명시
- [ ] AP-04: Pointer cancel 처리 (§3.4) 필수 규칙 명시 — 포인터 이벤트 cancel 누락 시 상태 leak

## Accessibility
- [ ] AX-01: 접근성 경고 (§5) 반영 — `prefers-reduced-motion` 미디어 쿼리 존중, 키보드 네비게이션 fallback, ARIA live regions 명시

## Reusability
- [ ] RE-01: SKILL.md + agent.md 구조 기존 react-kit/flutter-toolkit 스킬과 일관
- [ ] RE-02: 트리거 키워드가 기존 16 스킬 + 1 에이전트와 겹치지 않음

## Diagnostics
- [ ] DG-01: 파일 내 TODO/TBD/FIXME 0건
- [ ] DG-02: 모든 fenced code block 에 언어 힌트
