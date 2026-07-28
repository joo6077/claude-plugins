---
name: setup-guide
description: "프로젝트의 외부 서비스(Firebase, GCP, AWS, FCM, OAuth, Stripe 등) 설정 가이드를 그 시점 최신 정보 기준으로 step-by-step MD 문서로 생성한다. 콘솔/대시보드 클릭 경로, 인증 키 발급, 프로젝트 코드 연동까지 매번 1차 출처(공식 docs)를 fetch하여 deprecated 정보로 사용자가 헤매지 않게 한다. 사용자가 'FCM 설정해야 해', 'Firebase 어떻게 연동해?', 'GCP 설정 가이드', '외부 서비스 설정', 'push notification 세팅', 'OAuth 설정', '서드파티 연동 방법', '셋업 가이드 만들어줘' 등을 언급하면 이 스킬을 사용한다. 설정/세팅/연동/가이드 키워드와 외부 서비스명이 함께 나오면 반드시 트리거."
argument-hint: "[서비스명] 또는 빈값(전체 스캔)"
user-invocable: true
---

프로젝트를 분석하고 그 시점 최신 정보로 1차 출처를 fetch하여, 외부 서비스 설정 가이드 MD를 step-by-step으로 생성한다.

## Input

`$ARGUMENTS`:

- 특정 서비스: `/setup-guide firebase`, `/setup-guide fcm ios`, `/setup-guide stripe`
- 전체 스캔: `/setup-guide` (인자 없음) → 프로젝트 전체를 분석하여 외부 서비스 목록 도출 + 사용자에게 선택지 제시

## 핵심 원칙

이 스킬의 존재 이유는 **deprecated된 정보로 사용자가 헤매지 않도록** 하는 것이다.

- 학습 데이터의 콘솔 UI 정보는 자주 outdated → **매번 WebFetch로 공식 help 페이지 직접 조회**
- 검색 시 반드시 **현재 연도** 포함 — 연도 없이 검색하면 2~3년 전 deprecated 결과가 상위 노출
- 버전 번호, CLI 명령어, 콘솔 UI 경로는 **구체적으로** — 모호한 안내는 콘솔 UI 변경 시마다 사용자가 헤맴
- deprecated 발견 시 **명시적 경고** + 현재 권장 방법

### 출처 원장 (Source Ledger) — 문장 규칙이 아니라 아티팩트

"그 시점 최신 정보 기준" 이라는 주장은 **조회 흔적 없이는 성립하지 않는다.** 각 Step 을 쓰기 **전에** 그 Step 의 1차 출처를 fetch 하고, Step 본문에 **출처 URL + 조회일**을 남긴다 (`references/format-checklist.md` §3 의 `**출처:**` 줄). **fetch 하지 않은 Step 은 쓰지 않는다** — 학습 데이터로 채운 뒤 헤더의 대표 URL 하나로 전체를 정당화하는 것이 이 스킬의 대표 실패 형태다.

fetch 가 끝까지 실패한 항목은 조용히 넘기지 말고 `[미검증]` + 사유 한 줄을 붙인다. **`[미검증]` 이 2 건 이상이면 완료가 아니라 부분 완료로 보고**하고 사용자에게 확인을 요청한다.

마커 표기와 임계값은 `harness/docs/guides/qa-evaluation-guide.md` §Canonical Unverified-Evidence Protocol 이 정본이다 — 이 킷에서 재정의하거나 동의어(`미확인`, `N/A`, `unverified`) 를 만들지 않는다. 등급 근거는 `harness/docs/guides/skill-design-guide.md` §3.7 Completion Evidence Gate (같은 위반 2 회 재발 시 E1 문장 규칙 → E2 아티팩트).

## Gotchas (반복 실수 방지)

### Gotcha 1: 스택 확정 없이 가이드 작성 금지

가이드 작성을 시작하기 전에 **반드시 프로젝트 스택을 확정**한다. Flutter / 네이티브 iOS / React Native / Node 백엔드는 같은 서비스라도 SDK 설치 명령, 초기화 코드, CLI 자동화 도구가 완전히 다르다.

탐지 방법은 `references/project-detection.md` 참조.

스택 확정 실패 시 → 사용자에게 명시적으로 묻기 ("Flutter iOS 기준? 네이티브 Swift 기준?")

### Gotcha 2: 콘솔 UI 클릭 경로는 학습 데이터 추측 금지

Apple Developer Portal, Firebase Console 등의 + 버튼 옵션, 메뉴 라벨, 화면 순서는 자주 바뀐다. 학습 데이터로 답하면 사용자가 화면에서 못 찾는다.

**WebFetch 우선** — Codex 위임보다 빠르고 정확. `references/search-strategy.md` 참조.

### Gotcha 3: 사이트 혼동 (Apple)

Apple 셋업은 두 사이트가 완전히 다르다:

- **App Store Connect** (`appstoreconnect.apple.com`) — 앱 출시·심사 관리. 셋업 단계엔 거의 안 들어감
- **Apple Developer Portal** (`developer.apple.com/account`) — App ID·인증서·키 발급. 셋업의 99%가 여기

생성하는 가이드 사전 요구사항 섹션 맨 위에 두 사이트 차이 표 박기.

같은 패턴이 다른 플랫폼에도 있음:
- Google Cloud: GCP Console vs Firebase Console
- AWS: AWS Console vs AWS Marketplace

### Gotcha 4: 글로벌 유니크 식별자 충돌

Bundle ID (Apple), Package Name (Android), Project ID (GCP/Firebase) 등은 **전 세계 모든 계정에 걸쳐 유니크**해야 한다. 흔한 조합(`com.fitpal.app`)은 누가 선점했을 확률 높음.

가이드 트러블슈팅에 "not available" 에러 케이스 자동 포함. 해결책: 조직/도메인 reverse prefix 강조.

### Gotcha 5: 등록 ≠ 활성화

App ID 등록과 Provisioning Profile 생성은 별개. Firebase 프로젝트 생성과 APNs Key 업로드는 별개. 단계별 분리 명시.

### Gotcha 6: 출시 후 변경 불가 정책

Bundle ID는 빌드 업로드 후 변경 불가. Firebase Project ID도 생성 후 변경 불가. 가이드 사전 요구사항에 경고.

### Gotcha 7: 요청한 서비스·범위만 가이드 — 임의 확장 금지

(insights-report #1·#3 "스코프 임의 확장·과잉설계" 대응) 사용자가 요청한 **그 서비스, 그 기능 하나**만 가이드한다. 요청하지 않은 인접 서비스·단계를 "있으면 좋으니까" 끼워넣지 않는다.

- ❌ "FCM 가이드"를 요청했는데 같은 Firebase 우산 아래 Analytics·Crashlytics·Remote Config까지 묶어서 생성
- ❌ "Stripe 연동"에 요청 안 한 webhook·refund·subscription 흐름까지 자동 추가
- ❌ 단순 셋업에 요청 안 한 CI/CD·모니터링·IaC 단계 덧붙임

인접 서비스가 **셋업의 필수 선행 조건**이면(예: APNs Key 없이는 FCM iOS 불가) 그 의존만 사전 요구사항에 명시하고, 본문은 요청 서비스에 국한한다. 추가로 다룰 가치가 있어 보이면 가이드 생성이 아니라 **마지막에 한 줄로 제안**만 한다 ("Analytics도 필요하면 `/setup-guide firebase analytics`").

11개 섹션(`references/format-checklist.md`)은 **포맷 표준이지 채우기 할당량이 아니다**. 요청 서비스에 해당 없는 섹션(예: 클라이언트 전용 SDK에 IAM, 단발 셋업에 환경 분기)은 "해당 없음" 한 줄로 닫거나 생략한다 — 억지로 내용을 만들어 부피를 늘리지 않는다.

### Gotcha 8: 프로젝트 내부 경로·파일명·env 키는 날조 대상이 아니다 — 레포를 먼저 읽어라

(insights-report #3 실측: 기존 config 가 이미 있는데도 **존재하지 않는 FCM credentials 파일명을 날조**했다.)

콘솔 쪽 절차는 1차 출처 fetch 로 확인하고, **레포 쪽 산출물은 실제로 읽어서** 확인한다. 이 스킬은 파일 경로·환경변수 키를 대량 생성하므로 날조 리스크가 구조적으로 가장 크다.

가이드 본문에 프로젝트 파일 경로나 env 키를 쓰기 전에:

1. **패턴으로 탐색한다** — Glob/Grep 으로 실제 파일을 찾는다 (`**/GoogleService-Info.plist`, `.env*`, `**/firebase_options.dart`, `**/*.p8`). **이름을 가정한 단일 경로 확인은 탐색이 아니다** — flavor·모듈별로 경로가 갈린다.
2. **찾은 것을 `파일:라인` 으로 열거한다** — 이 열거가 아티팩트다 (E2). 기존 env 키는 실제 키 이름을 그대로 인용한다.
3. **없으면 "이 단계에서 새로 만든다/내려받는다" 를 명시하거나 사용자에게 묻는다.** 있을 것 같은 이름을 적지 않는다. 확인 자체가 불가하면 `[미검증]` 을 붙인다.

- ❌ 기존 `.env` 에 다른 이름의 키가 있는데 확인 없이 관례적인 이름(`FIREBASE_SERVER_KEY` 등)으로 안내
- ❌ 실측 없이 `ios/Runner/GoogleService-Info.plist` 를 단정 — flavor 별 디렉토리로 갈리는 프로젝트에서 즉시 틀림
- ✅ Glob 결과를 인용한 뒤 그 경로로 안내 / 결과 0 건이면 "이 Step 에서 새로 생성" 임을 명시

## Process

### Phase 1: 스택 + 외부 서비스 탐지

1. **스택 확정** — `references/project-detection.md`의 의존성 파일 매핑 따라 스캔. 멀티스택 모노레포면 사용자에게 명시적 확인.
2. **외부 서비스 의존성 탐지** — 의존성 파일, 설정 파일(`.env*`, `docker-compose*.yml`, `terraform/`), 코드 grep (SDK 초기화 패턴) 종합.
3. **인자 처리**:
   - 특정 서비스 지정 → 해당 서비스 집중
   - 빈 인자 → 탐지한 서비스 목록 사용자에게 제시 + 어떤 가이드 만들지 선택받기

### Phase 2: 최신 정보 수집

`references/search-strategy.md`의 우선순위에 따라:

1. **WebFetch** — 콘솔 UI/help 페이지 직접 fetch
2. **Context7** — SDK API 문서 (`resolve-library-id` → `query-docs`)
3. **Codex 위임** — 정책 검증, 교차검증, 깊은 분석 필요 시
4. **WebSearch** — fallback, 검색어에 현재 연도 필수

**Deprecated 감지**: 문서 마지막 업데이트 2년+, "deprecated/legacy/will be removed" 키워드, 메이저 버전 변경 안내 → 가이드에 ❌/✅ 박스로 명시. 반대로 **1차 출처가 deprecated 라고 하지 않은 것을 deprecated 로 쓰지 않는다** — "권장하지 않음(not recommended)" 과 "deprecated" 는 다른 주장이고, 출처가 말하지 않은 강도를 올리는 것도 날조다.

**출처 URL 은 그 시점 canonical host 로 기록한다.** 문서 호스트는 이전된다. WebFetch 는 크로스 호스트 리다이렉트를 따라가지 않고 리다이렉트 URL 을 되돌려주므로, 그것을 받으면 새 URL 로 다시 fetch 하고 **원장에는 최종 URL** 을 남긴다 (`references/search-strategy.md` 참조).

### Phase 3: 가이드 MD 생성

`references/format-checklist.md`의 11개 섹션을 **순서대로** 채운다.

저장 위치: 기본 `docs/setup/<서비스명>/<기능명>.md`. 사용자가 위치 지정하면 그쪽.

여러 하위 기능(예: Firebase → FCM, Analytics, Crashlytics)이면 각각 별도 파일로 분리.

### Phase 4: 검증 + 완료 안내

1. **출처 원장 대조** — 모든 Step 에 `**출처:**` 줄이 있는지 확인한다. 없는 Step 이 있으면 그 Step 은 fetch 없이 쓰였다는 뜻이므로, 지금 fetch 하거나 `[미검증]` 을 붙인다.
2. **레포 근거 대조** — 가이드에 등장하는 프로젝트 내부 경로·env 키가 전부 Glob/Grep 실측 근거를 갖는지 확인 (Gotcha 8). 근거 없는 항목은 제거하거나 "새로 생성" 으로 고친다.
3. 생성된 가이드의 모든 외부 URL이 공식 도메인인지 확인 (`references/search-strategy.md`)
4. 11개 섹션 누락 확인
5. **`[미검증]` 집계** — 건수를 세어 보고에 그대로 쓴다. 0 건이면 완료, 1 건이면 완료 + 경고 명시, **2 건 이상이면 부분 완료**로 보고하고 사용자 확인을 요청한다.
6. 사용자에게 파일 경로 + "막히는 부분 알려주세요" 안내. 사용자가 코드 변경에 도움 필요하면 직접 도와줄 수 있음 안내.

## References

- `references/project-detection.md` — 스택 탐지 패턴
- `references/format-checklist.md` — 가이드 MD 11개 섹션 체크리스트
- `references/search-strategy.md` — WebFetch → Context7 → Codex → WebSearch 우선순위
