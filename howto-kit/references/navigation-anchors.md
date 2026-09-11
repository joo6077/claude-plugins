# 네비게이션 앵커 — 딥링크 · 화면 지목 어휘 · 분기 카탈로그

사용자가 화면에서 길을 잃는 지점을 없애는 세 가지 장치다.

## 1. 불변도 순위 — 잘 안 바뀌는 것 위에 안내를 세운다

```text
불변도 높음   URL 경로 · 설정 키 / API 이름
             섹션명
             버튼 / 필드 라벨
불변도 낮음   아이콘 · 배치(좌 / 우 / 상단)
```

URL 은 버튼 라벨보다 훨씬 덜 바뀐다. **딥링크가 메뉴 경로보다 우선한다.**

## 2. 실측된 딥링크 관행

공식 문서에 콘솔 URL 이 그대로 박혀 있는 경우가 많다. 먼저 이것을 찾아라.

**확정 인용의 정본은 `docs/howto/deep-links.md` 다.** 아래는 요약이며 조회일 2026-09-09 기준이다.
인용 전에 다시 조회한다.

| 서비스 | 공식 문서에 등장하는 형태 | 출처 |
| --- | --- | --- |
| Firebase | `console.firebase.google.com/project/_/settings/general/android:com.random.android` | firebase.google.com/docs/reference/admin/node/firebase-admin.auth.decodedidtoken |
| Google Cloud | *"Send the following URL to the principal …"* + `https://console.cloud.google.com/logs?project=PROJECT_ID` | docs.cloud.google.com/iam/docs/grant-role-console |
| Apple | *"replace `[Team ID]` in the following URL with your Team ID: `https://appstoreconnect.apple.com/teams/[Team ID]/access/ci/infrastructure-validation`"* | developer.apple.com/documentation/xcode/understanding-infrastructure-validation-builds |
| Stripe | `dashboard.stripe.com/test/apikeys` · 문법 `dashboard.stripe.com/<ACCOUNT_ID>/<MODE>/<PAGE>` | docs.stripe.com/keys · docs.stripe.com/stripe-apps/deep-links |
| GitHub | `github.com/settings/personal-access-tokens/new` | docs.github.com |
| AWS | *"Sign in to the AWS Management Console and open the IAM console at `https://console.aws.amazon.com/iam/`"* | docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_last-accessed-view-data.html |
| Azure | `https://portal.azure.com/#view/Microsoft_Azure_Monitoring/AzureMonitoringBrowseBlade/%7E/logs` | learn.microsoft.com/en-us/azure/azure-monitor/logs/log-analytics-overview |

**Stripe 는 모드가 경로 세그먼트다** — *"MODE: Use `test` for sandboxes (including the test mode
sandbox) or omit a value for live mode"*. **생략하면 live** 이므로 `dashboard.stripe.com/apikeys`
라고만 쓰면 운영 모드 화면이 열리고, 테스트 키를 찾는 사용자는 원하는 값을 못 본다.

**Azure 는 프래그먼트(`#view/`)에 딥링크가 들어간다.** 프래그먼트는 서버로 가지 않으므로
리다이렉트 검사로 검증할 수 없다 — 근거는 Learn 문서가 그 링크를 건다는 사실뿐이다.

### 자리표시자 표기를 통일하지 마라

`_`(Firebase) · `PROJECT_ID`(Google Cloud) · `[Team ID]`(Apple) · `<ACCOUNT_ID>`(Stripe) —
벤더마다 다르다. 통일해 버리면 사용자가 문서와 화면을 대조하지 못한다. **원문 표기를 그대로 옮겨라.**

### 리전·계정 슬롯을 조심하라

AWS 는 로그인 엔드포인트에 리전을 실을 수 있고 **그 리전으로 리다이렉트된다**
(*"You can manually request a certain regional sign-in endpoint …"* — docs.aws.amazon.com/IAM/latest/UserGuide/id_users_sign-in.html).
리전을 모르면 슬롯을 비워라.

`/u/0/` 같은 Google 계정 인덱스도 임의로 박지 않는다. 다만 그 동작을 설명하는 공식 문장은
**확보하지 못했다** — `[미확인]`, `references/provenance-notes.md` §5 참조.

### 딥링크가 없으면 전역 검색어를 준다

대부분의 콘솔에 상단 검색창이 있다. 메뉴 트리를 외우게 하는 것보다 검색어 하나가 강하다.

> *"The Search bar at the top in the Google Cloud console is an efficient way to search for various
> product services, documentation pages, tutorials and even Google Cloud Resources"*
> — cloud.google.com/blog/topics/developers-practitioners/tips-get-most-out-google-cloud-documentation

## 3. 화면 지목 어휘 — 방향어는 단독으로 쓰지 않는다

**금지 대상은 방향어가 아니라 "방향어만" 이다.** 확정 정본은 `docs/howto/ui-anchoring.md` 다.

> *"Don't use directional terms as the only clue to location."*
> — learn.microsoft.com/en-us/style-guide/accessibility/writing-all-abilities (조회 2026-09-09)

> *"It's OK to use a directional term if another indication of location, such as in the Save As
> dialog box, on the Standard toolbar, or in the title bar, is also included."*
> — learn.microsoft.com/en-us/style-guide/a-z-word-list-term-collections/u/upper-left-upper-right (조회 2026-09-09)

Google 은 더 강하게 적었고 **완화 조건을 명시하지 않았다** — 그러므로 "이름과 함께면 된다" 의
근거로 Google 을 인용하지 마라.

> *"Don't use directional language to orient the reader, such as above, below, or right-hand side.
> … If a UI element is hard to find, provide a screenshot."*
> — developers.google.com/style/ui-elements (조회 2026-09-09)

`위쪽` · `아래` · `오른편` 은 화면 크기와 레이아웃에 따라 달라진다. **이름 있는 영역**을 1 순위로
쓰고, 방향어는 그것을 보조한다.

실제 지원 문서가 쓰는 지목 어휘:

| 위치 | 실제 문장 | 출처 |
| --- | --- | --- |
| 좌측 사이드바 | *"Click Components from the left sidebar."* | support.atlassian.com/statuspage |
| 사이드바 + 상세 | *"Click Network in the sidebar, then click the network service that you're using (such as Wi-Fi) on the right."* | support.apple.com/102022 |
| 탭 | *"Click the Third-party tab."* | support.atlassian.com/statuspage |
| 탭 아래 배너 | *"From the Commits tab, select Sync now in the info banner under the tabs."* | support.atlassian.com/bitbucket-cloud |
| 모달 | *"In the Sync branch dialog, select the Sync strategy dropdown…"* | 같음 |
| 우측 상단 액션 | *"Select more actions () at the top-right, then select Export."* | support.atlassian.com/jira-service-management-cloud |
| 우측 상단 버튼 | *"Stripe displays a Refund button in the upper-right corner of the page."* | docs.stripe.com/connect/end-to-end-marketplace |
| 페이지 하단 | *"Click Save component at the bottom of the page to save your changes."* | support.atlassian.com/statuspage |

쓸 수 있는 컨테이너 이름: `좌측 사이드바` · `상단 탭` · `탭 아래 정보 배너` · `<이름> 다이얼로그` ·
`우측 상단 액션 메뉴(⋯)` · `페이지 하단` · `툴바` · `<섹션명> 섹션`.

## 4. 중간 단계 무생략

경로 표기는 `A > B > C` 로 **전 구간**을 쓴다. 한 단계라도 빠지면 사용자가 화면에서 못 찾는다.
실측: `General` 한 단계를 빠뜨려 경로 전체가 무효가 된 사례가 있다.

> *"Don't use bold on the greater-than symbol. Include a space before and after the symbol."*
> — learn.microsoft.com/en-us/style-guide/procedures-instructions/describing-interactions-with-ui

## 5. 분기 카탈로그 — 되묻기 전에 선제 제공

라벨이 다르거나 항목이 아예 없는 경우를 **미리** 붙인다. 이것은 변명이 아니라 1 급 공식 문서 관행이다.

**확정 정본은 `docs/howto/branch-catalog.md` 다.** 아래는 요약이며 조회일 2026-09-10 기준이다.

### 사유 6 종 — 각 행에 1 차 출처가 있다

| 사유 | 실제 문장 | 출처 |
| --- | --- | --- |
| 권한 / 역할 | *"If you can't see the filter's sharing configuration, you'll need your Jira administrator to give you the Create Shared Object global permission."* | Atlassian — support.atlassian.com/jira-service-management-cloud/docs/manage-filters/ |
| 권한 / 조직 정책 | *"Organizations that you are a member of will not appear if the organization has blocked the use of fine-grained personal access tokens."* | GitHub — docs.github.com/en/enterprise-cloud@latest/…/managing-your-personal-access-tokens |
| **기능 선행조건** | *"The Campaigns feature becomes available only after your app has received analytics data."* | Apple — developer.apple.com/help/app-store-connect-analytics/acquisition/campaign-links |
| 요금제 | *"If you don't see a fax number there, it means you're on a free plan."* | Dropbox — help.dropbox.com/account-settings/where-can-i-find-my-dropbox-fax-number |
| 버전 | *"On Windows 11, select Advanced network settings > Network reset. On Windows 10, select Status > Network reset."* | Microsoft — support.microsoft.com/…/fix-wi-fi-connection-issues-in-windows |
| A/B 롤아웃 | *"This feature is being rolled out gradually and may not be available in your account yet."* | Google — support.google.com/displayvideo/answer/17234167 |

**기능 선행조건은 2026-09-10 사이클에서 새로 식별한 유형이다.** 그동안 Apple 인용을 권한 분기
예시로 썼는데 원문에 권한 이야기가 없다. 권한도 요금제도 버전도 아니고 **아직 조건이 안 찬 것**이며,
대응은 요청도 결제도 아닌 **기다리기**다. 이 유형을 놓치면 "권한을 확인하세요" 라고 잘못 안내하게 된다.

권한을 둘로 나눈 것은 대응이 다르기 때문이다 — 개인 권한 부족은 관리자 요청으로 풀리지만,
조직 정책 차단은 요청해도 안 되고 정책 자체를 바꿔야 한다.

| 사유 | 사용자가 할 일 |
| --- | --- |
| 권한 / 역할 | 사람에게 요청 |
| 권한 / 조직 정책 | 정책 변경 (요청으로 안 됨) |
| 기능 선행조건 | **기다린다** |
| 요금제 | 업그레이드 |
| 버전 | 분기된 경로를 따라간다 |
| A/B 롤아웃 | 기다리거나 전역 검색어로 우회 |

### 언어/로케일은 사유가 아니라 다른 축이다

위 6 종은 "항목이 **없다**" 인데 언어는 "항목은 있는데 **이름이 다르다**" 다. 같은 목록에 두면
"언어 때문에 항목이 없다" 는 잘못된 안내가 나온다. 처리도 다르다 — 사유를 알려주는 것이 아니라
**라벨을 양쪽 다** 준다 (영문 정본 + 한국어 괄호 병기).

언어 분기 문장의 1 차 출처는 **확인 실패**다 — `references/provenance-notes.md` §7.

### 안 보임 vs 회색(비활성)

권한 부족의 표현형은 둘이다. "안 보인다" 만 안내하면 **회색으로 보이는** 사용자가 자기 케이스가
아니라고 판단하고 막힌다.

> *"If the Save button is greyed out in the Azure portal"* — 원인 제목 *"Insufficient RBAC permissions"*
> — learn.microsoft.com/en-us/troubleshoot/azure/virtual-machines/windows/cannot-extend-volume-windows-vm (확인 2026-09-08)

> *"If you don't see the option to grant permission, ask an admin to manually grant the permission
> through GitHub."* — learn.microsoft.com/en-us/azure/data-factory/source-control (확인 2026-09-08)

**한 문서가 "권한 부족은 숨김 또는 회색 둘 다 가능" 이라고 규정한 원문은 못 찾았다.** 위 둘을
합쳐 하나의 규칙으로 만든 것은 **이 킷의 종합**이지 외부 표준의 인용이 아니다.

## 6. 사이트 배정표 — 사이트가 갈리는 절차

"셋업은 전부 A 사이트" 같은 뭉뚱그림은 사용자가 **첫 화면에서** 막히게 한다. 어느 작업이 어느
사이트인지 사전 요구사항 **맨 위에** 표로 둔다.

| 도메인 | 갈리는 사이트 |
| --- | --- |
| Apple | 키·식별자 발급 = Developer Account (developer.apple.com) / 앱 레코드·빌드 업로드·TestFlight = App Store Connect (appstoreconnect.apple.com) |
| Google | GCP Console (console.cloud.google.com) ↔ Firebase Console (console.firebase.google.com) |
| 한국 행정 | 주민등록등본 = 정부24 / 가족관계증명서 = 대법원 전자가족관계등록시스템 / 소득금액증명 = 홈택스 |

Apple 은 이 함정의 원형이다 — FCM 을 붙이려고 App Store Connect 로 들어가면 **옵션 자체가 없다.**

## 7. 언어 라벨 — 영문이 정본, 한국어는 괄호

한국어 라벨은 번역 추정이다. 영문을 정본으로 쓰고 한국어를 괄호에 넣는다.

실측 대조: `Settings > General > About` ↔ `설정 > 일반 > 정보`
(support.apple.com/en-us/109065 ↔ support.apple.com/ko-kr/109065)

같은 문서의 로케일 변형 URL 이 있으면 그것이 한국어 라벨의 1 차 출처다. 없으면 한국어 라벨은
`[추정]` 이다.
