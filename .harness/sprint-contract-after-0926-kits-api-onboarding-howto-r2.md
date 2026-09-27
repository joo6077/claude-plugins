---
feature: "카이젠 뒤 남은 것 — api · onboarding · howto-kit (k4) 2 회차 계약"
slug: after-0926-kits-api-onboarding-howto-r2
created: "2026-09-27 12:16"
complexity: "복잡"
conditions: 33
status: active
owner_session: bda55d45-296c-491f-89ba-b52042d58e72
conditions_digest: sha256:e480bffbe5e46407
measurement_digest: sha256:9ef53fe9b6426fff
locked_at: "2026-09-27 12:21"
---

## 배경

- **2 회차 계약이다.** 1 회차 계약 `.harness/sprint-contract-after-0926-kits-api-onboarding-howto.md`(봉인 커밋 `927c2a7`, 조건 33, 지금 `status: superseded`)를 대신한다. 1 회차 QA 판정은 `.harness/sprint-feedback-after-0926-kits-api-onboarding-howto.md`(커밋 `145cb63`, REJECT 31/33)에 있다.
- 틀린 측정: 1 회차 `RE-01` 의 N/A 사유 측정 `git diff --diff-filter=A --name-only 6378948 chore/ak2-k4 -- scripts '*.sh' '*.py'` 는 경로를 `.harness/` 밖으로 한정하지 않았다. 1 회차 `## 범위 경계` 가 「봉인 커밋 뒤 `.harness/` 만 든 커밋으로 싣는다」 고 정한 이 계약 자신의 측정 도우미 다섯 파일(`.harness/.meta/after-0926-kits-api-onboarding-howto/` 의 `ci-local.sh` · `ka5.sh` · `m.sh` · `ob.py` · `stub.py`)까지 세어, 계약대로 일하면 0 줄이 될 수 없었다. `RE-02` 도 「RE-01 과 같은 명령」 을 쓴다. 조건끼리 부딪힌 것이며 처음부터 틀린 측정이었다.
- 바로잡은 까닭: 조건 의도는 「킷 · `scripts/` 에 새 실행 파일을 더하지 않았다」 다. `.harness/` 는 계약 · 측정 기록 자리라 그 의도 밖이다(1 회차 `AR-01` · `AR-02` 도 `.harness/` 를 빼고 잰다). 그래서 같은 명령 끝에 `':(exclude).harness'` 를 붙인다. 바뀐 것은 이 두 조건의 측정뿐이고 나머지 31 조건은 1 회차 조건 줄 · 측정 줄을 글자 그대로 옮겼다(`AR-02` 는 봉인 커밋이 1 회차 것임을 괄호로 밝힌 한 구절만 더했다).
- 1 회차 개정 `.harness/sprint-amendments-after-0926-kits-api-onboarding-howto.md` A-01(같은 바로잡음, `relaxing · unanchored`)은 사용자 동의를 받지 않은 채 1 회차 기록으로 남긴다. 이 2 회차 계약은 그 개정을 동의 처리한 것이 아니라, 결정 파일 `.claude/worktrees/after-0926b/.harness/.meta/after-kaizen-0926b/decisions.md` 「추가 위임」 절이 정한 대로 계약을 새 판으로 다시 써서 다시 봉인하는 길이다. 위임 발언 2026-09-27T01:22:01.089Z 「자동으로 다 진행해 나한테 묻지 말고 …」(세션 `bda55d45-296c-491f-89ba-b52042d58e72`).
- 봉인 순서: 구현 커밋(`f07be35` ~ `c0b0ffb`)은 1 회차 봉인 커밋 `927c2a7` 뒤에 있다. 이 2 회차 계약의 봉인 커밋은 구현 뒤에 온다 — 새 판이라 피할 수 없다. 「봉인이 구현보다 먼저」 를 재는 `AR-02` 는 1 회차 봉인 커밋을 기준으로 잰다(측정 도구 `m.sh` 의 `AR-02)` 가 1 회차 계약 경로를 박아 둔다).
- 남은 일 목록 `.claude/worktrees/after-0926b/.harness/.meta/after-kaizen-0926b/leftovers.md`(기준 판 `6378948`)의 세 절 — 「## kit-api-kit」 KA-1 ~ KA-5, 「## kit-onboarding-kit」 KO-1 ~ KO-2, 「## kit-howto-kit」 KH-1 ~ KH-2 — 을 한 계약으로 처리한다.
- 작업 폴더 `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak2-k4`, 가지 `chore/ak2-k4`, 시작 판 `6378948`(origin/main). 시작할 때 `git status --short` 0 줄 · 로그 끝 `6378948` — 앞 단계가 남긴 파일은 없었다.
- 계약 합의는 사용자 위임으로 받았다 — 2026-09-26T10:09:00.557Z 「123다실행해 그러면끝나?다음카이젠에왜넘기는데?」 · 결정 답 2026-09-26T10:30:16.222Z (세션 `bda55d45-296c-491f-89ba-b52042d58e72`). 기록은 `.claude/worktrees/after-0926b/.harness/.meta/after-kaizen-0926b/decisions.md` 「## 위임」. 조건을 느슨하게 하는 개정은 이 위임으로 동의 처리하지 않는다.
- 복잡도 4 축: 레이어 = 예(스킬 문서 · 게이트 셸 함수 · 시험 러너 · 저장소 검사 스크립트) · 공개 계약 변경 = 예(`guide_gate` 출력 줄이 늘고, `/api-verify` 판정 줄 꼴을 정한다) · 소비면 = 예(`gate_cases` 기대 출력 · SKILL.md 의 「출력 N 줄」 문장 · `/api-ui` 가 판정 줄을 옮기는 규칙 · 저장소 검사 목록) · 회귀 위험 = 예(게이트 · 러너 · 저장소 검사를 고친다). 넷 다 예라 「복잡」 이고 양면 조건을 둔다.
- 기능 조건이 20 개를 넘는다(25). 킷 셋을 한 묶음으로 받은 배정이라 나누지 않고, 커밋을 킷별로 나눠 평가 단위를 가른다(AR-02).

## 리서치 소스

- EX-11 (`.claude/worktrees/after-0926b/.harness/.meta/after-kaizen-0926b/ex/EX-11.md`, 2026-09-26 원문 대조) — <https://firebase.google.com/docs/ios/setup>: 「Use Swift Package Manager for all new projects.」 · 「The CocoaPods ecosystem is deprecated: CocoaPods is moving to a read-only state and Firebase 12 is the final major version published to CocoaPods.」 폐기 날짜는 원문에 없다. 이 Apple 네이티브 문서만으로 FlutterFire 의 iOS 설치 절차를 SPM 으로 바꾸면 안 된다.
- EX-12 (`…/ex/EX-12.md`, 2026-09-26) — <https://www.oasis-open.org/committees/tc_home.php?wg_abbrev=dita>: DITA 1.3 이 2015-12-17 승인된 OASIS Standard 로 적혀 있고, DITA 2.0 의 Committee Specification · OASIS Standard 승인 여부와 날짜는 적혀 있지 않다.
- RFC 7493 원문 대조 `.harness/.meta/evidence/rfc7493-ijson-2026-09-26.md`(이 가지에 추적됨, 커밋 `f20f3b0`) — §2.2 「I-JSON messages SHOULD NOT include numbers that express greater magnitude or precision than an IEEE 754 double precision number provides」. 킷이 실패로 막으면 표준보다 엄격한 제품 정책이다.
- 평가 가이드 `harness/docs/guides/qa-evaluation-guide.md` v5.1 §Canonical Unverified-Evidence Protocol 머리말 — 「`*-kit/agents/*-reviewer.md` 는 아래 5 조항을 문구 변형 없이 복제」.
- Hurl 8.0.1(`/opt/homebrew/bin/hurl`) 실측 2026-09-27 — `jsonpath "$.data[*].id"` 는 항목이 하나일 때 값 하나로 벗겨져 `isCollection` 이 떨어진다(`actual: string <ord_1>`).

## GAP 분석

Pre-Edit Audit — 대상 파일을 열어 본 줄.

| 대상 파일 | 실제 Read 증거 (`파일:라인`) | 발견한 기존 갭 | 조건 |
| --- | --- | --- | --- |
| `api-kit/skills/api-ui/SKILL.md` | `:198` `chips` · `rows` 정의, `:241` 보고 줄에 `ep` · `shown` · `under24` · `under44` 만 | KA-1 보고 줄에 `chips` · `rows` 없음 | SK-01 |
| `api-kit/skills/api-ui/SKILL.md` | `:90` 「`→ 판정 불가` 로 끝나는 줄만 글자 그대로 `unjudged` 배열에 옮긴다」 | KA-2 항목 이름 앞머리를 떼는 규칙 없음 | SK-03 |
| `api-kit/skills/api-verify/SKILL.md` | `:135` · `:136` 판정 줄 예 `$.meta.total=47 · len($.data)=10 → PASS`, `:177` §9 7 항 | KA-2 판정 줄이 어느 항목 것인지 적는 꼴이 없음 | SK-02 |
| `api-kit/evals/fixtures/unjudged/.api/reports/2026-09-02T1422-dev/report.md` | `:21` ~ `:23` `- products.list: $.meta.total=(없음) · len($.data)=3 → 판정 불가` | 예시 입력은 이미 `<항목>: ` 앞머리 꼴 | ER-01 |
| `api-kit/evals/fixtures/unjudged/.api/ui.html` | `:1509` · `:1525` `unjudged:['…→ 판정 불가']` 앞머리 없이 | 예시 출력은 이미 앞머리를 뗀 꼴 | ER-01 |
| `api-kit/skills/api-ui/references/viewer-spec.md` | `:86` 상태 아이콘 4 종, `:230` `state:'pass' // 'pass' \| 'fail' \| 'pending' \| 'unjudged'` | KA-3 보류 · flaky 규칙 0 줄(`grep -c 보류` 0 · `flaky` 0) | SK-04 |
| `api-kit/skills/api-contract/SKILL.md` | `:68` `IEEE 754 binary64 표현 불가 숫자     → 실패`, `:20` Gotcha 「`$.data[0].id` 같은 index assertion 금지」, `:227` §9 예시 `jsonpath "$.data[0].id" isString` | KA-4 표준보다 엄격하다는 말 없음 · KA-5 예시가 같은 파일 Gotcha 와 어긋남, 항목 0 개 응답에서 hurl 종료 코드 4 | SK-05 · SK-06 · ER-02 |
| `api-kit/skills/api-verify/SKILL.md` | `:117` I-JSON 게이트 실패 → **비교 불가** | KA-4 같은 갭 | SK-05 · ER-02 |
| `api-kit/skills/api-probe/SKILL.md` | `:183` `2. I-JSON 검문 … binary64 표현 불가 숫자` | KA-4 같은 갭 | SK-05 · ER-02 |
| `api-kit/skills/api-ui/SKILL.md` | `:21` Gotcha 에만 CSP, `:134` ~ `:150` §6 렌더에 CSP 0, `:155` ~ `:165` §7 명령에 CSP 검사 0 | KA-5 확정 시안 v8 에 CSP `<meta>` 0 개 · 예시 `ui.html` 에만 1 개. §7 이 CSP 를 재지 않음 | SK-07 |
| `onboarding-kit/skills/setup-guide/SKILL.md` | `:54` ~ `:123` `guide_gate` G1 ~ G4, `:63` ~ `:74` misplaced 판정, `:126` 「5 줄 출력」, `:277` 「출력 5 줄」, `:218` ~ `:222` Gotcha 9 세 칸 | KO-2 막는 요구 세 칸을 게이트가 재지 않음(사람이 읽음) · CocoaPods 안내 0 줄 | SK-09 · SK-10 · SK-11 · ER-03 |
| `onboarding-kit/skills/setup-guide/evals/evals.json` | `:157` ~ `:250` `gate_cases` 7 개, `:29` SPM 흐름 아님 assertion | KO-1 「한 Step 에 출처 둘」 입력 없음(misplaced 만) | SK-08 · SK-10 |
| `onboarding-kit/skills/setup-guide/evals/run-gate-evals.sh` | `:22` 함수를 SKILL.md 에서 뽑음, `:48` 폴더에만 있는 픽스처는 실패 | 새 픽스처는 등록하지 않으면 러너가 떨어진다 | SK-08 · ER-03 |
| `docs/onboarding-kit/examples/fcm-ios-setup-guide.md` | `:34` `\| 요구 \| 출처 \| 막히는 것 \| 우회 \|` 표, `:202` CocoaPods 자동 `pod install` | 예제는 이미 세 칸 표 · Flutter 절차라 SPM 으로 바꾸지 않는다(EX-11) | SK-09 (고치지 않음) |
| `howto-kit/agents/howto-reviewer.md` | `:1` ~ `:92` 전문. `:30` · `:79` ~ `:82` `[미검증:ENV]` · `[미검증:INVALID]` 네 칸, 정본 사본 절 없음 | KH-1 사본 없음 | SK-12 |
| `scripts/check-reviewer-protocol-copies.py` | `:36` ~ `:44` `REVIEWERS` 일곱, `:46` ~ `:49` `EXCLUDED` 에 howto-reviewer 「다음 사이클 Phase 17 에서 넣는다」, `:2` 「킷 reviewer 일곱」 | KH-1 | SC-01 |
| `howto-kit/skills/howto-audit/SKILL.md` | `:119` ~ `:134` Phase 4 리포트 블록 — 에이전트 줄이 `PASS <x> / FAIL <y>` 뿐 | KH-2 미검증 칸 없음 | SK-13 |
| `howto-kit/references/provenance-notes.md` | `:222` ~ `:245` §9 절차 표준 — DITA 줄 0 | KH-2 DITA 2.0 확인 결과 없음 | SK-14 |
| `howto-kit/evals/run-evals.sh` | `:1` ~ `:210` 전문. `:63` · `:83` 셸 대조, `:71` assertion 대조 | KH-2 러너 자신을 망가뜨려도 `EVALS_PASS`(아래 실측) | SK-15 · SK-16 |
| `docs/howto/design-brief.md` | `:385` C5 「zsh·bash 양쪽에서 실행」 | KH-2 러너는 세 셸(zsh · bash · sh)을 대조 | SK-17 |

1 회차 봉인 전 실측(2026-09-27, 작업 폴더 `6378948` 그대로, 도구는 아래 「회귀 게이트」 의 `m.sh`):

- SK-01 `step7_lines=1 chips=0 rows=0` · SK-02 `s6_prefixed_example=0 s6_id_word=0 s9_item7_id=0` · SK-03 `s2_strip_rule=0`
- SK-04 `hold=0 flaky=0 hold_fail=0 flaky_fail=0 label=0 state_enum=1 new_state=0` · SK-05 세 파일 `strict_note=0`
- SK-06 `index_asserts=1 collection_line=1` · `n=0 rc=4` · `n=1 rc=0` · `n=2 rc=0`. 대조 사본 둘: `[*].id isCollection` 로 바꾼 사본 `n=0 rc=4 n=1 rc=4 n=2 rc=0`, 그 줄을 지운 사본 `index_asserts=0` · `n=0/1/2 rc=0`
- SK-07 `s7_cmd=0 s7_row=0 s6_csp=0` · `example_csp=1 mockup_v8_csp=0`
- SK-08 ~ SK-10 `ko1_cases=0` · `cases=7 g5_one=0 g5_fail_cases=0 empty_kind=0 nourl_kind=0` · `example_same_shell=1 example_g5_pass=0 example_gate_pass=1` · `five_lines=2 six_lines=0 run_line_g5=0` · `runner_rc=0 EVALS declared=7 ran=7 fail=0`
- NEG-KO `g5_mutated=0 g5_neg_rc=0` (G5 가 아직 없다) · `g1_mutated=1 g1_neg_rc=1 … fail=1`
- SK-11 `cocoapods_line=0 flutter_keep=0 evals_spm_assert=1`
- SK-12 · SC-01 `copies_rc=0 ok_lines=7 howto_ok=0 checked=7 violations=0 infra_errors=0 excluded=1` · `source_line=0 grade_line=0 tools=[Read, Grep, Glob] docstring_eight=0` · NEG-KH1(대상 = 시작 판 `6378948` 을 푼 사본 — 봉인 전이라 가지 끝 판이 아직 없었다. 가지 끝 판 기대값은 SC-01 음성 대조 `neg_rc=1 1`) `neg_rc=0 0`
- SK-13 `unverified_line=0 not_pass=0` · SK-14 `dita_lines=0 url=0 d13=0 checked=0`
- SK-15 `lit_assert=1 lit_shell=2` · `orig mutated=0 rc=0 last=EVALS_PASS` · `assert mutated=1 rc=0 last=EVALS_PASS` · `shell mutated=1 rc=0 last=EVALS_PASS` — 두 판정을 무력화해도 러너가 통과한다
- SK-16 `rc=0 EVALS total=33 pass=33 fail=0 seconds=9.6` · SK-17 `c5_three=0`
- ER-01 `report_unjudged=2 matched=2`. 대조 사본(예시 `ui.html` 의 `onHand` 를 `onHandX` 로) `matched=1`
- ER-02 `contract_gate=1 verify_class=1 probe_gate=1`
- DG-02 측정기 양성 대조: 임시 복제본에 MD040 한 줄 · pyflakes 한 줄을 넣은 커밋 → `files=2 new_warnings=2`

## 범위 경계

- 항목별 처리
  - KA-1 · KA-2 · KA-3 · KA-4 · KA-5 · KO-1 · KH-1 — 계약에 넣음
  - KO-2 — 넣은 것: `guide_gate` 막는 요구 세 칸 검사(SK-09 · SK-10 · ER-03), CocoaPods → SPM 안내(SK-11, EX-11). 넣지 않은 것: 서비스 계정 키(Workload Identity Federation 우선)는 근거 파일(`.harness/.meta/evidence/phase14.md:118`)이 스스로 추론이라 적었고 EX 대조가 없다 — 바깥 근거 없음. 평가 날짜(`evals.json:10` · `:69` 의 `Last updated 2026-07-20 UTC`)는 본문 주장(.p12 · Instance ID)을 다시 확인한 원문 대조가 없다 — 날짜만 옮기면 확인하지 않은 주장을 확인했다고 적게 되므로 바깥 근거 없음으로 둔다. AUTO 표지는 목록에 처리됨으로 적혀 있다
  - KH-2 — 넣은 것 다섯: 리포트 미검증 칸(SK-13) · DITA 2.0(SK-14, EX-12) · 러너 음성 대조를 킷 안에(SK-15) · 러너 시간(SK-16) · `design-brief.md:385`(SK-17)
- KH-1 결정: 사본을 둔다. 근거 셋 — (1) 정본 머리말이 `*-kit/agents/*-reviewer.md` 전부에 사본을 요구한다 (2) 제외 사유가 일정(「다음 사이클 Phase 17 에서 넣는다」)뿐이었다 (3) howto-reviewer 는 이미 `[미검증:ENV]` · `[미검증:INVALID]` 네 칸을 써서 정본 조항과 부딪히는 규칙이 없다. 한 곳만 조심한다 — 조항 1 이 `미확인` 을 마커 동의어로 금지하는데 howto-kit 은 `[미확인]` 을 출처 등급 이름으로 쓴다(`howto-kit/references/source-tiers.md:12`). 사본 밖에 둘을 가르는 한 줄을 둔다(SK-12)
- KA-3 결정: 상태 값은 넷 그대로 둔다. 보류(기준선 `pending` 의 실패)와 flaky(재실행에서 뒤집힌 실패)는 `/api-verify` §7 · §8 이 실패 기록을 남기라고 하므로 `state:'fail'` 로 두고, 행 · `실패 원인` 탭에 글자 표지(`보류` · `flaky`, `aria-label` 포함)로 가른다. 초록 표시 뒤로 실패가 숨지 않게 하는 쪽이다
- KA-5 결정: §9 예시에서 index assertion 을 지운다(대체 표현 `[*]` 은 항목 하나일 때 hurl 8 이 값을 벗겨 떨어진다 — 위 실측). CSP 는 §7 글자 검사에 한 줄, §6 에 「확정 시안에 CSP `<meta>` 가 없으니 `viewer-spec.md` §1 의 문자열을 넣는다」 한 문장. 확정 시안 파일(`.mockups/`, git 밖)은 고치지 않는다
- KH-2 러너 시간 결정: 킷에 시간 상한 검사를 넣지 않는다. 이 계약 SK-16 에 상한을 두고, CI 에 시간 제한을 걸지는 이 묶음 밖이다
- 고치지 않는 파일: `docs/onboarding-kit/examples/fcm-ios-setup-guide.md` 와 `docs/` 아래 HTML 전부. 바뀐 SKILL.md · references 에서 만든 문서 페이지(`docs/onboarding-kit/setup-guide.html` · `format-checklist.html` 등)는 부모의 「문서 페이지 다시 맞추기」 단계가 맡는다. 기존 마크다운 경고 전체 정리(VS-26)도 부모 몫이다
- 킷 버전 올림 · marketplace.json · CI 파일(`.github/workflows/ci.yml`)은 이 계약 밖이다. 러너 둘은 이미 CI 단계로 돈다(`ci.yml:99` · `:102`)
- 커밋 규칙: `git add <경로>` 뒤 `git commit -o <경로>`. 한 커밋에 킷 하나 — `docs/howto/design-brief.md` 는 howto-kit 커밋에, `scripts/check-reviewer-protocol-copies.py` 는 킷 없는 따로 커밋에 싣는다. `git add -A` · `git stash` · push · 가지 바꾸기 금지
- 측정 도구 네 파일(아래 「회귀 게이트」)은 1 회차 봉인 커밋 뒤 `.harness/` 만 든 커밋(`ee1fac4`)으로 실었다. 고치지 않는다(AR-03 이 지문으로 잰다). 2 회차는 새 측정 도구를 더하지 않는다 — 바로잡은 RE-01 · RE-02 측정은 `git` 명령 하나다
- 바로잡은 측정 실측(2026-09-27 12:16, 작업 폴더 `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak2-k4`, zsh · bash 같은 값): 시작 판 `git diff --diff-filter=A --name-only 6378948 6378948 -- scripts '*.sh' '*.py' ':(exclude).harness'` 0 줄 · 가지 끝(`be58f8b`) `git diff --diff-filter=A --name-only 6378948 chore/ak2-k4 -- scripts '*.sh' '*.py' ':(exclude).harness'` 0 줄. 같은 가지 끝에서 1 회차 원 측정은 5 줄(위 다섯 도우미). `.harness` 밖에 새로 더한 파일은 onboarding 픽스처 넷(`gate-blocking-ok.md` · `gate-fail-blocking-empty.md` · `gate-fail-blocking-nourl.md` · `gate-fail-ledger-double-source.md`)뿐이라 확장자 한정에 걸리지 않는다
- 바로잡은 측정 음성 대조 실측(같은 시각): 가지 끝을 scratchpad 로 복제해 `onboarding-kit/skills/setup-guide/evals/run-extra.sh` · `scripts/check-extra.py` · `.harness/.meta/after-0926-kits-api-onboarding-howto/extra.sh` 세 파일을 더한 커밋에서 바로잡은 측정 2 줄(킷 · scripts 쪽 둘만, `.harness` 쪽은 빠짐) — 0 이 아니므로 N/A 사유가 거짓이 되어 FAIL 이다. 같은 사본에서 원 측정은 8 줄
- 구현자는 `tone-kit:tone-guide` 1 단계를 구현 전에 부르고 5 단계를 완료 선언 전에 돌린다(사용자 전역 규칙). 결과는 notes 에 남기고 조건으로 두지 않는다
- 커버리지 해소: SK-05 — 산문 대상 세 파일을 측정 절이 경로로 모두 적었다
- 커버리지 해소: AR-01 — 필수 13 경로를 조건 산문과 `m.sh` `AR-01)` 파이썬 목록에 같은 표기로 적었다

## 회귀 게이트

측정 도구 — `.harness/.meta/after-0926-kits-api-onboarding-howto/` 의 `m.sh` · `ob.py` · `ka5.sh` · `stub.py`. 부르는 꼴은 `bash .harness/.meta/after-0926-kits-api-onboarding-howto/m.sh <작업 폴더 절대 경로> <조건 ID>` 이다. 구간 기준은 `6378948`, 상한은 가지 끝 `git rev-parse --verify -q chore/ak2-k4` 이다(해석이 안 되면 `UNRESOLVED` 로 멈춘다 — `HEAD` 로 떨어지지 않는다).
DG-02 는 환경 변수 둘을 받는다 — `MDL=<markdownlint-cli2 0.23.2 경로>` (예: 세션 scratchpad `mdl/node_modules/.bin/markdownlint-cli2`), `PYF=<pyflakes 가 든 파이썬>` (예: scratchpad `k4/venv/bin/python`). 없으면 `STOP` 으로 멈춘다.
두 예시 경로는 이 세션 scratchpad 에만 있다. 다른 세션에서 다시 잴 때는 새로 마련한다 — `npm i --prefix <폴더> markdownlint-cli2@0.23.2` 뒤 `MDL=<폴더>/node_modules/.bin/markdownlint-cli2`, `python3 -m venv <폴더> && <폴더>/bin/pip install pyflakes` 뒤 `PYF=<폴더>/bin/python`.
AR-04 의 로컬 CI 스크립트 사본 `ci-local.sh` 는 교차 진단(2026-09-27) 지적으로 도구 폴더에 더했다. AR-03 지문은 기존 네 파일만 잰다 — 사본은 AR-04 의 fallback 지문 `59fe55125c0dbc77` 로 따로 잰다.
교차 진단이 짚은 `DG-02` 측정기의 `comm` 앞 정렬(`sort -u`, 남은 일 목록 CS-4 는 `LC_ALL=C sort`)은 두 입력을 같은 방식으로 정렬해 지금 값이 맞다. 도구는 봉인 뒤 고치지 않으므로 그대로 두고 notes 「남은 것」 에 적는다.

## Skill

- [ ] SK-01: `/api-ui` 8 절 보고 목록의 「Step 7 브라우저 확인」 줄이 상태 네 가지의 칩 숫자와 트리 줄 수를 옮기라고 적는다 (KA-1) [exact]
      Given: 끝 판 작업 폴더 · When: `m.sh <W> SK-01` · Then: `step7_lines=1 chips=1 rows=1`
      (8 절 범위 = `## 8.` 줄부터 `# References` 앞까지. 시작 판 값 `chips=0 rows=0`)
- [ ] SK-02: `/api-verify` 가 경로 간 불변식 판정 줄을 항목별로 적는 꼴 — 줄 앞에 `<엔드포인트 id>: ` 앞머리 — 을 정한다 (KA-2 만드는 쪽) [exact]
      측정: `m.sh <W> SK-02` 가 `s6_prefixed_example>=1 s6_id_word>=1 s9_item7_id=1`
      (6 절 = `## 6.` 부터 `## 7.` 앞, 9 절 7 항 = 9 절 안 `7. ` 로 시작하는 줄. 앞머리 예시는 `orders.list: $.meta.total=47 · …` 처럼 `<소문자 이름>.<이름>: $.` 꼴. 시작 판 셋 다 0)
- [ ] SK-03: `/api-ui` 2 절이 판정 줄을 `unjudged` 배열에 옮길 때 `<엔드포인트 id>: ` 앞머리를 떼고 나머지를 글자 그대로 옮긴다고 적는다 (KA-2 받는 쪽) [exact]
      측정: `m.sh <W> SK-03` 가 `s2_strip_rule>=1` (2 절 = `## 2.` 부터 `## 3.` 앞, 한 줄에 `엔드포인트 id` 와 `앞머리` 가 함께. 시작 판 0)
- [ ] SK-04: 뷰어 스펙이 보류 · flaky 를 화면에 어떻게 보일지 정한다 — 상태 값은 넷(`'pass' | 'fail' | 'pending' | 'unjudged'`) 그대로이고, 보류와 flaky 는 각각 `'fail'` 로 두며 글자 표지와 `aria-label` 을 준다 (KA-3) [exact]
      Given: 끝 판 `api-kit/skills/api-ui/references/viewer-spec.md` · When: `m.sh <W> SK-04`
      Then: `hold>=1 flaky>=1 hold_fail>=1 flaky_fail>=1 label>=1 state_enum=1 new_state=0`
      (`hold_fail` = `보류` 와 `'fail'` 이 한 줄에 · `flaky_fail` = `flaky` 와 `'fail'` 이 한 줄에 · `label` = `보류` 나 `flaky` 가 든 줄 중 `aria-label` 이 든 줄. `new_state` = `state:'hold'` · `state:'flaky'` · `state:'보류'` 줄 수. 시작 판 `hold=0 flaky=0`)
- [ ] SK-05: 킷 문서 세 곳이 binary64 밖 숫자에 대해 RFC 7493 §2.2 는 SHOULD NOT 인데 킷은 실패로 막는다 — 표준보다 엄격하다 — 고 밝힌다 (KA-4) [exact, enumerated]
      측정: `m.sh <W> SK-05` 가 세 줄 모두 `strict_note>=1` — `api-kit/skills/api-contract/SKILL.md` · `api-kit/skills/api-verify/SKILL.md` · `api-kit/skills/api-probe/SKILL.md`
      (한 줄에 `RFC 7493` · `SHOULD NOT` · `엄격` 셋이 함께. 시작 판 세 파일 0)
- [ ] SK-06: `/api-contract` 9 절 `.hurl` 예시에 index assertion 이 없고, 그 예시가 항목 0 · 1 · 2 개 응답 모두에서 통과한다 (KA-5 예시) [goal]
      Given: 끝 판 · 이 기계의 hurl 8.0.1 · When: `m.sh <W> SK-06` (예시 블록을 뽑아 `stub.py` 가 띄운 로컬 응답에 `hurl --test` 를 돌린다)
      Then: `index_asserts=0 collection_line=1` 이고 `n=0 rc=0` · `n=1 rc=0` · `n=2 rc=0`
      음성 대조: 예시를 `jsonpath "$.data[*].id" isCollection` 으로 바꾼 사본은 `n=1 rc=4` 로 떨어진다(봉인 전 실측). 시작 판은 `index_asserts=1` · `n=0 rc=4`
- [ ] SK-07: `/api-ui` 가 CSP `<meta>` 를 잰다 — 7 절 명령 블록에 `grep -c 'http-equiv="Content-Security-Policy"' "$UI"` 줄이 `기대 1` 주석과 함께 있고, 7 절 기대값 표에 CSP 행이 있으며, 6 절이 CSP 를 적는다 (KA-5 CSP) [exact]
      측정: `m.sh <W> SK-07` 가 `s7_cmd=1 s7_row>=1 s6_csp>=1`
      양성 · 음성 대조(같은 출력 둘째 줄): 같은 명령이 예시 `ui.html` 에 `example_csp=1`, 확정 시안 v8 에 `mockup_v8_csp=0` — 시안만 믿으면 CSP 가 빠진다는 것이 이 검사로 드러난다. 시작 판 `s7_cmd=0 s7_row=0 s6_csp=0`
- [ ] SK-08: onboarding `gate_cases` 에 「한 Step 에 출처 둘 · 출처 없는 Step 없음」 입력이 등록되고 G1 FAIL 을 기대한다 (KO-1) [exact]
      Given: 끝 판 · When: `m.sh <W> SK-08` · Then: `ko1_cases>=1` 이고 `runner_rc=0` · `EVALS declared=D ran=D fail=0`
      (`ko1_cases` = 픽스처의 Step 별 `**출처:**` 줄 수가 최댓값 2 · 최솟값 1 이상이고 기대 출력에 `G1_LEDGER FAIL` 로 시작하는 줄이 있는 사례 수. 시작 판 0)
      음성 대조: `m.sh <W> NEG-KO` 의 `g1_mutated=1` 사본(G1 수 비교를 `if false` 로 끈 SKILL.md)에서 `g1_neg_rc=1`
- [ ] SK-09: `guide_gate` 가 막는 요구 세 칸을 잰다 — 출력에 `G5_BLOCKING PASS` 또는 `G5_BLOCKING FAIL` 로 시작하는 줄이 하나 생기고, 배포 예제 `docs/onboarding-kit/examples/fcm-ios-setup-guide.md` 는 스택 `flutter` 로 `G5_BLOCKING PASS` 와 `GATE_PASS` 를 zsh · bash 같은 출력으로 낸다 (KO-2 만드는 쪽) [exact]
      측정: `m.sh <W> SK-09` 가 `example_same_shell=1 example_g5_pass=1 example_gate_pass=1` (시작 판 `example_g5_pass=0`)
- [ ] SK-10: 게이트 출력을 받는 쪽이 새 줄을 따라간다 — `gate_cases` 의 모든 사례 기대 출력에 `G5_BLOCKING ` 줄이 정확히 하나, SKILL.md 의 출력 줄 수 문장이 「5 줄」 에서 「6 줄」 로, 체크리스트 1 항의 검사 이름 나열에 G5 가 든다 (KO-2 받는 쪽) [exact, enumerated]
      측정: `m.sh <W> SK-10` 가 `cases=g5_one` (두 값이 같다) · `five_lines=0 six_lines>=2 run_line_g5=1` · `runner_rc=0`
      (`run_line_g5` = `G1(출처 원장 완전성)` 이 든 줄 중 `G5` 가 든 줄. 시작 판 `g5_one=0 five_lines=2 six_lines=0 run_line_g5=0`)
- [ ] SK-11: `/setup-guide` 가 iOS Firebase SDK 설치 방식을 원문대로 안내한다 — 한 줄에 네이티브 Apple 가이드는 Swift Package Manager · CocoaPods 는 폐기 예정(Firebase 12 가 마지막 major) · 출처 URL 이 함께 있고, Flutter 가이드는 FlutterFire 의 CocoaPods 절차를 SPM 으로 바꾸지 않는다고 적는다 (KO-2, EX-11) [exact]
      측정: `m.sh <W> SK-11` 가 `cocoapods_line>=1 flutter_keep>=1 evals_spm_assert=1`
      (`cocoapods_line` = 한 줄에 `Swift Package Manager` · `CocoaPods` · `Firebase 12` · `https://firebase.google.com/docs/ios/setup`. `flutter_keep` = `CocoaPods` 와 `Flutter` 가 한 줄에. `evals_spm_assert` 는 기존 assertion 이 남았는지. 시작 판 `cocoapods_line=0 flutter_keep=0`)
- [ ] SK-12: `howto-reviewer` 가 미검증 규칙 정본 사본(조항 · 4 요건)을 글자 그대로 들고, 사본 출처 줄과 `[미확인]` 출처 등급을 미검증 마커와 가르는 한 줄을 두며, 도구는 읽기 전용 그대로다 (KH-1) [exact]
      측정: `m.sh <W> SK-12` 가 `howto_ok=1` · `source_line=1 grade_line>=1 tools=[Read, Grep, Glob]`
      (`source_line` = `사본 출처:` 로 시작하고 `qa-evaluation-guide.md` 가 든 줄 수, `grade_line` = `[미확인]` 과 `출처 등급` 이 한 줄에. 시작 판 `howto_ok=0 source_line=0 grade_line=0`)
- [ ] SK-13: `/howto-audit` Phase 4 리포트가 에이전트 판정의 미검증 두 분류 건수 칸을 두고, 미검증 행은 PASS 로 세지 않는다고 적는다 (KH-2) [exact]
      측정: `m.sh <W> SK-13` 가 `unverified_line>=1 not_pass>=1`
      (Phase 4 범위 = `### Phase 4` 부터 다음 `## ` 앞. `unverified_line` = `[미검증:ENV]` 와 `[미검증:INVALID]` 가 한 줄에, `not_pass` = `미검증` 과 `PASS 로 세지 않는다` 가 한 줄에. 시작 판 둘 다 0)
- [ ] SK-14: 출처 원장 9 절이 DITA 2.0 확인 결과를 적는다 — OASIS DITA 위원회 페이지 주소, DITA 1.3 승인일 2015-12-17, 조회일 2026-09-26, DITA 2.0 승인 기재가 없다는 사실 (KH-2, EX-12) [exact]
      측정: `m.sh <W> SK-14` 가 `dita_lines>=1 url>=1 d13>=1 checked>=1`
      (9 절 범위 = `## 9.` 부터 `## 이 원장을 쓰는 법` 앞. 시작 판 넷 다 0)
- [ ] SK-15: howto-kit 러너가 자기 음성 대조를 킷 안에 든다 — Given 러너의 assertion 대조(`grep -qF -- "$assertion"`) 또는 셸 대조(`[ "$out_zsh" = "$out_bash" ]`)를 `true` 로 바꾼 킷 사본 · When 그 사본의 러너를 `sh` 로 돌린다 · Then 러너가 `EVALS_FAIL` 과 종료 코드 1 을 낸다. 고치지 않은 사본은 `EVALS_PASS` · 0 이다 (KH-2) [goal]
      측정: `m.sh <W> SK-15` 가 `lit_assert=1 lit_shell>=1` 이고 `orig mutated=0 rc=0 last=EVALS_PASS` · `assert mutated=1 rc=1 last=EVALS_FAIL` · `shell mutated=1 rc=1 last=EVALS_FAIL`
      음성 대조: 이 조건 자체가 음성 대조다 — 시작 판은 `assert mutated=1 rc=0 last=EVALS_PASS` · `shell mutated=1 rc=0 last=EVALS_PASS` 로 무력화를 못 잡는다(봉인 전 실측). `mutated=0` 이면 변이가 안 들어간 것이라 FAIL 이다
- [ ] SK-16: howto-kit 러너 전체 실행이 이 기계에서 30 초 안에 끝난다 (KH-2 러너 시간 · 성능) [exact]
      측정: `m.sh <W> SK-16` 가 `rc=0` · `EVALS total=N pass=N fail=0` · `seconds<=30` (벽시계, `python3 time.time()` 차이. 시작 판 `total=33` · `seconds=9.6`)
- [ ] SK-17: 설계 기록 `docs/howto/design-brief.md` 의 C5 줄이 러너가 세 셸(`zsh·bash·sh`)을 대조한다고 적는다 (KH-2 `design-brief.md:385`) [exact]
      측정: `m.sh <W> SK-17` 가 `c5_three=1` (`| C5 |` 로 시작하는 줄에 `zsh·bash·sh`. 시작 판 0)

## Script

- [ ] SC-01: 저장소 검사 `scripts/check-reviewer-protocol-copies.py` 가 howto-reviewer 를 사본 대상에 넣는다 — 여덟 파일 모두 `OK`, 제외 0, 종료 코드 0, 머리 설명이 「여덟」 (KH-1 받는 쪽) [exact]
      측정: `m.sh <W> SC-01` 가 `copies_rc=0 ok_lines=8 howto_ok=1 checked=8 violations=0 infra_errors=0 excluded=0 … docstring_eight=1`
      음성 대조: `m.sh <W> NEG-KH1 chore/ak2-k4` (가지 끝 판을 풀어 howto-reviewer 의 `1. **마커는` 줄을 지운 사본) 가 `neg_rc=1 1` — 시작 판 `neg_rc=0 0`

## Error

- [ ] ER-01: 판정 줄 꼴을 정한 뒤에도 예시 입력과 예시 출력이 맞물린다 — 예시 리포트의 `→ 판정 불가` 줄마다 `<엔드포인트 id>: ` 를 떼면 예시 `ui.html` 그 항목의 `unjudged` 배열에 글자 그대로 있다 (KA-2 회귀 방지) [exact]
      측정: `m.sh <W> ER-01` 가 `report_unjudged=2 matched=2`
      음성 대조: 예시 `ui.html` 의 `$.data.onHand` 를 `$.data.onHandX` 로 바꾼 복제본에서 `matched=1` (봉인 전 실측)
- [ ] ER-02: KA-4 는 글만 바꾸고 동작은 그대로다 — binary64 밖 숫자는 계속 실패(`/api-contract`) · 비교 불가(`/api-verify`) · I-JSON 검문 대상(`/api-probe`) 이다 [exact, enumerated]
      측정: `m.sh <W> ER-02` 가 `contract_gate=1 verify_class=1 probe_gate=1` (시작 판과 같은 값. `contract_gate` 는 `/api-contract` 2 절 목록 줄, `verify_class` 는 `/api-verify` 5 절 비교 불가 줄, `probe_gate` 는 `/api-probe` 검문 2 번 줄)
- [ ] ER-03: `guide_gate` G5 가 세 칸 결함 두 가지를 잡는다 — 칸이 빈 행, 출처 칸에 `http` 주소가 없는 행. 두 결함을 든 픽스처가 `G5_BLOCKING FAIL` 과 `GATE_FAIL` 을 기대하는 사례로 등록되고 러너가 통과한다 (KO-2 오류 경로) [exact]
      측정: `m.sh <W> ER-03` 가 `g5_fail_cases>=2 empty_kind>=1 nourl_kind>=1` · `runner_rc=0`
      음성 대조: `m.sh <W> NEG-KO` 가 `g5_mutated=1` (SKILL.md 사본의 `echo "G5_BLOCKING FAIL` 을 `PASS` 로 바꿈) 이고 `g5_neg_rc=1`

## Architecture

- [ ] AR-01: 바뀐 파일이 정한 범위 안이다 [exact, enumerated]
      Given: 이 계약의 커밋이 모두 `chore/ak2-k4` 에 들어간 뒤 · 상한 `git rev-parse --verify -q chore/ak2-k4` (`HEAD` 금지)
      측정: `m.sh <W> AR-01` (= `git diff --name-status 6378948 <상한> -- . ':(exclude).harness'`) 가 `scope_out=0 required_missing=0 new_onboarding_fixtures>=3`
      필수 수정 13 경로: `api-kit/skills/api-ui/SKILL.md` · `api-kit/skills/api-ui/references/viewer-spec.md` · `api-kit/skills/api-verify/SKILL.md` · `api-kit/skills/api-contract/SKILL.md` · `api-kit/skills/api-probe/SKILL.md` · `onboarding-kit/skills/setup-guide/SKILL.md` · `onboarding-kit/skills/setup-guide/evals/evals.json` · `howto-kit/agents/howto-reviewer.md` · `howto-kit/skills/howto-audit/SKILL.md` · `howto-kit/references/provenance-notes.md` · `howto-kit/evals/run-evals.sh` · `docs/howto/design-brief.md` · `scripts/check-reviewer-protocol-copies.py`
      양성 대조: 임시 복제본에서 `onboarding-kit/README.md` 한 줄을 고친 커밋을 더하면 `scope_out=1` 과 `OUT M onboarding-kit/README.md` (봉인 전 실측)
      선택 수정 2 경로: `onboarding-kit/skills/setup-guide/references/format-checklist.md` · `howto-kit/evals/evals.json`. 새 파일은 `onboarding-kit/skills/setup-guide/evals/fixtures/` · `howto-kit/evals/fixtures/` 아래만. 그 밖의 추가 · 수정 · 삭제는 `scope_out` 에 센다(생성물 없음 — 이 레포에 codegen 이 없다)
- [ ] AR-02: 커밋이 킷별로 나뉘고 봉인 커밋이 구현보다 먼저다 [exact]
      Given: AR-01 과 같다 · 측정: `m.sh <W> AR-02` 가 `mixed=0 seal_commit_files=1 impl_before_seal=0`
      양성 대조: 임시 복제본에서 `howto-kit/references/provenance-notes.md` 와 `scripts/check-reviewer-protocol-copies.py` 를 한 커밋에 담으면 `mixed=1` (봉인 전 실측)
      (묶음 = `api-kit` · `onboarding-kit` · `howto-kit`(`docs/howto/` 포함) · `scripts`. `.harness/` 경로는 세지 않는다. 한 커밋에 묶음 둘 이상이면 `mixed` 에 센다. 봉인 커밋 = 1 회차 계약 파일 `.harness/sprint-contract-after-0926-kits-api-onboarding-howto.md` 를 처음 더한 커밋 `927c2a7` — `m.sh` 가 그 경로를 박아 둔다)
- [ ] AR-03: `.harness/` 계약 봉인이 하나도 깨지지 않고 측정 도구가 봉인 때 그대로다 [exact]
      측정: `m.sh <W> AR-03` 첫 줄에 `SEAL_BROKEN` 이 없고, 둘째 줄이 `tools_sha=8569f2af6e22daa3` (네 파일 `m.sh` · `ob.py` · `ka5.sh` · `stub.py` 를 이 차례로 이어 붙인 sha256 앞 16 자리, 봉인 전 실측)
      (봉인 전 실측 첫 줄: `10 SEAL_ABSENT   89 SEAL_OK` — 이 계약은 봉인 전이라 ABSENT 쪽에 들었다)
- [ ] AR-04: 로컬 CI 가 끝 판에서 봉인 전과 같게 통과한다 [exact]
      Given: 끝 판 작업 폴더 · When: `TMPDIR=<빈 폴더> bash /Users/jackson/Hub/10_Dev/claude-plugins/.harness/handoff/2026-09-26-tools/ci-local.sh <W>` · Then: `rc=0` 줄 수가 봉인 전 값(아래)과 같고, `rc=0` 이 아닌 줄은 `feedback-agg-test SKIP (yq 없음)` 하나뿐이다
      (봉인 전 값: 2026-09-27 11:0x 시작 판에서 `rc=0` 25 줄, 그 밖의 줄은 `feedback-agg-test SKIP (yq 없음)` 하나)
      도구 위치 3 단계: 기본 = 위 경로(git 밖 파일). 그 파일이 없거나 sha256 앞 16 자리가 `59fe55125c0dbc77` 가 아니면 fallback = 이 계약 도구 폴더의 사본 `.harness/.meta/after-0926-kits-api-onboarding-howto/ci-local.sh`(같은 값 `59fe55125c0dbc77`, 봉인 전 실측). 둘 다 없으면 `[미검증:ENV]` 와 4 요건으로 적는다 — PASS 로 세지 않는다

## Anti-patterns

- [ ] AP-03: bare code fence 금지 — `python3 scripts/validate-plugin.py --check=code-fence api-kit` · `onboarding-kit` · `howto-kit` 세 번 모두 종료 코드 0
      양성 대조: 임시 복제본의 `howto-kit/skills/howto-audit/SKILL.md` 끝에 언어 힌트 없는 펜스를 붙이면 `Exit: 2` (봉인 전 실측). references 쪽 펜스는 이 검사 범위 밖이라 DG-02 의 MD040 이 잡는다
- [ ] AP-04: SKILL.md / agents/*.md frontmatter 에 name 필드 누락 없음 — `python3 scripts/validate-plugin.py howto-kit` · `onboarding-kit` · `api-kit` 세 번 모두 종료 코드 0 (V1 포함)

## Reusability

- [ ] RE-01: N/A (새 공용 코드가 없다 — G5 검사는 기존 `guide_gate` 함수 안, 러너 자기 대조는 기존 `run-evals.sh` 안에 들고, 킷은 따로 설치되어 다른 킷이 부를 수 없다. 측정: `git diff --diff-filter=A --name-only 6378948 chore/ak2-k4 -- scripts '*.sh' '*.py' ':(exclude).harness'` 0 줄)
      (1 회차 측정에 `':(exclude).harness'` 를 더한 것이다 — 이 계약의 측정 도우미가 든 `.harness/` 는 킷 · scripts 가 아니다. 봉인 전 실측: 시작 판 `6378948` 0 줄 · 가지 끝 `be58f8b` 0 줄, 같은 가지 끝의 1 회차 원 측정 5 줄)
      음성 대조: 가지 끝 복제본에 `onboarding-kit/skills/setup-guide/evals/run-extra.sh` · `scripts/check-extra.py` · `.harness/.meta/after-0926-kits-api-onboarding-howto/extra.sh` 를 더한 커밋에서 이 측정이 2 줄(앞의 둘) — N/A 사유 거짓 → FAIL (봉인 전 실측)
- [ ] RE-02: 이미 있는 것을 다시 만들지 않았다 — 새 검사 스크립트 · 새 러너 파일이 없다 (측정: `git diff --diff-filter=A --name-only 6378948 chore/ak2-k4 -- scripts '*.sh' '*.py' ':(exclude).harness'` 0 줄, 그리고 `onboarding-kit/skills/setup-guide/evals/run-gate-evals.sh` 는 `git diff --quiet 6378948 chore/ak2-k4 -- <그 경로>` 종료 코드 0 — 러너를 고치지 않고 등록만으로 새 픽스처를 돌린다)
      (첫 측정은 RE-01 과 같은 바로잡은 명령이다. 봉인 전 실측: 가지 끝 `be58f8b` 에서 0 줄 · 러너 `git diff --quiet` 종료 코드 0)
      음성 대조: RE-01 과 같은 복제본에서 첫 측정 2 줄 → FAIL (봉인 전 실측)

## Diagnostics

- [ ] DG-01: N/A (commands.analyze `bash -n scripts/release.sh` 는 `scripts/release.sh` 만 잰다 — 이번 변경과 교집합 0. 측정: `git diff --name-only 6378948 chore/ak2-k4 | grep -c '^scripts/release.sh$'` 가 0)
- [ ] DG-02: 바뀐 `.md` · `.sh` · `.py` 파일의 더한 줄에 새 편집기 경고 0 개, 바뀐 `.json` 은 모두 읽힌다 (스펠체크 제외) [exact]
      측정: `MDL=… PYF=… m.sh <W> DG-02` 가 `new_warnings=0` 이고 `json_bad` 줄 0 개 (markdownlint-cli2 0.23.2 · MD013 끔 = 편집기 확장과 같은 설정, shellcheck, pyflakes)
      양성 대조: 임시 복제본에 MD040 한 줄 · pyflakes 한 줄을 넣은 커밋에서 `new_warnings=2` (봉인 전 실측)
- [ ] DG-03: N/A (commands.test `bash scripts/release.sh` 는 이번 변경 파일을 재지 않는다 — DG-01 과 같은 측정 0. 실제 시험은 SK-08 · SK-10 · SK-15 · SK-16 · AR-04 가 돌린다)
- [ ] DG-04: N/A (구동할 앱 · 서버가 없다 — 바뀐 것은 문서 · 셸 함수 · 시험 러너 · 검사 스크립트. 측정: 바뀐 파일에 실행 진입점(앱 · 서버) 0 개. 실행 결과는 SK-06 · SK-15 · AR-04 가 잰다)
