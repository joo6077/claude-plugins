# 픽스처 — 머리 칸이 밑줄 굵은 글자 (G5 FAIL)

이 파일은 `guide_gate` 의 G5 가 이 표 모양을 알아보는지 증명하는 입력이다. 머리 낱말을 `__` 로 감쌌다. 표를 알아보고 빈 우회 칸으로 FAIL 이어야 한다.

| __요구__ | __출처__ | __막히는 것__ | __우회__ |
| --- | --- | --- | --- |
| 실기기 | [Firebase Apple 셋업](https://firebase.google.com/docs/ios/setup) | 원격 메시지 수신 확인 | `우회 없음(출처 확인)` |
| 유료 개발자 계정 | [Apple 지원 기능 표](https://developer.apple.com/help/account/reference/supported-capabilities-ios) | APNs 키 구성 | |

## Step 1: FlutterFire CLI 설치

```bash
dart pub global activate flutterfire_cli
```

**출처:** <https://firebase.google.com/docs/flutter/setup> (조회 2026-09-08)
