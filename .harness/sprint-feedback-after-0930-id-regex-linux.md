# Sprint Feedback
Feature: 조건 번호 정규식을 리눅스에서도 돌게
Evaluated: 2026-09-30 17:11
Verdict: APPROVE
Iteration: 1

## Contract Fingerprint
- path: /Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak3-rx/.harness/sprint-contract-after-0930-id-regex-linux.md
- sha256: fe4f65e75666c7c2be62cfe81a767433eb500dc298e295f8b1a58927ab60ffd8
- status: active
- slug: after-0930-id-regex-linux
- contract_root: /Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak3-rx
- contract_root_unconfigured: false
- 선택 근거: ladder 1 명시경로 (부모가 계약 절대경로를 지정해 호출)
- legacy_contract_used: false
- seal_status: SEAL_OK
- contract_seal_broken: n/a
- measure_status: MEASURE_OK
- 재확인(Step 5): 일치
- status_transition: active -> done (APPROVE 직후 처리)

## Amendments
- amendments: 0 (사이드카 파일 없음)

## User Correction Audit
- correction_log_status: available (`/Users/jackson/.claude/logs/claude-plugins/2026-09.md`)
- unreflected_corrections: 0 — 세션 `bda55d45-296c-491f-89ba-b52042d58e72` 로그를 스프린트 구간(계약 생성 16:25 이후)에서 전수 대조. 같은 세션의 다른 항목은 PR #123 CI 감시·「end」 묶음 교차 진단 결과였고, 이 rx 조건과 충돌하는 지시는 없었다. 다른 세션(`97f28e34…`)의 발언은 별개 작업 폴더(scenario-report-per-case)라 무관
- verdict 영향: 없음 (표면화 전용)

## Deletions
- deletions_range: bbcb43d8..chore/ak3-rx
- 커밋 구간 삭제: 0
- 커밋하지 않은 삭제: 0 (`git status --porcelain --no-renames` 에 `D` 줄 없음)
- 선언 밖 삭제: 0

## Cross-Diagnosis Handoff
- 상태: pending-parent
- 부모가 띄울 때 넘길 것: 계약 절대경로 `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak3-rx/.harness/sprint-contract-after-0930-id-regex-linux.md` · 아래 판정 결과 전문
- 부모가 물을 두 가지:
  1. 계약 조건의 원래 의도와 다르게 해석해 PASS/FAIL 을 오판한 조건이 있는가?
  2. 0 건·빈 출력을 근거로 PASS 한 조건 중 공허한 통과가 있는가? 특히 스크립트-03(149 계약 지문 비교)·오류-01(알려진 답 입력)처럼 산출물이 검사인 조건에서 규칙 10 의 다섯 가지 확인이 빠짐없이 됐는지
- 부모가 교차 진단을 마친 뒤 `cross_diagnosis_by` 를 `sprint-contract` 로 갱신한다

## Results

### Skill (2/2)
- [x] 스킬-01: 규약 문서·스킬·평가자·평가 가이드 네 파일의 조건 번호 식이 로캘과 무관한 모양으로 바뀐다 — PASS
  - 근거: `m 스킬-01` 직접 실행(TMPDIR 격리). 실측 `hangul_range=0` 네 파일 모두, `new_piece` 7·6·2·1(want 7·6·2·1과 일치), `counts_ok=1`, 종료 코드 0. 계약 실측값(사본 실측 `counts_ok=1`)과 정확히 일치. `git grep -n '가-힣'` 로 네 파일 자체에 잔존 0건도 개별 확인(`harness/skills/sprint-contract/SKILL.md`, `harness/agents/qa-evaluator.md`, `harness/docs/guides/qa-evaluation-guide.md` 각각 0줄)
- [x] 스킬-02: 규약 문서의 식 설명에 까닭이 한 줄 있다 — PASS
  - 근거: `m 스킬-02` 실행. `reason_lines=1 after_rule_line=+2`, 종료 코드 0. `harness/references/contract-schema.md:302`에 "한국어 번호 몫은 `[^ -~]+`(출력 가능한 ASCII 밖 글자)로 적는다. 한글 범위식은 로캘마다 뜻이 달라 쓰지 않는다 — 우분투 GNU grep 은 C.UTF-8 에서 이 범위식을 오류로 거부해 0 건을 냈다(2026-09-30)." 확인(Read)

### Script (3/3)
- [x] 스크립트-01: 맥에서 측정 시험이 실패 0, K3 경우가 옛 식을 잡는다 — PASS
  - 근거: `m 스크립트-01` 실행. `mac_rc=0 mac_fails= k3_pass=1 last=[실패 0 건] neg_rc=1 neg_fails=[K3-C.UTF-8한국어번호] ci_step=1`, 종료 코드 0. 음성 대조(규약 문서만 시작 판으로 되돌린 사본)에서 K3만 실패하는 것도 실측으로 확인(discrimination — 결합 확인, 아래 별도 절)
- [x] 스크립트-02: 리눅스(도커 ubuntu:24.04, LC_ALL=C.UTF-8)에서 측정 시험이 실패 0 — PASS
  - 근거: `m 스크립트-02` 직접 도커 실행. `linux_rc=0 linux_fails=[] k3_pass=1 last=[실패 0 건] neg_rc=1 neg_fails=[K1-한국어번호지문-bash,K1-한국어번호지문-zsh,K2-한국어번호조건수,K3-C.UTF-8한국어번호,M-bash,M-zsh]`, 종료 코드 0. 이 여섯 실패 목록은 PR #123 CI 실패와 정확히 같은 결함 재현(음성 대조 성립)
- [x] 스크립트-03: 봉인된 계약 149개의 두 지문이 맥/리눅스에서 새 규약으로 그대로다 — PASS
  - 근거: `m 스크립트-03` 직접 도커 실행. `contracts=149 rows=149 mac_old_vs_mac_new=0 mac_old_vs_linux_new=0 linux_new_err=0 control_mac_old_vs_linux_old=294`, 종료 코드 0. 양성 대조(옛 규약으로 맥/리눅스 비교)가 294줄 차이를 내 측정이 살아있음을 확인

### Error (1/1)
- [x] 오류-01: 조건 번호가 아닌 줄은 세지 않는다(알려진 답 6줄 입력) — PASS
  - 근거: `m 오류-01` 직접 실행(맥 3로캘×2식 + 도커 리눅스 2로캘×2식). `mac=4,4,4,4,4,4 linux=4,4,4,4`, 종료 코드 0. 식은 규약 문서에서 직접 추출(`rx=^- \[[ x]\] ([A-Z]{2,}|[^ -~]+)-[0-9]{2}`)했으며 하드코딩 아님

### Architecture (3/3)
- [x] 구조-01: 문서 쪽 두 파일이 원본과 같이 바뀐다(가로 넘침 0, css 검사 통과) — PASS
  - 근거: `m 구조-01` 직접 실행(Node+Playwright 3뷰포트×2쪽). `counts_ok=1 reason_lines=1 reason_li=1 after_rule_line=+1 cases=6 overflow=0 css_rc=0`, 종료 코드 0. `docs/harness/contract-schema.html` 8곳·`docs/harness/qa-evaluation-guide.html` 1곳 diff(Read)로 원본과 문구 일치 확인
- [x] 구조-02: 다른 용도의 한국어 글자 찾기 식(6파일)은 그대로다 — PASS
  - 근거: `m 구조-02` 실행. `left=[docs/react-kit/build-audit.html docs/react/kit-design/g6-build-audit.md docs/tone-kit/antipattern-catalog.html docs/tone/antipattern-catalog.md react-kit/agents/react-reviewer.md react-kit/skills/react-audit/SKILL.md] changed_kept=0`, 종료 코드 0. `git grep -l '가-힣' -- . ':(exclude).harness'` 로 같은 6파일·8줄 재확인(sibling enumerated 전수)
- [x] 구조-03: 커밋 규칙(합침 0·3개 이상·맨 위 폴더 하나·서명 줄) — PASS
  - 근거: `m 구조-03` 실행. 커밋 4개(`f6b55082`·`7ea4c2c0`·`174890a2`·`1fc9cb30`) 각각 `OK tops=1 outside=0 trailer=1`, `commits=4 merges=0 bad=0`, 종료 코드 0. `git log -1 --format='%(trailers:key=Co-Authored-By,valueonly)'` 로 서명 줄이 계약 지정 문구("Claude Opus 5.5 (1M context) <noreply@anthropic.com>")와 정확히 일치함을 4개 커밋 모두 개별 확인

### Anti-patterns (3/3)
- [x] 금지-02: force push 금지 — PASS
  - 근거: `git reflog show chore/ak3-rx` 에 `forced-update` 0줄
- [x] 금지-03: bare code fence 금지 — PASS
  - 근거: `python3 scripts/validate-plugin.py --check=code-fence` 종료 코드 0(14 plugins, 14 OK)
- [x] 금지-04: frontmatter name 필드 누락 없음 — PASS
  - 근거: `python3 scripts/validate-plugin.py harness --check=frontmatter` 종료 코드 0(9 skills + 1 agent OK)

### Reusability (2/2)
- [x] 재사용-01: 새 코드는 기존 시험 파일 안의 경우 하나, CI 등록됨 — PASS
  - 근거: 스크립트-01 실측 `ci_step=1`(`.github/workflows/ci.yml` 에 시험 단계 정확히 1개). `M3-규약과같음` 시험을 직접 실행(`bash harness/evals/measure/measure-helpers-test.sh`) → `PASS M3-규약과같음 same_as_schema=1 copies=0`
- [x] 재사용-02: 새 파일을 만들지 않고 기존 시험 파일에 경우를 더함 — PASS
  - 근거: `git diff --name-status bbcb43d8..chore/ak3-rx -- . ':(exclude).harness'` 에 `A`(추가) 줄 0개

### Diagnostics (3/3, N/A 3)
- [x] 진단-01: N/A(commands.analyze 대상과 교집합 0) — PASS(사유 실측 확인)
  - 근거: `git diff --name-only bbcb43d8..chore/ak3-rx | grep -c '^scripts/release.sh$'` = 0
- [x] 진단-02: markdownlint 경고 0·shellcheck 지적 0·bash -n 종료 코드 0 — PASS
  - 근거: `m 진단-02` 실행. 네 `.md` 파일 각 `warnings=0`, `md_warnings=0 shellcheck=0 bash_n_rc=0`, 종료 코드 0
- [x] 진단-03: N/A(commands.test 대상과 교집합 0) — PASS(사유 실측 확인, 진단-01과 동일 명령)
- [x] 진단-04: N/A(변경 파일 전부 harness/docs 범위 안) — PASS(사유 실측 확인)
  - 근거: `git diff --name-only bbcb43d8..chore/ak3-rx -- . ':(exclude).harness' | grep -cvE '^(harness/(references|skills|agents|docs|evals)/|docs/harness/)'` = 0
- [x] 진단-05: 로컬 CI 25단계 전부 rc=0(SKIP 1)·CI 전용 명령 12개 전부 rc=0 — PASS
  - 근거: `m 진단-05` 직접 실행(ci-local.sh 전체 구동, node_modules 심볼릭 링크 경유 playwright 포함). `local_rc0=25 local_lines=26 skip=1 a11y=[206/206 PASS] ci_only_failed=[]`, 종료 코드 0. 계약 실측값과 정확히 일치

## Discrimination (규칙 12 적용 조건만)
- 적용 조건: 스크립트-01·스크립트-02(정규식 변경의 효과 검증 — 입력 처리 로직 성격) — 단, 규칙 12의 9항(동시성/인증/멱등성/입력검증/데이터유실/마이그레이션/재시도/보안경계/사용자보고충돌) 중 어디에도 정확히 속하지 않아 필수 적용 대상은 아님. 계약 자체가 음성 대조를 조건문에 내장하고 있어 참고로 기록
- 결합 확인: 스크립트-01·02 — 측정 도우미가 `harness/evals/measure/measure-helpers-test.sh` 를 직접 실행(reimplementation 아님), `M3-규약과같음` 이 `measure-common.sh`가 규약 함수 블록을 읽어씀을 확인해 로직 중복 0
- 음성 대조: 계약 기재 있음 — 스킬-01(파일별 미변경 시 hangul_range≥1), 스크립트-01/02(규약 문서만 되돌린 사본에서 K3/6실패 재현), 스크립트-03(옛 규약으로 맥/리눅스 비교 시 294줄 차이), 오류-01(알려진 답 6줄) — 전부 실행으로 확인(static-only 아님, 실제 도커·git clone 사본으로 재현)

## Check Artifacts (산출물이 검사인 조건 — 스크립트-03·오류-01)
- 대상: 스크립트-03 — `m.sh` 의 `dig.sh`(조건/측정 지문 계산), 오류-01 — 규약에서 추출한 grep/awk 식
- ① 첫 칸만: 해당 없음(단일 파일 다중 로캘/플랫폼 비교 구조, "칸" 개념 없음)
- ② 실행 목록: 해당 없음(K3 는 `measure-helpers-test.sh` 본문에 실제로 추가되어 CI 단계에서 직접 실행됨 — `PASS K3-C.UTF-8한국어번호` 를 실제 실행으로 확인)
- ③ 못 읽는 칸: 해당 없음(149계약 전부 개별 파일로 읽고 `rows=149`로 전수 확인, 스크립트-03의 `linux_new_err=0`이 리눅스 읽기 실패 0을 직접 검증)
- ④ zsh·bash: 스크립트-01/02/03/오류-01 모두 bash(m.sh 자체가 `#!/usr/bin/env bash`로 해석기 고정) — 해당 없음(고정 해석기)
- ⑤ 효과 증명: 스크립트-01(옛 규약 사본 → K3 실패 1건 재현) · 스크립트-02(옛 규약 사본 → 6실패 재현, PR #123 CI 실패와 동일) · 스크립트-03(옛 규약 비교 → 294줄 차이) · 오류-01(알려진 답 6줄 중 조건번호줄 4개만 셈) — 전부 손으로 답을 아는 입력/사본으로 직접 재확인

## Unverifiable Summary
- invalid_evidence: 0
- env_gaps: 0
- verified_coverage: (19 - 0) / 19 = 1.00 (임계 0.60)
- 연속 ENV 승급: 없음
- Verdict 영향: 통상

## Evidence Validity
- 검사 대상 증거: 19건 (전 조건)
- 무효 판정: 0건
- 셸 스니펫 실행 검증: 실행 19건(모든 `m <조건번호>` 를 QA가 직접 bash로 실행, m.sh 자체가 bash 고정 해석기라 zsh 대조는 해당 없음) · 미실행 0건
- 양성 대조: 스킬-01/구조-01(계약 절 음성 대조: 미변경 파일은 hangul_range≥1) · 스크립트-01(K3 재현) · 스크립트-02(6실패 재현) · 스크립트-03(294줄 차이) · 오류-01(알려진 답 6줄) — 전부 계약 절 기재 대조를 직접 실행해 재확인
- 무효 0건은 미검증 카운터에 합산 없음 (현재 누계: 0)

## Summary
- Total: 19/19 conditions passed
- Verdict: APPROVE
- 안티패턴 위반 0건, 계약 봉인(SEAL_OK)·측정 봉인(MEASURE_OK) 모두 유효, 봉인 커밋(`f6b55082`, 파일 1개) 이후 계약 원문 변조 없음, 개정 사이드카 없음, 반영 안 된 사용자 교정 없음, 작업 폴더 밖 범위 침범 없음(변경 파일 전부 sprint-scope 목록 또는 `.harness/` 안), 삭제 0건

## Improvement Suggestions
- 없음 (계약 결함·측정 방식 불일치 미발견)
