---
feature: "react-kit G6 Build & Audit Skills Design Spec"
created: "2026-04-10 18:45"
complexity: "중간"
conditions: 16
scope: "docs/react/kit-design/g6-build-audit.md — /react-run, /react-build, /react-preflight, /react-audit 스킬 4종 + react-reviewer 에이전트 + widget-inspector-react 에이전트 상세 설계"
---

## Skill
- [ ] SK-01: 파일 docs/react/kit-design/g6-build-audit.md 가 존재하고 본문 450줄 이상이다
- [ ] SK-02: /react-run 섹션에 개별 빌드 프리미티브 (dev, build, lint, test, wasm-build, format, codegen) 의 실행 명령과 감지 로직이 명시된다
- [ ] SK-03: /react-build 섹션에 vite build + tsc --noEmit + wasm-pack build 순서와 각 단계 실패 시 처리가 명시된다
- [ ] SK-04: /react-preflight 섹션에 pre-commit quality gate 순서 (fix → codegen → lint → tsc → test → wasm-build → vite-build) 와 각 단계 실패 시 롤백 규칙이 명시된다
- [ ] SK-05: /react-audit 섹션에 quick 모드와 deep 모드 (최대 4 에이전트 병렬) 구분이 명시되고, 변경 파일 수에 따른 자동 모드 선택 규칙이 포함된다
- [ ] SK-06: /react-audit 의 감사 체크리스트가 카테고리별로 명시된다 (Architecture / Strict TS / Performance / Accessibility / Anti-patterns / Library Policy)

## Agent
- [ ] AG-01: react-reviewer 에이전트가 정의된다 — 역할 (읽기 전용 독립 평가), 트리거 (/react-audit 에서 Agent 도구로 호출), 입력 (변경 파일 목록 + 카테고리), 출력 (PASS/FAIL 판정 + 근거)
- [ ] AG-02: react-reviewer 의 도구 스코프 (Read, Grep, Glob — 쓰기 없음) 가 명시된다
- [ ] AG-03: widget-inspector-react 에이전트가 G5 에서 정의된 것을 G6 /react-audit 의 deep 모드에서 병렬 실행되는 축으로 재사용함이 명시된다

## Script
- [ ] SC-01: vite, tsc, eslint, vitest, playwright, wasm-pack, pnpm 사용 명령이 2026-04 공식 문서에 부합한다
- [ ] SC-02: 메이저 범위 표기만, 패치 버전 하드코딩 없음
- [ ] SC-03: 외부 공식 문서 URL 인용이 최소 5개 이상 포함된다

## Error
- [ ] ER-01: /react-preflight 의 각 단계 실패 시 전체 파이프라인 중단 + 원인 파일 리스트 출력 규칙이 명시된다
- [ ] ER-02: /react-audit 가 검출해야 할 안티패턴 목록이 카테고리별로 정리되고, 각 안티패턴의 grep 패턴 또는 AST 검사 기준이 포함된다 (G0~G5b 모든 그룹의 안티패턴 통합)

## Architecture
- [ ] AR-01: 4개 스킬의 실행 위치 (npm scripts vs 직접 명령) 와 명령 경로가 명시된다
- [ ] AR-02: /react-audit 의 deep 모드가 병렬 실행할 4개 에이전트 축 (예: architecture / performance / accessibility / library-policy) 이 명시된다

## Anti-patterns
- [ ] AP-01: 특정 패치 버전 하드코딩 없음

## Reusability
- [ ] RE-01: G1 project-detection 을 모든 /react-run 서브커맨드가 재사용함이 명시된다
- [ ] RE-02: /react-audit 가 G0 wasm-catalog + G5b banned libraries 를 감사 기준으로 사용함이 명시된다

## Diagnostics
- [ ] DG-01: N/A (마크다운)
- [ ] DG-02: N/A (IDE diagnostics 대상 아님)
- [ ] DG-03: 문서 내 placeholder (TODO, TBD, FIXME) 0건
- [ ] DG-04: 모든 외부 URL이 http(s):// 형식
