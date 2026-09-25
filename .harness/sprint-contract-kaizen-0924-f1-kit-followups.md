---
feature: "카이젠 2026-09-24 Final 후속 수정 — 킷 쪽 (교차 진단 계약 밖 결함 · notes 가 Final 로 넘긴 킷 몫 · 연구 기록 새 편집기 경고 · Codex 검토 r2 · r3)"
slug: kaizen-0924-f1-kit-followups
created: "2026-09-25 15:01"
complexity: "복잡"
conditions: 30
status: active
owner_session: de8c7935-a5b6-4df5-9106-fafa73c288a0
conditions_digest: sha256:d165f830e0906f4b
locked_at: "2026-09-25 17:34"
---

## 배경

카이젠 2026-09-24 Final 의 두 후속 계약 가운데 킷 쪽이다. 입력은 Final 지침(`final-runbook.md`)의 「먼저 읽을 것」 다섯이다 — 공통 지침 `phase-runbook.md` ·
오케스트레이터 `.claude/skills/kaizen-orchestrator/SKILL.md` Step F1 ~ F4 · Final 처리 목록 `final-todo.md` · 교차 진단 전문 `xdiag-all.md` ·
Phase 1 ~ 17 notes(`.harness/.meta/kaizen-0924/phase{N}-notes.md`)의 「넘기는 것」 · 「미반영 키와 사유」 · 「다음 사이클 메모」. 이 계약이 고쳐도 되는 곳은
킷 폴더(`harness` 제외)와 그 킷 원본 문서 폴더(`docs/backend` 등, HTML 아님)다. `harness/` · `scripts/` · `.claude/skills/` · `.github/workflows/ci.yml` 은
`kaizen-0924-f1-harness-followups`, `.harness/` · 문서 사이트 HTML · 기록(changelog · 연구 기록 새 항목) · 버전 계획은 `kaizen-0924-final` 몫이다.

가장 무거운 입력은 교차 진단이 「뜻 기준 FAIL」 이라 한 DG-02 다. Phase 7 · 8 · 9 · 11 이 연구 기록 맨 위에 새 항목을 넣으면서 옛 항목과 같은 소제목을 써서
같은 제목 중복 경고(MD024)가 새로 생겼는데, 측정이 더한 줄만 봐서 0 이 나왔다. 봉인 전에 이 사이클 동안 바뀐 킷 쪽 마크다운 132 개를 사이클 개시 커밋(`7689fde`) 판과
규칙별로 비교했다 — 는 규칙이 있는 파일은 정확히 그 넷이다(`UP docs/backend/research-log.md MD024:13>17` · `UP docs/infra/research-log.md MD024:13>15` ·
`UP docs/planning/research-log.md MD024:1>2` · `UP docs/rust/research-log.md MD024:8>9` · `files=132 files_up=4`). Phase 5 · 6 · 10 · 12 ~ 17 의 파일은 는 규칙이 없다.

교차 진단이 적은 「계약 밖」 결함 가운데 킷 파일에 있는 것, notes 가 「Final」 에 넘긴 킷 몫, 그리고 같은 결함이 같은 줄에서 한 번 더 보인 자리를 이 계약이 고친다.
고치지 않는 입력은 `## 범위 경계` 의 입력 항목 표에 이유와 함께 적고 notes `## 다음 사이클 메모` 로 넘긴다.

초안을 쓴 뒤 Codex(`gpt-5.6-sol`, 읽기 전용)가 이 가지의 킷 쪽 변경을 두 묶음으로 따로 검토했다 — r2(flutter · design · react · backend · infra · rust · planning, 8 건)와
r3(reflect · bambu · onboarding · tone · api · howto, 6 건). 지적마다 명령을 돌리거나 파일을 인용해 다시 확인했다. 확인된 열 건은 조건으로 더했고(SK-03 (d) · SK-04 둘째 줄 ·
SK-05 넷째 줄 · SK-06 (c)(d) · SK-07 (d)(e) · SK-08 (d) · SK-12), 확인할 수 없거나 판정 문턱을 바꾸거나 심각도가 낮아 미룬 넷은 입력 항목 표 67 ~ 80 행에 「고치지 않음 — 이유」 로 적었다.
그래서 고치는 파일이 서른에서 마흔하나로 늘었다. 교차 진단 P12 결함 1(수집 멈춤 경고)은 r3-1 과 같은 결함이라 SK-06 (c) 한 조건으로 묶었다.

## 리서치 소스

새로 찾은 자료는 없다. 러닝북대로 Phase 근거 파일(`.harness/.meta/evidence/phase*.md`)에 있는 것만 쓴다 — ER-01 이 잰다.

- [Vite server options](https://vite.dev/config/server-options.html#server-port) · [Vite CLI](https://vite.dev/guide/cli) — `server.strictPort` 는 포트가 차 있으면 다음 포트로 옮기지 않고 멈춘다. CLI 에 `--strictPort` 가 있다 (`phase10.md:27` · `:28` · `:68` · `:71`, SK-05)
- [Firebase Apple 셋업](https://firebase.google.com/docs/ios/setup) — Xcode 26.2+ · 최소 iOS 15. Cloud Messaging 을 쓰면 실제 Apple 기기를 준비하라고 한다. 시뮬레이터 수신 주장은 근거가 없다 (`phase14.md:82` · `:90` · `:91` · `:98` · `:100`, SK-08)
- Apple 지원 기능 표 · 멤버십 개요 · 가입 비용 면제 — 예제의 막는 요구 표는 `onboarding-kit/skills/setup-guide/references/format-checklist.md` §2 의 세 행을 글자 그대로 옮긴다. 그 행의 주소는 `phase14.md:22` · `:27` · `:84` · `:85` 에 있다 (SK-08 · RE-02)
- [RFC 8785 정정 7920](https://www.rfc-editor.org/errata/rfc8785) — `-0` 은 `0` 으로 적혀 부호가 사라지니 읽는 쪽은 오류를 내야 한다(SHOULD) (`phase16.md:34` · `:137` · `:162`, SK-10)
- 내부: 교차 진단 전문 각 절 「계약 밖」 · Final 처리 목록 · notes 넘김 표 — 결함 위치와 재현 방법 (각 조건)
- 내부: Codex 검토 결과 `scratchpad/kaizen/codex/r2-kits-a.md` · `r3-kits-b.md` — 지적 위치와 재현 입력. 거기 인용된 바깥 주소(RFC 9457 · RFC 7493 · build_runner CHANGELOG)는 근거 파일에 없는 것이라 킷 파일에 옮기지 않는다 (입력 항목 표 67 · 73 · 80 행).
  build_runner 2.7.0 동작은 바깥 주소 대신 이 맥에 설치된 `build_runner-2.13.1` 의 CHANGELOG 파일로 확인했다 (73 행)
- 내부: `docs/api/contract/error-status-contracts.md` §2 — 같은 레포 api-kit 연구 문서가 RFC 9457 §3.1 을 1 차 출처로 대조해(`d937aca`) 「`type` 이 없으면 `about:blank` 로 간주 — 누락 자체는 위반이 아니다」 로 적었다. backend 세 자리의 「다섯 필드 필수」 가 RFC 요구가 아니라는 근거다 (SK-12 (a) `basis=1`)

## GAP 분석 · 개선안 초안

복잡도 4 축 (Step 1). 넷 다 예라 **복잡** 이다. 기능 조건이 20 이라 상한 안이다 — 킷 열셋에 걸친 작은 수정 묶음이고 킷마다 커밋을 나누므로 스프린트를 더 나누지 않는다.
Codex 지적은 조건 수를 늘리지 않으려고 그 킷의 기존 조건에 측정 줄로 더했고, 기존 조건이 없는 backend · infra 둘만 SK-12 하나로 묶었다 (Final 지침 「킷마다 조건 하나로 묶고 측정을 여럿 둔다」).

| 축 | 물음 | 값 |
| -- | ---- | -- |
| 레이어 수 | 몇 개 계층을 관통하는가 | 넷 — 스킬 문서(SKILL.md 열일곱 · references 일곱 · README 셋 · reflect 문서 둘) · 실행 블록과 스크립트(bambu 완료 검사 · 음성 대조 · 자기 검사 · 댓글 받기 블록 · design 결정 게이트 · infra checkout 검사 · onboarding `guide_gate` · howto 러너 · reflect `collect_status` 와 그 시험) · 평가 데이터(`evals.json` 둘) · 연구 기록 · 예제 · 원칙 문서 |
| 공개 API·계약 변경 | 밖에서 읽는 형식이 바뀌는가 | 예 — howto 러너가 세는 펜스가 넷으로 는다(`gate_blocks` 대조 범위) · bambu 완료 검사가 enum 0 목록에 `[미검증]` 을 낸다 · 음성 대조 블록이 반대 방향도 멈춘다 · 예제의 사전 요구사항이 세 칸 표가 된다 · design 결정 게이트가 필드 빠진 결정 · 표면 없는 결정에 종료 코드 2 · 1 · 3 을 내고 요약 줄에 `schema_errors=` 가 붙는다 · onboarding G1 이 Step 마다 출처 줄 하나를 요구한다(`misplaced=` FAIL 줄) · reflect `collect_status` 가 마지막 기록 뒤 실패에도 `⚠ 수집 멈춤` 줄을 낸다 |
| 소비면 존재 | 반대편이 있는가 | 예 — 문서 사이트 HTML(`fcm-ios-example.html` · `visual-evidence-protocol.html` · `project-detection.html` · `snapshot-sealing-canonicalization.html` · `gate-result-taxonomy.html`, `kaizen-0924-final` F2) · Phase 7 · 8 · 9 · 11 개정 파일의 「교차 진단 뒤 Final 에서 고침」 줄(`kaizen-0924-final`) · 버전 계획(`kaizen-0924-final`) · `.claude/skills/howto-kaizen/SKILL.md`(러너 끝 줄 `EVALS_PASS` 는 그대로다) · 올리지 않은 가지 `feat/bambu-kit-orca-h2s-feedback`(같은 음성 대조 블록을 고친다) · reflect-digest `## 승격 후보` 를 비우는 문턱(Gotcha 13)과 reflect-kaizen `calibration_confidence: low` — 새 `⚠ 수집 멈춤` 줄을 같은 머리 글로 읽는다 · design-audit · design-reviewer 의 Decision Propagation Coverage 판정(게이트 종료 코드를 읽는다) · 문서 사이트 `api-design.html` · `visual-change-protocol.html` · `bambu-print-profile.html`(bambu 자기 검사 블록의 사본이 있다) · `schema.html`(reflect 사유 태그 목록을 싣는다) — ER-03 이 넘김을 잰다 |
| 회귀 위험 | 기존 동작이 깨질 경로 | 예 — 러너 · 완료 검사 · 음성 대조 블록 · onboarding 검사 함수 `guide_gate`(G1 블록)와 그 함수가 도는 예제 · reflect `collect_status` · design 결정 게이트를 고친다. 바꾸지 않을 부분은 AR-03 이 잠그고, 기존 시험(reflect 열 경우 · onboarding 여섯 경우 · howto 서른셋)은 SK-06 · DG-04 가 다시 돌린다 |

설정 리터럴 대조표 (Step 1.2, `.harness/project.yaml` 원문):

| config key | project.yaml 에서 읽은 값 | 계약에 쓴 값 |
| ---------- | ------------------------- | ------------ |
| `commands.analyze` | `bash -n scripts/release.sh` | DG-01 N/A 사유에 그대로 |
| `commands.test` | `bash scripts/release.sh 2>&1 \|\| true` | DG-03 N/A 사유에 그대로 |
| `diagnostics.ide_exclude` | `[]` | DG-02 에 그대로 |
| `contract_categories[].id` / `prefix` | Skill/SK · Script/SC · Error/ER · Architecture/AR | 그대로 |
| `anti_patterns[].id` / `message` | AP-01 · AP-02 · AP-03 · AP-04 | AP-01 · AP-03 · AP-04 — 메시지 원문 그대로. AP-02(force push)는 이 계약이 푸시하지 않아 뺐다 |

편집 전 감사 (Step 1.4, 시작 커밋 `5b4fd72` 판을 실제로 읽은 줄):

| 대상 파일 | 실제 Read 증거 (`파일:라인`) | 발견한 기존 갭·위반 | 계약 조건화 여부 |
| --------- | ---------------------------- | ------------------- | ---------------- |
| `docs/backend/research-log.md` | `:18` · `:34` · `:42` · `:57` (2026-09-24 항목 소제목) · 같은 이름 `:103` · `:145` · `:153` · `:167` | MD024 13 → 17 (편집 전 판 대비) | SK-01 |
| `docs/infra/research-log.md` | `:14` · `:30` · 같은 이름 `:69` · `:100` | MD024 13 → 15 | SK-01 |
| `docs/rust/research-log.md` | `:14` · 같은 이름 `:73` | MD024 8 → 9 | SK-01 |
| `docs/planning/research-log.md` | `:37` · 같은 이름 `:98` · `:150` | MD024 1 → 2 | SK-01 |
| `flutter-toolkit/references/project-detection.md` | `:56` · `:57` 표 행 · `:59` | 묶음 타겟을 codegen 줄 자리에 넣으라는 문장 — 둘째 실행이 analyze · test 까지 돌고 실패가 `codegen_exit` 로 찍힌다. 두 스킬은 실제로 단계를 하나씩 부른다(flutter-build · flutter-preflight 에 `app-build` · `app-preflight` 0 줄) | SK-02 (a) |
| `flutter-toolkit/references/visual-evidence-protocol.md` | `:151` ~ `:154` 증거 블록 · `:156` 미검증 줄 · 머리 `version: 1.2.0` | 빈칸 넷이 `[미검증] 사유` — 네 칸을 요구하는 `:156` 과 어긋난다 | SK-02 (b) |
| `flutter-toolkit/skills/flutter-build/SKILL.md` · `flutter-preflight/SKILL.md` | `flutter-build:90` ~ `:94` · `flutter-preflight:135` ~ `:143` 실패 틀 | 성공 틀에만 삭제 줄이 있다 | SK-02 (c) |
| `flutter-toolkit/skills/flutter-l10n/SKILL.md` | `:15` Gotcha · `:121` ~ `:125` Step 6 표 · `:35` 설치 명령(`slang_build_runner`) | Gotcha 는 `fvm dart run slang`, 표는 build_runner 블록 — 두 경로가 어긋나고 Gotcha 쪽은 삭제를 세지 않는다 | SK-02 (d) |
| `design-kit/skills/design-component/SKILL.md` | `:15` `# Gotchas` ~ `:28` Gotcha 12 · `:30` `# Process` · `:46` Step 0 의 규약 인용 | 규약 머리(`visual-change-protocol.md:3` ~ `:4`)는 일곱 스킬이 Gotcha 한 줄로 인용한다는데 이 스킬만 Gotcha 에 없다 | SK-03 |
| `design-kit/README.md` · `reflect-kit/README.md` | `design-kit/README.md:5` `버전: \`0.1.0\`` · `reflect-kit/README.md:7` `버전: \`0.3.0\`` (plugin.json 은 0.4.0 · 0.7.1) | 하드코딩한 버전 줄이 둘 다 낡았다 — AP-01 과 같은 결함 | SK-03 · SK-06 · AP-01 |
| `infra-kit/references/gate-result-taxonomy.md` | `:42` 「같은 원칙이 **규칙 소스**에도 적용된다」 | 번역투(K-02 `(표시\|적용\|…)(됩니다\|된다)`). 같은 문장을 infra-audit Gotcha 12 는 「해당한다」 로 고쳤다 | ER-02 |
| `rust-kit/skills/rust-audit/SKILL.md` · `rust-model/SKILL.md` | `rust-audit:36` Gotcha 16 · `rust-model:31` | 네 칸 없는 `[미검증]` 두 자리 — rust-run (c) 와 같은 상황인데 이번 사이클 전수 감사가 놓쳤다 | SK-04 |
| `react-kit/skills/react-init/SKILL.md` · `react-run/SKILL.md` | `react-init:61` ~ `:88` 단계 2 · `:203` · `react-run:21` · `templates/vite.config.template.ts:24` ~ `:28` (`port: 5173` · `strictPort: true`) | react-init 이 템플릿을 쓰지 않아 `strictPort` 가 실제 프로젝트에 안 들어간다 — 두 자리의 「템플릿이 strictPort: true 라」 단정이 틀리다 | SK-05 |
| `reflect-kit/docs/SCHEMA.md` · `DESIGN.md` | `SCHEMA.md:123` §3 · `:145` · `DESIGN.md:172` · `:189` · 훅 `log-reflection.sh:147` · `:149` | 훅이 적는 `warn:lemma-map-unreadable` · `vocab:…` 가 두 문서 태그 목록에 없다 (손으로 센 답 2) | SK-06 |
| `bambu-kit/skills/bambu-print-profile/SKILL.md` | `:1600` 완료 검사 · `:1892` ~ `:1898` 음성 대조 블록 (1) · `:1992` ~ `:1994` 빈 목록 변이 · `:2015` | enum 줄만 빠진 목록이면 enum 검사가 조용히 꺼지고 `RESULT: PASS`. (1) 은 폴더 → 표 · 실행 줄 한 방향만 본다 | SK-07 |
| `onboarding-kit/skills/setup-guide/SKILL.md` · `evals/evals.json` | `SKILL.md:198` Gotcha 8 의 1 번 · `:202` 값 든 `.env` 문단 · `evals.json:124` | Grep 목록에 `.env*` · `**/*.p8` 이 있다(내용이 출력된다). 평가 항목이 여전히 `.env` 를 기준으로 삼는다 | SK-08 (a)(b) |
| `docs/onboarding-kit/examples/fcm-ios-setup-guide.md` | `:5` · `:28` ~ `:31` · `:46` · `:370` · `:381` · `:384` · `:385` · `:392` | 낡은 Xcode · iOS 값, 근거 없는 시뮬레이터 수신 주장 셋, 막는 요구가 한 줄, 특정 앱 이름 다섯 줄 | SK-08 (c) |
| `tone-kit/references/core-antipatterns.md` | `:22` 2 단계 「E · F · I 는 grep 으로」 · `:36` E 행 grep 칸 · `:110` E 절 코드 블록 | 표 칸이 `\|` 로 적혀 붙여 넣으면 0 줄 — 죽은 검사 | SK-09 |
| `api-kit/skills/api-ui/SKILL.md` · `api-verify/SKILL.md` · `docs/api/contract/snapshot-sealing-canonicalization.md` | `api-ui:168` · `api-verify:117` · `api-probe:183`(대조용) · 캐노니컬 `:35` · `:74` ~ `:81` 수치 기준 표 | 서버를 앞에서 띄워 셸이 묶인다 · 포트가 차 있을 때 할 일이 없다. api-verify 목록에 Infinity · binary64 가 없다. 수치 기준 표에 `-0` 행이 없다 | SK-10 |
| `howto-kit/evals/run-evals.sh` · `README.md` · `evals/evals.json` | `run-evals.sh:34` 한 글자 변수 · `:129` `bash` 펜스만 · `README.md:122` · `evals.json:3` | `sh` 펜스 블록은 수 대조와 실행에서 함께 빠진다 | SK-11 |
| `backend-kit/skills/backend-audit/references/audit-criteria.md` · `backend-system/references/system-principles.md` · `docs/backend/fundamentals/api-design.md` | `audit-criteria:20` · `system-principles:21` · `api-design:35` 원칙 3 · `:102` 수치 표 | 다섯 필드 필수를 RFC 9457 요구로 적었다 — 같은 레포 `docs/api/contract/error-status-contracts.md:25` 는 `type` 누락을 위반으로 보지 않는다. 원칙 3(`:35`)은 이 킷 규칙으로 다섯 필드를 요구한다 | SK-12 (a) (Codex r2-1) |
| `infra-kit/skills/infra-test/SKILL.md` | `:253` 규칙 1 · `:255` `grep -q 'actions/checkout'` | 주석 한 줄 `# uses: actions/checkout@v4` 로도 PASS (실행 재현) | SK-12 (b) (Codex r2-5) |
| `rust-kit/skills/rust-preflight/SKILL.md` | `:16` Gotcha 2 · `:34` · `:50` ~ `:51` Step 1 · `:158` 결과 표 `FIXED` | `:34` 만 「사용자에게 안내」 — 나머지 셋은 자동 적용 | SK-04 둘째 줄 (Codex r2-6) |
| `design-kit/references/visual-change-protocol.md` | `:369` ~ `:385` 스키마 · `:387` · `:389` 두 줄 규칙 · `:404` ~ `:440` 게이트 | 표면 없는 결정이 `decisions=1 surfaces=0 violations=0` · 종료 코드 0 (실행 재현). id 형식 · source · 이유 없는 제외도 안 본다 | SK-03 (d) (Codex r2-2) |
| `react-kit/skills/react-l10n/SKILL.md` | `:173` `grep -c '^-msgid '` | 지워진 키 0 개에서 종료 코드 1 (실행 재현) | SK-05 넷째 줄 (Codex r2-8) |
| `reflect-kit/hooks/_lib-project-id.sh` · `evals/hooks/collect-status-test.sh` | `lib:167` ~ `:211` `collect_status` · `:207` 경고 조건 · `test:101` 「7 일 · 두 폴더」 | 엔트리가 하나라도 있으면 기간 도중 멈춤을 못 잡는다 | SK-06 (c) (Codex r3-1 · 교차 진단 P12 결함 1) |
| `reflect-kit/skills/reflect-digest/SKILL.md` · `reflect-kaizen/SKILL.md` | `digest:35` Gotcha 13 · `:122` · `:126` · `:180` · `:183` · `:254` · `:314` · `kaizen:63` · `:68` | 실행 줄이 7 · 30 으로 고정돼 `period=30d` · `window=60d` 가 잘린다 | SK-06 (d) (Codex r3-2) |
| `bambu-kit/skills/bambu-print-profile/SKILL.md` | `:354` · `:2191` `S="$SKILL_DIR/SKILL.md"` · `:2446` 댓글 받기 블록 · `:2473` glob 집계 | 정의 안 된 `SKILL_DIR` 로 빈 코드를 돌아 `IndexError` (실행 재현) · 앞 실행 페이지가 섞여 `받은 hits 61 (페이지 2)` (가짜 curl 재현) | SK-07 (d)(e) (Codex r3-4 · r3-5) |
| `onboarding-kit/skills/setup-guide/SKILL.md` | `:60` ~ `:67` G1 | 한 Step 에 출처 둘 · 다른 Step 에 0 이 `G1_LEDGER PASS steps=2 ledger=2` (실행 재현) | SK-08 (d) (Codex r3-3) |

고칠 내용 — 정확한 문장은 조건 줄과 `m.sh` 토큰이 기준이다. 예행 도구 `mock.py`(스크래치 `kaizen/f1kit/`, sha256 앞 16 자리 `9e8da262a81720a3`)가
시작 커밋 판에 그대로 적용해 본 판이다(킷 이름 인자를 주면 그 킷만 적용한다). BUILD 는 이 파일을 편집 명세로 쓴다.

1. **연구 기록 넷** — 2026-09-24 항목 안에서 옛 항목과 이름이 같은 소제목 여덟 끝에 ` — 2026-09-24 사이클` 을 붙인다(backend 넷 · infra 둘 · rust 하나 · planning 하나). 다른 줄은 고치지 않는다.
   **backend** — 감사 기준 `:20` · 원칙 문서 수치 표 `:102` · 시스템 원칙 표 `:21` 의 「필수」 를 「다섯 필드를 모두 넣는 것은 이 킷 규칙 — RFC 9457 은 `type` 이 없으면 `about:blank`」 로. 원칙 3 본문(`:35`)의 킷 규칙은 그대로
2. **flutter-toolkit** — project-detection 표 두 행을 「단계마다 위 행의 타겟 — codegen 은 flutter-run codegen 절 블록 안의 `$MAKE app-codegen`」 으로, `:59` 를 묶음 타겟을 넣지 않는 이유 문장으로.
   규약 증거 블록 빈칸 넷을 `[미검증] — 네 칸은 아래 미검증 줄` 로, 규약 판 1.2.1. 두 스킬 실패 틀 codegen 줄에 삭제 줄과 늘어난 삭제 목록 줄. flutter-l10n Gotcha 를 Step 6 표를 가리키는 문장으로
3. **design-kit** — design-component Gotcha 13(규약 인용 — 숫자를 다시 적지 않는다). README 버전 줄을 「버전은 `.claude-plugin/plugin.json` 의 `version` 을 본다.」 로.
   결정 전파 게이트가 결정마다 id 형식(`DEC-YYYYMMDD-NNN`) · `source` 가 없으면 `SCHEMA_ERROR`(종료 코드 2), 두 표면 목록이 다 비거나 제외에 `reason` 이 없으면 `FAIL`(1), 표면 0 개면 `NO_SURFACE`(3).
   `status` 값 목록은 규약에 없어 보지 않는다
4. **infra-kit** — taxonomy `:42` 「적용된다」 → 「해당한다」 (infra-audit Gotcha 12 와 같은 말). infra-test 규칙 1 을 `uses:` 키 줄만 세는 식으로(주석 줄 제외) · 이유 주석 한 줄
5. **rust-kit** — 두 자리 `[미검증]` 에 네 칸(막는 것 · 시도한 우회 · 통제 불가 사유 · 재검증 명령). rust-preflight `:34` 를 Gotcha 2 · Step 1 과 같은 한 가지(먼저 `--check`, 실패하면 적용 뒤 다시 검사 · `FIXED` 보고)로
6. **react-kit** — react-l10n 지워진 키 수 명령을 `awk '/^-msgid /{n++} END{print n+0}'` 로. react-init 단계 2 끝에 `server: { port: 5173, strictPort: true },` 블록과 이유 한 문단(템플릿 `server` 블록과 같은 값). `:203` 주석과 react-run Gotcha 문장을 「단계 2 에서 넣은」 으로 고치고, 그 설정이 없는 프로젝트는 `pnpm vite dev --strictPort` 로 띄운다고 적는다. Gotcha 머리 글은 그대로 둔다(규약이 그 머리 글로 가리킨다)
7. **reflect-kit** — SCHEMA §3 · DESIGN 에러 관측성 목록에 두 태그 줄. README 버전 줄은 design-kit 과 같은 문장. `collect_status` 가 마지막 기록 시각을 먼저 구하고 그 뒤의 Stop 실패 시도를 따로 세어,
   엔트리가 있어도 1 이상이면 `⚠ 수집 멈춤 — 마지막 기록 뒤 Stop 실패 시도 N회` 를 낸다(엔트리 0 경고가 먼저다). 시험에 그 경우 하나(`b4`). reflect-digest 두 실행 줄 · reflect-kaizen 한 실행 줄의
   고정 일수를 `<일수>` 로, digest Gotcha 13 · 요약 규칙 두 자리에 새 경우
8. **bambu-kit** — 두 자기 검사 블록 첫 줄을 `SKILL_DIR=<이 스킬의 기준 폴더>` 로 두고 `S` 가 없으면 `STOP` 으로 멈춘다. 댓글 받기 블록이 `mkdir -p` 뒤에 앞 실행의 `comments-*.json` 을 지운다. 완료 검사 조건에 `or not ENUM` 과 알림 문구의 enum 수. 음성 대조 블록 (1) 에 반대 방향(표 행 · 실행 줄의 이름 → 폴더) 확인 `ORPHAN` 과 두 목록을 함께 보고하는 멈춤. 빈 목록 변이 뒤에 enum 없는 목록 변이 네 줄(설치된 BambuStudio 판 목록에서 enum 줄만 뺀다)과 그 결과 설명 한 줄
9. **onboarding-kit** — `guide_gate` G1 이 전체 수 비교 뒤에 Step 마다 출처 줄이 정확히 하나인지 세어 아니면 `G1_LEDGER FAIL … misplaced=N` (PASS 줄 모양은 그대로). Gotcha 8 의 1 번 Grep 목록에서 `.env*` · `**/*.p8` 을 빼고 「Glob 으로 있는지만 본다」 문장. 평가 항목 한 줄을 `.env.example` 기준으로(`setup.env_contains` 는 그대로 — 값 든 `.env` 가 있어야 「열지 않는다」 를 잰다). 예제: 기준 줄 · Xcode 26.2+ · 막는 요구 표(형식 문서 §2 세 행 그대로) · 시뮬레이터 세 줄 · 앱 이름 다섯 줄
10. **tone-kit** — E 행 grep 칸을 「아래 E 절의 grep 블록 — 대안 기호가 든 식은 표 칸에 옮기면 깨져서 옮기지 않는다」 로
11. **api-kit** — api-ui 여는 방법: 폴더 만드는 명령과 `&` 로 뒤에서 띄우는 명령을 나누고, 앞에서 띄우면 묶인다 · `Address already in use` 일 때 할 일.
    서버 명령의 폴더 변수는 `${D:?…}` 로 막고, 두 명령을 한 번의 셸 호출에서 잇는다는 문장을 둔다 — 명령마다 새 셸이 뜨는 도구에서 `$D` 가 비면 지금 폴더(`.api/` 포함)가 열린다(검토 C5).
    서버 명령 끝에 1 초 뒤 판정 줄(`SERVING pid=… dir=…` · `NOT_SERVING`)을 찍어 포트 충돌을 같은 호출 안에서 가르고, 내릴 때는 그 줄의 번호로 `kill` 한다 — 다른 셸 호출의 `kill $!` 는 서버를 못 내리고 zsh 에서는 `kill 0` 이 된다(검토 2 회차 R1). api-verify 목록에 `NaN/Infinity` · `binary64 로 표현 못 하는 숫자`. 수치 기준 표에 `-0` 행
12. **howto-kit** — 러너가 `bash` · `sh` · `shell` · `zsh` 펜스를 센다(주석 한 줄) · `for entry in data['cases']`. README · `evals.json` 설명의 「`bash` 블록」 을 「셸 블록」 으로

하지 않기로 한 것 (입력 항목 표의 「고치지 않음」 과 같은 것 가운데 설계 판단이 든 넷):

- reflect-kit 새 `⚠ 수집 멈춤` 줄은 수 문턱 없이 시각 순서(마지막 기록 뒤에 실패가 있는가)로 가른다 — 몇 회 · 며칠로 가를 근거가 없다. 그 줄은 digest `## 승격 후보` 를 비우는 문턱이라
  마지막 실행 한 번의 일시 실패에도 후보가 비는 쪽으로 기운다. 수집이 멈춘 채 후보를 내는 것보다 덜 위험하다고 봤다 — 너무 자주 나오면 다음 사이클 Phase 12 가 문턱을 정한다(notes 메모)
- api-kit 뷰어에 「판정 불가」 상태를 더하지 않는다 — 뷰어 상태 셋은 기준 시안 `.mockups/api-ui-v7.html` 과 맞춰야 하는데 그 시안이 `.gitignore` 라 이 작업 폴더에 없다. 사용자 확인이 먼저다
- `docs/superpowers/specs/2026-09-02-api-kit-design.md:249` 를 고치지 않는다 — 날짜 붙은 설계 기록이라 이 계약 범위(킷 폴더 · 킷 원본 문서 폴더)가 아니고 결론(후처리)은 맞다. Phase 14 가 `docs/onboarding-kit/plan-2026-05-18.md` 옛 호스트를 역사 문서라 둔 것과 같다
- bambu 음성 대조 블록을 고치면 올리지 않은 가지 `feat/bambu-kit-orca-h2s-feedback` 과 충돌할 자리가 는다 — 막지 않고 notes 에 적는다(Phase 13 notes 가 같은 가지 충돌을 이미 적었다)
- design-kit · planning-kit reviewer 의 미검증 사본(Codex r2-3 · r2-4)을 이번에 옮기지 않는다 — 기준 원본 `qa-evaluation-guide.md` §Canonical Unverified-Evidence Protocol 이 1 · 2 · 3 · 3 · 4 · 5 여섯 항목이라
  (`:1236` · `:1250` · `:1267` · `:1274` · `:1280` · `:1285`) reviewer 들이 적은 「5 조항 문구 변형 없이」 가 지금은 성립하지 않는다. 같은 옛 사본이 react-kit · api-kit reviewer 에도 있고(`임계값은 2 다` 각 1 줄),
  옮기면 design-audit · plan-audit 의 REJECT 문턱까지 같이 바뀐다(Phase 6 · 11 notes 「미반영」). 기준 원본 정리(harness 쪽)가 먼저라 다음 사이클 Phase 3 뒤 킷 넷을 한 번에
- api-kit `-0` 을 「I-JSON 게이트」 에서 떼어 이름을 나누지 않는다(Codex r3-6) — 「RFC 7493 은 `-0` 을 금지하지 않는다」 는 근거 파일에 없는 바깥 문서 주장이다(`phase16.md:37` S12 는 RFC 7493 상태만 적었다).
  킷의 `-0` 줄은 이유를 JCS 로 적었다(`api-contract/SKILL.md:67`). SK-10 (b) 는 세 자리 목록을 같게 맞추는 일이라 그대로 둔다
- onboarding G1 음성 입력(한 Step 에 출처 둘)을 킷 픽스처로 넣지 않는다 — 새 파일과 `gate_cases` 등록이 함께 필요하다. 이 계약은 SK-08 (d) 가 임시 파일로 재고, 킷 러너 등록은 다음 사이클 Phase 14(notes 메모 `misplaced`)

## 범위 경계

- 이 계약 시작 HEAD: `5b4fd72d5587c937c1875ddb62872f32ae087dcf` (이 계약 착수 때 `git rev-parse HEAD` 출력). 범위 상한은 개정 파일 `.harness/sprint-amendments-kaizen-0924-f1-kit-followups.md` 의
  `end_sha:` 마지막 값이다. `kaizen-0924-f1-harness-followups` 가 같은 가지 `kaizen/2026-09-24` 에 동시에 커밋하므로 `HEAD` 로 재지 않는다
- 연구 기록 경고 비교 기준은 사이클 개시 커밋 `7689fde`(카이젠 2026-09-24 사이클 개시 — 데이터 풀 · 근거 파일만 더한 커밋)다. 킷 파일은 그 부모 `83cfb4f` 와 같다
- 고치는 파일은 마흔하나이고 새 파일은 없다 — 아래 블록이 그 목록이다(`harness/README.md` §커밋 안전 훅 이 정한 범위 선언 자리). `.harness/` 쪽은 이 계약 · 개정 파일 · QA 피드백 ·
  `.harness/.meta/kaizen-0924/f1-kit-followups-notes.md` · `.harness/.meta/kaizen-0924/f1-kit-followups-review.md` 를 쓴다 — AR-01 둘째 값이 이 계약 이름이 든 허용 갈래로 잰다
  (다른 계약 슬러그는 나열하지 않는다). 허용 목록은 이 계약 서명 커밋에만 걸어서, 앞 스프린트의 status 전환이 구간에 들어와도 걸리지 않는다. 넷째 값 `verify_seal` 은 봉인이 깨졌는지만 잰다.
  Phase 7 · 8 · 9 · 11 개정 파일의 「교차 진단 뒤 Final 에서 고침」 줄은 `kaizen-0924-final` 이 붙인다 — 이 계약은 notes 에 sha 만 적는다.
  AR-01 여섯째 값이 이 블록과 측정 공통 정의의 `FILES` 가 같은지 잰다

```text
# sprint-scope
docs/backend/research-log.md
backend-kit/skills/backend-audit/references/audit-criteria.md
backend-kit/skills/backend-system/references/system-principles.md
docs/backend/fundamentals/api-design.md
docs/infra/research-log.md
infra-kit/references/gate-result-taxonomy.md
infra-kit/skills/infra-test/SKILL.md
docs/rust/research-log.md
rust-kit/skills/rust-audit/SKILL.md
rust-kit/skills/rust-model/SKILL.md
rust-kit/skills/rust-preflight/SKILL.md
docs/planning/research-log.md
flutter-toolkit/references/project-detection.md
flutter-toolkit/references/visual-evidence-protocol.md
flutter-toolkit/skills/flutter-build/SKILL.md
flutter-toolkit/skills/flutter-preflight/SKILL.md
flutter-toolkit/skills/flutter-l10n/SKILL.md
design-kit/skills/design-component/SKILL.md
design-kit/README.md
design-kit/references/visual-change-protocol.md
react-kit/skills/react-init/SKILL.md
react-kit/skills/react-run/SKILL.md
react-kit/skills/react-l10n/SKILL.md
reflect-kit/docs/SCHEMA.md
reflect-kit/docs/DESIGN.md
reflect-kit/README.md
reflect-kit/hooks/_lib-project-id.sh
reflect-kit/evals/hooks/collect-status-test.sh
reflect-kit/skills/reflect-digest/SKILL.md
reflect-kit/skills/reflect-kaizen/SKILL.md
bambu-kit/skills/bambu-print-profile/SKILL.md
onboarding-kit/skills/setup-guide/SKILL.md
onboarding-kit/skills/setup-guide/evals/evals.json
docs/onboarding-kit/examples/fcm-ios-setup-guide.md
tone-kit/references/core-antipatterns.md
api-kit/skills/api-ui/SKILL.md
api-kit/skills/api-verify/SKILL.md
docs/api/contract/snapshot-sealing-canonicalization.md
howto-kit/evals/run-evals.sh
howto-kit/README.md
howto-kit/evals/evals.json
.harness/
```

- **이 계약의 커밋 메시지에는 전부 `Co-Authored-By` 줄 바로 위에 서명 줄 `Kaizen-Phase: kaizen-0924-f1-kit-followups` 한 줄을 넣는다** (봉인 커밋 포함).
  AR-01 · ER-03 · SC-00 · DG-01 · DG-06 이 이 줄로 이 계약 커밋을 가린다(`harness/references/contract-schema.md` §여러 주체가 한 가지에 커밋할 때 선택지 B).
  서명을 빠뜨린 커밋은 서명 줄 목록에 안 보이므로 AR-01 첫째 값은 경로로 직접 센다. FIX 가 커밋을 더할 때도 넣고, 개정 파일에 `end_sha:` 줄을 덧붙인다(옛 줄은 지우지 않는다).
  notes 커밋도 이 계약 커밋이다 — notes 를 커밋한 뒤 그 sha 로 `end_sha:` 줄을 하나 더 덧붙여 커밋한다
- **한 커밋에 킷 하나** (Final 지침). 구현 커밋은 킷 묶음마다 하나씩 열셋이다 — 묶음 이름과 경로는 측정 공통 정의의 `KITG` · `GPATH` 다:
  `backend`(`backend-kit/` · `docs/backend/`) · `infra`(`infra-kit/` · `docs/infra/`) · `rust`(`rust-kit/` · `docs/rust/`) · `planning`(`docs/planning/`) · `flutter` · `design` · `react` · `reflect` · `bambu` ·
  `onboarding`(`onboarding-kit/` · `docs/onboarding-kit/examples/`) · `tone` · `api`(`api-kit/` · `docs/api/`) · `howto`. 커밋마다 `git add -- <그 묶음 파일> && git commit -o -- <그 묶음 파일>`.
  구현 커밋은 `.harness/` 를 함께 싣지 않는다(AR-01 셋째 값). 러너 `howto-kit/evals/run-evals.sh` 는 git 모드 `100755` 를 그대로 둔다
- notes `.harness/.meta/kaizen-0924/f1-kit-followups-notes.md` 에 적는 것 (ER-03 이 잰다):
  `## 커밋` — `| <묶음 이름> | <커밋 sha> |` 로 시작하는 표 행 열셋 · `## 다룬 항목` · `## 고치지 않은 항목과 이유` (아래 입력 항목 표의 「고치지 않음」 전부) ·
  `## Final 에 넘기는 것` — (a) Phase 7 · 8 · 9 · 11 개정 파일에 붙일 「교차 진단 뒤 Final 에서 고침 — 커밋 sha」 네 줄(각 줄에 그 Phase 슬러그와 그 묶음 커밋 sha)
  (b) 버전 계획 — 플러그인 파일이 바뀐 킷 열둘(`backend-kit` · `flutter-toolkit` · `design-kit` · `infra-kit` · `rust-kit` · `react-kit` · `reflect-kit` · `bambu-kit` · `onboarding-kit` · `tone-kit` · `api-kit` · `howto-kit`, 고침만이라 patch)
  (c) 다시 만들 문서 사이트 페이지 아홉(`fcm-ios-example.html` · `visual-evidence-protocol.html` · `project-detection.html` · `snapshot-sealing-canonicalization.html` · `gate-result-taxonomy.html` · `api-design.html` · `visual-change-protocol.html` · `bambu-print-profile.html` · `schema.html`) ·
  `## 다음 사이클 메모` — 아래 표 「고치지 않음」 가운데 다음 사이클로 가는 것. ER-03 이 토큰 열로 잰다: `claude -p` · `판정 불가` · `adapter-dart-flutter.md` ·
  `widget-inspector` · `fit-pal` · `2026-09-02-api-kit-design.md` · `flutter-preflight` · `G91` · `locale-korean.md` · `design-reviewer` · `planning-reviewer` · `2.7.0` · `RFC 7493` · `misplaced` · `harness-project.yaml.template` · `docs/infra/platform/cicd.md` · `build_runner-2.13.1`.
  reflect 새 경고 줄이 자주 나오면 문턱을 정한다는 메모도 여기 적는다. notes 에 URL 을 적으면 근거 파일에 있는 것만(ER-01 둘째 값)
- 측정이 기대는 제목 · 줄 머리는 이름을 바꾸지 않는다: 연구 기록 넷의 `## [2026-09-24]` 항목 머리 · design-component `# Gotchas` · `# Process` · react-init `### 단계 2 ` · react-run
  Gotcha 머리 `` - **`dev` 포트는 5173 에 묶여 있다 (`strictPort: true`)**: `` · reflect `## 3. ` · `## 에러 관측성` · bambu `# (1) 폴더의 시험 파일이` 줄 · `^TARGET_SLICER=.* python3 - ` 줄과 닫는 `PY` ·
  onboarding `1. **패턴으로 탐색한다**` · `guide_gate() {` · tone `## 카테고리 요약표` · `### E ` · api-ui `1. **여는 방법**` · howto README `## 결정론 게이트 G1~G6` ·
  flutter-l10n `### 6. Codegen 실행` · 형식 문서 `### 2. ` 와 세 행 머리(`| 실기기 |` · `| 유료 개발자 계정 |` · `| 앱 출시 |`) ·
  design 게이트 docstring `"""Decision Propagation Coverage Gate` · infra-test `# 규칙 1: checkout 스텝 존재` 와 그 루프를 닫는 `done` · rust-preflight `2. **fmt 실패 시 자동 적용**` ·
  react-l10n `git diff -U0 -- src/infrastructure/i18n/locales/ | ` 로 시작하는 두 줄 · reflect `collect_status() {` · 시험 끝 줄 `결과: ` · onboarding `  # G1 출처 원장 완전성` · `  # G2 미검증 마커` ·
  bambu `S="$SKILL_DIR/SKILL.md"` 두 줄 · `ID=<모델 번호>; OUT=<output_dir>/makerworld;` 줄 · 댓글 집계 줄 `comments total `
- 공유 파일(`.claude-plugin/marketplace.json` · 킷 `plugin.json` 버전 · 루트 `README.md` · 루트 `CLAUDE.md` · `docs/` HTML · `docs/index.html` · `docs/kaizen/` · 처리 배정표 · 감사 기록 ·
  실패 횟수 파일 · `.github/workflows/ci.yml` · `.harness/stale-values.yaml`)과 다른 계약 범위(`harness/` · `scripts/` · `.claude/skills/`)는 건드리지 않는다 — ER-03 마지막 값 · AR-01 둘째 값.
  킷 README 셋은 킷 전용 문서라 고친다 — AUTO 구간이 읽는 frontmatter · 파일 목록은 그대로다(AP-04 · DG-05 `sync_rc`). 문서 사이트 재생성은 `kaizen-0924-final` F2 몫이라 DG-06 에서 `docs-site-regen` 을 뺀다
- QA(`harness:qa-evaluator`)는 설치본이다 — 이 계약이 고치는 파일에 qa-evaluator 는 없다
- 사용자 승인(Step 5) 대체: 사용자가 「자동으로 끝까지 알아서 진행해 내 허락이 필요한건 코덱스로 리서치나 검토받고」라고 위임했다(세션
  `de8c7935-a5b6-4df5-9106-fafa73c288a0` 기록 queued_command `2026-09-24T04:04:16.964Z`). Codex 사용량 한도가 소진돼(오류 원문 「You've hit your usage limit … try
  again at 11:05 PM」, 2026-09-24) 독립 Claude 검토자(REVIEW 에이전트)가 대신한다. 이어 사용자가 「코덱스 대신에 그냥 너가 알아서 진행하라고」라고 명시했다(같은 세션
  기록 user `2026-09-24T11:54:58.940Z`). 검토 결과 파일: `.harness/.meta/kaizen-0924/f1-kit-followups-review.md` (검토자가 쓴 파일) — 1 회차 판정 `VERDICT: CHANGES`.
  고칠 것 여덟(C1 ~ C8)은 DRAFT 가 이 초안에 넣었다. 같은 파일 `## 2 회차` 의 마지막 판정도 `VERDICT: CHANGES` 다 — C1 ~ C8 이 모두 반영됐다고 확인하고
  새 고칠 것 둘(R1 api-ui 를 뒤에서 띄우면 포트 충돌 알림이 도구 출력에 안 실리고 다른 셸 호출의 `kill $!` 가 서버를 못 내린다 · R2 옛 파일 수 「서른」 두 자리)을 냈다.
  BUILD 가 봉인 전에 둘 다 넣었다 — R1 은 검토가 준 글자 그대로 `mock.py` api 갈래(서버 명령 · 판정 줄 문장 · 내리는 문장) · GAP 개선안 11 · SK-10 (a) 본문 · m.sh `SK-10)` 첫 줄 토큰과 `api_serve` 출력 줄 · 기대값 · `del.sh` 토큰에,
  R2 는 두 자리에. SK-10 은 시작 커밋 판 · 예행 판 · 2 회차 전 초안 명령에서 다시 재어 봉인 전 실측 표에 적었다(검토 표의 세 판 값과 같다). 반영하지 않은 지적은 없다.
  새 측정은 SK-10 한 조건이고 검토가 준 측정 설계 그대로라 3 회차 검토는 돌리지 않았다
- Codex 독립 검토: 사용자가 「코덱스도 사용할 수 있으니깐 사용해」라고 했다(같은 세션 기록 user `2026-09-25T06:19:45.056Z`). 그래서 이 가지의 킷 쪽 변경을 Codex(`gpt-5.6-sol`, 읽기 전용)가
  두 묶음으로 검토했다 — 결과 `scratchpad/kaizen/codex/r2-kits-a.md`(8 건) · `r3-kits-b.md`(6 건). 이 초안은 그 지적을 다시 확인해 반영한 판이고, 봉인 전 REVIEW 에이전트 검토는 그대로 받는다
- 판정 한계: 스킬을 부르는 모델이 새 문장대로 실제로 움직이는지(서버를 뒤에서 띄우는지 · `.env*` 를 Glob 으로만 보는지 · `strictPort` 줄을 실제 프로젝트에 넣는지)는 결정론 측정이 없다 —
  조건은 그 문장이 정해진 자리에 글자 그대로 있는지와, 블록 · 러너 · 완료 검사처럼 실제로 돌릴 수 있는 것은 돌린 결과를 잰다. bambu 완료 검사와 음성 대조 블록 (c) 는 설치된
  BambuStudio(`02.08.02.61`)가 있어야 돈다 — 없으면 `TOOL_MISSING BambuStudio` 로 멈춘다. api-ui 서버 대조는 비어 있는 포트 번호로 바꿔 돈다(이 맥에서 8765 가 쓰일 수 있다).
  bambu 댓글 받기 블록은 네트워크 대신 가짜 `curl`(주소별 JSON · 상태 200)로 돈다 — MakerWorld 응답 모양은 재지 않고 폴더 정리만 잰다. design 결정 게이트 대조는 PyYAML(`6.0.3`)이 있어야 돈다
- 판정 근거: SK-01 · DG-02 — 편집기와 같은 조건(markdownlint-cli2 0.23.2 · MD013 끔)으로 파일마다 규칙별 경고 수를 두 판에서 비교한 출력이다. 더한 줄만 보지 않는다 — MD022 · MD032 · MD024 는
  더한 줄 옆의 손대지 않은 줄에 붙는다(러닝북 측정 구멍 목록 · 교차 진단 P7 · P8 · P9 · P11)
- 판정 근거: SK-02 ~ SK-06 (문장 줄) · SK-08 (a)(b) · SK-09 끝 값 · SK-10 (b)(c) · SK-11 첫 줄 · SK-12 (a) · AR-02 — 산출물이 문서 문장 자체라 정해진 자리에 정해진 문장이 있는지가 판정이다. 토큰은 문장 전체라
  예행 판 값이 1 인 토큰은 그 줄만 지운 사본에서 0 이 된다(같은 파일에 두 번 나오는 토큰이 없다). 시작 커밋 판 값이 같은 측정의 양성 대조다
- 판정 근거: SK-03 (d) · SK-05 넷째 줄 · SK-06 (c) · SK-07 · SK-08 (c)(d) 검사 함수 줄 · SK-09 · SK-10 (a) · SK-11 · SK-12 (b) · DG-04 — 끝 판 문서에서 블록 · 함수 · 킷 시험을 뽑아 실제로 돌린 출력이다.
  시작 커밋 판에서 같은 측정이 결함을 드러낸다(봉인 전 실측 절)
- 판정 근거: ER-01 · ER-02 · AP-01 · AP-03 · DG-05 (d) — 마흔한 파일을 파일마다 편집 전 판과 비교한 계산이다. ER-01 은 파일마다 편집 전 판에 없던 URL 을 센다 — 고친 줄에 원래 있던 URL
  (backend 감사 기준 `:20` 의 RFC 9457 주소 등)은 새 URL 이 아니고, 다른 파일에서 옮겨 온 URL 은 새 URL 이다. 근거 파일은 시작 커밋 판에서 읽는다(끝 판은 `.harness/` 안이라 바뀔 수 있다)
- 판정 근거: ER-03 · AR-01 · SC-00 · DG-01 · DG-06 — 커밋 기록과 봉인 검증 함수를 실제로 돌린 출력이다. 예행 저장소 변형 열이 양성 · 음성 대조다
- 커버리지 해소: SK-02 · SK-03 · SK-05 · SK-06 · SK-08 · SK-11 · AR-03 — 산문의 파일 이름(`project-detection.md` · `visual-evidence-protocol.md` · `design-kit/README.md` · `SCHEMA.md` · `DESIGN.md` ·
  `reflect-kit/README.md` · `evals.json` · `docs/onboarding-kit/examples/fcm-ios-setup-guide.md` 등)은 측정 `m <조건 ID>` 가 공통 정의의 변수(`$RLB` · `$RLI` · `$RLR` · `$RLP` · `$TAX` · `$RAU` · `$RMO` · `$FPD` ·
  `$VEP` · `$FBU` · `$FPR` · `$FLN` · `$DCO` · `$DRD` · `$RIN` · `$RRU` · `$RSC` · `$RDE` · `$RRD` · `$BAM` · `$OSK` · `$OEV` · `$OEX` · `$TAP` · `$AUI` · `$AVE` · `$ACN` · `$HRN` · `$HRD` · `$HEV`)로 연다
  (파일과 변수의 대응은 `common.sh` 머리 — 이번에 더한 `$BAC` · `$BSP` · `$BAD` · `$ITS` · `$RPF` · `$DVP` · `$RLN` · `$RLIB` · `$RCT` · `$RDG` · `$RKZ` 포함). 그 밖의 경로(`visual-change-protocol.md` · `templates/vite.config.template.ts` · `reflect-kit/hooks/*.sh` · `format-checklist.md` · `skills/howto/SKILL.md`)는
  같은 ID 갈래가 경로를 적어 연다. `1.2.1` 은 SK-02 갈래가 `^version: 1.2.1$` 로, `.env.example` · `.p8` · `**/*.p8` 은 SK-08 갈래의 토큰으로 센다
- 커버리지 해소: SK-01 — `.claude/` · `.harness/` · `docs/kaizen/` · `harness/` 는 대상이 아니라 SK-01 갈래가 목록에서 빼는 접두(`grep -v`)이고 `m.sh` 는 측정 도구 이름이다
- 커버리지 해소: SK-03 · SK-06 · SK-12 — `decisions.yaml` 입력 다섯은 `dg_inputs` 가 만든다(`gate-exit-codes.md` 는 기대 종료 코드의 출처). `collect-status-test.sh` · `_lib-project-id.sh` 는 `$RCT` · `$RLIB`,
  `docs/api/contract/error-status-contracts.md` 는 SK-12 갈래가 경로를 적어 연다. `audit-criteria.md` · `system-principles.md` · `api-design.md` 는 `$BAC` · `$BSP` · `$BAD`, `actions/checkout` 입력 셋은 `infra_ci_inputs` 가 만든다
- 커버리지 해소: SK-07 · SK-10 — 픽스처 `process-thin-baseline.json` · `process-seam-slope-type-invalid.json` 은 SK-07 갈래가 경로를 적어 쓴다. `comments-*.json` · `SKILL_DIR` 은 `bambu_mw` · `bambu_selfblocks` 가 만들고 채우며, `S="$SKILL_DIR/SKILL.md"` 는 `bambu_selfblocks` 가 블록을 찾는 줄 머리다. `ui.html` 은 `api_serve` 가 만드는 시험용 파일 이름, `.api/` · `.api/credentials.local.json` 은 `api_unset` 이 만드는 시험용 폴더 · 파일,
  `snapshot-sealing-canonicalization.md` 는 `$ACN`, `NaN/Infinity` 는 SK-10 갈래 `toks` 의 인자다
- 커버리지 해소: ER-01 · ER-03 — `.harness/.meta/kaizen-0924/f1-kit-followups-notes.md` · `.harness/.meta/evidence/phase*.md` 는 공통 정의의 `$NOTES` 와 `ER-01)` 갈래의 근거 파일 경로다.
  ER-03 의 공유 경로(`.claude-plugin/marketplace.json` · `README.md` · `CLAUDE.md` · `.harness/.meta/orchestrator-audit-log.md` · `.harness/.meta/kaizen-failure-count.yaml` · `.claude/kaizen-input/insights-report.md` ·
  `.github` · `.harness/stale-values.yaml` · `.claude/skills` · `docs/index.html` · `docs/kaizen` · `docs/**/*.html` · `*/.claude-plugin/plugin.json`)는 `not_other` 의 인자, 메모 토큰(`2.7.0` ·
  `adapter-dart-flutter.md` · `2026-09-02-api-kit-design.md` · `locale-korean.md` · `harness-project.yaml.template` · `docs/infra/platform/cicd.md` · `build_runner-2.13.1` 등)은 `toks` 의 인자, 페이지 · 킷 이름(`api-design.html` · `visual-change-protocol.html` · `bambu-print-profile.html` · `schema.html` 포함)은 `ER-03)` 갈래의 목록이다. `commit_rows=11/13` · `harness/skills/` 는 양성 대조 변형의 값 · 경로다
- 커버리지 해소: AR-03 — `_lib-project-id.sh` 는 `$RLIB`(함수 밖 줄 대조 `cs_out`), `evals.json` 둘은 `$OEV` · `$HEV` 다
- 커버리지 해소: AR-01 — 첫째 값의 경로는 `AR-01)` 갈래가 넘기는 경로 조건(킷 폴더 `*-kit/` · `flutter-toolkit` · `docs/` 원본, HTML · `docs/kaizen` 제외)이고, 묶음 경로는 `GPATH`,
  `.harness/` 는 `scope` 블록 줄 · 둘째 값의 허용 갈래 정규식 · `verify_seal` 이 도는 폴더다. `planning-kit/README.md` · `.harness/sprint-amendments-kaizen-0924-p07-backend-kit.md` 는 양성 대조 변형이 고치는 파일이다. `harness/references/contract-schema.md` 는 넷째 값 권장 형태의 출처다
- 커버리지 해소: DG-05 — `.harness/stale-values.yaml` 은 DG-05 갈래 python 의 인자, `scripts/run-evals.py` · `scripts/validate-plugin.py` · `scripts/sync-docs.py` 는 같은 갈래가 돌리는 명령이다.
  `scripts/check-stale-values.py` 는 쓰지 않는 도구로 이름만 적었다. `3.1.1` 은 등록부의 `old` 값 하나라 갈래 python 이 등록부에서 읽는다. 시작 커밋 판에도 있던 옛 값 두 자리(backend 감사 기준 `:26` 의 `OpenAPI 3.1.1` 링크 글과 주소 — 3.1 의 `format` 동작을
  적은 인용이라 최신 판 표기가 아니다)는 등록부 `allow` 에 없어 세어진다 — 그래서 (d) 는 파일마다 시작 커밋 판보다 늘었는지 잰다. 등록부 `allow` 보강은 `kaizen-0924-final` 몫(입력 항목 표 22 행)
- 검출기는 공백 든 코드 조각 안의 인자를 읽지 못한다 — 위 해소 줄이 전부 그 경우다
- 편집 전부터 있던 경고(연구 기록의 옛 MD024 등)는 같은 수로 남으면 된다. SK-01 은 사이클 개시 판과, DG-02 는 시작 커밋 판과 파일마다 규칙별로 비교한다
- reflect `⚠ 수집 멈춤` 둘째 경우는 수 문턱 없이 시각 순서로 가른다 — `GAP 분석` 의 「하지 않기로 한 것」 첫째 줄. 기존 시험 열 경우는 그대로 통과해야 한다(SK-06 (c) 시작 커밋 시험 × 끝 판 라이브러리 대조를
  봉인 전에 돌렸다: `결과: 10 경우 중 불일치 0`)

입력 항목 표 — 「먼저 읽을 것」 가운데 킷 쪽에 닿는 항목 전부 (출처: FT = `final-todo.md`, XD = `xdiag-all.md` P 절 「계약 밖」 · 「(1)(2)」, N = Phase notes).
킷 범위 밖 항목은 마지막 행들에 묶었다.

| # | 입력 (출처) | 처리 |
| --- | --- | --- |
| 1 | DG-02 새 MD024 — backend 연구 기록 소제목 넷 (FT · XD P7 (1)) | 조건으로 다룸 — SK-01 |
| 2 | 같은 결함 — infra 연구 기록 `:69` · `:100` (FT · XD P8 (1)) | 조건으로 다룸 — SK-01 |
| 3 | 같은 결함 — rust 연구 기록 `:14` (FT · XD P9 (2)) | 조건으로 다룸 — SK-01 |
| 4 | 같은 결함 — planning 연구 기록 `:37` (FT · XD P11 (1)) | 조건으로 다룸 — SK-01 |
| 5 | P12 ~ 17 도 규칙별 비교로 전수 확인 (FT) | 조건으로 다룸 — SK-01 (c): 사이클 동안 바뀐 킷 쪽 마크다운 전부(P5 · P6 · P10 포함)를 사이클 개시 판과 비교 |
| 6 | P5 `project-detection.md:59` 묶음 타겟 (FT · XD P5 결함 1) | 조건으로 다룸 — SK-02 (a) |
| 7 | P5 `visual-evidence-protocol.md:151-154` 빈칸 넷 (FT · XD P5 (2) · 결함 2) | 조건으로 다룸 — SK-02 (b) |
| 8 | P5 flutter-build · flutter-preflight 실패 틀 삭제 줄 (FT · XD P5 결함 3) | 조건으로 다룸 — SK-02 (c) |
| 9 | P5 `flutter-l10n:15` slang 경로 (FT · XD P5 결함 5) | 조건으로 다룸 — SK-02 (d) |
| 10 | P5 `widget-inspector.md` §7 제목 · 본문 (XD P5 결함 4) | 고치지 않음 — P5 계약 SK-05 (c) 가 일부러 둔 자리이고, flutter-feature 가 표 없이 부르는 흐름을 바꿀지부터 정해야 한다 |
| 11 | P4 · P5 · P10 flutter-preflight · react-preflight 기준 커밋 비교 (N P4 · P5 · P10) | 고치지 않음 — 근거 파일에 기준 커밋 비교 근거가 없다(P5 · P10 notes 사유). 이 계약은 새 근거를 찾지 않는다 |
| 12 | P5 go_router · auto_route 새 내용 · `--delete-conflicting-outputs` · flutter-audit `:50` · codegen 안내 셋 · 평가 사례 18 `$DART test` (N P5) | 고치지 않음 — notes 가 다음 사이클 Phase 5 로 보냈다(새 내용 · 근거 없음 · 평가 측 형식 · 킷이 돌리지 않는 안내). 이 계약은 Final 로 넘어온 킷 몫과 교차 진단 결함만 다룬다. `--delete-conflicting-outputs` 는 Codex r2-7 과 같은 자리 — 73 행 |
| 13 | P6 design-component Gotcha 에 규약 인용 없음 (FT · XD P6) | 조건으로 다룸 — SK-03 (a)(b) |
| 14 | P6 RE-02 정규식 하이픈 (FT · XD P6 (2)) | 고치지 않음 — P6 계약 측정의 결함이지 킷 파일 결함이 아니다. 교차 진단 기록은 `kaizen-0924-final` 몫 |
| 15 | P6 임계값 다시 정의 (XD P6 · N P6 메모) | 고치지 않음 — 근본 해법(세 규약 공통 절)이 harness `skill-design-guide.md` 몫이라 다음 사이클 Phase 1 뒤 |
| 16 | P6 `design-kit/README.md` 버전 줄 (N P6 → Final) | 조건으로 다룸 — SK-03 (c) · AP-01 |
| 17 | P6 `docs/design/research-log.md` 킷 로그 옮기기 (N P6 → Final) | 다른 계약 몫 — `kaizen-0924-final` (`docs/*/research-log.md` 새 항목) |
| 18 | P6 design:P2 방향 · `UNVERIFIED_ENV` · design-mockup Step 0 · design-reviewer `[미검증]` 네 칸 · Material 3 · token-principles OKLCH (N P6) | 고치지 않음 — 사용자 확인 · 판정 문턱 변경 · 근거 없음(notes 사유). 다음 사이클 Phase 6. `UNVERIFIED_ENV` 는 Codex r2-3 과 같은 일 — 69 행 |
| 19 | P7 rust-model 시각 타입 대응 (N P7 → Phase 9) | 이미 반영 — `rust-kit/skills/rust-model/SKILL.md:35` Gotcha |
| 20 | P7 `infra-kit/README.md:54` 「7 카테고리 구조 감사」 (N P7 → Phase 8) | 이미 반영 — 그 문구 0 줄 |
| 21 | P7 OpenAPI 3.1 표기 · 벽시계 문자열 · 시간대 저장 · AsyncAPI 3.1.0 (N P7) | 고치지 않음 — 열린 질문 · 근거 없음(notes 사유) |
| 22 | P7 `.harness/stale-values.yaml` OpenAPI 항목 (N P7 → Final) · P8 등록 여부 (N P8 → Final) | 다른 계약 몫 — `kaizen-0924-final` (`.harness/`) |
| 23 | P8 `gate-result-taxonomy.md:42` 번역투 (FT · XD P8 결함 1) | 조건으로 다룸 — ER-02 `tax_old` |
| 24 | P8 판정 세 줄이 `docs/infra` 에만 (XD P8 결함 3) | 고치지 않음 — 원칙 문서 전부의 구조 문제라 한 줄 옮기기로 안 풀린다(교차 진단 「다음 사이클에 다룰 거리」). notes 다음 사이클 메모에 `docs/infra/platform/cicd.md` 로 적는다 |
| 25 | P8 Flux · Argo · Kubernetes 1.37 등 · GitHub 밖 CI · 세 분류 규범 · 1.7+ 표기 · 네 칸 이름과 `env_gaps` (N P8) | 고치지 않음 — 원칙 문서가 먼저 · 근거 없음 · 기준 원본 새 판 옮길 때(notes 사유) |
| 26 | P8 README 평가 사례 수 (infra 6 · backend 8) (N P8 메모) | 고치지 않음 — notes 가 두 킷을 함께 정하라고 다음 사이클로 보냈다 |
| 27 | P9 `rust-audit:36` · `rust-model:31` 네 칸 없는 `[미검증]` (FT · XD P9 (2) · (3)) | 조건으로 다룸 — SK-04 |
| 28 | P9 audit-criteria 시각 판정 행 · 버전 리터럴 · testcontainers 0.27 (N P9) | 고치지 않음 — 기준 문서에 자리부터 · breaking change 가 있는 판 올림 · 행 삭제 결정(notes 사유) |
| 29 | P9 rust-kit 특정 앱 이름 66 곳 (N P9 메모) | 고치지 않음 — 파일마다 확인해야 하는 정리 작업이라 다음 사이클 rust-kit 한 관심사로(한 파일씩) |
| 30 | P10 react-init 이 `strictPort` 를 안 넣음 (FT · XD P10 결함 1) | 조건으로 다룸 — SK-05 |
| 31 | P10 `harness-project.yaml.template` 복사 절차 없음 (XD P10 결함 1 끝) | 고치지 않음 — 이번 사이클 전부터 있던 것이고 템플릿을 쓸지 지울지부터 정해야 한다. notes 다음 사이클 메모에 `harness-project.yaml.template` 로 적는다 |
| 32 | P10 Activity canary · ViewTransition · react-reviewer §10 · `project-detect.sh` 미사용 · `g6-build-audit.md` (N P10) | 고치지 않음 — 근거 없음 · 평가 측 문턱 · 설계 기록 현행화 결정(notes 사유) |
| 33 | P11 planning-reviewer 기준 원본 사본 (N P11 → 다음 사이클 Phase 3 뒤) | 고치지 않음 — harness 기준 원본 번호 문제를 먼저 풀어야 한다(P8 넘김과 같은 일). Codex r2-4 와 같은 일 — 70 행 |
| 34 | P11 GitHub 문서 날짜 · Mermaid 12 렌더 · PRD 와 결정 기록 비교 등 (N P11) | 고치지 않음 — notes 사유 그대로 |
| 35 | P12 `_lib-project-id.sh:207` 기간 중간 멈춤 (FT · XD P12 결함 1) | 조건으로 다룸 — SK-06 (c). Codex r3-1 과 같은 결함이라 한 조건으로 묶었다(Final 지침). 문턱 없이 마지막 기록 뒤 실패로 가른다 — 「하지 않기로 한 것」 첫째 줄 |
| 36 | P12 `claude -p` 대체 경로가 사용자 훅을 띄움 (FT · XD P12 결함 2) | 고치지 않음 — 추정이고 확인하려면 실제 훅이 뜬다(교차 진단 「실행 금지」). 효과를 재지 못한 옵션을 넣지 않는다 |
| 37 | P12 태그 `vocab:…` · `warn:lemma-map-unreadable` (FT · XD P12 결함 3) | 조건으로 다룸 — SK-06 (a) |
| 38 | P12 `reflect-kit/README.md` 버전 줄 (N P12 → 다음 사이클 Phase 12) | 조건으로 다룸 — SK-06 (b) · AP-01. design-kit 과 같은 결함이라 같은 결정(README 에 버전을 적지 않는다)을 함께 적용한다 |
| 39 | P12 `hooks.json` 따옴표 · `async` · `last_assistant_message` · `facets_unmatched` 지워진 워크트리 (N P12) | 고치지 않음 — 킷 넷을 V8 검사와 함께(harness 쪽 scripts) · 다음 사이클(notes 사유) |
| 40 | P13 enum 줄만 빠진 목록 (XD P13 결함 1) | 조건으로 다룸 — SK-07 (a)(c) |
| 41 | P13 음성 대조 블록 (1) 한 방향 (XD P13 결함 2) | 조건으로 다룸 — SK-07 (b) |
| 42 | P13 SK-06 `G91` 뒤 E 상대값 (XD P13 (1)) | 고치지 않음 — 슬라이서 해석 관례는 교차 진단자의 지식이고 이 세션에서 실측하지 못했다. 설치본 시작 G-code 가 `M83` 만 써서 영향이 없다 |
| 43 | P13 `[미검증]` 네 칸 다섯 자리 · 현행화 · 금지 키 FAIL 시험 파일 (N P13) | 고치지 않음 — 관심사 상한 · `/bambu-research` 소관 · 한 파일 한 위반으로 다음 사이클(notes 사유) |
| 44 | P13 올리지 않은 가지 `feat/bambu-kit-orca-h2s-feedback` 충돌 (N P13) | 고치지 않음 — 다른 가지. 이 계약이 같은 블록을 또 고친다는 사실을 notes 에 적는다 |
| 45 | P14 `setup-guide/SKILL.md:198` Grep 에 `.env*` (XD P14 결함 1) | 조건으로 다룸 — SK-08 (a). 같은 줄 `**/*.p8`(개인 키)도 같은 결함이라 함께 |
| 46 | P14 `evals.json:124` `.env` 기준 평가 항목 (XD P14 결함 2) | 조건으로 다룸 — SK-08 (b). `setup.env_contains` 는 둔다 — 값 든 `.env` 가 있어야 「열지 않는다」 항목이 잴 거리가 생긴다 |
| 47 | P14 `docs/onboarding-kit/examples/fcm-ios-setup-guide.md` 옛 값 · 시뮬레이터 · 세 칸 · 앱 이름 (N P14 → Final) | 조건으로 다룸 — SK-08 (c) |
| 48 | P14 `guide_gate` 세 칸 검사 · AUTO 표지 · CocoaPods → SPM · 서비스 계정 키 · 평가 날짜 (N P14) | 고치지 않음 — notes 사유(예제를 고친 뒤 다음 사이클 · 표가 바뀜 · 근거 파일이 미루라 함) |
| 49 | P15 `core-antipatterns.md:36` 죽은 grep 칸 (XD P15) | 조건으로 다룸 — SK-09 |
| 50 | P15 `adapter-dart-flutter.md:26` · `docs/tone/dart-flutter-idioms.md:633` 같은 모양 (XD P15) | 고치지 않음 — 값을 설명하는 칸이고 실제로 도는 명령은 따로 있다(`adapter-dart-flutter.md:245` 코드 블록) |
| 51 | P15 연구 기록 「죽은 이름 검사 넷」 서술 (XD P15) | 고치지 않음 — 날짜 붙은 이력 기록이라 고치지 않고, 표 칸 둘이 더 있었다는 사실을 notes 메모에 남긴다 |
| 52 | P15 C-06 강도 · `etc_seq=663` 이름표 · `__` 예시 · 기준 버전 3.38.4 · go_router 링크 · 위키 이전 · `material_ui` · `locale-korean.md` §2 grep 열 · `sources.md` 「마지막 세 행」 (N P15) | 고치지 않음 — 근거 재확인이 필요하다. `locale-korean.md` §2 grep 열은 여러 계약이 번역투 정규식 원문으로 베낀 자리라 열을 없애면 인용이 끊긴다 — 다음 사이클 |
| 53 | P16 뷰어에 「판정 불가」 자리 없음 (XD P16 결함 1) | 고치지 않음 — 위 「하지 않기로 한 것」 둘째 줄 |
| 54 | P16 `api-ui:168` 서버를 앞에서 띄움 · 포트 충돌 (XD P16 결함 2) | 조건으로 다룸 — SK-10 (a) |
| 55 | P16 수치 기준 `-0` 행 · `api-verify:117` 목록 (XD P16 결함 3) | 조건으로 다룸 — SK-10 (b)(c) |
| 56 | P16 `docs/superpowers/specs/2026-09-02-api-kit-design.md:249` (N P16 → Final) | 고치지 않음 — 위 「하지 않기로 한 것」 셋째 줄 |
| 57 | P16 `/api-contract` §9 예시 · CSP · §7 식 · 판정 불가를 검사에 넣는 일 (N P16) | 고치지 않음 — hurl 로 먼저 재야 하거나 사용자 확인이 먼저다(notes 사유) |
| 58 | P17 러너가 `bash` 펜스만 봄 (XD P17 결함 1) | 조건으로 다룸 — SK-11 |
| 59 | P17 러너 `for c in data['cases']` (N P17 메모 「러너를 고칠 때 같이」) | 조건으로 다룸 — SK-11 |
| 60 | P17 howto-audit 리포트 미검증 칸 · DITA 2.0 · 러너 음성 대조를 킷 안에 · 러너 시간 · `design-brief.md:385` (N P17) | 고치지 않음 — notes 사유 그대로 |
| 61 | P1 넘김 — 킷 다섯 자리의 옛 `[미검증]` 문구 (N P1 → Phase 5 · 8 · 9 · 10 · 14) | 이미 반영 — 다섯 파일에서 옛 문구 0 줄(`infra-test:37` · `rust-reviewer.md:160` 은 네 칸) |
| 62 | P4 넘김 — 판정 세 줄 (N P4 → Phase 8 · 9) · F20 (→ Phase 11) · P6 넘김 — react 규약 되말하기 · 관례 표 · 3 회 (→ Phase 10) | 이미 반영 — `docs/infra/platform/cicd.md:77` · `rust-preflight/SKILL.md:113` · plan-prd Gotcha 14 · `render-evidence-protocol.md:54` · `:59` · `:106` |
| 63 | DG-02 교차 진단 기록 · Phase 7 · 8 · 9 · 11 개정 파일 줄 (FT · Final 지침) | 다른 계약 몫 — `kaizen-0924-final`. 이 계약은 notes `## Final 에 넘기는 것` 에 커밋 sha 를 적는다(ER-03) |
| 64 | `check-stale-values.py` `SOURCE_DIRS` · validate-plugin V 줄 · V6 범위 · 평가자 사용자 교정 대조 (FT · XD P3 · P6 · P13) | 다른 계약 몫 — `kaizen-0924-f1-harness-followups`. 이 계약 DG-05 는 옛 값을 마흔한 파일에 직접 세고 validate-plugin 을 종료 코드와 V 줄로 함께 잰다 |
| 65 | `.claude/skills/*-kaizen/` 고칠 것 (N P6 · P7 · P8 · P9 · P10 · P13 · P14 · P15 · P17) · `ci.yml` 줄 (N P10 · P12 · P14 · P17) · `detect-docs-drift.py` (N P14 · P16) · `save-feedback.sh` (N 여러 Phase) | 다른 계약 몫 — `kaizen-0924-f1-harness-followups` |
| 66 | 문서 사이트 HTML · 킷 `plugin.json` 버전 · marketplace · changelog · end_sha 덧붙임 커밋 세기 · QA 리포트 수 오기 (N 전 Phase · FT) | 다른 계약 몫 — `kaizen-0924-final` |
| 67 | Codex r2-1 · 높음 — backend `audit-criteria.md:20` · `api-design.md:102` 가 RFC 9457 다섯 멤버를 필수로 적음 | 조건으로 다룸 — SK-12 (a). 확인: 같은 레포 `docs/api/contract/error-status-contracts.md:25` 가 1 차 출처 대조로 「`type` 이 없으면 `about:blank` — 누락 자체는 위반이 아니다」 라 적었다. 같은 결함이 `backend-system/references/system-principles.md:21` 에도 있어 함께. 다섯 필드 규칙 자체는 원칙 3(`api-design.md:35`)의 킷 규칙이라 남기고 출처만 가른다. 나머지 네 멤버가 선택이라는 RFC 본문은 근거 파일에 없어 적지 않는다 |
| 68 | Codex r2-2 · 높음 — design 결정 전파 게이트가 표면 없는 결정을 통과 | 조건으로 다룸 — SK-03 (d). 확인: 시작 커밋 판 게이트에 `decision_id` · `status` 만 있는 결정을 넣으면 `decisions=1 surfaces=0 violations=0` · 종료 코드 0. `status` 는 값 목록이 규약에 없어 검사하지 않는다 |
| 69 | Codex r2-3 · 중간 — `design-reviewer.md:26` 미검증 사본이 2026-08-13 개정 전 판 | 고치지 않음 — 확인은 됐다(`design-reviewer.md` 의 `UNVERIFIED_ENV` 0 줄 · `임계값은 2 다` 1 줄). 기준 원본이 여섯 항목이라 「5 조항 복제」 가 성립하지 않고, 옮기면 design-audit Gotcha 11 · Step 4 · Step 5 · evals id 21 의 REJECT 문턱이 같이 바뀐다 — 「하지 않기로 한 것」 다섯째 줄. 다음 사이클 Phase 3 뒤 (18 행과 같은 일) |
| 70 | Codex r2-4 · 중간 — `planning-reviewer.md:22` 같은 옛 사본 · `:117` 없는 「4 요건」 가리킴 | 고치지 않음 — 69 행과 같은 이유. `docs/planning/research-log.md:39` 와 Phase 11 notes `:68` · `:86` 이 이미 넘겼다(33 행). react-kit · api-kit reviewer 도 같은 옛 사본이라 넷을 한 번에 |
| 71 | Codex r2-5 · 중간 — infra-test checkout 검사가 주석 줄로도 PASS | 조건으로 다룸 — SK-12 (b). 확인: `printf '# uses: actions/checkout@v4\n' \| grep -q 'actions/checkout'` 종료 코드 0, 규칙 1 을 뽑아 주석만 있는 워크플로에 돌리면 `PASS`. PyYAML 로 바꾸라는 제안 대신 `uses:` 키 줄만 세는 식으로 고친다 — python3 가 없을 때도 규칙 1 이 돌아야 한다(규칙 2 는 없으면 `[미검증]`) |
| 72 | Codex r2-6 · 중간 — rust-preflight `:16` 자동 적용 vs `:34` 사용자 안내 | 조건으로 다룸 — SK-04 둘째 줄. 확인: `:16` Gotcha 2 · `:50` ~ `:51` Step 1 · `:158` 결과 표 `FIXED` 셋이 자동 적용이고 `:34` 하나만 반대. 제안(16 행을 바꾸기)과 달리 한 줄만 고치는 쪽 — 셋을 바꾸는 것보다 작다 |
| 73 | Codex r2-7 · 낮음 — flutter-build `--delete-conflicting-outputs` 설명의 판 번호(2.7.0 주장) · 명령에서 빼기 | 고치지 않음 — 심각도 낮음. 2.7.0 동작은 설치된 `~/.pub-cache/hosted/pub.dev/build_runner-2.13.1/CHANGELOG.md` `:149` · `:150`(2.7.0 항목 「Ignore `-d` flag: always delete files as if `-d` was passed.」)으로 확인된다. 킷 문장(2.16 에서 제거된 호환 옵션 목록으로 옮겨짐, `phase5.md:41`)과 어긋나지 않고, 명령의 플래그는 효과 없는 인자다. 명령에서 뺄지는 Phase 5 notes `:79` 가 다음 사이클로 보냈다 — 그 notes 가 막힌 이유로 든 「경고인지 오류인지」 가운데 2.7.0 ~ 2.13.1 은 이 파일이 답한다(무시한다). 2.16 쪽은 설치본이 없어 모른다(이 맥의 설치본은 2.3.3 ~ 2.13.1). notes 다음 사이클 메모에 `build_runner-2.13.1` 로 적는다 |
| 74 | Codex r2-8 · 낮음 — react-l10n `grep -c` 가 0 건에 종료 코드 1 | 조건으로 다룸 — SK-05 넷째 줄. 확인: 빈 입력에 `grep -c '^-msgid '` → 출력 `0` · 종료 코드 1. 이번 사이클이 만든 줄(`001c900`)이고 한 줄 고침이다 |
| 75 | Codex r3-1 · 높음 — reflect `collect_status` 가 엔트리 하나라도 있으면 도중 멈춤을 못 잡음 | 조건으로 다룸 — SK-06 (c) (35 행과 한 조건). 확인: `_lib-project-id.sh:207` 조건이 `e == 0 && n > 0` 뿐. 제안 가운데 「마지막 성공 시각 뒤 실패」 쪽을 택했다 — 비율 문턱은 근거가 없다 |
| 76 | Codex r3-2 · 중간 — reflect-digest 실행 줄이 period 와 상관없이 7 | 조건으로 다룸 — SK-06 (d). 확인: `:122` 「첫 인자는 period 일수」 인데 `:126` · `:183` 이 `7`. 같은 결함이 reflect-kaizen `:68`(`window` 인데 `30`)에도 있어 함께 |
| 77 | Codex r3-3 · 중간 — onboarding G1 이 전체 수만 비교 | 조건으로 다룸 — SK-08 (d). 확인: Step 1 출처 둘 · Step 2 출처 0 인 입력이 `G1_LEDGER PASS steps=2 ledger=2`(bash · zsh 같음). 킷 픽스처 추가는 「하지 않기로 한 것」 일곱째 줄 |
| 78 | Codex r3-4 · 중간 — bambu 댓글 받기가 앞 실행 페이지를 함께 읽음 | 조건으로 다룸 — SK-07 (e). 확인: 가짜 `curl` 로 `comments-100.json`(59 개)이 남은 폴더에서 돌리면 `받은 hits 61 (페이지 2)` · `WARN` |
| 79 | Codex r3-5 · 중간 — bambu 자기 검사 블록이 정의 안 된 `SKILL_DIR` 사용 | 조건으로 다룸 — SK-07 (d). 확인: `SKILL_DIR` 없이 돌리면 `/SKILL.md` 를 읽어 빈 측정 코드로 `IndexError`. 같은 줄이 `:2191` 두 스크립트 자기 검사에도 있어 둘 다. 제안의 `${CLAUDE_PLUGIN_ROOT}` 대신 킷의 다른 블록(`:923` · `:1531`)과 같은 `SKILL_DIR=<이 스킬의 기준 폴더>` 로 둔다 |
| 80 | Codex r3-6 · 낮음 — api-kit `-0` 을 「I-JSON 게이트」 로 분류 | 고치지 않음 — 확인 불가. RFC 7493 이 `-0` 을 금지하지 않는다는 본문이 근거 파일에 없다(`phase16.md:37` S12 는 상태만). 킷의 `-0` 줄은 이유를 JCS 로 적었다(`api-contract/SKILL.md:67`) — 「하지 않기로 한 것」 여섯째 줄. 다음 사이클 Phase 16 이 RFC 7493 §2.2 원문을 근거 파일에 넣은 뒤 이름을 가른다 |

- 기능 조건 20 · 전체 조건 줄 30 (6.2 두 명령으로 셌다)
- 사용자가 할 일: 없음

## 회귀 게이트 — 측정 공통 정의와 봉인 전 실측

모든 조건의 측정은 아래 `common.sh` 와 `m.sh` 를 차례로 `.` 으로 읽은 **bash** 셸에서 돈다 — `common.sh` 는 bash 가 아니면 `NOT_BASH` 를 찍고 종료 코드 2 로 끝난다
(zsh 는 따옴표 없는 변수를 쪼개지 않고 배열 첨자가 1 부터다). `m` 은 도우미 함수와 세 판 폴더가 없으면 `HELPER_MISSING` · `SNAPSHOT_MISSING` 을 내고 멈춘다 —
그래서 조건마다 `type m` 하나로 정의 확인을 대신한다. 세 판(시작 커밋 · 끝 판 · 사이클 개시 커밋) 풀기가 끊기거나 마흔한 파일 가운데 하나라도 시작 · 끝 판에서 비면
`common.sh` 가 `SNAPSHOT_FAIL` 을 내고 종료 코드 2 로 끝난다. `END_UNRESOLVED` 가 찍히면 셸이 종료 코드 2 로 끝난다 — `HEAD` 로 바꿔 재지 않는다.
셸이 끝나면 임시 폴더를 지운다. `m` 의 종료 코드는 판정하지 않는다 — 판정은 출력 값으로 한다. 블록 · 러너 · 완료 검사 대조는 끝 판을 푼 폴더나 그 사본에서만 돈다 — 작업 폴더는 바뀌지 않는다.

세 블록을 각 블록 첫 `#` 주석 줄(셔뱅 다음)의 이름 그대로 한 폴더에 저장하고 그 폴더를 `K` 에 넣는다. `sweep.sh` 옆에는 `node_modules` 를
`/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/de8c7935-a5b6-4df5-9106-fafa73c288a0/scratchpad/p1build/node_modules` 로 잇고
`cfg.markdownlint-cli2.jsonc` = `{ "config": { "MD013": false } }` 를 둔다 — 준비 단계 실측(2026-09-25): 그 자리의 `.bin/markdownlint-cli2 --version` 첫 줄이
`markdownlint-cli2 v0.23.2 (markdownlint v0.41.1)`. 없으면 그 폴더에서 `npm install --no-save markdownlint-cli2@0.23.2` 부터 돌린다.
그 밖의 준비 단계 실측(2026-09-25): `command -v bash` → `/opt/homebrew/bin/bash` (5.3) · `/bin/sh` 는 bash 3.2.57 · `zsh` 5.9 · `shellcheck` 있음 · `python3` · `shasum` · `git` · `perl` · `pkill` 있음 ·
`defaults read /Applications/BambuStudio.app/Contents/Info.plist CFBundleShortVersionString` → `02.08.02.61` · 그 판의 옵션 목록 `bambu-kit/skills/bambu-print-profile/references/option-keys/bambu-02.08.02.61.tsv`
(`enum` 줄 385). `common.sh` 의 `R` 은 예행 저장소를 가리킬 때만 쓴다 — 비우면 작업 폴더다. 세 판을 `${TMPDIR:-/tmp}/f1k.XXXXXX` 에 푸니 `TMPDIR` 를 스크래치 폴더로 두고 읽는다.
`END_OVERRIDE` 는 예행에서 시작 커밋 판을 끝 판으로 잴 때만 쓴다 — 평가에서는 비운다.

예행 도구(스크래치 `kaizen/f1kit/`): `mock.py`(sha256 앞 16 자리 `9e8da262a81720a3` — 시작 커밋 판에 이 계약이 요구하는 편집을 적용한다) ·
`rehearse.sh`(시작 커밋에서 예행 저장소를 만들어 봉인 · 킷 묶음마다 한 커밋 · `end_sha` · notes · `end_sha` 를 흉내 낸다. 변형 `base` · `unsigned-kit` · `unsigned-planningkit` · `harness-other` · `typo-shared` · `mixed` · `cross-phase` ·
`seal-broken` · `wc-only` · `no-notes` · `bad-text`) · `runall.sh`(조건 ID 를 받아 차례로 `m` 을 돈다) · `variants-v3.sh`(변형마다 예행 저장소를 다시 만들고 겨냥한 조건을 잰다) ·
`del.sh`(끝 판을 푼 폴더에서 문장 하나가 든 줄만 지우고 값이 바뀌는지 본다) · `assemble.py`(계약 조각과 측정 블록을 이어 붙인다 — 측정 블록은 `k/` 의 파일 그대로다).

```bash
#!/usr/bin/env bash
# common.sh — 측정 공통 정의. bash 로 읽는다 (zsh 는 배열 첨자가 1 부터이고 따옴표 없는 변수를 쪼개지 않는다)
[ -n "${BASH_VERSION:-}" ] || { echo "NOT_BASH — bash -c 안에서 다시 읽는다"; exit 2; }
export LC_ALL=C.UTF-8   # 번역투 정규식이 글자 단위로 돌아야 한다
cd "${R:-/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/kaizen-0924}" || exit 2
B=5b4fd72d5587c937c1875ddb62872f32ae087dcf                  # 이 계약 시작 HEAD
C0=7689fde                                                  # 카이젠 2026-09-24 사이클 개시 커밋 — 연구 기록 경고 비교 기준
SIG='Kaizen-Phase: kaizen-0924-f1-kit-followups'
CF=.harness/sprint-contract-kaizen-0924-f1-kit-followups.md
AM=.harness/sprint-amendments-kaizen-0924-f1-kit-followups.md
NOTES=.harness/.meta/kaizen-0924/f1-kit-followups-notes.md
END=$( [ -f "$AM" ] && sed -n 's/^end_sha:[[:space:]]*//p' "$AM" | tail -1 )
[ -n "${END_OVERRIDE:-}" ] && END=$END_OVERRIDE             # 예행에서 시작 커밋 판을 잴 때만 쓴다
if [ -z "$END" ] || ! git rev-parse -q --verify "$END^{commit}" >/dev/null; then
  echo "END_UNRESOLVED — 측정을 멈춘다. HEAD 로 바꿔 재지 않는다"; exit 2
fi
END=$(git rev-parse "$END")
: "${K:?도우미 폴더를 K 에 넣는다}"
# 킷 묶음 — 한 커밋은 이 가운데 하나만 건드린다 (러닝북 「한 커밋에 킷 하나」)
KITG=(backend infra rust planning flutter design react reflect bambu onboarding tone api howto)
declare -A GPATH=(
  [backend]="backend-kit/ docs/backend/" [infra]="infra-kit/ docs/infra/" [rust]="rust-kit/ docs/rust/" [planning]="docs/planning/"
  [flutter]="flutter-toolkit/" [design]="design-kit/" [react]="react-kit/" [reflect]="reflect-kit/" [bambu]="bambu-kit/"
  [onboarding]="onboarding-kit/ docs/onboarding-kit/examples/" [tone]="tone-kit/" [api]="api-kit/ docs/api/" [howto]="howto-kit/")
RLB=docs/backend/research-log.md; RLI=docs/infra/research-log.md; RLR=docs/rust/research-log.md; RLP=docs/planning/research-log.md
TAX=infra-kit/references/gate-result-taxonomy.md; ITS=infra-kit/skills/infra-test/SKILL.md
BAC=backend-kit/skills/backend-audit/references/audit-criteria.md; BSP=backend-kit/skills/backend-system/references/system-principles.md; BAD=docs/backend/fundamentals/api-design.md
RAU=rust-kit/skills/rust-audit/SKILL.md; RMO=rust-kit/skills/rust-model/SKILL.md; RPF=rust-kit/skills/rust-preflight/SKILL.md
FPD=flutter-toolkit/references/project-detection.md; VEP=flutter-toolkit/references/visual-evidence-protocol.md
FBU=flutter-toolkit/skills/flutter-build/SKILL.md; FPR=flutter-toolkit/skills/flutter-preflight/SKILL.md; FLN=flutter-toolkit/skills/flutter-l10n/SKILL.md
DCO=design-kit/skills/design-component/SKILL.md; DRD=design-kit/README.md; DVP=design-kit/references/visual-change-protocol.md
RIN=react-kit/skills/react-init/SKILL.md; RRU=react-kit/skills/react-run/SKILL.md; RLN=react-kit/skills/react-l10n/SKILL.md
RSC=reflect-kit/docs/SCHEMA.md; RDE=reflect-kit/docs/DESIGN.md; RRD=reflect-kit/README.md
RLIB=reflect-kit/hooks/_lib-project-id.sh; RCT=reflect-kit/evals/hooks/collect-status-test.sh
RDG=reflect-kit/skills/reflect-digest/SKILL.md; RKZ=reflect-kit/skills/reflect-kaizen/SKILL.md
BAM=bambu-kit/skills/bambu-print-profile/SKILL.md
OSK=onboarding-kit/skills/setup-guide/SKILL.md; OEV=onboarding-kit/skills/setup-guide/evals/evals.json; OEX=docs/onboarding-kit/examples/fcm-ios-setup-guide.md
TAP=tone-kit/references/core-antipatterns.md
AUI=api-kit/skills/api-ui/SKILL.md; AVE=api-kit/skills/api-verify/SKILL.md; ACN=docs/api/contract/snapshot-sealing-canonicalization.md
HRN=howto-kit/evals/run-evals.sh; HRD=howto-kit/README.md; HEV=howto-kit/evals/evals.json
FILES=("$RLB" "$BAC" "$BSP" "$BAD" "$RLI" "$TAX" "$ITS" "$RLR" "$RAU" "$RMO" "$RPF" "$RLP" "$FPD" "$VEP" "$FBU" "$FPR" "$FLN"
       "$DCO" "$DRD" "$DVP" "$RIN" "$RRU" "$RLN" "$RSC" "$RDE" "$RRD" "$RLIB" "$RCT" "$RDG" "$RKZ" "$BAM" "$OSK" "$OEV" "$OEX"
       "$TAP" "$AUI" "$AVE" "$ACN" "$HRN" "$HRD" "$HEV")
MDF=(); for f in "${FILES[@]}"; do case $f in *.md) MDF+=("$f") ;; esac; done
T=$(mktemp -d "${TMPDIR:-/tmp}/f1k.XXXXXX") && T=$(cd "$T" && pwd -P) || exit 2
mkdir -p "$T/B" "$T/E" "$T/C0"
trap 'rm -rf "$T"' EXIT
# 세 판을 풀어 둔 폴더에서 잰다 — 작업 폴더에 남은 다른 계약의 미커밋 변경이 끼지 않는다
# 풀기가 도중에 끊기면 0 을 기대하는 값이 통과로 읽힌다 — 여기서 멈춘다
git archive "$B" | tar -x -C "$T/B" && git archive "$END" | tar -x -C "$T/E" && git archive "$C0" | tar -x -C "$T/C0" \
  || { echo "SNAPSHOT_FAIL — 측정을 멈춘다"; exit 2; }
for f in "${FILES[@]}"; do [ -s "$T/E/$f" ] && [ -s "$T/B/$f" ] || { echo "SNAPSHOT_FAIL $f"; exit 2; }; done
# sect <파일> <제목 앞부분> — 그 제목부터 같은 깊이 이하의 다음 제목 전까지. 코드 펜스 안의 `#` 줄은 제목으로 보지 않는다
sect() { awk -v h="$2" '
  /^[[:space:]]*(```|~~~)/ { fence = !fence }
  !f && !fence && index($0, h) == 1 { f = 1; lvl = match($0, /[^#]/) - 1; print; next }
  f && !fence && /^#+ / { l = match($0, /[^#]/) - 1; if (l <= lvl) exit }
  f' "$1"; }
# cnt <파일> <글> — 그 글이 든 줄 수 (글자 그대로)
cnt() { grep -cF -- "$2" "$1"; }
# toks <글> <토큰…> — 토큰마다 글 안에서 그 토큰이 든 줄 수
toks() { local s="$1" o=""; shift; for t in "$@"; do o="$o$(printf '%s\n' "$s" | grep -cF -- "$t") "; done; echo "${o% }"; }
fmb() { awk 'NR==1&&/^---/{fm=1;next} fm&&/^---/{exit} fm' "$1"; }
# barefence <파일> — 언어 힌트 없는 여는 펜스 수 (여닫기를 번갈아 센다)
barefence() { awk '/^[[:space:]]*```/{ if (!o) { o = 1; if ($0 ~ /^[[:space:]]*```[[:space:]]*$/) n++ } else o = 0 } END{print n+0}' "$1"; }
url()   { grep -oE 'https?://[^ )>"`]+' | sed -E 's/[.,;:]+$//' | sort -u; }
added1() { git diff --no-index -U0 "$T/B/$1" "$T/E/$1" | grep '^+' | grep -v '^+++'; }
added() { for f in "${FILES[@]}"; do added1 "$f"; done; }
mine() { git log --format= --name-only "${1}..${2}" --grep="^${3}\$" | grep . | LC_ALL=C sort -u; }
signed_commits() { git log --format=%H "${B}..${END}" --grep="^${SIG}\$"; }
unsigned_on() { _b=${1}; _u=${2}; _s=${3}; shift 3
  git log --format=%H "${_b}..${_u}" -- "$@" | while read -r _c; do git log -1 --format=%B "$_c" | grep -qxF "$_s" || echo "$_c"; done; }
# not_other <base> <상한> <서명> <경로…> — 경로를 건드린 구간 안 커밋 가운데 harness 쪽 계약 서명 줄이 글자 그대로 있는 커밋을 뺀 나머지 (0 줄이어야 한다)
not_other() { _b=${1}; _u=${2}; _s=${3}; shift 3
  git log --format=%H "${_b}..${_u}" -- "$@" | while read -r _c; do
    _m=$(git log -1 --format=%B "$_c")
    # 서명 모양만 보고 빼면 이 계약 서명을 잘못 적은 커밋도 「다른 Phase」 로 빠진다 — 이 구간에 함께 커밋하는 계약은 하나다
    printf '%s\n' "$_m" | grep -qxF 'Kaizen-Phase: kaizen-0924-f1-harness-followups' && continue
    echo "$_c"; done; }
# group_of <경로> — 킷 묶음 이름 (없으면 빈 값)
group_of() { local g p; for g in "${KITG[@]}"; do for p in ${GPATH[$g]}; do case $1 in "$p"*) echo "$g"; return ;; esac; done; done; }
scope() { awk '/^## /{s=$0} s ~ /^## 범위 경계/ && /^```text$/{b=1; n=0; next} b && /^```$/{b=0; next} b{n++; if (n==1 && $0 != "# sprint-scope") b=0; else if (n>1) print}' "$1"; }
fm_get() { awk -v k="^$2:[[:space:]]*" 'NR==1 && /^---[[:space:]]*$/ { fm=1; next } fm && /^---[[:space:]]*$/ { exit } fm && $0 ~ k { sub(k, "", $0); print; exit }' "$1" | sed -e "s/[[:space:]]*$//" -e "s/^['\"]//" -e "s/['\"]\$//"; }
sha256_16() { if command -v sha256sum >/dev/null 2>&1; then sha256sum; elif command -v shasum >/dev/null 2>&1; then shasum -a 256; else python3 -c 'import hashlib,sys; print(hashlib.sha256(sys.stdin.buffer.read()).hexdigest())'; fi | cut -c1-16; }
contract_digest() { grep -E '^- \[[ x]\] [A-Z]{2,}-[0-9]{2}' "$1" | sed -E 's/^- \[[ x]\]/- [ ]/' | sha256_16; }
verify_seal() { rec=$(fm_get "$1" conditions_digest); rec=${rec#sha256:}; if [ -z "$rec" ]; then echo "SEAL_ABSENT $1"; return 0; fi
  act=$(contract_digest "$1"); if [ "$rec" = "$act" ]; then echo "SEAL_OK $1"; else echo "SEAL_BROKEN $1 recorded=$rec actual=$act"; fi; }
# kitcp <판 폴더> <이름> <폴더…> — 그 판의 폴더들을 $T/<이름>/ 아래로 복사한다 (대조는 사본에서만 돈다)
kitcp() { local src=$1 dst=$T/$2; shift 2; rm -rf "$dst"; mkdir -p "$dst"; for d in "$@"; do mkdir -p "$dst/$(dirname "$d")"; cp -R "$src/$d" "$dst/$d" || return 2; done; printf '%s' "$dst"; }
K02='(을|를) ?(처리|관리)(합니다|한다)|에 대해서?|하도록 (합니다|한다)|에 의(해|하여)|되어 있(는 경우|을 때)|(표시|적용|호출|생성|반환)(됩니다|된다)'   # tone-kit/references/locale-korean.md §2 grep 열
NAMES='fit-?pal|fit_pal|fit pal|flutter[-_]playwright|playwright-mcp|chrome-devtools-mcp'
```

```bash
#!/usr/bin/env bash
# m.sh — 조건마다 한 갈래. common.sh 를 먼저 읽은 bash 셸에서 `m <조건 ID>` 로 부른다
m() {
  type sect added verify_seal group_of >/dev/null 2>&1 || { echo "HELPER_MISSING"; return 2; }
  [ -d "$T/E" ] && [ -d "$T/B" ] && [ -d "$T/C0" ] || { echo "SNAPSHOT_MISSING"; return 2; }
  local E=$T/E Bd=$T/B out rc
  case $1 in
  SK-01)
    # (a) 2026-09-24 항목 안 소제목 여덟이 날짜 붙은 이름으로 있다
    toks "$(sect "$E/$RLB" '## [2026-09-24]')" "### 외부 리서치 (evidence 파일 한정) — 2026-09-24 사이클" "### 사실 정정 — 2026-09-24 사이클" \
      "### Phase 7 변경 요약 — 2026-09-24 사이클" "### 미반영 (근거 부족 · 범위 밖) — 2026-09-24 사이클"
    toks "$(sect "$E/$RLI" '## [2026-09-24]')" "### 조회한 외부 소스 (근거 파일 \`.harness/.meta/evidence/phase8.md\`) — 2026-09-24 사이클" "### 변경 내역 — 2026-09-24 사이클"
    toks "$(sect "$E/$RLR" '## [2026-09-24]')" "### 채택한 인사이트 — 2026-09-24 사이클"
    toks "$(sect "$E/$RLP" '## [2026-09-24]')" "### 명시적 비범위 — 2026-09-24 사이클"
    # (b) 같은 제목 중복 경고(MD024) 수가 사이클 개시 판과 같다
    local f a z line=""
    for f in "$RLB" "$RLI" "$RLR" "$RLP"; do
      a=$(bash "$K/sweep.sh" --count "$T/C0/$f" MD024) || { echo "LINT_NOT_RUN $f"; return 2; }
      z=$(bash "$K/sweep.sh" --count "$E/$f" MD024) || { echo "LINT_NOT_RUN $f"; return 2; }
      line="$line$(basename "$(dirname "$f")")=$a/$z "
    done; echo "${line% }"
    # (c) 사이클 동안 바뀐 킷 쪽 마크다운 전부 — 규칙별 경고 수가 사이클 개시 판보다 는 규칙이 있는 파일 수
    git diff --name-only --diff-filter=AM "$C0" "$END" -- '*.md' | grep -v '^\.harness/\|^harness/\|^\.claude/\|^docs/kaizen/' > "$T/sw.txt"
    bash "$K/sweep.sh" --pair "$T/C0" "$E" "$T/sw.txt" ;;
  SK-02)
    echo "$(cnt "$E/$FPD" 'Makefile 타겟이 안에서 codegen 을 돌리면') $(cnt "$E/$FPD" '| `$MAKE app-preflight` |') $(cnt "$E/$FPD" '| `$MAKE app-build` |') $(cnt "$E/$FPD" '안에서 codegen 을 돌리는 묶음 타겟(`app-build` · `app-preflight`)은 codegen 줄 자리에 넣지 않는다.') $(cnt "$E/$FPD" '단계마다 위 행의 타겟 — codegen 은 flutter-run codegen 절 블록 안의 `$MAKE app-codegen`') $(cat "$E/$FBU" "$E/$FPR" | grep -cE 'app-(build|preflight)')"
    echo "$(cnt "$E/$VEP" '[미검증] 사유') $(cnt "$E/$VEP" '[미검증] — 네 칸은 아래 미검증 줄') $(cnt "$E/$VEP" '- 미검증: N 건 [항목 — 막는 것 — 시도한 우회 — 통제 불가 사유 — 재검증 명령]') $(fmb "$E/$VEP" | grep -c '^version: 1.2.1$')"
    echo "$(cnt "$E/$FBU" 'new_first=N new=N codegen_exit=N') $(cnt "$E/$FBU" '[늘어난 삭제 — new 가 0 이 아니면 그 목록]') $(cnt "$E/$FPR" 'new_first=N new=N codegen_exit=N') $(cnt "$E/$FPR" '[늘어난 삭제 — new 가 0 이 아니면 그 목록]')"
    echo "$(cnt "$E/$FLN" 'fvm dart run slang') $(cnt "$E/$FLN" '- 번역 키 추가 후 반드시 codegen 재실행 — 명령은 Step 6 표를 따른다. slang 은 `flutter-run` codegen 절 블록으로 build_runner 를 돌려 전후 삭제 수를 세고, intl 은 `fvm flutter gen-l10n`')" ;;
  SK-03)
    local s n=0 k=0 g
    echo "$(sect "$E/$DCO" '# Gotchas' | grep -c 'visual-change-protocol.md')"
    # 규약 머리가 적은 일곱 스킬 전부 — Gotcha 절 안에서 규약을 인용하는가
    for s in $(sed -n '3,4p' "$E/design-kit/references/visual-change-protocol.md" | grep -oE 'design-[a-z]+' | grep -vx design-kit | sort -u); do
      n=$((n + 1)); g=$(sect "$E/design-kit/skills/$s/SKILL.md" '# Gotchas'; sect "$E/design-kit/skills/$s/SKILL.md" '## Gotchas')
      printf '%s\n' "$g" | grep -q 'visual-change-protocol.md' && k=$((k + 1))
    done; echo "$k/$n"
    echo "$(cnt "$E/$DRD" '버전: `') $(cnt "$E/$DRD" '버전은 `.claude-plugin/plugin.json` 의 `version` 을 본다.')"
    # (d) 결정 전파 게이트 — 입력 다섯(표면 없음 · id 형식 · 온전한 예 · 제외만 · 이유 없는 제외)의 종료 코드
    design_gate "$E" > "$T/dg.py" || { echo "DGATE_EXTRACT_FAIL"; return 2; }
    dg_inputs "$T/dgi"
    local i o=""
    for i in 1 2 3 4 5; do python3 "$T/dg.py" "$T/dgi/i$i.yaml" > /dev/null 2>&1; o="$o i$i=$?"; done; echo "gate$o" ;;
  SK-04)
    echo "$(grep -F '16. **파이프라인 종료 코드로만' "$E/$RAU" | grep -F '`[미검증]`' | grep -cF '네 칸(막는 것 · 시도한 우회 · 통제 불가 사유 · 재검증 명령)') $(grep -F '라이브 DB 조회 불가 시 정적 대체 경로' "$E/$RMO" | grep -F '`[미검증]`' | grep -cF '네 칸(막는 것 · 시도한 우회 · 통제 불가 사유 · 재검증 명령)') | $(cnt "$E/$RAU" '그 row 는 `[미검증]` 이다.') $(cnt "$E/$RMO" '그건 `[미검증]` 이다.')"
    # rust-preflight — fmt 실패 때 할 일이 한 가지다 (자동 적용 · 다시 검사)
    echo "$(cnt "$E/$RPF" '실패 시 사용자에게 `cargo fmt` 실행을 안내하라.') $(cnt "$E/$RPF" '확인이 실패했을 때만 Gotcha 2 · Step 1 대로 `cargo fmt --all` 을 적용하고 다시 검사한 뒤') $(grep -c '^2\. \*\*fmt 실패 시 자동 적용\*\*' "$E/$RPF") $(cnt "$E/$RPF" 'FAIL → rust-run `fmt`를 실행하여 자동 적용 후 재검사')" ;;
  SK-05)
    local tp ts ip is
    tp=$(awk '/server: \{/{f=1} f' "$E/react-kit/templates/vite.config.template.ts" | sed -nE 's/^ *port: ([0-9]+),.*/\1/p' | head -1)
    ts=$(awk '/server: \{/{f=1} f' "$E/react-kit/templates/vite.config.template.ts" | sed -nE 's/^ *strictPort: (true|false),.*/\1/p' | head -1)
    s=$(sect "$E/$RIN" '### 단계 2 ')
    ip=$(printf '%s\n' "$s" | sed -nE 's/^server: \{ port: ([0-9]+), strictPort: (true|false) \},$/\1/p'); is=$(printf '%s\n' "$s" | sed -nE 's/^server: \{ port: ([0-9]+), strictPort: (true|false) \},$/\2/p')
    echo "tpl=${tp:-X}/${ts:-X} init=${ip:-X}/${is:-X} same=$( [ -n "$tp" ] && [ "$tp/$ts" = "$ip/$is" ] && echo 1 || echo 0)"
    echo "$(cnt "$E/$RIN" '템플릿이 strictPort: true 라') $(cnt "$E/$RIN" '# devUrl 포트는 vite.config.ts 의 server.port 와 같게 둔다 — 단계 2 에서 넣은 strictPort: true 라 포트가 차면 옮기지 않고 멈춘다')"
    echo "$(cnt "$E/$RRU" '템플릿(`templates/vite.config.template.ts`)은 `strictPort: true` 라') $(cnt "$E/$RRU" 'react-init 으로 만든 프로젝트는 단계 2 에서 `vite.config.ts` 에 `strictPort: true` 를 넣어') $(cnt "$E/$RRU" '그 설정이 없는 프로젝트면 `pnpm vite dev --strictPort` 로 띄운다.') $(grep -c '^- \*\*`dev` 포트는 5173 에 묶여 있다 (`strictPort: true`)\*\*:' "$E/$RRU")"
    # react-l10n — 지워진 키 수 명령을 빈 입력 · 두 줄 입력에 돌린다 (0 건이 실패 종료 코드가 아니어야 한다)
    local lc o0 r0 o2
    lc=$(grep -F 'git diff -U0 -- src/infrastructure/i18n/locales/ | ' "$E/$RLN" | grep -F 'msgid ' | grep -vF msgstr | head -1 | sed 's/^ *git diff -U0 -- src\/infrastructure\/i18n\/locales\/ | //')
    o0=$(printf '' | bash -c "$lc"); r0=$?
    o2=$(printf -- '-msgid "a"\n-msgid "b"\n+msgid "c"\n' | bash -c "$lc")
    echo "l10n empty=$o0 rc=$r0 two=$o2" ;;
  SK-06)
    local code
    # 훅이 적는 사유 태그 줄기 — 변수로 끝나는 줄기(`fail:` · `env-dedup:`)는 뺀다
    code=$(cat "$E"/reflect-kit/hooks/*.sh | grep -ohE '"(skip|fail|fallback|warn|vocab|env-dedup):[A-Za-z0-9_/-]*' | tr -d '"' | sed -E 's/-+$//' | grep -v ':$' | sort -u)
    tagdoc() { printf '%s\n' "$1" | grep -oE '^- `[a-z-]+:[A-Za-z0-9_/<>-]*' | sed 's/^- `//' | sed -E 's/<[^>]*>//g; s/-+$//' | sort -u; }
    echo "code=$(printf '%s\n' "$code" | grep -c .) schema_missing=$(comm -23 <(printf '%s\n' "$code") <(tagdoc "$(sect "$E/$RSC" '## 3. ')") | grep -c .) design_missing=$(comm -23 <(printf '%s\n' "$code") <(tagdoc "$(sect "$E/$RDE" '## 에러 관측성')") | grep -c .)"
    echo "$(cnt "$E/$RRD" '버전: `') $(cnt "$E/$RRD" '버전은 `.claude-plugin/plugin.json` 의 `version` 을 본다.')"
    # (c) 기간 도중 멈춤 — 킷 시험을 끝 판 사본에서 돌리고, 같은 시험을 시작 커밋 판 라이브러리로 다시 돌린다 (음성 대조)
    local kc o r
    kc=$(kitcp "$E" rf reflect-kit) || return 2
    o=$(bash "$kc/$RCT" 2>&1); r=$?
    echo "test rc=$r $(printf '%s\n' "$o" | grep '^결과')"
    o=$(PROJECT_ID_LIB="$Bd/$RLIB" bash "$kc/$RCT" 2>&1); r=$?
    echo "start_lib rc=$r $(printf '%s\n' "$o" | grep '^결과') $(printf '%s\n' "$o" | grep -c '^불일치 도중 멈춤')"
    # (d) period · window 를 받는 두 스킬의 실행 줄에 고정 일수가 없고, 새 경고가 나오는 경우를 적었다
    echo "$(cnt "$E/$RDG" '"${CLAUDE_PLUGIN_ROOT}" 7 ') $(cnt "$E/$RDG" '"${CLAUDE_PLUGIN_ROOT}" <일수> ') $(cnt "$E/$RKZ" '"${CLAUDE_PLUGIN_ROOT}" 30 ') $(cnt "$E/$RKZ" '"${CLAUDE_PLUGIN_ROOT}" <일수> ') $(cnt "$E/$RDG" '또는 마지막 기록 뒤 Stop 실패 시도가 1 이상일 때만 싣는다') $(cnt "$E/$RDG" '엔트리가 있어도 마지막 기록 뒤에 Stop 실패 시도가 있으면')" ;;
  SK-07)
    bambu_gate "$E" > "$T/gate.py" || { echo "GATE_EXTRACT_FAIL"; return 2; }
    local v nd
    v=$(defaults read /Applications/BambuStudio.app/Contents/Info.plist CFBundleShortVersionString 2>/dev/null) || { echo "TOOL_MISSING BambuStudio"; return 2; }
    nd=$T/noenum; rm -rf "$nd"; mkdir -p "$nd/references/option-keys"
    grep -v "^enum$(printf '\t')" "$E/bambu-kit/skills/bambu-print-profile/references/option-keys/bambu-$v.tsv" > "$nd/references/option-keys/bambu-$v.tsv"
    # (a) enum 줄만 뺀 목록 · 온전한 목록 — 받지 않는 값 픽스처
    out=$(cd "$E" && SKILL_DIR="$nd" TARGET_SLICER=bambu python3 "$T/gate.py" bambu-kit/evals/gate-fixtures/process-seam-slope-type-invalid.json 2>&1); rc=$?
    echo "noenum unv_enum=$(printf '%s\n' "$out" | grep '^\[미검증\]' | grep -c 'enum 0 줄') reject=$(printf '%s\n' "$out" | grep -c '받지 않는 값') $(printf '%s\n' "$out" | grep '^RESULT' | head -1) rc=$rc"
    out=$(cd "$E" && SKILL_DIR=bambu-kit/skills/bambu-print-profile TARGET_SLICER=bambu python3 "$T/gate.py" bambu-kit/evals/gate-fixtures/process-seam-slope-type-invalid.json 2>&1); rc=$?
    echo "full reject=$(printf '%s\n' "$out" | grep -c '받지 않는 값 seam_slope_type') unv=$(printf '%s\n' "$out" | grep -c '^\[미검증\]') rc=$rc"
    # (b) 음성 대조 블록 (1) — 시험 파일 하나를 지운 킷 사본 · 온전한 사본
    bambu_check1 "$E" > "$T/check1.sh" || { echo "CHECK1_EXTRACT_FAIL"; return 2; }
    local kc
    kc=$(kitcp "$E" bam bambu-kit) || return 2
    out=$(cd "$kc" && S=bambu-kit/skills/bambu-print-profile/SKILL.md FX=bambu-kit/evals/gate-fixtures bash "$T/check1.sh" 2>&1); rc=$?
    echo "intact lines=$(printf '%s' "$out" | grep -c .) rc=$rc"
    rm "$kc/bambu-kit/evals/gate-fixtures/process-thin-baseline.json"
    out=$(cd "$kc" && S=bambu-kit/skills/bambu-print-profile/SKILL.md FX=bambu-kit/evals/gate-fixtures bash "$T/check1.sh" 2>&1); rc=$?
    local oz rz
    oz=$(cd "$kc" && S=bambu-kit/skills/bambu-print-profile/SKILL.md FX=bambu-kit/evals/gate-fixtures zsh "$T/check1.sh" 2>&1); rz=$?
    echo "deleted orphan=$(printf '%s\n' "$out" | grep -cx '폴더에 없음 process-thin-baseline.json') stop=$(printf '%s\n' "$out" | grep -c '^STOP') rc=$rc zsh_same=$( [ "$out" = "$oz" ] && [ "$rc" = "$rz" ] && echo 1 || echo 0)"
    # (c) 킷 블록에 더한 enum 없는 목록 대조 줄을 그대로 돌린다
    awk '/^NOENUM=\$\(mktemp -d -t noenum\)/{f=1} f{print} f&&/^SKILL_DIR="\$NOENUM"/{exit}' "$E/$BAM" > "$T/noenum.sh"
    out=$(cd "$E" && GATE="$T/gate.py" FX=bambu-kit/evals/gate-fixtures SKILL_DIR=bambu-kit/skills/bambu-print-profile TMPDIR="$T" bash "$T/noenum.sh" 2>&1)
    echo "kit_noenum lines=$(grep -c . "$T/noenum.sh") unv_enum=$(printf '%s\n' "$out" | grep '^\[미검증\]' | grep -c 'enum 0 줄') $(printf '%s\n' "$out" | grep -c '^exit=0$')"
    # (d) 두 자기 검사 블록 — SKILL_DIR 을 채우는 줄이 맨 앞에 있고, 채우면 돌고 비우면 멈춘다
    bambu_selfblocks "$E"
    # (e) 댓글 받기 블록 — 앞 실행의 댓글 페이지가 남은 폴더에서 가짜 curl 로 돌린다
    bambu_mw "$E" ;;
  SK-08)
    local l1 lst
    l1=$(grep '^1\. \*\*패턴으로 탐색한다\*\*' "$E/$OSK")
    lst=$(printf '%s\n' "$l1" | sed -nE 's/.*실제 파일을 찾는다 \(([^)]*)\)\..*/\1/p')
    echo "grep_list_env=$(printf '%s' "$lst" | grep -cF '.env*') grep_list_p8=$(printf '%s' "$lst" | grep -cF '.p8') glob_only=$(printf '%s\n' "$l1" | grep -cF '`.env*` · `**/*.p8` 은 Glob 으로 있는지만 본다')"
    python3 - "$E/$OEV" <<'PY'
import json, sys
d = json.load(open(sys.argv[1], encoding="utf-8"))
c = [x for x in d["cases"] if x.get("id") == "no-invented-paths"]
a = c[0]["assertions"] if c else []
new = "guide_does_not_invent_env_key() — .env.example 과 그 키를 읽는 코드에 없는 키 이름을 안내하지 않는다 (값이 든 .env 는 기준으로 삼지 않는다 — Gotcha 8)"
old = "guide_does_not_invent_env_key() — 실제 .env 에 없는 키 이름을 안내하지 않는다"
print("json=1 case=%d new=%d old=%d env_contains=%d" % (len(c), a.count(new), a.count(old), int(bool(c and c[0].get("setup", {}).get("env_contains")))))
PY
    local rows_ok=0 r
    while IFS= read -r r; do grep -qxF -- "$r" "$E/$OEX" && rows_ok=$((rows_ok + 1)); done < <(grep -E '^\| (실기기|유료 개발자 계정|앱 출시) \|' "$E/onboarding-kit/skills/setup-guide/references/format-checklist.md")
    echo "x16=$(cnt "$E/$OEX" 'Xcode 16+') ios14=$(cnt "$E/$OEX" 'iOS 14+') names=$(grep -ciE "$NAMES" "$E/$OEX") sim=$(grep -cE '시뮬레이터도 일부 지원|FCM 푸시도 일부 지원|시뮬레이터에서도 토큰은 받지만|iOS 16 이전 시뮬레이터는 APNs 불가' "$E/$OEX") x262=$(cnt "$E/$OEX" 'Xcode 26.2+') head=$(grep -cxF '| 요구 | 출처 | 막히는 것 | 우회 |' "$E/$OEX") rows=$rows_ok/3"
    awk '/^guide_gate\(\) \{/{p=1} p{print} p&&/^\}$/{exit}' "$E/$OSK" > "$T/gg.sh"
    local gb gz
    gb=$(cd "$E" && bash -c '. "$1"; guide_gate "$2" flutter; echo "rc=$?"' _ "$T/gg.sh" "$OEX" 2>&1)
    gz=$(cd "$E" && zsh -c '. "$1"; guide_gate "$2" flutter; echo "rc=$?"' _ "$T/gg.sh" "$OEX" 2>&1)
    echo "$(printf '%s\n' "$gb" | tr '\n' ' ')| zsh_same=$( [ "$gb" = "$gz" ] && echo 1 || echo 0)"
    # (d) G1 — 한 Step 에 출처 둘 · 다른 Step 에 0 인 입력 (전체 수는 2 = 2)
    printf '# t\n\n## Step 1\n\n**출처:** a\n\n**출처:** b\n\n## Step 2\n\n본문\n' > "$T/g1.md"
    gb=$(bash -c '. "$1"; guide_gate "$2" flutter | head -1' _ "$T/gg.sh" "$T/g1.md" 2>&1)
    gz=$(zsh -c '. "$1"; guide_gate "$2" flutter | head -1' _ "$T/gg.sh" "$T/g1.md" 2>&1)
    echo "misplaced $gb | zsh_same=$( [ "$gb" = "$gz" ] && echo 1 || echo 0)" ;;
  SK-09)
    mkdir -p "$T/tfx"; printf '%s\n' 'final effectiveColor = base ?? fallback;' '// ------------------' 'Widget _buildHeader() {' > "$T/tfx/sample.dart"
    local cells=0 dead=0 p row
    while IFS= read -r row; do
      p=$(printf '%s\n' "$row" | awk -F' \\| ' '{print $NF}' | sed -nE 's/^`(.*)` \|$/\1/p')
      [ -n "$p" ] || continue
      cells=$((cells + 1)); [ "$(grep -cE -- "$p" "$T/tfx/sample.dart")" -ge 1 ] || dead=$((dead + 1))
    done < <(sect "$E/$TAP" '## 카테고리 요약표' | grep -E '^\| [A-J] \|')
    local eb
    eb=$(sect "$E/$TAP" '### E ' | awk '/^```bash$/{b=1;next} b&&/^```$/{exit} b')
    eb=${eb//<대상 경로>/\"$T/tfx\"}
    echo "cells=$cells dead=$dead e_block=$(bash -c "$eb" 2>/dev/null | grep -c .) e_cell=$(grep -E '^\| E \|' "$E/$TAP" | grep -cF '아래 E 절의 grep 블록')" ;;
  SK-10)
    local l c1 c2
    l=$(grep '^1\. \*\*여는 방법\*\*' "$E/$AUI")
    c1=$(printf '%s\n' "$l" | grep -oE '`[^`]*mktemp -d[^`]*`' | head -1 | tr -d '`'); c2=$(printf '%s\n' "$l" | grep -oE '`[^`]*http\.server[^`]*`' | head -1 | tr -d '`')
    echo "$(printf '%s\n' "$l" | grep -cF '`D=$(mktemp -d) && cp .api/ui.html "$D/"`') $(printf '%s\n' "$l" | grep -cF '`python3 -m http.server 8765 --bind 127.0.0.1 --directory "${D:?폴더 변수가 비었다 — 두 명령을 한 셸에서 잇는다}" & sleep 1; kill -0 $! 2>/dev/null && echo "SERVING pid=$! dir=$D" || echo "NOT_SERVING 8765"`') $(printf '%s\n' "$l" | grep -cF '"$D/" && python3 -m http.server') $(printf '%s\n' "$l" | grep -cF 'Address already in use') $(printf '%s\n' "$l" | grep -cF '두 명령은 한 번의 셸 호출에서 잇는다') $(printf '%s\n' "$l" | grep -cF '다른 셸 호출에서 `kill $!` 를 쓰지 마라') $(printf '%s\n' "$l" | grep -cF '(같은 셸이면 `kill $!`)')"
    api_serve "$c1" "$c2"
    api_unset "$c2"
    toks "$(grep -F 'I-JSON 게이트 실패(' "$E/$AVE" | head -1)" '중복 키' 'NaN/Infinity' 'binary64' 'lone surrogate' '`-0`'
    echo "$(grep -cF '| `-0` 허용 | `0` |' "$E/$ACN") $(sect "$E/$ACN" '## 수치 기준' | awk '/^\|/{if(!t){b++;t=1}} !/^\|/{t=0} END{print b+0}')" ;;
  SK-11)
    local kc n
    echo "$(cnt "$E/$HRN" "for c in data['cases']") $(cnt "$E/$HRN" "for entry in data['cases']:") $(cnt "$E/$HRN" 'if not inb and ln.strip() in ("```bash", "```sh", "```shell", "```zsh"):') $(cnt "$E/$HRD" '게이트를 부르는 셸 블록(`bash` · `sh` · `shell` · `zsh` 펜스)도') $(cnt "$E/$HRD" '게이트를 부르는 `bash` 블록도') $(cnt "$E/$HEV" 'gate_blocks 는 게이트를 부르는 셸 블록(bash · sh · shell · zsh 펜스) 수를')"
    for n in intact sh_block; do
      kc=$(kitcp "$E" "hk-$n" howto-kit) || return 2
      [ $n = intact ] || { printf '\n```sh\n'; sect "$E/$HRD" '## 결정론 게이트 G1~G6' | awk '/^```bash$/{b=1; next} b&&/^```$/{exit} b'; printf '```\n'; } >> "$kc/howto-kit/skills/howto/SKILL.md"
      out=$(bash "$kc/howto-kit/evals/run-evals.sh" 2>&1); rc=$?
      local oz rz
      oz=$(zsh "$kc/howto-kit/evals/run-evals.sh" 2>&1); rz=$?
      echo "$n rc=$rc | $(printf '%s\n' "$out" | sed -nE 's/^FAIL  ([^ ]+).*/\1/p' | sort | paste -sd, -) | $(printf '%s\n' "$out" | grep '^EVALS total') | zsh rc=$rz same_verdict=$( [ "$(printf '%s\n' "$out" | grep '^EVALS total')" = "$(printf '%s\n' "$oz" | grep '^EVALS total')" ] && echo 1 || echo 0)"
    done ;;
  SK-12)
    # (a) backend — 다섯 필드 필수를 RFC 9457 요구로 적은 세 자리와 고친 문장
    echo "$(cnt "$E/$BAC" '`title`/`status`/`detail`/`instance` 필수.') $(cnt "$E/$BAC" '다섯 필드를 모두 넣는 것은 이 킷 규칙(`api-design.md` 원칙 3)이다 — RFC 9457 은 `type` 이 없으면 `about:blank` 로 보므로 누락을 RFC 위반으로 적지 않는다.') $(cnt "$E/$BAD" '| RFC 9457 problem+json 필수 필드 |') $(cnt "$E/$BAD" '| problem+json 필드 (이 킷 규칙 — 원칙 3) | 5개 (type, title, status, detail, instance). RFC 9457 은 `type` 이 없으면 `about:blank` 로 본다 |') $(cnt "$E/$BSP" '`type` URI 필드 필수') $(cnt "$E/$BSP" 'RFC 9457 에러(`type` URI 로 유형 식별 — 없으면 `about:blank`. 다섯 필드는 이 킷 규칙)')"
    # 근거 — 같은 레포 api-kit 연구 문서가 RFC 9457 §3.1 을 1 차 출처로 대조해 적은 줄 (바뀌지 않아야 한다)
    echo "basis=$(cnt "$E/docs/api/contract/error-status-contracts.md" '`type`이 없으면 `about:blank`로 간주되므로, 누락 자체를 계약 위반으로 잡지 않는다.')"
    # (b) infra — checkout 검사가 주석 한 줄 · 실제 스텝 · 따옴표 스텝을 가른다
    infra_ci_inputs "$T/ifx"
    awk '/^# 규칙 1: checkout 스텝 존재$/{f=1} f{print} f&&/^done$/{exit}' "$E/$ITS" > "$T/r1.sh"
    out=$(bash -c 'workflows=("$@"); violation=0; . "$0"; echo "violation=$violation"' "$T/r1.sh" "$T/ifx/comment.yml" "$T/ifx/step.yml" "$T/ifx/quoted.yml" 2>&1)
    echo "r1_lines=$(grep -c . "$T/r1.sh") $(printf '%s\n' "$out" | awk '{print $1}' | paste -sd' ' -)" ;;
  NA)
    echo "SC-00=$(mine "$B" "$END" "$SIG" | grep -cE '^scripts/release\.sh$|(^|/)marketplace\.json$|/plugin\.json$') DG-01=$(mine "$B" "$END" "$SIG" | grep -cx 'scripts/release.sh') RE-01=$(git diff --name-status "$B" "$END" | awk '$1=="A"' | grep -v '[[:space:]]\.harness/' | grep -c .)" ;;
  ER-01)
    local nu="" f
    # 파일마다 편집 전 판에 없던 URL — 고친 줄에 원래 있던 URL 은 새 URL 이 아니고, 다른 파일에서 옮겨 온 URL 은 새 URL 이다
    for f in "${FILES[@]}"; do nu="$nu$(comm -13 <(url < "$Bd/$f") <(url < "$E/$f"))
"; done
    nu=$(printf '%s' "$nu" | grep . | grep -vE '^https?://(127\.0\.0\.1|localhost)[:/]' | sort -u)   # 셸이 여는 로컬 주소는 출처가 아니다
    cat "$Bd"/.harness/.meta/evidence/phase*.md | url > "$T/evid.txt"
    echo "new_urls=$(printf '%s\n' "$nu" | grep -c .) not_in_evidence=$(comm -23 <(printf '%s\n' "$nu" | grep .) "$T/evid.txt" | grep -c .)"
    echo "notes_urls_not_in_evidence=$( { git show "$END:$NOTES" 2>/dev/null || true; } | url | comm -23 - "$T/evid.txt" | grep -c .)" ;;
  ER-02)
    local a
    a=$(added)
    echo "added=$(printf '%s\n' "$a" | grep -c .) k02=$(printf '%s\n' "$a" | grep -cE "$K02") names=$(printf '%s\n' "$a" | grep -ciE "$NAMES") tax_old=$(cnt "$E/$TAX" '같은 원칙이 **규칙 소스**에도 적용된다')" ;;
  ER-03)
    local nt g sha ok=0 fin s4=0 slug grp
    git cat-file -e "$END:$NOTES" 2>/dev/null && echo "notes_committed=1" || { echo "notes_committed=0"; return 0; }
    nt=$(git show "$END:$NOTES")
    toks "$nt" '## 커밋' '## 다룬 항목' '## 고치지 않은 항목과 이유' '## Final 에 넘기는 것' '## 다음 사이클 메모'
    # `## 커밋` 표 — 킷 묶음마다 한 행, 그 커밋이 서명돼 있고 그 묶음 경로만 건드린다
    for g in "${KITG[@]}"; do
      sha=$(printf '%s\n' "$nt" | awk '/^## /{s=$0} s=="## 커밋"' | grep -E "^\| $g \|" | grep -oE '[0-9a-f]{7,40}' | head -1)
      [ -n "$sha" ] && git rev-parse -q --verify "$sha^{commit}" >/dev/null || continue
      git merge-base --is-ancestor "$B" "$sha" && git merge-base --is-ancestor "$sha" "$END" || continue
      git log -1 --format=%B "$sha" | grep -qxF "$SIG" || continue
      [ "$(git show --name-only --format= "$sha" | grep . | while read -r p; do group_of "$p"; done | sort -u | paste -sd, -)" = "$g" ] && ok=$((ok + 1))
    done; echo "commit_rows=$ok/${#KITG[@]}"
    fin=$(printf '%s\n' "$nt" | awk '/^## /{s=$0} s=="## Final 에 넘기는 것"')
    for slug in kaizen-0924-p07-backend-kit:backend kaizen-0924-p08-infra-kit:infra kaizen-0924-p09-rust-kit:rust kaizen-0924-p11-planning-kit:planning; do
      grp=${slug#*:}; slug=${slug%%:*}
      sha=$(printf '%s\n' "$nt" | awk '/^## /{s=$0} s=="## 커밋"' | grep -E "^\| $grp \|" | grep -oE '[0-9a-f]{7,40}' | head -1)
      [ -n "$sha" ] && printf '%s\n' "$fin" | grep -F "$slug" | grep -qF "$sha" && s4=$((s4 + 1))
    done; echo "final_dg02_rows=$s4/4"
    # 버전 계획 · 문서 사이트 — 플러그인 파일이 바뀐 킷 열둘과 다시 만들 페이지 아홉을 적었는가
    echo "release_kits=$(for k in backend-kit flutter-toolkit design-kit infra-kit rust-kit react-kit reflect-kit bambu-kit onboarding-kit tone-kit api-kit howto-kit; do printf '%s\n' "$fin" | grep -qF "$k" && echo "$k"; done | grep -c .)/12 pages=$(for pg in fcm-ios-example.html visual-evidence-protocol.html project-detection.html snapshot-sealing-canonicalization.html gate-result-taxonomy.html api-design.html visual-change-protocol.html bambu-print-profile.html schema.html; do printf '%s\n' "$fin" | grep -qF "$pg" && echo "$pg"; done | grep -c .)/9"
    toks "$(printf '%s\n' "$nt" | awk '/^## /{s=$0} s=="## 다음 사이클 메모"')" 'claude -p' '판정 불가' 'adapter-dart-flutter.md' 'widget-inspector' 'fit-pal' '2026-09-02-api-kit-design.md' 'flutter-preflight' 'G91' 'locale-korean.md' 'design-reviewer' 'planning-reviewer' '2.7.0' 'RFC 7493' 'misplaced' 'harness-project.yaml.template' 'docs/infra/platform/cicd.md' 'build_runner-2.13.1'
    echo "not_other=$(not_other "$B" "$END" "$SIG" .claude-plugin/marketplace.json README.md CLAUDE.md .harness/.meta/orchestrator-audit-log.md \
      .harness/.meta/kaizen-failure-count.yaml .claude/kaizen-input/insights-report.md .github .harness/stale-values.yaml harness scripts .claude/skills \
      docs/index.html docs/kaizen ':(glob)docs/**/*.html' ':(glob)*/.claude-plugin/plugin.json' | grep -c .)" ;;
  AR-01)
    local g p v1 v2 v3 one=0 bad=0 c gs hs
    # 킷 묶음 열셋 경로만 넘기면 planning-kit/ · docs/design/ 처럼 이 계약이 안 고치는 킷 자리를 서명 없이 건드려도 0 이다
    echo "$(unsigned_on "$B" "$END" "$SIG" ':(glob)*-kit/**' flutter-toolkit ':(glob)docs/**' ':(exclude,glob)docs/**/*.html' ':(exclude)docs/kaizen' | grep -c .)"
    mine "$B" "$END" "$SIG" > "$T/mine.txt"
    # .harness/ 는 이 계약 이름이 든 파일만 허용한다 — verify_seal 은 조건 줄만 봐서 다른 Phase 개정 파일 · project.yaml 을 고쳐도 0 이다
    echo "$(grep -vxF -f <(printf '%s\n' "${FILES[@]}") "$T/mine.txt" | grep -cvE '^\.harness/(sprint-(contract|amendments|feedback)-kaizen-0924-f1-kit-followups|\.meta/kaizen-0924/f1-kit-followups-[a-z0-9-]+)\.md$') $(grep -cxF -f <(printf '%s\n' "${FILES[@]}") "$T/mine.txt")"
    for c in $(signed_commits); do
      gs=$(git show --name-only --format= "$c" | grep . | while read -r p; do group_of "$p"; done | sort -u | grep -c .)
      hs=$(git show --name-only --format= "$c" | grep -c '^\.harness/')
      if [ "$gs" -gt 1 ] || { [ "$gs" = 1 ] && [ "$hs" -gt 0 ]; }; then bad=$((bad + 1)); elif [ "$gs" = 1 ]; then one=$((one + 1)); fi
    done; echo "mixed=$bad one_kit=$one"
    echo "$(grep '^\.harness/sprint-contract-.*\.md$' "$T/mine.txt" | while read -r f; do [ -f "$E/$f" ] && (cd "$E" && verify_seal "$f"); done | grep -c '^SEAL_BROKEN')"
    (cd "$E" && verify_seal "$CF") | awk '{print $1}'
    echo "scope_same=$( [ "$(scope "$E/$CF" | grep -v '^\.harness/$' | sort)" = "$(printf '%s\n' "${FILES[@]}" | sort)" ] && echo 1 || echo 0) harness_line=$(scope "$E/$CF" | grep -cx '\.harness/')" ;;
  AR-02)
    echo "$( [ -f "$E/design-kit/skills/design-component/../../references/visual-change-protocol.md" ] && echo 1 || echo 0) $(grep -c '^### 6\. Codegen 실행$' "$E/$FLN") $(grep -cF '막는 요구는 세 칸으로 쓴다' "$E/onboarding-kit/skills/setup-guide/references/format-checklist.md") $(cnt "$E/$OEX" '`onboarding-kit/skills/setup-guide/references/format-checklist.md` §2') $(grep -c '^### 2\. ' "$E/onboarding-kit/skills/setup-guide/references/format-checklist.md") $( [ "$(grep -F 'I-JSON 검문' "$E/api-kit/skills/api-probe/SKILL.md" | head -1 | grep -oE 'NaN/Infinity|binary64|lone surrogate|중복 키|-0' | sort | paste -sd, -)" = "$(grep -F 'I-JSON 게이트 실패(' "$E/$AVE" | grep -oE 'NaN/Infinity|binary64|lone surrogate|중복 키|-0' | sort | paste -sd, -)" ] && echo 1 || echo 0)" ;;
  AR-03)
    local f d acc=""
    for f in "$RLB" "$RLI" "$RLR" "$RLP"; do
      d=$(git diff --no-index -U0 "$Bd/$f" "$E/$f" | grep -E '^[-+]' | grep -vE '^(\+\+\+|---)')
      acc="$acc$(printf '%s\n' "$d" | grep -c '^-')/$(printf '%s\n' "$d" | grep -c '^+')/$( [ "$(printf '%s\n' "$d" | grep '^+' | sed -e 's/^+//' -e 's/ — 2026-09-24 사이클$//')" = "$(printf '%s\n' "$d" | grep '^-' | sed 's/^-//')" ] && echo 1 || echo 0) "
    done; echo "${acc% }"
    python3 - "$Bd/$OEV" "$E/$OEV" "$Bd/$HEV" "$E/$HEV" <<'PY'
import json, sys
ob, oe, hb, he = (json.load(open(p, encoding="utf-8")) for p in sys.argv[1:5])
new = "guide_does_not_invent_env_key() — .env.example 과 그 키를 읽는 코드에 없는 키 이름을 안내하지 않는다 (값이 든 .env 는 기준으로 삼지 않는다 — Gotcha 8)"
old = "guide_does_not_invent_env_key() — 실제 .env 에 없는 키 이름을 안내하지 않는다"
s = json.dumps(oe, ensure_ascii=False).replace(json.dumps(new, ensure_ascii=False)[1:-1], json.dumps(old, ensure_ascii=False)[1:-1])
he2 = dict(he); hb2 = dict(hb); he2.pop("description", None); hb2.pop("description", None)
print("onboarding_same_but_one=%d howto_same_but_desc=%d gate_blocks_same=%d" % (int(json.loads(s) == ob), int(he2 == hb2), int(he.get("gate_blocks") == hb.get("gate_blocks"))))
PY
    bambu_gate "$Bd" > "$T/gate-b.py"; bambu_gate "$E" > "$T/gate-e.py"
    d=$(git diff --no-index -U0 "$T/gate-b.py" "$T/gate-e.py" | grep -E '^[-+]' | grep -vE '^(\+\+\+|---)')
    echo "gate -$(printf '%s\n' "$d" | grep -c '^-') +$(printf '%s\n' "$d" | grep -c '^+') | runner -$(git diff --no-index -U0 "$Bd/$HRN" "$E/$HRN" | grep -E '^-' | grep -vc '^---') +$(git diff --no-index -U0 "$Bd/$HRN" "$E/$HRN" | grep -E '^\+' | grep -vc '^+++') | guide_gate_outside_g1_same=$( [ "$(gg_out "$Bd/$OSK")" = "$(gg_out "$E/$OSK")" ] && echo 1 || echo 0) lib_outside_collect_status_same=$( [ "$(cs_out "$Bd/$RLIB")" = "$(cs_out "$E/$RLIB")" ] && echo 1 || echo 0)" ;;
  AP-01)
    local a vers
    a=$(added)
    vers=$(for g in flutter-toolkit design-kit infra-kit rust-kit react-kit reflect-kit bambu-kit onboarding-kit tone-kit api-kit howto-kit backend-kit planning-kit; do
      python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["version"])' "$E/$g/.claude-plugin/plugin.json"; done | sort -u)
    echo "versions=$(printf '%s\n' "$vers" | grep -c .) hits=$(printf '%s\n' "$vers" | while read -r v; do printf '%s\n' "$a" | grep -cF -- "$v"; done | paste -sd+ - | bc) readme_version_lines=$(cat "$E/$DRD" "$E/$RRD" | grep -c '^버전: `')" ;;
  AP-03)
    local f up=0 n=0
    for f in "${MDF[@]}"; do n=$((n + 1)); [ "$(barefence "$E/$f")" -le "$(barefence "$Bd/$f")" ] || up=$((up + 1)); done
    echo "md=$n bare_up=$up" ;;
  AP-04)
    local f n=0 same=0
    for f in "${FILES[@]}"; do case $f in */SKILL.md) n=$((n + 1)); [ "$(fmb "$Bd/$f")" = "$(fmb "$E/$f")" ] && fmb "$E/$f" | grep -q '^name: ' && same=$((same + 1)) ;; esac; done
    echo "skill_fm_same=$same/$n" ;;
  RE-02)
    local r rows_ok=0
    while IFS= read -r r; do grep -qxF -- "$r" "$E/$OEX" && rows_ok=$((rows_ok + 1)); done < <(grep -E '^\| (실기기|유료 개발자 계정|앱 출시) \|' "$E/onboarding-kit/skills/setup-guide/references/format-checklist.md")
    echo "rows=$rows_ok/3 $(m SK-05 | head -1 | awk '{print $3}') redefine=$(grep -F '13. **시각 산출물 규약은' "$E/$DCO" | grep -cE '[0-9]+ ?(개|회)')" ;;
  DG-02)
    printf '%s\n' "${MDF[@]}" > "$T/mdf.txt"
    bash "$K/sweep.sh" --pair "$Bd" "$E" "$T/mdf.txt" ;;
  DG-04)
    local sh_ out
    local acc=""
    for sh_ in /bin/sh bash zsh; do out=$(cd "$E" && "$sh_" howto-kit/evals/run-evals.sh 2>&1); acc="$acc$sh_ rc=$? $(printf '%s\n' "$out" | tail -1) | "; done; echo "${acc% | }"
    out=$(cd "$E" && sh onboarding-kit/skills/setup-guide/evals/run-gate-evals.sh 2>&1); echo "onboarding rc=$? $(printf '%s\n' "$out" | tail -1)"
    bash -n "$E/$HRN"; local n1=$?
    out=$(shellcheck -s sh "$E/$HRN" 2>&1); echo "runner bash_n=$n1 shellcheck_rc=$? lines=$(printf '%s' "$out" | grep -c .) | gate_py_compile=$(bambu_gate "$E" > "$T/gc.py" && python3 -m py_compile "$T/gc.py" && echo 0 || echo 1)"
    bash -n "$E/$RLIB"; n1=$?
    echo "reflect lib_bash_n=$n1 lib_shellcheck_lines=$(shellcheck -s bash "$E/$RLIB" 2>&1 | grep -c .) test_shellcheck_lines=$(shellcheck "$E/$RCT" 2>&1 | grep -c .) | design_gate_py_compile=$(design_gate "$E" > "$T/dgc.py" && python3 -m py_compile "$T/dgc.py" && echo 0 || echo 1)" ;;
  DG-05)
    local k out bad=0 kitfail=0 n=0
    for k in flutter-toolkit design-kit infra-kit rust-kit react-kit reflect-kit bambu-kit onboarding-kit tone-kit api-kit howto-kit backend-kit planning-kit; do
      out=$(cd "$E" && python3 scripts/validate-plugin.py "$k" 2>&1) || kitfail=$((kitfail + 1)); n=$((n + 1))
      bad=$((bad + $(printf '%s\n' "$out" | grep -E '^ *V[0-9]+' | grep -vcE '— (OK|SKIP)')))
    done; echo "kits=$n kitfail=$kitfail bad_v=$bad"
    out=$(cd "$E" && python3 scripts/sync-docs.py --check-only 2>&1); echo "sync_rc=$? $(printf '%s\n' "$out" | grep -c '모든 README가 동기화 상태입니다')"
    out=$(cd "$E" && python3 scripts/run-evals.py 2>&1); echo "evals_rc=$? $(printf '%s\n' "$out" | grep '^Total')"
    python3 - "$E/.harness/stale-values.yaml" "$Bd" "$E" "${FILES[@]}" <<'PY'
# 옛 값 등록부의 old 값을 마흔한 파일에서 직접 센다 — scripts/check-stale-values.py 는 킷 폴더 대부분을 훑지 않는다 (러닝북 측정 구멍 목록)
# allow 에 적힌 (값, 경로) 짝은 뺀다 — 등록부가 「고치면 안 되는 자리」 로 정한 곳이다. 파일마다 시작 커밋 판과 비교해 는 파일을 센다
import sys, pathlib
yml, before, after, files = sys.argv[1], pathlib.Path(sys.argv[2]), pathlib.Path(sys.argv[3]), sys.argv[4:]
vals, cur = [], None
for line in open(yml, encoding="utf-8"):
    t = line.strip()
    if t.startswith("- old:"):
        cur = {"old": t[6:].strip().strip('"').strip("'"), "allow": set()}; vals.append(cur)
    elif t.startswith("- path:") and cur is not None:
        cur["allow"].add(t[7:].strip().strip('"').strip("'"))
def hits(root, f):
    return sum((root / f).read_text(encoding="utf-8").count(v["old"]) for v in vals if v["old"] and f not in v["allow"])
hb = {f: hits(before, f) for f in files}; he = {f: hits(after, f) for f in files}
up = [f for f in files if he[f] > hb[f]]
print("stale_old=%d files=%d hits_start=%d hits_end=%d files_up=%d" % (len(vals), len(files), sum(hb.values()), sum(he.values()), len(up)))
PY
    ;;
  DG-06)  # 사이클 검사 — 이 계약 몫 줄만 본다. docs-site-regen 은 kaizen-0924-final 몫
    python3 scripts/validate-post-kaizen.py --since "$B" --verbose > "$T/vpk.txt" 2>&1
    grep -E '\] . (scope-isolation|doc-contracts): ' "$T/vpk.txt" | awk '{print $5, $2}'
    python3 scripts/validate-doc-contracts.py -v 2>&1 | awk -F' → ' '/^ *검사: /{a=$1; sub(/^ *검사: /,"",a); sub(/:[0-9]+$/,"",a); print a; print $2}' | sort -u > "$T/dc.txt"
    echo "doc_checked=$(grep -c . "$T/dc.txt") doc_mine=$(comm -12 "$T/dc.txt" <(mine "$B" "$END" "$SIG") | grep -c .)"
    awk '/ scope-isolation: /{f=1;next} /^\[ /{f=0} f&&/^ +[0-9a-f]{7,40}$/{print $1}' "$T/vpk.txt" > "$T/viol.txt"
    echo "violators=$(grep -c . "$T/viol.txt") mine=$(while read -r c; do git log -1 --format=%B "$c" | grep -qxF "$SIG" && echo "$c"; done < "$T/viol.txt" | grep -c .)" ;;
  *) echo "UNKNOWN_ID $1"; return 2 ;;
  esac
}
# design_gate <판 폴더> — 결정 전파 게이트 python 블록 (문서 머리 docstring 으로 찾는다)
design_gate() { python3 - "$1/$DVP" <<'PY'
import re, sys
s = open(sys.argv[1], encoding="utf-8").read()
m = re.search(r'```python\n(#!/usr/bin/env python3\n"""Decision Propagation Coverage Gate.*?)```', s, re.S)
if not m:
    sys.exit(2)
print(m.group(1), end="")
PY
}
# dg_inputs <폴더> — 결정 전파 게이트 입력 다섯. 기대 종료 코드: 1 · 2 · 0 · 3 · 1 (gate-exit-codes.md 네 값)
dg_inputs() { mkdir -p "$1"
  printf 'decisions:\n  - decision_id: DEC-20260925-001\n    source: .design/approvals/x.md\n    status: approved\n' > "$1/i1.yaml"
  printf 'decisions:\n  - decision_id: D-1\n    source: .design/approvals/x.md\n    required_surfaces:\n      - surface_id: a\n        golden: g.png\n        assertions: ["main visible"]\n' > "$1/i2.yaml"
  printf 'decisions:\n  - decision_id: DEC-20260813-001\n    source: .design/approvals/20260813-dashboard.md\n    status: approved\n    required_surfaces:\n      - surface_id: dashboard.desktop.main\n        golden: g.png\n        assertions: ["main visible", "group rows >= 1", "container height > 0"]\n    excluded_surfaces:\n      - surface_id: onboarding.mobile\n        reason: "decision does not apply"\n' > "$1/i3.yaml"
  printf 'decisions:\n  - decision_id: DEC-20260925-002\n    source: .design/approvals/x.md\n    excluded_surfaces:\n      - surface_id: onboarding.mobile\n        reason: "not applicable"\n' > "$1/i4.yaml"
  printf 'decisions:\n  - decision_id: DEC-20260925-003\n    source: .design/approvals/x.md\n    required_surfaces:\n      - surface_id: a\n        golden: g.png\n        assertions: ["main visible"]\n    excluded_surfaces:\n      - surface_id: b\n' > "$1/i5.yaml"; }
# infra_ci_inputs <폴더> — 주석에만 checkout 이름 · 실제 스텝 · 작은따옴표 SHA 스텝
infra_ci_inputs() { mkdir -p "$1"
  printf 'on: push\njobs:\n  b:\n    runs-on: ubuntu-latest\n    steps:\n      # - uses: actions/checkout@v4\n      - run: echo hi\n' > "$1/comment.yml"
  printf 'on: push\njobs:\n  b:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v4\n' > "$1/step.yml"
  printf "on: push\njobs:\n  b:\n    runs-on: ubuntu-latest\n    steps:\n      - name: co\n        uses: 'actions/checkout@8f4b7f84864484a7bf31766abe9204da3cbe65b3'\n" > "$1/quoted.yml"; }
# gg_out · cs_out — 바꾼 G1 블록 · collect_status 함수 밖 줄만 (바꾸지 않을 곳 대조용)
gg_out() { awk '/^guide_gate\(\) \{/{p=1} p{print} p&&/^\}$/{exit}' "$1" | awk '/^  # G1 출처 원장 완전성/{s=1} /^  # G2 미검증 마커/{s=0} !s'; }
cs_out() { awk '/^collect_status\(\) \{/{s=1} s&&/^\}$/{s=0; next} !s' "$1"; }
# bambu_selfblocks <판 폴더> — 두 자기 검사 블록(`S="$SKILL_DIR/SKILL.md"` 줄, 바로 앞 SKILL_DIR 줄이 있으면 그 줄부터 닫는 펜스까지)을
#   기준 폴더를 채워서 · 비워서 돌린다. 시작 커밋 판에는 채울 자리가 없어 SKILL_DIR 을 지운 환경에서 그대로 돈다
bambu_selfblocks() { local d=$T/sb k heads fs=0 st=0 o
  rm -rf "$d"; mkdir -p "$d"
  heads=$(python3 - "$1/$BAM" "$d" <<'PY'
import sys
L = open(sys.argv[1], encoding="utf-8").read().split("\n")
starts = [i for i, l in enumerate(L) if l.startswith('S="$SKILL_DIR/SKILL.md"')]
h = 0
for k, s in enumerate(starts, 1):
    if s > 0 and L[s - 1].startswith("SKILL_DIR=<이 스킬의 기준 폴더>"):
        s -= 1
        h += 1
    e = next(j for j in range(s, len(L)) if L[j] == "```")
    open(f"{sys.argv[2]}/blk{k}.sh", "w", encoding="utf-8").write("\n".join(L[s:e]) + "\n")
print(f"{h}/{len(starts)}")
PY
) || return 2
  sed 's#^SKILL_DIR=<이 스킬의 기준 폴더>#SKILL_DIR=bambu-kit/skills/bambu-print-profile#' "$d/blk1.sh" > "$d/fill1.sh"
  o=$(cd "$1" && env -u SKILL_DIR bash "$d/fill1.sh" 2>&1)
  printf '%s\n' "$o" | grep -qx 'SELFTEST PASS' && printf '%s\n' "$o" | grep -qx 'exit=0' && fs=1
  for k in 1 2; do
    sed 's#^SKILL_DIR=<이 스킬의 기준 폴더>#SKILL_DIR=#' "$d/blk$k.sh" > "$d/empty$k.sh"
    o=$(cd "$1" && env -u SKILL_DIR bash "$d/empty$k.sh" 2>&1) && continue
    printf '%s\n' "$o" | grep -q '^STOP /SKILL.md 가 없다' && st=$((st + 1))
  done
  echo "selfblocks heads=$heads filled_selftest_pass=$fs empty_stop=$st/2"; }
# bambu_mw <판 폴더> — MakerWorld 받기 블록을 가짜 curl 로 돌린다. 폴더에 앞 실행의 댓글 페이지(59 개)를 미리 둔다
bambu_mw() { local d=$T/mw o
  rm -rf "$d"; mkdir -p "$d/bin" "$d/out"
  cat > "$d/bin/curl" <<'SH'
#!/usr/bin/env bash
# 가짜 curl — -o 파일에 주소별 JSON 을 쓰고 -w 형식의 %{http_code} 를 200 으로 바꿔 찍는다
o= w= u=
while [ $# -gt 0 ]; do case $1 in -o) o=$2; shift 2 ;; -w) w=$2; shift 2 ;; -*) shift ;; *) u=$1; shift ;; esac; done
case $u in
  */instances) printf '{"hits":[],"total":0}' > "$o" ;;
  *design-service/design/*) printf '{"title":"t","commentCount":2,"instances":[]}' > "$o" ;;
  *commentandrating*) printf '{"hits":[{"comment":"a"},{"comment":"b"}],"total":2}' > "$o" ;;
esac
printf "${w//%\{http_code\}/200}"
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
  python3 -c 'import json, sys; json.dump({"hits": [{"comment": "old"}] * 59, "total": 159}, open(sys.argv[1], "w"))' "$d/out/comments-100.json"
  o=$(PATH="$d/bin:$PATH" MWOUT="$d/out" bash "$d/run.sh" 2>&1)
  echo "mw $(printf '%s\n' "$o" | sed -nE 's/^comments total ([0-9]+) · 받은 hits ([0-9]+) \(페이지 ([0-9]+)\).*/total=\1 hits=\2 pages=\3/p') warn=$(printf '%s\n' "$o" | grep -c '^WARN') stale_left=$( [ -f "$d/out/comments-100.json" ] && echo 1 || echo 0)"; }
# bambu_gate <판 폴더> — 완료 검사 python 본문 (음성 대조 블록과 같은 방식으로 뽑는다)
bambu_gate() { local s=$1/$BAM a b
  a=$(grep -n '^TARGET_SLICER=.* python3 - ' "$s" | head -1 | cut -d: -f1); [ -n "$a" ] || return 2
  b=$(awk -v s="$a" 'NR>s && $(0)=="PY" {print NR; exit}' "$s"); [ -n "$b" ] || return 2
  sed -n "$((a + 1)),$((b - 1))p" "$s" | grep -q RESULT || return 2
  sed -n "$((a + 1)),$((b - 1))p" "$s"; }
# bambu_check1 <판 폴더> — 음성 대조 블록의 (1) 확인 부분 (`# (1) 폴더의 시험 파일이` 줄부터 그 확인을 닫는 `fi` 까지)
bambu_check1() { python3 - "$1/$BAM" <<'PY'
import sys
L = open(sys.argv[1], encoding="utf-8").read().split("\n")
s = next(i for i, l in enumerate(L) if l.startswith("# (1) 폴더의 시험 파일이"))
i = next(i for i in range(s, len(L)) if L[i].startswith('if [ -n "$MISSING'))
e = i if L[i].rstrip().endswith("fi") else next(j for j in range(i, len(L)) if L[j] == "fi")
print("\n".join(L[s:e + 1]))
PY
}
# api_serve <폴더 만드는 명령> <서버 명령> — 두 명령을 차례로 bash 로 돌려 셸이 서버에 묶이는지 · 응답 · 판정 줄 · 찍힌 번호로 내려지는지 · 포트가 차 있을 때 판정 줄을 잰다.
# 포트는 비어 있는 번호로 바꿔 돈다 (이 맥에서 8765 가 이미 쓰일 수 있다)
api_serve() { local d=$T/apirun p out rc pid left
  rm -rf "$d"; mkdir -p "$d/.api"; printf '<!doctype html><title>t</title>\n' > "$d/.api/ui.html"
  p=$(python3 -c 'import socket; s=socket.socket(); s.bind(("127.0.0.1",0)); print(s.getsockname()[1]); s.close()')
  printf '%s\n%s\n' "${1//8765/$p}" "${2//8765/$p}" > "$d/run.sh"
  # 셸이 서버에 묶이면 4 초 뒤 알람으로 끊겨 142 가 나온다. 끊겼다는 셸 알림은 버린다
  rc=$( { (cd "$d" && exec perl -e 'alarm 4; exec @ARGV' bash run.sh > "$d/out.txt" 2>&1); echo $?; } 2>/dev/null )
  # 셸이 돌아온 그때의 출력만 본다 — 뒤에서 도는 서버가 나중에 쓰는 줄은 도구 출력에 실리지 않는다 (검토 2 회차 R1)
  cp "$d/out.txt" "$d/out-exit.txt"
  out=$(python3 - "$p" <<'PY'
import sys, time, urllib.request
p = sys.argv[1]; code = 0
for _ in range(40):
    try:
        code = urllib.request.urlopen("http://127.0.0.1:%s/ui.html" % p, timeout=1).status; break
    except Exception:
        time.sleep(0.1)
print(code)
PY
)
  # 판정 줄에 찍힌 번호로 내린다 — 다른 셸 호출에서 $! 로 내리는 길은 서버를 남긴다
  pid=$(sed -nE 's/^SERVING pid=([0-9]+) .*/\1/p' "$d/out-exit.txt")
  [ -n "$pid" ] && kill "$pid" 2>/dev/null; python3 -c 'import time; time.sleep(0.5)'
  left=$(pgrep -f "http.server $p" | grep -c .)
  pkill -f "http.server $p" 2>/dev/null
  printf 'run rc=%s blocked=%s http=%s serving_line=%s left_after_kill=%s | ' "$rc" "$( [ "$rc" = 142 ] && echo 1 || echo 0)" "$out" "$(grep -c '^SERVING pid=' "$d/out-exit.txt")" "$left"
  # 포트를 먼저 다른 서버가 쥔 경우 — 그 서버는 살아 있어야 하고 우리 서버는 판정 줄을 남기고 끝나야 한다
  mkdir -p "$d/blk"; printf 'blocker\n' > "$d/blk/ui.html"
  python3 -c 'import subprocess,sys; subprocess.Popen([sys.executable,"-m","http.server",sys.argv[1],"--bind","127.0.0.1"], cwd=sys.argv[2], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)' "$p" "$d/blk"
  python3 - "$p" <<'PY'
import sys, time, urllib.request
for _ in range(40):
    try:
        urllib.request.urlopen("http://127.0.0.1:%s/ui.html" % sys.argv[1], timeout=1); break
    except Exception:
        time.sleep(0.1)
PY
  { (cd "$d" && exec perl -e 'alarm 4; exec @ARGV' bash run.sh > "$d/out2.txt" 2>&1); } 2>/dev/null
  cp "$d/out2.txt" "$d/out2-exit.txt"
  python3 -c 'import time; time.sleep(1)'
  out=$(python3 -c 'import sys,urllib.request; print(urllib.request.urlopen("http://127.0.0.1:%s/ui.html" % sys.argv[1], timeout=2).read().decode().strip())' "$p" 2>/dev/null)
  echo "busy not_serving_line=$(grep -c '^NOT_SERVING' "$d/out2-exit.txt") blocker_alive=$( [ "$out" = blocker ] && echo 1 || echo 0)"
  pkill -f "http.server $p" 2>/dev/null; return 0; }
# api_unset <서버 명령> — 폴더 변수가 빈 채(명령마다 새 셸이 뜨는 도구) 서버 명령만 돌려, 지금 폴더의 .api/ 가 열리는지 잰다
api_unset() { local d=$T/apiun p code
  rm -rf "$d"; mkdir -p "$d/.api"; printf 'secret\n' > "$d/.api/credentials.local.json"; printf '<title>t</title>\n' > "$d/.api/ui.html"
  p=$(python3 -c 'import socket; s=socket.socket(); s.bind(("127.0.0.1",0)); print(s.getsockname()[1]); s.close()')
  { (cd "$d" && exec perl -e 'alarm 4; exec @ARGV' env -u D bash -c "${1//8765/$p}" > "$d/out.txt" 2>&1); } 2>/dev/null
  code=$(python3 - "$p" <<'PY'
import sys, time, urllib.request
p = sys.argv[1]; code = 0
for _ in range(15):
    try:
        code = urllib.request.urlopen("http://127.0.0.1:%s/.api/credentials.local.json" % p, timeout=1).status; break
    except Exception:
        time.sleep(0.1)
print(code)
PY
)
  pkill -f "http.server $p" 2>/dev/null
  echo "unset_d served=$code guard_msg=$(grep -c 'D:' "$d/out.txt")"; }
```

```bash
#!/usr/bin/env bash
# sweep.sh — 편집기와 같은 조건(markdownlint-cli2 · MD013 끔)으로 규칙별 경고 수를 센다
#   --count <파일> <규칙>          그 파일의 그 규칙 경고 수
#   --pair <옛 폴더> <새 폴더> <목록> 목록의 파일마다 두 판의 규칙별 수를 비교해 는 규칙을 낸다 (옛 판에 없으면 빈 파일로 본다)
# 더한 줄만 보면 손대지 않은 옆 줄에 붙는 경고(MD022 · MD032 · MD024)를 놓친다 (러닝북 — Phase 7 · 8 · 9 · 11 실측)
# 린터가 안 돌면 0 이 조용히 나온다 — 돌았다는 줄(Linting: 1 file)이 없으면 멈춘다
set -u
DIR=$(cd "$(dirname "$0")" && pwd)
rules() { local out
  out=$("$DIR/node_modules/.bin/markdownlint-cli2" --config "$DIR/cfg.markdownlint-cli2.jsonc" "$1" 2>&1)
  printf '%s\n' "$out" | grep -q '^Linting: 1 file' || return 2
  printf '%s\n' "$out" | sed -nE 's/^[^ ]*:[0-9]+(:[0-9]+)? (error|warning) (MD[0-9]+)\/.*/\3/p' | sort | uniq -c | awk '{print $2, $1}'; }
case ${1:-} in
  --count)
    r=$(rules "$2") || { echo "LINT_NOT_RUN $2"; exit 2; }
    printf '%s\n' "$r" | awk -v k="$3" '$1==k{n=$2} END{print n+0}' ;;
  --pair)
    A=$2 Z=$3 L=$4 up=0 n=0 W=$(mktemp -d "${TMPDIR:-/tmp}/sw.XXXXXX") || exit 2
    trap 'rm -rf "$W"' EXIT
    while IFS= read -r f; do
      [ -n "$f" ] || continue
      n=$((n + 1)); mkdir -p "$W/$(dirname "$f")"
      if [ -f "$A/$f" ]; then cp "$A/$f" "$W/$f"; else : > "$W/$f"; fi
      O=$(rules "$W/$f") || { echo "LINT_NOT_RUN old $f"; exit 2; }
      N=$(rules "$Z/$f") || { echo "LINT_NOT_RUN new $f"; exit 2; }
      U=$(join -a 2 -e 0 -o 0,1.2,2.2 <(printf '%s\n' "$O" | grep . | sort) <(printf '%s\n' "$N" | grep . | sort) \
        | awk '$3 > $2 {printf "%s%s:%s>%s", (k++ ? " " : ""), $1, $2, $3}')
      [ -z "$U" ] || { up=$((up + 1)); echo "UP $f $U"; }
    done < "$L"
    echo "files=$n files_up=$up" ;;
  *) echo "usage: sweep.sh --count <파일> <규칙> | --pair <옛 폴더> <새 폴더> <목록>"; exit 2 ;;
esac
```

### 봉인 전 실측 — 예행 판 · 시작 커밋 판 · 예행 변형

예행 판은 이 계약 초안을 봉인해 커밋하고 `mock.py` 를 킷 묶음마다 한 커밋으로 적용한 뒤 `end_sha` · notes 모의본 · `end_sha` 까지 올린 예행 저장소(변형 `base`)다.
시작 커밋 판은 같은 저장소에서 `END_OVERRIDE` 를 시작 커밋으로 둔 값이다. 값은 `m <조건 ID>` 출력 그대로이고 여러 줄은 ` ⏎ ` 로 이었다.
전체 출력은 스크래치 `kaizen/f1kit/out-final-v3.txt`(예행 판) · `out-start-v2.txt` · `out-start-v3-sk10.txt`(시작 커밋 판 — 측정이 바뀐 SK-10 만 다시 쟀다) · `out-variants-v3.txt`(변형) · `out-variants-oldhelpers.txt`(새 변형 셋을 고치기 전 도우미 `kv2/` 로 잰 대조) · `out-del-v3.txt`(문장 삭제)에 있다 (2026-09-25, 검토 `f1-kit-followups-review.md` 의 고칠 것 C1 ~ C8 반영 뒤 다시 잰 값).
검토 2 회차 R1 을 넣은 뒤 BUILD 가 다시 잰 것: 예행 판 스물일곱 측정 전부 `out-final-r1.txt`(SK-10 만 바뀌고 나머지는 위 표 그대로) · 시작 커밋 판 SK-10 `out-start-r1-sk10.txt` ·
2 회차 전 초안 명령과 R1 명령을 같은 `api_serve` · `api_unset` 에 넣은 대조 `out-r1-old-vs-new.txt` · 문장 삭제 `out-del-r1.txt`.

```text
조건   예행 판 (기대값)                                                                                     시작 커밋 판 (양성 대조)
SK-01  1 1 1 1 ⏎ 1 1 ⏎ 1 ⏎ 1 ⏎ backend=13/13 infra=13/13 rust=8/8 planning=1/1 ⏎ files=136 files_up=0        0 0 0 0 ⏎ 0 0 ⏎ 0 ⏎ 0 ⏎ backend=13/17 infra=13/15 rust=8/9 planning=1/2 ⏎ UP 네 줄 ⏎ files=132 files_up=4
SK-02  0 0 0 1 2 0 ⏎ 0 4 1 1 ⏎ 1 1 1 1 ⏎ 0 1                                                             1 1 1 0 0 0 ⏎ 4 0 1 0 ⏎ 0 0 0 0 ⏎ 1 0
SK-03  1 ⏎ 7/7 ⏎ 0 1 ⏎ gate i1=1 i2=2 i3=0 i4=3 i5=1                                                       0 ⏎ 6/7 ⏎ 1 0 ⏎ gate i1=0 i2=0 i3=0 i4=0 i5=0
SK-04  1 1 | 0 0 ⏎ 0 1 1 1                                                                                 0 0 | 1 1 ⏎ 1 0 1 1
SK-05  tpl=5173/true init=5173/true same=1 ⏎ 0 1 ⏎ 0 1 1 1 ⏎ l10n empty=0 rc=0 two=2                      tpl=5173/true init=X/X same=0 ⏎ 1 0 ⏎ 1 0 0 1 ⏎ l10n empty=0 rc=1 two=2
SK-06  code=14 schema_missing=0 design_missing=0 ⏎ 0 1 ⏎ test rc=0 결과: 11 경우 중 불일치 0 ⏎            code=14 schema_missing=2 design_missing=2 ⏎ 1 0 ⏎ test rc=0 결과: 10 경우 중 불일치 0 ⏎
       start_lib rc=1 결과: 11 경우 중 불일치 1 1 ⏎ 0 2 0 1 2 1                                            start_lib rc=0 결과: 10 경우 중 불일치 0 0 ⏎ 2 0 1 0 0 0
SK-07  noenum unv_enum=1 reject=0 RESULT: PASS rc=0 ⏎ full reject=1 unv=1 rc=1 ⏎ intact lines=0 rc=0 ⏎    noenum unv_enum=0 reject=0 RESULT: PASS rc=0 ⏎ full reject=1 unv=1 rc=1 ⏎ intact lines=0 rc=0 ⏎
       deleted orphan=1 stop=1 rc=1 zsh_same=1 ⏎ kit_noenum lines=4 unv_enum=1 1 ⏎                         deleted orphan=0 stop=0 rc=0 zsh_same=1 ⏎ kit_noenum lines=0 unv_enum=0 0 ⏎
       selfblocks heads=2/2 filled_selftest_pass=1 empty_stop=2/2 ⏎                                        selfblocks heads=0/2 filled_selftest_pass=0 empty_stop=0/2 ⏎
       mw total=2 hits=2 pages=1 warn=0 stale_left=0                                                       mw total=2 hits=61 pages=2 warn=1 stale_left=1
SK-08  grep_list_env=0 grep_list_p8=0 glob_only=1 ⏎ json=1 case=1 new=1 old=0 env_contains=1 ⏎            grep_list_env=1 grep_list_p8=1 glob_only=0 ⏎ json=1 case=1 new=0 old=1 env_contains=1 ⏎
       x16=0 ios14=0 names=0 sim=0 x262=2 head=1 rows=3/3 ⏎ (검사 함수 다섯 줄) GATE_PASS rc=0 | zsh_same=1 ⏎ x16=2 ios14=1 names=5 sim=3 x262=0 head=0 rows=0/3 ⏎ (검사 함수 다섯 줄) GATE_PASS rc=0 | zsh_same=1 ⏎
       misplaced G1_LEDGER FAIL steps=2 ledger=2 misplaced=2 | zsh_same=1                                  misplaced G1_LEDGER PASS steps=2 ledger=2 | zsh_same=1
SK-09  cells=2 dead=0 e_block=1 e_cell=1                                                                   cells=3 dead=1 e_block=1 e_cell=0
SK-10  1 1 0 1 1 1 0 ⏎ run rc=0 blocked=0 http=200 serving_line=1 left_after_kill=0 |                     0 0 1 0 0 0 0 ⏎ run rc=142 blocked=1 http=200 serving_line=0 left_after_kill=1 |
       busy not_serving_line=1 blocker_alive=1 ⏎ unset_d served=0 guard_msg=1 ⏎ 1 1 1 1 1 ⏎ 1 1          busy not_serving_line=0 blocker_alive=1 ⏎ unset_d served=0 guard_msg=0 ⏎ 1 0 0 1 1 ⏎ 0 1
SK-11  0 1 1 1 0 1 ⏎ intact rc=0 |  | EVALS total=33 pass=33 fail=0 | zsh rc=0 same_verdict=1 ⏎         1 0 0 0 1 0 ⏎ intact rc=0 |  | EVALS total=33 pass=33 fail=0 | zsh rc=0 same_verdict=1 ⏎
       sh_block rc=1 | blocks-declared | EVALS total=37 pass=36 fail=1 | zsh rc=1 same_verdict=1          sh_block rc=0 |  | EVALS total=33 pass=33 fail=0 | zsh rc=0 same_verdict=1
SK-12  0 1 0 1 0 1 ⏎ basis=1 ⏎ r1_lines=9 VIOLATION PASS PASS violation=1                                  1 0 1 0 1 0 ⏎ basis=1 ⏎ r1_lines=8 PASS PASS PASS violation=0
NA     SC-00=0 DG-01=0 RE-01=0                                                                             —
ER-01  new_urls=6 not_in_evidence=0 ⏎ notes_urls_not_in_evidence=0                                        new_urls=0 not_in_evidence=0 ⏎ notes_urls_not_in_evidence=0
ER-02  added=172 k02=0 names=0 tax_old=0                                                                   added=0 k02=0 names=0 tax_old=1
ER-03  notes_committed=1 ⏎ 1 1 1 1 1 ⏎ commit_rows=13/13 ⏎ final_dg02_rows=4/4 ⏎                          —
       release_kits=12/12 pages=9/9 ⏎ 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 ⏎ not_other=0
AR-01  0 ⏎ 0 41 ⏎ mixed=0 one_kit=13 ⏎ 0 ⏎ SEAL_OK ⏎ scope_same=1 harness_line=1                          —
AR-02  1 1 1 1 1 1                                                                                         1 1 1 0 1 0
AR-03  4/4/1 2/2/1 1/1/1 1/1/1 ⏎ onboarding_same_but_one=1 howto_same_but_desc=1 gate_blocks_same=1 ⏎    0/0/1 0/0/1 0/0/1 0/0/1 ⏎ (같음) ⏎
       gate -2 +3 | runner -3 +4 | guide_gate_outside_g1_same=1 lib_outside_collect_status_same=1         gate -0 +0 | runner -0 +0 | guide_gate_outside_g1_same=1 lib_outside_collect_status_same=1
AP-01  versions=10 hits=0 readme_version_lines=0                                                           versions=10 hits=0 readme_version_lines=2
AP-03  md=36 bare_up=0                                                                                     md=36 bare_up=0
AP-04  skill_fm_same=17/17                                                                                 —
RE-02  rows=3/3 same=1 redefine=0                                                                          —
DG-02  files=36 files_up=0                                                                                 files=36 files_up=0
DG-04  /bin/sh rc=0 EVALS_PASS | bash rc=0 EVALS_PASS | zsh rc=0 EVALS_PASS ⏎ onboarding rc=0 EVALS_PASS ⏎ runner bash_n=0 shellcheck_rc=0 lines=0 | gate_py_compile=0 ⏎
       reflect lib_bash_n=0 lib_shellcheck_lines=0 test_shellcheck_lines=0 | design_gate_py_compile=0
DG-05  kits=13 kitfail=0 bad_v=0 ⏎ sync_rc=0 1 ⏎ evals_rc=0 Total: 115 passed, 0 failed ⏎                 kits=13 kitfail=0 bad_v=0 ⏎ sync_rc=0 1 ⏎ evals_rc=0 Total: 115 passed, 0 failed ⏎
       stale_old=15 files=41 hits_start=2 hits_end=2 files_up=0                                            stale_old=15 files=41 hits_start=2 hits_end=2 files_up=0
DG-06  scope-isolation: PASS ⏎ doc-contracts: PASS ⏎ doc_checked=2 doc_mine=0 ⏎ violators=0 mine=0
```

예행 변형 (그 변형이 겨냥한 조건만 쟀다):

```text
변형            바꾼 것                                                  값
unsigned-kit    서명 없는 커밋이 tone-kit/README.md 를 건드림            AR-01 첫째 1 (나머지 기대값 그대로)
unsigned-planningkit 서명 없는 커밋이 planning-kit/README.md 를 건드림  AR-01 첫째 1 (나머지 기대값 그대로) · ER-03 기대값 그대로 — 고치기 전 첫째 값은 0 이었다(검토 C1)
harness-other   서명 커밋이 .harness/sprint-amendments-kaizen-0924-p07-backend-kit.md 를 고침 (Final 몫)
                                                                          AR-01 둘째 1 41 (나머지 기대값 그대로) · ER-03 기대값 그대로 — 고치기 전 둘째 값은 0 41 이었다(검토 C2)
typo-shared     서명 줄을 Kaizen-Phase: kaizen-0924-f1-kit-followup 으로 잘못 적은 커밋이 docs/index.html 을 고침
                                                                          ER-03 not_other=1 (AR-01 은 기대값 그대로 — 서명이 달라 이 계약 커밋으로 안 보이고 첫째 값은 HTML 을 빼고 잰다) —
                                                                          고치기 전 not_other 는 0 이었다(검토 C3)
mixed           서명 커밋 하나가 tone · api 두 묶음                       AR-01 셋째 mixed=1 one_kit=11 · ER-03 commit_rows=11/13
cross-phase     서명 커밋이 harness/skills/sprint · tone-kit/skills 를 함께 AR-01 둘째 2 41 · 셋째 mixed=0 one_kit=14 · ER-03 not_other=1 · DG-06 scope-isolation: FAIL · violators=1 mine=1
seal-broken     서명 커밋이 봉인 뒤 SK-01 줄을 바꿈                        AR-01 넷째 1 · 다섯째 SEAL_BROKEN
wc-only         작업 폴더에서만 SK-01 줄을 바꾸고 커밋 안 함 (음성 대조)   AR-01 넷째 0 · 다섯째 SEAL_OK
no-notes        notes 를 안 올림                                           ER-03 notes_committed=0
bad-text        tone 파일에 「이 값에 대해 fit-pal 앱 0.4.0 … https://example.invalid/x (OpenAPI 3.1.1)」 와 언어 힌트 없는 펜스
                                                                           ER-01 new_urls=7 not_in_evidence=1 · ER-02 k02=1 names=1 · AP-01 hits=1 · AP-03 bare_up=1 ·
                                                                           DG-02 UP tone-kit/references/core-antipatterns.md MD034:0>1 MD040:0>1 · files_up=1 ·
                                                                           DG-05 kitfail=1 bad_v=1 · hits_end=3 files_up=1 · ER-02 added=178 (하한 조건이라 값은 판정에 안 쓴다)
```

문장 삭제 대조(`del.sh`, 예행 판을 푼 폴더에서 문장 하나가 든 줄만 지우고 같은 조건을 다시 잰다 — SK-02 ~ SK-08 · SK-09 · SK-10 · SK-11 · SK-12 · AR-02 의 토큰 44 개 — 검토 C5 의 「두 명령은 한 번의 셸 호출에서 잇는다」 와 2 회차 R1 의 「같은 호출 끝의 판정 줄로 가른다」 · 「다른 셸 호출에서 `kill $!` 를 쓰지 마라」 포함):
`del_cases=44 changed=44` — 지운 문장마다 값이 바뀌었다. 조건이 재는 파일에서만 지웠다. SK-03 (d) · SK-08 (d) · SK-12 (b) 처럼 코드 줄을 도는 측정은 문장 삭제 대신
시작 커밋 판 값(위 표 오른쪽)이 음성 대조다 — 고치기 전 코드로 같은 입력을 돌려 결함이 드러난다. SK-10 의 폴더 변수 막음은 앞 초안의 서버 명령
(`--directory "$D" &`)을 같은 `api_unset` 에 넣어 `unset_d served=200 guard_msg=0`(`.api/credentials.local.json` 이 열림)으로 대조했다.
SK-10 의 판정 줄은 2 회차 전 초안 명령(판정 줄 없이 `&` 로 끝남)을 같은 `api_serve` 에 넣어 `run rc=0 blocked=0 http=200 serving_line=0 left_after_kill=1 | busy not_serving_line=0 blocker_alive=1`
(내릴 번호가 없어 서버가 남고, 포트가 차 있어도 셸이 돌아온 때 판정 줄이 없다)로 대조했다.

준비 단계: 기준 검사를 시작 커밋 판에서 먼저 돌렸다 — 킷 열셋 `validate-plugin.py` 종료 코드 전부 0 · `sync-docs.py --check-only` 「모든 README가 동기화 상태입니다」 ·
`run-evals.py` `Total: 115 passed, 0 failed` · howto 러너 `EVALS total=33 pass=33 fail=0` · onboarding 러너 `EVALS declared=6 ran=6 fail=0` · reflect 시험 `결과: 10 경우 중 불일치 0`.
onboarding 검사 함수 `guide_gate` 를 시작 커밋 판 예제에 bash · zsh 로 돌린 다섯 줄이 예행 판과 같다(`G1_LEDGER PASS steps=8 ledger=8` … `GATE_PASS`). 예행 판에서 bambu 완료 검사의
온전한 목록 실행에 남는 `[미검증]` 한 줄은 픽스처에 `_wall_budget_short_share` 가 없어서다 — 편집 전과 같다(`full … unv=1`). 시작 커밋 판 reflect 시험 열 경우를 끝 판 라이브러리로 돌려도
`결과: 10 경우 중 불일치 0` 이다 — 새 경고는 기존 경우의 출력을 바꾸지 않는다(기록과 같은 초에 적힌 실패는 「뒤」 가 아니다).

## Skill

- [ ] SK-01: 연구 기록 새 편집기 경고가 없어진다 (교차 진단 DG-02 뜻 기준 FAIL 해소) — (a) 연구 기록 넷의 `## [2026-09-24]` 항목 안에서 옛 항목과 이름이 같던 소제목 여덟이 끝에 ` — 2026-09-24 사이클` 을 붙인 이름으로 각 1 줄 있다(backend 넷 · infra 둘 · rust 하나 · planning 하나 — `m.sh` `SK-01)` 갈래 글자 그대로) (b) 네 파일의 같은 제목 중복 경고(MD024) 수가 사이클 개시 커밋 `7689fde` 판과 같다 (c) 사이클 개시 판부터 `$END` 사이에 바뀐 킷 쪽 마크다운 전부(`.harness/` · `harness/` · `.claude/` · `docs/kaizen/` 밖, 예행 판 136 개)를 파일마다 규칙별로 사이클 개시 판과 비교해 는 규칙이 있는 파일이 0 이다. 양성 대조: 시작 커밋 판은 (a) 전부 0 · (b) `backend=13/17 infra=13/15 rust=8/9 planning=1/2` · (c) `files=132 files_up=4` (측정: `type m >/dev/null || exit 2;` 뒤 `m SK-01` 여섯 줄이 `1 1 1 1` · `1 1` · `1` · `1` · `backend=13/13 infra=13/13 rust=8/8 planning=1/1` · `files=<132 이상> files_up=0` — 예행 판 `files=136`) [exact, enumerated]
- [ ] SK-02: flutter-toolkit 네 자리가 스킬 동작과 맞는다 — (a) `project-detection.md` 에서 옛 `:59` 문장과 묶음 타겟 표 칸 둘(`` `$MAKE app-preflight` `` · `` `$MAKE app-build` ``)이 0 이고, 묶음 타겟을 codegen 줄 자리에 넣지 않는 이유 문장 1 · 「단계마다 위 행의 타겟 — codegen 은 flutter-run codegen 절 블록 안의 `$MAKE app-codegen`」 표 칸 2 가 있으며, flutter-build · flutter-preflight SKILL.md 에 `app-build` · `app-preflight` 가 0 줄이다 (b) `visual-evidence-protocol.md` 증거 블록에 `[미검증] 사유` 0 · `[미검증] — 네 칸은 아래 미검증 줄` 4 · 네 칸 미검증 줄 1 이고 머리 판이 `1.2.1` (c) 두 스킬 실패 틀에 `new_first=N new=N codegen_exit=N` 삭제 줄과 늘어난 삭제 목록 줄이 각 1 (d) `flutter-l10n` 에 `fvm dart run slang` 0 · Step 6 표를 가리키는 새 Gotcha 줄 1. 양성 대조: 시작 커밋 판 `1 1 1 0 0 0` · `4 0 1 0` · `0 0 0 0` · `1 0` (측정: `type m >/dev/null || exit 2;` 뒤 `m SK-02` 네 줄이 `0 0 0 1 2 0` · `0 4 1 1` · `1 1 1 1` · `0 1`) [exact, enumerated]
- [ ] SK-03: design-kit 규약 인용과 버전 줄 — (a) `design-component` SKILL.md 의 `# Gotchas` 절 안에 `visual-change-protocol.md` 가 1 줄 이상 (b) 규약 머리(`visual-change-protocol.md` 3 ~ 4 줄)가 적은 일곱 스킬 전부가 Gotcha 절 안에서 규약을 인용한다 (c) `design-kit/README.md` 에 `버전: \`` 로 시작하는 줄이 0 이고 「버전은 `.claude-plugin/plugin.json` 의 `version` 을 본다.」 가 1 (d) Given `$END` 판 `visual-change-protocol.md` 에서 docstring 으로 뽑은 결정 전파 게이트와 `dg_inputs` 의 `decisions.yaml` 다섯(i1 표면 없는 결정 · i2 `decision_id` 형식 틀림 · i3 규약 스키마 예와 같은 온전한 결정 · i4 제외 표면만 · i5 `reason` 없는 제외), When 차례로 돌리면, Then 종료 코드가 `harness/evals/gate-exit-codes.md` 네 값대로 1 · 2 · 0 · 3 · 1 이다 (Codex r2-2). 양성 대조: 시작 커밋 판 `0` · `6/7` · `1 0` · `gate i1=0 i2=0 i3=0 i4=0 i5=0` (다섯 다 통과) (측정: `type m >/dev/null || exit 2;` 뒤 `m SK-03` 네 줄이 `1` · `7/7` · `0 1` · `gate i1=1 i2=2 i3=0 i4=3 i5=1`) [exact, enumerated]
- [ ] SK-04: rust-kit 두 자리의 `[미검증]` 에 네 칸 · preflight fmt 규칙이 한 가지 — `rust-audit` Gotcha 16 줄과 `rust-model` 의 「라이브 DB 조회 불가 시 정적 대체 경로」 줄이 각각 `[미검증]` 과 「네 칸(막는 것 · 시도한 우회 · 통제 불가 사유 · 재검증 명령)」 을 함께 담고, 옛 문장 끝 「그 row 는 `[미검증]` 이다.」 · 「그건 `[미검증]` 이다.」 가 각 0 이다. 그리고 `rust-preflight` 에 옛 「실패 시 사용자에게 `cargo fmt` 실행을 안내하라.」 0 · 「확인이 실패했을 때만 Gotcha 2 · Step 1 대로 `cargo fmt --all` 을 적용하고 다시 검사한 뒤」 1 이며 같은 방향의 Gotcha 2 머리 줄 · Step 1 자동 적용 줄은 각 1 로 남는다 (Codex r2-6). 양성 대조: 시작 커밋 판 `0 0 | 1 1` · `1 0 1 1` (측정: `type m >/dev/null || exit 2;` 뒤 `m SK-04` 두 줄이 `1 1 | 0 0` · `0 1 1 1`) [exact, enumerated]
- [ ] SK-05: react-init 으로 만든 프로젝트에 포트 고정이 들어간다 — (a) `react-init` 의 `### 단계 2 ` 절 안에 `server: { port: 5173, strictPort: true },` 한 줄이 있고 그 두 값이 `templates/vite.config.template.ts` 의 `server` 블록 값과 같다 (b) 단계 10 주석의 옛 「템플릿이 strictPort: true 라」 0 · 「단계 2 에서 넣은 strictPort: true 라」 주석 1 (c) `react-run` 에 옛 「템플릿(`templates/vite.config.template.ts`)은 `strictPort: true` 라」 0 · 「react-init 으로 만든 프로젝트는 단계 2 에서 …」 1 · `pnpm vite dev --strictPort` 문장 1 이고 Gotcha 머리 글(`dev` 포트는 5173 에 묶여 있다)은 그대로 1 (d) `react-l10n` 의 지워진 키 수 명령(`git diff -U0 -- src/infrastructure/i18n/locales/ | ` 뒤 부분)을 뽑아 빈 입력에 돌리면 `0` · 종료 코드 0, `-msgid` 두 줄 · `+msgid` 한 줄 입력에 `2` (Codex r2-8). 양성 대조: 시작 커밋 판 `tpl=5173/true init=X/X same=0` · `1 0` · `1 0 0 1` · `l10n empty=0 rc=1 two=2` (0 건에 실패 종료 코드) (측정: `type m >/dev/null || exit 2;` 뒤 `m SK-05` 네 줄이 `tpl=5173/true init=5173/true same=1` · `0 1` · `0 1 1 1` · `l10n empty=0 rc=0 two=2`) [exact, enumerated]
- [ ] SK-06: reflect-kit 문서의 사유 태그 목록이 훅이 실제로 적는 태그를 다 담고, 수집 상태가 기간 도중 멈춤을 잡으며, 실행 줄이 요청한 기간을 쓴다 — (a) `$END` 판 `reflect-kit/hooks/*.sh` 의 문자열에서 뽑은 사유 태그 줄기(변수로 끝나는 `fail:` · `env-dedup:` 제외, 예행 판 14 개) 가운데 `SCHEMA.md` §3 목록에 없는 것과 `DESIGN.md` 에러 관측성 목록에 없는 것이 각 0 (b) `reflect-kit/README.md` 에 `버전: \`` 줄 0 · 「버전은 `.claude-plugin/plugin.json` 의 `version` 을 본다.」 1 (c) Given `$END` 판 `reflect-kit` 사본, When 킷 시험 `collect-status-test.sh` 를 돌리면, Then 종료 코드 0 · `결과: 11 경우 중 불일치 0` 이고 — 열한째 경우(`check` 이름 「도중 멈춤 — 마지막 기록 뒤 실패」)는 기록 하나(`D2`) 뒤에 Stop 실패 시도 하나(`D1`)만 있는 폴더에서 `⚠ 수집 멈춤 — 마지막 기록 뒤 Stop 실패 시도 1회` 를 기대한다 — When 같은 시험을 시작 커밋 판 `_lib-project-id.sh` 로 돌리면(`PROJECT_ID_LIB`), Then 종료 코드 1 · 불일치 1 · 그 불일치가 그 경우다(`불일치 도중 멈춤` 으로 시작하는 줄 1) (교차 진단 P12 결함 1 · Codex r3-1) (d) `reflect-digest` 에 고정 일수 실행 줄(`"${CLAUDE_PLUGIN_ROOT}" 7 `) 0 · `<일수>` 실행 줄 2, `reflect-kaizen` 에 `"${CLAUDE_PLUGIN_ROOT}" 30 ` 0 · `<일수>` 1, digest 의 경고 싣는 조건 두 자리에 「또는 마지막 기록 뒤 Stop 실패 시도가 1 이상일 때만 싣는다」 2 · Gotcha 13 에 새 경우 문장 1 (Codex r3-2). 알려진 답: 시작 커밋 판에서 빠진 태그를 손으로 세면 `vocab:raw_distinct/…` · `warn:lemma-map-unreadable` 둘(교차 진단 P12 결함 3) — 측정도 `schema_missing=2 design_missing=2` · README `1 0`. 양성 대조: 시작 커밋 판 (c) `test rc=0 결과: 10 경우 중 불일치 0` (그 경우가 없다) · (d) `2 0 1 0 0 0`. 음성 대조: 끝 판 시험에 시작 커밋 판 라이브러리 → `start_lib rc=1 … 불일치 1 1` (측정: `type m >/dev/null || exit 2;` 뒤 `m SK-06` 다섯 줄이 `code=14 schema_missing=0 design_missing=0` · `0 1` · `test rc=0 결과: 11 경우 중 불일치 0` · `start_lib rc=1 결과: 11 경우 중 불일치 1 1` · `0 2 0 1 2 1`) [exact, enumerated]
- [ ] SK-07: bambu 완료 검사와 음성 대조 블록이 빠진 목록 · 빠진 파일을 조용히 넘기지 않는다 — Given `$END` 판 SKILL.md 에서 음성 대조 블록과 같은 방식으로 뽑은 완료 검사(python)와 설치본 BambuStudio 판 옵션 목록, When (a) enum 줄만 뺀 목록으로 받지 않는 값 픽스처 `process-seam-slope-type-invalid.json` 을 돌리면, Then `[미검증]` 에 `enum 0 줄` 이 1 줄 나오고(받지 않는 값 FAIL 은 목록이 없어 0), 온전한 목록으로는 `받지 않는 값 seam_slope_type` FAIL 1 · 종료 코드 1 이다. When (b) 음성 대조 블록의 (1) 확인 부분(`# (1) 폴더의 시험 파일이` 줄부터 닫는 `fi` 까지)을 킷 사본에서 돌리면, Then 온전한 사본은 출력 0 줄 · 종료 코드 0, 시험 파일 `process-thin-baseline.json` 하나를 지운 사본은 `폴더에 없음 process-thin-baseline.json` 1 · `STOP` 1 · 종료 코드 1 이고 zsh 로 돌려도 같다. (c) 킷 블록에 더한 enum 없는 목록 변이 네 줄을 그대로 돌리면 `enum 0 줄` 알림 1 · `exit=0` 1. (d) 두 자기 검사 블록(`S="$SKILL_DIR/SKILL.md"` 줄이 든 블록 둘) 모두 바로 앞 줄이 `SKILL_DIR=<이 스킬의 기준 폴더>` 이고, 형상 측정 자기 검사를 기준 폴더로 채워 돌리면 `SELFTEST PASS` · `exit=0`, 두 블록을 빈 값으로 돌리면 둘 다 `STOP /SKILL.md 가 없다` 로 0 이 아닌 종료 코드다 (Codex r3-5) (e) Given 앞 실행의 댓글 페이지 `comments-100.json`(59 개)이 남은 출력 폴더와 주소별 JSON 을 내는 가짜 `curl`, When 댓글 받기 블록을 돌리면, Then `comments total 2 · 받은 hits 2 (페이지 1)` · `WARN` 0 · 옛 페이지 파일 0 이다 (Codex r3-4). 양성 대조: 시작 커밋 판은 (a) `noenum unv_enum=0 reject=0 RESULT: PASS rc=0` (enum 검사가 꺼진 채 통과) · (b) 지운 사본 `orphan=0 stop=0 rc=0` · (c) `lines=0` · (d) `selfblocks heads=0/2 filled_selftest_pass=0 empty_stop=0/2` (빈 측정 코드로 `IndexError`) · (e) `mw total=2 hits=61 pages=2 warn=1 stale_left=1` (측정: `type m >/dev/null || exit 2;` 뒤 `m SK-07` 일곱 줄이 `noenum unv_enum=1 reject=0 RESULT: PASS rc=0` · `full reject=1 unv=1 rc=1` · `intact lines=0 rc=0` · `deleted orphan=1 stop=1 rc=1 zsh_same=1` · `kit_noenum lines=4 unv_enum=1 1` · `selfblocks heads=2/2 filled_selftest_pass=1 empty_stop=2/2` · `mw total=2 hits=2 pages=1 warn=0 stale_left=0`) [exact, enumerated]
- [ ] SK-08: onboarding-kit 이 값 든 파일을 훑지 않게 하고 예제가 현행 요구와 세 칸 형식을 따른다 — (a) `setup-guide` Gotcha 8 의 `1. **패턴으로 탐색한다**` 줄에서 「실제 파일을 찾는다 (…)」 괄호 목록에 `.env*` · `.p8` 가 0 이고 「`.env*` · `**/*.p8` 은 Glob 으로 있는지만 본다」 가 1 (b) `evals.json` 이 JSON 으로 읽히고 `no-invented-paths` 사례의 평가 항목에 `.env.example` 기준 새 문장 1 · 옛 「실제 .env 에 없는」 문장 0 이며 `setup.env_contains` 는 남는다 (c) 예제 `docs/onboarding-kit/examples/fcm-ios-setup-guide.md` 에 `Xcode 16+` · `iOS 14+` · 특정 앱 이름(`fit-?pal` · `fit pal` 등, 대소문자 무시) · 시뮬레이터 수신 주장 넷(`시뮬레이터도 일부 지원` · `FCM 푸시도 일부 지원` · `시뮬레이터에서도 토큰은 받지만` · `iOS 16 이전 시뮬레이터는 APNs 불가`)이 줄 수 0, `Xcode 26.2+` 2, 막는 요구 표 머리 1, 표 세 행이 `format-checklist.md` 의 같은 세 행과 글자 그대로 같고(3/3), onboarding 검사 함수 `guide_gate <예제> flutter` 가 bash · zsh 에서 같은 다섯 줄 `GATE_PASS`(Step 8 · 출처 줄 8)다 (d) 같은 함수를 Step 1 에 출처 줄 둘 · Step 2 에 0 인 입력(전체 수는 2 = 2)에 돌리면 첫 줄이 `G1_LEDGER FAIL steps=2 ledger=2 misplaced=2` 이고 bash · zsh 가 같다 (Codex r3-3). 양성 대조: 시작 커밋 판 `grep_list_env=1 grep_list_p8=1 glob_only=0` · `new=0 old=1` · `x16=2 ios14=1 names=5 sim=3 x262=0 head=0 rows=0/3` · `misplaced G1_LEDGER PASS steps=2 ledger=2` (배치 오류를 통과) (측정: `type m >/dev/null || exit 2;` 뒤 `m SK-08` 다섯 줄이 `grep_list_env=0 grep_list_p8=0 glob_only=1` · `json=1 case=1 new=1 old=0 env_contains=1` · `x16=0 ios14=0 names=0 sim=0 x262=2 head=1 rows=3/3` · `G1_LEDGER PASS steps=8 ledger=8 G2_MARKER PASS bare=0 invalid=0 env=0 G3_STACKMIX PASS stack=flutter swift_fence=0 G4_DEPRECATION PASS unsourced_boxes=0 GATE_PASS rc=0 | zsh_same=1` · `misplaced G1_LEDGER FAIL steps=2 ledger=2 misplaced=2 | zsh_same=1`) [exact, enumerated]
- [ ] SK-09: tone-kit 요약표의 grep 칸이 붙여 넣으면 실제로 걸린다 — `core-antipatterns.md` `## 카테고리 요약표` 에서 grep 칸이 백틱 식인 행마다 그 식을 글자 그대로 `grep -cE` 로 시험 입력(`effectiveColor` · `// ---…` · `_buildHeader(` 세 줄)에 돌려 0 줄인 칸이 0 개이고, E 행 칸은 「아래 E 절의 grep 블록」 을 가리키며, E 절 코드 블록의 grep 명령은 같은 시험 입력에서 1 줄을 낸다. 양성 대조: 시작 커밋 판 `cells=3 dead=1 e_block=1 e_cell=0` (E 칸의 `\|` 때문에 0 줄) (측정: `type m >/dev/null || exit 2;` 뒤 `m SK-09` 가 `cells=2 dead=0 e_block=1 e_cell=1`) [exact]
- [ ] SK-10: api-kit 여는 방법이 셸을 묶지 않고 I-JSON 목록이 세 자리에서 같다 — (a) api-ui `1. **여는 방법**` 줄에 폴더 명령 `` `D=$(mktemp -d) && cp .api/ui.html "$D/"` `` 1 · 서버 명령 `` `python3 -m http.server 8765 --bind 127.0.0.1 --directory "${D:?폴더 변수가 비었다 — 두 명령을 한 셸에서 잇는다}" & sleep 1; kill -0 $! 2>/dev/null && echo "SERVING pid=$! dir=$D" || echo "NOT_SERVING 8765"` `` 1 · 옛 한 줄 명령 0 · `Address already in use` 1 · 「두 명령은 한 번의 셸 호출에서 잇는다」 1 · 「다른 셸 호출에서 `kill $!` 를 쓰지 마라」 1 · 옛 「(같은 셸이면 `kill $!`)」 0 이고, Given 그 두 명령을 뽑아 포트만 빈 번호로 바꾼 스크립트, When bash 로 돌리면, Then 스크립트가 4 초 안에 종료 코드 0 으로 돌아오고 그때까지의 출력에 `SERVING pid=` 줄이 1 이며, 띄운 서버가 `ui.html` 에 200 으로 답하고 그 줄의 번호로 `kill` 하면 그 포트의 서버가 0 이다. 같은 포트를 다른 서버가 먼저 쥐면 셸이 돌아온 때까지의 출력에 `NOT_SERVING` 줄이 1 이고 먼저 쥔 서버는 계속 답한다 (검토 2 회차 R1). Given 스크래치 폴더에 `.api/credentials.local.json` 을 둔 채 폴더 변수 없이(`env -u D`) 서버 명령만 돌리면(명령마다 새 셸이 뜨는 도구), Then 그 파일이 열리지 않고(`served=0`) 비었다는 알림이 1 줄이다 (검토 C5) (b) `api-verify` 의 「I-JSON 게이트 실패(」 로 시작하는 목록 줄에 `중복 키` · `NaN/Infinity` · `binary64` · `lone surrogate` · `` `-0` `` 가 각 1 (c) `snapshot-sealing-canonicalization.md` `## 수치 기준` 표에 `` | `-0` 허용 | `0` | `` 행 1 이고 그 절의 표가 끊기지 않고 한 덩어리다. 양성 대조: 시작 커밋 판 `0 0 1 0 0 0 0` · `run rc=142 blocked=1 http=200 serving_line=0 left_after_kill=1 | busy not_serving_line=0 blocker_alive=1` (알람이 끊을 때까지 묶이고 내릴 번호가 없다) · `unset_d served=0 guard_msg=0` · `1 0 0 1 1` · `0 1`, 앞 초안의 서버 명령(`--directory "$D" &`, 폴더 변수 막음 없음)은 `unset_d served=200 guard_msg=0` (`.api/` 가 열림), 2 회차 전 초안 명령(판정 줄 없음)은 `run rc=0 blocked=0 http=200 serving_line=0 left_after_kill=1 | busy not_serving_line=0 blocker_alive=1` (서버가 남고 충돌을 셸이 돌아온 때 못 가른다) (측정: `type m >/dev/null || exit 2;` 뒤 `m SK-10` 다섯 줄이 `1 1 0 1 1 1 0` · `run rc=0 blocked=0 http=200 serving_line=1 left_after_kill=0 | busy not_serving_line=1 blocker_alive=1` · `unset_d served=0 guard_msg=1` · `1 1 1 1 1` · `1 1`) [exact, enumerated]
- [ ] SK-11: howto 러너가 `sh` 펜스로 쓴 `howto_gate` 호출 블록도 센다 — (a) 러너에 `for c in data['cases']` 0 · `for entry in data['cases']:` 1 · 펜스 넷을 받는 줄 1, README 에 「게이트를 부르는 셸 블록(`bash` · `sh` · `shell` · `zsh` 펜스)도」 1 · 옛 「게이트를 부르는 `bash` 블록도」 0, `evals.json` 설명에 셸 블록 문장 1 (b) Given `$END` 판 `howto-kit` 사본, When 온전한 사본에서 러너를 bash · zsh 로 돌리면, Then 둘 다 종료 코드 0 · `EVALS total=33 pass=33 fail=0` 이고, When README 의 `howto_gate` 호출 블록을 `sh` 펜스로 `skills/howto/SKILL.md` 끝에 더한 사본(등록 안 된 블록)에서 돌리면, Then 둘 다 종료 코드 1 · FAIL 은 `blocks-declared` 하나 · `EVALS total=37 pass=36 fail=1` 이다. 음성 대조 겸 양성 대조: 시작 커밋 판 러너는 같은 `sh` 펜스 사본에서 `rc=0` · `total=33` (그 블록을 못 본다) (측정: `type m >/dev/null || exit 2;` 뒤 `m SK-11` 세 줄이 `0 1 1 1 0 1` · `intact rc=0 |  | EVALS total=33 pass=33 fail=0 | zsh rc=0 same_verdict=1` · `sh_block rc=1 | blocks-declared | EVALS total=37 pass=36 fail=1 | zsh rc=1 same_verdict=1`) [exact, enumerated]
- [ ] SK-12: backend · infra 감사 기준과 시험이 실제 규칙대로 가른다 — (a) backend 세 자리에서 다섯 필드 필수를 RFC 9457 요구로 적은 글(`audit-criteria.md` 「`title`/`status`/`detail`/`instance` 필수.」 · `api-design.md` 「`| RFC 9457 problem+json 필수 필드 |`」 · `system-principles.md` 「`type` URI 필드 필수」)이 각 0 이고, 다섯 필드는 이 킷 규칙이며 RFC 9457 은 `type` 이 없으면 `about:blank` 로 본다는 새 글이 각 1 이다. 근거 줄(`docs/api/contract/error-status-contracts.md` 「`type`이 없으면 `about:blank`로 간주되므로, 누락 자체를 계약 위반으로 잡지 않는다.」)은 끝 판에도 1 (Codex r2-1) (b) Given `$END` 판 `infra-test` 규칙 1 루프(`# 규칙 1: checkout 스텝 존재` 부터 닫는 `done` 까지)와 워크플로 셋(주석에만 `# - uses: actions/checkout@v4` · `- uses: actions/checkout@v4` 스텝 · 작은따옴표로 싼 SHA 고정 스텝), When 그 루프를 bash 로 돌리면, Then 차례로 `VIOLATION` · `PASS` · `PASS` 이고 `violation=1` 이다 (Codex r2-5). 양성 대조: 시작 커밋 판 `1 0 1 0 1 0` · `r1_lines=8 PASS PASS PASS violation=0` (주석 줄로 통과) (측정: `type m >/dev/null || exit 2;` 뒤 `m SK-12` 세 줄이 `0 1 0 1 0 1` · `basis=1` · `r1_lines=9 VIOLATION PASS PASS violation=1`) [exact, enumerated]

## Script

- [ ] SC-00: N/A (Script 카테고리는 `release.sh` 연동 · 버전 올림 · `marketplace.json` 갱신이다. 이 계약은 그 파일을 건드리지 않는다 — 버전 계획은 `kaizen-0924-final` 몫. 측정: `type m >/dev/null || exit 2;` 뒤 `m NA` 의 `SC-00=0`. 양성 대조: 예행 변형 `cross-phase` 는 버전 파일을 안 건드려 0 이다 — 이 값의 대조는 AR-01 둘째 값이 한다)

## Error

- [ ] ER-01: 마흔한 파일에 새로 생긴 외부 URL(파일마다 편집 전 판에 없던 URL — 고친 줄에 원래 있던 URL 은 빼고 다른 파일에서 옮겨 온 URL 은 넣는다, 셸이 여는 `127.0.0.1` · `localhost` 주소 제외, 예행 판 6 개)과 notes 의 URL 이 전부 시작 커밋 판 근거 파일 `.harness/.meta/evidence/phase*.md` 에 있다 — 근거 파일은 `.harness/` 안이라 끝 판에서 읽지 않는다. 양성 대조: 예행 변형 `bad-text`(근거 파일에 없는 URL 한 줄) → 첫 줄 `new_urls=7 not_in_evidence=1` (러닝북 — 근거 파일에 없는 URL 을 지어내지 마라) (측정: `type m >/dev/null || exit 2;` 뒤 `m ER-01` 두 줄이 `new_urls=<1 이상> not_in_evidence=0` · `notes_urls_not_in_evidence=0` — 예행 판 `new_urls=6`) [exact]
- [ ] ER-02: 마흔한 파일에 더한 줄에 번역투 6 종(`tone-kit/references/locale-korean.md` §2 치환표의 grep 열)과 특정 앱 이름 · 화면 도구 서버 이름(`fit-?pal` · `fit_pal` · `fit pal` · `flutter[-_]playwright` · `playwright-mcp` · `chrome-devtools-mcp`, 대소문자 무시)이 0 건이고, `gate-result-taxonomy.md` 의 옛 문장 「같은 원칙이 **규칙 소스**에도 적용된다」 가 0 이다. 양성 대조: 시작 커밋 판 `tax_old=1` · 예행 변형 `bad-text`(「이 값에 대해 fit-pal 앱」) → `k02=1 names=1` (측정: `type m >/dev/null || exit 2;` 뒤 `m ER-02` 가 `added=<1 이상> k02=0 names=0 tax_old=0` — 예행 판 `added=172`) [exact]
- [ ] ER-03: 이 계약이 고치지 않은 것과 다른 계약 몫을 명시적으로 넘기고 공유 파일을 건드리지 않는다 — `.harness/.meta/kaizen-0924/f1-kit-followups-notes.md` 가 `$END` 에 커밋돼 있고 (a) 절 머리 다섯(`## 커밋` · `## 다룬 항목` · `## 고치지 않은 항목과 이유` · `## Final 에 넘기는 것` · `## 다음 사이클 메모`)이 각 1 줄 이상 (b) `## 커밋` 표에 킷 묶음 열셋마다 `| <묶음 이름> |` 행이 있고 그 sha 가 시작 커밋 뒤 `$END` 조상이며 서명돼 있고 그 묶음 경로만 건드렸다 (c) `## Final 에 넘기는 것` 에 Phase 7 · 8 · 9 · 11 슬러그(`kaizen-0924-p07-backend-kit` · `kaizen-0924-p08-infra-kit` · `kaizen-0924-p09-rust-kit` · `kaizen-0924-p11-planning-kit`)가 각각 그 묶음 커밋 sha 와 한 줄에 있고, 버전 계획 킷 열둘(`backend-kit` 포함)과 다시 만들 페이지 아홉(`api-design.html` · `visual-change-protocol.html` · `bambu-print-profile.html` · `schema.html` 포함)이 있다 (d) `## 다음 사이클 메모` 에 토큰 열(`claude -p` · `판정 불가` · `adapter-dart-flutter.md` · `widget-inspector` · `fit-pal` · `2026-09-02-api-kit-design.md` · `flutter-preflight` · `G91` · `locale-korean.md` · `design-reviewer` · `planning-reviewer` · `2.7.0` · `RFC 7493` · `misplaced` · `harness-project.yaml.template` · `docs/infra/platform/cicd.md` · `build_runner-2.13.1`)이 각 1 줄 이상 (e) 시작 커밋부터 `$END` 사이에 공유 파일 · 다른 계약 경로(`.claude-plugin/marketplace.json` · `README.md` · `CLAUDE.md` · `.harness/.meta/orchestrator-audit-log.md` · `.harness/.meta/kaizen-failure-count.yaml` · `.claude/kaizen-input/insights-report.md` · `.github` · `.harness/stale-values.yaml` · `harness` · `scripts` · `.claude/skills` · `docs/index.html` · `docs/kaizen` · `docs/**/*.html` · `*/.claude-plugin/plugin.json`)를 건드린 커밋 가운데 `Kaizen-Phase: kaizen-0924-f1-harness-followups` 줄이 글자 그대로 있는 커밋을 뺀 수가 0 이다 — 서명을 잘못 적은 이 계약 커밋도 센다(이 구간에 함께 커밋하는 계약은 그 하나다). 양성 대조: 예행 변형 `no-notes` → `notes_committed=0` · `mixed`(tone · api 한 커밋) → `commit_rows=11/13` · `cross-phase`(서명 커밋이 `harness/skills/` 를 건드림) → 마지막 값 1 · `typo-shared`(서명 줄을 `…f1-kit-followup` 으로 잘못 적은 커밋이 `docs/index.html` 을 고침) → 마지막 값 1 (측정: `type m >/dev/null || exit 2;` 뒤 `m ER-03` 일곱 줄이 `notes_committed=1` · `1 1 1 1 1` · `commit_rows=13/13` · `final_dg02_rows=4/4` · `release_kits=12/12 pages=9/9` · `1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1` · `not_other=0`) [exact, enumerated]

## Architecture

- [ ] AR-01: 이 계약의 변경이 허용 경로 안에 머물고, 한 커밋에 킷 하나이며, 범위 선언 블록이 그 경로와 같고, 이 계약이 봉인돼 있다 [exact, enumerated]
  (측정: `type m >/dev/null || exit 2;` 뒤 `m AR-01` 여섯 줄이 `0` · `0 41` · `mixed=0 one_kit=<13 이상>` · `0` · `SEAL_OK` · `scope_same=1 harness_line=1` — 예행 판 `one_kit=13`.
  첫째 — 시작 커밋부터 `$END` 사이에 킷 폴더 전부(`*-kit/` · `flutter-toolkit/`, `harness/` 제외)와 `docs/` 원본(HTML · `docs/kaizen/` 제외)을 건드린 커밋 가운데 이 계약 서명 줄이 없는 커밋 수 0 (서명을 빠뜨린 커밋은 서명 줄 목록에 안 보이므로 경로로 직접 센다. 이 자리는 동시에 도는 harness 쪽 계약의 범위가 아니다).
  둘째 — 서명 커밋이 건드린 경로 가운데 `FILES` 마흔하나 밖이면서 이 계약 `.harness/` 허용 갈래(계약 · 개정 · QA 피드백 · `.harness/.meta/kaizen-0924/f1-kit-followups-*.md`) 밖인 경로 수 0 과, `FILES` 마흔하나 가운데 서명 커밋이 건드린 수 41.
  셋째 — 서명 커밋 가운데 킷 묶음 둘 이상을 건드렸거나 킷 묶음과 `.harness/` 를 함께 건드린 커밋 0 · 킷 묶음 하나만 건드린 커밋 13 이상(FIX 가 킷 커밋을 더할 수 있다. 묶음마다 커밋이 있는지는 ER-03 (b) 가 잰다).
  넷째 — 끝 판(`$END`)을 푼 폴더의 `.harness/` 에서, 슬러그를 열거하지 않고 봉인이 깨진 계약 가운데 이 계약 서명 커밋이 건드린 것의 수 0
  (`harness/references/contract-schema.md` §`.harness/` 범위 조건 권장 형태를 끝 판에 적용 — 작업 폴더에는 다른 세션의 미커밋 계약 변경이 있다).
  다섯째 — 끝 판 이 계약의 봉인이 `SEAL_OK`. 여섯째 — `## 범위 경계` 절 `# sprint-scope` 블록의 `.harness/` 밖 경로가 `FILES` 와 같고 `.harness/` 줄이 1.
  양성 대조: 예행 변형 `unsigned-kit` → 첫째 `1` · `unsigned-planningkit`(서명 없는 커밋이 `planning-kit/README.md` 를 고침) → 첫째 `1` · `cross-phase` → 둘째 `2 41` · `harness-other`(서명 커밋이 `.harness/sprint-amendments-kaizen-0924-p07-backend-kit.md` 를 고침 — Final 몫) → 둘째 `1 41` · `mixed` → 셋째 `mixed=1 one_kit=11` · `seal-broken`(서명 커밋이 봉인 뒤 조건 줄을 바꿈) → 넷째 `1` · 다섯째 `SEAL_BROKEN`.
  음성 대조: 예행 변형 `wc-only`(작업 폴더에서만 조건 줄을 바꾸고 커밋하지 않음) → 넷째 `0` · 다섯째 `SEAL_OK`)
- [ ] AR-02: 새 문장이 가리키는 자리가 실제로 있다 — (a) design-component 새 Gotcha 의 상대 경로 `../../references/visual-change-protocol.md` 가 그 스킬 폴더에서 열린다 (b) flutter-l10n 의 「Step 6 표」 가 가리키는 `### 6. Codegen 실행` 제목 1 (c) 예제가 가리키는 형식 문서에 「막는 요구는 세 칸으로 쓴다」 1 (d) 예제에 그 형식 문서 경로와 `§2` 를 적은 줄 1 (e) 형식 문서에 `### 2. ` 제목 1 (f) api-verify 목록 항목 집합이 api-probe `I-JSON 검문` 줄의 항목 집합과 같다. 양성 대조: 시작 커밋 판 `1 1 1 0 1 0` (측정: `type m >/dev/null || exit 2;` 뒤 `m AR-02` 가 `1 1 1 1 1 1`) [exact, enumerated]
- [ ] AR-03: 바꾸지 않을 곳이 그대로다 — (a) 연구 기록 넷은 날짜를 붙인 소제목 줄만 바뀌었다 — 파일마다 지운 줄 수 = 더한 줄 수 = 4 · 2 · 1 · 1 이고 더한 줄에서 ` — 2026-09-24 사이클` 을 떼면 지운 줄과 같다 (b) onboarding `evals.json` 은 평가 항목 한 줄을 빼면 시작 커밋 판과 같고, howto `evals.json` 은 `description` 을 빼면 같으며 `gate_blocks` 가 같다 (c) bambu 완료 검사 python 본문은 편집 전 판과 비교해 지운 줄 2 · 더한 줄 3 뿐이고(조건 줄 · 알림 줄 · 이유 주석), howto 러너는 지운 줄 3 · 더한 줄 4 뿐이며, onboarding `guide_gate` 함수는 G1 블록(`  # G1 출처 원장 완전성` 줄부터 `  # G2 미검증 마커` 줄 앞까지) 밖이 글자 그대로 같고, reflect `_lib-project-id.sh` 는 `collect_status()` 함수 밖이 글자 그대로 같다(`facets_unmatched` 등). 음성 대조: 시작 커밋 판에서 같은 측정은 (a) `0/0/1` 넷 · (c) `gate -0 +0 | runner -0 +0` (측정: `type m >/dev/null || exit 2;` 뒤 `m AR-03` 세 줄이 `4/4/1 2/2/1 1/1/1 1/1/1` · `onboarding_same_but_one=1 howto_same_but_desc=1 gate_blocks_same=1` · `gate -2 +3 | runner -3 +4 | guide_gate_outside_g1_same=1 lib_outside_collect_status_same=1`) [exact, enumerated]

## Anti-patterns

- [ ] AP-01: 버전을 하드코딩하지 않는다 — plugin.json에서 읽어야 한다. 이번 변경에 적용: 마흔한 파일에 더한 줄에 킷 열셋 `plugin.json` 의 `version` 값(`$END` 판에서 읽는다, 서로 다른 값 10 개)이 0 건이고, design-kit · reflect-kit README 에 `버전: \`` 줄이 0 이다 — 이 계약은 킷 버전을 적지 않고 `kaizen-0924-final` 이 버전 계획을 적는다. 양성 대조: 시작 커밋 판 `readme_version_lines=2` · 예행 변형 `bad-text`(design-kit 판 `0.4.0` 을 한 줄에) → `hits=1` (측정: `type m >/dev/null || exit 2;` 뒤 `m AP-01` 이 `versions=10 hits=0 readme_version_lines=0`) [exact]
- [ ] AP-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수 (```` ```text, ```bash, ```yaml ```` 등). 판정 권위는 validate-plugin V6 상태기계다 — 여는/닫는 fence 가 동형이라 줄 단위 정규식으로는 판정 불가. 이번 변경에 적용: V6 가 읽는 파일은 DG-05 의 V 줄이 보고, 마흔한 파일 가운데 마크다운 서른여섯 모두 같은 여닫기 방식으로 센 언어 힌트 없는 여는 펜스 수가 편집 전 판보다 늘지 않았다. 양성 대조: 예행 변형 `bad-text`(언어 힌트 없는 펜스) → `bare_up=1` (측정: `type m >/dev/null || exit 2;` 뒤 `m AP-03` 이 `md=36 bare_up=0`) [exact]
- [ ] AP-04: SKILL.md / agents/*.md frontmatter 에서 name 필드 누락 — validate-plugin V1 FAIL. 이번 변경에 적용: 마흔한 파일 가운데 SKILL.md 열일곱의 첫 frontmatter 블록이 편집 전과 글자 그대로 같고 `name:` 줄이 있다 — 그래서 킷 README AUTO 구간과 트리거 설명이 읽는 값도 바뀌지 않는다 (측정: `type m >/dev/null || exit 2;` 뒤 `m AP-04` 가 `skill_fm_same=17/17`) [exact]

## Reusability

- [ ] RE-01: N/A (재사용 단위 코드를 새로 만들지 않는다 — 새 파일 0 개, 바뀌는 것은 문서 문장 · 기존 블록 · 함수 몇 줄 · 러너 두 줄 · 킷 시험 한 경우다. 측정: `type m >/dev/null || exit 2;` 뒤 `m NA` 의 `RE-01=0` — 시작 커밋부터 `$END` 사이에 `.harness/` 밖에서 더한(`A`) 파일 수)
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다. 이번 변경에 적용: (a) 예제의 막는 요구 표 세 행은 새로 쓰지 않고 `format-checklist.md` §2 의 세 행을 글자 그대로 옮긴다(3/3) (b) react-init 의 `server` 값은 기존 템플릿 `server` 블록 값과 같다 (c) design-component 새 Gotcha 는 규약을 인용만 하고 숫자(「N 개」 · 「N 회」)를 다시 적지 않는다(0) (측정: `type m >/dev/null || exit 2;` 뒤 `m RE-02` 가 `rows=3/3 same=1 redefine=0`) [exact, enumerated]

## Diagnostics

- [ ] DG-01: N/A (`commands.analyze` 는 `bash -n scripts/release.sh` 라 `scripts/release.sh` 만 잰다 — 이번 변경 파일과 교집합 0 개. 측정: `type m >/dev/null || exit 2;` 뒤 `m NA` 의 `DG-01=0`. 새 셸 코드의 실제 검사는 DG-04)
- [ ] DG-02: IDE diagnostics 워닝/인포 0개 (`diagnostics.ide_exclude` 값 `[]`) — 이번 변경에 적용: 편집기 마크다운 확장과 같은 조건(markdownlint-cli2 0.23.2 · MD013 끔)으로 마흔한 파일 가운데 마크다운 서른여섯 **각각**에서 규칙별 경고 수를 시작 커밋 판과 비교해 는 규칙이 있는 파일이 0 이다. 더한 줄만 보지 않는다 — MD022 · MD032 · MD024 는 더한 줄 옆의 손대지 않은 줄에 붙는다(러닝북 측정 구멍 목록). 편집 전부터 있던 경고는 같은 수로 남아도 된다. 양성 대조: 예행 변형 `bad-text`(언어 힌트 없는 펜스) → `files_up=1` (측정: `type m >/dev/null || exit 2;` 뒤 `m DG-02` 가 `files=36 files_up=0`) [exact]
- [ ] DG-03: N/A (`commands.test` 는 `bash scripts/release.sh 2>&1 || true` 라 `scripts/release.sh` 만 잰다 — 교집합 0 개. 측정: DG-01 과 같은 `m NA` 의 `DG-01=0`. 실제 시험은 SK-07 · SK-11 · DG-04)
- [ ] DG-04: 실제 앱/서버 구동 시 에러 0개 — 이번 변경에 적용: 구동하는 것은 킷 시험 러너 둘 · bambu 완료 검사 · reflect 라이브러리와 그 시험 · design 결정 게이트다. `$END` 판에서 howto 러너를 `/bin/sh` · bash · zsh 로 돌리면 셋 다 종료 코드 0 · 끝 줄 `EVALS_PASS`, onboarding 게이트 러너가 종료 코드 0 · `EVALS_PASS`, howto 러너의 `bash -n` 종료 코드 0 · `shellcheck -s sh` 종료 코드 0 · 출력 0 줄, 뽑은 bambu 완료 검사의 `python3 -m py_compile` 종료 코드 0, `_lib-project-id.sh` 의 `bash -n` 종료 코드 0 · `shellcheck -s bash` 출력 0 줄 · `collect-status-test.sh` 의 `shellcheck` 출력 0 줄, 뽑은 design 결정 게이트의 `py_compile` 종료 코드 0 이다 (측정: `type m >/dev/null || exit 2;` 뒤 `m DG-04` 네 줄이 `/bin/sh rc=0 EVALS_PASS | bash rc=0 EVALS_PASS | zsh rc=0 EVALS_PASS` · `onboarding rc=0 EVALS_PASS` · `runner bash_n=0 shellcheck_rc=0 lines=0 | gate_py_compile=0` · `reflect lib_bash_n=0 lib_shellcheck_lines=0 test_shellcheck_lines=0 | design_gate_py_compile=0`) [exact]
- [ ] DG-05: 저장소 검사가 이 계약이 고친 킷을 문제로 가리키지 않는다 — `$END` 판을 푼 폴더에서 (a) `scripts/validate-plugin.py <킷>` 을 킷 열셋(`flutter-toolkit` · `design-kit` · `infra-kit` · `rust-kit` · `react-kit` · `reflect-kit` · `bambu-kit` · `onboarding-kit` · `tone-kit` · `api-kit` · `howto-kit` · `backend-kit` · `planning-kit`)에 돌려 종료 코드가 0 이 아닌 킷 0 · `— OK` · `— SKIP` 로 끝나지 않는 V 줄 0 (V 줄 글자만 세지 않는다 — 실패해도 V 줄에 FAIL 이 안 찍히는 검사가 있다) (b) `scripts/sync-docs.py --check-only` 종료 코드 0 · 「모든 README가 동기화 상태입니다」 1 (c) `scripts/run-evals.py` 종료 코드 0 · `0 failed` (d) `.harness/stale-values.yaml` 의 `old` 값 전부(15 개)를 마흔한 파일에서 직접 세어 시작 커밋 판보다 는 파일이 0 이다 — 등록부 `allow` 에 적힌 (값, 경로) 짝은 뺀다. 시작 커밋 판에도 있던 두 자리(backend 감사 기준 `:26` 의 `OpenAPI 3.1.1` 인용)는 그대로 세어져 `hits_start=2 hits_end=2` 다. `scripts/check-stale-values.py` 는 킷 폴더 대부분을 훑지 않아 쓰지 않는다. 양성 대조: 예행 변형 `bad-text`(tone-kit references 에 언어 힌트 없는 펜스 · 등록부 옛 값 `3.1.1` 한 줄) → `kitfail=1` · `hits_end=3 files_up=1` (측정: `type m >/dev/null || exit 2;` 뒤 `m DG-05` 네 줄이 `kits=13 kitfail=0 bad_v=0` · `sync_rc=0 1` · `evals_rc=0 Total: <1 이상> passed, 0 failed` · `stale_old=15 files=41 hits_start=2 hits_end=2 files_up=0` — 예행 판 `Total: 115 passed`) [exact, enumerated]
- [ ] DG-06: `python3 scripts/validate-post-kaizen.py --since 5b4fd72d5587c937c1875ddb62872f32ae087dcf` 출력의 `scope-isolation` · `doc-contracts` 줄이 `FAIL` · `ERROR` 가 아니다. `docs-site-regen` 은 `kaizen-0924-final` F2 몫이라 판정에서 뺀다. 다른 계약 커밋 때문에 `scope-isolation` 이 FAIL 이면 `--verbose` 위반 커밋 목록을 1 개 이상 읽었고 그 가운데 이 계약 서명 커밋이 0 개일 때, `doc-contracts` 가 FAIL · ERROR 이면 `validate-doc-contracts.py -v` 가 검사한 경로를 1 개 이상 읽었고 그 가운데 이 계약 서명 커밋이 건드린 경로가 0 개일 때 PASS 다 — 커밋 뒤에 잰다 (측정: `type m >/dev/null || exit 2;` 뒤 `m DG-06` 네 줄이 `scope-isolation: PASS` · `doc-contracts: PASS` · `doc_checked=<1 이상> doc_mine=0` · `violators=0 mine=0`, 또는 FAIL 이면 넷째 줄 `violators=<1 이상> mine=0`. 예행 판 `doc_checked=2`. 양성 대조: 예행 변형 `cross-phase`(서명 커밋 하나가 `harness/skills/` 와 `tone-kit/skills/` 를 함께 건드림) → `scope-isolation: FAIL` · `violators=1 mine=1`) [exact]
