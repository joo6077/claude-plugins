---
feature: "react-kit G3 Performance Layer Skills Design Spec"
created: "2026-04-10 17:10"
complexity: "중간"
conditions: 15
scope: "docs/react/kit-design/g3-performance.md — /react-wasm, /react-tauri 스킬 2종의 상세 설계"
---

## Skill
- [ ] SK-01: 파일 docs/react/kit-design/g3-performance.md 가 존재하고 본문 400줄 이상이다
- [ ] SK-02: /react-wasm 섹션이 docs/react/wasm-catalog.md 의 판정 흐름을 참조하여 자동 판정 로직을 명시하고, 카테고리 매칭 + 휴리스틱 fallback 5개를 모두 포함한다
- [ ] SK-03: /react-wasm 섹션에 Rust 함수 → wasm-pack 빌드 → Web Worker 래핑 → Clean Arch 배치의 end-to-end 파이프라인이 코드 예시와 함께 명시된다
- [ ] SK-04: /react-tauri 섹션에 Tauri command 정의 (Rust 측) + invoke 호출 (TS 측) + capabilities 권한 선언의 전체 흐름이 포함된다
- [ ] SK-05: /react-tauri 섹션에 feature detection gating 패턴 (Tauri 환경 / 브라우저 환경 분기) 이 코드 예시와 함께 명시된다
- [ ] SK-06: /react-wasm 과 /react-tauri 의 경계 (언제 WASM, 언제 Tauri command 사용) 가 결정 규칙으로 명시된다

## Script
- [ ] SC-01: wasm-pack, wasm-bindgen, tauri, @tauri-apps/api, Comlink 사용 코드가 2026-04 공식 문서에 부합한다 (deprecated API 0건)
- [ ] SC-02: 모든 라이브러리 참조에 메이저 범위 표기 사용, 특정 패치 버전 하드코딩 없음
- [ ] SC-03: 외부 공식 문서 URL 인용이 최소 6개 이상 포함된다 (wasm-bindgen, Tauri 2, Comlink, wasm-pack 등)

## Error
- [ ] ER-01: /react-wasm 에서 Rust panic 발생 시 JS 측에서 Result 로 변환되는 경로가 명시된다
- [ ] ER-02: /react-tauri 에서 Tauri API 호출 실패 시 Failure 변환 경로가 명시된다 (브라우저 환경에서 Tauri 없음도 포함)

## Architecture
- [ ] AR-01: /react-wasm 산출물이 Clean Arch 어느 레이어에 배치되는지 명시되고 (data/datasources/wasm/), domain/entities 는 WASM 을 모르는 불변 원칙이 기술된다
- [ ] AR-02: /react-tauri 산출물이 infrastructure/tauri/ 에 래핑되고 domain/data 레이어가 Tauri 를 직접 참조하지 않는 규칙이 명시된다
- [ ] AR-03: 웹 배포 / Tauri 데스크탑 배포 양쪽에서 동일한 React 코드가 동작해야 함을 명시하고, 분기 전략이 기술된다

## Anti-patterns
- [ ] AP-01: 특정 패치 버전 하드코딩 없음

## Reusability
- [ ] RE-01: G0 docs/react/wasm-catalog.md 를 /react-wasm 판정의 소스로 사용함을 명시한다
- [ ] RE-02: G1 /react-init 이 세팅한 crates/core/ 및 src-tauri/ 디렉토리를 전제로 함을 명시한다

## Diagnostics
- [ ] DG-01: N/A (마크다운)
- [ ] DG-02: N/A (IDE diagnostics 대상 아님)
- [ ] DG-03: 문서 내 placeholder (TODO, TBD, FIXME) 0건
- [ ] DG-04: 모든 외부 URL이 http(s):// 형식
