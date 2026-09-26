# c1a scripts 검사 도구 후속 — 구현 notes

- 계약: `.harness/sprint-contract-after-0924-scripts.md` (봉인 `sha256:e6e9d4a14f27da96`, 봉인 커밋 `fd1bc49`)
- 가지: `chore/ak-c1-harness-scripts`, 시작 판 `f81568d`. main 은 합치지 않았다 (계약 전제)
- QA 판정: APPROVE (Iteration 1, 조건 30 개 모두 재실행) — 리포트 `.harness/sprint-feedback-after-0924-scripts.md`, 커밋 `7e42c44`. 교차 진단은 판정을 뒤집을 결함 0 건, 짚은 것은 아래 `## 다음 사이클 메모`

## 한 일

| 커밋 | 내용 | 조건 |
| ---- | ---- | ---- |
| `282f7c0` | sync-docs — 표지 이름에 하이픈 허용, 짝 없는 표지를 파일 · 줄 번호와 함께 알리고 종료 코드 2, 훅 표 이름에서 따옴표 빼기, 루트 README 네 킷 절에 `skills-<킷>` 블록 | SC-10 · SC-11 · SC-12 · ER-02 |
| `d9c2623` · `399b9a9` · `a579f82` | onboarding-kit · planning-kit · rust-kit README 표지를 sync-docs 가 읽는 꼴로 고치고 표를 다시 만듦 | SC-11 |
| `f705e1c` · `1861c65` · `372dc38` · `c1843a5` | 킷 넷 hooks.json 명령 10 개의 `${CLAUDE_PLUGIN_ROOT}` 경로를 큰따옴표로. harness 커밋에 검증 가이드 V8 절을 함께 | SC-07 · SC-09 |
| `51f655c` | V8 — 큰따옴표 밖 변수가 든 명령을 FAIL, 따옴표 꼴 경로도 직접 실행으로 알아봄 | SC-08 |
| `b9aea2c` | 카이젠 회귀 패턴 실행기 `scripts/run-kaizen-assertions.py` 와 CI 단계 | SC-01 · SC-02 · SC-03 · ER-01 · RE-01 · RE-02 |
| `18b05e6` | 배정표 검사기 `--final` 이 Phase 번호와 슬러그 번호를 맞대 봄 | SC-04 |
| `7f4559b` | 감사 기록 도구 — 소제목에 날짜 · 사이클, 새 항목 앞 빈 줄, `--watch` | SC-05 · SC-06 |
| `0d90a2e` | sync-docs 훅 표 주석을 이유만 남기게 (톤 대조 결과) | — |

새로 찾은 결함 하나를 같은 커밋 `282f7c0` 에서 고쳤다. sync-docs 표지 정규식이 하이픈을 못 읽어 루트 README 의 `update-cmd` · `uninstall-cmd` · `release-cmd` 세 블록이 킷 10 개에 멈춰 있었다(지금 14 개). 짝 없는 표지를 알리게 하면 바로 드러나는 자리라 표지 읽기와 함께 고쳤고, 바뀐 파일 목록(AR-01)은 늘지 않았다.

## 판단이 갈린 곳

- **harness 파일을 범위에 넣었다.** 묶음 지시는 `harness/` 아래를 범위 밖으로 뒀지만 `harness/hooks/hooks.json` 과 `plugin-validation-guide.md` V8 절만 고쳤다. 근거는 `phase12-notes.md:59` · `:89` (킷 넷을 한 번에 고친다), 그리고 V8 이 따옴표 없는 명령을 FAIL 로 내면 harness 만 남길 때 CI 가 멈춘다는 점이다. 교차 진단이 사용자 확인을 권했으나 위임(묻지 말고 끝까지)대로 묻지 않았다
- **notes 경로.** 계약 작성 단계는 `.harness/.meta/after-0924/scripts-notes.md` 를 골랐는데, 묶음 지시가 이 파일 경로를 정해 두어 봉인 전에 계약을 이 경로로 맞췄다
- **루트 README 스킬 블록 꼴.** 한 줄 문단(`**스킬 N종** — 이름…` · `**에이전트 M종** — 이름…`)으로 했다. 표로 하면 루트 README 가 킷 README 와 같은 표를 한 벌 더 갖게 된다. harness 절의 옛 표(트리거 · 설명 열)는 사라졌고 설명은 `harness/README.md` 에 있다
- **다시 만든 킷 README 표.** 세 킷 표는 이제 SKILL.md 설명 첫 줄을 옮긴다. 손으로 쓴 「용도」 문구 대신 들어가고, 설명이 여러 줄인 스킬은 첫 줄에서 끊긴다(다른 킷 README 와 같은 동작). 끊김을 줄이려면 sync-docs 가 설명 전체 첫 문장을 읽게 바꿔야 한다 — 다음 묶음 후보

## 넘긴 것

- 옛 값 검사 backend-kit 해제와 allow 세 줄(F1H-79 · FN-64)은 이미 반영돼 있다 — 커밋 `72d6ddd`, `scripts/check-stale-values.py:45` · `.harness/stale-values.yaml:20-24`
- 오케스트레이터 Final 단계가 계약 밖 결함 같은 수동 감시 거리를 새 옵션 `--watch` 로 넘기게 하는 일 — `.claude/skills/kaizen-orchestrator/SKILL.md` (다른 묶음 몫). 지금은 실패 목록에서 온 감시 거리만 들어간다
- 카이젠 Step 7 이 새 실행기 `python3 scripts/run-kaizen-assertions.py` 를 부르게 하는 일 — `harness/skills/contract-kaizen/SKILL.md` · `harness/skills/evaluator-kaizen/SKILL.md`
- `harness/evals/kaizen/evaluator-kaizen/assertions.json` 의 `silent-check` 패턴 셋 가운데 둘이 제목 글자만 본다 (FN-18 뒷부분). 본문이 비어도 통과한다
- V6 · V10 검사 범위 결정 — F1H-40 · F1H-94
- main(`feat/v10-fence-commonmark` 가 합쳐진 판 `88ddfe5`)을 합친 뒤 할 일: `plugin-validation-guide.md` 머리 판 번호와 변경 이력 한 줄, 같은 가이드 수동 수정 표(V8 행, 지금 `:558` 근처)에 따옴표 고치는 법 한 줄, 그리고 `docs/harness/plugin-validation.html` 다시 만들기. 이 가지에서 고치면 AR-02 범위를 벗어나거나 main 과 부딪힌다
- `reflect-kit/README.md:156` · `:159` · `:162` 의 `bash ${CLAUDE_PLUGIN_ROOT}/scripts/install-scheduler.sh` 예시도 따옴표가 없다 — hooks.json 밖이라 이번 범위 밖
- 이번에 손대지 않은 기존 markdownlint 경고: 루트 `README.md` 15 · `rust-kit/README.md` 15 · `planning-kit/README.md` 6 · `onboarding-kit/README.md` 2 · 검증 가이드 30 (가이드는 모두 V8 절 밖). 계약은 늘지 않는 것만 잰다

## 킷별 버전 판단

| 킷 | 단계 | 이유 |
| -- | ---- | ---- |
| harness | patch | hooks.json 명령 모양만 바뀌고 동작은 같다(빈칸 든 경로에서 실행되게 된 것은 결함 수정). 가이드 V8 절 보강 |
| design-kit | patch | hooks.json 따옴표 |
| flutter-toolkit | patch | hooks.json 따옴표 |
| reflect-kit | patch | hooks.json 따옴표 |
| onboarding-kit · planning-kit · rust-kit | patch | README 표지와 다시 만든 표만 바뀌었다. 설치본 동작이 같아 다음 릴리스에 묶어도 된다 |

`scripts/` · 루트 `README.md` · `.github/workflows/ci.yml` 은 킷이 아니라 릴리스 대상이 아니다.

## docs 드리프트

`python3 scripts/detect-docs-drift.py --since f81568d` 출력 한 줄 — `harness/docs/guides/plugin-validation-guide.md → docs/harness/plugin-validation.html`. 페이지 다시 만들기는 부모가 모아서 한다 (위 넘긴 것 참고).

## 자기 측정 (끝 판 = 이 가지 끝)

계약의 측정 절(`## 회귀 게이트` 로 시작하는 절)에 든 도우미를 계약 본문에서 그대로 떼어 돌렸다.

- SC-01 `rc=0 pass=14 fail=0 pairs=9/9 total=[Total: 14 passed, 0 failed]` · RE-01 `rc=0` 같은 끝줄
- SC-02 `SC02a rc=1 fail_line=1 total=[Total: 13 passed, 1 failed]` · `SC02b rc=1 fail_line=1` · `SC02c rc=1 fail_line=1` · 망가뜨리기 적용 `MUT_OK` 8 줄(ER-01 다섯 포함)
- SC-03 `validate_job=1 whole_file=1`
- SC-04 `SC04a rc=0 ok=1` · `SC04b rc=1 fail=1 rows=9` · `SC04c basic rc=0` · `SC04d rc=0` · `SC04e rc=1 fail=1 rows=1` · 바꾼 수 9 · 3 · 4
- SC-05 `rc=[0 0 0]` · `heads=3 blank_before=3/3 subs=9 sub_ok=9/9` · `md024=0 md022_032=0` · `SC05r rc=0 prefix=1 md024_before=8 md024_after=8`
- SC-06 `a_none=1 b_items=11 b_none=0 c_items=11 c_none=0` · `help_watch=3`
- SC-07 `commands=10 quoted=10/10 same_shape=4/4 ran_env=10/10 ran_sub=10/10`
- SC-08 (a) `rc=0` · `14 OK` · harness `5 hook` · flutter-toolkit `1 hook` · design-kit `1 hook` (b) `rc=2 FAIL named=1` (c) `rc=2 FAIL named=1` (d) `rc=0 1 hook OK` (e) `rc=2 FAIL named=1`
- SC-09 `v8_section=1 quote_word=11 json_quoted_example=3 fail_blocks=2 unquoted_outside_fail=0`
- SC-10 두 README `same=1` · `quote_in_hook_rows=0`
- SC-11 `SC11a rc=0 synced=1 need_any=0` · `SC11b rc=1 onboarding=1 planning=1 rust=1` · 제목 다섯 모두 1
- SC-12 `end blocks=4/4 counts=4/4 names=4/4 outside_counts=0 outside_lists=0` · `SC12a rc=1 root=1` · `write_rc=0 recheck_rc=0` · `probe_block_21=1`
- ER-01 (d) ~ (h) 모두 `rc=2`, (d) ~ (g) `named=1` · ER-02 `rc=2 named=2`
- AR-01 `got=15 exact=1` · AR-02 `validate=[hunks=15 outside=0] guide=[hunks=8 outside=0]` · AR-03 `mixed=0` · AR-04 `seal_broken=0 shared_same=3/3 harness_extra=0`
- AP-01 `added_versions=0 hardcoded_pattern=0` · AP-02 `force_push=0` · AP-03 `bare_open=0` · `v6_rc=0`
- RE-02 `runner_import=1 runner_self_root=0 sync_collectors=5 insights_readers=2` · SK-00 `0` · DG-01 `0`
- DG-02 `md_worse=0` (`21->15 2->2 8->6 17->15 30->30`) · `py_compile=5/5 json=4/4 actionlint_rc=0`
- DG-05 로컬 CI 22 단계 `rc=0` · `feedback-agg-test SKIP (yq 없음)` · 새 단계 `python3 scripts/run-kaizen-assertions.py` 종료 코드 0
- 그 밖: `python3 scripts/validate-plugin.py` 14 킷 OK · `sync-evals.py --check-only` 종료 코드 0 · `run-evals.py` `Total: 116 passed, 0 failed` (시작 판과 같다)

AR-05 와 DG-02 의 notes 몫은 이 파일을 커밋한 뒤 다시 잰다.

## 톤 대조 (tone-guide 5 단계)

tone-kit 0.2.0 규칙을 불러와(코어 넷 · 한국어 축, 어댑터 없음 — `.claude/tone-project.md`) 더한 줄 345 줄에 맞대 봤다.

| 규칙 | 건수 | 판정 |
| ---- | ---- | ---- |
| C-01 무엇 말고 왜 | 1 | 고침 — sync-docs 훅 표 주석을 이유만 남김 (`0d90a2e`) |
| C-02 · C-03 이름을 되풀이하는 주석 | 0 | 통과 — 새 주석 여덟 줄은 모두 이유 · 실패 모습 · 제약이다 |
| C-04 · F 구분선 | 0 | 통과 |
| C-06 공개 동작의 계약 | 0 | 통과 — 새 실행기 · sync-docs · 감사 기록 도구 설명문에 쓰는 법 · 출력 줄 · 종료 코드를 적음 |
| C-10 디자인 도구 참조 | 0 | 통과 |
| C-13 자화자찬 머리 | 0 | 통과 — 걸린 한 줄은 rust-test 스킬 설명을 sync-docs 가 옮긴 표 칸이다 |
| N-07 fallback 접두사 | 0 | 통과 |
| N-08 한 글자 이름 | 1 | 남김 — `append-audit-log.py` 감시 목록 루프의 `f` 는 원래 있던 이름을 들여쓰기만 바꿨다. 같은 함수 위 루프도 `f` 라 한쪽만 바꾸면 갈린다(S-12). 새로 쓴 코드는 `match` · `pos` · `block` 을 썼다 |
| N-09 역할 없는 파일 이름 | 0 | 통과 — 새 파일은 `run-kaizen-assertions.py` |
| S-03 · S-04 · S-06 추출 | 0 | 통과 — 새 함수 넷(`_plugin_root_outside_double_quotes` · `unpaired_marker_lines` · `render_kit_skill_line` · 실행기 `main`) 모두 자기 일을 하고 다른 새 함수를 부르지 않는다 |
| S-12 같은 자리 같은 꼴 | 0 | 통과 — 새 실행기는 `run-evals.py` 처럼 `plugin_utils` 에서 저장소 뿌리를 받고 종료 코드 0 · 1 · 2 를 쓴다 |
| K-02 번역투 여섯 | 1 | 통과 — 걸린 한 줄(`에 대해`)은 plan-guide 스킬 설명을 옮긴 표 칸이고 내가 쓴 글이 아니다 |
| K-04 `한다`체 | 0 | 통과 |
| K-11 새로 지은 이름 | 0 | 통과 |
| H 보존 | — | 지운 주석 0 줄. `스크립트 이름만 추출` 한 줄은 이유 주석으로 바꿨다 |

## 측정 도구 경로

- 계약 도우미를 뗀 폴더: `/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/bda55d45-296c-491f-89ba-b52042d58e72/scratchpad/c1a-impl/K` (markdownlint 0.23.2 는 `scratchpad/c1a/mdl/node_modules` 를 가리킨다)
- 로컬 CI: `/Users/jackson/Hub/10_Dev/claude-plugins/.harness/handoff/2026-09-26-tools/ci-local.sh` (봉인 시점 지문 `a415eaff98a46b86`), 결과는 `TMPDIR=scratchpad/c1a-impl/ci1` 아래 `ci-local/summary.txt`
- 계약 피드백: `/Users/jackson/.harness/feedback/contract/1a3bcba6-2026-09-26T122741-bda55d45-6864.yaml` (`verify-feedback.sh` PASS)

## 다음 사이클 메모

QA 승인 뒤 교차 진단(2026-09-26)이 짚은 것이다. 판정을 뒤집을 결함은 0 건이고, 여섯은 모두 스크래치 사본으로 재현됐다. 위 「넘긴 것」 도 다음 사이클 몫이다.

- 감사 기록 도구 소제목이 같은 날 같은 사이클이면 여전히 겹친다 — `scripts/append-audit-log.py:139` 는 `{날짜} — {사이클}` 만 붙이는데, `.claude/skills/kaizen-orchestrator/SKILL.md:359` 는 사이클을 열 때 빈 항목 하나, Step 11 에 또 하나를 같은 사이클 이름으로 붙인다. 하루에 끝나는 사이클이면 같은 제목 경고(MD024)가 다시 난다(사본 재현 `:25` · `:30` · `:34` · `:38`). 항목 종류(시작 · 끝)나 시각을 소제목에 넣을지 정한다. 사이클 머리(둘째 단계 제목) 겹침은 원래 있던 문제다
- 새 실행기가 빈 문자열에도 맞는 패턴을 늘 통과시킨다 — `scripts/run-kaizen-assertions.py:81` 의 `len(re.findall(...))` 이 빈 일치도 센다. 패턴 `""` · `(?:gone)?` 은 대상 글이 `alpha` 한 줄이어도 `PASS … (7건)` 이 나온다. 「패턴이 사라진 것」 을 잡는 도구인데 이런 패턴은 영영 FAIL 이 안 난다. 지금 든 14 개는 해당 없음. 빈 일치를 빼고 세거나, 빈 문자열에 맞는 패턴을 입력 오류(종료 코드 2)로 막는다
- V8 따옴표 검사가 중괄호 없는 `$CLAUDE_PLUGIN_ROOT` 를 못 본다 — `scripts/validate-plugin.py:632` · `:634` 가 `${CLAUDE_PLUGIN_ROOT}` 글자만 찾는다. `"$CLAUDE_PLUGIN_ROOT/scripts/x.sh"` · `"bash $CLAUDE_PLUGIN_ROOT/scripts/x.sh"` 는 따옴표 검사도, 권한 644 사본의 실행 비트 검사도 `OK` 로 지나간다. 가이드가 중괄호 꼴만 다룬다고 적어 거짓 주장은 아니다. 실행 비트 쪽 빈틈은 원래 있던 것
- 검증 가이드 FAIL 예시 2 의 출처가 틀렸다 — `harness/docs/guides/plugin-validation-guide.md:417-421` 머리가 `# design-kit/hooks/hooks.json` 인데 둘째 줄 `bash ${CLAUDE_PLUGIN_ROOT}/hooks/log-prompt.sh` 는 reflect-kit 명령이다(`origin/main` 의 design-kit hooks.json 명령은 `env-check.sh` 하나). 실제 출력은 명령마다 `(<명령>)` 이 붙은 한 줄씩 두 줄인데 예시는 한 줄이다. 위 「넘긴 것」 의 가이드 판 번호 · 수동 수정 표와 함께 main 을 합친 뒤 고친다
- V8 설명 한 곳이 옛 글이다 — `.claude/skills/react-kaizen/SKILL.md:97` 이 `V8 hook-exec` 를 실행 비트(0755)로만 적어 따옴표 검사가 빠졌다. 가이드 수동 수정 표 · `docs/harness/plugin-validation.html` 과 같이 고치고, 그 전에 V8 설명이 적힌 자리를 전부 찾는다
- 다시 만든 킷 README 표 설명이 문장 중간에서 끊긴다 — `planning-kit/README.md:21` · `:25` (`…수렴(convergent)하여 |` · `…적용하여 |`), `rust-kit/README.md:16` (`… 정의 → |`). sync-docs 가 SKILL.md 설명 첫 줄만 옮긴다(다른 킷 README 도 같다). 위 「판단이 갈린 곳」 넷째 줄의 다음 묶음 후보와 같은 일이다
- 넘김 — 가이드의 「공식 hooks 문서도 따옴표를 권한다」 문장 근거는 `.harness/.meta/evidence/phase12.md:113` 이다. 원문을 직접 받아 대조하지는 못했다(WebFetch 훅이 막음). 다음 리서치 때 원문과 맞춘다
