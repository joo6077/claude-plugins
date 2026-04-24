# Kaizen Data Pool

Generated: 2026-04-24T10:48:01
Generator: `scripts/collect-kaizen-data.py`

카이젠 오케스트레이션의 Phase 별 서브에이전트가 참조할 통합 데이터 풀이다. 이 파일은 `scripts/collect-kaizen-data.py` 로 재생성된다 — 수동 수정 금지.

## 1. 글로벌 Evaluator Feedback

- 경로: `/Users/jackson/.harness/feedback/evaluator`
- 총 파일: **138**

### Verdict 분포

- **APPROVE**: 77
- **REJECT**: 61

### Skill 분포

- `qa-evaluator`: 138

### Project 분포

- `claude-plugins`: 109
- `fit-pal`: 19
- `fit-pal-server`: 4
- `fit-pal-flutter`: 1
- `fit-pal-app`: 1
- `fitpal-server`: 1
- `iyaki-zip-dev`: 1
- `claude-plugins / react-kit phase10-research kaizen`: 1
- `flutter_playwright`: 1

### 최근 REJECT 사유 (Top 20)

- [2026-04-23] **flutter_playwright**: AR-02: toolkit evaluate 단독 동사 네이밍
- [2026-04-23] **flutter_playwright**: AR-01: 도구 수 49개, 허용 범위 45~47 초과
- [2026-04-22] **fit-pal-server**: API-02: traces_sample_rate 필드 타입 f64 (계약 요구 f32). #[derive(Default)] 잔존 + 수동 impl Default 없음. 계약 패치 후 코드 미업데이트.
- [2026-04-21] **fit-pal-server**: LG-04: ScheduleNotification enum 에 group_id 필드 없어 payload 에 group_id 미포함. 계약 명시 payload(group_id/slot_id/outcome?) 불충족.
- [2026-04-21] **fit-pal-server**: LG-02: list_member_ids 가 GroupPort::list_members(Uuid::nil(), ...) 호출 → find_active_member 에서 항상 Forbidden 반환. 내부 컨텍스트 동작 불가.
- [2026-04-21] **fit-pal**: UI-04: [미검증] MCP Figma read-back 불가 (mcp_server=null)
- [2026-04-21] **fit-pal**: RE-02: ensure_slots_exist 시그니처 impl ConnectionTrait + Send (계약 명시: + Send + Sync)
- [2026-04-21] **fit-pal**: LG-04: [미검증] Figma 노드 read-back 불가 (mcp_server=null)
- [2026-04-21] **fit-pal**: AP-02: lazy_generation.rs:85 .expect() 프로덕션 경로 — 계약 허용 예외 목록(unwrap_or/and_hms_opt known-valid) 미포함
- [2026-04-20] **fit-pal**: LG-04: fitpal-routine 크레이트 미구현 — 7개 DTO 없음 (Task 2~3 미완료)
- [2026-04-20] **fit-pal**: LG-03: fitpal-routine 크레이트 미구현 — SkipPolicyMode 없음 (Task 2~3 미완료)
- [2026-04-20] **fit-pal**: DG-03: cargo test --workspace에서 fitpal-message 통합 테스트 3건 FAIL (pre-existing, sprint scope_out). DG-03 계약이 --workspace를 literal 명시하므로 FAIL 처리.
- [2026-04-19] **fit-pal**: DG-02: SKILL.md References 섹션에 docs/design/figma-decoration-session-log.md 의 §9/§10 링크 누락 (현재 §2.1, §3.1, §8만 있음)
- [2026-04-17] **fit-pal-flutter**: 미검증 항목 3개 (LG-02, DG-03, DG-04) — 미검증 2개 이상 REJECT 규칙 적용
- [2026-04-17] **fit-pal-flutter**: LG-02: 시각적 Figma 대조 불가 (mcp_server: null)
- [2026-04-17] **claude-plugins**: SK-06: reflect-digest/SKILL.md에 Gotchas 섹션과 Process 섹션 미존재
- [2026-04-17] **claude-plugins**: SK-04: docs/harness/plugin-validation.html card-source 2개 — 최소 3개 조건 미달
- [2026-04-17] **claude-plugins**: SK-01: normalize_project_query가 <basename>-<hash6> 입력 시 단일 패턴만 반환 — project=<basename>과 project=<basename>-<hash6> 호출 시 스캔 집합 불일치. _lib-project-id.sh:100-101
- [2026-04-17] **claude-plugins**: SK-01: 8개 HTML 파일 전부 미생성 — 구현 자체가 미수행
- [2026-04-17] **claude-plugins**: SC-05: git tag reflect-kit/v0.2.0 로컬 미생성 (git tag -l 결과 없음)

### 최근 Improvement Suggestions (Top 15)

- [2026-04-23] **flutter_playwright**: evaluate → evaluate_expression 1줄 수정으로 AR-05/ER-03/AR-01/AR-02 연쇄 해결
- [2026-04-22] **fit-pal-server**: 계약 패치 후 코드 동기화 여부를 제출 전 체크리스트에 추가
- [2026-04-22] **fit-pal-server**: DG-04 런타임 검증 — MCP 서버 설정 시 smoke test로 실제 worker 구동 확인 권장
- [2026-04-22] **fit-pal**: DG-04 런타임 검증을 위한 CI smoke test 추가 권장
- [2026-04-22] **fit-pal**: DA-01 조건이 seed_group_with_due_pending_slot(empty sequence)과 seed_group_with_real_routine_and_attend_votes(UPDATE로 덮어쓰기) 2단계로 나뉘어 있어 향후 계약에서 UPDATE 패턴도 명시하면 검증이 더 명확해진다.
- [2026-04-21] **fitpal-server**: DG-04 scope_out 범위의 fitpal-message flaky 테스트를 별도 이슈로 추적하는 것을 권장
- [2026-04-21] **fit-pal-server**: LG-04: ScheduleNotification enum 에 group_id 필드 추가하거나 계약 LG-04 payload 요건에서 group_id 제거
- [2026-04-21] **fit-pal-server**: LG-02: GroupPort 에 내부 전용 list_all_member_ids(group_id) 메서드 추가 권장 (권한 체크 없음)
- [2026-04-21] **fit-pal-server**: LG-02 관련: list_all_member_ids는 worker도 동일하게 쓸 예정이므로 worker Composition Root 재사용 문서화 권장
- [2026-04-21] **fit-pal-server**: DG-04 런타임 검증: MCP 서버 설정 시 schedule 경로 실제 401 응답 확인 자동화 추가 권장
- [2026-04-21] **fit-pal**: 카탈로그 앱 구동 후 DG-03 수동 확인 권장
- [2026-04-21] **fit-pal**: RE-02 계약 Send+Sync vs clippy implied_bounds 충돌 — 계약을 Send만으로 수정하거나 #[allow] 주석 허용을 명시 권장
- [2026-04-21] **fit-pal**: MCP Figma 서버 설정 시 UI-04/LG-04/DG-04 재검증 가능
- [2026-04-21] **fit-pal**: AP-02 계약 허용 예외에 fmt::Write on String의 .expect()를 infallible 케이스로 명시 추가 권장
- [2026-04-20] **fit-pal**: 계약 feature 이름에 Task 1~3이 포함되어 있으나 사용자가 Task 1만 구현했음 — 구현 범위와 계약 범위 사전 명확화 권장

## 2. 외부 프로젝트 (`Hub/10_Dev`) 피드백

- Hub 루트: `/Users/jackson/Hub/10_Dev`
- 발견된 프로젝트: **4**

### `apps`

- 경로: `/Users/jackson/Hub/10_Dev/apps`
- sprint-feedback.md: 163 lines
- history sprint-contracts: 25
- 최근 contracts:
  - 20260411-2324-sprint-contract.md
  - 20260412-0010-sprint-contract.md
  - 20260412-1259-sprint-contract.md
  - 20260412-1430-sprint-contract.md
  - 20260412-1620-sprint-contract.md

<details><summary>sprint-feedback.md 앞부분</summary>

```markdown
# Sprint Feedback
Feature: 위젯 리팩토링 — 터치 효과 추출, 셀렉트 통합, 캐러셀 분리
Evaluated: 2026-04-12 20:00
Verdict: REJECT
Iteration: 3

---

## Results

### UI (3/3)

- [x] UI-01: 터치 효과 적용 위젯이 리팩토링 전과 동일한 탭 피드백을 표시한다 — PASS [L3]
  - 근거: `pressable_widget.dart:39-57` — GestureDetector(onTapDown/Up/Cancel) + AnimatedScale(easeOut, buttonPressedScale). 버튼/날짜필드 모두 PressableWidget 래핑 확인.

- [x] UI-02: 언어/서버 선택 메시지 박스의 옵션 리스트가 리팩토링 전과 동일하게 표시된다 — PASS [L3]
  - 근거: `select_option_list_widget.dart:40-57` — Column + for loop, 선택 행 `AdmColors.progressTrack` 배경, `AdmSizes.h48` 높이. 두 메시지박스 모두 `AdmSelectOptionListWidget` 사용 확인.

- [x] UI-03: 캐러셀 위젯의 PageView와 인디케이터가 리팩토링 전과 동일하게 표시된다 — PASS [L3]
  - 근거: `carousel_widget.dart:55-90` — Column(PageView.builder + _CarouselIndicator). 도트 색상/크기/간격 Props 동일.
```

</details>

### `fit-pal`

- 경로: `/Users/jackson/Hub/10_Dev/fit-pal`
- sprint-feedback.md: 0 lines
- history sprint-contracts: 8
- 최근 contracts:
  - 20260420-2003-sprint-contract.md
  - 20260421-1113-sprint-contract.md
  - 20260421-1137-sprint-contract.md
  - 20260421-1254-sprint-contract.md
  - 20260421-1320-sprint-contract.md
### `flutter_playwright`

- 경로: `/Users/jackson/Hub/10_Dev/flutter_playwright`
- sprint-feedback.md: 152 lines
- history sprint-contracts: 9
- 최근 contracts:
  - 20260416-1815-sprint-contract.md
  - 20260417-1028-sprint-contract.md
  - 20260422-0945-sprint-contract.md
  - 20260422-phase-a-sprint-contract.md
  - 20260422-phase-b-sprint-contract.md

<details><summary>sprint-feedback.md 앞부분</summary>

```markdown
# Sprint Feedback (Phase B — kept above)

---

# Sprint Feedback
Feature: MCP Tool Consolidation + Playwright Parity + Rename (clean break)
Evaluated: 2026-04-23 (Phase C)
Verdict: REJECT
Iteration: 1

## Results

### Architecture (4/8)

- [ ] AR-01: 최종 MCP 도구 수가 45~47개 — FAIL
  - 근거: server 도구: reload_app, restart_app, get_vm_info, dump_tree, get_app_errors, take_screenshot, get_view_details, console_logs, tracing, get_performance_metrics, get_frame_metrics, snapshot_widgets, screenshot_widget, dump_widget_style, find_widget, evaluate_expression, resize_view = 17개. toolkit 도구: tap_widget, long_press_widget, hover_widget, drag_widget, swipe_area, scroll_area, type_text, select_option, set_checkbox, press_key, handle_dialog, fill_form, navigate, wait_for, resize_view, read_prefs, prefs_set, prefs_delete, prefs_clear, save_app_state, restore_app_state, read_state, mutate_state, poll_state, verify_visible, assert_widget, intercept_network, clear_network_intercepts, recording, set_overlay, get_network_log, evaluate = 32개. 합계 49개. 허용 범위 45~47 초과.
  - 원인: toolkit에 `evaluate`(AR-05로 삭제 필요)와 `get_network_log`(AR-02c에서 server 배치 필요) 여분 2개 + `resize_view` server/toolkit 중복. AR-05 evaluate 미rename → toolkit에서 구 이름 도구 잔존.
  - 수정: toolkit `expression_entries.dart` 의 `name: 'evaluate'` → `'evaluate_expression'` 로 rename. `get_network_log` server 측으로 이전 또는 계약 수정.

- [ ] AR-02: `verb_object` snake_case 네이밍 — FAIL (부분)
```

</details>

### `iyaki-zip-dev`

- 경로: `/Users/jackson/Hub/10_Dev/iyaki-zip-dev`
- sprint-feedback.md: 135 lines
- history sprint-contracts: 4
- 최근 contracts:
  - 20260414-1551-sprint-contract.md
  - 20260414-2300-sprint-contract.md
  - 20260415-1400-sprint-contract.md
  - 20260420-2020-sprint-contract.md

<details><summary>sprint-feedback.md 앞부분</summary>

```markdown
# Sprint Feedback
Feature: sprint4-figma-gap
Evaluated: 2026-04-15 17:20
Verdict: REJECT
Iteration: 1

## Results

### UI (4/6)

- [x] UI-01: Smart guide line renders in OverlayLayer during drag near other card edge/center — PASS (structural)
  - 근거: `DragController.ts:124-130` — computeGuides called, guide lines pushed as `guideLine` OverlayCommand; `OverlayLayer.ts:110-115` renders them. `CanvasView.tsx:64` passes `initialSmartGuideConfig`.
  - [정적] 런타임 검증 미수행 — MCP 서버 미설정

- [ ] UI-02: **DESCOPED** (removed from contract per user decision; UI-02 not present in the 26-condition contract above)
  - 계약에 없음 — 평가 대상 외

- [ ] UI-03: Right-click on card shows Edit/Duplicate/Delete/Bring to front/Send to back; Esc/outside click closes — PASS (structural)
  - 근거: `CanvasContextMenu.tsx:82-99` — all 5 menu items rendered when `hitId != null`; shadcn ContextMenu (Radix primitive) handles Esc + outside click natively; callbacks wired in `CanvasView.tsx:210-222`.
  - [정적] 런타임 검증 미수행
```

</details>


## 3. Followup 문서

- `docs/superpowers/followup-2026-04-11-plugin-validation-findings.md`

## 4. 현재 레포 최근 Sprint Contracts

- `.harness/history/20260411-kaizen-phase6-design-kit-sprint-contract.md`
- `.harness/history/20260411-phase5-flutter-toolkit-sprint-contract.md`
- `.harness/history/20260412-0045-post-missing-items-sprint-contract.md`
- `.harness/history/20260412-0115-automation-gap-10-sprint-contract.md`
- `.harness/history/20260412-1255-sprint-contract.md`
- `.harness/history/20260412-1302-sprint-contract.md`
- `.harness/history/20260412-2146-sprint-contract.md`
- `.harness/history/20260417-1037-sprint-contract.md`
- `.harness/history/20260417-1042-sprint-contract.md`
- `.harness/history/20260417-1717-sprint-contract.md`

## 5. Validate-Plugin 최근 실행 스냅샷

```text
... (이전 출력 생략)
  V3 refs            0 links — OK
  V4 triggers        26 keywords — OK
  V5 placeholders    0 found — OK
  V6 code-fence      0 bare — OK
  V7 plugin-json     v0.3.6 matches marketplace — OK

=== flutter-toolkit ===
  V1 frontmatter     18 skills + 1 agent — OK
  V2 templates       0 files — SKIP (no templates/)
  V3 refs            0 links — OK
  V4 triggers        141 keywords — OK
  V5 placeholders    0 found — OK
  V6 code-fence      0 bare — OK
  V7 plugin-json     v0.5.1 matches marketplace — OK

=== design-kit ===
  V1 frontmatter     8 skills + 1 agent — OK
  V2 templates       8 skipped (ts/js) — OK
  V3 refs            0 links — OK
  V4 triggers        46 keywords — OK
  V5 placeholders    0 found — OK
  V6 code-fence      0 bare — OK
  V7 plugin-json     v0.2.1 matches marketplace — OK

=== backend-kit ===
  V1 frontmatter     4 skills + 1 agent — OK
  V2 templates       0 files — SKIP (no templates/)
  V3 refs            0 links — OK
  V4 triggers        18 keywords — OK
  V5 placeholders    0 found — OK
  V6 code-fence      0 bare — OK
  V7 plugin-json     v0.1.1 matches marketplace — OK

=== infra-kit ===
  V1 frontmatter     4 skills + 1 agent — OK
  V2 templates       0 files — SKIP (no templates/)
  V3 refs            0 links — OK
  V4 triggers        19 keywords — OK
  V5 placeholders    0 found — OK
  V6 code-fence      0 bare — OK
  V7 plugin-json     v0.1.1 matches marketplace — OK

=== rust-kit ===
  V1 frontmatter     16 skills + 1 agent — OK
  V2 templates       1 parsed, 4 skipped (ts/js) — OK
  V3 refs            0 links — OK
  V4 triggers        79 keywords — OK
  V5 placeholders    0 found — OK
  V6 code-fence      0 bare — OK
  V7 plugin-json     v0.1.1 matches marketplace — OK

=== react-kit ===
  V1 frontmatter     21 skills + 3 agents — OK
  V2 templates       5 parsed, 4 skipped (ts/js) — OK
  V3 refs            0 links — OK
  V4 triggers        156 keywords — OK
  V5 placeholders    0 found — OK
  V6 code-fence      0 bare — OK
  V7 plugin-json     v0.1.1 matches marketplace — OK

=== planning-kit ===
  V1 frontmatter     12 skills + 1 agent — OK
  V2 templates       0 files — SKIP (no templates/)
  V3 refs            0 links — OK
  V4 triggers        95 keywords — OK
  V5 placeholders    0 found — OK
  V6 code-fence      0 bare — OK
  V7 plugin-json     v0.2.0 matches marketplace — OK

=== reflect-kit ===
  V1 frontmatter     3 skills — OK
  V2 templates       0 files — SKIP (no templates/)
  V3 refs            0 links — OK
  V4 triggers        20 keywords — OK
  V5 placeholders    0 found — OK
  V6 code-fence      0 bare — OK
  V7 plugin-json     v0.3.0 matches marketplace — OK

Total: 9 plugins, 9 OK
Exit: 0
```


## 6. Phase 별 참조 가이드

각 Phase subagent 는 아래 매핑을 참고하여 자신의 범위에 맞는 섹션을 우선 읽는다.

| Phase | 스킬 | 주요 참조 섹션 |
|-------|------|---------------|
| 1 설계 가이드 | skill-design-guide, agent-design-guide | §1 Improvement Suggestions |
| 2 Contract | contract-design-guide + sprint-contract | §1 Reject 사유 (계약 모호성) |
| 3 Evaluator | qa-evaluation-guide + qa-evaluator | §1 Improvement (L3, set intersection) |
| 4 Harness | harness/skills/* (sprint-contract, qa-evaluator 제외) | §5 validate-plugin 현재 상태 |
| 5 Flutter | flutter-toolkit/skills/* | §2 Hub 외부 프로젝트 (fit-pal, apps) |
| 6 Design | design-kit/skills/* | §5 validate-plugin 현재 상태 |
| 7 Backend | backend-kit/skills/* | §1 Backend 관련 feedback (있다면) |
| 8 Infra | infra-kit/skills/* | §5 validate-plugin 현재 상태 |
| 9 Rust | rust-kit/skills/* | §2 Hub 외부 프로젝트 (fit-pal server) |
| 10 React | react-kit/skills/* | §3 followup-2026-04-11, §5 |

