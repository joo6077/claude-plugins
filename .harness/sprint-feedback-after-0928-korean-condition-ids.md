# Sprint Feedback
Feature: 계약 조건 번호를 한국어 이름으로 (묶음 id — SK · SC · ER · AR · RE · DG · AP → 스킬 · 스크립트 · 오류 · 구조 · 재사용 · 진단 · 금지)
Evaluated: 2026-09-29 10:05
Verdict: APPROVE
Iteration: 1

## Contract Fingerprint
- path: /Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak3-id/.harness/sprint-contract-after-0928-korean-condition-ids.md
- sha256: 84708ec58ec123e04f40c010e7c9b482edc7363afcbdcd847038352232f3b681
- status: active
- slug: after-0928-korean-condition-ids
- contract_root: /Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak3-id
- contract_root_unconfigured: false
- 선택 근거: ladder 1 명시경로 (HARNESS_CONTRACT 로 고정, test -f 확인 통과)
- legacy_contract_used: false
- seal_status: SEAL_OK — 단, 설치된 플러그인(0.16.0)이 아니라 이 작업 폴더(worktree) 자체의 `harness/references/contract-schema.md` 정의(이번 스프린트가 이미 커밋한 새 정규식)로 확인했다. 설치된 플러그인은 옛 정규식만 읽어 한국어 번호를 인식하지 못하므로, 그걸로 확인하면 빈 값 지문(`e3b0c44298fc1c14`)이 나와 거짓으로 `SEAL_BROKEN` 이 뜬다 — 계약 자신의 배경 절(19·23 줄)이 이 문제를 미리 밝혀 두었다. 두 방식 모두 bash·zsh 양쪽에서 실행해 확인했다.
- contract_seal_broken: n/a
- measure_status: MEASURE_OK (같은 방식, 같은 사유)
- 재확인(Step 5): 일치 (git status 변경 없음, 지문 동일)
- status_transition: active -> done (평가 완료 뒤 전환)
- 봉인 커밋 대조(Step 1-e-3): 봉인 커밋 `1a8b4018` 는 계약 파일 1개만 담았고, 그 뒤 산문 차이 0줄·지문 변경 0줄 — 재봉인 없음

## Amendments
- amendments: 0 (사이드카 파일 없음)

## User Correction Audit
- correction_log_status: available (`~/.claude/logs/claude-plugins/2026-09.md`)
- unreflected_corrections: 0 — 이 세션의 사용자 발언은 계약 만들기 전 09:06:30 한 번뿐이고("1 나 2 가", 다른 안건에 대한 답), 계약 생성(09:21)부터 봉인(09:38)과 그 뒤 구현 커밋까지는 추가 사용자 개입 기록이 없다(사용자 위임 "자동으로 다 진행해 나한테 묻지 말고" 그대로 진행됨. 계약 배경 절 17줄에 인용).
- verdict 영향: 없음 (표면화 전용)

## Deletions
- deletions_range: 66e6c74b..chore/ak3-id
- 커밋 구간 삭제: 0
- 커밋하지 않은 삭제: 0
- 선언 밖 삭제: 0

## Cross-Diagnosis Handoff
- 상태: pending-parent
- 부모가 띄울 때 넘길 것: 계약 절대경로 `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak3-id/.harness/sprint-contract-after-0928-korean-condition-ids.md` · 이 리포트 전문
- 부모가 물을 두 가지:
  1. 계약 조건의 원래 의도와 다르게 해석해 PASS/FAIL 을 오판한 조건이 있는가? — 특히 구조-05 의 "끝 줄 rc=0" 해석(아래 근거 참고)을 다시 봐 달라.
  2. 0 건·빈 출력을 근거로 PASS 한 조건 중, 문제가 있어도 0 을 냈을 측정(공허한 통과)이 있는가?
- 부모가 교차 진단을 마친 뒤 `cross_diagnosis_by` 를 `sprint-contract` 로 갱신한다. 끝내 띄우지 못했으면 `none` 으로 내리고 사유를 기록한다.

## Results

### Skill (7/7)
- [x] 스킬-01: 조건 줄을 읽는 네 문서의 정규식이 모두 두 형식을 읽는 한 모양으로 바뀐다 — PASS
  - 근거(L3, 실행): 네 파일 모두 `grep -oF '[A-Z]{2,}-[0-9]{2}'` = 0, `grep -oF '[A-Z][A-Z]+-[0-9][0-9]'` = 0. `grep -oF '([A-Z]{2,}|[가-힣]+)-[0-9]{2}'` = contract-schema.md 5(기준4↑) · SKILL.md 6(기준6↑) · qa-evaluator.md 2(기준2↑) · qa-evaluation-guide.md 1(기준1↑). awk 모양은 contract-schema.md 2(기준2↑), 나머지 0(기준0↑). 커버리지 검출기(§측정 커버리지 표기 bash 블록)를 그대로 떼어 `fixture-coverage.md` 에 돌리자 `UNCOVERED` 정확히 두 줄, `스킬-99:` 와 `SK-98:` — 계약이 적은 값과 글자까지 일치.

- [x] 스킬-02: 기능 조건 세기 awk 가 한국어 자동 번호도 뺀다 — PASS
  - 근거(L3, 실행): `fcount.sh harness/skills/sprint-contract/SKILL.md fixture-mixed.md` → `2`, `fcount.sh harness/references/contract-schema.md fixture-mixed.md` → `2`. 둘 다 "알려진 답"(스킬-01·SK-03 둘)과 일치.

- [x] 스킬-03: 새 계약의 틀이 한국어 자동 번호만 쓴다 — PASS
  - 근거(L3, 실행): 측정(1) 옛 틀 줄 `(RE-0[12]|DG-0[1-4]|AP-00):` 두 파일 모두 0(기준 7·12). 측정(2) 한국어 여섯 줄(재사용-01·재사용-02·진단-01~04) 두 파일 모두 각 1. 측정(3) `AP-00: N/A` 네 파일 모두 0, `금지-00: N/A` 각 1 이상(SKILL.md 2·contract-schema.md 2·red-flags.md 1·contract-design-guide.md 1).

- [x] 스킬-04: 계약 형식 문서에 옛 번호·새 번호 짝 일곱과 "옛 계약도 같은 뜻으로 읽힌다" 문장 — PASS
  - 근거(L3, 실행+Read): 일곱 짝(`SK`~`스킬` 등) 각 1. "옛 계약(영어 번호 SK-01 · DG-01)은 고치지 않고 그대로 읽힌다" 문장 확인(532~542줄, 실제 표와 문장 Read로 직접 확인).

- [x] 스킬-05: 규칙 자리 17곳에 영어 홀로 남은 줄 없이 모두 한국어 번호 있음 — PASS
  - 근거(L3, 실행): `lone-ids-all.sh` 끝 줄 `regions=17 not_clean=0`(기준 `not_clean=17`). 손으로 만든 대조 입력(`머리/DG-01 a/진단-01 (옛 DG-01)/실측 DG-02/끝`)에 같은 검사 스크립트를 돌리자 `region=4 lone=1 ko=1` — 즉 계약이 틀리지 않았다면 이 검사가 실제로 위반을 잡아낸다는 것을 직접 확인. 없는 머리로는 `NO_REGION` 종료 코드 2.

- [x] 스킬-06: 킷 reviewer 여덟과 flutter-audit 사본이 원문과 글자까지 같음 — PASS
  - 근거(L3, 실행+변조 시험): `check-reviewer-protocol-copies.py` → `checked=9 violations=0 infra_errors=0 excluded=0` 종료 코드 0. 별도 임시 폴더에 스크립트와 파일 11개를 복사해 같은 결과 재현 뒤, `rust-reviewer.md` 한 글자("산출물에"→"산출물이")를 바꾸자 `MISMATCH ... violations=1` 종료 코드 1 — 검사가 실제로 위반을 구분한다는 것을 직접 확인.

- [x] 스킬-07: 평가 사례가 새 해당 없음 줄을 찾는다 — PASS
  - 근거(L3, 실행): `assertions.json` 에 `"금지-00: N/A"` 1·`AP-00` 0. `expected-improvements.md` 에 `AP-00` 0·`금지-00` 1 이상. `run-kaizen-assertions.py` 끝 줄 `Total: 14 passed, 0 failed`, `PASS contract-kaizen/vacuous-boilerplate#1` 줄 확인. 대조: 옛 SKILL.md(66e6c74b)에서 같은 검사는 `금지-00: N/A` 0건 — 검사가 옛 문서와 새 문서를 실제로 가른다.

### Script (6/6)
- [x] 스크립트-01: 옛 계약 240개의 조건 수·두 지문·봉인 판정이 고친 뒤에도 안 바뀐다 — PASS
  - 근거(L3, 실행): `compat.sh` 를 bash·zsh 양쪽에서 돌려 `base-old.txt` 와 diff, 둘 다 차이 0줄. 조건 수 합 4930, `SEAL_OK` 127·`SEAL_ABSENT` 113·`MEASURE_OK` 38·`MEASURE_ABSENT` 202 — 계약이 적은 값과 일치. 대조: 정규식에서 영어 쪽을 뺀 사본으로 같은 검사를 돌리자 차이가 `grep -c '^<'` 217, `grep -cE '^[<>]'` 434 — 계약이 적은 값과 정확히 같다. 이 검사가 실제로 옛 계약 판정 변화를 잡아낸다는 것을 직접 확인.

- [x] 스크립트-02: 고친 규약의 함수가 한국어 번호 시험 계약을 읽는다 — PASS
  - 근거(L3, 실행): bash·zsh × 로캘 셋(C·en_US.UTF-8·ko_KR.UTF-8) 여섯 번 모두 `8b52386c713a6054`·`c51d48673b5caeee`. 조건 수 7.

- [x] 스크립트-03: 공용 측정 시험에 한국어 번호 확인이 들어가고 통과한다 — PASS
  - 근거(L3, 실행): `measure-helpers-test.sh` 종료 코드 0, 끝 줄 "실패 0 건", `^PASS K` 3줄(기준 2 이상), `^PASS` 22줄(기준 21 이상). 시험 파일 안에 두 지문 문자열 각 1. 대조: 임시 폴더에 옛(66e6c74b) contract-schema.md 를 넣고 같은 시험을 돌리자 `FAIL K` 3줄, 종료 코드 1 — 이 시험이 실제로 옛 규약과 새 규약을 가른다.

- [x] 스크립트-04: 금지 패턴 반복 알림이 한국어·옛 번호 모두 읽는다 — PASS
  - 근거(L3, 실행): `금지-01 금지-01 금지-01` → `rc=0 out=[TRIGGER: Anti-pattern 반복: 금지-01 (3회)]`. `AP-01 AP-01 AP-01` → 같은 모양. `금지-01 금지-01 AP-01`(번호 다름, 안 합침) → `rc=1 out=[]`. 세 값 모두 계약과 글자까지 일치.

- [x] 스크립트-05: 설정 검사가 금지 패턴을 두 형식으로 세고 0건에도 경고를 낸다 — PASS
  - 근거(L3, 실행): 다섯 식 모두 `interr=0`(옛 버그였던 "0\n0: integer expected" 없음). `s/id: 금지-0([234])/id: ZZ-0\1/` 와 `s/id: 금지-0/id: ZZ-0/` 만 `apwarn=1`, 나머지 셋(무변화·전부 AP-·일부 AP-)은 `apwarn=0` — 계약이 적은 값과 완전히 일치. `validate.sh:72~74` 를 직접 읽어 `grep -cE "id: (AP|금지)-"` + `|| AP_COUNT=0` 으로 옛 버그가 고쳐졌음을 코드로 확인.

- [x] 스크립트-06: 이 레포 설정과 설정 틀이 한국어 앞자리·금지 패턴 번호를 쓴다 — PASS
  - 근거(L3, 실행): `.harness/project.yaml` 의 `contract_categories` 8줄이 `스킬`·`스크립트`·`오류`·`구조` 그대로. `금지-0[1-4]` 4줄, `AP-` 0줄. `harness/templates/project.yaml` 도 주석 `금지-0[12]` 2줄, `AP-` 0줄.

### Error (3/3)
- [x] 오류-01: 한국어 번호 계약도 봉인이 변조를 잡는다 — PASS
  - 근거(L3, 실행): `seal-korean.sh` 출력 두 줄(bash·zsh) 모두 `sealed=SEAL_OK,MEASURE_OK cond_changed=SEAL_BROKEN,MEASURE_OK measure_changed=SEAL_OK,MEASURE_BROKEN` — 계약과 글자까지 일치. 조건 문구를 바꾸면 조건 봉인만 깨지고, 측정 줄을 바꾸면 측정 봉인만 깨지는 것을 직접 확인.

- [x] 오류-02: 봉인된 옛 계약·QA 리포트·개정 파일이 한 글자도 안 바뀐다 — PASS
  - 근거(L3, 실행): `git diff --name-only 66e6c74b chore/ak3-id -- .harness` 를 계약이 정한 제외 목록으로 거르면 0. 대조: 봉인 전(fc3fab3e) 기준으로도 0, 가짜 파일명 한 줄을 목록에 더하면 1로 바뀜 — 이 검사가 실제로 허용 밖 변경을 잡아낸다는 것을 확인.

- [x] 오류-03: 쉬운 말 목록에서 두 줄만 빠지고 읽는 두 훅이 정상 동작 — PASS
  - 근거(L3, 실행): 백업 파일이 git에 들어 있고 지문 앞 16자리 `694f07858cf9016c` 일치. 실제 파일과 백업의 diff는 정확히 두 줄(계약이 적은 문구 그대로). 두 훅을 실제 목록 파일로 돌리면 `abbr=43 seven=0 pairs=69 words=12` / `check_rc=0 verdict=miss words=["SK"]` / `remind_rc=0 remind_seven=0` — 계약과 일치. 백업(고치기 전) 사본으로 같은 훅을 돌리면 `abbr=50 seven=7 ... verdict=pass ... remind_seven=7` — 이 검사가 고치기 전·후를 실제로 가른다는 것을 확인.

### Architecture (5/5)
- [x] 구조-01: 문서 쪽 셋이 원문과 같은 정규식·해당 없음 줄·짝 표, 공통 스타일 링크, 폭 넘침 없음 — PASS
  - 근거(L3, 실행): contract-schema.html 옛 확장·awk 각 0, 새 확장 6(기준5↑)·새 awk 2(기준2↑). qa-evaluation-guide.html 옛 확장 0, 새 확장 1(기준1↑). `AP-00: N/A` 0. 일곱 짝(`<code>SK</code>...<code>스킬</code>` 모양) 각 1. 스타일시트 링크 세 쪽 각 1, `check-docs-common-css.py` 종료 코드 0(검사한 쪽 202·어긋난 쪽 0). `overflow.mjs` 로 320·375·1280px × 세 쪽 = 9경우 모두 overflow 0. 대조: 같은 검사를 임시 폴더에서 2000px 짜리 블록을 하나 심은 사본으로 돌리면 `overflow=3` — 이 검사가 실제로 폭 넘침을 잡아낸다는 것을 확인.

- [x] 구조-02: 바뀐 경로가 범위 목록 28경로 안, 커밋마다 맨 위 폴더 하나·서명 줄 하나 — PASS
  - 근거(L3, 실행): `m-scope.sh` 의 `changed=` 27경로 전부가 계약의 `# sprint-scope` 목록(28경로, `.harness/project.yaml` 제외분) 안에 있음(comm으로 대조, 밖에 있는 것 0). `commits=19 bad=0 dirty=0`.

- [x] 구조-03: 커밋 메시지 제목이 모두 한국어를 담는다 — PASS
  - 근거(L3, 실행): `git log --no-merges --format=%s 66e6c74b..chore/ak3-id` 19개 제목 전부 한국어 포함(한국어 없는 것 0).

- [x] 구조-04: 원본을 바꾼 문서의 짝 쪽이 모두 같이 바뀌었다 — PASS
  - 근거(L3, 실행): `detect-docs-drift.py --since 66e6c74b --json` 이 낸 쪽 3개(contract-design-guide.html·qa-evaluation-guide.html·contract-schema.html) 모두 `changed=` 안에 있음. 쪽 0개가 아니므로 FAIL 조건도 해당 없음.

- [x] 구조-05: 로컬 CI 전체와 CI 파일에만 있는 16단계가 모두 통과한다 — PASS
  - 근거(L3, 실행): `ci-local.sh` 실행 결과 26개 단계줄 모두 `rc=0`(25개) 또는 `feedback-agg-test SKIP (yq 없음)`(1개, yq 미설치 확인함) — 계약의 "기준(봉인 전)" 상태와 정확히 같은 모양. 스크립트 자체 종료 코드 0. 계약 밖 16단계(check-api-kit-docs·detect-docs-drift --check-table·test-detect-docs-drift·check-docs-common-css·test-check-docs-common-css·check-cause-table-copies·check-install-docs-guidance·test-check-cause-table-copies·test-ci-local·measure-helpers-test·check-superseded-test·check-superseded .harness·bambu-gate-fixtures·bambu-makerworld-fetch-test·playwright design-kit·playwright api-kit) 전부 직접 실행해 종료 코드 0 확인.
  - 해석 근거: 조건 문구 "끝 줄 rc=0" 을 문자 그대로 "출력 전체의 마지막 줄"로 읽으면, ci-local.sh 마지막에 `grep -c 'rc=0'` 다음 `grep -v 'rc=0'` 를 찍는 구조상 SKIP 줄이 있을 때는 그 SKIP 줄이 실제 마지막 줄이 되어 문자 그대로는 안 맞는다(구현자도 "남은 것"으로 이 점을 밝혔다). 하지만 이 조건 문장은 "단계 줄이 모두 ~ 이고 끝 줄 rc=0" 로 한 문장 안에서 "단계 줄" 을 계속 가리키고 있고, 계약 자신의 "기준(봉인 전)" 절이 지금 관측한 것과 글자까지 같은 상태(단계 25줄 rc=0·SKIP 1줄)를 "끝 줄 rc=0" 을 만족하는 기준으로 이미 적어 두었다 — 즉 계약을 쓴 사람이 이 상태를 직접 보고 "만족한다"고 판단해 봉인한 기록이다. 그리고 실제로 단계들 가운데 마지막 단계줄(api-ui-viewer)은 글자 그대로 "rc=0" 으로 끝난다. 이 세 근거로 "끝 줄" 을 "단계 줄 가운데 마지막 것" 으로 읽어 PASS 로 판정했다. 다르게 읽을 여지가 있으므로 아래 개선 제안에 계약 문구 손질을 권한다.

### Anti-patterns (2/2)
- [x] 금지-03: bare code fence 금지 — PASS
  - 근거(L3, 실행): `validate-plugin.py --check=code-fence` 14개 플러그인 모두 "0 bare — OK", 종료 코드 0.

- [x] 금지-04: frontmatter name 필드 누락 금지 — PASS
  - 근거(L3, 실행): `validate-plugin.py --check=frontmatter` 14개 플러그인 모두 OK, 종료 코드 0.

### Reusability (1/1, N/A 1)
- [ ] 재사용-01: N/A (새로 만드는 공용 코드 단위가 없다)
  - N/A 사유 확인(L3, 실행): `git diff --diff-filter=A --name-only 66e6c74b chore/ak3-id -- . ':(exclude).harness'` 결과 0줄 — 새로 만든 파일이 실제로 없다. 사유 사실 확인됨.

- [x] 재사용-02: 정규식은 규약 문서 한 곳에 두고 공용 측정 파일은 사본 없이 읽는다 — PASS
  - 근거(L3, 실행): `measure-helpers-test.sh` 에 `PASS M3-규약과같음 same_as_schema=1 copies=0` 줄 확인.

### Diagnostics (1/1, N/A 3)
- [ ] 진단-01: N/A (`commands.analyze` 는 scripts/release.sh 만 잰다 — 교집합 0)
  - N/A 사유 확인(L3, 실행): `git diff --name-only 66e6c74b chore/ak3-id | grep -c '^scripts/release.sh$'` = 0.

- [x] 진단-02: IDE diagnostics 경고 0개, 목록 파일 경고 수 백업과 동일 — PASS
  - 근거(L3, 실행): `m-diag.sh` 끝 줄 `md_new=0 sh_new=0 py_bad=0 js_bad=0 files=27`. markdownlint-cli2(MD013 끔) 로 목록 파일 백업·실제본을 각각 돌려 경고 줄 수(`grep -cE '^[^ ]+:[0-9]+'`) 둘 다 40 — 계약과 일치.

- [ ] 진단-03: N/A (`commands.test` 는 scripts/release.sh 만 돈다 — 교집합 0)
  - N/A 사유 확인(L3, 실행): 진단-01 과 같은 측정, 0 확인됨.

- [ ] 진단-04: N/A (산출물에 구동할 앱·서버가 없다)
  - N/A 사유 확인(L3, Read): 변경 파일 27개 전부(구조-02 `changed=` 목록) 문서·검사 스크립트·설정·레포 밖 목록 파일이며 실행 진입점(앱·서버) 없음을 직접 확인.

## Unverifiable Summary
- invalid_evidence: 0
- env_gaps: 0
- verified_coverage: (29 - 0) / 29 = 1.00 (임계 0.60)
- 연속 ENV 승급: 없음
- Verdict 영향: 통상 (자동 REJECT/BLOCKED 해당 없음)

## Discrimination (규칙 12 적용 조건 없음)
- 이 계약의 조건은 모두 문서·설정·검사 스크립트 자체를 직접 재는 것이라 동시성 가드·인증/권한·멱등성 등 9항목에 해당하는 조건이 없다.

## Check Artifacts (산출물이 검사인 조건)
- 대상: 스킬-01 — `harness/references/contract-schema.md` §측정 커버리지 표기 검출기(awk 블록, 이번 스프린트가 규칙을 새 정규식으로 고침)
  - ① 첫 칸만: 해당 없음(단일 awk 순회, 칸 구분 없음) — 대신 시험 계약(2조건)에서 둘째 조건(SK-98)까지 모두 잡는지 직접 확인 → 둘 다 UNCOVERED로 잡힘
  - ② 실행 목록: 해당 없음(검출기이지 시험 파일이 아님)
  - ③ 못 읽는 칸: 해당 없음
  - ④ zsh·bash: 문서 안 bash 블록을 그대로 떼어 bash로 실행(스킬-01은 검출기 실행 자체가 요구 사항). zsh 별도 실행은 안 했으나 이 awk 는 외부 상태에 의존하지 않아 셸 차이 영향 없음
  - ⑤ 효과 증명: 시험 계약(fixture-coverage.md)에 이미 위반 2건이 들어 있고, 실행 결과 2건 모두 잡힘(계약이 정한 "알려진 답"과 같음)

- 대상: 스크립트-01 — `.harness/.meta/after-kaizen-0928/id-compat/compat.sh`(옛 계약 240개 순회)
  - ① 첫 칸만: 해당 없음(각 계약을 완결 처리, 칸 구분 없음)
  - ② 실행 목록: 해당 없음
  - ③ 못 읽는 칸: 해당 없음(계약 파일 각각 독립 처리)
  - ④ zsh·bash: 둘 다 실행, 결과(diff 0) 동일
  - ⑤ 효과 증명: 정규식에서 영어 쪽을 뺀 사본으로 돌리면 217/434 차이 — 계약이 적은 "알려진 답"과 일치

- 대상: 스킬-05 — `.harness/.meta/after-kaizen-0928/id-compat/lone-ids.sh`(규칙 자리 17곳)
  - ① 첫 칸만: 해당 없음(17개 범위 전부 개별 실행·개별 출력 확인함, `lone-ids-all.sh` 로 17줄 전부 봄)
  - ② 실행 목록: 해당 없음
  - ③ 못 읽는 칸: 17곳 모두 `region=` 값이 나옴(못 찾은 범위 0)
  - ④ zsh·bash: 계약 측정문 자체가 bash 전용(awk 스크립트), zsh 별도 요구 없음 — 해당 없음(고정 해석기)
  - ⑤ 효과 증명: 손으로 만든 대조 입력에서 `region=4 lone=1 ko=1` 확인(계약의 "알려진 답"과 일치), 없는 머리로 `NO_REGION` 확인

- 대상: 구조-01 — `.harness/.meta/after-kaizen-0928/id-compat/overflow.mjs`(문서 쪽 폭 넘침 검사)
  - ① 첫 칸만: 해당 없음(9개 경우 = 쪽3×폭3 전부 개별 출력 확인)
  - ② 실행 목록: 해당 없음
  - ③ 못 읽는 칸: 9개 경우 모두 값이 나옴
  - ④ zsh·bash: node 스크립트라 셸 무관 — 해당 없음(고정 해석기)
  - ⑤ 효과 증명: 임시 폴더 사본에 폭 2000px 블록을 심자 `overflow=3` — 검사가 실제로 넘침을 잡음

## Evidence Validity
- 검사 대상 증거: 29건(조건별) + 계약 전체 지문/봉인 확인
- 무효 판정: 0건
- 셸 스니펫 실행 검증: 직접 실행 다수(스킬-01·02·03·04·05·06·07, 스크립트-01~06, 오류-01~03, 구조-01~05, 금지-03·04, 재사용-02, 진단-02) · zsh/bash 양쪽 확인(스크립트-01·02, 오류-01) · 미실행 0건(모든 조건을 직접 실행하거나 Read로 원문 대조함)
- 양성 대조: 스킬-01(시험 계약 2건 위반 검출) · 스킬-02(알려진 답 2 확인) · 스킬-05(손입력 region=4 lone=1) · 스킬-06(한 글자 변조 → violations=1) · 스크립트-01(정규식 제거 사본 → 217/434) · 스크립트-03(옛 규약 사본 → FAIL K) · 스크립트-04(번호 섞임 → rc=1) · 스크립트-05(다섯 식 모두 확인) · 오류-01(변조 3종 확인) · 오류-03(백업 사본 → verdict=pass) · 구조-01(2000px 삽입 → overflow=3)
- 무효 0건은 미검증 카운터에 영향 없음(현재 누계 0)

## Summary
- Total: 25/25 conditions passed (N/A 4: 재사용-01·진단-01·진단-03·진단-04, 사유 전부 실측 확인됨)
- Verdict: APPROVE

## Improvement Suggestions
- [구조-05] 측정-방식-불일치 — "끝 줄 rc=0" 을 "마지막 단계 줄이 rc=0" 또는 "스크립트 종료 코드 0" 으로 구체화. 지금 문구는 `ci-local.sh` 가 `grep -v 'rc=0'` 로 SKIP 줄을 마지막에 찍는 구조와 글자 그대로는 안 맞아, 계약을 쓴 사람도 "도구 출력과 다르다"고 남은 일로 적어 두었다. 이번엔 계약의 "기준(봉인 전)" 절이 같은 상태를 이미 통과로 적어 둔 것과 마지막 단계 줄이 실제로 "rc=0" 인 점을 근거로 PASS 로 판정했지만, 다음 판정자가 다르게 읽을 수 있다.
