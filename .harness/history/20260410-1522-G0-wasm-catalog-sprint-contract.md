---
feature: "react-kit WASM Decision Catalog (docs/react/wasm-catalog.md)"
created: "2026-04-10 15:02"
complexity: "중간"
conditions: 14
---

## Skill
- [ ] SK-01: 파일 docs/react/wasm-catalog.md가 존재하고 본문이 400줄 이상이다
- [ ] SK-02: "WASM 권장 카테고리" 테이블이 최소 8개 항목을 포함하며 각 항목에 (카테고리, 근거, 프로덕션 사례, 출처 URL) 4개 필드가 모두 채워져 있다
- [ ] SK-03: "WASM 비권장 카테고리" 테이블이 최소 8개 항목을 포함하며 각 항목에 (카테고리, 이유, 출처) 3개 필드가 모두 채워져 있다
- [ ] SK-04: "Boundary cost" 섹션에 JS↔WASM 호출 오버헤드, 문자열 마샬링 비용, ArrayBuffer 전송 비용이 각각 수치와 단위로 명시된다

## Script
- [ ] SC-01: 본문 내 모든 인용에 실제 URL이 첨부된다 (placeholder URL/fake citation 0건)
- [ ] SC-02: "참고자료" 섹션에 최소 5개의 primary source (V8/Chromium 블로그, MDN, 학술 논문, 프로덕션 엔지니어링 포스트) 가 리스트된다
- [ ] SC-03: 측정 수치에 출처가 없거나 재확인 불가능한 주장은 "unverified" 또는 "추정" 마크가 붙는다

## Error
- [ ] ER-01: "카탈로그 미스 시 판정" 섹션이 존재하며 데이터 크기 / 호출 빈도 / 반복 루프 / 외부 접근 / SIMD 활용성 5개 휴리스틱이 모두 명시된다
- [ ] ER-02: "흔한 오해" 섹션이 WASM이 이길 것 같지만 실제로는 지는 케이스를 최소 3개 구체적으로 다룬다

## Architecture
- [ ] AR-01: 파일 경로가 docs/react/wasm-catalog.md 이며 기존 docs/rust/ docs/flutter/ 레이아웃 패턴과 일관된다
- [ ] AR-02: 문서 최상단에 last_updated 날짜 (YYYY-MM-DD) 와 리서치 소스 요약이 포함된다

## Anti-patterns
- [ ] AP-01: Tauri/브라우저 버전을 특정 패치 버전까지 하드코딩해서 결정 기준으로 못박지 않는다 (Tauri 2+ OK, Tauri 2.10.3에서만 유효 같은 표현 금지)

## Reusability
- [ ] RE-01: 다른 docs/*/ 리서치 문서와 중복되지 않고 react-kit 고유의 WASM 결정 관점만 다룬다
- [ ] RE-02: 이미 docs/rust/ 에 같은 주제 문서가 있으면 그쪽을 참조·확장하는 형태로 작성한다

## Diagnostics
- [ ] DG-01: N/A (마크다운 문서, 쉘 린트 대상 아님)
- [ ] DG-02: N/A (IDE diagnostics 대상 아님)
- [ ] DG-03: 문서 내 placeholder 텍스트 (TODO TBD FIXME 빈 - 행) 0건
- [ ] DG-04: 본문에 포함된 모든 URL이 표면상 유효한 형식 (http(s):// 형태, 공백/깨진 링크 없음)
