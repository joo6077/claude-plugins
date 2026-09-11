# Amendments — howto-kaizen-g4-precision

계약 본문은 봉인(`sha256:bcf7e7535ec1a339`)되어 수정하지 않았다.

## AM-01 — narrowing · unanchored

- 대상 조건: SC-03
- 변경: eval 케이스 수 기대값을 **15 → 16** 으로 읽는다.
- 근거: QA(Iteration 1)가 **SC-02 를 FAIL** 로 판정했다. 계약이 양성 3 종의 세 번째를
  `폐지 예정` 리터럴로 요구했는데 산출물에 그 픽스처가 없었고, 7 번째 슬롯을 기존
  `fail-g4-deprecation-ko.md`(`지원 종료`)로 채웠기 때문이다.

  그 지적을 수용해 `fail-g4-korean-abolish-unsourced.md` 를 추가하고 `E16` 으로 등록했다.
  그 결과 케이스가 하나 늘어 SC-03 의 리터럴 15 와 충돌한다. **SC-02 를 고치면 SC-03 이
  깨지는 구조**이므로 둘 중 하나는 사이드카로 읽어야 한다.

- direction 계산 (자기신고 아님):

  ```text
  $ amend_direction_oracle ev_orig.txt ev_new.txt
  narrowing measured_removed=0 measured_added=1
  ```

  **측정 집합 헬퍼 `amend_direction_oracle` 을 썼다.** eval 케이스 목록은 "재는 것의 집합"
  이다. 케이스가 하나 늘면 통과하는 구현의 집합이 **줄어든다** — 순수 추가이므로 `narrowing`.

  **정규화 기준을 밝힌다 (QA Iteration 2 지적).** 비교 단위를 무엇으로 두느냐에 따라 결과가
  갈린다. 이번 사이클에서 `E13` 의 id 를 개명했기 때문이다.

  ```text
  raw id 로 비교        relaxing measured_removed=1 measured_added=2   ← 개명이 삭제+추가로 보인다
  behavior 튜플로 비교  narrowing measured_removed=0 measured_added=1
  ```

  **behavior 튜플**(`fixture` + `expect_final` + `assertions`)이 맞는 단위다. id 는 사람이 읽는
  라벨이고 게이트가 재는 것은 튜플이기 때문이다. 개명은 측정 대상을 바꾸지 않는다.
  **id 를 비교 단위로 쓰면 개명이 방향을 뒤집는다** — 다음 사이클의 자문으로 남긴다.

- 근거 (redaction 거친 원문): 없음 — QA 판정을 수용한 변경이지 사용자 발언에서 비롯된 것이 아니다.
- 앵커: **없음 (`unanchored`)** — `narrowing` 은 제약을 강화하는 방향이라 PASS 근거로 쓸 수 있다
  (contract-schema §Amendment 사이드카 direction × consent 표). 앵커를 지어내지 않는다.

## AM-02 — narrowing · unanchored

- 대상 조건: ER-01 · ER-02
- 변경: 두 조건이 서술하는 **해법이 반대로 뒤집혔다.** 계약 작성 시점에는 "`확인:` 줄 제외가
  해법" 이라고 적었으나, QA 적대적 탐색이 그 해법의 사각지대를 실측으로 보였다 —
  `확인:` 에만 조작된 주장을 적으면 출처와 무관하게 **항상 통과**한다.

  면제를 **되돌렸다.** 대신 데이터 보존 안내는 이 킷의 기존 저작 규약(`출처:` 줄 주석)으로
  통과시킨다. 문서(`docs/howto/deprecation-policy.md` §7.1)도 그 결론으로 다시 썼다.

- direction: 게이트가 **더 많이 잡는** 방향이다 (면제 철회). 통과하는 구현의 집합이 줄어드므로
  `narrowing`. 실측: 조작된 `확인:` 주장이 면제 상태에서 `PASS` → 철회 후 `FAIL`.
- 근거 (redaction 거친 원문): 없음 — QA 판정 수용.
- 앵커: **없음 (`unanchored`)**. 2026-09-10T15:51:48+09:00 · session=4d264694-eb0e-4e84-801f-52b2db804772 ·
  cwd=/Users/jackson/Hub/10_Dev/claude-plugins

### 자기 평가

이번 사이클의 Surface A 는 **과교정이었다.** 직전 QA 가 원래 동작을 "방어 가능, 라벨만 부정확"
이라고 판정했는데, 그것을 오탐으로 읽고 필드를 통째로 면제했다. 게이트의 목적이 "출처보다 강한
주장 금지" 인데 한 필드를 면제하는 것은 목적과 반대 방향이다. 다음 사이클의 자문으로 남긴다.


## AM-03 — narrowing · unanchored

- 대상 조건: SK-01
- 변경: 계약은 게이트가 `- 확인:` 줄을 주장 탐지에서 **제외한다**고 요구했다. 그 요구를
  **따르지 않는다** — 반대로 제외하지 않는다.
- 근거: AM-02 와 같은 사유다. QA Iteration 1 이 면제의 사각지대를 실측으로 보였고
  (`확인:` 에만 조작된 주장 + 무관한 출처 → `PASS`), 그것을 수용해 되돌렸다.

  AM-02 가 `ER-01`·`ER-02` 만 대상으로 선언해 `SK-01` 이 덮이지 않았다. QA Iteration 2 가
  그 누락을 잡았다 — *"FAIL 을 흡수할 amendment 가 없다"*. 맞는 지적이라 이 항목을 추가한다.

- direction 계산 (자기신고 아님 — 주장 탐지가 스캔하는 **필드 집합**을 비교):

  ```text
  원   스텝헤더 · 무엇을 · 동작 · 값 · 안보이면 · 자유서술          (확인 제외)
  개정 위 6 개 + 확인

  $ amend_direction_oracle fld_orig.txt fld_new.txt
  narrowing measured_removed=0 measured_added=1
  ```

  스캔 필드가 **늘어난다** = 게이트가 더 많이 잡는다 = 통과하는 구현의 집합이 줄어든다.
  순수 추가이므로 `narrowing`. 실측 대조: 같은 조작 픽스처가 면제 상태에서 `PASS`,
  철회 후 `FAIL`.

- 근거 (redaction 거친 원문): 없음 — QA 판정 수용이지 사용자 발언에서 비롯된 것이 아니다.
- 앵커: **없음 (`unanchored`)**. 2026-09-11T11:19:17+09:00 · session=4d264694-eb0e-4e84-801f-52b2db804772 ·
  cwd=/Users/jackson/Hub/10_Dev/claude-plugins

  `narrowing · unanchored` 는 제약을 강화하는 방향이라 PASS 근거로 쓸 수 있다.
