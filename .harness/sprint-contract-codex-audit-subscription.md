---
feature: "Codex 감독 구독 로그인 · 역할별 모델"
slug: codex-audit-subscription
created: "2026-10-08 14:13"
complexity: "중간"
conditions: 18
status: active
owner_session: 35b5945f-4957-4359-9b18-2d22b3bafeb0
conditions_digest: sha256:163c95903f06c11d
measurement_digest: sha256:0f01372beff514eb
locked_at: "2026-10-08 14:18"
---

# Codex 감독 구독 로그인 · 역할별 모델

## 배경

- 사용자 결정(2026-10-08): 감독을 API 키 종량제 대신 ChatGPT Pro 구독으로 돌린다. 계약 작성은 Codex(좋은 모델), 판정은 luna(생각 강도를 올려서). 「계속 로그인해 줘야 하냐 — 알아서 갱신되게」.
- 감독 폴더 `~/.codex-qa` 는 2026-10-08 구독으로 로그인했다(`auth_mode: chatgpt`, 갱신 열쇠 있음). API 키 로그인은 `auth.json.apikey-bak-20261008` 로 남겼다.
- 지금 스크립트는 차례마다 감독 폴더의 `auth.json` · `config.toml` 을 임시 폴더로 복사해 쓰고 지운다(`private_home`). API 키는 바뀌지 않아 괜찮았지만, 구독 로그인은 쓰는 도중 새 로그인 정보로 갱신될 수 있고 그것이 사본과 함께 버려진다. 그래서 구독이면 복사하지 않고 감독 폴더를 그대로 쓴다 — 갱신은 Codex 가 자기 폴더에서 한다.
- 리서치용 `~/.codex` 는 플러그인 · MCP 서버(`node_repl`)가 걸려 있어 판정에 쓰면 격리 밖 도구가 열린다. 그래서 감독 전용 폴더를 쓴다.
- 판정 격리 설정은 감독 폴더의 `config.toml` 을 건드리지 않고, 차례마다 `<감독 폴더>/codex-audit-<번호>.config.toml` 를 만들어 `-p` 로 붙인 뒤 지운다. `codex sandbox -p … -P codex-audit-judge` 로 이 방식에서도 `~/.ssh` 가 막히고 입력 읽기 · 사본 쓰기가 됨을 봉인 전에 확인했다(codex 0.160.1).
- 공개 이름(구현이 만들 값): 설정 칸 `codex_audit.model_draft` · `codex_audit.model_impl`, 비용 문구 `구독 — 청구 없음`, 상한 건너뜀 문구 `구독이라 하루 상한을 건너뛴다`, 사용 기록 열쇠 `plan`(`chatgpt` | `apikey`).
- 이 계약은 감독이 꺼진 상태로 Claude 가 쓰고 Claude qa-evaluator 가 판정한다. 진짜 Codex 호출은 0 번 — 측정은 가짜 codex 와 로그인 없이 도는 `codex sandbox` 로 한다.
- W = `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/codex-judge-isolation`, 가지 `feat/codex-audit-judge-mode`(PR #136 에 이어 올린다), BASE = `da5cf49a`. 측정 묶음 = `bash .harness/.meta/codex-audit-subscription/measure/measure.sh <조건 번호>`(가지 끝, `--base` 면 BASE 의 `harness/` 로 가짜 codex 감독을 끝까지 돌리고 자기 임시 폴더를 지운다). 픽스처 감독 폴더의 `auth.json` 은 구독 모양(`auth_mode: chatgpt` · `tokens`) 또는 API 키 모양(`auth_mode: apikey` · `OPENAI_API_KEY`)이다. 가짜 codex 는 구독 모양일 때 차례마다 `CODEX_HOME/auth.json` 의 `tokens.access_token` 을 `refreshed-<차례 번호>` 로 바꿔 갱신을 흉내 낸다.

## Script

- [ ] 스크립트-01: Given 구독 모양 감독 폴더, When impl(REJECT → 재심) · draft · revise 를 돌리면, Then 세 경우 모두 모든 codex 호출(로그인 확인 포함)의 `CODEX_HOME` 이 감독 폴더 자신이고, 각 감독이 끝난 뒤 감독 폴더 `auth.json` 의 `tokens.access_token` 이 그 감독 마지막 차례의 `refreshed-<번호>` 다(갱신이 버려지지 않는다) [exact, enumerated]
  측정: bash .harness/.meta/codex-audit-subscription/measure/measure.sh 스크립트-01
  음성 대조: BASE 판은 임시 사본을 `CODEX_HOME` 으로 써서 FAIL 한다 (`measure.sh 스크립트-01 --base` 종료 1)
- [ ] 스크립트-02: Given 구독 모양 감독 폴더, When impl(REJECT → 재심)을 돌리면, Then 판정 · 재심 호출 인자에 `-p codex-audit-` 로 시작하는 이름과 `default_permissions="codex-audit-judge"` 가 있고 `-s` 가 0 개이며, 그 이름의 `<감독 폴더>/<이름>.config.toml` 이 차례 중에 있었고 그 안의 `[permissions.codex-audit-judge.network]` 가 `enabled = false` 다. 감독이 끝난 뒤(정상 끝 · judge 차례 중 SIGTERM 두 경우 모두) 감독 폴더의 `codex-audit-*.config.toml` 이 0 개이고 `config.toml` 이 감독 전과 바이트 단위로 같다 [exact, enumerated]
  측정: bash .harness/.meta/codex-audit-subscription/measure/measure.sh 스크립트-02
  음성 대조: BASE 판은 `-p` 를 쓰지 않아 FAIL 한다 (`measure.sh 스크립트-02 --base` 종료 1)
- [ ] 스크립트-03: Given 구독 모양 감독 폴더의 judge 차례가 멈춰 있는 동안, When 그 차례의 프로필 파일로 진짜 `codex sandbox -p <이름> -P codex-audit-judge -C <판정 사본>` 을 그 차례의 `TMPDIR` · `PATH` 로 돌리면, Then 판정 사본 쓰기 됨 · 얼린 입력 읽기 됨 · 얼린 입력 쓰기 막힘 · `~/.ssh` 읽기 막힘 · 감독 폴더 `auth.json` 읽기 막힘 5 칸이다. `~/.ssh` 가 없는 환경이면 그 칸은 `[미검증:ENV]` 로 적고 나머지 4 칸으로 판정한다. 진짜 `codex` 를 못 찾으면 FAIL 이 아니라 `[미검증:ENV]` 다 [exact, enumerated]
  측정: bash .harness/.meta/codex-audit-subscription/measure/measure.sh 스크립트-03
- [ ] 스크립트-04: Given API 키 모양 감독 폴더 두 가지(`auth_mode: apikey` 가 있는 것 · `OPENAI_API_KEY` 만 있는 것), When 각각 impl(REJECT → 재심)을 돌리면, Then 모든 codex 호출의 `CODEX_HOME` 이 감독 폴더가 아닌 임시 사본이고, 감독이 끝난 뒤 픽스처 TMPDIR 항목 수가 0 이며 감독 폴더 `auth.json` 이 감독 전과 바이트 단위로 같고, 사용 기록 줄의 `plan` 이 `apikey` 다 — 구독이 아닌 경로는 기존대로 사본을 쓴다(감독 폴더를 늘 그대로 쓰는 구현을 잡는다) [exact, enumerated]
  측정: bash .harness/.meta/codex-audit-subscription/measure/measure.sh 스크립트-04
- [ ] 스크립트-05: Given `model: m-base` · `model_draft: m-draft` · `model_impl: m-impl` · `effort_impl: max` 픽스처, Then draft · revise 차례의 `-m` 은 `m-draft`, judge · review · research 차례의 `-m` 은 `m-impl` 이고 judge 차례 인자에 `model_reasoning_effort="max"` 가 있다. `model_draft` 만 지우면 draft 는 `m-base` · judge 는 `m-impl`, `model_impl` 만 지우면 draft 는 `m-draft` · judge 는 `m-base`, 둘 다 지우면 모든 차례가 `m-base` 다. `CODEX_AUDIT_MODEL=m-env` 면 모든 차례가 `m-env` 다 [exact, enumerated]
  측정: bash .harness/.meta/codex-audit-subscription/measure/measure.sh 스크립트-05
  음성 대조: BASE 판은 역할별 칸을 몰라 draft 차례가 `m-base` 라 FAIL 한다 (`measure.sh 스크립트-05 --base` 종료 1)
- [ ] 스크립트-06: Given 구독 모양 감독 폴더와 가짜 codex 사용량(입력 1,000,000 · 캐시 900,000 · 출력 20,000, 모델 `gpt-6.1-sol`), Then `report.md` `## 비용` 의 차례 줄과 합계 줄에 `구독 — 청구 없음` 이 있고 차례 줄에 `1,000,000` 이 있으며, 사용 기록 마지막 줄의 `usd` 가 `null` · `plan` 이 `chatgpt` 다. 같은 모델로 `daily_budget_usd: 0.50` 이고 오늘 합계 0.74 여도 구독이면 impl 이 종료 0 으로 돌고 `report.md` 에 `구독이라 하루 상한을 건너뛴다` 가 있다. API 키 모양이면 같은 상한 · 같은 기록(구독 `usd: null` 줄이 섞여 있어도 오늘 합계 0.74)에서 종료 2 · 갈래 `한도-예산` 이고, API 키 경로의 차례 줄은 `0.49달러` 다 [exact, enumerated]
  측정: bash .harness/.meta/codex-audit-subscription/measure/measure.sh 스크립트-06
  음성 대조: BASE 판은 구독에도 금액을 적고 상한에서 막혀 FAIL 한다 (`measure.sh 스크립트-06 --base` 종료 1)
- [ ] 스크립트-07: Given 같은 구독 감독 폴더를 쓰는 impl 두 개가 동시에 judge 차례에서 멈춰 있을 때, Then 두 차례의 `-p` 이름이 서로 다르고, 한쪽을 끝내도 다른 쪽 프로필 파일이 남아 있으며, 둘 다 끝난 뒤 감독 폴더에 감독 전에 없던 항목은 `sessions` · `codex-audit-usage.jsonl` · `codex-audit-models.json` 밖에 0 개이고 감독 전에 있던 항목은 하나도 사라지지 않는다 [exact, enumerated]
  측정: bash .harness/.meta/codex-audit-subscription/measure/measure.sh 스크립트-07
- [ ] 스크립트-08: Given 구독 모양 감독 폴더, Then 로그인 확인(`codex login status`) 호출의 `CODEX_HOME` 이 감독 폴더 자신이고, 가짜 codex 가 로그인 실패를 내면 impl 이 종료 2 · 갈래 `로그인-없음` 이며 `exec` 호출이 0 번이다 [exact]
  측정: bash .harness/.meta/codex-audit-subscription/measure/measure.sh 스크립트-08

## Skill

- [ ] 스킬-01: `harness/README.md` Codex 감독 설정 문단에 `model_draft` · `model_impl` · `구독` 이 있고, `harness/templates/project.yaml` 의 `codex_audit` 칸에 `model_draft` · `model_impl` 줄이 있고, `harness/skills/sprint-contract/SKILL.md` 에 `model_draft` 가 있다 [exact, enumerated]
  측정: bash .harness/.meta/codex-audit-subscription/measure/measure.sh 스킬-01

## Architecture

- [ ] 구조-01: Given 구현이 커밋된 뒤, When `git diff --name-only da5cf49a..$(git rev-parse --verify -q feat/codex-audit-judge-mode) -- . ':(exclude).harness'` 를 보면, Then 바뀐 경로가 `## 범위 경계` sprint-scope 목록 중 `.harness/` 밖 4 개의 부분집합이고 `harness/scripts/codex-audit.sh` 를 포함한다. 상한 ref 해석 실패면 FAIL [exact, enumerated]
  측정: bash .harness/.meta/codex-audit-subscription/measure/measure.sh 구조-01

## Anti-patterns

- [ ] 금지-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수
  측정: python3 scripts/validate-plugin.py harness --check=code-fence
- [ ] 금지-04: SKILL.md / agents/*.md frontmatter 에서 name 필드 누락 금지
  측정: python3 scripts/validate-plugin.py harness --check=frontmatter

## Reusability

- [ ] 재사용-01: 판정 격리 설정은 구독 · API 키 두 경로가 같은 함수로 만든다 — `codex-audit.sh` 안에 `'[' + table + ']'` 처럼 권한 표 머리를 만드는 자리가 한 곳이고(`def judge_profile` 1 개), 구독 경로가 별도 표를 손으로 쓰지 않는다
  측정: bash .harness/.meta/codex-audit-subscription/measure/measure.sh 재사용-01
- [ ] 재사용-02: N/A (새 공용 모듈을 만들지 않는다 — 기존 `run_codex` · `login` · `drop_home` 의 감독 폴더 자리를 고쳐 쓴다)

## Diagnostics

- [ ] 진단-01: N/A (commands.analyze `bash -n scripts/release.sh` 는 이번 변경 파일을 재지 않는다 — 진단-04 가 `bash -n harness/scripts/codex-audit.sh` 를 잰다)
- [ ] 진단-02: 변경한 마크다운 파일(`harness/README.md` · `harness/skills/sprint-contract/SKILL.md` · 이 계약) 세 개를 모두 가지 끝에서 읽었고(못 읽은 파일이 있으면 FAIL), BASE 대비 더한 줄에 걸린 markdownlint-cli2 0.23.2 경고(MD013 끔)가 0 개다
  측정: bash .harness/.meta/codex-audit-subscription/measure/measure.sh 진단-02
  양성 대조: MD013 을 켜고 파일 전체 줄을 세면 1 이상이 나온다 (`measure.sh 진단-02 --positive`)
- [ ] 진단-03: N/A (commands.test `bash scripts/release.sh` 는 이번 변경과 무관 — 진단-04 가 측정 묶음 전체를 잰다)
- [ ] 진단-04: `bash -n harness/scripts/codex-audit.sh` 종료 0, `python3 scripts/validate-plugin.py harness` 종료 0, 측정 묶음 전체(`measure.sh all --skip 진단-04`) 종료 0 · `Traceback` 0 개, `.github/workflows/ci.yml` 의 한 줄 `run:` 명령 중 `python3 scripts/` · `bash harness/` · `bash flutter-toolkit/` 로 시작하는 것 전부(봉인 전 실측 34 개, 0 개면 FAIL)를 W 에서 돌려 실패 0
  측정: bash .harness/.meta/codex-audit-subscription/measure/measure.sh 진단-04

## 범위 경계

- 하지 않는 것: 리서치용 `~/.codex` 사용, 감독 폴더 `config.toml` 수정(사용자 설정 — 모델 바꾸기는 별도), 다른 저장소의 `mode: off` 되돌리기, 판정 모델 비교 실행(이 스프린트 뒤), harness 버전 올리기.
- 구독 경로에서 동시에 여러 감독이 같은 감독 폴더를 쓴다. 로그인 갱신 충돌은 Codex 가 자기 폴더에서 처리한다고 보고, 이 계약은 「사본에 갱신이 버려지지 않는다」(스크립트-01) · 「서로의 프로필 파일을 지우지 않는다」(스크립트-07) 까지만 잰다.
- `follow` 의 조용함 감지는 차례의 세션 기록을 차례 번호(thread)로 걸러 크기를 잰다. 구독 경로에서 감독 폴더 `sessions` 를 같이 쓰게 돼도 이 거름은 그대로라 조건으로 두지 않는다.
- 생각 강도는 기존 칸 `effort_draft` · `effort_impl` 로 정한다(스크립트-05 가 판정 차례에 실리는지 잰다). 판정 luna 의 강도 값 자체는 프로젝트 설정이라 이 계약 밖이다.
- 커버리지 해소: 스크립트-02 · 스크립트-07 · 스킬-01 · 구조-01 — 측정 줄은 `measure.sh <번호>` 한 명령이고 열거 대상은 `measure.py` 의 같은 이름 함수(`SCOPE` 상수 · 낱말 목록)가 같은 표기로 잰다.

```text
# sprint-scope
harness/scripts/codex-audit.sh
harness/templates/project.yaml
harness/README.md
harness/skills/sprint-contract/SKILL.md
.harness/
```
