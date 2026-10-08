---
feature: "Codex 감독 판정 막힘 미리 알리기 · 되돌려 쓰기 신호 빈틈"
slug: codex-audit-judge-guard
created: "2026-10-08 17:28"
complexity: "중간"
conditions: 14
status: active
owner_session: 35b5945f-4957-4359-9b18-2d22b3bafeb0
conditions_digest: sha256:02010867cef5ed26
measurement_digest: sha256:bbd23664ffb0e27b
locked_at: "2026-10-08 17:38"
---

# Codex 감독 판정 막힘 미리 알리기 · 되돌려 쓰기 신호 빈틈

## 배경

- 사용자 결정(2026-10-08): Codex 는 판정과 판정 중 조사만 맡고(gpt-6.1-sol), 계약은 Claude 가 쓴다(`mode: judge`). 구독 실측에서 sol 은 결함 판 3 회 중 2 회 실제 결함을 잡았고 luna 는 9 회 모두 놓쳤다. 계약 작성까지 sol 이면 주간 한도를 넘는다(하루 계약 19 개 기준 약 240 %). 사용자 답: 「그 밖에 확인할거 고치고」 · 「그럼 판정만 그리고 리서치랑」.
- 고칠 것 1 — 판정할 저장소가 `/tmp` 아래면 판정 격리(`":slash_tmp" = "deny"`)가 얼린 입력 읽기를 막는다. 2026-10-08 실측: `/private/tmp` 아래 시험 작업 폴더에서 sol 판정 3 개가 입력을 못 읽고 RESEARCH 를 두 번 낸 뒤 BLOCKED(형식-깨짐)로 끝났다 — 구독 사용량만 썼다. impl 감독은 Codex 를 부르기 전에 이것을 알아채고 `설정-오류` 로 끝내야 한다. draft · revise 는 판정 격리를 쓰지 않으니 막지 않는다.
- 고칠 것 2 — 앞 계약 `codex-audit-auth-writeback` 교차 진단이 재현한 빈틈: `write_back` 의 `signal.pthread_sigmask` 는 부른 스레드만 막는다. 출력을 복사하는 스레드가 살아 있으면 운영체제가 신호를 그 스레드로 주고, 파이썬 처리기는 메인 스레드에서 돌아 되돌려 쓰는 도중 `Interrupted` 가 터진다. 갱신이 버려진다. 고치는 방법: 쓰는 동안 신호 처리기를 「받은 신호를 적어 두기만 하는 함수」로 바꿔 끼우고, 끝나면 원래 처리기로 돌려놓은 뒤 적어 둔 신호를 다시 낸다. 파이썬 처리기는 늘 메인 스레드에서 도니 스레드 수와 상관없다. `os.replace` 가 실패하면 임시 파일을 지운다.
- 고칠 것 3 — 앞 계약 QA 제안: 되돌려 쓴 `auth.json` 과 잠금 파일 권한 600, 쓰다 만 `.codex-audit-auth-*` 0 개를 조건으로 잰다.
- 이 계약은 감독이 꺼진 상태로 Claude 가 쓰고 Claude qa-evaluator 가 판정한다. 진짜 Codex 모델 호출은 0 번 — 측정은 가짜 codex 로 한다.
- W = `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/codex-judge-isolation`, 가지 `feat/codex-audit-judge-mode`, BASE = `452ca7b8`. 측정 묶음 = `bash .harness/.meta/codex-audit-judge-guard/measure/measure.sh <조건 번호>`(가지 끝, `--base` 면 BASE 의 `harness/` 로 가짜 codex 감독을 끝까지 돌리고, 자기 임시 폴더 · `/tmp` 아래 픽스처 · 기록된 가짜 프로세스를 끝에서 지운다). 가짜 codex 의 `hold-late-orphan` 단계는 풀린 뒤 로그인을 갱신하고, 표준 출력을 쥔 손자 프로세스(`sleep 30`, 따로 띄운 세션)를 남긴 채 끝난다 — 감독의 출력 복사 스레드가 살아 있는 채 되돌려 쓰기에 들어간다.
- 봉인 전 실측(BASE 판 = 지금 판, 2026-10-08 17:40 · 교차 진단 반영 뒤 17:55 다시): 스크립트-01 FAIL(`/tmp 아래 impl 종료 0`), 스크립트-02 FAIL 5 회 연속(`(a) 토큰 original`), 스크립트-03 · 04 PASS(지켜야 할 기존 동작), 스킬-01 · 구조-01 · 재사용-01 FAIL. 끝난 뒤 남은 가짜 프로세스 · `/tmp/cag-*` 0 개.

## Script

- [ ] 스크립트-01: Given 구독 모양 감독 폴더와 `/tmp` 아래 저장소 · `/private/tmp` 아래 저장소 두 경우(둘 다 픽스처 `TMPDIR` 은 `/tmp` 밖), When impl 을 돌리면, Then 둘 다 종료 2 · `report.md` 갈래 `설정-오류` · `## 실패 원인` 에 `/tmp` 가 있고 exec 호출 0 번 · 로그인 확인 호출 0 번이며 픽스처 `TMPDIR` 항목 수가 0 이다. 같은 두 경우에 draft 는 exec 1 번이고 출력에 `설정-오류` 가 없다. `/tmp` 밖 저장소의 impl 은 종료 0 · exec 1 번이고, 저장소는 `/tmp` 밖이고 픽스처 `TMPDIR` 만 `/tmp` 아래인 impl 도 종료 0 · exec 1 번이다 [exact, enumerated]
  측정: bash .harness/.meta/codex-audit-judge-guard/measure/measure.sh 스크립트-01
  음성 대조: BASE 판은 `/tmp` 아래 impl 을 그대로 돌려 종료 0 이라 FAIL 한다 (`measure.sh 스크립트-01 --base` 종료 1)
- [ ] 스크립트-02: Given 구독 모양 감독 폴더와 `hold-late-orphan` 차례(출력 복사 스레드가 살아 있는 채 되돌려 쓰기에 들어감), When 측정이 `codex-audit-auth.lock` 에 `flock(LOCK_EX)` 를 잡은 채 차례를 풀고, 감독이 그 잠금 파일을 연 것이 `lsof -p <감독 pid>` 에 보이면(그때 토큰은 `original`) 0.5 초 뒤 신호를 보내고 — (a) SIGTERM 을 보내고 1 초 뒤 잠금을 놓는다 (b) SIGINT 를 보내고 13 초 뒤 잠금을 놓는다(되돌려 쓰기가 10 초 안에 잠금을 못 잡아 포기하는 길) — Then (a) 토큰이 그 차례가 만든 값 · 감독 종료 코드 143 (b) 토큰 `original` · 종료 코드 130 이고, 두 경우 모두 `report.md` 갈래 `중단됨` · 감독 출력에 `Traceback` 0 개 · 감독 폴더 새 항목이 `codex-audit-usage.jsonl` · `codex-audit-models.json` · `codex-audit-auth.lock` 밖에 0 개 · 픽스처 `TMPDIR` 항목 수 0 이다 [exact, enumerated]
  측정: bash .harness/.meta/codex-audit-judge-guard/measure/measure.sh 스크립트-02
  음성 대조: BASE 판은 신호가 미루기를 뚫어 토큰이 `original` 로 남아 FAIL 한다 (`measure.sh 스크립트-02 --base` 를 3 번 돌려 3 번 모두 종료 1)
- [ ] 스크립트-03: Given 구독 모양 감독 폴더의 `auth.json` 권한이 644 일 때, When impl 이 로그인 갱신을 되돌려 쓰면, Then 감독 폴더 `auth.json` 의 토큰이 그 차례가 만든 값이고 `auth.json` · `codex-audit-auth.lock` 권한이 둘 다 600 이며, 감독 폴더에 `.codex-audit-auth-` 로 시작하는 항목이 0 개다 [exact, enumerated]
  측정: bash .harness/.meta/codex-audit-judge-guard/measure/measure.sh 스크립트-03
- [ ] 스크립트-04: Then 앞 측정 묶음 세 가지 — `bash .harness/.meta/codex-audit-auth-writeback/measure/measure.sh all --skip 진단-04` · `bash .harness/.meta/codex-audit-subscription/measure/measure.sh 스크립트-05` · `… 스크립트-06` — 이 가지 끝에서 모두 종료 0 이고 출력에 `Traceback` 이 없다 [exact, enumerated]
  측정: bash .harness/.meta/codex-audit-judge-guard/measure/measure.sh 스크립트-04

## Skill

- [ ] 스킬-01: `harness/README.md` 의 Codex 감독 설정 문단에 `` `/tmp` 아래 `` 가 있다(판정할 저장소가 `/tmp` 아래면 impl 이 설정-오류로 끝난다는 안내) [exact]
  측정: bash .harness/.meta/codex-audit-judge-guard/measure/measure.sh 스킬-01

## Architecture

- [ ] 구조-01: Given 구현이 커밋된 뒤, When `git diff --name-only 452ca7b8..$(git rev-parse --verify -q feat/codex-audit-judge-mode) -- . ':(exclude).harness'` 를 보면, Then 바뀐 경로가 `## 범위 경계` sprint-scope 목록 중 `.harness/` 밖 2 개의 부분집합이고 `harness/scripts/codex-audit.sh` 를 포함한다. 상한 ref 해석 실패면 FAIL [exact, enumerated]
  측정: bash .harness/.meta/codex-audit-judge-guard/measure/measure.sh 구조-01

## Anti-patterns

- [ ] 금지-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수
  측정: python3 scripts/validate-plugin.py harness --check=code-fence
- [ ] 금지-04: SKILL.md / agents/*.md frontmatter 에서 name 필드 누락 금지
  측정: python3 scripts/validate-plugin.py harness --check=frontmatter

## Reusability

- [ ] 재사용-01: 가지 끝 `codex-audit.sh` 에 `pthread_sigmask` 가 0 곳이고 `def write_back(` 가 1 개다(되돌려 쓰기는 한 함수에서만 한다)
  측정: bash .harness/.meta/codex-audit-judge-guard/measure/measure.sh 재사용-01
- [ ] 재사용-02: N/A (새 공용 모듈을 만들지 않는다 — 기존 `write_back` · `impl` 을 고쳐 쓴다)

## Diagnostics

- [ ] 진단-01: N/A (commands.analyze `bash -n scripts/release.sh` 는 이번 변경 파일을 재지 않는다 — 진단-04 가 `bash -n harness/scripts/codex-audit.sh` 를 잰다)
- [ ] 진단-02: 변경한 마크다운 파일(`harness/README.md` · 이 계약) 두 개를 모두 가지 끝에서 읽었고(못 읽은 파일이 있으면 FAIL), BASE 대비 더한 줄에 걸린 markdownlint-cli2 0.23.2 경고(MD013 끔)가 0 개다
  측정: bash .harness/.meta/codex-audit-judge-guard/measure/measure.sh 진단-02
  양성 대조: MD013 을 켜고 파일 전체 줄을 세면 1 이상이 나온다 (`measure.sh 진단-02 --positive`)
- [ ] 진단-03: N/A (commands.test `bash scripts/release.sh` 는 이번 변경과 무관 — 진단-04 가 측정 묶음 전체를 잰다)
- [ ] 진단-04: `bash -n harness/scripts/codex-audit.sh` 종료 0, `python3 scripts/validate-plugin.py harness` 종료 0, 측정 묶음 전체(`measure.sh all --skip 진단-04`) 종료 0 · `Traceback` 0 개, `.github/workflows/ci.yml` 의 한 줄 `run:` 명령 중 `python3 scripts/` · `bash harness/` · `bash flutter-toolkit/` 로 시작하는 것 전부(0 개면 FAIL)를 W 에서 돌려 실패 0
  측정: bash .harness/.meta/codex-audit-judge-guard/measure/measure.sh 진단-04

## 범위 경계

- 하지 않는 것: 감독 폴더 `config.toml` 의 모델 바꾸기(사용자 설정 — 이 계약 밖에서 백업 뒤 바꾼다), 다른 저장소 `mode` 켜기, 구독 사용량 비율 상한 기능, harness 버전 올리기.
- `/tmp` 판정은 그 감독의 기록 폴더(저장소 `.harness/codex-audit/…`, 판정 입력이 얼려지는 자리)의 실제 경로가 `/tmp` 또는 그것의 실제 경로(`/private/tmp`) 아래인지로 한다. `TMPDIR`(`/var/folders/…`)는 해당하지 않는다 — 판정 격리는 그 차례 전용 임시 폴더만 쓰기로 연다.
- 측정은 맥(`TMPDIR` = `/var/folders/…`) 기준이다. `TMPDIR` 이 `/tmp` 인 환경(리눅스 기본)은 판정 사본이 `/tmp` 아래 생겨 판정 격리와 부딪힐 수 있으나 재지 않았다. 앞 측정 묶음들도 맥에서만 돈다.
- 신호를 미루는 동안(잠금 대기 최대 10 초) 중단이 늦게 먹는다 — 갱신을 버리지 않으려고 고른 것이다. 신호로 멈춘 차례의 세션 기록은 차례 폴더로 옮기지 않는다(맨 끝 정리가 지운다). 미루는 신호는 SIGINT · SIGTERM · SIGHUP 셋이고 측정은 SIGTERM · SIGINT 를 잰다 — SIGHUP 은 코드 검토로 본다.
- `/tmp` 검사는 impl 의 로그인 확인보다 먼저 하고, 실패 원인에 실제 경로와 「저장소를 `/tmp` 밖으로 옮긴다」 를 적는다. 경로 비교는 `Path.is_relative_to` 로 한다(`/tmpx` 오판 방지 — 코드 검토). README 안내는 기존 Codex 감독 설정 문단 안에 덧붙인다(앞 측정 묶음 스킬-01 이 같은 문단을 읽는다).
- `copier.join(5)` 는 바꾸지 않는다 — 스크립트-02 가 출력 복사 스레드가 살아 있는 채 되돌려 쓰기에 들어가는 것을 이 값에 기대어 재현한다.
- `os.replace` 실패 때 임시 파일 지우기는 실패를 흉내 낼 방법이 마땅치 않아 조건으로 두지 않는다 — 코드 검토로 본다.
- 커버리지 해소: 스크립트-01 · 02 · 03 · 04 · 구조-01 — 측정 줄은 `measure.sh <번호>` 한 명령이고 열거 대상은 `measure.py` 의 같은 이름 함수(`ALLOWED_NEW` · `PREVIOUS` · `SCOPE` 상수)가 같은 표기로 잰다.

```text
# sprint-scope
harness/scripts/codex-audit.sh
harness/README.md
.harness/
```
