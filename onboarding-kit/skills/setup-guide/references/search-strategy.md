# Search Strategy — 최신 정보 수집 우선순위

`/setup-guide`가 그 시점 최신 정보를 수집할 때 따르는 순서. 학습 데이터 추측은 금지.

## 우선순위 (위에서 아래로)

### 1. WebFetch — 콘솔 UI / 공식 help 페이지

가장 빠르고 정확. 콘솔 클릭 경로, 메뉴 라벨, + 버튼 옵션 리스트는 매번 WebFetch.

주요 출처 (호스트/섹션명 2026-07-27 실측):

- **Apple**: `developer.apple.com/help/account/` — 실측 top-level 섹션은 Release notes / Basics / Membership / Access / **Certificates** / **Keys** / **Identifiers** / **Capabilities** / **Services** / **Service Configurations** / **Devices** / **Provisioning Profiles** / Reference. App ID 는 **Identifiers**, APNs 키 등 개인 키는 **Keys** 아래다
- **Firebase**: `firebase.google.com/docs/`
- **Google Cloud**: `cloud.google.com/docs/`
- **AWS**: `docs.aws.amazon.com/`
- **Stripe**: `docs.stripe.com/` (`stripe.com/docs/` 는 구 호스트 — 아래 호스트 이전 주의 참조)
- **Sentry**: `docs.sentry.io/`

WebFetch 프롬프트 예시: "Apple Developer Portal에서 새 App ID를 등록하는 정확한 클릭 경로를 step-by-step으로 추출해줘. 좌측 메뉴 위치, + 버튼 이후 옵션, Capabilities 체크리스트 위치, 최종 등록 버튼 라벨까지. 한국어로 정리."

#### 호스트 이전 / 리다이렉트 주의

문서 호스트는 이전된다. WebFetch 는 **크로스 호스트 리다이렉트를 따라가지 않고 리다이렉트 URL 을 되돌려준다** — 본문이 없다고 "문서가 사라졌다" 로 해석하지 말고, 돌려받은 URL 로 다시 fetch 한 뒤 **원장에는 최종 URL** 을 남긴다.

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

## 버전 확인은 패키지 레지스트리 우선

SDK 버전은 GitHub Releases 페이지 대신 **패키지 레지스트리**(pub.dev / npm / crates.io / PyPI) 를 1차로 쓴다. 실측 2026-07-27: `github.com/firebase/flutterfire/releases` fetch 는 2020 년 프리릴리스만 반환하여 최신 버전 확인에 쓸 수 없었고, `pub.dev/packages/firebase_messaging` 은 현행 버전과 `firebase_core` 제약을 즉시 돌려줬다. GitHub Releases 는 **breaking change 서술을 읽을 때**만 보조로 쓴다.

## Deprecated 감지 규칙

매번 검색 결과에서 아래 확인:

- 문서/페이지의 **마지막 업데이트 날짜** — 2년+ 자동 ⚠️ 경고 박스
- 본문에 "deprecated", "legacy", "old method", "will be removed", "removed in" 키워드
- API/SDK 메이저 버전 변경 안내
- "use X instead" 같은 대체 권장

감지 시 가이드에 명시:

```text
> **❌ Deprecated:** <옛 방법 + 비추천 이유>
> **✅ 현재 권장:** <새 방법 + 이유>
```

**역방향 금지:** 1차 출처가 deprecated 라고 하지 않은 것을 deprecated 로 쓰지 않는다. "권장하지 않음(not recommended)" · "레거시" · "제거 예정" 은 서로 다른 강도의 주장이고, 출처보다 강한 주장을 쓰는 것도 날조다. 실측 2026-07-27: FCM Apple 클라이언트 문서는 APNs 인증 키(`.p8`) 를 **권장**하지만 인증서(`.p12`) 를 deprecated 로 표기하지 않는다 — 이 문서에서 deprecated 로 명시된 것은 Instance ID API 다.

## Fetch 실패 시 fallback 사다리

한 단계에서 실패하면 다음으로 내려가되, **어느 단계에서 얻었는지 기록**한다.

1. 대상 페이지 WebFetch → 리다이렉트가 오면 최종 URL 로 재시도
2. 같은 공식 도메인의 인접 페이지 (색인/개요 페이지에서 정확한 하위 경로 확인 후 재시도)
3. Context7 (SDK API 한정) → Codex 위임 (정책/교차검증)
4. WebSearch (현재 연도 포함)

네 단계 모두 실패하면 **학습 데이터로 채우지 않는다.** 해당 Step 에 `**출처:** [미검증] — <시도한 단계와 실패 사유>` 를 남긴다. `[미검증]` 이 2 건 이상이면 가이드는 부분 완료로 보고한다 (SKILL.md §출처 원장 · 정본은 `harness/docs/guides/qa-evaluation-guide.md` §Canonical Unverified-Evidence Protocol).

## 검색 결과 검증 체크리스트

- [ ] 공식 도메인 (developer.apple.com, firebase.google.com 등) URL인지 확인
- [ ] 문서 마지막 업데이트 날짜 추출 (없으면 추정 메모)
- [ ] 본문에 deprecated 경고 키워드 grep
- [ ] 여러 페이지에서 교차 확인 (한 페이지 정보를 절대적으로 신뢰하지 않기)
- [ ] 조회한 최종 URL + 조회일을 해당 Step 의 `**출처:**` 줄에 기록 (출처 원장 아티팩트)
