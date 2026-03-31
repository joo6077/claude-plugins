---
feature: "Phase 4 — 기존 20페이지 Claude 컬러 마이그레이션 + 전체 28페이지 디자인 QA"
created: "2026-04-01 02:00"
complexity: "복잡"
conditions: 14
---

## Architecture
- [ ] AR-01: docs/design-kit/ 19페이지 + docs/process/ 1페이지 모두 Claude 공통 토큰(--bg:#0d0d14, --surface:#181825, --text:#F5F0E8)을 사용한다
- [ ] AR-02: docs/design-kit/ 19페이지의 --accent가 Design Kit 컬러(#E8965A)이다
- [ ] AR-03: docs/process/kaizen-flow.html의 --accent가 Process 컬러(#4ADE80)이다
- [ ] AR-04: 전체 28페이지(harness 6 + flutter 2 + design-kit 19 + process 1)에서 구 토큰(--bg:#0a0a0f, --surface:#151621, --border:#252840)이 0건이다

## Skill
- [ ] SK-01: 전체 28페이지의 line-height가 1.2~1.7 범위이다 (Typography). 단, display heading(h1~h2)은 tight heading 관행에 따라 1.1~1.2 허용. Bad/Good 비교 시연용 예시 요소도 의도적이므로 제외
- [ ] SK-02: 전체 28페이지의 본문 font-size가 최소 13px 이상이다 (Typography)
- [ ] SK-03: 전체 28페이지가 시맨틱 CSS 변수를 사용한다 — 본문/제목에 하드코딩 hex 컬러 미사용 (Color)
- [ ] SK-04: 전체 28페이지에서 연속 3회 이상 동일 레이아웃 구조 반복이 없다 (Authenticity). Grep으로 동일 CSS 클래스(grid-2, grid-3) 연속 사용 패턴을 확인한다

## Error
- [ ] ER-01: 구 토큰에서 신 토큰으로 마이그레이션 후 CSS 구문 오류가 없다

## Anti-patterns
- [ ] AP-01: 하드코딩된 버전 없음
- [ ] AP-02: force push 금지

## Reusability
- [ ] RE-01: 다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다

## Diagnostics
- [ ] DG-01: bash -n scripts/release.sh 워닝 0개
- [ ] DG-02: 정적 HTML 사이트이므로 미적용 (N/A)
- [ ] DG-03: 정적 HTML 사이트이므로 미적용 (N/A)
- [ ] DG-04: 정적 HTML 사이트이므로 미적용 (N/A)
