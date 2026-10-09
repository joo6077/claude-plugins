# Sprint Feedback
Feature: 기존 마크다운 경고 정리 — docs 폴더 (docs/superpowers 제외) (l2)
Evaluated: 2026-09-27 14:34
Verdict: REJECT
Iteration: 2

## Contract Fingerprint
- path: /Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak2-l2/.harness/sprint-contract-after-0926-mdlint-l2.md
- sha256: d2dd65c5b60cdb17b830bb4e0e0dbbe8fdb1479e553945563eefba56de9383d5
- status: done (주의 — 1회차 APPROVE 때 붙은 값이 그대로 남아 있다. 이번 회차는 REJECT 이므로 이 평가자는 status 를 건드리지 않았다. 작업이 이어지는 한 active 로 되돌리는 편이 맞다 — 사용자 확인 필요)
- slug: after-0926-mdlint-l2
- contract_root: /Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak2-l2
- contract_root_unconfigured: false
- 선택 근거: ladder 1 (HARNESS_CONTRACT 명시 경로, 존재 확인 통과)
- legacy_contract_used: false
- seal_status: SEAL_OK (재확인, W 쪽 harness/references/contract-schema.md 함수로 계산)
- measure_status: MEASURE_OK (measurement_digest 재확인 — 조건 아래 측정 줄 변조 없음)
- contract_seal_broken: n/a
- 봉인 커밋 대조(1-e-3): c768d5d, 파일 1개만 담김. 그 뒤 diff는 frontmatter status 전환 한 줄뿐, 조건/측정 줄 산문 변경 없음, conditions_digest·measurement_digest 변경 없음 → 재봉인 없음
- 재확인(Step 5): 일치 (sha256 d2dd65c5… 동일)
- status_transition: skipped (verdict=REJECT)

## Amendments
- amendments: 0 (이 슬러그의 사이드카 없음)

## User Correction Audit
- correction_log_status: available (~/.claude/logs/claude-plugins/)
- unreflected_corrections: 0
- verdict 영향: 없음

## Deletions
- deletions_range: 7a7ecb4..229dea5 (가지 끝)
- 커밋 구간 삭제: 0
- 커밋하지 않은 삭제: 0
- 선언 밖 삭제: 0

## Cross-Diagnosis Handoff
- 상태: pending-parent
- 부모가 띄울 때 넘길 것: 계약 절대경로 `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak2-l2/.harness/sprint-contract-after-0926-mdlint-l2.md` · 이 판정 결과 전문
- 부모가 물을 두 가지:
  1. 계약 조건의 원래 의도와 다르게 해석해 PASS/FAIL 을 오판한 조건이 있는가? (특히 ER-01/AR-03/AR-05 의 "disable-line·disable/enable 블록은 wide 로 센다"는 해석)
  2. 0 건·빈 출력을 근거로 PASS 한 조건 중 공허한 통과가 있는가?
- 부모가 교차 진단을 마친 뒤 `cross_diagnosis_by` 를 `sprint-contract` 로 갱신한다.

## Results

### Architecture (2/5)
- [x] AR-01: 목록 파일의 편집기 경고가 0 건이다 — PASS
  - 근거: `m AR-01` → `ver=v0.23.2 list_n=123 list_same=1 warn=0`. 기대값과 문자 그대로 일치. L3.
- [x] AR-02: 고치지 않는 파일은 한 줄도 안 바뀐다 — PASS
  - 근거: `m AR-02` → `changed_paths=118 extra=0 harness_extra=0 docs_not_modify=0 guard_in_list=0 sealed=107 seal_broken=0`. L3.
- [ ] AR-03: 뜻이 안 바뀐다 — **FAIL**
  - 측정값: `m AR-03` → `changed=116 word_same=113 word_diff=3 wide_disable=7 nl_added=267` (기준: word_diff=0, wide_disable=0)
  - 근거: 회차 2 수정 커밋(3ad40cc)이 `docs/bambu-calibration/calibration-reference.md`(MD033 표 감싸기)·`docs/react/kit-design/g6-build-audit.md`(MD038 3곳)·`docs/api/execution/auth-secret-lifecycle.md`(MD038 2곳) 에 `<!-- markdownlint-disable MD033 -->`/`<!-- markdownlint-enable MD033 -->` 블록 1쌍과 `<!-- markdownlint-disable-line MD038 -->` 5개를 새로 넣었다. 도우미의 `WIDE` 정규식(`markdownlint-(disable|enable|…|disable-line)(?!-next-line)`)이 이 여섯 자리를 모두 "wide"(구간·줄끝 끄기, `-next-line` 아님)로 잡는다 — 계약 §배경 24행 "그 자리에만 `disable-next-line`… 파일 전체를 끄는 주석은 쓰지 않는다"와 ER-01 정의("한 줄짜리로만… `-next-line` 아닌 것을 새로 넣은 줄이 0")를 문자 그대로 어긴다. `word_diff=3`은 이 세 파일이 `norm()`의 표식 제거 후에도 달라졌다는 뜻 — disable-line 주석 자체가 `NL`(disable-next-line 전용) 정규식에 안 걸려 지워지지 않고 그대로 비교에 남기 때문이다. L3, 도구 직접 재실행.
  - 수정 방향: block 형태(disable/enable) 대신 표 각 줄 앞에 개별 disable-next-line을 넣거나(표가 쪼개지지 않도록 HTML 대체 수단 검토), MD038 줄들은 줄 끝 disable-line 대신 그 줄 바로 앞에 disable-next-line 한 줄을 추가하는 형태로 바꿔야 한다. 그마저 어렵다면 계약 조건 자체(ER-01/AR-03의 "-next-line만 허용")를 완화하는 개정을 사용자에게 요청해야 한다 — 임의로 오라클을 재해석하지 않았다.
- [x] AR-04: 커밋이 맨 위 폴더 둘을 섞지 않는다 — PASS
  - 근거: `m AR-04` → `impl_commits=3 multi_top=0`. L3.
- [ ] AR-05: 좁힌 끄기 주석 수와 이유가 notes 에 있다 — **FAIL**
  - 측정값: `m AR-05` → `committed=1 section=1 want=[MD024:164 MD025:86 MD028:4 MD036:12 MD041:1] rows_match=5/5 reason_ok=5/5 rows_extra=2` (기준: rows_extra=0)
  - 근거: notes 표에는 MD033·MD038 행이 추가돼 있으나(229dea5), 그 두 규칙의 새 주석이 disable-next-line이 아니라 disable/enable·disable-line 이라 `want`(disable-next-line만 세는 `rules` 카운터)에 잡히지 않는다. 표 행과 실제 주석 방식이 어긋나 `rows_extra=2`. AR-03/ER-01과 같은 근본 원인. L3.

### Script (1/1)
- [x] SC-01: 원본을 읽는 스크립트와 레포 검사가 끝점에서 모두 통과한다 — PASS
  - 근거: `m SC-01` → `rc: validate-plugin.py=0 sync-docs.py=0 sync-orchestrator.py=0 sync-evals.py=0 run-evals.py=0 run-kaizen-assertions.py=0 check-reviewer-protocol-copies.py=0 check-cause-table-copies.py=0 detect-docs-drift.py=0 measure-helpers-test.sh=0`. enumerated 10개 전부 개별 확인. L3.

### Error (0/1)
- [ ] ER-01: 끄는 주석은 실제로 걸리는 줄 바로 앞에만, 한 줄짜리로만 넣는다 — **FAIL**
  - 측정값: `m ER-01` → `comments=267 useless=0 wide_disable=7` (기준: wide_disable=0)
  - 근거: AR-03과 동일 원인 — disable/enable 블록 1쌍 + disable-line 5개 = 7건이 `-next-line` 아닌 끄기로 새로 들어갔다. `useless=0`은 통과지만 `wide_disable`이 조건의 필수 기준을 어긴다. L3.

### Anti-patterns (2/2)
- [x] AP-03: bare code fence 금지 — PASS
  - 근거: `m AP-03` → `md040=32->0 notes_bare=0`. L3.
- [x] AP-04: SKILL.md/agents frontmatter name 누락 금지 — PASS
  - 근거: `m AP-04` → `fm_changed=0 drafts_name=howto`. L3.

### Reusability (2/2)
- [x] RE-01: 재사용 가능 컴포넌트를 private으로 만들지 않음 — PASS (N/A성, 산출물에 코드 없음)
  - 근거: `m AR-02` → `extra=0 harness_extra=0`.
- [x] RE-02: 기존 컴포넌트 재사용 — PASS
  - 근거: `m AR-02` → `extra=0` (새 검사 도구 없음).

### Diagnostics (2/4, N/A 2)
- [ ] DG-01: N/A (`m DG-01` → `release_paths=0`)
- [ ] DG-02: IDE diagnostics 0건 — **FAIL**
  - 측정값: `m DG-02` → `notes_warn=3 list_warn=0` (기준: notes_warn=0)
  - 근거: `.harness/.meta/after-kaizen-0926b/l2-notes.md` 49행이 검사 패턴을 설명하며 `` `^export default ` ``·`` ` as [A-Z]…` ``·`` `Bearer ` `` 처럼 앞뒤 공백이 있는 코드 표시를 그대로 인용한다. markdownlint-cli2 로 직접 재실행 → `l2-notes.md:49`에서 MD038 3건(직접 명령 재현, 도구 자체 출력 인용). 229dea5에서 notes 를 갱신하며 새로 발생한 위반이다. L3.
- [ ] DG-03: N/A (DG-01과 동일 근거, `release_paths=0`)
- [x] DG-04: 실제 앱/서버 구동 시 에러 0개 (CI 로컬 대체) — PASS
  - 근거: `m DG-04` → `tool_same=1 ci_rc=0 rc0=25 other=[feedback-agg-test SKIP (yq 없음);]`. 기대값과 문자 그대로 일치. L3.

### Skill (0/0, N/A 1)
- [ ] SK-00: N/A (`m AR-02` extra=0)

## Unverifiable Summary
- invalid_evidence: 0
- env_gaps: 0
- verified_coverage: (16 - 0) / 16 = 1.00 (임계 0.60)
- Verdict 영향: 통상 (미검증 무관 — FAIL 4건으로 REJECT)

## Discrimination (규칙 12 적용 조건만)
- 적용 조건: 없음 (동시성/인증/멱등성/보안 경계 등 9항 대상 조건 없음 — 문서 정리 스프린트)

## Check Artifacts (산출물이 검사인 조건만)
- 해당 없음 — 이번 스프린트가 새 검사 스크립트를 만들거나 고치지 않았다. 기존 `run.sh`/`cfg.jsonc`/`m()` 측정 도우미로 평가자가 시작 판·끝 판을 독립 재실행했다.

## 표본 재확인 (바뀐 줄이 뜻을 안 바꿨는지)
- `docs/kaizen/changelog.md`·`docs/kaizen/research-log.md`: MD024 disable-next-line 삽입, URL을 `<>`로 감싼 것 확인 — 글 내용·문장 순서 불변. L3, 직접 diff 대조(1회차가 안 본 파일로 골라 표본 확대).
- 위 세 파일(calibration-reference·g6-build-audit·auth-secret-lifecycle)의 실제 고침 내용 자체는 뜻이 통한다(공백 되돌림, 표 감싸기) — 다만 **끄기 주석의 형식**이 계약 위반이다(위 AR-03/ER-01/AR-05/DG-02 근거).

## Summary
- Total: 12/16 conditions passed (PASS 9 · N/A 3 · FAIL 4)
- Verdict: **REJECT**
- FAIL 항목 요약 및 수정 우선순위:
  1. **AR-03 / ER-01 / AR-05 (근본 원인 동일)** — 회차 2 검토 수정에서 쓴 `markdownlint-disable`/`enable`(구간)과 `disable-line`(줄끝)은 계약이 명시적으로 요구하는 "그 자리 바로 앞 disable-next-line 한 줄"이 아니다. 세 파일(calibration-reference.md 표, g6-build-audit.md, auth-secret-lifecycle.md)의 끄기 주석 형식을 disable-next-line 방식으로 바꾸거나, 형식을 바꿀 수 없다면(예: 표 안에서는 disable-next-line이 첫 줄에만 적용돼 표가 쪼개짐) 계약 ER-01/AR-03 조건 자체의 "-next-line만 허용" 요건을 완화하는 개정을 사용자에게 요청해야 한다.
  2. **DG-02** — `l2-notes.md`가 검사 패턴을 설명하며 그 안에 문제되는 공백을 그대로 인용해 notes 파일 자신에서 새 MD038 3건이 발생했다. 코드 표시 안 공백을 유지해야 설명이 되는 자리이므로, 그 3곳에 줄끝 `<!-- markdownlint-disable-line MD038 -->`를 붙이거나(다만 이는 다시 ER-01 wide_disable을 늘림) 서술 방식을 바꿔 공백을 명시적으로 표현(예: "끝에 공백 한 칸")하는 방향을 검토해야 한다.
- 참고: 이번 회차가 고치려던 원래 2건(끊긴 표 렌더링, g6-build-audit·auth-secret-lifecycle 검사 패턴 공백 소실)은 실제로 해결됐다(1회차 교차 진단이 옳았다). 다만 그 해결 방법이 이 계약의 다른 조건(ER-01/AR-03/AR-05/DG-02)을 새로 위반했다.

## Improvement Suggestions
- [ER-01] 태그-산출물-불일치 — "표 안에서 여러 줄을 한 번에 끄는 합법적 수단이 disable-next-line 하나뿐"이라는 전제가 실무와 충돌한다(표는 여러 줄이라 첫 줄 disable-next-line만으로는 나머지 행이 안 커진다). 계약에 "표·여러 줄 구간은 그 구간 전체를 감싸는 disable/enable 쌍을 허용하되 구간 밖으로 새지 않아야 한다"는 예외 문구를 추가하거나, WIDE 판정에서 "여는/닫는 쌍이 같은 파일 안에서 서로 인접한 블록만 감쌌는지" 확인하는 구체적 대체 측정을 제안한다.
- [AR-05] 측정-방식-불일치 — `want` 카운터가 disable-next-line만 세고 있어 notes 표에 disable-line/구간 쌍을 적으면 항상 `rows_extra`가 발생한다. ER-01 예외가 확정되면 `rules` 카운터도 disable-line/구간 쌍을 함께 세도록 맞춰야 한다.
