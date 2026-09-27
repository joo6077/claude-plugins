---
slug: after-0926-orchestrator-docs
created: "2026-09-27"
---

## AM-01 — narrowing

- 대상 조건: SK-11
- 변경: 기대값을 `rules=69 read=69 unread=0` → `rules=79 read=79 unread=0` 으로, 망가뜨린 사본(D-04 강도 칸 `기타 (메모)`)의 기대값을 `rules=69 read=68 unread=1` → `rules=79 read=78 unread=1` 로 읽는다. 음성 대조를 하나 더한다 — `tone-kit/references/core-antipatterns.md` A 행 강도 칸 `MUST` 를 `필수` 로 바꾼 사본에서 `rules=79 read=78 unread=1` 과 `UNREAD core-antipatterns.md:A 필수` 가 나와야 한다. 측정 도우미 `tone.sh` 와 그 지문(`c6b5712616713339`)은 그대로 쓴다
- 까닭: 독립 검토가 69 는 번호 달린 행(`[A-Z]+-[0-9]+`)만 센 값이라 `core-antipatterns.md` 강도 표의 A ~ J 열 행이 통째로 빠진다고 짚었다(재현: A 행을 망가뜨려도 `rules=69 read=69 unread=0`). 블록이 강도 머리 아래 모든 행을 세도록 고치면 69 로는 통과할 수 없다. 조건 문구 69 는 그 구멍을 봉인한 값이었다
- 방향 계산 — 측정 집합(블록이 판정한 `파일:행` 목록)을 `amend_direction_oracle` 에 넣었다. 원 집합은 가지 끝 `b0dcf7d` 의 블록, 개정 집합은 고친 블록을 같은 저장소 폴더에 돌려 뽑았다

  ```text
  $ amend_direction_oracle old-set.txt new-set.txt
  narrowing measured_removed=0 measured_added=10
  ```

  더해진 열 개는 `core-antipatterns.md:A` ~ `:J` 다. 빠진 행은 0 이다 — 재는 행이 늘기만 하니 통과하는 구현이 줄어든다
- 근거: 에이전트 판단. 사용자 발언 인용은 없다. 묶음 전체의 계약 합의 위임은 2026-09-26T10:09:00.557Z(결정 답 10:30:16.222Z) · session=bda55d45-296c-491f-89ba-b52042d58e72 · cwd=/Users/jackson/Hub/10_Dev/claude-plugins 이지만, 이 개정을 콕 집은 동의는 아니다
- 앵커: 없음 — consent `unanchored`. 방향이 `narrowing` 이라 PASS 근거로 쓸 수 있다(계약 스키마 §Amendment 사이드카 표)
