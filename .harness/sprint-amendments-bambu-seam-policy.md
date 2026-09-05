# Sprint Amendments — bambu-seam-policy

계약 본문은 write-once 다. 조건 문구를 고치지 않고 여기에 기록한다.

## AM-01 — RE-02 카브아웃 (제안, 승인 대기)

- **대상 조건**: `RE-02: 이미 존재하는 references 파일을 새로 만들지 않고 해당 섹션을 확장한다`
- **제안 문구 추가**: "단, **다른 스프린트의 계약 조건이 명시적으로 요구해 생성된 파일**은
  이 조건의 위반으로 보지 않는다."
- **direction**: `relaxing` · **anchor**: unanchored (이 슬러그의 첫 amendment)
  - 계산 근거: 원 조건이 FAIL 처리하는 집합 = {신규 references 파일 전부}.
    개정 후 = {신규 references 파일} − {선행 계약이 요구한 파일}. **통과 집합이 넓어진다 →
    relaxing 이다.** "범위 명확화" 로 부를 여지가 없다.
- **consent**: **pending** — 완화 방향이므로 자체 승인 불가. 사용자 승인 전에는 미적용.

### 사실관계

`references/user-preferences.md` 는 **선행 스프린트 `bambu-kit` 의 조건 SK-05 가 경로까지
지정해 요구한 산출물**이다.

- 선행 계약 `.harness/sprint-contract-bambu-kit.md:74` —
  *"품질 우선 선호 영속화 지점이 `…/references/user-preferences.md` 경로로 명시되고…"*
- 선행 QA `.harness/sprint-feedback-bambu-kit.md:39` — `SK-05 … PASS`
- 선행 QA `…:85` — RE-02 와의 관계를 이미 판정: *"SK-05 가 명시적으로 요구하는 별도 조건의
  산출물로, RE-02 의 취지와 충돌하지 않는다고 판단"*
- 선행 QA `…:86` — **개선 제안: "RE-02 에 카브아웃 명시 권장"**

이번 스프린트 계약을 쓸 때 그 개선 제안을 반영하지 않고 RE-02 를 그대로 전사했다.
**계약 작성자(구현자)의 누락이며, 이번 평가자의 FAIL 판정은 계약 문면상 정당하다.**

### 평가가 이력을 볼 수 없었던 이유

두 스프린트의 산출물이 전부 미커밋이다 (`git log` 최신 = `3ae2ea3`, 이번 작업 커밋 0 건).
그래서 평가자가 `git log -- references/user-preferences.md` 로 선행 스프린트 귀속을 확인할 수
없었고 `??` 미추적만 관측했다. **커밋 부재가 provenance 검증을 불가능하게 만든 구조적 원인이다.**

### 선택지

1. **AM-01 승인** — 카브아웃 적용, RE-02 재판정
2. **선행 스프린트 산출물을 먼저 커밋** — 파일 이력이 생겨 평가자가 귀속을 확인 가능. AM-01 불필요
3. **`user-preferences.md` 내용을 기존 references 로 흡수** — RE-02 를 문자 그대로 만족하지만
   선행 계약 SK-05(경로 명시)를 깨뜨린다. **두 계약이 충돌하므로 비권장**
