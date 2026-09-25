---
feature: "카이젠 2026-09-24 Phase 12 계약 — Stop 훅 수집 복구 · 수집 상태 머리 · facets 대조 · 워크트리에서도 본 레포 이름"
slug: kaizen-0924-p12-reflect-kit
created: "2026-09-25 09:11"
complexity: "복잡"
conditions: 29
status: active
owner_session: de8c7935-a5b6-4df5-9106-fafa73c288a0
conditions_digest: sha256:71e1e96b9d125ed8
locked_at: "2026-09-25 10:01"
---

## 배경

이 Phase 의 외부 근거는 `.harness/.meta/evidence/phase12.md` 하나다. 처리 배정표(`.claude/kaizen-input/insights-report.md`)에서 `배정` 칸이
`Phase 12` 인 행은 셋이다(`reflect-collector:P3` · `reflect-collector:P4` · `reflect-collector:P5`). 다른 Phase 행의 비고가 Phase 12 를 가리키는 것이
하나(`harness:P02` — 「reflect-collector:P5 가 같은 파일의 프로젝트 이름 계산을 바꾸므로 함께 시험한다」)이고, 러닝북 `Phase 별 추가 과제` 의 Phase 12 줄이
하나(인사이트 스프린트에서 `save-feedback.sh` 가 워크트리 이름을 프로젝트 이름으로 적었다 — `reflect-collector:P5` 와 같은 규칙)다. 앞 Phase notes 가운데
Phase 12 를 부른 것은 `phase4-notes.md` 의 `reflect-collector:P5` 넘김 한 줄이다(「Phase 12 범위는 `reflect-kit/` 라 이 파일을 못 고친다 — 다음 사이클 Phase 4」).
근거 파일 §3 현행화 점검도 입력이다.

| 키 | 내용 | 이번 처리 |
| --- | --- | --- |
| `reflect-collector:P3` | Stop 훅 수집이 멈췄다 — 읽기 전용 실행, stderr 를 버리지 않음 | 반영 — codex 인자에서 `--full-auto` 를 빼고 `-s read-only`, 두 분석기 stderr 를 파일로 받아 한 줄을 `err=` 로, 대체 경로 모델 `haiku`와 `--no-session-persistence`, 분석기 표식으로 분석기 세션의 훅이 아무것도 적지 않게, 임시 파일 정리 (SC-01 ~ SC-04 · SC-08) |
| `reflect-collector:P4` | reflect-digest 머리에 수집 상태 줄과 facets 대조 | 반영 — `collect_status` · `facets_unmatched` 두 함수와 알려진 답 시험, digest Gotcha 13 · 14 와 Process · 출력 틀, reflect-kaizen §0 에 같은 수집 상태 (SK-01 · SK-02 · SK-04 · SC-06 · SC-07) |
| `reflect-collector:P5` | 프로젝트 이름을 워크트리 폴더가 아니라 본 레포 이름으로 | 반영 — `project_root` 와 알려진 답 시험, 문서 셋 (SK-03 · SK-05 · SC-05). 이미 워크트리 이름으로 생긴 폴더는 옮기지 않는다(아래 선택) |
| `harness:P02` 비고 · 러닝북 추가 과제 · Phase 4 넘김 | `harness/scripts/save-feedback.sh` 의 같은 규칙 | 미반영 — 이 Phase 범위는 `reflect-kit/` 다. 규칙과 시험 배치는 이 계약의 `project_root` · `project-id-test.sh` 를 그대로 옮기면 된다고 notes 에 적어 다음 사이클 Phase 4 로 넘긴다 (ER-03) |
| 근거 §3 현행화 | `hooks.json` 의 따옴표 없는 `${CLAUDE_PLUGIN_ROOT}` · 수동 `nohup` 대 `async` · `asyncRewake` · SCHEMA §5 · digest `:110` · `:297` · `plugin.json` | SCHEMA §5 · digest 두 곳은 반영(SK-01 · SK-03 · SK-05). 따옴표는 킷 넷의 `hooks.json` 이 모두 같은 모양이라 한 킷만 바꾸지 않고 다음 사이클 Phase 4(`validate-plugin.py` V8)로 넘긴다. `async` 전환은 근거 파일 스스로 「즉시 교체 필수는 아니다」 라고 적었다 — 다음 사이클. `plugin.json` 은 Final (ER-03) |

고칠 것은 네 갈래다.

1. **Stop 훅이 한 달 가까이 아무것도 못 적었다 (P3).** `reflect-kit/hooks/log-reflection.sh:273` 의 `--full-auto` 를 이 기계의 codex-cli 0.154.0 이 거부한다.
   아래 봉인 전 실측에서 옛 인자 묶음은 `error: unexpected argument '--full-auto' found` · 종료 코드 2 다. 첫 `fail:codex-exit-2` 는 2026-08-28T18:01:14, 마지막 기록은
   같은 날 17:28:39 다. 대체 경로 `claude -p --model haiku-4.5`(`:248`)는 CLI 가 모르는 모델이라 종료 코드 1 이다(`fallback:claude-used` 전 기간 0 건).
   두 분석기의 stderr 를 버려서(`:248` · `:277`) 원인이 로그에 한 줄도 없었다
2. **대체 경로가 원시 로그를 더럽혔다 (P3 에서 찾음).** 대체 경로 `claude -p` 의 프롬프트 제출 훅이 분석용 프롬프트(다른 세션의 transcript)를 원시 로그 `YYYY-MM.md` 에
   3,044 번 적었다(2026-09-25 오전 실측 — 수집이 멈춘 동안 계속 는다). 같은 때 실패한 대체 경로 수(3,041)와 거의 같다. 봉인 전 실측에서 `claude -p` 가 띄운 훅은 부른 쪽의 환경 변수를 받는다(`marker=[1]`)
3. **엔트리 0 이 「문제 없음」 으로 읽힌다 (P4).** digest 요약은 엔트리 · 세션 · 파싱 실패만 보인다(`reflect-digest/SKILL.md:297`). 수집이 멈춘 동안 digest 를 돌리면
   0 만 나오고 원인은 `## 훅 실패 요약` 의 건수에 묻힌다. facets 는 `/insights` 가 따로 낸 세션 요약인데 digest 가 읽지 않는다
4. **워크트리마다 로그 폴더가 갈린다 (P5).** `_lib-project-id.sh:62` 가 `--show-toplevel` 을 써서 링크된 워크트리에서 워크트리 폴더 이름이 나온다.
   봉인 전 실측: 로그 폴더 31 개 가운데 12 개가 워크트리 이름이다(`.project-root` 마커에 `/.claude/worktrees/` 가 든 폴더)

이번 사이클 Phase 1 가이드 변경과 이 킷(오케스트레이터 Gotcha 「Phase 1 에서 가이드를 변경했으면 전수 체크」):

| 변경 | 이 킷의 자리 | 처리 |
| --- | --- | --- |
| §3.7 `[미검증]` 네 칸 | 없음 — `reflect-kit/` 에 `[미검증]` 을 내는 자리가 0 이다(`grep -rn '미검증' reflect-kit` 은 codex-kaizen 의 「출처 미검증」 두 줄뿐) | 해당 없음 |
| §3.7 알려진 답 대조 | 이번에 새로 짜는 측정은 `collect_status` · `facets_unmatched` · `project_root` 와 그 시험 셋 | SC-05 ~ SC-07 이 손으로 센 답으로 잰다 |
| agent 가이드 §10 | 이 킷에 에이전트가 없다 | 해당 없음 |

## 리서치 소스

외부 조회 0 회. 아래 URL 은 전부 근거 파일 `.harness/.meta/evidence/phase12.md` 에서 가져왔다.

- [Codex non-interactive mode](https://developers.openai.com/codex/noninteractive) — `codex exec` 기본 샌드박스는 read-only, `--full-auto` 는 호환용으로만 남았다 (SC-01)
- [Codex CLI v0.156.1](https://github.com/openai/codex/releases/tag/rust-v0.156.1) — 최신 안정판. 로컬 0.154.0 은 `--full-auto` 를 아예 거부한다 (SC-01 · SC-08)
- [Claude Code model configuration](https://code.claude.com/docs/en/model-config) — 공식 값은 별칭 `haiku` 또는 `claude-haiku-4-5` 이고 `haiku-4.5` 는 아니다 (SC-03)
- [Claude Code CLI reference](https://code.claude.com/docs/en/cli-reference) · [headless mode](https://code.claude.com/docs/en/headless) — `--no-session-persistence`, 실패 시 0 아닌 종료 코드 (SC-03)
- [Claude Code Hooks reference](https://code.claude.com/docs/en/hooks) — 훅 입력의 `session_id` · `transcript_path` · `cwd`, Stop 의 `last_assistant_message`, `async` · `asyncRewake` (배경 · ER-03 넘김)
- [git-rev-parse](https://git-scm.com/docs/git-rev-parse) — `--path-format=absolute` · `--git-common-dir` · `--show-toplevel` (SC-05)
- [Reflexion](https://arxiv.org/abs/2303.11366) · [MultiSoc-4D](https://arxiv.org/abs/2605.06940) — facets 를 reflection 빈도에 더하지 않고 대조에만 쓴다, 닫힌 태그 목록을 만들지 않는다 (SK-02)

근거 파일이 스스로 밝힌 한계를 그대로 옮긴다: 대체 경로 종료 코드 1 의 원인은 옛 로그에 stderr 가 없어 확정하지 못했다(§5) — 이 계약은 봉인 전에
`claude -p --model haiku-4.5` 를 훅 없이 한 번 돌려 확정했다(아래 실측). facets · session-meta 형식의 공식 문서는 없다(§5) — 두 폴더는 선택 입력이고 읽지 못한
파일은 두 갈래로 나눠 센다(SC-07). Stop 시점 transcript 에 마지막 응답이 없을 수 있다(§5) — 이번에 다루지 않는다(ER-03 넘김). `수집 상태` 의 N 을 무엇으로 셀지
기존 계약에 없다(§5) — 이 계약은 「기록 없이 끝난 실행 수」 로 정한다(아래 선택).

내부 입력: 데이터 풀 §0 처리 배정표 · §0-b(18 세션 — reflect-kit 을 글자 그대로 언급한 행은 없다) · §0.5(reflect 그룹 주입 0 건) · 앞 Phase notes 열 개.
`validate-plugin.py reflect-kit` 는 시작 커밋에서 V1~V10 전부 OK(V2 는 templates 가 없어 SKIP)였다.

## GAP 분석 · 개선안 초안

### 카이젠 스킬 절차의 분류

이 Phase 의 카이젠 스킬 `reflect-kit/skills/reflect-kaizen/SKILL.md` 는 킷 파일을 고치는 절차가 아니라 수집된 reflections 의 품질을 재는 절차다(§0 파편화 게이트 →
§1 · §2 다른 모델 재분류 일치도 → §3 ledger 재발 → §4 임계 제안). 이번 사이클에 그 절차를 돌린 결과(읽기만 했다):

| 단계 | 결과 | 이번 처리 |
| --- | --- | --- |
| §0 | `tag_canon_selftest` → `SELFTEST_OK raw=4 clusters=2 canonical=edit-before-read`. 전 폴더 reflections 11 파일의 `tag_canon_fragmentation` → `3104 3024 5339 2682 1.03 0.887 1.77` — `singleton_share 0.887 > 0.70` 이라 `calibration_confidence: low` | 기록만 (notes) |
| §1 · §2 | 돌리지 않았다 — 마지막 기록이 2026-08-28 이라 30 일 창에 새 표본이 거의 없고, 모델 호출이 드는 측정이라 DRAFT 몫이 아니다 | notes 에 사유 |
| §3 | `~/.claude/logs/*/promotions-ledger.md` 가 없다(데이터 풀 §0.5 도 같은 결과) | 해당 없음 |
| §4 | §0 이 `low` 라 절차상 건너뛴다 | 해당 없음 |

절차 자체의 빈틈 하나를 찾았다: §0 은 **이미 쌓인** 기록의 모양만 재므로 수집기가 멈춰도 게이트를 통과한다. 수집이 멈춘 기간의 `post_freq == 0` 은
Gotcha 12 가 막는 「못 셌음」 과 같은 것이다 — SK-04 가 §0 에 수집 상태 줄을 더한다.

### 1.1 복잡도 4 축

| 축 | 물음 | 값 |
| -- | ---- | -- |
| 레이어 수 | 몇 개 계층을 관통하는가 | 4 — 훅 셋(수집) · 라이브러리(폴더 이름 · 상태 계산) · 스킬 둘(집계 · 보정) · 문서 셋 (+ 새 시험 셋) |
| 공개 API·계약 변경 | 외부에 노출된 형태가 바뀌는가 | 예 — `.errors.log` 줄에 `err=` 가 붙고 새 태그를 문서에 올린다, 새 함수 셋, 워크트리에서 부른 훅이 쓰는 폴더 이름이 바뀐다 |
| 소비면 존재 | 이 형태를 받아 쓰는 반대편이 있는가 | 예 — 아래 Counterpart 표 |
| 회귀 위험 | 기존 동작이 깨질 수 있는가 | 예 — 훅 셋은 모든 프롬프트 · 도구 실패 · 세션 끝에 돈다. 폴더 이름 규칙이 바뀌면 워크트리에서 쌓이던 새 기록이 본 레포 폴더로 간다 |

넷 가운데 셋이 「예」 이고 공개 형태 변경과 소비면이 둘 다 「예」 라 **복잡**이다. Step 2.5 Counterpart 조건을 넣는다(SK-01 ~ SK-05 · AR-02 · ER-03).
기능 조건은 20 개다 — 복잡 9~20 안이다(SKILL.md Step 6.2 둘째 명령으로 이 파일을 세면 20).

### 1.2 설정 리터럴 대조표

| config key | project.yaml 에서 읽은 값 | 계약에 쓴 값 |
| ---------- | ------------------------- | ------------ |
| `commands.analyze` | `bash -n scripts/release.sh` | DG-01 N/A 사유에 그대로 |
| `commands.test` | `bash scripts/release.sh 2>&1 \|\| true` | DG-03 N/A 사유에 그대로 |
| `diagnostics.ide_exclude` | `[]` | DG-02 에 그대로 |
| `contract_categories[].id` / `prefix` | `Skill`/`SK` · `Script`/`SC` · `Error`/`ER` · `Architecture`/`AR` | 조건 섹션 제목과 접두 그대로 |
| `anti_patterns[].id` / `message` | AP-01 · AP-02 · AP-03 · AP-04 | AP-01 · AP-03 · AP-04 선별, message 원문 그대로. AP-02(force push)는 이 Phase 가 밀어 넣지 않아서 뺀다 |

### 1.4 편집 전 감사 (실제로 읽은 줄 — 시작 커밋 `82b2493` 판)

| 대상 파일 | 실제 Read 증거 (`파일:라인`) | 발견한 기존 갭·위반 | 계약 조건화 |
| --------- | ---------------------------- | ------------------- | ----------- |
| `reflect-kit/hooks/log-reflection.sh` | `:1-48` (머리 · fast path, `:45` nohup 이 출력을 버림) · `:101` (「bg 경로라 stderr 는 버려진다」) · `:234-265` (대체 경로, `:248` `haiku-4.5` · stderr 버림) · `:267-288` (codex 호출, `:273` `--full-auto` · `:277` 출력 둘 다 버림) | 수집 멈춤 · 원인 기록 없음 · 대체 경로 실패 | SC-01 ~ SC-04 · SC-08 |
| `reflect-kit/hooks/_lib-project-id.sh` | `:1-18` (머리) · `:57-92` (`compute_project_id`, `:62` `--show-toplevel`) · `:114-124` (`log_hook_error`) | 워크트리 이름 폴더 | SC-05 · SC-06 · SC-07 |
| `reflect-kit/hooks/log-prompt.sh` · `log-tool-failure.sh` | 전체 (`log-prompt.sh:4` 「<basename>-<6자 hash>」 — v0.3.0 부터 틀린 주석) | 분석기 세션의 프롬프트 · 도구 실패도 적는다 | SC-04 |
| `reflect-kit/hooks/hooks.json` | 전체 (`:8` · `:19` · `:30` 따옴표 없는 `${CLAUDE_PLUGIN_ROOT}`) | 근거 §3 — 킷 넷이 같은 모양 | 그대로 (ER-03 넘김 · AR-02 `hooks_same`) |
| `reflect-kit/skills/reflect-digest/SKILL.md` | `:21-34` (Gotcha 1~12) · `:45-55` (프로젝트 ID, `:49` `basename(git-root)`) · `:70-75` (데이터 소스) · `:107-168` (Process, `:116-118` 4 단계 · `:167` 9 단계) · `:216-232` (project=all 머리) · `:289-368` (출력 포맷, `:297` 요약 · `:356-361` 훅 실패 요약) | 수집 상태 · facets 없음 | SK-01 ~ SK-03 |
| `reflect-kit/skills/reflect-kaizen/SKILL.md` | `:22-35` (Gotchas) · `:45-68` (§0) · `:112-126` (출력 (0) · (1), `:126` `haiku-4.5`) | 수집 멈춤을 모른다 · 없는 모델 이름 | SK-04 |
| `reflect-kit/docs/SCHEMA.md` | `:123-141` (§3 사유 태그 — 대체 경로 태그 넷 · `fail:tag-field-unresolved` 없음) · `:189-195` (§5 — v0.3.0 전 규칙 그대로) | 구현과 어긋남 | SK-05 |
| `reflect-kit/docs/DESIGN.md` | `:172-186` (에러 관측성 — SCHEMA §3 과 같은 목록) · `:229-266` (결정 #3 상세, `:243-248` Hybrid 표) | 워크트리 행 없음 | SK-05 · AR-02 |
| `reflect-kit/README.md` | `:7` (「버전: `0.3.0`」 — 실제 0.7.1) · `:94` (`basename(git-root)`) · `:96-102` (의존성 — `claude` CLI 없음) | 옛 판 · 대체 경로 의존 누락 | SK-05 · `:7` 은 ER-03 넘김 |
| `reflect-kit/skills/reflect-promote/SKILL.md` · `reflect-kit/scripts/legacy-id-migrate.sh` | `:52` (`compute_project_id` 를 부른다) · `:91` · `:129` · `:165` | 이름만 부른다 | 그대로 (Counterpart) |
| `harness/scripts/save-feedback.sh` (읽기만) | `:128-176` (`identity_root_of` 가 `--show-toplevel`) | 같은 결함 — 범위 밖 | ER-03 넘김 |
| `harness/agents/qa-evaluator.md` · `harness/docs/guides/qa-evaluation-guide.md` (읽기만) | `:754-765` · `:643-652` (`BASE=$(basename "$(git … --show-toplevel …)")` 로 prompt 로그 폴더를 찾는다) | 워크트리 계약에서 새 기록 폴더(본 레포 이름)를 못 찾는다 — 범위 밖 | ER-03 넘김 |

구현 후보가 둘 이상이었던 곳의 선택:

- **새 함수를 어디에.** 새 라이브러리 파일 대 `_lib-project-id.sh`. **`_lib-project-id.sh`.** `.errors.log` 를 쓰는 `log_hook_error` 와 폴더 순회용 `is_internal_logs_dir` 가
  이미 여기 있고 세 훅이 이미 읽는다. 새 파일이면 스킬이 두 라이브러리를 따로 읽어야 하고 zsh 에서 자기 위치를 찾는 코드를 또 써야 한다
- **셸.** 두 새 함수는 bash 가 아니면 멈춘다(`collect_status: bash 로 부른다`). 스킬 한 줄 명령은 `bash -c` 로 감싼다. zsh 에서는 시험하지 않았고, 같은 입력에 셸마다 조용히
  다른 답을 낸 전례(`_lib-tag-canon.sh` 2026-08-13)가 있다. 라이브러리를 zsh 에서 읽어 `compute_project_id` 를 부르는 기존 쓰임은 그대로 된다(SC-05 zsh 경우)
- **`Stop 실패 시도` 를 무엇으로 셀지.** 근거 권장안은 「codex 849 · 대체 경로 849 를 더하지 않는다」 까지만 정했다. **기록 없이 끝난 실행 수** = 대체 경로 실패 셋
  (`fallback:claude-exit-N` · `fallback:claude-empty-output` · `skip:fallback-unavailable`) + 분석 전 중단 둘(`skip:cli-missing` · `fail:tag-field-unresolved`).
  codex 실패 수는 따로 보인다. 대체 경로가 성공하면 기록이 남으므로 실패 시도에서 빠진다. `skip:transcript-*` 는 짧은 세션의 정상 건너뜀이라 세지 않는다
- **`err=` 를 어떤 줄로.** 근거 권장안 「stderr 첫 비어 있지 않은 줄」 대 「`error` · `ERROR` 로 시작하는 첫 줄, 없으면 첫 비어 있지 않은 줄」. **뒤쪽.** 봉인 전 실측에서
  codex 는 성공해도 stderr 에 머리글 열 줄 남짓과 받은 프롬프트 전문을 찍는다 — 첫 줄은 늘 `OpenAI Codex v0.154.0` 이라 원인이 안 보인다. 한도 초과 같은 실행 중 오류는
  `ERROR:` 로, 인자 오류는 `error:` 로 시작한다(코덱스 리서치 로그의 실패 줄 · 봉인 전 실측). 가린 뒤 200 자로 자른다 — 먼저 자르면 반 토막 난 키가 가림 패턴에 안 걸린다
- **대체 경로 `err=`.** stderr 가 비면 stdout 에서 고른다 — 봉인 전 실측에서 모델 이름 오류의 사람이 읽을 문장(「There's an issue with the selected model」)이 stdout 으로 나왔다
- **대체 경로 모델.** 별칭 `haiku` 대 `claude-haiku-4-5`. **`haiku`.** 봉인 전 실측에서 이 기계의 CLI 로 종료 코드 0 · `ok` 를 받았다. 별칭은 새 Haiku 가 나와도 낡지 않는다
- **분석기 표식.** 근거 파일에 없는 변경이다 — 이 Phase 가 실측으로 찾았다(원시 로그 3,044 건). `REFLECT_KIT_ANALYZER=1` 을 두 분석기 호출에 붙이고 세 훅 첫머리에서
  보면 끝난다. `--no-session-persistence` 만으로는 프롬프트 제출 훅을 못 막는다(봉인 전 실측: 그 옵션을 붙인 `claude -p` 에서도 훅이 돌았다)
- **워크트리 이름으로 이미 생긴 폴더.** 옮기기 · 읽을 때 합치기 · 그대로. **그대로.** 봉인 전 실측에서 그 12 개 폴더의 reflections 는 0 이고 원시 로그와 `.errors.log` 만 있다.
  옮기면 원시 로그의 `cwd:` 와 폴더 이름이 어긋나고, 합쳐 얻는 것은 실패 시도 수뿐이다. `project=all` 이 그대로 순회한다. 근거 §4 P5 「읽기 합치기나 옮기기를 명시적으로 결정한다」 의 답이다
- **`project_root` 조건.** 근거 권장안은 「공통 폴더 이름이 `.git` 이면 부모」. 여기에 「git-dir 과 common-dir 이 다를 때만(링크된 워크트리)」 을 더한다 — `git init --separate-git-dir`
  로 만든 본 체크아웃에서 공통 폴더 이름이 `.git` 이면 엉뚱한 부모를 쓰게 된다. 시험의 「다른 곳에 둔 git 폴더」 경우가 그 배치다
- **hooks.json 따옴표 · `async`.** 이번에 안 한다(위 배경 표)

### Counterpart — 바뀌는 형태를 받아 쓰는 반대편

| 파일 | 읽는 것 | 이번 처리 |
| --- | --- | --- |
| `reflect-kit/skills/reflect-digest/SKILL.md` · `reflect-kit/skills/reflect-kaizen/SKILL.md` | `.errors.log` 태그 · 폴더 이름 | 반영 — SK-01 ~ SK-04 |
| `reflect-kit/docs/SCHEMA.md` §3 · §5 · `reflect-kit/docs/DESIGN.md` 에러 관측성 · 결정 #3 · `reflect-kit/README.md` | 태그 목록 · 폴더 이름 규칙 | 반영 — SK-05, 두 목록이 같은지 AR-02 |
| `reflect-kit/skills/reflect-promote/SKILL.md:52` · `reflect-kit/scripts/legacy-id-migrate.sh` | `compute_project_id` 를 이름으로 부른다 | 그대로 — 부르는 모양이 안 바뀐다 |
| `harness/scripts/save-feedback.sh:136-176` | 같은 규칙을 따로 구현 | 미반영 — 범위 밖. 다음 사이클 Phase 4 (ER-03) |
| `harness/agents/qa-evaluator.md:754-765` · `harness/docs/guides/qa-evaluation-guide.md:643-652` | prompt 로그 폴더를 `--show-toplevel` 이름으로 찾는다 | 미반영 — 범위 밖. 워크트리 계약에서는 이 변경 뒤 새 기록이 본 레포 폴더에 쌓이므로 평가자 쪽 규칙도 같이 바뀌어야 한다. 다음 사이클 Phase 3 (ER-03) |
| `scripts/collect-kaizen-data.py:421` | facets `project_path` 를 `/.claude/worktrees/` 앞에서 자른다 | 같은 방향이라 그대로 |
| `docs/reflect-kit/*.html` | 스킬 문서 페이지 | Final F2 (ER-03) |
| `.github/workflows/ci.yml` | 새 시험을 돌릴 자리 | Phase 가 못 고친다 — notes 에 넣을 줄 셋 (ER-03) |

### 개선안 초안

정확한 내용은 스크래치 `/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/de8c7935-a5b6-4df5-9106-fafa73c288a0/scratchpad/p12d/mock.py`
(sha256 앞 16 자리 `75b19518ca3f7713` — 2 회차 검토가 고친 시험 파일을 넣어 다시 만든 판. 옛 판 `714450452fff4513` 은 `p12d/mock.v1.py`)가 쓰는 열두 파일 그대로다(`python3 mock.py <트리>`). mock.py 는 먼저 전부 확인하고 나서 쓴다 — 바꿀 아홉 파일은 시작 커밋 판(sha256)과 같아야 하고
새 파일 셋은 없어야 하며, 하나라도 어긋나면 아무것도 쓰지 않고 `MOCK_FAIL` 을 낸다. BUILD 는 작업 폴더에서 `python3 mock.py .` 을 돌려 `mock applied 12` 를 확인한다
(시작 커밋 판을 푼 새 사본에서 `mock applied 12` · 종료 코드 0, 두 번째 실행은 `MOCK_FAIL` · 종료 코드 3 · 파일 변화 0 을 확인했다 — 새 판으로 BUILD 가 다시 확인했다). 새 시험 셋은 모드 755 로 생긴다. 요지:

- `_lib-project-id.sh` — `project_root`(링크된 워크트리면 본 레포), `compute_project_id` 가 그것을 쓴다. `collect_status` · `facets_unmatched` 와 기간 계산 `_rk_since`
- `log-reflection.sh` — 분석기 표식 검사, `err_line`, codex `-s read-only` · stderr 파일, 대체 경로 `haiku` · `--no-session-persistence` · stderr 파일 · stdout 대체, 임시 폴더 하나와 `trap`
- `log-prompt.sh` · `log-tool-failure.sh` — 분석기 표식 검사 한 줄, `log-prompt.sh:4` 틀린 주석 정정
- reflect-digest — Gotcha 13 · 14, 프로젝트 ID 넷째 줄 · `project_root` 헬퍼, 데이터 소스 facets 줄, Process 4 · 9 단계, project=all 머리 · 예시, 출력 틀 머리 두 줄 · 대조 절 · 훅 실패 요약 두 줄
- reflect-kaizen — §0 수집 상태 문단과 한 줄 명령, 출력 (0) 한 줄, (1) 모델 이름
- SCHEMA §3 태그 다섯 · `err=` 문단, §5 다시 씀. DESIGN 에러 관측성 태그 다섯 · 두 문단, 결정 #3 표 한 행 · `### 워크트리 (2026-09-25)` 절. README 폴더 이름 줄 · 의존성 두 줄
- 새 시험 `reflect-kit/evals/hooks/log-reflection-test.sh`(24 경우) · `project-id-test.sh`(16 경우 — zsh 가 없으면 15) · `collect-status-test.sh`(10 경우 — zsh 가 없으면 9)

## 범위 경계

- 이 Phase 시작 HEAD: `82b2493da582554a0ae4c1ee36db1bb3ba7c511b`. 범위 상한은 개정 파일 `.harness/sprint-amendments-kaizen-0924-p12-reflect-kit.md` 의 `end_sha:`
  마지막 값이다. 여러 Phase 가 같은 가지 `kaizen/2026-09-24` 에 동시에 커밋하므로 `HEAD` 로 재지 않는다
- 고치는 파일은 열둘이다(새 파일 셋 포함) — 아래 블록이 그 목록이다(`harness/README.md` §커밋 안전 훅 이 정한 범위 선언 자리). `.harness/` 쪽은 이 계약 · 개정 파일 ·
  QA 피드백 · `.harness/.meta/kaizen-0924/phase12-notes.md` · `.harness/.meta/kaizen-0924/phase12-review.md` 를 쓴다 — 슬러그를 나열하지 않고 AR-01 셋째 값 `verify_seal` 로 잰다.
  AR-01 다섯째 값이 이 블록과 측정 공통 정의의 `FILES` 가 같은지 잰다

```text
# sprint-scope
reflect-kit/hooks/_lib-project-id.sh
reflect-kit/hooks/log-reflection.sh
reflect-kit/hooks/log-prompt.sh
reflect-kit/hooks/log-tool-failure.sh
reflect-kit/skills/reflect-digest/SKILL.md
reflect-kit/skills/reflect-kaizen/SKILL.md
reflect-kit/docs/SCHEMA.md
reflect-kit/docs/DESIGN.md
reflect-kit/README.md
reflect-kit/evals/hooks/log-reflection-test.sh
reflect-kit/evals/hooks/project-id-test.sh
reflect-kit/evals/hooks/collect-status-test.sh
.harness/
```

- **이 Phase 의 커밋 메시지에는 전부 `Co-Authored-By` 줄 바로 위에 서명 줄 `Kaizen-Phase: kaizen-0924-p12-reflect-kit` 한 줄을 넣는다** (봉인 커밋 포함).
  AR-01 · ER-03 · DG-01 · DG-03 · DG-04 · DG-06 이 이 줄로 이 Phase 커밋을 가린다(`harness/references/contract-schema.md` §여러 주체가 한 가지에 커밋할 때 선택지 B).
  서명을 빠뜨린 커밋은 서명 줄 목록에 안 보이므로 AR-01 첫째 값과 ER-03 마지막 값은 경로로 직접 센다.
  FIX 가 커밋을 더할 때도 넣고, 개정 파일에 `end_sha:` 줄을 덧붙인다(옛 줄은 지우지 않는다). notes 커밋도 이 Phase 커밋이다 — notes 를 커밋한 뒤 그 sha 로
  `end_sha:` 줄을 하나 더 덧붙여 커밋한다
- 구현 커밋은 `git add -- <파일…> && git commit -o -- <파일…>` 로 열두 파일만 싣는다. 새 시험 셋은 `add` 가 먼저다. 열둘 모두 이 킷 몫이라 한 커밋이어도
  `validate-post-kaizen.py` scope-isolation 에 걸리지 않는다. 새 시험 셋의 실행 비트는 `git ls-tree` 에서 `100755` 여야 한다(AR-02)
- 측정이 기대는 제목 · 줄 머리는 이름을 바꾸지 않는다: `## Gotchas` · `## 데이터 소스` · `## 프로젝트 ID` · `4. **엔트리 파싱**` · `5. **actionability 분리**` · `9. **리포트 출력**` ·
  `10. **결과 저장` · `### 4. Given-When-Then 동작 계약` · `## 출력 포맷` (digest) · `### 0. 파편화 지표 선행 확인` · `### (0) 파편화 지표` · `### (1) LLM-as-judge 일치도` (kaizen) ·
  `## 3. 훅 에러 로그` · `### 사유 태그` · `## 5. Project ID 포맷` (SCHEMA) · `## 에러 관측성` · `### 워크트리 (2026-09-25)` (DESIGN) · `codex exec \` 와 그 뒤 `  - ` 로 시작하는 줄
  (log-reflection.sh — `cxargs` 가 그 사이를 codex 인자로 읽는다) · `err_line() {` · `project_root() {` · `compute_project_id() {` · `facets_unmatched() {` 와 각 함수의 닫는 `}` 줄.
  이름이 바뀌면 `sect` · `between` · `awk` 범위가 빈 글을 내 값이 0 이 된다 — FAIL 쪽으로 틀린다
- 공유 파일(`.claude-plugin/marketplace.json` · `reflect-kit/.claude-plugin/plugin.json` 버전 · 루트 `README.md` · 루트 `CLAUDE.md` · `docs/` HTML · 처리 배정표 · 감사 로그 ·
  실패 횟수 파일 · `.github/workflows/ci.yml` · `.harness/stale-values.yaml`)과 다른 Phase · 레포 전용 파일(`harness/` · `scripts/` · `.claude/skills/`)과 이 킷의 나머지
  (`reflect-kit/hooks/hooks.json` · `reflect-kit/references/` · `reflect-kit/scripts/` · reflect-promote · codex-kaizen)는 건드리지 않는다 — ER-03 마지막 값.
  README 의 AUTO 구간은 스킬 frontmatter 를 읽는데 frontmatter 를 바꾸지 않는다(AP-04). 문서 사이트 재생성은 Final F2 몫이라 DG-06 에서 `docs-site-regen` 을 뺀다
- QA(`harness:qa-evaluator`)는 설치본이다 — 이 Phase 가 고치는 파일에 harness 파일은 없다
- **설치본은 이 Phase 가 고치지 않는다.** 실제 Stop 훅은 `~/.claude/plugins/cache/…/reflect-kit/<판>/hooks/` 의 옛 판이 돈다 — 배포(Final)와 설치본 갱신 전까지 수집은 계속 멈춰 있다.
  이 계약의 조건은 레포 판을 시험으로 잰다. 설치본에서 한 번 더 확인하는 일은 Final 뒤 몫이다(근거 §4 P3 마지막 줄)
- 사용자 승인(Step 5) 대체: 사용자가 「자동으로 끝까지 알아서 진행해 내 허락이 필요한건 코덱스로 리서치나 검토받고」라고 위임했다(세션
  `de8c7935-a5b6-4df5-9106-fafa73c288a0` 기록 queued_command `2026-09-24T04:04:16.964Z`). Codex 사용량 한도가 소진돼(오류 원문 「You've hit your usage limit … try
  again at 11:05 PM」, 2026-09-24) 독립 Claude 검토자(REVIEW 에이전트)가 대신한다. 이어 사용자가 「코덱스 대신에 그냥 너가 알아서 진행하라고」라고 명시했다(같은 세션
  기록 user `2026-09-24T11:54:58.940Z`). 검토 결과 파일: `.harness/.meta/kaizen-0924/phase12-review.md` — 1 회차 `VERDICT: CHANGES`(필수 둘: 시험 출력을
  `일치 ` 로 시작하는 줄만 세기 · SC-06 · SC-07 의 손으로 센 답을 시험 파일에서 재기)는 DRAFT 가 반영했다. 2 회차 `VERDICT: CHANGES`(고칠 것 셋: 시험의 가짜 codex 가
  거부하기 전에 호출을 적고 codex 성공 기록은 codex 만 내는 태그로 세기 · SC-01 문구와 편집 전 훅 대조 값 17 → 18 · `mock.py` 지문과 표)는 BUILD 가 봉인 전에 전부 넣었다.
  2 회차 권하는 것 1(SC-07 세션 줄 둘도 시험 파일에서 재기)도 넣었고 2(디스크 여유)는 예행 저장소를 하나씩 만들고 지워서 따랐다. 1 회차 권하는 것 5(시험 셋 지문 고정)는
  고르지 않았다 — 답 줄을 재는 것으로 갈음했다(2 회차가 문제 삼지 않았다). 3 회차 검토는 받지 않았다: 오케스트레이터 지시가 「남은 지적을 반영하거나 반영하지 않는 이유를
  계약 범위 경계에 적은 뒤 진행」 이고, 바뀐 조건 둘(SC-01 · SC-07)은 BUILD 가 예행 판과 망가뜨린 사본에서 다시 쟀다(`회귀 게이트` 절 `BUILD 재측정` 문단)
- 오라클 한계: 실제 Stop 훅이 실제 codex · claude 로 기록을 남기는지는 LLM 호출과 설치본이 걸려 결정론 측정이 없다 — 조건은 가짜 분석기로 돈 훅 동작(SC-01 ~ SC-04), 이 기계
  codex 의 인자 해석(SC-08), 문서 문장까지만 건다. 대체 경로 모델이 실제로 받아들여지는지는 봉인 전 실측 한 번(아래)으로만 남긴다
- 오라클 해소: SK-01 ~ SK-05 — 산출물이 문서 문장 자체라 정해진 절 · 줄에 정해진 문장이 있는지가 판정이다. `sect` 가 코드 펜스를 건너뛰고 절을 자르고, `between` 이 Process 번호
  단계 하나를, `gline` 이 한 줄짜리 Gotcha 를 고른다. 시작 커밋 판에서 새 문장 0 · 옛 문장 1 이상을 봉인 전에 확인했고, 문장 하나만 지운 사본에서 그 조건의 출력이 바뀌었다(`회귀 게이트` 절)
- 오라클 해소: SC-01 ~ SC-07 — 새 시험 셋을 `$END` 판 사본에서 실제로 돌린 출력이다. 셋 다 알려진 답(손으로 센 값)을 쓰고 음성 대조(편집 전 판 · 망가뜨린 사본)가 붙어 있다.
  시험 출력은 `일치 ` 로 시작하는 줄만 센다 — 시험이 실패를 `불일치 <이름>` 으로 찍어 그 줄에도 `일치 <이름>` 글자가 들어 있다(검토 1 회차가 찾았다: 망가뜨린 사본 셋에서 옛 측정이
  요구값을 그대로 냈다). SC-06 · SC-07 은 조건 문구에 적은 손으로 센 답이 시험 파일의 `check` 줄에 글자 그대로 있는지도 잰다 — 시험의 답을 바꾸면 측정 값이 떨어진다.
  시험의 가짜 codex 는 인자를 거부하기 전에 호출을 적고, codex 성공 기록은 가짜 codex 만 내는 태그로 센다 — 안 그러면 `--full-auto` 없음 줄이 떨어질 수 없고 대체 경로가
  남긴 기록이 codex 성공 기록으로 잡힌다(검토 2 회차가 찾았다)
- 오라클 해소: SC-08 — 훅 파일에서 codex 인자 줄을 그대로 떼어 이 기계의 codex 에 `--help` 와 함께 넘긴 종료 코드다. 편집 전 훅의 인자가 양성 대조(종료 코드 2)다.
  이 대조는 이 기계의 codex 판에 묶여 있다 — 근거 파일은 최신 0.156.1 문서가 `--full-auto` 를 「없어질 예정이지만 남아 있는」 것으로 적는다고 옮겼다. QA 전에 codex 가 올라가
  둘째 줄이 `rc=0` 이 되면 셋째 줄 `codex=` 로 그 사실을 확인하고 개정 파일로 둘째 줄을 고친다
- 오라클 해소: ER-01 · ER-02 · AP-01 · AP-03 · DG-02 · RE-02 — 편집 전 판과 파일마다 비교한 더한 줄 계산이다. 각각 양성 대조가 붙어 있다
- 오라클 해소: ER-03 · AR-01 · DG-01 · DG-03 · DG-04 · DG-06 — 커밋 기록과 봉인 검증 함수를 실제로 돌린 출력이다. 예행 저장소 변형 다섯이 양성 대조다
- 커버리지 해소: SK-01 ~ SK-05 · SC-01 ~ SC-07 · AR-02 · RE-01 · RE-02 — 산문의 파일 이름은 측정 `m <조건 ID>` 가 공통 정의의 변수(`$LIB` · `$REF` · `$PRM` · `$TFL` · `$DIG` · `$KZN` ·
  `$SCH` · `$DSN` · `$RDM` · `$TLR` · `$TPI` · `$TCS`)로 연다(파일과 변수의 대응은 `common.sh` 머리). 토큰은 `m.sh` 의 같은 ID 갈래에 글자 그대로 있다. 읽기만 하는 파일
  (`reflect-kit/hooks/hooks.json` · `reflect-kit/.claude-plugin/plugin.json`)은 `m.sh` 갈래 안에 경로 그대로 있다. SK-03 의 `reflect-kit/` 는 `grep -rn` 의 인자(`"$E/reflect-kit"`),
  SC-01 · SC-05 · SC-06 의 `/bin/bash` 와 PATH 값은 `m.sh` 의 `P32` 와 `/bin/bash` 인자, SC-04 의 훅 이름 셋은 `$REF` · `$PRM` · `$TFL`, SC-02 의 `.errors.log` 는 시험이 여는
  파일이라 시험 출력 줄로 잰다. RE-01 의 `reflect-kit/hooks/_lib-project-id.sh` 는 새 파일 목록에 **없어야** 하는 자리라 측정 출력이 그 경로를 안 내는 것이 판정이다.
  SC-03 의 `haiku-4.5` 는 `m.sh` `SC-03)` 갈래의 정규식 `haiku-4\.5` 다 — 점을 글자로 찾으려고 역슬래시를 넣어 글자 그대로는 안 맞는다(검토 반영으로 SC-03 산문에 두 번 나오면서
  검출기에 새로 걸렸다)
- 커버리지 해소: ER-01 · ER-03 — `.harness/.meta/kaizen-0924/phase12-notes.md` · `.harness/.meta/evidence/phase12.md` 는 공통 정의의 `$NOTES` · `$EVID` 다. ER-03 의 넘김 문자열과
  공유 경로는 `m.sh` `ER-03)` 갈래 `toks` · `not_other` 의 인자다(`0.3.0` 은 토큰 `` 버전: `0.3.0` `` 의 일부, `ci.yml` 은 `.github/workflows/ci.yml` 의 줄임)
- 커버리지 해소: AR-01 — `reflect-kit/` 는 `unsigned_on` 의 인자, `.harness/` 는 `scope` 블록 줄과 `verify_seal` 이 도는 폴더, `harness/references/contract-schema.md` 는 권장 형태의 출처다
- 검출기는 공백 든 코드 조각 안의 인자를 읽지 못한다 — 위 해소 줄이 전부 그 경우다
- 편집 전부터 있던 경고(markdownlint MD060 · MD031 · MD032 · MD034 등)는 범위 밖이다 — DG-02 는 더한 줄의 새 경고만 잰다
- notes 에 함께 적는다(조건으로는 재지 않는다): reflect-kaizen §0 실측값(`SELFTEST_OK` · `singleton_share 0.887` · ledger 없음)과 §1 · §2 를 안 돌린 사유 · 실제 로그 전체에
  `collect_status 30` 을 돌린 값(봉인 전 실측 절) · 설치본 갱신 전까지 수집이 계속 멈춰 있다는 한 줄 · 「넘기는 것」 에 README `버전: `0.3.0`` 줄(실제 0.7.1 — 버전을 적지
  말지 다음 사이클이 정한다) · `docs/reflect-kit/` 페이지(Final F2 — `scripts/detect-docs-drift.py` 가 `reflect-kit/skills/` 를 `docs/reflect-kit/` 로 잇는다) ·
  Final 이 볼 한 줄 — `harness/agents/qa-evaluator.md` Step 3.4 는 워크트리 폴더 이름으로 prompt 로그 폴더를 찾는다. reflect-kit 새 판이 배포되면 워크트리 세션의 새 발언은
  본 레포 폴더로 가므로, 다음 사이클 Phase 3 이 고치기 전까지 그 단계는 워크트리 계약에서 새 발언을 하나도 못 읽고 조용히 넘어간다 · `## 다음 사이클 메모` 에 — `facets_unmatched` 는
  session-meta 의 `project_path` 가 지워진 워크트리를 가리키면 워크트리 폴더 이름으로 남긴다(`scripts/collect-kaizen-data.py:421` 은 `/.claude/worktrees/` 앞에서 잘라 본 레포로 묶는다.
  지금 facets 18 개는 경로가 전부 살아 있어 영향이 없다) · 러닝북 검증의 `scripts/sync-evals.py --check-only` 종료 코드. 이 값은 조건으로 걸지 않는다 — 그 스크립트의 대상 목록
  `TARGET_KITS` 에 reflect-kit 이 없어 이 Phase 의 변경이 결과를 바꿀 수 없다
- 기능 조건 20 · 전체 조건 줄 29
- 사용자가 할 일: 없음 — 이 Phase 가 끝나도 실제 수집은 Final 배포 뒤 reflect-kit 설치본이 새 판으로 바뀌어야 살아난다(Final 몫)

## 회귀 게이트 — 측정 공통 정의와 봉인 전 실측

모든 조건의 측정은 아래 `common.sh` 와 `m.sh` 를 차례로 `.` 으로 읽은 **bash** 셸에서 돈다 — `common.sh` 는 bash 가 아니면 `NOT_BASH` 를 찍고 종료 코드 2 로 끝난다
(Claude Code 의 zsh 는 따옴표 없는 변수를 쪼개지 않고 `grep` 을 다른 검색 프로그램으로 바꿔 부른다 — Phase 5 실측). `m` 은 도우미 함수와 두 판 폴더가 없으면
`HELPER_MISSING` · `SNAPSHOT_MISSING` 을 내고 멈춘다 — 그래서 조건마다 `type m` 하나로 정의 확인을 대신한다. 세 블록을 각 블록 첫 `#` 주석 줄(셔뱅 다음)의 이름 그대로
한 폴더에 저장하고 그 폴더를 `K` 에 넣는다. `END_UNRESOLVED` 가 찍히면 셸이 종료 코드 2 로 끝난다.
`new-warnings.sh` 옆에는 `node_modules` 를 `/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/de8c7935-a5b6-4df5-9106-fafa73c288a0/scratchpad/p1build/node_modules` 로 잇고
`cfg.markdownlint-cli2.jsonc` = `{ "config": { "MD013": false } }` 를 둔다 — 준비 단계 실측(2026-09-25): 그 자리의 `.bin/markdownlint-cli2 --version` 첫 줄이
`markdownlint-cli2 v0.23.2 (markdownlint v0.41.1)`. 없으면 그 폴더에서 `npm install --no-save markdownlint-cli2@0.23.2` 부터 돌린다.
그 밖의 준비 단계 실측(2026-09-25): `command -v shellcheck` → `/opt/homebrew/bin/shellcheck` · `command -v jq` → `/usr/bin/jq` · `command -v zsh` → `/bin/zsh` ·
`command -v codex` → 있음(`codex --version` → `codex-cli 0.154.0`) · `/bin/bash --version` 3.2.57 · `/usr/bin/git --version` 2.54.0(Apple Git-157, `--path-format` 을 받는다) · `python3` 있음.
SC-08 은 codex 가 없으면 `CODEX_MISSING` 을, DG-02 는 shellcheck 가 없으면 `SHELLCHECK_MISSING` 을 내고 멈춘다. 새 시험 셋은 zsh 가 없으면 zsh 경우를 `건너뜀` 으로 적고 세지 않는다 —
그때 끝 줄의 경우 수가 하나 줄어 SC-05 · SC-06 이 요구값과 달라진다(이 기계에는 zsh 가 있다).
`common.sh` 의 `R` 은 예행 저장소를 가리킬 때만 쓴다 — 비우면 작업 폴더다. 두 판을 `${TMPDIR:-/tmp}/p12m.XXXXXX` 에 푸니 `TMPDIR` 를 스크래치 폴더로 두고 읽는다.

```bash
# common.sh — 측정 공통 정의. bash 로 읽는다 (zsh 는 배열 첨자가 1 부터이고 따옴표 없는 변수를 쪼개지 않는다)
[ -n "${BASH_VERSION:-}" ] || { echo "NOT_BASH — bash -c 안에서 다시 읽는다"; exit 2; }
export LC_ALL=C.UTF-8   # 번역투 정규식이 글자 단위로 돌아야 한다
cd "${R:-/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/kaizen-0924}" || exit 2
B=82b2493da582554a0ae4c1ee36db1bb3ba7c511b                  # 이 Phase 시작 HEAD
SIG='Kaizen-Phase: kaizen-0924-p12-reflect-kit'
CF=.harness/sprint-contract-kaizen-0924-p12-reflect-kit.md
AM=.harness/sprint-amendments-kaizen-0924-p12-reflect-kit.md
NOTES=.harness/.meta/kaizen-0924/phase12-notes.md
EVID=.harness/.meta/evidence/phase12.md
END=$( [ -f "$AM" ] && sed -n 's/^end_sha:[[:space:]]*//p' "$AM" | tail -1 )
if [ -z "$END" ] || ! git rev-parse -q --verify "$END^{commit}" >/dev/null; then
  echo "END_UNRESOLVED — 측정을 멈춘다. HEAD 로 바꿔 재지 않는다"; exit 2
fi
: "${K:?도우미 폴더를 K 에 넣는다}"
LIB=reflect-kit/hooks/_lib-project-id.sh
REF=reflect-kit/hooks/log-reflection.sh
PRM=reflect-kit/hooks/log-prompt.sh
TFL=reflect-kit/hooks/log-tool-failure.sh
DIG=reflect-kit/skills/reflect-digest/SKILL.md
KZN=reflect-kit/skills/reflect-kaizen/SKILL.md
SCH=reflect-kit/docs/SCHEMA.md
DSN=reflect-kit/docs/DESIGN.md
RDM=reflect-kit/README.md
TLR=reflect-kit/evals/hooks/log-reflection-test.sh
TPI=reflect-kit/evals/hooks/project-id-test.sh
TCS=reflect-kit/evals/hooks/collect-status-test.sh
FILES=("$LIB" "$REF" "$PRM" "$TFL" "$DIG" "$KZN" "$SCH" "$DSN" "$RDM" "$TLR" "$TPI" "$TCS")
MDS=("$DIG" "$KZN" "$SCH" "$DSN" "$RDM")
SHS=("$LIB" "$REF" "$PRM" "$TFL" "$TLR" "$TPI" "$TCS")
STATUS_TPL='수집 상태: Stop 실패 시도 <n>회 (codex 실패 <c> · 대체 경로 실패 <f> · 대체 경로 성공 <u> · 분석 전 중단 <p>; 고유 세션 <s>) / 기록된 세션 <k> / 엔트리 <e> / 마지막 기록 <ISO8601 | 없음>'
FACETS_TPL='facets 대조: facets <t>개 · 마찰 있는 세션 <m>개 · 그중 reflections 없음 <x>개 (facets 읽기 실패 <a> · session-meta 읽기 실패 <b>)'
WARN='⚠ 수집 멈춤 — 엔트리 0은 문제 없음이 아니다'
T=$(mktemp -d "${TMPDIR:-/tmp}/p12m.XXXXXX") || exit 2; mkdir -p "$T/B" "$T/E"
# 두 판을 풀어 둔 폴더에서 잰다 — 작업 폴더에 남은 다른 Phase 의 미커밋 변경이 끼지 않는다
git archive "$B" | tar -x -C "$T/B"; git archive "$END" | tar -x -C "$T/E"
# sect <파일> <제목 앞부분> — 그 제목부터 같은 깊이 이하의 다음 제목 전까지. 코드 펜스 안의 `#` 줄은 제목으로 보지 않는다
sect() { awk -v h="$2" '
  /^[[:space:]]*(```|~~~)/ { fence = !fence }
  !f && !fence && index($0, h) == 1 { f = 1; lvl = match($0, /[^#]/) - 1; print; next }
  f && !fence && /^#+ / { l = match($0, /[^#]/) - 1; if (l <= lvl) exit }
  f' "$1"; }
# between <파일> <시작 줄 앞부분> <끝 줄 앞부분> — 시작 줄부터 끝 줄 앞까지 (Process 의 번호 단계 하나)
between() { awk -v a="$2" -v z="$3" 'index($0, a) == 1 { f = 1 } f && index($0, z) == 1 { exit } f' "$1"; }
# gline <파일> <줄 앞부분> — 그 앞부분으로 시작하는 줄. Gotcha 와 표 행은 한 줄이다
gline() { awk -v p="$2" 'index($0, p) == 1' "$1"; }
# toks <글> <토큰…> — 토큰마다 글 안에서 그 토큰이 든 줄 수
toks() { local s="$1"; shift; for t in "$@"; do printf '%s ' "$(printf '%s\n' "$s" | grep -cF -- "$t")"; done; echo; }
# seq_ok <글> — 줄 머리 `N. **` 번호가 1 부터 빠짐없이 이어지면 「1 마지막번호」, 아니면 「0 번호들」
seq_ok() { printf '%s\n' "$1" | grep -oE '^[0-9]+\. \*\*' | tr -dc '0-9\n' | awk '{a[NR]=$1} END{ok=1; for(i=1;i<=NR;i++) if (a[i]+0 != i) ok=0; printf "%d %d\n", ok, NR}'; }
url()   { grep -oE 'https?://[^ )>"`]+' | sed -E 's/[.,;:]+$//' | sort -u; }
# 편집 전 판에 없는 새 파일은 빈 파일과 비교한다
added() { for f in "$@"; do if [ -f "$T/B/$f" ]; then git diff --no-index -U0 "$T/B/$f" "$T/E/$f"; else git diff --no-index -U0 /dev/null "$T/E/$f"; fi; done | grep '^+' | grep -v '^+++'; }
# lastline <명령…> — 명령 출력의 끝 줄과 종료 코드 (| tail 로 종료 코드를 잃지 않게 변수로 받는다)
lastline() { local o rc; o=$("$@" 2>&1); rc=$?; printf '%s rc=%s\n' "$(printf '%s\n' "$o" | tail -1)" "$rc"; }
# cxargs <훅> — log-reflection.sh 의 `codex exec \` 다음 줄부터 `  - ` 로 시작하는 줄 앞까지 (codex 에 넘기는 인자 줄)
cxargs() { awk '/codex exec \\$/ { f = 1; next } f && /^  - / { exit } f { sub(/[[:space:]]*\\$/, ""); print }' "$1"; }
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
K02='(을|를) ?(처리|관리)(합니다|한다)|에 대해서?|하도록 (합니다|한다)|에 의(해|하여)|되어 있(는 경우|을 때)|(표시|적용|호출|생성|반환)(됩니다|된다)'
```

```bash
# m.sh — 조건마다 재는 값을 한 줄씩 낸다. common.sh 를 읽은 bash 에서 `m <조건 ID>` 로 부른다
m() {
  local E=$T/E S L f n o rc
  # 도우미가 하나라도 없으면 grep -c 가 조용히 0 을 낸다 — 멈춘다
  for fn in sect between gline toks seq_ok url added lastline cxargs mine unsigned_on not_other my scope fm_get verify_seal; do
    type "$fn" >/dev/null 2>&1 || { echo "HELPER_MISSING $fn"; return 2; }; done
  [ -n "${T:-}" ] && [ -d "$T/B" ] && [ -d "$E" ] || { echo "SNAPSHOT_MISSING"; return 2; }
  local CS7='bash -c '"'"'. "${1}/hooks/_lib-project-id.sh"; shift; collect_status "$@"'"'"' _ "${CLAUDE_PLUGIN_ROOT}" 7 ~/.claude/logs/<bucket>'
  local CS30='bash -c '"'"'. "${1}/hooks/_lib-project-id.sh"; shift; collect_status "$@"'"'"' _ "${CLAUDE_PLUGIN_ROOT}" 30 ~/.claude/logs/<bucket>'
  local FU7='bash -c '"'"'. "${1}/hooks/_lib-project-id.sh"; shift; facets_unmatched "$@"'"'"' _ "${CLAUDE_PLUGIN_ROOT}" 7 <프로젝트 이름>'
  local P32='/usr/bin:/bin:/usr/sbin:/sbin'   # 이 PATH 의 bash 는 /bin/bash 3.2 다
  case "$1" in
  SK-01)  # reflect-digest — 수집 상태: Gotcha 13 · Process 4 · 출력 포맷 · project=all 머리 · Gotcha 번호
    L=$(gline "$E/$DIG" '13. **엔트리 0 을 「문제 없음」 으로 읽지 마라 — 수집기가 멈췄을 수 있다.**')
    toks "$L" '13. **엔트리 0 을' 'Stop 실패 시도 849 번(고유 세션 55), 기록된 세션 0, 마지막 기록 2026-08-28' \
      '요약 머리 첫 줄은 Process 4 단계의 `collect_status` 출력이다' '`## 승격 후보` 에는 `(수집 멈춤 — 산출하지 않는다)` 한 줄만 쓰고' \
      '`## 환경 액션 아이템` 에 수집 복구 한 줄을 `.errors.log` 의 가장 최근 `err=` 값과 함께 올린다'
    S=$(between "$E/$DIG" '4. **엔트리 파싱**' '5. **actionability 분리**')
    toks "$S" '**파싱 전에 수집 상태부터 잰다** (Gotcha #13)' "$CS7"
    S=$(sect "$E/$DIG" '## 출력 포맷')
    toks "$S" '제목 아래 `⚠ 수집 멈춤` 줄만은 엔트리 0 이고 Stop 실패 시도가 1 이상일 때만 싣는다 (Gotcha #13).' "$STATUS_TPL" "$WARN" \
      '- fail:codex-exit-N: Y건 (가장 최근 `err=` 값)' '- fallback:claude-exit-N / fallback:claude-used: V건 / U건 (가장 최근 `err=` 값)'
    S=$(sect "$E/$DIG" '### 4. Given-When-Then 동작 계약')
    toks "$S" "  $STATUS_TPL" "  $WARN" '- `수집 상태` 줄은 전 bucket 을 넘긴 `collect_status` 출력이며 값이 0 이어도 싣는다.'
    seq_ok "$(sect "$E/$DIG" '## Gotchas')" ;;
  SK-02)  # reflect-digest — facets 대조: Gotcha 14 · 데이터 소스 · Process 9 · 출력 절
    L=$(gline "$E/$DIG" '14. **facets 를 빈도에 더하지 마라 — 대조에만 쓴다.**')
    toks "$L" '14. **facets 를' '`cluster_freq` · `project_count` · 4 축 · precedence 에 더하면 같은 세션을 두 번 세고 척도가 섞인다' \
      '쓰는 곳은 `## 인사이트 세션 분석과 대조` 절 하나다' '폴더가 없으면 `facets 대조: (없음)` 한 줄로 넘어간다'
    toks "$(sect "$E/$DIG" '## 데이터 소스')" '- `~/.claude/usage-data/facets/*.json` + `session-meta/<session_id>.json` (선택)' \
      '**대조 전용**이다 (Gotcha #14)' 'session-meta 의 `project_path` 로 잇는다'
    S=$(between "$E/$DIG" '9. **리포트 출력**' '10. **결과 저장')
    toks "$S" '`## 인사이트 세션 분석과 대조 (합산 금지)` 절에는 아래 출력을 그대로 옮긴다' "$FU7" '- 이 절의 수는 7 · 8 단계 어디에도 더하지 않는다 (Gotcha #14)'
    S=$(sect "$E/$DIG" '## 출력 포맷')
    toks "$S" '## 인사이트 세션 분석과 대조 (합산 금지)' '`facets_unmatched` 출력을 그대로 옮긴다. facets 폴더가 없으면 `facets 대조: (없음)` 한 줄이다.' \
      "$FACETS_TPL" '- <session_id> · <start_time> · <project_path> — <friction_detail 원문>' ;;
  SK-03)  # reflect-digest 프로젝트 ID — 본 레포 이름 · 워크트리 폴더를 옮기지 않음 · project_root 헬퍼, 킷 전체의 옛 표기 0
    toks "$(sect "$E/$DIG" '## 프로젝트 ID')" \
      '- **기본**: `<basename(본 레포 root)>` — 충돌 없는 경우 hash 없이 사용. 워크트리 안에서 불러도 워크트리 폴더 이름이 아니라 본 레포 이름이다' \
      '- **워크트리 이름 폴더**: 이 규칙 전에 워크트리 이름으로 생긴 폴더는 옮기지 않는다' '- `project_root "$cwd"` — 본 레포 root (링크된 워크트리면 본 레포, git 밖이면 cwd)'
    grep -rn 'basename(git-root)' "$E/reflect-kit" | grep -c . ;;
  SK-04)  # reflect-kaizen — §0 수집 상태 · (0) 출력 줄 · 판정 모델 이름
    S=$(sect "$E/$KZN" '### 0. 파편화 지표 선행 확인')
    toks "$S" '- **수집 상태도 본다.** 파편화 지표는 이미 쌓인 기록만 재므로 수집기가 멈춰도 멀쩡해 보인다.' \
      '`calibration_confidence: low` 를 선언한다 — 파편화 임계 초과와 같은 효력이다' \
      '`post_freq == 0` 은 재발이 없었다는 뜻이 아니라 못 셌다는 뜻이다 (2026-09-14~23: Stop 실패 시도 849 번 · 기록 0)' "$CS30"
    toks "$(sect "$E/$KZN" '### (0) 파편화 지표')" '- `collect_status` 출력 원문 — `⚠ 수집 멈춤` 줄이 있으면 판정은 `low` 다'
    toks "$(sect "$E/$KZN" '### (1) LLM-as-judge 일치도')" '- sample: 10 건 / 모델: haiku / 모수: `claude_behavior` 만' '모델: haiku-4.5' ;;
  SK-05)  # 문서 — SCHEMA §3 · §5, DESIGN 에러 관측성 · 워크트리 절 · 표 행, README
    S=$(sect "$E/$SCH" '## 3. 훅 에러 로그')
    toks "$S" '- `fail:codex-exit-<N> session=<> err=<한 줄>` — codex exec 비정상 종료' '- `fallback:claude-used session=<>`' \
      '- `fallback:claude-exit-<N> session=<> err=<한 줄>`' '- `fallback:claude-empty-output session=<>`' '- `skip:fallback-unavailable session=<>`' \
      '- `fail:tag-field-unresolved session=<>`' '`err=` 는 줄 끝까지다 (공백 포함).' '`error` · `ERROR` 로 시작하는 첫 줄, 없으면 비어 있지 않은' \
      '첫 줄 하나를 가린 뒤 200 자로 자른다 — codex 는 성공해도 stderr 에 프롬프트 전문을 찍으므로 전문은 남기지 않는다.' '대체 경로는 stderr 가 비면 stdout 에서 고른다.'
    S=$(sect "$E/$SCH" '## 5. Project ID 포맷')
    toks "$S" '기본 `<basename(본 레포 root)>`' '링크된 워크트리(git-dir 과 common-dir 이 다름)이고 공통 git 폴더 이름이' \
      '- 충돌 판정 마커(`.project-root`)와 hash 입력도 같은 root 를 쓴다' '`DESIGN.md` 결정 #3 상세의 `### 워크트리` 절' '- basename만 같고 다른 repo라도 hash가 달라 충돌하지 않는다'
    S=$(sect "$E/$DSN" '## 에러 관측성')
    toks "$S" '- `fail:codex-exit-<N> session=<> err=<한 줄>` — codex exec 비정상 종료' '- `fallback:claude-exit-<N> session=<> err=<한 줄>`' \
      '`err=` 의 뽑는 규칙은 `SCHEMA.md` §3 이 정본이다.' '요약 머리의 `collect_status` 줄이 기록 없이 끝난'
    S=$(sect "$E/$DSN" '### 워크트리 (2026-09-25)')
    toks "$S" '(2026-09-25 실측: 로그 폴더 31 개 중 12 개가 워크트리 이름)' '(git-dir 과 common-dir 이 다름)이고 공통 git 폴더 이름이 `.git` 일 때만 그 부모를 본 레포로 쓴다' \
      '- 서브모듈의 공통 git 폴더는 상위 레포의 `.git/modules/<이름>` 이다' '- `git init --separate-git-dir` 로 만든 본 체크아웃은 git-dir 과 common-dir 이 같다' \
      'bare 레포에 붙인 워크트리는' '이미 워크트리 이름으로 생긴 폴더는 **옮기지 않는다.**' '그 12 개 폴더에는 reflections 가 한 건도 없고'
    echo "row=$(gline "$E/$DSN" '| 같은 레포의 링크된 워크트리에서 호출 |' | grep -c .)"
    toks "$(cat "$E/$RDM")" '`project_id` = `<basename(본 레포 root)>` (Hybrid 기본, v0.3.0+ — 워크트리 안에서도 본 레포 이름)' \
      '`collect_status` · `facets_unmatched` (digest 머리의 수집 상태 · facets 대조)' '- `codex` CLI (`codex exec -s read-only`로 세션 분석)' \
      '- `claude` CLI — codex 가 실패하면 `claude -p --model haiku` 로 한 번 더 분석한다' ;;
  SC-01)  # codex 호출 인자 — 시험 전체 · 인자 줄 · 음성 대조(편집 전 훅)
    lastline bash "$E/$TLR"
    lastline env PATH="$P32" /bin/bash "$E/$TLR"
    # 불일치 줄도 「일치 <이름>」 글자를 품는다 — 일치로 시작하는 줄만 남겨 센다 (SC-01 ~ SC-04 · SC-06 · SC-07)
    o=$(bash "$E/$TLR" 2>&1 | grep '^일치 ')
    toks "$o" '일치 codex 인자 -s read-only' '일치 codex 인자 --full-auto 없음' '일치 codex 성공 시 claude 호출 없음' '일치 codex 성공 기록' '일치 codex 성공 실패 줄 없음'
    echo "ro=$(cxargs "$E/$REF" | grep -cxE '[[:space:]]*-s read-only') fullauto=$(cxargs "$E/$REF" | grep -c -- '--full-auto')"
    REFLECT_KIT_HOOKS="$T/B/reflect-kit/hooks" lastline bash "$E/$TLR" ;;
  SC-02)  # 분석기 stderr 한 줄 — 시험 줄 일곱 · stderr 를 파일로 받는 줄 · 옛 버리는 줄 0
    o=$(bash "$E/$TLR" 2>&1 | grep '^일치 ')
    toks "$o" '일치 codex 실패 err= ERROR 줄' '일치 codex 실패 err= 첫 줄' '일치 transcript 가 .errors.log 에 없음' '일치 키 조각 없음' \
      '일치 err= 200 자 이하' '일치 stdout 에서 고른 err=' '일치 codex 빈 응답 줄'
    echo "$(grep -cF -- '- >/dev/null 2> "$ana_dir/codex.err"' "$E/$REF") $(grep -cF -- '> "$ana_dir/claude.out" 2> "$ana_dir/claude.err"' "$E/$REF") $(grep -cxF -- '  - >/dev/null 2>&1' "$E/$REF") $(grep -cF -- 'claude -p --model haiku-4.5 > "$fb_tmp" 2>/dev/null' "$E/$REF")" ;;
  SC-03)  # 대체 경로 — 시험 줄 넷 · 호출 줄 · 실행 줄의 옛 모델 이름 0
    o=$(bash "$E/$TLR" 2>&1 | grep '^일치 ')
    toks "$o" '일치 claude 인자 --model haiku' '일치 claude 인자 --no-session-persistence' '일치 대체 경로 기록' '일치 대체 경로 실패 시 기록 없음'
    echo "$(grep -cF 'echo "$prompt" | REFLECT_KIT_ANALYZER=1 claude -p --model haiku --no-session-persistence \' "$E/$REF") $(grep -v '^[[:space:]]*#' "$E/$REF" | grep -c 'haiku-4\.5')" ;;
  SC-04)  # 분석기 표식 · 임시 파일 — 시험 줄 일곱 · 세 훅 모두 표식 검사가 첫 source · mktemp · 입력 읽기보다 앞
    o=$(bash "$E/$TLR" 2>&1 | grep '^일치 ')
    toks "$o" '일치 codex 분석기 표식' '일치 claude 분석기 표식' '일치 표식 — Stop 분석 안 함' '일치 표식 — log-prompt.sh 안 적음' \
      '일치 표식 — log-tool-failure.sh 안 적음' '일치 표식 없음 — log-prompt.sh 적음' '일치 TMPDIR 비었음'
    for f in "$REF" "$PRM" "$TFL"; do
      awk -v n="$(basename "$f")" '$0 == "[ -n \"${REFLECT_KIT_ANALYZER:-}\" ] && exit 0" { g = g ? g : NR; c++ }
        !w && /^(source |input=\$\(cat\)|bg_input_file=)/ { w = NR }
        END { printf "%s:%d:%s ", n, c, (g && w && g < w) ? "ok" : "no" }' "$E/$f"; done; echo ;;
  SC-05)  # 본 레포 root — 알려진 답 시험 두 해석기 · 음성 대조 · 쓰기 id 가 root 를 한 곳에서 받는다
    lastline bash "$E/$TPI"
    lastline env PATH="$P32" /bin/bash "$E/$TPI"
    PROJECT_ID_LIB="$T/B/$LIB" lastline bash "$E/$TPI"
    echo "$(awk '/^compute_project_id\(\) \{/,/^\}/' "$E/$LIB" | grep -c 'show-toplevel') $(awk '/^compute_project_id\(\) \{/,/^\}/' "$E/$LIB" | grep -c 'repo_root=$(project_root "$cwd")')" ;;
  SC-06)  # collect_status — 알려진 답 시험 두 해석기 · 시험 줄 여섯 · 조건 문구의 답이 시험 check 줄에 있다
    lastline bash "$E/$TCS"
    lastline env PATH="$P32" /bin/bash "$E/$TCS"
    o=$(bash "$E/$TCS" 2>&1 | grep '^일치 ')
    toks "$o" '일치 7 일 · 두 폴더' '일치 all · 두 폴더' '일치 멈춤 — 엔트리 0 · 실패 1 이상' '일치 빈 폴더 — 경고 없음' '일치 일수 잘못 — 멈춤' '일치 zsh — 멈춤'
    toks "$(cat "$E/$TCS")" 'check "7 일 · 두 폴더" "수집 상태: Stop 실패 시도 5회 (codex 실패 4 · 대체 경로 실패 3 · 대체 경로 성공 1 · 분석 전 중단 2; 고유 세션 4) / 기록된 세션 1 / 엔트리 1 / 마지막 기록 $D1' \
      'check "all · 두 폴더" "수집 상태: Stop 실패 시도 6회 (codex 실패 5 · 대체 경로 실패 4 · 대체 경로 성공 1 · 분석 전 중단 2; 고유 세션 5) / 기록된 세션 2 / 엔트리 3 / 마지막 기록 $D1' ;;
  SC-07)  # facets_unmatched — 시험 줄 넷 · 조건 문구의 답과 세션 줄 둘이 시험 check 줄에 있다
    o=$(bash "$E/$TCS" 2>&1 | grep '^일치 ')
    toks "$o" '일치 facets 7 일 · alpha' '일치 facets 7 일 · all' '일치 facets all · alpha' '일치 facets 폴더 없음'
    # 세션 줄의 $(…) · $W 는 작은따옴표 안이라 글자 그대로 찾는다 — 시험 파일의 기대 줄 원문이다
    toks "$(cat "$E/$TCS")" 'check "facets 7 일 · alpha" "facets 대조: facets 4개 · 마찰 있는 세션 3개 · 그중 reflections 없음 2개 (facets 읽기 실패 1 · session-meta 읽기 실패 1)' \
      '- S-miss · $(jq -r .start_time "$W/usage/session-meta/S-miss.json") · $W/repos/alpha — missed friction' \
      '- S-wt · $(jq -r .start_time "$W/usage/session-meta/S-wt.json") · $W/wt/alpha-wt — worktree friction' ;;
  SC-08)  # 이 기계의 codex CLI 가 훅이 넘기는 인자 묶음을 받는다 — 편집 전 훅의 묶음은 거부한다
    command -v codex >/dev/null 2>&1 || { echo "CODEX_MISSING"; return 2; }
    local ana_dir=$T/ana out_tmp=$T/o side
    mkdir -p "$ana_dir"
    for side in E B; do
      eval "set -- $(cxargs "$T/$side/$REF" | tr '\n' ' ')"
      codex exec "$@" - --help < /dev/null > /dev/null 2> "$T/cx.err"; rc=$?
      printf '%s rc=%s args=%s first=%s\n' "$side" "$rc" "$#" "$(grep -m1 . "$T/cx.err")"
    done
    # 판정에 쓰지 않는다 — codex 가 올라가 옛 묶음을 받아들이면 둘째 줄이 바뀌므로 환경 변화인지 가르려고 적어 둔다
    echo "codex=$(codex --version 2>&1 | head -1)" ;;
  ER-01)  # 새로 생긴 URL 이 근거 파일에 있다 — 열두 파일은 파일마다 편집 전 판과 비교, notes 는 URL 전부
    for f in "${FILES[@]}"; do comm -13 <( [ -f "$T/B/$f" ] && url < "$T/B/$f" ) <(url < "$E/$f"); done | sort -u | comm -23 - <(url < "$E/$EVID") | grep -c .
    if [ -f "$E/$NOTES" ]; then url < "$E/$NOTES" | comm -23 - <(url < "$E/$EVID") | grep -c .; else echo NOTES_MISSING; fi ;;
  ER-02)  # 더한 줄의 번역투 6 종 · 특정 앱 · 도구 이름
    echo "added=$(added "${FILES[@]}" | grep -c .) k02=$(added "${FILES[@]}" | grep -cE "$K02") names=$(added "${FILES[@]}" | grep -ciE 'fit-?pal|fit_pal|flutter[-_]playwright|playwright-mcp|chrome-devtools-mcp')" ;;
  ER-03)  # notes 문자열 · 넘김 줄의 다음 사이클 Phase · 공유 파일과 다른 Phase 파일을 건드린 커밋
    git cat-file -e "$END:$NOTES" && echo notes_committed=1 || echo notes_committed=0
    toks "$(cat "$E/$NOTES")" 'reflect-collector:P3' 'reflect-collector:P4' 'reflect-collector:P5' \
      'harness/scripts/save-feedback.sh' 'harness/agents/qa-evaluator.md' 'qa-evaluation-guide.md' 'hooks.json' 'asyncRewake' 'last_assistant_message' \
      'plugin.json' '버전: `0.3.0`' 'docs/reflect-kit/' 'singleton_share 0.887' 'promotions-ledger' \
      'bash reflect-kit/evals/hooks/log-reflection-test.sh' 'bash reflect-kit/evals/hooks/project-id-test.sh' 'bash reflect-kit/evals/hooks/collect-status-test.sh' \
      '## 바꾼 파일' '## 반영한 처리 배정표 키' '## 미반영 키와 사유' '## 넘기는 것' '## changelog 한 단락' '## 킷 로그 한 단락' '## 다음 사이클 메모'
    # 넘김은 받을 Phase 와 같은 줄로 센다 — 낱말만 세면 다른 절에 나온 낱말로 넘김 줄을 빠뜨려도 1 이 된다
    echo "$(grep -F 'save-feedback.sh' "$E/$NOTES" | grep -cF '다음 사이클 Phase 4') $(grep -F 'qa-evaluator.md' "$E/$NOTES" | grep -cF '다음 사이클 Phase 3') $(grep -F 'hooks.json' "$E/$NOTES" | grep -cF '다음 사이클 Phase 4')"
    not_other "$B" "$END" "$SIG" .claude-plugin/marketplace.json reflect-kit/.claude-plugin/plugin.json README.md CLAUDE.md \
      .harness/.meta/orchestrator-audit-log.md .harness/.meta/kaizen-failure-count.yaml .claude/kaizen-input/insights-report.md \
      .github/workflows/ci.yml .harness/stale-values.yaml .claude/skills harness scripts docs \
      reflect-kit/hooks/hooks.json reflect-kit/references reflect-kit/scripts reflect-kit/skills/reflect-promote reflect-kit/skills/codex-kaizen | grep -c . ;;
  AR-01)  # 허용 경로 · 서명 · 봉인 · 범위 선언 블록
    unsigned_on "$B" "$END" "$SIG" reflect-kit | grep -c .
    echo "$(my | grep -v '^\.harness/' | grep -vxF -f <(printf '%s\n' "${FILES[@]}") | grep -c .) $(my | grep -cxF -f <(printf '%s\n' "${FILES[@]}"))"
    find .harness -type f -name 'sprint-contract*.md' -print0 | while IFS= read -r -d '' f; do verify_seal "$f"; done \
      | awk '$1=="SEAL_BROKEN"{print $2}' | sed 's#^\./##' | sort -u | comm -12 - <( { my; echo "$CF"; } | sort -u) | grep -c .
    verify_seal "$E/$CF" | cut -d' ' -f1
    diff <(scope "$E/$CF" | grep -vxF '.harness/' | sort) <(printf '%s\n' "${FILES[@]}" | sort) >/dev/null && echo "scope_same=1" || echo "scope_same=0"
    scope "$E/$CF" | grep -cxF '.harness/' ;;
  AR-02)  # 코드와 문서가 같은 것을 말한다 — 태그 목록 · 출력 틀 · 함수 정의 · 가리키는 절 · 훅 등록 · 시험 실행 비트
    diff <(sect "$E/$SCH" '### 사유 태그' | grep -oE '^- `[^` ]+' | sed 's/^- `//' | sort) <(sect "$E/$DSN" '## 에러 관측성' | grep -oE '^- `[^` ]+' | sed 's/^- `//' | sort) >/dev/null \
      && echo "tags_same=1 n=$(sect "$E/$SCH" '### 사유 태그' | grep -cE '^- `')" || echo "tags_same=0"
    python3 - "$E/$LIB" "$STATUS_TPL" "$FACETS_TPL" "$WARN" <<'PY'
import re, sys
src = open(sys.argv[1], encoding="utf-8").read()
def fmt(prefix, fills):
    m = re.search(r"printf '(" + re.escape(prefix) + r"[^']*)\\n'", src)
    if not m: return "MISSING"
    s = m.group(1)
    for x in fills: s = s.replace("%d" if x != "<ISO8601 | 없음>" else "%s", x, 1)
    return s
st = fmt("수집 상태:", ["<n>", "<c>", "<f>", "<u>", "<p>", "<s>", "<k>", "<e>", "<ISO8601 | 없음>"])
fa = fmt("facets 대조: facets", ["<t>", "<m>", "<x>", "<a>", "<b>"])
print("status_tpl=%d facets_tpl=%d warn=%d" % (st == sys.argv[2], fa == sys.argv[3], src.count("'" + sys.argv[4] + "'")))
PY
    for fn in project_root compute_project_id normalize_project_query collect_status facets_unmatched; do printf '%s ' "$(grep -c "^$fn() {" "$E/$LIB")"; done; echo
    echo "worktree_sect=$(grep -c '^### 워크트리 (2026-09-25)$' "$E/$DSN") hooks_same=$(cmp -s "$T/B/reflect-kit/hooks/hooks.json" "$E/reflect-kit/hooks/hooks.json" && echo 1 || echo 0)"
    git ls-tree "$END" -- "$TLR" "$TPI" "$TCS" | awk '{printf "%s ", $1} END {print ""}' ;;
  RE-01)  # 새 파일 목록 — 시험 셋뿐, 새 라이브러리 파일 없음
    comm -13 <(cd "$T/B" && find reflect-kit -type f | sort) <(cd "$E" && find reflect-kit -type f | sort) ;;
  RE-02)  # 있는 것을 다시 쓴다 — err= 는 redact_sensitive 로 가리고 새 가림 패턴 0 · 본 레포 root 계산은 한 함수
    echo "$(awk '/^err_line\(\) \{/,/^\}/' "$E/$REF" | grep -c 'redact_sensitive') $(added "$REF" | grep -c 'REDACTED')"
    echo "$(awk '/^project_root\(\) \{/,/^\}/' "$E/$LIB" | grep -c 'show-toplevel') $(grep -v '^[[:space:]]*#' "$E/$LIB" | grep -c 'show-toplevel') $(awk '/^facets_unmatched\(\) \{/,/^\}/' "$E/$LIB" | grep -c 'project_root "$pp"')" ;;
  AP-01)  # 더한 줄에 이 킷 플러그인 버전 값 — 값은 plugin.json 에서 읽는다
    L=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["version"])' "$E/reflect-kit/.claude-plugin/plugin.json")
    echo "version=$L $(added "${FILES[@]}" | grep -cF -- "$L")" ;;
  AP-03)  # 펜스 — V6 가 읽지 않는 docs 두 파일에 더한 줄의 펜스 줄 (V6 는 DG-05 가 잰다)
    added "$SCH" "$DSN" | grep -cE '^\+[[:space:]]*(```|~~~)' ;;
  AP-04)  # frontmatter — 고친 SKILL.md 둘의 첫 블록이 편집 전과 같고 name 줄이 폴더 이름이다
    for f in "$DIG" "$KZN"; do
      L=$(basename "$(dirname "$f")")
      printf '%s/%s ' "$(diff <(awk 'NR==1&&/^---/{fm=1;next} fm&&/^---/{exit} fm' "$T/B/$f") <(awk 'NR==1&&/^---/{fm=1;next} fm&&/^---/{exit} fm' "$E/$f") >/dev/null && echo 1 || echo 0)" \
        "$(awk 'NR==1&&/^---/{fm=1;next} fm&&/^---/{exit} fm' "$E/$f" | grep -cxF "name: $L")"; done; echo ;;
  DG-02)  # markdownlint — 더한 줄의 새 경고 · shellcheck · bash -n
    for f in "${MDS[@]}"; do k=$(printf '%s' "$f" | tr '/' '_'); cp "$T/B/$f" "$T/$k.0.md"; cp "$E/$f" "$T/$k.md"; bash "$K/new-warnings.sh" "$T/$k.0.md" "$T/$k.md"; done
    command -v shellcheck >/dev/null 2>&1 || { echo "SHELLCHECK_MISSING"; return 2; }
    echo "shellcheck=$(cd "$E" && shellcheck "${SHS[@]}" 2>&1 | grep -c .) bash_n=$(for f in "${SHS[@]}"; do bash -n "$E/$f" || echo x; done | grep -c .)" ;;
  DG-05)  # 저장소 검사 — $END 판을 git 저장소로 만든 사본에서 돈다 (작업 폴더의 다른 Phase 미커밋 변경이 끼지 않는다)
    local G=$T/G; rm -rf "$G"; cp -R "$E" "$G"
    git -C "$G" init -q && git -C "$G" add -A && git -C "$G" -c user.name=m -c user.email=m@m commit -qm snap || return 2
    # V 줄 머리에는 FAIL 이 안 찍힌다(아래 들여쓴 줄에 찍힌다) — `— OK` 로 끝나지 않는 V 줄을 센다. V2 는 templates 가 없어 SKIP 이다
    ( cd "$G" && python3 scripts/validate-plugin.py reflect-kit > "$T/vp.txt" 2>&1; echo $? > "$T/vp.rc" )
    echo "$(grep -cE '^  V([1-9]|10) ' "$T/vp.txt") $(grep -E '^  V([1-9]|10) ' "$T/vp.txt" | grep -v '^  V2 ' | grep -cv -- '— OK$') v6=$(grep -c '^  V6 code-fence        0 bare — OK$' "$T/vp.txt") rc=$(cat "$T/vp.rc")"
    ( cd "$G" && python3 scripts/validate-plugin.py --check=table-integrity,code-fence > "$T/ti.txt" 2>&1 )
    echo "tf_mine=$(grep 'FAIL' "$T/ti.txt" | grep -cF -f <(printf '%s\n' "${FILES[@]}"))"
    ( cd "$G" && python3 scripts/sync-docs.py --check-only > "$T/sd.txt" 2>&1 ); echo "sync_docs_rc=$? $(grep -cxF '  reflect-kit/README.md: 동기화됨' "$T/sd.txt")"
    ( cd "$G" && python3 scripts/run-evals.py reflect-kit > "$T/re.txt" 2>&1 ); echo "run_evals_rc=$?" ;;
  DG-06)  # 사이클 검사 — 이 Phase 몫 줄만 본다. docs-site-regen 은 Final F2 몫
    python3 scripts/validate-post-kaizen.py --since "$B" --verbose > "$T/vpk.txt" 2>&1
    grep -E '\] . (scope-isolation|doc-contracts): ' "$T/vpk.txt" | awk '{print $5, $2}'
    awk '/ scope-isolation: /{f=1;next} /^\[ /{f=0} f&&/^ +[0-9a-f]{7,40}$/{print $1}' "$T/vpk.txt" > "$T/viol.txt"
    echo "violators=$(grep -c . "$T/viol.txt") mine=$(while read -r c; do git log -1 --format=%B "$c" | grep -qxF "$SIG" && echo "$c"; done < "$T/viol.txt" | grep -c .)" ;;
  DG-01|DG-03)  # commands.analyze · commands.test 는 scripts/release.sh 만 잰다 — 이번 커밋이 그 파일을 건드린 수
    my | grep -c '^scripts/release.sh$' ;;
  DG-04)  # 구동할 앱 · 서버 — 이번 커밋의 실행 파일 가운데 훅 · 시험 셋 밖의 것
    my | grep -vE '^(\.harness/|reflect-kit/hooks/|reflect-kit/evals/hooks/)' | grep -cE '\.(dart|ts|tsx|js|rs|go|py|sh)$' ;;
  SC-00|RE-00) echo "UNKNOWN $1"; return 2 ;;
  *) echo "UNKNOWN $1"; return 2 ;;
  esac
}
```

```bash
#!/usr/bin/env bash
# new-warnings.sh <옛 파일> <새 파일> — 새 파일에서 더한 줄에 걸린 경고만 센다. 줄이 밀리므로 전체 수 차이로 세지 않는다
# 줄 번호는 경로 뒤 첫 번째 숫자다. 탐욕 매치(^[^ ]*:)로 뽑으면 열 번호가 줄 번호로 둔갑한다 (실측 2026-09-24)
# 린터가 안 돌면 경고 0 이 조용히 나온다 — 돌았다는 줄(Linting: 1 file)이 없으면 멈춘다 (실측 2026-09-25: 옆에 node_modules 가 없어 0)
set -u
DIR=$(cd "$(dirname "$0")" && pwd)
ADDED=$(git diff --no-index -U0 -- "$1" "$2" | awk '/^@@/{split($3,a,","); s=substr(a[1],2)+0; n=(a[2]==""?1:a[2]+0); for(i=0;i<n;i++) print s+i}' | sort -u)
OUT=$("$DIR/node_modules/.bin/markdownlint-cli2" --config "$DIR/cfg.markdownlint-cli2.jsonc" "$2" 2>&1)
printf '%s\n' "$OUT" | grep -q '^Linting: 1 file' || { echo "LINT_NOT_RUN $2"; exit 2; }
LINES=$(printf '%s\n' "$OUT" | grep -E ':[0-9]+(:[0-9]+)? (error|warning) ' | sed -E 's#^([^:]*):([0-9]+).*#\2#' | sort -u)
NEWW=$(comm -12 <(printf '%s\n' "$ADDED" | grep . | sort) <(printf '%s\n' "$LINES" | grep . | sort) | wc -l | tr -d ' ')
echo "total_warning_lines=$(printf '%s\n' "$LINES" | grep -c .) added_lines=$(printf '%s\n' "$ADDED" | grep -c .) new_warnings=$NEWW"
```

**예행.** 시작 커밋에서 레포를 스크래치로 복제해(`p12d/rehearse.sh`) BUILD 가 할 커밋을 흉내 냈다 — 봉인 커밋(이 계약 초안에 digest 를 적은 판) → 다른 Phase 서명 커밋 하나
(`planning-kit/README.md`, 걸러져야 한다) → `mock.py` 를 적용한 구현 커밋 하나(열두 파일) → `end_sha` → notes 모의본(`p12d/notes-mock.md`) → `end_sha` 한 줄 더.
변형 `base` 는 구현 없이 `end_sha` 를 시작 커밋으로 둬 시작 커밋 판을 잰다. 변형 다섯은 같은 흐름에 커밋 하나를 더한다: `unsigned-shared`(서명 없이 루트 `README.md`) ·
`unsigned-mine`(서명 없이 `reflect-kit/README.md`) · `unsigned-hooksjson`(서명 없이 `reflect-kit/hooks/hooks.json`) · `signed-outside`(서명하고 `reflect-kit/.claude-plugin/plugin.json`) ·
`cross-phase`(서명하고 `harness/skills/sprint/SKILL.md` 와 `reflect-kit/skills/reflect-promote/SKILL.md` 한 커밋). 변형 다섯의 저장소는 잰 뒤 지웠다(디스크 여유가 2 GB 안팎이라).
다시 재려면 `bash p12d/rehearse.sh <이 계약 사본의 절대경로> p12d/rh-<변형> <변형>` 으로 만든다. 한 번에 재는 도우미는 `p12d/run-all.sh <예행 폴더> [조건 ID…]` 다.

**봉인 전 실측 (2026-09-25, bash 5.3.9).** 예행 판 = 이 계약 초안을 봉인한 예행 저장소(`p12d/rh-none`), 시작 커밋 판 = 변형 `base`(`p12d/rh-base`).
모의본은 `mock.py`(sha256 앞 16 자리 위 `개선안 초안` 절)를 시작 커밋 판에 적용한 트리다. 측정 도우미는 이 절의 세 블록을 글자 그대로 뗀 것이다(`p12d/k/`).
새 시험 셋은 `/bin/bash` 3.2.57 로도 같은 끝 줄을 냈다(SC-01 · SC-05 · SC-06 둘째 줄).

| 조건 | 예행 판 (요구값) | 시작 커밋 판 | 양성 · 음성 대조 |
| --- | --- | --- | --- |
| SK-01 | `1` 다섯 · `1 1` · `1` 다섯 · `1` 셋 · `1 14` | `0` 다섯 · `0 0` · `0` 다섯 · `0` 셋 · `1 12` | 문장 삭제 15 개 모두 출력이 바뀜 |
| SK-02 | `1` 넷 · `1` 셋 · `1` 셋 · `1` 넷 | 전부 `0` | 문장 삭제 14 개 |
| SK-03 | `1 1 1` · `0` | `0 0 0` · `3` | 문장 삭제 3 개 · 둘째 값이 양성 대조(시작 판 3) |
| SK-04 | `1` 넷 · `1` · `1 0` | `0` 넷 · `0` · `0 1` | 문장 삭제 8 개 · 마지막 값이 양성 대조 |
| SK-05 | `1` 열 · `1 1 1 1 0` · `1` 넷 · `1` 일곱 · `row=1` · `1` 넷 | `0` 열 · `0 0 0 0 1` · `0` 넷 · `0` 일곱 · `row=0` · `0` 넷 | 문장 삭제 29 개 |
| SC-01 | `결과: 24 경우 중 불일치 0 rc=0` 두 줄 · `1` 다섯 · `ro=1 fullauto=0` · `결과: 24 경우 중 불일치 18 rc=1` | 시험 파일 없음 `rc=127` · `0` 다섯 · `ro=0 fullauto=1` | 마지막 줄이 음성 대조(편집 전 훅) · `-s read-only` 를 `--full-auto` 로 되돌린 사본 → 불일치 8 · 셋째 줄 `0 0 0 0 0` · 넷째 줄 `ro=0 fullauto=1` · `-s read-only` 를 두고 `--full-auto` 를 더한 사본 → 불일치 7 · 셋째 줄 `1 0 0 0 0` · 넷째 줄 `ro=1 fullauto=1` |
| SC-02 | `1` 일곱 · `1 1 0 0` | `0` 일곱 · `0 0 1 1` | 자르고 가리는 사본 → 시험 `불일치 키 조각 없음` 하나 · 첫 줄 `1 1 1 0 1 1 1` · 첫 줄만 고르는 사본 → 시험 `불일치 codex 실패 err= ERROR 줄` 하나 · 첫 줄 `0 1 1 1 1 1 1` (두 사본 모두 둘째 줄 `1 1 0 0`) |
| SC-03 | `1 1 1 1` · `1 0` | `0 0 0 0` · `0 1` | 모델을 `haiku-4.5` 로 되돌린 사본 → 불일치 7 · `0 1 0 1` · `0 1` |
| SC-04 | `1` 일곱 · `log-reflection.sh:1:ok log-prompt.sh:1:ok log-tool-failure.sh:1:ok` | `0` 일곱 · 셋 다 `:0:no` | `log-prompt.sh` 표식 검사를 뺀 사본 → 시험 `불일치 표식 — log-prompt.sh 안 적음` 하나 · `1 1 1 0 1 1 1` · 둘째 줄에 `log-prompt.sh:0:no` · `trap` 을 뺀 사본 → 시험 `불일치 TMPDIR 비었음`(남은 것 23) · `1 1 1 1 1 1 0` · 둘째 줄 그대로 |
| SC-05 | `결과: 16 경우 중 불일치 0 rc=0` 두 줄 · `결과: 16 경우 중 불일치 12 rc=1` · `0 1` | 시험 파일 없음 · `1 0` | `--show-toplevel` 만 쓰는 사본 → 불일치 5(워크트리 넷 · zsh 하나) · 공통 폴더 부모를 조건 없이 쓰는 사본 → 불일치 4(서브모듈 → `.git/modules` · 다른 곳에 둔 git 폴더 → `gitdirs` · bare 워크트리 → `repos` · 서브모듈 이름 `modules`) |
| SC-06 | `결과: 10 경우 중 불일치 0 rc=0` 두 줄 · `1` 여섯 · `1 1` | 시험 파일 없음 · `0` 여섯 · `0 0` | 둘을 더하는 사본 → 불일치 2(실패 9 · 11) · `0 0 1 1 1 1` · 기간으로 안 거르는 사본 → 불일치 1(7 일 값이 all 값) · `0 1 1 1 1 1` · 시험 답 `5회` → `9회` 사본 → `0 1 1 1 1 1` · `0 1` · 편집 전 판 라이브러리 → 불일치 10 |
| SC-07 | `1 1 1 1` · `1 1 1` | `0 0 0 0` · `0 0 0` | 기록된 세션도 내는 사본 → 불일치 3 · `0 0 0 1` · 프로젝트로 안 거르는 사본 → 불일치 2 · `0 1 0 1` · 시험 답 `없음 2개` → `없음 3개` 사본 → `0 1 1 1` · `0 1 1` · 시험 파일에서 `S-wt` 세션 줄을 지운 사본 → 불일치 1 · `0 1 1 1` · `1 1 0` · `S-miss` 세션 줄을 지운 사본 → 불일치 1 · `1 0 1` |
| SC-08 | `E rc=0 args=10 first=` · `B rc=2 args=9 first=error: unexpected argument '--full-auto' found` · 기록용 `codex=codex-cli 0.154.0` | `E` 줄도 `rc=2 args=9` | 둘째 줄이 양성 대조 |
| ER-01 | `0` · `0` | — | 스킬 끝 `https://example.invalid/x` → `1 0` · notes 끝 같은 URL → `0 1` · notes 없음 → `0 NOTES_MISSING` |
| ER-02 | `added=626 k02=0 names=0` | — | SCHEMA 끝 「이 값에 대해 적는다. fit-pal 화면」 → `k02=1 names=1` |
| ER-03 | `notes_committed=1` · `1` 스물넷 · `1 1 1` · `0` | — | 변형 `unsigned-shared` · `unsigned-hooksjson` · `signed-outside` · `cross-phase` → 넷째 값 `1`(`unsigned-mine` 은 `reflect-kit/README.md` 가 열두 파일이라 `0` — AR-01 이 잡는다) · `save-feedback.sh` 줄의 「다음 사이클 Phase 4」 를 뺀 사본 → `0 1 1` · `## 킷 로그 한 단락` 줄을 뺀 사본 → 스물셋째 값 `0` |
| AR-01 | `0` · `0 12` · `0` · `SEAL_OK` · `scope_same=1` · `1` | — | `unsigned-mine` · `unsigned-hooksjson` → 첫 값 `1` · `signed-outside` → `1 12` · `cross-phase` → `2 12` · 조건 줄 한 글자 변조 → `SEAL_BROKEN` |
| AR-02 | `tags_same=1 n=15` · `status_tpl=1 facets_tpl=1 warn=1` · `1 1 1 1 1` · `worktree_sect=1 hooks_same=1` · `100755 100755 100755` | `tags_same=1 n=10` · `status_tpl=0 facets_tpl=0 warn=0` · `0 1 1 0 0` · `worktree_sect=0 hooks_same=1` · 빈 줄 | DESIGN 태그 하나 뺀 사본 → `tags_same=0` · 라이브러리 틀 한 낱말 바꾼 사본 → `status_tpl=0` |
| AP-01 | `version=0.7.1 0` | — | SCHEMA 끝 「버전 0.7.1」 → `1` |
| AP-03 | `0` | — | SCHEMA 끝 펜스 한 쌍 → `2` |
| AP-04 | `1/1 1/1` | `1/1 1/1` | digest `name:` → `nam:` → `0/0` |
| RE-01 | 시험 셋 세 줄 | — | `reflect-kit/hooks/_lib-x.sh` 를 더한 사본 → 네 줄 |
| RE-02 | `1 0` · `1 1 1` | `0 0` · `0 1 0` | 훅 끝에 `[REDACTED-X]` 줄 · 라이브러리 끝에 `--show-toplevel` 줄 → `1 1` · `1 2 1` |
| DG-01 · DG-03 · DG-04 | `0` · `0` · `0` | — | DG-01 거르개에 `scripts/release.sh` · `.bak` → `1` · DG-04 거르개에 `reflect-kit/scripts/a.sh` · `b.md` → `1` |
| DG-02 | 다섯 줄 `new_warnings=0` · `shellcheck=0 bash_n=0` | 새 시험이 없어 `shellcheck=3 bash_n=3` | SCHEMA 끝 `#heading` → SCHEMA 줄 `new_warnings=1` · 시험 끝 `echo $undefined_var_x` → `shellcheck=9` |
| DG-05 | `10 0 v6=1 rc=0` · `tf_mine=0` · `sync_docs_rc=0 1` · `run_evals_rc=0` | 같다 | digest 끝 맨 펜스 한 쌍 → `10 1 v6=0 rc=2` · DESIGN Hybrid 표 가운데 문장 한 줄 → `tf_mine=1` · reflect-kaizen description 한 문장 바꾼 사본 → `sync_docs_rc=1 0` |
| DG-06 | `scope-isolation: PASS` · `doc-contracts: PASS` · `violators=0 mine=0` | — | 변형 `cross-phase` → `scope-isolation: FAIL` · `violators=1 mine=1` |

문장 삭제 사본(`p12d/del.sh` · 목록 `p12d/dellist.txt`, 목록 줄은 `조건|파일|몇 번째|토큰`): SK-01 15 · SK-02 14 · SK-03 3 · SK-04 8 · SK-05 29 — 토큰 하나를 그 파일에서 정해진 번째로
한 번 지운 사본 69 개 모두 그 조건의 `m` 출력이 바뀌었다(`DROP` 69 · `NODROP` 0 · `MISSING` 0). 한 파일에 두 번 나오는 토큰 셋(수집 상태 틀 · 멈춤 줄 · 대조 절 제목)은 재는 절의 자리를 지웠다.
양성 · 음성 대조 스크립트는 `p12d/ctl.sh`(출력 `p12d/ctl-out.txt`)다. 예행 변형의 커밋 기록 대조는 `p12d/rh-<변형>` 에서 `m ER-03` · `m AR-01` · `m DG-06` 을 돌렸다.
검토 1 회차(`.harness/.meta/kaizen-0924/phase12-review.md`) 반영: 옛 대조는 시험 출력이나 `m … | tail -1` 만 읽어서, 망가뜨린 사본에서 `m` 첫 줄이 요구값 그대로인 것을
못 봤다. SC-01 ~ SC-07 대조는 `p12d/ctl2.sh`(출력 `p12d/ctl2-out.txt`)로 사본마다 `m <조건 ID>` 전체 출력을 다시 읽었다 — 위 표의 SC-01 ~ SC-08 칸이 그 값이다.

**BUILD 재측정 (2026-09-25, 2 회차 검토 반영 뒤).** 시험 `log-reflection-test.sh` 를 2 회차 검토의 고친 사본(`p12r2/log-reflection-test.fixed.sh`)으로 바꿔 `mock.py` 를 다시 만들고
(`p12d/gen-mock.py`, 열두 항목 가운데 그 파일 하나만 달라졌다), 이 계약 초안으로 예행 저장소를 새로 만들어(`p12b/rh-none`) 스물아홉 조건을 계약에서 새로 뗀 도우미(`p12b/k/`)로 쟀다
(`p12b/run-all.sh`, 출력 `p12b/out-none.txt`). DRAFT 의 옛 예행 출력(`p12d/out-none2.txt`)과 다른 줄은 둘뿐이다 — SC-01 다섯째 줄 `불일치 17` → `불일치 18`, SC-07 둘째 줄 `1` → `1 1 1`.
ER-02 는 `added=626` 그대로다. 두 조건의 음성 대조는 `p12b/ctl.sh`(출력 `p12b/ctl-out.txt`)가 사본마다 `m` 전체 출력을 읽었다 — 위 표의 SC-01 · SC-07 칸이 그 값이다.
`common.sh` · `new-warnings.sh` 는 DRAFT 의 `p12d/k/` 와 글자 그대로 같고 `m.sh` 는 SC-07 갈래만 다르다.

**실제 도구 실측 (2026-09-25, 조건으로 잠그지 않는다 — 모델 호출 · 사용량이 걸린다).** 대체 경로는 플러그인 훅이 안 뜨게 `--setting-sources local` 과 환경 변수만 적는 시험 훅
(`--settings`)을 붙여 스크래치 폴더에서 돌렸다 — 로그 폴더 수는 전후 31 개 그대로였다.

- `claude -p --model haiku-4.5 --no-session-persistence` → 종료 코드 1, stdout `There's an issue with the selected model (haiku-4.5). It may not exist or you may not have access to it.`,
  stderr 첫 줄 `"haiku-4.5" isn't described by this version's model catalog; …` — 대체 경로가 한 번도 성공하지 못한 원인이다. 시험 훅은 `marker=[1]` 을 적었다 —
  `--no-session-persistence` 를 붙여도 프롬프트 제출 훅은 돌고, 부른 쪽의 `REFLECT_KIT_ANALYZER=1` 을 받는다
- `claude -p --model haiku --no-session-persistence` → 종료 코드 0, stdout `ok`, 시험 훅 `marker=[1]`
- 새 인자 묶음(`--ephemeral --skip-git-repo-check -s read-only --color never --cd "$HOME" --output-last-message <파일> -`)으로 codex 에 짧은 프롬프트 → 종료 코드 0, 마지막 메시지 `ok`.
  stderr 는 18 줄이고 첫 줄 `OpenAI Codex v0.154.0`, 이어 `sandbox: read-only` 와 받은 프롬프트 전문(`user` 아래)이 찍혔다 — `err=` 를 첫 줄로 고르면 안 되는 근거다
- 옛 인자 묶음(`--full-auto`)은 `--help` 를 붙여도 종료 코드 2 · `error: unexpected argument '--full-auto' found` (SC-08 둘째 줄과 같다)

**실제 로그에 새 함수를 돌린 값 (2026-09-25 09:08, 읽기만 · notes 에 옮긴다).** 로그 폴더 31 개 전부에 `collect_status 30` →
`수집 상태: Stop 실패 시도 2235회 (codex 실패 2235 · 대체 경로 실패 2235 · 대체 경로 성공 0 · 분석 전 중단 0; 고유 세션 151) / 기록된 세션 17 / 엔트리 117 / 마지막 기록 2026-08-28T17:28:39+0900`.
`claude-plugins` 폴더 하나에 `collect_status 30` → 실패 시도 442 · 고유 세션 25 · 기록 0 · 엔트리 0 과 `⚠ 수집 멈춤` 줄. `facets_unmatched all all` → `facets 18개 · 마찰 있는 세션 16개 ·
그중 reflections 없음 16개 (facets 읽기 실패 0 · session-meta 읽기 실패 0)`, `facets_unmatched all claude-plugins` → 6 · 5 · 5 (워크트리 경로 `bambu-orca-h2s-feedback` 세션 하나가 본 레포로 묶였다).
원시 로그의 분석용 프롬프트는 3,045 건, `fallback:claude-exit-1` 은 3,042 건, `fallback:claude-used` 는 0 건 — 설치본이 바뀌기 전까지 세 값은 계속 는다.

## Skill

- [ ] SK-01: `reflect-kit/skills/reflect-digest/SKILL.md` 가 수집 상태를 요약 머리에 올리게 한다 — 한 줄 Gotcha 13 이 다섯(제목 · 2026-09-14~23 실측 「Stop 실패 시도 849 번(고유 세션 55), 기록된 세션 0, 마지막 기록 2026-08-28」 · 요약 머리 첫 줄이 `collect_status` 출력 · 멈춤이면 `## 승격 후보` 에 한 줄만 · `## 환경 액션 아이템` 에 수집 복구와 가장 최근 `err=`)을 담고, Process `4. **엔트리 파싱**` 단계에 둘(파싱 전에 수집 상태부터 잰다 · `bash -c` 로 감싼 `collect_status` 한 줄 명령), `## 출력 포맷` 에 다섯(멈춤 줄을 싣는 조건 문장 · 수집 상태 틀 줄 `$STATUS_TPL` · 멈춤 줄 `$WARN` · 훅 실패 요약의 `err=` 두 줄), `### 4. Given-When-Then 동작 계약` 에 셋(들여쓴 틀 줄 · 들여쓴 멈춤 줄 · 싣는 규칙), `## Gotchas` 번호가 1 부터 14 까지 빠짐없이 이어진다 (`reflect-collector:P4`) — `m SK-01` 다섯 줄이 `1` 다섯 · `1 1` · `1` 다섯 · `1` 셋 · `1 14` [exact, enumerated]
- [ ] SK-02: `reflect-kit/skills/reflect-digest/SKILL.md` 가 facets 를 대조에만 쓰게 한다 — 한 줄 Gotcha 14 가 넷(제목 · 빈도 · 4 축 · precedence 에 더하면 두 번 센다 · 쓰는 곳은 `## 인사이트 세션 분석과 대조` 절 하나 · 폴더가 없으면 `facets 대조: (없음)`)을, `## 데이터 소스` 가 셋(facets · session-meta 줄 · 대조 전용 · `project_path` 로 잇는다)을, Process `9. **리포트 출력**` 단계가 셋(대조 절에 그대로 옮긴다 · `bash -c` 로 감싼 `facets_unmatched` 한 줄 명령 · 7 · 8 단계에 더하지 않는다)을, `## 출력 포맷` 이 넷(절 제목 `## 인사이트 세션 분석과 대조 (합산 금지)` · 옮기는 규칙 문장 · 머리 틀 줄 `$FACETS_TPL` · 세션 줄 틀)을 담는다 (`reflect-collector:P4`) — `m SK-02` 네 줄이 `1` 넷 · `1` 셋 · `1` 셋 · `1` 넷 [exact, enumerated]
- [ ] SK-03: `reflect-kit/skills/reflect-digest/SKILL.md` `## 프로젝트 ID` 가 본 레포 이름 규칙을 적고(기본 줄에 「워크트리 안에서 불러도 … 본 레포 이름이다」 · 워크트리 이름 폴더를 옮기지 않는다는 줄 · `project_root` 헬퍼 줄), `reflect-kit/` 전체에서 옛 표기 `basename(git-root)` 가 든 줄이 0 이다 (`reflect-collector:P5` · 근거 §3 digest `:110`) — `m SK-03` 두 줄이 `1 1 1` · `0` [exact, enumerated]
- [ ] SK-04: `reflect-kit/skills/reflect-kaizen/SKILL.md` 가 수집 상태를 게이트에 넣는다 — `### 0. 파편화 지표 선행 확인` 에 넷(수집 상태도 본다 · 멈춤이면 `calibration_confidence: low` 이고 파편화 임계 초과와 같은 효력 · 수집이 멈춘 기간의 `post_freq == 0` 은 못 셌다는 뜻 · `bash -c` 로 감싼 `collect_status` 30 일 한 줄 명령), `### (0) 파편화 지표` 에 `collect_status` 출력 원문 줄 하나, `### (1) LLM-as-judge 일치도` 의 모델이 `haiku` 이고 옛 `모델: haiku-4.5` 가 0 이다 (`reflect-collector:P4` 의 형제 자리 · 근거 §3 모델 이름) — `m SK-04` 세 줄이 `1` 넷 · `1` · `1 0` [exact, enumerated]
- [ ] SK-05: 문서 셋이 구현과 같은 말을 한다 — `reflect-kit/docs/SCHEMA.md` `## 3. 훅 에러 로그` 에 열(`err=` 가 붙은 codex 줄 · 새 태그 다섯 · `err=` 규칙 문장 넷), `## 5. Project ID 포맷` 에 넷(본 레포 root 기본 · 링크된 워크트리 조건 · 마커와 hash 입력 · DESIGN `### 워크트리` 절을 가리킴)과 옛 줄 「basename만 같고 다른 repo라도 hash가 달라 충돌하지 않는다」 0, `reflect-kit/docs/DESIGN.md` `## 에러 관측성` 에 넷, `### 워크트리 (2026-09-25)` 에 일곱(31 개 중 12 개 실측 · 링크된 워크트리 조건 · 서브모듈 · `--separate-git-dir` · bare 레포 · 옮기지 않는다 · 12 개 폴더에 reflections 0), Hybrid 표 행 「같은 레포의 링크된 워크트리에서 호출」 1, `reflect-kit/README.md` 에 넷(폴더 이름 줄 · 새 함수 두 이름 · codex `-s read-only` · `claude` CLI 의존) (`reflect-collector:P3` · `reflect-collector:P5` · 근거 §3 SCHEMA §5) — `m SK-05` 여섯 줄이 `1` 열 · `1 1 1 1 0` · `1` 넷 · `1` 일곱 · `row=1` · `1` 넷 [exact, enumerated]

## Script

- [ ] SC-01: Stop 훅이 codex 를 읽기 전용 인자로 부른다 — `$END` 판 사본에서 새 시험 `reflect-kit/evals/hooks/log-reflection-test.sh` 를 bash 5 와 `/bin/bash` 3.2(PATH 도 `/usr/bin:/bin:/usr/sbin:/sbin`)로 돌리면 둘 다 끝 줄 `결과: 24 경우 중 불일치 0` 에 종료 코드 0, 그 출력 가운데 `grep '^일치 '` 가 남긴 줄에 codex 경우 다섯 줄(`-s read-only` · `--full-auto` 없음 · codex 성공 시 대체 경로 안 부름 · codex 가 낸 기록이 남음 · 실패 줄 없음)이 각각 1, `reflect-kit/hooks/log-reflection.sh` 의 codex 인자 줄에 `-s read-only` 1 · `--full-auto` 0 이다. 음성 대조: 같은 시험에 편집 전 판 훅 폴더를 넣으면(`REFLECT_KIT_HOOKS`) 끝 줄 `결과: 24 경우 중 불일치 18` 에 종료 코드 1, `-s read-only` 를 두고 `--full-auto` 를 더한 사본은 `m SC-01` 셋째 줄이 `1 0 0 0 0` · 넷째 줄이 `ro=1 fullauto=1` 이다 (`reflect-collector:P3`) — `m SC-01` 다섯 줄이 `결과: 24 경우 중 불일치 0 rc=0` 두 줄 · `1` 다섯 · `ro=1 fullauto=0` · `결과: 24 경우 중 불일치 18 rc=1` [exact, enumerated]
- [ ] SC-02: 분석기가 실패하면 원인 한 줄이 `.errors.log` 에 남고 transcript · 키는 안 남는다 — 같은 시험 출력 가운데 `grep '^일치 '` 가 남긴 줄에 `err=` 경우 일곱 줄(한도 초과면 `ERROR` 줄 · error 줄이 없으면 비어 있지 않은 첫 줄 · transcript 표식이 `.errors.log` 에 0 · 키 조각 0 · `err=` 값 200 자 이하 · 대체 경로 stderr 가 비면 stdout 에서 · codex 빈 응답은 `err=` 없이)이 각각 1, 훅에 codex stderr 를 파일로 받는 줄 1 · claude stdout · stderr 를 파일로 받는 줄 1, 옛 줄 `  - >/dev/null 2>&1` 0 · `claude -p --model haiku-4.5 > "$fb_tmp" 2>/dev/null` 0 이다. 음성 대조: 가리기 전에 200 자로 자르는 사본은 `m SC-02` 첫 줄이 `1 1 1 0 1 1 1`, 비어 있지 않은 첫 줄만 고르는 사본은 `0 1 1 1 1 1 1` 이다(`회귀 게이트` 절) (`reflect-collector:P3`) — `m SC-02` 두 줄이 `1` 일곱 · `1 1 0 0` [exact, enumerated]
- [ ] SC-03: 대체 경로가 있는 모델 이름으로 기록을 남기지 않는 세션을 띄운다 — 같은 시험 출력 가운데 `grep '^일치 '` 가 남긴 줄에 대체 경로 경우 넷(`--model haiku` · `--no-session-persistence` · 대체 경로가 성공하면 기록이 남음 · 실패하면 기록 없음)이 각각 1, 훅에 호출 줄 `echo "$prompt" | REFLECT_KIT_ANALYZER=1 claude -p --model haiku --no-session-persistence \` 1, 주석이 아닌 줄의 `haiku-4.5` 0 이다. 음성 대조: 모델 이름을 `haiku-4.5` 로 되돌린 사본은 `0 1 0 1` · `0 1` (`reflect-collector:P3` · 근거 §3 모델 이름) — `m SC-03` 두 줄이 `1 1 1 1` · `1 0` [exact, enumerated]
- [ ] SC-04: 분석기 세션에서 돈 reflect-kit 훅은 아무것도 적지 않고 분석 임시 파일은 남지 않는다 — 같은 시험 출력 가운데 `grep '^일치 '` 가 남긴 줄에 경우 일곱 줄(codex · claude 가 표식 `REFLECT_KIT_ANALYZER=1` 을 받음 · 표식이 있으면 Stop 분석 · `log-prompt.sh` · `log-tool-failure.sh` 가 아무것도 안 적음 · 표식이 없으면 `log-prompt.sh` 가 적음(양성 대조) · 끝나면 `TMPDIR` 가 빔)이 각각 1, 세 훅(`log-reflection.sh` · `log-prompt.sh` · `log-tool-failure.sh`) 모두 표식 검사 줄 `[ -n "${REFLECT_KIT_ANALYZER:-}" ] && exit 0` 이 1 개이고 첫 `source` · 입력 읽기보다 앞이다. 음성 대조: 분석 임시 폴더 `trap` 을 뺀 사본은 첫 줄 끝 값이 `0`, `log-prompt.sh` 표식 검사를 뺀 사본은 첫 줄 넷째 값이 `0` 이고 둘째 줄에 `log-prompt.sh:0:no` (P3 에서 찾은 원시 로그 오염 3,044 건) — `m SC-04` 두 줄이 `1` 일곱 · `log-reflection.sh:1:ok log-prompt.sh:1:ok log-tool-failure.sh:1:ok` [exact, enumerated]
- [ ] SC-05: 폴더 이름이 워크트리에서도 본 레포 이름이다 — `$END` 판 사본에서 새 시험 `reflect-kit/evals/hooks/project-id-test.sh`(본 레포 · 그 하위 · 링크된 워크트리 · 그 하위 · git 밖 · 서브모듈 · 다른 곳에 둔 git 폴더 · bare 레포의 워크트리 · 없는 경로 아홉의 `project_root`, 본 레포 · 워크트리 · 마커 · 같은 이름 다른 레포 · 그 워크트리 · 서브모듈 여섯의 폴더 이름, zsh 로 읽은 워크트리 폴더 이름)를 bash 5 와 `/bin/bash` 3.2 로 돌리면 둘 다 끝 줄 `결과: 16 경우 중 불일치 0` 에 종료 코드 0, 편집 전 판 라이브러리를 넣으면(`PROJECT_ID_LIB`) `결과: 16 경우 중 불일치 12` 에 종료 코드 1, `compute_project_id` 본문의 `show-toplevel` 0 · `repo_root=$(project_root "$cwd")` 1 이다. 음성 대조: `project_root` 가 `--show-toplevel` 만 쓰는 사본과 공통 폴더의 부모를 조건 없이 쓰는 사본이 각각 요구값에서 벗어난다(`회귀 게이트` 절) (`reflect-collector:P5`) — `m SC-05` 네 줄이 `결과: 16 경우 중 불일치 0 rc=0` 두 줄 · `결과: 16 경우 중 불일치 12 rc=1` · `0 1` [exact, enumerated]
- [ ] SC-06: `collect_status` 가 손으로 센 답을 낸다 — `$END` 판 사본에서 새 시험 `reflect-kit/evals/hooks/collect-status-test.sh` 를 bash 5 와 `/bin/bash` 3.2 로 돌리면 둘 다 끝 줄 `결과: 10 경우 중 불일치 0` 에 종료 코드 0, 출력 가운데 `grep '^일치 '` 가 남긴 줄에 여섯 줄(7 일 · 두 폴더 — `Stop 실패 시도 5회 (codex 실패 4 · 대체 경로 실패 3 · 대체 경로 성공 1 · 분석 전 중단 2; 고유 세션 4) / 기록된 세션 1 / 엔트리 1` · all · 두 폴더 — 실패 6 · 기록 2 · 엔트리 3 · 엔트리 0 이고 실패 1 이상이면 멈춤 줄 · 빈 폴더는 멈춤 줄 없음 · 일수가 틀리면 종료 코드 2 · zsh 로 부르면 종료 코드 2)이 각각 1 이고, 시험 파일의 `check "7 일 · 두 폴더"` 줄과 `check "all · 두 폴더"` 줄에 손으로 센 답(`Stop 실패 시도 5회 (codex 실패 4 · 대체 경로 실패 3 · 대체 경로 성공 1 · 분석 전 중단 2; 고유 세션 4) / 기록된 세션 1 / 엔트리 1` · `Stop 실패 시도 6회 (codex 실패 5 · 대체 경로 실패 4 · 대체 경로 성공 1 · 분석 전 중단 2; 고유 세션 5) / 기록된 세션 2 / 엔트리 3`)이 글자 그대로 한 줄씩 있다. 음성 대조: codex 실패와 대체 경로 실패를 더하는 사본은 셋째 줄이 `0 0 1 1 1 1`, 기간으로 거르지 않는 사본은 `0 1 1 1 1 1`, 시험 파일의 답 `5회` 를 `9회` 로 바꾼 사본은 넷째 줄이 `0 1` 이다(`회귀 게이트` 절) (`reflect-collector:P4`) — `m SC-06` 네 줄이 `결과: 10 경우 중 불일치 0 rc=0` 두 줄 · `1` 여섯 · `1 1` [exact, enumerated]
- [ ] SC-07: `facets_unmatched` 가 마찰이 적혔는데 reflections 에 없는 세션만 원문과 함께 내고 읽지 못한 파일을 두 갈래로 센다 — 같은 시험 출력 가운데 `grep '^일치 '` 가 남긴 줄에 넷(7 일 · alpha — `facets 4개 · 마찰 있는 세션 3개 · 그중 reflections 없음 2개 (facets 읽기 실패 1 · session-meta 읽기 실패 1)` 과 세션 줄 둘, 워크트리에서 연 세션을 본 레포로 묶음 · 7 일 · all · all · alpha · facets 폴더 없음 — `facets 대조: (없음)` 과 종료 코드 0)이 각각 1 이고, 시험 파일의 `check "facets 7 일 · alpha"` 줄에 손으로 센 답 `facets 대조: facets 4개 · 마찰 있는 세션 3개 · 그중 reflections 없음 2개 (facets 읽기 실패 1 · session-meta 읽기 실패 1)` 이 글자 그대로 한 줄 있고, 그 답에 이어지는 세션 줄 둘(`S-miss` 의 `— missed friction` 줄 · 워크트리 `alpha-wt` 에서 연 `S-wt` 의 `— worktree friction` 줄)도 시험 파일에 글자 그대로 한 줄씩 있다. 음성 대조: reflections 에 있는 세션도 내는 사본은 `m SC-07` 첫 줄이 `0 0 0 1`, 프로젝트로 거르지 않는 사본은 `0 1 0 1`, 시험 파일의 답 `없음 2개` 를 `없음 3개` 로 바꾼 사본은 둘째 줄이 `0 1 1`, 시험 파일에서 `S-wt` 세션 줄을 지운 사본은 둘째 줄이 `1 1 0` 이다(`회귀 게이트` 절) (`reflect-collector:P4`) — `m SC-07` 두 줄이 `1 1 1 1` · `1 1 1` [exact, enumerated]
- [ ] SC-08: 이 기계의 codex CLI 가 훅이 넘기는 인자 묶음을 받는다 — `$END` 판 `reflect-kit/hooks/log-reflection.sh` 의 codex 인자 줄을 그대로 떼어 `codex exec <인자> - --help` 로 넘기면 종료 코드 0 에 stderr 첫 줄이 비고, 편집 전 판 훅의 인자 묶음은 종료 코드 2 에 `error: unexpected argument '--full-auto' found` 다 (`reflect-collector:P3` — 수집이 멈춘 직접 원인) — `m SC-08` 세 줄 가운데 앞 두 줄이 `E rc=0 args=10 first=` · `B rc=2 args=9 first=error: unexpected argument '--full-auto' found` 다. 셋째 줄 `codex=<판>` 은 판정에 쓰지 않는다 — 둘째 줄이 바뀌었을 때 codex 가 올라간 탓인지 가르는 기록이다(봉인 전 값 `codex=codex-cli 0.154.0`) [exact]

## Error

- [ ] ER-01: 열두 파일에 새로 생긴 URL 과 `.harness/.meta/kaizen-0924/phase12-notes.md` 의 URL 이 전부 이 Phase 의 외부 근거 파일 `.harness/.meta/evidence/phase12.md` 에 있다 — 열두 파일은 파일마다 편집 전 판과 비교한다 (러닝북 — 근거 파일에 없는 URL 을 지어내지 마라 · notes 킷 로그의 출처 URL 은 근거 파일에서만) — `m ER-01` 두 줄이 `0` · `0` [exact, enumerated]
- [ ] ER-02: 열두 파일에 더한 줄에 번역투 6 종(`tone-kit/references/locale-korean.md` §2 치환표의 grep 열)과 특정 앱 · 화면 조종 도구 이름(`fit-pal` · `fitpal` · `fit_pal` · `flutter-playwright` · `playwright-mcp` · `chrome-devtools-mcp` 모양)이 0 건이다 (러닝북 말투 규칙) — `m ER-02` 가 `added=N k02=0 names=0` 이고 N 은 1 이상 [exact]
- [ ] ER-03: 이 Phase 범위 밖과 미반영 몫을 명시적 미완으로 넘기고 공유 파일 · 다른 Phase 파일 · 이 킷의 나머지를 건드리지 않는다 — `.harness/.meta/kaizen-0924/phase12-notes.md` 가 `$END` 에 커밋돼 있고, 문자열 스물넷(처리 배정표 키 `reflect-collector:P3` · `reflect-collector:P4` · `reflect-collector:P5`, 넘김 `harness/scripts/save-feedback.sh` · `harness/agents/qa-evaluator.md` · `qa-evaluation-guide.md` · `hooks.json` · `asyncRewake` · `last_assistant_message` · `plugin.json` · `` 버전: `0.3.0` `` · `docs/reflect-kit/`, reflect-kaizen 실측 `singleton_share 0.887` · `promotions-ledger`, `ci.yml` 에 넣을 줄 셋 `bash reflect-kit/evals/hooks/log-reflection-test.sh` · `bash reflect-kit/evals/hooks/project-id-test.sh` · `bash reflect-kit/evals/hooks/collect-status-test.sh`, 러닝북 절 제목 일곱 `## 바꾼 파일` · `## 반영한 처리 배정표 키` · `## 미반영 키와 사유` · `## 넘기는 것` · `## changelog 한 단락` · `## 킷 로그 한 단락` · `## 다음 사이클 메모`)이 각각 1 줄 이상이고, 넘김 셋은 받을 Phase 와 같은 줄에 있으며(`save-feedback.sh` 줄에 「다음 사이클 Phase 4」 · `qa-evaluator.md` 줄에 「다음 사이클 Phase 3」 · `hooks.json` 줄에 「다음 사이클 Phase 4」 — 각각 1 줄 이상), 공유 파일 · `harness/` · `scripts/` · `docs/` · `.claude/skills/` · `reflect-kit/hooks/hooks.json` · `reflect-kit/references/` · `reflect-kit/scripts/` · reflect-promote · codex-kaizen 을 건드린 구간 안 커밋 가운데 다른 Phase 서명이 없는 것이 0 이다 (`reflect-collector:P5` 의 하네스 쪽 · Counterpart 미완) — `m ER-03` 네 줄이 `notes_committed=1` · 스물넷 값 전부 1 이상 · 세 값 전부 1 이상 · `0` [exact, enumerated]

## Architecture

- [ ] AR-01: 이 Phase 의 변경이 허용 경로 안에 머물고, 범위 선언 블록이 그 경로와 같으며, 이 계약이 봉인돼 있다 — `reflect-kit/` 를 건드린 구간 안 커밋이 전부 서명했고, 서명 커밋이 고친 `.harness/` 밖 경로가 열두 파일뿐이며(열둘 전부 포함), 서명 커밋이 건드린 계약 가운데 봉인이 깨진 것이 0, 이 계약이 `SEAL_OK`, `## 범위 경계` 의 `# sprint-scope` 블록이 열두 경로와 `.harness/` 한 줄이다. 양성 대조: 예행 변형 `unsigned-mine` → 첫 값 `1` · `signed-outside` · `cross-phase` → 둘째 줄 첫 값 `1` 이상 · 조건 줄 한 글자 변조 → `SEAL_BROKEN` — `m AR-01` 여섯 줄이 `0` · `0 12` · `0` · `SEAL_OK` · `scope_same=1` · `1` [exact, enumerated]
- [ ] AR-02: 코드와 문서가 같은 것을 말한다 — `reflect-kit/docs/SCHEMA.md` `### 사유 태그` 와 `reflect-kit/docs/DESIGN.md` `## 에러 관측성` 의 태그 목록이 같고(열다섯), `reflect-kit/hooks/_lib-project-id.sh` 의 출력 틀(수집 상태 · facets 머리)을 자리표시자로 바꾸면 digest 의 틀 줄 `$STATUS_TPL` · `$FACETS_TPL` 과 글자 그대로 같고 멈춤 줄 `$WARN` 이 라이브러리에 1, 문서가 부르는 함수 다섯(`project_root` · `compute_project_id` · `normalize_project_query` · `collect_status` · `facets_unmatched`)이 라이브러리에 한 번씩 정의돼 있고, SCHEMA 가 가리키는 DESIGN `### 워크트리 (2026-09-25)` 절이 있고, `reflect-kit/hooks/hooks.json` 은 편집 전과 같으며, 새 시험 셋의 git 모드가 `100755` 다 — `m AR-02` 다섯 줄이 `tags_same=1 n=15` · `status_tpl=1 facets_tpl=1 warn=1` · `1 1 1 1 1` · `worktree_sect=1 hooks_same=1` · `100755 100755 100755` [exact, enumerated]

## Anti-patterns

- [ ] AP-01: 버전을 하드코딩하지 않는다 — plugin.json에서 읽어야 한다. 이번 변경에 적용: 열두 파일에 더한 줄에 reflect-kit `plugin.json` 의 `version` 값(`$END` 판에서 읽는다)이 0 건이다 — 이 Phase 는 킷 버전을 적지 않고 Final 이 올린다. 외부 도구 버전(codex-cli 0.154.0)은 실측 날짜를 단 사실 문장이라 이 패턴의 대상이 아니다 — `m AP-01` 이 `version=0.7.1 0` [exact]
- [ ] AP-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수 (```` ```text, ```bash, ```yaml ```` 등). 판정 권위는 validate-plugin V6 상태기계다 — 여는/닫는 fence 가 동형이라 줄 단위 정규식으로는 판정 불가. 이번 변경에 적용: SKILL.md 둘과 README 는 DG-05 의 V6 가 `0 bare` 로 재고, V6 가 읽지 않는 `reflect-kit/docs/` 두 파일에 더한 줄에는 펜스가 0 이다 — `m AP-03` 이 `0` [exact]
- [ ] AP-04: SKILL.md / agents/*.md frontmatter 에서 name 필드 누락 — validate-plugin V1 FAIL. 이번 변경에 적용: 고친 SKILL.md 둘(`reflect-digest` · `reflect-kaizen`)의 첫 frontmatter 블록이 편집 전과 글자 그대로 같고 `name: <폴더 이름>` 줄이 1 개씩이다 — 그래서 README AUTO 구간과 트리거 설명이 읽는 값이 안 바뀐다 — `m AP-04` 가 `1/1 1/1` [exact]

## Reusability

- [ ] RE-01: 다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다. 이번 변경에 적용: 새 함수 셋(`project_root` · `collect_status` · `facets_unmatched`)은 세 훅과 두 스킬이 이미 읽는 공용 라이브러리 `reflect-kit/hooks/_lib-project-id.sh` 에 두고 새 라이브러리 파일을 만들지 않는다 — `m RE-01` 이 새 파일로 `reflect-kit/evals/hooks/collect-status-test.sh` · `reflect-kit/evals/hooks/log-reflection-test.sh` · `reflect-kit/evals/hooks/project-id-test.sh` 세 줄만 낸다 [exact, enumerated]
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다. 이번 변경에 적용: (a) `err=` 한 줄은 기존 `redact_sensitive` 로 가리고 `reflect-kit/hooks/log-reflection.sh` 에 더한 줄에 새 가림 패턴(`REDACTED`)이 0 (b) 본 레포 root 계산은 `project_root` 한 곳 — 라이브러리 전체의 `show-toplevel` 이 1 이고 그것이 `project_root` 안에 있으며 `facets_unmatched` 가 `project_root "$pp"` 를 부른다 — `m RE-02` 두 줄이 `1 0` · `1 1 1` [exact]

## Diagnostics

- [ ] DG-01: N/A (`commands.analyze` 는 `bash -n scripts/release.sh` 라 `scripts/release.sh` 만 잰다 — 이번 변경 파일과 교집합 0 개. 측정: `type m >/dev/null || exit 2;` 뒤 `m DG-01` 이 0. 양성 대조: 같은 `grep -c '^scripts/release.sh$'` 에 `scripts/release.sh` · `scripts/release.sh.bak` 두 줄을 넣으면 1. 이번 변경의 셸 파일 일곱은 DG-02 의 shellcheck · `bash -n` 과 SC-01 ~ SC-07 의 시험이 잰다)
- [ ] DG-02: IDE diagnostics 워닝/인포 0개 (`diagnostics.ide_exclude` 값 `[]`) — 이번 변경에 적용: 편집기 마크다운 확장과 같은 조건(markdownlint-cli2 0.23.2 · MD013 끔)으로 마크다운 다섯 파일의 **더한 줄**에 걸린 경고가 0 이고 린터가 다섯 번 다 돌았으며, 셸 파일 일곱(훅 넷 · 새 시험 셋)의 shellcheck 출력이 0 줄이고 `bash -n` 이 전부 통과한다. 편집 전부터 있던 경고는 `범위 경계` 절에 적은 대로 범위 밖이다 — `m DG-02` 여섯 줄 가운데 앞 다섯 줄 끝이 `new_warnings=0` 이고 여섯째 줄이 `shellcheck=0 bash_n=0` [exact]
- [ ] DG-03: N/A (`commands.test` 는 `bash scripts/release.sh 2>&1 || true` 라 `scripts/release.sh` 만 잰다 — 교집합 0 개. 측정: DG-01 과 같은 명령 `m DG-03` 이 0. 실제 시험은 SC-01 ~ SC-07 · DG-05)
- [ ] DG-04: N/A (구동할 앱 · 서버가 없다 — 실행 파일은 훅 셋과 새 시험 셋이고 SC-01 ~ SC-07 이 실제로 돌린다. 측정: `m DG-04` 가 이번 커밋의 실행 파일 가운데 `reflect-kit/hooks/` · `reflect-kit/evals/hooks/` · `.harness/` 밖의 것을 세어 0. 양성 대조: 같은 거르개에 `reflect-kit/scripts/a.sh` · `b.md` 두 줄을 넣으면 1)
- [ ] DG-05: 저장소 검사가 이 킷을 문제로 가리키지 않는다 — `$END` 판을 git 저장소로 만든 사본에서 (a) `scripts/validate-plugin.py reflect-kit` 출력에 `V1` ~ `V10` 열 줄이 있고 V2(templates 없음 — SKIP) 밖의 아홉이 전부 `— OK` 로 끝나며 V6 가 `0 bare — OK`, 종료 코드 0 이다 (b) 전체 킷 `--check=table-integrity,code-fence` 의 `FAIL` 줄 가운데 이 Phase 파일을 가리키는 줄 0 (c) `scripts/sync-docs.py --check-only` 가 종료 코드 0 에 `  reflect-kit/README.md: 동기화됨` 1 줄 (d) `scripts/run-evals.py reflect-kit` 가 종료 코드 0 — `m DG-05` 네 줄이 `10 0 v6=1 rc=0` · `tf_mine=0` · `sync_docs_rc=0 1` · `run_evals_rc=0` [exact]
- [ ] DG-06: `python3 scripts/validate-post-kaizen.py --since 82b2493da582554a0ae4c1ee36db1bb3ba7c511b` 출력의 `scope-isolation` · `doc-contracts` 줄이 `FAIL` · `ERROR` 가 아니다. `docs-site-regen` 은 Final F2 몫이라 판정에서 뺀다. 다른 Phase 커밋 때문에 `scope-isolation` 이 FAIL 이면 `--verbose` 위반 커밋 목록을 한 개 이상 읽었고 그 안에 이 Phase 서명 커밋이 없을 때 이 조건은 PASS 다 — `m DG-06` 의 `scope-isolation` · `doc-contracts` 줄과 `violators=N mine=0` [goal]
