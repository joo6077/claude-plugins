# Search Strategy — 최신 정보 수집 우선순위

`/setup-guide`가 그 시점 최신 정보를 수집할 때 따르는 순서. 학습 데이터 추측은 금지.

## 우선순위 (위에서 아래로)

### 1. WebFetch — 콘솔 UI / 공식 help 페이지

가장 빠르고 정확. 콘솔 클릭 경로, 메뉴 라벨, + 버튼 옵션 리스트는 매번 WebFetch.

주요 출처:

- **Apple**: `developer.apple.com/help/account/` 하위 (identifiers/keys/devices/profiles)
- **Firebase**: `firebase.google.com/docs/`
- **Google Cloud**: `cloud.google.com/docs/`
- **AWS**: `docs.aws.amazon.com/`
- **Stripe**: `stripe.com/docs/`
- **Sentry**: `docs.sentry.io/`

WebFetch 프롬프트 예시: "Apple Developer Portal에서 새 App ID를 등록하는 정확한 클릭 경로를 step-by-step으로 추출해줘. 좌측 메뉴 위치, + 버튼 이후 옵션, Capabilities 체크리스트 위치, 최종 등록 버튼 라벨까지. 한국어로 정리."

### 2. Context7 — SDK API 문서

라이브러리/SDK의 메서드 시그니처, 초기화 코드, 마이그레이션 가이드.

흐름:

1. `mcp__context7__resolve-library-id` — 라이브러리 ID 검색
2. `mcp__context7__query-docs` — 구체 API 질의

대상: firebase-ios-sdk, FlutterFire, AWS SDK, Stripe SDK 등.

### 3. Codex 위임 — 정책 / 교차검증 / 깊은 분석

`codex-rescue` 에이전트에 `MODE=research`, `--write` 없이 위임.

언제 쓸지:

- 정책 사실 검증 (예: Apple Bundle ID 변경 정책)
- 여러 출처 교차검증 필요
- WebFetch 한 페이지로 답이 안 나올 때
- 깊은 분석/판단 필요

언제 안 쓸지:

- 단순 페이지 fetch (WebFetch가 더 빠름)
- API 시그니처 (Context7가 더 정확)

`~/.claude/codex-prompt-template.md` 템플릿 필수.

### 4. WebSearch — fallback

위 세 가지로 안 잡힐 때만. 검색어에 **현재 연도 필수** (`2026 Firebase setup`). 연도 없으면 deprecated 결과가 상위 노출됨.

## Deprecated 감지 규칙

매번 검색 결과에서 아래 확인:

- 문서/페이지의 **마지막 업데이트 날짜** — 2년+ 자동 ⚠️ 경고 박스
- 본문에 "deprecated", "legacy", "old method", "will be removed", "removed in" 키워드
- API/SDK 메이저 버전 변경 안내
- "use X instead" 같은 대체 권장

감지 시 가이드에 명시:

```
> **❌ Deprecated:** <옛 방법 + 비추천 이유>
> **✅ 현재 권장:** <새 방법 + 이유>
```

## 검색 결과 검증 체크리스트

- [ ] 공식 도메인 (developer.apple.com, firebase.google.com 등) URL인지 확인
- [ ] 문서 마지막 업데이트 날짜 추출 (없으면 추정 메모)
- [ ] 본문에 deprecated 경고 키워드 grep
- [ ] 여러 페이지에서 교차 확인 (한 페이지 정보를 절대적으로 신뢰하지 않기)
