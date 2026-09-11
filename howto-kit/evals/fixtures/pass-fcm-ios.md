# FCM iOS APNs 인증키 등록

- 대상: iOS
- 적용 범위: Firebase Console 2026-09 · 언어 영문(한국어 병기)
- 수수료: 없음 / 처리기간: 즉시 / 되돌리기: 가능 (키 삭제로 원복)

## 사전 요구사항

| 작업 | 사이트 |
| --- | --- |
| APNs 인증키(.p8) 발급 | developer.apple.com (Developer Account) |
| 키 업로드 | console.firebase.google.com (Firebase Console) |

## S1. Firebase 프로젝트의 Cloud Messaging 설정을 연다

- 어디서: `console.firebase.google.com/project/_/settings/cloudmessaging`
- 무엇을: Cloud Messaging (탭)
- 동작: 열기
- 값: 입력 없음
- 확인: 페이지에 `Apple app configuration` 섹션이 보인다
- 안 보이면: 권한 — 프로젝트 소유자에게 Firebase 편집자 권한을 요청해야 설정 탭이 보인다
- 출처: https://firebase.google.com/docs/cloud-messaging/ios/certs (조회 2026-09-08)

## S2. APNs 인증키를 업로드한다

- 어디서: `Apple app configuration` 섹션 > `APNs authentication key`
- 무엇을: Upload (버튼)
- 동작: 업로드
- 값: 앞서 발급받은 `.p8` 파일 + Key ID(10자 영숫자) + Team ID(10자 영숫자)
- 확인: 키 목록에 Key ID 행이 새로 추가된다
- 안 보이면: 요금제 — 무료 Spark 플랜에서도 보인다. 안 보이면 iOS 앱이 프로젝트에 등록되지 않은 것이다
- 출처: https://firebase.google.com/docs/cloud-messaging/ios/certs (조회 2026-09-08)

## 최종 상태

`APNs authentication key` 아래에 Key ID 행이 1 개 이상 표시된다.

## 뒤처리

로컬에 내려받은 `.p8` 파일은 재발급이 불가하므로 안전한 곳에 보관한다.
