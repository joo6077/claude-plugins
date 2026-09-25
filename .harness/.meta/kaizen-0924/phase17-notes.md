# 카이젠 2026-09-24 Phase 17 (howto-kit) — notes

- 계약: `.harness/sprint-contract-kaizen-0924-p17-howto-kit.md` (조건 28 · 기능 조건 18, 봉인 `sha256:33e681f97ba3081e` · `locked_at` 2026-09-25 13:45)
- 개정: `.harness/sprint-amendments-kaizen-0924-p17-howto-kit.md` (조건 변경 0 건, `end_sha` 와 러너 변수 이름 한 건 — `amend_direction: unchanged`)
- 검토: `.harness/.meta/kaizen-0924/phase17-review.md` — 1 회차 `VERDICT: CHANGES`(고칠 것 넷 C1 ~ C4 · 권고 R1 · R2)는 DRAFT 가 전부 반영했다.
  2 회차 `VERDICT: APPROVE` — 새 예행 저장소에서 26 개 ID 출력이 초안 표와 바이트까지 같았다. 2 회차 권고 R3(notes 절 이름)은 BUILD 가 봉인 전에 `## 범위 경계` 산문에 넣었다
- 사용자 승인 대체: 사용자 위임(세션 기록 queued_command `2026-09-24T04:04:16.964Z`) · Codex 한도 소진(2026-09-24) · 「코덱스 대신에 그냥 너가 알아서 진행하라고」(user `2026-09-24T11:54:58.940Z`) — REVIEW 에이전트 검토로 대신했다
- 시작 커밋 `f936019c3f017be3e1bcc92570d677ef8cc6521b`
- 계약 피드백: `~/.harness/feedback/contract/5a24cc99-2026-09-25T135234-de8c7935-54250.yaml` (`verify-feedback.sh` PASS). 초안은 스크래치 `kaizen/p17/feedback-draft.yaml` 에 쓰고
  `HARNESS_CONTRACT_ROOT` · `HARNESS_CONTRACT` 를 명시해 저장했다 — 작업 폴더의 `.harness/feedback-draft.yaml` 은 다른 Phase 와 겹칠 수 있어 쓰지 않았다

## 커밋

| 커밋 | 내용 | 파일 |
| --- | --- | --- |
| `98f4d5e` | 봉인 커밋 | 계약 1 개 |
| `5a96f7c` | 게이트 스크립트를 자식 셸 안에서 읽고 경로를 세 단계로 찾음 · 러너가 블록을 직접 돌림 · 리뷰어 미검증 표기 | `howto-kit/` 일곱 개 |
| `f0af857` | 개정 파일에 `end_sha` (`5a96f7c`) | 개정 1 개 |
| 이 파일의 커밋 | notes · 검토 기록 | `.harness/` 두 개 |
| 그다음 커밋 | 개정 파일에 notes 커밋 sha 로 `end_sha` 한 줄 더 | 개정 1 개 |

모든 커밋 메시지 끝 문단에 `Kaizen-Phase: kaizen-0924-p17-howto-kit` 줄이 있다. 구현 커밋은 `git add -- <일곱> && git commit -o … -- <일곱>` 한 번으로 내 경로만 실었다.
러너와 게이트 스크립트는 git 모드 `100755` 그대로다. **FIX 가 커밋을 더할 때도 서명 줄을 넣고, 개정 파일에 `end_sha:` 줄을 덧붙인다.**

구현은 초안의 예행 도구(스크래치 `kaizen/p17/mock.py`, 지문 앞 16 자리 `d1eef64544f9fcbc` — 계약에 적힌 값)를 작업 폴더에 그대로 돌렸다(`MOCK_OK`).
돌리기 전에 `howto-kit/` · `docs/howto/` 가 시작 커밋과 `HEAD` 사이에 바뀌지 않았고 미커밋 변경도 없는 것을 봤다. 그 뒤 러너에서 새로 쓴 줄의 한 글자 변수 이름만
바꿨다(`tone-kit/references/core-naming.md` N-08 SHOULD) — 개정 파일에 적었다. 편집 전부터 있던 `for c in data['cases']` 는 그대로 뒀다.

28 조건 측정은 봉인 판 계약(`98f4d5e`)에서 뗀 네 블록으로 돌렸다 — 스크래치 `kaizen/p17/kb/`(`common.sh` · `m.sh` · `rule-delta.sh` · `ctl-runner.py`, DRAFT 판 `kaizen/p17/k/` 와
바이트까지 같다) · `kaizen/p17/build-run.sh`(`K` 와 `TMPDIR` 를 스크래치로 두고 `R` 을 비운 채 공통 정의를 `.` 로 읽은 뒤 `m <조건 ID>`). QA 가 같은 묶음을 다시 돌릴 수 있다.
구현 커밋 `5a96f7c` 를 상한으로 둔 첫 측정(`kaizen/p17/out-build-impl.txt` · `out-build-sk08.txt`)에서 스물한 ID 가 조건 줄의 값과 같았다
(ER-02 의 `added=` 수만 예행 256 → 258 — 변수 이름을 바꾼 줄 때문이고, 조건은 수 하나를 요구한다).

커밋 뒤 저장소 검사: `validate-plugin.py howto-kit` 종료 코드 0(V1 ~ V10 OK, V2 는 templates 없음 SKIP) · `sync-docs.py --check-only` 0 · `sync-evals.py --check-only` 0 ·
`run-evals.py` 0(115 passed — howto-kit 은 이 스크립트가 읽지 않는다) · `validate-post-kaizen.py --since f936019` 0(scope-isolation · doc-contracts PASS, docs-site-regen SKIP — Final F2 몫) ·
킷 시험 `howto-kit/evals/run-evals.sh` 를 dash · `/bin/sh` · bash · zsh 로 돌려 넷 다 `EVALS total=33 pass=33 fail=0` · 종료 코드 0, `shellcheck -s sh` 러너 · 게이트 스크립트 종료 코드 0.

말투 대조(tone-guide Step 5, 레포 파일 `tone-kit/skills/tone-guide/SKILL.md` 를 읽고 따름 — 어댑터 없음): 더한 줄의 번역투 6 종(K-02) 0 · `합니다`체 0 · 앱 · 도구 서버 이름 0(ER-02),
C-01(주석은 이유만) — 러너 새 주석 셋은 zsh 가 따옴표 없는 변수를 안 쪼갬 · git 이 실제 경로를 돌려줌 · 픽스처 셋만 쓰는 이유(20 초 대 9 초)라 통과,
N-08(한 글자 이름) — 러너 새 줄에서 고쳤다(위). K-11(새 합성어) — `RESOLVED:` · `MISSING:` 은 출력 줄 머리라 해당 없음.

## GAP 분석 — Phase 1 결과 대조

오케스트레이터 Step 17 전수 감사(`skill-design-guide.md` 1.6.0 · `agent-design-guide.md` 1.7.0) 기준이다. 계약 `## GAP 분석` 절 표와 같다.

| Phase 1 변경 | howto-kit 에서 본 자리 | 처리 |
| --- | --- | --- |
| agent 가이드 §10 1 · 2 항 — 분류 접미 `:ENV` · `:INVALID` 와 `ENV` 의 네 칸 | howto-reviewer 규칙 7 · 출력 형식의 접미 없는 `[미검증]` | SK-06 — 두 줄을 `[미검증:ENV]` · `[미검증:INVALID]` 와 네 칸으로 |
| skill 가이드 §3.7 조항 3 — 검증 · 작업을 못 할 때 네 칸(막는 것 · 시도한 우회 · 통제 불가 사유 · 재검증 명령) | 옛 블록은 스크립트를 못 찾아도 `command not found` 를 흘리고 넘어갔다 | 새 블록은 `MISSING:` 줄에 막는 것과 시도한 세 곳을 찍고 0 이 아닌 코드로 멈춘다. 두 스킬 문단이 나머지 두 칸을 붙여 `[미검증:ENV]` 로 보고하게 한다 (ER-04 · SK-02 · SK-04) |
| 0 이 기대값인 검증의 양성 대조 | 러너의 새 검사(`blocks-declared` · 네 경우) | SK-08 러너 변형 여덟과 zsh 대조 둘 |
| 알려진 답 대조 | 블록을 돌렸을 때의 판정 줄 수 | 손으로 센 답 — 픽스처 폴더 열다섯 · 파일 하나 (SK-01 · SK-03 · SK-05) |
| 에이전트 frontmatter 18 종 · 500 줄 권고 | howto-reviewer 네 필드 모두 목록 안 · 고친 SKILL.md 둘은 145 · 151 줄(howto 는 247 줄 그대로) | 해당 없음 |

howto-kaizen 절차 대조(`.claude/skills/howto-kaizen/SKILL.md`, 레포 파일):

| 절차 | 이번 Phase 에서 | 처리 |
| --- | --- | --- |
| Step 0 트리거 | 게이트가 놓친 실패의 실측 — 처리 배정표 P4 행 (자식 셸이 함수를 못 봐 판정 줄 0) | 진행 |
| Step 1 현행 측정 | 시작 커밋 판 러너 `EVALS total=16 pass=16 fail=0` · `validate-plugin.py howto-kit` 종료 코드 0 | 비교 기준값 |
| Step 2 한 사이클 관심사 1~2 개 | (1) 게이트 스크립트를 부르는 길과 그 길을 재는 러너 (2) 리뷰어의 판정 불가 표기 | 둘 |
| Step 3 새 검사에는 픽스처를 같이 등록 | 새 검사는 게이트가 아니라 러너 쪽이다. 살아 있다는 증명은 SK-08 변형 여덟으로 봉인 전 · 구현 뒤에 보였다 | 킷 안 픽스처로 둘지는 다음 사이클 메모 |
| Step 4 회귀 확인 | 끝 판 러너 `EVALS total=33 pass=33 fail=0`(네 해석기) · `validate-plugin.py howto-kit` 0 · `sync-docs.py --check-only` 0 | 통과 |

하지 않기로 한 여섯과 이유:

- `export -f` 로 함수를 넘기지 않는다 — 이 맥에서 `/bin/sh` · bash 자식만 부르고 `/bin/dash` · zsh 자식은 못 부른다(SK-02 넷째 줄). 우분투의 `sh` 는 dash 라 CI 에서 깨지고,
  `howto_gate` 가 부르는 보조 함수 둘과 변수 셋은 넘어가지 않아 macOS 에서도 판정이 깨진다(SK-08 `n2`)
- 레포 경로를 플러그인 경로보다 먼저 보지 않는다 — qa-evaluator Step 8 순서를 따르고, 어느 사본을 썼는지는 `RESOLVED:` 줄로 보인다(howto-doc 보고 · howto-audit 리포트 틀)
- 셋째 단계에 설치 복사본 `~/.claude/plugins/cache/*/howto-kit/*/` 를 넣지 않는다 — 아래 미반영 절
- 러너를 새 파일로 나누지 않는다 — 나누면 CI 넘김 줄 · howto-kaizen 절차 · README 표가 하나씩 늘어난다
- `references/provenance-notes.md` §9 · `docs/howto/procedure-standards.md` §4 에 26514 용어 정의 · DITA 2.0 초안 변화를 적지 않는다 — 아래 미반영 절
- howto-audit Phase 4 리포트 틀에 에이전트의 `[미검증]` 칸을 더하지 않는다 — 옛 표기에도 칸이 없던 기존 빈틈이고, SK-06 은 표기만 바꾼다

## 바꾼 파일

- `howto-kit/skills/howto-audit/SKILL.md` — Gotcha 6(함수는 자식 셸로 넘어가지 않는다 · 상대 경로 금지 · 실측), Phase 2 블록(세 단계 경로 찾기 · `sh -c` 안에서 읽기 · `RESOLVED:` / `MISSING:`)과
  뒤 문단(`MISSING:` 이면 멈춤 · 줄 수 대조 · `find` 종료 코드로 판정하지 않음 · `[미검증:ENV]` 네 칸), Phase 4 리포트 틀에 `스크립트:` 줄
- `howto-kit/skills/howto-doc/SKILL.md` — Gotcha 3 블록(폴더를 도는 블록, `find docs` → `find <대상>`)과 세 줄, Phase 4 블록과 여섯 줄(`RESOLVED:` 줄을 보고에 · 세 단계 · `MISSING:` 이면 완료 보고 금지 · 네 칸)
- `howto-kit/README.md` — `## 결정론 게이트 G1~G6` 사용 블록과 세 줄, `## Evals` 문단(세 셸 · 블록 네 경우 · `gate_blocks`). AUTO 구간은 그대로
- `howto-kit/scripts/howto-gate.sh` — 머리 주석만(사용법 · 세 단계 경로 · 자식 셸 · 세 셸 대조). `HOWTO_VERBS=` 줄부터 끝(판정 코드)은 그대로
- `howto-kit/evals/run-evals.sh` — 사례를 zsh · bash · sh 세 셸로 대조, assertion 을 파일로 받아 한 줄씩(zsh 로 불러도 판정이 같다), 킷 안 마크다운에서 게이트를 부르는 `bash` 블록을
  뽑아 `plugin` · `repo` · `market` · `none` 네 경우에서 zsh · bash 로 돌림, 파일마다 블록 수를 `gate_blocks` 와 대조(`blocks-declared`). 사례 16 → 33
- `howto-kit/evals/evals.json` — `description` 을 세 셸로, `gate_blocks` 필드 추가. 사례 열여섯 · `runner` · `kit` 은 그대로
- `howto-kit/agents/howto-reviewer.md` — 규칙 7 · 출력 형식의 판정 불가 표기를 `[미검증:ENV]` · `[미검증:INVALID]` 와 네 칸으로

## 반영한 처리 배정표 키

| 키 | 반영 |
| --- | --- |
| `other-kits:P4` | 게이트를 부르는 블록 넷(howto-audit Phase 2 · howto-doc Gotcha 3 · howto-doc Phase 4 · README)이 스크립트를 플러그인 설치 경로(`${CLAUDE_PLUGIN_ROOT}` 치환) → git 최상위 폴더의 `howto-kit/` → 마켓플레이스 설치본 순으로 찾고, 폴더를 도는 둘은 `sh -c` 안에서 읽는다. 못 찾으면 `MISSING:` 과 시도한 세 곳을 찍고 0 이 아닌 코드로 멈춘다. 옛 howto-audit 블록은 시험 입력 열다섯에 `command not found` 15 줄 · 판정 줄 0 이었고, 새 블록은 세 경우 모두 판정 줄 15 다 (SK-01 ~ SK-05 · SK-09 · ER-04 · RE-02) |
| `other-kits:P3` 의 howto-kit 단계 | 러너 쪽 — 세 셸 대조, 게이트를 부르는 블록을 직접 돌림, zsh 로 불러도 판정이 같음(SK-07 · SK-08 · DG-04). CI 줄은 러닝북이 Final 몫으로 정했다 — 아래 넘김 표. P3 의 onboarding-kit 시험 입력은 Phase 14 몫 |

적용 힌트 「검사 함수가 자식 셸에서 실제로 불리게 고친다」 는 SK-01 · SK-03 의 `plugin:R/15/15/0/0/1` 과 러너 사례 `howto-audit-1:*` · `howto-doc-1:*` 이다.
편집 전 감사가 찾은 러너 결함(zsh 로 부르면 assertion 이 한 덩어리가 되어 틀린 assertion 도 `EVALS_PASS`)도 같은 파일에서 고쳤다 — SK-08 `n7z_end rc=1` · `n7z_base rc=0`.

## 미반영 키와 사유

처리 배정표 키는 둘 다 반영했다(P3 은 howto-kit 단계만 — 이 Phase 몫). 근거 파일 권장안 가운데 아래는 넣지 않았다.

- DITA 2.0 초안에서 인용 문장 두 개가 빠진 것 — 근거 파일 §4 7 항이 「선택, 이번 범위 밖」 으로 적었고, 2.0 은 아직 표준이 아니다(v2.0-beta03). 표준이 되면 `provenance-notes.md` §9 에 적는다
- ISO/IEC/IEEE 26514:2022 용어 정의를 무료 견본으로 확인할 수 있다는 것 — 같은 7 항. 원장 항목(절차 작성 세부 조항)은 견본으로 확인되지 않아 여전히 미확인이다
- 설치 복사본 `~/.claude/plugins/cache` 를 셋째 단계에 넣는 것 — 버전 폴더가 여럿이면 고를 규칙이 없다(근거 파일 §5 열린 질문). 레포의 기존 순서(qa-evaluator Step 8)가 `marketplaces` 를 보므로 그대로 따랐다
- 근거 파일 §4 2 항의 「찾은 경로는 인자로 넘긴다」 는 반영했다(`sh "$GATE" {} +`). 「레포 경로를 먼저 볼지」 열린 질문은 위 하지 않기로 한 것 둘째 줄로 정했다

## 넘기는 것

| 파일 | 남은 것 | 맡을 곳 |
| --- | --- | --- |
| `.github/workflows/ci.yml` | validate 작업에 `command -v zsh >/dev/null \|\| { sudo apt-get update && sudo apt-get install -y zsh; }` 다음 `sh howto-kit/evals/run-evals.sh` 한 단계. 없을 때만 설치하고, 없으면 SKIP 으로 두지 않는다 — zsh 가 없으면 러너가 종료 코드 2 로 실패하는 지금 동작을 살린다. 러너는 git 도 쓴다(러너 머리 `TOOL_MISSING git`). 우분투 이미지의 `sh` 는 dash 라 러너의 셋째 셸이 dash 가 된다 | Final |
| `.claude/skills/howto-kaizen/SKILL.md` | `:26` Gotcha 2 「eval runner 가 두 셸 출력 동일성까지 검사한다」 → 세 셸 · 블록 네 경우. Step 1 이 부르는 러너 출력 줄 모양(`EVALS_PASS`)은 그대로다 | Final |
| `docs/howto-kit/overview.html` | `:318` 「두 셸 출력의 동일성」 | Final F2 |
| `howto-kit/.claude-plugin/plugin.json` | 버전 (이 Phase 는 버전을 적지 않았다 — AP-01) | Final |

## changelog 한 단락

howto-kit — `/howto-audit` Phase 2 가 부모 셸에서 게이트 스크립트를 읽고 `find -exec sh -c` 자식에서 부르던 탓에 파일마다 `command not found` 만 내고 판정 줄이 0 이던 것을 고쳤다.
게이트를 부르는 네 블록(`/howto-audit` Phase 2 · `/howto-doc` Gotcha 3 · Phase 4 · README)이 스크립트를 플러그인 설치 경로 → git 최상위 폴더 → 마켓플레이스 설치본 순으로 찾고
`RESOLVED:` 줄로 어느 사본을 썼는지 보이며, 못 찾으면 `MISSING:` 과 시도한 세 곳을 찍고 멈춘다 — 킷을 플러그인으로 설치한 프로젝트에서도 돈다.
러너는 사례를 zsh · bash · sh 세 셸로 대조하고 스킬 본문의 블록을 네 경우에서 직접 돌린다(사례 16 → 33). 러너를 zsh 로 부르면 틀린 assertion 도 통과하던 결함도 고쳤다.
`howto-reviewer` 의 판정 불가 표기는 `[미검증:ENV]` · `[미검증:INVALID]` 와 네 칸이다.

## 킷 로그 한 단락

2026-09-24 Phase 17 — 셸 함수는 `find` 가 새로 띄운 셸로 넘어가지 않는다([ShellCheck SC2033](https://www.shellcheck.net/wiki/SC2033),
[POSIX Shell Command Language](https://pubs.opengroup.org/onlinepubs/9799919799/utilities/V3_chap02.html) ·
[POSIX find](https://pubs.opengroup.org/onlinepubs/9799919799/utilities/find.html)). `export -f` 는 bash 기능이라([bash(1)](https://man7.org/linux/man-pages/man1/bash.1.html))
dash · zsh 자식에게 안 넘어간다([zsh Functions](https://zsh.sourceforge.io/Doc/Release/Functions.html) · 이 맥 실측). `${CLAUDE_PLUGIN_ROOT}` 는 플러그인 스킬 본문에서 글자로
치환되고 환경 변수로는 훅 · 보조 서버에만 간다([Claude Code skills](https://code.claude.com/docs/en/skills) · [Plugins reference](https://code.claude.com/docs/en/plugins-reference)).
CI 우분투 이미지에 zsh 가 없고 `sh` 가 dash 인 것은 [runner-images Ubuntu 24.04](https://github.com/actions/runner-images/blob/main/images/ubuntu/Ubuntu2404-Readme.md) ·
[GitHub Docs](https://docs.github.com/en/actions/how-tos/manage-runners/github-hosted-runners/customize-runners) 로 확인했다(설치 전 `apt-get update`).

## 다음 사이클 메모

- howto-audit Phase 4 리포트 틀에 에이전트의 `[미검증:ENV]` · `[미검증:INVALID]` 칸이 없다 — 옛 표기에도 없던 빈틈이다. 칸을 더할지 정한다
- DITA 2.0 이 표준이 되면 인용 문장 두 개가 빠진 것을 `provenance-notes.md` §9 에 적는다. 26514 견본으로 원장 항목을 확인할 수 있는지 다시 본다.
  설치 복사본 `cache` 를 셋째 단계에 넣을지는 버전 폴더를 고를 규칙(예: 설치 기록 파일)이 확인되면 다시 본다
- 러너 자체의 음성 대조(이번 SK-08 변형 여덟)를 킷 안 시험으로 둘지 — 지금은 계약 측정 안에만 있다
- 러너 시간이 3.4 초에서 8 ~ 9 초로 늘었다. CI 에 넣은 뒤 시간 상한을 조건으로 둘지 정한다(계약 피드백 `nfr_coverage: true`)
- 러너에 편집 전부터 있던 `for c in data['cases']`(한 글자 이름)가 남아 있다 — 다음에 러너를 고칠 때 같이
- `docs/howto/design-brief.md:385` C5 「zsh·bash 양쪽에서 실행」 은 틀린 말은 아니지만 러너가 세 셸을 대조하게 됐다 — 설계 문서를 다시 볼 때 같이
- 플러그인 치환(`plugin` 경우)은 Claude Code 가 하는 글자 치환을 측정이 흉내 낸 것이다. 설치본으로 `/howto-audit` 을 실제로 불러 `RESOLVED:` 줄을 확인하는 것은 Final 뒤 배포본에서
- `save-feedback.sh` 가 이 워크트리에서 `project_name: 'kaizen-0924'`(워크트리 이름)를 적었다 — Phase 4 · Phase 12 몫과 같은 문제
