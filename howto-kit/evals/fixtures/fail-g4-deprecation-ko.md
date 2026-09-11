# G4 양성 케이스 — 한국어 deprecation 주장에 근거 없음

기존 킷의 G4 는 영문 토큰 `[Dd]eprecat` 에만 묶여 있어 한국어 1 차 출처를 근거로 인정하지
못했고, 반대로 한국어로 한 근거 없는 주장도 잡지 못했다. 이 문서는 후자다.

- 대상: iOS

## S1. 인증서 방식 대신 인증키 방식을 쓴다

- 어디서: `developer.apple.com/account/resources/authkeys/list`
- 무엇을: Keys (메뉴)
- 동작: 열기
- 값: 입력 없음
- 확인: 키 목록 페이지가 열린다
- 안 보이면: 권한 — Account Holder 또는 Admin 역할이 필요하다
- 출처: https://developer.apple.com/help/account/ (조회 2026-09-08)

## S2. `.p12` 인증서 방식은 지원 종료되었으므로 쓰지 않는다

- 어디서: `developer.apple.com/account/resources/certificates/list`
- 무엇을: Certificates (메뉴)
- 동작: 선택
- 값: 입력 없음
- 확인: 기존 인증서 목록이 보인다
- 안 보이면: 요금제 — 무료 계정에는 배포용 인증서 항목이 없다
- 출처: https://developer.apple.com/help/account/ (조회 2026-09-08)
