---
feature: "react-kit G1 Scaffolding & Generation Skills Design Spec"
created: "2026-04-10 15:30"
complexity: "중간"
conditions: 13
scope: "docs/react/kit-design/g1-scaffolding.md — /react-init, /react-screen, /react-feature, /react-widget 스킬 4종의 상세 설계"
---

## Skill
- [ ] SK-01: 파일 docs/react/kit-design/g1-scaffolding.md 가 존재하고 본문 350줄 이상이다
- [ ] SK-02: /react-init 섹션에 (트리거, 입력, 산출 파일 트리, 생성 명령 순서, Gotchas) 5개 하위 항목이 모두 존재한다
- [ ] SK-03: /react-screen 섹션에 TanStack Router 파일 기반 라우트 등록 절차와 lazy load 패턴이 포함된다
- [ ] SK-04: /react-feature 섹션에 "화면 + 스토어 + UseCase + API" 4계층 생성 순서가 의존성 그래프와 함께 명시된다
- [ ] SK-05: /react-widget 섹션에 shadcn/ui 기반 variant 패턴 (cva 또는 동등) 과 Props 타이핑 규칙이 포함된다

## Script
- [ ] SC-01: Vite, Tauri, Tailwind, shadcn/ui, TanStack Router 설치 명령이 현재 (2026-04) 공식 문서 기준으로 명시된다 (deprecated 명령 0건)
- [ ] SC-02: 문서 내 모든 라이브러리 참조에 current version 범위 또는 "2+", "v5+" 같은 메이저 범위 표기가 있고 특정 패치 버전 하드코딩이 없다
- [ ] SC-03: 외부 공식 문서 URL 인용이 최소 6개 이상 포함된다 (Vite, Tauri, Tailwind, shadcn/ui, TanStack Router, Lingui/pnpm 중 택)

## Error
- [ ] ER-01: 각 스킬의 "생성 실패 시 롤백 / 중복 감지" 규칙이 명시된다 (예: 이미 파일 존재 시 overwrite 금지)
- [ ] ER-02: strict TypeScript 위반 생성 코드에 대한 거부 규칙이 각 스킬 Gotchas에 포함된다

## Architecture
- [ ] AR-01: 4개 스킬의 생성 결과물이 모두 Clean Architecture 레이어 (domain/data/presentation/infrastructure) 중 어느 위치에 배치되는지 명시된다
- [ ] AR-02: pnpm workspace + Cargo workspace 모노레포 레이아웃 초기 구조가 `/react-init` 섹션에 ASCII 트리로 첨부된다

## Anti-patterns
- [ ] AP-01: 특정 패치 버전 하드코딩 없음

## Reusability
- [ ] RE-01: 4개 스킬 간에 공유되는 project-detection 레퍼런스 문서 경로를 명시한다 (flutter-toolkit의 project-detection.md 패턴 모방)
- [ ] RE-02: 다른 그룹 (G2~G6) 에서 재사용할 수 있는 scaffold 헬퍼가 있으면 그 위치와 형태를 언급한다

## Diagnostics
- [ ] DG-01: N/A (마크다운)
- [ ] DG-02: N/A (IDE diagnostics 대상 아님)
- [ ] DG-03: 문서 내 placeholder (TODO, TBD, FIXME) 0건
- [ ] DG-04: 모든 외부 URL이 http(s):// 형식
