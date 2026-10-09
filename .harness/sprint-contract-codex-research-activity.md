---
feature: "리서치 진행을 채팅에 — Codex 가 그사이 한 말 · 검색 · 열람 · 명령을 30초마다"
slug: codex-research-activity
created: "2026-10-09 16:39"
complexity: "복잡"
conditions: 21
status: done
owner_session: 35b5945f-4957-4359-9b18-2d22b3bafeb0
conditions_digest: sha256:a548e37706b97536
measurement_digest: sha256:7dcf48c2e361a3ac
locked_at: "2026-10-09 17:37"
---

## 배경

- 사용자 요구(2026-10-09): 리서치 진행을 열어 보지 않아도 채팅에서 보고 싶다. 30초마다, 「어떤 리서치를 하는지, 어디를 조사하는지」 를 Codex 채팅 창에서 보이는 과정처럼. 상태 표시줄 · 옆 막대 목록 · `/tasks` 작업 카드는 모두 열어야 보이거나 별로라서 버렸다(옆 막대 판 0.3.0 은 병합 없이 지움).
- 방식(사용자 선택 「채팅에 진행 메시지」): 리서치 래퍼 `~/.claude/bin/codex-research` 를 Monitor 도구로 띄우면 표준 출력 줄이 그 세션 채팅에 알림으로 온다(시험 2026-10-09 16:3x — 10초 간격 다섯 줄이 채팅에 옮겨짐). 래퍼는 최종 답을 표준 출력, 진행 줄을 표준 오류로 내므로 Monitor 에는 `2>&1 >/dev/null` 로 표준 오류만 넘긴다.
- 재료: Codex 세션 기록(`rollout-*.jsonl`)에 실제로 남는 것(2026-10-09 16:07 실제 리서치 기록 실측) — 중간 말(`message` · `phase: commentary`), 검색어(`custom_tool_call` `exec` 입력의 `web__run({search_query:[{q:"…"}]})`), 연 주소(같은 꼴의 `open:[{ref_id:"…"}]`), 셸 명령(`custom_tool_call` `exec` 입력의 `tools.exec_command({cmd:"…", workdir:…})` — 이번 달 364 건, `function_call` 은 `wait` 3 건뿐). 생각 요약(`reasoning.summary`)은 비어 있고 내용은 암호화돼 있어 쓰지 않는다. 최종 답(`phase: final_answer`)은 진행 줄로 내지 않는다.
- 열람은 사용자에게 뜻이 있는 주소(`http` · `https` 로 시작)만 보인다. 실제 기록에 많은 `turn0search0` · `turn1view2` 같은 내부 번호는 보이지 않는다. 셸 명령이 변수 약식(`{cmd,workdir:…}`)이면 글자가 없어 건너뛴다.
- 줄 모양: 30초마다 머리 줄 `리서치 · <Goal 주제> · 시도 n/N · 경과 · 사용량` 아래에, 그사이 새로 생긴 것만 `  말: …` · `  검색: …` · `  열람: …` · `  명령: …` 줄로 붙인다. 한 줄은 200자 이하로 자르고 줄바꿈은 한 칸으로 합친다. 한 번에 내는 활동은 6 줄까지, 나머지는 `  …그 밖에 N개` 한 줄로 묶는다(Monitor 는 줄이 너무 많으면 저절로 멈춘다). 주기가 오기 전에 시도가 끝나도(성공 · 실패 모두) 끝내기 직전에 남은 활동을 한 번 더 낸다 — 30초 안에 끝나는 작은 리서치도 활동이 보이게.
- 래퍼는 차례마다 자기 세션 기록 경로를 이미 안다(`rollout_of`). 다른 세션 기록은 읽지 않는다.
- 측정 묶음 `.harness/.meta/codex-research-activity/measure/`(`check.py` · `fake/codex`): 가짜 codex 가 실제 기록과 같은 모양의 줄(사건은 빈칸 없는 JSON, 검색 · 열람 · 셸 명령은 `exec` 입력 꼴)을 4초 간격으로 쓰고, 래퍼를 `CODEX_PROGRESS_SECONDS=2` · `CODEX_TRIES=2` 로 돌린다(`flush` 만 주기 100초 · 간격 1초). 가짜 시나리오: `ok` · `fail-then-ok` · `corrupt` · `partial` · `burst`. 실제 `~/.codex/sessions` · `~/.codex-status` 는 건드리지 않는다. `--base` 는 고치기 전 백업 `~/.claude/bin/codex-research.bak-20261009c` · `~/.claude/CLAUDE.md.bak-20261009c` · `~/.claude/codex-prompt-template.md.bak-20261009c` 를 잰다. 봉인 전 `--base` 실측(2026-10-09, 교차 진단 반영 뒤): `activity` · `forms` · `once` · `length` · `burst` · `retry` · `flush` · `partial` · `corrupt` · `monitor` · `docs` · `reuse` 12 개는 종료 코드 1, `answer` 는 0(지켜야 할 기존 동작). 가짜 사건 줄을 래퍼의 식별자 읽기(`thread_id_of` 의 sed)에 넣으면 식별자가 나온다(실측 `abc-123`).
- 기존 셸 검사: `shellcheck -S warning ~/.claude/bin/codex-research.bak-20261009c` 경고 0 줄(16:39 실측).

### 복잡도 표

| 축 | 물음 | 값 |
| -- | ---- | -- |
| 레이어 수 | 몇 개 계층을 관통하는가 | 2 — 래퍼 실행 · 전역 규칙 문서 |
| 공개 API·계약 변경 | 바깥에서 보는 모양이 바뀌는가 | 예 — 래퍼 표준 오류 줄 모양 · 부르는 법(Monitor) |
| 소비면 존재 | 받아 쓰는 반대편이 있는가 | 예 — 부르는 쪽은 전역 규칙 · 위임 템플릿을 읽는 Claude 세션 |
| 회귀 위험 | 기존 동작이 깨질 경로가 있는가 | 예 — 최종 답 통로 · 재시도 · 종료 코드 |

3 축이 「예」 이고 공개 모양 변경 + 소비면이 함께라 복잡 — 소비면 조건 구조-01 을 따로 둔다. 기능 조건 13 개(복잡 기준 9~20).

## 범위 경계

```text
# sprint-scope
.harness/sprint-contract-codex-research-activity.md
.harness/sprint-feedback-codex-research-activity.md
.harness/sprint-amendments-codex-research-activity.md
.harness/.meta/codex-research-activity/
```

- 레포 밖에서 고치는 것(위 목록은 레포 안만 막는다): `~/.claude/bin/codex-research` · `~/.claude/CLAUDE.md` 의 리서치 호출 문장 1 줄 · `~/.claude/codex-prompt-template.md` 의 리서치 호출 문장 1 줄 · 메모 `feedback_codex_foreground_call_direct.md` 와 그 목차 줄.
- 하지 않는 것: 감독(`codex-audit.sh`) 쪽 진행 표시(이미 `follow --relay` 가 있다), 생각 요약 켜기(`model_reasoning_summary`), 상태 폴더 쓰기 제거, main 에 남은 VS Code 확장 코드 정리(끝나고 사용자에게 따로 묻는다).
- 오라클 해소: 구조-02 — 메모 글 자체가 산출물이라 글 확인이 곧 판정이다.
- 오라클 해소: 진단-04 — 진짜 Codex 실행에서 Monitor 가 받은 줄을 잰다(글 존재가 아니라 실행 출력).
- 「최종 답」 은 가짜 codex 가 `-o` 와 기록의 `final_answer` 에 쓰는 글자 `QQZ` 로 잰다.

## Skill

- [ ] 스킬-00: N/A (스킬 파일을 바꾸지 않는다 — 범위 목록에 `SKILL.md` 0 개)

## Script

- [ ] 스크립트-01: Given 가짜 codex 가 말 · 검색어 · 주소 열람 · 셸 명령을 시간차를 두고 기록에 쓸 때, When 래퍼를 돌리면, Then 표준 오류에 `  말: ` 줄(`공식 문서부터 확인하겠습니다.`) · `  검색: ` 줄(`alpha query one` · `beta query two`) · `  열람: ` 줄(`https://example.com/doc`) · `  명령: ` 줄(`gh api repos/x/y/releases`)이 각각 그 접두로 시작해 나오고, 머리 줄 `리서치 · 가짜 리서치 시험` 이 2 번 이상, 종료 코드는 0 이다 [exact, enumerated]
  - 측정: `python3 .harness/.meta/codex-research-activity/measure/check.py activity` 종료 코드 0 이고 출력에 `FAIL` 0 줄
  - 음성 대조: `--base` 는 종료 코드 1(실측 — 다섯 항목 FAIL). 기록 읽기를 빼면 다섯 항목이 FAIL 한다
- [ ] 스크립트-02: 실제 기록 꼴 — 따옴표 붙은 `"q"` 검색어(`gamma quoted`)가 `  검색: ` 줄로 나오고, 검색 · 열람이 한 호출에 섞여도 주소 열람이 `  열람: ` 줄로 나오며, 내부 번호 `turn0search0` 은 표준 오류에 0 번, 변수 약식 셸 명령은 건너뛰어 `  명령: ` 줄이 정확히 1 개다 [exact]
  - 측정: `python3 .harness/.meta/codex-research-activity/measure/check.py forms` 종료 코드 0 이고 출력에 `FAIL` 0 줄
  - 음성 대조: `--base` 는 종료 코드 1(실측). 내부 번호를 거르지 않으면 `turn0search0 … 0 번` 이 FAIL 한다
- [ ] 스크립트-03: 같은 실행에서 여섯 핵심 글자(`공식 문서부터 확인하겠습니다` · `alpha query one` · `beta query two` · `gamma quoted` · `example.com/doc` · `gh api repos/x/y/releases`)가 표준 오류에 각각 정확히 1 번 나온다 — 30초마다 같은 활동을 되풀이하지 않는다 [exact, enumerated]
  - 측정: `python3 .harness/.meta/codex-research-activity/measure/check.py once` 종료 코드 0 이고 출력에 `FAIL` 0 줄
  - 음성 대조: `--base` 는 여섯 개 모두 0 번이라 종료 코드 1(실측). 읽은 자리를 기억하지 않고 매번 처음부터 읽으면 2 번 이상이 되어 FAIL 한다
- [ ] 스크립트-04: 최종 답(`QQZ`)은 표준 오류에 0 번 나오고, 표준 출력과 출력 파일에는 그대로 나오며, 표준 오류에 `완료 (시도 1/2` 줄이 있다 — 최종 답 통로는 그대로다 [exact]
  - 측정: `python3 .harness/.meta/codex-research-activity/measure/check.py answer` 종료 코드 0 이고 출력에 `FAIL` 0 줄
  - 음성 대조: `final_answer` 말을 거르지 않으면 `최종 답이 표준 오류에 0 번` 이 FAIL 한다. `--base` 는 종료 코드 0(실측 — 지켜야 할 기존 동작)
- [ ] 스크립트-05: 진행 줄(`리서치 · ` 로 시작하는 머리 줄과 두 칸 들여쓴 활동 줄)은 모두 200 자 이하이고, 줄바꿈이 든 500 자 넘는 중간 말은 `  말: 긴말` 로 시작해 `…` 로 끝나는 한 줄이 되며 그 둘째 줄이 따로 나오지 않는다 [exact]
  - 측정: `python3 .harness/.meta/codex-research-activity/measure/check.py length` 종료 코드 0 이고 출력에 `FAIL` 0 줄 (길이는 파이썬 글자 수. 실패 줄 `시도 N/N 실패 […]` 는 진행 줄이 아니라 이 조건 밖)
  - 음성 대조: `--base` 는 `긴 말` 이 FAIL 해 종료 코드 1(실측). 자르기나 줄바꿈 합치기를 빼면 FAIL 한다
- [ ] 스크립트-06: Given 한 호출에 검색어 12 개(`burst q01`~`burst q12`)가 한꺼번에 기록될 때, Then 한 번에 내는 들여쓴 줄은 7 줄 이하(활동 6 + 나머지 1)이고 `  …그 밖에 6개` 줄과 `  검색: ` 줄(`burst q01`)이 나온다 [exact]
  - 측정: `python3 .harness/.meta/codex-research-activity/measure/check.py burst` 종료 코드 0 이고 출력에 `FAIL` 0 줄
  - 음성 대조: `--base` 는 종료 코드 1(실측). 상한을 빼면 들여쓴 줄 12 줄 이상이 되어 FAIL 한다
- [ ] 스크립트-07: Given 첫 시도가 활동 1 쌍을 쓰고 종료 코드 1 로 끝나고 둘째 시도가 다른 활동 1 쌍을 쓰고 성공할 때, Then `시도 1/2 실패` 줄과 두 시도의 네 항목(`  말: ` `첫시도말 확인하겠습니다.` · `  검색: ` `first attempt query` · `  말: ` `둘째시도말 다른 길로 갑니다.` · `  검색: ` `second attempt query`)이 표준 오류에 나오고 종료 코드는 0 이다 [exact, enumerated]
  - 측정: `python3 .harness/.meta/codex-research-activity/measure/check.py retry` 종료 코드 0 이고 출력에 `FAIL` 0 줄
  - 음성 대조: `--base` 는 네 항목 FAIL 로 종료 코드 1(실측). 읽은 자리를 시도가 바뀌어도 그대로 두면 둘째 시도 항목이 FAIL 한다
- [ ] 스크립트-08: Given 진행 주기가 100 초라 한 번도 오지 않고 시도가 끝날 때, Then 여섯 활동 항목이 `완료 (시도 1/2` 줄보다 앞에 나오고, 실패한 시도의 활동(`first attempt query`)은 `시도 1/2 실패` 줄보다 앞에 나온다 — 끝내기 직전에 남은 활동을 낸다 [exact]
  - 측정: `python3 .harness/.meta/codex-research-activity/measure/check.py flush` 종료 코드 0 이고 출력에 `FAIL` 0 줄
  - 음성 대조: `--base` 는 종료 코드 1(실측). 끝내기 직전에 남은 활동을 내는 부분을 빼면 FAIL 한다
- [ ] 스크립트-09: Given 한 기록 줄이 반쯤 쓰인 상태에서 진행 주기가 지나고 나중에 나머지가 쓰일 때, Then 그 검색어(`partial query`)가 표준 오류에 정확히 1 번 나오고 `Traceback` 은 0 번이다 [exact]
  - 측정: `python3 .harness/.meta/codex-research-activity/measure/check.py partial` 종료 코드 0 이고 출력에 `FAIL` 0 줄
  - 음성 대조: `--base` 는 종료 코드 1(실측). 줄바꿈으로 끝나지 않은 반 줄을 읽은 것으로 치면 그 활동이 사라지거나 깨져 FAIL 한다
- [ ] 스크립트-10: 전역 규칙 `~/.claude/CLAUDE.md` 에 백틱으로 적힌 Monitor 용 명령이 정확히 `~/.claude/bin/codex-research <프롬프트파일> <출력파일> 2>&1 >/dev/null` 하나이고, 그 글자를 문서에서 그대로 꺼내 자리표시자만 바꿔 돌리면 표준 출력에 검색어 · `완료 (시도 1/2` 줄이 나오고 최종 답 `QQZ` 는 0 번이며, 출력 파일에는 최종 답이 있다 [exact]
  - 측정: `python3 .harness/.meta/codex-research-activity/measure/check.py monitor` 종료 코드 0 이고 출력에 `FAIL` 0 줄 (명령은 문서에서 정규식으로 원문 그대로 꺼낸다 — 다시 타이핑하지 않는다)
  - 음성 대조: `--base` 는 명령 0 개로 종료 코드 1(실측). 문서 명령에서 `>/dev/null` 을 빼면 최종 답이 표준 출력에 섞여 FAIL 한다

## Error

- [ ] 오류-01: Given 세션 기록의 검색 줄 뒤에 깨진 줄 6 종(JSON 아님 `x{` · `payload` 가 null · `payload` 가 문자열 · `content` 항목이 사전 아님 · `input` 이 문자열 아님 · 중간에 잘린 줄)이 있고 같은 묶음에 좋은 말이 이어질 때, Then 래퍼는 종료 코드 0 으로 끝나고, 깨진 줄 바로 뒤 말(`깨진뒤말 이어갑니다.`)과 다음 묶음 열람(`https://example.com/doc`)을 보이며, 표준 오류에 `Traceback` · `Error` 가 0 번이고, 출력 파일에 최종 답이 있다 [exact]
  - 측정: `python3 .harness/.meta/codex-research-activity/measure/check.py corrupt` 종료 코드 0 이고 출력에 `FAIL` 0 줄
  - 음성 대조: `--base` 는 종료 코드 1(실측). 첫 깨진 줄에서 읽기를 멈추면 `깨진뒤말` 이 FAIL 한다

## Architecture

- [ ] 구조-01: 소비면 — `~/.claude/CLAUDE.md` 와 `~/.claude/codex-prompt-template.md` 각각에서 `codex-research` 와 (`run_in_background` 또는 `Monitor`)를 함께 담은 줄이 정확히 1 줄(템플릿은 기존 호출 줄을 고친다)이고, 그 줄에 `Monitor` · 명령 `~/.claude/bin/codex-research <프롬프트파일> <출력파일> 2>&1 >/dev/null` · 접두 `말:` · `검색:` · `열람:` · `명령:` 이 있으며, 파일 전체에서 `작업 카드` 와 `codex-research` 를 함께 담은 줄은 0 이다 [exact, enumerated]
  - 측정: `python3 .harness/.meta/codex-research-activity/measure/check.py docs` 종료 코드 0 이고 출력에 `FAIL` 0 줄
  - 음성 대조: `--base` 는 두 파일 모두 `Monitor` · 명령 · 접두 · `작업 카드` 가 FAIL 해 종료 코드 1(실측)
- [ ] 구조-02: 메모 `~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/memory/feedback_codex_foreground_call_direct.md` 와 그 목차 `MEMORY.md` 의 해당 줄이 「리서치 래퍼는 Monitor 로 띄워 채팅에 진행을 본다」 로 바뀌어, 두 파일 각각 `Monitor` 를 담은 줄이 1 개 이상이고 `작업 카드로 본다` 는 0 줄이다 [exact, enumerated]
  - 측정: `grep -c Monitor` 와 `grep -c '작업 카드로 본다'` 를 두 파일에 각각 돌린다
  - 양성 대조: 지금(고치기 전) `grep -c '작업 카드로 본다'` 가 `MEMORY.md` 에서 1(16:39 실측)

## Anti-patterns

- [ ] 금지-00: N/A (바꾸는 파일이 모두 레포 밖 `~/.claude` 셸 스크립트 · 문서와 레포 `.harness/.meta` 측정 묶음 — `project.yaml` 금지 패턴 4 종은 레포 플러그인 파일 · release.sh 전용)

## Reusability

- [ ] 재사용-01: 다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다 — 활동 읽기는 기존 진행 줄 함수가 이 차례의 세션 기록(`rollout`)을 받아 맡는다
  - 측정: `python3 .harness/.meta/codex-research-activity/measure/check.py reuse` 의 `진행 줄 함수가 이 차례의 세션 기록(rollout)을 읽음` 이 PASS (`--base` 는 FAIL — 실측)
- [ ] 재사용-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다 — 세션 기록을 찾는 길 · 진행 주기 변수를 새로 만들지 않는다
  - 측정: `python3 .harness/.meta/codex-research-activity/measure/check.py reuse` 의 `find "$SESS_DIR" 는 그대로 2 곳` · `progress_every 를 정하는 줄은 그대로 1 줄` 두 줄이 PASS (고치기 전 값 2 · 1 은 `.bak-20261009c` 에서 16:39 실측)

## Diagnostics

- [ ] 진단-01: N/A (commands.analyze 는 `bash -n scripts/release.sh` — 이번 변경 파일과 교집합 0 개. 측정: `git diff --name-only ae918dab feat/codex-research-activity | grep -c '^scripts/release.sh$'` 이 0)
- [ ] 진단-02: IDE diagnostics 워닝/인포 0개 (diagnostics.ide_exclude 는 `[]`) — 래퍼는 `bash -n` 종료 코드 0 이고 `shellcheck -S warning ~/.claude/bin/codex-research` 출력 0 줄, `check.py` 와 `fake/codex` 는 `python3 -c 'import ast,sys; ast.parse(open(sys.argv[1]).read())'` 종료 코드 0
  - 양성 대조: `printf '#!/bin/bash\ncd foo\n' | shellcheck -S warning -` 이 1 줄 이상(SC2164, 16:39 실측 2)
- [ ] 진단-03: N/A (commands.test 는 `bash scripts/release.sh 2>&1 || true` — 이번 변경 파일과 교집합 0 개. 측정: 진단-01 과 같은 명령이 0)
- [ ] 진단-04: 실제 구동 시 에러 0개 — 부모 세션이 진짜 Codex 로 웹 검색이 드는 작은 리서치 1 회를 전역 규칙의 Monitor 명령 그대로 Monitor 로 띄우고, Monitor 가 받은 줄을 `.harness/.meta/codex-research-activity/evidence/real-run.txt` 에 남긴다(첫 줄 `# 명령: <실행한 명령>`, 둘째 줄 `# 출력: <출력 파일 경로>`). 그 파일에서 첫 줄이 문서 명령 꼴(`~/.claude/bin/codex-research <경로> <경로> 2>&1 >/dev/null`)이고, 머리 줄 `리서치 · ` 1 개 이상 · 활동 줄(`  말: ` · `  검색: ` · `  열람: ` · `  명령: `) 1 개 이상 · `완료 (시도` 줄 정확히 1 개 · `Traceback` 0 개이며, 출력 파일 첫 줄(최종 답)이 진행 줄에 0 번 나온다 [exact]
  - 측정: `python3 .harness/.meta/codex-research-activity/measure/check.py evidence` 종료 코드 0 이고 출력에 `FAIL` 0 줄
