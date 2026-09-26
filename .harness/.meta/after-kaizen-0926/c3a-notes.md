# c3a 킷 후속 A — 구현 기록 (2026-09-26)

계약: `.harness/sprint-contract-after-0924-kits-a.md` (봉인 `sha256:03017626965ce499`, 봉인 커밋 `fe56268`).
가지 `chore/ak-c3-kits`, 시작점 `f81568d`. QA 판정은 이 기록에 적지 않는다 — 다음 단계의 qa-evaluator 몫이다.

## 한 일

| 커밋 | 킷 | 내용 | 조건 |
| --- | --- | --- | --- |
| `fe56268` | `.harness` | 계약 봉인 (교차 진단 지적 넷을 반영한 뒤) | — |
| `1428484` | flutter-toolkit | widget-inspector §7 「관례 표 없는 호출」 가르기 · flutter-feature 호출 문구 · flutter-build Gotcha · scenario-report 1 단계 · flutter-l10n slang 두 갈래 · project-detection Step 2b 타겟별 확인 · flutter-run · flutter-ai-rules · 예시 기록 옛 도구 이름 | SK-01~08 |
| `76debef` | design-kit | 결정 전파 문서 §6 규칙 두 줄(`status` 는 `approved` 하나 · `excluded_surfaces` 키 필수) · 검사 코드(상태 값 · 키 · 폴더와 UTF-8 아닌 입력을 종료 코드 2) · 시험 16 경우 | SK-09 · SK-10 · SC-01 · SC-02 · ER-01 |
| `19d93cd` | infra-kit | infra-test 규칙 1 을 YAML 구조로 읽기, python3 · PyYAML 이 없으면 줄 검사로 돌고 한 줄 알림 | SC-03 · SC-04 |
| `9a7c914` | react-kit | react-init 13 단계가 `harness-project.yaml.template` 을 `.harness/project.yaml` 로 덮어 쓰기 · README 빠른 시작의 중복 `/harness init` 제거 | SK-11 · SK-12 |

## 이 계약에서 정한 것과 근거

- **build_runner 플래그는 명령에서 빼지 않는다.** 2.7.0 부터는 무시되지만(pub 설치본 `build_runner-2.13.1/CHANGELOG.md:150`),
  2.7.0 미만이 쓰는 `build_runner_core` 7.3.2 · 8.0.0 의 `build_definition.dart:564-570` 은 플래그 없이 대화 없는 실행이면 빌드를 멈춘다.
  이 맥의 로컬 프로젝트 셋이 2.3.3 · 2.4.x 를 쓴다. 새 문장은 이미 있던 2.16 항목 한 줄 안에 이어 적었다(교차 진단 지적 2).
- **결정 전파의 상태 값은 `approved` 하나.** 근거는 같은 절의 「승인 기록 없는 결정은 manifest 에 올리지 않는다」 다.
- **`excluded_surfaces` 키는 늘 적는다.** 제외할 것이 없으면 `[]`. 키가 없으면 위반(종료 코드 1). 근거는 「침묵은 커버리지 공백」 문장이다.
- **react-kit 틀은 지우지 않고 쓴다.** 설계 문서 `docs/react/kit-design/final-integration.md:486` 이 복사를 정해 두었고,
  react-init 의 포트 고정이 틀에만 있는 `vm_port: 5173` 에 기댄다(harness 기본 틀은 `vm_port: null`).
- **「관례 표 없는 호출」 을 밝힌 호출은 건너뜀, 말 없이 표만 빠지면 `[미검증]`.** flutter-feature 는 관례 표를 만들지 않는 스킬이라 호출에 그 말을 밝힌다.
  평가 사례 16 의 단언은 뒤의 경우라 그대로 맞는다.
- 교차 진단이 SK-03 · SK-11(과제 목록을 뒤집는 결정)을 사용자에게 다시 물으라고 권했다. 위임 문구가 「묻지 마라」 라 묻지 않았다.
  사용자가 뒤집으면 개정 파일로 처리한다 — 부모 단계에서 한 줄로 알려 주기를 권한다.

## 넘긴 것과 사유

| 항목 | 사유 |
| --- | --- |
| `flutter-preflight` 기준 커밋 비교 | 저장소 안에 flutter 쪽에 넣을 근거가 없다(`phase5-notes.md:77` · `phase10-notes.md:66`). 가르는 규칙이 이미 세 곳이고 `insights-report.md:66` 이 「하나로 정한다」 를 먼저 요구한다 |
| `docs/infra/platform/cicd.md` 판정 세 줄 구조 | 원칙 문서 열두 개가 모두 같은 구조이고 설치본 infra-kit 0.4.0 에 `docs/` 가 없다. 세 줄만 옮기면 넷째 사본이 되고, 통째로 옮기면 `scripts/` · `.claude/` 까지 바뀌어 범위 밖이다 |
| build_runner 2.16 이후 동작 | 이 맥에 2.16 설치본이 없다(2.3.3 · 2.4.13 · 2.4.15 · 2.7.1 · 2.12.2 · 2.13.1 만 있다). 웹 조회는 이번 지시로 막혀 있다 |
| `approved` 밖의 상태 값(예: 대체됨) | 저장소 안에 근거가 없다 |

## 버전 판단 (릴리스 단계 몫)

규칙은 `.harness/.meta/kaizen-0924/release-plan.md:6` 「기능 추가 = minor, 고침만 = patch」 를 따른다. 넷 다 patch 로 본다 — 같은 성격이던 f1 킷 후속도 모두 patch 였다(`f1-kit-followups-notes.md:117`).

| 킷 | 판단 | 이유 |
| --- | --- | --- |
| flutter-toolkit | patch | 문서 규칙과 동작 사이 어긋남을 고쳤다. 새 스킬 · 새 절차 없음 |
| design-kit | patch | 문서가 이미 「선택이 아니다」 라고 적은 규칙을 검사 코드가 따르게 했다. 다만 `excluded_surfaces` 키가 없던 manifest 가 이제 종료 코드 1 이 되므로, 받는 입력이 좁아진 쪽으로 보면 minor 로 올릴 여지가 있다 |
| infra-kit | patch | 규칙 1 의 잘못된 판정 셋(run 본문 · 흐름 표기 · 읽을 수 없는 YAML)을 고쳤다 |
| react-kit | patch | 설계 문서가 정한 절차를 스킬에 옮겼다 |

## 문서 페이지 (다시 만들 것 — 이 계약 범위 밖, 부모가 모아서)

`python3 scripts/detect-docs-drift.py --since f81568d` 출력은 두 줄이었다.

- `docs/flutter-toolkit/flutter-ai-rules.html` ← `flutter-toolkit/references/flutter-ai-rules.md`
- `docs/flutter-toolkit/project-detection.html` ← `flutter-toolkit/references/project-detection.md`

검출기가 잡지 않았지만 같은 내용을 담은 페이지가 둘 더 있다(바뀐 낱말로 찾아 확인).

- `docs/design-kit/visual-change-protocol.html` ← `design-kit/references/visual-change-protocol.md` (`excluded_surfaces` 10 곳)
- `docs/infra-kit/infra-test.html` ← `infra-kit/skills/infra-test/SKILL.md` (`checkout` 10 곳)

react-kit 의 `docs/react-kit/scaffolding.html` · `integration.html` 도 `harness init` 을 담지만 원본이 `docs/react/` 설계 문서라 이번에 바뀌지 않았다.

## tone-guide 5 단계 대조

1 단계는 `tone-kit:tone-guide` 를 불러 오버레이 `.claude/tone-project.md`(어댑터 없음 · 주석 한국어)와 코어 넷 · `locale-korean.md` 를 읽었다.
대상은 이번 커밋 넷에서 더해진 줄 111 줄(`.json` · `.html` 제외)이다. 어댑터가 없어 스택 전용 검사는 돌지 않는다.

| 규칙 | 건수 | 판정 |
| --- | --- | --- |
| C-01 what 대신 why | 0 | 통과 — 새 주석 여섯은 실패 모드 · 이유를 적는다 (보존 범주 H) |
| C-04 · F 구분선 (`#` 로 바꿔 잰 G1) | 0 | 통과 |
| C-07 해설 3 줄 초과 | 0 | 통과 — 가장 긴 주석이 2 줄 |
| C-09 섹션 라벨 항목 수 | 0 | 통과 — 시험 입력 라벨 둘이 각각 4 · 2 개를 묶는다 |
| C-10 디자인 툴 참조 · C-13 자화자찬 | 0 · 0 | 통과 |
| C-16 값 메타 인라인 주석 | 1 | 허용 — `co_rc=3   # 3 = python3 · PyYAML 이 없어 구조로 못 읽음` |
| N-07 · E `effective` · `resolved` | 0 | 통과 |
| N-08 한 글자 이름 | 0 | 통과 — `st` · `fh` · `doc` 는 같은 스크립트 규칙 2 와 같은 이름 (S-12) |
| S-04 전달만 하는 래퍼 · S-06 헬퍼 체인 | 0 · 0 | 통과 |
| S-12 같은 역할 같은 패턴 | 0 | 통과 — `co_out` · `co_rc` 는 규칙 2 의 `pin_out` · `pin_rc` 와 같은 꼴 |
| K-02 번역투 여섯 가지 (G-1) | 0 | 통과 |
| K-04 · G-2 `합니다` 체 | 0 | 통과 |
| K-05 음역 | 0 | 통과 — `파싱` 은 정착 외래어, 규칙 2 의 `YAML 파싱 실패` 와 같은 말 |
| K-11 새 이름 | 0 | 통과 — `흐름 표기 스텝` 은 처음 나올 때 괄호에 예(`- {uses: ...}`)를 붙였다. 자리표시자 `<위젯 누르기 도구>` · `<로그인 도구>` 는 `record-format.md:62` 의 `<누르기 도구>` 꼴을 따랐다 |

## 측정 결과 (끝점 기준, 계약의 측정 도우미)

- SK-01 `0 1 1 1` · SK-02 `1 1 1` · SK-03 `1 1 1 2 2 2` · SK-04 `0 1 1 0 1 0 0` · SK-05 `3 1 1 0`
- SK-06 `lines=1 rule=1 app-codegen=1 app-analyze=1 app-fix=1 app-test=1 app-preflight=0 comment_target=0` · SK-07 `0 1 0 1`
- SK-08 `names=0 ut_rc=0 ut_last=OK` · SK-08N `neg_rc=1 2`
- SK-09 `1 1` · SK-10 `changed=0 cite=6 5 4` · SK-11 `tpl=1 dst=2 init_line=4 tpl_line=5 vm_port=1` · SK-12 `harness_init=0 react_init=1`
- SC-01 `ok=0/0 draft=2/0 nostatus=2/0 noexc=1/0 bothempty=1/0`
- SC-02 `rc=0 [결과: 16 경우 중 불일치 0] base_doc: tb=2 to2=2 to1=1`
- SC-03 `comment=0/1/1 step=1/0/1 quoted=1/0/0 block=0/1/1 flow=1/0/1 broken=0/0/2 | ka=1/0/1 refs=1 perref=2 total=1`
- SC-04 `nopy: step=1/0/2 comment=0/1/2 py=1 | nopyyaml: step=1/0/2 comment=0/1/2 py=1` (macOS 기본 bash 3.2 로도 flow · block · step 이 같은 판정)
- ER-01 `dir=2/0 nonutf8=2/0`
- AP-03 · AP-04 종료 코드 0 · RE-01 추가 파일 0 · DG-01 0 · DG-02 `md_new=0 sh_new=0 json_bad=0` (notes 커밋 전 측정)

## 교차 진단 뒤 고친 것 (2026-09-26 12:55)

교차 진단이 판정을 바꿀 결함 하나와 작은 문제 셋을 찾았다. 넷 다 고쳤고, 같은 모양인 flutter-run `:22` 도 함께 고쳤다.

| 커밋 | 킷 | 내용 |
| --- | --- | --- |
| `4dedb85` | flutter-toolkit | flutter-preflight Gotcha(`:18`)가 Step 2b 4 번의 타겟별 확인을 따른다 — `app-preflight` 묶음 타겟만 있으면 모든 단계가 기본 명령(판정을 바꿀 결함) · flutter-run Gotcha(`:22`)의 `make app-run` 도 타겟이 있을 때만 · widget-inspector 칸 값 문장(`:134`)과 리포트 틀(`:198`)이 표 없는 두 경우를 담는다 |
| `7799a5a` | infra-kit | infra-test 「빼면 안 되는 것」 표의 `CORE_TOOLS` 줄을 지금 동작에 맞췄다 · checkout rule 오류 문구 「YAML 파싱 실패」 를 「YAML 읽기 실패」 로 |

- flutter-preflight 는 AR-01 기대 집합 밖이다. 개정 파일 `.harness/sprint-amendments-after-0924-kits-a.md` 에 그 한 경로를 더하는 개정(AM-01, 조건을 느슨하게 하는 쪽)과 새로 고친 곳을 재는 측정(AM-02, 조건을 좁히는 쪽)을 적었다.
- infra-test 표 줄: 교차 진단은 사전 검사를 뺀 사본의 종료 코드 1 이 규칙 2 때문이라고 했다. 다시 돌려 보니 grep 과 python3 가 모두 없으면 규칙 2 가 `[미검증]` 이라 종료 코드가 2 다.
  줄 검사 갈래는 python3 나 PyYAML 이 없을 때만 돌고 그때 규칙 2 도 늘 `[미검증]` 이라, 옛 줄의 「exit 1 로 끝난다」 는 어느 조합에서도 나오지 않는다. 표 줄에 2 를 적었다 (재현 값은 AM-02).
- `CORE_TOOLS="grep"` 은 그대로 둔다. python3 · PyYAML 이 있으면 grep 없이도 돌지만, 사전 검사를 도구 조합으로 가르면 스크립트 동작이 바뀐다. 오보를 내는 갈래를 남기느니 멈추는 쪽을 골랐다고 표 줄에 적었다.

추가로 넘긴 것:

| 항목 | 사유 |
| --- | --- |
| widget-inspector 「관례 표 없는 호출」 평가 사례 | `flutter-toolkit/evals/evals.json` 이 AR-01 기대 집합 밖이고, 사례를 더하면 `CLAUDE.md` 의 평가 사례 수 문장까지 바뀐다 — 다음 사이클 몫 |
| build_runner 2.16 이후 동작 | 교차 진단이 올라온 변경 기록 2.15.0 항목(지운 옵션을 넘겨도 경고만 내고 무시한다)을 들어 닫았다. 이 맥 pub 설치본은 2.13.1 까지라 직접 확인하지 못했다. 결론(플래그를 빼지 않는다)은 그대로다 |

다시 만들 문서 페이지는 늘지 않았다 — flutter-preflight · widget-inspector 는 문서 사이트 페이지가 없고, `docs/infra-kit/infra-test.html` 은 이미 위 목록에 있다.

tone-guide 5 단계 대조 (이번에 더한 여섯 줄, 1 단계는 이번 수정 전에 다시 불러 코어 넷 · `locale-korean.md` · 오버레이를 읽었다):

| 규칙 | 건수 | 판정 |
| --- | --- | --- |
| K-02 번역투 여섯 가지 (G-1) · G-2 `합니다` 체 | 0 · 0 | 통과 |
| K-05 · 사용자 쉬운 말 목록 | 1 → 0 | 고침 — 앞 대조는 「파싱」 을 정착 외래어로 통과시켰으나 사용자 쉬운 말 목록(`~/.claude/rules/plain-korean.md`)이 이 낱말을 막는다. 새로 더한 checkout rule 문구만 「읽기」 로 바꿨고, 규칙 2 의 옛 문구는 이번 범위가 아니라 두었다 |
| K-11 새 이름 | 0 | 통과 — 「묶음 타겟」 은 project-detection Step 2b 가 이미 쓰는 말 |
| C-07 해설 3 줄 초과 · C-15 문체 | 0 · 0 | 통과 — 표 칸 · Gotcha 한 줄씩 |
| S-12 같은 역할 같은 패턴 | 0 | 통과 — flutter-preflight · flutter-run 두 Gotcha 가 flutter-ai-rules `:115` 와 같은 꼴로 Step 2b 4 번을 가리킨다 |

## 그 밖에 적어 둘 것

- 편집기가 바뀐 파일에서 띄우는 경고는 모두 이번에 손대지 않은 줄의 옛 경고다(`widget-inspector.md` MD060 · MD032, `project-detection.md` MD060 · MD032,
  `flutter-ai-rules.md:19` MD032, `visual-change-protocol.md:211` · `:503` MD024, `react-kit/README.md:17` · `:43` MD060). 범위를 벗어나 고치지 않았다.
- 라이브러리 문서 확인은 웹 조회가 막혀 있어 pub 설치본(`slang-4.14.0` · `slang_build_runner-4.14.0` · `build_runner-2.13.1` · `build_runner_core` 7.3.2 · 8.0.0)만 읽었다.
- 측정 도우미: 계약 끝의 측정 도우미 블록(떼어 둔 사본 `/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/bda55d45-296c-491f-89ba-b52042d58e72/scratchpad/kitsa-measure.sh`).
  로컬 CI 는 `/Users/jackson/Hub/10_Dev/claude-plugins/.harness/handoff/2026-09-26-tools/ci-local.sh`.

## QA 결과

qa-evaluator 2 회차 APPROVE — 조건 28 개, 개정 AM-01 · AM-02 둘 다 통과 근거로 썼다. 리포트는 `.harness/sprint-feedback-after-0924-kits-a.md`(커밋 `b0b1608`, 계약 status `done` 도 같은 커밋).
리포트가 부모에게 넘긴 교차 진단 두 가지(AR-01 을 개정 파일로 통과시킨 판단 · DG-05 를 1 회차 결과 대신 다시 잰 판단)는 부모 단계 몫이다.

## 다음 사이클 메모

교차 진단이 「판정은 안 바꾼다」 고 본 것 가운데 이번에 고치지 않은 셋과, QA 리포트 「남겨둘 것」 둘이다.

- flutter-toolkit: widget-inspector 의 새 칸 값 `건너뜀 — 관례 표 없는 호출` 을 재는 평가 사례가 `evals/evals.json` 에 없다. 사례 16 은 `[미검증] 관례 표 없음` 쪽만 잰다.
  사례를 더하면 루트 `CLAUDE.md` 의 평가 사례 수 문장도 같이 고친다(지금도 「23개」 · 「20개」 두 문장이 서로 다르다)
- infra-kit: infra-test `CORE_TOOLS="grep"`(`SKILL.md:220`) 때문에 python3 · PyYAML 이 있어 grep 없이도 돌 수 있는 환경도 종료 코드 2 로 멈춘다.
  안전한 쪽으로 틀린 것이라 두었다(표 줄 `:389` 에 까닭을 적음). 사전 검사를 도구 조합으로 가를지 정한다
- infra-kit: 핀닝 rule 의 옛 오류 문구(`SKILL.md:327`)가 사용자 쉬운 말 목록이 막는 낱말을 쓴다. checkout rule 과 같은 「YAML 읽기 실패」 로 맞출지 —
  바꾸면 `docs/infra-kit/infra-test.html` 도 같이 다시 만든다
- 계약: AR-01 은 개정 AM-01(허용 경로에 `flutter-toolkit/skills/flutter-preflight/SKILL.md`)을 적용해야 통과한다. 다음 계약은 Makefile 규칙을 따르는 스킬 넷
  (flutter-preflight · flutter-run · flutter-ai-rules · project-detection)을 처음부터 허용 경로와 SK-07 같은 셈에 넣는다
- 계약: DG-05 의 전제 「미커밋 변경 0건」 은 1 회차 QA 가 계약 status 줄을 바꿔 두므로 2 회차부터 늘 깨진다. 다음 계약은 계약 파일 자신의 status 줄 변경을 빼고 잰다
