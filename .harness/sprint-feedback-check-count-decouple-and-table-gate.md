# Sprint Feedback
Feature: 검사 개수를 지시문에서 떼어내고 표 무결성 검사를 추가
Evaluated: 2026-09-24 12:10
Verdict: REJECT
Iteration: 1

## Contract Fingerprint
- path: /Users/jackson/Hub/10_Dev/claude-plugins/.harness/sprint-contract-check-count-decouple-and-table-gate.md
- sha256: 320dbcf1f2c4304650e35cc1edf01582bfcc2f1dfc23cdaade530d302582b299
- status: active
- slug: check-count-decouple-and-table-gate
- contract_root: /Users/jackson/Hub/10_Dev/claude-plugins
- contract_root_unconfigured: false
- 선택 근거: ladder 2 세션소유 (owner_session == CLAUDE_CODE_SESSION_ID == f5b7f3a5-c03d-452b-b44b-fc3d15dcd1a0, 명시 경로도 사용자가 함께 지정해 일치)
- legacy_contract_used: false
- seal_status: SEAL_OK
- contract_seal_broken: n/a
- 재확인(Step 5): 일치 (sha256/status 동일)
- status_transition: skipped (verdict=REJECT status=active) — REJECT 는 재평가 대상이므로 active 유지

### 1-e-3 봉인 커밋 대조 (2026-09-24 신규 절차 검증)
- seal_commit: 2ae9794 (`git log --diff-filter=A` 로 확인한 첫 커밋)
- seal_commit_files: 1 (`git show --name-only --format='' 2ae9794` → 계약 파일 1개만)
- 산문 diff (조건 줄·status 전환 제외): 없음 (`git diff 2ae9794 -- $CONTRACT` 자체가 빈 출력 — 봉인 이후 파일이 전혀 바뀌지 않음)
- conditions_digest diff: 없음
- supersedes_digest / supersedes_commit: 0건 (필요 없음 — 재봉인 없음)
- 판정: 산문 변조 없음, 조용한 재봉인 없음 — 경고 대상 아님
- **status 전환 예외 동작 검증**: 이번 계약은 iteration 1 이라 실제 active→done 전환 사례가 없어 직접 관측은 불가. 대신 필터 로직만 따로 떼어 합성 입력으로 검증했다 (레포 파일은 건드리지 않음) — `status: active`→`status: done` 줄과 조건 체크박스 줄을 섞은 가짜 diff를 파이프로 흘려보내니 `grep -vE '^[+-]status: (active|done)$'` 필터가 그 두 줄만 정확히 걸러내고 순수 산문 변경 줄만 남겼다. 필터 자체는 의도대로 동작한다.

## Amendments
- amendments: 2건 (A-01, A-02) — 둘 다 조건 문구 자체를 바꾸는 요청이 아니라 사실 보고다
- A-01 (ER-02 측정 오탐 보고): direction=unchanged (조건을 고치지 않음, PASS/FAIL 주장 없이 판정을 QA에 위임), consent=n/a — PASS 근거로 쓸 수 없음(애초에 PASS를 주장하지 않음). 아래 ER-02/AR-02 판정에서 원 조건 문자 그대로 적용
- A-02 (구현 중 사소한 서식 수정 3건): direction=n/a, consent=n/a — 조건 판정에 영향 없는 정보성 기록. DG-02 측정으로 직접 재확인함 (아래 참조)
- PASS 근거 가능: 0건
- PASS 근거 불가: 0건 (애초에 PASS 주장이 없으므로 "사용자 확인 필요" 목록에 올릴 것도 없음)
- 집합형 direction 계산 결과: 해당 없음 (경로 집합을 바꾸는 amendment 아님)

## User Correction Audit
- correction_log_status: available (`~/.claude/logs/claude-plugins/2026-09.md`, 63668줄)
- 스프린트 기간: 계약 created 2026-09-24 11:20 ~ 평가 시각 2026-09-24 12:10
- unreflected_corrections: 0 (그 구간에 `[prompt]` 항목 없음 — 마지막 prompt 로그는 11:07:00 로 계약 생성 이전. 구현 단계는 `[tool-failure]` 로그만 있고 세션은 동일 f5b7f3a5)
- verdict 영향: 없음 (표면화 전용)

## Cross-Diagnosis Handoff

> 이번 호출은 구현 판정이다. 지시문 개정(harness/agents/qa-evaluator.md)에 따라 Step 7 을 이 에이전트가
> 직접 수행하지 않는다 — Agent 도구를 띄우지 않았다.

- 상태: pending-parent
- 부모가 띄울 때 넘길 것: 계약 절대경로 `/Users/jackson/Hub/10_Dev/claude-plugins/.harness/sprint-contract-check-count-decouple-and-table-gate.md` · 이 리포트 전문(verdict + 조건별 PASS/FAIL + 증거)
- 부모가 물을 두 가지:
  1. 계약 조건의 원래 의도와 다르게 해석해 PASS/FAIL 을 오판한 조건이 있는가? — 특히 ER-02·AR-02 를 "문자 그대로 FAIL" 로 판정한 것이 맞는지 (아래 근거 참조. 조건 취지는 만족하지만 조건 문구 그대로의 측정은 실패)
  2. 0건·빈 출력을 근거로 PASS 한 조건 중, 문제가 있어도 0을 냈을 측정(공허한 통과)이 있는가? — SK-01/AR-01/AR-02/ER-02 는 양성·음성 대조를 직접 실행해 확인했으므로 우선순위 낮음
- 부모가 교차 진단을 마친 뒤 `cross_diagnosis_by` 를 `sprint-contract` 로 갱신한다. 끝내 못 띄웠으면 `none`.

## Results

### Skill (3/3)
- [x] SK-01: 21개 파일 중 기준 문서를 뺀 20개(스크립트 .py 제외 시 실측 대상 19개)에 개수·범위 표기 0줄 — PASS
  - 근거: 지정된 측정 스크립트를 bash·zsh 양쪽에서 실행 → `총=0 대상=19` (양쪽 동일). 양성 대조로 봉인 전 상태(c0e12a8)에 같은 스크립트를 걸어 `총=32`(19파일 중 18파일 매치)를 확인 — 측정이 살아있음을 확인. L3
- [x] SK-02: 검사 목록을 얻는 명령이 지시문에 실려 있다 — PASS
  - 근거: `grep -Fc 'check_v[0-9]'` 가 `.claude/skills/design-kaizen/SKILL.md:46`, `.claude/skills/rust-kaizen/SKILL.md:110`, `.claude/skills/tone-kaizen/SKILL.md:77` 3개 파일에서 매치(요구 최소 3개 충족). 그 명령(`grep -oE '"[a-z-]+": check_v[0-9]+' scripts/validate-plugin.py | sed -E 's/"([a-z-]+)".*/\1/'`)을 bash·zsh 양쪽에서 직접 실행 → 10개 검사 이름(`table-integrity` 포함) 정상 출력. L3
- [x] SK-03: `sprint-contract/SKILL.md` 병합 서술이 재배치도 인정하고 위험을 구별한다 — PASS
  - 근거: `harness/skills/sprint-contract/SKILL.md:746-754` — "세 방식(병합 커밋·스쿼시·재배치)을 모두 허용... `--rebase`(재배치)로 병합한다 — 둘 다 봉인 커밋의 파일 1개를 지킨다... **재배치의 위험은 다른 데 있다** — `main`이 앞서 있으면 커밋 해시가 바뀌어..." — "main 이 앞서" 문구 존재 확인(`grep -Fc '재배치'`=4). L3
  - 참고(계약 품질 메모, 판정에 영향 없음): 조건의 양성 대조 문구는 "고치기 전 재배치는 0건"이라 적혀 있으나, 실측(c0e12a8)은 1건(세 방식을 나열하며 "재배치"를 언급하되 해시 위험은 서술하지 않은 문장)이었다. 핵심 판정 기준(카운트≥1 및 "main 이 앞서" 존재)은 그대로 충족되므로 SK-03 자체는 영향 없음.

### Script (2/2)
- [x] SC-01: `scripts/validate-plugin.py`에 표 무결성 검사가 V10으로 등록됐고 돌아간다 — PASS
  - 근거: (a) `grep -c 'def check_v10' scripts/validate-plugin.py` = 1 (`def check_v10_table_integrity`) (b) `grep -oE '"[a-z-]+": check_v10' ...` = 1건(`"table-integrity": check_v10_table_integrity`) (c) `python3 scripts/validate-plugin.py --check=table-integrity` → 14 plugins 14 OK. 양성 대조: c0e12a8 시점 `check_v10` 0건 확인. **사용자 요청 특별 검증**: `git show ac77cdc:harness/references/contract-schema.md` 를 `harness/docs/tmp-qa-seal-check-DELETE-ME.md` 에 임시로 놓고 `python3 scripts/validate-plugin.py harness --check=table-integrity` 실행 → `1 broken table row(s)` / `FAIL ...:1036 — 헤더 없이 끊긴 표 행` 정확히 1건, 계약이 예고한 줄번호(1036)와 일치. 전체 실행 시 `Total: 1 plugins, 1 ERROR / Exit: 2`. 확인 직후 임시 파일 삭제, `git status --porcelain` 로 원상 복구 확인. L3
- [x] SC-02: 전체 실행이 `14 plugins, 14 OK · Exit: 0` — PASS
  - 근거: 현재 트리에서 `python3 scripts/validate-plugin.py` 실행 → 마지막 두 줄 `Total: 14 plugins, 14 OK` / `Exit: 0`. 음성 대조: 위와 같은 임시 파일을 넣고 전체 실행 → `Total: 14 plugins, 13 OK, 1 ERROR` / `Exit: 2` 로 깨짐 확인 후 즉시 제거, 재확인 결과 `14 plugins, 14 OK`로 복귀. L3

### Error (1/2)
- [x] ER-01: V10 대상 범위가 V6보다 넓고 이유가 적혀 있다 — PASS
  - 근거: `check_v10_table_integrity` 함수 안에 `docs` 문자열 3회 등장(주석 설명 + `docs/**/*.md` glob 코드). `harness/docs/guides/plugin-validation-guide.md:450-453` "**범위** — V6보다 넓다... 그래서 킷 안의 `docs/**/*.md`를 더한다. 실측 210파일에서 오탐 0을 확인한 뒤 도입했다." L3
- [ ] ER-02: 개수 표기를 지운 자리가 "등록된 검사 전부" 같은 개수 없는 표현으로 바뀌었다 — **FAIL**
  - 근거(측정값 우선): 조건이 명시한 측정 `grep -c '10 카테고리\|V1~V10\|V1-V10'` 을 대상 20개 파일 전부에 실행한 결과 **총=3 (기준: 0)** — `.claude/skills/backend-kaizen/SKILL.md:26`, `.claude/skills/infra-kaizen/SKILL.md:25`, `.claude/skills/rust-kaizen/SKILL.md:99`. 셋 다 감사(audit) 카테고리 명명 규칙("10 카테고리 명명 규칙")을 가리키는 문장으로, 검사 번호(V1~V10)와 무관하다. `git show 2ae9794~1`로 대조한 결과 세 줄 모두 이번 스프린트 이전부터 존재했다(구현이 새로 추가한 것이 아님). 좁힌 패턴(`V1~V10\|V1-V10`)만 쓰면 총=0.
  - 판정 이유: 이 계약은 문자 그대로 해석을 원칙으로 하고(핵심 원칙 2), 조건에 박힌 측정 문구 자체가 이번 조건이 승인받은 오라클이다(SEAL_OK, 봉인 이후 조건 줄 변경 없음). 측정이 "죽어서 항상 0을 내는" 경우가 아니라 — 양성 대조(임시로 `10 카테고리 (V1~V10)`을 넣으면 1이 나옴, A-01에서 확인)로 살아있는 측정임이 확인됐다 — 오히려 대상과 무관한 문맥에서 오탐(false positive)을 내는 것이므로, "측정이 죽었을 때"의 대체 측정 허용 규정(규칙 10)은 적용 대상이 아니다. 사이드카 A-01은 조건을 고치지 않고 판정을 QA에 위임했으며(direction=unchanged), 이는 "동의어/취지 충족을 이유로 완화 승인"이 아니다. 계약 용어와 측정이 어긋나는 경우 "동의어는 FAIL, 계약 수정 권장"이 표준 처리다.
  - 수정 방향: 다음 이터레이션에서 이 조건의 측정을 `grep -c 'V1~V10\|V1-V10'`(검사 번호 표기만)으로 좁히거나, 계약을 amendment로 좁혀 사용자 승인을 받는다.

### Architecture (3/4)
- [x] AR-01: 변경 파일이 21개 경로와 정확히 일치 — PASS
  - 근거: STALE_HEAD 아님 확인(`sprint_head`가 57fdcb3로 resolve, c0e12a8과 다름) 후 `git diff --name-only c0e12a8..57fdcb3 -- . ':(exclude).harness/**'` 실행 → 21행 출력, `diff <(sort 선언목록) <(sort 실제목록)` 완전 일치. L3
- [ ] AR-02: 기준 문서가 개수를 적는 유일한 자리가 됐다 — **FAIL**
  - 근거: 전반부(가이드 문서 자체에 `10 카테고리` 또는 `V1~V10` ≥1)는 충족 — `harness/docs/guides/plugin-validation-guide.md` 에서 2건(line 27, 623) 확인. 그러나 조건이 "ER-02와 같은 측정"이라고 명시한 후반부("그 문서 밖 20개 파일에는 0")는 ER-02와 동일한 이유로 **총=3**, 기준 0 미충족.
  - 판정 이유: ER-02와 같은 측정을 명시적으로 공유하는 조건이므로 같은 결론이 적용된다. 별도의 독립 해석을 만들지 않았다.
  - 수정 방향: ER-02와 동일 — 측정 패턴을 좁히거나 amendment로 사용자 승인.
- [x] AR-03: 손대지 않기로 한 것이 변경되지 않았다 — PASS
  - 근거: (i) `harness/evals/` 관련 변경 0행 (ii) `docs/kaizen/` 관련 변경 0행 (iii) 저장소 전체(-maxdepth 없이, 워크트리 포함) `sprint-contract*.md` 284개에 verify_seal 실행 → `SEAL_BROKEN` 0건(SEAL_OK/SEAL_ABSENT만 존재). L3
- [x] AR-04: 이 계약 자신이 봉인 커밋 절차를 따랐다 — PASS
  - 근거: `git log --diff-filter=A --format='%h' -- .harness/sprint-contract-check-count-decouple-and-table-gate.md` → `2ae9794`(첫 커밋), `git show --name-only --format='' 2ae9794` → 파일 수 1. L3

### Anti-patterns (2/2, 계약 조건 기준)
- [x] AP-03: bare code fence 0건 (V6 대상 7개: harness/skills/*/SKILL.md 6개 + flutter-kaizen) — PASS
  - 근거: `python3 scripts/validate-plugin.py --check=code-fence` → 14 plugins 14 OK, Exit 0. 양성 대조: 대상 7개 중 3개(create-skill=4줄, init=6줄, sprint-contract=38줄)에 실제 코드 펜스가 있어 검사가 공허하지 않음을 확인. L3
- [x] AP-04: frontmatter가 보존됐다 (V1 FAIL 0건) — PASS
  - 근거: `python3 scripts/validate-plugin.py --check=frontmatter` → 14 plugins 14 OK, Exit 0. L3

#### 참고: project.yaml 표준 안티패턴(계약 조건 아님, 부가 확인)
- AP-01(`hardcoded.*version`): 변경 파일 21개 전수 Grep → 0건
- AP-02(`git push.*--force`): 변경 파일 21개 전수 Grep → 0건

### Reusability (2/2)
- [x] RE-01: V10이 기존 검사와 같은 형태(시그니처/ctx.read/CheckResult) — PASS
  - 근거: `def check_v10_table_integrity(ctx: CheckContext) -> CheckResult:` (scripts/validate-plugin.py:760) — V6(`check_v6_code_fence`, :512), V9(`check_v9_arg_substitution`, :723)와 동일한 시그니처 패턴. 함수 본문에 `ctx.read`/`CheckResult` 3회 사용. L3
- [x] RE-02: 판정 코드가 validate-plugin.py 한 곳에만 있다 — PASS
  - 근거: `grep -nE '^\s*def [a-zA-Z_]+\(' harness/docs/guides/plugin-validation-guide.md` → 0건(파이썬 함수 정의 없음, 가이드는 서술로만 가리킴). 실제 판정 로직은 scripts/validate-plugin.py:760-825. L3

### Diagnostics (1/1, N/A 3건)
- N/A DG-01: `commands.analyze`(`bash -n scripts/release.sh`) 대상과 변경 파일 교집합 0 — 사유 사실 확인(`grep -c '^scripts/release.sh$'` AR-01 목록에서 0). N/A 처리.
- [x] DG-02: 편집기와 같은 조건 마크다운 경고가 기준을 넘지 않는다 — PASS
  - 근거: scratchpad에 `markdownlint-cli2@0.23.2`(npx) 설치, `{"config":{"MD013":false}}`로 대상 20개(.md, .py 제외) 전수 실행 → `Summary: 347 issues in 19 files`(기준 347 이하 충족, 정확히 동일). `파일 RuleID` 정규화 후 `sort|uniq -c` → 49개 조합(기준 49와 일치). 봉인 시점(c0e12a8)의 같은 20개 파일에 동일 설정으로 재실행한 baseline과 `diff` → **완전 동일(0줄 차이)**, 늘어난 조합 0개 확인. L3
- N/A DG-03: `commands.test`(`bash scripts/release.sh`) 대상과 변경 파일 교집합 0 — DG-01과 동일 근거로 사실 확인. N/A 처리.
- N/A DG-04: 실행 진입점 없음 — `scripts/validate-plugin.py`는 c0e12a8 시점에 이미 존재(신규 진입점 아님) 확인. 대체 조건 SC-02는 PASS. N/A 처리.

## Unverifiable Summary
- invalid_evidence: 0
- env_gaps: 0
- verified_coverage: (19 - 0) / 19 = 1.00 (임계 0.60 충족)
- 연속 ENV 승급: 없음
- Verdict 영향: 통상 (미검증 카운터가 verdict를 바꾸지 않음 — FAIL 2건 자체가 REJECT 사유)

## Discrimination (규칙 12 적용 조건 없음)
- 이번 19개 조건 중 규칙 12의 9항(동시성 가드·인증/권한·멱등성·입력 검증·데이터 유실·마이그레이션 안전성·재시도/중복제거·보안 경계·사용자 결함 보고 충돌)에 해당하는 조건 없음 — 전부 문서/스크립트 구조 검증. 해당 없음.

## User-Reported Failures
- 없음 (사용자 결함 보고 없음)

## Evidence Validity
- 검사 대상 증거: 19건(조건) + 부가 2건(AP-01/AP-02)
- 무효 판정: 0건
- 셸 스니펫 실행 검증: SK-01·SK-02 측정 스니펫을 bash·zsh 양쪽에서 실행해 동일 결과 확인(2건). 그 외 조건은 대부분 zsh(사용자 셸) 단일 실행 + 결과 명시적 수치 확인.
- 양성 대조: SK-01(19파일/32건, 봉인 전), SK-03(재배치 1건 실측 — 계약 주장과 다름, 위 참고 메모 참조), SC-01(check_v10 0건 봉인 전 + 임시 파일로 1036행 1건 재현), AP-03(대상 7개 중 3개 실제 코드펜스 보유), ER-02/AR-02(계약 A-01에 기록된 양성 대조를 직접 실행하지 않고 A-01 서술을 근거로 인용 — 임시 파일로 직접 재현하지는 않았으나 A-01의 grep 결과 자체는 본 리포트에서 동일 패턴으로 재현 완료)
- 무효 0건은 미검증 카운터에 합산 없음

## Summary
- Total: 14 PASS / 2 FAIL / 3 N/A (19 conditions)
- Verdict: **REJECT**
- FAIL 항목: ER-02(개수 표기 잔존 — 조건 문구 그대로의 측정 기준), AR-02(같은 측정을 공유하는 후반부 조건)
- 수정 우선순위: 두 FAIL은 구현 결함이 아니라 계약의 측정 문구가 과대추출(over-broad)하는 문제다. (1) 조건 SK-01/ER-02/AR-02가 재는 패턴 중 `10 카테고리` 절반을 삭제하고 `V1~V10\|V1-V10`만 남기도록 amendment 또는 재계약, (2) 그 좁힌 패턴으로 재측정하면 두 조건 모두 0 → PASS 전환 가능. 구현 자체(`scripts/validate-plugin.py`, 21개 문서 수정)는 나머지 17개 조건에서 결함 없이 확인됨.

## Improvement Suggestions
- [ER-02] 측정-방식-불일치 — 측정을 `grep -c '10 카테고리\|V1~V10\|V1-V10'`에서 `grep -c 'V1~V10\|V1-V10'`(검사 번호 표기만)로 좁힌다. "10 카테고리"는 backend/infra-kaizen의 감사 카테고리 명명 규칙과 rust-kaizen의 sibling 참조에서 이미 쓰이는 무관한 문구다.
- [AR-02] 측정-방식-불일치 — ER-02와 동일한 측정을 공유하므로 동일하게 좁힌다. 두 조건이 같은 오탐을 공유한다는 사실 자체를 계약에 "같은 측정 재사용" 각주로 남겨, 다음에 한쪽만 고치고 한쪽을 놓치는 일을 방지한다.
- [SK-03] 측정-환경-오염 — 조건의 양성 대조 문구("고치기 전 재배치는 0건")가 실측(1건)과 다르다. 다음 계약 작성 시 양성 대조 수치도 반드시 봉인 전 실측값을 그대로 적어야 한다(이미 이번 스프린트가 이 규칙을 세웠는데 SK-03 작성 시 재적용을 놓쳤다).
