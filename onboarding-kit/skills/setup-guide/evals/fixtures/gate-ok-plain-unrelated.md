# 픽스처 — 막는 요구 표가 아닌 표만 있는 가이드 (G5 PASS rows=0)

이 파일은 `guide_gate` 의 G5 가 과하게 막지 않는지 증명하는 입력이다. 끝의 `| 요구 사항 | 설명 |` 표는
막는 요구 표가 아니므로 G5 는 `PASS rows=0` 이어야 한다.

## Step 1: FlutterFire CLI 설치

```bash
dart pub global activate flutterfire_cli
```

**출처:** <https://firebase.google.com/docs/flutter/setup> (조회 2026-09-08)

## Step 2: 프로젝트 연결

```bash
flutterfire configure
```

**출처:** <https://firebase.google.com/docs/flutter/setup> (조회 2026-09-08)

| 요구 사항 | 설명 |
| --- | --- |
| 로그인 | 계정이 있어야 한다 |
