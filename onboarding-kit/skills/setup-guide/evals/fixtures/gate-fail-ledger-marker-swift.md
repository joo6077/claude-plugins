# 픽스처 — G1 · G2 · G3 가 함께 FAIL (양성 대조 · 알려진 답)

G1 · G2 · G3 는 같은 수나 0 을 기대하는 검사라 정상 입력만으로는 살아 있는지 모른다. 이 파일은 셋을 한 번에 깨뜨린다.
손으로 센 답은 Step 2 · 출처 줄 1 (G1), 접미 없는 마커 1 · `INVALID` 2 · `ENV` 1 (G2), `flutter` 스택에 Swift 코드 블록 1 (G3) 이다.

## Step 1: APNs 인증 키 업로드

[미검증] 조회 실패

**출처:** <https://firebase.google.com/docs/cloud-messaging/flutter/get-started> (조회 2026-09-24) — [미검증:INVALID] 사다리를 타지 않았다 · [미검증:INVALID] 실패 출력이 없다 · [미검증:ENV] 네트워크 없음

## Step 2: 앱 초기화

```swift
FirebaseApp.configure()
```
