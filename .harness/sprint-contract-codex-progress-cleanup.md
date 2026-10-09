---
feature: "Codex 진행 표시 정리 — 최신 활동 우선 · 사용량 한 줄 · 상태 폴더와 VS Code 확장 지우기"
slug: codex-progress-cleanup
created: "2026-10-09 18:25"
complexity: "중간"
conditions: 17
status: active
owner_session: 35b5945f-4957-4359-9b18-2d22b3bafeb0
conditions_digest: sha256:349ecc1a78930b5d
measurement_digest: sha256:baf5e2a7ca2fd1be
locked_at: "2026-10-09 20:47"
---

## 배경

- 앞 스프린트 `codex-research-activity`(APPROVE, 같은 가지)의 교차 진단 중간 3 건과 사용자 결정(2026-10-09 18:1x, 네 질문 모두 추천안): (1) 한 주기 활동이 6 개를 넘으면 **최신 6 개**를 보이고 앞선 것은 `  …앞서 N개` 한 줄로 묶는다. (2) 사용량은 **머리 줄 하나**로 — 머리 줄의 `5시간 N% · 주간 N%`(쓴 양)만 남기고, 시작 줄 `남은 한도 약 N%` 와 완료 · 실패 줄 끝 `남은 한도 N%` 는 내지 않는다. 머리 줄 사용량은 상태 폴더 파일이 아니라 **이번 차례 세션 기록의 마지막 `token_count` · `rate_limits`** 에서 읽는다(다른 세션 값을 짐작하지 않는다). (3) 이제 안 쓰는 VS Code 확장(`harness/vscode-status/`)과 그것을 위한 상태 폴더(`~/.codex-status`, `CODEX_STATUS_DIR`) 쓰기를 감독 · 리서치 양쪽에서 지운다. (4) 고친 뒤 진짜 Codex 리서치로 한 번 확인한다.
- 사용량 상한(`usage_limit_percent`)은 그대로 — 감독은 사용 기록 `codex-audit-usage.jsonl` 의 `limits` 로 막는다(상태 폴더 `usage.json` 은 표시 전용이었다). 래퍼의 한도 판정(`LIMIT_FLOOR` · 작은 모델로 내리기)도 그대로 두고 **보여 주는 줄만** 뺀다.
- 지울 자리(레포, 18:2x 실측 `grep`): `harness/scripts/codex-audit.sh` 의 `status_dir` · `write_json` · `class Board` · `self.board` · `note()` 의 표시판 쓰기 · `record_usage()` 의 `usage.json` 쓰기 · `run()` 의 표시판 만들기 · 닫기, `harness/vscode-status/` 6 파일, `harness/README.md` 132 줄 「Codex 진행 상황 표시줄」 문단. 레포 밖: `~/.claude/bin/codex-research` 의 상태 파일 · `usage.json` 쓰기와 그 정리 trap.
- 측정 묶음 `.harness/.meta/codex-progress-cleanup/measure/`:
  - `research.py` + `fake/codex` — 앞 스프린트 측정을 가져와 `burst` 를 최신 우선으로 바꾸고 `usage` · `nousage` · `nostatus` 를 더했다. 가짜 `ok` 시나리오는 실제 모양의 `token_count` 사건(null 하나 뒤 5시간 11% · 주간 28%)을 쓴다. `--base` 는 이번 정리 직전 래퍼 백업 `~/.claude/bin/codex-research.bak-20261009d` 를 잰다.
  - `audit.sh`(`audit.py` + `fake_audit.py`) — `codex-status-bar` 측정의 감독 실행 준비(`Case`)를 가져와, 가지 끝 커밋의 `harness/` 로 가짜 codex 감독을 끝까지 돌린다. `--base` 는 기준 커밋 `ae918dab`.
  - 봉인 전 `--base` 실측(교차 진단 반영 뒤): `burst` · `usage` · `nostatus` · `flush` · `reuse` · `감독-01` · `구조-01` 은 FAIL, `activity` · `nousage` · `감독-02` 는 PASS(지켜야 할 기존 동작). 가짜 `ok` · `fail-then-ok` 는 이 차례보다 새로운 미끼 세션 기록(77 % · 66 %)을 같은 폴더에 만든다.
- 기존 검사 기준(18:25): `python3 scripts/validate-plugin.py harness` 종료 코드 0, `python3 scripts/sync-docs.py --check-only` 「모든 README가 동기화 상태입니다.」, 래퍼 `shellcheck -S warning` 0 줄.

### 복잡도 표

| 축 | 물음 | 값 |
| -- | ---- | -- |
| 레이어 수 | 몇 개 계층을 관통하는가 | 2 — 감독 스크립트 · 리서치 래퍼(+ 문서) |
| 공개 API·계약 변경 | 바깥에서 보는 모양이 바뀌는가 | 예 — 진행 줄 모양 · 상태 폴더 사라짐 |
| 소비면 존재 | 받아 쓰는 반대편이 있는가 | 아니오 — 상태 폴더를 읽던 확장을 같이 지운다(다른 소비자 `grep` 0) |
| 회귀 위험 | 기존 동작이 깨질 경로가 있는가 | 예 — 감독 끝내기 · 사용량 상한 · 앞 스프린트 진행 줄 |

2 축이 「예」 → 중간.

## 범위 경계

```text
# sprint-scope
harness/scripts/codex-audit.sh
harness/README.md
harness/vscode-status/
.harness/sprint-contract-codex-progress-cleanup.md
.harness/sprint-feedback-codex-progress-cleanup.md
.harness/sprint-amendments-codex-progress-cleanup.md
.harness/.meta/codex-progress-cleanup/
```

- 레포 밖: `~/.claude/bin/codex-research` 만. 전역 규칙 · 템플릿 문장은 앞 스프린트 그대로(「사용량」 낱말은 머리 줄 설명이라 맞다).
- 하지 않는 것: 래퍼의 한도 판정 로직(`remaining_percent` · `LIMIT_FLOOR`) 수정, 감독 진행 표시(`follow`) 변경, 사용자 맥에 남은 `~/.codex-status` 폴더 지우기(사용자 파일 — 끝나고 알려만 준다).

## Skill

- [ ] 스킬-00: N/A (스킬 파일을 바꾸지 않는다 — 범위 목록에 `SKILL.md` 0 개)

## Script

- [ ] 스크립트-01: Given 한 호출에 검색어 12 개(`burst q01`~`burst q12`)가 한꺼번에 기록될 때, Then 한 번에 내는 들여쓴 줄은 7 줄 이하이고, `  …앞서 6개` 줄 바로 뒤에 `  검색: burst q07`~`  검색: burst q12` 여섯 줄이 차례로 오며, `burst q01`~`burst q06` 은 표준 오류에 0 번이다 [exact]
  - 측정: `python3 .harness/.meta/codex-progress-cleanup/measure/research.py burst` 종료 코드 0 이고 출력에 `FAIL` 0 줄
  - 음성 대조: `--base` 는 앞쪽 6 개를 남겨 FAIL(실측). 상한을 빼면 7 줄 넘게 되어 FAIL 한다
- [ ] 스크립트-02: Given 이번 차례 세션 기록에 `token_count` 사건이 null · 5시간 11 % 주간 28 % · 5시간 14 % 주간 30 % · null 순서로 있고, 같은 세션 폴더에 이 차례보다 새로운 다른 세션 기록(5시간 77 % · 주간 66 %)이 있을 때, Then 머리 줄 하나 이상이 `· 5시간 14% · 주간 30%` 로 끝나고(「마지막」 = 이번 차례 기록에서 `rate_limits` 가 null 이 아닌 마지막 사건), `77%` · `66%` 는 표준 오류에 0 번, `남은 한도` 를 담은 줄이 0, `완료 (시도 1/2` 줄이 있다 [exact]
  - 측정: `python3 .harness/.meta/codex-progress-cleanup/measure/research.py usage` 종료 코드 0 이고 출력에 `FAIL` 0 줄
  - 음성 대조: `--base` 는 사용량을 상태 폴더 파일에서 읽어 머리 줄에 없고 완료 줄에 `남은 한도` 가 있어 FAIL(실측). 가장 새로운 세션 기록을 읽는 구현이면 77 · 66 이 나와 FAIL 한다
- [ ] 스크립트-03: Given 이번 차례 기록에 사용량 사건이 없고(시도 1 실패 · 시도 2 성공) 같은 세션 폴더에 더 새로운 다른 세션 기록(77 % · 66 %)이 있을 때, Then 머리 줄에 `%` 가 0 번이고 `Traceback` 0 · 종료 코드 0 이다 — 없는 사용량을 다른 기록에서 짐작해 채우지 않는다 [exact]
  - 측정: `python3 .harness/.meta/codex-progress-cleanup/measure/research.py nousage` 종료 코드 0 이고 출력에 `FAIL` 0 줄
  - 음성 대조: 머리 줄 사용량을 공용 파일이나 가장 새로운 세션 기록에서 읽으면 `%` 가 생겨 FAIL 한다. `--base` 는 PASS(실측 — 지켜야 할 동작)
- [ ] 스크립트-04: Given 래퍼를 상태 폴더(`CODEX_STATUS_DIR`)와 `HOME` 을 각각 임시 폴더로 가리켜 끝까지 돌릴 때, Then 종료 코드 0 이고 두 폴더에 생기거나 남은 파일이 0 이며, 래퍼 파일에 `CODEX_STATUS_DIR` · `.codex-status` · `status_write` · `usage_write` · `usage.json` · `STATUS_DIR` 여섯 낱말이 0 번이다 [exact, enumerated]
  - 측정: `python3 .harness/.meta/codex-progress-cleanup/measure/research.py nostatus` 종료 코드 0 이고 출력에 `FAIL` 0 줄
  - 음성 대조: `--base` 는 `usage.json` 이 생기고 여섯 낱말이 모두 있어 FAIL(실측)
- [ ] 스크립트-05: 앞 스프린트 동작이 그대로다 — `activity` · `forms` · `once` · `answer` · `length` · `retry` · `flush` · `partial` · `corrupt` · `monitor` · `docs` · `reuse` 12 측정이 각각 종료 코드 0 이다. 이 묶음의 `activity` 는 활동 6 개 이하 묶음에 `…앞서` 줄 0 을, `flush` 는 주기가 안 와 7 개가 한꺼번에 나올 때 최신 6 개 + `  …앞서 1개` 를, `reuse` 는 함수 수 = 정리 직전 판 − 2(`status_write` · `usage_write`)를 더 잰다 [exact, enumerated]
  - 측정: `python3 .harness/.meta/codex-progress-cleanup/measure/research.py <이름>` 을 12 이름에 각각 돌려 모두 종료 코드 0 (`burst` 는 스크립트-01 로 바뀌어 빠진다)
  - 음성 대조: `--base` 는 `flush`(앞쪽 6 개를 남김) · `reuse`(함수 수 17 → 17) 가 FAIL(실측), 나머지 10 개는 PASS. 앞 스프린트 판정에서 다섯 변이를 이 측정들이 잡았다
- [ ] 스크립트-06: Given 구현 커밋 뒤(작업 폴더의 `harness/scripts` · `harness/README.md` · `harness/vscode-status` 에 커밋 안 된 변경 0) 가지 끝 커밋의 `harness/` 로 가짜 codex 감독(impl)을 상태 폴더를 임시 폴더로 가리켜 돌릴 때, Then 판정 차례 중 · 끝난 뒤 · SIGTERM 뒤 · `--detach` 로 띄운 차례 중과 끝난 뒤 모두 상태 폴더 · 감독 `HOME`(`.codex-qa` 제외) · 임시 폴더의 `감독-*.json` 이 0 개이고, impl 은 종료 코드 0 이며, 사용 기록 `codex-audit-usage.jsonl` 의 마지막 `limits` 는 5시간 12 · 주간 3 이다 [exact]
  - 측정: `bash .harness/.meta/codex-progress-cleanup/measure/audit.sh 감독-01` 출력 `PASS 감독-01` (커밋 안 된 변경이 있으면 측정이 FAIL 로 끝난다)
  - 음성 대조: `--base` 는 `(a) 판정 차례 중 상태 폴더 파일: ['status/감독-<pid>.json']` 으로 FAIL(실측)

## Error

- [ ] 오류-00: N/A (오류 경로는 다른 조건이 이미 잰다 — 깨진 기록 줄은 스크립트-05 의 `corrupt`, 사용량 사건 null · 없음은 스크립트-02 · 스크립트-03, 막힌 감독은 재사용-02. 측정: 그 네 측정이 각각 종료 코드 0)

## Architecture

- [ ] 구조-01: 가지 끝 커밋에서 `harness/vscode-status` 아래 추적 파일 0 개, `harness/README.md` 에 `vscode-status` · `진행 상황 표시줄` · `CODEX_STATUS` · `.codex-status` 를 담은 줄 0, `harness/scripts/codex-audit.sh` 에 `status_dir` · `write_json` · `class Board` · `CODEX_STATUS` · `.codex-status` · `board` 여섯 낱말 0 번이다 [exact, enumerated]
  - 측정: `bash .harness/.meta/codex-progress-cleanup/measure/audit.sh 구조-01` 출력 `PASS 구조-01` (구현 커밋 뒤 잰다)
  - 음성 대조: `--base` 는 확장 파일 6 개가 남아 FAIL(실측)
- [ ] 구조-02: 레포 검사가 그대로 통과한다 — `python3 scripts/validate-plugin.py harness` 종료 코드 0, `python3 scripts/sync-docs.py --check-only | grep -c '모든 README가 동기화 상태입니다.'` 이 1 [exact]
  - 측정: 두 명령을 작업 폴더에서 돌린다 (봉인 전 18:25 실측 0 · 1)

## Anti-patterns

- [ ] 금지-03: bare code fence 금지 — `python3 scripts/validate-plugin.py harness --check=code-fence` 종료 코드 0
  - 측정: 그 명령의 종료 코드

## Reusability

- [ ] 재사용-01: 다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다 — 머리 줄 사용량도 기존 진행 줄 함수가 이번 차례 기록을 읽는 김에 함께 읽는다(새 함수 · 새 파일 없음)
  - 측정: `python3 .harness/.meta/codex-progress-cleanup/measure/research.py reuse` 종료 코드 0 (진행 줄 함수가 `rollout` 을 읽고, `find "$SESS_DIR"` 2 곳 · `progress_every=` 1 줄 그대로, 함수 수 = 정리 직전 판 − 2)
- [ ] 재사용-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다 — 감독 사용량 상한은 기존 사용 기록(`codex-audit-usage.jsonl`)만 쓴다. Given 사용 기록에 오늘 5시간 80 % 행이 있을 때 감독은 종료 코드 2 · 리포트 `갈래: 한도-사용량` 으로 막히고 Codex 를 부르지 않으며 상태 폴더 파일은 0 이다 [exact]
  - 측정: `bash .harness/.meta/codex-progress-cleanup/measure/audit.sh 감독-02` 출력 `PASS 감독-02`
  - 음성 대조: `record_usage` 가 사용 기록에 `limits` 를 안 쓰거나 상한 확인을 지우면 막히지 않아 FAIL 한다. `--base` 는 PASS(실측 — 지켜야 할 동작)

## Diagnostics

- [ ] 진단-01: N/A (commands.analyze 는 `bash -n scripts/release.sh` — 이번 변경 파일과 교집합 0 개. 측정: `git diff --name-only ae918dab feat/codex-research-activity | grep -c '^scripts/release.sh$'` 이 0)
- [ ] 진단-02: IDE diagnostics 워닝/인포 0개 (diagnostics.ide_exclude 는 `[]`) — `bash -n harness/scripts/codex-audit.sh` · `bash -n ~/.claude/bin/codex-research` 종료 코드 0, `shellcheck -S warning ~/.claude/bin/codex-research` 출력 0 줄, 측정 묶음 `research.py` · `audit.py` · `fake_audit.py` · `fake/codex` 는 `python3 -c 'import ast,sys; ast.parse(open(sys.argv[1]).read())'` 종료 코드 0
  - 양성 대조: `printf '#!/bin/bash\ncd foo\n' | shellcheck -S warning -` 이 1 줄 이상
- [ ] 진단-03: N/A (commands.test 는 `bash scripts/release.sh 2>&1 || true` — 이번 변경 파일과 교집합 0 개. 측정: 진단-01 과 같은 명령이 0)
- [ ] 진단-04: 실제 구동 시 에러 0개 — 부모 세션이 고친 래퍼로 진짜 Codex 리서치 1 회(프롬프트가 웹 검색을 요구한다)를 전역 규칙의 Monitor 명령 그대로 띄우고, Monitor 가 받은 줄을 `.harness/.meta/codex-progress-cleanup/evidence/real-run.txt` 에 남긴다(첫 줄 `# 명령: …`, 둘째 줄 `# 출력: …`, 셋째 줄 `# 세션기록: <그 차례 rollout 경로>`). 첫 줄이 문서 명령 꼴이고, 머리 줄 1 개 이상 · 활동 줄 1 개 이상 · `완료 (시도` 줄 정확히 1 개 · `Traceback` 0 · `남은 한도` 0, 출력 파일 첫 줄이 진행 줄에 0 번이며, 세션 기록 파일이 래퍼 수정 뒤에 쓰였고 증거의 검색 · 열람 줄이 그 기록에 모두 있다 [exact]
  - 측정: `python3 .harness/.meta/codex-progress-cleanup/measure/research.py evidence` 종료 코드 0 이고 출력에 `FAIL` 0 줄
