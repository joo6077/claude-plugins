# G4 오탐 대조 — 정상 액션으로서의 `삭제` 는 deprecation 주장이 아니다

- 대상: 웹 (Chrome)
- 조회일: 2026-09-10

## S1. 계정 설정 화면을 연다

- 어디서: `example.com/settings/account`
- 무엇을: 계정 (탭)
- 동작: 열기
- 값: 입력 없음
- 확인: 페이지에 `계정 삭제` 버튼이 보인다
- 안 보이면: 권한-역할 — 관리자에게 계정 관리 권한을 요청한다
- 출처: https://example.com/docs/account (조회 2026-09-10)

## S2. 계정을 삭제한다

- 어디서: `example.com/settings/account`
- 무엇을: 계정 삭제 (버튼)
- 동작: 누르기
- 값: 확인란에 `DELETE` 입력
- 확인: 로그인 화면으로 이동한다
- 안 보이면: 권한-역할 — 관리자에게 요청한다
- 출처: https://example.com/docs/account (조회 2026-09-10)
