---
feature: "카이젠 2026-09-24 PR 직전 검토 지적 수정 (Claude 검토 A 여덟 · B 열넷 · Codex 2 차 검토 확정 지적)"
slug: kaizen-0924-f2-review-fixes
created: "2026-09-26 02:29"
complexity: "복잡"
conditions: 30
status: active
owner_session: de8c7935-a5b6-4df5-9106-fafa73c288a0
conditions_digest: sha256:1d2980c691dc41b0
locked_at: "2026-09-26 03:38"
---

## 배경

카이젠 2026-09-24 가지 `kaizen/2026-09-24` 는 Final 까지 마치고(`kaizen-0924-final` QA APPROVE 26/26) main 을 합쳤다(`6a8be19`). PR 을 올리기 전에 독립 검토 둘을 돌렸다.
하나는 Claude 검토 워크플로(찾기 셋 + 지적마다 반박 검토 셋, 두 표 이상 유지 = 확정)이고 결과를 `review-fixes.md` 가 A · B · C 로 나눴다 —
A 확정 여덟(중간)은 전부 고치고, B 는 낮음 가운데 사실이 틀렸거나 한두 줄로 끝나는 열넷이라 고치고, C 는 나머지 · 반박된 지적이라 다음 사이클로 넘긴다.
다른 하나는 Codex 2 차 검토(`r4-final.md`, `gpt-5.6-sol` 읽기 전용, 두 회차)다 — 새 발견 넷 가운데 둘은 A1 · B14 와 같은 자리, 하나(N2)는 넘겼던 일인데 계약 초안 검토 뒤 오케스트레이터 한 줄로 고치기로 했고, 하나(N4)는 재현 안 됨이다.
앞선 21 건 상태표의 「일부」 · 「고치지 않기로 함」 은 이 계약이 지적마다 다시 확인해 `## 범위 경계` 입력 항목 표에 처리를 적었다.

이 계약은 A · B 와 Codex 확정 지적이 가리키는 파일, 그 파일을 재는 시험 · 픽스처, `.github/workflows/ci.yml`(시험 단계), 루트 `README.md`(수치),
그리고 원본이 바뀐 문서 사이트 페이지의 해당 절만 고친다. 지적마다 봉인 전에 시작 판에서 재현했다(`## 회귀 게이트` 봉인 전 실측).

## 리서치 소스

이 계약은 바깥 자료를 새로 찾지 않는다. 입력은 모두 이 세션 스크래치와 레포 안에 있다.

- 고칠 목록 `/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/de8c7935-a5b6-4df5-9106-fafa73c288a0/scratchpad/kaizen/review-fixes.md`
  (C 는 줄이 잘려 있어 전문은 `…/tasks/w5ft0hgez.output` 의 `result.low` · `result.rejected` 에서 읽었다)
- Codex 2 차 검토 `…/scratchpad/kaizen/codex/r4-final.md` (프롬프트 `r4-final.txt`). `run4.sh` 의 재시도 조건(`r4.err` 에서 「usage limit」 글자 찾기)이 검토 글 안의 같은 글자에 걸려 두 번 돌았다 —
  1 회차(02:00)는 2 회차(02:16)가 덮어써 초안 작성자가 읽은 글을 `r4-final-run1.md` 로 옮겼다. 두 회차를 모두 입력으로 받는다(아래 표는 「1 회차 n」 · 「2 회차 Rx-y · Nn」 으로 가리킨다)
- Final 지침 `…/scratchpad/kaizen/final-runbook.md` §PR 직전 검토 수정 계약 · 공통 지침 `phase-runbook.md` 의 계약 규칙 · git 규칙 · 말투 규칙 · 검증
- 계약 초안 검토 `.harness/.meta/kaizen-0924/f2-review-fixes-review.md` (REVIEW 에이전트, `VERDICT: CHANGES` — 꼭 고칠 것 둘 · 권함 넷 · 선택 셋). 반영 내역은 `## 범위 경계` 「계약 초안 검토 반영」 줄
- `final-todo.md` §PR 직전 — 메인 루프 몫(합침 · 재실행 · Codex 2 차 검토)이라 이 계약은 그 결과만 입력으로 받는다
- 레포: 지적이 가리키는 파일 스물여덟과 그 시험(`## GAP 분석` Pre-Edit 표)

## GAP 분석 · 개선안 초안

### 복잡도 (Step 1)

| 축 | 물음 | 값 |
| -- | ---- | -- |
| 레이어 수 | 몇 계층을 관통하는가 | 넷 — 스킬 문서 · 셸/파이썬 스크립트 · 킷 시험 · CI 설정과 문서 사이트 페이지 |
| 공개 API · 계약 변경 | 외부에 노출된 형태가 바뀌는가 | 예 — 결정 전파 검사 종료 코드(모양 오류 → 2) · reflect `.errors.log` 새 줄 `ok:no-issues` · 옛 값 검사 범위 |
| 소비면 존재 | 반대편이 있는가 | 예 — 종료 코드를 읽는 design-test · design-audit · design-reviewer (SK-03) · `.errors.log` 를 읽는 `collect_status` · SCHEMA.md · DESIGN.md · reflect-digest (ER-04) · 페이지 일곱 (AR-02) |
| 회귀 위험 | 기존 동작이 깨질 수 있는가 | 예 — reflect 훅 · 수집 상태, 봉인 범위 블록, CI |

넷 다 예라 **복잡**이다. 공개 형태 변경 + 소비면이 있어 Step 2.5 양면 조건을 넣었다 — 생산 쪽 ER-02 · ER-04 와 소비 쪽 SK-03 · ER-04 뒤 절 · AR-02.
기능 조건은 스물이다(상한).

### 설정 리터럴 대조 (Step 1.2)

| config key | project.yaml 에서 읽은 값 | 계약에 쓴 값 |
| ---------- | ------------------------- | ------------ |
| `commands.analyze` | `bash -n scripts/release.sh` | `bash -n scripts/release.sh` (DG-01 N/A 사유) |
| `commands.test` | `bash scripts/release.sh 2>&1 \|\| true` | 같음 (DG-03 N/A 사유) |
| `diagnostics.ide_exclude` | `[]` | `[]` (DG-02) |
| `contract_categories[].id` / `prefix` | Skill/SK · Script/SC · Error/ER · Architecture/AR | 같음 |
| `anti_patterns[].id` / `message` | AP-01 버전 하드코딩 · AP-02 force push · AP-03 bare fence · AP-04 frontmatter name | AP-01 · AP-03 · AP-04 (AP-02 는 이 계약이 push 하지 않아 뺀다) |

### Pre-Edit 감사 (Step 1.4)

| 대상 파일 | 실제 Read 증거 (`파일:라인`) | 발견한 기존 갭 · 위반 | 조건 |
| --------- | ---------------------------- | ------------------- | ---- |
| `scripts/check-stale-values.py` | `:45` ~ `:48` `EXCLUDED_KITS = {"backend-kit": …}` · `.harness/stale-values.yaml:20` ~ `:25` allow 셋 | 풀 조건(allow 등록)이 이미 채워졌는데 제외가 남았다 (A1 · Codex r4 새 발견 2) | ER-01 |
| `.claude/skills/react-kaizen/SKILL.md` · `design-kaizen/SKILL.md` | react `:82` 서명 줄 없는 커밋 명령 · design `:33` 「직접 실행하지 마라」 · `:81` 「Phase 로 호출한 경우 이 Step 을 실행하지 마라」 · `:82` 「커밋은 오케스트레이터에 넘긴다」 · 오케스트레이터 `:196` 서명 줄 | 두 스킬의 커밋 주체가 반대, 서명 줄 없음 (A2) | SK-01 |
| `.claude/skills/{backend,design,infra,rust}-kaizen/SKILL.md` | backend `:32` · design `:31` · infra `:29` · rust `:34` I-02 줄 | 슬러그 QA 산출물 · 개정 경로 없음, rust 는 슬러그 계약 경로도 없음 (B2) | SK-01 |
| `.claude/skills/kaizen-orchestrator/SKILL.md` | `:25` 「Phase 17 표는 아직 없다」 뒤 대신 읽을 출처 없음 · `:583` 스킬 수 · `:608` 「docs-site 스킬 Step 1 참조」 · `:624` api-kit 행 · `:622` onboarding 행 · `:478` Phase 12 범위(AUTO `:409` ~ `:528` 안) | 수 둘 틀림 (B3) · 표가 detect-docs-drift 와 어긋남 (B5) · docs-site 표 7 행 (B13) · AUTO 범위 줄과 phase-dependencies 차이 (B12) · 「최소 3 건 조회」 규칙과 「Phase 17 표 없음」 이 한 줄에서 어긋남 (Codex N2) | SK-02 |
| `.claude/skills/tone-kaizen/SKILL.md` · `docs-site/SKILL.md` | tone `:35` 「8종」(실제 11) · docs-site `:47` ~ `:55` 7 행 | B4 · B13 | SK-02 |
| `harness/references/contract-schema.md` | `:607` ~ `:608` `type verify_seal fm_get` · `:304` ~ `:321` 봉인 함수 넷 | 넷 가운데 둘만 확인 (B1) | ER-03 |
| `react-kit/skills/react-l10n/SKILL.md` | `:173` ~ `:176` 둘째 줄 `grep -E` | 0 건이면 블록 종료 코드 1 (A3) | SK-05 |
| `design-kit/references/visual-change-protocol.md` | `:405` ~ `:452` 검사 코드 · `:420` `doc.get` · `:434` `x.get("reason")` · `assertions` 형 확인 없음 | 모양 틀린 입력이 종료 코드 1 로 멈춤 · 문자열 `assertions` 는 멈추지 않고 위반(1)으로 잘못 분류 (A4 · 계약 초안 검토) | ER-02 |
| `design-kit/skills/design-test/SKILL.md` · `design-audit/SKILL.md` · `agents/design-reviewer.md` | test `:303` · `:366` 「위반 0」 · audit `:115` ~ `:117` · reviewer `:178` ~ `:179` | 종료 코드 2 · 3 을 모른다 (A5) | SK-03 |
| `flutter-toolkit/skills/flutter-scenario-report/SKILL.md` · `references/record-format.md` · `evals/scenario-report/` | SKILL `:4` `Flutter Playwright MCP` · `:19` `find_widget` · `verify_visible` · `:44` 「이 파일에 적지 않는다」 · record-format `:38` · `:39` · `:62` `fitpal-mobile` · `tap_native_point` · 시험 `:56` · 예시 record.json `:81` · `:85` · `:96` | 스킬 자기 규칙 · 이 가지 규칙과 어긋남 (A6) | SK-04 |
| `flutter-toolkit/skills/flutter-preflight/SKILL.md` | `:138` `2. codegen : success ·` 고정 | 실패 틀이 성공으로 적힌다 (B8) | SK-04 |
| `reflect-kit/hooks/log-reflection.sh` · `_lib-project-id.sh` · 시험 둘 · 문서 셋 | 훅 `:317` 「noissues」 면 흔적 없이 끝 · lib `:188` ~ `:211` 마지막 기록 뒤 실패만 셈 · SCHEMA `:136` ~ `:147` · DESIGN `:174` ~ `:191` · digest `:35` Gotcha 13 · `:78` `## 입력` 의 `.errors.log` 설명 줄 | 정상 실행 뒤 실패 한 번에 멈춤 경고 (A7) | ER-04 |
| `api-kit/skills/api-ui/SKILL.md` | `:168` 「두 명령은 한 번의 셸 호출에서 잇는다」 | bash `&&` 이음이면 번호 · 폴더가 틀린다 (A8) | SK-07 |
| `rust-kit/skills/rust-audit/SKILL.md` | `:33` `grep -c '.unwrap()' src/` · `:36` 「rust-run (c)」 · rust-run `:78` · `:91` ~ `:92` | 폴더를 못 센다 (B9) · 없는 자리를 가리킨다 (B7) | SK-06 |
| `onboarding-kit/skills/setup-guide/SKILL.md` · `evals/evals.json` | SKILL `:63` ~ `:76` misplaced 판정 · evals `gate_cases` 여섯 · 러너 고아 픽스처 검사 | 판정을 지키는 시험 없음 (B10) | ER-05 |
| `bambu-kit/skills/bambu-print-profile/SKILL.md` | `:2466` ~ `:2469` 댓글 페이지만 지움 · `:2489` `load(out / "design.json")` | 받기 실패 때 옛 모델 파일을 보고 (B11) | SK-08 |
| `.github/workflows/ci.yml` | `:87` 이후 validate 잡 — scenario-report 시험 없음 | B6 · C L13 | ER-06 |
| `README.md` | `:157` · `:162` · `:264` 19종 | B14 · Codex r4 새 발견 1 | SK-04 |
| 문서 사이트 페이지 일곱 | `docs/harness/contract-schema.html` 의 `type verify_seal fm_get` 1 줄 · `docs/design-kit/visual-change-protocol.html:878` 검사 코드 · `docs/design-kit/design-test.html:656` · `:845` · `:900` 「위반 0」 · `docs/bambu-kit/bambu-print-profile.html:582` · `docs/reflect-kit/schema.html` · `design.html` 태그 목록 · `docs/api-kit/static-evidence-viewer-contract.html:834` | 원본이 바뀌면 같은 절이 옛 판으로 남는다 | AR-02 |

### 개선안 (조건과 같은 순서)

1. **A2 · B2** — design-kaizen 두 자리(Gotcha 7 · Step 5 의 「이 Step 을 실행하지 마라」 · 「커밋은 오케스트레이터에 넘긴다」)를 react-kaizen 과 같은 규칙(Phase 가 제 경로만 경로 지정 커밋)으로 바꾸고, 두 스킬의 명령에 서명 줄 `-m "Kaizen-Phase: <슬러그>"` 를 넣는다.
   I-02 목록 넷에 `.harness/sprint-contract-<slug>.md` · `.harness/sprint-feedback-<slug>.md` · `.harness/sprint-amendments-<slug>.md` 를 같은 모양으로 넣는다 (SK-01)
2. **B3 · B4 · B5 · B12 · B13** — 오케스트레이터 Final 조건 줄의 수(12 · 4), tone-kaizen 의 `docs/tone/*.md` 수(11), F2 표 api-kit 행에서 `api-kit/references/` 를 빼고
   onboarding 예제를 파일 하나(`docs/onboarding-kit/examples/fcm-ios-setup-guide.md`)로 좁혀 detect-docs-drift 와 맞춘다. docs-site Step 1 표를 F2 표와 같은 열다섯 행으로 늘린다
   (F2 표 머리의 「docs-site 스킬 Step 1 참조」 는 그대로 참이 된다). B12 는 AUTO 영역을 손으로 고칠 수 없으므로 AUTO 밖 「각 Phase 공통 실행 패턴」 에
   「넘기는 범위 = AUTO 범위 줄 + `references/phase-dependencies.md` 목록」 한 줄을 넣는다 — 생성기(`scripts/sync-orchestrator.py`)는 C L7 과 같은 자리라 다음 사이클.
   **Codex N2** — `:25` 괄호를 「(Phase 17 표는 아직 없다 — 표가 생길 때까지 Phase 17 은 `.claude/skills/howto-research/SKILL.md` Step 1 표의 1차 출처에서 3 건 이상을 조회한다)」 로 바꾼다.
   표를 새로 만들지 않고 이미 있는 출처 표를 가리킨다 (SK-02)
3. **A5** — design-test (Step 5-b 끝 문단 · Step 7 표) · design-audit Step 5 · design-reviewer 판정 규칙에 「종료 코드 2(`SCHEMA_ERROR`)는 판정 불가라 REJECT(design-test 는 통과로 읽지 않는다) ·
   종료 코드 3(`NO_SURFACE` · `NO_DECISION`)은 `NO_MANIFEST` 와 같이 대상 0 건 보고」 를 넣고 「위반 0」 을 「종료 코드 0」 으로 바꾼다 (SK-03)
4. **A6 · B8 · B14** — scenario-report SKILL.md 설명과 Gotcha 에서 서버 · 도구 이름을 빼고(설명은 「MCP 로」, Gotcha 는 「위젯 찾기 · 보임 확인 도구처럼 프로젝트 설정에서 읽은 도구」),
   record-format 예시의 도구 · 서버 이름을 자리표시(`<서버명>` · `<도구명>`)와 「위젯 찾기」 로 바꾼다. 킷 시험 · 예시 기록의 `fitpal` 을 일반 이름으로 바꾸고 예시 보고서를 스크립트로 다시 만든다
   (시험이 바이트로 대조한다). 설명이 바뀌므로 `python3 scripts/sync-docs.py flutter-toolkit` 로 킷 README AUTO 를 맞춘다. 메인이 가져온 스킬의 자기 규칙(44 행 「이 파일에 적지 않는다」)과
   이 가지 규칙(킷 파일에 특정 앱 · 도구 이름을 적지 않는다)이 같은 방향이라 두 문서와 예시만 최소로 고친다. flutter-preflight 실패 틀 codegen 줄을 flutter-build 와 같게. 루트 README 세 자리를 20 으로 (SK-04)
5. **A3** — 둘째 줄을 `awk '/^-(msgstr "[^"]|")/{print; n++} END{print "filled_deleted=" n+0}'` 로, 주석과 뒤 문장을 새 끝 줄에 맞춘다 (SK-05)
6. **B7 · B9** — Gotcha 16 을 「rust-run §2 첫 항목과 같다」 로, 0 건 설명 명령을 `grep -rF --include='*.rs' '.unwrap()' src/ | awk 'END{print NR}'` 로 바꾸고, 같은 줄 끝에
   「위 명령은 `src/` 가 없으면 오류는 화면에만 나오고 0 이 찍힌다 — (a) 로 거른다」 를 덧붙인다 — 파이프 끝 awk 가 grep 의 종료 코드 2 를 가리는 모양이라 바로 아래 Gotcha 16 이 경고하는 경우다 (SK-06)
7. **A8** — 여는 방법 항목에 한 덩어리 bash 블록(첫 줄 `D=$(mktemp -d) && cp .api/ui.html "$D/" || exit 1`, 둘째 줄 서버 `& sleep 1`, 셋째 줄 판정)을 넣고
   「줄바꿈이나 `;` 로 잇고 `&&` 로 잇지 않는다 — bash 는 목록 전체를 하위 셸로 보낸다」 와 bash · zsh 확인 결과를 적는다 (SK-07)
8. **B11** — 댓글 페이지를 지우는 줄 옆에서 `design.json` · `instances.json` 도 지운다 (SK-08)
9. **A1** — `EXCLUDED_KITS` 를 비운다 (ER-01)
10. **A4** — 검사 코드가 맨 위 · `decisions` · 결정 하나 · `required_surfaces` · `excluded_surfaces` 목록과 그 항목 · `assertions` 의 형(문자열이면 틀림)이 틀리면 `SCHEMA_ERROR` 를 찍고 schema 로 세어 종료 코드 2 로 끝낸다.
    새 킷 시험 `design-kit/evals/decision-gate-test.sh` 는 부를 때마다 문서에서 코드를 떼어 입력 열(`assertions` 문자열 포함)의 종료 코드를 대조한다(`DECISION_GATE_DOC` 로 다른 판을 가리킬 수 있다).
    새 파일이라 `python3 scripts/sync-docs.py design-kit` 로 킷 README AUTO 를 맞춘다 (ER-02)
11. **B1** — 확인 줄을 `type verify_seal fm_get contract_digest sha256_16` 으로 넓히고 STOP 문구 · 윗줄 주석을 넷으로 (ER-03)
12. **A7** — 분석 결과가 「no issues」 인 정상 종료도 `.errors.log` 에 `ok:no-issues session=<>` 한 줄을 남기고, `collect_status` 는 마지막 기록과 마지막 정상 종료(`ok:no-issues` · `skip:env-dedup-all`)
    가운데 늦은 쪽 뒤의 실패만 「마지막 기록 뒤」 로 센다. 시험 둘에 경우를 더하고 SCHEMA.md · DESIGN.md 태그 목록 · reflect-digest Gotcha 13 과 `## 입력` 의 `.errors.log` 설명 줄(실패로 세지 않는 줄이라고 적는다)을 맞춘다.
    검토가 준 다른 길(문턱을 고유 세션 N 개로 올린다)은 문턱 값을 새로 정해야 하고 정상 실행 뒤 실패 한 번을 여전히 가르지 못해 고르지 않았다 (ER-04)
13. **B10** — 픽스처 `fixtures/gate-fail-ledger-misplaced.md`(Step 1 에 출처 둘 · Step 2 에 0, 주소는 `<…>` 로 감싸 편집기 경고를 늘리지 않는다)와 `gate_cases` 사례 하나 (ER-05)
14. **B6 · C L13** — CI validate 잡 끝에 scenario-report 단위 시험과 결정 전파 킷 시험 두 단계 (ER-06)
15. **문서 사이트** — 원본이 바뀐 페이지 일곱의 해당 절만: 봉인 범위 블록 확인 줄 · MakerWorld 블록 `rm -f` 줄 · 결정 전파 검사 코드 블록 전체 · design-test 「위반 0」 셋과 종료 코드 2 · 3 문장 ·
    reflect 태그 목록 두 쪽 · api 뷰어 쪽 「두 명령은 한 번의 셸 호출에서 잇는다」 문장. 페이지를 새로 만들지 않고 부분만 맞추는 것은 Final 지침 §PR 직전이 정한 방식이다 (AR-02)

## 범위 경계

- 이 계약 시작 HEAD: `6a8be196d9c40a1686f51f9a6bd50039c2bd5b71` (착수 때 `git rev-parse HEAD` 출력 — main 을 합친 커밋. main 에서 들어온 커밋은 그 조상이라 범위에 들지 않는다).
  범위 상한은 개정 파일 `.harness/sprint-amendments-kaizen-0924-f2-review-fixes.md` 의 `end_sha:` 마지막 값이다 — `HEAD` 로 재지 않는다. notes 커밋도 이 계약 커밋이라
  notes 를 커밋한 뒤 그 sha 로 `end_sha:` 줄을 하나 더 덧붙인다(옛 줄은 지우지 않는다)
- 고치는 파일은 마흔여섯이고 그 가운데 새 파일은 둘(`design-kit/evals/decision-gate-test.sh` · `onboarding-kit/skills/setup-guide/evals/fixtures/gate-fail-ledger-misplaced.md`)이다.
  아래 블록이 그 목록이다(`harness/README.md` §커밋 안전 훅 이 정한 범위 선언 자리). `.harness/` 쪽은 이 계약 · 개정 파일 · QA 피드백 · `.harness/.meta/kaizen-0924/f2-review-fixes-notes.md` ·
  `.harness/.meta/kaizen-0924/f2-review-fixes-review.md` 와 감사 기록 `.harness/.meta/orchestrator-audit-log.md` 에 더하는 한 줄이다(AR-01 둘째 값의 허용 갈래). AR-01 여섯째 값이 이 블록과 측정 공통 정의의 `FILES` 가 같은지 잰다

```text
# sprint-scope
scripts/check-stale-values.py
.claude/skills/react-kaizen/SKILL.md
.claude/skills/design-kaizen/SKILL.md
.claude/skills/backend-kaizen/SKILL.md
.claude/skills/infra-kaizen/SKILL.md
.claude/skills/rust-kaizen/SKILL.md
.claude/skills/kaizen-orchestrator/SKILL.md
.claude/skills/tone-kaizen/SKILL.md
.claude/skills/docs-site/SKILL.md
harness/references/contract-schema.md
docs/harness/contract-schema.html
.github/workflows/ci.yml
react-kit/skills/react-l10n/SKILL.md
design-kit/references/visual-change-protocol.md
design-kit/evals/decision-gate-test.sh
design-kit/README.md
design-kit/skills/design-test/SKILL.md
design-kit/skills/design-audit/SKILL.md
design-kit/agents/design-reviewer.md
docs/design-kit/visual-change-protocol.html
docs/design-kit/design-test.html
flutter-toolkit/skills/flutter-scenario-report/SKILL.md
flutter-toolkit/skills/flutter-scenario-report/references/record-format.md
flutter-toolkit/evals/scenario-report/test_build_report.py
flutter-toolkit/evals/scenario-report/example/TC-001-transfer-leader-cancel/record.json
flutter-toolkit/evals/scenario-report/example/TC-002-appoint-vice-leader/record.json
flutter-toolkit/evals/scenario-report/example/index.html
flutter-toolkit/README.md
flutter-toolkit/skills/flutter-preflight/SKILL.md
reflect-kit/hooks/log-reflection.sh
reflect-kit/hooks/_lib-project-id.sh
reflect-kit/evals/hooks/collect-status-test.sh
reflect-kit/evals/hooks/log-reflection-test.sh
reflect-kit/docs/SCHEMA.md
reflect-kit/docs/DESIGN.md
reflect-kit/skills/reflect-digest/SKILL.md
docs/reflect-kit/schema.html
docs/reflect-kit/design.html
api-kit/skills/api-ui/SKILL.md
docs/api-kit/static-evidence-viewer-contract.html
rust-kit/skills/rust-audit/SKILL.md
onboarding-kit/skills/setup-guide/evals/evals.json
onboarding-kit/skills/setup-guide/evals/fixtures/gate-fail-ledger-misplaced.md
bambu-kit/skills/bambu-print-profile/SKILL.md
docs/bambu-kit/bambu-print-profile.html
README.md
.harness/
```

- **이 계약의 커밋 메시지에는 전부 `Co-Authored-By` 줄 바로 위에 서명 줄 `Kaizen-Phase: kaizen-0924-f2-review-fixes` 한 줄을 넣는다** (봉인 커밋 · notes · `end_sha` 커밋 포함).
  AR-01 · ER-08 · SC-00 이 이 줄로 이 계약 커밋을 가린다(`harness/references/contract-schema.md` §여러 주체가 한 가지에 커밋할 때). 서명을 빠뜨린 커밋은 서명 목록에 안 보이므로 AR-01 첫째 값은 경로로 직접 센다
- **한 커밋에 묶음 하나** (Final 지침 「한 커밋에 킷 하나」). 묶음 열셋과 경로는 측정 공통 정의의 `GRPS` · `GPATH` 다 — `scripts` · `claude`(`.claude/skills/`) · `harness`(`harness/` · `docs/harness/`) · `ci` ·
  `react` · `design`(`design-kit/` · `docs/design-kit/`) · `flutter` · `reflect`(`reflect-kit/` · `docs/reflect-kit/`) · `api`(`api-kit/` · `docs/api-kit/`) · `rust` · `onboarding` · `bambu`(`bambu-kit/` · `docs/bambu-kit/`) · `readme`(루트 `README.md`).
  킷의 문서 사이트 페이지는 그 킷 묶음에 든다. 커밋마다 `git add -- <그 묶음 파일> && git commit -o -- <그 묶음 파일>`. 구현 커밋은 `.harness/` 를 함께 싣지 않는다(AR-01 셋째 값). 새 시험 셸 파일은 git 모드 `100755`
- notes `.harness/.meta/kaizen-0924/f2-review-fixes-notes.md` 에 적는 것 (ER-08 이 잰다): `## 커밋` — `| <묶음 이름> | <커밋 sha> |` 로 시작하는 표 행 열셋 · `## 다룬 항목` ·
  `## 고치지 않은 항목과 이유` (아래 입력 항목 표의 「고치지 않음」 전부) · `## 다음 사이클 메모` — 아래 표 「고치지 않음」 가운데 다음 사이클로 가는 것. ER-08 이 토큰 열아홉으로 잰다:
  `commit-guard.sh` · `detect-docs-drift.py` · `sync-orchestrator.py` · `infra-test` · `VISUAL_CHANNEL` · `enum 값 검사 미실행` · `adapter-dart-flutter.md` · `noncharacter` · `slang` · `app-preflight` ·
  `design-reviewer` · `planning-reviewer` · `excluded_surfaces` · `silent-check` · `delete-conflicting-outputs` · `RFC 7493` · `AUTO 마커` · `tone-research` · `reflect-kit/README.md`.
  감사 기록 `.harness/.meta/orchestrator-audit-log.md` §Phase 다음 사이클 메모 (2026-09-24 사이클) 끝에 「PR 직전 검토 수정 계약이 고치지 않은 것은 `f2-review-fixes-notes.md` §다음 사이클 메모」 한 줄을 더한다 —
  다음 사이클이 그 절에서 notes 를 찾는다. 이 줄 말고는 감사 기록을 고치지 않는다 — ER-08 (d) 가 빈 줄을 뺀 더한 줄 수 1 로 잰다
- 측정이 기대는 제목 · 줄 머리는 이름을 바꾸지 않는다: 오케스트레이터 `### Step F2` · `**절차:**` · AUTO 마커 두 줄 · Final 조건 줄 머리 「Phase 1에서 업데이트된 설계 원칙이 Phase 2~17 변경에 반영되었는가」 ·
  docs-site `## Step 1` · `## Step 2` · tone-kaizen `- \`docs/tone/*.md\`` 줄 머리 · I-02 줄의 `**I-02 예외 목록 명시화**` · design-audit `## Step 5` · design-test 표 행 머리 `| 결정 전파 |` ·
  rust-audit `16. **파이프라인 종료 코드로만` · 「→ 0 을 "안티패턴 없음 PASS"」 · rust-run `## 2. 실행 + 결과 출력` · api-ui `1. **여는 방법**` · `2. **콘솔 오류**` ·
  react-l10n `3. 지워진 키 수와` · bambu `ID=<모델 번호>; OUT=<output_dir>/makerworld;` 줄 · contract-schema 블록 머리 셋(`fm_get() { # fm_get <file> <key>` · `verify_seal() {  # verify_seal` · `# .harness/ 의 계약 파일만 골라`) ·
  onboarding `  elif [ "$misplaced" -ne 0 ]; then` · reflect-digest `13. **엔트리 0 을` · reflect-digest 입력 줄 「/.errors.log` — 훅 자체 실패 로그」 · 검사 코드 docstring `Decision Propagation Coverage Gate` ·
  오케스트레이터 「Phase 17 표는 아직 없다」 · `scripts/validate-post-kaizen.py` 의 검사 이름 `scope-isolation` · `doc-contracts`
- 공유 파일(`.claude-plugin/marketplace.json` · 킷 `plugin.json` 버전 · 루트 `CLAUDE.md` · `.claude/kaizen-input/insights-report.md` · `.harness/.meta/kaizen-failure-count.yaml` · `.harness/stale-values.yaml` ·
  `docs/index.html` · `docs/kaizen/`)은 건드리지 않는다 — ER-08 (e). 버전은 `release-plan.md` 대로 PR 을 합친 뒤 올린다(이 계약이 바꾼 킷의 단계는 notes `## 다룬 항목` 에 적는다)
- QA(`harness:qa-evaluator`)는 설치본이다. 이 계약이 고치는 harness 파일은 `contract-schema.md` 한 줄이라 평가자 동작에는 닿지 않는다
- 사용자 승인(Step 5) 대체: 사용자가 「자동으로 끝까지 알아서 진행해 내 허락이 필요한건 코덱스로 리서치나 검토받고」라고 위임했다(세션 `de8c7935-a5b6-4df5-9106-fafa73c288a0` 기록 queued_command
  `2026-09-24T04:04:16.964Z`). Codex 사용량 한도가 소진돼(오류 원문 「You've hit your usage limit … try again at 11:05 PM」, 2026-09-24) 독립 Claude 검토자(REVIEW 에이전트)가 대신한다.
  이어 사용자가 「코덱스 대신에 그냥 너가 알아서 진행하라고」라고 명시했다(같은 세션 기록 user `2026-09-24T11:54:58.940Z`). 뒤에 「코덱스도 사용할 수 있으니깐 사용해」(user `2026-09-25T06:19:45.056Z`)라
  Codex 2 차 검토 결과를 입력으로 받았다. 계약 초안 검토 결과 파일: `.harness/.meta/kaizen-0924/f2-review-fixes-review.md` (REVIEW 에이전트가 쓴다)
- 계약 초안 검토 반영(`VERDICT: CHANGES`, 초안 sha256 앞 16 자 `9e185d8e3aa0dea4`): 꼭 둘 — SK-01 옛 문장에 design-kaizen Step 5 의 「Phase 로 호출한 경우 이 Step 을 실행하지 마라」 더함 · DG-06 을 두 줄 모두 `[ PASS  ]` 로 좁힘(빈 출력 · `SKIP` 은 실패).
  권함 넷 — ER-08 (d) 더한 줄 수 · AR-02 (g) 원본 낱말 비율(`wr`) · ER-04 digest `## 입력` 줄 · 입력 표 39 행(Codex N2)은 (가) 고침을 골랐다(SK-02 (f)).
  선택 셋 — ER-02 입력 열(`assertions` 문자열) · SK-06 (b) `src/` 부재 한계 문장 · 0 기대 값 양성 대조 넷(AP-03 · DG-02 · RE-02 · AR-02) 모두 반영.
  AR-02 (g) 에는 검토가 선택으로 든 api 쪽 둘째 원본(`api-kit/skills/api-ui/SKILL.md`)도 짝으로 넣었다. 조건 수 30 · 기능 조건 20 은 그대로다
- 승인 대체 기록(봉인 직전, 2026-09-26): 같은 검토 파일 `## 2 회차`(검토 시점 초안 sha256 앞 16 자 `e35ae81b777b14e0`)의 마지막 판정이 `VERDICT: APPROVE` 다.
  위 「사용자 승인(Step 5) 대체」 의 두 앵커 위임(queued_command `2026-09-24T04:04:16.964Z` · user `2026-09-24T11:54:58.940Z`)에 따라 사용자 승인 자리를 이 두 회차 검토와 그 지적 반영이 대신한다.
  2 회차가 「막지 않는다」 로 적은 셋은 이렇게 다룬다 — (1) `m.sh` ER-02 갈래 주석의 입력 수를 열로 고쳤다(조건 줄 밖이라 봉인과 무관) (2) tone-kaizen `:35` 괄호에 overview · research-log · templates 셋을 모두 적고,
  notes `## 다룬 항목` 에 「`F1H-78` 의 `:35` 쪽은 B4 로 닫았고 `:100` 「리서치 문서 8종」 은 셈 기준이 달라 둔다」 한 줄을 남긴다 (3) SK-02 (f) 는 QA 가 그 줄 전문을 읽어 뜻을 확인한다.
  봉인 뒤 조건이 틀린 것을 알게 되면 조건 줄을 고치지 않고 개정 파일에 적는다(Step 6.6 (d)). 사용자가 할 일: 없음
- 판정 한계: 스킬을 부르는 모델이 새 문장대로 움직이는지(서명 줄을 실제로 넣는지 · 종료 코드 2 를 REJECT 로 읽는지)는 결정론 측정이 없다 — 조건은 문장이 정해진 자리에 있는지와,
  블록 · 검사 코드 · 훅 · 러너처럼 돌릴 수 있는 것은 돌린 결과를 잰다. api-ui 대조는 비어 있는 포트로 바꿔 돌린다(`lsof` 필요). reflect 대조는 가짜 codex 로 실제 Stop 훅을 돌린다(`jq` 필요).
  bambu 대조는 네트워크 대신 연결 실패를 흉내 내는 가짜 curl 로 돈다. design 대조는 PyYAML 이 있어야 돈다. DG-06 은 `scripts/validate-post-kaizen.py` 가 `HEAD` 까지 재는 도구라 QA 시점 작업 폴더에서 돈다
- 판정 근거: SK-01 · SK-02 · SK-03 · SK-04 (b)(d)(e) · SK-05 끝 두 값 · SK-06 (a) · SK-06 (b) 끝 값 · SK-07 문장 · ER-04 태그 · digest 두 값 · AR-02 토큰 — 산출물이 문서 문장 자체라 정해진 자리에 정해진 토큰이 있는지가 판정이다.
  토큰은 한 줄 전체가 아니라 짧은 글이므로 봉인 전에 「그 줄만 지운 사본」 에서 값이 떨어지는지 예행으로 확인했다(봉인 전 실측 표 「삭제 대조」)
- 판정 근거: SK-05 · SK-06 (b) · SK-07 · SK-08 · ER-01 ~ ER-06 · DG-04 — 끝 판 문서에서 블록 · 코드 · 훅을 떼거나 킷 시험을 끝 판 사본에서 실제로 돌린 출력이다. 시작 판에서 같은 측정이 결함을 드러낸다
- 판정 근거: ER-07 · ER-08 · AR-01 · SC-00 · AP-01 · DG-02 — 커밋 기록 · 파일마다 편집 전 판과의 비교다. 예행 저장소 변형 열이 양성 · 음성 대조다
- 오라클 해소: SK-05 — 첫 측정 줄은 끝 판 문서의 `3. 지워진 키 수와` 아래 첫 bash 블록을 원문 그대로 떼어 임시 저장소 둘에서 bash · zsh 로 돌린 출력과 종료 코드다(`l10n.sh`). 문장 두 값(`sentence` · `grep_second`)은 그 뒤에 붙인 보조 값이다
- Codex 2 차 검토(`r4-final.md`, 2 회차) 재확인: 앞선 21 건 표의 「일부」 · 「고치지 않기로 함」 일곱(R1-2 · R2-2 · R2-3 · R2-4 · R2-5 · R2-7 · R3-6)과 새 발견 넷(N1 ~ N4)을 봉인 전에 다시 재현 · 확인했다.
  새로 더한 조건은 없다 — N1 · N3 은 ER-01 · SK-04 (e) 가 이미 다루고, N2 는 계약 초안 검토 뒤 SK-02 (f) 로 다룬다(39 행). 나머지 여덟은 입력 항목 표 26 · 34 ~ 38 · 40 행에 다시 확인한 근거와 「고치지 않음」 이유를 적었다
- 커버리지 해소: 측정 공통 정의의 파일 변수(`$SCV` · `$KRE` · `$KDE` · `$KBE` · `$KIN` · `$KRU` · `$KOR` · `$KTO` · `$KDS` · `$HCS` · `$PCS` · `$CI` · `$RLN` · `$DVP` · `$DGT` · `$DRD` · `$DTE` · `$DAU` · `$DRV` · `$PVP` · `$PDT` ·
  `$FSR` · `$FRF` · `$FTT` · `$FE1` · `$FE2` · `$FEI` · `$FRD` · `$FPR` · `$RLR` · `$RLIB` · `$RCT` · `$RLT` · `$RSC` · `$RDE` · `$RDG` · `$PRS` · `$PRD` · `$AUI` · `$PAV` · `$RAU` · `$OEV` · `$OFX` · `$BAM` · `$PBA` · `$RMD`)가
  산문의 파일 이름을 연다 — 대응은 `common.sh` 머리
- 커버리지 해소: SK-01 — `.claude/skills/*/SKILL.md` 는 SK-01 갈래의 `cat "$E"/.claude/skills/*/SKILL.md` 가 끝 판 폴더에서 펼친다(예행 판 스물다섯 파일). `.harness/sprint-contract-<slug>.md` · `.harness/sprint-feedback-<slug>.md` · `.harness/sprint-amendments-<slug>.md` 는 갈래 `toks` 의 인자 글자다
- 커버리지 해소: SK-02 — `scripts/detect-docs-drift.py` 는 갈래의 파이썬이 끝 판 폴더에서 불러 쓰고, `api-kit/references/` 는 `api_ref` 셈 글자, `references/phase-dependencies.md` · `hooks/` 는 `phase_dep_line` 의 grep 글자, `docs/tone/*.md` 는 `tn` · `tc` 식(`docs/tone` 폴더를 `find` 로 센다), `howto-research/SKILL.md`(`.claude/skills/howto-research/SKILL.md`)는 `p17_src` 의 grep 글자다
- 커버리지 해소: SK-04 — `flutter-toolkit/` 는 `fitpal` grep 과 단위 시험 사본 경로, `references/record-format.md` 는 `$FRF`, `skills/` 는 README 트리 줄 awk 글자다
- 커버리지 해소: ER-08 — `.harness/…` 경로는 공통 정의의 `$NOTES` · `$AUD` 이고, 공유 경로 여덟(`.claude-plugin/marketplace.json` · `*/.claude-plugin/plugin.json` · `CLAUDE.md` · `.claude/kaizen-input/insights-report.md` · `.harness/.meta/kaizen-failure-count.yaml` · `.harness/stale-values.yaml` · `docs/index.html` · `docs/kaizen`)은 ER-08 갈래 `git log -- <경로>` 의 인자 글자다. `f2-review-fixes-notes.md` 는 `added_ptr` 의 grep 글자, `reflect-kit/README.md` 는 다음 사이클 메모 `toks` 의 인자 글자다
- 커버리지 해소: AR-02 — 페이지 일곱은 `$PCS` · `$PBA` · `$PVP` · `$PDT` · `$PRS` · `$PRD` · `$PAV`, 원본은 `$DVP` · `$DTE` · `$HCS` · `$BAM` · `$RSC` · `$RDE` · `$AUI` 와 갈래 안 글자 `docs/api/verification/static-evidence-viewer-contract.md` 다(`api-kit/skills/api-ui/SKILL.md` 는 `$AUI` · `visual-change-protocol.md` · `design-test/SKILL.md` · `contract-schema.md` · `bambu-print-profile/SKILL.md` 는 산문의 줄임 이름)
- 커버리지 해소: DG-05 — 스크립트 일곱(`sync-docs.py` · `sync-evals.py` · `sync-orchestrator.py` · `run-evals.py` · `check-docs-links.py` · `check-contrast-claims.py` · `check-stale-values.py`)과 킷 열넷은 DG-05 갈래 `for k in …` 목록 글자다
- 커버리지 해소: 그 밖의 경로(`rust-kit/skills/rust-run/SKILL.md` · `planning-kit/skills` · `reflect-kit/skills` · `onboarding-kit/skills/setup-guide/evals/run-gate-evals.sh` · `backend-kit/skills/backend-test/SKILL.md`)는 같은 ID 갈래가 경로를 적어 연다
- 커버리지 해소: AR-01 — `.harness/…` 허용 갈래는 공통 정의의 `$CF` · `$AM` · `$NOTES` · `$AUD` 와 AR-01 갈래의 글자다

### 입력 항목 처리표

`review-fixes.md`(A · B · C) · Codex `r4-final.md` · 지침 「먼저 읽을 것」 에서 이 계약 몫을 전부 뽑았다. 「고치지 않음」 은 notes `## 고치지 않은 항목과 이유` · `## 다음 사이클 메모` 로 옮긴다.

| # | 입력 | 처리 |
| --- | --- | --- |
| 1 | A1 `scripts/check-stale-values.py:45` backend-kit 제외가 남음 | 조건으로 다룸 — ER-01 (Codex r4 1 회차 새 발견 2 · 2 회차 N1 과 같은 자리) |
| 2 | A2 `react-kaizen:82` · `design-kaizen:33` · `:81` 커밋 주체 · 서명 줄 | 조건으로 다룸 — SK-01 (a) |
| 3 | A3 `react-l10n:175` 둘째 줄 `grep -E` 종료 코드 1 | 조건으로 다룸 — SK-05 |
| 4 | A4 `visual-change-protocol.md:435` 모양 오류가 종료 코드 1 · 시험 0 개 | 조건으로 다룸 — ER-02 · ER-06 · AR-02 |
| 5 | A5 design-test `:366` · design-audit `:115` · design-reviewer `:179` 종료 코드 2 · 3 | 조건으로 다룸 — SK-03 · AR-02 (design-test 페이지) |
| 6 | A6 scenario-report `:19` · record-format `:62` 도구 · 앱 이름 | 조건으로 다룸 — SK-04 (a)(b)(c) |
| 7 | A7 `_lib-project-id.sh:199` 정상 실행 뒤 실패 한 번에 멈춤 경고 | 조건으로 다룸 — ER-04 · AR-02 (reflect 두 쪽) |
| 8 | A8 `api-ui:168` 잇는 방법 미정 — bash `&&` 면 번호 · 폴더 틀림 | 조건으로 다룸 — SK-07 · AR-02 (api 뷰어 쪽) |
| 9 | B1 `contract-schema.md:608` 정의 확인이 둘뿐 | 조건으로 다룸 — ER-03 · AR-02 (harness 쪽) |
| 10 | B2 I-02 목록 넷 슬러그 경로 | 조건으로 다룸 — SK-01 (b) |
| 11 | B3 오케스트레이터 `:583` planning 10 · reflect 3 | 조건으로 다룸 — SK-02 (a) |
| 12 | B4 tone-kaizen `:35` `docs/tone/*.md` 8종 | 조건으로 다룸 — SK-02 (b) |
| 13 | B5 오케스트레이터 `:624` F2 표 api-kit · onboarding 이 detect-docs-drift 와 다름 | 조건으로 다룸 — SK-02 (c). 표 쪽을 좁혔다(detect-docs-drift 에 매핑 · 페이지를 더하는 길은 새 페이지를 만들어야 해 고르지 않음) |
| 14 | B6 `ci.yml:87` scenario-report 시험이 CI 에 없음 | 조건으로 다룸 — ER-06 |
| 15 | B7 rust-audit `:36` 「rust-run (c)」 | 조건으로 다룸 — SK-06 (a) |
| 16 | B8 flutter-preflight `:138` codegen 줄 `success` 고정 | 조건으로 다룸 — SK-04 (d) |
| 17 | B9 rust-audit `:33` `grep -c` 폴더 | 조건으로 다룸 — SK-06 (b) |
| 18 | B10 setup-guide `:73` misplaced 판정을 지키는 시험 없음 | 조건으로 다룸 — ER-05 |
| 19 | B11 bambu `:2469` design.json · instances.json 이 남음 | 조건으로 다룸 — SK-08 · AR-02 (bambu 쪽) |
| 20 | B12 오케스트레이터 `:478` Phase 12 범위 줄 ↔ phase-dependencies | 조건으로 다룸 — SK-02 (e). AUTO 밖 한 줄로. 생성기 고치기는 고치지 않음 — C L7 과 같은 자리(`sync-orchestrator.py`), 다음 사이클 |
| 21 | B13 오케스트레이터 `:608` F2 표 ↔ docs-site Step 1 표 | 조건으로 다룸 — SK-02 (d) |
| 22 | B14 루트 `README.md:157` 19종 · 목록에 scenario-report 없음 | 조건으로 다룸 — SK-04 (e) (Codex r4 1 회차 새 발견 1 · 2 회차 N3 과 같은 자리). 「AUTO 마커 안으로 옮기기」 는 고치지 않음 — sync-docs 에 새 마커 종류가 필요한 기능 추가라 다음 사이클 |
| 23 | C L2 `commit-guard.sh:231` `-i` 커밋 막힘 설명 빠짐 | 고치지 않음 — 낮음 · 사실 오류 아님(막는 동작은 맞고 안내 글만 빠졌다). 다음 사이클 Phase 4 |
| 24 | C L3 `detect-docs-drift.py:65` howto 초안 파일을 새 페이지 대상으로 냄 | 고치지 않음 — 낮음. F2 는 이번 사이클에 끝났고 다음 사이클 F2 전에 매핑 밖 목록을 정한다 |
| 25 | C L7 `sync-orchestrator.py:121` planning docs · references 추론 | 고치지 않음 — 낮음. 생성기 고치기는 AUTO 영역 전체를 다시 만든다 — 다음 사이클 Phase 4 (20 행과 함께) |
| 26 | C L10 · Codex r4 1 회차 12 · 2 회차 R2-5 `infra-test:256` checkout 을 줄 글자로 판정 | 고치지 않음 — 낮음. 2 회차 뒤 다시 재현했다(시작 커밋의 규칙 1 블록을 그대로 떼어 bash 로): checkout 단계 없이 `run: \|` 블록 안에 `uses: actions/checkout@v4` 줄만 둔 워크플로 → 종료 코드 0(PASS), 흐름 표기 `- {uses: actions/checkout@v4}` 로 적은 진짜 checkout → 종료 코드 1(VIOLATION). 원래 지적(주석 한 줄로 PASS, 중간)은 f1 kit 계약 71 행이 막았고 남은 두 경우는 드물다. 막으려면 YAML 을 구조로 읽어 판정해야 하는데, f1 이 줄 판정을 고른 까닭이 python3 없는 환경에서도 규칙 1 이 돌게 하려는 것이라 그렇게 바꾸면 그 환경에서 규칙 1 이 빠진다 — 새 동작 설계다. 다음 사이클 Phase 8 |
| 27 | C L13 scenario-report 시험을 돌리는 곳 없음 | 조건으로 다룸 — ER-06 (B6 과 같은 고침) |
| 28 | C L14 scenario-report `:44` `VISUAL_CHANNEL` 우선순위 표 | 고치지 않음 — 낮음. project-detection Step 8 의 채널 결정 규칙을 바꾸는 일이라 다음 사이클 Phase 5 |
| 29 | C L17 bambu `:1603` `[미검증]` 문구가 「키 존재 · 종류 · enum 값 검사 미실행」 | 고치지 않음 — 낮음(출력 문구). 다음 사이클 Phase 13 |
| 30 | C L19 tone `adapter-dart-flutter.md:26` 표 칸의 `\|` 정규식 | 고치지 않음 — 낮음. 어댑터 슬롯 값 형식을 정하는 일이라 다음 사이클 Phase 15 |
| 31 | C L20 `api-verify:117` 목록에 noncharacter 없음 | 고치지 않음 — 낮음. 다음 사이클 Phase 16 (35 행과 함께) |
| 32 | C R1 (반박 2/3) flutter-l10n slang 명령 경로 | 고치지 않음 — 반박 검토 셋 가운데 둘이 기각. 다음 사이클 Phase 5 에서 `slang_build_runner` 유무 갈래를 정한다 |
| 33 | C R2 (반박 2/3) project-detection Makefile 타겟마다 확인 | 고치지 않음 — 반박 둘이 기각. 다음 사이클 Phase 5 (`app-preflight` 묶음 타겟만 있는 경우) |
| 34 | C R3 (반박 2/3) · Codex r4 1 회차 10 · 11 · 2 회차 R2-3 · R2-4 design-reviewer · planning-reviewer 미검증 규칙 옛 사본 | 고치지 않음 — 검토가 갈렸다(Claude 반박 둘은 기각, Codex 1 회차는 연기 이유가 타당하지 않다고, 2 회차는 범위 사유가 타당하다고 봄). 2 회차 뒤 다시 확인: `design-reviewer.md:26` · `planning-reviewer.md:25` 는 「5 조항」 을 「문구 변형 없이」 옮겼다고 적는데, 기준 원본 `qa-evaluation-guide.md` §Canonical Unverified-Evidence Protocol(`:1231`)의 항목 번호가 1 · 2 · 3 · 3 · 4 · 5 여섯이고 둘째 항목은 DG-01 · DG-02 N/A 규칙이라 그대로 옮길 판부터 정해야 한다(f1 kit 계약 69 행). 옮기면 design-audit Gotcha 11 · Step 4 · Step 5 · evals id 21 과 react · api reviewer 의 REJECT 문턱이 함께 바뀌어 PR 직전 사실 오류 고치기를 넘는 판정 동작 변경이다. 다음 사이클 Phase 3 뒤 reviewer 넷을 한 번에 |
| 35 | Codex r4 1 회차 21 · 2 회차 R3-6 api-kit `-0` 을 「I-JSON 게이트」 로 분류 | 고치지 않음 — 레포 안에서는 어긋나지 않는다: 킷의 「I-JSON 게이트」 는 JCS 앞 검문 단계 이름이고 `api-contract/SKILL.md:69` 가 `-0` 을 그 단계에서 막는 이유를 JCS 로 적었다(`api-verify:117` · `api-probe:183` 도 같은 목록). 레포 연구 기록 `docs/api/research-log.md:204` 도 「I-JSON 게이트 목록」 에 `-0` 을 RFC 8785 정정 7920 을 근거로 넣었다고 적었다 — 단계 이름은 레포가 정한 검문 단계 이름이다. 2 회차가 든 `snapshot-sealing-canonicalization.md:82` 도 `-0` 거부 이유를 JCS(RFC 8785 정정)로 적을 뿐 킷 문장과 어긋나지 않는다. RFC 7493 이 `-0` 을 금지하지 않는다는 주장은 근거 파일 밖이다 — 이름을 가를지는 다음 사이클 Phase 16 |
| 36 | Codex r4 1 회차 9 · 2 회차 R2-2 결정 전파 검사가 `status` 값 · `excluded_surfaces` 키 유무를 안 봄 | 고치지 않음 — 재현은 됐다(`status: nonsense` · 제외 없음 → `violations=0 schema_errors=0` · 종료 코드 0, 봉인 전 실측). 그러나 §6 의 「스키마」 절이 `status` 값 목록도, 모든 화면에 적용되는 결정이 빈 `excluded_surfaces` 를 적어야 하는지도 정하지 않았다 — 규칙을 새로 정하는 일이라 다음 사이클 Phase 6. 2 회차 뒤 다시 확인: `status` 는 스키마 예시(`:372` `status: approved`)에만 있고 §4 승인 기록 최소 필드에도 그 칸이 없다 — f1 kit 계약 68 행이 같은 이유로 `status` 를 검사하지 않기로 했다. `:389` 「`excluded_surfaces` 는 선택이 아니다」 는 적용하지 않는 표면을 이유와 함께 적으라는 규칙이고, 그런 표면이 없을 때 빈 목록 키를 둬야 하는지는 적지 않았다 |
| 37 | Codex r4 1 회차 14 · 2 회차 R2-7 flutter-build `--delete-conflicting-outputs` | 고치지 않음 — f1 계약 73 행 이유 유지: 2.16 은 이 플래그를 「제거된 호환 옵션」 목록에 두어 받기는 하고 효과가 없다. Codex 1 회차 「일부 타당」 · 2 회차 「타당」. 명령에서 뺄지는 다음 사이클 Phase 5 |
| 38 | Codex r4 1 회차 2 · 2 회차 R1-2 `silent-check` 실행기 없음 | 고치지 않음 — Codex 도 연기 이유가 타당하다고 봄(새 실행기 = 새 기능). 2 회차 뒤 다시 확인: 레포에서 `silent-check` 가 든 파일은 `assertions.json` 과 `expected-improvements.md` 둘뿐이고 `scripts/run-evals.py` 는 킷마다 `evals/evals.json` 만 읽는다(`:54`, 끝 줄 `Total: 116 passed, 0 failed`). 실행기를 새로 두는 일은 오케스트레이터 Gotcha `:47` 「Final에서 새 기능을 추가하지 마라」 에 걸린다 — 이 계약도 Final 단계다. 다음 사이클 Phase 3 |
| 39 | Codex r4 2 회차 N2 — `phase-research-templates.md` 에 Phase 17 의무 리서치 표 없음 | 조건으로 다룸 — SK-02 (f). 초안은 「이미 넘긴 일」 로 두었으나 계약 초안 검토(6 번)가 그 사유 가운데 「`docs/howto/` 에는 출처 표가 든 연구 기록이 없다」 가 틀렸다고 짚었다 — 다시 재 보니 `.claude/skills/howto-research/SKILL.md` Step 1 에 「카테고리 · 문서 · 1차 출처」 표(여섯 행)가 있고 `docs/howto/changelog-feeds.md` 에 주소 30 개 · `deep-links.md` 에 17 개가 있다. 오케스트레이터 `:25` 는 한 줄 안에서 「최소 3 건 조회」 와 「Phase 17 표는 아직 없다」 가 어긋나 있어, 괄호가 그 출처 표를 가리키게 한다 — 출처를 새로 고르지 않으므로 Gotcha `:47` 「Final에서 새 기능을 추가하지 마라」 에 걸리지 않는다. `phase-research-templates.md` 에 Phase 17 표를 더하는 일(f1 계약 F1H-76 · 감사 기록 `:542`)은 다음 사이클 Phase 17 그대로다 |
| 40 | Codex r4 2 회차 N4 — `docs/kaizen/changelog.md:110` 「133 → 389 파일」 이 지금 출력 391 과 다름 | 고치지 않음 — 재현 안 됨: 합치기 전 `760a75f` 판에서 옛 값 검사를 돌리면 「파일 389 개」, 합친 `6a8be19` 판은 「파일 391 개」 다(봉인 전 실측 · 2 회차 뒤 다시 잼). 합침이 scenario-report 원본 두 개를 더해 391 이 됐다 — 그때 실측을 적은 기록이라 맞다. `docs/kaizen/` 는 공유 파일이기도 하다 |
| 41 | Codex r4 두 회차의 「고침」 열셋 · 열넷과 합침 결과 확인 넷 | 해당 없음 — 고쳐졌다고 확인됐다. 합침 결과 README 한 건은 22 행, 오케스트레이터 「일부」(2 회차)는 39 행 |
| 42 | 지침 「먼저 읽을 것」 — `final-todo.md` · `xdiag-all.md` · Phase notes 넘김 | 해당 없음 — f1 두 계약과 `kaizen-0924-final` 이 처리했다(QA APPROVE). `final-todo.md` §PR 직전은 메인 루프 몫(합침 `6a8be19` · 재실행 · Codex 2 차 검토 `r4-final.md`)이고 그 결과가 이 계약 입력이다 |
| 43 | 직접 찾은 것 — 루트 `CLAUDE.md:294` 「리서치 문서는 `docs/tone/` 8종」 · `tone-research/SKILL.md:4` 「docs/tone/ 8종」 · `CLAUDE.md:284` 「`docs/api/` 12종」(파일 13) | 고치지 않음 — 「리서치 문서」 를 셀 때 overview · research-log · templates 를 넣는지 정한 곳이 없어 사실 오류로 확정 못 한다(B4 는 글로브 `docs/tone/*.md` 를 적은 줄이라 11 이 확정). 다음 사이클 Phase 15 · 16 |
| 44 | 계약 초안 검토 5 번 — `reflect-kit/README.md:84` 한 줄 설명(「훅 실패 메타 로그 + 환경 오설정 억제 기록」)에 `ok:no-issues` 가 없다 | 고치지 않음 — 원래도 `vocab:` · `warn:` 줄을 적지 않는 뭉뚱그린 설명이라 사실 오류가 아니다. 파일을 늘리지 않고 notes 다음 사이클 메모에 남긴다(ER-08 토큰 `reflect-kit/README.md`). 다음 사이클 Phase 12 |

## 회귀 게이트 — 측정 공통 정의와 봉인 전 실측

모든 조건의 측정은 아래 `common.sh` 와 `m.sh` 를 차례로 `.` 으로 읽은 **bash** 셸에서 돈다 — `common.sh` 는 bash 가 아니면 `NOT_BASH` 를 찍고 종료 코드 2 로 끝난다.
`m` 은 도우미 함수와 두 판 폴더가 없으면 `HELPER_MISSING` · `SNAPSHOT_MISSING` 을 내고 멈춘다 — 그래서 조건마다 `type m >/dev/null || exit 2;` 하나로 정의 확인을 대신한다.
두 판(시작 커밋 · 끝 판) 풀기가 끊기거나 마흔여섯 파일 가운데 하나라도 끝 판에서 비면(새 파일 둘을 뺀 마흔넷은 시작 판에서도) `common.sh` 가 `SNAPSHOT_FAIL` 을 내고 종료 코드 2 로 끝난다.
`END_UNRESOLVED` 가 찍히면 셸이 종료 코드 2 로 끝난다 — `HEAD` 로 바꿔 재지 않는다. 셸이 끝나면 임시 폴더를 지운다. `m` 의 종료 코드는 판정하지 않는다 — 판정은 출력 값으로 한다.
블록 · 검사 코드 · 훅 · 러너 대조는 끝 판을 푼 폴더의 사본에서만 돈다 — 작업 폴더는 바뀌지 않는다.

아래 블록 여덟을 각 블록 첫 주석 줄(셔뱅 다음 `#` 줄, 파이썬은 docstring 첫 낱말)의 파일 이름 그대로 한 폴더에 저장하고 그 폴더를 `K` 에 넣는다. `mdrules.sh` 옆에는 `node_modules` 를
`/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/de8c7935-a5b6-4df5-9106-fafa73c288a0/scratchpad/p1build/node_modules` 로 잇고 `cfg.markdownlint-cli2.jsonc` = `{ "config": { "MD013": false } }` 를 둔다.
준비 단계 실측(2026-09-26): 그 자리의 `.bin/markdownlint-cli2 --version` 첫 줄 `markdownlint-cli2 v0.23.2 (markdownlint v0.41.1)` · `command -v bash` → `/opt/homebrew/bin/bash` (5.3.9) ·
`bash -c 'type grep'` → `/usr/bin/grep` (BSD grep 2.6.0 — 이 맥 zsh 의 `grep` 은 ugrep 함수라 `grep -c` 가 폴더를 훑어 결과가 다르다, 측정은 bash 로만) · `zsh` · `jq` · `lsof` · `actionlint` · `shellcheck` · `perl` · `python3` + PyYAML 있음.
세 판을 `${TMPDIR:-/tmp}/f2r.XXXXXX` 에 푸니 `TMPDIR` 를 스크래치 폴더로 두고 읽는다. `END_OVERRIDE` 는 예행에서만 쓴다 — 평가에서는 비운다.

예행 도구(스크래치 `kaizen/f2d/`): `start/`(시작 커밋 판을 푼 폴더) · `k/mock.py`(시작 판에 이 계약이 요구하는 편집을 적용한다 — 문장은 한 예시) · `rh/`(mock 을 적용한 판) ·
`k/rehearse.sh`(시작 커밋에서 예행 저장소 `rrepo/` 를 만들어 봉인 · 묶음마다 한 커밋 · notes · `end_sha` 를 흉내 내고, 변형 저장소를 만든다) · `k/del.sh`(끝 판 사본에서 토큰이 든 줄만 지우고 값이 바뀌는지 본다) · `k/vedit.py`(계약 초안 검토 뒤 더한 변형 열둘의 편집 — `rehearse.sh` 가 부른다).

```bash
#!/usr/bin/env bash
# common.sh — 측정 공통 정의. bash 로 읽는다 (zsh 는 따옴표 없는 변수를 쪼개지 않고 배열 첨자가 1 부터다)
[ -n "${BASH_VERSION:-}" ] || { echo "NOT_BASH — bash -c 안에서 다시 읽는다"; exit 2; }
export LC_ALL=C.UTF-8   # 번역투 정규식이 글자 단위로 돌아야 한다
cd "${R:-/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/kaizen-0924}" || exit 2
B=6a8be196d9c40a1686f51f9a6bd50039c2bd5b71                  # 이 계약 시작 HEAD (main 합침 커밋)
SIG='Kaizen-Phase: kaizen-0924-f2-review-fixes'
CF=.harness/sprint-contract-kaizen-0924-f2-review-fixes.md
AM=.harness/sprint-amendments-kaizen-0924-f2-review-fixes.md
NOTES=.harness/.meta/kaizen-0924/f2-review-fixes-notes.md
AUD=.harness/.meta/orchestrator-audit-log.md
END=$( [ -f "$AM" ] && sed -n 's/^end_sha:[[:space:]]*//p' "$AM" | tail -1 )
[ -n "${END_OVERRIDE:-}" ] && END=$END_OVERRIDE             # 예행에서만 쓴다
if [ -z "$END" ] || ! git rev-parse -q --verify "$END^{commit}" >/dev/null; then
  echo "END_UNRESOLVED — 측정을 멈춘다. HEAD 로 바꿔 재지 않는다"; exit 2
fi
END=$(git rev-parse "$END")
: "${K:?도우미 폴더를 K 에 넣는다}"
# 묶음 — 한 커밋은 이 가운데 하나만 건드린다 (러닝북 「한 커밋에 킷 하나」. 킷 문서 사이트 쪽은 그 킷 묶음에 든다)
GRPS=(scripts claude harness ci react design flutter reflect api rust onboarding bambu readme)
declare -A GPATH=(
  [scripts]="scripts/" [claude]=".claude/skills/" [harness]="harness/ docs/harness/" [ci]=".github/workflows/ci.yml"
  [react]="react-kit/" [design]="design-kit/ docs/design-kit/" [flutter]="flutter-toolkit/" [reflect]="reflect-kit/ docs/reflect-kit/"
  [api]="api-kit/ docs/api-kit/" [rust]="rust-kit/" [onboarding]="onboarding-kit/" [bambu]="bambu-kit/ docs/bambu-kit/" [readme]="README.md")
SCV=scripts/check-stale-values.py
KRE=.claude/skills/react-kaizen/SKILL.md; KDE=.claude/skills/design-kaizen/SKILL.md; KBE=.claude/skills/backend-kaizen/SKILL.md
KIN=.claude/skills/infra-kaizen/SKILL.md; KRU=.claude/skills/rust-kaizen/SKILL.md; KOR=.claude/skills/kaizen-orchestrator/SKILL.md
KTO=.claude/skills/tone-kaizen/SKILL.md; KDS=.claude/skills/docs-site/SKILL.md
HCS=harness/references/contract-schema.md; PCS=docs/harness/contract-schema.html
CI=.github/workflows/ci.yml
RLN=react-kit/skills/react-l10n/SKILL.md
DVP=design-kit/references/visual-change-protocol.md; DGT=design-kit/evals/decision-gate-test.sh; DRD=design-kit/README.md
DTE=design-kit/skills/design-test/SKILL.md; DAU=design-kit/skills/design-audit/SKILL.md; DRV=design-kit/agents/design-reviewer.md
PVP=docs/design-kit/visual-change-protocol.html; PDT=docs/design-kit/design-test.html
FSR=flutter-toolkit/skills/flutter-scenario-report/SKILL.md; FRF=flutter-toolkit/skills/flutter-scenario-report/references/record-format.md
FTT=flutter-toolkit/evals/scenario-report/test_build_report.py; FEX=flutter-toolkit/evals/scenario-report/example
FE1=$FEX/TC-001-transfer-leader-cancel/record.json; FE2=$FEX/TC-002-appoint-vice-leader/record.json; FEI=$FEX/index.html
FRD=flutter-toolkit/README.md; FPR=flutter-toolkit/skills/flutter-preflight/SKILL.md
RLR=reflect-kit/hooks/log-reflection.sh; RLIB=reflect-kit/hooks/_lib-project-id.sh; RCT=reflect-kit/evals/hooks/collect-status-test.sh
RLT=reflect-kit/evals/hooks/log-reflection-test.sh; RSC=reflect-kit/docs/SCHEMA.md; RDE=reflect-kit/docs/DESIGN.md; RDG=reflect-kit/skills/reflect-digest/SKILL.md
PRS=docs/reflect-kit/schema.html; PRD=docs/reflect-kit/design.html
AUI=api-kit/skills/api-ui/SKILL.md; PAV=docs/api-kit/static-evidence-viewer-contract.html
RAU=rust-kit/skills/rust-audit/SKILL.md
OEV=onboarding-kit/skills/setup-guide/evals/evals.json; OFX=onboarding-kit/skills/setup-guide/evals/fixtures/gate-fail-ledger-misplaced.md
BAM=bambu-kit/skills/bambu-print-profile/SKILL.md; PBA=docs/bambu-kit/bambu-print-profile.html
RMD=README.md
FILES=("$SCV" "$KRE" "$KDE" "$KBE" "$KIN" "$KRU" "$KOR" "$KTO" "$KDS" "$HCS" "$PCS" "$CI" "$RLN"
       "$DVP" "$DGT" "$DRD" "$DTE" "$DAU" "$DRV" "$PVP" "$PDT"
       "$FSR" "$FRF" "$FTT" "$FE1" "$FE2" "$FEI" "$FRD" "$FPR"
       "$RLR" "$RLIB" "$RCT" "$RLT" "$RSC" "$RDE" "$RDG" "$PRS" "$PRD"
       "$AUI" "$PAV" "$RAU" "$OEV" "$OFX" "$BAM" "$PBA" "$RMD")
NEWF=("$DGT" "$OFX")   # 이 계약이 새로 만드는 파일 — 시작 판에는 없다
T=$(mktemp -d "${TMPDIR:-/tmp}/f2r.XXXXXX") && T=$(cd "$T" && pwd -P) || exit 2
mkdir -p "$T/B" "$T/E"
trap 'rm -rf "$T"' EXIT
# 두 판을 풀어 둔 폴더에서 잰다 — 작업 폴더에 남은 다른 세션의 미커밋 변경이 끼지 않는다. 풀기가 끊기면 멈춘다
git archive "$B" | tar -x -C "$T/B" && git archive "$END" | tar -x -C "$T/E" || { echo "SNAPSHOT_FAIL — 측정을 멈춘다"; exit 2; }
# 끝 판이 시작 커밋과 같으면(예행에서 시작 판 값을 잴 때만) 새 파일 둘은 없어도 된다
for f in "${FILES[@]}"; do [ "$END" = "$B" ] && case " ${NEWF[*]} " in *" $f "*) continue ;; esac; [ -s "$T/E/$f" ] || { echo "SNAPSHOT_FAIL $f"; exit 2; }; done
for f in "${FILES[@]}"; do case " ${NEWF[*]} " in *" $f "*) continue ;; esac; [ -s "$T/B/$f" ] || { echo "SNAPSHOT_FAIL start $f"; exit 2; }; done
# sect <파일> <제목 앞부분> — 그 제목부터 같은 깊이 이하의 다음 제목 전까지. 코드 펜스 안의 `#` 줄은 제목으로 보지 않는다
sect() { awk -v h="$2" '
  /^[[:space:]]*(```|~~~)/ { fence = !fence }
  !f && !fence && index($0, h) == 1 { f = 1; lvl = match($0, /[^#]/) - 1; print; next }
  f && !fence && /^#+ / { l = match($0, /[^#]/) - 1; if (l <= lvl) exit }
  f' "$1"; }
cnt() { grep -cF -- "$2" "$1"; }                                   # cnt <파일> <글> — 그 글이 든 줄 수
toks() { local s="$1" o=""; shift; for t in "$@"; do o="$o$(printf '%s\n' "$s" | grep -cF -- "$t") "; done; echo "${o% }"; }
alltok() { local l; while IFS= read -r l; do local ok=1 t; for t in "${@:2}"; do case $l in *"$t"*) ;; *) ok=0 ;; esac; done; [ "$ok" = 1 ] && echo "$l"; done < "$1" | grep -c .; }
ptext() { python3 -c 'import html,re,sys; h=open(sys.argv[1],encoding="utf-8").read(); h=re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>"," ",h); print(re.sub(r"\s+"," ",html.unescape(re.sub(r"<[^>]+>"," ",h))))' "$1"; }
fmb() { awk 'NR==1&&/^---/{fm=1;next} fm&&/^---/{exit} fm' "$1"; }
barefence() { awk '/^[[:space:]]*```/{ if (!o) { o = 1; if ($0 ~ /^[[:space:]]*```[[:space:]]*$/) n++ } else o = 0 } END{print n+0}' "$1"; }
added1() { if [ -f "$T/B/$1" ]; then git diff --no-index -U0 "$T/B/$1" "$T/E/$1"; else git diff --no-index -U0 /dev/null "$T/E/$1"; fi | grep '^+' | grep -v '^+++'; }
added() { for f in "${FILES[@]}"; do added1 "$f"; done; }
unsigned_on() { _b=${1}; _u=${2}; _s=${3}; shift 3
  git log --format=%H "${_b}..${_u}" -- "$@" | while read -r _c; do git log -1 --format=%B "$_c" | grep -qxF "$_s" || echo "$_c"; done; }
signed_commits() { git log --format=%H "${B}..${END}" --grep="^${SIG}\$"; }
group_of() { local g p; for g in "${GRPS[@]}"; do for p in ${GPATH[$g]}; do case $1 in "$p"*) echo "$g"; return ;; esac; done; done; }
scope() { awk '/^## /{s=$0} s ~ /^## 범위 경계/ && /^```text$/{b=1; n=0; next} b && /^```$/{b=0; next} b{n++; if (n==1 && $0 != "# sprint-scope") b=0; else if (n>1) print}' "$1"; }
fm_get() { awk -v k="^$2:[[:space:]]*" 'NR==1 && /^---[[:space:]]*$/ { fm=1; next } fm && /^---[[:space:]]*$/ { exit } fm && $0 ~ k { sub(k, "", $0); print; exit }' "$1" | sed -e "s/[[:space:]]*$//" -e "s/^['\"]//" -e "s/['\"]\$//"; }
sha256_16() { if command -v sha256sum >/dev/null 2>&1; then sha256sum; elif command -v shasum >/dev/null 2>&1; then shasum -a 256; else python3 -c 'import hashlib,sys; print(hashlib.sha256(sys.stdin.buffer.read()).hexdigest())'; fi | cut -c1-16; }
contract_digest() { grep -E '^- \[[ x]\] [A-Z]{2,}-[0-9]{2}' "$1" | sed -E 's/^- \[[ x]\]/- [ ]/' | sha256_16; }
verify_seal() { rec=$(fm_get "$1" conditions_digest); rec=${rec#sha256:}; if [ -z "$rec" ]; then echo "SEAL_ABSENT $1"; return 0; fi
  act=$(contract_digest "$1"); if [ "$rec" = "$act" ]; then echo "SEAL_OK $1"; else echo "SEAL_BROKEN $1 recorded=$rec actual=$act"; fi; }
# cp1 <판 폴더> <이름> <경로…> — 그 판의 경로들을 $T/<이름>/ 아래로 복사한다 (시험 · 변형은 사본에서만 돈다)
cp1() { local src=$1 dst=$T/$2; shift 2; rm -rf "$dst"; mkdir -p "$dst"; for d in "$@"; do mkdir -p "$dst/$(dirname "$d")"; cp -R "$src/$d" "$dst/$d" || return 2; done; printf '%s' "$dst"; }
K02='(을|를) ?(처리|관리)(합니다|한다)|에 대해서?|하도록 (합니다|한다)|에 의(해|하여)|되어 있(는 경우|을 때)|(표시|적용|호출|생성|반환)(됩니다|된다)'   # tone-kit/references/locale-korean.md §2 grep 열
NAMES='fit-?pal|fit_pal|fit pal|flutter[-_]playwright|playwright-mcp|chrome-devtools-mcp'
TOOLN='find_widget|verify_visible|tap_native_point|tap_widget|Flutter Playwright'   # flutter-scenario-report 두 문서에서 뺄 화면 조종 도구 · 서버 이름
```

```bash
#!/usr/bin/env bash
# m.sh — 조건마다 한 갈래. common.sh 를 먼저 읽은 bash 셸에서 `m <조건 ID>` 로 부른다. 판정은 출력 값으로 한다
# sealrun <판 폴더> <셸> <missing|full> — 계약 봉인 범위 블록을 정의 네 개 가운데 둘만 둔 셸(missing) · 넷 다 둔 셸(full)에서 돌린다
sealrun() { local d=$T/seal-$2-$3 o rc
  rm -rf "$d"; mkdir -p "$d/.harness"
  python3 - "$1/$HCS" "$d" <<'PY' || return 2
import re, sys
s = open(sys.argv[1], encoding="utf-8").read(); d = sys.argv[2]
bl = re.findall(r"(?ms)^```bash\n(.*?)^```", s)
fm = next(b for b in bl if "fm_get() { # fm_get <file> <key>" in b)
sv = next(b for b in bl if "verify_seal() {  # verify_seal" in b)
rg = next(b for b in bl if "# .harness/ 의 계약 파일만 골라" in b)
open(d + "/defs.sh", "w").write(fm + sv)
open(d + "/range.sh", "w").write(rg)
PY
  printf -- '---\nconditions_digest: sha256:%s\n---\n- [ ] SK-01: a\n' "$(printf -- '- [ ] SK-01: a\n' | sha256_16)" > "$d/.harness/sprint-contract-x.md"
  { cat "$d/defs.sh"; [ "$3" = missing ] && echo 'unset -f contract_digest sha256_16'; cat "$d/range.sh"; } > "$d/run.sh"
  o=$(cd "$d" && "$2" run.sh 2>&1); rc=$?
  echo "$2:rc=$rc,stop=$(printf '%s\n' "$o" | grep -c '^STOP '),ok=$(printf '%s\n' "$o" | grep -cE '^ *1 SEAL_OK$'),broken=$(printf '%s\n' "$o" | grep -cE 'SEAL_BROKEN')"; }
# gate_matrix <판 폴더> — 결정 전파 검사를 문서에서 떼어 이 계약이 정한 입력 열로 돌린다 (구현이 만든 시험과 따로 잰다)
gate_matrix() { local d=$T/gm c name want out rc ok=0 tb=0 bad=""
  rm -rf "$d"; mkdir -p "$d"
  awk '/^```python/{b=1;n="";next} b&&/^```/{if(ok){exit} b=0;next} b{n=n $0 "\n"; if($0 ~ /Decision Propagation Coverage Gate/) ok=1} END{printf "%s", n}' "$1/$DVP" > "$d/g.py"
  grep -q 'Decision Propagation Coverage Gate' "$d/g.py" || { echo "gate EXTRACT_FAIL"; return 2; }
  local V='decision_id: DEC-20260813-001
    source: .design/approvals/DEC-20260813-001.md'
  printf 'decisions:\n  - %s\n    required_surfaces:\n      - surface_id: a\n        golden: g.png\n        assertions: ["main visible"]\n' "$V" > "$d/ok.yaml"
  printf 'decisions:\n  - decision_id: DEC-2026-1\n    source: s\n    required_surfaces:\n      - surface_id: a\n        assertions: ["main visible"]\n' > "$d/badid.yaml"
  printf 'decisions:\n  - %s\n    required_surfaces:\n      - surface_id: a\n        assertions: ["main visible"]\n    excluded_surfaces: [onboarding.mobile]\n' "$V" > "$d/exstr.yaml"
  printf 'decisions: [DEC-20260813-001]\n' > "$d/decstr.yaml"
  printf -- '- a\n- b\n' > "$d/toplist.yaml"
  printf 'decisions:\n  - %s\n    required_surfaces: [dashboard.desktop]\n' "$V" > "$d/reqstr.yaml"
  printf 'decisions:\n  - %s\n    required_surfaces:\n      - surface_id: a\n        golden: g.png\n' "$V" > "$d/goldonly.yaml"
  printf 'decisions:\n  - %s\n    required_surfaces:\n      - surface_id: a\n        golden: g.png\n        assertions: "main visible"\n' "$V" > "$d/assertstr.yaml"
  printf 'decisions: []\n' > "$d/empty.yaml"
  for c in ok:0 badid:2 exstr:2 decstr:2 toplist:2 reqstr:2 assertstr:2 goldonly:1 empty:3 missing:3; do
    name=${c%%:*}; want=${c##*:}
    out=$(python3 "$d/g.py" "$d/$name.yaml" 2>&1); rc=$?
    printf '%s\n' "$out" | grep -q '^Traceback' && tb=$((tb + 1))
    [ "$rc" = "$want" ] && ok=$((ok + 1)) || bad="$bad $name=$rc"
  done
  echo "gate ok=$ok/10 traceback=$tb${bad:+ wrong:$bad}"; }
# bambu_stale <판 폴더> — 앞 실행의 design.json · instances.json 을 둔 채 받기가 전부 실패하는 가짜 curl 로 MakerWorld 받기 블록을 돌린다
bambu_stale() { local d=$T/mw o
  rm -rf "$d"; mkdir -p "$d/bin" "$d/out"
  cat > "$d/bin/curl" <<'SH'
#!/usr/bin/env bash
# 가짜 curl — 연결 실패처럼 -o 파일을 쓰지 않고 %{http_code} 를 000 으로 찍고 종료 코드 7
w=; while [ $# -gt 0 ]; do case $1 in -w) w=$2; shift 2 ;; -o) shift 2 ;; *) shift ;; esac; done
printf "${w//%\{http_code\}/000}"; exit 7
SH
  chmod +x "$d/bin/curl"
  python3 - "$1/$BAM" "$d/run.sh" <<'PY' || return 2
import sys
L = open(sys.argv[1], encoding="utf-8").read().split("\n")
s = next(i for i, l in enumerate(L) if l.startswith("ID=<모델 번호>; OUT=<output_dir>/makerworld;"))
e = next(j for j in range(s, len(L)) if L[j] == "```")
body = "\n".join(L[s:e]).replace("ID=<모델 번호>; OUT=<output_dir>/makerworld;", 'ID=1; OUT="$MWOUT";', 1)
open(sys.argv[2], "w", encoding="utf-8").write(body + "\n")
PY
  printf '{"title":"OLD-MODEL","commentCount":3,"instances":[1]}' > "$d/out/design.json"
  printf '{"hits":[{"id":1}],"total":1}' > "$d/out/instances.json"
  o=$(PATH="$d/bin:$PATH" MWOUT="$d/out" bash "$d/run.sh" 2>&1)
  echo "mw stale_title=$(printf '%s\n' "$o" | grep -c 'OLD-MODEL') fail_line=$(printf '%s\n' "$o" | grep -c '^FAIL design.json') left=$(find "$d/out" -maxdepth 1 \( -name design.json -o -name instances.json \) | grep -c .)"; }
# stale_run <판 폴더> <주입 여부 0|1> — 그 판 전체 사본에서 옛 값 검사를 돌린다. 1 이면 backend-kit 스킬 한 줄에 등록 옛 값을 넣는다
stale_run() { local d o rc
  d=$(cp1 "$1" sv$2 .) || return 2
  [ "$2" = 1 ] && printf '\nOpenAPI 3.1.1 최신\n' >> "$d/backend-kit/skills/backend-test/SKILL.md"
  o=$(cd "$d" && python3 scripts/check-stale-values.py 2>&1); rc=$?
  echo "inject=$2 rc=$rc scope=$(printf '%s\n' "$o" | sed -nE 's/^검사 범위: 소스 디렉토리 ([0-9]+\/[0-9]+).*/\1/p') excluded_line=$(printf '%s\n' "$o" | grep -c '검사 제외:') hit=$(printf '%s\n' "$o" | grep -c '^  backend-kit/skills/backend-test/SKILL.md:')"; }
m() {
  type sect added verify_seal group_of sealrun gate_matrix >/dev/null 2>&1 || { echo "HELPER_MISSING"; return 2; }
  [ -d "$T/E" ] && [ -d "$T/B" ] || { echo "SNAPSHOT_MISSING"; return 2; }
  local E=$T/E Bd=$T/B
  case $1 in
  SK-01)
    # A2 — 커밋 명령에 서명 줄 · 옛 「오케스트레이터가 커밋」 문장 0. B2 — I-02 목록 넷의 슬러그 경로 셋
    echo "design_cmd=$(alltok "$E/$KDE" 'git commit -o <내 경로>' 'Kaizen-Phase: <슬러그>') react_cmd=$(alltok "$E/$KRE" 'git commit -o <내 경로>' 'Kaizen-Phase: <슬러그>') old=$(cat "$E"/.claude/skills/*/SKILL.md | grep -cE 'git add/commit/tag 를 직접 실행하지 마라|커밋은 오케스트레이터(가|에)|Phase 로 호출한 경우 이 Step 을 실행하지 마라')"
    local f o=""
    for f in "$KBE" "$KDE" "$KIN" "$KRU"; do
      o="$o $(basename "$(dirname "$f")")=$(toks "$(grep -F '**I-02 예외 목록 명시화**' "$E/$f")" '`.harness/sprint-contract-<slug>.md`' '`.harness/sprint-feedback-<slug>.md`' '`.harness/sprint-amendments-<slug>.md`' | tr -d ' ' | awk '{print gsub(/1/,"")}')/3"
    done; echo "i02$o" ;;
  SK-02)
    # B3 — Final 조건 줄의 스킬 수가 실제 수와 같다. B4 — docs/tone 파일 수
    local l pl rf pn rn tn tc
    l=$(grep -F 'Phase 1에서 업데이트된 설계 원칙이 Phase 2~17 변경에 반영되었는가' "$E/$KOR")
    pl=$(printf '%s\n' "$l" | sed -nE 's/.*planning-kit ([0-9]+) 스킬.*/\1/p'); rf=$(printf '%s\n' "$l" | sed -nE 's/.*reflect-kit ([0-9]+) 스킬.*/\1/p')
    pn=$(find "$E/planning-kit/skills" -mindepth 2 -maxdepth 2 -name SKILL.md | grep -c .); rn=$(find "$E/reflect-kit/skills" -mindepth 2 -maxdepth 2 -name SKILL.md | grep -c .)
    tn=$(sed -nE 's/^- `docs\/tone\/\*\.md` ([0-9]+)종.*/\1/p' "$E/$KTO"); tc=$(find "$E/docs/tone" -maxdepth 1 -name '*.md' | grep -c .)
    echo "planning=${pl:-X}/$pn reflect=${rf:-X}/$rn tone_docs=${tn:-X}/$tc"
    # B5 — F2 표의 원본 경로가 모두 detect-docs-drift 매핑(접두 또는 개별 파일)에 있다 · api-kit 행에 references 없음
    # B13 — docs-site Step 1 표 행이 F2 표 행과 글자 그대로 같다. B12 — AUTO 밖에 범위 합치기 줄
    python3 - "$E" <<'PY'
import importlib.util, re, sys
E = sys.argv[1]
o = open(E + "/.claude/skills/kaizen-orchestrator/SKILL.md", encoding="utf-8").read()
a = o.index("### Step F2")
rows = [l for l in o[a:].split("\n**절차:**")[0].splitlines() if l.startswith("| ") and "`docs/" in l]
spec = importlib.util.spec_from_file_location("ddd", E + "/scripts/detect-docs-drift.py"); m = importlib.util.module_from_spec(spec)
sys.argv = ["x"]; spec.loader.exec_module(m)
pre = [p for p, _ in m.SOURCE_TO_HTML]; ov = set(m.SOURCE_OVERRIDES)
unc = []
for r in rows:
    src = r.split("|")[2]
    for p in re.findall(r"`([^`]+)`", src):
        if not (p in ov or any(p.startswith(x) for x in pre)):
            unc.append(p)
api = [r for r in rows if r.startswith("| api-kit |")]
d = open(E + "/.claude/skills/docs-site/SKILL.md", encoding="utf-8").read()
s1 = d[d.index("## Step 1"):d.index("## Step 2")]
drows = [l for l in s1.splitlines() if l.startswith("| ") and "`docs/" in l]
print(f"f2_rows={len(rows)} uncovered={len(unc)} api_ref={sum('api-kit/references/' in r for r in api)} docs_site_rows={len(drows)} same={int(drows == rows)} {unc[:3]}")
PY
    # Codex N2 — Phase 17 의무 리서치 표가 없는 동안 쓸 출처를 같은 줄이 가리킨다
    echo "phase_dep_line=$(awk '/AUTO:plugin_phases:begin/{a=1} /AUTO:plugin_phases:end/{a=0; next} !a' "$E/$KOR" | grep -F 'references/phase-dependencies.md' | grep -F '합친' | grep -cF '`hooks/`') p17_src=$(grep -F 'Phase 17 표는 아직 없다' "$E/$KOR" | grep -F 'howto-research/SKILL.md' | grep -cF 'Step 1')" ;;
  SK-03)
    # A5 — 세 자리가 종료 코드 2 · 3 을 다룬다. design-test 는 「위반 0」 대신 종료 코드 0
    echo "test: v0=$(cnt "$E/$DTE" '위반 0') row=$(grep -F '| 결정 전파 |' "$E/$DTE" | grep -cF '종료 코드 0') c2=$(alltok "$E/$DTE" '종료 코드 2' 'SCHEMA_ERROR') c3=$(alltok "$E/$DTE" '종료 코드 3' 'NO_SURFACE' 'NO_DECISION')" \
      "| audit: c2=$(sect "$E/$DAU" '## Step 5' > "$T/a5"; alltok "$T/a5" '종료 코드 2' 'SCHEMA_ERROR' 'REJECT') c3=$(alltok "$T/a5" '종료 코드 3' 'NO_SURFACE' 'NO_DECISION')" \
      "| reviewer: c2=$(alltok "$E/$DRV" '종료 코드 2' 'SCHEMA_ERROR' 'REJECT') c3=$(alltok "$E/$DRV" '종료 코드 3' 'NO_SURFACE' 'NO_DECISION')" ;;
  SK-04)
    # A6 — 킷 안 특정 앱 이름 0 · 두 문서의 도구 · 서버 이름 0 · 단위 시험 통과 · README AUTO 동기. B8 — 실패 틀 codegen 줄. B14 — 루트 README 수
    local u ur ut sk n
    echo "fitpal=$(grep -rniE 'fit-?pal|fit_pal' "$E/flutter-toolkit" | grep -c .) names_skill=$(grep -cE "$TOOLN" "$E/$FSR") names_format=$(grep -cE "$TOOLN" "$E/$FRF")"
    u=$(cp1 "$E" ut flutter-toolkit) || return 2
    ut=$(cd "$u" && python3 -m unittest discover -s flutter-toolkit/evals/scenario-report 2>&1); ur=$?
    echo "unittest rc=$ur $(printf '%s\n' "$ut" | grep -E '^Ran [0-9]+ tests')"
    # 실패 틀만 본다 — 성공 틀(「Ready to commit.」 쪽)의 codegen 줄은 success 가 맞다
    awk '/^하나라도 실패하면/{f=1} f&&/^Fix the issues above/{exit} f' "$E/$FPR" > "$T/pfail"
    echo "preflight new=$(grep -c '^  2\. codegen : success / failed / skipped · 삭제' "$T/pfail") old=$(grep -c '^  2\. codegen : success · 삭제' "$T/pfail")"
    sk=$(find "$E/flutter-toolkit/skills" -mindepth 2 -maxdepth 2 -name SKILL.md | grep -c .)
    n=$(sect "$E/$RMD" '### flutter-toolkit' | sed -n 's/^\*\*제공 스킬:\*\* //p' | tr ',' '\n' | grep -c .)
    echo "readme intro=$(sect "$E/$RMD" '### flutter-toolkit' | sed -nE 's/^Flutter 프로젝트 전용 개발 워크플로우 스킬 ([0-9]+)종\.$/\1/p')/$sk tree=$(awk '/^├── flutter-toolkit\//{f=1;next} f&&/skills\//{print;exit}' "$E/$RMD" | sed -nE 's/.*스킬 ([0-9]+)종.*/\1/p')/$sk list=$n/$sk has_sr=$(sect "$E/$RMD" '### flutter-toolkit' | grep '^\*\*제공 스킬:\*\*' | grep -c 'scenario-report')" ;;
  SK-05)
    # A3 — 지워진 번역 블록을 빈 번역 키만 지운 저장소 · 채운 번역을 지운 저장소에서 bash · zsh 로 돌린다
    local c sh o=""
    for c in empty filled; do for sh in bash zsh; do o="$o $c/$sh=[$(bash "$K/l10n.sh" "$E/$RLN" $c $sh | tr -d '\n')]"; done; done; echo "l10n$o"
    echo "sentence=$(cnt "$E/$RLN" '`filled_deleted=0` 이 아니면') grep_second=$(grep -F 'git diff -U0 -- src/infrastructure/i18n/locales/ | ' "$E/$RLN" | grep -cF '| grep')" ;;
  SK-06)
    # B7 — Gotcha 16 이 가리키는 자리가 실제로 있다. B9 — 0 건 설명의 명령이 폴더를 재귀로 세고 0 건에도 종료 코드 0
    local g16 cmd d o1 r1 o0 r0
    g16=$(grep -F '16. **파이프라인 종료 코드로만' "$E/$RAU")
    echo "g16 ref=$(printf '%s\n' "$g16" | grep -cF 'rust-run §2 첫 항목') old=$(printf '%s\n' "$g16" | grep -cF 'rust-run (c)') run2_first4=$(sect "$E/rust-kit/skills/rust-run/SKILL.md" '## 2. 실행 + 결과 출력' | awk 'f&&!/^  /{exit} /^- /{if(f)exit; f=1} f' | grep -c '네 칸')"
    cmd=$(grep -F '→ 0 을 "안티패턴 없음 PASS"' "$E/$RAU" | head -1 | sed -nE 's/^[[:space:]]*- `([^`]+)`.*/\1/p')
    d=$T/rs; rm -rf "$d"; mkdir -p "$d/src/sub"
    printf 'fn a(){ x.unwrap(); }\n' > "$d/src/a.rs"; printf 'fn b(){ y.unwrap(); }\n' > "$d/src/sub/b.rs"; printf 'z.unwrap()\n' > "$d/src/note.txt"
    o1=$(cd "$d" && bash -c "$cmd" 2>&1); r1=$?
    printf 'fn a(){}\n' > "$d/src/a.rs"; printf 'fn b(){}\n' > "$d/src/sub/b.rs"
    o0=$(cd "$d" && bash -c "$cmd" 2>&1); r0=$?
    echo "cmd two_hits=[$o1] rc=$r1 zero=[$o0] rc=$r0 no_src_note=$(grep -F '→ 0 을 "안티패턴 없음 PASS"' "$E/$RAU" | grep -F '가 없으면' | grep -cF '(a) 로 거른다')" ;;
  SK-07)
    # A8 — 여는 방법 블록을 bash · zsh 로 돌려 찍힌 번호가 포트를 쥔 파이썬인지 · 문장
    bash "$K/api_serve.sh" "$E"
    local l; l=$(awk '/^1\. \*\*여는 방법\*\*/{f=1} f&&/^2\. \*\*콘솔 오류\*\*/{exit} f' "$E/$AUI")
    echo "no_amp=$(printf '%s\n' "$l" | grep -cF '`&&` 로 잇지 않는다') both_shells=$(printf '%s\n' "$l" | grep -cF 'bash · zsh')" ;;
  SK-08)
    # B11 — 앞 모델 파일이 남은 폴더에서 받기가 전부 실패하면 옛 제목을 보고하지 않는다
    bambu_stale "$E" ;;
  SC-00|RE-01|DG-01|DG-03)
    # N/A 넷 — release.sh · marketplace · plugin.json 을 건드린 커밋 수 · 새 파일 목록 · analyze/test 대상 교집합
    echo "SC-00=$(git log --oneline "$B..$END" -- scripts/release.sh .claude-plugin/marketplace.json '*/.claude-plugin/plugin.json' | grep -c .)" \
      "RE-01=$(git diff --name-only --diff-filter=A "$B" "$END" -- . ':(exclude).harness' | LC_ALL=C sort | tr '\n' ' ')" \
      "DG-01=$(git diff --name-only "$B" "$END" | grep -cx 'scripts/release.sh')" ;;
  ER-01)
    # A1 — 끝 판은 backend-kit 을 빼지 않고, 넣은 옛 값을 잡는다 (시작 판은 못 잡는다)
    stale_run "$E" 0; stale_run "$E" 1 ;;
  ER-02)
    # A4 — 입력 열의 종료 코드 · 킷 시험 통과 · 킷 시험을 시작 판 문서로 돌리면 실패 (음성 대조)
    gate_matrix "$E"
    local tc r1 r2
    tc=$(cp1 "$E" dgt design-kit) || return 2
    bash "$tc/$DGT" > "$T/dgt1" 2>&1; r1=$?
    DECISION_GATE_DOC="$Bd/$DVP" bash "$tc/$DGT" > "$T/dgt2" 2>&1; r2=$?
    echo "kit_test rc=$r1 $(grep '^결과' "$T/dgt1") start_doc rc=$r2 $(grep '^결과' "$T/dgt2") exec=$(git ls-tree "$END" -- "$DGT" | awk '{print $1}')" ;;
  ER-03)
    # B1 — 봉인 범위 블록이 정의 넷 가운데 하나라도 없으면 멈춘다 · 넷 다 있으면 센다
    echo "missing $(sealrun "$E" bash missing) $(sealrun "$E" zsh missing) | full $(sealrun "$E" bash full) $(sealrun "$E" zsh full)" ;;
  ER-04)
    # A7 — no issues 로 끝난 실행 뒤 경고 없음 · 그 뒤 실패는 다시 경고 · 킷 시험 둘 · 시작 판 코드로 돌리면 실패 · 태그 문서화 · digest 문장
    bash "$K/reflect_e2e.sh" "$E"
    local rk o1 r1 o2 r2 o3 r3 o4 r4 code
    rk=$(cp1 "$E" rk reflect-kit) || return 2
    o1=$(bash "$rk/$RCT" 2>&1); r1=$?; o2=$(bash "$rk/$RLT" 2>&1); r2=$?
    o3=$(PROJECT_ID_LIB="$Bd/$RLIB" bash "$rk/$RCT" 2>&1); r3=$?
    o4=$(REFLECT_KIT_HOOKS="$Bd/reflect-kit/hooks" bash "$rk/$RLT" 2>&1); r4=$?
    echo "tests collect rc=$r1 [$(printf '%s\n' "$o1" | grep '^결과')] log rc=$r2 [$(printf '%s\n' "$o2" | grep '^결과')] | start_lib rc=$r3 start_hook rc=$r4"
    # 훅이 적는 사유 태그 줄기 — 변수로 끝나는 줄기(`fail:` · `env-dedup:` · `fallback:claude-exit-`)는 뺀다
    code=$(cat "$E"/reflect-kit/hooks/*.sh | grep -ohE '"(ok|skip|fail|fallback|warn|vocab|env-dedup):[A-Za-z0-9_/-]*' | tr -d '"' | sed -E 's/-+$//' | grep -v ':$' | sort -u)
    tagdoc() { grep -oE '^- `[a-z-]+:[A-Za-z0-9_/<>-]*' "$1" | sed 's/^- `//' | sed -E 's/<[^>]*>//g; s/-+$//' | sort -u; }
    echo "tags code=$(printf '%s\n' "$code" | grep -c .) has_ok=$(printf '%s\n' "$code" | grep -cx 'ok:no-issues') schema_missing=$(comm -23 <(printf '%s\n' "$code") <(tagdoc "$E/$RSC") | grep -c .) design_missing=$(comm -23 <(printf '%s\n' "$code") <(tagdoc "$E/$RDE") | grep -c .) digest_g13=$(grep -F '13. **엔트리 0 을' "$E/$RDG" | grep -cF 'ok:no-issues') digest_in=$(grep -F '/.errors.log` — 훅 자체 실패 로그' "$E/$RDG" | grep -cF 'ok:no-issues')" ;;
  ER-05)
    # B10 — 러너 통과 · 픽스처 등록 · misplaced 판정 두 줄을 지운 사본에서 러너가 실패 (시작 판에서는 같은 삭제가 통과했다)
    local oc o r n
    oc=$(cp1 "$E" ob onboarding-kit) || return 2
    o=$(sh "$oc/onboarding-kit/skills/setup-guide/evals/run-gate-evals.sh" 2>&1); r=$?
    echo "runner rc=$r $(printf '%s\n' "$o" | grep '^EVALS declared') $(printf '%s\n' "$o" | tail -1) case=$(python3 -c 'import json,sys; print(sum(1 for c in json.load(open(sys.argv[1]))["gate_cases"] if c["fixture"]=="fixtures/gate-fail-ledger-misplaced.md" and "G1_LEDGER FAIL steps=2 ledger=2 misplaced=2" in c["expect"] and c["expect"][-1]=="GATE_FAIL"))' "$E/$OEV")"
    python3 - "$oc/onboarding-kit/skills/setup-guide/SKILL.md" <<'PY' || { echo "NEG_EDIT_FAIL"; return 2; }
import sys
p = sys.argv[1]; L = open(p, encoding="utf-8").read().split("\n")
i = next(k for k, l in enumerate(L) if l.startswith('  elif [ "$misplaced" -ne 0 ]; then'))
del L[i:i + 2]; open(p, "w", encoding="utf-8").write("\n".join(L))
PY
    o=$(sh "$oc/onboarding-kit/skills/setup-guide/evals/run-gate-evals.sh" 2>&1); r=$?
    echo "no_misplaced_check rc=$r $(printf '%s\n' "$o" | tail -1)" ;;
  ER-06)
    # B6 · C L13 — CI validate 잡에 두 시험 줄 · actionlint · 두 명령이 끝 판에서 통과
    python3 - "$E/$CI" <<'PY'
import sys, yaml
d = yaml.safe_load(open(sys.argv[1], encoding="utf-8"))
runs = [s.get("run", "") for s in d["jobs"]["validate"]["steps"]]
want = ["python3 -m unittest discover -s flutter-toolkit/evals/scenario-report -v", "bash design-kit/evals/decision-gate-test.sh"]
print(f"ci jobs={len(d['jobs'])} validate_has={sum(1 for w in want if w in runs)}/2")
PY
    local c r1 r2
    command -v actionlint >/dev/null || { echo "TOOL_MISSING actionlint"; return 2; }
    actionlint "$E/$CI" >/dev/null 2>&1; echo "actionlint=$?"
    c=$(cp1 "$E" ci flutter-toolkit design-kit) || return 2
    (cd "$c" && python3 -m unittest discover -s flutter-toolkit/evals/scenario-report >/dev/null 2>&1); r1=$?
    (cd "$c" && bash design-kit/evals/decision-gate-test.sh >/dev/null 2>&1); r2=$?
    echo "run scenario=$r1 decision_gate=$r2" ;;
  ER-07)
    # 더한 줄의 번역투 · 특정 앱 · 서버 이름
    local a; a=$(added)
    echo "added=$(printf '%s\n' "$a" | grep -c .) k02=$(printf '%s\n' "$a" | grep -cE "$K02") names=$(printf '%s\n' "$a" | grep -ciE "$NAMES")" ;;
  ER-08)
    # notes · 감사 기록 한 줄 · 공유 파일 무변경
    local nt g sha ok=0 ad dl
    git cat-file -e "$END:$NOTES" 2>/dev/null && echo "notes_committed=1" || { echo "notes_committed=0"; return 0; }
    nt=$(git show "$END:$NOTES")
    toks "$nt" '## 커밋' '## 다룬 항목' '## 고치지 않은 항목과 이유' '## 다음 사이클 메모'
    for g in "${GRPS[@]}"; do
      sha=$(printf '%s\n' "$nt" | awk '/^## /{s=$0} s=="## 커밋"' | grep -E "^\| $g \|" | grep -oE '[0-9a-f]{7,40}' | head -1)
      [ -n "$sha" ] && git rev-parse -q --verify "$sha^{commit}" >/dev/null || continue
      git merge-base --is-ancestor "$sha" "$END" && git log -1 --format=%B "$sha" | grep -qxF "$SIG" || continue
      [ "$(git show --name-only --format= "$sha" | grep . | while read -r p; do group_of "$p"; done | sort -u | tr '\n' ' ')" = "$g " ] && ok=$((ok + 1))
    done; echo "commit_rows=$ok/${#GRPS[@]}"
    toks "$(printf '%s\n' "$nt" | awk '/^## /{s=$0} s=="## 다음 사이클 메모"')" 'commit-guard.sh' 'detect-docs-drift.py' 'sync-orchestrator.py' 'infra-test' 'VISUAL_CHANNEL' 'enum 값 검사 미실행' 'adapter-dart-flutter.md' 'noncharacter' 'slang' 'app-preflight' 'design-reviewer' 'planning-reviewer' 'excluded_surfaces' 'silent-check' 'delete-conflicting-outputs' 'RFC 7493' 'AUTO 마커' 'tone-research' 'reflect-kit/README.md'
    at=$(git diff "$B" "$END" -- "$AUD" | grep '^+' | grep -v '^+++' | grep -vc '^+[[:space:]]*$')
    ad=$(git diff "$B" "$END" -- "$AUD" | grep '^+' | grep -v '^+++' | grep -cF 'f2-review-fixes-notes.md'); dl=$(git diff "$B" "$END" -- "$AUD" | grep '^-' | grep -vc '^---')
    echo "audit added=$at added_ptr=$ad deleted=$dl shared_commits=$(git log --oneline "$B..$END" -- .claude-plugin/marketplace.json '*/.claude-plugin/plugin.json' CLAUDE.md .claude/kaizen-input/insights-report.md .harness/.meta/kaizen-failure-count.yaml .harness/stale-values.yaml docs/index.html docs/kaizen | grep -c .)" ;;
  AR-01)
    # 범위 — 여섯 값 (측정 절 참조)
    local s u out=0 inf mixed=0 one=0 c gs hs br p
    u=$(unsigned_on "$B" "$END" "$SIG" "${FILES[@]}" $(for g in "${GRPS[@]}"; do echo ${GPATH[$g]}; done) | sort -u | grep -c .)
    echo "$u"
    s=$(signed_commits)
    inf=$(for c in $s; do git show --name-only --format= "$c"; done | grep . | LC_ALL=C sort -u)
    out=$(printf '%s\n' "$inf" | while read -r p; do
      [ -z "$p" ] && continue
      case " ${FILES[*]} " in *" $p "*) continue ;; esac
      case $p in "$CF"|"$AM"|.harness/sprint-feedback-kaizen-0924-f2-review-fixes.md|.harness/.meta/kaizen-0924/f2-review-fixes-*.md|"$AUD") continue ;; esac
      echo "$p"; done | grep -c .)
    echo "$out $(for f in "${FILES[@]}"; do printf '%s\n' "$inf" | grep -qxF "$f" && echo 1; done | grep -c .)"
    for c in $s; do
      gs=$(git show --name-only --format= "$c" | grep . | while read -r p; do group_of "$p"; done | sort -u | grep -c .)
      hs=$(git show --name-only --format= "$c" | grep -c '^\.harness/')
      if [ "$gs" -ge 2 ] || { [ "$gs" -ge 1 ] && [ "$hs" -ge 1 ]; }; then mixed=$((mixed + 1)); elif [ "$gs" = 1 ]; then one=$((one + 1)); fi
    done; echo "mixed=$mixed one_kit=$one"
    rm -rf "$T/hs"; mkdir -p "$T/hs"; git archive "$END" .harness | tar -x -C "$T/hs"
    br=$(for c in $s; do git show --name-only --format= "$c"; done | grep '^\.harness/.*sprint-contract.*\.md$' | sort -u | while read -r p; do [ -f "$T/hs/$p" ] && (cd "$T/hs" && verify_seal "$p"); done | grep -c '^SEAL_BROKEN')
    echo "$br"
    (cd "$T/hs" && verify_seal "$CF" | awk '{print $1}')
    echo "scope_same=$( [ "$(scope "$T/hs/$CF" | grep -v '^\.harness/$' | LC_ALL=C sort)" = "$(printf '%s\n' "${FILES[@]}" | LC_ALL=C sort)" ] && echo 1 || echo 0) harness_line=$(scope "$T/hs/$CF" | grep -cx '\.harness/')" ;;
  AR-02)
    # 문서 사이트 일곱 쪽 — 원본이 바뀐 절만 맞추고 원본 담김은 옛 판 이상
    local pc pb pv pd ps pr pa
    pc=$(ptext "$E/$PCS"); pb=$(ptext "$E/$PBA"); pd=$(ptext "$E/$PDT"); ps=$(ptext "$E/$PRS"); pr=$(ptext "$E/$PRD"); pa=$(ptext "$E/$PAV")
    echo "schema=$(toks "$pc" 'type verify_seal fm_get contract_digest sha256_16' 'type verify_seal fm_get >/dev/null' | tr ' ' '/')" \
      "bambu=$(toks "$pb" 'rm -f "$OUT/design.json" "$OUT/instances.json"')" \
      "$(python3 "$K/blockcmp.py" "$E" "$DVP" "$PVP" 'Decision Propagation Coverage Gate' | awk '{print "vcp_" $4}')" \
      "design_test=$(toks "$pd" '위반 0' 'SCHEMA_ERROR' 'NO_SURFACE' | tr ' ' '/')" \
      "reflect=$(toks "$ps" 'ok:no-issues')/$(toks "$pr" 'ok:no-issues')" \
      "api=$(toks "$pa" '&& 로 잇지 않는다' '두 명령은 한 번의 셸 호출에서 잇는다' | tr ' ' '/')"
    local src page
    # wr 은 원본 낱말이 페이지 글에 든 비율 — 부분 편집이 원본 문장을 페이지에서 떨어뜨리면 준다
    while read -r src page; do python3 "$K/cov2.py" "$Bd" "$E" "$src" "$page" | awk '{w=$6; sub(/^wr=/,"",w); split(w,a,"->"); print $2, $5, (a[2]+0 >= a[1]+0 ? "wr_ok" : "wr_down")}'; done <<EOF
$DVP $PVP
$DTE $PDT
$HCS $PCS
$BAM $PBA
$RSC $PRS
$RDE $PRD
docs/api/verification/static-evidence-viewer-contract.md $PAV
$AUI $PAV
EOF
    ;;
  AP-01)
    local v a; v=$(for p in "$E"/*/.claude-plugin/plugin.json; do python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["version"])' "$p"; done | sort -u)
    a=$(added)
    echo "versions=$(printf '%s\n' "$v" | grep -c .) hits=$(printf '%s\n' "$v" | while read -r x; do printf '%s\n' "$a" | grep -F -- "$x" | grep -cE "(^|[^0-9.])${x//./\\.}([^0-9.]|$)"; done | awk '{s+=$1} END{print s+0}')" ;;
  AP-03)
    local f up=0 n=0
    for f in "${FILES[@]}"; do case $f in *.md) n=$((n + 1)); [ "$(barefence "$E/$f")" -gt "$( [ -f "$Bd/$f" ] && barefence "$Bd/$f" || echo 0)" ] && up=$((up + 1)) ;; esac; done
    (cd "$E" && python3 scripts/validate-plugin.py --check=code-fence >/dev/null 2>&1); echo "md=$n bare_up=$up v6_rc=$?" ;;
  AP-04)
    local f n=0 same=0 nm=0
    for f in "${FILES[@]}"; do case $f in */SKILL.md|*/agents/*.md) n=$((n + 1))
      fmb "$E/$f" | grep -q '^name: ' && nm=$((nm + 1))
      [ "$(fmb "$E/$f" | grep -v '^  Flutter 앱을 ')" = "$(fmb "$Bd/$f" | grep -v '^  Flutter 앱을 ')" ] && same=$((same + 1)) ;; esac; done
    echo "skill_agent=$n name=$nm fm_same_but_scenario_desc=$same scenario_desc_changed=$(diff <(fmb "$Bd/$FSR") <(fmb "$E/$FSR") | grep -c '^>')" ;;
  RE-02)
    echo "test_reads_doc=$(grep -cF 'visual-change-protocol.md' "$E/$DGT") copied_gate_lines=$(grep -cE '^(PATTERNS|viol|decisions) *=' "$E/$DGT") ci_jobs=$(python3 -c 'import sys,yaml; print(len(yaml.safe_load(open(sys.argv[1]))["jobs"]))' "$E/$CI")" ;;
  DG-02)
    # 편집기 경고 — 파일마다 규칙별 수를 시작 판과 비교 (새 파일은 0 과) · 셸 파일은 shellcheck 줄 수
    bash "$K/mdrules.sh" "$Bd" "$E" "${FILES[@]}"
    local f sa sb up=0 n=0
    command -v shellcheck >/dev/null || { echo "TOOL_MISSING shellcheck"; return 2; }
    for f in "${FILES[@]}"; do case $f in *.sh) n=$((n + 1))
      sb=0; [ -f "$Bd/$f" ] && sb=$(cd "$Bd" && shellcheck -f gcc "$f" | awk 'END{print NR}'); sa=$(cd "$E" && shellcheck -f gcc "$f" | awk 'END{print NR}')
      [ "$sa" -gt "$sb" ] && { up=$((up + 1)); echo "SC_UP $f $sb>$sa"; } ;; esac; done
    echo "sh_files=$n sh_up=$up" ;;
  DG-04)
    # CI 가 돌리는 킷 시험 전부를 끝 판 사본에서 (zsh 는 이 맥에 있다)
    local c r o=""
    c=$(cp1 "$E" dg4 .) || return 2
    # save-test.sh 는 뺀다 — 실제 ~/.harness/feedback 에 썼다 지우고, 이 계약은 그 스크립트가 재는 harness/scripts 를 건드리지 않는다
    for t in "bash react-kit/evals/scripts/project-detect-test.sh" "bash reflect-kit/evals/hooks/log-reflection-test.sh" "bash reflect-kit/evals/hooks/project-id-test.sh" \
             "bash reflect-kit/evals/hooks/collect-status-test.sh" "sh onboarding-kit/skills/setup-guide/evals/run-gate-evals.sh" "sh howto-kit/evals/run-evals.sh" \
             "python3 -m unittest discover -s flutter-toolkit/evals/scenario-report" "bash design-kit/evals/decision-gate-test.sh" "python3 scripts/test-collect-kaizen-data.py" \
             "bash harness/evals/hooks/commit-guard-test.sh" "bash flutter-toolkit/evals/hooks/format-edited-dart-test.sh"; do
      (cd "$c" && $t >/dev/null 2>&1); r=$?; o="$o $(printf '%s' "$t" | awk '{print $NF}' | sed 's#.*/##')=$r"
    done; echo "tests$o" ;;
  DG-05)
    local c k r o=""
    c=$(cp1 "$E" dg5 .) || return 2
    for k in harness flutter-toolkit design-kit backend-kit infra-kit rust-kit react-kit planning-kit reflect-kit bambu-kit onboarding-kit tone-kit api-kit howto-kit; do
      (cd "$c" && python3 scripts/validate-plugin.py "$k" >/dev/null 2>&1); r=$?; [ "$r" = 0 ] || o="$o $k=$r"
    done; echo "validate_fail:${o:- none}"
    o=""
    for k in "sync-docs.py --check-only" "sync-evals.py --check-only" "sync-orchestrator.py --check-only" "run-evals.py" "check-docs-links.py" "check-contrast-claims.py" "check-stale-values.py"; do
      (cd "$c" && python3 scripts/$k >/dev/null 2>&1); o="$o ${k%% *}=$?"
    done; echo "checks$o" ;;
  DG-06)
    # 두 줄이 모두 있고 둘 다 PASS 여야 한다 — 줄이 없거나 SKIP 이면 pass 가 2 에 못 미친다
    python3 scripts/validate-post-kaizen.py --since "$B" 2>&1 | grep -E 'scope-isolation|doc-contracts' | awk '{print} /^\[ PASS/{p++} END{print "dg06 lines=" NR " pass=" p+0}' ;;
  *) echo "UNKNOWN $1"; return 2 ;;
  esac
}
```

```bash
#!/usr/bin/env bash
# l10n.sh — 사용: l10n.sh <SKILL.md> <case: empty|filled> <shell: bash|zsh>
# SKILL.md 의 「3. 지워진 키 수와」 아래 첫 bash 블록을 떼어 임시 저장소에서 돌린다
set -u
SK=$1; CASE=$2; SH=$3
T=$(mktemp -d); trap 'rm -rf "$T"' EXIT
awk '/^3\. 지워진 키 수와/{f=1} f&&/^ *```bash/{b=1;next} b&&/^ *```/{exit} b{sub(/^   /,"");print}' "$SK" > "$T/blk.sh"
[ -s "$T/blk.sh" ] || { echo "NO_BLOCK"; exit 2; }
cd "$T" && git init -q r && cd r && mkdir -p src/infrastructure/i18n/locales
P=src/infrastructure/i18n/locales/ko.po
printf 'msgid "a"\nmsgstr ""\n\nmsgid "b"\nmsgstr "비"\n\nmsgid "c"\nmsgstr "씨"\n' > $P
git add . && git -c user.email=x@x -c user.name=x commit -qm init
if [ "$CASE" = empty ]; then
  printf 'msgid "b"\nmsgstr "비"\n\nmsgid "c"\nmsgstr "씨"\n' > $P
else
  printf 'msgid "a"\nmsgstr ""\n\nmsgid "c"\nmsgstr "씨"\n' > $P
fi
out=$($SH "$T/blk.sh" 2>&1); rc=$?
echo "$out" | tr '\n' '|'; echo " rc=$rc"
```

```bash
#!/usr/bin/env bash
# reflect_e2e.sh <판 폴더> — 가짜 codex 가 「no issues」 를 내는 실행 하나를 실제 훅으로 돌린 뒤 collect_status 경고를 센다
# 폴더: 5 일 전 기록 1 · 4 일 전 실패 한 쌍. (1) 훅 실행 전 경고 (2) no issues 실행 뒤 경고 (3) 그 뒤 실패 한 쌍을 더한 뒤 경고
set -u
V=$1; W=$(mktemp -d "${TMPDIR:-/tmp}/re2e.XXXXXX") || exit 2; trap 'rm -rf "$W"' EXIT
command -v jq >/dev/null || { echo "TOOL_MISSING jq"; exit 2; }
mkdir -p "$W/bin" "$W/tmp" "$W/proj" "$W/home/.claude/logs/proj"
cat > "$W/bin/codex" <<'EOF'
#!/usr/bin/env bash
out=""; prev=""; for a in "$@"; do [ "$prev" = "--output-last-message" ] && out=$a; prev=$a; done
cat > /dev/null; printf 'no issues\n' > "$out"; exit 0
EOF
chmod +x "$W/bin/codex"
at() { local e=$(( $(date +%s) - $1 )); date -r "$e" "$2" 2>/dev/null || date -d "@$e" "$2"; }
B=$W/home/.claude/logs/proj
# shellcheck disable=SC2016
printf '\n## %s\n\n- session: `R1`\n\n```yaml\nprimary_category: tool_failure\n```\n' "$(at 432000 '+%Y-%m-%dT%H:%M:%S%z')" > "$B/reflections-$(date '+%Y-%m').md"
D4=$(at 345600 '+%Y-%m-%dT%H:%M:%S%z')
printf '%s [log-reflection] fail:codex-exit-1 session=F1\n%s [log-reflection] fallback:claude-exit-1 session=F1\n' "$D4" "$D4" > "$B/.errors.log"
cs() { bash -c '. "$1" 2>/dev/null; collect_status 7 "$2"' _ "$V/reflect-kit/hooks/_lib-project-id.sh" "$B" | grep -c '^⚠ 수집 멈춤'; }
w0=$(cs)
T=$W/t.jsonl; for i in $(seq 1 12); do printf '{"type":"user","message":{"content":"line %s"}}\n' "$i"; done > "$T"
jq -cn --arg t "$T" --arg c "$W/proj" '{session_id: "N1", transcript_path: $t, cwd: $c}' > "$W/in.json"
env HOME="$W/home" TMPDIR="$W/tmp" PATH="$W/bin:$PATH" bash "$V/reflect-kit/hooks/log-reflection.sh" --background "$W/in.json" >/dev/null 2>&1
recs=$(grep -c '^- session: `N1`' "$B"/reflections-*.md | awk -F: '{s+=$NF} END{print s+0}')
w1=$(cs)
sleep 1
D0=$(date '+%Y-%m-%dT%H:%M:%S%z')
printf '%s [log-reflection] fail:codex-exit-1 session=F2\n%s [log-reflection] fallback:claude-exit-1 session=F2\n' "$D0" "$D0" >> "$B/.errors.log"
w2=$(cs)
echo "reflect_e2e before=$w0 after_noissues=$w1 after_new_fail=$w2 noissues_record=$recs"
```

```bash
#!/usr/bin/env bash
# api_serve.sh <판 폴더> — api-ui 「1. 여는 방법」 항목 안의 bash 블록을 떼어 bash · zsh 로 돌리고, 찍힌 번호가 포트를 쥔 파이썬인지 본다
set -u
V=$1; W=$(mktemp -d "${TMPDIR:-/tmp}/aserve.XXXXXX") || exit 2; W=$(cd "$W" && pwd -P); trap 'rm -rf "$W"' EXIT
awk '/^1\. \*\*여는 방법\*\*/{f=1;next} f&&/^2\. \*\*콘솔 오류\*\*/{exit} f&&/^ *```bash/{b=1;next} b&&/^ *```/{b=0;done=1;next} b&&!done{sub(/^   /,"");print}' \
  "$V/api-kit/skills/api-ui/SKILL.md" > "$W/blk.sh"
[ -s "$W/blk.sh" ] || { echo "api_serve NO_BLOCK"; exit 0; }
PORT=$(python3 -c 'import socket; s=socket.socket(); s.bind(("127.0.0.1",0)); print(s.getsockname()[1]); s.close()')
sed "s/8765/$PORT/g" "$W/blk.sh" > "$W/run.sh"
out=""
for sh in bash zsh; do
  mkdir -p "$W/$sh/.api" && printf '<html></html>\n' > "$W/$sh/.api/ui.html"
  # 파일로 받는다 — 파이프로 받으면 뒤에서 도는 서버가 출력을 쥐어 명령 치환이 끝나지 않는다. 셸이 묶이면 6 초 알람(142)
  rc=$( { (cd "$W/$sh" && exec perl -e 'alarm 6; exec @ARGV' $sh "$W/run.sh" > "$W/$sh.out" 2>&1); echo $?; } 2>/dev/null )
  line=$(grep -E '^(SERVING|NOT_SERVING)' "$W/$sh.out" | head -1)
  pid=$(printf '%s\n' "$line" | sed -nE 's/^SERVING pid=([0-9]+) dir=.*/\1/p')
  dir=$(printf '%s\n' "$line" | sed -nE 's/^SERVING pid=[0-9]+ dir=(.*)$/\1/p')
  lp=$(lsof -nP -iTCP:"$PORT" -sTCP:LISTEN -t 2>/dev/null | head -1)
  is=0; [ -n "$pid" ] && [ "$pid" = "$lp" ] && is=1
  dok=0; [ -n "$dir" ] && [ "$(ls "$dir" 2>/dev/null)" = ui.html ] && dok=1
  [ -n "$pid" ] && kill "$pid" 2>/dev/null
  sleep 1
  rel=0; [ -z "$(lsof -nP -iTCP:"$PORT" -sTCP:LISTEN -t 2>/dev/null)" ] && rel=1
  pkill -f "http.server $PORT" 2>/dev/null   # 시험이 남긴 서버는 끈다 — 이 포트 번호로만 고른다
  [ -n "$dir" ] && case $dir in "${TMPDIR:-/tmp}"*|/var/folders/*|/private/var/*|/tmp/*) rm -rf "$dir" ;; esac
  out="$out $sh:rc=$rc,pid_is_server=$is,dir_ok=$dok,released=$rel"
done
echo "api_serve$out"
```

```bash
#!/usr/bin/env bash
# mdrules.sh <옛 판 폴더> <새 판 폴더> <파일…> — 파일마다 규칙별 편집기 경고 수를 두 판에서 세어 는 규칙을 찍는다
# 편집기 확장과 같은 조건(markdownlint-cli2 0.23.2 · MD013 끔). 옛 판에 없는 새 파일은 0 과 비교한다
set -u
HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
ML=$HERE/node_modules/.bin/markdownlint-cli2; CFG=$HERE/cfg.markdownlint-cli2.jsonc
[ -x "$ML" ] || { echo "TOOL_MISSING markdownlint-cli2"; exit 2; }
O=$1; N=$2; shift 2
rules() { [ -f "$1/$2" ] || return 0; (cd "$1" && "$ML" --config "$CFG" "$2" 2>&1) | sed -nE 's/^[^ ]+:[0-9]+(:[0-9]+)? (error )?(MD[0-9]+)\/.*/\3/p' | sort | uniq -c | awk '{print $2, $1}'; }
up=0; n=0
for f in "$@"; do
  case $f in *.md) ;; *) continue ;; esac
  n=$((n + 1))
  line=$(join -a1 -a2 -e0 -o 0,1.2,2.2 <(rules "$O" "$f" | sort) <(rules "$N" "$f" | sort) | awk '$3 > $2 {printf " %s:%d>%d", $1, $2, $3}')
  [ -n "$line" ] && { echo "UP $f$line"; up=$((up + 1)); }
done
echo "md_files=$n files_up=$up"
```

```python
"""cov2.py <옛 판 폴더> <새 판 폴더> <원본> <페이지> — coverage.py 와 같은 셈을 두 판 폴더로 한다.
원본의 백틱 표시(codes) 가운데 옛 페이지에 있던 것이 새 페이지에서 빠진 수(lost)와, 원본 낱말이 페이지 글에 든 비율(wr 옛→새)을 찍는다.
원본은 새 판 것을 쓴다."""
import html, os, re, sys
old_root, new_root, src, page = sys.argv[1:5]


def text(h):
    h = re.sub(r'(?is)<(script|style)[^>]*>.*?</\1>', ' ', h)
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', h)))


s = open(os.path.join(new_root, src), encoding='utf-8').read()
new = text(open(os.path.join(new_root, page), encoding='utf-8').read())
old = text(open(os.path.join(old_root, page), encoding='utf-8').read())
codes = sorted({c.strip() for c in re.findall(r'`([^`\n]+)`', s) if c.strip()})
cn = [c for c in codes if re.sub(r'\s+', ' ', c) in new]
co = [c for c in codes if re.sub(r'\s+', ' ', c) in old]
lost = [c for c in co if c not in cn]
words = {w for w in re.findall(r'[0-9A-Za-z가-힣_.-]{2,}', re.sub(r'`[^`]*`', ' ', s))}
wr = lambda t: sum(1 for w in words if w in t) / max(1, len(words))
print(f'cov {page} new={len(cn)} old={len(co)} lost={len(lost)} wr={wr(old):.2f}->{wr(new):.2f} {lost[:4]}')
```

```python
"""blockcmp.py <판 폴더> <원본> <페이지> <블록 표지> — 원본의 코드 펜스 가운데 표지 글이 든 것과 페이지의 <pre> 가운데 표지 글이 든 것을
줄 단위로 대조한다. 원본 줄(앞뒤 공백 · 빈 줄 제외) 가운데 페이지 블록에 없는 줄 수를 찍는다. 블록을 못 찾으면 missing=NA."""
import html, os, re, sys
root, src, page, mark = sys.argv[1:5]
s = open(os.path.join(root, src), encoding='utf-8').read()
blocks = re.findall(r'(?ms)^[ \t]*```[a-z]*\n(.*?)^[ \t]*```', s)
sb = next((b for b in blocks if mark in b), None)
p = open(os.path.join(root, page), encoding='utf-8').read()
pres = [html.unescape(re.sub(r'<[^>]+>', '', m)) for m in re.findall(r'(?s)<pre[^>]*>(.*?)</pre>', p)]
pb = next((b for b in pres if mark in b), None)
if sb is None or pb is None:
    print(f'blockcmp {page} missing=NA src_block={sb is not None} page_block={pb is not None}')
    sys.exit(0)
norm = lambda t: {l.strip() for l in t.splitlines() if l.strip()}
miss = sorted(norm(sb) - norm(pb))
print(f'blockcmp {page} src_lines={len(norm(sb))} missing={len(miss)} {miss[:3]}')
```

### 봉인 전 실측

2026-09-26 02:20 ~ 02:45 에 재고, 계약 초안 검토를 반영한 뒤 03:13 ~ 03:21 에 예행 저장소를 다시 만들어 조건 서른의 예행 판 값 · 바뀐 조건의 시작 판 값 · 변형 스물 · 삭제 대조 열일곱 · 음성 대조 넷을
다시 잰 값이다. 「예행 1 차 판」 이라 적은 양성 대조 두 줄만 검토 전 값이다(그때의 중간 판을 다시 만들지 않았다). 끝 판은 예행 저장소(`rrepo/` — 시작 커밋에 `mock.py` 편집을 묶음마다 서명 커밋으로 싣고 notes · `end_sha` 까지 흉내 낸 판)이고,
시작 판은 같은 저장소에서 `END_OVERRIDE=6a8be196d9c40a1686f51f9a6bd50039c2bd5b71` 로 잰 값이다. 조건 문장의 기대값은 아래 「예행 판」 출력에서 옮겼다.

#### 지적 재현 (시작 판)

```text
A1  check-stale-values — backend-kit/skills/backend-test/SKILL.md 끝에 'OpenAPI 3.1.1 최신' 을 넣고 돌림
    지금 판   : 검사 제외: backend-kit … / 되살아난 옛 값 없음 · 종료 코드 0
    제외만 비운 판: 되살아난 옛 값 1 건: backend-kit/skills/backend-test/SKILL.md:269 '3.1.1' -> '3.2.0' · 종료 코드 1
    제외만 비운 판(넣지 않음): 검사 범위: 소스 디렉토리 26/26 · 파일 401 개 · 되살아난 옛 값 없음 · 종료 코드 0
A3  react-l10n 블록 — 빈 번역 키 하나만 지운 저장소: bash 출력 1 · 종료 코드 1 / zsh 출력 1 · 종료 코드 1
A4  결정 전파 검사 — exstr · decstr · toplist · reqstr 넷이 Traceback 과 종료 코드 1 · assertstr(`assertions: "main visible"`)은 멈추지 않고 종료 코드 1 (gate ok=5/10 traceback=4)
A7  reflect_e2e before=1 after_noissues=1 after_new_fail=1 noissues_record=0   (no issues 실행 뒤에도 경고)
A8  「&&」 로 이은 명령(비어 있는 포트)
    bash: SERVING pid=3142 dir=        · 포트를 쥔 번호 3146   (번호가 하위 셸 · 폴더 빈칸)
    zsh : SERVING pid=3236 dir=/var/folders/…/tmp.2L1f4VhcwY · 포트를 쥔 번호 3236
B1  봉인 범위 블록 — contract_digest · sha256_16 을 지운 셸: bash · zsh 모두 rc=0,stop=0,broken=1 (봉인된 계약이 SEAL_BROKEN 인 채 종료 코드 0)
B5  F2 표 원본 가운데 detect-docs-drift 매핑에 없는 것: ['docs/onboarding-kit/examples/', 'api-kit/references/']
B9  bash -c "grep -c '.unwrap()' src/" → grep: src/: Is a directory · 종료 코드 2
    (이 맥 zsh 의 grep 은 ugrep 함수라 같은 명령이 파일마다 수를 찍는다 — src/n.txt:1 · src/b.rs:0. 측정은 bash 의 /usr/bin/grep 으로만)
B10 SKILL.md 에서 misplaced 판정 두 줄을 지운 사본의 러너: EVALS declared=6 ran=6 fail=0 · EVALS_PASS (지키는 시험이 없다)
B11 mw stale_title=1 fail_line=0 left=2   (받기가 전부 실패해도 옛 모델 제목을 보고)
r4 1 회차 9 · 2 회차 R2-2  status: nonsense · required surface 1 · excluded 없음 → decisions=1 surfaces=1 violations=0 schema_errors=0 · 종료 코드 0 (재현됨 — 처리표 36 행)
r4 2 회차 N4  합치기 전 760a75f 판: 검사 범위: 소스 디렉토리 25/25 · 파일 389 개 · 등록값 18 개 / 합친 6a8be19 판: 파일 391 개 (changelog 의 389 는 그때 값 — 처리표 40 행)
r4 2 회차 R2-5  infra-test 「# 규칙 1: checkout 스텝 존재」 블록을 시작 커밋에서 그대로 떼어 bash 로 — checkout 없이 `run: |` 블록 안 줄 `uses: actions/checkout@v4` 만 둔 워크플로
                → PASS : a.yml checkout 존재 · violation=0 / 흐름 표기 `- {uses: actions/checkout@v4}` 진짜 checkout → VIOLATION : b.yml checkout 스텝 없음 · violation=1 (재현됨 — 처리표 26 행)
r4 2 회차 N2  오케스트레이터 :25 「각 Phase 서브에이전트는 이 템플릿에 명시된 최소 3 건 이상을 조회」 와 같은 줄 「(Phase 17 표는 아직 없다)」 · phase-research-templates.md 의 ^## Phase 열여섯
                · howto-research/SKILL.md Step 1 「카테고리 | 문서 | 1차 출처」 표 여섯 행 · docs/howto/changelog-feeds.md 주소 30 · deep-links.md 17 (처리표 39 행)
r4 2 회차 R1-2  `silent-check` 가 든 파일 = assertions.json · expected-improvements.md 둘 · scripts/run-evals.py → Total: 116 passed, 0 failed (그 픽스처를 읽는 실행기 없음 — 처리표 38 행)
```

#### 조건별 — 시작 판 → 예행 판

```text
SK-01  시작  design_cmd=0 react_cmd=0 old=3 / i02 backend-kaizen=1/3 design-kaizen=1/3 infra-kaizen=1/3 rust-kaizen=0/3
       예행  design_cmd=1 react_cmd=1 old=0 / i02 backend-kaizen=3/3 design-kaizen=3/3 infra-kaizen=3/3 rust-kaizen=3/3
SK-02  시작  planning=10/12 reflect=3/4 tone_docs=8/11 / f2_rows=15 uncovered=2 api_ref=1 docs_site_rows=7 same=0 / phase_dep_line=0 p17_src=0
       예행  planning=12/12 reflect=4/4 tone_docs=11/11 / f2_rows=15 uncovered=0 api_ref=0 docs_site_rows=15 same=1 [] / phase_dep_line=1 p17_src=1
SK-03  시작  test: v0=2 row=0 c2=0 c3=0 | audit: c2=0 c3=0 | reviewer: c2=0 c3=0
       예행  test: v0=0 row=1 c2=1 c3=1 | audit: c2=1 c3=1 | reviewer: c2=1 c3=1
SK-04  시작  fitpal=6 names_skill=2 names_format=3 / unittest rc=0 Ran 24 tests / preflight new=0 old=1 / readme intro=19/20 tree=19/20 list=19/20 has_sr=0
       예행  fitpal=0 names_skill=0 names_format=0 / unittest rc=0 Ran 24 tests / preflight new=1 old=0 / readme intro=20/20 tree=20/20 list=20/20 has_sr=1
SK-05  시작  l10n empty/bash=[1| rc=1] empty/zsh=[1| rc=1] filled/bash=[1|-msgstr "비"| rc=0] filled/zsh=[1|-msgstr "비"| rc=0] / sentence=0 grep_second=1
       예행  l10n empty/bash=[1|filled_deleted=0| rc=0] empty/zsh=[1|filled_deleted=0| rc=0] filled/bash=[1|-msgstr "비"|filled_deleted=1| rc=0] filled/zsh=[1|-msgstr "비"|filled_deleted=1| rc=0] / sentence=1 grep_second=0
SK-06  시작  g16 ref=0 old=1 run2_first4=1 / cmd two_hits=[grep: src/: Is a directory] rc=2 zero=[grep: src/: Is a directory] rc=2 no_src_note=0
       예행  g16 ref=1 old=0 run2_first4=1 / cmd two_hits=[2] rc=0 zero=[0] rc=0 no_src_note=1
SK-07  시작  api_serve NO_BLOCK / no_amp=0 both_shells=0
       예행  api_serve bash:rc=0,pid_is_server=1,dir_ok=1,released=1 zsh:rc=0,pid_is_server=1,dir_ok=1,released=1 / no_amp=1 both_shells=1
SK-08  시작  mw stale_title=1 fail_line=0 left=2
       예행  mw stale_title=0 fail_line=1 left=0
SC-00  예행  SC-00=0 RE-01=design-kit/evals/decision-gate-test.sh onboarding-kit/skills/setup-guide/evals/fixtures/gate-fail-ledger-misplaced.md  DG-01=0
ER-01  시작  inject=0 rc=0 scope=25/25 excluded_line=1 hit=0 / inject=1 rc=0 scope=25/25 excluded_line=1 hit=0
       예행  inject=0 rc=0 scope=26/26 excluded_line=0 hit=0 / inject=1 rc=1 scope=26/26 excluded_line=0 hit=1
ER-02  시작  gate ok=5/10 traceback=4 wrong: exstr=1 decstr=1 toplist=1 reqstr=1 assertstr=1 / kit_test rc=127 (파일 없음)
       예행  gate ok=10/10 traceback=0 / kit_test rc=0 결과: 10 경우 중 불일치 0 start_doc rc=1 결과: 10 경우 중 불일치 5 exec=100755
ER-03  시작  missing bash:rc=0,stop=0,ok=0,broken=1 zsh:rc=0,stop=0,ok=0,broken=1 | full bash:rc=0,stop=0,ok=1,broken=0 zsh:rc=0,stop=0,ok=1,broken=0
       예행  missing bash:rc=2,stop=1,ok=0,broken=0 zsh:rc=2,stop=1,ok=0,broken=0 | full bash:rc=0,stop=0,ok=1,broken=0 zsh:rc=0,stop=0,ok=1,broken=0
ER-04  시작  reflect_e2e before=1 after_noissues=1 after_new_fail=1 noissues_record=0 / tags code=14 has_ok=0 schema_missing=0 design_missing=0 digest_g13=0 digest_in=0
       예행  reflect_e2e before=1 after_noissues=0 after_new_fail=1 noissues_record=0
             tests collect rc=0 [결과: 13 경우 중 불일치 0] log rc=0 [결과: 26 경우 중 불일치 0] | start_lib rc=1 start_hook rc=1
             tags code=15 has_ok=1 schema_missing=0 design_missing=0 digest_g13=1 digest_in=1
ER-05  시작  runner rc=0 EVALS declared=6 ran=6 fail=0 EVALS_PASS case=0 / no_misplaced_check rc=0 EVALS_PASS
       예행  runner rc=0 EVALS declared=7 ran=7 fail=0 EVALS_PASS case=1 / no_misplaced_check rc=1 EVALS_FAIL
ER-06  시작  ci jobs=3 validate_has=0/2 / actionlint=0 / run scenario=0 decision_gate=127
       예행  ci jobs=3 validate_has=2/2 / actionlint=0 / run scenario=0 decision_gate=0
ER-07  예행  added=205 k02=0 names=0
ER-08  예행  notes_committed=1 / 1 1 1 1 / commit_rows=13/13 / 1 ×19 / audit added=1 added_ptr=1 deleted=0 shared_commits=0
AR-01  예행  0 / 0 46 / mixed=0 one_kit=13 / 0 / SEAL_OK / scope_same=1 harness_line=1
AR-02  시작  schema=0/1 bambu=0 vcp_missing=0 design_test=1/0/0 reflect=0/0 api=0/1 / 짝 여덟 lost=0 wr_ok (시작 판끼리라 wr 은 같다)
       예행  schema=1/0 bambu=1 vcp_missing=0 design_test=0/1/1 reflect=1/1 api=1/0 / 짝 여덟 lost=0 wr_ok
             (cov2 원값 wr 옛→새: 0.95→0.95 · 0.92→0.92 · 0.97→0.97 · 0.73→0.73 · 0.80→0.80 · 0.90→0.91 · 0.92→0.92 · api-ui 짝 0.40→0.41 — 검토가 잰 값과 같다)
AP-01  예행  versions=11 hits=0
AP-03  예행  md=27 bare_up=0 v6_rc=0
AP-04  시작  skill_agent=18 name=18 fm_same_but_scenario_desc=18 scenario_desc_changed=0
       예행  skill_agent=18 name=18 fm_same_but_scenario_desc=18 scenario_desc_changed=1
RE-02  예행  test_reads_doc=2 copied_gate_lines=0 ci_jobs=3
DG-02  예행  md_files=27 files_up=0 / sh_files=5 sh_up=0
DG-04  예행  tests project-detect-test.sh=0 log-reflection-test.sh=0 project-id-test.sh=0 collect-status-test.sh=0 run-gate-evals.sh=0 run-evals.sh=0 scenario-report=0 decision-gate-test.sh=0 test-collect-kaizen-data.py=0 commit-guard-test.sh=0 format-edited-dart-test.sh=0
DG-05  예행  validate_fail: none / checks sync-docs.py=0 sync-evals.py=0 sync-orchestrator.py=0 run-evals.py=0 check-docs-links.py=0 check-contrast-claims.py=0 check-stale-values.py=0
DG-06  시작  [ PASS  ] scope-isolation (0 commits · 13 kits) · [ PASS  ] doc-contracts → dg06 lines=2 pass=2 (작업 폴더 HEAD = 시작 커밋 — 시작 판은 결함 재현 대상이 아니라 양성 대조는 아래 변형 둘)
       예행  [ PASS  ] scope-isolation (16 commits · 13 kits) · [ PASS  ] doc-contracts → dg06 lines=2 pass=2
```

#### 예행 변형 · 삭제 대조 · 음성 대조

```text
변형 unsigned    (서명 없는 커밋이 react-l10n 을 고침)            AR-01 → 1 / 0 46 / mixed=0 one_kit=13 / 0 / SEAL_OK / scope_same=1 harness_line=1
변형 outside     (서명 커밋이 infra-kit/README.md 를 고침)         AR-01 → 0 / 1 46 / …
변형 mixed       (서명 커밋 하나가 react-kit · rust-kit 을 함께)    AR-01 → 0 / 0 46 / mixed=1 one_kit=13 / …
변형 seal-broken (서명 커밋이 SK-08 조건 줄을 바꿈)               AR-01 → … / 1 / SEAL_BROKEN / …
변형 no-notes    (notes 를 지운 커밋)                           ER-08 → notes_committed=0
변형 shared      (서명 커밋이 루트 CLAUDE.md 를 고침)              ER-08 → … shared_commits=1 · SC-00 → SC-00=0
변형 release     (서명 커밋이 marketplace.json 을 고침)            SC-00 → SC-00=1
변형 bad-text    (README 에 「이 값에 대해 fit-pal 앱 0.9.1」)       ER-07 → added=207 k02=1 names=1 · AP-01 → versions=11 hits=1
변형 step5-keep  (design-kaizen Step 5 옛 줄만 되살림)             SK-01 → design_cmd=1 react_cmd=1 old=1   (검토 전 정규식이면 old=0 으로 통과 — 검토가 잰 값)
변형 audit2      (감사 기록에 줄 둘을 더 더함)                      ER-08 → audit added=3 added_ptr=1 deleted=0 shared_commits=0
변형 dg06-fail   (한 커밋이 harness/skills/ 와 react-kit/skills/ 를 함께) DG-06 → [ FAIL  ] ✗ scope-isolation: 1 cross-phase commits · dg06 lines=2 pass=1
변형 dg06-skip   (오케스트레이터 `# docs-contract` → `# docs-contract-off`) DG-06 → [ SKIP  ] · doc-contracts: docs-contract 선언 블록 없음 · dg06 lines=2 pass=1
변형 bare-fence  (rust-audit 끝에 힌트 없는 펜스)                   AP-03 → md=27 bare_up=1 v6_rc=2
변형 sh-unquoted (새 시험 끝에 echo $W)                            DG-02 → SC_UP design-kit/evals/decision-gate-test.sh 0>1 · sh_files=5 sh_up=1
변형 copied-gate (새 시험 끝 빈 heredoc 에 decisions = … 한 줄)       RE-02 → test_reads_doc=2 copied_gate_lines=1 ci_jobs=3
변형 page-loss   (reflect design 쪽에서 <code> 셋 이상 든 목록 하나를 지움) AR-02 → docs/reflect-kit/design.html lost=1 wr_ok (나머지 일곱 짝 lost=0 wr_ok)
변형 page-prose  (같은 쪽에서 <code> 없는 문단 열아홉만 지움)          AR-02 → docs/reflect-kit/design.html lost=0 wr_down   (cov2 원값 wr 0.90→0.84 · lost 만 보던 검토 전 측정은 통과)
변형 no-src-note (rust-audit 새 문장만 지움)                        SK-06 → … no_src_note=0
변형 no-digest-in (reflect-digest 입력 줄의 새 글만 지움)            ER-04 → … digest_g13=1 digest_in=0
변형 no-p17      (오케스트레이터 :25 괄호의 새 글만 지움)                SK-02 → phase_dep_line=1 p17_src=0
삭제 design-kaizen 「Kaizen-Phase: <슬러그>」 줄   SK-01 → design_cmd=0
삭제 react-kaizen 같은 줄                          SK-01 → react_cmd=0
삭제 rust-kaizen I-02 줄                           SK-01 → rust-kaizen=0/3
삭제 tone-kaizen docs/tone 줄                      SK-02 → tone_docs=X/11
삭제 오케스트레이터 범위 합치기 줄                    SK-02 → phase_dep_line=0
삭제 design-audit 「종료 코드 2」 줄                  SK-03 → audit: c2=0 c3=0
삭제 design-reviewer 「종료 코드 3」 줄               SK-03 → reviewer: c2=0 c3=0
삭제 design-test 결정 전파 표 행                      SK-03 → test: … row=0
삭제 flutter-preflight 새 codegen 줄                SK-04 → preflight new=0 old=0
삭제 README 소개 줄                                 SK-04 → readme intro=/20
삭제 react-l10n 「filled_deleted=0` 이 아니면」 줄    SK-05 → sentence=0
삭제 rust-audit Gotcha 16 줄                        SK-06 → g16 ref=0
삭제 api-ui 여는 방법 줄                             SK-07 → api_serve NO_BLOCK · no_amp=0 both_shells=0
삭제 reflect-digest Gotcha 13 줄                    ER-04 → digest_g13=0
삭제 api 뷰어 쪽 새 문장                             AR-02 → api=0/0 · api-ui 짝 lost=0 wr_down
삭제 reflect schema 쪽 태그 줄                       AR-02 → reflect=0/1
삭제 reflect SCHEMA.md 의 ok:no-issues 태그 줄          ER-04 → tags … schema_missing=1   (검토가 잰 대조를 다시 잼)
음성 ER-02  시작 판 문서로 킷 시험                    start_doc rc=1 (불일치 5)
음성 ER-04  시작 판 라이브러리 · 훅으로 킷 시험           start_lib rc=1 · start_hook rc=1 (새 경우 각 1 불일치)
음성 ER-05  misplaced 판정 두 줄을 지운 끝 판 사본        rc=1 EVALS_FAIL
음성 SK-04 (c) 예시 기록 TC-002 의 서버 이름만 바꾸고 보고서를 안 다시 만든 사본  FAIL: test_example_report_is_current · Ran 24 tests · rc=1
양성 AR-02 (c) 원본 검사 코드만 고치고 페이지는 두 줄만 맞춘 예행 1 차 판  blockcmp missing=11
양성 DG-02  새 픽스처 주소를 <…> 없이 둔 예행 1 차 판      UP onboarding-kit/skills/setup-guide/evals/fixtures/gate-fail-ledger-misplaced.md MD034:0>2
```

예행 도중 고친 측정 셋: (1) SK-04 preflight 옛 줄은 성공 틀(`:125`)에도 있어 실패 틀(「하나라도 실패하면」 부터 「Fix the issues above」 앞까지)로 좁혔다
(2) README 트리 줄은 킷마다 있어 `├── flutter-toolkit/` 다음 `skills/` 줄로 좁혔다 (3) rust-run §2 첫 항목은 두 줄이라 이어진 줄까지 읽는다.
DG-02 셸 비교는 `grep -c` 가 0 건에 종료 코드 1 을 내 `|| echo 0` 과 겹쳐 값이 두 줄이 되던 것을 `awk 'END{print NR}'` 로 바꿨다.

## Skill

- [ ] SK-01: 카이젠 스킬 넷의 커밋 규칙과 I-02 예외 목록이 오케스트레이터 · qa-evaluator 규약과 맞는다 — (a) `design-kaizen` · `react-kaizen` 각각에 Phase 커밋 명령이 경로 지정 커밋 `git commit -o <내 경로>` 와 서명 줄 `Kaizen-Phase: <슬러그>` 를 한 줄에 함께 담은 줄이 1 이고, `.claude/skills/*/SKILL.md` 전체에서 옛 문장(「git add/commit/tag 를 직접 실행하지 마라」 · 「커밋은 오케스트레이터가」 · 「커밋은 오케스트레이터에」 · 「Phase 로 호출한 경우 이 Step 을 실행하지 마라」)이 든 줄 0 (b) `backend-kaizen` · `design-kaizen` · `infra-kaizen` · `rust-kaizen` 넷의 `**I-02 예외 목록 명시화**` 줄이 `.harness/sprint-contract-<slug>.md` · `.harness/sprint-feedback-<slug>.md` · `.harness/sprint-amendments-<slug>.md` 셋을 모두 담는다. 양성 대조: 시작 판 `design_cmd=0 react_cmd=0 old=3` · `backend-kaizen=1/3 design-kaizen=1/3 infra-kaizen=1/3 rust-kaizen=0/3` · 예행 변형 `step5-keep`(design-kaizen Step 5 옛 줄만 되살림) → `design_cmd=1 react_cmd=1 old=1` (측정: `type m >/dev/null || exit 2;` 뒤 `m SK-01` 두 줄이 `design_cmd=1 react_cmd=1 old=0` · `i02 backend-kaizen=3/3 design-kaizen=3/3 infra-kaizen=3/3 rust-kaizen=3/3`) [exact, enumerated]
- [ ] SK-02: 오케스트레이터 · docs-site · tone-kaizen 의 수 · 표 · 출처 안내가 실제와 맞는다 — (a) Final 조건 줄(「Phase 1에서 업데이트된 설계 원칙이 Phase 2~17 변경에 반영되었는가」)의 `planning-kit N 스킬` · `reflect-kit N 스킬` 이 끝 판 실제 스킬 수와 같다 (b) tone-kaizen 의 `- \`docs/tone/*.md\` N종` 이 끝 판 `docs/tone/*.md` 파일 수와 같다 (c) F2 매핑 표의 원본 경로가 모두 끝 판 `scripts/detect-docs-drift.py` 의 접두 매핑이나 개별 파일 키에 들고, api-kit 행에 `api-kit/references/` 가 없다 (d) docs-site `## Step 1` 표의 행이 F2 표 행과 글자 그대로 같은 열다섯 행이다 (e) AUTO 영역 밖에 `references/phase-dependencies.md` · 「합친」 · `` `hooks/` `` 를 한 줄에 담은 줄이 1 (f) 오케스트레이터에서 「Phase 17 표는 아직 없다」 가 든 줄 가운데 `howto-research/SKILL.md` 와 `Step 1` 을 함께 담은 줄이 1. 양성 대조: 시작 판 `planning=10/12 reflect=3/4 tone_docs=8/11` · `f2_rows=15 uncovered=2 api_ref=1 docs_site_rows=7 same=0` · `phase_dep_line=0 p17_src=0` · 예행 변형 `no-p17`(괄호의 새 글만 지움) → `p17_src=0` (측정: `type m >/dev/null || exit 2;` 뒤 `m SK-02` 세 줄이 `planning=12/12 reflect=4/4 tone_docs=11/11` · `f2_rows=15 uncovered=0 api_ref=0 docs_site_rows=15 same=1` 로 시작 · `phase_dep_line=1 p17_src=1`) [exact, enumerated]
- [ ] SK-03: design-kit 결정 전파 검사를 쓰는 세 자리가 종료 코드 2 · 3 을 다룬다 — `design-test` 에 「위반 0」 이 든 줄 0 · Step 7 표의 `| 결정 전파 |` 행이 `종료 코드 0` 을 담고, `design-test` · `design-audit` 의 `## Step 5` 절 · `design-reviewer` 셋 각각에 `종료 코드 2` 와 `SCHEMA_ERROR` 를 한 줄에 담은 줄(design-audit · design-reviewer 는 그 줄에 `REJECT` 도)과 `종료 코드 3` · `NO_SURFACE` · `NO_DECISION` 을 한 줄에 담은 줄이 각 1 이상. 양성 대조: 시작 판 `test: v0=2 row=0 c2=0 c3=0 | audit: c2=0 c3=0 | reviewer: c2=0 c3=0` (측정: `type m >/dev/null || exit 2;` 뒤 `m SK-03` 이 `test: v0=0 row=1 c2=<1 이상> c3=<1 이상> | audit: c2=<1 이상> c3=<1 이상> | reviewer: c2=<1 이상> c3=<1 이상>`) [exact, enumerated]
- [ ] SK-04: flutter-toolkit 과 루트 README 가 이 가지 규칙(킷 파일에 특정 앱 · 화면 조종 도구 이름을 적지 않는다)과 실제 스킬 수에 맞는다 — (a) 끝 판 `flutter-toolkit/` 전체에서 `fit-?pal` · `fit_pal`(대소문자 무시)이 든 줄 0 (b) `flutter-scenario-report` 의 SKILL.md 와 `references/record-format.md` 각각에 `find_widget` · `verify_visible` · `tap_native_point` · `tap_widget` · `Flutter Playwright` 가 든 줄 0 (c) 끝 판 사본에서 `python3 -m unittest discover -s flutter-toolkit/evals/scenario-report` 종료 코드 0 · 시험 24 개 이상 (d) flutter-preflight 실패 틀에 `  2. codegen : success / failed / skipped · 삭제` 로 시작하는 줄 1 · 옛 `  2. codegen : success · 삭제` 줄 0 (e) 루트 README `### flutter-toolkit` 절의 소개 수 · 파일 트리 `skills/` 줄의 수 · `**제공 스킬:**` 목록 항목 수가 모두 끝 판 flutter-toolkit 스킬 수와 같고 목록에 `scenario-report` 가 있다. 양성 대조: 시작 판 `fitpal=6 names_skill=2 names_format=3` · `preflight new=0 old=1` · `readme intro=19/20 tree=19/20 list=19/20 has_sr=0`. 음성 대조 (c): 예시 기록의 앱 이름만 바꾸고 보고서를 다시 만들지 않은 사본에서 같은 시험이 실패한다(봉인 전 실측) (측정: `type m >/dev/null || exit 2;` 뒤 `m SK-04` 네 줄이 `fitpal=0 names_skill=0 names_format=0` · `unittest rc=0 Ran <24 이상> tests …` · `preflight new=1 old=0` · `readme intro=20/20 tree=20/20 list=20/20 has_sr=1`) [exact, enumerated]
- [ ] SK-05: react-l10n 「지워진 키 수와 지워진 번역」 블록이 0 건 정상 상황에서 종료 코드 0 으로 끝나고 채운 번역 삭제는 드러낸다 — Given 빈 번역 키 하나만 지운 저장소(empty) · 채운 번역 하나를 지운 저장소(filled), When 끝 판 블록(`3. 지워진 키 수와` 아래 첫 bash 블록)을 bash · zsh 로 돌리면, Then 네 실행 모두 종료 코드 0 이고 끝 줄이 empty 는 `filled_deleted=0` · filled 는 `filled_deleted=1` 이며 filled 는 `-msgstr "비"` 줄을 찍는다. 블록 안 `git diff -U0 -- src/infrastructure/i18n/locales/ | ` 로 시작하는 줄 가운데 `| grep` 을 담은 줄 0 · 「`filled_deleted=0` 이 아니면」 이 든 줄 1. 양성 대조: 시작 판 empty 의 bash · zsh 종료 코드 1 (측정: `type m >/dev/null || exit 2;` 뒤 `m SK-05` 두 줄이 `l10n empty/bash=[1|filled_deleted=0| rc=0] empty/zsh=[1|filled_deleted=0| rc=0] filled/bash=[1|-msgstr "비"|filled_deleted=1| rc=0] filled/zsh=[1|-msgstr "비"|filled_deleted=1| rc=0]` · `sentence=1 grep_second=0`) [exact]
- [ ] SK-06: rust-audit 두 줄이 가리키는 자리와 명령이 맞다 — (a) Gotcha 16 줄이 「rust-run §2 첫 항목」 을 담고 옛 「rust-run (c)」 0 이며, rust-run `## 2. 실행 + 결과 출력` 절의 첫 `- ` 항목이 「네 칸」 을 담는다 (b) 「→ 0 을 "안티패턴 없음 PASS"」 줄의 첫 백틱 명령을 bash 로 돌리면 `.rs` 두 파일(하위 폴더 하나 포함)에 하나씩 든 `src/` 에서 출력 `2` · 종료 코드 0, 하나도 없는 `src/` 에서 출력 `0` · 종료 코드 0 이다(같은 폴더 `.txt` 의 같은 글은 세지 않는다). 그 줄이 「가 없으면」 · 「(a) 로 거른다」 를 함께 담는다(`src/` 가 없을 때 파이프 끝 awk 가 grep 오류를 가려 0 이 찍히는 한계). 양성 대조: 시작 판 `g16 ref=0 old=1` · 명령 종료 코드 2 (`Is a directory`) · `no_src_note=0`, 예행 변형 `no-src-note`(그 문장만 지움) → `no_src_note=0` (측정: `type m >/dev/null || exit 2;` 뒤 `m SK-06` 두 줄이 `g16 ref=1 old=0 run2_first4=1` · `cmd two_hits=[2] rc=0 zero=[0] rc=0 no_src_note=1`) [exact]
- [ ] SK-07: api-ui 여는 방법이 bash · zsh 둘 다에서 포트를 쥔 서버 번호와 한 장 폴더를 찍는다 — `1. **여는 방법**` 항목 안(`2. **콘솔 오류**` 앞)의 bash 블록을 비어 있는 포트로 바꿔 bash · zsh 로 돌리면 두 셸 모두 셸이 서버에 묶이지 않고(종료 코드 0), `SERVING` 줄의 번호가 그 포트를 쥔 파이썬이며, `dir=` 폴더에 `ui.html` 한 장만 있고, 그 번호로 `kill` 하면 포트가 풀린다. 같은 항목에 「`` `&&` `` 로 잇지 않는다」 · 「bash · zsh」 가 든 줄이 각 1 이상. 양성 대조: 시작 판 `api_serve NO_BLOCK` · `no_amp=0 both_shells=0`. 앞 판 문장이 권하던 `&&` 이음은 bash 에서 찍힌 번호와 포트를 쥔 번호가 다르고 `dir=` 가 빈다(봉인 전 실측) (측정: `type m >/dev/null || exit 2;` 뒤 `m SK-07` 두 줄이 `api_serve bash:rc=0,pid_is_server=1,dir_ok=1,released=1 zsh:rc=0,pid_is_server=1,dir_ok=1,released=1` · `no_amp=<1 이상> both_shells=<1 이상>`) [exact]
- [ ] SK-08: bambu MakerWorld 받기 블록이 앞 실행이 남긴 모델 파일을 보고하지 않는다 — Given 앞 실행의 `design.json`(제목 `OLD-MODEL`) · `instances.json` 이 남은 폴더와 모든 받기가 연결 실패(파일을 쓰지 않고 상태 `000` · 종료 코드 7)하는 가짜 curl, When 끝 판 블록(`ID=<모델 번호>; OUT=<output_dir>/makerworld;` 줄부터 닫는 펜스 앞까지)을 bash 로 돌리면, Then 출력에 `OLD-MODEL` 0 · `FAIL design.json` 으로 시작하는 줄 1 · 두 파일이 남지 않는다. 양성 대조: 시작 판 `mw stale_title=1 fail_line=0 left=2` (측정: `type m >/dev/null || exit 2;` 뒤 `m SK-08` 이 `mw stale_title=0 fail_line=1 left=0`) [exact]

## Script

- [ ] SC-00: N/A (Script 카테고리는 `release.sh` 연동 · 버전 올림 · `marketplace.json` 갱신이다. 이 계약은 그 파일과 킷 `plugin.json` 을 건드리지 않는다 — 버전은 `.harness/.meta/kaizen-0924/release-plan.md` 대로 PR 을 합친 뒤 올린다. 측정: `type m >/dev/null || exit 2;` 뒤 `m SC-00` 의 `SC-00=0`. 양성 대조: 예행 변형 `shared` 는 루트 `CLAUDE.md` 만 건드려 `SC-00=0` 그대로이고, 같은 방식으로 `marketplace.json` 을 건드린 변형 `release` → `SC-00=1`)

## Error

- [ ] ER-01: 옛 값 검사가 backend-kit 을 뺀 채 넘어가지 않는다 — 끝 판 전체 사본에서 `python3 scripts/check-stale-values.py` 가 종료 코드 0 · 「검사 제외:」 줄 0 · 검사 범위 `26/26`, 같은 사본의 `backend-kit/skills/backend-test/SKILL.md` 끝에 `OpenAPI 3.1.1 최신` 한 줄을 넣으면 종료 코드 1 · 그 파일을 가리키는 줄 1. 양성 대조: 시작 판은 넣어도 `inject=1 rc=0 scope=25/25 excluded_line=1 hit=0` (측정: `type m >/dev/null || exit 2;` 뒤 `m ER-01` 두 줄이 `inject=0 rc=0 scope=26/26 excluded_line=0 hit=0` · `inject=1 rc=1 scope=26/26 excluded_line=0 hit=1`) [exact]
- [ ] ER-02: design-kit 결정 전파 검사가 모양이 틀린 입력을 종료 코드 2 로 내고 킷 시험이 그것을 지킨다 — Given 이 계약이 정한 입력 열(온전한 예 → 0 · id 형식 오류 → 2 · `excluded_surfaces` 문자열 목록 → 2 · `decisions` 문자열 목록 → 2 · 맨 위 목록 → 2 · `required_surfaces` 문자열 목록 → 2 · `assertions` 가 목록이 아닌 문자열 → 2 · 골든만 → 1 · 결정 0 건 → 3 · 파일 없음 → 3), When 끝 판 `design-kit/references/visual-change-protocol.md` 에서 뗀 검사 코드로 돌리면, Then 열 모두 기대 종료 코드이고 `Traceback` 으로 시작하는 줄을 낸 입력 0. 새 킷 시험 `design-kit/evals/decision-gate-test.sh`(git 모드 `100755`)가 끝 판 사본에서 종료 코드 0 이고, `DECISION_GATE_DOC` 로 시작 판 문서를 가리켜 돌리면 종료 코드가 0 이 아니다(음성 대조). 양성 대조: 시작 판 `gate ok=5/10 traceback=4` (`assertions` 문자열은 멈추지 않고 종료 코드 1 — 위반으로 잘못 분류) (측정: `type m >/dev/null || exit 2;` 뒤 `m ER-02` 두 줄이 `gate ok=10/10 traceback=0` · `kit_test rc=0 결과: … 불일치 0 start_doc rc=<0 아님> … exec=100755`) [exact]
- [ ] ER-03: 계약 봉인 범위 블록이 봉인 함수 넷 가운데 하나라도 없으면 멈춘다 — `harness/references/contract-schema.md` 의 `fm_get` 블록 · 봉인 블록 · `.harness/` 범위 블록을 떼어, `contract_digest` · `sha256_16` 을 지운 셸(missing)에서 봉인된 계약 하나가 든 `.harness/` 에 돌리면 bash · zsh 모두 종료 코드 2 · `STOP ` 으로 시작하는 줄 1 · `SEAL_BROKEN` 0, 넷 다 둔 셸(full)에서는 종료 코드 0 · `1 SEAL_OK`. 양성 대조: 시작 판 missing 은 `rc=0,stop=0,ok=0,broken=1` (측정: `type m >/dev/null || exit 2;` 뒤 `m ER-03` 이 `missing bash:rc=2,stop=1,ok=0,broken=0 zsh:rc=2,stop=1,ok=0,broken=0 | full bash:rc=0,stop=0,ok=1,broken=0 zsh:rc=0,stop=0,ok=1,broken=0`) [exact]
- [ ] ER-04: reflect-kit 수집 상태가 정상으로 끝난 실행 뒤를 멈춤으로 보지 않고, 그 뒤 실패는 다시 멈춤으로 본다 — Given 5 일 전 기록 하나 · 4 일 전 실패 한 쌍이 든 폴더, When 분석 결과가 「no issues」 인 실행 하나를 끝 판 Stop 훅(가짜 codex)으로 돌리면, Then `collect_status 7` 의 `⚠ 수집 멈춤` 줄이 1 → 0 이고 기록은 늘지 않으며, 그 뒤 실패 한 쌍을 더하면 다시 1. 킷 시험 둘(`collect-status-test.sh` · `log-reflection-test.sh`)이 끝 판 사본에서 종료 코드 0 이고, 시작 판 라이브러리(`PROJECT_ID_LIB`) · 시작 판 훅(`REFLECT_KIT_HOOKS`)으로 돌리면 각각 종료 코드 1 이다(음성 대조). 끝 판 훅 문자열에서 뽑은 사유 태그 줄기(변수로 끝나는 줄기 제외)에 정상 종료 태그 `ok:no-issues` 가 있고 그 가운데 SCHEMA.md · DESIGN.md 에 없는 것 0, reflect-digest Gotcha 13 줄과 `## 입력` 의 `.errors.log` 설명 줄(「/.errors.log` — 훅 자체 실패 로그」 가 든 줄)이 각각 `ok:no-issues` 를 담는다. 양성 대조: 시작 판 `after_noissues=1` · `has_ok=0` · `digest_in=0` · 예행 변형 `no-digest-in`(설명 줄의 새 글만 지움) → `digest_in=0` (측정: `type m >/dev/null || exit 2;` 뒤 `m ER-04` 세 줄이 `reflect_e2e before=1 after_noissues=0 after_new_fail=1 noissues_record=0` · `tests collect rc=0 […불일치 0] log rc=0 […불일치 0] | start_lib rc=1 start_hook rc=1` · `tags code=<N> has_ok=1 schema_missing=0 design_missing=0 digest_g13=1 digest_in=1`) [exact]
- [ ] ER-05: onboarding 게이트의 「Step 마다 출처 정확히 하나」 판정을 시험이 지킨다 — 끝 판 사본에서 러너 `run-gate-evals.sh` 가 종료 코드 0 · `EVALS declared=7 ran=7 fail=0` · `EVALS_PASS`, `gate_cases` 에 픽스처 `fixtures/gate-fail-ledger-misplaced.md` · 기대 줄 `G1_LEDGER FAIL steps=2 ledger=2 misplaced=2` · 끝 줄 `GATE_FAIL` 인 사례 1. 음성 대조: 끝 판 사본 SKILL.md 에서 misplaced 판정 두 줄(`  elif [ "$misplaced" -ne 0 ]; then` 과 다음 줄)을 지우면 러너가 종료 코드 1 · `EVALS_FAIL` — 시작 판에서 같은 삭제는 `EVALS_PASS` 였다(봉인 전 실측) (측정: `type m >/dev/null || exit 2;` 뒤 `m ER-05` 두 줄이 `runner rc=0 EVALS declared=7 ran=7 fail=0 EVALS_PASS case=1` · `no_misplaced_check rc=1 EVALS_FAIL`) [exact]
- [ ] ER-06: CI 가 evals.json 규칙 밖 새 시험 둘을 돈다 — `.github/workflows/ci.yml` 의 `validate` 잡 단계 `run` 값 가운데 `python3 -m unittest discover -s flutter-toolkit/evals/scenario-report -v` · `bash design-kit/evals/decision-gate-test.sh` 가 글자 그대로 있고(2/2) 잡 수는 3 그대로이며, `actionlint` 종료 코드 0, 두 명령을 끝 판 사본에서 돌리면 둘 다 종료 코드 0. 양성 대조: 시작 판 `ci jobs=3 validate_has=0/2` (측정: `type m >/dev/null || exit 2;` 뒤 `m ER-06` 세 줄이 `ci jobs=3 validate_has=2/2` · `actionlint=0` · `run scenario=0 decision_gate=0`) [exact, enumerated]
- [ ] ER-07: 마흔여섯 파일에 더한 줄(파일마다 시작 판과 비교, 새 파일은 전부)에 번역투 6 종(`tone-kit/references/locale-korean.md` §2 치환표의 grep 열)과 특정 앱 이름 · 화면 도구 서버 이름(`fit-?pal` · `fit_pal` · `fit pal` · `flutter[-_]playwright` · `playwright-mcp` · `chrome-devtools-mcp`, 대소문자 무시)이 든 줄 0. 양성 대조: 예행 변형 `bad-text`(「이 값에 대해 fit-pal 앱」 한 줄) → `k02=1 names=1` (측정: `type m >/dev/null || exit 2;` 뒤 `m ER-07` 이 `added=<1 이상> k02=0 names=0`) [exact]
- [ ] ER-08: 고치지 않은 것을 다음 사이클로 넘기고 공유 파일을 건드리지 않는다 — notes `.harness/.meta/kaizen-0924/f2-review-fixes-notes.md` 가 끝 판에 커밋돼 있고 (a) 절 머리 넷(`## 커밋` · `## 다룬 항목` · `## 고치지 않은 항목과 이유` · `## 다음 사이클 메모`) 각 1 (b) `## 커밋` 표에 묶음 열셋마다 `| <묶음> | <sha> |` 행이 있고 그 커밋이 끝 판의 조상 · 서명 커밋 · 그 묶음 경로만 건드린 커밋이다(13/13) (c) `## 다음 사이클 메모` 가 `## 범위 경계` 에 적은 토큰 열아홉을 각 1 이상 담는다 (d) 감사 기록 `.harness/.meta/orchestrator-audit-log.md` 는 시작 판에서 지운 줄 0 · 더한 줄(빈 줄 제외) 1 이고 그 줄이 `f2-review-fixes-notes.md` 를 담는다 (e) 공유 파일 여덟(`.claude-plugin/marketplace.json` · `*/.claude-plugin/plugin.json` · `CLAUDE.md` · `.claude/kaizen-input/insights-report.md` · `.harness/.meta/kaizen-failure-count.yaml` · `.harness/stale-values.yaml` · `docs/index.html` · `docs/kaizen`)을 건드린 커밋 0. 양성 대조: 예행 변형 `no-notes` → `notes_committed=0` · `shared` → `shared_commits=1` · `audit2`(감사 기록에 줄 둘을 더 더함) → `audit added=3 added_ptr=1 deleted=0 shared_commits=0` (측정: `type m >/dev/null || exit 2;` 뒤 `m ER-08` 다섯 줄이 `notes_committed=1` · `1 1 1 1` · `commit_rows=13/13` · 열아홉 값 모두 1 이상 · `audit added=1 added_ptr=1 deleted=0 shared_commits=0`) [exact, enumerated]

## Architecture

- [ ] AR-01: 이 계약의 변경이 허용 경로 안에 머물고, 한 커밋에 묶음 하나이며, 범위 선언 블록이 그 경로와 같고, 이 계약이 봉인돼 있다 [exact, enumerated]
  (측정: `type m >/dev/null || exit 2;` 뒤 `m AR-01` 여섯 줄이 `0` · `0 46` · `mixed=0 one_kit=<13 이상>` · `0` · `SEAL_OK` · `scope_same=1 harness_line=1`.
  첫째 — 시작 커밋부터 `$END` 사이에 `FILES` 마흔여섯과 묶음 경로(`GPATH`)를 건드린 커밋 가운데 이 계약 서명 줄이 없는 커밋 수 0 (서명을 빠뜨린 커밋은 서명 목록에 안 보이므로 경로로 직접 센다).
  둘째 — 서명 커밋이 건드린 경로 가운데 `FILES` 밖이면서 이 계약 `.harness/` 허용 갈래(계약 · 개정 · QA 피드백 · `.harness/.meta/kaizen-0924/f2-review-fixes-*.md` · 감사 기록) 밖인 경로 수 0 과, `FILES` 가운데 서명 커밋이 건드린 수 46.
  셋째 — 서명 커밋 가운데 묶음 둘 이상을 건드렸거나 묶음과 `.harness/` 를 함께 건드린 커밋 0 · 묶음 하나만 건드린 커밋 13 이상(FIX 가 커밋을 더할 수 있다. 묶음마다 커밋이 있는지는 ER-08 (b) 가 잰다).
  넷째 — 끝 판을 푼 폴더의 `.harness/` 에서, 이 계약 서명 커밋이 건드린 계약 파일 가운데 봉인이 깨진 것의 수 0 (`harness/references/contract-schema.md` §`.harness/` 범위 조건 권장 형태 — 작업 폴더에는 다른 세션의 미커밋 변경이 있을 수 있다).
  다섯째 — 끝 판 이 계약의 봉인이 `SEAL_OK`. 여섯째 — `## 범위 경계` 절 `# sprint-scope` 블록의 `.harness/` 밖 경로가 `FILES` 와 같고 `.harness/` 줄이 1.
  양성 대조: 예행 변형 `unsigned` → 첫째 `1` · `outside`(서명 커밋이 `infra-kit/README.md` 를 고침) → 둘째 `1 46` · `mixed`(서명 커밋 하나가 `react-kit` · `rust-kit` 파일을 함께 고침) → 셋째 `mixed=1` · `seal-broken`(서명 커밋이 봉인 뒤 조건 줄을 바꿈) → 넷째 `1` · 다섯째 `SEAL_BROKEN`)
- [ ] AR-02: 문서 사이트 일곱 쪽이 원본이 바뀐 절만 따라가고 원본 담김은 줄지 않는다 — 끝 판 페이지 글(태그를 벗기고 엔티티를 푼 글)에서 (a) `docs/harness/contract-schema.html` 에 `type verify_seal fm_get contract_digest sha256_16` 1 · `type verify_seal fm_get >/dev/null` 0 (b) `docs/bambu-kit/bambu-print-profile.html` 에 `rm -f "$OUT/design.json" "$OUT/instances.json"` 1 (c) `docs/design-kit/visual-change-protocol.html` 의 검사 코드 블록이 끝 판 원본 검사 코드 블록의 줄(앞뒤 공백 · 빈 줄 제외)을 모두 담는다(빠진 줄 0) (d) `docs/design-kit/design-test.html` 에 「위반 0」 0 · `SCHEMA_ERROR` · `NO_SURFACE` 각 1 (e) `docs/reflect-kit/schema.html` · `docs/reflect-kit/design.html` 각각에 `ok:no-issues` 1 (f) `docs/api-kit/static-evidence-viewer-contract.html` 에 「&& 로 잇지 않는다」 1 · 옛 「두 명령은 한 번의 셸 호출에서 잇는다」 0 (g) 원본 · 페이지 짝 여덟(일곱 쪽 · api 쪽은 원본 둘) 모두 원본의 백틱 표시 가운데 시작 판 페이지에 있던 것이 끝 판 페이지에서 빠진 수(`lost`) 0 이고, 원본 낱말이 페이지 글에 든 비율(`wr`)이 시작 판 페이지 이상이다 — 원본은 순서대로 `visual-change-protocol.md` · `design-test/SKILL.md` · `contract-schema.md` · `bambu-print-profile/SKILL.md` · `reflect-kit/docs/SCHEMA.md` · `reflect-kit/docs/DESIGN.md` · `docs/api/verification/static-evidence-viewer-contract.md` · `api-kit/skills/api-ui/SKILL.md`. 양성 대조: 시작 판 `schema=0/1 bambu=0 design_test=1/0/0 reflect=0/0 api=0/1` · 예행 변형(원본 검사 코드만 고치고 페이지는 두 줄만 맞춘 판) → (c) `missing=11` · 예행 변형 `page-loss`(reflect design 쪽에서 `<code>` 셋 이상 든 목록 하나를 지움) → (g) `docs/reflect-kit/design.html lost=1 wr_ok` · `page-prose`(같은 쪽에서 `<code>` 없는 문단만 지움 — `lost` 로는 안 잡히는 경우) → `docs/reflect-kit/design.html lost=0 wr_down` (측정: `type m >/dev/null || exit 2;` 뒤 `m AR-02` 첫 줄이 `schema=1/0 bambu=1 vcp_missing=0 design_test=0/1/1 reflect=1/1 api=1/0` 이고 뒤 여덟 줄이 모두 `lost=0 wr_ok` 로 끝난다) [exact, enumerated]

## Anti-patterns

- [ ] AP-01: 버전을 하드코딩하지 않는다 — plugin.json에서 읽어야 한다. 이번 변경에 적용: 마흔여섯 파일에 더한 줄에 끝 판 킷 `plugin.json` 의 `version` 값(서로 다른 값 모두)이 앞뒤가 숫자 · 점이 아닌 자리로 든 줄 0 — 이 계약은 킷 버전을 적지 않는다. 양성 대조: 예행 변형 `bad-text` 에 킷 버전 한 줄을 더하면 `hits=1` (측정: `type m >/dev/null || exit 2;` 뒤 `m AP-01` 이 `versions=11 hits=0`)
- [ ] AP-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수 (```` ```text, ```bash, ```yaml ```` 등). 판정 권위는 validate-plugin V6 상태기계다 — 여는/닫는 fence 가 동형이라 줄 단위 정규식으로는 판정 불가. 이번 변경에 적용: 끝 판 `python3 scripts/validate-plugin.py --check=code-fence` 종료 코드 0 이고, 마흔여섯 파일 가운데 마크다운 스물일곱 각각의 언어 힌트 없는 여는 펜스 수가 시작 판(새 파일은 0)보다 늘지 않는다. 양성 대조: 예행 변형 `bare-fence`(rust-audit 끝에 힌트 없는 펜스 하나) → `md=27 bare_up=1 v6_rc=2` (측정: `type m >/dev/null || exit 2;` 뒤 `m AP-03` 이 `md=27 bare_up=0 v6_rc=0`)
- [ ] AP-04: SKILL.md / agents/*.md frontmatter 에서 name 필드 누락 — validate-plugin V1 FAIL. 이번 변경에 적용: 마흔여섯 파일 가운데 SKILL.md · agents 열여덟 모두 첫 frontmatter 블록에 `name: ` 줄이 있고, scenario-report 설명 줄(「  Flutter 앱을 」 으로 시작)을 빼면 시작 판과 글자 그대로 같으며, 그 설명 줄은 바뀌었다 (측정: `type m >/dev/null || exit 2;` 뒤 `m AP-04` 가 `skill_agent=18 name=18 fm_same_but_scenario_desc=18 scenario_desc_changed=1`)

## Reusability

- [ ] RE-01: N/A (재사용 단위 코드를 새로 만들지 않는다 — 새 파일 둘은 킷 시험 스크립트와 시험 입력이다. 측정: `type m >/dev/null || exit 2;` 뒤 `m RE-01` 의 `RE-01=` 값이 `design-kit/evals/decision-gate-test.sh onboarding-kit/skills/setup-guide/evals/fixtures/gate-fail-ledger-misplaced.md` 두 경로뿐)
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다. 이번 변경에 적용: (a) 새 결정 전파 시험은 검사 코드를 복사하지 않고 부를 때마다 `visual-change-protocol.md` 에서 뗀다(onboarding 러너와 같은 방식) — 시험 파일에 `visual-change-protocol.md` 가 든 줄 1 이상 · 검사 코드 줄(`PATTERNS =` · `viol =` · `decisions =` 로 시작) 0 (b) 새 CI 단계는 기존 `validate` 잡(파이썬 · PyYAML 설치됨)에 넣고 잡을 새로 만들지 않는다 — 잡 수 3 (c) docs-site 표는 F2 표 행을 글자 그대로 옮긴다(SK-02 (d)). 양성 대조: 예행 변형 `copied-gate`(시험 끝에 검사 코드 한 줄을 빈 heredoc 으로 복사) → `copied_gate_lines=1` (측정: `type m >/dev/null || exit 2;` 뒤 `m RE-02` 가 `test_reads_doc=<1 이상> copied_gate_lines=0 ci_jobs=3`)

## Diagnostics

- [ ] DG-01: N/A (`commands.analyze` 는 `bash -n scripts/release.sh` 라 `scripts/release.sh` 만 잰다 — 이번 변경 파일과 교집합 0 개. 측정: `type m >/dev/null || exit 2;` 뒤 `m DG-01` 의 `DG-01=0`. 새 셸 코드의 실제 검사는 DG-02 의 shellcheck 와 DG-04)
- [ ] DG-02: IDE diagnostics 워닝/인포 0개 (`diagnostics.ide_exclude` 값 `[]`) — 이번 변경에 적용: 편집기 마크다운 확장과 같은 조건(markdownlint-cli2 0.23.2 · MD013 끔)으로 마흔여섯 파일 가운데 마크다운 스물일곱 **각각**에서 규칙별 경고 수를 시작 판(새 파일은 0)과 비교해 는 규칙이 있는 파일 0, 셸 파일 다섯 각각의 `shellcheck -f gcc` 줄 수가 시작 판(새 파일은 0)보다 늘지 않는다. 더한 줄만 세지 않는다 — MD022 · MD032 · MD024 는 더한 줄 옆의 손대지 않은 줄에 붙는다. 양성 대조: 예행 판에서 새 픽스처의 주소를 `<…>` 없이 두면 `UP onboarding-kit/…/gate-fail-ledger-misplaced.md MD034:0>2` · 예행 변형 `sh-unquoted`(새 시험 끝에 따옴표 없는 `echo $W`) → `SC_UP design-kit/evals/decision-gate-test.sh 0>1` · `sh_files=5 sh_up=1` (측정: `type m >/dev/null || exit 2;` 뒤 `m DG-02` 끝 두 줄이 `md_files=27 files_up=0` · `sh_files=5 sh_up=0`)
- [ ] DG-03: N/A (`commands.test` 는 `bash scripts/release.sh 2>&1 || true` 라 `scripts/release.sh` 만 잰다 — 교집합 0 개. 측정: DG-01 과 같은 `m DG-01` 의 `DG-01=0`. 실제 시험은 DG-04)
- [ ] DG-04: 실제 앱/서버 구동 시 에러 0개 — 이번 변경에 적용: 구동하는 것은 킷 시험 · 러너다. 끝 판 전체 사본에서 CI 가 도는 킷 시험 열하나(react 프로젝트 감지 · reflect 셋 · onboarding 러너 · howto 러너 · scenario-report 단위 시험 · 결정 전파 시험 · 카이젠 수집기 시험 · 커밋 안전 훅 시험 · Dart 포맷 훅 시험)가 모두 종료 코드 0 (`save-test.sh` 는 실제 `~/.harness/feedback` 에 쓰고, 이 계약이 그 스크립트가 재는 `harness/scripts` 를 건드리지 않아 뺀다) (측정: `type m >/dev/null || exit 2;` 뒤 `m DG-04` 가 `tests project-detect-test.sh=0 log-reflection-test.sh=0 project-id-test.sh=0 collect-status-test.sh=0 run-gate-evals.sh=0 run-evals.sh=0 scenario-report=0 decision-gate-test.sh=0 test-collect-kaizen-data.py=0 commit-guard-test.sh=0 format-edited-dart-test.sh=0`)
- [ ] DG-05: 저장소 검사가 이 계약이 고친 곳을 문제로 가리키지 않는다 — 끝 판 전체 사본에서 (a) `python3 scripts/validate-plugin.py <킷>` 을 킷 열넷(`harness` · `flutter-toolkit` · `design-kit` · `backend-kit` · `infra-kit` · `rust-kit` · `react-kit` · `planning-kit` · `reflect-kit` · `bambu-kit` · `onboarding-kit` · `tone-kit` · `api-kit` · `howto-kit`)에 돌려 종료 코드가 0 이 아닌 킷 0 (V 줄 글자가 아니라 종료 코드) (b) `sync-docs.py --check-only` · `sync-evals.py --check-only` · `sync-orchestrator.py --check-only` · `run-evals.py` · `check-docs-links.py` · `check-contrast-claims.py` · `check-stale-values.py` 일곱이 모두 종료 코드 0 (측정: `type m >/dev/null || exit 2;` 뒤 `m DG-05` 두 줄이 `validate_fail: none` · `checks sync-docs.py=0 sync-evals.py=0 sync-orchestrator.py=0 run-evals.py=0 check-docs-links.py=0 check-contrast-claims.py=0 check-stale-values.py=0`) [exact, enumerated]
- [ ] DG-06: `python3 scripts/validate-post-kaizen.py --since 6a8be196d9c40a1686f51f9a6bd50039c2bd5b71` 출력에 `scope-isolation` 줄과 `doc-contracts` 줄이 각각 있고 둘 다 `[ PASS  ]` 로 시작한다 — 줄이 없거나 `SKIP` 이어도 실패다. 양성 대조: 예행 변형 `dg06-fail`(한 커밋이 `harness/skills/` 와 `react-kit/skills/` 를 함께 고침) → `[ FAIL  ]` 로 시작하는 `scope-isolation` 줄 · `dg06 lines=2 pass=1` · `dg06-skip`(오케스트레이터 `# docs-contract` 머리를 바꿔 선언 블록 0) → `[ SKIP  ]` 로 시작하는 `doc-contracts` 줄 · `dg06 lines=2 pass=1` (측정: 작업 폴더에서 `type m >/dev/null || exit 2;` 뒤 `m DG-06` 끝 줄이 `dg06 lines=2 pass=2`) [exact]
