---
feature: "킷 후속 A — flutter-toolkit · design-kit · infra-kit · react-kit (2026-09-24 카이젠 다음 사이클 메모)"
slug: after-0924-kits-a
created: "2026-09-26 11:55"
complexity: "복잡"
conditions: 28
status: done
owner_session: bda55d45-296c-491f-89ba-b52042d58e72
conditions_digest: sha256:03017626965ce499
locked_at: "2026-09-26 12:12"
---

## 배경

2026-09-24 카이젠이 다음 사이클로 넘긴 킷 몫 가운데 네 킷(flutter-toolkit · design-kit · infra-kit · react-kit) 항목을 한 계약으로 묶는다.
근거 원문은 `.harness/handoff/2026-09-26-0110.md` §C3(본 체크아웃, 읽기만) 과 이 가지의
`.harness/.meta/kaizen-0924/f1-kit-followups-notes.md` · `f2-review-fixes-notes.md` 의 「다음 사이클 메모」 절이다.

- 사용자 합의(Step 5): 사용자 위임으로 받은 것으로 적는다 — user 2026-09-26T01:04:21.505Z 「다음 세션에서 직접할 일을 다 실행하고 이어질것도 실행해」
  (세션 기록 `/Users/jackson/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/de8c7935-a5b6-4df5-9106-fafa73c288a0.jsonl`),
  그 앞의 「나한테 물어보지 말고 자동으로 끝까지」(2026-09-24T04:04:16.964Z). 판단이 갈린 곳은 저장소 안 근거로 정했고 `## 범위 경계` 에 적었다.
- 작업 폴더 W = `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak-c3`, 가지 `chore/ak-c3-kits`, 시작점 `f81568d`(origin/main, #110).
- 커밋 규칙: `git add <경로>` 뒤 `git commit -o <경로>` · 한 커밋에 킷 하나 · `.harness/` 파일은 킷과 다른 커밋 · `git add -A` · `git stash` · push · 가지 바꾸기 금지.
- 구현 전에 `tone-kit:tone-guide` 1 단계(규칙 불러오기)를, 완료 선언 전에 5 단계(전수 대조)를 한다 — 대조 결과는 notes 에 남긴다(AR-02).
- 사용자가 할 일: 없음.

복잡도 4 축 — 셋이 「예」 이고 공개 약속 변경과 소비자가 함께 있어 「복잡」 이다. Step 2.5 짝 조건: SK-02(widget-inspector 호출자) · SK-07(Makefile 소비자) · SK-10(결정 전파 소비자) · SK-12(react-kit 빠른 시작).

| 축 | 물음 | 값 |
| -- | ---- | -- |
| 레이어 수 | 몇 개 계층을 관통하는가 | 셋 — 스킬 · 에이전트 · 참조 문서, 문서 안 검사 코드와 시험 스크립트, 시험 입력(예시 기록 · 보고서) |
| 공개 API·계약 변경 | 외부에 노출된 약속이 바뀌는가 | 예 — 결정 전파 목록의 `status` · `excluded_surfaces` 규칙과 종료 코드, widget-inspector 호출 약속, infra-test 규칙 1 출력, Makefile 타겟 판정 |
| 소비면 존재 | 반대편이 있는가 | 예 — design-test · design-audit · design-reviewer, flutter-feature · flutter-widget · flutter-screen, flutter-run · flutter-ai-rules, react-kit README |
| 회귀 위험 | 기존 동작이 깨질 수 있는가 | 예 — 결정 전파 시험의 기존 입력 열, 예시 보고서 바이트 비교 시험, infra-test 알려진 답 |

설정 값 대조 (`.harness/project.yaml` 을 글자 그대로 옮김):

| config key | project.yaml 에서 읽은 값 | 계약에 쓴 값 |
| ---------- | ------------------------- | ------------ |
| `commands.analyze` | `bash -n scripts/release.sh` | DG-01 N/A — 재는 파일이 바뀐 파일에 없다 |
| `commands.test` | `bash scripts/release.sh 2>&1 \|\| true` | DG-03 N/A — 같은 이유 |
| `diagnostics.ide_exclude` | `[]` | DG-02 의 `([] 제외)` |
| `contract_categories[].id` / `prefix` | Skill/SK · Script/SC · Error/ER · Architecture/AR | 같은 넷 |
| `anti_patterns[].id` / `message` | AP-01 버전 하드코딩 · AP-02 force push · AP-03 bare code fence · AP-04 frontmatter name 누락 | AP-03 · AP-04 (바뀌는 파일이 SKILL.md · 에이전트 · 코드 블록 있는 MD 라 걸릴 수 있다). AP-01 은 plugin.json 버전을 안 건드려서, AP-02 는 이 계약이 push 하지 않아서 뺐다 |

## GAP 분석 (Pre-Edit Audit)

대상 파일을 읽기만 하고 줄을 적었다. 줄 번호는 시작점 `f81568d` 기준이다.

| 대상 파일 | 실제 Read 증거 (`파일:라인`) | 발견한 기존 갭·위반 | 계약 조건화 여부 |
| --------- | ---------------------------- | ------------------- | ---------------- |
| `flutter-toolkit/agents/widget-inspector.md` | `:122` §7 제목 · `:134-135` 표 없음 규칙 · `:244` Rules 마지막 MUST | 제목은 「관례 표를 받았을 때」 인데 본문은 표가 없으면 `[미검증]` 을 적으라 한다. flutter-feature 는 늘 표 없이 불러 그 `[미검증]` 이 매번 버려진다 | SK-01 |
| `flutter-toolkit/skills/flutter-feature/SKILL.md` | `:191-193` Post-Creation 호출 · `:196-200` 보일러플레이트만 만든다 | 관례 표를 만들지 않는 스킬인데 호출에 그 사실을 밝히지 않는다 | SK-02 |
| `flutter-toolkit/skills/flutter-widget/SKILL.md` · `flutter-screen/SKILL.md` | `flutter-widget:267` · `flutter-screen:276` | 표를 넘긴다 — 맞다. 바꾸지 않는다 | SK-02 (그대로인지) |
| `flutter-toolkit/evals/evals.json` | `:204` 사례 16 단언 | 표가 없으면 `[미검증] 관례 표 없음` — 「밝히지 않은 표 없음」 경우라 새 규칙과 맞는다. 바꾸지 않는다 | SK-01 (근거) |
| `flutter-toolkit/skills/flutter-build/SKILL.md` | `:16` Gotcha(2.16 문장) · `:48` · `:53` 명령 | 2.7.0 부터 플래그가 무시된다는 것도, 그래도 남기는 이유도 없다 | SK-03 |
| `flutter-toolkit/skills/flutter-run/SKILL.md` · `flutter-preflight/SKILL.md` | `flutter-run:43` · `:51` · `:56` · `flutter-preflight:79` · `:84` | 같은 명령 — 남긴다. `flutter-run:43` 은 `HAS_MAKEFILE` 하나로 `$MAKE app-codegen` 을 고른다 | SK-03 · SK-07 |
| `~/.pub-cache/hosted/pub.dev/build_runner-2.13.1/CHANGELOG.md` | `:149` · `:150` (2.7.0 「Ignore `-d` flag: always delete files as if `-d` was passed.」) | 2.7.0 이상에서 플래그는 효과 없는 인자 | SK-03 (근거) |
| `~/.pub-cache/hosted/pub.dev/build_runner_core-7.3.2/lib/src/generate/build_definition.dart` · `build_runner_core-8.0.0/…` 같은 파일 | `:529-535` 플래그면 확인 없이 지움 · `:564-570` 대화 불가 실행이면 「run with `--delete-conflicting-outputs`」 와 함께 빌드 중단 | 2.7.0 미만(2.3.3 · 2.4.x 가 이 판을 쓴다 — `build_runner-2.4.15/pubspec.yaml:23` `^8.0.0`, `build_runner-2.4.13/pubspec.yaml:23` `^7.2.0`)은 플래그를 빼면 멈춘다. 설치본 폴더에 2.3.3 · 2.4.13 · 2.4.15 가 있다 | SK-03 (빼지 않는 근거) |
| `flutter-toolkit/skills/flutter-scenario-report/SKILL.md` | `:44` 채널 조건 · `:54` 완료 기준 | `VISUAL_CHANNEL` 이 `mcp:` 여야 한다는데 Step 8 은 golden · integration_test 를 먼저 고른다 — MCP 가 있어도 할 일이 정해져 있지 않다 | SK-04 |
| `flutter-toolkit/references/project-detection.md` | `:32-59` Step 2b · `:41-45` 타겟 목록 · `:47-56` 매핑 표 · `:138-147` Step 8 표 | 타겟 하나만 있어도 `HAS_MAKEFILE = true` 이고 표의 모든 행이 `$MAKE app-…` 를 부른다 — `app-preflight` 만 있으면 `app-codegen` 등이 없어 실패한다 | SK-06 |
| `flutter-toolkit/references/flutter-ai-rules.md` | `:115` | `HAS_MAKEFILE` 하나로 `make <target>` 우선 | SK-07 |
| `flutter-toolkit/skills/flutter-l10n/SKILL.md` | `:15` Gotcha · `:35` 설치 안내 · `:122-129` Step 6 | slang 을 늘 build_runner 로만 돌린다. `slang_build_runner` 가 없으면 생성되지 않는다 | SK-05 |
| `~/.pub-cache/hosted/pub.dev/slang-4.14.0/README.md` · `slang_build_runner-4.14.0/README.md` | `slang:49` · `:190` `dart run slang` · `:193` 「requires slang_build_runner」 · `slang_build_runner:7` · `:34` | 두 갈래가 설치본 문서에 있다 | SK-05 (근거) |
| `flutter-toolkit/evals/scenario-report/example/…/record.json` · `index.html` | `TC-001…/record.json:85` · `:89` · `:93` · `TC-002…/record.json:100` · `:104` · `:108` · `index.html:87` | 옛 도구 이름 넷(`login_as` · `tap_native_point` · `tap_widget` · `find_widget`) 26 번 | SK-08 |
| `flutter-toolkit/evals/scenario-report/test_build_report.py` · `skills/flutter-scenario-report/references/record-format.md` | `test_build_report.py:222-227` 예시 바이트 비교 · `record-format.md:62` 자리표시자 꼴 | 기록을 바꾸면 보고서를 다시 만들어야 시험이 통과한다 | SK-08 |
| `design-kit/references/visual-change-protocol.md` | `:372` `status: approved` · `:387-390` 규칙 두 줄 · `:410-417` 파일 열기 · `:437-441` 목록 검사 | `status` 값 목록이 없고, `excluded_surfaces` 키가 없어도 통과한다. 폴더 · UTF-8 아닌 입력은 오류 추적과 종료 코드 1 | SK-09 · SC-01 · ER-01 |
| `design-kit/evals/decision-gate-test.sh` | `:31` 입력 열 열 개 | 새 규칙을 재는 입력이 없다 | SC-02 |
| `design-kit/skills/design-test/SKILL.md` · `design-audit/SKILL.md` · `agents/design-reviewer.md` | `design-test:276-278` 「여기서 재정의하지 않는다」 · `:367` 검사 실행 · `design-audit:49` · `design-reviewer:53` | §6 을 가리키기만 한다 — 바꿀 것 없음 | SK-10 |
| `infra-kit/skills/infra-test/SKILL.md` | `:221` `OPTIONAL_TOOLS` · `:253-261` 규칙 1 · `:263-268` 규칙 2 python3 검사 · `:428` 알려진 답 | 규칙 1 이 줄 검사라 `run: \|` 안의 글자로 통과하고 흐름 표기 스텝을 놓친다(봉인 전 재현: block · flow · broken 셋이 틀린다) | SC-03 · SC-04 |
| `docs/infra/platform/cicd.md` · `infra-kit/README.md` · 설치본 `~/.claude/plugins/cache/joo6077-plugins/infra-kit/0.4.0/` | `cicd.md:77-81` 판정 세 줄 · `README.md:26` 「모든 스킬이 이를 SSOT로 참조」 · 설치본에 `docs/` 폴더 없음 | 원칙 문서 열두 개 전부가 설치본에 없다 | 넘김 (`## 범위 경계`) |
| `react-kit/skills/react-init/SKILL.md` | `:90` harness `vm_port` 언급 · `:253-257` 단계 13 | 틀을 복사하는 절차가 없다 | SK-11 |
| `react-kit/templates/harness-project.yaml.template` · `harness/templates/project.yaml` · `harness/skills/init/SKILL.md` | 틀 `:3` `stack: "react"` · `:98` `vm_port: 5173` · 기본 틀 `:59` `vm_port: null` · init `:17` · `:54` | 기본 틀로는 react-init `:90` 의 5173 약속이 안 선다. init 은 `.harness/` 가 있으면 멈춘다 | SK-11 (근거) |
| `docs/react/kit-design/final-integration.md` | `:486` 「`/react-init` 이 `/harness init` 을 함께 호출할 때 … 복사」 | 설계는 복사를 정해 두었다 | SK-11 (근거) |
| `react-kit/README.md` | `:55-57` 빠른 시작 2 번 `/harness init` | react-init 13 단계와 겹친다 | SK-12 |
| `.claude/kaizen-input/insights-report.md` · `.harness/.meta/kaizen-0924/phase5-notes.md` · `phase10-notes.md` | `insights-report.md:66` 「기준 커밋 가르기 규칙이 … 세 곳이다 — 카이젠에서 하나로 정한다」 · `phase5-notes.md:77` · `phase10-notes.md:66` | flutter-preflight 에 넣을 근거가 저장소에 없다 | 넘김 (`## 범위 경계`) |

## Skill

- [ ] SK-01: widget-inspector 감지 기준 7 의 제목과 본문이 같은 말을 한다 — Given 호출 스킬이 관례 표를 넘기지 않는 두 경우(호출 프롬프트가 「관례 표 없는 호출」 이라고 밝힌 경우 · 아무 말 없이 표만 빠진 경우), When 에이전트가 §7 을 따르면, Then 앞의 경우는 §7 을 건너뛰고 리포트 Convention Match 칸에 `건너뜀 — 관례 표 없는 호출` 한 줄을 적고(`[미검증]` 이 아니다), 뒤의 경우는 지금처럼 `[미검증] 관례 표 없음` 을 적는다. §7 제목에서 「관례 표를 받았을 때」 가 빠지고, `## Rules` 절도 두 경우를 같은 말로 가른다. 평가 사례 16 의 단언은 뒤의 경우라 그대로 맞는다. 측정: `m SK-01` 이 네 값 `a b c d` 를 내고 a=0 · b≥1 · c≥1 · d≥1 (a 는 제목 줄(`#` 으로 시작하는 줄)의 「관례 표를 받았을 때」 줄 수 — 옛 이력을 설명하는 본문 줄은 세지 않는다, b · c 는 §7 절의 두 문구 줄 수, d 는 `## Rules` 절의 건너뜀 문구 줄 수. 시작 판 `1 0 1 0` — a=1 이 양성 대조) [exact, enumerated]
- [ ] SK-02: 호출하는 쪽이 짝을 맞춘다 — flutter-feature 의 `## Post-Creation: Widget Inspector` 절이 widget-inspector 를 부를 때 「관례 표 없는 호출」 임을 프롬프트에 밝힌다고 적는다(보일러플레이트만 만들어 관례 표를 만들지 않는 스킬이라서). 표를 넘기는 flutter-widget · flutter-screen 의 호출 문장(「편집 전에 만든 관례 표(규약 Step 0 의 6 번)를 함께 넘긴다」)은 각 1 줄 그대로다. 측정: `m SK-02` 가 `x 1 1` 이고 x≥1 (시작 판 `0 1 1`) [exact, enumerated]
- [ ] SK-03: build_runner 의 `--delete-conflicting-outputs` 는 명령에서 빼지 않고, 남기는 이유를 flutter-build Gotchas 에 근거와 함께 적는다 — flutter-run · flutter-build · flutter-preflight 세 스킬의 codegen 명령 줄(`$DART run build_runner build --delete-conflicting-outputs`)이 각 2 줄 그대로이고, flutter-build `## Gotchas` 절에 (a) 2.7.0 이상은 이 플래그를 무시하고 늘 지운다 (b) 2.7.0 미만은 플래그가 없으면 대화 없이 도는 실행에서 충돌하는 생성물 앞에서 빌드가 멈춘다 — 두 가지가 pub 설치본 근거(`build_runner-2.13.1/CHANGELOG.md:150` · `build_runner_core` 7.3.2 · 8.0.0 의 `build_definition.dart:564-570`)와 함께 적혀 있다. 새 내용은 이미 있는 2.16 항목(「`--delete-conflicting-outputs` 로 생성물이 안전하다고 믿지 마라」 줄)과 따로 놀지 않도록 그 항목 한 줄 안에 이어 쓰고, 그 줄이 「빼지 않는다」 는 결론까지 담는다 — 판별 구간 셋(2.7.0 미만 · 2.7.0 이상 · 2.16 이후)이 한 항목에서 읽힌다. 측정: `m SK-03` 이 `a b j 2 2 2` 이고 a≥1(Gotchas 절의 `2.7.0` 줄 수) · b≥1(같은 절의 `build_runner_core` 줄 수) · j≥1(같은 절에서 `2.16` · `2.7.0` · `build_runner_core` · `빼지 않는다` 넷을 모두 담은 줄 수) (시작 판 `0 0 0 2 2 2`). 플래그를 명령에서 지우면 뒤 세 값이 0 이 되고, 새 내용을 2.16 줄과 다른 항목에 따로 쓰면 j 가 0 이다 [exact, enumerated]
- [ ] SK-04: flutter-scenario-report 가 golden · integration_test 로 감지된 프로젝트에서도 MCP(앱을 조작하는 도구 서버)가 있으면 진행한다 — project-detection Step 8 은 채널 하나만 고르고 golden(1 순위) · integration_test(2 순위)가 MCP(3 순위)보다 앞선다. Given 골든 시험과 등록된 MCP 서버가 둘 다 있는 프로젝트, When 스킬 1 단계를 따르면, Then `VISUAL_CHANNEL` 값이 아니라 Step 8 표 3 행 감지로 서버 이름을 얻어 진행하고, 3 행이 서버 이름을 못 찾을 때만 멈추고 알린다. 1 단계 절(`### 1. 프로젝트 감지` 부터 `### 2.` 앞까지)에서 옛 문장 「`VISUAL_CHANNEL` 이 `mcp:<서버명>` 이어야 이 스킬을 쓸 수 있다」 · 옛 완료 기준 「채널 줄(`VISUAL_CHANNEL = mcp:<서버명>`)」 이 각 0 이고, `golden` · `integration_test` 가 각 1 줄 이상, 그 두 낱말 줄 가운데 멈춘다는 줄은 0, 멈추는 줄(「멈춘다」 · 「멈추고」)은 1 이상이며, 멈추는 줄은 모두 멈추는 경우를 「서버 이름」 을 「못 찾」 을 때로 한정한다 — 「MCP 서버가 없으면 멈춘다」 처럼 더 넓게 쓴 멈춤 줄은 일곱째 값을 1 이상으로 만든다. 측정: `m SK-04` 가 `0 a b 0 c 0 0` 이고 a≥1 · b≥1 · c≥1 (일곱째 값은 멈추는 줄 가운데 `서버 이름` 과 `못 찾` 을 함께 담지 않은 줄 수. 시작 판 `1 0 0 0 1 1 1`). 넷째 값 양성 대조: `printf 'golden 이면 멈추고 알린다\n' | grep -E 'golden|integration_test' | grep -cE '멈춘다|멈추고'` 가 1 · 일곱째 값 양성 대조: `printf 'MCP 서버가 없으면 멈춘다\n' | grep -E '멈춘다|멈추고' | awk 'index($0,"서버 이름")==0 || index($0,"못 찾")==0' | grep -c .` 가 1 (봉인 전 실측) [exact, enumerated]
- [ ] SK-05: flutter-l10n 의 slang 코드 생성이 두 갈래다 — pubspec 에 `slang_build_runner` 가 있으면 flutter-run codegen 절 블록(build_runner)으로, 없으면 `$DART run slang` 으로 돌린다(근거: pub 설치본 `slang-4.14.0/README.md:190` · `:193`, `slang_build_runner-4.14.0/README.md:7`). Step 6 절(`### 6. Codegen 실행` 부터 `### 7.` 앞까지)에 `slang_build_runner` · `$DART run slang` 이 각 1 줄 이상이고, Gotchas 의 「번역 키 추가 후 반드시 codegen 재실행」 줄이 두 갈래를 한 줄에 담으며(1), 옛 고정 명령 `fvm dart run slang` 은 0 이다. 측정: `m SK-05` 가 `a b 1 0` 이고 a≥1 · b≥1 (시작 판 `0 0 0 0`). 마지막 값 양성 대조: `git -C W show 535e143~1:flutter-toolkit/skills/flutter-l10n/SKILL.md | grep -cF 'fvm dart run slang'` 가 1 (봉인 전 실측) [exact, enumerated]
- [ ] SK-06: project-detection Step 2b 가 Makefile 타겟을 하나씩 확인한다 — Given `app-preflight:` 타겟 하나만 있는 Makefile, When Step 2b 절(`### Step 2b.` 부터 `### Step 3.` 앞까지) bash 코드 블록의 확인 명령 한 줄(`<타겟>` 자리표시자를 쓰고 `Makefile` 을 읽는 줄)을 타겟 이름마다 바꿔 넣어 돌리면, Then `app-codegen` · `app-analyze` · `app-fix` · `app-test` 는 0 이 아닌 종료 코드, `app-preflight` 는 0 이고, `app-codegen: ## gen` 처럼 뒤에 설명이 붙은 타겟도 0 이다. 그리고 그 절에 「그 타겟이 없으면 그 행은 기본 동작」 뜻의 줄(`타겟` · `없으면` · `기본 동작` 을 함께 담은 줄)이 1 이상이다 — 묶음 타겟만 있는 Makefile 은 표의 모든 행이 기본 동작이 된다. 측정: `m SK-06` 이 `lines=1 rule=r app-codegen=x1 app-analyze=x2 app-fix=x3 app-test=x4 app-preflight=0 comment_target=0` 이고 r≥1 · x1~x4 모두 0 이 아니다 (시작 판 `lines=0 rule=0`). 알려진 답: 확인 줄을 `grep -qE '^<타겟>[[:space:]]*:' Makefile` 로 넣은 임시 복제본에서 `lines=1 rule=1 app-codegen=1 app-analyze=1 app-fix=1 app-test=1 app-preflight=0 comment_target=0` · 종료 코드 0 (봉인 전 실측) [exact, enumerated]
- [ ] SK-07: Makefile 타겟을 쓰는 두 소비자가 Step 2b 의 타겟별 확인을 따른다 — flutter-run codegen 절의 옛 문장 「`HAS_MAKEFILE = true` 면 두 줄을 `$MAKE app-codegen` 으로 바꾼다」 와 flutter-ai-rules 의 옛 문장 「`HAS_MAKEFILE = true` 감지 시 `make <target>` 우선」 이 각 0 이고, 바꾼 줄(`$MAKE app-codegen` 을 담은 flutter-run 줄 · `make <target>` 을 담은 flutter-ai-rules 줄)이 각각 `Step 2b` 를 가리킨다. 측정: `m SK-07` 이 `0 a 0 b` 이고 a≥1 · b≥1 (시작 판 `1 0 1 0`) [exact, enumerated]
- [ ] SK-08: scenario-report 시험 예시에 옛 도구 이름이 없고 예시 보고서가 기록과 맞는다 — Given 두 예시 기록의 `run` 칸에서 `login_as` · `tap_native_point` · `tap_widget` · `find_widget` 을 `record-format.md:62` 와 같은 꼴의 자리표시자(예: `<누르기 도구>`)로 바꾸고 예시 `index.html` 을 `build_report.py` 로 다시 만든 뒤, When `python3 -m unittest discover -s flutter-toolkit/evals/scenario-report` 를 돌리면, Then 종료 코드 0 · 마지막 줄 `OK` 이고 예시 폴더의 `.json` · `.html` 안 네 이름 등장 수가 0 이다. 캡처 PNG 는 건드리지 않는다(AR-01 기대 집합에 없다). 측정: `m SK-08` 이 `names=0 ut_rc=0 ut_last=OK` (시작 판 `names=26 ut_rc=0 ut_last=OK`). 음성 대조: `m SK-08N` — 기록 제목만 바꾸고 보고서를 다시 만들지 않은 사본에서 `neg_rc=1` 이고 실패 이름 `test_example_report_is_current` 가 나온다 (봉인 전 실측 `neg_rc=1 2`) [exact, enumerated]
- [ ] SK-09: 결정 전파 문서 §6 이 두 규칙을 적는다 — (a) `status` 에 쓸 수 있는 값은 `approved` 하나이고 다른 값이나 빠진 값은 형식 오류(종료 코드 2)다 — 근거는 같은 절 `:387-388` 「승인 기록 없는 결정은 manifest 에 올리지 않는다」 (b) `excluded_surfaces` 키는 늘 적고, 제외할 표면이 없으면 `excluded_surfaces: []` 로 적는다. 키가 없으면 침묵이라 커버리지 위반(종료 코드 1)이다 — 근거는 `:389-390`. 측정: `m SK-09` 가 `a b` 이고 a≥1(§6 절에서 백틱 `status` 와 백틱 `approved` 를 함께 담은 줄 수) · b≥1(백틱 `excluded_surfaces: []` 줄 수) (시작 판 `0 0`) [exact, enumerated]
- [ ] SK-10: 결정 전파 문서의 소비자 셋은 고치지 않는다 — design-test · design-audit · design-reviewer 는 형식과 규칙을 §6 에서 가져오고 스스로 다시 정하지 않으므로(`design-test/SKILL.md:277-278` 「여기서 재정의하지 않는다」) 새 규칙을 따로 옮기지 않는다. Given 구현 커밋이 끝난 뒤, 세 파일이 시작점과 끝점 사이에 바뀌지 않았고 셋 다 `visual-change-protocol.md` 를 가리킨다. 측정: `m SK-10` 이 `changed=0 cite=a b c` 이고 a · b · c 모두 ≥1 (시작 판 `changed=0 cite=6 5 4`). 양성 대조: AR-01 양성 대조와 같은 임시 복제본에서 같은 diff 명령이 바뀐 파일을 센다(`changed=5`, 봉인 전 실측) [structural, enumerated]
- [ ] SK-11: react-init 13 단계가 react-kit 틀을 쓴다 — `### 단계 13` 절에 `/harness init` 로 `.harness/` 를 만든 뒤 킷의 `templates/harness-project.yaml.template` 을 `.harness/project.yaml` 로 덮어 쓰는 절차가 있다(init 은 `.harness/` 가 있으면 멈추므로 init 이 먼저다 — `harness/skills/init/SKILL.md:17` · `:54`). 틀은 지우지 않고 `vm_port: 5173` 줄도 그대로다 — react-init `:90` 의 포트 고정이 harness `vm_port` 5173 에 기대는데 harness 기본 틀은 `vm_port: null`(`harness/templates/project.yaml:59`)이다. 측정: `m SK-11` 이 `tpl=a dst=b init_line=i tpl_line=t vm_port=1` 이고 a≥1 · b≥1 · 0<i<t (절 안에서 `/harness init` 첫 줄이 틀 경로 첫 줄보다 앞선다. 시작 판 `tpl=0 dst=1 init_line=4 tpl_line=0 vm_port=1`) [exact, enumerated]
- [ ] SK-12: react-kit README 빠른 시작이 react-init 13 단계와 어긋나지 않는다 — `## Quickstart` 절에 react-init 뒤 따로 부르는 `/harness init` 줄이 없다(react-init 이 이미 `.harness/` 를 만들어 두어, 뒤에 부르면 init 이 「이미 있다」 로 멈춘다). 측정: `m SK-12` 가 `harness_init=0 react_init=r` 이고 r≥1 (시작 판 `harness_init=1 react_init=1`) [exact, enumerated]

## Script

- [ ] SC-01: 결정 전파 검사가 상태 값과 제외 표면 키를 가른다 — Given §6 에서 뗀 검사 코드와 손으로 만든 입력 다섯(모두 형식이 맞는 `decision_id` · `source`, golden 과 `main visible` 단언이 있는 표면 하나): `ok`(`status: approved` · `excluded_surfaces: []`) · `draft`(`status: draft`) · `nostatus`(`status` 없음) · `noexc`(`status: approved`, `excluded_surfaces` 키 없음) · `bothempty`(`status: approved`, 두 목록 다 `[]`), When 각각 돌리면, Then 종료 코드/오류 추적 줄 수가 `ok=0/0 draft=2/0 nostatus=2/0 noexc=1/0 bothempty=1/0` 이다. 기대값은 문서 규칙에서 손으로 정했다 — 구현이 낸 값을 옮긴 것이 아니다. 측정: `m SC-01` (시작 판 `ok=0/0 draft=0/0 nostatus=0/0 noexc=0/0 bothempty=1/0`) [exact, enumerated]
- [ ] SC-02: 기존 시험 `decision-gate-test.sh` 가 새 규칙을 잰다 — 자기 입력 열에 폴더 · UTF-8 아닌 파일 · 상태 값 · 제외 표면 키 경우를 더해 통과하고, 옛 검사 코드로 돌리면 그 경우들이 어긋난다. 측정: `m SC-02` 가 `rc=0 [결과: N 경우 중 불일치 0]` 이고 N≥16, 같은 줄 `base_doc:` 뒤가 tb≥2 · to2≥1 · to1≥1 이다 — 시작점의 `visual-change-protocol.md` 를 `DECISION_GATE_DOC` 로 준 실행에서 폴더 · UTF-8 경우가 `Traceback=1` 로, 상태 경우가 `rc=0 (답 2)` 로, 제외 표면 경우가 `rc=0 (답 1)` 로 어긋난다. 음성 대조: 그 옛 문서 실행 자체다 (시작 판 `rc=0 [결과: 10 경우 중 불일치 0] base_doc: tb=0 to2=0 to1=0`) [exact, enumerated]
- [ ] SC-03: infra-test 규칙 1(checkout 스텝)이 워크플로를 YAML 구조로 읽는다 — Given `**구조 검증 스크립트**` 아래 bash 블록을 뗀 스크립트와 워크플로 하나짜리 폴더 여섯(주석에만 checkout · 보통 스텝 · 작은따옴표로 싼 SHA 고정 스텝 · `run: |` 안의 글자 · 흐름 표기 `- {uses: actions/checkout@v4}` · 읽을 수 없는 YAML), When python3 와 PyYAML 이 있는 환경에서 `WF_DIR` 로 하나씩 돌리면, Then 규칙 1 결과(`checkout 존재` 줄 수/`checkout 스텝 없음` 줄 수/종료 코드)가 `comment=0/1/1 step=1/0/1 quoted=1/0/0 block=0/1/1 flow=1/0/1` 이고 읽을 수 없는 YAML 은 `broken=0/*/2`(`*` 는 아무 값 — `checkout 존재` 가 0 이고 종료 코드 2)이며, 문서 `:428` 의 알려진 답 입력(checkout@v4 · SHA 고정 액션 · `@v4` 태그 액션)은 그대로 `ka=1/0/1 refs=1 perref=2 total=1` 이다. 출력 문구 `checkout 존재` · `checkout 스텝 없음` 은 지금 글자 그대로 쓴다. 측정: `m SC-03` (시작 판 `comment=0/1/1 step=1/0/1 quoted=1/0/0 block=1/0/0 flow=0/1/1 broken=1/0/2 | ka=1/0/1 refs=1 perref=2 total=1` — block · flow · broken 셋이 지금 틀린다) [exact, enumerated]
- [ ] SC-04: python3 나 PyYAML 이 없어도 규칙 1 은 돈다 — Given `PATH` 를 bash 와 `/usr/bin/grep` 만 있는 폴더로 좁힌 환경(python3 없음)과, 거기에 `/usr/bin/python3`(PyYAML 없음)을 더한 환경, When 보통 스텝(`step`)과 주석(`comment`) 워크플로에 돌리면, Then 두 환경 모두 `step=1/0/2 comment=0/1/2` 이고(규칙 1 은 줄 검사로 판정, 규칙 2 는 `[미검증]` 이라 종료 코드 2), `comment` 출력에 규칙 1 이 YAML 구조 대신 줄 검사로 돌았다는 줄(`checkout` 과 `python3` 또는 `PyYAML` 을 함께 담은 줄)이 1 이상이다. 규칙 1 을 `[미검증]` 으로 돌리지 않는다 — `.harness/sprint-contract-kaizen-0924-f1-kit-followups.md:349`(입력 표 71 행)의 결정을 따른다. 측정: `m SC-04` 가 `nopy_python3=없음 nopyyaml_python3=1 nopyyaml_yaml=없음 | nopy: step=1/0/2 comment=0/1/2 py=a | nopyyaml: step=1/0/2 comment=0/1/2 py=b` 이고 a≥1 · b≥1 (시작 판 a=0 · b=0. 앞 전제 셋은 봉인 전 실측 값과 같다) [exact, enumerated]

## Error

- [ ] ER-01: 결정 전파 검사가 입력 오류를 종료 코드 2 로 낸다 — Given 폴더 경로와 UTF-8 이 아닌 바이트(`\377\376`)가 든 파일, When §6 검사 코드에 주면, Then 둘 다 종료 코드 2 이고 오류 추적(`Traceback`) 줄이 0 이다. 지금은 `IsADirectoryError` · `UnicodeDecodeError` 추적과 종료 코드 1 이라 커버리지 위반으로 읽힌다. 측정: `m ER-01` 이 `dir=2/0 nonutf8=2/0` (시작 판 `dir=1/1 nonutf8=1/1` — 양성 대조) [exact, enumerated]

## Architecture

- [ ] AR-01: 바뀐 파일이 기대 집합 안이고 한 커밋에 킷 하나다 — Given 구현 · notes · QA 리포트 커밋이 모두 가지 `chore/ak-c3-kits` 에 들어간 뒤, 시작점 `BASE=$(git -C W merge-base origin/main chore/ak-c3-kits)` 부터 끝점 `TIP=$(git -C W rev-parse --verify chore/ak-c3-kits)` 까지(`HEAD` 를 쓰지 않는다. 해석이 안 되면 `UNRESOLVED` 로 멈춘다) `git diff --name-only` 로 모은 경로가 측정 도우미 `ALLOWED` 의 스무 경로 안에만 있고(부분 집합, 생성물 제외 없음 — 예시 `index.html` 은 기대 집합에 이름으로 들어 있다), 네 킷이 각 1 경로 이상이며, 커밋마다 맨 위 폴더가 하나뿐이다(킷 넷과 `.harness` 가운데 하나). 측정: `m AR-01` 이 extra=0 · 네 킷 값 ≥1 · multi_top=0 (시작 판: 구간이 비어 `changed=0`). 양성 대조: 임시 복제본에서 두 킷과 범위 밖 파일 하나를 한 커밋에 넣으면 `extra=1` · `multi_top=1` 이고 남는 경로를 출력한다 (봉인 전 실측) [exact, collective]
- [ ] AR-02: 결정과 넘김을 notes 에 남긴다 — Given 끝점 `TIP`, notes 파일 `.harness/.meta/after-kaizen-0926/c3a-notes.md` 가 커밋돼 있고 열세 토큰(`flutter-preflight` · `docs/infra/platform/cicd.md` · `2.16` · `build_runner_core` · `approved` · `excluded_surfaces` · `harness-project.yaml.template` · `관례 표 없는 호출` · `tone-guide` · `docs/design-kit/visual-change-protocol.html` · `docs/flutter-toolkit/project-detection.html` · `docs/flutter-toolkit/flutter-ai-rules.html` · `docs/infra-kit/infra-test.html`)이 각 1 줄 이상이다. 담을 내용: 넘긴 것(flutter-preflight 기준 커밋 비교 · cicd.md 판정 세 줄 구조 · build_runner 2.16 이후 동작 · `approved` 밖의 상태 값)과 사유, 이 계약의 결정(플래그 유지 · 상태 값 · 제외 표면 키 · 틀 사용 · 관례 표 없는 호출)과 근거, tone-guide 5 단계 대조 결과, 원본이 바뀌어 다시 만들어야 할 문서 페이지(문서 사이트는 이 계약 범위 밖). 측정: `m AR-02` 가 `committed=1` 과 1 이상 열셋 (시작 판 `committed=0` 과 0 열셋). 양성 대조: 임시 복제본에 열세 토큰을 담은 notes 를 커밋하면 `committed=1` 과 1 열셋 (봉인 전 실측) [exact, enumerated]

## Anti-patterns

- [ ] AP-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수 (```text, ```bash, ```yaml 등). 판정 권위는 validate-plugin V6 상태기계다 — 여는/닫는 fence 가 동형이라 줄 단위 정규식으로는 판정 불가. 측정: 끝점을 풀어 둔 판 `E` 에서 `python3 "$E/scripts/validate-plugin.py" --check=code-fence` 종료 코드 0 (시작 판 0). 양성 대조: 임시 복제본의 flutter-l10n SKILL.md 끝에 언어 없는 fence 를 붙이면 `V6 code-fence 1 bare — FAIL` · 종료 코드 2 (봉인 전 실측)
- [ ] AP-04: SKILL.md / agents/*.md frontmatter 에서 name 필드 누락 — validate-plugin V1 FAIL. 측정: `python3 "$E/scripts/validate-plugin.py" --check=frontmatter` 종료 코드 0 (시작 판 0). 양성 대조: 임시 복제본의 flutter-build SKILL.md 에서 `name:` 줄을 지우면 `누락 필드 ['name']` · 종료 코드 2 (봉인 전 실측)

## Reusability

- [ ] RE-01: N/A (산출물이 문서 문장 · 시험 입력 · 문서 안 검사 코드 조각뿐이라 새 컴포넌트 · 함수 모듈이 없다. 측정: `git -C W diff --diff-filter=A --name-only BASE TIP -- flutter-toolkit design-kit infra-kit react-kit` 가 0 줄)
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다 — 새 시험 파일 · 새 검사 스크립트를 만들지 않고 기존 `decision-gate-test.sh` 입력 열과 infra-test 스크립트의 기존 YAML 읽기(규칙 2 의 `yaml.safe_load`)를 다시 쓴다. 측정: RE-01 의 명령이 0 줄

## Diagnostics

- [ ] DG-01: N/A (commands.analyze `bash -n scripts/release.sh` 가 재는 `scripts/release.sh` 는 이번 바뀐 파일에 없다. 측정: `git -C W diff --name-only BASE TIP | grep -cx 'scripts/release.sh'` 가 0)
- [ ] DG-02: IDE diagnostics 워닝/인포 0개 ([] 제외) — IDE(편집기) 진단을 명령줄로 같게 잰다: 바뀐 `.md`(계약 · QA 리포트 · 개정 파일 제외)의 더해진 줄에 걸린 markdownlint-cli2 0.23.2(MD013 끔, 편집기 확장과 같은 설정) 경고 0 · `decision-gate-test.sh` 의 더해진 줄에 걸린 shellcheck 경고 0 · 바뀐 `.json` 읽기 실패 0. 측정: `m DG-02` 가 `md_new=0 sh_new=0 json_bad=0` (도구가 없으면 도우미 `mdl_ready` 가 임시 폴더에 설치한다). 양성 대조: 임시 복제본에 `#bad heading` 줄 · `echo $UNQUOTED` 줄 · 깨진 JSON 을 넣으면 `md_new=3 sh_new=1 json_bad=1` (봉인 전 실측)
- [ ] DG-03: N/A (commands.test `bash scripts/release.sh 2>&1 || true` 가 재는 `scripts/release.sh` 는 이번 바뀐 파일에 없다. 측정: DG-01 과 같은 명령이 0)
- [ ] DG-04: N/A (구동할 앱 · 서버가 없다 — 바뀐 파일이 스킬 문서 · 참조 문서 · 시험 입력 · 시험 스크립트뿐. 대신 DG-05 가 CI 단계를 전부 돌린다)
- [ ] DG-05: CI(자동 검사) 단계를 로컬에서 전부 돌려 통과한다 — Given 작업 폴더 W 가 끝점과 같다(`git -C W rev-parse HEAD` 가 `TIP` 이고 `git -C W status --porcelain --untracked-files=no` 가 빈 출력), When `TMPDIR=<임시 폴더> bash /Users/jackson/Hub/10_Dev/claude-plugins/.harness/handoff/2026-09-26-tools/ci-local.sh /Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak-c3` 를 돌리면, Then 요약(`$TMPDIR/ci-local/summary.txt`)에 `rc=0` 줄이 22 개이고 `rc=0` 이 아닌 줄은 `feedback-agg-test SKIP (yq 없음)` 하나뿐이다. 측정: `grep -c 'rc=0' "$TMPDIR/ci-local/summary.txt"` 가 22 · `grep -v 'rc=0' "$TMPDIR/ci-local/summary.txt"` 가 그 한 줄 (시작 판 봉인 전 실측: 22 · SKIP 한 줄). 음성 대조: 이 묶음이 기대는 `scenario-report-ut` · `decision-gate-test` 단계는 SK-08N · SC-02 의 옛 문서 실행이 보여 주듯 구현을 되돌리면 실패한다

## 범위 경계

항목별 처리 — 입력은 핸드오프 §C3 의 네 킷 줄과 과제 목록이다.

| 킷 | 항목 | 처리 | 조건 · 사유 |
| --- | --- | --- | --- |
| flutter-toolkit | `widget-inspector.md` §7 제목 · 본문 | 계약에 넣음 | SK-01 · SK-02. flutter-feature 는 관례 표를 만들지 않는 스킬(`:196-200`)이라 「밝힌 표 없음 = 건너뜀」 · 「말 없는 표 없음 = `[미검증]`」 으로 가른다 |
| flutter-toolkit | flutter-preflight 기준 커밋 비교 | 넘김 | 저장소 안에 flutter 쪽에 넣을 근거가 없다 — Phase 5 · 10 이 같은 사유로 넘겼다(`phase5-notes.md:77` · `phase10-notes.md:66`). 가르기 규칙이 이미 세 곳이고 처리 배정표가 「하나로 정한다」 를 먼저 요구한다(`insights-report.md:66`) — 넷째 사본을 만들지 않는다 |
| flutter-toolkit | build_runner `--delete-conflicting-outputs` 빼기 | 계약에 넣음 — 결정은 「빼지 않는다」 | SK-03. 2.7.0 이상은 무시, 2.7.0 미만은 빼면 대화 없는 실행이 멈춘다(`## GAP 분석` 의 pub 설치본 근거). 2.16 이후 동작은 설치본이 없어 넘김 |
| flutter-toolkit | scenario-report `VISUAL_CHANNEL` 이 golden 일 때 | 계약에 넣음 | SK-04 |
| flutter-toolkit | flutter-l10n slang 명령 두 갈래 | 계약에 넣음 | SK-05 |
| flutter-toolkit | project-detection Makefile 타겟마다 확인 | 계약에 넣음 | SK-06 · SK-07 |
| flutter-toolkit | scenario-report 시험 예시의 옛 도구 이름 | 계약에 넣음 | SK-08 |
| design-kit | 결정 전파 검사 `status` 값 목록 · 빈 `excluded_surfaces` 규칙 | 계약에 넣음 | SK-09 · SC-01 · SC-02 · SK-10. 값은 `approved` 하나(`:387-388`). `superseded` 같은 다른 값은 저장소 근거가 없어 넘김 |
| design-kit | 폴더 · UTF-8 아닌 입력을 종료 코드 2 로 | 계약에 넣음 | ER-01 · SC-02 |
| infra-kit | infra-test checkout 판정을 YAML 구조로 · python3 없을 때 규칙 1 | 계약에 넣음 | SC-03 · SC-04. python3 · PyYAML 이 없으면 줄 검사로 남긴다 |
| infra-kit | 판정 세 줄이 `docs/infra/platform/cicd.md` 에만 있는 구조 | 넘김 | 원칙 문서 열두 개 전부가 같은 구조다(`infra-kit/README.md:26`, 설치본 `infra-kit/0.4.0` 에 `docs/` 없음). 세 줄만 킷으로 옮기면 넷째 사본이 되고, 문서 전체를 킷 안으로 옮기면 `scripts/` · `.claude/skills/docs-site` 의 원본 ↔ 페이지 짝까지 바뀌어 이 계약 범위 밖이다 |
| react-kit | `harness-project.yaml.template` 복사 절차 | 계약에 넣음 — 결정은 「쓴다」 | SK-11 · SK-12. 설계(`final-integration.md:486`)와 포트 약속(react-init `:90`)이 틀을 전제한다 |

범위 밖(이 계약이 고치지 않는다): rust-kit · api-kit 뷰어 · reviewer 에이전트의 미검증 규칙 · `docs/` HTML 페이지(다시 만들 페이지는 notes 에 적어 문서 사이트 묶음으로 넘긴다) · `scripts/` · `harness/` · `.claude/` · 킷 `plugin.json` 버전(릴리스 단계 몫) · react-preflight 기준 커밋 비교(이 묶음 과제 목록에 없다).

커버리지 해소 — Step 6.5 (4) 검출기가 낸 `UNCOVERED` 여섯 건과 AR-01 의 처리:

- 커버리지 해소: AR-01 — 경로 기대 집합은 측정 도우미 `ALLOWED` 한 곳에만 적는다(목록을 두 번 적지 않는다는 계약 형식 규칙)
- 커버리지 해소: SK-05 — 산문의 README 두 경로는 근거 인용이지 잴 대상이 아니다
- 커버리지 해소: SK-08 — `.json` · `.html` · 예시 보고서는 `m SK-08` 의 `--include` 두 개와 단위 시험이 덮고, `build_report.py` 는 그 시험이 부른다
- 커버리지 해소: SK-10 — 문서 이름은 `m SK-10` 의 `cite` 가 세는 토큰이고, design-test 줄 번호는 근거 인용이다
- 커버리지 해소: SK-11 — `.harness/project.yaml` · 틀 경로는 `m SK-11` 의 `dst` · `tpl` 이 세고, harness 파일 두 줄은 근거 인용이다
- 커버리지 해소: SC-04 — `/usr/bin/python3` · `/usr/bin/grep` 은 `m SC-04` 가 만드는 좁힌 `PATH` 의 구성물이고, f1 계약 경로는 근거 인용이다
- 커버리지 해소: AR-02 — 열세 토큰과 notes 경로는 `m AR-02` 의 토큰 목록과 `NOTES` 변수가 덮는다
- 오라클 해소: SK-04 — 산출물이 스킬 1 단계의 절차 문장이라 부를 코드가 없다. 옛 문장 0 · 두 낱말 줄의 멈춤 0 · 멈춤 줄의 한정(일곱째 값)과 양성 대조 둘로 잰다. SK-01 · SK-02 · SK-05 · SK-07 · SK-09 · SK-11 · SK-12 도 같은 사유다 — 실행해서 재는 조건은 SK-06 · SK-08 · SC-01~04 · ER-01 이다
- notes 경로: 구현 지시가 정한 `.harness/.meta/after-kaizen-0926/c3a-notes.md` 로 봉인 전에 맞췄다(작성 초안은 `kits-a-notes.md` 였다)

교차 진단 반영(봉인 전, qa-evaluator 1 회):

- SK-03 · SK-11 — 과제 목록을 뒤집는 결정 두 건. 교차 진단이 사용자 재확인을 권했으나 이 계약은 위임(`## 배경`)으로 합의를 받았고 「묻지 마라」 가 위임 문구다 — 묻지 않고 근거(`## GAP 분석` 의 pub 설치본 · 설계 문서)를 notes 에 남긴다. 사용자가 뒤집으면 개정 파일로 처리한다
- SK-03 — 새 문장이 이미 있는 2.16 줄과 이어지도록 한 항목 안에 쓰게 하고, 넷을 함께 담은 줄 수(j)를 측정에 더했다
- SK-04 — 멈추는 경우를 「서버 이름을 못 찾을 때」 로 한정했는지 재는 일곱째 값과 양성 대조를 더했다
- SK-01 — 옛 문구 검사를 제목 줄로 좁혔다(본문의 이력 설명에 걸리지 않게)

## 회귀 게이트 — 측정 도우미

평가 때 이 블록을 떼어 bash 에서 불러 쓴다. `TMPDIR` 은 평가자 임시 폴더로 준다. 도우미는 끝점을 `git archive` 로 풀어 재므로 작업 폴더의 미커밋 변경을 보지 않는다.
작업 폴더 밖 입력은 지우지 마라 — 도우미가 만든 `$T` 아래만 치워도 된다.

```bash
# 떼기: awk '/^# === 측정 도우미 시작/{f=1} f{print} /^# === 측정 도우미 끝/{exit}' <계약> > "$TMPDIR/kitsa-measure.sh"
# 부르기: bash -c 'source "$TMPDIR/kitsa-measure.sh" || exit 2; type m >/dev/null || exit 2; m SK-01'
# 시작 판: E_REF=BASE 를 주고 부른다
# === 측정 도우미 시작 (after-0924-kits-a) ===
# 쓰는 법: 이 블록을 파일로 떼어 bash 에서 source 한 뒤 `m <조건 ID>`. zsh 에서 부르지 마라.
# 잴 트리 E — 기본은 가지 끝(TIP)을 git archive 로 푼 임시 폴더. 시작 판을 재려면 E_REF=BASE.
W=${W:-/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak-c3}
BR=${BR:-chore/ak-c3-kits}
BASE=$(git -C "$W" merge-base origin/main "$BR") || { echo "UNRESOLVED BASE"; return 2 2>/dev/null || exit 2; }
TIP=$(git -C "$W" rev-parse --verify "$BR") || { echo "UNRESOLVED TIP"; return 2 2>/dev/null || exit 2; }
T=$(mktemp -d "${TMPDIR:-/tmp}/kitsa.XXXXXX")
snap() { mkdir -p "$2" && git -C "$W" archive "$1" | tar -x -C "$2"; }
case "${E_REF:-TIP}" in
  BASE) E=$T/base; snap "$BASE" "$E" ;;
  *)    E=$T/tip;  snap "$TIP" "$E" ;;
esac
FT=$E/flutter-toolkit
# s 로 시작하는 줄부터 e 로 시작하는 다음 줄 앞까지
sec() { awk -v s="$1" -v e="$2" 'index($0,s)==1{f=1;print;next} f&&index($0,e)==1{exit} f' "$3"; }
# 표준 입력에서 글자 그대로 든 줄 수 (0 건에도 0 을 찍는다)
n() { grep -cF -- "$1" || true; }
gate() {  # 결정 전파 검사 코드를 문서에서 뗀다 (decision-gate-test.sh 와 같은 awk)
  awk '/^```python/{b=1;n="";next} b&&/^```/{if(ok){exit} b=0;next} b{n=n $0 "\n"; if($0 ~ /Decision Propagation Coverage Gate/) ok=1} END{printf "%s", n}' \
    "$E/design-kit/references/visual-change-protocol.md" > "$T/gate.py"
}
runc() { o=$(python3 "$T/gate.py" "$1" 2>&1); rc=$?; printf '%s/%s' "$rc" "$(printf '%s\n' "$o" | grep -c '^Traceback')"; }
infra_script() {  # infra-test 의 구조 검증 스크립트 블록을 뗀다
  awk '/^\*\*구조 검증 스크립트\*\*/{f=1} f&&/^```bash/{b=1;next} b&&/^```/{exit} b' \
    "$E/infra-kit/skills/infra-test/SKILL.md" > "$T/ci-validation.sh"
}
wf() {  # wf <이름> <steps 아래 줄들> — 워크플로 하나짜리 폴더
  mkdir -p "$T/wf-$1"
  printf 'on: push\njobs:\n  b:\n    runs-on: ubuntu-latest\n    steps:\n%b' "$2" > "$T/wf-$1/w.yml"
}
r1() {  # r1 <이름> [PATH] — 규칙 1 줄 수와 종료 코드
  if [ -n "${2:-}" ]; then o=$(PATH="$2" WF_DIR="$T/wf-$1" bash "$T/ci-validation.sh" 2>&1); rc=$?
  else o=$(WF_DIR="$T/wf-$1" bash "$T/ci-validation.sh" 2>&1); rc=$?; fi
  printf '%s' "$o" > "$T/out-$1.txt"
  printf '%s=%s/%s/%s' "$1" "$(printf '%s\n' "$o" | n 'checkout 존재')" "$(printf '%s\n' "$o" | n 'checkout 스텝 없음')" "$rc"
}
wf_all() {
  wf comment '      # - uses: actions/checkout@v4\n      - run: echo hi\n'
  wf step    '      - uses: actions/checkout@v4\n'
  wf quoted  "      - name: co\n        uses: 'actions/checkout@8f4b7f84864484a7bf31766abe9204da3cbe65b3'\n"
  wf block   '      - run: |\n          uses: actions/checkout@v4\n'
  wf flow    '      - {uses: actions/checkout@v4}\n'
  wf broken  '      - uses: actions/checkout@v4\n    bad: [\n'
  wf ka      '      - uses: actions/checkout@v4\n      - uses: org/a@8f4b7f84864484a7bf31766abe9204da3cbe65b3\n      - uses: org/b@v4\n'
}
MDL=${MDL:-$T/mdl}
mdl_ready() {  # markdownlint-cli2 0.23.2 · MD013 끔 — 편집기 확장과 같은 설정
  [ -x "$MDL/node_modules/.bin/markdownlint-cli2" ] || { mkdir -p "$MDL" && (cd "$MDL" && npm install --no-save --no-audit --no-fund markdownlint-cli2@0.23.2 >/dev/null 2>&1); }
  printf '{ "config": { "MD013": false } }\n' > "$MDL/cfg.markdownlint-cli2.jsonc"
  [ -x "$MDL/node_modules/.bin/markdownlint-cli2" ]
}
added() { diff -U0 "$1" "$2" | awk '/^@@/{split($3,a,","); s=substr(a[1],2); c=(a[2]=="")?1:a[2]; for(i=0;i<c;i++) print s+i}'; }
newmd() {  # newmd <옛 파일|/dev/null> <새 파일> — 새 파일에서 더해진 줄에 걸린 경고 수
  ( cd "$(dirname "$2")" && "$MDL/node_modules/.bin/markdownlint-cli2" --config "$MDL/cfg.markdownlint-cli2.jsonc" "$(basename "$2")" 2>&1 ) \
    | awk -F: '/^[^ ]+:[0-9]+/{print $2+0}' | sort -n > "$T/w.txt"
  added "$1" "$2" | sort -n > "$T/a.txt"
  comm -12 "$T/w.txt" "$T/a.txt" | grep -c . || true
}
newsc() {  # newsc <옛 .sh> <새 .sh> — 더해진 줄에 걸린 shellcheck 경고 수
  shellcheck -f gcc "$2" 2>/dev/null | awk -F: '{print $2+0}' | sort -n > "$T/w.txt"
  added "$1" "$2" | sort -n > "$T/a.txt"
  comm -12 "$T/w.txt" "$T/a.txt" | grep -c . || true
}
ALLOWED='flutter-toolkit/agents/widget-inspector.md
flutter-toolkit/skills/flutter-feature/SKILL.md
flutter-toolkit/skills/flutter-build/SKILL.md
flutter-toolkit/skills/flutter-scenario-report/SKILL.md
flutter-toolkit/skills/flutter-l10n/SKILL.md
flutter-toolkit/skills/flutter-run/SKILL.md
flutter-toolkit/references/project-detection.md
flutter-toolkit/references/flutter-ai-rules.md
flutter-toolkit/evals/scenario-report/example/TC-001-transfer-leader-cancel/record.json
flutter-toolkit/evals/scenario-report/example/TC-002-appoint-vice-leader/record.json
flutter-toolkit/evals/scenario-report/example/index.html
design-kit/references/visual-change-protocol.md
design-kit/evals/decision-gate-test.sh
infra-kit/skills/infra-test/SKILL.md
react-kit/skills/react-init/SKILL.md
react-kit/README.md
.harness/sprint-contract-after-0924-kits-a.md
.harness/sprint-feedback-after-0924-kits-a.md
.harness/sprint-amendments-after-0924-kits-a.md
.harness/.meta/after-kaizen-0926/c3a-notes.md'
NOTES=.harness/.meta/after-kaizen-0926/c3a-notes.md

m() {
  case "$1" in
  SK-01) f=$FT/agents/widget-inspector.md; s7=$(sec '### 7. 관례 대조' '## Process' "$f")
    echo "$(grep -E '^#' "$f" | n '관례 표를 받았을 때') $(printf '%s\n' "$s7" | n '건너뜀 — 관례 표 없는 호출') $(printf '%s\n' "$s7" | n '[미검증] 관례 표 없음') $(sec '## Rules' '## ZZZ' "$f" | n '건너뜀 — 관례 표 없는 호출')" ;;
  SK-02) p=$(sec '## Post-Creation: Widget Inspector' '## Related Skills' "$FT/skills/flutter-feature/SKILL.md"); k='편집 전에 만든 관례 표(규약 Step 0 의 6 번)를 함께 넘긴다'
    echo "$(printf '%s\n' "$p" | n '관례 표 없는 호출') $(n "$k" <"$FT/skills/flutter-widget/SKILL.md") $(n "$k" <"$FT/skills/flutter-screen/SKILL.md")" ;;
  SK-03) g=$(sec '## Gotchas' '## ' "$FT/skills/flutter-build/SKILL.md"); c='$DART run build_runner build --delete-conflicting-outputs'
    echo "$(printf '%s\n' "$g" | n '2.7.0') $(printf '%s\n' "$g" | n 'build_runner_core') $(printf '%s\n' "$g" | grep -F '2.16' | grep -F '2.7.0' | grep -F 'build_runner_core' | n '빼지 않는다') $(n "$c" <"$FT/skills/flutter-run/SKILL.md") $(n "$c" <"$FT/skills/flutter-build/SKILL.md") $(n "$c" <"$FT/skills/flutter-preflight/SKILL.md")" ;;
  SK-04) s1=$(sec '### 1. 프로젝트 감지' '### 2.' "$FT/skills/flutter-scenario-report/SKILL.md")
    echo "$(printf '%s\n' "$s1" | n '`VISUAL_CHANNEL` 이 `mcp:<서버명>` 이어야 이 스킬을 쓸 수 있다') $(printf '%s\n' "$s1" | n 'golden') $(printf '%s\n' "$s1" | n 'integration_test') $(printf '%s\n' "$s1" | grep -E 'golden|integration_test' | grep -cE '멈춘다|멈추고' || true) $(printf '%s\n' "$s1" | grep -cE '멈춘다|멈추고' || true) $(printf '%s\n' "$s1" | n '채널 줄(`VISUAL_CHANNEL = mcp:<서버명>`)') $(printf '%s\n' "$s1" | grep -E '멈춘다|멈추고' | awk 'index($0,"서버 이름")==0 || index($0,"못 찾")==0' | grep -c . || true)" ;;
  SK-05) f=$FT/skills/flutter-l10n/SKILL.md; s6=$(sec '### 6. Codegen 실행' '### 7.' "$f")
    echo "$(printf '%s\n' "$s6" | n 'slang_build_runner') $(printf '%s\n' "$s6" | n '$DART run slang') $(grep -F '번역 키 추가 후 반드시 codegen 재실행' "$f" | grep -F 'slang_build_runner' | n '$DART run slang') $(n 'fvm dart run slang' <"$f")" ;;
  SK-06) s=$(sec '### Step 2b.' '### Step 3.' "$FT/references/project-detection.md")
    ls_=$(printf '%s\n' "$s" | awk '/^```bash/{b=1;next} b&&/^```/{b=0} b' | grep -F '<타겟>' | grep -F 'Makefile')
    line=$(printf '%s\n' "$ls_" | head -1); d=$T/mk; mkdir -p "$d"
    out="lines=$(printf '%s\n' "$ls_" | grep -c . || true) rule=$(printf '%s\n' "$s" | grep -F '타겟' | grep -F '없으면' | grep -cF '기본 동작' || true)"
    if [ -n "$line" ]; then
      printf 'app-preflight:\n\t@echo hi\n' > "$d/Makefile"
      for t in app-codegen app-analyze app-fix app-test app-preflight; do (cd "$d" && bash -c "${line//<타겟>/$t}") >/dev/null 2>&1; out="$out $t=$?"; done
      printf 'app-codegen: ## gen\n\t@echo hi\n' > "$d/Makefile"; (cd "$d" && bash -c "${line//<타겟>/app-codegen}") >/dev/null 2>&1; out="$out comment_target=$?"
    fi
    echo "$out" ;;
  SK-07) echo "$(n '`HAS_MAKEFILE = true` 면 두 줄을 `$MAKE app-codegen` 으로 바꾼다' <"$FT/skills/flutter-run/SKILL.md") $(grep -F '$MAKE app-codegen' "$FT/skills/flutter-run/SKILL.md" | n 'Step 2b') $(n '`HAS_MAKEFILE = true` 감지 시 `make <target>` 우선' <"$FT/references/flutter-ai-rules.md") $(grep -F 'make <target>' "$FT/references/flutter-ai-rules.md" | n 'Step 2b')" ;;
  SK-08) ex=$FT/evals/scenario-report/example
    c=$(grep -roE --include='*.json' --include='*.html' 'login_as|tap_native_point|tap_widget|find_widget' "$ex" | grep -c . || true)
    (cd "$E" && python3 -m unittest discover -s flutter-toolkit/evals/scenario-report) > "$T/ut.log" 2>&1; rc=$?
    echo "names=$c ut_rc=$rc ut_last=$(tail -1 "$T/ut.log")" ;;
  SK-08N) # 음성 대조 — 기록만 고치고 보고서를 다시 만들지 않으면 예시 시험이 실패해야 한다
    cp -R "$E/flutter-toolkit" "$T/ftneg"; r=$T/ftneg/evals/scenario-report/example/TC-001-transfer-leader-cancel/record.json
    python3 - "$r" <<'PY'
import json, sys
p = sys.argv[1]; d = json.load(open(p, encoding="utf-8")); d["title"] = d["title"] + " (변형)"
json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
PY
    python3 -m unittest discover -s "$T/ftneg/evals/scenario-report" > "$T/utneg.log" 2>&1; echo "neg_rc=$? $(grep -c 'test_example_report_is_current' "$T/utneg.log")" ;;
  SK-09) s6=$(sec '## 6. Decision Propagation Manifest' '## 7.' "$E/design-kit/references/visual-change-protocol.md")
    echo "$(printf '%s\n' "$s6" | grep -F '`status`' | n '`approved`') $(printf '%s\n' "$s6" | n '`excluded_surfaces: []`')" ;;
  SK-10) echo "changed=$(git -C "$W" diff --name-only "$BASE" "$TIP" -- design-kit/skills/design-test/SKILL.md design-kit/skills/design-audit/SKILL.md design-kit/agents/design-reviewer.md | grep -c . || true) cite=$(for f in skills/design-test/SKILL.md skills/design-audit/SKILL.md agents/design-reviewer.md; do n 'visual-change-protocol.md' <"$E/design-kit/$f"; done | tr '\n' ' ')" ;;
  SK-11) s=$(sec '### 단계 13' '### 단계 14' "$E/react-kit/skills/react-init/SKILL.md")
    a=$(printf '%s\n' "$s" | grep -nF '/harness init' | head -1 | cut -d: -f1); b=$(printf '%s\n' "$s" | grep -nF 'harness-project.yaml.template' | head -1 | cut -d: -f1)
    echo "tpl=$(printf '%s\n' "$s" | n 'harness-project.yaml.template') dst=$(printf '%s\n' "$s" | n '.harness/project.yaml') init_line=${a:-0} tpl_line=${b:-0} vm_port=$(grep -cE '^[[:space:]]+vm_port: 5173$' "$E/react-kit/templates/harness-project.yaml.template")" ;;
  SK-12) q=$(sec '## Quickstart' '## ' "$E/react-kit/README.md")
    echo "harness_init=$(printf '%s\n' "$q" | grep -cE '^/harness init' || true) react_init=$(printf '%s\n' "$q" | n '/react-init')" ;;
  SC-01) gate; D='  - decision_id: DEC-20260813-001\n    source: .design/approvals/DEC-20260813-001.md\n'
    R='    required_surfaces:\n      - surface_id: a\n        golden: g.png\n        assertions: ["main visible"]\n'
    printf "decisions:\n${D}    status: approved\n${R}    excluded_surfaces: []\n" > "$T/d-ok.yaml"
    printf "decisions:\n${D}    status: draft\n${R}    excluded_surfaces: []\n" > "$T/d-draft.yaml"
    printf "decisions:\n${D}${R}    excluded_surfaces: []\n" > "$T/d-nostatus.yaml"
    printf "decisions:\n${D}    status: approved\n${R}" > "$T/d-noexc.yaml"
    printf "decisions:\n${D}    status: approved\n    required_surfaces: []\n    excluded_surfaces: []\n" > "$T/d-bothempty.yaml"
    out=""; for c in ok draft nostatus noexc bothempty; do out="$out $c=$(runc "$T/d-$c.yaml")"; done; echo "${out# }" ;;
  SC-02) g=$E/design-kit/evals/decision-gate-test.sh; git -C "$W" show "$BASE:design-kit/references/visual-change-protocol.md" > "$T/base-doc.md"
    o=$(bash "$g" 2>&1); rc=$?; ob=$(DECISION_GATE_DOC="$T/base-doc.md" bash "$g" 2>&1)
    echo "rc=$rc [$(printf '%s\n' "$o" | tail -1)] base_doc: tb=$(printf '%s\n' "$ob" | n 'Traceback=1') to2=$(printf '%s\n' "$ob" | n 'rc=0 (답 2)') to1=$(printf '%s\n' "$ob" | n 'rc=0 (답 1)') [$(printf '%s\n' "$ob" | tail -1)]" ;;
  SC-03) infra_script; wf_all; out=""; for c in comment step quoted block flow broken; do out="$out $(r1 "$c")"; done
    k=$(r1 ka); o=$(cat "$T/out-ka.txt")
    echo "${out# } | $k refs=$(printf '%s\n' "$o" | n '열거된 uses 참조 수: 3') perref=$(printf '%s\n' "$o" | grep -cE '^VIOLATION .*-> ' || true) total=$(printf '%s\n' "$o" | n 'VIOLATION=1')" ;;
  SC-04) infra_script; wf_all; nb=$T/nopy; ny=$T/nopyyaml; mkdir -p "$nb" "$ny"
    for d in "$nb" "$ny"; do ln -sf "$(command -v bash)" "$d/bash"; ln -sf /usr/bin/grep "$d/grep"; done; ln -sf /usr/bin/python3 "$ny/python3"
    pre="nopy_python3=$(PATH="$nb" bash -c 'command -v python3 >/dev/null && echo 보임 || echo 없음') nopyyaml_python3=$(PATH="$ny" bash -c 'python3 -c "print(1)" 2>/dev/null || echo 안돎') nopyyaml_yaml=$(PATH="$ny" bash -c 'python3 -c "import yaml" >/dev/null 2>&1 && echo 보임 || echo 없음')"
    a="$(r1 step "$nb") $(r1 comment "$nb") py=$(grep -F 'checkout' "$T/out-comment.txt" | grep -cF 'python3' || true)"
    b="$(r1 step "$ny") $(r1 comment "$ny") py=$(grep -F 'checkout' "$T/out-comment.txt" | grep -cE 'python3|PyYAML' || true)"
    echo "$pre | nopy: $a | nopyyaml: $b" ;;
  ER-01) gate; mkdir -p "$T/d-dir"
    printf 'decisions:\n  - decision_id: DEC-20260813-001\n    source: s\n    status: approved\n    note: \377\376\n' > "$T/d-nonutf8.yaml"
    echo "dir=$(runc "$T/d-dir") nonutf8=$(runc "$T/d-nonutf8.yaml")" ;;
  AR-01) ch=$(git -C "$W" diff --name-only "$BASE" "$TIP")
    extra=$(printf '%s\n' "$ch" | grep . | grep -vxF -f <(printf '%s\n' "$ALLOWED") | grep -c . || true)
    kits=""; for k in flutter-toolkit design-kit infra-kit react-kit; do kits="$kits $k=$(printf '%s\n' "$ch" | grep -c "^$k/" || true)"; done
    multi=0; for c in $(git -C "$W" rev-list "$BASE..$TIP"); do t=$(git -C "$W" show --name-only --format= "$c" | awk -F/ 'NF{print $1}' | sort -u | grep -c .); [ "$t" -gt 1 ] && multi=$((multi + 1)); done
    echo "base=${BASE:0:7} tip=${TIP:0:7} changed=$(printf '%s\n' "$ch" | grep -c . || true) extra=$extra$kits multi_top=$multi"
    [ "$extra" = 0 ] || printf '%s\n' "$ch" | grep . | grep -vxF -f <(printf '%s\n' "$ALLOWED") ;;
  AR-02) b=$(git -C "$W" show "$TIP:$NOTES" 2>/dev/null); c=$([ -n "$b" ] && echo 1 || echo 0); out="committed=$c"
    for k in flutter-preflight docs/infra/platform/cicd.md 2.16 build_runner_core approved excluded_surfaces harness-project.yaml.template '관례 표 없는 호출' tone-guide docs/design-kit/visual-change-protocol.html docs/flutter-toolkit/project-detection.html docs/flutter-toolkit/flutter-ai-rules.html docs/infra-kit/infra-test.html; do out="$out $(printf '%s\n' "$b" | n "$k")"; done
    echo "$out" ;;
  DG-02) mdl_ready || { echo "MDL_NOT_READY"; return; }; tot=0; rows=""
    for f in $(git -C "$W" diff --name-only "$BASE" "$TIP" -- '*.md' ':(exclude).harness/sprint-*.md'); do
      o=$T/old.md; git -C "$W" show "$BASE:$f" > "$o" 2>/dev/null || : > "$o"
      c=$(newmd "$o" "$E/$f"); tot=$((tot + c)); rows="$rows $f=$c"; done
    s=design-kit/evals/decision-gate-test.sh; git -C "$W" show "$BASE:$s" > "$T/old.sh"; sc=$(newsc "$T/old.sh" "$E/$s")
    json=0; for f in $(git -C "$W" diff --name-only "$BASE" "$TIP" -- '*.json'); do python3 -m json.tool "$E/$f" >/dev/null 2>&1 || json=$((json + 1)); done
    echo "md_new=$tot sh_new=$sc json_bad=$json |$rows" ;;
  *) echo "모르는 조건 $1"; return 2 ;;
  esac
}
# === 측정 도우미 끝 ===
```

봉인 전 실측(2026-09-26, 시작점 `f81568d` 을 풀어 둔 판, `E_REF` 없이 — 끝점이 아직 시작점과 같다):

| 조건 | 값 |
| --- | --- |
| SK-01 · SK-02 · SK-03 | `1 0 1 0` · `0 1 1` · `0 0 0 2 2 2` |
| SK-04 · SK-05 · SK-06 · SK-07 | `1 0 0 0 1 1 1` · `0 0 0 0` · `lines=0 rule=0` · `1 0 1 0` |
| SK-08 · SK-08N | `names=26 ut_rc=0 ut_last=OK` · `neg_rc=1 2` |
| SK-09 · SK-10 · SK-11 · SK-12 | `0 0` · `changed=0 cite=6 5 4` · `tpl=0 dst=1 init_line=4 tpl_line=0 vm_port=1` · `harness_init=1 react_init=1` |
| SC-01 | `ok=0/0 draft=0/0 nostatus=0/0 noexc=0/0 bothempty=1/0` |
| SC-02 | `rc=0 [결과: 10 경우 중 불일치 0] base_doc: tb=0 to2=0 to1=0 [결과: 10 경우 중 불일치 0]` |
| SC-03 | `comment=0/1/1 step=1/0/1 quoted=1/0/0 block=1/0/0 flow=0/1/1 broken=1/0/2 \| ka=1/0/1 refs=1 perref=2 total=1` |
| SC-04 | `nopy_python3=없음 nopyyaml_python3=1 nopyyaml_yaml=없음 \| nopy: step=1/0/2 comment=0/1/2 py=0 \| nopyyaml: step=1/0/2 comment=0/1/2 py=0` |
| ER-01 · AR-01 · AR-02 · DG-02 | `dir=1/1 nonutf8=1/1` · `changed=0 extra=0` 킷 넷 0 `multi_top=0` · `committed=0` 과 0 열셋 · `md_new=0 sh_new=0 json_bad=0` |
| 양성 대조(임시 복제본) | AR-01 `extra=1 multi_top=1` · AR-02 `committed=1` 과 1 열셋 · DG-02 `md_new=3 sh_new=1 json_bad=1` · SK-06 알려진 답 · AP-03 · AP-04 종료 코드 2 |
| DG-05 (시작 판 ci-local) | `rc=0` 22 · `feedback-agg-test SKIP (yq 없음)` 한 줄 |

## 리서치 소스

- 저장소 안: 핸드오프 `.harness/handoff/2026-09-26-0110.md` §C3(본 체크아웃) · `.harness/.meta/kaizen-0924/f1-kit-followups-notes.md` · `f2-review-fixes-notes.md` · `final-notes.md` 「다음 사이클 메모」 · `.harness/sprint-contract-kaizen-0924-f1-kit-followups.md` 입력 표 10 · 11 · 24 · 31 · 71 · 73 행
- 이 맥 설치본(읽기만, 웹 조회 없음): `~/.pub-cache/hosted/pub.dev/build_runner-2.13.1/CHANGELOG.md` · `build_runner_core-7.3.2` · `8.0.0` 의 `lib/src/generate/build_definition.dart` · `build_runner-2.3.3` · `2.4.13` · `2.4.15` 의 `pubspec.yaml` · `slang-4.14.0/README.md` · `slang_build_runner-4.14.0/README.md` · `~/.claude/plugins/cache/joo6077-plugins/infra-kit/0.4.0/`
- 교차 진단 원문(이전 세션 스크래치, 읽기만): `xdiag-all.md` P5 결함 4 · P8 결함 3 — 결정은 저장소 안 근거로만 했다
