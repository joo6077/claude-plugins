---
slug: bambu-kit-orca-h2s-feedback
contract: .harness/sprint-contract-bambu-kit-orca-h2s-feedback.md
created: "2026-09-19 10:40"
---

계약 봉인(`sha256:3888c2d2c799092a`) 뒤 qa-evaluator 교차 진단(agentId a522dc223f8f783e8)이 지적한 8 건을 반영한다.
계약 본문은 고치지 않는다. 앵커는 모두 없다 — 사용자 발언이 아니라 교차 진단 결과에 따른 작성자 판단이다.

## AM-01 — narrowing

- 대상 조건: AR-05
- 변경: 토큰 개수 외에 **값의 짝**도 본다. §6.5.4 구간에서 `뱀부` 가 있고 `오르카` 가 없는 줄은 `true` 를 1 번 이상 담고
  `false` 를 담지 않는다. `오르카` 가 있고 `뱀부` 가 없는 줄은 `false` 를 1 번 이상 담고 `true` 를 담지 않는다.
  두 값을 뒤바꿔 적어도 원 측정은 통과하던 구멍을 막는다
- 측정: `cut_sec "$R/seam-recipes.md" "### 6.5.4" "### 6.5.5" | awk '/뱀부/ && !/오르카/ {b++; if(/false/) bad++; if(/true/) bt++} /오르카/ && !/뱀부/ {o++; if(/true/) bad++; if(/false/) of++} END{print (bt>=1 && of>=1 && bad==0) ? "OK" : "FAIL"}'` 가 `OK`
- 근거: 교차 진단 (2) — "뱀부는 false, 오르카는 true 처럼 값을 뒤바꿔 적어도 토큰 카운트는 통과한다"
- 앵커: 없음 (unanchored · 작성자 판단) — narrowing 이라 PASS 근거로 쓸 수 있다

## AM-02 — narrowing

- 대상 조건: ER-02
- 변경: 음성 대조를 더한다. 키가 있는 원본 `$FX/machine-orca-h2s-bs-start.json` 에서는 `printer_settings_id` 가 든 FAIL 줄이
  **0** 이어야 한다 (키를 지운 사본에서만 걸리는지 확인)
- 측정: `TARGET_SLICER=orca python3 "$GATE" "$FX/machine-orca-h2s-bs-start.json" | grep '^FAIL' | grep -cF 'printer_settings_id'` == 0
- 근거: 교차 진단 (3)
- 앵커: 없음 (unanchored · 작성자 판단)

## AM-03 — narrowing (측정 추가 · `amend_direction_oracle` 기준 measured_added>0)

- 대상 조건: DG-02
- 변경: "대체: 없음" 을 구체화한다. 기본 측정은 **편집 직후 편집기가 돌려준 진단**이다 — 이 세션에서는 파일을 고칠 때마다
  편집기 진단이 자동으로 따라온다. 변경한 마크다운·JSON 파일마다 새로 생긴 경고 수를 근거 문서
  `.harness/.meta/evidence/bambu-orca-h2s-feedback.md` 의 `## 편집기 진단` 표에 적는다. 표가 없거나 새 경고가 1 건 이상이면 FAIL.
  맞춤법 검사 경고는 제외한다 (전역 규칙)
- 근거: 교차 진단 (4) — "DG-02 는 대체: 없음이라 스스로 적어 놨다"
- 앵커: 없음 (unanchored · 작성자 판단)

## AM-04 — 기록만 (조건 변경 없음)

- 대상 조건: AR-09
- 내용: 교차 진단 (5) 는 평가자 규약상 피드백 초안 이름이 `feedback-draft-<slug>.yaml` 이라 목록 밖으로 잡힐 수 있다고 했다.
  `git ls-files .harness | grep -c feedback-draft` 가 0 (2026-09-19 실측) — 이 저장소는 피드백 초안을 커밋한 적이 없다.
  이번에도 커밋하지 않는다. 목록을 넓히지 않으므로 완화가 아니다

## AM-05 — 기록만 (측정 대상 불변)

- 대상 조건: AR-07
- 내용: 측정 문구 "파일마다" 는 "토큰마다" 의 오기다. 대상 파일은 근거 문서 1 개이고, 산문에 나열한 5 토큰을 하나씩 센다
  (범위 경계의 커버리지 해소 기록과 같은 뜻)

## 평가 시 유의 (교차 진단 (1)(7)(8) · 조건 변경 없음)

- 범위 경계의 준비 블록은 셸 호출마다 다시 실행한다. 환경변수·임시 파일·함수가 다음 호출에 남지 않는다
- SC-06 의 두 경로는 공백이 있어 각각 따옴표로 감싼다
- RE-01 은 구현 전에도 값이 1 이다. 이번 스프린트의 기계 설정 지원 여부는 SC-01~04 가 판정한다 — RE-01 은 중복 재구현이
  없음만 본다
