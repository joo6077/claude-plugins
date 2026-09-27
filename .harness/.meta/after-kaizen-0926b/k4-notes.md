# k4 — api · onboarding · howto-kit 남은 것 (2026-09-27)

계약 `.harness/sprint-contract-after-0926-kits-api-onboarding-howto.md` — 조건 33 개, 봉인 `conditions_digest: sha256:ed5edc70a958a281` · `measurement_digest: sha256:d4cffb14fe02b098` (봉인 커밋 `927c2a7`, 파일 1 개). 교차 진단 지적 셋은 봉인 전에 반영했다(AR-04 로컬 CI 스크립트 사본과 3 단계 문장, DG-02 도구 다시 마련하는 명령, `comm` 앞 정렬 메모).

시작할 때 작업 폴더에는 계약과 측정 도구 넷만 커밋 안 된 채 있었다. 앞 단계가 남긴 QA 리포트는 없었다.

## 항목별 결과

| 항목 | 한 일 | 조건 · 자기 측정 |
| --- | --- | --- |
| KA-1 | `/api-ui` §8 보고 줄에 상태 네 가지의 `chips` · `rows` | SK-01 `step7_lines=1 chips=1 rows=1` |
| KA-2 | `/api-verify` §6 판정 줄 앞에 `<엔드포인트 id>:` 앞머리, §9 7 항에도. `/api-ui` §2 는 앞머리를 떼고 그 항목 `unjudged` 에 옮긴다. 뷰어 스펙 두 곳도 같게 | SK-02 `s6_prefixed_example=2 s6_id_word=1 s9_item7_id=1` · SK-03 `s2_strip_rule=1` · ER-01 `report_unjudged=2 matched=2` |
| KA-3 | 뷰어 스펙: 보류 · flaky 는 `state:'fail'` 에 `failMark` 와 글자 표지 · `aria-label`, 요약 칩은 FAIL 로 센다 | SK-04 `hold=3 flaky=3 hold_fail=3 flaky_fail=3 label=2 state_enum=1 new_state=0` |
| KA-4 | 세 파일에 「RFC 7493 §2.2 는 SHOULD NOT, 킷은 실패로 막는다 — 표준보다 엄격한 킷 정책」 | SK-05 세 파일 `strict_note=1` · ER-02 `contract_gate=1 verify_class=1 probe_gate=1` |
| KA-5 예시 | `/api-contract` §9 에서 `$.data[0].id` 줄을 빼고, 지킬 것에 이유(빈 목록 종료 코드 4 · `[*]` 한 항목 벗겨짐) | SK-06 `index_asserts=0 collection_line=1` · `n=0/1/2 rc=0` |
| KA-5 CSP | `/api-ui` §6 에 시안에 CSP 가 없으니 스펙 §1 문자열을 넣으라는 문장, §7 에 검사 줄과 표 행 | SK-07 `s7_cmd=1 s7_row=1 s6_csp=1` · `example_csp=1 mockup_v8_csp=0` |
| KO-1 | 픽스처 `gate-fail-ledger-double-source.md`(Step 1 출처 둘 · Step 2 하나) 등록, 기대 `G1_LEDGER FAIL steps=2 ledger=3` | SK-08 `ko1_cases=1` · `runner_rc=0 EVALS declared=11 ran=11 fail=0` |
| KO-2 세 칸 | `guide_gate` G5: 막는 요구 표의 빈 칸 · 주소 없는 출처 칸을 센다. 출력 6 줄. 기존 사례 7 개 기대 출력에 G5 줄, 새 픽스처 셋(정상 표 · 빈 칸 · 주소 없음) | SK-09 `example_same_shell=1 example_g5_pass=1 example_gate_pass=1` · SK-10 `cases=11 g5_one=11 five_lines=0 six_lines=2 run_line_g5=1` · ER-03 `g5_fail_cases=2 empty_kind=1 nourl_kind=1` · NEG-KO `g5_neg_rc=1` · `g1_neg_rc=1` |
| KO-2 CocoaPods | Gotcha 1 에 두 줄: 네이티브 Apple 은 SPM(원문 인용 · 폐기 날짜 없음), Flutter 는 FlutterFire 절차를 SPM 으로 바꾸지 않는다 | SK-11 `cocoapods_line=1 flutter_keep=1 evals_spm_assert=1` |
| KO-2 서비스 계정 키 · 평가 날짜 | 하지 않음 — 바깥 근거 없음(계약 `## 범위 경계`) | — |
| KH-1 | howto-reviewer 에 평가 가이드 v5.1 미검증 규칙 사본(조항 · 4 요건), 출처 줄, `[미확인]` 출처 등급을 가르는 한 줄. 검사 스크립트 여덟 · 제외 0 | SK-12 `howto_ok=1 source_line=1 grade_line=1 tools=[Read, Grep, Glob]` · SC-01 `copies_rc=0 ok_lines=8 checked=8 violations=0 infra_errors=0 excluded=0 docstring_eight=1` · NEG-KH1 `neg_rc=1 1` |
| KH-2 리포트 | `/howto-audit` Phase 4 에이전트 줄에 N/A · `[미검증:ENV]` · `[미검증:INVALID]` 칸, 미검증 row 는 PASS 로 세지 않는다 | SK-13 `unverified_line=1 not_pass=1` |
| KH-2 DITA 2.0 | 출처 기록 9 절에 확인 결과 한 문단(`[미확인]` 건수 제목은 그대로 — 킷이 기대는 근거가 아니다) | SK-14 `dita_lines=1 url=1 d13=1 checked=1` |
| KH-2 러너 자기 대조 | 판정을 `judge_case` 로 묶고, 알려진 나쁜 입력 둘(없는 assertion · 셸 출력 차이)을 돌려 잡는지 보는 두 줄 | SK-15 `lit_assert=1 lit_shell=2` · `orig rc=0 EVALS_PASS` · `assert mutated=1 rc=1 EVALS_FAIL` · `shell mutated=1 rc=1 EVALS_FAIL` |
| KH-2 러너 시간 | 바꾸지 않음. 사례가 33 → 35 | SK-16 `rc=0 total=35 pass=35 fail=0 seconds=13.2` (먼저 잰 값 9.3 · 10.2) |
| KH-2 design-brief | C5 를 세 셸 대조로 | SK-17 `c5_three=1` |

범위 · 구조 조건:

- AR-01 `scope_out=0 required_missing=0 new_onboarding_fixtures=4`
- AR-02 `impl_commits=7 mixed=0 seal_commit_files=1 impl_before_seal=0`
- AR-03 `9 SEAL_ABSENT 90 SEAL_OK` · `tools_sha=8569f2af6e22daa3`
- AR-04 로컬 CI `rc=0` 25 줄, 그 밖의 줄은 `feedback-agg-test SKIP (yq 없음)` 하나 (TMPDIR 은 scratch `k4i/ci2`)
- AP-03 · AP-04 세 킷 모두 종료 코드 0
- DG-01 · DG-03 `scripts/release.sh` 교집합 0
- DG-02 `files=17 new_warnings=0`, `json_ok onboarding-kit/skills/setup-guide/evals/evals.json`. 처음 잰 값은 6 이었다(코드 칸 끝 빈칸 MD038 넷 · 맨 주소 MD034 하나 · 빈 칸 표 공백 MD060 하나) — 두 커밋으로 고쳤다
- RE-02 러너 파일 `run-gate-evals.sh` 는 그대로(`git diff --quiet` 0)
- **RE-01 · RE-02 의 「새 스크립트 0 줄」 은 지금 5 줄이다.** 잡힌 다섯은 전부 계약이 싣기로 한 `.harness/` 측정 도구(`ci-local.sh` · `ka5.sh` · `m.sh` · `ob.py` · `stub.py`)이고 킷 쪽은 0 줄이다. 측정에서 `.harness/` 를 빼는 개정 A-01 을 `.harness/sprint-amendments-after-0926-kits-api-onboarding-howto.md` 에 적었다. 방향 계산 `relaxing measured_removed=5` 라 위임으로 동의 처리하지 않았고 동의 칸은 비어 있다

동기화 검사: `sync-docs.py --check-only` 0 · `sync-evals.py --check-only` 0 · `validate-plugin.py` 세 킷 0.

## 커밋

| 커밋 | 묶음 |
| --- | --- |
| `927c2a7` | 계약 봉인 (파일 1 개) |
| `ee1fac4` | `.harness/` 측정 도구 다섯 |
| `f07be35` · `538744a` | api-kit |
| `3b65ecf` · `c420af5` · `c0b0ffb` | onboarding-kit |
| `297df7c` | howto-kit (`docs/howto/design-brief.md` 포함) |
| `c7f301c` | scripts |

## 킷별 버전 판단

- api-kit — patch. 스킬 문서 · 뷰어 스펙 글만 바뀌었다. 판정 줄 앞머리는 새 꼴이지만 예시 리포트가 이미 그 꼴이었다
- onboarding-kit — minor. `guide_gate` 출력이 5 줄에서 6 줄로 바뀌어, 게이트 출력을 받아 쓰는 쪽이 달라진다
- howto-kit — patch. reviewer 사본 · 리포트 칸 · 러너 자기 대조로 판정 기준은 그대로다

## 문서 페이지 차이 (`python3 scripts/detect-docs-drift.py`)

```text
api-kit/skills/api-ui/SKILL.md → docs/api-kit/static-evidence-viewer-contract.html
docs/howto/design-brief.md → docs/howto-kit/design-brief.html  [NEW — 대응 HTML 없음, 신규 생성 + index.html 등록 필요]
onboarding-kit/skills/setup-guide/SKILL.md → docs/onboarding-kit/setup-guide.html
onboarding-kit/skills/setup-guide/references/format-checklist.md → docs/onboarding-kit/format-checklist.html
```

페이지 다시 만들기는 부모 몫이라 손대지 않았다. `design-brief` 줄은 대응 페이지가 원래 없던 문서라 새 페이지를 만들지는 부모가 정한다.

## 톤 대조 (tone-kit:tone-guide 5 단계)

1 단계에서 읽은 것: `.claude/tone-project.md`(어댑터 없음 · 주석 언어 ko) · `tone-kit/references/core-comment.md` · `core-naming.md`(규칙표) · `core-structure.md`(규칙표) · `core-antipatterns.md` · `locale-korean.md`. 어댑터가 없어 스택 전용 대조 목록은 돌리지 않았다. 대상은 구간 `6378948..chore/ak2-k4` 에서 `.harness/` 밖에 더한 줄 310 줄이다.

| 규칙 | 건수 | 판정 |
| --- | --- | --- |
| C-01 · C-02 what 만 말하는 주석 | 0 | 통과 — 새 셸 주석(G5 · 러너 자기 대조)은 왜 필요한지와 되살아나는 증상을 적는다(H 보존 범주) |
| C-04 · F 구분선 | 0 | 통과 |
| C-07 해설 3 줄 초과 | 0 | 통과 — 가장 긴 새 주석이 2 줄 |
| C-10 디자인 툴 참조 | 0 | 통과 |
| C-13 자화자찬 헤더 | 0 | 통과 |
| C-15 주석 종결형 (관측 컨벤션) | 0 | 통과 |
| K-02 번역투 여섯 (locale §8 G-1) | 1 | 위반 아님 — `howto-reviewer.md` 에 옮긴 평가 가이드 사본 「적용된다」. 글자 그대로 옮겨야 사본 검사가 통과한다 |
| K-04 `합니다`체 | 0 | 통과 |
| K-11 새로 지은 이름 (관측 컨벤션) | 0 | 통과 — `failMark` · `judge_case` · `G5_BLOCKING` 은 코드 식별자, 글에서는 「글자 표지」 「보류」 처럼 하는 일로 적었다 |
| N-07 fallback 접두사 | 0 | 통과 |
| N-08 한 글자 이름 | 1 → 0 | G5 awk 의 `k` · `tb` · `s` 를 `ncell` · `in_table` · `text` 로 고쳤다(`c0b0ffb`). 남은 `i` 는 루프 번호 |
| N-09 무역할 파일명 | 0 | 통과 — 새 파일은 픽스처 넷, 이름이 입력 모양을 말한다 |
| S-03 · S-04 이름이 더하는 게 없는 추출 · 그대로 넘기는 래퍼 | 0 | 통과 — `judge_case` 는 실제 사례와 자기 대조 두 곳이 부른다 |
| S-06 헬퍼 체인 (관측 컨벤션) | 0 | 통과 |
| S-12 같은 역할은 같은 패턴 (관측 컨벤션) | 0 | 통과 — G5 는 G4 처럼 awk 한 번 · `echo` 판정 두 갈래 |

H 보존: 옛 주석은 지우지 않았다. 범위 밖 파일은 건드리지 않았다(AR-01 `scope_out=0`).

## 남은 것

- 개정 A-01(RE-01 · RE-02 측정에서 `.harness/` 빼기)의 사용자 동의. 동의가 없으면 두 줄은 지금 측정대로 사유 거짓이다
- QA 판정 — 이 문서는 판정을 내리지 않았고 계약 status 는 active 그대로다
- 문서 페이지 넷 다시 맞추기(위 표) · 기존 마크다운 경고 전체 정리(VS-26)는 부모 몫
- 교차 진단이 짚은 `DG-02` 측정기의 `comm` 앞 정렬(`sort -u`)은 남은 일 목록 CS-4 의 `LC_ALL=C sort` 와 다르다. 두 입력을 같은 방식으로 정렬해 지금 값은 맞다. 도구는 봉인 뒤라 고치지 않았다
- `/api-ui` 뷰어가 보류 · flaky 표지를 실제로 그리는지는 스펙만 정했고 예시 `ui.html` 은 바꾸지 않았다(계약 범위 밖). 화면 확인 수단이 이 계약 밖이라는 교차 진단 지적이 그대로 남는다
