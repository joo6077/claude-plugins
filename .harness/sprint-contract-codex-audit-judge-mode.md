---
feature: "Codex 감독 판정 전용 모드 (mode: judge)"
slug: codex-audit-judge-mode
created: "2026-10-07 17:56"
complexity: "중간"
conditions: 13
status: active
owner_session: 35b5945f-4957-4359-9b18-2d22b3bafeb0
conditions_digest: sha256:450d67ea16afb873
measurement_digest: sha256:d57469dca4dbefa5
locked_at: "2026-10-07 18:02"
---

# Codex 감독 판정 전용 모드 (mode: judge)

## 배경

- 사용자 결정(2026-10-07): 감독 기본 모델을 gpt-6-luna 로 바꿨다(`~/.codex-qa/config.toml`). 계약 작성은 측정 묶음까지 짜고 돌리는 일이라 작은 모델에 맡기기 어렵고, 계약 작성 차례가 판정보다 많고 오래 걸린다(10-06~07 계약 작성 62 · 판정 37). 그래서 「계약은 Claude 가 쓰고, 구현 판정만 Codex 가 한다」 는 `codex_audit.mode: judge` 를 더한다. 사용자 답 「ㄱㄱ」.
- 하루 평균 계약 19 개(최대 31, 2026-09-23~10-07 실측). judge 모드 + luna 판정이면 하루 약 4달러로 본다.
- 이 계약은 감독이 꺼진 상태(`mode: off`)로 Claude 가 쓰고 Claude qa-evaluator 가 판정한다. 진짜 Codex 호출은 0 번 — 측정은 앞 스프린트 측정 묶음의 가짜 codex(`.harness/.meta/codex-judge-isolation/measure/fake.py`)를 쓴다.
- W = `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/codex-judge-isolation`, 가지 `feat/codex-audit-judge-mode`(앞 스프린트 가지 `feat/codex-judge-isolation` 끝 `889b2a23` 위), BASE = `889b2a23`.
- 측정 묶음 = `bash .harness/.meta/codex-audit-judge-mode/measure/measure.sh <조건 번호>`. 가지 끝 커밋(`--base` 면 BASE)의 `harness/` 를 임시 폴더로 꺼내 가짜 codex 로 감독을 끝까지 돌리고, 끝나면 자기 임시 폴더를 지운다. 종료 코드 0 = PASS, 1 = FAIL.

## Script

- [ ] 스크립트-01: Given `codex_audit` 에 `mode: judge` 와 감독 폴더가 적힌 픽스처, When draft 와 revise 를 부르면, Then 둘 다 종료 코드 3 이고 출력에 `감독 판정: SKIPPED (codex_audit.mode: judge — 계약은 Claude 가 쓴다)` 줄이 있고 가짜 codex `exec` 호출이 0 번이다 [exact, enumerated]
  측정: bash .harness/.meta/codex-audit-judge-mode/measure/measure.sh 스크립트-01
  음성 대조: BASE 판으로 돌리면 `judge` 를 모르는 값으로 보고 BLOCKED(종료 2)라 FAIL 한다 (`measure.sh 스크립트-01 --base` 종료 1)
- [ ] 스크립트-02: Given 같은 `mode: judge` 픽스처와 APPROVE 를 내는 가짜 codex, When impl 을 부르면, Then 종료 코드 0 이고 `report.md` 끝 줄이 `감독 판정: APPROVE` 이며, judge-1 차례의 codex 호출 인자에 `default_permissions="codex-audit-judge"` 가 있다 [exact]
  측정: bash .harness/.meta/codex-audit-judge-mode/measure/measure.sh 스크립트-02
  음성 대조: BASE 판으로 돌리면 BLOCKED(종료 2) · `exec` 0 번이라 FAIL 한다 (`measure.sh 스크립트-02 --base` 종료 1)
- [ ] 스크립트-03: Given 다른 값의 픽스처, Then 기존 동작이 그대로다 — (a) `mode: codex` 의 draft 는 `exec` 1 번 · 종료 0 (b) `mode: off` 의 impl 은 종료 3 · `감독 판정: SKIPPED (codex_audit.mode: off)` · `exec` 0 번 (c) 칸이 없을 때 impl 도 (b) 와 같다 (d) `mode: banana` 의 impl 은 종료 2 · `report.md` 갈래 `설정-오류` · 실패 원인에 `codex · judge · off` 가 나온다 [exact, enumerated]
  측정: bash .harness/.meta/codex-audit-judge-mode/measure/measure.sh 스크립트-03
  음성 대조: BASE 판으로 돌리면 (d) 의 실패 원인에 `judge` 가 없어 FAIL 한다 (`measure.sh 스크립트-03 --base` 종료 1)

## Skill

- [ ] 스킬-01: 다음 4 파일이 `judge` 모드를 낱말 그대로 적는다 — `harness/skills/sprint-contract/SKILL.md`: `mode: judge` 줄과 그 모드에서 계약은 `mode: off` 절차로 Claude 가 쓴다는 문장; `harness/agents/qa-evaluator.md`: `mode: judge` 에서 계약 검토는 직접 하고 구현 판정은 `codex` 모드와 같은 절차(`impl --detach`)라는 문장; `harness/templates/project.yaml`: `codex | judge | off`; `harness/README.md` Codex 감독 설정 문단: `judge` [exact, enumerated]
  측정: bash .harness/.meta/codex-audit-judge-mode/measure/measure.sh 스킬-01

## Architecture

- [ ] 구조-01: Given 구현이 커밋된 뒤, When `git diff --name-only 889b2a23..$(git rev-parse --verify -q feat/codex-audit-judge-mode) -- . ':(exclude).harness'` 를 보면, Then 바뀐 경로가 `## 범위 경계` 의 sprint-scope 목록 중 `.harness/` 밖 5 개의 부분집합이고 `harness/scripts/codex-audit.sh` 를 포함한다. 상한 ref 해석 실패면 FAIL [exact, enumerated]
  측정: bash .harness/.meta/codex-audit-judge-mode/measure/measure.sh 구조-01

## Anti-patterns

- [ ] 금지-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수
  측정: python3 scripts/validate-plugin.py harness --check=code-fence
- [ ] 금지-04: SKILL.md / agents/*.md frontmatter 에서 name 필드 누락 금지
  측정: python3 scripts/validate-plugin.py harness --check=frontmatter

## Reusability

- [ ] 재사용-01: N/A (새 함수 · 모듈을 만들지 않는다 — 기존 mode 분기 두 자리에 값 하나를 더한다)
- [ ] 재사용-02: N/A (같은 이유 — 기존 `prepare` · `main` 의 mode 확인을 그대로 고쳐 쓴다)

## Diagnostics

- [ ] 진단-01: N/A (commands.analyze `bash -n scripts/release.sh` 는 이번 변경 파일을 재지 않는다 — 진단-04 가 `bash -n harness/scripts/codex-audit.sh` 를 잰다)
- [ ] 진단-02: 변경한 마크다운 파일(`harness/README.md` · `harness/skills/sprint-contract/SKILL.md` · `harness/agents/qa-evaluator.md` · 이 계약)에서 BASE 대비 더한 줄에 걸린 markdownlint-cli2 0.23.2 경고(MD013 끔)가 0 개다
  측정: bash .harness/.meta/codex-audit-judge-mode/measure/measure.sh 진단-02
  양성 대조: MD013 을 켜고 파일 전체 줄을 세면 1 이상이 나온다 (`measure.sh 진단-02 --positive`)
- [ ] 진단-03: N/A (commands.test `bash scripts/release.sh` 는 이번 변경과 무관 — 진단-04 가 측정 묶음 전체를 잰다)
- [ ] 진단-04: `bash -n harness/scripts/codex-audit.sh` 종료 0, `python3 scripts/validate-plugin.py harness` 종료 0, 측정 묶음 전체(`measure.sh all --skip 진단-04`) 종료 0 · `Traceback` 0 개, `.github/workflows/ci.yml` 의 한 줄 `run:` 명령 중 `python3 scripts/` · `bash harness/` · `bash flutter-toolkit/` 로 시작하는 것 전부(봉인 전 실측 34 개)를 W 에서 돌려 실패 0
  측정: bash .harness/.meta/codex-audit-judge-mode/measure/measure.sh 진단-04

## 범위 경계

- 하지 않는 것: 모델 기본값 바꾸기(이미 사용자 설정 파일에서 바꿨다 — 이 계약은 그 파일을 건드리지 않는다), 다른 저장소의 `mode: off` 되돌리기, 모델 비교 실행, harness 버전 올리기.
- 커버리지 해소: 스킬-01 · 구조-01 — 측정 줄은 `measure.sh <번호>` 한 명령이고 열거 대상은 `measure.py` 의 `skill_01` · `structure_01`(`SCOPE` 상수)이 같은 표기로 잰다.
- `judge` 모드에서 draft · revise 를 부르면 SKIPPED(종료 3)로 끝난다 — 부른 쪽은 `mode: off` 와 같이 Claude 절차로 계약을 쓴다는 신호로 읽는다.

```text
# sprint-scope
harness/scripts/codex-audit.sh
harness/templates/project.yaml
harness/README.md
harness/skills/sprint-contract/SKILL.md
harness/agents/qa-evaluator.md
.harness/
```
