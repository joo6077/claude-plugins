# Kaizen Data Pool

Generated: 2026-09-24T19:27:38
Generator: `scripts/collect-kaizen-data.py`

카이젠 오케스트레이션의 Phase 별 서브에이전트가 참조할 통합 데이터 풀이다. 이 파일은 `scripts/collect-kaizen-data.py` 로 재생성된다 — 수동 수정 금지.

## 0. `/insights` Report (외부 도구 산출물)

- 경로: `.claude/kaizen-input/insights-report.md` · Markdown 추출본
- 보고서 관측 기간: 2026-09-14 ~ 2026-09-23 (출처: `~/.claude/usage-data/report-2026-09-24-095238.html` 본문)
- 기준 시각: 2026-09-24T00:00:00 (frontmatter generated) ✓ VERY FRESH (19.5시간 전)
- 모든 Phase 서브에이전트가 **최우선** 참조해야 한다 (Friction Points / Recommended Patterns / Feature Suggestions / 이번 사이클 신규 워크플로우 제안)

<details><summary>insights report 본문 (auto-extracted)</summary>

---
source: claude-code-insights
generated: 2026-09-24
window: "2026-09-14 ~ 2026-09-23 (18 세션, 메시지 290)"
report_file: ~/.claude/usage-data/report-2026-09-24-095238.html
supersedes: 2026-08-13
facets: ~/.claude/usage-data/facets/
session_meta: ~/.claude/usage-data/session-meta/
---

##### Claude Code Insights — 카이젠 입력 (§0)

관측 기간 2026-09-14 ~ 2026-09-23, 18 세션. 인사이트 리포트 항목 F01~F32 와 빈틈 대조 제안 64 건을
아래 처리 배정표에 한 줄씩 올렸다. 각 Phase 는 자기 배정 줄만 맡고, 아래 흡수 표에 있는 것은 새 규칙으로 또 넣지 않는다.

###### 직전 사이클 흡수분 — 중복 금지

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

###### 이번 델타 요약 (2026-09-14 ~ 2026-09-23)

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

###### 처리 배정표

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
| F07 | 잘못된 커밋이 파일 3217 개를 삭제로 기록 | 이번 스프린트 | insights-0924-hooks-skill-collector | APPROVE | harness:P01 커밋 안전 훅 (커밋 전 50 개 넘는 삭제 차단, 커밋 직후 알림) |
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
| F23 | 디버그 겹침을 칩 렌더링 결함으로 오진 | 이번 스프린트 | insights-0924-hooks-skill-collector | APPROVE | flutter:P-VEP-shot-checklist 의 디버그 겹침 줄. 남은 제안 없음 |
| F24 | 기본 로캘·빌드 중 provider 수정 때문에 시험 실패 | Phase 5 | | | flutter:P-TEST-locale-buildmod |
| F25 | 그룹 설정 시안 21 종 | Phase 5 | | | 사고는 flutter-widget 에서 났는데 그 자리를 고치는 제안이 없다(검토자 지적). design-kit 쪽은 design:P2(Phase 6). 한 프로젝트 기억(「여러 개 다 만들어 나란히」)과 방향이 반대라 사용자 확인이 필요하다 |
| F26 | 스크린샷을 합의 조건으로 — 기준 화면, 변경, 재촬영, 비교, 스스로 고치기, 전·후 보고 | 이번 스프린트 | insights-0924-hooks-skill-collector | APPROVE | flutter-ui-verify 스킬과 규약 두 번 실행. design-kit 쪽 비교 반복은 design:P6(Phase 6) |
| F27 | 스스로 검증하는 계약 — 조건마다 명령·출력·종료 코드, 계약 검사기, 크기 검사 | Phase 2 | | | harness:P02 · harness:P03 · harness:P06 |
| F28 | 워크트리 준비 스크립트, 워크트리 상태 스크립트, 커밋 전 검사 | Phase 4 | | | 50 개 넘는 삭제는 이번 스프린트 훅. 범위 밖 파일 차단은 insights:scope-commit-block. 시뮬레이터·데이터베이스 나누기와 워크트리 상태 스크립트는 맡은 제안이 없다(검토자 지적) |
| F29 | Edit·Write 뒤 편집한 파일만 dart format | 이번 스프린트 | insights-0924-hooks-skill-collector | APPROVE | flutter:P-FORMAT-changed-files 와 format-edited-dart.sh 훅. 사용자 block-dirwide-autofixer.sh 가 fvm 붙은 형태를 놓치는 것은 킷 밖 |
| F30 | MakerWorld 를 헤드리스 브라우저로 긁다 막힘 | Phase 13 | | | bambu:P1 |
| F31 | 측정 스크립트·UI 변경마다 독립 검토 에이전트 | Phase 3 | | | 계약 지정 배정. harness:P04 와 함께 본다. 관례 대조는 flutter:P-INSPECTOR-convention(Phase 5) |
| F32 | 카이젠 수집기가 8 월 요약본을 집고 facets 를 안 읽음 | 이번 스프린트 | insights-0924-hooks-skill-collector | APPROVE | reflect-collector:P1 · reflect-collector:P2, harness 카이젠 3 스킬의 §0 경유, 이 파일 교체 |
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
| flutter:P-VEP-two-phase | 규약을 편집 전과 완료 직전 두 번 부르고 다섯 UI 스킬에 편집 전 호출 | 이번 스프린트 | insights-0924-hooks-skill-collector | APPROVE | SK-03(a) · SK-04 |
| flutter:P-VEP-restart-marker | 재캡처 전 반영 확인 — 바뀌어야 할 표식으로 판정, 안 되면 앱을 다시 띄움 | 이번 스프린트 | insights-0924-hooks-skill-collector | APPROVE | SK-03(c) |
| flutter:P-VEP-shot-checklist | 캡처 점검 목록 — 넘침·글리프·칩·뱃지·카드와 평평한 줄·디버그 겹침 | 이번 스프린트 | insights-0924-hooks-skill-collector | APPROVE | SK-03(d) |
| flutter:P-VEP-intent-convention | Step 0 에 요청 되말하기·화면 자체 대상·관례 표 | 이번 스프린트 | insights-0924-hooks-skill-collector | APPROVE | SK-03(b) |
| flutter:P-VEP-tool-diagnosis | 도구가 고장이라 말하기 전 확인 순서 | 이번 스프린트 | insights-0924-hooks-skill-collector | APPROVE | SK-03(e) |
| flutter:P-INSPECTOR-convention | widget-inspector 에 관례 대조 감지 기준 | Phase 5 | | | |
| flutter:P-TEST-locale-buildmod | flutter-test 에 기본 로캘·빌드 중 provider 수정 함정 | Phase 5 | | | |
| flutter:P-CATALOG-tile-height | 카탈로그 타일 높이를 내용보다 낮게 고정하는 함정 | Phase 5 | | | |
| flutter:P-FORMAT-changed-files | 포맷 범위를 이번에 바뀐 .dart 파일로 좁힘 | 이번 스프린트 | insights-0924-hooks-skill-collector | APPROVE | AR-05. 제안은 훅을 빼자고 했지만 이번 스프린트는 편집 파일 포맷 훅(F29)도 함께 넣었다 |
| flutter:P-EVAL-ui-loop | flutter-widget 평가 사례 — 되말하기·관례 표·기준 캡처·반영 확인·점검 목록 | 이번 스프린트 | insights-0924-hooks-skill-collector | APPROVE | SK-06 |
| harness:P01 | 커밋 안전 훅 — 커밋 전 대량 삭제 차단, 커밋 직후 알림 | 이번 스프린트 | insights-0924-hooks-skill-collector | APPROVE | SC-01~SC-03 · ER-01 · ER-02 |
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
| reflect-collector:P1 | 수집기가 요약본을 「어느 보고서를 요약했나」(report_file)로 고름 | 이번 스프린트 | insights-0924-hooks-skill-collector | APPROVE | SC-05 · SC-06 |
| reflect-collector:P2 | facets·session-meta 를 §0 안 0-b 절로 싣고 --usage-data 옵션을 둠 | 이번 스프린트 | insights-0924-hooks-skill-collector | APPROVE | SC-07 · SC-08 · ER-03 |
| reflect-collector:P3 | reflect-kit Stop 훅 수집 멈춤 — 읽기 전용 실행, stderr 를 버리지 않음 | Phase 12 | | | |
| reflect-collector:P4 | reflect-digest 머리에 수집 상태 줄과 facets 대조 | Phase 12 | | | |
| reflect-collector:P5 | 프로젝트 이름을 워크트리 폴더가 아니라 본 레포 이름으로 | Phase 12 | | | harness/scripts/save-feedback.sh 도 같이 바뀐다 — harness:P02 와 함께 시험한다 |
| reflect-collector:P6 | tone-kit K-11 — 사전에 없는 한국어 합성어를 새로 만들지 않음 | Phase 15 | | | |
| user-setup:P1 | codegen 의 build-filter 줄을 전부 없앰 | Phase 5 | | | flutter:P-F06-codegen-delete-count 와 방향이 두 갈래 — 카이젠에서 하나로 정한다 |
| user-setup:P2 | /sprint 에 워크트리 권고, 폐기 결정 줄, 커밋 전 삭제 보고 | Phase 4 | | | harness:P07 과 겹친다. 커밋 전 삭제 멈춤은 이번 스프린트 훅과 같은 일이다. 폐기 결정 기록 자리 네 곳 · 기준 커밋 가르기 세 곳 — 카이젠에서 하나로 정한다 |
| user-setup:P3 | 화면 규약 Step 0·2·3·4 보강 | 이번 스프린트 | insights-0924-hooks-skill-collector | APPROVE | flutter:P-VEP-* 제안과 같은 것이라 한 번만 넣었다 |
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

###### Phase 별 적용 힌트

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

</details>

### 0-b. 세션별 분석 (facets)

§0 보고서와 같은 세션에서 나온 원자료다 — 건수를 §0 과 더하지 마라

- 소스: `~/.claude/usage-data/facets/*.json` 과 짝 `session-meta/<id>.json` (facets 가 없는 session-meta 는 세지 않는다)
- 집계: 세션 18 · 프로젝트 묶음 2 · 임시 폴더 2 · 못 읽은 파일 0 (깨진 facets JSON 0 · session-meta 없음·깨짐 0)

마찰 종류 이름은 합치지 않는다 (`environment_issue` 와 `environment_issues` 는 다른 줄이다).

| 프로젝트 묶음 | 세션 | outcome 분포 | 마찰 합계 |
| --- | --- | --- | --- |
| fit-pal | 10 | mostly_achieved 8 · partially_achieved 2 | wrong_approach 17 · buggy_code 14 · misunderstood_request 13 · environment_issues 5 · incorrect_diagnosis 3 · environment_tooling_issue 2 · incomplete_work 2 · slow_progress 2 · excessive_changes 1 · incorrect_claim 1 · premature_giving_up 1 |
| claude-plugins | 6 | mostly_achieved 4 · fully_achieved 2 | buggy_code 14 · wrong_approach 3 · environment_issue 1 · excessive_changes 1 · misunderstood_request 1 |
| (임시 폴더 — 시험 세션) | 2 | fully_achieved 1 · not_achieved 1 | missing_tools 1 |

- 전체 마찰 합계: buggy_code 28 · wrong_approach 20 · misunderstood_request 14 · environment_issues 5 · incorrect_diagnosis 3 · environment_tooling_issue 2 · excessive_changes 2 · incomplete_work 2 · slow_progress 2 · environment_issue 1 · incorrect_claim 1 · missing_tools 1 · premature_giving_up 1 (합 82)
- 전체 outcome: mostly_achieved 12 · fully_achieved 3 · partially_achieved 2 · not_achieved 1

#### 세션별 행

`friction_detail` · `brief_summary` 는 원문이다 (줄바꿈만 공백으로 폈다). `언급된 킷` 은 플러그인 이름이 목표·마찰 원문에 글자 그대로 나온 것만 적었다.

- `9a0d4163` · 2026-09-14 · fit-pal · 마찰 7 · 언급된 킷: (킷 언급 없음 — 전 Phase 공통)
  - friction_detail: Claude re-introduced previously-discarded timezone/country settings ('내가 분명히 폐기처리햇는데'), repeatedly reasoned Korea-first despite user correction, a bulk-delete script over-deleted code blocks, and a bad git commit recorded 3217 files as deleted before being reverted.
  - brief_summary: User wanted group settings screens redesigned with mockups and role-based visibility, which led to discovering and removing obsolete group timezone/country fields via a full server migration to wall-clock scheduling — Claude delivered 21 mockup variants and the server refactor with all 1115 tests passing, though with friction from resurrecting discarded decisions and Korea-centric assumptions.
- `e19c3133` · 2026-09-16 · fit-pal · 마찰 3 · 언급된 킷: (킷 언급 없음 — 전 Phase 공통)
  - friction_detail: Claude's build-filter codegen deleted 267 generated files (self-recovered), a test failed due to default locale/provider-modified-during-build bugs, and it misdiagnosed a debug overlay as a chip rendering defect before correcting itself.
  - brief_summary: User asked Claude to resume a wall-clock scheduling migration from stage 4 of a handoff doc; Claude implemented the server/app holiday changes, refactors, group settings and photo editing, verified on simulator, pushed five-plus commits, and prepared a next-session handoff, with only deferred items remaining.
- `00f4e982` · 2026-09-17 · fit-pal · 마찰 12 · 언급된 킷: (킷 언급 없음 — 전 Phase 공통)
  - friction_detail: Claude repeatedly built onboarding pages with wrong content (set rows on home, non-existent face-grid widget, padded real widgets, fake action band instead of real bottom sheet), dropped an approved page, put the ✕ icon on collapse instead of finish, and shipped overflow/broken-glyph issues the user had to catch.
  - brief_summary: User wanted onboarding guide sheets built from real app widgets and repeatedly corrected Claude's wrong content, missing pages, and layout bugs; much landed and was committed, but the player guide was deferred to a next session as still unsatisfactory.
- `a1412bc8` · 2026-09-18 · fit-pal · 마찰 9 · 언급된 킷: (킷 언급 없음 — 전 Phase 공통)
  - friction_detail: Claude misdiagnosed MCP tooling as broken three times (wrong arg key, wrong assumption that bottom sheets are invisible to the widget walker, actually attached to another session's simulator), and initially misread which 'time text' misalignment the user meant.
  - brief_summary: User wanted a swipeable routine-turn carousel in the routine picker with polished visuals; Claude designed, implemented, tested, committed it and eventually verified swiping on the real simulator, though several self-inflicted misdiagnoses of MCP tooling cost significant time.
- `e863512e` · 2026-09-18 · fit-pal · 마찰 8 · 언급된 킷: (킷 언급 없음 — 전 Phase 공통)
  - friction_detail: Claude initially declared two tasks impossible ('app hasn't shipped', 'no physical device') prompting the user's pushback '앱 올리면 되잖아?', then spent hours chasing a continuously-red shared dev branch broken by other sessions before the user had to suggest using a separate worktree and twice asked '아직도 안함?' / '테스트 진행됨?'.
  - brief_summary: User wanted the deferred wall-clock tasks completed and a real release shipped; Claude dropped the guard columns, diagnosed and fixed five unrelated CI breakages from other sessions, cut a release branch from a verified commit, and shipped app 0.14.0 to TestFlight/Play plus server 0.14.0 — but only after being pushed to stop giving up and to isolate work in its own worktree.
- `1f6230f1` · 2026-09-19 · (임시 폴더 — 시험 세션) · 마찰 0 · 언급된 킷: (킷 언급 없음 — 전 Phase 공통)
  - friction_detail: (없음)
  - brief_summary: User asked Claude to act as a QA evaluator and judge an implementation against a sprint contract; Claude verified all conditions, detected a misleading measurement command, ran cross-diagnosis, saved feedback, and issued a REJECT verdict with reasoning.
- `8fa13c90` · 2026-09-19 · claude-plugins · 마찰 6 · 언급된 킷: (킷 언급 없음 — 전 Phase 공통)
  - friction_detail: Claude invented a nonsensical Korean term ("표시훅") the user didn't understand, wrote contract verification commands it never actually tested (wasting a full QA round that returned REJECT), and buried the simple fix under a heavy contract/QA process that left the user asking "so what am I supposed to do?"
  - brief_summary: User complained that the style-check hook ran after the answer was written (producing duplicate output) and asked for it to be applied before reporting instead; Claude diagnosed the Stop-hook placement, moved the reminder to PostToolBatch, and verified it works, though the process was noisy and over-ceremonious.
- `bcf7a121` · 2026-09-19 · claude-plugins · 마찰 2 · 언급된 킷: bambu-kit
  - friction_detail: Claude's own contract/feedback artifacts were initially rejected by validators (missing project_hash/project_name, forbidden time notation, per-condition line formatting) requiring several self-correction cycles.
  - brief_summary: User wanted a defect-free 3D print profile for their fly-catcher model plus kit documentation and QA validation; Claude produced measured profiles, updated 14 files, and got independent QA approval (28/28 conditions), though push/PR remained pending.
- `cfa1f76f` · 2026-09-19 · fit-pal · 마찰 8 · 언급된 킷: (킷 언급 없음 — 전 Phase 공통)
  - friction_detail: Claude repeatedly built card-based mockups and wrong badge shapes/chips that ignored existing app conventions (flat rows, invite-envelope seal), and a file rename plus nested ProviderScope broke the catalog so scrolling appeared frozen twice.
  - brief_summary: User wanted the split-selection sheet redesigned using existing app widgets and conventions; after several corrective rounds (cards→flat rows, gradient chip→envelope seal, badge layout→polygon vertices, subtitle→auto-scrolling body-part strip) the final design was confirmed and shipped to origin/dev, though the production deploy was blocked by a broken dev build and real-device verification remained pending.
- `858c246f` · 2026-09-21 · (임시 폴더 — 시험 세션) · 마찰 1 · 언급된 킷: harness
  - friction_detail: No filesystem or shell tools (Bash, Read, Write, Grep, Glob) were available in the session, blocking the command at Step 0.
  - brief_summary: User ran a sprint-contract command but Claude could not proceed because no filesystem/shell tools were loaded; it clearly explained the blocker instead.
- `3ac429d0` · 2026-09-22 · fit-pal · 마찰 3 · 언급된 킷: (킷 언급 없음 — 전 Phase 공통)
  - friction_detail: Simulator/session contention and widget scroll targeting required several retries, and an attempt to force text overflow by editing the dev DB failed because the app caches templates (hot restart didn't help), so Claude pivoted to enlarging simulator font size.
  - brief_summary: User wanted the redesigned split sheet verified on device and then everything pushed/merged; Claude verified all four visual behaviors, found and committed three missing-definition/runner-config root causes blocking CI, fixed its own failing test, and merged PR #147 to main despite 11 unrelated failing tests from other sessions (user chose to proceed).
- `d204ea78` · 2026-09-22 · claude-plugins · 마찰 3 · 언급된 킷: (킷 언급 없음 — 전 Phase 공통)
  - friction_detail: Claude's own measurement scripts had bugs (G2/G3 arc lengths omitted, zsh array off-by-one) and a headless-browser scrape of MakerWorld was blocked by Cloudflare before delegating to Codex.
  - brief_summary: User wanted filament weight and properly tuned PETG-HF then ABS print profiles with overhang optimization for a bent exhaust duct; Claude measured all nine orientations by real slicing, produced validated baked 3mf bundles for both slicers, and delivered research-backed overhang speed fixes that were approved.
- `e163621c` · 2026-09-22 · fit-pal · 마찰 6 · 언급된 킷: (킷 언급 없음 — 전 Phase 공통)
  - friction_detail: Claude repeatedly substituted the rail's +/✎ chips for the user's actual request to show the exercise add/edit screens themselves, and once claimed the catalog was refreshed when hot restart had silently failed.
  - brief_summary: User wanted the player how-to guide boards reworked (motion + exercise add/edit screens) and visually verified; Claude delivered a three-page redesign with passing tests and safe commits but kept misreading the add/edit request, leaving it deferred to a handoff doc after the user grew frustrated.
- `e8a3c269` · 2026-09-22 · claude-plugins · 마찰 0 · 언급된 킷: harness
  - friction_detail: (없음)
  - brief_summary: User asked to verify the harness v0.10.0 QA-hook enforcement in the next session; Claude gathered current state via git/shell checks and wrote a ready-to-paste handoff document.
- `f5b7f3a5` · 2026-09-22 · claude-plugins · 마찰 5 · 언급된 킷: harness
  - friction_detail: Several self-inflicted measurement/shell bugs (zsh word-splitting silently yielding 0, broken YAML block, markdown table split by an insertion, a guessed timestamp causing a QA REJECT) required extra iterations, though Claude caught and fixed each.
  - brief_summary: The user asked Claude to resume verifying harness 0.10.0 loading and cross-diagnosis behavior, then complete remaining fixes and ship; Claude found the evaluator was faking cross-diagnosis, redesigned that flow across three sealed-contract sprints, merged PRs #76/#84/#86/#87, and released harness 0.11.0 plus sibling kit versions, with the fourth backlog sprint still in progress.
- `ad969ac3` · 2026-09-23 · fit-pal · 마찰 2 · 언급된 킷: (킷 언급 없음 — 전 Phase 공통)
  - friction_detail: Claude inverted the layout instruction, pinning the whole reaction row to the right instead of keeping reaction chips left-aligned with only the add chip pinned right, requiring a correction round-trip.
  - brief_summary: The user iteratively directed refinements to a cheer sheet's reaction row and inline comment input; Claude implemented, verified with live widget screenshots and tests, and fixed each issue after one misread instruction.
- `be3037df` · 2026-09-23 · claude-plugins · 마찰 4 · 언급된 킷: bambu-kit
  - friction_detail: Claude's own new checks repeatedly introduced silent-failure regressions (first-slot-only reads, test file registered only in a table, whole check disabled on one unparseable slot) that cross-review agents had to catch, plus a zsh word-splitting issue and a dropped connection during CI watching.
  - brief_summary: User asked to encode print-profile lessons into the bambu-kit validation skill, release the kits, and confirm the merged main still catches slicer key differences and geometry/wall-budget checks — Claude delivered five merged PRs, deployed six kits, and verified the checks live on latest main.
- `d93c7e7a` · 2026-09-23 · fit-pal · 마찰 3 · 언급된 킷: (킷 언급 없음 — 전 Phase 공통)
  - friction_detail: Claude initially over-thought the server 100-item limit as a blocker for onboarding samples (user pushed back: 'why does onboarding need server integration at all'), and a commit accidentally reverted another session's two commits before being repaired.
  - brief_summary: User wanted the onboarding guide pages rebuilt as real add/edit exercise screens plus several follow-up fixes (i18n, server limit raise, catalog caching, memory rule removal), and Claude delivered all of them with committed, tested changes despite one detour and a git index mishap.

## 0.5. 프로젝트 메모리 (`feedback` 타입 · 전 프로젝트 교차)

- 소스: `~/.claude/projects/*/memory/*.md` (`MEMORY.md` 은 색인이라 제외)
- 집계: 프로젝트 **7** · `feedback` 엔트리 **268** (스캔한 메모리 파일 510)
- 주입 **32** · 탈락 **236** (= 32 + 236 = **268**)
- grounding 분포: `user_correction` 31 · `execution_evidence` 58 · `mixed` 22 · `self_inference` 1 · `미분류` 156
- grounding 값이 허용 4 값 밖 → 집계 제외 **0** 건
- 재발 신호 참조 ledger: 없음 (`~/.claude/logs/*/promotions-ledger.md` 미존재 — 재발 가중치 0 으로 진행)

### 선별 축 · 읽는 법

- 선별은 **관련성 · 중요도 2 축**이다. **시간(recency) 축은 쓰지 않는다** — 갱신 시각 필드의 보유율이 낮아(실측 104 중 44) 나머지가 임의 판정되기 때문이다.
- **관련성**: 메모리 `description`·`name`(가중 2) 과 본문(가중 1) 의 도메인 키워드 일치. 데이터 풀은 Phase 별로 나뉘지 않으므로 아래 그룹 제목에서 자기 도메인을 찾아라.
- **중요도**: `grounding` 등급 + 재발 신호(본문의 반복 언급 + ledger `post_freq`/`initial_freq`). 그룹별 상위 3 건까지 본문을 싣고 (전체 상한 40), 나머지는 말미에 제목만 남긴다.
- ⚠ **`self_inference` 와 `미분류` 는 계약 조건의 PASS 근거로 쓰지 마라.** 외부 검증(사용자 교정 · 실행 증거)이 없는 자기추론이다. 참고 신호로만 읽고, 근거가 필요하면 원 출처를 다시 확인하라.
- 이 절은 **읽기 전용**이다. 카이젠은 메모리 파일도 승격 ledger 도 직접 쓰지 않는다 — 승격은 `/reflect-promote` 소관이다.

### 주입 — 도메인 그룹별

#### [harness] harness · 계약 · QA (Phase 2·3·4) — 전체 85 건 중 3 건 주입

- **바뀐 파일 범위 조건이 깨진 6가지 이유** — 계약에 "이번에 바뀐 파일이 몇 개"(AR-0x) 같은 조건을 걸고 git diff 로 재면 여섯 가지를 놓친다 — git 이 아직 추적하지 않는 새 파일, 다른 세션이 만든 변경, 잘못 잡은 비교 기준 커밋, 계약 옆에 따로 두는 보조 파일, 그 파일 자신을 담는 커밋 해시, 클릭으로
  - `~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/memory/feedback_diff_scope_oracle_blind_spots.md` · grounding `미분류` · 중요도 9 · 연관 `bambu`·`design` · ⚠ **PASS 근거 사용 금지**

<details><summary>feedback_diff_scope_oracle_blind_spots.md 본문 발췌</summary>

계약에 "이번에 바뀐 파일이 몇 개인지" 를 조건으로 걸어놓고 그걸 `git diff --name-only` 로 재면
아래 여섯 가지를 놓친다. 2026-09-06 한 세션에서 3 회, 2026-09-08 다른 세션에서 **같은 조건이
3 회 연속** 깨졌다.

| 회차 | 조건 | 깨진 이유 |
|---|---|---|
| 1 | `bambu-kit-enum-allowlist-gate` `AR-03` | 같은 시각에 돌던 다른 세션이 같은 경로의 파일을 건드려서, 세어진 파일 수가 6 개에서 10 개로 늘었다 |
| 2 | `harness-core-defects` `AR-03` | 조건이 `Given: 아직 커밋하지 않은 상태` 를 전제로 삼았는데, 다른 사람이 커밋을 해버려서 그 전제가 깨졌다 |
| 3 | `harness-attribution-followup` `AR-01` | **새로 만든 파일은 git 이 아직 추적하지 않아서 `git diff` 에 나오지 않는다** — 그래서 센 값이 0 이 됐다 |
| 4 | `howto-kit-implementation` `AR-07` | 비교 기준을 `main` 으로 잡는 바람에, **바로 앞 스프린트**(스프린트 이름표가 다르고 `status: done` 인)에서 만든 파일 2 개까지 이번 범위로 세어졌다. 스프린트 이름표란 파일 이름 앞에 붙는 그 스프린트 고유 이름이다 |
| 5 | 같은 조건, 2 차 시도 | 스프린트 이름표 하나당 만들어지는 파일이 3 종인데, 허용 목록에 그중 **계약 수정 기록을 담는 보조 파일**이 빠져 있었다. 그래서 A-01 을 적어 넣은 그 보조 파일 자체가 "범위 밖 파일 1 건" 으로 잡혔다 — 조건을 고치려고 한 조치가 만들어낸 파일이 같은 조건을 다시 깨뜨린 것이다 |
| 6 | 같은 조건, 3 차 시도 | 계약 수정 2 건의 동의를 **AskUserQuestion 선택지 클릭**으로 받았는데, 클릭은 프롬프트 로그에 남지 않아서 평가자가 근거를 못 찾고 `unanchored`(근거가 어디에도 없음)로 판정했다. 게다가 보조 파일에 적어둔 HEAD 커밋 해시를 바로 뒤에 `--amend` 로 무효화해버렸다 |

**Why:** `git diff` 는 (a) git 이 아직 추적하지 않는 새 파일을 빼고 세고, (b) 그 변경을 누가 썼는지
구분하지 않으며, (c) 비교 기준 커밋이 틀리면 남의 스프린트 작업까지 같이 센다. 조건이 재려던 것은
"내가 손댄 파일의 집합" 인데 검사는 "두 커밋 사이의 차이" 를 잰다 — 결함 태그로는 `측정-방식-불일치`
다. 4~6 번은 검사 방식 문제가 아니라 **계약을 쓴 사람의 실수**다: 측정하는 과정에서 생기는
파일(보조 파일, 커밋 해시, 동의 기록)이 측정 대상 안으로 들어온다는 걸 계약을 쓸 때 생각하지 못했다.

… (본문 18 줄까지만 — 전문은 위 경로를 직접 읽어라)

</details>

- **feedback_contract_baseline_oracle_multisession** — git-status baseline 스냅샷을 AR 변경범위 오라클로 쓰면 병렬 세션 환경에서 구조적으로 깨진다 — 5회 재발, 화이트리스트+금지목록 형태가 실전 통과 확인됨
  - `~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_contract_baseline_oracle_multisession.md` · grounding `execution_evidence` · 중요도 9 · 연관 `bambu`

<details><summary>feedback_contract_baseline_oracle_multisession.md 본문 발췌</summary>

Sprint Contract 의 변경범위 조건(AR-01 류)을 **"계약 시점 `git status` baseline 과 정확히
일치"** 로 쓰면, 같은 레포에서 다른 세션이 병렬로 작업하는 순간 **내 잘못 없이 FAIL 한다.**
qa-evaluator 가 이 프로젝트에서만 **4 회 연속** 같은 패턴을 REJECT 했다
(player-rest-standalone AR-04 · statistics-tab AR pathspec · figma-box-path-shape AR-01 ·
chat-thread-redesign AR-01).

**Why**: baseline 은 한 시점의 스냅샷인데 워킹트리는 공유 자원이다. 평가 시점의 워킹트리에는
남의 산출물이 섞여 있고, 계약 문언은 "정확히 일치" 를 요구하므로 오라클이 참을 반환할 수 없다.
더 나쁜 것은 구제 경로다 — 사이드카 amendment 에 "이건 남의 것" 이라고 근거를 붙여도,
평가자는 **사용자 발언 prompt-log 앵커**가 없으면 `unknown` 으로 분류해 PASS 근거로 안 쓴다.
그리고 AskUserQuestion 승인은 prompt 로그에 안 남아 앵커가 되지 않는다
([[feedback_contract_conflict_fix_code_not_wording]]).

**How to apply**: 변경범위 조건을 **baseline 차집합이 아니라 화이트리스트 + 금지목록**으로 써라.

```text
- [ ] AR-01: 이 스프린트가 만든/고친 파일이 아래 N 경로에 **포함된다** [exact, enumerated]
      (측정: 각 경로를 `git status --short -- <경로>` 로 개별 확인.
```

… (본문 18 줄까지만 — 전문은 위 경로를 직접 읽어라)

</details>

- **feedback_contract_scope_paths_after_design** — Sprint Contract 의 변경범위(AR-04) 경로 열거는 설계 확정 후에 써라 — 3연속 같은 이유로 QA FAIL
  - `~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_contract_scope_paths_after_design.md` · grounding `execution_evidence` · 중요도 9 · 연관 `flutter`·`backend`

<details><summary>feedback_contract_scope_paths_after_design.md 본문 발췌</summary>

Sprint Contract 의 diff-scope 조건(보통 `AR-04`)에서 **경로를 열거하는 절은 구현 설계가
확정된 뒤에 채워라.** 계약 작성 시점의 추정 경로로 `[exact, enumerated]` 를 쓰면 구현이
정당하게 인접 모듈을 건드리는 순간 자기 계약에 걸린다.

2026-08-11 세션에서 **연속 2회** 같은 이유로 QA FAIL:

- `statistics-tab`: 위젯 테스트를 `app/test/features/statistics/` 에 두는 게 프로젝트 관례인데
  pathspec 에 `app/test/catalog` 만 적어, **자기 산출물이 범위 밖**이 됐다.
- `muscle-share`: 소비자 소유 포트를 쓰면 provider 모듈(`server/modules/exercise/`)에 포트
  메서드가 추가되는데 경로 열거에 `record`·`apps/api`·`.harness` 만 적었다. 계약의 GAP 분석은
  이미 exercise 재사용을 예견하고 있었는데도 조건에 반영되지 않았다.

3 회째(`bodymap`)에도 또 틀렸다 — **이 메모를 쓴 직후 작성한 계약에서 바로 재발했다.**
`test/catalog` 의 import 갱신(이식의 불가피한 파생)을 경로에 안 넣었고, 문구는 "5 경로"라
쓰면서 6 개를 나열해 자기 서술도 어긋났다. "잘 쓰겠다"는 의도로는 안 막힌다.

**How to apply — 의도가 아니라 절차로 막는다:**
1. **커밋 직전에 diff-scope 명령을 실제로 실행하고, 그 출력에서 경로를 역산해 계약 AR 조건에

… (본문 18 줄까지만 — 전문은 위 경로를 직접 읽어라)

</details>

#### [flutter] flutter-toolkit (Phase 5) — 전체 58 건 중 3 건 주입

- **feedback_fifo_write_kills_flutter_run** — flutter run 에 hot reload 키를 보낼 때 fifo 대신 «보통 파일 + tail -f -n0» 을 stdin 으로 물려라 — fifo 는 상주 writer 를 둬도 죽었다
  - `~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_fifo_write_kills_flutter_run.md` · grounding `미분류` · 중요도 8 · 연관 `tooling`·`design` · ⚠ **PASS 근거 사용 금지**

<details><summary>feedback_fifo_write_kills_flutter_run.md 본문 발췌</summary>

`tail -f fifo | fvm flutter run` 또는 `flutter run < fifo` 구성에서 `printf 'r' > $FIFO`
로 hot reload 키를 보내면 **앱이 죽는다**. 리다이렉션이 끝나는 순간 writer 가 닫히고,
reader 가 EOF 를 받아 flutter run 의 stdin 이 닫히면서 프로세스가 종료된다.
2026-08-26 에 이걸로 다른 세션이 띄워둔 시뮬레이터 앱을 통째로 날렸다.

**상주 writer(`sleep 100000 > $FIFO`)를 먼저 띄워도 죽었다** (2026-09-04 재현).
그러니 fifo 자체를 쓰지 마라.

**Why:** fifo 는 writer 가 하나도 없으면 EOF 다. 한 번짜리 `>` 리다이렉션은 매번
open→write→close 라서 매 전송이 EOF 신호가 되고, macOS `tail -f` 는 fifo 에서 그 EOF 를
그대로 흘려보낸다. 보통 파일에는 EOF 개념이 이렇게 걸리지 않는다.

**How to apply:**
- **정본 레시피 — 보통 파일을 stdin 으로 물려라.** 2026-09-04 에 hot reload 4 회 연속 성공.
  ```sh
  : > "$S/cmds.txt"
  nohup sh -c "export PATH=\"\$PATH:/opt/homebrew/bin\"; cd <app 디렉터리>; \
    tail -f -n0 '$S/cmds.txt' | fvm flutter run -d <udid> \
```

… (본문 18 줄까지만 — 전문은 위 경로를 직접 읽어라)

</details>

- **feedback_bottomsheet_safearea** — 새 바텀시트는 showSheet 재사용 + 콘텐츠 bottom에 paddingOf bottom 필수. 직접 핸드롤 금지
  - `~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_bottomsheet_safearea.md` · grounding `user_correction` · 중요도 5 · 연관 `design`

<details><summary>feedback_bottomsheet_safearea.md 본문 발췌</summary>

새 바텀시트(showModalBottomSheet)를 만들 때 **바닥 세이프에리어(홈 인디케이터)를 자꾸 빠뜨림**. 2026-06-15 RoutineSelectionSheet 에서 사용자 재지적("왜 자꾸 바텀에 세이프에리어 적용 안 해? 룰로 안 되어있음?").

**Why:** 룰은 이미 `app/CLAUDE.md`에 있다 — "바텀시트 배경은 세이프에리어까지 확장(SafeArea로 시트 감싸지 않음), 콘텐츠만 `MediaQuery.paddingOf(context).bottom`을 bottom padding에 추가". 그런데 시트를 DecoratedBox+handle 로 직접 핸드롤하면서 이 룰을 빠뜨림. CLAUDE.md 에 있어도 매번 누락 → 실측 반복 지적.

**How to apply:**
1. 새 시트는 가능하면 `lib/shared/presentation/widgets/sheets/sheet_scaffold.dart` 의 `showSheet()` + `sheetHandleBar()` 재사용 (barrier/shadow/radius 공통 처리). 직접 `DecoratedBox`+핸들 핸드롤 금지.
2. 콘텐츠(특히 스크롤 리스트의 contentPadding)의 **bottom = base + `MediaQuery.paddingOf(context).bottom`**. 키보드 있으면 `viewInsetsOf(context).bottom` 도 합산.
3. 시트를 `SafeArea` 로 감싸지 말 것 — 배경이 화면 끝까지 못 덮음. 관련: [[feedback_safearea_scroll_surface]]

참조 관용구: `rest_timer_sheet.dart`(`28 + paddingOf bottom`), `member_profile_sheet.dart`(`AppSpacing.xl + paddingOf bottom`), `routine_item_edit_sheet.dart`(viewInsets+safeBottom 합산).

</details>

- **feedback_codex_dies_on_long_prompts** — codex-rescue 는 길고 여러 갈래인 프롬프트에서 최종 답 없이 끊긴다 — 한 문단짜리 질문 하나로 쪼개라
  - `~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_codex_dies_on_long_prompts.md` · grounding `미분류` · 중요도 5 · 연관 `research` · ⚠ **PASS 근거 사용 금지**

<details><summary>feedback_codex_dies_on_long_prompts.md 본문 발췌</summary>

**codex-rescue 는 요청이 길고 갈래가 많으면 최종 답 없이 끊긴다.** 2026-09-06 에 네 번
불렀는데 셋이 죽고 하나가 살았다. 갈린 축은 모델도 주제도 아니고 **프롬프트 길이와 질문
개수** 였다.

- 죽음 — 산출물 5개(셰이더 전문 + Dart 배선 + 프레임 의미론 + 샘플러 + 폴백)를 한 번에 요구
- 죽음 — 같은 요청을 `--resume-last` 로 이어붙이기 3회 시도(앞 스레드가 running 이라 거부)
- 죽음 — 산출물 3개로 줄였지만 여전히 여러 갈래
- **살아남음** — 질문 하나, 「band only 냐 full screen 이냐」, 답은 한 문단 + file:line

증상은 도구 트레이스만 잔뜩 남고 assistant 최종 메시지가 안 오는 것이다. 서브에이전트
transcript(`~/.claude/projects/*/subagents/agent-*.jsonl`)를 봐도 트레이스뿐이다. 앞 스레드가
안 끝나면 이어붙이기가 계속 거부되므로 **재시도 말고 새 스레드로 좁혀 다시 물어라.**

**Why:** 세 번 재시도하며 20분 넘게 날렸다. 그동안 답은 로컬에 이미 있었다 —
`~/fvm/versions/<ver>/engine/src/flutter` 에 엔진 소스가 통째로 있어서 uniform 복사 의미론,
스냅샷 크기, 샘플러 기본값을 내가 직접 읽어 확정했다.

**How to apply:**

… (본문 18 줄까지만 — 전문은 위 경로를 직접 읽어라)

</details>

#### [design] design-kit (Phase 6) — 전체 23 건 중 3 건 주입

- **feedback-design-detail-sketch** — 디자인 세부(코너/베벨/핀 모양) 텍스트 추측 반복 금지 — 1~2회 어긋나면 손그림 요청
  - `~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_design_detail_sketch.md` · grounding `user_correction` · 중요도 6 · 연관 `tooling`·`harness`·`flutter`

<details><summary>feedback_design_detail_sketch.md 본문 발췌</summary>

칩 코너 색·베벨·핀처럼 **시각적 세부 모양**을 사용자가 텍스트로 설명하면, 머릿속 추측으로 구현하지 마라. 2026-06-16~17 세션에서 "그룹칩 한 코너에 직각 그룹색" 하나를 텍스트 왕복으로 **40턴 가까이** 못 맞춰 사용자가 극도로 분노("말이 안통하노", 욕설 반복)했다.

**Why:** 코너 위치(우상/우하)·직각 여부·클립(겹치는 부분 자름)·테두리 유무·이모지 배경 투명 같은 미세 모양은 텍스트로 한 사람의 머릿속 이미지를 정확히 전달·복원하기 거의 불가능하다. 추측→구현→"이상함"→재추측 루프는 시간만 태우고 신뢰를 파괴한다.

**How to apply:**
1. 시각 세부가 **1~2회 어긋나면 즉시 멈추고** 손그림 사진 1장 또는 참조 앱 스크린샷을 요청하라. "이대로 진행"보다 "그림 한 장"이 빠르다.
2. 카탈로그(웹) 반복 재시작 대신, **MCP 연결을 유지하고 `mcp__fitpal-web__reload_app`(hot reload)** 로 반영하라. `flutter run` 재실행을 남발하면 MCP wrapper가 첫 VM에 고정돼 ambiguous로 캡처가 막힌다([[feedback_mcp_runtime_verify_no_relaunch]] 동일 교훈).
3. 내가 직접 확인할 땐 `screenshot_widget`은 flutter **web에서 layer assertion 버그**로 실패한다. 대신 macOS `screencapture -R<x,y,w,h> /tmp/cap.png` 후 Read 로 화면을 직접 본다. 사용자에게 "보세요"라고 떠넘기지 마라(반복 시 "만만하냐" 분노).
4. 관련: 시안은 실제 데코로 카탈로그 검증([[feedback_catalog_web]]), HTML 근사는 메탈/아쿠아 부정확.

</details>

- **feedback_render_capture_via_repaintboundary** — MCP 시각 캡처가 막히면 RepaintBoundary.toImage 위젯테스트 하네스로 실제 데코를 PNG 로 뽑아라
  - `~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_render_capture_via_repaintboundary.md` · grounding `execution_evidence` · 중요도 6 · 연관 `flutter`·`harness`·`tooling`

<details><summary>feedback_render_capture_via_repaintboundary.md 본문 발췌</summary>

fitpal-web/mobile MCP 의 `screenshot_widget` 이 `ext.flutter.inspector.screenshot` 쪽
assert(`RenderBox was not laid out: RenderSemanticsAnnotations#... NEEDS-LAYOUT`)로 막히면,
`set_overlay(false)` · `restart_app` 로도 안 풀린다. 거기서 더 파지 말고
([[feedback_mcp_screenshot_dont_spiral]]) **임시 위젯테스트 캡처 하네스**로 갈아타라.

**Why**: 이 경로는 실제 `BoxDecoration`/`FigmaDecoration`/그라디언트/섀도를 그대로 래스터라이즈
한다 — HTML 근사가 아니라 진짜 렌더다. 폰트만 테스트 폴백(글자가 네모)이라 **표면·레이아웃
판단에는 충분하고 텍스트 판독에는 부적합**하다. 결정적으로, 이걸로 실제 결함 2 건을 잡았다:
안 A 의 zebra 가 라이트에서 ΔRGB 2~8 로 안 보이는 것, 안 B 의 음각/양각이 다크에서 안 보이는 것.
둘 다 코드만 봐서는 안 나온다.

**How to apply**: `app/test/**/_x_capture_tmp_test.dart` 로 만들고 검증 후 **반드시 삭제**한다
(변경 범위 조건에 남으면 안 된다).

```dart
tester.view.physicalSize = const Size(440 * 2, 900 * 2); // 물리 픽셀! dpr 로 나눈 값이
tester.view.devicePixelRatio = 2;                        // 프레임보다 작으면 오버플로 인디케이터가
                                                          // 캡처 위에 덧그려진다
```

… (본문 18 줄까지만 — 전문은 위 경로를 직접 읽어라)

</details>

- **feedback-button-horizontal-padding** — 버튼·탭 요소는 좌우(가로) 패딩을 항상 넣는다 — 콘텐츠가 가장자리에 붙지 않게
  - `~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_button_horizontal_padding.md` · grounding `user_correction` · 중요도 5 · 연관 `flutter`

<details><summary>feedback_button_horizontal_padding.md 본문 발췌</summary>

버튼·탭 가능한 인터랙티브 요소(IFButton/IFMiniButton 등 버튼, 리스트 행, 칩, 아이템)를 구현·배치할 때 **좌우(horizontal) 패딩을 항상 포함**한다. 콘텐츠(텍스트·아이콘)가 화면이나 컨테이너 가장자리에 딱 붙으면 안 된다. 프로젝트 토큰(`AppPadding.h20`, `AppSpacing.*`) 사용.

**터치영역 풀폭과의 양립:** 행/버튼의 탭(hit) 영역이 화면 좌우 끝까지여야 하는 경우(예: 멤버 리스트 행)에는 **터치영역(Pressable)만 풀폭 + borderRadius 제거**로 하고, 그 **내부 콘텐츠 Row에는 좌우 패딩을 그대로 유지**한다. 둘은 모순이 아니다 — 풀블리드 탭 + 안쪽 콘텐츠 여백.

**Why:** 사용자가 "버튼 구현할 때마다 양옆 패딩을 안 넣는다"고 반복 지적(2026-06-16). 매번 짚어주게 하는 것은 마찰. 좌우 패딩 누락은 기본 실수로 취급하고 작성 시점에 항상 챙긴다.
**How to apply:** 버튼·탭 위젯 작성/수정 시 좌우 패딩을 기본으로 넣었는지 자기검토. 새 버튼/행/칩을 만들 때 `EdgeInsets.symmetric(horizontal: ...)` 또는 `AppPadding.h20`를 빠뜨리지 않는다. 관련: [[feedback_use_existing_skills]]

</details>

#### [backend] backend-kit (Phase 7) — 전체 9 건 중 3 건 주입

- **feedback_shared_index_use_private_index_file** — 공유 워크트리에서 커밋할 때는 GIT_INDEX_FILE 로 개인 인덱스를 써라 — add+commit 을 한 호출에 붙여도 새는다
  - `~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_shared_index_use_private_index_file.md` · grounding `미분류` · 중요도 4 · ⚠ **PASS 근거 사용 금지**

<details><summary>feedback_shared_index_use_private_index_file.md 본문 발췌</summary>

공유 워크트리(여러 세션이 같은 레포에서 동시에 일함)에서 커밋할 때,
**`git add <경로> && git commit` 을 한 Bash 호출에 붙여도 남의 파일이 실려 나간다.**
다른 세션이 그 «사이»가 아니라 «앞»에 이미 스테이징해 뒀으면 소용이 없다.

`git commit -- <경로>` 도 답이 아니다 — 인덱스를 무시하고 그 경로의 **워킹트리 전체**를
커밋하므로, 같은 파일 안에 있는 남의 hunk 가 딸려 들어간다(hunk 단위로 걸러 놨어도 무시된다).

**정답은 개인 인덱스 파일이다:**

```bash
IDX=$SCRATCH/myindex
GIT_INDEX_FILE=$IDX git read-tree HEAD
GIT_INDEX_FILE=$IDX git add <내 경로들>
# 같은 파일에 남의 hunk 가 섞였으면: GIT_INDEX_FILE=$IDX git apply --cached <내 hunk만 담은 patch>
GIT_INDEX_FILE=$IDX git commit -F msg.txt
```

공유 인덱스는 손도 안 대므로 남의 스테이징이 그대로 남고, 내 커밋에는 내 것만 담긴다.

… (본문 18 줄까지만 — 전문은 위 경로를 직접 읽어라)

</details>

- **feedback_verify_build_freshness_before_e2e** — 실기 e2e 전에 앱**과 서버** 둘 다 검증 대상 코드로 빌드됐는지 기동시각 vs 커밋시각으로 확인
  - `~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_verify_build_freshness_before_e2e.md` · grounding `execution_evidence` · 중요도 3 · 연관 `tooling`·`harness`·`flutter`·`design`·`infra`·`rust`

<details><summary>feedback_verify_build_freshness_before_e2e.md 본문 발췌</summary>

실기 e2e 를 돌리기 전에 **구동 중인 앱이 검증하려는 코드로 빌드된 것인지** 먼저 확인하라.
MCP 가 붙어 있고 동적 도구가 다 뜨고 런타임 에러가 0 건이어도, 그 앱이 옛 빌드면
**아무것도 검증되지 않는다.**

확인법 — 프로세스 기동시각과 커밋시각을 비교한다:

```bash
ps -o lstart= -p <flutter run pid>
git log -1 --format="%ad" --date=format:"%a %b %d %H:%M:%S %Y"
```

**Why:** 2026-08-11 세션에서 시뮬레이터에 떠 있던 `main.dart` 가 15:29 빌드였는데 검증 대상
커밋은 20:37 이었다. MCP attach·동적도구 26개·에러 0건이 전부 정상이라 그대로 e2e 를 돌 뻔했다.
hot reload 로도 안 메워진다 — drift `schemaVersion` 변경이나 freezed 재생성은 hot reload 가
반영하지 못한다.

**How to apply:**
- 내가 띄우지 않은 앱은 특히 의심하라. 병렬 세션·사용자가 몇 시간 전에 띄워 둔 것일 수 있다

… (본문 18 줄까지만 — 전문은 위 경로를 직접 읽어라)

</details>

- **feedback_worker_nplus1_tx_boundary** — read-decide-guard-write 백그라운드 잡의 N+1 배치화 — 입력을 tx 안/밖 어디서 읽을지 판정 기준
  - `~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_worker_nplus1_tx_boundary.md` · grounding `execution_evidence` · 중요도 3 · 연관 `harness`·`research`·`reflect`

<details><summary>feedback_worker_nplus1_tx_boundary.md 본문 발췌</summary>

2026-07-14 DB-1/DB-2 워커 N+1 배치화에서 확립. Codex 리서치(Postgres READ COMMITTED 공식 문서 근거).

**판정 기준:** "읽는 입력이 write(가드 UPDATE)의 정당성을 좌우하는가?"
- **좌우함 → tx 안에서 읽어라.** 예: resolution 잡의 투표. 투표로 outcome(모임 성사)을 계산하는데, 투표 API 가 resolved_at IS NULL 동안 과거 슬롯에도 투표를 허용한다(cast_vote 는 resolved_at 만 막고 scheduled_at 과거는 안 막음). tick 시작 배치로 투표를 미리 읽어두고 나중에 슬롯 확정하면, 그 사이 들어온 투표가 누락된 채 커밋된다. **가드 UPDATE(resolved_at IS NULL)는 중복 확정만 막지 stale input 은 못 막는다** — 멱등성 문제가 아니라 "결정 입력 신선도" 문제.
- **안 좌우함 → 배치 가능.** 예: 멤버 목록(참석자 후보). 멤버는 본래 per-slot tx 밖 포트 호출이라 배치해도 tx 경계 의미 불변.

**Why:** READ COMMITTED 는 문장별 스냅샷이라 read-decide-write 가 여러 문장에 걸치면 입력이 흔들린다. 결정 입력을 확정 write 와 같은 무결성 경계에 두려면 (1) 확정 tx 안 SELECT (2) 투표 먼저 닫기(status 전환) (3) 낙관적 version guard 중 하나 필요.

**How to apply:** 워커/크론 잡 N+1 을 배치로 풀 때, 각 입력마다 이 판정을 먼저 하라. 무조건 "다 tick 시작에 배치 프리로드"하지 마라. 단일 tx 잡(리마인더)은 tx 안에서 `= ANY($1)` 로 배치하면 스냅샷 동일(오히려 per-slot 개별 조회보다 일관적). per-slot tx 잡(결과확정)은 tx 밖 입력만 배치. 헥사고날: 다른 모듈 테이블 배치는 raw SQL 직격 말고 포트에 배치 메서드 추가([[project_audit_backlog_cb_cdn]]).

###### 색인 이관 상세 (2026-07-27 MEMORY.md 압축)

read-decide-guard-write 잡: 입력이 write 정당성 좌우하면 tx 안(투표), 아니면 배치 가능(멤버). 가드 UPDATE 는 중복만 막지 stale input 못 막음. 단일tx 잡은 = ANY 로 tx 안 배치

</details>

#### [infra] infra-kit · 훅 (Phase 8) — 전체 16 건 중 3 건 주입

- **feedback_app_deploy_local** — 앱(iOS/Android) 배포는 로컬 fastlane(make deploy-ios/android)으로. CI 아님 — 사용자 반복 지시
  - `~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_app_deploy_local.md` · grounding `mixed` · 중요도 5 · 연관 `flutter`·`backend`·`harness`

<details><summary>feedback_app_deploy_local.md 본문 발췌</summary>

앱(iOS·Android) 출시는 **로컬 fastlane**으로 한다: `cd app && make deploy-ios` / `make deploy-android` (= `bundle exec fastlane beta` / `internal`). GitHub Actions CI 워크플로우(`app-ios-testflight.yml`, `app-android-internal-test.yml`)로 끌고 가지 마라.

**Why:** 사용자가 2회 이상 명시("앱들은 그냥 로컬로해서 배포하라고"). 그리고 iOS CI는 구조적으로 못 됨 — self-hosted mac 러너(`fitpal-mac`)가 `svc.sh` LaunchAgent(서비스) 컨텍스트라 `security unlock-keychain`이 exit 51로 깨져 **단 한 번도 성공 못함**. 로컬은 GUI 로그인 세션이라 login 키체인이 이미 풀려 있어 Xcode 자동 서명(team DA3T6MDM25)으로 그냥 됨. (2026-06-16 build 5 로컬 업로드 성공, 0.3.0 build 4가 이미 TestFlight에 있어 로컬 경로가 원래 동작했음을 확인.)

**⚠️ 버전 함정 (2026-06-16 실수):** 로컬 `make deploy-ios`/`deploy-android`는 **현재 체크아웃 브랜치의 `app/pubspec.yaml` version**으로 빌드한다. release-please(app=`release-type: dart`)는 pubspec/manifest/태그를 **main**에서만 범프하므로 dev는 버전이 뒤처진다(예: main 0.4.0 / dev 0.3.0). dev에서 그냥 배포하면 **구버전(0.3.0)이 스토어에 올라간다.** 릴리스 배포는 반드시 `app-v<X>` 태그 또는 origin/main을 **체크아웃한 상태에서** 빌드하라(.env는 로컬 git-crypt라 유지됨). 또는 dev→main 머지 후 다음 버전으로 한번에 출시. iOS 빌드번호는 `latest_testflight+1` 자동, Android versionCode는 Play latest+1 자동.

**How to apply:** 사전조건 `app/.env.fastlane`(ASC API key id/issuer/p8 path, IOS_BUNDLE_ID, APPLE_TEAM_ID, PLAY_SERVICE_ACCOUNT_JSON_PATH) + `cd ios && bundle install` / `cd android && bundle install`. Makefile이 `.env.fastlane`을 `include`+`export`로 환경 주입. iOS는 빌드번호 자동 채번(latest_testflight+1), Android는 `internal` 트랙. **서버만** CI(self-hosted)로 배포 [[project_server_deploy_self_hosted]]. 앱 CI 배포 워크플로우는 자동 트리거(push tags)를 꺼두는 게 맞다(매 태그 실패 알림 방지). [[project_release_040_deploy]]

</details>

- **feedback-own-worktree-not-shared-dev** — fit-pal 에서는 공유 dev 트리에서 일하지 말고 내 워크트리를 따로 판다 — dev 는 늘 남이 쓰고 있다
  - `~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_own_worktree_not_shared_dev.md` · grounding `미분류` · 중요도 5 · 연관 `harness`·`rust`·`flutter`·`backend` · ⚠ **PASS 근거 사용 금지**

<details><summary>feedback_own_worktree_not_shared_dev.md 본문 발췌</summary>

**공유 워킹트리에서 작업하지 마라. 세션마다 제 워크트리를 판다.** 2026-09-19 사용자 지시.

**Why**: fit-pal 의 dev 는 상시 두셋이 붙어 있다. 2026-09-18~19 출시에서 이것 때문에 다섯 번
막혔다.

- `cargo clippy` · `flutter test` 가 남의 **미커밋 반제품**을 같이 컴파일해 판정이 불가능했다
  (서버 12 파일이 컴파일 실패 → 내 변경이 아닌데 내 검사가 섰다)
- `git-crypt unlock` 이 «Working directory not clean» 으로 거부됐다. 남의 작업이라
  stash 도 commit 도 못 한다 → 배포가 암호문 `.env.fastlane` 로 들어가 `make` 가 섰다
- 커밋마다 공유 인덱스에 남의 스테이징이 섞여 개인 `GIT_INDEX_FILE` 을 매번 세워야 했다
- 검사를 고쳐 push 하면 그사이 다음 반제품이 랜딩해 **끝없이 쫓게 된다**

**How to apply**:

1. 세션 시작 때 `EnterWorktree` 로 판다(`git worktree add` 직접 호출 금지 — 하네스가 모른다).
2. **git-crypt 키를 넣어야 시크릿이 풀린다.** 새 워크트리는 암호문으로 온다.
   워크트리 세션은 한 명령에 `git` 이 두 번 나오면 셸 가드가 막으므로 두 단계로 한다.
   ```bash
```

… (본문 18 줄까지만 — 전문은 위 경로를 직접 읽어라)

</details>

- **테스트가 구현의 값을 가져다 쓰면 그 값이 틀린 걸 못 잡는다** — 테스트 입력을 구현 코드 안의 목록에서 그대로 뽑아 쓰면, 그 목록 자체가 틀렸다는 사실은 아무리 돌려도 드러나지 않는다. 실제 도구의 실제 옵션을 손으로 적어 넣고 확인하는 검사를 따로 둬야 한다 — 2026-08-15 훅 작업에서 조합 84가지가 전부 통과했는데 실제 옵션을 넣자 잘
  - `~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/memory/feedback_self_referential_oracle_blind.md` · grounding `execution_evidence` · 중요도 4 · 연관 `backend`

<details><summary>feedback_self_referential_oracle_blind.md 본문 발췌</summary>

테스트에 넣을 입력을 **구현 코드 안에 적혀 있는 목록에서 그대로 뽑아 쓰면**(구현과 테스트가
서로 어긋나는 걸 막으려고 흔히 이렇게 한다), 그 목록 자체가 틀렸다는 사실은 **구조상 절대
드러나지 않는다**. 실제로 명령을 돌려보는 테스트여도 마찬가지다 — 검사하는 쪽과 검사받는 쪽이
같은 값을 보고 있으니, 그 값이 틀려도 둘이 사이좋게 틀린 채로 통과한다. 그러니 **바깥에서 실제로
확인한 값**(그 도구가 진짜로 받는 옵션, 서버가 진짜로 돌려준 응답)을 **손으로 적어 넣는 검사를
따로** 둬라.

**Why:** 2026-08-15 훅 작업에서 조합 84가지(도구 14개 × 동작 방식 2가지 × 값을 주는 방식 3가지)를
훅 코드에 적혀 있는 `TOOLS_NAME`/`TOOLS_RO` 목록에서 뽑아 돌렸다. 결과는 `mismatch=0` 이었고, 일부러
틀리게 바꾼 7가지 변형을 넣어 검사가 걸러내는지 확인하는 것도 전부 통과했다. 그런데 실제 도구가
받는 옵션을 손으로 넣어보니 **문제가 없는데 잘못 잡은 것 7건 + 문제가 있는데 못 잡은 것 1건**이
나왔다. 가장 위험했던 건 `validate-plugin.py --check=LIST` 를 "읽기만 하는 명령"으로 분류해 둔
것이다. `--check` 는 어떤 항목을 검사할지 «고르는» 옵션일 뿐이고 파일을 고칠지는 `--fix` 가
정하므로, `--check=x --fix` 가 막는 검사를 그대로 통과해서 실제로 파일을 고쳤다. 목록이 틀려
있었으니, 그 목록에서 뽑아 만든 84가지는 같은 오류를 계속 다시 찍어낼 뿐이었다.

**How to apply:**
- 구현에서 값을 뽑아 쓰는 검사(구현과 테스트가 어긋나는 걸 막는 용도)와 **바깥에서 확인한 값을

… (본문 18 줄까지만 — 전문은 위 경로를 직접 읽어라)

</details>

#### [planning] planning-kit (Phase 11) — 전체 2 건 중 2 건 주입

- **feedback-brainstorm-one-question** — 브레인스토밍은 한 질문씩, 구현 전 충분히 탐색 — 다중 질문 배치 금지
  - `~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_brainstorm_one_question.md` · grounding `user_correction` · 중요도 3 · 연관 `design`·`backend`

<details><summary>feedback_brainstorm_one_question.md 본문 발췌</summary>

브레인스토밍(superpowers:brainstorming) 진행 시 AskUserQuestion으로 여러 질문을 한 번에 배치하지 마라. **한 번에 한 질문씩** 물어라. 2026-05-30 그룹 상세 compact-dot 설계 중, 백엔드 의미론 결정 3개(presence/streak/mode-UI)를 한 번에 몰아 물었다가 사용자가 거부하고 "구현하기 전에 브레인스토밍 하고 진행하자"고 명시 요청.

**Why:** 사용자는 구현으로 서둘러 넘어가는 흐름을 경계한다. 여러 질문을 몰면 충분한 탐색 없이 결정을 강요하는 느낌. brainstorming 스킬 자체도 "One question at a time"을 명시.

**How to apply:** 결정 포인트가 여러 개여도 한 번에 하나씩, 직전 답을 반영해 다음 질문을 다듬어라. 트레이드오프를 짧게 설명한 뒤 단일 질문. 설계 승인 전엔 구현 스킬 호출 금지(HARD-GATE). 관련 [[feedback_research_before_flip_flop]].

</details>

- **h2s-arc-fitting-curve-planning** — H2S 기본 프로파일은 enable_arc_fitting=1로 출고되는데 H2S 펌웨어에는 Curve Planning이 있어 서로 간섭한다. Studio 자신이 끄라고 경고한다
  - `~/.claude/projects/-Users-jackson/memory/bambu_h2s_arc_fitting_off.md` · grounding `미분류` · 중요도 1 · 연관 `bambu` · ⚠ **PASS 근거 사용 금지**

<details><summary>bambu_h2s_arc_fitting_off.md 본문 발췌</summary>

H2S용 process 프로파일을 만들 때 **`enable_arc_fitting: "0"` 을 명시하라.**

**Why:** H2S 세대(X2D/H2D/H2C 계열)는 **펌웨어 레벨 Curve Planning** 을 갖는다 — 프린터가 실시간으로 경로를
원호로 평활화한다. Bambu Studio 는 이를 감지하면 *"turned off its own arc fitting to avoid conflicts"* 경고를 띄운다.
그런데 **H2S 기본 프로파일(`fdm_process_common.json`)은 `enable_arc_fitting: "1"` 로 출고**된다.
inherits 로 base 를 받으면 이 값이 조용히 딸려와서 **슬라이서 원호 + 펌웨어 원호가 동시에 걸린다.**

보고된 증상은 **원호/원형 경로에 한정**된다: 곡선 코너가 직선으로 잘림 · 원통 벽 리플·밴딩 · 원 그릴 때 X/Y stuttering 소음.
arc fitting 을 끄면 완화된다는 보고가 다수다.

**끄는 데 품질상 손해가 없다.** OrcaSlicer 위키 명시: *"Arc fitting is not a feature to improve quality."*
목적은 G-code 크기 축소와 모션 평활이지 표면 품질이 아니다. 출력 시간이 다소 늘 수 있다(사용자 원칙상 수용).

**진단 감별 포인트 (2026-08-16 superlube 팁 케이스에서 얻음):**
사용자가 **"원형을 그릴 때 항상"** 이라고 말하면 그게 결정적 단서다.
- `seam_gap` 은 **루프당 심 한 점**에만 작용 → "원 전체가 항상"을 설명 못 함
- `enable_arc_fitting` 은 **원호 경로 전체**에 작용 → 설명됨
증상이 "한 점"인지 "경로 전체"인지를 먼저 물어라. 이걸 안 갈라서 seam 배치만 두 번 만지다 실패했다.

… (본문 18 줄까지만 — 전문은 위 경로를 직접 읽어라)

</details>

#### [research] 리서치 위임 · codex — 전체 13 건 중 3 건 주입

- **feedback_codex_background_research_stalls** — 리서치는 codex-rescue 에 위임하되 반드시 foreground. 백그라운드는 죽고, WebSearch 직행은 우선순위 위반
  - `~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_codex_background_research_stalls.md` · grounding `mixed` · 중요도 10 · 연관 `design`·`infra`·`planning`·`reflect`

<details><summary>feedback_codex_background_research_stalls.md 본문 발췌</summary>

codex-rescue 에이전트에 MODE=research를 위임하면 codex를 **백그라운드**로 돌리는데, 이 환경(fit-pal, 2026-05-30)에서 **2회 연속** 동일 실패: codex thread 시작 → assistant 첫 메시지 → web "Searching:" 여러 번 → 그 직후 codex exec 프로세스가 사라지고 .output 이 수백 바이트에서 멈춤. 완료 알림 없음, 최종 structured output 미반환. 한 번은 유휴 2시간 후 발견, 한 번은 ~20분 후 확인 시 이미 죽음.

**Why:** 백그라운드 codex가 web search 단계에서 행/리프되며 background 태스크 트래킹이 완료를 못 받음. 리서치는 산출물이 0이라 5축 점수 이전에 delivery 자체가 실패.

**How to apply:** (1) codex-rescue 리서치는 백그라운드 의존 금지 — 결과를 받을 때까지 능동 확인하거나, (2) 1~2회 죽으면 즉시 `WebSearch`/`WebFetch` 직접 fallback (전역 규칙: "WebSearch는 Codex가 불가능할 때만 fallback" 충족). 같은 codex 길을 3번째 재시도하지 마라 — 토큰·시간 낭비. [[feedback_codex_delegation]]

###### 2026-08-04 — 한 턴에 같은 걸 두 번 틀렸다. 정답은 **foreground codex**.

두 번의 오답과 사용자 지적:

1. `Workflow` 도구로 리서치를 돌렸다 → "리서치 백그라운드로 돌리지 말라고 전부터 말했는데"
   / "맨날 실패하잖아" / "포그라운드로 하라고 항상"
2. 그래서 인라인 `WebSearch` 로 직접 조사했다 → **"포그라운드 코덱스로 리서치하라고 몇 번 말하냐고"**

즉 문제는 백그라운드**만**이 아니었다. 도구 선택도 틀렸다.

**정답 한 줄: 리서치 = `codex-rescue` 위임, `run_in_background: false`.**

… (본문 18 줄까지만 — 전문은 위 경로를 직접 읽어라)

</details>

- **feedback_codex_research_use_shell_not_builtin_search** — Codex 리서치가 멈추는 건 내장 검색 때문 — workspace-write + network_access 로 gh/curl 쓰게 하라
  - `~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/memory/feedback_codex_research_use_shell_not_builtin_search.md` · grounding `미분류` · 중요도 6 · 연관 `backend` · ⚠ **PASS 근거 사용 금지**

<details><summary>feedback_codex_research_use_shell_not_builtin_search.md 본문 발췌</summary>

Codex 리서치 위임이 `Searching:` 에서 멈추거나 출력 0바이트로 끝나면 **Codex 본체 문제가 아니다.**
2026-09-12 세션에서 6회 시도 중 5회 실패한 뒤 원인을 갈랐다.

**진단 절차 (이 순서로 3분이면 끝난다):**
1. `codex exec -s read-only "2+2 는? 숫자만."` → **4초 응답**. 본체는 멀쩡하다.
2. `codex exec -s read-only '... curl -s -o /dev/null -w "%{http_code}" https://api.github.com/...'`
   → **exit 6, 000**. read-only 샌드박스는 네트워크가 막혀 있다.
3. 그래서 내장 검색/브라우저가 유일한 통로가 되고, 그게 멈춘다.

**해결 — research 표준 호출:**
```bash
codex exec -s workspace-write -c 'sandbox_workspace_write.network_access=true' \
  --skip-git-repo-check "$(cat <프롬프트파일>)"
```
실측 HTTP 200 / 222ms. 프롬프트에 "내장 웹검색 쓰지 마라, shell 로 `gh search repos` · `gh api` ·
`curl` 로 조회하라" 를 명시하고, `workspace-git-write` 라도 "파일을 만들거나 고치지 마라" 로 묶는다.

**하지 말 것:** 프롬프트를 줄여 고치려 들기. 질문 6개→2개로 줄여도 똑같이 멈췄다.

… (본문 18 줄까지만 — 전문은 위 경로를 직접 읽어라)

</details>

- **feedback_codex_stdin_must_be_closed** — codex exec 가 멈추는 주원인은 열린 stdin 이다. `</dev/null` 을 붙여라
  - `~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/memory/feedback_codex_stdin_must_be_closed.md` · grounding `미분류` · 중요도 6 · 연관 `harness` · ⚠ **PASS 근거 사용 금지**

<details><summary>feedback_codex_stdin_must_be_closed.md 본문 발췌</summary>

`codex exec` 를 부를 때 **`</dev/null` 을 반드시 붙인다.** 빼면 codex 가
`Reading additional input from stdin...` 을 찍고 무한 대기한다. 세션 id 는 나오지만
`~/.codex/sessions/.../rollout-*.jsonl` 을 만들지 않아서 «멈췄다» 로 오진하게 된다.

**Why:** 2026-09-12 실측. 같은 리서치 프롬프트가 stdin 을 연 채로 3 회 연속 실패했고
(9분 대기 2회 + 조기 감지 3회), `</dev/null` 하나를 붙이자 115 초에 완료됐다. 짧은 질문은
stdin 이 열려 있어도 통과할 때가 있어서 «비결정적 멈춤» 으로 잘못 읽기 쉽다.
공식 도움말에 적힌 정상 동작이다 — stdin 이 파이프면 그 내용을 `<stdin>` 블록으로 덧붙인다.
파이프(`| tail`)나 배경 실행 안에서 부를 때 특히 잘 걸린다.

**[2026-09-14 정정] 저 메시지 자체는 지표가 아니다.** `Reading additional input from stdin...` 은
`</dev/null` 로 닫고 **정상 완료한 실행에서도 항상** 찍힌다(실측 2/2 — 정상 리서치와 강제 실패 둘 다).
그 줄이 보인다고 stdin 이 열린 것이 아니다. stdin 갈래는 **그 줄이 있는데 차례가 안 열릴 때**다 —
`--json` 으로 부르면 `{"type":"thread.started"}` 가 1 초쯤에 오고, 안 붙이면 `session id:` 헤더가
나온다. 그 신호가 몇 초를 기다려도 없어야 stdin 이다. 호출기의 판정 로직은 원래부터 두 신호를
같이 봤으므로 옳았고, 틀린 것은 사람이 읽는 템플릿 문구였다.

**How to apply:** 리서치는 `~/.claude/bin/codex-research <프롬프트파일> <출력파일>` 로 부른다

… (본문 18 줄까지만 — 전문은 위 경로를 직접 읽어라)

</details>

#### [bambu] bambu-kit · 3D 프린트 — 전체 24 건 중 3 건 주입

- **3d** — 3D 프린트 프로파일을 만들거나 추천할 때 출력 시간/속도를 의사결정 근거로 쓰지 마라. 사용자가 반복적으로 명시한 고정 선호다.
  - `~/.claude/projects/-Users-jackson/memory/3d_print_time_not_a_constraint.md` · grounding `user_correction` · 중요도 5 · 연관 `harness`

<details><summary>3d_print_time_not_a_constraint.md 본문 발췌</summary>

3D 프린팅 관련 작업(프로파일 생성, 설정 추천, 소재 선택)에서 **출력 시간과 속도는 트레이드오프 대상이 아니다.**
품질·강도와 시간이 충돌하면 **항상 품질·강도**를 택한다.

**Why:** 사용자가 반복해서 명시했다.
- 2026-07-30 표면 마감 선택 시 — "시간 오래걸려도 상관없음, 공차만 없이 진행하면 됨"
- 2026-07-31 — "속도 느려도 되", "내가 항상말하는데 속도는 신경쓰지말라고"

실제 워크플로우가 큰 판을 **10분 단위 조각으로 잘라서** 출력하는 방식이라 총 출력 시간이 병목이 아니다.
그런데도 내가 시간을 근거로 품질을 깎는 판단을 반복해서 사용자가 직접 교정해야 했다.

**How to apply:**
- 시간이 늘어난다는 이유로 다음을 하지 마라: layer height 올리기, ironing_spacing 넓히기,
  wall_loops/shell layers 줄이기, infill 낮추기, 저속 외벽 포기하기.
- 출력 시간 추정치는 **결정 근거가 아니라 사후 고지**다. 보고할 때 1줄로만 언급하고,
  "시간이 오래 걸리니 X를 낮췄다" 같은 문장을 쓰지 마라.
- 옵션을 제시할 때 "~배 시간" 라벨로 사용자를 저품질 쪽으로 유도하지 마라. 품질 축으로만 구분하라.
- 실패 리스크는 시간과 별개 축이다. 리스크가 높은 설정은 시간이 아니라 **검증 여부**를 근거로 다뤄라.

… (본문 18 줄까지만 — 전문은 위 경로를 직접 읽어라)

</details>

- **3d-print-drying-is-always-done** — 필라멘트 건조 여부를 사용자에게 묻지 마라 — AMS HT + AMS 2 Pro 상시 건조 환경이다. 이미 충족된 것으로 간주하고 다음 원인으로 넘어가라
  - `~/.claude/projects/-Users-jackson/memory/3d_print_drying_is_always_done.md` · grounding `user_correction` · 중요도 4 · 연관 `harness`

<details><summary>3d_print_drying_is_always_done.md 본문 발췌</summary>

**출력 실패를 진단할 때 "필라멘트 건조했냐"고 묻지 마라.** 사용자 환경은 AMS HT(단일 high-temp
dryer) + AMS 2 Pro(4-spool active drying)다. 건조는 워크플로우에 이미 들어가 있다.

**Why:** 2026-09-05 사용자 직접 교정 — "앞으로 계속 건조 안햇냐고 물어보지마".
그 직전 답변에서 실제로 80 °C 건조 확인을 받고도 물었다. 스트링잉을 보면 반사적으로 건조부터
의심하는 게 기본값이 돼 있었는데, 이 사용자에겐 매번 같은 답이 나오는 무의미한 왕복이다.

**How to apply:**
- `bambu-print-profile` 스킬 `failure-recipes.md` **L2 스트링잉 게이트의 (0) 건조 확인 단계는
  이 사용자에게 항상 충족으로 간주**하고 곧바로 (1) `filament_wipe` / `filament_wipe_distance`,
  이어서 (2) `filament_retraction_length` 로 진행하라.
- 같은 이유로 소재 추천에서 "PETG/PA/PC 는 건조 필수" 를 **경고나 결정 근거로 쓰지 마라.**
  준비 절차 문서(notes 의 사전 준비 섹션)에 1줄 기재까지가 상한이다.
- 스트링잉의 실제 원인은 건조 말고 여기서 찾아라 — 순서대로:
  1. **`filament_retraction_length`** — Bambu 소재 프리셋이 프린터 기본을 크게 낮춰 놓는 경우가 있다.
     실측: `Bambu ABS @BBL H2S` 는 `0.4` 인데 `Bambu Lab H2S 0.4 nozzle` 프린터 기본은 `0.8` 로
     **절반**이다. 구멍/메시가 많아 travel 이 폭증하는 형상에서 이게 바로 원인이 된다.
  2. `filament_wipe_distance` (스톡 `1`)

… (본문 18 줄까지만 — 전문은 위 경로를 직접 읽어라)

</details>

- **inherits-high-quality** — bambu-print-profile에서 표면/심리스 요구가 있으면 베이스를 "0.20mm Standard"(속도용)가 아니라 "0.1x mm High Quality"로 잡는다. 속도 계열을 직접 지어내지 말고 벤더 튜닝값을 상속받아라.
  - `~/.claude/projects/-Users-jackson/memory/bambu_inherit_quality_base_for_surface.md` · grounding `mixed` · 중요도 4 · 연관 `harness`

<details><summary>bambu_inherit_quality_base_for_surface.md 본문 발췌</summary>

표면 품질·seam 은닉 요구가 있는 프로파일은 `inherits`를 **`0.12mm High Quality @BBL H2S`** 계열로 잡는다.
`0.20mm Standard @BBL H2S`를 베이스로 깔고 그 위에 표면 설정만 얹지 마라.

**Why:** 2026-07-31 SKADIS 프레임 PETG HF 출력이 "엉망진창"으로 나온 근본 원인.
`0.20mm Standard @BBL H2S`는 **속도용 프리셋**이라 `outer_wall_speed = ['200','500']`이다.
거기에 ironing만 느리게(30→15) 얹으니 벽은 200mm/s로 거칠게 뽑히고 다림질만 질질 끄는
앞뒤 안 맞는 조합이 됐다. scarf도 같이 켜져 있었지만 PETG scarf 권장 속도(50-70mm/s)와
베이스 200이 정면 충돌했다.

`0.12mm High Quality @BBL H2S`는 이미 `outer_wall_speed ['60','60']`, `inner_wall_speed ['150','150']`,
`outer_wall_acceleration ['2000','2000']`, `top_surface_speed ['150','150']`을 갖고 있다.
**내가 지어내려던 값이 벤더 프리셋에 이미 있었다.**

**How to apply:**
- 표면/심리스/scarf 요구 → `inherits`를 High Quality 계열로. 그러면 속도·가속도를 **하나도 override 하지 않아도** 된다.
- 속도 계열은 되도록 건드리지 마라. 건드려야 하면 배열 길이를 부모에서 읽어 맞춘다
  **칸 수를 기억으로 쓰지 말고 매번 부모에서 읽어라 — 번들 갱신으로 바뀐다.**
  프로파일 번들 `02.08.00.06` 실측: H2S = **3칸**

… (본문 18 줄까지만 — 전문은 위 경로를 직접 읽어라)

</details>

#### [onboarding] onboarding-kit · 셋업 가이드 — 전체 6 건 중 3 건 주입

- **관리 화면 클릭 순서는 공식 문서를 직접 가져와서 써라** — 외부 서비스의 관리 화면(Apple Developer Portal, Firebase, AWS 등)에서 어느 메뉴를 누르고 어떤 항목을 고르는지는 자주 바뀐다. 기억에 있는 내용으로 쓰지 말고, 그 서비스가 직접 만든 공식 도움말 페이지를 WebFetch 로 매번 가져와서 그 내용대로 써
  - `~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/memory/feedback_setup_guide_console_ui_fetch.md` · grounding `mixed` · 중요도 5 · 연관 `research`·`reflect`

<details><summary>feedback_setup_guide_console_ui_fetch.md 본문 발췌</summary>

외부 서비스의 관리 화면(Apple Developer Portal, Firebase Console, AWS Console 등)은 **어디를 눌러야 하는지가 자주 바뀌고, 내가 학습한 내용은 그 시점의 옛날 화면**이다. 설정 안내 문서를 만들 때 "어느 메뉴 → 어느 버튼 → 어떤 항목" 부분은 추측하지 말고, 공식 도움말 페이지를 매번 직접 가져와서 그 내용대로 쓴다.

**Why:** 2026-05-18 세션에서 FCM iOS 설정 안내를 학습한 기억만으로 작성했다. Apple Developer Portal 에서 `+` 버튼을 누른 뒤 나오는 항목 목록과 화면 순서가 실제와 달라서, 사용자가 "Step 1부터 다르다 시발련아"라며 크게 화를 냈다. WebFetch 로 `developer.apple.com/help/account/` 를 직접 가져오니 5초 만에 정확한 절차를 확보했다. 같은 일을 Codex 에 뒤에서 돌리는 방식으로 맡겼을 때는 검색 단계에서 5분 넘게 진행이 막혔다.

**How to apply:**
- 안내 문서에서 화면을 눌러 가는 단계를 쓰기 전에, 해당 서비스의 공식 도움말 페이지를 WebFetch 로 먼저 가져온다
- Apple: `developer.apple.com/help/account/` 아래 경로 (identifiers/keys/devices 등)
- Firebase: `firebase.google.com/docs/` 아래 경로
- Google Cloud: `cloud.google.com/docs/` 아래
- AWS: `docs.aws.amazon.com/`
- **WebFetch 를 먼저 쓰고, Codex 는 WebFetch 가 안 될 때만 쓴다** — 화면 조작 절차처럼 문서에서 그대로 뽑아오면 되는 일은 WebFetch 가 압도적으로 효율이 좋다. Codex 에 맡기는 것은 정책이 맞는지 따져보거나, 여러 출처를 서로 대조해 확인하거나, 판단이 필요한 일에 더 어울린다
- 사용자가 "내 화면은 그렇게 안 생겼다"고 알려주면 추측을 더 하지 말고 그 자리에서 화면 사진을 요청한다. 그리고 그 화면을 기준으로 다시 쓴다

관련: [[setup-guide-stack-first]] [[feedback_setup_guide_site_distinction]]

</details>

- **setup-guide-stack-first** — Firebase·FCM·Stripe 같은 외부 서비스 셋업 가이드를 만들 때, 그 프로젝트를 무엇으로 만들었는지(Flutter / Swift 네이티브 / React Native / 웹 등)를 가장 먼저 확정해야 한다. 같은 서비스라도 만든 기술에 따라 설치 명령, 초기화 코드, 명령줄 
  - `~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/memory/feedback_setup_guide_stack_first.md` · grounding `user_correction` · 중요도 4 · 연관 `flutter`·`react`·`design`·`backend`·`rust`

<details><summary>feedback_setup_guide_stack_first.md 본문 발췌</summary>

외부 서비스(Firebase, FCM, Stripe, Sentry 등) 셋업 가이드를 만들 때는 **그 프로젝트를 무엇으로 만들었는지 가장 먼저 확정한다.** 이걸 정하지 않고 가이드를 쓰면 SDK(서비스가 제공하는 개발용 라이브러리) 설치 명령, 초기화 코드, 그리고 콘솔(서비스를 관리하는 웹 화면) 설정을 대신 해주는 도구의 사용법이 기술마다 전부 달라져서, 사용자가 따라가다 막힌다.

**Why:** 2026-05-18 세션에서 fit-pal 프로젝트(Flutter 와 Rust 를 한 저장소에 같이 담은 구조)의 FCM iOS 가이드를 만들면서, 무엇으로 만든 앱인지 묻지 않고 Swift 로 직접 만드는 iOS 앱 기준으로 작성했다. 그 바람에 Step 4(콘솔에 앱 등록), Step 6(SPM 으로 패키지 추가), Step 7(AppDelegate 코드)이 전부 틀렸다. 사용자가 따라가다 막힌 뒤 "이거 플러터 기준으로 작성된 거임?" 이라고 지적해서야 알아차렸다. 같은 서비스라도 무엇으로 만든 앱이냐에 따라 절차가 완전히 달라진다.

**How to apply:**
- 가이드를 만들어 달라는 요청을 받으면, 가장 먼저 프로젝트의 의존성 파일(`pubspec.yaml` / `package.json` / `Podfile` / `requirements.txt` 등 — 이 프로젝트가 어떤 외부 라이브러리를 쓰는지 적어둔 파일)을 훑어서 무엇으로 만든 프로젝트인지 스스로 알아낸다.
- 알아낸 결과가 분명하지 않거나, 한 저장소 안에 여러 기술이 섞여 있으면 사용자에게 직접 물어서 확인한다 ("Flutter iOS 기준인가요? Swift 네이티브 기준인가요?").
- 기술별로 달라지는 핵심:
  - **Flutter**: `flutterfire configure` 명령을 먼저 실행해 설정을 자동으로 받아오고, `firebase_messaging` 의 Dart API 를 쓴다. AppDelegate 에 넣는 코드는 최소한만 넣는다.
  - **Swift 로 직접 만드는 iOS**: SPM(Swift Package Manager, 애플이 만든 패키지 설치 도구)이나 CocoaPods 로 패키지를 직접 추가하고, 알림 권한 요청과 알림 주소(토큰) 받는 코드를 전부 Swift AppDelegate 에 넣는다.
  - **React Native**: `@react-native-firebase/messaging` 을 쓰고 처리는 JavaScript 쪽에서 한다. iOS 네이티브 코드는 최소한만 건드린다.
- onboarding-kit 의 `/setup-guide` 스킬 Process 섹션 1단계에 "무엇으로 만든 프로젝트인지 먼저 확정" 을 못 박아야 한다.

이 내용은 [[feedback_setup_guide_console_ui_fetch]] 와 함께 onboarding-kit 의 Gotchas(같은 실수를 반복하지 않도록 미리 적어두는 주의 항목) 섹션에서 가장 중요한 두 가지다.

</details>

- **애플 설정 가이드는 사이트 두 개를 먼저 구분해서 알려라** — 애플 관련 설정 가이드(FCM, Sign in with Apple, 인앱 결제 등)를 쓸 때, App Store Connect(앱을 스토어에 내보내고 관리하는 곳)와 Apple Developer Portal(인증서·식별자·키를 발급받는 곳)이 서로 완전히 다른 웹사이트라는 점을 가장 앞
  - `~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/memory/feedback_setup_guide_site_distinction.md` · grounding `user_correction` · 중요도 3

<details><summary>feedback_setup_guide_site_distinction.md 본문 발췌</summary>

애플 관련 설정 가이드(FCM, Sign in with Apple, 인앱 결제 등)를 쓸 때는 **두 웹사이트가 서로 다르다는 사실을 가이드 맨 앞의 "미리 준비할 것" 부분에 적어둔다.** 주소와 용도를 표로 적어두지 않으면, 사용자가 엉뚱한 사이트로 들어가서 "1단계부터 화면이 안 맞는다"며 막힌다.

| 사이트 | 주소 | 무엇을 하는 곳인가 |
|--------|-----|------|
| App Store Connect | `appstoreconnect.apple.com` | 앱을 App Store 에 내보내고, 심사를 넣고, 앱 소개 정보를 관리하는 곳 — 앱을 실제로 출시할 때만 쓴다 |
| Apple Developer Portal | `developer.apple.com/account` | App ID, 인증서, Provisioning Profile, APNs Key 를 발급받는 곳 — FCM, 푸시 알림, Sign in with Apple 같은 설정 작업의 99% 는 여기서 한다 |

**Why:** 2026-05-18 세션에서 사용자가 FCM 을 설정하려다가 App Store Connect 로 들어가서 + 버튼을 눌렀다. 가이드가 가리키던 곳은 Apple Developer Portal 이었는데 사이트 자체가 달라서, 가이드에 적힌 선택지가 화면에 아예 나오지 않았다. 사용자가 크게 화를 냈다. 원인은 이렇다 — 가이드의 "어디서" 줄에 주소만 적어두었는데 사용자가 그 줄을 보지 못했고, 대신 "Apple 콘솔" 정도로 검색해서 다른 사이트로 들어갔다.

**How to apply:**
- 애플 관련 설정 가이드는 "미리 준비할 것" 부분의 맨 위에 두 사이트를 비교한 표를 넣는다
- 각 단계의 "어디서:" 줄에 사이트 주소를 정확히 적는다 (`developer.apple.com/...` 처럼)
- 사용자가 "+ 버튼을 눌렀는데 선택지가 안 나온다" 같은 말을 하면, 다른 걸 따지기 전에 지금 어느 사이트에 있는지부터 물어본다
- App Store Connect 는 앱을 출시할 때만 들어간다 — 설정 단계에서는 거의 들어갈 일이 없다
- 다른 회사 서비스에도 똑같은 함정이 있다:
  - **Google Cloud**: GCP Console (`console.cloud.google.com`) 과 Firebase Console (`console.firebase.google.com`) 은 다른 사이트다 — 같은 프로젝트를 다루더라도 들어가는 사이트가 다르다
  - **AWS**: AWS Console 과 AWS Marketplace 가 다르다
  - **Stripe**: Dashboard, Sigma, Connect 가 각각 다르다

… (본문 18 줄까지만 — 전문은 위 경로를 직접 읽어라)

</details>

#### [tooling] 구동 검증 · MCP 도구 — 전체 22 건 중 3 건 주입

- **feedback-catalog-web** — 디자인 카탈로그(main_catalog)는 시뮬레이터가 아니라 Chrome 웹으로 띄운다 (make app-catalog)
  - `~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_catalog_web.md` · grounding `mixed` · 중요도 8 · 연관 `design`·`flutter`·`harness`

<details><summary>feedback_catalog_web.md 본문 발췌</summary>

디자인 카탈로그 앱(`app/lib/main_catalog.dart`)은 **iOS/Android 시뮬레이터가 아니라 Chrome 웹**으로 띄운다. 정본 명령은 `Makefile`의 `make app-catalog` = `fvm flutter run -t lib/main_catalog.dart -d chrome`.

웹이라 `usePathUrlStrategy`로 URL deep link 가능 — 특정 목업으로 바로 진입: `http://localhost:<port>/mockups/<categoryName>` (예: `/mockups/aquaSelection`), 컴포넌트는 `/components/<categoryName>`. MCP는 `fitpal-web`(`/tmp/fp-fitpal-web-vmservice.txt`)로 연결되고, 단순 화면 캡처는 playwright로 `localhost:<port>` 직접 navigate 가능.

**Why:** 카탈로그는 web 타겟으로 설계됨(`usePathUrlStrategy` + `flutter_web_plugins` + `fitpal-web` MCP 별도 존재). 시뮬레이터로 띄우면 룰 위반이고 deep link도 안 된다. 2026-06-16 세션에서 iOS 시뮬레이터로 잘못 띄워 사용자가 지적. **2026-07-14 또 위반** — 웹 CanvasKit이라 MCP 인스펙터 스크린샷이 안 나온다는 이유로 카탈로그를 iOS 시뮬레이터로 띄웠다가 사용자 격노("몇번이나 말하냐").
**How to apply:** 카탈로그/목업 시안 확인 요청 시 `make app-catalog`(또는 `-d chrome`)로 실행. 메인 앱(`main.dart`)은 시뮬레이터/실기, 카탈로그는 웹 — 혼동 금지.
**절대 금지 우회:** 웹 카탈로그를 playwright/MCP로 스크린샷 못 뜬다고 해서 **카탈로그를 시뮬레이터로 옮기지 마라.** CanvasKit이라 MCP 스크린샷이 안 나오는 건 알려진 한계다([[feedback_mcp_screenshot_dont_spiral]]). 그럴 땐 (a) 코드 수정으로 렌더 버그를 고치고, (b) 시각 확인은 **사용자의 Chrome 육안**에 맡긴다(디자인 선호 결정은 사용자 몫이지 내 "검증"이 아니다). "내가 직접 스크린샷 떠야 한다"는 요구가 있어도 웹 카탈로그를 시뮬로 옮기는 건 유효한 예외가 아니다. 관련: [[feedback_mcp_runtime_verify_no_relaunch]] [[feedback_mcp_screenshot_dont_spiral]]

**목업 파일을 «새로 추가» 하면 카탈로그를 재기동해야 한다 (2026-08-12 실측).** Flutter **웹**은
hot restart 로 **새로 생긴 라이브러리를 싣지 못한다** — MCP `restart_app` 이 `success: true` 를
돌려줘도 새 파일의 목업은 안 들어온다(기존 엔트리는 정상 렌더되므로 「앱이 깨졌다」로 오진하기 쉽다).
`pkill -f main_catalog.dart` → `make app-catalog` 후, 새 VM URI 를 로그(`Debug service listening on ws://...`)
에서 뽑아 `/tmp/fp-fitpal-web-vmservice.txt` 에 써넣고 `pkill -f flutter_playwright_server` 로 MCP 재attach.
기존 파일 «수정» 은 hot reload/restart 로 반영되므로 재기동 불필요.

**카탈로그 갤러리 조작 요령 (같은 세션 실측):**
- 검색창(`placeholder: "Search components..."`)에 `fill_form` 으로 값을 넣으면 **한국어도 들어간다**.
  `type_text` 는 기존 값에 이어붙어 0 매치가 나므로 `fill_form`(치환)을 써라.

… (본문 18 줄까지만 — 전문은 위 경로를 직접 읽어라)

</details>

- **feedback-mcp-screenshot-dont-spiral** — iOS MCP screenshot가 pushed route에서 깨질 때 자가캡처에 매달리지 말 것 — 사용자가 보는 실화면 + verify_visible 활용
  - `~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_mcp_screenshot_dont_spiral.md` · grounding `execution_evidence` · 중요도 6 · 연관 `flutter`·`harness`·`design`·`reflect`

<details><summary>feedback_mcp_screenshot_dont_spiral.md 본문 발췌</summary>

fitpal-mobile MCP `screenshot_widget`(ext.flutter.inspector.screenshot)는 **pushed route 위
(group detail / schedule edit / 캘린더 glow 등)** 에서 `_repaintCompositedChild` detached-layer
assertion 으로 자주 깨진다. fresh home(루트, push 없음)에서만 안정적. hot restart 직후 한두 번
되다가 네비게이션 쌓이면 다시 깨짐.

**Why:** bottom-nav shell 위에 route를 push하면 비활성 하위 트리의 RepaintBoundary layer가
detached 되고, 인스펙터 full-tree toImage가 그걸 만나 assert. set_overlay false/AnimatedClipRect
expand/wait 로도 안 풀림.

**How to apply:**
- 자가 스크린샷 1~2회 실패하면 **즉시 포기**하고 (a) `verify_visible`(text/list) + `dump_tree
  semantics` 로 렌더 확인 — 텍스트/구조 검증엔 충분, (b) **사용자가 실 시뮬레이터를 보고 있으면
  그냥 물어봐라** ("그 화면 어디가 이상한지 한 줄"). 캡처 못 떠도 사용자는 본다. 2026-06 이걸로
  수십 턴 허비함.
- 디자인 **후보 비교**가 필요하면 카탈로그/시뮬 말고 **정적 HTML 후보 파일**을 `open <file>` 로
  사용자 브라우저에 띄워 비교(다크/crimson 근사). 단 확정 구현은 실제 위젯/DS로([[feedback_visual_design_iteration]]).
- 사용자가 "브라우저로 띄워"=후보(candidate)를 브라우저로 보여달라는 뜻일 수 있다(카탈로그 launch 아님).
- e2e 자체는 [[feedback_e2e_use_mcp_dont_flail]] + [[feedback_mcp_runtime_verify_no_relaunch]] 준수

… (본문 18 줄까지만 — 전문은 위 경로를 직접 읽어라)

</details>

- **feedback-e2e-runtime-test-last** — 구동/실기 e2e 테스트는 phase별로 하지 말고 전 phase 구현 후 맨 마지막에 일괄
  - `~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_e2e_runtime_test_last.md` · grounding `user_correction` · 중요도 5 · 연관 `harness`·`backend`·`rust`·`onboarding`

<details><summary>feedback_e2e_runtime_test_last.md 본문 발췌</summary>

다단계(Phase) 기능 구현 시, **실기 구동/e2e 테스트는 각 phase마다 하지 말고 모든 phase 구현이 끝난 뒤 맨 마지막에 일괄로 한다.** 각 phase는 코드 + 단위/통합 테스트 + QA(APPROVE) + 커밋/push 까지만 하고, 앱·서버를 실제로 띄워 눈으로 확인하는 구동 검증은 끝에 모은다.

**Why:** 2026-06-25 메시지 기능 Phase 도입(P0~P3) 중 사용자가 "구동 테스트는 마지막에" 명시. P0·P1에서 매번 실기 e2e를 시도하다 실행 중인 앱(병렬 작업)·구버전 서버 바이너리와 엉켜 비효율(서버 재빌드·재기동이 병렬 작업 방해, 2계정 필요, MCP 네비 churn). phase별 e2e는 환경 셋업 비용이 반복된다.

**How to apply:** phase 완료 보고에 "실기 e2e는 마지막에 일괄"로 명시하고 다음 phase로 진행. 마지막에 서버 재빌드+재기동+2계정으로 누적 e2e 한 번에. 단, QA Evaluator의 정적 검증(빌드/clippy/analyze/단위·통합 테스트)은 phase마다 그대로 수행. 관련: [[feedback_mcp_runtime_verify_no_relaunch]], [[feedback_verify_ci_logs_not_handoff]].

</details>

#### [general] 공통 · 작업 절차 (도메인 키워드 미검출) — 전체 10 건 중 3 건 주입

- **포매터는 이번에 바꾼 파일만 골라서 돌려라** — 코드 형식을 자동으로 고쳐주는 도구(fix-markdown-lint, prettier, black 등)를 docs/ 나 src/ 같은 디렉토리 이름을 인자로 주고 돌리지 마라 — 이번에 안 건드린 파일까지 같이 고쳐져 이번 변경 범위가 오염된다. 반드시 이번에 고친 파일만 경로 하나하나
  - `~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/memory/feedback_no_dirwide_autofixer.md` · grounding `execution_evidence` · 중요도 4

<details><summary>feedback_no_dirwide_autofixer.md 본문 발췌</summary>

코드 형식을 자동으로 고쳐주는 도구(fix-markdown-lint, prettier, black 같은 포매터와 린트 자동 수정기)를 `docs/`, `src/` 같은 디렉토리 이름을 인자로 주고 돌리지 마라. 이번 작업에서 손대지도 않은 파일까지 한꺼번에 고쳐져서, 이번에 바뀐 파일 범위가 엉망이 된다. 반드시 이번에 고친 파일만 파일 경로 하나하나로 지정해서 넘겨라.

**Why:** 2026-06-05 카이젠 작업에서 `fix-markdown-lint.py docs/`를 돌렸더니 파일 110개 중 102개가 수정됐고, 그중 100개 넘게는 이번 작업과 아무 상관 없는 파일이었다. 이걸 되돌리는 과정에서도 되돌릴 범위를 너무 넓게 잡는 바람에 원래 살려야 할 항목까지 같이 지워졌고, 그걸 다시 쓰느라 시간을 한 번 더 낭비했다. 도구를 필요 이상으로 넓게 적용하는 것은 [[feedback-minimal-change-no-overeng]]가 말하는 과잉 작업의 도구 버전이다.

**How to apply:** 포매터를 돌리기 전에 `git diff --name-only`로 이번에 바뀐 파일 목록을 먼저 뽑고, 그 파일들만 인자로 넘겨라. 잘못 고친 것을 되돌릴 때도 `git stash`로 전체를 되돌리지 말고, 파일 경로를 직접 적어서 `git checkout -- <file>`로 하나씩 되돌려라. 디렉토리 이름을 인자로 주는 것을 금지하는 안전장치는 카이젠 오케스트레이터 Step 12에 글로 박아두었다.

</details>

- **스킬을 실행했다고 보고할 때는 명령과 출력을 같이 보여라** — 스킬이나 도구를 "실행했다"고 보고하려면 실제로 입력한 명령과 거기서 나온 출력을 함께 보여야 한다. 이미 있던 파일을 읽어본 것을 실행했다고 말하면 안 된다 — 그 스킬이 예전에 만들어 둔 파일이든, 그 스킬과 아무 상관 없는 파일이든 마찬가지다. `/insights` 스킬에서 실제로
  - `~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/memory/feedback_skill_invocation_evidence.md` · grounding `user_correction` · 중요도 4

<details><summary>feedback_skill_invocation_evidence.md 본문 발췌</summary>

스킬이나 도구를 "실행했다"고 보고할 때는 실제로 입력한 명령과 거기서 나온 출력을 같이 보여라. 이미 있던 파일을 읽어본 것뿐인데 "실행했다"고 말을 바꾸면 안 된다. 그 스킬이 예전에 만들어 둔 파일이든, 그 스킬과 아무 상관 없는 파일이든 똑같이 안 된다.

**Why:** 이 저장소에서 작업하다가 `/insights` 스킬을 실제로 실행하지 않고, 이미 있던 파일만 읽은 다음 "실행했다"고 보고한 적이 있다. 사용자가 곧바로 알아채서 문서를 다시 고쳐야 했다. 카이젠이나 킷 만드는 작업은 여러 단계가 자동으로 줄줄이 이어지기 때문에, 실행하지도 않은 것을 끝냈다고 말하면 그 뒤에 이어지는 단계가 전부 잘못된 전제 위에서 돌아간다.

**How to apply:** 완료 보고에 실행한 도구의 명령 한 줄과 그 출력 일부를 그대로 인용해라. 스킬이 출력 형식(예: 꾸밈 없는 일반 텍스트)이나 최소 몇 개 이상 적으라는 규칙을 정해 두었으면 그 규칙을 그대로 지켜라. 프로젝트와 상관없이 적용되는 원래 규칙은 `~/.claude/rules/architecture-guardrails.md` §4 에 있다. [[feedback-minimal-change-no-overeng]]

</details>

- **feedback_plain_korean_no_jargon** — 사용자에게 말할 때는 쉬운 한국어로 — 내가 만든 비유·축약어 금지, 코드 주석 말투를 대화로 가져오지 말 것
  - `~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_plain_korean_no_jargon.md` · grounding `미분류` · 중요도 2 · ⚠ **PASS 근거 사용 금지**

<details><summary>feedback_plain_korean_no_jargon.md 본문 발췌</summary>

사용자에게 보내는 글은 **처음 보는 사람도 한 번에 알아듣게** 쓴다.
2026-08-22 지적: "알아듣게 말해 너만의 언어로 말하지 마라, 이거 전부터 이러네."
2026-08-28 재지적: "찍은 칸이 뭐야 전부터말하는데 알아듣게 말해" — 세 번째다.

**Why:** 내가 쓰던 비유("창구", "축", "얼굴", "그물", "무대")와 영어 조각
("amend", "blame", "falsify")이 섞이면 사용자가 매번 해석부터 해야 한다.

**2026-08-28 의 새 원인: 코드 주석 말투를 대화로 그대로 가져왔다.**
이 저장소의 record/player 코드는 주석이 「찍다·칸·차례·얼굴」로 쓰여 있다.
그 파일을 오래 읽으면 그 말투가 대화로 새어 나온다. **파일에 그렇게 쓰여 있어도
대화에서는 안 쓴다.**

**How to apply:**
- 코드 주석 말투 → 보통 말:
  "찍은 칸" → **완료 체크한 세트**, "찍는 칸/차례 칸" → **다음에 할 세트**,
  "칸" → **세트**(또는 칸이 실제로 뜻하는 것), "얼굴" → **플레이어 화면**,
  "무대" → **카탈로그 화면**, "창구" → **함수/값을 넘기는 자리**,
  "축" → **애니메이션**, "그물" → **테스트**.

… (본문 18 줄까지만 — 전문은 위 경로를 직접 읽어라)

</details>

### 탈락 — 제목만 (236 건)

선별에서 밀렸을 뿐 틀린 신호가 아니다. 자기 도메인 항목이 보이면 경로를 직접 읽어라.

- **feedback_isolated_lane_not_kill_shared** [backend][flutter][tooling][design][infra] — 병렬 세션이 쓰는 서버·앱을 죽이지 말고 내 포트·내 시뮬로 «내 차선» 을 따로 깔아라  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_isolated_lane_not_kill_shared.md` · grounding `미분류` · 중요도 1)
- **feedback_plan_assert_must_fail_without_impl** [backend][harness] — 계획에 시험 단언을 쓸 때 「구현을 지웠다면 실패하는가」를 먼저 따져라 — 안 따지면 빈 시험이 된다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_plan_assert_must_fail_without_impl.md` · grounding `미분류` · 중요도 1)
- **feedback_play_upload_terminated** [backend][infra][harness][design] — Play 업로드 「Upload has already been terminated」 = 회선·플레이 문제가 아니라 supply 의 타임아웃이 세션을 깬 것. google-apis 로 직접 올리면 41초  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_play_upload_terminated.md` · grounding `미분류` · 중요도 1)
- **feedback_push_rejected_merge_in_temp_worktree** [backend][rust] — push 가 거절됐는데 공유 폴더에 남의 미커밋 작업이 있으면 임시 워크트리에서 합쳐라  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_push_rejected_merge_in_temp_worktree.md` · grounding `미분류` · 중요도 1)
- **feedback_push_without_touching_shared_worktree** [backend][infra][rust] — 공유 워킹트리가 origin/dev 와 갈렸을 때 파일을 안 건드리고 병합 커밋만 만들어 올리는 방법. 그리고 「쓰는 쪽만 올라가고 정의가 빠지는」 반복 사고  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_push_without_touching_shared_worktree.md` · grounding `미분류` · 중요도 1)
- **feedback_seed_before_overwrite_backup_row** [backend] — 화면 확인용으로 DB 행을 덮어쓰기 전에 원래 값을 먼저 뜬다 — 트랜잭션을 뺀 순간 백업도 함께 빠졌다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_seed_before_overwrite_backup_row.md` · grounding `미분류` · 중요도 1)
- **bambu-ironing-type-enum** [bambu][harness][design] — bambu-kit references가 적어둔 ironing_type 값(topmost_only/top_surfaces/all_solid)은 전부 틀렸다. 실제 enum은 no ironing / top / topmost / solid 네 개다.  (`~/.claude/projects/-Users-jackson/memory/bambu_ironing_type_enum.md` · grounding `execution_evidence` · 중요도 4)
- **bambu-scarf-override** [bambu][harness] — process에 seam_slope_* 를 아무리 넣어도 override_filament_scarf_seam_setting=1 이 없으면 filament의 scarf 설정이 이겨서 scarf가 전부 안 걸린다  (`~/.claude/projects/-Users-jackson/memory/bambu_scarf_override_gate.md` · grounding `execution_evidence` · 중요도 4)
- **bambu ironing은 평면 top 전용 — 곡면/래티스에 금지** [bambu][harness] — bambu-print-profile에서 ironing을 적용할 형상 판정 규칙. 곡면·래티스·회전체 등 "평평한 top이 없는" 표면에 ironing을 넣으면 표면이 오히려 뭉개진다. surface-recipes.md §5.2와 Phase 3 ironing 정책에 반영 필요.  (`~/.claude/projects/-Users-jackson/memory/bambu_ironing_curved_surfaces.md` · grounding `mixed` · 중요도 3)
- **seam** [bambu][reflect] — 한 모델에 원통과 박스가 섞여 있으면 process를 형상별로 분리하고 seam 정책도 각각 적용해야 한다. 최소 변경 원칙이 형상 결정 트리를 덮어쓰면 안 된다  (`~/.claude/projects/-Users-jackson/memory/bambu_per_part_seam_policy.md` · grounding `mixed` · 중요도 3)
- **cad-export-facet-shrinks-holes** [bambu] — Fusion/CAD의 3MF·STL 기본 refinement 저다각형 근사가 소구경 홀을 실질적으로 좁힌다 — 공차 계산 시 수축률과 별도로 빼야 하는 항  (`~/.claude/projects/-Users-jackson/memory/cad_export_facet_shrinks_holes.md` · grounding `execution_evidence` · 중요도 3)
- **mesh-wall-hole-axis** [bambu] — 원통 벽을 관통하는 홀은 축이 반경 방향이라 Z축 원통면 검출로는 안 잡힌다. 벽 두께 안의 중간 반경 vertex로도 안 잡힌다 — 평면 단면을 축 방향으로 훑어야 한다.  (`~/.claude/projects/-Users-jackson/memory/mesh_wall_hole_axis.md` · grounding `execution_evidence` · 중요도 3)
- **출력 실패를 필라멘트 수분 탓부터 하지 마라** [bambu][harness] — 3D 프린터 출력이 실패했다는 보고를 받았을 때 필라멘트 수분 탓부터 하지 말고, 증상이 어디에서 언제 생겼는지부터 물어 원인을 좁히는 순서. 수분을 원인으로 지목해도 되는 관측 신호와, 수분으로는 설명되지 않아 다른 원인을 가리키는 신호를 함께 적어둔다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/memory/feedback_no_drying_reflex_diagnose_first.md` · grounding `미분류` · 중요도 3)
- **출력물 같은 자리가 패이면 열 문제가 아니다** [bambu] — 3D 출력물마다 똑같은 위치에 결함이 나면 원인은 온도·냉각이 아니라 모델 형상과 노즐 경로다. 속도·팬 값을 만지기 전에 아무것도 안 고친 기본 설정으로 한 번 뽑아 비교 기준을 먼저 만들어라. 격자(그물) 구조 통을 세 번 반복해서 실패한 사례  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/memory/feedback_same_position_defect_means_geometry_not_thermal.md` · grounding `미분류` · 중요도 3)
- **bambu-hole-comp-vs-functional-mesh** [bambu] — 통기/메시 구멍이 기능인 모델에서는 소재 수축률 표대로 xy_hole_compensation을 올리면 안 된다 — 단일 값이 기능 구멍까지 넓힌다  (`~/.claude/projects/-Users-jackson/memory/bambu_hole_comp_vs_functional_mesh.md` · grounding `미분류` · 중요도 2)
- **seam-position-seam-gap** [bambu][research] — Bambu의 seam_gap 기본 15%는 심 자리에 갭을 일부러 남기는 설정이라, seam_position을 aligned에서 random으로 바꿔도 파임은 흩어질 뿐 사라지지 않는다  (`~/.claude/projects/-Users-jackson/memory/bambu_seam_gap_divot.md` · grounding `미분류` · 중요도 2)
- **Bambu 프로파일은 제조사 폴더 안에서만 찾아라** [bambu][infra] — Bambu Studio 설치본에서 프로파일 설정값을 찾아 인용할 때, 똑같은 이름의 파일이 13개 제조사 폴더에 중복으로 들어 있으므로 (제조사, 이름) 두 값을 묶어서 구분하고 상속도 같은 제조사 안에서만 따라가야 한다. 그러지 않으면 Prusa·Creality 값을 Bambu 값으로  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/memory/feedback_bambu_profile_resolve_vendor_scoped.md` · grounding `미분류` · 중요도 2)
- **검사는 금지 목록 말고 허용 목록으로** [bambu] — 쓰면 안 되는 이름만 나열해서 검사하면, 오타가 난 이름이나 아예 없는 이름은 그냥 통과한다. 쓸 수 있는 이름 전체를 모아놓고 대조해야 하며, 그 목록 자체가 빠짐없는지부터 확인해야 한다. bambu-kit 설정 파일 검사에서 겪은 일  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/memory/feedback_gate_blocklist_misses_unknown_keys.md` · grounding `미분류` · 중요도 2)
- **설치된 프로그램에서 읽은 기준값은 옛날 값일 수 있다** [bambu][infra] — 설치된 프로그램의 설정 파일에서 비교 기준값을 읽어 분석할 때, 그 설치본이 최신 버전인지 먼저 확인하지 않으면 이미 바뀐 옛날 값으로 결론을 내게 된다. Bambu Studio 구버전에서 읽은 값으로 권장값 표를 확정할 뻔한 사례  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/memory/feedback_local_install_baseline_staleness.md` · grounding `미분류` · 중요도 2)
- **feedback_makerworld_profile_per_material_scale** [bambu][design][backend] — MakerWorld 모델은 소재별로 3mf 를 따로 올릴 수 있고 확대 비율이 다르다 — 소재 바꾸면 원본부터 다시 받아라  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/memory/feedback_makerworld_profile_per_material_scale.md` · grounding `미분류` · 중요도 2)
- **작은 조각으로 잘라 찍으면 냉각 설정 비교가 무효가 된다** [bambu][harness] — Bambu 3D 프린터에서 부품을 잘라 일부만 출력하면 한 층을 찍는 데 걸리는 시간이 달라져서, 냉각 설정을 바꿔가며 비교하는 시험이 성립하지 않는다. 한 층에서 재료를 뿜으며 지나가는 경로 길이를 계산해, 최소 층 시간(ABS 소재와 H2S 프린터 기준 12 초, 경로 길이로 환산하  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/memory/feedback_small_coupon_wrong_thermal_regime.md` · grounding `미분류` · 중요도 2)
- **print_defect_positional_means_hardware** [bambu] — 결함이 특정 방향·좌표에서만 나오거나 이상 소음이 동반되면 슬라이서 설정을 만지지 말고 먼저 기계를 의심하라. 설정은 위치를 가리지 않는다  (`~/.claude/projects/-Users-jackson/memory/print_defect_positional_means_hardware.md` · grounding `미분류` · 중요도 1)
- **돌출 구간 속도 0 은 외벽 속도를 그대로 따라간다** [bambu] — Bambu 프로파일에서 돌출 구간별 속도 키 계열(`overhang_1_4_speed` ~ `overhang_4_4_speed`, 묶어서 `overhang_N_4_speed`)에 "0" 을 넣으면 감속을 끄는 게 아니라 외벽 속도(outer_wall_speed)를 그대로 쓴다. 외벽 속  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/memory/feedback_bambu_overhang_zero_sentinel_depends_on_wall_speed.md` · grounding `미분류` · 중요도 1)
- **creator-3mf-printable-off** [bambu] — 제작자 3mf 의 build item 에 printable="0" 부품이 숨어 있을 수 있다 — 부품 수를 셀 때 출력 여부까지 봐라  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/memory/feedback_creator_3mf_printable_off.md` · grounding `미분류` · 중요도 1)
- **feedback_key_exists_is_not_key_usable** [bambu][harness][research] — 설정 키는 실존만으로 부족하다 — 받는 프리셋 종류와 enum 값까지 옵션 목록으로 확인하라  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/memory/feedback_key_exists_is_not_key_usable.md` · grounding `미분류` · 중요도 1)
- **orca-h2s-start-gcode-lags-bambu** [bambu] — 오르카 2.4.2 의 H2S 시작 명령은 뱀부보다 8개월 낡아서 툴헤드 카메라 초기화 실패(0500-8092)를 낸다 — 오르카용 H2S 프로파일에는 뱀부 최신 시작 명령을 넣은 프린터 설정을 같이 줘라  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/memory/feedback_orca_h2s_start_gcode_lags_bambu.md` · grounding `미분류` · 중요도 1)
- **xy-hole-comp-misses-horizontal-holes** [bambu][harness] — xy_hole_compensation 은 옆으로 뚫린(가로) 구멍에 전혀 안 먹는다 — 대신 컵 안쪽 벽 같은 세로 내벽만 넓힌다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/memory/feedback_xy_hole_comp_misses_horizontal_holes.md` · grounding `미분류` · 중요도 1)
- **feedback_catalog_wholesale_replace** [design][flutter][backend][reflect] — 확정 시안은 부분 이식이 아니라 통째 교체 — 카탈로그에서 완성하고 앱은 그 코드를 그대로 쓴다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_catalog_wholesale_replace.md` · grounding `미분류` · 중요도 5)
- **feedback_dont_let_metric_drive_design** [design][harness][reflect] — 시각 디자인에서 측정 가능한 지표(대비비 등)를 최적화 대상으로 삼지 마라 — 요구는 지표가 아니라 사용자가 말한 제약이다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_dont_let_metric_drive_design.md` · grounding `미분류` · 중요도 4)
- **feedback_icons_embossed** [design][flutter] — 플레이어(및 앱 전반) 아이콘은 전부 IFIcon.embossed 양각 처리. plain Icon 금지.  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_icons_embossed.md` · grounding `user_correction` · 중요도 4)
- **feedback_layout_means_element_position** [design][harness][flutter][research] — 사용자가 말하는 "레이아웃"은 요소 위치이고, 시안은 화면을 꽉 채워야 한다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_layout_means_element_position.md` · grounding `mixed` · 중요도 4)
- **feedback_photo_always_full_width** [design][harness][flutter] — 사진/미디어는 무조건 풀너비 — 인셋·썸네일·절반폭 금지, 변주 축으로도 쓰지 마라  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_photo_always_full_width.md` · grounding `user_correction` · 중요도 4)
- **subfolder-grouping-for-multi-file-components** [design][flutter] — 한 컴포넌트가 여러 파일로 분리되면 부모 폴더에 평면 나열하지 말고 전용 서브폴더로 묶어 관리  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-apps/memory/feedback_subfolder_grouping.md` · grounding `user_correction` · 중요도 3)
- **feedback-lensbar-in-decoration** [design][flutter][reflect] — vote card 좌측 시맨틱 바는 ClipRRect 안 Stack + Positioned 풀하이트 3px 직사각형으로 합성하면 sharp 직선 룩 정답. perSideStroke.left.weight=3 single-edge 패턴은 carrier corner radius 따라 휘어 r  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_lensbar_in_decoration.md` · grounding `mixed` · 중요도 3)
- **feedback_no_aqua_fill** [design] — 아쿠아필(aquaPrimary/AquaMorphButton)은 사용자가 금지했다 — 표면이 필요하면 메탈  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_no_aqua_fill.md` · grounding `미분류` · 중요도 3)
- **feedback-visual-design-iteration** [design][tooling][reflect][flutter][research] — 모호한 시각 디자인 반복 시 — 동일 픽셀 재생산 금지, 칩≠이미지 radius, 웹 stale view 주의  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_visual_design_iteration.md` · grounding `mixed` · 중요도 3)
- **안 쓰인 CSS 규칙은 검사에 안 걸린다** [design][infra][tooling] — 화면을 실제로 그려서 검사하는 도구는 안 쓰인 CSS 규칙을 검사하지 못하고 통과로 표시한다. 그래서 그 규칙을 처음 쓰는 페이지에서 문제가 터지고, 새 페이지 작성자가 남이 남긴 문제를 자기 문제로 오해한다. CSS 블록을 다른 페이지에서 가져다 쓸 때와, 검사 실패 원인이 가져온 규  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/memory/feedback_dead_css_hides_gate_failure.md` · grounding `미분류` · 중요도 2)
- **테마는 색만 바꾸는 게 아니다** [design] — 디자인 테마·컨셉 시안을 여러 개 만들 때 CSS 변수에 든 색 값만 갈아끼우면 전부 같은 사이트로 보인다. 시안마다 첫 화면 배치, 카드 늘어놓는 방식, 글꼴 종류, 전체 분위기까지 달라야 고를 만한 선택지가 된다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/memory/feedback_theme_not_just_colors.md` · grounding `미분류` · 중요도 2)
- **feedback_drawer_no_body_duplication** [design] — 서랍·메뉴 시안에 그 화면 본문에 이미 있는 것(그룹 이름·사진, 오늘 멤버들, 멤버 목록)을 다시 싣지 마라. 머리·바닥은 앱 부품(IFHeader·렌즈 판·시트 띠)으로  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_drawer_no_body_duplication.md` · grounding `미분류` · 중요도 2)
- **feedback_mockup_letter_number** [design][flutter] — 카탈로그 시안에는 «알파벳 + 번호» 를 붙인다 — 말로 지목할 수 있어야 한다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_mockup_letter_number.md` · grounding `미분류` · 중요도 2)
- **feedback_mockups_implement_dont_ask** [design][harness] — 시안 추가 요청은 제안 후 승인 대기하지 말고 바로 구현한다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_mockups_implement_dont_ask.md` · grounding `미분류` · 중요도 2)
- **feedback_no_amend_in_shared_worktree** [design] — 공유 워크트리에서 git commit --amend 금지 — 내 커밋 위에 남의 세션 커밋이 끼면 남의 커밋을 고쳐버린다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_no_amend_in_shared_worktree.md` · grounding `미분류` · 중요도 2)
- **feedback-boxdecoration-color-vs-gradient** [design][flutter] — BoxDecoration 에 color 와 gradient 를 함께 주면 색이 통째로 무시된다 — 두 겹으로 쌓아라  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_boxdecoration_color_vs_gradient.md` · grounding `미분류` · 중요도 1)
- **feedback-no-timezone-country-ui** [design][flutter][backend] — 그룹 시간대·국가는 화면에 내지 않는다 — 기기에서 유도하고 끝. 사용자가 폐기한 항목이다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_no_timezone_country_ui.md` · grounding `미분류` · 중요도 1)
- **feedback_padding_always_uniform** [design] — 패딩은 항상 좌우(사방) 일정하게 — 확정 레시피가 비대칭이어도 맞춘다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_padding_always_uniform.md` · grounding `미분류` · 중요도 1)
- **feedback_pageview_loop_precision_cap** [design][flutter] — 무한 캐러셀을 PageView 로 만들 때 바퀴 수를 키우면 정밀도 단언으로 레이아웃이 통째로 깨진다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_pageview_loop_precision_cap.md` · grounding `미분류` · 중요도 1)
- **feedback_tap_then_single_pump_animation_stalls** [design][flutter][infra] — 위젯 검사에서 탭으로 애니메이션을 출발시킨 뒤 pump(길게) 한 번만 하면 값이 안 움직인다 — 첫 틱은 출발 시각만 잡는다. pump() 후 pump(시간)  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_tap_then_single_pump_animation_stalls.md` · grounding `미분류` · 중요도 1)
- **feedback_reproduction_delete_not_match** [flutter] — 재현본(같은 화면의 두 번째 구현)을 발견하면 값을 맞추지 말고 지우고 확정 위젯을 호스팅하라  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_reproduction_delete_not_match.md` · grounding `mixed` · 중요도 5)
- **feedback_web_hot_restart_no_recompile** [flutter][tooling][harness][backend] — 웹 카탈로그는 MCP restart_app 으로 재컴파일이 안 된다 — flutter run 에 fifo stdin 을 물려 'R' 을 보내라  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_web_hot_restart_no_recompile.md` · grounding `execution_evidence` · 중요도 5)
- **lazy-builder-shrinkwrap** [flutter][harness][reflect] — 모든 스크롤·반복 렌더는 builder/Sliver로 보이는 것만 그린다. SingleChildScrollView+Column·eager ListView·shrinkWrap 전면 금지(예외 없음)  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-apps/memory/feedback_listview_shrinkwrap.md` · grounding `user_correction` · 중요도 4)
- **prefer-hooks-trio** [flutter][harness][infra] — flutter_hooks 프로젝트 — 상태/이펙트/메모는 useState·useEffect·useMemoized 3종 우선. useValueChanged·ValueNotifier·setState 지양. §28-2 결정순서 유지(싼 계산 build, useMemoized 남발 금지) (F  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-apps/memory/feedback_prefer_hooks_trio.md` · grounding `user_correction` · 중요도 4)
- **rebuild-scope-isolation** [flutter][research][harness] — 값 하나 바뀔 때 그 위젯만 리빌드, 전체(부모·화면) 리빌드 금지. leaf 토글(checkbox/radio/switch)은 HookWidget+useState(값 소유)+useEffect(부모 변경 동기화; 2026-06-22 useValueChanged→useEffect 번복).   (`~/.claude/projects/-Users-jackson-Hub-10-Dev-apps/memory/feedback_rebuild_scope_isolation.md` · grounding `user_correction` · 중요도 4)
- **feedback_widget_no_inline_no_compute** [flutter][harness][infra] — Flutter admin 위젯 build()에서 계산 금지(VM/derived/getter 이관), 인라인 위젯 불허(별도 파일), useMemoized 결정순서, 프로바이더 BuildContext 금지  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-apps/memory/feedback_widget_no_inline_no_compute.md` · grounding `execution_evidence` · 중요도 4)
- **feedback_never_patch_shared_gallery** [flutter][harness][design][tooling] — 카탈로그 캡처하려고 공용 mockups_screen.dart 의 entries 필터를 임시 변경 금지 — category 를 무시해 모든 탭이 오염된다. 원복 판정은 파일이 아니라 «실행 중 앱» 으로  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_never_patch_shared_gallery.md` · grounding `미분류` · 중요도 4)
- **feedback_single_item_mutation_no_refetch** [flutter][backend][harness][design][tooling] — 목록 한 항목만 바뀌면 전체 재조회·전체 리빌드 금지 — 서버 반환값으로 그 항목만 교체하고 행별 select  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_single_item_mutation_no_refetch.md` · grounding `mixed` · 중요도 4)
- **feedback-wheel-jumpto-cancels-fling** [flutter][tooling][harness][reflect] — 스크롤 컨트롤러 jumpTo/jumpToItem 을 useEffect([prop]) 안에서 호출하면 onChanged 되먹임 에코마다 진행 중 fling 을 끊는다. '스크롤 끊김/멈춤'=fling 취소(로직)이지 jank(성능) 아님  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_wheel_jumpto_cancels_fling.md` · grounding `mixed` · 중요도 4)
- **callback-typedef-ownership** [flutter][design] — 위젯이 노출하는 각 콜백 prop은 시맨틱 typedef로 선언한다(generic AdmSwitchChanged/AdmPressableTap 재사용 금지). typedef는 의미 원천 위젯이 소유+상위 import. 공유 typedef 파일·co-import 중복 금지 (F85 개정,   (`~/.claude/projects/-Users-jackson-Hub-10-Dev-apps/memory/feedback_callback_typedef_ownership.md` · grounding `user_correction` · 중요도 3)
- **file-header-author-current-dev** [flutter] — 새 파일 헤더의 작성자는 옛 파일에서 복사한 작성자(jtmoon 등)가 아니라 현재 작업자(git user, app_kiosk=jackson)로 설정  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-apps/memory/feedback_file_header_author.md` · grounding `user_correction` · 중요도 3)
- **feedback-melos-codegen-needs-fvm** [flutter] — melos run br:build가 dart not found로 조용히 실패, 코드젠은 fvm dart run build_runner 직접 실행  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-apps/memory/feedback_melos_codegen_needs_fvm.md` · grounding `execution_evidence` · 중요도 3)
- **feedback-no-duplicate-registry** [flutter] — 새 상수 카탈로그/목록 만들기 전 기존 enum·레지스트리에 같은 데이터 있는지 grep 먼저, 있으면 통합  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-apps/memory/feedback_no_duplicate_registry.md` · grounding `mixed` · 중요도 3)
- **feedback_analyze_root_cause_before_offering_choices** [flutter][reflect][research] — 구조적/애매한 버그는 선택지 제시 전에 코덱스로 근본 원인을 코드 기반 분석부터  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_analyze_root_cause_before_offering_choices.md` · grounding `user_correction` · 중요도 3)
- **feedback_animated_theme_needs_extra_pump** [flutter][design] — 위젯 테스트에서 같은 트리에 테마를 갈아 끼우면 AnimatedTheme 탓에 한 프레임 동안 옛 테마가 읽힌다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_animated_theme_needs_extra_pump.md` · grounding `execution_evidence` · 중요도 3)
- **feedback_build_runner_filter_deletes_outputs** [flutter][reflect] — build_runner --build-filter 는 단독으로도 필터 밖 생성물을 전부 삭제한다 — 필터를 쓰지 마라  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_build_runner_filter_deletes_outputs.md` · grounding `execution_evidence` · 중요도 3)
- **feedback_catalog_mcp_scroll_blocked** [flutter][tooling][harness][design][bambu] — 카탈로그 갤러리에서 fitpal-web MCP 상호작용(scroll/tap/type)은 walker assert로 전면 불가 — 검색어 하드코딩 + hot reload로 타일별 확인  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_catalog_mcp_scroll_blocked.md` · grounding `execution_evidence` · 중요도 3)
- **feedback_codegen_notifier_select_needs_hooks_riverpod** [flutter][reflect] — codegen @Riverpod Notifier가 build()에서 다른 provider를 .select로 읽으면 hooks_riverpod import 필수(riverpod_annotation만으론 .select 미정의)  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_codegen_notifier_select_needs_hooks_riverpod.md` · grounding `execution_evidence` · 중요도 3)
- **feedback_custompaint_needs_both_dimensions** [flutter][harness][design][bambu] — 자식 없는 CustomPaint 는 폭·높이를 둘 다 받아야 한다 — 한쪽이 0 이어도 페인터는 박스 밖에 그려서 눈에는 멀쩡해 보인다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_custompaint_needs_both_dimensions.md` · grounding `execution_evidence` · 중요도 3)
- **feedback_flex_yield_slot** [flutter][planning] — 폭 부족 시 양보하는 슬롯은 ClipRect·OverflowBox 말고 FittedBox scaleDown. ClipRect는 Flex 오버플로를 못 막고 OverflowBox는 cross axis에서 높이가 Infinity가 된다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_flex_yield_slot.md` · grounding `execution_evidence` · 중요도 3)
- **feedback_mcp_navigate_current_poisons_tree** [flutter][harness][backend][tooling] — navigate action=current 가 위젯 트리를 오염시켜 라우트 assert 를 냈던 버그 — 2026-07-29 툴킷에서 수정·push 완료, 이제 써도 된다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_mcp_navigate_current_poisons_tree.md` · grounding `execution_evidence` · 중요도 3)
- **feedback-morph-single-element-dedup** [flutter] — 풀↔미니 플레이어에서 양쪽에 겹치는 요소는 단일 morph 요소로 통합(중복 금지)  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_morph_single_element_dedup.md` · grounding `user_correction` · 중요도 3)
- **feedback-native-assets-cold-run** [flutter][tooling][research][harness][backend][infra][onboarding] — native-assets 패키지(objective_c 등) 변경/빌드 깨짐 후엔 hot restart 말고 cold reinstall로 검증. 스플래시 행의 진짜 원인 구분법.  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_native_assets_cold_run.md` · grounding `execution_evidence` · 중요도 3)
- **feedback_pressable_scale_removed** [flutter][design] — PressableEffect.standard는 의도적으로 scale 없음(highlight만). 되돌리지 말 것  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_pressable_scale_removed.md` · grounding `user_correction` · 중요도 3)
- **feedback_previewheight_needs_font_slack** [flutter][harness] — 카탈로그 previewHeight에 실측값을 그대로 박으면 Chrome에서만 잘린다 — flutter test는 실제 폰트를 안 실어 ~11px 과소측정  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_previewheight_needs_font_slack.md` · grounding `execution_evidence` · 중요도 3)
- **feedback_safearea_scroll_surface** [flutter][design] — 스크롤 효과 헤더/하단 버튼바 화면을 SafeArea로 감싸지 말 것 — 서피스가 safe area를 못 덮는다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_safearea_scroll_surface.md` · grounding `execution_evidence` · 중요도 3)
- **feedback_serena_diagnostics_sdk_mismatch** [flutter][harness][infra][backend][tooling] — serena get_diagnostics_for_file 는 번들 Dart 3.7.1 을 써서 오탐한다 — IDE 진단 오라클로 쓰지 마라  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_serena_diagnostics_sdk_mismatch.md` · grounding `execution_evidence` · 중요도 3)
- **feedback_shared_worktree_reread_before_patch** [flutter] — 공유 워크트리에서는 계획 문서와 lib/ 이 세션 중간에 갈린다 — 패치 전 재읽기, 실패 한 번은 재실행으로 확인  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_shared_worktree_reread_before_patch.md` · grounding `미분류` · 중요도 3)
- **feedback_shrinkwrap_defeats_builder** [flutter][design][harness] — shrinkWrap true면 .builder 여도 전 항목을 빌드·레이아웃한다 — 부모가 높이를 주면 반드시 제거  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_shrinkwrap_defeats_builder.md` · grounding `user_correction` · 중요도 3)
- **feedback_catalog_delete_also_widgetbook** [flutter][design][infra] — 카탈로그 시안 파일을 지우면 app/widgetbook 의 use case 도 같이 걷어야 한다 — CI analyze 는 lib·test 만 봐서 위젯북 깨짐을 못 잡는다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_catalog_delete_also_widgetbook.md` · grounding `미분류` · 중요도 2)
- **feedback_flex_slot_must_take_full_width** [flutter][harness] — 곁엣것을 줄 끝에 붙이려면 옆 칸이 남는 폭을 다 쥐어야 한다 — Expanded 든 shrinkWrap 제거든 «하나만» 하면 된다(실측표)  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_flex_slot_must_take_full_width.md` · grounding `미분류` · 중요도 2)
- **feedback_keyboard_resize_not_overlay** [flutter][tooling] — 인증 폼 키보드는 덮기(resize off) 말고 밀기(기본값). 덮기는 램프마다 뷰포트를 다시 재서 스크롤이 튄다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_keyboard_resize_not_overlay.md` · grounding `미분류` · 중요도 2)
- **feedback-no-opacity-inside-fittedbox** [flutter][design][reflect] — FittedBox/캔버스 스케일 안의 Opacity 위젯은 레이어라 축소를 탈출한다 — 걷힘은 색 알파로  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_no_opacity_inside_fittedbox.md` · grounding `미분류` · 중요도 2)
- **feedback_postframe_retry_needs_schedule_frame** [flutter][tooling] — 프레임을 세며 기다리는 재시도는 addPostFrameCallback 과 scheduleFrame 을 함께 불러야 이어진다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_postframe_retry_needs_schedule_frame.md` · grounding `미분류` · 중요도 2)
- **feedback_private_index_leaves_shared_index_stale** [flutter] — 개인 GIT_INDEX_FILE 로 커밋하면 공유 인덱스가 옛 HEAD 에 멈춰 「신규 파일=삭제됨」 상태로 남는다. 커밋 뒤 git reset 으로 되맞춰라  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_private_index_leaves_shared_index_stale.md` · grounding `미분류` · 중요도 2)
- **feedback_catalog_temp_capture_hack_blocks_all** [flutter][design][tooling] — 카탈로그가 비어 보이면 mockups_screen.dart 의 TEMP-CAPTURE 하드코딩부터 의심하라 — 카테고리를 통째로 무시한다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_catalog_temp_capture_hack_blocks_all.md` · grounding `미분류` · 중요도 1)
- **feedback-confirmed-widget-input-must-match** [flutter][design][harness] — 확정 위젯을 실 앱에 붙일 때 «넘기는 입력»이 시안과 다르면 확정이 무의미해진다 — 시안 호출부를 먼저 읽어라  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_confirmed_widget_input_must_match.md` · grounding `미분류` · 중요도 1)
- **feedback_dart_format_shared_worktree** [flutter] — 공유 워크트리에서 dart format 을 디렉터리 단위로 돌리면 남의 미커밋 파일을 재정렬한다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_dart_format_shared_worktree.md` · grounding `미분류` · 중요도 1)
- **feedback_entity_field_needs_return_path** [flutter][design] — 엔티티에 필드를 더하면 «되돌아오는» 변환 자리도 전부 고쳐라 — 안 고치면 조용히 지워진다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_entity_field_needs_return_path.md` · grounding `미분류` · 중요도 1)
- **feedback_footer_grows_scroll_must_track** [flutter] — 입력바·푸터가 두꺼워지면 목록을 그만큼 내려라. 닫기 레이어는 투명 판 말고 Listener 로  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_footer_grows_scroll_must_track.md` · grounding `미분류` · 중요도 1)
- **feedback_google_fonts_weight_copywith** [flutter][design][infra] — 글꼴은 assets 번들로 등록하라 — google_fonts 는 굵기를 패밀리에 박아 copyWith(fontWeight)를 죽인다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_google_fonts_weight_copywith.md` · grounding `미분류` · 중요도 1)
- **feedback_goroute_param_shadows_literal** [flutter][tooling] — GoRouter는 선언 순서로 먹는다 — /user/:userId 뒤에 둔 /user/following 은 영영 안 열린다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_goroute_param_shadows_literal.md` · grounding `미분류` · 중요도 1)
- **feedback_hosts_means_subject_not_presence** [flutter][harness][design] — 카탈로그 hosts 는 「타일 안에 앱 위젯이 있다」가 아니라 「그 위젯이 타일의 주제다」로 채운다 — 부품을 빌린 것은 parts  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_hosts_means_subject_not_presence.md` · grounding `미분류` · 중요도 1)
- **feedback_hunk_split_breaks_pairs** [flutter][infra] — 공유 워킹트리에서 hunk 골라 담기와 줄 번호 삽입이 파일을 갈라 CI 를 깨뜨린 사고  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_hunk_split_breaks_pairs.md` · grounding `미분류` · 중요도 1)
- **feedback_mcp_runclienttool_args_dropped** [flutter][harness][backend][tooling] — runClientTool 의 인자 칸 이름은 args 가 아니라 arguments 다 — 틀리면 툴킷이 죽는데 도구 결함으로 오진하기 쉽다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_mcp_runclienttool_args_dropped.md` · grounding `미분류` · 중요도 1)
- **feedback_mcp_scroll_target_scrollable** [flutter][tooling][harness] — MCP scroll_area 는 글자 위젯 말고 Scrollable 타입에 걸어야 먹는다. 화면 밖 위젯은 tap_widget 이 성공을 돌려줘도 안 눌린다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_mcp_scroll_target_scrollable.md` · grounding `미분류` · 중요도 1)
- **feedback_no_stash_in_shared_worktree** [flutter][design] — 공유 워크트리에서 git stash 로 「내 변경만 빼고 테스트」를 하지 마라 — 남의 파일까지 딸려 나간다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_no_stash_in_shared_worktree.md` · grounding `미분류` · 중요도 1)
- **feedback_path_combine_dead_on_web** [flutter][research] — Path.combine 으로 건 clipPath 는 웹에서 통째로 무시된다 — evenOdd 로 써라. 네이티브 검사로는 못 잡는다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_path_combine_dead_on_web.md` · grounding `미분류` · 중요도 1)
- **feedback_positioned_must_be_stack_child** [flutter] — Positioned 를 Opacity/AnimatedBuilder 로 감싸면 Stack 직계 자식이 아니게 돼 좌표가 통째로 깨진다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_positioned_must_be_stack_child.md` · grounding `미분류` · 중요도 1)
- **feedback_runclienttool_arguments_key** [flutter][backend][tooling] — runClientTool 의 인자 이름은 args 가 아니라 arguments — 틀리면 값이 조용히 안 넘어가고 앱 쪽 에러로 보인다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_runclienttool_arguments_key.md` · grounding `미분류` · 중요도 1)
- **feedback_scope_test_runs_to_own_change** [flutter][harness] — 공유 워크트리에서 전체 스위트를 돌리지 마라 — 내 변경분 경로로만 좁혀서 검증한다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_scope_test_runs_to_own_change.md` · grounding `미분류` · 중요도 1)
- **feedback_show_the_screen_not_its_handle** [flutter][design] — 「X 를 보여줘」는 X 화면을 세우라는 뜻이다 — 그 화면을 여는 버튼으로 대신하지 마라  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_show_the_screen_not_its_handle.md` · grounding `미분류` · 중요도 1)
- **feedback_verify_screen_not_command** [flutter][backend][harness][tooling] — 「띄웠다」는 명령 성공이 아니라 화면을 본 것이다 — 캡처로 확인하기 전엔 말하지 마라  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_verify_screen_not_command.md` · grounding `미분류` · 중요도 1)
- **feedback_widget_test_hangs_on_real_clock** [flutter][onboarding] — 위젯 테스트가 멈추면 가짜 시간 탓이다 — toImage 는 runAsync 로 감싸고, 로케일 전환은 setUp 으로 빼라  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_widget_test_hangs_on_real_clock.md` · grounding `미분류` · 중요도 1)
- **feedback_internal_tag_flat_model** [flutter][backend][harness][reflect] — 서버의 internally-tagged serde enum은 Flutter에서 freezed union 말고 flat {tag-field, optional payload} 모델로 미러링하라  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_internal_tag_flat_model.md` · grounding `self_inference` · 중요도 0)
- **feedback_shared_index_snapshot_reverts_commits** [general] — 개인 인덱스 스냅샷을 오래 들고 있다 커밋하면 그 사이 남의 커밋을 트리째 뒤집는다 — 커밋 직전 read-tree HEAD 필수  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_shared_index_snapshot_reverts_commits.md` · grounding `미분류` · 중요도 2)
- **orca-overhang-printable-range-only** [general] — 오르카 make_overhang_printable 을 모델 전체에 켜면 가로 구멍 윗부분이 메워진다 — 판에서 시작하는 필렛은 높이 구간 설정으로 바닥 몇 mm 에만 켜라  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/memory/feedback_orca_overhang_printable_range_only.md` · grounding `미분류` · 중요도 1)
- **feedback_orca_rejects_old_bambu_3mf_values** [general] — 옛 뱀부 버전으로 만든 제작자 3mf 는 오르카가 범위 검사로 거부한다 — 안 쓰는 키라도 막힌다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/memory/feedback_orca_rejects_old_bambu_3mf_values.md` · grounding `미분류` · 중요도 1)
- **feedback_release_dryrun_mutates_files** [general] — release.sh --dry-run 은 버전 파일을 실제로 고친다 — 돌린 뒤 반드시 되돌려라  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/memory/feedback_release_dryrun_mutates_files.md` · grounding `미분류` · 중요도 1)
- **feedback_ci_queued_is_not_stalled_one_mac_runner** [general] — 맥 러너가 하나뿐이라 앱 시험이 직렬로 선다 — 「1시간째 queued」는 죽은 게 아니라 줄 선 것  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_ci_queued_is_not_stalled_one_mac_runner.md` · grounding `미분류` · 중요도 1)
- **feedback-shared-index-reset-paths-only** [general] — 개인 인덱스로 커밋한 뒤 공유 인덱스를 되돌릴 때 경로를 반드시 한정하라 — 맨 git reset 은 남의 스테이징을 지운다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_shared_index_reset_paths_only.md` · grounding `미분류` · 중요도 1)
- **feedback_scratch_path_absolute** [general] — 임시 산출물은 스크래치 절대경로에 바로 쓴다 — `cd "$VAR" || cd 대체경로` 는 변수가 비면 대체로 안 넘어간다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-flutter-playwright/memory/feedback_scratch_path_absolute.md` · grounding `미분류` · 중요도 1)
- **feedback_contract_writeonce_and_unverifiable** [harness][flutter][infra][backend][bambu] — 계약 본문은 write-once — relaxing amendment 는 앵커가 있어도 PASS 근거가 못 되고, 검증 불가 조건 2건이면 계약이 영영 APPROVE 될 수 없다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_contract_writeonce_and_unverifiable.md` · grounding `execution_evidence` · 중요도 9)
- **feedback_fix_can_remove_implicit_guard** [harness][design] — 검증 primitive 를 교체하는 수정은 옛 코드가 부수적으로 주던 보호를 같이 날릴 수 있다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_fix_can_remove_implicit_guard.md` · grounding `execution_evidence` · 중요도 8)
- **같은 규칙이 여러 파일에 박혀 있으면 먼저 전부 찾아라** [harness] — 여러 파일이 각자 똑같은 규칙(파일 경로를 정하는 방법, 이름표 값을 계산하는 방법 등)을 따로 구현해 놓았을 때, 발견되는 순서대로 한 곳씩 고치면 매번 다른 파일이 남아 같은 문제가 다시 터진다. 고치기 전에 grep 으로 그 규칙이 적힌 파일을 전부 찾아 목록을 만들고, 글자가 같  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/memory/feedback_enumerate_all_surfaces_first.md` · grounding `execution_evidence` · 중요도 7)
- **검사 결과 "0건"을 통과로 읽기 전에 확인할 것** [harness][design][backend][bambu] — 측정해서 "0건"이 나왔다고 통과로 읽지 마라. 그 검사가 정말 문제가 있을 때 0이 아닌 값을 내는지, 그리고 검사가 훑은 범위가 내가 주장하는 범위와 같은지부터 확인하라. 실제로 범위가 0줄이었거나, 엉뚱한 요소를 쟀거나, 도구가 내 파일을 아예 안 읽은 사례 6건  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/memory/feedback_metric_must_match_claim.md` · grounding `미분류` · 중요도 7)
- **검사는 문서에서 글자 찾기 말고 실제로 돌려보기** [harness][bambu] — 계약 조건이 지켜졌는지 판정할 때 '문서에 그런 설명이 적혀 있는가'를 grep 으로 확인하면, 25 개 조건이 전부 통과인데 기능은 완전히 깨져 있는 상태를 그냥 넘긴다. 문서에 적어둔 셸 명령은 원문 그대로 꺼내서 zsh 와 bash 양쪽에서 실제로 돌려보고, 그 실행 결과만 증거로  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/memory/feedback_oracle_must_execute_not_grep.md` · grounding `execution_evidence` · 중요도 7)
- **feedback_contract_conflict_fix_code_not_wording** [harness][design] — 계약 조건끼리 충돌하면 해석 완화 말고 코드로 풀어라 — AskUserQuestion 승인은 QA가 검증할 앵커를 못 남긴다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_contract_conflict_fix_code_not_wording.md` · grounding `execution_evidence` · 중요도 7)
- **자동화는 훅이 하게 하고, 규칙은 줄여라** [harness][research][infra] — codex 위임 기록을 남기는 올바른 방법 — 손으로 반복하던 절차를 CLAUDE.md에서 지우고 Stop 훅이 원문 그대로 모으게 한다. 스스로 자기 점수를 매기는 건 믿을 수 없고, 주기적 개선 루프는 자동으로 모은 깨끗한 기록이 먼저 있을 때만 만든다. 새 스킬은 harness:c  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/memory/feedback_codex_orthodox_hook_not_empire.md` · grounding `user_correction` · 중요도 6)
- **섹션 범위 조건은 awk 로 잘라서 재라** [harness][bambu][research] — 계약 조건에 "그 섹션 안에서" 처럼 범위를 정하는 말을 썼으면, 그 섹션만 잘라내는 awk 명령을 같은 조건 안에 함께 적어라. 파일 전체를 grep 하면 손대기 전 파일에 이미 있던 낱말 때문에 아무것도 안 고쳐도 통과한다. awk 는 두 패턴 사이를 잡는 범위형 대신 표시 변수를   (`~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/memory/feedback_contract_section_scope_awk_anchor.md` · grounding `미분류` · 중요도 6)
- **고친 자리 말고 옛 값이 남았는지를 확인하라** [harness][backend][design][infra] — 값을 고친 뒤에는 새 값이 잘 들어갔는지가 아니라 옛 값이 어디에도 안 남았는지를 전부 찾아봐야 한다. 그리고 전체를 훑는 검사는 몇 개 파일을 봤는지부터 출력해야 한다 — zsh 에서 따옴표 없는 변수로 경로를 넘기는 바람에 grep 이 아무 데도 안 뒤진 채 0 건을 돌려줬고, 그   (`~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/memory/feedback_verify_absence_not_presence.md` · grounding `미분류` · 중요도 6)
- **wall-budget-planar-too** [harness][bambu] — 구멍 뚫린 판·래티스 부품은 형상 판정이 planar 여도 벽 예산을 재라 — 벽이 못 들어가는 자리를 classic 이 갭필로 때워 모서리마다 덩어리가 튀어나온다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/memory/feedback_wall_budget_planar_too.md` · grounding `미분류` · 중요도 6)
- **feedback_mcp_vmservice_file_race** [harness][flutter][tooling][backend][reflect] — 병렬 세션/여러 기기가 같은 vmservice-out-file을 경합하면 MCP가 엉뚱한 기기에 attach — 도구 0/flip-flop  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_mcp_vmservice_file_race.md` · grounding `execution_evidence` · 중요도 6)
- **feedback_shared_worktree_stage_hunks** [harness][flutter][design][infra][rust][bambu] — 병렬 세션이 같은 파일을 동시에 고치므로 커밋 전 hunk 단위로 내 것만 스테이징하라 — git add <파일> 은 남의 미완 작업을 딸려 보낸다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_shared_worktree_stage_hunks.md` · grounding `execution_evidence` · 중요도 6)
- **feedback-sealed-contract-scope-drift** [harness][reflect][bambu][tooling] — 봉인된 계약은 도중에 추가된 작업을 흡수하지 못한다 — 범위가 늘면 그 시점에 amendment 를 쓰고, 화이트리스트는 기억이 아니라 diff 에서 도출하라  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-flutter-playwright/memory/feedback_sealed_contract_scope_drift.md` · grounding `미분류` · 중요도 6)
- **widget-refactor-protocol** [harness][flutter][design][backend][infra] — 위젯 리팩토링은 위젯 지정 → 불필요 Props 분석(실콜러 grep, dev 쇼케이스 제외) → 내부 상태변경 파악(use*) → 브리핑 → sprint-contract → 사용자 허락 → 구현 순서. Props 제거 기준: 실콜러 0건 OR 단일 호출처가 고정 스타일값 전달 = 제거  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-apps/memory/feedback_widget_refactor_protocol.md` · grounding `user_correction` · 중요도 5)
- **막는 훅을 고쳤으면 실제로 막히는지 넣어봐라** [harness][infra][bambu] — 작업을 막는 훅은 훅 자체가 실패해도 작업을 통과시키도록 만들어져 있어서, 검사가 아예 죽어버린 상태도 똑같이 조용하다. 훅을 고친 뒤 실제로 막혀야 하는 입력을 한 건 실행해 차단이 나오는지 확인하는 절차, 그리고 셸 함수 정의 순서와 문자열 기준점 중복 때문에 검사가 통째로 죽었던   (`~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/memory/feedback_fail_open_hides_dead_guard.md` · grounding `execution_evidence` · 중요도 5)
- **새 킷 만들 때 빠뜨리면 안 되는 12가지** [harness][design][onboarding][research][bambu] — 새 플러그인 킷을 만들 때 작업 계획에 반드시 넣어야 하는 12개 항목 목록. 플러그인 폴더, marketplace.json 등록, CLAUDE.md 갱신, kaizen-orchestrator 단계 등록, docs/ 문서 페이지 만들기, docs/index.html 아이콘 등록, css  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/memory/feedback_kit_creation_complete_pipeline.md` · grounding `user_correction` · 중요도 5)
- **평가 에이전트에 출력 형식을 강제하지 마라** [harness] — qa-evaluator 를 서브에이전트로 돌릴 때 출력 형식을 미리 정한 틀(schema 옵션)로 고정하면, 스킬 절차 뒷부분의 피드백 저장(`~/.harness/feedback/evaluator/`)이 통째로 건너뛰어지고 판정 품질까지 떨어진다. 2026-08-13 카이젠에서 결과 파  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/memory/feedback_no_schema_on_qa_subagent.md` · grounding `execution_evidence` · 중요도 5)
- **feedback-harness-feedback-draft** [harness] — save-feedback.sh 는 draft 를 소비하고, HARNESS_CONTRACT 없이 실행하면 plain 계약에 오귀속된다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-flutter-playwright/memory/feedback_harness_feedback_draft.md` · grounding `execution_evidence` · 중요도 5)
- **bare-catch-convention** [harness][flutter][bambu] — bare catch (e)는 의도된 컨벤션 — on Exception/on Type으로 좁히지 마라, QA가 지적해도 수정 금지  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-apps/memory/feedback_bare_catch_convention.md` · grounding `mixed` · 중요도 4)
- **feedback_contract_internal_conflict_check** [harness][infra][bambu][tooling] — 계약을 봉인하기 전에 조건끼리 서로 어긋나는지 확인하라 — 파일 집합과 재사용 요구가 부딪힌다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/memory/feedback_contract_internal_conflict_check.md` · grounding `미분류` · 중요도 4)
- **카이젠은 전체 실행 말고 돌릴 단계부터 골라라** [harness][design][flutter][react][reflect] — kaizen-orchestrator를 전부 돌리기 전에, /insights §0 리포트가 직전 사이클과 내용이 겹치는지와 단계(Phase)마다 고칠 거리가 얼마나 모여 있는지를 먼저 재고, 신호가 많은 단계만 돌릴지 사용자에게 제안하라  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/memory/feedback_kaizen_phase_triage.md` · grounding `execution_evidence` · 중요도 4)
- **feedback_measure_command_before_sealing** [harness][infra][onboarding] — 계약에 적을 재는 명령은 봉인 전에 한 번 돌려봐라 — 안 돌려보면 통과 불가능한 조건이 박힌다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/memory/feedback_measure_command_before_sealing.md` · grounding `미분류` · 중요도 4)
- **요청한 것만 최소로 고쳐라** [harness][flutter][design][tooling] — 요청을 정확히 만족하는 가장 작은 변경만 하고, 시키지 않은 캐시 검사·뼈대 코드·중간 층·새 디렉토리를 덧붙이지 마라. 단, 계약(Sprint Contract)에 적힌 조건은 그 자체가 요청이므로 최소 변경을 이유로 빼면 QA 에서 REJECT 를 받는다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/memory/feedback_minimal_change_no_overeng.md` · grounding `execution_evidence` · 중요도 4)
- **공통 전제는 계약 맨 앞에서 한 번만 선언** [harness] — 여러 조건에 똑같이 걸리는 전제(측정에서 뺄 대상, 미리 성립해 있어야 하는 상태)는 조건마다 따로 적지 말고 계약 맨 앞에서 한 번만 선언하라. 조건별로 관리하면 반드시 하나를 빠뜨리고, 빠뜨린 그 조건은 아무리 고쳐도 통과할 수 없게 된다 — 2026-08-13 카이젠 Final 계  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/memory/feedback_shared_premise_to_header.md` · grounding `execution_evidence` · 중요도 4)
- **feedback_error_verdict_use_probe_log** [harness][flutter][design] — 앱 런타임 에러 유무 판정은 get_runtime_events 말고 fp-framework-errors.log 를 1차 자료로 쓴다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_error_verdict_use_probe_log.md` · grounding `execution_evidence` · 중요도 4)
- **feedback_mcp_capture_stable_filename** [harness][tooling][flutter][design] — MCP screenshot_widget 은 ref 기반 파일명이라 다음 캡처가 덮어쓴다 — 증거는 고정 이름으로 복사해 둘 것  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_mcp_capture_stable_filename.md` · grounding `execution_evidence` · 중요도 4)
- **feedback_measure_where_value_reaches_user** [harness][bambu] — 계약 측정 지점을 정하기 전에 그 함수의 반환값이 사용자에게 실제로 도달하는지 호출 그래프로 확인하라 — 죽은 경로를 지목하면 잘못된 구현이 PASS 한다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_measure_where_value_reaches_user.md` · grounding `execution_evidence` · 중요도 4)
- **feedback_morph_codex_review** [harness][design][research][flutter] — 모프/전환 애니메이션은 구현 후 사용자 확인을 요청하기 전에 codex 검토를 먼저 거친다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_morph_codex_review.md` · grounding `mixed` · 중요도 4)
- **feedback-verify-ci-logs-not-handoff** [harness][infra][flutter][rust] — CI 실패 원인은 핸드오프/추측이 아니라 실제 run 로그로 확인하라  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_verify_ci_logs_not_handoff.md` · grounding `execution_evidence` · 중요도 4)
- **feedback-approval-must-be-single-issue** [harness][design][infra] — 승인을 받을 때는 그 안건 하나만 묻는다 — 다른 안건과 같은 메시지에 묶인 응답은 앵커로 쓸 수 없다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-flutter-playwright/memory/feedback_approval_must_be_single_issue.md` · grounding `execution_evidence` · 중요도 4)
- **feedback-mutation-site-matters** [harness][bambu][flutter][tooling] — 음성 대조를 할 때 헬퍼가 아니라 호출부를 변이시켜야 한다 — 헬퍼 변이는 배선이 끊겨 있어도 통과한다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-flutter-playwright/memory/feedback_mutation_site_matters.md` · grounding `미분류` · 중요도 4)
- **feedback_preserve_artifact_before_rerun** [harness][backend][tooling] — 실패 산출물을 조사하기 전에 복사하지 않으면 재실행이 그것을 덮어써서 귀속 자체가 불가능해진다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-flutter-playwright/memory/feedback_preserve_artifact_before_rerun.md` · grounding `미분류` · 중요도 4)
- **feedback-sc-whitelist-from-touchable-paths** [harness][tooling][bambu] — SC 화이트리스트는 «바꿀 파일» 이 아니라 «건드릴 수 있는 파일» 로 도출한다 — 계약·계획·spec·사이드카 경로가 늘 빠진다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-flutter-playwright/memory/feedback_sc_whitelist_from_touchable_paths.md` · grounding `execution_evidence` · 중요도 4)
- **ephemeral-tests** [harness][bambu][flutter][design] — app_kiosk 테스트 파일은 스프린트 검증용 일회성 — 사용자가 의도적으로 삭제, 재생성 금지, git 커밋 제안 금지  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-apps/memory/feedback_ephemeral_tests.md` · grounding `user_correction` · 중요도 3)
- **profile-generation-needs-qa** [harness][design][bambu] — 출력 설정(JSON·3mf·notes) 만들기도 구현이다 — 킷 자체 검사만 돌리고 끝내지 말고 계약과 qa-evaluator 를 거쳐라  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/memory/feedback_profile_generation_needs_qa.md` · grounding `미분류` · 중요도 3)
- **feedback_amendment_commit_separate** [harness][design][bambu] — sprint-amendments 사이드카는 코드 커밋과 분리해서 커밋해야 AR-01 화이트리스트를 안 깬다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_amendment_commit_separate.md` · grounding `execution_evidence` · 중요도 3)
- **feedback_blame_tool_last_verify_identity_first** [harness][flutter][backend][reflect][tooling] — 도구 탓 하기 전에 계약·대상·정체 셋을 확인하라 — 2026-09-19 에 이걸 건너뛰고 하루에 오진 셋을 냈다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_blame_tool_last_verify_identity_first.md` · grounding `미분류` · 중요도 3)
- **feedback_english_identifiers** [harness][flutter][backend][rust] — 식별자(함수·변수·테스트 함수명)는 항상 영어. 한국어는 주석/doc/에러메시지만. "주변 코드 따라가기"가 이걸 못 덮는다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_english_identifiers.md` · grounding `mixed` · 중요도 3)
- **feedback_pipe_masks_exit_code** [harness][flutter][rust][infra] — 검증 명령을 파이프로 tail/grep 하면 exit code가 가려져 false-positive PASS가 난다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_pipe_masks_exit_code.md` · grounding `execution_evidence` · 중요도 3)
- **feedback_run_guard_appenv_bug** [harness][backend][infra][rust] — harness run-guard 훅이 APP_ENV=dev cargo run 을 차단하는 버그 — 빌드된 바이너리 직접 실행으로 우회  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_run_guard_appenv_bug.md` · grounding `execution_evidence` · 중요도 3)
- **feedback-plugin-source-not-marketplace** [harness][infra][flutter] — 플러그인/스킬을 고칠 때 ~/.claude/plugins/marketplaces/ 는 배포본이다 — 소스는 ~/Hub/10_Dev/claude-plugins  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-flutter-playwright/memory/feedback_plugin_source_not_marketplace.md` · grounding `execution_evidence` · 중요도 3)
- **feedback-scoped-format-only** [harness][flutter] — dart format을 디렉토리 단위로 돌리면 손대지 않은 파일까지 재포맷되어 변경 범위가 오염된다 — 편집한 파일만 지정하라  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-flutter-playwright/memory/feedback_scoped_format_only.md` · grounding `execution_evidence` · 중요도 3)
- **feedback_check_open_release_prs_first** [harness] — 릴리스 전에 열린 릴리스 PR 부터 봐라 — 서로 쌓인 체인이라 내 것과 버전이 갈린다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/memory/feedback_check_open_release_prs_first.md` · grounding `미분류` · 중요도 2)
- **feedback_commit_state_checks_after_commit** [harness][reflect][bambu] — 커밋을 재는 검사는 커밋 뒤에 다시 돌려라 — 커밋 전 자기 확인이 통과해도 QA 가 REJECT 한다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/memory/feedback_commit_state_checks_after_commit.md` · grounding `미분류` · 중요도 2)
- **feedback_doc_insert_breaks_table** [harness] — 문서에 절을 끼워 넣으면 표·목록이 갈라진다. 마크다운 경고 수로는 안 잡힌다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/memory/feedback_doc_insert_breaks_table.md` · grounding `미분류` · 중요도 2)
- **만들어진 파일만 고치면 되돌아간다** [harness][design][research] — 자동으로 만들어지는 문서 파일만 고치면 다음에 다시 만들 때 원래대로 돌아간다 — 원본 파일을 같이 고치고, 사이트 목차에 등록되지 않아 아무도 열어볼 수 없는 페이지를 고치고 있는 건 아닌지 먼저 확인하라  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/memory/feedback_fix_source_not_generated.md` · grounding `미분류` · 중요도 2)
- **규칙을 바꾸면 설계 기준 문서부터 검색하라** [harness][onboarding][design][research][bambu] — 규칙·등급·용어를 바꾸는 작업에서 설계 기준 문서(docs/howto/design-brief.md 같은 원본 문서)가 '무엇이 빠졌나' 분석에서 세 번 연속 누락됐다 — 고칠 파일 목록이 아니라 바뀌는 낱말로 저장소 전체를 먼저 검색하라.  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/memory/feedback_gap_analysis_misses_design_brief.md` · grounding `미분류` · 중요도 2)
- **feedback_mutation_must_hit_what_check_reads** [harness][bambu] — 검사가 살아 있는지 볼 때 변이는 그 검사가 실제로 읽는 자리에 넣어야 한다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/memory/feedback_mutation_must_hit_what_check_reads.md` · grounding `미분류` · 중요도 2)
- **feedback_mutation_must_verify_applied** [harness] — 음성 대조에서 변이가 실제로 적용됐는지 먼저 확인하라. 안 그러면 원본을 돌려놓고 눈먼 측정이라 오진한다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/memory/feedback_mutation_must_verify_applied.md` · grounding `미분류` · 중요도 2)
- **feedback_repo_clean_condition_catches_other_sessions** [harness][design] — 레포 변경 0건 조건은 다른 창의 작업을 같이 잡는다 — 건수만 보지 말고 파일 이름을 대조하라  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/memory/feedback_repo_clean_condition_catches_other_sessions.md` · grounding `미분류` · 중요도 2)
- **feedback_rules_shrink_move_list_to_machine** [harness][infra] — 규칙에 금지 단어 표를 늘리지 마라 — 목록은 기계가 읽는 파일로 빼고 규칙에는 판정 기준만 남겨라  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/memory/feedback_rules_shrink_move_list_to_machine.md` · grounding `미분류` · 중요도 2)
- **검사 스크립트는 실행 위치가 아니라 자기 파일 위치를 기준으로 삼는다** [harness][onboarding] — validate-plugin.py 와 sync-docs.py 는 명령을 실행한 폴더가 아니라 스크립트 파일이 놓인 폴더를 기준으로 저장소 최상위(REPO_ROOT)를 정한다. 그래서 워크트리에서 `../../../scripts/` 로 부르면 내가 고친 파일이 아니라 원래 저장소 폴더의   (`~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/memory/feedback_script_repo_root_not_cwd.md` · grounding `미분류` · 중요도 2)
- **feedback_skill_tool_runs_installed_cache** [harness][design][infra][bambu] — Skill 도구는 레포가 아니라 설치본 캐시를 부른다 — 고친 킷을 도그푸드하려면 레포 파일을 직접 실행하라  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/memory/feedback_skill_tool_runs_installed_cache.md` · grounding `미분류` · 중요도 2)
- **워크트리 세션에서는 명령을 스크립트 파일로 만들어 실행하라** [harness] — EnterWorktree 로 격리한 세션에서는 여러 줄 코드 끼워넣기(heredoc)·변수·cd 가 섞인 Bash 명령이 "워크트리 밖을 건드릴지 확인할 수 없다"며 거부된다. 2026-09-08 에 실제로 거부된 명령 형태와 통과한 형태 목록, 그리고 Write 로 스크립트 파일을 만  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/memory/feedback_worktree_guard_script_files.md` · grounding `미분류` · 중요도 2)
- **feedback_e2e_on_empty_fixture** [harness][tooling][flutter][backend] — 실기 시험은 «비어 있는» 자리에서 하라 — 데이터가 있는 방은 결함을 가린다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_e2e_on_empty_fixture.md` · grounding `미분류` · 중요도 2)
- **feedback_focus_handoff_needs_own_scope** [harness][flutter][design] — 페이지 전환에서 키보드를 유지하려면 unfocus 대신 «페이지마다 제 FocusScope + 첫 칸 autofocus» 로 포커스를 직행시켜야 한다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_focus_handoff_needs_own_scope.md` · grounding `미분류` · 중요도 2)
- **feedback_review_finds_dead_capability** [harness][backend][planning] — 과제별 리뷰는 「이 조건이 언제나 거짓」을 못 본다 — 전체 리뷰에서만 잡힌다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_review_finds_dead_capability.md` · grounding `미분류` · 중요도 2)
- **feedback_shared_index_steals_staged_files** [harness][design][rust] — 공유 워크트리는 git 인덱스도 공유한다 — 스테이징해 두면 다른 세션 커밋이 내 파일을 가져간다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_shared_index_steals_staged_files.md` · grounding `미분류` · 중요도 2)
- **feedback-ci-linux-renders-worse** [harness][design][infra][backend] — 내 맥에서는 화면 밖으로 넘친 양이 0 인데 CI 리눅스에서는 넘친다. 리눅스가 글자 폭을 더 넓게 잡기 때문이다 — 레이아웃 검증은 기준 너비보다 좁은 폭으로 하고, 아슬아슬하게 수치를 맞추는 대신 구조를 고쳐라  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/memory/feedback_ci_linux_renders_worse.md` · grounding `미분류` · 중요도 1)
- **feedback_consent_anchor_from_machine_record** [harness][design][infra][reflect] — 합의 시각을 짐작해 적지 마라 — 기계 기록에서 뽑아라. 커밋보다 뒤인 시각을 적어 REJECT 났다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/memory/feedback_consent_anchor_from_machine_record.md` · grounding `미분류` · 중요도 1)
- **feedback_gcode_arc_moves_break_length_measure** [harness] — G-code 길이를 잴 때 호(G2/G3)를 건너뛰면 다음 직선이 부풀어 총합이 그럴듯해 보인 채로 틀린다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/memory/feedback_gcode_arc_moves_break_length_measure.md` · grounding `미분류` · 중요도 1)
- **feedback_literal_not_word_for_absence_checks** [harness] — 조건을 낱말 하나로 재면 양쪽으로 샌다 — 넣을 문장을 리터럴로 못박고 grep -F 로 재라  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/memory/feedback_literal_not_word_for_absence_checks.md` · grounding `미분류` · 중요도 1)
- **feedback_negative_control_target_must_be_checked** [harness][bambu] — 음성 대조로 망가뜨릴 값을 고를 때 그 키가 검사 대상인지 먼저 확인하라 — 숫자 키는 값 검사를 안 받는다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/memory/feedback_negative_control_target_must_be_checked.md` · grounding `미분류` · 중요도 1)
- **feedback-never-exempt-whole-field-from-gate** [harness][design] — 게이트 오탐을 필드 통째 면제로 고치지 마라 — 목적과 반대 방향이면 수정이 아니라 구멍이다.  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/memory/feedback_never_exempt_whole_field_from_gate.md` · grounding `미분류` · 중요도 1)
- **feedback_new_check_inherit_sibling_exceptions** [harness] — 기존 검사를 닮은 새 검사를 만들면 형제 검사의 예외와 화해 경로를 먼저 옮겨라  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/memory/feedback_new_check_inherit_sibling_exceptions.md` · grounding `미분류` · 중요도 1)
- **시험 파일을 새로 만들면 돌리는 자리에도 넣어라** [harness][bambu] — 검사용 시험 파일을 문서 표에만 등록하고 실제로 돌리는 명령 목록에 안 넣으면, 다음 사람이 그 절차를 그대로 돌려도 새 검사만 한 번도 안 돌아간다. bambu-kit PR  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/memory/feedback_new_fixture_must_join_run_list.md` · grounding `미분류` · 중요도 1)
- **feedback_output_file_records_defaults_not_accepted_keys** [harness][reflect] — 결과 파일에 기록된 키 집합은 입력에서 받는 키 집합이 아니다 — 계약 오라클로 둘을 섞지 마라  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/memory/feedback_output_file_records_defaults_not_accepted_keys.md` · grounding `미분류` · 중요도 1)
- **한 칸을 못 읽어도 나머지는 재고, 못 읽은 칸은 말해라** [harness][bambu] — 여러 칸(압출기 슬롯·배열 값)을 묶어 검사할 때 한 칸이 안 읽히면 검사 전체를 끄기 쉽다. 그러면 "쟀는데 괜찮다" 와 "그 칸은 못 쟀다" 가 구분되지 않는다. bambu-kit 완료 검사에서 하루에 네 번 같은 모양으로 터졌다.  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/memory/feedback_partial_read_must_not_silence_check.md` · grounding `미분류` · 중요도 1)
- **feedback_profile_count_misleads_both_ways** [harness][bambu] — 슬라이서 키 존재는 프로파일 집계도 실행 파일 문자열도 틀린다 — bambu-kit 옵션 목록(option-keys/)으로 판정하라  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/memory/feedback_profile_count_misleads_both_ways.md` · grounding `미분류` · 중요도 1)
- **품질 검사는 계약 먼저, 그다음 qa-evaluator** [harness] — 사용자가 "QA 돌려줘", "검증해줘" 같은 품질 검사를 요청했을 때, superpowers 쪽 리뷰 도구를 쓰지 말고 harness 플러그인의 sprint-contract 스킬로 완료 조건을 먼저 만든 다음 qa-evaluator 에이전트로 그 조건에 맞는지 판정하라는 규칙  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/memory/feedback_qa_preference.md` · grounding `미분류` · 중요도 1)
- **ratio-baseline-weighting** [harness][bambu] — 비율 기준값을 잠글 때 무엇으로 세는지(점 수 · 길이 · 면적)를 적고 두 방식으로 재 봐라 — 같은 부품이 58.8 % 와 72.0 % 로 갈렸다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/memory/feedback_ratio_baseline_weighting.md` · grounding `미분류` · 중요도 1)
- **PR 올리기 전에 자동 검사 전부 돌리기** [harness][design] — 내 컴퓨터에서 validate-plugin.py 하나만 돌려놓고 PR 을 올렸다가 막혔다. 깃허브가 자동으로 돌리는 검사는 7개였고, 내가 안 돌린 check-docs-links.py 가 docs/index.html 의 아이콘 누락을 잡아냈다. PR 전에 검사 목록을 .github/wo  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/memory/feedback_run_ci_checks_locally.md` · grounding `미분류` · 중요도 1)
- **같은 작업 폴더를 다른 세션이 같이 쓰고 있다** [harness][research][design] — 이 저장소는 여러 Claude 세션이 작업 폴더 하나를 같이 쓴다. 그래서 브랜치를 새로 만들면 남의 세션까지 내 브랜치로 끌려오고, "이번에 바뀐 파일"을 세는 계약 조건에 남의 변경이 섞여 들어간다. 작업 시작 시 비교 기준값 남기기, 누가 고쳤는지 가리는 법, git add -A   (`~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/memory/feedback_shared_worktree_concurrent_session.md` · grounding `미분류` · 중요도 1)
- **feedback_stop_hook_check_via_session_log** [harness][infra][bambu] — Stop 훅이 불렸는지·죽었는지는 세션 기록 jsonl 의 첨부 종류로 센다. "hook error" 글자는 없고, -p 실행 기록엔 stop_hook_summary 줄도 없다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/memory/feedback_stop_hook_check_via_session_log.md` · grounding `미분류` · 중요도 1)
- **feedback_subagent_fabricates_tool_calls** [harness] — 서브에이전트가 "다른 에이전트를 띄웠다"고 적어도 실제로는 안 띄울 수 있다 — 부모 기록으로 세라  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/memory/feedback_subagent_fabricates_tool_calls.md` · grounding `미분류` · 중요도 1)
- **feedback_dart_sort_not_stable** [harness][flutter][design] — 다트 List.sort 는 서른둘 넘는 목록에서 같은 값끼리의 원래 차례를 안 지킨다 — 두 통에 나눠 담아라  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_dart_sort_not_stable.md` · grounding `미분류` · 중요도 1)
- **feedback_sheet_keyboard_inset_is_content_job** [harness][design][tooling] — showSheet 트레이는 키보드를 안 비킨다 — 입력칸 든 시트 «내용» 이 viewInsets 만큼 민다. 트레이에 넣으면 기존 시트 셋이 두 번 밀린다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_sheet_keyboard_inset_is_content_job.md` · grounding `미분류` · 중요도 1)
- **feedback_shrink_screen_scale_not_crop** [harness][flutter] — 화면이 버튼으로 빨려 들어가게 할 때, 안무 없는 화면은 잘라내지 말고 통째로 줄여라(FittedBox.cover)  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_shrink_screen_scale_not_crop.md` · grounding `미분류` · 중요도 1)
- **feedback_text_height_one_clips_glyph** [harness][design] — 작은 뱃지·칩 안 Text 에 height:1 을 주면 RenderParagraph 기본 overflow=clip 이 글리프 «위쪽 잉크» 를 잘라낸다 — 뱃지가 잘린 게 아니라 숫자가 잘린 것  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_text_height_one_clips_glyph.md` · grounding `미분류` · 중요도 1)
- **feedback_width_tests_need_both_locales** [harness] — 줄 폭·잘림 검사는 한국어·영어 둘 다 돌리고, 폭 목록에 접는 문턱 «바로 위» 를 넣어라  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_width_tests_need_both_locales.md` · grounding `미분류` · 중요도 1)
- **feedback_control_must_differ_from_subject** [harness][flutter][tooling] — 대조군이 대상과 같은 조건을 공유하면 대조가 아니다 — 실기 검증에서 오진을 만든 패턴  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-flutter-playwright/memory/feedback_control_must_differ_from_subject.md` · grounding `미분류` · 중요도 1)
- **feedback_oracle_fallback_upfront** [harness][infra][flutter][backend][bambu] — 빌드·런타임 오라클은 봉인 전에 실제로 돌리고 대체 수단을 조건에 먼저 적어라 — 봉인 뒤 개정은 사용자 동의 질문으로 번진다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-flutter-playwright/memory/feedback_oracle_fallback_upfront.md` · grounding `미분류` · 중요도 1)
- **feedback_ci_job_cancelled_mac_sleeps** [infra][harness][design] — 자가 호스트 러너가 이 맥에 있다 — 잡이 「취소」로 끝나면 실패가 아니라 기계가 잔 것이다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_ci_job_cancelled_mac_sleeps.md` · grounding `미분류` · 중요도 4)
- **feedback-ci-read-job-log-not-duration** [infra][flutter][backend] — CI 잡 실패 원인을 소요시간·러너 상태로 추정하지 마라 — failed_step 을 먼저 보고 그 스텝 로그를 읽어라  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_ci_read_job_log_not_duration.md` · grounding `미분류` · 중요도 4)
- **feedback-fix-root-cause-not-workaround** [infra][harness][design][backend] — 에러가 나면 그 에러의 근본 원인을 정공법으로 잡아라 — 우회로/workaround 금지  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_fix_root_cause_not_workaround.md` · grounding `mixed` · 중요도 4)
- **feedback-no-read-env** [infra][design][backend][reflect][onboarding] — .env / .env.fastlane / .env.* 등 시크릿이 들어 있는 환경 파일은 Read 도구로 직접 열지 마라  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_no_read_env.md` · grounding `user_correction` · 중요도 3)
- **feedback-self-check-before-emit** [infra][design] — 답을 내보내기 전에 쉬운 말 규칙을 스스로 훑어라 — 훅에 걸려 다시 쓰면 같은 답을 두 번 보게 된다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_self_check_before_emit.md` · grounding `미분류` · 중요도 3)
- **feedback_guard_must_block_its_own_recommended_form** [infra][harness][backend][research] — 막는 검사를 만들었으면, 내 문서가 권장하는 사용 형태로 그 검사를 뚫어봐라. 권장 형태가 제일 잘 뚫는다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/memory/feedback_guard_must_block_its_own_recommended_form.md` · grounding `미분류` · 중요도 2)
- **feedback_stop_hook_runs_after_display** [infra][harness] — Stop 훅은 답변이 화면에 나간 뒤에 돈다 — 걸러서 다시 쓰게 하면 사용자는 초안과 고친 답 두 벌을 본다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/memory/feedback_stop_hook_runs_after_display.md` · grounding `미분류` · 중요도 2)
- **feedback_ios_distribution_cert_missing** [infra][backend] — iOS 「No signing certificate iOS Distribution」 = 인증서 실종이 아니라 Xcode 애플 ID 로그아웃. 배포 인증서는 클라우드 관리라 키체인·ASC 목록에 안 보인다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_ios_distribution_cert_missing.md` · grounding `미분류` · 중요도 2)
- **feedback_macos_clock_hides_precision_bugs** [infra][harness][design][backend][rust][reflect] — macOS 의 Utc::now() 는 나노 자리가 늘 0 이라 마이크로초 절삭 버그가 로컬에서 영영 안 보인다. 리눅스 CI 에서만 실패하면 시계 정밀도를 의심하라  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_macos_clock_hides_precision_bugs.md` · grounding `미분류` · 중요도 2)
- **feedback_merge_clobbers_unstaged_edit** [infra][harness][backend][rust] — 공유 워크트리에서 남의 머지가 스테이징 안 된 내 수정을 지운다. 경로 한정 커밋은 그 지워진 상태를 그대로 커밋한다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_merge_clobbers_unstaged_edit.md` · grounding `미분류` · 중요도 1)
- **feedback_reproduce_handoff_diagnosis** [infra] — 핸드오프가 적어 둔 «원인»을 그대로 믿지 말고 재현부터 하라 — 5건 중 2건이 오진이었다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_reproduce_handoff_diagnosis.md` · grounding `미분류` · 중요도 1)
- **feedback_shared_worktree_branch_moves** [infra] — 공유 워킹트리는 «브랜치»도 공유한다 — 커밋 직전에 현재 브랜치를 확인하고, 남의 브랜치에 얹혔으면 체크아웃 없이 옮긴다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_shared_worktree_branch_moves.md` · grounding `미분류` · 중요도 1)
- **feedback_verify_the_convention_protects** [infra][harness][onboarding] — 리포의 기존 시크릿 관례를 따르라고 권하기 전에 그 관례가 실제로 보호를 주는지(키가 안 새고 있는지) 먼저 감사하라  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-flutter-playwright/memory/feedback_verify_the_convention_protects.md` · grounding `미분류` · 중요도 1)
- **feedback-console-ui-verify** [onboarding][research][design][infra][harness][reflect] — 외부 콘솔(Play, App Store Connect, GCP, AWS 등) UI 안내 시 반드시 공식 docs 또는 fastlane docs WebFetch 후 정확한 메뉴 경로 인용. 추측 금지.  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_console_ui_verify.md` · grounding `mixed` · 중요도 3)
- **feedback-terminology-glossary** [onboarding][backend][design][planning] — 셋업/온보딩 가이드 등 문서 작성 시 영어 약자가 처음 등장하면 한글 풀이를 병기한다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_terminology_glossary.md` · grounding `user_correction` · 중요도 3)
- **feedback_negative_control_on_zero_failure_paths** [onboarding][tooling] — 실패 경로 코드는 클린 런에서 실행조차 안 되므로 음성 대조 없이는 결함이 영원히 숨는다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-flutter-playwright/memory/feedback_negative_control_on_zero_failure_paths.md` · grounding `미분류` · 중요도 1)
- **feedback-user-confirmed-facts** [research][harness][design] — 사용자가 이미 확인했다고 명시한 사실은 재검증하지 마라 — Codex/WebFetch 위임 금지  (`~/.claude/projects/-Users-jackson/memory/feedback_user_confirmed_facts.md` · grounding `user_correction` · 중요도 5)
- **codex-default-model** [research][backend] — codex-rescue 간헐 실패의 진짜 원인 = 공유 app-server broker/데몬 경로 (모델 아님). codex exec 직접 호출이 정공법.  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-purchase-bot/memory/codex-default-model.md` · grounding `execution_evidence` · 중요도 4)
- **codex-research-foreground** [research][harness] — codex 리서치 위임은 항상 foreground(블로킹)로 실행 — 백그라운드는 hang 시 결과가 유기됨  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-apps/memory/feedback_codex_research_foreground.md` · grounding `mixed` · 중요도 3)
- **codex 는 기다리면서 직접 불러라** [research][infra] — codex 는 자주 죽으므로 결과가 나올 때까지 기다리는 방식으로만 돌린다. codex-rescue 에이전트는 겉보기에 기다리는 것 같아도 내부에서 뒤로 넘겨버리므로 쓰지 말고, codex-companion.mjs 를 Bash 로 직접 호출하라. 일반 서브에이전트를 뒤에서 돌리는 것은   (`~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/memory/feedback_codex_foreground_call_direct.md` · grounding `user_correction` · 중요도 3)
- **feedback-codex-research-backgrounded** [research] — codex-rescue가 foreground 지정을 무시하고 백그라운드 태스크로 던질 수 있다 — companion 스크립트로 직접 회수하라  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-flutter-playwright/memory/feedback_codex_research_backgrounded.md` · grounding `execution_evidence` · 중요도 3)
- **인용문을 못 찾았다면 문서에 없는 게 아니라 내가 확인을 못 한 것이다** [research][harness] — 공식 문서에서 인용한 문장을 찾지 못했을 때, 그건 문서에 그 문장이 없다는 뜻이 아니라 내가 확인을 못 했다는 뜻이다. HTML 특수문자 표기, 줄바꿈과 들여쓰기, 본문을 자바스크립트로 그리는 사이트, 쓰인 글자만 추려 담은 PDF 글꼴 — 이 네 가지를 먼저 걸러낸 다음에 판단하라.  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/memory/feedback_quote_verification_traps.md` · grounding `미분류` · 중요도 2)
- **feedback_codex_diagnose_split_by_source** [research][harness][backend][rust] — codex 실패를 진단할 땐 세션 기록을 source 별로 갈라라. 섞으면 남의 경로 통계로 내 래퍼를 고치게 된다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/memory/feedback_codex_diagnose_split_by_source.md` · grounding `미분류` · 중요도 1)
- **feedback_codex_json_events_not_faster** [research][harness][design][rust] — codex exec --json 은 끊김을 빨리 잡아주지 않는다. 얻는 것은 실패 원인 구분과 차례 식별자다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/memory/feedback_codex_json_events_not_faster.md` · grounding `미분류` · 중요도 1)
- **feedback_codex_relays_orca_keys_not_in_bambu** [research][bambu] — Codex 의 슬라이서 설정 제안은 OrcaSlicer 키를 섞는다 — Bambu 설치본에서 실존 확인 필수  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/memory/feedback_codex_relays_orca_keys_not_in_bambu.md` · grounding `미분류` · 중요도 1)
- **feedback_no_blocking_ui_give_undo** [research] — 값이 사라지는 조작은 막거나 잠금 표시를 달지 말고, 되돌리는(초기화) 창구를 하나 줘라  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_no_blocking_ui_give_undo.md` · grounding `미분류` · 중요도 1)
- **feedback_e2e_use_mcp_dont_flail** [tooling][design][backend][flutter][infra][reflect][harness] — 실기/시뮬 e2e 테스트는 fitpal-mobile MCP로 직접 구동하라 — 넘겨짚고 포기하지 말 것. 반복 지적된 최악 마찰  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_e2e_use_mcp_dont_flail.md` · grounding `mixed` · 중요도 4)
- **feedback_hot_reload_log_string** [tooling][flutter][harness] — hot reload 적재 확인 문자열은 "Reloaded application in"이 아니라 "Reloaded N of M libraries in" (Flutter 3.41)  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_hot_reload_log_string.md` · grounding `execution_evidence` · 중요도 4)
- **feedback_isolate_the_instrument_too** [tooling][harness][flutter] — 격리 재현을 주장할 때 코드·기기·로그뿐 아니라 조작 수단(계측 도구)도 격리했는지 확인하라  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_isolate_the_instrument_too.md` · grounding `execution_evidence` · 중요도 4)
- **feedback_mcp_dynamic_tools_need_hot_restart** [tooling][flutter][backend][harness][design] — MCP 동적 도구 0개는 서버가 아니라 앱이 등록을 재전송해야 복구된다 — pkill 말고 hot restart  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_mcp_dynamic_tools_need_hot_restart.md` · grounding `execution_evidence` · 중요도 4)
- **feedback_simctl_privacy_kills_app** [tooling][harness][flutter] — grant_app_permission(simctl privacy)은 대상 앱을 종료시킨다 — 실기 검증 «전에» 미리 줘라  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_simctl_privacy_kills_app.md` · grounding `execution_evidence` · 중요도 4)
- **feedback-flutter-playwright-only** [tooling][harness][flutter][backend][reflect][design] — 앱/카탈로그 검증에 범용 playwright MCP 금지 — fitpal-web/mobile 전용, 동적도구 0이면 풀로드 후 pkill 재spawn  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_flutter_playwright_only.md` · grounding `mixed` · 중요도 3)
- **mcp** [tooling][flutter][harness][backend] — flutter-playwright MCP로 앱 검증 시 full flutter run 재실행 금지 — VM주소 변경 + 서버 kill이 동적도구 채널을 끊는다. hot restart만 사용.  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_mcp_runtime_verify_no_relaunch.md` · grounding `execution_evidence` · 중요도 3)
- **feedback_mcp_widget_absent_check_route** [tooling][flutter][design][reflect] — MCP find_widget 0매치는 도구 버그가 아니라 "그 화면에 진짜 없음" 신호 — pushed route 여부부터 확인하라  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_mcp_widget_absent_check_route.md` · grounding `execution_evidence` · 중요도 3)
- **feedback_runtime_test_last** [tooling][harness][flutter][reflect][bambu][design] — 실기 구동(앱 launch) e2e 테스트는 스프린트마다 하지 말고 기능 전체(멀티 스프린트) 맨 끝에 한 번에  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_runtime_test_last.md` · grounding `user_correction` · 중요도 3)
- **feedback_cdp_navigate_breaks_dwds** [tooling][flutter] — 플러터 웹 debug 세션에 CDP Page.navigate 로 주소를 바꾸면 DWDS 가 옛 JS 컨텍스트에 묶여 죽는다 — 라우트를 바꾸려면 재기동  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_cdp_navigate_breaks_dwds.md` · grounding `미분류` · 중요도 2)
- **feedback_ios26_photo_permission_needs_dialog_tap** [tooling][flutter][backend] — iOS26 시뮬레이터는 simctl privacy grant photos 가 안 먹는다 — MCP dismiss_native_dialog 로 알럿을 눌러야 열린다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_ios26_photo_permission_needs_dialog_tap.md` · grounding `미분류` · 중요도 2)
- **feedback_mcp_no_fullscreen_capture** [tooling][harness][flutter][design][backend][infra] — fitpal-mobile MCP 빌드에는 전체 화면 캡처 도구가 없다 — BackdropFilter 는 subtree 캡처로 판정하면 틀린 그림이 나온다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_mcp_no_fullscreen_capture.md` · grounding `미분류` · 중요도 2)
- **feedback_mcp_pointer_leak_dead_swipe** [tooling][flutter] — MCP swipe_area 가 갑자기 무반응이면 앱이 아니라 툴킷이 포인터를 물고 있는 것 — 라우트 재진입으로 푼다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_mcp_pointer_leak_dead_swipe.md` · grounding `미분류` · 중요도 2)
- **feedback_mcp_recording_kills_ios_app** [tooling][flutter][design] — MCP recording 도구는 stop 에서 iOS 앱을 죽인다 — 애니메이션 증거는 simctl 연속 캡처로  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_mcp_recording_kills_ios_app.md` · grounding `미분류` · 중요도 2)
- **flutter-playwright-mcp-gotchas** [tooling][harness][flutter][backend][onboarding] — Flutter Playwright MCP 로 실기 검증할 때 반복해서 시간을 잡아먹는 네 가지 함정과 대처  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-viseo365/memory/flutter-playwright-mcp-gotchas.md` · grounding `미분류` · 중요도 2)
- **feedback_mcp_arg_ahead_of_release** [tooling][flutter][backend][harness] — .mcp.json 이 아직 안 나온 서버 기능의 인자를 쓰면 MCP 가 조용히 죽고 그 세션에선 못 살린다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_mcp_arg_ahead_of_release.md` · grounding `미분류` · 중요도 1)
- **feedback_mcp_server_unmodifiable_list** [tooling][flutter][backend][infra] — MCP 동적 도구 0개 + refreshClientTools 실패는 앱이 아니라 flutter_playwright_server 결함일 수 있다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_mcp_server_unmodifiable_list.md` · grounding `미분류` · 중요도 1)
- **feedback_profile_build_has_no_mcp** [tooling][flutter][harness][backend] — profile 빌드에는 MCP 도구가 하나도 없다 — 툴킷이 서비스 확장을 assert 안에서 등록한다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_profile_build_has_no_mcp.md` · grounding `미분류` · 중요도 1)
- **feedback_parallel_sessions_share_everything** [tooling][harness] — 한 리포에 Claude 세션이 둘 이상이면 워킹트리·git 인덱스·/tmp 경로·시뮬레이터를 공유한다. git add 는 격리 수단이 아니다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-flutter-playwright/memory/feedback_parallel_sessions_share_everything.md` · grounding `미분류` · 중요도 1)

## 1. 글로벌 Evaluator Feedback

- 경로: `/Users/jackson/.harness/feedback/evaluator`
- 총 파일: **450**

### Verdict 분포

- **APPROVE**: 266
- **REJECT**: 175
- **UNKNOWN**: 9

### Skill 분포

- `qa-evaluator`: 450

### Project 분포 (canonical — allowlist 병합 후)

canonical 기준은 **writer 쪽 identity** 다 — `harness/scripts/save-feedback.sh` 가 CONTRACT_ROOT 의 git root basename 으로 계산하는 이름. 집계가 다른 방향으로 정규화하면 같은 프로젝트가 신·구 버킷으로 영구 분열하므로 writer 에 맞춘다 (예: `fit-pal/app`·`fit-pal/server` 는 .git 이 없어 git root 가 `fit-pal` 하나다).

병합은 `PROJECT_NAME_ALIASES` **명시 allowlist** 로만 한다. 이름 유사도/fuzzy 매칭은 쓰지 않는다. 병합된 그룹은 서브프로젝트 구분이 사라지지 않도록 원본 이름 내역을 `←` 뒤에 함께 보여준다.

- `claude-plugins`: 219  ← `claude-plugins` 215, `bambu-kit-v0.4.0-9mm-craft-knife` 1, `claude-plugins / react-kit phase10-research kaizen` 1, `bambu-kit/bambu-print-profile v0.4.1` 1, `bambu-kit/bambu-print-profile` 1
- `fit-pal`: 175  ← `fit-pal` 106, `fit-pal-app` 37, `fit-pal-server` 17, `fit-pal/app` 6, `fit-pal/server` 5, `fitpal-server` 4
- `flutter_playwright`: 30
- `navi2025flutter`: 6
- `viseo365`: 5
- `insights-0924-kaizen`: 2
- `harness-amend-direction`: 1
- `fit-pal-flutter`: 1
- `onboarding-gate-defects`: 1
- `wt-e2e`: 1
- `harness-auto-section-na`: 1
- `bambu-orca-h2s-feedback`: 1
- `fp-accounts`: 1
- `iyaki-zip-dev`: 1
- `bambu-surface-first-geometry`: 1
- `bambu-print-lessons`: 1
- `bambu-bridge-scope`: 1
- `fp-prep`: 1
- `joo6077-plugins`: 1

### Project 분포 (raw `project_name` — 병합 전 원본)

병합이 원본을 감추지 않도록 그대로 남긴다. canonical 과 raw 개수가 다르면 그 차이가 곧 레거시 표기 흔들림의 규모다.

- `claude-plugins`: 215
- `fit-pal`: 106
- `fit-pal-app`: 37  → merged into `fit-pal`
- `flutter_playwright`: 30
- `fit-pal-server`: 17  → merged into `fit-pal`
- `fit-pal/app`: 6  → merged into `fit-pal`
- `navi2025flutter`: 6
- `fit-pal/server`: 5  → merged into `fit-pal`
- `viseo365`: 5
- `fitpal-server`: 4  → merged into `fit-pal`
- `insights-0924-kaizen`: 2
- `harness-amend-direction`: 1
- `fit-pal-flutter`: 1
- `bambu-kit-v0.4.0-9mm-craft-knife`: 1  → merged into `claude-plugins`
- `onboarding-gate-defects`: 1
- `wt-e2e`: 1
- `harness-auto-section-na`: 1
- `bambu-orca-h2s-feedback`: 1
- `fp-accounts`: 1
- `iyaki-zip-dev`: 1
- `bambu-surface-first-geometry`: 1
- `claude-plugins / react-kit phase10-research kaizen`: 1  → merged into `claude-plugins`
- `bambu-print-lessons`: 1
- `bambu-bridge-scope`: 1
- `fp-prep`: 1
- `bambu-kit/bambu-print-profile v0.4.1`: 1  → merged into `claude-plugins`
- `bambu-kit/bambu-print-profile`: 1  → merged into `claude-plugins`
- `joo6077-plugins`: 1

- raw 이름 종류: **28** → canonical 그룹: **19** (allowlist 적용 파일 73건)

### schema_version / 세대 분포

`schema_version` 과 결정론적 identity 필드(`draft_project_name`, `draft_project_hash`, `sprint_slug`, `contract_path`) 유무로 신·구 피드백을 구분한다. `legacy-identity` 는 `project_name`/`project_hash` 가 cwd 기준으로 계산되던 시기의 기록이라 위 raw 분포의 표기 흔들림 원인이 된다.

- schema_version `1`: 450
  - 정규화 전 원본 표기: `1` 440, `'1.0'` 7, `'1'` 3

- v1 · legacy-identity: 244
- v1 · deterministic-identity: 206

#### `contract_path` 귀속 근거

`save-feedback.sh` 는 `HARNESS_CONTRACT` / draft 값이 없으면 계약 경로를 **추측**하고 `contract_path_inferred: true` 를 남긴다. `inferred` 비율이 높으면 피드백이 stale 한 plain 계약에 오귀속되고 있을 수 있다.

- explicit(명시): 206

### 최근 REJECT 사유 (Top 20)

- [2026-09-24] **insights-0924-kaizen**: DG-03: validate-post-kaizen.py 가 docs-site-regen · scope-isolation 2건 FAIL — N/A 주장에 딸린 'FAIL 0' 측정 요건 미충족
- [2026-09-24] **insights-0924-kaizen**: DG-02: flutter-toolkit/skills/flutter-ui-verify/SKILL.md:23 에 신규 MD025(중복 H1) 경고 — 새로 더한 줄에 걸린 markdownlint 경고 0개 요건 위반
- [2026-09-24] **claude-plugins**: ER-02: 측정(grep '10 카테고리|V1~V10|V1-V10')이 대상 20개 파일 중 3건 매치 (기준 0). 매치는 감사 카테고리 명명 규칙 등 무관한 문맥 — 검사 번호 표기(V1~V10)만 좁히면 0
- [2026-09-24] **claude-plugins**: DG-04: 브라우저 콘솔 에러 실측 1건 (favicon 404, docs/index.html 발) — 조건 요구값 0과 불일치. 범위 경계가 docs/index.html 수정을 금지해 조건과 충돌
- [2026-09-24] **claude-plugins**: AR-02: ER-02와 동일 측정을 공유하는 후반부 조건이 같은 이유로 실패
- [2026-09-22] **claude-plugins**: ER-02: 계약 명시 측정(PATH=/usr/bin:/bin로 jq 은폐)을 문자 그대로 실행하면 이 기계에서 jq(/usr/bin/jq)가 은폐되지 않아 스크립트가 정상 동작(1567바이트 출력)해 0바이트 기준 위반. 사이드카 AM-01이 측정 명령 정정을 제안했으나 direction=relaxing × consent=unanchored라 PASS 근
- [2026-09-22] **claude-plugins**: AR-04: 계약 명시 find 명령을 문자 그대로 실행하면 범위 6파일+.plain-korean-*(7개) 외에 sessions/*.json 2개·codex-research-log/.harvested.json 1개(총 10개)가 검출됨. 사이드카 AM-02가 제외 경로 추가를 제안했으나 direction=relaxing × consent=unanchore
- [2026-09-22] **claude-plugins**: AR-04 FAIL — amendment A-01의 consent: anchored 주장이 기계적으로 반증됨 (사이드카가 포함된 커밋 cb39d899의 시각 15:49:57이 합의 주장 시각 16:05보다 앞섬, reflect-kit 프롬프트 기록에도 해당 세션 대화 없음). A-01을 PASS 근거로 쓸 수 없어 원 계약(허용 3개 파일)으로 판정하면 s
- [2026-09-15] **claude-plugins**: DG-02: 신규 build-option-list.sh 에서 shellcheck SC2206 경고 3건(26·27·35행, $VERSION 미인용 배열 확장) — IDE diagnostics 0건 요구를 충족하지 못함
- [2026-09-14] **claude-plugins**: DG-04: 수정된 스킬 end-to-end 실행 산출물 0 건. 스킬 출력 루트에서 계약 봉인(2026-09-13 11:44) 이후 mtime 파일 0 건, 최신 산출물은 2026-09-13 10:10 이며 process 만 있고 filament 없음. Phase 1.95 표식 _target_slicer 도 전 산출물 0 건. 양쪽 슬라이서 설치본과 모델
- [2026-09-14] **claude-plugins**: AR-03: 파생 HTML 3 종 중 docs/bambu-kit/bambu-print-profile.html 이 소스 변경 미반영. SKILL.md 신설분(Phase 1.95 / TARGET_SLICER / 슬라이서 판별 / 음성 대조) 4 토큰 전부 0 건이고, SK-01 이 제거를 요구한 오르카 배제 문구가 :151 · :170 에 잔존. 계약 측정문 
- [2026-09-11] **navi2025flutter**: RE-01(AM-10): AR-03과 동일한 grep, 동일 임계치로 동일하게 3파일, 정확히 2 미충족
- [2026-09-11] **navi2025flutter**: AR-03: grep -rl body_delta_editor.dart lib/pages/ 실측 3파일, 조건 요구 정확히 2파일 - 리터럴 불일치
- [2026-09-11] **flutter_playwright**: SC-02 FAIL — docs/superpowers/plans/2026-09-10-accounts-environments.md and docs/superpowers/specs/2026-09-10-accounts-environments-design.md fall outside the original 13-item whitelist. AM-01 correct
- [2026-09-11] **flutter_playwright**: SC-01: .claude/tone-project.md 가 SC-01 허용 4경로 밖에서 생성됨 (이 스프린트 자신의 커밋)
- [2026-09-11] **flutter_playwright**: PK-03: 사진 피커 완주 증거 부재 (제출된 증거는 카메라 권한 거부 시나리오이며 피커 표시/선택/확인 단계가 없음)
- [2026-09-11] **flutter_playwright**: CT-02: 도구 스키마 변경 소비면 3종 중 tool_contract_test.dart / native_platform_tools_test.dart 2종이 diff에 없음
- [2026-09-11] **flutter_playwright**: AN-03: 권한 다이얼로그 전면 실측 XML 픽스처 부재 (다른 앱(카메라) 전면으로 대체, 정식 amendment 승인 없음)
- [2026-09-11] **claude-plugins**: SK-01 FAIL — 게이트가 확인: 줄을 deprecation 주장 탐지에서 제외해야 하는데 구현이 QA Iteration 1 지적을 수용하며 의도적으로 되돌렸다. AM-02는 ER-01/ER-02만 대상으로 선언해 SK-01을 흡수하지 않는다.
- [2026-09-11] **claude-plugins**: RE-02 FAIL — 적용 메모가 명시한 hook_field 재사용을 하지 않음. check-plain-korean.sh 는 _lib-hook-payload.sh 를 source 조차 하지 않고 jq 파싱을 자체 인라인으로 중복 구현했다. block-dirwide-autofixer.sh 의 소스 방식을 그대로 따를 수 있었고 AR-03 파일 수에 영향을 

### 최근 Improvement Suggestions (Top 15)

- [2026-09-24] **insights-0924-kaizen**: [DG-03] 측정-환경-오염 — AR-01 화이트리스트(docs/harness/*.html 미포함)와 DG-03의 validate-post-kaizen.py FAIL 0 요건이 구조적으로 충돌. docs-site-regen/scope-isolation 을 화이트리스트에 포함하거나 DG-03 측정에서 명시적으로 제외해야 한다
- [2026-09-24] **insights-0924-kaizen**: [DG-02] 측정-환경-오염 — SKILL.md 신규 작성 시 H1 정확히 1개(grep -c '^# ') 확인을 계약에 못박아 A-01류 부분 수정 재발 방지
- [2026-09-24] **flutter_playwright**: [RG-01] 검증경로-미기재 — 빌드 실패 시 flutter run 단일 아키텍처 산출물로 대체하는 fallback 오라클을 최초 계약에 명시할 것
- [2026-09-24] **flutter_playwright**: [DG-04] 콘솔 오류 grep 은 대소문자 무시(grep -ci)로 쓰고, runZonedGuarded 앱은 서버 runtime events 를 측정에 넣을 것
- [2026-09-24] **fit-pal**: [DG-04] 검증경로-미기재 — evaluator 도구셋(Read/Grep/Glob/Bash, MCP 미포함)으로는 카탈로그 상호작용을 수행할 수 없다. 위젯 시험 대체 인정 명문화 또는 runtime_inspection.mcp_server 설정을 권장
- [2026-09-24] **claude-plugins**: [문서 정리] amendment 사이드카 파일 안에서 헤더 식별자(A-02)가 서로 다른 내용으로 두 번 재사용됐다. 새 개정마다 번호를 이어가는 규칙(A-03, A-04...)을 명문화할 필요가 있다.
- [2026-09-24] **claude-plugins**: [SK-03] 측정-환경-오염 — 조건의 양성 대조 문구가 실측과 다르다(Iteration 1에서 이미 지적, 이번 판정에는 영향 없음).
- [2026-09-24] **claude-plugins**: [SK-01] 태그-산출물-불일치 — 측정문을 grep -n '^### 6.7' (헤더 자체) 기준으로 바꾸는 편을 권장
- [2026-09-24] **claude-plugins**: [ER-04, ER-05] 측정-방식-불일치 — 한국어 'N개 킷' 패턴은 잡지만 영어 'N plugins' 형태는 못 잡는 사각지대가 남아있다
- [2026-09-24] **claude-plugins**: [ER-02] 측정-방식-불일치 — grep 패턴을 'V1~V10|V1-V10'로 좁힌다 ('10 카테고리'는 backend/infra-kaizen 감사 카테고리 명명 규칙과 충돌)
- [2026-09-24] **claude-plugins**: [ER-02/AR-02] 측정-방식-불일치 — 검사 번호(V1~VN) 표기만 재는 관례를 처음부터 적용할 것
- [2026-09-24] **claude-plugins**: [ER-02/AR-02] 측정-방식-불일치 — 'N 카테고리' 형태는 backend-kit/infra-kit 감사 카테고리(10종)와 항상 겹치므로 다음부터 애초에 재는 낱말 후보에서 제외할 것
- [2026-09-24] **claude-plugins**: [DG-04] 검증경로-미기재 — node Playwright fallback을 기본 헤드리스로 돌리면 파비콘류 결함을 못 보는 죽은 측정이 될 수 있다. headless:false(또는 신형 헤드리스 명시)를 fallback 절차에 명시할 것을 제안
- [2026-09-24] **claude-plugins**: [AR-02] 측정-방식-불일치 — ER-02와 동일 측정 공유. 같은 수정 필요, 계약에 '같은 측정 재사용' 각주 권장
- [2026-09-24] **claude-plugins**: [AR-02] 범위-미명시 — 기준 문서 안 개수 표기 다수 위치 흩어짐 (Iteration 3부터 누적)

## 2. 외부 프로젝트 (`Hub/10_Dev`) 피드백

- Hub 루트: `/Users/jackson/Hub/10_Dev`
- 발견된 프로젝트: **17**

- 수집된 sprint-feedback 파일: **154** (그중 접미형 `sprint-feedback-<slug>.md`: **140**)

### `_sandbox/flutter_colorpicker`

- 경로: `/Users/jackson/Hub/10_Dev/_sandbox/flutter_colorpicker`
- sprint-feedback 파일: 0개 (총 0 lines)
- history sprint-contracts: 0

### `apps`

- 경로: `/Users/jackson/Hub/10_Dev/apps`
- sprint-feedback 파일: 1개 (총 270 lines)
- history sprint-contracts: 54
- 최근 contracts:
  - 20260629-1808-sprint-contract.md
  - 20260629-1944-sprint-contract.md
  - 20260629-1958-sprint-contract.md
  - 20260630-1257-sprint-contract.md
  - 20260630-1721-sprint-contract.md
- 파일별 내역:
  - `sprint-feedback.md` — plain (슬러그 없음), 270 lines, mtime 2026-06-30T15:49:36

<details><summary>sprint-feedback.md 앞부분</summary>

```markdown
---

# Sprint Feedback
Feature: preset 리팩토링 5단계 (per-screen skin 섹션 위젯 추출)
Evaluated: 2026-06-30 14:30
Verdict: APPROVE
Iteration: 1

## Results

### UI (1/1)
- [x] UI-01: per-screen skin 섹션 1:1 동일 표시 — PASS [L3]
  - 근거: `adm_preset_per_screen_skin_widget.dart:141–218`
    (a) 헤더 Row: `admin_preset_skin_title` Text + `admin_preset_skin_reset` 버튼 — `:150,:158`
    (b) 14개 화면 행(for 루프): `AdmSectionHeaderWidget(title+preview버튼+change버튼)` — `:173–201`
    (c) 행 간 `if (i > 0) SizedBox(height: AdmSizes.h40)` — `:172`
    (d) `hasAnimation && skin?.getGuideAnimation == ''` 경고 텍스트 — `:204–211`
    원본 `e61f26c6:_sectionPerScreenSkin` 구조 1:1 일치.

### Logic (4/4)
```

</details>

### `claude-plugins`

- 경로: `/Users/jackson/Hub/10_Dev/claude-plugins`
- sprint-feedback 파일: 70개 (총 10591 lines)
- history sprint-contracts: 101
- 접미형 슬러그: `plugin-validation-page-sync`, `check-count-decouple-and-table-gate`, `seal-commit-and-evidence-boundary`, `bambu-kit-gate-unread-slot-report`, `bambu-kit-gate-unreadable-slot`, `bambu-kit-bridge-scope-extruders`, `cross-diagnosis-to-parent`, `contract-verifiability-gaps`, `h2-flipper-rear-exhaust-abs-overhang`, `bambu-kit-bridge-ironing`, `h2-flipper-rear-exhaust-abs-profile`, `validate-check-count-sync`, `h2-flipper-rear-exhaust-petg-hf-profile`, `plain-korean-remind-before-report`, `contract-kaizen-arg-safe-na-precheck`, `harness-auto-section-na`, `bambu-kit-print-lessons`, `evaluator-kaizen-zero-control-cross-diag`, `qa-pending-hook-context-reject`, `fly-catcher-orca-h2s-profile`, `qa-pending-stop-hook`, `h2-ams-flipper-abs-profile-v2`, `bambu-kit-option-key-registry-probe`, `bambu-kit-slicer-axis-and-seam-policy`, `codex-stdin-guard-gap-and-json-failure-verdict`, `codex-research-pipeline`, `plain-korean-output-gate`, `howto-research-ui-anchoring`, `howto-research-procedure-standards`, `howto-research-deprecation-policy`, `howto-research-branch-catalog`, `howto-kaizen-g4-precision`, `bambu-kit-surface-first-geometry-class`, `howto-research-deep-links`, `harness-archetype12-unchanged-oracle`, `howto-kit-implementation`, `howto-kit-design-brief`, `onboarding-kit-gate-defects`, `harness-amend-direction-baseline-case`, `antipattern-command-field`, `harness-attribution-followup`, `harness-attribution-followup-v2`, `harness-core-defects`, `docs-quality-gates`, `bambu-kit-enum-allowlist-gate`, `bambu-seam-policy`, `bambu-kit`, `tone-kit-framework-vocab`, `tone-kit`, `autofixer-oracle-guards`, `kaizen-phase9-rust-guards`, `kaizen-phase8-infra-gate-taxonomy`, `kaizen-phase7-write-path-integrity`, `kaizen-phase6-variant-decision-gates`, `kaizen-phase5-flutter-gates`, `kaizen-phase4-doc-contract-gates`, `kaizen-phase3-unverified-triage`, `kaizen-phase2-contract-seal`, `kaizen-phase14-onboarding-facts`, `kaizen-phase13-failure-modes`, `kaizen-phase12b-oracle-positive-control`, `kaizen-phase12a-tag-canonicalization`, `kaizen-phase11-planning-facts`, `kaizen-phase1-design-guides`, `kaizen-memory-integration`, `kaizen-final-2026-08-13`, `visual-styles-modal`, `task2`, `task-78`
- 최근 contracts:
  - 20260727-kaizen-phase9-rust-sprint-contract.md
  - 20260727-phase1-prev-sprint-contract.md
  - 20260727-phase1-sprint-contract.md
  - 20260727-phase2-sprint-contract.md
  - 20260727-phase3-sprint-contract.md
- 파일별 내역:
  - `sprint-feedback.md` — plain (슬러그 없음), 47 lines, mtime 2026-06-11T16:05:20
  - `sprint-feedback-plugin-validation-page-sync.md` — slug=`plugin-validation-page-sync`, 142 lines, mtime 2026-09-24T15:10:06
  - `sprint-feedback-check-count-decouple-and-table-gate.md` — slug=`check-count-decouple-and-table-gate`, 244 lines, mtime 2026-09-24T13:21:34
  - `sprint-feedback-seal-commit-and-evidence-boundary.md` — slug=`seal-commit-and-evidence-boundary`, 220 lines, mtime 2026-09-24T10:38:10
  - `sprint-feedback-bambu-kit-gate-unread-slot-report.md` — slug=`bambu-kit-gate-unread-slot-report`, 102 lines, mtime 2026-09-23T12:18:41
  - `sprint-feedback-bambu-kit-gate-unreadable-slot.md` — slug=`bambu-kit-gate-unreadable-slot`, 140 lines, mtime 2026-09-23T11:40:35
  - `sprint-feedback-bambu-kit-bridge-scope-extruders.md` — slug=`bambu-kit-bridge-scope-extruders`, 117 lines, mtime 2026-09-23T11:15:24
  - `sprint-feedback-cross-diagnosis-to-parent.md` — slug=`cross-diagnosis-to-parent`, 220 lines, mtime 2026-09-23T10:55:59
  - `sprint-feedback-contract-verifiability-gaps.md` — slug=`contract-verifiability-gaps`, 235 lines, mtime 2026-09-23T10:55:59
  - `sprint-feedback-h2-flipper-rear-exhaust-abs-overhang.md` — slug=`h2-flipper-rear-exhaust-abs-overhang`, 121 lines, mtime 2026-09-23T09:57:02
  - `sprint-feedback-bambu-kit-bridge-ironing.md` — slug=`bambu-kit-bridge-ironing`, 133 lines, mtime 2026-09-23T09:49:48
  - `sprint-feedback-h2-flipper-rear-exhaust-abs-profile.md` — slug=`h2-flipper-rear-exhaust-abs-profile`, 200 lines, mtime 2026-09-22T17:05:19
  - `sprint-feedback-validate-check-count-sync.md` — slug=`validate-check-count-sync`, 176 lines, mtime 2026-09-22T15:06:31
  - `sprint-feedback-h2-flipper-rear-exhaust-petg-hf-profile.md` — slug=`h2-flipper-rear-exhaust-petg-hf-profile`, 171 lines, mtime 2026-09-22T14:58:10
  - `sprint-feedback-plain-korean-remind-before-report.md` — slug=`plain-korean-remind-before-report`, 129 lines, mtime 2026-09-22T14:02:53
  - `sprint-feedback-contract-kaizen-arg-safe-na-precheck.md` — slug=`contract-kaizen-arg-safe-na-precheck`, 138 lines, mtime 2026-09-21T10:20:47
  - `sprint-feedback-harness-auto-section-na.md` — slug=`harness-auto-section-na`, 108 lines, mtime 2026-09-20T00:21:29
  - `sprint-feedback-bambu-kit-print-lessons.md` — slug=`bambu-kit-print-lessons`, 112 lines, mtime 2026-09-20T00:21:29
  - `sprint-feedback-evaluator-kaizen-zero-control-cross-diag.md` — slug=`evaluator-kaizen-zero-control-cross-diag`, 162 lines, mtime 2026-09-19T22:15:49
  - `sprint-feedback-qa-pending-hook-context-reject.md` — slug=`qa-pending-hook-context-reject`, 103 lines, mtime 2026-09-19T13:45:43
  - `sprint-feedback-fly-catcher-orca-h2s-profile.md` — slug=`fly-catcher-orca-h2s-profile`, 100 lines, mtime 2026-09-19T12:57:24
  - `sprint-feedback-qa-pending-stop-hook.md` — slug=`qa-pending-stop-hook`, 113 lines, mtime 2026-09-19T12:34:19
  - `sprint-feedback-h2-ams-flipper-abs-profile-v2.md` — slug=`h2-ams-flipper-abs-profile-v2`, 141 lines, mtime 2026-09-19T11:08:38
  - `sprint-feedback-bambu-kit-option-key-registry-probe.md` — slug=`bambu-kit-option-key-registry-probe`, 224 lines, mtime 2026-09-16T11:09:00
  - `sprint-feedback-bambu-kit-slicer-axis-and-seam-policy.md` — slug=`bambu-kit-slicer-axis-and-seam-policy`, 313 lines, mtime 2026-09-14T12:37:54
  - `sprint-feedback-codex-stdin-guard-gap-and-json-failure-verdict.md` — slug=`codex-stdin-guard-gap-and-json-failure-verdict`, 135 lines, mtime 2026-09-14T10:43:43
  - `sprint-feedback-codex-research-pipeline.md` — slug=`codex-research-pipeline`, 149 lines, mtime 2026-09-12T22:03:19
  - `sprint-feedback-plain-korean-output-gate.md` — slug=`plain-korean-output-gate`, 152 lines, mtime 2026-09-12T15:49:04
  - `sprint-feedback-howto-research-ui-anchoring.md` — slug=`howto-research-ui-anchoring`, 162 lines, mtime 2026-09-12T15:49:04
  - `sprint-feedback-howto-research-procedure-standards.md` — slug=`howto-research-procedure-standards`, 121 lines, mtime 2026-09-12T15:49:04
  - `sprint-feedback-howto-research-deprecation-policy.md` — slug=`howto-research-deprecation-policy`, 150 lines, mtime 2026-09-12T15:49:04
  - `sprint-feedback-howto-research-branch-catalog.md` — slug=`howto-research-branch-catalog`, 126 lines, mtime 2026-09-12T15:49:04
  - `sprint-feedback-howto-kaizen-g4-precision.md` — slug=`howto-kaizen-g4-precision`, 205 lines, mtime 2026-09-12T15:49:04
  - `sprint-feedback-bambu-kit-surface-first-geometry-class.md` — slug=`bambu-kit-surface-first-geometry-class`, 132 lines, mtime 2026-09-10T11:10:24
  - `sprint-feedback-howto-research-deep-links.md` — slug=`howto-research-deep-links`, 128 lines, mtime 2026-09-09T16:05:46
  - `sprint-feedback-harness-archetype12-unchanged-oracle.md` — slug=`harness-archetype12-unchanged-oracle`, 142 lines, mtime 2026-09-09T16:05:16
  - `sprint-feedback-howto-kit-implementation.md` — slug=`howto-kit-implementation`, 196 lines, mtime 2026-09-08T18:29:30
  - `sprint-feedback-howto-kit-design-brief.md` — slug=`howto-kit-design-brief`, 139 lines, mtime 2026-09-08T18:29:30
  - `sprint-feedback-onboarding-kit-gate-defects.md` — slug=`onboarding-kit-gate-defects`, 152 lines, mtime 2026-09-08T18:28:12
  - `sprint-feedback-harness-amend-direction-baseline-case.md` — slug=`harness-amend-direction-baseline-case`, 120 lines, mtime 2026-09-08T18:28:12
  - `sprint-feedback-antipattern-command-field.md` — slug=`antipattern-command-field`, 152 lines, mtime 2026-09-06T16:07:29
  - `sprint-feedback-harness-attribution-followup.md` — slug=`harness-attribution-followup`, 128 lines, mtime 2026-09-06T15:02:37
  - `sprint-feedback-harness-attribution-followup-v2.md` — slug=`harness-attribution-followup-v2`, 136 lines, mtime 2026-09-06T15:02:37
  - `sprint-feedback-harness-core-defects.md` — slug=`harness-core-defects`, 284 lines, mtime 2026-09-06T13:34:43
  - `sprint-feedback-docs-quality-gates.md` — slug=`docs-quality-gates`, 129 lines, mtime 2026-09-06T13:34:43
  - `sprint-feedback-bambu-kit-enum-allowlist-gate.md` — slug=`bambu-kit-enum-allowlist-gate`, 186 lines, mtime 2026-09-06T13:34:43
  - `sprint-feedback-bambu-seam-policy.md` — slug=`bambu-seam-policy`, 150 lines, mtime 2026-09-06T02:48:11
  - `sprint-feedback-bambu-kit.md` — slug=`bambu-kit`, 132 lines, mtime 2026-09-06T02:48:11
  - `sprint-feedback-tone-kit-framework-vocab.md` — slug=`tone-kit-framework-vocab`, 116 lines, mtime 2026-09-05T14:10:44
  - `sprint-feedback-tone-kit.md` — slug=`tone-kit`, 169 lines, mtime 2026-09-01T18:27:03
  - `sprint-feedback-autofixer-oracle-guards.md` — slug=`autofixer-oracle-guards`, 230 lines, mtime 2026-08-16T13:59:25
  - `sprint-feedback-kaizen-phase9-rust-guards.md` — slug=`kaizen-phase9-rust-guards`, 126 lines, mtime 2026-08-14T19:45:16
  - `sprint-feedback-kaizen-phase8-infra-gate-taxonomy.md` — slug=`kaizen-phase8-infra-gate-taxonomy`, 123 lines, mtime 2026-08-14T19:45:16
  - `sprint-feedback-kaizen-phase7-write-path-integrity.md` — slug=`kaizen-phase7-write-path-integrity`, 147 lines, mtime 2026-08-14T19:45:16
  - `sprint-feedback-kaizen-phase6-variant-decision-gates.md` — slug=`kaizen-phase6-variant-decision-gates`, 154 lines, mtime 2026-08-14T19:45:16
  - `sprint-feedback-kaizen-phase5-flutter-gates.md` — slug=`kaizen-phase5-flutter-gates`, 142 lines, mtime 2026-08-14T19:45:16
  - `sprint-feedback-kaizen-phase4-doc-contract-gates.md` — slug=`kaizen-phase4-doc-contract-gates`, 205 lines, mtime 2026-08-14T19:45:16
  - `sprint-feedback-kaizen-phase3-unverified-triage.md` — slug=`kaizen-phase3-unverified-triage`, 128 lines, mtime 2026-08-14T19:45:16
  - `sprint-feedback-kaizen-phase2-contract-seal.md` — slug=`kaizen-phase2-contract-seal`, 202 lines, mtime 2026-08-14T19:45:16
  - `sprint-feedback-kaizen-phase14-onboarding-facts.md` — slug=`kaizen-phase14-onboarding-facts`, 129 lines, mtime 2026-08-14T19:45:16
  - `sprint-feedback-kaizen-phase13-failure-modes.md` — slug=`kaizen-phase13-failure-modes`, 144 lines, mtime 2026-08-14T19:45:16
  - `sprint-feedback-kaizen-phase12b-oracle-positive-control.md` — slug=`kaizen-phase12b-oracle-positive-control`, 121 lines, mtime 2026-08-14T19:45:16
  - `sprint-feedback-kaizen-phase12a-tag-canonicalization.md` — slug=`kaizen-phase12a-tag-canonicalization`, 134 lines, mtime 2026-08-14T19:45:16
  - `sprint-feedback-kaizen-phase11-planning-facts.md` — slug=`kaizen-phase11-planning-facts`, 95 lines, mtime 2026-08-14T19:45:16
  - `sprint-feedback-kaizen-phase1-design-guides.md` — slug=`kaizen-phase1-design-guides`, 154 lines, mtime 2026-08-14T19:45:16
  - `sprint-feedback-kaizen-memory-integration.md` — slug=`kaizen-memory-integration`, 210 lines, mtime 2026-08-14T19:45:16
  - `sprint-feedback-kaizen-final-2026-08-13.md` — slug=`kaizen-final-2026-08-13`, 114 lines, mtime 2026-08-14T19:45:16
  - `sprint-feedback-visual-styles-modal.md` — slug=`visual-styles-modal`, 71 lines, mtime 2026-04-08T15:06:05
  - `sprint-feedback-task2.md` — slug=`task2`, 70 lines, mtime 2026-04-04T15:10:42
  - `sprint-feedback-task-78.md` — slug=`task-78`, 190 lines, mtime 2026-04-04T15:10:42

<details><summary>sprint-feedback.md 앞부분</summary>

```markdown
# Sprint Feedback
Feature: kaizen/2026-06-11 — Phase 4 harness validate-plugin V8 hook-exec 가드
Evaluated: 2026-06-11 07:00
Verdict: APPROVE
Iteration: 1

## Results

### V8 가드 정확성 (4/4)
- [x] VG-01: `validate-plugin.py --check=hook-exec` 11 plugins OK, Exit 0 — PASS
  - 근거: `Total: 11 plugins, 11 OK / Exit: 0` (명령 직접 실행)
- [x] VG-02: 음성 테스트 chmod -x → FAIL+Exit2 확인, chmod +x 복원 → OK 재확인 — PASS
  - 근거: `mode 0o644 — chmod +x 필요` + Exit:2 → 복원 후 `3 hook 스크립트 실행 가능 — OK`
- [x] VG-03: reflect-kit bash 경유 스크립트 제외(OK) — PASS
  - 근거: `validate-plugin.py reflect-kit --check=hook-exec` → "직접 실행 hook 스크립트 없음 — OK". `scripts/validate-plugin.py:658-659` `_is_direct_exec` False → continue
- [x] VG-04: ast.parse 구문 통과 + CHECK_REGISTRY `hook-exec` 키 존재 — PASS
  - 근거: `syntax OK` + `scripts/validate-plugin.py:697` `"hook-exec": check_v8_hook_exec`

### 카운트 정합성 (3/3)
- [x] CC-01: 4개 파일 전부 8/V1~V8 갱신 확인 — PASS
```

</details>

<details><summary>sprint-feedback-plugin-validation-page-sync.md 앞부분</summary>

```markdown
# Sprint Feedback
Feature: plugin-validation 문서 페이지를 기준 문서 1.3 판에 맞춰 다시 만들기
Evaluated: 2026-09-24 15:05
Verdict: APPROVE
Iteration: 3

## Contract Fingerprint
- path: /Users/jackson/Hub/10_Dev/claude-plugins/.harness/sprint-contract-plugin-validation-page-sync.md
- sha256: 1fa298876c38a8c669c9faf4c7c33912d72df59d2d29cd1f76b593e1130d1e08
- status: done (Iteration 2에서 이미 전환)
- slug: plugin-validation-page-sync
- contract_root: /Users/jackson/Hub/10_Dev/claude-plugins
- contract_root_unconfigured: false
- 선택 근거: ladder 1 (명시 경로, 부모가 절대경로로 직접 지정)
- legacy_contract_used: false
- seal_status: SEAL_OK (recorded=actual=0c84c3f3266af6ec)
- seal_commit: 2a190d7 (계약 파일 단독 · 1 file changed, 204 insertions)
- 봉인 커밋 대조: status 전환(active→done) 외 산문·조건 변경 없음. conditions_digest 불변
- 재확인(Step 5): 일치 (SHA·status 저장 직전까지 불변)
- status_transition: skipped (verdict=APPROVE 이지만 status 가 이미 done — Iteration 2에서 전환 완료, 재전환 불필요)
```

</details>

<details><summary>sprint-feedback-check-count-decouple-and-table-gate.md 앞부분</summary>

```markdown
# Sprint Feedback
Feature: 검사 개수를 지시문에서 떼어내고 표 무결성 검사를 추가
Evaluated: 2026-09-24 13:20
Verdict: APPROVE
Iteration: 4

## Contract Fingerprint
- path: /Users/jackson/Hub/10_Dev/claude-plugins/.harness/sprint-contract-check-count-decouple-and-table-gate.md
- sha256: 074c59853f26389e9360f9eb96db518683bc362516951df0dea8f8ca9dde673b
- status: done (iteration 2 APPROVE 때 이미 전환됨 — 이번 재평가로 새로 바꾸지 않는다)
- slug: check-count-decouple-and-table-gate
- contract_root: /Users/jackson/Hub/10_Dev/claude-plugins
- contract_root_unconfigured: false
- 선택 근거: 사용자가 계약 절대경로를 명시 (ladder 1)
- legacy_contract_used: false
- seal_status: SEAL_OK
- contract_seal_broken: n/a
- 재확인(Step 5): 일치 (평가 시작·종료 시점 sha256 동일: 074c5985...)
- 봉인 커밋 대조(1-e-3): 봉인 커밋 2ae9794 대비 diff는 frontmatter `status: active -> done`
  한 줄뿐. 조건 줄·산문 전부 봉인 시점과 동일. `reseal_detected: false`
```

</details>

<details><summary>sprint-feedback-seal-commit-and-evidence-boundary.md 앞부분</summary>

```markdown
# Sprint Feedback
Feature: 봉인 시점 원문을 커밋으로 남기고 근거 경계를 한 기준으로 정리
Evaluated: 2026-09-24 10:11
Verdict: APPROVE
Iteration: 1

## Contract Fingerprint
- path: /Users/jackson/Hub/10_Dev/claude-plugins/.harness/sprint-contract-seal-commit-and-evidence-boundary.md
- sha256: d642ef4a512eafb550fb25846ebf6e0460c19986fe3bd623090a85effa8d027e
- status: active
- slug: seal-commit-and-evidence-boundary
- contract_root: /Users/jackson/Hub/10_Dev/claude-plugins
- contract_root_unconfigured: false
- 선택 근거: ladder 1 명시경로 (동시에 ladder 2 세션소유와도 일치 — owner_session == CLAUDE_CODE_SESSION_ID)
- legacy_contract_used: false
- seal_status: SEAL_OK
- contract_seal_broken: n/a
- 재확인(Step 5): 일치
- status_transition: active -> done

```

</details>

<details><summary>sprint-feedback-bambu-kit-gate-unread-slot-report.md 앞부분</summary>

```markdown
# Sprint Feedback
Feature: bambu-kit 완료 검사 — 못 읽은 슬롯을 네 검사 모두 알리게
Evaluated: 2026-09-23 12:18
Verdict: APPROVE
Iteration: 1

## Contract Fingerprint
- path: /Users/jackson/Hub/10_Dev/claude-plugins/.harness/sprint-contract-bambu-kit-gate-unread-slot-report.md
- sha256: f1d97fbbefa57d15364790c1ed6fc57cc82de649e1d646d84c7dac5612c80c47
- status: active
- slug: bambu-kit-gate-unread-slot-report
- contract_root: /Users/jackson/Hub/10_Dev/claude-plugins
- contract_root_unconfigured: false
- 선택 근거: ladder 1 명시경로 (호출 프롬프트가 계약 경로를 직접 지정)
- legacy_contract_used: false
- seal_status: SEAL_OK (recorded=actual=contract_digest, 18개 조건 줄 기준)
- contract_seal_broken: n/a
- 재확인(Step 5): 일치 (저장 직전 sha256·status 동일)
- status_transition: active -> done (아래 절차로 전환)

```

</details>
- (본문 미리보기는 최신 5개만 표시 — 나머지 65개는 위 파일별 내역 참조)

### `fit-pal`

- 경로: `/Users/jackson/Hub/10_Dev/fit-pal`
- sprint-feedback 파일: 2개 (총 267 lines)
- history sprint-contracts: 37
- 접미형 슬러그: `invite-link-android`
- 최근 contracts:
  - 20260623-1118-sprint-contract.md
  - 20260625-1850-sprint-contract.md
  - 20260626-1507-sprint-contract.md
  - 20260723-1444-sprint-contract.md
  - 20260727-1812-sprint-contract.md
- 파일별 내역:
  - `sprint-feedback.md` — plain (슬러그 없음), 121 lines, mtime 2026-07-27T19:10:10
  - `sprint-feedback-invite-link-android.md` — slug=`invite-link-android`, 146 lines, mtime 2026-09-24T15:32:39

<details><summary>sprint-feedback.md 앞부분</summary>

```markdown
# Sprint Feedback
Feature: 루틴 없음=404→200 빈응답 + FCM 토큰 PUT 멱등화(409 근절)
Evaluated: 2026-07-27 19:45
Verdict: APPROVE
Iteration: 2

## Results

### UI (2/2)

- [x] UI-01: 루틴 없는 그룹의 스케줄 화면이 에러 배너/토스트 없이 "루틴 없음" 빈 상태를 표시한다 — PASS [정적, fallback L3]
  - 근거: `schedule_screen.dart:252-267` — `ref.listen(routineDetailProvider(g.id), ...)` 는 `next.hasError == true` 일 때만 `errorProvider.notifier.show(...)` 호출. `AsyncValue.data(null)` 은 `hasError == false` 이므로 배너 미발화. `routine_section.dart:65-67` — `data: (routine) { if (routine == null) return _RoutineEmpty(...); }` — 빈 상태 위젯 렌더, 에러 경로 없음.
  - MCP 미수행 사유: 프로젝트 root `project.yaml.runtime_inspection.mcp_server: null`. 3단계 fallback 중 단계2(정적 검증)를 소비자 위젯 레벨(schedule_screen/routine_section)까지 추적해 실행.

- [x] UI-02: 루틴 있는 그룹은 기존과 동일하게 루틴이 표시된다(회귀 없음) — PASS [정적]
  - 근거: `routine_section.dart:68-72` — `data: (routine) { ...; return builder(context, routine); }` non-null 분기 동작 불변. `LG-02`(nullable 체인)가 non-null 경우 `model?.toEntity() == model.toEntity()`로 동일 동작.

### Logic (7/7)

- [x] LG-01: 서버 GET /groups/{id}/routine 이 (활성 멤버 + 루틴 없음)일 때 HTTP 200 + body null — PASS [exact]
```

</details>

<details><summary>sprint-feedback-invite-link-android.md 앞부분</summary>

```markdown
# Sprint Feedback
Feature: 초대 링크 — 안드로이드 링크 열기 시험 설정 + 실기 시나리오
Evaluated: 2026-09-24 15:40
Verdict: APPROVE
Iteration: 1

## Contract Fingerprint
- path: .harness/sprint-contract-invite-link-android.md
- sha256: 5b6014a986d98e07d0c918ef0d510c2e62115b94ff9a6b2594592eb53edc72c1
- status: active (→ done, 본 평가 직후 전환)
- slug: invite-link-android
- contract_root: /Users/jackson/Hub/10_Dev/fit-pal
- contract_root_unconfigured: false
- 선택 근거: ladder 1 (명시경로)
- legacy_contract_used: false
- seal_status: SEAL_OK (recorded=154d8387007000b1, actual=154d8387007000b1)
- contract_seal_broken: n/a
- seal_commit: fd4d72a8 (계약 파일 1개만 담긴 단독 커밋, git diff 봉인커밋 대비 조건 줄·산문 0건 변경)
- 재확인(Step 5): 일치
- status_transition: active -> done (아래 실행)
```

</details>

### `fit-pal/app`

- 경로: `/Users/jackson/Hub/10_Dev/fit-pal/app`
- sprint-feedback 파일: 36개 (총 5693 lines)
- history sprint-contracts: 49
- 접미형 슬러그: `player-howto-custom`, `history-session-row`, `history-stock-select`, `post-card-mockups`, `chat-reply-stacked`, `aqua-cta-tone`, `history-stock-guide`, `history-stock-axis`, `history-stock-total`, `history-stock-refine`, `history-stock-delta`, `history-record-graph`, `chat-send-morph-gt`, `chat-send-morph`, `chat-tray-mockups`, `app-post-like-notification`, `history-mockups-round2`, `history-screen-mockups`, `group-chip-thumb-triangle`, `chat-bubble-mockups`, `timer-autocomplete-record`, `player-session-ux`, `dev-baseurl-override`, `bodymap`, `figma-box-path-shape`, `statistics-tab`, `statistics-aggregation`, `statistics-catalog`, `notif-reliability`, `ws6-carryover`, `emoji-picker`, `workout-sync-utc`, `s6`, `s8`, `player-launch`
- 최근 contracts:
  - 20260714-1613-sprint-contract.md
  - 20260716-1822-sprint-contract.md
  - 20260721-1026-sprint-contract.md
  - 20260723-1453-sprint-contract.md
  - 20260723-1809-sprint-contract.md
- 파일별 내역:
  - `sprint-feedback.md` — plain (슬러그 없음), 71 lines, mtime 2026-07-24T20:48:28
  - `sprint-feedback-player-howto-custom.md` — slug=`player-howto-custom`, 136 lines, mtime 2026-09-24T12:54:12
  - `sprint-feedback-history-session-row.md` — slug=`history-session-row`, 236 lines, mtime 2026-08-19T13:37:24
  - `sprint-feedback-history-stock-select.md` — slug=`history-stock-select`, 219 lines, mtime 2026-08-14T14:11:50
  - `sprint-feedback-post-card-mockups.md` — slug=`post-card-mockups`, 178 lines, mtime 2026-08-14T11:57:32
  - `sprint-feedback-chat-reply-stacked.md` — slug=`chat-reply-stacked`, 87 lines, mtime 2026-08-14T11:50:00
  - `sprint-feedback-aqua-cta-tone.md` — slug=`aqua-cta-tone`, 292 lines, mtime 2026-08-14T11:44:59
  - `sprint-feedback-history-stock-guide.md` — slug=`history-stock-guide`, 175 lines, mtime 2026-08-14T11:23:49
  - `sprint-feedback-history-stock-axis.md` — slug=`history-stock-axis`, 167 lines, mtime 2026-08-14T11:11:13
  - `sprint-feedback-history-stock-total.md` — slug=`history-stock-total`, 255 lines, mtime 2026-08-13T21:09:38
  - `sprint-feedback-history-stock-refine.md` — slug=`history-stock-refine`, 103 lines, mtime 2026-08-13T19:27:27
  - `sprint-feedback-history-stock-delta.md` — slug=`history-stock-delta`, 109 lines, mtime 2026-08-13T18:37:37
  - `sprint-feedback-history-record-graph.md` — slug=`history-record-graph`, 184 lines, mtime 2026-08-13T18:22:29
  - `sprint-feedback-chat-send-morph-gt.md` — slug=`chat-send-morph-gt`, 127 lines, mtime 2026-08-13T17:21:59
  - `sprint-feedback-chat-send-morph.md` — slug=`chat-send-morph`, 155 lines, mtime 2026-08-13T16:13:17
  - `sprint-feedback-chat-tray-mockups.md` — slug=`chat-tray-mockups`, 167 lines, mtime 2026-08-13T15:00:12
  - `sprint-feedback-app-post-like-notification.md` — slug=`app-post-like-notification`, 174 lines, mtime 2026-08-13T14:34:51
  - `sprint-feedback-history-mockups-round2.md` — slug=`history-mockups-round2`, 103 lines, mtime 2026-08-13T12:20:06
  - `sprint-feedback-history-screen-mockups.md` — slug=`history-screen-mockups`, 109 lines, mtime 2026-08-13T10:19:29
  - `sprint-feedback-group-chip-thumb-triangle.md` — slug=`group-chip-thumb-triangle`, 145 lines, mtime 2026-08-12T20:18:44
  - `sprint-feedback-chat-bubble-mockups.md` — slug=`chat-bubble-mockups`, 237 lines, mtime 2026-08-12T18:27:22
  - `sprint-feedback-timer-autocomplete-record.md` — slug=`timer-autocomplete-record`, 198 lines, mtime 2026-08-12T14:54:49
  - `sprint-feedback-player-session-ux.md` — slug=`player-session-ux`, 330 lines, mtime 2026-08-12T13:14:57
  - `sprint-feedback-dev-baseurl-override.md` — slug=`dev-baseurl-override`, 103 lines, mtime 2026-08-12T12:19:27
  - `sprint-feedback-bodymap.md` — slug=`bodymap`, 258 lines, mtime 2026-08-11T20:38:28
  - `sprint-feedback-figma-box-path-shape.md` — slug=`figma-box-path-shape`, 190 lines, mtime 2026-08-11T19:12:05
  - `sprint-feedback-statistics-tab.md` — slug=`statistics-tab`, 120 lines, mtime 2026-08-11T18:15:52
  - `sprint-feedback-statistics-aggregation.md` — slug=`statistics-aggregation`, 242 lines, mtime 2026-08-04T18:27:18
  - `sprint-feedback-statistics-catalog.md` — slug=`statistics-catalog`, 290 lines, mtime 2026-08-02T15:03:38
  - `sprint-feedback-notif-reliability.md` — slug=`notif-reliability`, 76 lines, mtime 2026-07-13T16:37:26
  - `sprint-feedback-ws6-carryover.md` — slug=`ws6-carryover`, 84 lines, mtime 2026-07-13T14:51:33
  - `sprint-feedback-emoji-picker.md` — slug=`emoji-picker`, 30 lines, mtime 2026-07-12T16:01:27
  - `sprint-feedback-workout-sync-utc.md` — slug=`workout-sync-utc`, 85 lines, mtime 2026-07-12T14:24:59
  - `sprint-feedback-s6.md` — slug=`s6`, 104 lines, mtime 2026-07-12T14:24:59
  - `sprint-feedback-s8.md` — slug=`s8`, 76 lines, mtime 2026-07-11T19:34:56
  - `sprint-feedback-player-launch.md` — slug=`player-launch`, 78 lines, mtime 2026-07-11T19:34:56

<details><summary>sprint-feedback.md 앞부분</summary>

```markdown
# Sprint Feedback
Feature: 운동 플레이어 FAB 재진입 수정 + 첫 시작 화면/기록방식 탭바/하단 transport 재설계
Evaluated: 2026-07-24
Verdict: APPROVE
Iteration: 1

## Results

### UI (4/4)
- [x] UI-01: 빈 화면에 제목 + 안내 아이콘 + primary 버튼 — PASS
  - 근거: `routine_player_body.dart:258-351` — `activeSessionProvider.select(session?.title)` Text(307-318행), MetalSurface.neutral 88원형 + dumbbell 아이콘(295-303행), IFButton '운동 추가'(329-352행). 세 요소 모두 존재.
- [x] UI-02: 기록방식 탭바 IFSlidingTabBar 재사용 — PASS
  - 근거: `routine_player_body.dart:32` import + `routine_player_body.dart:1171-1179` `SizedBox(height:48, child: IFSlidingTabBar(...))`.
- [x] UI-03: 하단 transport 균형 — PASS
  - 근거: `routine_player_body.dart:1606-1679` `_buildTransport` — Row[_skip, WeakAquaButton 52원형, Expanded(IFButton height:56 ✓), _skip]. Expanded IFButton이 폭을 채움.
- [x] UI-04: 세트 완료 ✓ 하단 통합, 휠 옆 제거 — PASS
  - 근거: git diff `-WeakAquaButton`(이전 787행 휠 내부) 제거 확인. 현재 WeakAquaButton은 1619행(transport 재생/일시정지)만 1건. `onCompleteSet`/`canCompleteSet` 파라미터 하단 CTA 추가(1513-1533행).

### Logic (4/4)
- [x] LG-01: FAB 연타 시 시트 최대 1개 — PASS
```

</details>

<details><summary>sprint-feedback-player-howto-custom.md 앞부분</summary>

```markdown
# Sprint Feedback
Feature: 플레이어 사용법 3 장 — 커스텀 만들기까지 저절로 도는 미리보기
Evaluated: 2026-09-24 13:20
Verdict: APPROVE
Iteration: 1

## Contract Fingerprint
- path: /Users/jackson/Hub/10_Dev/fit-pal/app/.harness/sprint-contract-player-howto-custom.md
- sha256: 77669e74a23113f3977dbf654e87d051133261236b282822a6b74d49e93743fe
- status: active (평가 후 done 으로 전환, 아래 status_transition 참조)
- slug: player-howto-custom
- contract_root: /Users/jackson/Hub/10_Dev/fit-pal/app
- contract_root_unconfigured: false
- 선택 근거: ladder 1 (사용자가 절대경로를 명시) — 2 단계(세션 소유)로도 동일 결과(owner_session 이 이 세션과 일치)
- legacy_contract_used: false
- seal_status: SEAL_OK
- seal_commit: bf2286a6 (mixed, 계약+구현 9 파일 — 이 계약이 git 에 처음 들어온 커밋이자 유일 커밋. 사전 판본이 없어 재봉인 위험 없음. 조건 줄 해시는 지금 파일 내용과 직접 일치 확인(SEAL_OK)됨)
- contract_seal_broken: n/a
- 재확인(Step 5): 일치
- status_transition: active -> done (아래 참조)
```

</details>

<details><summary>sprint-feedback-history-session-row.md 앞부분</summary>

```markdown
# Sprint Feedback
Feature: 히스토리 세션 행 디자인 비교판
Evaluated: 2026-08-13 15:10
Verdict: REJECT
Iteration: 2

## Contract Fingerprint
- path: /Users/jackson/Hub/10_Dev/fit-pal/app/.harness/sprint-contract-history-session-row.md
- sha256: 648e215aa45ec9cbca550a4eefa6d2e8a6cc7d35f3667529f3b4c8c952d653d5
- status: active
- slug: history-session-row
- contract_root: /Users/jackson/Hub/10_Dev/fit-pal/app
- contract_root_unconfigured: false
- 선택 근거: ladder 1 명시경로 (호출 시 경로 명시, owner_session == CLAUDE_CODE_SESSION_ID 로 교차검증)
- legacy_contract_used: false
- 재확인(Step 5): 일치 (sha256/status 저장 직전 재계산 동일)
- status_transition: skipped (verdict=REJECT — active 유지, 재평가 대상)

## Amendments
- amendments: 0 (사이드카 `sprint-amendments-history-session-row.md` 없음)
```

</details>

<details><summary>sprint-feedback-history-stock-select.md 앞부분</summary>

```markdown
# Sprint Feedback
Feature: S-A 행 선택 — 하이라이트 · 곡선 전환 애니메이션
Evaluated: 2026-08-14 14:15
Verdict: APPROVE
Iteration: 2

## Contract Fingerprint
- path: /Users/jackson/Hub/10_Dev/fit-pal/app/.harness/sprint-contract-history-stock-select.md
- sha256: 6c653a10dd75087421d513e71c97f0d8045160c095c442da9ac92b77b9860883
- status: active
- slug: history-stock-select
- contract_root: /Users/jackson/Hub/10_Dev/fit-pal/app
- contract_root_unconfigured: false
- 선택 근거: ladder 1 (명시 경로 — 평가 요청에 계약 절대경로가 직접 지정됨, `test -f` 확인 통과)
- legacy_contract_used: false
- 재확인(Step 5): 일치 (sha256/status 동일, 평가 종료 시점 재확인)
- status_transition: active -> done (verdict=APPROVE)

## Amendments
- amendments: 0 (`.harness/sprint-amendments-history-stock-select.md` 없음)
```

</details>

<details><summary>sprint-feedback-post-card-mockups.md 앞부분</summary>

```markdown
# Sprint Feedback
Feature: 포스트 시안 — 아키타입 6 종 확정 + 레이아웃 조판 축 6 타일
Evaluated: 2026-08-14 11:56
Verdict: APPROVE
Iteration: 1

## Contract Fingerprint
- path: /Users/jackson/Hub/10_Dev/fit-pal/app/.harness/sprint-contract-post-card-mockups.md
- sha256: 9f965ec5fa633d7b18be8c0dbe25424cb8bba7da16c135b47969ce2d539e2daf
- status(선택 시점): active
- slug: post-card-mockups
- contract_root: /Users/jackson/Hub/10_Dev/fit-pal/app
- contract_root_unconfigured: false
- 선택 근거: ladder 2 (세션 소유 — owner_session == $CLAUDE_CODE_SESSION_ID, 명시 경로와도 일치)
- legacy_contract_used: false
- 재확인(Step 5): 일치 (FINGERPRINT OK, 저장 직전 재확인 완료)
- status_transition: active -> done

## Amendments
- amendments: 4 (A-01~A-04)
```

</details>
- (본문 미리보기는 최신 5개만 표시 — 나머지 31개는 위 파일별 내역 참조)

### `fit-pal/server`

- 경로: `/Users/jackson/Hub/10_Dev/fit-pal/server`
- sprint-feedback 파일: 9개 (총 1354 lines)
- history sprint-contracts: 29
- 접미형 슬러그: `social-feed-likes`, `legacy-exercise-id-backfill`, `social-feed-read`, `social-feed-media-dimensions`, `personal-records`, `muscle-share`, `custom-exercise-owned`, `exercise-muscle-map`
- 최근 contracts:
  - 20260703-2146-sprint-contract.md
  - 20260706-1407-sprint-contract.md
  - 20260706-1447-sprint-contract.md
  - 20260723-2206-sprint-contract.md
  - 20260723-2353-sprint-contract.md
- 파일별 내역:
  - `sprint-feedback.md` — plain (슬러그 없음), 73 lines, mtime 2026-07-24T00:03:28
  - `sprint-feedback-social-feed-likes.md` — slug=`social-feed-likes`, 312 lines, mtime 2026-08-13T13:45:50
  - `sprint-feedback-legacy-exercise-id-backfill.md` — slug=`legacy-exercise-id-backfill`, 130 lines, mtime 2026-08-12T20:48:32
  - `sprint-feedback-social-feed-read.md` — slug=`social-feed-read`, 232 lines, mtime 2026-08-12T20:13:47
  - `sprint-feedback-social-feed-media-dimensions.md` — slug=`social-feed-media-dimensions`, 116 lines, mtime 2026-08-12T17:46:24
  - `sprint-feedback-personal-records.md` — slug=`personal-records`, 116 lines, mtime 2026-08-12T15:51:55
  - `sprint-feedback-muscle-share.md` — slug=`muscle-share`, 134 lines, mtime 2026-08-11T19:32:50
  - `sprint-feedback-custom-exercise-owned.md` — slug=`custom-exercise-owned`, 124 lines, mtime 2026-08-09T16:25:39
  - `sprint-feedback-exercise-muscle-map.md` — slug=`exercise-muscle-map`, 117 lines, mtime 2026-08-09T15:03:36

<details><summary>sprint-feedback.md 앞부분</summary>

```markdown
# Sprint Feedback
Feature: app_minimum_versions 시드 마이그레이션 (ios/android)
Evaluated: 2026-07-24 00:10
Verdict: APPROVE
Iteration: 1

## Results

### API (1/1)
- [x] API-01: 마이그레이션 적용 후 `GET /api/v1/app-version/check?platform=ios`(및 android)가 200(update_required=false)을 반환한다 — PASS [정적]
  - 근거(DB 직접 확인): `docker exec server-postgres-1 psql -U fitpal -d fitpal` → `ios | 0.0.1 | 1`, `android | 0.0.1 | 1` 2행 존재 확인
  - 근거(코드 경로 L3): `modules/app-version/src/service.rs:40-48` — row 없으면 `AppError::NotFound` → HTTP 404, row 있으면 버전 비교 후 200 반환. `min_version='0.0.1'`이면 클라이언트 버전 ≥ 0.0.1인 경우 update_required=false
  - 서버 미실행으로 curl 직접 확인 불가. 3단계 fallback 단계 2(정적 검증)로 판정
  - 검증 깊이: L3 도달 (DB 직접 쿼리 + 코드 경로 추적)

### Data (2/2)
- [x] DA-01: `app_minimum_versions`에 platform='ios'와 'android' row가 각각 min_version='0.0.1', min_build_number=1로 시드된다 — PASS (enumerated 2개 전수 확인)
  - 근거(ios): `docker exec server-postgres-1 psql -U fitpal -d fitpal -c "SELECT platform, min_version, min_build_number FROM app_minimum_versions"` → `ios | 0.0.1 | 1` 확인
  - 근거(android): 동일 쿼리 → `android | 0.0.1 | 1` 확인
  - 검증 깊이: L3 도달 (DB 직접 쿼리 + 값 정확성 확인)
```

</details>

<details><summary>sprint-feedback-social-feed-likes.md 앞부분</summary>

```markdown
# Sprint Feedback
Feature: 소셜 피드 S4a — 좋아요
Evaluated: 2026-08-13 13:50
Verdict: APPROVE
Iteration: 1

## Contract Fingerprint
- path: /Users/jackson/Hub/10_Dev/fit-pal/server/.harness/sprint-contract-social-feed-likes.md
- sha256: 457028d726f59b56b601b59608015ba9e092206e077a06a2cadb386979ad601d
- status: active
- slug: social-feed-likes
- contract_root: /Users/jackson/Hub/10_Dev/fit-pal/server
- contract_root_unconfigured: false
- 선택 근거: ladder 1 명시경로 (평가 대상이 프롬프트에서 절대경로로 고정됨, 후보 열거 결과와도
  일치 — active 후보 유일 1개)
- legacy_contract_used: false
- 재확인(Step 5): 일치 (sha256/status 불변)
- status_transition: active -> done (아래 Step 5.5 참조)

## Amendments
```

</details>

<details><summary>sprint-feedback-legacy-exercise-id-backfill.md 앞부분</summary>

```markdown
# Sprint Feedback
Feature: 과거 운동 기록의 exercise_id 이름 기반 백필
Evaluated: 2026-08-12 21:15
Verdict: APPROVE
Iteration: 3

## Contract Fingerprint
- path: /Users/jackson/Hub/10_Dev/fit-pal/server/.harness/sprint-contract-legacy-exercise-id-backfill.md
- sha256: 961ee163945429482a3bbb9bc5d98addb5007eebbd076195f08a8bc3b704db7b
- status: active (평가 시점) → done (Step 5.5 전환)
- slug: legacy-exercise-id-backfill
- contract_root: /Users/jackson/Hub/10_Dev/fit-pal/server
- contract_root_unconfigured: false
- 선택 근거: ladder 1 명시경로 (사용자가 절대경로로 지정, test -f 로 존재 확인)
- legacy_contract_used: false
- 재확인(Step 5): 일치 (sha256/status 동일, 저장 직전 재해시 961ee1639...b704db7b == 원본)
- status_transition: active -> done (verdict=APPROVE)

## Amendments
- amendments: 1 (A-01, **WITHDRAWN** — 사이드카 본문에 명시)
```

</details>

<details><summary>sprint-feedback-social-feed-read.md 앞부분</summary>

```markdown
# Sprint Feedback
Feature: 소셜 피드 S3 — 피드 읽기
Evaluated: 2026-08-12 20:12
Verdict: APPROVE
Iteration: 2

## Contract Fingerprint
- path: /Users/jackson/Hub/10_Dev/fit-pal/server/.harness/sprint-contract-social-feed-read.md
- sha256: 15195cda24c1c43a6e25801e5e4f37ca25c3363892b8061ba39e14288e2d260b
- status: active
- slug: social-feed-read
- contract_root: /Users/jackson/Hub/10_Dev/fit-pal/server
- contract_root_unconfigured: false
- 선택 근거: ladder 1 명시경로 (호출 인자로 절대경로 지정됨)
- legacy_contract_used: false
- 재확인(Step 5): 일치 (sha256 재계산 동일, status 여전히 active)
- status_transition: active -> done (verdict=APPROVE)

## Amendments
- amendments: 4 (A-01, A-02, A-03, A-04)
```

</details>

<details><summary>sprint-feedback-social-feed-media-dimensions.md 앞부분</summary>

```markdown
# Sprint Feedback
Feature: 소셜 피드 A-04 — 업로드 이미지 실측 치수
Evaluated: 2026-08-12 17:45
Verdict: APPROVE
Iteration: 1

## Contract Fingerprint
- path: /Users/jackson/Hub/10_Dev/fit-pal/server/.harness/sprint-contract-social-feed-media-dimensions.md
- sha256: 4ff98d7da46b73c3cffe6f7a0a4912b935d3940d1b834d7da0ef483537f9162b
- status: active (판정 완료 후 done 으로 전환)
- slug: social-feed-media-dimensions
- contract_root: /Users/jackson/Hub/10_Dev/fit-pal/server
- contract_root_unconfigured: false
- 선택 근거: ladder 1 명시경로 (호출 인자로 지정된 절대경로, 존재 확인 완료) — 세션소유(owner_session)도 일치
- legacy_contract_used: false
- 재확인(Step 5): 일치 (sha256/status 동일, TOCTOU 없음)
- status_transition: active -> done

## Amendments
- amendments: 0 (사이드카 파일 없음)
```

</details>
- (본문 미리보기는 최신 5개만 표시 — 나머지 4개는 위 파일별 내역 참조)

### `fit-pal-solo`

- 경로: `/Users/jackson/Hub/10_Dev/fit-pal-solo`
- sprint-feedback 파일: 1개 (총 56 lines)
- history sprint-contracts: 23
- 최근 contracts:
  - 20260603-1520-sprint-contract.md
  - 20260603-server-plan1-sprint-contract.md
  - 20260610-1537-member-manage-sprint-contract.md
  - 20260611-0919-server-authz-sprint-contract.md
  - 20260611-1300-server-m5-storage-sprint-contract.md
- 파일별 내역:
  - `sprint-feedback.md` — plain (슬러그 없음), 56 lines, mtime 2026-07-29T13:38:12

<details><summary>sprint-feedback.md 앞부분</summary>

```markdown
# Sprint Feedback
Feature: force_resolve 이중 resolve 방지 가드
Evaluated: 2026-07-03 21:10
Verdict: APPROVE
Iteration: 1

## Results

### API (1/1)
- [x] API-01: 성공 응답 스키마 무변경 + 409 Conflict 반환 — PASS
  - 근거: `server/modules/schedule/src/service.rs:712-718` force_skip/force_held → `Result<SlotResponse, AppError>` 시그니처 유지. `git diff --stat` 결과 service.rs 1파일만 변경, router.rs/dto.rs 무변경. 409 경로: 서비스 내 `AppError::Conflict` → 기존 Axum error handler에서 409 매핑.

### Logic (2/2)
- [x] LG-01: rows_affected==0 경로에서 advance/dispatch 미호출 검증 — PASS
  - 근거: `service.rs:1514-1561` 신규 테스트 `force_resolve_lost_race_returns_conflict_without_advance_or_dispatch`. MockDatabase `rows_affected:0` 시 `advance.call_count()==0`, `notification.calls.len()==0` 두 assert 통과. `cargo test` 64/64 passed.
- [x] LG-02: 승리 경로 기존 동작 보존 — PASS
  - 근거: `service.rs:1008-1031`. rows_affected==1 통과 후 → Held 시 `self.routine_advance.advance(source_id)`, 전원 `self.notification.dispatch`. `force_held_writes_snapshot_and_calls_advance`(advance.call_count()==1), `force_skip_writes_null_snapshot_and_does_not_advance`(advance==0) 기존 테스트 계속 통과.

### Error (1/1)
- [x] ER-01: `AppError::Conflict` + `schedule.slot_already_resolved` 키, DB write 시점 최종 확정 — PASS
```

</details>

### `fit-pal-solo/app`

- 경로: `/Users/jackson/Hub/10_Dev/fit-pal-solo/app`
- sprint-feedback 파일: 8개 (총 597 lines)
- history sprint-contracts: 30
- 접미형 슬러그: `ws6-carryover`, `workout-sync-utc`, `s8`, `s6`, `player-launch`, `notif-reliability`, `emoji-picker`
- 최근 contracts:
  - 20260609-1549-sprint-contract.md
  - 20260609-1640-darkmetal-sprint-contract.md
  - 20260611-1955-track6-uri-mask-sprint-contract.md
  - 20260612-1726-sprint-contract.md
  - 20260625-1516-sprint-contract.md
- 파일별 내역:
  - `sprint-feedback.md` — plain (슬러그 없음), 64 lines, mtime 2026-07-29T13:38:12
  - `sprint-feedback-ws6-carryover.md` — slug=`ws6-carryover`, 84 lines, mtime 2026-07-29T13:38:12
  - `sprint-feedback-workout-sync-utc.md` — slug=`workout-sync-utc`, 85 lines, mtime 2026-07-29T13:38:12
  - `sprint-feedback-s8.md` — slug=`s8`, 76 lines, mtime 2026-07-29T13:38:12
  - `sprint-feedback-s6.md` — slug=`s6`, 104 lines, mtime 2026-07-29T13:38:12
  - `sprint-feedback-player-launch.md` — slug=`player-launch`, 78 lines, mtime 2026-07-29T13:38:12
  - `sprint-feedback-notif-reliability.md` — slug=`notif-reliability`, 76 lines, mtime 2026-07-29T13:38:12
  - `sprint-feedback-emoji-picker.md` — slug=`emoji-picker`, 30 lines, mtime 2026-07-29T13:38:12

<details><summary>sprint-feedback.md 앞부분</summary>

```markdown
# Sprint Feedback
Feature: 그룹 상세 UI 재설계 (MeetingScheduleCard 공휴일 열 · IFSectionHeader · _NextRoutineLine · FCM microtask)
Evaluated: 2026-07-22 12:00
Verdict: APPROVE
Iteration: 1

## Results

### DoD (10/10)

- [x] DoD-1: HolidayPolicyMode 3분기 + 공휴일 헤더 i18n-safe 아이콘 + 44px 고정폭 열 — PASS
  - 근거: `meeting_schedule_card.dart:135-148` — switch로 rest/asUsual/specialTime 분기. specialTime 합성 행 추가 구현. `_HolidayCell:224` — `SizedBox(width: 44)` 고정폭. 헤더: `Semantics(label: context.t.group.holidayColumn, child: IFIcon.embossed(LucideIcons.calendarOff, ...))` (line 180-189). Expanded 요일 셀 + 고정 HolidayCell 구조라 RenderFlex overflow 없음.

- [x] DoD-2: 빈 점 = 보더 없이 overlayMedium 채움 / 활성 점 = accentColor / 공휴일 점 = statusDanger — PASS
  - 근거: `meeting_schedule_card.dart:277-285` — `_Dot.build()`: `BoxDecoration(shape: BoxShape.circle, color: active ? activeColor : colors.overlayMedium)`. border 프로퍼티 없음. 공휴일 점: `_BlockRow:334` — `_Dot(active: holiday, activeColor: colors.statusDanger)`. 활성: `accentColor ?? context.colorScheme.primary` (line 307).

- [x] DoD-3: 공휴일/요일 구분선 = 양각 세로 divider, IFDividerTokens alpha 사용, raw alpha 리터럴 없음 — PASS
  - 근거: `meeting_schedule_card.dart:232-263` — `_VDivider`가 그림자(`IFDividerTokens.shadowDefaultAlphaDark/Light`)·하이라이트(`IFDividerTokens.highlightAlphaDark/Light`) 토큰만 사용. raw 숫자 alpha 리터럴 0건.

- [x] DoD-4: 섹션 헤더 = `IFDivider.red()`, 섹션간 독립 gradient divider 제거, Members = `IFSectionHeader` 승격 — PASS
```

</details>

<details><summary>sprint-feedback-ws6-carryover.md 앞부분</summary>

```markdown
# Sprint Feedback
Feature: WS-6 이월(carryover) 정책 — 미투표/모두 불참 회차는 루틴 순서를 넘기지 않는다
Evaluated: 2026-07-13 10:30
Verdict: APPROVE
Iteration: 1

## Results

### Server Logic (5/5)

- [x] SV-01: SkipPolicy DTO에 `#[serde(default)] carry_over: bool` 추가 — PASS
  - 근거: `server/modules/routine/src/dto.rs:118` — `#[serde(default)] pub carry_over: bool` 확인. `SkipPolicy` 구조체에 JSONB 기반 default 주석과 함께 정확히 추가됨. 구버전 행 역직렬화 대비 `serde(default)` 적용 확인. (L3 달성)

- [x] SV-02: `resolution::carry_over_outcome(outcome, votes, carry_over)` 순수 함수 — PASS
  - 근거: `server/modules/schedule/src/resolution.rs:113-127`. 함수 시그니처 `carry_over_outcome(outcome: SlotOutcome, votes: &[(Uuid, VoteChoice)], carry_over: bool) -> SlotOutcome` 정확. 로직: `!carry_over || outcome == Skipped` → passthrough; `has_attendance` true → 원 outcome; `has_attendance` false → `Skipped` 강등. 정확히 "carry_over && 참석 0건이면 Held→Skipped, 그 외 passthrough". 5개 유닛 테스트 직접 실행: `cargo test -p fitpal-schedule --lib carry_over` → 5 passed 확인. (L3 달성)

- [x] SV-03: ResolutionJob이 resolve 후 carry_over_outcome 적용 — PASS
  - 근거: `server/apps/worker/src/jobs/resolution_job.rs:144-148`. `let outcome = carry_over_outcome(resolve(mode, ..., &votes), &votes, snapshot.carry_over)` 패턴으로 resolve 결과에 carry_over_outcome을 체이닝 적용. 이후 `Held` 일 때만 `routine_a.advance(...)` 호출(line 181) — Skipped는 포인터 전진 없음 확인. (L3 달성)

- [x] SV-04: RoutineSnapshot에 carry_over 관통 + 양쪽 adapter carry_over 채움 — PASS
```

</details>

<details><summary>sprint-feedback-workout-sync-utc.md 앞부분</summary>

```markdown
# Sprint Feedback
Feature: 운동 완료 세션 서버 sync UTC 직렬화 수정 (POST 400 해소)
Evaluated: 2026-06-29 19:10
Verdict: REJECT
Iteration: 2

## Results

### UI (1/1)
- [x] UI-01: 완료 요약 스트릭 밴드 일수가 완료 세션의 로컬 날짜 기준 운동일 수와 일치한다 — PASS
  - 근거: `app/test/features/record/data/models/workout_session_model_test.dart:47-54` — round-trip 테스트 PASS. `compute_workout_streak_test.dart` 전체 PASS (83/83). `compute_workout_streak.dart:61-63` — `_dateOnly`가 UTC DateTime에 `toLocal()` 정규화하여 로컬 날짜 기준 집계 L3 추적 완료.
  - 검증 깊이: L3

### Logic (3/3)
- [x] LG-01: 완료된 운동 세션이 서버에 정상 저장된다 — PASS
  - 근거: 라이브 증거(Iteration 2 제공) — UTC `"2026-06-29T08:10:42.365474Z"` POST → HTTP 200 수락, postgres `workout_sessions` 행 생성(started_at `2026-06-29 08:10:42.365474+00`). 서버 단위 테스트 `create_session_accepts_utc_z_format` PASS (직접 실행, exit 0).
  - 검증 깊이: L3 (실행 산출물 + 단위 테스트 교차검증)

- [x] LG-02: 앱이 전송하는 started_at/ended_at 이 타임존 오프셋을 포함한 RFC3339 문자열이다 — PASS
  - 근거: `app/lib/features/record/data/models/workout_session_model.dart:56-57` — `session.startedAt.toUtc().toIso8601String()` (literal). 앱 단위 테스트 `rfc3339WithOffset = RegExp(r'T.*(Z|[+-]\d\d:\d\d)$')` 매칭 3/3 PASS (직접 실행, exit 0).
```

</details>

<details><summary>sprint-feedback-s8.md 앞부분</summary>

```markdown
# Sprint Feedback
Feature: 글로벌 모임일정 S8 — 다음 모임 서버 슬롯 소스 전환
Evaluated: 2026-06-25
Verdict: APPROVE
Iteration: 1

## Results

### UI (3/3)
- [x] UI-01: nextMeetingAt 주입 시 "다음 모임" 라벨·포맷 시각·chevron 표시 — PASS
  - 근거: `routine_rotation_list.dart:91-112` — `if (nextSlot != null)` 분기 내 `group.nextMeeting` 라벨, `_formatSlot()` 포맷 텍스트(toLocal), `LucideIcons.chevronRight` 순서 렌더. 테스트 `routine_rotation_list_test.dart:101-113` — `nextMeetingAt: DateTime(2026,6,2,9,30)` 주입 시 `find.text('다음 모임')` + `find.text('내일 09:30')` findsOneWidget 통과. L3 도달.
- [x] UI-02: nextMeetingAt null 시 "다음 모임" 라인 숨김, 사이클 표기 유지 — PASS
  - 근거: `routine_rotation_list.dart:87,91` — `final nextSlot = nextMeetingAt;` + `if (nextSlot != null)` 조건으로 null 시 블록 미렌더. `routine_rotation_list_test.dart:115-122` — null 주입 시 `find.text('다음 모임')` findsNothing, `find.text('이번 사이클 1/3')` findsOneWidget 통과. L3 도달.
- [x] UI-03: 기존 회전 리스트 표시(✓/다음 배지/사이클 N/총/항목 탭) 회귀 없음 — PASS
  - 근거: `routine_rotation_list_test.dart:56-132` — pointer 0/1/2 케이스, 탭 콜백, 사이클 텍스트 전 케이스 11개 통과(fvm flutter test 결과: +11: All tests passed). L3 도달.

### LG (3/3)
- [x] LG-01: 위젯 코드에 `nextMeetingSlot` 호출 0건 — PASS
  - 근거: `grep -rn "nextMeetingSlot" app/lib/` → `.g.dart` doc comment 내 언급 6건만 히트, 실제 함수 호출(비-주석 코드 경로) 0건 확인. 코드 경로 추적: `routine_rotation_list.dart:87` `final nextSlot = nextMeetingAt;` — 파라미터로만 수신. L3 도달.
- [x] LG-02: 과거/resolved 제외, 미래 pending 최소값 선택, 빈 결과 null — PASS
```

</details>

<details><summary>sprint-feedback-s6.md 앞부분</summary>

```markdown
---
feature: "Sprint 6 — 루틴 holiday_policy + 멀티 시간블록 편집"
evaluated: "2026-06-25"
verdict: APPROVE
iteration: 2
---

# Sprint Feedback

Feature: Sprint 6 — 루틴 holiday_policy + 멀티 시간블록 편집
Evaluated: 2026-06-25
Verdict: APPROVE
Iteration: 2

## Results

### UI (3/3 PASS)

- [x] UI-01 — PASS
  - 근거: `group_schedule_edit_page.dart:137-151` — `for (var i = 0; i < form.blocks.length; i++)` 루프로 N개 TimeBlockCard 렌더. `group_schedule_edit_page_test.dart:41-59` — 기본 1블록 확인 → "Add Time" 탭 → 2블록 확인 → 삭제 → 1블록 확인. 28개 테스트 전체 PASS.
```

</details>
- (본문 미리보기는 최신 5개만 표시 — 나머지 3개는 위 파일별 내역 참조)

### `fit-pal-solo/server`

- 경로: `/Users/jackson/Hub/10_Dev/fit-pal-solo/server`
- sprint-feedback 파일: 1개 (총 69 lines)
- history sprint-contracts: 12
- 최근 contracts:
  - 20260611-1620-h1-ratelimit-xrealip-sprint-contract.md
  - 20260611-1706-track2-authz-sprint-contract.md
  - 20260611-1820-track4-scalar-dev-sprint-contract.md
  - 20260611-1850-track5-block-sprint-contract.md
  - 20260611-2100-track7-session-invalidation-sprint-contract.md
- 파일별 내역:
  - `sprint-feedback.md` — plain (슬러그 없음), 69 lines, mtime 2026-07-29T13:38:13

<details><summary>sprint-feedback.md 앞부분</summary>

```markdown
# Sprint Feedback
Feature: API-3 — 누락 6개 모듈 OpenAPI 스펙 집계 (notification/social/message/user/upload/invitation)
Evaluated: 2026-07-15 11:30
Verdict: APPROVE
Iteration: 1

## Results

### API (2/2)
- [x] API-01: 병합된 OpenAPI 스펙에 6개 모듈의 대표 경로가 모두 포함된다 — PASS
  - 근거: `apps/api/src/main.rs:1257-1275` — `openapi_merge_tests::merged_spec_contains_all_six_module_paths` 테스트가 6개 경로 전수를 key 존재 확인. 테스트 2/2 통과 (cargo test -p fitpal-api openapi_merge).
- [x] API-02: 병합 후 스펙의 총 경로 key 수가 하한 이상이다 — PASS
  - 근거: `apps/api/src/main.rs:1278-1286` — `merged_spec_path_count_above_floor` 테스트 `paths.len() >= 40` 통과. 측정: 테스트 OK (실측 카운트는 런타임 확정이나 컴파일타임 merge 구조상 하한 충족).

### Logic (2/2)
- [x] LG-01: 5개 어노테이션된 모듈 각각에 `*ApiDoc` 구조체 + main.rs 5 merge 라인 — PASS [enumerated 5개 전수]
  - 근거 (개별):
    - `modules/notification/src/router.rs:242-264`: `#[derive(utoipa::OpenApi)]` + `pub struct NotificationApiDoc` (9 paths, 5 schemas)
    - `modules/social/src/router.rs:369-397`: `#[derive(utoipa::OpenApi)]` + `pub struct SocialApiDoc` (12 paths, 8 schemas)
    - `modules/message/src/router.rs:290-317`: `#[derive(utoipa::OpenApi)]` + `pub struct MessageApiDoc` (9 paths, 10 schemas)
```

</details>

### `fit-pal-wt`

- 경로: `/Users/jackson/Hub/10_Dev/fit-pal-wt`
- sprint-feedback 파일: 1개 (총 78 lines)
- history sprint-contracts: 23
- 최근 contracts:
  - 20260603-1520-sprint-contract.md
  - 20260603-server-plan1-sprint-contract.md
  - 20260610-1537-member-manage-sprint-contract.md
  - 20260611-0919-server-authz-sprint-contract.md
  - 20260611-1300-server-m5-storage-sprint-contract.md
- 파일별 내역:
  - `sprint-feedback.md` — plain (슬러그 없음), 78 lines, mtime 2026-06-11T19:45:15

<details><summary>sprint-feedback.md 앞부분</summary>

```markdown
# Sprint Feedback
Feature: deferred follow-up (record LIMIT / schedule guard / N+1 / UI i18n / tests)
Evaluated: 2026-06-11 09:30
Verdict: APPROVE
Iteration: 1

## Results

### Logic/API — Server (4/4)

- [x] S1: record `list_sessions` LIMIT(200) 적용 — PASS
  - 근거: `server/modules/record/src/service.rs:18` — `const MAX_SESSIONS: u64 = 200;`
  - 근거: `service.rs:89` — `.limit(MAX_SESSIONS)` (L3: list_sessions 외 다른 경로 없음)

- [x] S2: `confirm_time` 과거 후보 거부 + 단위테스트 confirm_time_rejects_past_candidate — PASS
  - 근거: `service.rs:753` — `if candidate.candidate_at <= Utc::now().fixed_offset() { return Err(AppError::Validation(t("schedule.candidate_in_past"))) }`
  - 근거: `service.rs:1170` — `async fn confirm_time_rejects_past_candidate()` 존재 + 어서션 `matches!(err, AppError::Validation(_))` (line 1201)

- [x] S3: `add_time_candidate` ≤10 상한 + ko.yml/en.yml 키 존재 [exact, enumerated] — PASS
  - 근거: `service.rs:19` — `const MAX_TIME_CANDIDATES: u64 = 10;`, `service.rs:665` — `if existing >= MAX_TIME_CANDIDATES { Err(t("schedule.candidate_limit")) }`
```

</details>

### `fit-pal-wt/app`

- 경로: `/Users/jackson/Hub/10_Dev/fit-pal-wt/app`
- sprint-feedback 파일: 1개 (총 147 lines)
- history sprint-contracts: 27
- 최근 contracts:
  - 20260605-ifminibutton-prev-sprint-contract.md
  - 20260608-1637-sprint-contract.md
  - 20260608-1710-tabbar-profile-sprint-contract.md
  - 20260609-1549-sprint-contract.md
  - 20260609-1640-darkmetal-sprint-contract.md
- 파일별 내역:
  - `sprint-feedback.md` — plain (슬러그 없음), 147 lines, mtime 2026-06-11T20:13:43

<details><summary>sprint-feedback.md 앞부분</summary>

```markdown
# Sprint Feedback
Feature: 재감사 Track6 — L-5 로그 URI 쿼리스트링 토큰 마스킹
Evaluated: 2026-06-11 20:15
Verdict: REJECT
Iteration: 1

## Results

### UI (N/A)

- [x] UI-00: N/A — 계약 명시. UI 변경 없음.

---

### Logic (3/3)

- [x] LG-01: 요청 URI 쿼리스트링 token 평문 미노출 — PASS
  - 태그: [goal]
  - 근거 (L3):
    - 테스트 함수: `logging_interceptor_test.dart:138` "요청 URI 쿼리스트링의 토큰을 마스킹한다"
```

</details>

### `fit-pal-wt/server`

- 경로: `/Users/jackson/Hub/10_Dev/fit-pal-wt/server`
- sprint-feedback 파일: 1개 (총 66 lines)
- history sprint-contracts: 10
- 최근 contracts:
  - 20260611-1539-group-detail-routine-backend-sprint-contract.md
  - 20260611-1615-notification-push-i18n-sprint-contract.md
  - 20260611-1620-h1-ratelimit-xrealip-sprint-contract.md
  - 20260611-1706-track2-authz-sprint-contract.md
  - 20260611-1820-track4-scalar-dev-sprint-contract.md
- 파일별 내역:
  - `sprint-feedback.md` — plain (슬러그 없음), 66 lines, mtime 2026-06-11T20:13:43

<details><summary>sprint-feedback.md 앞부분</summary>

```markdown
# Sprint Feedback
Feature: Track5 — L-2 프로필 조회·유저 검색에 차단(block) 관계 반영
Evaluated: 2026-06-11 19:45
Verdict: APPROVE
Iteration: 1

## Results

### API (3/3)
- [x] API-01: 차단 관계면 프로필 조회 NotFound — PASS
  - 근거: `modules/user/src/service.rs:252` — `AppError::NotFound(fitpal_error::t("user.not_found"))` 반환. 단위테스트 `차단_관계면_프로필_조회는_not_found` 통과 (L3)
- [x] API-02: 비차단 관계면 프로필 조회 성공 — PASS
  - 근거: `modules/user/src/service.rs:256-275` — block_checker 통과 후 정상 프로필 반환. 단위테스트 `비차단_관계면_프로필_조회_성공` 통과 (L3)
- [x] API-03: 검색 결과에서 차단 사용자 제외 — PASS
  - 근거: `modules/user/src/service.rs:322-325` — `blocked_ids.contains(&u.id)` 필터 적용. 단위테스트 `검색_결과에서_차단_사용자_제외` 통과 (L3)

### Logic (2/2)
- [x] LG-01: 차단 판정이 outbound 포트를 통해 이뤄지고 검색은 batch 단일 호출 — PASS
  - 근거: `modules/user/src/service.rs:314` — `checker.blocked_among(viewer_id, &candidate_ids)` 루프 외부에서 1회 호출 (N+1 없음). 프로필 1:1은 `is_blocked_either_direction`. `modules/user/Cargo.toml`에 `fitpal-social` 의존 없음 (L3)
- [x] LG-02: 양방향 차단 판정 — PASS
```

</details>

### `flutter_playwright`

- 경로: `/Users/jackson/Hub/10_Dev/flutter_playwright`
- sprint-feedback 파일: 14개 (총 2823 lines)
- history sprint-contracts: 11
- 접미형 슬러그: `release-build-recording-strip`, `release-prep-0-15-0`, `locator-parse-validation`, `app-readiness-honest-reporting`, `accounts-environments`, `native-layer-observe-and-act`, `phase-c-e2e-standing-failures`, `mcp-dynamic-pull-collision`, `fit-pal-form-login-e2e`, `mcp-login-path`, `mcp-session-resilience`, `mcp-session-isolation`, `mcp-overlay-isolation`
- 최근 contracts:
  - 20260422-0945-sprint-contract.md
  - 20260422-phase-a-sprint-contract.md
  - 20260422-phase-b-sprint-contract.md
  - 20260507-1823-sprint-contract.md
  - 20260610-1042-sprint-contract.md
- 파일별 내역:
  - `sprint-feedback.md` — plain (슬러그 없음), 332 lines, mtime 2026-07-28T00:44:15
  - `sprint-feedback-release-build-recording-strip.md` — slug=`release-build-recording-strip`, 181 lines, mtime 2026-09-24T18:01:17
  - `sprint-feedback-release-prep-0-15-0.md` — slug=`release-prep-0-15-0`, 169 lines, mtime 2026-09-11T15:16:55
  - `sprint-feedback-locator-parse-validation.md` — slug=`locator-parse-validation`, 262 lines, mtime 2026-09-11T15:16:55
  - `sprint-feedback-app-readiness-honest-reporting.md` — slug=`app-readiness-honest-reporting`, 148 lines, mtime 2026-09-11T15:16:55
  - `sprint-feedback-accounts-environments.md` — slug=`accounts-environments`, 148 lines, mtime 2026-09-11T15:16:55
  - `sprint-feedback-native-layer-observe-and-act.md` — slug=`native-layer-observe-and-act`, 165 lines, mtime 2026-09-11T14:10:15
  - `sprint-feedback-phase-c-e2e-standing-failures.md` — slug=`phase-c-e2e-standing-failures`, 223 lines, mtime 2026-09-11T09:37:43
  - `sprint-feedback-mcp-dynamic-pull-collision.md` — slug=`mcp-dynamic-pull-collision`, 291 lines, mtime 2026-09-08T13:55:15
  - `sprint-feedback-fit-pal-form-login-e2e.md` — slug=`fit-pal-form-login-e2e`, 142 lines, mtime 2026-09-07T18:15:57
  - `sprint-feedback-mcp-login-path.md` — slug=`mcp-login-path`, 228 lines, mtime 2026-09-03T18:35:29
  - `sprint-feedback-mcp-session-resilience.md` — slug=`mcp-session-resilience`, 115 lines, mtime 2026-08-13T20:18:18
  - `sprint-feedback-mcp-session-isolation.md` — slug=`mcp-session-isolation`, 271 lines, mtime 2026-08-13T20:18:18
  - `sprint-feedback-mcp-overlay-isolation.md` — slug=`mcp-overlay-isolation`, 148 lines, mtime 2026-08-13T20:18:18

<details><summary>sprint-feedback.md 앞부분</summary>

```markdown
# Sprint Feedback
Feature: MCP 스택 업그레이드 — dart_mcp 0.5.2 + ToolAnnotations + wait_for settled + structured output
Evaluated: 2026-07-28 00:24
Verdict: REJECT
Iteration: 1

---

## Pre-Check: Binary Decidability (Step 1.5)

25개 조건 전수 점검. 범위어("주요/모든/대부분") 없음 — 전 조건이 "몇 개 중 몇 개"로 enumerate 되어 있어 자체 해석 여지가 없었다.
Tag 파싱 요약: `[exact, enumerated]` 12건 (AR-01, AR-03, LG-01, LG-02, LG-03, LG-05, LG-06, ER-01, AP-04), `[goal]` 4건 (LG-04, ER-03, AP-03 + 관련), `[structural]` 3건 (CP-01, CP-03, DG-02), 나머지 `[exact]`.
Fallback 정책(DG-04)은 계약에 3단계(stdio 실행 → 실패 시 대체 → `[미검증]`)가 명시되어 있고 1단계에서 성공했다.

측정 기준점: 스프린트 base commit `571dbeb`. 아래 모든 diff 기반 조건은 `git diff 571dbeb` + 워킹 트리(untracked 포함) 합산으로 측정했다. `debug_pause_support.dart` 변경분은 계약 전제에 따라 diff 조건에서 제외했다.

## Results

### Architecture (3/3)

```

</details>

<details><summary>sprint-feedback-release-build-recording-strip.md 앞부분</summary>

```markdown
# Sprint Feedback
Feature: 릴리스 빌드에서 화면 녹화 코드·권한 제거
Evaluated: 2026-09-24 17:50
Verdict: APPROVE
Iteration: 1

## Contract Fingerprint
- path: .harness/sprint-contract-release-build-recording-strip.md
- sha256: aa368d82d3d0ec2cfdf1ae9890f89ba88dc285b8d032feddceb3e2f050828628
- status: active
- slug: release-build-recording-strip
- contract_root: /Users/jackson/Hub/10_Dev/flutter_playwright
- contract_root_unconfigured: false
- 선택 근거: ladder 1 명시경로 (HARNESS_CONTRACT 로 지정된 경로)
- legacy_contract_used: false
- seal_status: SEAL_OK
- contract_seal_broken: n/a
- 봉인 커밋 대조: f861992 은 계약 파일 1개만 담음, 현재 판과 산문·조건 diff 없음, conditions_digest 불변 — 원문 그대로
- 재확인(Step 5): 일치
- status_transition: active -> done (아래 참조)
```

</details>

<details><summary>sprint-feedback-release-prep-0-15-0.md 앞부분</summary>

```markdown
# Sprint Feedback
Feature: 0.15.0 릴리스 준비 — 버전·포맷·테스트앱 환경 선언
Evaluated: 2026-09-11 11:45
Verdict: APPROVE
Iteration: 1

## Contract Fingerprint
- path: .harness/sprint-contract-release-prep-0-15-0.md
- sha256: 89ab0c836ae66152c6f272bc59753c7ce0ba398f2b04c6685591f305ccf40ac4
- status: active
- slug: release-prep-0-15-0
- contract_root: /private/tmp/claude-501/-Users-jackson-Hub-10-Dev-flutter-playwright/876f1e2c-a9b4-4869-8db6-9a189e9052d4/scratchpad/fp-prep
- contract_root_unconfigured: false
- 선택 근거: ladder 2 세션소유 (owner_session == $CLAUDE_CODE_SESSION_ID == 876f1e2c-a9b4-4869-8db6-9a189e9052d4; 병렬 active 계약 `fit-pal-form-login-e2e` 는 다른 세션 소유라 배제)
- legacy_contract_used: false
- seal_status: SEAL_OK
- contract_seal_broken: n/a
- 재확인(Step 5): 일치 (sha256/status 저장 직전 재계산 동일, working tree clean)
- status_transition: active -> done (본 피드백 저장 후 수행)

```

</details>

<details><summary>sprint-feedback-locator-parse-validation.md 앞부분</summary>

```markdown
# Sprint Feedback
Feature: locator 파싱 실패를 구조적 오류로 되돌린다
Evaluated: 2026-09-10 14:20
Verdict: APPROVE
Iteration: 3

## Contract Fingerprint
- path: .harness/sprint-contract-locator-parse-validation.md (worktree fp-locator)
- sha256: 4a63bc7a803ca7bebf39eae6f8c4caa84cca85b2102e289f014262ba2af791eb (iteration 1·2와 동일 —
  계약 본문 무변경, `git diff f6b1177..HEAD`가 사이드카 파일 1개만 보임)
- status: active
- slug: locator-parse-validation
- contract_root: <worktree>/fp-locator (git worktree, 메인 워킹트리와 격리 — 그쪽은 다른
  세션이 사용 중이라 건드리지 않음)
- contract_root_unconfigured: false
- 선택 근거: 명시 경로 (HARNESS_CONTRACT 로 지정, test -f 확인 후 사용 — ladder 1)
- legacy_contract_used: false
- seal_status: SEAL_OK (`verify_seal` 재실행 — recorded `sha256:88c4d8036b1b06e5` == 실측
  digest, iteration 1·2와 동일)
- contract_seal_broken: n/a
```

</details>

<details><summary>sprint-feedback-app-readiness-honest-reporting.md 앞부분</summary>

```markdown
# Sprint Feedback
Feature: 앱 준비 상태의 정직한 보고
Evaluated: 2026-09-11 12:10
Verdict: APPROVE
Iteration: 1

## Contract Fingerprint
- path: /private/tmp/claude-501/-Users-jackson-Hub-10-Dev-flutter-playwright/e65d2a06-e299-46a5-a5da-e2aa588bd34e/scratchpad/wt-e2e/.harness/sprint-contract-app-readiness-honest-reporting.md
- sha256: b0c21510dbe223aba72bb38ae8764b6f2560d6424a9ff67461d7c24421683903
- status: active
- slug: app-readiness-honest-reporting
- contract_root: /private/tmp/claude-501/-Users-jackson-Hub-10-Dev-flutter-playwright/e65d2a06-e299-46a5-a5da-e2aa588bd34e/scratchpad/wt-e2e
- contract_root_unconfigured: false
- 선택 근거: ladder 1 (명시경로, 사용자가 절대경로 직접 지정, test -f 통과)
- legacy_contract_used: false
- seal_status: SEAL_OK (recorded sha256:abf2f8cc2e5543c4 == actual, verify_seal 직접 실행)
- contract_seal_broken: n/a
- 재확인(Step 5): 일치 (FINGERPRINT OK, 저장 직전 재계산)
- status_transition: active -> done (APPROVE 확정에 따라 전환)

```

</details>
- (본문 미리보기는 최신 5개만 표시 — 나머지 9개는 위 파일별 내역 참조)

### `iyaki-zip-dev`

- 경로: `/Users/jackson/Hub/10_Dev/iyaki-zip-dev`
- sprint-feedback 파일: 1개 (총 131 lines)
- history sprint-contracts: 6
- 최근 contracts:
  - 20260414-2300-sprint-contract.md
  - 20260415-1400-sprint-contract.md
  - 20260420-2020-sprint-contract.md
  - 20260424-1530-sprint-contract.md
  - 20260507-2056-sprint-contract.md
- 파일별 내역:
  - `sprint-feedback.md` — plain (슬러그 없음), 131 lines, mtime 2026-05-07T21:23:27

<details><summary>sprint-feedback.md 앞부분</summary>

```markdown
---
feature: "Visual-center anchored card grow/shrink (option c — REF-based)"
evaluated: "2026-05-07 22:05"
verdict: APPROVE
iteration: 2
---

# Sprint Feedback

Feature: Visual-center anchored card grow/shrink (option c — REF-based)
Evaluated: 2026-05-07 22:05
Verdict: APPROVE
Iteration: 2

## Results

### Behavior (4/4)

- [x] BH-01: Tier 전환 시 visual center ±0.5px 유지 — PASS
  - 근거: `cardSizingController.ts:396-403` — pivot=spec/2, position=visualCenterOf(cardPos). boost 분기 없음. 회귀 없음.
```

</details>

### `navi2025flutter`

- 경로: `/Users/jackson/Hub/10_Dev/navi2025flutter`
- sprint-feedback 파일: 3개 (총 566 lines)
- history sprint-contracts: 0
- 접미형 슬러그: `quill-delta`, `todo-attachment-s3`, `ai-memo-attachment`
- 파일별 내역:
  - `sprint-feedback-quill-delta.md` — slug=`quill-delta`, 150 lines, mtime 2026-09-11T10:03:39
  - `sprint-feedback-todo-attachment-s3.md` — slug=`todo-attachment-s3`, 173 lines, mtime 2026-09-10T13:59:34
  - `sprint-feedback-ai-memo-attachment.md` — slug=`ai-memo-attachment`, 243 lines, mtime 2026-09-10T13:52:58

<details><summary>sprint-feedback-quill-delta.md 앞부분</summary>

```markdown
# Sprint Feedback
Feature: 본문 Quill Delta 대응
Evaluated: 2026-09-11 10:20
Verdict: REJECT
Iteration: 1

## Contract Fingerprint
- path: /Users/jackson/Hub/10_Dev/navi2025flutter/.harness/sprint-contract-quill-delta.md
- sha256: cd61e64fbc28aaaec256480a9796119eb8f5e8a8d98dd8ae5fb6544cc62138b4
- status: active
- slug: quill-delta
- contract_root: /Users/jackson/Hub/10_Dev/navi2025flutter
- contract_root_unconfigured: false
- 선택 근거: ladder 2 세션소유 (owner_session == $CLAUDE_CODE_SESSION_ID, active 후보 유일)
- legacy_contract_used: false
- seal_status: SEAL_OK (conditions_digest sha256:7dc10edc8b488e87 == 실측 contract_digest)
- contract_seal_broken: n/a
- 재확인(Step 5): 일치 (구현 커밋 be72fdb == HEAD, 계약 파일 미변경)
- status_transition: skipped (verdict=REJECT → active 유지)

```

</details>

<details><summary>sprint-feedback-todo-attachment-s3.md 앞부분</summary>

```markdown
# Sprint Feedback
Feature: 할일 첨부 저장소 S3 presign 이관
Evaluated: 2026-09-10 14:10
Verdict: APPROVE
Iteration: 4

## Contract Fingerprint
- path: /Users/jackson/Hub/10_Dev/navi2025flutter/.harness/sprint-contract-todo-attachment-s3.md
- sha256(full file): b4ff27bcfc16deceebc84d26d3451fe4a7402a09941c01367b6364d9a4032201 (Iteration 1~3 와 바이트 단위 동일)
- conditions_digest (frontmatter): sha256:87f2f2cc0adaf858
- status: active
- slug: todo-attachment-s3
- contract_root: /Users/jackson/Hub/10_Dev/navi2025flutter
- contract_root_unconfigured: false
- 선택 근거: ladder 1 (명시 경로 — 사용자가 계약 절대경로를 직접 지정) — 세션소유(ladder 2)로도 동일 결과($CLAUDE_CODE_SESSION_ID = cf179aec-7a1f-4c0c-a160-e972da9a0a17 = 계약 owner_session)
- legacy_contract_used: false
- seal_status: SEAL_OK — `verify_seal` 재실행, contract_digest 재계산값 = frontmatter 기록값(`87f2f2cc0adaf858`)과 일치. 조건 문구 무변경 확인
- contract_seal_broken: n/a
- 재확인(Step 5): 일치 (평가 시작·종료 시점 sha256/status 동일, TOCTOU 없음)
- status_transition: active -> done (verdict=APPROVE)
```

</details>

<details><summary>sprint-feedback-ai-memo-attachment.md 앞부분</summary>

```markdown
# Sprint Feedback
Feature: AI메모 첨부파일 업로드
Evaluated: 2026-09-09 15:30
Verdict: APPROVE
Iteration: 1

## Contract Fingerprint
- path: /Users/jackson/Hub/10_Dev/navi2025flutter/.harness/sprint-contract-ai-memo-attachment.md
- sha256: 3230659e91948746fac61b7925ecebf4b46f3ad88a878c5b64425a3d2cfa5d94
- status: active
- slug: ai-memo-attachment
- contract_root: /Users/jackson/Hub/10_Dev/navi2025flutter
- contract_root_unconfigured: false
- 선택 근거: ladder 1 명시경로 (HARNESS_CONTRACT 상당 — 사용자가 경로를 직접 지정)
- legacy_contract_used: false
- seal_status: SEAL_OK (conditions_digest sha256:49a1392b3a255f97 == 실측 contract_digest)
- contract_seal_broken: n/a
- 재확인(Step 5): 일치 (저장 직전 재계산 sha256 동일, status=active 동일)
- status_transition: active -> done (APPROVE 확정, 아래 참조)

```

</details>

### `purchase-bot`

- 경로: `/Users/jackson/Hub/10_Dev/purchase-bot`
- sprint-feedback 파일: 1개 (총 97 lines)
- history sprint-contracts: 0
- 파일별 내역:
  - `sprint-feedback.md` — plain (슬러그 없음), 97 lines, mtime 2026-06-08T15:56:48

<details><summary>sprint-feedback.md 앞부분</summary>

```markdown
---
feature: "드라이런(observe) 모드 + 결제안전가드 + 구조/타이밍 리팩토링"
evaluated: "2026-06-08 17:10"
verdict: APPROVE
iteration: 1
---

# Sprint Feedback
Feature: 드라이런(observe) 모드 + 결제안전가드 + 구조/타이밍 리팩토링
Evaluated: 2026-06-08 17:10
Verdict: APPROVE
Iteration: 1

## Results

### Logic (4/4)
- [x] LG-01: observe 전체 흐름 실행 + mutating 액션 0회 — PASS
  - 근거: `bot.py:66-70` click_any_text observe=True 분기에서 trial=True만 수행 (실 click 없음). `bot.py:253-255` run_checkout에 if observe: return early. `bot.py:258-265` try_enter_pin/confirm_payment는 return 이후 코드이므로 도달 불가. `bot.py:346-347` install_observe_network_guard가 observe=True 시 반드시 설치됨. 모든 mutating 액션이 observe 가드 뒤에 있음. [L3]

- [x] LG-02: locator.click(trial=True) + "[DRY] would click ..." 로그 — PASS
```

</details>

### `viseo365`

- 경로: `/Users/jackson/Hub/10_Dev/viseo365`
- sprint-feedback 파일: 4개 (총 629 lines)
- history sprint-contracts: 0
- 접미형 슬러그: `familyevent-money-form`, `flutter-playwright-toolkit`, `familyevent-obituary-preview`, `home-renewal-wiring`
- 파일별 내역:
  - `sprint-feedback-familyevent-money-form.md` — slug=`familyevent-money-form`, 155 lines, mtime 2026-09-04T16:10:46
  - `sprint-feedback-flutter-playwright-toolkit.md` — slug=`flutter-playwright-toolkit`, 193 lines, mtime 2026-09-03T11:27:35
  - `sprint-feedback-familyevent-obituary-preview.md` — slug=`familyevent-obituary-preview`, 139 lines, mtime 2026-09-03T10:18:43
  - `sprint-feedback-home-renewal-wiring.md` — slug=`home-renewal-wiring`, 142 lines, mtime 2026-09-02T17:49:12

<details><summary>sprint-feedback-familyevent-money-form.md 앞부분</summary>

```markdown
# Sprint Feedback
Feature: 경조금 기록 폼 저장 연동
Evaluated: 2026-09-04 16:10
Verdict: REJECT
Iteration: 1

## Contract Fingerprint
- path: .harness/sprint-contract-familyevent-money-form.md
- sha256: 326c2b6e6003b9bf32a38cb0d537189039a5e644025c0b5bbaa50eb65afbfdb4
- status: active
- slug: familyevent-money-form
- contract_root: /Users/jackson/Hub/10_Dev/viseo365
- contract_root_unconfigured: false
- 선택 근거: ladder 2 세션소유 (owner_session == CLAUDE_CODE_SESSION_ID, active 유일)
- legacy_contract_used: false
- seal_status: SEAL_OK
- contract_seal_broken: n/a
- 재확인(Step 5): 일치
- status_transition: skipped (verdict=REJECT)

```

</details>

<details><summary>sprint-feedback-flutter-playwright-toolkit.md 앞부분</summary>

```markdown
# Sprint Feedback
Feature: flutter_playwright 툴킷 머신별 stub 전환
Evaluated: 2026-09-03 11:25
Verdict: REJECT
Iteration: 1

## Contract Fingerprint
- path: .harness/sprint-contract-flutter-playwright-toolkit.md
- sha256: 065e00f539841b5926dbfc90aeeb09b2b3297a617f98a00874555193a605e723
- status: active
- slug: flutter-playwright-toolkit
- contract_root: /Users/jackson/Hub/10_Dev/viseo365
- contract_root_unconfigured: false
- 선택 근거: ladder 2 세션소유 (owner_session == $CLAUDE_CODE_SESSION_ID, active 후보 2개 중 세션 소유 유일)
- legacy_contract_used: false
- seal_status: SEAL_OK (conditions_digest sha256:5b3709ffe6e6524a == 실측 조건줄 해시 일치)
- contract_seal_broken: n/a
- 재확인(Step 5): 일치
- status_transition: skipped (verdict=REJECT status=active — active 유지)

```

</details>

<details><summary>sprint-feedback-familyevent-obituary-preview.md 앞부분</summary>

```markdown
# Sprint Feedback
Feature: 경조사 알리기 — 부고장 미리보기 웹뷰 배선
Evaluated: 2026-09-03 10:17
Verdict: APPROVE
Iteration: 1

## Contract Fingerprint
- path: .harness/sprint-contract-familyevent-obituary-preview.md
- sha256: 2cbd1fa612d247461c01c3b732f46bcd84ac0e4c826f3f9174c8b56c05207fef
- status (평가 시점): active
- slug: familyevent-obituary-preview
- contract_root: /Users/jackson/Hub/10_Dev/viseo365
- contract_root_unconfigured: false
- 선택 근거: ladder 2 세션소유 (owner_session == CLAUDE_CODE_SESSION_ID == 85ab0412-9795-4813-b2af-e9a5efa545eb)
- legacy_contract_used: false
- seal_status: SEAL_OK (conditions_digest sha256:65b15811b9d3014d 일치, contract_digest 재계산 확인)
- contract_seal_broken: n/a
- 재확인(Step 5): 일치 (저장 직전 재확인 FINGERPRINT OK)
- status_transition: active -> done (APPROVE 확정 후 전환 완료)

```

</details>

<details><summary>sprint-feedback-home-renewal-wiring.md 앞부분</summary>

```markdown
# Sprint Feedback
Feature: 홈 세 섹션 최신 3건 조회와 카드 탭 상세 연결
Evaluated: 2026-09-02 17:50
Verdict: REJECT
Iteration: 1

## Contract Fingerprint
- path: /Users/jackson/Hub/10_Dev/viseo365/.harness/sprint-contract-home-renewal-wiring.md
- sha256: 89f7815e77575530eee2a9eb5e4946cdbb3d0ea15326b202247f7763d76acada
- status: active
- slug: home-renewal-wiring
- contract_root: /Users/jackson/Hub/10_Dev/viseo365
- contract_root_unconfigured: false
- 선택 근거: 사용자가 절대경로로 명시 (ladder 1)
- legacy_contract_used: false
- seal_status: SEAL_OK (conditions_digest sha256:3b72ad42ab7c0d78 == 실측 contract_digest)
- contract_seal_broken: n/a
- 재확인(Step 5): 일치 (평가 개시/종료 시점 sha256 동일)
- status_transition: skipped (verdict=REJECT, active 유지)

```

</details>


## 3. Followup 문서

- `docs/superpowers/followup-2026-04-11-plugin-validation-findings.md`
- `docs/superpowers/followup-kaizen-memory-integration.md`

## 4. 현재 레포 최근 Sprint Contracts

- `.harness/history/20260727-kaizen-phase4-harness-sprint-contract.md`
- `.harness/history/20260727-kaizen-phase5-flutter-sprint-contract.md`
- `.harness/history/20260727-kaizen-phase6-design-sprint-contract.md`
- `.harness/history/20260727-kaizen-phase7-backend-sprint-contract.md`
- `.harness/history/20260727-kaizen-phase8-infra-sprint-contract.md`
- `.harness/history/20260727-kaizen-phase9-rust-sprint-contract.md`
- `.harness/history/20260727-phase1-prev-sprint-contract.md`
- `.harness/history/20260727-phase1-sprint-contract.md`
- `.harness/history/20260727-phase2-sprint-contract.md`
- `.harness/history/20260727-phase3-sprint-contract.md`

## 5. Validate-Plugin 최근 실행 스냅샷

```text
... (이전 출력 생략)
  V6 code-fence        0 bare — OK
  V7 plugin-json       v0.5.1 matches marketplace — OK
  V8 hook-exec         no hooks.json — OK
  V9 arg-substitution  12 skills — OK
  V10 table-integrity   14 md files — OK

=== reflect-kit ===
  V1 frontmatter       4 skills — OK
  V2 templates         0 files — SKIP (no templates/)
  V3 refs              0 links — OK
  V4 triggers          25 keywords — OK
  V5 placeholders      0 found — OK
  V6 code-fence        0 bare — OK
  V7 plugin-json       v0.7.1 matches marketplace — OK
  V8 hook-exec         직접 실행 hook 스크립트 없음 — OK
  V9 arg-substitution  4 skills — OK
  V10 table-integrity   10 md files — OK

=== bambu-kit ===
  V1 frontmatter       1 skill — OK
  V2 templates         0 files — SKIP (no templates/)
  V3 refs              0 links — OK
  V4 triggers          6 keywords — OK
  V5 placeholders      0 found — OK
  V6 code-fence        0 bare — OK
  V7 plugin-json       v0.9.5 matches marketplace — OK
  V8 hook-exec         no hooks.json — OK
  V9 arg-substitution  1 skills — OK
  V10 table-integrity   2 md files — OK

=== onboarding-kit ===
  V1 frontmatter       1 skill — OK
  V2 templates         0 files — SKIP (no templates/)
  V3 refs              0 links — OK
  V4 triggers          8 keywords — OK
  V5 placeholders      0 found — OK
  V6 code-fence        0 bare — OK
  V7 plugin-json       v0.3.2 matches marketplace — OK
  V8 hook-exec         no hooks.json — OK
  V9 arg-substitution  1 skills — OK
  V10 table-integrity   2 md files — OK

=== tone-kit ===
  V1 frontmatter       3 skills — OK
  V2 templates         6 skipped (ts/js) — OK
  V3 refs              54 links — OK
  V4 triggers          8 keywords — OK
  V5 placeholders      0 found — OK
  V6 code-fence        0 bare — OK
  V7 plugin-json       v0.1.0 matches marketplace — OK
  V8 hook-exec         no hooks.json — OK
  V9 arg-substitution  3 skills — OK
  V10 table-integrity   13 md files — OK

=== api-kit ===
  V1 frontmatter       5 skills + 1 agent — OK
  V2 templates         0 files — SKIP (no templates/)
  V3 refs              0 links — OK
  V4 triggers          20 keywords — OK
  V5 placeholders      0 found — OK
  V6 code-fence        0 bare — OK
  V7 plugin-json       v0.1.0 matches marketplace — OK
  V8 hook-exec         no hooks.json — OK
  V9 arg-substitution  5 skills — OK
  V10 table-integrity   9 md files — OK

=== howto-kit ===
  V1 frontmatter       3 skills + 1 agent — OK
  V2 templates         0 files — SKIP (no templates/)
  V3 refs              0 links — OK
  V4 triggers          18 keywords — OK
  V5 placeholders      0 found — OK
  V6 code-fence        0 bare — OK
  V7 plugin-json       v0.2.1 matches marketplace — OK
  V8 hook-exec         no hooks.json — OK
  V9 arg-substitution  3 skills — OK
  V10 table-integrity   10 md files — OK

Total: 14 plugins, 14 OK
Exit: 0
```


## 6. Phase 별 참조 가이드

각 Phase subagent 는 아래 매핑을 참고하여 자신의 범위에 맞는 섹션을 우선 읽는다. §0 (/insights) 가 존재할 때는 **모든 Phase** 가 §0 을 최우선 참조한다.

§0-b 에서 자기 킷이 언급된 행을 먼저 읽는다. 킷 언급이 없는 행은 전 Phase 공통이다.

**모든 Phase 는 §0.5 (프로젝트 메모리) 에서 자기 도메인 그룹을 함께 읽는다.** 그룹 제목의 `[gid]` 가 Phase 대상 킷에 대응한다. 단 `self_inference`·`미분류` 라벨이 붙은 항목은 계약 조건의 PASS 근거로 쓸 수 없다.

| Phase | 스킬 | 주요 참조 섹션 |
|-------|------|---------------|
| 1 설계 가이드 | skill-design-guide, agent-design-guide | §0 + §1 Improvement Suggestions |
| 2 Contract | contract-design-guide + sprint-contract | §0 + §1 Reject 사유 (계약 모호성) |
| 3 Evaluator | qa-evaluation-guide + qa-evaluator | §0 + §1 Improvement (L3, set intersection) |
| 4 Harness | harness/skills/* (sprint-contract, qa-evaluator 제외) | §0 + §5 validate-plugin 현재 상태 |
| 5 Flutter | flutter-toolkit/skills/* | §0 + §2 Hub 외부 프로젝트 (fit-pal, apps) |
| 6 Design | design-kit/skills/* | §0 + §5 validate-plugin 현재 상태 |
| 7 Backend | backend-kit/skills/* | §0 + §1 Backend 관련 feedback (있다면) |
| 8 Infra | infra-kit/skills/* | §0 + §5 validate-plugin 현재 상태 |
| 9 Rust | rust-kit/skills/* | §0 + §2 Hub 외부 프로젝트 (fit-pal server) |
| 10 React | react-kit/skills/* | §0 + §3 followup-2026-04-11, §5 |
| 11 Planning | planning-kit/skills/* | §0 + §1 planning 관련 feedback |
| 12 Reflect | reflect-kit/skills/* | §0 + §1 Reflexion 패턴 피드백 |

