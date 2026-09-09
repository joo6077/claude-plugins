# 콘솔 딥링크 관행 — 벤더 문서가 URL 을 박아 두는 방식

`last_updated: 2026-09-09`

이 킷의 P3 는 **딥링크가 메뉴 경로보다 우선한다**이다. 메뉴 이름은 개편마다 바뀌지만 URL 은
훨씬 덜 바뀌기 때문이다. 그 원칙이 서려면 전제가 하나 성립해야 한다 — **벤더가 공식 문서
본문에 콘솔 URL 을 실제로 박아 둔다.** 이 문서는 그 전제의 실측 기록이다.

**콘솔 URL 자체를 열어 검증하지 않는다.** 로그인 리다이렉트라 무엇도 증명하지 못한다. 근거는
언제나 **그 URL 을 담고 있는 공식 문서 페이지**이고, 아래 인용은 전부 그 페이지의 응답 본문에서
추출했다.

---

## 1. 확정된 딥링크 인용 — 7 벤더 · 8 건

조회일 **2026-09-09**.

| 벤더 | 문서에 박힌 URL 형태 | 출처 문서 | 조회일 |
| --- | --- | --- | --- |
| Firebase | `console.firebase.google.com/project/_/settings/general/android:com.random.android` | `https://firebase.google.com/docs/reference/admin/node/firebase-admin.auth.decodedidtoken` | 2026-09-09 |
| Google Cloud | `https://console.cloud.google.com/logs?project=PROJECT_ID` | `https://docs.cloud.google.com/iam/docs/grant-role-console` | 2026-09-09 |
| Apple | `https://appstoreconnect.apple.com/teams/[Team ID]/access/ci/infrastructure-validation` | `https://developer.apple.com/documentation/xcode/understanding-infrastructure-validation-builds` | 2026-09-09 |
| Stripe (a) | `https://dashboard.stripe.com/test/apikeys` | `https://docs.stripe.com/keys` | 2026-09-09 |
| Stripe (b) | `https://dashboard.stripe.com/<ACCOUNT_ID>/<MODE>/<PAGE>?apps[<APP_ID>][TARGET]=VIEWPORT_ID` | `https://docs.stripe.com/stripe-apps/deep-links` | 2026-09-09 |
| GitHub | `github.com/settings/personal-access-tokens/new` | `https://docs.github.com/en/copilot/how-tos/copilot-cli/automate-copilot-cli/automate-with-actions` | 2026-09-09 |
| AWS | `https://console.aws.amazon.com/iam/` | `https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_last-accessed-view-data.html` | 2026-09-09 |
| Azure | `https://portal.azure.com/#view/Microsoft_Azure_Monitoring/AzureMonitoringBrowseBlade/%7E/logs` | `https://learn.microsoft.com/en-us/azure/azure-monitor/logs/log-analytics-overview` | 2026-09-09 |

### 1.1 자리표시자 표기는 벤더마다 다르다

같은 "여기에 당신 값을 넣으라" 를 벤더마다 다르게 쓴다. 절차 문서에서 이걸 통일해 버리면
사용자가 문서와 화면을 대조하지 못한다. **벤더 표기를 그대로 옮겨라.**

| 벤더 | 자리표시자 | 원문 |
| --- | --- | --- |
| Firebase | `_` | URL 경로에 `project/_/` |
| Google Cloud | `PROJECT_ID` | `?project=PROJECT_ID` |
| Apple | `[Team ID]` | 대괄호 + 공백 포함 |
| Stripe | `<ACCOUNT_ID>` `<MODE>` `<PAGE>` | 꺾쇠 |

Apple 은 자리표시자를 **문장으로 설명한다**:

> *"To reach the Infrastructure Validation page more quickly, replace `[Team ID]` in the following
> URL with your Team ID: `https://appstoreconnect.apple.com/teams/[Team ID]/access/ci/infrastructure-validation`"*
> — developer.apple.com/documentation/xcode/understanding-infrastructure-validation-builds (조회 2026-09-09)

Google Cloud 도 마찬가지다:

> *"Send the following URL to the principal to whom you granted the role in the preceding step:
> `https://console.cloud.google.com/logs?project=PROJECT_ID`"*
> — docs.cloud.google.com/iam/docs/grant-role-console (조회 2026-09-09)

AWS 는 절차 문장 안에 URL 을 넣는다:

> *"Sign in to the AWS Management Console and open the IAM console at
> `https://console.aws.amazon.com/iam/`"*
> — docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_last-accessed-view-data.html (조회 2026-09-09)

### 1.2 Stripe — 모드가 URL 세그먼트다

Stripe 는 딥링크 문법을 **정식으로 문서화**한 드문 사례다. 그 문법에서 모드는 쿼리 파라미터가
아니라 **경로 세그먼트**다.

```text
https://dashboard.stripe.com/<ACCOUNT_ID>/<MODE>/<PAGE>?apps[<APP_ID>][TARGET]=VIEWPORT_ID
```

> *"MODE: Use `test` for sandboxes (including the test mode sandbox) or omit a value for live mode"*
> — docs.stripe.com/stripe-apps/deep-links (조회 2026-09-09)

**"생략하면 live"** 라는 것이 이 문법의 함정이다. 절차 문서에서 `dashboard.stripe.com/apikeys`
라고만 쓰면 그것은 **운영 모드 화면**을 연다. 테스트 키를 찾는 사용자는 거기서 원하는 값을
보지 못한다. `docs.stripe.com/keys` 본문의 "API keys" 링크는 실제로
`https://dashboard.stripe.com/test/apikeys` 를 가리킨다 — 문서가 테스트 모드를 기본으로 삼는다.

### 1.3 Azure — 포털 딥링크는 `#view/` 프래그먼트다

Azure Portal 의 딥링크는 경로가 아니라 **URL 프래그먼트**에 들어간다. 공식 Learn 문서 본문의
"Azure Monitor" 링크가 그 형태다:

```text
https://portal.azure.com/#view/Microsoft_Azure_Monitoring/AzureMonitoringBrowseBlade/%7E/logs
```

프래그먼트는 서버로 전송되지 않으므로, 이 URL 을 리다이렉트 검사로 확인할 수 없다. 근거는
**Learn 문서가 그 링크를 걸고 있다**는 사실뿐이다 — 그 이상으로 단정하지 않는다.

---

## 2. 딥링크를 안내할 때의 함정

### 2.1 리전이 URL 에 박히는 벤더가 있다 — AWS `확인됨`

AWS 는 로그인 엔드포인트 자체에 리전을 실을 수 있고, **그 리전으로 리다이렉트된다.**

> *"You can manually request a certain regional sign-in endpoint by signing in to the region-enabled
> main console home page using a URL syntax like the following:"* +
> `https://alias.signin.aws.amazon.com/console?region=ap-southeast-1`
> — docs.aws.amazon.com/IAM/latest/UserGuide/id_users_sign-in.html (조회 2026-09-09)

절차 문서가 리전을 박아 두면 다른 리전을 쓰는 사용자는 **엉뚱한 리전의 콘솔**에 도착한다.
리전을 아는 경우가 아니면 슬롯을 비워라.

### 2.2 Google 계정 인덱스 슬롯 `/u/0/` — `[미확인]`

`/u/0/` 같은 계정 인덱스를 임의로 박으면 다른 계정으로 리다이렉트된다는 것은 널리 알려진
관행이지만, **그 동작을 설명하는 공식 문장을 확보하지 못했다.** 시도한 URL 은
`howto-kit/references/provenance-notes.md` §5 에 있다.

킷의 처리: 계정이 여럿일 수 있으면 **슬롯을 빼고** 안내한다. 이 규칙은 유지하되, 근거를
"Google 이 그렇게 문서화했다" 고 말하지 않는다.

### 2.3 Firebase `_` 가 프로젝트 id 자리라는 **설명 문장** — `[미확인]`

URL 안에 `project/_/` 가 등장하는 것은 확인했다. 그러나 `_` 가 프로젝트 id 자리표시자라고
**설명하는 문장**은 찾지 못했다. 관행으로는 통용되지만 1 차 출처가 없다.

---

## 3. 검증 기법 — 문서가 SPA 면 HTML 로는 못 잡는다

`developer.apple.com` 의 문서는 클라이언트 렌더링이다. HTML 을 받아도 **17KB 껍데기**만 오고
본문 문장이 들어 있지 않다. 이 사실을 모르면 Apple 인용은 영원히 "확인 실패" 로 남는다 —
이번 사이클의 Codex 위임이 정확히 그렇게 끝났다.

검증 가능한 원문은 문서 데이터 엔드포인트다.

```text
https://developer.apple.com/tutorials/data/documentation/<문서 경로>.json
```

예: `xcode/understanding-infrastructure-validation-builds` →
`https://developer.apple.com/tutorials/data/documentation/xcode/understanding-infrastructure-validation-builds.json`
(8.7KB, `application/json`). 본문이 `inlineContent` 배열로 들어 있어 문장을 그대로 뽑을 수 있다.

**일반 규칙**: 문서 페이지의 응답 크기가 부자연스럽게 작고 `<script>` 만 몇 개 있으면 SPA 를
의심하라. 그 벤더의 문서 데이터 API 를 찾아라. 못 찾으면 그 인용은 `[미확인]` 이다.

---

## 4. 조회 기록 — 위임 결과를 그대로 옮기지 않았다

Codex 위임 1 회 (MODE=research · read-only · foreground · 검색 하드캡 20). rollout 로그의
`turn_aborted` 는 0 건으로 정상 완주했다. 결과는 5 건 확정 · 2 건 확인 실패였다.

그 결과를 **그대로 쓰지 않았다.** 반환된 인용문을 로컬 `curl` 로 대조했더니 8 건 중 **3 건이
MISS** 였다:

| 항목 | 1 차 대조 | 원인 |
| --- | --- | --- |
| Google Cloud | MISS | 인용문은 맞았고 내 대조 문자열이 과도하게 엄격했다 — 재추출로 확정 |
| AWS | MISS | 같음 — 재추출로 확정 |
| Apple | MISS | **문서가 SPA** — HTML 에 본문이 없다. §3 의 JSON 엔드포인트로 확정 |

그리고 Codex 가 확인 실패로 돌려준 **2 건(Stripe · Azure)은 로컬 조회로 해소**했다. Stripe 는
`docs.stripe.com/keys` 본문에 `dashboard.stripe.com/test/apikeys` 링크가 6 회 있었고,
Azure 는 `log-analytics-overview` 본문에 `#view/` 딥링크가 있었다.

**교훈**: 위임 결과의 "확인 실패" 는 그 도구의 환경 한계일 수 있다. 확인 실패를 문서에 옮기기
전에 **다른 경로로 한 번 더** 시도하라. 반대로, 위임이 "확인됨" 이라 답한 인용도 대조 없이
옮기지 마라 — 이번에 8 건 중 3 건이 1 차 대조에서 어긋났다.

미확정 근거의 원장은 `howto-kit/references/provenance-notes.md` 가 정본이다. 확정된 항목은
이 문서가 정본이다.
