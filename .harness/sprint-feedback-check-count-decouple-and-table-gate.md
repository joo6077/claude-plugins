# Sprint Feedback
Feature: 검사 개수를 지시문에서 떼어내고 표 무결성 검사를 추가
Evaluated: 2026-09-24 12:50
Verdict: APPROVE
Iteration: 3

## Contract Fingerprint
- path: /Users/jackson/Hub/10_Dev/claude-plugins/.harness/sprint-contract-check-count-decouple-and-table-gate.md
- sha256: 074c59853f26389e9360f9eb96db518683bc362516951df0dea8f8ca9dde673b
- status: done (앞 iteration 2 APPROVE 때 이미 전환됨 — 이번 재평가로 새로 바꾸지 않는다)
- slug: check-count-decouple-and-table-gate
- contract_root: /Users/jackson/Hub/10_Dev/claude-plugins
- contract_root_unconfigured: false
- 선택 근거: 사용자가 계약 절대경로를 명시 (ladder 1)
- legacy_contract_used: false
- seal_status: SEAL_OK
- contract_seal_broken: n/a
- 재확인(Step 5): 일치 (평가 시작·종료 시점 sha256 동일)
- 봉인 커밋 대조(1-e-3): 봉인 커밋 2ae9794 이후 계약 파일 diff는 frontmatter `status: active -> done` 한 줄뿐. 조건 줄·산문 전부 봉인 시점과 동일. `reseal_detected: false`
- status_transition: skipped (verdict=APPROVE 이지만 status 가 이미 done — 전환 대상 아님)

## 재평가 배경 — 구현이 바뀐 이유 직접 확인

Iteration 2 APPROVE 뒤 부모 교차 진단이 V10(`check_v10_table_integrity`)의 코드 판정 결함을
짚었다 — `startswith` 만 써서 들여쓴 표 행(목록·인용 안에 들어간 표)을 못 봤다는 지적이다.
아래를 직접 재현해 확인했다.

- `git show 57fdcb3:reflect-kit/skills/reflect-promote/SKILL.md` 를 떠서 확인: 8행 표(헤더+구분선+행0~3) 뒤에
  `**규칙 #3 판정 근거**: …` 산문 한 문단이 끼어들고 그 뒤에 행4~7이 헤더 없이 이어졌다 — 실제로 깨진 표였다.
- `git show 04e49f6:reflect-kit/skills/reflect-promote/SKILL.md` 확인: 그 산문이 표 뒤로 옮겨져 8행이 하나의
  표로 복원됐다.
- 고친 `check_v10_table_integrity`(현재 `scripts/validate-plugin.py:760`)는 `line.strip().startswith("```")`로
  코드펜스를 판정하고(V6과 동일 기준), 표행 판정 시 `line.lstrip()`을 써서 들여쓴 표도 본다.
- 되돌린 판(`57fdcb3` 버전)에 현재 V10을 걸면 `reflect-promote/SKILL.md:66`에서 FAIL, `Exit 2`가 남을
  것이므로(코드 경로 직접 확인), 그 파일을 고치지 않으면 이 스프린트가 만든 검사 자신이 CI를 막는다.
  A-04가 그 파일을 AR-01 허용 목록에 추가한 이유이며, 정당하다.

## Amendments

- amendments: 5건 (A-01~A-05, 번호 중복 없음 — `grep -n '^## A-'` 확인)
- PASS 근거 가능: 2건 — A-03(ER-02·AR-02 측정 좁힘), A-04(AR-01 허용 목록 22개로 확장)
- PASS 근거 불가 조합: 0건
- A-01: 정보성 보고 (오탐 발견 서술). direction=`unchanged`. 판정에는 A-03이 대체
- A-02: 구현 중 사소 수정 3건. 조건 판정 무관
- A-03: `amend_direction_oracle` — 재는 낱말집합 {10 카테고리, V1~V10, V1-V10} → {V1~V10, V1-V10}.
  직접 계산: `removed=1 added=0` → **relaxing** (측정 집합이 준 것이므로 `amend_direction_oracle`이
  맞는 헬퍼 — 자기신고 아님, 계산 확인함). consent=`anchored` —
  세션 기록의 `AskUserQuestion` 쌍을 내가 직접 파싱해 확인: header="REJECT 처리",
  call=2026-09-24T02:34:33.381Z, answer=2026-09-24T02:34:43.593Z, session=f5b7f3a5-...,
  cwd=/Users/jackson/Hub/10_Dev/claude-plugins — 개정 문서의 기재와 정확히 일치.
  순서 확인: 동의(02:34:43.593Z) < 그 개정을 구현한 커밋 f68963d(2026-09-24T11:35:45+09:00=02:35:45Z).
  시간 역전 없음. → PASS 근거로 사용 가능(표: relaxing×anchored)
- A-04: `amend_direction` — 허용 파일 집합(AR-01) 21개 → 22개, `comm` 계산: `added=1 removed=0` →
  **relaxing**. consent=`anchored` — 이번엔 두 출처를 모두 확인했다: (1) 세션 기록의 `type=user`
  메시지(시각 2026-09-24T03:34:07.454Z, 내용 "…: 개정으로 1개 추가 (추천)") (2) 같은 내용이
  reflect-kit prompt 로그 `~/.claude/logs/claude-plugins/2026-09.md:63689`에
  `## [prompt] 2026-09-24T12:34:07+0900` + `- session:` + `- cwd:` 형식으로 그대로 존재 —
  스키마가 요구하는 "reflect-kit prompt 로그" 출처와 정확히 일치한다(개정 문서가 "세션 기록에서
  뽑았다"고 적었지만 실제로는 두 출처 모두에서 확인되므로 분류가 맞다).
  순서 확인: 동의(03:34:07.454Z) < 구현 커밋 04e49f6(2026-09-24T12:35:20+09:00=03:35:20Z),
  74초 앞섬. 시간 역전 없음. → PASS 근거로 사용 가능(표: relaxing×anchored)
- A-05: 판정 뒤 고친 것 3건(코드펜스 판정 기준 통일, 서술 오류 정정, `--help` 옛 개수 제거).
  조건 판정 결과에 영향 없음(각주 처리)

## User Correction Audit

- correction_log_status: available (`~/.claude/logs/claude-plugins/2026-09.md`)
- unreflected_corrections: 0 — 이번 재평가 구간의 사용자 발언은 위 A-03·A-04 동의로 전부
  사이드카에 반영되어 있다
- verdict 영향: 없음 (표면화 전용)

## Cross-Diagnosis Handoff

- 상태: pending-parent
- 부모가 띄울 때 넘길 것: 계약 절대경로
  `/Users/jackson/Hub/10_Dev/claude-plugins/.harness/sprint-contract-check-count-decouple-and-table-gate.md`
  · 이 판정 결과 전문
- 부모가 물을 두 가지:
  1. 계약 조건의 원래 의도와 다르게 해석해 PASS/FAIL 을 오판한 조건이 있는가? (특히 AR-01·ER-02·AR-02의
     amendment 적용 판정)
  2. 0 건·빈 출력을 근거로 PASS 한 조건(SK-01·ER-02·AR-02·AR-03) 중, 문제가 있어도 0 을 냈을
     측정(공허한 통과)이 있는가?
- 부모가 교차 진단을 마친 뒤 `cross_diagnosis_by` 를 `sprint-contract` 로 갱신한다.

## Results

### Skill (3/3)
- [x] SK-01: 21개 파일 중 기준 문서를 뺀 20개(.py 제외 19개)에 개수·범위 표기 0줄 — PASS
  - 근거: L3. 계약 지정 측정 명령 직접 실행 → `총=0 대상=19`. 개별 파일 스캔 결과에서
    양성 매치 0건 확인 (grep -c '9 카테고리\|9-카테고리\|V1~V9\|V1-V9')
- [x] SK-02: 검사 목록을 얻는 명령이 지시문에 실려 있다(최소 3개 파일) — PASS
  - 근거: L3. `.claude/skills/design-kaizen/SKILL.md`, `.claude/skills/rust-kaizen/SKILL.md`,
    `.claude/skills/tone-kaizen/SKILL.md` 3개 파일에 `check_v[0-9]` 패턴 각 1건 확인
    (요구 최소 3개 충족)
- [x] SK-03: sprint-contract/SKILL.md 의 병합 서술이 재배치를 인정하고 위험을 구별 — PASS
  - 근거: L3. `harness/skills/sprint-contract/SKILL.md:746-752` 직접 Read.
    `재배치` 4건, 같은 문맥에 "`main` 이 앞서 있으면" · "해시가 바뀌어" 명시. 위험(인용 해시가
    조상 아니게 됨)을 정확히 서술함

### Script (2/2)
- [x] SC-01: `validate-plugin.py`에 표 무결성 검사가 V10으로 등록되고 돌아간다 — PASS
  - 근거: L3. (a) `grep -c 'def check_v10' scripts/validate-plugin.py` = 1
    (실제 함수명 `check_v10_table_integrity`, 부분 일치로 조건 문구 충족)
    (b) `grep -oE '"[a-z-]+": check_v10'` = 1건 (`"table-integrity": check_v10`)
    (c) `python3 scripts/validate-plugin.py --check=table-integrity` → 14 plugins 14 OK
    양성 대조 직접 재현: `git show ac77cdc:harness/references/contract-schema.md` 를
    임시 파일로 떠서 검사하니 `FAIL …:1036 — 헤더 없이 끊긴 표 행` 1건 정확히 재현.
    확인 뒤 즉시 삭제, `git status --porcelain` 로 흔적 없음 확인
- [x] SC-02: `python3 scripts/validate-plugin.py` 전체가 14 plugins 14 OK Exit 0 — PASS
  - 근거: L3. 직접 실행 → `Total: 14 plugins, 14 OK` / `Exit: 0`.
    음성 대조 직접 재현: 위 임시 파일 존재 상태에서 전체 실행 →
    `Total: 14 plugins, 13 OK, 1 ERROR` / `Exit: 2` (V10이 정확히 FAIL을 유발함을 확인).
    파일 삭제 후 재실행 → 다시 14 OK 로 복구 확인

### Error (2/2)
- [x] ER-01: V10 대상 범위가 V6보다 넓고 이유가 적혀 있다 — PASS
  - 근거: L3. `check_v10_table_integrity` 함수 내 `docs/**/*.md` glob 포함(문자열 "docs" 3회
    등장 — `ctx.kit_path.glob("docs/**/*.md")` 및 docstring 2곳).
    `harness/docs/guides/plugin-validation-guide.md:450-453` (### V10 마크다운 표 무결성 절)에
    이유 서술 확인 — A-05가 고친 정정판("표가 끊긴 자리는 원래 V6 범위 안이었고, 넓힌 이유는
    같은 종류 문서가 docs/에도 있어서")이 실제로 반영되어 있음을 직접 Read로 확인
- [x] ER-02: 개수 표기를 지운 자리가 "등록된 검사 전부" 식으로 바뀌었다 (개수 신규 박기 없음) — PASS
  - 근거: L3 (amendment A-03 적용). 좁힌 측정 명령(`grep -c 'V1~V10\|V1-V10'`)을 20개 파일에
    직접 실행 → `총=0`. A-03의 direction·consent 검증은 위 Amendments 절 참조

### Architecture (4/4)
- [x] AR-01: 변경 파일이 21개 경로와 정확히 일치 (amendment A-04 적용 시 22개) — PASS
  - 근거: L3. `sprint_head` 해석 → `04e49f6`(UNRESOLVED 아님, STALE_HEAD 아님).
    `git diff --name-only c0e12a8..04e49f6 -- . ':(exclude).harness/**'` → 정확히 22행,
    전부 원 21개 목록 + `reflect-kit/skills/reflect-promote/SKILL.md`(A-04로 추가된 1개)와
    1:1 일치. A-04의 direction·consent 검증은 위 Amendments 절 참조
- [x] AR-02: 기준 문서가 개수를 적는 유일한 자리 (그 밖 20개는 0) — PASS
  - 근거: L3. `plugin-validation-guide.md`에 `V1~V10` 2건 확인. `scripts/validate-plugin.py`
    포함 나머지 19개(+py) 파일에서 `V1~V10\|V1-V10` 0건. (참고: 가이드 문서 안에 "카테고리"
    관련 표기가 4곳 있다는 A-05의 자기 신고를 직접 확인했으나, AR-02 조건 문구는 "그 문서
    밖 0건"만 요구하므로 문자 그대로 PASS. 이 문서-내부-단일화 갭은 이미 A-05가
    "다음 스프린트로 남기는 것"에 기록해 뒀다 — 계약 갭이지 이번 조건의 미충족이 아님)
- [x] AR-03: 손대지 않기로 한 것이 변경되지 않았다 — PASS
  - 근거: L3. `git diff c0e12a8..04e49f6 -- harness/evals/` = 0행,
    `-- docs/kaizen/` = 0행. `verify_seal`을 `find .harness -name 'sprint-contract*.md'`
    (maxdepth 없음) 전체에 실행 → `SEAL_OK 63 · SEAL_ABSENT 10 · SEAL_BROKEN 0`
- [x] AR-04: 이 계약 자신이 봉인 커밋 절차를 따랐다 — PASS
  - 근거: L3. `git log --diff-filter=A -- .harness/sprint-contract-check-count-decouple-and-table-gate.md`
    → 첫 커밋 `2ae9794`. `git show --name-only --format='' 2ae9794` → 파일 1개
    (`.harness/sprint-contract-check-count-decouple-and-table-gate.md`)

### Anti-patterns (2/2, + 프로젝트 공통 AP-01·AP-02 위반 0건)
- [x] AP-03: bare code fence 0건(V6 대상) — PASS
  - 근거: L3. `python3 scripts/validate-plugin.py --check=code-fence` → 14 plugins 14 OK
- [x] AP-04: frontmatter 보존, V1 FAIL 0건 — PASS
  - 근거: L3. `python3 scripts/validate-plugin.py --check=frontmatter` → 14 plugins 14 OK
- 프로젝트 공통 anti_patterns(project.yaml) AP-01(hardcoded version)·AP-02(force push):
  변경 파일 22개 전체에 패턴 검색 → 0건. 대상 파일 수 > 0 확인(공허한 0 아님)

### Reusability (2/2)
- [x] RE-01: V10이 기존 검사(V6·V9)와 같은 시그니처·형태를 따른다 — PASS
  - 근거: L3. `def check_v10_table_integrity(ctx: CheckContext) -> CheckResult:` 시그니처가
    `check_v6_code_fence`·`check_v9_arg_substitution`과 동일. 함수 내 `ctx.read`·`CheckResult`
    각 사용 확인
- [x] RE-02: 판정 로직이 `validate-plugin.py` 한 곳에만, 기준 문서는 가리키기만 — PASS
  - 근거: L3. `grep -c '^def ' harness/docs/guides/plugin-validation-guide.md` = 0

### Diagnostics (2/2, N/A 2)
- [x] DG-01: N/A — 근거 확인: AR-01의 22행에 `scripts/release.sh` 0건 (사유 사실과 일치)
- [x] DG-02: 편집기 조건 마크다운 경고가 기준값 이내 — PASS
  - 근거: L3. scratchpad에 `markdownlint-cli2@0.23.2` 설치, `{"config":{"MD013":false}}` 설정으로
    대상 20개 .md 파일에 직접 실행(zsh unquoted 변수 word-split 실패를 발견해 xargs로 우회 —
    최초 시도 "Linting: 0 files" 였던 것을 원인 규명 후 재실행).
    결과: 총 347건, (파일,규칙) 조합 49개 — 계약의 봉인 전 기준값(347건·49조합)과 정확히 일치.
    조합별 개수까지 산출해 통합 목록으로 확인(늘어난 조합 0개)
- [x] DG-03: N/A — DG-01과 동일 사유·측정
- [x] DG-04: N/A — SC-02가 실질 검사 역할 수행(위에서 PASS 확인)

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
- 없음 (사용자로부터 별도 실패 보고 없음. 이번 재평가는 부모 교차 진단이 짚은 코드 결함에 대한
  자발적 수정이며, 위 "재평가 배경"에서 직접 재현·확인함)

## Evidence Validity
- 검사 대상 증거: 19건 (조건별) + amendment 2건(A-03·A-04) + 봉인·재봉인 대조
- 무효 판정: 0건
- 셸 스니펫 실행 검증: 실행 다수건, zsh 문제 1건 직접 발견 및 우회 확인 (DG-02 측정 시
  `$FILES` unquoted 변수를 zsh에서 word-split 안 해 "Linting: 0 files"로 죽는 것을 발견 →
  xargs로 재실행하여 정상 측정값 획득. contract-schema §셸 이식성 규약이 경고하는 바로 그 함정)
- 양성 대조: SC-01/SC-02 — `ac77cdc:harness/references/contract-schema.md`를 임시 파일로 사용해
  1건 FAIL·Exit 2 재현 확인 후 즉시 삭제. AR-03(iii) — 계약 63개 전체에 verify_seal 실행해
  SEAL_BROKEN 0건 확인(양성 대조: SEAL_BROKEN을 낼 변조 파일은 만들지 않음 — 이미 이 레포에
  SEAL_ABSENT 10건이 실재해 verify_seal 함수 자체의 판별력은 별도로 검증됨)
- 추가 실행: V10 개선판의 오탐 여부를 직접 검증하기 위해 인용문 표·목록 내 들여쓴 표·HTML 표·
  표 뒤 각주·4중 백틱 안 3중 백틱 5개 합성 사례를 `probe-kit/`에 만들어 `check_v10_table_integrity`를
  직접 호출·검사함. 결과: 4개는 정확히 판정(오탐 없음), 1개(4중 백틱 안 3중 백틱)는 FAIL 오탐 —
  단, 이는 A-05가 "다음 스프린트로 남기는 것" 3번에 이미 명시적으로 기록한 기존 한계이고 실제
  210개 파일 코퍼스에는 해당 패턴이 0건이라 이번 조건(SC-02: 14 OK)에는 영향 없음. 확인 후
  `probe-kit/` 즉시 삭제, `git status --porcelain`으로 흔적 없음 확인
- 무효 0건 — 미검증 카운터 변화 없음

## Summary
- Total: 19/19 conditions passed
- Verdict: APPROVE

## Improvement Suggestions
- [AR-02] 범위-미명시 — 기준 문서(`plugin-validation-guide.md`) 안에서 개수 표기가 4곳
  (줄 10, 27, 599, 629)에 흩어져 있다. 계약은 "한 곳에만"이라 서술했으나 측정 조건은 그것을
  재지 않는다. 다음 계약에서는 "기준 문서 안에서도 §3 헤더 한 곳에만 등장"처럼 문서 내부
  단일화까지 재는 조건을 명시할 것을 권고 (A-05가 이미 이 갭을 자체 기록해 둠 — 구현 결함이
  아니라 계약 결함)
- [ER-02/AR-02] 측정-방식-불일치 — 이번 계약이 A-01→A-03 두 단계를 거쳐 "10 카테고리"를
  재는 낱말에서 빼는 데 도달했다. 다음부터는 처음부터 검사 번호 표기(`V1~VN`)만 재고,
  "N 카테고리" 류는 이 레포에서 감사 카테고리(backend/infra-kit 10종)와 항상 겹치므로
  애초에 재는 낱말 후보에서 제외할 것

## References
- 계약: .harness/sprint-contract-check-count-decouple-and-table-gate.md
- 개정: .harness/sprint-amendments-check-count-decouple-and-table-gate.md (A-01~A-05)
- 검사 스크립트: scripts/validate-plugin.py
- 기준 문서: harness/docs/guides/plugin-validation-guide.md
