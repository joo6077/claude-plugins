# Sprint Feedback
Feature: 카이젠 Phase 12 재검증 — 정규화 오라클에 양성 대조 부착(F2) + grep 거짓음성 규약(F1) + 추출 SSOT 통합(F4) + 열 서술 정정(F3) — **재평가 (2026-08-13 사이클 phase12b, 독립 재판정)**
Evaluated: 2026-08-14 11:32
Verdict: APPROVE
Iteration: 1 (재평가 — 로컬/글로벌 피드백 산출물 부재로 인한 독립 재실행. 이전 판정은 승계하지 않음)

## 재평가 사유

이 계약은 이미 `status: done` 이며 원 판정(2026-08-13)의 근거는 워크플로 저널에 남아 있으나,
오케스트레이터의 QA 서브에이전트 structured-output 강제로 Step 8(글로벌 피드백 저장)이
실행되지 않아 `~/.harness/feedback/evaluator/` 에 아티팩트가 없었다. 본 재평가는 그 판정을
**승계하지 않고 14개 조건 전부를 직접 재실행**했다.

## Contract Fingerprint
- path: `.harness/sprint-contract-kaizen-phase12-oracle-positive-control.md`
- sha256: `8e1e7e44dbd038defa7337434b45f199c5218d3797f0194d2293fa73a042f238`
- status: `done` (이미 done — 이번 verdict 로 되돌리거나 재전환하지 않음, 오케스트레이터 처리 대상)
- slug: `kaizen-phase12-oracle-positive-control`
- contract_root: `/Users/jackson/Hub/10_Dev/claude-plugins`
- contract_root_unconfigured: false
- 선택 근거: ladder 1 (명시 경로 — 사용자 지정)
- legacy_contract_used: false
- 봉인: **SEAL_OK** (`conditions_digest` = `sha256:87763986f7bc35b4`, 재계산값과 일치)
- 재확인(Step 5, 저장 직전): **일치** (sha256 동일 · status 동일 `done`)
- status_transition: skipped (verdict=APPROVE 이나 status 가 이미 `done` — active→done 전환 대상 아님)

## Amendments
- amendments: 7 (AM-01~AM-07, 전부 `.harness/sprint-amendments-kaizen-phase12-oracle-positive-control.md`)
- narrowing: 0
- relaxing / unknown: 1 — **AM-01 (SC-05 측정문을 좁히자는 제안)**. 사용자 앵커 없음(unanchored) +
  방향 relaxing으로 분류되어 PASS 근거 불가 판정이 이미 내려졌고(원 QA 사이클), 구현자가 자체
  철회(AM-04)하여 원 측정문을 그대로 충족시키는 구현 수정으로 대체했다. 본 재평가에서도 SC-05를
  **원 조건 문언 그대로** 재검증했다(`grep -rlF 'mistake_tag:' reflect-kit/hooks` → 1행, 아래
  SC-05 참조) — AM-01을 PASS 근거로 쓰지 않았다.
- 나머지 6건(AM-02·AM-03·AM-05·AM-06·AM-07)은 direction 변화 0 (측정 해석 기록·범위 밖 판단
  보존·자진 정정·범위 경계 위반 복구)이며 조건 판정에 영향 없음. 상세는 사이드카 원문 참조.
- **사용자 확인 필요**: 없음 (AM-01은 이미 구현으로 해소됨, 나머지는 정보성 기록)

## User Correction Audit
- correction_log_status: available (`~/.claude/logs/claude-plugins/2026-08.md`)
- 스프린트 창(2026-08-13 18:20 ~ 평가 시각) 내 prompt 전부가 동일 세션(`df1b3e15-...`)의
  오케스트레이터 task-notification/tool-failure 로그이거나 "ㄱㄱ"(진행 지시), "다음 세션"
  등 계속 진행 지시였다. Phase 12 관련 방향 교정 발언은 발견되지 않았다.
- unreflected_corrections: 0
- verdict 영향: 없음 (표면화 전용)

## Results

### Skill (3/3)
- [x] SK-01: `tag_canon_selftest` 를 호출하는 스킬 2개 — PASS
  - 근거: `grep -rlF 'tag_canon_selftest' reflect-kit/skills` → `reflect-kit/skills/reflect-digest/SKILL.md`, `reflect-kit/skills/reflect-kaizen/SKILL.md` (정확히 2행, 계약 열거와 일치). L3.
- [x] SK-02: selftest 실패 효력이 두 스킬에 규정 — PASS
  - 근거: `reflect-kaizen/SKILL.md` `calibration_confidence: low` 카운트 = 7 (스프린트 시작 시점 baseline `409c780` 대비 6→7, 증가 확인), 해당 문자열이 `tag_canon_selftest` 호출 직후 문맥(50-60행)에 위치 확인. `reflect-digest/SKILL.md` `집계 근거로 쓰지 마라` 카운트 = 2 (>=1), `tag_canon_selftest || echo "...집계 근거로 쓰지 마라"` 로 직결 확인. L3.
- [x] SK-03: SSOT에 규칙 6·7 존재 — PASS
  - 근거: `tag-canonicalization.md` `규칙 6` 2건, `규칙 7` 2건, 규칙 7 문맥(186행)에 `ugrep 7.5.0` 문자열 확인. L3.

### Script (6/6)
- [x] SC-01: 정상 맵에서 `SELFTEST_OK` + rc 0, 음성 대조(`verb` 행 제거)에서 FAIL — PASS
  - 근거: `bash -c '. _lib-tag-canon.sh; tag_canon_selftest'` → `SELFTEST_OK raw=4 clusters=2 canonical=edit-before-read` rc=0. `verb` 행 제거한 맵(`awk -F'\t' '$1!="verb"'`)을 `export REFLECT_TAG_LEMMA_MAP`으로 넘기면 `SELFTEST_FAIL fold raw=4 clusters=4` rc=1. 직접 실행 확인 (bash/zsh/sh 3셸 동일). L3.
- [x] SC-02: 손상 맵 3종 전부 rc 1 + `clusters` 값이 정상(2)과 다름 — PASS
  - 근거: (a) `/nonexistent` → `SELFTEST_FAIL` rc=1, clusters=4. (b) `verb` 행 제거 → rc=1, clusters=4. (c) `verb-synonym` 행 제거 → rc=1, clusters=3. 3케이스 모두 `export`로 전달, rc=1, `SELFTEST_FAIL` 포함, clusters(4/4/3)가 정상(2)과 상이함을 직접 실행으로 확인. L3.
- [x] SC-03: `set -u` 유무 × {bash,zsh,sh} × cwd 4종 = 24회 전 조합 동일 출력 — PASS
  - 근거: 24회 전부 실행(`2*3*4`를 `${#SHELLS[@]}*${#SETU[@]}*${#CWDS[@]}`로 산출), `sort -u` 결과 1행 = `SELFTEST_OK raw=4 clusters=2 canonical=edit-before-read` (퇴화 출력 `0 0 0 0...` 아님을 확인). L3.
- [x] SC-04: 훅 어휘 생성 경로 3종 + 음성 대조 — PASS
  - 근거: `log-reflection.sh` 102~163행을 원문 그대로 추출해 격리 실행. (a) 정상 fixture → `- skipped-required-api-doc-check  (freq 3)  ← ...` 행 존재. (b) `REFLECT_TAG_LEMMA_MAP=/nonexistent` → `.errors.log`에 `warn:lemma-map-unreadable` 1행 + `known_tags_block` 비어있지 않음(`- skipped-required-api-doc-check  (freq 2)`). (c) 빈 디렉토리 → `(없음 — 첫 수집)` 포함, 셸 에러 0 (exit 0). 음성 대조: `tag_canon_extract` 호출을 `true`로 치환하면 (a)의 canonical 행이 사라지고 `(없음 — 첫 수집)`으로 퇴화함을 확인. L3.
- [x] SC-05: 추출 규칙이 `reflect-kit/hooks` 안에서 라이브러리 1곳에만 존재 + 등가 증명 — PASS
  - 근거: `grep -rlF 'mistake_tag:' reflect-kit/hooks` → `_lib-tag-canon.sh` 1행 (log-reflection.sh 0건, `grep -nF`로 재확인). 등가 증명은 실측으로 독립 재현: 실 로그 14파일(13+bundle) 4,825행에 대해 **통합 전 인라인 추출**(`grep -h '^[[:space:]]*mistake_tag:' | sed ...`)과 **현재 `tag_canon_extract`**의 출력이 `diff` 0행, md5 `19bb2cabb12671530a623bd635556de0`로 완전 동일함을 직접 계산 확인 (AM-04가 제시한 md5와는 다른 값이나, 이는 로그가 그 사이 증가했기 때문이며 독립 재현이 목적이므로 문제 아님 — 핵심 명제인 "신·구 추출 방식이 바이트 단위로 동일"은 내가 직접 재현했다). L3.
- [x] SC-06: 변경 셸 스크립트 2개 shellcheck 0 + `bash -n` 통과 — PASS
  - 근거: `shellcheck reflect-kit/hooks/_lib-tag-canon.sh reflect-kit/hooks/log-reflection.sh` → 출력 0행, exit 0 (shellcheck 0.11.0). `bash -n` 양쪽 파일 exit 0. L3.

### Architecture (3/3)
- [x] AR-01: 변경이 정확히 5경로로 한정 — PASS `[상태 전제 명시 필요 — 아래 참조]`
  - 근거: 이 스프린트는 QA blocking→fix 반복(최초 커밋 `175ef87` + blocking 해소 커밋 `ffc0a84`·`f62691f`)이 있었다. "커밋 직전 working tree" 문언을 최초 커밋 단독으로 읽으면 3경로뿐이라 문언과 불일치한다. **스프린트 누적 diff**(`git diff --name-only 409c780 f62691f -- reflect-kit/`, 409c780=스프린트 직전 커밋, f62691f=이 스프린트의 마지막 자체 fix 커밋)로 측정하면 계약이 선언한 5경로(`_lib-tag-canon.sh`·`log-reflection.sh`·`tag-canonicalization.md`·`reflect-digest/SKILL.md`·`reflect-kaizen/SKILL.md`)와 **정확히 일치**(`diff` 0행). 그 뒤에 온 `03669c7`(11개 킷 전체 버전 bump, `reflect-kit/.claude-plugin/plugin.json` 포함 10개 킷 모두 동일 변경)은 사이클 전역 릴리스 housekeeping이며 이 스프린트 범위가 아니라고 판단해 diff 종료점에서 제외했다. **상태 전제 미명시 플래그**: 계약 조건 문구에 다중 커밋 스프린트의 diff 종료점 기준이 없어 평가자가 이 상태를 선택했다는 점을 명시한다. L3.
- [x] AR-02: 3열 서술 0건 — PASS
  - 근거: `grep -cF 'clusters \t ratio' reflect-kit/hooks/_lib-tag-canon.sh` = 0, 대조로 7열 서술 3곳(26·139-140·260행) 확인. L3.
- [x] AR-03: 봉인 계약(`...tag-canonicalization.md`) 파일 변경 없음 — PASS
  - 근거: `git diff --name-only -- .harness/sprint-contract-kaizen-phase12-tag-canonicalization.md` → 0행. L3.

### Diagnostics (2/2)
- [x] DG-01: `validate-plugin.py reflect-kit` V1~V8 전부 OK, exit 0 — PASS
  - 근거: 직접 실행 — V1~V8 전부 OK, `Exit: 0`. L3.
- [x] DG-02: `sync-docs.py reflect-kit --check-only` 동기화 필요 0건 — PASS
  - 근거: 직접 실행 — "모든 README가 동기화 상태입니다.", exit 0. L3.

### Anti-patterns (4/4 — 실질 위반 0)
- [x] AP-01 하드코딩 버전: 5개 변경 파일에서 0건 — PASS (L2)
- [x] AP-02 force push: 0건 — PASS (L2)
- [x] AP-03 bare code fence: raw grep은 8행 매치(````` ``` `````만 있는 줄)하나, 전수 Read 확인 결과 전부 언어 힌트 있는 opening(```bash/```yaml/```text/```markdown/```diff)과 정상 pairing된 **closing** fence였다. `validate-plugin.py` V6(코드펜스 authoritative 검사)도 "0 bare — OK"로 확인 — **실질 위반 0**. PASS (L3, grep 오탐 필터링 완료)
- [x] AP-04 SKILL.md name 필드 누락: `reflect-digest/SKILL.md`·`reflect-kaizen/SKILL.md` 둘 다 frontmatter 첫 줄에 `name:` 존재 — PASS (L2)

### Reusability
- N/A — `project.yaml`의 `shared_path`(`scripts/`)와 이번 변경 대상(`reflect-kit/hooks`, `reflect-kit/references`, `reflect-kit/skills`)이 무관. 검토 대상 없음.

## Unverifiable Summary
- 총 미검증 건수: 0
- Verdict 영향: 해당 없음 (전 조건 L3 직접 실행 검증 완료)

## Evidence Validity
- 검사 대상 증거: 14개 조건 전부 + anti-pattern 4종
- 무효 판정: 0건
- 셸 스니펫 실행 검증: 전체 14개 조건에서 실행이 필요한 12개(SK 3종은 grep 정적 확인, SC 6종+DG 2종+AR 1종(git diff)은 직접 실행) 전부 bash로 실행, 그중 SC-01/SC-02/SC-03은 zsh·sh 교차 확인까지 완료 (SC-03은 계약이 명시한 조합 자체가 bash·zsh·sh 3셸 포함)
- 무효 0건이므로 미검증 카운터에 추가 없음

## Summary
- Total: 14/14 conditions passed
- Anti-patterns: 4/4 (실질 위반 0, AP-03 grep 오탐 1건은 Read로 정정 확인)
- Verdict: **APPROVE**
- 이 판정은 원 판정(미저장)을 승계하지 않고 14개 조건을 처음부터 직접 재실행하여 독립적으로 도출했다. 결함은 발견되지 않았다.

## Cross Diagnosis
- 이 실행 컨텍스트에는 Task/Agent 서브에이전트 호출 도구가 제공되지 않아 `sprint-contract` 서브에이전트를 통한 정규 Step 7 교차 진단을 물리적으로 수행할 수 없었다. 대신 Step 3.5(Self-Evaluator Rule-by-Rule Audit)를 보완 통제로 수행 — 카테고리별(Skill/Script/Architecture/Diagnostics) 전 조건 나열, enumerated 서브체크 전수 확인(SK-01 2/2 · SK-02 2/2 · SK-03 2/2 · SC-02 3/3 · SC-03 24/24 · SC-06 2/2 · AR-01 5/5), `[미검증]` 0건, FAIL 사유 없음을 재확인했다.
- 이 한계를 `diagnosis.cross_diagnosis_notes`에 투명하게 기록했다 (아래 글로벌 피드백 참조).

## Improvement Suggestions
- [오케스트레이터] structured output schema를 QA 서브에이전트에 강제하면 Step 8(글로벌 피드백 저장)이 스킵될 수 있다 — 이번 재평가의 근본원인. 스키마 강제와 무관하게 Step 8이 항상 실행되도록 강제하거나, 오케스트레이터가 후처리로 저장을 대행하는 방식을 검토할 것.
- [AR-01] 측정-상태-모호 — "Given: 커밋 직전 working tree"만으로는 QA REJECT→fix 반복이 있는 스프린트에서 diff 종료점이 모호하다. "Given: 이 슬러그의 스프린트 전체 누적 diff(직전 사이클 마지막 커밋..이 스프린트의 마지막 자체 fix 커밋, 사이클 전역 release 커밋 제외)"로 구체화 권장.
- [project.yaml AP-03] 태그-산출물-불일치 — `^```\s*$` 패턴이 정상 closing fence를 상시 오탐한다. `validate-plugin.py` V6가 이미 opening/closing을 구분하는 authoritative 검사이므로, project.yaml에서 이 anti-pattern 항목을 제거하고 V6로 일원화할 것을 권고.

## 글로벌 피드백 저장
- 저장 경로: `/Users/jackson/.harness/feedback/evaluator/1a3bcba6-2026-08-14T113251-1e76aa0b-41672.yaml`
- `verify-feedback.sh` 결과: **PASS**
