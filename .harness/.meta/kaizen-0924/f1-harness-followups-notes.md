# 카이젠 2026-09-24 Final — kaizen-0924-f1-harness-followups notes

- 계약: `.harness/sprint-contract-kaizen-0924-f1-harness-followups.md` (조건 30 · 기능 조건 20, 봉인 `sha256:a37827c20fae4fbe` · `locked_at` 2026-09-25 16:40)
- 개정: `.harness/sprint-amendments-kaizen-0924-f1-harness-followups.md` (조건 변경 0 건. 구현이 개선안과 다른 곳 셋 · DG-05 (b) 측정 전제 한 건 — 모두 `amend_direction: unchanged`)
- 검토: `.harness/.meta/kaizen-0924/f1-harness-followups-review.md` — 1 회차 `VERDICT: CHANGES`(고칠 것 C1 ~ C10 · 권고 R1 ~ R7)는 DRAFT 가 반영했다.
  2 회차 `VERDICT: CHANGES`(고칠 것 C11 · C12 · 권고 R8)는 BUILD 가 봉인 전에 넣었다 — 새 실측이 필요 없는 문구 고침이라 3 회차는 돌리지 않았다
- Codex 독립 검토 r1(`scratchpad/kaizen/codex/r1-harness.md`, 7 건): 다섯은 조건(ER-01 · SK-05 (마)(바)(사)(아) · ER-06 (d)), 하나는 ER-01 과 같은 결함, 하나(r1 2 `assertions.json` 실행기)는 고치지 않음 — 계약 입력 표 F1H-83 ~ F1H-89
- 사용자 승인 대체: 사용자 위임(세션 기록 queued_command `2026-09-24T04:04:16.964Z`) · Codex 한도 소진(2026-09-24) · 「코덱스 대신에 그냥 너가 알아서 진행하라고」(user `2026-09-24T11:54:58.940Z`) ·
  「코덱스도 사용할 수 있으니깐 사용해」(user `2026-09-25T06:19:45.056Z`) — REVIEW 에이전트 검토와 Codex 검토로 대신했다
- 시작 커밋 `5b4fd72d5587c937c1875ddb62872f32ae087dcf`
- 계약 피드백: `~/.harness/feedback/contract/1a3bcba6-2026-09-25T170814-de8c7935-77695.yaml` (`verify-feedback.sh` PASS). 초안은 스크래치 `kaizen/f1h-build/feedback-draft.yaml`,
  `HARNESS_CONTRACT_ROOT` · `HARNESS_CONTRACT` 를 명시해 이 가지의 새 `save-feedback.sh` 로 저장했다 — 저장본 `project_name` 이 `claude-plugins` 로 나왔다(ER-02 가 실제로 도는 것을 확인. 같은 워크트리의 Phase 17 저장본은 `kaizen-0924`)

## 커밋

| 커밋 | 내용 | 파일 |
| --- | --- | --- |
| `5cb9eb0` | 봉인 커밋 | 계약 1 개 |
| `bfadfbb` | 커밋 안전 훅 이름 바꾸기 · 피드백 저장본 이름 (ER-01 · ER-02) | `harness/` 스크립트 · 시험 넷 |
| `e4692cb` | 평가자 · 평가 가이드 · 스키마 · 설계 가이드 · 계약 가이드 · 검증 가이드 · README · 하네스 스킬 둘 (SK-05 · ER-01 (e) · ER-03 ~ ER-06 · ER-08 (c)) | `harness/` 문서 열 |
| `3e874e8` | 옛 값 검사 범위 · V 줄 판정 · bare-fence 종료 코드 · 드리프트 매핑 (ER-07 · ER-08 · AR-01 (a)) | `scripts/` 넷 |
| `66b4e4c` | 오케스트레이터 Phase 17 · F2 매핑 표 · AUTO 범위 줄 (SK-01 · AR-01 (b) · AR-03) | 오케스트레이터 SKILL.md · `scripts/sync-orchestrator.py` |
| `306948c` | 참조 문서 둘 · 카이젠 스킬 여덟 (SK-02 ~ SK-04) | `.claude/skills/` 열 |
| `d97944c` | CI zsh 설치 · 새 시험 여섯 (AR-02) | `.github/workflows/ci.yml` |
| `927434b` | 개정 파일에 `end_sha` (`d97944c`) | 개정 1 개 |
| 이 파일의 커밋 | notes · 검토 기록 · 개정 파일에 DG-05 (b) 측정 전제 한 줄 | `.harness/` 셋 |
| 그다음 커밋 | 개정 파일에 notes 커밋 sha 로 `end_sha` 한 줄 더 | 개정 1 개 |

모든 커밋 메시지 끝 문단에 `Kaizen-Phase: kaizen-0924-f1-harness-followups` 줄이 있다. 구현 커밋은 `git add -- <경로…> && git commit -o -F <메시지> -- <경로…>` 로 내 경로만 실었다.
`harness/` 와 `scripts/` · `.claude/skills/` · `.github/` 는 커밋을 나눴고, AR-03 대로 `scripts/sync-orchestrator.py` 와 다시 만든 오케스트레이터 SKILL.md 는 한 커밋이다.
**FIX 가 커밋을 더할 때도 서명 줄을 넣고, 개정 파일에 `end_sha:` 줄을 덧붙인다.**

30 조건 측정은 봉인 판 계약에서 뗀 도우미(스크래치 `kaizen/f1h-build/K/`, 계약에 적힌 떼는 명령 그대로)와 공통 정의 `common.sh` 로, 상한 `d97944c` 에서 돌렸다
(`kaizen/f1h-build/run1.sh` · `run2.sh` · `run3.sh`). 조건 줄 기대값과 모두 같았다 — 요지:

- 문서 글자: `toks.py` 접두 열둘 전부 `ng=0` (SK01 30 · SK02 16 · SK03 8 · SK04 6 · SK05 34 · ER01 · ER03 · ER04 · ER05 · ER06 · ER07 · AR03). `orch.sh` `diagram=1 depdoc=1 concur=1 signline=1 auto_removed=3 auto_added=3` 과 기대 세 줄.
  `upref.sh` `upper=5/5` · 배치 우선순위 `1(최고),2,3,4,5(최저),` · 첫 행 managed settings 1 · 템플릿 6 · rust 새 꼴 종료 코드 1 · 옛 계약 경로 파일 0
- ER-01: `ren2.sh` 다섯 줄 `agree`(N1 · N2 · N5 `hook_rc=0`), `align.sh` 열한 줄 `agree` · `60 51 50 0 0 55 59 60 0 0 0`, 훅 시험 bash · `/bin/bash` 둘 다 `실패 0 건` · ㉖ ~ ㉚ 각 1, 시작 판 훅으로 돌린 음성 대조의 FAIL 번호 정확히 `㉖ ㉗ ㉘`
- ER-02: `ident.sh` 둘째 줄 `wt-x project_name=projmain hash_is_main=1 verify_rc=0`, 저장 시험 종료 코드 0 · 워크트리 PASS 1 · 임시 HOME 남은 파일 0, 시작 판 스크립트 음성 대조 종료 코드 1 · FAIL 1
- ER-03: `logdir.sh` 여덟 번 — 작업 폴더일 때 네 폴더, 본 레포일 때 두 폴더, `made=0` (두 파일 · 두 셸). 두 블록 명령 줄 차이 0
- ER-04: `evald.sh` bash · zsh 네 줄 `rc=0 lines=1 now=1 other_changed=0 extra=0`. ER-05: `renlist.sh` 새 꼴만 옛 경로를 D 로
- ER-06: 예시 두 줄에 `U=$(sprint_head <slug>) || exit 2` · `sealcnt.sh` 끝 판에서 `none rc=2` · `no_fm_get rc=2` · `full rc=0 broken= ok=68 absent=10` (bash · zsh) · 상한 꼴 대조 종료 코드 2 (bash · zsh) · `sigline.sh` 두 셸 `mine_last=1 mine_middle=1 mine_inline=0 unsigned=[inline.txt]`
- ER-07: `stale.sh` `clean rc=0 files=389 want=389 excluded_line=1` · `seeded rc=1 hits=5/5 other_owasp=0`
- ER-08: `vline.sh` `A vp_rc=2 v3569_fail_lines=4 unjudged=0 bare_fence=FAIL` · `B vp_rc=0 v3569_fail_lines=0 unjudged=0 bare_fence=PASS`, harness V 줄 열 개 `— OK` · 종료 코드 0, 검증 가이드 예시 판정 없는 줄 0 · `— FAIL` 1
- AR-01: `drift.sh` 기대 열세 줄 그대로 · `[NEW` 0 · `rc=0`, `f2map.sh` `reflect-kit=1 bambu-kit=1 onboarding-kit=1 howto-kit=1 api-kit=1 planning_refs=0`
- AR-02: `ci.py` `placed=7/7 zsh_first=1` · `\|\|` 0 · actionlint 0 · 끝 판에서 여섯 명령 모두 종료 코드 0 (`결과: 6 · 24 · 16 · 10 경우 중 불일치 0` · `EVALS_PASS` 둘). AR-03: `sync-orchestrator.py --check-only` 0
- AR-05: (a) 0 · (b) 0 · (c) 0 · (d) `SEAL_OK` · `SEAL_BROKEN` 0 · (e) 계약 파일 한 줄 · (f) 0. SC-00 · DG-01 · DG-03 · DG-04 모두 0
- SK-06 · AP-01 · RE-01: 번역투 0 · 근거 밖 새 URL 0 · 버전꼴 0 · `def _` 0. RE-02: 훅 함수 13 · 저장 스크립트 7 · `--check=code-fence` 2 줄 · `"0 bare" in out` 0 · `marketplace.json` 3. AP-04 열두 파일 각 1
- DG-02: `mdcmp.sh` 스물한 파일 `new_total=0` · `shcmp.sh` 넷 `new_total=0` · 파이썬 다섯 `py_compile -W error` 0. AP-03: `--check=code-fence` 종료 코드 0 · V6 `0 bare — OK` · 새 MD040 0
- DG-05: 끝 판 사본에서 `validate-plugin` · `sync-docs` · `sync-evals` · `run-evals` · `sync-orchestrator --check-only` 모두 0, 셸 넷 `bash -n` · `/bin/bash -n` 0.
  `validate-doc-contracts.py` 는 git 저장소가 필요해 풀어 둔 판에서는 끝 판 · 시작 판 둘 다 NOT RUN 종료 코드 2 — git init 한 사본에서 둘 다 0 (개정 파일에 적음).
  작업 폴더에서 `validate-post-kaizen.py --since 5b4fd72…` 은 `scope-isolation` · `doc-contracts` · `bare-fence` PASS, `docs-site-regen` FAIL(Final F2 몫)

커밋 뒤 저장소 검사(러닝북 검증 절): `validate-plugin.py` 전체 종료 코드 0 · `sync-docs.py --check-only` 0 · `sync-evals.py --check-only` 0 · `run-evals.py` 0(115 passed) ·
`validate-post-kaizen.py --since 5b4fd72` 위와 같음 · 킷 시험 `harness/evals/hooks/commit-guard-test.sh` 0 · `scripts/test-collect-kaizen-data.py` 0(31 통과) · `aggregation-test.sh` 0.

말투 대조(tone-guide Step 5, 레포 파일 `tone-kit/skills/tone-guide/SKILL.md` 와 코어 규칙표를 읽고 따름 — 어댑터 없음): 더한 줄 번역투 6 종(K-02) 0 ·
C-01 — 새 주석은 이유만(이름 바꾸기 세기 · 희소 체크아웃 · `.bak` 부산물 · 서브모듈 공통 폴더 · 부분 글자 판정 · 두 번 세지 않음), C-07 — 새 주석 블록은 3 줄 이하,
N-08 — 새 변수 한 글자 0(`t` 는 같은 함수의 기존 관례), K-11 — 새 합성어 0(「판정 글자」 · 「서명 줄」 은 계약 · 스키마에 있던 말).

## 바꾼 파일

서른하나 — 계약 공통 정의 `FILES` 그대로. `harness/` 열넷(README · 평가자 · 가이드 다섯 · 스키마 · 스킬 둘 · 스크립트 둘 · 시험 둘) · `scripts/` 다섯 ·
`.claude/skills/` 열하나(오케스트레이터 SKILL.md · 참조 둘 · 카이젠 스킬 여덟) · `.github/workflows/ci.yml`. 새 파일 없음.
공유 파일(`marketplace.json` · 킷 `plugin.json` · 루트 README · 루트 CLAUDE.md · `docs/` HTML · 처리 배정표 · 감사 기록 · 실패 횟수 · `.harness/stale-values.yaml`)은 건드리지 않았다.

## 반영한 처리 배정표 키

Final 계약이라 처리 배정표 행을 직접 받지 않는다. 받은 입력은 final-todo · xdiag · Phase notes 넘김 · Codex r1 이고 처리는 계약 입력 표 F1H-01 ~ F1H-95 에 있다.
조건으로 고친 것: F1H-04 · 05 · 07 · 08 · 09 · 11 · 12 · 13 · 15 · 16 · 17 · 18 · 21 · 24 · 25 · 27 · 29 · 32 · 36 · 46 · 49 · 50 · 51 · 52 · 53 · 55 · 57 · 61 · 62 · 63 · 64 · 68 · 69 · 70 · 71 · 72 · 73 · 75 · 83 · 85 · 86 · 87 · 88 · 89 · 90 · 93.
확인만: F1H-19 · 31 · 33 · 34. 다른 계약으로 넘긴 것은 입력 표 그대로(`kaizen-0924-final` · `kaizen-0924-f1-kit-followups`).

## 미반영 키와 사유

입력 표의 `고치지 않음` 스물아홉은 아래 `## 다음 사이클 메모` 에 ID 와 사유를 모두 옮겼다. 요지 — 새 도구 · 새 절 · 새 규칙이라 Final 에서 넣지 않는 것(오케스트레이터 Gotcha 「Final에서 새 기능을 추가하지 마라」),
세 Final 계약 어느 범위에도 없는 파일, 킷 폴더를 함께 고쳐야 하는 것, 근거 파일 재조회가 먼저인 것, 첫 CI 결과를 PR 뒤에만 볼 수 있는 것.

## 넘기는 것 (`kaizen-0924-final` 이 받는다)

- 버전 계획(`release-plan.md`): harness 는 고침 · 문서 정정 · 시험 추가만이라 patch 로 본다 — 새 기능 없음(훅 판정 · 저장본 값은 기존 규약에 맞춘 고침). `scripts/` · `.claude/skills/` · CI 는 버전 대상이 아니다
- 문서 사이트(F2): 이 계약이 고친 원본 가운데 대응 HTML 이 있는 것 — `harness/docs/guides/qa-evaluation-guide.md` · `skill-design-guide.md` · `agent-design-guide.md` ·
  `contract-design-guide.md` · `plugin-validation-guide.md`(→ `docs/harness/plugin-validation.html`) · `harness/references/contract-schema.md`. 이번에 고친 드리프트 검사가 매핑을 낸다
- 교차 진단 기록: Phase 계약 측정 구멍(F1H-95)과 p01 · p02 · p03 측정 결함(F1H-01 · 02 · 03 · 10)은 입력 표대로 `kaizen-0924-final` 몫
- 감사 로그 · 다음 사이클 메모로 옮길 것: 아래 `## 다음 사이클 메모` 전부

## changelog 한 단락

커밋 안전 훅이 경로를 지정한 커밋과 `-i` 커밋에서 이름 바꾸기를 삭제로 세지 않는다. 목록 사본에 작업 폴더 상태를 얹은 뒤 git 처럼 이름 바꾸기를 가려 남는 삭제만 세므로,
`git mv` 로 옮긴 폴더를 경로 지정 커밋으로 올려도 막히지 않고, 옮긴 새 경로가 지정 경로 밖이라 옛 경로가 삭제로 실리는 커밋은 그대로 막는다. 피드백 저장본과 평가자의
사용자 교정 로그 조회가 워크트리에서도 본 레포 이름을 쓴다. 평가자는 리포트 시각을 저장 순간의 `date` 로 덮어쓰고, 삭제 열거에서 이름 바꾸기 감지를 끈다. 계약 스키마의 측정
예시는 상한 해석이 실패하면 멈추고, 봉인 세기 블록은 함수 정의가 없으면 멈춘다. Diff-Scope 표준형의 상한 ref 는 커밋 구간을 재는 조건에만 요구한다. validate-plugin 의 V 줄은
늘 판정 글자로 끝나고, 사후 점검의 bare-fence 는 종료 코드로 판정한다. 옛 값 검사는 marketplace.json 의 킷 폴더까지 읽는다(133 → 389 파일). 문서 낡음 검사가 api-kit ·
howto-kit · onboarding-kit 원본과 스킬 본문을 실제 페이지로 잇는다. 오케스트레이터와 참조 문서가 Phase 17 을 담고, CI 가 Phase 가 넘긴 새 시험 여섯을 돈다.

## 킷 로그 한 단락

2026-09-24 사이클 Final — harness 쪽 후속 수정(`kaizen-0924-f1-harness-followups`). 입력: 교차 진단 P1 ~ P17 · final-todo · Phase notes 열일곱 · Codex 독립 검토 r1 7 건 · REVIEW 검토 두 회차.
외부 근거는 사이클이 이미 모은 근거 파일에서만 옮겼다 — 서브에이전트 동시 20 상한이 ultracode 에 없다 · `initialPrompt` 가 플러그인 서브에이전트에서 무시된다 · 배치 우선순위 1 위가 managed settings 다
([Claude Code sub-agents](https://code.claude.com/docs/en/sub-agents.md), `.harness/.meta/evidence/phase1.md:87` · `:90` · `phase4.md:148` · `:149`),
국립국어원 자료 `etc_seq=663` 의 실제 제목(`phase15.md:114`). 나머지는 저장소 안 실측 — 킷 Phase 동시 5 · 4 개에서 과부하 오류 529(감사 기록 두 사이클), api-verify 의 종료 코드 3 실측,
reflect-kit `project_root` 규칙.

## 다음 사이클 메모

계약 입력 표의 `고치지 않음` 스물아홉과 그 사유. 셋째 칸은 받을 곳이다.

| ID | 항목 | 사유 · 받을 곳 |
| --- | --- | --- |
| F1H-14 | `run-evals.py` 가 `evals.json` 만 읽음 · `assertions.json` 회귀 패턴 실행기 없음 | 실행기는 새 도구 — Final 에서 새 기능 금지. 다음 사이클 Phase 3 · 4 첫 항목 (F1H-84 와 같은 것) |
| F1H-35 | `feedback-schema.yaml` true 뜻 · 새 키 둘 | Phase 4 넘김대로 다음 사이클 Phase 2 · 3. `verify-feedback.sh` 가 체크리스트 키를 재지 않아 지금 저장 · 검증을 막지 않는다 |
| F1H-37 | 개정 번호 규칙 · 열 번호 정규식 · 측정 묶음 관례 · 도우미 추출 스크립트 · 봉인 둘째 줄 · `mktemp` 폴더 · 측정 공통 정의 예시 · 검사기가 돈 줄 · 추적 규칙 표 | 계약 스키마 · 설계 가이드의 새 규칙 — 다음 사이클 Phase 1 · 2 · 4 |
| F1H-38 | §3.7 ①~④ 생성 측 짝 · 스키마 ①~④ 계약 측 짝 | 새 절 신설 — 다음 사이클 Phase 1 · 2 |
| F1H-39 | `.harness/feedback-draft.yaml` 고정 이름 · sprint-contract Step 9 문구 | Phase 4 넘김대로 다음 사이클 Phase 2 |
| F1H-40 | `# sprint-scope` · agent 가이드 `:79` · create-agent `:25` · create-skill `:27` · Step 6.7 (a) · V6 범위 | 근거 재조회 · 새 절차 — 다음 사이클 Phase 4 |
| F1H-41 | `/sprint` Step 3 판정 표 · 재검증 블록의 폐기 결정 자리 | 새 규칙 · F20 결정 뒤 — 다음 사이클 Phase 4 |
| F1H-43 | 세 화면 규약의 공통 규칙 원문 절을 skill 가이드에 | 새 절 신설 — 다음 사이클 Phase 1 |
| F1H-44 | design · backend · rust-kaizen Gotcha 6 형제 표에 새 행 | 새 대조 항목 — 다음 사이클 그 킷 Phase (notes 배정 그대로) |
| F1H-47 | 평가 가이드 미검증 규약 새 판 · 킷 reviewer 일곱 사본 | 판정 문턱을 바꾸는 별도 관심사 — 다음 사이클 Phase 3 |
| F1H-48 | infra-kaizen Gotcha 8 복제 문구 | F1H-47 결정 뒤 |
| F1H-56 | 킷 넷 `hooks.json` 따옴표 · V8 검사 | 킷 넷을 함께 고쳐야 하는데 킷 폴더는 이 계약 범위 밖이고 한 커밋에 킷 하나 규칙과 부딪힌다 — 다음 사이클 Phase 4 |
| F1H-58 | `sync-evals.py` `TARGET_KITS` 에 reflect-kit 없음 | reflect-kit 에 `evals.json` 이 없어 결과가 안 바뀐다 |
| F1H-59 | bambu-kaizen Step 2 점검 줄 · 회귀 음성 대조 줄 | 새 절차 추가 — 다음 사이클 Phase 13 |
| F1H-60 | bambu-research 문구 | 세 Final 계약 어느 범위에도 없다(`.claude/skills/*-research/`) — 다음 사이클 Phase 13 |
| F1H-65 | `run-evals.py` `ALL_KITS` 에 onboarding 없음 | 평가 파일이 `skills/setup-guide/evals/` 에 있어 `<킷>/evals/evals.json` 규칙에 안 맞고 형식도 게이트 평가다. 대신 AR-02 가 CI 에 러너를 넣었다 |
| F1H-66 | `sync-docs.py` `MARKER_RE` 가 onboarding · planning README 표지를 못 읽음 | 고치면 킷 README 둘이 다시 만들어져 킷 범위다 — 다음 사이클 |
| F1H-67 | 설계 문서 `docs/superpowers/specs/2026-09-02-api-kit-design.md:249` | 세 Final 계약 어느 범위에도 없다 — 다음 사이클 Phase 16 (예제 원본은 kit-followups 몫) |
| F1H-76 | research-templates 에 Phase 17 표 없음 | 출처 선정은 새 내용 — 다음 사이클 Phase 17. 오케스트레이터가 「Phase 17 표는 아직 없다」 로 적었다 |
| F1H-77 | 오케스트레이터 · 수집기의 Phase 별 참조 매핑 표가 13 · 14 까지 | Phase 마다 참조 절을 정하는 새 내용 — 다음 사이클 |
| F1H-78 | tone-kaizen `docs/tone/*.md` 「8종」 (`:35` · `:100`) — 실제 `.md` 11 개 | 셈 기준(리서치 문서만인지)이 불분명 — 다음 사이클 tone-kaizen |
| F1H-79 | backend-kit 세 줄이 OpenAPI 명세 링크의 버전 표기를 인용해 옛 값 검사에 걸림 | 예외 등록부 `.harness/stale-values.yaml` 은 `kaizen-0924-final` 범위. 옛 값 검사가 backend-kit 을 빼고 이유를 출력한다. 다음 사이클: allow 세 줄을 넣고 `EXCLUDED_KITS` 에서 뺀다 |
| F1H-80 | 근거 재조회 항목 · 오류 문구 짝 · `omitClaudeMd` · 문장 삭제 사본 검토 절차 · 평가 가이드 「12 개 이상의 편향」 | 근거 파일 재조회가 먼저 — 다음 사이클 Phase 1 · 3 (배치 우선순위는 이번에 고쳤다) |
| F1H-81 | `scripts/collect-kaizen-data.py:421` 워크트리 묶기 규칙과 reflect-kit `facets_unmatched` 규칙 | 지금 facets 18 개는 경로가 전부 살아 있어 영향 0 — 지워진 워크트리 세션이 생기면 맞춘다 |
| F1H-82 | CI 에 넣은 러너의 첫 우분투 실행 확인 · 시간 상한 | 첫 CI 결과는 PR 뒤에만 볼 수 있다 — 다음 사이클 첫 확인 항목. zsh 설치 단계 시간과 howto 러너 8 ~ 9 초를 함께 본다 |
| F1H-84 | Codex r1 2 — `silent-check` 픽스처와 `assertions.json` 을 읽는 실행기가 없음 | F1H-14 와 같은 것 — 새 기능이라 다음 사이클 Phase 3 · 4 첫 항목 |
| F1H-91 | `.claude/skills/docs-site/SKILL.md:47-55` 매핑 표가 일곱 줄뿐 | `.claude/skills/docs-site/` 는 세 Final 계약 어느 범위에도 없다 — 다음 사이클. 이번에 고친 드리프트 매핑 · 오케스트레이터 F2 표와 맞춘다 |
| F1H-92 | 오케스트레이터 F4 research-log 목록 · 체크리스트 「per-kit research-log 6개 파일」 에 design · tone · api 없음 | 「파일이 없으면 새로 만든다」 조문과 함께 정해야 하는 새 내용 — 다음 사이클 |
| F1H-94 | validate-plugin V10 이 `docs/<킷>/` 원본을, V6 가 `skills/*/references/` 를 읽지 않음 | F1H-40 의 `V6 범위` 결정과 함께 — 다음 사이클 Phase 4 |

구현 중 새로 찾은 것 (입력 표 밖):

- 커밋 안전 훅의 `-a` · 같은 명령의 `git add -A` 경로도 옮긴 폴더(`mv` 뒤 새 경로를 올림)를 작업 폴더 삭제로 더해 센다 — 경로 지정 · `-i` 와 같은 결함이다.
  이번 계약 범위가 아니라 그대로 뒀다. 같은 목록 사본 방식(`overlay_deletes`)으로 고칠 수 있다 — 다음 사이클 Phase 4
- `validate-plugin.py` 의 V2 「없음」 줄은 상태가 `OK` 인데 글자는 `— SKIP (no templates/)` 다. 글자를 바꾸면 봉인된 Phase 11 · 13 · 14 · 16 · 17 계약의 DG-05 꼴과 어긋나 이번에는 그대로 뒀다
- 풀어 둔 판(`git archive`)에서 `validate-doc-contracts.py` 는 git 저장소가 없어 NOT RUN 이다. 계약 측정이 그 스크립트를 사본에서 돌리게 적을 때는 git init 한 사본을 쓰라고 contract-schema 측정 예시에 한 줄 둘 만하다 — 다음 사이클 Phase 2
- 이번 계약도 측정 도우미 스물하나 · 공통 정의 블록이 계약 1094 줄의 절반 가까이다. Phase 15 · 16 · 17 notes 와 같은 제안 — harness 공용 측정 파일로 빼면 계약과 검토가 가벼워진다
