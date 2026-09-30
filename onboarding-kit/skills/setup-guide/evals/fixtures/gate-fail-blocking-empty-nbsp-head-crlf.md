# 픽스처 — 머리 칸 공백이 U+00A0 이고 줄 끝이 CRLF (G5 FAIL)

이 파일은 `guide_gate` 의 G5 가 이 표 모양을 알아보는지 증명하는 입력이다. 머리 칸 사이 공백이 줄바꿈 없는 공백(U+00A0)이다. 표를 알아보고 빈 우회 칸으로 FAIL 이어야 한다. 그 공백 글자가 이 입력의 목적이라 표 칸 모양 경고(MD060)만 끈다.

<!-- markdownlint-disable MD060 -->

| 요구 | 출처 | 막히는 것 | 우회 |
| --- | --- | --- | --- |
| 실기기 | [Firebase Apple 셋업](https://firebase.google.com/docs/ios/setup) | 원격 메시지 수신 확인 | `우회 없음(출처 확인)` |
| 유료 개발자 계정 | [Apple 지원 기능 표](https://developer.apple.com/help/account/reference/supported-capabilities-ios) | APNs 키 구성 | |

## Step 1: FlutterFire CLI 설치

```bash
dart pub global activate flutterfire_cli
```

**출처:** <https://firebase.google.com/docs/flutter/setup> (조회 2026-09-08)
