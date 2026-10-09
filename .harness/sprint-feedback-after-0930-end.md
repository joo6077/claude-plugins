# Sprint Feedback
Feature: 끝 — 깨진 바로가기 · 머리말 시험 · 평가 실행기 · 평가자 머리 읽기
Evaluated: 2026-09-30 15:34
Verdict: APPROVE
Iteration: 1

## Contract Fingerprint
- path: /Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak3-end/.harness/sprint-contract-after-0930-end.md
- sha256: 30ca71ad05141b0de311154bc71ee4a0a253f954d39d9248dd1ccf8cb2e6cfd4
- status: active
- slug: after-0930-end
- contract_root: /Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak3-end
- contract_root_unconfigured: false
- 선택 근거: ladder 1 명시경로 (지시문이 계약 절대경로를 직접 지정)
- legacy_contract_used: false
- seal_status: SEAL_OK (conditions_digest 기록 sha256:d2437ae0709e3d1a = 실측 d2437ae0709e3d1a — 단, 설치본 캐시 harness 0.16.0 의 verify_seal 정규식 `[A-Z]{2,}-[0-9]{2}` 은 이 계약의 한글 조건 번호(스크립트-XX 등)를 못 읽어 빈 해시를 낸다. 이 계약 자신의 GAP 분석 · 오류-01 이 이미 문서화한 결함이며, 레포 사본의 `([A-Z]{2,}|[가-힣]+)-[0-9]{2}` 정규식으로 재면 22 개 조건 전부 매치되고 지문이 정확히 일치한다. 레포 사본으로 판정했다 — 설치본은 harness 다음 릴리스로 풀릴 예정이라고 계약 자신이 명시)
- contract_seal_broken: n/a (SEAL_OK)
- measure_status: MEASURE_OK (measurement_digest 기록 sha256:1775115ab58ed74e = 실측 1775115ab58ed74e, 레포 사본 정규식 기준)
- 봉인 커밋 대조: seal_commit=6e87f54a, 담긴 파일 1개(계약 파일 단독), 봉인 커밋 대비 지금 판 조건 줄 밖(산문) 차이 0, conditions_digest/measurement_digest 변경 없음 → reseal 없음
- 재확인(Step 5): 일치 (평가 시작~종료까지 sha256 · mtime · git status 불변)
- status_transition: active -> done (아래 참조)

## Amendments
- amendments: 0 (`.harness/sprint-amendments-after-0930-end.md` 없음)
- PASS 근거 가능: 0
- PASS 근거 불가: 0

## User Correction Audit
- correction_log_status: available (`~/.claude/logs/claude-plugins/2026-09.md`)
- unreflected_corrections: 0
  - 스프린트 구간(계약 생성 2026-09-30 12:36 ~ 평가 시각) 안에서 세션 bda55d45 의 [prompt] 항목은 트리거 문구 "ㄱㄱ"(14:50:15) 하나뿐이고, 그 밖은 전부 도구 호출(tool-failure) 또는 다른 세션(97f28e34)의 무관한 작업(시나리오 보고서 템플릿)이다. 방향 교정·범위 축소·금지 지시·재작업 요구 성격의 사용자 발언은 없었다.
- verdict 영향: 없음 (표면화 전용)

## Deletions
- deletions_range: f0fcc534..HEAD
- 커밋 구간 삭제: 0
- 커밋하지 않은 삭제: 0
- 선언 밖 삭제: 0

## Cross-Diagnosis Handoff

- 상태: pending-parent
- 부모가 띄울 때 넘길 것: 계약 절대경로 `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak3-end/.harness/sprint-contract-after-0930-end.md` · 이 판정 결과 전문(본 리포트)
- 부모가 물을 두 가지:
  1. 계약 조건의 원래 의도와 다르게 해석해 PASS/FAIL 을 오판한 조건이 있는가? (특히: 설치본 캐시 harness 0.16.0 의 `verify_seal` 정규식이 한글 조건 번호를 못 읽어 봉인 검증에 레포 사본 정규식을 대신 쓴 판단이 타당한가)
  2. 0 건·빈 출력을 근거로 PASS 한 조건 중, 문제가 있어도 0 을 냈을 측정(공허한 통과)이 있는가? 산출물이 검사인 조건(스크립트-01~06)은 규칙 10 의 다섯 가지 가운데 돌리지 않은 것이 있는가?
- 부모가 교차 진단을 마친 뒤 `cross_diagnosis_by` 를 `sprint-contract` 로 갱신한다.

## Results

### Script (6/6)
- [x] 스크립트-01: 설치본 안내 검사가 대상 없는 바로가기를 못 읽음으로 잡는다 — PASS
  - 근거: `python3 .harness/.meta/after-0930-end/measure.py 스크립트-01` 직접 실행. 4 경우(`broken-link` rc=2 `UNREADABLE k/link.md` · `deleted` rc=0 `SKIP k/gone.md` · `link-deleted` rc=0 `SKIP k/link.md` · `live-link` rc=0 `TOTAL files=2 ok=2`) 모두 기대와 일치, `cases=4 right=4 ok=1` 종료 코드 0. 코드 확인: `scripts/check-install-docs-guidance.py`
- [x] 스크립트-02: 설치본 안내 시험이 두 모양을 가른다 — PASS
  - 근거: `m 스크립트-02` 직접 실행. `test_ok=1 base_fails=4 base_ok=1 pre_fails=3 pre_ok=1` 종료 코드 0. 시작 판(`f0fcc534`) 도구는 새 경우 4 에서만 실패, 지운 파일도 UNREADABLE 로 치던 판(`8dca3e73^`)은 경우 3 에서만 실패 — 시험이 두 결함을 따로 가른다(음성 대조 직접 재현)
- [x] 스크립트-03: Mermaid 시험이 머리말 건너뛰기를 지킨다 — PASS
  - 근거: `m 스크립트-03` 직접 실행. `test_ok=1 old_fails=9 old_ok=1 stub_ok=1 head_ok=1 ci_ok=1` 종료 코드 0. 머리말 건너뛰기 두 줄을 되돌린 사본은 경우 9만 실패, 늘 0을 내는 가짜 검사(stub)도 잡힘. CI 단계 이름에 "아홉 경우" 직접 확인(`.github/workflows/ci.yml:212`)
- [x] 스크립트-04: 평가 실행기가 이름으로 받은 킷을 재지 못하면 2로 끝난다 — PASS
  - 근거: `m 스크립트-04` 직접 실행. `no-such-kit`/`planning-kit` 모두 rc=2 + 킷 이름 포함, `backend-kit` rc=0. `cases=3 right=3 ok=1` 종료 코드 0
- [x] 스크립트-05: 평가 실행기 둘이 못 읽는 평가 파일을 2로 끝낸다 — PASS
  - 근거: `m 스크립트-05` 직접 실행(non-root 사용자, `rootless()` 확인 통과). `run`/`sync` 모두 권한 0일 때 `UNREADABLE ... evals.json (Permission denied)` + rc=2, 권한 복원 시 rc=0. `run_ok=1 sync_ok=1` 종료 코드 0
- [x] 스크립트-06: 평가 실행기 시험이 새 모양을 실패 경우로 갖고 CI 이름이 맞다 — PASS
  - 근거: `m 스크립트-06` 직접 실행. `test-run-evals.py` 경우 6개 중 통과 6, `test-sync-evals.py` 경우 3개 중 통과 3, 시작 판 도구는 각각 경우 4,5,6 / 3 만 실패. CI 단계 이름에 "없는 킷"·"못 읽" 확인. `ci_ok=1` 종료 코드 0

### Error (3/3)
- [x] 오류-01: 머리 읽개 사본 다섯이 줄 끝 주석을 값으로 읽지 않는다 — PASS
  - 근거: `m 오류-01` 직접 실행. qa-evaluator·contract-schema.md·contract-schema.html·sprint-contract·commit-guard 5개 사본 모두 `active|abc|x-y|a#b` 로 일치, 주석 벗기기 줄을 지운 변이(mutant)는 다른 값을 냄(`mut_ok=1`), `git grep`으로 같은 읽개 모양(4개 파일)과 정확히 일치(`grep_ok=1`). `copies=5 right=5 ok=1` 종료 코드 0
- [x] 오류-02: 앞 묶음 cx 재현의 평가·안내 검사 줄이 그대로다 — PASS
  - 근거: `m 오류-02` 직접 실행. `repro.sh` 출력 7줄(d2/d4/d6) 이 계약이 요구한 순서·내용과 정확히 일치. `lines=7 same=1` 종료 코드 0
- [x] 오류-03: 킷 이름을 주고 평가 실행기를 부르는 소비처가 그대로 통과한다 — PASS
  - 근거: `m 오류-03` 직접 실행. `tone-kit`(4 passed)·`backend-kit`(8 passed)·`infra-kit`(6 passed)·인자없음(122 passed) 모두 rc=0. 소비처 3파일(`.claude/skills/tone-kaizen/SKILL.md:95`·`backend-kit/README.md:56`·`infra-kit/README.md:56`) `git grep`으로 직접 확인, 그 외 소비처 없음. `cases=4 right=4 ok=1` 종료 코드 0

### Architecture (3/3)
- [x] 구조-01: 커밋 규칙 — PASS
  - 근거: `m 구조-01` 직접 실행 + 수동 대조(`git log --format='%P'`·`--format='%(trailers:key=Co-Authored-By,...)'`). `f0fcc534..HEAD` 커밋 7개 전부 부모 1개(합침 아님), 맨 위 폴더 1개(`.harness`/`scripts`/`.github` 만), 서명 줄 "Claude ... <noreply@anthropic.com>" 모양 일치, 범위 목록 안. `commits=7 bad=0` 종료 코드 0
- [x] 구조-02: 도구 설명 글이 새 종료 코드 까닭을 적는다 — PASS
  - 근거: `m 구조-02` 직접 실행. `check-install-docs-guidance.py`에 "바로가기", `run-evals.py`에 "없는 킷"·"평가 파일"·"못 읽", `sync-evals.py`에 "못 읽" 모두 확인. `miss=[] ok=1` 종료 코드 0
- [x] 구조-03: 기록 — PASS
  - 근거: `m 구조-03` 직접 실행. `.harness/.meta/after-kaizen-0928/end-notes.md` 존재, 10개 낱말 모두 포함, 서로 다른 8자리 16진수 10개(요구 3개 이상). `keys_ok=1 miss=[] hashes_ok=1` 종료 코드 0

### Anti-patterns (3/3)
- [x] 금지-02: force push 금지 — PASS
  - 근거: `git reflog show chore/ak3-end` 에서 `forced-update` 0줄
- [x] 금지-03: bare code fence 금지 — PASS
  - 근거: `python3 scripts/validate-plugin.py --check=code-fence` 직접 실행. 14개 플러그인 전부 `0 bare — OK`, 종료 코드 0. markdownlint(설정 `{MD013:false}`) 로 새 기록 `.harness/.meta/after-kaizen-0928/end-notes.md` 직접 측정: MD 경고 0건, `Linting: 1 file` 확인. 양성 대조: 같은 도구로 알려진 위반 사본(`scratchpad/mdl/pos.md`)을 재면 3건 검출(패턴 유효성 확인)
- [x] 금지-04: N/A (측정값 재현) — PASS
  - 근거: `git diff --name-only f0fcc534..chore/ak3-end | grep -cE '(SKILL|agents/[^/]+)\.md$'` 직접 실행 → 0. N/A 사유(SKILL.md/agents/*.md 미변경) 사실과 일치

### Reusability (2/2)
- [x] 재사용-01: 재사용 가능한 컴포넌트를 private 으로 만들지 않았다 — PASS
  - 근거: 새 코드는 전부 기존 검사·실행기의 예외 처리·판정 줄과 기존 시험 파일의 경우 추가뿐(신규 파일 0, 아래 재사용-02). 4개 시험 파일 모두 CI(`ci.yml:39,55,120,212`)에 등록되어 `git grep`으로 직접 확인, 이미 있던 CI 단계 재확인
- [x] 재사용-02: 기존 컴포넌트를 재사용했다(신규 파일 없음) — PASS
  - 근거: `git diff --name-status f0fcc534..chore/ak3-end -- scripts .github` 직접 실행 → 8개 파일 전부 `M`(수정), `A`(신규) 줄 0건. 못 읽음 줄 모양은 기존 `UNREADABLE <경로> (<까닭>)` 을 그대로 씀(오류-01/스크립트-05 출력에서 확인)

### Diagnostics (5/5, N/A 3)
- [x] 진단-01: N/A (측정값 재현) — PASS
  - 근거: `git diff --name-only f0fcc534..chore/ak3-end | grep -c '^scripts/release.sh$'` 직접 실행 → 0
- [x] 진단-02: IDE diagnostics 0개 — PASS
  - 근거: 바뀐 `.py` 6개 `python3 -m py_compile` 전부 rc=0, 바뀐 `.js` 1개 `node --check` rc=0. `.harness/.meta/after-kaizen-0928/end-notes.md` 를 markdownlint-cli2(scratch 사본 도구 + `{MD013:false}` 설정)로 직접 실행 → MD 경고 0건, `Linting: 1 file` 확인
- [x] 진단-03: N/A (측정값 재현, 진단-01과 동일 명령) — PASS
  - 근거: 위와 동일, 0
- [x] 진단-04: N/A (측정값 재현) — PASS
  - 근거: `git diff --name-only f0fcc534..HEAD -- . ':(exclude).harness' | grep -cvE '^(scripts/|\.github/)'` 직접 실행 → 0
- [x] 진단-05: 로컬 CI 와 CI 파일 전용 단계가 모두 통과한다 — PASS
  - 근거: `bash .harness/handoff/2026-09-26-tools/ci-local.sh <W>`(TMPDIR=scratch 아래 새 폴더) 직접 실행 — 25단계 전부 `rc=0`(`feedback-agg-test SKIP (yq 없음)` 예외 1건), `docs-a11y.log` 끝줄 `206/206 PASS`. CI 전용 명령 21개(check-api-kit-docs·test-check-api-kit-docs·detect-docs-drift --check-table·test-detect-docs-drift·check-docs-common-css·test-check-docs-common-css·check-cause-table-copies·test-check-cause-table-copies·check-install-docs-guidance·test-check-install-docs-guidance·test-run-evals·test-sync-evals·test-ci-local·measure-helpers-test·check-superseded-test·check-superseded .harness·bambu run-gate-fixtures·bambu makerworld-fetch-test·npx playwright test·check-docs-mermaid·test-check-docs-mermaid) 전부 직접 실행, rc=0 확인. 끝 줄: `12/12 PASS`·`경우 10개 중 통과 10`·`어긋남 0`·`경우 4개 중 통과 4`·`검사한 쪽 206·어긋난 쪽 0·못 읽은 쪽 0`·`경우 8개 중 통과 8`·`checked=2 violations=0`·`실패 0건`(x3)·`checked=6 violations=0`·`28경우 중 불일치 0`·`5경우 중 불일치 0`·`174 passed`·`쪽 3·예시 9·안 그려진 예시 0`·`경우 9개 중 통과 9` — 계약이 명시한 "구현 뒤 모양 사본" 값과 전부 일치

## Unverifiable Summary
- invalid_evidence: 0
- env_gaps: 0
- verified_coverage: (22 - 0) / 22 = 1.00 (임계 0.60)
- 연속 ENV 승급: 없음
- Verdict 영향: 통상

## Discrimination (규칙 12 적용 조건만)
- 적용 조건: 없음 (9항 — 동시성 가드/인증권한/멱등성/입력검증/데이터유실/마이그레이션안전성/재시도중복제거/보안경계/사용자보고충돌 — 중 어느 것에도 명시적으로 해당하지 않음. 다만 실행 오류-처리 성격이 있어 아래 결합 확인은 부가로 수행)
- 결합 확인(부가): `test-check-install-docs-guidance.py`(subprocess→check-install-docs-guidance.py) · `test-run-evals.py`(subprocess→run-evals.py) · `test-sync-evals.py`(subprocess→sync-evals.py) · `test-check-docs-mermaid.js`(spawnSync→check-docs-mermaid.js) 모두 `grep`으로 직접 대상 스크립트를 subprocess/spawnSync 로 호출함을 확인 — 결합 0 아님
- 음성 대조: 스크립트-01/02/03/04/05/06 전부 계약에 기재됨. 시작 판·중간 판 도구로 직접 재실행해 실패 재현 완료(위 Results 근거란)

## Check Artifacts (산출물이 검사인 조건만 — 규칙 10)
- 대상: 스크립트-01(`check-install-docs-guidance.py`) · 스크립트-04/05(`run-evals.py`/`sync-evals.py`) · 스크립트-03(`check-docs-mermaid.js`)
- ① 첫 칸만: 해당 없음 (표 형태 검사 아님 — 각 사례를 독립 임시 경로/저장소로 실행하는 구조라 순서 의존 첫 항목만 읽는 결함이 구조적으로 없음. `INSTALL_CASES` 4개·평가 실행기 사례 6개를 개별 확인해 전부 올바르게 갈림)
- ② 실행 목록: `test-check-install-docs-guidance.py`·`test-run-evals.py`·`test-sync-evals.py`·`test-check-docs-mermaid.js` 를 직접 실행해 새 경우 번호(4/5/6/9)가 실제로 돌고 통과하는 것을 출력에서 확인(표에만 올리고 안 돈 시험 없음)
- ③ 못 읽는 칸 + 실제 위반: 스크립트-05 에서 `k/evals/evals.json` 권한만 0으로 두고 나머지는 정상인 트리를 직접 만들어 돌림 — `UNREADABLE ... k/evals/evals.json (Permission denied)` + rc=2 로 그 파일만 짚어 잡음, 권한 복원 시 rc=0(다른 칸은 문제 없음을 확인)
- ④ zsh·bash: 해당 없음 (고정 해석기 — 대상 전부 `python3`/`node` 로 지정되어 사용자 셸에 붙여넣는 스니펫이 아님). 단, 같은 스프린트 안 K1-한국어번호지문 시험(`harness/evals/measure/measure-helpers-test.sh`)은 zsh·bash 양쪽에서 동일 결과(`8b52386c713a6054 c51d48673b5caeee`) 직접 확인 — 봉인 검증에 쓴 한글 정규식 함수의 셸 이식성 방증
- ⑤ 효과 증명: 스크립트-01(BASE 도구 `broken-link` rc=0/틀림 vs 구현 뒤 rc=2/맞음) · 스크립트-02(base_fails=4·pre_fails=3, 손으로 아는 결함과 일치) · 스크립트-03(old_fails=9, stub 가짜 검사도 rc=1로 잡힘) · 스크립트-04(BASE `no-such-kit`/`planning-kit` 모두 rc=0으로 틀림) · 스크립트-05(시작 판 rc=1 추적 출력·구현 뒤 rc=2) · 스크립트-06(run_base_fails=4,5,6·sync_base_fails=3) 모두 직접 재실행해 확인 — 다섯 항목 전부 충족

## User-Reported Failures
- 해당 없음 (이번 회차 신규 계약, 재개(REOPENED) 대상 없음)

## Evidence Validity
- 검사 대상 증거: 22건 (조건 22개, N/A 3건 포함 — 전부 측정값 직접 재현)
- 무효 판정: 0건
- 셸 스니펫 실행 검증: 실행 33건(measure.py 12조건 + CI 전용 21명령) · zsh/bash 양쪽 확인 1건(measure-helpers-test.sh) · 미실행 0건
- 양성 대조: [금지-03/진단-02 — 출처: 임시 사본(scratchpad/mdl/pos.md, 알려진 markdownlint 위반) — 대조 결과 MD 경고 3건 검출 · 종료 코드 1(위반 있음)] · [스크립트-01~06 — 출처: 계약 자체 기재 시작 판/중간 판 도구 — 대조 결과 각 조건 음성 대조란 참조]
- 무효 0건은 미검증 카운터에 합산 없음 (현재 누계: 0)

## Summary
- Total: 22/22 conditions passed
- Verdict: APPROVE

## Improvement Suggestions
- [seal_status] 검증경로-미기재 — 설치된 harness 0.16.0 의 `verify_seal`/`contract_digest` 정규식(`[A-Z]{2,}-[0-9]{2}`)이 한글 조건 번호(`스크립트-XX` 등)를 지원하지 않아 봉인 검증이 항상 빈 해시로 실패한다. 이 계약 자신의 GAP 분석·오류-01이 이미 레포 사본으로 고쳐진 사실(`([A-Z]{2,}|[가-힣]+)-[0-9]{2}`)을 문서화했다. 다음 harness 릴리스에서 설치본 캐시에 이 정규식이 반영되면 qa-evaluator 의 Step 1-e-2 SCHEMA ladder 1단계(설치본)가 정상 동작한다. 범위 밖으로 이미 계약에 명시돼 있어 이번 판정에는 영향 없음
