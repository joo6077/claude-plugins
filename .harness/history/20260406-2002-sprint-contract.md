---
feature: "docs-site backend-kit/infra-kit 페이지 재생성"
created: "2026-04-04 20:30"
complexity: "중간"
conditions: 19
---

## Skill
- [ ] SK-01: 각 HTML 페이지가 standalone이다 (외부 CSS/JS/font CDN 참조 0개)
- [ ] SK-02: 각 페이지에 hero 섹션(badge + h1 gradient + subtitle)이 존재한다
- [ ] SK-03: 각 페이지에 원칙 카드 섹션이 존재하며, 모든 원칙에 출처 URL이 포함된다
- [ ] SK-04: 각 페이지에 수치 기준 테이블이 존재하며, 구체적 수치(타임아웃, 임계값, 비율)가 명시된다
- [ ] SK-05: 각 페이지에 안티패턴 비교 패널(bad/good)이 최소 1개 존재한다
- [ ] SK-06: 각 페이지에 Gotchas 체크리스트가 존재한다

## Script
- [ ] SC-01: docs/index.html의 categories 배열에 Backend Kit 카테고리가 존재하며 4개 페이지가 등록되어 있다
- [ ] SC-02: docs/index.html의 categories 배열에 Infra Kit 카테고리가 존재하며 4개 페이지가 등록되어 있다
- [ ] SC-03: getIcon() 함수에 8개 페이지 id에 대한 SVG 아이콘이 모두 등록되어 있다

## Error
- [ ] ER-01: prefers-reduced-motion 미디어 쿼리가 모든 페이지에 존재한다

## Architecture
- [ ] AR-01: backend-kit 페이지 accent는 #A78BFA이고, infra-kit 페이지 accent는 #34D399이다
- [ ] AR-02: 각 페이지가 최소 400줄 이상이다
- [ ] AR-03: 페이지 파일 경로가 docs/backend-kit/*.html, docs/infra-kit/*.html 패턴을 따른다
- [ ] AR-04: 연속 3개 이상 섹션이 동일한 레이아웃 구조를 반복하지 않는다

## Anti-patterns
- [ ] AP-01: 버전을 하드코딩하지 않는다
- [ ] AP-02: force push 금지

## Reusability
- [ ] RE-01: 다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다

## Diagnostics
- [ ] DG-01: bash -n scripts/release.sh 워닝 0개
- [ ] DG-02: IDE diagnostics 워닝/인포 0개
- [ ] DG-03: 콘솔 로그에 에러/예외 0개
- [ ] DG-04: 실제 앱/서버 구동 시 에러 0개
