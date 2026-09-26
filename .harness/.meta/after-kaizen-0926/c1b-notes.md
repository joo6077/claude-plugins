# c1b 구현 기록 — harness 커밋 훅 · 오케스트레이터 · 문서 매핑 후속

- 계약: `.harness/sprint-contract-after-0924-harness-orch.md` (봉인 `sha256:d65525591fade384`, 봉인 커밋 `86f63a3` — 파일 1 개)
- 가지: `chore/ak-c1b-harness-docs`, 기준 `f81568d`
- 계약 피드백: `/Users/jackson/.harness/feedback/contract/1a3bcba6-2026-09-26T121840-bda55d45-21477.yaml` (verify-feedback PASS)
- 측정 도우미: `.harness/.meta/after-0924/harness-orch-tools/` 17 개 (커밋 `2c85936`)
- QA: 1 회차 27/27 APPROVE → 교차 진단 뒤 고침(`bb4b2b1`) → 2 회차 APPROVE. 리포트 `.harness/sprint-feedback-after-0924-harness-orch.md`, 계약 status done (커밋 `188a25b`)

## 한 일

| 커밋 | 내용 | 조건 |
| --- | --- | --- |
| `86f63a3` | 계약 봉인 (27 조건) | — |
| `2c85936` | 측정 도우미 17 개 | AR-03 |
| `7b0ba08` | 커밋 안전 훅: `-a` · 같은 명령 `git add -A`/`.`/`-u` 도 목록 사본에 작업 폴더 상태를 얹어 이름 바꾸기를 삭제로 세지 않는다. `-i` 막힘 설명의 「작업 폴더 삭제 포함」 되살림. 시험 ㉛~㊴ 추가 | SC-01 · SC-02 · SC-07 · ER-01 · RE-02 |
| `aea6e75` | 매핑 표를 docs-site Step 1 한 곳으로, 오케스트레이터 F2 는 가리키기만. 낡은 페이지 감지 짝 여섯 추가 · 초안 폴더 제외 · 없는 폴더 `planning-kit/references/` 삭제 · 표에 `docs/flutter/` | SK-01 · SK-02 · SC-03 · SC-04 |
| `a987ef3` | css-tokens accent 표에 Howto Kit 행 (`#F59E0B` 계열). 같은 파일의 기존 경고 셋(표 구분 줄 MD060 · 코드 블록 앞뒤 빈 줄 MD031 둘)도 고침 | SK-03 |
| `afff36a` | sync-orchestrator 범위 줄이 킷에 있는 `references/` · `skills/*/references/` · `agents/` · `hooks/` · `docs/` · `evals/` 를 모두 적고 planning 리서치 폴더도 적는다. 오케스트레이터 옛 설명 문장 고침. 같은 파일의 자리표시 없는 f-string 경고도 고침 | SC-05 · ER-02 |
| `a99a1ca` | Phase 별 참조 표를 오케스트레이터 · 데이터 풀 §6 모두 1~17 로 | SK-05 |
| `4bc33c8` | 킷별 리서치 기록 목록을 네 자리 모두 아홉 개로, PASS 줄 개수를 목록 길이에서 뽑음 | SK-06 · SC-06 |
| `9c24bbc` | Phase 17 howto-kit 리서치 틀 절 추가, 오케스트레이터 「표가 아직 없다」 문장 삭제 | SK-04 |
| `1c17532` | 톤 대조 반영 (아래 `## 톤 대조`) | — |
| `bb4b2b1` | 교차 진단 뒤 고침 — 훅의 파일 ↔ 폴더 바뀜 · 경로를 좁힌 `git add` 구멍, 시험 ㊵~㊿ (아래 `## 교차 진단 뒤 고침`) | SC-01 · SC-02 |
| `188a25b` | QA 2 회차 APPROVE 리포트 · 계약 status done | — |

판단이 갈린 곳과 근거:

- 기록 파일 경로: 계약 원안은 `.harness/.meta/after-0924/harness-orch-notes.md` 였고 구현 지시는 이 파일이었다. 봉인 전에 계약 AR-02(b) 를 이 경로로 맞췄다.
- Phase 13~17 참조 칸: 13 · 14 는 오케스트레이터에 이미 있던 글을 수집기에 옮겼다. 15~17 은 Hub 외부 사용 기록이 없는 최근 킷이라 11 Planning 행과 같은 꼴(`§1 <킷> 관련 feedback (있을 시), §5`)로 썼다.
- 매핑 짝: design-kit 은 `design-kit/references/` 전체가 아니라 짝이 있는 두 파일만 이었다. 폴더 전체로 이으면 페이지 없는 원본이 새 페이지 대상으로 잡힌다. reflect-kit 셋과 api-ui 는 이름 규칙으로 못 잇거나(대문자 파일 이름 · 다른 페이지 이름) 맥 파일 시스템에서 대소문자가 틀린 대상을 내므로 개별 지정으로 넣었다.
- 훅의 작업 폴더 범위: `-a` · `git add` 경로의 삭제 목록은 예전과 같게 커밋하는 폴더 아래만 본다(`git ls-files` 기본 범위). 이름을 저장소 기준으로 맞추려고 `--full-name` 만 더했다.

## 넘김

- `N1` 짝 원본이 없는 등록 페이지 21 쪽 — 쪽마다 원본을 정해야 하고 f2 교차 진단이 짚은 범위 밖이다. 관찰: `design-kit/references/visual-styles.md` ↔ `docs/design-kit/visual-styles.html` 은 이름이 같아 다음 후보로 보인다(이번에는 잇지 않았다).
- `N2` 없는 페이지를 가리키는 원본 43 개 — 원본 ↔ 페이지 이름 규칙부터 정해야 한다.
- `N3` `docs/howto/design-brief.md` ↔ `docs/howto-kit/overview.html` 짝 — overview 가 README 를 5 회, design-brief 를 2 회 인용해 원본 하나로 못 정한다.
- `N4` 매핑 표와 스크립트를 늘 맞대는 검사 — 새 기능이라 이번에는 계약 SK-01 로 한 번만 쟀다.
- `N5` `scripts/spawn-kaizen-phase.sh` 의 Phase 별 데이터 풀 절 배정(5~10 만 §2 · §3) — 과제 목록 밖.
- `N6` howto-kit 리서치 기록 파일 — 만들지 않는다. howto-research 가 기록 파일을 쓰지 않는다. Phase 17 틀의 주의 셋째 줄과 오케스트레이터 Gotcha 에 같은 결정을 적었다.
- `N7` 범위 줄에 킷의 `scripts/` · `templates/` 가 빠져 있다(교차 진단 셋째 지적, 판정 영향 없음). `scripts/sync-orchestrator.py` 의 `KIT_SCOPE_DIRS` 와 `phase-dependencies.md` 에 두 폴더가 없는데, 2026-09-24 카이젠이 `howto-kit/scripts/howto-gate.sh`(`5a96f7c`) · `react-kit/scripts/project-detect.sh` · `react-kit/templates/vite.config.template.ts`(`001c900`) · `bambu-kit/scripts/option-key-probe/generate-option-list.py`(`c012f2b`) 를 고쳤다. 계약 SC-05 가 폴더 다섯 가지로 정해 두어 이번 고침 범위 밖이다.
- `N8` 커밋 안전 훅이 `f81568d` 때부터 놓치는 두 모양 — 이번 가지가 만든 구멍이 아니다. (a) `-A` · `-u` 없는 `git add <경로>` 도 git 2.x 에서는 그 경로의 삭제를 싣는데 훅은 세지 않는다(`rm -rf d1; git add d1 && git commit` 이 통과, git 이 싣는 삭제 60). `add_all` 로 올리면 가장 흔한 `git add <파일> && git commit` 에서 되돌림 검사가 꺼지므로 따로 설계해야 한다. (b) 하위 폴더에서 `git commit -a` 를 하면 작업 폴더 삭제를 그 폴더 아래만 센다. 두 경우 모두 커밋 직후 알림(`post`)은 뜬다.
- 기존 경고(범위 밖, 사용자 확인이 필요해 손대지 않음): `.claude/skills/docs-site/SKILL.md` Step 2~7 의 markdownlint 9 건(MD032 · MD031 · MD025), `phase-research-templates.md` 의 12 건(MD024 · MD036, 이번에 더한 절에는 0 건), 오케스트레이터의 줄 길이(MD013 은 검사에서 끔). 이번 구간에서 더한 줄의 새 경고는 0 이다(DG-02).

## 킷별 버전 판단

| 킷 | 바뀐 파일 | 판단 | 이유 |
| --- | --- | --- | --- |
| harness | `harness/scripts/commit-guard.sh` · `harness/evals/hooks/commit-guard-test.sh` | patch | 훅이 옮긴 폴더를 삭제로 잘못 세던 판정 오류와 빠진 설명 줄을 고친 것이다. 새 기능 · 새 설정 없음 |
| (킷 아님) | `scripts/` 넷 · `.claude/skills/` 넷 | 릴리스 없음 | 레포 전용 도구 · 스킬이라 marketplace 에 없다 |

## docs 드리프트

`python3 scripts/detect-docs-drift.py --since f81568d` → `no docs drift since f81568d`. 바뀐 원본이 매핑 밖(`.claude/` · `scripts/` · `.sh`)이다.
`docs/harness/qa-evaluation-guide.html` 이 `harness/scripts/commit-guard.sh` 를 「50 개를 넘는 삭제만 막는다」 로 언급하는데 이번 변경 뒤에도 맞다. 다시 만들 페이지는 없다.

## 조건별 자기 측정 (상한 `1c17532` 에서 전부 다시 잼 — 이 기록 커밋은 `.harness` 만 바꾼다)

| 조건 | 값 |
| --- | --- |
| SK-01 | docs-site `rows=15 script_only=0 table_only=0 ghost=0`, 오케스트레이터 `rows=0`, `script_ghost=0` |
| SK-02 | (a) 1 · (b) 1 · (c) 0 · (d) 1 |
| SK-03 | `rows=1 pages=7 page_variants=1 match=1` |
| SK-04 | `heading=1 rows=7 urls=9 invented=0 missing_paths=0`, (b) 0 · (c) 0 |
| SK-05 | 두 표 `missing=[]` · `dup=[]` · `ref_13_17_differ=[]` · `not_s0=[]` · `collector_rc=0` |
| SK-06 | 네 줄 `n=9 missing_vs_want=[] extra=[]`, `checklist_number=9 want_files_exist=9/9 all_equal=1` |
| SC-01 | `mismatch_sc=0/7` (G1~G7 MATCH) |
| SC-02 | `old_fail=6 new_pass=54 new_fail=0 new_rc=0` |
| SC-03 | `expected_hit=7/7 unexpected=0 rc=0` |
| SC-04 | `orphan_pages=21 new_targets=43 added_orphan=0 added_new=0` |
| SC-05 | `uncovered=0 phases=13` · `folder_miss=0 ghost=0 kits=13` · `--check-only` 0 · 옛 문장 0 |
| SC-06 | `caught=9/9`, intact `PASS ... all 9 per-kit research-logs exist` |
| SC-07 | 세 번씩 여섯 줄 모두 `rc=0`, 가장 느린 값 `-a` 0.23 초 · `add -A` 0.46 초 |
| SC-08 | `steps=14 nonzero=0` |
| ER-01 | `mismatch_er=0/2` |
| ER-02 | `intact=0 no_begin_marker=2 no_marketplace=2` |
| AR-01 | `changed=10 outside=0 missing=0 multi_kit=0 no_hangul=0` (이 기록 커밋 전 10 커밋) |
| AR-03 | `diff` 출력 없음, 종료 코드 0 |
| AP-03 · AP-04 | 종료 코드 0 · `name:` 둘 다 있음 |
| RE-01 · RE-02 | 0 · 정의 1 호출 3 |
| DG-01 · DG-03 | 0 |
| DG-02 | `files=10 new_warnings=0` |
| DG-04 | 확장자 md 4 · py 4 · sh 2 |

로컬 CI(`ci-local.sh`): 스물두 단계 모두 종료 코드 0, `feedback-agg-test` 는 yq 가 없어 SKIP.

## 톤 대조

규칙은 레포 `tone-kit/references/` 의 core-comment · core-naming · core-structure · core-antipatterns · locale-korean 에서 읽었다. 어댑터는 없다(`.claude/tone-project.md`, 플러그인 모노레포 — 스택 고유 검사는 끔).

대조한 파일(이번 구간 `.harness` 밖 변경 전부):

- `.claude/skills/docs-site/SKILL.md`
- `.claude/skills/docs-site/references/css-tokens.md`
- `.claude/skills/kaizen-orchestrator/SKILL.md`
- `.claude/skills/kaizen-orchestrator/references/phase-research-templates.md`
- `harness/evals/hooks/commit-guard-test.sh`
- `harness/scripts/commit-guard.sh`
- `scripts/collect-kaizen-data.py`
- `scripts/detect-docs-drift.py`
- `scripts/sync-orchestrator.py`
- `scripts/validate-post-kaizen.py`

| 규칙 (강도) | 건수 | 판정 |
| --- | --- | --- |
| C-01 why 만 (SHOULD) | 0 | 통과 — 더한 주석은 모두 실패 모드 · 제약(H) 이다 |
| C-02 · A 이름 번역 주석 (SHOULD · MUST) | 2 → 0 | 고침 — `SOURCE_EXCLUDES` 앞 「페이지를 만들지 않는 원본.」, `KIT_SCOPE_DIRS` 앞 「범위 줄에 적는 킷 폴더.」 삭제 (`1c17532`) |
| C-04 · F 구분선 · 템플릿 마커 (관측 컨벤션 · MUST) | 0 | 통과 — 시험 파일의 `# ── … ──` 절 제목은 그 파일의 기존 꼴(S-12) |
| C-07 해설 3 줄 초과 (SHOULD) | 0 | 통과 |
| C-10 디자인 툴 참조 (MUST) | 0 | 통과 — css-tokens 값은 주석이 아니라 표 값 |
| C-12 · C-13 계산 근거 · 자화자찬 | 0 | 통과 |
| N-07 fallback 접두사 (관측 컨벤션) | 0 | 통과 |
| N-08 한 글자 이름 (SHOULD) | 0 | 통과 — 새로 지은 한 글자 이름 없음. 시험의 `r` · `k`, 생성식의 `p` 는 같은 파일 기존 꼴 |
| N-09 무역할 파일명 (SHOULD) | 0 | 통과 — 새 파일 없음 |
| S-03 · S-04 · S-06 추출 · 전달만 하는 층 · 헬퍼 사슬 | 0 | 통과 — `infer_references_dir` 를 `infer_scope_dirs` 로 바꾼 것뿐, 훅은 기존 `overlay_deletes` 를 다시 씀 |
| S-12 같은 자리 같은 꼴 (관측 컨벤션) | 0 | 통과 — 파일 경로 접두는 onboarding `SKILL.md` 줄과 같은 꼴, 개별 지정은 `SOURCE_OVERRIDES` |
| K-02 번역투 (SHOULD) | 0 | 통과 — 더한 문서 줄 grep 0 |
| K-11 새로 지은 이름 (관측 컨벤션) | 1 → 0 | 고침 — docs-site Step 1 의 「낡음 감지」 를 `scripts/detect-docs-drift.py` 로, 검사 이름 G5 · G6 에 괄호로 뜻을 붙임 (`1c17532`) |
| H 보존 | — | 지운 기존 주석 없음. 훅의 `-i` 설명 주석은 `-a` 까지 덮게 고쳐 썼고 정보는 그대로다 |

## 교차 진단 뒤 고침 (`bb4b2b1`)

QA 는 27/27 로 APPROVE 했지만 교차 진단이 훅에서 판정을 바꾸는 결함 둘을 찾았다. 둘 다 `f81568d` 판 훅은 막던 커밋을 이 가지 훅이 통과시킨 것이다.
계약 조건 줄은 고치지 않았다 — SC-01 의 「진짜 삭제는 그대로 막는다」 를 이 모양들에서 지키도록 훅을 고치고, 레포 시험에 줄을 더해 SC-02 · SC-08 이 다시 재게 했다. 개정 파일은 만들지 않았다.

| 결함 | 원인 | 고침 |
| --- | --- | --- |
| 파일 자리가 폴더로(또는 그 반대로) 바뀐 이름이 있으면 `git add -A` · `git add .` 커밋의 삭제 수가 0 이 된다. 이미 `git rm` 한 삭제도 사라진다 | `overlay_deletes` 에서 `git update-index` 가 종료 코드 128 로 실패하면 빈 값을 냈다 | `--replace` 를 준다(git add 와 같게 옛 항목을 바꿔 넣는다). 그래도 못 얹으면(읽을 수 없는 새 파일 등) 목록 사본의 삭제에 작업 폴더에 없는 이름을 더해 낸다 — 이름 바꾸기는 가리지 않는다 |
| `git add -A d1` · `git add -A -- d1` 처럼 경로를 좁혀도 경로 밖 추적 안 된 사본(`backup/`)이 삭제와 이름 바꾸기로 짝지어져 진짜 삭제 60 이 통과한다 | `git add` 인자에서 `-A` 만 보고 경로를 버린 뒤 저장소 전체의 추적 안 된 파일을 얹었다 | `handle_git` 이 `git add` 를 볼 때 그 자리에서 `ls-files --others` 를 그 add 의 경로(없으면 `:/`)로 좁혀 `add_untracked` 에 모은다. 새 파일은 `-A`, 또는 `-u` 없이 경로를 준 add 만 올린다. `-n` · `-i` · `-p` · `-e` · `-N` · `--pathspec-from-file` 은 새 파일을 얹지 않는다 |

판단이 갈린 곳:

- `-u .` 는 예전 훅이 `.` 만 보고 새 파일까지 얹었다. git 은 `-u` 에서 새 파일을 올리지 않으므로 얹지 않는다(시험 ㊻).
- `-u` 없는 경로 지정 add(`git add d2 && git commit -a`)는 git 이 그 경로의 새 파일을 올리므로 얹는다. 예전에는 옮긴 폴더를 삭제 60 으로 잘못 막았다(시험 ㊾). 경로 지정 add 자체를 `add_all` 로 올리지는 않았다 — `N8` (a).
- 목록 사본에 못 얹을 때의 대체 셈은 `overlay_deletes` 안에 두어 경로 지정 커밋(`check_path_commit`)도 같이 받는다. 예전에는 거기서도 빈 값(통과)이었다.
- 교차 진단 셋째 지적(범위 줄의 `scripts/` · `templates/`)은 조건 위반이 아니어서 고치지 않고 `N7` 로 넘겼다.

다시 잰 값 (상한 `bb4b2b1`):

| 조건 · 확인 | 값 |
| --- | --- |
| 교차 진단 재현(probe2 · probe3 · probe6) | P4b · P5 · P6 · P8 · P9 · `add -A -- d1` 모두 종료 2, 삭제 수가 git 이 실제로 싣는 수와 같다(60 · 61). 경로 없는 `add -A` 는 종료 0 그대로(git 도 이름 바꾸기) |
| SC-01 · ER-01 | `mismatch=0/9 mismatch_sc=0/7 mismatch_er=0/2` |
| SC-02 | `old_fail=11 old_rc=1 new_pass=65 new_fail=0 new_rc=0` |
| 음성 대조 | 고치기 전 훅(`fec3713`)으로 레포 시험을 돌리면 ㊵~㊿ 가운데 ㊽ 을 뺀 10 줄이 FAIL(㊽ 은 통과해야 하는 경우) |
| 변이 대조 | `--replace` 를 빼면 ㊵ ㊶ ㊷, 대체 셈을 빼면 ㊿, 경로 좁힘을 `:/` 로 바꾸면 ㊹ ㊺, `-n` 판정을 빼면 ㊼ 이 FAIL |
| SC-07 | `-a` 0.30 · 0.26 · 0.23 초, `add -A` 0.46 · 0.45 · 0.49 초, 여섯 줄 모두 `rc=0` |
| SC-08 | `steps=14 nonzero=0` |
| AR-01 | `changed=10 outside=0 missing=0 commits=12 multi_kit=0 no_hangul=0` |
| AR-03 · AP-03 | `diff` 출력 없음 종료 0 · 종료 0 |
| RE-01 · RE-02 | 0 · 정의 1 호출 3 |
| DG-02 | `files=10 new_warnings=0`. `shellcheck` 가 시험 파일 67 · 96 줄에 SC2016(info)을 내지만 둘 다 이번에 더한 줄이 아니다 |
| 로컬 CI | 스물두 단계 모두 종료 0, `feedback-agg-test` 는 yq 가 없어 SKIP |
| bash 3.2 | `/bin/bash -n` 통과, 레포 시험을 `/bin/bash` 로 돌려 `실패 0 건` |

톤 대조 (`harness/scripts/commit-guard.sh` · `harness/evals/hooks/commit-guard-test.sh` 에 더한 79 줄):

| 규칙 (강도) | 건수 | 판정 |
| --- | --- | --- |
| C-01 why 만 · C-07 해설 3 줄 초과 (SHOULD) | 0 | 통과 — 더한 훅 주석 셋은 실패 모드(H) 이고 한 덩어리가 1~2 줄 |
| C-02 · A 이름 번역 주석 (SHOULD · MUST) | 0 | 통과 |
| N-07 fallback 접두사 (관측 컨벤션) | 0 | 통과 — grep 0 |
| N-08 한 글자 이름 (SHOULD) | 0 | 통과 — 새 이름은 `names` · `name` · `take` · `after_dd` · `flag_all` · `flag_update` · `no_new` · `spec_file` · `specs` · `add_untracked` |
| S-03 · S-06 추출 · 헬퍼 사슬 (SHOULD · 관측 컨벤션) | 0 | 통과 — 새 함수 없음. `add` 인자 풀이는 같은 파일 `parse_commit_args` 와 같은 꼴(`take` · `after_dd`, S-12) |
| K-02 번역투 (SHOULD) | 0 | 통과 — 더한 줄 grep 0, 양성 대조 `값을 처리한다` 1 |
| K-11 새로 지은 이름 (관측 컨벤션) | 0 | 통과 — 「목록 사본」 은 이 파일이 이미 쓰던 말 |
| H 보존 | — | 지운 주석은 「얹지 못하면 빈 값(통과)이다」 한 구절뿐 — 동작이 바뀌어 거짓이 된 문장이라 대체 셈 주석으로 바꿨다 |

## QA 2 회차 뒤 확인 (상한 `188a25b`)

독립 검토가 판정을 바꾼다고 적은 결함 둘(파일 ↔ 폴더 바뀜 · 경로를 좁힌 `git add -A`)은 고치기 전 훅 `fec3713` 을 잰 것이다.
재현 스크립트는 13:00~13:05 에 만들어졌고 고침 커밋 `bb4b2b1` 은 13:19 다.
같은 스크립트 여섯(`scratchpad/c1b-review/probe1.sh` ~ `probe6.sh`)을 지금 훅으로 다시 돌렸다.

| 경우 | 지금 훅 | `fec3713` 훅 | git 이 싣는 삭제 |
| --- | --- | --- | --- |
| P4b 파일 → 폴더 + 작업 폴더 삭제, `add -A` | 종료 2 (삭제 60) | 종료 0 | 60 |
| P5 목록 삭제 60 + `a.txt` → 폴더, `add -A` | 종료 2 (삭제 61) | 종료 0 | 61 |
| P6 같은 상태, `add .` | 종료 2 (삭제 61) | 종료 0 | 61 |
| P8 `add -A d1`, 추적 안 된 사본 `backup/` | 종료 2 (삭제 60) | 종료 0 | 60 |
| P9 폴더 → 같은 이름 파일, `add -A` | 종료 2 (삭제 60) | 종료 0 | 60 |
| `add -A -- d1`, 사본 있음 | 종료 2 (삭제 60) | — | 60 |
| 경로 없는 `add -A`, 사본 있음 | 종료 0 | — | 0 (git 도 이름 바꾸기) |

probe1 · probe4 · probe5 의 나머지 여덟 경우(P1 ~ P4 · P9a · P9u · P10 · P11)도 지금 훅에서 모두 종료 2 다. 판정을 바꾸는 결함은 남아 있지 않다.

로컬 CI(`ci-local.sh`, 상한 `188a25b`): 스물두 단계 모두 종료 0, `feedback-agg-test` 는 yq 가 없어 SKIP.
`ci.yml` 의 `run` 줄 27 개 가운데 스크립트 밖 다섯은 설치 넷(`pip install pyyaml` · zsh · `npm ci` · playwright 브라우저)과 yq 가 있을 때만 도는 덩어리 하나다. 이 덩어리는 스크립트의 SKIP 줄이 대신한다.
CI 가 만든 `__pycache__` 두 폴더(flutter-scenario-report 시험)는 지웠다.

2 회차 평가자 피드백 `/Users/jackson/.harness/feedback/evaluator/1a3bcba6-2026-09-26T133724-bda55d45-59933.yaml` 의 교차 진단 칸은 `pending-parent` 다. 부모 세션이 채운다.

## 다음 사이클 메모

| ID | 항목 | 사유 · 받을 곳 |
| --- | --- | --- |
| N7 | 범위 줄에 킷의 `scripts/` · `templates/` 가 없다 (독립 검토 셋째 지적, 판정 영향 없음) | 계약 SC-05 가 폴더 다섯으로 정해 이번 범위 밖. 다음 사이클 오케스트레이터 범위 줄 고침 — `scripts/sync-orchestrator.py` `KIT_SCOPE_DIRS` · `.claude/skills/kaizen-orchestrator/SKILL.md` 범위 줄 · `.claude/skills/kaizen-orchestrator/references/phase-dependencies.md` |
| N8 | 커밋 안전 훅이 `f81568d` 때부터 놓치는 두 모양 (경로 지정 `git add <경로>` 의 삭제 · 하위 폴더 `commit -a`) | 되돌림 검사와 얽혀 설계가 따로 필요하다(위 `## 넘김` N8). 다음 harness 훅 계약 |
| N1 ~ N6 | 매핑 짝 · Phase 데이터 풀 배정 · howto 리서치 기록 | 위 `## 넘김` 그대로. docs-site 매핑 규칙 결정 · `scripts/spawn-kaizen-phase.sh` |
| QA-1 | QA 개선 제안 `[SC-01] 범위-미명시` — 열거한 G1 ~ G9 가 「진짜 삭제는 그대로 막는다」 는 목표 문장의 실제 모양을 다 담지 못했다. 1 회차가 27/27 로 통과한 뒤 교차 진단이 결함 둘을 찾은 이유다 | contract-kaizen. 목표 성격 하위 문장을 따로 된 조건으로 떼거나, 무작위로 만든 입력 몇 개를 최소 요건으로 둔다 |
| 기존 경고 | docs-site `SKILL.md` Step 2 ~ 7 의 markdownlint 9 건 · `phase-research-templates.md` 12 건 | 위 `## 넘김` 마지막 줄. 이번 구간에서 생긴 것이 아니라 사용자 확인 뒤 고친다 |
