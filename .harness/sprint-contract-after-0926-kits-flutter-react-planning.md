---
feature: "킷 남은 것 — flutter-toolkit · react-kit · planning-kit (카이젠 뒤 이어질 것 2026-09-26 두 번째 묶음 k1)"
slug: after-0926-kits-flutter-react-planning
created: "2026-09-26 20:51"
complexity: "복잡"
conditions: 29
status: done
owner_session: bda55d45-296c-491f-89ba-b52042d58e72
conditions_digest: sha256:534198c0775e068c
measurement_digest: sha256:e957eecfbfa776f5
locked_at: "2026-09-26 21:02"
---

## 배경

2026-09-24 카이젠 뒤에 남은 일 가운데 세 킷(flutter-toolkit · react-kit · planning-kit)과 `docs/react/` 몫을 한 계약으로 묶는다.
입력은 통합 폴더(읽기만)의 `.harness/.meta/after-kaizen-0926b/leftovers.md` 「## kit-flutter-toolkit」 KF-1~KF-4 · 「## kit-react-kit」 KRe-1 · 「## kit-planning-kit」 KP-1 과
같은 폴더 `decisions.md` 의 UD-1 · UD-3 · UD-6 이다. 통합 폴더는 `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0926b` 다.

- 사용자 합의(Step 5): 위임으로 받은 것으로 적는다 — 세션 `bda55d45-296c-491f-89ba-b52042d58e72`, 위임 2026-09-26T10:09:00.557Z 「123다실행해 그러면끝나?다음카이젠에왜넘기는데?」,
  결정 답 2026-09-26T10:30:16.222Z(AskUserQuestion 「일곱 다 · 설계도 현행화」 와 같은 시각의 「그대로 유지」 · 작은 결정 넷 선택). 그 앞의 위임 2026-09-24T04:04:16.964Z 「나한테 물어보지 말고 자동으로 끝까지」.
  봉인된 조건을 느슨하게 하는 개정(허용 파일 늘리기 · 측정 대상 줄이기 · 문턱 낮추기)은 이 위임으로 동의 처리하지 않는다 — 개정 파일에 동의 칸을 비워 두고 부모에게 넘긴다.
- 작업 폴더 W = `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak2-k1`, 가지 `chore/ak2-k1`, 시작점 `6378948`(origin/main, #119).
- 커밋 규칙: `git add <경로>` 뒤 `git commit -o <경로>` · 한 커밋에 맨 위 자리 하나(flutter-toolkit · react-kit · planning-kit · `docs/react` · 루트 `CLAUDE.md` · `.harness` 가운데 하나 — 세 킷은 각각 따로 센다) · `git add -A` · `git stash` · push · 가지 바꾸기 금지.
- 구현 전에 `tone-kit:tone-guide` 1 단계(규칙 불러오기)를, 완료 선언 전에 5 단계(전수 대조)를 한다 — 대조 결과는 notes 에 남긴다(AR-02).
- 다른 묶음(1 차: harness 스크립트 · 계약 형식 · PRD 없음 규칙 · 문서 사이트)이 같은 파일을 고칠 수 있다. 바꿀 줄은 최소로 하고 이 계약 항목에 없는 절은 건드리지 않는다. 기존 마크다운 경고 정리(VS-26)는 부모 몫이라 더해진 줄의 새 경고만 잰다(DG-02).
- 사용자가 할 일: 없음.

복잡도 4 축 — 넷 다 「예」 이고 공개 약속 변경과 소비자가 함께 있어 「복잡」 이다. Step 2.5 짝 조건: SK-03 ↔ SK-04(평가 사례 ↔ 루트 문서 수), SK-09 ↔ SK-10(두 preflight), SK-11(스킬 ↔ 에이전트), SK-12(참조 문서 ↔ 스크립트 출력), SK-15 · SK-16(스킬 ↔ 설계 문서), AR-02(설계 문서 ↔ 문서 사이트 페이지).

| 축 | 물음 | 값 |
| -- | ---- | -- |
| 레이어 수 | 몇 개 계층을 관통하는가 | 셋 — 스킬 · 에이전트 · 참조 문서, 평가 사례 JSON 과 루트 안내 문서, 설계 문서 · 조사 기록 |
| 공개 API·계약 변경 | 외부에 노출된 약속이 바뀌는가 | 예 — flutter-audit 의 미검증 판정 규칙(두 카운터), 두 preflight 의 실패 보고 절차, react-kit 감지 절차가 스크립트를 부름 |
| 소비면 존재 | 반대편이 있는가 | 예 — 루트 `CLAUDE.md` 의 평가 사례 수, animation-architect-react, `project-detect.sh`, `docs/react-kit/*.html` 페이지 |
| 회귀 위험 | 기존 동작이 깨질 수 있는가 | 예 — `run-evals.py` 평가 사례 검사, `project-detect-test.sh`, validate-plugin 검사, 로컬 CI 25 단계 |

설정 값 대조 (`.harness/project.yaml` 을 글자 그대로 옮김):

| config key | project.yaml 에서 읽은 값 | 계약에 쓴 값 |
| ---------- | ------------------------- | ------------ |
| `commands.analyze` | `bash -n scripts/release.sh` | DG-01 N/A — 재는 파일이 바뀐 파일에 없다 |
| `commands.test` | `bash scripts/release.sh 2>&1 \|\| true` | DG-03 N/A — 같은 이유 |
| `diagnostics.ide_exclude` | `[]` | DG-02 의 `([] 제외)` |
| `contract_categories[].id` / `prefix` | Skill/SK · Script/SC · Error/ER · Architecture/AR | 같은 넷 (Script 는 `SC-00: N/A`) |
| `anti_patterns[].id` / `message` | AP-01 버전 하드코딩 · AP-02 force push · AP-03 bare code fence · AP-04 frontmatter name 누락 | AP-03 · AP-04 (바뀌는 파일이 SKILL.md · 에이전트 · 코드 블록 있는 MD 라 걸릴 수 있다). AP-01 은 `plugin.json` 버전을 안 건드려서, AP-02 는 이 계약이 push 하지 않아서 뺐다 |

## 리서치 소스

바깥 사실은 Codex 가 원문을 인용해 둔 대조 결과 셋만 쓴다(통합 폴더 `.harness/.meta/after-kaizen-0926b/ex/`, 읽기만). 여기 없는 바깥 사실은 새로 찾지 않고 「바깥 근거 없음」 으로 notes 에 적는다.

- EX-5 (`.../ex/EX-5.md`) — build_runner. 원문 <https://raw.githubusercontent.com/dart-lang/build/master/build_runner/CHANGELOG.md> 2.7.0 항목 「Ignore `-d` flag: always delete files as if `-d` was passed.」,
  <https://raw.githubusercontent.com/dart-lang/build/master/build_runner/lib/src/build_runner_command_line.dart> 「Removed options, kept to not break old command lines.」, 2.16.0 「New default output behavior: always fix incorrect generated files.」.
  판정: 무시 전환은 2.16 이 아니라 2.7.0, 지금은 옛 명령줄을 깨지 않으려고 숨은 옵션으로 받는다
- EX-9 (`.../ex/EX-9.md`) — <https://react.dev/blog/2026/09/09/react-19-3> 「We shared it as an experimental API last year, and in 19.3 it's stable and ready to use.」 `<ViewTransition>` 은 `react` 에서 가져와 감싸고,
  Transition 으로 표시된 업데이트(`startTransition` · Suspense reveal · `useDeferredValue`)에서 돈다. DOM 에서만. `<Activity>` 의 안정 · 실험 상태는 원문에 없다
- EX-10 (`.../ex/EX-10.md`) — <https://github.com/mermaid-js/mermaid/releases/tag/mermaid%4012.0.0> (2026-09-10 · ELK · `redux-color` · `neo` 기본값, 문법 변경 아님),
  <https://docs.github.com/en/rest/about-the-rest-api/api-versions> 「The API version `2026-03-10` was released on Tue, 10 Mar 2026.」 · 「`2022-11-28` | March 10, 2028」

## GAP 분석 (Pre-Edit Audit)

대상 파일을 읽기만 하고 줄을 적었다. 줄 번호는 시작점 `6378948` 기준이다.

| 대상 파일 | 실제 Read 증거 (`파일:라인`) | 발견한 기존 갭·위반 | 계약 조건화 여부 |
| --------- | ---------------------------- | ------------------- | ---------------- |
| `flutter-toolkit/skills/flutter-audit/SKILL.md` | `:30-51` 「아래 5 조항은 정본을 문구 변형 없이 복제」 · `:41` 「임계값은 2 다」 · `:25` L3 Honesty · `:407-411` Unverifiable 틀 · `:425` 「미검증 누계 임계(2 건)」 | 원문이 v5.1 로 바뀌었는데(`qa-evaluation-guide.md:1260-1311` 번호 목록 · `:892-900` 4 요건) 옛 다섯 조항이 남았다. c4b 가 reviewer 일곱만 옮기고 넘겼다(`c4b-notes.md:99`) | SK-01 · SK-02 |
| `react-kit/agents/react-reviewer.md` | `:169` 사본 출처 v5.1 · `:171-226` 번호 목록 · `:228-237` 4 요건 | KRe-1 의 「react-reviewer §10」 은 c4b `446428a` 가 처리했다 | 처리됨 |
| `flutter-toolkit/evals/evals.json` | 사례 16(`id: 16`) 마지막 단언 · 사례 18 마지막 단언 「생성 후 $DART test로 검증한다」 · 사례 23 개 | 「건너뜀 — 관례 표 없는 호출」 을 재는 사례가 없다. 사례 18 이 flutter-test Step 4(`flutter-test/SKILL.md:152` `$FLUTTER test`)와 어긋난다 | SK-03 · SK-07 |
| `flutter-toolkit/agents/widget-inspector.md` · `skills/flutter-feature/SKILL.md` | `widget-inspector.md:147` · `:212` · `:260` · `flutter-feature/SKILL.md:199` | 새 칸 값 규칙은 이미 있다 — 사례만 없다 | SK-03 (근거) |
| `CLAUDE.md` (루트) | `:52` 「23개 테스트 케이스」 · `:373` 「20개 스킬별 assertion」 | 두 문장이 서로 다르다 | SK-04 |
| `flutter-toolkit/skills/flutter-kaizen/SKILL.md` | `:28-50` `## Gotchas` · `:37-44` 짝 스킬 표 | Makefile 규칙 스킬 넷을 계약 허용 경로에 처음부터 넣으라는 교훈이 없다(`c3a-notes.md:155-156`) | SK-05 |
| `flutter-toolkit/skills/flutter-api/SKILL.md` · `flutter-feature/SKILL.md` · `flutter-screen/SKILL.md` | `flutter-api:333-336` · `flutter-feature:147-151` · `flutter-screen:269-272` | 사용자에게 보이는 codegen 안내가 flutter-run 의 전후 삭제 수 블록을 가리키지 않는다(`phase5-notes.md:81`) | SK-06 |
| `flutter-toolkit/skills/flutter-build/SKILL.md` | `:16` Gotcha 「build_runner 2.16 부터 … 이 플래그는 제거된 호환 옵션 목록으로 옮겨졌다」 | EX-5 — 무시 전환은 2.7.0, 2.16 에 옮겨졌다는 말은 원문에 없다. 플래그 유지 결정(UD-1)은 그대로 | SK-08 |
| `flutter-toolkit/skills/flutter-run/SKILL.md` · `flutter-build` · `flutter-preflight` | 세 파일 각 2 줄 `build_runner build --delete-conflicting-outputs` (flutter-preflight `:79` · `:84`) | UD-1 로 바꾸지 않는다 | SK-08 (그대로인지) |
| `flutter-toolkit/skills/flutter-preflight/SKILL.md` | `:46-66` fix · `:93` 「실패 시 즉시 중단」 · `:147-152` Rules | 빨간 단계의 원인을 가르는 절차가 없다 | SK-09 · ER-01 |
| `react-kit/skills/react-preflight/SKILL.md` | `:31-66` 7 단계 · `:68-77` 복구 안내 · `:137-145` Rules | 같은 빈자리 | SK-10 · ER-01 |
| `harness/skills/sprint/SKILL.md` | `:92-126` Step 3 — 원인 가르기 조각 `:105-114` · 판정 표 `:116-120` | UD-3 사본의 원문 | SK-09 · SK-10 (원문) |
| `react-kit/skills/react-animation/SKILL.md` · `agents/animation-architect-react.md` | `react-animation:35` Gotcha 10 · `:231-256` `withViewTransition` · `animation-architect-react:54` | React 19.3 `<ViewTransition>` 안정화(EX-9)가 스킬 · 에이전트 어디에도 없다 | SK-11 |
| `react-kit/skills/react-screen/SKILL.md` | `:24` Gotcha 11 `<Activity />` 「canary 채널에서 안정화 중」 | EX-9 에 상태 근거가 없다 | 바깥 근거 없음 (범위 경계) |
| `react-kit/references/project-detection.md` · `scripts/project-detect.sh` · `evals/scripts/project-detect-test.sh` | 참조 `:1-54`(스크립트 언급 0) · 스크립트 `:1-87` · 시험 `:9` | 부르는 곳이 시험뿐이다. 참조 문서의 JSON 예시 키와 스크립트 출력 키는 같다(봉인 전 실측 11 개) | SK-12 |
| `planning-kit/skills/plan-sync-github/SKILL.md` · `docs/planning/research-log.md` | `plan-sync-github:18` Gotcha 4 · `:171` `apiVersion=2022-11-28` · `research-log.md:31-32` | 지원 기한(2028-03-10)은 설치되지 않는 `docs/` 에만 있다 | SK-13 |
| `docs/planning/flows.md` · `data-modeling.md` | `flows.md:61` 「최신 안정판은 12.0.0」 · `data-modeling.md:90` ELK · 「문법은 그대로」 | EX-10 판정 「맞음」 — Mermaid 12 는 처리됨. `flows.md:61` 의 「최신 안정판」 수식어만 원문 직접 인용이 아니다 | 처리됨 (범위 경계) |
| `docs/react/research-log.md` | `:39` 19.3 표 줄 · `:437` `react-view-transitions` 「backlog (canary 대기)」 · `:496` 같은 이름 다른 표 | canary 대기가 풀렸는데 backlog 줄이 그대로 | SK-14 |
| `docs/react/kit-design/*.md` 여덟 | 모두 `last_updated: 2026-04-10`. `g6-build-audit.md:52` dev 줄 「포트 5173」(strictPort 없음) · `:144-206` §3 여덟 단계(스킬은 일곱) · `:416` `verdict: APPROVE \| REJECT` · `g1-scaffolding.md:192-193` 「/harness init 호출 → .harness/project.yaml 자동 생성」 · `final-integration.md:243` · `:487` | 2026-04-11 뒤 스킬 바뀜 커밋(문서별 2~9 개, 합 47 개)이 반영 안 됐다. `render-evidence-protocol` · `strictPort` · `BLOCKED` · `passed` 는 여덟 문서 모두 0 | SK-15 · SK-16 |

## Skill

- [ ] SK-01: flutter-audit 의 미검증 규칙 사본이 원문 v5.1 과 같다 — `## Unverified-Evidence Protocol` 절의 옛 다섯 조항을 지우고, `harness/docs/guides/qa-evaluation-guide.md` §Canonical Unverified-Evidence Protocol 번호 목록과 §증거 분류 triage 의 `UNVERIFIED_ENV` 남용 방지 4 요건 두 덩어리를 글자 그대로 넣는다(reviewer 일곱과 같은 모양 — 출처 줄 하나에 원문 경로 · `v5.1` · 「사본」, 앞뒤 MD029 끄기 · 켜기 주석). Given 가지 끝, When `m SK-01`, Then `clauses=1 req=1` · prov≥1 · `old=0` · `md029=1/1` 이다 [exact, enumerated]
    측정: `m SK-01` — 같음 판정은 `scripts/check-reviewer-protocol-copies.py` 의 `canonical_blocks` · `normalized` · `contains_block` 을 그대로 불러 쓴다. 시작 판 `clauses=0 req=0 prov=0 old=1 md029=0/0`
    알려진 답: `react-reviewer.md:169-237` 을 flutter-audit 끝에 붙인 임시 복제본에서 `clauses=1 req=1 prov=1 old=1 md029=1/1` (봉인 전 실측)
- [ ] SK-02: flutter-audit 자기 규칙 · 보고 틀이 v5.1 두 카운터를 쓴다 — 사본 밖에서 `env_gaps` · `invalid_evidence` 가 각 1 줄 이상, 리포트 틀 `Unverifiable` 블록(구분선 앞까지)에 둘 다 있고, `## Rules` 의 옛 줄 「미검증 누계 임계(2 건)」 이 0 이며 그 절의 임계 줄은 `invalid_evidence` 를 같은 줄에 적는다. `## Gotchas` 의 `L3 Honesty` 줄은 `4 요건` 을 가리킨다. Given 가지 끝, When `m SK-02`, Then 여섯 값이 모두 기대대로다 [exact, enumerated]
    측정: `m SK-02` 가 `env_gaps=a invalid=b rep_env=c rep_inv=d rule_old=0 rule_inv=e l3_4req=f` 이고 a · b · c · d · e · f ≥1. 시작 판 `env_gaps=0 invalid=0 rep_env=0 rep_inv=0 rule_old=1 rule_inv=0 l3_4req=0` — `rule_old=1` 이 양성 대조
- [ ] SK-03: 평가 사례에 「관례 표 없는 호출」 사례가 하나 더해진다 — Given 가지 끝의 `flutter-toolkit/evals/evals.json`, When `m SK-03`, Then `agent` 가 `widget-inspector` 이고 프롬프트에 「관례 표 없는 호출」 이 있으며 단언 하나가 `건너뜀 — 관례 표 없는 호출` 을 담는 사례가 1 개 이상(`skip_case≥1`)이고, 사례 번호가 1 부터 빈틈없이 이어지며(`ids_ok=1`), 사례 16 은 시작 판과 JSON 값이 같다(`case16_same=1`). 그리고 `python3 scripts/run-evals.py flutter-toolkit` 이 종료 코드 0 과 `<사례 수> passed, 0 failed` 를 낸다 [exact, enumerated]
    측정: `m SK-03` (시작 판 `cases=23 ids_ok=1 skip_case=0 case16_same=1`) · `(cd E && python3 scripts/run-evals.py flutter-toolkit)` 의 마지막 줄 (시작 판 `Total: 23 passed, 0 failed` · 종료 코드 0)
- [ ] SK-04: 루트 `CLAUDE.md` 의 flutter-toolkit 평가 사례 수 두 문장(Commands 절 `evals.json (flutter-toolkit/evals/evals.json)` 줄 · Key Conventions 절 `flutter-toolkit evals는` 줄)이 `evals.json` 사례 수와 같은 수를 적는다. Given 가지 끝, When `m SK-04`, Then `cases=N commands=N개 conventions=N개` 로 세 값이 같다 [exact, enumerated]
    측정: `m SK-04` (시작 판 `cases=23 commands=23개 conventions=20개` — conventions 가 양성 대조)
- [ ] SK-05: flutter-kaizen `## Gotchas` 에 교훈 한 줄 — Makefile 규칙(`references/project-detection.md` Step 2b)을 따르는 스킬 넷(flutter-preflight · flutter-run · flutter-ai-rules · project-detection)은 그 규칙을 바꾸는 계약의 허용 경로에 처음부터 함께 넣는다. 네 이름 · `Step 2b` · `허용 경로` 를 모두 담은 줄이 그 절에 1 줄 이상이다 [exact, enumerated]
    측정: `m SK-05` 가 1 이상 (시작 판 0)
- [ ] SK-06: 사용자에게 보이는 codegen 안내 셋이 flutter-run 의 전후 삭제 수 블록을 가리킨다 — flutter-api `## After Creation` 절, flutter-feature `### 4. codegen 안내` 절, flutter-screen `## After Creation` 절에 각각 `flutter-run` 과 `삭제` 를 함께 담은 줄이 1 줄 이상이다. 안내 명령 줄 `$DART run build_runner build --delete-conflicting-outputs` 는 UD-1 로 그대로 둔다 [exact, enumerated]
    측정: `m SK-06` 이 `api=a feature=b screen=c` 이고 a · b · c ≥1 (시작 판 `api=0 feature=0 screen=0`)
- [ ] SK-07: 평가 사례 18(`skill: flutter-test`)의 실행 단언이 flutter-test Step 4 와 같다 — 단언에 `$FLUTTER test` 가 1 개 이상, 옛 단언 「생성 후 $DART test로 검증한다」 는 0 이다 [exact, enumerated]
    측정: `m SK-07` 이 `flutter_test=a dart_verify=0 skill=flutter-test` 이고 a≥1 (시작 판 `flutter_test=0 dart_verify=1` — `dart_verify=1` 이 양성 대조)
- [ ] SK-08: flutter-build Gotcha 의 build_runner 문장이 EX-5 원문과 맞고 플래그는 명령에 그대로다(UD-1) — `## Gotchas` 절에서 옛 구절 「이 플래그는 제거된 호환 옵션 목록으로 옮겨졌다」 가 0 이고, 한 줄 안에 `2.16` · `2.7.0` · `빼지 않는다` · `build_runner_command_line.dart`(EX-5 가 인용한 지금 CLI 원문 주소)가 함께 있다. flutter-run · flutter-build · flutter-preflight 의 `build_runner build --delete-conflicting-outputs` 줄 수는 시작 판과 같다(각 2) [exact, enumerated]
    측정: `m SK-08` 이 `old216=0 joined=a flags=[2/2 2/2 2/2]` 이고 a≥1 (시작 판 `old216=1 joined=0 flags=[2/2 2/2 2/2]` — `old216=1` 이 양성 대조)
- [ ] SK-09: flutter-preflight 에 `## 실패 원인 가르기` 절이 있다(UD-3) — Given 가지 끝, When `m SK-09`, Then 그 절에 (a) `harness/skills/sprint/SKILL.md` · `Step 3` · `사본` 을 함께 담은 출처 줄이 1 이상 (b) 시작 판 sprint Step 3 판정 표의 다섯 줄(머리 · 구분 · 판정 셋)이 글자 그대로 모두 있고 (c) `merge-base` · `worktree add` 가 각 1 이상 (d) 임시 워크트리 준비 명령 `pub get` 이 1 이상이다 [exact, enumerated]
    측정: `m SK-09` 가 `sec=s prov=p rows=5/5 merge_base=a wt=b prep=c` 이고 s · p · a · b · c ≥1 (시작 판 `sec=0 prov=0 rows=0/5 merge_base=0 wt=0 prep=0`)
    알려진 답: sprint 원문 조각과 표를 붙인 임시 복제본에서 `sec=18 prov=1 rows=5/5 merge_base=1 wt=1 prep=1` (봉인 전 실측)
- [ ] SK-10: react-preflight 에 같은 `## 실패 원인 가르기` 절이 있다(UD-3) — SK-09 의 (a)(b)(c)와 같고, (d) 준비 명령은 `pnpm install` 이 1 이상이다 [exact, enumerated]
    측정: `m SK-10` 이 `sec=s prov=p rows=5/5 merge_base=a wt=b prep=c` 이고 s · p · a · b · c ≥1 (시작 판 `sec=0 prov=0 rows=0/5 merge_base=0 wt=0 prep=0`)
- [ ] SK-11: react-animation 과 animation-architect-react 가 React 19.3 `<ViewTransition>` 을 안다(EX-9) — react-animation `## Gotchas` 절에 `<ViewTransition>` · `19.3` · `startTransition` · `react.dev/blog/2026/09/09/react-19-3` 을 함께 담은 줄이 1 이상이고, Tier 2 의 `withViewTransition` 래퍼는 지우지 않으며(등장 수가 시작 판 이상), animation-architect-react 에 `<ViewTransition>` 줄이 1 이상이다. 결정: Tier 2 를 통째로 옮기지 않고, Transition 으로 표시된 업데이트에는 `<ViewTransition>` 을 쓰고 그 밖의 DOM 갱신은 래퍼를 쓴다고 가른다 [exact, enumerated]
    측정: `m SK-11` 이 `gotcha=a wrapper=6/w agent=b` 이고 a≥1 · w≥6 · b≥1 (시작 판 `gotcha=0 wrapper=6/6 agent=0`)
- [ ] SK-12: react-kit 감지 절차가 `project-detect.sh` 를 부른다 — `react-kit/references/project-detection.md` 에 `project-detect.sh` 와 `bash` 를 함께 담은 줄이 1 이상이고, 그 문서의 JSON 예시 키 집합이 빈 폴더에서 스크립트를 돌린 출력 키 집합과 같으며(11 개), 스크립트 자체는 바뀌지 않는다 [exact, enumerated]
    측정: `m SK-12` 가 `call=a keys_same=1 nkeys=11 script_changed=0` 이고 a≥1 (시작 판 `call=0 keys_same=1 nkeys=11 script_changed=0`)
- [ ] SK-13: plan-sync-github `## Gotchas` 에 GitHub 문서 버전 날짜 사실이 있다(EX-10) — `2022-11-28` · `2028-03-10` · `2026-03-10` · `docs.github.com/en/rest/about-the-rest-api/api-versions` 를 함께 담은 줄이 1 이상이다. 문서 링크의 `apiVersion=2022-11-28` 은 바꾸지 않는다 [exact, enumerated]
    측정: `m SK-13` 이 1 이상 (시작 판 0) · `grep -c 'apiVersion=2022-11-28' E/planning-kit/skills/plan-sync-github/SKILL.md` 가 시작 판과 같은 2
- [ ] SK-14: `docs/react/research-log.md` 의 `react-view-transitions` backlog 줄이 19.3 안정화를 적는다 — 그 이름으로 시작하는 표 줄 가운데 「canary 대기」 를 담은 줄이 0 이고 `19.3` 을 담은 줄이 1 이상이다 [exact, enumerated]
    측정: `m SK-14` 가 `row=2 canary_wait=0 v193=a` 이고 a≥1 (시작 판 `row=2 canary_wait=1 v193=0` — `canary_wait=1` 이 양성 대조)
- [ ] SK-15: `docs/react/kit-design/` 설계 문서 여덟이 지금 스킬로 현행화됐다(UD-6) — Given 가지 끝, When `m SK-15`, Then 여덟 문서(`g1-scaffolding.md` · `g2-state-data.md` · `g3-performance.md` · `g4-quality.md` · `g5-ui-patterns.md` · `g5b-animation.md` · `g6-build-audit.md` · `final-integration.md`) 각각 머리 블록의 `last_updated` 가 `2026-09-26` 이상이고, 새 절 `## 현행화 기록` 이 시작 판에서 그 문서가 맡은 경로(머리 블록 `skills` · `agents`, `final-integration.md` 는 `react-kit/references` · `templates` · `scripts`)를 2026-04-11 뒤에 바꾼 커밋 해시 앞 7 자를 모두 담는다(문서별 2~9 개, 합 47 개). 각 커밋 줄에는 그 문서에서 고친 절이나 「설계 영향 없음」 과 이유를 적는다 [exact, enumerated]
    측정: `m SK-15` 의 여덟 줄이 모두 `lu=1 … miss=0` (시작 판: 여덟 줄 모두 `lu=0` 이고 miss 가 commits 와 같다 — g1 9 · g2 7 · g3 2 · g4 6 · g5 3 · g5b 5 · g6 9 · final 6)
    알려진 답: g3 에 `last_updated: 2026-09-26` 과 두 해시 표를 넣은 임시 복제본에서 `g3-performance.md lu=1 commits=2 miss=0` (봉인 전 실측)
- [ ] SK-16: 설계 문서가 지금 스킬 사실을 담는다(UD-6) — g6: dev 서브커맨드 표 줄에 `strictPort`, §3 `/react-preflight` 에 8 번째 단계(`8. audit`) 없음(스킬은 7 단계), §3 에 `passed` · `skipped` · `merge-base`(원인 가르기) 각 1 이상, `verdict:` 줄에 `BLOCKED`. 나머지: g1 13 번 단계 블록에 `harness-project.yaml.template`, g1 에 `strictPort`, g5b 에 `<ViewTransition>`, final-integration 에 `project-detect.sh` 와 `project-detection.md` 를 함께 담은 줄, `render-evidence-protocol` 이 g1 · g4 · g5 · g5b · g6 · final-integration 여섯 문서에 각 1 이상 [exact, enumerated]
    측정: `m SK-16` 첫 줄 `dev_strict≥1 step8=0 passed≥1 skipped≥1 split≥1 verdict≥1`, 둘째 줄 `g1_tpl≥1 g1_strict≥1 vt≥1 fi_link≥1 rep=` 뒤 여섯 값 모두 ≥1 (시작 판 `dev_strict=0 step8=1 passed=0 skipped=0 split=0 verdict=0` · `g1_tpl=0 g1_strict=0 vt=0 fi_link=0 rep=0,0,0,0,0,0,` — `step8=1` 이 양성 대조)

## Script

- [ ] SC-00: N/A (이 계약은 `scripts/release.sh` · `marketplace.json` · `plugin.json` 버전을 건드리지 않는다 — 릴리스는 부모 몫. 측정: `git -C W diff --name-only BASE TIP | grep -cE '^(scripts/release\.sh|\.claude-plugin/marketplace\.json|[^/]+/\.claude-plugin/plugin\.json)$'` 가 0)

## Error

- [ ] ER-01: 두 preflight 의 원인 가르기 조각이 실제로 셋을 가른다 — Given `## 실패 원인 가르기` 절의 첫 bash 블록을 떼어 `<기준 가지>` → `main`, `<실패한 검사 명령>` → `test -f marker` 로 바꾸고, 커밋 A(빈 커밋 · `origin/main`) 위에 `marker` 를 더한 커밋 B 가 HEAD 인 임시 저장소, When `FLUTTER=true` · 가짜 `pnpm`(종료 0)을 `PATH` 앞에 둔 채 돌리면, Then 세 줄의 종료 값이 차례로 `0 1 1` 이다(HEAD 통과 · 분기점 실패 · origin/main 실패). 기대값은 sprint 원문 조각의 알려진 답이다 [exact, enumerated]
    측정: `m ER-01` 이 `flutter=[0 1 1] react=[0 1 1]` (시작 판 `flutter=[no_block] react=[no_block]`)
    알려진 답: sprint Step 3 원문 조각을 `## 실패 원인 가르기` 절 하나짜리 파일로 감싸 돌리면 `0 1 1` (봉인 전 실측)
    음성 대조: 조각에서 `"$FORK_BASE"` 를 빼면 `0 1` 두 값만 나와 FAIL 한다 (봉인 전 실측)

## Architecture

- [ ] AR-01: 바뀐 파일이 기대 집합 안이고 한 커밋에 맨 위 자리 하나다 — Given 구현 · notes · QA 리포트 커밋이 모두 가지 `chore/ak2-k1` 에 들어간 뒤, 시작점 `BASE=$(git -C W merge-base origin/main chore/ak2-k1)` 부터 끝점 `TIP=$(git -C W rev-parse --verify chore/ak2-k1)` 까지(`HEAD` 를 쓰지 않는다. 해석이 안 되면 `UNRESOLVED` 로 멈춘다) `git diff --name-only` 로 모은 경로가 측정 도우미 `ALLOWED` 의 스물일곱 경로 안에만 있고(부분 집합, 생성물 제외 없음), flutter-toolkit · react-kit · planning-kit · `docs/react` · 루트 `CLAUDE.md` 가 각 1 경로 이상이며, 커밋마다 맨 위 자리가 하나뿐이다 — 자리는 flutter-toolkit · react-kit · planning-kit · `docs/react` · 루트 파일 · `.harness` 여섯이고, 세 킷은 각각 별도 자리라 한 커밋에 두 킷을 같이 넣으면 위반이다 [exact, collective]
    측정: `m AR-01` 이 `extra=0 multi_top=0` 이고 `flutter` · `react` · `planning` · `docs_react` · `root` ≥1 (시작 판 `changed=0`)
    양성 대조: 임시 복제본에서 flutter-audit · `react-kit/README.md` · g6 설계 문서를 한 커밋에 넣으면 `extra=1 multi_top=1` 과 `EXTRA react-kit/README.md` (봉인 전 실측)
- [ ] AR-02: 결정 · 처리됨 · 바깥 근거 없음 · 다시 만들 문서 페이지를 notes 에 남긴다 — Given 끝점 `TIP` 과 작업 폴더 HEAD 가 같고, notes `.harness/.meta/after-kaizen-0926b/k1-notes.md` 가 커밋돼 있다. Then 스물세 토큰(`KF-1` · `KF-2` · `KF-3` · `KF-4` · `KRe-1` · `KP-1` · `UD-1` · `UD-3` · `UD-6` · `go_router` · `auto_route` · `<Activity>` · `ADR` · `바깥 근거 없음` · `처리됨` · `tone-guide` · `EX-5` · `EX-9` · `EX-10` · `react-reviewer` · `REVIEWERS` · `research-log.md:19` · `sprint/SKILL.md`)이 각 1 줄 이상이고(뒤 셋은 「범위 경계」 의 넘김 약속 셋 — KF-2 · KF-4 · UD-3 행), `scripts/detect-docs-drift.py --since BASE` 가 낸 `docs/**.html` 페이지가 모두 notes 에 적혀 있다(문서 사이트 재생성은 이 계약 범위 밖 — 목록만 넘긴다). 바깥 근거 인용은 EX 파일 경로와 원문 URL 을 함께 적는다 [exact, enumerated]
    측정: `m AR-02` 첫 줄 `committed=1` 과 1 이상 스물셋, 둘째 줄 `rc=0 pages=p miss=0` (시작 판 `committed=0` 과 0 스물셋 · `pages=0`)
    양성 대조: 임시 복제본에서 g6 설계 문서만 바꿔 커밋하면 둘째 줄 `pages=1 miss=1` 과 `MISS docs/react-kit/g6-build-audit.html` (봉인 전 실측)

## Anti-patterns

- [ ] AP-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수 (```text, ```bash, ```yaml 등). 판정 권위는 validate-plugin V6 상태기계다 — 여는/닫는 fence 가 동형이라 줄 단위 정규식으로는 판정 불가
    측정: 끝점을 풀어 둔 판 `E` 에서 `python3 "$E/scripts/validate-plugin.py" --check=code-fence` 종료 코드 0 (시작 판 0)
    양성 대조: 임시 복제본의 react-preflight SKILL.md 끝에 언어 없는 fence 를 붙이면 종료 코드 2 (봉인 전 실측)
- [ ] AP-04: SKILL.md / agents/*.md frontmatter 에서 name 필드 누락 — validate-plugin V1 FAIL
    측정: `python3 "$E/scripts/validate-plugin.py" --check=frontmatter` 종료 코드 0 (시작 판 0)
    양성 대조: 임시 복제본의 plan-sync-github SKILL.md 에서 `name:` 줄을 지우면 `누락 필드 ['name']` · 종료 코드 2 (봉인 전 실측)

## Reusability

- [ ] RE-01: N/A (산출물이 문서 문장 · 평가 사례 JSON · 설계 문서뿐이라 새 컴포넌트 · 함수 모듈이 없다. 측정: `git -C W diff --diff-filter=A --name-only BASE TIP -- . ':(exclude).harness'` 가 0 줄)
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다 — 미검증 규칙은 원문 v5.1 을 글자 그대로 옮기고(SK-01), 원인 가르기는 sprint Step 3 표 · 조각을 사본으로 옮기며(SK-09 · SK-10), react-kit 감지는 있던 `project-detect.sh` 를 부른다(SK-12). 새 검사 스크립트 · 새 시험 파일을 만들지 않는다
    측정: RE-01 의 명령이 0 줄 · `m SK-12` 의 `script_changed=0`

## Diagnostics

- [ ] DG-01: N/A (commands.analyze `bash -n scripts/release.sh` 가 재는 `scripts/release.sh` 는 이번 바뀐 파일에 없다. 측정: `git -C W diff --name-only BASE TIP | grep -cx 'scripts/release.sh'` 가 0)
- [ ] DG-02: IDE diagnostics 워닝/인포 0개 ([] 제외) — IDE(편집기) 진단을 명령줄로 같게 잰다: 바뀐 `.md`(`.harness/sprint-*` 제외)의 더해진 줄에 걸린 markdownlint-cli2 0.23.2(MD013 끔, 편집기 확장과 같은 설정) 경고 0 · 바뀐 `.json` 읽기 실패 0
    측정: `m DG-02` 가 `md_new=0 json_bad=0` (도구가 없으면 도우미 `mdl_ready` 가 임시 폴더에 설치한다)
    양성 대조: 임시 복제본의 flutter-audit 끝에 `#bad heading` 줄을 넣어 커밋하면 `md_new=1` (봉인 전 실측)
- [ ] DG-03: N/A (commands.test `bash scripts/release.sh 2>&1 || true` 가 재는 `scripts/release.sh` 는 이번 바뀐 파일에 없다. 측정: DG-01 과 같은 명령이 0)
- [ ] DG-04: N/A (구동할 앱 · 서버가 없다 — 바뀐 파일이 스킬 문서 · 참조 문서 · 평가 사례 JSON · 설계 문서뿐. 대신 DG-05 가 `ci-local.sh` 가 담은 단계를 돌린다)
- [ ] DG-05: 지금 `ci-local.sh` 가 담은 CI(자동 검사) 단계 26 개(통과 25 · yq 없음 건너뜀 1)를 로컬에서 돌려 통과한다 — Given 작업 폴더 W 가 끝점과 같다(`git -C W rev-parse HEAD` 가 `TIP` 이고 `git -C W status --porcelain --untracked-files=no` 가 빈 출력), When `TMPDIR=<임시 폴더> bash /Users/jackson/Hub/10_Dev/claude-plugins/.harness/handoff/2026-09-26-tools/ci-local.sh /Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak2-k1` 를 돌리면, Then 요약(`$TMPDIR/ci-local/summary.txt`)에 `rc=0` 줄이 25 개이고 `rc=0` 이 아닌 줄은 `feedback-agg-test SKIP (yq 없음)` 하나뿐이다
    측정: `grep -c 'rc=0' "$TMPDIR/ci-local/summary.txt"` 가 25 · `grep -v 'rc=0' "$TMPDIR/ci-local/summary.txt"` 가 그 한 줄 (시작 판 봉인 전 실측: 25 · SKIP 한 줄)
    음성 대조: 이 묶음이 기대는 `run-evals` · `react-detect-test` · `reviewer-copies` · `validate-plugin` 단계는 평가 사례 JSON · `project-detect.sh` · 킷 문서 frontmatter 를 깨면 실패한다 — SK-03 · SK-12 · AP-04 의 대조가 같은 명령을 쓴다

## 범위 경계

항목별 처리 — 입력은 `leftovers.md` 의 여섯 행과 `decisions.md` 의 셋이다.

| ID | 항목 | 처리 | 조건 · 사유 |
| --- | --- | --- | --- |
| KF-1 | widget-inspector 「건너뜀」 평가 사례 · 루트 `CLAUDE.md` 사례 수 두 문장 | 계약에 넣음 | SK-03 · SK-04 |
| KF-2 | flutter-audit 옛 다섯 조항 → v5.1 | 계약에 넣음 | SK-01 · SK-02. 새 검사 스크립트 목록(`check-reviewer-protocol-copies.py` `REVIEWERS`)에 flutter-audit 를 넣는 일은 `scripts/` 라 이 묶음 밖 — notes 에 넘김으로 적는다 |
| KF-3 | Makefile 규칙 스킬 넷 교훈 | 계약에 넣음 | SK-05. 이 계약은 Makefile 규칙을 바꾸지 않아 네 파일을 허용 경로에 넣지 않았다(flutter-preflight 는 UD-3 로 들어 있다) |
| KF-4 | go_router 18 · auto_route 11.1 | 바깥 근거 없음 | EX 대조 결과에 없다. 지금 문장이 틀린 것도 아니다(`phase5-notes.md:78`) |
| KF-4 | flutter-audit `:50` | 계약에 넣음 | SK-01 이 조항 5 를 원문 v5.1 글자 그대로로 바꾼다 — 평가 측 보고 모양 `[조건/항목 ID, 사유, 시도한 fallback 단계]` 는 원문이 그대로 둔 것이라 따로 고치지 않는다 |
| KF-4 | codegen 안내 셋 | 계약에 넣음 | SK-06 |
| KF-4 | 평가 사례 18 `$DART test` | 계약에 넣음 | SK-07 |
| KF-4 | `--delete-conflicting-outputs` | 계약에 넣음 — 결정은 「빼지 않는다」(UD-1) | SK-08. EX-5 로 경계를 2.7.0 으로 바로잡는다. `docs/flutter/research-log.md:20` 의 2026-09-24 조사 기록은 그날 기록이라 두고 notes 에 적는다 |
| KRe-1 | Activity canary | 바깥 근거 없음 | EX-9 가 상태를 판정할 수 없다고 했다. react-screen Gotcha 11 은 그대로 |
| KRe-1 | `<ViewTransition>` Tier 2 | 계약에 넣음 | SK-11 · SK-14 · SK-16(g5b) |
| KRe-1 | react-reviewer §10 | 처리됨 | c4b `446428a` 가 사본을 v5.1 로 옮겼다(`react-reviewer.md:169` · `:228`) |
| KRe-1 | `project-detect.sh` | 계약에 넣음 — 결정은 「참조 문서가 부른다」 | SK-12. 설계(`final-integration.md:243`)가 킷 구성으로 정했고 시험이 있다. react-kit 스킬은 감지 절차를 모두 이 참조 문서로 넘기므로(스킬 본문에 감지 코드가 따로 없다) 참조 문서가 부르게 하는 것이 스킬이 부르는 길이다. 스킬마다 스크립트 실행 줄을 따로 넣는 일은 이 계약이 재지 않는다 — 교차 진단이 짚은 좁힘이며 의도한 것이다 |
| KRe-1 · UD-6 | 설계 문서 `g6-build-audit.md` dev 포트 · preflight 절 · 나머지 설계 문서 | 계약에 넣음 | SK-15 · SK-16 |
| UD-3 | flutter-preflight · react-preflight 기준 커밋 비교 | 계약에 넣음 | SK-09 · SK-10 · ER-01. 원문은 시작 판 `harness/skills/sprint/SKILL.md` Step 3 이다 — 다른 묶음이 원문을 바꾸면 사본 동기화는 그 묶음 몫으로 notes 에 적는다 |
| UD-1 | build_runner 플래그 · react 틀 | 그대로 유지 | SK-08 이 플래그 줄 수를, AR-01 이 `react-kit/templates/` 가 바뀌지 않음을 잰다 |
| KP-1 | GitHub 문서 날짜 | 계약에 넣음 | SK-13. 링크 날짜 `2022-11-28` 은 그대로(옛 호출이 깨지는 변경이 있다는 판단은 `research-log.md:32` 그대로) |
| KP-1 | Mermaid 12 | 처리됨 | `bbdebaf` 가 `flows.md:61` · `data-modeling.md:90` 을 고쳤고 EX-10 이 「맞음」 으로 판정했다. 「최신 안정판」 수식어 한 곳은 원문 직접 인용이 아니라는 EX-10 의 열린 질문만 notes 에 적는다 |
| KP-1 | PRD 와 결정 기록(ADR) 비교 | 바깥 근거 없음 | EX-10 이 비교 자료를 다루지 않았다 |

`docs/react/research-log.md:39` 산문은 이미 「canary 대기가 풀렸다」 고 적어 표 줄과 어긋나 있다 — SK-14 가 바로 이 표 줄을 맞춘다(교차 진단 확인).

DG-05 의 범위: `leftovers.md` VS-24 는 `ci-local.sh` 에 `run-kaizen-assertions.py` 단계가 빠졌다고 적었지만, 지금 도구는 32 번째 줄 `run kaizen-assertions` 로 그 단계를 담고 있다(봉인 전 기준 측정 출력에 `kaizen-assertions rc=0`). DG-05 는 지금 도구가 담은 26 단계만 재며, `.github/workflows/ci.yml` 의 설치 줄(pip · npm · playwright 설치)은 로컬에 이미 있다고 보고 돌리지 않는다.

범위 밖(이 계약이 고치지 않는다): `docs/**.html` 페이지(다시 만들 페이지는 notes 에 적어 문서 사이트 묶음으로 넘긴다 — AR-02) · `scripts/` · `harness/` · `.claude/` · `docs/flutter/` · `docs/planning/` · 킷 `plugin.json` 버전(릴리스 단계 몫) · react-screen `<Activity />` Gotcha.

기능 조건 수는 20 개(SK 16 · ER 1 · AR 2 · DG-05)로 「복잡」 상한과 같다. 묶음 배정이 부모 오케스트레이션에서 정해져 계약을 나누지 않는다.

커버리지 해소 — Step 6.5 (4) 검출기가 낸 `UNCOVERED` 아홉 건(봉인 전 실측)과 AR-01 의 처리. 모두 측정 도우미 `m` 의 그 조건 갈래가 해당 토큰을 읽거나 센다:

- 커버리지 해소: AR-01 — 경로 기대 집합은 측정 도우미 `ALLOWED` 한 곳에만 적는다(목록을 두 번 적지 않는다). 검출기는 잡지 않았다
- 커버리지 해소: SK-01 — 원문 경로 · `v5.1` · MD029 주석은 `m SK-01` 의 파이썬 조각이 원문을 열고 `prov` · `md029` 로 센다
- 커버리지 해소: SK-04 — `evals.json` · `CLAUDE.md` 는 `m SK-04` 가 읽는 두 파일이다
- 커버리지 해소: SK-08 — `2.16` · `2.7.0` · `build_runner_command_line.dart` 는 `m SK-08` 의 `joined` 가 한 줄에 함께 있는지 센다
- 커버리지 해소: SK-11 — `19.3` · 원문 주소는 `m SK-11` 의 `gotcha` 가 센다
- 커버리지 해소: SK-12 — 참조 문서 경로와 `project-detect.sh` 는 `m SK-12` 가 읽고 돌린다
- 커버리지 해소: SK-14 — `docs/react/research-log.md` · `19.3` 은 `m SK-14` 가 읽고 센다
- 커버리지 해소: SK-15 — 문서 여덟 이름은 도우미 `DOCS` 에, 문서별 커밋 집합은 `doc_paths` 와 시작 판 `git log` 가 계산한다. 합 47 개는 봉인 전 실측이다
- 커버리지 해소: SK-16 — `project-detect.sh` · `project-detection.md` · 틀 이름 · `/react-preflight` 절 머리는 `m SK-16` 두 줄이 센다
- 커버리지 해소: AR-02 — notes 경로는 도우미 `NOTES`, `docs/**.html` 은 `detect-docs-drift.py` 출력에서 뽑는 페이지 집합이다. 넘김 토큰 `sprint/SKILL.md` · `REVIEWERS` · `research-log.md:19` 는 `m AR-02` 첫 줄 토큰 목록이 센다(교차 진단 반영)
- 오라클 해소: SK-02 · SK-05 · SK-06 · SK-08 · SK-11 · SK-13 · SK-14 · SK-16 — 산출물이 문서 문장이라 부를 코드가 없다. 옛 문구 0 과 새 문구 줄 수(양성 대조는 시작 판 값)로 잰다. 실행해서 재는 조건은 SK-01 · SK-03 · SK-12 · ER-01 · AR-01 · AR-02 · DG-05 다

## 회귀 게이트 — 측정 도우미

평가 때 이 블록을 떼어 bash 에서 불러 쓴다. `TMPDIR` 은 평가자 임시 폴더로 준다. 도우미는 끝점과 시작점을 `git archive` 로 풀어 재므로 작업 폴더의 미커밋 변경을 보지 않는다
(AR-02 둘째 줄만 작업 폴더에서 `detect-docs-drift.py` 를 돌리므로 작업 폴더 HEAD 가 `TIP` 이어야 한다). 작업 폴더 밖 입력은 지우지 마라 — 도우미가 만든 `$T` 아래만 치워도 된다.

```bash
# === 측정 도우미 시작 (after-0926-kits-flutter-react-planning) ===
# 쓰는 법: 이 블록을 파일로 떼어 bash 에서 source 한 뒤 `m <조건 ID>`. zsh 에서 부르지 마라.
# 잴 트리 E — 기본은 가지 끝(TIP)을 git archive 로 푼 임시 폴더. 시작 판을 재려면 E_REF=BASE.
W=${W:-/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak2-k1}
BR=${BR:-chore/ak2-k1}
BASE=$(git -C "$W" merge-base origin/main "$BR") || { echo "UNRESOLVED BASE"; return 2 2>/dev/null || exit 2; }
TIP=$(git -C "$W" rev-parse --verify "$BR") || { echo "UNRESOLVED TIP"; return 2 2>/dev/null || exit 2; }
T=$(mktemp -d "${TMPDIR:-/tmp}/k1m.XXXXXX")
snap() { mkdir -p "$2" && git -C "$W" archive "$1" | tar -x -C "$2"; }
B=$T/base; snap "$BASE" "$B"
case "${E_REF:-TIP}" in
  BASE) E=$B ;;
  *)    E=$T/tip; snap "$TIP" "$E" ;;
esac
FT=$E/flutter-toolkit; RK=$E/react-kit; KD=$E/docs/react/kit-design
# 머리줄 s 로 시작하는 줄부터, 그 뒤 처음 나오는 같은 급 이상 머리줄 앞까지 (s 는 글자 그대로 앞부분)
secx() { awk -v s="$1" '
  function lv(x){ match(x, /^#+ /); return (RSTART==1) ? RLENGTH-1 : 0 }
  !f && index($0,s)==1 { f=1; L=lv($0); print; next }
  f && lv($0)>0 && lv($0)<=L { exit }
  f' "$2"; }
# 표준 입력에서 글자 그대로 든 줄 수 (0 건에도 0)
n() { grep -cF -- "$1" || true; }
# 표준 입력에서 모든 인자를 함께 담은 줄 수
nall() { awk -v a="$*" 'BEGIN{k=split(a,w,"\t")} { ok=1; for(i=1;i<=k;i++) if(index($0,w[i])==0) ok=0; if(ok) c++ } END{print c+0}'; }
all() { local IFS=$'\t'; nall "$*"; }
cnt() { printf '%s' "$1" | awk 'NF{c++} END{print c+0}'; }
PY=${PY:-python3}
ALLOWED='flutter-toolkit/skills/flutter-audit/SKILL.md
flutter-toolkit/evals/evals.json
flutter-toolkit/skills/flutter-kaizen/SKILL.md
flutter-toolkit/skills/flutter-api/SKILL.md
flutter-toolkit/skills/flutter-feature/SKILL.md
flutter-toolkit/skills/flutter-screen/SKILL.md
flutter-toolkit/skills/flutter-build/SKILL.md
flutter-toolkit/skills/flutter-preflight/SKILL.md
CLAUDE.md
react-kit/skills/react-preflight/SKILL.md
react-kit/skills/react-animation/SKILL.md
react-kit/agents/animation-architect-react.md
react-kit/references/project-detection.md
docs/react/kit-design/final-integration.md
docs/react/kit-design/g1-scaffolding.md
docs/react/kit-design/g2-state-data.md
docs/react/kit-design/g3-performance.md
docs/react/kit-design/g4-quality.md
docs/react/kit-design/g5-ui-patterns.md
docs/react/kit-design/g5b-animation.md
docs/react/kit-design/g6-build-audit.md
docs/react/research-log.md
planning-kit/skills/plan-sync-github/SKILL.md
.harness/sprint-contract-after-0926-kits-flutter-react-planning.md
.harness/sprint-amendments-after-0926-kits-flutter-react-planning.md
.harness/sprint-feedback-after-0926-kits-flutter-react-planning.md
.harness/.meta/after-kaizen-0926b/k1-notes.md'
NOTES=.harness/.meta/after-kaizen-0926b/k1-notes.md
# 설계 문서 → 시작 판에서 그 문서가 맡은 경로를 2026-04-11 뒤에 바꾼 커밋 (판정 기준 집합, 시작 판으로 고정)
doc_paths() {
  case "$1" in
    final-integration.md) echo "react-kit/references react-kit/templates react-kit/scripts" ;;
    *) awk 'NR>2 && /^```$/{exit} /^(skills|agents):/{print}' "$B/docs/react/kit-design/$1" \
         | sed -E 's/^[a-z]+: *\[//; s/\].*$//' | tr ',' '\n' | sed -E 's/^ *//; s/ *$//' | awk 'NF' \
         | while read -r x; do case "$x" in /*) echo "react-kit/skills/${x#/}" ;; *) echo "react-kit/agents/$x.md" ;; esac; done | tr '\n' ' ' ;;
  esac
}
DOCS='g1-scaffolding.md g2-state-data.md g3-performance.md g4-quality.md g5-ui-patterns.md g5b-animation.md g6-build-audit.md final-integration.md'
# 시작 판 sprint Step 3 표 (머리 · 구분 · 행 셋) — UD-3 사본의 원문
sprint_rows() { secx '### Step 3:' "$B/harness/skills/sprint/SKILL.md" | grep -E '^\| (공용 작업 폴더|---|실패) '; }
# 원인 가르기 조각을 떼어 임시 저장소에서 돌린다 — 알려진 답: HEAD 0 · 분기점 1 · origin/main 1
split_run() {  # split_run <SKILL.md> — 출력: 세 줄의 exit 값을 공백으로
  local f=$1 r=$T/splitrepo-$RANDOM fake=$T/fakebin
  mkdir -p "$fake"; printf '#!/bin/sh\nexit 0\n' > "$fake/pnpm"; chmod +x "$fake/pnpm"
  secx '## 실패 원인 가르기' "$f" | awk '/^```bash/{b=1;next} b&&/^```/{exit} b' \
    | sed -e 's/<기준 가지>/main/g' -e 's/<실패한 검사 명령>/test -f marker/g' > "$T/split.sh"
  [ -s "$T/split.sh" ] || { echo "no_block"; return; }
  git init -q "$r" && git -C "$r" -c user.email=a@b -c user.name=m commit -q --allow-empty -m A \
    && git -C "$r" update-ref refs/remotes/origin/main HEAD \
    && : > "$r/marker" && git -C "$r" add marker && git -C "$r" -c user.email=a@b -c user.name=m commit -q -m B
  ( cd "$r" && PATH="$fake:$PATH" FLUTTER=true DART=true bash "$T/split.sh" 2>/dev/null ) \
    | sed -nE 's/.*exit=([0-9]+).*/\1/p' | tr '\n' ' ' | sed 's/ $//'
}
mdl_ready() {  # markdownlint-cli2 0.23.2 · MD013 끔 — 편집기 확장과 같은 설정
  MDL=${MDL:-$T/mdl}
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

m() {
  case "$1" in
  SK-01)  # flutter-audit 미검증 사본이 원문 v5.1 두 덩어리를 글자 그대로 든다
    "$PY" - "$E" <<'PY'
import importlib.util, sys
E = sys.argv[1]
sys.path.insert(0, E + "/scripts")
spec = importlib.util.spec_from_file_location("c", E + "/scripts/check-reviewer-protocol-copies.py")
c = importlib.util.module_from_spec(spec); spec.loader.exec_module(c)
g = open(E + "/harness/docs/guides/qa-evaluation-guide.md", encoding="utf-8").read().split("\n")
cl, rq = c.canonical_blocks(g)
raw = open(E + "/flutter-toolkit/skills/flutter-audit/SKILL.md", encoding="utf-8").read().split("\n")
lines = c.normalized(raw)
prov = sum(1 for l in raw if "qa-evaluation-guide.md" in l and "v5.1" in l and "사본" in l)
old = sum(1 for l in raw if "임계값은 2 다" in l)
dis = sum(1 for l in raw if l.startswith("<!-- markdownlint-disable MD029"))
en = sum(1 for l in raw if l.startswith("<!-- markdownlint-enable MD029"))
print(f"clauses={int(c.contains_block(lines, c.normalized(cl)))} req={int(c.contains_block(lines, c.normalized(rq)))} prov={prov} old={old} md029={dis}/{en}")
PY
    ;;
  SK-02)  # flutter-audit 자기 보고 틀 · 규칙이 두 카운터를 쓴다 (사본 밖에서 잰다)
    f=$FT/skills/flutter-audit/SKILL.md
    out=$(awk '/^<!-- markdownlint-disable MD029/{s=1} /^<!-- markdownlint-enable MD029/{s=0;next} /^#+ `UNVERIFIED_ENV` 남용 방지 4 요건/{q=1;next} q&&/^#/{q=0} !s&&!q' "$f")
    rep=$(printf '%s\n' "$out" | awk '/^Unverifiable/{f=1} f&&/^-{10,}/{exit} f')
    rules=$(secx '## Rules' "$f")
    echo "env_gaps=$(printf '%s\n' "$out" | n 'env_gaps') invalid=$(printf '%s\n' "$out" | n 'invalid_evidence') rep_env=$(printf '%s\n' "$rep" | n 'env_gaps') rep_inv=$(printf '%s\n' "$rep" | n 'invalid_evidence') rule_old=$(printf '%s\n' "$rules" | n '미검증 누계 임계(2 건)') rule_inv=$(printf '%s\n' "$rules" | all '임계' 'invalid_evidence') l3_4req=$(secx '## Gotchas' "$f" | all 'L3 Honesty' '4 요건')"
    ;;
  SK-03)  # 평가 사례 — 관례 표 없는 호출 사례가 있고 사례 16 은 그대로
    "$PY" - "$B/flutter-toolkit/evals/evals.json" "$FT/evals/evals.json" <<'PY'
import json, sys
b = json.load(open(sys.argv[1], encoding="utf-8"))["evals"]; e = json.load(open(sys.argv[2], encoding="utf-8"))["evals"]
ids = [x["id"] for x in e]
hit = [x for x in e if x.get("agent") == "widget-inspector" and "관례 표 없는 호출" in x.get("prompt", "")
       and any("건너뜀 — 관례 표 없는 호출" in a["text"] for a in x.get("assertions", []))]
b16 = [x for x in b if x["id"] == 16][0]; e16 = [x for x in e if x["id"] == 16]
print(f"cases={len(e)} ids_ok={int(ids == list(range(1, len(e) + 1)))} skip_case={len(hit)} case16_same={int(bool(e16) and e16[0] == b16)}")
PY
    ;;
  SK-04)  # 루트 CLAUDE.md 평가 사례 수 두 문장 = evals.json 사례 수
    N=$("$PY" -c 'import json,sys; print(len(json.load(open(sys.argv[1]))["evals"]))' "$FT/evals/evals.json")
    a=$(grep -F 'evals.json (flutter-toolkit/evals/evals.json)' "$E/CLAUDE.md" | grep -oE '[0-9]+개' | head -1)
    b=$(grep -F 'flutter-toolkit evals는' "$E/CLAUDE.md" | grep -oE '[0-9]+개' | head -1)
    echo "cases=$N commands=${a:-없음} conventions=${b:-없음}"
    ;;
  SK-05)  # flutter-kaizen Gotchas 에 Makefile 규칙 스킬 넷 교훈 한 줄
    secx '## Gotchas' "$FT/skills/flutter-kaizen/SKILL.md" | all 'flutter-preflight' 'flutter-run' 'flutter-ai-rules' 'project-detection' 'Step 2b' '허용 경로'
    ;;
  SK-06)  # codegen 안내 셋이 flutter-run 의 전후 삭제 수 블록을 가리킨다
    a=$(secx '## After Creation' "$FT/skills/flutter-api/SKILL.md" | all 'flutter-run' '삭제')
    b=$(secx '### 4. codegen 안내' "$FT/skills/flutter-feature/SKILL.md" | all 'flutter-run' '삭제')
    c=$(secx '## After Creation' "$FT/skills/flutter-screen/SKILL.md" | all 'flutter-run' '삭제')
    echo "api=$a feature=$b screen=$c"
    ;;
  SK-07)  # 평가 사례 18 — 시험 실행 명령이 flutter-test Step 4 와 같다
    "$PY" - "$FT/evals/evals.json" <<'PY'
import json, sys
e = [x for x in json.load(open(sys.argv[1], encoding="utf-8"))["evals"] if x["id"] == 18][0]
t = [a["text"] for a in e["assertions"]]
print(f"flutter_test={sum('$FLUTTER test' in x for x in t)} dart_verify={sum('$DART test로 검증' in x for x in t)} skill={e.get('skill')}")
PY
    ;;
  SK-08)  # build_runner Gotcha 가 EX-5 대로 · 명령의 플래그는 그대로 (UD-1)
    g=$(secx '## Gotchas' "$FT/skills/flutter-build/SKILL.md")
    flags=""; for s in flutter-run flutter-build flutter-preflight; do
      flags="$flags $(n 'build_runner build --delete-conflicting-outputs' < "$B/flutter-toolkit/skills/$s/SKILL.md")/$(n 'build_runner build --delete-conflicting-outputs' < "$FT/skills/$s/SKILL.md")"; done
    echo "old216=$(printf '%s\n' "$g" | n '이 플래그는 제거된 호환 옵션 목록으로 옮겨졌다') joined=$(printf '%s\n' "$g" | all '2.16' '2.7.0' '빼지 않는다' 'build_runner_command_line.dart') flags=[${flags# }]"
    ;;
  SK-09|SK-10)  # preflight 두 곳의 원인 가르기 절 (UD-3)
    if [ "$1" = SK-09 ]; then f=$FT/skills/flutter-preflight/SKILL.md; prep='pub get'; else f=$RK/skills/react-preflight/SKILL.md; prep='pnpm install'; fi
    s=$(secx '## 실패 원인 가르기' "$f")
    rows_ok=0; rows=$(sprint_rows)
    while IFS= read -r r; do printf '%s\n' "$s" | grep -qxF -- "$r" && rows_ok=$((rows_ok+1)); done <<< "$rows"
    echo "sec=$(printf '%s\n' "$s" | awk 'NF{c++}END{print c+0}') prov=$(printf '%s\n' "$s" | all 'harness/skills/sprint/SKILL.md' 'Step 3' '사본') rows=$rows_ok/$(cnt "$rows") merge_base=$(printf '%s\n' "$s" | n 'merge-base') wt=$(printf '%s\n' "$s" | n 'worktree add') prep=$(printf '%s\n' "$s" | n "$prep")"
    ;;
  ER-01)  # 원인 가르기 조각을 실제로 돌린다 — 알려진 답 `0 1 1`
    echo "flutter=[$(split_run "$FT/skills/flutter-preflight/SKILL.md")] react=[$(split_run "$RK/skills/react-preflight/SKILL.md")]"
    ;;
  SK-11)  # react-animation · animation-architect-react 의 <ViewTransition> (EX-9)
    g=$(secx '## Gotchas' "$RK/skills/react-animation/SKILL.md")
    echo "gotcha=$(printf '%s\n' "$g" | all '<ViewTransition>' '19.3' 'startTransition' 'react.dev/blog/2026/09/09/react-19-3') wrapper=$(n 'withViewTransition' < "$B/react-kit/skills/react-animation/SKILL.md")/$(n 'withViewTransition' < "$RK/skills/react-animation/SKILL.md") agent=$(n '<ViewTransition>' < "$RK/agents/animation-architect-react.md")"
    ;;
  SK-12)  # project-detection.md 가 project-detect.sh 를 부르고 JSON 키가 스크립트 출력과 같다
    d=$RK/references/project-detection.md
    doc_keys=$(awk '/^```json/{f=1;next} f&&/^```/{exit} f' "$d" | "$PY" -c 'import json,sys; print(" ".join(sorted(json.load(sys.stdin))))' 2>/dev/null)
    mkdir -p "$T/emptyproj"; out_keys=$( (cd "$T/emptyproj" && bash "$RK/scripts/project-detect.sh") | "$PY" -c 'import json,sys; print(" ".join(sorted(json.load(sys.stdin))))' 2>/dev/null)
    echo "call=$(all 'project-detect.sh' 'bash' < "$d") keys_same=$([ -n "$doc_keys" ] && [ "$doc_keys" = "$out_keys" ] && echo 1 || echo 0) nkeys=$(printf '%s' "$out_keys" | wc -w | tr -d ' ') script_changed=$(git -C "$W" diff --name-only "$BASE" "$TIP" -- react-kit/scripts | awk 'NF{c++}END{print c+0}')"
    ;;
  SK-13)  # plan-sync-github 의 GitHub 문서 버전 날짜 (EX-10)
    secx '## Gotchas' "$E/planning-kit/skills/plan-sync-github/SKILL.md" | all '2022-11-28' '2028-03-10' '2026-03-10' 'docs.github.com/en/rest/about-the-rest-api/api-versions'
    ;;
  SK-14)  # research-log backlog 줄 react-view-transitions
    l=$(grep -E '^\| `react-view-transitions` \|' "$E/docs/react/research-log.md")
    echo "row=$(cnt "$l") canary_wait=$(printf '%s\n' "$l" | n 'canary 대기') v193=$(printf '%s\n' "$l" | n '19.3')"
    ;;
  SK-15)  # 설계 문서 여덟 — last_updated 와 현행화 기록 절이 시작 판 기준 커밋을 모두 담는다
    for doc in $DOCS; do
      f=$KD/$doc
      # shellcheck disable=SC2046
      C=$(git -C "$W" log --no-merges --format=%H --since=2026-04-11 "$BASE" -- $(doc_paths "$doc") | cut -c1-7)
      rec=$(secx '## 현행화 기록' "$f")
      miss=0; while IFS= read -r h; do [ -z "$h" ] && continue; printf '%s\n' "$rec" | grep -qF -- "$h" || miss=$((miss+1)); done <<< "$C"
      printf '%s lu=%s commits=%s miss=%s\n' "$doc" "$(awk 'NR>2&&/^```$/{exit} /^last_updated: /{ if ($2 >= "2026-09-26") c++ } END{print c+0}' "$f")" "$(cnt "$C")" "$miss"
    done
    ;;
  SK-16)  # 설계 문서 사실 — 첫 줄 g6 다섯, 둘째 줄 나머지
    f=$KD/g6-build-audit.md; s3=$(secx '## 3. /react-preflight' "$f")
    echo "dev_strict=$(grep -E '^\| \*\*dev\*\* \|' "$f" | n 'strictPort') step8=$(printf '%s\n' "$s3" | grep -cE '^8\. ' || true) passed=$(printf '%s\n' "$s3" | n 'passed') skipped=$(printf '%s\n' "$s3" | n 'skipped') split=$(printf '%s\n' "$s3" | n 'merge-base') verdict=$(grep -E '^verdict:' "$f" | n 'BLOCKED')"
    printf 'g1_tpl=%s g1_strict=%s vt=%s fi_link=%s rep=' \
      "$(awk 'index($0,"13. harness")==1{f=1;print;next} f&&/^[^ ]/{exit} f' "$KD/g1-scaffolding.md" | n 'harness-project.yaml.template')" \
      "$(n 'strictPort' < "$KD/g1-scaffolding.md")" \
      "$(n '<ViewTransition>' < "$KD/g5b-animation.md")" \
      "$(all 'project-detect.sh' 'project-detection.md' < "$KD/final-integration.md")"
    for doc in g1-scaffolding.md g4-quality.md g5-ui-patterns.md g5b-animation.md g6-build-audit.md final-integration.md; do printf '%s,' "$(n 'render-evidence-protocol' < "$KD/$doc")"; done; echo
    ;;
  AR-01)  # 바뀐 파일이 기대 집합 안 · 커밋마다 맨 위 자리 하나
    ch=$(git -C "$W" diff --name-only "$BASE" "$TIP")
    extra=$(printf '%s\n' "$ch" | awk 'NF' | grep -vxF -- "$ALLOWED" || true)
    multi=0; for c in $(git -C "$W" rev-list --no-merges "$BASE..$TIP"); do
      k=$(git -C "$W" show --name-only --format= "$c" | awk -F/ 'NF{ if ($1=="docs") print $1"/"$2; else if (NF==1) print "(root)"; else print $1 }' | sort -u | awk 'END{print NR}')
      [ "$k" -gt 1 ] && multi=$((multi+1)); done
    echo "changed=$(cnt "$ch") extra=$(cnt "$extra") multi_top=$multi flutter=$(printf '%s\n' "$ch" | grep -c '^flutter-toolkit/' || true) react=$(printf '%s\n' "$ch" | grep -c '^react-kit/' || true) planning=$(printf '%s\n' "$ch" | grep -c '^planning-kit/' || true) docs_react=$(printf '%s\n' "$ch" | grep -c '^docs/react/' || true) root=$(printf '%s\n' "$ch" | grep -cx 'CLAUDE.md' || true)"
    [ -n "$extra" ] && printf 'EXTRA %s\n' $extra
    ;;
  AR-02)  # notes 가 커밋돼 있고 토큰을 담는다 · 둘째 줄은 문서 페이지 드리프트 (전제: 작업 폴더 HEAD 가 TIP)
    f=$E/$NOTES; committed=$(git -C "$W" cat-file -e "$TIP:$NOTES" 2>/dev/null && echo 1 || echo 0)
    printf 'committed=%s' "$committed"
    for t in KF-1 KF-2 KF-3 KF-4 KRe-1 KP-1 UD-1 UD-3 UD-6 go_router auto_route '<Activity>' ADR '바깥 근거 없음' '처리됨' tone-guide EX-5 EX-9 EX-10 react-reviewer REVIEWERS 'research-log.md:19' 'sprint/SKILL.md'; do printf ' %s' "$( [ -f "$f" ] && n "$t" < "$f" || echo 0)"; done; echo
    [ "$(git -C "$W" rev-parse HEAD)" = "$TIP" ] || { echo "PREMISE W_HEAD!=TIP"; return 2; }
    out=$(cd "$W" && "$PY" scripts/detect-docs-drift.py --since "$BASE" 2>&1); rc=$?
    pages=$(printf '%s\n' "$out" | grep -oE 'docs/[A-Za-z0-9_./-]+\.html' | sort -u)
    miss=0; while IFS= read -r p; do [ -z "$p" ] && continue; grep -qF -- "$p" "$E/$NOTES" 2>/dev/null || { miss=$((miss+1)); echo "MISS $p"; }; done <<< "$pages"
    echo "rc=$rc pages=$(cnt "$pages") miss=$miss"
    ;;
  DG-02)  # 더해진 줄의 markdownlint 새 경고 · JSON 읽기
    mdl_ready || { echo "mdl_unavailable"; return 2; }
    md=0; for p in $(git -C "$W" diff --name-only "$BASE" "$TIP" -- '*.md' ':(exclude).harness/sprint-*'); do
      o=$B/$p; [ -f "$o" ] || o=/dev/null; [ -f "$E/$p" ] || continue
      md=$((md + $(newmd "$o" "$E/$p")))
    done
    jb=0; for p in $(git -C "$W" diff --name-only "$BASE" "$TIP" -- '*.json'); do "$PY" -m json.tool "$E/$p" >/dev/null 2>&1 || jb=$((jb+1)); done
    echo "md_new=$md json_bad=$jb"
    ;;
  *) echo "모르는 조건 $1"; return 2 ;;
  esac
}
# === 측정 도우미 끝 ===
```
