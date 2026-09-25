# kaizen-0924-f2-review-fixes — notes

카이젠 2026-09-24 가지를 PR 로 올리기 직전 독립 검토 둘(Claude 검토 워크플로 · Codex 2 차 검토)이 짚은 것을 고친 계약의 기록이다.
계약 `.harness/sprint-contract-kaizen-0924-f2-review-fixes.md` (봉인 `c6850fe`, 조건 30) · 개정 `.harness/sprint-amendments-kaizen-0924-f2-review-fixes.md` ·
계약 초안 검토 `.harness/.meta/kaizen-0924/f2-review-fixes-review.md` (1 회차 CHANGES → 2 회차 APPROVE).
시작 HEAD `6a8be19` (main 합침 커밋).

## 커밋

묶음마다 한 커밋이다. 모든 커밋에 서명 줄 `Kaizen-Phase: kaizen-0924-f2-review-fixes` 가 있다.

| 묶음 | 커밋 | 고친 것 |
| --- | --- | --- |
| scripts | 72d6ddd | 옛 값 검사 backend-kit 제외 풀기 (A1) |
| claude | 5a5c420 | 카이젠 스킬 커밋 규칙 · I-02 목록 · 오케스트레이터 수와 표 · docs-site 표 · tone-kaizen 수 (A2 · B2 · B3 · B4 · B5 · B12 · B13 · Codex N2) |
| harness | 211d1d7 | 봉인 범위 블록이 봉인 함수 넷을 확인 · 문서 사이트 contract-schema 두 줄 (B1) |
| ci | b52f43c | validate 잡에 scenario-report 단위 시험 · 결정 전파 시험 (B6 · C L13) |
| react | 59f8ca4 | react-l10n 지워진 번역 줄도 0 건에 종료 코드 0 (A3) |
| design | 1113bdd | 결정 전파 검사 모양 오류 → 종료 코드 2 · 새 시험 · 쓰는 세 자리 · 문서 사이트 두 쪽 (A4 · A5) |
| flutter | 0dd1f66 | scenario-report 스킬 문서 · 기록 형식 문서의 도구 · 앱 이름(시험 예시 기록 `example/*/record.json` · `example/index.html` 의 도구 이름은 그대로 — 아래 교차 진단 뒤 기록) · 예시 보고서 다시 만듦 · preflight 실패 틀 (A6 · B8) |
| reflect | 8d5e2c1 | no issues 정상 종료 기록 · 그 뒤 실패만 수집 멈춤 · 시험 · 문서 · 문서 사이트 두 쪽 (A7) |
| api | 1396a11 | api-ui 서버 띄우기 세 줄 블록 · 문서 사이트 뷰어 쪽 (A8) |
| rust | 05e796d | rust-audit 가리키는 자리 · unwrap 세기 명령 (B7 · B9) |
| onboarding | 04e3591 | G1 misplaced 판정 시험 입력 (B10) |
| bambu | 5a4b31b | MakerWorld 받기 전 design.json · instances.json 지움 · 문서 사이트 쪽 (B11) |
| readme | d24d382 | 루트 README flutter-toolkit 20종 · scenario-report (B14 · Codex N3) |

그 밖의 이 계약 커밋: 봉인 `c6850fe` · 개정 파일 `end_sha` 기록 `c3911b7` · 이 notes 커밋과 그 뒤 `end_sha` 한 줄 더 커밋.

## 다룬 항목

- A 여덟 · B 열넷 전부를 조건으로 다뤘다(계약 입력 항목 처리표 1 ~ 22 행). Codex 2 차 새 발견 가운데 N1 · N3 은 A1 · B14 와 같은 자리, N2 는 오케스트레이터 `:25` 괄호가
  `.claude/skills/howto-research/SKILL.md` Step 1 표를 가리키게 고쳤다(SK-02 (f)). `phase-research-templates.md` 에 Phase 17 표를 더하는 일은 다음 사이클 Phase 17 그대로다(감사 기록 `F1H-76`)
- 감사 기록 `F1H-79`(`EXCLUDED_KITS` 해제가 남았다)는 `72d6ddd` 가 닫았다. `F1H-78` 가운데 tone-kaizen `:35` 쪽은 B4 로 닫았고, `:100` 「리서치 문서 8종」 은 셈 기준이 달라(글로브 전체 11 − overview · research-log · templates = 8) 그대로 둔다
- 구현이 개선안과 다른 곳 넷은 개정 파일에 적었다 — 가장 큰 것은 A7 에서 엔트리 0 경고도 같은 셈을 쓰게 한 것이다. 실패 뒤에 정상 종료가 있으면 엔트리 0 이어도 수집기는 돌고 있어,
  마지막 기록 뒤 갈래만 고치면 같은 오판이 엔트리 0 갈래에 남는다. 정상 종료 줄이 없으면 두 셈은 같아 기존 시험 값은 바뀌지 않았다
- 킷 판 단계: 이 계약이 바꾼 킷(harness · flutter-toolkit · design-kit · rust-kit · react-kit · reflect-kit · bambu-kit · onboarding-kit · api-kit)은 모두 고침만이라 patch 다.
  `.harness/.meta/kaizen-0924/release-plan.md` 의 단계(아홉 킷 모두 minor)가 더 크므로 그대로 쓴다. flutter-toolkit 은 main 이 v0.9.0 · v0.9.1 을 먼저 올렸다 — 합친 뒤 `release.sh` 가 그 킷 `plugin.json` 에서 판을 읽는다
- 검증(끝 판 `d24d382`, 계약 측정 글자 그대로): 조건 스물여덟이 기대값과 같다 — SK-01 ~ SK-08 · SC-00 · RE-01 · ER-01 ~ ER-07 · AR-02 · AP-01 · AP-03 · AP-04 · RE-02 · DG-02 · DG-04 · DG-05 · DG-06.
  ER-08 · AR-01 은 이 notes 커밋 뒤 상한으로 다시 잰다. `validate-post-kaizen.py --since 6a8be19` 는 13 PASS · 0 FAIL · 2 SKIP(판 번호 둘 — 이 계약이 올리지 않는다)
- 계약 피드백: `~/.harness/feedback/contract/1a3bcba6-2026-09-26T035651-de8c7935-6958.yaml` (`verify-feedback.sh` PASS)

## 고치지 않은 항목과 이유

계약 입력 항목 처리표 「고치지 않음」 행이다. 이유 전문은 그 표에 있다.

- C L2 `harness/scripts/commit-guard.sh:231` — `-i` 커밋의 작업 폴더 삭제가 staged 로 올라가 막힐 때 설명 줄이 빠졌다. 막는 동작은 맞고 안내 글만 빠진 낮음
- C L3 `scripts/detect-docs-drift.py:65` — howto 접두 매핑과 SKILL 폴더 이름 규칙이 겹쳐 초안 파일을 새 페이지 대상으로 낸다. F2 는 이번 사이클에 끝났다
- C L7 `scripts/sync-orchestrator.py:121` — 범위 줄 추론이 planning docs · 킷과 스킬 references 둘 다 가진 킷을 놓친다. 생성기를 고치면 AUTO 영역 전체가 다시 만들어진다
- B12 의 생성기 쪽 — 이번에는 AUTO 밖 한 줄(넘기는 범위 = AUTO 줄 + phase-dependencies 목록)로 막았다. 생성기 고치기는 C L7 과 같은 자리
- C L10 · Codex R2-5 `infra-kit/skills/infra-test/SKILL.md:256` — checkout 검사가 줄 글자로 판정한다(`run: |` 안 줄에 PASS · 흐름 표기 진짜 checkout 에 VIOLATION, 재현됨). 막으려면 YAML 을 구조로 읽어야 하는데 python3 없는 환경에서 규칙 1 이 빠진다 — 새 동작 설계
- C L14 `flutter-toolkit/skills/flutter-scenario-report/SKILL.md:44` — `VISUAL_CHANNEL` 우선순위 표에서 golden 프로젝트는 MCP 가 있어도 이 스킬 완료 기준을 못 채운다. project-detection Step 8 규칙을 바꾸는 일
- C L17 `bambu-kit/skills/bambu-print-profile/SKILL.md:1603` — enum 줄만 빠진 옵션 목록에서 `[미검증]` 문구가 「키 존재 · 종류 · enum 값 검사 미실행」 이라고 적는다(실제로는 키 · 종류 검사는 돈다). 출력 문구 낮음
- C L19 `tone-kit/references/adapter-dart-flutter.md:26` — 표 칸의 `\|` 정규식이 그대로 grep 에 넣으면 0 건이다. 어댑터 슬롯 값 형식을 정하는 일
- C L20 `api-kit/skills/api-verify/SKILL.md:117` — 목록에 noncharacter 가 없다. 낮음
- C R1 flutter-l10n slang 명령 경로 · C R2 project-detection Makefile 타겟마다 확인 — 반박 검토 셋 가운데 둘이 기각
- C R3 · Codex R2-3 · R2-4 design-reviewer · planning-reviewer 미검증 규칙 옛 사본 — 옮기면 여러 스킬 · evals 의 REJECT 문턱이 같이 바뀌는 판정 동작 변경이라 PR 직전 사실 오류 고치기를 넘는다
- Codex R3-6 api-kit `-0` 을 「I-JSON 게이트」 로 분류 — 레포 안에서는 어긋나지 않는다(킷의 검문 단계 이름). RFC 7493 이 `-0` 을 금지하지 않는다는 주장은 근거 파일 밖
- Codex R2-2 결정 전파 검사가 `status` 값 · `excluded_surfaces` 키 유무를 안 본다(재현됨) — §6 스키마가 `status` 값 목록도 빈 목록 규칙도 정하지 않았다. 규칙을 새로 정하는 일
- Codex R2-7 flutter-build `--delete-conflicting-outputs` — 받기는 하고 효과가 없는 호환 옵션. 동작 파손 증거 없음
- Codex R1-2 `silent-check` 실행기 없음 — 새 실행기는 Final 단계의 「새 기능을 추가하지 마라」 에 걸린다
- Codex N4 `docs/kaizen/changelog.md:110` 「133 → 389 파일」 — 재현 안 됨: 합치기 전 판은 389, 합친 판은 391. 그때 실측을 적은 기록이라 맞다
- 루트 `CLAUDE.md:294` 「`docs/tone/` 8종」 · `tone-research/SKILL.md:4` 「docs/tone/ 8종」 · `CLAUDE.md:284` 「`docs/api/` 12종」 — 「리서치 문서」 를 셀 때 overview · research-log · templates 를 넣는지 정한 곳이 없어 사실 오류로 확정 못 한다
- B14 의 「AUTO 마커 안으로 옮기기」 — sync-docs 에 새 마커 종류가 필요한 기능 추가
- 계약 초안 검토 5 번 `reflect-kit/README.md:84` 한 줄 설명에 `ok:no-issues` 가 없다 — 원래도 `vocab:` · `warn:` 줄을 적지 않는 뭉뚱그린 설명이라 사실 오류가 아니다

## 다음 사이클 메모

- Phase 4 (harness · scripts): `commit-guard.sh` `-i` 커밋 막힘 설명 줄 되살리기 · `detect-docs-drift.py` 매핑 밖 목록(howto 초안 파일) 정하기 — 다음 F2 전에 ·
  `sync-orchestrator.py` 범위 줄 추론을 `references/phase-dependencies.md` 와 맞추기(planning docs · 킷과 스킬 references 둘 다 · hooks/ · docs/ · agents/)
- Phase 8 (infra-kit): `infra-test` checkout 판정을 YAML 구조로 읽을지, python3 없는 환경의 규칙 1 을 어떻게 남길지
- Phase 5 (flutter-toolkit): scenario-report `VISUAL_CHANNEL` 이 golden 일 때 할 일 · flutter-l10n `slang` 명령 경로(`slang_build_runner` 유무 갈래) ·
  project-detection Makefile 타겟마다 확인(`app-preflight` 묶음 타겟만 있는 경우) · flutter-build `delete-conflicting-outputs` 를 명령에서 뺄지
- Phase 13 (bambu-kit): enum 줄만 빠진 옵션 목록의 `[미검증]` 문구 「enum 값 검사 미실행」 을 실제로 안 돈 검사만 적게
- Phase 15 (tone-kit): `adapter-dart-flutter.md` 표 칸 정규식 형식 · 「리서치 문서 N종」 셈 기준(루트 CLAUDE.md · `tone-research` 설명 줄)
- Phase 16 (api-kit): api-verify 목록의 `noncharacter` · `-0` 분류 이름을 가를지(`RFC 7493` 원문을 근거 파일에 넣은 뒤)
- Phase 6 (design-kit): 결정 전파 검사 스키마에 `status` 값 목록과 빈 `excluded_surfaces` 규칙을 정할지 — 정하면 검사 코드와 `decision-gate-test.sh` 입력 열을 같이 늘린다
- Phase 3 뒤 reviewer 넷 한 번에: `design-reviewer` · `planning-reviewer` · react · api reviewer 의 미검증 규칙을 정본 판으로 맞추기(REJECT 문턱 변경이 따라온다) · `silent-check` 픽스처 실행기
- Final: 루트 README 킷 절 스킬 수 · 목록을 `AUTO 마커` 안으로 옮겨 sync-docs 가 세게 하기
- Phase 12 (reflect-kit): `reflect-kit/README.md` 의 `.errors.log` 한 줄 설명에 정상 종료 줄(`ok:no-issues`)을 넣을지. 새 판 설치 뒤 설치본 Stop 훅이 `ok:no-issues` 줄을 실제로 남기는지 `.errors.log` 로 한 번 본다
- 측정 도구: 이 계약 DG-02 는 세션 스크래치의 markdownlint-cli2 에 기댄다 — 다음 계약은 판과 설치 명령을 준비 단계에 적거나 오래 남는 자리에 둔다

## 교차 진단 뒤 기록 (2026-09-26, 부모)

교차 진단은 판정을 뒤집을 근거가 없다고 했다(QA APPROVE 26/26 유지). 짚은 것 넷을 다음 사이클 메모로 넘긴다.

- SK-04 는 스킬 문서 둘만 잰다. `flutter-toolkit/evals/scenario-report/example/TC-001-*/record.json:85·89·93` · `TC-002-*/record.json:100·104` · `example/index.html:87` 에 `login_as` · `tap_native_point` · `tap_widget` · `find_widget` 이 남았다. 단위 시험이 커밋된 보고서와 바이트 단위로 비교하므로 예시를 다시 만들 때 함께 바꾼다. 이 표와 `docs/kaizen/flutter-changelog.md` 의 「뺐다」 문장은 이 사실에 맞게 정정했다
- `scripts/detect-docs-drift.py` 가 원본 다섯(`design-kit/references/visual-change-protocol.md` · `design-kit/skills/design-test/SKILL.md` · `reflect-kit/docs/` · `api-kit/skills/api-ui/SKILL.md`)과 그 페이지의 짝을 모른다. 오케스트레이터 F2 표 · docs-site Step 1 표에도 없고, 반대로 감지 도구의 `docs/flutter/` 는 두 표에 없다 — 세 곳을 한 표로 맞춘다
- 결정 전파 검사(`design-kit/references/visual-change-protocol.md`)가 폴더 경로 · UTF-8 이 아닌 파일을 받으면 오류 추적과 종료 코드 1(위반)로 끝난다(`IsADirectoryError` · `UnicodeDecodeError`). 입력 오류는 2 여야 한다
- 새 시험 둘은 이 맥(Python 3.14 · BSD 도구)에서만 돌았다 — PR 의 첫 CI(ubuntu · Python 3.12) 결과로 확인한다

