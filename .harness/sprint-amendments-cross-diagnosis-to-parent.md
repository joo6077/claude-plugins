---
slug: cross-diagnosis-to-parent
created: "2026-09-22 16:05"
---

## A-01 — AR-04 (iv) 허용 목록에 앞 스프린트 계약 파일 1개 추가

**앵커**: AR-04 측정 (iv) — "`.harness/` 로 시작하는 줄 중 이 스프린트 산출물 3개
(`sprint-contract-cross-diagnosis-to-parent.md` ·
`sprint-feedback-cross-diagnosis-to-parent.md` ·
`sprint-amendments-cross-diagnosis-to-parent.md`) 를 뺀 나머지 0행"

**무엇이 달라졌나**: 허용 집합에 `.harness/sprint-contract-validate-check-count-sync.md` 를
더한다. 그 파일은 앞 스프린트 계약이고, 이 구간에 들어온 변경은 `status: active → done`
**한 줄**이다.

**왜 이번 스프린트의 산출물이 아닌가**: 그 전환은 앞 스프린트의 qa-evaluator 가 APPROVE
시점에 수행하는 정상 동작이다 (`qa-evaluator.md` Step 5.5 · `contract-schema.md` §status 해석
규칙 — 계약을 `done` 으로 바꾸는 주체는 평가자다). 이번 스프린트가 만든 변경이 아니고,
봉인된 조건 줄도 건드리지 않았다(`SEAL_OK` 확인). AR-04 의 취지는 "과거 기록을 고치지
않았다" 인데 이 전환은 기록을 고치는 것이 아니라 기록이 스스로 완료를 표시하는 것이다.

**왜 하한을 바꾸는 대신 허용 목록을 넓혔나**: AR-04 의 하한 `ab396f2` 는 봉인된 값이다.
앞 스프린트 커밋이 이미 그 해시이고, status 전환은 그 뒤에 일어났으므로 어떤 구간을 잡아도
이 파일은 들어온다. 하한을 움직이면 AR-01 과 어긋나므로 허용 목록 쪽을 고쳤다.

**amend_direction**: `relaxing added=1 removed=0` — 집합 비교로 계산했다.
원 허용 집합 3개 → 개정 4개. 자기신고가 아니라 계산값이다.

**consent**: `anchored` — 2026-09-22 16:05, 세션 `f5b7f3a5-c03d-452b-b44b-fc3d15dcd1a0`.
사용자에게 세 선택지(개정으로 허용 / status 되돌리기 / AR-04 FAIL 받기)를 제시하고
"개정으로 한 개 허용" 을 받았다. 되돌리는 쪽은 APPROVE 된 스프린트를 `active` 로 남겨
기록을 거짓으로 만들기 때문에 택하지 않았다.

**남는 구조적 문제**: 여러 스프린트를 한 브랜치에 쌓으면 앞 스프린트의 `status` 전환이 항상
뒤 스프린트의 범위 조건에 들어온다. 다음 계약에서 `.harness/` 범위 조건을 쓸 때는 산출물
슬러그를 열거하는 대신 **"이 구간에서 조건 줄이 바뀐 계약 파일 0개"** 로 재는 편이 낫다 —
`status` 토글과 조건 변조를 구별하는 것이 원래 의도였고, 봉인 검사가 이미 그것을 한다.
