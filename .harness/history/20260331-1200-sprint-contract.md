---
feature: "visuals 폴더 CSS/구조 통일"
created: "2026-03-31 12:00"
complexity: "복잡"
conditions: 15
---

## Architecture
- [ ] AR-01: 19개 콘텐츠 HTML 파일 모두 동일한 CSS 기본 토큰 체계(--bg, --surface, --border, --text, --radius)를 사용한다 (페이지별 accent 컬러 변형은 허용)
- [ ] AR-02: 패턴A 4개 파일(typography-scale, color-palette, spacing-system, accessibility)에서 page-nav 요소와 관련 CSS가 제거되었다
- [ ] AR-03: 패턴C 3개 파일(ethical-design, image-illustration, information-density)의 CSS 변수가 공백 없는 압축 포맷(--border:#2a2e45)으로 통일되었다
- [ ] AR-04: 19개 파일 모두 동일한 래퍼 클래스(page)를 사용한다 (page-wrap, container 미사용)
- [ ] AR-05: index.html의 카테고리 목록과 실제 HTML 파일이 1:1 대응한다 (누락/미등록 없음)

## Error
- [ ] ER-01: page-nav 제거 후 콘텐츠 상단이 가려지지 않는다 (hero/첫 섹션의 padding-top이 iframe 내 적절한 값으로 조정됨)
- [ ] ER-02: 패턴C 파일의 래퍼 변경(container → page) 후 레이아웃이 깨지지 않는다 (max-width, padding 유지)

## Anti-patterns
- [ ] AP-01: 하드코딩된 버전 없음
- [ ] AP-02: force push 사용 안 함

## Reusability
- [ ] RE-01: 다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다

## Diagnostics
- [ ] DG-01: bash -n scripts/release.sh 워닝 0개 (변경/생성 파일 대상)
- [ ] DG-02: IDE diagnostics 워닝/인포 0개
- [ ] DG-03: 콘솔 로그에 에러/예외 0개
- [ ] DG-04: 실제 앱/서버 구동 시 에러 0개
