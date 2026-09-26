---
feature: "계약 형식 문서 · 피드백 형식 — 남은 일 CS-1 ~ CS-11"
slug: after-0926-contract-schema
created: "2026-09-26 19:49"
complexity: "복잡"
conditions: 32
status: active
owner_session: bda55d45-296c-491f-89ba-b52042d58e72
conditions_digest: sha256:fdaf977d37a36b86
measurement_digest: sha256:b588e1b0e6a52014
locked_at: "2026-09-26 20:00"
---

# Sprint Contract — 계약 형식 문서 · 피드백 형식 (after-0926-contract-schema)

## 배경

- 남은 일 목록 `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0926b/.harness/.meta/after-kaizen-0926b/leftovers.md` 의 「## cs」 절 CS-1 ~ CS-11 을 처리한다. CS-12(`# sprint-scope` 블록)는 hs 묶음 몫이라 뺀다.
- 사용자 위임: 2026-09-26T10:09:00.557Z 「123다실행해 그러면끝나?다음카이젠에왜넘기는데?」, 결정 답 2026-09-26T10:30:16.222Z, 세션 `bda55d45-296c-491f-89ba-b52042d58e72`. 결정 파일 `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0926b/.harness/.meta/after-kaizen-0926b/decisions.md`. 이 계약의 합의는 그 위임으로 받은 것으로 적는다. 조건을 느슨하게 하는 개정은 이 위임으로 동의 처리하지 않는다.
- 작업 폴더 W = `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak2-cs`, 가지 `chore/ak2-cs`, 기준 판 B = `6378948` (origin/main). 이 가지에는 이 묶음만 커밋한다.
- 설치본 sprint-contract 는 0.14.0 이고 W 의 원본은 harness 0.15.2 다. 절차는 W 의 `harness/skills/sprint-contract/SKILL.md` 를 따랐다 (`measurement_digest` 가 있는 판).
- 계약 형식 문서 `harness/references/contract-schema.md` 의 판 번호를 v5.7 로 올리고 변경 이력에 v5.7 한 줄을 더한다. 지금 머리(`:6`)는 v5.6 인데 `## 스키마 버전` 절은 `현재: **v5.5**`(`:1301`)이고 변경 이력에 v5.6 줄이 없다 — v5.6 줄도 한 줄 채운다.

## 리서치 소스

- 저장소 안 기록만 쓴다. 바깥 문서가 있어야 판단되는 항목은 없다.
- CS-1: `.harness/.meta/kaizen-0924/phase4-notes.md` 넘김 표 · `phase2-notes.md` §Phase 4 가 읽을 것 · `harness/skills/contract-kaizen/SKILL.md:69`
- CS-2: `phase2-notes.md:116` (개정 번호 · 원 제안은 `.harness/.meta/kaizen-data-pool.md:1446`) · `phase2-notes.md` 측정 묶음 · 넘김 목록 `경로:줄` · `phase7-notes.md` `mktemp` · `phase9-notes.md` 두 판 풀기 공통 정의 · `phase10-notes.md` 검사기가 돈 줄 · `phase4-notes.md` 서명 없는 커밋 두 측정 · `phase3-notes.md` 「바꾸지 않는다」 더한 줄 · 열 번호는 `harness/docs/guides/qa-evaluation-guide.md:1201-1203`
- CS-3: `phase3-notes.md` 넘김 표 · `qa-evaluation-guide.md:1167-1210` (①~⑤)
- CS-4: `.harness/.meta/after-kaizen-0926/` 의 FU-2 (C3a DG-02)
- CS-5: `.harness/.meta/kaizen-0924/f1-harness-followups-notes.md` 구현 중 셋째
- CS-6: `.harness/.meta/after-kaizen-0926/c1b-notes.md:200` (QA-1)
- CS-7: `.harness/.meta/after-kaizen-0926/c3a-notes.md:157`
- CS-8: `.harness/.meta/after-kaizen-0926/c4b-notes.md:112`
- CS-9: `.harness/.meta/after-kaizen-0926/c4a-notes.md:111` (R6)
- CS-10: `.harness/.meta/kaizen-0924/f2-review-fixes-notes.md:80`
- CS-11: `/Users/jackson/Hub/10_Dev/claude-plugins/.harness/sprint-amendments-plugin-validation-page-sync.md` 「다음 스프린트로 남기는 것」 1 · 2 · 3 · 4 · 6 (5 는 GD-1) · 메모리 `project_after_kaizen_0924_pending.md` 5 번

## GAP 분석

### 복잡도 네 축 (SKILL Step 1)

| 축 | 물음 | 값 |
| --- | --- | --- |
| 레이어 수 | 몇 계층을 관통하나 | 문서 규칙 · 셸 도우미 · 피드백 형식 셋 |
| 공개 형식 변경 | 밖에 드러난 형식이 바뀌나 | 예 — 계약 형식 문서 판 번호 · 피드백 체크리스트 키 |
| 소비면 존재 | 받아 쓰는 쪽이 있나 | 예 — sprint-contract SKILL.md · qa-evaluator · 평가 가이드 · 문서 사이트 페이지 |
| 회귀 위험 | 기존 동작이 깨질 길이 있나 | 예 — 기존 도우미 코드 블록 · 봉인 함수가 같은 파일에 있다 |

네 축 중 셋 이상이 「예」 이고 형식 변경과 소비면이 함께 있어 복잡이다. 기능 조건은 24 개로 가이드 상한 20 을 넘는다 — 부모가 정한 한 묶음(CS-1 ~ CS-11, 한 킷 한 커밋)이라 나누지 않았다. 항목 열하나 · 판 번호 · 범위 · 측정 묶음 · 로컬 CI 가 각각 하나씩이다.

### 설정 값 대조 (SKILL Step 1.2)

| 설정 키 | project.yaml 값 | 계약에 쓴 값 |
| --- | --- | --- |
| `commands.analyze` | `bash -n scripts/release.sh` | DG-01 N/A 사유에 그대로 |
| `commands.test` | `bash scripts/release.sh 2>&1 \|\| true` | DG-03 N/A 사유에 그대로 |
| `diagnostics.ide_exclude` | `[]` | DG-02 에 `[]` |
| `contract_categories` | Skill/SK · Script/SC · Error/ER · Architecture/AR | 같은 넷 |
| `anti_patterns` | AP-01 · AP-02 · AP-03 · AP-04 | AP-03 · AP-04 (AP-01 · AP-02 는 문서 변경에 걸릴 모양이 아니다) |

### 고치기 전 확인 (SKILL Step 1.4) — 대상 파일을 B 판에서 직접 읽었다

| 대상 | 읽은 자리 | 지금 상태 | 조건 |
| --- | --- | --- | --- |
| CS-1 `harness/references/feedback-schema.yaml` | `:31-56` 자기진단 절 · `:92` 예시 | 체크리스트 sprint-contract 필수 다섯만. `measure_premise_unrun` · `known_answer_missing` 0 건, true 뜻 문장 0 건. 같은 두 키는 `harness/skills/sprint-contract/SKILL.md:816-817` 과 `contract-design-guide.md:1169-1170` 에는 있다 | SK-01 |
| CS-1 막는 조문 | `harness/skills/harness-kaizen/SKILL.md:46` | 「Phase 2/3 공동, harness-kaizen 수정 금지」 — harness-kaizen 실행에만 걸린다. 이 묶음은 harness-kaizen 이 아니다 | 조건 없음 |
| CS-2 개정 번호 | `contract-schema.md:1263-1275` §엔트리 포맷 | 번호 규칙 0 건 | SK-02 |
| CS-2 측정 관례 | `contract-schema.md` 전체 | `mktemp` · `git archive` · `경로:13:8` · `경로:줄` · `검사 범위` · `더한 줄` 모두 0 건 (`grep -nF` 으로 확인) | SK-03 · SC-01 · SC-02 · ER-01 |
| CS-2 서명 두 측정 | `contract-schema.md:710-743` | `unsigned_on` 은 내 서명이 없는 커밋을 센다. 두 측정의 정의를 맞추라는 문장 0 건 | SK-04 |
| CS-2 봉인 둘째 줄 | `contract-schema.md:360-384` | 처리됨 — PR #114 `measurement_digest` | 조건 없음 |
| CS-3 | `contract-schema.md:935-971` · `qa-evaluation-guide.md:1167-1210` | 계약 측 짝은 ⑤ 만(§알려진 답 대조). ①~④ 0 건 | SK-05 |
| CS-4 | `contract-schema.md:78-113` §셸 이식성 | `LC_ALL=C sort` 는 도우미 안에만(`:111` · `:735` · `:1096`), `comm` 앞 정렬 규칙 문장 0 건 | SK-06 |
| CS-5 | 풀어 둔 사본 실측 | `git archive 6378948` 사본에서 `python3 scripts/validate-doc-contracts.py` → `NOT RUN: git ls-files 실패 (rc=128)` 종료 2. 같은 사본에 `git init -q && git add -A` 뒤 → `doc-contracts: 1 블록 검사 · violation 0` 종료 0 | SK-03 |
| CS-6 | `contract-schema.md` 전체 · 레포 `.md` | 「기존 동작 유지」 패턴 0 건. 「계약 문언 밖」 은 `.harness/sprint-feedback-after-0924-harness-orch.md:144` · `.harness/.meta/hook-verification-autofixer-oracle-guards.md:216` 에 있다 | SK-07 |
| CS-7 | `contract-schema.md:641-672` | 「미커밋 변경 0」 전제 규칙 0 건 | SK-08 · SC-03 · ER-01 |
| CS-8 | `contract-schema.md:853-895` §인자 매트릭스 | FAIL 칸 규칙 0 건 | SK-09 |
| CS-9 | `contract-schema.md:1038-1060` · `SKILL.md:522-557` | `AUTO:` 0 건 (SKILL.md 의 `SLUG_AUTO` 는 다른 말) | SK-10 · SK-11 |
| CS-10 | `contract-schema.md:745-776` | `markdownlint` 0 건 | SK-12 |
| CS-11 | `contract-schema.md` 전체 | `@import` · `plugins` 규칙 0 건 (`:1270` 의 `claude-plugins` 는 경로) | SK-13 |
| 판 번호 | `contract-schema.md:6` · `:1301` · `:1303-1305` | 머리 v5.6 · 절 v5.5 · 이력 첫 줄 v5.5 | AR-03 |
| 소비면 | `qa-evaluation-guide.md:1210` · `SKILL.md:471` · `docs/harness/contract-schema.html` | 이 묶음 범위 밖 — 넘김 기록 | AR-04 |
| 판 번호를 옮겨 적은 자리 | `contract-design-guide.md:1311` (버전 정보 표 `v5.5`) · `docs/index.html:239` (목차 제목 `v5.5`) · `qa-evaluation-guide.md:12` · `:15` · `:22` · `:1968` · `:2038` · `:2047` (`v5.5`) | 지금도 v5.6 을 못 따라갔다. 이 묶음 범위 밖 — 넘김 기록 (교차 진단이 찾았다) | AR-04 |

도우미 이름 열셋(`resolve_contract_root` · `list_contracts` · `fm_get` · `sha256_16` · `contract_digest` · `verify_seal` · `measurement_digest` · `verify_measurement` · `sprint_head` · `mine` · `unsigned_on` · `amend_direction` · `amend_direction_oracle`)은 B 판에서 정의가 각각 1 번이다. 새 이름 셋(`with_two` · `line_of` · `dirty_except_status`)은 0 번이다.

### 항목별 배치

| ID | 둘 자리 (계약 형식 문서 제목 줄) | 조건 |
| --- | --- | --- |
| CS-1 | `feedback-schema.yaml` 의 `# --- 자기진단` ~ `# --- 사용자 시그널` 사이 | SK-01 |
| CS-2 (가) 개정 번호 | `### 엔트리 포맷` | SK-02 |
| CS-2 (나 · 다 · 라 · 마 · 바 · 사 · 자) + CS-5 | 새 절 `#### 측정 관례 — 두 판 풀기 · 줄 번호 · 넘김 목록 (v5.7 추가)` | SK-03 · SC-01 · SC-02 |
| CS-2 (아) 서명 두 측정 | `##### 여러 주체가 한 가지에 커밋할 때 — …` | SK-04 |
| CS-3 | 새 절 `#### 산출물이 검사인 조건 — 사본 대조 ①~④ 의 계약 측 짝 (v5.7 추가)` | SK-05 |
| CS-4 | ``### 셸 이식성 규약 — 글로빙 대신 `find` (v5.1)`` | SK-06 |
| CS-6 | 새 절 `#### 기존 동작 유지 조건 — 기준 판과 새 판을 여러 입력으로 맞댄다 (v5.7 추가)` | SK-07 |
| CS-7 | ``##### `.harness/` 범위 조건 — …`` | SK-08 · SC-03 |
| CS-8 | `#### 인자 매트릭스 (Factor Matrix · v5.3 추가)` | SK-09 |
| CS-9 | `### 4. Diagnostics (자동 포함)` · SKILL.md `### 4. 자동 포함 섹션` | SK-10 · SK-11 |
| CS-10 | `#### 미실측 오라클 봉인 금지 (v5.4 추가)` | SK-12 |
| CS-11 | 새 절 `#### 페이지 맞추기 계약 — 다섯 가지 (v5.7 추가)` | SK-13 |

새 절 넷은 `#### 알려진 답 대조 …` 절 뒤, `#### 조건 작성 preflight …` 절 앞에 둔다. 제목 줄은 위 글자 그대로 쓴다 — 측정이 제목 줄로 자리를 찾는다.

## 범위 경계

- 고치는 파일은 셋이다: `harness/references/contract-schema.md` · `harness/references/feedback-schema.yaml` · `harness/skills/sprint-contract/SKILL.md`. SKILL.md 는 CS-9 한 줄만, Step 4 절 안에서 더한다. 다른 묶음(gd · pd · hs)이 같은 SKILL.md 의 Step 1 · 6 · 6.7 · 9 와 계약 형식 문서 측정 절을 고칠 수 있어 절 단위로 자리를 잠갔다.
- 문서 사이트 `docs/harness/*.html` 은 부모가 마지막에 다시 만든다. harness `plugin.json` 판 올림 · marketplace · README 도 부모 몫이다.
- 명시적 미완 (소비면 가운데 이번에 안 바꾸는 것) — 넘김 기록 `.harness/.meta/after-kaizen-0926b/cs-notes.md` 에 `경로:줄` 로 적는다: `harness/docs/guides/qa-evaluation-guide.md:1210` 의 「①~④ 의 짝은 다음 사이클 Phase 1 · 2 로 넘긴다」 (계약 측 짝이 생기면 낡는다 · 생성 측 짝 GD-7 과 함께 고친다), `harness/skills/sprint-contract/SKILL.md:471` 조건 패턴 표 (v5.5 다섯 — 새 패턴 둘이 없다. Step 2 는 이 묶음 표에 없는 절이다), `docs/harness/contract-schema.html` (문서 사이트). 판 번호를 옮겨 적은 자리 여덟도 같이 적는다: `harness/docs/guides/contract-design-guide.md:1311` · `docs/index.html:239` · `harness/docs/guides/qa-evaluation-guide.md:12` · `:15` · `:22` · `:1968` · `:2038` · `:2047` — v5.7 로 올리면 갭이 더 벌어진다.
- 교차 진단 반영 (봉인 전, 2026-09-26): SK-01 측정에 `Step 7` 을 더했다 · AR-02 의 제목 수를 실제 값 열넷으로 고쳤다 · AR-04 에 판 번호 자리 여덟을 더했다 · SK-13 에 교훈 다섯과 낱말 여덟의 관계를 적었다. 넷 모두 조건을 좁히는 쪽이다. `m.sh` 가 바뀌어 AR-05 의 `m.sh` 값을 새로 쟀다. SC-01 ~ SC-03 의 `[goal]` 은 그대로 둔다 — 도우미 안쪽 구현은 자유이고 이름은 SK-03 `[exact]` 가 이미 잠근다.
- 기존 편집기 경고: B 판에서 markdownlint-cli2 0.23.2 · MD013 끔 기준 `contract-schema.md` 8 건(`:519` · `:536` · `:537` 표 모양) · `SKILL.md` 9 건(`:104` · `:344` · `:406` · `:412` · `:425` · `:451` · `:628` · `:841` · `:850`). 둘 다 이 묶음 표에 없는 절이고 VS-26 목록에도 없다 — 이번에 더한 줄의 경고만 0 으로 잰다. 넘김 기록에 적어 부모가 배정한다.
- 구현 단계는 `tone-kit:tone-guide` 1 단계를 부른 뒤 편집하고, 완료 전 5 단계 대조를 한다. 새 도우미 코드는 `harness/references/` 라 톤 범위 안이다.
- 커밋: `git add <경로>` 뒤 `git commit -o <경로>`. 한 커밋에 킷 하나(harness 셋은 한 킷). 측정 묶음 다섯 파일(`.harness/.meta/after-0926-contract-schema/`)은 봉인 커밋과 따로 커밋한다.
- 커버리지 해소: AR-01 — 산문 쪽 `.harness/` 는 측정의 `':(exclude).harness'` 가, `chore/ak2-cs` 는 Given 줄의 상한 해석(`m.sh` 의 기본 `U`)이 덮는다. 검출기가 백틱 안 빈칸 없는 토큰만 보고 측정 줄의 따옴표 꼴을 같은 토큰으로 읽지 못해 난 경보다.

## 회귀 게이트

- 기준 실측 (B 판, 2026-09-26 19:4x): `python3 scripts/validate-plugin.py harness` 종료 0 (V1 ~ V10 모두 OK) · `bash harness/evals/kaizen/feedback-system/save-test.sh` 종료 0 (`ALL TESTS PASSED`) · `python3 scripts/validate-doc-contracts.py` 종료 0 · 로컬 CI(`ci-local.sh`) 스물두 단계 `rc=0`, `feedback-agg-test SKIP (yq 없음)` 한 줄.
- 측정 묶음 `.harness/.meta/after-0926-contract-schema/` — `m.sh`(조건별 측정, 해석기 bash 고정, 도우미 실행 칸만 zsh 를 따로 부른다) · `hunks.py`(더한 줄 · 지운 줄을 제목별로 가른다, 코드 울타리 안 `#` 줄은 제목이 아니다) · `plain.py`(쉬운 말 목록 낱말 세기) · `plain-korean.snapshot.md`(`~/.claude/rules/plain-korean.md` 2026-09-26 사본) · `ci-local.sh`(`/Users/jackson/Hub/10_Dev/claude-plugins/.harness/handoff/2026-09-26-tools/ci-local.sh` 사본).
- 준비 단계 실측: `command -v zsh` → `/bin/zsh` 계열 (zsh 5.9) · `python3 -c 'import yaml'` → PyYAML 6.0.3 · markdownlint-cli2 는 PATH 에 없다(`command -v` 종료 1) — 스크래치에 `npm install --no-save markdownlint-cli2@0.23.2` 뒤 `--help` 첫 줄 `markdownlint-cli2 v0.23.2 (markdownlint v0.41.1)`. 이 기계의 `bash` 안 `grep` 은 `/usr/bin/grep` (BSD 2.6.0) 이라 `m.sh` 는 `grep -P` 를 쓰지 않는다.
- 알려진 답 (봉인 전 실측): `hunks.py owners` — 제목 `# A` · 3 백틱 울타리 안 `# not heading` · `### B` · 4 백틱 울타리 안 3 백틱과 `## still code` 가 든 16 줄 입력에서 1 줄 `(없음)`, 2~8 줄 `# A`, 9~16 줄 `### B` (기대와 같음 · 종료 0). `hunks.py removed/added` — `a / -- dash / b` → `a / b / --- new / c` 에서 지운 줄 `2 -- dash`, 더한 줄 `3 --- new` · `4 c` (종료 0). `plain.py` — 두 줄 입력(`rest api interest 스키마` 와, 그 낱말을 백틱으로 감싼 줄 + `forest`)에서 `hits=3` (첫 줄의 세 낱말만 걸리고 `interest` · `forest` · 백틱 안은 안 걸림).
- 양성 대조 · 음성 대조 (봉인 전 실측, 스크래치 복제본에 흉내 구현을 커밋해 돌렸다): 흉내 구현 판에서 `bash m.sh all` 28 줄 모두 PASS · 종료 0. 같은 명령을 `U=6378948`(변경 없음)로 돌리면 SK-01 ~ SK-13 · SC-01 ~ SC-03 · ER-01 · AR-01 ~ AR-04 · RE-02 가 FAIL. 변경 없이도 통과하는 여섯은 변이 사본으로 FAIL 을 확인했다 — SK-14(더한 줄에 `스키마` · `hits=1`) · RE-01(SKILL.md 에 함수 정의 한 줄) · AP-03 · DG-02(언어 표시 없는 울타리 · `new_warn=1`) · AP-04(`name:` 줄 삭제) · DG-01·03·04(`scripts/release.sh` 한 줄). 그 밖 변이: 허용 밖 절에 한 줄 → AR-02 FAIL, 기존 줄 한 줄 삭제 → AR-02 FAIL(지운 줄 3), `line_of` 를 옛 탐욕 식 `s#^[^ ]*:([0-9]+).*#\1#p` 로 → SC-02 FAIL(`8 104`), `with_two` 에서 `rm -rf` 삭제 → SC-01 FAIL, `dirty_except_status` 에서 status 줄 빼기 삭제 → SC-03 FAIL(`k2=2`), 파일 확인 삭제 → ER-01 FAIL(`des_rc=0 des_out=[0]`), 판 확인 삭제 → ER-01 FAIL(`bad_rc=0 ran=yes`). 변이마다 `git diff --stat` 으로 실제로 들어갔는지 먼저 봤다 (탐욕 식 변이는 첫 시도에 안 들어가 다시 넣었다).
- 공통 전제 (모든 조건): Given 이 스프린트의 커밋이 끝난 뒤. R = W, B = `6378948`, U = `git -C "$R" rev-parse --verify -q chore/ak2-cs` (해석 실패면 `m.sh` 가 종료 2 로 멈춘다 — `HEAD` 로 떨어지지 않는다). `m.sh` 는 `git show "$U:<경로>"` 로 상한 판을 읽는다. 측정 명령은 R 에서 `TMPDIR=<빈 임시 폴더>` 로 부른다.

## Skill

- [ ] SK-01: 피드백 형식 파일의 자기진단 절에 체크리스트 true 가 「문제가 있다」 는 뜻이라는 문장과 새 키 둘 `measure_premise_unrun` · `known_answer_missing` 이 들어가고, 전체 목록 자리로 sprint-contract SKILL.md Step 7 을 가리킨다 [exact, enumerated]
      측정: `bash .harness/.meta/after-0926-contract-schema/m.sh SK-01` 이 `PASS SK-01` — `# --- 자기진단` 줄과 `# --- 사용자 시그널` 줄 사이에 더한 줄에서 `measure_premise_unrun: bool` · `known_answer_missing: bool` · `문제가 있다` · `sprint-contract/SKILL.md` · `Step 7` 다섯이 각각 1 번 이상
      양성 대조: `U=6378948` 로 돌리면 FAIL (다섯 낱말 모두 빠짐, 봉인 전 실측)
      음성 대조: 흉내 구현에서 `Step 7` 만 지운 변이가 `빠진 낱말: [Step 7]` 로 FAIL (봉인 전 실측)
- [ ] SK-02: 개정 파일 엔트리 포맷 절에 개정 번호를 파일 안에서 이어 붙이고 같은 번호를 다시 쓰지 않는다는 규칙이 들어간다 [exact]
      측정: `m.sh SK-02` 가 PASS — `### 엔트리 포맷` 몫의 더한 줄에 `같은 번호를 두 번 쓰지 않는다` 가 1 번 이상
      양성 대조: `U=6378948` 로 FAIL (봉인 전 실측)
- [ ] SK-03: 새 절 「측정 관례」 가 두 판 풀기 도우미 `with_two` (폴더는 `mktemp -d "${TMPDIR:-/tmp}/…"`, 실패하면 멈추고 끝나면 지움) · 줄 번호 도우미 `line_of` (`경로:13:8` 에서 열 번호를 줄 번호로 읽지 않음) · 넘김 목록은 `경로:줄` 로 쪼개 재기 · 측정 묶음을 QA 에 같이 넘기기 · 검사기가 돌았다는 줄 함께 세기 · 「바꾸지 않는다」 구간은 더한 줄의 자리와 수까지 잠그기 · 풀어 둔 판에서 `validate-doc-contracts.py` 는 `git init` · `git add -A` 한 사본에서 돌리기를 담는다 [exact, enumerated]
      측정: `m.sh SK-03` 이 PASS — 제목 줄 `#### 측정 관례 — 두 판 풀기 · 줄 번호 · 넘김 목록 (v5.7 추가)` 몫의 더한 줄에서 글자 열셋 `` `경로:13:8` `` · `` `경로:줄` `` · `측정 묶음을 QA 에 같이 넘긴다` · `mktemp -d "${TMPDIR:-/tmp}/` · `검사기가 돌았다는 줄` · `더한 줄의 자리와 수` · `git diff -U0` · `validate-doc-contracts.py` · `git init` · `git add -A` · `NOT RUN` · `with_two` · `line_of` 가 각각 1 번 이상
      양성 대조: `U=6378948` 로 FAIL (열셋 모두 빠짐, 봉인 전 실측)
- [ ] SK-04: 서명 줄 절에 한 계약 안에서 서명으로 커밋을 가르는 측정은 모두 같은 정의를 쓰고 기본은 `unsigned_on` 이라는 규칙이 들어간다 [exact]
      측정: `m.sh SK-04` 가 PASS — `##### 여러 주체가 한 가지에 커밋할 때 — 서명 줄로 내 커밋을 가린다 (2026-09-24 추가)` 몫의 더한 줄에 `unsigned_on` · `같은 정의` 가 각각 1 번 이상
      양성 대조: `U=6378948` 로 FAIL (봉인 전 실측)
- [ ] SK-05: 새 절 「산출물이 검사인 조건」 이 평가 가이드 ①~④ 각각에 대해 계약이 조건에 적을 사본 대조(① 첫 칸 밖 위반 · ② 실행 목록에 든 것 · ③ 못 읽는 칸을 섞은 사본 · ④ zsh · bash 두 셸의 대상 수)를 담고 `qa-evaluation-guide.md` 를 가리킨다 [exact, enumerated]
      측정: `m.sh SK-05` 가 PASS — 제목 줄 `#### 산출물이 검사인 조건 — 사본 대조 ①~④ 의 계약 측 짝 (v5.7 추가)` 몫의 더한 줄에 `①` · `②` · `③` · `④` · `qa-evaluation-guide.md` · `첫 칸` · `실행 목록` · `못 읽는 칸` · `zsh` · `bash` 가 각각 1 번 이상
      양성 대조: `U=6378948` 로 FAIL (봉인 전 실측)
- [ ] SK-06: 셸 이식성 절에 `comm` 앞 정렬은 `LC_ALL=C sort` 로 하고 `sort -n` 을 쓰지 않는다는 규칙이 들어간다 [exact]
      측정: `m.sh SK-06` 이 PASS — ``### 셸 이식성 규약 — 글로빙 대신 `find` (v5.1)`` 몫의 더한 줄에 `comm` · `LC_ALL=C sort` · `sort -n` 이 각각 1 번 이상
      양성 대조: `U=6378948` 로 FAIL (봉인 전 실측)
- [ ] SK-07: 새 절 「기존 동작 유지 조건」 이 목표 문장을 하위 문장으로 나눠 따로 재기 · 무작위 입력 3 개 이상과 시드 기록을 최소 요건으로 두기 · 「계약 문언 밖」 대신 「조건 문장 안, 측정 밖」 이라 부르기를 담는다 [exact, enumerated]
      측정: `m.sh SK-07` 이 PASS — 제목 줄 `#### 기존 동작 유지 조건 — 기준 판과 새 판을 여러 입력으로 맞댄다 (v5.7 추가)` 몫의 더한 줄에 `목표 문장` · `하위 문장` · `무작위` · `시드` · `3 개 이상` · `조건 문장 안, 측정 밖` · `계약 문언 밖` 이 각각 1 번 이상
      양성 대조: `U=6378948` 로 FAIL (봉인 전 실측)
- [ ] SK-08: `.harness/` 범위 조건 절에 「미커밋 변경 0」 전제는 QA 가 바꾸는 계약 자신의 status 줄을 빼고 잰다는 규칙과 그 수를 내는 도우미 `dirty_except_status` 가 들어간다 [exact]
      측정: `m.sh SK-08` 이 PASS — ``##### `.harness/` 범위 조건 — 산출물 슬러그를 열거하지 마라 (2026-09-23 추가)`` 몫의 더한 줄에 `dirty_except_status` · `QA 가 바꾸는` 이 각각 1 번 이상
      양성 대조: `U=6378948` 로 FAIL (봉인 전 실측)
- [ ] SK-09: 인자 매트릭스 절에 판정 규칙을 바꾸는 계약의 대응표에는 FAIL 이 하나 이상인 칸을 넣는다는 규칙이 들어간다 [exact]
      측정: `m.sh SK-09` 가 PASS — `#### 인자 매트릭스 (Factor Matrix · v5.3 추가)` 몫의 더한 줄에 `판정 규칙` · `FAIL 이 하나 이상인 칸` 이 각각 1 번 이상
      양성 대조: `U=6378948` 로 FAIL (봉인 전 실측)
- [ ] SK-10: 계약 형식 문서의 Diagnostics 절(규칙을 정하는 쪽)에 편집기 경고 조건은 `<!-- AUTO:* -->` 블록 안 · 밖을 나눠 잰다는 규칙이 들어간다 [exact]
      측정: `m.sh SK-10` 이 PASS — `### 4. Diagnostics (자동 포함)` 몫의 더한 줄에 `<!-- AUTO:` · `블록 안` · `블록 밖` 이 각각 1 번 이상
      양성 대조: `U=6378948` 로 FAIL (봉인 전 실측)
- [ ] SK-11: sprint-contract SKILL.md Step 4 (규칙을 받아 쓰는 쪽)에 같은 규칙 한 줄이 들어가고 계약 형식 문서를 가리킨다 [exact]
      측정: `m.sh SK-11` 이 PASS — SKILL.md `### 4. 자동 포함 섹션` 몫의 더한 줄에 `<!-- AUTO:` · `블록 안` · `블록 밖` · `contract-schema.md` 가 각각 1 번 이상
      양성 대조: `U=6378948` 로 FAIL (봉인 전 실측)
- [ ] SK-12: 미실측 값 봉인 금지 절에 측정 도구(markdownlint-cli2 등)의 판과 설치 명령을 준비 단계에 적는다는 규칙이 들어간다 [exact]
      측정: `m.sh SK-12` 가 PASS — `#### 미실측 오라클 봉인 금지 (v5.4 추가)` 몫의 더한 줄에 `markdownlint-cli2@` · `설치 명령` 이 각각 1 번 이상
      양성 대조: `U=6378948` 로 FAIL (봉인 전 실측)
- [ ] SK-13: 새 절 「페이지 맞추기 계약」 이 다섯 가지(교훈 다섯을 아래 측정의 낱말 여덟로 잰다 — `N plugins` 같은 영어 꼴과 쉼표 나열까지 세기 · 작은따옴표 · `@import` · `//` 주소까지 보기 · 도구가 죽어도 0 줄 통과를 막는 종료 코드 · 상세 줄 모양 · 0 기대 조건의 양성 대조)를 담는다 [exact, enumerated]
      측정: `m.sh SK-13` 이 PASS — 제목 줄 `#### 페이지 맞추기 계약 — 다섯 가지 (v5.7 추가)` 몫의 더한 줄에 `plugins` · `쉼표` · `작은따옴표` · `@import` · `//` · `종료 코드` · `상세 줄` · `양성 대조` 가 각각 1 번 이상
      양성 대조: `U=6378948` 로 FAIL (봉인 전 실측)
- [ ] SK-14: 세 파일에 더한 줄(백틱 안 제외)에 쉬운 말 목록의 검사 켜진 낱말이 0 번 나온다 [exact]
      측정: `m.sh SK-14` 가 `PASS SK-14 hits=0 words=69` — `plain.py` 가 `plain-korean.snapshot.md` 의 `## 바꿔 쓸 말` 표에서 3 열 `on` 인 낱말 69 개를 읽는다
      양성 대조: B 판 계약 형식 문서 전체를 넣으면 `hits=137` · 더한 줄에 `스키마` 한 낱말을 넣은 변이는 `hits=1` 로 FAIL (둘 다 봉인 전 실측)

## Script

- [ ] SC-01: `with_two <저장소> <판1> <판2> <명령> [인자...]` 가 두 판을 풀어 명령에 두 폴더를 넘기고, 명령의 종료 코드를 그대로 돌려주고, 폴더를 `$TMPDIR` 아래 만들고, 끝나면 지운다 — bash · zsh 에서 같다 [goal]
      측정: `m.sh SC-01` 이 PASS — 새 절 「측정 관례」 의 코드 울타리에서 `with_two` 정의 블록을 떼어 bash · zsh 각각에서 판 둘(`f.txt` 가 `one` · `two`)짜리 임시 저장소로 돌린다. 두 셸 모두 `one` · `two` 각 1 줄, `cmd_rc=0`, 명령 `false` 로 `false_rc=1`, 첫 폴더가 `$TMPDIR/` 아래, 끝난 뒤 `$TMPDIR` 안 남은 항목 `left=0`
      알려진 답: 흉내 구현에서 위 값 그대로 · 종료 0 (봉인 전 실측)
      음성 대조: `with_two` 에서 `rm -rf` 를 빼면 `left=0` 이 깨져 FAIL (봉인 전 실측)
- [ ] SC-02: `line_of` 가 stdin 경고 줄 `경로:줄[:열] …` 에서 줄 번호만 한 줄에 하나씩 낸다 — 열 번호를 줄 번호로 읽지 않고, 경로에 빈칸이 있어도 된다 [goal]
      측정: `m.sh SC-02` 가 PASS — 블록을 떼어 bash · zsh 에서 `a/b.md:13:8 error MD060 x` · `c.md:104 error MD032 y` · `d/e f.md:7:1 warn z` 세 줄을 넣으면 두 셸 모두 `13 104 7`
      알려진 답: 기대 `13 104 7` · 흉내 구현 실제 `13 104 7` · 종료 0 (봉인 전 실측)
      음성 대조: 옛 탐욕 식 `s#^[^ ]*:([0-9]+).*#\1#p` 로 바꾸면 `8 104` 로 FAIL (봉인 전 실측)
- [ ] SC-03: `dirty_except_status <계약파일>` 이 (계약 밖 `git status --porcelain --untracked-files=all` 줄 수) + (계약 파일 미커밋 차이에서 `status:` 줄이 아닌 `+` · `-` 줄 수)를 낸다 [goal]
      측정: `m.sh SC-03` 이 PASS — 블록을 떼어 bash · zsh 에서 임시 저장소(커밋된 `c.md` 에 `status: active` 와 조건 한 줄, `o.txt`)로 다섯 경우를 잰다: 깨끗함 `k1=0` · status 줄만 바꿈 `k2=0` · status 줄과 조건 줄을 바꿈 `k3=2` · `o.txt` 만 바꿈 `k4=1` · 추적 안 된 새 파일 `k5=1`
      알려진 답: 기대 0 · 0 · 2 · 1 · 1, 흉내 구현 실제 같음 · 종료 0 (봉인 전 실측)
      음성 대조: status 줄 빼기를 없애면 `k2=2` 로 FAIL (봉인 전 실측)

## Error

- [ ] ER-01: 두 도우미가 실패를 성공처럼 삼키지 않는다 — `with_two` 는 없는 판을 받으면 종료 코드가 0 이 아니고 명령을 부르지 않고 임시 폴더를 남기지 않으며, `dirty_except_status` 는 없는 파일을 받으면 종료 코드가 0 이 아니고 표준 출력이 비어 있다 — bash · zsh 에서 같다 [goal]
      측정: `m.sh ER-01` 이 PASS — 두 셸 모두 `bad_rc` 가 0 아님 · `ran=no` · `left=0` · `des_rc` 가 0 아님 · `des_out=[]`
      음성 대조: 파일 확인을 빼면 `des_rc=0 des_out=[0]`, 판 확인을 빼면 `bad_rc=0 ran=yes` 로 각각 FAIL (봉인 전 실측)

## Architecture

- [ ] AR-01: `.harness/` 밖 바뀐 경로가 정확히 세 개다 [exact, enumerated]
      Given: 이 스프린트의 커밋이 끝난 뒤 · 상한 U = 가지 `chore/ak2-cs` 끝 (`git rev-parse --verify -q chore/ak2-cs`, 실패면 멈춤)
      측정: `m.sh AR-01` 이 PASS — `git diff --name-only 6378948 "$U" -- . ':(exclude).harness'` 를 `LC_ALL=C sort` 한 결과가 `harness/references/contract-schema.md` · `harness/references/feedback-schema.yaml` · `harness/skills/sprint-contract/SKILL.md` 세 줄과 정확히 같다 (생성물 없음 — 세 파일 모두 손으로 쓴 문서)
      기준 실측: 봉인 전 `U=6378948` 이면 빈 출력이라 FAIL
- [ ] AR-02: 편집 자리가 묶음 표의 절로 한정되고 기존 줄은 판 번호 두 줄 말고 지워지지 않는다 [exact, enumerated]
      측정: `m.sh AR-02` 가 PASS — (1) 계약 형식 문서에서 지운 줄은 정확히 2 줄이고 하나는 `> **최근 갱신:` 으로, 하나는 `현재: **v5.5**` 로 시작한다 (2) 계약 형식 문서에 더한 줄의 몫 제목(`hunks.py outside`, 코드 울타리 안 `#` 줄은 제목 아님)이 모두 아래 열넷 가운데 하나다: `# Sprint Contract 스키마`(머리) · 셸 이식성 · `.harness/` 범위 조건 · 여러 주체 · 미실측 값 봉인 금지 · 인자 매트릭스 · 알려진 답 대조 · 새 절 넷 · `### 4. Diagnostics (자동 포함)` · `### 엔트리 포맷` · `## 스키마 버전` (제목 줄 글자는 `m.sh` 의 `H_TOP` ~ `H_VER` 열넷 값. `H_S4` 는 SKILL.md 몫이라 여기 들지 않는다) (3) 피드백 형식 파일은 지운 줄 0 이고 더한 줄 모두 자기진단 절 안 (4) SKILL.md 는 지운 줄 0 이고 더한 줄 모두 `### 4. 자동 포함 섹션` 몫
      음성 대조: `## 허용 섹션 헤더` 아래 한 줄을 더한 변이 · `- 선례:` 한 줄을 지운 변이가 각각 FAIL (봉인 전 실측)
- [ ] AR-03: 계약 형식 문서 판 번호가 v5.7 이다 — 머리 첫 줄 · 이전 줄 v5.6 · 「현재」 줄 · 변경 이력 첫 항목 v5.7 · 변경 이력에 v5.6 항목 한 줄 [exact, enumerated]
      측정: `m.sh AR-03` 이 PASS — 상한 판 첫 10 줄에 `> **최근 갱신: 2026-..-.. (v5.7)**` · 첫 12 줄에 `> 이전: 2026-09-26 (v5.6)` · `현재:` 로 시작하는 줄이 정확히 1 줄이고 `현재: **v5.7** (2026-..-..)` · `변경 이력:` 뒤 첫 `- **` 항목이 `- **v5.7 (2026-` · `- **v5.7 (2026-` 줄 1 개 · `- **v5.6 (2026-09-26)**` 줄 1 개
      양성 대조: `U=6378948` 로 여섯 항목 모두 FAIL (봉인 전 실측)
- [ ] AR-04: 넘김 기록 `.harness/.meta/after-kaizen-0926b/cs-notes.md` 가 상한 판에 있고 명시적 미완(소비면 셋과 스키마 판 번호를 옮겨 적은 자리 여덟)을 `경로:줄` 로, 항목 CS-1 ~ CS-11 처리 상태와 CS-12 제외를 적는다 [exact, enumerated]
      측정: `m.sh AR-04` 가 PASS — `git show "$U:.harness/.meta/after-kaizen-0926b/cs-notes.md"` 에 `harness/docs/guides/qa-evaluation-guide.md:1210` · `harness/skills/sprint-contract/SKILL.md:471` · `docs/harness/contract-schema.html` · `CS-12` · `harness/docs/guides/contract-design-guide.md:1311` · `docs/index.html:239` · `harness/docs/guides/qa-evaluation-guide.md:12` · `harness/docs/guides/qa-evaluation-guide.md:15` · `harness/docs/guides/qa-evaluation-guide.md:22` · `harness/docs/guides/qa-evaluation-guide.md:1968` · `harness/docs/guides/qa-evaluation-guide.md:2038` · `harness/docs/guides/qa-evaluation-guide.md:2047` 가 각각 1 번 이상(줄 번호 뒤에 숫자가 이어지지 않는 꼴 — `:12` 가 `:1210` 으로 채워지지 않는다), `CS-1` ~ `CS-11` 이 뒤에 숫자가 붙지 않은 꼴로 각각 1 번 이상
      양성 대조: `U=6378948` 로 FAIL (파일 없음, 봉인 전 실측). 흉내 구현의 넘김 기록에서 `:12` 를 `:129` 로 바꾼 변이도 `빠짐: [harness/docs/guides/qa-evaluation-guide.md:12]` 로 FAIL (봉인 전 실측)
- [ ] AR-05: 측정 묶음 다섯 파일이 상한 판에 커밋돼 있고 sha256 앞 16 자리가 봉인 전 값과 같다 [exact, enumerated]
      측정: 파일마다 `git show "$U:.harness/.meta/after-0926-contract-schema/<파일>" | shasum -a 256 | cut -c1-16` 이 `m.sh` = `160e1a01e0b9abc3` · `hunks.py` = `f752bc96de973949` · `plain.py` = `1895ef36f037a105` · `plain-korean.snapshot.md` = `694f07858cf9016c` · `ci-local.sh` = `59fe55125c0dbc77`
- [ ] AR-06: 로컬 CI 가 기준과 같은 상태로 끝난다 [exact]
      Given: 작업 폴더 W 의 `HEAD` 가 상한 U 와 같고 `git status --porcelain -- . ':(exclude).harness'` 가 빈 출력
      측정: `TMPDIR=$(mktemp -d "${TMPDIR:-/tmp}/ci.XXXXXX") bash .harness/.meta/after-0926-contract-schema/ci-local.sh "$PWD"` 의 요약 파일 `$TMPDIR/ci-local/summary.txt` 에서 `rc=0` 줄이 22 줄이고, `rc=0` 이 아닌 줄은 `feedback-agg-test SKIP (yq 없음)` 한 줄뿐 (yq 가 설치돼 있으면 그 줄이 `feedback-agg-test rc=0` 이고 `rc=0` 이 23 줄)
      기준 실측: B 판에서 22 · SKIP 1 (봉인 전)
      음성 대조: SKILL.md `name:` 줄을 지운 변이에서 `python3 scripts/validate-plugin.py harness` 가 `V1 … 1 failed — FAIL` · `Total: 1 plugins, 1 ERROR` 라 첫 단계가 떨어진다 (봉인 전 실측)

## Anti-patterns

- [ ] AP-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수
      측정: `m.sh AP-03` 이 PASS — 계약 형식 문서 · SKILL.md 상한 판에서 더한 줄에 있는 여는 울타리 가운데 언어 표시 없는 것 0 개
      양성 대조: 언어 표시 없는 울타리를 더한 변이에서 `AP-03 1 곳` FAIL (봉인 전 실측)
- [ ] AP-04: SKILL.md / agents/*.md frontmatter 에서 name 필드 누락 금지
      측정: `m.sh AP-04` 가 PASS — SKILL.md 상한 판 frontmatter 의 `name:` 줄이 정확히 1 개. AR-06 의 `validate-plugin` 단계가 V1 을 함께 잰다
      양성 대조: `name:` 줄을 지운 변이에서 FAIL (봉인 전 실측)

## Reusability

- [ ] RE-01: 새 셸 도우미 정의는 공용 자리인 계약 형식 문서에만 두고 SKILL.md · 피드백 형식 파일에는 두지 않는다
      측정: `m.sh RE-01` 이 PASS — SKILL.md · 피드백 형식 파일에 더한 줄 가운데 `이름() {` 꼴 함수 정의 0 줄
      양성 대조: SKILL.md 에 `foo() { :; }` 한 줄을 더한 변이에서 FAIL (봉인 전 실측)
- [ ] RE-02: 기존 도우미를 다시 정의하지 않고 새 도우미도 한 번씩만 정의한다
      측정: `m.sh RE-02` 가 PASS — 상한 판 계약 형식 문서에서 기존 열셋(`resolve_contract_root` · `list_contracts` · `fm_get` · `sha256_16` · `contract_digest` · `verify_seal` · `measurement_digest` · `verify_measurement` · `sprint_head` · `mine` · `unsigned_on` · `amend_direction` · `amend_direction_oracle`)과 새 셋(`with_two` · `line_of` · `dirty_except_status`)의 정의 줄이 각각 정확히 1 번
      기준 실측: B 판은 기존 열셋 각 1 · 새 셋 각 0

## Diagnostics

- [ ] DG-01: N/A (commands.analyze `bash -n scripts/release.sh` 가 재는 `scripts/release.sh` 가 이번 변경 파일에 없다)
      측정: `m.sh DG_NA` 가 PASS — `git diff --name-only 6378948 "$U" | grep -c '^scripts/release.sh$'` 가 0
- [ ] DG-02: IDE diagnostics 워닝/인포 0개 ([] 제외) — 두 마크다운 파일의 더한 줄에 걸린 markdownlint 경고 0 개 · 피드백 형식 파일 YAML 읽기 성공
      측정: `ML=<markdownlint-cli2 0.23.2 실행 파일> m.sh DG-02` 가 PASS — 준비: 빈 폴더에서 `npm install --no-save markdownlint-cli2@0.23.2`, 설정 `{ "config": { "MD013": false } }` (편집기 확장과 같은 값). 두 파일 모두 `Linting: 1 file` 줄이 나오고(검사기가 돌았다는 줄) 종료 코드 0 또는 1, 경고 줄 번호 가운데 더한 줄 번호와 겹치는 것 0 개. `yaml.safe_load` 뒤 `example.schema_version == 1`
      양성 대조: 언어 표시 없는 울타리를 더한 변이에서 `new_warn=1` 로 FAIL (봉인 전 실측)
- [ ] DG-03: N/A (commands.test `bash scripts/release.sh 2>&1 || true` 도 같은 파일만 부른다 — 변경 파일과 겹침 0)
      측정: DG-01 과 같은 `m.sh DG_NA`
- [ ] DG-04: N/A (산출물이 마크다운 · YAML 문서뿐이라 구동할 앱 · 서버가 없다)
      측정: `m.sh DG_NA` 가 PASS — `.harness/` 밖 바뀐 파일 가운데 `.md` · `.yaml` 이 아닌 것 0 개
