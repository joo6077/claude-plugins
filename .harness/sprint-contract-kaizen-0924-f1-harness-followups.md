---
feature: "카이젠 2026-09-24 Final 후속 수정 — harness 쪽 (훅 이름 바꾸기 · 피드백 저장 워크트리 · 평가자 로그 폴더 · 평가 시각 · 삭제 열거 · 스키마 예시 · 옛 값 검사 범위 · V 줄 판정 · 드리프트 매핑 · CI 새 시험 · 오케스트레이터 Phase 17 · Codex 검토 r1 — Diff-Scope 상한 · CONTRACT_ROOT 정의 · 서명 줄 설명 · 플러그인 무시 필드 · 배치 우선순위)"
slug: kaizen-0924-f1-harness-followups
created: "2026-09-25 15:10"
complexity: "복잡"
conditions: 30
status: active
owner_session: de8c7935-a5b6-4df5-9106-fafa73c288a0
conditions_digest: sha256:a37827c20fae4fbe
locked_at: "2026-09-25 16:40"
---

## 배경

카이젠 2026-09-24 사이클의 Phase 1 ~ 17 은 모두 QA 승인으로 끝났다. 각 Phase 의 교차 진단(`scratchpad/kaizen/xdiag-all.md`)과 notes 가
Phase 범위 밖이라 못 고친 결함을 Final 로 넘겼다. Final 은 계약 셋으로 나뉜다(`scratchpad/kaizen/final-runbook.md` 「계약 셋과 범위」).
이 계약은 그중 harness 쪽이다 — `harness/` · `scripts/` · `.claude/skills/kaizen-orchestrator/` · `.claude/skills/*-kaizen/` · `.github/workflows/ci.yml`.
킷 폴더 결함은 `kaizen-0924-f1-kit-followups`, `.harness/` · 문서 사이트 · 처리 배정표 · 버전 계획은 `kaizen-0924-final` 이 맡는다.

읽은 입력은 지침의 「먼저 읽을 것」 다섯이다 — 공통 지침(`scratchpad/kaizen/phase-runbook.md`), 오케스트레이터 스킬 Step F1 ~ F4,
Final 처리 목록(`scratchpad/kaizen/final-todo.md`), 교차 진단 전문(`xdiag-all.md` P1 ~ P17), Phase notes 열일곱의
「넘기는 것」 · 「미반영 키와 사유」 · 「다음 사이클 메모」. 입력 항목 전부의 처리는 `범위 경계` 절의 입력 표에 있다.

고치는 결함은 둘로 나뉜다.

- **동작 결함 (검사 · 훅 · 스크립트가 틀린 답을 낸다)** — 커밋 안전 훅이 파일 이름만 바꾼 경로 지정 커밋을 「삭제 60 개」로 막는다(Phase 4 가 새로 만든 잘못된 차단).
  피드백 저장본의 `project_name` 이 워크트리 이름이다(일곱 Phase notes 가 같은 것을 적었다). 평가자의 사용자 교정 대조가 워크트리에서 로그 폴더를 못 찾는다.
  평가 시각을 짐작해 적는다. 삭제 열거가 옮긴 파일을 놓친다. 스키마의 측정 예시 둘이 실패를 삼킨다. 옛 값 검사가 킷 폴더 대부분을 안 읽는다.
  검증 스크립트가 실패한 V 줄에 판정을 안 적고, 사후 점검의 bare-fence 줄은 늘 통과한다. 문서 드리프트 검사가 api-kit · howto-kit · onboarding-kit 원본을 놓친다
- **문서 결함 (적힌 말이 실제와 다르다)** — 오케스트레이터 스킬 · 참조 문서가 Phase 17 을 빠뜨렸다. 카이젠 스킬 다섯이 틀린 수 · 죽은 검사를 적었다.
  카이젠 스킬 넷이 옛 계약 경로를 가르친다. 설계 가이드 둘 · 평가자 문서가 서로 어긋난 네 곳이 있다. CI 가 Phase 가 새로 만든 시험 여섯을 안 돌린다

편집 전 실측으로 입력에 없던 결함 셋을 더 찾았다 — `-i` 커밋도 이름 바꾸기를 삭제로 센다, 스키마의 봉인 세기 예시는 `fm_get` 이 없어도 「SEAL_BROKEN 0」 을 낸다,
사후 점검 `check_bare_fence` 가 `"0 bare"` 부분 글자로 판정해 늘 통과한다. 셋 다 같은 조건 안에서 고친다.

초안을 쓴 뒤 Codex 독립 검토(가지 전체 `83cfb4f..HEAD`, 이 계약 몫 7 건 — `scratchpad/kaizen/codex/r1-harness.md`)가 들어왔다. 지적마다 파일을 다시 읽고
명령을 돌려 확인했다. 다섯은 기존 조건에 더했다 — Diff-Scope 표준형이 커밋 전 두 상태를 허용하면서 상한 ref 를 늘 요구한다 ·
평가 가이드의 `CONTRACT_ROOT` 정의가 옛 규칙이다 · create-agent 가 플러그인에서 무시되는 `initialPrompt` 를 빠뜨렸다 · 에이전트 배치 우선순위 표에
managed settings 가 없다(넷 다 SK-05) · 스키마가 서명 줄 도우미를 실제보다 좁게 설명한다(ER-06). 하나는 ER-01 과 같은 결함이고, 하나(`assertions.json`
실행기)는 F1H-14 와 같아 고치지 않는다. 처리는 입력 표 F1H-83 ~ F1H-89.

그 뒤 REVIEW 검토(`.harness/.meta/kaizen-0924/f1-harness-followups-review.md`, 고칠 것 열 · 권하는 것 일곱)를 반영했다. V 줄 글자를 받는 쪽 하나
(`harness/docs/guides/plugin-validation-guide.md` §출력 포맷 예시)를 더해 파일이 서른하나가 됐다. 오케스트레이터 F2 매핑 표 · phase-dependencies 의 같은 결함 두 자리 ·
CI 의 zsh 설치 차례 · 평가 시각 블록의 `.bak` 부산물 · 공유 파일 직접 세기 · 함수 정의 확인을 조건 안에서 고쳤다. 새 조건은 없다. 처리는 입력 표 F1H-90 ~ F1H-95.

## 리서치 소스

- 이 계약은 새 외부 조회를 하지 않는다. 외부 사실은 사이클이 이미 모은 근거 파일에서만 옮긴다
  - `.harness/.meta/evidence/phase1.md:90` — 서브에이전트 동시 20 상한이 ultracode 에는 없다 ([Claude Code sub-agents](https://code.claude.com/docs/en/sub-agents.md), 이미 `agent-design-guide.md` 가 인용하는 문서)
  - `.harness/.meta/evidence/phase15.md:114` · `:131` — `etc_seq=663` 의 실제 제목은 「유형별로 알아보는 보도자료 작성 길잡이」
  - `.harness/.meta/evidence/phase1.md:87` · `phase4.md:148` — `initialPrompt` 는 플러그인 서브에이전트에서 무시된다
  - `.harness/.meta/evidence/phase4.md:149` — 에이전트 배치 우선순위는 managed settings · `--agents` · project · user · plugin 차례다
- 저장소 안 근거
  - `infra-kit/skills/infra-guide/SKILL.md:29` (Gotcha 13) — OpenTelemetry 상태는 signal 마다 다르다
  - `api-kit/skills/api-verify/SKILL.md:133` — 경로 간 불변식은 한쪽 경로가 없으면 Hurl 이 종료 코드 3 을 내 판정 불가를 가를 곳이 후처리뿐이다(실측 2026-09-24)
  - `.harness/.meta/orchestrator-audit-log.md:297` · `:472` — 킷 Phase 를 동시 5 개 · 4 개로 돌렸을 때 서브에이전트가 과부하 오류 529 로 죽었고, 2 ~ 3 개는 무사고
  - `reflect-kit/hooks/_lib-project-id.sh:63-78` (`project_root`) — 워크트리에서도 본 저장소 폴더를 내는 규칙. 피드백 저장 · 평가자 로그 조회가 같은 규칙을 쓴다
  - `scratchpad/kaizen/codex/r1-harness.md` — Codex 독립 검토(`gpt-5.6-sol`, 읽기 전용) 7 건. 공식 문서를 인용한 둘(r1 6 · 7)은 위 근거 파일로 다시 확인했다
- 새로 생긴 URL 은 전부 위 근거 파일에 있어야 한다(SK-06 (b))

## GAP 분석 · 개선안 초안

### 1.1 복잡도 4 축

| 축 | 물음 | 값 |
| -- | ---- | -- |
| 레이어 수 | 몇 개 계층을 관통하는가 | 넷 — 커밋 훅 · 저장소 검사 스크립트 · 평가자 · 스키마 문서 · CI |
| 공개 API·계약 변경 | 외부에 노출된 형태가 바뀌는가 | 예 — 훅 판정, 저장본 `project_name` 값, validate-plugin V 줄 글자, 드리프트 출력 줄, CI 단계 |
| 소비면 존재 | 반대편이 있는가 | 예 — 훅 시험 · README, `verify-feedback.sh` · 수집기, 사후 점검 · CI, 오케스트레이터 F2 |
| 회귀 위험 | 기존 동작이 깨질 수 있는가 | 예 — 훅의 기존 차단 열한 경우, CI 의 옛 값 검사 단계 |

넷 다 예라 **복잡**이다. 기능 조건 20 개 — Step 6.2 두 번째 명령으로 센 값(DG-05 포함). 가이드 상한 20 에 맞추려고 저장소 검사 · 사후 점검을 DG-05 하나로 묶었다.
Codex 검토 r1 에서 더한 다섯도 새 조건을 만들지 않고 같은 성격의 SK-05 · ER-06 에 측정으로 더했다(러닝북 「킷 또는 파일 묶음마다 조건 하나」).

### 1.2 설정 리터럴 대조표

| config key | project.yaml 에서 읽은 값 | 계약에 쓴 값 |
| ---------- | ------------------------- | ------------ |
| `commands.analyze` | `bash -n scripts/release.sh` | DG-01 N/A 사유에 그대로 |
| `commands.test` | `bash scripts/release.sh 2>&1 \|\| true` | DG-03 N/A 사유에 그대로 |
| `diagnostics.ide_exclude` | `[]` | DG-02 에 그대로 |
| `contract_categories[].id` / `prefix` | `Skill`/`SK` · `Script`/`SC` · `Error`/`ER` · `Architecture`/`AR` | 조건 절 네 개 |
| `anti_patterns[].id` / `message` | `AP-01` 버전 하드코딩 · `AP-02` force push · `AP-03` bare code fence · `AP-04` frontmatter name | AP-01 · AP-03 · AP-04 (AP-02 는 푸시를 하지 않아 뺐다) |

### 1.4 편집 전 감사 (시작 커밋 `5b4fd72` 판을 실제로 읽은 줄)

| 대상 파일 | 읽은 줄 | 기존 결함 | 조건 |
| --------- | ------- | --------- | ---- |
| `harness/scripts/commit-guard.sh` | `:163-182` `check_path_commit` · `:169` `ls-files --deleted` · `:212-214` `-i` 의 `ls-files --deleted` | 이름 바꾸기 감지 없이 셈 — `ren2.sh` 에서 N1 · N2 · N5 가 `hook_rc=2 git_dels=0 DISAGREE` | ER-01 |
| `harness/README.md` | `:52` 「이름 바꾸기는 세지 않는다」 · `:56` 경로 지정 커밋 문단 | 문장과 동작이 어긋남 | ER-01 (e) |
| `harness/scripts/save-feedback.sh` | `:138-143` `identity_root_of` 가 `--show-toplevel` | 워크트리 이름 — `ident.sh` 둘째 줄 `wt-x project_name=wt-x hash_is_main=0` | ER-02 |
| `harness/agents/qa-evaluator.md` | `:762` `BASE=$(basename …--show-toplevel…)` · `:821` Evaluated 틀 주석 · `:957` 「지문이 일치하면 저장한다.」 · `:667` 삭제 열거 · `:65` 「위 (c)」 · `:592` 표준형 5 요소 | 워크트리에서 `correction_log_status: unavailable`(실측) · 저장 절차에 `date` 블록 없음 · `--no-renames` 없음 · 가리킴 흐림 · 커밋 전 전제에도 상한 ref 가 없으면 REJECT | ER-03 · ER-04 · ER-05 · SK-05 (라)(마) |
| `harness/docs/guides/qa-evaluation-guide.md` | `:650` 같은 `BASE` · `:696` 삭제 열거 · `:1989` 짝 대조표 16 행 · `:757` `CONTRACT_ROOT` 정의 · `:789-790` 표준형 5 요소 | 평가자와 같은 결함 셋. 16 행은 맞다. `:757` 은 옛 `project.yaml` 기준(스키마 `:29` 는 먼저 만나는 `.harness/`) | ER-03 · ER-05 · SK-05 (마)(바) |
| `harness/docs/guides/skill-design-guide.md` | `:304` 「없음 — 이유」 · `:1144` 16 행 · `:1146` 「Item 16 은 Item 12 처럼 …」 | 평가자 규칙 11 (2) 보다 넓음 · 평가자 짝(Phase 3 이 만든 ⑤)을 모름 | SK-05 (가)(다) |
| `harness/docs/guides/agent-design-guide.md` | `:464` 동시 20 · `:572` 「없음 — 이유」 · `:703` 하드 리밋 행 · `:55-62` 배치 우선순위 표 · `:549` 플러그인 제약 | ultracode 예외 빠짐 · 허용 폭 넓음 · managed settings 빠짐 · `:549` 에 `initialPrompt` 빠짐(`:99` 는 넷) | SK-05 (가)(나)(사)(아) |
| `harness/references/contract-schema.md` | `:578` · `:650` `<base>..$(sprint_head <slug>)` · `:608` 봉인 세기 블록 · `:571-573` 표준형 5 요소 · `:670` 서명 줄 설명 | 상한 해석 실패 시 `B..HEAD` · 함수 정의가 없으면 `SEAL_BROKEN 0` (`sealcnt.sh` 실측) · 커밋 전 두 상태를 허용하면서 상한 ref 를 늘 요구 · 「끝 문단의 한 줄」 이 도우미 동작과 다름(`sigline.sh` `mine_middle=1`) | ER-06 · SK-05 (마) |
| `harness/docs/guides/contract-design-guide.md` | `:686` · `:695` 5 번 요소 · `:710-712` 추가 규칙 | 추가 규칙은 커밋 전 두 상태를 허용하는데 표는 상한 ref 를 늘 요구 | SK-05 (마) |
| `harness/skills/sprint-contract/SKILL.md` | `:56` Gotcha 표준형 5 요소 | 같은 모순 | SK-05 (마) |
| `harness/skills/create-agent/SKILL.md` | `:24` Gotcha · `:111` 체크리스트 | `initialPrompt` 빠짐 | SK-05 (사) |
| `scripts/check-stale-values.py` | `:21` 범위 한계 문단 · `:45` `SOURCE_DIRS` 열둘 | 킷 폴더를 안 읽음 — 사본 다섯 곳에 등록 옛 값을 넣어도 `rc=0 hits=0/5` | ER-07 |
| `scripts/validate-plugin.py` | `:877` V 줄 출력 · `:367` V3 · `:499` V5 · `:558` V6 · `:752` V9 요약 | 실패해도 V 줄에 판정 글자 없음 | ER-08 |
| `harness/docs/guides/plugin-validation-guide.md` | `:486-522` §출력 포맷 · `:506` · `:509` | 실패 V 줄 예시(`V3 refs 89 links, 2 BROKEN` · `V4 triggers 58 keywords, 1 duplicate`)가 판정 글자 없이 끝난다 — ER-08 뒤 실제 출력과 다르다 | ER-08 (c) |
| `scripts/validate-post-kaizen.py` | `:500-510` `check_bare_fence` 의 `"0 bare" in out` | 다른 킷 줄의 `0 bare` · `10 bare` 의 부분 글자로 늘 PASS (사본 A 실측) | ER-08 |
| `scripts/detect-docs-drift.py` | `:33-61` `SOURCE_TO_HTML` · `:66-77` 덮어쓰기 · `:190` 이름 규칙 | `docs/api/` · `docs/howto/` · onboarding 매핑 없음 · `SKILL.md` 가 `SKILL.html` 로 감 | AR-01 |
| `scripts/sync-orchestrator.py` | `:74` 범위 줄 틀 | 없는 `<킷>/references/` 를 적음(planning · bambu · onboarding) | AR-03 |
| `.github/workflows/ci.yml` | `validate` · `harness` 작업 전체 | 새 시험 여섯이 없음 | AR-02 |
| `.claude/skills/kaizen-orchestrator/SKILL.md` | `:9` · `:15` · `:25` · `:40` · `:100` · `:122` · `:152` · `:169` · `:173` · `:201` · `:566` · `:571-578` · `:749` · `:771` · `:601-615` Step F2 매핑 표 | Phase 17 빠짐 · 옛 범위 수 · 불변식 이유 틀림 · 동시 상한 · 서명 줄 안내 없음 · F2 표에 reflect · bambu · onboarding · howto 행이 없고 planning 행이 없는 `planning-kit/references/` 를 적음 | SK-01 · AR-01 (b) |
| `.claude/skills/kaizen-orchestrator/references/phase-dependencies.md` | `:56` · `:70` · `:77-82` · `:123-124` (`:124` 괄호 목록 포함) · `:130` | Phase 17 빠짐 · 없는 `onboarding-kit/references/` · 없는 `planning-kit/references/` · 리서치 전용 모드 목록에 howto 없음 | SK-02 |
| `.claude/skills/kaizen-orchestrator/references/phase-research-templates.md` | `:28` · `:116` · `:230` | 「500 라인 상한」 · 「3 signals stable」 · 출처 이름 틀림 | SK-02 |
| `.claude/skills/tone-kaizen/SKILL.md` | `:34` | 템플릿 「8종」(실제 6) | SK-03 |
| `.claude/skills/howto-kaizen/SKILL.md` | `:26` | 「두 셸」(러너는 세 셸 · 블록 네 경우) | SK-03 |
| `.claude/skills/onboarding-kaizen/SKILL.md` | `:35-41` Phase 4 | 게이트 평가 러너를 돌리는 줄 없음 | SK-03 |
| `.claude/skills/rust-kaizen/SKILL.md` | `:40` AR-02 검사 | `grep -rn … .` 이 자기 파일을 잡아 늘 1 이상 | SK-03 |
| `.claude/skills/infra-kaizen/SKILL.md` | `:24` 형제 표 · `:29` Gotcha 7 | 「미검증 3항」(Phase 8 뒤 네 칸) · history 계약 경로 | SK-03 · SK-04 |
| `.claude/skills/backend-kaizen/SKILL.md` · `design-kaizen/SKILL.md` | `:32` · `:31` Gotcha 7 | history 계약 경로 | SK-04 |
| `.claude/skills/react-kaizen/SKILL.md` | `:80` · `:82` Step 6 | history 계약 경로 · 「병렬 실행 중 git 쓰기 금지」 | SK-04 |

### Counterpart — 바뀌는 형태를 받아 쓰는 반대편

| 바뀌는 것 (만드는 쪽) | 받아 쓰는 쪽 | 다루는 곳 |
| --------------------- | ------------ | --------- |
| 커밋 안전 훅의 경로 지정 · `-i` 삭제 세기 | 훅 시험 `commit-guard-test.sh` · `harness/README.md` `## 커밋 안전 훅` · CI `harness` 작업 · `/sprint` Step 5 의 `git commit -o` | ER-01 (c)(e). `/sprint` 는 문구를 바꾸지 않는다 — 그 커밋 꼴이 이제 이름 바꾸기에서 막히지 않을 뿐이다 |
| 피드백 저장본 `project_name` · `project_hash` 값 (필드 이름 · 형식 그대로) | `verify-feedback.sh` · `scripts/collect-kaizen-data.py` §1 프로젝트 분포 · 카이젠 Step 2 집계 | ER-02 (a) `verify_rc=0`. 수집기는 값만 받는다 — 워크트리 이름이 본 저장소 이름으로 합쳐지는 것이 목적이다 |
| reflect-kit 로그 폴더 이름 (만드는 쪽 `project_root`) | 평가자 Step 3.4 · 평가 가이드 §읽기 전용이 절대 조건 | ER-03 — 받는 쪽을 만드는 쪽 규칙에 맞춘다 |
| validate-plugin V 줄 글자 | `validate-post-kaizen.py` `check_bare_fence`(부분 글자) · `check_validate_plugin`(Total 줄 — 안 바뀐다) · 수집기 §5(출력을 그대로 싣는다) · CI(종료 코드) · `plugin-validation-guide.md` §출력 포맷 예시 | ER-08 (a)(c) |
| 옛 값 검사 범위 · 종료 코드 | CI `Stale value check` 단계 | ER-07 (a) 원본 그대로 `clean rc=0` |
| 드리프트 매핑 줄(`원본 → 페이지`, 형식 그대로) | 오케스트레이터 F2 · docs-site 스킬 · 같은 매핑을 사람이 읽게 적은 오케스트레이터 F2 표 | AR-01 (a) · F2 표는 AR-01 (b). docs-site 스킬 매핑 표는 범위 밖(F1H-91) |
| 오케스트레이터 AUTO 범위 줄 | 오케스트레이터 SKILL.md AUTO 구간 · CI `Sync orchestrator check` | AR-03 (a)(b) |
| 스키마 예시 두 블록 | 계약 작성자가 베끼는 측정 | ER-06 — 받는 쪽은 베낀 사본이라 조건을 두지 않는다 |
| Diff-Scope 표준형의 상한 ref 요구 범위 | 평가자 Step 1.5 여섯째 · sprint-contract 자기진단 `diff_oracle_nonstandard`(`:792`) · 계약 가이드 체크리스트 `:1160` · 안티패턴 표 `:1133` | SK-05 (마) — 규칙을 정의하는 다섯 줄을 고친다. 뒤 셋은 「5 요소 중 빠졌는가」 만 묻고 뜻은 정의 줄을 따라 문구를 바꾸지 않는다 |
| 스키마 서명 줄 설명 (도우미 `mine` · `unsigned_on` 은 그대로) | 계약 작성자 · 이 계약의 공통 정의 | ER-06 (d) — 설명만 동작에 맞춘다 |

### 조건 작성 자문 (contract-schema §조건 작성 preflight 의 열 태그)

- `측정-수단-부재` · `측정-방식-불일치` — 모든 기능 조건에 도우미 명령 · 기대 출력을 적었다. 값은 `회귀 게이트` 절의 봉인 전 실측과 같다
- `측정-환경-오염` · `측정-상태-모호` — 측정은 공통 정의가 푸는 두 판(`$T/B` · `$T/E`)에서 돈다. 작업 폴더의 미커밋 변경 · 다른 Final 계약의 동시 작업이 끼지 않는다.
  예외는 실제 저장소를 읽어야 하는 둘(ER-03 의 `git -C` · DG-05 (d))이고, 전제를 조건에 적었다
- `측정-산출물-부재` — 모든 측정이 읽는 대상(도우미 · 두 판 · notes)을 공통 정의가 만들거나 이 계약 커밋이 만든다
- `검증경로-미기재` — 외부 도구는 `markdownlint-cli2` · `shellcheck` · `actionlint` · `zsh` 넷이다. 준비 단계 실측 값을 `회귀 게이트` 절에 적었다. 없으면 `TOOL_MISSING` 으로 멈춘다(`shcmp.sh`)
- `측정-중복` — V 줄 판정(ER-08)과 전체 검증 종료 코드(DG-05)는 대상이 다르다
- `태그-산출물-불일치` — 시험 경우 ㉖ ~ ㉙ 와 `워크트리 저장본 project_name` 은 이 계약이 내는 산출물이다
- `범위-미명시` · `증거-경로-부재` — 파일은 서른하나로 열거했고 notes · 검토 파일 경로를 적었다

### 개선안 초안 (조건별 — BUILD 가 따를 방향)

- **SK-01** 오케스트레이터 스킬 — 설명 · 첫 문단 순서 목록 끝에 `→ reflect-kit → bambu-kit → onboarding-kit → tone-kit → api-kit → howto-kit`,
  `argument-hint` 에 `phase12` ~ `phase17`, 의존성 그림에 `Phase 17: Howto-kit 카이젠 (howto-kaizen)`, 순서 논리 `17. Howto-kit 카이젠 — …`, 수동 목록 · F1 · F4 의 수를 17 로.
  「Phase 1~14」 네 곳은 「모든 Phase」 로 바꾸거나(`/meta-kaizen` · Step 0 · F4 체크리스트) 실제 범위로(`references/phase-research-templates.md` 줄 — 표가 16 까지다).
  공통 실행 패턴 절 끝에 두 줄 — 동시 상한(근거 감사 기록 경로 포함)과 서명 줄 안내(스키마 절 이름 포함). Phase 16 추가 지시의 불변식 이유를 api-verify 실측 문장으로
- **SK-02** phase-dependencies 에 Phase 17 블록 · 표 행 · 스킵 줄, `Phase 7~16` 두 곳을 `7~17` 로, Phase 14 블록 경로를 실제 폴더로.
  같은 파일의 같은 결함 두 자리도 — Phase 11 블록(`:56`)에서 없는 `planning-kit/references/` 줄을 빼고, `:124` 리서치 전용 모드 괄호 목록 끝에 `|howto` 를 더한다.
  research-templates 세 행 정정
- **SK-03** tone 「6종」, howto 「세 셸(zsh · bash · sh) … 게이트 블록 네 경우」, onboarding Phase 4 에 러너 줄과 `EVALS_PASS` 인용, rust AR-02 검사를 `rust-kit docs/rust` 로 좁힘, infra 형제 표 「`[미검증]` 네 칸」
- **SK-04** 넷 모두 계약 경로를 슬러그 경로 `` `.harness/sprint-contract-<slug>.md` `` 로(스키마 §계약 파일 — 산출물 경로). react Step 6 의 병렬 문단은 「내 경로만 싣는다 — `git add <내 경로> && git commit -o <내 경로>`」
- **SK-05** (가) 두 가이드의 「없음」 칸을 `` `없음 — 계약에 대체 검증 단계가 없음` `` 한 가지로 좁히고, 대체 단계가 있는데 건너뛰면 `없음` 이어도 `INVALID` 라는 문장(평가자 규칙 8 · 11 (2)).
  (나) 동시 20 상한 줄과 요약 표에 ultracode 예외. (다) skill 가이드 16 행 넷째 칸과 Item 설명 문단에 평가자 쪽 짝(`qa-evaluation-guide.md` §산출물이 검사일 때 ⑤). (라) 「위 (c)」 를 문단 이름으로.
  (마) 상한 ref 를 정의하는 다섯 줄(스키마 `**(5) 상한 ref**` 줄 · 계약 가이드 표 5 행 · 평가자 Step 1.5 여섯째 · 평가 가이드 같은 문단 · sprint-contract Gotcha)에
  같은 문장 「상한 ref 는 커밋 구간을 재는 조건에만 요구한다」 를 그 줄 안에 붙인다 — 커밋 전 두 상태(`git diff HEAD` · `--cached`)에는 상한이 없다.
  커밋 전 두 상태를 표준형에서 빼는 쪽은 택하지 않는다 — 계약 가이드 `:710-712` 가 그 두 상태의 쓸 자리를 이번 사이클에 정했다.
  (바) 평가 가이드 `:757` 을 스키마 문구 「처음 만나는 `.harness/` 디렉토리를 가진 조상의 절대경로」 로. (사) 플러그인 제약 세 자리(agent 가이드 `:549` ·
  create-agent `:24` · `:111`)에 `initialPrompt`. (아) 배치 우선순위 표 맨 위에 managed settings 행, 기존 네 행을 2 ~ 5 로.
  가이드 머리의 `version` 은 올리지 않는다 — 평가 가이드 · 계약 가이드의 `Parity with` 값이 같이 움직여야 해서다. 문구 정정이다
- **ER-01** 경로 지정 커밋: 임시 목록을 HEAD 로 채운 뒤 지정 경로 안에서 git 이 아는 파일(HEAD 와 실제 목록의 합)의 작업 폴더 상태를 얹고,
  `diff --cached -M --diff-filter=D HEAD` 로 센다. `-i` 는 실제 목록 사본에 같은 방식으로 얹는다. 기존 도우미(`block` · `top_dirs`)로 막는다. 시험 ㉖ ~ ㉚ 와 README 한 문장.
  ㉚ 은 옮긴 새 경로가 지정 경로 밖이라 삭제가 그대로 실리는 경로 지정 커밋(`git mv d1 d2` 뒤 `git commit -o -- d1`)을 막는 경우다 — 계약 도우미 `ren2.sh` 의 N4 와 같은 꼴을 CI 가 도는 시험에도 둔다
- **ER-02** `identity_root_of` 를 reflect-kit `project_root` 와 같은 규칙으로(`--git-common-dir` 가 `--git-dir` 와 다르고 이름이 `.git` 이면 그 부모). 저장 시험에 워크트리 경우
- **ER-03** Step 3.4 블록이 본 저장소 이름(`--git-common-dir` 부모)과 워크트리 이름(`--show-toplevel`) 둘을 hash 접미 포함으로 합쳐 찾는다. 가이드 블록을 같이 고친다
- **ER-04** Step 5 「지문이 일치하면 저장한다.」 뒤에 한 문장과 `$OUT` 을 받는 bash 블록 — `Evaluated:` 줄을 그 순간의 `date '+%Y-%m-%d %H:%M'` 로 덮어쓰고 그 줄을 출력한다(BSD · GNU `sed` 둘 다 도는 꼴).
  블록은 리포트 옆에 새 파일을 남기지 않는다 — `sed -i.bak` 을 쓰면 `.bak` 을 지운다(또는 임시 파일에 쓰고 `mv`). 안 지우면 평가마다 `.harness/` 에 `sprint-feedback-<slug>.md.bak` 이 쌓인다
- **ER-05** 두 문서의 두 명령에 `--no-renames`
- **ER-06** 두 예시를 `U=$(sprint_head <slug>) || exit 2` 뒤 `<base>..$U` 로. 봉인 세기 블록 머리에 `verify_seal` · `fm_get` 정의 확인 — 없으면 종료 코드 0 이 아닌 값으로 멈춘다.
  서명 줄 설명 `:670` 의 「끝 문단의 한 줄」 을 도우미가 실제로 하는 일(메시지 어느 문단이든 글자가 똑같은 한 줄)로 고친다. 도우미를 끝 문단만 읽게 바꾸는 쪽은
  택하지 않는다 — 봉인된 Phase 계약들이 같은 도우미를 베껴 쓰고 있어 설명만 맞추는 것이 가장 작은 고침이다.
  새 설명에 「서명 줄을 끝 문단에 두는 관례는 그대로 둔다 — 도우미가 자리를 보지 않을 뿐이다」 를 함께 적는다. 옛 문장을 통째로 지우면 다음 작성자가 서명 줄을 아무 데나 둔다
- **ER-07** 킷 폴더는 `.claude-plugin/marketplace.json` 의 `source` 에서 읽고 backend-kit 만 뺀다 — 세 줄이 OpenAPI 3.1.1 명세 링크를 인용해 걸리고, 그 예외 등록부(`.harness/stale-values.yaml`)는 이 계약 범위 밖이다.
  같은 파일을 두 번 세지 않는다. 뺀 폴더는 출력에 `검사 제외: backend-kit — <이유>` 로 적는다. 머리 문단의 「docs-site 파이프라인 전용」 범위 한계 문장을 새 범위로 바꾼다.
  제외 이유 글자에 버전꼴 숫자(`x.y.z`)와 근거 파일 밖 URL 을 쓰지 않는다 — AP-01 · SK-06 (b) 와 부딪힌다
- **ER-08** V 줄 요약이 판정 글자로 끝나지 않으면 `— <판정>` 을 붙인다. `check_bare_fence` 는 `--check=code-fence` 의 종료 코드로 판정한다.
  받는 쪽인 검증 가이드 §출력 포맷 예시의 실패 V 줄도 같은 꼴(`— FAIL` · `— WARN`)로 고친다. 실패 예시는 지우지 않는다.
  검증 가이드의 머리 `version` 은 올리지 않고 변경 이력 표에 행을 더하지 않는다 — 그 표의 여섯 행이 모두 `x.y.z` 꼴(`plugin-validation-guide.md:655-660`, 머리 `version: 1.4.0`)이라 새 행이 AP-01 에 걸린다
- **AR-01** `docs/api/` → `docs/api-kit/` · `docs/howto/` → `docs/howto-kit/` · onboarding 참조 → `docs/onboarding-kit/`, 스킬 본문 `SKILL.md` 는 그 스킬 폴더 이름을 페이지 이름으로, 예제 원본 하나는 덮어쓰기 표에.
  오케스트레이터 F2 표에 reflect-kit · bambu-kit · onboarding-kit · howto-kit 행을 드리프트 매핑과 같은 원본으로 더하고, planning-kit 행에서 없는 `planning-kit/references/` 를 뺀다
- **AR-02** `validate` 작업에 zsh 설치 단계 하나와 시험 여섯. zsh 설치 단계는 여섯 시험 단계 모두보다 앞에 둔다 — reflect-kit 시험 둘은 zsh 가 없으면
  zsh 경우를 건너뛰고 통과한다. notes 표의 `\|\|` 는 `||` 로 풀어 넣는다
- **AR-03** 범위 줄 틀: 킷 바로 아래 `references/` 가 있으면 그것, 없고 `skills/*/references/` 가 있으면 그것, 둘 다 없으면 참조 폴더를 적지 않는다. 그 뒤 `python3 scripts/sync-orchestrator.py` 로 AUTO 구간을 다시 만든다
- **AR-04** notes 를 쓰고 커밋 · `end_sha` 를 러닝북대로 덧붙인다

## 범위 경계

- 이 계약 시작 HEAD: `5b4fd72d5587c937c1875ddb62872f32ae087dcf` (`git rev-parse HEAD`, 2026-09-25). 범위 상한은 개정 파일
  `.harness/sprint-amendments-kaizen-0924-f1-harness-followups.md` 의 `end_sha:` 마지막 값이다. `kaizen-0924-f1-kit-followups` 가 같은 가지에 동시에 커밋하므로 `HEAD` 로 재지 않는다
- 고치는 파일은 서른하나다(공통 정의 `FILES`) — 마크다운 스물하나(`MDS`) · 셸 넷(`SHS`) · 파이썬 다섯(`PYS`) · `.github/workflows/ci.yml`. 새 파일은 없다.
  Codex 검토 r1 로 마크다운 셋(`harness/docs/guides/contract-design-guide.md` · `harness/skills/sprint-contract/SKILL.md` · `harness/skills/create-agent/SKILL.md`)이,
  REVIEW 검토로 V 줄 글자를 받는 쪽인 `harness/docs/guides/plugin-validation-guide.md` 하나가 늘었다.
  `.harness/` 쪽은 이 계약 · 개정 파일 · QA 피드백 · notes `.harness/.meta/kaizen-0924/f1-harness-followups-notes.md` · 검토 기록 `.harness/.meta/kaizen-0924/f1-harness-followups-review.md` 다섯만 쓴다(공통 정의 `MYHARNESS`)
- **이 계약의 커밋 메시지에는 전부 `Co-Authored-By` 줄 바로 위에 서명 줄 `Kaizen-Phase: kaizen-0924-f1-harness-followups` 한 줄을 넣는다** (봉인 커밋 포함).
  AR-04 · AR-05 · SC-00 · DG-01 · DG-03 · DG-04 가 이 줄로 이 계약 커밋을 가린다(`harness/references/contract-schema.md` §여러 주체가 한 가지에 커밋할 때 선택지 B).
  notes 커밋도 이 계약 커밋이다 — notes 를 커밋한 뒤 그 sha 로 `end_sha:` 줄을 하나 더 덧붙여 커밋한다(옛 줄은 지우지 않는다)
- 커밋은 **`git add -- <파일> && git commit -o -- <파일…>` 로 내 파일만** 싣는다. 한 커밋에 킷 하나 — `harness/` 파일과 `scripts/` · `.github/` · `.claude/skills/` 파일은 커밋을 나눈다.
  AR-03 은 `scripts/sync-orchestrator.py` 와 다시 만든 오케스트레이터 SKILL.md 를 한 커밋에 싣는다
- 이 세션의 커밋 안전 훅 · qa-evaluator 는 설치본이다 — 이 가지의 새 판은 BUILD 커밋과 QA 에 걸리지 않는다. 새 판의 동작은 ER-01 · ER-03 · ER-04 가 사본에서 잰다
- 측정이 기대는 제목 · 줄 머리는 이름을 바꾸지 않는다: `## 커밋 안전 훅` (README) · `### Step 5:` · `### Step 3.4:` (qa-evaluator) · `### Phase 4:` (onboarding-kaizen) ·
  `## Phase 의존성` · `### 각 Phase 공통 실행 패턴` · `<!-- AUTO:plugin_phases:begin -->` (오케스트레이터) · `| 16 |` · `Item 7 은` (skill 가이드) · `| **하드 리밋** |` · `### 배치 위치 (우선순위순)` (agent 가이드) ·
  `**(5) 상한 ref**` · `mine() {` 가 든 bash 블록 (스키마) · `| 5 | **상한 ref** —` (계약 가이드) · `중 빠진 것을 REJECT 사유에 열거한다` (평가자 · 평가 가이드) · `표준형 5 요소를 다 채워라` (sprint-contract) ·
  `### 출력 포맷` (검증 가이드) · `**소스 → 출력 매핑` · `**절차:**` (오케스트레이터 F2)
- 공유 파일(`marketplace.json` · 킷 `plugin.json` 버전 · 루트 README · 루트 CLAUDE.md · `docs/` HTML · 처리 배정표 · 감사 기록 · 실패 횟수 파일 · `docs/kaizen/*.md` ·
  `docs/*/research-log.md` · `.harness/stale-values.yaml`)과 킷 폴더(`harness` 제외 열셋)는 건드리지 않는다 — AR-05 (c)(f). `docs/*/research-log.md` 는 kit-followups 가
  고치는 파일이라 (f) 목록에 넣지 않고 (a) · (c) 로 잰다
- 편집 전부터 있던 경고(마크다운 21 파일 합계 242 줄 — 초안의 17 파일 187 줄에 Codex 검토로 늘어난 셋 8 · 9 · 8 줄 · REVIEW 검토로 늘어난 검증 가이드 30 줄 · `commit-guard-test.sh` 의 shellcheck 2 줄)는 범위 밖이다 — DG-02 는 파일마다 (규칙, 줄 글자) 묶음이 느는지만 잰다
- CI 새 단계는 우분투에서 돌려 보지 못했다 — 이 기계(macOS · dash · bash 3.2 · bash 5 · zsh 5.9)의 사본에서 여섯 시험이 모두 통과했다(`회귀 게이트` 표). 첫 CI 실행 확인은 입력 표 F1H-82
- 사용자 승인(Step 5) 대체: 사용자가 「자동으로 끝까지 알아서 진행해 내 허락이 필요한건 코덱스로 리서치나 검토받고」라고 위임했다(세션
  `de8c7935-a5b6-4df5-9106-fafa73c288a0` 기록 queued_command `2026-09-24T04:04:16.964Z`). Codex 사용량 한도가 소진돼(오류 원문 「You've hit your usage limit … try
  again at 11:05 PM」, 2026-09-24) 독립 Claude 검토자(REVIEW 에이전트)가 대신한다. 이어 사용자가 「코덱스 대신에 그냥 너가 알아서 진행하라고」라고 명시했다(같은 세션
  기록 user `2026-09-24T11:54:58.940Z`). 검토 결과 파일: `.harness/.meta/kaizen-0924/f1-harness-followups-review.md` — 1 회차 판정 `VERDICT: CHANGES`.
  고칠 것 열(C1 ~ C10)과 권고 일곱(R1 ~ R7)은 DRAFT 가 이 초안에 넣었다. 같은 파일 `## 2 회차` 의 마지막 판정도 `VERDICT: CHANGES` 다 — 1 회차 열일곱은 모두 반영됐다고 확인하고
  새 고칠 것 둘(C11 ER-07 예외가 파일 이름을 찍지 않는 출력을 가리킴 · C12 AR-05 (d) 가 살아 있는 작업 폴더를 읽음)과 권고 하나(R8 검증 가이드 이력 표)를 냈다.
  BUILD 가 봉인 전에 셋 다 넣었다 — C11 은 ER-07 예외 첫 문장을 검토가 준 글자 그대로, C12 는 AR-05 (d) 를 `$T/E` 로 읽게 바꾸고 봉인 전 실측 표에 한 줄(값은 BUILD 가 다시 재어 검토 값과 같음),
  R8 은 개선안 ER-08 끝 문장. 새 실측이 필요 없는 문구 고침이라 3 회차 검토는 돌리지 않았다. 반영하지 않은 지적은 없다
- Codex 독립 검토: 이어 사용자가 「코덱스도 사용할 수 있으니깐 사용해」 라고 했다(같은 세션 기록 user `2026-09-25T06:19:45.056Z`). 가지 전체(`83cfb4f..HEAD`)를
  Codex(`gpt-5.6-sol`, 읽기 전용)가 세 묶음으로 검토했고 이 계약 몫은 `scratchpad/kaizen/codex/r1-harness.md` 7 건이다. 지적마다 파일을 다시 읽거나 명령을 돌려
  확인한 처리는 입력 표 F1H-83 ~ F1H-89. 공식 문서를 인용한 둘(r1 6 · 7)은 근거 파일 `phase1.md` · `phase4.md` 에 같은 내용이 있어 조건으로 삼았다
- 이 계약은 DRAFT 가 쓰고 BUILD 가 위 2 회차 반영 뒤 봉인(6.6) · 봉인 커밋 · 구현을 한다. `conditions_digest` · `locked_at` 은 봉인 때 채운다
- 측정 해소: SK-01 ~ SK-05 · ER-01 (e) · ER-03 (c) · ER-04 (b) · ER-05 (a) · ER-06 (a) · ER-07 (b) · ER-08 (c) · AR-01 (b) · AR-03 (c) — 산출물이 문서 문장이라 정해진 파일 · 절 · 줄에 정해진 글자가 있는지가 판정이다.
  글자는 문장 전체라 낱말이 옆 문장에 있어 통과하는 일이 없다 — `toks.py` 백열 줄 가운데 새 글자 일흔은 시작 커밋 판에서 전부 0, 옛 글자 서른아홉은 전부 1 이상이다(실측). 남은 한 줄 SK05-N8 은 바뀌지 않아야 할 평가 가이드 16 행이다. 그 글자만 지운 사본에서는 해당 줄이 NG 로 떨어진다(글자가 곧 그 문장이다).
  ER-08 (c) 는 검증 가이드 예시 절의 V 줄을, AR-01 (b) 는 오케스트레이터 F2 표 행을 센다 — 둘 다 시작 커밋 판에서 떨어지는 값을 적었다
- 새 글자는 한 줄 안에 둔다 — `toks.py` 는 줄마다 세므로 긴 문장을 줄바꿈으로 가르면 NG 다. 이 계약이 고치는 가이드들은 한 문장을 여러 줄로 감싸는 곳이 많다
- 측정 해소: ER-01 ~ ER-08 (a)(b) · AR-01 (a) · AR-02 · AR-03 (a) — 훅 · 스크립트 · 문서 블록을 사본에서 실제로 돌린 출력이다. 알려진 답(git 이 실제로 싣는 삭제 수 · 손으로 아는 폴더 이름 ·
  실제로 있는 페이지 이름 · 따로 센 파일 수)과 시작 커밋 판 음성 대조가 붙어 있고, 도우미마다 고친 모의본에서 기대 출력이 나오는지 봉인 전에 돌려 도우미가 살아 있음을 확인했다
- 측정 해소: SK-05 (d)(e) · ER-06 (d) — 문서 줄 짝(`upref.sh`) · 표 행 차례 · 스키마 도우미를 임시 저장소에서 돌린 출력(`sigline.sh`)이다. `upref.sh` 는 시작 커밋 판 `upper=0/5`,
  개선안대로 고친 모의본 `upper=5/5`. `sigline.sh` 는 도우미가 바뀌지 않아 두 판이 같다 — 새 설명 문장(ER06-N2)이 실제 동작과 맞는다는 알려진 답이고, 음성 대조는 옛 설명 문장(ER06-O2)이다
- 측정 해소: SK-06 · AP-01 · RE-01 — 더한 줄을 세는 계산이다. 양성 대조가 붙어 있다
- 측정 해소: AR-04 · AR-05 · SC-00 · DG-01 · DG-03 · DG-04 — 커밋 기록 · notes 글자 · 봉인 검증 함수를 실제로 돌린 출력이다
- 측정 해소: DG-02 · DG-05 · AP-03 — 린터 · 검사 스크립트를 실제로 돌린 출력이다
- 커버리지 해소: 모든 조건 — 산문의 파일 이름은 측정의 `"$T/E/…"` · `"$T/B/…"` · 공통 정의 배열(`FILES` · `MDS` · `SHS` · `PYS` · `MYHARNESS`)이고, 도우미는 측정의 `"$K/…"` 로 부른다. 검출기는 공백 든 코드 조각 안의 인자를 읽지 못한다
- 커버리지 해소: AR-01 — 산문의 `reflect-kit/skills/` · `docs/howto/` · `SKILL.md` · `SKILL.html` 은 결함 설명(어느 매핑이 빠졌고 어디로 잘못 가는지)이다. 측정은 그 결함이 걸린 원본 열세 파일을 `drift.sh` 로 돌리고 기대 줄 열셋에 `docs/howto/deep-links.md` · `reflect-kit/skills/codex-kaizen/SKILL.md` 를 담는다
- 커버리지 해소: AR-03 — 산문의 `references/` · `skills/*/references/` 는 범위 줄 규칙이다. 측정의 기대 세 줄이 그 규칙의 세 경우(참조 폴더 없음 · 스킬 폴더 아래 참조 둘)를 글자 그대로 담는다
- 커버리지 해소: AP-04 — 측정의 `<파일>` · `<이름>` 은 산문에 열거한 열두 파일 · 이름이다(`.claude/skills/<폴더>/SKILL.md` 아홉 · `harness/skills/<폴더>/SKILL.md` 둘 · `harness/agents/qa-evaluator.md`)
- 기능 조건 20 · 전체 조건 줄 30 (Step 6.2 두 명령으로 센 값)

### 입력 표 — 항목마다 처리

처리 칸: `조건 <ID>` · `확인만 — <근거>` · `다른 계약 — <슬러그>` · `고치지 않음 — <이유>`. `고치지 않음` 인 ID 는 AR-04 (b) 가 notes 의 다음 사이클 메모에 있는지 센다.

| ID | 출처 | 항목 | 처리 |
| -- | ---- | ---- | ---- |
| F1H-01 | final-todo P1 · xdiag P1 (2) a | p01 notes 커밋이 `end_sha` 밖 · ER-04 셋째 · AR-04 ② 재측정 | 다른 계약 — `kaizen-0924-final` (`.harness/` 개정 파일) |
| F1H-02 | final-todo P1 · xdiag P1 (2) b | p01 SK-01 측정이 핵심 문장 삭제를 못 잡음 | 다른 계약 — `kaizen-0924-final` (계약 피드백 교차 진단 기록) |
| F1H-03 | final-todo P1 · xdiag P1 (2) d | p01 QA 리포트 `:39` 대조 실행 주장 | 다른 계약 — `kaizen-0924-final` (평가자 피드백 교차 진단) |
| F1H-04 | final-todo P1 계약 밖 1 | 「시도한 우회: 없음 — 이유」 허용 폭 | 조건 SK-05 (가) — Phase 3 · 4 가 고치지 않았다(SK05-O1 · O2 시작 판 1 · 1) |
| F1H-05 | final-todo P1 계약 밖 2 | ultracode 동시 20 제한 | 조건 SK-05 (나) |
| F1H-06 | final-todo 모든 Phase 공통 | Phase 2 이후 notes 뒤 `end_sha` 덧붙임 확인 | 다른 계약 — `kaizen-0924-final` |
| F1H-07 | final-todo 오케스트레이터 첫째 | 의존성 그림 · 순서 논리에 Phase 17 없음 | 조건 SK-01 · SK-02 (참조 문서에 같은 결함) |
| F1H-08 | final-todo 오케스트레이터 둘째 | F1 범위 · F4 scope 격리 · failure-count 범위 | 조건 SK-01 |
| F1H-09 | final-todo 오케스트레이터 셋째 | 킷 Phase 동시 실행 수 한 줄 | 조건 SK-01 — 넣는다(감사 기록 `:297` · `:472` 두 사이클) |
| F1H-10 | final-todo P2 · xdiag P2 (2) | ER-01 · ER-03 · AR-06 측정 결함 | 다른 계약 — `kaizen-0924-final` |
| F1H-11 | final-todo P2 계약 밖 1 | `<base>..$(sprint_head <slug>)` | 조건 ER-06 (a)(c) |
| F1H-12 | final-todo P2 계약 밖 2 | `Evaluated` 가 `date` 출력 아님 | 조건 ER-04 — Phase 3 틀 주석 뒤에도 p04 · p15 · p16 리포트가 재발(실측) |
| F1H-13 | final-todo P3 · xdiag P3 (2) | 옛 값 검사에 `harness/agents` · `harness/evals` 없음 | 조건 ER-07 |
| F1H-14 | final-todo P3 · xdiag P3 (2) · Codex r1 2 (F1H-84) | `run-evals.py` 가 `evals.json` 만 읽음 · `assertions.json` 회귀 패턴 #1 #2 · 실행기 없음 | 고치지 않음 — 실행기는 새 도구다. 오케스트레이터 Gotcha 「Final에서 새 기능을 추가하지 마라」, Phase 4 가 다음 사이클로 넘겼다 |
| F1H-15 | final-todo P3 · xdiag P3 (2) | `verify_seal` 미정의 시 조용히 0 | 조건 ER-06 (b) — 편집 전 실측에서 `fm_get` 만 빠져도 79 개가 전부 `SEAL_ABSENT` 로 나오는 것까지 찾았다 |
| F1H-16 | final-todo P3 계약 밖 1 | 삭제 열거 `--no-renames` | 조건 ER-05 |
| F1H-17 | final-todo P3 계약 밖 2 | 짝 대조표 16 행 어긋남 | 조건 SK-05 (다) — skill 가이드를 고친다. 평가 가이드의 ⑤ 는 Phase 3 이 실제로 만든 짝이다 |
| F1H-18 | final-todo P3 작은 것 첫째 | `qa-evaluator.md:65` 「위 (c)」 | 조건 SK-05 (라) |
| F1H-19 | final-todo P3 작은 것 둘째 | `qa-evaluator.md:671` 「50 개를 넘는 삭제만 막는다」 | 확인만 — Phase 4 뒤 경로 지정 커밋도 50 개 넘는 삭제를 막아 문장이 맞다. ER-01 뒤에도 맞다 |
| F1H-20 | final-todo 여러 Phase 첫째 | DG-02 새 MD024 (P7 · P8 · P9 · P11) · P12 ~ 17 전수 | 다른 계약 — `kaizen-0924-f1-kit-followups` |
| F1H-21 | final-todo 여러 Phase 둘째 | 옛 값 검사 `SOURCE_DIRS` 에 킷 폴더 대부분 없음 | 조건 ER-07 — 넓힌다(실측: 킷 열넷 가운데 backend-kit 만 3 줄이 걸리고 나머지 0) |
| F1H-22 | final-todo 여러 Phase 셋째 | 마지막 `end_sha` 커밋이 구조상 범위 밖 | 다른 계약 — `kaizen-0924-final` |
| F1H-23 | final-todo 여러 Phase 넷째 | QA 리포트 요약 수 오기 | 다른 계약 — `kaizen-0924-final` |
| F1H-24 | final-todo 여러 Phase 다섯째 · xdiag P6 (2) 1 | V3 · V4 · V5 · V9 실패가 V 줄에 FAIL 없음 | 조건 ER-08 |
| F1H-25 | final-todo P4 계약 밖 · xdiag P4 · Codex r1 1 (F1H-83) | 훅이 이름 바꾸기를 삭제로 셈 · README `:52` · 시험 | 조건 ER-01 — `-i` 커밋의 같은 결함(편집 전 실측 N5)도 |
| F1H-26 | final-todo P5 · P6 · P8 · P9 · P10 계약 밖 | 킷 파일 결함 | 다른 계약 — `kaizen-0924-f1-kit-followups`. P6 RE-02 정규식은 계약 측정 결함이라 `kaizen-0924-final` |
| F1H-27 | final-todo P12 ~ 17 · xdiag P17 계약 밖 2 | CI 줄 `\|\|` 풀기 | 조건 AR-02 (b) |
| F1H-28 | final-todo P12 · xdiag P12 ~ P17 계약 밖 | reflect · bambu · onboarding · tone · api · howto 킷 결함 | 다른 계약 — `kaizen-0924-f1-kit-followups`. 예외: xdiag P13 계약 밖 3(평가자가 워크트리 이름으로 로그를 찾음)은 조건 ER-03 |
| F1H-29 | phase1-notes §Final 에 넘기는 것 둘째 | phase-research-templates `:28` 「500 라인 상한」 | 조건 SK-02 |
| F1H-30 | phase1 ~ 17 notes §Final | 문서 사이트 페이지 재생성 | 다른 계약 — `kaizen-0924-final` (F2) |
| F1H-31 | phase1-notes §넘기는 것 | `sprint/SKILL.md:77` · create-agent · create-skill | 확인만 — Phase 4 반영(`15 종` · `1500-2000 words` · `` `[미검증]` + 사유 한 줄 `` 모두 0) |
| F1H-32 | phase1 · 2 · 3 · 12 · 15 · 16 · 17 notes · 러닝북 Phase 12 과제 · `reflect-collector:P5` · `harness:P02` 비고 | 저장본 `project_name` 이 워크트리 이름 | 조건 ER-02 |
| F1H-33 | phase2-notes §넘기는 것 — Phase 3 | `qa-evaluator.md:590` · `:1217` · 평가 가이드 `:12` · `:742` · `:746` · `:1785` · `:1862` · `:1915` | 확인만 — Phase 3 반영(평가 가이드 `Parity with` 가 1.6.0 · 1.7.0 · v5.1) |
| F1H-34 | phase2-notes §Phase 4 가 읽을 것 | `/sprint` 사용자가 할 일 · 초안 필수 필드 · contract-kaizen Step 2 | 확인만 — Phase 4 SK-04 · ER-02 · SK-06 반영 |
| F1H-35 | phase2-notes §Phase 4 가 읽을 것 · phase4-notes | `feedback-schema.yaml` true 뜻 · 새 키 둘 | 고치지 않음 — Phase 4 넘김대로 다음 사이클 Phase 2 · 3. `verify-feedback.sh` 가 체크리스트 키를 재지 않아 지금 저장 · 검증을 막지 않는다(`grep -n checklist harness/scripts/verify-feedback.sh` 0 줄) |
| F1H-36 | phase2-notes §Final 에 넘기는 것 둘째 | 서명 줄 규약을 러닝북 · 오케스트레이터가 스키마 절로 가리키게 | 조건 SK-01 (오케스트레이터 쪽). 러닝북은 레포 밖 작업 파일이라 이 계약이 고치지 않는다 |
| F1H-37 | phase2 · 3 · 4 · 7 · 9 · 10 notes §다음 사이클 메모 | 개정 번호 규칙 · 열 번호 정규식 · 측정 묶음 관례 · 도우미 추출 스크립트 · 봉인 둘째 줄 · `mktemp` 폴더 · 측정 공통 정의 예시 · 검사기가 돈 줄 · 추적 규칙 표 | 고치지 않음 — 계약 스키마 · 설계 가이드의 새 규칙이라 다음 사이클 Phase 1 · 2 · 4 몫 |
| F1H-38 | phase3-notes §넘기는 것 | §3.7 ①~④ 생성 측 짝 · 스키마 ①~④ 계약 측 짝 | 고치지 않음 — 새 절 신설, 다음 사이클 Phase 1 · 2 |
| F1H-39 | phase3 · 4 notes | `.harness/feedback-draft.yaml` 고정 이름 · sprint-contract Step 9 문구 | 고치지 않음 — Phase 4 넘김대로 다음 사이클 Phase 2 |
| F1H-40 | phase4-notes §넘기는 것 | `# sprint-scope` · `agent-design-guide.md:79` · `create-agent/SKILL.md:25` · `create-skill/SKILL.md:27` · `sprint-contract Step 6.7 (a)` · `V6 범위` | 고치지 않음 — Phase 4 넘김대로 다음 사이클(근거 재조회 · 새 절차) |
| F1H-41 | phase4 · 8 · 9 · 11 notes | `/sprint` Step 3 판정 표 · 재검증 블록의 폐기 결정 자리 | 고치지 않음 — 다음 사이클 Phase 4 (새 규칙 · F20 결정 뒤) |
| F1H-42 | phase5 notes | flutter changelog · research-log | 다른 계약 — `kaizen-0924-final` |
| F1H-43 | phase6 · 10 notes | 세 화면 규약의 공통 규칙 원문 절을 skill 가이드에 | 고치지 않음 — 새 절 신설, 다음 사이클 Phase 1 |
| F1H-44 | phase6 · 7 · 9 notes | design · backend · rust-kaizen Gotcha 6 형제 표에 새 행 | 고치지 않음 — 새 대조 항목이라 다음 사이클(notes 배정 그대로) |
| F1H-45 | phase7 · 8 notes | `.harness/stale-values.yaml` 새 항목 · allow | 다른 계약 — `kaizen-0924-final` (`.harness/`) |
| F1H-46 | phase8 notes | research-templates Phase 8 「3 signals stable」 | 조건 SK-02 |
| F1H-47 | phase8 · 9 · 11 notes | 평가 가이드 미검증 규약 새 판 · 킷 reviewer 일곱 사본 | 고치지 않음 — 판정 문턱을 바꾸는 별도 관심사, 다음 사이클 Phase 3 |
| F1H-48 | phase8 notes | infra-kaizen Gotcha 8 복제 문구 | 고치지 않음 — F1H-47 결정 뒤 |
| F1H-49 | phase8 notes | infra-kaizen Gotcha 6 「미검증 3항」 | 조건 SK-03 |
| F1H-50 | phase9 notes | rust-kaizen Gotcha 9 AR-02 가 자기 파일을 잡음 | 조건 SK-03 |
| F1H-51 | phase10 notes | CI react 시험 | 조건 AR-02 |
| F1H-52 | phase10 notes | react-kaizen Step 6 계약 경로 · git 쓰기 금지 | 조건 SK-04 — backend · design · infra-kaizen Gotcha 7 의 같은 규칙도 |
| F1H-53 | phase10 notes | 옛 값 검사에 `react-kit/references` 없음 | 조건 ER-07 |
| F1H-54 | phase5 ~ 17 notes | 킷 폴더 · 킷 원본 문서 안의 넘김과 킷 다음 사이클 메모 전부(flutter-preflight · go_router · design:P2 · UNVERIFIED_ENV · OpenAPI 3.1 · Flux · g6-build-audit · planning-reviewer · reflect README 버전 줄 · bambu 현행화 · tone · api · howto 메모 등) | 다른 계약 — `kaizen-0924-f1-kit-followups` 가 이번에 고치는 것 말고는 그 킷의 다음 사이클. 이 계약 범위 밖 |
| F1H-55 | phase12 notes | 평가자 Step 3.4 · 평가 가이드 `:643-652` | 조건 ER-03 |
| F1H-56 | phase12 notes | 킷 넷 `hooks.json` 따옴표 · V8 검사 | 고치지 않음 — 킷 넷을 함께 고쳐야 하는데 킷 폴더는 이 계약 범위 밖이고 한 커밋에 킷 하나 규칙과 부딪힌다. 다음 사이클 Phase 4 |
| F1H-57 | phase12 notes | CI 세 줄 | 조건 AR-02 |
| F1H-58 | phase12 notes | `sync-evals.py` `TARGET_KITS` 에 reflect-kit 없음 | 고치지 않음 — reflect-kit 에 `evals.json` 이 없어 결과가 안 바뀐다 |
| F1H-59 | phase13 notes | bambu-kaizen Step 2 점검 줄 · 회귀 음성 대조 줄 | 고치지 않음 — 새 절차 추가라 Final 에서 넣지 않는다. 다음 사이클 Phase 13 |
| F1H-60 | phase13 notes | bambu-research 문구 | 고치지 않음 — 세 Final 계약 어느 범위에도 없다(`.claude/skills/*-research/`) |
| F1H-61 | phase14 notes | CI 두 단계 | 조건 AR-02 |
| F1H-62 | phase14 notes | onboarding-kaizen Phase 4 검증 줄 | 조건 SK-03 |
| F1H-63 | phase14 notes | 드리프트 검사 onboarding 매핑 | 조건 AR-01 |
| F1H-64 | phase14 notes §미반영 마지막 줄 | 오케스트레이터 Step 14 `onboarding-kit/references/` | 조건 AR-03 · SK-02 |
| F1H-65 | phase14 notes 메모 | `run-evals.py` `ALL_KITS` 에 onboarding 없음 | 고치지 않음 — 그 킷 평가 파일은 `skills/setup-guide/evals/` 에 있어 `<킷>/evals/evals.json` 규칙에 안 맞고 형식도 게이트 평가다. 대신 AR-02 가 CI 에 러너를 넣는다 |
| F1H-66 | phase14 notes 메모 | `sync-docs.py` `MARKER_RE` 가 onboarding · planning README 표지를 못 읽음 | 고치지 않음 — 고치면 킷 README 둘이 다시 만들어져 킷 범위다. 다음 사이클 |
| F1H-67 | phase14 · 16 notes | 예제 원본 `docs/onboarding-kit/examples/` · `docs/superpowers/specs/2026-09-02-api-kit-design.md:249` | 예제는 다른 계약 — `kaizen-0924-f1-kit-followups`. 설계 문서 `:249` 는 고치지 않음 — 세 Final 계약 어느 범위에도 없다 |
| F1H-68 | phase15 notes | tone-kaizen 템플릿 「8종」 | 조건 SK-03 |
| F1H-69 | phase15 notes | research-templates `:230` 출처 이름 | 조건 SK-02 |
| F1H-70 | phase16 notes | 오케스트레이터 `:566` 불변식 이유 | 조건 SK-01 |
| F1H-71 | phase16 notes | 드리프트 검사 `docs/api` 매핑 | 조건 AR-01 |
| F1H-72 | phase17 notes | CI howto 단계 | 조건 AR-02 |
| F1H-73 | phase17 notes | howto-kaizen `:26` | 조건 SK-03 |
| F1H-74 | phase1 ~ 17 notes | 킷 `plugin.json` 버전 · marketplace | 다른 계약 — `kaizen-0924-final` (`release-plan.md`) |
| F1H-75 | 편집 전 감사 (입력 밖) | `check_bare_fence` 가 `"0 bare"` 부분 글자로 늘 PASS | 조건 ER-08 (V 줄 형식의 받는 쪽) |
| F1H-76 | 편집 전 감사 (입력 밖) | research-templates 에 Phase 17 표 없음 | 고치지 않음 — 출처 선정은 새 내용, 다음 사이클. SK-01 이 「Phase 17 표는 아직 없다」 로 적는다 |
| F1H-77 | 편집 전 감사 (입력 밖) | 오케스트레이터 · 수집기의 Phase 별 참조 매핑 표가 13 · 14 까지 | 고치지 않음 — Phase 마다 참조 절을 정하는 새 내용, 다음 사이클 |
| F1H-78 | 편집 전 감사 (입력 밖) | tone-kaizen `docs/tone/*.md` 「8종」 (`:35` · `:100`) — 실제 `.md` 11 개 | 고치지 않음 — 셈 기준(리서치 문서만인지)이 불분명, 다음 사이클 tone-kaizen |
| F1H-79 | 편집 전 감사 (입력 밖) | backend-kit 세 줄이 OpenAPI 3.1.1 명세 링크를 인용해 옛 값 검사에 걸림 | 고치지 않음 — 예외 등록부 `.harness/stale-values.yaml` 은 `kaizen-0924-final` 범위. ER-07 이 backend-kit 을 빼고 이유를 출력한다. 다음 사이클: allow 세 줄을 넣고 제외를 푼다 |
| F1H-80 | phase1 · 3 notes §다음 사이클 메모 | 근거 재조회 항목 · 오류 문구 짝 · `omitClaudeMd` · 문장 삭제 사본 검토 절차 · 평가 가이드 「12 개 이상의 편향」 | 고치지 않음 — 근거 파일 재조회가 먼저라 다음 사이클 Phase 1 · 3. 단 agent 가이드 `:59` 배치 우선순위는 근거 파일 `phase4.md:149` 가 있어 이번에 고친다(F1H-89) |
| F1H-81 | phase12 notes §다음 사이클 메모 | `scripts/collect-kaizen-data.py:421` 워크트리 묶기 규칙과 reflect-kit `facets_unmatched` 규칙 | 고치지 않음 — 지금 facets 18 개는 경로가 전부 살아 있어 영향 0, 지워진 워크트리 세션이 생기면 맞춘다 |
| F1H-82 | phase14 · 17 notes 메모 · phase17-notes `:138` (러너 시간 3.4 초 → 8 ~ 9 초, CI 에 넣은 뒤 시간 상한을 조건으로 둘지) | CI 에 넣은 러너의 첫 우분투 실행 확인 · 시간 상한 | 고치지 않음 — 이 계약이 넣은 단계의 첫 CI 결과는 PR 뒤에만 볼 수 있다. 다음 사이클 첫 확인 항목 |
| F1H-83 | Codex r1 1 (중간) | 경로 지정 커밋이 이름 바꾸기를 삭제로 셈 · README `:52` 와 어긋남 · 경로 지정 이름 바꾸기 시험 없음 | 조건 ER-01 — F1H-25 와 같은 결함이라 한 조건. 다시 확인: 시작 커밋 판 `ren2.sh` 에서 N1 · N2 · N5 가 `hook_rc=2 git_dels=0 DISAGREE` (2026-09-25 재실행) |
| F1H-84 | Codex r1 2 (중간) | `silent-check` 픽스처와 `assertions.json` 을 읽는 실행기가 없음 | 고치지 않음 — F1H-14 와 같은 것. 다시 확인: 소비자 grep 결과는 설계 문서 둘과 contract-kaizen 픽스처만 읽는 `aggregation-test.sh` 뿐이고, `run-evals.py:115-119` 는 `behavior` · `output` 두 종류의 구조만 본다. 같은 빈틈이 전부터 있던 픽스처 넷(`l3-miss` 등)에도 있다. 실행기는 새 기능이라 오케스트레이터 Gotcha(`SKILL.md:47` 「Final에서 새 기능을 추가하지 마라」)와 부딪힌다 — 다음 사이클 Phase 3 · 4 첫 항목 |
| F1H-85 | Codex r1 3 (중간) | Diff-Scope 표준형이 커밋 전 두 상태를 허용하면서 상한 ref 를 늘 요구 — 커밋 전 조건이 상한이 없다고 REJECT 될 수 있다 | 조건 SK-05 (마) — 다시 확인: 스키마 `:571` 세 상태 · `:573` 「5 요소를 모두 채운다」, 계약 가이드 `:695` · `:710-712`, 평가자 `:592`, 평가 가이드 `:789-790`, sprint-contract `:56`. 같은 규칙이 박힌 자리를 `grep -n '5 요소\|상한 ref'` 로 모두 찾아 정의 줄 다섯을 고친다(Counterpart 표) |
| F1H-86 | Codex r1 4 (중간) | 스키마 `:670` 은 서명 줄을 끝 문단에서만 인정한다고 적지만 `mine` · `unsigned_on` 은 메시지 어느 줄이든 찾는다 | 조건 ER-06 (d) — 다시 확인: 시작 커밋 판 `sigline.sh` 가 bash · zsh 둘 다 `mine_middle=1`(가운데 문단 서명도 잡힘). 설명을 동작에 맞춘다 |
| F1H-87 | Codex r1 5 (중간) | 평가 가이드 `:757` 의 `CONTRACT_ROOT` 정의가 스키마 `:29`(먼저 만나는 `.harness/`)와 반대인 옛 `project.yaml` 기준 | 조건 SK-05 (바) — 다시 확인: 같은 옛 정의는 `harness/` · `.claude/skills/` 에서 이 한 줄뿐(grep) |
| F1H-88 | Codex r1 6 (낮음) | create-agent 가 플러그인에서 무시되는 `initialPrompt` 를 빠뜨림 | 조건 SK-05 (사) — 다시 확인: 근거 파일 `phase1.md:87` · `phase4.md:148` 에 같은 내용, 같은 변경의 agent 가이드 `:99` 는 넷을 적는다. Codex 가 짚지 않은 셋째 자리 agent 가이드 `:549` 도 셋만 적어 함께 고친다 |
| F1H-89 | Codex r1 7 (낮음) | agent 가이드 배치 우선순위 표에 managed settings 가 없어 번호가 한 단계씩 틀림 | 조건 SK-05 (아) — 다시 확인: 근거 파일 `phase4.md:149` 「managed settings가 1위, `--agents` 2위, project 3위, user 4위, plugin 5위」. phase1-notes §다음 사이클 메모가 「근거 파일 phase4.md 에만 있어 미반영」 으로 넘긴 `:59` 항목이다 |
| F1H-90 | REVIEW 검토 C2 (입력 밖) | 오케스트레이터 F2 매핑 표에 reflect · bambu · onboarding · howto 행이 없고 planning 행이 없는 `planning-kit/references/` 를 적는다 — Final 러닝북이 문서 사이트 재생성에 이 표를 쓴다 | 조건 AR-01 (b) |
| F1H-91 | REVIEW 검토 (입력 밖) | `.claude/skills/docs-site/SKILL.md:47-55` 매핑 표가 harness · flutter · design · backend · infra · tone · process 일곱 줄뿐이다 | 고치지 않음 — `.claude/skills/docs-site/` 는 세 Final 계약 어느 범위에도 없다. 다음 사이클 |
| F1H-92 | REVIEW 검토 (입력 밖) | 오케스트레이터 F4 research-log 목록(`:731-738`)과 체크리스트 「per-kit research-log 6개 파일」(`:765`)에 design · tone · api 연구 기록이 없다 | 고치지 않음 — 목록을 「`docs/*/research-log.md` 가 있는 킷 전부」 같은 규칙으로 바꾸려면 「파일이 없으면 새로 만든다」 조문(`:56`)과 함께 정해야 하는 새 내용이다. 이번 Final 은 러닝북이 `docs/*/research-log.md` 로 대신 정했다. 다음 사이클 |
| F1H-93 | REVIEW 검토 C1 (받는 쪽 대조) | `harness/docs/guides/plugin-validation-guide.md` §출력 포맷 예시가 실패 V 줄을 판정 글자 없이 적는다 | 조건 ER-08 (c) |
| F1H-94 | xdiag P10 (2) DG-05 (b) · P13 (2) AP-03 | validate-plugin V10 이 `docs/<킷>/` 원본을, V6 가 `skills/*/references/` 를 읽지 않는다 | 고치지 않음 — F1H-40 의 `V6 범위` 결정(다음 사이클 Phase 4)과 함께 정한다 |
| F1H-95 | xdiag P5 · P6 (2) 2 · 3 · P7 · P8 (2) 1 · 2 · P9 · P10 · P11 · P12 · P13 · P14 · P16 의 (2) 절 | Phase 계약 측정의 구멍(서명 없는 커밋 · 더한 줄만 센 편집기 경고 · 좁은 정규식 · 구조상 늘 0 인 값 등) | 다른 계약 — `kaizen-0924-final` (계약 · 평가자 피드백 교차 진단 기록) |

## 회귀 게이트 — 측정 공통 정의 · 도우미 · 봉인 전 실측

모든 조건의 측정은 공통 정의 블록(`common.sh`)을 먼저 읽은 **bash** 셸에서 돈다 — 블록과 측정을 한 `bash -c` 안에 넣거나 블록을 파일로 저장해 `. 파일` 뒤에 잇는다.
`END_UNRESOLVED` 가 찍히면 셸이 종료 코드 2 로 끝난다. HEAD 로 바꿔 재지 않는다.

도우미 준비 — 이 절의 bash · python 코드 블록은 각 블록 첫 `#` 주석 줄(셔뱅 다음)에 적힌 이름 그대로 한 폴더에 저장하고, 그 폴더를 공통 정의를 읽기 전에 `K` 에 넣는다. 떼는 명령:

```bash
# 이 계약에서 도우미 블록을 떼어 $K 에 저장한다 — 블록 첫 주석 줄의 이름(셔뱅 다음 줄)이 파일 이름이다
K=${K:?도우미 폴더}; mkdir -p "$K"
python3 - .harness/sprint-contract-kaizen-0924-f1-harness-followups.md "$K" <<'PY'
import re, sys, pathlib
src = open(sys.argv[1], encoding="utf-8").read(); K = pathlib.Path(sys.argv[2])
for body in re.findall(r"^```(?:bash|python)\n(.*?)^```$", src, re.S | re.M):
    lines = body.splitlines(); i = 1 if lines and lines[0].startswith("#!") else 0
    m = re.match(r"# ([\w.-]+\.(?:sh|py)) ", lines[i]) if len(lines) > i else None
    if m and m.group(1) != "extract.sh":
        (K / m.group(1)).write_text(body, encoding="utf-8")
PY
# align.sh 는 봉인된 Phase 4 계약의 블록을 그대로 쓴다 (경로 지정 커밋 열한 경우의 알려진 답)
awk '/^```bash$/{f=1; buf=""; next} f && /^```$/{ if (buf ~ /^#!\/usr\/bin\/env bash\n# align\.sh/) { printf "%s", buf; exit } f=0; next } f { buf = buf $0 "\n" }' \
  .harness/sprint-contract-kaizen-0924-p04-harness.md >"$K/align.sh"
# mdcmp.sh 옆에 markdownlint 와 설정 — 편집기 확장과 같은 조건(MD013 끔)
ln -sfn /private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/de8c7935-a5b6-4df5-9106-fafa73c288a0/scratchpad/p1build/node_modules "$K/node_modules"
printf '{ "config": { "MD013": false } }\n' >"$K/cfg.markdownlint-cli2.jsonc"
```

준비 단계 실측(2026-09-25): `$K/node_modules/.bin/markdownlint-cli2 --version` 첫 줄 `markdownlint-cli2 v0.23.2 (markdownlint v0.41.1)` — 없으면 그 폴더에서 `npm install --no-save markdownlint-cli2@0.23.2` 부터 ·
`command -v shellcheck` → `/opt/homebrew/bin/shellcheck` (0.11.0) · `command -v actionlint` → `/opt/homebrew/bin/actionlint` (1.7.12) · `command -v jq` → `/usr/bin/jq` ·
`command -v zsh` → `/bin/zsh` (5.9) · `command -v dash` → `/bin/dash` · `/bin/bash --version` 3.2.57 · `git --version` 2.53.0 · `python3 -c 'import yaml'` 성공.
도우미 다섯 개(`ren2.sh` · `ident.sh` · `renlist.sh` · `align.sh` · `sigline.sh`)는 `GIT_CONFIG_GLOBAL=/dev/null` 인 임시 저장소를 만들어 쓰고 끝나면 지운다. 작업 폴더는 건드리지 않는다.

측정이 기대는 공통 정의 이름: `B` · `END` · `SIG` · `CF` · `AM` · `NOTES` · `FILES` · `MDS` · `SHS` · `PYS` · `MYHARNESS` · `T/B` · `T/E` · `my` · `unsigned_on` · `verify_seal` · `sect` · `logblk` · `added` · `newurls` · `evurls` · `K02`.
셸 함수에 기대는 측정 앞에는 `type <함수> >/dev/null || exit 2` 를 둔다 — 정의가 없으면 조용히 0 이 나온다.

측정 공통 정의 — 두 판을 풀고 이 계약 커밋 · 봉인 · 절 자르기 도우미를 정의한다:

```bash
# common.sh — 측정 공통 정의. bash 로 실행한다 (zsh 는 배열 첨자가 1 부터이고 따옴표 없는 변수를 쪼개지 않는다)
export LC_ALL=C.UTF-8   # 번역투 정규식이 글자 단위로 돌아야 한다 — C 로케일이면 덜 잡힌다
cd /Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/kaizen-0924 || exit 2
B=5b4fd72d5587c937c1875ddb62872f32ae087dcf                  # 이 계약 시작 HEAD
SIG='Kaizen-Phase: kaizen-0924-f1-harness-followups'
CF=.harness/sprint-contract-kaizen-0924-f1-harness-followups.md
AM=.harness/sprint-amendments-kaizen-0924-f1-harness-followups.md
NOTES=.harness/.meta/kaizen-0924/f1-harness-followups-notes.md
REVIEW=.harness/.meta/kaizen-0924/f1-harness-followups-review.md
FB=.harness/sprint-feedback-kaizen-0924-f1-harness-followups.md
END=$( [ -f "$AM" ] && sed -n 's/^end_sha:[[:space:]]*//p' "$AM" | tail -1 )
if [ -z "$END" ] || ! git rev-parse -q --verify "$END^{commit}" >/dev/null; then
  echo "END_UNRESOLVED — 측정을 멈추고 BUILD 에 묻는다. HEAD 로 바꿔 재지 않는다"; exit 2
fi
: "${K:?도우미 폴더를 K 에 넣는다}"
MDS=(harness/README.md harness/agents/qa-evaluator.md harness/docs/guides/qa-evaluation-guide.md
  harness/docs/guides/skill-design-guide.md harness/docs/guides/agent-design-guide.md harness/references/contract-schema.md
  .claude/skills/kaizen-orchestrator/SKILL.md .claude/skills/kaizen-orchestrator/references/phase-dependencies.md
  .claude/skills/kaizen-orchestrator/references/phase-research-templates.md
  .claude/skills/tone-kaizen/SKILL.md .claude/skills/howto-kaizen/SKILL.md .claude/skills/onboarding-kaizen/SKILL.md
  .claude/skills/rust-kaizen/SKILL.md .claude/skills/infra-kaizen/SKILL.md .claude/skills/backend-kaizen/SKILL.md
  .claude/skills/design-kaizen/SKILL.md .claude/skills/react-kaizen/SKILL.md
  harness/docs/guides/contract-design-guide.md harness/skills/sprint-contract/SKILL.md harness/skills/create-agent/SKILL.md
  harness/docs/guides/plugin-validation-guide.md)
SHS=(harness/scripts/commit-guard.sh harness/evals/hooks/commit-guard-test.sh harness/scripts/save-feedback.sh
  harness/evals/kaizen/feedback-system/save-test.sh)
PYS=(scripts/check-stale-values.py scripts/validate-plugin.py scripts/validate-post-kaizen.py scripts/detect-docs-drift.py
  scripts/sync-orchestrator.py)
FILES=("${MDS[@]}" "${SHS[@]}" "${PYS[@]}" .github/workflows/ci.yml)
MYHARNESS=("$CF" "$AM" "$NOTES" "$REVIEW" "$FB")
T=$(mktemp -d "${TMPDIR:-/tmp}/f1h.XXXXXX") || exit 2
trap 'rm -rf "$T"' EXIT
mkdir -p "$T/B" "$T/E"
# 두 판을 풀어 두고 거기서 잰다 — 작업 폴더에 남은 다른 계약의 미커밋 변경이 끼지 않는다
git archive "$B" | tar -x -C "$T/B" || exit 2
git archive "$END" | tar -x -C "$T/E" || exit 2
mine() { git log --format= --name-only "${1}..${2}" --grep="^${3}\$" | grep . | LC_ALL=C sort -u; }
unsigned_on() { _b=${1}; _u=${2}; _s=${3}; shift 3
  git log --format=%H "${_b}..${_u}" -- "$@" | while read -r _c; do git log -1 --format=%B "$_c" | grep -qxF "$_s" || echo "$_c"; done; }
my() { mine "$B" "$END" "$SIG"; }
fm_get() { awk -v k="^$2:[[:space:]]*" 'NR==1 && /^---[[:space:]]*$/ { fm=1; next } fm && /^---[[:space:]]*$/ { exit } fm && $0 ~ k { sub(k, "", $0); print; exit }' "$1" | sed -e "s/[[:space:]]*$//" -e "s/^['\"]//" -e "s/['\"]\$//"; }
sha256_16() { if command -v sha256sum >/dev/null 2>&1; then sha256sum; elif command -v shasum >/dev/null 2>&1; then shasum -a 256; else python3 -c 'import hashlib,sys; print(hashlib.sha256(sys.stdin.buffer.read()).hexdigest())'; fi | cut -c1-16; }
contract_digest() { grep -E '^- \[[ x]\] [A-Z]{2,}-[0-9]{2}' "$1" | sed -E 's/^- \[[ x]\]/- [ ]/' | sha256_16; }
verify_seal() { rec=$(fm_get "$1" conditions_digest); rec=${rec#sha256:}; if [ -z "$rec" ]; then echo "SEAL_ABSENT $1"; return 0; fi
  act=$(contract_digest "$1"); if [ "$rec" = "$act" ]; then echo "SEAL_OK $1"; else echo "SEAL_BROKEN $1 recorded=$rec actual=$act"; fi; }
# sect <파일> <제목 앞부분> — 그 제목부터 같은 깊이 이하의 다음 제목 전까지. 코드 펜스 안의 `#` 줄은 제목으로 보지 않는다
sect() { awk -v h="$2" '
  /^[[:space:]]*(```|~~~)/ { fence = !fence }
  !f && !fence && index($0, h) == 1 { f = 1; lvl = match($0, /[^#]/) - 1; print; next }
  f && !fence && /^#+ / { l = match($0, /[^#]/) - 1; if (l <= lvl) exit }
  f' "$1"; }
# logblk <md 파일> — 사용자 교정 로그 폴더를 찾는 bash 블록(LOGS_ROOT= 가 든 첫 블록)을 뗀다
logblk() { awk '/^```bash$/{f=1; buf=""; next} f && /^```$/{ if (buf ~ /LOGS_ROOT=/) { printf "%s", buf; exit } f=0; next } f { buf = buf $0 "\n" }' "$1"; }
added() { for f in "${FILES[@]}"; do git diff --no-index -U0 "$T/B/$f" "$T/E/$f"; done | grep '^+' | grep -v '^+++'; }
url() { grep -oE 'https?://[^ )>"`]+' | sed -E 's/[.,;:]+$//' | LC_ALL=C sort -u; }
newurls() { for f in "${FILES[@]}"; do LC_ALL=C comm -13 <(url <"$T/B/$f") <(url <"$T/E/$f"); done | LC_ALL=C sort -u; }
evurls() { cat "$T/B"/.harness/.meta/evidence/phase*.md | url; }
K02='(을|를) ?(처리|관리)(합니다|한다)|에 대해서?|하도록 (합니다|한다)|에 의(해|하여)|되어 있(는 경우|을 때)|(표시|적용|호출|생성|반환)(됩니다|된다)'
```

문장 글자 표 — 조건별 ID 접두로 새 글자 · 옛 글자 줄 수를 기대값과 맞댄다:

```python
#!/usr/bin/env python3
# toks.py <판 폴더> [ID 접두] — 표의 줄마다 그 판 파일에서 글자가 든 줄 수를 세어 기대값과 맞대 본다.
# 파일이 없으면 MISSING 으로 NG 다 (0 으로 세지 않는다). 끝줄 rows=<센 줄 수> ng=<어긋난 수>.
import sys
from pathlib import Path
F = {
    "OS": ".claude/skills/kaizen-orchestrator/SKILL.md",
    "PD": ".claude/skills/kaizen-orchestrator/references/phase-dependencies.md",
    "RT": ".claude/skills/kaizen-orchestrator/references/phase-research-templates.md",
    "TK": ".claude/skills/tone-kaizen/SKILL.md",
    "HK": ".claude/skills/howto-kaizen/SKILL.md",
    "OK": ".claude/skills/onboarding-kaizen/SKILL.md",
    "RK": ".claude/skills/rust-kaizen/SKILL.md",
    "IK": ".claude/skills/infra-kaizen/SKILL.md",
    "BK": ".claude/skills/backend-kaizen/SKILL.md",
    "DK": ".claude/skills/design-kaizen/SKILL.md",
    "RC": ".claude/skills/react-kaizen/SKILL.md",
    "SDG": "harness/docs/guides/skill-design-guide.md",
    "ADG": "harness/docs/guides/agent-design-guide.md",
    "QEG": "harness/docs/guides/qa-evaluation-guide.md",
    "QAE": "harness/agents/qa-evaluator.md",
    "CS": "harness/references/contract-schema.md",
    "RM": "harness/README.md",
    "CSV": "scripts/check-stale-values.py",
    "CDG": "harness/docs/guides/contract-design-guide.md",
    "SCK": "harness/skills/sprint-contract/SKILL.md",
    "CA": "harness/skills/create-agent/SKILL.md",
}
ROWS = [
    ("SK01-O1", "OS", r"""phase10|phase11|final]""", 0),
    ("SK01-O2", "OS", r"""Phase 1~14""", 0),
    ("SK01-O3", "OS", r"""→16→Final""", 0),
    ("SK01-O4", "OS", r"""Phase 1~16 완료 전제""", 0),
    ("SK01-O5", "OS", r"""Phase 1~16 전체 변경사항""", 0),
    ("SK01-O6", "OS", r"""`phase_1` ~ `phase_12`""", 0),
    ("SK01-O7", "OS", r"""react-kit → planning-kit 순서로""", 0),
    ("SK01-O8", "OS", r"""Phase 2~16 변경에""", 0),
    ("SK01-O9", "OS", r"""Phase 5~16 (""", 0),
    ("SK01-O10", "OS", r"""경로 간 불변식(`$.meta.total >= len($.data)`)은 Hurl assert 로 표현할 수 없다""", 0),
    ("SK01-N1", "OS", r"""Phase 17: Howto-kit 카이젠 (howto-kaizen)""", 1),
    ("SK01-N2", "OS", r"""17. Howto-kit 카이젠""", 1),
    ("SK01-N3", "OS", r"""`/kaizen-orchestrator phase17`""", 1),
    ("SK01-N4", "OS", r"""phase16|phase17|final]""", 1),
    ("SK01-N5", "OS", r"""→17→Final""", 1),
    ("SK01-N6", "OS", r"""Phase 1~17 완료 전제""", 1),
    ("SK01-N7", "OS", r"""Phase 1~17 전체 변경사항""", 1),
    ("SK01-N8", "OS", r"""`phase_1` ~ `phase_17`""", 1),
    ("SK01-N9", "OS", r"""api-kit → howto-kit 순서로""", 2),
    ("SK01-N10", "OS", r"""Phase 2~17 변경에 반영되었는가""", 1),
    ("SK01-N11", "OS", r"""Phase 5~17 (""", 1),
    ("SK01-N12", "OS", r"""howto-kit 3 스킬 + howto-reviewer 에이전트""", 1),
    ("SK01-N13", "OS", r"""동시에 도는 킷 Phase 는 3 개까지""", 1),
    ("SK01-N14", "OS", r"""§여러 주체가 한 가지에 커밋할 때""", 1),
    ("SK01-N15", "OS", r"""경로가 없으면 종료 코드 3 이라 판정 불가를 가를 곳이 후처리뿐""", 1),
    ("SK01-N16", "OS", r"""Phase 1~16 각 의무 리서치 소스 테이블""", 1),
    ("SK01-N17", "OS", r"""Phase 17 표는 아직 없다""", 1),
    ("SK01-N18", "OS", r"""모든 Phase 범위 밖""", 1),
    ("SK01-N19", "OS", r"""모든 Phase 서브에이전트가 공유할""", 1),
    ("SK01-N20", "OS", r"""모든 Phase 간 scope 격리가 유지되었다""", 1),
    ("SK02-O1", "PD", r"""Phase 7~16""", 0),
    ("SK02-O2", "PD", r"""onboarding-kit/references/""", 0),
    ("SK02-N1", "PD", r"""Phase 17: Howto-kit 카이젠 (howto-kaizen)""", 1),
    ("SK02-N2", "PD", r"""howto-kit/agents/howto-reviewer.md""", 1),
    ("SK02-N3", "PD", r"""Phase 16 스킵 → Phase 17 진행에 영향 없음 (독립 스택)""", 1),
    ("SK02-N4", "PD", r"""| docs/howto/ | howto-kit 전 스킬 |""", 1),
    ("SK02-N5", "PD", r"""onboarding-kit/skills/setup-guide/references/""", 1),
    ("SK02-O6", "PD", r"""planning-kit/references/""", 0),
    ("SK02-O7", "PD", r"""|planning|tone|api}/""", 0),
    ("SK02-N9", "PD", r"""|planning|tone|api|howto}/""", 1),
    ("SK02-O3", "RT", r"""500 라인 상한""", 0),
    ("SK02-O4", "RT", r"""| 공식 | 3 signals stable |""", 0),
    ("SK02-O5", "RT", r"""[국립국어원 공공언어](""", 0),
    ("SK02-N6", "RT", r"""500 줄 미만 권고""", 1),
    ("SK02-N7", "RT", r"""signal 마다 안정 상태가 다르다""", 1),
    ("SK02-N8", "RT", r"""[국립국어원 보도자료 작성 길잡이](https://korean.go.kr/front/etcData/etcDataView.do?etc_seq=663)""", 1),
    ("SK03-O1", "TK", r"""`tone-kit/templates/*.md` 8종""", 0),
    ("SK03-N1", "TK", r"""`tone-kit/templates/*.md` 6종""", 1),
    ("SK03-O2", "HK", r"""eval runner 가 두 셸 출력 동일성까지 검사한다""", 0),
    ("SK03-N2", "HK", r"""eval runner 가 세 셸(zsh · bash · sh) 출력 동일성과 게이트 블록 네 경우까지 검사한다""", 1),
    ("SK03-N3", "OK", r"""`sh onboarding-kit/skills/setup-guide/evals/run-gate-evals.sh`""", 1),
    ("SK03-O4", "RK", r"""`grep -rn "17개 리서치\|17 리서치\|docs/rust/ 리서치 문서 17" .`""", 0),
    ("SK03-N4", "RK", r"""`grep -rn "17개 리서치\|17 리서치\|docs/rust/ 리서치 문서 17" rust-kit docs/rust`""", 1),
    ("SK03-O5", "IK", r"""미검증 3항""", 0),
    ("SK04-O1", "RC", r"""병렬 실행 중 git 쓰기 금지""", 0),
    ("SK04-N1", "BK", r"""`.harness/sprint-contract-<slug>.md`""", 1),
    ("SK04-N2", "DK", r"""`.harness/sprint-contract-<slug>.md`""", 1),
    ("SK04-N3", "IK", r"""`.harness/sprint-contract-<slug>.md`""", 1),
    ("SK04-N4", "RC", r"""`.harness/sprint-contract-<slug>.md`""", 1),
    ("SK04-N5", "RC", r"""git add <내 경로> && git commit -o <내 경로>""", 1),
    ("SK05-O1", "SDG", r"""검증을 못 한 경우 우회가 정말 없으면 칸을 비우지 말고 `없음 — 이유` 를 적는다""", 0),
    ("SK05-O2", "ADG", r"""정말 없으면 `없음 — 이유`""", 0),
    ("SK05-N1", "SDG", r"""`없음 — 계약에 대체 검증 단계가 없음`""", 1),
    ("SK05-N2", "ADG", r"""`없음 — 계약에 대체 검증 단계가 없음`""", 1),
    ("SK05-N3", "SDG", r"""계약에 대체 검증 단계가 있는데 건너뛰었으면 `없음` 으로 적어도 `INVALID` 다""", 1),
    ("SK05-N4", "ADG", r"""계약에 대체 검증 단계가 있는데 건너뛰었으면 `없음` 으로 적어도 `INVALID` 다""", 1),
    ("SK05-N5", "ADG", r"""ultracode 에서는 동시 실행 20 개 상한도 적용되지 않는다""", 1),
    ("SK05-N6", "ADG", r"""ultracode 는 동시 상한 없음""", 1),
    ("SK05-O3", "SDG", r"""Item 16 은 Item 12 처럼 생성 측 전용이라 평가자 가이드에 대응 절을 두지 않고 계약 조건으로 흡수한다""", 0),
    ("SK05-O4", "SDG", r"""— (생성 측 전용 · 평가자는 계약 조건으로 받는다)""", 0),
    ("SK05-N7", "SDG", r"""평가자 쪽 짝은 `qa-evaluation-guide.md` §산출물이 검사일 때 ⑤""", 2),
    ("SK05-N8", "QEG", r"""**§산출물이 검사일 때 ⑤ 효과 증명""", 1),
    ("SK05-O5", "QAE", r"""위 (c) 의 대체 측정은""", 0),
    ("SK05-N9", "QAE", r"""위 「0 이 기대값인 측정」 문단 (c) 의 대체 측정은""", 1),
    ("SK05-N10", "CS", r"""상한 ref 는 커밋 구간을 재는 조건에만 요구한다""", 1),
    ("SK05-N11", "CDG", r"""상한 ref 는 커밋 구간을 재는 조건에만 요구한다""", 1),
    ("SK05-N12", "QAE", r"""상한 ref 는 커밋 구간을 재는 조건에만 요구한다""", 1),
    ("SK05-N13", "QEG", r"""상한 ref 는 커밋 구간을 재는 조건에만 요구한다""", 1),
    ("SK05-N14", "SCK", r"""상한 ref 는 커밋 구간을 재는 조건에만 요구한다""", 1),
    ("SK05-O7", "QEG", r"""`.harness/project.yaml` 을 가진 가장 가까운 조상의 절대경로이며""", 0),
    ("SK05-N15", "QEG", r"""처음 만나는 `.harness/` 디렉토리를 가진 조상의 절대경로이며""", 1),
    ("SK05-O8", "CA", r"""hooks, mcpServers, permissionMode 를 지원하지 않는다""", 0),
    ("SK05-N16", "CA", r"""hooks, mcpServers, permissionMode, initialPrompt 를 지원하지 않는다""", 1),
    ("SK05-O9", "CA", r"""hooks/mcpServers/permissionMode 미사용 확인""", 0),
    ("SK05-N17", "CA", r"""hooks/mcpServers/permissionMode/initialPrompt 미사용 확인""", 1),
    ("SK05-O10", "ADG", r"""`hooks`, `mcpServers`, `permissionMode`를 지원하지 않는다""", 0),
    ("SK05-N18", "ADG", r"""`hooks`, `mcpServers`, `permissionMode`, `initialPrompt`를 지원하지 않는다""", 1),
    ("SK05-O11", "ADG", r"""| `--agents` CLI 플래그 | 현재 세션만 | 1 (최고) |""", 0),
    ("SK05-O12", "ADG", r"""| 플러그인 `agents/` | 플러그인 활성화된 곳 | 4 (최저) |""", 0),
    ("SK05-N19", "ADG", r"""| managed settings | managed settings 가 적용된 곳 | 1 (최고) |""", 1),
    ("SK05-N20", "ADG", r"""| `--agents` CLI 플래그 | 현재 세션만 | 2 |""", 1),
    ("SK05-N21", "ADG", r"""| `.claude/agents/` | 현재 프로젝트 | 3 |""", 1),
    ("SK05-N22", "ADG", r"""| `~/.claude/agents/` | 모든 프로젝트 | 4 |""", 1),
    ("SK05-N23", "ADG", r"""| 플러그인 `agents/` | 플러그인 활성화된 곳 | 5 (최저) |""", 1),
    ("ER01-N1", "RM", r"""이름 바꾸기는 여기서도 삭제로 세지 않는다""", 1),
    ("ER03-N1", "QAE", r"""워크트리에서 부르면 본 저장소 이름과 워크트리 이름을 둘 다 찾는다""", 1),
    ("ER03-N2", "QEG", r"""워크트리에서 부르면 본 저장소 이름과 워크트리 이름을 둘 다 찾는다""", 1),
    ("ER04-N1", "QAE", r"""저장한 뒤 아래 블록으로 `Evaluated:` 줄을 그 순간의 `date` 출력으로 덮어쓴다""", 1),
    ("ER05-O1", "QAE", r"""git diff --name-status --diff-filter=D <base>..<상한>""", 0),
    ("ER05-O2", "QEG", r"""git diff --name-status --diff-filter=D <base>..<상한>""", 0),
    ("ER05-N1", "QAE", r"""git diff --no-renames --name-status --diff-filter=D <base>..<상한>""", 1),
    ("ER05-N2", "QEG", r"""git diff --no-renames --name-status --diff-filter=D <base>..<상한>""", 1),
    ("ER05-N3", "QAE", r"""git status --porcelain --no-renames""", 1),
    ("ER05-N4", "QEG", r"""git status --porcelain --no-renames""", 1),
    ("ER06-O1", "CS", r"""..$(sprint_head""", 0),
    ("ER06-N1", "CS", r"""U=$(sprint_head <slug>) || exit 2""", 2),
    ("ER06-O2", "CS", r"""서명 줄은 제목이나 본문 가운데가 아니라 **끝 문단의 한 줄**로 둔다""", 0),
    ("ER06-N2", "CS", r"""`mine` · `unsigned_on` 은 메시지 어느 문단이든 서명 줄과 글자가 똑같은 줄을 찾는다 — 끝 문단인지는 보지 않는다""", 1),
    ("ER07-O1", "CSV", r"""**범위 한계 — 이 게이트는 docs-site 파이프라인 전용이다.**""", 0),
    ("AR03-O1", "OS", r"""onboarding-kit/references/""", 0),
]
root = Path(sys.argv[1]); pre = sys.argv[2] if len(sys.argv) > 2 else ""
n = ng = 0
for i, f, t, w in ROWS:
    if not i.startswith(pre):
        continue
    n += 1
    p = root / F[f]
    if not p.is_file():
        print(f"{i} MISSING {F[f]}"); ng += 1; continue
    got = sum(1 for ln in p.read_text(encoding="utf-8").splitlines() if t in ln)
    ok = got == w
    ng += not ok
    print(f"{i} {'OK' if ok else 'NG'} got={got} want={w}")
print(f"rows={n} ng={ng}")
```

오케스트레이터 자리 검사 — 의존성 그림 순서 · 공통 실행 패턴 두 줄 · AUTO 구간 차이 (SK-01 · SK-02 · AR-03):

```bash
#!/usr/bin/env bash
# orch.sh <옛 판 폴더> <새 판 폴더> — 오케스트레이터 스킬의 자리 검사: 의존성 그림 순서 · 공통 실행 패턴 절의 두 줄 · AUTO 구간 차이.
old=${1:?}; new=${2:?}
OS=.claude/skills/kaizen-orchestrator/SKILL.md; PD=.claude/skills/kaizen-orchestrator/references/phase-dependencies.md
# fence_after <파일> <제목 앞부분> — 그 제목 뒤 첫 ```text 블록
fence_after() { awk -v h="$2" 'index($0, h) == 1 { s = 1 } s && /^```text$/ { f = 1; next } f && /^```$/ { exit } f' "$1"; }
order() {  # order <블록> <앞 글자> <가운데 글자> <뒤 글자> — 세 줄이 이 순서로 한 번씩 있으면 1
  printf '%s\n' "$1" | awk -v a="$2" -v b="$3" -v c="$4" '
    index($0, a) == 1 { ia = NR; na++ } index($0, b) == 1 { ib = NR; nb++ } index($0, c) == 1 { ic = NR; nc++ }
    END { print (na == 1 && nb == 1 && nc == 1 && ia < ib && ib < ic) ? 1 : 0 }'; }
d1=$(order "$(fence_after "$new/$OS" '## Phase 의존성')" 'Phase 16: Api-kit' 'Phase 17: Howto-kit' 'Final:')
d2=$(order "$(fence_after "$new/$PD" '## ')" 'Phase 16: Api-kit' '  api-kit/skills/*/SKILL.md' 'Phase 17: Howto-kit')
sec=$(awk 'index($0, "### 각 Phase 공통 실행 패턴") == 1 { s = 1; next } s && /^### / { exit } s' "$new/$OS")
c1=$(printf '%s\n' "$sec" | grep -F '동시에 도는 킷 Phase 는 3 개까지' | grep -cF '.harness/.meta/orchestrator-audit-log.md')
c2=$(printf '%s\n' "$sec" | grep -F '§여러 주체가 한 가지에 커밋할 때' | grep -cF 'Kaizen-Phase: <슬러그>')
auto() { sed -n '/<!-- AUTO:plugin_phases:begin -->/,/<!-- AUTO:plugin_phases:end -->/p' "$1/$OS"; }
rm_n=$(diff <(auto "$old") <(auto "$new") | grep -c '^<')
add=$(diff <(auto "$old") <(auto "$new") | grep '^>' | sed 's/^> //')
printf 'diagram=%s depdoc=%s concur=%s signline=%s auto_removed=%s auto_added=%s\n' "$d1" "$d2" "$c1" "$c2" "$rm_n" "$(printf '%s\n' "$add" | grep -c .)"
printf '%s\n' "$add" | grep . | sed 's/^/  + /'
```

SK-05 (d) — Diff-Scope 상한 ref 규칙 줄 다섯의 짝:

```bash
#!/usr/bin/env bash
# upref.sh <판 폴더> — 다섯 문서에서 Diff-Scope 표준형 상한 ref 규칙이 적힌 줄(앞 글자로 찾는다)에
# 「상한 ref 는 커밋 구간을 재는 조건에만 요구한다」 가 같은 줄로 붙었는지 본다. 파일마다 0/1, 끝줄 upper=<맞은 수>/5.
r=${1:?}; t='상한 ref 는 커밋 구간을 재는 조건에만 요구한다'; n=0
pair() {  # pair <파일> <규칙 줄의 앞 글자>
  local c; c=$(grep -F -- "$2" "$r/$1" | grep -cF -- "$t")
  printf '%s %s\n' "$1" "$c"; [ "$c" = 1 ] && n=$((n + 1)); return 0; }
pair harness/references/contract-schema.md '**(5) 상한 ref**'
pair harness/docs/guides/contract-design-guide.md '| 5 | **상한 ref** —'
pair harness/agents/qa-evaluator.md '중 빠진 것을 REJECT 사유에 열거한다'
pair harness/docs/guides/qa-evaluation-guide.md '중 빠진 것을 REJECT 사유에 열거한다'
pair harness/skills/sprint-contract/SKILL.md '표준형 5 요소를 다 채워라'
printf 'upper=%s/5\n' "$n"
```

ER-01 (a) 알려진 답 — 이름 바꾸기가 섞인 커밋 다섯 경우:

```bash
#!/usr/bin/env bash
# ren2.sh <훅 경로> — 이름 바꾸기가 섞인 경로 지정 커밋 네 경우에서 훅 판정(exit 2 = 막음)과 git 이 실제로 싣는 삭제 수를 맞대 본다.
# 답은 git 이 낸다: 같은 명령을 훅 없이 커밋해 HEAD 의 삭제 줄을 이름 바꾸기 감지(-M)로 센다. 막음 ⇔ 삭제 50 개 초과여야 agree.
hook=${1:?}
export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1
export GIT_AUTHOR_NAME=t GIT_AUTHOR_EMAIL=t@e GIT_COMMITTER_NAME=t GIT_COMMITTER_EMAIL=t@e
unset HARNESS_COMMIT_GUARD GIT_INDEX_FILE GIT_DIR GIT_WORK_TREE
w=$(mktemp -d "${TMPDIR:-/tmp}/ren2.XXXXXX") || exit 2
trap 'rm -rf "$w"' EXIT
mk() { local r=$1 k; mkdir -p "$r/d1" "$r/d3"; git -C "$r" init -q -b main
  for ((k = 1; k <= 60; k++)); do
    printf 'l%d\n' "$k" >"$r/d1/$(printf 'f%03d' "$k")"; printf 'm%d\n' "$k" >"$r/d3/$(printf 'g%03d' "$k")"
  done
  git -C "$r" add -A; git -C "$r" commit -qm init; }
case_() {  # case_ <이름> <cwd> <명령>
  local name=$1 cwd=$2 cmd=$3 rc before dels a
  jq -nc --arg c "$cmd" --arg d "$cwd" '{hook_event_name:"PreToolUse",tool_name:"Bash",tool_input:{command:$c},cwd:$d}' \
    | bash "$hook" pre >/dev/null 2>&1; rc=$?
  before=$(git -C "$cwd" rev-parse HEAD)
  (cd "$cwd" && eval "$cmd") >/dev/null 2>&1
  if [ "$(git -C "$cwd" rev-parse HEAD)" = "$before" ]; then dels=0
  else dels=$(git -C "$cwd" show -M --diff-filter=D --name-only --format= HEAD | grep -c .); fi
  if { [ "$rc" = 2 ] && [ "$dels" -gt 50 ]; } || { [ "$rc" != 2 ] && [ "$dels" -le 50 ]; }; then a=agree; else a=DISAGREE; fi
  printf '%s hook_rc=%s git_dels=%s %s\n' "$name" "$rc" "$dels" "$a"
}
r=$w/N1; mk "$r"; git -C "$r" mv d1 d2; case_ N1_mv_path "$r" 'git commit -o -m x -- d1 d2'
r=$w/N2; mk "$r"; mv "$r/d1" "$r/d2"; git -C "$r" add d2; case_ N2_mvadd_path "$r" 'git commit -o -m x -- d1 d2'
r=$w/N3; mk "$r"; git -C "$r" mv d1 d2; git -C "$r" rm -rq d3; case_ N3_mv_del_path "$r" 'git commit -o -m x -- d1 d2 d3'
r=$w/N4; mk "$r"; git -C "$r" mv d1 d2; case_ N4_mv_half_path "$r" 'git commit -o -m x -- d1'
r=$w/N5; mk "$r"; mv "$r/d1" "$r/d2"; git -C "$r" add d2; case_ N5_mvadd_include "$r" 'git commit -i -m x -- d1'
```

ER-02 (a) 알려진 답 — 본 저장소 · 워크트리의 저장본 이름:

```bash
#!/usr/bin/env bash
# ident.sh <save-feedback.sh 경로> — 본 저장소와 그 워크트리에서 저장본의 project_name · project_hash 가 본 저장소 것인지 본다.
# 답은 손으로 안다: 본 저장소 폴더 이름 projmain, project_hash 는 그 폴더 절대 경로 SHA-256 앞 8 자.
sf=${1:?}
export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1
export GIT_AUTHOR_NAME=t GIT_AUTHOR_EMAIL=t@e GIT_COMMITTER_NAME=t GIT_COMMITTER_EMAIL=t@e
unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE REFLECT_KIT_LOGS_ROOT
w=$(mktemp -d "${TMPDIR:-/tmp}/ident.XXXXXX") || exit 2
w=$(cd "$w" && pwd -P); trap 'rm -rf "$w"' EXIT
export HOME=$w/home; mkdir -p "$HOME"
m=$w/projmain; mkdir -p "$m/.harness"; : >"$m/.harness/.keep"
git -C "$m" init -q -b main; git -C "$m" add -A; git -C "$m" commit -qm init
git -C "$m" worktree add -q -b wtb "$m/.claude/worktrees/wt-x" 2>/dev/null || exit 2
h8() { printf '%s' "$1" | { sha256sum 2>/dev/null || shasum -a 256; } | cut -c1-8; }
main_hash=$(h8 "$m")
for d in "$m" "$m/.claude/worktrees/wt-x"; do
  cat >"$w/draft.yaml" <<'YAML'
schema_version: 1
timestamp: "2026-09-25T10:00:00+09:00"
skill: sprint-contract
skill_version: "0.13.0"
outcome: completed
diagnosis:
  checklist:
    ambiguous_conditions: false
  cross_diagnosis_by: qa-evaluator
  cross_diagnosis_notes: "ident 시험"
  improvement_suggestions: []
YAML
  out=$(cd "$d" && bash "$sf" contract "$w/draft.yaml" 2>"$w/err") || { printf '%s SAVE_FAIL %s\n' "$(basename "$d")" "$(head -1 "$w/err")"; continue; }
  name=$(sed -n "s/^project_name:[[:space:]]*//p" "$out" | head -1 | tr -d "'\"")
  hash=$(sed -n "s/^project_hash:[[:space:]]*//p" "$out" | head -1 | tr -d "'\"")
  vf=$(bash "$(dirname "$sf")/verify-feedback.sh" "$out" >/dev/null 2>&1 && echo 0 || echo 1)
  printf '%s project_name=%s hash_is_main=%s verify_rc=%s\n' "$(basename "$d")" "$name" "$([ "$hash" = "$main_hash" ] && echo 1 || echo 0)" "$vf"
done
printf 'saved_in_temp_home=%s\n' "$(find "$w/home" -type f | grep -c .)"
```

ER-03 (a) 알려진 답 — 가짜 로그 폴더 다섯에서 찾는 폴더:

```bash
#!/usr/bin/env bash
# logdir.sh <md 파일> <셸> <CONTRACT_ROOT> — 그 파일에서 LOGS_ROOT= 가 든 bash 블록을 떼어, 가짜 로그 폴더에서 그 셸로 돌린다.
# 가짜 로그 폴더에는 본 저장소 이름 둘 · 워크트리 이름 둘 · 남의 이름 하나를 만든다. 블록이 폴더를 새로 만들면 made= 가 0 이 아니다.
md=${1:?}; sh=${2:?}; root=${3:?}
w=$(mktemp -d "${TMPDIR:-/tmp}/logdir.XXXXXX") || exit 2
trap 'rm -rf "$w"' EXIT
awk '/^```bash$/{f=1; buf=""; next} f && /^```$/{ if (buf ~ /LOGS_ROOT=/) { printf "%s", buf; exit } f=0; next } f { buf = buf $0 "\n" }' "$md" >"$w/block.sh"
[ -s "$w/block.sh" ] || { echo "NO_BLOCK $md"; exit 2; }
L=$w/logs; mkdir -p "$L/claude-plugins" "$L/claude-plugins-a1b2c3" "$L/kaizen-0924" "$L/kaizen-0924-d4e5f6" "$L/other-repo"
before=$(find "$L" | wc -l | tr -d ' ')
out=$(cd "$w" && CONTRACT_ROOT=$root REFLECT_KIT_LOGS_ROOT=$L "$sh" -c ". '$w/block.sh'" 2>&1)
after=$(find "$L" | wc -l | tr -d ' ')
printf '%s\n' "$out" | sed "s#^$L/##"
printf 'made=%s\n' "$((after - before))"
```

ER-04 (a) 알려진 답 — 평가 시각 덮어쓰기 블록:

```bash
#!/usr/bin/env bash
# evald.sh <qa-evaluator.md> <셸> — `### Step 5` 절에서 Evaluated 가 든 bash 블록을 떼어 가짜 리포트 두 벌에 그 셸로 돌린다.
# 답: 돌린 뒤 Evaluated 줄이 하나이고 값이 돌리기 직전 · 직후의 date 출력 가운데 하나다. 다른 줄은 그대로다.
# extra 는 블록이 리포트 옆에 새로 남긴 파일 수다(`sed -i.bak` 의 .bak 등) — 0 이어야 한다.
md=${1:?}; sh=${2:?}
w=$(mktemp -d "${TMPDIR:-/tmp}/evald.XXXXXX") || exit 2
trap 'rm -rf "$w"' EXIT
awk '/^### /{ s = index($0, "### Step 5:") == 1 } s && /^```bash$/{f=1; buf=""; next} s && f && /^```$/{ if (buf ~ /Evaluated/) { printf "%s", buf; exit } f=0; next } s && f { buf = buf $0 "\n" }' "$md" >"$w/block.sh"
[ -s "$w/block.sh" ] || { echo "NO_BLOCK"; exit 2; }
for v in '2099-01-01 00:00' '2026-09-25 (평가 시각, 이 파일 저장 시점)'; do
  printf '# Sprint Feedback\nFeature: x\nEvaluated: %s\nVerdict: APPROVE\n' "$v" >"$w/r.md"; cp "$w/r.md" "$w/orig.md"
  n0=$(ls -A "$w" | wc -l | tr -d ' ')
  t0=$(date '+%Y-%m-%d %H:%M')
  (cd "$w" && OUT=$w/r.md "$sh" -c ". '$w/block.sh'") >/dev/null 2>&1; rc=$?
  t1=$(date '+%Y-%m-%d %H:%M')
  n1=$(ls -A "$w" | wc -l | tr -d ' ')
  got=$(sed -n 's/^Evaluated: //p' "$w/r.md")
  n=$(grep -c '^Evaluated: ' "$w/r.md")
  other=$(diff <(grep -v '^Evaluated: ' "$w/orig.md") <(grep -v '^Evaluated: ' "$w/r.md") | grep -c '^[<>]')
  ok=0; { [ "$got" = "$t0" ] || [ "$got" = "$t1" ]; } && ok=1
  printf 'rc=%s lines=%s now=%s other_changed=%s extra=%s\n' "$rc" "$n" "$ok" "$other" "$((n1 - n0))"
  rm -f "$w"/*.bak   # 첫 바퀴가 남긴 .bak 이 둘째 바퀴 셈을 가리지 않게
done
```

ER-05 (b) 알려진 답 — 삭제 열거 두 명령의 옛 꼴 · 새 꼴:

```bash
#!/usr/bin/env bash
# renlist.sh — 커밋한 이동 하나 · 스테이징한 이동 하나가 있는 임시 저장소에서 삭제 열거 두 명령의 옛 꼴과 새 꼴을 돌린다.
# 답: 옮긴 파일의 옛 경로 keep/data.txt(커밋) · keep/two.txt(스테이징)가 새 꼴에서만 D 로 나온다.
export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1
export GIT_AUTHOR_NAME=t GIT_AUTHOR_EMAIL=t@e GIT_COMMITTER_NAME=t GIT_COMMITTER_EMAIL=t@e
w=$(mktemp -d "${TMPDIR:-/tmp}/renlist.XXXXXX") || exit 2
trap 'rm -rf "$w"' EXIT
cd "$w" && git init -q -b main && mkdir keep scope && echo a >keep/data.txt && echo b >keep/two.txt && git add -A && git commit -qm init || exit 2
base=$(git rev-parse HEAD)
git mv keep/data.txt scope/data.txt && git commit -qm mv && up=$(git rev-parse HEAD)
git mv keep/two.txt scope/two.txt
old_d=$(git diff --name-status --diff-filter=D "$base..$up" | awk '{print $2}' | tr '\n' ' ')
new_d=$(git diff --no-renames --name-status --diff-filter=D "$base..$up" | awk '{print $2}' | tr '\n' ' ')
old_s=$(git status --porcelain | grep -E '^(D.|.D) ' | awk '{print $2}' | tr '\n' ' ')
new_s=$(git status --porcelain --no-renames | grep -E '^(D.|.D) ' | awk '{print $2}' | tr '\n' ' ')
printf 'diff old=[%s] new=[%s]\nstatus old=[%s] new=[%s]\n' "${old_d% }" "${new_d% }" "${old_s% }" "${new_s% }"
```

ER-06 (b) 알려진 답 — 봉인 세기 블록이 정의 없이 멈추는가:

```bash
#!/usr/bin/env bash
# sealcnt.sh <contract-schema.md> <셸> <저장소 폴더> — 스키마의 「계약 봉인 상태 세기」 블록을 떼어 세 번 돈다.
# (1) 함수 정의 없이 (2) 봉인 블록만 읽고 fm_get 없이 (3) fm_get 블록과 봉인 블록을 읽고.
# 답: (1)(2) 는 종료 코드 0 이 아니어야 한다 — 정의가 빠진 채 세면 모든 계약이 SEAL_ABSENT 로 보여 「SEAL_BROKEN 0」 이 거짓으로 나온다.
md=${1:?}; sh=${2:?}; repo=${3:?}
w=$(mktemp -d "${TMPDIR:-/tmp}/sealcnt.XXXXXX") || exit 2
trap 'rm -rf "$w"' EXIT
blk() { awk -v pat="$1" '/^```bash$/{f=1; buf=""; next} f && /^```$/{ if (index(buf, pat)) { printf "%s", buf; exit } f=0; next } f { buf = buf $0 "\n" }' "$md"; }
blk 'verify_seal "$f"' >"$w/count.sh"; blk 'verify_seal() {' >"$w/defs.sh"; blk 'fm_get() {' >"$w/fm.sh"
[ -s "$w/count.sh" ] && [ -s "$w/defs.sh" ] && [ -s "$w/fm.sh" ] || { echo "NO_BLOCK"; exit 2; }
run() { out=$(cd "$repo" && "$sh" -c "$1" 2>/dev/null); rc=$?
  printf '%s rc=%s broken=%s ok=%s absent=%s\n' "$2" "$rc" "$(printf '%s\n' "$out" | awk '$2 == "SEAL_BROKEN" {print $1}')" \
    "$(printf '%s\n' "$out" | awk '$2 == "SEAL_OK" {print $1}')" "$(printf '%s\n' "$out" | awk '$2 == "SEAL_ABSENT" {print $1}')"; }
run ". '$w/count.sh'" none
run ". '$w/defs.sh'; . '$w/count.sh'" no_fm_get
run ". '$w/fm.sh'; . '$w/defs.sh'; . '$w/count.sh'" full
```

ER-06 (d) 알려진 답 — 스키마 서명 줄 도우미가 어느 문단의 서명을 잡는가:

```bash
#!/usr/bin/env bash
# sigline.sh <contract-schema.md> <셸> — 스키마의 서명 줄 도우미 블록(mine · unsigned_on)을 떼어 임시 저장소의 세 커밋에 그 셸로 돌린다.
# 세 커밋: 서명 줄이 끝 문단 · 서명 줄이 가운데 문단(끝 문단은 다른 글) · 문장 안에 슬러그 인용. 답은 git 이 낸다 — 도우미가 어느 커밋을 서명으로 보는가.
md=${1:?}; sh=${2:?}
export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1
export GIT_AUTHOR_NAME=t GIT_AUTHOR_EMAIL=t@e GIT_COMMITTER_NAME=t GIT_COMMITTER_EMAIL=t@e
unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE
w=$(mktemp -d "${TMPDIR:-/tmp}/sigline.XXXXXX") || exit 2
trap 'rm -rf "$w"' EXIT
awk '/^```bash$/{f=1; buf=""; next} f && /^```$/{ if (index(buf, "mine() {")) { printf "%s", buf; exit } f=0; next } f { buf = buf $0 "\n" }' "$md" >"$w/sig.sh"
[ -s "$w/sig.sh" ] || { echo "NO_BLOCK"; exit 2; }
r=$w/r; mkdir -p "$r"; git -C "$r" init -q -b main; : >"$r/base.txt"; git -C "$r" add -A; git -C "$r" commit -qm base
base=$(git -C "$r" rev-parse HEAD)
sig='Kaizen-Phase: s-x'
cm() { printf 'x\n' >"$r/$1.txt"; git -C "$r" add "$1.txt"; git -C "$r" commit -q -F -; }
printf '제목\n\n본문\n\n%s\nCo-Authored-By: t <t@e>\n' "$sig" | cm last
printf '제목\n\n%s\n\n끝 문단은 다른 글이다\n' "$sig" | cm middle
printf '제목\n\n본문에서 %s 를 인용한다\n\nCo-Authored-By: t <t@e>\n' "$sig" | cm inline
up=$(git -C "$r" rev-parse HEAD)
out=$(cd "$r" && "$sh" -c ". '$w/sig.sh'; mine $base $up '$sig'; echo ---; unsigned_on $base $up '$sig' last.txt middle.txt inline.txt | while read -r c; do git log -1 --format=%s --name-only \$c | tail -1; done" 2>&1)
m=$(printf '%s\n' "$out" | sed -n '1,/^---$/p')
u=$(printf '%s\n' "$out" | sed -n '/^---$/,$p' | grep -v '^---$' | grep . | tr '\n' ' ')
printf 'mine_last=%s mine_middle=%s mine_inline=%s unsigned=[%s]\n' "$(printf '%s\n' "$m" | grep -cx last.txt)" \
  "$(printf '%s\n' "$m" | grep -cx middle.txt)" "$(printf '%s\n' "$m" | grep -cx inline.txt)" "${u% }"
```

ER-07 (a) 알려진 답 — 원본 그대로 · 옛 값 다섯을 넣은 사본:

```bash
#!/usr/bin/env bash
# stale.sh <풀어 둔 판 폴더> — 그 판의 check-stale-values.py 를 원본 그대로 한 번, 등록된 옛 값을 다섯 파일에 넣은 사본으로 한 번 돌린다.
# 다섯 파일은 지금 검사 범위 밖이던 자리다(harness/agents · harness/evals · react-kit/references · onboarding-kit · rust-kit).
src=${1:?}
w=$(mktemp -d "${TMPDIR:-/tmp}/stale.XXXXXX") || exit 2
trap 'rm -rf "$w"' EXIT
cp -R "$src" "$w/t"
out=$(cd "$w/t" && python3 scripts/check-stale-values.py 2>&1); rc=$?
got=$(printf '%s\n' "$out" | sed -n 's/^검사 범위:.* 파일 \([0-9][0-9]*\) 개.*/\1/p' | head -1)
# 기대 파일 수: marketplace.json 의 킷 폴더(backend-kit 제외) ∪ 옛 소스 폴더 열둘 아래 .md 의 합집합
want=$(cd "$w/t" && python3 -c '
import json; from pathlib import Path
old=["design-kit/docs/design","design-kit/references","harness/docs/guides","harness/references","flutter-toolkit/references","docs/backend","docs/infra","docs/tone","docs/api","docs/rust","docs/react","docs/planning"]
kits=[p["source"].lstrip("./") for p in json.load(open(".claude-plugin/marketplace.json"))["plugins"] if p["name"]!="backend-kit"]
print(len({f.resolve() for d in old+kits if Path(d).exists() for f in Path(d).rglob("*.md")}))')
printf 'clean rc=%s files=%s want=%s excluded_line=%s\n' "$rc" "$got" "$want" "$(printf '%s\n' "$out" | grep -c '^ *검사 제외: backend-kit —')"
P=(harness/agents/qa-evaluator.md harness/evals/gate-exit-codes.md react-kit/references/render-evidence-protocol.md
   onboarding-kit/skills/setup-guide/SKILL.md rust-kit/skills/rust-model/SKILL.md)
for p in "${P[@]}"; do printf '\nbcrypt 비용은 OWASP 권장 12 로 둔다.\n' >>"$w/t/$p"; done
out=$(cd "$w/t" && python3 scripts/check-stale-values.py 2>&1); rc=$?
hits=0; for p in "${P[@]}"; do printf '%s\n' "$out" | grep -qF "  $p:" && hits=$((hits + 1)); done
other=$(printf '%s\n' "$out" | grep -E "^  [^ ]+:[0-9]+  'OWASP 권장 12'" | grep -vcF -e "${P[0]}:" -e "${P[1]}:" -e "${P[2]}:" -e "${P[3]}:" -e "${P[4]}:")
printf 'seeded rc=%s hits=%s/5 other_owasp=%s\n' "$rc" "$hits" "$other"
```

ER-08 (a) 알려진 답 — 실패 넷을 넣은 사본 · 원본 사본:

```bash
#!/usr/bin/env bash
# vline.sh <풀어 둔 판 폴더> — 그 판의 사본 셋에서 validate-plugin 의 V 줄과 post-kaizen 의 bare-fence 판정을 본다.
# 사본 A: harness 스킬 하나에 끊긴 링크(V3) · TODO(V5) · `$1`(V9) · 언어 표시 없는 펜스(V6)를 넣는다.
# 사본 B: 원본 그대로. 답: A 에서 V3 · V5 · V6 · V9 줄이 `— FAIL` 로 끝나고 bare-fence 가 FAIL, B 에서 둘 다 통과.
# unjudged 는 판정 글자(— OK · WARN · FAIL · SKIP)로 끝나지 않는 V 줄 수다 — 넷 밖의 줄이 판정 없이 남아도 잡는다.
src=${1:?}
w=$(mktemp -d "${TMPDIR:-/tmp}/vline.XXXXXX") || exit 2
trap 'rm -rf "$w"' EXIT
cp -R "$src" "$w/A"; cp -R "$src" "$w/B"
f=$w/A/harness/skills/init/SKILL.md
printf '\n[없는 문서](references/nope-zz.md)\n\nTODO 나중에 채운다\n\nawk 는 $1 을 쓴다\n\n```\nbare\n```\n' >>"$f"
for t in A B; do
  out=$(cd "$w/$t" && python3 scripts/validate-plugin.py harness 2>&1); rc=$?
  vfail=$(printf '%s\n' "$out" | grep -E '^  V(3|5|6|9) ' | grep -cE '— FAIL$')
  bf=$(cd "$w/$t" && python3 -c '
import importlib.util,sys
s=importlib.util.spec_from_file_location("vpk","scripts/validate-post-kaizen.py"); m=importlib.util.module_from_spec(s); s.loader.exec_module(m)
print(m.check_bare_fence().status)' 2>&1 | tail -1)
  uj=$(printf '%s\n' "$out" | grep -E '^  V[0-9]+ ' | grep -cvE '— (OK|WARN|FAIL|SKIP)$')
  printf '%s vp_rc=%s v3569_fail_lines=%s unjudged=%s bare_fence=%s\n' "$t" "$rc" "$vfail" "$uj" "$bf"
  if [ "$t" = A ]; then printf '%s\n' "$out" | grep -E '^  V(3|5|6|9) ' | sed "s/^/   /"; fi
done
```

AR-01 알려진 답 — 원본 열세 파일의 페이지 이름:

```bash
#!/usr/bin/env bash
# drift.sh <풀어 둔 판 폴더> — 그 판을 임시 저장소로 만들고 원본 열세 파일에 한 줄씩 더한 커밋을 올린 뒤
# detect-docs-drift.py --since HEAD~1 이 각 원본을 어느 페이지로 잇는지 본다. 답은 docs/ 에 실제로 있는 페이지 이름이다.
src=${1:?}
export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1
export GIT_AUTHOR_NAME=t GIT_AUTHOR_EMAIL=t@e GIT_COMMITTER_NAME=t GIT_COMMITTER_EMAIL=t@e
w=$(mktemp -d "${TMPDIR:-/tmp}/drift.XXXXXX") || exit 2
trap 'rm -rf "$w"' EXIT
cp -R "$src" "$w/t"; cd "$w/t" || exit 2
git init -q -b main && git add -A && git commit -qm base || exit 2
S=(onboarding-kit/skills/setup-guide/SKILL.md onboarding-kit/skills/setup-guide/references/format-checklist.md
   onboarding-kit/skills/setup-guide/references/project-detection.md docs/onboarding-kit/examples/fcm-ios-setup-guide.md
   docs/api/execution/probe-synthesis-hurl-semantics.md docs/api/execution/auth-secret-lifecycle.md
   docs/api/contract/snapshot-sealing-canonicalization.md docs/api/contract/contract-extraction-modes.md
   docs/api/verification/regression-diff-failure-policy.md docs/api/verification/static-evidence-viewer-contract.md
   docs/howto/deep-links.md reflect-kit/skills/codex-kaizen/SKILL.md bambu-kit/skills/bambu-print-profile/SKILL.md)
for s in "${S[@]}"; do printf '\n드리프트 시험 줄\n' >>"$s"; done
git add -A && git commit -qm edit || exit 2
out=$(python3 scripts/detect-docs-drift.py --since HEAD~1 2>&1); rc=$?
for s in "${S[@]}"; do
  line=$(printf '%s\n' "$out" | grep -F "$s → " | head -1)
  printf '%s\n' "${line:-$s → (없음)}"
done
printf 'rc=%s\n' "$rc"
```

AR-01 (b) — 오케스트레이터 F2 표의 킷 행:

```bash
#!/usr/bin/env bash
# f2map.sh <오케스트레이터 SKILL.md> — Step F2 「소스 → 출력 매핑」 표(그 굵은 줄부터 `**절차:**` 전까지)에서
# 출력 칸이 `docs/<킷>/` 인 행 수를 킷 다섯에 대해 세고, 없는 `planning-kit/references/` 가 표에 남았는지 센다.
f=${1:?}
[ -f "$f" ] || { echo "NO_FILE $f"; exit 2; }
tb=$(sed -n '/^\*\*소스 → 출력 매핑/,/^\*\*절차:\*\*/p' "$f" | grep -E '^\| ')
[ -n "$tb" ] || { echo "NO_TABLE"; exit 2; }
for k in reflect-kit bambu-kit onboarding-kit howto-kit api-kit; do
  printf '%s=%s ' "$k" "$(printf '%s\n' "$tb" | grep -cF "| \`docs/$k/\` |")"
done
printf 'planning_refs=%s\n' "$(printf '%s\n' "$tb" | grep -cF 'planning-kit/references/')"
```

AR-02 (a) — 새 단계 일곱의 자리:

```python
#!/usr/bin/env python3
# ci.py <ci.yml> — 새 시험 여섯 줄과 zsh 설치 줄이 validate 작업에 하나씩, 설치가 여섯 시험 모두보다 앞에 있는지 본다.
# reflect-kit 시험 둘은 zsh 가 없으면 zsh 경우를 건너뛰고 통과하므로 sh 러너 둘보다만 앞서서는 모자라다.
import sys, yaml
d = yaml.safe_load(open(sys.argv[1], encoding="utf-8"))
CMDS = ["bash react-kit/evals/scripts/project-detect-test.sh",
        "bash reflect-kit/evals/hooks/log-reflection-test.sh",
        "bash reflect-kit/evals/hooks/project-id-test.sh",
        "bash reflect-kit/evals/hooks/collect-status-test.sh",
        "sh onboarding-kit/skills/setup-guide/evals/run-gate-evals.sh",
        "sh howto-kit/evals/run-evals.sh"]
ZSH = "command -v zsh >/dev/null || { sudo apt-get update && sudo apt-get install -y zsh; }"
where = {c: [] for c in CMDS + [ZSH]}
for job, spec in (d.get("jobs") or {}).items():
    for i, st in enumerate(spec.get("steps") or []):
        run = (st.get("run") or "").strip()
        for c in where:
            if run == c:
                where[c].append((job, i))
ok = 0
for c in CMDS + [ZSH]:
    good = len(where[c]) == 1 and where[c][0][0] == "validate"
    ok += good
    print(f"{'OK' if good else 'NG'} {c} at={where[c]}")
zi = where[ZSH][0][1] if len(where[ZSH]) == 1 else None
order = zi is not None and all(len(where[c]) == 1 and where[c][0][1] > zi for c in CMDS)
print(f"placed={ok}/7 zsh_first={int(order)}")
```

DG-02 (a) — 파일마다 (규칙, 줄 글자) 묶음 비교:

```bash
#!/usr/bin/env bash
# mdcmp.sh <옛 판 폴더> <새 판 폴더> <파일…> — 파일마다 markdownlint 경고를 (규칙, 그 줄 글자) 묶음으로 두 판에서 세어,
# 새 판에만 더 있는 묶음 수를 낸다. 줄 번호를 쓰지 않으므로 더한 줄 옆 손대지 않은 줄에 붙은 새 경고(MD022 · MD024 · MD032)도 잡힌다.
K=$(cd "$(dirname "$0")" && pwd)
old=${1:?}; new=${2:?}; shift 2
lint() {  # lint <파일> — "규칙<TAB>줄 글자" 를 한 줄씩
  [ -f "$1" ] || return 0
  "$K/node_modules/.bin/markdownlint-cli2" --config "$K/cfg.markdownlint-cli2.jsonc" "$1" 2>&1 \
    | sed -nE 's/^[^ ]*:([0-9]+)(:[0-9]+)? (error|warning) (MD[0-9]+)\/.*/\1 \4/p' \
    | while read -r n r; do printf '%s\t%s\n' "$r" "$(sed -n "${n}p" "$1")"; done | sort
}
total=0
for f in "$@"; do
  a=$(lint "$old/$f"); b=$(lint "$new/$f")
  n=$(comm -13 <(printf '%s\n' "$a" | grep .) <(printf '%s\n' "$b" | grep .) | grep -c .)
  rules=$(comm -13 <(printf '%s\n' "$a" | grep .) <(printf '%s\n' "$b" | grep .) | cut -f1 | sort | uniq -c | awk '{printf "%s:%s ", $2, $1}')
  printf '%s new=%s %s\n' "$f" "$n" "$rules"
  total=$((total + n))
done
printf 'new_total=%s\n' "$total"
```

DG-02 (b) — 셸 경고 (코드, 줄 글자) 묶음 비교:

```bash
#!/usr/bin/env bash
# shcmp.sh <옛 판 폴더> <새 판 폴더> <파일…> — 파일마다 shellcheck 경고를 (코드, 그 줄 글자) 묶음으로 두 판에서 세어 새 판에만 더 있는 수를 낸다.
command -v shellcheck >/dev/null || { echo "TOOL_MISSING shellcheck"; exit 2; }
old=${1:?}; new=${2:?}; shift 2
lint() { [ -f "$1" ] || return 0
  shellcheck -f gcc "$1" 2>/dev/null | sed -nE 's/^[^:]*:([0-9]+):[0-9]+: [a-z]+: .*\[(SC[0-9]+)\]$/\1 \2/p' \
    | while read -r n c; do printf '%s\t%s\n' "$c" "$(sed -n "${n}p" "$1")"; done | sort; }
total=0
for f in "$@"; do
  n=$(comm -13 <(lint "$old/$f" | grep .) <(lint "$new/$f" | grep .) | grep -c .)
  printf '%s new=%s\n' "$f" "$n"; total=$((total + n))
done
printf 'new_total=%s\n' "$total"
```

### 봉인 전 실측 (2026-09-25, `END` 자리에 시작 커밋 `5b4fd72` 를 넣고 같은 측정을 돌림)

시작 커밋 판 값은 조건이 떨어져야 할 값이다(음성 대조). 「모의본」 은 개선안대로 고친 사본을 스크래치에 만들어 도우미가 기대 출력을 내는지 본 것이다 — 도우미가 살아 있다는 확인이지 구현이 아니다.

| 조건 | 측정 | 시작 커밋 판 | 모의본 · 양성 대조 |
| ---- | ---- | ------------ | ------------------ |
| SK-01 ~ SK-05 · ER-01 (e) · ER-03 (c) · ER-04 (b) · ER-05 (a) · ER-06 (a) · ER-07 (b) · AR-03 (c) | `toks.py` 접두별 끝줄 | SK01 `rows=30 ng=30` · SK02 `16 ng=16` · SK03 `8 ng=8` · SK04 `6 ng=6` · SK05 `34 ng=33`(SK05-N8 만 OK — 바뀌지 않아야 할 줄) · ER01 `1 ng=1` · ER03 `2 ng=2` · ER04 `1 ng=1` · ER05 `6 ng=6` · ER06 `4 ng=4` · ER07 `1 ng=1` · AR03 `1 ng=1` | 새 글자 일흔(바뀌지 않을 SK05-N8 포함 일흔하나)에 번역투 · 버전꼴 0 (K02 grep 종료 코드 1). SK02 새 세 줄만 고친 phase-dependencies 모의본: SK02-O6 · O7 · N9 셋 다 OK |
| SK-01 (b) · SK-02 (b) · AR-03 (a) | `orch.sh B B` | `diagram=0 depdoc=0 concur=0 signline=0 auto_removed=0 auto_added=0` | 모의본 둘: `diagram=1 depdoc=1 concur=1 signline=1` · 범위 줄 틀만 고쳐 `sync-orchestrator.py` 를 돌린 사본 `auto_removed=3 auto_added=3` 과 기대 세 줄 · `--check-only` 종료 코드 0 |
| SK-03 (b)(c)(d)(e) | 템플릿 수 · 표 줄 · Phase 4 절 · rust 새 꼴 grep | `6` · `0` · `n3=0 evals=0` · 새 꼴 종료 코드 1, 옛 꼴은 `./.claude/kaizen-input/plugin-qa-data.md` · `./.claude/skills/rust-kaizen/SKILL.md` 를 잡음 | — |
| SK-04 (a) | `grep -lE 'history/[^ ]*(contract\|[*][.]md)'` 파일 수 | `4` (backend · design · infra · react) | — |
| SK-05 (b)(c) | 줄 단위 grep | `0 · 0` · `row16=0 item7=0` | — |
| SK-05 (d)(e) | `upref.sh` · 배치 우선순위 넷째 칸 차례 · 첫 행 | `upper=0/5` · `1(최고),2,3,4(최저),` · `0` | 개선안 (마) ~ (아)만 고친 모의본: `upper=5/5` · `1(최고),2,3,4,5(최저),` · `1` · 새 toks 스무 줄 모두 OK · 일곱 파일 `mdcmp.sh` `new_total=0` · 더한 줄 번역투 · 버전꼴 0 · `validate-plugin.py harness` · `sync-docs.py --check-only` 종료 코드 0. 모의본에서 평가 가이드의 문장만 규칙 줄 밖 새 문단으로 옮긴 사본: toks SK05-N13 은 OK 인데 `upper=4/5` — 짝 검사가 따로 잡는다 |
| SK-06 · AP-01 | `added` · `newurls` · 버전꼴 | 0 · 0 · 0 (더한 줄 없음) | 사본 README 에 「이 문제에 대해 적는다. 버전 v9.8.7 로 둔다. https://example.invalid/fake-f1h」 한 줄 → `k02=1 ver=1 newurl_not_in_evidence=1` |
| ER-01 (a) | `ren2.sh` | `N1 hook_rc=2 git_dels=0 DISAGREE` · `N2 … DISAGREE` · `N3 hook_rc=2 git_dels=60 agree` · `N4 hook_rc=2 git_dels=60 agree` · `N5 hook_rc=2 git_dels=0 DISAGREE` | — (구현 몫. 교차 진단 재현 `xdiag-p4/ren.sh` 와 같은 값) |
| ER-01 (b) | `align.sh` | 열한 줄 `agree` · `60 51 50 0 0 55 59 60 0 0 0` | — |
| ER-01 (c) | 훅 시험 `bash` · `/bin/bash` | 둘 다 `rc=0` · `실패 0 건` · PASS 39 줄 | — |
| ER-02 (a)(b) | `ident.sh` · 저장 시험 | `projmain project_name=projmain hash_is_main=1 verify_rc=0` · `wt-x project_name=wt-x hash_is_main=0 verify_rc=0` · `saved_in_temp_home=2` · 저장 시험 `rc=0` · `=== ALL TESTS PASSED ===` · 남은 파일 0 | 모의본(`identity_root_of` 를 `--git-common-dir` 규칙으로): 둘째 줄 `wt-x project_name=projmain hash_is_main=1` |
| ER-03 (a)(b) | `logdir.sh` 여덟 번 · `logblk` 비교 | 작업 폴더: `kaizen-0924 kaizen-0924-d4e5f6 made=0` · 본 저장소: `claude-plugins claude-plugins-a1b2c3 made=0` (두 파일 · 두 셸 같음) · 명령 줄 차이 0 | 모의 블록: 작업 폴더 `claude-plugins claude-plugins-a1b2c3 kaizen-0924 kaizen-0924-d4e5f6 made=0` · 본 저장소 두 줄 (bash · zsh 같음). 실제 `~/.claude/logs` 에는 `claude-plugins` 가 있고 `kaizen-0924` 는 없다 — 지금 판은 이 작업 폴더에서 `correction_log_status: unavailable` |
| ER-04 (a) | `evald.sh` | `NO_BLOCK` (bash · zsh) | `sed -i.bak` 만 쓴 모의 블록: 두 줄 `rc=0 lines=1 now=1 other_changed=0 extra=1` · 끝에 `rm -f "$OUT.bak"` 를 붙인 모의 블록: 두 줄 `… extra=0` (bash · zsh 같음 — 둘째 바퀴도 1 이라 바퀴 사이 정리가 셈을 가리지 않는다). 시각을 고정한 나쁜 블록: `now=0` (bash · zsh) |
| ER-05 (b) | `renlist.sh` | `diff old=[] new=[keep/data.txt]` · `status old=[] new=[keep/two.txt]` | — |
| ER-06 (d) | `sigline.sh` bash · zsh | 둘 다 `mine_last=1 mine_middle=1 mine_inline=0 unsigned=[inline.txt]` — 시작 판 설명 「끝 문단의 한 줄」 과 다른 동작 | 설명만 고친 모의본도 같은 값 · toks ER06-O2 · N2 OK |
| ER-06 (b)(c) | `sealcnt.sh` 를 `$T/B` 에 · 상한 꼴 | `none rc=0` · `no_fm_get rc=0 absent=77` · `full rc=0 ok=67 absent=10` (bash · zsh) · 옛 꼴 `old_rc=0` · 새 꼴 `new_rc=2` | 모의본(블록 머리에 정의 확인 한 줄)을 `$T/B` 에: `none rc=2` · `no_fm_get rc=2` · `full rc=0 ok=67 absent=10` (bash · zsh). 작업 폴더에는 커밋 안 된 Final 초안 둘이 더 있어 `absent=12` 로 달라진다 — 그래서 끝 판을 읽는다 |
| ER-07 (a) | `stale.sh` | `clean rc=0 files=133 want=389 excluded_line=0` · `seeded rc=0 hits=0/5 other_owasp=0` | 네 폴더만 넓힌 모의본: `seeded rc=1 hits=5/5 other_owasp=0` · 킷 전부로 넓히면 backend-kit 세 줄(`OpenAPI 3.1.1` 명세 링크)만 걸림 — 그래서 뺀다 |
| ER-08 (a)(b)(c) | `vline.sh` · harness V 줄 · 검증 가이드 예시 절 | `A vp_rc=2 v3569_fail_lines=0 unjudged=4 bare_fence=PASS` · `B vp_rc=0 v3569_fail_lines=0 unjudged=0 bare_fence=PASS` · V 줄 열 개 `— OK` · 종료 코드 0 · 예시 절 판정 없는 V 줄 2 (`V3 refs 89 links, 2 BROKEN` · `V4 triggers 58 keywords, 1 duplicate`) · `— FAIL` 줄 0 | 모의본(요약 끝에 `— <판정>` · `check_bare_fence` 를 `--check=code-fence` 종료 코드로): `A vp_rc=2 v3569_fail_lines=4 unjudged=0 bare_fence=FAIL` · `B vp_rc=0 v3569_fail_lines=0 unjudged=0 bare_fence=PASS`. 예시 V3 · V4 줄에 `— FAIL` · `— WARN` 을 붙인 가이드 모의본: 판정 없는 줄 0 · `— FAIL` 1. 실패 예시 줄을 지운 모의본: `— FAIL` 0 으로 떨어진다 |
| AR-01 | `drift.sh` · `f2map.sh` | 열한 줄 `(없음)` · codex-kaizen 줄 `docs/reflect-kit/SKILL.html  [NEW …` · bambu 줄만 맞음 · `rc=0` · `reflect-kit=0 bambu-kit=0 onboarding-kit=0 howto-kit=0 api-kit=1 planning_refs=1` | 매핑 · 이름 규칙 · 덮어쓰기를 넣은 모의본: 기대 열세 줄 그대로 · `[NEW` 0. F2 표에 넷 행을 더하고 planning 행에서 `planning-kit/references/` 를 뺀 모의본: `reflect-kit=1 bambu-kit=1 onboarding-kit=1 howto-kit=1 api-kit=1 planning_refs=0`. 표 머리 줄을 지운 사본: `NO_TABLE` · 종료 코드 2 (조용히 0 을 내지 않는다) |
| AR-02 | `ci.py` · `\|\|` · actionlint · 여섯 시험 · (c) 예외의 킷 폴더 커밋 수 | `placed=0/7 zsh_first=0` · `0` · `0` · 시작 판 사본에서 여섯 모두 종료 코드 0(`결과: 6 · 24 · 16 · 10 경우 중 불일치 0` · `EVALS_PASS` · `EVALS_PASS`) · 킷 넷 모두 0 (구간 빈 상태) | zsh 단계를 맨 앞에 둔 일곱 단계 모의 ci.yml: `placed=7/7 zsh_first=1` · actionlint 0 · `\|\|` 0. zsh 단계를 reflect-kit 시험 뒤 · `sh` 러너 앞에 둔 모의본: `placed=7/7 zsh_first=0` (옛 측정이면 통과했을 꼴) |
| AR-05 (c)(f) | 알려진 두 서명 밖 커밋의 `.harness/` 밖 파일 수 · 공유 파일을 건드린 kit-followups 밖 커밋 수 | `0` · `0` (구간 빈 상태) | 시작 커밋 판 임시 복제본에 커밋을 얹어 봄: 서명 끝 글자가 빠진 커밋이 킷 파일을 건드리면 (c) 새 꼴 1 · 옛 꼴(`Kaizen-Phase:` 로 시작하는 줄만 봄) 0. 이 계약 서명 커밋이 `marketplace.json` 을 건드리면 (f) 1. kit-followups 서명 커밋이 `docs/index.html` 을 건드리면 (f) 0. 양성 대조 `c=9cb0e02`(합치기 커밋) 의 `c~1..c` 에 (f) 2. 경로 열하나 모두 마지막으로 건드린 커밋이 있다(glob 경로 표기가 살아 있다) |
| AR-05 (d) | 끝 판 `.harness/` 봉인 상태 세기 | `$T/B/.harness` 에서 `SEAL_BROKEN` 0 · `SEAL_OK` 67 · `SEAL_ABSENT` 10. 이 계약 파일은 시작 판에 없어 `SEAL_ABSENT` (2 회차 검토 실측 · BUILD 가 봉인 전에 다시 잼) | — |
| RE-02 | 함수 수 · `check_bare_fence` 본문 · marketplace | `commit-guard.sh` 12 · `save-feedback.sh` 7 · 본문 `--check=code-fence` 0 · `"0 bare" in out` 1 · `marketplace.json` 0 | — |
| DG-02 | `mdcmp.sh` · `shcmp.sh` · `py_compile` | 시작 판끼리 `new_total=0`(마크다운 스물한 파일) · `new_total=0` · 파이썬 다섯 통과 | 사본에 맨 URL · 언어 표시 없는 펜스 → `README new=1 MD034:1` · `tone-kaizen new=1 MD040:1` · `new_total=2`. `save-feedback.sh` 에 `echo $1` → `new=1` |
| AP-03 | `validate-plugin.py harness --check=code-fence` | 종료 코드 0 · V6 줄 `0 bare — OK` | — |
| DG-05 | 저장소 검사 · 사후 점검 | `validate-plugin` 0 · `sync-docs` 0 · `sync-evals` 0 · `run-evals` 0(`115 passed`) · `validate-doc-contracts` 0 · `check-stale-values` 0 · `sync-orchestrator --check-only` 0 · 사후 점검 `scope-isolation` · `doc-contracts` · `bare-fence` PASS | — |
| SC-00 · DG-01 · DG-04 | 양성 대조 grep | — | `3` · `1` · `2` |

## Skill

- [ ] SK-01: 오케스트레이터 스킬이 Phase 17(howto-kit)을 빠뜨린 자리를 모두 채우고, 킷 Phase 동시 실행 상한 · 서명 줄 규약의 원문 위치 · api-kit 경로 간 불변식을 후처리에 두는 이유를 바르게 적는다 (final-todo 「카이젠 진행 스킬 문서」 세 줄 · phase2-notes §Final 에 넘기는 것 둘째 줄 · phase16-notes §넘기는 것 둘째 줄) — Given: 이 계약의 커밋이 끝난 뒤(공통 정의의 `$END`). 측정: (a) `python3 "$K/toks.py" "$T/E" SK01` 끝줄이 `rows=30 ng=0` — 옛 글자 열 줄(`phase10|phase11|final]` · `Phase 1~14` · `→16→Final` · `Phase 1~16 완료 전제` · `Phase 1~16 전체 변경사항` · `` `phase_1` ~ `phase_12` `` · `react-kit → planning-kit 순서로` · `Phase 2~16 변경에` · `Phase 5~16 (` · 옛 불변식 문장)이 0, 새 글자 스무 줄이 기대 수(`api-kit → howto-kit 순서로` 2, 나머지 1) (b) `bash "$K/orch.sh" "$T/B" "$T/E"` 첫 줄에 `diagram=1` · `concur=1` · `signline=1` — `## Phase 의존성` 그림 블록에서 `Phase 16: Api-kit` · `Phase 17: Howto-kit` · `Final:` 로 시작하는 줄이 이 차례로 한 번씩이고, `### 각 Phase 공통 실행 패턴` 절 안에서 `동시에 도는 킷 Phase 는 3 개까지` 가 든 줄이 `.harness/.meta/orchestrator-audit-log.md` 를, `§여러 주체가 한 가지에 커밋할 때` 가 든 줄이 `Kaizen-Phase: <슬러그>` 를 함께 담는다 [exact, enumerated]
- [ ] SK-02: 오케스트레이터 참조 두 문서가 Phase 17 과 실제 경로 · 출처 이름을 적는다 — phase-dependencies 는 Phase 17 블록 · 표 행 · 스킵 줄과 onboarding 의 실제 참조 폴더, phase-research-templates 는 세 행 정정 (phase1-notes §Final 에 넘기는 것 둘째 줄 · phase8-notes §넘기는 것 · phase15-notes §넘기는 것 넷째 줄 · phase14-notes §미반영 마지막 줄) — 측정: (a) `python3 "$K/toks.py" "$T/E" SK02` 끝줄이 `rows=16 ng=0` (옛 글자 `Phase 7~16` · `onboarding-kit/references/` · `planning-kit/references/` · `|planning|tone|api}/` · `500 라인 상한` · `| 공식 | 3 signals stable |` · `[국립국어원 공공언어](` 0, 새 글자 아홉 1 — 같은 파일의 같은 결함 두 자리(`:56` 없는 planning 참조 폴더 · `:124` 리서치 전용 모드 목록에 howto 없음)를 포함한다) (b) `bash "$K/orch.sh" "$T/B" "$T/E"` 첫 줄에 `depdoc=1` — phase-dependencies 그림 블록에서 `Phase 16: Api-kit` · `  api-kit/skills/*/SKILL.md` · `Phase 17: Howto-kit` 로 시작하는 줄이 이 차례로 한 번씩 [exact, enumerated]
- [ ] SK-03: 카이젠 스킬 다섯의 틀린 수 · 죽은 검사를 고친다 — tone-kaizen 템플릿 수, howto-kaizen 러너 설명, onboarding-kaizen 검증 줄, rust-kaizen 의 자기 파일을 잡는 검사, infra-kaizen 형제 표의 미검증 칸 (phase15 · phase17 · phase14 · phase9 · phase8 notes §넘기는 것) — 측정: (a) `python3 "$K/toks.py" "$T/E" SK03` 끝줄이 `rows=8 ng=0` (b) `find "$T/E/tone-kit/templates" -maxdepth 1 -name '*.md' | wc -l` 이 6 — SK03-N1 의 「6종」 과 같은 수 (c) `grep -F 'infra-audit · infra-reviewer (agent)' "$T/E/.claude/skills/infra-kaizen/SKILL.md" | grep -cF '`[미검증]` 네 칸'` 이 1 (d) `sect "$T/E/.claude/skills/onboarding-kaizen/SKILL.md" '### Phase 4:'` 출력에 `` `sh onboarding-kit/skills/setup-guide/evals/run-gate-evals.sh` `` 1 줄 · `EVALS_PASS` 1 줄 이상 (e) `cd "$T/E" && grep -rn "17개 리서치\|17 리서치\|docs/rust/ 리서치 문서 17" rust-kit docs/rust` 의 종료 코드가 1 (찾은 줄 없음 — 옛 꼴 `.` 전체 검사는 시작 커밋 판에서 rust-kaizen SKILL.md 자신을 잡아 늘 1 이상이었다) [exact, enumerated]
- [ ] SK-04: 카이젠 스킬 넷이 병렬 Phase 계약을 `.harness/history/` 에 쓰라는 옛 규칙을 버리고 슬러그 계약 경로를 가리킨다 — react-kaizen Step 6 · backend-kaizen · design-kaizen · infra-kaizen Gotcha 7 (phase10-notes §넘기는 것 다섯째 줄 · 같은 규칙의 다른 자리 셋은 편집 전 감사) — 측정: (a) `grep -lE 'history/[^ ]*(contract|[*][.]md)' "$T/E"/.claude/skills/*-kaizen/SKILL.md | wc -l` 이 0 (시작 커밋 판 4) (b) `python3 "$K/toks.py" "$T/E" SK04` 끝줄이 `rows=6 ng=0` — 네 파일에 `` `.harness/sprint-contract-<slug>.md` `` 가 1 줄씩, react-kaizen 에 `git add <내 경로> && git commit -o <내 경로>` 1 줄, `병렬 실행 중 git 쓰기 금지` 0 [exact, enumerated]
- [ ] SK-05: 설계 · 계약 가이드와 평가자 문서 · 하네스 스킬 둘이 서로 어긋나거나 빠뜨린 여덟 곳을 고친다 — (가) 「시도한 우회」 칸의 `없음` 을 평가자 규칙 11 (2) 와 같은 폭(계약에 대체 검증 단계가 없을 때만)으로 좁힌다 (나) 동시 실행 20 개 상한이 ultracode 에는 없다는 근거 파일 내용을 옮긴다 (다) skill 가이드 짝 대조표 16 행과 그 설명 문단이 평가자 쪽 짝을 적는다 (라) 평가자 규칙 10 의 「위 (c)」 가리킴을 문단 이름으로 바꾼다 (마) Diff-Scope 표준형의 상한 ref 는 커밋 구간을 재는 조건에만 요구한다고 그 규칙을 정의하는 다섯 줄(스키마 · 계약 가이드 · 평가자 · 평가 가이드 · sprint-contract Gotcha)에 적는다 — 커밋 전 두 상태를 허용하면서 상한을 늘 요구하던 모순 (바) 평가 가이드의 `CONTRACT_ROOT` 정의를 스키마와 같은 「처음 만나는 `.harness/`」 기준으로 (사) 플러그인에서 무시되는 필드를 적은 세 자리(agent 가이드 플러그인 주의 줄 · create-agent Gotcha · 체크리스트)에 `initialPrompt` 를 더한다 (아) 에이전트 배치 우선순위 표 맨 위에 managed settings 를 넣고 나머지 넷을 2 ~ 5 로 (xdiag P1 계약 밖 1 · 2 · P3 계약 밖 2 · 작은 것 첫째 · Codex r1 3 · 5 · 6 · 7) — 측정: (a) `python3 "$K/toks.py" "$T/E" SK05` 끝줄이 `rows=34 ng=0` (b) `grep -F '**동시 실행 20 개**' "$T/E/harness/docs/guides/agent-design-guide.md" | grep -cF 'ultracode 에서는 동시 실행 20 개 상한도 적용되지 않는다'` 가 1 이고 `grep '^| \*\*하드 리밋\*\* |' "$T/E/harness/docs/guides/agent-design-guide.md" | grep -cF 'ultracode 는 동시 상한 없음'` 이 1 (c) `$T/E/harness/docs/guides/skill-design-guide.md` 에서 `` 평가자 쪽 짝은 `qa-evaluation-guide.md` §산출물이 검사일 때 ⑤ `` 가 `| 16 |` 로 시작하는 줄에 1 · `Item 7 은` 으로 시작하는 줄에 1 (d) `bash "$K/upref.sh" "$T/E"` 끝줄이 `upper=5/5` — 스키마 `**(5) 상한 ref**` 줄 · 계약 가이드 `| 5 | **상한 ref** —` 줄 · 평가자와 평가 가이드의 `중 빠진 것을 REJECT 사유에 열거한다` 줄 · sprint-contract `표준형 5 요소를 다 채워라` 줄에 `상한 ref 는 커밋 구간을 재는 조건에만 요구한다` 가 같은 줄로 있다 (시작 커밋 판 `upper=0/5`) (e) `sect "$T/E/harness/docs/guides/agent-design-guide.md" '### 배치 위치 (우선순위순)' | grep -E '^\| ' | tail -n +3 | awk -F'|' '{gsub(/ /,"",$4); printf "%s,", $4}'` 출력이 정확히 `1(최고),2,3,4,5(최저),` 이고 같은 표의 첫 데이터 행(`grep -E '^\| ' | sed -n 3p`)에 `managed settings` 가 1 (시작 커밋 판 `1(최고),2,3,4(최저),` · 0) [exact, enumerated]
- [ ] SK-06: 더한 글이 문체 규칙과 근거 규칙을 지킨다 — (a) 서른한 파일(공통 정의 `FILES`)에 더한 줄에 번역투 6 종(`tone-kit/references/locale-korean.md` §2 치환표의 grep 열 — 공통 정의 `K02`)이 0 줄 (b) 서른한 파일에 새로 생긴 URL 가운데 시작 커밋 판 `.harness/.meta/evidence/phase*.md` 열일곱 파일에 없는 것이 0 개 — 파일마다 편집 전 판과 비교한다. 측정: 두 측정 앞에 `type added newurls evurls >/dev/null || exit 2;` 를 둔다 (a) `added | grep -cE "$K02"` 가 0 (b) `LC_ALL=C comm -23 <(newurls) <(evurls) | grep -c .` 가 0. 양성 대조: 시작 커밋 판 사본의 `harness/README.md` 끝에 「이 문제에 대해 적는다 … `https://example.invalid/fake-f1h`」 한 줄을 넣으면 (a) 1 · (b) 1 (봉인 전 실측) [exact]

## Script

- [ ] SC-00: N/A (Script 카테고리는 `release.sh` 연동 · 버전 올림 · `marketplace.json` 갱신이다. Final 계약들은 버전을 올리지 않는다 — `kaizen-0924-final` 이 `.harness/.meta/kaizen-0924/release-plan.md` 에 적는다. 측정: `type my >/dev/null || exit 2;` 뒤 `my | grep -cE '^(scripts/release\.sh|\.claude-plugin/marketplace\.json|[^/]+/\.claude-plugin/plugin\.json)$'` 이 0. 양성 대조: 같은 `grep -cE` 에 `scripts/release.sh` · `.claude-plugin/marketplace.json` · `harness/.claude-plugin/plugin.json` · `harness/README.md` 네 줄을 넣으면 3)

## Error

- [ ] ER-01: 커밋 안전 훅이 이름 바꾸기를 삭제로 세지 않는다 — 경로 지정 커밋(`-o` · `-- <경로>`)과 `-i` 커밋에서도 git 이 이름 바꾸기 감지로 싣는 삭제만 센다. 옮긴 새 경로가 지정 경로 밖이라 실제로 삭제가 실리는 커밋과, 이름 바꾸기에 진짜 삭제 51 개 이상이 섞인 커밋은 여전히 막는다 (xdiag P4 계약 밖 1 · final-todo 「Phase 4 계약 밖」) — Given: 이 계약의 커밋이 끝난 뒤. 측정: (a) 알려진 답 — `bash "$K/ren2.sh" "$T/E/harness/scripts/commit-guard.sh"` 다섯 줄이 모두 `agree` 이고 차례로 `N1_mv_path hook_rc=0 git_dels=0` · `N2_mvadd_path hook_rc=0 git_dels=0` · `N3_mv_del_path hook_rc=2 git_dels=60` · `N4_mv_half_path hook_rc=2 git_dels=60` · `N5_mvadd_include hook_rc=0 git_dels=0` (시작 커밋 판은 N1 · N2 · N5 가 `hook_rc=2 … DISAGREE`) (b) 기존 경우가 그대로다 — `bash "$K/align.sh" "$T/E/harness/scripts/commit-guard.sh"` 열한 줄이 모두 `agree` 이고 `git_dels` 가 차례로 `60 51 50 0 0 55 59 60 0 0 0` (c) `$T/E/harness/evals/hooks/commit-guard-test.sh` 를 `bash` 와 `/bin/bash`(3.2) 로 각각 돌리면 둘 다 끝줄 `실패 0 건` · 종료 코드 0 이고, `PASS ㉖ ` · `PASS ㉗ ` · `PASS ㉘ ` · `PASS ㉙ ` · `PASS ㉚ ` 로 시작하는 줄이 각각 1 개 (㉖ `git mv` 뒤 경로 지정 커밋 통과 · ㉗ `mv` + `git add` 뒤 경로 지정 커밋 통과 · ㉘ `-i` 로 옮긴 파일 커밋 통과 · ㉙ 이름 바꾸기 60 + 삭제 60 경로 지정 커밋 차단 · ㉚ 옮긴 새 경로가 지정 경로 밖이라 삭제 60 이 실리는 경로 지정 커밋 차단 — `ren2.sh` N4 꼴) (d) 음성 대조 — 같은 시험을 `COMMIT_GUARD_HOOK="$T/B/harness/scripts/commit-guard.sh"` 로 돌리면 `FAIL` 로 시작하는 줄의 번호가 정확히 `㉖ ㉗ ㉘` (㉙ · ㉚ 은 시작 커밋 판 훅도 막는다 — `ren2.sh` N3 · N4 가 시작 커밋 판에서 `hook_rc=2 git_dels=60 agree`) (e) `sect "$T/E/harness/README.md" '## 커밋 안전 훅' | grep -cF '이름 바꾸기는 여기서도 삭제로 세지 않는다'` 가 1 [exact, enumerated]
- [ ] ER-02: 피드백 저장 스크립트가 워크트리에서 불려도 저장본의 `project_name` · `project_hash` 를 본 저장소 기준으로 적는다 — reflect-kit `project_root` 와 같은 규칙 (`reflect-collector:P5` · `harness:P02` 비고 · 러닝북 Phase 12 추가 과제 · phase1 · 2 · 3 · 12 · 15 · 16 · 17 notes) — 측정: (a) 알려진 답 — `bash "$K/ident.sh" "$T/E/harness/scripts/save-feedback.sh"` 세 줄이 `projmain project_name=projmain hash_is_main=1 verify_rc=0` · `wt-x project_name=projmain hash_is_main=1 verify_rc=0` · `saved_in_temp_home=2` (시작 커밋 판은 둘째 줄이 `wt-x project_name=wt-x hash_is_main=0 verify_rc=0`) (b) `HOME` 을 새 임시 폴더로, `GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1` 로 두고 `bash "$T/E/harness/evals/kaizen/feedback-system/save-test.sh"` 를 돌리면 종료 코드 0 · 끝줄 `=== ALL TESTS PASSED ===` · `PASS: 워크트리 저장본 project_name` 으로 시작하는 줄 1 · 임시 HOME 에 남은 파일 0 (c) 음성 대조 — `$T/E` 를 복사한 사본에서 `harness/scripts/save-feedback.sh` 만 `$T/B` 판으로 바꾸고 (b) 를 같은 방식으로 돌리면 종료 코드 0 이 아니고 `FAIL: 워크트리 저장본 project_name` 으로 시작하는 줄 1 [exact, enumerated]
- [ ] ER-03: 평가자의 사용자 교정 대조가 워크트리에서 불려도 본 저장소 이름의 로그 폴더를 찾는다 — 본 저장소 이름과 워크트리 이름 둘을 hash 접미 포함으로 합쳐 찾고, 폴더를 새로 만들지 않는다 (phase12-notes §넘기는 것 둘째 줄 · xdiag P13 계약 밖 3) — 측정: (a) `$T/E` 판 `harness/agents/qa-evaluator.md` 와 `harness/docs/guides/qa-evaluation-guide.md` 각각에 `bash "$K/logdir.sh" <파일> <셸> <CONTRACT_ROOT>` 를 셸 `bash` · `zsh`, CONTRACT_ROOT 작업 폴더(`$PWD`) · `/Users/jackson/Hub/10_Dev/claude-plugins` 로 여덟 번 돌리면, 작업 폴더일 때 네 줄 `claude-plugins` · `claude-plugins-a1b2c3` · `kaizen-0924` · `kaizen-0924-d4e5f6` 과 `made=0`, 본 저장소일 때 두 줄 `claude-plugins` · `claude-plugins-a1b2c3` 과 `made=0` (시작 커밋 판은 작업 폴더일 때 `kaizen-0924` · `kaizen-0924-d4e5f6` 둘뿐) (b) 두 파일에서 `LOGS_ROOT=` 가 든 bash 블록의 주석 줄을 뺀 명령 줄이 같다 — `type logblk >/dev/null || exit 2;` 뒤 `diff <(logblk "$T/E/harness/agents/qa-evaluator.md" | grep -v '^#') <(logblk "$T/E/harness/docs/guides/qa-evaluation-guide.md" | grep -v '^#') | grep -c .` 이 0 (공통 정의 `logblk`) (c) `python3 "$K/toks.py" "$T/E" ER03` 끝줄이 `rows=2 ng=0` [exact, enumerated]
- [ ] ER-04: 평가자가 리포트의 `Evaluated` 시각을 짐작하지 않는다 — 저장 절차(`### Step 5:` 절)가 리포트 경로 `$OUT` 을 받아 저장한 뒤 `Evaluated:` 줄을 그 순간의 `date` 출력으로 덮어쓰는 bash 블록을 두고, 그 블록은 리포트 옆에 새 파일(`.bak` 등)을 남기지 않는다 (xdiag P2 계약 밖 2 · final-todo 「Phase 2」 넷째 줄 — Phase 3 이 틀 주석으로 넣은 뒤에도 p04 리포트는 `Evaluated: 2026-09-25 (평가 시각, 이 파일 저장 시점)`, p15 · p16 은 파일 저장보다 19 분 · 29 분 뒤 시각을 적었다) — 측정: (a) 알려진 답 — `bash "$K/evald.sh" "$T/E/harness/agents/qa-evaluator.md" bash` 와 `… zsh` 가 각각 두 줄 `rc=0 lines=1 now=1 other_changed=0 extra=0` (시작 커밋 판은 `NO_BLOCK`. `sed -i.bak` 만 쓰고 `.bak` 을 지우지 않는 블록은 `extra=1` 로 떨어진다 — 봉인 전 실측) (b) `sect "$T/E/harness/agents/qa-evaluator.md" '### Step 5:' | grep -cF '저장한 뒤 아래 블록으로 `Evaluated:` 줄을 그 순간의 `date` 출력으로 덮어쓴다'` 가 1 [exact, enumerated]
- [ ] ER-05: 평가자의 삭제 열거가 옮긴 파일의 옛 경로를 놓치지 않는다 — 커밋 구간 명령과 커밋 안 한 변경 명령 둘 다 이름 바꾸기 감지를 끈다 (xdiag P3 계약 밖 1) — 측정: (a) `python3 "$K/toks.py" "$T/E" ER05` 끝줄이 `rows=6 ng=0` (두 파일 각각 옛 꼴 `git diff --name-status --diff-filter=D <base>..<상한>` 0 · 새 꼴 `git diff --no-renames --name-status --diff-filter=D <base>..<상한>` 1 · `git status --porcelain --no-renames` 1) (b) 알려진 답 — `bash "$K/renlist.sh"` 두 줄이 `diff old=[] new=[keep/data.txt]` · `status old=[] new=[keep/two.txt]` (새 꼴 두 명령이 커밋한 이동 · 스테이징한 이동의 옛 경로를 D 로 낸다) [exact, enumerated]
- [ ] ER-06: 계약 스키마의 측정 예시 두 가지가 실패를 삼키지 않고, 서명 줄 도우미 설명이 실제 동작과 같다 — 커밋 구간 상한을 못 찾으면 `HEAD` 까지 재지 않고 멈추고, 봉인 상태 세기가 `verify_seal` · `fm_get` 정의 없이 돌면 「SEAL_BROKEN 0」 을 내지 않고 멈춘다. 서명 줄 설명은 「끝 문단의 한 줄만 인정」 대신 `mine` · `unsigned_on` 이 실제로 하는 일(메시지 어느 문단이든 글자가 똑같은 한 줄)을 적는다 (xdiag P2 계약 밖 1 · P3 (2) AR-06 ③ · 러닝북 측정 구멍 「셸 함수에 기대는 측정」 · Codex r1 4) — 측정: (a) `python3 "$K/toks.py" "$T/E" ER06` 끝줄이 `rows=4 ng=0` (옛 설명 ER06-O2 0 · 새 설명 ER06-N2 1 포함) 이고, `$T/E/harness/references/contract-schema.md` 에서 `app/lib ':(exclude)*.g.dart'` 가 든 줄과 `-- packages/server/lib` 가 든 줄이 각각 `U=$(sprint_head <slug>) || exit 2` 를 담는다(각 1) (b) 알려진 답 — `bash "$K/sealcnt.sh" "$T/E/harness/references/contract-schema.md" <셸> "$T/E"` 를 `bash` · `zsh` 로 돌리면 둘 다 `none rc=` · `no_fm_get rc=` 값이 0 이 아니고, `full rc=0` · `broken=` 빈 값 · `ok=` 1 이상 — 세는 대상은 끝 판(`$T/E`)의 `.harness/` 다. 다른 Final 계약이 동시에 쓰는 작업 폴더를 읽지 않는다 (시작 커밋 판 `$T/B` 는 `none rc=0` · `no_fm_get rc=0 absent=77` · `full rc=0 ok=67 absent=10`) (c) 상한 꼴 대조 — 실패하는 흉내 함수 `sprint_head(){ return 1; }` 아래 `U=$(sprint_head s) || exit 2; echo reached` 가 `bash -c` · `zsh -c` 둘 다 종료 코드 2 · `reached` 출력 없음 (옛 꼴 `git diff --name-only 04a0e76..$(sprint_head s)` 는 종료 코드 0 — 봉인 전 실측) (d) 알려진 답 — `bash "$K/sigline.sh" "$T/E/harness/references/contract-schema.md" bash` 와 `… zsh` 가 각각 `mine_last=1 mine_middle=1 mine_inline=0 unsigned=[inline.txt]` — 스키마 도우미가 끝 문단 서명과 가운데 문단 서명을 둘 다 서명으로 보고 문장 안 인용은 보지 않는다. ER06-N2 문장이 이 동작과 같다 (도우미는 바뀌지 않아 시작 커밋 판도 같은 값이다 — 음성 대조는 (a) 의 옛 설명 글자) [exact, enumerated]
- [ ] ER-07: 옛 값 검사가 킷 폴더까지 읽는다 — `.claude-plugin/marketplace.json` 의 킷 폴더 전부(backend-kit 제외)와 기존 소스 폴더 열둘을 합쳐 같은 파일을 두 번 세지 않고, 뺀 폴더는 출력에 `검사 제외: backend-kit — <이유>` 로 시작하는 줄(앞 공백 허용)로 적는다 (xdiag P3 (2) DG-05 (b) · P6 (2) 4 · P7 (2) · P8 (2) 3 · P9 (2) · phase10 · phase14 notes) — 측정: (a) 알려진 답 — `bash "$K/stale.sh" "$T/E"` 첫 줄이 `clean rc=0 files=<N> want=<N> excluded_line=1` 로 `files` 와 `want` 가 같고(`want` 는 도우미가 marketplace.json 킷 폴더(backend-kit 제외) ∪ 기존 열두 폴더 아래 `.md` 합집합을 따로 센 값), 둘째 줄이 `seeded rc=1 hits=5/5 other_owasp=0` — 사본의 `harness/agents/qa-evaluator.md` · `harness/evals/gate-exit-codes.md` · `react-kit/references/render-evidence-protocol.md` · `onboarding-kit/skills/setup-guide/SKILL.md` · `rust-kit/skills/rust-model/SKILL.md` 에 넣은 등록 옛 값을 전부 잡는다 (시작 커밋 판은 `files=133 want=389` · `seeded rc=0 hits=0/5`) (b) `python3 "$K/toks.py" "$T/E" ER07` 끝줄이 `rows=1 ng=0` (「docs-site 파이프라인 전용」 범위 한계 문장을 새 범위로 바꿈). 예외: (a) 첫 줄의 `rc` 가 1 이면 `cd "$T/E" && python3 scripts/check-stale-values.py` 를 다시 돌려, `되살아난 옛 값 N 건:` 아래 두 칸 들여 쓴 `<파일>:<줄>` 꼴로 찍힌 파일이 `my` 에 하나도 없을 때만 그 `rc` 를 PASS 로 본다 — 다른 계약이 넣은 옛 값이다. 이때도 `files` 와 `want` 가 같고 `excluded_line=1` 이어야 하며, 둘째 줄은 그대로 요구한다 [exact, enumerated]
- [ ] ER-08: 검증 스크립트가 실패한 검사의 V 줄에 판정을 적고, 사후 점검의 bare-fence 줄이 V6 판정을 종료 코드로 읽으며, 검증 가이드의 출력 예시가 새 V 줄 꼴과 같다 (xdiag P6 (2) 1 · final-todo 「validate-plugin 의 V3 · V4 · V5 · V9 실패가 V 줄에 FAIL 로 안 찍힘」 · 받는 쪽 대조에서 찾은 `check_bare_fence` 의 `"0 bare"` 부분 글자 판정 · REVIEW 검토 C1 의 가이드 예시) — 측정: (a) 알려진 답 — `bash "$K/vline.sh" "$T/E"` 가 `A vp_rc=2 v3569_fail_lines=4 unjudged=0 bare_fence=FAIL` · `B vp_rc=0 v3569_fail_lines=0 unjudged=0 bare_fence=PASS` 를 낸다 (A 는 harness 스킬 하나에 끊긴 링크 · `TODO` · `$1` · 언어 표시 없는 펜스를 넣은 사본 — V3 · V5 · V6 · V9 줄이 `— FAIL` 로 끝나고, 판정 글자 없이 끝나는 V 줄이 없다. B 는 원본 사본. 시작 커밋 판은 `A … v3569_fail_lines=0 unjudged=4 bare_fence=PASS`) (b) `cd "$T/E" && python3 scripts/validate-plugin.py harness` 의 `  V1` ~ `  V10` 열 줄이 모두 `— OK` 로 끝나고 종료 코드 0 (c) `type sect >/dev/null || exit 2;` 뒤 `sect "$T/E/harness/docs/guides/plugin-validation-guide.md" '### 출력 포맷' | grep -E '^  V[0-9]+ ' | grep -cvE '— (OK|WARN|FAIL|SKIP)$'` 이 0 이고, 같은 출력에서 `— FAIL` 로 끝나는 줄이 1 이상 (시작 커밋 판 2 · 0 — 실패 예시를 지워서 맞추는 길을 막는다) [exact, enumerated]

## Architecture

- [ ] AR-01: 문서 사이트 드리프트 검사가 api-kit · howto-kit · onboarding-kit 원본과 스킬 본문 `SKILL.md` 를 실제 페이지 이름으로 잇고, 같은 매핑을 사람이 읽게 적은 오케스트레이터 F2 표도 그 킷들을 담는다 (phase14-notes §넘기는 것 마지막 줄 · phase16-notes §넘기는 것 넷째 줄 · 같은 누락이 `docs/howto/` 에도 있다 · phase12-notes 가 믿은 `reflect-kit/skills/` 매핑이 `SKILL.html` 로 간다 — 편집 전 감사 · REVIEW 검토 C2) — 측정: (a) 알려진 답 — `bash "$K/drift.sh" "$T/E"` 가 열세 줄과 끝줄 `rc=0` 을 내고, 열세 줄이 차례로 정확히 `onboarding-kit/skills/setup-guide/SKILL.md → docs/onboarding-kit/setup-guide.html` · `onboarding-kit/skills/setup-guide/references/format-checklist.md → docs/onboarding-kit/format-checklist.html` · `onboarding-kit/skills/setup-guide/references/project-detection.md → docs/onboarding-kit/project-detection.html` · `docs/onboarding-kit/examples/fcm-ios-setup-guide.md → docs/onboarding-kit/fcm-ios-example.html` · `docs/api/execution/probe-synthesis-hurl-semantics.md → docs/api-kit/probe-synthesis-hurl-semantics.html` · `docs/api/execution/auth-secret-lifecycle.md → docs/api-kit/auth-secret-lifecycle.html` · `docs/api/contract/snapshot-sealing-canonicalization.md → docs/api-kit/snapshot-sealing-canonicalization.html` · `docs/api/contract/contract-extraction-modes.md → docs/api-kit/contract-extraction-modes.html` · `docs/api/verification/regression-diff-failure-policy.md → docs/api-kit/regression-diff-failure-policy.html` · `docs/api/verification/static-evidence-viewer-contract.md → docs/api-kit/static-evidence-viewer-contract.html` · `docs/howto/deep-links.md → docs/howto-kit/deep-links.html` · `reflect-kit/skills/codex-kaizen/SKILL.md → docs/reflect-kit/codex-kaizen.html` · `bambu-kit/skills/bambu-print-profile/SKILL.md → docs/bambu-kit/bambu-print-profile.html` 이다(어느 줄에도 `[NEW` 없음). 시작 커밋 판은 열한 줄이 `(없음)` 이고 codex-kaizen 줄이 `docs/reflect-kit/SKILL.html  [NEW …` (b) 오케스트레이터 Step F2 「소스 → 출력 매핑」 표 — `bash "$K/f2map.sh" "$T/E/.claude/skills/kaizen-orchestrator/SKILL.md"` 출력이 정확히 `reflect-kit=1 bambu-kit=1 onboarding-kit=1 howto-kit=1 api-kit=1 planning_refs=0` (출력 칸이 `docs/<킷>/` 인 행이 넷 킷에 하나씩 있고, 없는 `planning-kit/references/` 가 표에서 빠졌다. `api-kit=1` 은 이미 있는 행이 셈에 걸리는지 보는 양성 대조. 시작 커밋 판 `reflect-kit=0 bambu-kit=0 onboarding-kit=0 howto-kit=0 api-kit=1 planning_refs=1`) [exact, enumerated]
- [ ] AR-02: CI 가 Phase notes 가 넘긴 새 시험 여섯을 돈다 (phase10 · phase12 · phase14 · phase17 notes §넘기는 것 · final-todo 「CI 줄 옮길 때 주의」) — 측정: (a) `python3 "$K/ci.py" "$T/E/.github/workflows/ci.yml"` 끝줄이 `placed=7/7 zsh_first=1` — `validate` 작업에 `run:` 값이 정확히 `bash react-kit/evals/scripts/project-detect-test.sh` · `bash reflect-kit/evals/hooks/log-reflection-test.sh` · `bash reflect-kit/evals/hooks/project-id-test.sh` · `bash reflect-kit/evals/hooks/collect-status-test.sh` · `sh onboarding-kit/skills/setup-guide/evals/run-gate-evals.sh` · `sh howto-kit/evals/run-evals.sh` 인 단계가 하나씩, `command -v zsh >/dev/null || { sudo apt-get update && sudo apt-get install -y zsh; }` 인 단계가 하나 있고 그 단계가 여섯 시험 단계 모두보다 앞에 있다 — reflect-kit 시험 둘은 zsh 가 없으면 zsh 경우를 건너뛰고 통과한다 (b) `grep -cF '\|\|' "$T/E/.github/workflows/ci.yml"` 이 0 이고 `actionlint "$T/E/.github/workflows/ci.yml"` 종료 코드 0 (c) `cd "$T/E"` 에서 여섯 명령을 각각 돌리면 모두 종료 코드 0 이고 끝줄이 차례로 `결과: <N> 경우 중 불일치 0` 꼴 넷(N ≥ 1)과 `EVALS_PASS` 둘. 예외: 어느 명령이 종료 코드 0 이 아니면, 그 명령이 도는 킷 폴더(`react-kit/` · `reflect-kit/` · `onboarding-kit/` · `howto-kit/` 가운데 명령 경로의 첫 칸)를 구간 안에서 바꾼 커밋이 전부 `Kaizen-Phase: kaizen-0924-f1-kit-followups` 서명이고 — `git log --format=%H "$B..$END" -- <킷 폴더> | while read -r c; do git log -1 --format=%B "$c" | grep -qxF 'Kaizen-Phase: kaizen-0924-f1-kit-followups' || echo "$c"; done | grep -c .` 이 0 — `cd "$T/B"` 에서 같은 명령이 종료 코드 0 일 때만 이 계약 몫이 아닌 것으로 본다(kit-followups 가 같은 때에 고치는 파일이다) [exact, enumerated]
- [ ] AR-03: 오케스트레이터 자동 생성 구간의 킷 범위 줄이 실제로 있는 참조 폴더만 적는다 — 킷 바로 아래 `references/` 가 있으면 그것, 없고 `skills/*/references/` 가 있으면 그것, 둘 다 없으면 참조 폴더를 적지 않는다 (phase14-notes §미반영 키와 사유 마지막 줄) — 측정: (a) `bash "$K/orch.sh" "$T/B" "$T/E"` 첫 줄에 `auto_removed=3 auto_added=3` 이고 더한 세 줄이 정확히 ``**범위:** `planning-kit/skills/*/SKILL.md` `` · ``**범위:** `bambu-kit/skills/*/SKILL.md`, `bambu-kit/skills/*/references/` `` · ``**범위:** `onboarding-kit/skills/*/SKILL.md`, `onboarding-kit/skills/*/references/` `` (끝 공백 없음) (b) `cd "$T/E" && python3 scripts/sync-orchestrator.py --check-only` 종료 코드 0 (c) `python3 "$K/toks.py" "$T/E" AR03` 끝줄이 `rows=1 ng=0` (오케스트레이터 SKILL.md 에 `onboarding-kit/references/` 0) [exact, enumerated]
- [ ] AR-04: 고치지 않은 입력 항목을 notes 의 다음 사이클 메모로 넘기고, Final 이 옮겨 적을 커밋 목록 · 두 단락을 남긴다 (final-runbook 「넘김 항목 가운데 고치지 않기로 한 것은 … 다음 사이클 메모로 남긴다」 · 「followups notes 의 커밋 sha 를 옮겨 적는다」) — 측정: `$T/E/$NOTES` 에 (a) 제목 줄 `## 커밋` · `## changelog 한 단락` · `## 킷 로그 한 단락` · `## 다음 사이클 메모` 가 각각 1 — 제목마다 `grep -cxF '<제목>' "$T/E/$NOTES"` 이 1 (b) `sect "$T/E/$NOTES" '## 다음 사이클 메모'` 출력에 `범위 경계` 절 입력 표의 `고치지 않음` ID 스물아홉 `F1H-14` · `F1H-35` · `F1H-37` · `F1H-38` · `F1H-39` · `F1H-40` · `F1H-41` · `F1H-43` · `F1H-44` · `F1H-47` · `F1H-48` · `F1H-56` · `F1H-58` · `F1H-59` · `F1H-60` · `F1H-65` · `F1H-66` · `F1H-67` · `F1H-76` · `F1H-77` · `F1H-78` · `F1H-79` · `F1H-80` · `F1H-81` · `F1H-82` · `F1H-84` · `F1H-91` · `F1H-92` · `F1H-94` 가 각각 1 줄 이상 (c) `git log --format=%h "$B..$END" --grep="^$SIG\$"` 가 낸 짧은 sha 가운데 `$END` 자신(notes 커밋)을 뺀 전부가 `sect "$T/E/$NOTES" '## 커밋'` 출력에 있다 [exact, enumerated]
- [ ] AR-05: 이 계약의 변경이 허용 경로 안에 머물고 이 계약이 봉인돼 있다 — Given: 이 계약의 커밋이 끝난 뒤. 측정: (a)(b)(d) 앞에 `type my unsigned_on verify_seal >/dev/null || exit 2;` 를 둔다 (a) `my` 의 모든 줄이 공통 정의 `FILES` 서른하나 · `MYHARNESS` 다섯 가운데 하나 — `my | grep -vxF -f <(printf '%s\n' "${FILES[@]}" "${MYHARNESS[@]}") | grep -c .` 이 0 (b) `unsigned_on "$B" "$END" "$SIG" "${FILES[@]}" | grep -c .` 이 0 — 서명 없이 서른한 파일을 건드린 구간 안 커밋이 없다 (c) 구간 안 커밋 가운데 알려진 두 서명(`Kaizen-Phase: kaizen-0924-f1-harness-followups` · `Kaizen-Phase: kaizen-0924-f1-kit-followups`) 어느 것과도 글자가 같은 줄이 없는 커밋이 `.harness/` 밖 파일을 건드린 수가 0 — 서명 글자를 잘못 적은 커밋도 잡는다. `git log --format=%H "$B..$END" | while read -r c; do git log -1 --format=%B "$c" | grep -qxE 'Kaizen-Phase: kaizen-0924-f1-(harness|kit)-followups' && continue; git show --name-only --format= "$c" | grep -v '^\.harness/' | grep -c .; done | awk '{s+=$1} END{print s+0}'` 이 0 (d) `verify_seal "$T/E/$CF"` 가 `SEAL_OK` 이고 `find "$T/E/.harness" -type f -name 'sprint-contract*.md' -print0 | while IFS= read -r -d '' f; do verify_seal "$f"; done | grep -c '^SEAL_BROKEN'` 이 0 — 봉인 상태는 끝 판 커밋에 든 계약 파일로 잰다 (e) 봉인 커밋(`git log --format=%H "$B..$END" --grep='^contract: kaizen-0924-f1-harness-followups 봉인'` 의 마지막 줄)의 `git show --name-only --format=` 가 정확히 `$CF` 한 줄 (f) 공유 파일을 건드린 구간 안 커밋을 서명과 상관없이 직접 센다(러닝북 「건드리면 안 되는 파일은 … 직접 센다」). kit-followups 서명 커밋은 그 계약 몫이라 뺀다 — `git log --format=%H "$B..$END" -- .claude-plugin/marketplace.json ':(glob)*/.claude-plugin/plugin.json' README.md CLAUDE.md ':(glob)docs/**/*.html' ':(glob)docs/kaizen/**' .claude/kaizen-input/insights-report.md .harness/.meta/orchestrator-audit-log.md .harness/.meta/kaizen-failure-count.yaml .harness/stale-values.yaml ':(glob).claude/skills/docs-site/**' | while read -r c; do git log -1 --format=%B "$c" | grep -qxF 'Kaizen-Phase: kaizen-0924-f1-kit-followups' || echo "$c"; done | grep -c .` 이 0. `docs/*/research-log.md` 는 kit-followups 가 고치는 파일이라 넣지 않는다. 양성 대조: `c=$(git log -1 --format=%H -- .claude-plugin/marketplace.json)` 로 `"$c~1..$c"` 구간에 같은 경로 목록을 주면 1 이상 (봉인 전 실측) [exact, enumerated]

## Anti-patterns

- [ ] AP-01: 버전을 하드코딩하지 않는다 — plugin.json에서 읽어야 한다. 이번 변경에 적용: 서른한 파일에 더한 줄 가운데 `harness/evals/` 아래 시험 파일을 뺀 줄에 버전꼴 문자열(`[0-9]+\.[0-9]+\.[0-9]+`)이 0 줄. 측정: `for f in "${FILES[@]}"; do case $f in harness/evals/*) continue ;; esac; git diff --no-index -U0 "$T/B/$f" "$T/E/$f"; done | grep '^+' | grep -v '^+++' | grep -cE '[0-9]+\.[0-9]+\.[0-9]+'` 이 0. 양성 대조: 사본 `harness/README.md` 에 `v9.8.7` 한 줄 → 1 (봉인 전 실측) [exact]
- [ ] AP-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수 (```` ```text, ```bash, ```yaml ```` 등). 판정 권위는 validate-plugin V6 상태기계다 — 여는/닫는 fence 가 동형이라 줄 단위 정규식으로는 판정 불가. 이번 변경에 적용: V6 는 `.claude/skills/` · `harness/docs/guides/` 를 읽지 않으므로 DG-02 (a) 의 비교 출력에 `MD040` 새 묶음이 0 이고, `cd "$T/E" && python3 scripts/validate-plugin.py harness --check=code-fence` 의 종료 코드가 0 이고 V6 줄이 `0 bare — OK` — 러닝북대로 V 줄 글자보다 종료 코드를 먼저 본다 (시작 커밋 판 종료 코드 0 · `0 bare — OK`) [exact]
- [ ] AP-04: SKILL.md / agents/*.md frontmatter 에서 name 필드 누락 — validate-plugin V1 FAIL. 이번 변경에 적용: 고친 SKILL.md 열하나(`.claude/skills/kaizen-orchestrator` · `tone-kaizen` · `howto-kaizen` · `onboarding-kaizen` · `rust-kaizen` · `infra-kaizen` · `backend-kaizen` · `design-kaizen` · `react-kaizen` · `harness/skills/sprint-contract` · `harness/skills/create-agent`)의 첫 frontmatter 블록에 `name: <폴더 이름>` 줄이 1 개씩, `harness/agents/qa-evaluator.md` 에 `name: qa-evaluator` 1 개 — 측정: `awk 'NR==1 && /^---[[:space:]]*$/ { fm=1; next } fm && /^---[[:space:]]*$/ { exit } fm' <파일> | grep -cx "name: <이름>"` 이 열두 파일 모두 1 [exact, enumerated]

## Reusability

- [ ] RE-01: 다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다. 이번 변경에 적용: 파이썬 다섯 파일에 더한 줄에 밑줄로 시작하는 새 함수(`def _`)가 0 — 드리프트 검사의 이름 규칙 · 옛 값 검사의 킷 폴더 목록을 모듈 최상위 이름으로 두어 시험과 다른 스크립트가 같은 값을 읽는다. 측정: `for f in "${PYS[@]}"; do git diff --no-index -U0 "$T/B/$f" "$T/E/$f"; done | grep -cE '^\+[[:space:]]*def _'` 이 0 [exact]
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다. 이번 변경에 적용: (a) 커밋 안전 훅은 새 함수를 많아야 하나 더하고(`grep -cE '^[a-z_]+\(\) *\{' "$T/E/harness/scripts/commit-guard.sh"` 가 13 이하 — 시작 판 12) 막을 때 기존 `block` 을 부르며, 피드백 저장 스크립트는 기존 `identity_root_of` 를 고쳐 함수 수가 그대로다(`save-feedback.sh` 7) (b) 사후 점검의 `check_bare_fence` 가 V6 판정을 다시 짜지 않고 `validate-plugin.py --check=code-fence` 결과를 쓴다 — `awk '/^def check_bare_fence/{f=1} f && /^def / && !/check_bare_fence/{exit} f' "$T/E/scripts/validate-post-kaizen.py"` 출력에 `--check=code-fence` 1 줄 이상 · `"0 bare" in out` 0 (시작 판 0 · 1) (c) 옛 값 검사가 킷 목록을 새로 적지 않고 `marketplace.json` 에서 읽는다 — `grep -cF 'marketplace.json' "$T/E/scripts/check-stale-values.py"` 가 1 이상 (시작 판 0) [exact]

## Diagnostics

- [ ] DG-01: N/A (`commands.analyze` 는 `bash -n scripts/release.sh` 라 `scripts/release.sh` 만 잰다 — 이번 변경 파일과 교집합 0 개. 측정: `type my >/dev/null || exit 2;` 뒤 `my | grep -c '^scripts/release.sh$'` 이 0. 양성 대조: 같은 `grep -c` 에 `scripts/release.sh` · `scripts/release.sh.bak` 두 줄을 넣으면 1. 실제 분석은 DG-02 · DG-05)
- [ ] DG-02: IDE diagnostics 워닝/인포 0개 (`diagnostics.ide_exclude` 값 `[]`) — 이번 변경에 적용: (a) 마크다운 스물한 파일(`MDS`)을 편집기 마크다운 확장과 같은 조건(markdownlint-cli2 0.23.2 · MD013 끔)으로 재어 파일마다 (규칙, 그 줄 글자) 묶음이 편집 전 판보다 늘지 않았다 — `bash "$K/mdcmp.sh" "$T/B" "$T/E" "${MDS[@]}"` 끝줄 `new_total=0` (더한 줄 옆 손대지 않은 줄에 붙는 MD022 · MD024 · MD032 도 잡는다) (b) 셸 네 파일(`SHS`) — `bash "$K/shcmp.sh" "$T/B" "$T/E" "${SHS[@]}"` 끝줄 `new_total=0` (c) 파이썬 다섯 파일(`PYS`)이 `python3 -W error -m py_compile "$T/E/<파일>"` 로 종료 코드 0 (d) `.github/workflows/ci.yml` 은 AR-02 (b) 의 actionlint. 편집 전부터 있던 경고는 `범위 경계` 절에 적은 대로 범위 밖이다. 양성 대조: 시작 판 사본의 `harness/README.md` 끝에 맨 URL 한 줄, tone-kaizen SKILL.md 끝에 언어 표시 없는 펜스를 넣으면 (a) 가 `new_total=2`(MD034 · MD040), `save-feedback.sh` 에 `echo $1` 한 줄을 넣으면 (b) 가 `new=1` (봉인 전 실측) [exact]
- [ ] DG-03: N/A (`commands.test` 는 `bash scripts/release.sh 2>&1 || true` 라 `scripts/release.sh` 만 잰다 — 교집합 0 개. 측정: DG-01 과 같은 명령 `type my >/dev/null || exit 2;` 뒤 `my | grep -c '^scripts/release.sh$'` 이 0. 실제 시험은 ER-01 · ER-02 · AR-02 (c))
- [ ] DG-04: N/A (구동할 앱 · 서버가 없다 — 훅 · 스크립트 · 문서뿐이고 ER-01 · ER-02 · ER-07 · ER-08 · AR-01 이 시험 저장소 · 사본에서 실제로 돌린다. 측정: `type my >/dev/null || exit 2;` 뒤 `my | grep -cE '\.(dart|ts|tsx|js|rs|go)$'` 이 0. 양성 대조: 같은 `grep -cE` 에 `a/b.dart` · `c.ts` · `d.md` 세 줄을 넣으면 2)
- [ ] DG-05: 저장소 검사 · 사후 점검이 이 계약 파일을 문제로 가리키지 않는다 — (a) `cd "$T/E"` 사본에서 `python3 scripts/validate-plugin.py` 종료 코드 0 — 0 이 아니면 `FAIL` 로 시작하는 상세 줄의 파일이 `my` 에 하나도 없을 때 PASS (다른 계약 몫) (b) 같은 사본에서 `python3 scripts/sync-docs.py --check-only` · `python3 scripts/sync-evals.py --check-only` · `python3 scripts/run-evals.py` · `python3 scripts/validate-doc-contracts.py` · `python3 scripts/sync-orchestrator.py --check-only` 가 모두 종료 코드 0 (c) 셸 네 파일(`SHS`)이 `bash -n` · `/bin/bash -n` 둘 다 종료 코드 0 (d) Given: 작업 폴더 HEAD 가 `$END` 이거나 그 자손 — `python3 scripts/validate-post-kaizen.py --since 5b4fd72d5587c937c1875ddb62872f32ae087dcf` 출력의 `scope-isolation` · `doc-contracts` · `bare-fence` 줄이 `FAIL` · `ERROR` 가 아니다. `docs-site-regen` 은 `kaizen-0924-final` F2 몫이라 판정에서 뺀다. 다른 계약 커밋 때문에 `scope-isolation` 이 FAIL 이면 `--verbose` 위반 커밋 목록에 이 서명 줄 커밋이 없을 때, `bare-fence` 가 FAIL 이면 `python3 scripts/validate-plugin.py --check=code-fence` 의 `FAIL` 줄 파일이 `my` 에 없을 때 PASS. `check-stale-values.py` 는 ER-07 이 잰다 [exact]
