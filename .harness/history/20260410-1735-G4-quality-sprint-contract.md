---
feature: "react-kit G4 Quality & Patterns Skills Design Spec"
created: "2026-04-10 17:25"
complexity: "중간"
conditions: 14
scope: "docs/react/kit-design/g4-quality.md — /react-test, /react-error, /react-l10n 스킬 3종의 상세 설계"
---

## Skill
- [ ] SK-01: 파일 docs/react/kit-design/g4-quality.md 가 존재하고 본문 400줄 이상이다
- [ ] SK-02: /react-test 섹션에 Vitest unit, Testing Library component, Playwright e2e 3종 테스트 유형별 생성 패턴이 각각 코드 예시와 함께 명시된다
- [ ] SK-03: /react-test 섹션에 Clean Architecture 레이어별 테스트 전략 (domain 순수 함수, data repository, presentation hook/component) 이 명시된다
- [ ] SK-04: /react-error 섹션에 경계에서 예외 → Failure 변환 → Error Boundary + UI 표시 흐름이 코드 예시와 함께 명시된다
- [ ] SK-05: /react-error 섹션에 Severity 매핑 (info/warning/error/fatal) 과 사용자 표시 (snackbar/dialog/page) 매핑이 명시된다
- [ ] SK-06: /react-l10n 섹션에 Lingui 매크로 기반 번역 문자열 추가 + codegen 재생성 + locale 전환 흐름이 명시된다

## Script
- [ ] SC-01: Vitest, @testing-library/react, Playwright, @lingui/macro, @lingui/react 사용 코드가 2026-04 공식 문서에 부합한다 (deprecated API 0건)
- [ ] SC-02: 모든 라이브러리 참조에 메이저 범위 표기, 패치 버전 하드코딩 없음
- [ ] SC-03: 외부 공식 문서 URL 인용이 최소 6개 이상 포함된다 (Vitest, Testing Library, Playwright, Lingui, neverthrow 중 택)

## Error
- [ ] ER-01: /react-error 에서 throw 하는 코드가 Failure 로 변환되는 경로가 레이어별로 명시된다 (data boundary → domain Failure → presentation Error Boundary)
- [ ] ER-02: 테스트 코드에서 에러 경로를 검증하는 패턴이 /react-test 섹션에 포함된다 (예: Result.isErr() 체크, Error Boundary 트리거)

## Architecture
- [ ] AR-01: 3개 스킬의 산출물이 Clean Architecture 레이어 중 어디에 배치되는지 각각 명시된다
- [ ] AR-02: i18n 번역 키 정의 위치 (domain vs presentation), locale 파일 위치, codegen 산출물 위치가 /react-l10n 섹션에 명시된다

## Anti-patterns
- [ ] AP-01: 특정 패치 버전 하드코딩 없음

## Reusability
- [ ] RE-01: G1 project-detection + G2 데이터 레이어 패턴 재사용 명시
- [ ] RE-02: G4 의 테스트 스킬이 G1~G3 산출물을 대상으로 동작한다는 관계 명시

## Diagnostics
- [ ] DG-01: N/A (마크다운)
- [ ] DG-02: N/A (IDE diagnostics 대상 아님)
- [ ] DG-03: 문서 내 placeholder (TODO, TBD, FIXME) 0건
- [ ] DG-04: 모든 외부 URL이 http(s):// 형식
