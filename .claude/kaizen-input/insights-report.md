---
source: claude-code-insights
generated: 2026-09-24
window: "2026-09-14 ~ 2026-09-23 (18 세션, 메시지 290)"
report_file: ~/.claude/usage-data/report-2026-09-24-095238.html
supersedes: 2026-08-13
facets: ~/.claude/usage-data/facets/
session_meta: ~/.claude/usage-data/session-meta/
---

# Claude Code Insights — 카이젠 입력 (§0)

관측 기간 2026-09-14 ~ 2026-09-23, 18 세션. 인사이트 리포트 항목 F01~F32 와 빈틈 대조 제안 64 건을
아래 처리 배정표에 한 줄씩 올렸다. 각 Phase 는 자기 배정 줄만 맡고, 아래 흡수 표에 있는 것은 새 규칙으로 또 넣지 않는다.

## 직전 사이클 흡수분 — 중복 금지

| 신호 | 이미 반영된 곳 | 반영 시점 |
| --- | --- | --- |
| 진단 전에 편집부터 시작 (wrong_approach) | Phase 1 강제 3등급(E1/E2/E3) + §3.7 Completion Evidence Gate | 2026-07-27 사이클 |
| 검증 없이 끝났다고 주장 | Phase 3 Evidence Validity Gate (있다 → 맞다), `[미검증]` 3 갈래 분류 | 2026-07-27 사이클 |
| 확정한 결정이 일부 자리에만 들어감 | Phase 1 §5.5 Counterpart Enumeration, Phase 7/11 `## Surfaces` 양쪽 열거 | 2026-07-27 사이클 |
| 서버만 바꾸고 앱 쪽을 빠뜨림 | Phase 2 양쪽 계약 + Phase 7/9 Counterpart 일반화 | 2026-07-27 사이클 |
| 화면 작업이 의도 밖 영역을 바꿈 | Phase 6 `visual-change-protocol.md` §2 (의도 밖 변화 = 실패), Phase 5 `visual-evidence-protocol.md` | 2026-07-27 사이클 |
| 낡은 핸드오프를 그대로 다시 씀 | Phase 4 `/sprint` 핸드오프를 git 기록으로 다시 확인 (E2) | 2026-07-27 사이클 |
| 빈 캡처로 정상이라고 주장 | Phase 3 「빈 캡처는 PASS 증거가 아니라 검증 실패 신호」 | 2026-07-27 사이클 |
| 대량 삭제·남의 커밋 되돌림·공용 목록이 옛 내용을 쥔 커밋 | `harness/scripts/commit-guard.sh` 커밋 전 차단(삭제 50 개 초과) + 커밋 직후 알림 | 이번 스프린트 |
| 편집한 .dart 파일만 포맷 | `flutter-toolkit/scripts/format-edited-dart.sh` 훅 + flutter-run·flutter-preflight 포맷 범위를 바뀐 파일로 좁힘 | 이번 스프린트 |
| 화면 규약이 완료 직전에만 불림 | `visual-evidence-protocol.md` 편집 전과 완료 직전 두 번 실행, 다섯 UI 스킬에 편집 전 호출, `flutter-ui-verify` 스킬 | 이번 스프린트 |
| 요청 되말하기·관례 표·반영 확인·캡처 점검 목록·도구 고장 전 확인 | `visual-evidence-protocol.md` Step 0·2·3·4 | 이번 스프린트 |
| 수집기가 옛 요약본을 집고 facets 를 안 읽음 | `scripts/collect-kaizen-data.py` report_file 기준 선택 + §0 안 `### 0-b` 세션별 분석, harness 카이젠 3 스킬이 데이터 풀 §0 을 거쳐 읽음 | 이번 스프린트 |

**이번 사이클의 유효 신호는 위 표에 없는 것이다.** 2026-08-13 요약본의 신규 델타 D1~D5 는 그 사이클의 입력이었으므로 여기 다시 올리지 않는다.

## 이번 델타 요약 (2026-09-14 ~ 2026-09-23)

18 세션, 메시지 290. 프로젝트 묶음은 플러터 앱 프로젝트 10 · claude-plugins 6 · 임시 폴더 2 이다.
마찰 상위 셋은 buggy_code 28 · wrong_approach 20 · misunderstood_request 14 이다.

1. **커밋 사고 세 가지** (F06 F07 F08) — 파일 3217 개를 삭제로 기록한 커밋, 남의 커밋 두 개를 되돌린 커밋, 코드 생성 한 번이 생성물 267 개를 지운 일. 킷에도 사용자 설정에도 막는 장치가 없었다. 커밋 단계는 이번 스프린트가 막았고, 코드 생성 단계는 Phase 5 에 남는다.
2. **화면 작업에서 의도가 샘** (F01~F05, F22, F23, F25, F26) — 되말하기 없이 착수, 기존 관례 무시, 재시작이 조용히 실패했는데 갱신됐다고 보고, 넘침·깨진 글리프를 사용자가 잡음, 화면 조종 도구를 고장으로 오진. 플러터 규약은 이번 스프린트가 고쳤다. design-kit·react-kit 규약과 widget-inspector 는 남는다.
3. **새 검사가 조용히 실패** (F16 F17 F18) — 첫 칸만 읽기, 표에만 있고 안 돌아가는 시험 파일, 한 칸을 못 읽으면 검사 전체가 꺼짐, zsh 배열 첨자. 평가자 확인 목록은 Phase 3, 킷별 실제 결함은 각 Phase 에 있다.
4. **계약 절차 마찰** (F11~F14, F21, F27) — 돌려보지 않은 명령, 손으로 짐작한 시각, 검사기가 거부한 필드, 한 줄 수정에 무거운 절차, 도구 없는 세션에서 0 단계 멈춤. Phase 2·4 몫이다.
5. **폐기한 결정을 되살림** (F20) — 이미 버린 시간대·국가 항목을 되살리고 한 나라 우선으로 판단했다. 기록 자리가 네 곳으로 갈려 있어 하나로 정하는 것이 먼저다.
6. **카이젠 수집기 결함** (F32) — 이번 스프린트가 고쳤다. 이 파일도 그래서 새로 썼다.

제안에 적힌 줄 번호는 대부분 c0e12a8 기준이고 사용자 설정 묶음만 390dea8 기준이다. 이번 스프린트 뒤에는 어긋나므로 파일을 다시 열어 찾는다.
V10 표 검사 가지는 이미 origin/main 에 합쳐졌다(검토자 확인). 「합쳐진 뒤 작업」 조건은 풀렸다.

## 처리 배정표

배정 칸 값은 `이번 스프린트` · `Phase N` · `기각` · `해당 없음` 넷 중 하나다.
Phase 가 끝나면 그 Phase 행의 대상 계약 칸에 계약 슬러그를, QA 칸에 `APPROVE` 또는 `REJECT` 를 적는다.
카이젠 Final 은 `python3 scripts/check-insights-tracking.py --final .claude/kaizen-input/insights-report.md` 로 빈칸을 잡는다.

| 항목 | 내용 요약 | 배정 | 대상 계약 | QA | 비고 |
| --- | --- | --- | --- | --- | --- |
| F01 | UI 의도가 샘 — 평평한 줄 대신 카드, 화면 대신 그리로 가는 칩, 고정 범위를 뒤집음 | Phase 6 | | | 플러터 규약의 되말하기·화면 자체 대상은 이번 스프린트(flutter:P-VEP-intent-convention). 남은 것 design:P3. 리액트 규약에도 되말하기가 없다(검토자 지적) — Phase 10 에서 other-kits:P1 과 함께 본다 |
| F02 | 기존 관례 무시, 없는 위젯 지어냄, 승인된 페이지 누락, 아이콘 뜻 오용 | Phase 5 | | | 관례 표는 이번 스프린트 규약 Step 0 에 들어갔다. 남은 것 flutter:P-INSPECTOR-convention, design-kit 쪽 design:P1·design:P7(Phase 6). 대조할 기존 화면 수가 2 개(이번 규약·design:P7) 대 3 개(design:P1·인사이트 원문)로 갈린다 — 카이젠에서 하나로 정한다 |
| F03 | 핫 리스타트가 조용히 실패했는데 갱신됐다고 보고, 앱이 옛 데이터를 들고 있음 | Phase 10 | | | 플러터 규약 Step 2 반영 확인은 이번 스프린트(flutter:P-VEP-restart-marker). 남은 것 other-kits:P1(리액트), design:P6(Phase 6). 사용자 규칙 쪽은 user-setup:P8 |
| F04 | 글자 넘침·깨진 글리프를 사용자가 잡음, 넘침 재현을 데이터 수정으로 시도 | Phase 6 | | | 플러터 규약 Step 3 점검 목록은 이번 스프린트(flutter:P-VEP-shot-checklist). 남은 것 design:P4 |
| F05 | 화면 조종 도구를 세 번 고장이라 오진 — 인자 이름 틀림, 따로 뜨는 층, 남의 시뮬레이터 | Phase 10 | | | 플러터 규약 Step 4 확인 순서는 이번 스프린트(flutter:P-VEP-tool-diagnosis). 남은 것 other-kits:P1 의 리액트 쪽 확인 |
| F06 | 코드 생성 build-filter 한 번이 생성물 267 개를 지움 | Phase 5 | | | 커밋 단계 대량 삭제는 이번 스프린트 커밋 안전 훅이 막는다. 남은 것 flutter:P-F06-codegen-delete-count 와 user-setup:P1 — build-filter 를 조건부로 남길지 전부 없앨지 두 갈래다 — 카이젠에서 하나로 정한다 |
| F07 | 잘못된 커밋이 파일 3217 개를 삭제로 기록 | 이번 스프린트 | insights-0924-hooks-skill-collector | | harness:P01 커밋 안전 훅 (커밋 전 50 개 넘는 삭제 차단, 커밋 직후 알림) |
| F08 | 커밋 하나가 다른 세션의 커밋 두 개를 되돌림 | Phase 4 | | | 공용 목록이 옛 내용을 쥔 커밋은 이번 스프린트 훅이 막는다(SC-01 ③). 남은 것 harness:P07 의 내 경로만 커밋 권고 |
| F09 | 공용 개발 가지가 남의 변경으로 몇 시간 빨간 채, 워크트리는 사용자가 먼저 제안 | Phase 4 | | | 기준 커밋 가르기 규칙이 harness:P07 · backend-family:P3(Phase 8) · backend-family:P4(Phase 9) 세 곳이다 — 카이젠에서 하나로 정한다. flutter-preflight·react-preflight 에는 기준 커밋 비교가 없다(검토자 지적) |
| F10 | 앱이 안 올라갔다·실기기가 없다로 불가능 선언, 서버 목록 상한을 막힘으로 과대 해석 | Phase 1 | | | harness:P09. 셋업 가이드 쪽은 other-kits:P9(Phase 14) |
| F11 | 한 줄 훅 수정이 무거운 계약·QA 절차에 묻힘 | Phase 2 | | | harness:P06 (크기에 맞춘 조건 수, 끝에 사용자가 할 일 한 줄) |
| F12 | 돌려보지 않은 검증 명령을 계약에 적어 QA REJECT | Phase 2 | | | harness:P03 |
| F13 | 짐작한 시각 때문에 QA REJECT | Phase 2 | | | harness:P08. 사용자 설정 묶음은 처리됐다고 봤지만 틀은 여전히 손으로 채운다 — 처리 안 됨으로 본다(검토자 지적) |
| F14 | 계약·피드백 파일이 검사기에 여러 번 거부됨 | Phase 4 | | | harness:P02. 사용자 lint-contract-oracle.sh 쪽은 킷 밖 |
| F15 | 평가자가 교차 진단을 흉내만 냄 | 해당 없음 | | | harness 0.11 에서 이미 고쳤다 — 검토자가 원문과 대조해 확인 |
| F16 | 새 검사가 조용히 실패 — 첫 칸만 읽기, 안 돌아가는 시험 파일, 한 칸 못 읽으면 전체 꺼짐 | Phase 3 | | | harness:P04. 같은 확인이 user-setup:P4 에도 있다 — 한쪽만 남긴다. 킷별 실제 결함은 bambu:P2~P4 · other-kits:P2 · other-kits:P3 · other-kits:P5 행 |
| F17 | 측정 스크립트 자체 버그 — 호 길이 누락, zsh 배열 첨자, 따옴표 없는 변수 | Phase 2 | | | harness:P05 (알려진 답 대조). zsh 배열 줄은 user-setup:P5 와 같은 줄이라 하나만 넣는다. 뱀부 쪽은 bambu:P5 · bambu:P6 |
| F18 | YAML 블록 깨짐, 절을 끼워 넣다 마크다운 표가 갈라짐 | Phase 4 | | | other-kits:P10 (V10 검사 범위 넓히기). YAML 깨짐은 맡은 제안이 없다(검토자 지적) — Phase 4 에서 검사를 더할지 정한다 |
| F19 | 사용자가 모르는 한국어 말을 지어냄 | Phase 15 | | | reflect-collector:P6 (K-11). 사용자 설정 쪽 장치는 사고 뒤에 생겨 효과가 확인되지 않았다(검토자 지적) |
| F20 | 이미 폐기한 시간대·국가 항목을 되살림, 한 나라 우선으로 거듭 판단 | Phase 11 | | | backend-family:P1. 폐기 결정 기록 자리가 design:P5 · backend-family:P1 · user-setup:P2 · user-setup:P6 네 곳이다 — 카이젠에서 하나로 정한다. 시간대를 설정값으로 다루는 것은 backend-family:P2(Phase 7) |
| F21 | 필요한 도구가 없는 세션에서 계약 스킬이 0 단계에서 멈춤 | Phase 2 | | | 맡은 제안이 0 개다(검토자 지적). sprint-contract 0 단계에 「도구가 없으면 첫 줄에 알리고 멈춘다」 한 줄을 넣을지 본다 |
| F22 | 파일 이름 변경과 겹친 ProviderScope 가 카탈로그를 깨 스크롤이 멈춘 듯 보임 | Phase 5 | | | flutter:P-CATALOG-tile-height. 이름 변경 뒤 재시작 실패는 이번 스프린트 규약 Step 2 가 맡는다 |
| F23 | 디버그 겹침을 칩 렌더링 결함으로 오진 | 이번 스프린트 | insights-0924-hooks-skill-collector | | flutter:P-VEP-shot-checklist 의 디버그 겹침 줄. 남은 제안 없음 |
| F24 | 기본 로캘·빌드 중 provider 수정 때문에 시험 실패 | Phase 5 | | | flutter:P-TEST-locale-buildmod |
| F25 | 그룹 설정 시안 21 종 | Phase 5 | | | 사고는 flutter-widget 에서 났는데 그 자리를 고치는 제안이 없다(검토자 지적). design-kit 쪽은 design:P2(Phase 6). 한 프로젝트 기억(「여러 개 다 만들어 나란히」)과 방향이 반대라 사용자 확인이 필요하다 |
| F26 | 스크린샷을 합의 조건으로 — 기준 화면, 변경, 재촬영, 비교, 스스로 고치기, 전·후 보고 | 이번 스프린트 | insights-0924-hooks-skill-collector | | flutter-ui-verify 스킬과 규약 두 번 실행. design-kit 쪽 비교 반복은 design:P6(Phase 6) |
| F27 | 스스로 검증하는 계약 — 조건마다 명령·출력·종료 코드, 계약 검사기, 크기 검사 | Phase 2 | | | harness:P02 · harness:P03 · harness:P06 |
| F28 | 워크트리 준비 스크립트, 워크트리 상태 스크립트, 커밋 전 검사 | Phase 4 | | | 50 개 넘는 삭제는 이번 스프린트 훅. 범위 밖 파일 차단은 insights:scope-commit-block. 시뮬레이터·데이터베이스 나누기와 워크트리 상태 스크립트는 맡은 제안이 없다(검토자 지적) |
| F29 | Edit·Write 뒤 편집한 파일만 dart format | 이번 스프린트 | insights-0924-hooks-skill-collector | | flutter:P-FORMAT-changed-files 와 format-edited-dart.sh 훅. 사용자 block-dirwide-autofixer.sh 가 fvm 붙은 형태를 놓치는 것은 킷 밖 |
| F30 | MakerWorld 를 헤드리스 브라우저로 긁다 막힘 | Phase 13 | | | bambu:P1 |
| F31 | 측정 스크립트·UI 변경마다 독립 검토 에이전트 | Phase 3 | | | 계약 지정 배정. harness:P04 와 함께 본다. 관례 대조는 flutter:P-INSPECTOR-convention(Phase 5) |
| F32 | 카이젠 수집기가 8 월 요약본을 집고 facets 를 안 읽음 | 이번 스프린트 | insights-0924-hooks-skill-collector | | reflect-collector:P1 · reflect-collector:P2, harness 카이젠 3 스킬의 §0 경유, 이 파일 교체 |
| design:P1 | 시안·컴포넌트 전에 재사용 부품 목록과 구조 관례 목록을 기존 화면 근거로 남김 | Phase 6 | | | 기존 화면 3 개(이 제안) 대 2 개(design:P7·플러터 규약) — 카이젠에서 하나로 정한다 |
| design:P2 | 시안 개수 규칙을 파일마다 맞춤 (미지정 3 · 지정 N · 승인 시 최대 5) | Phase 6 | | | 한 프로젝트 기억과 방향이 반대라 사용자 확인 필요 |
| design:P3 | design-mockup Step 1 에 대상 화면 경로와 한 문장 되말하기, 요소 하나 지목 요청까지 §2 를 넓힘 | Phase 6 | | | |
| design:P4 | 렌더 산출물 캡처 점검 목록 4 줄과 가장 큰 글자 크기로 한 번 더 찍기 | Phase 6 | | | 같은 점검 항목이 규약·audit-criteria·design-reviewer 세 자리에 있다 |
| design:P5 | 승인 기록에 확정 구성과 폐기 항목 칸 | Phase 6 | | | 폐기 결정 기록 자리가 design:P5 · backend-family:P1 · user-setup:P2 · user-setup:P6 네 곳 — 카이젠에서 하나로 정한다 |
| design:P6 | 비교 반복 순서와 새로 그려졌는지 확인, 스스로 고치기 최대 5 회 | Phase 6 | | | 되풀이 상한이 플러터 규약 3 회 대 이 제안 5 회 — 카이젠에서 하나로 정한다 |
| design:P7 | 감사 기준에 기존 화면 관례 일치 행 | Phase 6 | | | 기존 화면 2 개(이 제안) 대 3 개(design:P1) — 카이젠에서 하나로 정한다 |
| bambu:P1 | MakerWorld 읽는 순서를 JSON 주소 먼저로 다시 적음 | Phase 13 | | | |
| bambu:P2 | G-code 설정 대조와 3mf 값 박기를 칸마다 읽음 | Phase 13 | | | |
| bambu:P3 | 폴더에만 있는 시험 파일 8 개를 표와 실행 줄에 넣음 | Phase 13 | | | |
| bambu:P4 | 빈 목록이 검사를 조용히 끄는 두 자리를 막음 | Phase 13 | | | |
| bambu:P5 | G-code 길이 재기 블록 (호 이동 포함) | Phase 13 | | | |
| bambu:P6 | 형상 측정 블록에 정답 아는 입력 한 벌 | Phase 13 | | | |
| flutter:P-F06-codegen-delete-count | 코드 생성 전후 삭제 수 비교, build-filter 기본 사용 중지 | Phase 5 | | | user-setup:P1 과 방향이 두 갈래(조건부 유지 대 전부 제거) — 카이젠에서 하나로 정한다. 대상 목록도 서로 하나씩 빠졌다(flutter-l10n · project-detection.md) |
| flutter:P-VEP-two-phase | 규약을 편집 전과 완료 직전 두 번 부르고 다섯 UI 스킬에 편집 전 호출 | 이번 스프린트 | insights-0924-hooks-skill-collector | | SK-03(a) · SK-04 |
| flutter:P-VEP-restart-marker | 재캡처 전 반영 확인 — 바뀌어야 할 표식으로 판정, 안 되면 앱을 다시 띄움 | 이번 스프린트 | insights-0924-hooks-skill-collector | | SK-03(c) |
| flutter:P-VEP-shot-checklist | 캡처 점검 목록 — 넘침·글리프·칩·뱃지·카드와 평평한 줄·디버그 겹침 | 이번 스프린트 | insights-0924-hooks-skill-collector | | SK-03(d) |
| flutter:P-VEP-intent-convention | Step 0 에 요청 되말하기·화면 자체 대상·관례 표 | 이번 스프린트 | insights-0924-hooks-skill-collector | | SK-03(b) |
| flutter:P-VEP-tool-diagnosis | 도구가 고장이라 말하기 전 확인 순서 | 이번 스프린트 | insights-0924-hooks-skill-collector | | SK-03(e) |
| flutter:P-INSPECTOR-convention | widget-inspector 에 관례 대조 감지 기준 | Phase 5 | | | |
| flutter:P-TEST-locale-buildmod | flutter-test 에 기본 로캘·빌드 중 provider 수정 함정 | Phase 5 | | | |
| flutter:P-CATALOG-tile-height | 카탈로그 타일 높이를 내용보다 낮게 고정하는 함정 | Phase 5 | | | |
| flutter:P-FORMAT-changed-files | 포맷 범위를 이번에 바뀐 .dart 파일로 좁힘 | 이번 스프린트 | insights-0924-hooks-skill-collector | | AR-05. 제안은 훅을 빼자고 했지만 이번 스프린트는 편집 파일 포맷 훅(F29)도 함께 넣었다 |
| flutter:P-EVAL-ui-loop | flutter-widget 평가 사례 — 되말하기·관례 표·기준 캡처·반영 확인·점검 목록 | 이번 스프린트 | insights-0924-hooks-skill-collector | | SK-06 |
| harness:P01 | 커밋 안전 훅 — 커밋 전 대량 삭제 차단, 커밋 직후 알림 | 이번 스프린트 | insights-0924-hooks-skill-collector | | SC-01~SC-03 · ER-01 · ER-02 |
| harness:P02 | save-feedback.sh 첫 검사에서 project_hash·project_name 을 필수에서 뺌 | Phase 4 | | | sprint-contract 9 단계 문구는 Phase 2 와 맞춘다. reflect-collector:P5 가 같은 파일의 프로젝트 이름 계산을 바꾸므로 함께 시험한다 |
| harness:P03 | 면제는 값에만 — 재는 명령의 준비 단계는 봉인 전에 돌려 봄 | Phase 2 | | | |
| harness:P04 | qa-evaluator 규칙 10 아래, 산출물이 검사일 때 평가자가 직접 돌려 볼 다섯 가지 | Phase 3 | | | 계약 지정 배정. user-setup:P4 와 앞 세 가지가 같다 — 한쪽만 남긴다 |
| harness:P05 | 알려진 답 대조 소절, zsh 배열은 1 부터 센다 | Phase 2 | | | skill-design-guide §3.7 부분은 Phase 1 과 맞춘다. zsh 배열 줄은 user-setup:P5 와 같다 |
| harness:P06 | 조건 수를 작업 크기에 맞추고 끝에 사용자가 할 일 한 줄 | Phase 2 | | | |
| harness:P07 | /sprint 에 내 경로만 커밋, 워크트리 권고, 기준 커밋 비교 | Phase 4 | | | 기준 커밋 가르기 규칙이 harness:P07 · backend-family:P3 · backend-family:P4 세 곳 — 카이젠에서 하나로 정한다. user-setup:P2 와 겹친다 |
| harness:P08 | 계약 created·평가 Evaluated 시각을 date 출력으로 채움 | Phase 2 | | | qa-evaluator 쪽 Evaluated 는 Phase 3 과 맞춘다 |
| harness:P09 | 검증 불가 문장을 「막는 것 · 시도한 우회 · 다시 돌릴 명령」으로 | Phase 1 | | | sprint/SKILL.md 3 단계 부분은 Phase 4 와 맞춘다 |
| backend-family:P1 | plan-prd 에 폐기 결정 Non-goals 세 칸 (무엇 · 왜 · 남은 흔적) | Phase 11 | | | 폐기 결정 기록 자리 네 곳 — 카이젠에서 하나로 정한다 |
| backend-family:P2 | 시각 종류(한 순간 대 벽시계)를 가르고 나라·시간대는 설정값으로 | Phase 7 | | | rust-model 부분은 Phase 9 와 맞춘다 |
| backend-family:P3 | infra-guide — 자동 검사가 빨갛다고 내 변경 탓으로 단정하지 않기 | Phase 8 | | | 기준 커밋 가르기 규칙 세 곳 — 카이젠에서 하나로 정한다 |
| backend-family:P4 | rust-preflight 실패를 내 변경 · 남의 미커밋 · 기준 커밋에서 이미 실패로 가름 | Phase 9 | | | 기준 커밋 가르기 규칙 세 곳 — 카이젠에서 하나로 정한다 |
| reflect-collector:P1 | 수집기가 요약본을 「어느 보고서를 요약했나」(report_file)로 고름 | 이번 스프린트 | insights-0924-hooks-skill-collector | | SC-05 · SC-06 |
| reflect-collector:P2 | facets·session-meta 를 §0 안 0-b 절로 싣고 --usage-data 옵션을 둠 | 이번 스프린트 | insights-0924-hooks-skill-collector | | SC-07 · SC-08 · ER-03 |
| reflect-collector:P3 | reflect-kit Stop 훅 수집 멈춤 — 읽기 전용 실행, stderr 를 버리지 않음 | Phase 12 | | | |
| reflect-collector:P4 | reflect-digest 머리에 수집 상태 줄과 facets 대조 | Phase 12 | | | |
| reflect-collector:P5 | 프로젝트 이름을 워크트리 폴더가 아니라 본 레포 이름으로 | Phase 12 | | | harness/scripts/save-feedback.sh 도 같이 바뀐다 — harness:P02 와 함께 시험한다 |
| reflect-collector:P6 | tone-kit K-11 — 사전에 없는 한국어 합성어를 새로 만들지 않음 | Phase 15 | | | |
| user-setup:P1 | codegen 의 build-filter 줄을 전부 없앰 | Phase 5 | | | flutter:P-F06-codegen-delete-count 와 방향이 두 갈래 — 카이젠에서 하나로 정한다 |
| user-setup:P2 | /sprint 에 워크트리 권고, 폐기 결정 줄, 커밋 전 삭제 보고 | Phase 4 | | | harness:P07 과 겹친다. 커밋 전 삭제 멈춤은 이번 스프린트 훅과 같은 일이다. 폐기 결정 기록 자리 네 곳 · 기준 커밋 가르기 세 곳 — 카이젠에서 하나로 정한다 |
| user-setup:P3 | 화면 규약 Step 0·2·3·4 보강 | 이번 스프린트 | insights-0924-hooks-skill-collector | | flutter:P-VEP-* 제안과 같은 것이라 한 번만 넣었다 |
| user-setup:P4 | qa-evaluator 규칙 10 뒤 네 줄 (첫 칸만 · 안 돌아가는 시험 · 전체 꺼짐 · 삭제 열거) | Phase 3 | | | harness:P04 와 같다 — 한쪽만 남긴다. 변경분 삭제 파일 열거는 harness:P04 에 없다 |
| user-setup:P5 | contract-schema 셸 이식성 절에 zsh 배열 한 줄 | Phase 2 | | | harness:P05 와 같은 줄 |
| user-setup:P6 | 핸드오프 템플릿에 폐기·거절한 결정 절 | 해당 없음 | | | 킷 밖 — 카이젠 뒤 사용자 설정 처리 목록 |
| user-setup:P7 | parallel-session-guard.sh 구멍 두 개와 커밋 직후 삭제 수 알림 | 해당 없음 | | | 킷 밖 — 카이젠 뒤 사용자 설정 처리 목록. 킷 훅은 50 개를 넘을 때만 알리므로 두 번 울리는지 그때 확인한다 |
| user-setup:P8 | 플러터 검증 규칙에 「표식이 안 바뀌면 앱을 새로 띄운다」 반 문장 | 해당 없음 | | | 킷 밖 — 카이젠 뒤 사용자 설정 처리 목록 |
| user-setup:P9 | 전역 CLAUDE.md 두 줄 — 못 한다고 할 때 막는 것과 우회, 작은 수정 예외 | 해당 없음 | | | 킷 밖 — 카이젠 뒤 사용자 설정 처리 목록. 사용자 확인 필요 |
| user-setup:P10 | 한 프로젝트 기억 두 가지 — 한 나라 우선 추론 금지, 공용 폴더 커밋 요령 정리 | 해당 없음 | | | 킷 밖 — 카이젠 뒤 사용자 설정 처리 목록. 사용자 확인 필요 |
| other-kits:P4 | howto-audit 이 자식 셸에서 검사 함수를 못 부름, 상대 경로 호출 | Phase 17 | | | |
| other-kits:P3 | 자동 검사에 howto-kit 시험 단계, onboarding-kit 의 등록 안 된 시험 입력 3 개 | Phase 14 | | | howto-kit 단계는 Phase 17 과 함께 넣는다. ci.yml 은 이번 스프린트가 이미 고쳤으니 그 위에 더한다 |
| other-kits:P2 | react-kit project-detect.sh 가 없는 값을 참으로 읽는 비교 버그 | Phase 10 | | | 부르는 스킬이 없다 — 지울지 고칠지 사용자 확인 |
| other-kits:P1 | 리액트 규약에 「지금 보는 화면을 이번 코드가 그렸는지」 확인, 개발 서버 포트 고정 | Phase 10 | | | 리액트 규약에는 되말하기·화면 자체 대상도 없다(검토자 지적, F01) |
| other-kits:P5 | react-preflight 보고에 skipped 칸, 0 개 실행은 통과로 적지 않음 | Phase 10 | | | |
| other-kits:P7 | api-verify 경로 간 조건에 양쪽 실제 값, 판정 불가를 따로 셈 | Phase 16 | | | |
| other-kits:P8 | api-ui 에 브라우저로 여는 화면 확인 한 단계 | Phase 16 | | | |
| other-kits:P10 | V10 표 검사 범위에 skills/*/references 아래 문서를 더함 | Phase 4 | | | validate-plugin.py 는 harness-kaizen 이 본다 |
| other-kits:P6 | react-l10n 의 extract --clean 을 기본 흐름에서 뺌 | Phase 10 | | | |
| other-kits:P9 | setup-guide 의 막는 요구에 출처 · 막히는 것 · 우회를 함께 | Phase 14 | | | |
| insights:scope-commit-block | 선언한 범위 밖 파일의 커밋 차단 (인사이트 장기 제안) | Phase 4 | | | 계약 지정 배정. 범위 선언을 기계가 읽을 자리가 킷에 없어 이번 스프린트에서 빼고 넘겼다 |

## Phase 별 적용 힌트

- **Phase 1 설계 가이드** — harness:P09 · F10. 못 한다고 말하기 전에 막는 것 · 시도한 우회 · 다시 돌릴 명령을 적게 한다. harness:P05 의 §3.7 부분도 여기서 맞춘다.
- **Phase 2 contract** — harness:P03 · harness:P05 · harness:P06 · harness:P08 · user-setup:P5 · F11 · F12 · F13 · F17 · F21 · F27. 계약의 명령은 봉인 전에 돌려 보고, 시각은 명령 출력에서 가져오고, 조건 수는 작업 크기에 맞춘다.
- **Phase 3 evaluator** — harness:P04 · user-setup:P4 · F16 · F31. 산출물이 검사일 때 평가자가 사본 입력으로 직접 돌려 보는 확인 목록을 한 벌만 넣는다.
- **Phase 4 harness** — harness:P02 · harness:P07 · user-setup:P2 · other-kits:P10 · insights:scope-commit-block · F08 · F09 · F14 · F18 · F28. 내 경로만 커밋하게 하고, 기준 커밋 가르기 규칙을 하나로 정한다. 범위 밖 커밋 차단은 범위 선언을 둘 자리부터 정한다.
- **Phase 5 flutter-toolkit** — flutter:P-F06-codegen-delete-count · flutter:P-INSPECTOR-convention · flutter:P-TEST-locale-buildmod · flutter:P-CATALOG-tile-height · user-setup:P1 · F02 · F06 · F22 · F24 · F25. build-filter 방향을 먼저 하나로 정한다. 규약 보강·편집 파일 포맷 훅·flutter-ui-verify 는 이번 스프린트가 넣었으니 다시 넣지 않는다.
- **Phase 6 design-kit** — design:P1 ~ design:P7 · F01 · F04. 플러터 규약에 들어간 되말하기·관례 표·반영 확인·점검 목록을 design-kit 규약과 맞춘다. 기존 화면 수(2 대 3)와 되풀이 상한(3 대 5)을 먼저 하나로 정한다.
- **Phase 7 backend-kit** — backend-family:P2. 시각은 한 순간과 벽시계를 가르고, 나라·시간대는 설정값으로 받는다.
- **Phase 8 infra-kit** — backend-family:P3. 자동 검사 실패를 내 변경 · 기준 커밋에서 이미 실패 · 환경으로 가른다.
- **Phase 9 rust-kit** — backend-family:P4 (backend-family:P2 의 rust-model 부분 포함). 실패를 내 변경 · 남의 미커밋 · 기준 커밋으로 가른다.
- **Phase 10 react-kit** — other-kits:P1 · other-kits:P2 · other-kits:P5 · other-kits:P6 · F03 · F05. 지금 보는 화면이 이번 코드인지 확인하고, 0 개 실행을 통과로 적지 않는다.
- **Phase 11 planning-kit** — backend-family:P1 · F20. 폐기한 결정을 제품 요구 문서에 남기되, 기록 자리를 하나로 정한 뒤에 넣는다.
- **Phase 12 reflect-kit** — reflect-collector:P3 · reflect-collector:P4 · reflect-collector:P5. 멈춘 Stop 훅 수집을 되살리고, 수집이 멈췄음을 요약 머리에 드러낸다.
- **Phase 13 bambu-kit** — bambu:P1 ~ bambu:P6 · F30. MakerWorld 읽는 순서, 칸마다 읽기, 정답 아는 입력.
- **Phase 14 onboarding-kit** — other-kits:P3 · other-kits:P9. 등록 안 된 시험 입력을 돌리는 자리에 넣고, 막는 요구에 출처와 우회를 함께 적는다.
- **Phase 15 tone-kit** — reflect-collector:P6 · F19. 새 합성어 금지를 관측 컨벤션 강도로 넣는다.
- **Phase 16 api-kit** — other-kits:P7 · other-kits:P8. 경로 간 조건에 양쪽 값을 적고, 화면 확인 숫자를 보고에 인용한다.
- **Phase 17 howto-kit** — other-kits:P4 (other-kits:P3 의 howto-kit 자동 검사 단계 포함). 검사 함수가 자식 셸에서 실제로 불리게 고친다.
- **킷 밖** — user-setup:P6 ~ user-setup:P10 은 카이젠 뒤 사용자 설정 처리 목록으로 넘긴다.
