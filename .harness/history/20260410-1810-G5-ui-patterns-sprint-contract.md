---
feature: "react-kit G5 UI Patterns Skills Design Spec"
created: "2026-04-10 17:40"
complexity: "중간"
conditions: 13
scope: "docs/react/kit-design/g5-ui-patterns.md — /react-responsive, /react-skeleton, /react-extract 스킬 3종의 상세 설계. /react-animation 은 별도 문서 g5b-animation.md."
---

## Skill
- [ ] SK-01: 파일 docs/react/kit-design/g5-ui-patterns.md 가 존재하고 본문 350줄 이상이다
- [ ] SK-02: /react-responsive 섹션에 Tailwind v4 breakpoint 체계 (sm/md/lg/xl/2xl) + container queries (@container) 사용 지침이 코드 예시와 함께 명시된다
- [ ] SK-03: /react-responsive 섹션에 "페이지 크기 기반" vs "컨테이너 크기 기반" 결정 규칙이 포함된다
- [ ] SK-04: /react-skeleton 섹션에 shadcn Skeleton 컴포넌트 기반 shimmer 로딩 UI 생성 패턴 + TanStack Query isPending 연동 예시가 포함된다
- [ ] SK-05: /react-extract 섹션에 중복 위젯 감지 → 공용 컴포넌트 추출 → import 경로 자동 수정 흐름이 명시되고, widget-inspector 에이전트 연동 관계가 포함된다

## Script
- [ ] SC-01: Tailwind v4 container queries, shadcn Skeleton, TanStack Query isPending 사용이 2026-04 공식 문서에 부합한다
- [ ] SC-02: 패치 버전 하드코딩 없음
- [ ] SC-03: 외부 공식 문서 URL 인용이 최소 4개 이상 포함된다

## Error
- [ ] ER-01: /react-responsive 에서 breakpoint 미대응 시 fallback 규칙이 명시된다
- [ ] ER-02: /react-skeleton 에서 로딩 실패 (error state) 와 빈 상태 (empty state) 처리의 구분이 명시된다

## Architecture
- [ ] AR-01: 3개 스킬의 산출물이 presentation 레이어 (features/<feat>/components 또는 shared/components) 에 배치됨을 명시한다
- [ ] AR-02: /react-extract 의 추출 결과가 shared/components 로 이동할 때 원본 feature 의 import 경로가 자동 업데이트되는 규칙이 명시된다

## Anti-patterns
- [ ] AP-01: 특정 패치 버전 하드코딩 없음

## Reusability
- [ ] RE-01: G1 /react-widget 이 생성한 컴포넌트 구조 (cva, forwardRef) 를 기반으로 함을 명시한다
- [ ] RE-02: /react-extract 이 widget-inspector 에이전트 리포트와 연동됨을 명시한다

## Diagnostics
- [ ] DG-01: N/A (마크다운)
- [ ] DG-02: N/A (IDE diagnostics 대상 아님)
- [ ] DG-03: 문서 내 placeholder (TODO, TBD, FIXME) 0건
- [ ] DG-04: 모든 외부 URL이 http(s):// 형식
