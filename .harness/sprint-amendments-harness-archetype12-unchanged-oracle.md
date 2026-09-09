# Amendments — harness-archetype12-unchanged-oracle

계약 본문은 봉인(`sha256:c335ef27bcb4405e`)되어 수정하지 않았다.

## AM-01 — relaxing · anchored

- 대상 조건: AR-04
- 변경: 허용 경로 pathspec 에 `docs` 를 **추가**한다 (5 경로 → 6 경로).
  - 원 pathspec: `harness CLAUDE.md flutter-toolkit .claude/skills .harness`
  - 개정 pathspec: 위 5 개 + `docs`
  - 제외 pathspec 은 그대로다: `':(exclude).claude/worktrees' ':(exclude)result.json'`
- 근거: 계약 작성 시 **생성 HTML 미러를 소비면으로 세지 않은 것**이 작성자의 실수다.
  AR-01 sweep 이 `docs/harness/skill-design-guide.html:224-225` 가 아직 `11 가지` 로
  적혀 있음을 잡아냈다. 소스 `.md` 만 고치면 docs-site 재생성이 조용히 되돌리므로
  (레포의 반복 결함), 짝으로 고쳐야 AR-01 의 목표가 성립한다.

  같은 이유로 `docs/harness/agent-design-guide.html` 도 소스와 짝으로 고쳤다 — 그쪽은
  **생성물이 소스보다 앞서 있던** 반대 방향의 드리프트였다 (HTML `:903` 은 훅 트리거를
  포함한 7 패턴, 소스 `:682` 는 6 패턴).

- direction 계산 (자기신고 아님):

  ```text
  $ amend_direction a_orig.txt a_new.txt
  relaxing added=1 removed=0
  ```

  **허용 집합 헬퍼 `amend_direction` 을 썼다.** AR-04 의 pathspec 은 "바꿔도 되는 경로" 의
  목록, 즉 허용 집합이다. 측정 집합 헬퍼를 쓰면 극성이 뒤집힌다.

- 근거 (redaction 거친 원문): 사용자가 선택지 "AR-04만 승인, AR-03 은 에이전트 카탈로그도
  같이 고침" 을 골랐다 — *"봉인된 AR-03 · AR-04 의 오라클 결함 2건을 어떻게 처리할까요?"* 에
  대한 응답.
- 앵커: 2026-09-09T15:07:15+09:00 · session=4d264694-eb0e-4e84-801f-52b2db804772 · cwd=/Users/jackson/Hub/10_Dev/claude-plugins

## AR-03 은 amendment 없이 통과했다

같은 질문에서 사용자가 **오라클을 고치지 말고 대상을 고치라**고 결정했다. 원 측정식
`grep -cE '[0-9]+ ?가지'` 가 오탐하던 2 건은 에이전트 디자인 패턴 카탈로그의 실제
드리프트였고(소스는 패턴 7 개인데 인용은 `6가지`·`5가지`), 그것을 고치자 7 파일 전부
0 이 됐다. 측정식은 원문 그대로 유지한다.
