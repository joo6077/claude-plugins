# 요구사항 — Codex 판정 격리 강화 (slug: codex-judge-isolation)

작성: Claude (2026-10-07). 사용자와 합의한 내용을 옮긴 것이다. 계약서는 이 문서를 받은 Codex 가 쓴다.

## 1. 배경

harness 0.20.0 의 `harness/scripts/codex-audit.sh impl` 은 판정 Codex 를 `codex exec -s workspace-write` 로 부른다. 2026-10-07 에 세 가지 문제가 실측으로 드러났다.

1. **판정끼리 서로 오염된다.** `workspace-write` 는 쓰기만 작업 폴더 · `/tmp` · `TMPDIR` 로 좁히고 **읽기는 디스크 전체**다. 앞선 판정이 `/tmp` · `TMPDIR` 에 남긴 재현 파일을 다음 판정이 읽어 결과가 오염됐다. 판정은 홈 폴더(`~/.ssh` 등)도 읽을 수 있다.
2. **임시 폴더가 지워지지 않는다.** 판정 사본은 `call(..., keep=True)` 로 일부러 남기고(「운영체제가 치운다」 주석), 사전 측정 명령과 판정 안 명령이 만든 임시 파일도 시스템 `TMPDIR` 에 그대로 남는다. 하루 72GB(741회 × 80~157MB)가 쌓여 손으로 지웠다. 이 문서를 쓰는 지금도 `$TMPDIR` 에 `codex-audit` 이름 폴더가 6개 남아 있다.
3. **판정이 사전 측정을 다시 돌린다.** `harness/templates/codex-audit/premeasure.md` 가 「격리 안에서 돌릴 수 있는 측정은 직접 돌린다」 고 시켜, 판정이 같은 측정을 20회 넘게 다시 돌렸다. 판정 한 번이 150만 토큰을 쓴 주원인이다.

## 2. 사용자 결정 (2026-10-07 대화)

1. 판정은 `-s workspace-write` 대신 **권한 프로필**로 돌린다. 허용하는 것은 셋뿐이다 — 판정 사본 쓰기, 얼린 입력(`<감독 폴더>/input`) 읽기, 판정이 쓰는 도구 경로(`~/.pyenv` · fnm 의 node, 그리고 그 밖에 측정에 꼭 필요한 시스템 경로) 읽기. 그 밖의 홈 폴더 · 다른 판정의 임시 폴더 · `/tmp` 는 읽지 못한다.
2. 사전 측정 한 번, 판정 한 차례마다 **전용 TMPDIR** 를 주고, 끝나면(성공 · 실패 · 시간 초과 · 중단 신호 모두) 지운다.
3. 판정 사본은 판정 뒤 지운다(지금은 남긴다).
4. 판정은 사전 측정 결과를 증거로 쓰고 **같은 측정을 다시 돌리지 않는다.** 사전 측정이 없는 조건만 직접 잰다.
5. 증명 두 가지:
   - `codex sandbox -P <프로필> --log-denials` 로 판정과 같은 프로필을 걸었을 때 판정 사본 쓰기 · 얼린 입력 읽기 · 도구 실행(python · node)은 되고 `~/.ssh` 읽기는 막힘을 보인다.
   - 판정(impl) 한 번이 끝난 뒤 이 감독이 만든 임시 폴더가 0개임을 보인다(실행 전후 개수 비교, 같은 시각 다른 감독이 만든 것과 구분).

## 3. 확인된 사실

- Codex 0.160.1 (최신과 같음, 2026-10-07 `npm view @openai/codex version`). `codex sandbox` 에 `-P, --permission-profile <NAME>` 과 `--log-denials` 가 있다. `codex exec` 에는 `--permission-profile` 옵션이 없다.
- 공식 문서(learn.chatgpt.com/docs/permissions · config-reference)와 0.160.1 소스 리서치 결과(2026-10-07):
  - 읽기를 좁히는 방법은 권한 프로필이다. 예: `default_permissions = "judge"`, `[permissions.judge] extends = ":workspace"`, `[permissions.judge.filesystem]` 에 `":root" = "deny"` · `":minimal" = "read"` · `"/절대경로" = "read"` · `":tmpdir"` · `":slash_tmp"` 제어, `[permissions.judge.network] enabled = …`. `codex exec` 에서는 `-c 'default_permissions="judge"'` 로 고른다.
  - **`-s/--sandbox` · `sandbox_mode` · `[sandbox_workspace_write]` 가 명령줄이나 설정 어디든 있으면 옛 방식이 이긴다** — 판정 호출에서 이것들을 모두 빼야 한다. 지금 `run_codex` 는 `-s workspace-write` 와 `-c sandbox_workspace_write.network_access=true` 를 넣는다.
  - 입력 폴더를 `workspace_roots` 에 넣으면 쓰기가 상속되니 절대 경로 `read` 규칙으로만 연다. 비대화식이라 `approval_policy = "never"` 가 필요할 수 있다.
  - 권한 프로필은 베타 기능이다(0.138+). 실제 이름 · 문법은 설치된 0.160.1 로 확인하고 계약에 적는다.
- 이 맥에서 python 은 `~/.pyenv`, node 는 `~/.local/share/fnm` 아래다. `:root = deny` 면 막힌다.
- 판정 호출은 `CODEX_HOME` 을 감독용 폴더(`~/.codex-qa`)의 임시 사본(`private_home`)으로 준다. 그 사본의 `config.toml` 은 원본을 그대로 복사한 것이라, 프로필 설정을 실행마다 그 사본에만 덧붙이면 원본 설정 파일은 바뀌지 않는다.
- 감독용 `~/.codex-qa/config.toml` 은 지금 `model = "gpt-6.1-sol"` · `cli_auth_credentials_store = "file"` · 프로젝트 신뢰 설정뿐이다. 사용자 설정 파일을 고치지 않는다.
- 지금 판정 차례(judge · review · research)는 인터넷을 켠다(`network=True`). 조사 차례(research)는 인터넷이 필요하다. 판정 · 재심 차례에 인터넷이 필요한지는 계약이 정한다(필요 없으면 끈다).
- 사전 측정은 `premeasure()` 가 `bash -c` 로 판정 사본에서 조건마다 돌린다. 지금 환경 변수를 그대로 물려받아 측정이 만든 임시 파일은 시스템 `TMPDIR` 에 남는다.
- 판정 격리 안에서는 `ps` · 겹친 격리(`codex sandbox` 안의 `codex sandbox`) · 키체인 · `rm -rf` 가 막힌다(메모 `reference_codex_sandbox_limits`). 증명 측정 중 격리 안에서 못 도는 것(`codex sandbox -P` 증명 자체)은 사전 측정으로 돌린다.

## 4. 제안 설계 (바꿔도 되지만 바꾸면 계약 `## 배경` 에 이유를 적는다)

- `run_codex` 에 격리 방식을 넘긴다. 판정 · 재심 차례는 권한 프로필(예: 이름 `codex-audit-judge`)로, 계약 작성(draft · revise) · 조사 차례는 지금 방식 그대로 둔다(이번 범위 밖).
  - 프로필은 실행마다 `private_home` 사본의 `config.toml` 끝에 덧붙인다. 판정 사본 경로 · 얼린 입력 경로 · 전용 TMPDIR 경로를 그 실행의 절대 경로로 채운다.
  - 판정 Codex 를 부를 때 `TMPDIR` 환경 변수를 전용 폴더로 준다. `/tmp`(`:slash_tmp`)는 막는다.
- 사전 측정도 전용 TMPDIR(`TMPDIR` · `TMP` · `TEMP` 환경 변수)로 돌리고 끝나면 지운다.
- 판정 사본은 `keep=True` 를 없애고 판정 뒤 지운다. `report.md` 의 판정 사본 목록 절은 「지웠다」 로 바꾸거나 뺀다.
- 감독이 만드는 임시 폴더 이름에 공통 앞머리(예: `codex-audit-`)와 감독 폴더를 가리킬 수 있는 표식을 둬서, 증명 측정이 「이 감독이 만든 것」 만 셀 수 있게 한다. 중단 신호(`cleanup()`)에서도 지운다.
- `premeasure.md` 를 바꾼다 — 사전 측정이 있는 조건은 그 기록을 증거로 쓰고 같은 명령을 다시 돌리지 않는다. 기록이 모자라면 다시 돌리지 말고 그 사실을 분석에 적는다.
- 판정 프롬프트(`judge.md`)에 격리 범위(읽을 수 있는 곳 · 쓸 수 있는 곳)를 알려 판정이 막힌 경로를 헤매지 않게 한다.
- 문서: `harness/README.md` 의 Codex 감독 설정 문단에 격리 방식 · 임시 폴더 정리 · 사전 측정 재실행 금지를 고친다.

하지 않는 것: draft · revise · research 차례의 격리 방식 변경, 여러 모델 동시 판정(다음 스프린트), VS Code 상태 표시줄, 감독 모델 바꾸기, 사용자 설정 파일(`~/.codex-qa/config.toml` · `~/.claude/settings.json`) 수정, harness 버전 올리기.

## 5. 이 레포 계약 규칙 (반드시 읽고 따른다)

- 형식 정의: `harness/references/contract-schema.md`. 작성 절차와 함정: `harness/skills/sprint-contract/SKILL.md`. 설정: `.harness/project.yaml`(카테고리 Skill/`스킬` · Script/`스크립트` · Error/`오류` · Architecture/`구조`, 금지 패턴 `금지-01`~`금지-04`). 조건 번호에 영어 약자를 쓰지 않는다.
- 최근 본보기: `.harness/sprint-contract-codex-audit-progress.md` 와 개정 `.harness/sprint-amendments-codex-audit-progress.md`, 측정 묶음 `.harness/.meta/codex-audit-progress/measure/`(가짜 codex · 손 예제 재사용 가능).
- 측정은 판정 Codex 의 격리 공간 안에서도 돌 수 있게 한다(`rm -rf` 금지 · `ps` 에 기대지 않기). 이번 스프린트 뒤에는 판정 격리가 더 좁아지므로(홈 · `/tmp` 읽기 금지), 측정 묶음이 그 안에서 도는지 따진다. 못 도는 측정은 `.harness/project.yaml` 의 `codex_audit.premeasure` 를 이 계약의 측정 묶음(`.harness/.meta/codex-judge-isolation/measure/`)으로 바꿔 격리 밖에서 돈다는 점을 적는다.
- 측정은 글자 찾기가 아니라 실제로 돌려서 잰다(가짜 codex 로 `impl` 을 끝까지 돌리고 임시 폴더 수 · 권한 거부 기록을 본다). 진짜 Codex 판정 한 번은 증거로 한 번만 쓴다.
- 작업 폴더 W = `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/codex-judge-isolation`, 가지 `feat/codex-judge-isolation`, 시작 판 `BASE` = `fc9ab639` (harness 0.20.0 병합 커밋). 커밋 구간 상한은 `git rev-parse --verify -q feat/codex-judge-isolation`.
- 이 계약은 `codex-audit.sh draft` 로 쓴다.

## 6. 범위 확대 결정 (2026-10-07 오후, 사용자)

- 감독 키 충전 잔액이 12:02 에 0 이 됐다(`credit_balance_exhausted`, OpenAI 직접 요청으로 확인). 사용자 지시로 `~/Hub` 아래 46곳 `codex_audit.mode` 를 off 로 바꿨다. 이 계약은 `mode: off` 절차로 Claude 가 쓰고 Claude qa-evaluator 가 판정한다.
- 사용자: 「비용 · 성능 · 용량 · 속도 문제를 최적으로 다 잡자」 → 격리와 비용 항목을 한 스프린트로 합친다(`.harness/.meta/codex-audit-cost/requirements-draft.md` 의 항목 1~5 를 이 계약으로 흡수).
- 용량 실측: 판정 사본은 추적 파일 37MB 인데 남은 사본은 150~394MB, 측정 묶음이 만든 폴더 하나(`implementation-audit-…`) 4.0GB, 시스템 임시 폴더 8.3GB. 판정 한 차례 세션 기록 9MB.
- 권한 프로필 실측(codex 0.160.1, `codex sandbox -P`): `~/.ssh` · `/tmp`(`":slash_tmp" = "deny"`) · 홈 읽기와 얼린 입력 쓰기는 막히고, 사본 쓰기 · 입력 읽기 · 전용 TMPDIR 쓰기는 된다. python 은 `/opt/homebrew` 라이브러리, node 는 `/System/Library/OpenSSL` 설정을 읽어야 돈다.
- `codex_audit` 칸이 없으면 꺼짐을 기본값으로 바꾼다(사용자 확정).
- 모델 비교는 이 스프린트 다음 단계: gpt-6.1-sol · gpt-6-sol · gpt-6-luna · gpt-5.6-sol · gpt-5.6-terra · gpt-5.6-luna × 결함 판(7a5ac6e1) · 고친 판(829a3125) × 3회 = 36회. astra 는 뺀다(사용자). 충전 필요.
