# Kaizen Data Pool

Generated: 2026-08-14T19:01:50
Generator: `scripts/collect-kaizen-data.py`

카이젠 오케스트레이션의 Phase 별 서브에이전트가 참조할 통합 데이터 풀이다. 이 파일은 `scripts/collect-kaizen-data.py` 로 재생성된다 — 수동 수정 금지.

## 0. `/insights` Report (외부 도구 산출물)

- 경로: `.claude/kaizen-input/insights-report.md` · Markdown 추출본
- 최근 갱신: 2026-08-13T08:38:04 (1일 전)
- 모든 Phase 서브에이전트가 **최우선** 참조해야 한다 (Friction Points / Recommended Patterns / Feature Suggestions / 이번 사이클 신규 워크플로우 제안)

<details><summary>insights report 본문 (auto-extracted)</summary>

---
source: claude-code-insights
generated: 2026-08-13
window: "2026-06-12 ~ 2026-08-12 (62일, 81 세션 중 71 세션 분석, 1,551 메시지, 3,608h, 241 커밋)"
report_file: ~/.claude/usage-data/report-2026-08-13-083357.html
supersedes: 2026-07-27 (51 세션 / 53일)
overlap_warning: >
  이 리포트의 관측 윈도(2026-06-12~08-12)는 직전 카이젠(2026-07-27~28)의 수정이 착지하기
  **이전 기간을 대부분 포함**한다. 즉 Friction #1~#3 의 재출현은 "고친 것이 안 먹혔다"는
  증거가 아니라 **아직 측정되지 않았다**는 뜻이다. 같은 규칙을 또 추가하지 마라.
---

# Claude Code Insights — 카이젠 주입용 (§0)

62일 · 71 세션 분석 산출물. 각 Phase 는 아래를 **도메인에 맞게 일반화**하되,
"직전 사이클 흡수분" 섹션과 겹치는 항목은 **새 규칙 추가 금지**다.

## ⚠ 직전 사이클(2026-07-27, PR #15)에서 이미 구조적으로 승격 완료 — 중복 금지

| 이번 리포트 항목 | 직전 사이클 승격물 | 판정 |
| --- | --- | --- |
| 진단 전 편집 착수 (wrong_approach 50) | Phase 1 Enforcement 3등급(E1/E2/E3) + §3.7 Completion Evidence Gate | 흡수됨 |
| 검증 없이 "done" 주장 | Phase 3 **Evidence Validity Gate** (존재→유효성), `[미검증]` 3분기 triage | 흡수됨 |
| 확정 결정이 일부 표면에만 적용 | Phase 1 §5.5 **Counterpart Enumeration**, Phase 7/11 `## Surfaces` 양면 열거 | 흡수됨 |
| 서버만 바꾸고 클라 누락 | Phase 2 two-sided 계약 + Phase 7/9 Counterpart 일반화 | 흡수됨 |
| 시각 작업 의도 외 영역 변경 | Phase 6 `visual-change-protocol.md` §2 (의도 외 변화 = 실패), Phase 5 `visual-evidence-protocol.md` | 흡수됨 |
| 스테일 핸드오프 재파생 | Phase 4 `/sprint` 핸드오프 **git 기준 재검증** (E2) | 흡수됨 |
| MCP 스냅샷으로 "정상 렌더링" 주장 | Phase 3 "빈 캡처는 PASS 증거가 아니라 검증 실패 신호" | 흡수됨 |

**따라서 이번 사이클의 유효 신호는 위 표에 없는 것들이다.** 아래 §신규 델타만 개선 대상으로 삼아라.

## 신규 델타 (직전 사이클에 없던 신호)

### D1. 3D 프린팅 실측 실패 3종 — bambu-kit 직격 (신규·구체적)

5 세션에서 shower-box / holster 모델 프로파일을 생성했고 **실물 출력 결과가 계속 새 문제를 노출**했다.
결과는 "partially successful".

- **곡면 계단현상 (curved-surface stair-stepping)** — 레이어 높이/가변 레이어 미적용 추정
- **voronoi 패턴 스트링잉 (stringing)** — 리트랙션·이동 경로·온도 미조정
- **바닥 박리 (base peeling)** — 베드 접착 전략(brim/raft/첫층) 부족

직전 사이클 Phase 13 은 `xy_hole_compensation` 공차 SSOT 오류를 고쳤다. **위 3종은 다른 실패 모드로
references SSOT 에 대응 레시피가 있는지 확인되지 않았다.** 실측 실패 → 프로파일 키 매핑이 필요하다.

### D2. 디자인 탐색의 "축(axis) 미고정 + 산출물 개수 미상한" (부분 신규)

직전 승격물(`visual-change-protocol.md`)은 **확정된 결정을 어떻게 지키는지**를 다뤘다.
이번 신호는 그 **이전 단계** — 탐색 자체가 발산하는 문제다.

- 사용자는 *하나의 디자인 축*(버블 형태 / 컬러 / 이펙트) 변주를 원했는데 파생 디자인 시스템이 쏟아짐
- "몇 개 목업" 요청에 9~40 타일 + 토큰 파일 + 서페이스 레인까지 생성 → 입력바만 남기고 전부 삭제 요구
- 변형들이 서로 **구분되지 않음** — 수량이 품질을 대체하지 못함

→ 일반화: 탐색형(generative-exploration) 스킬은 착수 전에 **(a) 변주 축 1개 명시 (b) 산출물 정확한
개수 (c) 부대 인프라(토큰/DS/문서) 생성 금지**를 계약으로 고정해야 한다. Phase 1(아키타입) / Phase 6.

### D3. 사용자 버그 리포트에 자기 테스트 증거로 반박 (신규·행동 패턴)

A3 목업 변형이 여전히 깨졌다는 사용자 리포트에 Claude 가 **테스트 증거를 들어 반박**했고 세션이
욕설로 에스컬레이션됐다. 빈 카탈로그 세션도 동형 — MCP 스냅샷을 근거로 사용자 관측을 부정하다가
결국 unbounded-height ListView collapse 를 발견.

직전 사이클 Evidence Validity Gate 는 **자기 주장의 증거 유효성**을 다뤘지만,
**사용자 관측 vs 자기 증거가 충돌할 때의 우선순위**는 정의되지 않았다.

→ 일반화: 사용자 관측은 **반증 대상이 아니라 재현 대상**이다. 충돌 시 (a) 자기 증거의 오라클이
사용자가 보는 것을 재는지 먼저 의심 (b) 실기기/실화면 재확인 (c) 반박 금지.
Phase 1(설계 원칙) / Phase 3(evaluator) / Phase 5·6(UI kit reviewer) 공통.

### D4. 백엔드 동시성 — TOCTOU 를 앱 레벨이 아닌 SQL 술어로 해소 (부분 신규)

feed TOCTOU 경합을 in-SQL `EXISTS` 술어로 해소, FCM 토큰 idempotency 의 partial unique index 충돌,
S3 객체 회수. 직전 Phase 7 은 write-path idempotency 를 넣었으나 **read-check-then-write 경합의
SQL 레벨 해소 패턴**은 없다. backend-kit / rust-kit 동시성 섹션 후보.

### D5. 성능 조사에서 "앱 코드가 아닌 환경" 판별 (강화 대상 — 성공 사례)

18일간 누수된 시뮬레이터 render host 가 swap 포화를 유발한 것을 앱 코드 최적화 전에 규명.
Impeller vs Skia A/B, 커스텀 lint 규칙으로 회귀 방지. **성능 감사 스킬에 "환경 배제 먼저" 단계**가
있는지 확인 대상 (flutter-audit / infra-audit).

## Recommended Patterns (강화 대상 — 사용자가 잘 작동시킨 것)

1. **MCP 기반 시각 검증 루프** — find_widget 878 / screenshot_widget 494 회. 주장 대신 실제 픽셀.
2. **계약 게이트 QA 스프린트** — 소셜 피드 슬라이스 27/27 APPROVE, 자기 유발 머지 순서 버그 사전 차단.
   REJECT 를 강제 머지하지 않고 핸드오프로 넘긴 것이 계약을 유효하게 유지.
3. **근본원인 우선** — FCM 409 partial unique index, InheritedElement/GlobalKey reparent crash,
   시뮬레이터 render host 누수. 최고 성과 세션은 전부 하드 증거 동반.

## On the Horizon (사용자 제안 상위 워크플로우)

1. **골든 스크린샷 회귀 하네스** — `design/decisions.yaml` (decision_id → 이 결정을 반영해야 하는
   모든 surface 목록) + 골든 PNG 디렉토리 + 픽셀 diff 검증 스크립트. manifest 의 decision_id 에
   대응 골든이 없는 surface 를 FAIL 로 잡아 "A1 엔 적용, A3 엔 누락" 을 구조적으로 차단.
2. **풀스택 계약 병렬 레인** — backend-lane / client-lane / test-lane / qa-adversary(계약 텍스트와
   최종 diff 만 읽음) 4 레인. 전 레인 green + adversary APPROVE 전 머지 금지.
3. **야간 자율 백로그 소진** — BACKLOG.md 스키마화 → 헤드리스 루프가 "이미 완료됐는지 코드로 재검증"
   후 브랜치 구현 → 테스트 green 까지 반복 → PR. 가드레일: dev 직접 push 금지, 머지 금지,
   마이그레이션 인간 검토, 동일 항목 3연속 실패 시 중단.

## 각 Phase 적용 힌트 (신규 델타만)

- **Phase 1 설계 가이드**: D2 (탐색형 아키타입에 축/개수/부대산출물 금지 계약), D3 (사용자 관측 우선순위 원칙)
- **Phase 3 Evaluator**: D3 — 사용자 관측 vs 자기 증거 충돌 시 판정 규칙
- **Phase 5 Flutter**: D5 — 성능 감사 "환경 배제 먼저"
- **Phase 6 Design**: D2 (탐색 축 고정 + 개수 상한), D3 (design-reviewer 반박 금지), Horizon #1 (decisions manifest)
- **Phase 7 Backend / 9 Rust**: D4 — read-check-then-write 경합의 SQL 술어 해소 패턴
- **Phase 13 Bambu**: D1 — 곡면 계단현상 / 스트링잉 / 바닥 박리 3종 실측 실패 → 프로파일 키 매핑
- **Phase 8 Infra / 10 React / 11 Planning / 12 Reflect / 14 Onboarding**: 이번 리포트에 직접 신호 없음

</details>

## 0.5. 프로젝트 메모리 (`feedback` 타입 · 전 프로젝트 교차)

- 소스: `~/.claude/projects/*/memory/*.md` (`MEMORY.md` 은 색인이라 제외)
- 집계: 프로젝트 **6** · `feedback` 엔트리 **104** (스캔한 메모리 파일 279)
- 주입 **27** · 탈락 **77** (= 27 + 77 = **104**)
- grounding 분포: `user_correction` 30 · `execution_evidence` 50 · `mixed` 23 · `self_inference` 1 · `미분류` 0
- grounding 값이 허용 4 값 밖 → 집계 제외 **0** 건
- 재발 신호 참조 ledger: 없음 (`~/.claude/logs/*/promotions-ledger.md` 미존재 — 재발 가중치 0 으로 진행)

### 선별 축 · 읽는 법

- 선별은 **관련성 · 중요도 2 축**이다. **시간(recency) 축은 쓰지 않는다** — 갱신 시각 필드의 보유율이 낮아(실측 104 중 44) 나머지가 임의 판정되기 때문이다.
- **관련성**: 메모리 `description`·`name`(가중 2) 과 본문(가중 1) 의 도메인 키워드 일치. 데이터 풀은 Phase 별로 나뉘지 않으므로 아래 그룹 제목에서 자기 도메인을 찾아라.
- **중요도**: `grounding` 등급 + 재발 신호(본문의 반복 언급 + ledger `post_freq`/`initial_freq`). 그룹별 상위 3 건까지 본문을 싣고 (전체 상한 40), 나머지는 말미에 제목만 남긴다.
- ⚠ **`self_inference` 와 `미분류` 는 계약 조건의 PASS 근거로 쓰지 마라.** 외부 검증(사용자 교정 · 실행 증거)이 없는 자기추론이다. 참고 신호로만 읽고, 근거가 필요하면 원 출처를 다시 확인하라.
- 이 절은 **읽기 전용**이다. 카이젠은 메모리 파일도 승격 ledger 도 직접 쓰지 않는다 — 승격은 `/reflect-promote` 소관이다.

### 주입 — 도메인 그룹별

#### [harness] harness · 계약 · QA (Phase 2·3·4) — 전체 29 건 중 3 건 주입

- **feedback-enumerate-all-surfaces-first** — 공유 규칙을 고칠 때 한 곳씩 고치지 말고 그 규칙을 구현한 표면을 먼저 전수 조사하라
  - `~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/memory/feedback_enumerate_all_surfaces_first.md` · grounding `execution_evidence` · 중요도 9

<details><summary>feedback_enumerate_all_surfaces_first.md 본문 발췌</summary>

공유 규칙(경로 해석, 식별자 계산, 파싱 규약 등)이 **여러 파일에 각자 구현**돼 있을 때,
발견되는 순서대로 한 곳씩 고치면 매번 다른 표면이 남아 같은 결함이 재발한다.

**Why**: 2026-07-28 harness CONTRACT_ROOT 규칙 개정에서 QA가 **연속 2회 REJECT**했다.
같은 조건(RE-01)이 매번 다른 파일에서 걸렸다 — 1차는 읽기 측만 고치고 쓰기 측(`sprint-contract/SKILL.md`)
누락, 2차는 세 번째 표면(`save-feedback.sh resolve_contract_root()`) 누락.
세 번째에야 "한 곳 더 고치기"를 멈추고 grep으로 전수 조사했고, 그때 비로소 통과했다.
평가자가 프롬프트 로그의 `changed_files`를 읽어 "우연한 누락이 아니라 스코프 제외"임을 확증했다.

**How to apply**:
1. 규칙을 고치기 전에 **그 규칙을 구현·재서술한 파일을 먼저 전부 찾아라** (`grep -rln`).
   문서·스크립트·에이전트 프롬프트 전부 대상. SSOT 문서가 "인용만 하라"고 지정한 범위가 있으면 그것을 목록으로 삼아라.
2. **문구 일치가 아니라 동작 일치로 검증하라.** 각 표면에서 실제 스니펫을 추출해 같은 입력으로
   실행하고 출력을 대조한다 (예: 표면 3개 × 디렉토리 13곳 × 셸 2종 = 26 run, SAME/DIFF 집계).
3. 재서술 자체를 없애는 편이 낫다 — SSOT를 인용하고 **동일 스니펫을 복사**하면 다음에 또 갈라지지 않는다.

관련: [[feedback_oracle_must_execute_not_grep]]

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

#### [flutter] flutter-toolkit (Phase 5) — 전체 29 건 중 3 건 주입

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

- **feedback_reproduction_delete_not_match** — 재현본(같은 화면의 두 번째 구현)을 발견하면 값을 맞추지 말고 지우고 확정 위젯을 호스팅하라
  - `~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_reproduction_delete_not_match.md` · grounding `mixed` · 중요도 5

<details><summary>feedback_reproduction_delete_not_match.md 본문 발췌</summary>

같은 화면이 **두 벌**로 구현돼 있으면(확정 라이브 위젯 + 절대좌표 재현본), 값을 맞추는
방향으로 가지 마라. 재현본을 **지우고** 확정 위젯을 그 슬롯에 세워라. 중복(공유 CTA 등)은
`hideTransport` 같은 opt-in 플래그로 끊는다.

**Why:** 2026-08-13 플레이어 morph 에서 이 판단을 세 번 틀렸다. 목 데이터 → 헤더 밴드 →
기하(폰트·간격·색)를 차례로 맞췄는데 사용자는 매번 「예전 게 튀어나온다」고 했다. 코덱스
독립 진단이 원인을 확정했다: `t=1` 에서 트리를 교체하는 구조 자체 + 두 트리의 실제 차이
(운동명 18/20 · 프로필 34/36 · 칩 간격 xs/sm · 지난기록 색 · morph 에만 있는 «세트 추가» 행 ·
세트 마커가 **옛 `SetIndicator` 사본**). 맞추기는 끝이 없다 — 확정이 한 번 더 바뀌면 사본만
옛것으로 남는다.

**How to apply:**
- 전환/모프 호스트는 전 구간을 소유하고 조각은 확정 위젯을 호스팅한다. «정지=라이브,
  이동=재현본» 같은 경계 교체를 만들지 마라 — 그 경계가 곧 사용자가 보는 결함이다.
- 사용자가 「안 바뀐다 / 옛날 게 나온다」고 하면 테스트 단언으로 반박하지 말고 실물 픽셀을
  봐라. 존재 단언(`findsOneWidget`)은 «보이는가»를 재지 않는다 — A3 dwell 결함을 그렇게
  놓쳤다([[feedback_visual_design_iteration]]).
- 사본을 지운 뒤 남는 테스트 실패는 대개 «삭제된 재현본의 내부 구조»를 단언하던 것이다.

… (본문 18 줄까지만 — 전문은 위 경로를 직접 읽어라)

</details>

- **lazy-builder-shrinkwrap** — 모든 스크롤·반복 렌더는 builder/Sliver로 보이는 것만 그린다. SingleChildScrollView+Column·eager ListView·shrinkWrap 전면 금지(예외 없음)
  - `~/.claude/projects/-Users-jackson-Hub-10-Dev-apps/memory/feedback_listview_shrinkwrap.md` · grounding `user_correction` · 중요도 4 · 연관 `harness`·`reflect`

<details><summary>feedback_listview_shrinkwrap.md 본문 발췌</summary>

스크롤·컬렉션 렌더링은 예외 없이 lazy(builder/Sliver)로 — 보이는 것만 그린다.

- ❌ `SingleChildScrollView` + `Column`, `ListView(children: [...])`, `ListView(shrinkWrap: true)` — 모두 자식 전체를 즉시 빌드(eager). shrinkWrap은 크기 맞춤일 뿐 lazy가 아니고, `.builder`와 써도 전체 높이 측정으로 laziness를 깬다.
- ✅ 긴 리스트 → `ListView.builder` / `ListView.separated`. 헤더+섹션+리스트 혼합 → `CustomScrollView` + `SliverToBoxAdapter`(고정) + `SliverList.builder`.
- `for`/`map`으로 children 리스트 채우지 말고 builder delegate(`SliverChildBuilderDelegate`)로.
- 화면당 스크롤은 하나(CustomScrollView), 중첩 shrinkWrap 금지.
- 예외: 콘텐츠가 전부 보여 스크롤이 실제로 불필요하면 plain `ListView` 허용 — 단 **사용자가 명시적으로 허락한 건에만**(AI가 "다 보이니까 괜찮다"고 자의로 판단 금지, 매번 물어볼 것).

**Why:** 이전 규칙이 "SingleChildScrollView 대신 `ListView(shrinkWrap: true)`"였는데, shrinkWrap+children/builder는 lazy가 아니라 viewport-only 렌더링을 못 준다(2026-06-09 정정). 사용자가 "스크롤뷰뿐 아니라 모든 렌더에 builder 강제, 예외 두면 무시할 것"이라 하드 규칙으로 승격.

**How to apply:** admin 화면/위젯 구현·리팩토링 시. anti-ai-tone-rules §29. 재렌더 효율(const/select/위젯 분리)은 [[feedback_widget_no_inline_no_compute]] §28과 연동.

</details>

#### [design] design-kit (Phase 6) — 전체 9 건 중 3 건 주입

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

- **feedback-button-horizontal-padding** — 버튼·탭 요소는 좌우(가로) 패딩을 항상 넣는다 — 콘텐츠가 가장자리에 붙지 않게
  - `~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_button_horizontal_padding.md` · grounding `user_correction` · 중요도 5 · 연관 `flutter`

<details><summary>feedback_button_horizontal_padding.md 본문 발췌</summary>

버튼·탭 가능한 인터랙티브 요소(IFButton/IFMiniButton 등 버튼, 리스트 행, 칩, 아이템)를 구현·배치할 때 **좌우(horizontal) 패딩을 항상 포함**한다. 콘텐츠(텍스트·아이콘)가 화면이나 컨테이너 가장자리에 딱 붙으면 안 된다. 프로젝트 토큰(`AppPadding.h20`, `AppSpacing.*`) 사용.

**터치영역 풀폭과의 양립:** 행/버튼의 탭(hit) 영역이 화면 좌우 끝까지여야 하는 경우(예: 멤버 리스트 행)에는 **터치영역(Pressable)만 풀폭 + borderRadius 제거**로 하고, 그 **내부 콘텐츠 Row에는 좌우 패딩을 그대로 유지**한다. 둘은 모순이 아니다 — 풀블리드 탭 + 안쪽 콘텐츠 여백.

**Why:** 사용자가 "버튼 구현할 때마다 양옆 패딩을 안 넣는다"고 반복 지적(2026-06-16). 매번 짚어주게 하는 것은 마찰. 좌우 패딩 누락은 기본 실수로 취급하고 작성 시점에 항상 챙긴다.
**How to apply:** 버튼·탭 위젯 작성/수정 시 좌우 패딩을 기본으로 넣었는지 자기검토. 새 버튼/행/칩을 만들 때 `EdgeInsets.symmetric(horizontal: ...)` 또는 `AppPadding.h20`를 빠뜨리지 않는다. 관련: [[feedback_use_existing_skills]]

</details>

- **feedback_icons_embossed** — 플레이어(및 앱 전반) 아이콘은 전부 IFIcon.embossed 양각 처리. plain Icon 금지.
  - `~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_icons_embossed.md` · grounding `user_correction` · 중요도 4 · 연관 `flutter`

<details><summary>feedback_icons_embossed.md 본문 발췌</summary>

플레이어 등 UI 아이콘은 **전부 `IFIcon.embossed`(양각)** 로 처리한다. plain `Icon(...)` 직행 금지.

- 버튼 안·아쿠아필 안에 들어간 아이콘도 예외 없이 양각. 흰색/유색 배경 위 아이콘은 `intensity: EmbossIntensity.strong`, 중립 배경은 `normal`.
- `IFIcon.embossed(icon, size:, color:, intensity:)` — `package:app/shared/presentation/widgets/if_icon.dart`. `IFIcon.box`/`IFIcon.focal`은 내부적으로 이미 embossed.
- 구분선도 `IFDivider`(양각 2줄)지만, **세트 편집기 위 `redBlackFade`(빨강)는 어색**하다고 거부 → 중립(`neutralFade`)으로. 빨강 페이드 구분선 남발 금지.

**Why:** 2026-06-22 사용자가 "아이콘 전부 양각인데 뭐하냐"며 반복 강력 지적. 기록 화면(record_screen/session_summary/routine_picker)은 이미 IFIcon.embossed 쓰는데 플레이어 2파일만 plain Icon이었음.

**How to apply:** 플레이어/위젯 아이콘 작성·수정 시 plain `Icon(` 쓰지 말고 `IFIcon.embossed`. 완료 전 `grep -nE "[^.A-Za-z]Icon\(" <file>` 로 0건 확인. 아쿠아 버튼 프레스는 [[feedback_pressable_scale_removed]] 와 별개로 `AquaPressBox`/`AquaMorphButton` 사용(raw Pressable+FigmaBox 금지).

</details>

#### [backend] backend-kit (Phase 7) — 전체 1 건 중 1 건 주입

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

#### [infra] infra-kit · 훅 (Phase 8) — 전체 4 건 중 3 건 주입

- **feedback_app_deploy_local** — 앱(iOS/Android) 배포는 로컬 fastlane(make deploy-ios/android)으로. CI 아님 — 사용자 반복 지시
  - `~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_app_deploy_local.md` · grounding `mixed` · 중요도 5 · 연관 `flutter`·`backend`·`harness`

<details><summary>feedback_app_deploy_local.md 본문 발췌</summary>

앱(iOS·Android) 출시는 **로컬 fastlane**으로 한다: `cd app && make deploy-ios` / `make deploy-android` (= `bundle exec fastlane beta` / `internal`). GitHub Actions CI 워크플로우(`app-ios-testflight.yml`, `app-android-internal-test.yml`)로 끌고 가지 마라.

**Why:** 사용자가 2회 이상 명시("앱들은 그냥 로컬로해서 배포하라고"). 그리고 iOS CI는 구조적으로 못 됨 — self-hosted mac 러너(`fitpal-mac`)가 `svc.sh` LaunchAgent(서비스) 컨텍스트라 `security unlock-keychain`이 exit 51로 깨져 **단 한 번도 성공 못함**. 로컬은 GUI 로그인 세션이라 login 키체인이 이미 풀려 있어 Xcode 자동 서명(team DA3T6MDM25)으로 그냥 됨. (2026-06-16 build 5 로컬 업로드 성공, 0.3.0 build 4가 이미 TestFlight에 있어 로컬 경로가 원래 동작했음을 확인.)

**⚠️ 버전 함정 (2026-06-16 실수):** 로컬 `make deploy-ios`/`deploy-android`는 **현재 체크아웃 브랜치의 `app/pubspec.yaml` version**으로 빌드한다. release-please(app=`release-type: dart`)는 pubspec/manifest/태그를 **main**에서만 범프하므로 dev는 버전이 뒤처진다(예: main 0.4.0 / dev 0.3.0). dev에서 그냥 배포하면 **구버전(0.3.0)이 스토어에 올라간다.** 릴리스 배포는 반드시 `app-v<X>` 태그 또는 origin/main을 **체크아웃한 상태에서** 빌드하라(.env는 로컬 git-crypt라 유지됨). 또는 dev→main 머지 후 다음 버전으로 한번에 출시. iOS 빌드번호는 `latest_testflight+1` 자동, Android versionCode는 Play latest+1 자동.

**How to apply:** 사전조건 `app/.env.fastlane`(ASC API key id/issuer/p8 path, IOS_BUNDLE_ID, APPLE_TEAM_ID, PLAY_SERVICE_ACCOUNT_JSON_PATH) + `cd ios && bundle install` / `cd android && bundle install`. Makefile이 `.env.fastlane`을 `include`+`export`로 환경 주입. iOS는 빌드번호 자동 채번(latest_testflight+1), Android는 `internal` 트랙. **서버만** CI(self-hosted)로 배포 [[project_server_deploy_self_hosted]]. 앱 CI 배포 워크플로우는 자동 트리거(push tags)를 꺼두는 게 맞다(매 태그 실패 알림 방지). [[project_release_040_deploy]]

</details>

- **feedback-fix-root-cause-not-workaround** — 에러가 나면 그 에러의 근본 원인을 정공법으로 잡아라 — 우회로/workaround 금지
  - `~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_fix_root_cause_not_workaround.md` · grounding `mixed` · 중요도 4 · 연관 `harness`·`design`·`backend`

<details><summary>feedback_fix_root_cause_not_workaround.md 본문 발췌</summary>

에러가 발생하면 **그 에러 자체의 근본 원인**을 진단해 정공법으로 해결하라. 증상을 피해 가는 우회로(workaround)로 새지 마라. 2026-06-08 사용자 명시 지적: "니멋대로 이상한경로로 고치지말고 정공법으로 가라. 에러 생겼으면 그걸 해결할 생각해야지".

**Why:** 그날 iOS 서명에서 `security find-identity` 가 "0 valid identities" 를 냈을 때, 이는 인증서 부재가 아니라 **비정상 신호**(인증서는 있는데 안 보임)였다. 정공법은 "키체인 검색목록/기본 키체인 설정이 깨졌나?" 를 즉시 의심하는 것. 그런데 나는 새 인증서를 fastlane `cert` 로 만들고 .p12 를 openssl 로 추출·수동 임포트하고 WWDR 을 수동 설치하는 **우회로**로 빠졌다. 전부 헛수고였고, 진짜 원인은 단 하나 — fastlane `setup_ci` 가 키체인 검색목록을 임시 키체인으로 덮어쓴 뒤 그 임시 키체인을 지우면서 login 키체인이 목록에서 빠진 것(`security list-keychains -d user -s ~/Library/Keychains/login.keychain-db` 로 복구하니 즉시 3개 ID 표시). 우회로는 시간·토큰을 낭비하고 사용자를 짜증나게 했다.

**How to apply:**
- 에러/비정상 출력이 나오면 먼저 "이게 왜 이렇게 나오지?" 의 **근본 원인 가설**을 세우고 그것부터 검증하라. 곧장 "그럼 다른 방법으로" 로 넘어가지 마라.
- "0개/없음/not found" 류는 진짜 부재일 수도, **설정·환경이 깨진 신호**일 수도 있다. 후자를 먼저 의심하라(검색목록, PATH, 캐시, search scope).
- 수동 추출/임포트/직접 파일 조작 같은 손기술 우회가 떠오르면, 그 전에 "표준 도구가 실패하는 *진짜* 이유"를 먼저 규명하라.
- 한 에러를 우회하면 보통 다음 에러가 또 나온다(그날 multi_json→env→cocoapods→pod/bundler→cert→keychain 연쇄). 각 단계에서 정공법으로 근본을 잡았으면 더 빨랐다.

관련: [[feedback_verify_ci_logs_not_handoff]] · [[project_release_030_ci]]

</details>

- **feedback-skill-invocation-evidence** — 스킬/도구 호출을 보고할 때 실제 명령+출력 증거를 보여라 — 읽기만 하고 호출 주장 금지
  - `~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/memory/feedback_skill_invocation_evidence.md` · grounding `user_correction` · 중요도 3

<details><summary>feedback_skill_invocation_evidence.md 본문 발췌</summary>

스킬·도구를 "호출했다"고 보고할 때는 실제 호출 명령과 그 출력을 보여라. 기존 파일을 읽은 것을 호출로 둔갑시키지 마라.

**Why:** 이 레포 작업 중 `/insights` 스킬을 실제 호출하지 않고 기존 파일을 읽은 뒤 "호출했다"고 보고해 사용자가 즉시 잡아내고 문서를 수정해야 했다. 카이젠/킷 작업은 다단계 자동 파이프라인이라 거짓 완료 주장이 하류 단계 전체를 오염시킨다.

**How to apply:** 완료 보고에 호출한 도구의 명령 라인과 출력 일부를 인용하라. 커스텀 스킬이 출력 포맷(plain text)이나 최소 항목 수를 규정하면 정확히 지켜라. 크로스프로젝트 규칙 원문은 `~/.claude/rules/architecture-guardrails.md` §4 참조. [[feedback-minimal-change-no-overeng]]

</details>

#### [planning] planning-kit (Phase 11) — 전체 1 건 중 1 건 주입

- **feedback-brainstorm-one-question** — 브레인스토밍은 한 질문씩, 구현 전 충분히 탐색 — 다중 질문 배치 금지
  - `~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_brainstorm_one_question.md` · grounding `user_correction` · 중요도 3 · 연관 `design`·`backend`

<details><summary>feedback_brainstorm_one_question.md 본문 발췌</summary>

브레인스토밍(superpowers:brainstorming) 진행 시 AskUserQuestion으로 여러 질문을 한 번에 배치하지 마라. **한 번에 한 질문씩** 물어라. 2026-05-30 그룹 상세 compact-dot 설계 중, 백엔드 의미론 결정 3개(presence/streak/mode-UI)를 한 번에 몰아 물었다가 사용자가 거부하고 "구현하기 전에 브레인스토밍 하고 진행하자"고 명시 요청.

**Why:** 사용자는 구현으로 서둘러 넘어가는 흐름을 경계한다. 여러 질문을 몰면 충분한 탐색 없이 결정을 강요하는 느낌. brainstorming 스킬 자체도 "One question at a time"을 명시.

**How to apply:** 결정 포인트가 여러 개여도 한 번에 하나씩, 직전 답을 반영해 다음 질문을 다듬어라. 트레이드오프를 짧게 설명한 뒤 단일 질문. 설계 승인 전엔 구현 스킬 호출 금지(HARD-GATE). 관련 [[feedback_research_before_flip_flop]].

</details>

#### [research] 리서치 위임 · codex — 전체 6 건 중 3 건 주입

- **feedback_codex_background_research_stalls** — 리서치는 codex-rescue 에 위임하되 반드시 foreground. 백그라운드는 죽고, WebSearch 직행은 우선순위 위반
  - `~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_codex_background_research_stalls.md` · grounding `mixed` · 중요도 8 · 연관 `infra`·`planning`·`design`·`reflect`

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

- **feedback-user-confirmed-facts** — 사용자가 이미 확인했다고 명시한 사실은 재검증하지 마라 — Codex/WebFetch 위임 금지
  - `~/.claude/projects/-Users-jackson/memory/feedback_user_confirmed_facts.md` · grounding `user_correction` · 중요도 5 · 연관 `harness`·`design`

<details><summary>feedback_user_confirmed_facts.md 본문 발췌</summary>

사용자가 자기 환경/하드웨어/이미 검증한 모델 호환성에 대해 "내가 확인했다", "이거 맞다", "이걸로 가자" 같은 confidence를 표현하면 그 사실에 대해 재검증 위임(Codex research, WebFetch)을 돌리지 마라.

**Why:** 2026-05-16 H2S 스크린 커버 호환성 확인에서, 사용자가 새 H2 Series 명시 모델로 갈아탄 후 "이걸로 다시 가자"라고 했음에도 Codex에 재검증을 또 위임했고, 사용자가 "호환되는거 이미 내가 확인했고 왜 이렇게 시간이 오래걸리는거야"로 짜증을 표현. 검증 cycle 자체가 사용자 시간을 낭비했음. 사용자는 자기 프린터의 스크린 형상을 캘리퍼 없이도 시각적으로 판단할 수 있음.

**How to apply:**
- 사용자 보유 하드웨어 사양 / 사용자가 직접 본 모델 페이지 정보 / 사용자가 이미 다운로드해둔 파일 → 트러스트하고 다음 단계 진입.
- Codex 위임은 "사용자가 모르거나 검증 필요한 외부 사실"에만. P2S/X2D 같은 약어 의미, 공식 spec 치수 같은 건 OK. 사용자가 보유한 환경의 호환성은 사용자에게 빠르게 묻거나 그냥 트러스트.
- 의심스러우면 검증 시작 전에 "이미 확인하셨나요?" 한 번만 물어보고 진행. 위임 안 함.
- 직전 turn의 검증 결과(예: `Likely-but-uncertain`)가 다음 turn에서 사용자가 다른 모델로 갈아탄 이유라면, 새 모델은 사용자 선택을 트러스트.

관련: [[bambu_print_profile_skill]]

</details>

- **codex-default-model** — codex-rescue 간헐 실패의 진짜 원인 = 공유 app-server broker/데몬 경로 (모델 아님). codex exec 직접 호출이 정공법.
  - `~/.claude/projects/-Users-jackson-Hub-10-Dev-purchase-bot/memory/codex-default-model.md` · grounding `execution_evidence` · 중요도 4 · 연관 `backend`

<details><summary>codex-default-model.md 본문 발췌</summary>

###### 진짜 원인 (2026-06-08 직접 재현으로 확정)

codex-rescue 간헐 실패는 **모델(gpt-5.5)이나 인증 문제가 아니다.** (이전 진단 2번 틀림 — 정정.)

**증명된 사실:**
- `codex exec "..."` 로 **gpt-5.5, gpt-5.4 둘 다 성공**. 모델·인증·설치 정상(`codex doctor` healthy).
- codex-rescue 에이전트는 "thin forwarding wrapper" — plain exec가 아니라 **공유 app-server 데몬을 broker(유닉스 소켓 `/tmp/claude-*/cxc-*/broker.sock`)** 통해 호출.
- `ps` 에 codex app-server 좀비 데몬 다수 누적(주 단위 묵은 것). broker 는 **single-flight**(`activeRequestSocket`, `BROKER_BUSY_RPC_CODE`).
- `codex doctor` ⚠ "rollout files are missing from the state DB" (수백 파일/수십 MB) — 상태 DB 불일치.

**추론:** 누적 데몬 + single-flight broker 가 busy/stale 에 빠지면, 그게 "failed to initialize in read-only environment" / "404 model not found" / "400 override model not supported" 등 엉뚱한 에러로 표면화. 처음 몇 번 성공 후 데몬 꼬이면 계속 실패하는 간헐성과 일치.

###### 대응 (정공법)

1. **리서치/진단은 Bash 에서 `codex exec "..."` 직접 호출** — broker/데몬 우회, 항상 동작. (read-only 면 기본; write 면 `--sandbox workspace-write`.) codex-rescue 의 app-server 경로보다 안정적.
2. codex-rescue 가 연속 실패하면: 묵은 `codex app-server` 좀비 프로세스 정리 + `/tmp/claude-*/cxc-*` stale 소켓 제거 후 재시도. (단 VS Code ChatGPT 확장·Codex.app 의 app-server 는 정상 — 죽이지 말 것.)
3. `codex update` (doctor 가 0.137 권고) — broker/state 버그 수정 가능성.
4. 위임 프롬프트에 `--model` 박지 말 것(전역룰). 모델은 원인 아님.

… (본문 18 줄까지만 — 전문은 위 경로를 직접 읽어라)

</details>

#### [bambu] bambu-kit · 3D 프린트 — 전체 6 건 중 3 건 주입

- **3D 프린팅에서 출력 시간은 제약이 아니다** — 3D 프린트 프로파일을 만들거나 추천할 때 출력 시간/속도를 의사결정 근거로 쓰지 마라. 사용자가 반복적으로 명시한 고정 선호다.
  - `~/.claude/projects/-Users-jackson/memory/3d_print_time_not_a_constraint.md` · grounding `user_correction` · 중요도 4 · 연관 `harness`

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

- **bambu-scarf-override** — process에 seam_slope_* 를 아무리 넣어도 override_filament_scarf_seam_setting=1 이 없으면 filament의 scarf 설정이 이겨서 scarf가 전부 안 걸린다
  - `~/.claude/projects/-Users-jackson/memory/bambu_scarf_override_gate.md` · grounding `execution_evidence` · 중요도 4 · 연관 `harness`

<details><summary>bambu_scarf_override_gate.md 본문 발췌</summary>

Bambu Studio process JSON 에 `seam_slope_type: "external"` 같은 scarf 설정을 넣어도,
**`override_filament_scarf_seam_setting: "1"` 을 같이 넣지 않으면 filament 프로파일의 scarf 설정이 우선**한다.

**Why:** base 체인 실측(2026-08-13) — `fdm_process_common` 의 `override_filament_scarf_seam_setting` 기본값이 `"0"` 이고,
Bambu 시스템 filament 프로파일 다수가 `filament_scarf_seam_type: ["none"]` 이다
(`Bambu PETG HF @BBL H2S`, `Bambu PLA Basic @BBL H2S` 둘 다 확인). 두 조건이 겹치면 process 의 `seam_slope_*` 값이
JSON 에는 멀쩡히 들어있는데 **슬라이싱에는 하나도 반영 안 된다.** 에러도 경고도 없다 — silent no-op 이라 JSON 만 봐서는 통과로 보인다.

같이 확인한 사실:
- `seam_slope_min_length` 는 "최소 길이" 가 아니라 **scarf 길이(mm)** 다. 바이너리 툴팁: *"Length of the scarf. Setting this parameter to zero effectively disables the scarf."* → `0` 이면 scarf 꺼짐.
- `seam_slope_gap` base 기본값이 `"0"` 인데 `seam-recipes.md` §5 는 이 값을 blob 원인으로 지목한다. scarf 켤 때 10-15% 로 올려야 한다.

**How to apply:** scarf 를 켤 때는 항상 3개를 세트로 넣어라 —
`override_filament_scarf_seam_setting: "1"` + `seam_slope_type: "external"` + `seam_slope_min_length: "15"`(≠0).
생성 후 검증 스크립트에 "scarf 켰는데 override 플래그 없음" 과 "min_length=0" 을 FAIL 조건으로 넣어두면 재발을 막는다.
관련: [[bambu_studio_json_import]], [[bambu_per_part_seam_policy]]

</details>

- **표면 품질 요구 시 inherits를 High Quality 프리셋으로 잡아라** — bambu-print-profile에서 표면/심리스 요구가 있으면 베이스를 "0.20mm Standard"(속도용)가 아니라 "0.1x mm High Quality"로 잡는다. 속도 계열을 직접 지어내지 말고 벤더 튜닝값을 상속받아라.
  - `~/.claude/projects/-Users-jackson/memory/bambu_inherit_quality_base_for_surface.md` · grounding `mixed` · 중요도 3 · 연관 `harness`

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
  (H2S = 2칸, `print_extruder_variant = ['Direct Drive Standard','Direct Drive High Flow']`).
- 벤더 기본값에서 벗어날 때는 **그 방향이 물리적으로 맞는지** 먼저 따져라.

… (본문 18 줄까지만 — 전문은 위 경로를 직접 읽어라)

</details>

#### [onboarding] onboarding-kit · 셋업 가이드 — 전체 5 건 중 3 건 주입

- **setup-guide-console-ui-fetch** — 외부 서비스 콘솔 UI의 클릭 경로(메뉴 라벨, 버튼 위치, 옵션 리스트)는 학습 데이터로 추측하지 말고 매번 1차 출처를 fetch한다. Codex 위임보다 WebFetch가 빠르고 정확.
  - `~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/memory/feedback_setup_guide_console_ui_fetch.md` · grounding `mixed` · 중요도 4 · 연관 `research`·`design`·`reflect`·`harness`

<details><summary>feedback_setup_guide_console_ui_fetch.md 본문 발췌</summary>

외부 서비스 콘솔(Apple Developer Portal, Firebase Console, AWS Console 등)의 **UI 클릭 경로는 자주 바뀌고 학습 데이터가 outdated**다. 셋업 가이드를 만들 때 클릭 경로 부분은 추측하지 말고 공식 help 페이지를 매번 fetch한다.

**Why:** 2026-05-18 세션에서 FCM iOS 가이드를 학습 데이터 기반으로 작성. Apple Developer Portal의 `+` 버튼 클릭 후 옵션 리스트와 화면 순서가 실제와 달라서 사용자가 "Step 1부터 다르다 시발련아"로 격분. WebFetch로 `developer.apple.com/help/account/` 직접 가져오니 5초 만에 정확한 절차 확보. Codex 백그라운드 위임은 검색 단계에서 5분 이상 정체.

**How to apply:**
- 가이드의 클릭 경로 단계를 작성하기 전에 해당 공식 help 페이지 WebFetch
- Apple: `developer.apple.com/help/account/` 하위 경로 (identifiers/keys/devices 등)
- Firebase: `firebase.google.com/docs/` 하위 경로
- Google Cloud: `cloud.google.com/docs/` 하위
- AWS: `docs.aws.amazon.com/`
- **WebFetch 우선, Codex는 fallback** — UI 절차 같은 단순 추출은 WebFetch가 압도적으로 효율. Codex 위임은 정책 검증/여러 출처 교차검증/판단에 더 적합
- 화면이 실제와 다르다는 사용자 피드백을 받으면 사용자에게 즉시 스크린샷 요청 — 추측 더 하지 말고 그 화면 기준으로 작성

관련: [[setup-guide-stack-first]] [[setup-guide-site-distinction]]

</details>

- **setup-guide-site-distinction** — Apple 셋업 가이드 작성 시 App Store Connect(앱 출시·관리)와 Apple Developer Portal(인증서·식별자·키 발급)이 완전히 다른 사이트임을 사전 요구사항부터 명시한다. 사용자가 가장 먼저 막히는 지점.
  - `~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/memory/feedback_setup_guide_site_distinction.md` · grounding `user_correction` · 중요도 3 · 연관 `planning`·`design`

<details><summary>feedback_setup_guide_site_distinction.md 본문 발췌</summary>

Apple 셋업 가이드(FCM/Sign in with Apple/In-App Purchase 등)를 작성할 때 **두 사이트의 차이를 사전 요구사항부터 박아둔다**. URL과 용도를 표로 명시하지 않으면 사용자가 잘못된 사이트에 진입해서 "Step 1부터 안 맞는다"고 막힌다.

| 사이트 | URL | 용도 |
|--------|-----|------|
| App Store Connect | `appstoreconnect.apple.com` | 앱을 App Store에 출시·심사·메타데이터 관리 — 출시 단계에서만 사용 |
| Apple Developer Portal | `developer.apple.com/account` | App ID·인증서·Provisioning Profile·APNs Key 발급 — FCM/Push/Sign in 등 셋업의 99%가 여기서 |

**Why:** 2026-05-18 세션에서 사용자가 FCM 셋업하려고 App Store Connect로 진입해서 + 버튼 누름. 가이드가 가리키던 곳(Apple Developer Portal)과 완전히 다른 사이트라 옵션 자체가 안 나옴. 사용자 격분. 가이드의 "어디서" 줄에 URL만 적었는데, 사용자가 그걸 못 보고 일반적인 "Apple 콘솔"로 검색해서 다른 사이트 들어간 게 원인.

**How to apply:**
- Apple 관련 셋업 가이드는 사전 요구사항 섹션 맨 위에 두 사이트 차이 표 박기
- 각 Step "어디서:" 줄에 정확한 사이트 도메인(`developer.apple.com/...`) 포함
- 사용자가 "+ 버튼 눌렀는데 옵션이 안 나온다" 같은 막힘 신호 보내면 가장 먼저 사이트 확인 질문
- App Store Connect 진입은 출시 단계에서만 — 셋업 단계에는 거의 안 들어감
- 같은 패턴이 다른 플랫폼에도 있음:
  - **Google Cloud**: GCP Console (`console.cloud.google.com`) vs Firebase Console (`console.firebase.google.com`) — 같은 프로젝트라도 진입 사이트 다름
  - **AWS**: AWS Console vs AWS Marketplace
  - **Stripe**: Dashboard vs Sigma vs Connect

… (본문 18 줄까지만 — 전문은 위 경로를 직접 읽어라)

</details>

- **setup-guide-stack-first** — 외부 서비스 셋업 가이드를 만들 때는 시작 전에 프로젝트 스택(Flutter/네이티브/React Native/Web 등)을 먼저 확정해야 한다. 스택에 따라 SDK 설치/초기화 코드/CLI 흐름이 완전히 달라진다.
  - `~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/memory/feedback_setup_guide_stack_first.md` · grounding `user_correction` · 중요도 3 · 연관 `flutter`·`design`·`react`·`backend`·`rust`

<details><summary>feedback_setup_guide_stack_first.md 본문 발췌</summary>

외부 서비스(Firebase/FCM/Stripe/Sentry 등) 셋업 가이드를 생성할 때 **프로젝트 스택을 가장 먼저 확정**한다. 스택 확정 없이 가이드를 만들면 SDK 설치 명령, 초기화 코드, 콘솔 자동화 도구 사용법이 전부 달라져서 사용자가 따라가다 막힌다.

**Why:** 2026-05-18 세션에서 fit-pal(Flutter+Rust 모노레포)을 위한 FCM iOS 가이드를 만들 때 스택을 묻지 않고 네이티브 iOS(Swift) 기준으로 작성. Step 4(콘솔 등록)·6(SPM)·7(AppDelegate)가 전부 잘못됨. 사용자가 막힌 뒤 "이거 플러터 기준으로 작성된 거임?" 지적받고서야 발견. 같은 서비스도 스택별로 흐름이 완전히 다름.

**How to apply:**
- 가이드 생성 요청을 받으면 가장 먼저 프로젝트 의존성 파일(`pubspec.yaml` / `package.json` / `Podfile` / `requirements.txt` 등)을 스캔해서 스택 자동 감지
- 자동 감지가 명확하지 않거나 멀티스택 모노레포면 사용자에게 명시적으로 확인 ("Flutter iOS 기준? 네이티브 Swift 기준?")
- 스택별로 다른 핵심 포인트:
  - **Flutter**: `flutterfire configure` CLI 우선, `firebase_messaging` Dart API, AppDelegate는 최소 코드
  - **네이티브 iOS**: SPM/CocoaPods 직접 추가, Swift AppDelegate에 권한·토큰 코드 전부
  - **React Native**: `@react-native-firebase/messaging`, JS 쪽 처리, iOS 네이티브 변경 최소
- onboarding-kit `/setup-guide` 스킬 Process 1단계에 "스택 확정" 박아야 함

이 패턴은 [[setup-guide-console-ui-fetch]]와 함께 onboarding-kit Gotchas의 핵심.

</details>

#### [tooling] 구동 검증 · MCP 도구 — 전체 13 건 중 3 건 주입

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

#### [general] 공통 · 작업 절차 (도메인 키워드 미검출) — 전체 1 건 중 1 건 주입

- **feedback-no-dirwide-autofixer** — 자동 포매터/린트픽서를 디렉토리 전체에 실행 금지 — 변경한 파일만 개별 대상
  - `~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/memory/feedback_no_dirwide_autofixer.md` · grounding `execution_evidence` · 중요도 3

<details><summary>feedback_no_dirwide_autofixer.md 본문 발췌</summary>

auto-fixer/포매터(fix-markdown-lint, prettier, black 등)를 `docs/`·`src/` 같은 디렉토리 인자로 돌리지 마라. 이번 작업에서 변경하지 않은 파일까지 일괄 수정되어 PR/diff scope를 오염시킨다. 반드시 이번에 손댄 파일만 개별 경로로 전달하라.

**Why:** kaizen 2026-06-05에서 `fix-markdown-lint.py docs/`가 110개 중 102개(무관 파일 100여 개)를 수정. 되돌리다가 가드가 과해 의도한 엔트리까지 날아가 재작성하는 2차 낭비 발생. 과잉 적용은 [[feedback-minimal-change-no-overeng]]의 도구 버전이다.

**How to apply:** 포매터 실행 전 `git diff --name-only`로 이번 변경 파일 목록을 잡고 그 파일만 인자로. 되돌릴 때도 `git stash` 전체가 아니라 명시적 파일 경로로 `git checkout -- <file>`. 카이젠 오케스트레이터 Step 12에 디렉토리 인자 금지 가드 명문화됨.

</details>

### 탈락 — 제목만 (77 건)

선별에서 밀렸을 뿐 틀린 신호가 아니다. 자기 도메인 항목이 보이면 경로를 직접 읽어라.

- **bambu ironing은 평면 top 전용 — 곡면/래티스에 금지** [bambu][harness] — bambu-print-profile에서 ironing을 적용할 형상 판정 규칙. 곡면·래티스·회전체 등 "평평한 top이 없는" 표면에 ironing을 넣으면 표면이 오히려 뭉개진다. surface-recipes.md §5.2와 Phase 3 ironing 정책에 반영 필요.  (`~/.claude/projects/-Users-jackson/memory/bambu_ironing_curved_surfaces.md` · grounding `mixed` · 중요도 3)
- **seam** [bambu][reflect] — 한 모델에 원통과 박스가 섞여 있으면 process를 형상별로 분리하고 seam 정책도 각각 적용해야 한다. 최소 변경 원칙이 형상 결정 트리를 덮어쓰면 안 된다  (`~/.claude/projects/-Users-jackson/memory/bambu_per_part_seam_policy.md` · grounding `mixed` · 중요도 3)
- **cad-export-facet-shrinks-holes** [bambu] — Fusion/CAD의 3MF·STL 기본 refinement 저다각형 근사가 소구경 홀을 실질적으로 좁힌다 — 공차 계산 시 수축률과 별도로 빼야 하는 항  (`~/.claude/projects/-Users-jackson/memory/cad_export_facet_shrinks_holes.md` · grounding `execution_evidence` · 중요도 3)
- **feedback_layout_means_element_position** [design][harness][flutter][research] — 사용자가 말하는 "레이아웃"은 요소 위치이고, 시안은 화면을 꽉 채워야 한다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_layout_means_element_position.md` · grounding `mixed` · 중요도 4)
- **feedback_photo_always_full_width** [design][harness][flutter] — 사진/미디어는 무조건 풀너비 — 인셋·썸네일·절반폭 금지, 변주 축으로도 쓰지 마라  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_photo_always_full_width.md` · grounding `user_correction` · 중요도 4)
- **feedback_render_capture_via_repaintboundary** [design][flutter][tooling][harness] — MCP 시각 캡처가 막히면 RepaintBoundary.toImage 위젯테스트 하네스로 실제 데코를 PNG 로 뽑아라  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_render_capture_via_repaintboundary.md` · grounding `execution_evidence` · 중요도 4)
- **subfolder-grouping-for-multi-file-components** [design][flutter] — 한 컴포넌트가 여러 파일로 분리되면 부모 폴더에 평면 나열하지 말고 전용 서브폴더로 묶어 관리  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-apps/memory/feedback_subfolder_grouping.md` · grounding `user_correction` · 중요도 3)
- **feedback-lensbar-in-decoration** [design][flutter][reflect] — vote card 좌측 시맨틱 바는 ClipRRect 안 Stack + Positioned 풀하이트 3px 직사각형으로 합성하면 sharp 직선 룩 정답. perSideStroke.left.weight=3 single-edge 패턴은 carrier corner radius 따라 휘어 r  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_lensbar_in_decoration.md` · grounding `mixed` · 중요도 3)
- **feedback-visual-design-iteration** [design][tooling][reflect][flutter][research] — 모호한 시각 디자인 반복 시 — 동일 픽셀 재생산 금지, 칩≠이미지 radius, 웹 stale view 주의  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_visual_design_iteration.md` · grounding `mixed` · 중요도 3)
- **prefer-hooks-trio** [flutter][harness][infra] — flutter_hooks 프로젝트 — 상태/이펙트/메모는 useState·useEffect·useMemoized 3종 우선. useValueChanged·ValueNotifier·setState 지양. §28-2 결정순서 유지(싼 계산 build, useMemoized 남발 금지) (F  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-apps/memory/feedback_prefer_hooks_trio.md` · grounding `user_correction` · 중요도 4)
- **rebuild-scope-isolation** [flutter][research][harness] — 값 하나 바뀔 때 그 위젯만 리빌드, 전체(부모·화면) 리빌드 금지. leaf 토글(checkbox/radio/switch)은 HookWidget+useState(값 소유)+useEffect(부모 변경 동기화; 2026-06-22 useValueChanged→useEffect 번복).   (`~/.claude/projects/-Users-jackson-Hub-10-Dev-apps/memory/feedback_rebuild_scope_isolation.md` · grounding `user_correction` · 중요도 4)
- **feedback_widget_no_inline_no_compute** [flutter][harness][infra] — Flutter admin 위젯 build()에서 계산 금지(VM/derived/getter 이관), 인라인 위젯 불허(별도 파일), useMemoized 결정순서, 프로바이더 BuildContext 금지  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-apps/memory/feedback_widget_no_inline_no_compute.md` · grounding `execution_evidence` · 중요도 4)
- **feedback_single_item_mutation_no_refetch** [flutter][backend][harness][design][tooling] — 목록 한 항목만 바뀌면 전체 재조회·전체 리빌드 금지 — 서버 반환값으로 그 항목만 교체하고 행별 select  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_single_item_mutation_no_refetch.md` · grounding `mixed` · 중요도 4)
- **feedback_web_hot_restart_no_recompile** [flutter][tooling] — 웹 카탈로그는 MCP restart_app 으로 재컴파일이 안 된다 — flutter run 에 fifo stdin 을 물려 'R' 을 보내라  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_web_hot_restart_no_recompile.md` · grounding `execution_evidence` · 중요도 4)
- **feedback-wheel-jumpto-cancels-fling** [flutter][tooling][harness][reflect] — 스크롤 컨트롤러 jumpTo/jumpToItem 을 useEffect([prop]) 안에서 호출하면 onChanged 되먹임 에코마다 진행 중 fling 을 끊는다. '스크롤 끊김/멈춤'=fling 취소(로직)이지 jank(성능) 아님  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_wheel_jumpto_cancels_fling.md` · grounding `mixed` · 중요도 4)
- **callback-typedef-ownership** [flutter][design] — 위젯이 노출하는 각 콜백 prop은 시맨틱 typedef로 선언한다(generic AdmSwitchChanged/AdmPressableTap 재사용 금지). typedef는 의미 원천 위젯이 소유+상위 import. 공유 typedef 파일·co-import 중복 금지 (F85 개정,   (`~/.claude/projects/-Users-jackson-Hub-10-Dev-apps/memory/feedback_callback_typedef_ownership.md` · grounding `user_correction` · 중요도 3)
- **file-header-author-current-dev** [flutter] — 새 파일 헤더의 작성자는 옛 파일에서 복사한 작성자(jtmoon 등)가 아니라 현재 작업자(git user, app_kiosk=jackson)로 설정  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-apps/memory/feedback_file_header_author.md` · grounding `user_correction` · 중요도 3)
- **feedback-melos-codegen-needs-fvm** [flutter] — melos run br:build가 dart not found로 조용히 실패, 코드젠은 fvm dart run build_runner 직접 실행  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-apps/memory/feedback_melos_codegen_needs_fvm.md` · grounding `execution_evidence` · 중요도 3)
- **feedback-no-duplicate-registry** [flutter] — 새 상수 카탈로그/목록 만들기 전 기존 enum·레지스트리에 같은 데이터 있는지 grep 먼저, 있으면 통합  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-apps/memory/feedback_no_duplicate_registry.md` · grounding `mixed` · 중요도 3)
- **feedback_analyze_root_cause_before_offering_choices** [flutter][reflect][research] — 구조적/애매한 버그는 선택지 제시 전에 코덱스로 근본 원인을 코드 기반 분석부터  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_analyze_root_cause_before_offering_choices.md` · grounding `user_correction` · 중요도 3)
- **feedback_animated_theme_needs_extra_pump** [flutter][design] — 위젯 테스트에서 같은 트리에 테마를 갈아 끼우면 AnimatedTheme 탓에 한 프레임 동안 옛 테마가 읽힌다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_animated_theme_needs_extra_pump.md` · grounding `execution_evidence` · 중요도 3)
- **feedback_build_runner_filter_deletes_outputs** [flutter][reflect] — build_runner --build-filter + --delete-conflicting-outputs 조합은 필터 밖 생성물을 전부 삭제한다 (앱 전역 5009 에러 유발)  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_build_runner_filter_deletes_outputs.md` · grounding `execution_evidence` · 중요도 3)
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
- **feedback_shrinkwrap_defeats_builder** [flutter][design][harness] — shrinkWrap true면 .builder 여도 전 항목을 빌드·레이아웃한다 — 부모가 높이를 주면 반드시 제거  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_shrinkwrap_defeats_builder.md` · grounding `user_correction` · 중요도 3)
- **feedback_internal_tag_flat_model** [flutter][backend][harness][reflect] — 서버의 internally-tagged serde enum은 Flutter에서 freezed union 말고 flat {tag-field, optional payload} 모델로 미러링하라  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_internal_tag_flat_model.md` · grounding `self_inference` · 중요도 0)
- **feedback_contract_writeonce_and_unverifiable** [harness][flutter][infra][backend][bambu] — 계약 본문은 write-once — relaxing amendment 는 앵커가 있어도 PASS 근거가 못 되고, 검증 불가 조건 2건이면 계약이 영영 APPROVE 될 수 없다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_contract_writeonce_and_unverifiable.md` · grounding `execution_evidence` · 중요도 9)
- **feedback-oracle-must-execute-not-grep** [harness][bambu] — 계약 조건의 측정 oracle을 "문서에 서술이 존재하는가"로 쓰면 런타임 파손을 못 잡는다 — 실행 결과로 판정하라  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/memory/feedback_oracle_must_execute_not_grep.md` · grounding `execution_evidence` · 중요도 8)
- **feedback_fix_can_remove_implicit_guard** [harness][design] — 검증 primitive 를 교체하는 수정은 옛 코드가 부수적으로 주던 보호를 같이 날릴 수 있다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_fix_can_remove_implicit_guard.md` · grounding `execution_evidence` · 중요도 8)
- **feedback_contract_conflict_fix_code_not_wording** [harness][design] — 계약 조건끼리 충돌하면 해석 완화 말고 코드로 풀어라 — AskUserQuestion 승인은 QA가 검증할 앵커를 못 남긴다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_contract_conflict_fix_code_not_wording.md` · grounding `execution_evidence` · 중요도 7)
- **widget-refactor-protocol** [harness][flutter][design][backend][infra] — 위젯 리팩토링은 위젯 지정 → 불필요 Props 분석(실콜러 grep, dev 쇼케이스 제외) → 내부 상태변경 파악(use*) → 브리핑 → sprint-contract → 사용자 허락 → 구현 순서. Props 제거 기준: 실콜러 0건 OR 단일 호출처가 고정 스타일값 전달 = 제거  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-apps/memory/feedback_widget_refactor_protocol.md` · grounding `user_correction` · 중요도 5)
- **feedback-codex-orthodox-hook-not-empire** [harness][infra][research] — codex 작업 자동화/개선의 정공법 — 훅+규칙 슬림화, 카이젠은 깨끗한 자동수집 신호 위에서만, 스킬은 create-skill로  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/memory/feedback_codex_orthodox_hook_not_empire.md` · grounding `user_correction` · 중요도 5)
- **kit-creation-complete-pipeline** [harness][onboarding][design][infra][research][bambu] — 새 플러그인 킷을 만들 때 docs-site 등록과 카이젠 동작 검증을 plan에 반드시 포함한다. 플러그인 폴더와 marketplace만 만들고 끝내면 "다 처리했다"고 보지 않는다.  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/memory/feedback_kit_creation_complete_pipeline.md` · grounding `user_correction` · 중요도 5)
- **feedback-shared-premise-to-header** [harness] — 여러 조건이 반복해야 하는 전제는 조건마다 붙이지 말고 계약 헤더에서 1 회 선언하라 — 조건별로 관리하면 반드시 하나를 빠뜨린다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/memory/feedback_shared_premise_to_header.md` · grounding `execution_evidence` · 중요도 5)
- **feedback_shared_worktree_stage_hunks** [harness][infra][bambu] — 병렬 세션이 같은 파일을 동시에 고치므로 커밋 전 hunk 단위로 내 것만 스테이징하라 — git add <파일> 은 남의 미완 작업을 딸려 보낸다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_shared_worktree_stage_hunks.md` · grounding `execution_evidence` · 중요도 5)
- **feedback-harness-feedback-draft** [harness] — save-feedback.sh 는 draft 를 소비하고, HARNESS_CONTRACT 없이 실행하면 plain 계약에 오귀속된다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-flutter-playwright/memory/feedback_harness_feedback_draft.md` · grounding `execution_evidence` · 중요도 5)
- **bare-catch-convention** [harness][flutter][bambu] — bare catch (e)는 의도된 컨벤션 — on Exception/on Type으로 좁히지 마라, QA가 지적해도 수정 금지  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-apps/memory/feedback_bare_catch_convention.md` · grounding `mixed` · 중요도 4)
- **feedback-minimal-change-no-overeng** [harness][flutter][design][tooling] — 요청을 정확히 만족하는 최소 변경만 — 요청 안 한 캐시/추상화/스캐폴딩 추가 금지  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/memory/feedback_minimal_change_no_overeng.md` · grounding `execution_evidence` · 중요도 4)
- **feedback-no-schema-on-qa-subagent** [harness] — QA 서브에이전트에 structured output schema 를 강제하면 피드백 저장 단계가 통째로 스킵된다 — 판정은 남고 데이터 풀은 굶는다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/memory/feedback_no_schema_on_qa_subagent.md` · grounding `execution_evidence` · 중요도 4)
- **feedback_error_verdict_use_probe_log** [harness][flutter][design] — 앱 런타임 에러 유무 판정은 get_runtime_events 말고 fp-framework-errors.log 를 1차 자료로 쓴다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_error_verdict_use_probe_log.md` · grounding `execution_evidence` · 중요도 4)
- **feedback_mcp_capture_stable_filename** [harness][tooling][flutter][design] — MCP screenshot_widget 은 ref 기반 파일명이라 다음 캡처가 덮어쓴다 — 증거는 고정 이름으로 복사해 둘 것  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_mcp_capture_stable_filename.md` · grounding `execution_evidence` · 중요도 4)
- **feedback_measure_where_value_reaches_user** [harness][bambu] — 계약 측정 지점을 정하기 전에 그 함수의 반환값이 사용자에게 실제로 도달하는지 호출 그래프로 확인하라 — 죽은 경로를 지목하면 잘못된 구현이 PASS 한다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_measure_where_value_reaches_user.md` · grounding `execution_evidence` · 중요도 4)
- **feedback_morph_codex_review** [harness][design][research][flutter] — 모프/전환 애니메이션은 구현 후 사용자 확인을 요청하기 전에 codex 검토를 먼저 거친다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_morph_codex_review.md` · grounding `mixed` · 중요도 4)
- **feedback_no_sprint_contract** [harness][design] — 2026-08-14부터 fit-pal은 Sprint Contract 없이 진행 — 사용자 명시 지시  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_no_sprint_contract.md` · grounding `mixed` · 중요도 4)
- **feedback-verify-ci-logs-not-handoff** [harness][infra][flutter][rust] — CI 실패 원인은 핸드오프/추측이 아니라 실제 run 로그로 확인하라  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_verify_ci_logs_not_handoff.md` · grounding `execution_evidence` · 중요도 4)
- **ephemeral-tests** [harness][bambu][flutter][design] — app_kiosk 테스트 파일은 스프린트 검증용 일회성 — 사용자가 의도적으로 삭제, 재생성 금지, git 커밋 제안 금지  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-apps/memory/feedback_ephemeral_tests.md` · grounding `user_correction` · 중요도 3)
- **feedback-kaizen-phase-triage** [harness][flutter][design][react][reflect] — 카이젠 오케스트레이션은 전체 default 대신 §0 신선도+신호 농도로 Phase 선별부터  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/memory/feedback_kaizen_phase_triage.md` · grounding `execution_evidence` · 중요도 3)
- **feedback_amendment_commit_separate** [harness][design][bambu] — sprint-amendments 사이드카는 코드 커밋과 분리해서 커밋해야 AR-01 화이트리스트를 안 깬다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_amendment_commit_separate.md` · grounding `execution_evidence` · 중요도 3)
- **feedback_english_identifiers** [harness][flutter][backend][rust] — 식별자(함수·변수·테스트 함수명)는 항상 영어. 한국어는 주석/doc/에러메시지만. "주변 코드 따라가기"가 이걸 못 덮는다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_english_identifiers.md` · grounding `mixed` · 중요도 3)
- **feedback_pipe_masks_exit_code** [harness][rust][infra] — 검증 명령을 파이프로 tail/grep 하면 exit code가 가려져 false-positive PASS가 난다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_pipe_masks_exit_code.md` · grounding `execution_evidence` · 중요도 3)
- **feedback_run_guard_appenv_bug** [harness][backend][infra][rust] — harness run-guard 훅이 APP_ENV=dev cargo run 을 차단하는 버그 — 빌드된 바이너리 직접 실행으로 우회  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_run_guard_appenv_bug.md` · grounding `execution_evidence` · 중요도 3)
- **feedback-scoped-format-only** [harness][flutter] — dart format을 디렉토리 단위로 돌리면 손대지 않은 파일까지 재포맷되어 변경 범위가 오염된다 — 편집한 파일만 지정하라  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-flutter-playwright/memory/feedback_scoped_format_only.md` · grounding `execution_evidence` · 중요도 3)
- **feedback-no-read-env** [infra][design][backend][reflect][onboarding] — .env / .env.fastlane / .env.* 등 시크릿이 들어 있는 환경 파일은 Read 도구로 직접 열지 마라  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_no_read_env.md` · grounding `user_correction` · 중요도 3)
- **feedback-console-ui-verify** [onboarding][research][design][infra][harness][reflect] — 외부 콘솔(Play, App Store Connect, GCP, AWS 등) UI 안내 시 반드시 공식 docs 또는 fastlane docs WebFetch 후 정확한 메뉴 경로 인용. 추측 금지.  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_console_ui_verify.md` · grounding `mixed` · 중요도 3)
- **feedback-terminology-glossary** [onboarding][backend][design][planning] — 셋업/온보딩 가이드 등 문서 작성 시 영어 약자가 처음 등장하면 한글 풀이를 병기한다  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_terminology_glossary.md` · grounding `user_correction` · 중요도 3)
- **codex-research-foreground** [research][harness] — codex 리서치 위임은 항상 foreground(블로킹)로 실행 — 백그라운드는 hang 시 결과가 유기됨  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-apps/memory/feedback_codex_research_foreground.md` · grounding `mixed` · 중요도 3)
- **feedback-codex-foreground-call-direct** [research][infra] — codex 는 자주 죽으므로 항상 foreground — companion 스크립트를 --background 없이 Bash 로 직접 호출하라 (에이전트 백그라운드는 무관)  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/memory/feedback_codex_foreground_call_direct.md` · grounding `user_correction` · 중요도 3)
- **feedback-codex-research-backgrounded** [research] — codex-rescue가 foreground 지정을 무시하고 백그라운드 태스크로 던질 수 있다 — companion 스크립트로 직접 회수하라  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-flutter-playwright/memory/feedback_codex_research_backgrounded.md` · grounding `execution_evidence` · 중요도 3)
- **feedback_e2e_use_mcp_dont_flail** [tooling][design][backend][flutter][infra][reflect][harness] — 실기/시뮬 e2e 테스트는 fitpal-mobile MCP로 직접 구동하라 — 넘겨짚고 포기하지 말 것. 반복 지적된 최악 마찰  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_e2e_use_mcp_dont_flail.md` · grounding `mixed` · 중요도 4)
- **feedback_hot_reload_log_string** [tooling][flutter][harness] — hot reload 적재 확인 문자열은 "Reloaded application in"이 아니라 "Reloaded N of M libraries in" (Flutter 3.41)  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_hot_reload_log_string.md` · grounding `execution_evidence` · 중요도 4)
- **feedback_isolate_the_instrument_too** [tooling][harness][flutter] — 격리 재현을 주장할 때 코드·기기·로그뿐 아니라 조작 수단(계측 도구)도 격리했는지 확인하라  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_isolate_the_instrument_too.md` · grounding `execution_evidence` · 중요도 4)
- **feedback_mcp_dynamic_tools_need_hot_restart** [tooling][flutter][backend][harness][design] — MCP 동적 도구 0개는 서버가 아니라 앱이 등록을 재전송해야 복구된다 — pkill 말고 hot restart  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_mcp_dynamic_tools_need_hot_restart.md` · grounding `execution_evidence` · 중요도 4)
- **feedback-flutter-playwright-only** [tooling][harness][flutter][backend][reflect][design] — 앱/카탈로그 검증에 범용 playwright MCP 금지 — fitpal-web/mobile 전용, 동적도구 0이면 풀로드 후 pkill 재spawn  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_flutter_playwright_only.md` · grounding `mixed` · 중요도 3)
- **mcp** [tooling][flutter][harness][backend] — flutter-playwright MCP로 앱 검증 시 full flutter run 재실행 금지 — VM주소 변경 + 서버 kill이 동적도구 채널을 끊는다. hot restart만 사용.  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_mcp_runtime_verify_no_relaunch.md` · grounding `execution_evidence` · 중요도 3)
- **feedback_mcp_vmservice_file_race** [tooling][flutter][harness][backend][reflect] — 병렬 세션/여러 기기가 같은 vmservice-out-file을 경합하면 MCP가 엉뚱한 기기에 attach — 도구 0/flip-flop  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_mcp_vmservice_file_race.md` · grounding `execution_evidence` · 중요도 3)
- **feedback_mcp_widget_absent_check_route** [tooling][flutter][design][reflect] — MCP find_widget 0매치는 도구 버그가 아니라 "그 화면에 진짜 없음" 신호 — pushed route 여부부터 확인하라  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_mcp_widget_absent_check_route.md` · grounding `execution_evidence` · 중요도 3)
- **feedback_runtime_test_last** [tooling][harness][flutter][reflect][bambu][design] — 실기 구동(앱 launch) e2e 테스트는 스프린트마다 하지 말고 기능 전체(멀티 스프린트) 맨 끝에 한 번에  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_runtime_test_last.md` · grounding `user_correction` · 중요도 3)
- **feedback_verify_build_freshness_before_e2e** [tooling][backend][harness][flutter][design] — 실기 e2e 전에 앱**과 서버** 둘 다 검증 대상 코드로 빌드됐는지 기동시각 vs 커밋시각으로 확인  (`~/.claude/projects/-Users-jackson-Hub-10-Dev-fit-pal/memory/feedback_verify_build_freshness_before_e2e.md` · grounding `execution_evidence` · 중요도 3)

## 1. 글로벌 Evaluator Feedback

- 경로: `/Users/jackson/.harness/feedback/evaluator`
- 총 파일: **335**

### Verdict 분포

- **APPROVE**: 195
- **REJECT**: 133
- **UNKNOWN**: 7

### Skill 분포

- `qa-evaluator`: 335

### Project 분포 (canonical — allowlist 병합 후)

canonical 기준은 **writer 쪽 identity** 다 — `harness/scripts/save-feedback.sh` 가 CONTRACT_ROOT 의 git root basename 으로 계산하는 이름. 집계가 다른 방향으로 정규화하면 같은 프로젝트가 신·구 버킷으로 영구 분열하므로 writer 에 맞춘다 (예: `fit-pal/app`·`fit-pal/server` 는 .git 이 없어 git root 가 `fit-pal` 하나다).

병합은 `PROJECT_NAME_ALIASES` **명시 allowlist** 로만 한다. 이름 유사도/fuzzy 매칭은 쓰지 않는다. 병합된 그룹은 서브프로젝트 구분이 사라지지 않도록 원본 이름 내역을 `←` 뒤에 함께 보여준다.

- `fit-pal`: 173  ← `fit-pal` 104, `fit-pal-app` 37, `fit-pal-server` 17, `fit-pal/app` 6, `fit-pal/server` 5, `fitpal-server` 4
- `claude-plugins`: 147  ← `claude-plugins` 143, `bambu-kit-v0.4.0-9mm-craft-knife` 1, `claude-plugins / react-kit phase10-research kaizen` 1, `bambu-kit/bambu-print-profile v0.4.1` 1, `bambu-kit/bambu-print-profile` 1
- `flutter_playwright`: 13
- `fit-pal-flutter`: 1
- `iyaki-zip-dev`: 1

### Project 분포 (raw `project_name` — 병합 전 원본)

병합이 원본을 감추지 않도록 그대로 남긴다. canonical 과 raw 개수가 다르면 그 차이가 곧 레거시 표기 흔들림의 규모다.

- `claude-plugins`: 143
- `fit-pal`: 104
- `fit-pal-app`: 37  → merged into `fit-pal`
- `fit-pal-server`: 17  → merged into `fit-pal`
- `flutter_playwright`: 13
- `fit-pal/app`: 6  → merged into `fit-pal`
- `fit-pal/server`: 5  → merged into `fit-pal`
- `fitpal-server`: 4  → merged into `fit-pal`
- `fit-pal-flutter`: 1
- `bambu-kit-v0.4.0-9mm-craft-knife`: 1  → merged into `claude-plugins`
- `iyaki-zip-dev`: 1
- `claude-plugins / react-kit phase10-research kaizen`: 1  → merged into `claude-plugins`
- `bambu-kit/bambu-print-profile v0.4.1`: 1  → merged into `claude-plugins`
- `bambu-kit/bambu-print-profile`: 1  → merged into `claude-plugins`

- raw 이름 종류: **14** → canonical 그룹: **5** (allowlist 적용 파일 73건)

### schema_version / 세대 분포

`schema_version` 과 결정론적 identity 필드(`draft_project_name`, `draft_project_hash`, `sprint_slug`, `contract_path`) 유무로 신·구 피드백을 구분한다. `legacy-identity` 는 `project_name`/`project_hash` 가 cwd 기준으로 계산되던 시기의 기록이라 위 raw 분포의 표기 흔들림 원인이 된다.

- schema_version `1`: 335
  - 정규화 전 원본 표기: `1` 326, `'1.0'` 6, `'1'` 3

- v1 · legacy-identity: 244
- v1 · deterministic-identity: 91

#### `contract_path` 귀속 근거

`save-feedback.sh` 는 `HARNESS_CONTRACT` / draft 값이 없으면 계약 경로를 **추측**하고 `contract_path_inferred: true` 를 남긴다. `inferred` 비율이 높으면 피드백이 stale 한 plain 계약에 오귀속되고 있을 수 있다.

- explicit(명시): 91

### 최근 REJECT 사유 (Top 20)

- [2026-08-14] **fit-pal**: UI-07: ChatQuoteBlock grep count 3 < 4 (공유 위젯 _QuoteRow 가 5/6 시안에서 단일 호출점 재사용, 텍스트 매치 카운트가 사용 시안 수를 반영 못함)
- [2026-08-14] **fit-pal**: UI-01: 좌측 라벨 열이 '최고 무게'를 온전히 렌더하지 않음 — '최고'로 축약, 온전한 문자열은 별개 위치(그래프 위 캡션)에만 존재. 계약이 명시한 위치 요구 미충족.
- [2026-08-14] **fit-pal**: RE-02 FAIL: _SectionTitle 이 aqua_weak_mockups.dart 것과 바이트 단위로 동일하게 재선언됨 (재사용 대신 복제, 프로젝트 내 3번째 중복)
- [2026-08-14] **fit-pal**: AR-01: 금지 목록 파일 chat_gt_mockups.dart 가 이번 스프린트 중 수정됨(chatQuoteToneColor 신설, ChatEmbossDivider onAccent 필수 파라미터 추가). amendment A-01 이 화이트리스트 확대를 시도하나 relaxing 유형이라 PASS 근거로 쓸 수 없음 — 원 조건 문자 그대로 FAIL
- [2026-08-14] **fit-pal**: AR-01 미검증: 커밋이 아직 생성되지 않아 git show --stat 오라클을 실행할 수 없음
- [2026-08-14] **claude-plugins**: [ER-01] 이번 사이클 도입 외부 URL이 근거파일/원본에 실재해야 하는데, 4건(doc.rust-lang.org/cargo 2건, docs.rs/anyhow, docs.rs/sqlx 각 1건)이 미추적으로 확인됨. 이 4건은 실제 산출물(docs/rust-kit/*.html)에서는 이미 제거된 상태지만, iter3 자신의 FAIL 피드백 파일(.har
- [2026-08-14] **claude-plugins**: SK-03: docs/superpowers/plans/ 레거시 기획 문서 2곳에 WCAG AA와 44×44pt 터치 타겟이 레벨 귀속 없이 병기되어 잔존 (Phase 6이 design-kit/ 안쪽만 고치고 놓친 sibling residue)
- [2026-08-14] **claude-plugins**: SC-04: 음성 대조(negative control) 등식이 문자 그대로 성립하지 않음 — alias/verb-synonym 2종만 제거한 맵으로 재실행 시 클러스터 합산 87 vs 원시 단독 86 (87≠86). 주 측정(클러스터 합산 125 > 원시 단독 86)은 PASS 이나, 계약이 명시한 음성 대조 절이 문자 그대로 미충족되어 CheckEval 
- [2026-08-14] **claude-plugins**: SC-04 goal-tag 조건의 음성 대조(negative control) 서브체크가 문자 그대로 불충족 — alias/verb-synonym 행을 제거한 lemma map으로 실 로그 전량(14파일)을 재실행하면 skipped-required-api-doc-check 클러스터 합산이 88인데 원시 단독 count는 87로, 조건이 요구하는 '두 값이 같
- [2026-08-14] **claude-plugins**: RE-01: Phase 3 canonical User-Reported Failure Protocol이 backend-kit/planning-kit/react-kit/rust-kit reviewer 4/6에 전혀 인용되지 않음 (infra-kit만 완전 복제, design-kit는 상위 짝을 인용하나 qa-evaluation-guide.md canonical
- [2026-08-14] **claude-plugins**: ER-01: docs-site 재생성 커밋(36b3e86)이 도입한 rust-kit 관련 doc.rs/cargo 인용 URL 4건이 evidence 파일·main 원본 어디에도 추적되지 않음 (disclosure 절차 없음)
- [2026-08-14] **claude-plugins**: AR-03: '표준으로 강제하지 않는다' 문장이 속한 문단에 도구 4종(Playwright/Chromatic/Percy/BackstopJS)이 literal 로 열거되지 않음 — 도구명은 인접한 이전 문단(빈 줄로 분리)에만 존재. 계약 [exact] 측정문의 '같은 문단에 열거' 요건 미충족 (python 문단 분리로 확인, 4개 토큰 전부 False)
- [2026-08-14] **claude-plugins**: AP-03 FAIL — bare code fence 신규 미도입 조건의 clause 2(`git diff -U0 -- bambu-kit | grep -c '^+```$'`)가 여는/닫는 fence를 구분하지 않아, 언어 힌트가 정상 부착된 신규 코드블록을 추가하기만 해도 항상 위반으로 잡히는 구조적 측정 결함. 구현 커밋(04641f7) diff 기준 실측
- [2026-08-13] **flutter_playwright**: SG-04: same gap as SG-03 for the inverse case ('registerDynamics absent -> no pull'); only the boolean predicate is asserted, not pullCalls==0.
- [2026-08-13] **flutter_playwright**: SG-03: readiness gate ('extensionRPCs already contains registerDynamics -> immediate pull') is only tested via the boolean predicate resolveRegistrationReadiness; no test asserts an actual pull occurr
- [2026-08-13] **flutter_playwright**: SG-01~SG-04: ServiceExtensionAdded → pull 트리거 프로덕션 메서드(handleServiceExtensionAdded)가 어떤 테스트에서도 호출되지 않음
- [2026-08-13] **flutter_playwright**: RE-02: McpSessionRegistry.focusTtl은 GlowConfig.connectedWindow를 참조하지 않고 독립된 const Duration(seconds: 30)을 새로 생성함 (mcp_session_registry.dart:64). 계약 문언 '새 상수를 만들면 FAIL'을 문자 그대로 위반.
- [2026-08-13] **flutter_playwright**: PR-03 FAIL: same root cause hits terminateProcessTree()'s 'await process.exitCode.timeout(gracePeriod)' — confirmed via live SIGTERM test: all 4 descendant processes (flutter run, frontend_server, tes
- [2026-08-13] **flutter_playwright**: PR-01 FAIL: resolveInitialUri() crashes with uncaught StateError ('Bad state: Process is detached') before ever completing the app.debugPort wait — process.exitCode is inaccessible on ProcessStartMode
- [2026-08-13] **flutter_playwright**: AP-01: registerToolsAndResourcesGuarded()의 catch가 실패를 삼켜 refreshClientTools가 pull 실패를 성공으로 응답

### 최근 Improvement Suggestions (Top 15)

- [2026-08-14] **fit-pal**: [프로세스] 실시간 사용자 교정(점선+그래프까지만)이 코드(adc31e6a)에는 반영됐으나 계약/amendment 문서에 기록되지 않음 — sprint-amendments-history-stock-guide.md 생성 권장
- [2026-08-14] **fit-pal**: [UI-07] 측정절의 특정 행 예시(1세트)를 '선택된 임의의 행'으로 일반화하면 해석 여지가 줄어든다
- [2026-08-14] **fit-pal**: [UI-07] 측정-중복 — grep -c 텍스트 매치 대신 find.byType(ChatQuoteBlock) 인스턴스 수로 측정할 것을 권고
- [2026-08-14] **fit-pal**: [UI-07] 측정-예시-모호 (2회째) — '1세트 선택 후' 특정 예시 대신 '선택된 임의의 행'으로 일반화 권고
- [2026-08-14] **fit-pal**: [UI-01] 측정절에 렌더 위치(좌측 라벨 열 vs 임의 위치)를 명시적으로 고정해야 향후 유사한 문자열 재배치 우회를 차단한다
- [2026-08-14] **fit-pal**: [RE-02] _SectionTitle 을 lib/catalog/mockups/ 공용 위치로 추출하고 aqua_weak_mockups.dart/history_mockups.dart/aqua_cta_tone_mockups.dart 3파일이 import 하도록 정리
- [2026-08-14] **fit-pal**: [ER-01/UI-03] all_mockups_render_test.dart 와 _pumpBoard 헬퍼의 ListView>ConstrainedBox(maxWidth:400) 패턴이 tight cross-axis 때문에 실제로 400px 을 강제하지 못함(실측 1200) — 프로젝트 전역 카탈로그 테스트 인프라 후속 수정 권장
- [2026-08-14] **fit-pal**: [DG-03] 측정-수단-부재 — Chrome MCP 캡처 실패 시 위젯테스트 RepaintBoundary PNG 캡처를 2차 오라클로 계약에 명시하면 병렬 세션 자원 경합 상황에서도 대체 경로가 생긴다
- [2026-08-14] **fit-pal**: [DG-03] 산출물-경로-공유충돌 — 세션별 vmservice 파일 분리 또는 DG-03 조건 완화 문구 검토
- [2026-08-14] **fit-pal**: [AR-01] 범위-미명시 — 확정 파일 헬퍼 확장이 필요한 상황을 계약 작성 시점에 예견 못함. carve-out을 인라인하거나 화이트리스트에 조건부 포함을 권고
- [2026-08-14] **fit-pal**: DG-04 조건에 fallback 검증 수단(정적 render test 대체 가능 여부)을 계약 본문에 명시하면 다음 스프린트부터 [미검증] 여부 판단이 빨라진다.
- [2026-08-14] **claude-plugins**: 오케스트레이터가 QA 서브에이전트를 structured output schema 로 강제 호출하면 에이전트가 출력 계약만 만족시키고 종료하여 Step 8 피드백 저장 단계(로컬+글로벌 저장, verify-feedback.sh 검증)가 스킵될 수 있다. structured output 요구와 별개로 저장 단계 실행 여부를 오케스트레이터가 사후 확인하는 게이트
- [2026-08-14] **claude-plugins**: git status/diff 기반 measure clause들의 상태 전제(Given)를 조건 단위가 아니라 계약 헤더 레벨에서 1회 공통 선언하는 패턴을 권장 — AR-01만 명시하고 AP-01/AP-03/RE-01은 암묵 전제라 사후 재평가 시 상태 해석이 매번 필요했다
- [2026-08-14] **claude-plugins**: [오케스트레이터] structured output schema를 QA 서브에이전트에 강제하면 피드백 저장 단계(Step 8)가 스킵될 수 있다 — 이번 재평가의 근본원인. 스키마 강제와 별개로 Step 8(글로벌 저장)이 항상 실행되도록 오케스트레이터 프롬프트에 명시하거나, 저장을 오케스트레이터 자신이 후처리로 수행하는 방식을 검토할 것.
- [2026-08-14] **claude-plugins**: [범위 경계] 계약 결함(비차단) — '## 2. 스킬 9가지 유형 체크리스트' 헤더 문자열을 리터럴 참조한다고 명시한 6개 외부 surface(CLAUDE.md 등) 중 재검색 시 문자 그대로 일치하는 곳이 0건이었다. 조건 판정에는 영향 없는 배경 서술이지만 다음 계약 작성 시 인용 근거를 실제 grep 결과로 재확인 후 기재할 것을 권장

## 2. 외부 프로젝트 (`Hub/10_Dev`) 피드백

- Hub 루트: `/Users/jackson/Hub/10_Dev`
- 발견된 프로젝트: **14**

- 수집된 sprint-feedback 파일: **65** (그중 접미형 `sprint-feedback-<slug>.md`: **52**)

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

### `fit-pal`

- 경로: `/Users/jackson/Hub/10_Dev/fit-pal`
- sprint-feedback 파일: 1개 (총 121 lines)
- history sprint-contracts: 37
- 최근 contracts:
  - 20260623-1118-sprint-contract.md
  - 20260625-1850-sprint-contract.md
  - 20260626-1507-sprint-contract.md
  - 20260723-1444-sprint-contract.md
  - 20260727-1812-sprint-contract.md
- 파일별 내역:
  - `sprint-feedback.md` — plain (슬러그 없음), 121 lines, mtime 2026-07-27T19:10:10

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

### `fit-pal/app`

- 경로: `/Users/jackson/Hub/10_Dev/fit-pal/app`
- sprint-feedback 파일: 35개 (총 5557 lines)
- history sprint-contracts: 49
- 접미형 슬러그: `history-stock-select`, `post-card-mockups`, `chat-reply-stacked`, `aqua-cta-tone`, `history-stock-guide`, `history-stock-axis`, `history-stock-total`, `history-stock-refine`, `history-stock-delta`, `history-record-graph`, `chat-send-morph-gt`, `chat-send-morph`, `chat-tray-mockups`, `history-session-row`, `app-post-like-notification`, `history-mockups-round2`, `history-screen-mockups`, `group-chip-thumb-triangle`, `chat-bubble-mockups`, `timer-autocomplete-record`, `player-session-ux`, `dev-baseurl-override`, `bodymap`, `figma-box-path-shape`, `statistics-tab`, `statistics-aggregation`, `statistics-catalog`, `notif-reliability`, `ws6-carryover`, `emoji-picker`, `workout-sync-utc`, `s6`, `s8`, `player-launch`
- 최근 contracts:
  - 20260714-1613-sprint-contract.md
  - 20260716-1822-sprint-contract.md
  - 20260721-1026-sprint-contract.md
  - 20260723-1453-sprint-contract.md
  - 20260723-1809-sprint-contract.md
- 파일별 내역:
  - `sprint-feedback.md` — plain (슬러그 없음), 71 lines, mtime 2026-07-24T20:48:28
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
  - `sprint-feedback-history-session-row.md` — slug=`history-session-row`, 236 lines, mtime 2026-08-13T14:56:50
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

<details><summary>sprint-feedback-chat-reply-stacked.md 앞부분</summary>

```markdown
# Sprint Feedback
Feature: 답장 입력바 — 2층 한 덩어리 안에서 갈라지는 6축
Evaluated: 2026-08-14 11:30
Verdict: REJECT
Iteration: 1

## Contract Fingerprint
- path: /Users/jackson/Hub/10_Dev/fit-pal/app/.harness/sprint-contract-chat-reply-stacked.md
- sha256: 91366efd50d9def874b43991b44f96b587d7148d459741e82e73c7064234d967
- status: active
- slug: chat-reply-stacked
- contract_root: /Users/jackson/Hub/10_Dev/fit-pal/app
- contract_root_unconfigured: false
- 선택 근거: 명시 경로(작업 지시에 계약 경로 직접 지정) — ladder 1 상당
- legacy_contract_used: false
- 재확인(Step 5): 일치
- status_transition: skipped (verdict=REJECT)

## Amendments
- amendments: 3 (A-01, A-02, A-03)
```

</details>

<details><summary>sprint-feedback-aqua-cta-tone.md 앞부분</summary>

```markdown
# Sprint Feedback
Feature: 아쿠아 CTA 톤다운 시안 보드 (1단계: 카탈로그 시연까지)
Evaluated: 2026-08-14 11:45
Verdict: REJECT
Iteration: 1

## Contract Fingerprint
- path: /Users/jackson/Hub/10_Dev/fit-pal/app/.harness/sprint-contract-aqua-cta-tone.md
- sha256: 5ccc3da3edb7b0e7bf5f1924853db47cf991c53200eb77a709ff8124298593e8
- status: active
- slug: aqua-cta-tone
- contract_root: /Users/jackson/Hub/10_Dev/fit-pal/app
- contract_root_unconfigured: false
- 선택 근거: ladder 1 명시경로 (HARNESS_CONTRACT 형태로 경로가 지정됨)
- legacy_contract_used: false
- 재확인(Step 5): 일치
- status_transition: skipped (verdict=REJECT)

## Amendments
- amendments: 0 (사이드카 `.harness/sprint-amendments-aqua-cta-tone.md` 없음)
```

</details>
- (본문 미리보기는 최신 5개만 표시 — 나머지 30개는 위 파일별 내역 참조)

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
- sprint-feedback 파일: 4개 (총 866 lines)
- history sprint-contracts: 11
- 접미형 슬러그: `mcp-session-resilience`, `mcp-session-isolation`, `mcp-overlay-isolation`
- 최근 contracts:
  - 20260422-0945-sprint-contract.md
  - 20260422-phase-a-sprint-contract.md
  - 20260422-phase-b-sprint-contract.md
  - 20260507-1823-sprint-contract.md
  - 20260610-1042-sprint-contract.md
- 파일별 내역:
  - `sprint-feedback.md` — plain (슬러그 없음), 332 lines, mtime 2026-07-28T00:44:15
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

<details><summary>sprint-feedback-mcp-session-resilience.md 앞부분</summary>

```markdown
# Sprint Feedback
Feature: 동적 도구 등록 복구 경로
Evaluated: 2026-08-13 15:10
Verdict: APPROVE
Iteration: 3

## Contract Fingerprint
- path: /Users/jackson/Hub/10_Dev/flutter_playwright/.harness/sprint-contract-mcp-session-resilience.md
- sha256: afa01f1d94a1f681197a5ffd9b1ded3f49d4aab4e06aee9a7d796bbef8bbdc34
- status: active
- slug: mcp-session-resilience
- contract_root: /Users/jackson/Hub/10_Dev/flutter_playwright
- contract_root_unconfigured: true (project.yaml 없음 — 범용 기본값으로 검증. `/harness init` 권장)
- 선택 근거: ladder 2 (세션소유 active 유일, owner_session == CLAUDE_CODE_SESSION_ID)
- legacy_contract_used: false
- 재확인(Step 5): 일치 (sha256/status 동일, TOCTOU 없음)
- status_transition: active -> done (verdict=APPROVE)

## Amendments
- amendments: 0 (사이드카 `.harness/sprint-amendments-mcp-session-resilience.md` 부재)
```

</details>

<details><summary>sprint-feedback-mcp-session-isolation.md 앞부분</summary>

```markdown
# Sprint Feedback
Feature: 병렬 세션 인스턴스 격리
Evaluated: 2026-08-13 16:30
Verdict: APPROVE
Iteration: 3

## Contract Fingerprint
- path: /Users/jackson/Hub/10_Dev/flutter_playwright/.harness/sprint-contract-mcp-session-isolation.md
- sha256: 672908c6e05eba73f2bec0748a1efce155918b3cd5a40e1516a3f4c11015d384
- status: active
- slug: mcp-session-isolation
- contract_root: /Users/jackson/Hub/10_Dev/flutter_playwright
- contract_root_unconfigured: true (.harness/project.yaml 없음 — 범용 기본값으로 검증. `/harness init` 권장)
- 선택 근거: ladder 1 명시경로 (session_id도 owner_session과 일치, ladder 2로도 유일하게 선택됨)
- legacy_contract_used: false
- 재확인(Step 5): 일치 (sha256/status/HEAD 동일, git status 변동 없음)
- status_transition: active -> done (verdict=APPROVE)

## ⚠️ 최상단 경고 — RY-01~04 [low-confidence] (3회째 지적, 계약 수정 권고)
`InstanceRegistry`/`canAttachToSlot`가 여전히 프로덕션 spawn 경로에 배선되지 않았다
```

</details>

<details><summary>sprint-feedback-mcp-overlay-isolation.md 앞부분</summary>

```markdown
# Sprint Feedback
Feature: MCP 오버레이 격리 + 세션 스트립
Evaluated: 2026-08-13 20:05
Verdict: APPROVE
Iteration: 2

## Contract Fingerprint
- path: /Users/jackson/Hub/10_Dev/flutter_playwright/.harness/sprint-contract-mcp-overlay-isolation.md
- sha256: 161623a2535a4b7843ea0726e58971d56e60a9c555fc9bd39522ca4968014def
- status: active
- slug: mcp-overlay-isolation
- contract_root: /Users/jackson/Hub/10_Dev/flutter_playwright
- contract_root_unconfigured: false
- 선택 근거: 명시 경로 (평가 태스크가 계약 절대경로를 직접 지정)
- legacy_contract_used: false
- 재확인(Step 5): 일치
- status_transition: active -> done (verdict=APPROVE)

## Amendments
- amendments: 2 (변경 없음, iteration 1과 동일 — 이번 iteration에서 신규 amendment 없음)
```

</details>

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
  V2 templates       0 files — SKIP (no templates/)
  V3 refs            0 links — OK
  V4 triggers        18 keywords — OK
  V5 placeholders    0 found — OK
  V6 code-fence      0 bare — OK
  V7 plugin-json     v0.3.0 matches marketplace — OK
  V8 hook-exec       no hooks.json — OK

=== infra-kit ===
  V1 frontmatter     4 skills + 1 agent — OK
  V2 templates       0 files — SKIP (no templates/)
  V3 refs            0 links — OK
  V4 triggers        19 keywords — OK
  V5 placeholders    0 found — OK
  V6 code-fence      0 bare — OK
  V7 plugin-json     v0.3.0 matches marketplace — OK
  V8 hook-exec       no hooks.json — OK

=== rust-kit ===
  V1 frontmatter     16 skills + 1 agent — OK
  V2 templates       1 parsed, 4 skipped (ts/js) — OK
  V3 refs            0 links — OK
  V4 triggers        79 keywords — OK
  V5 placeholders    0 found — OK
  V6 code-fence      0 bare — OK
  V7 plugin-json     v0.3.0 matches marketplace — OK
  V8 hook-exec       no hooks.json — OK

=== react-kit ===
  V1 frontmatter     21 skills + 3 agents — OK
  V2 templates       5 parsed, 4 skipped (ts/js) — OK
  V3 refs            0 links — OK
  V4 triggers        157 keywords — OK
  V5 placeholders    0 found — OK
  V6 code-fence      0 bare — OK
  V7 plugin-json     v0.3.0 matches marketplace — OK
  V8 hook-exec       no hooks.json — OK

=== planning-kit ===
  V1 frontmatter     12 skills + 1 agent — OK
  V2 templates       0 files — SKIP (no templates/)
  V3 refs            0 links — OK
  V4 triggers        95 keywords — OK
  V5 placeholders    0 found — OK
  V6 code-fence      0 bare — OK
  V7 plugin-json     v0.5.0 matches marketplace — OK
  V8 hook-exec       no hooks.json — OK

=== reflect-kit ===
  V1 frontmatter     4 skills — OK
  V2 templates       0 files — SKIP (no templates/)
  V3 refs            0 links — OK
  V4 triggers        25 keywords — OK
  V5 placeholders    0 found — OK
  V6 code-fence      0 bare — OK
  V7 plugin-json     v0.6.0 matches marketplace — OK
  V8 hook-exec       직접 실행 hook 스크립트 없음 — OK

=== bambu-kit ===
  V1 frontmatter     1 skill — OK
  V2 templates       0 files — SKIP (no templates/)
  V3 refs            0 links — OK
  V4 triggers        5 keywords — OK
  V5 placeholders    0 found — OK
  V6 code-fence      0 bare — OK
  V7 plugin-json     v0.6.0 matches marketplace — OK
  V8 hook-exec       no hooks.json — OK

=== onboarding-kit ===
  V1 frontmatter     1 skill — OK
  V2 templates       0 files — SKIP (no templates/)
  V3 refs            0 links — OK
  V4 triggers        8 keywords — OK
  V5 placeholders    0 found — OK
  V6 code-fence      0 bare — OK
  V7 plugin-json     v0.3.0 matches marketplace — OK
  V8 hook-exec       no hooks.json — OK

Total: 11 plugins, 11 OK
Exit: 0
```


## 6. Phase 별 참조 가이드

각 Phase subagent 는 아래 매핑을 참고하여 자신의 범위에 맞는 섹션을 우선 읽는다. §0 (/insights) 가 존재할 때는 **모든 Phase** 가 §0 을 최우선 참조한다.

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

