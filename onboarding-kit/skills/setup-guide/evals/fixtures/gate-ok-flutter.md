# 픽스처 — 정상 Flutter 가이드 (G3 스택 인자 판정 · ER-02 빈 문자열 스택)

이 파일은 `guide_gate` 의 G3 가 스택 인자 유무로 갈리는지 증명하는 입력이다. Swift 펜스가 없으므로
`flutter` 를 주면 PASS, 스택을 비우면 FAIL 이어야 한다.

## Step 1: FlutterFire CLI 설치

```bash
dart pub global activate flutterfire_cli
```

**출처:** https://firebase.google.com/docs/flutter/setup (조회 2026-09-08)

## Step 2: 프로젝트 연결

```bash
flutterfire configure
```

**출처:** https://firebase.google.com/docs/flutter/setup (조회 2026-09-08)
