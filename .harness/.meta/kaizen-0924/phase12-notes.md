# 카이젠 2026-09-24 Phase 12 (reflect-kit) — notes

- 계약: `.harness/sprint-contract-kaizen-0924-p12-reflect-kit.md` (조건 29 · 기능 조건 20, 봉인 `sha256:71e1e96b9d125ed8` · `locked_at` 2026-09-25 10:01)
- 개정: `.harness/sprint-amendments-kaizen-0924-p12-reflect-kit.md` (조건 변경 0 건, `end_sha` 만)
- 검토: `.harness/.meta/kaizen-0924/phase12-review.md` (1 회차 CHANGES 필수 둘은 DRAFT 가, 2 회차 CHANGES 고칠 것 셋과 권하는 것 1 은 BUILD 가 봉인 전에 넣었다.
  3 회차 검토 없이 BUILD 가 바뀐 두 조건 SC-01 · SC-07 을 예행 판과 망가뜨린 사본 다섯에서 다시 쟀다 — 계약 `회귀 게이트` 절 `BUILD 재측정` 문단)
- 시작 커밋 `82b2493da582554a0ae4c1ee36db1bb3ba7c511b`
- 계약 피드백: `~/.harness/feedback/contract/5a24cc99-2026-09-25T100523-de8c7935-24528.yaml` (`verify-feedback.sh` PASS). 초안은 `.harness/feedback-draft-p12.yaml` 로 갈라 썼고
  `HARNESS_CONTRACT` · `HARNESS_SPRINT_SLUG` 를 명시해 저장했다

## 커밋

| 커밋 | 내용 | 파일 |
| --- | --- | --- |
| `3697018` | 봉인 커밋 | 계약 1 개 |
| `9c680cb` | Stop 훅 수집 복구 · 수집 상태 머리 · facets 대조 · 워크트리에서도 본 레포 이름 | `reflect-kit/` 열두 개 |
| `858787e` | 개정 파일에 `end_sha` (`9c680cb`) | 개정 1 개 |
| 이 파일의 커밋 | notes · 검토 기록 | `.harness/` 두 개 |
| 그다음 커밋 | 개정 파일에 notes 커밋 sha 로 `end_sha` 한 줄 더 | 개정 1 개 |

모든 커밋 메시지 끝 문단에 `Kaizen-Phase: kaizen-0924-p12-reflect-kit` 줄이 있다. 구현 커밋은 `git add -- <파일…> && git commit -o -- <파일…>` 로 내 경로만 실었다.
**FIX 가 커밋을 더할 때도 서명 줄을 넣고, 개정 파일에 `end_sha:` 줄을 덧붙인다.**

구현은 초안의 모의본(스크래치 `p12d/mock.py`, 지문 앞 16 자리 `75b19518ca3f7713` — 2 회차 검토의 고친 시험을 넣어 다시 만든 판)을 작업 폴더에 그대로 돌렸다.
돌리기 전에 `reflect-kit/` 가 시작 커밋과 `HEAD` 사이에 바뀌지 않았고 미커밋 변경도 없는 것을 봤다. 시작 커밋 판 새 사본에서 `mock applied 12` · 두 번째 실행 `MOCK_FAIL`
(종료 코드 3, 파일 변화 0)을 본 뒤 작업 폴더에서도 `mock applied 12` · 종료 코드 0 이 나왔고, 커밋한 열두 파일이 예행 저장소(`p12b/rh-none`)의 같은 경로와 blob 이 같다.
29 조건 측정은 봉인 판 계약에서 뗀 묶음으로 돌렸다 — 스크래치 `p12b/k/`(`common.sh` · `m.sh` · `new-warnings.sh`) · `p12b/run-all.sh <저장소>`(공통 정의를 `.` 로 읽고
`TMPDIR` 를 스크래치로 둔 뒤 `type m` 을 확인하고 `m <조건 ID>`). QA 가 같은 묶음을 다시 돌릴 수 있다.

## 바꾼 파일

- `reflect-kit/hooks/log-reflection.sh` — 분석기 표식 검사(첫머리), codex 인자 `--full-auto` → `-s read-only`, codex · 대체 경로 stderr 를 임시 폴더 파일로 받아 `err_line`
  (`error` · `ERROR` 로 시작하는 첫 줄, 없으면 비어 있지 않은 첫 줄 → `redact_sensitive` → 200 자)으로 `err=`, 대체 경로 `claude -p --model haiku --no-session-persistence`
  (stderr 가 비면 stdout 에서), 분석 임시 폴더 하나와 `trap`
- `reflect-kit/hooks/log-prompt.sh` · `log-tool-failure.sh` — 분석기 표식 검사 한 줄. `log-prompt.sh:4` 의 틀린 주석(「`<basename>-<6자 hash>`」)을 정본 가리킴으로
- `reflect-kit/hooks/_lib-project-id.sh` — `project_root`(링크된 워크트리면 본 레포), `compute_project_id` 가 그것을 쓴다. `collect_status` · `facets_unmatched` 와 기간 계산 `_rk_since`
- `reflect-kit/skills/reflect-digest/SKILL.md` — Gotcha 13(엔트리 0 을 문제 없음으로 읽지 않기) · 14(facets 는 대조에만), 프로젝트 ID 넷째 줄 · `project_root` 헬퍼,
  데이터 소스 facets 줄, Process 4 · 9 단계 한 줄 명령, project=all 머리 · 예시, 출력 틀 머리 두 줄 · `## 인사이트 세션 분석과 대조 (합산 금지)` 절 · 훅 실패 요약 두 줄
- `reflect-kit/skills/reflect-kaizen/SKILL.md` — §0 수집 상태 문단과 한 줄 명령, 출력 (0) 한 줄, (1) 모델 이름 `haiku-4.5` → `haiku`
- `reflect-kit/docs/SCHEMA.md` — §3 태그 다섯 · `err=` 문단, §5 다시 씀(v0.3.0 Hybrid · 본 레포 root)
- `reflect-kit/docs/DESIGN.md` — 에러 관측성 태그 다섯 · 두 문단, 결정 #3 Hybrid 표 한 행 · `### 워크트리 (2026-09-25)` 절
- `reflect-kit/README.md` — 폴더 이름 줄, 의존성 두 줄(codex `-s read-only` · `claude` CLI)
- 새 시험 셋(모드 755): `reflect-kit/evals/hooks/log-reflection-test.sh`(24 경우) · `project-id-test.sh`(16 경우) · `collect-status-test.sh`(10 경우)

스킬 머리 설정 둘은 그대로다(AP-04). `hooks.json` 도 그대로다(AR-02 `hooks_same=1`). reflect-kit README 의 AUTO 구간은 바뀌지 않았다 — `sync-docs.py --check-only` 는 「모든 README가 동기화 상태입니다」.

## 반영한 처리 배정표 키

| 키 | 반영 |
| --- | --- |
| `reflect-collector:P3` | Stop 훅 수집이 2026-08-28 18:01 부터 멈춘 원인(codex-cli 0.154.0 이 `--full-auto` 를 거부, 종료 코드 2)을 고쳤다. 두 분석기 stderr 한 줄을 `err=` 로 남기고, 대체 경로 모델을 CLI 가 아는 별칭 `haiku` 로, 분석기 표식으로 분석기 세션의 훅이 아무것도 적지 않게 했다 (SC-01 ~ SC-04 · SC-08) |
| `reflect-collector:P4` | reflect-digest 요약 머리 첫 줄을 `collect_status` 출력으로, `⚠ 수집 멈춤` 이면 승격 후보를 내지 않고 환경 액션 아이템에 수집 복구를 올린다. facets 는 대조 절 하나에만 쓴다. reflect-kaizen §0 이 같은 수집 상태를 게이트로 쓴다 (SK-01 · SK-02 · SK-04 · SC-06 · SC-07) |
| `reflect-collector:P5` | 폴더 이름을 워크트리 폴더가 아니라 본 레포 이름으로(`project_root`). 이미 워크트리 이름으로 생긴 12 개 폴더는 옮기지 않는다 — reflections 0 이고 원시 로그와 `.errors.log` 뿐이라 (SK-03 · SK-05 · SC-05) |
| 근거 §3 현행화 | SCHEMA §5 · digest 두 곳(`basename(git-root)` 0 건) · reflect-kaizen 모델 이름 |

## 미반영 키와 사유

- `harness:P02` 비고 · 러닝북 Phase 12 추가 과제 · Phase 4 넘김(`harness/scripts/save-feedback.sh` 의 같은 규칙) — 이 Phase 범위는 `reflect-kit/` 다. 아래 넘김 표
- 근거 §3 의 `hooks.json` 따옴표 없는 `${CLAUDE_PLUGIN_ROOT}` — 킷 넷의 `hooks.json` 이 모두 같은 모양이라 한 킷만 바꾸지 않는다. 아래 넘김 표
- 근거 §3 의 수동 `nohup` 대신 훅 설정 `async` · `asyncRewake` — 근거 파일이 「즉시 교체 필수는 아니다」 라고 적었다. 다음 사이클
- Stop 시점 transcript 에 마지막 응답이 없을 수 있다(근거 §5, 훅 입력의 `last_assistant_message`) — 이번에 다루지 않았다. 다음 사이클
- reflect-kaizen §1 · §2(다른 모델 재분류 일치도) — 돌리지 않았다. 마지막 기록이 2026-08-28 이라 30 일 창에 새 표본이 거의 없고 모델 호출이 드는 측정이다
- reflect-kit `plugin.json` 버전 — Final 이 올린다

reflect-kaizen 절차를 이번 사이클에 돌린 값(읽기만): §0 `tag_canon_selftest` → `SELFTEST_OK raw=4 clusters=2 canonical=edit-before-read`, 전 폴더 reflections 11 파일의
`tag_canon_fragmentation` → `3104 3024 5339 2682 1.03 0.887 1.77` — `singleton_share 0.887` > 0.70 이라 `calibration_confidence: low`. §3 은
`~/.claude/logs/*/promotions-ledger.md` 가 없어 해당 없음, §4 는 §0 이 `low` 라 건너뛴다.

실제 로그에 새 함수를 돌린 값(2026-09-25 10:05, 읽기만): 로그 폴더 31 개 전부에 `collect_status 30` →
`Stop 실패 시도 2235회 (codex 실패 2235 · 대체 경로 실패 2235 · 대체 경로 성공 0 · 분석 전 중단 0; 고유 세션 151) / 기록된 세션 17 / 엔트리 117 / 마지막 기록 2026-08-28T17:28:39+0900`.
`claude-plugins` 폴더 하나에 `collect_status 30` → 실패 시도 442 · 고유 세션 25 · 기록 0 · 엔트리 0 과 `⚠ 수집 멈춤` 줄. `facets_unmatched all all` → facets 18 · 마찰 16 · reflections 없음 16,
`facets_unmatched all claude-plugins` → 6 · 5 · 5. 이 작업 폴더에서 `project_root` 는 `/Users/jackson/Hub/10_Dev/claude-plugins` 를 낸다.
**설치본이 새 판으로 바뀌기 전까지 수집은 계속 멈춰 있다** — 실제 Stop 훅은 `~/.claude/plugins/cache/…/reflect-kit/<판>/hooks/` 의 옛 판이 돈다. `fallback:claude-exit-1` 누계는 지금 3,042 건이고 계속 는다.

Phase 1 가이드 변경 셋(오케스트레이터 전수 감사):

| 가이드 변경 | 이 킷 | 자리 |
| --- | --- | --- |
| `[미검증]` 네 칸 (skill-design-guide §3.7) | 해당 없음 | `reflect-kit/` 에 `[미검증]` 을 내는 자리가 0 이다(codex-kaizen 의 「출처 미검증」 두 줄뿐) |
| 0 이 아닌 값을 내는 새 측정 — 알려진 답 대조 (§3.7) | 해당 — 반영 | 새 측정 `collect_status` · `facets_unmatched` · `project_root` 셋 모두 손으로 센 답으로 재는 시험이 있다(SC-05 ~ SC-07) |
| agent 가이드 §10 | 해당 없음 | 이 킷에 에이전트가 없다 |

## 넘기는 것

| 대상 | 누가 | 할 일 |
| --- | --- | --- |
| `harness/scripts/save-feedback.sh` | 다음 사이클 Phase 4 | `identity_root_of` 가 `--show-toplevel` 을 써서 워크트리에서 부르면 `project_name` 이 워크트리 이름이 된다(이번 계약 피드백도 `project_name: 'kaizen-0924'`). reflect-collector:P5 와 같은 규칙이다 — 이 계약의 `project_root` 와 `reflect-kit/evals/hooks/project-id-test.sh` 의 경우 표를 그대로 옮기면 된다 |
| `harness/agents/qa-evaluator.md` Step 3.4 (754~765 줄) · `harness/docs/guides/qa-evaluation-guide.md` (643~652 줄) | 다음 사이클 Phase 3 | prompt 로그 폴더를 `basename(--show-toplevel)` 로 찾는다. 새 판 reflect-kit 이 배포되면 워크트리 세션의 새 발언은 본 레포 폴더로 가므로 평가자 쪽 규칙도 `project_root` 로 바꾼다 |
| `reflect-kit/hooks/hooks.json` 따옴표 | 다음 사이클 Phase 4 | 킷 넷의 `hooks.json` 이 따옴표 없는 `${CLAUDE_PLUGIN_ROOT}` 를 쓴다. `validate-plugin.py` V8 에 검사를 두고 넷을 한 번에 고친다 |
| `reflect-kit/.claude-plugin/plugin.json` | Final | reflect-kit 버전(지금 0.7.1). 훅 동작 · 폴더 이름 규칙 · digest 출력 틀이 바뀌었다 |
| `reflect-kit/README.md` 의 `` 버전: `0.3.0` `` 줄 | 다음 사이클 Phase 12 | 실제 판은 0.7.1 이다. 버전을 README 에 적을지부터 정한다(이 Phase 는 킷 버전을 적지 않는다 — AP-01) |
| `docs/reflect-kit/` 페이지 | Final F2 | `scripts/detect-docs-drift.py` 가 `reflect-kit/skills/` 를 `docs/reflect-kit/` 로 잇는다. digest · kaizen 문서 페이지를 다시 만든다 |
| `.github/workflows/ci.yml` | Final | 새 시험 셋을 돌리는 줄 셋 — `bash reflect-kit/evals/hooks/log-reflection-test.sh` · `bash reflect-kit/evals/hooks/project-id-test.sh` · `bash reflect-kit/evals/hooks/collect-status-test.sh` (`jq` · `git` 이 필요하고 zsh 가 없으면 zsh 경우를 건너뛴다) |
| reflect-kit 설치본 | Final 뒤 | 배포 뒤 설치본에서 Stop 훅이 실제로 reflections 를 적는지 한 번 본다(`collect_status 1` 의 `기록된 세션` 이 1 이상) — 이 계약은 가짜 분석기로만 쟀다 |

Final 이 볼 한 줄: `harness/agents/qa-evaluator.md` Step 3.4 는 워크트리 폴더 이름으로 prompt 로그 폴더를 찾는다. reflect-kit 새 판이 배포되면 워크트리 세션의 새 발언은
본 레포 폴더로 가므로, 다음 사이클 Phase 3 이 고치기 전까지 그 단계는 워크트리 계약에서 새 발언을 하나도 못 읽고 조용히 넘어간다.

Final 이 더 할 것: 이 Phase 는 공유 파일(marketplace · `plugin.json` · 루트 README · 루트 CLAUDE.md · `docs/` HTML · 감사 기록 · 실패 횟수 파일 · 처리 배정표 ·
`.github/workflows/ci.yml` · `.harness/stale-values.yaml`)을 건드리지 않았다.

## changelog 한 단락

reflect-kit Stop 훅이 다시 기록을 남긴다. 2026-08-28 부터 codex-cli 0.154.0 이 훅의 `--full-auto` 인자를 거부해 한 달 가까이 아무것도 못 적었는데, 두 분석기의 stderr 를 버려서
원인이 로그에 한 줄도 없었다. 이제 codex 는 `-s read-only` 로 부르고, 실패하면 `.errors.log` 에 원인 한 줄(`err=`, 가린 뒤 200 자)을 남긴다. 대체 경로는 CLI 가 아는 모델 별칭
`haiku` 로 바꿨고, 분석기 세션에서 도는 reflect-kit 훅은 아무것도 적지 않는다 — 대체 경로가 원시 로그에 분석용 프롬프트를 3,000 건 넘게 적고 있었다. `/reflect-digest` 요약 머리
첫 줄은 수집 상태(`collect_status`)라 엔트리 0 이 「문제 없음」 으로 읽히지 않고, `/insights` facets 는 빈도에 더하지 않고 놓친 세션을 드러내는 대조 절에만 쓴다.
`/reflect-kaizen` §0 도 수집이 멈추면 보정 신뢰도를 낮춘다. 워크트리 안에서 불러도 로그 폴더는 본 레포 이름이다. 새 시험 셋(`reflect-kit/evals/hooks/`)이 이 동작을 잰다.
실제 수집은 reflect-kit 새 판이 설치된 뒤부터 살아난다.

## 킷 로그 한 단락

2026-09-25 reflect-kit (카이젠 2026-09-24 Phase 12) — 처리 배정표 Phase 12 행 셋(`reflect-collector:P3` · `reflect-collector:P4` · `reflect-collector:P5`)을 받았다.
P3 을 고치다 대체 경로가 원시 로그를 더럽힌 것(분석기 표식)을 새로 찾았다. `save-feedback.sh` 의 같은 규칙은 범위 밖이라 다음 사이클 Phase 4 로 넘겼다.
근거: [Codex non-interactive mode](https://developers.openai.com/codex/noninteractive) · [Codex CLI v0.156.1](https://github.com/openai/codex/releases/tag/rust-v0.156.1) ·
[Claude Code model configuration](https://code.claude.com/docs/en/model-config) · [Claude Code CLI reference](https://code.claude.com/docs/en/cli-reference) ·
[headless mode](https://code.claude.com/docs/en/headless) · [Claude Code Hooks reference](https://code.claude.com/docs/en/hooks) ·
[git-rev-parse](https://git-scm.com/docs/git-rev-parse) · [Reflexion](https://arxiv.org/abs/2303.11366) · [MultiSoc-4D](https://arxiv.org/abs/2605.06940).

## 다음 사이클 메모

- `facets_unmatched` 는 session-meta 의 `project_path` 가 지워진 워크트리를 가리키면 git 이 본 레포를 못 구해 워크트리 폴더 이름으로 남긴다. `scripts/collect-kaizen-data.py:421` 은
  `/.claude/worktrees/` 글자 앞에서 잘라 본 레포로 묶는다 — 지금 facets 18 개는 경로가 전부 살아 있어 영향이 없다. 지워진 워크트리 세션이 생기면 두 규칙을 맞춘다
- 러닝북 검증의 `scripts/sync-evals.py --check-only` 는 종료 코드 0 이었다. 조건으로 걸지 않았다 — 그 스크립트의 대상 목록 `TARGET_KITS` 에 reflect-kit 이 없어 이 Phase 의 변경이 결과를 바꿀 수 없다
- 이번 계약의 시험 측정 구멍 둘을 검토자가 찾았다: 시험이 실패를 `불일치 <이름>` 으로 찍어 그 줄에도 `일치 <이름>` 이 들어 있었고(줄 머리로 거른 뒤 센다), 가짜 codex 가 인자를 거부하기 전에
  호출을 적지 않아 「`--full-auto` 없음」 줄이 떨어질 수 없었다. 시험을 낱말로 세는 다른 킷 계약에도 같은 구멍이 있는지 본다
- `collect_status` · `facets_unmatched` 는 bash 에서만 시험했고 bash 가 아니면 멈춘다. zsh 에서도 같은 답을 내게 하려면 시험에 zsh 경우를 먼저 넣는다
- 워크트리 이름으로 이미 생긴 12 개 폴더는 옮기지 않았다. 새 판 배포 뒤 그 폴더에 새 기록이 더 쌓이지 않는지 한 번 본다
