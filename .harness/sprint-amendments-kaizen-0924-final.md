---
slug: kaizen-0924-final
created: "2026-09-25 22:52"
---

# kaizen-0924-final 개정

이 파일은 범위 상한 `end_sha` 를 적는 자리다. 조건은 바꾸지 않았다 — 개정 0 건. 봉인 뒤 계약의 산문도 고치지 않았다.

측정 공통 정의가 아래 `end_sha:` 줄의 마지막 값을 `END` 로 읽는다. 커밋을 더하면 새 값으로 한 줄을 **덧붙인다** (옛 줄은 지우지 않는다).
그 커밋 메시지에도 `Co-Authored-By` 줄 바로 위에 서명 줄 `Kaizen-Phase: kaizen-0924-final` 을 넣는다 — 빠지면 AR-09 `unsigned` 가 떨어진다.

- 봉인 커밋: `509d29530fdaf9335f93a066211f51a7007bc95e` (계약 파일 1 개, `conditions_digest: sha256:81b9a7409e53588b`)
- 문서 사이트 페이지 마흔넷: 봉인 뒤 페이지마다 한 커밋(Claude 28 쪽 · Codex 16 쪽) — 목록은 `.harness/.meta/kaizen-0924/final-notes.md` `## 문서 사이트`
- 나머지 구현 커밋: `18b1b11` 상태 커밋 · `8370391` 개정 파일 다섯 · `7813569` 처리 배정표 · `3484855` 옛 값 등록부 · `098f671` surface-recipes 페이지 한 문단 ·
  `55d8a36` 첫 화면 제목 · `c18e7e0` changelog · 연구 기록 · CLAUDE.md · `8163d69` 상태 · 기록 파일 · `410dcc9` 감사 기록

구현이 개선안과 다른 곳 하나 — 개선안 6 은 페이지를 한 페이지 = 한 에이전트로 원본 전체에서 만든다고 적었다. Codex 가 만든 `docs/bambu-kit/surface-recipes.html` 이
원본의 「잰 방법 (2026-09-25 추가)」 문단을 줄여 옮기며 블록 이름(「G-code 로 길이 재기」)을 빠뜨려 AR-03 새 글자 하나가 비었다. 페이지를 다시 만들지 않고 그 문단 하나를 원본 문장대로 고쳤다(`098f671`).
조건 · 측정은 그대로다 — amend_direction: unchanged.

end_sha: 410dcc9178c4553ea7ffffd0dba11f3abd8ab2a1

notes 커밋 `fdae7db91c4abc1c50a4c999b32540200a15c634` (`final-notes.md` · `final-review.md`) — 이 계약 커밋이라 상한을 옮긴다.

end_sha: fdae7db91c4abc1c50a4c999b32540200a15c634

notes 커밋 `3596bf6ea2fd738a0820fc3f5d91c048abbcaae5` (`final-notes.md` 끝 판 재측정 · 계약 피드백 저장 기록) — 이 계약 커밋이라 상한을 옮긴다.

end_sha: 3596bf6ea2fd738a0820fc3f5d91c048abbcaae5

## 교차 진단 뒤 보강 — 조건 변경 없음 (direction: unchanged)

QA 1 회차 판정(`APPROVE` 26/26) 뒤 부모 세션의 교차 진단(2026-09-25)은 판정을 뒤집을 근거가 없다고 했다. 다만 두 가지를 짚었다.

- 「원본 전체로 다시 만든다」(계약 `## 배경` 과 개선안 6, 러닝북 「문서 사이트」 절)는 뜻으로 보면 Codex 가 만든 페이지 몇 쪽이 옛 페이지(봉인 커밋 `509d295` 판)보다 원본 내용을 덜 담는다.
  원본 낱말 가운데 페이지 글에 든 비율이 옛 판보다 낮았던 쪽 — `docs/tone-kit/korean-technical-writing.html` · `docs/onboarding-kit/fcm-ios-example.html` ·
  `docs/bambu-kit/surface-recipes.html` · `docs/tone-kit/overview.html` · `docs/backend-kit/database.html`
- AR-03 측정(`docs.py`)은 새 글자 · 옛 글자 · 줄 수만 봐서 본문이 빠져도 통과한다. 끝 판 사본에서 본문 700 줄을 지워도 끝줄이 같았다(교차 진단 사본 `scratchpad/xdiag-final/ar03neg/`)

그래서 세션 스크래치 `kaizen/coverage.py` 로 페이지마다 원본을 얼마나 담았는지 옛 페이지와 맞대 재고, 모자란 열네 쪽을 채웠다. 목표는 둘이다 —
옛 페이지에 있던 원본 코드 표시(백틱으로 감싼 글)가 새 페이지에서 빠진 수 0(`lost=0`), 원본 낱말이 페이지 글에 든 비율이 옛 판 이상(`wr=옛->새` 에서 새 값이 옛 값 이상).

조건 문구 · 측정 · 기대값은 하나도 바꾸지 않았다. 보강은 AR-03 이 이미 요구하는 「원본 전체 반영」 을 채운 구현 수정이라 조건을 느슨하게도 좁게도 하지 않는다 — amend_direction: unchanged.
페이지는 한 쪽에 한 커밋, 그 파일 하나만 실었고 커밋마다 서명 줄 `Kaizen-Phase: kaizen-0924-final` 이 있다. 파일 이름 · 내비 id · `--accent` 는 그대로이고 `docs/index.html` 은 건드리지 않았다.

사용자 위임 앵커: 세션 기록 `/Users/jackson/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/de8c7935-a5b6-4df5-9106-fafa73c288a0.jsonl` 의
queued_command `2026-09-24T04:04:16.964Z`(「자동으로 끝까지 알아서 진행해 …」) · user `2026-09-24T11:54:58.940Z`(「… 그냥 너가 알아서 진행하라고」) ·
user `2026-09-24T12:21:36Z`(「끝까지 계속 진행해」) · user `2026-09-25T06:19:45.056Z`(「코덱스도 사용할 수 있으니깐 사용해」).

담김 검사 전후 — 고치기 전은 그 커밋의 부모 판, 고친 뒤는 그 커밋 판에서 `coverage.py` 와 같은 식으로 잰 값이다. `wr` 왼쪽은 옛 페이지(`509d295`) 값이다.

| 페이지 | 커밋 | 원본 코드 표시 | 고치기 전 | 고친 뒤 | 줄 수 |
| --- | --- | --- | --- | --- | --- |
| `docs/bambu-kit/bambu-print-profile.html` | `8e2b8e7` | 442 | `new=385 lost=2 wr=0.26->0.73` | `new=387 lost=0 wr=0.26->0.73` | 2225 → 2226 |
| `docs/backend-kit/database.html` | `1625851` | 48 | `new=38 lost=5 wr=0.71->0.65` | `new=48 lost=0 wr=0.71->0.92` | 671 → 743 |
| `docs/tone-kit/korean-technical-writing.html` | `723072d` | 56 | `new=40 lost=14 wr=0.81->0.53` | `new=56 lost=0 wr=0.81->0.94` | 416 → 545 |
| `docs/bambu-kit/surface-recipes.html` | `45204d9` | 170 | `new=98 lost=41 wr=0.57->0.45` | `new=170 lost=0 wr=0.57->0.99` | 900 → 910 |
| `docs/tone-kit/overview.html` | `22cdca1` | 27 | `new=27 lost=0 wr=0.87->0.75` | `new=27 lost=0 wr=0.87->0.92` | 517 → 525 |
| `docs/flutter-toolkit/project-detection.html` | `d67a2a9` | 141 | `new=140 lost=1 wr=0.81->0.84` | `new=141 lost=0 wr=0.81->0.84` | 600 → 600 |
| `docs/flutter-toolkit/primitive-substitution-gate.html` | `414c510` | 44 | `new=43 lost=0 wr=0.96->0.89` | `new=44 lost=0 wr=0.96->1.00` | 662 → 671 |
| `docs/harness/qa-evaluation-guide.html` | `8b86185` | 394 | `new=392 lost=1 wr=0.68->0.96` | `new=393 lost=0 wr=0.68->0.96` | 1993 → 1994 |
| `docs/harness/plugin-validation.html` | `d6b2189` | 159 | `new=157 lost=1 wr=0.66->0.78` | `new=159 lost=0 wr=0.66->0.78` | 1031 → 1031 |
| `docs/react-kit/render-evidence-protocol.html` | `d12b7b6` | 64 | `new=48 lost=9 wr=0.53->0.61` | `new=64 lost=0 wr=0.53->0.97` | 838 → 882 |
| `docs/onboarding-kit/fcm-ios-example.html` | `26eb44d` | 75 | `new=50 lost=8 wr=0.70->0.49` | `new=75 lost=0 wr=0.70->0.97` | 428 → 536 |
| `docs/design-kit/design-test.html` | `d18a2b0` | 61 | `new=49 lost=2 wr=0.40->0.52` | `new=61 lost=0 wr=0.40->0.93` | 745 → 991 |
| `docs/reflect-kit/design.html` | `c220dee` | 123 | `new=69 lost=7 wr=0.33->0.52` | `new=122 lost=0 wr=0.33->0.91` | 424 → 520 |
| `docs/infra-kit/infra-test.html` | `a38de63` | 132 | `new=88 lost=4 wr=0.33->0.86` | `new=132 lost=0 wr=0.33->0.86` | 666 → 807 |

끝 판(`a38de63`)에서 마흔넷 쪽 모두를 같은 식으로 다시 재니 `lost` 가 1 이상이거나 새 비율이 옛 비율보다 낮은 쪽은 0 이다.

같은 보강에서 함께 실은 커밋 둘 — `849940e`(이 계약 `status: done` 과 QA 1 회차 리포트) · `a784aef`(`.harness/.meta/evals-audit-2026-09-24.md` 의 bambu-kit CI 문장을 사실대로 — 교차 진단 계약 밖 결함 1).
교차 진단 계약 밖 결함 2(감사 기록 감시 목록 줄 · `scripts/append-audit-log.py:171-178`)와 측정 구멍 셋은 고치지 않고 notes `## 다음 사이클 메모` 에 적는다.

교차 진단 뒤 보강 커밋 열일곱(페이지 열넷 `8e2b8e7` ~ `a38de63` · `849940e` · `a784aef` · 위 절 `65ea663`) — 이 계약 커밋이라 상한을 옮긴다.

end_sha: 65ea663cc27189ab2508fc518ca9399d50dc24ff

notes 커밋 `0cf02789a6c6f03ccb9651528c028b6172e197ee` (`final-notes.md` 교차 진단 뒤 보강 절 · 다음 사이클 메모 넷) — 이 계약 커밋이라 상한을 옮긴다.

end_sha: 0cf02789a6c6f03ccb9651528c028b6172e197ee

## 교차 진단 2 회차 뒤 보강 — 조건 변경 없음 (direction: unchanged)

QA 2 회차 APPROVE 뒤 교차 진단이 보강 잣대(`coverage.py`)가 원본의 코드 블록 안을 재지 않는다고 짚었다. 코드 블록 줄을
공백·태그를 빼고 대조하면(`scratchpad/xd-final2/fence2.py`) Codex 가 만든 두 쪽이 옛 판보다 덜 담았다. 조건 문구는 바꾸지 않는다.

| 페이지 | 커밋 | 코드 블록 대조 전 → 뒤 | coverage.py 뒤 |
| --- | --- | --- | --- |
| `docs/rust-kit/sqlx-patterns.html` | `a0a395e` | `in_old=48 in_new=46 lost=4` → `in_new=52 lost=0` | `lost=0 wr=0.43->0.77` |
| `docs/backend-kit/backend-test.html` | `10d42ee` | `in_old=5 in_new=31 lost=2` → `in_new=46 lost=0` | `lost=0 wr=0.47->0.69` |

두 쪽 모두 `check-docs-a11y.js` 2/2 PASS · `check-docs-links.py` · `check-contrast-claims.py` 종료 코드 0. QA 2 회차 리포트 커밋 `bc6302c`.

end_sha: 10d42ee02d227081aed436a221bb6233be50e152
