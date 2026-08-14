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

fetch 가 끝까지 실패한 항목은 조용히 넘기지 말고 마커 + 사유 한 줄을 붙인다. **마커는 접미로 분류한다** — 접미 없는 `[미검증]` 은 정본에서 `INVALID` 로 해석되므로 쓰지 않는다.

| 상황 | 마커 | 카운터 |
| --- | --- | --- |
| 1차 출처 문서에 **접근 자체가 불가**했다 (네트워크·도구 부재·크로스호스트 fetch 실패 등 내가 통제할 수 없는 요인) | `[미검증:ENV]` | `env_gaps` |
| 도구 부재라고 적었지만 fallback 사다리를 안 탔거나, 조회는 됐는데 그 출력이 아무것도 입증하지 못한다 | `[미검증:INVALID]` | 임계 카운터 |
| 문서에 그 내용이 **없다** / 아직 안 썼다 / **이번엔 안 돌리기로 했다** | 마커가 아니라 **FAIL** — 해당 Step 을 쓰지 않거나 사용자에게 묻는다 | — |

**임계는 `[미검증:INVALID]` 에만 적용되고, 건수별 판정 규칙의 숫자는 정본이 정한다** — `harness/docs/guides/qa-evaluation-guide.md` §카운팅 및 자동 REJECT 임계. **이 킷에서 그 숫자를 다시 적지 않는다.** 킷마다 임계를 따로 쓰면 같은 상태가 킷마다 다른 판정으로 갈린다 (정본 §Canonical Unverified-Evidence Protocol 이 기록한 실측 drift: 킷별 2/3/0 건). `[미검증:ENV]` 는 이 카운터에 합산하지 않고 따로 세어 검증 커버리지(`(총 Step − env_gaps) / 총 Step`)로만 보고하며, 커버리지 임계 역시 정본 §검증 커버리지 게이트를 따른다.

`[미검증:ENV]` 를 쓰려면 근거란에 **4 요건**이 전부 있어야 한다 (하나라도 없으면 `INVALID` 강등): ① 1차 도구 시도 기록과 그 출력 ② `references/search-strategy.md` §Fetch 실패 시 fallback 사다리 4 단계를 실제로 탄 기록 ③ 실패를 서술이 아닌 **출력**으로 ④ 왜 내 통제 밖인지 한 문장 + 환경이 갖춰졌을 때 실행할 **재검증 명령**.

마커 의미·분류·임계는 `harness/docs/guides/qa-evaluation-guide.md` §Canonical Unverified-Evidence Protocol 이 정본이다 — 이 킷에서 재정의하거나 동의어(`미확인`, `N/A`, `unverified`) 를 만들지 않는다. 등급 근거는 `harness/docs/guides/skill-design-guide.md` §3.7 (Completion Evidence Gate · Enforcement 3 등급).

### Guide Conformance Gate (E3) — 규칙은 **이미 배포된 가이드**에도 소급된다

이 스킬은 가이드를 **영속 아티팩트**로 생산한다. 그래서 규칙이 바뀌면 어제 만든 가이드가 조용히 규칙 위반 상태가 된다. 실측 (2026-08-13): 이 킷의 쇼케이스 예제가 킷 자신의 evals 6 케이스 중 3 개를 **3 개월간 위반한 채** 배포돼 있었다 — 출처 원장 0/8, Flutter 가이드에 네이티브 Swift 초기화, 출처에 없는 `.p12` deprecated 단정. 규칙과 evals 는 고쳤는데 **이미 나간 산출물을 다시 재는 경로가 없었다.**

그래서 이 규칙들은 문장(E1)·자기보고 체크리스트(E2)가 아니라 **결정론적 게이트(E3)** 다. 아래 함수는 LLM 을 호출하지 않는 순수 판정이며, **지금 쓰는 가이드와 이미 배포된 가이드 양쪽에 똑같이 적용된다.**

```bash
# Guide Conformance Gate — LLM 호출 없는 순수 판정. zsh · bash 동일 출력 (2026-08-13 양쪽 실행 확인).
# 사용: guide_gate <가이드.md> [스택]     예) guide_gate docs/setup/firebase/fcm-ios.md flutter
guide_gate() {
  g=$1; stack=${2:-}
  [ -f "$g" ] || { echo "GATE_BLOCKED no_such_file=$g"; return 0; }
  fence=$(printf '\140\140\140')   # 백틱 3 개 — 문서 렌더링 보호를 위해 8 진수로 생성
  fail=0

  # G1 출처 원장 완전성 — Step 수와 출처 줄 수가 같아야 한다 (열거값은 타이핑하지 말고 계산)
  steps=$(grep -c '^## Step ' "$g" || true)
  ledger=$(grep -c '^\*\*출처:\*\*' "$g" || true)
  if [ "$steps" -eq 0 ] || [ "$steps" -ne "$ledger" ]; then
    echo "G1_LEDGER FAIL steps=$steps ledger=$ledger"; fail=1
  else
    echo "G1_LEDGER PASS steps=$steps ledger=$ledger"
  fi

  # G2 미검증 마커 — 접미 없는 레거시 0 건 · INVALID 는 정본 임계 미만 (ENV 는 별도 카운터).
  #    아래 상수는 정본(qa-evaluation-guide §카운팅 및 자동 REJECT 임계)을 그대로 **구현**한 것이지
  #    킷이 새로 정한 값이 아니다. 정본이 바뀌면 이 상수도 같이 바꾼다 — 여기서 먼저 바꾸지 마라.
  bare=$(grep -oF '[미검증]' "$g" | grep -c . || true)
  inval=$(grep -oF '[미검증:INVALID]' "$g" | grep -c . || true)
  envg=$(grep -oF '[미검증:ENV]' "$g" | grep -c . || true)
  if [ "$bare" -ne 0 ] || [ "$inval" -ge 2 ]; then
    echo "G2_MARKER FAIL bare=$bare invalid=$inval env=$envg"; fail=1
  else
    echo "G2_MARKER PASS bare=$bare invalid=$inval env=$envg"
  fi

  # G3 스택 혼용 — Flutter 가이드에 네이티브 Swift 코드블록이 있으면 실패.
  #    산문으로 "Flutter 는 AppDelegate 를 건드리지 않는다" 고 쓰는 것은 통과한다 — 코드 지시만 잡는다
  sw=$(grep -c "^${fence}swift" "$g" || true)
  if [ "$stack" = "flutter" ] && [ "$sw" -ne 0 ]; then
    echo "G3_STACKMIX FAIL swift_fence=$sw"; fail=1
  else
    echo "G3_STACKMIX PASS stack=${stack:-unset} swift_fence=$sw"
  fi

  # G4 deprecation 주장 결합 — Deprecated 박스를 쓴 Step 은 그 Step 의 출처 줄이
  #    "출처가 실제로 deprecated 라고 말했다" 는 근거를 담아야 한다 (출처보다 강한 주장 금지)
  g4=$(awk '
    function flush(){ if (st != "" && dep && src !~ /[Dd]eprecat/) print ln }
    /^## /           { flush(); st=""; src=""; dep=0 }
    /^## Step /      { st=$0; ln=FNR }
    /^\*\*출처:\*\*/ { src=$0 }
    /❌ Deprecated/  { dep=1 }
    END              { flush() }
  ' "$g" | grep -c . || true)
  if [ "$g4" -ne 0 ]; then
    echo "G4_DEPRECATION FAIL unsourced_boxes=$g4"; fail=1
  else
    echo "G4_DEPRECATION PASS unsourced_boxes=0"
  fi

  [ "$fail" -eq 0 ] && echo GATE_PASS || echo GATE_FAIL
}
```

- **게이트 출력을 그대로 보고에 붙여라.** "게이트 통과함" 이라는 문장은 증거가 아니다 — `GATE_PASS` 를 포함한 5 줄 출력이 증거다.
- `GATE_FAIL` 이면 완료 보고를 하지 마라. 고치고 다시 돌린다.
- **게이트를 우회하거나 조건을 느슨하게 고치지 마라.** 우회된 게이트는 없는 게이트보다 나쁘다. 게이트가 정당한 케이스를 막는다고 판단되면 그 사실을 사용자에게 보고하고 판단을 받는다.
- 게이트가 잡는 것은 **기계로 판정 가능한 4 가지**뿐이다. 사실 정확성·스코프·경로 날조는 여전히 Gotchas 와 Phase 4 검증의 몫이다 (단일 게이트는 보장이 아니다).

## Gotchas (반복 실수 방지)

### Gotcha 1: 스택 확정 없이 가이드 작성 금지

가이드 작성을 시작하기 전에 **반드시 프로젝트 스택을 확정**한다. Flutter / 네이티브 iOS / React Native / Node 백엔드는 같은 서비스라도 SDK 설치 명령, 초기화 코드, CLI 자동화 도구가 완전히 다르다.

탐지 방법은 `references/project-detection.md` 참조.

스택 확정 실패 시 → 사용자에게 명시적으로 묻기 ("Flutter iOS 기준? 네이티브 Swift 기준?")

### Gotcha 2: 콘솔 UI 라벨은 학습 데이터 추측 금지 — 그리고 **로그인 뒤 화면은 애초에 검증 불가다**

Apple Developer Portal, Firebase Console 등의 + 버튼 옵션, 메뉴 라벨, 화면 순서는 자주 바뀐다. 학습 데이터로 답하면 사용자가 화면에서 못 찾는다. **WebFetch 우선** — Codex 위임보다 빠르고 정확. `references/search-strategy.md` 참조.

**단, WebFetch 로 닿는 것은 로그인 없이 볼 수 있는 공개 문서뿐이다.** 콘솔에 로그인한 뒤의 실제 화면은 어떤 도구로도 확인할 수 없다 (실측 2026-08-13: Firebase Console · Apple Developer Portal 양쪽 모두 로그인 뒤 실시간 UI 는 fetch 불가). 따라서:

- **인용 가능한 것은 공개 문서에 실제로 적혀 있는 라벨뿐이다.** 예로 Firebase FCM 문서에서 확인되는 라벨은 `Settings` · `General` · `Cloud Messaging tab` · `iOS app configuration` · `APNs authentication key` · `Upload`/`Save` · `DevOps & Engagement` · `Messaging` · `New campaign` · `Notifications` · `Send test message` · `Add an FCM registration token` · `Test` 다 (조회 2026-08-13).
- 공개 문서에 없는 **버튼 단위 흐름**을 "이렇게 생겼다" 고 단정하지 마라. 문서에 있는 **상위 섹션명까지만** 확정하고, 그 아래는 "이 섹션에서 …" 로 열어 둔다.
- 생성하는 가이드에 **"이 라벨은 공개 문서 기준이며 로그인 뒤 화면은 다를 수 있다"** 는 한 줄을 남긴다. 이것이 이 스킬이 사용자에게 줄 수 있는 가장 정직한 안내다 — 없는 확신을 파는 것보다 낫다.
- A/B 롤아웃·언어 설정 때문에 라벨이 갈릴 수 있으므로, 사용자가 화면에서 못 찾을 때 쓸 **상위 섹션명 검색어**를 함께 준다.

### Gotcha 3: 사이트 혼동 (Apple) — "어느 사이트냐" 는 **작업마다** 갈린다

Apple 은 두 사이트가 완전히 다르고, **어느 한쪽이 셋업 전부를 담당하지 않는다.** "셋업은 전부 Developer Portal" 같은 뭉뚱그린 안내를 쓰지 마라 — 앱 레코드 생성·빌드 업로드·TestFlight 에서 사용자가 곧바로 막힌다. 생성하는 가이드의 사전 요구사항 섹션 맨 위에 **작업별 표**를 박는다 (조회 2026-08-13, Apple 공개 Help 기준):

| 작업 | 사이트 | 섹션/흐름 |
| --- | --- | --- |
| Bundle ID / App ID 등록 | Apple Developer Account (`developer.apple.com/account`) | `Certificates, Identifiers & Profiles` → `Identifiers` → App IDs |
| APNs 키 생성 | Apple Developer Account | `Certificates, Identifiers & Profiles` → `Keys` (APNs service 선택 → `.p8` 다운로드) |
| 인증서 | Apple Developer Account | `Certificates` |
| Provisioning Profile | Apple Developer Account | `Profiles` / `Provisioning Profiles` |
| **앱 레코드** 생성 | **App Store Connect** (`appstoreconnect.apple.com`) | `Apps` → `+` → `New App` |
| **빌드 업로드** | **App Store Connect** | 앱 추가 후 Xcode/Transporter/API 로 업로드 (bundle ID + version + build string 으로 연결) |
| **TestFlight** | **App Store Connect** | beta build 배포 · 테스터 관리 · 피드백 |

키·식별자 발급은 Developer Account, **앱이라는 레코드와 배포는 App Store Connect** 다. 요청받은 셋업이 어느 행에 해당하는지 먼저 확정하고, 해당 행만 가이드에 넣는다 (Gotcha 7 스코프).

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
3. **없으면 "이 단계에서 새로 만든다/내려받는다" 를 명시하거나 사용자에게 묻는다.** 있을 것 같은 이름을 적지 않는다. 레포를 읽을 수 있는데 결과가 0 건인 것은 미검증이 아니라 **"아직 없음"** 이라는 확정 사실이다 — 그대로 쓴다. 레포 접근 자체가 불가한 환경일 때만 `[미검증:ENV]` 를 4 요건과 함께 붙인다.

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

4. **Regeneration Drift 검사 — 같은 가이드가 이미 있으면 새로 쓰기 전에 먼저 잰다.**

   `docs/setup/` 아래(또는 사용자가 지정한 위치)에 같은 서비스·기능의 가이드가 이미 있으면, 덮어쓰거나 무시하지 말고 **기존 파일에 게이트를 먼저 돌린다.**

   ```bash
   find docs/setup -type f -name '*.md' 2>/dev/null | while IFS= read -r f; do
     printf '%s\n' "--- $f"; guide_gate "$f" "$STACK"
   done
   ```

   - `GATE_FAIL` 이 나오면 **그것이 이번 작업의 첫 산출물**이다. 어느 검사가 왜 깨졌는지 사용자에게 보고하고, 새 가이드를 만들지 기존 가이드를 갱신할지 확인받는다.
   - 규칙이 바뀐 뒤 이미 배포된 가이드가 조용히 위반 상태로 남는 것이 이 스킬의 구조적 실패 형태다 (§Guide Conformance Gate 실측). **이 단계를 건너뛰면 같은 사고가 그대로 재발한다.**
   - 글로빙 대신 `find` 를 쓴 이유: zsh 는 `nomatch` 가 기본이라 매치 0 인 글로브가 명령을 통째로 죽인다.

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

1. **Guide Conformance Gate 실행 (E3 · 먼저 한다)** — `guide_gate <생성한 가이드> <스택>` 을 돌리고 **출력 5 줄을 보고에 그대로 붙인다.** `GATE_FAIL` 이면 완료 보고를 하지 말고 고친 뒤 다시 돌린다. 이 게이트가 G1(출처 원장 완전성) · G2(마커 분류/임계) · G3(스택 혼용) · G4(deprecation 근거 결합) 을 기계적으로 판정한다.
2. **레포 근거 대조** — 가이드에 등장하는 프로젝트 내부 경로·env 키가 전부 Glob/Grep 실측 근거를 갖는지 확인 (Gotcha 8). 근거 없는 항목은 제거하거나 "새로 생성" 으로 고친다.
3. 생성된 가이드의 모든 외부 URL이 공식 도메인인지 + **그 시점 canonical host** 인지 확인 (`references/search-strategy.md`)
4. 11개 섹션 누락 확인
5. **마커 집계 보고** — 게이트 G2 가 낸 `bare` / `invalid` / `env` 세 숫자를 그대로 쓴다. `invalid` 에 대한 건수별 판정은 정본(`harness/docs/guides/qa-evaluation-guide.md` §카운팅 및 자동 REJECT 임계)을 그대로 적용하고 **여기서 숫자를 재정의하지 않는다.** `env` 는 임계에 합산하지 않고 검증 커버리지로 따로 보고한다.
6. 사용자에게 파일 경로 + "막히는 부분 알려주세요" 안내. 사용자가 코드 변경에 도움 필요하면 직접 도와줄 수 있음 안내. **콘솔 라벨은 공개 문서 기준이며 로그인 뒤 화면과 다를 수 있다**는 점을 함께 알린다 (Gotcha 2).

## References

- `references/project-detection.md` — 스택 탐지 패턴
- `references/format-checklist.md` — 가이드 MD 11개 섹션 체크리스트
- `references/search-strategy.md` — WebFetch → Context7 → Codex → WebSearch 우선순위
