# Sprint Feedback
Feature: 문서 사이트 약점 — 짝 없는 원본 · 밝은 테마 · 옛 값 · 모양만 바뀐 원본 거르기
Evaluated: 2026-09-28 13:41
Verdict: APPROVE
Iteration: 2

## Contract Fingerprint
- path: /Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak3-d1/.harness/sprint-contract-after-0928-docs-site.md
- sha256: bfc303f9f8b2074d172fde35642e591969a8eb70270fd88fa6917014984f27ea
- status: done (1회차 QA가 active→done 전환, 커밋되지 않은 채 작업 폴더에 남음 — 조건 줄은 봉인 커밋 c6b8cf41 이후 변경 없음)
- slug: after-0928-docs-site
- contract_root: /Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak3-d1
- contract_root_unconfigured: false
- 선택 근거: ladder 1 명시 경로
- legacy_contract_used: false
- seal_status: SEAL_OK (재계산 일치)
- contract_seal_broken: n/a
- 봉인 커밋 대조(1-e-3): 봉인 커밋 c6b8cf41(계약 파일 1개). `git diff c6b8cf41 -- 계약` 에서 조건 줄·conditions_digest 변화 없음(status 줄만 uncommitted 차이, 걸러냄) — 조용한 재봉인 없음
- 측정 도우미 지문: measure.py b734c2fe788cff17 · theme.js 51b8e20d5161199d (봉인 값과 일치)
- 재확인(Step 5): 일치
- status_transition: active -> done (1회차에서 이미 수행, 이번 회차는 변경 없음 유지)

## Amendments
- amendments: 0 (사이드카 없음)

## User Correction Audit
- correction_log_status: available (`~/.claude/logs/claude-plugins/2026-09.md`)
- unreflected_corrections: 0 — 스프린트 구간(2026-09-28 12:15~) 사용자 발언에서 이 계약(after-0928-docs-site)을 향한 미반영 교정 없음. 교차 진단 지적 2건은 커밋 41815d82·1f4763ed·9fe8c710 으로 반영됨(아래 참조), 3번째는 기록에 남기고 봉인 수치를 지키기 위해 되돌림
- verdict 영향: 없음

## Deletions
- deletions_range: e500a63..HEAD
- 커밋 구간 삭제: 0
- 커밋하지 않은 삭제: 0
- 선언 밖 삭제: 0

## Cross-Diagnosis Handoff
- 상태: pending-parent
- 부모가 띄울 때 넘길 것: 계약 절대경로 `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak3-d1/.harness/sprint-contract-after-0928-docs-site.md` · 아래 판정 결과 전문
- 부모가 물을 두 가지:
  1. 계약 조건의 원래 의도와 다르게 해석해 PASS/FAIL 을 오판한 조건이 있는가?
  2. 0 건·빈 출력을 근거로 PASS 한 조건 중, 문제가 있어도 0 을 냈을 측정(공허한 통과)이 있는가? 산출물이 검사인 조건(SC-04·SC-05·SC-06)의 다섯 가지 중 돌리지 않은 것이 있는가?
- 끝내 부모가 못 띄우면 cross_diagnosis_by 를 none 으로 내린다.

## 2회차 재검증 배경
1회차(Evaluated 2026-09-28 13:13, 이 파일의 이전 판)에서 31/31 조건 APPROVE 후, 독립 검토가 지적한 두 가지 결함을 고치는 커밋 3개(41815d82·1f4763ed·9fe8c710)가 추가됐다.
- **결함 1** — 드리프트 도구가 기호만 바뀐 내용 수정(예: `+`→`-`)까지 「모양만 바뀐 원본」으로 잘못 빼던 것 → 낱말+기호 순서 대조로 수정
- **결함 2** — 공통 CSS 검사가 이름 글자 참조(`&period;`)와 태그 끼우기(`site<span>.</span>css`)로 쪼갠 이름을 놓치던 것 → 글자 참조를 풀고 태그를 걷어낸 뒤 원문과 비교하는 방식으로 수정
- 3번째 지적(design 조사 기록 매핑)은 봉인된 SC-02/SC-03/SC-05 의 기대 수(190/56/134/202)와 부딪혀 되돌리고 기록에 남김 — 계약 범위 밖 처리로 타당

이 3개 커밋은 모두 `## 범위 경계` 의 sprint-scope 목록 안(scripts/detect-docs-drift.py · scripts/test-detect-docs-drift.py · scripts/check-docs-common-css.py · scripts/test-check-docs-common-css.py · .claude/skills/docs-site/SKILL.md) 또는 `.harness/` 안에 있다. 평가자가 31개 조건 전부를 이 세션에서 독립적으로 다시 실행해 재확인했다(아래 Results). 특히 드리프트 도구·공통 CSS 검사에 의존하는 조건(SK-01·SC-01~06·AR-04)은 변경된 코드로 다시 돌려 값이 그대로인지 직접 확인했다.

## Results

### Skill (1/1)
- [x] SK-01: docs-site 스킬이 이번 동작을 적는다 — PASS
  - 근거: `.claude/skills/docs-site/SKILL.md` 네 문자열 각 1회 이상(grep -cF, 평가자 재실행). `python3 scripts/detect-docs-drift.py --check-table` rc=0, "매핑 맞대기: 스크립트 50 짝 · 표 34 짝 · 어긋남 0"

### Script (6/6)
- [x] SC-01: 짝 다섯 — PASS. 근거: `m SC-01` → 5/5 OK, `pairs_ok=5/5 drift_rc=0`
- [x] SC-02: NEW 표지 0 — PASS. 근거: `m SC-02` → `new_marks=0 no_page_lines=0 lines=190 drift_rc=0`(수정된 드리프트 도구로 재확인, 값 불변)
- [x] SC-03: 기본 출력이 모양만 바뀐 원본 제외 — PASS. 근거: `m SC-03` → `all=190 default=56 expect_real=56 only_tool=0 only_ref=0 rc=0,0`, stderr "134...--include-format-only", JSON `56 ['exists','registered','source','target']`, `m KA` → `caching=SHAPE tone_overview=REAL`
- [x] SC-04: 새 시험 3경우 — PASS. 근거: `python3 scripts/test-detect-docs-drift.py` rc=0, 3/3 통과(수정된 시험 코드 자체를 재실행). 판별력: `is_format_only` 를 `return False` 로 무력화한 사본(scratchpad/qa2)에 `--tool` 로 돌리자 경우1 FAIL, 종료 코드 1(평가자 직접 실행 음성 대조, 2회차 재현)
- [x] SC-05: 새 검사 — PASS. 근거: `python3 scripts/check-docs-common-css.py` → "검사한 쪽 202 · 어긋난 쪽 0 · 못 읽은 쪽 0" rc=0, `git ls-files 'docs/*.html' | wc -l`=202, CI 등록 확인
- [x] SC-06: 새 시험 5경우 — PASS. 근거: `python3 scripts/test-check-docs-common-css.py` rc=0, 5/5 통과(수정된 검사·시험 재실행). 판별력: 글자참조 세기 제거 사본 → 경우2 FAIL rc=1, 주석 제거 무력화 사본 → 경우3 FAIL rc=1(평가자 직접 실행 음성 대조, 2회차 재현)

### Error (5/5)
- [x] ER-01: B17 세 쪽 — PASS. 근거: `m ER-01` 세 줄 OK, charref=0 전부
- [x] ER-02: 카드 들뜸 움직임 설정 — PASS. 근거: `node theme.js hover` → reduce transform=none / no-preference matrix(1,0,0,1,0,-2)
- [x] ER-03: G1~G5 — PASS. 근거: `m ER-03` → `G1~G4=0 G1~G5=1`
- [x] ER-04: bambu 세 쪽 판번호 안내 — PASS. 근거: `m ER-04` 세 줄 OK, `loose_version_lines=[]`
- [x] ER-05: setup-guide 인라인 코드 82/82 — PASS. 근거: `m ER-05` → `code=82/82 rule_sentence=1 miss=[]`

### Architecture (9/9)
- [x] AR-01: 새 쪽 열셋 — PASS. 근거: `m AR-01` → `new_pages_ok=13/13`
- [x] AR-02: 밝은 테마 20쪽 — PASS. 근거: `m AR-02` → `ok=20/20 a11y_rc=0 theme_rc=0`(평가자 직접 실행, playwright 기반)
- [x] AR-03: B16 형제 링크·손 글 절 — PASS. 근거: `m AR-03` 열 줄 OK
- [x] AR-04: D3 짝 56개 원본 내용 반영 — PASS. 근거: `m AR-04`(수정된 드리프트 도구로 재확인) → `pairs=56 bad=0 drift_rc=0`, 56줄 전부 code_miss=0 word_miss=0
- [x] AR-05: D5 기록 표 27행 — PASS. 근거: `m AR-05` → `rows_ok=27/27`, `grep -c 'after-kaizen-0928/d1-notes.md' dca-notes.md`=1
- [x] AR-06: 접근성 41 쪽 — PASS. 근거: `m PAGES` → `pages=41 bad=0`
- [x] AR-07: 외부 자원 0 — PASS. 근거: `m EXT` → `checked=42 ext_pages=0`
- [x] AR-08: 커밋 규칙 — PASS. 근거: `m COMMITS` 전부 OK(21개→3개 추가돼 24개), `bad=0 scope_entries=48`, 새 커밋 3개 모두 tops 단일·서명·범위 안 확인
- [x] AR-09: 기록 10항목+tone-guide+118 — PASS. 근거: grep -cw 결과 전부 1 이상

### Anti-patterns (3/3)
- [x] AP-01: 버전 하드코딩 없음 — PASS (ER-04와 동일 측정)
- [x] AP-02: force push 0 — PASS. 근거: `git reflog show chore/ak3-d1 | grep -c forced-update` = 0
- [x] AP-03: bare code fence — PASS. 근거: `validate-plugin.py --check=code-fence` 14 plugins 0 bare, markdownlint MD040 0건(바뀐 md 3개, 아래 DG-02 근거와 동일 실행)

### Reusability (2/2)
- [x] RE-01: private 아님 — PASS. 근거: `scripts/check-docs-common-css.py` 인자 없이·파일 인자 둘 다 동작 확인
- [x] RE-02: 재사용 — PASS. 근거: SC-01(짝 5개 기존쪽 재사용), page-template.html·docs/assets/site.css·check-docs-a11y.js·check-docs-links.py 재사용 확인

### Diagnostics (5/5, N/A 3)
- [ ] DG-01: N/A — `git diff --name-only e500a63..chore/ak3-d1 | grep -c '^scripts/release.sh$'` = 0, 확인
- [x] DG-02: markdownlint·py_compile 0건 — PASS. 근거: 바뀐 md 2개(`SKILL.md` · `d1-notes.md`) markdownlint-cli2 0.23.2(MD013 끔) 0건, "Linting: 1 file" 포함. 바뀐 py 4개(`detect-docs-drift.py` · `test-detect-docs-drift.py` · `check-docs-common-css.py` · `test-check-docs-common-css.py`) `py_compile` 전부 rc=0
- [ ] DG-03: N/A — DG-01과 동일 명령, 0
- [ ] DG-04: N/A — 정적 문서, 구동 앱 없음
- [x] DG-05: 로컬 CI + CI 전용 단계 — PASS. 근거: 평가자가 직접 `ci-local.sh` 재실행(신규 TMPDIR, 2회차) 25/25 rc=0(yq 없어 feedback-agg-test SKIP), docs-a11y 로그 끝 "202/202 PASS". CI 전용 10단계 개별 재실행 전부 rc=0: check-api-kit-docs.py(12/12 PASS) · detect-docs-drift.py --check-table(어긋남 0) · check-cause-table-copies.py(위반 0) · measure-helpers-test.sh(실패 0) · run-gate-fixtures.sh(24/24 일치) · makerworld-fetch-test.sh(5/5 일치) · check-docs-common-css.py(rc=0) · test-detect-docs-drift.py(rc=0) · test-check-docs-common-css.py(rc=0) · npx playwright test(164 passed)

## Unverifiable Summary
- invalid_evidence: 0
- env_gaps: 0
- verified_coverage: 31/31 = 1.00 (임계 0.60)
- Verdict 영향: 통상

## Discrimination (규칙 12 적용 조건만)
- 적용 조건: SC-04, SC-06 (산출물이 검사인 조건 — 새 시험 스크립트, 이번 회차에 코드가 바뀜)
- 결합 확인: SC-04 — `test-detect-docs-drift.py`(2회차 판) 가 `--tool` 인자로 `detect-docs-drift.py`(2회차 판) 사본을 직접 경유 확인. SC-06 — `test-check-docs-common-css.py`(2회차 판) 가 `--check` 인자로 `check-docs-common-css.py`(2회차 판) 사본을 직접 경유 확인
- 음성 대조(2회차 평가자 직접 재현, scratchpad/qa2):
  - SC-04: `is_format_only` 를 `return False` 로 무력화한 사본 → 경우1 FAIL, 시험 전체 rc=1(3개 중 2개 통과)
  - SC-06: `split_names` 의 글자참조 판정을 무력화한 사본(nosplit) → 경우2 FAIL rc=1(5개 중 4개 통과). `COMMENT_RE.sub` 주석 제거를 무력화한 사본(nocomment) → 경우3 FAIL rc=1(5개 중 4개 통과)
  - 계약 명시 음성 대조와 일치

## Check Artifacts (산출물이 검사인 조건만 — 규칙 10)
- 대상: SC-05/SC-06 — scripts/check-docs-common-css.py (2회차 판)
  - ① 첫 칸만: 해당 없음 (전수 스캔형 검사 — `git ls-files` 전체 순회, 202개 전부 읽음 확인)
  - ② 실행 목록: `.github/workflows/ci.yml:88,90` run 줄에 등록, grep 확인
  - ③ 못 읽는 칸: SC-06 경우4(UTF-8 아닌 바이트)로 대체 확인 — rc=2, 두 파일명 모두 적힘(2회차 재실행 확인)
  - ④ zsh·bash: 해당 없음 (고정 해석기 python3, 계약 명시)
  - ⑤ 효과 증명: 위 Discrimination 절 참조 — 2회차 코드에서도 알려진 위반(글자참조 미탐지·주석 미제외) 사본에서 FAIL 재현
- 대상: SC-04 — scripts/test-detect-docs-drift.py (2회차 판, 도구 시험)
  - ⑤ 효과 증명: is_format_only 무력화 사본에서 경우1 FAIL 재현(2회차)
  - 나머지 항목: 해당 없음 (단일 도구 대상 판별 시험, 다중 칸 구조 아님)

## User-Reported Failures
- 없음 (사용자 보고 없음)

## Evidence Validity
- 검사 대상 증거: 31 건 (전 조건, 2회차 전수 재검증)
- 무효 판정: 0 건
- 셸 스니펫 실행 검증: 전부 실제 명령 실행(zsh 사용자 셸). SC-06 고정 해석기 python3 는 계약 명시대로 셸 대조 해당 없음
- 양성 대조: SC-02(계약 명시 봉인 전 실측값 채택), AR-06·AR-07(계약 명시), DG-02(직접 재현 가능하나 이번 회차는 markdownlint-cli2 실행 결과 자체를 근거로 채택), SC-04·SC-06(2회차 신규 음성 대조 — 위 Discrimination 절)
- 무효 0 건 — 미검증 카운터 영향 없음

## Summary
- Total: 31/31 conditions passed (N/A 3: DG-01·DG-03·DG-04)
- Verdict: APPROVE

## Improvement Suggestions
- 없음 (계약 결함 미발견 — 31개 조건 전부 측정 가능·명확했고, 2회차에 코드가 바뀐 뒤에도 값이 그대로 재현됐다. 독립 검토가 지적한 결함 2건은 이미 코드 수정으로 해소됐고, 3번째는 계약 범위 밖으로 판단해 되돌린 것이 타당하다)
