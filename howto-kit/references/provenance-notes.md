# 이 킷이 사실로 말하지 않는 것 — 미확정 근거 원장

이 킷은 절차 안내에서 **확인 못 한 것을 확인한 척하지 않는 것**을 요구한다. 그 요구를 킷 자신에게
먼저 적용한 결과가 이 파일이다. 아래 항목은 킷의 규칙에 영향을 주지만 1 차 출처를 확보하지
못했다. **인용할 때 반드시 등급 표기를 함께 쓴다.**

조회 기록:

- 2026-09-08 — Codex 위임 리서치 1 회 (read-only). 원문 로그는
  `~/.claude/plugins/data/codex-openai-codex/state/claude-plugins-*/jobs/task-mts2e4by-exu3bg.log`
  및 자동 수집본 `~/.claude/codex-research-log/2026-09.md`.
- 2026-09-09 — `changelog-feeds` 사이클. §3 의 확정분 5 건이
  `docs/howto/changelog-feeds.md` 로 이관됐다.

---

## 1. 체크리스트 방법론 — `[미확인]`

**영향받는 규칙**: Step Contract 의 `mode: READ_DO | DO_CONFIRM` 필드
(`step-contract.md` §mode), 그리고 설계 브리프가 언급한 "한 묶음 5~9 항목 상한" ·
"killer item" 표시.

| 항목 | 상태 | 근거 |
| --- | --- | --- |
| Degani & Wiener, *Human Factors of Flight-Deck Checklists: The Normal Checklist*, NASA-CR-177549 (1990) — **문서의 존재** | 확인됨 | ntrs.nasa.gov/archive/nasa/casi.ntrs.nasa.gov/19910017830.pdf — *"Human factors of flight-deck checklists: The normal checklist"*, *"Report Number: NASA-CR-177549"* |
| (a) READ-DO vs DO-CONFIRM 의 **원 정의 문장** | **확인 실패** | 아래 시도 URL 참조 |
| (b) 한 묶음 **5~9 항목 상한**의 1 차 출처 | **확인 실패** | 같음 |
| (c) **killer item** 용어의 정의 원문 | **확인 실패** | 같음 |

시도했으나 원문 문장을 얻지 못한 URL:

```text
https://ntrs.nasa.gov/citations/19910017830
https://ntrs.nasa.gov/archive/nasa/casi.ntrs.nasa.gov/19910017830.pdf
https://ntrs.nasa.gov/api/citations/19910017830/downloads/19910017830.pdf
https://doi.org/10.1177/001872089303500209
https://books.google.com/books?id=x3IcTjuj4uIC          (Gawande, The Checklist Manifesto)
```

**킷의 처리**: `READ_DO` / `DO_CONFIRM` 두 값은 **이 킷의 운영 어휘로 유지**하되, 그 구분을
외부 표준이나 특정 저작의 정의로 **인용하지 않는다**. "5~9 항목" 과 "killer item" 은 킷의 규칙에
넣지 않았다 — 근거 없이 숫자를 규칙으로 만들면 그것 자체가 이 킷이 막으려는 F3 다.

`step-contract.md` 의 `mode` 표에 이 파일을 가리키는 등급 주석이 달려 있다.

---

## 2. Microsoft Learn 권한 관련 인용 — 1 건 확정 · 1 건 `[미확인]`

**영향받는 규칙**: `navigation-anchors.md` §5 분기 카탈로그의 "권한/역할" 사유 근거.

| 인용 | 상태 | URL |
| --- | --- | --- |
| *"If you don't see the option to grant permission, ask an admin to manually grant the permission through GitHub."* | **확인됨 2026-09-08** | learn.microsoft.com/en-us/azure/data-factory/source-control |
| *"If you're missing permissions, the resource group is greyed out"* | **확인 실패** | 아래 참조 |
| (대체 근거) *"If the Save button is greyed out in the Azure portal"* — 원인 제목 *"Insufficient RBAC permissions"* | **확인됨 2026-09-08** | learn.microsoft.com/en-us/troubleshoot/azure/virtual-machines/windows/cannot-extend-volume-windows-vm |

`resource group … greyed out` 문장을 찾지 못한 시도 URL:

```text
https://learn.microsoft.com/en-us/troubleshoot/azure/virtual-machines/windows/cannot-extend-volume-windows-vm
https://learn.microsoft.com/en-us/answers/questions/5634426/my-resource-group-not-deleting-but-i-cant-access-p
https://learn.microsoft.com/en-us/answers/questions/2201392/move-resources-to-new-subscription-getting-error
```

**킷의 처리**: 확인된 2 건만 근거로 쓴다. 설계 브리프가 지적한 `%20` 깨진 URL 문제는
첫 번째 인용에서 해소됐다 — 정상 URL 은 위 표의 것이다.

---

## 3. 변경 로그 폴링 대상 — 3 건 `[미확인]`

**영향받는 규칙**: `howto-research` 스킬의 폴링 대상 (최신성 축).

**확정된 피드는 이 원장이 아니라 `docs/howto/changelog-feeds.md` 가 정본이다.** 2026-09-09
사이클에서 5 건이 루트 엘리먼트 실측으로 확정되어 그리로 옮겨졌다. 여기 남은 것은 확인하지
못한 3 건뿐이다.

| 대상 | 상태 | HTML 폴링 대체 |
| --- | --- | --- |
| Firebase release notes | **확인 실패** | `https://firebase.google.com/support/releases` |
| Stripe changelog | **확인 실패** | `https://docs.stripe.com/changelog` |
| Azure updates | **확인 실패** | `https://azure.microsoft.com/en-us/updates/` |

피드를 찾지 못한 시도 URL (2026-09-08 · 2026-09-09 누적):

```text
https://firebase.google.com/feeds/support-release-notes.xml
https://firebase.google.com/feeds/firebase-release-notes.xml
https://firebase.google.com/support/releases.xml                  (200 이지만 text/html — soft 200)
https://docs.stripe.com/changelog.atom
https://docs.stripe.com/changelog.rss
https://stripe.com/blog/feed.rss
https://docs.stripe.com/changelog/feed.xml
https://docs.stripe.com/changelog/rss.xml
https://azure.microsoft.com/en-us/updates/feed/                   (301 → HTML)
https://www.microsoft.com/releasecommunications/api/v2/azure/rss  (403)
https://azurecomcdn.azureedge.net/en-us/updates/feed/             (200 이지만 image/vnd.microsoft.icon)
```

**킷의 처리**: 세 대상은 RSS 가 있다고 말하지 않는다 — HTML changelog 를 폴링 대상으로 적었다.
**"확인 실패" 를 "피드 없음" 으로 승격하지 않는다.** autodiscovery 링크 부재는 피드 부재의
근거가 못 된다는 반례를 2026-09-09 사이클이 확보했기 때문이다 (AWS — `docs/howto/changelog-feeds.md` §3).
Azure 의 `403` 은 접근 차단이지 부재 증명이 아니다.

---

## 4. `howto-kit` 이름 충돌 검사 — `[미확인]`

npm · GitHub · 공개 플러그인 마켓플레이스에서 `howto-kit` exact-name 충돌 여부를
**확정하지 못했다.** 시도 URL:

```text
https://www.npmjs.com/package/howto-kit
https://registry.npmjs.org/howto-kit
https://github.com/search?q=howto-kit&type=repositories
```

**현재 결과는 "확인된 충돌 없음"이 아니라 "확인 실패"다.** 이 레포의
`.claude-plugin/marketplace.json` 안에서는 충돌이 없음을 로컬로 확인했다 (2026-09-08).
외부 생태계 충돌은 미확인 상태로 남는다. 이름을 바꿔야 할 근거가 나오면
아직 배포 전이므로 변경 비용은 낮다.

---

## 5. 딥링크 함정 2 건 — `[미확인]`

**영향받는 규칙**: `navigation-anchors.md` §2 의 "계정 슬롯을 조심하라" 와 Firebase 자리표시자 표기.
확정분은 `docs/howto/deep-links.md` 가 정본이다.

| 항목 | 상태 | 킷의 처리 |
| --- | --- | --- |
| Google 계정 인덱스 `/u/0/` 가 다중 계정에서 다른 계정으로 리다이렉트된다는 **공식 문장** | **확인 실패** | 슬롯을 빼고 안내하는 규칙은 유지하되, 근거를 "Google 이 그렇게 문서화했다" 고 말하지 않는다 |
| Firebase `_` 가 프로젝트 id 자리표시자라고 **설명하는 문장** | **확인 실패** | URL 안에 `project/_/` 가 등장하는 것만 확정. 관행 설명은 `[추정]` 으로 표기한다 |

시도했으나 근거 문장을 얻지 못한 URL · 검색:

```text
https://support.google.com/accounts/answer/1721977                     (200 이지만 /u/N 표기 없음)
site:support.google.com OR site:developers.google.com "/u/0/" "account" "redirect"
https://firebase.google.com/docs/reference/admin/node/firebase-admin.auth.decodedidtoken
```

## 6. Apple 의 방향어 규정 — `[미확인]`

**영향받는 규칙**: `navigation-anchors.md` §3 · `skills/howto` Gotcha 5 의 근거 목록.
확정분은 `docs/howto/ui-anchoring.md` 가 정본이다.

Apple Style Guide 에서 "방향어를 위치 단서로 단독 사용하지 마라" 에 **동등한 조항을 확보하지
못했다.** Apple 은 방향어를 금지 대상이 아니라 **용법**으로 다룬다 (`left side` — `left-hand side`
를 쓰지 말라는 식). 시도 URL:

```text
https://support.apple.com/guide/applestyleguide/welcome/web
https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf
```

**킷의 처리**: Apple 을 이 규칙의 근거로 인용하지 않는다. 근거는 Microsoft(완화 조건 포함)와
Google(완화 조건 없음) 둘뿐이다.

---

## 이 원장을 쓰는 법

- 킷의 다른 파일이 위 항목을 언급할 때는 **이 파일을 가리키고** 등급을 함께 적는다.
- 항목이 확정되면 이 파일에서 확정 사실로 옮기고, 근거를 인용한 파일도 **같이** 고친다.
  한쪽만 고치면 옛 등급 표기가 남는다.
- 새 미확정 항목이 생기면 여기에 추가한다. 킷 파일 안에 흩어 놓지 않는다.
