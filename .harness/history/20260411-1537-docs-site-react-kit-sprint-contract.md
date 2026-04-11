---
feature: "docs-site: react-kit 9 HTML 페이지 + index.html 등록"
created: "2026-04-11T13:30:00+09:00"
complexity: "복잡"
conditions: 18
scope: "docs/react-kit/ 9개 HTML 페이지 생성 (g1~g6 + g5b + final-integration + wasm-catalog) + docs/index.html categories 배열 + getIcon 함수 업데이트. React Kit accent: #38BDF8 / #7DD3FC"
---

## Files (9 HTML 페이지)
- [ ] FL-01: `docs/react-kit/scaffolding.html` 생성 (소스: `docs/react/kit-design/g1-scaffolding.md`)
- [ ] FL-02: `docs/react-kit/state-data.html` 생성 (소스: `docs/react/kit-design/g2-state-data.md`)
- [ ] FL-03: `docs/react-kit/performance.html` 생성 (소스: `docs/react/kit-design/g3-performance.md`)
- [ ] FL-04: `docs/react-kit/quality.html` 생성 (소스: `docs/react/kit-design/g4-quality.md`)
- [ ] FL-05: `docs/react-kit/ui-patterns.html` 생성 (소스: `docs/react/kit-design/g5-ui-patterns.md`)
- [ ] FL-06: `docs/react-kit/animation.html` 생성 (소스: `docs/react/kit-design/g5b-animation.md`) — **라이브러리 0개 원칙 섹션 필수**
- [ ] FL-07: `docs/react-kit/build-audit.html` 생성 (소스: `docs/react/kit-design/g6-build-audit.md`)
- [ ] FL-08: `docs/react-kit/wasm-catalog.html` 생성 (소스: `docs/react/wasm-catalog.md`)
- [ ] FL-09: `docs/react-kit/integration.html` 생성 (소스: `docs/react/kit-design/final-integration.md`)

## Content Density
- [ ] CD-01: 각 HTML 페이지 최소 400 lines 이상 (docs-site 스킬 §8 원칙)
- [ ] CD-02: 각 페이지 필수 섹션 — hero (h1+gradient) / 원칙 카드 + 출처 URL / 수치 테이블 / 안티패턴 bad·good 비교 / Gotchas 체크리스트
- [ ] CD-03: 원칙 카드 하단에 `<a class="card-source" href="URL">출처명</a>` 링크 필수 (docs-site 스킬 §9)

## Design System
- [ ] DS-01: 모든 9 페이지가 `:root --accent: #38BDF8`, `--accent2: #7DD3FC` 사용 (css-tokens.md React Kit 매핑)
- [ ] DS-02: 모든 9 페이지의 body 배경 gradient 에 `rgba(56,189,248,0.06)` 사용
- [ ] DS-03: h1 gradient, .section-label 색상, .card:hover 보더가 React Kit accent 값 사용
- [ ] DS-04: 외부 CSS/JS/font CDN 0건 (standalone HTML, docs-site 스킬 §1)

## Index 등록
- [ ] IX-01: `docs/index.html` 의 `categories` 배열에 "React Kit — Vite + Tauri + WASM" (또는 적절한 label) 카테고리 추가. rust-kit 과 process 사이 위치
- [ ] IX-02: categories 에 9개 page 항목 (id, title 한국어, file) 추가
- [ ] IX-03: `getIcon()` 함수에 9개 page 의 SVG 아이콘 추가

## Library Policy (react-kit 특화)
- [ ] LP-01: `docs/react-kit/animation.html` 에 "라이브러리 0개 원칙" 섹션이 존재하고 Motion/framer-motion/dnd-kit/react-spring/react-transition-group 등 금지 라이브러리 목록 명시

## Accessibility
- [ ] AX-01: 9개 HTML 파일 모두 `prefers-reduced-motion` 미디어 쿼리 고려 또는 정적 페이지 (애니메이션 없음)
- [ ] AX-02: 본문 텍스트 대비 WCAG AA 4.5:1 이상 (design-kit audit-criteria.md 기준)

## Diagnostics
- [ ] DG-01: 각 HTML 파일 valid HTML 구문 (head/body/meta charset)
- [ ] DG-02: 모든 9 파일 및 index.html 변경분에 TODO/TBD/FIXME 0건
