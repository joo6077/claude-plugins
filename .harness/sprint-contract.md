---
feature: "authentic-design visual 페이지 추가"
created: "2026-03-31 17:00"
complexity: "단순"
conditions: 6
---

## Architecture
- [ ] AR-01: docs/design/visuals/authentic-design.html이 존재하고 다른 visual 파일과 동일한 CSS 토큰 체계(--surface:#151621, --border:#252840, --radius:14px)를 사용한다
- [ ] AR-02: index.html의 카테고리 목록에 authentic-design 페이지가 등록되어 있다

## Error
- [ ] ER-01: index.html에서 authentic-design 페이지 클릭 시 iframe에 정상 로드된다 (파일명 일치)

## Anti-patterns
- [ ] AP-01: 하드코딩된 버전 없음
- [ ] AP-02: force push 금지

## Reusability
- [ ] RE-01: 다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다

## Diagnostics
- [ ] DG-01: bash -n scripts/release.sh 워닝 0개
- [ ] DG-02: IDE diagnostics 워닝/인포 0개
- [ ] DG-03: 콘솔 로그에 에러/예외 0개
- [ ] DG-04: 실제 앱/서버 구동 시 에러 0개
