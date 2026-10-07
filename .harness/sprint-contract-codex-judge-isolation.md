---
feature: "Codex 감독 판정 격리 · 용량 · 비용 · 속도 최적화"
slug: codex-judge-isolation
created: "2026-10-07 14:29"
complexity: "복잡"
conditions: 25
status: active
owner_session: 35b5945f-4957-4359-9b18-2d22b3bafeb0
conditions_digest: sha256:d1e0c6639fea2acf
measurement_digest: sha256:7d4bba22350ba3d0
locked_at: "2026-10-07 14:50"
---

## 배경

- 요구사항: `.harness/.meta/codex-judge-isolation/requirements.md` (1~6절). 6절이 사용자의 범위 확대 결정이다 — 격리와 비용 항목을 한 스프린트로, `codex_audit` 칸이 없으면 꺼짐, 모델 비교는 다음 단계(astra 제외 6모델).
- 감독 키 충전 잔액이 2026-10-07 12:02 에 0 이 돼 46곳 감독을 껐다. 이 계약은 `mode: off` 절차로 Claude 가 썼고 Claude qa-evaluator 가 판정한다. 진짜 Codex 호출은 0 번 쓴다 — 측정은 가짜 codex 와 로그인 없이 도는 `codex sandbox -P` 로만 한다.
- 실측 근거: 이틀 약 140달러(astra 120달러), 계약 작성 62 차례 · 판정 37 차례, 판정 평균 입력 0.81M 토큰, 남은 판정 사본 150~394MB(추적 파일은 37MB), 측정 묶음 폴더 하나 4.0GB, 판정 한 차례 세션 기록 9MB.
- 권한 프로필 실측(codex 0.160.1): `":root" = "deny"` · `":minimal" = "read"` · `":slash_tmp" = "deny"` 로 `~/.ssh` · `/tmp` · 홈 읽기와 얼린 입력 쓰기가 막히고, 사본 쓰기 · 입력 읽기 · 전용 TMPDIR 쓰기는 된다. python 은 `/opt/homebrew`, node 는 `/System/Library/OpenSSL` 읽기가 더 있어야 돈다.
- 공개 이름(구현이 만들 값, 조건이 이 이름으로 잰다): 권한 프로필 `codex-audit-judge`, 설정 칸 `codex_audit.daily_budget_usd`, 환경 변수 `CODEX_AUDIT_DRAFT_LIMIT` · `CODEX_AUDIT_MODEL`, 부속 명령 `usage`, 결과 파일 절 `## 비용`, 사용 기록 `<감독용 Codex 폴더>/codex-audit-usage.jsonl`, 단가 표 `harness/templates/codex-audit/prices.json`, 실패 갈래 `한도-예산`. 사용 기록 한 줄의 열쇠는 `date`(YYYY-MM-DD, 그 맥의 날짜) · `repo` · `slug` · `verb` · `turn` · `model` · `input` · `cached` · `output` · `usd`, 단가 표의 열쇠는 `checked` · `source` · `models.<모델>.input` · `.cached_input` · `.output`(1M 토큰당 달러).
- 단가 근거(2026-10-07, codex-research 가 developers.openai.com 모델 페이지 · 가격표에서 확인, 원문 세션 scratchpad `model-research/answer.md` · 메모 `project_codex_judge_model_comparison`): 입력 / 캐시 입력 / 출력 — gpt-6.1-sol 2.00 / 0.10 / 10.00 · gpt-6-sol 2.00 / 0.20 / 10.00 · gpt-6-luna 0.10 / 0.01 / 0.50 · gpt-5.6-sol 4.00 / 0.40 / 20.00 · gpt-5.6-terra 2.00 / 0.20 / 12.00 · gpt-5.6-luna 0.20 / 0.02 / 1.20. 구조-02 와 스크립트-06 은 이 값을 같이 쓴다.

### 공통 정의

- W = `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/codex-judge-isolation`, 가지 `feat/codex-judge-isolation`, BASE = `fc9ab639`.
- 측정 묶음 = `bash .harness/.meta/codex-judge-isolation/measure/measure.sh <조건 번호>`. W 에서 돌린다. 종료 코드 0 = PASS, 1 = FAIL. 가지 끝 커밋을 임시 폴더로 꺼내 그 안에서 가짜 codex 로 감독을 끝까지 돌리고, 끝나면 자기 임시 폴더를 지운다.
- 가짜 codex = 측정 묶음의 `fake.py`. 모델을 부르지 않는다. 호출 인자 · 환경 변수(`TMPDIR` 포함) · 지시문 · 그 차례의 `CODEX_HOME/config.toml` 을 기록하고, 정해진 토큰 사용량을 `turn.completed` 로 낸다.
- 픽스처 TMPDIR = 측정 묶음이 감독마다 따로 만든 빈 폴더. 감독은 이것을 시스템 임시 폴더로 받는다. 감독이 끝난 뒤 그 안에 남은 항목 수가 「남은 임시 폴더 수」다.

## Script

- [ ] 스크립트-01: Given 가짜 codex 로 impl(REJECT → 재심) · draft · research 를 한 번씩 돌렸을 때, When 차례별 codex 호출 인자를 보면, Then 판정 · 재심 차례(judge-* · review-*)는 `-s` 와 `sandbox_workspace_write` 가 0 개이고 `default_permissions="codex-audit-judge"` 가 1 개이며, 계약 작성 · 조사 차례(draft-* · research-*)는 `-s workspace-write` 를 그대로 쓴다 [exact, enumerated]
  측정: bash .harness/.meta/codex-judge-isolation/measure/measure.sh 스크립트-01
  음성 대조: BASE 판 스크립트로 같은 측정을 돌리면 판정 차례에 `-s workspace-write` 가 있어 FAIL 한다 (`measure.sh 스크립트-01 --base` 종료 1)
- [ ] 스크립트-02: Given 판정 차례에 감독이 쓴 `config.toml`(가짜 codex 가 기록한 것)을 그대로 쓴 `codex sandbox -P codex-audit-judge -C <판정 사본> --log-denials`, Then 8 칸이 이렇다 — 판정 사본 쓰기 됨 · 얼린 입력 읽기 됨 · `python3 -c 1` 종료 0 · `node -e 1` 종료 0 · 얼린 입력 쓰기 막힘 · `~/.ssh` 읽기 막힘 · `/private/tmp` 아래 미끼 파일 읽기 막힘 · 다른 감독 몫으로 만든 임시 폴더의 미끼 파일 읽기 막힘. 그리고 같은 설정의 `[permissions.codex-audit-judge.network]` 가 `enabled = false` 다 [exact, enumerated]
  측정: bash .harness/.meta/codex-judge-isolation/measure/measure.sh 스크립트-02
  양성 대조: 같은 8 칸을 `extends = ":workspace"` 만 둔 프로필로 돌리면 `~/.ssh` · `/private/tmp` 미끼 · 다른 감독 미끼 읽기 3 칸이 「됨」으로 바뀐다 — 측정이 막힘을 실제로 구분한다는 확인 (`measure.sh 스크립트-02 --positive`)
- [ ] 스크립트-03: Given premeasure 명령이 `$TMPDIR` 을 출력하는 픽스처로 impl(REJECT → 재심)을 돌렸을 때, Then 사전 측정 명령 · judge-1 · review-1 이 받은 `TMPDIR` · `TMP` · `TEMP` 가 셋 다 같은 값이고, 세 단계의 값이 서로 다르고, 셋 다 픽스처 TMPDIR 아래이되 픽스처 TMPDIR 자신이 아니다 [exact, enumerated]
  측정: bash .harness/.meta/codex-judge-isolation/measure/measure.sh 스크립트-03
  음성 대조: BASE 판은 환경 변수를 넘기지 않아 세 단계가 시스템 값을 그대로 받으므로 FAIL 한다 (`measure.sh 스크립트-03 --base` 종료 1)
- [ ] 스크립트-04: Given 네 경우 — (a) impl APPROVE (b) impl REJECT → 재심 (c) judge 차례 시간 초과(`CODEX_AUDIT_LIMIT=3`) (d) judge 차례 도중 감독 프로세스에 SIGTERM — 를 각자 빈 픽스처 TMPDIR 로 돌렸을 때, Then 감독이 끝난 뒤 픽스처 TMPDIR 안 항목 수가 네 경우 모두 0 이고, 가짜 codex 가 기록한 각 판정 · 재심 차례의 작업 폴더(판정 사본) 경로가 위치와 상관없이 더는 존재하지 않는다. 각 경우의 사전 측정 명령은 전용 TMPDIR 에 1MB 파일과 하위 폴더를 만들고 판정 사본 안에도 파일을 남긴다 [exact, enumerated]
  측정: bash .harness/.meta/codex-judge-isolation/measure/measure.sh 스크립트-04
  양성 대조: 같은 측정이 감독이 도는 중(judge 차례가 멈춰 있는 동안)에는 픽스처 TMPDIR 항목 수 1 이상을 낸다 — 0 이 「셀 대상이 없어서」가 아님을 확인한다
  음성 대조: 판정 사본을 남기는(`keep=True`) BASE 판으로 돌리면 (a) 가 FAIL 한다 (`measure.sh 스크립트-04 --base` 종료 1)
- [ ] 스크립트-05: Given premeasure 가 있는 계약(조건 2 개)으로 impl 을 돌렸을 때, Then judge-1 지시문에 (1) 사전 측정한 조건 번호 2 개가 모두 나오고 (2) 「사전 측정 기록이 있는 조건은 같은 명령을 다시 돌리지 않는다」 는 문장이 나오고 (3) 「격리 안에서 돌릴 수 있는 측정은 직접 돌린다」 가 0 번 나오고 (4) 판정이 읽을 수 있는 곳(얼린 입력 폴더 · 판정 사본)과 쓸 수 있는 곳(판정 사본 · 전용 임시 폴더)이 절대 경로로 나온다 [exact, enumerated]
  측정: bash .harness/.meta/codex-judge-isolation/measure/measure.sh 스크립트-05
  음성 대조: BASE 판(스크립트와 `premeasure.md` · `judge.md`)으로 돌리면 (2) · (3) 이 FAIL 한다 (`measure.sh 스크립트-05 --base` 종료 1)
- [ ] 스크립트-06: Given 가짜 codex 가 judge-1 에서 모델 `gpt-6.1-sol` · 입력 1,000,000 · 캐시 입력 900,000 · 출력 20,000 을 냈을 때, Then `report.md` 의 `## 비용` 절에 그 차례 줄과 합계 줄이 있고 두 줄 모두 `0.49` 달러를 적으며, 같은 감독의 `follow` 출력에도 judge-1 끝 줄에 `0.49` 가 나온다. 단가 표에 없는 모델 `fixture-unknown` 으로 돌리면 그 차례 줄에 `단가 모름` 과 토큰 수가 나오고 감독은 정상으로 끝난다 [exact]
  측정: bash .harness/.meta/codex-judge-isolation/measure/measure.sh 스크립트-06
  알려진 답: (1,000,000 − 900,000) × 2 / 1e6 + 900,000 × 0.10 / 1e6 + 20,000 × 10 / 1e6 = 0.20 + 0.09 + 0.20 = 0.49 (단가 2.00 / 0.10 / 10.00 은 `prices.json` 의 gpt-6.1-sol 값)
  음성 대조: 단가 표가 없는 BASE 판으로 돌리면 `## 비용` 절이 없어 FAIL 한다 (`measure.sh 스크립트-06 --base` 종료 1)
- [ ] 스크립트-07: Given 감독 차례가 끝날 때마다 `<감독용 Codex 폴더>/codex-audit-usage.jsonl` 에 한 줄(날짜 · 저장소 경로 · 계약 슬러그 · 단계 · 차례 · 모델 · 입력 · 캐시 · 출력 · 달러)이 붙고, When 두 저장소 A · B 로 오늘 날짜 줄 각각 0.49 · 0.25 달러, 지난달 날짜 줄 1.00 달러를 미리 넣은 기록에서 `codex-audit.sh usage` 를 돌리면, Then 오늘 합계 `0.74` · 이번 달 합계 `0.74` · 저장소 A `0.49` · 저장소 B `0.25` 가 나온다. impl 한 번(judge-1 하나)을 돌린 뒤 기록 줄은 정확히 1 줄 늘고 그 줄의 달러가 `0.49` 다 [exact, enumerated]
  측정: bash .harness/.meta/codex-judge-isolation/measure/measure.sh 스크립트-07
  알려진 답: 오늘 0.49 + 0.25 = 0.74, 지난달 줄 1.00 은 이번 달 합계에서 빠진다
- [ ] 스크립트-08: Given `codex_audit.daily_budget_usd: 0.50` 이고 사용 기록의 오늘 합계가 0.74 일 때, When draft 와 impl 을 각각 부르면, Then 둘 다 종료 코드 2 · `report.md` 갈래 `한도-예산` · 가짜 codex `exec` 호출 0 번이다. 오늘 합계가 0.30 이면 impl 이 정상으로 돌아 종료 코드 0 이다. 칸을 비우면 오늘 합계 100.00 에서도 정상으로 돈다 [exact, enumerated]
  측정: bash .harness/.meta/codex-judge-isolation/measure/measure.sh 스크립트-08
  음성 대조: 상한 확인이 없는 BASE 판으로 돌리면 첫 경우의 `exec` 호출이 1 이상이라 FAIL 한다 (`measure.sh 스크립트-08 --base` 종료 1)
- [ ] 스크립트-09: Given 가짜 codex 가 응답 없이 멈추는 차례로, When `CODEX_AUDIT_DRAFT_LIMIT=3`(계약 작성 · 수정 차례 상한 — draft 와 revise 가 함께 쓴다) 으로 draft 를, `CODEX_AUDIT_LIMIT=3` 으로 impl 을 부르면, Then 둘 다 가짜 codex `exec` 호출이 정확히 1 번이고 갈래 `시간-초과` · 종료 코드 2 다. 빈 응답 차례면 `exec` 호출이 2 번이다. `CODEX_AUDIT_DRAFT_LIMIT` 을 비우면 draft 차례 상한은 1500 초이고, `report.md` 의 draft-1 차례 줄에 `상한 1500초` 가 적힌다 [exact, enumerated]
  측정: bash .harness/.meta/codex-judge-isolation/measure/measure.sh 스크립트-09
  음성 대조: 시간 초과에서도 다시 시도하는 BASE 판으로 돌리면 `exec` 호출이 2 번이라 FAIL 한다 (`measure.sh 스크립트-09 --base` 종료 1)
- [ ] 스크립트-10: Given impl(REJECT → 재심) 한 번을 돌린 뒤, Then 감독 폴더 아래 보관된 세션 기록은 `.jsonl.gz` 뿐이고 `.jsonl` 은 0 개이며, 각 `.gz` 를 풀면 가짜 codex 가 쓴 첫 줄(`turn_context`)이 그대로 나온다 [exact]
  측정: bash .harness/.meta/codex-judge-isolation/measure/measure.sh 스크립트-10
- [ ] 스크립트-11: Given `CODEX_AUDIT_MODEL=gpt-6-luna` 로 impl 을 돌렸을 때, Then 모든 codex 호출 인자의 `-m` 값이 `gpt-6-luna` 이고 `report.md` 차례 줄의 모델도 `gpt-6-luna` 다. 변수를 비우면 `project.yaml` 의 `model` 값(픽스처 `fixture-supervisor`)을 쓴다 [exact]
  측정: bash .harness/.meta/codex-judge-isolation/measure/measure.sh 스크립트-11
- [ ] 스크립트-12: Given `.harness/project.yaml` 에 `codex_audit` 칸이 없을 때와 칸은 있으나 `mode` 줄이 없을 때, When draft · revise · impl 을 부르면, Then 여섯 경우 모두 출력에 `감독 판정: SKIPPED (codex_audit.mode: off)` 줄이 있고 종료 코드 3 이고 가짜 codex `exec` 호출 0 번이다. `mode: codex` 를 적으면 impl 이 돌아 `exec` 호출이 1 이상이다 [exact, enumerated]
  측정: bash .harness/.meta/codex-judge-isolation/measure/measure.sh 스크립트-12
  음성 대조: BASE 판 `codex-audit.sh` 로 돌리면 칸 없는 impl 이 Codex 를 불러 FAIL 한다 (`measure.sh 스크립트-12 --base` 종료 1)

## Error

- [ ] 오류-01: Given 가짜 codex 의 `sandbox --help` 출력에 `--permission-profile` 이 없을 때, When impl 을 부르면, Then 종료 코드 2 · 갈래 `설정-오류` · 실패 원인에 권한 프로필을 지원하지 않는다는 문장이 있고 judge 차례 `exec` 호출이 0 번이다 — 옛 `-s workspace-write` 방식으로 조용히 돌지 않는다 [exact]
  측정: bash .harness/.meta/codex-judge-isolation/measure/measure.sh 오류-01
- [ ] 오류-02: Given 사용 기록에 JSON 이 아닌 줄 1 개와 달러 칸이 문자열인 줄 1 개가 섞여 있을 때, When `usage` 와 `daily_budget_usd` 가 걸린 impl 을 부르면, Then 둘 다 traceback 없이 끝나고, 읽은 줄만으로 합계를 내며(스크립트-07 픽스처 기준 `0.74`), 출력에 `못 읽은 줄 2` 가 나온다 [exact]
  측정: bash .harness/.meta/codex-judge-isolation/measure/measure.sh 오류-02

## Skill

- [ ] 스킬-01: 다음 4 파일에 이번 동작이 낱말 그대로 적혀 있다 — `harness/README.md` (Codex 감독 설정 문단): `codex-audit-judge` · `daily_budget_usd` · `CODEX_AUDIT_DRAFT_LIMIT` · `CODEX_AUDIT_MODEL` · `usage` · `codex-audit-usage.jsonl` · `prices.json` · `.jsonl.gz`; `harness/skills/sprint-contract/SKILL.md` 와 `harness/agents/qa-evaluator.md`: 칸이 없으면 꺼짐(옛 문장 「칸이 없으면(기본값)」 0 번) · `daily_budget_usd`; `harness/templates/project.yaml`: `mode: off` 기본값과 `daily_budget_usd` 칸 [exact, enumerated]
  측정: bash .harness/.meta/codex-judge-isolation/measure/measure.sh 스킬-01

## Architecture

- [ ] 구조-01: Given 구현이 커밋된 뒤, When `git diff --name-only fc9ab639..$(git rev-parse --verify -q feat/codex-judge-isolation) -- . ':(exclude).harness'` 를 보면, Then 바뀐 경로가 `## 범위 경계` 의 sprint-scope 목록 중 `.harness/` 밖 8 개의 부분집합이고 `harness/scripts/codex-audit.sh` 를 포함한다. 상한 ref 해석 실패면 FAIL 이다 (`HEAD` 로 떨어지지 않는다) [exact, enumerated]
  측정: bash .harness/.meta/codex-judge-isolation/measure/measure.sh 구조-01
- [ ] 구조-02: 단가는 `harness/templates/codex-audit/prices.json` 한 곳에만 있다 — 그 파일에 확인일(`checked`) · 출처 주소(`source`) · 모델 6 개(`gpt-6.1-sol` · `gpt-6-sol` · `gpt-6-luna` · `gpt-5.6-sol` · `gpt-5.6-terra` · `gpt-5.6-luna`)의 입력 · 캐시 입력 · 출력 단가가 `## 배경` 의 단가 근거 값과 정확히 같고, `git diff -U0 fc9ab639..<가지 끝> -- harness/scripts/codex-audit.sh` 의 더한 줄(`+` 로 시작, `+++` 제외)에 그 단가 값과 같은 숫자 문자열이 0 개다 (BASE 에 이미 있는 대기 간격 `0.25` · `0.03` 은 더한 줄이 아니라 세지 않는다) [exact, enumerated]
  측정: bash .harness/.meta/codex-judge-isolation/measure/measure.sh 구조-02

## Anti-patterns

- [ ] 금지-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수
  측정: python3 scripts/validate-plugin.py harness --check=code-fence
- [ ] 금지-04: SKILL.md / agents/*.md frontmatter 에서 name 필드 누락 금지
  측정: python3 scripts/validate-plugin.py harness --check=frontmatter

## Reusability

- [ ] 재사용-01: 다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다 — 단가 계산 · 사용 기록 읽기는 `usage` · 상한 확인 · `## 비용` 이 같은 함수를 쓴다
  측정: bash .harness/.meta/codex-judge-isolation/measure/measure.sh 재사용-01
- [ ] 재사용-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다 — 임시 폴더는 기존 `scratch()` · `private_home()` 자리를 고쳐 쓰고, 정리는 기존 `cleanup()` 과 `ACTIVE` 목록을 쓴다
  측정: bash .harness/.meta/codex-judge-isolation/measure/measure.sh 재사용-02

## Diagnostics

- [ ] 진단-01: N/A (commands.analyze `bash -n scripts/release.sh` 는 이번 변경 파일을 재지 않는다 — 대신 `bash -n harness/scripts/codex-audit.sh` 종료 0 과 `python3 scripts/validate-plugin.py harness` FAIL 0 을 진단-04 측정에 묶는다)
- [ ] 진단-02: 변경한 마크다운 파일(`harness/README.md` · `harness/skills/sprint-contract/SKILL.md` · `harness/agents/qa-evaluator.md` · 이 계약)에서 BASE 대비 더한 줄(`git diff -U0` 의 `+` 줄 번호)에 걸린 markdownlint-cli2 0.23.2 경고(편집기와 같게 MD013 끔)가 0 개다
  측정: bash .harness/.meta/codex-judge-isolation/measure/measure.sh 진단-02
  양성 대조: MD013 을 켜고 파일 전체 줄을 세면 1 이상이 나온다 (`measure.sh 진단-02 --positive`, 봉인 전 실측 README 35 · SKILL 129 · qa-evaluator 218)
- [ ] 진단-03: N/A (commands.test `bash scripts/release.sh` 는 이번 변경과 무관 — 측정 묶음 전체 실행의 traceback 0 을 진단-04 에서 잰다)
- [ ] 진단-04: `bash -n harness/scripts/codex-audit.sh` 종료 0, `python3 scripts/validate-plugin.py harness` 종료 0, 측정 묶음 전체(`measure.sh all --skip 진단-04`, 상한 900 초) 종료 0 이고 출력에 `Traceback` 0 개, `.github/workflows/ci.yml` 의 한 줄 `run:` 명령 중 `python3 scripts/` · `bash harness/` · `bash flutter-toolkit/` 로 시작하는 것 전부(봉인 전 실측 34 개, BASE 에서 실패 0)를 W 에서 돌려 실패 0. Playwright 갈래는 이번 변경 파일이 `docs/` 를 건드리지 않아 돌리지 않는다
  측정: bash .harness/.meta/codex-judge-isolation/measure/measure.sh 진단-04

## 범위 경계

- 하지 않는 것: 계약 작성 · 조사 차례의 격리 방식 변경, 여러 모델 동시 판정과 FAIL 합집합 재심(모델 비교 뒤 결정), 모델 비교 실행(충전 필요 — 다음 단계), VS Code 상태 표시줄, 감독 모델 기본값 변경, 사용자 설정 파일(`~/.codex-qa/config.toml` · `~/.claude/settings.json`) 수정, harness 버전 올리기, 다른 저장소의 `project.yaml`(오늘 손으로 끈 46곳) 되돌리기.
- 다음 단계(이 계약 밖): 충전 뒤 6 모델(gpt-6.1-sol · gpt-6-sol · gpt-6-luna · gpt-5.6-sol · gpt-5.6-terra · gpt-5.6-luna) × 결함 판 7a5ac6e1 · 고친 판 829a3125 × 3 회 = 36 회 판정, 예상 약 17달러, `CODEX_AUDIT_MODEL` 로 모델을 바꿔 돈다.
- 단가는 Standard · 요청당 입력 272K 이하 기준이다. 감독은 차례 단위 합계만 받으므로 긴 문맥 할증은 반영하지 못한다 — 실제 청구가 더 클 수 있다는 점을 README 에 적는다.
- 커버리지 해소: 스크립트-02 · 스크립트-07 · 스킬-01 · 구조-01 · 구조-02 — 측정 줄은 `measure.sh <번호>` 한 명령이고, 산문의 열거 대상은 `measure.py` 의 같은 이름 함수(`script_02` · `script_07` · `skill_01` · `structure_01` · `structure_02`)가 같은 표기로 잰다(`SCOPE` · `MODELS` 상수, 낱말 목록, 알려진 답 수치). 검출기 출력 5 건(2026-10-07 봉인 전)은 이 위임 때문이다.
- `.harness/project.yaml` 은 이 저장소의 감독을 끈 상태(`mode: off`)로 커밋한다(사용자 지시 2026-10-07). `premeasure` 줄은 이 계약 측정 묶음으로 바꾼다.

```text
# sprint-scope
harness/scripts/codex-audit.sh
harness/templates/codex-audit/judge.md
harness/templates/codex-audit/premeasure.md
harness/templates/codex-audit/prices.json
harness/templates/project.yaml
harness/README.md
harness/skills/sprint-contract/SKILL.md
harness/agents/qa-evaluator.md
.harness/
```
