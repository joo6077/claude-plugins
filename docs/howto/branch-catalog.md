# 선제 분기 카탈로그 — 항목이 안 보이는 사유는 몇 가지인가

`last_updated: 2026-09-10`

절차 문서는 "그 항목이 안 보일 수도 있다" 를 **되묻기 전에 미리** 붙여야 한다. 사용자가 화면에서
막힌 뒤에 "안 보이시나요?" 라고 되묻는 것은 이미 늦었다.

이 킷은 그 분기의 사유를 **5 종**으로 유형화해 놓았었다. 이번 사이클이 그 목록을 검증했고,
**둘이 틀렸다**는 것을 확인했다.

---

## 1. 무엇이 틀렸나

| 문제 | 내용 |
| --- | --- |
| 근거 부족 | 5 종을 주장했지만 실제 인용이 있던 것은 **권한 계열뿐**이었다. 나머지 4 종은 목록에만 있었다 |
| 유형 누락 | 기존 목록의 Apple 인용은 **권한 분기가 아니었다.** 읽어 보니 기능 선행조건 분기였다 |
| 축 혼동 | **언어**는 다른 사유들과 실패 모드가 다르다. 같은 목록에 둘 것이 아니다 |

근거 없이 목록을 늘려 놓은 것 자체가 이 킷이 막으려는 F3(최신성·근거 결여)다. 킷의 규칙을
킷 자신에게 먼저 적용한 결과가 이 문서다.

---

## 2. 확정된 분기 사유 6 종

조회일 **2026-09-10**. 각 행에 1 차 출처가 붙어 있다 — **출처 열이 빈 행은 없다.**

| 사유 | 실제 문장 | 벤더 | 출처 |
| --- | --- | --- | --- |
| **권한 / 역할** | *"If you can't see the filter's sharing configuration, you'll need your Jira administrator to give you the Create Shared Object global permission."* | Atlassian | support.atlassian.com/jira-service-management-cloud/docs/manage-filters/ |
| **권한 / 조직 정책** | *"Organizations that you are a member of will not appear if the organization has blocked the use of fine-grained personal access tokens."* | GitHub | docs.github.com/en/enterprise-cloud@latest/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens |
| **기능 선행조건** | *"The Campaigns feature becomes available only after your app has received analytics data."* | Apple | developer.apple.com/help/app-store-connect-analytics/acquisition/campaign-links |
| **요금제** | *"If you don't see a fax number there, it means you're on a free plan."* | Dropbox | help.dropbox.com/account-settings/where-can-i-find-my-dropbox-fax-number |
| **버전** | *"On Windows 11, select Advanced network settings > Network reset. On Windows 10, select Status > Network reset."* | Microsoft | support.microsoft.com/en-us/windows/experience/connectivity-networking/fix-wi-fi-connection-issues-in-windows |
| **A/B 롤아웃** | *"This feature is being rolled out gradually and may not be available in your account yet."* | Google | support.google.com/displayvideo/answer/17234167 |

권한을 둘로 나눈 것은 **대응이 다르기 때문**이다. 개인 권한 부족은 "관리자에게 요청" 이지만,
조직 정책 차단은 요청해도 안 되고 **정책 자체를 바꿔야** 한다.

### 2.1 기능 선행조건 — 새로 발견한 유형

기존 목록에 없던 사유다. Apple 인용은 그동안 권한 분기 예시로 쓰였는데, 원문을 끝까지 읽으면
권한 이야기가 전혀 없다.

> *"If you don't see a Campaigns tab or add button: The Campaigns feature becomes available only
> after your app has received analytics data. If your app is new or hasn't yet had any downloads,
> the add button (+) next to Campaigns may not appear. Continue checking after your app has been
> live and generating downloads for at least 24 hours."*
> — developer.apple.com/help/app-store-connect-analytics/acquisition/campaign-links (조회 2026-09-10)

권한도 요금제도 버전도 아니다. **아직 조건이 안 찼을 뿐**이고, 대응도 다르다 — 관리자에게
요청할 것도, 결제할 것도, 업그레이드할 것도 없다. **기다리는 것**이 답이다.

이 유형을 놓치면 절차 문서가 "권한을 확인하세요" 라고 잘못 안내하고, 사용자는 있지도 않은
권한 문제를 찾아 헤맨다.

### 2.2 사유별 전형적 대응

| 사유 | 대응 | 사용자가 할 일 |
| --- | --- | --- |
| 권한 / 역할 | "관리자에게 `<권한명>` 을 요청해야 보입니다" | 사람에게 요청 |
| 권한 / 조직 정책 | "조직이 이 기능을 차단했습니다 — 정책 변경이 필요합니다" | 정책 변경 (요청으로 안 됨) |
| 기능 선행조건 | "`<조건>` 이 충족된 뒤에 나타납니다" | **기다린다** |
| 요금제 | "무료 플랜에는 이 메뉴가 없습니다" | 업그레이드 |
| 버전 | "`<버전>` 이상에서는 A, 이하에서는 B" | 분기된 경로를 따라간다 |
| A/B 롤아웃 | 상위 섹션명 + 전역 검색어 제공 | 기다리거나 우회 |

---

## 3. 언어/로케일은 사유가 아니라 다른 축이다

**실패 모드가 다르다.**

| | 위 6 종 | 언어/로케일 |
| --- | --- | --- |
| 증상 | 항목이 **없다** | 항목은 **있는데 이름이 다르다** |
| 사용자 경험 | 아무리 찾아도 못 찾는다 | 찾긴 찾는데 문서와 안 맞아 확신을 못 한다 |
| 해법 | 사유를 알려주고 대응을 안내 | **라벨을 양쪽 다** 준다 |

같은 목록에 두면 "언어 때문에 항목이 없다" 는 잘못된 안내가 나온다. 그래서 이 문서는 언어를
사유 목록에서 빼고 별도 축으로 둔다.

**언어 분기 문장의 1 차 출처는 확보하지 못했다** — `[미확인]`. 시도한 URL 은
`howto-kit/references/provenance-notes.md` §7 에 있다.

킷의 처리는 바뀌지 않는다: 영문 라벨을 정본으로 두고 한국어를 괄호에 병기한다. 이것은 킷의
운영 규약이지 외부 표준의 인용이 아니다.

---

## 4. 안 보임 vs 회색(비활성)

권한 부족의 표현형은 둘이다. 절차 문서가 "안 보인다" 만 안내하면, **회색으로 보이는** 사용자는
자기 케이스가 아니라고 판단하고 막힌다.

| 표현형 | 근거 |
| --- | --- |
| 항목이 **안 보인다** | Atlassian — *"If you can't see the filter's sharing configuration…"* |
| 보이되 **회색/비활성** | Microsoft — *"If the Save button is greyed out in the Azure portal"*, 원인 제목 *"Insufficient RBAC permissions"* |

**한 문서가 "권한 부족은 숨김 또는 회색 둘 다 가능" 이라고 한 문장으로 규정한 원문은 찾지
못했다.** 위 둘은 서로 다른 벤더의 문서이고, 둘을 합쳐 하나의 규칙으로 만든 것은 **이 킷의
종합**이다 — 외부 표준의 인용이 아니다. 그렇게 표기한다.

---

## 5. 선제 분기를 규정한 스타일 가이드 조항 — `[미확인]`

"절차 문서에 선제 분기 문장을 쓰라" 고 **규정한** 스타일 가이드 조항을 확보하지 못했다.
Google · Microsoft 양쪽에서 실패했다.

그러므로 이 킷의 P6("분기를 되묻기 전에 선제 제공한다")는 **관행의 귀납**이지 표준의 인용이
아니다. 근거는 위 §2 의 벤더 문서 6 건이 실제로 그렇게 쓴다는 사실이다. 그 구분을 흐리지 마라.

---

## 6. 검증 함정 — HTML 엔티티 때문에 대조가 실패한다

Dropbox 인용은 1 차 대조에서 **MISS** 였다. 페이지는 정상이었고 문장도 있었다. 원인은
아포스트로피가 원문에 **HTML 엔티티로 들어 있던 것**이다.

```text
검색한 문자열:  you're on a free plan
응답 본문 원문:  you&#39;re on a free plan
```

`curl | grep -F` 로 대조하면 이런 인용은 전부 "없음" 으로 나온다. **엔티티를 디코드한 뒤
대조하라.** 그러지 않으면 멀쩡한 1 차 출처를 "확인 실패" 로 잘못 기록하게 된다 — 이 킷에서는
그것이 가장 비싼 오류다.

같은 계열의 함정이 이미 둘 더 있다:

- `developer.apple.com` **문서는 SPA** — HTML 에 본문이 없다. `tutorials/data/documentation/<경로>.json`
  을 써라 (`docs/howto/deep-links.md` §3).
- **Apple Style Guide 는 PDF** — 폰트 서브셋 인코딩 때문에 정규식으로는 안 잡힌다. `pdftotext`
  로 추출하라 (`provenance-notes.md` §6).

**공통 규칙**: "문자열을 못 찾았다" 는 **확인 실패이지 부재가 아니다.** 도구를 바꿔 한 번 더
시도한 뒤에 판정하라.

---

## 7. 조회 기록

Codex 위임 1 회 (MODE=research · read-only · foreground · 검색 하드캡 20). rollout 로그의
`turn_aborted` 는 0 건으로 정상 완주했다. 기존 3 건 재확인 · 신규 3 종 확보 · 언어와 스타일
가이드 조항은 확인 실패로 반환했다.

인용 6 건은 전부 세션 로컬 `curl` 로 응답 본문에서 직접 대조했다. 1 차 대조 결과는
**5 HIT / 1 MISS** 였고, MISS 1 건의 원인이 §6 의 HTML 엔티티였다.

미확정 근거의 원장은 `howto-kit/references/provenance-notes.md` 가 정본이다. 확정된 항목은
이 문서가 정본이다.
