# 픽스처 — 막는 요구 표의 출처 칸에 주소가 없다 (G5 FAIL nourl)

이 파일은 `guide_gate` 의 G5 가 주소 없는 출처를 잡는지 증명하는 입력이다. 네 칸은 다 찼지만 첫 행 출처가 문서 이름뿐이라 FAIL 이어야 한다.

| 요구 | 출처 | 막히는 것 | 우회 |
| --- | --- | --- | --- |
| 실기기 | Firebase Apple 셋업 문서 | 원격 메시지 수신 확인 | `우회 없음(출처 확인)` |

## Step 1: FlutterFire CLI 설치

```bash
dart pub global activate flutterfire_cli
```

**출처:** <https://firebase.google.com/docs/flutter/setup> (조회 2026-09-08)
