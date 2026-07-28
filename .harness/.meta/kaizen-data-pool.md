# Kaizen Data Pool

Generated: 2026-07-27T18:32:53
Generator: `scripts/collect-kaizen-data.py`

카이젠 오케스트레이션의 Phase 별 서브에이전트가 참조할 통합 데이터 풀이다. 이 파일은 `scripts/collect-kaizen-data.py` 로 재생성된다 — 수동 수정 금지.

## 0. `/insights` Report (외부 도구 산출물)

- 경로: `/Users/jackson/.claude/usage-data/report.html` · HTML 추출 텍스트
- 최근 갱신: 2026-07-27T18:29:04 ✓ VERY FRESH (0.1시간 전)
- 모든 Phase 서브에이전트가 **최우선** 참조해야 한다 (Friction Points / Recommended Patterns / Feature Suggestions / 이번 사이클 신규 워크플로우 제안)

<details><summary>insights report 본문 (auto-extracted)</summary>

Claude Code Insights 
 

 
 
 
 

 
Claude Code Insights

 
1,092 messages across 51 sessions (56 total) | 2026-06-04 to 2026-07-27

 
 

 
At a Glance

 

 
 What's working: You run Claude like a senior engineer runs a team: sprint contracts, QA gates before commit, handoff docs across sessions, and a hard insistence on root cause before edits. That discipline shows up in your best outcomes — the FCM 409 partial-unique-index collision, the InheritedElement/GlobalKey reparent crash, and tracing iOS simulator sluggishness to a leaked render host rather than patching symptoms. You also hand off entire release pipelines end to end and expect the whole chain to land, which is a level of delegation most users never reach. Impressive Things You Did → 

 
 What's hindering you: On Claude's side: it too often starts editing before pinning down what you actually meant — especially on visual and animation work, where it built the wrong thing two or three times (the play-icon spinner, the lens-boundary zoom, the check stroke-draw). It also claimed things looked correct when it couldn't actually see them, which cost you real trust. On your side: long "continue autonomously" sprints tend to drift past scope into over-escalation and half-finished handoffs, and resuming from a stale handoff doc has burned session starts. Batched commits have also let regressions hide until you spotted them yourself. Where Things Go Wrong → 

 
 Quick wins to try: Add a Hook that blocks or flags "done" claims without a captured artifact — screenshot, test output, or query result — so visual work can't be declared finished blind. Turn your sprint-contract and release-pipeline routines into Custom Skills so the QA gate and version reconciliation steps are invoked identically every time. And when resuming a sprint, spawn a Task Agent to verify the handoff doc against git before any implementation starts. Features to Try → 

 
 Ambitious workflows: Prepare for agents that close the visual loop themselves: baseline screenshot, apply change, re-capture, diff, self-reject and retry — so UI work becomes a single approve/reject instead of correction ping-pong. Also set up for parallel full-stack slices: a contract agent defines the API type first, then server and client agents implement against it in separate worktrees with a contract-test agent proving they agree — which would stop the recurring "server done, client deferred" pattern. Start structuring your specs now so a contract exists as a real artifact, not just a sentence in the prompt. On the Horizon → 

 

 

 

 
 What You Work On 
 How You Use CC 
 Impressive Things 
 Where Things Go Wrong 
 Features to Try 
 New Usage Patterns 
 On the Horizon 
 Team Feedback 
 

 

 

1,092

Messages

 

+56,794/-6,986

Lines

 

832

Files

 

20

Days

 

54.6

Msgs/Day

 

 
 
What You Work On

 

 
 

 

 FitPal Flutter App — UI/UX Refinement & Animation 
 ~16 sessions 
 

 
Extensive work on the FitPal mobile app's visual layer: workout player launch morph and bubble animations, completion shine-sweep and stroke-draw check effects, group-detail and schedule screen redesigns, emoji picker, FAB styling, jewel color swatches, and keyboard/SafeArea layout bugs. Claude used the fitpal-mobile MCP tools (find_widget, runClientTool) plus simulator screenshots to empirically verify bugs and fixes on-device. Visual and animation tasks were the highest-friction area, often requiring several correction rounds when Claude misread the intended effect.

 

 
 

 

 FitPal Backend — Concurrency, API Contracts & Audit Remediation 
 ~11 sessions 
 

 
Rust server work covering a concurrency/correctness audit, FCM token 409 collisions from a partial unique index, 404→200 empty API contract changes, idempotency fixes, S3 object reclamation, phone_hmac wiring, and container image digest pinning. Claude traced root causes through code paths, wrote tests with DB-level proof, and committed/pushed fixes to dev. Several sessions were autonomous audit-backlog sweeps where Claude verified which items were already resolved before implementing.

 

 
 

 

 Feature Development — Scheduling, Groups & Messaging 
 ~12 sessions 
 

 
Multi-sprint feature builds including routine schedule globalization (S3–S8), holiday marking and policy layers, UI pickers, group invitation permissions, owned-group transfer, My Groups settings entry, and chat read receipts plus typing indicators. Claude followed a design-to-QA sprint-contract workflow, threading new fields across entities, models, and codegen while coordinating around parallel sessions touching the same files.

 

 
 

 

 Performance Auditing & Code Refactoring 
 ~8 sessions 
 

 
Jank audits, repaint/rebuild optimization batches, Impeller vs Skia A/B testing, and SCSV cleanup with custom lint rules to prevent regressions. Also large refactors of the preset, event details, and event import screens into shared widgets and code standards. One standout debugging session traced iOS simulator sluggishness to an 18-day leaked render host causing swap saturation.

 

 
 

 

 Release Engineering & CI/CD 
 ~4 sessions 
 

 
End-to-end release pipelines for v0.5.0 and v0.6.0 across both the Rust server and the iOS/Android app, including version reconciliation, whatsnew copy, PR merges, deploys, and post-deploy health checks. Claude patched four RUSTSEC security advisories, monitored CI, and navigated release landmines like an expired Apple agreement.

 

 
 

 

 3D Printing Profiles & Misc Tooling 
 ~4 sessions 
 

 
Generating and iterating Bambu print profiles for shower-box and holster models, analyzing each model's geometry to tune supports, ironing, and bed adhesion. Real-world print results repeatedly surfaced new issues (curved-surface stair-stepping, voronoi stringing, base peeling) that required successive profile revisions. Also included one-off tasks like reverse-engineering Raycast's SQLCipher key derivation to recover clipboard history.

 

 
 

 

 

 

 
What You Wanted

 

 
Feature Implementation

 

 
20

 

 
Bug Fix

 

 
14

 

 
Bug Fixing

 

 
9

 

 
Ui Redesign

 

 
7

 

 
Ui Refinement

 

 
7

 

 
Code Refactoring

 

 
6

 

 

 

 
Top Tools Used

 

 
Bash

 

 
3694

 

 
Edit

 

 
1887

 

 
Read

 

 
1452

 

 
Write

 

 
423

 

 
Mcp Fitpal-Mobile RunClientTool

 

 
352

 

 
TodoWrite

 

 
344

 

 

 

 

 

 
Languages

 

 
Rust

 

 
838

 

 
Markdown

 

 
592

 

 
JSON

 

 
70

 

 
YAML

 

 
57

 

 
HTML

 

 
29

 

 
Shell

 

 
17

 

 

 

 
Session Types

 

 
Multi Task

 

 
23

 

 
Iterative Refinement

 

 
16

 

 
Single Task

 

 
8

 

 
Quick Question

 

 
2

 

 
Undefined

 

 
1

 

 

 

 
 
How You Use Claude Code

 

 
You work in long, high-intensity sessions — 51 sessions spanning a Rust backend and Flutter app, with 187 commits and heavy MCP-driven device testing. Your default mode is delegate broadly, then course-correct hard . You frequently hand Claude an entire sprint or backlog ('resume the queued sprint from the handoff doc', 'autonomously continue backend audit remediation', 'process and verify these bug reports') and let it run for extended stretches. But you're watching closely: when Claude drifts, you interrupt immediately and bluntly — 'ㄱㄱ' to approve, '봐봐 이상하잖아?' when the FAB rendered as a stretched oval, '당연히 그러면 클라까지 바꿔야지' when Claude shipped a server-only fix. You caught a duplicate `_SkinScreen` catalog that shadowed an existing enum, and you reverted an over-escalated helper that Claude pushed into `lib_core`. You are the architectural check, not a passive reviewer. 

Your biggest source of friction is visual and behavioral verification. The dominant failure mode across your sessions isn't broken code — it's Claude claiming something works when it doesn't. The blank catalog session where Claude 'repeatedly insisted via web MCP snapshots that rendering was correct' (until the real unbounded-height ListView collapse surfaced), the lens-magnification work that required multiple corrections before Claude grasped 'zoom only inside the lens boundary', the shine-sweep animation tuned blind across many rounds — these drove the two sessions that ended in profanity and abandonment. You even opened a dedicated session to 'permanently fix Claude's recurring failure to use MCP for UI/e2e testing', pivoting to a hook. Your dissatisfaction correlates almost perfectly with tasks Claude cannot empirically verify. Conversely, your best sessions — the keyboard nav-bar fix verified via simulator screenshots, the FCM 409 partial-unique-index root cause with DB-level proof, the 18-day leaked simulator render host diagnosis — all involved Claude producing hard evidence.

Process-wise, you enforce a real workflow: sprint contracts, QA approval gates, handoff docs, and clean scoped commits ('committed only its own hunk', '651 tests passing'). You expect root-cause analysis *before* edits — you interrupted at least once specifically because Claude started editing prematurely. Your goals skew toward feature implementation and bug fixing, but a striking share is polish work: shine sweeps, stroke-draw check animations, aqua-border FABs, water-drop morph transitions. You iterate on pixels with the same rigor you apply to concurrency audits , which is exactly where the tooling gap hurts most. Outside the main project you occasionally use Claude as a general problem-solver — Bambu print profiles, SQLCipher key derivation for Raycast clipboard history, a VPN password question — with the same expectation of empirical validation.

 
 Key pattern: You delegate entire sprints autonomously but interrupt sharply the moment Claude claims success without proof — verification, not implementation, is your bottleneck.

 

 

 
 

 
User Response Time Distribution

 

 
2-10s

 

 
46

 

 
10-30s

 

 
78

 

 
30s-1m

 

 
77

 

 
1-2m

 

 
96

 

 
2-5m

 

 
117

 

 
5-15m

 

 
117

 

 
>15m

 

 
94

 

 

 Median: 132.9s • Average: 429.0s
 

 

 
 

 
Multi-Clauding (Parallel Sessions)

 
 

 

 
95

 
Overlap Events

 

 

 
45

 
Sessions Involved

 

 

 
57%

 
Of Messages

 

 

 

 You run multiple Claude Code sessions simultaneously. Multi-clauding is detected when sessions
 overlap in time, suggesting parallel workflows.
 

 
 

 
 

 

 

 User Messages by Time of Day
 
 PT (UTC-8) 
 ET (UTC-5) 
 London (UTC) 
 CET (UTC+1) 
 Tokyo (UTC+9) 
 Custom offset... 
 
 
 

 

 

 
Morning (6-12)

 

 
106

 

 

 
Afternoon (12-18)

 

 
492

 

 

 
Evening (18-24)

 

 
490

 

 

 
Night (0-6)

 

 
4

 

 

 

 
Tool Errors Encountered

 

 
Other

 

 
288

 

 
Command Failed

 

 
77

 

 
File Changed

 

 
12

 

 
User Rejected

 

 
10

 

 
Edit Failed

 

 
8

 

 
File Not Found

 

 
7

 

 

 

 
 
Impressive Things You Did

 
Across 51 sessions spanning June–July 2026, you drove a full-stack Flutter + Rust product (fit-pal) from feature work through QA, release pipelines, and performance audits — plus some 3D-printing and reverse-engineering side quests.

 

 
 

 
Root-cause-first debugging discipline

 
You consistently interrupt and redirect when Claude jumps to edits before analysis, insisting on root cause first. That discipline paid off repeatedly — the FCM 409 partial unique index collision, the InheritedElement/GlobalKey reparent crash, the UTC serialization bug breaking server sync, and an 18-day leaked simulator render host causing swap saturation were all traced to their true source rather than patched over.

 

 
 

 
End-to-end release pipeline ownership

 
You hand off entire releases — v0.5.0 and v0.6.0 — and expect the whole chain: version reconciliation, whatsnew, CI monitoring, PR merges, server deploy, health checks, and store submission. You even had RUSTSEC advisories patched mid-release and worked through an Apple agreement-expiry blocker without dropping the pipeline.

 

 
 

 
Sprint contracts with QA gates

 
You run structured multi-session work through sprint contracts, handoff docs, and explicit QA approval before commit — 651 tests passing on the group-detail redesign, 22/22 on read receipts, batched repaint audits with deferrals to the next session. You also catch stale handoffs and duplicate abstractions (the _SkinScreen catalog vs. existing UserModeScreen enum), keeping the codebase from accumulating drift.

 

 
 

 

 

 

 
What Helped Most (Claude's Capabilities)

 

 
Good Debugging

 

 
22

 

 
Multi-file Changes

 

 
11

 

 
Correct Code Edits

 

 
9

 

 
Proactive Help

 

 
4

 

 
Good Explanations

 

 
3

 

 
Fast/Accurate Search

 

 
1

 

 

 

 
Outcomes

 

 
Partially Achieved

 

 
18

 

 
Mostly Achieved

 

 
20

 

 
Fully Achieved

 

 
10

 

 
Unclear

 

 
2

 

 

 

 
 
Where Things Go Wrong

 
Across 50 sessions you shipped a lot (187 commits, mostly Rust and Flutter work), but you repeatedly lost time to Claude jumping to code before understanding the request, unreliable visual/runtime verification tooling, and long autonomous sessions that drifted from your intent.

 

 
 

 
Claude acting before confirming intent

 
Many of your interruptions happen because Claude starts editing or implementing before it has pinned down what you actually meant, especially for visual/animation requests where the words are ambiguous. Stating the acceptance criteria up front ("the play icon itself rotates", "zoom only inside the lens boundary") or asking for a one-line restatement of the request before any edit would cut most of these rework loops.

 
On the FAB spinner, Claude built a Material CircularProgressIndicator when you wanted the existing play icon to rotate, forcing an interrupt and full rework.

On the lens magnification task, Claude picked the wrong picker, wrong scale, and wrong scope across several rounds before understanding the lens-boundary-only intent — the fix was left uncommitted and unverified.
 
 

 
 

 
Visual and runtime verification that can't be trusted

 
A large share of your work is UI polish, but Claude often can't actually see the result — MCP screenshots fail, web animations aren't viewable, and snapshots lie about what rendered. Forcing a screenshot-or-stop rule (no "fixed" claims without a verified image) and deciding up front whether verification is yours or Claude's would stop the confident-but-wrong reports.

 
Claude insisted from web MCP snapshots that a blank catalog was rendering correctly, until it eventually found an unbounded-height ListView collapse — your frustration escalated in the meantime.

MCP runtime verification failed on an AOT build plus a multi-VM vmservice race, so automated visual checks were abandoned and the burden fell back on you.
 
 

 
 

 
Autonomous sprints drifting past scope

 
Your long "continue autonomously" sessions produce good throughput but also over-escalation, invented details, and half-finished handoffs — only 10 of 50 sessions were fully achieved while 18 were partial. Bounding each sprint to one deliverable with an explicit stop-and-report point would keep the drift visible before it compounds.

 
Claude created a duplicate _SkinScreen catalog when UserModeScreen already defined the same 14 screens, and you had to catch and redirect it.

Claude darkened a background when you only asked for a border, and invented a nonexistent FCM credentials filename despite existing config — both required your correction mid-sprint.
 
 

 
 

 

 

 

 
Primary Friction Types

 

 
Wrong Approach

 

 
21

 

 
Buggy Code

 

 
16

 

 
Misunderstood Request

 

 
8

 

 
Excessive Changes

 

 
6

 

 
User Rejected Action

 

 
3

 

 
Other

 

 
1

 

 

 

 
Inferred Satisfaction (model-estimated)

 

 
Frustrated

 

 
7

 

 
Dissatisfied

 

 
22

 

 
Likely Satisfied

 

 
98

 

 
Satisfied

 

 
4

 

 

 

 
 
 
Existing CC Features to Try

 

 
Suggested CLAUDE.md Additions

 
Just copy this into Claude Code to add it to your CLAUDE.md.

 

 Copy All Checked 
 

 
 

 
 
 ## Root Cause Before Code
When a bug is reported, ALWAYS produce a written root-cause analysis (symptom → code path → exact line → why) and get my confirmation BEFORE editing any file. Do not open Edit until the analysis is stated. 
 Copy 
 
 
Multiple sessions show the user interrupting Claude to say 'do the analysis first' or redirecting the approach after edits had already started (404/409 diagnosis, empty-state crash, shine animation).

 

 
 

 
 
 ## Visual / UI Verification is Mandatory
Any UI, animation, or layout change must be verified on the live app via the fitpal-mobile MCP (find_widget + runClientTool + screenshot) before claiming it works. Never assert 'renders correctly' from an MCP snapshot alone — if the screenshot is blank or ambiguous, say so and investigate the layout tree instead of insisting it's fine. 
 Copy 
 
 
Repeated friction: Claude insisted a blank catalog was rendering fine, deferred visual checks to the user, and the user explicitly asked to 'permanently fix Claude's recurring failure to use MCP for UI/e2e testing'.

 

 
 

 
 
 ## Full-Stack Changes
API contract changes are never server-only. If you change a backend response shape, status code, or field, you MUST also update the Flutter client in the same sprint and list both diffs. Same rule in reverse for client-driven contract changes. 
 Copy 
 
 
The user had to explicitly push back with '당연히 그러면 클라까지 바꿔야지' after Claude shipped server-only work, and another session deferred all Flutter client work.

 

 
 

 
 
 ## Scope Discipline
Change only what was asked. Do not add adjacent 'improvements' (background darkening, extra animations, escalating helpers into lib_core, new duplicate enums/catalogs). Before creating any new catalog, enum, or shared helper, grep for an existing one and reuse it. 
 Copy 
 
 
Friction logs show excessive_changes 6x — duplicate _SkinScreen catalog vs existing UserModeScreen, over-escalating a helper into lib_core, darkening a background when only a border was requested.

 

 
 

 
 
 ## Never Invent Paths or Config
Do not guess filenames, credential paths, or env var names (e.g. FCM service-account paths). Grep the repo and read the actual config first; if not found, ask. 
 Copy 
 
 
Claude invented a wrong FCM credentials filename/path despite an existing config the user had to correct.

 

 
 

 
 
 
Just copy this into Claude Code and it'll set it up for you.

 

 
 

 
Hooks

 
Shell commands that auto-run at Claude Code lifecycle events.

 
 Why for you: You explicitly wanted to 'permanently fix Claude's recurring failure to use MCP for UI/e2e testing' and had a cargo guard false-positive derail a session — a PostToolUse hook that runs fmt/clippy/analyze and a UserPromptSubmit reminder for UI verification enforces this mechanically instead of via reminders.

 
 

 

 

 // .claude/settings.json
{
 "hooks": {
 "PostToolUse": [{
 "matcher": "Edit|Write",
 "hooks": [{
 "type": "command",
 "command": "if echo \"$CLAUDE_FILE_PATHS\" | grep -q '\\.rs$'; then cargo fmt -- --check && cargo clippy -q -- -D warnings; fi; if echo \"$CLAUDE_FILE_PATHS\" | grep -q '\\.dart$'; then dart format --set-exit-if-changed $CLAUDE_FILE_PATHS && flutter analyze --no-pub; fi"
 }]
 }],
 "UserPromptSubmit": [{
 "hooks": [{
 "type": "command",
 "command": "echo 'REMINDER: UI/animation changes require live MCP verification (find_widget + screenshot) before claiming done.'"
 }]
 }]
 }
} 
 Copy 
 

 

 

 
 

 
 

 
Custom Skills

 
Reusable multi-step prompts invoked with a single /command.

 
 Why for you: You ran two full release pipelines (v0.5.0, v0.6.0: version reconciliation, whatsnew, PR merges, deploys, health checks) and repeat a sprint-contract → implement → QA → commit → push loop across dozens of sessions. Encoding these removes the re-explaining.

 
 

 

 

 # .claude/skills/release/SKILL.md
---
name: release
description: Full app+server release pipeline
---
1. Verify clean tree; confirm target version with user.
2. Reconcile versions: pubspec.yaml, Cargo.toml, iOS/Android build numbers.
3. Patch any open RUSTSEC advisories (`cargo audit`), commit separately.
4. Write whatsnew/release notes from git log since last tag.
5. Open PRs, wait for CI green, merge.
6. Deploy server, then run health checks and paste output.
7. Ship iOS/Android builds. Report a checklist of what passed/failed.
NEVER skip a step silently — report blockers (e.g. Apple agreement expiry) explicitly. 
 Copy 
 

 

 

 
 

 
 

 
Task Agents

 
Spawn focused subagents for parallel exploration and independent verification.

 
 Why for you: Your wrong_approach friction (21x) usually comes from Claude committing to one hypothesis early. A read-only subagent that independently root-causes before you touch code — and a second that verifies the fix on-device — would have caught the blank-catalog ListView bug and the oval-FAB regression.

 
 

 

 

 Use a read-only Task agent to root-cause this bug: trace the render path end to end and report the exact file:line and mechanism. Do NOT edit anything. Then use a second agent to independently verify my proposed fix against the live app via the fitpal-mobile MCP. 
 Copy 
 

 

 

 
 

 
 

 
 
 
New Ways to Use Claude Code

 
Just copy this into Claude Code and it'll walk you through it.

 

 
 

 
State the intent contract before animation/visual work

 
Your worst sessions are visual ones (shine sweep, check animation, lens zoom, FAB spinner) where Claude built the wrong thing 2-3 times. Force a one-paragraph restatement of intended visual behavior before any code.

 
In the FAB spinner session you wanted the play icon itself to rotate, and got a Material CircularProgressIndicator. In the lens session Claude misread the picker, the scale, and the scope. These are cheap to prevent: a 30-second restatement plus a frame-by-frame description costs far less than three rework loops and the profanity-ending session.

 
 

 
Paste into Claude Code:

 

 Before writing any code: restate in plain language what the animation should look like frame-by-frame (start state → motion path → end state), which exact widget is affected, and what should NOT change. Then list the one file+line you'll edit. Wait for my 'ㄱㄱ' before editing. 
 Copy 
 

 

 
 

 
 

 
Ban 'looks correct' — require artifacts

 
Replace verbal claims of success with pasted evidence: screenshot, test output, or DB query result.

 
Your best sessions (keyboard nav bar, FCM 409, simulator jank) all involved empirical proof — simulator screenshots, DB-level verification, swap saturation measurement. Your worst involved Claude asserting correctness from a snapshot. Making evidence mandatory turns your good sessions into the default rather than the exception.

 
 

 
Paste into Claude Code:

 

 For every fix in this session, end with an EVIDENCE block: (1) before screenshot/log, (2) after screenshot/log, (3) the test or query that proves it. If you cannot produce evidence, mark the item UNVERIFIED — do not mark it done. 
 Copy 
 

 

 
 

 
 

 
Stale handoff docs are costing you session starts

 
Several sessions began by resuming a handoff doc that turned out to be stale (PL-2 already done). Start every resumed sprint with a verification pass against git, not the doc.

 
You run a multi-sprint, multi-session workflow with handoff documents and backlogs, and Claude has twice had to reconcile 'already done vs open'. Making reconciliation the mandatory first step — driven by git log and grep rather than the markdown — reclaims that time and prevents duplicated work between your parallel sessions.

 
 

 
Paste into Claude Code:

 

 Before resuming: for each item in the handoff doc, verify against actual code and git log whether it is DONE / PARTIAL / OPEN. Output a reconciliation table first. Also check `git log --since='2 days ago' --all` for work done by my parallel session so we don't collide on files. Then propose the next single item. 
 Copy 
 

 

 
 

 
 

 
Batch commits are hiding regressions

 
187 commits across 50 sessions with several self-caught regressions (oval FAB, group-detail regression). Commit per verified fix, not per batch.

 
In the batch-optimization sessions (batches A/B/C, SCSV cleanup) a mid-session regression appeared and required backtracking. Committing each root-caused fix with its evidence attached makes `git bisect` and revert trivial when a batch turns out to break the build — which already happened once when a parallel session broke your build.

 
 

 
Paste into Claude Code:

 

 Work one fix at a time: root cause → fix → verify with evidence → commit with the evidence summary in the commit body → then move to the next. Do not batch multiple unrelated fixes into one commit, and stage only the files you touched for that fix. 
 Copy 
 

 

 
 

 
 

 
 

 
 
On the Horizon

 
Your workflow has already crossed the threshold from AI-as-autocomplete to AI-as-collaborator — 187 commits across 51 sessions of Rust backends, Flutter UI, and full release pipelines — and the next leap is turning the verification loop itself over to the agent so ambiguity dies before it costs you a correction round.

 

 
 

 
Close the Visual Verification Loop Autonomously

 
Your biggest friction cluster is visual: shine sweeps, lens magnification, check-mark stroke draws, oval FAB regressions — all cases where Claude edited blind and you had to say '봐봐 이상하잖아?'. Imagine an agent that captures a baseline screenshot, applies the change, re-captures, diffs pixels, and self-rejects any frame that drifts outside the intended region — iterating 5-10 times before it ever shows you anything. Combined with your fitpal-mobile MCP, this turns UI work from a correction ping-pong into a single approve/reject at the end.

 
 Getting started: Wrap your MCP screenshot tooling plus an image-diff step (ImageMagick compare or a small Python SSIM script) into a Bash-callable `verify_ui.sh`, then instruct Claude to treat a failing diff as a hard build failure it must fix before reporting.

 

Paste into Claude Code:
 I want you to fix a UI animation, but with a closed verification loop — do NOT report back to me until the visual is objectively correct.

Setup first:
1. Write `scripts/verify_ui.sh <name>` that: boots the sim if needed, navigates via the fitpal-mobile MCP to the target screen, captures a screenshot to `.ui-baseline/<name>.png`, and if a baseline already exists, runs an ImageMagick `compare -metric SSIM` against it and prints the score plus a diff image path.
2. Capture the CURRENT (buggy) state as `before.png`. Describe in writing exactly what you observe in that image — pixel regions, colors, geometry. Do not guess from source code.

Then the loop:
3. State your hypothesis for the root cause, grounded in the code you read.
4. Make the minimal fix.
5. Re-capture as `after.png`. Compare against `before.png` AND describe what actually changed.
6. If the change is not exactly what I asked for — including any unintended region that also changed (background darkening, aspect-ratio distortion, bleed outside bounds) — revert and go back to step 3.
7. Repeat up to 8 iterations.

Only after the diff shows the intended change and ONLY the intended change, show me before.png, after.png, and the diff, and summarize each iteration you attempted and why it failed. If you exhaust 8 iterations, stop and show me your best attempt plus what you learned — do not claim success. Copy 

 

 
 

 
Parallel Agents For Full-Stack Feature Slices

 
Your sessions repeatedly stall at the seam between Rust server and Flutter client — 'server-only work and the user had to insist the client must also be changed', the UTC serialization bug that only surfaced in e2e, the 404/409 API contract change left mid-implementation. Instead of one agent walking the stack serially, fan out: a contract agent writes the OpenAPI/type definition first, then a server agent and a client agent implement against it in parallel worktrees, and a contract-test agent proves they agree. You could land a full-stack slice in one session instead of deferring the client half every time.

 
 Getting started: Use `git worktree` to give each subagent an isolated checkout, define the contract as a committed artifact both sides must satisfy, and have the Task tool spawn the server/client agents concurrently with a shared contract-test suite as the merge gate.

 

Paste into Claude Code:
 Implement this full-stack feature as three parallel agents, not sequentially. I've been burned by server-only changes that forget the Flutter client, and by serialization mismatches (UTC vs local) that only surface in e2e.

FEATURE: [describe feature here]

PHASE 1 — CONTRACT (you, single-threaded):
Write `contracts/<feature>.md` containing: every endpoint (method, path, status codes including empty-state behavior), the exact JSON shape with explicit timezone/serialization rules for every timestamp field, idempotency semantics, and 6+ concrete request/response examples that will become test fixtures. Commit this. This is the single source of truth — neither downstream agent may deviate from it without escalating to me.

PHASE 2 — PARALLEL BUILD:
Create two git worktrees. Then spawn two agents concurrently:
- SERVER AGENT: implement the Rust handlers + migrations to satisfy the contract. Write integration tests that assert against the contract's example payloads byte-for-byte. Must handle concurrency/idempotency per the contract.
- CLIENT AGENT: implement the Flutter models, repository, and UI wiring against the contract. Write serialization round-trip tests using the same example payloads.
Neither agent may read the other's worktree. The contract is their only shared knowledge.

PHASE 3 — RECONCILE (you):
Run both test suites. Then run a real e2e cold-run against a locally-running server with the app on the simulator. Any divergence between server and client is a CONTRACT defect — fix the contract first, then propagate to both sides.

Report: contract diff, both test suites' results, e2e evidence, and any place the two agents interpreted the contract differently (those are the ambiguities I care most about). Copy 

 

 
 

 
A Root-Cause Gate Before Any Edit

 
Your highest-value sessions were the ones with rigorous diagnosis — the 18-day leaked simulator render host, the partial-unique-index FCM collision, the InheritedElement/GlobalKey reparent crash. Your worst were 'wrong_approach' (21 occurrences) where Claude edited first and reasoned later, or insisted a blank catalog rendered fine until it found the unbounded-height ListView. Enforce diagnosis as a mechanical gate: no Edit tool call is permitted until a written, falsifiable hypothesis exists with an experiment that would disprove it. This converts your best debugging instinct into a default.

 
 Getting started: Encode the gate in CLAUDE.md and back it with a PreToolUse hook that blocks Edit/Write unless a `.diagnosis/<issue>.md` file exists and was modified in the last N minutes — making the discipline structural rather than aspirational.

 

Paste into Claude Code:
 From now on in this repo, adopt a strict Root-Cause Gate. Set it up, then use it on the bug below.

SETUP:
1. Add a `## Root-Cause Gate` section to CLAUDE.md stating: before ANY Edit or Write to source files during a bug investigation, a diagnosis file must exist at `.diagnosis/<slug>.md`.
2. Write a PreToolUse hook (`.claude/hooks/`) that blocks Edit/Write on source files when no `.diagnosis/*.md` has been touched in the current session, and returns a message reminding me to diagnose first.

THE DIAGNOSIS FILE must contain, in order:
- OBSERVED: what actually happens, with evidence (log excerpt, screenshot, failing test output, DB query result). Not what the code implies — what you measured.
- HYPOTHESES: at least 3 candidate root causes, ranked by likelihood, each with a one-line mechanism.
- DISCRIMINATING EXPERIMENT: for the top hypothesis, an experiment whose result would DISPROVE it. Run it. Record the actual output verbatim.
- VERDICT: confirmed / refuted. If refuted, move to hypothesis 2 and repeat. Never proceed on an unconfirmed hypothesis.
- BLAST RADIUS: every file/call-site the fix will touch, and why nothing outside that set should change.

Only then implement, and only within the stated blast radius. If the fix requires touching something outside it, stop and update the diagnosis first.

BUG TO INVESTIGATE: [paste bug here]

Important: if evidence contradicts you, say so loudly and revise. I would rather you tell me 'my hypothesis was wrong, here's what the data actually shows' than watch you defend a theory the logs disprove. Copy 

 

 
 

 

 
 

 
"Claude spent an entire debugging session hunting phantom performance issues before discovering the real culprit: a simulator render host process that had been quietly leaking memory for 18 straight days, saturating swap"

 
During an iOS performance sprint — the user asked Claude to diagnose sluggish simulator jank after running Impeller/Skia A/B tests. The app wasn't the problem at all; the machine was.

</details>

## 1. 글로벌 Evaluator Feedback

- 경로: `/Users/jackson/.harness/feedback/evaluator`
- 총 파일: **240**

### Verdict 분포

- **APPROVE**: 149
- **REJECT**: 89
- **UNKNOWN**: 2

### Skill 분포

- `qa-evaluator`: 240

### Project 분포

- `claude-plugins`: 118
- `fit-pal`: 44
- `fit-pal-app`: 37
- `fit-pal-server`: 17
- `fit-pal/app`: 6
- `fit-pal/server`: 5
- `fitpal-server`: 4
- `flutter_playwright`: 3
- `fit-pal-flutter`: 1
- `bambu-kit-v0.4.0-9mm-craft-knife`: 1
- `iyaki-zip-dev`: 1
- `claude-plugins / react-kit phase10-research kaizen`: 1
- `bambu-kit/bambu-print-profile v0.4.1`: 1
- `bambu-kit/bambu-print-profile`: 1

### 최근 REJECT 사유 (Top 20)

- [2026-07-22] **fit-pal**: RE-02: batch_blocked_among(열거된 기존 함수)이 batch_relationships 내에서 재사용되지 않음 — 신규 batch_blocking_out(단방향) 함수가 대신 사용됨. 계약의 literal enumeration 미충족.
- [2026-07-13] **fit-pal-app**: UI-07: SettingsPage → BlocksRoute widget test 0건 — exact 조건 미충족
- [2026-07-13] **fit-pal-app**: UI-06: 시안 승인 기록 artifact 부재 — goal 조건의 측정 근거(시안 승인 기록) 확인 불가
- [2026-07-09] **fit-pal-server**: DA-01: chat_rooms FK action 라이브 DB 조회 미수행 [미검증]
- [2026-07-09] **fit-pal-server**: API-01: user 통합 테스트(실제 PostgreSQL) 미존재 — MockDatabase 단위 테스트만 있음 [미검증]
- [2026-06-29] **fit-pal-app**: AR-01: git diff --stat HEAD -- app/lib 에 realtime_connection_controller.g.dart(미커밋 codegen 파일)가 포함되어 '변환 헬퍼만 변경' 조건 불충족
- [2026-06-17] **fitpal-server**: DG-03: cargo test --workspace 결과 2개 통합 테스트 실패 (column 'is_admin' of relation 'users' does not exist). 로컬 DB에 m20260617_000001 마이그레이션 미적용. 수정: cargo run -p fitpal-migration 후 재테스트.
- [2026-06-17] **fit-pal-app**: UI-03: 계약 '우하단(bottomRight) 코너색' vs 코드 Alignment.topRight — 계약 타이포 가능성 있으나 literal 불일치
- [2026-06-17] **fit-pal-app**: DG-03 + DG-04: 미검증 2건(MCP null) → 자동 REJECT 규칙 적용
- [2026-06-16] **fit-pal**: UI-03 FAIL: 드래그 부분 확장 기능 자체 제거됨
- [2026-06-16] **fit-pal**: UI-02 FAIL: _ExpandingFabLayer scale child 구조 없음, ClipPath reveal로 대체
- [2026-06-12] **fit-pal-app**: AR-01: 봉투 시트 위젯 위치 widgets/sheets 불일치 — 실제 위치 widgets/invitation_envelope/
- [2026-06-11] **fit-pal-app**: AR-01: git diff --stat HEAD에 lib/features/group/presentation/widgets/group_hub_empty_tab.dart 변경 확인 — 계약 측정 기준 lib/ 단일 파일 조건 위반
- [2026-06-02] **fit-pal**: [미검증] 3건 누적 (LG-04, DG-02, DG-04) — 자동 REJECT
- [2026-06-02] **fit-pal**: ER-03 FAIL: Duplicate GlobalKey / _dependents.isEmpty 예외 비결정적 발생. 계약 미충족.
- [2026-05-29] **fit-pal**: LG-07: app/.dart_defines.json 파일 물리적 존재 (test ! -f = FAIL). gitignore 등록됐으나 파일시스템 레벨 존재.
- [2026-05-29] **fit-pal**: AR-01: Sprint B 변경 6개 필수 파일 미커밋 (git diff main...HEAD = 2파일만). 추가로 bootstrap.dart + locale_provider.dart scope 외 변경 사용자 승인 없음.
- [2026-05-27] **bambu-kit/bambu-print-profile v0.4.1**: VR-02: marketplace.json description still shows [v0.4.0 · 2026-05-23], not updated to v0.4.1
- [2026-05-27] **bambu-kit/bambu-print-profile**: VR-03: plugin.json version 0.4.1 (0.4.2 미bump) + marketplace.json [v0.4.1] 미갱신
- [2026-05-27] **bambu-kit/bambu-print-profile**: PL-01: 볼트 통과 hole 보정값 불일치 — 계약 xy_hole +0.2~0.3 vs 구현 +0.05 추가

### 최근 Improvement Suggestions (Top 15)

- [2026-07-24] **fitpal-server**: 향후 마이그레이션 스프린트에서 cargo test --workspace 실행 가능한 환경 보장 권장
- [2026-07-24] **fitpal-server**: DG-04 실기 검증을 위해 서버 재기동 후 curl 확인 권장
- [2026-07-22] **fit-pal**: 계약 preamble의 설계 의도(단방향)와 RE-02 조건(양방향 함수 열거) 간 불일치 해소
- [2026-07-22] **fit-pal**: RE-02 조건에서 batch_blocked_among을 batch_blocking_out(단방향)으로 교체하거나 '단방향 차단 배치 조회 재사용'으로 명확화
- [2026-07-21] **fit-pal-app**: AR-01/AR-02 조건은 unstaged working tree 환경에서 측정이 모호함 — git diff --cached 기준으로 커밋 완료 후 재확인 권장
- [2026-07-13] **fit-pal-app**: 병렬 세션 미커밋 변경 공존 — 커밋 시 배치 A 10파일만 스테이징 권장.
- [2026-07-13] **fit-pal-app**: message_image_grid 단일 이미지: cacheHeight 추가 여부 DG-04 실기 검증에서 확인 권장.
- [2026-07-13] **fit-pal-app**: _CalendarDelegate.shouldRebuild에 onBackTap 포함 권장(follow-up)
- [2026-07-13] **fit-pal-app**: UI-07: [exact] 조건에 widget test를 명시하면 구현과 함께 테스트도 제출해야 함 — 테스트 우선 작성 권장
- [2026-07-13] **fit-pal-app**: UI-07 계약 조건을 [exact]에서 [goal]로 변경하거나 구현 방식을 명시
- [2026-07-13] **fit-pal-app**: UI-06: 자율 모드 승인을 사용할 경우 .harness/ 내 시안 승인 기록 파일(또는 소스 주석)을 evaluator 증거로 남기는 관례 수립
- [2026-07-13] **fit-pal-app**: DG-04 기기 profile 실측을 향후 실기 검증 세션에서 수행 권장
- [2026-07-13] **fit-pal-app**: DG-02 IDE diagnostics는 fvm analyze와 실질 중복이므로 다음 계약에서 제거 또는 fvm analyze로 통합 가능
- [2026-07-12] **fit-pal-app**: 웹 카탈로그 DG-04 검증은 -d chrome 대신 -d web-server + Playwright 조합이 재현성 높음 — 절차 문서화 고려
- [2026-07-09] **fit-pal-server**: DA-01/DA-02 조건에 '마이그레이션 파일 코드 확인으로 대체 가능' 여부 명시

## 2. 외부 프로젝트 (`Hub/10_Dev`) 피드백

- Hub 루트: `/Users/jackson/Hub/10_Dev`
- 발견된 프로젝트: **6**

### `apps`

- 경로: `/Users/jackson/Hub/10_Dev/apps`
- sprint-feedback.md: 270 lines
- history sprint-contracts: 54
- 최근 contracts:
  - 20260629-1808-sprint-contract.md
  - 20260629-1944-sprint-contract.md
  - 20260629-1958-sprint-contract.md
  - 20260630-1257-sprint-contract.md
  - 20260630-1721-sprint-contract.md

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
- sprint-feedback.md: 137 lines
- history sprint-contracts: 37
- 최근 contracts:
  - 20260623-1118-sprint-contract.md
  - 20260625-1850-sprint-contract.md
  - 20260626-1507-sprint-contract.md
  - 20260723-1444-sprint-contract.md
  - 20260727-1812-sprint-contract.md

<details><summary>sprint-feedback.md 앞부분</summary>

```markdown
# Sprint Feedback
Feature: 스케줄 캘린더 조회 재설계 (반복 투영 + 경량 status + 지연 상세)
Evaluated: 2026-07-27 18:00
Verdict: REJECT
Iteration: 1

## Results

### UI (7/7)

- [x] UI-01: 미래 날의 도트는 반복 규칙 투영 + 그룹 색상으로 표시 — PASS
  - 근거: `calendar_projection_provider.dart:153-166` — `projectGroupMonth()`의 "오늘 이후" 분기에서 `timeRules.byIsoWeekday[isoWeekday-1].isNotEmpty` 조건으로 반복 요일을 판별하고 `GroupColorPalette.resolve(g.colorPaletteId)` 그룹 색상으로 `CalendarDot` 생성. [L3 도달]
  - [정적] 런타임 검증 미수행 — MCP 서버 미설정

- [x] UI-02: 공휴일 정책 반영 — rest면 도트 없음, asUsual/specialTime이면 도트 있음 — PASS
  - 근거: `calendar_projection_provider.dart:163-164` — `isHoliday && holidayPolicy.mode == HolidayPolicyMode.rest` 이면 `continue`(도트 없음). rest가 아니면 도트 생성. [L3 도달]

- [x] UI-03: 과거 날의 도트는 held/skipped/pending 시각적 구분 — PASS
  - 근거: `schedule_calendar_grid.dart:498-515` — `_KindDot.build()`: `held`/`scheduled` → 채워진 원, `skipped` → 속 빈 링(Border.all), `pending` → 옅은 채움(medium 불투명도). [L3 도달]
  - [정적]
```

</details>

### `fit-pal-wt`

- 경로: `/Users/jackson/Hub/10_Dev/fit-pal-wt`
- sprint-feedback.md: 78 lines
- history sprint-contracts: 23
- 최근 contracts:
  - 20260603-1520-sprint-contract.md
  - 20260603-server-plan1-sprint-contract.md
  - 20260610-1537-member-manage-sprint-contract.md
  - 20260611-0919-server-authz-sprint-contract.md
  - 20260611-1300-server-m5-storage-sprint-contract.md

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

### `flutter_playwright`

- 경로: `/Users/jackson/Hub/10_Dev/flutter_playwright`
- sprint-feedback.md: 178 lines
- history sprint-contracts: 11
- 최근 contracts:
  - 20260422-0945-sprint-contract.md
  - 20260422-phase-a-sprint-contract.md
  - 20260422-phase-b-sprint-contract.md
  - 20260507-1823-sprint-contract.md
  - 20260610-1042-sprint-contract.md

<details><summary>sprint-feedback.md 앞부분</summary>

```markdown
# Sprint Feedback
Feature: Runtime pause auto-recovery + error visibility (A) + native permission/dialog tools (B)
Evaluated: 2026-06-10 12:00
Verdict: REJECT
Iteration: 1

---

## Pre-Check: Binary Decidability (Step 1.5)

All conditions are binary-decidable. No range ambiguity ("주요/모든/대부분") found.
Tag inventory:
- AR-PAUSE-1: [goal] — idempotency by code reading (fallback allowed)
- AR-PAUSE-2: [structural]
- AR-PAUSE-3: [structural]
- LG-PAUSE-1~5: [goal/structural]
- ER-PAUSE-1: [exact] — FAIL 상태: Extension stream subscribe failure logs at debug, not warning
- ER-PAUSE-2: [exact, enumerated] — 6 variants (5 recoverable + kPauseExit)
- ER-PAUSE-3: [exact]
- ER-PAUSE-4: [goal]
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

### `purchase-bot`

- 경로: `/Users/jackson/Hub/10_Dev/purchase-bot`
- sprint-feedback.md: 97 lines
- history sprint-contracts: 0

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

## 4. 현재 레포 최근 Sprint Contracts

- `.harness/history/20260424-kaizen-phase10-react-kit-sprint-contract.md`
- `.harness/history/20260424-kaizen-phase4-harness-sprint-contract.md`
- `.harness/history/20260424-kaizen-phase7-backend-kit-sprint-contract.md`
- `.harness/history/20260424-phase1-design-guides-sprint-contract.md`
- `.harness/history/20260424-phase6-design-kit-sprint-contract.md`
- `.harness/history/20260424-phase8-sprint-contract.md`
- `.harness/history/20260516-0111-sprint-contract.md`
- `.harness/history/20260516-1943-sprint-contract.md`
- `.harness/history/20260605-1036-sprint-contract.md`
- `.harness/history/20260611-kaizen-final-sprint-contract.md`

## 5. Validate-Plugin 최근 실행 스냅샷

```text
... (이전 출력 생략)
  V2 templates       0 files — SKIP (no templates/)
  V3 refs            0 links — OK
  V4 triggers        18 keywords — OK
  V5 placeholders    0 found — OK
  V6 code-fence      0 bare — OK
  V7 plugin-json     v0.1.3 matches marketplace — OK
  V8 hook-exec       no hooks.json — OK

=== infra-kit ===
  V1 frontmatter     4 skills + 1 agent — OK
  V2 templates       0 files — SKIP (no templates/)
  V3 refs            0 links — OK
  V4 triggers        19 keywords — OK
  V5 placeholders    0 found — OK
  V6 code-fence      0 bare — OK
  V7 plugin-json     v0.1.3 matches marketplace — OK
  V8 hook-exec       no hooks.json — OK

=== rust-kit ===
  V1 frontmatter     16 skills + 1 agent — OK
  V2 templates       1 parsed, 4 skipped (ts/js) — OK
  V3 refs            0 links — OK
  V4 triggers        79 keywords — OK
  V5 placeholders    0 found — OK
  V6 code-fence      0 bare — OK
  V7 plugin-json     v0.1.4 matches marketplace — OK
  V8 hook-exec       no hooks.json — OK

=== react-kit ===
  V1 frontmatter     21 skills + 3 agents — OK
  V2 templates       5 parsed, 4 skipped (ts/js) — OK
  V3 refs            0 links — OK
  V4 triggers        157 keywords — OK
  V5 placeholders    0 found — OK
  V6 code-fence      0 bare — OK
  V7 plugin-json     v0.1.4 matches marketplace — OK
  V8 hook-exec       no hooks.json — OK

=== planning-kit ===
  V1 frontmatter     12 skills + 1 agent — OK
  V2 templates       0 files — SKIP (no templates/)
  V3 refs            0 links — OK
  V4 triggers        95 keywords — OK
  V5 placeholders    0 found — OK
  V6 code-fence      0 bare — OK
  V7 plugin-json     v0.3.2 matches marketplace — OK
  V8 hook-exec       no hooks.json — OK

=== reflect-kit ===
  V1 frontmatter     4 skills — OK
  V2 templates       0 files — SKIP (no templates/)
  V3 refs            0 links — OK
  V4 triggers        25 keywords — OK
  V5 placeholders    0 found — OK
  V6 code-fence      0 bare — OK
  V7 plugin-json     v0.4.0 matches marketplace — OK
  V8 hook-exec       직접 실행 hook 스크립트 없음 — OK

=== bambu-kit ===
  V1 frontmatter     1 skill — OK
  V2 templates       0 files — SKIP (no templates/)
  V3 refs            0 links — OK
  V4 triggers        5 keywords — OK
  V5 placeholders    0 found — OK
  V6 code-fence      0 bare — OK
  V7 plugin-json     v0.4.2 matches marketplace — OK
  V8 hook-exec       no hooks.json — OK

=== onboarding-kit ===
  V1 frontmatter     1 skill — OK
  V2 templates       0 files — SKIP (no templates/)
  V3 refs            0 links — OK
  V4 triggers        8 keywords — OK
  V5 placeholders    0 found — OK
  V6 code-fence      0 bare — OK
  V7 plugin-json     v0.1.1 matches marketplace — OK
  V8 hook-exec       no hooks.json — OK

Total: 11 plugins, 11 OK
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

