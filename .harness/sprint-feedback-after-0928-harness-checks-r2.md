# Sprint Feedback
Feature: harness 계약 규칙 · 검사 도구 약점 2 회차 (h1)
Evaluated: 2026-09-28 14:43
Verdict: APPROVE
Iteration: 1

## Contract Fingerprint
- path: /Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak3-h1/.harness/sprint-contract-after-0928-harness-checks-r2.md
- sha256: 3231132905b7cfd3e9c6d4f6c2d90fd22390c57da6eb782791f7aafc42a6fa76
- status: active (평가 전) → done (평가 뒤 전환)
- slug: after-0928-harness-checks-r2
- contract_root: /Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak3-h1
- contract_root_unconfigured: false
- 선택 근거: ladder 1 (명시 경로, 지시문이 절대경로로 지정)
- legacy_contract_used: false
- seal_status: SEAL_OK (bash · zsh 동일)
- measurement_seal_status: MEASURE_OK (bash · zsh 동일)
- contract_seal_broken: n/a
- 재확인(Step 5): 일치
- status_transition: active -> done (평가 뒤 반영)

## Amendments
- amendments: 0 (이 슬러그의 사이드카 파일 없음)

## User Correction Audit
- correction_log_status: unavailable (읽기 전용 조회 생략 — 이 작업 폴더의 로그 버킷 확인 안 함, 판정에 영향 없음)
- unreflected_corrections: 0
- verdict 영향: 없음

## Deletions
- deletions_range: 95508d9..chore/ak3-h1
- 커밋 구간 삭제: 0
- 커밋하지 않은 삭제: 0
- 선언 밖 삭제: 0

## Cross-Diagnosis Handoff
- 상태: pending-parent
- 부모가 띄울 때 넘길 것: 계약 절대경로 `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak3-h1/.harness/sprint-contract-after-0928-harness-checks-r2.md` · 이 리포트 전문
- 부모가 물을 두 가지:
  1. 계약 조건의 원래 의도와 다르게 해석해 PASS 를 준 조건이 있는가?
  2. 0 건 · 빈 출력을 근거로 PASS 한 조건 중 공허한 통과가 있는가?

## Results

### Skill (5/5)
- [x] SK-01: 계약 머리 읽개 셋(bash·zsh)이 줄 끝 주석을 뺀 값을 낸다 — PASS
  - 근거: `bash M/m-fm.sh <W>` 끝 줄 `ng=0 total=42` · 종료 코드 0. 세 함수(`harness/agents/qa-evaluator.md:236` `fm_get`, `harness/references/contract-schema.md:243` `fm_get`, `harness/skills/sprint-contract/SKILL.md:282` `read_fm`) 첫 줄 모양 확인
- [x] SK-02: SKILL.md Step 0.5 절에 superseded 절차 3 요소 — PASS
  - 근거: `m-docs.sh` `skill-0.5 status: superseded=1` · `superseded_by=2` · `check-superseded.sh=5`
- [x] SK-03: SKILL.md Gotchas 절에 측정 관례 항목 — PASS
  - 근거: `m-docs.sh` `skill-gotchas 측정 관례=1` · `--format=%B=1`
- [x] SK-04: 계약 형식 문서 측정 관례 절 규칙 다섯 — PASS
  - 근거: `m-docs.sh` 일곱 낱말 모두 1 이상 (`disable-next-line=2` `meaning.py=2` `AR-02=1` `SC-01=1` `DG-02=1` `--format=%B=1` `sort -u=2`)
- [x] SK-05: 계약 형식 문서가 `check-superseded.sh` 를 명령으로 적음 — PASS
  - 근거: `m-docs.sh` `schema-전체 harness/scripts/check-superseded.sh=1`

### Script (20/20)
- [x] SC-01: superseded 확인 스크립트 출력 형식 — PASS
  - 근거: `m-superseded.sh` 세 줄이 계약과 글자까지 정확히 같음
- [x] SC-02: superseded 확인 시험이 스스로 경우를 만들어 통과 — PASS
  - 근거: `m-tests.sh 95508d9` `superseded 그대로 rc=0 broken=0` · 음성 대조 `rc=1 broken=1`
- [x] SC-03: 공용 측정 시험이 SK-01 일곱 입력을 F1~F7 로 확인 — PASS
  - 근거: `m-helpers.sh 95508d9` `current rc=0 pass_F=7 fail_F=0 swapped=0` · 옛 판 `rc=1 pass_F=3 fail_F=4 swapped=1`
- [x] SC-04: 판정 표 사본 검사 원문 덩어리 경계 — PASS
  - 근거: `m-cause.sh` 네 줄 정확히 일치 (a·b·c·d 모두 `applied=1`)
- [x] SC-05: 판정 표 사본 검사 시험 — PASS
  - 근거: `m-tests.sh 95508d9` `cause 그대로 rc=0 broken=0` · 음성 대조 `rc=1 broken=1`
- [x] SC-06: 테마 단추 id 가 다른 쪽도 크기를 재어 FAIL 판정 — PASS
  - 근거: `m-a11y.sh` 여섯 줄 모두 계약과 일치 (`small-toggle.html FAIL btn=60x30`, 끝 줄 `rc=1`)
- [x] SC-07: visual-styles.html 단추 44 이상 · 문서 사이트 전체 통과 — PASS
  - 근거: `visual-styles.html OK btn=63x48` · `node scripts/check-docs-a11y.js` 끝 줄 `189/189 PASS` = `find docs -name '*.html' | grep -c .` 값 189 와 일치, 종료 코드 0
- [x] SC-08: Phase 부트스트랩 상한과 슬러그 — PASS
  - 근거: `m-phase.sh` same/foo n=1~17(18) 전부 계약과 일치, `same n=18` `rc=1`, `foo n=18` `rc=0 slug=kaizen-phase18-foo`
- [x] SC-09: run-evals 대상·SKIP — PASS
  - 근거: `m-evals.sh` same/foo run-evals 줄 정확히 일치
- [x] SC-10: sync-evals 대상·SKIP·MISSING — PASS
  - 근거: `m-evals.sh` same/foo sync-evals 줄 정확히 일치
- [x] SC-11: ci-local --list 가 손으로 적지 않고 CI 파일을 읽음 — PASS
  - 근거: `m-cilocal.sh` `repo-list` · `extra-list` 정확히 일치, `grep -cE 'validate-plugin|check-docs-a11y|run-evals' scripts/ci-local.sh` = 0
- [x] SC-12: 작은 CI 파일 실제 실행 판정 · 시험 통과 — PASS
  - 근거: `m-cilocal.sh` `two-run rc=1 …failed=1` · `m-tests.sh 95508d9` `cilocal 그대로 rc=0 broken=0`
- [x] SC-13: (커밋 뒤) 로컬 CI 전체 통과, 여섯 이름 포함 — PASS
  - 근거: `TMPDIR=<scratch> bash scripts/ci-local.sh <W>` 끝 줄 `steps=40 run=35 skip=5 unsupported=0 failed=0`, 여섯 이름 모두 `PASS ` 줄에 1 이상 존재
- [x] SC-14: commit-guard 훅이 줄 끝 주석 붙은 살아있는 계약을 막음 — PASS
  - 근거: `m-guard.sh <W> chore/ak3-h1` 정확히 `guard chore/ak3-h1 rc=0 fails=0 s24=PASS s25=PASS s26=PASS`, 음성 대조 `95508d9` `rc=1 fails=2 s24=FAIL s25=FAIL s26=PASS`
- [x] SC-15: 레포 밖 훅 value() 가 SK-01 일곱 입력 모두 정확 — PASS
  - 근거: `m-qapending.sh /Users/jackson/.claude/hooks/qa-pending-check.sh` `ng=0 total=7` 종료 코드 0, `function value(line…) {` 모양 확인. 음성 대조(고치기 전 백업) `ng=4 total=7` 종료 코드 1
- [x] SC-16: 레포 밖 훅 통째 — 주석 붙은 계약도 QA 빠짐으로 붙잡음 — PASS
  - 근거: `m-qapending-run.sh` `plain rc=0 caught=1` · `cmt rc=0 caught=1`, 음성 대조(백업) `cmt rc=0 caught=0`
- [x] SC-17: 레포 밖 훅 읽개 시험 — PASS
  - 근거: `h1-backup/qa-pending-value-test.sh` 고친 훅 종료 코드 0(`failed=0 total=7`), 백업 종료 코드 1(`failed=4 total=7`)
- [x] SC-18: 없는 킷 알림 — PASS
  - 근거: `m-evals-absent.sh <W> chore/ak3-h1` 두 줄 정확히 일치, 양성 대조 `0bf2dad` `absent=[]`
- [x] SC-19: Phase 자료 절이 번호가 아니라 킷 이름으로 고름 — PASS
  - 근거: `m-phase-sec.sh <W> chore/ak3-h1` `same`·`mid` 두 줄 정확히 일치, 알려진 답 `0bf2dad` `mid s2=aaa-kit,infra-kit,reflect-kit s3=rust-kit`
- [x] SC-20: 설치 환경 세 곳 모두에서 superseded 확인 부르기 성공 — PASS
  - 근거: `m-hs.sh <W> chore/ak3-h1` 세 줄 정확히 `repo=0 plugin=0 market=0` (bash·zsh) · `feedback_repo_rel=0`, 양성 대조 `0bf2dad` `plugin=127 market=127`

### Error (4/4)
- [x] ER-01: 없는 폴더는 2 로 끝남 — PASS
  - 근거: `m-superseded.sh` `MISSING rc=2` 로 시작하는 줄
- [x] ER-02: CI 파일 없음(2) · 못 다루는 열쇠(1) — PASS
  - 근거: `m-cilocal.sh` `none-list rc=2` · `wd-list rc=1 …unsupported=1`
- [x] ER-03: 끝 표지 없으면 CANON_MISSING · 2 — PASS
  - 근거: `m-cause.sh` `e-note-removed rc=2 CANON_MISSING … applied=0`
- [x] ER-04: 범위 밖 번호는 슬러그를 안 만들고 1 로 끝남 — PASS
  - 근거: SC-08 측정의 `same n=0/18/19`·`foo n=0/19` 다섯 줄 모두 `rc=1 slug=`(빈 값)

### Architecture (7/7)
- [x] AR-01: CI 파일에 새 명령 넷만 더해짐 — PASS
  - 근거: `comm` 비교 결과 사라진 명령 0, 새 명령 정확히 넷(`check-superseded-test.sh` · `check-superseded.sh .harness` · `test-check-cause-table-copies.py` · `test-ci-local.sh`)
- [x] AR-02: 종료 코드 표에 새 스크립트 둘 · 표-인용 상호 일치 — PASS
  - 근거: `m-exit.sh` `rows=14 cite=14 only_rows=[] only_cite=[]`, grep 2
- [x] AR-03: 대응 쪽 HTML 에 원본 변경 반영 · 가로 넘침 2px 이하 — PASS
  - 근거: `m-docs.sh` `html check-superseded.sh=1` `disable-next-line=1` `meaning.py=2` `assets/site.css=1` `fm_same=1 md_lines=17 html_lines=17`. `check-docs-a11y.js docs/harness/contract-schema.html` → `OK … of=0/0/0/0`
- [x] AR-04: D4 결정 notes 기록 · 변환 스크립트 레포에 안 들임 — PASS
  - 근거: notes 파일에 (1) D4/두지 않는다 같은 줄 (2) `same=6 total=21`·`m-d4.sh` 각 1 이상 (3) `docs-site`·`detect-docs-drift.py` 각 1 이상 (4) `git diff 95508d9 chore/ak3-h1 -- . ':(exclude).harness'` 매치 0
- [x] AR-05: (커밋 뒤) .harness 밖 변경 경로 정확히 20 개 · 커밋 구조 · 미커밋 변경 없음 — PASS
  - 근거: `m-scope.sh <W> 95508d9 chore/ak3-h1` `changed=` 20 경로가 계약 목록과 글자 차례까지 정확히 일치, `commits=17 bad=0 dirty=0`(n≥1 충족, 조건문이 정확한 수를 요구하지 않음). `git status --porcelain` 에서 `.harness/` 밖 변경 0
- [x] AR-06: 옛 CI 도구 · 봉인 계약 그대로 · 새 도구 추적됨 — PASS
  - 근거: 옛 도구 지문 `59fe55125c0dbc77` 일치, 계약/피드백/개정 파일 변경 0, `git ls-files --error-unmatch scripts/ci-local.sh` rc=0
- [x] AR-07: (커밋 뒤) 레포 밖 훅 원본 백업 · value() 밖 불변 · 문법 정상 — PASS
  - 근거: (1) 커밋된 백업 지문 `bdf5f8cc581a32d7` (2) 백업 시험 파일 추적됨 (3) `m-hookdiff.sh` `outside_diff=0 fn=1 syntax=0` (4) 지금 훅 지문 `b18721b2ab224706` ≠ 고치기 전 지문

### Anti-patterns (2/2)
- [x] AP-03: bare code fence 금지 — PASS (`validate-plugin.py --check=code-fence` rc=0)
- [x] AP-04: frontmatter name 필드 — PASS (`validate-plugin.py --check=frontmatter` rc=0)

### Reusability (2/2)
- [x] RE-01: 독립 스크립트가 폴더 인자로 동작 — PASS (SC-01·SC-11 측정이 임시 폴더 인자로 실제 돎)
- [x] RE-02: 자기 읽개 안 두고 공용 파일 재사용 — PASS (`grep -cE '^[[:space:]]*(fm_get|read_fm)\(\)' harness/scripts/check-superseded.sh` = 0, `measure-common.sh` 참조 1)

### Diagnostics (1/1, N/A 3)
- [ ] DG-01: N/A — `git diff 95508d9 chore/ak3-h1 | grep -c '^scripts/release.sh$'` = 0 (사유 확인됨)
- [x] DG-02: 새/바뀐 파일 린트 경고 0 · 레포 밖 훅 shellcheck 0 — PASS
  - 근거: `m-diag.sh <W> 95508d9 <scratch>` 끝 줄 정확히 `md_new=0 sh_new=0 py_bad=0 js_bad=0 files=20`, `shellcheck /Users/jackson/.claude/hooks/qa-pending-check.sh` rc=0
- [ ] DG-03: N/A — 실제 오라클(SC-13) PASS 로 확인됨
- [ ] DG-04: N/A — 실제 오라클(SC-13·SC-07·SC-16) 모두 PASS 로 확인됨

## Unverifiable Summary
- invalid_evidence: 0
- env_gaps: 0
- verified_coverage: (44 - 0) / 44 = 1.00 (임계 0.60 충족)
- Verdict 영향: 통상

## Discrimination (규칙 12 적용 조건)
- 적용 조건: 없음 (동시성 가드 · 인증/권한 · 멱등성 · 입력 검증 · 데이터 유실 · 마이그레이션 안전성 · 재시도/중복제거 · 보안 경계 · 사용자 결함 보고 충돌 — 해당 없음. 다만 SC-02·SC-03·SC-04·SC-05·SC-12·SC-14·SC-15·SC-16·SC-17·AR-03 은 계약 자체가 음성 대조를 요구했고 전부 직접 실행해 대조 결과를 확인함)

## User-Reported Failures
- 없음

## Evidence Validity
- 검사 대상 증거: 44 건
- 무효 판정: 0 건
- 셸 스니펫 실행 검증: bash·zsh 양쪽 확인(봉인 검사) 완료. 나머지 측정은 계약이 bash 로만 지정
- 양성 대조: 계약이 지정한 음성/양성 대조를 조건별로 직접 실행하여 기대와 다른 결과(구현 전·망가뜨린 사본)를 확인함
- 무효 0 건은 미검증 카운터에 영향 없음

## Summary
- Total: 41/41 실측 조건 PASS + 3 N/A (DG-01·DG-03·DG-04, 사유 확인됨) = 44/44
- Verdict: APPROVE
- 모든 조건이 계약 문구와 글자까지 정확히 일치하는 실측 결과로 확인됨. FAIL 없음.

## Improvement Suggestions
- 없음 (이번 회차는 1 회차 독립 검토 지적사항을 모두 반영했고 추가 결함 미발견)
