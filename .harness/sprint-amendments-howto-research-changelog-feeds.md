# Amendments — howto-research-changelog-feeds

계약 본문은 봉인(`sha256:ca745849209eb9d6`)되어 수정하지 않았다. 아래는 "이 조건을 이렇게
읽어라" 를 덧붙인 것이다.

## AM-01 — narrowing · unanchored

- 대상 조건: AR-03
- 변경: 측정 명령의 awk 를 **범위 형태에서 플래그 형태로** 교체한다.
  - 원 오라클: `awk '/^## 이 킷이 사실로 말하지 않는 것/,/^## /' howto-kit/README.md`
  - 개정 오라클: `awk '/^## 이 킷이 사실로 말하지 않는 것/{f=1;print;next} f&&/^## /{exit} f' howto-kit/README.md`
- 근거: 원 오라클은 **작동하지 않는다.** awk 의 범위 패턴은 시작 줄에서 종료 패턴도 함께
  검사하는데, 시작 줄 `## 이 킷이 사실로 말하지 않는 것` 이 종료 패턴 `^## ` 에도 매치되므로
  범위가 그 줄에서 즉시 닫힌다. 실행 결과 출력이 **헤더 1 줄**뿐이라 섹션 본문을 전혀 재지
  못한다. 개정 오라클은 헤더를 출력에 유지한 채 다음 `## ` 직전까지 읽는다.

  ```text
  $ awk '/^## 이 킷이 사실로 말하지 않는 것/,/^## /' howto-kit/README.md | wc -l
  1
  $ awk '/^## 이 킷이 사실로 말하지 않는 것/{f=1;print;next} f&&/^## /{exit} f' howto-kit/README.md | wc -l
  9
  ```

- direction 계산 (자기신고 아님 — 측정 집합 전용 헬퍼 사용):

  ```text
  $ amend_direction_oracle oracle_orig.txt oracle_new2.txt
  narrowing measured_removed=0 measured_added=5
  ```

  측정 집합에서 **빠지는 줄이 0** 이고 5 줄이 새로 측정 대상에 들어온다. 순수 추가이므로
  `narrowing` 이다 — 통과하는 구현의 집합이 줄어든다. 헬퍼는 `amend_direction` 이 아니라
  **`amend_direction_oracle`** 을 썼다. 이 amendment 가 바꾸는 것은 허용 집합이 아니라
  측정 집합이며, 두 헬퍼는 극성이 반대다.

  (참고: 헤더 줄을 출력에서 빼는 형태로 고쳤을 때는 같은 헬퍼가
  `relaxing measured_removed=1 measured_added=5` 를 돌려줬다. 측정에서 한 줄이라도 빠지면
  보수적으로 완화로 보기 때문이다. 그래서 헤더를 유지하는 형태로 다시 잡았다.)

- 근거 (redaction 거친 원문): 없음 — 사용자 발언에서 비롯된 변경이 아니다.
- 앵커: **없음 (`unanchored`)** — 구현 중 에이전트가 오라클 결함을 직접 발견해 제안한 변경이다.
  reflect-kit prompt 로그에 대응하는 사용자 발언이 없으므로 앵커를 지어내지 않는다.
  `narrowing · unanchored` 는 제약을 강화하는 방향이라 PASS 근거로 쓸 수 있다
  (contract-schema §Amendment 사이드카 direction × consent 표).

### 같은 결함을 갖지 않는 조건

AR-02 의 오라클 `awk '/^## 3\./,/^## 4\./'` 은 시작·종료 패턴이 서로 달라 범위가 즉시 닫히지
않는다. 실행해서 §3 블록 전체를 반환하는 것을 확인했으므로 amendment 대상이 아니다.

## AM-02 — relaxing · anchored

- 대상 조건: AR-09
- 변경: 허용 경로 pathspec 에 `.harness` 를 **추가**한다 (5 경로 → 6 경로).
  - 원 pathspec: `docs/howto docs/howto-kit docs/index.html howto-kit .claude/skills/howto-research`
  - 개정 pathspec: 위 5 개 + `.harness`
  - 제외 pathspec 은 그대로다: `':(exclude).claude/worktrees' ':(exclude)result.json'`
- 근거: 계약 작성 시 `.harness` 를 빠뜨린 것이 **작성자의 실수**다. 이 레포는 스프린트 계약을
  같은 PR 에 커밋하는 관례를 갖는다 — 직전 4 개 커밋 중 3 개가 `.harness/` 파일을 포함한다.

  ```text
  5625a10 docs: 미러 2건 동기화                      .harness 파일: 0
  50b31a7 feat(howto-kit): 절차 안내 킷 v0.1.0        .harness 파일: 6
  540dfee feat(harness): amend_direction_oracle       .harness 파일: 2
  fc9e0af fix(onboarding-kit): 게이트 결함 3건        .harness 파일: 2
  ```

- direction 계산 (자기신고 아님):

  ```text
  $ amend_direction allow_orig.txt allow_new.txt
  relaxing added=1 removed=0
  ```

  **허용 집합 헬퍼 `amend_direction` 을 썼다.** AR-09 의 pathspec 은 "재는 것" 이 아니라
  "바꿔도 되는 경로" 의 목록, 즉 허용 집합이다. 허용 경로가 1 개 늘었으므로 PASS 하는 구현의
  집합이 커진다 → `relaxing`. 측정 집합 헬퍼(`amend_direction_oracle`)에 같은 입력을 넣으면
  `narrowing` 이 나오는데, 그것이 스키마가 경고한 **극성 반전 오라벨**이다. 이 amendment 는
  허용 집합 변경이므로 `amend_direction` 이 맞다.

- 근거 (redaction 거친 원문): 사용자가 선택지 "함께 커밋 + relaxing 승인 (권장)" 을 골랐다 —
  *"스프린트 계약 파일 2개(.harness/sprint-contract-*.md, sprint-amendments-*.md)를 이번
  브랜치에 함께 커밋할까요?"* 에 대한 응답.
- 앵커: 2026-09-09T12:41:52+09:00 · session=4d264694-eb0e-4e84-801f-52b2db804772 · cwd=/Users/jackson/Hub/10_Dev/claude-plugins
  (AskUserQuestion 응답으로 기록된 명시적 승인. `relaxing` 의 승인 주체는 사용자뿐이며
  이 항목이 그 근거다.)
