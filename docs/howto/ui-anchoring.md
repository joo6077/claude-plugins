# UI 지목 어휘 — 방향어는 금지가 아니라 단독 사용 금지다

`last_updated: 2026-09-09`

절차 문서에서 화면의 요소를 어떻게 가리킬 것인가. 이 킷은 P5 를 **"방향어 대신 명명된 컨테이너"**
라고 써 왔다. 이번 사이클이 그 진술이 **근거보다 강했다**는 것을 확인하고 고친다.

---

## 1. 모순이 있었다

킷의 P5 는 Google 스타일 가이드를 근거로 방향어를 배제하라고 했다. 그런데 킷이 **근거로 인용한
벤더 지원 문서 8 건 중 4 건이 방향어를 쓴다.**

| 인용 | 방향어 |
| --- | --- |
| *"Click Network in the sidebar, then click the network service … **on the right**."* | `on the right` |
| *"Select more actions () **at the top-right**, then select Export."* | `at the top-right` |
| *"Stripe displays a Refund button **in the upper-right corner of the page**."* | `upper-right corner` |
| *"Click Save component **at the bottom of the page** to save your changes."* | `at the bottom` |

규칙이 맞다면 이 문장들은 전부 위반이다. 벤더 지원 문서가 죄다 틀렸을 리는 없으니, 규칙 쪽을
의심하는 것이 맞다.

---

## 2. Google 은 무엇을 말했나 — 완화 조건이 없다

> *"Don't use directional language to orient the reader, such as above, below, or right-hand side.
> Phrases like those don't work well for accessibility or for localization. If a UI element is hard
> to find, provide a screenshot."*
>
> Recommended: *"Click menu Menu."*
> Not recommended: *"In the left-side panel, click the button with three lines."*
>
> — developers.google.com/style/ui-elements (조회 2026-09-09)

**Google 은 예외를 명시하지 않는다.** 다만 "권장하지 않음" 예시를 보면 무엇을 겨냥하는지는
분명하다 — `the button with three lines` 는 **이름이 없다.** 방향어가 이름을 대신하고 있는 문장이다.
Google 의 대안은 이름(`menu Menu`)이고, 못 찾겠으면 **스크린샷**을 주라고 한다.

Google 만 근거로 삼으면 "방향어 금지" 로 읽을 수 있고, 실제로 이 킷이 그렇게 읽었다.

---

## 3. Microsoft 가 모순을 푼다 — `only clue`

Microsoft 스타일 가이드는 같은 문제를 다르게 규정한다. **금지의 단위가 "방향어" 가 아니라
"방향어만" 이다.**

> *"Don't use directional terms as the only clue to location. Left, right, up, down, above, and below aren't very useful for people who use screen-reading software. Instead, use specific language that conveys context, such as "the first item in the following list" or "on the toolbar.""*
>
> — learn.microsoft.com/en-us/style-guide/accessibility/writing-all-abilities (조회 2026-09-09)

그리고 허용 조건을 **두 개** 명시한다:

> *"Don't use directional terms (left, right, up, down) as the only clue to location. Individuals with cognitive impairments might have difficulty interpreting them, as might people who are blind and use screen-reading software."*
>
> **핵심 — 허용 조건:** *"It's OK to use a directional term if another indication of location, such as in the Save As dialog box, on the Standard toolbar, or in the title bar, is also included."*
>
> *"Directional terms are also OK to use when a sighted user with dyslexia can clearly see a change in the interface as the result of an action, such as a change in the right pane when an option in the left pane is selected."*
>
> — learn.microsoft.com/en-us/style-guide/a-z-word-list-term-collections/u/upper-left-upper-right (조회 2026-09-09)

정리하면:

| | 허용 | 예 |
| --- | --- | --- |
| 방향어 **단독** | ✗ | "오른쪽 위 버튼을 누르세요" |
| 방향어 **+ 다른 위치 단서** | ✓ | *"more actions () at the top-right"* — 요소 이름이 함께 있다 |
| 동작 결과로 **보이는 변화** | ✓ | *"a change in the right pane when an option in the left pane is selected"* |

§1 의 벤더 문장 4 건은 **전부 방향어에 이름이 붙어 있다.** 위반이 아니다. 모순이 해소된다.

---

## 4. Apple — `[미확인]`

Apple Style Guide 에서 동등한 금지 조항을 **확보하지 못했다.** Apple 은 방향어를 금지 대상이
아니라 **용법**으로 다룬다 (`left side` — `left-hand side` 를 쓰지 말라는 식). 시도한 URL 은
`howto-kit/references/provenance-notes.md` §6 에 있다.

킷의 처리: Apple 을 이 규칙의 근거로 인용하지 않는다.

---

## 5. 킷의 규칙은 어떻게 바뀌나

**약화가 아니다.** 단독 사용 금지는 그대로 강제한다. 바뀌는 것은 두 가지다.

1. **진술** — "방향어 **대신** 명명된 컨테이너" → "방향어를 **단독으로** 쓰지 않는다.
   위치 단서를 함께 준다."
2. **출처 귀속** — 완화 조건의 근거는 Google 이 아니라 **Microsoft** 다. Google 은 완화 조건을
   명시하지 않았으므로 Google 을 근거로 "이름과 함께면 된다" 고 말하면 그것이 과대 인용이다.

킷 내부는 이미 갈려 있었다 — 체크리스트와 `howto-reviewer` 의 R4 는 `~만으로`(단독)라고 옳게
썼는데 제목과 본문은 `~대신`(대체)이라고 썼다. 이번에 그 불일치를 없앤다.

### 쓸 수 있는 위치 단서

방향어와 짝지을 수 있는 것들이다. 이름 있는 컨테이너가 1 순위이고, 방향어는 그것을 **보조**한다.

```text
좌측 사이드바 · 상단 탭 · 탭 아래 정보 배너 · <이름> 다이얼로그
우측 상단 액션 메뉴(⋯) · 페이지 하단 · 툴바 · <섹션명> 섹션
```

### 그래도 못 찾으면 — 스크린샷

Google 이 제시하는 최후 수단이다. *"If a UI element is hard to find, provide a screenshot."*
이 킷의 등급 사다리에서 스크린샷은 `관측` 등급에 해당한다 — 사용자가 화면을 읽어 준 것과 같은
강도다.

---

## 6. 실측된 지목 어휘 — 재확인

조회일 **2026-09-09**. §1 의 4 건은 방향어를 포함하지만 전부 이름과 짝지어져 있어 위반이 아니다.

| 위치 | 실제 문장 | 출처 | 방향어 단독? |
| --- | --- | --- | --- |
| 좌측 사이드바 | *"Click Components from the left sidebar."* | support.atlassian.com/statuspage | 아니오 (`Components`) |
| 사이드바 + 상세 | *"Click Network in the sidebar, then click the network service that you're using (such as Wi-Fi) on the right."* | support.apple.com/102022 | 아니오 (`Network`) |
| 탭 | *"Click the Third-party tab."* | support.atlassian.com/statuspage | 방향어 없음 |
| 탭 아래 배너 | *"From the Commits tab, select Sync now in the info banner under the tabs."* | support.atlassian.com/bitbucket-cloud | 아니오 (`Sync now`) |
| 모달 | *"In the Sync branch dialog, select the Sync strategy dropdown…"* | 같음 | 방향어 없음 |
| 우측 상단 액션 | *"Select more actions () at the top-right, then select Export."* | support.atlassian.com/jira-service-management-cloud | 아니오 (`more actions`) |
| 우측 상단 버튼 | *"Stripe displays a Refund button in the upper-right corner of the page."* | docs.stripe.com/connect/end-to-end-marketplace | 아니오 (`Refund`) |
| 페이지 하단 | *"Click Save component at the bottom of the page to save your changes."* | support.atlassian.com/statuspage | 아니오 (`Save component`) |

**8 건 중 방향어 단독은 0 건이다.** 이것이 규칙의 실증이다.

---

## 7. 조회 기록

Codex 위임 1 회 (MODE=research · read-only · foreground · 검색 하드캡 20). rollout 로그의
`turn_aborted` 는 0 건으로 정상 완주했고, Google · Microsoft 원문을 확보했으며 Apple 동등 조항은
확인 실패로 반환했다.

Codex 가 **본문 fetch 에 실패한 Stripe 인용 1 건**은 세션 로컬 `curl` 로 해소했다
(`upper-right corner of the page` 문자열이 2.1MB 응답 본문에 존재).

인용 4 건(Google 1 · Microsoft 2 · Stripe 1)은 전부 응답 본문에서 직접 추출해 대조했다 —
위임 요약을 그대로 옮기지 않았다.

미확정 근거의 원장은 `howto-kit/references/provenance-notes.md` 가 정본이다. 확정된 항목은
이 문서가 정본이다.
