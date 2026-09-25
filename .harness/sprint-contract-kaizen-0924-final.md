---
feature: "카이젠 2026-09-24 Final — 오케스트레이터 F1 ~ F4 (교차 Phase 정합 · 처리 배정표 닫기 · 문서 사이트 재생성 · 피드백 정리 · 메모리 후보 · changelog · 연구 기록 · evals 점검 · 실패 횟수 · 감사 기록 · Phase 계약 상태 커밋 · 교차 진단 기록 · 릴리스 계획)"
slug: kaizen-0924-final
created: "2026-09-25 19:11"
complexity: "복잡"
conditions: 26
status: done
owner_session: de8c7935-a5b6-4df5-9106-fafa73c288a0
conditions_digest: sha256:81b9a7409e53588b
locked_at: "2026-09-25 20:43"
---

## 배경

카이젠 2026-09-24 사이클은 Phase 1 ~ 17 과 Final 후속 계약 둘(`kaizen-0924-f1-harness-followups` · `kaizen-0924-f1-kit-followups`)이
모두 QA 승인으로 끝났다(열아홉 QA 리포트 `Verdict: APPROVE` · `Iteration: 1`). 이 계약은 Final 계약 셋 가운데 마지막이다 —
오케스트레이터 Step F1 ~ F4 를 닫는다. 코드 · 킷 파일은 고치지 않는다. 기록 · 문서 사이트 · 상태 파일만 고친다.

읽은 입력은 Final 지침(`scratchpad/kaizen/final-runbook.md`)의 「먼저 읽을 것」 다섯과 두 followups notes 다 — 공통 지침(`phase-runbook.md`),
오케스트레이터 `.claude/skills/kaizen-orchestrator/SKILL.md` Step F1 ~ F4(`:576-793`), Final 처리 목록(`final-todo.md`), 교차 진단 전문(`xdiag-all.md` P1 ~ P17),
Phase notes 열일곱의 「넘기는 것」 · 「미반영 키와 사유」 · 「다음 사이클 메모」, 그리고 `f1-harness-followups-notes.md` · `f1-kit-followups-notes.md` 의
「넘기는 것」 · 「다음 사이클 메모」 · 「고치지 않은 항목」. 입력 항목 전부의 처리는 `범위 경계` 절 입력 표에 있다.

할 일은 넷으로 나뉜다.

- **닫기** — Phase 계약 열아홉의 `status: done` 과 QA 리포트 열아홉을 커밋한다. 처리 배정표 Phase 행 일흔넷에 계약 슬러그 · QA 판정을 채운다.
  평가자 피드백 열일곱의 `cross_diagnosis_by: pending-parent` 를 교차 진단 결론으로 바꾸고, 계약 피드백 열일곱에 교차 진단이 찾은 측정 구멍을 붙인다.
  Phase 1 개정 파일에 notes 커밋을 상한으로 덧붙이고, Phase 7 · 8 · 9 · 11 개정 파일에 「교차 진단 뒤 Final 에서 고침」 줄을 단다
- **문서 사이트 (F2)** — 사이클 동안 바뀐 원본의 페이지 마흔넷을 원본 전체로 다시 만든다. 새 페이지는 만들지 않는다.
  첫 화면 `docs/index.html` 은 harness 다섯 항목 제목의 판 번호만 원본 판 번호로 고친다
- **기록 (F3 · F3.5 · F4)** — 피드백 정리, 메모리 승격 후보, changelog · 연구 기록, evals 점검, 실패 횟수, 사이클 상태, 감사 기록, 옛 값 등록부, 릴리스 계획
- **정합 확인 (F1)** — Phase 1 가이드 변경의 반영, Phase 2 ↔ 3 판 번호, tone-kit 강도 · 트리거, api-kit 확정 결정, 사이클 전체 문법 검사를 재어 notes 에 남긴다.
  루트 `CLAUDE.md` 의 카이젠 설명 세 줄이 Phase 17 까지를 적게 고친다

편집 전 실측에서 입력에 없던 결함 넷을 더 찾았다.

- `.harness/.meta/kaizen-state.yaml:8` 이 아직 `cycle_id: "kaizen-2026-08-13"` 이다. 사후 점검 `scripts/validate-post-kaizen.py:197` 이 이 값에서 날짜를 뽑아
  changelog · 연구 기록 · 정리 기록 · 실패 횟수 · evals 점검 다섯 검사를 **옛 사이클 항목으로 통과**시킨다 — 이번 사이클 항목이 하나도 없는 지금도
  `12 PASS` 다. 사본에서 `cycle_id` 만 `kaizen-2026-09-24` 로 바꾸면 그 다섯이 FAIL 로 떨어진다(봉인 전 실측). 이번 사이클은 워크플로가 Phase 를 돌려
  `scripts/spawn-kaizen-phase.sh` 가 이 파일을 갱신하지 않았다
- 전역 피드백이 639 개로 F3 의 500 개 상한을 넘었다(`find ~/.harness/feedback -type f | wc -l`). 가장 오래된 139 개가 2026-04-04 ~ 2026-04-17 판이다
- `scripts/check-insights-tracking.py:21` 은 대상 계약 칸의 슬러그 **형식**만 본다 — Phase 6 행에 Phase 5 슬러그를 적어도 `TRACKING_TABLE_OK` 가 나온다(사본 실측).
  그래서 AR-02 는 번호 ↔ 슬러그 대응을 따로 잰다
- `scripts/append-audit-log.py:148` · `:159` · `:171` 이 매번 같은 소제목 셋을 찍는다. 감사 기록에 이미 한 벌(`:220` · `:224` · `:228`)이 있어 이번 항목이 같은 제목 경고
  (MD024) 셋을 새로 낸다. 스크립트는 이 계약 범위 밖이라 DG-02 에 그 세 줄만 예외로 적고 다음 사이클 메모로 넘긴다

## 리서치 소스

- 이 계약은 새 외부 조회를 하지 않는다. 외부 사실은 사이클이 이미 모은 근거 파일(`.harness/.meta/evidence/phase*.md`)과 Phase · followups notes 에서만 옮긴다.
  changelog · 연구 기록에 새로 적는 URL 은 그 파일들에 있어야 한다(AR-04 `url_out=0`)
- 저장소 안 근거
  - `.claude/skills/kaizen-orchestrator/SKILL.md:576-793` — Step F1 ~ F4 와 Post-Kaizen Checklist
  - `.claude/skills/docs-site/SKILL.md:14-40` — 페이지 원칙(외부 리소스 금지 · 400 줄 · 출처 링크 · 가로 넘침 네 규칙 · 대비 토큰)
  - `.claude/skills/docs-site/references/css-tokens.md:25-41` — 킷별 accent
  - `reflect-kit/references/memory-grounding.md` — 메모리 후보의 `grounding` 네 값
  - `reflect-kit/skills/reflect-promote/SKILL.md:44` — 카이젠 후보 파일을 받는 쪽
  - `scripts/detect-docs-drift.py:33-77` — 원본 → 페이지 매핑(harness followups AR-01 뒤 판)
  - `harness/references/feedback-schema.yaml:46-55` — `cross_diagnosis_by` 네 값과 뜻
  - `scratchpad/kaizen/xdiag-all.md` — Phase 교차 진단 전문(교차 진단 기록의 원문)

## GAP 분석 · 개선안 초안

### 1.1 복잡도 4 축

| 축 | 물음 | 값 |
| -- | ---- | -- |
| 레이어 수 | 몇 개 계층을 관통하는가 | 넷 — `.harness/` 상태 · 기록, 처리 배정표, 공개 문서 사이트 HTML, 저장소 밖 전역 피드백 |
| 공개 API·계약 변경 | 외부에 노출된 형태가 바뀌는가 | 예 — 사이클 상태 값(사후 점검이 읽음), 처리 배정표 칸, 전역 피드백 두 칸, 문서 사이트 페이지 |
| 소비면 존재 | 반대편이 있는가 | 예 — 사후 점검 · 감사 기록 도구 · 다음 사이클 수집기 · `/reflect-promote` · `check-insights-tracking.py` · CI 문서 검사 |
| 회귀 위험 | 기존 동작이 깨질 수 있는가 | 예 — 전역 피드백을 옮기면 다음 사이클 데이터 풀이 줄고, 페이지 마흔넷을 다시 만들면 대비 · 넘침 · 내비 등록이 깨질 수 있다 |

넷 다 예라 **복잡**이다. 기능 조건 18 개 — Step 6.2 두 번째 명령으로 센 값(DG-05 포함). 상한 20 안에 두려고 성격이 같은 일을 한 조건에 묶었다
(F1 정합 여섯 가지는 SK-01 하나, 사이클 상태 · 실패 횟수 · evals 점검은 AR-05 하나).

### 1.2 설정 리터럴 대조표

| config key | project.yaml 에서 읽은 값 | 계약에 쓴 값 |
| ---------- | ------------------------- | ------------ |
| `commands.analyze` | `bash -n scripts/release.sh` | DG-01 N/A 사유에 그대로 |
| `commands.test` | `bash scripts/release.sh 2>&1 \|\| true` | DG-03 N/A 사유에 그대로 |
| `diagnostics.ide_exclude` | `[]` | DG-02 에 그대로 |
| `contract_categories[].id` / `prefix` | `Skill`/`SK` · `Script`/`SC` · `Error`/`ER` · `Architecture`/`AR` | 조건 절 네 개 |
| `anti_patterns[].id` / `message` | `AP-01` 버전 하드코딩 · `AP-02` force push · `AP-03` bare code fence · `AP-04` frontmatter name | AP-01 · AP-03 (AP-02 는 푸시를 하지 않고, AP-04 는 이 계약이 SKILL.md · 에이전트를 고치지 않아 뺐다) |

### 1.4 편집 전 감사 (시작 커밋 `511f19b` 판을 실제로 읽은 줄)

| 대상 | 읽은 줄 | 기존 결함 · 상태 | 조건 |
| ---- | ------- | ---------------- | ---- |
| Phase · followups 계약 열아홉 | 작업 폴더 `git diff -- .harness/` — 열아홉 파일 각 `-status: active` `+status: done` 한 줄 | 커밋 안 됨. QA 리포트 열아홉은 추적 안 됨(`??`) | AR-01 |
| `~/.harness/feedback/evaluator/*.yaml` | Phase 열일곱 파일 `diagnosis.cross_diagnosis_by: pending-parent` · notes 「부모 세션이 … 교차 진단해야 한다」 | 교차 진단 결론이 기록 안 됨 (`fbx.py` 시작 판 `by=0 marker=0`) | ER-01 |
| `~/.harness/feedback/contract/*.yaml` | Phase 열일곱 파일 `cross_diagnosis_by: qa-evaluator` · 봉인 전 검토 기록 | 교차 진단이 찾은 측정 구멍이 없다 | ER-02 |
| `.harness/sprint-amendments-kaizen-0924-p01-guides.md:17` | `end_sha:` 한 줄(`18b8ff0`) | notes 커밋 `76cfb37` 이 범위 밖(`amend.sh` `after_other=1`) | ER-03 |
| 같은 파일 P7 `:23-24` · P8 · P9 · P11 | `end_sha:` 두 줄 | DG-02 뜻 기준 FAIL 을 고친 커밋이 적혀 있지 않다 | ER-03 |
| `.harness/stale-values.yaml:12-19` | OpenAPI `old: "3.1.1"` 항목 · allow 둘 | 새 옛 값 셋이 등록 안 됨(사본 세 곳에 넣어도 `rc=0`) · backend-kit 세 줄이 allow 밖 | ER-04 |
| `.harness/.meta/cleanup-log.yaml:62-68` | 마지막 항목 2026-08-13 | 이번 사이클 항목 없음 · 피드백 639 개 | ER-05 |
| `.claude/kaizen-input/insights-report.md:56-153` | 처리 배정표 96 행 · Phase 행 74 개의 대상 계약 · QA 칸이 비었다 | `check-insights-tracking.py --final` 종료 코드 1 · `Phase 행 미완료 74` | AR-02 |
| `docs/**/*.html` 마흔넷 | 아래 페이지 표의 페이지 · `docs.py` 시작 판 `changed=0 short=7 tok_new=0/56 tok_old=9/9` | 원본보다 옛 판. 일곱 쪽이 400 줄 미만 · api-kit 둘이 원본 출처 URL 을 빠뜨림(`check-api-kit-docs.py` `10/12 PASS`) · 열넷이 원본 머리 설정의 옛 판 번호를 제목 · 뱃지에 보인다 | AR-03 · DG-04 |
| `docs/index.html:234-238` | harness 다섯 항목 제목 `v1.5.0` · `v1.6.0` · `v5.0` · `v5.0` · `v5.3` | 원본 판 번호(`1.6.0` · `1.7.0` · `v5.1` · `v5.1` · `v5.5`)보다 옛 판 (`navver.py` 시작 판 `nav_ver=0/5`) | AR-03 |
| `docs/kaizen/changelog.md:1-7` · `research-log.md:9` · `flutter-changelog.md:9` · `flutter-research-log.md:9` · `docs/design/research-log.md:360` | 마지막 항목 2026-09-21 · 2026-08-13 | 이번 사이클 항목 없음 | AR-04 |
| `.harness/.meta/kaizen-state.yaml:8-9` · `kaizen-failure-count.yaml:4` · `:19` | `cycle_id: "kaizen-2026-08-13"` · `last_updated: "2026-08-13"` · `phase_14` 까지 | 사후 점검 날짜 검사가 옛 항목으로 통과 · `phase_15` ~ `phase_17` 없음 | AR-05 |
| `.harness/.meta/` | `evals-audit-2026-08-13.md` 까지 · `memory-promotion-candidates-*` 0 개 | 이번 사이클 점검 기록 · 후보 파일 없음 | AR-05 · AR-06 |
| `.harness/.meta/orchestrator-audit-log.md:368` | 마지막 항목 2026-08-13 사이클 개시, 499 줄 | 이번 사이클 항목 없음 · 도구 고정 소제목 셋이 `:220` · `:224` · `:228` 에 이미 있음 | AR-07 · DG-02 |
| `CLAUDE.md:47` · `:101` · `:310` | 「전체 10 Phase」 두 줄 · 「→ … → tone-kaizen (Phase 15)」 한 줄 | Phase 17 까지를 적지 않는다 | SK-02 |
| `scripts/validate-post-kaizen.py:163-205` · `:377-406` | 사이클 날짜를 `kaizen-state.yaml` 에서 뽑음 · `docs-site-regen` 은 harness 원본만 봄 | 위 첫 결함 · 작업 폴더에서 `docs-site-regen` FAIL(시작 판) | AR-05 · DG-05 |
| `scripts/append-audit-log.py:97-106` · `:148-182` | 끝에 빈 줄 없이 붙인다 · 고정 소제목 셋 | 앞 항목 끝 목록에 MD032, 새 머리에 MD022 · 소제목 셋 MD024 | AR-07 · DG-02 |
| `.claude/skills/docs-site/references/css-tokens.md:25-41` | 킷별 accent 표 | howto-kit 행이 없다(페이지는 `#F59E0B`) | 고치지 않음 FN-79 |
| `docs/process/kaizen-flow.html` | 「9-Phase 카이젠 사이클」 | 오래전부터 낡음. 원본이 F2 표에 「내부 문서」 뿐 | 고치지 않음 FN-80 |

### Counterpart — 바뀌는 형태를 받아 쓰는 반대편

| 바뀌는 것 (만드는 쪽) | 받아 쓰는 쪽 | 다루는 곳 |
| --------------------- | ------------ | --------- |
| `kaizen-state.yaml` `cycle_id` | `validate-post-kaizen.py` 날짜 검사 다섯 · `append-audit-log.py` 사이클 이름 · `spawn-kaizen-phase.sh` | AR-05 · DG-05 (사후 점검이 새 날짜로 PASS) · AR-07 (도구 머리 줄의 사이클 이름) |
| 처리 배정표 대상 계약 · QA · 비고 칸 | `check-insights-tracking.py --final` · 다음 사이클 수집기 §0 | AR-02 (검사기 종료 코드 0 + 번호 ↔ 슬러그 대응) |
| 전역 피드백 두 칸 · 보관 폴더로 옮긴 139 개 | `verify-feedback.sh` · `scripts/collect-kaizen-data.py` §1 · `aggregation-test.sh` | ER-01 · ER-02 (`verify-feedback.sh` PASS) · ER-05 (피드백 경로만 읽는 수집기는 보관 폴더를 읽지 않는다 — `grep -rn feedback-archive` 0 줄) |
| 옛 값 등록부 | `check-stale-values.py` · CI `Stale value check` | ER-04 · DG-05 |
| 메모리 후보 파일 | `/reflect-promote` §A (`reflect-promote/SKILL.md:44`) | AR-06 — 받는 쪽이 읽는 네 축 · `source_evidence` 형식만 쓴다 |
| 페이지 마흔넷 | `docs/index.html` 내비 · CI `check-docs-a11y.js` · `check-contrast-claims.py` · `check-docs-links.py` | AR-03 · DG-04 (페이지 id · 파일 이름을 그대로 두고, 내비는 harness 다섯 제목의 판 번호만 고친다 — `navver.py`) |
| 릴리스 계획 | 사람이 돌리는 `scripts/release.sh <킷> <단계>` | SC-01 — 줄 꼴을 `release.sh` 인자 그대로 |

### 조건 작성 자문 (contract-schema §조건 작성 preflight 의 열 태그)

- `측정-수단-부재` · `측정-방식-불일치` — 모든 기능 조건에 도우미 명령과 기대 출력을 적었다. 시작 판 값과 양성 대조는 `회귀 게이트` 절 봉인 전 실측 표에 있다
- `측정-환경-오염` · `측정-상태-모호` — 저장소 파일은 공통 정의가 푸는 두 판(`$T/B` · `$T/E`)에서 잰다. 저장소 밖 전역 피드백 · 보관 폴더 · 정리 직전 목록은
  BUILD 가 만드는 사본(`$FBK`)과 목록(`$FBLIST`)을 전제로 잰다 — 전제를 조건 안에 적었다. 사후 점검 · CI 시험은 `$END` 를 새로 복제한 폴더에서 돈다(`dg05.sh`)
- `측정-산출물-부재` — 읽을 대상(두 판 · 사본 · 목록 · notes)은 공통 정의나 이 계약 BUILD 가 만든다. 없으면 도우미가 `MISSING` · `UNREADABLE` · 종료 코드 2 로 멈춘다
- `검증경로-미기재` — 외부 도구는 `markdownlint-cli2` · `actionlint` · `dash` · `node`(playwright-core) · PyYAML 다섯이다. 준비 단계 실측을 `회귀 게이트` 절에 적었다
- `측정-중복` — 페이지 내용(AR-03)과 브라우저 렌더(DG-04)는 대상이 다르다. 저장소 검사 묶음(DG-05)은 사이클 전체 회귀를 본다
- `태그-산출물-불일치` — notes · 릴리스 계획 · 메모리 후보 · evals 점검 기록은 이 계약이 새로 만드는 산출물이다
- `범위-미명시` · `증거-경로-부재` — 페이지 마흔넷 · 전역 피드백 서른넷 · 개정 파일 다섯을 표와 도우미 목록으로 열거했다

### 개선안 초안 (BUILD 가 따를 차례)

BUILD 는 봉인(6.6) · 봉인 커밋(계약 파일 하나) 뒤 아래 차례로 한다. 커밋마다 `Co-Authored-By` 줄 바로 위에 서명 줄 `Kaizen-Phase: kaizen-0924-final` 을 둔다.

1. **AR-01 상태 커밋** — 열아홉 계약과 열아홉 QA 리포트만 `git add -- <38 경로> && git commit -o -- <38 경로>` 로 싣는다
2. **ER-01 · ER-02 교차 진단 기록** — 먼저 `$FBK/evaluator` · `$FBK/contract` 에 서른네 파일을 `cp -p` 로 떠 둔다(슬러그마다 한 파일 — `fbx.py` 가 찾는 방식과 같다).
   그다음 `fbedit.py` 로 고친다 — 평가자 피드백은 `fbedit.py <파일> sprint-contract replace "<글>"`, 계약 피드백은 `fbedit.py <파일> - append "<글>"`.
   글은 `Final 교차 진단 (xdiag-all.md P<N>):` 로 시작하고 아래 표의 결론을 담는다. 평가자 쪽 글에는 「판정 유지」 와 표의 필수 글자를 넣는다.
   고친 파일마다 `bash harness/scripts/verify-feedback.sh <파일>` 이 `PASS` 여야 한다. 두 followups 평가자 피드백은 건드리지 않는다(FN-77)
3. **ER-03 개정 파일** — P1 개정 파일 끝에 설명 한 줄과 `end_sha: 76cfb376e2293350e2583c50166286bd2ec95b82` 를 덧붙인다.
   P7 · P8 · P9 · P11 개정 파일 끝에 한 줄씩 — `교차 진단 뒤 Final 에서 고침 — <kit-followups 커밋 전체 sha> (<고친 것>) · amend_direction: unchanged — 조건 · 측정은 그대로 두고 구현을 고쳤다. 근거: xdiag-all.md P<N> DG-02`.
   새 줄이 `end_sha:` 로 시작하면 그 Phase 측정 상한이 움직인다 — 그렇게 쓰지 않는다
4. **AR-02 처리 배정표** — Phase 행 일흔넷의 대상 계약 칸에 그 번호 Phase 슬러그, QA 칸에 `APPROVE`. 미반영 여덟 행의 비고 끝에 「 · 미반영 — <사유> (<notes 파일> §미반영 키와 사유)」.
   다른 칸 · 다른 행은 손대지 않는다. 비고가 빈 행은 원래처럼 `| |` 로 둔다(`|  |` 로 쓰면 MD060 새 경고 — 사본 실측)
5. **ER-04 옛 값 등록부** — OpenAPI `3.1.1` 항목 allow 에 backend-kit 세 경로(`backend-kit/skills/backend-audit/references/audit-criteria.md` · `backend-kit/skills/backend-guide/SKILL.md` ·
   `backend-kit/skills/backend-system/SKILL.md`, 사유 「date-time 형식 근거로 특정 판 명세 링크를 인용 — 최신판 주장이 아니다」)를 더한다.
   새 항목 셋 — `old: "OpenAPI 3.2.0"` → `new: "OpenAPI 3.2.1"`(allow `docs/backend/research-log.md` 날짜 박힌 기록), `old: "1.7+ native state encryption"`
   (allow `docs/infra/research-log.md` 옛 문장을 고친 이력), `old: "-kubernetes-version 1.30.0"` → `new: '-kubernetes-version "$K8S_VERSION"'`(allow 없음).
   `note` 에 출처 Phase 를 적는다. `scripts/check-stale-values.py` 의 `EXCLUDED_KITS` 해제는 범위 밖이라 다음 사이클(F1H-79)
6. **AR-03 문서 사이트** — 아래 페이지 표 마흔넷을 `.claude/skills/docs-site/SKILL.md` 원칙대로 원본 전체에서 다시 만든다(한 페이지 = 한 에이전트, 부분 패치 금지).
   파일 이름 · 내비 id · `--accent` 는 그대로 둔다. 새 페이지는 없다. `docs/index.html` 은 harness 다섯 항목(`skill-design` · `agent-design` · `contract-design` ·
   `qa-evaluation` · `contract-schema`) 제목의 판 번호만 원본 판 번호로 고친다(다섯 줄 — 오케스트레이터 F2 넷째 줄 「갱신 페이지 등록」).
   원본 머리 설정 판 번호가 사이클 동안 오른 페이지 열넷은 새 판 번호를 제목 · 뱃지에 담는다(`TOKENS` 끝 열넷). 표의 「새 글자」 가 페이지 본문에 있고 「옛 글자」 가 없는지
   `docs.py` · `navver.py` · `titlever.py` 로 돌려 보고, `node scripts/check-docs-a11y.js <페이지>` · `check-api-kit-docs.py` · `check-docs-links.py` · `check-contrast-claims.py` 를 통과시킨 뒤 킷 폴더마다 커밋한다
   (`docs/index.html` 은 harness 페이지와 같은 커밋). notes · 기록에는 페이지 판 번호를 글자로 옮기지 않는다 — `0.3.0` · `0.2.1` 이 react-kit · howto-kit
   `plugin.json` 판과 같아 AP-01 이 센다(판 번호 확인은 `docs.py` 출력 줄로 대신한다)
7. **AR-04 · SK-02 기록** — `docs/kaizen/changelog.md` 에 `## [2026-09-24] — …` 항목 하나(Phase 1 ~ 17 changelog 단락과 Final 세 계약 단락),
   `flutter-changelog.md` 에 Phase 5, `docs/kaizen/research-log.md` 에 Phase 1 ~ 4 · 12 · 13 · 14 · 17 킷 로그와 Final 두 followups 킷 로그,
   `flutter-research-log.md` 에 Phase 5, `docs/design/research-log.md` 에 Phase 6 킷 로그. 소제목에는 `(2026-09-24 사이클)` 을 붙여 옛 제목과 겹치지 않게 한다.
   URL 은 `<…>` 또는 `[이름](URL)` 로 감싼다(MD034). 머리 설정은 `version` · `last_updated` 만 바꾼다. `CLAUDE.md` 세 줄을 Phase 17 까지로 고친다
8. **ER-05 피드백 정리** — `python3 "$K/cleanup-do.py" "$FBD" "$ARCH" "$FBLIST"` 가 목록을 먼저 쓰고 가장 오래된 초과분을 보관 폴더로 옮긴다(지우지 않는다).
   `cleanup-log.yaml` 끝에 한 건 — `date`(그 순간 `date +%Y-%m-%d`) · `cycle: "kaizen-2026-09-24"` · `total_before` · `aged_over_6months` · `over_500_truncated` ·
   `deleted: 0` · `archived_to: "<$ARCH 절대경로>"` · `notes`
9. **AR-05 · AR-06 · SC-01** — `kaizen-state.yaml` 의 `cycle_id` 를 `"kaizen-2026-09-24"` 로(`status: completed` 그대로). 실패 횟수 파일에 `phase_15` ~ `phase_17`(0),
   `last_updated: "2026-09-24"`. `evals-audit-2026-09-24.md`(sync-evals 요약 줄 · evals.json 열 경로 · 스킬 더함·지움·이름 바꿈을 찾은 `git diff --name-status` 명령과 0 건).
   메모리 후보 `memory-promotion-candidates-2026-09-24.md`(아래 후보). 릴리스 계획 `release-plan.md`(아래 릴리스 표와 `release.sh` 열네 줄).
   릴리스 계획 표의 근거 칸은 notes 파일을 `` `.harness/.meta/kaizen-0924/<파일>.md` `` 전체 경로(백틱으로 감쌈)로 적는다 — 아래 표의 짧은 이름(`phase3-notes.md`)을 그대로 옮기면 `plan.py` 가 `basis=0` 을 낸다(모의 판 실측).
   메모리 후보의 `source_evidence` 경로는 저장소 경로나 `~/.harness/` 아래로 적는다 — 교차 진단 원문 `xdiag-all.md` 는 세션 스크래치에만 있어 다음 세션의 `/reflect-promote` 가 열 수 없다.
   교차 진단 근거는 ER-01 · ER-02 가 고친 전역 피드백 파일이나 notes `## 교차 진단 기록` 절을 가리킨다
10. **DG-05 예행** — `bash "$K/dg05.sh" HEAD "$CB"` 가 모두 0 · 사후 점검 PASS 인지 본다
11. **AR-07 감사 기록** — 파일 끝에 빈 줄 하나를 먼저 붙이고(MD022 · MD032 방지), 오케스트레이터 SKILL.md 수동 편집(harness followups `66b4e4c`, `+29 −18`)을 담은
    JSON 으로 `python3 scripts/append-audit-log.py --cycle-id kaizen/2026-09-24 --manual-edits <json> --notes "<한 줄>"` 을 돌린다(사후 점검 실패가 남았으면 `--failures` 도).
    JSON 은 스크래치 `$SP/final-manual-edits.json`(`--failures` 도 스크래치)에 두고 커밋하지 않는다 — 저장소에 두면 SK-01 (f) `json=14` 가 15 가 되어 SK-01 · AR-08 이 함께 떨어진다.
    그다음 새로 붙은 항목의 끝 `---` 앞에 `### 두 followups 가 고치지 않은 것 (2026-09-24 사이클)` 등 소제목(날짜 붙임)으로 F1H 스물아홉 · F1K 서른셋 · F1H-N1 ~ N4 ·
    두 후속 notes 파일 이름(`f1-harness-followups-notes.md` · `f1-kit-followups-notes.md` — `F1K-10` 같은 이름은 이 계약이 붙였고 원래 표는 행 번호만 쓴다) ·
    Phase notes 열일곱의 다음 사이클 메모 경로 · 이번 사이클 메타 이슈(아래)를 적는다
12. **AR-08 notes** — 차례가 중요하다(공통 정의는 `$AM` 에 `end_sha:` 가 없으면 `END_UNRESOLVED` 로 멈춘다).
    (가) `$AM` 에 마지막 구현 커밋으로 `end_sha:` 를 적어 커밋한다 (나) 공통 정의를 읽은 셸에서 `f1.sh` · `tonegrade.py` · `toneterms.py` · `synt.sh` · `amend.sh` 를 돌려
    그 출력 줄을 `## F1 정합` 절에 글자 그대로 옮긴다 (다) notes · 검토 기록을 커밋한다 (라) 그 sha 로 `end_sha:` 를 한 줄 더 덧붙여 커밋한다.
    notes 에 옮길 여덟 줄은 (가) · (다) · (라) 커밋으로 바뀌지 않는다 — `synt.sh` 는 셸 · 파이썬 · JSON · YAML 만 세고, `amend.sh` 는 Phase 개정 파일과 Phase 서명 커밋만 읽는다

교차 진단 기록 표 — ER-01 · ER-02 글의 원문(`xdiag-all.md` 각 절). 「필수 글자」 는 `fbx.py` 가 새로 적은 부분에서 찾는다:

| P | 평가자 피드백에 적을 결론 (필수 글자) | 계약 피드백에 붙일 측정 구멍 (필수 글자) |
| - | ------------------------------------- | ---------------------------------------- |
| 1 | 판정 유지. QA 리포트 `:39` 가 ER-03 · SK-04(b) · AR-04② 대조를 실행했다고 적었지만 본문 근거에 실행 기록이 없다(교차 진단이 돌려 보니 셋 다 살아 있음). `Evaluated` 20:55 vs 파일 20:52 (`:39`) | ER-04 셋째 · AR-04② 가 notes 커밋 `76cfb37` 을 범위 밖에 뒀다 — Final 이 상한을 덧붙이고 다시 재어 0 · 0. SK-01 은 핵심 문장을 지운 사본에서도 통과한다 (`SK-01`) |
| 2 | 판정 유지. `Evaluated` 22:38 이 파일 저장 22:34 보다 늦다 — harness followups ER-04 가 평가자 저장 절차를 고쳤다 (`Evaluated`) | ER-01 이 네 파일 URL 을 합쳐 비교해 파일 사이로 옮긴 인용을 못 잡는다. ER-03 둘째 · AR-06 ①② · N/A 다섯이 서명 줄 커밋만 본다 (`ER-01`) |
| 3 | 판정 유지. DG-05 (b)(c) 가 다섯 파일 가운데 넷을 읽지 않는데 QA 가 짚지 않았다 (`DG-05`) | AR-06 ③ 교집합이 `verify_seal` 이 없으면 조용히 0. `assertions.json` #1 · #2 는 제목 글자만 본다 (`AR-06`) |
| 4 | 판정 유지. 리포트가 `end_sha` 5 회(실제 2) · N/A 3 건(실제 4)으로 적었다 (`N/A`) | DG-02 (b) 가 shellcheck 가 있는지 확인하지 않는다. ER-01 의 열한 경우 밖에 이름 바꾸기 경로 지정 커밋이 있었다 (`DG-02 (b)`) |
| 5 | 판정 유지. SK-09 (a) 정규식이 좁아 증거 블록 빈칸 넷을 못 잡았다 — kit followups `535e143` 이 고쳤다 (`SK-09`) | SK-09 (a) 가 「와」 · 「+」 없는 꼴을 못 잡는다 (`SK-09 (a)`) |
| 6 | 판정 유지. 리포트 N/A 3 건(실제 4) · AR-01 근거 커밋 오기 (`N/A`) | DG-05 (a) `bad=` 가 늘 0(V 줄에 FAIL 이 안 찍힘) · RE-02 정규식이 하이픈 폴더를 못 읽음 · AR-01 `outside=` 가 `.harness/` 를 통째로 뺌 (`RE-02`) |
| 7 | 판정 유지(글자 기준). DG-02 는 뜻 기준 FAIL — 연구 기록 소제목 넷을 kit followups `154916a` 가 고쳐 해소. 리포트 N/A 6 건(실제 5) (`DG-02` · `154916a`) | DG-02 가 더한 줄 경고만 세어 옛 줄에 붙은 MD024 넷을 놓쳤다 · DG-05 (c) 범위 · ER-03 셋째 · AR-01 ①② 서명 없는 커밋 (`DG-02`) |
| 8 | 판정 유지(글자 기준). DG-02 뜻 기준 FAIL — `cc11f71` 이 고침 (`DG-02` · `cc11f71`) | DG-02 · AR-01 ②③ 이 `.harness/` 를 통째로 뺌 · ER-03 셋째 · AR-01 ① 이 다른 공유 파일을 못 봄 · DG-05 (c) (`AR-01`) |
| 9 | 판정 유지(글자 기준). DG-02 뜻 기준 FAIL — `c4eeef3` 이 고침. QA 교차 진단 요청 목록에 DG-02 가 빠졌다 (`DG-02` · `c4eeef3`) | DG-02 · SK-09 여덟째 값이 목록 밖 옛 꼴을 못 봄 · DG-05 (c) (`SK-09`) |
| 10 | 판정 유지. SK-07 이 템플릿 값만 재어 실제 프로젝트에 `strictPort` 가 안 들어가는 것을 못 봤다 — kit followups `d6e30aa` 가 고쳤다. 리포트 사용자 발화 시각 · 증거 부풀림 (`strictPort`) | DG-05 (b) 가 `docs/react/` 를 못 읽음 · SK-04 마지막 값이 콜론 꼴을 못 잡음 · RE-02 숫자 뒤 빈칸 (`SK-04`) |
| 11 | 판정 유지(글자 기준). DG-02 뜻 기준 FAIL — `cfef54f` 가 고침 (`DG-02` · `cfef54f`) | DG-02 · ER-03 (d) · AR-01 ① 서명 없는 다른 킷 커밋 · SK-04 ~ 06 · AR-03 (c) 좁음 (`DG-02`) |
| 12 | 판정 유지. DG-02 는 더한 줄만 세지만 실제 판은 새 경고 0 (`DG-02`) | DG-02 · SC-02 transcript 검사 판별력 · AR-01 · ER-03 이 서명 없는 다른 킷 커밋을 못 봄 (`DG-02`) |
| 13 | 판정 유지. 사용자 교정 대조가 워크트리 이름으로 로그를 찾다 건너뛰었다 — harness followups ER-03 이 고쳤다. SK-06 알려진 답이 킷 출력을 잠갔다 (`사용자 교정`) | AP-03 이 V6 가 안 읽는 두 파일에서 공허 · SK-07 정책 셋 가운데 하나만 · DG-06 `doc_mine` 늘 0 (`AP-03`) |
| 14 | 판정 유지. 리포트 측정 수 26 vs 25 · N/A 3 vs 2 · 28/28 오기 (`N/A`) | DG-02 가 규칙별 수만 비교해 자리가 바뀐 경고를 못 봄 · ER-03 (d) · AR-01 ① (`DG-02`) |
| 15 | 판정 유지. 같은 종류 죽은 검사 `core-antipatterns.md:36` 이 남았다 — kit followups `f93d715` 가 고쳤다 (`core-antipatterns`) | 측정 구멍 없음 — 0 기대 값 모두 사본에서 1 이상. 한계 메모: DG-02 가 규칙별 수만 비교해 자리가 바뀐 경고를 못 볼 수 있다(교차 진단이 규칙 + 줄 글자로 다시 재어 0) (`없음`) |
| 16 | 판정 유지. 뷰어에 판정 불가 자리가 없다(다음 사이클) · api-ui 서버 명령 — kit followups `9da098b` (`판정 불가`) | SK-09 `curl_missing` · AR-03 `outside_changed` · SK-05 `dir_api` · ER-02 `NAMES` 구멍 넷 (`SK-09`) |
| 17 | 판정 유지. 러너가 `bash` 펜스만 봤다 — kit followups `6de53a3` 가 고쳤다 (`펜스`) | 측정 구멍 없음 — 여섯 0 기대 값 모두 사본에서 1 이상. 한계 메모: DG-04 · SK-07 에서 러너 안쪽 셸이 이 맥에서는 늘 `/bin/sh` 라 dash 로 한 번도 돌지 않았다(교차 진단이 dash 를 앞에 두고 다시 돌려 통과 — 결함 아님) (`없음`) |

미반영 여덟 행 — AR-02 비고에 붙일 사유와 notes:

| 행 | 사유 요지 | notes |
| -- | --------- | ----- |
| `F09` | flutter-preflight · react-preflight 기준 커밋 비교 — 근거 파일에 근거가 없다 | `phase5-notes.md` · `phase10-notes.md` |
| `F18` | YAML 블록 검사 — 걸리는 것이 전부 일부러 깬 예시 | `phase4-notes.md` |
| `F20` | 한 나라 우선 판단 — `user-setup:P10`(킷 밖)으로 | `phase11-notes.md` |
| `F22` | 겹친 `ProviderScope` 부분 — 근거 파일에 없다 | `phase5-notes.md` |
| `F25` | 근거 파일이 규칙을 만들지 말라고 권함 · 사용자 확인이 먼저 | `phase5-notes.md` |
| `F28` | 워크트리 상태 스크립트 — 외부 권고 없음 | `phase4-notes.md` |
| `design:P2` | 개수 규칙 방향 — 사용자 확인 목록 | `phase6-notes.md` |
| `user-setup:P2` | 폐기 결정 줄 — F20(Phase 11) 몫 | `phase4-notes.md` |

릴리스 표 — SC-01. 기능 추가 = minor, 고침만 = patch(러닝북 「버전」 절). 한 킷에 Phase 와 후속 계약이 다른 단계를 적었으면 큰 쪽을 쓴다:

| 킷 | 단계 | 근거 |
| -- | ---- | ---- |
| `harness` | minor | `phase3-notes.md` 「검증 레벨/루브릭 변경 … minor」 · `phase4-notes.md` 「스킬 절차 추가와 훅 동작 변경이라 minor」 (followups 는 patch 로 봤지만 큰 쪽) |
| `flutter-toolkit` | minor | `phase5-notes.md` 「스킬 프롬프트 · eval 기준 변경이라 minor」 |
| `design-kit` | minor | `phase6-notes.md` 규약 절 셋 · 승인 기록 칸 둘 · 감사 행 · 평가 사례 셋 |
| `backend-kit` | minor | `phase7-notes.md` 새 Gotcha 둘 · 감사 기준 두 행 |
| `infra-kit` | minor | `phase8-notes.md` Gotcha · 평가 사례 · 보고 형태(네 칸) |
| `rust-kit` | minor | `phase9-notes.md` Gotcha 둘 · 절차 하나 · 판정 형식 · 평가 사례 |
| `react-kit` | minor | `phase10-notes.md` 규약 틀 · 보고 형식 · 템플릿 기본값 · react-l10n 기본 흐름 |
| `planning-kit` | minor | `phase11-notes.md` PRD 산출물 틀(비범위 표) · 뒤 단계 스킬 동작 |
| `reflect-kit` | minor | `phase12-notes.md` 훅 동작 · 폴더 이름 규칙 · digest 출력 틀 |
| `bambu-kit` | minor | `phase13-notes.md` MakerWorld 읽는 순서 · G-code 길이 재기 블록 · 자기 검사 · 시험 파일 |
| `onboarding-kit` | minor | `phase14-notes.md` Gotcha 9 · 게이트 평가 러너 · 평가 사례 |
| `tone-kit` | minor | `phase15-notes.md` K-11 새 규칙(관측 컨벤션) · 이름 게이트 복구 |
| `api-kit` | minor | `phase16-notes.md` 판정 줄 양쪽 값 · 판정 불가 수 · 브라우저 확인 단계 |
| `howto-kit` | patch | `phase17-notes.md` 게이트 스크립트를 자식 셸에서 찾게 고침 · 러너 셸 확대 — 새 기능이 아니다 |

메모리 후보 — AR-06. 반드시 낼 둘과 낼 만한 둘. `grounding` 은 모두 `execution_evidence`(교차 진단 · QA 리포트 · 명령 출력), `actionability` 는 `claude_behavior`.
`source_evidence` 는 저장소 경로(QA 리포트 · notes · 개정 파일)나 `~/.harness/` 아래 전역 피드백 파일만 가리킨다 — 세션 스크래치(`/private/tmp` · `/tmp`) 경로는 0 개(AR-06 `tmp_bad=0`):

- `lint-new-warning-added-lines-only` — 편집기 경고를 더한 줄에서만 세어 옛 줄에 붙은 새 MD024 를 놓침. P7 · P8 · P9 · P11 (freq 4). 바라는 것: 파일마다 (규칙, 줄 글자) 묶음을 편집 전 판과 비교
- `scope-count-signed-commits-only` — 범위 측정이 서명 줄 커밋만 봐서 서명 빠진 커밋을 못 봄. P2 · P7 · P8 · P11 · P12 · P14 (freq 6). 바라는 것: `git log <기준>..<상한> -- <경로>` 로 직접 센다
- `qa-report-summary-count-typed` — QA 리포트 요약 수(N/A 건수 · end_sha 줄 수 · 측정 수)를 손으로 적어 틀림. P4 · P6 · P7 · P10 · P14 (freq 5)
- `cycle-state-not-advanced` — 사이클 상태 파일을 새 사이클로 안 바꿔 사후 점검 날짜 검사가 옛 항목으로 통과(이 계약 편집 전 실측, freq 1)

감사 기록에 적을 이번 사이클 메타 이슈 — 위 넷(`kaizen-state.yaml` 미갱신 · 피드백 500 초과 · 검사기 슬러그 형식만 · 도구 고정 소제목)과 FN-79 · FN-80.
붙은 부분에 여섯 글자가 있어야 한다(AR-07 `meta=6/6`): `kaizen-state.yaml` · `feedback-archive`(옮긴 보관 폴더) · `check-insights-tracking.py` ·
`append-audit-log.py:148`(고정 소제목을 찍는 줄) · `FN-79` · `FN-80`. 도구가 찍는 생성 줄에 이미 `scripts/append-audit-log.py` 가 들어 있어 파일 이름만으로는 이 이슈를 적었는지 알 수 없다 — 줄 번호를 붙인다.

문서 사이트 페이지 표 — 러닝북 규칙 「F2 매핑 표 원본 가운데 대응 HTML 이 있는 것」 을 이 넷으로 정했다.
(가) `detect-docs-drift.py --since 390dea8` 가 있는 페이지로 잇는 것 32 · (나) 원본 이름과 다른 페이지를 `docs/` HTML grep · `card-source` 링크로 찾은 것 1(`g4-quality.md` → `quality.html`) ·
(다) 매핑 표 밖 원본이지만 킷 문서 폴더에 같은 이름 페이지가 있는 것 10 · (라) Phase notes 가 Final F2 로 넘긴 페이지 가운데 위에 없는 것 1(`howto-kit/overview.html`, phase17-notes).
(다) 를 넣은 이유 — Phase 8 · kit followups notes 가 `infra-test.html` · `gate-result-taxonomy.html` · `visual-change-protocol.html` · `schema.html` 을 이름으로 넘겼고,
같은 성격의 나머지 여섯(스킬 페이지 다섯 · reflect `design.html`)만 빼면 F4 체크리스트 「변경된 소스에 대응하는 HTML 이 최신」 이 깨진다. 표는 `docs.py` 의 `PAIRS` 가 그대로다.

대응 페이지가 없어 만들지 않는 원본 열아홉 — `detect-docs-drift.py` 가 `[NEW]` 로 낸 스물 가운데 (나) 로 잇는 하나를 뺀 것. notes `## 문서 사이트` 에 그대로 적는다:
`bambu-kit/skills/bambu-print-profile/references/comment-analysis.md` · 연구 기록 여덟(`docs/api` · `docs/backend` · `docs/flutter` · `docs/infra` · `docs/planning` · `docs/react` · `docs/rust` · `docs/tone` 의 `research-log.md`) ·
`flutter-toolkit/references/figma-parity-self-verify.md` · `react-kit/references/common-gotchas.md` · `reflect-kit/skills/reflect-digest/SKILL.md` · `reflect-kit/skills/reflect-kaizen/SKILL.md` ·
`rust-kit/references/project-detection.md` · `tone-kit/references/` 다섯(`core-antipatterns.md` · `core-comment.md` · `core-naming.md` · `locale-korean.md` · `sources.md`).

## 범위 경계

- 이 계약 시작 HEAD: `511f19b5823886bef5c21dadcd656a692f298db5` (`git rev-parse HEAD`, 2026-09-25 19:11). 범위 상한은 개정 파일
  `.harness/sprint-amendments-kaizen-0924-final.md` 의 `end_sha:` 마지막 값이다 — `HEAD` 로 재지 않는다. 사이클 전체를 재는 기준은 가지가 `main` 에서 갈라진
  `83cfb4f311d6497186da13c75bdb8f8a108481b3`(공통 정의 `CB`), 문서 사이트 기준은 러닝북이 정한 `390dea8`(공통 정의 `DB`)다
- **이 계약의 커밋 메시지에는 전부 `Co-Authored-By` 줄 바로 위에 서명 줄 `Kaizen-Phase: kaizen-0924-final` 한 줄을 넣는다** (봉인 커밋 · 상태 커밋 · notes · `end_sha` 커밋 포함).
  AR-08 · AR-09 가 이 줄로 이 계약 커밋을 가리고, 서명 없는 커밋은 AR-09 `unsigned` 로 따로 센다. notes 를 커밋한 뒤 그 sha 로 `end_sha:` 줄을 하나 더 덧붙여 커밋한다(옛 줄은 지우지 않는다)
- 커밋은 **`git add -- <경로…> && git commit -o -- <경로…>` 로 내 경로만** 싣는다. `git add -A` · `git commit -a` · `git stash` · `git reset --hard` 금지
- 쓰는 저장소 경로 — `.harness/`(계약 · 개정 · notes · 검토 기록 · QA 리포트 열아홉 · 상태 · 기록 파일) · `.claude/kaizen-input/insights-report.md` · 페이지 표의 `docs/**/*.html` 마흔넷 ·
  `docs/kaizen/` 네 파일 · `docs/design/research-log.md`(새 항목만) · 루트 `CLAUDE.md` · `docs/index.html`. `docs/index.html` 은 harness 다섯 항목 제목의 판 번호만 고친다
  (원본 판 번호가 이번 사이클에 올랐다). 루트 `README.md` 는 러닝북 범위이지만 바꿀 것이 없다(README 판 번호 표는 릴리스 때 `release.sh` 가 고친다) — AR-09 허용 경로에서도 뺐다
- 이 계약 피드백 초안(`.harness/feedback-draft*.yaml`)은 커밋하지 않는다 — 저장소에 YAML 이 하나 늘면 SK-01 (f) 의 `yaml=6` 이 7 로 바뀐다. 이 계약이 커밋하는 YAML 은 `cleanup-log.yaml` · `kaizen-failure-count.yaml` · `kaizen-state.yaml` · `stale-values.yaml` 넷뿐이다
- 쓰는 저장소 밖 경로 — `~/.harness/feedback/`(평가자 · 계약 피드백 서른넷의 두 칸, 가장 오래된 초과분 이동) · `~/.harness/feedback-archive/kaizen-2026-09-24/`(옮긴 파일) ·
  스크래치 `kaizen/final-fb-before/`(고치기 전 사본) · `kaizen/final-fb-before-cleanup.txt`(정리 직전 목록). 승격 원장(`~/.claude/logs/*/promotions-ledger.md`)과
  메모리 파일은 쓰지 않는다(오케스트레이터 F3.5 경계)
- **피드백은 지우지 않고 옮긴다.** F3 는 「6 개월 초과 삭제 · 500 개 초과 삭감」 이다. 사용자 전역 자료를 되돌릴 수 없게 지우는 대신 피드백 경로 밖 보관 폴더로 옮겨
  피드백 경로를 500 개 이하로 만든다 — 수집기 · 집계 시험은 피드백 경로만 읽으므로(`grep -rn feedback-archive` 저장소 0 줄) F3 의 목적과 결과가 같다. 기록의 `deleted` 는 0, `archived_to` 에 보관 폴더를 적는다
- 건드리지 않는 것 — 킷 폴더 열넷 · `scripts/` · `.claude/skills/` · `.github/` · `.claude-plugin/marketplace.json` · 킷 `plugin.json`(AR-09 `forbidden=0`).
  버전은 올리지 않는다(러닝북 「버전」 절) — `release-plan.md` 가 오케스트레이터 Step F4 1 번과 체크리스트의 버전 두 줄을 대신한다(SC-01)
- 이 계약 범위가 아닌 것 — PR 생성 · 푸시(오케스트레이터 F4 7 번)는 Final QA 뒤 부모가 사용자 규칙대로 한다. 이 계약 자신의 `status: done` · QA 리포트 커밋은 QA 뒤 일이다
- Phase 상태 커밋을 Final 서명으로 싣는다 — 교차 진단 P7 은 「그 Phase 서명으로 싣고 그 Phase 개정 파일에 `end_sha` 를 한 줄 더」 를 제안했지만 택하지 않는다.
  `status:` 줄은 봉인 밖이고 어느 Phase 측정도 재지 않는다. 열아홉 개정 파일에 `end_sha` 를 더하면 봉인된 Phase 계약들의 측정 상한이 움직인다
- 공통 정의가 읽는 이름은 바꾸지 않는다 — notes 소제목 `## 커밋` · `## F1 정합` · `## 교차 진단 기록` · `## 문서 사이트` · `## 넘기는 것` · `## 다음 사이클 메모`,
  감사 기록의 도구 머리 줄, 피드백 글 머리 `Final 교차 진단 (xdiag-all.md P<N>)`, 개정 파일 줄 머리 `교차 진단 뒤 Final 에서 고침 —`
- 편집 전부터 있던 경고(changelog MD024 22 줄 · 감사 기록 MD024 5 줄 등 — 1.4 표)는 범위 밖이다 — DG-02 는 파일마다 (규칙, 줄 글자) 묶음이 느는지만 잰다.
  예외 하나: `append-audit-log.py` 가 찍는 고정 소제목 세 줄의 MD024. 도구 형식이라 이번에 피할 수 없고 스크립트는 범위 밖이다(FN-78)
- DG-02 · AP-01 · AP-03 이 재지 않는 마크다운 — (1) 이 계약이 커밋하는 QA 리포트 열아홉(편집기 경고 648 개: MD022 332 · MD032 309 · MD038 7). 평가자가 쓴 기록이라 글자를 고치지 않는다 —
  이미 추적되는 QA 리포트 57 개와 같은 관례다 (2) 계약 파일 자신의 MD041 하나 — 머리 설정 뒤 첫 제목이 `##` 인 계약 공통 꼴이다. 같은 파일의 MD038 여섯(AR-04 측정 · 봉인 전 실측 표)은
  `tr '\n' ' '` 출력의 끝 빈칸을 기대 출력 글자 그대로 보인 코드 조각이라 고치지 않는다 — 빈칸을 지우면 기대 출력이 실제 출력과 달라진다 (3) 검토 기록 `$REVIEW` — REVIEW 가 쓴 기록이라 BUILD 가 고치지 않는다.
  검토 시점 편집기 경고 0 건(REVIEW 실측)이지만, 페이지 판 번호 인용(`0.3.0` · `0.2.1`)이 react-kit · howto-kit `plugin.json` 판과 글자가 같아 `MDS` 에 넣으면 AP-01 이 판 번호가 아닌 인용을 센다.
  개정 파일 `$AM` 은 BUILD 가 새로 쓰는 마크다운이라 `MDS` 에 넣었다(열여덟)
- 오라클 해소: AR-03 · DG-02 — 훅이 「산문-grep」 으로 잡은 것은 측정 절의 기대 출력 글자(`내비 등록: …` · `NEW … MD024 ### …`)다. 판정은 `docs.py` · `navver.py` · `titlever.py` · 검사 스크립트 셋과
  markdownlint-cli2 를 실제로 돌린 출력이고, 문서에 문장이 있는지를 재는 grep 은 없다
- 오라클 해소: AR-06 — 훅이 「산문-grep」 으로 잡은 것은 승격 원장 파일 수를 세는 `find … | grep -c .` 다. 판정은 후보 파일을 yaml 로 읽어 키 · 값 · 근거 경로 존재를 재는
  `mem.py` 실행 출력이고, 따옴표 없는 시각 · `~/.harness` 밖 경로 · 스크래치 경로를 넣은 모의 파일로 값이 바뀌는 것을 봉인 전에 돌렸다(봉인 전 실측 표 AR-06 행)
- 측정 전제 — (1) 공통 정의의 두 판 `$T/B` · `$T/E` 는 `git archive` 로 푼다 (2) 저장소 밖 측정(ER-01 · ER-02 · ER-05 · AR-06 원장)은 BUILD 가 만든 사본 `$FBK` · 목록 `$FBLIST` 를 읽는다.
  둘이 없으면 도우미가 `사본 없음` · `UNREADABLE` 로 멈춘다 — 사본 없이 고치면 이 조건은 판정할 수 없어 FAIL 이다 (3) DG-05 사후 점검은 git 기록이 필요해 `$END` 를 새로 복제해 돈다
  (4) 스크래치 경로는 이 세션 폴더다 — QA 는 같은 세션에서 돈다
- 사용자 승인(Step 5) 대체: 사용자가 「자동으로 끝까지 알아서 진행해 내 허락이 필요한건 코덱스로 리서치나 검토받고」라고 위임했다(세션
  `de8c7935-a5b6-4df5-9106-fafa73c288a0` 기록 queued_command `2026-09-24T04:04:16.964Z`). Codex 사용량 한도가 소진돼(오류 원문 「You've hit your usage limit … try
  again at 11:05 PM」, 2026-09-24) 독립 Claude 검토자(REVIEW 에이전트)가 대신한다. 이어 사용자가 「코덱스 대신에 그냥 너가 알아서 진행하라고」라고 명시했다(같은 세션
  기록 user `2026-09-24T11:54:58.940Z`). 뒤에 「코덱스도 사용할 수 있으니깐 사용해」(user `2026-09-25T06:19:45.056Z`)가 있었고 Codex 검토는 두 followups 몫으로 끝났다 —
  이 계약은 Codex 지적을 고치지 않는다(러닝북). 검토 결과 파일: `.harness/.meta/kaizen-0924/final-review.md`(REVIEW 가 쓴다)
- 검토 반영(2026-09-25, 검토 시점 초안 sha256 앞 16 자 `50a027d88f4a03d9`): 반드시 고칠 것 여섯은 모두 반영했다. 권고 일곱 가운데 여섯은 반영했고,
  권고 2 의 「`$REVIEW` 를 `MDS` 에 넣기」 만 뺐다(AP-01 과 부딪힘 — 위 「DG-02 · AP-01 · AP-03 이 재지 않는 마크다운」 줄). 검토 문구와 다르게 쓴 곳 둘 —
  AR-07 메타 글자는 `append-audit-log.py` 대신 `append-audit-log.py:148` 로 쓰고 피드백 500 초과 이슈의 `feedback-archive` 를 더했다(도구 생성 줄 때문에 파일 이름만으로는
  메타 절 없이 `1/5` 가 남는다 — 봉인 전 실측 표 AR-07 행). 첫 화면 판 번호 측정은 블록 대신 도우미 `navver.py` 로 두었다(같은 식)
- 2 회차 검토 반영(2026-09-25, 검토 시점 초안 sha256 앞 16 자 `3e5a3fb5735ad9ab`, 마지막 판정 `VERDICT: CHANGES`): 반드시 고칠 것 하나(AR-06 `mem.py` — 따옴표 없는 `generated_at` 을
  떨어뜨림 · `~/.harness` 밖 절대경로를 재지 않음)를 검토 문구대로 반영했다. 검토 문구와 다른 곳은 시각 식이 끝 `Z` 도 받게 한 것 하나다 — 따옴표 친 `…Z` 가 떨어지지 않게 했다.
  권고 1(harness 다섯 페이지 `<title>` 판 번호)은 개선안 6 의 「제목 · 뱃지에 담는다」 와 맞춰 AR-03 에 `titlever.py` 로 넣었다. 권고 2 는 조건끼리 부딪힘이 없다는 확인 기록이라 고칠 것이 없다.
  반영 뒤 봉인 전에 다시 돌린 값은 봉인 전 실측 표 AR-03 · AR-06 행이다 — `titlever.py` 시작 판 `title_ver=0/5` · 제목 하나 `1/5` · 본문에만 `1/5` · 다섯 제목 `5/5`,
  `mem.py` 모의 파일 열하나(따옴표 없는 시각 `parse=1`, 고치기 전 식 `parse=0` · 시간대 없음 `parse=0` · `~/.harness` 경로 `out_bad=0` · `$HOME/.claude/CLAUDE.md` 한 줄 `out_bad=1` ·
  스크래치 한 줄 `tmp_bad=1 out_bad=1` · `status: active` 와 `self_inference` `keys_bad=2 forbidden=2 grounding_bad=2`)
- 승인 대체 기록(봉인 직전, 2026-09-25): 위 「사용자 승인(Step 5) 대체」 의 두 앵커 위임에 따라 사용자 승인 자리를 REVIEW 두 회차 검토(`.harness/.meta/kaizen-0924/final-review.md`)와
  그 지적 반영이 대신한다. 2 회차 판정이 `CHANGES` 였지만 남은 지적은 반드시 고칠 것 하나 · 권고 둘이 전부이고 위 줄대로 모두 반영하거나 확인했으므로 3 회차 검토 없이 봉인한다.
  봉인 뒤 조건이 틀린 것을 알게 되면 조건 줄을 고치지 않고 개정 파일에 적는다(Step 6.6 (d)). 사용자가 할 일: 없음
- 문서 사이트 페이지 재생성(AR-03)은 Claude 에이전트와 Codex(`gpt-5.6-sol`, 쓰기 모드 — 사용자 지시 「코덱스도 사용할 수 있으니깐 사용해」, user `2026-09-25T06:19:45.056Z`)가
  나눠 맡는다. 한 페이지 = 한 에이전트 · 원본 전체 반영 원칙과 조건 · 측정은 그대로이고, 페이지마다 누가 만들었는지는 notes `## 문서 사이트` 절에 적는다
- 이 계약은 DRAFT 가 썼다. 봉인(6.6) · 봉인 커밋(6.7)은 SEAL 이, 구현은 BUILD 가 한다. `conditions_digest` · `locked_at` 은 봉인 때 채운다. 계약 경로는 Step 0.5 로 선점했다(`RESERVED`)
- 측정 해소: SK-01 · AR-02 · AR-03 · AR-05 · SC-01 · AR-06 — 파일을 읽는 도우미의 출력 줄 글자가 판정이다. 시작 판 값과 사본에 나쁜 예를 넣은 양성 대조가 봉인 전 실측 표에 있다
- 측정 해소: ER-01 · ER-02 · ER-05 — 저장소 밖 파일을 사본 · 목록과 맞대는 도우미 출력이다. 알려진 답(손으로 만든 모의 폴더 열한 파일 · 서른넷 사본)으로 도우미가 살아 있음을 봉인 전에 돌렸다.
  `verify-feedback.sh` 는 `cross_diagnosis_by` 값을 재지 않는다 — 사본에 `cross_diagnosis_by: bogus` 를 넣어도 `PASS` 다(REVIEW 실측). 그 값은 `fbx.py` 의 `by=17` 만이 잰다.
  `verify-feedback.sh` 반복의 17 은 스키마 · 저장 형식이 깨지지 않았다는 증거일 뿐이다
- 측정 해소: ER-03 · AR-01 · AR-07 · AR-08 · AR-09 · RE-01 · RE-02 · DG-01 · DG-03 — 커밋 기록 · 개정 파일 글자 · 봉인 검증 함수를 실제로 돌린 출력이다
- 측정 해소: ER-04 · DG-02 · DG-04 · DG-05 · AP-01 · AP-03 — 검사 스크립트 · 린터 · 브라우저를 실제로 돌린 출력이다
- 커버리지 해소: 모든 조건 — 산문의 파일 · 페이지 이름은 도우미 안 목록(`PAIRS` · `TOKENS` · `SLUGS` · `WANT` · `MISS` · `LEVEL` · `NOH` · `MDS` · `PHASES` · `FN` · `MT` · `MEMO_IDS`)이고 측정은 `"$K/…"` 로 부른다.
  검출기는 공백 든 코드 조각 안의 인자를 읽지 못한다
- 커버리지 해소: SC-01 — `.harness/.meta/kaizen-0924/release-plan.md` 는 측정의 `"$T/E/$PLAN"`(공통 정의 `PLAN`)이다. `plugin.json` · `marketplace.json` 은 `plan.py` 가 `git log -- '*/.claude-plugin/plugin.json' .claude-plugin/marketplace.json` 으로 세어 `bumped` 로 낸다.
  근거 칸 꼴 `.harness/.meta/kaizen-0924/<파일>.md` 는 `plan.py` 의 `rows` 식(`\.harness/\.meta/kaizen-0924/[\w-]+\.md`)이 읽고 그 파일이 있는지 `basis` 로 센다
- 커버리지 해소: ER-01 — `verify-feedback.sh` 는 측정의 `harness/scripts/verify-feedback.sh` 이고, `$FBK/evaluator/` 는 Given 전제로 `fbx.py` 둘째 인자 `"$FBK"` 가 읽는다
- 커버리지 해소: AR-03 — `docs/` HTML 목록은 `docs.py` 의 `html_added` · `html_removed`, `docs/index.html` 은 측정의 `git diff --numstat "$B" "$END" -- docs/index.html` · `navver.py` 가 읽는 `"$T/E/docs/index.html"` · `my | grep -cxF docs/index.html`, `docs.py` 는 `"$K/docs.py"` 다.
  harness 다섯 항목 id(`skill-design` · `agent-design` · `contract-design` · `qa-evaluation` · `contract-schema`)는 `navver.py` 의 `WANT` 표에, 그 다섯 페이지 파일 이름과 판 번호는 `titlever.py` 의 `W` 표에 있다
- 커버리지 해소: AR-04 — 다섯 파일은 `logs.py` 의 `WANT` 표에 글자 그대로 있다(`docs/kaizen/changelog.md` · `docs/kaizen/flutter-changelog.md` · `docs/kaizen/research-log.md` · `docs/kaizen/flutter-research-log.md` · `docs/design/research-log.md`).
  per-kit 연구 기록 여섯은 측정의 `for k in backend infra rust react flutter planning` 반복이 `"$T/E/docs/$k/research-log.md"` 로 읽는다
- 커버리지 해소: AR-07 — `append-audit-log.py` 머리 줄과 `.claude/skills/kaizen-orchestrator/SKILL.md` 는 `audit.sh` 의 `generated` · `manual_orch` 가 붙은 부분에서 찾는다.
  두 후속 notes 이름은 `audit.sh` 의 `FN`, 메타 이슈 글자(`kaizen-state.yaml` · `check-insights-tracking.py` · `append-audit-log.py:148` 등)는 `MT` 배열이 붙은 부분에서 찾는다
- 커버리지 해소: AR-09 — 허용 경로(`.harness/` · `docs/kaizen/` · `docs/design/research-log.md` · `CLAUDE.md` · `docs/index.html`)는 `range.sh` 의 `ALLOW` 정규식, 금지 경로(`.github/` · `.claude-plugin/` · `.claude/skills/`)는 `forbidden` 의 `git log -- …` 경로 목록이다
- 기능 조건 18 · 전체 조건 줄 26 (Step 6.2 두 명령으로 센 값)

### 입력 표 — 항목마다 처리

처리 칸: `조건 <ID>` · `확인만 — <근거>` · `다른 계약 — <슬러그>` · `고치지 않음 — <이유>`. `고치지 않음` 인 ID 는 notes `## 다음 사이클 메모` 와 감사 기록에 옮긴다(AR-07 · AR-08).

| ID | 출처 | 항목 | 처리 |
| -- | ---- | ---- | ---- |
| FN-01 | 러닝북 「계약 셋과 범위」 | Final 은 두 followups 뒤에 시작 | 확인만 — 두 followups QA 리포트 `Verdict: APPROVE` · `Iteration: 1` (2026-09-25 17:24 · 18:15) |
| FN-02 | 러닝북 「버전」 | 버전을 올리지 않고 `release-plan.md` 에 단계를 적는다 | 조건 SC-01 |
| FN-03 | 러닝북 「교차 진단 기록」 첫 줄 | 평가자 피드백 `pending-parent` → `sprint-contract` + 결론 | 조건 ER-01 |
| FN-04 | 러닝북 「교차 진단 기록」 둘째 줄 | DG-02 Phase 개정 파일에 「교차 진단 뒤 Final 에서 고침 — sha」 | 조건 ER-03 |
| FN-05 | 러닝북 「처리 배정표 닫기」 | 대상 계약 · QA · 미반영 비고 · 검사기 종료 코드 | 조건 AR-02. NO_CHANGE Phase 는 없다(열일곱 모두 커밋 · QA) |
| FN-06 | 러닝북 「문서 사이트」 | 기준 `390dea8` · 대응 HTML 있는 원본만 · 부분 패치 금지 | 조건 AR-03 · DG-04 |
| FN-07 | 러닝북 「새 기록 항목을 쓸 때」 | 날짜 붙인 소제목 · 규칙별 경고 비교 | 조건 AR-04 · DG-02 |
| FN-08 | 러닝북 「Codex 독립 검토」 끝 줄 | followups 가 고치지 않은 것을 감사 기록 · 다음 사이클 메모로 | 조건 AR-07 · AR-08 |
| FN-09 | final-todo P1 첫 줄 | P1 개정 파일에 `end_sha: 76cfb37…` · ER-04 셋째 · AR-04 ② 재측정 | 조건 ER-03 (`p1_remeasure=0 0`) |
| FN-10 | final-todo P1 둘째 줄 | SK-01 측정이 핵심 문장 삭제를 못 잡음 → 계약 피드백 | 조건 ER-02 (P1 `SK-01`) |
| FN-11 | final-todo P1 셋째 줄 | QA 리포트 `:39` 대조 실행 주장 → 평가자 피드백 | 조건 ER-01 (P1 `:39`) |
| FN-12 | final-todo P1 계약 밖 1 · 2 | 「없음 — 이유」 폭 · ultracode 동시 20 | 확인만 — harness followups SK-05 (가)(나) 가 고쳤다(`e4692cb`) |
| FN-13 | final-todo 모든 Phase 공통 | Phase 2 이후 notes 뒤 `end_sha` 덧붙임 확인 | 조건 ER-03 — 시작 판 실측: P2 ~ P17 notes 커밋이 모두 마지막 `end_sha` 와 같다(`amend.sh` `kept=16`) |
| FN-14 | final-todo 카이젠 진행 스킬 문서 | Phase 17 · 범위 수 · 동시 실행 수 | 확인만 — harness followups SK-01 (`66b4e4c`) |
| FN-15 | final-todo P2 · xdiag P2 (2) | ER-01 · ER-03 둘째 · AR-06 측정 결함 | 조건 ER-02 (P2 `ER-01`) |
| FN-16 | final-todo P2 계약 밖 1 | `<base>..$(sprint_head <slug>)` | 확인만 — harness followups ER-06 |
| FN-17 | final-todo P2 계약 밖 2 | `Evaluated` 가 `date` 출력 아님 | 평가자 저장 절차는 harness followups ER-04 가 고쳤다. 기록은 조건 ER-01 (P2 `Evaluated`) |
| FN-18 | final-todo P3 · xdiag P3 (2) | DG-05 (b)(c) · AR-06 ③ · `assertions.json` 제목만 | 조건 ER-01 (P3 `DG-05`) · ER-02 (P3 `AR-06`). 실행기는 고치지 않음 — F1H-14 · F1H-84 다음 사이클 |
| FN-19 | final-todo P3 계약 밖 · 작은 것 | `--no-renames` · 16 행 · 「위 (c)」 · `:671` | 확인만 — harness followups ER-05 · SK-05 (다)(라) · F1H-19 |
| FN-20 | final-todo 여러 Phase 첫째 | DG-02 뜻 기준 FAIL (P7 · P8 · P9 · P11) · P12 ~ 17 전수 | 구현은 kit followups SK-01. 기록은 조건 ER-01 · ER-02 · ER-03 |
| FN-21 | final-todo 여러 Phase 둘째 | 옛 값 검사 `SOURCE_DIRS` | 확인만 — harness followups ER-07 (389 파일) |
| FN-22 | final-todo 여러 Phase 셋째 | 마지막 `end_sha` 커밋이 구조상 범위 밖 — 한 번에 센다 | 조건 ER-03 (`after=16 after_other=0`) |
| FN-23 | final-todo 여러 Phase 넷째 | QA 리포트 요약 수 오기 (P4 · P6 · P7 · P10 · P14) | 조건 ER-01 (P4 · P6 · P14 `N/A` · P7 · P10 결론) |
| FN-24 | final-todo 여러 Phase 다섯째 | V 줄에 FAIL 이 안 찍힘 | 확인만 — harness followups ER-08 |
| FN-25 | final-todo P4 ~ P10 계약 밖 | 커밋 훅 이름 바꾸기 · 킷 결함 | 확인만 — harness followups ER-01 · kit followups SK-02 ~ SK-05 |
| FN-26 | final-todo · kit followups 14 행 | P6 RE-02 정규식 하이픈 | 조건 ER-02 (P6 `RE-02`) |
| FN-27 | final-todo P12 ~ 17 | CI 줄 · 킷 결함 | 확인만 — harness followups AR-02 · kit followups SK-06 ~ SK-11 |
| FN-28 | 오케스트레이터 F1 1 | 교차 Phase 정합 조건(Phase 1 반영 · P2 ↔ P3 · P4 vs 5 ~ 17 · tone 강도 · tone 트리거 · api-kit 결정 · 버전 · changelog · research-log · `bash -n`) | 조건 SK-01 (여섯) · SC-01 (버전) · AR-04 (기록) · DG-05 (`scope-isolation`) |
| FN-29 | 오케스트레이터 F1 2 | 처리 배정표 닫기 | 조건 AR-02 |
| FN-30 | 오케스트레이터 F1 3 | Final QA | 이 계약의 QA — 범위 밖(다음 단계) |
| FN-31 | 오케스트레이터 F2 | 문서 사이트 재생성 · `docs/index.html` 에 갱신 페이지 등록(넷째 줄) · `validate-plugin.py` OK | 조건 AR-03 (첫 화면은 harness 다섯 제목 판 번호 — `nav_ver=5/5`) · DG-04 · DG-05 |
| FN-32 | 오케스트레이터 F3 | 피드백 정리 · 정리 기록 | 조건 ER-05 (지우지 않고 옮긴다 — 위 경계 줄) |
| FN-33 | 오케스트레이터 F3.5 | 메모리 승격 후보 파일 · 원장 불가침 | 조건 AR-06 |
| FN-34 | 오케스트레이터 F4 1 | 버전 올리기 | 조건 SC-01 (계획으로 대신) |
| FN-35 | 오케스트레이터 F4 2 · 3 | changelog · research-log · per-kit 연구 기록 여섯 · 출처 URL 5 건 | 조건 AR-04 (다섯 파일 · 연구 기록 셋 URL 5 개 이상 · per-kit 여섯은 확인만) |
| FN-36 | 오케스트레이터 F4 4 | evals 점검 기록 | 조건 AR-05 |
| FN-37 | 오케스트레이터 F4 5 | 실패 횟수 `phase_1` ~ `phase_17` · `last_updated` | 조건 AR-05 — 열일곱 모두 1 회차 APPROVE 라 0 |
| FN-38 | 오케스트레이터 F4 6 | Post-Kaizen Checklist | 조건 DG-05 (`validate-post-kaizen.py` PASS 13 · SKIP 둘은 버전 두 줄) |
| FN-39 | 오케스트레이터 F4 7 | PR 생성 | 고치지 않음 — 이 계약 밖. Final QA 뒤 부모가 사용자 규칙(푸시는 사용자가 요청할 때만)대로 |
| FN-40 | 오케스트레이터 연동 스크립트 | `append-audit-log.py` 로 감사 기록 | 조건 AR-07 · RE-02 |
| FN-41 | phase1-notes §Final | 문서 사이트 두 페이지 · research-templates `:28` · 버전 | 페이지는 조건 AR-03, `:28` 은 확인만 — harness followups SK-02, 버전은 SC-01 |
| FN-42 | phase2-notes §Final | 문서 사이트 · 서명 줄 규약을 러닝북 · 오케스트레이터가 가리키게 | 페이지는 조건 AR-03. 오케스트레이터는 확인만 — harness followups SK-01. 러닝북은 레포 밖 작업 파일 |
| FN-43 | phase3-notes §넘기는 것 | `ci.yml` 실행기 줄 · 평가 가이드 페이지 · harness minor | 실행기 줄은 고치지 않음 — 실행기가 없다(F1H-14). 페이지는 AR-03, 단계는 SC-01 |
| FN-44 | phase4-notes §넘기는 것 | 검증 가이드 페이지 · harness minor | 조건 AR-03 · SC-01 |
| FN-45 | phase5-notes §넘기는 것 | flutter changelog · research-log · 버전 · 페이지 넷 | 조건 AR-04 · SC-01 · AR-03 |
| FN-46 | phase6-notes §넘기는 것 | README 버전 줄 · design 연구 기록 · 버전 · 페이지 | README 는 확인만 — kit followups SK-03 (c). 나머지 조건 AR-04 · SC-01 · AR-03 |
| FN-47 | phase7-notes §넘기는 것 | 페이지 둘 · `stale-values.yaml` OpenAPI · 버전 | 조건 AR-03 · ER-04 · SC-01 |
| FN-48 | phase8-notes §넘기는 것 | 페이지 셋 · `stale-values.yaml` 등록 여부 · 버전 | 조건 AR-03 · ER-04 · SC-01 |
| FN-49 | phase9-notes §넘기는 것 | `sqlx-patterns.html` · rust-preflight · rust-model 페이지 · 버전 | 조건 AR-03 · SC-01. rust-preflight · rust-model 페이지는 없다(`docs/rust-kit/` 목록) — 만들지 않는다 |
| FN-50 | phase10-notes §넘기는 것 | `ci.yml` · 버전 · 규약 페이지 | CI 는 확인만 — harness followups AR-02. 나머지 조건 SC-01 · AR-03 |
| FN-51 | phase11-notes §넘기는 것 | 페이지 셋 · 버전 | 조건 AR-03 · SC-01 |
| FN-52 | phase12-notes §넘기는 것 | 버전 · 페이지 · `ci.yml` · 평가자 Step 3.4 · 설치본 확인 | 조건 SC-01 · AR-03(`schema.html` · `design.html`, digest · kaizen 페이지는 없다). CI · Step 3.4 는 확인만 — harness followups AR-02 · ER-03. 설치본 Stop 훅 확인은 배포 뒤라 SC-01 이 계획 파일에 확인 줄로 남긴다 |
| FN-53 | phase13-notes §넘기는 것 | 페이지 · 버전 | 조건 AR-03 · SC-01 |
| FN-54 | phase14-notes §넘기는 것 | CI · 예제 · 예제 페이지 · onboarding-kaizen · 버전 · 페이지 셋 · 드리프트 | 예제 · CI · 스킬 · 드리프트는 확인만 — kit followups SK-08 (c) · harness followups AR-02 · SK-03 · AR-01. 조건 AR-03 · SC-01 |
| FN-55 | phase15-notes §넘기는 것 | 페이지 둘 · tone-kaizen · research-templates · 버전 | 조건 AR-03 · SC-01. 스킬 둘은 확인만 — harness followups SK-02 · SK-03 |
| FN-56 | phase16-notes §넘기는 것 | 설계 문서 `:249` · 오케스트레이터 `:567` · 페이지 여섯 · 드리프트 · 버전 | 설계 문서는 고치지 않음 — `docs/superpowers/` 는 세 Final 계약 어느 범위에도 없다(F1H-67 · F1K-56). 오케스트레이터 · 드리프트는 확인만 — harness followups SK-01 · AR-01. 조건 AR-03 · SC-01 |
| FN-57 | phase17-notes §넘기는 것 | CI · howto-kaizen `:26` · `overview.html` · 버전 | CI · 스킬은 확인만 — harness followups AR-02 · SK-03. 조건 AR-03 · SC-01 |
| FN-58 | Phase notes 열일곱 §다음 사이클 메모 | 각 Phase 다음 사이클 메모 | 고치지 않음 — Phase 가 다음 사이클로 보낸 것. 감사 기록이 notes 경로 열일곱을 가리킨다(AR-07 `notes=17/17`) |
| FN-59 | f1-harness-followups-notes §넘기는 것 | 버전 patch 제안 | 조건 SC-01 — harness 는 Phase 3 · 4 가 minor 라 큰 쪽 minor |
| FN-60 | 같은 notes | 문서 사이트 여섯 페이지 | 조건 AR-03 |
| FN-61 | 같은 notes | 교차 진단 기록(F1H-01 · 02 · 03 · 10 · 95) | 조건 ER-01 · ER-02 · ER-03 |
| FN-62 | 같은 notes §다음 사이클 메모 | 고치지 않음 스물아홉(F1H-14 ~ F1H-94) · 구현 중 새로 찾은 넷(F1H-N1 ~ N4) | 조건 AR-07 (`f1h=29/29 new4=4/4`) |
| FN-63 | 같은 notes · 입력 표 F1H-45 | `stale-values.yaml` 새 항목 · allow | 조건 ER-04 |
| FN-64 | 같은 notes F1H-79 | backend-kit 세 줄 allow 뒤 `EXCLUDED_KITS` 해제 | allow 반쪽은 조건 ER-04 (`unexcluded=0 0`). 해제는 고치지 않음 — `scripts/` 범위 밖, 다음 사이클 |
| FN-65 | f1-kit-followups-notes (a) | Phase 7 · 8 · 9 · 11 개정 파일 줄 넷 | 조건 ER-03 |
| FN-66 | 같은 notes (b) | 킷 열둘 patch | 조건 SC-01 — Phase 판정과 합쳐 큰 쪽(howto-kit 만 patch) |
| FN-67 | 같은 notes (c) | 페이지 아홉 | 조건 AR-03 (아홉 모두 페이지 표에 있음) |
| FN-68 | 같은 notes (d) | OpenAPI allow · design 연구 기록 | 조건 ER-04 · AR-04 |
| FN-69 | 같은 notes (e)(f) | changelog · 킷 로그 단락 | 조건 AR-04 |
| FN-70 | 같은 notes §고치지 않은 항목 | 서른셋(F1K-10 ~ F1K-80) | 조건 AR-07 (`f1k=33/33`) |
| FN-71 | 러닝북 「Codex 독립 검토」 | Codex 지적을 고치지 않는다 | 확인만 — 두 followups 가 조건 · 고치지 않음으로 처리했고 고치지 않은 것은 FN-62 · FN-70 |
| FN-72 | 편집 전 감사 (입력 밖) | `kaizen-state.yaml` 옛 사이클 → 사후 점검 날짜 검사 다섯이 옛 항목으로 통과 | 조건 AR-05 · DG-05 |
| FN-73 | 편집 전 감사 (입력 밖) | 피드백 639 개 > 500 | 조건 ER-05 |
| FN-74 | 편집 전 감사 (입력 밖) | `CLAUDE.md` 카이젠 세 줄이 10 Phase · Phase 15 | 조건 SK-02 |
| FN-75 | 편집 전 감사 (입력 밖) | 매핑 표 밖 원본의 같은 이름 페이지 열 | 조건 AR-03 (페이지 표 (다)) |
| FN-76 | 편집 전 감사 (입력 밖) | 검사기가 슬러그 형식만 봄 | 조건 AR-02 가 번호 ↔ 슬러그를 따로 잰다. 검사기 고치기는 고치지 않음 — `scripts/` 범위 밖, 다음 사이클 |
| FN-77 | 편집 전 감사 (입력 밖) | 두 followups 평가자 피드백도 `pending-parent` | 고치지 않음 — 교차 진단 전문이 P1 ~ P17 뿐이다. 부모가 두 followups 교차 진단을 돌리면 그때 갱신 — 다음 확인 항목 |
| FN-78 | 편집 전 감사 (입력 밖) | `append-audit-log.py` 고정 소제목 MD024 · 끝 빈 줄 없음 | DG-02 예외 한 줄 · 빈 줄은 BUILD 가 먼저 붙인다. 스크립트 고치기는 고치지 않음 — 범위 밖, 다음 사이클(소제목에 날짜) |
| FN-79 | 편집 전 감사 (입력 밖) | css-tokens 매핑 표에 howto-kit accent 없음 | 고치지 않음 — `.claude/skills/docs-site/` 범위 밖, F1H-91 과 함께 다음 사이클. 이번 페이지는 기존 `#F59E0B` 그대로 |
| FN-80 | 편집 전 감사 (입력 밖) | `docs/process/kaizen-flow.html` 이 9-Phase | 고치지 않음 — 원본이 F2 표에 「내부 문서」 뿐이라 특정할 수 없고 이번 사이클 변경 탓이 아니다. 다음 사이클 docs-site 매핑 결정과 함께 |

## 회귀 게이트 — 측정 공통 정의 · 도우미 · 봉인 전 실측

모든 조건의 측정은 공통 정의 블록(`common.sh`)을 먼저 읽은 **bash** 셸에서 돈다 — 블록과 측정을 한 `bash -c` 안에 넣거나 블록을 파일로 저장해 `. 파일` 뒤에 잇는다.
`END_UNRESOLVED` 가 찍히면 셸이 종료 코드 2 로 끝난다. HEAD 로 바꿔 재지 않는다. 셸 함수에 기대는 측정 앞에는 `type <함수> >/dev/null || exit 2` 를 둔다.

도우미 준비 — 이 절의 bash · python 코드 블록은 각 블록 첫 `#` 주석 줄(셔뱅 다음)에 적힌 이름 그대로 한 폴더에 저장하고, 그 폴더를 공통 정의를 읽기 전에 `K` 에 넣는다. 떼는 명령:

```bash
# 이 계약에서 도우미 블록을 떼어 $K 에 저장한다 — 블록 첫 주석 줄의 이름(셔뱅 다음 줄)이 파일 이름이다
K=${K:?도우미 폴더}; mkdir -p "$K"
python3 - .harness/sprint-contract-kaizen-0924-final.md "$K" <<'PY'
import re, sys, pathlib
src = open(sys.argv[1], encoding="utf-8").read(); K = pathlib.Path(sys.argv[2])
for body in re.findall(r"^```(?:bash|python)\n(.*?)^```$", src, re.S | re.M):
    lines = body.splitlines(); i = 1 if lines and lines[0].startswith("#!") else 0
    m = re.match(r"# ([\w.-]+\.(?:sh|py)) ", lines[i]) if len(lines) > i else None
    if m:
        (K / m.group(1)).write_text(body, encoding="utf-8")
PY
# mdcmp.sh 옆에 markdownlint 와 설정 — 편집기 확장과 같은 조건(MD013 끔)
ln -sfn /private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/de8c7935-a5b6-4df5-9106-fafa73c288a0/scratchpad/p1build/node_modules "$K/node_modules"
printf '{ "config": { "MD013": false } }\n' >"$K/cfg.markdownlint-cli2.jsonc"
```

준비 단계 실측(2026-09-25): `$K/node_modules/.bin/markdownlint-cli2 --version` 첫 줄 `markdownlint-cli2 v0.23.2 (markdownlint v0.41.1)` — 없으면 그 폴더에서 `npm install --no-save markdownlint-cli2@0.23.2` 부터 ·
`command -v actionlint` → `/opt/homebrew/bin/actionlint` · `command -v dash` → `/bin/dash` · `command -v node` → fnm 셸 경로(`node --version` `v24.14.1`), 작업 폴더에 `node_modules/playwright-core` 있음 ·
`python3 -c 'import yaml'` 성공 · `git --version` 2.53.0. `node scripts/check-docs-a11y.js` 는 작업 폴더에서 부르고 인자로 `$T/E` 아래 페이지 경로를 넘긴다(스크래치 경로 페이지로 돌려 확인).
도우미 스물여섯 가운데 `fbedit.py` · `cleanup-do.py` 는 BUILD 가 쓰는 구현 도구이고 나머지는 측정 도구다.

측정이 기대는 공통 정의 이름: `B` · `CB` · `DB` · `SIG` · `CF` · `AM` · `NOTES` · `REVIEW` · `FB` · `PLAN` · `MEM` · `EVA` · `SP` · `FBD` · `FBK` · `ARCH` · `FBLIST` · `END` · `T/B` · `T/E` ·
`mine` · `unsigned_on` · `my` · `fm_get` · `sha256_16` · `contract_digest` · `verify_seal` · `PHASES` · `FOLLOWUPS` · `MDS` · `added_md`.

측정 공통 정의 — 두 판을 풀고 이 계약 커밋 · 봉인 · 경로 이름을 정의한다:

```bash
# common.sh — 측정 공통 정의. bash 로 실행한다 (zsh 는 배열 첨자가 1 부터이고 `$ref:a` 를 수식어로 읽는다)
export LC_ALL=C.UTF-8
cd /Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/kaizen-0924 || exit 2
B=511f19b5823886bef5c21dadcd656a692f298db5    # 이 계약 시작 HEAD
CB=83cfb4f311d6497186da13c75bdb8f8a108481b3   # 사이클 가지가 main 에서 갈라진 커밋 (사이클 전체를 재는 기준)
DB=390dea8                                    # 문서 사이트 기준 (러닝북 F2)
SIG='Kaizen-Phase: kaizen-0924-final'
CF=.harness/sprint-contract-kaizen-0924-final.md
AM=.harness/sprint-amendments-kaizen-0924-final.md
NOTES=.harness/.meta/kaizen-0924/final-notes.md
REVIEW=.harness/.meta/kaizen-0924/final-review.md
FB=.harness/sprint-feedback-kaizen-0924-final.md
PLAN=.harness/.meta/kaizen-0924/release-plan.md
MEM=.harness/.meta/memory-promotion-candidates-2026-09-24.md
EVA=.harness/.meta/evals-audit-2026-09-24.md
SP=/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/de8c7935-a5b6-4df5-9106-fafa73c288a0/scratchpad/kaizen
FBD=$HOME/.harness/feedback                        # 전역 피드백 경로 (harness/scripts/feedback-path.sh 출력)
FBK=$SP/final-fb-before                            # 교차 진단 기록 전 사본 — BUILD 가 고치기 전에 만든다
ARCH=$HOME/.harness/feedback-archive/kaizen-2026-09-24   # 500 개 초과분을 옮기는 곳 (지우지 않는다)
FBLIST=$SP/final-fb-before-cleanup.txt             # 정리 직전 목록 "mtime<TAB>상대 경로" — BUILD 가 옮기기 전에 만든다
END=$( [ -f "$AM" ] && sed -n 's/^end_sha:[[:space:]]*//p' "$AM" | tail -1 )
if [ -z "$END" ] || ! git rev-parse -q --verify "$END^{commit}" >/dev/null; then
  echo "END_UNRESOLVED — 측정을 멈추고 BUILD 에 묻는다. HEAD 로 바꿔 재지 않는다"; exit 2
fi
: "${K:?도우미 폴더를 K 에 넣는다}"
T=$(mktemp -d "${TMPDIR:-/tmp}/kfinal.XXXXXX") || exit 2
trap 'rm -rf "$T"' EXIT
mkdir -p "$T/B" "$T/E"
# 두 판을 풀어 두고 거기서 잰다 — 작업 폴더의 미커밋 변경이 끼지 않는다
git archive "$B" | tar -x -C "$T/B" || exit 2
git archive "$END" | tar -x -C "$T/E" || exit 2
mine() { git log --format= --name-only "${1}..${2}" --grep="^${3}\$" | grep . | LC_ALL=C sort -u; }
unsigned_on() { _b=${1}; _u=${2}; _s=${3}; shift 3
  git log --format=%H "${_b}..${_u}" -- "$@" | while read -r _c; do git log -1 --format=%B "$_c" | grep -qxF "$_s" || echo "$_c"; done; }
my() { mine "$B" "$END" "$SIG"; }
fm_get() { awk -v k="^$2:[[:space:]]*" 'NR==1 && /^---[[:space:]]*$/ { fm=1; next } fm && /^---[[:space:]]*$/ { exit } fm && $0 ~ k { sub(k, "", $0); print; exit }' "$1" | sed -e "s/[[:space:]]*$//" -e "s/^['\"]//" -e "s/['\"]\$//"; }
sha256_16() { if command -v sha256sum >/dev/null 2>&1; then sha256sum; elif command -v shasum >/dev/null 2>&1; then shasum -a 256; else python3 -c 'import hashlib,sys; print(hashlib.sha256(sys.stdin.buffer.read()).hexdigest())'; fi | cut -c1-16; }
contract_digest() { grep -E '^- \[[ x]\] [A-Z]{2,}-[0-9]{2}' "$1" | sed -E 's/^- \[[ x]\]/- [ ]/' | sha256_16; }
verify_seal() { rec=$(fm_get "$1" conditions_digest); rec=${rec#sha256:}; if [ -z "$rec" ]; then echo "SEAL_ABSENT $1"; return 0; fi
  act=$(contract_digest "$1"); if [ "$rec" = "$act" ]; then echo "SEAL_OK $1"; else echo "SEAL_BROKEN $1 recorded=$rec actual=$act"; fi; }
# 17 Phase 슬러그 — 번호 차례
PHASES=(kaizen-0924-p01-guides kaizen-0924-p02-contract kaizen-0924-p03-evaluator kaizen-0924-p04-harness
  kaizen-0924-p05-flutter-toolkit kaizen-0924-p06-design-kit kaizen-0924-p07-backend-kit kaizen-0924-p08-infra-kit
  kaizen-0924-p09-rust-kit kaizen-0924-p10-react-kit kaizen-0924-p11-planning-kit kaizen-0924-p12-reflect-kit
  kaizen-0924-p13-bambu-kit kaizen-0924-p14-onboarding-kit kaizen-0924-p15-tone-kit kaizen-0924-p16-api-kit
  kaizen-0924-p17-howto-kit)
FOLLOWUPS=(kaizen-0924-f1-harness-followups kaizen-0924-f1-kit-followups)
# 이 계약이 쓰는 마크다운 열여덟 (새 파일 · 개정 파일 포함) — DG-02 · AP-01 · AP-03 이 파일마다 잰다
MDS=(docs/kaizen/changelog.md docs/kaizen/research-log.md docs/kaizen/flutter-changelog.md docs/kaizen/flutter-research-log.md
  docs/design/research-log.md CLAUDE.md .claude/kaizen-input/insights-report.md .harness/.meta/orchestrator-audit-log.md
  "$NOTES" "$PLAN" "$MEM" "$EVA" "$AM"
  .harness/sprint-amendments-kaizen-0924-p01-guides.md .harness/sprint-amendments-kaizen-0924-p07-backend-kit.md
  .harness/sprint-amendments-kaizen-0924-p08-infra-kit.md .harness/sprint-amendments-kaizen-0924-p09-rust-kit.md
  .harness/sprint-amendments-kaizen-0924-p11-planning-kit.md)
added_md() { for f in "${MDS[@]}"; do git diff --no-index -U0 "$T/B/$f" "$T/E/$f" 2>/dev/null; if [ ! -f "$T/B/$f" ] && [ -f "$T/E/$f" ]; then sed 's/^/+/' "$T/E/$f"; fi; done | grep '^+' | grep -v '^+++'; }
```

교차 Phase 정합 (SK-01):

```bash
#!/usr/bin/env bash
# f1.sh <판 폴더> — 교차 Phase 정합 넷을 한 판에서 잰다. 출력 네 줄은 notes `## F1 정합` 표에 글자 그대로 옮긴다
#  p1hand  — Phase 1 이 넘긴 여덟 자리: 앞 여섯은 옛 문구 수(0 이어야 함), 뒤 둘은 새 칸 「시도한 우회」 수(1 이상)
#  parity  — 평가 가이드 `Parity with` · `Schema link` 가 세 가이드 머리 version · 스키마 현재 판과 글자 그대로 같은가
#  apikit  — api-kit 확정 결정 일곱 글자 수(각 1 이상)
#  orch16  — 오케스트레이터 Phase 16 추가 지시의 확정 결정 다섯 글자 수(각 1)
R=${1:?판 폴더}
c() { if [ -f "$R/$1" ]; then grep -cF -- "$2" "$R/$1"; else echo MISSING; fi; }
printf 'p1hand=%s %s %s %s %s %s %s %s\n' \
  "$(c harness/skills/sprint/SKILL.md '`[미검증]` + 사유 한 줄')" \
  "$(c harness/skills/create-agent/SKILL.md '15 종')" \
  "$(c harness/skills/create-skill/SKILL.md '1500-2000 words')" \
  "$(c react-kit/references/render-evidence-protocol.md '`[미검증]` 마커와 사유 한 줄')" \
  "$(c flutter-toolkit/references/visual-evidence-protocol.md '`[미검증]` 마커 + 사유 한 줄')" \
  "$(c onboarding-kit/skills/setup-guide/SKILL.md '마커 + 사유 한 줄')" \
  "$(c infra-kit/skills/infra-test/SKILL.md '시도한 우회')" \
  "$(c rust-kit/agents/rust-reviewer.md '시도한 우회')"
v() { awk '/^---$/{n++; next} n==1 && /^version:/{sub(/^version:[[:space:]]*/,""); print; exit}' "$R/harness/docs/guides/$1.md"; }
S=$(v skill-design-guide); A=$(v agent-design-guide); C=$(v contract-design-guide)
SC=$(sed -n 's/^현재: \*\*\(v[0-9.]*\)\*\*.*/\1/p' "$R/harness/references/contract-schema.md")
QG=$R/harness/docs/guides/qa-evaluation-guide.md
printf 'parity=%s %s\n' \
  "$(grep -cxF -- "- **Parity with**: skill-design-guide $S · agent-design-guide $A · contract-design-guide $C" "$QG")" \
  "$(grep -cF -- "- **Schema link**: contract-schema.md $SC " "$QG")"
AC=api-kit/skills/api-contract/SKILL.md; AV=api-kit/skills/api-verify/SKILL.md
printf 'apikit=%s %s %s %s %s %s %s\n' \
  "$(c $AC "\`pin\` 은 '값 고정' 이 아니다 — 경로별 명시 assertion 이다.")" \
  "$(c $AC '`exact` 는 본문만 본다. 헤더는 diff 대상 0개다.')" \
  "$(c $AC '독립 샘플 `>=3`')" \
  "$(c $AV '기본 허용 메서드는 `GET`/`HEAD`/`OPTIONS` 뿐이고')" \
  "$(c $AV '| `3` | 런타임 오류 (DNS/TLS/connect/timeout) | **환경 실패** |')" \
  "$(c $AV '| `4` | assert 실패 | **계약 실패** |')" \
  "$(c $AC '비교 기준선은 JCS 이고')"
OS=.claude/skills/kaizen-orchestrator/SKILL.md
printf 'orch16=%s %s %s %s %s\n' \
  "$(c $OS '`exact` 는 **본문만** 본다')" \
  "$(c $OS 'enum 승격은 **3 샘플 이상**')" \
  "$(c $OS 'prod 기본 동사는 **GET/HEAD/OPTIONS**')" \
  "$(c $OS '비교 기준선은 **RFC 8785 JCS**')" \
  "$(c $OS '계약 실패와 환경 실패는 **exit code 로 구분**한다')"
```

```python
#!/usr/bin/env python3
# tonegrade.py <옛 판 폴더> <새 판 폴더> — tone-kit/references 규칙 표의 강도가 옛 판보다 오른 규칙을 센다.
# 강도 차례는 관측 컨벤션 < SHOULD < MUST. 규칙 표 행을 하나도 못 읽으면 종료 코드 2 (빈 표를 통과로 세지 않는다)
import re, sys
from pathlib import Path
RANK = {"관측 컨벤션": 0, "SHOULD": 1, "MUST": 2}
ROW = re.compile(r"^\|\s*([A-Z]{1,2}-\d{2})\s*\|.*?\|\s*(관측 컨벤션|SHOULD|MUST)\s*\|")
def grades(root):
    g = {}
    for p in sorted((Path(root) / "tone-kit/references").glob("*.md")):
        for line in p.read_text(encoding="utf-8").splitlines():
            m = ROW.match(line)
            if m:
                g.setdefault(m.group(1), set()).add(m.group(2))
    return g
old, new = grades(sys.argv[1]), grades(sys.argv[2])
if not old or not new:
    print(f"UNREADABLE rules_old={len(old)} rules_new={len(new)}"); sys.exit(2)
top = lambda s: max(RANK[x] for x in s)
up = [(k, sorted(old[k]), sorted(new[k])) for k in sorted(new) if k in old and top(new[k]) > top(old[k])]
added = sorted((k, sorted(new[k])) for k in new if k not in old)
print(f"rules_old={len(old)} rules_new={len(new)} raised={len(up)} added={added}")
for u in up:
    print("RAISED", *u)
sys.exit(1 if up else 0)
```

```python
#!/usr/bin/env python3
# toneterms.py [루트] — tone-kit 스킬 설명의 트리거 어휘(따옴표 구문)가 다른 킷 스킬 · 에이전트 설명과
# 같은 말(set intersection)이나 한쪽이 다른 쪽을 품는 말(substring)로 겹치는 쌍을 센다
import json, re, sys
from pathlib import Path
R = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
def desc(p):
    t = p.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---", t, re.S)
    if not m: return ""
    fm = m.group(1)
    d = re.search(r"^description:[ \t]*(?:>-?|\|-?)[ \t]*\n((?:[ \t]+.*(?:\n|$))*)", fm, re.M)
    one = re.search(r"^description:\s*(.+)$", fm, re.M)
    return d.group(1) if d else (one.group(1) if one else "")
def terms(text):
    return {x.strip() for x in re.findall(r"[\"“]([^\"”]{2,40})[\"”]", text)}
kits = [p["source"].lstrip("./") for p in json.loads((R/".claude-plugin/marketplace.json").read_text())["plugins"]]
files = {}
for k in kits:
    base = R/k
    for p in list(base.glob("skills/*/SKILL.md")) + list(base.glob("agents/*.md")):
        files[str(p.relative_to(R))] = terms(desc(p))
tone = {f: t for f, t in files.items() if f.startswith("tone-kit/")}
other = {f: t for f, t in files.items() if not f.startswith("tone-kit/")}
inter = [(a, b, x) for a, ta in tone.items() for b, tb in other.items() for x in ta & tb]
sub = [(a, b, x, y) for a, ta in tone.items() for b, tb in other.items() for x in ta for y in tb if x != y and (x in y or y in x)]
print(f"tone_terms={sum(len(t) for t in tone.values())} other_files={len(other)} other_terms={sum(len(t) for t in other.values())} intersect={len(inter)} substring={len(sub)}")
for r in inter + sub: print("OVERLAP", *r)
sys.exit(1 if inter or sub else 0)
```

```bash
#!/usr/bin/env bash
# synt.sh <판 폴더> <기준 ref> <상한 ref> — 사이클 동안 더하거나 고친 셸 · 파이썬 · JSON · YAML 을 그 판에서 문법 검사한다.
# 셸은 첫 줄 해석기대로(bash → bash -n, /bin/sh → sh -n 과 dash -n). 도구가 없으면 TOOL_MISSING 으로 멈춘다(빈 검사를 0 으로 세지 않는다)
# all_sh — 상한 판에 추적되는 셸 전부(오케스트레이터 F1 「전체 bash -n」). 해석기 줄이 없는 셸은 bash -n 으로 잰다
R=${1:?판}; FROM=${2:?기준}; TO=${3:?상한}
for t in dash actionlint python3; do command -v "$t" >/dev/null || { echo "TOOL_MISSING $t"; exit 2; }; done
L=$(git diff --name-only --diff-filter=AM "$FROM" "$TO")
sh=0; shb=0; py=0; pyb=0; js=0; jsb=0; ym=0; ymb=0
for f in $L; do
  [ -f "$R/$f" ] || continue
  case $f in
    *.sh) sh=$((sh+1)); first=$(head -1 "$R/$f")
      case $first in
        *bash*) bash -n "$R/$f" 2>/dev/null || { shb=$((shb+1)); echo "BAD bash -n $f"; } ;;
        *sh) { sh -n "$R/$f" && dash -n "$R/$f"; } 2>/dev/null || { shb=$((shb+1)); echo "BAD sh/dash -n $f"; } ;;
        *) shb=$((shb+1)); echo "BAD 해석기 줄 없음 $f" ;;
      esac ;;
    *.py) py=$((py+1)); python3 -m py_compile "$R/$f" 2>/dev/null || { pyb=$((pyb+1)); echo "BAD py $f"; } ;;
    *.json) js=$((js+1)); python3 -c 'import json,sys; json.load(open(sys.argv[1],encoding="utf-8"))' "$R/$f" 2>/dev/null || { jsb=$((jsb+1)); echo "BAD json $f"; } ;;
    *.yaml|*.yml) ym=$((ym+1)); python3 -c 'import yaml,sys; yaml.safe_load(open(sys.argv[1],encoding="utf-8"))' "$R/$f" 2>/dev/null || { ymb=$((ymb+1)); echo "BAD yaml $f"; } ;;
  esac
done
ash=0; ashb=0
for f in $(git ls-tree -r --name-only "$TO" | grep '\.sh$'); do
  [ -f "$R/$f" ] || continue; ash=$((ash+1)); first=$(head -1 "$R/$f")
  case $first in
    '#!'*bash*) bash -n "$R/$f" 2>/dev/null || { ashb=$((ashb+1)); echo "BAD all bash -n $f"; } ;;
    '#!'*sh) { sh -n "$R/$f" && dash -n "$R/$f"; } 2>/dev/null || { ashb=$((ashb+1)); echo "BAD all sh/dash -n $f"; } ;;
    *) bash -n "$R/$f" 2>/dev/null || { ashb=$((ashb+1)); echo "BAD all bash -n (해석기 줄 없음) $f"; } ;;
  esac
done
actionlint "$R/.github/workflows/ci.yml" >/dev/null 2>&1; al=$?
echo "sh=$sh sh_bad=$shb py=$py py_bad=$pyb json=$js json_bad=$jsb yaml=$ym yaml_bad=$ymb all_sh=$ash all_sh_bad=$ashb actionlint_rc=$al"
```

교차 진단 기록 (ER-01 · ER-02) — 재는 도구와 BUILD 가 쓰는 편집 도구:

```python
#!/usr/bin/env python3
# fbx.py <전역 피드백 폴더> <고치기 전 사본 폴더> — Phase 17 개의 평가자 · 계약 피드백에 교차 진단 기록이 들어갔는지,
# 기록 두 칸 말고는 사본과 같은지 잰다. 슬러그마다 파일이 정확히 하나가 아니면 그 슬러그는 NG 다(0 개를 통과로 세지 않는다)
import sys, yaml
from pathlib import Path
FBD, FBK = Path(sys.argv[1]), Path(sys.argv[2])
KITS = ["guides", "contract", "evaluator", "harness", "flutter-toolkit", "design-kit", "backend-kit", "infra-kit", "rust-kit",
        "react-kit", "planning-kit", "reflect-kit", "bambu-kit", "onboarding-kit", "tone-kit", "api-kit", "howto-kit"]
SLUGS = [f"kaizen-0924-p{i:02d}-{k}" for i, k in enumerate(KITS, 1)]
# 평가자 피드백에 들어가야 할 글자 — 교차 진단(xdiag-all.md)이 그 Phase QA 를 두고 짚은 것
EVAL_TOK = {1: [":39"], 2: ["Evaluated"], 3: ["DG-05"], 4: ["N/A"], 5: ["SK-09"], 6: ["N/A"], 7: ["DG-02", "154916a"],
            8: ["DG-02", "cc11f71"], 9: ["DG-02", "c4eeef3"], 10: ["strictPort"], 11: ["DG-02", "cfef54f"], 12: ["DG-02"],
            13: ["사용자 교정"], 14: ["N/A"], 15: ["core-antipatterns"], 16: ["판정 불가"], 17: ["펜스"]}
# 계약 피드백에 들어가야 할 글자 — 교차 진단이 찾은 그 계약 측정의 구멍 (없으면 「없음」)
CON_TOK = {1: ["SK-01"], 2: ["ER-01"], 3: ["AR-06"], 4: ["DG-02 (b)"], 5: ["SK-09 (a)"], 6: ["RE-02"], 7: ["DG-02"],
           8: ["AR-01"], 9: ["SK-09"], 10: ["SK-04"], 11: ["DG-02"], 12: ["DG-02"], 13: ["AP-03"], 14: ["DG-02"],
           15: ["없음"], 16: ["SK-09"], 17: ["없음"]}
def load(p):
    try:
        return yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError:
        print(f"NG 읽기 실패 {p}"); return {"_unreadable": str(p)}
def strip(d):
    d = dict(d); g = dict(d.get("diagnosis") or {})
    g.pop("cross_diagnosis_by", None); g.pop("cross_diagnosis_notes", None); d["diagnosis"] = g
    return d
IDX = {}
def find(kind, slug):
    if kind not in IDX:   # 폴더를 한 번만 읽는다 — 슬러그 문자열이 든 파일만 yaml 로 읽는다
        IDX[kind] = [(p, str(load(p).get("sprint_slug", "")).strip()) for p in sorted((FBD / kind).glob("*.yaml"))
                     if "kaizen-0924-p" in p.read_text(encoding="utf-8", errors="replace")]
    return [p for p, s in IDX[kind] if s == slug]
res = {"evaluator": dict(files=0, by=0, marker=0, tok=0, keep=0, other_diff=0),
       "contract": dict(files=0, by=0, marker=0, tok=0, keep=0, other_diff=0)}
for n, slug in enumerate(SLUGS, 1):
    marker = f"Final 교차 진단 (xdiag-all.md P{n})"
    for kind, toks in (("evaluator", EVAL_TOK[n]), ("contract", CON_TOK[n])):
        r = res[kind]; hits = find(kind, slug)
        if len(hits) != 1:
            print(f"NG {kind} {slug} files={len(hits)}"); continue
        p = hits[0]; bk = FBK / kind / p.name
        if not bk.exists():
            print(f"NG {kind} {slug} 사본 없음 {bk}"); continue
        r["files"] += 1
        now, old = load(p), load(bk)
        g, og = now.get("diagnosis") or {}, old.get("diagnosis") or {}
        notes, onotes = str(g.get("cross_diagnosis_notes", "")), str(og.get("cross_diagnosis_notes", ""))
        want_by = "sprint-contract" if kind == "evaluator" else og.get("cross_diagnosis_by")
        r["by"] += g.get("cross_diagnosis_by") == want_by
        r["marker"] += notes.count(marker) == 1
        seg = notes[notes.find(marker):] if marker in notes else ""   # 이번에 적은 부분만 본다 — 옛 기록의 같은 글자로 통과하지 않게
        r["tok"] += bool(seg) and all(t in seg for t in toks) and ("판정 유지" in seg if kind == "evaluator" else True)
        # 계약 피드백은 옛 기록을 지우지 않고 뒤에 붙인다 · 평가자 피드백은 부모 몫 자리표시를 갈아 끼운다
        r["keep"] += notes.startswith(onotes.strip()) if kind == "contract" else True
        diff = strip(now) != strip(old)
        r["other_diff"] += diff
        if diff or g.get("cross_diagnosis_by") != want_by:
            print(f"NG {kind} {slug} by={g.get('cross_diagnosis_by')} other_diff={int(diff)}")
for kind, r in res.items():
    print(kind, " ".join(f"{k}={v}" for k, v in r.items()))
```

```python
#!/usr/bin/env python3
# fbedit.py <피드백 yaml> <by 값 | -> <replace | append> <글> — diagnosis 의 두 칸만 줄 단위로 고친다.
# yaml 을 읽어 다시 쓰지 않는다 — 저장본에는 같은 키가 두 번 있고(초안 칸 + save-feedback.sh 가 덧붙인 칸) 다시 쓰면 하나가 사라진다.
# notes 는 한 줄 작은따옴표 문자열로 쓴다. append 는 옛 기록 뒤에 ` | ` 로 잇는다. 고친 뒤 yaml 로 읽혀야 저장한다.
import sys, yaml
from pathlib import Path
path, by, mode, text = Path(sys.argv[1]), sys.argv[2], sys.argv[3], sys.argv[4]
lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
old = yaml.safe_load("".join(lines))
old_notes = str((old.get("diagnosis") or {}).get("cross_diagnosis_notes", "")).strip()
new_notes = text if mode == "replace" else (old_notes + " | " + text if old_notes else text)
q = "'" + new_notes.replace("'", "''") + "'"
out, i, seen_by, seen_notes = [], 0, 0, 0
while i < len(lines):
    ln = lines[i]
    if ln.startswith("  cross_diagnosis_by:") and by != "-":
        out.append(f"  cross_diagnosis_by: {by}\n"); seen_by += 1; i += 1; continue
    if ln.startswith("  cross_diagnosis_notes:"):
        out.append(f"  cross_diagnosis_notes: {q}\n"); seen_notes += 1; i += 1
        while i < len(lines) and lines[i].startswith("    "):   # 접힌 블록(>) 의 이어지는 줄
            i += 1
        continue
    out.append(ln); i += 1
if seen_notes != 1 or (by != "-" and seen_by != 1):
    print(f"NG {path} by_lines={seen_by} notes_lines={seen_notes}"); sys.exit(1)
new = yaml.safe_load("".join(out))
g = new.get("diagnosis") or {}
if str(g.get("cross_diagnosis_notes")) != new_notes or (by != "-" and g.get("cross_diagnosis_by") != by):
    print(f"NG {path} 다시 읽은 값이 다르다"); sys.exit(1)
path.write_text("".join(out), encoding="utf-8")
print(f"OK {path}")
```

개정 파일 (ER-03):

```bash
#!/usr/bin/env bash
# amend.sh <옛 판 폴더> <새 판 폴더> <상한 ref> — Phase 개정 파일 열일곱을 잰다.
#  ends    — Phase 마다 `end_sha:` 줄 수 (차례대로 17 개)
#  p1_last — P1 마지막 end_sha 가 notes 커밋 76cfb37 인가 (1/0)
#  kept    — P2 ~ P17 의 end_sha 줄이 옛 판과 글자 그대로 같은 수 (16 이어야 함)
#  xfix    — P7 · P8 · P9 · P11 에 「교차 진단 뒤 Final 에서 고침 — <전체 sha>」 와 `amend_direction: unchanged` 가 한 줄에 든 줄 수
#  p1_remeasure — P1 계약 ER-04 셋째 · AR-04 ② 를 새 상한으로 다시 잰 값 (0 0 이어야 함) · 두 가이드 수(2)
#  after   — Phase 마다 마지막 end_sha 뒤에 그 Phase 서명으로 들어온 커밋 수 합 · 그 가운데 자기 개정 파일 말고 다른 파일을 건드린 커밋 수
O=${1:?옛 판}; N=${2:?새 판}; U=${3:?상한}
S=(p01-guides p02-contract p03-evaluator p04-harness p05-flutter-toolkit p06-design-kit p07-backend-kit p08-infra-kit
   p09-rust-kit p10-react-kit p11-planning-kit p12-reflect-kit p13-bambu-kit p14-onboarding-kit p15-tone-kit p16-api-kit p17-howto-kit)
am() { echo ".harness/sprint-amendments-kaizen-0924-${1}.md"; }
ends=""; kept=0
for s in "${S[@]}"; do f=$(am "$s"); ends="$ends $(grep -c '^end_sha:' "$N/$f")"
  [ "$s" = p01-guides ] && continue
  [ "$(grep '^end_sha:' "$O/$f")" = "$(grep '^end_sha:' "$N/$f")" ] && kept=$((kept+1)); done
P1L=$(sed -n 's/^end_sha:[[:space:]]*//p' "$N/$(am p01-guides)" | tail -1)
p1=0; [ "$P1L" = 76cfb376e2293350e2583c50166286bd2ec95b82 ] && p1=1
xfix=""
for pair in p07-backend-kit:154916a p08-infra-kit:cc11f71 p09-rust-kit:c4eeef3 p11-planning-kit:cfef54f; do
  s=${pair%%:*}; full=$(git rev-parse "${pair#*:}^{commit}") || exit 2
  xfix="$xfix $(grep -F "교차 진단 뒤 Final 에서 고침 — $full" "$N/$(am "$s")" | grep -cF 'amend_direction: unchanged')"; done
# P1 계약의 두 측정을 새 상한으로 (P1 계약 공통 정의의 mine 과 같은 식)
B1=7689fde6efdaa2401e90689dd15dd16baf8d59a0
m1=$(git log --format= --name-only "$B1..$P1L" --grep='^Kaizen-Phase: kaizen-0924-p01-guides$' | grep . | sort -u)
er4=$(printf '%s\n' "$m1" | grep -cE '^harness/(skills/(sprint|create-agent|create-skill)/SKILL\.md|agents/qa-evaluator\.md|docs/guides/qa-evaluation-guide\.md)$')
ar4=$(printf '%s\n' "$m1" | grep -vE '^(\.harness/|harness/docs/guides/(skill|agent)-design-guide\.md$)' | grep -c .)
gd=$(printf '%s\n' "$m1" | grep -cxE 'harness/docs/guides/(skill|agent)-design-guide\.md')
after=0; bad=0
for s in "${S[@]}"; do f=$(am "$s"); e=$(sed -n 's/^end_sha:[[:space:]]*//p' "$N/$f" | tail -1)
  for c in $(git log --format=%H --grep="^Kaizen-Phase: kaizen-0924-${s}\$" "$e..$U"); do after=$((after+1))
    other=$(git show --name-only --format= "$c" | grep . | grep -vxF "$f" | grep -c .)
    [ "$other" -gt 0 ] && { bad=$((bad+1)); echo "OTHER ${c:0:7} $s"; }; done; done
echo "ends=${ends# } p1_last=$p1 kept=$kept xfix=${xfix# } p1_remeasure=$er4 $ar4 guides=$gd after=$after after_other=$bad"
```

옛 값 등록부 (ER-04):

```bash
#!/usr/bin/env bash
# stale.sh <판 폴더> — 옛 값 등록부를 그 판에서 잰다.
#  clean      — 그 판 그대로 검사 종료 코드 · 등록값 수 · 사유(why) 없는 allow 수
#  unexcluded — backend-kit 을 빼지 않고 돌린 종료 코드 · 찾은 수 (allow 가 세 줄을 덮는지)
#  seeded     — 사본 세 곳에 새 옛 값 셋을 하나씩 넣고 돌린 종료 코드 · 그 값으로 찾은 수 (1 1 1 이어야 산 검사)
R=${1:?판}
python3 "$R/scripts/check-stale-values.py" >/dev/null 2>&1; rc=$?
nv=$(python3 -c 'import yaml,sys; v=yaml.safe_load(open(sys.argv[1],encoding="utf-8"))["values"]; print(len(v), "why_missing=%d" % sum(1 for x in v for a in (x.get("allow") or []) if not str(a.get("why","")).strip()))' "$R/.harness/stale-values.yaml")
ux=$(python3 - "$R" <<'PY'
import importlib.util, io, contextlib, json, sys
spec = importlib.util.spec_from_file_location("csv_", sys.argv[1] + "/scripts/check-stale-values.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
m.EXCLUDED_KITS = {}; sys.argv = ["x", "--json"]; buf = io.StringIO()
with contextlib.redirect_stdout(buf): rc = m.main()
print(rc, len(json.loads(buf.getvalue())["findings"]))
PY
)
X=$(mktemp -d "${TMPDIR:-/tmp}/stale.XXXXXX"); trap 'rm -rf "$X"' EXIT
seed() { rm -rf "$X/r"; cp -R "$R" "$X/r"; printf '\n%s\n' "$2" >> "$X/r/$1"
  python3 "$X/r/scripts/check-stale-values.py" --json 2>/dev/null | python3 -c 'import json,sys; d=json.load(sys.stdin); print(sum(1 for x in d["findings"] if x["old"]==sys.argv[1]))' "$3"
  python3 "$X/r/scripts/check-stale-values.py" >/dev/null 2>&1; echo "rc=$?"; }
s1=$(seed docs/backend/fundamentals/api-design.md 'OpenAPI 3.2.0 스펙을 단일 소스로 유지한다' 'OpenAPI 3.2.0' | tr '\n' ' ')
s2=$(seed infra-kit/references/audit-criteria.md 'OpenTofu 1.7+ native state encryption' '1.7+ native state encryption' | tr '\n' ' ')
s3=$(seed infra-kit/skills/infra-test/SKILL.md 'kubeconform -kubernetes-version 1.30.0 -strict' '-kubernetes-version 1.30.0' | tr '\n' ' ')
echo "clean rc=$rc values=$nv unexcluded=$ux seeded=[$s1] [$s2] [$s3]"
```

피드백 정리 (ER-05) — BUILD 가 쓰는 정리 도구와 재는 도구:

```python
#!/usr/bin/env python3
# cleanup-do.py <피드백 폴더> <보관 폴더> <정리 직전 목록> — (BUILD 가 쓰는 구현 도구) F3 정리를 한다.
# 목록을 먼저 쓰고, 180 일 넘은 파일과 500 개를 넘는 가장 오래된 파일을 보관 폴더로 옮긴다(지우지 않는다).
# 차례는 (mtime, 상대 경로) — cleanup.py 가 같은 차례로 잰다. 이미 목록이 있으면 덮어쓰지 않고 멈춘다(두 번 돌려 기준이 바뀌지 않게)
import os, sys, time
from pathlib import Path
fbd, arch, lst = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
cap = int(os.environ.get("CAP", "500"))
if lst.exists():
    print(f"STOP 목록이 이미 있다 {lst}"); sys.exit(2)
rows = sorted((int(p.stat().st_mtime), str(p.relative_to(fbd))) for p in fbd.rglob("*") if p.is_file())
lst.write_text("".join(f"{t}\t{p}\n" for t, p in rows), encoding="utf-8")
aged = sum(1 for t, _ in rows if t < time.time() - 180 * 86400)
cut = max(0, len(rows) - cap, aged)   # 180 일 넘은 파일은 늘 가장 오래된 쪽이라 같은 차례로 함께 옮긴다
for _, rel in rows[:cut]:
    dst = arch / rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    os.rename(fbd / rel, dst)   # 같은 볼륨 안 이동 — mtime 이 그대로 남는다
print(f"total_before={len(rows)} aged_over_6months={aged} moved={cut} remain={len(rows) - cut}")
```

```python
#!/usr/bin/env python3
# cleanup.py <피드백 폴더> <보관 폴더> <정리 직전 목록> <cleanup-log.yaml> — F3 정리를 잰다.
# 목록 줄 꼴: "<mtime 초>\t<피드백 폴더 기준 상대 경로>". 옮긴 것이 목록의 가장 오래된 (전체 - 500) 개와 같은가,
# 목록에 있던 나머지가 하나도 사라지지 않았는가, 기록 한 건이 그 수들과 맞는가. 상한은 CAP 환경변수(기본 500)
import datetime, os, sys, yaml
from pathlib import Path
fbd, arch, lst, log = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]), Path(sys.argv[4])
cap = int(os.environ.get("CAP", "500"))
if not lst.exists():
    print("UNREADABLE 정리 직전 목록 없음"); sys.exit(2)
rows = [l.split("\t", 1) for l in lst.read_text(encoding="utf-8").splitlines() if l.strip()]
rows = sorted((int(t), p) for t, p in rows)
n = len(rows); cut = max(0, n - cap)
ents = (yaml.safe_load(log.read_text(encoding="utf-8")) or {}).get("cleanup_log") or []
e = [x for x in ents if str(x.get("cycle", "")) == "kaizen-2026-09-24"]
aged = -1
if len(e) == 1:   # 기록 날짜 기준 180 일 넘은 파일 수 — 목록에서 센다 (하루 안쪽 경계 차이는 옮긴 수 비교로 드러난다)
    d0 = datetime.datetime.strptime(str(e[0].get("date")), "%Y-%m-%d") - datetime.timedelta(days=180)
    aged = sum(1 for t, _ in rows if t < d0.timestamp())
moved = max(cut, aged)   # 180 일 넘은 파일은 늘 가장 오래된 쪽이다
want = {p for _, p in rows[:moved]}
got = {str(p.relative_to(arch)) for p in arch.rglob("*") if p.is_file()} if arch.exists() else set()
still = {p for _, p in rows[moved:] if (fbd / p).exists()}
leaked = {p for p in want if (fbd / p).exists()}
ok_log = len(e) == 1 and e[0].get("total_before") == n and e[0].get("over_500_truncated") == cut \
    and e[0].get("deleted") == 0 and e[0].get("aged_over_6months") == aged and str(e[0].get("archived_to", "")) == str(arch)
print(f"before={n} cut={cut} archived={len(got)} archived_is_oldest={int(got == want)} leaked={len(leaked)} "
      f"remain_from_list={len(still)} missing={n - moved - len(still)} aged={aged} log={int(ok_log)} log_entries={len(e)}")
```

상태 커밋 (AR-01):

```bash
#!/usr/bin/env bash
# status.sh — (공통 정의를 읽은 셸에서 부른다) Phase · followups 계약 열아홉의 상태 커밋을 잰다.
#  done        — 새 판 머리 설정 status 가 done 인 계약 수
#  status_only — 옛 판 → 새 판 차이가 `status:` 한 줄 바꿈뿐인 계약 수 (조건 · 산문 · 봉인 칸 그대로)
#  seal_ok     — 새 판 verify_seal 이 SEAL_OK 인 수 · fb_tracked — 새 판에 추적되는 QA 리포트 수 · fb_new — 그중 옛 판에 없던 수
#  dirty       — 작업 폴더에서 이 서른여덟 경로에 커밋 안 한 변경이 남은 수
type fm_get verify_seal >/dev/null || exit 2
done_n=0; only=0; ok=0; tr=0; nw=0; paths=()
for s in "${PHASES[@]}" "${FOLLOWUPS[@]}"; do
  c=.harness/sprint-contract-$s.md; f=.harness/sprint-feedback-$s.md; paths+=("$c" "$f")
  [ "$(fm_get "$T/E/$c" status)" = done ] && done_n=$((done_n+1))
  d=$(git diff -U0 "$B" "$END" -- "$c" | grep -E '^[-+]' | grep -vE '^(\+\+\+|---)')
  [ "$(printf '%s\n' "$d" | grep -c .)" = 2 ] && printf '%s\n' "$d" | grep -qx -- '-status: active' && printf '%s\n' "$d" | grep -qx -- '+status: done' && only=$((only+1))
  verify_seal "$T/E/$c" | grep -q '^SEAL_OK' && ok=$((ok+1))
  git cat-file -e "$END:$f" 2>/dev/null && { tr=$((tr+1)); git cat-file -e "$B:$f" 2>/dev/null || nw=$((nw+1)); }
done
dirty=$(git status --porcelain -- "${paths[@]}" | grep -c .)
echo "done=$done_n status_only=$only seal_ok=$ok fb_tracked=$tr fb_new=$nw dirty=$dirty"
```

처리 배정표 (AR-02):

```python
#!/usr/bin/env python3
# insights.py <옛 판 파일> <새 판 파일> — 처리 배정표를 옛 판과 행 단위로 맞대 잰다.
#  rows       — 두 판의 항목 열이 같은 차례로 같은가 · 배정 칸이 전부 그대로인가
#  phase_ok   — `Phase N` 행의 대상 계약이 그 번호 Phase 슬러그와 글자 그대로 같고 QA 가 APPROVE 인 수
#  miss_ok    — 미반영 여덟 행의 비고가 옛 비고로 시작하고 「 · 미반영 — 」 와 그 Phase notes 파일 이름을 담은 수
#  other_note — 나머지 Phase 행 가운데 비고가 바뀐 수 (0 이어야 함) · non_phase_changed — Phase 가 아닌 행이 바뀐 수 (0)
import re, sys
KITS = ["guides", "contract", "evaluator", "harness", "flutter-toolkit", "design-kit", "backend-kit", "infra-kit", "rust-kit",
        "react-kit", "planning-kit", "reflect-kit", "bambu-kit", "onboarding-kit", "tone-kit", "api-kit", "howto-kit"]
SLUG = {i: f"kaizen-0924-p{i:02d}-{k}" for i, k in enumerate(KITS, 1)}
# 미반영이 있는 행 → 그 사유를 적은 notes (§미반영 키와 사유)
MISS = {"F09": ["phase5-notes.md", "phase10-notes.md"], "F18": ["phase4-notes.md"], "F20": ["phase11-notes.md"],
        "F22": ["phase5-notes.md"], "F25": ["phase5-notes.md"], "F28": ["phase4-notes.md"],
        "design:P2": ["phase6-notes.md"], "user-setup:P2": ["phase4-notes.md"]}
def rows(path):
    out, head = [], None
    for line in open(path, encoding="utf-8"):
        if not line.startswith("|"):
            if head: break
            continue
        cells = [c.strip() for c in re.split(r"(?<!\\)\|", line.strip().strip("|"))]
        if head is None:
            if "대상 계약" in cells: head = cells
            continue
        if set("".join(cells)) <= set("-: "):
            continue
        out.append(dict(zip(head, cells)))
    return out
old, new = rows(sys.argv[1]), rows(sys.argv[2])
same_rows = [r["항목"] for r in old] == [r["항목"] for r in new] and all(a["배정"] == b["배정"] for a, b in zip(old, new))
phase_n = phase_ok = miss_ok = other = nonp = 0
for a, b in zip(old, new):
    m = re.fullmatch(r"Phase\s*(\d+)", b["배정"])
    if not m:
        nonp += a != b; continue
    phase_n += 1; n = int(m.group(1))
    phase_ok += b["대상 계약"] == SLUG.get(n) and b["QA"] == "APPROVE"
    if b["항목"] in MISS:
        miss_ok += b["비고"].startswith(a["비고"]) and " · 미반영 — " in b["비고"] and all(x in b["비고"] for x in MISS[b["항목"]])
    else:
        other += a["비고"] != b["비고"]
print(f"rows={len(new)} same_rows={int(same_rows)} phase_rows={phase_n} phase_ok={phase_ok} miss_ok={miss_ok}/{len(MISS)} "
      f"other_note={other} non_phase_changed={nonp}")
```

문서 사이트 (AR-03) — 페이지 표 `PAIRS` 와 새 글자 · 옛 글자 표 `TOKENS`:

```python
#!/usr/bin/env python3
# docs.py <옛 판 폴더> <새 판 폴더> — 다시 만들 페이지 44 개를 두 판에서 맞대 잰다.
#  exist · changed — 새 판에 있고 옛 판과 바이트가 다른 페이지 수
#  short   — 400 줄(api-kit 은 450 줄) 미만 페이지 수 (docs-site Gotcha 8 · check-api-kit-docs.py MIN_LINES)
#  accent  — `--accent` 값이 옛 판과 다른 페이지 수 · ext — 외부 리소스를 부르는 페이지 수 · hidden_up — overflow hidden 이 옛 판보다 는 페이지 수
#  tok_new — 원본에 새로 생긴 글자가 페이지 글(태그를 벗긴 본문)에 든 행 수 · tok_old — 원본에서 사라진 옛 글자가 아직 남은 행 수
#            (끝 열넷은 원본 머리 설정 판 번호 — 사이클 동안 오른 새 판 번호가 제목 · 뱃지에 있어야 한다)
#  html_added · html_removed — docs/ 아래 HTML 파일 목록이 옛 판과 다른 수 (새 페이지를 만들지 않는다)
import html, re, sys
from pathlib import Path
O, N = Path(sys.argv[1]), Path(sys.argv[2])
PAIRS = """
bambu-kit/skills/bambu-print-profile/SKILL.md docs/bambu-kit/bambu-print-profile.html
bambu-kit/skills/bambu-print-profile/references/surface-recipes.md docs/bambu-kit/surface-recipes.html
docs/api/contract/contract-extraction-modes.md docs/api-kit/contract-extraction-modes.html
docs/api/contract/snapshot-sealing-canonicalization.md docs/api-kit/snapshot-sealing-canonicalization.html
docs/api/execution/auth-secret-lifecycle.md docs/api-kit/auth-secret-lifecycle.html
docs/api/execution/probe-synthesis-hurl-semantics.md docs/api-kit/probe-synthesis-hurl-semantics.html
docs/api/verification/regression-diff-failure-policy.md docs/api-kit/regression-diff-failure-policy.html
docs/api/verification/static-evidence-viewer-contract.md docs/api-kit/static-evidence-viewer-contract.html
docs/backend/fundamentals/api-design.md docs/backend-kit/api-design.html
docs/backend/fundamentals/database.md docs/backend-kit/database.html
docs/infra/platform/cicd.md docs/infra-kit/cicd.html
docs/onboarding-kit/examples/fcm-ios-setup-guide.md docs/onboarding-kit/fcm-ios-example.html
docs/planning/data-modeling.md docs/planning-kit/data-modeling.html
docs/planning/flows.md docs/planning-kit/flows.html
docs/planning/prd-patterns.md docs/planning-kit/prd-patterns.html
docs/rust/data/sqlx-patterns.md docs/rust-kit/sqlx-patterns.html
docs/tone/korean-technical-writing.md docs/tone-kit/korean-technical-writing.html
docs/tone/overview.md docs/tone-kit/overview.html
flutter-toolkit/references/flutter-ai-rules.md docs/flutter-toolkit/flutter-ai-rules.html
flutter-toolkit/references/primitive-substitution-gate.md docs/flutter-toolkit/primitive-substitution-gate.html
flutter-toolkit/references/project-detection.md docs/flutter-toolkit/project-detection.html
flutter-toolkit/references/visual-evidence-protocol.md docs/flutter-toolkit/visual-evidence-protocol.html
harness/docs/guides/agent-design-guide.md docs/harness/agent-design-guide.html
harness/docs/guides/contract-design-guide.md docs/harness/contract-design-guide.html
harness/docs/guides/plugin-validation-guide.md docs/harness/plugin-validation.html
harness/docs/guides/qa-evaluation-guide.md docs/harness/qa-evaluation-guide.html
harness/docs/guides/skill-design-guide.md docs/harness/skill-design-guide.html
harness/references/contract-schema.md docs/harness/contract-schema.html
onboarding-kit/skills/setup-guide/SKILL.md docs/onboarding-kit/setup-guide.html
onboarding-kit/skills/setup-guide/references/format-checklist.md docs/onboarding-kit/format-checklist.html
onboarding-kit/skills/setup-guide/references/project-detection.md docs/onboarding-kit/project-detection.html
react-kit/references/render-evidence-protocol.md docs/react-kit/render-evidence-protocol.html
docs/react/kit-design/g4-quality.md docs/react-kit/quality.html
backend-kit/skills/backend-test/SKILL.md docs/backend-kit/backend-test.html
design-kit/references/visual-change-protocol.md docs/design-kit/visual-change-protocol.html
design-kit/skills/design-component/SKILL.md docs/design-kit/design-component.html
design-kit/skills/design-concept/SKILL.md docs/design-kit/design-concept.html
design-kit/skills/design-mockup/SKILL.md docs/design-kit/design-mockup.html
design-kit/skills/design-test/SKILL.md docs/design-kit/design-test.html
infra-kit/references/gate-result-taxonomy.md docs/infra-kit/gate-result-taxonomy.html
infra-kit/skills/infra-test/SKILL.md docs/infra-kit/infra-test.html
reflect-kit/docs/DESIGN.md docs/reflect-kit/design.html
reflect-kit/docs/SCHEMA.md docs/reflect-kit/schema.html
howto-kit/README.md docs/howto-kit/overview.html
"""
# (종류, 페이지, 글자) — new 는 새 판 페이지에 1 이상, old 는 0 이어야 한다. 옛 판에서는 new 0 · old 1 이상(봉인 전 실측)
TOKENS = [
    ("new", "docs/bambu-kit/bambu-print-profile.html", "MakerWorld 읽는 순서"),
    ("old", "docs/bambu-kit/bambu-print-profile.html", "Cloudflare"),
    ("new", "docs/bambu-kit/surface-recipes.html", "G-code 로 길이 재기"),
    ("new", "docs/api-kit/contract-extraction-modes.html", "한 번 망가뜨려 본다"),
    ("new", "docs/api-kit/snapshot-sealing-canonicalization.html", "정정 7920"),
    ("new", "docs/api-kit/auth-secret-lifecycle.html", "--curl"),
    ("new", "docs/api-kit/probe-synthesis-hurl-semantics.html", "HURL_VARIABLE_"),
    ("new", "docs/api-kit/regression-diff-failure-policy.html", "판정 불가"),
    ("new", "docs/api-kit/static-evidence-viewer-contract.html", "24×24"),
    ("new", "docs/backend-kit/api-design.html", "OpenAPI 3.2.1"),
    ("old", "docs/backend-kit/api-design.html", "OpenAPI 3.2.0"),
    ("new", "docs/backend-kit/database.html", "벽시계"),
    ("new", "docs/infra-kit/cicd.html", "merge-base"),
    ("new", "docs/onboarding-kit/fcm-ios-example.html", "Xcode 26.2"),
    ("new", "docs/planning-kit/data-modeling.html", "ELK"),
    ("new", "docs/planning-kit/flows.html", "12.0.0"),
    ("new", "docs/planning-kit/prd-patterns.html", "폐기한 결정"),
    ("new", "docs/rust-kit/sqlx-patterns.html", "벽시계"),
    ("new", "docs/tone-kit/korean-technical-writing.html", "새 이름을 만들지 않는다"),
    ("new", "docs/tone-kit/overview.html", "INC=(--include="),
    ("old", "docs/tone-kit/overview.html", 'INC="--include'),
    ("new", "docs/flutter-toolkit/flutter-ai-rules.html", "4.0.2"),
    ("old", "docs/flutter-toolkit/flutter-ai-rules.html", "3.2.5"),
    ("old", "docs/flutter-toolkit/primitive-substitution-gate.html", "fit-pal"),
    ("new", "docs/flutter-toolkit/project-detection.html", "전후 삭제 수"),
    ("new", "docs/flutter-toolkit/visual-evidence-protocol.html", "캡처 점검 목록"),
    ("new", "docs/harness/agent-design-guide.html", "managed settings"),
    ("new", "docs/harness/contract-design-guide.html", "이 스프린트의 커밋이 끝난 뒤"),
    ("new", "docs/harness/plugin-validation.html", "— FAIL"),
    ("new", "docs/harness/qa-evaluation-guide.html", "산출물이 검사일 때"),
    ("new", "docs/harness/skill-design-guide.html", "알려진 답 대조"),
    ("old", "docs/harness/skill-design-guide.html", "500 라인 상한"),
    ("new", "docs/harness/contract-schema.html", "알려진 답 대조"),
    ("new", "docs/onboarding-kit/setup-guide.html", "[미검증:ENV]"),
    ("new", "docs/onboarding-kit/format-checklist.html", "막는 요구"),
    ("new", "docs/onboarding-kit/project-detection.html", "열지 않는다"),
    ("new", "docs/react-kit/render-evidence-protocol.html", "캡처 점검 목록"),
    ("new", "docs/react-kit/quality.html", "사용자가 요청할 때만"),
    ("new", "docs/backend-kit/backend-test.html", "mock-only"),
    ("new", "docs/design-kit/visual-change-protocol.html", "되말하기"),
    ("new", "docs/design-kit/design-component.html", "visual-change-protocol"),
    ("new", "docs/design-kit/design-concept.html", "폐기한 대안"),
    ("new", "docs/design-kit/design-mockup.html", "container-type"),
    ("old", "docs/design-kit/design-test.html", "법적 기준"),
    ("new", "docs/infra-kit/gate-result-taxonomy.html", "시도한 우회"),
    ("new", "docs/infra-kit/infra-test.html", "TOOL_OR_ENV_MISSING"),
    ("old", "docs/infra-kit/infra-test.html", "1.30.0"),
    ("new", "docs/reflect-kit/design.html", "codex-exit"),
    ("new", "docs/reflect-kit/schema.html", "claude-used"),
    ("new", "docs/howto-kit/overview.html", "howto-gate.sh"),
    ("old", "docs/howto-kit/overview.html", "두 셸 출력의"),
    ("new", "docs/harness/skill-design-guide.html", "1.6.0"),
    ("new", "docs/harness/agent-design-guide.html", "1.7.0"),
    ("new", "docs/harness/contract-design-guide.html", "v5.1"),
    ("new", "docs/harness/qa-evaluation-guide.html", "v5.1"),
    ("new", "docs/harness/contract-schema.html", "v5.5"),
    ("new", "docs/harness/plugin-validation.html", "1.4.0"),
    ("new", "docs/react-kit/render-evidence-protocol.html", "1.1.0"),
    ("new", "docs/backend-kit/database.html", "0.3.0"),
    ("new", "docs/api-kit/contract-extraction-modes.html", "0.1.1"),
    ("new", "docs/api-kit/snapshot-sealing-canonicalization.html", "0.1.1"),
    ("new", "docs/api-kit/auth-secret-lifecycle.html", "0.2.1"),
    ("new", "docs/api-kit/probe-synthesis-hurl-semantics.html", "0.2.1"),
    ("new", "docs/api-kit/regression-diff-failure-policy.html", "0.1.1"),
    ("new", "docs/api-kit/static-evidence-viewer-contract.html", "0.1.1"),
]
EXTERNAL = re.compile(r'<link\s|<script[^>]+src=|@import\s|url\(\s*[\'"]?https?://')
SUPPRESS = re.compile(r"overflow\s*:\s*hidden|overflow-x\s*:\s*hidden")
ACCENT = re.compile(r"--accent:\s*(#[0-9A-Fa-f]{6})")
def text(p):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", p.read_text(encoding="utf-8"))))
pages = [l.split()[1] for l in PAIRS.strip().splitlines()]
c = dict(pairs=len(pages), exist=0, changed=0, short=0, accent=0, ext=0, hidden_up=0)
for pg in pages:
    o, n = O / pg, N / pg
    if not n.exists():
        print("NG 없음", pg); continue
    c["exist"] += 1
    t, ot = n.read_text(encoding="utf-8"), (o.read_text(encoding="utf-8") if o.exists() else "")
    if t != ot: c["changed"] += 1
    else: print("NG 그대로", pg)
    lim = 450 if pg.startswith("docs/api-kit/") else 400
    if t.count("\n") < lim: c["short"] += 1; print("NG 짧음", pg, t.count("\n"))
    a, oa = ACCENT.search(t), ACCENT.search(ot)
    if (a and a.group(1).upper()) != (oa and oa.group(1).upper()): c["accent"] += 1; print("NG accent", pg)
    if EXTERNAL.search(t): c["ext"] += 1; print("NG 외부 리소스", pg)
    if len(SUPPRESS.findall(t)) > len(SUPPRESS.findall(ot)): c["hidden_up"] += 1; print("NG overflow hidden 늘어남", pg)
nn = no = nn_ok = no_bad = 0
for kind, pg, tok in TOKENS:
    k = text(N / pg).count(tok) if (N / pg).exists() else 0
    if kind == "new":
        nn += 1; nn_ok += k >= 1
        if k < 1: print("NG 새 글자 없음", pg, tok)
    else:
        no += 1; no_bad += k > 0
        if k > 0: print("NG 옛 글자 남음", pg, tok)
hs = lambda R: {str(p.relative_to(R)) for p in (R / "docs").rglob("*.html")}
ho, hn = hs(O), hs(N)
print(" ".join(f"{k}={v}" for k, v in c.items()) +
      f" tok_new={nn_ok}/{nn} tok_old={no_bad}/{no} html_added={len(hn - ho)} html_removed={len(ho - hn)}")
```

```python
#!/usr/bin/env python3
# navver.py <판 폴더> — 첫 화면(docs/index.html) harness 다섯 항목 제목이 원본 판 번호를 담는지 센다.
# 판 번호는 원본 머리 설정 version · contract-schema 「현재:」 줄의 사이클 끝 값이다(이 계약은 원본을 고치지 않는다)
import re, sys
t = open(sys.argv[1] + "/docs/index.html", encoding="utf-8").read()
WANT = {"skill-design": "v1.6.0", "agent-design": "v1.7.0", "contract-design": "v5.1", "qa-evaluation": "v5.1", "contract-schema": "v5.5"}
ok = sum(1 for i, v in WANT.items() if re.search(r"\{ id: '%s',\s*title: '[^']*%s'" % (re.escape(i), re.escape(v)), t))
print(f"nav_ver={ok}/{len(WANT)}")
```

```python
#!/usr/bin/env python3
# titlever.py <판 폴더> — harness 다섯 페이지 <title> 이 원본 판 번호를 담는지 센다.
# 판 번호 넷은 원본 본문에도 나와 tok_new 만으로는 제목에 옛 판이 남아도 통과한다(2 회차 검토 권고 1)
import re, sys
W = {"skill-design-guide": "1.6.0", "agent-design-guide": "1.7.0", "contract-design-guide": "v5.1",
     "qa-evaluation-guide": "v5.1", "contract-schema": "v5.5"}
def title(p):
    m = re.search(r"<title>([^<]*)</title>", open(p, encoding="utf-8").read())
    return m.group(1) if m else ""
ok = sum(1 for p, v in W.items() if v in title(f"{sys.argv[1]}/docs/harness/{p}.html"))
print(f"title_ver={ok}/{len(W)}")
```

changelog · 연구 기록 (AR-04):

```python
#!/usr/bin/env python3
# logs.py <옛 판 폴더> <새 판 폴더> — changelog · 연구 기록 다섯 파일에 더한 줄을 잰다.
#  head    — 더한 줄 가운데 `## ` 머리이면서 2026-09-24 를 담은 줄 수 (1 이어야 함)
#  missing — 이 파일이 담아야 할 Phase 번호 가운데 더한 줄에 `Phase N` 이 없는 번호 · final — `Final` 이 있어야 하는 파일에서 든 줄 수
#  del_bad — 지운 줄 가운데 머리 설정의 `version:` · `last_updated:` 줄이 아닌 수 (새 항목만 더한다)
#  url_out — 더한 줄의 URL 가운데 Phase notes 열일곱 · followups notes 둘 · 근거 파일 어디에도 없는 수
#  urls    — 더한 줄의 서로 다른 출처 URL 수. 연구 기록 셋은 5 이상이어야 한다(오케스트레이터 F4 3 번 「출처 URL 최소 5 건」)
import difflib, re, sys
from pathlib import Path
O, N = Path(sys.argv[1]), Path(sys.argv[2])
# 파일 → (담을 Phase 번호, Final 이 있어야 하는가, 최소 출처 URL 수)
WANT = {
    "docs/kaizen/changelog.md": (list(range(1, 18)), True, 0),
    "docs/kaizen/flutter-changelog.md": ([5], False, 0),
    "docs/kaizen/research-log.md": ([1, 2, 3, 4, 12, 13, 14, 17], True, 5),
    "docs/kaizen/flutter-research-log.md": ([5], False, 5),
    "docs/design/research-log.md": ([6], False, 5),
}
URL = re.compile(r'https?://[^\s)>"`\]]+')
clean = lambda u: u.rstrip(".,;:")
meta = N / ".harness/.meta"
known = set()
for p in [x for x in (meta / "kaizen-0924").glob("*-notes.md") if x.name != "final-notes.md"] + list((meta / "evidence").glob("phase*.md")):
    known |= {clean(u) for u in URL.findall(p.read_text(encoding="utf-8"))}
tot_bad = 0
for f, (phases, need_final, min_urls) in WANT.items():
    a = (O / f).read_text(encoding="utf-8").splitlines() if (O / f).exists() else []
    b = (N / f).read_text(encoding="utf-8").splitlines()
    d = list(difflib.unified_diff(a, b, lineterm="", n=0))
    add = [l[1:] for l in d if l.startswith("+") and not l.startswith("+++")]
    rem = [l[1:] for l in d if l.startswith("-") and not l.startswith("---")]
    body = "\n".join(add)
    head = sum(1 for l in add if l.startswith("## ") and "2026-09-24" in l)
    miss = [n for n in phases if not re.search(rf"Phase {n}(?!\d)", body)]
    fin = body.count("Final") if need_final else -1
    del_bad = sum(1 for l in rem if not re.match(r"^(version|last_updated):", l))
    urls = {clean(u) for u in URL.findall(body)}
    out = sorted(urls - known)
    bad = (head != 1) + bool(miss) + (need_final and fin < 1) + (del_bad > 0) + bool(out) + (len(urls) < min_urls)
    tot_bad += bad
    print(f"{f} head={head} missing={miss} final={fin} del_bad={del_bad} urls={len(urls)} url_out={len(out)} {out[:3]}")
print(f"files={len(WANT)} bad={tot_bad} known_urls={len(known)}")
```

사이클 상태 · 실패 횟수 · evals 점검 (AR-05):

```python
#!/usr/bin/env python3
# meta.py <판 폴더> — 사이클 상태 · 실패 횟수 · evals 점검 기록을 한 판에서 잰다.
#  state   — kaizen-state.yaml 의 cycle_id 가 kaizen-2026-09-24 이고 status 가 completed 인가 (1/0)
#  phases  — 실패 횟수 파일의 phase_N 키 수 · 1 ~ 17 이 빠짐없이 있고 전부 0 인가 · last_updated 에 2026-09-24 가 있는가
#  evals   — 점검 기록 파일에 sync-evals 요약 줄 · evals.json 열 경로 · 스킬 더함·지움·이름 바꿈 명령이 다 있는가
import re, sys, yaml
from pathlib import Path
R = Path(sys.argv[1]); M = R / ".harness/.meta"
st = yaml.safe_load((M / "kaizen-state.yaml").read_text(encoding="utf-8")) or {}
state = int(st.get("cycle_id") == "kaizen-2026-09-24" and st.get("status") == "completed")
fc = yaml.safe_load((M / "kaizen-failure-count.yaml").read_text(encoding="utf-8")) or {}
ph = fc.get("phases") or {}
keys_ok = int(set(ph) == {f"phase_{i}" for i in range(1, 18)})
zero = int(all(ph.get(f"phase_{i}") == 0 for i in range(1, 18)))
lu = int("2026-09-24" in str(fc.get("last_updated", "")))
ev = M / "evals-audit-2026-09-24.md"
EV = ["backend-kit/evals/evals.json", "design-kit/evals/evals.json", "flutter-toolkit/evals/evals.json", "harness/evals/evals.json",
      "howto-kit/evals/evals.json", "infra-kit/evals/evals.json", "onboarding-kit/skills/setup-guide/evals/evals.json",
      "react-kit/evals/evals.json", "rust-kit/evals/evals.json", "tone-kit/evals/evals.json"]
if ev.exists():
    t = ev.read_text(encoding="utf-8")
    evals = f"total_line={int('Total: 0 added, 0 orphans, 0 missing' in t)} paths={sum(p in t for p in EV)}/{len(EV)} " \
            f"adr_cmd={int('git diff --name-status' in t)}"
else:
    evals = "MISSING"
print(f"state={state} phases={len(ph)} keys_ok={keys_ok} zero={zero} last_updated={lu} evals=[{evals}]")
```

릴리스 계획 (SC-01):

```python
#!/usr/bin/env python3
# plan.py <판 폴더> <기준 ref> <상한 ref> — 릴리스 계획을 잰다.
#  changed — 사이클 동안 파일이 바뀐 킷 수 (marketplace.json 의 source 폴더 기준)
#  lines   — 계획 파일 bash 블록의 `bash scripts/release.sh <킷> <minor|patch>` 줄이 바뀐 킷과 하나씩 맞는가 · 단계가 아래 표와 같은가
#  basis   — 표의 근거 칸이 가리키는 notes 파일이 그 판에 있는 행 수
#  bumped  — 사이클 동안 plugin.json · marketplace.json 을 건드린 커밋 수 (0 이어야 함)
import json, re, subprocess, sys
from pathlib import Path
R, FROM, TO = Path(sys.argv[1]), sys.argv[2], sys.argv[3]
# 킷 → 단계. 기능 추가 = minor, 고침만 = patch (러닝북 「버전」 절). 근거는 계약 GAP 분석의 릴리스 표
LEVEL = {"harness": "minor", "flutter-toolkit": "minor", "design-kit": "minor", "backend-kit": "minor", "infra-kit": "minor",
         "rust-kit": "minor", "react-kit": "minor", "planning-kit": "minor", "reflect-kit": "minor", "bambu-kit": "minor",
         "onboarding-kit": "minor", "tone-kit": "minor", "api-kit": "minor", "howto-kit": "patch"}
plugins = json.loads((R / ".claude-plugin/marketplace.json").read_text(encoding="utf-8"))["plugins"]
files = subprocess.run(["git", "diff", "--name-only", FROM, TO], capture_output=True, text=True, check=True).stdout.split()
changed = {p["name"] for p in plugins if any(f.startswith(p["source"].lstrip("./").rstrip("/") + "/") for f in files)}
plan = (R / ".harness/.meta/kaizen-0924/release-plan.md")
if not plan.exists():
    print("MISSING release-plan.md"); sys.exit(2)
t = plan.read_text(encoding="utf-8")
blocks = re.findall(r"^```bash\n(.*?)^```$", t, re.S | re.M)
cmds = re.findall(r"^bash scripts/release\.sh (\S+) (minor|patch)$", "\n".join(blocks), re.M)
got = {}
for k, lv in cmds:
    got.setdefault(k, []).append(lv)
lines_ok = int(set(got) == changed and all(len(v) == 1 for v in got.values()))
level_ok = sum(1 for k in changed if got.get(k) == [LEVEL.get(k)])
rows = re.findall(r"^\| `?([a-z-]+)`? \| (minor|patch) \| .*?`(\.harness/\.meta/kaizen-0924/[\w-]+\.md)`", t, re.M)
basis = sum(1 for k, lv, p in rows if k in changed and (R / p).exists())
bumped = len(subprocess.run(["git", "log", "--format=%H", f"{FROM}..{TO}", "--", "*/.claude-plugin/plugin.json",
                             ".claude-plugin/marketplace.json"], capture_output=True, text=True, check=True).stdout.split())
print(f"changed={len(changed)} cmds={len(cmds)} lines_ok={lines_ok} level_ok={level_ok}/{len(changed)} basis={basis} bumped={bumped}")
```

메모리 후보 (AR-06):

```python
#!/usr/bin/env python3
# mem.py <판 폴더> — 메모리 승격 후보 파일(F3.5)을 잰다. 파일의 첫 ```yaml 블록을 읽는다.
#  parse     — yaml 로 읽히고 첫 줄이 `# kaizen-memory-candidates` 인가 · cycle_id · generated_at(시간대 붙은 ISO 8601)
#  keys      — 모든 후보가 오케스트레이터 F3.5 포맷의 열세 키를 빠짐없이, 그 밖의 키 없이 갖는가
#  forbidden — 판정 결과 키(promoted_to · rule_id · enforcement_level · status)가 파일 어디에든 든 수 (0)
#  grounding — self_inference 이거나 네 값 밖인 후보 수 (0) · actionability 가 claude_behavior 가 아닌 후보 수 (0)
#  evidence  — source_evidence 경로가 없는 항목 수 (0) · need — 반드시 낼 두 근본원인 태그가 든 수 (2)
#  tmp_bad   — source_evidence 경로가 세션 스크래치(/private/tmp · /tmp) 아래인 수 (0 — 세션이 끝나면 사라져 /reflect-promote 가 열 수 없다)
#  out_bad   — 절대경로인데 ~/.harness/ 아래가 아닌 수 (0 — 조건은 저장소 경로이거나 ~/.harness/ 아래만 허용한다)
import datetime, os, re, sys, yaml
from pathlib import Path
R = Path(sys.argv[1]); f = R / ".harness/.meta/memory-promotion-candidates-2026-09-24.md"
if not f.exists():
    print("MISSING"); sys.exit(2)
t = f.read_text(encoding="utf-8")
m = re.search(r"^```yaml\n(.*?)^```$", t, re.S | re.M)
body = m.group(1) if m else ""
d = yaml.safe_load(body) if body else None
# 따옴표 없는 시각은 yaml 이 datetime 으로 읽어 str() 이 가운데 T 를 빈칸으로 바꾼다 — F3.5 틀이 따옴표 없이 보인다
ga = d.get("generated_at") if isinstance(d, dict) else None
ga = ga.isoformat() if isinstance(ga, datetime.datetime) else str(ga or "")
parse = int(isinstance(d, dict) and body.startswith("# kaizen-memory-candidates") and d.get("cycle_id") == "kaizen-2026-09-24"
            and bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(:\d{2})?([+-]\d{2}:\d{2}|Z)", ga)))
KEYS = {"canonical_tag", "grounding", "actionability", "scope", "risk_class", "procedurality", "enforcement_need",
        "user_stated_constraint", "freq", "undesired_behavior", "desired_behavior", "source_evidence", "draft_rule"}
cands = (d or {}).get("candidates") or []
keys_bad = sum(1 for c in cands if set(c) != KEYS)
forbidden = sum(len(re.findall(rf"^\s*{k}\s*:", t, re.M)) for k in ("promoted_to", "rule_id", "enforcement_level", "status"))
g_bad = sum(1 for c in cands if c.get("grounding") not in ("user_correction", "execution_evidence", "mixed"))
a_bad = sum(1 for c in cands if c.get("actionability") != "claude_behavior")
ev_bad = tmp_bad = out_bad = 0
for c in cands:
    for e in c.get("source_evidence") or []:
        p = os.path.expanduser(str(e.get("path", "")))
        if not (Path(p) if os.path.isabs(p) else R / p).exists():
            ev_bad += 1; print("NG 근거 경로 없음", p)
        if p.startswith(("/private/tmp/", "/tmp/")):
            tmp_bad += 1; print("NG 세션 스크래치 경로", p)
        if os.path.isabs(p) and not p.startswith(os.path.expanduser("~/.harness/")):
            out_bad += 1; print("NG 저장소 · ~/.harness 밖 경로", p)
NEED = ["lint-new-warning-added-lines-only", "scope-count-signed-commits-only"]
need = sum(1 for n in NEED if any(c.get("canonical_tag") == n for c in cands))
print(f"parse={parse} candidates={len(cands)} keys_bad={keys_bad} forbidden={forbidden} grounding_bad={g_bad} "
      f"actionability_bad={a_bad} evidence_bad={ev_bad} need={need}/{len(NEED)} tmp_bad={tmp_bad} out_bad={out_bad}")
```

감사 기록 (AR-07):

```bash
#!/usr/bin/env bash
# audit.sh <옛 판 폴더> <새 판 폴더> — 감사 기록(orchestrator-audit-log.md)에 더한 부분을 잰다.
#  append_only — 새 판이 옛 판 전체로 시작하는가 (지운 · 고친 줄 없음)
#  head · generated · manual_orch — 도구가 찍는 머리 줄 · 생성 줄 · 수동 편집 절의 오케스트레이터 SKILL.md 가 든 수
#  f1h · f1k · new4 — 두 followups 가 「고치지 않음」 으로 남긴 ID 스물아홉 · 행 서른셋 · 구현 중 새로 찾은 넷이 든 수
#  notes — Phase notes 열일곱의 파일 이름이 든 수 (다음 사이클 메모를 가리킨다)
#  fnotes — 두 후속 notes 파일 이름이 든 수 (F1H · F1K 번호를 찾아갈 자리) · meta — 이번 사이클 메타 이슈 여섯 글자가 든 수
#           (`append-audit-log.py` 파일 이름만은 도구 생성 줄에도 있어 줄 번호 `:148` 을 붙여 잰다)
O=${1:?옛 판}; N=${2:?새 판}; F=.harness/.meta/orchestrator-audit-log.md
python3 - "$O/$F" "$N/$F" <<'PY'
import re, sys
o = open(sys.argv[1], encoding="utf-8").read(); n = open(sys.argv[2], encoding="utf-8").read()
ap = int(n.startswith(o)); add = n[len(o):] if ap else ""
F1H = [14, 35, 37, 38, 39, 40, 41, 43, 44, 47, 48, 56, 58, 59, 60, 65, 66, 67, 76, 77, 78, 79, 80, 81, 82, 84, 91, 92, 94]
F1K = [10, 11, 12, 14, 15, 18, 21, 24, 25, 26, 28, 29, 31, 32, 33, 34, 36, 39, 42, 43, 44, 48, 50, 51, 52, 53, 56, 57, 60, 69, 70, 73, 80]
has = lambda tok: re.search(re.escape(tok) + r"(?![0-9])", add) is not None
head = len(re.findall(r"^## \d{4}-\d{2}-\d{2} — kaizen/2026-09-24$", add, re.M))
gen = add.count("**Generated:** `scripts/append-audit-log.py` (auto-append)")
orch = add.count(".claude/skills/kaizen-orchestrator/SKILL.md")
FN = ["f1-harness-followups-notes.md", "f1-kit-followups-notes.md"]
MT = ["kaizen-state.yaml", "feedback-archive", "check-insights-tracking.py", "append-audit-log.py:148", "FN-79", "FN-80"]
print(f"append_only={ap} head={head} generated={gen} manual_orch={int(orch >= 1)} "
      f"f1h={sum(has(f'F1H-{i}') for i in F1H)}/{len(F1H)} f1k={sum(has(f'F1K-{i}') for i in F1K)}/{len(F1K)} "
      f"new4={sum(has(f'F1H-N{i}') for i in range(1, 5))}/4 notes={sum(has(f'phase{i}-notes.md') for i in range(1, 18))}/17 "
      f"fnotes={sum(has(x) for x in FN)}/{len(FN)} meta={sum(has(x) for x in MT)}/{len(MT)}")
PY
```

notes (AR-08):

```bash
#!/usr/bin/env bash
# notes.sh — (공통 정의를 읽은 셸에서 부른다) Final notes 가 측정 도우미의 실제 출력을 글자 그대로 담았는지 잰다.
#  heads   — 필수 소제목 여섯이 하나씩 있는 수
#  lines   — 도우미 출력 여덟 줄(f1.sh 넷 · tonegrade · toneterms · synt · amend) 가운데 notes 에 글자 그대로 든 수
#  nohtml  — 대응 페이지가 없는 원본 열아홉 경로가 notes 에 든 수
#  memo    — `## 다음 사이클 메모` 절에 입력 표 `고치지 않음` ID 열하나와 두 후속 notes 파일 이름이 든 수 (13)
type my >/dev/null || exit 2
NF=$T/E/$NOTES
[ -f "$NF" ] || { echo "MISSING $NOTES"; exit 2; }
h=0
for s in '## 커밋' '## F1 정합' '## 교차 진단 기록' '## 문서 사이트' '## 넘기는 것' '## 다음 사이클 메모'; do
  [ "$(grep -cx -- "$s" "$NF")" = 1 ] && h=$((h+1)); done
mkdir -p "$T/CB"; git archive "$CB" tone-kit | tar -x -C "$T/CB" || exit 2
L=$( { bash "$K/f1.sh" "$T/E"; python3 "$K/tonegrade.py" "$T/CB" "$T/E" | head -1; python3 "$K/toneterms.py" "$T/E" | head -1;
       bash "$K/synt.sh" "$T/E" "$CB" "$END" | tail -1; bash "$K/amend.sh" "$T/B" "$T/E" "$END" | tail -1; } )
n=0; while IFS= read -r l; do [ -n "$l" ] && grep -qF -- "$l" "$NF" && n=$((n+1)); [ -n "$l" ] && ! grep -qF -- "$l" "$NF" && echo "MISS $l"; done <<< "$L"
NOH="bambu-kit/skills/bambu-print-profile/references/comment-analysis.md docs/api/research-log.md docs/backend/research-log.md
docs/flutter/research-log.md docs/infra/research-log.md docs/planning/research-log.md docs/react/research-log.md docs/rust/research-log.md
docs/tone/research-log.md flutter-toolkit/references/figma-parity-self-verify.md react-kit/references/common-gotchas.md
reflect-kit/skills/reflect-digest/SKILL.md reflect-kit/skills/reflect-kaizen/SKILL.md rust-kit/references/project-detection.md
tone-kit/references/core-antipatterns.md tone-kit/references/core-comment.md tone-kit/references/core-naming.md
tone-kit/references/locale-korean.md tone-kit/references/sources.md"
m=0; for p in $NOH; do grep -qF -- "$p" "$NF" && m=$((m+1)); done
MEMO=$(awk '/^## 다음 사이클 메모$/{p=1; next} /^## /{p=0} p' "$NF")
MEMO_IDS="FN-18 FN-39 FN-43 FN-56 FN-58 FN-64 FN-76 FN-77 FN-78 FN-79 FN-80 f1-harness-followups-notes.md f1-kit-followups-notes.md"
# 뒤 글자를 보는 까닭 — 번호 뒤에 숫자가 붙은 다른 ID(FN-180 등)로 통과하지 않게
mm=0; for x in $MEMO_IDS; do printf '%s\n' "$MEMO" | grep -qE -- "${x}([^0-9]|\$)" && mm=$((mm+1)); done
echo "heads=$h/6 lines=$n/$(printf '%s\n' "$L" | grep -c .) nohtml=$m/19 memo=$mm/13"
```

범위 (AR-09):

```bash
#!/usr/bin/env bash
# range.sh — (공통 정의를 읽은 셸에서 부른다) 이 계약 변경이 허용 경로 안에 머무는지 잰다.
#  outside      — 서명 커밋이 건드린 파일 가운데 허용 경로 밖 수
#  html_extra   — 서명 커밋이 건드린 docs/ HTML 가운데 다시 만들 44 페이지와 docs/index.html 밖 수
#  forbidden    — 서명 여부와 상관없이 구간 안에서 킷 폴더 · scripts/ · .claude/skills/ · .github/ · 버전 파일을 건드린 커밋 수
#  unsigned     — 구간 안 커밋 가운데 서명 줄이 없는 수 · broken — 새 판 계약 가운데 SEAL_BROKEN 수 · self — 이 계약 봉인
#  seal_files   — 이 계약 첫 서명 커밋(봉인 커밋)이 실은 파일 수
type my verify_seal >/dev/null || exit 2
PAGES=$(python3 -c 'import re,sys; s=open(sys.argv[1],encoding="utf-8").read(); print("\n".join(re.search(r"PAIRS = \"\"\"(.*?)\"\"\"", s, re.S).group(1).split()[1::2]))' "$K/docs.py")
ALLOW='^(\.harness/|\.claude/kaizen-input/insights-report\.md$|docs/index\.html$|docs/kaizen/[^/]+\.md$|docs/design/research-log\.md$|CLAUDE\.md$|docs/.+\.html$)'
outside=$(my | grep -vcE "$ALLOW")
html_extra=$(my | grep -E '^docs/.+\.html$' | grep -vxF 'docs/index.html' | grep -vxF -f <(printf '%s\n' "$PAGES") | grep -c .)
KITS=$(python3 -c 'import json; print(" ".join(p["source"].lstrip("./").rstrip("/") for p in json.load(open(".claude-plugin/marketplace.json"))["plugins"]))')
# shellcheck disable=SC2086
forbidden=$(git log --format=%H "$B..$END" -- $KITS scripts .claude/skills .github .claude-plugin | grep -c .)
unsigned=$(git log --format=%H "$B..$END" | while read -r c; do git log -1 --format=%B "$c" | grep -qxF "$SIG" || echo "$c"; done | grep -c .)
broken=$(find "$T/E/.harness" -maxdepth 1 -type f -name 'sprint-contract*.md' -print0 | while IFS= read -r -d '' f; do verify_seal "$f"; done | grep -c '^SEAL_BROKEN')
self=$(verify_seal "$T/E/$CF" | awk '{print $1}')
first=$(git log --reverse --format=%H --grep="^$SIG\$" "$B..$END" | head -1)
seal_files=$(git show --name-only --format= "$first" | grep -c .)
echo "my=$(my | grep -c .) outside=$outside html_extra=$html_extra forbidden=$forbidden unsigned=$unsigned broken=$broken self=$self seal_files=$seal_files"
```

편집기 경고 · 펜스 (DG-02 · AP-03):

```bash
#!/usr/bin/env bash
# mdcmp.sh <옛 판 폴더> <새 판 폴더> <파일…> — 파일마다 markdownlint 경고를 (규칙, 그 줄 글자) 묶음으로 두 판에서 세어,
# 새 판에만 더 있는 묶음 수를 낸다. 줄 번호를 쓰지 않으므로 더한 줄 옆 손대지 않은 줄에 붙은 새 경고(MD022 · MD024 · MD032)도 잡힌다.
# 옛 판에 없는 파일은 경고 전부가 새 경고다. VERBOSE=1 이면 새 묶음을 `NEW <파일> <규칙> <줄 글자>` 로 찍는다
# 경고 줄 꼴은 `경로:줄[:열] 심각도 규칙/…` — 줄 번호는 첫 콜론 바로 뒤다. 경로에 콜론이 있으면 줄 번호를 잘못 읽으므로 멈춘다
K=$(cd "$(dirname "$0")" && pwd)
[ -x "$K/node_modules/.bin/markdownlint-cli2" ] || { echo "TOOL_MISSING markdownlint-cli2"; exit 2; }
old=${1:?}; new=${2:?}; shift 2
case "$old$new$*" in *:*) echo "PATH_HAS_COLON"; exit 2 ;; esac
lint() {  # lint <파일> — "규칙<TAB>줄 글자" 를 한 줄씩
  [ -f "$1" ] || return 0
  "$K/node_modules/.bin/markdownlint-cli2" --config "$K/cfg.markdownlint-cli2.jsonc" "$1" 2>&1 \
    | sed -nE 's/^[^:]*:([0-9]+)(:[0-9]+)? (error|warning) (MD[0-9]+)\/.*/\1 \4/p' \
    | while read -r n r; do printf '%s\t%s\n' "$r" "$(sed -n "${n}p" "$1")"; done | sort
}
total=0
for f in "$@"; do
  a=$(lint "$old/$f"); b=$(lint "$new/$f")
  d=$(comm -13 <(printf '%s\n' "$a" | grep .) <(printf '%s\n' "$b" | grep .))
  n=$(printf '%s\n' "$d" | grep -c .)
  rules=$(printf '%s\n' "$d" | grep . | cut -f1 | sort | uniq -c | awk '{printf "%s:%s ", $2, $1}')
  printf '%s new=%s %s\n' "$f" "$n" "$rules"
  [ "${VERBOSE:-0}" = 1 ] && printf '%s\n' "$d" | grep . | sed "s#^#NEW $f #"
  total=$((total + n))
done
printf 'new_total=%s\n' "$total"
```

```python
#!/usr/bin/env python3
# fence.py <파일…> — 여는 펜스에 언어 힌트가 없는 수와 닫히지 않은 펜스 수를 센다 (validate-plugin V6 와 같은 여닫기 방식)
import re, sys
tb = tu = 0
for path in sys.argv[1:]:
    open_len, open_ch, bare = 0, "", []
    for n, line in enumerate(open(path, encoding="utf-8"), 1):
        m = re.match(r"^\s*(`{3,}|~{3,})(.*)$", line.rstrip("\n"))
        if not m:
            continue
        run, rest = m.group(1), m.group(2).strip()
        if open_len == 0:
            open_len, open_ch = len(run), run[0]
            if not rest:
                bare.append(n)
        elif run[0] == open_ch and len(run) >= open_len and not rest:
            open_len = 0
    tb += len(bare); tu += 1 if open_len else 0
    if bare or open_len:
        print(f"{path}: bare_open={bare} unclosed={1 if open_len else 0}")
print(f"bare_open_total={tb} unclosed_total={tu}")
```

저장소 검사 · CI 시험 · 사후 점검 (DG-05):

```bash
#!/usr/bin/env bash
# dg05.sh <상한 ref> <사이클 기준 ref> — 상한 판을 새로 복제해 저장소 검사 · CI 시험 · 사후 점검을 돌린다.
# 작업 폴더를 쓰지 않는다 — 커밋 안 한 변경(다음 QA 의 상태 전환 등)이 끼지 않는다. 사후 점검은 git 기록이 있어야 해서 복제한다
U=${1:?상한}; CBR=${2:?사이클 기준}
W=$(git rev-parse --show-toplevel) || exit 2
X=$(mktemp -d "${TMPDIR:-/tmp}/dg05.XXXXXX"); trap 'rm -rf "$X"' EXIT
git clone -q --shared "$W" "$X/c" && git -C "$X/c" checkout -q "$U" || { echo "CLONE_FAIL"; exit 2; }
cd "$X/c" || exit 2
rc_list=""
for t in "python3 scripts/validate-plugin.py" "python3 scripts/sync-docs.py --check-only" "python3 scripts/sync-evals.py --check-only" \
         "python3 scripts/sync-orchestrator.py --check-only" "python3 scripts/run-evals.py" "python3 scripts/check-stale-values.py" \
         "python3 scripts/validate-doc-contracts.py" "python3 scripts/check-contrast-claims.py" "python3 scripts/check-docs-links.py" \
         "python3 scripts/check-api-kit-docs.py" \
         "bash harness/evals/hooks/commit-guard-test.sh" "bash harness/evals/kaizen/feedback-system/save-test.sh" \
         "bash harness/evals/kaizen/feedback-system/aggregation-test.sh" "python3 scripts/test-collect-kaizen-data.py" \
         "bash reflect-kit/evals/hooks/log-reflection-test.sh" "bash reflect-kit/evals/hooks/project-id-test.sh" \
         "bash reflect-kit/evals/hooks/collect-status-test.sh" "sh onboarding-kit/skills/setup-guide/evals/run-gate-evals.sh" \
         "sh howto-kit/evals/run-evals.sh" "bash react-kit/evals/scripts/project-detect-test.sh" \
         "bash flutter-toolkit/evals/hooks/format-edited-dart-test.sh"; do
  # shellcheck disable=SC2086
  $t >/dev/null 2>&1; r=$?; rc_list="$rc_list$r"; [ "$r" = 0 ] || echo "NONZERO rc=$r $t"
done
vpk=$(python3 scripts/validate-post-kaizen.py --since "$CBR" 2>&1); vrc=$?
bad=$(printf '%s\n' "$vpk" | grep -E '^\[ (FAIL|ERROR) *\]' | grep -c .)
skip=$(printf '%s\n' "$vpk" | grep -E '^\[ SKIP' | sed -E 's/^\[ SKIP +\] · ([a-z-]+):.*/\1/' | sort | tr '\n' ' ')
pass=$(printf '%s\n' "$vpk" | grep -cE '^\[ PASS')
printf '%s\n' "$vpk" | grep -E '^\[ (FAIL|ERROR) *\]'
echo "rc=[$rc_list] vpk_rc=$vrc vpk_pass=$pass vpk_bad=$bad vpk_skip=[${skip% }]"
```

### 봉인 전 실측 (2026-09-25, `END` 자리에 시작 커밋 `511f19b` 를 넣고 같은 도우미를 돌림)

「시작 판」 은 `END=B` 로 돌린 값, 「양성 대조」 는 사본에 나쁜 예를 넣거나 모의 폴더로 돌린 값이다. 구현이 만들 값(끝 판 칸)은 봉인 전에 잴 수 없어 면제이고,
그 값을 재는 명령 · 도구 · 경로는 모두 이 표의 시작 판 줄로 돌려 살아 있음을 확인했다.

| 조건 | 시작 판 | 끝 판 기대 | 양성 · 음성 대조 |
| ---- | ------- | ---------- | ---------------- |
| SK-01 (a)(b)(c) | `p1hand=0 0 0 0 0 0 4 1` · `parity=1 1` · `apikit=1 1 1 1 1 1 1` · `orch16=1 1 1 1 1` (사이클 기준 판 `CB`: `p1hand=1 3 1 1 1 1 0 0` · `parity=1 0`) | 같은 네 줄 | 사본에서 skill 가이드 `version` 한 글자 → `parity=0 1` · `>=3` → `>=2` → `apikit` 셋째 0 · sprint 에 옛 문구 한 줄 → `p1hand` 첫 값 1 |
| SK-01 (d) | `rules_old=62 rules_new=63 raised=0 added=[('K-11', ['관측 컨벤션'])]` 종료 코드 0 | 같음 | 사본 C-01 `SHOULD` → `MUST` → `raised=1` 종료 코드 1 · 빈 references → `UNREADABLE` 종료 코드 2 |
| SK-01 (e) | `tone_terms=8 other_files=119 other_terms=652 intersect=0 substring=0` 종료 코드 0 | 같음 | design-guide 설명에 「"톤 위반"」 · 「"주석 골격 만들기"」 → `intersect=1 substring=1` 종료 코드 1 (설명 읽기 정규식을 고치기 전에는 `tone_terms=0` 이었다 — 그 공허를 이 대조로 잡았다) |
| SK-01 (f) | `sh=16 sh_bad=0 py=8 py_bad=0 json=14 json_bad=0 yaml=2 yaml_bad=0 all_sh=43 all_sh_bad=0 actionlint_rc=0` | `yaml=6` 로만 다름(이 계약이 YAML 넷을 고친다) | 사본 훅에 `if then` → `sh_bad=1` · evals.json `{broken` → `json_bad=1` · 사이클에 안 바뀐 `scripts/release.sh` 에 `if then` → `sh_bad=0 … all_sh_bad=1` (`BAD all bash -n scripts/release.sh`) |
| SK-02 | `10 Phase` 2 · `17 Phase` 0 · `howto-kaizen (Phase 17)` 0 · `tone-kaizen (Phase 15)` 1 | 0 · 2 · 1 · 0 · numstat `3 3` | 시작 판 값이 곧 음성 대조 |
| SC-01 | `MISSING release-plan.md` · 바뀐 킷 14 · 사이클 동안 버전 파일 커밋 0 | `changed=14 cmds=14 lines_ok=1 level_ok=14/14 basis=14 bumped=0` | 모의 판(표 열넷 · `release.sh` 열네 줄, 근거 칸 전체 경로)에서 기대 줄 그대로 · 같은 판에서 근거 칸만 짧은 이름(`phase3-notes.md`)으로 → `basis=0` |
| ER-01 · ER-02 | `evaluator files=17 by=0 marker=0 tok=0 keep=17 other_diff=0` · `contract files=17 by=17 marker=0 tok=0 keep=17 other_diff=0` · `verify-feedback.sh` 34/34 PASS | 둘 다 `files=17 by=17 marker=17 tok=17 keep=17 other_diff=0` · 34/34 PASS | 모의 사본에서 P7 두 파일만 `fbedit.py` 로 고침 → `by=1 marker=1 tok=1` · 다른 칸(`verdict`)을 바꾸면 `other_diff=1` · 편집 뒤 두 파일 `verify-feedback.sh` PASS |
| ER-03 | `ends=1 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 p1_last=0 kept=16 xfix=0 0 0 0 p1_remeasure=0 0 guides=2 after=18 after_other=1` (`OTHER 76cfb37 p01-guides`) | `ends=` 열일곱 모두 2 · `p1_last=1 kept=16 xfix=1 1 1 1 p1_remeasure=0 0 guides=2 after=16 after_other=0` | 모의 판(P1 한 줄 · P7 · 8 · 9 · 11 한 줄씩)에서 기대 줄 그대로 |
| ER-04 | `clean rc=0 values=15 why_missing=0 unexcluded=1 3 seeded=[0 rc=0 ] [0 rc=0 ] [0 rc=0 ]` | `clean rc=0 values=18 why_missing=0 unexcluded=0 0 seeded=[1 rc=1 ] [1 rc=1 ] [1 rc=1 ]` | 모의 등록부(개선안 5 번 글자)에서 기대 줄 그대로 |
| ER-05 | 피드백 639 개 · 180 일 초과 0 · 정리 기록 없음 | `before=N cut=N-500 archived=N-500 archived_is_oldest=1 leaked=0 remain_from_list=500 missing=0 aged=0 log=1 log_entries=1` (N 은 정리 순간 수, 639 이상) | 모의 폴더 열한 파일 · `CAP=7`: 바른 이동 → `archived_is_oldest=1 leaked=0 missing=0 log=1` · 한 파일을 되돌리고 새 파일을 옮기고 하나를 지우면 `archived_is_oldest=0 leaked=1 missing=2` · `cleanup-do.py` 두 번째 호출은 `STOP` 종료 코드 2 |
| AR-01 | `done=0 status_only=0 seal_ok=19 fb_tracked=0 fb_new=0 dirty=38` | `done=19 status_only=19 seal_ok=19 fb_tracked=19 fb_new=19 dirty=0` | 시작 판 값이 곧 음성 대조 |
| AR-02 | `rows=96 same_rows=1 phase_rows=74 phase_ok=0 miss_ok=0/8 other_note=0 non_phase_changed=0` · 검사기 종료 코드 1 · `Phase 행 미완료 74` | `phase_ok=74 miss_ok=8/8` 나머지 같음 · 종료 코드 0 · `Phase 행 미완료 0` · `TRACKING_TABLE_OK` | 모의 판(칸 채움)에서 기대 줄 · 종료 코드 0. 그 판에서 Phase 6 행 여덟에 Phase 5 슬러그 → 검사기는 여전히 `TRACKING_TABLE_OK`, `insights.py` 는 `phase_ok=66` 으로 떨어짐 |
| AR-03 | `pairs=44 exist=44 changed=0 short=7 accent=0 ext=0 hidden_up=0 tok_new=0/56 tok_old=9/9 html_added=0 html_removed=0` · `nav_ver=0/5` · `title_ver=0/5` · 첫 화면 numstat 빈 출력 · api-kit 문서 `10/12 PASS` 종료 코드 1 · 내비 `페이지 176 · 등록 176` 종료 코드 0 · 대비 수치 종료 코드 0 | `changed=44 short=0 tok_new=56/56 tok_old=0/9` 나머지 같음 · `nav_ver=5/5` · `title_ver=5/5` · numstat `5 5 docs/index.html` · `12/12 PASS` 종료 코드 0 · 176 · 176 · 0 | 시작 판 값이 곧 음성 대조(새 글자 쉰여섯 모두 0, 옛 글자 아홉 모두 1 이상, 원본에는 새 글자 1 이상 · 옛 글자 0 — 판 번호 열넷은 원본 머리 설정 · 「현재:」 줄과 열넷 모두 같음). 임시 복제본에서 다섯 제목만 고쳐 커밋 → `5 5 docs/index.html` · `nav_ver=5/5` · 내비 176 · 176, 한 제목만 → `nav_ver=1/5`. 페이지 사본에 `v1.6.0` 한 줄 → `tok_new=1/56`. `skill-design-guide` 페이지 `<title>` 만 고친 사본 → `title_ver=1/5`, 거기에 `contract-design-guide` 본문에만 `v5.1` → `1/5` |
| AR-04 | `files=5 bad=15 known_urls=350` (연구 기록 셋 `urls=0`) · per-kit `1 1 1 1 1 1 ` (사이클 기준 판 `0 0 0 0 0 0 `) | `files=5 bad=0` (파일마다 `head=1 missing=[] del_bad=0 url_out=0`, 연구 기록 셋 `urls=` 5 이상) · per-kit `1 1 1 1 1 1 ` | 모의 판 changelog 에 근거 파일 밖 URL 한 줄 → `url_out=1` · 다섯 파일 첫 `##` 앞에 날짜 머리 항목을 끼우고 연구 기록 셋에 아는 URL 다섯 → `bad=0`, 넷 → `bad=3` |
| AR-05 | `state=0 phases=14 keys_ok=0 zero=0 last_updated=0 evals=[MISSING]` · 스킬 더함·지움·이름 바꿈 0 줄 | `state=1 phases=17 keys_ok=1 zero=1 last_updated=1 evals=[total_line=1 paths=10/10 adr_cmd=1]` | 모의 판에서 기대 줄 그대로 · 복제본에서 `cycle_id` 만 바꾸면 사후 점검 FAIL 여섯(날짜 다섯 + `docs-site-regen`) |
| AR-06 | `MISSING` · 원장 0 개 | `parse=1 candidates=N keys_bad=0 forbidden=0 grounding_bad=0 actionability_bad=0 evidence_bad=0 need=2/2 tmp_bad=0 out_bad=0` (N ≥ 2) · 원장 0 개 | 모의 파일에 `status: active` · `self_inference` → `keys_bad=2 forbidden=2 grounding_bad=2` · 후보 둘 모의 파일 근거가 저장소 notes → `tmp_bad=0 out_bad=0`, `~/.harness/feedback/evaluator/…` 와 그 절대경로 → `tmp_bad=0 out_bad=0`, `$HOME/.claude/CLAUDE.md` → `out_bad=1`, 스크래치 `xdiag-all.md`(있는 경로) → `evidence_bad=0 … tmp_bad=1 out_bad=1`. `generated_at` 따옴표 없이 `2026-09-25T20:00:00+09:00` → `parse=1`(2 회차 검토 전 식은 `parse=0`) · 시간대 없는 `2026-09-25T20:00:00` → `parse=0` · 끝이 `Z` → `parse=1` |
| AR-07 | `append_only=1 head=0 generated=0 manual_orch=0 f1h=0/29 f1k=0/33 new4=0/4 notes=0/17 fnotes=0/2 meta=0/6` | `append_only=1 head=1 generated=1 manual_orch=1 f1h=29/29 f1k=33/33 new4=4/4 notes=17/17 fnotes=2/2 meta=6/6` | 모의 판(도구 `render_entry` 출력 + 두 notes 이름 · ID 목록 + 메타 절)에서 기대 줄 그대로 · 메타 절만 빼면 `meta=0/6`(검토가 제안한 다섯 글자는 도구 생성 줄의 `scripts/append-audit-log.py` 로 `1/5` 가 남았다 — 그래서 `:148` 을 붙였다) · 수동 편집 JSON 경로를 틀리면 도구가 「빈 목록」 으로 처리해 `manual_orch=0` 이 된다(실측) |
| AR-08 | `MISSING .harness/.meta/kaizen-0924/final-notes.md` 종료 코드 2 | `heads=6/6 lines=8/8 nohtml=19/19 memo=13/13` · notes 커밋이 `END` | 모의 notes 에 amend 줄을 빼면 `lines=7/8` 과 `MISS ends=…` · 메모 절에 열세 글자를 둔 모의 notes → `memo=13/13`, `FN-80` 을 넘기는 것 절로만 옮기면 `memo=12/13`(실제 `notes.sh` 로 돌림) |
| AR-09 | (구현 전이라 없음) | `outside=0 html_extra=0 forbidden=0 unsigned=0 broken=0 self=SEAL_OK seal_files=1` | 임시 복제본: 서명 커밋이 `scripts/` 한 파일과 목록 밖 페이지를 고치고 서명 없는 커밋 하나 · 가짜 봉인 → `outside=1 html_extra=1 forbidden=1 unsigned=1 broken=1 self=SEAL_BROKEN seal_files=1` · 고친 `ALLOW` 식은 `README.md` 를 허용 밖으로 낸다(네 경로 가운데 `README.md` · `harness/README.md` 둘) |
| DG-02 · AP-03 | `new_total=0` (`MDS` 열여덟) · `bare_open_total=0 unclosed_total=0` | `new_total=3` — 새 묶음 셋이 모두 감사 기록의 도구 소제목 MD024 · 펜스 0 · 0 | 모의 판: 빈 줄 하나 뒤 도구 출력 + 두 notes · 메타 절 → `new_total=3` · `NEW` 셋 모두 도구 소제목 MD024 · 걸러낸 뒤 0. 빈 줄 없이 붙이면 `new_total=5`(MD022 · MD032 더함, 걸러낸 뒤 2). flutter 연구 기록 끝에 맨 URL · 옛 제목 → `new=2 MD024:1 MD034:1`. 음성 대조: 다섯 기록 파일 첫 `##` 앞에 경고 없는 새 항목 → 모두 `new=0` (고치기 전 sed 식은 `new_total=18` — research-log `MD034:1` · flutter-research-log `MD033:1 MD060:3` · design `MD060:13`). 경로에 콜론이 든 판 → `PATH_HAS_COLON` 종료 코드 2 |
| DG-04 | 페이지 마흔넷 `44/44 PASS` 종료 코드 0 · `docs` 전체 `177/177 PASS` | 같음 | 사본 페이지에 폭 2000px · 대비 1.11 인 줄 → `0/1 PASS` 종료 코드 1 |
| DG-05 | `rc=[000000000100000000000] vpk_rc=1 vpk_pass=12 vpk_bad=1` — 열째(`check-api-kit-docs.py`)만 1 · 사후 점검 `docs-site-regen` FAIL · 날짜 다섯은 옛 항목으로 PASS | `rc=[000000000000000000000] vpk_rc=0 vpk_pass=13 vpk_bad=0 vpk_skip=[marketplace-sync plugin-json-bumps]` | 복제본에서 `cycle_id` 를 새 사이클로 → FAIL 여섯 · 종료 코드 1 |
| AP-01 | 더한 줄 없음 | 0 | 「harness 0.13.0 로 올린다」 한 줄 → 1, 「contract-schema v5.5 · skill-design-guide 1.6.0」 → 0 |
| RE-01 | (구현 전) | 0 | 모의 목록에 `scripts/x.py` → 1 |

## Skill

- [ ] SK-01: 끝 판이 교차 Phase 정합 여섯 가지를 지킨다 — (a) Phase 1 이 넘긴 여덟 자리에서 옛 문구 여섯이 0 이고 새 칸 둘이 1 이상 (b) Phase 3 평가 가이드의 `Parity with` · `Schema link` 가 Phase 1 · 2 판 번호(세 가이드 머리 `version` · 스키마 현재 판)와 글자 그대로 같다 (c) api-kit 확정 결정 일곱 글자와 오케스트레이터 Phase 16 결정 다섯 글자가 남아 있다 (d) tone-kit 규칙 가운데 사이클 기준 판보다 강도가 오른 것이 0 이다 (e) tone-kit 트리거 어휘가 다른 킷 스킬 · 에이전트 설명과 같은 말 · 품는 말 0 쌍이다 (f) 사이클 동안 더하거나 고친 셸 열여섯 · 파이썬 여덟 · JSON 열넷 · YAML 여섯이 해석기대로 문법 검사를 통과하고, 끝 판에 추적되는 셸 마흔셋 전체도 해석기대로(해석기 줄이 없으면 `bash -n`) 통과하며(오케스트레이터 F1 「전체 `bash -n` 검증」), CI 워크플로가 actionlint 0 이다. 출력 줄은 notes 에 글자 그대로 남는다(AR-08) [exact, enumerated]
      (측정: (a)(b)(c) `bash "$K/f1.sh" "$T/E"` 네 줄이 `p1hand=0 0 0 0 0 0 X Y`(X · Y 1 이상) · `parity=1 1` · `apikit=1 1 1 1 1 1 1` · `orch16=1 1 1 1 1` ·
       (d) `mkdir -p "$T/CB" && git archive "$CB" tone-kit | tar -x -C "$T/CB"` 뒤 `python3 "$K/tonegrade.py" "$T/CB" "$T/E"` 종료 코드 0 · 첫 줄에 `raised=0` ·
       (e) `python3 "$K/toneterms.py" "$T/E"` 종료 코드 0 · 첫 줄 `tone_terms=8` · `intersect=0 substring=0` · `other_terms=` 값 600 이상 ·
       (f) `bash "$K/synt.sh" "$T/E" "$CB" "$END"` 끝줄 `sh=16 sh_bad=0 py=8 py_bad=0 json=14 json_bad=0 yaml=6 yaml_bad=0 all_sh=43 all_sh_bad=0 actionlint_rc=0`.
       양성 대조 · 시작 판: 봉인 전 실측 표 SK-01 네 행 — 사이클 기준 판 `p1hand=1 3 1 1 1 1 0 0` · `parity=1 0`, 강도를 올린 사본 `raised=1` 종료 코드 1, 겹침을 넣은 사본 `intersect=1 substring=1` 종료 코드 1, 셸 · JSON 을 깬 사본 `sh_bad=1` · `json_bad=1`, 사이클에 안 바뀐 `scripts/release.sh` 를 깬 사본 `sh_bad=0 … all_sh_bad=1`)
- [ ] SK-02: 루트 `CLAUDE.md` 의 카이젠 설명 세 줄(명령 예시 주석 · Kaizen Orchestration 의 Phase 순서 · 레포 전용 스킬 표 `/kaizen` 행)이 Phase 17(howto-kaizen)까지를 적고, 이 파일의 다른 줄은 그대로다 [exact]
      (측정: `grep -cF '10 Phase' "$T/E/CLAUDE.md"` 0 · `grep -cF '17 Phase' "$T/E/CLAUDE.md"` 2 · `grep -cF 'howto-kaizen (Phase 17)' "$T/E/CLAUDE.md"` 1 · `grep -cF 'tone-kaizen (Phase 15)' "$T/E/CLAUDE.md"` 0 ·
       `git diff --numstat "$B" "$END" -- CLAUDE.md | tr '\t' ' '` 가 `3 3 CLAUDE.md` 한 줄. 시작 판: 2 · 0 · 0 · 1 · 빈 출력)

## Script

- [ ] SC-01: 버전 파일을 올리지 않고 릴리스 계획으로 대신한다 — `.harness/.meta/kaizen-0924/release-plan.md` 의 bash 블록에 사이클 동안 파일이 바뀐 킷 열넷이 `bash scripts/release.sh <킷> <단계>` 한 줄씩 있고, 단계는 GAP 분석 릴리스 표와 같으며(howto-kit 만 patch), 표의 근거 칸이 notes 파일을 `.harness/.meta/kaizen-0924/<파일>.md` 전체 경로(백틱으로 감쌈)로 가리키고 그 파일이 있다. 이 파일은 오케스트레이터 Step F4 1 번과 체크리스트 버전 두 줄을 대신한다는 문장과 reflect-kit 배포 뒤 설치본 Stop 훅 확인 줄(`collect_status 1` 의 기록된 세션 1 이상 — phase12-notes)을 담는다. 사이클 동안 `plugin.json` · `marketplace.json` 을 건드린 커밋은 0 이다 [exact, enumerated]
      (측정: `python3 "$K/plan.py" "$T/E" "$CB" "$END"` 가 `changed=14 cmds=14 lines_ok=1 level_ok=14/14 basis=14 bumped=0` ·
       `grep -cF '오케스트레이터 Step F4 1 번과 체크리스트 버전 두 줄을 이 파일로 대신한다' "$T/E/$PLAN"` 1 · `grep -cF 'collect_status 1' "$T/E/$PLAN"` 1 이상.
       시작 판: `MISSING release-plan.md` 종료 코드 2 · 바뀐 킷 14 · 버전 파일 커밋 0. 양성 대조: 모의 판에서 기대 줄 그대로 — 킷 하나를 빼면 `lines_ok=0`, 단계를 바꾸면 `level_ok=13/14`, 근거 칸을 짧은 이름(`phase3-notes.md`)으로 쓰면 `basis=0`)

## Error

- [ ] ER-01: Phase 열일곱 평가자 피드백에 교차 진단 결론이 들어간다 — 전역 피드백 폴더의 슬러그마다 한 파일이 `cross_diagnosis_by: sprint-contract` 이고, `cross_diagnosis_notes` 가 `Final 교차 진단 (xdiag-all.md P<N>)` 로 시작하는 글을 한 번 담으며 그 글에 「판정 유지」 와 GAP 분석 교차 진단 기록 표의 평가자 쪽 필수 글자가 있다. 두 칸 말고는 고치기 전 사본과 같고, 열일곱 모두 `verify-feedback.sh` 가 PASS 다 [exact, enumerated]
      (Given: BUILD 가 고치기 전에 `$FBK/evaluator/` 에 열일곱 사본을 `cp -p` 로 떴다 · 측정: `python3 "$K/fbx.py" "$FBD" "$FBK"` 의 `evaluator` 줄이 `files=17 by=17 marker=17 tok=17 keep=17 other_diff=0` ·
       `n=0; for f in $(grep -lE 'sprint_slug: *.?kaizen-0924-p(0[1-9]|1[0-7])-' "$FBD"/evaluator/*.yaml); do bash harness/scripts/verify-feedback.sh "$f" 2>&1 | tail -1 | grep -qx PASS && n=$((n+1)); done; echo "$n"` 17.
       시작 판: `files=17 by=0 marker=0 tok=0 keep=17 other_diff=0` · 17. 양성 대조: 모의 사본의 P7 만 고치면 `by=1 marker=1 tok=1`, `verdict` 를 바꾸면 `other_diff=1`)
- [ ] ER-02: Phase 열일곱 계약 피드백에 교차 진단이 찾은 그 계약의 측정 구멍이 붙는다 — 슬러그마다 한 파일의 `cross_diagnosis_notes` 가 옛 기록으로 시작하고 뒤에 `Final 교차 진단 (xdiag-all.md P<N>)` 로 시작하는 글이 한 번 붙으며 그 글에 교차 진단 기록 표의 계약 쪽 필수 글자(구멍이 없던 P15 · P17 은 「없음」)가 있다. `cross_diagnosis_by` 와 나머지 칸은 사본과 같고 열일곱 모두 `verify-feedback.sh` PASS 다 [exact, enumerated]
      (Given: `$FBK/contract/` 에 열일곱 사본 · 측정: `python3 "$K/fbx.py" "$FBD" "$FBK"` 의 `contract` 줄이 `files=17 by=17 marker=17 tok=17 keep=17 other_diff=0` · ER-01 과 같은 반복을 `"$FBD"/contract/*.yaml` 로 돌려 17.
       시작 판: `files=17 by=17 marker=0 tok=0 keep=17 other_diff=0` · 17. 양성 대조: 모의 사본 P7 에 `fbedit.py … append` 한 번 → `marker=1 tok=1`, 옛 기록은 그대로라 `keep` 유지)
- [ ] ER-03: Phase 개정 파일이 교차 진단 뒤 사실을 적는다 — P1 개정 파일 마지막 `end_sha:` 가 notes 커밋 `76cfb37`(전체 sha)이고 그 상한으로 다시 잰 P1 ER-04 셋째 · AR-04 ② 가 0 · 0 이다. P7 · P8 · P9 · P11 개정 파일에 「교차 진단 뒤 Final 에서 고침 — <kit followups 커밋 전체 sha>」 와 `amend_direction: unchanged` 가 한 줄에 하나씩 있다(`154916a` · `cc11f71` · `c4eeef3` · `cfef54f`). P2 ~ P17 의 `end_sha:` 줄은 시작 판과 글자 그대로 같고, Phase 마다 마지막 `end_sha` 뒤에 그 Phase 서명으로 들어온 커밋은 자기 개정 파일만 고쳤다 [exact, enumerated]
      (측정: `bash "$K/amend.sh" "$T/B" "$T/E" "$END"` 끝줄이 `ends=2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 p1_last=1 kept=16 xfix=1 1 1 1 p1_remeasure=0 0 guides=2 after=16 after_other=0` 이고 `OTHER` 줄이 0 개.
       시작 판: `ends=1 2 … p1_last=0 kept=16 xfix=0 0 0 0 p1_remeasure=0 0 guides=2 after=18 after_other=1` · `OTHER 76cfb37 p01-guides`. 양성 대조: 모의 판에서 기대 줄 그대로)
- [ ] ER-04: 옛 값 등록부가 이번 사이클이 고친 옛 값 셋을 잡고 backend-kit 세 줄을 사유와 함께 허용한다 — 등록값이 열여덟이고 사유 없는 allow 가 0 이며, 그 판 그대로 검사 종료 코드 0, backend-kit 을 빼지 않고 돌려도 종료 코드 0 · 찾은 수 0, 사본 세 곳에 `OpenAPI 3.2.0` · `1.7+ native state encryption` · `-kubernetes-version 1.30.0` 을 하나씩 넣으면 각각 한 건을 찾고 종료 코드 1 이다 [exact, enumerated]
      (측정: `bash "$K/stale.sh" "$T/E"` 가 `clean rc=0 values=18 why_missing=0 unexcluded=0 0 seeded=[1 rc=1 ] [1 rc=1 ] [1 rc=1 ]`.
       시작 판: `clean rc=0 values=15 why_missing=0 unexcluded=1 3 seeded=[0 rc=0 ] [0 rc=0 ] [0 rc=0 ]` — 새 옛 값이 되살아나도 못 잡는 상태. 양성 대조: 모의 등록부에서 기대 줄 그대로)
- [ ] ER-05: 전역 피드백 정리(F3)가 지우지 않고 옮긴다 — 정리 직전 목록의 가장 오래된 (전체 − 500) 개가 보관 폴더에 있고 피드백 경로에는 없으며, 목록의 나머지 500 개는 하나도 사라지지 않았다. `cleanup-log.yaml` 에 `cycle: "kaizen-2026-09-24"` 항목이 하나 있고 그 `total_before` · `over_500_truncated` · `aged_over_6months` · `deleted: 0` · `archived_to` 가 목록과 맞는다. 피드백 경로에 180 일 넘은 파일이 0 이다 [exact]
      (Given: BUILD 가 `python3 "$K/cleanup-do.py" "$FBD" "$ARCH" "$FBLIST"` 로 목록을 먼저 쓰고 옮겼다 · 측정: `python3 "$K/cleanup.py" "$FBD" "$ARCH" "$FBLIST" "$T/E/.harness/.meta/cleanup-log.yaml"` 가
       `before=N cut=M archived=M archived_is_oldest=1 leaked=0 remain_from_list=500 missing=0 aged=0 log=1 log_entries=1` 이고 N 은 639 이상 · M = N − 500 ·
       `find "$FBD" -type f -mtime +180 | grep -c .` 0. 시작 판: 피드백 639 개 · 180 일 초과 0 · 정리 기록 없음. 양성 대조: 모의 폴더 열한 파일(`CAP=7`) — 바른 이동은 기대 꼴, 한 파일을 되돌리고 다른 파일을 옮기고 하나를 지우면 `archived_is_oldest=0 leaked=1 missing=2`)

## Architecture

- [ ] AR-01: Phase · followups 계약 열아홉의 상태 전환과 QA 리포트 열아홉이 이 계약 커밋으로 들어간다 — 끝 판 열아홉 계약이 `status: done` 이고 시작 판과의 차이는 그 한 줄뿐이며 모두 `SEAL_OK` 다. QA 리포트 열아홉은 끝 판에 추적되고 시작 판에는 없었다. 작업 폴더에 그 서른여덟 경로의 커밋 안 한 변경이 없다 [exact, enumerated]
      (Given: 이 계약 커밋이 끝난 뒤 · 측정: `type fm_get verify_seal >/dev/null || exit 2;` 뒤 `. "$K/status.sh"` 가 `done=19 status_only=19 seal_ok=19 fb_tracked=19 fb_new=19 dirty=0`.
       시작 판: `done=0 status_only=0 seal_ok=19 fb_tracked=0 fb_new=0 dirty=38`)
- [ ] AR-02: 처리 배정표를 닫는다 — Phase 행 일흔넷의 대상 계약 칸이 그 번호 Phase 슬러그와 글자 그대로 같고 QA 칸이 `APPROVE` 다. 미반영 여덟 행(`F09` · `F18` · `F20` · `F22` · `F25` · `F28` · `design:P2` · `user-setup:P2`)의 비고가 옛 비고로 시작하고 「 · 미반영 — 」 와 GAP 분석 미반영 표의 notes 파일 이름을 담는다. 다른 Phase 행의 비고와 Phase 가 아닌 행은 그대로이고, 검사기 `--final` 이 종료 코드 0 이다 [exact, enumerated]
      (측정: `python3 "$K/insights.py" "$T/B/.claude/kaizen-input/insights-report.md" "$T/E/.claude/kaizen-input/insights-report.md"` 가 `rows=96 same_rows=1 phase_rows=74 phase_ok=74 miss_ok=8/8 other_note=0 non_phase_changed=0` ·
       `python3 "$T/E/scripts/check-insights-tracking.py" --final "$T/E/.claude/kaizen-input/insights-report.md"` 종료 코드 0 · 출력에 `Phase 행 미완료 0` 과 `TRACKING_TABLE_OK` · `TRACKING_TABLE_FAIL` 0 줄.
       시작 판: `phase_ok=0 miss_ok=0/8` · 종료 코드 1 · `Phase 행 미완료 74`. 양성 대조: 칸을 다 채운 모의 판에서 Phase 6 행 여덟에 Phase 5 슬러그 → 검사기는 `TRACKING_TABLE_OK` 인데 `phase_ok=66`)
- [ ] AR-03: 문서 사이트(F2)를 다시 만든다 — GAP 분석 페이지 표의 마흔넷(`docs.py` `PAIRS`)이 모두 바뀌고 400 줄(api-kit 450 줄) 이상이며, `--accent` 가 시작 판과 같고, 외부 리소스를 부르지 않으며, `overflow hidden` 이 시작 판보다 늘지 않는다. `TOKENS` 의 새 글자 쉰여섯(원본 머리 설정 판 번호 열넷 포함)이 모두 페이지 본문에 있고 옛 글자 아홉이 모두 없다. `docs/` HTML 목록은 시작 판 그대로이고, `docs/index.html` 은 harness 다섯 항목(`skill-design` · `agent-design` · `contract-design` · `qa-evaluation` · `contract-schema`) 제목의 판 번호 다섯 줄만 원본 판 번호로 바뀐다. 원본 판 번호가 사이클 동안 바뀐 페이지 열넷은 새 판 번호를 본문에 담고, 그 가운데 harness 다섯 페이지는 `<title>` 에도 원본 판 번호를 담는다. 이 계약 서명 커밋이 건드린 HTML 은 그 마흔넷과 `docs/index.html` 이다. 끝 판에서 api-kit 문서 검사 · 내비 등록 검사 · 대비 수치 검사가 모두 종료 코드 0 이다 [exact, enumerated]
      (측정: `python3 "$K/docs.py" "$T/B" "$T/E"` 끝줄이 `pairs=44 exist=44 changed=44 short=0 accent=0 ext=0 hidden_up=0 tok_new=56/56 tok_old=0/9 html_added=0 html_removed=0` ·
       `git diff --numstat "$B" "$END" -- docs/index.html | tr '\t' ' '` 가 `5 5 docs/index.html` 한 줄 · `python3 "$K/navver.py" "$T/E"` 가 `nav_ver=5/5` · `python3 "$K/titlever.py" "$T/E"` 가 `title_ver=5/5` ·
       `type my >/dev/null || exit 2;` 뒤 `my | grep -E '^docs/.+\.html$' | grep -vxF docs/index.html | grep -c .` 44 · `my | grep -cxF docs/index.html` 1 ·
       `python3 "$T/E/scripts/check-api-kit-docs.py"` 종료 코드 0 · 끝줄 `12/12 PASS` · `python3 "$T/E/scripts/check-docs-links.py"` 종료 코드 0 · `내비 등록: 페이지 176 · 등록 176` · `python3 "$T/E/scripts/check-contrast-claims.py"` 종료 코드 0.
       시작 판: `changed=0 short=7 … tok_new=0/56 tok_old=9/9` · numstat 빈 출력 · `nav_ver=0/5` · `title_ver=0/5` · api-kit `10/12 PASS` 종료 코드 1 · 내비 176 · 176 · 대비 0.
       양성 대조: 임시 복제본에서 다섯 제목만 고쳐 커밋 → numstat `5 5 docs/index.html` · `nav_ver=5/5` · 내비 176 · 176 종료 코드 0, 한 제목만 고치면 `nav_ver=1/5`.
       페이지 사본 하나에 `v1.6.0` 을 넣으면 `tok_new=1/56`. `skill-design-guide` 페이지 `<title>` 만 고친 사본 → `title_ver=1/5`, 거기에 `contract-design-guide` 본문에만 `v5.1` 을 더해도 `1/5`)
- [ ] AR-04: changelog · 연구 기록에 이번 사이클 항목을 새로 더한다 — 다섯 파일(`docs/kaizen/changelog.md` · `flutter-changelog.md` · `research-log.md` · `flutter-research-log.md` · `docs/design/research-log.md`)마다 2026-09-24 를 담은 `##` 머리가 하나 더해지고, 더한 줄에 그 파일이 맡은 Phase 번호(changelog Phase 1 ~ 17 과 `Final` · flutter 둘 Phase 5 · kaizen 연구 기록 Phase 1 ~ 4 · 12 · 13 · 14 · 17 과 `Final` · design 연구 기록 Phase 6)가 모두 있다. 지운 줄은 머리 설정 `version:` · `last_updated:` 뿐이고, 더한 URL 은 모두 Phase notes · followups notes · 근거 파일에 있다. 연구 기록 셋(`docs/kaizen/research-log.md` · `flutter-research-log.md` · `docs/design/research-log.md`)은 더한 줄에 서로 다른 출처 URL 이 5 개 이상이다(오케스트레이터 F4 3 번). per-kit 연구 기록 여섯(`docs/{backend,infra,rust,react,flutter,planning}/research-log.md`)은 Phase 가 쓴 이번 사이클 `##` 머리를 하나씩 담는다(확인만 — 이 계약은 고치지 않는다) [exact, enumerated]
      (측정: `python3 "$K/logs.py" "$T/B" "$T/E"` 끝줄 `files=5 bad=0` · 다섯 줄 모두 `head=1 missing=[]` · `del_bad=0 url_out=0` · 연구 기록 세 줄의 `urls=` 5 이상 ·
       `for k in backend infra rust react flutter planning; do grep -cE '^## .*2026-09-2[45]' "$T/E/docs/$k/research-log.md"; done | tr '\n' ' '` 가 `1 1 1 1 1 1 `.
       시작 판: `files=5 bad=15` (연구 기록 셋 `urls=0`) · per-kit `1 1 1 1 1 1 ` (사이클 기준 판 `CB` 에서 같은 반복은 `0 0 0 0 0 0 `).
       양성 대조: 모의 판 changelog 에 근거 파일 밖 URL 한 줄 → `url_out=1`. 연구 기록 셋 첫 `##` 앞에 날짜 머리 새 항목을 끼운 모의 판 — 아는 URL 다섯 → `bad=0`, 넷 → `bad=3`)
- [ ] AR-05: 사이클 상태 · 실패 횟수 · evals 점검 기록이 이번 사이클을 가리킨다 — `kaizen-state.yaml` 이 `cycle_id: "kaizen-2026-09-24"` · `status: completed`, 실패 횟수 파일이 `phase_1` ~ `phase_17` 열일곱 키만 0 으로 갖고 `last_updated` 에 2026-09-24 가 있으며, `evals-audit-2026-09-24.md` 가 sync-evals 요약 줄 · evals.json 열 경로 · 스킬 더함 · 지움 · 이름 바꿈을 찾은 `git diff --name-status` 명령을 담는다. 사이클 동안 스킬 · 에이전트 파일의 더함 · 지움 · 이름 바꿈이 0 이라 evals.json 은 고치지 않는다 [exact]
      (측정: `python3 "$K/meta.py" "$T/E"` 가 `state=1 phases=17 keys_ok=1 zero=1 last_updated=1 evals=[total_line=1 paths=10/10 adr_cmd=1]` ·
       `git diff --name-status -M "$CB" "$END" -- '*/skills/*/SKILL.md' '*/agents/*.md' | grep -vc '^M'` 0.
       시작 판: `state=0 phases=14 keys_ok=0 zero=0 last_updated=0 evals=[MISSING]` · 0. 양성 대조: 복제본에서 `cycle_id` 만 바꾸면 사후 점검 날짜 검사 다섯이 FAIL — 이 조건이 없으면 DG-05 의 날짜 검사가 옛 항목으로 통과한다)
- [ ] AR-06: 메모리 승격 후보(F3.5)를 낸다 — `.harness/.meta/memory-promotion-candidates-2026-09-24.md` 의 첫 yaml 블록이 `# kaizen-memory-candidates` 로 시작하고 `cycle_id: kaizen-2026-09-24` · 시간대 붙은 `generated_at` 을 가지며, 모든 후보가 오케스트레이터 F3.5 포맷 열세 키만 갖고, 판정 결과 키(`promoted_to` · `rule_id` · `enforcement_level` · `status`)가 파일에 0 개다. `grounding` 은 `self_inference` 가 아닌 세 값 가운데 하나, `actionability` 는 `claude_behavior`, `source_evidence` 경로는 모두 있고, 저장소 경로이거나 `~/.harness/` 아래다 — `/private/tmp` · `/tmp` 아래 경로는 0 개다(세션이 끝나면 사라진다). `lint-new-warning-added-lines-only` · `scope-count-signed-commits-only` 두 후보가 있다. 승격 원장은 만들지 않는다 [exact]
      (측정: `python3 "$K/mem.py" "$T/E"` 가 `parse=1 candidates=N keys_bad=0 forbidden=0 grounding_bad=0 actionability_bad=0 evidence_bad=0 need=2/2 tmp_bad=0 out_bad=0` 이고 N 2 이상 ·
       `find "$HOME/.claude/logs" -name promotions-ledger.md | grep -c .` 0. 시작 판: `MISSING` · 0. 양성 대조: 모의 파일에 `status: active` 와 `self_inference` → `keys_bad=2 forbidden=2 grounding_bad=2`,
       근거 한 줄을 스크래치 `xdiag-all.md`(지금은 있는 경로)로 → `evidence_bad=0 … tmp_bad=1 out_bad=1`, `$HOME/.claude/CLAUDE.md` 로 → `tmp_bad=0 out_bad=1`.
       음성 대조: 오케스트레이터 F3.5 틀대로 따옴표 없이 쓴 `generated_at: 2026-09-25T20:00:00+09:00` → `parse=1`(고치기 전 식은 `parse=0`), 시간대 없는 시각 → `parse=0`)
- [ ] AR-07: 감사 기록에 이번 사이클 항목을 붙인다 — 새 판이 시작 판 전체로 시작하고(지우거나 고친 줄 0), 붙은 부분에 `append-audit-log.py` 가 찍는 머리 줄 `## <날짜> — kaizen/2026-09-24` 과 생성 줄(`scripts/append-audit-log.py` 와 `(auto-append)` 를 담은 `**Generated:**` 줄)이 하나씩, 수동 편집 절에 `.claude/skills/kaizen-orchestrator/SKILL.md` 가 있다. 두 followups 가 고치지 않은 ID 스물아홉(`F1H-14` … `F1H-94`) · 행 서른셋(`F1K-10` … `F1K-80`) · 구현 중 새로 찾은 넷(`F1H-N1` ~ `F1H-N4`)과 Phase notes 열일곱 파일 이름이 모두 붙은 부분에 있다. 두 후속 notes 파일 이름(`f1-harness-followups-notes.md` · `f1-kit-followups-notes.md`)과 이번 사이클 메타 이슈 여섯 글자(`kaizen-state.yaml` · `feedback-archive` · `check-insights-tracking.py` · `append-audit-log.py:148` · `FN-79` · `FN-80`)도 붙은 부분에 있다 [exact, enumerated]
      (측정: `bash "$K/audit.sh" "$T/B" "$T/E"` 가 `append_only=1 head=1 generated=1 manual_orch=1 f1h=29/29 f1k=33/33 new4=4/4 notes=17/17 fnotes=2/2 meta=6/6`. ID 목록은 `audit.sh` 의 `F1H` · `F1K` 배열 — 두 notes 의 다음 사이클 메모 표 · 고치지 않은 항목 표와 같다. 두 notes 이름 · 메타 글자는 `FN` · `MT` 배열이다.
       시작 판: `append_only=1 head=0 generated=0 manual_orch=0 f1h=0/29 f1k=0/33 new4=0/4 notes=0/17 fnotes=0/2 meta=0/6`. 양성 대조: 모의 판(도구 `render_entry` 출력 + ID 목록 + 메타 절)에서 기대 줄 그대로, 메타 절만 빼면 `meta=0/6`, 수동 편집 JSON 경로를 틀리면 `manual_orch=0`)
- [ ] AR-08: Final notes 가 측정 도우미의 실제 출력과 대응 페이지 없는 원본을 담고, 범위 상한이 notes 커밋이다 — `.harness/.meta/kaizen-0924/final-notes.md` 에 필수 소제목 여섯이 하나씩 있고, 끝 판에서 다시 돌린 `f1.sh` 네 줄 · `tonegrade.py` 첫 줄 · `toneterms.py` 첫 줄 · `synt.sh` 끝줄 · `amend.sh` 끝줄이 글자 그대로 있으며, GAP 분석의 대응 페이지 없는 원본 열아홉 경로가 모두 있다. `## 다음 사이클 메모` 절이 입력 표에서 처리 칸이 `고치지 않음` 인 열하나(`FN-18` · `FN-39` · `FN-43` · `FN-56` · `FN-58` · `FN-64` · `FN-76` · `FN-77` · `FN-78` · `FN-79` · `FN-80`)와 두 후속 notes 파일 이름을 담는다. 개정 파일 마지막 `end_sha:` 가 notes 를 마지막으로 바꾼 커밋이다 [exact, enumerated]
      (Given: notes 커밋 뒤 `end_sha` 를 덧붙인 뒤 · 측정: `type my >/dev/null || exit 2;` 뒤 `. "$K/notes.sh"` 가 `heads=6/6 lines=8/8 nohtml=19/19 memo=13/13` 이고 `MISS` 줄 0 ·
       `[ "$(git log -1 --format=%H "$END" -- "$NOTES")" = "$(git rev-parse "$END^{commit}")" ] && echo 1` 이 1.
       시작 판: `MISSING .harness/.meta/kaizen-0924/final-notes.md` 종료 코드 2. 양성 대조: 모의 notes 에서 amend 줄을 빼면 `lines=7/8` · `MISS ends=…`, `FN-80` 을 메모 절 밖(넘기는 것)에만 두면 `memo=12/13`)
- [ ] AR-09: 이 계약 변경이 허용 경로 안에 머물고 이 계약이 봉인돼 있다 — 서명 커밋이 건드린 파일이 `.harness/` · 처리 배정표 · 페이지 마흔넷 · `docs/index.html` · `docs/kaizen/` · `docs/design/research-log.md` · `CLAUDE.md` 밖에 0 개이고(루트 `README.md` 는 허용 밖), 구간 안에서 킷 폴더 열넷 · `scripts/` · `.claude/skills/` · `.github/` · `.claude-plugin/` 을 건드린 커밋과 서명 없는 커밋이 0 이며, 끝 판 계약 가운데 `SEAL_BROKEN` 이 0 이고 이 계약은 `SEAL_OK`, 첫 서명 커밋(봉인 커밋)은 파일 하나다 [exact, enumerated]
      (Given: 이 계약 커밋이 끝난 뒤 · 측정: `type my verify_seal >/dev/null || exit 2;` 뒤 `. "$K/range.sh"` 가 `outside=0 html_extra=0 forbidden=0 unsigned=0 broken=0 self=SEAL_OK seal_files=1`.
       양성 대조: 임시 복제본 — 서명 커밋이 `scripts/` 한 파일과 목록 밖 페이지를 고치고 서명 없는 커밋을 더하고 가짜 봉인을 둔 판 → `outside=1 html_extra=1 forbidden=1 unsigned=1 broken=1 self=SEAL_BROKEN seal_files=1`.
       `README.md` · `docs/index.html` · `CLAUDE.md` · `harness/README.md` 네 경로를 `ALLOW` 식으로 거르면 허용 밖은 `README.md` · `harness/README.md` 둘)

## Anti-patterns

- [ ] AP-01: 버전을 하드코딩하지 않는다 — plugin.json에서 읽어야 한다. 이번 변경에 적용: 이 계약이 쓰는 마크다운 열여덟(공통 정의 `MDS`)에 더한 줄에 킷 열넷 `plugin.json` 의 `version` 값(끝 판에서 읽는다)이 0 건이다 — 릴리스 계획도 판 번호를 적지 않고 단계만 적는다 [exact]
      (측정: `type added_md >/dev/null || exit 2; V=$(cd "$T/E" && python3 -c 'import json,glob; print("|".join(sorted({json.load(open(p))["version"].replace(".","\\.") for p in glob.glob("*/.claude-plugin/plugin.json")})))'); added_md | grep -cE "(^|[^0-9.])($V)([^0-9.]|$)"` 0.
       양성 대조: 「harness 0.13.0 로 올린다」 한 줄 → 1, 「contract-schema v5.5 · skill-design-guide 1.6.0」 → 0)
- [ ] AP-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수 (```` ```text, ```bash, ```yaml ```` 등). 판정 권위는 validate-plugin V6 상태기계다 — 여는/닫는 fence 가 동형이라 줄 단위 정규식으로는 판정 불가. 이번 변경에 적용: V6 는 `.harness/` · `docs/kaizen/` 를 읽지 않으므로 같은 여닫기 방식으로 마크다운 열여덟을 직접 세어 언어 힌트 없는 여는 펜스 · 닫히지 않은 펜스가 0 이다 [exact]
      (측정: `python3 "$K/fence.py" $(for f in "${MDS[@]}"; do echo "$T/E/$f"; done)` 끝줄 `bare_open_total=0 unclosed_total=0`. 시작 판: 같은 명령(있는 파일만) `0 0`. 양성 대조: 사본 끝에 언어 이름 없는 펜스 한 쌍 → `bare_open_total=1`)

## Reusability

- [ ] RE-01: N/A (산출물에 재사용 단위 코드(컴포넌트 · 함수 · 모듈)가 없다 — 이 계약 서명 커밋이 싣는 파일은 기록 마크다운 · YAML · HTML 뿐이다. 측정 도우미는 계약 안 블록이다. 측정: `type my >/dev/null || exit 2;` 뒤 `my | grep -cE '\.(py|sh|js|ts|mjs)$'` 0. 양성 대조: 모의 목록에 `scripts/x.py` → 1)
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다. 이번 변경에 적용: 감사 기록 항목은 `scripts/append-audit-log.py` 로 만들고(AR-07 `generated=1`), 페이지는 킷별 기존 accent 를 그대로 쓰며(AR-03 `accent=0`), 저장소에 새 스크립트를 더하지 않는다 [exact]
      (측정: `bash "$K/audit.sh" "$T/B" "$T/E"` 의 `generated=1` · `python3 "$K/docs.py" "$T/B" "$T/E"` 끝줄의 `accent=0` · `type my >/dev/null || exit 2;` 뒤 `my | grep -cE '^(scripts|harness/scripts)/'` 0)

## Diagnostics

- [ ] DG-01: N/A (`commands.analyze` 는 `bash -n scripts/release.sh` 라 `scripts/release.sh` 만 잰다 — 이번 변경 파일과 교집합 0 개. 측정: `type my >/dev/null || exit 2;` 뒤 `my | grep -c '^scripts/release.sh$'` 0. 사이클 전체 셸 문법은 SK-01 (f) 가 잰다)
- [ ] DG-02: IDE diagnostics 워닝/인포 0개 (`diagnostics.ide_exclude` 값 `[]`) — 이번 변경에 적용: 마크다운 열여덟(`MDS`)을 편집기 마크다운 확장과 같은 조건(markdownlint-cli2 0.23.2 · MD013 끔)으로 재어 파일마다 (규칙, 그 줄 글자) 묶음이 시작 판보다 늘지 않았다. 예외는 `append-audit-log.py` 가 찍는 고정 소제목 세 줄(`### Post-Kaizen Checklist failures` · `### Orchestrator SKILL.md manual edits` · `### Next-cycle watchlist`)의 MD024 셋뿐이다. YAML 은 SK-01 (f) 가 읽히는지 재고, HTML 은 편집기 검사 대신 DG-04 가 브라우저로 잰다 [exact]
      (측정: `VERBOSE=1 bash "$K/mdcmp.sh" "$T/B" "$T/E" "${MDS[@]}"` 끝줄 `new_total=3` · `NEW` 줄이 정확히 셋이고 모두 `NEW .harness/.meta/orchestrator-audit-log.md MD024` 뒤에 위 세 소제목 가운데 하나 — `… | grep '^NEW ' | tr '\t' ' ' | grep -vcE '^NEW \.harness/\.meta/orchestrator-audit-log\.md MD024 ### (Post-Kaizen Checklist failures|Orchestrator SKILL\.md manual edits|Next-cycle watchlist)$'` 0 · `… | grep -c '^NEW '` 3.
       시작 판: `new_total=0`. 양성 대조: 모의 판에서 도구 출력을 빈 줄 없이 붙이면 MD022 · MD032 새 묶음(`NEW` 다섯 · 걸러낸 뒤 둘), 맨 URL 한 줄 · 옛 제목 한 줄이면 `new=2 MD024:1 MD034:1`.
       음성 대조: 연구 기록 셋 · changelog 둘의 첫 `##` 앞에 경고 없는 새 항목을 끼운 모의 판 → 다섯 파일 모두 `new=0` (고치기 전 sed 식은 열 번호를 줄 번호로 읽어 `new_total=18` 로 잘못 셌다))
- [ ] DG-03: N/A (`commands.test` 는 `bash scripts/release.sh 2>&1 || true` 라 `scripts/release.sh` 만 잰다 — 교집합 0 개. 측정: DG-01 과 같은 명령 0. 실제 시험은 DG-05 가 끝 판 복제본에서 돌린다)
- [ ] DG-04: 실제 앱/서버 구동 시 에러 0개 — 이번 변경에 적용: 다시 만든 페이지 마흔넷을 실제 브라우저(`scripts/check-docs-a11y.js`, playwright-core)로 띄워 콘솔 에러 · 가로 넘침(375 · 768 · 1280px) · 대비 실패 · 터치 타깃이 모두 0 이고, 끝 판 `docs/` HTML 전체도 같은 검사를 통과한다 [exact]
      (측정: 작업 폴더에서 `node scripts/check-docs-a11y.js $(python3 -c 'import re,sys; s=open(sys.argv[1],encoding="utf-8").read(); print(" ".join(sys.argv[2]+"/"+p for p in re.search(r"PAIRS = \"\"\"(.*?)\"\"\"", s, re.S).group(1).split()[1::2]))' "$K/docs.py" "$T/E")` 종료 코드 0 · 끝줄 `44/44 PASS` · 모든 `OK` 줄이 `err=0` ·
       `node scripts/check-docs-a11y.js $(find "$T/E/docs" -name '*.html')` 종료 코드 0 · 끝줄 `177/177 PASS`.
       시작 판: `44/44 PASS` · `177/177 PASS`. 양성 대조: 사본 페이지에 폭 2000px · 대비 1.11 인 줄 → `0/1 PASS` 종료 코드 1)
- [ ] DG-05: 끝 판을 새로 복제해 돌린 저장소 검사 · CI 시험 · 사후 점검이 모두 통과한다 — `validate-plugin.py` · `sync-docs.py` · `sync-evals.py` · `sync-orchestrator.py` 세 `--check-only` · `run-evals.py` · `check-stale-values.py` · `validate-doc-contracts.py` · 문서 검사 셋 · CI 시험 열하나가 모두 종료 코드 0 이고, `validate-post-kaizen.py --since <사이클 기준>` 이 종료 코드 0 · PASS 13 · FAIL · ERROR 0 · SKIP 은 버전 두 줄(`marketplace-sync` · `plugin-json-bumps`)뿐이다 [exact]
      (Given: 이 계약 커밋이 끝난 뒤 · 측정: `bash "$K/dg05.sh" "$END" "$CB"` 끝줄이 `rc=[000000000000000000000] vpk_rc=0 vpk_pass=13 vpk_bad=0 vpk_skip=[marketplace-sync plugin-json-bumps]` 이고 `NONZERO` 줄 0.
       시작 판(`HEAD`): `rc=[000000000100000000000] vpk_rc=1 vpk_pass=12 vpk_bad=1` — 열째(`check-api-kit-docs.py`) 1 · `docs-site-regen` FAIL, 날짜 검사 다섯은 옛 사이클 항목으로 PASS.
       음성 대조: 복제본에서 `kaizen-state.yaml` 의 `cycle_id` 만 새 사이클로 바꾸면 FAIL 여섯 · 종료 코드 1 — 기록 산출물이 빠지면 이 측정이 떨어진다)
