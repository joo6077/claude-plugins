---
feature: "카이젠 2026-09-24 Phase 17 계약 — 게이트 스크립트를 자식 셸 안에서 읽고 경로를 세 단계로 찾음 · 러너가 게이트를 부르는 블록을 직접 돌림 · 리뷰어 미검증 표기"
slug: kaizen-0924-p17-howto-kit
created: "2026-09-25 12:49"
complexity: "복잡"
conditions: 28
status: active
owner_session: de8c7935-a5b6-4df5-9106-fafa73c288a0
conditions_digest: sha256:33e681f97ba3081e
locked_at: "2026-09-25 13:45"
---

## 배경

이 Phase 의 외부 근거는 `.harness/.meta/evidence/phase17.md` 하나다. 처리 배정표(`.claude/kaizen-input/insights-report.md`)에서 `배정` 칸이
`Phase 17` 인 행은 `other-kits:P4` 하나다. `other-kits:P3` 는 Phase 14 배정이지만 비고가 「howto-kit 단계는 Phase 17 과 함께 넣는다」 로 이 Phase 를 가리키고,
적용 힌트도 「other-kits:P4 (other-kits:P3 의 howto-kit 자동 검사 단계 포함). 검사 함수가 자식 셸에서 실제로 불리게 고친다」 다. 러닝북 `Phase 별 추가 과제` 에
Phase 17 줄은 없다. 앞 Phase notes 가 넘긴 줄은 Phase 14 의 「howto-kit 단계는 Phase 17 과 함께」 하나다. 데이터 풀 §0-b 에 howto-kit 을 적은 세션은 없고,
§0.5 에 howto-kit 도메인 그룹이 없다 — 「규칙을 바꾸면 바뀌는 낱말로 저장소 전체를 먼저 검색하라」(grounding `미분류`)는 배경으로만 따라 `howto-gate` · `howto_gate` 로
레포 전체를 먼저 찾았다. 오케스트레이터 Step 17 은 「Phase 1 에서 설계 가이드가 변경되었으면 howto-kit 전 스킬을 전수 감사한다」 고 적는다 — 그 결과는 `GAP 분석` 절 둘째 표에 있다.

| 키 · 출처 | 내용 | 이번 처리 |
| --- | --- | --- |
| `other-kits:P4` | howto-audit 이 자식 셸에서 검사 함수를 못 부름, 상대 경로 호출 | 반영 — 게이트를 부르는 블록 넷(howto-audit Phase 2 · howto-doc Gotcha 3 · howto-doc Phase 4 · README)을 스크립트를 `sh -c` 안에서 읽는 모양과 세 단계 경로 찾기로 바꾼다(SK-01 ~ SK-05 · SK-09 · ER-04 · RE-02) |
| `other-kits:P3` 의 howto-kit 단계 | 자동 검사에 howto-kit 시험 단계 | 러너 쪽만 반영 — 러너가 세 셸을 대조하고 게이트를 부르는 블록을 직접 돌리며 zsh 로 불러도 판정이 같다(SK-07 · SK-08 · DG-04). CI 줄은 러닝북이 Final 몫으로 정했다 — notes 넘김 표에 넣을 줄을 적는다(ER-03) |
| 오케스트레이터 Step 17 전수 감사 | Phase 1 이 바꾼 agent-design-guide §10 — `[미검증]` 에 분류 접미와 네 칸 | 반영 — howto-reviewer 의 판정 불가 표기 두 줄(SK-06) |
| 편집 전 감사가 찾은 러너 결함 | 러너를 zsh 로 부르면 assertion 검사가 꺼진다 — 틀린 assertion 에도 `EVALS_PASS` | 반영 — 러너를 고치는 김에 같은 파일에서(SK-08 `n7z`) |

## 리서치 소스

근거 파일 `.harness/.meta/evidence/phase17.md` 에서만 가져왔다. 새로 찾은 자료는 없다.

- [ShellCheck SC2033](https://www.shellcheck.net/wiki/SC2033) — 셸 함수는 `find` 같은 외부 명령에 넘어가지 않는다. 해법은 `sh -c` 안에서 실행하기 (SK-01 · SK-02)
- [POSIX 2024 Shell Command Language](https://pubs.opengroup.org/onlinepubs/9799919799/utilities/V3_chap02.html) — 별도 실행 환경으로 넘어가는 목록에 함수가 없다. 점 명령이 파일을 못 찾으면 비대화형 셸은 중단한다 (SK-02 · ER-04)
- [POSIX 2024 find](https://pubs.opengroup.org/onlinepubs/9799919799/utilities/find.html) — `-exec … {} +` 는 유틸리티를 새로 실행하고 작업 폴더는 find 를 시작한 폴더다 (SK-01)
- [bash(1)](https://man7.org/linux/man-pages/man1/bash.1.html) · [zsh Functions](https://zsh.sourceforge.io/Doc/Release/Functions.html) — `export -f` 는 bash 기능이다. 근거 파일 실측: dash · zsh 자식에게 안 넘어간다 (SK-02 · SK-08 `n2`)
- [Claude Code skills](https://code.claude.com/docs/en/skills) · [Plugins reference](https://code.claude.com/docs/en/plugins-reference) — `${CLAUDE_PLUGIN_ROOT}` 는 플러그인 스킬 본문에서 글자로 치환된다. 환경 변수로 내보내는 곳은 훅 · 보조 서버 프로세스뿐이다. 설치 복사본은 `~/.claude/plugins/cache` 에 있다 (SK-01 · RE-02)
- [actions/runner-images](https://github.com/actions/runner-images) · [Ubuntu 24.04 설치 목록](https://github.com/actions/runner-images/blob/main/images/ubuntu/Ubuntu2404-Readme.md) · [GitHub Docs — Customizing GitHub-hosted runners](https://docs.github.com/en/actions/how-tos/manage-runners/github-hosted-runners/customize-runners) — 우분투 이미지에 zsh 가 없고 `sh` 는 dash 다. 설치 전 `apt-get update` (ER-03 넘김 줄)
- 내부: `harness/agents/qa-evaluator.md:1089`~`:1097` Step 8 · `harness/skills/refactor-checklist/SKILL.md:52`~`:61` — 레포의 기존 경로 찾기 순서(플러그인 치환 → 레포 → 마켓플레이스 설치본, `RESOLVED:` / `MISSING`). 새 순서를 만들지 않고 이 순서를 따른다 (RE-02)
- 내부: `harness/docs/guides/agent-design-guide.md` §10 Unverifiable 조건 정책 1 · 2 항 · `harness/docs/guides/skill-design-guide.md` §3.7 (Phase 1 결과) — SK-06 · ER-04

## GAP 분석 · 개선안 초안

복잡도 4 축 (Step 1). 넷 다 예라 **복잡** 이다 — Step 2.5 양면 조건을 넣었다(생산 쪽 SK-01 ~ SK-09, 소비 쪽 넘김 ER-03).

| 축 | 물음 | 값 |
| -- | ---- | -- |
| 레이어 수 | 몇 개 계층을 관통하는가 | 셋 — 스킬 문서(SKILL.md 둘 · README · 에이전트) · 실행 스크립트(러너 · 게이트 스크립트 머리 주석) · 평가 데이터(`evals.json`) |
| 공개 API·계약 변경 | 밖에서 읽는 형식이 바뀌는가 | 예 — 게이트를 부르는 블록의 첫 줄이 `RESOLVED:` 또는 `MISSING:` 이 되고, 러너 사례가 16 에서 33 으로 늘고, `evals.json` 에 `gate_blocks` 필드가 생긴다 |
| 소비면 존재 | 반대편이 있는가 | 예 — howto-audit Phase 4 리포트(같은 스킬 안 — SK-02 가 셈 규칙을 적는다) · `.claude/skills/howto-kaizen/SKILL.md` Step 1 · 4(러너를 부르고 `EVALS_PASS` 를 읽는다 — 그 줄 모양은 그대로다. Gotcha 2 의 「두 셸」 은 범위 밖 넘김) · CI(범위 밖 넘김) · `docs/howto-kit/overview.html:318` 「두 셸 출력의 동일성」(범위 밖, Final F2 넘김). 레포 스크립트 둘은 howto-kit 을 안 읽는다 — `scripts/run-evals.py:32` `ALL_KITS` · `scripts/sync-evals.py:32` `TARGET_KITS` |
| 회귀 위험 | 기존 동작이 깨질 경로 | 예 — 두 스킬이 실제로 부르는 블록을 바꾸고 러너를 다시 쓴다. 게이트 판정 코드(`HOWTO_VERBS=` 줄부터 끝까지)와 평가 사례 열여섯은 그대로 둔다(AR-03) |

설정 리터럴 대조표 (Step 1.2, `.harness/project.yaml` 원문):

| config key | project.yaml 에서 읽은 값 | 계약에 쓴 값 |
| ---------- | ------------------------- | ------------ |
| `commands.analyze` | `bash -n scripts/release.sh` | DG-01 N/A 사유에 그대로 |
| `commands.test` | `bash scripts/release.sh 2>&1 \|\| true` | DG-03 N/A 사유에 그대로 |
| `diagnostics.ide_exclude` | `[]` | DG-02 에 그대로 |
| `contract_categories[].id` / `prefix` | Skill/SK · Script/SC · Error/ER · Architecture/AR | 그대로 |
| `anti_patterns[].id` / `message` | AP-01 · AP-02 · AP-03 · AP-04 | AP-01 · AP-03 · AP-04 — 메시지 원문 그대로. AP-02(force push)는 이 Phase 가 푸시하지 않아 뺐다 |

편집 전 감사 (Step 1.4, 대상 파일을 실제로 읽은 줄):

| 대상 파일 | 실제 Read 증거 (`파일:라인`) | 발견한 기존 갭·위반 | 계약 조건화 여부 |
| --------- | ---------------------------- | ------------------- | ---------------- |
| `howto-kit/skills/howto-audit/SKILL.md` | `:73`~`:82` Phase 2 — 부모 셸에서 `. howto-kit/scripts/howto-gate.sh` 뒤 `find -exec sh -c` 자식에서 `howto_gate` · `:61`~`:64` Gotcha 5(마지막 Gotcha) · `:89`~`:103` Phase 4 리포트 틀 | 자식 셸이 함수를 못 본다 — 시작 커밋 판 블록을 시험 입력 열다섯에 돌리면 `command not found` 15 줄, 판정 줄 0 (봉인 전 실측, `m SK-01` 시작 커밋 판 `X/15/0/15/1`). 상대 경로라 플러그인 설치 프로젝트에서 못 찾는다 | SK-01 · SK-02 · ER-04 |
| `howto-kit/skills/howto-doc/SKILL.md` | `:55`~`:69` Gotcha 3 블록(`sh -c` 안에서 상대 경로로 읽음) · `:98`~`:105` Phase 4 블록과 「출력 7 줄을 보고에 **그대로** 붙인다.」 | 둘 다 상대 경로 — 레포 밖에서 Phase 4 블록은 종료 코드 127 · `not found` 한 줄, 판정 줄 0 (`m SK-03` 시작 커밋 판 `plugin:X/0/0/1/127/0`) | SK-03 · SK-04 · ER-04 |
| `howto-kit/README.md` | `:55`~`:58` 사용 블록(상대 경로) · `:108`~`:109` 「zsh 와 bash 양쪽에서」 | 사용 블록이 레포 루트에서만 돈다. 러너가 부르는 셸 수와 설명이 어긋나게 된다 | SK-05 |
| `howto-kit/scripts/howto-gate.sh` | `:4`~`:8` 머리 주석(상대 경로 사용법 · 「zsh · bash · sh 에서 동일 출력」) · `:13`~`:190` 판정 코드 | 러너가 sh 를 재지 않아 「sh 에서 동일」 이 측정되지 않은 주장이었다. 판정 코드는 고칠 곳이 없다 | SK-09 · AR-03 (그대로) |
| `howto-kit/evals/run-evals.sh` | `:39`~`:40` zsh · bash 두 셸만 · `:46`~`:56` `for a in $for_each` — 따옴표 없는 변수 | 러너를 zsh 로 부르면 assertion 이 한 덩어리로 `grep -F` 에 들어가 하나만 맞아도 통과한다 — 봉인 전 실측: 사례 E2 의 assertion 을 틀리게 바꾼 사본에서 sh · bash 는 `rc=1 fail=1`, zsh 는 `rc=0 pass=16`(`m SK-08` `n7z_base`). 게이트를 부르는 블록은 한 번도 돌리지 않는다 | SK-07 · SK-08 · DG-04 |
| `howto-kit/evals/evals.json` | `:3` 설명 「zsh 와 bash 양쪽」 · `:4` `runner` · `:5`~ 사례 열여섯 | 블록 수를 적을 자리가 없다 | SK-09 · AR-03 (사례 그대로) |
| `howto-kit/agents/howto-reviewer.md` | `:29`~`:30` 규칙 7 · `:78` 출력 형식 — 접미 없는 `[미검증]` 두 곳 | Phase 1 이 바꾼 agent-design-guide §10 1 · 2 항과 어긋난다. 이 킷의 G2 도 접미 없는 마커를 절차 문서에서 막는다 | SK-06 |
| `howto-kit/skills/howto/SKILL.md` · `howto-kit/references/` 다섯 · `docs/howto/` | `howto/SKILL.md:225` · `references/step-contract.md:109` · `references/source-tiers.md:31` · `docs/howto/deprecation-policy.md:86` — 게이트 스크립트를 가리키기만 하고 부르지 않는다 (`git grep -n 'howto-gate\|howto_gate'`) | 고칠 곳이 없다 | AR-03 (그대로) |
| `.claude/skills/howto-kaizen/SKILL.md` · `docs/howto-kit/overview.html` · `.github/workflows/ci.yml` | `howto-kaizen/SKILL.md:26` 「두 셸 출력 동일성」 · `overview.html:318` 「두 셸 출력의 동일성」 · `ci.yml:46`~`:47` `run-evals.py --verbose` 뿐 | 이 Phase 범위 밖(레포 전용 스킬 · 문서 사이트 · 공유 파일) | 범위 밖 — ER-03 넘김 |
| `harness/agents/qa-evaluator.md` · `harness/skills/refactor-checklist/SKILL.md` | `qa-evaluator.md:1089`~`:1097` · `refactor-checklist/SKILL.md:52`~`:61` | 기존 경로 찾기 순서 — 읽기만 한다 | RE-02 |

Phase 1 결과 대조 (오케스트레이터 Step 17 전수 감사 — `skill-design-guide.md` 1.6.0 · `agent-design-guide.md` 1.7.0):

| Phase 1 변경 | howto-kit 에서 본 자리 | 처리 |
| --- | --- | --- |
| agent 가이드 §10 1 · 2 항 — 분류 접미 `:ENV` · `:INVALID` 와 `ENV` 의 네 칸 | howto-reviewer `:30` · `:78` 접미 없는 `[미검증]` | SK-06 |
| skill 가이드 §3.7 조항 3 — 검증 · 작업을 못 할 때 `[미검증]` 에 네 칸(막는 것 · 시도한 우회 · 통제 불가 사유 · 재검증 명령) | 옛 블록은 스크립트를 못 찾아도 `command not found` 를 흘리고 넘어갔다 | 새 블록은 `MISSING:` 줄에 막는 것과 시도한 세 곳을 찍고 0 이 아닌 코드로 멈춘다. 두 스킬 문단이 그 줄에 나머지 두 칸을 붙여 `[미검증:ENV]` 로 보고하게 한다 (ER-04 · SK-02 · SK-04) |
| 0 이 기대값인 검증의 양성 대조 | 러너의 새 검사(`blocks-declared` · 네 경우) | SK-08 대조 여덟과 `n7z` |
| 알려진 답 대조 | 블록을 돌렸을 때의 판정 줄 수 | 손으로 센 답 — 픽스처 폴더 열다섯 · 파일 하나 (SK-01 · SK-03 · SK-05) |
| 에이전트 frontmatter 18 종 | howto-reviewer — `name` · `description` · `tools` · `model` 넷, 모두 목록 안 | 해당 없음 |
| 500 줄 「권고」 | SKILL.md 114 · 123 · 247 줄 → 편집 뒤 150 줄 안팎 | 해당 없음 |

`.claude/skills/howto-kaizen/SKILL.md` 절차 대조 (이 Phase 의 카이젠 스킬):

| 절차 | 이번 Phase 에서 | 처리 |
| --- | --- | --- |
| Step 0 트리거 | 「게이트가 놓친 실패 사례가 실측으로 잡혔다」 — `other-kits:P4` (자식 셸이 함수를 못 봐 판정 줄 0) | 진행 |
| Step 1 현행 측정 | 시작 커밋 판 러너 `EVALS total=16 pass=16 fail=0` · `validate-plugin.py howto-kit` (`회귀 게이트` 절 시작 커밋 판 SK-07 · DG-05) | 비교 기준값으로 기록 |
| Step 2 한 사이클 관심사 1~2 개 | (1) 게이트 스크립트를 부르는 길과 그 길을 재는 러너 (2) 리뷰어의 판정 불가 표기 — 둘로 센다 | 상한 안 |
| Step 3 새 검사에는 픽스처를 같이 등록 | 러너의 새 검사(`blocks-declared` · 네 경우)가 살아 있다는 증명은 SK-08 변형 여덟으로 봉인 전에 보인다. 킷 안 픽스처로는 두지 않는다 | 러너 자체의 음성 대조를 킷 안에 둘지는 notes 다음 사이클 메모 |
| Step 4 회귀 확인 | `validate-plugin.py howto-kit` · 러너 · `sync-docs.py --check-only` | DG-05 · SK-07 · RE-01 이 잰다. 레포 전체 `sync-docs.py --check-only` 는 BUILD 검증 |

개선안 초안 — 정확한 문장은 조건 줄과 `m.sh` 토큰이 기준이다. 예행 도구 `mock.py`(스크래치 `kaizen/p17/`)가 시작 커밋 판에 그대로 적용해 본 판이다.

1. **게이트를 부르는 블록 넷** (`other-kits:P4`) — 앞 여섯 줄이 같은 경로 찾기다: `GATE="${CLAUDE_PLUGIN_ROOT}/scripts/howto-gate.sh"` → `git rev-parse --show-toplevel` 아래 `howto-kit/scripts/howto-gate.sh` →
   `find "$HOME/.claude/plugins/marketplaces" -maxdepth 4 -type f -path '*/howto-kit/scripts/howto-gate.sh'`, 찾으면 `RESOLVED: <경로>` 를 찍는다. 폴더를 도는 두 블록은
   `find <대상> … -exec sh -c '. "${1}"; shift; …' sh "$GATE" {} +` 로 스크립트를 자식 셸 **안에서** 읽고, 파일 하나를 도는 두 블록은 같은 셸에서 `. "$GATE"; howto_gate <…>` 다.
   못 찾으면 `MISSING: howto-gate.sh tried=<세 곳>` 을 찍고 `false` 로 끝난다. `export -f` 는 쓰지 않는다
2. **스킬 문단** — howto-audit 에 Gotcha 6(함수는 자식 셸로 넘어가지 않는다 · 상대 경로 금지 · 실측), Phase 2 뒤에 `MISSING:` 이면 멈춤 · `### <경로>` 줄 수와 판정 줄 수와 Phase 1 파일 수가 같아야 함 ·
   `find` 종료 코드로 판정하지 않음 · `MISSING:` 으로 멈출 때 `[미검증:ENV]` 네 칸 두 줄, Phase 4 리포트 틀에 `RESOLVED:` 줄 한 줄. howto-doc Gotcha 3 뒤 세 줄, Phase 4 뒤 여섯 줄(같은 네 칸 두 줄 포함).
   README 사용 블록 뒤 세 줄과 Evals 문단. 게이트 스크립트 머리 주석
3. **러너** — 게이트 사례를 zsh · bash · sh 세 셸로 대조하고, assertion 을 파일로 받아 한 줄씩 돌아 zsh 로 불러도 판정이 같게 한다. 킷 안 마크다운에서 게이트를 부르는 `bash` 블록을 뽑아
   `plugin` · `repo` · `market` · `none` 네 경우에서 zsh · bash 로 돌리고, 파일마다 찾은 블록 수를 `evals.json` 의 `gate_blocks` 와 대조한다. 폴더 경우는 픽스처 이름순 앞 셋만 쓴다(20 초 → 9 초)
4. **Phase 1 대조** — howto-reviewer 두 줄을 `[미검증:ENV]` · `[미검증:INVALID]` 와 네 칸으로

하지 않기로 한 것:

- `export -f` 로 함수를 넘기지 않는다 — 봉인 전 실측(`m SK-02` 넷째 줄) `/bin/sh=called bash=called /bin/dash=no zsh=no`. 우분투의 `sh` 는 dash 라 CI 와 zsh 에서 깨진다.
  게다가 `howto_gate` 가 부르는 보조 함수 둘과 변수 셋은 넘어가지 않아 macOS 에서도 판정이 깨진다(SK-08 `n2`)
- 레포 경로를 플러그인 경로보다 먼저 보지 않는다 — 근거 파일 §5 열린 질문(레포에서 고칠 때 `${CLAUDE_PLUGIN_ROOT}` 가 옛 설치본을 먼저 잡는다)은 qa-evaluator Step 8 순서를 따르고,
  어느 사본을 썼는지는 `RESOLVED:` 줄로 보인다. 그 줄은 howto-doc 보고(SK-04)와 howto-audit Phase 4 리포트 틀(SK-02 (d))에 싣는다
- 셋째 단계에 설치 복사본 `~/.claude/plugins/cache/*/howto-kit/*/` 를 넣지 않는다 — 버전 폴더가 여럿이면 고를 규칙이 없다(근거 파일 §5 열린 질문). 레포의 기존 순서가 `marketplaces` 를 보므로 그대로 따른다
- 러너를 새 파일로 나누지 않는다 — 나누면 CI 넘김 줄 · howto-kaizen 절차 · README 표가 하나씩 늘어난다. 기존 러너 한 파일에 더한다
- `references/provenance-notes.md` §9 · `docs/howto/procedure-standards.md` §4 에 ISO/IEC/IEEE 26514 용어 정의 · DITA 2.0 초안 변화를 적지 않는다 — 근거 파일이 「선택, 이번 범위 밖」 으로 적었고, 원장 항목(절차 작성 세부 조항)은 여전히 미확인이다. notes 다음 사이클 메모로
- howto-audit Phase 4 리포트 틀에 에이전트의 `[미검증]` 칸을 더하지 않는다 — 옛 표기에도 칸이 없던 기존 빈틈이고, SK-06 이 표기만 바꾼다. notes 다음 사이클 메모로

## 범위 경계

- 이 Phase 시작 HEAD: `f936019c3f017be3e1bcc92570d677ef8cc6521b`. 범위 상한은 개정 파일 `.harness/sprint-amendments-kaizen-0924-p17-howto-kit.md` 의
  `end_sha:` 마지막 값이다. 여러 Phase 가 같은 가지 `kaizen/2026-09-24` 에 동시에 커밋하므로 `HEAD` 로 재지 않는다
- 고치는 파일은 일곱이고 새 파일은 없다 — 아래 블록이 그 목록이다(`harness/README.md` §커밋 안전 훅 이 정한 범위 선언 자리). `.harness/` 쪽은 이 계약 · 개정 파일 · QA 피드백 ·
  `.harness/.meta/kaizen-0924/phase17-notes.md` · `.harness/.meta/kaizen-0924/phase17-review.md` 를 쓴다 — 슬러그를 나열하지 않고 AR-01 셋째 값 `verify_seal` 로 잰다.
  AR-01 다섯째 값이 이 블록과 측정 공통 정의의 `FILES` 가 같은지 잰다

```text
# sprint-scope
howto-kit/skills/howto-audit/SKILL.md
howto-kit/skills/howto-doc/SKILL.md
howto-kit/README.md
howto-kit/scripts/howto-gate.sh
howto-kit/evals/run-evals.sh
howto-kit/evals/evals.json
howto-kit/agents/howto-reviewer.md
.harness/
```

- **이 Phase 의 커밋 메시지에는 전부 `Co-Authored-By` 줄 바로 위에 서명 줄 `Kaizen-Phase: kaizen-0924-p17-howto-kit` 한 줄을 넣는다** (봉인 커밋 포함).
  AR-01 · ER-03 · SC-00 · DG-01 · DG-03 · DG-06 이 이 줄로 이 Phase 커밋을 가린다(`harness/references/contract-schema.md` §여러 주체가 한 가지에 커밋할 때 선택지 B).
  서명을 빠뜨린 커밋은 서명 줄 목록에 안 보이므로 AR-01 첫째 값과 ER-03 마지막 값은 경로로 직접 센다.
  FIX 가 커밋을 더할 때도 넣고, 개정 파일에 `end_sha:` 줄을 덧붙인다(옛 줄은 지우지 않는다). notes 커밋도 이 Phase 커밋이다 — notes 를 커밋한 뒤 그 sha 로
  `end_sha:` 줄을 하나 더 덧붙여 커밋한다
- 구현 커밋은 `git add -- <일곱> && git commit -o -- <일곱>` 한 번이다. 일곱이 전부 howto-kit 이라 `validate-post-kaizen.py` scope-isolation 에 걸리지 않는다(예행에서 한 커밋으로 확인).
  러너 · 게이트 스크립트는 git 모드 `100755` 를 그대로 둔다
- 측정이 기대는 제목 · 줄 머리는 이름을 바꾸지 않는다: `### Gotcha 5: ` · `### Gotcha 6: ` · `### Phase 2: 게이트 전수 실행` · `### Phase 4: 리포트` · `## Process` (howto-audit) ·
  `### Gotcha 1: ` · `### Gotcha 3: ` · `### Phase 4: 게이트 실행 (E3)` (howto-doc) · `## 결정론 게이트 G1~G6` · `## Evals` (README) · `HOWTO_VERBS=` 줄 머리(게이트 스크립트) ·
  `name:` 줄 셋 · 러너 대조가 깨뜨리는 자리(`ctl-runner.py` 의 옛 글 — 깨뜨릴 글이 없으면 `NEG_EDIT_FAIL` 이 찍혀 기대값과 달라진다) ·
  읽기만 하는 `harness/agents/qa-evaluator.md` Step 8 의 `find "$HOME/.claude/plugins/marketplaces" -maxdepth 4 -type f` 줄과 `harness/docs/guides/agent-design-guide.md` 의 `1. **분류 접미를 붙인 마커**` 줄
- 공유 파일(`.claude-plugin/marketplace.json` · `howto-kit/.claude-plugin/plugin.json` 버전 · 루트 `README.md` · 루트 `CLAUDE.md` · `docs/` HTML · 처리 배정표 · 감사 로그 ·
  실패 횟수 파일 · `.github/workflows/ci.yml` · `.harness/stale-values.yaml`)과 다른 Phase · 레포 전용 파일(`harness/` · `scripts/` · `.claude/skills/`)은 건드리지 않는다 — ER-03 마지막 값.
  러닝북 Phase 표가 이 Phase 에 `howto-kit/` · `docs/howto/` 를 줬고 `docs/howto/` 는 이번에 고칠 곳이 없다(AR-03). howto-kit README 는 킷 전용 문서라 고친다 —
  AUTO 구간은 스킬 · 에이전트 frontmatter 와 스크립트 둘째 줄 · `evals/` 파일 목록만 읽는데 그 셋이 그대로다(AP-04 · SK-09 · 새 파일 없음). 문서 사이트 재생성은 Final F2 몫이라 DG-06 에서 `docs-site-regen` 을 뺀다
- QA(`harness:qa-evaluator`)는 설치본이다 — 이 Phase 가 고치는 파일에 qa-evaluator 는 없다
- 사용자 승인(Step 5) 대체: 사용자가 「자동으로 끝까지 알아서 진행해 내 허락이 필요한건 코덱스로 리서치나 검토받고」라고 위임했다(세션
  `de8c7935-a5b6-4df5-9106-fafa73c288a0` 기록 queued_command `2026-09-24T04:04:16.964Z`). Codex 사용량 한도가 소진돼(오류 원문 「You've hit your usage limit … try
  again at 11:05 PM」, 2026-09-24) 독립 Claude 검토자(REVIEW 에이전트)가 대신한다. 이어 사용자가 「코덱스 대신에 그냥 너가 알아서 진행하라고」라고 명시했다(같은 세션
  기록 user `2026-09-24T11:54:58.940Z`). 검토 결과 파일: `.harness/.meta/kaizen-0924/phase17-review.md` — 1 회차 판정 `VERDICT: CHANGES`. 고칠 것 넷(C1 DG-04 종료 코드 ·
  C2 AR-01 셋째 값을 끝 판에서 · C3 `[미검증:ENV]` 네 칸 · C4 넘김 줄 `apt-get update`)과 권고 둘(R1 · R2)을 이 초안에 넣고 봉인 전 실측을 다시 했다.
  같은 파일 `## 2 회차` 의 최종 판정은 `VERDICT: APPROVE` 다 — 새 예행 저장소에서 26 개 ID 출력이 초안 표와 바이트까지 같았다. 2 회차 권고 R3(notes 절 이름을 ER-03 (c) 와 맞춤)은
  BUILD 가 봉인 전에 아래 「notes 에 함께 적는다」 줄에 넣었다 — 조건 줄이 아니라 봉인 값에 영향이 없다
- 판정 한계: 두 스킬을 부르는 LLM 이 `MISSING:` 에서 실제로 멈추는지 · 줄 수를 실제로 대조하는지는 결정론 측정이 없다 — 조건은 그 지시 문장이 정해진 절에 글자 그대로 있는지(SK-02 · SK-04)와
  블록 자체가 멈추는지(ER-04)를 잰다. 플러그인 치환(`plugin` 경우)은 Claude Code 가 하는 글자 치환을 측정이 흉내 낸 것이다 — 설치본으로 스킬을 불러 본 것은 아니다.
  CI 는 Final 이 줄을 넣은 뒤에야 돈다 — 러너는 이 맥의 dash · `/bin/sh`(bash 3.2.57) · bash 5.3 · zsh 5.9 로 돌렸고(DG-04) 우분투에서는 돌려 보지 못했다. SK-02 넷째 줄(`export -f`)은 이 맥 값이고, 산출물의 증거가 아니라 Gotcha 6 문장의 전제 확인이다(BUILD 가 무엇을 하든 값이 같다)
- 판정 근거: SK-01 · SK-03 · SK-05 · ER-04 — 끝 판 문서에서 블록을 뽑아(`gblk`) 네 경우를 만들고(`envs` — 킷 사본 셋 · `git init` 한 폴더 · 빈 `HOME`) zsh · bash 로 돌린 출력이다.
  러너와 따로 짠 측정이라 러너가 틀려도 이 값은 따로 떨어진다
- 판정 근거: SK-02 · SK-04 · SK-05 · SK-06 · SK-09 — 산출물이 문서 문장 자체라 정해진 절에 정해진 문장이 있는지가 판정이다. `sect` 가 코드 펜스를 건너뛰고 절을 자른다.
  시작 커밋 판에서 새 문장 0 을 봉인 전에 확인했고, 문장 하나만 지운 사본에서 그 값이 떨어졌다(`회귀 게이트` 절 `del.sh` 43 개 중 43)
- 판정 근거: SK-07 · SK-08 · RE-01 · DG-04 — 러너를 실제로 돌린 출력이다. SK-08 은 끝 판 킷 사본을 한 군데씩 깨뜨린 여덟(`ctl-runner.py`)과 zsh 대조 둘이다
- 판정 근거: ER-01 · ER-02 · AP-01 — 편집 전 판과 파일마다 비교한 더한 줄 계산이다. 근거 파일은 시작 커밋 판에서 읽는다(끝 판은 `.harness/` 안이라 이 Phase 가 고칠 수 있다)
- 판정 근거: DG-02 — 마크다운 네 파일마다 규칙별 경고 수를 편집 전 판과 비교한 출력이다. 더한 줄만 보지 않는다 — MD022 · MD032 · MD024 는 더한 줄 옆의 손대지 않은 줄에 붙는다(러닝북 측정 구멍 목록)
- 판정 근거: ER-03 · AR-01 · SC-00 · DG-01 · DG-03 · DG-06 — 커밋 기록과 봉인 검증 함수를 실제로 돌린 출력이다. 예행 저장소 변형 여섯이 양성 · 음성 대조다
- 판정 근거: AR-02 · AR-03 · RE-02 · AP-03 · AP-04 · DG-05 — 가리키는 자리 · 편집 전과 같아야 하는 곳 · 저장소 검사 도구를 실제로 돌린 출력이다. DG-05 의 옛 값은 등록부 값을 일곱 파일에서 직접 센 수다.
  `scripts/sync-docs.py howto-kit --check-only` 가 이 README 를 실제로 읽는지는 AUTO 표 한 칸을 바꾼 사본에서 `sync_rc=1` 로 확인했다
- 커버리지 해소: SK-01 ~ SK-09 · ER-04 · AR-02 · AR-03 · AP-04 · RE-01 · RE-02 · DG-04 — 산문의 파일 이름은 측정 `m <조건 ID>` 가 공통 정의의 변수(`$AU` · `$DO` · `$RD` · `$GS` · `$RUN` · `$EV` · `$RV`)로 연다
  (파일과 변수의 대응은 `common.sh` 머리). 토큰은 `m.sh` 의 같은 ID 갈래에 글자 그대로 있다. 러너 대조의 깨뜨릴 자리는 `ctl-runner.py` 의 같은 변형 갈래에 있다.
  `qa-evaluator.md` · `agent-design-guide.md` · `howto/SKILL.md` · `references/` · `docs/howto` · `fixtures` 는 `m.sh` 의 `RE-02)` · `AR-02)` · `AR-03)` 갈래가 경로를 적어 연다.
  `mock.py` · `rehearse.sh` · `common.sh` · `m.sh` · `rule-delta.sh` · `ctl-runner.py` · `del.sh` · `ctl.sh` · `runall.sh` 는 측정 도구 자체의 이름이다
- 커버리지 해소: ER-01 · ER-03 — `.harness/.meta/kaizen-0924/phase17-notes.md` · `.harness/.meta/evidence/phase17.md` 는 공통 정의의 `$NOTES` · `$EVID` 다. ER-03 의 넘김 경로
  (`.github/workflows/ci.yml` · `.claude/skills/howto-kaizen/SKILL.md` · `docs/howto-kit/overview.html` · `plugin.json`)는 `m.sh` `ER-03)` 갈래 `toks` 의 인자이고, 공유 경로는 `not_other` 의 인자다
- 커버리지 해소: AR-01 — `howto-kit` · `docs/howto` 는 `unsigned_on` 의 인자, `.harness/` 는 `scope` 블록 줄과 `verify_seal` 이 도는 폴더다. `harness/references/contract-schema.md` 는 셋째 값 권장 형태의 출처다
- 커버리지 해소: SK-02 · SK-03 · SK-05 · SK-08 · ER-01 · ER-04 · AR-02 · AR-03 · RE-02 — `/bin/sh` · `/bin/dash` 는 `m.sh` `SK-02)` 갈래의 인자, `pass-fcm-ios.md` 는 `common.sh` `runcase` 의 치환 값,
  `references/step-contract.md` 는 `ctl-runner.py` `n4` 갈래의 경로, `GATE="${CLAUDE_PLUGIN_ROOT}/scripts/howto-gate.sh"` 는 `m.sh` `RE-02)` 갈래가 줄 그대로 센다.
  `R/15/15/0/0/1` · `X/0/0/1/127/0` · `market:M/0/0/0/1/1` · `none:M/0/0/0/0/1` 같은 토큰은 대상이 아니라 `runcase` 출력 값이다. 산문의 `evals.json` 은 `$EV` 이고,
  ER-01 산문의 `.harness/` 는 근거 파일을 시작 커밋 판에서 읽는 까닭을 적은 말이다
- 검출기는 공백 든 코드 조각 안의 인자를 읽지 못한다 — 위 해소 줄이 전부 그 경우다
- 편집 전부터 있던 경고(마크다운 네 파일의 표 MD060 등)는 같은 수로 남으면 된다. DG-02 는 파일마다 규칙별 경고 수를 편집 전 판과 비교한다
- notes 에 함께 적는다: `GAP 분석` 절의 Phase 1 대조 표 · howto-kaizen 절차 대조 표, 하지 않기로 한 여섯과 이유, `## 미반영 키와 사유` 에 `provenance-notes.md` §9 ·
  `procedure-standards.md` §4 의 26514 용어 정의 · DITA 2.0 초안 변화 · 셋째 단계에 `cache` 를 넣지 않은 이유(ER-03 (c) 가 이 절에서 센다),
  `## 다음 사이클 메모` 에 howto-audit Phase 4 리포트의 미검증 칸 · 위 셋을 다음에 다시 볼지 · 러너 자체의 음성 대조를 킷 안에 둘지
- 기능 조건 18 · 전체 조건 줄 28
- 사용자가 할 일: 없음

## 회귀 게이트 — 측정 공통 정의와 봉인 전 실측

모든 조건의 측정은 아래 `common.sh` 와 `m.sh` 를 차례로 `.` 으로 읽은 **bash** 셸에서 돈다 — `common.sh` 는 bash 가 아니면 `NOT_BASH` 를 찍고 종료 코드 2 로 끝난다
(zsh 는 따옴표 없는 변수를 쪼개지 않고 배열 첨자가 1 부터다). `m` 은 도우미 함수와 두 판 폴더가 없으면 `HELPER_MISSING` · `SNAPSHOT_MISSING` 을 내고 멈춘다 —
그래서 조건마다 `type m` 하나로 정의 확인을 대신한다. 두 판 풀기가 끊기거나 일곱 파일 가운데 하나라도 어느 판에서 비면 `common.sh` 가 `SNAPSHOT_FAIL` 을 내고 종료 코드 2 로 끝난다.
셸이 끝나면 임시 폴더를 지운다. `END_UNRESOLVED` 가 찍히면 셸이 종료 코드 2 로 끝난다. `m` 의 종료 코드는 판정하지 않는다 — 판정은 출력 값으로 한다.
블록 · 러너 대조는 끝 판 `howto-kit/` 을 임시 폴더에 복사한 사본에서만 돈다 — 작업 폴더와 두 판 폴더는 바뀌지 않는다.
네 블록을 각 블록 첫 `#` 주석 줄(셔뱅 다음)의 이름 그대로 한 폴더에 저장하고 그 폴더를 `K` 에 넣는다. `rule-delta.sh` 옆에는 `node_modules` 를
`/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/de8c7935-a5b6-4df5-9106-fafa73c288a0/scratchpad/p1build/node_modules` 로 잇고
`cfg.markdownlint-cli2.jsonc` = `{ "config": { "MD013": false } }` 를 둔다 — 준비 단계 실측(2026-09-25): 그 자리의 `.bin/markdownlint-cli2 --version` 첫 줄이
`markdownlint-cli2 v0.23.2 (markdownlint v0.41.1)`. 없으면 그 폴더에서 `npm install --no-save markdownlint-cli2@0.23.2` 부터 돌린다.
그 밖의 준비 단계 실측(2026-09-25): `command -v bash` → `/opt/homebrew/bin/bash` (5.3) · `/bin/sh` 는 bash 3.2.57 · `/bin/dash` 있음 · `zsh` 5.9 · `shellcheck` 0.11.0 ·
`python3` · `shasum` · `git` 있음 · `env -u` 가 된다. `common.sh` 의 `R` 은 예행 저장소를 가리킬 때만 쓴다 — 비우면 작업 폴더다. 두 판을 `${TMPDIR:-/tmp}/p17m.XXXXXX` 에 푸니
`TMPDIR` 를 스크래치 폴더로 두고 읽는다.
예행 도구(스크래치 `kaizen/p17/`): `mock.py`(sha256 앞 16 자리 `d1eef64544f9fcbc` — 시작 커밋 판에 이 계약이 요구하는 편집을 적용한다. 러너 새 판은 `new/run-evals.sh`, 앞 16 자리 `47e5292a9e2b120c`) ·
`rehearse.sh`(시작 커밋에서 예행 저장소를 만들어 봉인 · 다른 Phase 커밋 · 구현 한 커밋 · `end_sha` · notes · `end_sha` 를 흉내 낸다. 변형 `base` · `unsigned-mine` · `unsigned-shared` ·
`signed-outside` · `cross-phase` · `seal-broken` · `wc-only`) · `runall.sh` · `del.sh`(문장 삭제 대조 — 조건이 재는 파일에서만 지운다) · `ctl.sh`(양성 · 음성 대조).

```bash
# common.sh — 측정 공통 정의. bash 로 읽는다 (zsh 는 배열 첨자가 1 부터이고 따옴표 없는 변수를 쪼개지 않는다)
[ -n "${BASH_VERSION:-}" ] || { echo "NOT_BASH — bash -c 안에서 다시 읽는다"; exit 2; }
export LC_ALL=C.UTF-8   # 번역투 정규식이 글자 단위로 돌아야 한다
cd "${R:-/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/kaizen-0924}" || exit 2
B=f936019c3f017be3e1bcc92570d677ef8cc6521b                  # 이 Phase 시작 HEAD
SIG='Kaizen-Phase: kaizen-0924-p17-howto-kit'
CF=.harness/sprint-contract-kaizen-0924-p17-howto-kit.md
AM=.harness/sprint-amendments-kaizen-0924-p17-howto-kit.md
NOTES=.harness/.meta/kaizen-0924/phase17-notes.md
EVID=.harness/.meta/evidence/phase17.md
END=$( [ -f "$AM" ] && sed -n 's/^end_sha:[[:space:]]*//p' "$AM" | tail -1 )
if [ -z "$END" ] || ! git rev-parse -q --verify "$END^{commit}" >/dev/null; then
  echo "END_UNRESOLVED — 측정을 멈춘다. HEAD 로 바꿔 재지 않는다"; exit 2
fi
: "${K:?도우미 폴더를 K 에 넣는다}"
AU=howto-kit/skills/howto-audit/SKILL.md
DO=howto-kit/skills/howto-doc/SKILL.md
RD=howto-kit/README.md
GS=howto-kit/scripts/howto-gate.sh
RUN=howto-kit/evals/run-evals.sh
EV=howto-kit/evals/evals.json
RV=howto-kit/agents/howto-reviewer.md
FILES=("$AU" "$DO" "$RD" "$GS" "$RUN" "$EV" "$RV")
MDF=("$AU" "$DO" "$RD" "$RV")           # 마크다운 검사 대상
T=$(mktemp -d "${TMPDIR:-/tmp}/p17m.XXXXXX") && T=$(cd "$T" && pwd -P) || exit 2
mkdir -p "$T/B" "$T/E"
trap 'rm -rf "$T"' EXIT
# 두 판을 풀어 둔 폴더에서 잰다 — 작업 폴더에 남은 다른 Phase 의 미커밋 변경이 끼지 않는다
# 풀기가 도중에 끊기면 0 을 기대하는 값이 통과로 읽힌다 — 여기서 멈춘다
git archive "$B" | tar -x -C "$T/B" && git archive "$END" | tar -x -C "$T/E" || { echo "SNAPSHOT_FAIL — 측정을 멈춘다"; exit 2; }
for f in "${FILES[@]}"; do [ -s "$T/E/$f" ] && [ -s "$T/B/$f" ] || { echo "SNAPSHOT_FAIL $f"; exit 2; }; done
# sect <파일> <제목 앞부분> — 그 제목부터 같은 깊이 이하의 다음 제목 전까지. 코드 펜스 안의 `#` 줄은 제목으로 보지 않는다
sect() { awk -v h="$2" '
  /^[[:space:]]*(```|~~~)/ { fence = !fence }
  !f && !fence && index($0, h) == 1 { f = 1; lvl = match($0, /[^#]/) - 1; print; next }
  f && !fence && /^#+ / { l = match($0, /[^#]/) - 1; if (l <= lvl) exit }
  f' "$1"; }
# gblk <파일> <제목 앞부분> — 그 제목 절 안의 첫 bash 코드 블록 본문 (펜스 줄 빼고)
gblk() { sect "$1" "$2" | awk '/^```bash$/{b=1; next} b&&/^```$/{exit} b'; }
# toks <글> <토큰…> — 토큰마다 글 안에서 그 토큰이 든 줄 수
toks() { local s="$1"; shift; for t in "$@"; do printf '%s ' "$(printf '%s\n' "$s" | grep -cF -- "$t")"; done; echo; }
# fmb <파일> — 첫 frontmatter 블록 본문
fmb() { awk 'NR==1&&/^---/{fm=1;next} fm&&/^---/{exit} fm' "$1"; }
# barefence <파일> — 언어 힌트 없는 여는 펜스 수 (여닫기를 번갈아 센다)
barefence() { awk '/^[[:space:]]*```/{ if (!o) { o = 1; if ($0 ~ /^[[:space:]]*```[[:space:]]*$/) n++ } else o = 0 } END{print n+0}' "$1"; }
url()   { grep -oE 'https?://[^ )>"`]+' | sed -E 's/[.,;:]+$//' | sort -u; }
added() { for f in "${FILES[@]}"; do git diff --no-index -U0 "$T/B/$f" "$T/E/$f"; done | grep '^+' | grep -v '^+++'; }
mine() { git log --format= --name-only "${1}..${2}" --grep="^${3}\$" | grep . | LC_ALL=C sort -u; }
unsigned_on() { _b=${1}; _u=${2}; _s=${3}; shift 3
  git log --format=%H "${_b}..${_u}" -- "$@" | while read -r _c; do git log -1 --format=%B "$_c" | grep -qxF "$_s" || echo "$_c"; done; }
# not_other <base> <상한> <서명> <경로…> — 경로를 건드린 구간 안 커밋 가운데 다른 Phase 서명이 없는 커밋 (0 줄이어야 한다)
not_other() { _b=${1}; _u=${2}; _s=${3}; shift 3
  git log --format=%H "${_b}..${_u}" -- "$@" | while read -r _c; do
    _m=$(git log -1 --format=%B "$_c")
    if printf '%s\n' "$_m" | grep -qE '^Kaizen-Phase: ' && ! printf '%s\n' "$_m" | grep -qxF "$_s"; then continue; fi
    echo "$_c"; done; }
my() { mine "$B" "$END" "$SIG"; }
# scope <계약> — `## 범위 경계` 절 안, 첫 줄이 `# sprint-scope` 인 text 블록의 경로 줄
scope() { awk '/^## /{s=$0} s ~ /^## 범위 경계/ && /^```text$/{b=1; n=0; next} b && /^```$/{b=0; next} b{n++; if (n==1 && $0 != "# sprint-scope") b=0; else if (n>1) print}' "$1"; }
fm_get() { awk -v k="^$2:[[:space:]]*" 'NR==1 && /^---[[:space:]]*$/ { fm=1; next } fm && /^---[[:space:]]*$/ { exit } fm && $0 ~ k { sub(k, "", $0); print; exit }' "$1" | sed -e "s/[[:space:]]*$//" -e "s/^['\"]//" -e "s/['\"]\$//"; }
sha256_16() { if command -v sha256sum >/dev/null 2>&1; then sha256sum; elif command -v shasum >/dev/null 2>&1; then shasum -a 256; else python3 -c 'import hashlib,sys; print(hashlib.sha256(sys.stdin.buffer.read()).hexdigest())'; fi | cut -c1-16; }
contract_digest() { grep -E '^- \[[ x]\] [A-Z]{2,}-[0-9]{2}' "$1" | sed -E 's/^- \[[ x]\]/- [ ]/' | sha256_16; }
verify_seal() { rec=$(fm_get "$1" conditions_digest); rec=${rec#sha256:}; if [ -z "$rec" ]; then echo "SEAL_ABSENT $1"; return 0; fi
  act=$(contract_digest "$1"); if [ "$rec" = "$act" ]; then echo "SEAL_OK $1"; else echo "SEAL_BROKEN $1 recorded=$rec actual=$act"; fi; }
# kit <이름> [판 폴더] — 그 판(기본 끝 판)의 howto-kit 을 $T/<이름>/howto-kit 에 복사하고 그 경로를 낸다 (대조는 사본에서만 돈다)
kit() { rm -rf "$T/$1"; mkdir -p "$T/$1"; cp -R "${2:-$T/E}/howto-kit" "$T/$1/" && printf '%s' "$T/$1/howto-kit"; }
# envs <판 폴더> — 게이트를 부르는 블록을 돌릴 네 경우를 $T/X 에 만든다. 픽스처 열다섯 전부를 docs 에 둔다
envs() { local X=$T/X; rm -rf "$X"; mkdir -p "$X/docs" "$X/work" "$X/home0" "$X/plug" "$X/repo" "$X/homem/.claude/plugins/marketplaces/mk" || return 2
  cp "$1"/howto-kit/evals/fixtures/*.md "$X/docs/" && cp -R "$1/howto-kit" "$X/plug/" && cp -R "$1/howto-kit" "$X/repo/" \
    && cp -R "$1/howto-kit" "$X/homem/.claude/plugins/marketplaces/mk/" && git -C "$X/repo" init -q || return 2; }
# runcase <블록 파일> <경우> — 블록을 그 경우에서 zsh · bash 로 돌려 `경우:첫 줄/### 줄/판정 줄/not found 줄/종료 코드/두 셸 같음` 을 낸다
#   첫 줄 — R: 그 경우에 기대하는 RESOLVED 경로 그대로 · M: `MISSING: howto-gate.sh tried=` 로 시작 · X: 그 밖
runcase() { local X=$T/X f=$T/X/run.sh cwd=$T/X/work home=$T/X/home0 want oz ob rz rb first c
  # 자리표시자 셋만 바꾼다 — 모르는 자리표시자가 남으면 블록이 깨져 X 로 나온다. plugin 은 치환된 모양을 글자로 흉내 낸다
  python3 - "$1" "$f" "$X" "$2" <<'PY' || return 2
import sys
src, dst, X, case = sys.argv[1:5]
s = open(src, encoding="utf-8").read()
s = s.replace("<대상>", '"%s/docs"' % X).replace("<생성한 문서>", '"%s/docs/pass-fcm-ios.md"' % X).replace("<절차 문서>", '"%s/docs/pass-fcm-ios.md"' % X)
if case == "plugin":
    s = s.replace("${CLAUDE_PLUGIN_ROOT}", X + "/plug/howto-kit")
open(dst, "w", encoding="utf-8").write(s)
PY
  case $2 in
    plugin) want="RESOLVED: $X/plug/howto-kit/scripts/howto-gate.sh" ;;
    repo)   cwd=$X/repo; want="RESOLVED: $X/repo/howto-kit/scripts/howto-gate.sh" ;;
    market) home=$X/homem; want="RESOLVED: $X/homem/.claude/plugins/marketplaces/mk/howto-kit/scripts/howto-gate.sh" ;;
    none)   want="" ;;
  esac
  oz=$(cd "$cwd" && env -u CLAUDE_PLUGIN_ROOT HOME="$home" GIT_CEILING_DIRECTORIES="$X" zsh "$f" 2>&1); rz=$?
  ob=$(cd "$cwd" && env -u CLAUDE_PLUGIN_ROOT HOME="$home" GIT_CEILING_DIRECTORIES="$X" bash "$f" 2>&1); rb=$?
  first=$(printf '%s\n' "$ob" | head -1)
  if [ -n "$want" ] && [ "$first" = "$want" ]; then c=R; elif [ "${first#MISSING: howto-gate.sh tried=}" != "$first" ]; then c=M; else c=X; fi
  printf '%s:%s/%s/%s/%s/%s/%s' "$2" "$c" "$(printf '%s\n' "$ob" | grep -c '^### ')" "$(printf '%s\n' "$ob" | grep -cE '^GATE_(PASS|FAIL|BLOCKED)')" \
    "$(printf '%s\n' "$ob" | grep -ci 'not found')" "$rb" "$( [ "$oz" = "$ob" ] && [ "$rz" = "$rb" ] && echo 1 || echo 0)"; }
# cases <블록 본문> <경우…> — 블록 본문을 파일로 두고 경우마다 runcase
cases() { local b=$1; shift; [ -n "$b" ] || { echo "BLOCK_EMPTY"; return 0; }; printf '%s\n' "$b" > "$T/X/blk.sh"
  for c in "$@"; do printf '%s ' "$(runcase "$T/X/blk.sh" "$c")"; done; echo; }
# sub <파일> <옛 글> <새 글> — 한 번만 나오는 글을 바꾼다. 없거나 여럿이면 NEG_EDIT_FAIL (변이가 안 걸린 채 "통과" 로 읽히지 않게)
sub() { python3 - "$1" "$2" "$3" <<'PY' || { echo "NEG_EDIT_FAIL $1"; return 1; }
import sys
p, o, n = sys.argv[1:4]
s = open(p, encoding="utf-8").read()
if s.count(o) != 1: sys.exit(1)
open(p, "w", encoding="utf-8").write(s.replace(o, n))
PY
}
# runk <킷 사본> — 러너를 bash 로 돌려 `rc=<종료코드> | FAIL 줄의 id(정렬) | EVALS 줄` 한 줄로 낸다
runk() { local o rc; o=$(bash "$1/evals/run-evals.sh" 2>&1); rc=$?
  printf 'rc=%s | %s | %s\n' "$rc" "$(printf '%s\n' "$o" | awk '/^FAIL  /{print $2}' | sort | paste -sd, -)" "$(printf '%s\n' "$o" | grep -E '^EVALS total=')"; }
K02='(을|를) ?(처리|관리)(합니다|한다)|에 대해서?|하도록 (합니다|한다)|에 의(해|하여)|되어 있(는 경우|을 때)|(표시|적용|호출|생성|반환)(됩니다|된다)'
NAMES='fit-?pal|fit_pal|flutter[-_]playwright|playwright-mcp|chrome-devtools-mcp'
```

```bash
# m.sh — 조건마다 재는 값을 한 줄씩 낸다. common.sh 를 읽은 bash 에서 `m <조건 ID>` 로 부른다
m() {
  local E=$T/E S f fn o rc KC V
  # 도우미가 하나라도 없으면 grep -c 가 조용히 0 을 낸다 — 멈춘다
  for fn in sect gblk toks fmb barefence url added mine unsigned_on not_other my scope fm_get verify_seal kit envs runcase cases sub runk; do
    type "$fn" >/dev/null 2>&1 || { echo "HELPER_MISSING $fn"; return 2; }; done
  [ -n "${T:-}" ] && [ -d "$T/B" ] && [ -d "$E" ] || { echo "SNAPSHOT_MISSING"; return 2; }
  V=${V_OVERRIDE:-$E}   # 블록을 잴 판 — 기본 끝 판. V_OVERRIDE=$T/B 면 시작 커밋 판
  case "$1" in
  SK-01)  # howto-audit Phase 2 블록 — 스크립트를 찾는 세 경우에서 파일마다 판정 줄이 나온다
    envs "$V" || { echo "ENV_FAIL"; return 2; }
    S=$(gblk "$V/$AU" '### Phase 2: 게이트 전수 실행')
    cases "$S" plugin repo market
    toks "$S" '. "${1}"; shift' 'sh "$GATE" {} +' '. howto-kit/scripts/howto-gate.sh' 'export -f' ;;
  SK-02)  # howto-audit Gotcha 6 · Phase 2 뒤 문단 · export -f 사실 확인
    toks "$(sect "$E/$AU" '### Gotcha 6: ')" '### Gotcha 6: 게이트 함수는 자식 셸로 넘어가지 않는다' \
      '셸 함수는 그 함수를 읽은 셸 안에서만 보인다.' \
      '`find -exec sh -c` 안에서 `howto_gate` 를 부르면 파일마다 `command not found` 만 나온다.' \
      '그래서 Phase 2 는 스크립트를 `sh -c` **안에서** 읽는다. `export -f` 로 넘기지 마라 — macOS 의' \
      '`sh` · bash 자식에게만 넘어가고 우분투의 `sh`(dash) · zsh 자식에게는 안 넘어간다.' \
      '스크립트 경로를 `howto-kit/scripts/` 로 시작하는 상대 경로로 쓰지 않는다. 킷을 플러그인으로 설치한' \
      '마켓플레이스 설치본 순으로 `test -f` 해서 처음 있는 경로를 쓴다.' \
      '실측(2026-09-24): 부모 셸에서 읽고 자식 셸에서 부르던 옛 Phase 2 블록을 시험 입력 15 개에 돌리면' \
      '`command not found` 가 15 줄, `GATE_PASS` · `GATE_FAIL` · `GATE_BLOCKED` 줄이 0 줄이었고 `find` 는'
    awk '/^### Gotcha 5: /{a=NR} /^### Gotcha 6: /{b=NR} /^## Process$/{c=NR} END{print (a&&b&&c&&a<b&&b<c)?1:0}' "$E/$AU"
    toks "$(sect "$E/$AU" '### Phase 2: 게이트 전수 실행')" \
      '파일별 출력을 그대로 수집한다. 첫 줄이 `MISSING:` 이면 게이트를 돌리지 못한 것이다 — 판정을 내지 말고' \
      '그 줄을 그대로 보고하고 멈춘다. `### <경로>` 줄 수와 `GATE_PASS` · `GATE_FAIL` · `GATE_BLOCKED` 줄 수가' \
      'Phase 1 의 파일 수와 셋 다 같아야 한다. 다르면 판정이 아니라 실행 오류다 (Gotcha 6).' \
      '`find` 의 종료 코드로 판정하지 마라 — `howto_gate` 는 판정과 무관하게 0 을 돌려준다.' \
      '`MISSING:` 으로 멈출 때는 `[미검증:ENV]` 에 네 칸을 붙인다 — 막는 것(그 `MISSING:` 줄) · 시도한 우회(`tried=` 의 세 곳) ·' \
      '통제 불가 사유(한 문장) · 재검증 명령(킷을 설치하거나 킷이 든 저장소 안에서 이 블록을 다시 돌린다).'
    for c in /bin/sh bash /bin/dash zsh; do bash -c 'howto_probe() { echo called; }; export -f howto_probe; '"$c"' -c howto_probe' >/dev/null 2>&1 \
      && printf '%s=called ' "$c" || printf '%s=no ' "$c"; done; echo
    toks "$(sect "$E/$AU" '### Phase 4: 리포트')" '스크립트:   <Phase 2 첫 줄의 RESOLVED: 줄 그대로>' ;;
  SK-03)  # howto-doc Gotcha 3 · Phase 4 블록
    envs "$V" || { echo "ENV_FAIL"; return 2; }
    S=$(gblk "$V/$DO" '### Gotcha 3: '); cases "$S" plugin repo market
    toks "$S" '. "${1}"; shift' 'sh "$GATE" {} +' '. howto-kit/scripts/howto-gate.sh'
    S=$(gblk "$V/$DO" '### Phase 4: 게이트 실행 (E3)'); cases "$S" plugin repo market
    toks "$S" '  . "$GATE"; howto_gate <생성한 문서>' '. howto-kit/scripts/howto-gate.sh' ;;
  SK-04)  # howto-doc 문단 — Gotcha 3 뒤 · Phase 4 뒤
    toks "$(sect "$E/$DO" '### Gotcha 3: ')" \
      '스크립트는 `sh -c` **안에서** 읽는다 — 셸 함수는 자식 셸로 넘어가지 않는다. 경로를 찾는 순서와' \
      '`MISSING:` 일 때 할 일은 Phase 4 와 같다. `### <경로>` 줄 수와 `GATE_PASS` · `GATE_FAIL` · `GATE_BLOCKED`' \
      '줄 수가 다르면 판정이 아니라 실행 오류다.'
    toks "$(sect "$E/$DO" '### Phase 4: 게이트 실행 (E3)')" \
      '`RESOLVED:` 줄과 출력 7 줄을 보고에 **그대로** 붙인다. `GATE_FAIL` 이면 고치고 다시 돌린다.' \
      '경로는 플러그인 설치 경로(`CLAUDE_PLUGIN_ROOT` 치환) → git 최상위 폴더의 `howto-kit/` → 마켓플레이스 설치본' \
      '순으로 찾는다. `howto-kit/scripts/` 로 시작하는 상대 경로는 킷을 플러그인으로 설치한 프로젝트에 없다.' \
      '첫 줄이 `MISSING:` 이면 게이트를 돌리지 못한 것이다 — 완료를 보고하지 말고 그 줄을 그대로 보고한다 (Gotcha 1).' \
      '`MISSING:` 으로 멈출 때는 `[미검증:ENV]` 에 네 칸을 붙인다 — 막는 것(그 `MISSING:` 줄) · 시도한 우회(`tried=` 의 세 곳) ·' \
      '통제 불가 사유(한 문장) · 재검증 명령(킷을 설치하거나 킷이 든 저장소 안에서 이 블록을 다시 돌린다).'
    echo "old_line=$(grep -cxF '. howto-kit/scripts/howto-gate.sh' "$E/$DO") old_find=$(grep -cxF "find docs -type f -name '*.md' -exec sh -c '" "$E/$DO")" ;;
  SK-05)  # README — 사용 블록 · 두 문단
    envs "$V" || { echo "ENV_FAIL"; return 2; }
    S=$(gblk "$V/$RD" '## 결정론 게이트 G1~G6'); cases "$S" plugin repo market
    toks "$(sect "$E/$RD" '## 결정론 게이트 G1~G6')" \
      '`howto-doc` Phase 4 와 같은 블록이다. 스크립트를 플러그인 설치 경로 → git 최상위 폴더의 `howto-kit/` →' \
      '마켓플레이스 설치본 순으로 찾고, 못 찾으면 `MISSING:` 을 찍는다. `find -exec sh -c` 로 여러 파일을 돌릴 때는' \
      '스크립트를 `sh -c` 안에서 읽는다 — 셸 함수는 자식 셸로 넘어가지 않는다 (`howto-audit` Gotcha 6).'
    toks "$(sect "$E/$RD" '## Evals')" \
      'evals 는 서술이 아니라 **실행 결과**로 판정한다. 모든 케이스를 zsh · bash · sh 세 셸에서 돌려 출력이' \
      '같은지까지 본다. 스킬 본문과 이 README 에서 게이트를 부르는 `bash` 블록도 그대로 뽑아 네 경우(플러그인 설치 경로 ·' \
      'git 최상위 폴더 · 마켓플레이스 설치본 · 스크립트 없음)에서 zsh · bash 로 돌린다. 블록 수는 `evals.json` 의' \
      '`gate_blocks` 와 같아야 한다.' '모든 케이스를 zsh 와 bash 양쪽에서'
    echo "old_line=$(grep -cxF '. howto-kit/scripts/howto-gate.sh' "$E/$RD")" ;;
  SK-06)  # howto-reviewer — 판정 불가 표기를 분류 접미와 네 칸으로 (Phase 1 가이드 대조)
    toks "$(cat "$E/$RV")" '판정 불가면 그 row 는 `[미검증:ENV]` 또는 `[미검증:INVALID]` 이고 PASS 가 아니다.' \
      '- 판정 불가는 분류 접미를 붙여 적는다. 출처 문서를 읽을 도구가 없는 것처럼 이 에이전트가 통제할 수 없는' \
      '부재면 `[미검증:ENV]` 에 네 칸 — 막는 것(시도한 도구와 그 결과) · 시도한 우회(하나 이상과 결과, 없으면' \
      '`없음 — 이유`) · 통제 불가 사유 · 재검증 명령(무엇이 있으면 어떻게 다시 판정하는지) — 을 붙인다.' \
      '네 칸을 못 채우면 `[미검증:INVALID]` 다. 접미 없는 표기는 쓰지 않는다 — 이 킷의 G2 가 절차 문서에서 막는' \
      '레거시 마커이고, `harness/docs/guides/agent-design-guide.md` §10 도 `INVALID` 로 읽는다.'
    echo "bare=$(grep -oF '[미검증]' "$E/$RV" | grep -c .)" ;;
  SK-07)  # 러너 — 끝 판 통과와 PASS 줄 이름 전부
    KC=$(kit k0); runk "$KC"
    o=$(bash "$KC/evals/run-evals.sh" 2>&1)
    python3 - "$E/$EV" <<'PY' > "$T/want.txt"
import json, sys
d = json.load(open(sys.argv[1], encoding="utf-8"))
ids = [c["id"] for c in d["cases"]] + ["blocks-declared"]
ids += ["%s:%s" % (b, c) for b in ("readme-md-1", "howto-audit-1", "howto-doc-1", "howto-doc-2") for c in ("plugin", "repo", "market", "none")]
print("\n".join(sorted(ids)))
PY
    printf '%s\n' "$o" | awk '/^PASS  /{print $2}' | sort > "$T/got.txt"
    echo "want=$(grep -c . "$T/want.txt") got=$(grep -c . "$T/got.txt") same=$(cmp -s "$T/want.txt" "$T/got.txt" && echo 1 || echo 0)" ;;
  SK-08)  # 러너 대조 — 끝 판 킷 사본을 한 군데씩 깨뜨린 여덟 (변형 정의는 ctl-runner.py)
    for v in n1 n2 n3 n4 n5 n6 n7 n8; do KC=$(kit "$v"); python3 "$K/ctl-runner.py" "$KC" "$v" >/dev/null || { echo "$v NEG_EDIT_FAIL"; continue; }
      printf '%s ' "$v"; runk "$KC"; done
    # n7 을 zsh 로 — 끝 판 러너는 틀린 assertion 을 잡고, 시작 커밋 판 러너는 zsh 에서 놓친다 (고친 것이 이 차이다)
    for P in "$E" "$T/B"; do KC=$(kit n7z "$P"); python3 "$K/ctl-runner.py" "$KC" n7 >/dev/null || { echo "n7z NEG_EDIT_FAIL"; continue; }
      o=$(zsh "$KC/evals/run-evals.sh" 2>&1); rc=$?
      echo "n7z_$( [ "$P" = "$E" ] && echo end || echo base ) rc=$rc | $(printf '%s\n' "$o" | awk '/^FAIL  /{print $2}' | sort | paste -sd, -) | $(printf '%s\n' "$o" | grep -E '^EVALS total=')"; done ;;
  SK-09)  # 게이트 스크립트 머리 주석 · evals.json 설명과 gate_blocks
    S=$(sed -n '1,/^HOWTO_VERBS=/p' "$E/$GS")
    toks "$S" '# 사용:  . <이 파일 경로>' '# 스킬은 이 파일을 플러그인 설치 경로 → git 최상위 폴더의 howto-kit/ → 마켓플레이스 설치본 순으로' \
      '# 찾는다 (howto-doc Phase 4). 셸 함수는 자식 셸로 넘어가지 않는다 — find -exec sh -c 로 부를 때는' \
      '# 이 파일을 sh -c 안에서 읽는다. export -f 는 dash · zsh 자식에게 넘어가지 않는다.' \
      '# zsh · bash · sh 에서 동일 출력 (evals/run-evals.sh 가 세 셸 출력을 대조한다). 글로빙을 쓰지 않는다' \
      '# 사용:  . howto-kit/scripts/howto-gate.sh'
    python3 - "$E/$EV" <<'PY'
import json, sys
d = json.load(open(sys.argv[1], encoding="utf-8"))
print("keys=%s gate_blocks=%d desc_three=%d" % (",".join(d), d.get("gate_blocks") == {"README.md": 1, "skills/howto-audit/SKILL.md": 1, "skills/howto-doc/SKILL.md": 2},
      "zsh · bash · sh 세 셸" in d.get("description", "")))
PY
    ;;
  ER-01)  # 새로 생긴 URL 이 근거 파일에 있다 — 근거 파일은 시작 커밋 판에서 읽는다 (끝 판은 .harness/ 안이라 이 Phase 가 고칠 수 있다)
    for f in "${FILES[@]}"; do comm -13 <(url < "$T/B/$f") <(url < "$E/$f"); done | sort -u | comm -23 - <(url < "$T/B/$EVID") | grep -c .
    if [ -f "$E/$NOTES" ]; then url < "$E/$NOTES" | comm -23 - <(url < "$T/B/$EVID") | grep -c .; else echo NOTES_MISSING; fi
    cmp -s "$T/B/$EVID" "$E/$EVID" && echo evid_same=1 || echo evid_same=0 ;;
  ER-02)  # 더한 줄의 번역투 6 종 · 앱 · 도구 서버 이름, 킷 전체의 앱 이름
    echo "added=$(added | grep -c .) k02=$(added | grep -cE "$K02") names=$(added | grep -ciE "$NAMES") kit_names=$(grep -rhiE "$NAMES" "$E/howto-kit" | grep -c .)" ;;
  ER-03)  # notes 문자열 · 넘김 · 미반영 사유 · 공유 파일과 다른 Phase 파일을 건드린 커밋
    git cat-file -e "$END:$NOTES" 2>/dev/null && echo notes_committed=1 || echo notes_committed=0
    toks "$(cat "$E/$NOTES" 2>/dev/null)" '`other-kits:P4`' '`other-kits:P3`' '## 바꾼 파일' '## 반영한 처리 배정표 키' '## 미반영 키와 사유' \
      '## 넘기는 것' '## changelog 한 단락' '## 킷 로그 한 단락' '## 다음 사이클 메모'
    # 넘김 · 미반영 사유는 그 절 안에서 센다 — 낱말은 다른 절에도 나와 넘김 줄을 빠뜨려도 1 이 된다
    toks "$(sect "$E/$NOTES" '## 넘기는 것' 2>/dev/null)" '.github/workflows/ci.yml' 'command -v zsh' 'apt-get update' 'sh howto-kit/evals/run-evals.sh' \
      '.claude/skills/howto-kaizen/SKILL.md' 'docs/howto-kit/overview.html' 'plugin.json'
    toks "$(sect "$E/$NOTES" '## 미반영 키와 사유' 2>/dev/null)" 'DITA 2.0' '26514' 'cache'
    not_other "$B" "$END" "$SIG" .claude-plugin/marketplace.json howto-kit/.claude-plugin/plugin.json README.md CLAUDE.md \
      .harness/.meta/orchestrator-audit-log.md .harness/.meta/kaizen-failure-count.yaml .claude/kaizen-input/insights-report.md \
      .github/workflows/ci.yml .harness/stale-values.yaml .claude/skills harness scripts docs/howto-kit docs/index.html | grep -c . ;;
  ER-04)  # 스크립트를 어디서도 못 찾으면 네 블록 모두 MISSING: 을 찍고 0 이 아닌 코드로 멈춘다 — 게이트를 부르지 않는다
    envs "$V" || { echo "ENV_FAIL"; return 2; }
    for S in "$(gblk "$V/$AU" '### Phase 2: 게이트 전수 실행')" "$(gblk "$V/$DO" '### Gotcha 3: ')" "$(gblk "$V/$DO" '### Phase 4: 게이트 실행 (E3)')" "$(gblk "$V/$RD" '## 결정론 게이트 G1~G6')"; do
      cases "$S" none | tr -d '\n'
      printf '%s\n' "$S" | sed -e "s#<대상>#\"$T/X/docs\"#g" -e "s#<생성한 문서>#x.md#g" -e "s#<절차 문서>#x.md#g" > "$T/X/run.sh"
      o=$(cd "$T/X/work" && env -u CLAUDE_PLUGIN_ROOT HOME="$T/X/home0" GIT_CEILING_DIRECTORIES="$T/X" bash "$T/X/run.sh" 2>&1 | head -1)
      [ "$o" = "MISSING: howto-gate.sh tried=/scripts · /howto-kit/scripts · $T/X/home0/.claude/plugins/marketplaces" ] && echo " exact=1" || echo " exact=0"; done ;;
  AR-01)  # 허용 경로 · 서명 · 봉인 · 범위 선언 블록
    unsigned_on "$B" "$END" "$SIG" howto-kit docs/howto | grep -c .
    echo "$(my | grep -v '^\.harness/' | grep -vxF -f <(printf '%s\n' "${FILES[@]}") | grep -c .) $(my | grep -cxF -f <(printf '%s\n' "${FILES[@]}"))"
    find "$E/.harness" -type f -name 'sprint-contract*.md' -print0 | while IFS= read -r -d '' f; do verify_seal "$f"; done \
      | awk '$1=="SEAL_BROKEN"{print $2}' | sed "s#^$E/##" | sort -u | comm -12 - <( { my; echo "$CF"; } | sort -u) | grep -c .
    verify_seal "$E/$CF" | cut -d' ' -f1
    diff <(scope "$E/$CF" | grep -vxF '.harness/' | sort) <(printf '%s\n' "${FILES[@]}" | sort) >/dev/null && echo "scope_same=1" || echo "scope_same=0"
    scope "$E/$CF" | grep -cxF '.harness/' ;;
  AR-02)  # 새 문장이 가리키는 자리가 실제로 있다
    echo "$(grep -cF '(`howto-audit` Gotcha 6)' "$E/$RD") $(grep -cF '(Gotcha 6)' "$E/$AU") $(grep -c '^### Gotcha 6: ' "$E/$AU") | $(grep -cF '(howto-doc Phase 4)' "$E/$GS") $(grep -cF '`howto-doc` Phase 4 와 같은 블록이다' "$E/$RD") $(grep -cF 'Phase 4 와 같다' "$E/$DO") $(grep -cx '### Phase 4: 게이트 실행 (E3)' "$E/$DO") | $(grep -cF '(Gotcha 1).' "$E/$DO") $(grep -c '^### Gotcha 1: ' "$E/$DO") | $(grep -cF '`harness/docs/guides/agent-design-guide.md` §10' "$E/$RV") $(grep -cF '1. **분류 접미를 붙인 마커**' "$E/harness/docs/guides/agent-design-guide.md") | $(python3 -c 'import json,os,sys; d=json.load(open(sys.argv[1],encoding="utf-8")); print(sum(os.path.isfile(os.path.join(sys.argv[2],k)) for k in d.get("gate_blocks",{})), len(d.get("gate_blocks",{})))' "$E/$EV" "$E/howto-kit")" ;;
  AR-03)  # 손대지 않을 곳 — 게이트 판정 코드 · 평가 사례 · 픽스처 · 다른 스킬 · references
    f=$GS; diff <(sed -n '/^HOWTO_VERBS=/,$p' "$T/B/$f") <(sed -n '/^HOWTO_VERBS=/,$p' "$E/$f") >/dev/null && [ -n "$(sed -n '/^HOWTO_VERBS=/,$p' "$E/$f")" ] && printf '1 ' || printf '0 '
    python3 -c 'import json,sys; a=json.load(open(sys.argv[1],encoding="utf-8")); b=json.load(open(sys.argv[2],encoding="utf-8")); print(int(a["cases"]==b["cases"] and a["runner"]==b["runner"] and a["kit"]==b["kit"]), end=" ")' "$T/B/$EV" "$E/$EV"
    diff -r "$T/B/howto-kit/evals/fixtures" "$E/howto-kit/evals/fixtures" >/dev/null && printf '1 ' || printf '0 '
    diff -r "$T/B/howto-kit/references" "$E/howto-kit/references" >/dev/null && printf '1 ' || printf '0 '
    cmp -s "$T/B/howto-kit/skills/howto/SKILL.md" "$E/howto-kit/skills/howto/SKILL.md" && printf '1 ' || printf '0 '
    diff -r "$T/B/docs/howto" "$E/docs/howto" >/dev/null && echo 1 || echo 0 ;;
  AP-01)  # 더한 줄에 이 킷 플러그인 버전 값
    f=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["version"])' "$E/howto-kit/.claude-plugin/plugin.json")
    echo "version=$f $(added | grep -cF -- "$f")" ;;
  AP-03)  # 언어 힌트 없는 여는 펜스 — 마크다운 네 파일
    for f in "${MDF[@]}"; do printf '%s ' "$(barefence "$E/$f")"; done; echo ;;
  AP-04)  # SKILL.md 둘 · 에이전트 frontmatter 가 편집 전과 같고 name 줄이 하나씩
    for f in "$AU" "$DO" "$RV"; do printf '%s ' "$(diff <(fmb "$T/B/$f") <(fmb "$E/$f") >/dev/null && echo 1 || echo 0)"; done
    echo "| $(fmb "$E/$AU" | grep -cx 'name: howto-audit') $(fmb "$E/$DO" | grep -cx 'name: howto-doc') $(fmb "$E/$RV" | grep -cx 'name: howto-reviewer')" ;;
  RE-01)  # 러너가 자기 위치 기준으로 돈다 — 레포 밖 폴더에서 절대 경로로 불러도 같은 결과
    o=$(cd / && bash "$E/$RUN" 2>&1); echo "rc=$? $(printf '%s\n' "$o" | tail -2 | paste -sd' ' -)" ;;
  RE-02)  # 경로 찾기는 qa-evaluator Step 8 과 같은 세 단계이고 네 블록의 앞 여섯 줄이 같다. howto_gate 정의는 게이트 스크립트 하나
    for S in "$(gblk "$E/$AU" '### Phase 2: 게이트 전수 실행')" "$(gblk "$E/$DO" '### Gotcha 3: ')" "$(gblk "$E/$DO" '### Phase 4: 게이트 실행 (E3)')" "$(gblk "$E/$RD" '## 결정론 게이트 G1~G6')"; do
      printf '%s\n' "$S" | head -6 | sha256_16; done | sort -u | grep -c .
    S=$(gblk "$E/$AU" '### Phase 2: 게이트 전수 실행' | head -4)
    echo "$(printf '%s\n' "$S" | sed -n 1p | grep -cxF 'GATE="${CLAUDE_PLUGIN_ROOT}/scripts/howto-gate.sh"') $(printf '%s\n' "$S" | sed -n 2p | grep -cF 'git rev-parse --show-toplevel') $(printf '%s\n' "$S" | sed -n 3p | grep -cF 'find "$HOME/.claude/plugins/marketplaces" -maxdepth 4 -type f') | qa=$(grep -cF 'find "$HOME/.claude/plugins/marketplaces" -maxdepth 4 -type f' "$E/harness/agents/qa-evaluator.md") | $(grep -rlE '^howto_gate\(\) \{' "$E/howto-kit" | sed "s#^$E/##" | paste -sd' ' -)" ;;
  DG-02)  # markdownlint — 파일마다 규칙별 경고 수를 편집 전 판과 비교. 더한 줄만 보면 옆 줄에 붙는 MD022 · MD032 · MD024 를 놓친다
    for f in "${MDF[@]}"; do L=$(printf '%s' "$f" | tr '/' '_'); cp "$E/$f" "$T/$L.md"; cp "$T/B/$f" "$T/$L.0.md"
      printf '%s ' "$f"; bash "$K/rule-delta.sh" "$T/$L.0.md" "$T/$L.md"; done ;;
  DG-04)  # 러너를 네 해석기로 — 종료 코드 · stderr · 출력이 같은지, shellcheck · 문법 검사 (러너 · 게이트 스크립트)
    for f in /bin/dash /bin/sh bash zsh; do "$f" "$E/$RUN" > "$T/out.$(basename "$f")" 2> "$T/err.$(basename "$f")"; printf '%s rc=%s err=%s same=%s | ' "$f" "$?" "$(grep -c . "$T/err.$(basename "$f")")" "$(cmp -s "$T/out.dash" "$T/out.$(basename "$f")" && echo 1 || echo 0)"; done; echo
    # 종료 코드는 printf 전에 받는다 — 인자의 명령 치환이 먼저 풀려 $? 가 basename 의 0 이 된다
    for f in "$RUN" "$GS"; do o=$(shellcheck -s sh "$E/$f" 2>&1); rc=$?; printf '%s shellcheck rc=%s lines=%s ' "$(basename "$f")" "$rc" "$(printf '%s' "$o" | grep -c .)"; done
    for f in /bin/dash /bin/sh bash zsh; do "$f" -n "$E/$RUN" 2>/dev/null; rc=$?; printf 'n_%s=%s ' "$(basename "$f")" "$rc"; done; echo ;;
  DG-05)  # 저장소 검사 — $END 판을 git 저장소로 만든 사본에서. 옛 값은 일곱 파일에서 직접 센다
    local G=$T/G; rm -rf "$G"; cp -R "$E" "$G"
    git -C "$G" init -q && git -C "$G" add -A && git -C "$G" -c user.name=m -c user.email=m@m commit -qm snap || return 2
    ( cd "$G" && python3 scripts/validate-plugin.py howto-kit > "$T/vp.txt" 2>&1; echo $? > "$T/vp.rc" )
    echo "$(grep -cE '^  V([1-9]|10) ' "$T/vp.txt") $(grep -E '^  V([1-9]|10) ' "$T/vp.txt" | grep -cvE -- '— (OK|SKIP \(no templates/\))$') rc=$(cat "$T/vp.rc")"
    ( cd "$G" && python3 scripts/sync-docs.py howto-kit --check-only > "$T/sd.txt" 2>&1; echo "sync_rc=$? $(grep -c 'howto-kit/README.md: 동기화됨' "$T/sd.txt")" )
    python3 - "$E/.harness/stale-values.yaml" "${FILES[@]/#/$E/}" <<'PY'
import sys, yaml
vals = [v["old"] for v in yaml.safe_load(open(sys.argv[1], encoding="utf-8"))["values"]]
hits = sum(open(p, encoding="utf-8").read().count(o) for p in sys.argv[2:] for o in vals)
print("stale_old=%d files=%d hits=%d" % (len(vals), len(sys.argv[2:]), hits))
PY
    ;;
  DG-06)  # 사이클 검사 — 이 Phase 몫 줄만 본다. docs-site-regen 은 Final F2 몫
    python3 scripts/validate-post-kaizen.py --since "$B" --verbose > "$T/vpk.txt" 2>&1
    grep -E '\] . (scope-isolation|doc-contracts): ' "$T/vpk.txt" | awk '{print $5, $2}'
    python3 scripts/validate-doc-contracts.py -v 2>&1 | awk -F' → ' '/^ *검사: /{a=$1; sub(/^ *검사: /,"",a); sub(/:[0-9]+$/,"",a); print a; print $2}' | sort -u > "$T/dc.txt"
    echo "doc_checked=$(grep -c . "$T/dc.txt") doc_mine=$(comm -12 "$T/dc.txt" <(my) | grep -c .)"
    awk '/ scope-isolation: /{f=1;next} /^\[ /{f=0} f&&/^ +[0-9a-f]{7,40}$/{print $1}' "$T/vpk.txt" > "$T/viol.txt"
    echo "violators=$(grep -c . "$T/viol.txt") mine=$(while read -r c; do git log -1 --format=%B "$c" | grep -qxF "$SIG" && echo "$c"; done < "$T/viol.txt" | grep -c .)" ;;
  NA)  # N/A 줄(SC-00 · DG-01 · DG-03) 의 사유 측정 — 서명 커밋이 건드린 경로
    echo "SC-00=$(my | grep -cE '^(scripts/release\.sh|\.claude-plugin/marketplace\.json|[^/]+/\.claude-plugin/plugin\.json)$') DG-01=$(my | grep -c '^scripts/release.sh$')" ;;
  *) echo "UNKNOWN $1"; return 2 ;;
  esac
}
```

```bash
#!/usr/bin/env bash
# rule-delta.sh <옛 파일> <새 파일> — 규칙별 경고 수를 두 판에서 세어 늘어난 규칙만 낸다
# 더한 줄만 보면 손대지 않은 옆 줄에 붙는 경고(MD022 · MD032 · MD024)를 놓친다 (러닝북 — Phase 7 · 8 · 9 · 11 실측)
# 린터가 안 돌면 0 이 조용히 나온다 — 돌았다는 줄(Linting: 1 file)이 없으면 멈춘다
set -u
DIR=$(cd "$(dirname "$0")" && pwd)
cnt() { local out
  out=$("$DIR/node_modules/.bin/markdownlint-cli2" --config "$DIR/cfg.markdownlint-cli2.jsonc" "$1" 2>&1)
  printf '%s\n' "$out" | grep -q '^Linting: 1 file' || return 2
  printf '%s\n' "$out" | sed -nE 's/^[^ ]*:[0-9]+(:[0-9]+)? (error|warning) (MD[0-9]+)\/.*/\3/p' | sort | uniq -c | awk '{print $2, $1}'; }
O=$(cnt "$1") || { echo "LINT_NOT_RUN $1"; exit 2; }
N=$(cnt "$2") || { echo "LINT_NOT_RUN $2"; exit 2; }
UP=$(join -a 2 -e 0 -o 0,1.2,2.2 <(printf '%s\n' "$O" | grep . | sort) <(printf '%s\n' "$N" | grep . | sort) | awk '$3 > $2 {printf "%s%s:%s>%s", (n++ ? " " : ""), $1, $2, $3}')
echo "rules_up=$(printf '%s' "$UP" | wc -w | tr -d ' ')${UP:+ $UP}"
```

```python
# ctl-runner.py <킷 사본> <변형> — 러너 음성 대조용 변형을 킷 사본에 적용한다
import json, os, re, sys
kit, v = sys.argv[1], sys.argv[2]
def sub(rel, o, n, cnt=1):
    p = os.path.join(kit, rel); s = open(p, encoding="utf-8").read()
    if s.count(o) != cnt: sys.exit("NEG_EDIT_FAIL %s %s" % (v, rel))
    open(p, "w", encoding="utf-8").write(s.replace(o, n))
AU = "skills/howto-audit/SKILL.md"; DO = "skills/howto-doc/SKILL.md"
old_audit = '''```bash
. howto-kit/scripts/howto-gate.sh
find <대상> -type f -name '*.md' -exec sh -c '
  for f in "$@"; do echo "### $f"; howto_gate "$f"; done
' sh {} +
```'''
if v == "n1":   # 옛 Phase 2 블록으로 되돌림
    p = os.path.join(kit, AU); s = open(p, encoding="utf-8").read()
    s2 = re.sub(r"(### Phase 2: 게이트 전수 실행\n\n)```bash\n.*?\n```", lambda m: m.group(1) + old_audit, s, count=1, flags=re.S)
    if s2 == s: sys.exit("NEG_EDIT_FAIL n1")
    open(p, "w", encoding="utf-8").write(s2)
elif v == "n2": # 부모에서 읽고 export -f 로 넘김
    p = os.path.join(kit, AU); s = open(p, encoding="utf-8").read()
    o = '''  echo "RESOLVED: $GATE"
  find <대상> -type f -name '*.md' -exec sh -c '
    . "${1}"; shift
'''
    n = '''  echo "RESOLVED: $GATE"
  . "$GATE"; export -f howto_gate
  find <대상> -type f -name '*.md' -exec sh -c '
    shift
'''
    if s.count(o) != 1: sys.exit("NEG_EDIT_FAIL n2")
    open(p, "w", encoding="utf-8").write(s.replace(o, n))
elif v == "n3": # README 블록을 지움
    p = os.path.join(kit, "README.md"); s = open(p, encoding="utf-8").read()
    s2 = re.sub(r"```bash\nGATE=.*?\n```\n", "", s, count=1, flags=re.S)
    if s2 == s: sys.exit("NEG_EDIT_FAIL n3")
    open(p, "w", encoding="utf-8").write(s2)
elif v == "n4": # 등록 안 된 블록을 references 에 더함
    p = os.path.join(kit, "README.md"); s = open(p, encoding="utf-8").read()
    m = re.search(r"```bash\nGATE=.*?\n```\n", s, flags=re.S)
    if not m: sys.exit("NEG_EDIT_FAIL n4")
    blk = m.group(0)
    with open(os.path.join(kit, "references/step-contract.md"), "a", encoding="utf-8") as f: f.write("\n" + blk)
elif v == "n5": # Phase 4 블록의 마켓플레이스 경로를 틀리게
    p = os.path.join(kit, DO); s = open(p, encoding="utf-8").read()
    i = s.find("### Phase 4: 게이트 실행 (E3)")
    j = s.find('"$HOME/.claude/plugins/marketplaces" -maxdepth 4', i)
    if i < 0 or j < 0: sys.exit("NEG_EDIT_FAIL n5")
    s = s[:j] + '"$HOME/.claude/plugins/marketplace" -maxdepth 4' + s[j + len('"$HOME/.claude/plugins/marketplaces" -maxdepth 4'):]
    open(p, "w", encoding="utf-8").write(s)
elif v == "n6": # Gotcha 3 블록의 MISSING 갈래에서 false 를 지움
    p = os.path.join(kit, DO); s = open(p, encoding="utf-8").read()
    i = s.find("### Gotcha 3:"); j = s.find("  false\nfi\n", i)
    if i < 0 or j < 0: sys.exit("NEG_EDIT_FAIL n6")
    s = s[:j] + "fi\n" + s[j + len("  false\nfi\n"):]
    open(p, "w", encoding="utf-8").write(s)
elif v == "n7": # 평가 사례 assertion 하나를 틀리게
    p = os.path.join(kit, "evals/evals.json"); d = json.load(open(p, encoding="utf-8"))
    c = [x for x in d["cases"] if x["id"] == "E2-granularity-terminal-action"][0]
    c["assertions"] = ["G5_TERMINAL FAIL", "nonterminal=99"]
    open(p, "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False, indent=2) + "\n")
elif v == "n8": # sh 에서만 한 줄 더 내는 게이트
    sub("scripts/howto-gate.sh", '''howto_gate() {
  g=$1
''', '''howto_gate() {
  g=$1
  [ "$0" = sh ] && echo SH_ONLY
''')
else:
    sys.exit("UNKNOWN " + v)
print("applied " + v)
```

### 봉인 전 실측 — 예행 판 · 시작 커밋 판

예행 판은 이 계약 초안을 봉인해 커밋하고 `mock.py` 를 적용한 구현 커밋 · 다른 Phase 커밋 · notes 모의본까지 올린 예행 저장소(변형 없음)다. 시작 커밋 판은 `end_sha` 를 시작 커밋으로 둔
예행 저장소다. 블록 조건의 `경우:첫 줄/### 줄/판정 줄/not found 줄/종료 코드/두 셸 같음` 에서 첫 줄 `R` 은 그 경우에 기대하는 `RESOLVED:` 경로 그대로, `M` 은 `MISSING: howto-gate.sh tried=` 로 시작, `X` 는 그 밖이다.

값은 `m <조건 ID>` 출력 그대로다. 여러 줄은 ` ⏎ ` 로 이었다. 검토(phase17-review.md) 반영 뒤 2026-09-25 에 다시 돈 값이다 — 예행 판 전체 출력은 스크래치 `kaizen/p17/out-final-v2.txt`,
시작 커밋 판은 `out-base-v2.txt`, 예행 변형은 `out-variants-v2.txt` · `out-cross-v2.txt`, 대조는 `out-ctl-v2.txt` · `out-del-v2.txt` 에 있다.

```text
조건    예행 판                                                          시작 커밋 판
SK-01   plugin:R/15/15/0/0/1 repo:R/15/15/0/0/1 market:R/15/15/0/0/1 ⏎ 1 1 0 0
                                                                         plugin:X/15/0/15/1/0 repo:X/15/0/15/1/1 market:X/15/0/15/1/0 ⏎ 0 0 1 0
SK-02   1 1 1 1 1 1 1 1 1 ⏎ 1 ⏎ 1 1 1 1 1 1 ⏎ /bin/sh=called bash=called /bin/dash=no zsh=no ⏎ 1
                                                                         0 0 0 0 0 0 0 0 0 ⏎ 0 ⏎ 0 0 0 0 0 0 ⏎ (같은 넷째 줄) ⏎ 0
SK-03   plugin:R/15/15/0/0/1 repo:R/15/15/0/0/1 market:R/15/15/0/0/1 ⏎ 1 1 0 ⏎ plugin:R/0/1/0/0/1 repo:R/0/1/0/0/1 market:R/0/1/0/0/1 ⏎ 1 0
                                                                         plugin:X/0/0/0/1/1 repo:X/0/0/0/1/1 market:X/0/0/0/1/1 ⏎ 0 0 1 ⏎ plugin:X/0/0/1/127/0 repo:X/0/1/0/0/1 market:X/0/0/1/127/0 ⏎ 0 1
SK-04   1 1 1 ⏎ 1 1 1 1 1 1 ⏎ old_line=0 old_find=0                       0 0 0 ⏎ 0 0 0 0 0 0 ⏎ old_line=1 old_find=1
SK-05   plugin:R/0/1/0/0/1 repo:R/0/1/0/0/1 market:R/0/1/0/0/1 ⏎ 1 1 1 ⏎ 1 1 1 1 0 ⏎ old_line=0
                                                                         plugin:X/0/0/1/127/0 repo:X/0/1/0/0/1 market:X/0/0/1/127/0 ⏎ 0 0 0 ⏎ 0 0 0 0 1 ⏎ old_line=1
SK-06   1 1 1 1 1 1 ⏎ bare=0                                              0 0 0 0 0 0 ⏎ bare=2
SK-07   rc=0 |  | EVALS total=33 pass=33 fail=0 ⏎ want=33 got=33 same=1   rc=0 |  | EVALS total=16 pass=16 fail=0 ⏎ want=33 got=16 same=0
SK-08   조건 줄의 열 줄과 글자 그대로 같다 (n1 ~ n8 · n7z_end · n7z_base)
                                                                         n1 ~ n6 NEG_EDIT_FAIL (깨뜨릴 블록이 없다) ⏎ n7 rc=1 | E2-granularity-terminal-action | EVALS total=16 pass=15 fail=1
                                                                         ⏎ n8 rc=0 |  | EVALS total=16 pass=16 fail=0 (옛 러너는 sh 를 재지 않는다) ⏎ n7z_end · n7z_base 둘 다 rc=0 |  | EVALS total=16 pass=16 fail=0 (옛 러너 · zsh)
SK-09   1 1 1 1 1 0 ⏎ keys=kit,description,runner,gate_blocks,cases gate_blocks=1 desc_three=1
                                                                         0 0 0 0 0 1 ⏎ keys=kit,description,runner,cases gate_blocks=0 desc_three=0
ER-01   0 ⏎ 0 ⏎ evid_same=1                                               0 ⏎ NOTES_MISSING ⏎ evid_same=1
ER-02   added=256 k02=0 names=0 kit_names=0                               added=0 k02=0 names=0 kit_names=0
ER-03   notes_committed=1 ⏎ 1×9 ⏎ 1×7 ⏎ 1 1 1 ⏎ 0                          notes_committed=0 ⏎ 0×9 ⏎ 0×7 ⏎ 0 0 0 ⏎ 0
ER-04   none:M/0/0/0/1/1  exact=1 (네 줄)                                  none:X/15/0/15/1/0  exact=0 ⏎ none:X/0/0/0/1/1  exact=0 ⏎ none:X/0/0/1/127/0  exact=0 (두 줄)
AR-01   0 ⏎ 0 7 ⏎ 0 ⏎ SEAL_OK ⏎ scope_same=1 ⏎ 1                           0 ⏎ 0 0 ⏎ 0 ⏎ SEAL_ABSENT ⏎ scope_same=0 ⏎ 0 (끝 판에 계약이 없다)
AR-02   1 1 1 | 1 1 1 1 | 1 1 | 1 1 | 3 3
AR-03   1 1 1 1 1 1                                                       1 1 1 1 1 1
AP-01   version=0.2.1 0
AP-03   0 0 0 0
AP-04   1 1 1 | 1 1 1
RE-01   rc=0 EVALS total=33 pass=33 fail=0 EVALS_PASS
RE-02   1 ⏎ 1 1 1 | qa=2 | howto-kit/scripts/howto-gate.sh
DG-02   rules_up=0 (네 파일)
DG-04   /bin/dash rc=0 err=0 same=1 | /bin/sh rc=0 err=0 same=1 | bash rc=0 err=0 same=1 | zsh rc=0 err=0 same=1 |
        ⏎ run-evals.sh shellcheck rc=0 lines=0 howto-gate.sh shellcheck rc=0 lines=0 n_dash=0 n_sh=0 n_bash=0 n_zsh=0
DG-05   10 0 rc=0 ⏎ sync_rc=0 1 ⏎ stale_old=15 files=7 hits=0            10 0 rc=0 ⏎ sync_rc=0 1 ⏎ stale_old=15 files=7 hits=0 (howto-kaizen Step 1 비교 기준값)
DG-06   scope-isolation: PASS ⏎ doc-contracts: PASS ⏎ doc_checked=2 doc_mine=0 ⏎ violators=0 mine=0
NA      SC-00=0 DG-01=0                                                   SC-00=0 DG-01=0
```

양성 · 음성 대조 (끝 판 사본을 한 군데씩 깨뜨림 — `ctl.sh`, 예행 변형 — `rehearse.sh`):

```text
ER-04   howto-audit 블록 MISSING 갈래의 false 를 지움           → 첫 줄 none:M/0/0/0/0/1  exact=1 (나머지 셋 그대로)
SK-03   howto-doc Gotcha 3 블록 셋째 단계 -maxdepth 4 → 1        → 첫 줄 ... market:M/0/0/0/1/1
ER-01   README 에 근거 파일에 없는 URL 한 줄                      → 1 ⏎ 0 ⏎ evid_same=1
ER-02   reviewer 끝에 「이 값에 대해 적는다」 · 「fit-pal 앱」     → added=257 k02=1 · names=1 kit_names=1
AR-02   howto-audit Gotcha 6 제목을 바꿈                          → 1 1 0 | 1 1 1 1 | 1 1 | 1 1 | 3 3
AR-03   게이트 회피 표현 한 글자 · evals.json 사례 id 하나         → 0 1 1 1 1 1 · 1 0 1 1 1 1
AP-01   reviewer 끝에 0.2.1                                        → version=0.2.1 1
AP-03   reviewer 끝에 언어 힌트 없는 펜스                          → 0 0 0 1
AP-04   howto-doc name 줄                                          → 1 0 1 | 1 0 1
RE-01   러너 KIT_DIR 을 $(pwd) 기준으로                            → rc=2 EVALS_MISSING ///evals/evals.json
RE-02   README 블록 셋째 단계만 -maxdepth 5                        → 2
DG-02   howto-audit 에 목록 앞 빈 줄 없는 절                       → rules_up=3 MD022:0>1 MD030:0>1 MD032:0>1
SK-09   gate_blocks 의 howto-doc 수를 3 으로                       → gate_blocks=0
DG-05   README AUTO 표 한 칸 · howto-audit 끝 맨 펜스 · reviewer 끝 「7개 킷」 → sync_rc=1 0 · 10 1 rc=2 · hits=1
AR-01   변형 unsigned-mine · signed-outside · cross-phase          → 첫째 1 · 둘째 1 7 · 둘째 2 7
AR-01   변형 seal-broken (서명 커밋이 봉인 뒤 조건 줄을 바꿈)       → 셋째 1 ⏎ 넷째 SEAL_BROKEN
AR-01   변형 wc-only (작업 폴더에서만 조건 줄을 바꾸고 커밋 안 함)  → 셋째 0 ⏎ 넷째 SEAL_OK (고치기 전 명령은 같은 사본에서 셋째 1 — 작업 폴더를 읽었다)
ER-03   변형 unsigned-shared · signed-outside · cross-phase        → 마지막 값 1 · 1 · 1 (unsigned-mine 은 0 — howto-kit/README.md 는 공유 파일이 아니다. 그 경우는 AR-01 첫째가 잡는다)
DG-04   러너 끝에 `echo $1` · `if then` 두 줄                        → 첫 줄 그대로(러너가 끝 줄 전에 끝나 문법 오류에 닿지 않는다) ⏎ 둘째 줄
                                                                    run-evals.sh shellcheck rc=1 lines=7 howto-gate.sh shellcheck rc=0 lines=0 n_dash=2 n_sh=2 n_bash=2 n_zsh=1
                                                                    (고치기 전 명령은 같은 사본에서 shellcheck rc=0 lines=7 · n_*=0 — `$?` 가 basename 의 0 이었다)
NA      변형 signed-outside                                        → SC-00=1
DG-06   변형 cross-phase                                           → scope-isolation: FAIL ⏎ violators=1 mine=1
AR-03   변형 cross-phase                                           → 1 1 1 1 0 1
문장    SK-02 · SK-04 · SK-05 · SK-06 · SK-09 토큰 43 개를 하나씩 지운 사본 → 43 개 모두 값이 바뀜 (del.sh — 끝 판에 없는 다섯은 빠졌다: 옛 글 토큰 넷은 시작 커밋 판 1 이 양성 대조이고, 나머지 하나는 SK-09 의 sed 식이다.
        조건이 재는 파일에서만 지운다 — `[미검증:ENV]` 두 줄은 두 스킬에 같은 글로 있어 앞 파일에서 지우면 SK-04 값이 안 바뀐다)
```

러너 결함 실측(편집 전 감사): 시작 커밋 판 킷 사본에서 사례 E2 의 assertion 을 `["G5_TERMINAL FAIL", "nonterminal=99"]` 로 바꾸면 `sh` · `bash` 는 `rc=1` · `FAIL  E2-granularity-terminal-action — missing_assert`,
`zsh` 는 `rc=0` · `EVALS total=16 pass=16 fail=0` 이었다(2026-09-25). 게이트를 부르는 블록 실측: 시작 커밋 판 howto-audit Phase 2 블록을 레포 루트에서 `<대상>` = `howto-kit/evals/fixtures` 로
zsh · bash 에 돌리면 둘 다 종료 코드 1 · `not found` 15 줄 · 판정 줄 0 · `### ` 줄 15 였다(근거 파일 §2 실측과 같다).
러너 시간(이 맥): 시작 커밋 판 3.4 초 · 폴더 경우에 픽스처 열다섯을 쓴 판 20 초 · 앞 셋만 쓴 판 8 ~ 9 초.

## Skill

- [ ] SK-01: howto-kit 의 `howto-audit` 스킬 Phase 2 블록이 스크립트를 찾는 세 경우 모두에서 파일마다 판정한다 — Given `$END` 판 `howto-kit/skills/howto-audit/SKILL.md` 의 `### Phase 2: 게이트 전수 실행` 절 첫 `bash` 블록을 `<대상>` 만 픽스처 열다섯을 둔 폴더로 바꿔, When 플러그인 치환 경우(`${CLAUDE_PLUGIN_ROOT}` 를 킷 사본 경로 글자로) · git 최상위 폴더 경우(`git init` 한 폴더 아래 킷 사본, 치환 없음) · 마켓플레이스 설치본 경우(`HOME` 아래 `.claude/plugins/marketplaces/mk/howto-kit`) 를 zsh · bash 로 돌리면, Then 세 경우 모두 첫 줄이 그 경우의 `RESOLVED:` 경로이고 `### <경로>` 줄 15 · `GATE_PASS` · `GATE_FAIL` · `GATE_BLOCKED` 줄 15 · `not found` 줄 0 · 종료 코드 0 · 두 셸 출력이 같다. 블록 안에 `. "${1}"; shift` 와 `sh "$GATE" {} +` 가 각 1 줄, `. howto-kit/scripts/howto-gate.sh` 와 `export -f` 가 0 줄이다. 알려진 답: 픽스처 폴더 `.md` 열다섯을 손으로 셌다. 양성 대조: 시작 커밋 판 블록은 `X/15/0/15/1` (자식 셸이 함수를 못 봄) (측정: `type m >/dev/null || exit 2;` 뒤 `m SK-01` 두 줄이 `plugin:R/15/15/0/0/1 repo:R/15/15/0/0/1 market:R/15/15/0/0/1` · `1 1 0 0`) [exact]
- [ ] SK-02: `howto-audit` SKILL.md 에 (a) 제목 `### Gotcha 6: 게이트 함수는 자식 셸로 넘어가지 않는다` 절이 `### Gotcha 5: ` 뒤 · `## Process` 앞에 있고 그 절에 여덟 문장 조각 — 함수는 읽은 셸 안에서만 보인다 · 부모에서 읽고 `find -exec sh -c` 에서 부르면 `command not found` · Phase 2 는 `sh -c` 안에서 읽고 `export -f` 로 넘기지 않는다 · macOS `sh` · bash 자식에게만 넘어가고 우분투 `sh`(dash) · zsh 에게는 안 넘어간다 · `howto-kit/scripts/` 상대 경로 금지 · 세 단계 `test -f` · 실측(2026-09-24) 두 줄 — 이 `m.sh` `SK-02)` 갈래 글자 그대로 각 1 줄 이상 (b) `### Phase 2: 게이트 전수 실행` 절에 여섯 줄 — `MISSING:` 이면 판정을 내지 않고 그 줄을 보고하고 멈춘다 · `### <경로>` 줄 수와 판정 줄 수와 Phase 1 파일 수가 같아야 한다 · 다르면 실행 오류(Gotcha 6) · `find` 종료 코드로 판정하지 않는다 · `MISSING:` 으로 멈출 때 `[미검증:ENV]` 에 네 칸(막는 것 · 시도한 우회 · 통제 불가 사유 · 재검증 명령)을 붙인다는 두 줄 — 이 각 1 줄 이상 (c) Gotcha 의 `export -f` 주장이 이 맥에서 사실이다 — `bash` 로 내보낸 함수를 `/bin/sh` · `bash` 는 부르고 `/bin/dash` · `zsh` 는 못 부른다 (d) `### Phase 4: 리포트` 절 틀에 Phase 2 첫 줄 `RESOLVED:` 를 싣는 줄 1 줄 이상. 문장 삭제 대조: 조각 하나만 지운 사본에서 이 값이 바뀐다(`del.sh`) (측정: `type m >/dev/null || exit 2;` 뒤 `m SK-02` 다섯 줄이 `1 1 1 1 1 1 1 1 1` · `1` · `1 1 1 1 1 1` · `/bin/sh=called bash=called /bin/dash=no zsh=no` · `1`) [exact, enumerated]
- [ ] SK-03: `howto-doc` 스킬의 두 블록이 세 경우에서 판정한다 — `$END` 판 `howto-kit/skills/howto-doc/SKILL.md` 의 (a) `### Gotcha 3: ` 절 첫 `bash` 블록(폴더를 돈다)은 SK-01 과 같은 세 경우 · 두 셸에서 `R/15/15/0/0/1` 이고 `. "${1}"; shift` · `sh "$GATE" {} +` 각 1 줄, `. howto-kit/scripts/howto-gate.sh` 0 줄 (b) `### Phase 4: 게이트 실행 (E3)` 절 첫 `bash` 블록(`<생성한 문서>` 를 픽스처 `pass-fcm-ios.md` 로)은 세 경우 모두 `R/0/1/0/0/1` 이고 `  . "$GATE"; howto_gate <생성한 문서>` 1 줄, `. howto-kit/scripts/howto-gate.sh` 0 줄이다. 알려진 답: 폴더 15 · 파일 1. 양성 대조: 시작 커밋 판 Phase 4 블록은 레포 밖 경우에서 `X/0/0/1/127/0`. 음성 대조: 끝 판 Gotcha 3 블록 셋째 단계 `-maxdepth 4` 를 `1` 로 바꾼 사본에서 마켓플레이스 경우가 `market:M/0/0/0/1/1` (측정: `type m >/dev/null || exit 2;` 뒤 `m SK-03` 네 줄이 `plugin:R/15/15/0/0/1 repo:R/15/15/0/0/1 market:R/15/15/0/0/1` · `1 1 0` · `plugin:R/0/1/0/0/1 repo:R/0/1/0/0/1 market:R/0/1/0/0/1` · `1 0`) [exact, enumerated]
- [ ] SK-04: `howto-doc` SKILL.md 의 (a) `### Gotcha 3: ` 절에 세 줄 — 스크립트는 `sh -c` 안에서 읽는다 · 경로 순서와 `MISSING:` 일 때 할 일은 Phase 4 와 같다 · 줄 수가 다르면 실행 오류 — 이 `m.sh` `SK-04)` 갈래 글자 그대로 (b) `### Phase 4: 게이트 실행 (E3)` 절에 여섯 줄 — `RESOLVED:` 줄과 출력 7 줄을 그대로 붙인다 · 세 단계 경로 순서 · 상대 경로는 플러그인 설치 프로젝트에 없다 · `MISSING:` 이면 완료를 보고하지 않고 그 줄을 보고한다(Gotcha 1) · SK-02 (b) 와 같은 네 칸 두 줄 — 각 1 줄 이상 (c) 옛 줄 `. howto-kit/scripts/howto-gate.sh` 와 `find docs -type f -name '*.md' -exec sh -c '` 가 파일 안에 줄 그대로 0 이다. 문장 삭제 대조: `del.sh` (측정: `type m >/dev/null || exit 2;` 뒤 `m SK-04` 세 줄이 `1 1 1` · `1 1 1 1 1 1` · `old_line=0 old_find=0`) [exact, enumerated]
- [ ] SK-05: `howto-kit/README.md` 의 (a) `## 결정론 게이트 G1~G6` 절 첫 `bash` 블록이 SK-03 (b) 와 같은 세 경우에서 `R/0/1/0/0/1` 이고 (b) 같은 절에 세 줄 — `howto-doc` Phase 4 와 같은 블록 · 세 단계로 찾고 못 찾으면 `MISSING:` · 여러 파일은 `sh -c` 안에서 읽는다(`howto-audit` Gotcha 6) — 각 1 줄 이상 (c) `## Evals` 절에 네 줄 — 세 셸 대조 · 게이트를 부르는 `bash` 블록을 네 경우에서 zsh · bash 로 돌린다 · 블록 수는 `evals.json` 의 `gate_blocks` 와 같아야 한다 — 각 1 줄 이상이고 옛 글 「모든 케이스를 zsh 와 bash 양쪽에서」 가 0 (d) 옛 줄 `. howto-kit/scripts/howto-gate.sh` 가 줄 그대로 0 이다. 양성 대조: 시작 커밋 판 README 블록은 레포 밖 경우에서 `X/0/0/1/127/0` (측정: `type m >/dev/null || exit 2;` 뒤 `m SK-05` 네 줄이 `plugin:R/0/1/0/0/1 repo:R/0/1/0/0/1 market:R/0/1/0/0/1` · `1 1 1` · `1 1 1 1 0` · `old_line=0`) [exact, enumerated]
- [ ] SK-06: Phase 1 가이드 대조 — `howto-kit/agents/howto-reviewer.md` 에 규칙 7 의 「판정 불가면 그 row 는 `[미검증:ENV]` 또는 `[미검증:INVALID]` 이고 PASS 가 아니다.」 와 출력 형식 절의 다섯 조각(분류 접미 · `ENV` 에 네 칸 막는 것 · 시도한 우회 · 통제 불가 사유 · 재검증 명령 · 못 채우면 `INVALID` · 접미 없는 표기는 쓰지 않는다와 그 근거 `harness/docs/guides/agent-design-guide.md` §10)이 `m.sh` `SK-06)` 갈래 글자 그대로 각 1 줄 이상이고, 파일 안 접미 없는 `[미검증]` 이 0 개다. 양성 대조: 시작 커밋 판은 `bare=2` (측정: `type m >/dev/null || exit 2;` 뒤 `m SK-06` 두 줄이 `1 1 1 1 1 1` · `bare=0`) [exact, enumerated]
- [ ] SK-07: 러너가 끝 판에서 통과하고 사례 이름이 전부 나온다 — `$END` 판 킷 사본에서 `bash howto-kit/evals/run-evals.sh` 가 종료 코드 0 · `FAIL` 줄 0 · `EVALS total=33 pass=33 fail=0` 이고, `PASS  ` 줄의 이름 서른셋이 기대 목록(끝 판 `evals.json` 사례 열여섯 + `blocks-declared` + `readme-md-1` · `howto-audit-1` · `howto-doc-1` · `howto-doc-2` 각각의 `plugin` · `repo` · `market` · `none`)과 같다. 양성 대조: 시작 커밋 판 러너는 `total=16` · `got=16 same=0` (측정: `type m >/dev/null || exit 2;` 뒤 `m SK-07` 두 줄이 `rc=0 |  | EVALS total=33 pass=33 fail=0` · `want=33 got=33 same=1`) [exact, enumerated]
- [ ] SK-08: 러너가 깨진 곳만 잡는다 — `$END` 판 킷 사본을 `ctl-runner.py` 로 한 군데씩 깨뜨린 여덟에서 bash 러너가 종료 코드 1 과 그 자리 사례만 `FAIL` 로 낸다: (n1) howto-audit Phase 2 를 시작 커밋 판 블록으로 → `howto-audit-1` 네 경우 (n2) 부모에서 읽고 `export -f` 로 넘김 → `howto-audit-1` 의 `market` · `plugin` · `repo` (n3) README 블록을 지움 → `blocks-declared` 하나(`total=29`) (n4) 등록 안 된 블록을 `references/step-contract.md` 에 더함 → `blocks-declared` 하나(`total=37`) (n5) howto-doc Phase 4 블록의 `marketplaces` 를 `marketplace` 로 → `howto-doc-2:market` 하나 (n6) howto-doc Gotcha 3 블록 `MISSING` 갈래의 `false` 를 지움 → `howto-doc-1:none` 하나 (n7) 사례 E2 의 assertion 을 `nonterminal=99` 로 → `E2-granularity-terminal-action` 하나 (n8) sh 로 부를 때만 한 줄 더 내는 게이트 → 게이트 사례 열여섯 전부. 그리고 n7 사본을 zsh 로 부르면 끝 판 러너는 같은 한 사례로 `rc=1` 이고, 시작 커밋 판 러너는 zsh 에서 `rc=0` · `pass=16` 이다 — 이 차이가 zsh assertion 결함을 고친 증거다. 변형이 안 걸리면 `NEG_EDIT_FAIL` 이 찍혀 기대값과 달라진다 (측정: `type m >/dev/null || exit 2;` 뒤 `m SK-08` 열 줄이 차례로 `n1 rc=1 | howto-audit-1:market,howto-audit-1:none,howto-audit-1:plugin,howto-audit-1:repo | EVALS total=33 pass=29 fail=4` · `n2 rc=1 | howto-audit-1:market,howto-audit-1:plugin,howto-audit-1:repo | EVALS total=33 pass=30 fail=3` · `n3 rc=1 | blocks-declared | EVALS total=29 pass=28 fail=1` · `n4 rc=1 | blocks-declared | EVALS total=37 pass=36 fail=1` · `n5 rc=1 | howto-doc-2:market | EVALS total=33 pass=32 fail=1` · `n6 rc=1 | howto-doc-1:none | EVALS total=33 pass=32 fail=1` · `n7 rc=1 | E2-granularity-terminal-action | EVALS total=33 pass=32 fail=1` · `n8 rc=1 | E1-pass-baseline,E10-g4-korean-delete-unsourced,E11-g4-korean-delete-sourced,E12-g4-delete-action-not-deprecation,E13-g4-retention-notice-sourced,E14-g4-completion-phrase-not-deprecation,E15-g4-korean-shutdown-unsourced,E16-g4-korean-abolish-unsourced,E2-granularity-terminal-action,E3-granularity-verify-and-branch,E4-domain-mix-declared,E5-domain-mix-undeclared,E6-deprecation-korean-unsourced,E7-deprecation-korean-sourced,E8-zero-steps-no-divide-by-zero,E9-missing-file-blocked | EVALS total=33 pass=17 fail=16` · `n7z_end rc=1 | E2-granularity-terminal-action | EVALS total=33 pass=32 fail=1` · `n7z_base rc=0 |  | EVALS total=16 pass=16 fail=0`) [exact, enumerated]
- [ ] SK-09: `howto-kit/scripts/howto-gate.sh` 머리 주석(`HOWTO_VERBS=` 줄 전까지)에 다섯 줄 — `# 사용:  . <이 파일 경로>` · 세 단계 경로(howto-doc Phase 4) 두 줄 · 자식 셸 · `export -f` 한 줄 · 세 셸 대조 한 줄 — 이 `m.sh` `SK-09)` 갈래 글자 그대로 각 1 줄이고 옛 줄 `# 사용:  . howto-kit/scripts/howto-gate.sh` 가 0, `howto-kit/evals/evals.json` 의 최상위 키가 차례로 `kit,description,runner,gate_blocks,cases` 이고 `gate_blocks` 가 `{"README.md": 1, "skills/howto-audit/SKILL.md": 1, "skills/howto-doc/SKILL.md": 2}` 이며 `description` 에 「zsh · bash · sh 세 셸」 이 있다. 음성 대조: `gate_blocks` 의 howto-doc 수를 3 으로 바꾼 사본에서 `gate_blocks=0` (측정: `type m >/dev/null || exit 2;` 뒤 `m SK-09` 두 줄이 `1 1 1 1 1 0` · `keys=kit,description,runner,gate_blocks,cases gate_blocks=1 desc_three=1`) [exact, enumerated]

## Script

- [ ] SC-00: N/A (Script 카테고리는 `release.sh` 연동 · 버전 올림 · `marketplace.json` 갱신이다. 이 Phase 는 그 파일을 건드리지 않는다 — 공유 파일은 Final 몫. 러너는 스킬 평가 도구라 Skill 카테고리에서 잰다(SK-07 · SK-08). 측정: `type m >/dev/null || exit 2;` 뒤 `m NA` 의 `SC-00=0`. 양성 대조: 예행 변형 `signed-outside` 에서 `SC-00=1`)

## Error

- [ ] ER-01: 일곱 파일에 새로 생긴 URL 과 `.harness/.meta/kaizen-0924/phase17-notes.md` 의 URL 이 전부 시작 커밋 판의 외부 근거 파일 `.harness/.meta/evidence/phase17.md` 에 있고, 끝 판 근거 파일이 시작 커밋 판과 같다 — 근거 파일은 `.harness/` 안이라 이 Phase 가 고칠 수 있으므로 끝 판에서 읽지 않는다. 일곱 파일은 파일마다 편집 전 판과 비교한다. 양성 대조: 근거 파일에 없는 URL 한 줄을 README 사본에 더하면 첫 값 1 (러닝북 — 근거 파일에 없는 URL 을 지어내지 마라 · notes 킷 로그의 출처 URL 은 근거 파일에서만) (측정: `type m >/dev/null || exit 2;` 뒤 `m ER-01` 세 줄이 `0` · `0` · `evid_same=1`) [exact, enumerated]
- [ ] ER-02: 일곱 파일에 더한 줄에 번역투 6 종(`tone-kit/references/locale-korean.md` §2 치환표의 grep 열)이 0 건, 특정 앱 이름 · 특정 화면 도구 서버 이름(`fit-?pal` · `fit_pal` · `flutter[-_]playwright` · `playwright-mcp` · `chrome-devtools-mcp`, 대소문자 무시)이 0 건이고, `$END` 판 `howto-kit/` 전체에서 같은 이름이 0 줄이다. 양성 대조: reviewer 사본 끝에 「이 값에 대해 적는다」 → `k02=1`, 「fit-pal 앱」 → `names=1 kit_names=1` (러닝북 말투 · 문서 규칙) (측정: `type m >/dev/null || exit 2;` 뒤 `m ER-02` 가 `added=` 뒤 수 하나와 `k02=0 names=0 kit_names=0`) [exact]
- [ ] ER-03: 이 Phase 범위 밖 반대편을 명시적 미완으로 넘기고 건드리지 않는다 — `.harness/.meta/kaizen-0924/phase17-notes.md` 가 `$END` 에 커밋돼 있고 (a) 처리 배정표 키 `other-kits:P4` · `other-kits:P3` 와 러닝북이 적게 한 절 머리 일곱(`## 바꾼 파일` · `## 반영한 처리 배정표 키` · `## 미반영 키와 사유` · `## 넘기는 것` · `## changelog 한 단락` · `## 킷 로그 한 단락` · `## 다음 사이클 메모`)이 각각 1 줄 이상 (b) `## 넘기는 것` 절 안에 넘김 일곱 토큰 — `.github/workflows/ci.yml` (Final — validate 작업에 `command -v zsh` 로 보고 없을 때만 `apt-get update` 뒤 zsh 를 설치하는 줄과 `sh howto-kit/evals/run-evals.sh`) · `.claude/skills/howto-kaizen/SKILL.md` (Final — Gotcha 2 「두 셸」) · `docs/howto-kit/overview.html` (Final F2 — 「두 셸 출력의 동일성」) · `plugin.json` (Final — 버전) — 이 각 1 줄 이상 (c) `## 미반영 키와 사유` 절에 `DITA 2.0` · `26514` · `cache` 가 각 1 줄 이상 (d) 시작 커밋부터 `$END` 사이에 공유 파일(`.claude-plugin/marketplace.json` · `howto-kit/.claude-plugin/plugin.json` · `README.md` · `CLAUDE.md` · `.harness/.meta/orchestrator-audit-log.md` · `.harness/.meta/kaizen-failure-count.yaml` · `.claude/kaizen-input/insights-report.md` · `.github/workflows/ci.yml` · `.harness/stale-values.yaml`)과 레포 전용 경로(`.claude/skills` · `harness` · `scripts` · `docs/howto-kit` · `docs/index.html`)를 건드린 커밋 가운데 다른 Phase 서명이 없는 커밋이 0 개다. 양성 대조: 예행 변형 `unsigned-shared` · `signed-outside` · `cross-phase` 에서 마지막 값 1 (측정: `type m >/dev/null || exit 2;` 뒤 `m ER-03` 다섯 줄이 `notes_committed=1` · `1 1 1 1 1 1 1 1 1` · `1 1 1 1 1 1 1` · `1 1 1` · `0`) [exact, enumerated]
- [ ] ER-04: 스크립트를 어디서도 못 찾으면 네 블록이 게이트를 부르지 않고 멈춘다 — Given `$END` 판 네 블록(howto-audit Phase 2 · howto-doc Gotcha 3 · howto-doc Phase 4 · README), When `CLAUDE_PLUGIN_ROOT` 를 치환하지 않고 환경에서도 지운 채 git 저장소 밖 폴더에서 빈 `HOME` 으로 zsh · bash 로 돌리면, Then 네 블록 모두 첫 줄이 `MISSING: howto-gate.sh tried=` 로 시작하고 `### <경로>` · 판정 줄 · `not found` 줄이 0 · 종료 코드 1 · 두 셸 출력이 같으며, bash 첫 줄이 `MISSING: howto-gate.sh tried=/scripts · /howto-kit/scripts · <그 HOME>/.claude/plugins/marketplaces` 와 글자 그대로 같다(시도한 세 곳). 양성 대조: 시작 커밋 판 블록은 네 줄 모두 `exact=0` 이고 howto-audit 은 `X/15/0/15/1/0`. 음성 대조: 끝 판 howto-audit 블록 `MISSING` 갈래의 `false` 를 지운 사본에서 첫 줄이 `none:M/0/0/0/0/1` (측정: `type m >/dev/null || exit 2;` 뒤 `m ER-04` 네 줄이 모두 `none:M/0/0/0/1/1  exact=1`) [exact, enumerated]

## Architecture

- [ ] AR-01: 이 Phase 의 변경이 허용 경로 안에 머물고, 범위 선언 블록이 그 경로와 같으며, 이 계약이 봉인돼 있다 [exact, enumerated]
  (측정: `type m >/dev/null || exit 2;` 뒤 `m AR-01` 여섯 줄이 `0` · `0 7` · `0` · `SEAL_OK` · `scope_same=1` · `1`.
  첫째 — 시작 커밋부터 `$END` 사이에 `howto-kit` · `docs/howto` 를 건드린 커밋 가운데 서명 줄이 없는 커밋 수 0 (서명을 빠뜨린 커밋은 서명 줄 목록에 안 보이므로 경로로 직접 센다).
  둘째 — 서명 커밋이 건드린 경로 가운데 `.harness/` 밖이면서 `FILES` 일곱 밖인 경로 수 0 과, `FILES` 일곱 가운데 서명 커밋이 건드린 수 7.
  셋째 — 끝 판(`$END`)을 푼 폴더의 `.harness/` 에서, 슬러그를 열거하지 않고 봉인이 깨진 계약 가운데 이 Phase 가 건드린 것의 수 0
  (`harness/references/contract-schema.md` §`.harness/` 범위 조건 권장 형태를 끝 판에 적용 — 작업 폴더에는 다른 세션의 미커밋 계약 변경이 있다).
  넷째 — 끝 판 이 계약의 봉인이 `SEAL_OK`. 다섯째 — `## 범위 경계` 절 `# sprint-scope` 블록의 `.harness/` 밖 경로가 `FILES` 와 같다. 여섯째 — 그 블록에 `.harness/` 줄 1.
  양성 대조: 예행 변형 `unsigned-mine` → 첫째 `1` · `signed-outside` → 둘째 `1 7` · `cross-phase` → 둘째 `2 7` · `seal-broken`(서명 커밋이 봉인 뒤 조건 줄을 바꿈) → 셋째 `1` · 넷째 `SEAL_BROKEN`.
  음성 대조: 예행 변형 `wc-only`(작업 폴더에서만 조건 줄을 바꾸고 커밋하지 않음) → 셋째 `0` · 넷째 `SEAL_OK`)
- [ ] AR-02: 새 문장이 가리키는 자리가 실제로 있다 — (a) README 의 `(`howto-audit` Gotcha 6)` 1 · howto-audit 의 `(Gotcha 6)` 1 · howto-audit `### Gotcha 6: ` 제목 1 (b) 게이트 스크립트의 `(howto-doc Phase 4)` 1 · README 의 「`howto-doc` Phase 4 와 같은 블록이다」 1 · howto-doc 의 「Phase 4 와 같다」 1 · howto-doc `### Phase 4: 게이트 실행 (E3)` 제목 1 (c) howto-doc 의 `(Gotcha 1).` 1 · howto-doc `### Gotcha 1: ` 제목 1 (d) reviewer 의 `harness/docs/guides/agent-design-guide.md` §10 인용 1 · 그 가이드에 `1. **분류 접미를 붙인 마커**` 1 (e) `evals.json` `gate_blocks` 의 키 셋이 모두 킷 안에 있는 파일이다. 음성 대조: howto-audit Gotcha 6 제목을 바꾼 사본에서 (a) 셋째 값 0 (측정: `type m >/dev/null || exit 2;` 뒤 `m AR-02` 가 `1 1 1 | 1 1 1 1 | 1 1 | 1 1 | 3 3`) [exact, enumerated]
- [ ] AR-03: 손대지 않을 곳이 그대로다 — (a) 게이트 스크립트의 `HOWTO_VERBS=` 줄부터 끝까지(판정 코드)가 시작 커밋 판과 글자 그대로 같고 비지 않았다 (b) `evals.json` 의 `cases` · `runner` · `kit` 가 시작 커밋 판과 같다 (c) `howto-kit/evals/fixtures/` (d) `howto-kit/references/` (e) `howto-kit/skills/howto/SKILL.md` (f) `docs/howto/` 가 시작 커밋 판과 같다. 음성 대조: 회피 표현 목록 한 글자 → (a) `0` · 사례 id 하나 → (b) `0` (측정: `type m >/dev/null || exit 2;` 뒤 `m AR-03` 이 `1 1 1 1 1 1`) [exact, enumerated]

## Anti-patterns

- [ ] AP-01: 버전을 하드코딩하지 않는다 — plugin.json에서 읽어야 한다. 이번 변경에 적용: 일곱 파일에 더한 줄에 howto-kit `plugin.json` 의 `version` 값(`$END` 판에서 읽는다)이 0 건이다 — 이 Phase 는 킷 버전을 적지 않고 Final 이 올린다. 양성 대조: reviewer 사본 끝에 그 값 → 1 (측정: `type m >/dev/null || exit 2;` 뒤 `m AP-01` 이 `version=0.2.1 0`) [exact]
- [ ] AP-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수 (```` ```text, ```bash, ```yaml ```` 등). 판정 권위는 validate-plugin V6 상태기계다 — 여는/닫는 fence 가 동형이라 줄 단위 정규식으로는 판정 불가. 이번 변경에 적용: V6 가 읽는 파일은 DG-05 의 V6 줄이 보고, 마크다운 네 파일(howto-audit · howto-doc SKILL.md · README · reviewer) 모두 같은 여닫기 방식으로 센 언어 힌트 없는 여는 펜스가 0 이다. 양성 대조: reviewer 사본 끝에 언어 힌트 없는 펜스 → 넷째 값 1 (측정: `type m >/dev/null || exit 2;` 뒤 `m AP-03` 이 `0 0 0 0`) [exact]
- [ ] AP-04: SKILL.md / agents/*.md frontmatter 에서 name 필드 누락 — validate-plugin V1 FAIL. 이번 변경에 적용: howto-audit · howto-doc SKILL.md 와 reviewer 의 첫 frontmatter 블록이 편집 전과 글자 그대로 같고 `name: howto-audit` · `name: howto-doc` · `name: howto-reviewer` 줄이 각 1 개다 — 그래서 README AUTO 구간과 트리거 설명이 읽는 값도 바뀌지 않는다. 음성 대조: howto-doc `name:` 줄을 바꾼 사본에서 `1 0 1 | 1 0 1` (측정: `type m >/dev/null || exit 2;` 뒤 `m AP-04` 가 `1 1 1 | 1 1 1`) [exact]

## Reusability

- [ ] RE-01: 다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다. 이번 변경에 적용: 러너는 자기 파일 위치로 킷을 잡아, 레포 밖 폴더(`/`)에서 절대 경로로 불러도 `$END` 판과 같은 결과를 낸다 — CI 든 사람이든 작업 폴더와 상관없이 부를 수 있다. 음성 대조: 러너 사본의 `KIT_DIR=$(cd "$(dirname "$0")/..` 를 `$(pwd)` 기준으로 바꾸면 `rc=2 EVALS_MISSING` (측정: `type m >/dev/null || exit 2;` 뒤 `m RE-01` 이 `rc=0 EVALS total=33 pass=33 fail=0 EVALS_PASS`) [goal]
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다. 이번 변경에 적용: 경로 찾기는 레포의 기존 순서(`harness/agents/qa-evaluator.md` Step 8 — 플러그인 치환 → 레포 → `find "$HOME/.claude/plugins/marketplaces" -maxdepth 4 -type f`)를 따르고 새 순서를 만들지 않는다 — (a) 네 블록의 앞 여섯 줄(경로 찾기와 `RESOLVED:` 줄)이 서로 글자 그대로 같고 (b) howto-audit 블록의 첫 줄이 `GATE="${CLAUDE_PLUGIN_ROOT}/scripts/howto-gate.sh"`, 둘째 줄에 `git rev-parse --show-toplevel`, 셋째 줄에 `find "$HOME/.claude/plugins/marketplaces" -maxdepth 4 -type f` 가 있고 같은 셋째 줄 글이 qa-evaluator 에 1 번 이상 있다 (c) `howto_gate() {` 정의는 킷 안에서 게이트 스크립트 하나다. 음성 대조: README 블록 셋째 단계만 `-maxdepth 5` 로 바꾸면 (a) `2` (측정: `type m >/dev/null || exit 2;` 뒤 `m RE-02` 두 줄이 `1` · `1 1 1 | qa=<1 이상> | howto-kit/scripts/howto-gate.sh` — 예행 판 `qa=2`) [exact, enumerated]

## Diagnostics

- [ ] DG-01: N/A (`commands.analyze` 는 `bash -n scripts/release.sh` 라 `scripts/release.sh` 만 잰다 — 이번 변경 파일과 교집합 0 개. 측정: `type m >/dev/null || exit 2;` 뒤 `m NA` 의 `DG-01=0`. 새 셸 코드의 실제 검사는 DG-04)
- [ ] DG-02: IDE diagnostics 워닝/인포 0개 (`diagnostics.ide_exclude` 값 `[]`) — 이번 변경에 적용: 편집기 마크다운 확장과 같은 조건(markdownlint-cli2 0.23.2 · MD013 끔)으로 마크다운 네 파일 **각각**에서 규칙별 경고 수를 편집 전 판과 비교해 늘어난 규칙이 0 개다. 더한 줄만 보지 않는다 — MD022 · MD032 · MD024 는 더한 줄 옆의 손대지 않은 줄에 붙는다(러닝북 측정 구멍 목록). 편집 전부터 있던 경고는 같은 수로 남아도 된다. 양성 대조: howto-audit 사본에 목록 앞 빈 줄 없는 절 → `rules_up=3` (측정: `type m >/dev/null || exit 2;` 뒤 `m DG-02` 네 줄이 모두 `rules_up=0`) [exact]
- [ ] DG-03: N/A (`commands.test` 는 `bash scripts/release.sh 2>&1 || true` 라 `scripts/release.sh` 만 잰다 — 교집합 0 개. 측정: DG-01 과 같은 `m NA` 의 `DG-01=0`. 실제 시험은 SK-07 · SK-08 · DG-04)
- [ ] DG-04: 실제 앱/서버 구동 시 에러 0개 — 이번 변경에 적용: 구동하는 것은 러너다. `$END` 판 러너를 네 해석기(`/bin/dash` · `/bin/sh` · bash · zsh)로 돌리면 네 번 모두 종료 코드 0 · stderr 0 줄 · 표준 출력이 dash 판과 같고, 러너와 게이트 스크립트에 `shellcheck -s sh` 가 각각 종료 코드 0 · 출력 0 줄, 네 해석기의 러너 `-n` 문법 검사가 모두 종료 코드 0 이다. 종료 코드는 `printf` 전에 받는다(인자의 명령 치환이 먼저 풀리면 `$?` 가 `basename` 의 0 이 된다). 음성 대조: 끝 판 러너 사본 끝에 `echo $1` · `if then` 두 줄 → 둘째 줄 `run-evals.sh shellcheck rc=1 lines=7 howto-gate.sh shellcheck rc=0 lines=0 n_dash=2 n_sh=2 n_bash=2 n_zsh=1` (첫 줄은 그대로다 — 러너가 끝 줄 전에 끝나 문법 오류에 닿지 않는다. 그래서 `-n` 검사를 따로 둔다) (측정: `type m >/dev/null || exit 2;` 뒤 `m DG-04` 두 줄이 `/bin/dash rc=0 err=0 same=1 | /bin/sh rc=0 err=0 same=1 | bash rc=0 err=0 same=1 | zsh rc=0 err=0 same=1 |` · `run-evals.sh shellcheck rc=0 lines=0 howto-gate.sh shellcheck rc=0 lines=0 n_dash=0 n_sh=0 n_bash=0 n_zsh=0`) [exact]
- [ ] DG-05: 저장소 검사가 이 킷을 문제로 가리키지 않는다 — `$END` 판을 git 저장소로 만든 사본에서 (a) `scripts/validate-plugin.py howto-kit` 출력에 `V1` ~ `V10` 열 줄이 있고 `— OK` · `— SKIP (no templates/)` 로 끝나지 않는 줄이 0 이며 종료 코드 0 (b) `scripts/sync-docs.py howto-kit --check-only` 가 종료 코드 0 이고 `howto-kit/README.md: 동기화됨` 1 줄 (c) `.harness/stale-values.yaml` 의 `old` 값 전부를 일곱 파일에서 직접 센 수가 0 이다. 양성 대조: README AUTO 표 한 칸 → `sync_rc=1 0` · howto-audit 끝에 언어 힌트 없는 펜스 → `10 1 rc=2` · reviewer 끝에 등록부 옛 값 → `hits=1` (측정: `type m >/dev/null || exit 2;` 뒤 `m DG-05` 세 줄이 `10 0 rc=0` · `sync_rc=0 1` · `stale_old=15 files=7 hits=0`) [exact]
- [ ] DG-06: `python3 scripts/validate-post-kaizen.py --since f936019c3f017be3e1bcc92570d677ef8cc6521b` 출력의 `scope-isolation` · `doc-contracts` 줄이 `FAIL` · `ERROR` 가 아니다. `docs-site-regen` 은 Final F2 몫이라 판정에서 뺀다. 다른 Phase 커밋 때문에 `scope-isolation` 이 FAIL 이면 `--verbose` 위반 커밋 목록을 1 개 이상 읽었고 그 가운데 서명 줄 커밋이 0 개일 때, `doc-contracts` 가 FAIL · ERROR 이면 `validate-doc-contracts.py -v` 가 검사한 경로를 1 개 이상 읽었고 그 가운데 서명 커밋이 건드린 경로가 0 개일 때 PASS 다 — 커밋 뒤에 잰다 (측정: `type m >/dev/null || exit 2;` 뒤 `m DG-06` 이 `scope-isolation: PASS` · `doc-contracts: PASS` 또는 FAIL 이면 넷째 줄 `violators=<1 이상> mine=0` · 셋째 줄 `doc_checked=<1 이상> doc_mine=0`. 예행 판 `scope-isolation: PASS` · `doc-contracts: PASS` · `doc_checked=2 doc_mine=0` · `violators=0 mine=0`. 양성 대조: 예행 변형 `cross-phase`(서명 커밋 하나가 `harness/skills/` 와 `howto-kit/skills/` 를 함께 건드림) → `scope-isolation: FAIL` · `violators=1 mine=1`) [exact]
