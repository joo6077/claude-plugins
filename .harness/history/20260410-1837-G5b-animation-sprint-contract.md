---
feature: "react-kit G5b Animation (pure, no-library)"
created: "2026-04-10 18:15"
complexity: "중간"
conditions: 16
scope: "docs/react/kit-design/g5b-animation.md — /react-animation 스킬 + animation-architect-react 에이전트. 라이브러리 0개 원칙 (Tailwind + View Transitions + 커스텀 pointer primitives)"
principle: "NO THIRD-PARTY ANIMATION LIBRARY. Motion/framer-motion/dnd-kit/react-spring/auto-animate 금지. 순수 CSS + 네이티브 브라우저 API + 커스텀 hook 만 허용."
---

## Skill
- [ ] SK-01: 파일 docs/react/kit-design/g5b-animation.md 가 존재하고 본문 500줄 이상이다
- [ ] SK-02: 문서 최상단에 "라이브러리 0개 원칙" 이 명시되고 금지 라이브러리 목록 (Motion, framer-motion, react-spring, auto-animate, dnd-kit 등) 이 리스트된다
- [ ] SK-03: Tier 1 (Tailwind animate + transition + CSS keyframes) 섹션에 최소 3개 시나리오 (fade-in, slide-in, scale-on-hover) 의 코드 예시가 포함된다
- [ ] SK-04: Tier 2 (View Transitions API) 섹션에 (a) document.startViewTransition 사용법, (b) view-transition-name CSS 프로퍼티, (c) 그리드 ↔ 보드 뷰 전환 구체 예시, (d) Firefox fallback 전략이 포함된다
- [ ] SK-05: Tier 3 (커스텀 pointer primitives) 섹션에 useDrag / useDrop / useSortable 커스텀 훅의 구현 패턴이 pointer events (pointerdown/move/up/cancel) 기반으로 명시되고, FSM (idle/dragging/dropping) 상태 관리가 포함된다
- [ ] SK-06: 복잡 시나리오별 통합 예시 — (a) 그리드 ↔ 보드 뷰 전환, (b) 칸반 드래그앤드롭 (pointer event 기반), (c) SVG 화살표 연결선 (path 직접 계산) — 3개가 각각 코드 예시와 함께 명시된다
- [ ] SK-07: /react-animation 스킬의 자동 티어 판정 로직 (요청 분석 → Tier 1/2/3 선택) 이 명시된다
- [ ] SK-08: 키보드 접근성 / ARIA / screen reader 트레이드오프가 경고로 명시되고 사용자 구현 책임임이 기록된다

## Agent
- [ ] AG-01: animation-architect-react 에이전트 정의가 포함된다 — 역할 (설계 자문), 트리거 조건, 입력 (UI 인터랙션 설명 + 제약), 출력 (티어 권장 + 구현 전략 + 잠재 엣지케이스)
- [ ] AG-02: 에이전트의 tool 스코프 (Read, Grep, Glob — 쓰기 권한 없음, 읽기 전용 자문) 가 명시된다
- [ ] AG-03: 에이전트와 /react-animation 스킬의 연동 흐름 (에이전트 권장 → 사용자 승인 → 스킬이 구현) 이 명시된다

## Script
- [ ] SC-01: View Transitions API 사용 코드가 2026-04 MDN / Chrome Developers 공식 문서에 부합한다
- [ ] SC-02: pointer event 코드가 MDN 표준에 부합하고 touch-action CSS 속성 사용이 포함된다
- [ ] SC-03: 외부 공식 문서 URL 인용이 최소 5개 이상 포함된다 (MDN View Transitions, MDN Pointer Events, Tailwind, tailwindcss-animate 등)

## Error
- [ ] ER-01: Tier 2 의 Firefox / Safari 구버전 fallback 전략이 명시된다 (feature detection + graceful degradation)
- [ ] ER-02: Tier 3 의 pointer cancel 처리 (예: 드래그 중 브라우저 탭 전환, ESC 키) 가 명시된다

## Architecture
- [ ] AR-01: Tier 1/2/3 산출물의 Clean Architecture 레이어 배치가 명시된다 (CSS → styles/, 커스텀 훅 → presentation/shared/hooks/, 컴포넌트 → shared/components/)
- [ ] AR-02: 커스텀 훅이 React 트리 밖 상태를 관리할 때 (예: drag state 전역 store) Zustand 와의 연동 규칙이 명시된다

## Anti-patterns
- [ ] AP-01: 특정 라이브러리 패치 버전 언급 없음, 동시에 "외부 애니메이션 라이브러리 import" 코드 예시 0건

## Reusability
- [ ] RE-01: G1 /react-widget cva/forwardRef 컴포넌트 기반 동작 명시
- [ ] RE-02: G5 /react-responsive, /react-skeleton 과의 상호작용 (반응형 breakpoint 에 따른 애니메이션 분기, 로딩→완료 전환 애니메이션) 이 명시된다

## Diagnostics
- [ ] DG-01: N/A (마크다운)
- [ ] DG-02: N/A (IDE diagnostics 대상 아님)
- [ ] DG-03: 문서 내 placeholder (TODO, TBD, FIXME) 0건
- [ ] DG-04: 모든 외부 URL이 http(s):// 형식
