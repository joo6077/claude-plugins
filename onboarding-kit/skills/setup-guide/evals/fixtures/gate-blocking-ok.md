# 픽스처 — 막는 요구 세 칸이 다 찬 표 (G5 PASS)

이 파일은 `guide_gate` 의 G5 가 제대로 채운 표를 통과시키는지 증명하는 입력이다. 두 행 모두 네 칸이 차 있고 출처 칸에 주소가 있다.

| 요구 | 출처 | 막히는 것 | 우회 |
| --- | --- | --- | --- |
| 실기기 | [Firebase Apple 셋업](https://firebase.google.com/docs/ios/setup) | 원격 메시지 수신 확인 | `우회 없음(출처 확인)` |
| 앱 출시 | 막는 요구가 아니다 — [Push Notification Console](https://developer.apple.com/documentation/usernotifications/testing-notifications-using-the-push-notification-console) | 없음 | 해당 없음 |

## Step 1: FlutterFire CLI 설치

```bash
dart pub global activate flutterfire_cli
```

**출처:** <https://firebase.google.com/docs/flutter/setup> (조회 2026-09-08)
