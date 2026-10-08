---
feature: "Codex 감독 구독 사용량 상한 · API 키 로그인 막기 · 금액 코드 지우기"
slug: codex-audit-usage-cap
created: "2026-10-08 18:55"
complexity: "중간"
conditions: 16
status: done
owner_session: 35b5945f-4957-4359-9b18-2d22b3bafeb0
conditions_digest: sha256:fdf5647740feff2d
measurement_digest: sha256:115c554922854eaf
locked_at: "2026-10-08 19:06"
---

# Codex 감독 구독 사용량 상한 · API 키 로그인 막기 · 금액 코드 지우기

## 배경

- 2026-10-08 감독을 ChatGPT Pro 구독(`~/.codex-qa`, 모델 gpt-6.1-sol)으로 바꾸고 `~/Hub` 15 곳을 `mode: judge` 로 켰다. 구독은 금액 상한(`daily_budget_usd`)이 꺼지고, 한도는 Pro 의 5 시간 창 · 주간 창 사용량이다. 실측: sol 판정 한 차례가 5 시간 창 약 4~7 %, 주간 약 0.6 % — 하루 계약 19 개를 다 판정하면 주간 약 120 %.
- 사용자 결정(2026-10-08): 「3 ㄱㄱ」(사용량 비율 상한), 상한 값 「70%」, API 키는 「아예 안쓰는걸로」 · 「막고 코드도 지우기」. 이 맥의 API 키 사본은 이미 지웠다.
- 만들 것: (1) Codex 가 세션 기록의 `token_count` 사건에 싣는 `rate_limits` 중 null 이 아닌 마지막 값(창마다 `used_percent` · `window_minutes` · `resets_at`)를 차례가 끝날 때 사용 기록 `codex-audit-usage.jsonl` 의 `limits` 열쇠로 남긴다(`window_minutes` 300 → `5시간`, 10080 → `주간`, 그 밖은 `<분>분`, null 인 창은 뺀다). 응답(`turn.completed`)의 토큰 수가 없는 차례(시간 초과 등)도 세션 기록에 `rate_limits` 가 있으면 토큰 0 으로 줄을 남긴다. (2) 감독을 시작할 때 가장 최근 `limits` 가 있는 줄을 보고, 아직 안 풀린 창(`resets_at` 이 지금보다 뒤) 중 하나라도 `used` 가 상한 이상이면 Codex 를 부르지 않고 BLOCKED(`한도-사용량`)로 끝낸다. 상한은 `codex_audit.usage_limit_percent`(0 초과 100 이하 숫자, 그 밖이면 BLOCKED `설정-오류`), 칸이 없거나 비면 70. `used` 가 상한과 같아도 막는다. 못 읽는 `limits` 줄(숫자 아닌 `used` 등)은 `limits` 없는 줄로 치고 그 앞 줄을 본다. 실패 원인에 창 이름 · 사용 % · 상한 % · 풀리는 시각을 적는다. (3) 감독 폴더가 구독 로그인이 아니면(`auth.json` 이 없을 때 포함) 모든 verb 가 모델 확인과 Codex 호출 전에 BLOCKED(`로그인-없음`)로 끝나고 실패 원인에 「구독」 으로 로그인하라는 안내가 있다. (4) API 키 전용 코드를 지운다 — `daily_budget_usd` · `한도-예산` · 단가 파일 `harness/templates/codex-audit/prices.json` · 금액 계산 · 기록 줄의 `usd` · `plan` · API 키로만 도는 모델 목록 조회(`gpt_models` · `CODEX_AUDIT_MODELS_URL`, 구독에서는 늘 「키 로그인이 아니다」로 실패해 새 Codex 판 알림까지 죽였다). 모델 확인은 Codex 판 확인만 한다. `report.md` 의 `## 비용` 은 `## 사용량` 으로 바꿔 차례마다 토큰과 그 차례 뒤 창별 사용 % 를 적는다. `follow` 의 차례 끝 줄도 금액 대신 창별 사용 % 를 적는다. `codex-audit.sh usage` 는 오늘 차례 수와 최근 창별 사용 % · 풀리는 시각을 보인다.
- 리서치용 `~/.codex` 와 감독용 `~/.codex-qa` 는 같은 ChatGPT 계정이다(2026-10-08 `account_id` 지문 비교). 사용량 % 는 계정 전체 값이라 리서치 사용량도 이 상한 판정에 들어간다. 진행 상황과 사용량을 VS Code 상태 표시줄에 보이는 일은 다음 스프린트다(사용자 결정 「이 계약 먼저 → 상태 표시줄」).
- 이 계약은 감독이 꺼진 상태로 Claude 가 쓰고 Claude qa-evaluator 가 판정한다. 진짜 Codex 모델 호출은 0 번 — 측정은 가짜 codex 로 한다. 가짜 codex 는 실제 기록 모양대로 한 차례에 `token_count` 를 넷(null · 5 %/1 % · 12 %/3 % · null) 싣는다 — 마지막 null 아닌 값이 5 시간 12 % · 주간 3 %(한 시간 · 하루 뒤 풀림)다.
- W = `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/codex-usage-cap`, 가지 `feat/codex-audit-usage-cap`(origin/main `b699b17e` = harness 0.21.0 위), BASE = `b699b17e`. 측정 묶음 = `bash .harness/.meta/codex-audit-usage-cap/measure/measure.sh <조건 번호>`. 픽스처 감독 폴더의 기본 로그인은 구독 모양이다.
- 봉인 전 교차 진단(2026-10-08) 반영: 가짜 codex 의 `token_count` 를 실제 모양(여러 번 · null 섞임)으로, 스크립트-01 에 (h)~(l) 과 실패 원인 정규식, 스크립트-02 에 follow · 시간 초과, 스크립트-03 에 revise · `auth.json` 없음 · 모델 확인 순서, 스크립트-04 에 어제 줄, 스킬-01 · 재사용-01 금지 낱말을 더했다. 모델 목록 조회 지우기는 API 키 코드 지우기 결정에 따른다.
- 봉인 전 실측(BASE 판, 2026-10-08 18:50 · 교차 진단 반영 뒤 다시): 스크립트-01 · 02 · 03 · 04 · 스킬-01 · 구조-01 · 재사용-01 FAIL, 스크립트-05 · 06 PASS(지켜야 할 앞 동작). 남은 가짜 프로세스 0 개.

## Script

- [ ] 스크립트-01: Given 구독 모양 감독 폴더와 사용 기록, When impl 을 돌리면, Then 막히는 경우는 종료 2 · 갈래 `한도-사용량` · exec 0 번 · 로그인 확인 0 번 · 출력에 `Traceback` 0 개이고 `## 실패 원인` 이 정규식 `<창>\D*<사용>\s*%` · `<상한>\s*%` · `\d{1,2}:\d{2}`(풀리는 시각)에 맞는다 — (a) 최근 줄 `5시간` 75 % · 상한 칸 없음 → 막힘(5시간 · 75 · 70) (b) `주간` 75 % → 막힘(주간 · 75 · 70) (c) 95 % 지만 두 창 모두 풀림 → 종료 0 · exec 1 번 (d) 95 % 줄 뒤에 10 % 줄 → 종료 0 · exec 1 번 (e) 기록 없음 → 종료 0 · exec 1 번 (f) `usage_limit_percent: 80` 에 75 % → 종료 0 · exec 1 번 (g) `usage_limit_percent: 80` 에 85 % → 막힘(5시간 · 85 · 80) (h) `usage_limit_percent` 가 `abc` · `0` · `150` · `"70%"` → 넷 다 종료 2 · 갈래 `설정-오류` · exec 0 번 (i) 75 % 줄 뒤에 `limits` 없는 줄 → 막힘(5시간 · 75 · 70) (j) 정확히 70 % → 막힘(5시간 · 70 · 70) (k) 5 시간 창은 95 % 로 풀렸고 주간 창은 75 % 로 안 풀림 → 막힘(주간 · 75 · 70) (l) 75 % 줄 뒤에 `used` 가 글자인 줄 → 막힘(5시간 · 75 · 70) [exact, enumerated]
  측정: bash .harness/.meta/codex-audit-usage-cap/measure/measure.sh 스크립트-01
  음성 대조: BASE 판은 상한이 없어 (a) 가 종료 0 이라 FAIL 한다 (`measure.sh 스크립트-01 --base` 종료 1)
- [ ] 스크립트-02: Given 구독 모양 감독 폴더, When impl(판정 1 차례)을 돌리면, Then 사용 기록 줄이 1 개이고 그 줄의 `limits` 가 `5시간` used 12 · `주간` used 3 이며(null 아닌 마지막 `token_count` 값) 둘 다 `resets_at` 이 정수이고, 줄에 `usd` · `plan` 열쇠가 없으며, `report.md` `## 사용량` 에 `judge-1` · `5시간 12%` · `주간 3%` 가 한 줄에 있고, `report.md` 에 `달러` · `청구` 가 없으며, 같은 감독 폴더로 `codex-audit.sh follow <감독 폴더> --wait-seconds 1` 을 부르면 마지막 `차례 judge-1 끝` 줄에 `5시간 12%` 가 있고 출력에 `청구` 가 없다. 또 `timeout` 단계 · `CODEX_AUDIT_LIMIT=2` 로 돌리면 사용 기록 마지막 줄의 `limits` `5시간` used 가 12 다 [exact, enumerated]
  측정: bash .harness/.meta/codex-audit-usage-cap/measure/measure.sh 스크립트-02
  음성 대조: BASE 판은 `limits` 를 남기지 않아 FAIL 한다 (`measure.sh 스크립트-02 --base` 종료 1)
- [ ] 스크립트-03: Given API 키 모양 감독 폴더 두 가지(`OPENAI_API_KEY` 만 · `auth_mode: apikey`), When 각각 impl · draft · revise 를 돌리면, Then 여섯 경우 모두 종료 2 · 갈래 `로그인-없음` · 실패 원인에 `구독` · exec 0 번 · 로그인 확인 0 번 · 픽스처 `TMPDIR` 항목 수 0 · `report.md` 에 `## 모델 확인` 절이 없다(구독 확인이 모델 확인보다 먼저). 감독 폴더에 `auth.json` 이 없을 때 impl 도 종료 2 · 갈래 `로그인-없음` · exec 0 번이다 [exact, enumerated]
  측정: bash .harness/.meta/codex-audit-usage-cap/measure/measure.sh 스크립트-03
  음성 대조: BASE 판은 API 키로 그대로 돌아 종료 0 이라 FAIL 한다 (`measure.sh 스크립트-03 --base` 종료 1)
- [ ] 스크립트-04: Given 사용 기록에 어제 날짜 줄 1 개가 있는 구독 모양 감독 폴더에서 impl 을 한 번 돌린 뒤, When `codex-audit.sh usage` 를 부르면, Then 종료 0 이고 출력에 `5시간 12%` · `주간 3%` 와 정규식 `차례 1\b`(오늘 차례만 센다) · `\d{1,2}:\d{2}`(풀리는 시각)이 맞고 `달러` 가 없다 [exact, enumerated]
  측정: bash .harness/.meta/codex-audit-usage-cap/measure/measure.sh 스크립트-04
- [ ] 스크립트-05: Then 앞 측정 묶음 중 구독 모양으로 재는 조건 — `codex-audit-judge-guard` 의 스크립트-01 · 02 · 03, `codex-audit-auth-writeback` 의 스크립트-01 · 02 · 03 · 05 · 07 — 을 재는 가지만 이번 가지로 바꾼 사본으로 돌려 모두 종료 0 이고 `Traceback` 이 없다 [exact, enumerated]
  측정: bash .harness/.meta/codex-audit-usage-cap/measure/measure.sh 스크립트-05
- [ ] 스크립트-06: Given 구독 모양 감독 폴더와 `model: m-base` · `model_draft: m-draft` · `model_impl: m-impl`, Then draft 차례의 `-m` 은 `m-draft`, judge 차례의 `-m` 은 `m-impl` 이다 [exact, enumerated]
  측정: bash .harness/.meta/codex-audit-usage-cap/measure/measure.sh 스크립트-06

## Skill

- [ ] 스킬-01: `harness/README.md` Codex 감독 설정 문단에 `usage_limit_percent` · `70` · `## 사용량` · `한도-사용량` · `로그인-없음` 이 있고, `harness/templates/project.yaml` 의 `codex_audit` 칸에 `usage_limit_percent:` 줄이 있으며, 네 파일(`harness/README.md` · `harness/templates/project.yaml` · `harness/skills/sprint-contract/SKILL.md` · `harness/agents/qa-evaluator.md`)에 `daily_budget_usd` · `한도-예산` · `API 키로 쓴 만큼` · `## 비용` · `청구 없음` · `prices.json` · `CODEX_AUDIT_MODELS_URL` 이 하나도 없다 [exact, enumerated]
  측정: bash .harness/.meta/codex-audit-usage-cap/measure/measure.sh 스킬-01

## Architecture

- [ ] 구조-01: Given 구현이 커밋된 뒤, When `git diff --name-only b699b17e..$(git rev-parse --verify -q feat/codex-audit-usage-cap) -- . ':(exclude).harness'` 를 보면, Then 바뀐 경로가 `## 범위 경계` sprint-scope 목록 중 `.harness/` 밖 6 개의 부분집합이고 `harness/scripts/codex-audit.sh` 를 포함한다. 상한 ref 해석 실패면 FAIL [exact, enumerated]
  측정: bash .harness/.meta/codex-audit-usage-cap/measure/measure.sh 구조-01

## Anti-patterns

- [ ] 금지-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수
  측정: python3 scripts/validate-plugin.py harness --check=code-fence
- [ ] 금지-04: SKILL.md / agents/*.md frontmatter 에서 name 필드 누락 금지
  측정: python3 scripts/validate-plugin.py harness --check=frontmatter

## Reusability

- [ ] 재사용-01: 가지 끝 `codex-audit.sh` 에 `daily_budget` · `load_prices` · `turn_cost` · `money(` · `spent(` · `check_budget` · `SUBSCRIBED` · `subscribed` · `'usd'` · `usd=` · `달러` · `prices.json` · `gpt_models` · `MODELS_URL` 이 하나도 없고, 정규식 `\bsubscription\(` 가 2 곳(정의 1 · 감독 시작 때 판정 1)이며, 가지 끝에 `harness/templates/codex-audit/prices.json` 이 없다
  측정: bash .harness/.meta/codex-audit-usage-cap/measure/measure.sh 재사용-01
- [ ] 재사용-02: N/A (새 공용 모듈을 만들지 않는다 — 기존 `check_budget` 자리를 사용량 확인으로 바꾸고 `read_usage` · `record_usage` · `usage_report` 를 고쳐 쓴다)

## Diagnostics

- [ ] 진단-01: N/A (commands.analyze `bash -n scripts/release.sh` 는 이번 변경 파일을 재지 않는다 — 진단-04 가 `bash -n harness/scripts/codex-audit.sh` 를 잰다)
- [ ] 진단-02: 변경한 마크다운 파일(`harness/README.md` · `harness/skills/sprint-contract/SKILL.md` · `harness/agents/qa-evaluator.md` · 이 계약) 네 개를 모두 가지 끝에서 읽었고(못 읽은 파일이 있으면 FAIL), BASE 대비 더한 줄에 걸린 markdownlint-cli2 0.23.2 경고(MD013 끔)가 0 개다
  측정: bash .harness/.meta/codex-audit-usage-cap/measure/measure.sh 진단-02
  양성 대조: MD013 을 켜고 파일 전체 줄을 세면 1 이상이 나온다 (`measure.sh 진단-02 --positive`)
- [ ] 진단-03: N/A (commands.test `bash scripts/release.sh` 는 이번 변경과 무관 — 진단-04 가 측정 묶음 전체를 잰다)
- [ ] 진단-04: `bash -n harness/scripts/codex-audit.sh` 종료 0, `python3 scripts/validate-plugin.py harness` 종료 0, 측정 묶음 전체(`measure.sh all --skip 진단-04`) 종료 0 · `Traceback` 0 개, `.github/workflows/ci.yml` 의 한 줄 `run:` 명령 중 `python3 scripts/` · `bash harness/` · `bash flutter-toolkit/` 로 시작하는 것 전부(0 개면 FAIL)를 W 에서 돌려 실패 0
  측정: bash .harness/.meta/codex-audit-usage-cap/measure/measure.sh 진단-04

## 범위 경계

- 하지 않는 것: 감독 폴더 `config.toml` 수정, 15 곳 프로젝트 설정 고치기(칸이 없으면 70 이 기본이라 손대지 않는다), harness 버전 올리기(이 스프린트 뒤 따로), 차례 도중 상한을 넘었을 때 그 감독을 멈추기 — 상한 확인은 감독을 시작할 때 한 번이다.
- 여러 감독이 거의 동시에 시작하면 모두 같은 마지막 기록(예: 69 %)을 보고 통과할 수 있다 — 시작 때 한 번 확인하는 방식의 한계로 두고, 상한을 70 으로 낮게 잡아 메운다.
- 사용량 비율은 Codex 가 다음 차례 때 갱신하는 값이라 마지막 기록 뒤 다른 곳(직접 Codex 쓰기 · 리서치)에서 쓴 사용량은 다음 감독의 첫 차례가 끝나야 보인다. 그래서 상한을 100 이 아니라 70 으로 둔다.
- 앞 측정 묶음 중 API 키 모양을 쓰는 조건(`codex-audit-auth-writeback` 스크립트-04 · 06 · 08, `codex-audit-subscription` 전부, `codex-audit-judge-guard` 스크립트-04)과 `## 비용` · 금액 문구를 재는 조건은 이 계약이 그 동작을 지우므로 이제 FAIL 하는 것이 맞다 — 스크립트-05 는 구독 모양 조건만 돌리고, 역할별 모델은 스크립트-06 이 구독 모양으로 다시 잰다.
- 커버리지 해소: 스크립트-01 · 02 · 03 · 04 · 05 · 06 · 스킬-01 · 구조-01 — 측정 줄은 `measure.sh <번호>` 한 명령이고 열거 대상은 `measure.py` 의 같은 이름 함수(`PREVIOUS` · `SCOPE` 상수 · 낱말 목록)가 같은 표기로 잰다.

```text
# sprint-scope
harness/scripts/codex-audit.sh
harness/templates/project.yaml
harness/templates/codex-audit/prices.json
harness/README.md
harness/skills/sprint-contract/SKILL.md
harness/agents/qa-evaluator.md
.harness/
```
