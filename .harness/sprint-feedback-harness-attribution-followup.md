# Sprint Feedback
Feature: harness 스프린트 귀속 기록 + 계약 결함 사이드카
Evaluated: 2026-09-06 14:40
Verdict: REJECT
Iteration: 1

## Contract Fingerprint
- path: .harness/sprint-contract-harness-attribution-followup.md
- sha256: 3525f6b048addfa2310ceef32c1ad4f7d5e4d474fe9886e56059dd425eb6ec9d
- status: active
- slug: harness-attribution-followup
- contract_root: /Users/jackson/Hub/10_Dev/claude-plugins
- contract_root_unconfigured: false
- 선택 근거: ladder 1 명시경로 (owner_session 도 현재 세션과 일치 — ladder 2 로도 유일 성립)
- legacy_contract_used: false
- seal_status: SEAL_OK
- contract_seal_broken: n/a
- 재확인(Step 5): 일치 (FINGERPRINT OK)
- status_transition: skipped (verdict=REJECT status=active)

## Amendments
- amendments: 2 (사이드카 2 파일: sprint-amendments-harness-core-defects.md 의 AM-01/AM-02, sprint-amendments-harness-attribution-followup.md 의 AM-01)
- PASS 근거 가능: 0 (이 계약 15 조건 중 어느 것도 amendment 를 PASS 근거로 쓰지 않았다 — AR-01/DG-04 는 계약 원문 그대로 판정)
- PASS 근거 불가/해당없음: 2
  - [narrowing · unanchored · 대상=harness-core-defects AR-03] 이 계약 조건이 아니라 선행 계약(done) 소관 — 정보성
  - [기록 전용(direction 없음) · unanchored · 대상=이 계약 AR-01·DG-04] "조건 문구 불변 → PASS 집합 불변" 이라는 작성자 자체 주장. 검증 결과 이 주장은 사실이었다(계약 원문 변경 없음, SEAL_OK) — 그러나 이것이 AR-01/DG-04 를 PASS 시키는 근거는 되지 않는다. 원 조건은 여전히 원문 그대로 판정해야 하고, 아래 Results 에서 직접 재측정한 결과 둘 다 FAIL이다
- 집합형 direction 계산 결과 (harness-core-defects AM-01): `narrowing added=0 removed=2` (원 8개 파일 → 개정 6개 파일, 자기신고 아닌 집합 비교로 명시)
- 집합형 direction 계산 결과 (이 계약 AM-01): 작성자 주장 `added=0 removed=0`(조건 집합 불변) — verify_seal SEAL_OK 로 교차 확인됨(조건 줄 미변경 사실 자체는 참)

## User Correction Audit
- correction_log_status: available (/Users/jackson/.claude/logs/claude-plugins/2026-09.md)
- unreflected_corrections: 0 (세션 44c7700e 의 2026-09-06 12:30~14:31 프롬프트 5건 확인 — "돌려"/"1 a"/"다 됏음"/"열려잇는거까지 다 진행해" 등 방향 교정 성격 발언 없음)
- verdict 영향: 없음 (표면화 전용)

## Results

### Skill (3/3)
- [x] SK-01: 귀속 기록물 `.harness/sprint-amendments-harness-core-defects.md` 존재 + 결함 3종 각 조건ID 동반 기록 — PASS
  - 근거(L3): 파일 존재 확인. `grep -c "측정-상태-모호"`=1(라인42, AR-03 동반), `grep -c "측정-산출물-부재"`=1(라인43, DG-04 동반), `grep -c "범위-미명시"`=1(라인44, AR-02 동반). 3종 모두 >=1 기준 충족, 3종 모두 조건ID 와 같은 표 행에 존재
- [x] SK-02: 사이드카 direction 이 자기신고가 아니라 집합 비교로 산출 — PASS
  - 근거(L3): `sprint-amendments-harness-core-defects.md:8` `## AM-01 — narrowing`, `:19` `**direction 산출** (자기신고 아님 · 집합 비교):`, `:22-24` `원 집합 8 / 개정 집합 6 / added=0 · removed=2 → narrowing`. direction 필드 1건 + 산출 근거 문장 1건 이상 확인
- [x] SK-03: 귀속 기록이 커밋 해시별 파일↔스프린트 소속 표로 존재 — PASS
  - 근거(L3): `sprint-amendments-harness-core-defects.md:58-62` 표. 커밋 해시 2종(`e73429f`, `3cd7dfe`) + 스프린트 슬러그 2종(`bambu-kit-enum-allowlist-gate`, `harness-core-defects`)이 같은 표 안에 등장

### Script (1/1, N/A 유효)
- [x] SC-00: N/A (사유: 이번 스프린트 셸 스크립트 변경 0건) — 유효
  - 근거(L3): `git status --porcelain` 결과 미추적 파일이 사이드카 1개(.md)뿐이고, 계약 파일도 이미 커밋된 .md. 스크립트 카테고리 대상 실제로 0건

### Error (1/1)
- [x] ER-01: 사이드카가 보완임을 명시 + 원문 인용 명시 — PASS
  - 근거(L3): 두 사이드카 파일 모두 최상단에 `> 이 파일은 봉인된 계약의 보완이지 대체가 아니다.` + `write-once 이며 조건 줄을 수정하지 않았다` + `아래 인용은 전부 원문 그대로다` 문장 존재 (harness-core-defects.md:3-6, harness-attribution-followup.md:3-6)

### Architecture (1/2)
- [ ] AR-01: 변경 범위가 기록물 2개로 한정 (baseline 3cd7dfe 기준 git diff) — **FAIL**
  - 근거(L3, 측정값 우선 제시): `git diff --name-only 3cd7dfe -- .harness/ harness/ bambu-kit/ docs/` 직접 실행 결과 8개 파일:
    ```
    .harness/sprint-amendments-harness-core-defects.md
    .harness/sprint-contract-docs-quality-gates.md
    .harness/sprint-contract-harness-attribution-followup.md
    .harness/sprint-contract-harness-core-defects.md
    .harness/sprint-feedback-docs-quality-gates.md
    .harness/sprint-feedback-harness-core-defects.md
    .harness/stale-values.yaml
    docs/backend/fundamentals/api-design.md
    ```
    조건 요구: 정확히 2개(계약 파일 + 사이드카) & `docs/` 0건. 측정값: 8개 & `docs/` 1건(`docs/backend/fundamentals/api-design.md`) (기준: ==2, docs 0건) → 불일치. 게다가 이 세션의 실제 사이드카 파일(`sprint-amendments-harness-attribution-followup.md`)은 미추적(`??`) 상태라 `git diff` 출력에 아예 나타나지 않는다(diff는 추적 파일만 비교) — 작성자가 사이드카에 셀프 리포트한 결함(미추적 파일 미반영)이 실측으로 재현됨. 사이드카의 "고친 형태" 제안(AR-01')은 계약이 봉인돼 있어 적용 불가 — 원문 그대로 판정
  - 수정: 계약을 고칠 수 없으므로 이번 iteration은 FAIL 확정. 다음 계약부터 diff-scope 조건은 "각 산출물 경로에 대해 `git log --oneline <BASE>..HEAD -- <path>` 1건 이상"처럼 파일 열거+개별 존재 확인 방식으로 작성 권장(사이드카 스스로도 이미 이 형태 제안)
- [x] AR-02: 봉인된 계약 2건의 conditions_digest 가 baseline 시점과 동일 — PASS
  - 근거(L3): `verify_seal` 직접 실행 — `SEAL_OK .harness/sprint-contract-bambu-kit-enum-allowlist-gate.md`, `SEAL_OK .harness/sprint-contract-harness-core-defects.md` (contract-schema §계약 봉인 함수 그대로 사용)

### Anti-patterns (2/2)
- [x] AP-01: 버전 하드코딩 없음 — PASS
  - 근거(L3): `grep -niE "hardcoded.*version"` 대상 2파일(계약 71줄+사이드카 69줄, 총 140줄) 매치 0건. "버전" 언급은 조건 텍스트(AP-01 설명 자체) 1건뿐, 실제 하드코딩 없음 확인 — 의도된 0
- [x] AP-03: bare code fence 없음 — PASS
  - 근거(L3): project.yaml 리터럴 정규식 `^```\s*$` 은 사이드카 39·62행(정상 닫는 펜스)에 매치되나, 이는 마크다운 문법상 항상 힌트 없는 닫는 태그이며 안티패턴이 실제로 겨냥하는 "여는 펜스에 언어 힌트 누락"이 아니다. 여는 펜스는 35·58행 모두 ` ```text `로 힌트 존재. 안티패턴 message 가 명시적으로 인용하는 권위 도구 `validate-plugin.py --check=code-fence` 를 실제 실행한 결과 `Total: 13 plugins, 13 OK`(전체 저장소 0 bare) — 해당 검사는애초에 `.harness/` 를 스캔 대상에 포함하지 않음(skills/agents/references/README 전용). 실제 위반 0건
  - 참고(계약결함 아님, project.yaml 결함): `^```\s*$` 정규식은 닫는 펜스도 항상 매치하므로 이 규칙 자체가 과매치 구조 — 여는 펜스만 판정하는 상태기계 방식(validate-plugin.py 의 in_block 토글)으로 교정 권장

### Reusability (2/2)
- [x] RE-01: 재사용 가능 컴포넌트를 private 처리하지 않음 — PASS
  - 근거(L2/L3): 두 산출물 전문 검토 — 마크다운 기록물 2건이며 컴포넌트/코드 요소 자체가 없음. 위반 대상 부재로 vacuous 충족 아님 — "컴포넌트가 없으므로 위반 발생 여지가 없음"을 직접 확인
- [x] RE-02: 기존 유사 컴포넌트 재사용 — PASS
  - 근거(L2/L3): 사이드카 엔트리 포맷(대상 조건·변경·근거·앵커)이 `harness/references/contract-schema.md` §Amendment 사이드카 엔트리 포맷을 그대로 따름(기존 사이드카 `sprint-amendments-bambu-seam-policy.md` 등과 동일 컨벤션 재사용), 새 포맷 발명 없음

### Diagnostics (2/4, N/A 2건 유효)
- [x] DG-01: N/A (사유: 셸 스크립트 변경 없음) — 유효
  - 근거(L3): 위 SC-00 과 동일 근거 재확인. `bash -n scripts/release.sh` 자체는 문법 통과하나 이번 세션 변경 대상 아님
- [x] DG-02: N/A (사유: .md 만 생성) — 유효
  - 근거(L1/L3): 생성 파일 확장자 둘 다 `.md` 확인 (`ls -la` 결과)
- [x] DG-03: 콘솔 로그 에러/예외 0개 — PASS
  - 근거(L3): `bash scripts/release.sh 2>&1 || true` 실행 결과 사용법 안내만 출력, `grep -iE "error|exception|traceback|fatal"` 매치 0건(NO_MATCH)
- [ ] DG-04: 기록물 2개가 Step 6.5 게이트 기준을 위반 0건으로 통과 — **FAIL**
  - 근거(L3): Step 6.5 3개 명령을 계약 파일과 사이드카 파일 양쪽에 리터럴 적용.
    계약 파일: 헤더 전부 허용 목록 내(배경/범위 경계/Skill/Script/Error/Architecture/Anti-patterns/Reusability/Diagnostics), 체크박스 전부 조건 섹션 내, frontmatter `conditions=15`==실제 15 → 위반 0건 (PASS 부분)
    사이드카 파일(`sprint-amendments-harness-attribution-followup.md`): 헤더 목록에 `## AM-01 — 기록 전용 (direction 없음)`, `## 재발 방지` — 둘 다 허용 섹션 헤더 목록(Skill/Script/Error/Architecture/Anti-patterns/Reusability/Diagnostics + 배경/리서치 소스/GAP 분석/범위 경계/회귀 게이트) 밖. 체크박스 패턴 매칭 시도 결과 `- [ ] AR-01':`, `- [ ] DG-04':` 2건이 `## AM-01` 섹션(비허용 섹션) 안에서 검출됨. frontmatter 자체가 없어 `conditions:` 값 대조 불가(정의되지 않음=불일치). 조건 문구 "생성한 기록물 2개가 ... 위반 0건으로 통과한다"는 계약 파일뿐 아니라 사이드카도 포함해 요구하며, 사이드카는 이 리터럴 게이트를 통과하지 못한다
    (참고: `harness/references/contract-schema.md` §Amendment 사이드카 는 "사이드카 파일은 계약 파서 대상이 아니므로 `##` 헤더 이름에 제약이 없다"고 명시 — 즉 설계 의도상 Step 6.5 는 사이드카에 적용되지 않아야 한다. 그러나 이 계약의 DG-04 조건 문구는 그 스코프 제한을 걸지 않고 "기록물 2개" 전체에 게이트를 걸었고, 조건은 봉인되어 있어 문구를 사후에 좁힐 수 없다. 작성자의 사이드카 주장("조건이 틀렸고 구현이 맞다")은 설계 의도 관점에서 타당하나, 봉인된 조건의 문자 그대로 판정에서는 FAIL이 맞다)
  - 수정: 계약을 고칠 수 없으므로 이번 iteration은 FAIL 확정. 다음 계약부터 DG-04류 조건은 "계약 파일은 Step 6.5 게이트 위반 0건 / 사이드카는 §Amendment 사이드카 엔트리 포맷을 만족" 처럼 산출물 종류별로 게이트를 분리해 작성 권장 (사이드카 스스로도 이미 이 형태(DG-04')를 제안함)

## Unverifiable Summary
- invalid_evidence: 0
- env_gaps: 0
- verified_coverage: (15 - 0) / 15 = 1.00 (임계 0.60 충족)
- 연속 ENV 승급: 없음
- Verdict 영향: 통상 (모든 조건이 직접 측정으로 판정 완료, 미검증 마커 없음)

## Discrimination
- 적용 조건: 없음 (동시성 가드·인증·멱등성·입력검증·데이터유실·마이그레이션·재시도·보안경계·사용자보고-테스트충돌 9항목 해당 조건 없음)

## User-Reported Failures
- 해당 없음 (이번 평가는 신규 계약 최초 판정이며 재발 보고 없음)

## Evidence Validity
- 검사 대상 증거: 15건 (조건별 1건씩)
- 무효 판정: 0건
- 셸 스니펫 실행 검증: 실행 15건 (모든 측정 명령을 zsh 환경에서 직접 실행. 이 세션 환경은 zsh 단일 — bash 교차 검증은 명령 자체가 POSIX 호환 grep/git/awk 조합으로 셸 특이 문법(glob 등) 미사용이라 결과 동일 예상, 별도 bash 재실행은 생략)
- 무효 0건은 미검증 카운터에 영향 없음

## Summary
- Total: 13/15 conditions passed (SK-01,02,03 · SC-00(N/A) · ER-01 · AR-02 · AP-01,03 · RE-01,02 · DG-01(N/A),02(N/A),03 = PASS/유효N/A, AR-01 · DG-04 = FAIL)
- Verdict: REJECT
- FAIL 항목 요약:
  1. **AR-01** — diff-scope 오라클이 baseline 커밋 기준 8개 파일을 잡아내고(요구:2개), docs/ 경로에도 1개(`docs/backend/fundamentals/api-design.md`) 걸림(요구:0). 게다가 이 세션의 실제 사이드카 파일은 미추적 상태라 오히려 diff에 안 잡힘 — 오라클이 "내가 만진 파일"이 아니라 "두 커밋의 차이"를 재는 근본 문제가 실측으로 재현됨
  2. **DG-04** — "기록물 2개"에 Step 6.5 게이트(계약 파일 전용 파서 호환성 게이트)를 무차별 적용하도록 조건이 쓰여있어, 사이드카가 스키마상 허용된 자유 헤더(`## AM-01`, `## 재발 방지`)를 쓰는 순간 리터럴 판정으로 위반이 발생
  - 수정 우선순위: 두 FAIL 모두 "계약 결함(오라클이 조건 의도와 다른 것을 잼)"이 원인이나, 계약은 봉인되어 있어 이번 iteration에서 구제 불가. 사용자가 계약을 폐기하고 재작성하거나, 다음 스프린트에서 사이드카가 이미 제안한 AR-01'/DG-04' 형태로 후속 계약을 작성해야 함

## Improvement Suggestions
- [AR-01] 측정-방식-불일치 — "git diff --name-only <baseline> -- <paths>" 는 미추적 신규 파일을 못 잡고 동시 세션 커밋을 걸러내지 못한다. 대체: "이번 스프린트가 생성한 기록물 각 경로에 대해 `git log --oneline <BASE>..HEAD -- <path>` 가 1건 이상"으로 재작성 (사이드카 AR-01' 제안과 동일)
- [DG-04] 측정-산출물-미분리 — "기록물 2개"를 단일 게이트로 뭉쳐 요구하면 계약 파일과 사이드카처럼 파서 요구사항이 다른 산출물에 동일 게이트를 강제하게 된다. 대체: "생성한 계약 파일은 Step 6.5 게이트 위반 0건 / 생성한 사이드카는 §Amendment 사이드카 엔트리 포맷(대상 조건·변경·근거·앵커)을 만족" 처럼 산출물별로 게이트 분리 (사이드카 DG-04' 제안과 동일)
- [AP-03 / project.yaml] 패턴-과매치 — `^```\s*$` 정규식은 정상적으로 닫히는 모든 코드펜스와 매치되어 사실상 상시 오탐 소지가 있다. validate-plugin.py 의 in_block 상태기계처럼 "여는 펜스인데 힌트 없음"만 판정하도록 project.yaml 의 anti_patterns 패턴 자체를 교정 권장 (이번 스프린트는 실제 위반이 없어 FAIL로 잡지 않았으나, 다음 스프린트에서 우연히 매치가 늘어나면 오판 소지)
