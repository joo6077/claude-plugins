# G3 양성 케이스 — 도메인 혼용

iOS 를 대상으로 선언해 놓고 Android 경로를 섞었다. 기존 킷의 G3 는 stack 인자가 비면
항상 PASS 하는 no-op 이라 이런 문서를 3 개월간 통과시켰다.

- 대상: iOS

## S1. APNs 인증키를 업로드한다

- 어디서: `console.firebase.google.com/project/_/settings/cloudmessaging`
- 무엇을: APNs authentication key (버튼)
- 동작: 업로드
- 값: `.p8` 파일
- 확인: Key ID 행이 추가된다
- 안 보이면: 권한 — Firebase 편집자 권한이 필요하다
- 출처: https://firebase.google.com/docs/cloud-messaging/ios/certs (조회 2026-09-08)

## S2. google-services.json 을 프로젝트에 넣는다

- 어디서: `android/app/` 디렉토리 (AndroidManifest 와 같은 모듈)
- 무엇을: google-services.json (파일)
- 동작: 저장
- 값: Firebase 콘솔에서 받은 파일
- 확인: `build.gradle` 동기화가 성공한다
- 안 보이면: 버전 — 구버전 Gradle 플러그인은 경로가 다르다
- 출처: https://firebase.google.com/docs/android/setup (조회 2026-09-08)
