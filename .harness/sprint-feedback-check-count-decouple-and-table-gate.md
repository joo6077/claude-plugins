# Sprint Feedback
Feature: 검사 개수를 지시문에서 떼어내고 표 무결성 검사를 추가
Evaluated: 2026-09-24 13:20
Verdict: APPROVE
Iteration: 4

## Contract Fingerprint
- path: /Users/jackson/Hub/10_Dev/claude-plugins/.harness/sprint-contract-check-count-decouple-and-table-gate.md
- sha256: 074c59853f26389e9360f9eb96db518683bc362516951df0dea8f8ca9dde673b
- status: done (iteration 2 APPROVE 때 이미 전환됨 — 이번 재평가로 새로 바꾸지 않는다)
- slug: check-count-decouple-and-table-gate
- contract_root: /Users/jackson/Hub/10_Dev/claude-plugins
- contract_root_unconfigured: false
- 선택 근거: 사용자가 계약 절대경로를 명시 (ladder 1)
- legacy_contract_used: false
- seal_status: SEAL_OK
- contract_seal_broken: n/a
- 재확인(Step 5): 일치 (평가 시작·종료 시점 sha256 동일: 074c5985...)
- 봉인 커밋 대조(1-e-3): 봉인 커밋 2ae9794 대비 diff는 frontmatter `status: active -> done`
  한 줄뿐. 조건 줄·산문 전부 봉인 시점과 동일. `reseal_detected: false`
- status_transition: skipped (verdict=APPROVE 이지만 status 가 이미 done — 전환 대상 아님)

## 재평가 배경 — Iteration 3 APPROVE 뒤 커밋 2831bcb 로 무엇이 바뀌었나

부모 교차 진단이 Iteration 3 리포트/구현의 사실 오류 셋을 짚었고(개정 A-06), 커밋 2831bcb 로
고쳤다. 변경 파일 3개:

1. `scripts/validate-plugin.py` — (a) `check_v10_table_integrity` 함수 안 주석의 "136 줄"을
   "84 줄(9 파일)"로 정정 (b) `--help` epilog 를 하드코딩된 8개 이름 나열에서
   `f"체크 이름: {', '.join(CHECK_REGISTRY)}"` 로 바꿔 등록 표에서 직접 뽑도록 함
   (c) 모듈 설명 첫 줄 "7가지 카테고리로 검증한다" → "등록된 검사 전부로 검증한다"
2. `harness/docs/guides/plugin-validation-guide.md` — 같은 "136 줄" → "84 줄(9 파일)" 정정 1곳
3. `.harness/sprint-amendments-check-count-decouple-and-table-gate.md` — 개정 A-06 추가 (범위 밖)

이 세 변경은 모두 **주석·문서·도움말 텍스트**이고 `check_v10_table_integrity` 의 판정 로직
자체(코드펜스 처리, lstrip 판정, prev/next 행 판정)는 한 줄도 바뀌지 않았다. 아래에서 19개
조건 전부를 이 커밋 기준(HEAD=2831bcb)으로 직접 재실행해 확인했다.

## Amendments

- amendments: 6건 (A-01~A-06, 번호 중복 없음 — `grep -n '^## A-'` 확인: 6/43/67/138/183/198행)
- PASS 근거 가능: 2건 — A-03(ER-02·AR-02 측정 좁힘, relaxing×anchored),
  A-04(AR-01 허용 목록 22개로 확장, relaxing×anchored). Iteration 3에서 이미 확인됨, 변동 없음
- PASS 근거 불가 조합: 0건
- A-01: 정보성 보고. A-03으로 대체됨
- A-02, A-05: 구현/판정 후 사소 수정. 조건 판정 무관
- A-06: **정보성 사실 정정** — Iteration 3 리포트·구현의 서술 오류 3건을 부모 교차 진단이
  짚고 이 스프린트 범위 안에서 고침. 측정 대상 집합이나 통과 기준을 바꾸지 않았으므로
  direction/consent 분류 대상이 아니다(허용 파일 집합·재는 낱말 집합 어느 쪽도 불변).
  아래에서 A-06이 주장한 수치(84줄·9파일 vs 136줄·26파일, `--help` 10개 완전 나열)를
  전부 직접 재현해 확인했다

## User Correction Audit

- correction_log_status: available (`~/.claude/logs/claude-plugins/2026-09.md`)
- unreflected_corrections: 0 — 이 세션(f5b7f3a5-...)의 마지막 사용자 프롬프트는
  12:34:07(A-04 동의)이며 그 이후 항목(A-06)은 부모 교차 진단에 대한 자동 수정으로,
  이 세션에 새 사용자 지시가 없었다. 13:00 전후 로그의 다른 프롬프트(12:58~13:00)는
  세션 `de8c7935-...`의 별개 작업(인사이트/카이젠)이며 이 계약과 무관
- verdict 영향: 없음 (표면화 전용)

## Cross-Diagnosis Handoff

- 상태: pending-parent
- 부모가 띄울 때 넘길 것: 계약 절대경로
  `/Users/jackson/Hub/10_Dev/claude-plugins/.harness/sprint-contract-check-count-decouple-and-table-gate.md`
  · 이 판정 결과 전문 · 개정 A-06 (앞선 교차 진단이 짚은 사실 오류 3건과 그 수정)
- 부모가 물을 두 가지:
  1. 계약 조건의 원래 의도와 다르게 해석해 PASS/FAIL 을 오판한 조건이 있는가?
  2. 0 건·빈 출력을 근거로 PASS 한 조건(SK-01·ER-02·AR-02·AR-03) 중, 문제가 있어도 0 을 냈을
     측정(공허한 통과)이 있는가?
- 부모가 교차 진단을 마친 뒤 `cross_diagnosis_by` 를 `sprint-contract` 로 갱신한다.

## Results

### Skill (3/3)
- [x] SK-01: 21개 파일 중 기준 문서를 뺀 20개(.py 제외 19개)에 개수·범위 표기 0줄 — PASS
  - 근거: L3. 계약 지정 측정 명령 직접 재실행(HEAD=2831bcb) → `총=0 대상=19`.
    2831bcb가 건드린 두 파일(validate-plugin.py, plugin-validation-guide.md)은
    이 측정 대상에서 원래부터 제외 대상이라 영향 없음을 직접 확인
- [x] SK-02: 검사 목록을 얻는 명령이 지시문에 실려 있다(최소 3개 파일) — PASS
  - 근거: L3. `.claude/skills/design-kaizen/SKILL.md`, `.claude/skills/rust-kaizen/SKILL.md`,
    `.claude/skills/tone-kaizen/SKILL.md` 3개 파일에 `check_v[0-9]` 패턴 각 1건 재확인
- [x] SK-03: sprint-contract/SKILL.md 의 병합 서술이 재배치를 인정하고 위험을 구별 — PASS
  - 근거: L3. `harness/skills/sprint-contract/SKILL.md:746-752` 직접 Read.
    `재배치` 4건, "main 이 앞서 있으면" · "해시가 바뀌어" 문맥 확인. 이 파일은 2831bcb의
    변경 대상이 아니므로 변동 없음

### Script (2/2)
- [x] SC-01: `validate-plugin.py`에 표 무결성 검사가 V10으로 등록되고 돌아간다 — PASS
  - 근거: L3. (a) `grep -c 'def check_v10' scripts/validate-plugin.py` = 1
    (b) `grep -oE '"[a-z-]+": check_v10'` = 1건 (`"table-integrity": check_v10`)
    (c) `python3 scripts/validate-plugin.py --check=table-integrity` →
    `V10 table-integrity   10 md files — OK` / `Total: 14 plugins, 14 OK` / `Exit: 0`.
    2831bcb는 이 함수의 주석 문구만 고쳤고(136→84줄 정정) 판정 로직은 무변경 —
    diff 직접 확인(`git show 2831bcb -- scripts/validate-plugin.py`)
- [x] SC-02: `python3 scripts/validate-plugin.py` 전체가 14 plugins 14 OK Exit 0 — PASS
  - 근거: L3. 직접 재실행 → `Total: 14 plugins, 14 OK` / `Exit: 0`

### Error (2/2)
- [x] ER-01: V10 대상 범위가 V6보다 넓고 이유가 적혀 있다 — PASS
  - 근거: L3. `check_v10_table_integrity` 함수 안 `docs` 문자열 3회(glob 1곳 + docstring 2곳).
    `harness/docs/guides/plugin-validation-guide.md:450-453`에 정정된 이유 서술 확인
    (2831bcb가 건드린 줄은 그 바로 다음 문단의 "136→84줄" 수치뿐, 이유 서술 문장은 무변경)
- [x] ER-02: 개수 표기를 지운 자리가 "등록된 검사 전부" 식으로 바뀌었다(개수 신규 박기 없음) — PASS
  - 근거: L3 (amendment A-03 적용). 좁힌 측정(`grep -c 'V1~V10\|V1-V10'`)을 20개 파일에
    직접 재실행 → `총=0`

### Architecture (4/4)
- [x] AR-01: 변경 파일이 21개 경로와 정확히 일치(amendment A-04 적용 시 22개) — PASS
  - 근거: L3. `sprint_head` 해석 → `2831bcbd37eb4bf0bcb28e2bba6acb7dc82c1937`
    (UNRESOLVED 아님, STALE_HEAD 아님 — feat/check-count-decouple-and-table-gate 브랜치가
    아직 main에 병합되지 않아 `git rev-parse --verify` 로 직접 해석됨).
    `git diff --name-only c0e12a8..2831bcb -- . ':(exclude).harness/**'` → 정확히 22행,
    원 21개 + A-04로 추가된 `reflect-kit/skills/reflect-promote/SKILL.md` 와 1:1 일치.
    2831bcb 자신이 건드린 3개 파일(validate-plugin.py, plugin-validation-guide.md,
    사이드카) 중 사이드카는 `.harness/**` 제외 대상이고 나머지 둘은 이미 22개 목록 안에
    있어 diff 결과에 새 항목이 추가되지 않았다
- [x] AR-02: 기준 문서가 개수를 적는 유일한 자리(그 밖 20개는 0) — PASS
  - 근거: L3. `plugin-validation-guide.md`에 `V1~V10|V1-V10` 2건. 나머지 19개(+py)
    파일에서 동일 패턴 0건(ER-02 측정과 동일 수치, 총=0)
- [x] AR-03: 손대지 않기로 한 것이 변경되지 않았다 — PASS
  - 근거: L3. `git diff c0e12a8..2831bcb -- harness/evals/` = 0행,
    `-- docs/kaizen/` = 0행. `verify_seal`을 `find .harness -name 'sprint-contract*.md'`
    (maxdepth 없음) 전체 63건에 직접 실행 → `SEAL_OK 63 · SEAL_ABSENT 10 · SEAL_BROKEN 0`.
    작업 폴더(`git status --porcelain`)도 확인 대상 외 잔여 변경 0건
- [x] AR-04: 이 계약 자신이 봉인 커밋 절차를 따랐다 — PASS
  - 근거: L3. `git log --diff-filter=A -- .harness/sprint-contract-check-count-decouple-and-table-gate.md`
    → 첫 커밋 `2ae9794`. `git show --name-only --format='' 2ae9794` → 파일 1개

### Anti-patterns (2/2, + 프로젝트 공통 AP-01·AP-02 위반 0건)
- [x] AP-03: bare code fence 0건(V6 대상) — PASS
  - 근거: L3. `python3 scripts/validate-plugin.py --check=code-fence` → 14 plugins 14 OK
- [x] AP-04: frontmatter 보존, V1 FAIL 0건 — PASS
  - 근거: L3. `python3 scripts/validate-plugin.py --check=frontmatter` → 14 plugins 14 OK
- 프로젝트 공통 anti_patterns(project.yaml) AP-01(hardcoded version)·AP-02(force push):
  c0e12a8..2831bcb 변경 파일 22개 전체에 패턴 검색 → 0건

### Reusability (2/2)
- [x] RE-01: V10이 기존 검사(V6·V9)와 같은 시그니처·형태를 따른다 — PASS
  - 근거: L3. `def check_v10_table_integrity(ctx: CheckContext) -> CheckResult:` 시그니처가
    `check_v6_code_fence`·`check_v9_arg_substitution`과 동일. `ctx.read`·`CheckResult` 각
    사용 확인(4건)
- [x] RE-02: 판정 로직이 `validate-plugin.py` 한 곳에만, 기준 문서는 가리키기만 — PASS
  - 근거: L3. `grep -c '^def ' harness/docs/guides/plugin-validation-guide.md` = 0

### Diagnostics (2/2, N/A 2)
- [x] DG-01: N/A — 근거 확인: 22행에 `scripts/release.sh` 0건 (사유 사실과 일치)
- [x] DG-02: 편집기 조건 마크다운 경고가 기준값 이내 — PASS
  - 근거: L3. scratchpad의 `markdownlint-cli2@0.23.2`(설정 `{"config":{"MD013":false}}`)로
    대상 20개 `.md` 파일에 직접 재실행. 결과: 총 347건, (파일,규칙) 조합 49개 —
    봉인 전 기준값(347건·49조합)과 정확히 일치, 늘어난 조합 0개.
    plugin-validation-guide.md가 2831bcb로 1줄 바뀌었지만(표 밖 산문 문단의 숫자 정정)
    경고 수·조합 수 모두 불변임을 직접 재실행으로 확인
- [x] DG-03: N/A — DG-01과 동일 사유·측정
- [x] DG-04: N/A — SC-02가 실질 검사 역할 수행(위에서 PASS 확인)

## 요청받은 3개 항목 직접 확인 (AR-01 · SK-01 · DG-02 무영향 + `--help` 실행)

- **AR-01**: 위에서 확인. 2831bcb가 건드린 파일 3개 중 2개(`.py`, 기준 문서)는 이미 22개
  허용 목록 안, 1개(사이드카)는 `.harness/**` 제외 대상 — diff 결과 22행 그대로, 무영향
- **SK-01**: 위에서 확인. 측정 대상 20개(기준 문서·`.py` 제외)에 2831bcb가 건드린 두 파일 다
  포함되지 않음 — 총=0 그대로, 무영향
- **DG-02**: 위에서 확인. 347건·49조합 정확히 재현 — 무영향
- **`--help` 실제 실행**:

  ```text
  $ python3 scripts/validate-plugin.py --help
  ...
  체크 이름: frontmatter, templates, refs, triggers, placeholders, code-fence, plugin-json,
  hook-exec, arg-substitution, table-integrity
  가이드: harness/docs/guides/plugin-validation-guide.md
  ```

  10개 등록 검사(`CHECK_REGISTRY` 순서)가 전부 나열됨을 직접 실행으로 확인. 이전 판은
  8개(하드코딩)만 나열해 `arg-substitution`·`table-integrity` 가 빠져 있었다(A-06의 지적).
  `CHECK_REGISTRY` 딕셔너리 정의(10개 키)와 1:1 일치도 직접 대조

## A-06 수치 독립 재현 (84줄·9파일 vs 136줄·26파일)

계약이 정의한 210개 대상 파일(marketplace.json 등록 14개 킷 × `skills/*/SKILL.md` +
`agents/*.md` + `references/*.md` + `docs/**/*.md` + 킷 루트 `README.md`)에 대해 두 셈법을
독립적으로(스크립트 재사용 없이 새로 작성한 파이썬 코드로) 실행:

```text
총 대상 파일 수: 210
코드 블록 제외 (지금 V10 로직 — line.strip().startswith("```") 로 펜스 토글, lstrip 판정): 84 줄 · 9 파일
코드 블록 포함(전부 셈 — 펜스 무시): 136 줄 · 26 파일
```

A-06의 주장(현재 V10 기준 84줄·9파일, 코드 블록 안까지 센 옛 수치 136줄·26파일)과 정확히
일치. `validate-plugin.py`와 `plugin-validation-guide.md`의 정정된 수치가 사실임을 확인

## Unverifiable Summary
- invalid_evidence: 0
- env_gaps: 0
- verified_coverage: (19-0)/19 = 1.00 (임계 0.60 충족)
- 연속 ENV 승급: 없음
- Verdict 영향: 통상

## Discrimination (규칙 12 적용 조건 없음)
- 적용 조건: 없음 — 이 스프린트 조건 중 동시성 가드·인증/권한·멱등성·입력 검증·데이터 유실·
  마이그레이션·재시도/중복제거·보안 경계·사용자 결함 보고 충돌 어디에도 해당하지 않음

## User-Reported Failures
- 없음. 이번 재평가는 부모 교차 진단이 짚은 사실 오류에 대한 자발적 수정(A-06)이며 사용자의
  별도 결함 보고는 없었다

## Evidence Validity
- 검사 대상 증거: 19건(조건별) + A-06 수치 재현 2건 + `--help` 실행 1건 + 봉인·재봉인 대조
- 무효 판정: 0건
- 셸 스니펫 실행 검증: 계약 지정 측정 명령 전부 zsh(현재 셸)로 직접 실행. markdownlint는
  scratchpad에 재설치 없이 기존 설치본 재사용해 재실행
- 양성 대조: SC-01/SC-02는 Iteration 3에서 이미 확인된 임시 파일 재현(이번엔 재실행하지
  않음 — 판정 로직 자체가 2831bcb로 바뀌지 않았음을 diff로 직접 확인했으므로 결합 재확인
  불필요). AR-03(iii)은 이번에도 계약 63개 전체에 verify_seal 재실행해 SEAL_BROKEN 0건 확인
- 무효 0건 — 미검증 카운터 변화 없음

## Summary
- Total: 19/19 conditions passed
- Verdict: APPROVE
- 커밋 2831bcb(A-06 수정)는 19개 조건 중 어느 것도 FAIL로 돌리지 않았고, 사용자가 요청한
  AR-01·SK-01·DG-02 무영향과 `--help` 실행 결과, A-06의 수치 주장(84줄·9파일 / 136줄·26파일)을
  전부 직접 재현해 사실임을 확인했다

## Improvement Suggestions
- [AR-02] 범위-미명시 — 기준 문서(`plugin-validation-guide.md`) 안에서 개수 표기가 여러 곳에
  흩어져 있다는 갭이 Iteration 3부터 남아 있다(A-05가 자체 기록). 다음 계약에서 "기준 문서
  안에서도 특정 헤더 한 곳에만 등장"처럼 문서 내부 단일화까지 재는 조건을 명시할 것을 권고
- [ER-02/AR-02] 측정-방식-불일치 — Iteration 3에서 이미 지적됨(A-01→A-03). 다음부터는 처음부터
  검사 번호 표기(`V1~VN`)만 재고 "N 카테고리"류는 애초에 재는 낱말 후보에서 제외할 것
- [일반] 이번 스프린트는 APPROVE 이후에도 두 차례(A-04, A-06) 부모 교차 진단이 실물 결함·사실
  오류를 찾아 추가 커밋으로 이어졌다. 두 경우 모두 계약 조건 판정 자체는 흔들리지 않았지만,
  "APPROVE 후 교차 진단 결과를 계약 범위 안에서 즉시 반영"하는 패턴이 이 스프린트에서 3회
  반복됐다(A-04, A-05, A-06) — 계약 결함이라기보다 이 검사(V10) 자체가 처음 만들어지는
  스프린트라 발견 곡선이 길었던 것으로 보인다. 다음 신규 검사 추가 스프린트에서도 유사 패턴을
  예상하고 여유를 둘 것

## References
- 계약: .harness/sprint-contract-check-count-decouple-and-table-gate.md
- 개정: .harness/sprint-amendments-check-count-decouple-and-table-gate.md (A-01~A-06)
- 검사 스크립트: scripts/validate-plugin.py
- 기준 문서: harness/docs/guides/plugin-validation-guide.md
- 이번 재평가 대상 커밋: 2831bcb (Iteration 3 APPROVE 이후 사실 오류 정정)
