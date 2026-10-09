---
slug: after-0926-kits-reflect-bambu-tone
created: "2026-09-27 10:42"
---

## A-01 — SC-05 측정 첫 줄의 `mut=4`

**앵커**: SC-05 측정 「첫 줄 `mut=4 rc=0 fixtures=F match≥8 bad=0 skip=F-match skip_named=skip`」.

**무엇이 틀렸나**: `mut` 는 SKILL.md 사본에서 `/Applications/` 를 `/nonexistent-apps/` 로 바꾼 줄 수다(도우미 `grep -c nonexistent-apps`).
시작 판 `6378948` 에서 같은 명령을 돌리면 **10** 이고, 가지 끝에서도 **10** 이다. 이 스프린트는 `/Applications/` 가 든 줄을 더하거나 빼지 않았다.
`4` 는 봉인 전에 잰 적이 없는 값이다 — 계약 작성자가 적은 봉인 전 실측은 판정 수(FAIL 기대 넷 · PASS 기대 셋)뿐이고 `mut` 값은 없다.
그래서 원래 조건은 구현과 무관하게 통과할 수 없다(PASS 집합이 비었다).

**바꾸려는 것**: `mut=4` → `mut=10`. 나머지(`rc=0` · `match≥8` · `bad=0` · `skip=F-match` · `skip_named=skip` · 둘째 줄 음성 대조)는 그대로 둔다.
`mut` 는 변이가 실제로 먹었는지 보는 값이라 `≥1` 로 넓히지 않고 지금 잰 값 그대로 적는다.

**가지 끝 실측 (2026-09-27)**: `mut=10 rc=0 fixtures=24 match=8 bad=0 skip=16 skip_named=16` · 둘째 줄 `neg mut=1 rc=1 bad_class=1`.

**amend_direction_oracle**: `relaxing` — 원 조건의 PASS 집합이 공집합이라 어떤 값을 넣어도 PASS 집합이 늘어난다(contract-schema.md §미실측 오라클 봉인 금지).
**consent**: (비어 있음 — 사용자 동의가 필요하다. 위임 문구로 동의 처리하지 않는다)
