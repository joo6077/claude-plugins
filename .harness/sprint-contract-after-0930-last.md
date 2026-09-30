---
feature: "마지막 — Mermaid 예시 세기 · check-superseded 안내"
slug: after-0930-last
created: "2026-09-30 11:01"
complexity: "복잡"
conditions: 23
status: done
owner_session: bda55d45-296c-491f-89ba-b52042d58e72
conditions_digest: "sha256:4d110e818423f53a"
measurement_digest: "sha256:6fb5c275e1ad69eb"
locked_at: "2026-09-30 11:37"
---

## 배경

- 묶음 last. 출처는 `.harness/.meta/after-kaizen-0928/tail-notes.md` 「남긴 것」 절의 Mermaid 검사 약점 하나와, 가지 `chore/ak3-cx` 가 바꾼 `harness/scripts/check-superseded.sh` 출력 모양을 스킬 안내에 옮기는 일이다. 결정 파일 `.harness/.meta/after-kaizen-0928/decisions.md`, 남은 일 목록 `.harness/.meta/after-kaizen-0928/remaining.md`. 사용자 위임: 2026-09-27T01:22:01.089Z 「자동으로 다 진행해 나한테 묻지 말고 …」 · 2026-09-28 「약점과 일부만 한 거 다처리하지??」(세션 bda55d45-296c-491f-89ba-b52042d58e72).
- 작업 폴더 W = `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak3-last`, 가지 `chore/ak3-last`, 시작 판 `BASE` = `0928bf65` (가지 `chore/after-kaizen-0928` 끝 — tail 이 합쳐진 판).
- 사용자가 할 일: 없음.

공통 전제 G (조건마다 되풀이하지 않는다) — 구현 · 기록 커밋이 가지 `chore/ak3-last` 에 모두 들어가고, W 의 HEAD 가 그 가지 끝이며, `git -C W status --porcelain -- . ':(exclude).harness' ':(exclude)node_modules'` 가 빈 출력이고, W 에서 `npm ci` 를 커밋된 `package-lock.json` 으로 다시 돌린 뒤 W 맨 위 폴더에서 잰다. 가지 `chore/ak3-cx` 가 로컬에 있어야 한다(스킬-01 이 그 가지의 스크립트를 풀어 돌린다). 이 가지는 이 스프린트만 커밋한다(가지를 합친 뒤에는 재지 않는다). 측정 도우미는 `## 회귀 게이트` 의 `m <조건 번호>` 다. 브라우저 측정은 W 의 `node_modules` 의 playwright 를 쓰고, `TMPDIR` 는 scratch 아래 폴더로 둔다.

항목별 처리 방침 (결정):

- **(1) Mermaid 예시 세기** — `scripts/check-docs-mermaid.js` 는 `<pre>` 첫 줄이 그림 종류 이름으로 시작할 때만 예시로 센다. 그래서 `flowchart LR` 을 `flowchat LR` 로 잘못 쓴 예시와, Mermaid 정상 문법인 `---` 머리말이 앞에 붙은 예시를 아예 빼고 세어 종료 코드 0 을 낸다(봉인 전 실측 — 아래 GAP). 고치는 방법은 **이름표 방식**으로 정했다: `<pre>` 의 `aria-label` 이 「Mermaid … 예시」 이면 첫 줄과 무관하게 예시로 세어 그려 보고, 이름표 없는 `<pre>` 는 머리말(`---` 두 줄 사이)을 건넌 첫 줄로 판정한다. 쪽별 예시 수를 못박는 방식은 버렸다 — 시험이 임시 폴더의 새 쪽으로 돌기 때문에 못박은 표에 없는 쪽은 잡을 수 없고, 쪽을 더할 때마다 표를 고쳐야 한다. `docs/planning-kit/reference.html` 의 예시 셋(`xychart-beta` · `quadrantChart` · `mindmap`)은 이름표가 없으므로 구현이 `aria-label="Mermaid <종류> 예시"` 를 붙인다(`flows.html` 넷 · `data-modeling.html` 둘은 이미 있다). 시험 `scripts/test-check-docs-mermaid.js` 에 경우 5 ~ 8 을 더한다(스크립트-04).
- **(2) check-superseded 안내** — `harness/skills/sprint-contract/SKILL.md` 357 ~ 370 줄 안내는 `MISSING_BY` · `MISSING_TARGET` · `CHAIN` 과 종료 코드 0 만 적는다. 가지 `chore/ak3-cx` 의 스크립트(커밋 `90e08acf`)는 못 읽는 계약을 `UNREADABLE <계약>`, 못 읽는 새 판을 `UNREADABLE <계약> -> <새 판>` 으로 적고 끝 줄에 `unreadable=` 을 더하며 그때 종료 코드 2 를 낸다. 그 모양을 안내에 옮긴다(스킬-01). 규약 문서 `harness/references/contract-schema.md` 의 `superseded_by` 행과 그 쪽 `docs/harness/contract-schema.html` 의 같은 행에도 한 문장을 더한다(구조-01). 스킬 파일 자체에는 문서 쪽이 없다 — `.claude/skills/docs-site/SKILL.md` 의 harness 원본 폴더는 `harness/docs/guides/` · `harness/references/` 다.
- 이 가지의 `harness/scripts/check-superseded.sh` 는 아직 옛 모양이다. 안내가 새 모양을 먼저 적고, 스크립트는 `chore/ak3-cx` 가 통합 가지에 합쳐질 때 들어온다. 스크립트 · 그 시험은 이 계약이 고치지 않는다.

## GAP 분석 (Pre-Edit Audit)

| 대상 파일 | 읽은 자리 | 발견 | 조건 |
| --- | --- | --- | --- |
| `scripts/check-docs-mermaid.js` | 8 줄(예시 정의) · 35 ~ 41 줄(첫 줄 판정) | 첫 줄이 종류 이름이어야만 예시. 머리말 · 오타 예시를 빼고 셈 | 스크립트-01 · 02 · 03, 오류-01 |
| `scripts/test-check-docs-mermaid.js` | 3 ~ 9 줄(네 경우) · 36 ~ 50 줄 | 두 모양의 경우가 없음 | 스크립트-04 |
| `.github/workflows/ci.yml` | 195 ~ 196 줄 | 시험 단계 이름 「네 경우」 | 스크립트-04 |
| `docs/planning-kit/reference.html` | 598 · 610 · 628 줄 | 예시 셋에 이름표 없음 | 스크립트-01(`ref-typo`) · 02(`ref-front`) |
| `docs/planning-kit/flows.html` | 482 · 578 · 635 · 696 줄 | 이름표 넷 있음 — 고치지 않음 | 사본 모양의 원본 |
| `harness/skills/sprint-contract/SKILL.md` | 357 ~ 370 줄 | `UNREADABLE` · 종료 코드 2 없음 | 스킬-01 · 02 |
| `harness/references/contract-schema.md` | 268 줄 | 기계 확인 문장에 못 읽는 경우 없음 | 구조-01 |
| `docs/harness/contract-schema.html` | 466 줄 | 원본 268 줄과 같은 글 | 구조-01 |
| 가지 `chore/ak3-cx` 의 `harness/scripts/check-superseded.sh` | `git show` 전체 (머리 주석 6 ~ 9 줄, 끝 줄 · 종료 코드) | 새 출력 모양의 정본 | 스킬-01 알려진 답 |

봉인 전 실측 (W 시작 판, 2026-09-30):

- 레포 전체 `node scripts/check-docs-mermaid.js` → `쪽 3 · 예시 9 · 안 그려진 예시 0` · 종료 코드 0. 시험 → `경우 4 개 중 통과 4` · 종료 코드 0.
- 사본 모양(도우미 `MUTATIONS`)을 시작 판 검사에 주면: `flows-typo` → `쪽 1 · 예시 3 · 안 그려진 예시 0` · 0, `ref-typo` → `예시 2` · 0, `flows-front-typo` → `예시 3` · 0, `flows-front` → `예시 3` · 0 (정상 예시 하나가 빠짐), `ref-front` → `예시 2` · 0. 다섯 모두 결함 재현.
- Mermaid 12.0.0 에서 `flowchat LR` 은 `mermaid.render` 가 `No diagram type detected …` 로 던지고, 머리말 + `flowchart LR` 은 오류 없이 그린다(도우미 밖 scratch 탐침으로 확인).
- `chore/ak3-cx` 스크립트를 픽스처(옛 판이 가리킨 새 판 · 다른 계약 하나를 읽기 권한 0 으로)에 돌리면 `UNREADABLE <옛 판> -> new` · `UNREADABLE <다른 계약>` · `checked=1 violations=0 unreadable=2` · 종료 코드 2, 권한을 돌리면 `OK …` · `checked=1 violations=0 unreadable=0` · 종료 코드 0. 이 가지의 스크립트는 같은 못 읽는 픽스처에서 `awk: can't open file` 을 흘리고 `checked=1 violations=0` · 종료 코드 0 이다(못 읽은 것을 통과로 친다 — 이 계약이 고치지 않는다).

## Skill

- [ ] 스킬-01: sprint-contract 스킬의 check-superseded 안내가 새 출력 모양을 적는다 — `harness/skills/sprint-contract/SKILL.md` 의 「적은 뒤 `check-superseded.sh`」 줄부터 다음 `**결과:` 줄 앞 마지막 글 줄까지(안내 덩어리)에 `UNREADABLE <계약>` · `UNREADABLE <계약> -> <새 판>` · `unreadable=` · `checked=` · `violations=` · `종료 코드 2` · `못 읽` 이 모두 있고, 기존의 `MISSING_BY` · `MISSING_TARGET` · `CHAIN` · `종료 코드 0` 도 남아 있다. 알려진 답 대조: 가지 `chore/ak3-cx` 의 `harness/` 를 `git archive` 로 임시 폴더에 풀어 픽스처 두 판(못 읽는 새 판 · 다른 계약 / 모두 읽힘)에 돌린 출력의 줄 머리 낱말(`OK` 를 뺀 것)과 끝 줄 키가 모두 안내 덩어리에 있다. Given 공통 전제 G, When `m 스킬-01`, Then `cx_rc=2,0 cx_heads=OK,UNREADABLE cx_keys=checked,unreadable,violations known_ok=1 miss=[] ok=1` · 종료 코드 0 [exact, enumerated]
  측정: `m 스킬-01`. 시작 판 `block=357-370 cx_rc=2,0 cx_heads=OK,UNREADABLE cx_keys=checked,unreadable,violations known_ok=1 miss=[UNREADABLE <계약>,UNREADABLE <계약> -> <새 판>,unreadable=,종료 코드 2,못 읽,UNREADABLE,checked=,unreadable=,violations=] ok=0` · 종료 코드 1. 구현 뒤 모양 사본에서 `block=357-373 … miss=[] ok=1` · 종료 코드 0
  알려진 답: 픽스처 세 파일의 기대 출력은 스크립트 머리 주석(6 ~ 9 줄)에서 손으로 옮긴 두 줄 모양 · 끝 줄 · 종료 코드 2 이고, 봉인 전 실측 `cx_rc=2,0` · 줄 머리 `UNREADABLE` 둘 · `unreadable=2` 로 같다
- [ ] 스킬-02: 스킬 파일은 안내 덩어리 밖이 그대로다 — `git diff -U0 0928bf65..chore/ak3-last -- harness/skills/sprint-contract/SKILL.md` 의 변경 덩어리가 1 개 이상이고, 모두 시작 판 안내 덩어리 줄 범위 안(옛 쪽)이며 새 판 안내 덩어리 줄 범위 안(새 쪽)이다. Given 공통 전제 G, When `m 스킬-02`, Then `hunks` 1 이상 · `outside=0 ok=1` · 종료 코드 0 [exact]
  측정: `m 스킬-02`. 시작 판 `hunks=0 outside=0 ok=0` · 종료 코드 1. 구현 뒤 모양 사본에서 `hunks=1 outside=0 ok=1`. 양성 대조: 구현 뒤 모양 사본에 안내 밖 13 줄 제목 `# Sprint Contract` 도 고친 커밋을 얹으면 `OUT -13,1 +13,1 …` · `hunks=2 outside=1 ok=0` · 종료 코드 1 (봉인 전 실측). 줄 범위 비교는 도우미 `m_skill_scope` 가 덩어리 머리 `@@ -a,b +c,d @@` 로 한다

## Script

- [ ] 스크립트-01: Mermaid 검사가 그림 종류 이름이 틀린 예시를 안 그려진 예시로 잡는다 — 레포 쪽 사본 셋 ① `flows-typo`(`docs/planning-kit/flows.html` 첫 예시 `flowchart LR` → `flowchat LR`) ② `ref-typo`(`docs/planning-kit/reference.html` 의 `xychart-beta` → `xychat-beta`) ③ `flows-front-typo`(① 의 자리에 `---` / `title: 흐름 예시` / `---` 머리말과 `flowchat LR`)를 각각 인자로 주면 종료 코드 1 이고 출력에 그 사본 이름이 적힌다. Given 공통 전제 G, When `m 스크립트-01`, Then 세 줄 `OK` · `cases=3 right=3 ok=1` · 종료 코드 0 [exact, enumerated]
  측정: `m 스크립트-01` — 도우미 `MUTATIONS` 가 원본 쪽에서 `<pre …>` 부터 종류 이름 앞까지를 정규식으로 한 곳만 찾아 바꾼다(한 곳이 아니면 `NOT_APPLIED` · 종료 코드 2 — 이름표를 붙여도 맞는다). 시작 판 `BAD` 셋(`rc=0` · `예시 3` · `예시 2` · `예시 3`) · `cases=3 right=0 ok=0` · 종료 코드 1 (결함 재현). 구현 뒤 모양 사본에서 `right=3`(끝 줄 `예시 4 · 안 그려진 예시 1` · `예시 3 · 안 그려진 예시 1` · `예시 4 · 안 그려진 예시 1`)
- [ ] 스크립트-02: 머리말 붙은 정상 예시는 그려진 예시로 센다 — 사본 둘 ④ `flows-front`(① 의 자리에 머리말과 정상 `flowchart LR`) ⑤ `ref-front`(`reference.html` 의 `mindmap` 앞에 머리말)를 각각 주면 종료 코드 0 이고 끝 줄이 ④ `쪽 1 · 예시 4 · 안 그려진 예시 0` ⑤ `쪽 1 · 예시 3 · 안 그려진 예시 0` 이다(예시 하나도 빠지지 않는다). Given 공통 전제 G, When `m 스크립트-02`, Then 두 줄 `OK` · `cases=2 right=2 ok=1` · 종료 코드 0 [exact, enumerated]
  측정: `m 스크립트-02`. 시작 판 `BAD` 둘(`예시 3` · `예시 2`, 종료 코드 0) · `right=0` · 종료 코드 1. 구현 뒤 모양 사본에서 `right=2`. 알려진 답: 쪽별 예시 수 4 · 3 은 쪽의 `<pre>` 가운데 Mermaid 예시를 손으로 센 값이다(flows 482 · 578 · 635 · 696 줄, reference 598 · 610 · 628 줄)
- [ ] 스크립트-03: 세지 말아야 할 `<pre>` 는 여전히 세지 않고, 레포 전체 수는 그대로다 — 인자 없이 돌린 끝 줄이 `쪽 3 · 예시 9 · 안 그려진 예시 0` · 종료 코드 0 이고(레포 쪽의 Mermaid 아닌 이름표 `<pre>` 넷 — `Reflection YAML 스키마` · `Promotion Ledger YAML 스키마` · `Project ID 포맷` · `환경 오설정 TSV 스키마` — 을 세면 9 가 넘는다), 이름표가 `셸 명령 예시` · `Reflection YAML 스키마` 인 `<pre>` 둘만 있는 임시 쪽은 예시 0 · 종료 코드 3 이다. Given 공통 전제 G, When `m 스크립트-03`, Then `repo_ok=1 shell_rc=3 shell_ok=1` · 종료 코드 0 [exact, enumerated]
  측정: `m 스크립트-03`. 시작 판 `rc=0 tail=[쪽 3 · 예시 9 · 안 그려진 예시 0] repo_ok=1 shell_rc=3 shell_ok=1` · 종료 코드 0 (지킬 동작). 양성 대조: 이름표가 있기만 하면 세는 구현이면 `shell_ok=0` 이다 — 봉인 전 구현 뒤 모양 사본에서 이름표 판정식 `/^Mermaid .*예시$/` 를 `/./` 로 바꾸면 `tail=[쪽 4 · 예시 13 · 안 그려진 예시 4] repo_ok=0 shell_rc=1 shell_ok=0` · 종료 코드 1
- [ ] 스크립트-04: Mermaid 검사 시험이 두 모양을 실패 경우로 갖고 CI 이름이 맞다 — `node scripts/test-check-docs-mermaid.js` 가 기존 네 경우에 더해 ⑤ 그려지는 예시와 `aria-label="Mermaid flowchart 예시"` 가 붙은 `flowchat LR` 예시 쪽 → 검사 종료 코드 1 ⑥ 그려지는 예시와 같은 이름표에 머리말 + `flowchat LR` 예시 쪽 → 1 ⑦ 같은 이름표에 머리말 + 정상 `flowchart LR` 예시만 있는 쪽 → 0 · 출력에 `예시 1 · 안 그려진 예시 0` ⑧ 그려지는 예시와 `aria-label="셸 명령 예시"` 인 `ls -la` `<pre>` 쪽 → 0 · 출력에 `예시 1 · 안 그려진 예시 0` 을 확인하고 끝 줄 `경우 8 개 중 통과 8` · 종료 코드 0 을 낸다. 시험 머리 설명이 「여덟 경우」 를 적거나 경우 5 ~ 8 을 번호로 적고, `.github/workflows/ci.yml` 의 `playwright` 묶음 `run: node scripts/test-check-docs-mermaid.js` 단계가 정확히 1 개 · `run: npm ci` 뒤 · 이름에 「여덟 경우」 가 있다. Given 공통 전제 G, When `m 스크립트-04`, Then `test_ok=1 base_rc=1 base_fails=5,6,7 base_ok=1 stub_ok=1 head_ok=1 ci_ok=1` · 종료 코드 0 [exact, enumerated]
  측정: `m 스크립트-04`. 시작 판 `test_rc=0 test_tail=[경우 4 개 중 통과 4] test_ok=0 base_rc=0 base_fails= base_ok=0 stub_rc=1 stub_ok=1 head_ok=0 ci_ok=0` · 종료 코드 1
  음성 대조: 시작 판 검사(`git show 0928bf65:scripts/check-docs-mermaid.js` 를 레포 `scripts/` 옆 임시 이름으로 꺼냄 — node_modules 를 레포에서 찾게)를 `--check` 로 주면 경우 5 · 6 · 7 만 `FAIL` 이고 시험 종료 코드 1 (`base_fails=5,6,7`) — 고치기 전 판은 두 모양을 통과시키고 고친 판은 잡는다는 뜻이다. 경우 8 은 시작 판도 통과한다(세지 말아야 할 것을 안 세는 동작은 전부터 맞다). 늘 `쪽 0 · 예시 0 · 안 그려진 예시 0` 과 0 을 내는 가짜 검사(도우미가 임시 폴더에 새로 쓰는 `stub-check.js`)는 시험 종료 코드 1 (`stub_ok`). 구현 뒤 모양 사본에서 `base_fails=5,6,7 stub_rc=1`

## Error

- [ ] 오류-01: 이름표 붙은 빈 예시는 건너뛰지 않고 안 그려진 예시로 센다 — 그려지는 예시 하나와 `<pre aria-label="Mermaid flowchart 예시"></pre>` 가 있는 임시 쪽을 주면 종료 코드 1 · 끝 줄 `쪽 1 · 예시 2 · 안 그려진 예시 1` 이다. Given 공통 전제 G, When `m 오류-01`, Then `rc=1 … ok=1` · 종료 코드 0 [exact]
  측정: `m 오류-01`. 시작 판 `rc=0 tail=[쪽 1 · 예시 1 · 안 그려진 예시 0] ok=0` · 종료 코드 1 (빈 예시를 빼고 셈). 구현 뒤 모양 사본에서 `rc=1 … ok=1`
- [ ] 오류-02: 앞 묶음 tail 의 Mermaid 측정이 이 판에서도 통과한다 — `python3 .harness/.meta/after-0929-tail/measure.py 스크립트-04`(레포 쪽 셋 · 예시 9 · 따로 짠 그리기 `pages=3 examples=9 bad=0` · 괄호 깨진 flows 사본이 종료 코드 1)가 종료 코드 0 이다. Given 공통 전제 G, When `m 오류-02`, Then `tail_rc=0 ok=1` · 종료 코드 0 [exact]
  측정: `m 오류-02`. 시작 판 `tail_rc=0 ok=1` · 종료 코드 0. 봉인 전 사본 대조: 구현 뒤 모양 사본에서도 종료 코드 0 (「더하라」 조건 스크립트-01 ~ 04 와 「그대로」 조건 오류-02 가 함께 겨누는 파일 `scripts/check-docs-mermaid.js` 에서 부딪히지 않는다). tail 의 `스크립트-05`(시험 네 경우 · CI 이름 「네 경우」)는 이 계약이 일부러 바꾸므로 지키지 않는다 — `## 범위 경계`

## Architecture

- [ ] 구조-01: 규약 문서와 그 쪽이 못 읽는 경우를 같이 적는다 — `harness/references/contract-schema.md` 의 `| \`superseded_by\` |` 로 시작하는 행과 `docs/harness/contract-schema.html` 의 `<tr><td><code>superseded_by</code></td>` 행이 모두 `UNREADABLE` 과 `종료 코드 2` 를 담고(쪽은 보이는 글로), 두 행의 인라인 코드 집합(원본 백틱 · 쪽 `<code>`)이 같다. Given 공통 전제 G, When `m 구조-01`, Then `md_need_ok=1 page_need_ok=1 codes_only_md=[] codes_only_page=[] codes_same=1` · 종료 코드 0 [exact, enumerated]
  측정: `m 구조-01`. 시작 판 `md_row=1 page_row=1 md_need_ok=0 page_need_ok=0 codes_only_md=[] codes_only_page=[] codes_same=1` · 종료 코드 1. 구현 뒤 모양 사본에서 종료 코드 0. 양성 대조: 구현 뒤 모양 사본의 원본 행에만 인라인 코드 `EXTRA` 를 더하면 `codes_only_md=[EXTRA] codes_same=0` · 종료 코드 1 (봉인 전 실측)
- [ ] 구조-02: 이번에 바뀐 docs 쪽(`git diff --name-only 0928bf65..HEAD -- docs` 의 `.html` — 구현 뒤 `docs/harness/contract-schema.html` · `docs/planning-kit/reference.html`)이 두 테마(`dark` · `light`) 각각 320 · 375 · 1280 폭에서 가로 넘침 0 이다. Given 공통 전제 G, When `m 구조-02`, Then `pages` 1 이상 · `bad=0 br_rc=0,0` · 종료 코드 0 [exact]
  측정: `m 구조-02` (rest `m_overflow` 를 이 기준 판으로). 시작 판 `pages=0 themes=2 bad=0 br_rc=0,0` · 종료 코드 1 (바뀐 쪽 없음). 양성 대조는 같은 함수로 rest 가 봉인 전에 쟀다(폭 2000px 상자 사본 → `of=1680/1625/720`)
- [ ] 구조-03: 바뀐 docs 파일(`.html` · `.css` · `.js`)이 레포 밖 자원을 부르지 않는다 — fs2 구조-10 과 같은 식. Given 공통 전제 G, When `m 구조-03`, Then `checked` 1 이상 · `ext_files=0` · 종료 코드 0 [exact]
  측정: `m 구조-03`. 시작 판 `checked=0 ext_files=0 git_rc=0` · 종료 코드 1. 양성 대조는 같은 함수로 fs2 가 봉인 전에 쟀다(`ext_files=3`)
- [ ] 구조-04: 커밋 규칙 — `0928bf65..HEAD` 의 커밋마다 합침 커밋이 아니고, 맨 위 폴더가 하나(docs 는 `docs/<폴더>` 하나 — `docs/harness` · `docs/planning-kit` 은 서로 다른 폴더)이며, `.harness/` 파일은 구현 파일과 다른 커밋이고, 서명 줄(`git log -1 --format='%(trailers:key=Co-Authored-By,valueonly)'`)이 `Claude … <noreply@anthropic.com>` 모양이며, 바뀐 파일이 모두 `## 범위 경계` 의 `# sprint-scope` 목록(또는 `.harness/`) 안이다. Given 공통 전제 G, When `m 구조-04`, Then 모든 줄 `OK` · `bad=0` · 종료 코드 0 [exact]
  측정: `m 구조-04` (tail `m_commits` 를 이 기준 판 · 계약으로). 시작 판 `commits=0` · 종료 코드 1
- [ ] 구조-05: 기록 — `.harness/.meta/after-kaizen-0928/last-notes.md` 에 낱말 `check-docs-mermaid` · `aria-label` · `flowchat` · `머리말` · `UNREADABLE` · `check-superseded` · `contract-schema` · `tone-guide`(1 단계 · 5 단계 결과) · `남긴 것` 이 모두 있고, 서로 다른 8 자리 16 진수(처리 커밋 해시) 3 개 이상이 있다. Given 공통 전제 G, When `m 구조-05`, Then `keys_ok=1 miss=[] hashes_ok=1` · 종료 코드 0 [exact, enumerated]
  측정: `m 구조-05`. 시작 판 파일 없음 · `keys_ok=0` · 종료 코드 1

## Anti-patterns

- [ ] 금지-02: force push 금지 (측정: 이 스프린트는 push 하지 않는다 — `git reflog show chore/ak3-last` 에 `forced-update` 0 줄)
- [ ] 금지-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수 (측정: `python3 scripts/validate-plugin.py --check=code-fence` 종료 코드 0, 그리고 바뀐 `.md` 세 파일에 markdownlint MD040 0 건 — 진단-02 와 같은 명령)
- [ ] 금지-04: SKILL.md / agents/*.md frontmatter 에서 name 필드 누락 — validate-plugin V1 FAIL (측정: `python3 scripts/validate-plugin.py harness --check=frontmatter` 종료 코드 0. 시작 판 종료 코드 0)

## Reusability

- [ ] 재사용-01: 다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다 (측정: 새 코드는 기존 검사 · 시험 파일 안의 판정 한 곳과 시험 경우뿐이고, 검사 · 시험은 CI 에 등록돼 누구나 부른다 — 스크립트-04 `ci_ok`)
- [ ] 재사용-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다 (측정: 새 검사 · 새 시험 파일을 만들지 않고 기존 `scripts/check-docs-mermaid.js` · `scripts/test-check-docs-mermaid.js` 를 고친다 — `git diff --name-status 0928bf65..chore/ak3-last -- scripts` 에 `A` 줄 0. 예시 표시는 쪽에 이미 있는 `aria-label="Mermaid … 예시"` 모양을 그대로 쓴다)

## Diagnostics

- [ ] 진단-01: N/A (commands.analyze 는 scripts/release.sh 만 잰다 — 이번 변경 파일과 교집합 0 개. 측정: git diff --name-only 0928bf65..chore/ak3-last | grep -c '^scripts/release.sh$' 이 0)
- [ ] 진단-02: IDE diagnostics 워닝/인포 0개 ([] 제외) — 바뀐 `.md` 세 파일(`harness/skills/sprint-contract/SKILL.md` · `harness/references/contract-schema.md` · `.harness/.meta/after-kaizen-0928/last-notes.md`)은 markdownlint-cli2(MD013 끔)로 경고 0 건 · 검사기가 돈 줄 `Linting: 1 file`, 바뀐 `.js` 둘(`scripts/check-docs-mermaid.js` · `scripts/test-check-docs-mermaid.js`)은 `node --check` 종료 코드 0
  측정: 파일마다 `<scratch>/mdl/node_modules/.bin/markdownlint-cli2 --config <scratch>/rest/mdl/mdl.jsonc <파일> 2>&1 | grep -cE ' MD[0-9]{3}'` 이 0 이고 같은 출력에 `Linting: 1 file` 이 있다(설정 파일 내용 `{ "config": { "MD013": false } }`, `<scratch>` = `/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/bda55d45-296c-491f-89ba-b52042d58e72/scratchpad`). 시작 판 앞 두 파일 `warn=0 ran=1`, 구현 뒤 모양 사본 두 파일 `warn=0`. 양성 대조: tail 이 봉인 전에 같은 명령으로 잰 `pos.md` → 경고 4
- [ ] 진단-03: N/A (commands.test 대상도 scripts/release.sh 라 이번 변경 파일에 없다. 측정: 진단-01 과 같은 명령)
- [ ] 진단-04: N/A (구동할 앱 · 서버가 없다 — 산출물은 검사 스크립트 · 시험 · 문서 쪽 · 스킬 · 규약 문서 · CI 파일 · 기록. 측정: git diff --name-only 0928bf65..HEAD -- . ':(exclude).harness' | grep -cvE '^(docs/|scripts/|\.github/|harness/skills/sprint-contract/SKILL\.md$|harness/references/contract-schema\.md$)' 이 0. 쪽을 브라우저로 여는 확인은 스크립트-01 ~ 04 · 오류-01 · 구조-02 가 한다)
- [ ] 진단-05: 로컬 CI 와 CI 파일에만 있는 단계가 모두 통과한다 — `bash /Users/jackson/Hub/10_Dev/claude-plugins/.harness/handoff/2026-09-26-tools/ci-local.sh <W>` (TMPDIR 은 scratch 아래 새 폴더)의 단계가 모두 `rc=0`(yq 없는 `feedback-agg-test SKIP` 만 예외)이고 `docs-a11y` 로그 끝이 `206/206 PASS`, 그리고 `python3 scripts/check-api-kit-docs.py` · `python3 scripts/test-check-api-kit-docs.py` · `python3 scripts/detect-docs-drift.py --check-table` · `python3 scripts/test-detect-docs-drift.py` · `python3 scripts/check-docs-common-css.py` · `python3 scripts/test-check-docs-common-css.py` · `python3 scripts/check-cause-table-copies.py` · `python3 scripts/check-install-docs-guidance.py` · `python3 scripts/test-check-cause-table-copies.py` · `bash scripts/test-ci-local.sh` · `bash harness/evals/measure/measure-helpers-test.sh` · `bash harness/evals/superseded/check-superseded-test.sh` · `bash harness/scripts/check-superseded.sh .harness` · `bash bambu-kit/evals/run-gate-fixtures.sh` · `bash bambu-kit/evals/makerworld-fetch-test.sh` · `npx playwright test` · `node scripts/check-docs-mermaid.js` · `node scripts/test-check-docs-mermaid.js` 의 종료 코드가 모두 0 [exact, enumerated]
  측정: 위 명령들의 종료 코드와 `grep -c 'rc=0' <TMPDIR>/ci-local/summary.txt`. 봉인 전 시작 판 · 구현 뒤 모양 사본 값은 `## 회귀 게이트` 에 적는다

## 범위 경계

- 이 계약이 고칠 경로는 아래 블록뿐이다. `.harness/` 아래(이 계약 · 기록 · 측정 묶음)는 늘 허용된다.

```text
# sprint-scope
scripts/check-docs-mermaid.js
scripts/test-check-docs-mermaid.js
.github/workflows/ci.yml
docs/planning-kit/reference.html
harness/skills/sprint-contract/SKILL.md
harness/references/contract-schema.md
docs/harness/contract-schema.html
```

- 하지 않는 것: `harness/scripts/check-superseded.sh` · 그 시험 고치기(가지 `chore/ak3-cx` 몫), 이름표 없는 `<pre>` 의 종류 이름 오타 잡기(이름표 없는 예시는 새 쪽에 생길 수 있으나, 레포 예시 9 개는 구현 뒤 모두 이름표를 가진다 — 쪽을 더하는 사람이 이름표를 붙인다는 규칙은 이번에 문서로 올리지 않는다), 원본 `.md` 울타리를 그려 보기, `docs/planning/reference.md` 고치기(이름표는 쪽에만 있는 속성이라 원본에 대응 글이 없다), `docs/planning-kit/flows.html` · `data-modeling.html` 고치기, 킷 버전 올리기 · 릴리스 · 합치기 · push, 로컬 CI 도구 `ci-local.sh`(레포 밖) 고치기, `.harness/` 아래 봉인된 계약 · QA 리포트 · 개정 파일 고치기.
- 앞 묶음 봉인 측정 가운데 이번 변경이 일부러 바꾸는 것(그 계약은 `status: done` 이고 이 계약의 조건을 느슨하게 하지 않는다): tail 계약 `스크립트-05` 측정이 적은 시험 끝 줄 `경우 4 개 중 통과 4` 와 CI 단계 이름 「네 경우」 는 여덟로 는다(경우를 더하는 쪽이라 더 엄격하다). tail `진단-05` 의 Mermaid 두 명령은 종료 코드 0 으로 그대로 잰다.
- 커밋: `git add <경로>` 뒤 `git commit -o <경로>`. `git add -A` · `git stash` · push · 가지 바꾸기 금지. 메시지 한국어, 끝에 빈 줄 뒤 서명 줄 「Co-Authored-By: Claude Opus 5.5 (1M context) <noreply@anthropic.com>」. 한 커밋에 맨 위 폴더 하나 — `scripts/` · `.github/` · `harness/` 는 따로, docs 는 `docs/planning-kit` · `docs/harness` 따로. 봉인 커밋(계약 파일 하나)과 측정 묶음 커밋(`.harness/.meta/after-0930-last/`)은 따로다.

## 회귀 게이트 — 측정 도우미 · 봉인 전 실측

- 도우미 `m <조건 번호>` = `python3 .harness/.meta/after-0930-last/measure.py <조건 번호>` (W 맨 위 폴더에서, 종료 코드 0 성립 · 1 불성립 · 2 잴 수 없음). 넘침 · 밖 자원 · 커밋 규칙 · CI 단계 읽기는 tail 도우미 `.harness/.meta/after-0929-tail/measure.py` 와 그것이 부르는 rest · fs2 도우미를 불러 쓴다.
- 봉인 전 실측(2026-09-30, W 시작 판): 스킬-01 · 스킬-02 · 스크립트-01 · 스크립트-02 · 스크립트-04 · 오류-01 · 구조-01 · 구조-02 · 구조-03 · 구조-04 · 구조-05 종료 코드 1(결함 재현 · 산출물 없음), 스크립트-03 · 오류-02 종료 코드 0(지킬 동작). 값은 각 조건 측정 줄에 있다.
- 진단-05 봉인 전 실측 — 시작 판(W): ci-local 25 단계 `rc=0` · `feedback-agg-test SKIP (yq 없음)` · `docs-a11y` `206/206 PASS`, CI 전용 명령 열여덟 모두 종료 코드 0 (`12/12 PASS` · `경우 10 개 중 통과 10` · `어긋남 0` · `경우 3 개 중 통과 3` · `검사한 쪽 206 · 어긋난 쪽 0 · 못 읽은 쪽 0` · `경우 8 개 중 통과 8` · `checked=2 violations=0 infra_errors=0` · `need=0` · `실패 0 건` 넷 · `checked=6 violations=0` · `28 경우 중 불일치 0` · `5 경우 중 불일치 0` · `174 passed` · `쪽 3 · 예시 9 · 안 그려진 예시 0` · `경우 4 개 중 통과 4`).
- 봉인 전 사본 대조(구현 뒤 모양 scratch 사본 `git clone --shared` 뒤 검사 판정 · 시험 경우 5 ~ 8 · CI 이름 한 줄 · reference 이름표 셋 · 스킬 안내 세 줄 · 규약 문서 · 쪽 한 문장을 폴더별 서명 커밋 다섯에 담고 기록 · 계약 · 도우미 커밋 셋, 2026-09-30): 이 계약 측정 열셋(스킬-01 · 02, 스크립트-01 ~ 04, 오류-01 · 02, 구조-01 ~ 05) 모두 종료 코드 0 (구조-02 `pages=2` · 구조-03 `checked=2 ext_files=0` · 구조-04 `commits=8 bad=0`). 같은 사본에서 ci-local 25 단계 `rc=0` · `docs-a11y` `206/206 PASS`, 진단-05 의 CI 전용 명령 열여덟 모두 종료 코드 0 (Mermaid 시험만 `경우 8 개 중 통과 8` 로 바뀜), `python3 scripts/detect-docs-drift.py --since 0928bf65` 짝은 `harness/references/contract-schema.md → docs/harness/contract-schema.html` 하나(구조-01 이 맞춘다), `node --check` 두 파일 · 스킬 · 규약 문서 markdownlint 경고 0, `python3 scripts/validate-plugin.py --check=code-fence` · `harness --check=frontmatter` 종료 코드 0.
- 교차 대조(봉인 전): 바뀌는 글자 · 파일(`check-docs-mermaid` · `test-check-docs-mermaid` · `aria-label` · `reference.html` · `contract-schema` · `sprint-contract/SKILL.md` · `check-superseded` · `MISSING_BY`)을 읽는 기존 검사를 `scripts/` · `.github/` · `harness/evals/` · `harness/scripts/` 에서 `grep` 으로 찾았다 — `.github/workflows/ci.yml`(Mermaid 두 단계 — 스크립트-04 가 이름을 고친다), `scripts/detect-docs-drift.py`(원본 → 쪽 짝 — 구조-01 이 두 쪽을 같이 고친다), `scripts/check-install-docs-guidance.py` · `scripts/validate-plugin.py`(규약 문서 · 스킬을 읽는다 — 사본에서 종료 코드 0), `harness/evals/gate-exit-codes.md`(check-superseded 줄 `0 · 1 · 2` 이미 있음 — 고치지 않는다), `harness/evals/superseded/check-superseded-test.sh`(스크립트만 잰다 — 이 계약 밖). 「더하라」 조건(스크립트-01 ~ 04 · 스킬-01 · 구조-01)과 「그대로」 조건(스크립트-03 · 오류-02 · 스킬-02 · 진단-05)이 함께 겨누는 파일은 `scripts/check-docs-mermaid.js` · `harness/skills/sprint-contract/SKILL.md` 이고, 위 사본에서 두 쪽이 모두 종료 코드 0 이라 부딪히지 않는다. CI 전용 단계와 범위 목록을 맞대면 범위 밖 스크립트를 고쳐야 하는 경우는 없다.
- 도우미 지문(봉인 전, `shasum -a 256 <파일> | cut -c1-16`): 이 계약 `measure.py` `8aabd86cb275ad35` · tail `measure.py` `3d920fd41c46e7f6`.
- 커버리지 해소: 스크립트-01 · 스크립트-02 — 사본 다섯의 이름 · 원본 쪽(`FLOWS` = `docs/planning-kit/flows.html` · `REF` = `docs/planning-kit/reference.html`) · 바꿀 글 · 기대 종료 코드 · 끝 줄은 도우미 `MUTATIONS` 한 곳에 글자 그대로 있고 `m` 이 사본마다 한 줄을 찍는다.
- 커버리지 해소: 스크립트-03 — Mermaid 아닌 이름표 넷은 레포 쪽 전체 실행(예시 9)이 덮고, 임시 쪽 두 이름표는 도우미 `m_repo` 에 글자 그대로 있다.
- 커버리지 해소: 스크립트-04 — 경우 5 ~ 8 의 쪽 내용은 시험 파일의 몫이고, 도우미는 끝 줄 · 실패 경우 번호 · CI 이름으로 잰다.
- 커버리지 해소: 스킬-01 — 낱말 목록은 도우미 `m_skill` 의 `lits` 에, 스킬 파일 경로 · 가지 이름 · 풀어 쓸 폴더(`harness`)는 `SKILL` · `CX` · `cx_runs` 에 글자 그대로 있다. `check-superseded.sh` 는 안내 덩어리를 찾는 첫 줄 글이다.
- 커버리지 해소: 구조-01 — 두 파일 경로와 행 머리 글은 도우미 `SCHEMA_MD` · `SCHEMA_PAGE` · `schema_rows` 에 글자 그대로 있다.
- 커버리지 해소: 진단-02 · 진단-05 — 파일 · 명령 목록이 조건 줄 안에 백틱으로 있다.
- 오라클 해소: 스크립트-01 ~ 04 · 오류-01 · 진단-05 — 글자 찾기가 아니라 검사 · 시험을 실제로 돌린 종료 코드 · 끝 줄로 판정한다. 스크립트-04 는 음성 대조(시작 판 검사 · 가짜 검사)가 붙어 있다.
- 오라클 해소: 스킬-01 — 안내 글 찾기에 더해, 새 모양의 정본인 `chore/ak3-cx` 스크립트를 픽스처에 실제로 돌려 나온 줄 머리 · 끝 줄 키를 안내와 맞댄다. 안내 글만 보고 스크립트와 어긋난 모양을 적으면 `miss` 에 걸린다.
- 오라클 해소: 진단-02 — 글자 찾기가 아니라 markdownlint · `node --check` 를 실행해 그 출력으로 판정하고, 양성 대조(경고 4)가 있다.
- 오라클 해소: 구조-01 — 원본 · 쪽 글을 고치는 것 자체가 요구다. 두 행의 인라인 코드 집합을 맞대어 한쪽만 고친 경우를 잡는다.
- 교차 진단(봉인 전, qa-evaluator): 측정이 늘 0 · 늘 실패인 곳 없음, 음성 · 양성 대조 성립, 조건을 고칠 지적 없음. 이 가지 `check-superseded.sh` 가 못 읽는 계약을 통과로 치는 결함은 `chore/ak3-cx` 가 종료 코드 2 로 고친다 — 기록 파일 `남긴 것` 에 그 가지가 합쳐져야 풀린다고 적는다.
