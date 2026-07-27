# Research Sources — onboarding-kit kaizen

`/onboarding-kaizen` Phase 1 데이터 수집 시 폴링하는 외부 출처 목록.

## 1차 출처 (공식 docs/help)

| 서비스 | URL | 폴링 빈도 |
|--------|-----|-----------|
| Apple Developer Account Help | https://developer.apple.com/help/account/ | 월 1회 |
| Apple Bundle ID 정책 | https://developer.apple.com/help/app-store-connect/reference/app-information/ | 분기 1회 |
| Firebase iOS docs | https://firebase.google.com/docs/cloud-messaging/ios/client | 월 1회 |
| FlutterFire docs | https://github.com/firebase/flutterfire/tree/main/docs | 월 1회 |
| Google Cloud Console help | https://cloud.google.com/docs/ | 분기 1회 |
| AWS Console help | https://docs.aws.amazon.com/ | 분기 1회 |
| Stripe iOS / Web docs | https://docs.stripe.com/ | 월 1회 |
| Sentry SDK docs | https://docs.sentry.io/ | 분기 1회 |

## 2차 출처 (커뮤니티 / 변경 시그널)

| 출처 | 신호 |
|------|------|
| Firebase 공식 블로그 | https://firebase.blog/ — 메이저 SDK 릴리스, deprecated 공지 |
| Apple Developer Forums | https://developer.apple.com/forums/ — Push/FCM 트러블슈팅 트렌드 |
| FlutterFire GitHub Releases | https://github.com/firebase/flutterfire/releases — 호환 매트릭스 변경 |
| Reddit /r/iOSProgramming | 커뮤니티에서 자주 막히는 단계 |
| Stack Overflow firebase-cloud-messaging 태그 | 최근 질문 트렌드 |

## 사용자 피드백 메모리

`~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/memory/feedback_setup_guide_*.md` 스캔 → SKILL.md Gotchas에 추가/수정할 패턴 도출.

## kaizen 트리거 체크

1. 1차 출처의 페이지 마지막 업데이트 날짜 비교 — 변경이 있으면 해당 섹션 재검토
2. 2차 출처에서 deprecated/breaking change 시그널 grep
3. 피드백 메모리 3개+ 누적 시 자동 트리거
