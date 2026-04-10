---
feature: "react-kit G2 State & Data Skills Design Spec"
created: "2026-04-10 16:55"
complexity: "중간"
conditions: 14
scope: "docs/react/kit-design/g2-state-data.md — /react-store, /react-api, /react-query, /react-form 스킬 4종의 상세 설계"
---

## Skill
- [ ] SK-01: 파일 docs/react/kit-design/g2-state-data.md 가 존재하고 본문 400줄 이상이다
- [ ] SK-02: /react-store 섹션에 Zustand 스토어 정의 패턴 + selector hook + React 외부 접근 (WASM 콜백용) 예시가 포함된다
- [ ] SK-03: /react-api 섹션에 Clean Architecture 4계층 (datasource → model → repository → usecase) 생성 순서와 각 계층의 파일 위치·역할이 명시된다
- [ ] SK-04: /react-query 섹션에 TanStack Query v5 useQuery/useMutation 패턴 + queryKey 네이밍 규칙 + cache invalidation 전략이 포함된다
- [ ] SK-05: /react-form 섹션에 React Hook Form + Zod resolver 통합 패턴 + form 에러 표시 + Result 타입 반환 규칙이 포함된다

## Script
- [ ] SC-01: Zustand, TanStack Query, React Hook Form, Zod, neverthrow 설치 명령이 2026-04 기준 공식 문서에 부합한다 (deprecated API 0건)
- [ ] SC-02: 문서 내 모든 라이브러리 참조에 메이저 범위 표기 (v5+, v4+ 등) 가 사용되고 특정 패치 버전 하드코딩 없음
- [ ] SC-03: 외부 공식 문서 URL 인용이 최소 5개 이상 포함된다 (Zustand, TanStack Query, RHF, Zod, neverthrow 중 택)

## Error
- [ ] ER-01: 각 스킬이 에러 경계에서 Result 타입 또는 Failure 반환 규칙을 명시한다 (throw 금지)
- [ ] ER-02: Zod parse 실패 시 처리 흐름 (어느 레이어에서 검증, 실패 시 어떤 Failure 로 변환) 이 /react-api 또는 /react-form 섹션에 명시된다

## Architecture
- [ ] AR-01: 4개 스킬의 산출물이 Clean Architecture 레이어 (domain/data/presentation/infrastructure) 중 어디에 배치되는지 각각 명시된다
- [ ] AR-02: "Zustand는 외부 상태, TanStack Query는 서버 상태" 분리 원칙이 명시되고 두 상태가 교차하는 지점 (예: mutation 성공 후 store 업데이트) 의 처리 패턴이 포함된다

## Anti-patterns
- [ ] AP-01: 특정 패치 버전 하드코딩 없음

## Reusability
- [ ] RE-01: G1 에서 정의한 project-detection 및 Clean Arch 레이아웃 규칙을 재사용함을 명시한다
- [ ] RE-02: G2 의 스킬들이 G1 /react-feature 가 생성한 skeleton 위에서 동작한다는 관계를 명시한다

## Diagnostics
- [ ] DG-01: N/A (마크다운)
- [ ] DG-02: N/A (IDE diagnostics 대상 아님)
- [ ] DG-03: 문서 내 placeholder (TODO, TBD, FIXME) 0건
- [ ] DG-04: 모든 외부 URL이 http(s):// 형식
