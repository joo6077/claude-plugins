---
feature: "Codex 진행 상황 — 리서치 작업 카드 줄 · 짧은 상태 표시줄 · 표시 결함 고치기"
slug: codex-status-card
created: "2026-10-09 12:21"
complexity: "중간"
conditions: 18
status: done
owner_session: 35b5945f-4957-4359-9b18-2d22b3bafeb0
conditions_digest: sha256:d1c630e9e40b2763
measurement_digest: sha256:ea8144966084fb1a
locked_at: "2026-10-09 12:47"
---

# Codex 진행 상황 — 리서치 작업 카드 줄 · 짧은 상태 표시줄 · 표시 결함 고치기

## 배경

- 앞 계약 `codex-status-bar`(APPROVE, PR #142 병합 `afbb36f2`) 로 VS Code 하단 상태 표시줄에 작업마다 항목을 띄웠다. 사용자 확인(2026-10-09): 「아래 뜬다」 · 「어떤 리서치인지 나와야 하는데」 · 「상태바에 하면 길어질거 같은데 … 세션별로 다르게 보여줘야지」. Claude Code 채팅 창 입력창 위에는 확장이 글을 넣을 수 없다. 사용자 결정: 「작업 카드 + 상태바 짧게 (추천)」 — 세션별 자세한 진행은 Claude 가 뒤에서 돌린 명령의 작업 카드(그 세션 채팅 창에만 뜬다)로, 상태 표시줄은 창마다 한 줄로 짧게.
- 만들 것: (1) 리서치 실행기(`~/.claude/bin/codex-research`)가 진행 줄 `리서치 · <주제> · 시도 n/N · <경과> · 5시간 n% · 주간 n%` 를 `CODEX_PROGRESS_SECONDS`(기본 30)와 반복 주기(3 초) 중 긴 쪽마다 stderr 에만 낸다(답이 나가는 stdout 에는 내지 않는다). 경과는 실행기 시작부터 센다. 주제는 프롬프트 파일에서 처음 나오는 `Goal:` 줄(어느 줄이든, 없으면 첫 비지 않은 줄)이고 40 글자를 넘으면 40 글자 + `…` 로 자른다 — 자르기는 python 으로 해 셸 로캘과 상관없게 한다. 상태 파일에도 `topic` 으로 남긴다. 사용량은 상태 폴더 `usage.json` 의 아직 안 풀린 창만. (2) 리서치 상태 파일의 `folder` 를 실제 경로(`pwd -P`)로 쓴다. (3) 상태 표시줄은 창마다 항목 하나 — `$(sync~spin) 감독 n · 리서치 n`(0 인 종류는 빼고, 감독 다음 리서치 순), 풀이에 작업별 줄 `<세션 앞 4글자> <종류> · <주제 있으면 주제 · ><단계> · <경과><사용량>`. 도는 작업이 없으면 띄우지 않는다. 작업별 줄 · 요약은 `status.js` 의 `jobsToItems` · `summarize` 가 만들고 `extension.js` 는 그리기만 한다. (4) 감독이 상태 폴더에 쓰는 세 자리(상태 파일 쓰기 · 지우기 · `usage.json`) 모두 실패해도(상태 폴더를 못 만듦 · 디스크) 감독은 그대로 끝까지 돌고, 감독 폴더 사용 기록(`codex-audit-usage.jsonl`)은 그대로 남긴다. 갱신 주기는 `CODEX_STATUS_BEAT`(기본 30초, 숫자가 아니면 기본, 60 초 상한)로 바꿀 수 있다. (5) 상태 표시줄 항목 ID 는 `joo6077.codex-status` 하나로 고정하고, 풀이는 일반 글자(작업마다 한 줄, `\n` 으로 나눔)다. (6) 문장 「래퍼는 Bash `run_in_background: true` 로 돌려 그 세션 채팅 창의 작업 카드로 진행을 보고, 끝 알림이 오면 출력 파일을 읽는다」 를 전역 규칙 `~/.claude/CLAUDE.md` 의 Codex 호출 방식 문단과 `~/.claude/codex-prompt-template.md` 의 리서치 호출 문단에 넣는다 — 직접 `codex exec` 를 부를 때 「앞에서 기다리며」 는 그대로 둔다. 메모 `feedback_codex_foreground_call_direct` 에도 래퍼는 예외라고 적는다. 리서치를 뒤에서 막는 훅(`enforce-foreground-research.sh`)은 Agent · Workflow 만 막고 Bash 는 막지 않아 고치지 않는다.
- 레포 밖 파일 셋을 고친다 — 백업: `~/.claude/bin/codex-research.bak-20261009b` · `~/.claude/CLAUDE.md.bak-20261009` · `~/.claude/codex-prompt-template.md.bak-20261009`(2026-10-09).
- 이 계약은 Claude 가 쓰고 Claude qa-evaluator 가 판정한다. 진짜 Codex 모델 호출은 0 번 — 감독은 가짜 codex, 리서치 실행기는 가짜 `codex` 를 `PATH` 앞에 두고, 확장은 가짜 `vscode` 모듈로 잰다.
- W = `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/codex-status-card`, 가지 `feat/codex-status-card`, BASE = `afbb36f2`. 측정 묶음 = `bash .harness/.meta/codex-status-card/measure/measure.sh <조건 번호>`(`--base` 면 BASE 의 `harness/` 와 리서치 실행기 백업본 `codex-research.bak-20261009b` 로 잰다).
- 봉인 전 교차 진단(2026-10-09) 반영: 실제 템플릿처럼 `Goal:` 이 셋째 줄인 프롬프트, 진행 줄 간격(1 초 · 20 초) · stderr 만, 풀린 창 빼기, `LC_ALL=C` 자르기, 상태 폴더 세 자리 실패 · 갱신 스레드 · 사용 기록 유지, 항목 ID 고정 · 일반 글자 풀이 · 감독 2, 규칙 문장 고정 · 「앞에서 기다리며」 범위, 끄기는 `deactivate` 만. 감시자 오류 처리는 측정할 수 없어 범위에서 뺐다.
- 봉인 전 실측(BASE 판, 2026-10-09 12:21 직전): 스크립트-01~05 · 07 · 스킬-01 · 구조-01 FAIL(05 (a) 는 상태 폴더를 못 쓰면 감독이 종료 1 — 결함 재현, 02 는 바로가기 경로를 그대로 적음 — 결함 재현), 스크립트-06 · 08 · 재사용-01 PASS(지켜야 할 동작). 남은 가짜 프로세스 0 개.

## Script

- [ ] 스크립트-01: Given 가짜 `codex` 를 `PATH` 앞에 둔 리서치 실행기와 `usage.json`(5시간 12 % 안 풀림 · 주간 3 % 이미 풀림), stdout · stderr 를 따로 받아 도는 중에 읽는 측정, When (a)(b1) 프롬프트가 `Role: 조사자. Read-only.` · 빈 줄 · `Goal: VS Code 상태 표시줄 API 조사` 이고 `CODEX_PROGRESS_SECONDS=1` 로 7 초 붙잡으면 (b2) 같은 프롬프트에 `CODEX_PROGRESS_SECONDS=20` 으로 5 초 붙잡으면 (c) `Goal:` 뒤가 60 글자면(보통 로캘 · `LC_ALL=C` 두 번) (d) `Goal:` 줄 없이 빈 줄 뒤 앞에 빈칸 둘을 둔 `첫 줄 주제` 면, Then (a) 상태 파일이 1 개이고 `topic` 이 `VS Code 상태 표시줄 API 조사` (b1) 놓아주기 전 stderr 에 정규식 `^리서치 · VS Code 상태 표시줄 API 조사 · 시도 1/1 · \d+(초|분) · 5시간 12%$` 에 맞는 줄이 2 개 이상 · 실행기 종료 0 · stdout 에는 그런 줄 0 개 (b2) 5 초 안에 그런 줄 1 개 이하 (c) 두 번 다 `topic` 이 앞 40 글자 + `…` (d) `topic` 이 `첫 줄 주제` [exact, enumerated]
  측정: bash .harness/.meta/codex-status-card/measure/measure.sh 스크립트-01
  음성 대조: 백업본은 `topic` 을 쓰지 않아 FAIL 한다 (`measure.sh 스크립트-01 --base` 종료 1)
- [ ] 스크립트-02: Given 실제 폴더를 가리키는 바로가기(심볼릭 링크) 폴더, When 그 바로가기 경로로 들어가 리서치 실행기를 돌리면, Then 상태 파일 `folder` 가 실제 경로(`os.path.realpath`)와 같다 [exact]
  측정: bash .harness/.meta/codex-status-card/measure/measure.sh 스크립트-02
  음성 대조: 백업본은 바로가기 경로를 그대로 적어 FAIL 한다 (`measure.sh 스크립트-02 --base` 종료 1)
- [ ] 스크립트-03: Given 고정 입력(지금 시각 고정 · 작업 폴더 `/w/repo` · 사용량 5시간 12 % · 주간 3 %), When `status.js` 의 `jobsToItems` 와 `summarize` 를 부르면, Then (a) 주제 있는 리서치 작업의 줄이 정확히 `e5f6 리서치 · VS Code 상태 표시줄 API 조사 · 시도 1/3 · 30초 · 5시간 12% · 주간 3%` (b) 주제 없는 감독 작업의 줄이 정확히 `a1b2 감독 · judge-1 · 4분 · 5시간 12% · 주간 3%` (c) 감독 · 리서치 하나씩의 요약 글자가 정확히 `$(sync~spin) 감독 1 · 리서치 1` 이고 풀이에 두 작업별 줄이 다 있다 (d) 리서치만 하나 → 요약 `$(sync~spin) 리서치 1` (e) 작업 없음 → 요약 `null` (f) 감독 둘 · 리서치 하나 → 요약 `$(sync~spin) 감독 2 · 리서치 1` (g) (c) 의 풀이가 문자열이고 줄바꿈이 정확히 1 개(작업마다 한 줄) [exact, enumerated]
  측정: bash .harness/.meta/codex-status-card/measure/measure.sh 스크립트-03
- [ ] 스크립트-04: Given 가짜 `vscode` 모듈, When `extension.js` 를 띄운 뒤 그 창 작업 폴더 안의 감독 · 리서치 작업 파일을 만들고, 리서치를 지우고, 감독이 살아 있는 채로 구독 목록은 하나도 부르지 않고 `deactivate` 만 부르면, Then (a) 보이는 항목이 정확히 1 개이고 글자가 `$(sync~spin) 감독 1 · 리서치 1` · 풀이에 `a1b2 감독` 과 `e5f6 리서치 · 상태 표시줄 조사` (b) 리서치를 지우면 보이는 항목 글자가 `$(sync~spin) 감독 1` 하나 (c) 끈 뒤 만든 항목이 모두 정리(dispose)됐고, 끈 뒤 작업 파일을 만들어도 항목이 새로 생기지 않으며 프로세스가 25 초 안에 스스로 끝난다 (d) 만든 항목의 ID 가 모두 `joo6077.codex-status` 하나 [exact, enumerated]
  측정: bash .harness/.meta/codex-status-card/measure/measure.sh 스크립트-04
- [ ] 스크립트-05: Given 구독 모양 감독 폴더, When (a) `CODEX_STATUS_DIR` 가 파일 아래 경로(폴더를 만들 수 없음)이고 `CODEX_STATUS_BEAT=1` 인 채 판정 차례를 3 초 붙잡았다가 놓으면 (b) 보통 상태 폴더에 `CODEX_STATUS_BEAT=1` 로 판정 차례를 멈춰 두면, Then (a) 종료 0 · `report.md` 끝 줄 `감독 판정: APPROVE` · 출력에 `Traceback` · `Exception in thread` 0 개 · 감독 폴더 `codex-audit-usage.jsonl` 줄 1 개 (b) 상태 파일 `updated` 가 3 초 뒤 더 크다 [exact, enumerated]
  측정: bash .harness/.meta/codex-status-card/measure/measure.sh 스크립트-05
  음성 대조: BASE 판은 상태 폴더를 못 쓰면 감독이 Codex 를 부르기 전에 멈춰 FAIL 한다 (`measure.sh 스크립트-05 --base` 종료 1)
- [ ] 스크립트-06: Given 리서치 실행기의 차례가 멈춘 동안, When 상태 파일 `updated` 를 5 초 간격으로 두 번 읽으면, Then 두 번째가 더 크다(반복 주기마다 갱신) [exact]
  측정: bash .harness/.meta/codex-status-card/measure/measure.sh 스크립트-06
- [ ] 스크립트-07: Then `~/.claude/CLAUDE.md` 의 `**호출 방식:**` 으로 시작하는 문단과 `~/.claude/codex-prompt-template.md` 의 `리서치는 래퍼를 쓴다` 로 시작하는 문단(다음 빈 줄까지)에 문장 「래퍼는 Bash `run_in_background: true` 로 돌려 그 세션 채팅 창의 작업 카드로 진행을 보고, 끝 알림이 오면 출력 파일을 읽는다」 가 그대로 있고, CLAUDE.md 그 문단의 「앞에서 기다리며」 는 「직접 부를 때는」 뒤에만 있다 [exact, enumerated]
  측정: bash .harness/.meta/codex-status-card/measure/measure.sh 스크립트-07
- [ ] 스크립트-08: Then 앞 측정 묶음 — `codex-audit-usage-cap` 의 스크립트-01 · 02 · 03 · 04, `codex-status-bar` 의 스크립트-01 · 02 · 05 — 을 재는 가지만 이번 가지로 바꾼 사본으로 돌려 모두 종료 0 이고 `Traceback` 이 없다 [exact, enumerated]
  측정: bash .harness/.meta/codex-status-card/measure/measure.sh 스크립트-08

## Skill

- [ ] 스킬-01: `harness/README.md` 의 `**Codex 진행 상황 표시줄**` 문단에 `작업 카드` · `감독 1 · 리서치 1` · `Goal:` 이 있다 [exact, enumerated]
  측정: bash .harness/.meta/codex-status-card/measure/measure.sh 스킬-01

## Architecture

- [ ] 구조-01: Given 구현이 커밋된 뒤, When `git diff --name-only afbb36f2..$(git rev-parse --verify -q feat/codex-status-card) -- . ':(exclude).harness'` 를 보면, Then 바뀐 경로가 `## 범위 경계` sprint-scope 목록 중 `.harness/` 밖 6 개의 부분집합이고 `harness/scripts/codex-audit.sh` 를 포함한다. 상한 ref 해석 실패면 FAIL [exact, enumerated]
  측정: bash .harness/.meta/codex-status-card/measure/measure.sh 구조-01

## Anti-patterns

- [ ] 금지-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수
  측정: python3 scripts/validate-plugin.py harness --check=code-fence
- [ ] 금지-04: SKILL.md / agents/*.md frontmatter 에서 name 필드 누락 금지
  측정: python3 scripts/validate-plugin.py harness --check=frontmatter

## Reusability

- [ ] 재사용-01: 가지 끝 `harness/vscode-status/extension.js` 가 `require('./status')` 를 정확히 1 번 쓰고 `process.kill` · `relative(` · `resets_at` · `'감독'` · `'리서치'` 가 없다(판단 · 종류별 셈은 `status.js` 에만)
  측정: bash .harness/.meta/codex-status-card/measure/measure.sh 재사용-01
- [ ] 재사용-02: N/A (새 공용 모듈을 만들지 않는다 — `status.js` 에 `summarize` 를 더하고 기존 함수를 고쳐 쓴다)

## Diagnostics

- [ ] 진단-01: N/A (commands.analyze `bash -n scripts/release.sh` 는 이번 변경 파일을 재지 않는다 — 진단-04 가 `bash -n` · `node --check` 로 잰다)
- [ ] 진단-02: 변경한 마크다운 파일(`harness/README.md` · `harness/vscode-status/README.md` · 이 계약) 세 개를 모두 가지 끝에서 읽었고(못 읽은 파일이 있으면 FAIL), BASE 대비 더한 줄에 걸린 markdownlint-cli2 0.23.2 경고(MD013 끔)가 0 개다
  측정: bash .harness/.meta/codex-status-card/measure/measure.sh 진단-02
  양성 대조: MD013 을 켜고 파일 전체 줄을 세면 1 이상이 나온다 (`measure.sh 진단-02 --positive`)
- [ ] 진단-03: N/A (commands.test `bash scripts/release.sh` 는 이번 변경과 무관 — 진단-04 가 측정 묶음 전체를 잰다)
- [ ] 진단-04: `bash -n harness/scripts/codex-audit.sh` · `bash -n ~/.claude/bin/codex-research` · `node --check` 로 `extension.js` · `status.js` 가 종료 0, `python3 scripts/validate-plugin.py harness` 종료 0, 측정 묶음 전체(`measure.sh all --skip 진단-04`) 종료 0 · `Traceback` 0 개, `.github/workflows/ci.yml` 의 한 줄 `run:` 명령 중 `python3 scripts/` · `bash harness/` · `bash flutter-toolkit/` 로 시작하는 것 전부(0 개면 FAIL)를 W 에서 돌려 실패 0
  측정: bash .harness/.meta/codex-status-card/measure/measure.sh 진단-04

## 범위 경계

- 하지 않는 것: 채팅 창 입력창 위에 넣기(수단 없음), 감독 진행 줄 바꾸기(`follow` 가 이미 작업 카드로 보인다), 훅 고치기, 감독 다시 켜기, harness 버전 올리기(이 스프린트 뒤 따로).
- 레포 밖 파일: `~/.claude/bin/codex-research` · `~/.claude/CLAUDE.md` · `~/.claude/codex-prompt-template.md` 를 고친다(스크립트-01 · 02 · 06 · 07 · 진단-04 가 잰다). 구조-01 은 레포 안 경로만 잰다.
- 앞 측정 묶음 `codex-status-bar` 의 스크립트-03 · 04 는 작업마다 항목 · 옛 글자 모양을 재므로, 이 계약이 그 동작을 바꿔 이제 FAIL 하는 것이 맞다 — 스크립트-08 은 바뀌지 않는 01 · 02 · 05 만 돌린다.
- `usage.json` 은 계정 하나로 본다 — 리서치(`~/.codex`)와 감독(`~/.codex-qa`)이 같은 계정임을 2026-10-09 지문으로 확인했다.
- 커버리지 해소: 스크립트-01~08 · 스킬-01 · 구조-01 — 측정 줄은 `measure.sh <번호>` 한 명령이고 열거 대상은 `measure.py` · `check_summary.js` · `check_extension.js` 의 같은 이름 함수(`SCOPE` · `PREVIOUS` · `RULES` 상수 · 낱말 목록)가 같은 표기로 잰다.

```text
# sprint-scope
harness/scripts/codex-audit.sh
harness/README.md
harness/vscode-status/extension.js
harness/vscode-status/status.js
harness/vscode-status/README.md
harness/vscode-status/package.json
.harness/
```
