---
slug: flutter-catalog
created: "2026-10-09 15:05"
---

## A-01 — 측정용 핏팰 감싸개 두 개의 언어 준비 정정

**앵커**: 배경 「시험용 위젯 · 감싸개」 와 오류-01 · 스크립트-04~06 · 스크립트-09 · 구조-05 가 쓰는
측정 준비물 `.harness/.meta/flutter-catalog/fixtures/catalog_kit_host.dart` ·
`catalog_kit_app_host.dart` (봉인 커밋 `72d276b8` 뒤 측정 묶음 커밋 `d23c77d1` 의 판).

**무엇이 달라졌나**:

- `catalog_kit_host.dart` 의 `setUpHost` 가 `LocaleSettings.setLocaleRawSync(...)` 를 부르던 것을
  `await LocaleSettings.setLocaleRaw(...)` 로 바꿨다.
- `catalog_kit_app_host.dart` 의 `appWrap` 이 부르던 `LocaleSettings.setLocaleRawSync('ko')` 한 줄을 뺐다
  (기본 언어로 띄운다).

**왜**: 핏팰 번역(`slang`)은 언어 파일을 늦게 불러오는 방식이라 동기 함수로 언어를 바꾸면
`Deferred library l_ko was not loaded` 로 그 자리에서 죽는다(2026-10-09 14:2x 실측, 글꼴 시험 출력).
옛 판으로는 어떤 구현을 넣어도 시험 감싸개를 거치는 시험이 전부 그리기 전에 실패했다.
핏팰 앱 자신도 `await LocaleSettings.useDeviceLocale()` · 시험에서 `await LocaleSettings.setLocale(...)`
처럼 기다려서 부른다 — 측정 준비물이 앱과 다르게 쓰여 있었던 것이다.

**판정 기준은 그대로다**: 조건 줄 · 측정 줄 · `measure.sh` 의 판정식은 한 글자도 안 바꿨다.
`wrapper` 사례가 쓰는 맨 감싸개 `catalog_kit_host.bare.dart` 도 그대로다.

**amend_direction_oracle**: `relaxing` (계산) — 옛 준비물로는 감싸개를 거치는 조건의 통과 집합이
비어 있었고 새 준비물로는 비어 있지 않다. 집합이 늘었으니 규칙대로 느슨해지는 쪽으로 적는다.
기준을 낮춘 것이 아니라 돌릴 수 없던 준비물을 앱과 같은 호출로 고친 것이지만, 방향은 그 사정과
따로 계산한다.

**consent**: `anchored` — 2026-10-09 16:05 사용자가 A-01 · A-02 를 콕 집은 질문에 「둘 다 승인」 으로 답했다 (이 세션 질문 도구 응답).

## A-02 — 화면 점검 스크립트의 누르기를 좌표 누르기로 정정

**앵커**: 구조-05 · 진단-04 가 쓰는 `.harness/.meta/flutter-catalog/web_check.js` (측정 묶음 커밋 `d23c77d1` 의 판).

**무엇이 달라졌나**: 누르기 다섯 곳의 `.click()` 을 `.click({ force: true })` 로 바꿨다. 찾는 이름 · 단계 수 6 ·
단계마다의 전후 비교 · 화면 오류 0 건 · 끝 줄 판정은 그대로다.

**왜**: Flutter 3.47 웹은 겹친 화면 층마다 화면 전체를 덮는 빈 접근성 요소(`flt-semantics`, `pointer-events: auto`)를
뿌리 바로 아래에 둔다(2026-10-09 실측: 1440 × 900 요소 네 개, z-index 2~5). 실제 마우스 클릭은 이 요소를 거쳐
Flutter 화면으로 올라가 좌표로 처리되지만, playwright 의 기본 누르기는 「다른 요소가 가렸다」 며 30 초 기다린 뒤
포기한다. 옛 판으로는 어떤 놀이터를 띄워도 셋째 단계에서 실행 오류로 끝났다.
`force` 는 가림 확인만 건너뛰고 같은 좌표에 마우스 누르기를 보낸다 — 누른 뒤 화면이 바뀌었는지는 단계마다 따로 잰다.

**amend_direction_oracle**: `relaxing` (계산) — 옛 판의 통과 집합은 비어 있었고 새 판은 비어 있지 않다.

**consent**: `anchored` — 2026-10-09 16:05 A-01 과 같은 질문에서 「둘 다 승인」.
