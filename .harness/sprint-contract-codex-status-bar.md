---
feature: "Codex 진행 상황 VS Code 상태 표시줄 (세션마다 · 도는 동안만)"
slug: codex-status-bar
created: "2026-10-09 02:23"
complexity: "중간"
conditions: 16
status: done
owner_session: 35b5945f-4957-4359-9b18-2d22b3bafeb0
conditions_digest: sha256:e170158226a1abbc
measurement_digest: sha256:1456137da08cb5a7
locked_at: "2026-10-09 11:04"
---

# Codex 진행 상황 VS Code 상태 표시줄 (세션마다 · 도는 동안만)

## 배경

- 사용자 요구(2026-10-08~09): 감독 · 리서치 진행 상황과 Codex 사용량을 보이게 한다 — 「세션마다」, 「하는 거에 있어서만 보여주기, 그 세션 그 당시에」. 자리는 「VS Code 하단 상태 표시줄 (추천)」. Claude Code 채팅 창(네이티브)은 상태 줄(statusLine)을 그리지 않고 입력창 위에 글을 띄울 수단도 없다(사용자 확인: 「터미널에서는 보인다」).
- 설계: (1) 감독(`harness/scripts/codex-audit.sh`)과 리서치 실행기(`~/.claude/bin/codex-research`, 레포 밖 사용자 파일 — 2026-10-09 `codex-research.bak-20261009` 로 백업)가 시작할 때 상태 폴더(`$CODEX_STATUS_DIR`, 없으면 `$HOME/.codex-status`)에 `<종류>-<pid>.json` 을 쓰고 끝나면(성공 · 실패 · 신호 · 막힘) 지운다. 감독은 실제로 도는 프로세스(`--detach` 면 뒤에서 도는 자식)가 쓴다. 쓰기는 같은 폴더 임시 파일에 쓴 뒤 이름 바꾸기로 한다. 도는 동안 `updated` 를 30 초마다(리서치는 반복 주기마다) 갱신한다. 내용: `kind`(`감독` | `리서치`) · `session`(`CLAUDE_CODE_SESSION_ID`) · `folder`(감독은 저장소 루트, 리서치는 부른 폴더) · `step`(감독은 차례 이름, 리서치는 `시도 n/N`) · `started` · `updated`(유닉스 초) · `pid`(감독 프로세스, 리서치는 실행기 자신). 사용량을 알게 되면(감독 차례 끝 · 리서치 시도 끝 — 리서치는 그 차례 번호의 세션 기록에서만 읽는다) 같은 폴더 `usage.json` 에 `limits`(`5시간` · `주간` 의 `used` · `resets_at`)를 쓴다. (2) VS Code 확장 `harness/vscode-status/`(의존성 없는 순수 JS) 가 상태 폴더를 읽어, 이 창의 작업 폴더 안에서 살아 있는 작업만 작업마다 상태 표시줄 항목 하나로 띄운다 — `$(sync~spin) <세션 앞 4글자> <종류> <단계> · <경과> · 5시간 n% · 주간 n%`. 도는 작업이 없으면 아무것도 띄우지 않는다. `updated` 가 2 분 넘게 멈춘 작업(강제 종료 · pid 재사용)과 이미 풀린 사용량 창은 보이지 않는다. 상태 폴더가 없거나 반쯤 쓴 파일이 있어도 확장은 죽지 않는다(1 초 주기 읽기가 기준, 폴더 감시는 거들기만). 판단(폴더 · 살아 있음 · 글자)은 `status.js` 의 순수 함수에만 둔다.
- API 근거(Codex 리서치 2026-10-09, `gpt-5.6-sol`): `window.createStatusBarItem(id, alignment, priority)` · `text` 의 `$(name~spin)` · `tooltip` · `show/hide/dispose`, `workspace.workspaceFolders[].uri.fsPath`, `activationEvents: ["onStartupFinished"]`, 순수 JS `main` 허용. 폴더 복사 설치는 공식 근거가 없어 VSIX(`@vscode/vsce` 4.0.0, 2026-10-03) 로 묶어 VS Code CLI 로 설치한다(`install.sh`).
- 감독은 지금 15 곳 모두 `mode: off`(감독 계정이 Plus 라 Claude 가 맡는다, 2026-10-08) — 상태 표시줄은 리서치와, 나중에 감독을 켰을 때 함께 쓴다.
- 이 계약은 Claude 가 쓰고 Claude qa-evaluator 가 판정한다. 진짜 Codex 모델 호출은 0 번 — 감독은 가짜 codex, 리서치 실행기는 가짜 `codex`(측정 묶음 `fake_research.py`)를 `PATH` 앞에 두고 잰다. 확장은 가짜 `vscode` 모듈로 띄워 잰다(`check_extension.js`).
- W = `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/codex-status-bar`, 가지 `feat/codex-status-bar`, BASE = `d72bd22c`(harness 0.22.0). 측정 묶음 = `bash .harness/.meta/codex-status-bar/measure/measure.sh <조건 번호>`(`--base` 면 BASE 의 `harness/` 와 리서치 실행기 백업본으로 잰다).
- 봉인 전 교차 진단(2026-10-09) 반영: 가짜 리서치 codex 를 빈칸 없는 JSON(실제 모양)으로 · 미끼 세션 기록 · SIGTERM, 감독 `--detach`, 확장의 작업마다 항목 · 정리 · 상태 폴더 없음 · 반쯤 쓴 파일 · 죽은 pid · 폴더 밖, 화면 판단의 오래 멈춘 작업 · 풀린 창 · 기본 살아 있음 판단을 더했다.
- 봉인 전 실측(BASE 판, 2026-10-09 02:15 · 반영 뒤 02:45 다시): 스크립트-01~05 · 스킬-01 · 구조-01 · 재사용-01 FAIL, 스크립트-06 PASS(지켜야 할 앞 동작). 남은 가짜 프로세스 0 개.

## Script

- [ ] 스크립트-01: Given 구독 모양 감독 폴더와 `CLAUDE_CODE_SESSION_ID`, When impl 의 판정 차례가 멈춘 동안 · 끝난 뒤 · SIGTERM 뒤 · 구독이 아니라 막힌 뒤 · `--detach` 로 띄웠을 때 상태 폴더를 보면, Then (a) 도는 동안 상태 파일이 정확히 1 개이고 `kind` 감독 · `session` 이 그 값 · `folder` 가 저장소 루트(실제 경로) · `step` 에 `judge-1` · `started` · `updated` · `pid` 가 정수이며 그 pid 가 살아 있다 (b) 끝난 뒤 종료 0 · 상태 파일 0 개 · `usage.json` 의 `limits` 가 `5시간` 12 · `주간` 3 (c) SIGTERM 뒤 상태 파일 0 개 (d) 막힌 감독(종료 2) 뒤 상태 파일이 남지 않는다 (e) `--detach` 로 띄우면 판정 차례 중 상태 파일이 정확히 1 개(a 와 같은 칸)이고 그 `pid` 가 감독 폴더 `pid` 파일 값과 같으며, 끝난 뒤 0 개 [exact, enumerated]
  측정: bash .harness/.meta/codex-status-bar/measure/measure.sh 스크립트-01
  음성 대조: BASE 판은 상태 파일을 쓰지 않아 FAIL 한다 (`measure.sh 스크립트-01 --base` 종료 1)
- [ ] 스크립트-02: Given 실제 codex 처럼 빈칸 없는 JSON 을 내는 가짜 `codex` 를 `PATH` 앞에 둔 리서치 실행기(`~/.claude/bin/codex-research`, `CODEX_TRIES=1`)와, 세션 기록 폴더의 더 새 미끼 기록(다른 차례, 사용량 50 % · 40 %), When 차례가 열려 멈춘 동안(실행기 반복 주기 3 초보다 긴 4 초 뒤) · 끝난 뒤 · 끝내라는 신호(SIGTERM) 뒤 상태 폴더를 보면, Then (a) 도는 동안 상태 파일이 정확히 1 개이고 `kind` 리서치 · `session` 이 그 값 · `folder` 가 부른 폴더 · `step` 에 `시도 1/1` · 시각과 pid 가 정수이며 pid 가 살아 있다 (b) 끝난 뒤 실행기 종료 0 · 상태 파일 0 개 · `usage.json` 의 `limits` 가 `5시간` 12 · `주간` 3(미끼 50 / 40 이 아니다) (c) 실행기에 SIGTERM 을 보내면 상태 파일 0 개 · 가짜 codex 프로세스가 살아 있지 않다 [exact, enumerated]
  측정: bash .harness/.meta/codex-status-bar/measure/measure.sh 스크립트-02
  음성 대조: 백업본(`codex-research.bak-20261009`)은 상태 파일을 쓰지 않아 FAIL 한다 (`measure.sh 스크립트-02 --base` 종료 1)
- [ ] 스크립트-03: Given 고정 입력(지금 시각 고정 · 작업 폴더 `/w/repo` · 사용량 5시간 12 % · 주간 3 %), When `status.js` 의 `jobsToItems(jobs, usage, folders, now, alive)`(돌려받는 값은 `{key, text, tooltip}` 목록, `alive` 를 빼면 기본 판단)를 부르면, Then (a) 폴더 안 · 살아 있는 감독 작업 하나 → 항목 1 개, 글자가 정확히 `$(sync~spin) a1b2 감독 judge-1 · 4분 · 5시간 12% · 주간 3%` 이고 풀이에 세션 전체와 폴더가 있다 (b) 다른 폴더 (c) 죽은 pid (d) 작업 없음 (g) 이름만 비슷한 옆 폴더(`/w/repo-other`) (i) `updated` 가 10 분 전 → 다섯 다 항목 0 개 (e) 두 세션(감독 · 리서치) → 항목 2 개 · 열쇠가 서로 다르고 리서치 글자가 `$(sync~spin) e5f6 리서치 시도 1/3 · 30초 · 5시간 12% · 주간 3%` (f) 사용량 없음 → 항목 1 개 · 글자에 `%` 없음 (h) 세션 없음 → 글자가 `$(sync~spin) ---- 감독` 으로 시작 (j) 5시간 창이 이미 풀림 → 글자에 `5시간` 없고 `주간 3%` 있음 (k) `alive` 를 빼고 살아 있는 pid → 항목 1 개 [exact, enumerated]
  측정: bash .harness/.meta/codex-status-bar/measure/measure.sh 스크립트-03
- [ ] 스크립트-04: Given 가짜 `vscode` 모듈과 아직 없는 상태 폴더, When `extension.js` 를 띄운 뒤 상태 폴더 · 반쯤 쓴 파일 · 작업 파일들을 만들고 지우고 끄면, Then (a) 오류 없이 시작하고 보이는 항목 0 개 (b) 반쯤 쓴 파일이 섞여도 작업 하나 → 4 초 안에 보이는 항목 1 개 · 글자에 `감독 judge-1` · `5시간 12%` (c) 다른 세션 작업을 더하면 4 초 안에 2 개 · id 가 서로 다름 (d) 죽은 pid 작업 · 작업 폴더 밖 작업을 더해도 2 개 그대로 (e) 하나 지우면 4 초 안에 1 개 (f) 다 지우면 4 초 안에 0 개 (g) 만든 항목이 4 개 이하(쌓이지 않음) (h) 끄면(구독 해제 · `deactivate`) 만든 항목이 모두 정리(dispose)되고, 끈 뒤 작업 파일을 만들어도 항목이 새로 생기지 않으며 프로세스가 35 초 안에 스스로 끝난다 [exact, enumerated]
  측정: bash .harness/.meta/codex-status-bar/measure/measure.sh 스크립트-04
- [ ] 스크립트-05: Then `harness/vscode-status/package.json` 의 `main` 이 `./extension.js` · `activationEvents` 가 `["onStartupFinished"]` · `name` · `publisher` · `version` · `engines.vscode` 가 있고 `dependencies` 가 없으며, `npx --yes @vscode/vsce@4.0.0 package --no-dependencies --allow-missing-repository --skip-license` 가 종료 0 으로 VSIX 를 만들고 그 안에 `extension/package.json` · `extension/extension.js` · `extension/status.js` 가 있고 `extension/install*` 는 없다 [exact, enumerated]
  측정: bash .harness/.meta/codex-status-bar/measure/measure.sh 스크립트-05
- [ ] 스크립트-06: Then 앞 측정 묶음 `codex-audit-usage-cap` 의 스크립트-01 · 02 · 03 · 04 를 재는 가지만 이번 가지로 바꾼 사본으로 돌려 모두 종료 0 이고 `Traceback` 이 없다 [exact, enumerated]
  측정: bash .harness/.meta/codex-status-bar/measure/measure.sh 스크립트-06

## Skill

- [ ] 스킬-01: `harness/README.md` 에 `vscode-status` 가 든 문단이 있고 그 문단에 `~/.codex-status` · `CLAUDE_CODE_SESSION_ID` · `install.sh` · `감독` · `리서치` 가 있다 [exact, enumerated]
  측정: bash .harness/.meta/codex-status-bar/measure/measure.sh 스킬-01

## Architecture

- [ ] 구조-01: Given 구현이 커밋된 뒤, When `git diff --name-only d72bd22c..$(git rev-parse --verify -q feat/codex-status-bar) -- . ':(exclude).harness'` 를 보면, Then 바뀐 경로가 `## 범위 경계` sprint-scope 목록 중 `.harness/` 밖 8 개의 부분집합이고 `harness/scripts/codex-audit.sh` 를 포함한다. 상한 ref 해석 실패면 FAIL [exact, enumerated]
  측정: bash .harness/.meta/codex-status-bar/measure/measure.sh 구조-01

## Anti-patterns

- [ ] 금지-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수
  측정: python3 scripts/validate-plugin.py harness --check=code-fence
- [ ] 금지-04: SKILL.md / agents/*.md frontmatter 에서 name 필드 누락 금지
  측정: python3 scripts/validate-plugin.py harness --check=frontmatter

## Reusability

- [ ] 재사용-01: 가지 끝 `harness/vscode-status/extension.js` 가 `require('./status')` 를 정확히 1 번 쓰고 `process.kill` · `relative(` · `resets_at` 이 없다(폴더 · 살아 있음 · 사용량 판단은 `status.js` 에만)
  측정: bash .harness/.meta/codex-status-bar/measure/measure.sh 재사용-01
- [ ] 재사용-02: N/A (새 공용 모듈을 만들지 않는다 — 감독은 기존 `Audit` · `record_usage` 자리에 상태 쓰기를 붙이고, 리서치 실행기는 기존 시도 반복에 붙인다)

## Diagnostics

- [ ] 진단-01: N/A (commands.analyze `bash -n scripts/release.sh` 는 이번 변경 파일을 재지 않는다 — 진단-04 가 `bash -n` · `node --check` 로 잰다)
- [ ] 진단-02: 변경한 마크다운 파일(`harness/README.md` · 이 계약) 두 개를 모두 가지 끝에서 읽었고(못 읽은 파일이 있으면 FAIL), BASE 대비 더한 줄에 걸린 markdownlint-cli2 0.23.2 경고(MD013 끔)가 0 개다
  측정: bash .harness/.meta/codex-status-bar/measure/measure.sh 진단-02
  양성 대조: MD013 을 켜고 파일 전체 줄을 세면 1 이상이 나온다 (`measure.sh 진단-02 --positive`)
- [ ] 진단-03: N/A (commands.test `bash scripts/release.sh` 는 이번 변경과 무관 — 진단-04 가 측정 묶음 전체를 잰다)
- [ ] 진단-04: `bash -n harness/scripts/codex-audit.sh` · `bash -n ~/.claude/bin/codex-research` · `node --check` 로 `extension.js` · `status.js` 가 종료 0, `python3 scripts/validate-plugin.py harness` 종료 0, 측정 묶음 전체(`measure.sh all --skip 진단-04`) 종료 0 · `Traceback` 0 개, `.github/workflows/ci.yml` 의 한 줄 `run:` 명령 중 `python3 scripts/` · `bash harness/` · `bash flutter-toolkit/` 로 시작하는 것 전부(0 개면 FAIL)를 W 에서 돌려 실패 0
  측정: bash .harness/.meta/codex-status-bar/measure/measure.sh 진단-04

## 범위 경계

- 하지 않는 것: Claude Code 채팅 창 안에 띄우기(수단 없음), 터미널 상태 줄(`~/.claude/statusline-command.sh`) 고치기, 감독 다시 켜기, harness 버전 올리기(이 스프린트 뒤 따로), 마켓플레이스 등록.
- 레포 밖 파일: `~/.claude/bin/codex-research` 를 고친다(스크립트-02 · 진단-04 가 잰다). 구조-01 은 레포 안 경로만 잰다.
- 「세션마다」 는 작업마다 항목을 따로 띄우고 세션 앞 4 글자로 가르는 것으로 한다 — 상태 표시줄은 VS Code 창 하나에 하나라, 지금 보고 있는 채팅 탭만 골라 보일 수단은 없다.
- 측정은 맥 기준이고 `npx` 가 `@vscode/vsce@4.0.0` 을 받을 인터넷이 필요하다(스크립트-05). 반쯤 쓴 파일 대신 임시 파일 · 이름 바꾸기로 쓰는지와 30 초 갱신 주기는 코드 검토로 본다 — 측정은 확장이 반쯤 쓴 파일을 견디는지(스크립트-04 (b))와 오래 멈춘 작업을 숨기는지(스크립트-03 (i))를 잰다.
- 실제 VS Code 화면 확인은 설치 뒤 사용자가 창을 다시 불러와 본다 — 측정은 가짜 `vscode` 모듈로 한다.
- 커버리지 해소: 스크립트-01~06 · 스킬-01 · 구조-01 — 측정 줄은 `measure.sh <번호>` 한 명령이고 열거 대상은 `measure.py` · `check_status.js` · `check_extension.js` 의 같은 이름 함수(`SCOPE` · `PREVIOUS` 상수 · 낱말 목록)가 같은 표기로 잰다.

```text
# sprint-scope
harness/scripts/codex-audit.sh
harness/README.md
harness/vscode-status/package.json
harness/vscode-status/extension.js
harness/vscode-status/status.js
harness/vscode-status/install.sh
harness/vscode-status/.vscodeignore
harness/vscode-status/README.md
.harness/
```
