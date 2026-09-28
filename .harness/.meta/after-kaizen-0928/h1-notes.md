# h1 — harness 계약 규칙 · 검사 도구 약점 (2026-09-28)

계약 `.harness/sprint-contract-after-0928-harness-checks.md` (36 조건, 봉인 `455c55aaa06642fa` · 측정 `d6e75fb37b35d6bd`).
가지 `chore/ak3-h1`, 시작 판 `95508d9`. QA 판정과 `status: done` 전환은 이 묶음에서 하지 않았다.

## 항목별 결과

| 항목 | 결과 | 근거 (명령 출력) |
| --- | --- | --- |
| B1 | 고침 — 머리 읽개 셋이 따옴표와 줄 끝 주석(빈칸 · 탭 뒤의 `#`)을 벗긴다. `abc#def` 는 값 그대로 | `m-fm.sh` → `ng=0 total=42` (전 `ng=24`). 공용 측정 시험에 `F1-` ~ `F7-` 을 더했다: 새 판 `pass_F=7`, 옛 `fm_get` 사본 `pass_F=3 fail_F=4` |
| B2 | 고침 — `harness/scripts/check-superseded.sh` 와 시험, CI 두 단계 | `m-superseded.sh` → A `rc=1 checked=4 violations=3` · B `rc=0` · 없는 폴더 `rc=2` · 레포 `checked=3 violations=0` |
| B3 | 고침 — sprint-contract Step 0.5 에 superseded 로 바꾸는 절차 · 확인 명령 | `m-docs.sh` 의 `skill-0.5` 세 값 1 이상 |
| B4 | 고침 — 원문 덩어리 끝을 `판정 표와 두 경우는` 표지 줄 앞으로. 표지가 없으면 `CANON_MISSING` · 2 | `m-cause.sh` → b · c 가 `rc=1 mismatch=2`, e 가 `rc=2`. 시험 `scripts/test-check-cause-table-copies.py` 다섯 경우 통과 |
| B7 | 고침 — 접근성 검사가 `themeToggle` 단추도 잰다. visual-styles 단추 63x33 → 63x48 (320 · 375 · 1280 모두 63x48) | `m-a11y.sh` → 네 쪽 `OK`, 임시 작은 단추 `FAIL btn=60x30`, `rc=1` |
| B8 | 고침 — Phase 상한 = 4 + (harness 를 뺀 킷 수), 5 번부터 마켓 목록 차례 | `m-phase.sh` → 킷을 더한 사본 `n=18 rc=0 slug=kaizen-phase18-foo`, 도움말 `1 ~ 17` 0 건 |
| B9 | 고침 — run-evals · sync-evals 대상을 마켓 목록에서 뽑고 빼는 킷은 `SKIP <킷> (<사유>)` | `m-evals.sh` → 새 킷이 둘 다에 잡히고 sync-evals 는 사례 없는 스킬로 `rc=1` |
| B22 | 고침 — 계약 형식 문서 §측정 관례 에 규칙 다섯, sprint-contract Gotchas 에 그 절 안내 | `m-docs.sh` 의 `schema-측정관례` 일곱 줄 · `skill-gotchas` 두 줄 모두 1 이상 |
| D2 | 고침 — `scripts/ci-local.sh` 가 CI 파일의 run 단계를 직접 읽는다. 준비 단계 다섯은 SKIP, 못 다루는 열쇠는 UNSUPPORTED · 1 | `m-cilocal.sh` → `steps=40 run=35 skip=5 unsupported=0`, 단계를 더한 사본에서 새 단계를 돈다. 옛 도구 파일은 손대지 않았다(지문 `59fe55125c0dbc77`) |
| D4 | 결정 — 변환 스크립트는 레포에 두지 않는다 | 아래 절 |

## D4 — 변환 스크립트는 레포에 두지 않는다

- D4 결정: 새 쪽 · 다시 쓴 쪽을 만든 변환 스크립트(세션 임시 폴더 `dcb/gen` · `dr2/gen`)는 레포에 두지 않는다.
- 근거 1 — 같은 결과를 못 낸다. `bash .harness/.meta/after-0928-harness-checks/m-d4.sh <W> 95508d9 <scratch>/dcb/gen <scratch>/dr2/gen` 로
  판 `95508d9` 원본에 다시 돌린 결과 `same=6 total=21` 이다. 나머지 15 쪽은 그 뒤 원본이 바뀌었거나(코드 울타리 언어 표기) 스크립트 결함 때문에 다르다.
- 근거 2 — 결함이 있다. 원본의 `<!-- markdownlint-disable … -->` 주석을 본문 글로 옮긴다 (`docs/tone-kit/locale-korean.html` 차이 2 줄).
  레포에 들이면 다음 사람이 이 결함째로 쪽을 다시 만든다.
- 다시 만드는 길: 원본이 바뀌면 레포 `.claude/skills/docs-site` 스킬로 쪽을 고치고, `python3 scripts/detect-docs-drift.py` 가 원본 → 쪽 짝의 어긋남을 알린다.

## 교차 진단 반영 (봉인 전)

- `m-scope.sh` 가 서명 줄을 모델 이름 한 벌과 글자로 맞대어, 모델이 바뀌면 AR-05 가 늘 FAIL 한다는 지적 — 서명 판정을
  `Claude <이름> <noreply@anthropic.com>` 모양 한 줄로 바꿨다. 같은 규칙을 §측정 관례 셋째 줄에도 적었다.
- 기능 조건 28 개로 가이드 상한 20 을 넘지만 한 묶음으로 갔다 — 나누면 CI 파일 · 종료 코드 표 · 계약 형식 문서를 두 가지에서 따로 고쳐 부딪힌다.

## 킷 버전 판단

- harness: 올린다 — patch (0.16.0 → 0.16.1). qa-evaluator · sprint-contract · 계약 형식 문서의 동작(머리 값 읽기)이 바뀌고 새 확인 스크립트가 들어간다. 기능 추가지만 규약 뜻은 그대로라 patch 로 본다.
- design-kit: 올리지 않는다 — `docs/` 쪽만 바뀌었다(킷 폴더 밖).
- 그 밖 킷: 바뀐 것 없음. `scripts/` · `.github/` 는 킷 밖이다.
- 릴리스는 통합 가지에서 한 번에 한다(이 가지에서 `release.sh` 를 돌리지 않았다).

## 남은 것

- QA 판정: qa-evaluator 로 이 계약을 평가해야 한다 — 이 묶음의 구현자는 판정을 하지 않는다는 지시를 따랐다.
- 옛 로컬 CI 도구 `/Users/jackson/Hub/10_Dev/claude-plugins/.harness/handoff/2026-09-26-tools/ci-local.sh` 는 그대로 있다 — 그 경로 · 지문을 적은 봉인 계약이 있어 지우거나 고칠 수 없다. 앞으로의 계약은 `scripts/ci-local.sh` 를 쓰면 된다.
- 카이젠 오케스트레이터 문서(`.claude/skills/kaizen-orchestrator/SKILL.md` · `docs/process/kaizen-flow.html` 등)는 여전히 「Phase 1~17」 이라 적는다. 지금 킷 수로는 맞지만 킷이 늘면 손으로 고쳐야 한다 — 이 계약 범위 밖이라 두었다.
- 로컬 CI 새 도구는 `npm ci` 같은 준비 단계를 돌리지 않는다. 새 작업 폴더에서는 `npm ci` 를 먼저 해야 playwright 단계가 돈다.

## 독립 검토 뒤 고친 것 (2026-09-28)

- B1 남은 자리: `harness/scripts/commit-guard.sh` 의 `scope_blocks` 안 `val()` 이 줄 끝 주석을 값으로 읽었다.
  `status: active   # 진행 중` 계약을 없는 것으로 봐 범위 밖 커밋이 통과했다. fm_get 과 같은 규칙으로 고치고 시험 SCOPE-s24~s26 을 더했다 (76b6cc5).
  이 두 파일은 AR-05 의 18 경로 밖이다 — AR-05 는 이제 20 경로로 FAIL 한다. 경로 목록을 넓히는 개정(느슨해지는 쪽)이나 새 계약이 필요하다.
- B9: run-evals · sync-evals 가 평가 파일 없는 킷 이름을 한 줄로 찍는다 (dd60755). SC-09 · SC-10 측정값은 그대로다.
- B8: `spawn-kaizen-phase.sh` 의 §2 · §3 을 킷 이름으로 고른다 (dd60755).
- B3: sprint-contract 의 스크립트 셋을 설치 환경에서도 찾게 했다 (df5adaf).
- SC-07 의 1 회 `63x33` 은 부하 탓이 아니라 기본 작업 폴더(고치기 전 파일)를 잰 것으로 보인다 — 검토자가 같은 값을 다시 냈다. 봉인된 QA 리포트는 고치지 않는다.
- 레포 밖 `~/.claude/hooks/qa-pending-check.sh` 의 `value()` 도 같은 결함이다. 작업 폴더 밖이라 손대지 않았다 — 50~60 줄의 값 읽기를 fm_get 규칙으로 바꾸면 된다.

## 2 회차 계약 (2026-09-28)

계약 `.harness/sprint-contract-after-0928-harness-checks-r2.md` (44 조건, 기능 36). 1 회차 계약은 `status: superseded` 로 두었다 (0fbb27d).
봉인 `conditions_digest: sha256:925cf12b1330ffe9` · `measurement_digest: sha256:ff2e15044cb81057` · `locked_at: 2026-09-28 14:09`, 봉인 커밋 3f44337 (파일 1 개).
교차 진단 지적 하나(GAP 분석 · AR-05 알려진 답의 `commits=13` 이 측정 묶음 커밋 뒤 14)를 봉인 전에 고쳤다 — 조건 줄은 그대로 `n ≥ 1` 이다.
계약 피드백 `~/.harness/feedback/contract/1a3bcba6-2026-09-28T140952-bda55d45-38415.yaml` 은 verify-feedback `PASS`.

### 이 판에서 한 구현

- 레포 밖 훅 `~/.claude/hooks/qa-pending-check.sh` 의 `value()` 만 고쳤다 — 따옴표 값은 닫는 따옴표까지, 아니면 빈칸 · 탭 뒤 `#` 앞까지 읽는다. 고치기 전 원본(지문 `bdf5f8cc581a32d7`)과 시험 `h1-backup/qa-pending-value-test.sh` 를 먼저 커밋했다 (600e7a7). 고친 뒤 지문 `b18721b2ab224706`.
- 지역 변수 이름은 `first` · `closing` 이다. `close` 는 awk 내장 함수라 쓰지 않았다.
- 그 밖의 구현은 1 회차 가지 커밋 그대로다. 새 조건이 구현 빈틈을 드러낸 곳은 없었다.

### 조건별 자기 측정 (가지 끝, 봉인 뒤)

| 조건 | 값 |
| --- | --- |
| 측정 파일 21 개 지문 | 계약에 적힌 값과 모두 같다 |
| SK-01 | `ng=0 total=42` · 종료 코드 0 |
| SK-02 · SK-03 · SK-04 · SK-05 | `skill-0.5` 1 · 2 · 5, `skill-gotchas` 1 · 1, `schema-측정관례` 일곱 모두 1 이상, `schema-전체` 1 |
| SC-01 · ER-01 | A · B · REPO 세 줄 계약과 같다 (`REPO rc=0 checked=4 violations=0 states=`), `MISSING rc=2` |
| SC-02 · SC-05 · SC-12 | `그대로 rc=0 broken=0` 셋, `망가뜨림 rc=1 broken=1` 셋, `two-run rc=1 … failed=1] fail_line=1 pass_line=1` |
| SC-03 | `current rc=0 pass_F=7 fail_F=0 swapped=0` · `old-fm_get rc=1 pass_F=3 fail_F=4 swapped=1` |
| SC-04 · ER-03 | a · b · c · d 네 줄 계약과 같다, `e-note-removed rc=2 … applied=0` |
| SC-06 · SC-07 | 여섯 줄 계약과 같다 (visual-styles `btn=63x48`), 전체 `189/189 PASS` · 쪽 189 · 종료 코드 0 |
| SC-08 · ER-04 | `same` · `foo` 슬러그 17 개와 `foo n=18 … kaizen-phase18-foo`, 범위 밖 다섯 줄 `rc=1 slug=`, `help_1_17=0` 둘 |
| SC-09 · SC-10 | `m-evals.sh` 네 줄 계약과 글자까지 같다 |
| SC-11 · ER-02 | `repo-list … steps=40 run=35 skip=5 unsupported=0` · `extra-list … extra_run=1` · `wd-list rc=1 … unsupported_line=1` · `none-list rc=2`, `grep -cE` 0 |
| SC-13 | `steps=40 run=35 skip=5 unsupported=0 failed=0` · 종료 코드 0, 여섯 단계 이름 모두 `PASS` 줄에 1 이상 |
| SC-14 | `guard chore/ak3-h1 rc=0 fails=0 s24=PASS s25=PASS s26=PASS` · 음성 대조 `guard 95508d9 rc=1 fails=2 s24=FAIL s25=FAIL s26=PASS` |
| SC-15 | 고친 훅 `ng=0 total=7` · 종료 코드 0, 원본 사본 `ng=4 total=7` · 1 |
| SC-16 | 고친 훅 `plain rc=0 caught=1` · `cmt rc=0 caught=1`, 원본 사본 `cmt rc=0 caught=0` |
| SC-17 | 고친 훅 종료 코드 0 (`failed=0 total=7`), 원본 사본 1 |
| SC-18 | `run` · `sync` 둘 다 `rc=0 absent=[planning-kit, reflect-kit, bambu-kit, onboarding-kit]`, `0bf2dad` 는 `absent=[]` |
| SC-19 | `same` · `mid` 둘 다 `s2=flutter-toolkit,rust-kit,bambu-kit s3=react-kit bad_rc=0`, `0bf2dad` `mid s2=aaa-kit,infra-kit,reflect-kit s3=rust-kit` |
| SC-20 | bash · zsh `repo=0 plugin=0 market=0`, `feedback_repo_rel=0`. `0bf2dad` 는 `plugin=127 market=127` · `feedback_repo_rel=2` |
| AR-01 | 사라진 명령 0, 새 명령 넷이 계약과 같다 |
| AR-02 | `rows=14 cite=14 only_rows=[] only_cite=[]`, 새 두 행 `grep -cE` 2 |
| AR-03 | `html` 세 값 1 이상, `assets/site.css=1`, `fm_same=1 md_lines=17 html_lines=17`, 쪽 `OK … of=0/0/0/0` |
| AR-04 | (1) 3 줄 (2) 1 · 1 (3) 1 · 1 (4) 0 |
| AR-05 | `changed=` 20 경로가 계약과 같다, `commits=16 bad=0 dirty=0` (이 notes 커밋 전) |
| AR-06 | (1) `59fe55125c0dbc77` (2) 0 (3) 0, 양성 대조 1 |
| AR-07 | (1) `bdf5f8cc581a32d7` (2) 0 (3) `outside_diff=0 fn=1 syntax=0` (4) `b18721b2ab224706` |
| AP-03 · AP-04 | 종료 코드 0 · 0 |
| RE-02 | 자기 읽개 0, `measure-common.sh` 1 |
| DG-01 | 0 |
| DG-02 | `md_new=0 sh_new=0 py_bad=0 js_bad=0 files=20`, 훅 shellcheck 종료 코드 0 |

### 2 회차 검사

- `python3 scripts/validate-plugin.py` → `14 plugins, 14 OK` · 종료 코드 0. `sync-docs.py --check-only` 0. `sync-evals.py --check-only` → `0 added, 0 orphans, 0 missing` · 0.
- 새 로컬 CI(`scripts/ci-local.sh`) 위 SC-13 값. 옛 도구(`.harness/handoff/2026-09-26-tools/ci-local.sh`) 종료 코드 0, 모든 단계 `rc=0`, `feedback-agg-test` 만 yq 가 없어 SKIP. 옛 도구가 모르는 새 단계는 「이 스크립트 밖의 것」 목록으로만 나온다.
- `detect-docs-drift.py` → `harness/references/contract-schema.md → docs/harness/contract-schema.html` 한 짝을 알린다. 이 가지가 두 파일을 같이 고쳤고 AR-03 `fm_same=1` 이다. `--check-table` 은 어긋남 0.

### 톤 대조 (tone-guide 5 단계)

어댑터 없음(오버레이 `.claude/tone-project.md`), 주석 언어 ko. 대상은 새 시험 파일과 훅 `value()`.

| 규칙 | 건수 | 판정 |
| --- | --- | --- |
| C-01 · C-02 (what 대신 why, 이름 반복) | 0 | 통과 — 시험 머리 두 줄은 쓰는 법과 종료 코드 뜻 |
| C-04 · C-09 (템플릿 마커 · 구분선) | 0 | 통과 |
| C-07 (해설 3 줄 초과) | 0 | 통과 |
| C-15 (주석 종결형, 관측 컨벤션) | 0 | 통과 |
| N-08 (한 글자 이름) | 0 | 통과 — 1 회차 사본의 `c` · `e` 를 `first` · `closing` 으로 |
| N-09 (무역할 파일명) | 0 | 통과 |
| S-03 · S-04 (의미 없는 추출 · 넘기기만 하는 래퍼) | 0 | 통과 |
| S-12 (같은 역할은 같은 모양, 관측 컨벤션) | 0 | 통과 — 함수 떼기 · 입력 일곱은 `m-qapending.sh` 와 같은 모양 |
| H (보존 주석) | 0 삭제 | 훅의 기존 주석 세 줄(첫 머리말 블록 · 따옴표 · find 제약)은 그대로 |
| K-02 G-1 (번역투 여섯 종) | 0 | 통과 — 새 시험 파일 · 이 절에 grep |

### 킷 버전 판단 (2 회차)

- harness: 1 회차 판단 그대로 patch (0.16.0 → 0.16.1). 이 판에서 레포 파일은 `.harness/` 안만 더했다.
- 그 밖 킷: 바뀐 것 없음. 레포 밖 훅은 킷이 아니다.

### 2 회차 남은 것

- QA 판정: qa-evaluator 로 2 회차 계약을 평가해야 한다. 이 묶음은 판정하지 않았고 `status` 는 `active` 그대로다.
- 레포 밖 훅은 이 컴퓨터에만 있다. 되돌리려면 `h1-backup/qa-pending-check.sh` 를 `~/.claude/hooks/` 로 복사하면 된다.
- AR-05 의 커밋 수는 이 notes 커밋 뒤 17 이 된다 — 조건은 `n ≥ 1` 이다.
- 지시문에 적힌 notes 경로 `.harness/.meta/after-kaizen-0926b/h1-notes.md` 는 없는 파일이다. 계약 AR-04 가 재는 `.harness/.meta/after-kaizen-0928/h1-notes.md` 에 이어 썼다.

### 2 회차 QA 뒤 남은 것

- QA 판정: APPROVE, 44/44 실측 통과. 계약 `status` 는 `done` 으로 바꿔 판정 기록과 함께 커밋했다.
- 교차 진단: 평가자 피드백의 `Cross-Diagnosis Handoff` 가 `pending-parent` 다. 부모 세션이 교차 진단을 돌려 `cross_diagnosis_by` 를 채워야 한다.
- 독립 검토에서 막지 않는 결함 1 건 — `scripts/ci-local.sh:37-46`
  - 단계 안의 추가 설정만 보고, 작업 전체나 워크플로 전체에 걸린 `if` · `env` · `defaults.run.working-directory` 는 보지 않는다. 그런 단계를 못 다룬다고 알리지 않고 레포 뿌리 폴더에서 그냥 돌린다. 머리 주석의 「흉내 내지 않고 알린다」와 동작이 다르다.
  - 재현: 작업 `a` 에 `defaults: run: working-directory: sub` 와 `env: MUST: yes`, 단계 `Where` 가 `test "$(basename "$PWD")" = sub && test "$MUST" = yes`. 작업 `b` 에 `if: false`, 단계 `Never` 가 `exit 3`. 이 파일을 임시 폴더에 두고 `bash scripts/ci-local.sh <폴더>`.
  - 출력은 `FAIL a Where rc=1` · `FAIL b Never rc=3` · `failed=2`. 기대는 `UNSUPPORTED` 두 줄.
  - 지금 `.github/workflows/ci.yml` 에는 그런 설정이 없어 SC-13 결과엔 영향이 없다. 들어오는 날부터 틀린 결과가 난다. 다음 묶음에서 작업·워크플로 단계의 `if` · `env` · `defaults` 를 보면 `UNSUPPORTED` 로 알리게 고친다.
- 레포 밖 훅 되돌리기 경로는 위 절 그대로다.
