---
slug: kaizen-0924-f2-review-fixes
created: "2026-09-26 03:55"
---

# kaizen-0924-f2-review-fixes 개정

이 파일은 범위 상한 `end_sha` 를 적는 자리다. 조건은 바꾸지 않았다 — 개정 0 건. 봉인 뒤 계약의 산문도 고치지 않았다.

측정 공통 정의가 아래 `end_sha:` 줄의 마지막 값을 `END` 로 읽는다. 커밋을 더하면 새 값으로 한 줄을 **덧붙인다** (옛 줄은 지우지 않는다).
그 커밋 메시지에도 `Co-Authored-By` 줄 바로 위에 서명 줄 `Kaizen-Phase: kaizen-0924-f2-review-fixes` 를 넣는다 — 빠지면 AR-01 첫째 값이 떨어진다.

- 봉인 커밋: `c6850fee84c8d05c1f6ac8c63a7934d0e8fec4e0` (계약 파일 1 개, `conditions_digest: sha256:1d2980c691dc41b0`)
- 구현 커밋 열셋(묶음마다 하나): `72d6ddd` scripts · `5a5c420` claude · `211d1d7` harness · `59f8ca4` react · `1113bdd` design · `b52f43c` ci ·
  `0dd1f66` flutter · `8d5e2c1` reflect · `1396a11` api · `05e796d` rust · `04e3591` onboarding · `5a4b31b` bambu · `d24d382` readme

## 구현이 개선안과 다른 곳 — 조건 변경 없음 (amend_direction: unchanged)

조건 줄 · 측정은 그대로이고 통과 집합도 바뀌지 않는다. 개선안 문장과 다르게 구현한 자리만 적는다.

- 개선안 12 (A7): `collect_status` 의 「마지막 기록 뒤」 셈만이 아니라 엔트리 0 경고도 같은 셈(마지막 기록과 마지막 정상 종료 가운데 늦은 쪽 뒤의 실패)을 쓴다.
  엔트리 0 이어도 실패 뒤에 `ok:no-issues` 가 있으면 수집기는 돌고 있어, 두 갈래를 달리 두면 같은 지적(정상 실행 뒤를 멈춤으로 봄)이 엔트리 0 쪽에 남는다.
  정상 종료 줄이 없으면 엔트리 0 에서 두 셈은 같다 — 기존 시험 경우는 값이 바뀌지 않는다. 시험에 「엔트리 0 · 실패 뒤 정상 종료 — 경고 없음」 한 경우를 더했다(시작 판 라이브러리로 돌리면 불일치)
- 개선안 4 (A6): record-format 예시의 도구 자리표시를 `<도구명>` 하나 대신 하는 일로 가른 `<누르기 도구>` · `<위젯 찾기 도구>` 로 썼다 — 한 줄에 서로 다른 도구 둘이 나온다
- 개선안 2 (B4): tone-kaizen `:35` 괄호는 2 회차 검토 권함대로 「(리서치 문서 8종 + overview · research-log · templates)」 로 썼다
- 개선안 7 (A8): 블록을 항목 첫 문장 바로 뒤에 두고, 잇는 방법 문장은 「첫 줄과 둘째 줄은 줄바꿈이나 `;` 로 잇고 `&&` 로 잇지 않는다」 로 썼다 — 블록은 세 줄이고 규칙은 첫 줄과 둘째 줄 사이에 걸린다

end_sha: d24d382adeb55dfdd8470c17ee6fa2969fafa8a2

notes 커밋 `7f874b4db6df605eb0b64b803258fef4d5cfe260` (`f2-review-fixes-notes.md` · `f2-review-fixes-review.md` · 감사 기록 한 줄) — 이 계약 커밋이라 상한을 옮긴다.

end_sha: 7f874b4db6df605eb0b64b803258fef4d5cfe260
