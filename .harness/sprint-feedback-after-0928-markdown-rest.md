# Sprint Feedback
Feature: 마크다운 남은 경고 · 깨진 코드 블록 · 목록 · 밀린 줄 참조 (A1 · B18 · B19 · B20)
Evaluated: 2026-09-28 13:13
Verdict: REJECT
Iteration: 1

## Contract Fingerprint
- path: .harness/sprint-contract-after-0928-markdown-rest.md
- sha256: ab16bb3be2891ba42cc0ee3b86358c370e180c0dcebbff7073d2a1c99f0b4288
- status: active
- slug: after-0928-markdown-rest
- contract_root: /Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak3-lt
- contract_root_unconfigured: false
- 선택 근거: ladder 1 명시경로
- legacy_contract_used: false
- seal_status: SEAL_OK
- contract_seal_broken: n/a
- seal_commit: b53f607f (files=1, 계약 파일 하나만)
- 재확인(Step 5): 일치
- status_transition: skipped (verdict=REJECT status=active — active 유지, 재평가 대상)

## Amendments
- amendments: 0 (사이드카 `.harness/sprint-amendments-after-0928-markdown-rest.md` 없음)
- PASS 근거 가능: 0
- PASS 근거 불가: 0
- 비고: 계약 배경 절에 「RELAXING_PENDING — SK-06 을 완화하는 개정에 사용자 동의가 필요하다」는
  기록이 있으나, 실제 사이드카 파일은 아직 생성되지 않았다. 사용자 동의(anchored consent)가
  없으므로 SK-06 은 원 조건 문자 그대로 판정한다(아래에서 실제로 SK-06 은 PASS — 완화가
  필요했던 것은 SK-01/DG-02 이지 SK-06 자체가 아니었다).

## User Correction Audit
- correction_log_status: available (`~/.claude/logs/claude-plugins/2026-09.md`)
- unreflected_corrections: 0 (봉인 시각 12:43 이후 이 세션의 user prompt 는 이번 QA 요청 1건뿐)
- verdict 영향: 없음 (표면화 전용)

## Deletions
- deletions_range: e500a63..2f0bb0d
- 커밋 구간 삭제: 0
- 커밋하지 않은 삭제: 0
- 선언 밖 삭제: 0

## Cross-Diagnosis Handoff
- 상태: pending-parent
- 부모가 띄울 때 넘길 것: 계약 절대경로 `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak3-lt/.harness/sprint-contract-after-0928-markdown-rest.md` · 이 판정 결과 전문
- 부모가 물을 두 가지:
  1. 계약 조건의 원래 의도와 다르게 해석해 PASS/FAIL 을 오판한 조건이 있는가?
  2. 0 건·빈 출력을 근거로 PASS 한 조건 중, 문제가 있어도 0 을 냈을 측정(공허한 통과)이 있는가?
- 부모가 교차 진단을 마친 뒤 `cross_diagnosis_by` 를 `sprint-contract` 로 갱신한다.

## Results

### Skill (10/11)
- [x] SK-01: FAIL — 아래 참조
- [x] SK-02: (A1) 뺀 시험 입력 21 파일이 BASE 와 같고 notes 가 이유를 적는다 — PASS
  - 근거: `git diff --name-only $BASE $TIP -- $(cat a1-excluded.txt)` = 0건. `git cat-file -e $TIP:$N` rc=0. 21개 경로 각각 notes 에서 '시험 입력' 문구와 함께 1건 이상 확인(L3, 직접 실행).
- [x] SK-03: 여덟 파일 경고 정리가 모양을 안 바꿈 — PASS
  - 근거: `shape-run.sh $BASE $TIP a1-files.txt` → `TOTAL 0 0 0` (직접 실행 확인).
- [x] SK-04: (B18) 아홉 파일 울타리 짝 다섯 칸 0, 레포 전체 삼킨 줄·안 닫힌 블록 0 — PASS
  - 근거: `fence-check.mjs` 문제행 0/9, `TOTAL 0 0 0 69 1 1 2294` (swallowed·unclosed 열 = 0·0).
- [x] SK-05: (B18) 바깥 코드 블록 28곳 모두 정상 — PASS
  - 근거: `site-check.mjs sites.tsv` → `SITES 28 28`, `rc=0`, FAIL/BADANCHOR 줄 0.
- [x] SK-06: (B18) 아홉 파일에서 바뀐 줄이 울타리·주석·빈 줄뿐 — PASS
  - 근거: `line-kinds.py` TOTAL 5열(other) = 0 (`TOTAL 210 28 31 0 0`).
- [x] SK-07: (B18) 끄던 block 꼴 주석 사라지고 남는 것은 MD001 짝뿐 — PASS
  - 근거: 9개 파일 각각 grep 카운트가 계약값(0·0·2·0·0·6·0·0·0)과 일치. design-kit 계열 MD001 예외 grep 0건.
- [x] SK-08: (B19) 열 파일 모양 c3e45f3 와 동일, 레포 전체 촘촘함 변화 0 — PASS
  - 근거: `shape-run.sh c3e45f3 $TIP b19-files.txt` → 10개 파일 모두 2·3열 0, `TOTAL 0 0 0`. wide 비교 TOTAL `0 2 1`(tight열=0).
- [x] SK-09: (B19) 열 파일에서 바뀐 줄이 주석·빈 줄뿐 — PASS
  - 근거: `line-kinds.py` TOTAL `0 24 22 0 0` (2열 fence=0, 5열 other=0).
- [x] SK-10: (B20) 밀린 줄 참조 23곳+페이지 3곳 정상 — PASS
  - 근거: `ref-check.py` → `REFS 31 31`, `rc=0`, 31개 묶음 모두 OK.
- [x] SK-11: (B20·B18) notes 가 고치지 않은 것 넷을 적음 — PASS
  - 근거: 4개 문자열 모두 notes 에서 1건 이상 확인. `.claude/kaizen-input` 외 삭제 0건.

- [ ] **SK-01: (A1) 레포 전체 경고 가운데 시험 입력을 뺀 수가 0 — FAIL**
  - 근거: `bash run.sh $W | awk ... a1-excluded.txt` = **4건** (0이어야 함). 시험 입력 제외 후 잔여 90건은 조건대로 일치.
  - 실제 위반 줄: `docs/react/kit-design/final-integration.md:457:1/8/8/15` — MD060(table-column-style, compact 스타일 표 파이프 앞뒤 공백 누락) 4건.
  - 구현자 자신도 이 결함을 정확히 알고 있었고(RELAXING_PENDING), 원인도 동일(B18 코드펜스 수정 부작용으로 표가 다시 렌더되며 MD060 신규 발생) — 계약이 요구하는 완화 개정(SK-06 조건을 표 구분 줄 한 줄만 예외로 넓히는 것)은 사용자 승인이 있어야 하며, 현재 사이드카 파일이 없어 미승인 상태다.
  - 수정: 사용자가 SK-06 완화 개정에 동의 → 사이드카 amendment 작성(anchored consent) → `final-integration.md:457` 표 구분 줄 칸 띄움만 수정 → 재검증. 또는 동의를 받지 못하면 다른 방식(예: 해당 표를 코드 블록이 아닌 형태로 재구성)으로 SK-06 을 깨지 않고 해결.

### Script (3/3, SC-02 부분검증)
- [x] SC-01: 측정 묶음 14파일 sha256 일치 — PASS
  - 근거: 16개(내부 14 + 바깥 도구 2) 해시 모두 계약 값과 일치 (직접 `git show $TIP:… | shasum` 실행).
- [x] SC-02: 로컬 CI + 9개 킷 시험 — PASS
  - 근거: `ci-local.sh` 19/19 확인된 단계 rc=0 (validate-plugin·sync-evals·sync-docs·sync-orchestrator·run-evals·contrast-claims·docs-links·stale-values·collector-test·react-detect-test·reflect-log-test·reflect-projid-test·reflect-collect-test·onboarding-gate-evals·howto-gate-evals·feedback-save-test·commit-guard-test·dart-format-hook-test·playwright-visuals), feedback-agg-test SKIP(yq 없음, 계약과 동일). 남은 2단계(docs-a11y·scenario-report-ut)는 백그라운드 실행이 평가 시각까지 끝나지 않아 `[샘플링-19/21]` — 결과는 SC-03(docs-a11y 대상 페이지 4개 직접 재확인, PASS)과 self-report(scenario-report-ut rc=0 주장)로 보강.
  - 아홉 개 CI-only 명령은 전부 직접 실행 확인: check-api-kit-docs·detect-docs-drift·check-cause-table-copies·check-reviewer-protocol-copies·measure-helpers-test 전부 rc=0; run-gate-fixtures(24건 불일치 0)·makerworld-fetch-test(5건 불일치 0)·decision-gate-test(21건 불일치 0)·playwright api-kit(8 passed) 모두 계약값과 정확히 일치.
- [x] SC-03: 바뀐 docs 페이지 접근성 — PASS
  - 근거: `check-docs-a11y.js` 4개 페이지(research-log·visual-change-protocol·plugin-validation·overview) → `4/4 PASS`, 가로 넘침 0/0/0/0, 콘솔 에러 0. `assets/site.css` grep 각 1.

### Error (3/3)
- [x] ER-01: block 꼴 markdownlint 지시 0건 — PASS
  - 근거: `line-kinds.py` TOTAL 6열(blockdir) = 0 (`TOTAL 210 54 86 141 0`).
- [x] ER-02: NEXTLINE 줄마다 notes 기록 — PASS
  - 근거: 31개 NEXTLINE 줄 전부 notes 에서 1건 이상 발견(직접 grep, 31/31).
- [x] ER-03: A1 네 파일 새 제목이 대응 페이지에 등장 — PASS
  - 근거: 2건의 새 제목 줄(visual-change-protocol.md) 모두 대응 HTML 에서 발견. 나머지 세 원본은 새 제목 줄 없음(해당 없음 통과).

### Architecture (3/3)
- [x] AR-01: 커밋마다 폴더 하나만, 서명 줄 확인 — PASS
  - 근거: BAD 카운트 0, 커밋 수 17.
- [x] AR-02: 바뀐 경로 전부 범위 목록 안 — PASS
  - 근거: awk 대조 출력 0줄.
- [x] AR-03: 계약 봉인 안 깨짐 — PASS
  - 근거: `seal-count.sh` SEAL_BROKEN 줄 없음(10 ABSENT/119 OK). `.harness` 변경/삭제 파일이 이 계약 파일 외 0건.

### Anti-patterns (2/2)
- [x] AP-03: bare code fence 금지 — PASS (`Total: 14 plugins, 14 OK`, rc=0)
- [x] AP-04: frontmatter name 누락 금지 — PASS (`Total: 14 plugins, 14 OK`, rc=0)

### Reusability (1/1, N/A 1)
- [ ] RE-01: N/A (근거 확인: 저장소 변경이 문서·스킬 본문 모양 수정뿐 — 실제로 diff 대상에 재사용 코드 단위 없음, 사유 참)
- [x] RE-02: 새 저장소 검사 스크립트 미생성 — PASS (`git diff --diff-filter=A` 0건)

### Diagnostics (1/1, N/A 3)
- [ ] DG-01: N/A (사유 확인: `git diff --name-only` 에 `scripts/release.sh` 없음, 0건 — 사유 참)
- [ ] **DG-02: 바꾼 md 파일 markdownlint 경고 0개 — FAIL**
  - 근거: `git diff --name-only $BASE $TIP -- '*.md' ':(exclude).harness'` 대상으로 `run.sh` 실행 → **4건** (0이어야 함). SK-01 과 동일한 `final-integration.md:457` MD060 4건.
  - 수정: SK-01 과 동일 — 완화 개정 승인 또는 다른 해법 필요.
- [ ] DG-03: N/A (사유 확인: `scripts/release.sh` 관련 없음, 실제 시험은 SC-02 가 잼 — 사유 참)
- [ ] DG-04: N/A (사유 확인: 구동할 앱·서버 없음, 페이지 렌더는 SC-03 이 잼 — 사유 참)

## Unverifiable Summary
- invalid_evidence: 0
- env_gaps: 0
- verified_coverage: (28 - 0) / 28 = 1.00 (임계 0.60)
- 연속 ENV 승급: 없음
- Verdict 영향: 통상 (SC-02 는 `[샘플링-19/21]` 로 별도 표기했으나 4 요건 미충족 도구부재 주장이 아니라 실행 중 백그라운드 작업의 시간 제약이며, 확인된 19단계 + 9개 CI-only 명령 + SC-03 교차 확인으로 결합 강도가 충분하다고 판단해 PASS 로 판정. 단 FAIL 조건과 무관하므로 verdict 는 이미 REJECT)

## Discrimination (규칙 12 적용 조건 없음)
- 적용 조건: 해당 없음 (동시성 가드·인증·멱등성·입력검증·데이터유실·마이그레이션·재시도·보안경계 대상 아님)

## Check Artifacts (산출물이 검사인 조건만 — 규칙 10)
- 대상: 이번 스프린트가 만든 검사 스크립트는 14개(측정 묶음) — 전부 SK/ER/AR 조건에서 대상 파일에 직접 실행해 확인했고, 양성 대조(BASE 실측값)도 계약에 명시되어 있어 개별 검사마다 확인함.
- ① 첫 칸만: 해당 없음 (측정 스크립트는 파일 목록 전체를 순회하는 구조, fence-check/line-kinds/ref-check 모두 여러 파일·여러 줄 입력에서 값이 갈림을 확인)
- ② 실행 목록: 해당 없음 (이 검사들은 CI 등록 대상이 아님 — RE-02 로 확인, 새 저장소 검사 미생성)
- ③ 못 읽는 칸: 해당 없음 (전부 정적 스크립트, 부분 실패 없음)
- ④ zsh·bash: 이 평가는 zsh 환경에서 실행(사용자 셸). 계약 자체가 "zsh·bash 같은 결과" 를 전제로 정의했고 구현자가 사전 검증함(공통 정의 절). 평가자는 zsh 로 전부 재실행해 동일 값을 확인함.
- ⑤ 효과 증명: SK-01/DG-02 에서 알려진 위반(final-integration.md:457)을 실제로 검출함을 확인 — 검사가 죽어있지 않음을 실증.

## Evidence Validity
- 검사 대상 증거: 28건 (조건별)
- 무효 판정: 0건
- 셸 스니펫 실행 검증: 실행 24건(0/0/N/A 4건 제외) · zsh 단독 실행(계약이 zsh·bash 동일을 전제로 사전 검증했다고 명시) · 미실행 0건
- 양성 대조: 각 exact 조건마다 계약에 명시된 BASE 실측값을 그대로 재확인 근거로 사용(예: SK-01 BASE 177/90, SK-04 BASE 9/1, SK-05 BASE 28/1, SK-08 BASE 11/1, SK-10 BASE 31/0)
- 무효 0건은 미검증 카운터에 영향 없음

## Summary
- Total: 26/28 conditions passed (2 FAIL: SK-01, DG-02 — 동일 원인)
- Verdict: **REJECT**
- FAIL 요약 및 수정 우선순위:
  1. **SK-01 · DG-02 (동일 결함)**: `docs/react/kit-design/final-integration.md:457` 표 구분 줄에 markdownlint MD060(테이블 파이프 공백) 경고 4건. B18 코드펜스 수정으로 이전에 코드 블록에 묻혀 있던 표가 다시 렌더되며 새로 발생.
  2. 이 결함을 고치려면 SK-06(아홉 파일에서 울타리·주석·빈 줄만 변경)을 「표 구분 줄 칸 띄움 한 줄만 예외」로 완화하는 개정이 필요하며, 계약 배경 절이 이를 `RELAXING_PENDING` 으로 명시하고 있다.
  3. **필요한 결정은 사용자 몫이다** — 완화 개정에 동의하면 `sprint-amendments-after-0928-markdown-rest.md` 사이드카(anchored consent)를 작성하고 그 한 줄만 고쳐 재평가한다. 동의하지 않으면 SK-06 을 깨지 않는 다른 해법(예: 표 구조 자체를 바꾸거나 MD060 룰 자체를 그 줄만 disable-next-line 처리 — 단 이는 ER-02 대상이 되어 notes 기록 필요)을 구현자가 다시 찾아야 한다.
  4. 그 외 26개 조건은 전부 직접 실행 확인으로 PASS했고, 구현자의 self-report 수치와 정확히 일치했다.

## Improvement Suggestions
- [SK-01, DG-02] 범위-미명시 — 계약이 B18 코드펜스 수정과 표 재렌더링의 상호작용(MD060 신규 발생 가능성)을 사전에 예견하지 못해 사후 완화 개정이 필요해졌다. 다음 유사 계약에서는 "코드펜스 수정이 표를 재노출시킬 수 있는 파일"을 GAP 분석 단계에서 미리 markdown-it 렌더로 스캔해 조건에 반영하면 이런 RELAXING_PENDING 상황을 막을 수 있다.
