# after-0928-external-facts-2 개정

계약 `sprint-contract-after-0928-external-facts-2.md` (봉인 `sha256:30978e4d67ca2840` · 측정 `sha256:8c1c9fcbc681c2ca`,
봉인 커밋 ce5df05) 의 조건 줄과 측정 줄은 고치지 않았다. 바뀐 것은 여기에만 적는다.

## A-01 — ER-01 음성 대조에 쓰는 주소를 시작 판에 없는 것으로 바꾼다

**앵커**: ER-01 — "음성 대조: 구현 뒤 문서 한 곳에 `https://z.example.com/new` 를 더한 떠 있는 커밋(가지는 안 옮김)에 돌리면 1 이 나온다."

**무엇이 달라졌나**: 음성 대조에 넣는 주소만 `https://neg-ex2.example.org/fresh-20260928` 로 바꾼다. 통과 판정(`newurls.sh` 출력 0 줄 · 종료 코드 0)과 측정 명령은 그대로다.

**왜** — 적힌 주소 `https://z.example.com/new` 는 앞 묶음 기록 `.harness/.meta/after-kaizen-0928/ex-notes.md` 와 앞 계약
`.harness/sprint-contract-after-0928-external-facts.md` 에 이미 있어 시작 판 `e500a63` 에서 「이미 있는 주소」 로 걸러진다. 그래서
그 주소로 만든 떠 있는 커밋(`4c601c7`)에서는 0 이 나왔다 (2026-09-28 실측). 측정이 죽은 것이 아니라 대조용 주소가 알려진
주소였다. 시작 판 · 끝 판 · X 파일 어디에도 없는 주소(`git grep -c` 0 · X 파일 0)로 만든 떠 있는 커밋(`14d581b`)에서는
출력이 그 주소 한 줄, 수 1 이다.

**amend_direction_oracle**: `unchanged measured_removed=0 measured_added=0` — 통과 집합을 정하는 측정 줄은 바뀌지 않았고,
바뀐 것은 측정이 살아 있는지 보는 대조 입력뿐이다.

**consent**: 해당 없음 — 조건을 느슨하게 하지 않는다.
