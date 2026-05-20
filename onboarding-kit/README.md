# onboarding-kit

스택 무관 외부 서비스 셋업 가이드 자동 생성 플러그인.

## 개요

프로젝트의 외부 서비스(Firebase, GCP, AWS, FCM, OAuth, Stripe, Sentry 등)를 셋업할 때 **그 시점 최신 정보 기준 step-by-step 가이드 MD**를 자동 생성한다. 학습 데이터의 outdated 정보가 아니라 매 호출마다 WebFetch → Context7 → Codex 순서로 1차 출처를 fetch하여 deprecated 정보로 사용자가 헤매지 않게 한다.

bambu-kit과 같은 도구형 1스킬 킷. 스택 무관 — Flutter / 네이티브 / React Native / Node / Python / Rust 등 어떤 프로젝트에서도 동작.

## 스킬

<!-- AUTO:skills:start -->
| 스킬 | 용도 |
|------|------|
| `/setup-guide` | 그 시점 최신 정보 기준 외부 서비스 셋업 가이드 step-by-step MD 자동 생성 |
<!-- AUTO:skills:end -->

트리거 키워드: "FCM 설정해야 해", "Firebase 어떻게 연동해?", "GCP 설정 가이드", "OAuth 설정", "셋업 가이드 만들어줘".

## 사용 흐름

1. 프로젝트 스택 자동 탐지 (`pubspec.yaml` / `Cargo.toml` / `package.json` / `requirements.txt` / `Podfile` 등)
2. 외부 서비스 의존성 grep + 사용자 확인
3. WebFetch로 공식 docs/help 페이지 직접 조회 → 최신 콘솔 UI 경로 확보
4. Context7으로 SDK API 문서 조회
5. 11개 섹션 표준 포맷(헤더 / 사전 요구사항 / 설정 단계 / 코드 변경 / 권한 / 비용 / 환경 분기 / Rollback / 보안 / 검증 / 트러블슈팅)으로 가이드 MD 생성
6. 사용자에게 파일 경로 + 다음 단계 안내

## 핵심 가치

- **그 시점 최신 정보** — 학습 데이터 추측 금지, 매 호출 시 1차 출처 fetch
- **스택 무관** — 의존성 파일 자동 탐지, 멀티스택 모노레포는 사용자에게 확인
- **사이트 혼동 사전 박기** — Apple/Google/AWS의 두 콘솔 차이를 가이드 사전 요구사항에 표로
- **deprecated 자동 경고** — 2년+ 문서, 키워드 grep, ❌/✅ 박스 자동 삽입

## 카이젠

이 레포 개발용으로 `.claude/skills/onboarding-kaizen/`이 존재한다 (플러그인에는 포함 X). bambu-kaizen 패턴과 동일하게 SKILL.md/references/evals를 주기적으로 개선한다.

- 수동 호출: `/onboarding-kaizen`
- 전체 카이젠: `/kaizen` (Phase 13으로 자동 실행)
- 사용자 피드백 메모리(`feedback_setup_guide_*`)가 3개 이상 누적되면 자동 트리거 후보

## License

MIT
