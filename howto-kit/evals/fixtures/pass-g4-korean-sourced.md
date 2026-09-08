# G4 오탐 대조 — 한국어 근거가 붙은 한국어 주장은 통과해야 한다

G4 에서 영문 토큰 종속을 없앤 목적은 **한국어 1 차 출처를 근거로 인정하는 것**이다.
근거 없는 주장만 잡아야지 한국어라는 이유로 잡으면 안 된다.

- 대상: iOS

## S1. 인증키(.p8) 방식으로 발급받는다

- 어디서: `developer.apple.com/account/resources/authkeys/list`
- 무엇을: Keys (메뉴)
- 동작: 열기
- 값: 입력 없음
- 확인: 키 목록 페이지가 열린다
- 안 보이면: 권한 — Account Holder 또는 Admin 역할이 필요하다
- 출처: https://developer.apple.com/help/account/ (조회 2026-09-08)

## S2. 구 방식은 지원 종료 대상이므로 신규 등록에 쓰지 않는다

- 어디서: `developer.apple.com/account/resources/certificates/list`
- 무엇을: Certificates (메뉴)
- 동작: 선택
- 값: 입력 없음
- 확인: 기존 인증서 목록이 보인다
- 안 보이면: 요금제 — 무료 계정에는 배포용 인증서 항목이 없다
- 출처: https://developer.apple.com/help/account/ (조회 2026-09-08) — 문서에 "지원 종료" 명시
