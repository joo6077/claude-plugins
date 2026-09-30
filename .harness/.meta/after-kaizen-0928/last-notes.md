# 묶음 last 기록 — Mermaid 예시 세기 · check-superseded 안내

계약 `.harness/sprint-contract-after-0930-last.md` (23 조건, 봉인 커밋 `7d156456`, 지문 `sha256:4d110e818423f53a`).
가지 `chore/ak3-last`, 시작 판 `0928bf65`. QA 판정은 아직 없다.

## 항목별 결과

### (1) Mermaid 예시 세기 — 처리함

- `scripts/check-docs-mermaid.js` (커밋 `b867b1ef`): 예시를 두 길로 센다. `<pre>` 의 `aria-label` 이
  「Mermaid … 예시」 이면 첫 줄과 무관하게 예시로 세어 그려 본다 — 그래서 `flowchart LR` 을 `flowchat LR` 로
  잘못 쓴 예시가 더는 조용히 빠지지 않고 안 그려진 예시로 잡힌다. 이름표가 없으면 `---` 머리말을 건넌 첫 줄로
  판정한다 — 머리말 붙은 정상 예시가 빠지던 구멍이 막혔다. 이름표 붙은 빈 예시도 안 그려진 예시로 센다.
- `scripts/test-check-docs-mermaid.js` (같은 커밋): 경우 5 ~ 8 을 더해 여덟 경우. 시작 판 검사를 넣으면
  경우 5 · 6 · 7 만 실패하고, 늘 0 을 내는 가짜 검사는 경우 2 ~ 8 이 실패한다.
- `.github/workflows/ci.yml` (커밋 `ccfd73f8`): 시험 단계 이름을 「여덟 경우」 로.
- `docs/planning-kit/reference.html` (커밋 `3b7a3402`): 이름표 없던 예시 셋(`xychart-beta` · `quadrantChart` ·
  `mindmap`)에 `aria-label="Mermaid <종류> 예시"` 를 붙였다. 이제 레포 예시 9 개가 모두 이름표를 가진다.
- 레포 전체는 그대로 `쪽 3 · 예시 9 · 안 그려진 예시 0`.

### (2) check-superseded 안내 — 처리함

- `harness/skills/sprint-contract/SKILL.md` (커밋 `43439c11`): 안내에 `UNREADABLE <계약>` ·
  `UNREADABLE <계약> -> <새 판>` · 끝 줄 `checked=` · `violations=` · `unreadable=` · 종료 코드 2 를 적었다.
  안내 밖 줄은 그대로다(덩어리 1 개).
- `harness/references/contract-schema.md` (같은 커밋) · `docs/harness/contract-schema.html` (커밋 `61137280`):
  `superseded_by` 행에 「못 읽는 계약 · 새 판은 `UNREADABLE` 줄로 적고 통과로 치지 않는다 — 그때 종료 코드 2」
  를 같은 글로 더했다. `detect-docs-drift --since 0928bf65` 짝은 이 둘 하나뿐이다.

## tone-guide 결과

- 1 단계: 오버레이 `.claude/tone-project.md` (어댑터 없음 · 주석 한국어)와 레포 `tone-kit/references/` 의
  코어 네 파일 · `locale-korean.md` 규칙 ID 를 읽었다. 걸리는 규칙은 C-01 · C-07 · N-08 · K-03 · K-10 · F.
- 5 단계: 추가된 46 줄에 한국어 번역투 여섯 패턴(G-1) 0 건, 구분선(F) 0 건, 한 글자 이름(N-08) 0 건.
  새 주석은 동작 설명이 아니라 왜 세는지(이름표 · 머리말)만 적는다(C-01). 위반 없음.

## 킷 버전 판단

- harness: 스킬 안내와 규약 문서 글만 더했다 — 동작 바뀜 없음, 다음 릴리스 때 patch 한 단계면 된다.
  이 묶음에서는 올리지 않는다(계약 범위 밖).
- planning-kit: 쪽(`docs/`)만 바뀌어 킷 파일은 그대로다 — 올릴 것 없음.
- `scripts/` · `.github/` 는 킷이 아니다.

## 남긴 것

- `chore/ak3-cx` 합치기: 이 가지의 `harness/scripts/check-superseded.sh` 는 아직 옛 모양이라 못 읽는 계약을 만나면
  `awk` 오류만 흘리고 종료 코드 0 을 낸다. 안내는 새 모양(`UNREADABLE` · 종료 코드 2)을 먼저 적었으므로,
  `chore/ak3-cx` (커밋 `90e08acf`)가 통합 가지에 합쳐져야 안내와 스크립트가 맞는다. 합치는 일은 이 묶음 범위 밖이다.
- 이름표 없는 `<pre>` 의 종류 이름 오타는 여전히 못 잡는다. 새 쪽에 Mermaid 예시를 넣을 때 이름표를 붙이라는
  규칙은 문서로 올리지 않았다(계약 `## 범위 경계` 의 하지 않는 것).
- 교차 진단이 짚은 것: `harness/agents/qa-evaluator.md` Step 1-b 의 frontmatter 읽기 사본은 줄 끝 주석을 값으로
  읽을 수 있다(규약 문서의 정의는 이미 고쳐짐). 이 계약과 무관해 손대지 않았다.
- QA 판정과 계약 `status: done` 은 qa-evaluator 몫이라 하지 않았다.
