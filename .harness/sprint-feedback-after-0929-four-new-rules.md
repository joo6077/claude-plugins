# Sprint Feedback
Feature: 새 규칙 넷 — 시각 문자열 · 요구 문서와 결정 기록 경계 · 조회일과 갱신일 · 서비스 계정 선택 순서
Evaluated: 2026-09-29 18:03
Verdict: APPROVE
Iteration: 1

## Contract Fingerprint
- path: /Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak3-nr/.harness/sprint-contract-after-0929-four-new-rules.md
- sha256: f88d7aecee912c45266650560a12673c6d534d68eaa72603fc38cb7c126a5b0e
- status: active
- slug: after-0929-four-new-rules
- contract_root: /Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak3-nr
- contract_root_unconfigured: false
- 선택 근거: ladder 1 명시경로 (호출 시 계약 절대경로를 명시)
- legacy_contract_used: false
- seal_status: SEAL_OK — 단, 설치된 플러그인 캐시(0.16.0)의 `[A-Z]{2,}-[0-9]{2}` 패턴으로는 이 계약(한글 조건 번호)의 조건 줄이 0건 매치되어 `SEAL_BROKEN(actual=e3b0c44298fc1c14, 빈 문자열 해시)`으로 오판됨. 이 레포 자신의 `harness/references/contract-schema.md`(스프린트 시작 판 279085a3 시점부터 이미 존재, 이번 스프린트 범위 밖)는 `([A-Z]{2,}|[가-힣]+)-[0-9]{2}` 로 이미 한글 조건 번호를 지원하며, 그 패턴으로 재계산하면 `conditions_digest=b809213f05ea2d04`·`measurement_digest=a142377bc0fe31be` 로 frontmatter 기록과 완전히 일치함(둘 다 직접 재현). 설치 캐시가 이 레포 자체보다 구식인 상황 — 계약 위·변조가 아니라 스키마 패턴 도구 결함으로 판단하고 레포 로컬 정본을 사용함
- contract_seal_broken: n/a (위 사유로 SEAL_OK 확정)
- measure_status: MEASURE_OK (같은 사유 — 레포 로컬 패턴으로 재계산 시 일치)
- 재확인(Step 5): 일치
- status_transition: active -> done (아래 참고)

## Amendments
- amendments: 0 (사이드카 `sprint-amendments-after-0929-four-new-rules.md` 없음)

## User Correction Audit
- correction_log_status: available (`~/.claude/logs/claude-plugins/2026-09.md`)
- unreflected_corrections: 0 — 계약 생성 시각(2026-09-29 17:23) 이후 창 안에서 세션 `bda55d45…`의 사용자 발언은 17:21:38 "아직도?" 1건뿐이며, 방향 교정이 아니라 진행 확인 질문이라 계약·구현 반영 대상이 아님
- verdict 영향: 없음 (표면화 전용)

## Deletions
- deletions_range: 279085a3..HEAD
- 커밋 구간 삭제: 0
- 커밋하지 않은 삭제: 0
- 선언 밖 삭제: 0

## Cross-Diagnosis Handoff
- 상태: pending-parent
- 부모가 띄울 때 넘길 것: 계약 절대경로 `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak3-nr/.harness/sprint-contract-after-0929-four-new-rules.md` · 이 판정 결과 전문
- 부모가 물을 두 가지:
  1. 계약 조건의 원래 의도와 다르게 해석해 PASS/FAIL 을 오판한 조건이 있는가? (특히 봉인 SEAL_BROKEN 을 레포 로컬 스키마 패턴으로 재판정해 SEAL_OK 로 바꾼 판단이 타당한가)
  2. 0 건·빈 출력을 근거로 PASS 한 조건 중, 문제가 있어도 0 을 냈을 측정(공허한 통과)이 있는가? — measure.py 는 이번 스프린트가 만든 새 검사 스크립트이므로 규칙 10 다섯 가지(아래 Check Artifacts) 결과도 함께 검토
- 부모가 교차 진단을 마친 뒤 `cross_diagnosis_by` 를 `sprint-contract` 로 갱신한다

## Results

### Skill (4/4)
- [x] 스킬-01: backend-kit 원본 둘이 벽시계 문자열 모양을 적는다 — PASS
  - 근거: `python3 .harness/.meta/after-0929-four-new-rules/measure.py 스킬-01` → `checks=9 missing=0` 종료 코드 0. `backend-kit/skills/backend-system/SKILL.md:30` Gotcha 15 줄, `backend-kit/skills/backend-audit/references/audit-criteria.md` Timestamp 행에 다섯/넷 요소 모두 확인 (L3)
- [x] 스킬-02: plan-prd 가 PRD·ADR 경계를 추론 표시로 적는다 — PASS
  - 근거: `m 스킬-02` → `checks=4 missing=0` 종료 코드 0 (L3)
- [x] 스킬-03: 출처 기록이 조회일·갱신일을 따로 적는다 — PASS
  - 근거: `m 스킬-03` → `checks=7 missing=0` 종료 코드 0 (L3)
- [x] 스킬-04: 서비스 계정 선택 순서가 Gotcha 10 에 있다 — PASS
  - 근거: `m 스킬-04` → `checks=8 missing=0` 종료 코드 0. 순서(①~⑤) 판정 함수는 표지 위치를 전부 순서대로 찾으므로 자리바꿈에 민감함 (L3)

### Script (N/A 1)
- [ ] 스크립트-00: N/A (스크립트·검사 미변경) — N/A 확인
  - 근거: `git diff --name-only 279085a3..HEAD -- scripts '*.py' '*.sh' '*.js' ':(exclude).harness'` 빈 출력 (직접 재실행 확인)

### Error (2/2)
- [x] 오류-01: 새로 더한 영어 원문 인용이 대조 파일 글자 그대로다 — PASS
  - 근거: `m 오류-01` → `quotes=9 bad=0 need_missing=0 ex_len=23040` 종료 코드 0. 독립 음성 대조: `database.md` 의 RFC 인용 한 낱말(`relationship`→`relation`)을 임시 사본에서 바꾸자 `bad=1` 종료 코드 1 로 잡힘 (규칙 10 ⑤, L3)
- [x] 오류-02: 가이드 게이트 코드·출력·이웃 규칙 줄이 시작 판과 같다 — PASS
  - 근거: `m 오류-02` → `gate_rc=0,0 gate_tail=[GATE_PASS] checks=6 missing=0` 종료 코드 0 (L3)

### Architecture (8/8)
- [x] 구조-01: 데이터베이스 원칙 10·쪽이 모양과 인용 둘을 싣는다 — PASS
  - 근거: `m 구조-01` → `checks=14 missing=0` 종료 코드 0 (L3)
- [x] 구조-02: PRD 원칙 문서·쪽이 경계를 싣는다 — PASS
  - 근거: `m 구조-02` → `checks=9 missing=0` 종료 코드 0 (L3)
- [x] 구조-03: 셋업 가이드·형식 목록 쪽이 두 날짜 규칙을 싣는다 — PASS
  - 근거: `m 구조-03` → `checks=4 missing=0` 종료 코드 0 (L3)
- [x] 구조-04: 셋업 가이드 쪽 Gotchas 목록이 10 항목이다 — PASS
  - 근거: `m 구조-04` → `gotcha_items=1,2,3,4,5,6,7,8,9,10` `checks=7 missing=0` 종료 코드 0. 독립 음성 대조: 끝 체크리스트의 `Last updated` 를 임시 사본에서 다른 말로 바꾸자 `missing=1(final:Last updated)` 종료 코드 1 로 잡힘 — 목록 끝자리 항목도 놓치지 않음 확인 (규칙 10 ①⑤, L3)
- [x] 구조-05: 드리프트 도구가 원본·쪽 넷을 짝짓고 모두 같은 구간에서 바뀌었다 — PASS
  - 근거: `m 구조-05` → `pairs=4 drift_rc=0 new_marks=0`, `pages_changed` 정확히 기대 4쪽. 독립 음성 대조: 임시 사본에서 `format-checklist.html` 만 시작 판으로 되돌려 커밋하자 `pages_changed` 3쪽 종료 코드 1 로 잡힘(규칙 10 ⑤, L3)
- [x] 구조-06: 바뀐 쪽 넷이 넘치지 않고 접근성 검사를 통과한다 — PASS
  - 근거: `m 구조-06` → `pages=4 bad=0 br_rc=0,0 a11y_ok=4/4 a11y_rc=0` 종료 코드 0. `br.js` 지문 `01c706e939a85586` 이 봉인 커밋 메시지와 일치 (L3)
- [x] 구조-07: 기록 파일에 규칙 넷 커밋·tone-guide·남긴 것이 있다 — PASS
  - 근거: `m 구조-07` → 여섯 낱말 모두 1 이상, `hashes=11`(>=4) 종료 코드 0 (L3)
- [x] 구조-08: 커밋 규칙 — 합침 아님·맨 위 폴더 하나·서명 줄·범위 안 — PASS
  - 근거: `m 구조-08` → 11개 커밋 모두 `OK`, `bad=0 scope_entries=11 git_rc=0`. 독립 음성 대조: 임시 사본에서 범위 밖 파일(`react-kit/README.md`)을 커밋하자 `BAD ... out_of_scope=['react-kit/README.md'] signed=0` `bad=1` 로 잡힘 (규칙 10 ⑤, L3)

### Anti-patterns (3/3)
- [x] 금지-02: force push 금지 — PASS
  - 근거: `git reflog show chore/ak3-nr` 에 `forced-update` 0줄 (직접 재실행)
- [x] 금지-03: bare code fence 금지 — PASS
  - 근거: `python3 scripts/validate-plugin.py --check=code-fence` 종료 코드 0 (`V6 code-fence 0 bare`, 14 plugins OK). 진단-02 의 markdownlint MD040 0건과 중복 확인
- [x] 금지-04: frontmatter name 필드 누락 금지 — PASS
  - 근거: `python3 scripts/validate-plugin.py --check=frontmatter` 종료 코드 0 (`V1 frontmatter 3 skills + 1 agent — OK`)

### Reusability (2/2)
- [x] 재사용-01: 새 컴포넌트를 private 으로 만들지 않았다 — PASS
  - 근거: `git diff --name-only --diff-filter=A 279085a3..HEAD -- . ':(exclude).harness'` 빈 출력(새 파일 0개), 짝 쪽 넷은 구조-05 가 확인
- [x] 재사용-02: 기존 자리에 더했다(신규 대체 아님) — PASS
  - 근거: 스킬-01·스킬-02·스킬-03 측정이 기존 Gotcha/원칙 줄에 더한 것을 확인, 구조-06 넘침 측정은 fs2 번들 `br.js`(지문 일치) 재사용

### Diagnostics (2/2, N/A 3)
- [ ] 진단-01: N/A (commands.analyze 대상 교집합 0) — N/A 확인
  - 근거: `git diff --name-only 279085a3..HEAD | grep -c '^scripts/release.sh$'` = 0
- [x] 진단-02: markdownlint 경고 0건(바뀐 md 8파일) — PASS
  - 근거: 8개 파일 각각 `markdownlint-cli2 --config {"MD013":false}` 결과 `warn=0 ran=1`(직접 재실행, 전량). 양성 대조: `#bad`+연속 빈줄 임시 샘플 → `4 issues` 확인(규칙 10 ⑤)
- [ ] 진단-03: N/A (commands.test 대상 교집합 0) — N/A 확인
  - 근거: 진단-01과 동일 명령, 0
- [ ] 진단-04: N/A (구동 앱·서버 없음) — N/A 확인
  - 근거: `git diff --name-only 279085a3..HEAD -- . ':(exclude).harness' | grep -cvE '^(docs/|backend-kit/|planning-kit/|onboarding-kit/)'` = 0
- [x] 진단-05: 로컬 CI·CI 전용 단계 모두 통과 — PASS
  - 근거: `ci-local.sh` 직접 재실행 → 25단계 전부 `rc=0`(`feedback-agg-test SKIP (yq 없음)` 만 예외), `docs-a11y` 로그 끝 `204/204 PASS`. CI 전용 18개 명령 개별 재실행(`check-api-kit-docs.py` ~ `validate-plugin.py onboarding-kit`) 전부 `rc=0`. `npx playwright test` → `172 passed`. [exact, enumerated] 21개 항목 전수 확인, 누락 없음

## Unverifiable Summary
- invalid_evidence: 0
- env_gaps: 0
- verified_coverage: (25 - 0) / 25 = 1.00 (임계 0.60)
- 연속 ENV 승급: 없음
- Verdict 영향: 통상

## Discrimination (규칙 12 적용 조건만)
- 적용 조건: 없음 — 25개 조건 모두 문서/정적 페이지 규칙 배치와 커밋 위생이 대상이며, 규칙 12의 9항(동시성 가드·인증/권한·멱등성·입력 검증·데이터 유실·마이그레이션 안전성·재시도/중복제거·보안 경계·사용자 결함보고-테스트 충돌) 어디에도 해당하지 않음

## Check Artifacts (measure.py — 이번 스프린트가 만든 새 검사 스크립트, 규칙 10)
- 대상: 스킬-01~04·구조-01~08·오류-01·오류-02 (14조건) — `.harness/.meta/after-0929-four-new-rules/measure.py`
- ① 첫 칸만: `report()` 는 `has()` 로 만든 dict 전 키를 순회해 missing 을 계산 — 첫 항목만 보지 않음. 임시 사본에서 스킬-01 둘째 요소(`type: string`) 제거 → 잡힘, 구조-04 마지막 요소(`final:Last updated`) 제거 → 잡힘. 둘 다 종료 코드 1
- ② 실행 목록: 해당 없음 (measure.py 자체가 대상 조건의 유일한 측정 스크립트이며, 별도 실행 목록에 등록되는 시험 파일이 아님)
- ③ 못 읽는 칸 + 실제 위반: 구조-08 임시 사본에서 범위 밖 파일 커밋(다른 칸의 실제 위반)을 추가 → `BAD ... out_of_scope=[...] bad=1` 로 나머지 칸(OK 11개)과 함께 정확히 구분되어 나옴. 종료 코드 1
- ④ zsh·bash: 해당 없음 (고정 해석기 — `python3 measure.py` 직접 호출, 내부 셸 호출(`오류-02`)도 `bash -c` 로 고정)
- ⑤ 효과 증명: 스킬-01·오류-01·구조-04·구조-05·구조-08 다섯 조건에서 알려진 위반을 임시 사본(`git clone` 격리, 원본 미변경)에 주입 → 전부 종료 코드 1 로 잡힘, 복원 후 종료 코드 0 재확인. 진단-02 markdownlint 는 양성 대조(`#bad`+빈줄) → 4건 확인

## User-Reported Failures
- 없음 (해당 없음)

## Evidence Validity
- 검사 대상 증거: 21건 (PASS 21 + N/A 4)
- 무효 판정: 0건
- 셸 스니펫 실행 검증: 해당 없음 (이 계약은 셸 스니펫 문서화 조건이 아님 — 코드·문서 배치 조건)
- 양성 대조: [진단-02 — 출처: 임시 샘플(`#bad`+연속 빈줄) — 대조 결과 4건, 종료 코드 1]
- 무효 0건은 미검증 카운터에 합산 없음

## Summary
- Total: 21/21 conditions passed (N/A 4: 스크립트-00·진단-01·진단-03·진단-04)
- Verdict: APPROVE

## Improvement Suggestions
- [SEAL] 검증경로-미기재 — `qa-evaluator` 의 봉인 스키마 경로 해석 ladder(1 설치 플러그인 → 2 레포 자체)가 "레포 자신을 평가하는 상황"을 구분하지 않아, 설치 캐시(0.16.0)가 레포 자체의 최신 스키마(한글 조건 번호 지원, `harness/references/contract-schema.md`)보다 구식일 때 `SEAL_BROKEN` 오판을 낸다. 이번엔 레포 로컬 패턴 재계산으로 자체 해소했으나, harness 플러그인 저장소 자신을 대상으로 하는 스프린트에서는 (2) 레포 자체 경로를 (1) 설치 캐시보다 우선하거나, 두 패턴이 다르면 그 사실 자체를 verdict 본문에 경고로 노출하는 규칙을 `qa-evaluator.md` Step 1-e-2 에 추가하는 것을 제안한다
