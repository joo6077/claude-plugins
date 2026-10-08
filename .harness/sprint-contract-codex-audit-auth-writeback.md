---
feature: "Codex 감독 구독 로그인 — 사본 쓰고 갱신만 되돌려 쓰기"
slug: codex-audit-auth-writeback
created: "2026-10-08 14:31"
complexity: "중간"
conditions: 18
status: done
owner_session: 35b5945f-4957-4359-9b18-2d22b3bafeb0
conditions_digest: sha256:80088810feb9c37e
measurement_digest: sha256:46e309b59b638721
locked_at: "2026-10-08 15:08"
---

# Codex 감독 구독 로그인 — 사본 쓰고 갱신만 되돌려 쓰기

## 배경

- 앞 계약 `codex-audit-subscription`(APPROVE, 커밋 `2f98abee`)은 구독 로그인이면 감독 폴더 `~/.codex-qa` 를 그대로 `CODEX_HOME` 으로 썼다. 교차 진단이 계약 밖 결함을 짚었다 — 진짜 codex 가 자기 폴더에 남기는 부산물(`memories_1.sqlite` · `thread_history_1.sqlite` · `logs_2.sqlite` · `state_5.sqlite` · `shell_snapshots/`)이 감독 폴더에 쌓여 앞 판정이 다음 판정에 섞일 수 있고, 차례 번호를 못 받은 차례의 세션 기록이 감독 폴더에 남으며, 구독 여부를 차례마다 다시 읽어 중간에 API 키 경로로 빠질 수 있다. `~/.codex-qa` 에는 10-06 에 생긴 `memories_1.sqlite` · `thread_history_1.sqlite` 가 이미 있다.
- 사용자 결정(2026-10-08): 「고치고 시험 (추천)」 — 실제 구독 시험 전에 고친다.
- 고치는 방향: 구독이어도 차례마다 예전처럼 임시 사본을 `CODEX_HOME` 으로 쓰고, 차례가 끝나면 사본의 `auth.json` 이 사본을 뜰 때와 달라졌을 때만 감독 폴더에 되돌려 쓴다. 되돌려 쓰기는 감독 폴더의 잠금 파일 `codex-audit-auth.lock` 을 잡고, 감독 폴더 `auth.json` 이 사본을 뜰 때와 바이트 단위로 같을 때만 한다 — 그사이 다른 감독이나 사용자가 바꿨으면 덮지 않는다. 되돌려 쓰기 규칙: 사본 `auth.json` 이 JSON 으로 읽히고 `auth_mode` 가 `chatgpt` 일 때만 쓰고, 잠금은 `fcntl.flock` 으로 잡되 10 초 안에 못 잡으면 되돌려 쓰지 않고 `report.md` 에 한 줄 남기며, 잠금 파일은 지우지 않고(권한 600), 쓰는 동안 신호를 미뤄 두고(`signal.pthread_sigmask`), 같은 폴더 임시 파일(권한 600)에 쓴 뒤 `os.replace` 로 바꾼다. 로그인 확인 차례와 시간 초과 · 중단 신호로 끝난 차례도 같은 되돌려 쓰기를 거친다. 구독인지는 감독을 시작할 때 하루 상한 확인보다 먼저 한 번만 판정한다. 판정 격리 설정은 앞 격리 스프린트처럼 사본의 `config.toml` 에 붙이고 `-p` 를 쓰지 않는다.
- 공개 이름(구현이 만들 값): 잠금 파일 `codex-audit-auth.lock`. 앞 계약의 `model_draft` · `model_impl` · `구독 — 청구 없음` · `구독이라 하루 상한을 건너뛴다` · `plan` 은 그대로 둔다.
- 이 계약은 감독이 꺼진 상태로 Claude 가 쓰고 Claude qa-evaluator 가 판정한다. 진짜 Codex 모델 호출은 0 번 — 측정은 가짜 codex 와 로그인 없이 도는 `codex sandbox` 로 한다.
- W = `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/codex-judge-isolation`, 가지 `feat/codex-audit-judge-mode`, BASE = `2f98abee`. 측정 묶음 = `bash .harness/.meta/codex-audit-auth-writeback/measure/measure.sh <조건 번호>`(가지 끝, `--base` 면 BASE 의 `harness/` 로 가짜 codex 감독을 끝까지 돌리고, 자기 임시 폴더와 기록된 가짜 codex 프로세스를 끝에서 지운다). 가짜 codex 는 구독 모양일 때 차례마다 `CODEX_HOME/auth.json` 의 `tokens.access_token` 을 `refreshed-<차례 번호>-<자기 pid>` 로 바꾸고(상태 폴더에 `no-refresh` 표식이 있으면 안 바꾸고, `hold-late` 단계는 멈췄다 풀린 뒤에 바꾸고, `corrupt` 단계는 `{` 로 깨뜨린다. `login-refresh` 표식이 있으면 로그인 확인도 `login-refreshed-<pid>` 로 바꾼다), 위 부산물 다섯 가지를 `CODEX_HOME` 에 만든다.
- 봉인 전 실측(BASE 판 = 지금 판, 2026-10-08 14:50 교차 진단 반영 뒤): 스크립트-01~07 · 스킬-01 · 구조-01 · 재사용-01 이 FAIL, 스크립트-08 이 PASS(지켜야 할 기존 동작). `measure.sh 스크립트-03 --base` 3 회 모두 종료 1(교차 진단 전 판은 7 회 중 5 회 PASS 로 순서 운에 갈렸다 — `hold-late` 로 고침). 교차 진단 전 판 측정이 남긴 가짜 codex 3 개는 끄고, 측정 묶음이 끝날 때 기록된 가짜 pid 를 끄게 고쳤다. 진단-04 의 로컬 CI 명령은 앞 계약 봉인 전 실측 34 개다.

## Script

- [ ] 스크립트-01: Given 구독 모양 감독 폴더, When impl(REJECT → 재심) · draft · revise 를 돌리면, Then 세 경우 모두 모든 codex 호출(로그인 확인 포함)의 `CODEX_HOME` 이 픽스처 `TMPDIR` 아래 임시 사본이고(감독 폴더 자신이면 FAIL), 각 감독이 끝난 뒤 감독 폴더 `auth.json` 의 `tokens.access_token` 이 그 감독 마지막 차례가 만든 값이며 권한이 600 이고, 픽스처 `TMPDIR` 항목 수가 0 이다. 또 (a) 로그인 확인만 갱신하는 경우(`login-refresh` · `no-refresh`) 토큰이 로그인 확인이 만든 값이고 (b) 시간 초과 차례(`timeout` 단계, `CODEX_AUDIT_LIMIT=2`) 뒤 토큰이 그 차례가 만든 값이며 픽스처 `TMPDIR` 항목 수가 0 이다 [exact, enumerated]
  측정: bash .harness/.meta/codex-audit-auth-writeback/measure/measure.sh 스크립트-01
  음성 대조: BASE 판은 감독 폴더를 `CODEX_HOME` 으로 써서 FAIL 한다 (`measure.sh 스크립트-01 --base` 종료 1)
- [ ] 스크립트-02: Given 구독 모양 감독 폴더, When impl(REJECT → 재심)을 정상으로 끝내거나 judge 차례 중 SIGTERM 으로 끝내면, Then 두 경우 모두 감독 폴더에 감독 전에 없던 항목이 `codex-audit-usage.jsonl` · `codex-audit-models.json` · `codex-audit-auth.lock` 밖에 0 개이고(부산물 다섯 가지가 생기면 FAIL), 감독 전에 있던 항목이 하나도 사라지지 않고, `config.toml` 이 바이트 단위로 같으며 `codex-audit-*.config.toml` 이 0 개다. 정상 끝의 판정 · 재심 호출 인자에 `-p` · `-s` 가 0 개이고 `default_permissions="codex-audit-judge"` 가 있으며, 차례마다 가짜 codex 가 읽은 사본 `config.toml` 이 감독 폴더 `config.toml` 바이트로 시작하고 `[permissions.codex-audit-judge]` 를 정확히 1 번 담는다. SIGTERM 뒤 감독 폴더 `auth.json` 의 `access_token` 이 그 차례가 만든 값이고 픽스처 `TMPDIR` 항목 수가 0 이다 [exact, enumerated]
  측정: bash .harness/.meta/codex-audit-auth-writeback/measure/measure.sh 스크립트-02
  음성 대조: BASE 판은 `-p` 를 쓰고 부산물을 감독 폴더에 남겨 FAIL 한다 (`measure.sh 스크립트-02 --base` 종료 1)
- [ ] 스크립트-03: Given 구독 모양 감독 폴더와 풀린 뒤에 갱신하는 가짜 codex 차례(`hold-late`), Then (a) judge 차례가 멈춘 동안 바깥에서 감독 폴더 `auth.json` 을 `access_token: outside-newer` 로 바꾸면 감독이 끝난 뒤에도 `outside-newer` 다 (b) 같은 감독 폴더를 쓰는 impl 두 개가 동시에 멈춘 뒤 먼저 하나를 끝내면 토큰이 그 감독 차례가 만든 값이 되고, 나머지를 끝낸 뒤에도 그 값 그대로다 (c) 측정이 `codex-audit-auth.lock` 에 `flock(LOCK_EX)` 를 잡은 채 차례를 풀면 3 초 동안 토큰이 `original` 그대로이고, 놓은 뒤 그 차례가 만든 값이 된다 (d) (c) 처럼 잠금을 잡은 동안 감독에 SIGTERM 을 보내고 놓으면 토큰이 그 차례가 만든 값이고, 감독 폴더 새 항목이 위 세 이름 밖에 0 개, 픽스처 `TMPDIR` 항목 수가 0 이다 [exact, enumerated]
  측정: bash .harness/.meta/codex-audit-auth-writeback/measure/measure.sh 스크립트-03
  음성 대조: BASE 판은 감독 폴더를 직접 고쳐 (a) 에서 FAIL 한다 (`measure.sh 스크립트-03 --base` 를 3 번 돌려 3 번 모두 종료 1)
- [ ] 스크립트-04: Given (a) 가짜 codex 가 로그인 파일을 바꾸지 않는 구독 모양 감독 폴더 (b) 가짜 codex 가 사본 로그인 파일을 `{` 로 깨뜨리는 구독 모양 감독 폴더(`corrupt`) (c) API 키 모양 감독 폴더 두 가지(`OPENAI_API_KEY` 만 있는 것 · `auth_mode: apikey` 가 있는 것), When 각각 impl 을 돌리면, Then (a) 감독 폴더 `auth.json` 의 바이트와 수정 시각(`st_mtime_ns`)이 감독 전과 같다 (b) 감독 폴더 `auth.json` 바이트가 감독 전과 같다(깨진 사본을 되돌려 쓰지 않는다) (c) 모든 exec 호출의 `CODEX_HOME` 이 픽스처 `TMPDIR` 아래 사본이고, 픽스처 `TMPDIR` 항목 수 0, `auth.json` 바이트 동일, `codex-audit-auth.lock` 이 생기지 않고, 사용 기록 모든 줄의 `plan` 이 `apikey` 다 [exact, enumerated]
  측정: bash .harness/.meta/codex-audit-auth-writeback/measure/measure.sh 스크립트-04
  음성 대조: BASE 판은 깨진 파일을 감독 폴더에 직접 써서 (b) 에서 FAIL 한다 (`measure.sh 스크립트-04 --base` 종료 1)
- [ ] 스크립트-05: Given 구독 모양 감독 폴더와 차례 번호(`thread.started`)를 내지 않고 세션 기록만 남기는 가짜 codex 차례, When impl 을 돌리면, Then 감독 폴더 아래 `rollout-*.jsonl` 이 0 개이고 픽스처 `TMPDIR` 항목 수가 0 이다 [exact]
  측정: bash .harness/.meta/codex-audit-auth-writeback/measure/measure.sh 스크립트-05
  음성 대조: BASE 판은 그 기록을 감독 폴더 `sessions` 에 남겨 FAIL 한다 (`measure.sh 스크립트-05 --base` 종료 1)
- [ ] 스크립트-06: Given 구독 모양 감독 폴더, When impl(REJECT → 재심)의 judge 차례가 멈춘 동안 감독 폴더 `auth.json` 을 읽히지 않는 내용 `{` 로 바꾸고 이어 가면, Then 차례가 2 개(판정 · 재심)이고 사용 기록 두 줄의 `plan` 이 모두 `chatgpt`, `report.md` `## 비용` 의 모든 목록 줄(`-` 와 빈칸으로 시작하는 줄)에 `구독 — 청구 없음` 이 있으며, 감독 폴더 `auth.json` 이 `{` 그대로다(바뀐 파일을 덮지 않는다) [exact, enumerated]
  측정: bash .harness/.meta/codex-audit-auth-writeback/measure/measure.sh 스크립트-06
  음성 대조: BASE 판은 차례마다 구독 여부를 다시 읽어 `plan` 이 `apikey` 로 빠져 FAIL 한다 (`measure.sh 스크립트-06 --base` 종료 1)
- [ ] 스크립트-07: Given 구독 모양 감독 폴더의 judge 차례가 멈춘 동안, When 그 차례의 `CODEX_HOME`(사본) · `TMPDIR` · `PATH` 로 진짜 `codex sandbox -P codex-audit-judge -C <판정 사본>` 을 돌리면, Then 판정 사본 쓰기 됨 · 얼린 입력 읽기 됨 · 얼린 입력 쓰기 막힘 · `~/.ssh` 읽기 막힘 · 감독 폴더 `auth.json` 읽기 막힘 · 사본 `auth.json` 읽기 막힘 6 칸이다. `~/.ssh` 가 없는 환경이면 그 칸은 `[미검증:ENV]` 로 적고 나머지 5 칸으로 판정한다. 진짜 `codex` 를 못 찾으면 FAIL 이 아니라 `[미검증:ENV]` 다 [exact, enumerated]
  측정: bash .harness/.meta/codex-audit-auth-writeback/measure/measure.sh 스크립트-07
- [ ] 스크립트-08: Then 앞 계약 측정 묶음의 역할별 모델 조건과 비용 조건(`bash .harness/.meta/codex-audit-subscription/measure/measure.sh 스크립트-05` · `… 스크립트-06`)이 가지 끝에서 둘 다 종료 0 이고, 구독 모양 감독 폴더에서 가짜 codex 가 로그인 실패를 내면 impl 이 종료 2 · 갈래 `로그인-없음` · exec 0 번이며 픽스처 `TMPDIR` 항목 수가 0 이다 [exact, enumerated]
  측정: bash .harness/.meta/codex-audit-auth-writeback/measure/measure.sh 스크립트-08

## Skill

- [ ] 스킬-01: `harness/README.md` 의 Codex 감독 설정 문단에 `codex-audit-auth.lock` 과 `되돌려 쓴다` 가 있고, 옛 문구 넷(`감독 폴더를 그대로 쓴다` · `복사하지 않고` · `` `-p` 로 붙`` · `codex-audit-<번호>.config.toml`)이 하나도 없다 [exact, enumerated]
  측정: bash .harness/.meta/codex-audit-auth-writeback/measure/measure.sh 스킬-01

## Architecture

- [ ] 구조-01: Given 구현이 커밋된 뒤, When `git diff --name-only 2f98abee..$(git rev-parse --verify -q feat/codex-audit-judge-mode) -- . ':(exclude).harness'` 를 보면, Then 바뀐 경로가 `## 범위 경계` sprint-scope 목록 중 `.harness/` 밖 2 개의 부분집합이고 `harness/scripts/codex-audit.sh` 를 포함한다. 상한 ref 해석 실패면 FAIL [exact, enumerated]
  측정: bash .harness/.meta/codex-audit-auth-writeback/measure/measure.sh 구조-01

## Anti-patterns

- [ ] 금지-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수
  측정: python3 scripts/validate-plugin.py harness --check=code-fence
- [ ] 금지-04: SKILL.md / agents/*.md frontmatter 에서 name 필드 누락 금지
  측정: python3 scripts/validate-plugin.py harness --check=frontmatter

## Reusability

- [ ] 재사용-01: 판정 격리 설정은 한 함수로만 만들고 구독 여부는 한 곳에서만 판정한다 — 가지 끝 `codex-audit.sh` 에 `def judge_profile(` 1 개, `'[' + table + ']'` 1 곳, `'-p'` 0 곳, 정규식 `\bsubscription\(` 2 곳(정의 1 · 감독 시작 때 판정 1)이다
  측정: bash .harness/.meta/codex-audit-auth-writeback/measure/measure.sh 재사용-01
- [ ] 재사용-02: N/A (새 공용 모듈을 만들지 않는다 — 기존 `private_home` · `drop_home` · `login` · `run_codex` 를 고쳐 쓴다)

## Diagnostics

- [ ] 진단-01: N/A (commands.analyze `bash -n scripts/release.sh` 는 이번 변경 파일을 재지 않는다 — 진단-04 가 `bash -n harness/scripts/codex-audit.sh` 를 잰다)
- [ ] 진단-02: 변경한 마크다운 파일(`harness/README.md` · 이 계약) 두 개를 모두 가지 끝에서 읽었고(못 읽은 파일이 있으면 FAIL), BASE 대비 더한 줄에 걸린 markdownlint-cli2 0.23.2 경고(MD013 끔)가 0 개다
  측정: bash .harness/.meta/codex-audit-auth-writeback/measure/measure.sh 진단-02
  양성 대조: MD013 을 켜고 파일 전체 줄을 세면 1 이상이 나온다 (`measure.sh 진단-02 --positive`)
- [ ] 진단-03: N/A (commands.test `bash scripts/release.sh` 는 이번 변경과 무관 — 진단-04 가 측정 묶음 전체를 잰다)
- [ ] 진단-04: `bash -n harness/scripts/codex-audit.sh` 종료 0, `python3 scripts/validate-plugin.py harness` 종료 0, 측정 묶음 전체(`measure.sh all --skip 진단-04`) 종료 0 · `Traceback` 0 개, `.github/workflows/ci.yml` 의 한 줄 `run:` 명령 중 `python3 scripts/` · `bash harness/` · `bash flutter-toolkit/` 로 시작하는 것 전부(0 개면 FAIL)를 W 에서 돌려 실패 0
  측정: bash .harness/.meta/codex-audit-auth-writeback/measure/measure.sh 진단-04

## 범위 경계

- 하지 않는 것: 사용자 감독 폴더 `~/.codex-qa` 의 기존 부산물 지우기(사용자 파일 — 지울지는 따로 묻는다), 감독 폴더 `config.toml` 수정, 기억 기능 설정 바꾸기, 판정 모델 비교 실행, harness 버전 올리기.
- 갱신 열쇠가 한 번 쓰면 버려지는 방식일 때 두 감독이 같은 열쇠로 동시에 갱신하면 한쪽이 실패할 수 있다. 이 계약은 「먼저 되돌려 쓴 것을 나중 감독이 덮지 않는다」(스크립트-03)까지만 잰다 — 가짜 codex 로는 진짜 갱신 서버 동작을 잴 수 없다. 실제 구독 시험에서 로그인 끊김이 생기면 따로 다룬다.
- 앞 계약 측정 묶음의 스크립트-01 · 02 · 03 · 07 · 08 은 「감독 폴더를 그대로 쓴다」를 잰다. 이 계약이 그 설계를 바꾸므로 이제 FAIL 하는 것이 맞다 — 진단-04 · 스크립트-08 은 그 묶음에서 바뀌지 않는 스크립트-05 · 06 만 돌린다.
- 커버리지 해소: 스크립트-01 · 02 · 03 · 04 · 06 · 07 · 08 · 스킬-01 · 구조-01 — 측정 줄은 `measure.sh <번호>` 한 명령이고 열거 대상은 `measure.py` 의 같은 이름 함수(`ALLOWED_NEW` · `SCOPE` 상수 · 낱말 목록)가 같은 표기로 잰다.

```text
# sprint-scope
harness/scripts/codex-audit.sh
harness/README.md
.harness/
```
