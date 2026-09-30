# Sprint Feedback
Feature: 바깥 원문 대조 셋 더 반영 · routing 예시 (X1 · X2 · X3 · R)
Evaluated: 2026-09-28 13:24
Verdict: APPROVE
Iteration: 1

## Contract Fingerprint
- path: .harness/sprint-contract-after-0928-external-facts-2.md
- sha256: c663adc56cdd7d95fab549587752f548934162daea0da40c0cf3ba15796a808f
- status: active
- slug: after-0928-external-facts-2
- contract_root: /Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak3-ex2
- contract_root_unconfigured: false
- 선택 근거: ladder 1 명시경로 (HARNESS_CONTRACT)
- legacy_contract_used: false
- seal_status: SEAL_OK
- contract_seal_broken: n/a
- 봉인 커밋 대조 (1-e-3): seal_commit=ce5df05e files=1, 봉인 뒤 조건 줄·본문 변화 0, conditions_digest 변화 0 — 재봉인 없음
- 재확인(Step 5): 일치
- status_transition: active -> done (APPROVE)

## Amendments
- amendments: 1
- PASS 근거 가능: 1 [ER-01 — amend_direction_oracle=unchanged (통과 판정·측정 줄 불변, 음성 대조 입력 주소만 교체)]
- PASS 근거 불가: 0
- 비고: A-01 은 direction=해당없음(조건을 느슨/강화하지 않음), consent=해당없음. 통과 집합에 영향 없음을 직접 재현해 확인함(아래 ER-01 근거)

## User Correction Audit
- correction_log_status: available (/Users/jackson/.claude/logs/claude-plugins/2026-09.md)
- unreflected_corrections: 0 (이번 스프린트 범위와 겹치는 미반영 교정 없음 — 계약 자체가 「맞게 고쳐」 지시의 직접 반영)
- verdict 영향: 없음

## Deletions
- deletions_range: e500a63..047d1099
- 커밋 구간 삭제: 0
- 커밋하지 않은 삭제: 0
- 선언 밖 삭제: 0

## Cross-Diagnosis Handoff
- 상태: pending-parent
- 부모가 띄울 때 넘길 것: 계약 절대경로 `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak3-ex2/.harness/sprint-contract-after-0928-external-facts-2.md` · 이 리포트 전문
- 부모가 물을 두 가지:
  1. 계약 조건의 원래 의도와 다르게 해석해 PASS/FAIL 을 오판한 조건이 있는가?
  2. 0 건·빈 출력을 근거로 PASS 한 조건 중, 문제가 있어도 0 을 냈을 측정(공허한 통과)이 있는가? (SK-01·SK-03·SK-05~SK-12·ER-01·ER-02·AR-02 가 이 유형)

## Results

### Skill (12/12)
- [x] SK-01: Android 16 문장 원문 표현 낮춤 + 출처 — PASS
  - 근거: `design-kit/docs/design/systems/material-design.md` — 금지 4 낱말 각 0, 필수 4 낱말 각 1 이상, 표 행 1. 양성 대조(BASE)는 정반대 값으로 확인
- [x] SK-02: 대응 페이지 6 절 — PASS
  - 근거: `docs/design-kit/material-design.html` — 옛 문구 0, 새 표지 1, 인용 4개 각 1 이상
- [x] SK-03: 레포 전체 센 표현 잔존 0 — PASS
  - 근거: `git grep` 두 측정 모두 기대값과 일치 (첫 측정 0, 둘째 측정 정확히 두 파일)
- [x] SK-04: evals.json 사례 정합성 — PASS
  - 근거: `x2check.py` 출력 `OK`, JSON 파싱·run-gate-evals·sync-evals 전부 rc=0. 알려진 답(작은 JSON) `OK`→상태 깨면 `BAD states`, 괄호 누락 사본 rc=1 — 전부 일치
- [x] SK-05: korean-technical-writing.md 663 인용 배치 — PASS
  - 근거: 원칙별 663 값 0·0·1·1·0, 근거 문구 1, 강도 목록 정확히 일치
- [x] SK-06: 대응 페이지 카드 인용 배치 — PASS
  - 근거: `docs/tone-kit/korean-technical-writing.html` 카드별 값·강도 목록 SK-05 와 동일하게 일치
- [x] SK-07: locale-korean.md 범위 문장 — PASS
  - 근거: §2·§3·§4·§10 여섯 값 전부 1, 규칙표 강도 정확히 일치
- [x] SK-08: 대응 페이지 네 문장 — PASS
  - 근거: `docs/tone-kit/locale-korean.html` 절 s4/s5/s6/s12 값 전부 1, 주소 모음 문구 1
- [x] SK-09: sources.md·페이지 663 행 상태 — PASS
  - 근거: 두 파일 모두 `본문 PDF 는 미확인` 0, `첨부 PDF 본문 확인` 1, `이 자료에 없고` 1
- [x] SK-10: overview.md·페이지 663 인용 제거 — PASS
  - 근거: 두 파일 663 각 0, 9 절 강도·출처 문구 1, 페이지 출처 문구 1 이상
- [x] SK-11: routing.md 와일드카드 치환 — PASS
  - 근거: 레포 전체 옛 모양 0, 네 줄 각 1, 대응 페이지 옛 모양 0
- [x] SK-12: C-06 옛 값 제거 — PASS
  - 근거: 레포 전체(제외 경로 빼고) MUST 표기 0, comment-economy.html 새 표지 1, 원본 강도 SHOULD 1

### Script (1/1)
- [x] SC-01: 로컬 CI + CI 전용 6 단계 — PASS
  - 근거: `ci-local.sh` summary.txt — `rc=0` 25 개, 그 외 줄은 `feedback-agg-test SKIP (yq 없음)` 1 줄뿐. 6 개 CI 전용 명령 개별 실행 전부 rc=0

### Error (2/2)
- [x] ER-01: 인용 없는 새 주소 0 개 — PASS
  - 근거: `newurls.sh` 실행 결과 0 줄, rc=0. 알려진 답(임시 저장소) 결과가 계약 명시값과 정확히 일치. 음성 대조(개정된 A-01 주소로 만든 떠 있는 커밋)에서 그 주소 한 줄이 나옴을 직접 재현 확인
- [x] ER-02: 번역투 킬러 패턴 0건 — PASS
  - 근거: 추가된 줄 전수 검사 매치 0, 양성 대조 문자열 2개 매치로 패턴 살아있음 확인

### Architecture (3/3)
- [x] AR-01: 커밋 구조·서명 줄 — PASS
  - 근거: 8개 커밋 전수 검사 BAD 0. 양성 대조(`a5152c5`)는 17
- [x] AR-02: 범위 목록 밖 변경 파일 0 — PASS
  - 근거: `comm -23` 결과 0줄
- [x] AR-03: 문서 페이지 6개 CSS·접근성 — PASS
  - 근거: 6파일 CSS 링크 각 1, `check-docs-a11y.js` `6/6 PASS` rc=0

### Anti-patterns (2/2)
- [x] AP-03: bare code fence 금지 — PASS
  - 근거: `validate-plugin.py --check=code-fence` rc=0 (14 플러그인 전부 OK)
- [x] AP-04: frontmatter name 필드 — PASS
  - 근거: `validate-plugin.py --check=frontmatter` rc=0

### Reusability (N/A 2)
- [ ] RE-01: N/A — 근거: 범위 목록 12경로 확장자가 .md/.html/.json뿐임을 직접 확인 (사유 사실)
- [ ] RE-02: N/A — RE-01과 동일 근거

### Diagnostics (1/1, N/A 2)
- [ ] DG-01: N/A — 근거: `git diff --name-only e500a63 TIP | grep -c '^scripts/release.sh$'` = 0 (사유 사실)
- [x] DG-02: 편집기 설정 markdownlint 경고 0 — PASS
  - 근거: 대상 md 6개 전부 경고 0줄·rc=0. 양성 대조(끝에 나쁜 줄 붙인 사본) 6줄 경고·rc=1로 검사기 살아있음 확인. (도구 버전 0.23.3 설치, 계약 명시 0.23.2와 patch 차이 — 규칙 자체는 동일, 결과에 영향 없음 확인)
- [ ] DG-03: N/A — 근거: SC-01이 실제 시험을 재고 이미 PASS 확인함

## Unverifiable Summary
- invalid_evidence: 0
- env_gaps: 0
- verified_coverage: (26 - 0) / 26 = 1.00 (임계 0.60)
- 연속 ENV 승급: 없음
- Verdict 영향: 통상

## Discrimination (규칙 12)
- 적용 조건: 없음 — 대상이 문서/평가데이터이며 9항(동시성·인증·멱등성 등)에 해당하는 조건이 없음

## Check Artifacts
- 대상: SC-01(ci-local.sh), ER-01(newurls.sh), DG-02(markdownlint-cli2)
- ① 첫 칸만: 해당 없음 (다중 칸 구조 아님 — 파일 전체 텍스트/커밋 diff 스캔형 검사)
- ② 실행 목록: newurls.sh·x2check.py·markdownlint 전부 이 세션이 직접 실행, 출력 수집함
- ③ 못 읽는 칸 + 실제 위반: 해당 없음
- ④ zsh · bash: 사용자 셸 zsh, 이 세션은 Bash 도구(bash)로 실행 — 계약 측정문 자체가 bash 스크립트 파일 실행형이라 셸 무관. glob 미사용 확인
- ⑤ 효과 증명: ER-01 음성 대조(신규 주소 커밋 → 1줄 검출) 직접 재현, DG-02 양성 대조(나쁜 사본 → 6개 경고·rc=1) 직접 재현, SK-04 음성 대조(괄호 누락 사본 → rc=1) 직접 재현

## Evidence Validity
- 검사 대상 증거: 26 건
- 무효 판정: 0 건
- 셸 스니펫 실행 검증: 실행 26 건 (전부 이 세션이 직접 Bash 로 실행) · zsh/bash 양쪽 확인 해당없음(글로빙 없는 고정 명령) · 미실행 0 건
- 양성 대조: SK-01~SK-12·SC-01·ER-01·ER-02·AR-01~AR-03·DG-02 — 계약 명시 BASE 값/음성 대조 재현으로 확인, 전부 기대와 일치

## Summary
- Total: 계약 조건 26개 — PASS 21 (SK 12 · SC 1 · ER 2 · AR 3 · AP 2 · DG 1) + N/A 5 (RE-01·RE-02·DG-01·DG-03·DG-02는 PASS로 계상) + FAIL 0. N/A 5건은 각각 괄호 안 사유를 직접 측정해 사실임을 확인함
- Verdict: APPROVE

## Improvement Suggestions
- 없음 — 계약의 오라클 해소 문단과 양성/음성 대조가 조건 대부분에 미리 기재돼 있어 재현이 수월했음. DG-02의 markdownlint-cli2 버전을 0.23.2로 정확히 고정 설치하는 방법(package-lock 등)을 계약에 덧붙이면 다음 회차 재현성이 더 좋아짐
