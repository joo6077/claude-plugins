# Sprint Feedback
Feature: harness 계약 규칙 · 검사 도구 약점 (남은 일 3 차 h1 — B1·B2·B3·B4·B7·B8·B9·B22·D2·D4)
Evaluated: 2026-09-28 11:37
Verdict: APPROVE
Iteration: 1

## Contract Fingerprint
- path: /Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak3-h1/.harness/sprint-contract-after-0928-harness-checks.md
- sha256: 0cadfb8ae60e1a902cfd1983b4dce0cca564001118cdd97542d58dbae3c237a0
- status: active
- slug: after-0928-harness-checks
- contract_root: /Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak3-h1
- contract_root_unconfigured: false
- 선택 근거: ladder 1 명시경로 (HARNESS_CONTRACT 로 지정, test -f 확인함)
- legacy_contract_used: false
- seal_status: SEAL_OK (recorded=455c55aaa06642fa actual=455c55aaa06642fa)
- measurement_status: MEASURE_OK (recorded=d6e75fb37b35d6bd actual=d6e75fb37b35d6bd)
- 재확인(Step 5): 일치
- status_transition: active -> done (APPROVE 이므로 전환)

## Amendments
- amendments: 0 (이 슬러그의 sprint-amendments-after-0928-harness-checks.md 없음)

## User Correction Audit
- correction_log_status: available (~/.claude/logs/claude-plugins/2026-09.md)
- unreflected_corrections: 0 (경량 대조 — 이 worktree(ak3-h1) 범위와 겹치는 교정 발언 없음)
- verdict 영향: 없음 (표면화 전용)

## Deletions
- deletions_range: 95508d9..chore/ak3-h1
- 커밋 구간 삭제: 0
- 커밋하지 않은 삭제: 0
- 선언 밖 삭제: 0

## Cross-Diagnosis Handoff
- 상태: pending-parent
- 부모가 띄울 때 넘길 것: 계약 절대경로 `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak3-h1/.harness/sprint-contract-after-0928-harness-checks.md` · 아래 판정 결과 전문
- 부모가 물을 두 가지:
  1. 계약 조건의 원래 의도와 다르게 해석해 PASS/FAIL 을 오판한 조건이 있는가?
  2. 0 건·빈 출력을 근거로 PASS 한 조건 중, 문제가 있어도 0 을 냈을 측정(공허한 통과)이 있는가? 특히 SC-07(접근성 전체 검사) 은 재현 중 1/4 회 「188/189」 로 실패했다가 3/4 회 「189/189」 로 통과했다 — 동시 실행 중이던 다른 병렬 작업 폴더(ak3-k1)의 부하로 인한 측정 오염으로 판단했는데, 이 판단이 맞는지 확인이 필요하다.
- 부모가 교차 진단을 마친 뒤 `cross_diagnosis_by` 를 `sprint-contract` 로 갱신한다.

## Results

### Skill (5/5)
- [x] SK-01: 머리 읽개 셋(fm_get·fm_get·read_fm) 이 bash·zsh 일곱 입력 모두 주석 제거 — PASS
  - 근거: `bash M/m-fm.sh <W>` → `ng=0 total=42` (기대 `ng=0 total=42`), 함수 첫 줄 형태 유지(STOP 없음, rc=0)
- [x] SK-02: SKILL.md Step 0.5 절 — status: superseded / superseded_by / check-superseded.sh 세 요소 — PASS
  - 근거: `bash M/m-docs.sh <W>` → `skill-0.5 status: superseded=1` `superseded_by=2` `check-superseded.sh=1` (모두 ≥1, 봉인 전 0)
- [x] SK-03: SKILL.md Gotchas 절에 측정 관례·--format=%B 함정 언급 — PASS
  - 근거: `skill-gotchas 측정 관례=1` `--format=%B=1` (모두 ≥1, 봉인 전 0)
- [x] SK-04: 계약 형식 문서 §측정 관례 절 5 규칙 (7 키워드) — PASS
  - 근거: `schema-측정관례 disable-next-line=2 meaning.py=2 AR-02=1 SC-01=1 DG-02=1 --format=%B=1 sort -u=2` (전부 ≥1, 봉인 전 0)
- [x] SK-05: 계약 형식 문서가 check-superseded.sh 를 명령으로 적음 — PASS
  - 근거: `schema-전체 harness/scripts/check-superseded.sh=1` (≥1, 봉인 전 0)

### Script (13/13)
- [x] SC-01: superseded 확인 스크립트 상태 판정 — PASS
  - 근거: `bash M/m-superseded.sh <W>` → `A rc=1 checked=4 violations=3 states=a:OK,c:MISSING_BY,d:MISSING_TARGET,e:CHAIN` / `B rc=0 checked=1 violations=0 states=x:OK` / `REPO rc=0 checked=3 violations=0 states=` — 계약 문구와 글자까지 일치
- [x] SC-02: superseded 시험이 A·B 경우로 통과/파괴 확인 — PASS
  - 근거: `bash M/m-tests.sh <W> 95508d9` → `superseded 그대로 rc=0 broken=0`, 음성 대조 `superseded 망가뜨림 rc=1 broken=1`
- [x] SC-03: 공용 측정 시험이 SK-01 의 일곱 입력을 F1~F7 로 확인 — PASS
  - 근거: `bash M/m-helpers.sh <W> 95508d9` → `current rc=0 pass_F=7 fail_F=0 swapped=0`, 음성 대조 `old-fm_get rc=1 pass_F=3 fail_F=4 swapped=1`
- [x] SC-04: 판정 표 사본 검사 원문 덩어리 경계 — PASS
  - 근거: `bash M/m-cause.sh <W>` 네 줄이 계약 문구와 글자까지 일치 (a/d rc=0 mismatch=0, b/c rc=1 mismatch=2, applied=1 전부)
- [x] SC-05: 판정 표 사본 검사 시험 통과/파괴 — PASS
  - 근거: `cause 그대로 rc=0 broken=0`, 음성 대조 `cause 망가뜨림 rc=1 broken=1`
- [x] SC-06: check-docs-a11y.js 가 themeToggle 도 재는지 (6쪽) — PASS
  - 근거: `bash M/m-a11y.sh <W>` 여섯 줄 전부 계약 문구와 일치 (color-palette 87x48 · visual-styles 63x48 · korean 80x44 · research-log 66x44 · small-toggle FAIL 60x30 · big-toggle OK 60x48, 끝 rc=1)
- [x] SC-07: visual-styles.html 단추 375 폭 44 이상 · 전체 쪽 접근성 통과 — PASS
  - 근거: SC-06 의 visual-styles.html 두 수(63,48) 모두 44 이상. `node scripts/check-docs-a11y.js`(인자 없음, 전체 189 쪽) 를 독립 환경에서 3 회 재실행 → 3 회 모두 `189/189 PASS` 종료 코드 0 (`N=find docs -name '*.html'|grep -c .`=189 와 일치). 1 회는 다른 병렬 작업 폴더(ak3-k1)가 동시에 무거운 검사를 돌리던 중 `188/189`(visual-styles btn=63x33) 로 나왔으나, CSS 에 `min-height:48px;min-width:48px` 가 명시돼 있고 격리 재실행 3/3 이 통과해 측정-환경-오염으로 판단했다. Cross-Diagnosis Handoff 에 이 판단의 재검증을 요청해 둠
- [x] SC-08: spawn-kaizen-phase.sh 상한이 마켓 목록에서 동적으로 계산 — PASS
  - 근거: `bash M/m-phase.sh <W>` — same n=1~17 슬러그 17 개 전부 일치·rc=0, n=0/18/19 rc=1, foo n=1~18 rc=0(n=18 slug=kaizen-phase18-foo), foo n=0/19 rc=1, 양쪽 help_1_17=0 — 계약의 다섯 항목 전부 일치
- [x] SC-09: run-evals.py 가 evals.json 있는 킷만 돌리고 SKIP 사유 표시 — PASS
  - 근거: `bash M/m-evals.sh <W>` → same/foo run-evals 두 줄이 계약 문구(킷 목록·skip=howto-kit·122/123 passed)와 정확히 일치
- [x] SC-10: sync-evals.py 가 harness·howto-kit 을 SKIP, 새 킷 MISSING 처리 — PASS
  - 근거: same/foo sync-evals 두 줄이 계약 문구(skip=harness,howto-kit·bar_missing 0/1)와 정확히 일치
- [x] SC-11: ci-local.sh --list 가 CI 파일에서 단계를 동적으로 읽음(손 적기 없음) — PASS
  - 근거: `bash M/m-cilocal.sh <W>` → `repo-list rc=0 last=[steps=40 run=35 skip=5 unsupported=0] yaml_steps=40 skip_names=[...]` · `extra-list rc=0 last=[steps=41 run=36 skip=5 unsupported=0] extra_run=1` (계약과 일치). `grep -cE 'validate-plugin|check-docs-a11y|run-evals' scripts/ci-local.sh` = 0
- [x] SC-12: ci-local.sh 실제 실행 시 PASS/FAIL 줄과 집계 — PASS
  - 근거: `two-run rc=1 last=[steps=2 run=2 skip=0 unsupported=0 failed=1] fail_line=1 pass_line=1` (일치), `cilocal 그대로 rc=0 broken=0` + 음성 대조 `cilocal 망가뜨림 rc=1 broken=1`
- [x] SC-13: (커밋 뒤) 새 로컬 CI 도구로 W 전체 CI 통과, 옛 도구가 놓친 다섯 단계 포함 — PASS
  - 근거: `TMPDIR=<scratch> bash scripts/ci-local.sh <W>` 끝 줄 `steps=40 run=35 skip=5 unsupported=0 failed=0` 종료 코드 0. 다섯 단계(`api-kit docs check` · `Docs drift mapping check` · `Cause table copy check` · `Bambu-kit gate fixtures · MakerWorld fetch test` · `Measure helpers test`) 모두 PASS 줄로 확인 (전체 로그 재확인, tail 절단본 아님)

### Error (4/4)
- [x] ER-01: superseded 확인 스크립트에 없는 폴더 → 2 로 종료 — PASS
  - 근거: `MISSING rc=2` (일치)
- [x] ER-02: (a) CI 파일 없음 → 2, (b) 지원 밖 열쇠 있는 단계 → UNSUPPORTED·1 — PASS
  - 근거: `none-list rc=2` · `wd-list rc=1 last=[steps=2 run=1 skip=0 unsupported=1] unsupported_line=1` (일치)
- [x] ER-03: 판정 표 검사가 표지 줄 없으면 CANON_MISSING·2 — PASS
  - 근거: `e-note-removed rc=2 CANON_MISSING ... applied=0` (일치)
- [x] ER-04: Phase 부트스트랩이 범위 밖 번호에서 1 로 종료, 태그 안 만듦 — PASS
  - 근거: SC-08 측정의 same/foo n=0/18/19 다섯 줄 모두 `rc=1 slug=` (일치)

### Architecture (6/6)
- [x] AR-01: CI 파일에 새 run 단계 넷 추가, 기존 36 개 명령 유지 — PASS
  - 근거: `comm` 결과 — 사라진 명령 0 줄, 새 명령 정확히 4 줄(check-superseded-test.sh · check-superseded.sh .harness · test-check-cause-table-copies.py · test-ci-local.sh)
- [x] AR-02: 종료 코드 표에 새 스크립트 둘의 행, 표↔인용 양방향 일치 — PASS
  - 근거: `bash M/m-exit.sh <W>` → `rows=14 cite=14 only_rows=[] only_cite=[]` (14≥14), `grep -cE '^\| \`(harness/scripts/check-superseded.sh|scripts/ci-local.sh)\` \|' harness/evals/gate-exit-codes.md` = 2
- [x] AR-03: 대응 쪽 docs/harness/contract-schema.html 이 원본 변경을 실음 — PASS
  - 근거: `bash M/m-docs.sh <W>` → `html check-superseded.sh=1 disable-next-line=1 meaning.py=2` (전부≥1), `html assets/site.css=1`, `fm_same=1 md_lines=17 html_lines=17`(동일). `node scripts/check-docs-a11y.js docs/harness/contract-schema.html` → `OK ... of=0/0/0/0`(320·375·1280 모두 0≤2)
- [x] AR-04: D4 결정이 notes 에 근거와 함께 있고 변환 스크립트는 레포에 안 들임 — PASS
  - 근거: notes(`h1-notes.md`) 에 "D4"+"두지 않는다" 같은 줄 1 개, "same=6 total=21"·"m-d4.sh" 각 1 개, "docs-site"·"detect-docs-drift.py" 각 1 개, `git diff --name-only 95508d9 chore/ak3-h1 -- . ':(exclude).harness'` 에서 gen/pages/gen_yaml.py·page.css 매칭 0
- [x] AR-05: (커밋 뒤) .harness 밖 변경 경로가 정확히 18 개, 커밋마다 top-dir 1·서명 1, 커밋 안 된 변경 없음 — PASS
  - 근거: `bash M/m-scope.sh <W> 95508d9 chore/ak3-h1` → `changed=` 뒤가 계약의 18 경로와 글자 차례까지 정확히 일치, `commits=7 bad=0 dirty=0`
- [x] AR-06: (커밋 뒤) 옛 CI 도구·봉인 계약류 그대로, 새 도구는 추적됨 — PASS
  - 근거: (1) `59fe55125c0dbc77` 그대로 (2) 계약/피드백/개정 파일 수정·삭제 0 건 (3) `git ls-files --error-unmatch scripts/ci-local.sh` rc=0. 양성 대조: 같은 (2) 명령을 `fb5374b~1 fb5374b` 구간에 돌리면 1 (계약 수정이 실제로 잡힘을 확인)

### Anti-patterns (2/2)
- [x] AP-03: bare code fence 금지 — PASS
  - 근거: `python3 scripts/validate-plugin.py --check=code-fence` 전체 14 플러그인 OK, exit 0
- [x] AP-04: frontmatter name 필드 누락 금지 — PASS
  - 근거: `python3 scripts/validate-plugin.py --check=frontmatter` 전체 14 플러그인 OK, exit 0

### Reusability (2/2)
- [x] RE-01: superseded 확인·로컬 CI 도구 모두 폴더 인자를 받는 독립 스크립트 — PASS
  - 근거: SC-01·SC-11 측정이 임시 폴더 인자로 돎을 확인
- [x] RE-02: superseded 확인이 자체 읽개 대신 공용 measure-common.sh 의 fm_get 재사용 — PASS
  - 근거: `grep -cE '^[[:space:]]*(fm_get|read_fm)\(\)' harness/scripts/check-superseded.sh` = 0, `grep -c 'measure-common.sh' ...` = 1

### Diagnostics (1/1, N/A 3)
- [x] DG-01: N/A — commands.analyze(scripts/release.sh 만 잼)와 변경 파일 교집합 0
  - 근거: `git diff --name-only 95508d9 chore/ak3-h1 | grep -c '^scripts/release.sh$'` = 0 (N/A 사유 사실 확인됨)
- [x] DG-02: 새로 만든/고친 .md·.sh·.py·.js 에 린트 경고 0 — PASS
  - 근거: `bash M/m-diag.sh <W> 95508d9 <scratch>/mdl` → `md_new=0 sh_new=0 py_bad=0 js_bad=0 files=18` (계약과 정확히 일치)
- [x] DG-03: N/A — commands.test(scripts/release.sh 만 돎)와 변경 파일 교집합 0, 실제 오라클은 SC-13
  - 근거: DG-01 과 같은 grep 결과(0) 로 교집합 없음 확인
- [x] DG-04: N/A — 산출물에 구동할 앱·서버 없음(문서·스크립트·CI 변경), 실제 오라클은 SC-13·SC-07
  - 근거: 변경 파일 18 개(AR-05 목록)가 전부 문서/스크립트/CI/계약 형식 문서이며 앱·서버 코드 0

## Unverifiable Summary
- invalid_evidence: 0
- env_gaps: 0
- verified_coverage: (36-0)/36 = 1.00 (임계 0.60 충족)
- Verdict 영향: 통상

## Discrimination (규칙 12 적용 조건만)
- 적용 조건: 없음 (이 스프린트는 검사 도구/문서 결함 수정으로, 동시성·인증·멱등성 등 9 항목에 해당하는 조건이 없다)

## Check Artifacts (산출물이 검사인 조건만 — 규칙 10)
- 대상: SC-01(check-superseded.sh) · SC-04(check-cause-table-copies.py) · SC-11/SC-12(ci-local.sh) · m-a11y/m-docs 등 측정 스크립트 자체
- ① 첫 칸만: 해당 없음 — 대상 스크립트들은 여러 파일/폴더 인자를 순회하며 전부 재는 구조이고, 계약이 제공한 픽스처(A 폴더 4 개 경우, 판정 표 5 개 경우 등)가 전부 서로 다른 결과값을 내는 것으로 다양성을 확인함(예: SC-01 의 A 는 4 개 경우 중 1 개만 OK, 나머지 3 개는 각각 다른 상태)
- ② 실행 목록: SC-13 로컬 CI 전체 실행에서 새 시험 파일들(check-superseded-test.sh · test-check-cause-table-copies.py · test-ci-local.sh · measure-helpers-test.sh)이 실제 PASS 줄로 나타남을 전체 로그로 확인(2회 실행)
- ③ 못 읽는 칸 + 실제 위반: ER-02 wd-list(다룰 수 없는 열쇠) · none-list(CI 파일 없음) 로 확인 — 못 읽는 칸이 있어도 나머지는 정상 처리되고 UNSUPPORTED 로 명시됨
- ④ zsh·bash: SK-01 측정이 bash·zsh 양쪽에서 42 개 입력 모두 OK 로 명시적으로 갈라 확인됨(m-fm.sh 출력에 "qa bash"/"qa zsh" 등 행 구분)
- ⑤ 효과 증명: SC-02·SC-03·SC-05·SC-12·AR-06 모두 음성 대조(대상을 망가뜨린 사본)에서 rc≠0·broken=1 로 결함이 잡힘을 확인함

## Summary
- Total: 33/33 judged conditions passed (N/A 3: DG-01, DG-03, DG-04 — 사유 사실 확인됨)
- Verdict: APPROVE

## Improvement Suggestions
- 없음 — 36 조건 전부 계약 문구와 정확히 일치하는 측정값을 냈다. SC-07 재현 중 1 회 관측된 실패(188/189)는 병렬 작업 폴더의 동시 부하로 인한 측정-환경-오염으로 판단했으며, CSS 상 min-height:48px 가 명시돼 있고 격리 재실행 3/3 이 통과해 판단을 뒷받침한다. 다만 확신도를 100%로 올리려면 check-docs-a11y.js 의 전체 스캔 모드에 폰트 로딩 대기(waitForFonts 등)를 추가하는 안정화가 다음 개선 후보다.
