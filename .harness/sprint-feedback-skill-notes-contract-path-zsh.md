# Sprint Feedback
Feature: 계약 스킬 안내 두 가지 — 피드백 저장의 계약 경로 · zsh 함정
Evaluated: 2026-09-26 19:10
Verdict: APPROVE
Iteration: 1

## Contract Fingerprint
- path: /Users/jackson/Hub/10_Dev/claude-plugins/.harness/sprint-contract-skill-notes-contract-path-zsh.md
- sha256: ca457eea907f28ce8173d6fb7422325e0629ee079e53423fdac871c291fe05ce
- status: active
- slug: skill-notes-contract-path-zsh
- contract_root: /Users/jackson/Hub/10_Dev/claude-plugins
- contract_root_unconfigured: false
- 선택 근거: ladder 1 명시경로
- legacy_contract_used: false
- seal_status: SEAL_OK
- measurement_seal_status: MEASURE_OK (v5.6 measurement_digest)
- contract_seal_broken: n/a
- 봉인 커밋 대조(1-e-3): seal_commit=d116907, files=1, 산문 차이 없음, conditions_digest 차이 없음
- 재확인(Step 5): 일치
- status_transition: active -> done (아래 참조)

## Amendments
- amendments: 0 (사이드카 없음)

## User Correction Audit
- correction_log_status: available
- unreflected_corrections: 0
- verdict 영향: 없음

## Cross-Diagnosis Handoff
- 상태: pending-parent
- 부모가 띄울 때 넘길 것: 계약 절대경로 `/Users/jackson/Hub/10_Dev/claude-plugins/.harness/sprint-contract-skill-notes-contract-path-zsh.md` · 아래 판정 결과 전문
- 부모가 물을 두 가지:
  1. 계약 조건의 원래 의도와 다르게 해석해 PASS/FAIL 을 오판한 조건이 있는가?
  2. 0 건·빈 출력을 근거로 PASS 한 조건 중, 문제가 있어도 0 을 냈을 측정(공허한 통과)이 있는가?

## Results

### Skill (4/4)
- [x] SK-01: Step 9 명령을 슬러그 계약 경로로 원문 그대로 실행 — PASS
  - 근거: `bash $M/step9_probe.sh harness/skills/sprint-contract/SKILL.md` → `saved=yes` · `contract_path: '/Users/jackson/Hub/10_Dev/claude-plugins/.harness/sprint-contract-measurement-digest-seal.md'` · `contract_path_inferred: false` · `warnings=0` (계약 기대값과 정확히 일치)
  - 음성 대조: 기준 판(6ad3cbc) SKILL.md 로 같은 도구 실행 → `contract_path 없음` · `warnings=1` (계약 기대값과 일치, 판별력 확인됨)
- [x] SK-02: HARNESS_CONTRACT 안내 문구 — PASS
  - 근거: Step 9 절 자르기에서 `HARNESS_CONTRACT` 3 줄(기준 ≥2) · `뺀다` 1 줄(기준 ≥1). `harness/skills/sprint-contract/SKILL.md:23-24,28-29`
- [x] SK-03: Gotchas 두 문구 — PASS
  - 근거: 경계값 Gotcha `grep -cF "grep -cE '^[<>]'"` = 1, 글로빙 Gotcha `grep -c '셸 이식성 규약'` = 1 (`SKILL.md:16,32`). 기준 판(6ad3cbc) 둘 다 0 확인
- [x] SK-04: 인자 치환 검사 V9 — PASS
  - 근거: `python3 scripts/validate-plugin.py harness` → `V9 arg-substitution  9 skills — OK`

### Script (1/1, 1 N/A)
- [ ] SC-00: N/A (스크립트 미변경) — 근거: 변경 3 경로에 `harness/scripts/` 0 줄 (`git diff --name-only 6ad3cbc origin/feat/skill-notes-contract-path-zsh -- . ':(exclude).harness'`)

### Error (1/1)
- [x] ER-01: 세 함정 + diff 줄 세기 예시 — PASS
  - 근거: `zsh -c 'n=3; echo "x $n[^0-9]"'` → `bad math expression`(실패), `${n}[^0-9]` → `x 3[^0-9]`(성공), `path=/tmp; tail -n1 /etc/hosts` (zsh) → `command not found: tail`(실패). `diff … | wc -l` = 4, `grep -cE '^[<>]'` = 2. 전부 계약이 적은 결과와 정확히 일치 (zsh·bash 양쪽 실행)

### Architecture (3/3)
- [x] AR-01: 셸 이식성 규약 글머리 2 개 추가 — PASS
  - 근거: 절 자르기에서 `grep -c '^- '` = 7(기준 5), `${n}` 이 20행, `PATH` 가 23행(서로 다른 줄), `2026-09-24` = 3(기준 ≥3). 기준 판(6ad3cbc) `${n}` 0 · `PATH` 0 · 날짜 1 확인
- [x] AR-02: HTML `id="shell"` 절 `<li>` 6 개 — PASS
  - 근거: `<li>` = 6(기준 4), `${n}` ≥1, `PATH` ≥1. 기준 판 `<li>` 4 확인
- [x] AR-03: 변경 파일 정확히 3 경로 — PASS
  - 근거: `git diff --name-only 6ad3cbc origin/feat/skill-notes-contract-path-zsh -- . ':(exclude).harness'` → `docs/harness/contract-schema.html` · `harness/references/contract-schema.md` · `harness/skills/sprint-contract/SKILL.md` (정확히 3개, 계약 기재 목록과 일치)

### Anti-patterns (2/2)
- [x] AP-03: 코드 블록 언어 표시 — PASS
  - 근거: `python3 scripts/validate-plugin.py harness` → `V6 code-fence  0 bare — OK`
- [x] AP-04: frontmatter name 유지 — PASS
  - 근거: 같은 명령 `V1 frontmatter  9 skills + 1 agent — OK`
- AP-01/AP-02 (패턴형): 변경분 diff 에 `hardcoded.*version` · `git push.*--force` 매치 0 건 (대상 3 파일 diff, 패턴 유효 — grep exit 1)

### Reusability (1/1, 1 N/A)
- [ ] RE-01: N/A (재사용 코드 없음) — 근거: AR-03 의 3 경로가 전부 `.md`/`.html`
- [x] RE-02: zsh 함정은 스키마 한 곳에만 — PASS
  - 근거: `grep -cF '${n}' harness/skills/sprint-contract/SKILL.md` = 0 (기준 판과 동일)

### Diagnostics (2/2, 2 N/A)
- [ ] DG-01: N/A (analyze 대상과 교집합 0) — 근거: AR-03 목록에 `scripts/release.sh` 0 줄
- [x] DG-02: 마크다운 경고 수 증가 없음 — PASS
  - 근거: `markdownlint-cli2 --config … SKILL.md` = 9(기준 9), `contract-schema.md` = 8(기준 8)
- [ ] DG-03: N/A (test 대상과 교집합 0) — 근거: DG-01 과 동일
- [x] DG-04: HTML 접근성 + 플러그인 검사 — PASS
  - 근거: `node scripts/check-docs-a11y.js docs/harness/contract-schema.html` → `1/1 PASS`. `python3 scripts/validate-plugin.py harness` → `Exit: 0`

## Unverifiable Summary
- invalid_evidence: 0
- env_gaps: 0
- verified_coverage: (17 - 0) / 17 = 1.00 (임계 0.60 충족)
- Verdict 영향: 통상

## Discrimination
- 적용 조건: 없음 (규칙 12 의 9 항 — 동시성 가드 · 인증/권한 · 멱등성 · 입력 검증 · 데이터 유실 · 마이그레이션 안전성 · 재시도/중복제거 · 보안 경계 · 사용자 결함 보고 충돌 — 대상 아님)
- 참고: SK-01 은 규칙 12 대상은 아니지만 계약이 자체 음성 대조를 요구해 기준 판(6ad3cbc)으로 실행 확인함 (결과 일치)

## Evidence Validity
- 검사 대상 증거: 17 건 (조건별 실행 산출물)
- 무효 판정: 0 건
- 셸 스니펫 실행 검증: 실행 17 건 · zsh/bash 양쪽 확인 1 건(ER-01, 계약이 zsh·bash 결과를 각각 요구) · 미실행 0 건
- 양성/음성 대조: SK-01, SK-03, AR-01, AR-02 — 계약에 실린 봉인 전 실측값(기준 커밋 6ad3cbc)과 대조하여 전부 일치

## Summary
- Total: 17/17 conditions passed (N/A 4건 별도 — SC-00, RE-01, DG-01, DG-03; 사유 확인됨)
- Verdict: APPROVE

## Improvement Suggestions
(없음 — 계약 조건 전부 명확했고 측정문이 실제로 판별력을 가짐)
