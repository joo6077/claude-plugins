# Kaizen Data Pool

Generated: 2026-05-07T22:02:11
Generator: `scripts/collect-kaizen-data.py`

카이젠 오케스트레이션의 Phase 별 서브에이전트가 참조할 통합 데이터 풀이다. 이 파일은 `scripts/collect-kaizen-data.py` 로 재생성된다 — 수동 수정 금지.

## 0. `/insights` Report (외부 도구 산출물)

- 경로: `.claude/kaizen-input/insights-report.md`
- 최근 갱신: 2026-04-24T14:12:37 (13일 전)
- 모든 Phase 서브에이전트가 **최우선** 참조해야 한다 (Friction Points / Recommended Patterns / Feature Suggestions)

<details><summary>insights-report.md 본문</summary>

# /insights Report Extract

30일 세션 로그 분석 결과. 원본: `~/.claude/usage-data/report.html`

## Key Insight
- Key pattern: You run Claude as an autonomous sprint executor under formal contracts, intervening sharply and explicitly when it fails to proactively apply the rules you've established.

## Friction Points (마찰점)
### 1. Proactive quality gaps in refactoring During your anti-AI-tone refactoring sweeps, Claude consistently fails to spot obv
Proactive quality gaps in refactoring During your anti-AI-tone refactoring sweeps, Claude consistently fails to spot obvious improvements (text style migrations, redundant variables, hardcoded values) that your rules already cover, making you re-prompt with mounting frustration. Consider having Claude produce an explicit rule-by-rule checklist pass before claiming a file is done, so violations surface without your intervention. Claude forgot to migrate legacy bodyMSemiBold despite rule R1 mandating it, triggering an angry correction On S6 list widgets you had to point out TextStyle migration, unneeded null branches, and manual SizedBox gaps repeatedly, eventually codifying them as new rules

### 2. Wrong approach and false dichotomies in architecture work Claude often commits to an approach (widget choice, contract w
Wrong approach and false dichotomies in architecture work Claude often commits to an approach (widget choice, contract wording, solution framing) without verifying against Figma tokens, existing code, or your actual intent, leading to rework cycles. Requiring Claude to verify exact style/token names and enumerate options before acting would cut the iteration count. Repeatedly used Stack where Column sufficed and mismatched Figma text style tokens, causing visual drift and frustration Parity/Consolidation contract needed 3 iterations due to arithmetic errors, naming issues, and unclear server/toolkit boundaries

### 3. Session truncation and tool/infrastructure failures A meaningful share of your sessions end mid-task due to output token
Session truncation and tool/infrastructure failures A meaningful share of your sessions end mid-task due to output token limits, sandbox network blocks, or hung background agents, producing unclear outcomes and lost work. Splitting large multi-phase runs into smaller committed checkpoints and avoiding long inline responses would reduce these dead-ends. Multiple sessions showed only API errors from exceeded output token limits, leaving goals indeterminable Two of three Codex background research tasks (R2, R3) hung indefinitely, and a final git push was blocked by sandbox HTTPS leaving 2 commits unpushed

## Recommended Patterns
### 1. Batch-identify refactor opportunities up front Before editing any file in a refactoring sweep, have Claude enumerate eve
Batch-identify refactor opportunities up front Before editing any file in a refactoring sweep, have Claude enumerate every applicable rule violation first, then you approve the list. Your anti-AI-tone sessions show a repeated pattern: Claude fixes some issues, you point out missed ones (legacy text styles, hardcoded values, unneeded nulls), Claude fixes those, you find more. Front-loading a full audit turns N frustrating round-trips into 1 review + 1 execution. This also prevents Claude from 'over-interpreting rules' or making unauthorized changes because the scope is locked before edits begin. Paste into Claude Code: Before editing anything, read the target files and produce a checklist of EVERY anti-AI-tone rule violation you find: TextStyle token migrations (including legacy bodyMSemiBold), Stack-vs-Column choices, unnecessary local variables, unneeded null branches, hardcoded values, manual SizedBox gaps, Figma text-style name mismatches. Show me the full checklist and wait for my approval before making any changes. Copy

### 2. Check for parallel work before starting a task Make 'git fetch + log inspection' the mandatory first step of any sprint 
Check for parallel work before starting a task Make 'git fetch + log inspection' the mandatory first step of any sprint task. Multiple sessions wasted effort because parallel automation had already completed or was concurrently modifying the same tasks (Tasks 20/21 session explicitly required a reconciliation commit). You're running enough concurrent work that this collision is structural, not incidental. A 30-second check upfront prevents hours of desync. Paste into Claude Code: Before starting Task X, run: git fetch --all && git log origin/dev --oneline -20 && git log --all --oneline --since='2 days ago' | head -30. Check whether this task or adjacent files have been touched by parallel automation. Report findings before proceeding. Copy

### 3. Guard against output-token truncation on long sessions For multi-phase sprints, explicitly request chunked output and in
Guard against output-token truncation on long sessions For multi-phase sprints, explicitly request chunked output and intermediate commits. At least 5 of your sessions were truncated or rendered unreadable by output_token_limit errors. Your average session is long (568 hours / 93 sessions ≈ 6 hours) and involves heavy Bash/Edit/Read loops. Instructing Claude to commit progress every checkpoint and keep per-turn responses short preserves state when limits hit and makes resumption trivial. Paste into Claude Code: This will be a long session. Rules: (1) commit and push after every checkpoint, not at the end; (2) keep each response under 300 lines — if more is needed, split across turns; (3) after each checkpoint, write a 3-line status to a SESSION_LOG.md so we can resume if the session is truncated. Copy

## Feature Suggestions (Skills/Hooks/MCP)
### 1. Custom Skills Reusable markdown prompts invoked via /command for repetitive workflows. Why for you: You run the same Con
Custom Skills Reusable markdown prompts invoked via /command for repetitive workflows. Why for you: You run the same Contract → Implement → QA → Commit → Push → Handoff cycle every sprint (131 commits across 48 sessions), and anti-AI-tone refactoring follows a fixed rule checklist. Encoding these as /contract, /qa, /handoff, /refactor-antitone skills would eliminate the repeated rule-reminding and missed-step friction. mkdir -p .claude/skills/handoff && cat > .claude/skills/handoff/SKILL.md <<'EOF' --- name: handoff description: Produce session handoff with completion summary, next-session resume prompt, and push status --- 1. Summarize what was completed this session (commits, tasks, QA status) 2. List outstanding work and blockers 3. Write a copy-pasteable next-session prompt the user can send verbatim 4. Report git push status for all branches touched EOF Copy

### 2. Hooks Shell commands that auto-run on Claude lifecycle events. Why for you: You already deployed a PreToolUse hook to en
Hooks Shell commands that auto-run on Claude lifecycle events. Why for you: You already deployed a PreToolUse hook to enforce skill usage in one session — extend this pattern. A PostToolUse hook running `dart format` / `cargo fmt` / `cargo clippy` after Edit events would catch the clippy/fmt issues that show up during QA, and a PreToolUse hook checking `git fetch && git status` would prevent the parallel-automation desync you hit multiple times. // .claude/settings.json { "hooks": { "PostToolUse": [ {"matcher": "Edit|Write", "command": "[ -f Cargo.toml ] && cargo fmt --all -- --check 2>&1 | head -20 || true"} ], "PreToolUse": [ {"matcher": "Bash", "command": "echo '[hook] current branch:' $(git branch --show-current)"} ] } } Copy

### 3. MCP Servers Connect Claude to external tools like Figma, GitHub, and databases. Why for you: You repeatedly hit friction
MCP Servers Connect Claude to external tools like Figma, GitHub, and databases. Why for you: You repeatedly hit friction on Figma text-style name verification and Flutter/HTML visual parity (one session burned 5+ hours on button matching). A Figma MCP server would let Claude fetch exact token names and pixel values directly instead of guessing, eliminating a major class of rework. Your flutter-playwright MCP also needs stabilization given the 45+ stale process incident. claude mcp add figma -- npx -y figma-developer-mcp --figma-api-key=$FIGMA_API_KEY # Then ask: 'fetch the exact text style tokens for frame X from Figma before refactoring' Copy

</details>

## 1. 글로벌 Evaluator Feedback

- 경로: `/Users/jackson/.harness/feedback/evaluator`
- 총 파일: **150**

### Verdict 분포

- **APPROVE**: 85
- **REJECT**: 64
- **UNKNOWN**: 1

### Skill 분포

- `qa-evaluator`: 150

### Project 분포

- `claude-plugins`: 109
- `fit-pal`: 27
- `fit-pal-server`: 4
- `fit-pal-app`: 3
- `flutter_playwright`: 3
- `fit-pal-flutter`: 1
- `fitpal-server`: 1
- `iyaki-zip-dev`: 1
- `claude-plugins / react-kit phase10-research kaizen`: 1

### 최근 REJECT 사유 (Top 20)

- [2026-04-28] **fit-pal**: 미검증 4건 (LG-03, ER-01, DG-02, DG-04) — 자동 REJECT 임계 2건 초과
- [2026-04-27] **fit-pal-app**: LG-02: rg ref.read(castVoteUseCaseProvider) 0매치 (기준 1매치). dart format 줄바꿈으로 단일행 패턴 매칭 실패. 계약 측정 결함.
- [2026-04-27] **fit-pal**: AR-01: working tree에 Aqua 3D Button 스프린트 미커밋 파일 4건(action_samples.dart, if_button.dart, aqua_button_decorations.dart, aqua_press_box.dart)이 계약 exclusion list에 없어 범위 초과 판정
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

### 최근 Improvement Suggestions (Top 15)

- [2026-05-06] **fit-pal**: 미검증 2건 구조적 한계 해소를 위한 flutter-playwright MCP 설정 추진
- [2026-05-06] **fit-pal**: DG-03/DG-04 런타임 검증을 위해 project.yaml mcp_server 활성화 권장
- [2026-05-05] **fit-pal-app**: DG-04 런타임 검증을 위해 MCP 서버 설정 권장
- [2026-04-28] **fit-pal**: 런타임 의존 조건(LG-03/ER-01/DG-04)을 시뮬레이터 진입 후 재검증
- [2026-04-28] **fit-pal**: DG-02는 DG-01 flutter analyze 결과로 사실상 커버됨 — 계약에서 IDE diagnostics와 analyze를 동치로 명시 고려
- [2026-04-27] **fit-pal-app**: LG-02 측정식에 dart format 줄바꿈 허용 carve-out 추가 (LG-05와 동일 처리)
- [2026-04-27] **fit-pal**: DG-04 런타임 검증을 위해 MCP 서버 설정 권장
- [2026-04-27] **fit-pal**: DG-04 pre-existing 잔류(group_create_page.dart line-length 등) 별도 백로그 티켓으로 분리 처리 권장
- [2026-04-27] **fit-pal**: DG-04 exit 0 요구를 '변경/생성 파일 범위 내 이슈 0건'으로 명확화
- [2026-04-27] **fit-pal**: DG-01/DG-04 exit 0 요구를 변경 파일 범위 내 이슈 0건으로 명확화 권장
- [2026-04-27] **fit-pal**: AR-05 계약 측정 기준: 향후 git diff <base>..HEAD 커밋 기준으로 명시하면 working tree 잔류 파일 혼입 방지 가능
- [2026-04-27] **fit-pal**: AR-01 exclusion list에 타 스프린트 working tree dirt 포괄 제외 절 추가 권장
- [2026-04-27] **fit-pal**: AR-01 exclusion list에 다른 스프린트의 미커밋 working tree 변경을 포괄하는 절 추가 또는 Aqua 파일 4건 명시 추가
- [2026-04-24] **flutter_playwright**: project.yaml 설정 시 MCP 런타임 검증 활성화로 LG-D4 정적 판정을 런타임 검증으로 승격 가능
- [2026-04-23] **flutter_playwright**: evaluate → evaluate_expression 1줄 수정으로 AR-05/ER-03/AR-01/AR-02 연쇄 해결

## 2. 외부 프로젝트 (`Hub/10_Dev`) 피드백

- Hub 루트: `/Users/jackson/Hub/10_Dev`
- 발견된 프로젝트: **4**

### `apps`

- 경로: `/Users/jackson/Hub/10_Dev/apps`
- sprint-feedback.md: 90 lines
- history sprint-contracts: 36
- 최근 contracts:
  - 20260430-1435-sprint-contract.md
  - 20260430-1514-sprint-contract.md
  - 20260430-1531-sprint-contract.md
  - 20260430-1905-sprint-contract.md
  - 20260504-1920-sprint-contract.md

<details><summary>sprint-feedback.md 앞부분</summary>

```markdown
# Sprint Feedback
Feature: 공연 다운로드 플로우
Evaluated: 2026-05-07 14:00
Verdict: REJECT
Iteration: 1

## Results

### UI (5/5)
- [x] UI-01: import 화면에서 다운로드 버튼 클릭 시 진행 다이얼로그가 표시되고 progress(0~1)가 실시간 업데이트된다 — PASS [L2]
  - 근거: `apps/app_kiosk/lib/features/admin/event/adm_event_import_screen.dart:547-577` — `progressNotifier` + `unawaited(showDialog)` + `onProgress` 콜백 연결
- [x] UI-02: 다운로드 완료 시 다이얼로그가 isCompleted 상태로 전환되고 1.5초 후 자동 닫힌다 — PASS [L2]
  - 근거: `apps/app_kiosk/lib/features/admin/event/adm_event_import_screen.dart:583-586` — `completedNotifier.value = true` → `Future.delayed(1500ms)` → `context.pop()`
- [x] UI-03: 이미 다운로드된 공연은 검색 결과에서 "다운로드 완료" 텍스트 + dimmed 처리로 표시된다 — PASS [L2]
  - 근거: `apps/app_kiosk/lib/features/admin/event/adm_event_import_screen.dart:353-381` — `alreadyDownloaded` 플래그 → `dimmed: true` + `download_done` 텍스트
- [x] UI-04: 공연 데이터 관리 목록에서 저장된 포스터 이미지가 썸네일로 표시된다 (경로가 없으면 placeholder) — PASS [L2]
  - 근거: `apps/app_kiosk/lib/features/admin/event/adm_event_list_screen.dart:210-217` — `posterPath` null 체크 → `FileImage` 또는 null 전달 → `AdmImageViewWidget`이 null일 때 placeholder 처리
- [x] UI-05: 공연 상세 화면에서 좌석 다운로드 버튼 클릭 시 진행 다이얼로그가 표시되고 완료 후 자동 닫힌다 — PASS [L3]
  - 근거: `apps/app_kiosk/lib/features/admin/event/adm_event_details_screen.dart:228-274` — `unawaited(showDialog)` + `AdmDualProgressMessageBoxWidget` + `isCompleted: true` → 1500ms delay → `context.pop()`

```

</details>

### `fit-pal`

- 경로: `/Users/jackson/Hub/10_Dev/fit-pal`
- sprint-feedback.md: 104 lines
- history sprint-contracts: 9
- 최근 contracts:
  - 20260421-1113-sprint-contract.md
  - 20260421-1137-sprint-contract.md
  - 20260421-1254-sprint-contract.md
  - 20260421-1320-sprint-contract.md
  - 20260507-1256-sprint-contract.md

<details><summary>sprint-feedback.md 앞부분</summary>

```markdown
# Sprint Feedback
Feature: 검색 결과 사용자 행에 그룹 초대 버튼 + 바텀시트/확인 다이얼로그
Evaluated: 2026-05-07 14:30
Verdict: APPROVE_WITH_BLOCKED
Iteration: 1

## Results

### UI (3/5 — 코드 검증 PASS, 시뮬 3건 BLOCKED)
- [x] UI-01: invite 버튼 노출 조건 + self-filter — PASS (코드), BLOCKED (시뮬)
  - 근거: `home_search_results.dart:149` `if (invitableGroups.isNotEmpty)` 조건 확인. `home_search_provider.dart:144-148` viewer.id == user.id 제외 후처리 확인. 시뮬 3 시나리오는 BLOCKED.
  - [L3, 정적]
- [x] UI-02: IFButton "초대" 배치 + raw Color/EdgeInsets.all 0건 — PASS
  - 근거: `home_search_results.dart:211` `IFButton(onTap: onTap, ...)` + `Text('초대')`. `rg 'Color\(0x|EdgeInsets\.all\(\d'` 변경/생성 파일 전체 0건.
  - [L3, 정적]
- [x] UI-03: 단일→AlertDialog / 다중→showSheet 분기 — PASS (코드), BLOCKED (시뮬)
  - 근거: `home_search_results.dart:170-199` `groups.length == 1` → `InviteConfirmDialog.show`, `>= 2` → `InviteToGroupSheet.show`. `invite_to_group_sheet.dart:28` `showSheet<void>` 래퍼 사용 확인.
  - [L3, 정적]
- [x] UI-04: InviteStatus enum 정확히 3값 + 사유 텍스트/disabled 분기 — PASS (코드), BLOCKED (시뮬)
  - 근거: `invite_status.dart:6-13` `invitable|alreadyMember|alreadyInvited` 3값만. `invite_to_group_sheet.dart:93-105` 사유 텍스트 + `onTap: g.status == InviteStatus.invitable ? ... : null` disabled 처리.
```

</details>

### `flutter_playwright`

- 경로: `/Users/jackson/Hub/10_Dev/flutter_playwright`
- sprint-feedback.md: 117 lines
- history sprint-contracts: 10
- 최근 contracts:
  - 20260417-1028-sprint-contract.md
  - 20260422-0945-sprint-contract.md
  - 20260422-phase-a-sprint-contract.md
  - 20260422-phase-b-sprint-contract.md
  - 20260507-1823-sprint-contract.md

<details><summary>sprint-feedback.md 앞부분</summary>

```markdown
# Sprint Feedback
Feature: DTD-based VM service auto-discovery (Flutter CLI hosted DTD)
Evaluated: 2026-05-07 20:05
Verdict: APPROVE
Iteration: 2

---

## Pre-Check: Binary Decidability (Iteration 2)

**ER-DTD-4** — FAIL 상태: "파일 상태 4케이스 테스트 4건 중 1건이라도 미존재 또는 FAIL". [exact, enumerated] — 4건 전부 개별 Grep 필수.

**LG-DTD-2/3/4** — 계약 frontmatter `fallback_policy` (sprint-contract.md:7)가 "3건 모두 허용"으로 명시적 revision. 새 계약 기준으로 [미검증, fallback PASS] 허용.

---

## Results

### Architecture (3/3)

```

</details>

### `iyaki-zip-dev`

- 경로: `/Users/jackson/Hub/10_Dev/iyaki-zip-dev`
- sprint-feedback.md: 131 lines
- history sprint-contracts: 6
- 최근 contracts:
  - 20260414-2300-sprint-contract.md
  - 20260415-1400-sprint-contract.md
  - 20260420-2020-sprint-contract.md
  - 20260424-1530-sprint-contract.md
  - 20260507-2056-sprint-contract.md

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


## 3. Followup 문서

- `docs/superpowers/followup-2026-04-11-plugin-validation-findings.md`

## 4. 현재 레포 최근 Sprint Contracts

- `.harness/history/20260412-2146-sprint-contract.md`
- `.harness/history/20260417-1037-sprint-contract.md`
- `.harness/history/20260417-1042-sprint-contract.md`
- `.harness/history/20260417-1717-sprint-contract.md`
- `.harness/history/20260424-kaizen-phase10-react-kit-sprint-contract.md`
- `.harness/history/20260424-kaizen-phase4-harness-sprint-contract.md`
- `.harness/history/20260424-kaizen-phase7-backend-kit-sprint-contract.md`
- `.harness/history/20260424-phase1-design-guides-sprint-contract.md`
- `.harness/history/20260424-phase6-design-kit-sprint-contract.md`
- `.harness/history/20260424-phase8-sprint-contract.md`

## 5. Validate-Plugin 최근 실행 스냅샷

```text
... (이전 출력 생략)
  V3 refs            0 links — OK
  V4 triggers        26 keywords — OK
  V5 placeholders    0 found — OK
  V6 code-fence      0 bare — OK
  V7 plugin-json     v0.4.0 matches marketplace — OK

=== flutter-toolkit ===
  V1 frontmatter     18 skills + 1 agent — OK
  V2 templates       0 files — SKIP (no templates/)
  V3 refs            0 links — OK
  V4 triggers        141 keywords — OK
  V5 placeholders    0 found — OK
  V6 code-fence      0 bare — OK
  V7 plugin-json     v0.5.2 matches marketplace — OK

=== design-kit ===
  V1 frontmatter     8 skills + 1 agent — OK
  V2 templates       8 skipped (ts/js) — OK
  V3 refs            0 links — OK
  V4 triggers        46 keywords — OK
  V5 placeholders    0 found — OK
  V6 code-fence      0 bare — OK
  V7 plugin-json     v0.2.2 matches marketplace — OK

=== backend-kit ===
  V1 frontmatter     4 skills + 1 agent — OK
  V2 templates       0 files — SKIP (no templates/)
  V3 refs            0 links — OK
  V4 triggers        18 keywords — OK
  V5 placeholders    0 found — OK
  V6 code-fence      0 bare — OK
  V7 plugin-json     v0.1.2 matches marketplace — OK

=== infra-kit ===
  V1 frontmatter     4 skills + 1 agent — OK
  V2 templates       0 files — SKIP (no templates/)
  V3 refs            0 links — OK
  V4 triggers        19 keywords — OK
  V5 placeholders    0 found — OK
  V6 code-fence      0 bare — OK
  V7 plugin-json     v0.1.2 matches marketplace — OK

=== rust-kit ===
  V1 frontmatter     16 skills + 1 agent — OK
  V2 templates       1 parsed, 4 skipped (ts/js) — OK
  V3 refs            0 links — OK
  V4 triggers        79 keywords — OK
  V5 placeholders    0 found — OK
  V6 code-fence      0 bare — OK
  V7 plugin-json     v0.1.2 matches marketplace — OK

=== react-kit ===
  V1 frontmatter     21 skills + 3 agents — OK
  V2 templates       5 parsed, 4 skipped (ts/js) — OK
  V3 refs            0 links — OK
  V4 triggers        157 keywords — OK
  V5 placeholders    0 found — OK
  V6 code-fence      0 bare — OK
  V7 plugin-json     v0.1.2 matches marketplace — OK

=== planning-kit ===
  V1 frontmatter     12 skills + 1 agent — OK
  V2 templates       0 files — SKIP (no templates/)
  V3 refs            0 links — OK
  V4 triggers        95 keywords — OK
  V5 placeholders    0 found — OK
  V6 code-fence      0 bare — OK
  V7 plugin-json     v0.3.0 matches marketplace — OK

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

각 Phase subagent 는 아래 매핑을 참고하여 자신의 범위에 맞는 섹션을 우선 읽는다. §0 (/insights) 가 존재할 때는 **모든 Phase** 가 §0 을 최우선 참조한다.

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

