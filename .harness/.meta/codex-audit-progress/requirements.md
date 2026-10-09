# 요구사항 — Codex 감독 진행 상황 표시 (slug: codex-audit-progress)

작성: Claude (2026-10-06, 세션 fb4aefa8-0ee1-4711-9b22-7baf9c6b989f). 사용자와 합의한 내용을 옮긴 것이다. 계약서는 이 문서를 받은 Codex 가 쓴다.

## 1. 배경

harness 0.19.0 의 `harness/scripts/codex-audit.sh` 는 Codex 가 계약을 쓰고(draft · revise) 구현을 판정한다(impl). 감독 한 번에 몇 분이 걸린다(실측: 사전 측정 35 개 + 판정 1 차례 = 6 분 19 초). 그동안 사용자 화면에는 아무것도 보이지 않았다 — `wait` 는 끝날 때까지 `RUNNING` 만 찍고, 그 출력도 평가자 서브에이전트 안에서만 보였다. 사용자는 「내가 알려 달라 하는 게 아니라 항상 보이게」 를 요구했다.

## 2. 사용자 결정 (2026-10-06 대화)

1. 진행 상황을 사용자가 파일을 열어 보는 방식은 싫다. Claude 대화 화면에서 Bash 명령 출력처럼 계속 보이는 창으로 보인다 — VS Code 확장에서는 백그라운드 작업 카드(최신 출력이 갱신된다)다.
2. 감독(draft · revise · impl)이 시작되면 사용자가 요청하지 않아도 그 창이 **항상** 함께 뜬다.
3. 단계가 바뀌면 채팅에도 한 줄씩 옮긴다.
4. Codex 가 지금 무엇을 하는지 분석해 보여 준다 — 생각 중인지, 어떤 명령을 실행 중인지(명령 요약과 경과 시간), 답을 냈는지 아직인지, 오래 조용하면 멈춤 의심(얼마나 조용했는지), 다시 시도했는지.
5. Claude Code 상태줄은 VS Code 확장에 표시되지 않아(공식 문서 https://code.claude.com/docs/en/statusline · https://code.claude.com/docs/en/vs-code) 넣지 않는다. 플러그인은 상태줄을 제공할 수도 없다.
6. 줄 모양은 이런 식이다(사용자가 본 예시):

```text
[13:56:03] 감독 시작 · impl-r2 · 조건 35개
[13:56:10] 사전 측정 1/35 스킬-01 · 종료 0 (7초)
[14:00:41] 사전 측정 35/35 끝 (4분 31초)
[14:00:42] 판정 1차 시작 · gpt-6-astra · 생각 medium
[14:02:20] 판정 1차 끝 · APPROVE (PASS 35 · FAIL 0)
[14:02:22] 감독 판정: APPROVE · 총 6분 19초
```

7. **(2026-10-06 추가)** 새 GPT 모델이나 새 Codex 판이 나오면 사용자에게 보고한다. 감독 모델을 자동으로 바꾸지는 않는다 — 실측: 감독용 키 계정에 `gpt-6.1-sol` 이 새로 보였지만 등급이 `sol`(중간)이라 지금 감독 모델 `gpt-6-astra`(품질 우선)보다 나은지 알 수 없다. 바꿀지는 보고를 받은 사용자가 정한다.

## 3. 확인된 사실

- 백그라운드로 띄운 명령의 최신 출력은 VS Code 확장의 백그라운드 작업 카드에 보인다(공식 문서 https://code.claude.com/docs/en/vs-code). 상태줄은 이벤트가 있을 때만 갱신되고 VS Code 확장에는 안 나온다.
- 지금 `impl` 은 차례마다 `<감독 폴더>/<차례>/events.jsonl` 에 Codex `--json` 사건을 쓴다. 사건 종류: `thread.started` · `turn.started` · `item.started` · `item.updated` · `item.completed` · `turn.completed` · `turn.failed` · `error`. `item` 의 `type` 에는 `command_execution`(명령 실행, `command` 칸) · `reasoning` · `agent_message` 등이 있다. 추론 구간에서는 `item.started` 가 몇 분씩 안 오기도 한다 — 사건이 조용하다고 곧 죽은 것은 아니다(`~/.claude/codex-prompt-template.md`).
- 세션 기록 파일은 차례가 끝날 때 감독 폴더로 옮겨지므로, 진행 중에는 임시 Codex 폴더 아래에 있다.
- 사전 측정은 조건마다 순서대로 돈다(`premeasure/NN.json` 이 하나씩 생긴다).
- 평가자(`harness:qa-evaluator`)는 서브에이전트라 그 안의 Bash 출력은 부모 대화 화면의 작업 카드로 뜨지 않을 수 있다. 진행 창은 **부모 세션**이 띄우는 것이 확실하다.

## 4. 제안 설계 (바꿔도 되지만 바꾸면 계약 `## 배경` 에 이유를 적는다)

- 새 부속 명령 `codex-audit.sh follow <감독 폴더 | 계약 파일>`.
  - 감독 폴더면 그 감독을 따라간다. 계약 파일이면 그 계약의 가장 최근 감독 폴더를 따라가고, 아직 없거나 이미 끝난 것뿐이면 새 감독 폴더가 생길 때까지 기다린다(상한 있음).
  - 줄마다 `[HH:MM:SS]` 시각을 앞에 붙인다. 단계 줄: 감독 시작(종류 · 회차 · 조건 수) · 사전 측정 n/m(조건 · 종료 코드 · 걸린 초) · 사전 측정 끝 · 차례 시작(이름 · 모델 · 생각 강도) · 차례 끝(결과) · 다시 시도(사유) · 조사 · 재심 · 최종 판정(총 시간).
  - Codex 상태 줄: 진행 중인 차례의 `events.jsonl` 에서 새 사건이 오면 바뀐 상태만 찍는다 — 명령 실행 시작(명령 앞부분), 명령 끝(종료 코드 · 걸린 초), 생각 중, 답 작성, 답 받음. 같은 상태를 되풀이해 찍지 않는다.
  - 사건이 정한 초(기본 60) 넘게 없으면 「Codex 조용함 N초 — 생각 중이거나 멈춤 의심」 을 그 간격마다 한 번 찍는다. 세션 기록 파일이 자라고 있으면 「생각 중(기록은 자람)」 으로 구분한다.
  - 감독이 끝나면 마지막 줄 `감독 판정: <…>` 과 그 판정의 종료 코드(0 · 1 · 2 · 3)로 끝난다. 이미 끝난 감독이면 지난 단계를 다 찍고 같은 방식으로 끝난다.
  - 키 글자는 어떤 줄에도 나오지 않는다.
- `draft` · `revise` · `impl` 은 진행 중 단계를 감독 폴더 안 내부 기록에 남긴다(사용자가 여는 파일이 아니라 `follow` 가 읽는 것). `wait` 와 기존 동작 · 종료 코드는 그대로다.
- 새 모델 · 새 판 보고: 감독(draft · revise · impl)이 시작될 때 감독용 계정으로 쓸 수 있는 GPT 모델 목록과 Codex 최신 판(`npm view @openai/codex version`)을 확인해, 감독 폴더 밖 기억 파일(감독용 Codex 폴더 안)의 지난 목록과 다르면 `follow` 첫 줄 · `report.md` 에 「새 모델: … (지금 감독 모델 …)」 · 「새 Codex 판: … (설치 …)」 를 찍는다. 처음 한 번은 기억만 하고 알리지 않는다. 확인에 실패(인터넷 · 키 · 명령 없음)해도 감독을 막지 않고 「모델 확인 못 함: 사유」 한 줄만 남긴다. 모델 목록 확인은 키를 화면 · 파일 어디에도 남기지 않는다. 감독 없이 확인만 하는 부속 명령 `codex-audit.sh models` 도 둔다(새 것 · 지금 감독 모델 · 설치 판 · 최신 판을 찍는다).
- 문서:
  - `harness/skills/sprint-contract/SKILL.md` 와 `harness/agents/qa-evaluator.md` — 감독을 부른 쪽이 아니라 **부모 세션**이, 감독을 시작하면(직접 부르든 평가자를 띄우든) 같은 때 `follow <계약 파일>` 을 백그라운드 명령으로 띄우고, 단계 줄을 채팅에 옮긴다. 사용자가 요청하지 않아도 항상 한다.
  - `harness/README.md` 스크립트 표에 `follow` 를 더한다.

하지 않는 것: 상태줄 · 맥 알림 · 사용자 설정 파일(`~/.claude/settings.json`) 수정 · harness 버전 올리기 · 감독관 모델 자동 변경 · 감독관 모델 바꾸기(별도 리서치 중).

## 5. 이 레포 계약 규칙 (반드시 읽고 따른다)

- 형식 정의: `harness/references/contract-schema.md`. 작성 절차와 함정: `harness/skills/sprint-contract/SKILL.md`. 설정: `.harness/project.yaml`(카테고리 Skill/`스킬` · Script/`스크립트` · Error/`오류` · Architecture/`구조`, 금지 패턴 `금지-01`~`금지-04`).
- 최근 본보기: `.harness/sprint-contract-codex-supervisor.md` 와 그 개정 `.harness/sprint-amendments-codex-supervisor.md`, 측정 묶음 `.harness/.meta/codex-supervisor/measure/`(가짜 codex · 손 예제 재사용 가능).
- 측정은 판정 Codex 의 격리 공간 안에서도 돌 수 있게 한다(`rm -rf` 금지 · `ps` 에 기대지 않기). 못 도는 측정이 있으면 `.harness/project.yaml` 의 `codex_audit.premeasure` 로 격리 밖에서 돈다는 점을 적는다.
- 작업 폴더 W = `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/codex-audit-progress`, 가지 `feat/codex-audit-progress`, 시작 판 `BASE` = `c78b4f09` (harness 0.19.0). 커밋 구간 상한은 `git rev-parse --verify -q feat/codex-audit-progress`.
- 이 계약은 `codex-audit.sh draft` 로 쓴다(이 기능을 만든 스프린트 다음 첫 실사용).
