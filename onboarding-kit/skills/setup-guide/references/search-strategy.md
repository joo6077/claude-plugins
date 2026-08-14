# Search Strategy — 최신 정보 수집 우선순위

`/setup-guide`가 그 시점 최신 정보를 수집할 때 따르는 순서. 학습 데이터 추측은 금지.

## 우선순위 (위에서 아래로)

### 1. WebFetch — 콘솔 UI / 공식 help 페이지

가장 빠르고 정확. 콘솔 클릭 경로, 메뉴 라벨, + 버튼 옵션 리스트는 매번 WebFetch.

주요 출처 (호스트/섹션명 2026-07-27 실측):

- **Apple**: `developer.apple.com/help/account/` — 실측 top-level 섹션은 Release notes / Basics / Membership / Access / **Certificates** / **Keys** / **Identifiers** / **Capabilities** / **Services** / **Service Configurations** / **Devices** / **Provisioning Profiles** / Reference. App ID 는 **Identifiers**, APNs 키 등 개인 키는 **Keys** 아래다. 앱 레코드 생성·빌드 업로드·TestFlight 는 이 사이트가 아니라 **App Store Connect** 다 (SKILL.md Gotcha 3 작업별 표)
- **Firebase**: `firebase.google.com/docs/`
- **Google Cloud**: `docs.cloud.google.com/docs/` — `cloud.google.com/docs/` 로 요청하면 이쪽으로 리다이렉트된다 (실측 2026-08-13). 서비스 계정 / ADC 문서도 최종 URL 이 `docs.cloud.google.com` 이다. **원장에는 최종 URL 을 남긴다**
- **AWS**: `docs.aws.amazon.com/`
- **Stripe**: `docs.stripe.com/` (`stripe.com/docs/` 는 구 호스트 — 아래 호스트 이전 주의 참조). 개발환경 문서는 언어별 variant URL 을 제공한다
- **Sentry**: `docs.sentry.io/`

WebFetch 프롬프트 예시: "Apple Developer 공개 Help 에서 App ID 등록이 어느 섹션에 있는지, 그 페이지에 적힌 섹션명·필드명을 문서 표기 그대로 추출해줘. 문서에 없는 화면 흐름은 '문서에 없음' 이라고 답할 것."

#### WebFetch 로 닿지 않는 것 — 로그인 뒤 콘솔 화면

**WebFetch 가 볼 수 있는 것은 로그인 없이 접근 가능한 공개 문서뿐이다.** Firebase Console · Apple Developer Portal · App Store Connect 의 **로그인 뒤 실시간 UI 는 어떤 도구로도 확인할 수 없다** (실측 2026-08-13). 따라서:

- 인용은 **공개 문서에 실제로 적힌 라벨**로 한정한다. 문서에 없는 버튼 단위 흐름을 "이렇게 생겼다" 고 단정하지 마라.
- 확정할 수 있는 것은 대개 **상위 섹션명까지**다 (Apple: `Identifiers` / `Keys` / `Certificates` / `Provisioning Profiles` · Firebase: `Settings` → `General` → `Cloud Messaging` 탭 → `iOS app configuration`).
- 이 한계를 **가이드 본문에 한 줄로 적는 것**까지가 절차다. 없는 확신을 파는 것보다 정직한 경계 표시가 사용자를 덜 헤매게 한다.
- 이것은 `[미검증:ENV]` 를 붙일 사유가 **아니다** — 공개 문서로 확인한 부분은 정상 출처이고, 확인 못 한 부분은 애초에 쓰지 않는다.

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

**역방향 금지:** 1차 출처가 deprecated 라고 하지 않은 것을 deprecated 로 쓰지 않는다. "권장하지 않음(not recommended)" · "레거시" · "제거 예정" 은 서로 다른 강도의 주장이고, 출처보다 강한 주장을 쓰는 것도 날조다. 실측 2026-07-27 · 재확인 2026-08-13: FCM Apple/Flutter 문서는 APNs 인증 키(`.p8`) 를 **안내**하지만 인증서(`.p12`) 를 deprecated 로 표기하지 않는다 — 이 문서에서 deprecated 로 명시된 것은 Instance ID API 다. `.p8` 을 권장한다는 사실로부터 `.p12` 의 deprecation 을 **추론하지 마라.** 이 승격은 `guide_gate` G4 가 기계적으로 잡는다 (SKILL.md §Guide Conformance Gate).

## Fetch 실패 시 fallback 사다리

한 단계에서 실패하면 다음으로 내려가되, **어느 단계에서 얻었는지 기록**한다.

1. 대상 페이지 WebFetch → 리다이렉트가 오면 최종 URL 로 재시도
2. 같은 공식 도메인의 인접 페이지 (색인/개요 페이지에서 정확한 하위 경로 확인 후 재시도)
3. Context7 (SDK API 한정) → Codex 위임 (정책/교차검증)
4. WebSearch (현재 연도 포함)

네 단계 모두 실패하면 **학습 데이터로 채우지 않는다.** 해당 Step 에 `**출처:** [미검증:ENV] — <시도한 단계와 실패 출력 · 통제 불가 사유 · 재검증 명령>` 을 남긴다. 접미 없는 `[미검증]` 은 정본에서 `INVALID` 로 해석되므로 쓰지 않는다.

**네 단계를 실제로 타지 않았으면 `:ENV` 를 쓸 수 없다.** 사다리를 건너뛴 주장은 `[미검증:INVALID]` 로 강등되고, "이번엔 안 조회하기로 했다" 는 마커가 아니라 그냥 **미완**이다. 마커 분류·카운터 분리·임계는 SKILL.md §출처 원장 을 따르며, 정본은 `harness/docs/guides/qa-evaluation-guide.md` §Canonical Unverified-Evidence Protocol 이다 — 이 문서에서 임계 숫자를 재정의하지 않는다.

## 검색 결과 검증 체크리스트

- [ ] 공식 도메인 (developer.apple.com, firebase.google.com 등) URL인지 확인
- [ ] 문서 마지막 업데이트 날짜 추출 (없으면 추정 메모)
- [ ] 본문에 deprecated 경고 키워드 grep
- [ ] 여러 페이지에서 교차 확인 (한 페이지 정보를 절대적으로 신뢰하지 않기)
- [ ] 조회한 최종 URL + 조회일을 해당 Step 의 `**출처:**` 줄에 기록 (출처 원장 아티팩트)
