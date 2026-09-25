# Sprint Feedback
Feature: 카이젠 2026-09-24 Phase 17 — howto-kit 게이트를 부르는 블록을 자식 셸 안에서 읽고 경로를 세 단계로 찾음 · 러너가 그 블록을 직접 돌림 · 리뷰어 판정 불가 표기
Evaluated: 2026-09-25 14:12
Verdict: APPROVE
Iteration: 1

## Contract Fingerprint
- path: /Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/kaizen-0924/.harness/sprint-contract-kaizen-0924-p17-howto-kit.md
- sha256: 2315b00c9e299d9fa4ce39c359d1f4d4925158ae87be400e69b9144365d4e4f6
- status: active (판정 후 done 으로 전환)
- slug: kaizen-0924-p17-howto-kit
- contract_root: /Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/kaizen-0924
- contract_root_unconfigured: false
- 선택 근거: ladder 1 명시경로 (task 가 계약 절대경로를 지정)
- legacy_contract_used: false
- seal_status: SEAL_OK (conditions_digest sha256:33e681f97ba3081e = 실측 digest 일치)
- contract_seal_broken: n/a
- 봉인 커밋 대조(1-e-3): 98f4d5e — 계약 파일 1개만 포함(순수 봉인 커밋). 구현 커밋(5a96f7c) · notes 커밋(04a0e76) 모두 `Kaizen-Phase: kaizen-0924-p17-howto-kit` 서명 줄 있음. conditions_digest 재봉인 없음
- 재확인(Step 5): 일치
- status_transition: active -> done (아래 Step 5.5 수행)

## Amendments
- amendments: 0 (조건을 바꾸는 개정 없음)
- 사이드카 내용: 범위 상한 `end_sha` 2개 값(구현 커밋 → notes 커밋)을 덧붙인 것 뿐 — 계약이 정한 메커니즘 그대로(옛 줄 보존, 조건 줄 미변경)
- `amend_direction: unchanged` — 구현이 예행과 다른 유일한 곳은 러너 안 변수 이름(한 글자 → 서술적 이름) 재명명뿐이고 동작은 동일. 조건 줄이 가리키는 출력값에 영향 없음(직접 재측정으로 확인)
- PASS 근거로 쓸 수 없는 조합: 0건

## User Correction Audit
- correction_log_status: available (~/.claude/logs/claude-plugins/2026-09.md)
- unreflected_corrections: 0 (이 세션의 Phase 17 구간(12:20~14:12) 사용자 발언 2건은 모두 진행 상황을 묻는 질문 — "지금 어디야" · "지금은?" — 이며 방향 교정이 아님)
- verdict 영향: 없음

## Cross-Diagnosis Handoff
- 상태: pending-parent
- 부모가 띄울 때 넘길 것: 계약 절대경로 `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/kaizen-0924/.harness/sprint-contract-kaizen-0924-p17-howto-kit.md` · 이 판정 결과 전문
- 부모가 물을 두 가지:
  1. 계약 조건의 원래 의도와 다르게 해석해 PASS/FAIL 을 오판한 조건이 있는가?
  2. 0 건·빈 출력을 근거로 PASS 한 조건 중, 문제가 있어도 0 을 냈을 측정(공허한 통과)이 있는가? — 특히 DG-04 는 평가자 자신의 측정 방식 결함(뒤 Evidence Validity 절 참조)을 실제로 겪었으므로 교차 진단에서 다시 볼 가치가 있다
- 부모가 교차 진단을 마친 뒤 `cross_diagnosis_by` 를 `sprint-contract` 로 갱신한다. 끝내 띄우지 못했으면 `none` 으로 내리고 사유를 `cross_diagnosis_notes` 에 적는다

## Results

모든 측정은 계약의 `## 회귀 게이트` 절에 적힌 `common.sh` · `m.sh` 를 그대로 추출해 실제 저장소(시작 커밋 `f936019c` · 끝 판 `04a0e763a`)에서 `git archive` 로 두 판을 풀어 직접 실행했다. 값은 전부 `type m >/dev/null || exit 2; m <조건 ID>` 실행 출력 그대로이며, 계약이 봉인 전에 적어 둔 "예행 판" 기대값과 라인 단위로 정확히 일치한다(단 하나 예외는 DG-04 — 아래 Evidence Validity 절에서 원인을 밝히고 재검증했다).

### Skill (9/9)
- [x] SK-01: howto-audit Phase 2 블록, 세 경우(plugin/repo/market) 모두 `R/15/15/0/0/1`, 토큰 `1 1 0 0` — 기대값과 완전 일치 — PASS
  - 근거: `out-clean.txt` SK-01 `plugin:R/15/15/0/0/1 repo:R/15/15/0/0/1 market:R/15/15/0/0/1` / `1 1 0 0`. L3(의미 검증) — 세 경우 모두 첫 줄이 그 경우의 `RESOLVED:` 경로이고 판정 줄 15·not found 0·종료 코드 0
- [x] SK-02: Gotcha 6 절 위치(Gotcha5<Gotcha6<Process)·9개 문장 조각·Phase2 뒤 6줄·export -f 사실(4개 셸)·Phase4 RESOLVED줄 — 전부 계약이 요구한 그대로 — PASS
  - 근거: `1 1 1 1 1 1 1 1 1` / `1` / `1 1 1 1 1 1` / `/bin/sh=called bash=called /bin/dash=no zsh=no` / `1`
- [x] SK-03: howto-doc Gotcha3(폴더, 세 경우 R/15/15/0/0/1)·Phase4(파일, 세 경우 R/0/1/0/0/1) — PASS
  - 근거: `plugin:R/15/15/0/0/1 repo:R/15/15/0/0/1 market:R/15/15/0/0/1` `1 1 0` / `plugin:R/0/1/0/0/1 repo:R/0/1/0/0/1 market:R/0/1/0/0/1` `1 0`
- [x] SK-04: Gotcha3 뒤 3줄·Phase4 뒤 6줄·옛 줄 0건 — PASS
  - 근거: `1 1 1` / `1 1 1 1 1 1` / `old_line=0 old_find=0`
- [x] SK-05: README 블록 세 경우 R/0/1/0/0/1·두 문단 각 1줄 이상·옛 글 0·옛 줄 0 — PASS
  - 근거: `plugin:R/0/1/0/0/1 repo:R/0/1/0/0/1 market:R/0/1/0/0/1` `1 1 1` `1 1 1 1 0` `old_line=0`
- [x] SK-06: 규칙7 + 출력형식 5조각 전부 있음·접미없는 `[미검증]` 0개 — PASS
  - 근거: `1 1 1 1 1 1` `bare=0`
- [x] SK-07: 끝 판 러너 `EVALS total=33 pass=33 fail=0`, PASS 줄 이름 33개가 기대 목록과 완전 일치 — PASS
  - 근거: `rc=0 |  | EVALS total=33 pass=33 fail=0` / `want=33 got=33 same=1`
- [x] SK-08: 8개 변이(n1~n8)가 각각 계약이 적은 정확한 실패 사례 집합·통과/실패 수를 냄. n7 을 zsh 로 돌리면 끝 판만 그 한 사례로 실패하고 시작 커밋 판 러너는 zsh 에서 놓친다(고친 것의 증거) — PASS
  - 근거: `out-clean.txt` 38~47행, 계약 조건문의 enumerated 값과 글자 그대로 일치(전부 대조 완료, 누락 없음). NEG_EDIT_FAIL 없음(변이 전부 성공 적용)
- [x] SK-09: 게이트 스크립트 머리 5줄·옛 줄 0·evals.json 키 순서·gate_blocks 값·description 문구 — PASS
  - 근거: `1 1 1 1 1 0` / `keys=kit,description,runner,gate_blocks,cases gate_blocks=1 desc_three=1`

### Script (N/A 1)
- [x] SC-00: N/A 사유 실측 확인 — 이 Phase 가 건드린 경로 중 `scripts/release.sh`·`marketplace.json`·`plugin.json` 계열 0건 — N/A
  - 근거: `SC-00=0` (`m NA`)

### Error (4/4)
- [x] ER-01: 7개 파일 + notes 파일에 새로 생긴 URL 전부 근거 파일에 있음(0건 미포함), 끝 판 근거 파일이 시작 커밋 판과 동일 — PASS
  - 근거: `0` / `0` / `evid_same=1`
- [x] ER-02: 더한 줄에 번역투 6종·특정 이름 0건, 킷 전체에서도 0건 — PASS
  - 근거: `added=258 k02=0 names=0 kit_names=0` (added 수는 조건 판정 대상이 아님 — k02/names/kit_names 만 0 확인)
- [x] ER-03: notes 파일 커밋됨, 절 머리 9개·넘김 절 7개 토큰·미반영 절 3개 토큰 전부 1줄 이상, 공유·타 Phase 경로를 건드린 무서명 커밋 0개 — PASS
  - 근거: `notes_committed=1` / `1 1 1 1 1 1 1 1 1` / `1 1 1 1 1 1 1` / `1 1 1` / `0`
- [x] ER-04: 스크립트를 못 찾는 환경에서 네 블록 모두 `MISSING:` 으로 멈춤, 글자 그대로 일치, 판정/not found 줄 0 — PASS
  - 근거: 4줄 모두 `none:M/0/0/0/1/1  exact=1`. **양성 대조 직접 재현**: howto-audit 블록의 `MISSING` 분기 `false` 를 지운 사본에서 첫 블록만 `none:M/0/0/0/0/1`(4번째 값 1→0)로 바뀌고 나머지 3블록은 그대로 — 계약이 적은 음성 대조와 정확히 일치, 이 측정이 실제로 판별력이 있음을 확인(사본에서만 실행, 원본 불변)

### Architecture (3/3)
- [x] AR-01: 서명 없는 커밋 0·서명 커밋이 건드린 경로가 FILES 7개와 일치·봉인 깨진 계약 0·SEAL_OK·범위 선언 블록 일치 — PASS
  - 근거: `0` / `0 7` / `0` / `SEAL_OK` / `scope_same=1` / `1`
- [x] AR-02: 새 문장이 가리키는 자리(Gotcha6·Phase4·Gotcha1·agent-design-guide §10·gate_blocks 키) 전부 실재 — PASS
  - 근거: `1 1 1 | 1 1 1 1 | 1 1 | 1 1 | 3 3`. **음성 대조 직접 재현**: howto-audit `### Gotcha 6: ` 제목 줄 접두 자체를 바꾼 사본에서 셋째 값만 `1→0`(`1 1 0`)으로 떨어짐, 나머지는 그대로 — 계약 음성 대조와 일치
- [x] AR-03: 게이트 판정 코드·evals.json cases/runner/kit·fixtures·references·howto/SKILL.md·docs/howto 전부 시작 커밋 판과 동일 — PASS
  - 근거: `1 1 1 1 1 1`

### Anti-patterns (3/3)
- [x] AP-01: 더한 줄에 킷 버전(0.2.1) 하드코딩 0건 — PASS
  - 근거: `version=0.2.1 0`
- [x] AP-03: 마크다운 4파일 모두 언어 힌트 없는 여는 펜스 0개 — PASS
  - 근거: `0 0 0 0`. **양성 대조 직접 재현**: reviewer 사본 끝에 언어 힌트 없는 펜스를 추가하면 `barefence` 값이 `0→1` — 측정이 판별력 있음을 확인
- [x] AP-04: SKILL.md 2개·reviewer frontmatter 편집 전과 동일, name 줄 각 1개 — PASS
  - 근거: `1 1 1 | 1 1 1`

### Reusability (2/2)
- [x] RE-01: 러너가 레포 밖(`/`)에서 절대경로로 불러도 끝 판과 동일 결과 — PASS
  - 근거: `rc=0 EVALS total=33 pass=33 fail=0 EVALS_PASS`
- [x] RE-02: 네 블록의 경로 찾기 앞 6줄이 서로 글자 그대로 같고, qa-evaluator Step 8 과 같은 3단계(플러그인 치환→git 최상위→마켓플레이스), howto_gate 정의는 게이트 스크립트 하나뿐 — PASS
  - 근거: `1` / `1 1 1 | qa=2 | howto-kit/scripts/howto-gate.sh`

### Diagnostics (4/4, N/A 2)
- [x] DG-01: N/A 사유 확인 — `commands.analyze` 대상(`scripts/release.sh`)과 교집합 0 — N/A (`DG-01=0`)
- [x] DG-02: 마크다운 4파일 각각 편집 전 대비 늘어난 markdownlint 규칙 0개 — PASS
  - 근거: 4파일 모두 `rules_up=0`
- [x] DG-03: N/A 사유 확인 — `commands.test` 대상과 교집합 0 — N/A (같은 `DG-01=0`)
- [x] DG-04: 러너를 4개 해석기(dash/sh/bash/zsh)로 — 전부 종료 코드 0·stderr 0·dash 출력과 동일, shellcheck·문법검사 전부 0 — PASS (아래 Evidence Validity 절 참조 — 최초 측정에서 평가자 자신의 환경 오염으로 `/bin/sh` 만 깨진 값이 나왔던 것을 원인 규명 후 재확인)
  - 근거(깨끗한 환경 재실행): `/bin/dash rc=0 err=0 same=1 | /bin/sh rc=0 err=0 same=1 | bash rc=0 err=0 same=1 | zsh rc=0 err=0 same=1 |` / `run-evals.sh shellcheck rc=0 lines=0 howto-gate.sh shellcheck rc=0 lines=0 n_dash=0 n_sh=0 n_bash=0 n_zsh=0`
- [x] DG-05: `validate-plugin.py howto-kit` 10줄 전부 OK·rc=0, `sync-docs.py --check-only` rc=0 동기화됨, stale-values 옛 값 0건 — PASS
  - 근거: `10 0 rc=0` / `sync_rc=0 1` / `stale_old=15 files=7 hits=0`
- [x] DG-06: `validate-post-kaizen.py --since <시작HEAD>` scope-isolation·doc-contracts 모두 PASS — PASS
  - 근거: `scope-isolation: PASS` / `doc-contracts: PASS` / `doc_checked=2 doc_mine=0` / `violators=0 mine=0`

## Discrimination (규칙 12)
- 적용 여부: 이 Phase 는 규칙 12의 9항(동시성 가드/인증/멱등성/입력검증/데이터유실/마이그레이션/재시도·중복제거/보안경계/사용자보고 vs 테스트 충돌)에 정확히 해당하지 않아 필수 적용 대상은 아님
- 그럼에도 SK-08 의 8개 내장 변이(n1~n8)가 러너-게이트 결합을 이미 실측으로 증명한다 — 각 변이가 끝 판 킷 사본의 정확히 그 지점만 깨뜨리고, 러너가 그 지점만 실패로 잡음(결합 확인 충족)
- n7 을 zsh 로 돌리는 교차 비교가 "끝 판 러너는 잡고 시작 커밋 판 러너는 놓친다"를 직접 보여 이 Phase 가 고친 결함(zsh assertion 버그)의 판별력을 증명

## Evidence Validity
- 검사 대상 증거: 28건 전부(25 PASS + 3 N/A)
- 무효 판정: 0건. 단, **1차 측정에서 DG-04 하나가 일시적으로 무효였다** — 평가자가 `set -a` 로 계약의 `common.sh`/`m.sh` 를 읽으면서 bash 함수(`sub`·`runcase` 등)가 환경변수(`BASH_FUNC_*`)로 자동 export 되었고, `/bin/sh`(이 맥의 bash 3.2.57)가 그 함수를 임포트하다 구문 오류를 내며 전혀 다른 대량 출력(32180바이트, dash 대비 31배)을 냈다. `env -i` 로 오염 없는 환경에서 재실행하니 계약이 예상한 값과 정확히 일치(`same=1` 4개 전부)했다 — 이는 howto-kit 구현의 결함이 아니라 평가자 자신의 측정 방법 결함이었음을 격리해서 확인했다. 최종 채택 값은 오염 없는 재실행 값이다
- 셸 스니펫 실행 검증: 계약의 회귀 게이트 절 전체(`common.sh`·`m.sh`·`rule-delta.sh`·`ctl-runner.py`)를 원문 그대로 추출해 직접 실행 (실행 N=28조건 전부, zsh·bash 양쪽 확인은 SK-01/03/05/ER-04 자체가 `runcase()` 로 매 조건마다 zsh·bash 둘 다 돌림)
- 양성·음성 대조: [ER-04 — 음성 대조 직접 재현(사본) — howto-audit MISSING 분기 false 제거 → 첫 블록만 4번째 값 1→0, 계약 기재값과 일치] [AR-02 — 음성 대조 직접 재현(사본) — Gotcha6 제목 접두 변경 → 셋째 값 1→0, 계약 기재값과 일치] [AP-03 — 양성 대조 직접 재현(사본) — reviewer 끝에 언어힌트없는 펜스 추가 → 0→1] [SK-08 — n1~n8 전부 계약 내장 변이 실행, NEG_EDIT_FAIL 없음]
- 무효 0건 → 미검증 카운터에 합산 없음

## Unverifiable Summary
- invalid_evidence: 0
- env_gaps: 0
- verified_coverage: 28/28 = 1.00 (임계 0.60 충족)
- Verdict 영향: 통상

## Summary
- Total: 25/25 조건 PASS (N/A 3건 — SC-00·DG-01·DG-03 — 은 사유 실측으로 확인, TOTAL 에서 제외)
- Verdict: APPROVE

## Improvement Suggestions
(없음 — 계약의 측정 정의가 실제 구현과 완전히 부합했고, 개선 제안을 낼 결함을 발견하지 못함)
