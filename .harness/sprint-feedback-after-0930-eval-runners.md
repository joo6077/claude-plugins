# Sprint Feedback
Feature: 평가 실행기 둘 — 대상 없는 바로가기 · 못 읽는 킷 하나
Evaluated: 2026-09-30 19:00
Verdict: APPROVE
Iteration: 1

## Contract Fingerprint
- path: /Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak3-ev/.harness/sprint-contract-after-0930-eval-runners.md
- sha256: 9bd3a7f990dac1baf230680c7dfcf1fbb7a83afc049bdba3697ac48e4026ec22
- status: active
- slug: after-0930-eval-runners
- contract_root: /Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak3-ev
- contract_root_unconfigured: false
- 선택 근거: ladder 1 명시경로 (HARNESS_CONTRACT 로 고정)
- legacy_contract_used: false
- seal_status: SEAL_OK (설치 플러그인 캐시 0.16.0 의 옛 정규식으로는 SEAL_BROKEN 오탐 — 조건 번호가 한글(스크립트-01 등)인데 캐시의 `contract_digest` 가 `[A-Z]{2,}-[0-9]{2}` 만 매치. 레포 자체 `harness/references/contract-schema.md`(dev v0.17.0, 커밋 `0e367f03`·`7ea4c2c0` 로 한글 조건번호 정규식 `([A-Z]{2,}|[^ -~]+)-[0-9]{2}` 반영)로 재검증하면 SEAL_OK. 캐시가 레포보다 낡아 생긴 스키마 버전 불일치이며 계약 위조가 아님)
- measure_status: MEASURE_OK (같은 레포 자체 스키마 기준)
- 재확인(Step 5): 일치
- status_transition: active -> done (본 평가 APPROVE 로 전환)

## Amendments
- amendments: 0 (사이드카 `sprint-amendments-after-0930-eval-runners.md` 없음)

## User Correction Audit
- correction_log_status: available (`~/.claude/logs/claude-plugins/2026-09.md`)
- unreflected_corrections: 0 (계약 생성 시각 2026-09-30 18:05 이후 세션 bda55d45 의 로그 항목 없음. 그 이전 항목은 "ㄱㄱ"·"지금은"·"얼마나햇어"·"다 끝난거임?" 류 진행 확인 질문뿐, 방향 교정 아님)
- verdict 영향: 없음 (표면화 전용)

## Deletions
- deletions_range: fe6704d8..HEAD
- 커밋 구간 삭제: 0
- 커밋하지 않은 삭제: 0
- 선언 밖 삭제: 0

## Cross-Diagnosis Handoff

- 상태: pending-parent
- 부모가 띄울 때 넘길 것: 계약 절대경로 `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak3-ev/.harness/sprint-contract-after-0930-eval-runners.md` · 본 판정 결과 전문
- 부모가 물을 두 가지:
  1. 계약 조건의 원래 의도와 다르게 해석해 PASS/FAIL 을 오판한 조건이 있는가?
  2. 0 건·빈 출력을 근거로 PASS 한 조건 중, 문제가 있어도 0 을 냈을 측정(공허한 통과)이 있는가? 산출물이 검사인 조건(스크립트-01~04, test-run-evals.py·test-sync-evals.py)이면 규칙 10 의 다섯 가지 가운데 돌리지 않은 것이 있는가?
- 부모가 교차 진단을 마친 뒤 `cross_diagnosis_by` 를 `sprint-contract` 로 갱신한다.

## Results

### Script (4/4)
- [x] 스크립트-01: 대상 없는 바로가기를 못 읽음으로 잡는다 — PASS
  - 근거: `python3 .harness/.meta/after-0930-eval-runners/measure.py 스크립트-01` 직접 재실행 → `OK b-dangling run/sync-check/sync-plain rc=2 line=1 measured=1 summary=1` × 3, `cases=3 right=3 ok=1`, 종료 코드 0. 계약 지정값과 정확히 일치 (L3)
- [x] 스크립트-02: 진짜 없는 평가 파일은 지금처럼 넘긴다 — PASS
  - 근거: `m 스크립트-02` 재실행 → `cases=6 right=6 ok=1 lexists_uses=4 mut_right=0 mut_ok=1`, 종료 코드 0. `LEXISTS_TRUE` 변이(바로가기 판정을 늘 참으로 바꿈) 사본은 `b-absent` 세 경우가 걸려 `mut_ok=1` — 판별력 있는 음성 대조 확인 (L3)
- [x] 스크립트-03: 한 칸을 못 읽어도 나머지를 재고 끝에 2 — PASS
  - 근거: `m 스크립트-03` 재실행 → 9 줄 `OK`, `cases=9 right=9 ok=1`, 종료 코드 0. `m 스크립트-03-base`(시작 판 도구, 음성 대조) 재실행 → `cases=12 base_right=0 base_all_wrong=1`, 종료 코드 0 — 옛 도구는 12 경우 모두 `BAD` (L3)
- [x] 스크립트-04: 시험 두 파일이 새 경우를 갖고 옛 판 · 지나친 판을 가른다 — PASS
  - 근거: `m 스크립트-04` 재실행 → `run_ok=1 sync_ok=1 run_base_fails=7,9 sync_base_fails=4,6 run_mut_fails=8 sync_mut_fails=5 ci_ok=1`, 종료 코드 0. 직접 `python3 scripts/test-run-evals.py`(경우 9 개 중 통과 9) · `python3 scripts/test-sync-evals.py`(경우 6 개 중 통과 6) 재실행, `.github/workflows/ci.yml` 39·55 줄 각각 1 개 단계이고 이름에 "여섯 경우"·"아홉 경우" 직접 확인 (L3)

### Error (2/2)
- [x] 오류-01: 이미 되던 호출은 그대로다 — PASS
  - 근거: `m 오류-01` 재실행 → `cases=6 right=6 ok=1 absent_same=1`, 종료 코드 0. 다섯 명령 개별 재실행으로 재확인(`--verbose`→122 passed, `--check-only`→0 added/orphans/missing, `tone-kit`→4 passed, `backend-kit`→8 passed, `infra-kit`→6 passed) (L3)
- [x] 오류-02: 앞 묶음 cx 재현의 평가 줄이 그대로다 — PASS
  - 근거: `m 오류-02` 재실행 → `lines=7 same=1`, 종료 코드 0 (L3)

### Skill (1/1)
- [x] 스킬-01: backend-kaizen 규칙이 새 동작을 적는다 — PASS
  - 근거: `m 스킬-01` 재실행 → `line=1 old=0 ok=1`, 종료 코드 0. `git diff fe6704d8..chore/ak3-ev -- .claude/skills/backend-kaizen/SKILL.md` 로 직접 대조 — 40 번째 줄이 "10. **run-evals.py ER-01 회귀 방지** — `scripts/run-evals.py` · `scripts/sync-evals.py` 는 … 나머지 킷을 끝까지 재고 … 2 로 끝난다" 로 바뀜, 옛 글 "즉시 종료하는 구조 유지" 없음 (L3)

### Architecture (3/3)
- [x] 구조-01: 커밋 규칙 — PASS
  - 근거: `m 구조-01` 재실행 → 커밋 6 개 모두 `OK`(맨 위 폴더 하나·서명 줄·범위 안), `bad=0 scope_entries=6 git_rc=0`, 종료 코드 0 (교차 진단 지적으로 시작 판 값이 `scope_entries=0`→`6`으로 실측 수정된 것도 직접 확인) (L3)
- [x] 구조-02: 설명 글이 새 동작을 적는다 — PASS
  - 근거: `m 구조-02` 재실행 → `miss=[] ok=1`, 종료 코드 0. 4 대상 파일의 docstring 에 요구 낱말(바로가기·나머지·7./8./9./4./5./6.) 전부 존재 확인 (L3, enumerated 4 파일 전수)
- [x] 구조-03: 기록 — PASS
  - 근거: `m 구조-03` 재실행 → `exists=1 miss=[] keys_ok=1 hashes=6 hashes_ok=1`, 종료 코드 0. `.harness/.meta/after-kaizen-0928/ev-notes.md` 에 8 개 낱말 전부 + 8 자리 16 진수 처리 커밋 해시 6 개(요구 3 개 이상) (L3)

### Anti-patterns (3/3)
- [x] 금지-02: force push 금지 — PASS
  - 근거: `git reflog show chore/ak3-ev | grep -c forced-update` → 0 (L2)
- [x] 금지-03: bare code fence 금지 — PASS
  - 근거: `python3 scripts/validate-plugin.py --check=code-fence` → 14 개 플러그인 전부 `0 bare — OK`, 종료 코드 0. `.harness/.meta/after-kaizen-0928/ev-notes.md` markdownlint MD040 경고 0 도 진단-02 에서 함께 확인 (L3)
- [x] 금지-04: SKILL.md 머리말 불변 — PASS
  - 근거: `m 금지-04` 재실행 → `found=1 same=1`, 종료 코드 0. `.claude/skills/backend-kaizen/SKILL.md` 의 `---`~`---` frontmatter 가 `fe6704d8` 판과 바이트 동일 (L3)

### Reusability (2/2)
- [x] 재사용-01: private 화 없음 — PASS
  - 근거: `git diff fe6704d8..chore/ak3-ev -- scripts/run-evals.py` 직접 읽음 — 새 코드는 `load_evals` 의 예외 분기(UNREADABLE 반환)·`main`의 요약/종료 코드 몇 줄뿐이고 새 공유 컴포넌트 없음. 시험은 CI 에 등록돼 누구나 부름(스크립트-04 `ci_ok=1`) (L3)
- [x] 재사용-02: 기존 파일 재사용, 새 파일 0개 — PASS
  - 근거: `git diff --name-status fe6704d8..chore/ak3-ev -- scripts .github .claude` → 전부 `M` 줄, `A` 줄 개수 0. 바로가기 판정은 `os.path.lexists`(기존 `check-install-docs-guidance.py` 선례와 동일 API), `UNREADABLE <경로> (<까닭>)` 형식도 기존 관례 그대로 diff 로 직접 확인 (L3)

### Diagnostics (2/2, N/A 3)
- [ ] 진단-01: N/A (commands.analyze 대상 `scripts/release.sh` 와 변경 파일 교집합 0)
  - 근거: `git diff --name-only fe6704d8..chore/ak3-ev | grep -c '^scripts/release.sh$'` → 0. N/A 사유 직접 측정으로 확인, 사실 (L3)
- [x] 진단-02: IDE diagnostics 경고/정보 0건 — PASS
  - 근거: 바뀐 `.py` 4개 모두 `python3 -m py_compile` 재실행 rc=0. 바뀐/새 `.md` 2개(`backend-kaizen/SKILL.md`, `ev-notes.md`) 각각 markdownlint-cli2(MD013 끔) 직접 재실행 → 경고 0건 · `Linting: 1 file` 확인. 양성 대조로 임시 `pos.md`(제목 없음+bare fence) 만들어 같은 명령 실행 → 경고 2건(MD041, MD040) 확인 — 검사가 살아있음을 직접 입증 (L3, 패턴 유효성 실측)
- [ ] 진단-03: N/A (commands.test 대상도 scripts/release.sh, 진단-01과 동일 근거)
  - 근거: 진단-01과 같은 명령, 0 (L3)
- [ ] 진단-04: N/A (구동할 앱/서버 없음, 산출물이 스크립트/시험/CI/스킬글/기록뿐)
  - 근거: `git diff --name-only fe6704d8..HEAD -- . ':(exclude).harness' | grep -cvE '^(scripts/|\.github/|\.claude/skills/backend-kaizen/)'` → 0. 직접 측정 확인, 사실 (L3)
- [x] 진단-05: 로컬 CI 와 CI 파일에만 있는 단계 모두 통과 — PASS
  - 근거: 레포 밖 옛 도구 `.harness/handoff/2026-09-26-tools/ci-local.sh` 부재 직접 확인. `bash scripts/ci-local.sh <W>`(TMPDIR 별도 스크래치, W 맨 위에서) 직접 재실행 → 끝 줄 `steps=52 run=47 skip=5 unsupported=0 failed=0`, `FAIL` 줄 0건, 종료 코드 0. 따로 지정된 9개 명령(`check-api-kit-docs.py`→12/12 PASS, `detect-docs-drift.py --check-table`→어긋남 0, `check-cause-table-copies.py`→violations=0, `measure-helpers-test.sh`→실패 0건, `run-gate-fixtures.sh`→28경우 불일치 0, `makerworld-fetch-test.sh`→5경우 불일치 0, `npx playwright test`→174 passed, `test-run-evals.py`→경우9개 중 통과9, `test-sync-evals.py`→경우6개 중 통과6) 전부 개별 재실행하여 종료 코드 0 확인 (L3)

## Discrimination (규칙 12)
- 적용 조건: 스크립트-01~04 (입력 검증에 준하는 구조적 오류 처리 — 엄격 적용은 아니나 계약 자체 내장 음성 대조로 점검)
- 결합 확인: 스크립트-01~04 — `measure.py` 의 `TOOLS` 가 `python3 scripts/run-evals.py`·`scripts/sync-evals.py` 를 서브프로세스로 직접 호출. 자체 재구현 아님, 직접 결합 확인
- 음성 대조: 스크립트-01~04 계약에 명시(있음) · 스크립트-03-base(시작 판 도구 12경우 전부 BAD) · 스크립트-02(`LEXISTS_TRUE` 변이 3경우 걸림) · 스크립트-04(base_fails=7,9/4,6, mut_fails=8/5) 모두 실행 재확인 — 구현을 무력화하면 측정이 실제로 실패함을 직접 확인

## Check Artifacts (규칙 10 — test-run-evals.py · test-sync-evals.py)
- 대상: 스크립트-04 — `scripts/test-run-evals.py`(9경우), `scripts/test-sync-evals.py`(6경우)
- ① 첫 칸만: `m 스크립트-04` 재실행 결과 `run_base_fails=7,9`(1번이 아닌 7·9번에서 실패)·`sync_base_fails=4,6`·`run_mut_fails=8`·`sync_mut_fails=5` — 여러 다른 위치의 경우가 각각 실패로 잡힘, 첫 칸만 읽는 결함 없음
- ② 실행 목록: `.github/workflows/ci.yml` 39·55줄에 `python3 scripts/test-sync-evals.py`·`python3 scripts/test-run-evals.py` 각 1개 단계 존재(직접 grep 확인) + 로컬 `scripts/ci-local.sh` 실행에서 해당 단계 rc=0 확인 + 직접 실행한 출력에 9/6 케이스 각각 `PASS 경우 N …` 줄로 전부 등장
- ③ 못 읽는 칸 + 실제 위반: 스크립트-03 경우 `ac-unreadable`(`a`·`c` 둘 다 권한 0)에서 `b` 는 재고 요약 줄 `못 읽은 킷 2 개: a, c` 로 정확히 구분 — 못 읽는 칸이 있어도 전체가 조용히 꺼지지 않음을 `m 스크립트-03` 직접 재실행으로 확인
- ④ zsh · bash: 해당 없음 (고정 해석기 — `test-run-evals.py`·`test-sync-evals.py` 는 순수 Python, `#!/usr/bin/env python3` 로 python3 인터프리터 고정)
- ⑤ 효과 증명: `스크립트-03-base`(시작 판 도구, 12경우 모두 `BAD`, `base_all_wrong=1`) · `스크립트-02` 변이(`LEXISTS_TRUE`, `mut_right=0 mut_ok=1`) 둘 다 알려진 결함 입력에서 실패를 정확히 냄을 직접 재실행으로 확인

## Unverifiable Summary
- invalid_evidence: 0
- env_gaps: 0
- verified_coverage: (20 - 0) / 20 = 1.00 (임계 0.60)
- Verdict 영향: 통상

## Summary
- Total: 17/17 conditions passed (N/A 3: 진단-01·03·04)
- Verdict: APPROVE

계약 20개 조건을 전부 직접 재실행하여(측정 도우미 `measure.py` 및 관련 명령 개별 실행) 계약에 명시된 기대 출력과 정확히 일치함을 확인했다. 음성 대조(구현을 되돌린 시작 판 도구, 판별력을 무력화한 변이)도 계약 명시대로 실패함을 직접 재현했다. 범위 경계(`# sprint-scope` 6개 경로 + `.harness/`) 밖 변경 없음, 삭제 없음, amendment 없음, 반영 안 된 사용자 교정 없음. 계약 봉인은 레포 자체(dev v0.17.0)의 최신 정규식 기준으로 SEAL_OK·MEASURE_OK — 설치된 플러그인 캐시(0.16.0)는 한글 조건번호 정규식이 없어 오탐(SEAL_BROKEN)을 내므로 그 결과는 폐기했다(스키마 버전 불일치, 계약 위조 아님).

## Improvement Suggestions
- [해당 없음] 설치된 harness 플러그인 캐시(v0.16.0)의 `contract-schema.md` 가 레포 dev 버전(v0.17.0, 한글 조건번호 정규식 도입)보다 낡아 `verify_seal`/`verify_measurement` 가 한글 조건번호 계약에서 오탐(SEAL_BROKEN)을 낸다. 이 자체는 이번 스프린트의 계약 조건은 아니지만, harness 플러그인을 다음 릴리스할 때 반영되어야 한다(이미 dev 판에 커밋 `0e367f03`·`7ea4c2c0` 로 존재 — 릴리스만 하면 해소).
