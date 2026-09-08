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

| 서비스 | 공식 문서에 등장하는 형태 | 출처 |
| --- | --- | --- |
| Firebase | `console.firebase.google.com/project/_/settings/general/…` (`_` = 프로젝트 id 자리) | firebase.google.com 문서 내 딥링크 |
| Google Cloud | `console.cloud.google.com/<서비스>` + `?project=` | cloud.google.com |
| Apple | *"replace `[Team ID]` in the following URL with your Team ID: `https://appstoreconnect.apple.com/teams/[Team ID]/access/ci/…`"* | developer.apple.com/documentation/xcode/understanding-infrastructure-validation-builds |
| Stripe | `dashboard.stripe.com/test/apikeys` — *"MODE: Use `test` for sandboxes … or omit a value for live mode"* | docs.stripe.com/keys · docs.stripe.com/stripe-apps/deep-links |
| GitHub | `github.com/settings/personal-access-tokens/new` | docs.github.com |

**Stripe 는 모드가 URL 로 갈린다** — `dashboard.stripe.com/test/…`(test) ↔ `dashboard.stripe.com/…`(live).
잘못된 모드의 화면을 열면 키가 안 보인다.

### 계정 슬롯을 조심하라

`/u/0/` 같은 계정 인덱스를 임의로 박으면 **다른 계정으로 리다이렉트된다.** 계정이 여럿일 수 있으면
슬롯을 빼고 안내한다.

### 딥링크가 없으면 전역 검색어를 준다

대부분의 콘솔에 상단 검색창이 있다. 메뉴 트리를 외우게 하는 것보다 검색어 하나가 강하다.

> *"The Search bar at the top in the Google Cloud console is an efficient way to search for various
> product services, documentation pages, tutorials and even Google Cloud Resources"*
> — cloud.google.com/blog/topics/developers-practitioners/tips-get-most-out-google-cloud-documentation

## 3. 화면 지목 어휘 — 방향어 대신 명명된 컨테이너

> *"Don't use directional language to orient the reader"* / *"Add context to help the user find the element."*
> — developers.google.com/style/ui-elements

`위쪽` · `아래` · `오른편` 은 화면 크기와 레이아웃에 따라 달라진다. **이름 있는 영역**을 쓴다.

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

> *"If you don't see a Campaigns tab or add button…"* — Apple
> *"If you can't see the filter's sharing configuration, you'll need your Jira administrator to give
> you the Create Shared Object global permission."* — Atlassian
> *"Organizations that you are a member of will not appear if the organization has blocked…"* — GitHub
> *"If you don't see the option to grant permission, ask an admin to manually grant the permission
> through GitHub."* — learn.microsoft.com/en-us/azure/data-factory/source-control (확인 2026-09-08)
> *"If the Save button is greyed out in the Azure portal"* — 원인 제목 *"Insufficient RBAC permissions"*
> — learn.microsoft.com/en-us/troubleshoot/azure/virtual-machines/windows/cannot-extend-volume-windows-vm (확인 2026-09-08)

권한 부족의 표현형은 **두 가지**다 — 항목이 아예 **안 보이거나**, 보이되 **회색(비활성)** 이다.
분기 문장을 쓸 때 둘을 구분하라. "안 보인다"만 안내하면 회색 상태인 사용자가 자기 케이스가
아니라고 판단하고 막힌다.

분기 사유 5 종과 전형적 대응:

| 사유 | 전형적 대응 |
| --- | --- |
| 권한 / 역할 | "관리자에게 `<권한명>` 을 요청해야 보입니다" |
| 요금제 | "무료 플랜에는 이 메뉴가 없습니다" |
| 버전 | "`<버전>` 이상에서는 A, 이하에서는 B" |
| 언어 | 영문 라벨을 정본으로, 한국어를 괄호에 |
| A/B 롤아웃 | 상위 섹션명 + 전역 검색어 제공 |

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
