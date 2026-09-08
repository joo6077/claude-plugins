# G5 양성 케이스 — 말단 액션 위반

이 파일은 **일부러 G5 를 위반**한다. 게이트가 실제로 FAIL 을 내는지 증명하는 용도이며
정상 산출물의 예시가 아니다.

- 대상: iOS

## S1. Cloud Messaging 섹션에서 APNs 키를 설정한다

- 어디서: `console.firebase.google.com/project/_/settings/cloudmessaging`
- 무엇을: APNs 인증키 (섹션)
- 동작: 이 섹션에서 적절히 설정
- 값: 입력 없음
- 확인: 설정이 반영된다
- 안 보이면: 권한 — 관리자에게 문의한다
- 출처: https://firebase.google.com/docs/cloud-messaging/ios/certs (조회 2026-09-08)

## S2. 해당 항목을 찾아 값을 넣는다

- 어디서: `Apple app configuration` 섹션
- 무엇을: 해당 항목을
- 동작: 필요에 따라
- 값: 알맞은 값
- 확인: 값이 저장된다
- 안 보이면: 버전 — 구버전 콘솔에는 위치가 다르다
- 출처: https://firebase.google.com/docs/cloud-messaging/ios/certs (조회 2026-09-08)
