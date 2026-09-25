# 카이젠 2026-09-24 Final — kaizen-0924-final notes

- 계약: `.harness/sprint-contract-kaizen-0924-final.md` (조건 26 · 기능 조건 18, 봉인 `sha256:81b9a7409e53588b` · `locked_at` 2026-09-25 20:43)
- 개정: `.harness/sprint-amendments-kaizen-0924-final.md` (조건 변경 0 건. 구현이 개선안과 다른 곳 하나 — surface-recipes 페이지 한 문단, `amend_direction: unchanged`)
- 검토: `.harness/.meta/kaizen-0924/final-review.md` — REVIEW 두 회차. 1 회차 반드시 고칠 것 여섯 · 권고 일곱, 2 회차 `VERDICT: CHANGES`(반드시 고칠 것 하나 · 권고 둘)를 DRAFT · SEAL 이 봉인 전에 반영했다
- 사용자 승인 대체: 사용자 위임(세션 기록 queued_command `2026-09-24T04:04:16.964Z`) · Codex 한도 소진(2026-09-24) · 「코덱스 대신에 그냥 너가 알아서 진행하라고」(user `2026-09-24T11:54:58.940Z`) ·
  「코덱스도 사용할 수 있으니깐 사용해」(user `2026-09-25T06:19:45.056Z`) — REVIEW 두 회차 검토로 대신했고, 문서 사이트 페이지 일부를 Codex(`gpt-5.6-sol`, 쓰기)가 만들었다
- 시작 커밋 `511f19b5823886bef5c21dadcd656a692f298db5` · 사이클 기준 `83cfb4f` · 문서 사이트 기준 `390dea8`

## 커밋

모든 커밋 메시지는 `Co-Authored-By` 줄 바로 위에 `Kaizen-Phase: kaizen-0924-final` 이 있다. 커밋은 `git add -- <경로…> && git commit -o -F <메시지> -- <경로…>` 로 내 경로만 실었다.

| 커밋 | 내용 | 조건 |
| --- | --- | --- |
| `509d295` | 봉인 커밋 (계약 파일 1 개) | AR-09 |
| 페이지 마흔넷 | 페이지마다 한 커밋 — 아래 `## 문서 사이트` 표 | AR-03 · DG-04 |
| `18b1b11` | Phase · followups 계약 열아홉 `status: done` 과 QA 리포트 열아홉 (서른여덟 경로) | AR-01 |
| `8370391` | Phase 1 개정 파일 `end_sha` 한 줄 · Phase 7 · 8 · 9 · 11 개정 파일 「교차 진단 뒤 Final 에서 고침」 줄 | ER-03 |
| `7813569` | 처리 배정표 Phase 행 일흔넷 · 미반영 여덟 비고 | AR-02 |
| `3484855` | 옛 값 등록부 새 항목 셋 · backend-kit 예외 셋 | ER-04 |
| `098f671` | `docs/bambu-kit/surface-recipes.html` 한 문단(블록 이름) | AR-03 |
| `55d8a36` | `docs/index.html` harness 다섯 항목 제목 판 번호 | AR-03 |
| `c18e7e0` | changelog 둘 · 연구 기록 셋 · 루트 `CLAUDE.md` 세 줄 | AR-04 · SK-02 |
| `8163d69` | 사이클 상태 · 실패 횟수 · evals 점검 · 정리 기록 · 메모리 후보 · 릴리스 계획 | AR-05 · ER-05 · AR-06 · SC-01 |
| `410dcc9` | 감사 기록 항목 | AR-07 |
| `73462de` | 개정 파일 `end_sha` (`410dcc9`) | AR-08 |
| `fdae7db` | notes · 검토 기록 | AR-08 |
| `507db0f` | 개정 파일에 notes 커밋 sha 로 `end_sha` 한 줄 더 (`fdae7db`) | AR-08 |
| 이 파일을 고친 커밋 | 끝 판 재측정 · 계약 피드백 저장 기록(아래 두 절) | AR-08 |
| 그다음 커밋 | 개정 파일에 그 커밋 sha 로 `end_sha` 한 줄 더 | AR-08 |

저장소 밖 변경(커밋 없음): 전역 피드백 서른넷의 교차 진단 두 칸(ER-01 · ER-02), 가장 오래된 139 개를 `~/.harness/feedback-archive/kaizen-2026-09-24/` 로 옮김(ER-05).
고치기 전 사본은 스크래치 `kaizen/final-fb-before/`(서른넷), 정리 직전 목록은 `kaizen/final-fb-before-cleanup.txt`(639 줄)다.
감사 기록 도구에 넘긴 수동 편집 JSON 은 스크래치 `kaizen/final-manual-edits.json` 이고 커밋하지 않았다(SK-01 (f) `json=14` 유지).

## F1 정합

오케스트레이터 Step F1 교차 Phase 정합. 공통 정의를 읽은 bash 에서 상한 `410dcc9`(개정 파일 첫 `end_sha`)로 돌린 도우미 출력 여덟 줄을 글자 그대로 옮긴다
(`f1.sh` 넷 · `tonegrade.py` 첫 줄 · `toneterms.py` 첫 줄 · `synt.sh` 끝줄 · `amend.sh` 끝줄). `tonegrade.py` · `toneterms.py` 종료 코드는 둘 다 0 이다.
상한을 notes 커밋 `fdae7db` 로 옮겨 다시 돌려도 여덟 줄이 글자까지 같았다(아래 `## 끝 판 재측정`).

```text
p1hand=0 0 0 0 0 0 4 1
parity=1 1
apikit=1 1 1 1 1 1 1
orch16=1 1 1 1 1
rules_old=62 rules_new=63 raised=0 added=[('K-11', ['관측 컨벤션'])]
tone_terms=8 other_files=119 other_terms=652 intersect=0 substring=0
sh=16 sh_bad=0 py=8 py_bad=0 json=14 json_bad=0 yaml=6 yaml_bad=0 all_sh=43 all_sh_bad=0 actionlint_rc=0
ends=2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 p1_last=1 kept=16 xfix=1 1 1 1 p1_remeasure=0 0 guides=2 after=16 after_other=0
```

| 정합 항목 | 결과 |
| --- | --- |
| Phase 1 가이드 변경의 반영 | 옛 문구 여섯 자리 0 · 새 칸 「시도한 우회」 infra-test 4 · rust-reviewer 1 |
| Phase 2 ↔ 3 판 번호 | 평가 가이드 `Parity with` · `Schema link` 가 세 가이드 머리 version · 스키마 현재 판과 글자 그대로 같다 |
| Phase 4 vs 5 ~ 17 | 사이클 전체 셸 열여섯 · 파이썬 여덟 · JSON 열넷 · YAML 여섯 문법 통과, 추적 셸 마흔셋 전체 통과, CI actionlint 0. 사후 점검 `scope-isolation` PASS (DG-05) |
| tone-kit 강도 | 사이클 기준 판보다 오른 규칙 0 — 새 규칙 K-11 은 관측 컨벤션 |
| tone-kit 트리거 | 다른 킷 스킬 · 에이전트 설명과 같은 말 0 · 품는 말 0 |
| api-kit 확정 결정 | 킷 일곱 글자 · 오케스트레이터 Phase 16 다섯 글자 모두 남아 있다 |
| 버전 | 올리지 않았다 — `.harness/.meta/kaizen-0924/release-plan.md` (SC-01) |
| changelog · research-log | Phase 1 ~ 17 · Final 이 들어갔다 (AR-04) |

## 조건별 결과 (BUILD 예행)

상한을 HEAD(구현 커밋 뒤)로 둔 예행 값이다. 기록 상한으로 다시 잰 값은 QA 가 공통 정의로 잰다.

- SK-01 — 위 여덟 줄. SK-02 — `10 Phase` 0 · `17 Phase` 2 · `howto-kaizen (Phase 17)` 1 · `tone-kaizen (Phase 15)` 0 · numstat `3 3 CLAUDE.md`
- SC-01 — `changed=14 cmds=14 lines_ok=1 level_ok=14/14 basis=14 bumped=0` · 대신한다는 문장 1 · `collect_status 1` 1
- ER-01 · ER-02 — `evaluator files=17 by=17 marker=17 tok=17 keep=17 other_diff=0` · `contract files=17 by=17 marker=17 tok=17 keep=17 other_diff=0` · `verify-feedback.sh` 17 · 17 PASS
- ER-03 — 위 `amend.sh` 줄 (`OTHER` 줄 0)
- ER-04 — `clean rc=0 values=18 why_missing=0 unexcluded=0 0 seeded=[1 rc=1 ] [1 rc=1 ] [1 rc=1 ]`
- ER-05 — `before=639 cut=139 archived=139 archived_is_oldest=1 leaked=0 remain_from_list=500 missing=0 aged=0 log=1 log_entries=1` · 180 일 넘은 파일 0
- AR-01 — 열아홉 계약 `status: done` 한 줄 차이 · QA 리포트 열아홉 추적. AR-02 — `rows=96 same_rows=1 phase_rows=74 phase_ok=74 miss_ok=8/8 other_note=0 non_phase_changed=0` · 검사기 `Phase 행 미완료 0` · `TRACKING_TABLE_OK` 종료 코드 0
- AR-03 — `pairs=44 exist=44 changed=44 short=0 accent=0 ext=0 hidden_up=0 tok_new=56/56 tok_old=0/9 html_added=0 html_removed=0` · `nav_ver=5/5` · `title_ver=5/5` · 첫 화면 numstat `5 5` ·
  api-kit 문서 `12/12 PASS` · 내비 등록 176 · 176 · 대비 수치 종료 코드 0
- AR-04 — 다섯 파일 `head=1 missing=[] del_bad=0 url_out=0`, 연구 기록 셋 `urls=` 47 · 15 · 9, `files=5 bad=0` · per-kit 여섯 각 1
- AR-05 — `state=1 phases=17 keys_ok=1 zero=1 last_updated=1 evals=[total_line=1 paths=10/10 adr_cmd=1]` · 더함 · 지움 · 이름 바꿈 0
- AR-06 — `parse=1 candidates=4 keys_bad=0 forbidden=0 grounding_bad=0 actionability_bad=0 evidence_bad=0 need=2/2 tmp_bad=0 out_bad=0` · 승격 원장 0 개
- AR-07 — `append_only=1 head=1 generated=1 manual_orch=1 f1h=29/29 f1k=33/33 new4=4/4 notes=17/17 fnotes=2/2 meta=6/6`
- DG-02 — 마크다운 열여덟 가운데 새 묶음은 감사 기록의 도구 고정 소제목 MD024 셋뿐. AP-03 — 펜스 `0 0`. AP-01 — 더한 줄의 킷 판 번호 0
- DG-04 — 페이지 마흔넷 `44/44 PASS` · `docs` 전체 `177/177 PASS` (종료 코드 0)
- DG-05 — 새 복제본에서 `rc=[000000000000000000000] vpk_rc=0 vpk_pass=13 vpk_bad=0 vpk_skip=[marketplace-sync plugin-json-bumps]`

## 끝 판 재측정

BUILD-FINISH 가 커밋 뒤 상태에서 조건 스물여섯을 계약 측정 글자 그대로 다시 쟀다. 도우미는 계약에서 새로 떼어 냈고(떼는 명령 그대로, 스물여섯 · BUILD 가 쓴 도우미와 파일 내용이 같다),
공통 정의가 개정 파일 마지막 `end_sha:` 인 `fdae7db` 를 `END` 로 읽었다. 모든 조건이 기대값과 같아 고친 것이 없다.

- 위 `## 조건별 결과 (BUILD 예행)` 의 값이 모두 그대로 나왔다. 더해서 AR-08 `heads=6/6 lines=8/8 nohtml=19/19 memo=13/13` · `MISS` 0 줄 · notes 마지막 커밋이 `END`,
  AR-09 `my=107 outside=0 html_extra=0 forbidden=0 unsigned=0 broken=0 self=SEAL_OK seal_files=1`, AP-01 `0`, AP-03 `bare_open_total=0 unclosed_total=0`,
  RE-01 `0` · RE-02 `generated=1` · `accent=0` · 스크립트 `0`, DG-01 · DG-03 `0`
- DG-02 — `new_total=3`, `NEW` 셋이 모두 감사 기록의 도구 고정 소제목 MD024(`### Post-Kaizen Checklist failures` · `### Orchestrator SKILL.md manual edits` · `### Next-cycle watchlist`), 예외 밖 0
- DG-04 — 페이지 마흔넷 `44/44 PASS` 종료 코드 0 · `OK` 줄 모두 `err=0`, `docs` 전체 `177/177 PASS` 종료 코드 0
- 공통 지침 검증 절 — `HEAD` 새 복제본에서 `validate-plugin.py` · `sync-docs.py --check-only` · `sync-evals.py --check-only`(`Total: 0 added, 0 orphans, 0 missing`) · `run-evals.py` 모두 종료 코드 0.
  `validate-post-kaizen.py --since 511f19b` 종료 코드 0 — PASS 12 · SKIP 셋(버전 두 줄 · 이 계약 구간에 harness 원본 변경이 없어 `docs-site-regen`), `scope-isolation` · `doc-contracts` PASS.
  훅 시험 `harness/evals/hooks/commit-guard-test.sh` · `flutter-toolkit/evals/hooks/format-edited-dart-test.sh` · `scripts/test-collect-kaizen-data.py` 종료 코드 0

## 계약 피드백 (Step 7 · 9 · 10)

- Step 7 자기진단 — 스물다섯 항목 가운데 true 는 `implementation_leakage` 하나다. 조건 측정 절에 도우미 이름 · 셸 함수 이름이 들어갔다(대상이 기록 파일이라 도우미 출력 글자를 기대값으로 적었다).
  ER-01 · ER-02 · ER-05 가 세션 스크래치 사본에 기대는 점은 `untestable_conditions` false 로 두고 사유에 적었다 — 같은 세션에서는 명령으로 판정된다
- Step 8 교차 진단 — 봉인 전 REVIEW 두 회차(`.harness/.meta/kaizen-0924/final-review.md`)를 `cross_diagnosis_notes` 에 옮겼다(`cross_diagnosis_by: qa-evaluator`)
- Step 9 저장 — `~/.harness/feedback/contract/1a3bcba6-2026-09-25T230229-de8c7935-38547.yaml` (`sprint_slug: 'kaizen-0924-final'`). 초안은 저장 도구가 지웠고 커밋하지 않았다
- Step 10 검증 — `bash harness/scripts/verify-feedback.sh <그 파일>` → `PASS` 종료 코드 0
- 개선 제안 셋 — 저장소 밖 상태를 고치기 전 사본을 오래 남는 자리에 두기 · 나눠 맡긴 페이지 재생성은 원본 소제목 비율도 재기 · 범위 밖 도구 형식 경고는 예외로 굳히지 말고 도구를 고치기(FN-78)

## 교차 진단 기록

러닝북 「교차 진단 기록」 절대로 열일곱 Phase 의 전역 피드백 서른넷을 고쳤다(판정은 뒤집지 않았다). 글은 모두 `Final 교차 진단 (xdiag-all.md P<N>)` 로 시작한다.

- 평가자 피드백 열일곱(`~/.harness/feedback/evaluator/`): `cross_diagnosis_by: pending-parent` → `sprint-contract`, `cross_diagnosis_notes` 에 「판정 유지」 와 결론 — 뒤집을 근거 유무 · 공허한 통과 · 계약 밖 결함 요지 · 그것을 고친 후속 커밋
- 계약 피드백 열일곱(`~/.harness/feedback/contract/`): `cross_diagnosis_by` 는 그대로 두고 옛 기록 뒤에 ` | ` 로 그 계약 측정의 구멍을 붙였다. 구멍이 없던 P15 · P17 은 「없음」 과 한계 메모
- 원문은 교차 진단 전문(세션 스크래치 `xdiag-all.md`)이고 필수 글자 표는 계약 GAP 분석 「교차 진단 기록 표」 다
- Phase 개정 파일: P1 에 notes 커밋 `76cfb37…` 를 상한으로 덧붙여 ER-04 셋째 · AR-04 ② 를 다시 재니 0 · 0. P7 · P8 · P9 · P11 에 kit followups 커밋 `154916a` · `cc11f71` · `c4eeef3` · `cfef54f` 전체 sha 와
  `amend_direction: unchanged` 한 줄씩(DG-02 뜻 기준 FAIL 해소)
- 두 followups 평가자 피드백은 `pending-parent` 그대로다 — 교차 진단 전문이 P1 ~ P17 뿐이다(FN-77). 2026-09-26 에 두 followups 교차 진단 결론으로 갱신했다(아래 `## 교차 진단 뒤 보강 (2026-09-26)`)

## 문서 사이트

기준 `390dea8`. 러닝북 규칙 「F2 매핑 표 원본 가운데 대응 HTML 이 있는 것」 을 계약 GAP 분석의 네 갈래로 정한 마흔넷을 원본 전체에서 다시 만들었다(한 페이지 = 한 에이전트, 부분 패치 금지).
파일 이름 · 내비 id · `--accent` 는 그대로다. 새 페이지는 없다. 페이지 판 번호는 이 파일에 글자로 옮기지 않는다 — 확인은 `docs.py` 출력 줄(`tok_new=56/56`)로 한다.

| 페이지 | 원본 | 만든 주체 | 커밋 |
| --- | --- | --- | --- |
| `docs/bambu-kit/bambu-print-profile.html` | `bambu-kit/skills/bambu-print-profile/SKILL.md` | Claude | `7379736` |
| `docs/bambu-kit/surface-recipes.html` | `bambu-kit/skills/bambu-print-profile/references/surface-recipes.md` | Codex | `bb9aebe` · `098f671`(한 문단) |
| `docs/api-kit/contract-extraction-modes.html` | `docs/api/contract/contract-extraction-modes.md` | Claude | `f29760c` |
| `docs/api-kit/snapshot-sealing-canonicalization.html` | `docs/api/contract/snapshot-sealing-canonicalization.md` | Claude | `657c011` |
| `docs/api-kit/auth-secret-lifecycle.html` | `docs/api/execution/auth-secret-lifecycle.md` | Claude | `2274d82` |
| `docs/api-kit/probe-synthesis-hurl-semantics.html` | `docs/api/execution/probe-synthesis-hurl-semantics.md` | Claude | `38f650f` |
| `docs/api-kit/regression-diff-failure-policy.html` | `docs/api/verification/regression-diff-failure-policy.md` | Claude | `77dcb48` |
| `docs/api-kit/static-evidence-viewer-contract.html` | `docs/api/verification/static-evidence-viewer-contract.md` | Claude | `8254f26` |
| `docs/backend-kit/api-design.html` | `docs/backend/fundamentals/api-design.md` | Claude | `d37c3c8` |
| `docs/backend-kit/database.html` | `docs/backend/fundamentals/database.md` | Codex | `5f5349f` |
| `docs/infra-kit/cicd.html` | `docs/infra/platform/cicd.md` | Claude | `3168679` |
| `docs/planning-kit/data-modeling.html` | `docs/planning/data-modeling.md` | Claude | `33441bd` |
| `docs/planning-kit/flows.html` | `docs/planning/flows.md` | Claude | `75b3d24` |
| `docs/planning-kit/prd-patterns.html` | `docs/planning/prd-patterns.md` | Claude | `33e17d1` |
| `docs/rust-kit/sqlx-patterns.html` | `docs/rust/data/sqlx-patterns.md` | Codex | `5cc76e5` |
| `docs/tone-kit/korean-technical-writing.html` | `docs/tone/korean-technical-writing.md` | Codex | `da28072` |
| `docs/tone-kit/overview.html` | `docs/tone/overview.md` | Codex | `b250cbf` |
| `docs/flutter-toolkit/flutter-ai-rules.html` | `flutter-toolkit/references/flutter-ai-rules.md` | Claude | `0e2188a` |
| `docs/flutter-toolkit/primitive-substitution-gate.html` | `flutter-toolkit/references/primitive-substitution-gate.md` | Claude | `1c7ed43` |
| `docs/flutter-toolkit/project-detection.html` | `flutter-toolkit/references/project-detection.md` | Codex | `4237b71` |
| `docs/flutter-toolkit/visual-evidence-protocol.html` | `flutter-toolkit/references/visual-evidence-protocol.md` | Claude | `3006e2d` |
| `docs/harness/agent-design-guide.html` | `harness/docs/guides/agent-design-guide.md` | Claude | `cbc7e87` |
| `docs/harness/contract-design-guide.html` | `harness/docs/guides/contract-design-guide.md` | Claude | `af93eab` |
| `docs/harness/qa-evaluation-guide.html` | `harness/docs/guides/qa-evaluation-guide.md` | Claude | `ad7ab52` |
| `docs/harness/skill-design-guide.html` | `harness/docs/guides/skill-design-guide.md` | Claude | `58c821b` |
| `docs/harness/contract-schema.html` | `harness/references/contract-schema.md` | Claude | `6877d97` |
| `docs/onboarding-kit/setup-guide.html` | `onboarding-kit/skills/setup-guide/SKILL.md` | Codex | `d1e6392` |
| `docs/onboarding-kit/format-checklist.html` | `onboarding-kit/skills/setup-guide/references/format-checklist.md` | Claude | `e0a5623` |
| `docs/onboarding-kit/project-detection.html` | `onboarding-kit/skills/setup-guide/references/project-detection.md` | Claude | `f58ca23` |
| `docs/react-kit/render-evidence-protocol.html` | `react-kit/references/render-evidence-protocol.md` | Codex | `f23e46e` |
| `docs/harness/plugin-validation.html` | `harness/docs/guides/plugin-validation-guide.md` | Claude | `8a7df32` |
| `docs/react-kit/quality.html` | `docs/react/kit-design/g4-quality.md` | Claude | `44b4367` |
| `docs/onboarding-kit/fcm-ios-example.html` | `docs/onboarding-kit/examples/fcm-ios-setup-guide.md` | Codex | `22eb365` |
| `docs/backend-kit/backend-test.html` | `backend-kit/skills/backend-test/SKILL.md` | Codex | `70db598` |
| `docs/design-kit/visual-change-protocol.html` | `design-kit/references/visual-change-protocol.md` | Claude | `176d9e4` |
| `docs/design-kit/design-component.html` | `design-kit/skills/design-component/SKILL.md` | Claude | `8b5dbfb` |
| `docs/design-kit/design-concept.html` | `design-kit/skills/design-concept/SKILL.md` | Codex | `0d53316` |
| `docs/design-kit/design-mockup.html` | `design-kit/skills/design-mockup/SKILL.md` | Codex | `c6303e5` |
| `docs/design-kit/design-test.html` | `design-kit/skills/design-test/SKILL.md` | Codex | `150a80a` |
| `docs/infra-kit/gate-result-taxonomy.html` | `infra-kit/references/gate-result-taxonomy.md` | Claude | `6afed82` |
| `docs/infra-kit/infra-test.html` | `infra-kit/skills/infra-test/SKILL.md` | Codex | `6c0457b` |
| `docs/reflect-kit/design.html` | `reflect-kit/docs/DESIGN.md` | Codex | `223c629` |
| `docs/reflect-kit/schema.html` | `reflect-kit/docs/SCHEMA.md` | Codex | `ca36dd3` |
| `docs/howto-kit/overview.html` | `howto-kit/README.md` | Claude | `f7d1788` |

- Claude 28 쪽 · Codex 16 쪽. Codex 는 사용 한도로 도중에 멈췄고 나머지 19 쪽을 Claude 가 넘겨받았다(Codex 결과 표는 세션 스크래치 `kaizen/codex-pages/results.tsv`)
- Codex 가 만든 `docs/bambu-kit/surface-recipes.html` 이 원본 「잰 방법 (2026-09-25 추가)」 문단을 줄이며 블록 이름을 빠뜨려 AR-03 새 글자 하나가 비었다 — 그 문단만 원본 문장대로 고쳤다(`098f671`, 개정 파일에 적음)
- 첫 화면 `docs/index.html`: harness 다섯 항목(`skill-design` · `agent-design` · `contract-design` · `qa-evaluation` · `contract-schema`) 제목의 판 번호만 원본 판 번호로 고쳤다(`55d8a36`, 다섯 줄).
  다른 서른아홉 페이지는 id · 파일 이름이 그대로라 등록을 바꿀 것이 없다 — Codex 가 만든 16 쪽도 `check-docs-links.py` 가 내비 176 · 등록 176 · 고아 · 유령 · 아이콘 누락 없음으로 확인했다
- 대응 페이지가 없어 만들지 않은 원본 열아홉(`detect-docs-drift.py --since 390dea8` 가 `[NEW]` 로 낸 스물 가운데 `g4-quality.md` 를 뺀 것):
  `bambu-kit/skills/bambu-print-profile/references/comment-analysis.md` ·
  `docs/api/research-log.md` · `docs/backend/research-log.md` · `docs/flutter/research-log.md` · `docs/infra/research-log.md` · `docs/planning/research-log.md` · `docs/react/research-log.md` · `docs/rust/research-log.md` · `docs/tone/research-log.md` ·
  `flutter-toolkit/references/figma-parity-self-verify.md` · `react-kit/references/common-gotchas.md` · `reflect-kit/skills/reflect-digest/SKILL.md` · `reflect-kit/skills/reflect-kaizen/SKILL.md` ·
  `rust-kit/references/project-detection.md` · `tone-kit/references/core-antipatterns.md` · `tone-kit/references/core-comment.md` · `tone-kit/references/core-naming.md` ·
  `tone-kit/references/locale-korean.md` · `tone-kit/references/sources.md`
- 페이지 에이전트가 넘긴 원본 결함(고치지 않음 — 원본은 이 계약 범위 밖): `harness/docs/guides/qa-evaluation-guide.md` 미검증 규약 「5 조항」 번호가 1 · 2 · 3 · 3 · 4 · 5,
  `flutter-toolkit/references/visual-evidence-protocol.md` Step 3 「4 검사」 가 평가 가이드의 5 검사와 어긋남, `docs/planning/data-modeling.md` 판이 올랐는데 계약 `TOKENS` 판 번호 열넷에 없었음(페이지는 새 판을 담았다)

## 넘기는 것

- Final QA — 이 계약의 `harness:qa-evaluator` 판정. 이 계약 자신의 `status: done` 과 QA 리포트 커밋은 QA 뒤 일이다
- PR · 푸시(오케스트레이터 F4 7 번) — Final QA 뒤 부모가 사용자 규칙(푸시는 사용자가 요청할 때만)대로 한다(FN-39)
- 버전 — 카이젠 PR 을 합친 뒤 `main` 에서 `.harness/.meta/kaizen-0924/release-plan.md` 의 `release.sh` 열네 줄. 배포 뒤 reflect-kit 설치본 Stop 훅 확인 한 줄
- 메모리 승격 — `.harness/.meta/memory-promotion-candidates-2026-09-24.md` 후보 넷. `/reflect-promote` 호출을 사용자에게 제안한다(후보 파일은 승격 완료가 아니다)
- 두 followups 교차 진단 — 부모가 돌리면 두 평가자 피드백의 `pending-parent` 를 그때 갱신(FN-77). 2026-09-26 에 갱신을 마쳤다

## 다음 사이클 메모

입력 표에서 처리 칸이 `고치지 않음` 인 열하나와 두 followups 가 고치지 않은 것의 자리. 감사 기록 2026-09-25 항목에도 같은 목록이 있다.

| ID | 항목 | 사유 · 받을 곳 |
| --- | --- | --- |
| FN-18 | `run-evals.py` 가 `assertions.json` 을 읽지 않음 · 실행기 없음 | 새 도구 — 다음 사이클 Phase 3 · 4 (F1H-14 · F1H-84) |
| FN-39 | PR 생성 | 이 계약 밖. Final QA 뒤 부모가 사용자 규칙대로 |
| FN-43 | `ci.yml` 실행기 줄 | 실행기가 없다(F1H-14) |
| FN-56 | 설계 문서 `docs/superpowers/specs/2026-09-02-api-kit-design.md:249` | 세 Final 계약 어느 범위에도 없다 — 다음 사이클 Phase 16 (F1H-67 · F1K-56) |
| FN-58 | Phase notes 열일곱의 다음 사이클 메모 | Phase 가 다음 사이클로 보낸 것. 감사 기록이 notes 경로 열일곱을 가리킨다 |
| FN-64 | `scripts/check-stale-values.py` 의 `EXCLUDED_KITS` 에서 backend-kit 해제 | 예외 셋은 이번에 등록부에 넣었다. 해제는 `scripts/` 라 다음 사이클 (F1H-79) |
| FN-76 | `check-insights-tracking.py` 가 슬러그 형식만 봄 | `scripts/` 범위 밖 — 번호 ↔ 슬러그 대응을 검사기에 넣는다 |
| FN-77 | 두 followups 평가자 피드백 `pending-parent` | 교차 진단 전문이 P1 ~ P17 뿐 — 부모가 두 followups 교차 진단을 돌리면 그때. 2026-09-26 에 끝냈다(다음 사이클로 넘기지 않는다) |
| FN-78 | `append-audit-log.py` 고정 소제목 MD024 · 끝 빈 줄 없음 | `scripts/` 범위 밖 — 소제목에 날짜를 붙이고 앞에 빈 줄을 넣는다 |
| FN-79 | css-tokens 매핑 표에 howto-kit accent 없음 | `.claude/skills/docs-site/` 범위 밖 — F1H-91 과 함께 |
| FN-80 | `docs/process/kaizen-flow.html` 이 9-Phase | 원본이 「내부 문서」 뿐 — 다음 사이클 docs-site 매핑 결정과 함께 |

두 followups 가 고치지 않은 것은 원래 notes 에 있다 — `.harness/.meta/kaizen-0924/f1-harness-followups-notes.md` §다음 사이클 메모(F1H 스물아홉 · 구현 중 찾은 넷) ·
`.harness/.meta/kaizen-0924/f1-kit-followups-notes.md` §고치지 않은 항목과 이유 · §다음 사이클 메모(서른셋). 이번 사이클 메타 이슈 여덟은 감사 기록 `### 이번 사이클 메타 이슈 (2026-09-24 사이클)` 에 있다.

Final 교차 진단(2026-09-25)이 더 짚은 것 가운데 고치지 않은 넷 — 판정에는 영향이 없다.

- 계약 밖 결함 2 — `.harness/.meta/orchestrator-audit-log.md:517` 의 도구 생성 줄 「Next-cycle watchlist — 특별 감시 대상 없음」 이 같은 항목 아래쪽의 감시 거리
  (`:548` `F1H-82` — CI 에 넣은 러너의 첫 우분투 실행, PR 뒤 첫 확인 항목)와 어긋난다. 원인은 `scripts/append-audit-log.py:171-178` 이 사후 점검 실패 목록으로만 감시 목록을 만드는 것이다.
  감사 기록은 덧붙이기만 하고(AR-07 `append_only`) 스크립트는 `scripts/` 라 이 계약 범위 밖이다 — 다음 사이클에 수동 입력의 감시 거리도 받게 고친다(FN-78 과 같은 도구)
- 측정 구멍 1 — AR-03 의 `docs.py` 는 새 글자 · 옛 글자 · 줄 수만 봐서 페이지 본문이 빠져도 통과한다(교차 진단이 본문 700 줄을 지운 사본에서도 끝줄이 같음을 확인).
  이번에는 담김 검사(스크래치 `kaizen/coverage.py`)로 열네 쪽을 채웠다. 다음 사이클 문서 사이트 계약은 옛 페이지 대비 원본 코드 표시 · 낱말 비율을 조건으로 잰다
- 측정 구멍 2 — AR-03 이 판 번호를 재는 페이지는 열넷인데, 사이클 동안 머리 설정 `version` 이 바뀐 원본은 스물하나다. 빠진 일곱
  (`api-design` · `cicd` · `data-modeling` · `flows` · `prd-patterns` · `sqlx-patterns` · `visual-evidence-protocol`)도 새 판 번호가 있고 옛 판 번호는 0 이다(교차 진단 직접 확인).
  다음 사이클에는 판 번호 목록을 손으로 적지 말고 원본 머리 설정에서 뽑는다
- 측정 구멍 3 — SK-01 (d) 의 `tonegrade.py` 가 강도 칸에 글이 덧붙은 줄(예: `tone-kit/references/adapter-dart-flutter.md:40` D-04) 등을 못 읽어
  교차 진단 셈으로 규칙 79 개 가운데 63 개만 센다. 바뀐 표 줄을 직접 대조해 강도가 바뀐 줄은 0 이었다. 다음 사이클 tone-kit 정합 검사는 강도 칸의 앞머리만 보고 판정한다

## 교차 진단 뒤 보강 (2026-09-26)

QA 1 회차(`APPROVE` 26/26) 뒤 부모 세션의 교차 진단(2026-09-25)은 판정을 유지하면서 페이지 내용 빠짐 · 측정 구멍 셋 · 계약 밖 결함 둘을 짚었다.
조건은 바꾸지 않았다 — 개정 파일 `## 교차 진단 뒤 보강 — 조건 변경 없음 (direction: unchanged)` 절에 이유 · 페이지 · 담김 검사 전후 값 표를 적었다.

| 커밋 | 내용 |
| --- | --- |
| `8e2b8e7` ~ `a38de63` (열넷) | 원본을 옛 페이지보다 덜 담은 페이지 열넷 보강 — 한 쪽 한 커밋 (Claude 에이전트) |
| `849940e` | 이 계약 `status: done` 과 QA 1 회차 리포트 |
| `a784aef` | `.harness/.meta/evals-audit-2026-09-24.md` 의 bambu-kit CI 문장을 사실대로 (계약 밖 결함 1) |
| `65ea663` | 개정 파일 「교차 진단 뒤 보강」 절 |
| `8d914c5` | 개정 파일 `end_sha` (`65ea663`) |
| 이 절을 넣은 커밋 | notes — 이 절 · 다음 사이클 메모 넷 · FN-77 끝남 표시 |
| 그다음 커밋 | 개정 파일에 그 커밋 sha 로 `end_sha` 한 줄 더 |

담김 검사 — 봉인 커밋 `509d295` 판 옛 페이지와 맞대 원본 코드 표시가 빠진 수(`lost`)와 원본 낱말 비율(`wr=옛->새`)을 쟀다(스크래치 `kaizen/coverage.py` 와 같은 식).
열네 쪽 모두 `lost=0` 이고 새 비율이 옛 비율 이상이다. 끝 판 페이지 마흔넷 전부를 다시 재도 `lost` 가 1 이상이거나 새 비율이 낮은 쪽은 0 이다. 쪽마다 값은 개정 파일 표에 있다.

저장소 밖(커밋 없음) — 평가자 피드백 셋의 `cross_diagnosis_by: pending-parent` 를 `sprint-contract` 로, `cross_diagnosis_notes` 를 교차 진단 결론(판정 유지 · 공허한 통과 · 계약 밖 결함)으로 바꿨다.
고치기 전 사본은 스크래치 `kaizen/fix2/fb-before/` 이고 두 칸 말고 달라진 것은 0, 셋 모두 `verify-feedback.sh` `PASS` 다. FN-77 은 이것으로 끝났다.

- `~/.harness/feedback/evaluator/5a24cc99-2026-09-25T172451-de8c7935-85973.yaml` — `kaizen-0924-f1-harness-followups` (원문 스크래치 `kaizen/final-xdiag-followups.md`)
- `~/.harness/feedback/evaluator/5a24cc99-2026-09-25T180346-de8c7935-52654.yaml` — `kaizen-0924-f1-kit-followups` (같은 원문)
- `~/.harness/feedback/evaluator/1a3bcba6-2026-09-25T232231-de8c7935-24681.yaml` — `kaizen-0924-final` QA 1 회차 (이번 교차 진단 요지)

재측정 — 도우미 스물여섯을 계약에서 새로 떼어(BUILD 판과 파일 내용이 같다) 공통 정의가 개정 파일 마지막 `end_sha:` 인 `65ea663` 을 `END` 로 읽은 bash 에서 돌렸다.
조건 스물여섯이 모두 기대값과 같다. 앞 절과 값이 달라진 것은 AR-09 `my` 하나다(이 계약 QA 리포트 한 파일이 늘었다).

- AR-03 — `pairs=44 exist=44 changed=44 short=0 accent=0 ext=0 hidden_up=0 tok_new=56/56 tok_old=0/9 html_added=0 html_removed=0` · `nav_ver=5/5` · `title_ver=5/5` ·
  서명 커밋 HTML 44 · 첫 화면 1 · 첫 화면 numstat `5 5` · api-kit 문서 `12/12 PASS` · 내비 등록 176 · 176 · 대비 수치 종료 코드 0
- DG-04 — 페이지 마흔넷 `44/44 PASS`(`OK` 줄 모두 `err=0`) · `docs` 전체 `177/177 PASS`, 둘 다 종료 코드 0
- DG-05 — 새 복제본에서 `rc=[000000000000000000000] vpk_rc=0 vpk_pass=13 vpk_bad=0 vpk_skip=[marketplace-sync plugin-json-bumps]`
- DG-02 — `new_total=3`, `NEW` 셋이 모두 감사 기록의 도구 고정 소제목 MD024. 개정 파일 · evals 점검 기록에 새 경고 0
- AR-05 — evals 점검 기록을 고친 뒤에도 `state=1 phases=17 keys_ok=1 zero=1 last_updated=1 evals=[total_line=1 paths=10/10 adr_cmd=1]`
- AR-01 — `done=19 status_only=19 seal_ok=19 fb_tracked=19 fb_new=19 dirty=0`. AR-09 — `my=108 outside=0 html_extra=0 forbidden=0 unsigned=0 broken=0 self=SEAL_OK seal_files=1`
- SK-01 여덟 줄은 위 `## F1 정합` 과 글자까지 같다. SK-02 · SC-01 · ER-01 ~ ER-05 · AR-02 · AR-04 · AR-06 · AR-07 · AP-01 · AP-03 · RE-01 · RE-02 · DG-01 · DG-03 도
  `## 조건별 결과 (BUILD 예행)` · `## 끝 판 재측정` 값과 같다
- AR-08 — `heads=6/6 lines=8/8 nohtml=19/19 memo=13/13`. notes 마지막 커밋이 `END` 인지는 이 notes 커밋 뒤 `end_sha` 를 덧붙이고 다시 잰다
- 공통 지침 검증 절 — `65ea663` 새 복제본에서 `validate-post-kaizen.py --since 511f19b` 종료 코드 0(PASS 12 · SKIP 셋 — 버전 두 줄 · `docs-site-regen`),
  `validate-plugin.py` · `sync-docs.py --check-only` · `sync-evals.py --check-only`(`Total: 0 added, 0 orphans, 0 missing`) · `run-evals.py`(`Total: 115 passed, 0 failed`) 종료 코드 0.
  훅 시험 · CI 시험 열하나는 DG-05 안에서 모두 종료 코드 0

## 교차 진단 2 회차 뒤 보강 (2026-09-26)

- 커밋: QA 2 회차 리포트 `bc6302c` · sqlx-patterns `a0a395e` · backend-test `10d42ee` · 개정 `fc2f6e8`
- 다음 사이클 메모 — 담김 잣대 `coverage.py` 는 원본 코드 블록 안을 재지 않는다. 코드 블록 줄 대조(`fence2.py` 꼴)를 합쳐야 한다
- 다음 사이클 메모 — 옛 판보다는 늘었지만 원본 전체 기준으로 아직 낮은 쪽: `docs/onboarding-kit/setup-guide.html`(코드 블록 61 줄 중 1, `guide_gate` 함수 블록 없음) · `docs/design-kit/design-concept.html`(52 줄 중 3) · `docs/design-kit/design-mockup.html`(20 줄 중 15)
