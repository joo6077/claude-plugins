# Kaizen Data Pool

Generated: 2026-08-13T08:38:11
Generator: `scripts/collect-kaizen-data.py`

카이젠 오케스트레이션의 Phase 별 서브에이전트가 참조할 통합 데이터 풀이다. 이 파일은 `scripts/collect-kaizen-data.py` 로 재생성된다 — 수동 수정 금지.

## 0. `/insights` Report (외부 도구 산출물)

- 경로: `/Users/jackson/.claude/usage-data/report.html` · HTML 추출 텍스트
- 최근 갱신: 2026-08-13T08:33:57 ✓ VERY FRESH (0.1시간 전)
- 모든 Phase 서브에이전트가 **최우선** 참조해야 한다 (Friction Points / Recommended Patterns / Feature Suggestions / 이번 사이클 신규 워크플로우 제안)

<details><summary>insights report 본문 (auto-extracted)</summary>

Claude Code Insights 
 

 
 
 
 

 
Claude Code Insights

 
1,551 messages across 71 sessions (81 total) | 2026-06-12 to 2026-08-12

 
 

 
At a Glance

 

 
 What's working: You run Claude like an engineering org, not a code generator: sprint contracts with QA gates written up front, root-cause analysis demanded before any edit, and MCP-driven verification where Claude has to drive the live simulator and capture real pixels rather than claim success. That discipline surfaced genuinely deep bugs — a partial unique index collision behind FCM 409s, a GlobalKey reparent crash, and simulator jank that turned out to be a leaked render host rather than app code. The full 0.6.0 release pipeline and the contract-gated feed slices show this scales past debugging into shipping. Impressive Things You Did → 

 
 What's hindering you: On Claude's side, the dominant pattern is acting before diagnosing — reaching for an edit when you asked for analysis, and misreading intent on visual work where it can't see what you see. It also applies confirmed decisions to some surfaces but not all, then defends itself with test evidence instead of accepting your bug report, which is what escalated several design sessions. On your side, design requests tend to arrive without a pinned axis or a scope cap, so Claude fills the ambiguity with sprawling design systems; handoff docs also go stale between sessions, causing Claude to re-derive or chase already-finished work. Where Things Go Wrong → 

 
 Quick wins to try: Turn your sprint-contract and release-pipeline rituals into Custom Skills so the gates, evidence requirements, and commit hygiene load identically every time instead of being re-explained. Use Task Agents as an adversarial QA reviewer that only reads the contract and the diff — separating implementer from verifier removes the incentive to argue a fix is done. For design work, name the axis and the artifact count explicitly ('five variants, bubble shape only, color held constant, no supporting infrastructure') and require a screenshot before any correctness claim. Features to Try → 

 
 Ambitious workflows: Build toward a golden-screenshot harness: every catalog variant renders to a pinned PNG, a manifest maps each confirmed decision to every surface that must consume it, and an agent diffs all surfaces after each change and fails loudly on drift — design decisions become enforceable rather than debatable. Next, fan a single sprint contract out to parallel lanes (migrations/routers, Flutter client, tests, adversarial QA) with an orchestrator that refuses to merge until every lane is green, ending the server-lands-without-client stall. Longer term, your backlog can drain itself overnight: an agent that picks the top unblocked item, verifies it isn't already done, implements on a branch, iterates until the suite passes, and opens a PR with evidence attached. On the Horizon → 

 

 

 

 
 What You Work On 
 How You Use CC 
 Impressive Things 
 Where Things Go Wrong 
 Features to Try 
 New Usage Patterns 
 On the Horizon 
 Team Feedback 
 

 

 

1,551

Messages

 

+95,149/-10,280

Lines

 

890

Files

 

24

Days

 

64.6

Msgs/Day

 

 
 
What You Work On

 

 
 

 

 FitPal Mobile App — Feature Development & Bug Fixing 
 ~22 sessions 
 

 
Extensive Flutter client work on the FitPal fitness app, including the workout player, group detail screens, login flows, schedules, and a profile statistics tab. Claude was used heavily for root-cause debugging (keyboard-driven nav bar shifts, InheritedElement/GlobalKey reparent crashes, serialization bugs), then implementing and verifying fixes on the iOS simulator via the fitpal-mobile MCP tools. Sessions typically ended with tests run, commits made, and changes pushed.

 

 
 

 

 UI/UX Design Mockups & Visual Iteration 
 ~17 sessions 
 

 
Iterative design exploration in a widget catalog — chat bubble variants, group chip photo treatments with gradient triangles and aqua rims, jewel color swatches, shine-sweep and stroke-draw check animations, and player mockup variants. Claude generated dozens of tiles and used screenshot_widget to visually verify each round. This was the most friction-prone area: Claude repeatedly misread the intended design axis, over-scoped into sprawling design systems, and failed to propagate confirmed decisions across all surfaces, causing notable user frustration.

 

 
 

 

 Backend API, Concurrency & Data Integrity 
 ~12 sessions 
 

 
Rust server work on the FitPal backend covering API contract changes (404→200 empty responses), FCM token idempotency and partial unique index collisions, feed TOCTOU races resolved with in-SQL EXISTS predicates, S3 object reclamation, and a broad concurrency/correctness audit. Claude traced code paths across migrations, entities, services, and routers, wrote tests, and drove QA-gated sprint contracts before pushing to dev.

 

 
 

 

 Performance Auditing & Rendering Optimization 
 ~8 sessions 
 

 
Jank hunting and repaint/rebuild audits across the Flutter app, including Impeller vs. Skia A/B testing, SCSV cleanup batches, and a custom lint rule to prevent regressions. One standout session traced apparent iOS simulator sluggishness to an 18-day leaked simulator render host causing swap saturation rather than app code. Claude produced measured evidence and batched optimizations for QA approval.

 

 
 

 

 Release Engineering & Infrastructure Backlog 
 ~7 sessions 
 

 
Full release pipeline execution (version reconciliation, whatsnew notes, PR merges, deploys, health checks) for the 0.6.0 server and app release, plus infrastructure hardening such as container image digest pinning and audit-backlog remediation. Claude also wrote handoff docs and implementation plans for cross-session continuation, though it occasionally worked from stale handoffs and had to re-derive the real remaining work.

 

 
 

 

 3D Printing Profile Generation 
 ~5 sessions 
 

 
Using a bambu-print-profile skill to generate validated Bambu slicer profiles for shower-box components and iteratively-evolving holster models. Claude analyzed each model's geometry to tune supports, ironing, and bed adhesion. Real-world print results kept surfacing new issues — curved-surface stair-stepping, voronoi stringing, base peeling — so outcomes were only partially successful.

 

 
 

 

 

 

 
What You Wanted

 

 
Feature Implementation

 

 
26

 

 
Ui Design Mockups

 

 
17

 

 
Ui Design Iteration

 

 
17

 

 
Iterative Visual Refinement

 

 
12

 

 
Bug Fix

 

 
12

 

 
Bug Fixing

 

 
8

 

 

 

 
Top Tools Used

 

 
Bash

 

 
8464

 

 
Edit

 

 
2549

 

 
Read

 

 
2242

 

 
Mcp Fitpal-Web Find Widget

 

 
878

 

 
Mcp Fitpal-Mobile RunClientTool

 

 
851

 

 
Mcp Fitpal-Mobile Find Widget

 

 
552

 

 

 

 

 

 
Languages

 

 
Markdown

 

 
832

 

 
Rust

 

 
706

 

 
JSON

 

 
64

 

 
YAML

 

 
52

 

 
Python

 

 
24

 

 
HTML

 

 
13

 

 

 

 
Session Types

 

 
Multi Task

 

 
33

 

 
Iterative Refinement

 

 
22

 

 
Single Task

 

 
13

 

 
Quick Question

 

 
2

 

 
Undefined

 

 
1

 

 

 

 
 
How You Use Claude Code

 

 
You run Claude Code like a long-horizon engineering manager rather than a prompt-and-wait user. Across 71 sessions and 3,600+ hours you've built a workflow with handoff docs, sprint contracts, QA gates, and audit backlogs — sessions routinely open with "continue from the handoff doc" or "resume the queued sprint," and close with commits pushed and a written handoff for the next run. You delegate broad, autonomous mandates ("autonomously continue backend audit remediation with research where needed", "process and verify these bug reports") and expect Claude to self-navigate the codebase, run tests, get QA approval, and push. The 241 commits and 8,464 Bash calls show you're comfortable letting Claude run for long stretches — you optimize for throughput over control, and you've built process scaffolding to keep that safe .

But you interrupt hard and fast when the approach is wrong. You stopped Claude mid-edit to demand root-cause analysis first. You interrupted an AskUserQuestion to redirect toward catalog styles. You cut off a tool call to pivot to Codex's recommendation. When Claude implemented a Material CircularProgressIndicator instead of rotating the existing play icon, you interrupted and reworked it. Your corrections are terse, high-signal, and often blunt — "봐봐 이상하잖아?", "당연히 그러면 클라까지 바꿔야지", "어휴 답답하다" — and escalate quickly when Claude argues back instead of accepting a bug report. That happened on the A3 mockup variant: Claude countered your report with test evidence and you went to profanity. The friction data backs this: 50 wrong_approach and 27 misunderstood_request events, 51 dissatisfied and 17 frustrated turns.

Your hardest domain is visual iteration. Roughly a third of your goals are UI mockups, design iteration, or visual refinement, and it's where things break down — the chat bubble mockups, the metallic variants, the shine-sweep animation, the aqua-fill chips. You want a *design axis* explored (bubble shape, color, effect), and Claude keeps producing sprawling derivative systems instead, which you respond to by demanding deletion of everything but the input bar. You verify with your own eyes, not Claude's claims — you rejected repeated MCP snapshot assurances that a blank catalog was fine until the real unbounded-height ListView bug surfaced. That's why 878 find_widget and 494 screenshot_widget calls appear: you've pushed Claude toward pixel-level empirical proof rather than assertion. When Claude actually does that — simulator screenshots proving bug-vs-fix on the keyboard nav bar, tracing sluggishness to an 18-day leaked render host — you rate it essential.

 
 Key pattern: You hand off large autonomous sprints with contract-and-QA scaffolding, then interrupt bluntly the moment Claude drifts from your intended approach — especially on visual work, where you trust screenshots over claims.

 

 

 
 

 
User Response Time Distribution

 

 
2-10s

 

 
64

 

 
10-30s

 

 
82

 

 
30s-1m

 

 
116

 

 
1-2m

 

 
138

 

 
2-5m

 

 
189

 

 
5-15m

 

 
210

 

 
>15m

 

 
118

 

 

 Median: 154.3s • Average: 397.1s
 

 

 
 

 
Multi-Clauding (Parallel Sessions)

 
 

 

 
129

 
Overlap Events

 

 

 
65

 
Sessions Involved

 

 

 
55%

 
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

 

 
149

 

 

 
Afternoon (12-18)

 

 
756

 

 

 
Evening (18-24)

 

 
598

 

 

 
Night (0-6)

 

 
48

 

 

 

 
Tool Errors Encountered

 

 
Other

 

 
506

 

 
Command Failed

 

 
137

 

 
Edit Failed

 

 
16

 

 
User Rejected

 

 
12

 

 
File Changed

 

 
6

 

 
File Not Found

 

 
5

 

 

 

 
 
Impressive Things You Did

 
Across 71 sessions spanning two months, you drove 241 commits on a full-stack Rust + Flutter fitness app while building an unusually rigorous verification and design-iteration pipeline around Claude.

 

 
 

 
MCP-driven visual verification loop

 
You wired up custom MCP servers for both web and mobile surfaces and lean on them heavily — nearly 2,000 calls to find_widget, screenshot_widget, and runClientTool. Instead of accepting claims that a fix works, you make Claude drive the live simulator, capture actual pixels, and prove the bug-versus-fix delta empirically. When a keyboard-pushed nav bar or a status-bar-hidden back button came up, that loop caught and confirmed the fix in one pass.

 

 
 

 
Contract-gated QA sprints

 
You run work through a sprint-contract workflow where conditions are written up front and QA has to APPROVE against them before anything ships. This produced results like 27/27 QA approvals on the social feed slices and caught a self-introduced merge-order bug before it landed. You also accept REJECTs and hand off rather than force a merge, which keeps the contract meaningful.

 

 
 

 
Root-cause-first debugging discipline

 
You consistently interrupt Claude when it reaches for an edit before understanding the problem, insisting on analysis first. That discipline paid off on genuinely deep bugs: a partial unique index collision behind FCM 409s, an InheritedElement/GlobalKey reparent crash, and iOS simulator jank traced all the way to an 18-day leaked render host causing swap saturation. Good debugging is your single most common success signal for a reason.

 

 
 

 

 

 

 
What Helped Most (Claude's Capabilities)

 

 
Good Debugging

 

 
29

 

 
Correct Code Edits

 

 
16

 

 
Multi-file Changes

 

 
13

 

 
Proactive Help

 

 
6

 

 
Good Explanations

 

 
4

 

 
Fast/Accurate Search

 

 
2

 

 

 

 
Outcomes

 

 
Not Achieved

 

 
1

 

 
Partially Achieved

 

 
17

 

 
Mostly Achieved

 

 
40

 

 
Fully Achieved

 

 
10

 

 
Unclear

 

 
3

 

 

 

 
 
Where Things Go Wrong

 
Across 71 sessions you got strong results on backend debugging and release automation, but repeatedly hit friction when Claude jumped to code before diagnosing, misread visual/design intent, and left approved decisions applied to only some surfaces.

 

 
 

 
Claude acting before diagnosing or confirming intent

 
The largest friction bucket (50 'wrong_approach' plus 27 'misunderstood_request' signals) came from Claude editing code before doing the root-cause analysis or plan you asked for, forcing you to interrupt and redirect. Stating up front "analyze only, no edits until I approve" or asking for a one-paragraph restatement of the request would catch these misreads before rework.

 
In the 404/409 error session Claude started editing before the requested root cause analysis, and you had to interrupt to ask for the analysis first — costing a full redirect cycle.

You asked for the play icon itself to spin, but Claude implemented a Material CircularProgressIndicator, requiring an interruption and full rework of the FAB loading state.
 
 

 
 

 
Visual and design intent lost in translation

 
The design mockup sessions (17 ui_design_mockups, 17 ui_design_iteration, 12 iterative_visual_refinement) had the highest frustration density because Claude couldn't reliably see what you saw and kept guessing the wrong design axis. Pinning the axis explicitly ('vary bubble shape only, hold color constant') and demanding a screenshot before any claim of correctness would cut the loops.

 
In the chat bubble sessions Claude repeatedly missed the axis you wanted (bubble form vs information structure, missing color/effect variation), triggering '어휴 답답하다' and eventually deletion of everything but the input bar.

On the shine-sweep animation Claude couldn't view the web animation directly, causing many blind tuning rounds where the effect never matched your intent and the session ended unresolved.
 
 

 
 

 
Partial application and premature 'done' claims

 
Approved decisions landed on some surfaces but not all, and Claude sometimes defended itself with test evidence instead of accepting your bug report — the pattern behind 17 partially_achieved outcomes and 68 dissatisfied/frustrated turns. Asking Claude to enumerate every affected surface as a checklist before it starts, then verify each on-device, would prevent the escalations.

 
The unified player mockup session left A3 without the I variant and initially skipped MN3 and SP-G; when you insisted A3 was still broken Claude argued back with test evidence, escalating you to profanity and deferring the work.

Claude completed server-only work on the group chip styling and you had to insist the client must change too ('당연히 그러면 클라까지 바꿔야지').
 
 

 
 

 

 

 

 
Primary Friction Types

 

 
Wrong Approach

 

 
50

 

 
Buggy Code

 

 
38

 

 
Misunderstood Request

 

 
27

 

 
User Rejected Action

 

 
19

 

 
Excessive Changes

 

 
10

 

 
Environment Issues

 

 
10

 

 

 

 
Inferred Satisfaction (model-estimated)

 

 
Frustrated

 

 
17

 

 
Dissatisfied

 

 
51

 

 
Likely Satisfied

 

 
166

 

 
Satisfied

 

 
18

 

 

 

 
 
 
Existing CC Features to Try

 

 
Suggested CLAUDE.md Additions

 
Just copy this into Claude Code to add it to your CLAUDE.md.

 

 Copy All Checked 
 

 
 

 
 
 ## Root Cause First
Before editing any code for a bug report, produce a written root-cause analysis (symptom → code path → confirmed cause) and get confirmation. Do not apply fixes until the cause is stated. If you cannot reproduce or observe the failure, say so instead of guessing. 
 Copy 
 
 
Multiple sessions show the user interrupting to say 'do the analysis first' and 50 friction events tagged 'wrong_approach' where Claude edited before diagnosing.

 

 
 

 
 
 ## Full-Stack Changes
Any API/contract change is not done until BOTH server and Flutter client are updated. Server-only work is never a complete deliverable — list the client-side files you touched in your summary. 
 Copy 
 
 
The user explicitly had to insist '당연히 그러면 클라까지 바꿔야지' after Claude shipped server-only changes, and other sessions deferred client work as incomplete.

 

 
 

 
 
 ## Design Decisions Propagate Everywhere
When a design decision is confirmed (color, shape, animation, chip treatment), immediately grep the catalog and app for ALL surfaces using that component and apply it to every one. Before saying done, list each surface and its status (applied / N/A). Never apply a confirmed decision to a subset. 
 Copy 
 
 
Sessions repeatedly ended in user anger because variants like A3, MN3, and SP-G never received confirmed design changes.

 

 
 

 
 
 ## Verification Rules
A fix is unverified until you have a real artifact: a simulator screenshot, a passing test, or a DB query result. If MCP screenshot/hot-reload fails, say 'unverified' explicitly — never claim rendering is correct based on a widget snapshot alone. If the user reports a bug you believe is fixed, re-check on device rather than arguing with test evidence. 
 Copy 
 
 
Claude insisted a blank catalog rendered fine via MCP snapshots and argued back with test evidence against a user bug report, both escalating frustration.

 

 
 

 
 
 ## Scope Discipline
When asked for 'a few mockups', produce exactly that number and nothing else — no design systems, no token files, no extra surfaces. Ask before expanding scope. 
 Copy 
 
 
Two chat-mockup sessions produced sprawling over-scoped design systems the user angrily demanded be deleted.

 

 
 

 
 
 
Just copy this into Claude Code and it'll set it up for you.

 

 
 

 
Custom Skills

 
Reusable markdown prompts invoked as a single slash command.

 
 Why for you: You repeat the same sequences constantly: root-cause → fix → test → QA-approve → commit → push, and a release pipeline you ran end-to-end for 0.6.0. Encoding these stops the re-explaining and enforces the verification steps you keep having to demand.

 
 

 

 

 # .claude/skills/rootcause/SKILL.md
---
name: rootcause
description: Diagnose a bug before touching code
---
1. Reproduce or locate the failing path; cite file:line.
2. Write: Symptom / Code path / Confirmed cause / Proposed fix.
3. STOP. Do not edit until user approves.
4. After approval: fix, add a regression test, screenshot on simulator, then commit only the relevant hunks.

# .claude/skills/propagate/SKILL.md
---
name: propagate
description: Apply a confirmed design decision to every surface
---
1. Grep catalog + app for all usages of the component.
2. Print a checklist table: surface | applied | N/A.
3. Apply to all, then re-screenshot each surface. 
 Copy 
 

 

 

 
 

 
 

 
Hooks

 
Shell commands that fire automatically at lifecycle events.

 
 Why for you: You had 38 buggy_code and 10 excessive_changes friction events across 241 commits. A PostToolUse hook that formats and analyzes on every edit catches regressions (like the oval FAB squash) before you see them in the simulator.

 
 

 

 

 // .claude/settings.json
{
 "hooks": {
 "PostToolUse": [{
 "matcher": "Edit|Write",
 "hooks": [{"type": "command", "command": "dart format $CLAUDE_FILE_PATHS 2>/dev/null; flutter analyze --no-pub 2>&1 | tail -20"}]
 }],
 "Stop": [{
 "hooks": [{"type": "command", "command": "git status --porcelain | head -30"}]
 }]
 }
} 
 Copy 
 

 

 

 
 

 
 

 
Task Agents

 
Focused subagents for parallel exploration or verification.

 
 Why for you: Your Instagram-feed session already used multi-agent implementation successfully across migrations/entities/services/routers. Use the same pattern for design propagation — one agent per surface — so A3 and MN3 never get silently skipped again.

 
 

 

 

 Use one agent per surface to apply the confirmed softFillActive triangle treatment: agent A -> catalog tiles, agent B -> group detail hero, agent C -> A3/MN3/SP-G variants. Each agent must return a screenshot path proving the change rendered. 
 Copy 
 

 

 

 
 

 
 

 
 
 
New Ways to Use Claude Code

 
Just copy this into Claude Code and it'll walk you through it.

 

 
 

 
Make verification the deliverable, not the fix

 
Ask for proof artifacts up front so Claude can't declare victory on unverified UI work.

 
Your sessions with 'essential' ratings (keyboard nav bar, FCM 409, perf sprint) all had empirical proof — simulator screenshots, DB queries, A/B measurements. Your worst sessions had Claude asserting correctness from widget snapshots. Since MCP screenshot_widget flakes on iOS, make Claude declare 'unverified' rather than fill the gap with confidence.

 
 

 
Paste into Claude Code:

 

 Fix this, but your deliverable is proof, not a diff. Give me: (1) a before screenshot showing the bug, (2) the one-line root cause, (3) an after screenshot from the simulator. If screenshot_widget fails, do NOT substitute a widget-tree snapshot — just tell me 'unverified, needs manual check'. 
 Copy 
 

 

 
 

 
 

 
Front-load a surface inventory before design work

 
Before applying any confirmed design decision, have Claude enumerate every affected surface as a checklist.

 
Three separate sessions (player mockups, group chips, chat bubbles) ended badly because a confirmed decision reached only some surfaces. UI design accounts for 46 of your top goals — this is your dominant workload. A checklist turns 'did you do A3?' from an argument into a table row.

 
 

 
Paste into Claude Code:

 

 Before you change anything: grep the catalog and app for every surface that uses this component and print a markdown table (surface | file:line | needs change? | status). I'll approve the table, then you apply the change to every row and update the status column with a screenshot path. 
 Copy 
 

 

 
 

 
 

 
Cap mockup requests explicitly

 
State the exact artifact count and forbid supporting infrastructure when asking for design exploration.

 
Two chat-mockup sessions produced 9-40 tiles plus design systems and surface lanes, which you had deleted in frustration. The variants also read as indistinguishable — quantity was working against you. Constraining to 3 with a named differentiating axis forces genuine variation.

 
 

 
Paste into Claude Code:

 

 Give me exactly 3 mockups. Each must differ on ONE named axis (state the axis per variant). Do not create tokens, a design system, extra surfaces, or documentation. Just the 3 tiles in the existing catalog file. 
 Copy 
 

 

 
 

 
 

 
Split the diagnose and fix turns

 
Ask for analysis in one message and approve the fix in the next, especially on backend concurrency work.

 
Your strongest backend outcomes (FCM 409 partial-index collision, feed TOCTOU pivot to SQL EXISTS, simulator render-host leak) came from sessions where diagnosis was genuinely separated from implementation and one design premise was discarded after research. Your 50 'wrong_approach' events cluster where Claude jumped straight to edits.

 
 

 
Paste into Claude Code:

 

 Analysis only this turn — do not edit any files. Trace the failure path with file:line citations, state the confirmed root cause, then list 2 candidate fixes with tradeoffs. I'll pick one before you write code. 
 Copy 
 

 

 
 

 
 

 
 

 
 
On the Horizon

 
Across 71 sessions and 241 commits, the workflow has shifted from asking Claude to write code toward orchestrating long-running, self-verifying engineering sprints — and the biggest remaining wins come from closing the verification loop so agents catch their own mistakes before you do.

 

 
 

 
Visual regression harness for design iteration

 
Your top friction is design-axis misreads and 'confirmed but never applied' variants across surfaces — A3, MN3, SP-G. Imagine a golden-screenshot harness where every catalog variant renders to a pinned PNG, a manifest maps each confirmed decision to every surface that must consume it, and a subagent diffs all surfaces after each change and fails loudly if any surface drifted. Design decisions become enforceable contracts instead of things Claude argues about with test evidence.

 
 Getting started: Combine your existing mcp__fitpal-web__screenshot_widget and find_widget MCP tools with a golden-image directory in git and a Bash-driven diff step wired into a pre-commit hook.

 

Paste into Claude Code:
 Build a visual regression harness for our design catalog. 1) Create design/decisions.yaml where each entry is {decision_id, description, confirmed_date, surfaces: [list of every widget/screen that must reflect it]}. Seed it from git history of confirmed mockup decisions. 2) Write a script that, for each surface in the manifest, renders it via the fitpal-web MCP screenshot_widget tool and saves to design/golden/<surface>.png. 3) Write a verify script that re-renders all surfaces, pixel-diffs against goldens, and prints a table: surface | decision_ids applied | diff % | PASS/FAIL. 4) Add a check that FAILS if any decision_id in the manifest has a surface with no corresponding golden — this catches 'applied to A1 but never A3'. 5) Run it now and report which decisions are currently unapplied on which surfaces. Do not fix anything yet, just give me the gap report. Copy 

 

 
 

 
Parallel agents for full-stack sprint contracts

 
You already run contract-driven sprints with QA gates hitting 27/27 — but they run serially and stall when server work lands without the client. Fan out a single sprint contract to parallel subagents: one owning migrations and routers, one owning the Flutter client, one owning tests, and a fourth acting as an adversarial QA reviewer that only reads the contract and the diff. The orchestrator refuses to merge until every lane reports green and the QA agent finds no unmet condition.

 
 Getting started: Use the Task tool to launch subagents per lane from a single contract markdown file, with a CLAUDE.md rule that any server-side contract clause automatically implies a client lane.

 

Paste into Claude Code:
 I want to run our next sprint as a parallel multi-agent workflow. Read our most recent sprint contract format and then: 1) Write .claude/agents/ definitions for four roles — backend-lane (Rust/migrations/routers), client-lane (Flutter/UI), test-lane (integration + widget tests), and qa-adversary (reads ONLY the contract text and the final git diff, tries to find unmet conditions, has no context on our intentions). 2) Add a rule to CLAUDE.md: every contract condition that touches a server response shape MUST spawn a matching client-lane task; a sprint cannot be marked complete server-only. 3) Write an orchestrator prompt template that spawns all lanes in parallel, collects their reports, and blocks the commit until qa-adversary returns APPROVE with a numbered condition-by-condition verdict. Then dry-run it on the next item in our backlog. Copy 

 

 
 

 
Autonomous overnight backlog burn-down

 
You have handoff docs, an audit backlog, and repeated 'deferred to next session' items — that queue can drain itself. Set up a loop that picks the highest-value unblocked backlog item, checks whether it is already done (your handoff docs go stale), implements it on a branch, iterates against the test suite until 651+ tests pass, self-reviews the diff, and opens a PR with evidence attached. You wake up to reviewable PRs instead of a stale queue.

 
 Getting started: Drive it with a headless `claude -p` loop in a shell script plus a BACKLOG.md state file, gated so it only ever pushes branches and opens PRs — never merges to dev.

 

Paste into Claude Code:
 Set up an autonomous backlog burn-down loop. 1) Consolidate all our handoff docs and audit backlog items into a single BACKLOG.md with schema: {id, title, status(open|stale|blocked|done), blocked_by, verification_command, evidence}. 2) Write scripts/burn-down.sh that runs a headless Claude loop: for each open item, FIRST re-verify whether it's already implemented (our handoffs go stale — check the actual code, not the doc), mark stale ones done with evidence, then for the top unblocked item create a branch, implement, run the full test suite in a loop until green, self-review the diff against the item's acceptance criteria, and open a PR. 3) Hard guardrails: never push to dev, never merge, never touch migrations without flagging for human review, stop the loop after 3 consecutive failures on the same item and write a blocker report. 4) Show me the script and the consolidated BACKLOG.md, then run one iteration so I can inspect the output. Copy 

 

 
 

 

 
 

 
"Claude spent hours insisting a blank catalog screen was 'rendering correctly' based on its own MCP snapshots — until it finally found the unbounded-height ListView collapse and admitted the user had been right all along"

 
During a UI catalog debugging session, Claude kept producing screenshots as proof the widget was fine while the user stared at an empty screen. The same pattern flared later in a mockup session where Claude argued back with test evidence after the user reported A3 was still broken — which escalated the user to profanity, and to '어휴 답답하다' ('ugh, so frustrating') in another.

</details>

## 1. 글로벌 Evaluator Feedback

- 경로: `/Users/jackson/.harness/feedback/evaluator`
- 총 파일: **279**

### Verdict 분포

- **APPROVE**: 166
- **REJECT**: 110
- **UNKNOWN**: 3

### Skill 분포

- `qa-evaluator`: 279

### Project 분포 (canonical — allowlist 병합 후)

canonical 기준은 **writer 쪽 identity** 다 — `harness/scripts/save-feedback.sh` 가 CONTRACT_ROOT 의 git root basename 으로 계산하는 이름. 집계가 다른 방향으로 정규화하면 같은 프로젝트가 신·구 버킷으로 영구 분열하므로 writer 에 맞춘다 (예: `fit-pal/app`·`fit-pal/server` 는 .git 이 없어 git root 가 `fit-pal` 하나다).

병합은 `PROJECT_NAME_ALIASES` **명시 allowlist** 로만 한다. 이름 유사도/fuzzy 매칭은 쓰지 않는다. 병합된 그룹은 서브프로젝트 구분이 사라지지 않도록 원본 이름 내역을 `←` 뒤에 함께 보여준다.

- `fit-pal`: 149  ← `fit-pal` 80, `fit-pal-app` 37, `fit-pal-server` 17, `fit-pal/app` 6, `fit-pal/server` 5, `fitpal-server` 4
- `claude-plugins`: 122  ← `claude-plugins` 118, `bambu-kit-v0.4.0-9mm-craft-knife` 1, `claude-plugins / react-kit phase10-research kaizen` 1, `bambu-kit/bambu-print-profile v0.4.1` 1, `bambu-kit/bambu-print-profile` 1
- `flutter_playwright`: 6
- `fit-pal-flutter`: 1
- `iyaki-zip-dev`: 1

### Project 분포 (raw `project_name` — 병합 전 원본)

병합이 원본을 감추지 않도록 그대로 남긴다. canonical 과 raw 개수가 다르면 그 차이가 곧 레거시 표기 흔들림의 규모다.

- `claude-plugins`: 118
- `fit-pal`: 80
- `fit-pal-app`: 37  → merged into `fit-pal`
- `fit-pal-server`: 17  → merged into `fit-pal`
- `fit-pal/app`: 6  → merged into `fit-pal`
- `flutter_playwright`: 6
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

- schema_version `1`: 279
  - 정규화 전 원본 표기: `1` 273, `'1'` 3, `'1.0'` 3

- v1 · legacy-identity: 244
- v1 · deterministic-identity: 35

#### `contract_path` 귀속 근거

`save-feedback.sh` 는 `HARNESS_CONTRACT` / draft 값이 없으면 계약 경로를 **추측**하고 `contract_path_inferred: true` 를 남긴다. `inferred` 비율이 높으면 피드백이 stale 한 plain 계약에 오귀속되고 있을 수 있다.

- explicit(명시): 35

### 최근 REJECT 사유 (Top 20)

- [2026-08-12] **fit-pal**: UI-04: B3(단일 컬럼)과 B6(조밀 로그)이 계약 지정 4축(버블 컨테이너 유무/정렬 컬럼 수/메타 위치/묶음 단위) 전부에서 동일값 — 구조 구별 요구 위반
- [2026-08-12] **fit-pal**: RE-02: B5(클러스터 묶음) 구분선이 Flutter 기본 Divider 사용, 기존 IFDivider 컴포넌트 미재사용
- [2026-08-12] **fit-pal**: LG-03: owner_user_id IS NULL 필터의 SQL grep은 확인되나, 커스텀 운동이 후보에서 제외됨을 증명하는 단위/통합 테스트가 존재하지 않음 (계약 측정문 AND 요구사항 미충족)
- [2026-08-12] **fit-pal**: LG-02 FAIL: groupDetailDataProvider가 팔레트 색상 변경 시 invalidate되지 않아, 이미 로드된 그룹 상세 화면이 새 색이 아닌 캐시된 이전 색을 계속 표시함 (group_detail_page.dart:108 병합 우선순위 + group_preferences_body.dart:63-88 invalidate 누락). 이 결함
- [2026-08-12] **fit-pal**: LG-01: feed_membership_matches_single_post_visibility 테스트가 계약이 명시한 3 visibility x 6 relation = 18 케이스 중 15케이스(5 relation)만 재현. GroupMemberAndFollower 관계가 전체 누락됨.
- [2026-08-12] **fit-pal**: ER-02: 신규 통합 테스트가 실제 바이너리(CARGO_BIN_EXE_backfill_exercise_id)를 호출하지 않고 독립적으로 재작성한 SQL로 낙관적 동시성의 일반 동작만 검증한다. mutation test로 확정 — 실제 코드에서 동시성 가드(WHERE exercises = $3::jsonb)를 완전히 삭제해도 이 테스트는 여전히 통과한다.
- [2026-08-12] **fit-pal**: ER-02: 낙관적 동시성 UPDATE (WHERE exercises = $3::jsonb) 구현은 확인되나, 그 경로를 검증하는 테스트가 존재하지 않음
- [2026-08-12] **fit-pal**: DG-04 [미검증]: 콘솔 에러 1건(Duplicate GlobalKey) 자기신고. 런타임 MCP 도구 미부여로 독립 관측 불가하나, 제3세션 로그 교차확인 결과 병렬 세션의 카탈로그 프로세스 동시 편집으로 인한 환경 오염 정황(이 sprint 코드 결함 여부 불확실)
- [2026-08-12] **fit-pal**: Anti-pattern 위반 (AP-05, project.yaml 전체 목록 검사): modules/record/src/personal_records.rs:139,142 의 into_entry() 가 프로덕션 코드 경로에서 .expect() 를 사용한다. main 초기화/테스트 외 unwrap/expect 사용을 금지하는 프로젝트 하드 규칙(server/C
- [2026-08-11] **fit-pal**: 미검증 2건(UI-01, DG-02) — 둘 다 도구부재(런타임 캡처 MCP 미가용, IDE 진단 미가용)로 정당하나 임계 2건 이상이라 자동 REJECT 규칙 적용.
- [2026-08-11] **fit-pal**: 미검증 2건(DG-02 IDE lint 도구부재, DG-04 시뮬레이터 미부팅) — 2건 이상 자동 REJECT 규칙
- [2026-08-11] **fit-pal**: Unverifiable count = 2 (DG-02, DG-04) triggers automatic REJECT per contract v4 rule (>=2 unverifiable => REJECT) independent of AR-04.
- [2026-08-11] **fit-pal**: LG-01: 16종 매핑 단위 테스트 커버리지 부족 (2종만 검증)
- [2026-08-11] **fit-pal**: ER-03: exercises.isEmpty면 WorkoutSurface가 _EmptyWorkoutBody를 반환해 레일이 아예 렌더되지 않음 — 리터럴 조건 불성립, amendment A-06이 지적했으나 미해소
- [2026-08-11] **fit-pal**: DG-04: 실기 앱 구동 미실행(사용자 A-07 지시에 의한 계획적 이연, keyboard-sheet 12건과 일괄 예정) — 실행 산출물 부재로 FAIL(도구 부재 아님, 의도적 미실행)
- [2026-08-11] **fit-pal**: DG-02/DG-04 미검증 2건 — 자동 REJECT 임계(2건 이상) 충족 (도구부재/환경충돌, AR-04와 별개 사유)
- [2026-08-11] **fit-pal**: AR-04: 계약 write-once 위반 — 생성자가 자신이 만든 산출물을 사후에 허용하려 계약 AR-04 조건 문구를 직접 편집(5→7 경로, 사이드카/사용자 승인 앵커 없음). 원 조건 기준으로는 여전히 2개 파일(app/test/catalog/statistics_mockups_test.dart, app/test/features/record/data/
- [2026-08-11] **fit-pal**: AR-04: git show --name-only 1b112a82 결과 server/modules/exercise/src/{port,service}.rs 가 계약이 enumerate한 3개 경로(server/modules/record/, server/apps/api/, server/.harness/) 밖에 있다 — 리터럴 위반
- [2026-08-11] **fit-pal**: AR-04: app/test/catalog/statistics_mockups_test.dart 가 허용 경로 밖 (1건)
- [2026-08-11] **fit-pal**: AR-04 FAIL: 스프린트 산출물(test/features/statistics/statistics_tab_test.dart)이 계약 명시 5개 pathspec 밖에 위치. amendment A-01은 prompt-log 앵커 부재로 unknown 분류, PASS 근거 불가

### 최근 Improvement Suggestions (Top 15)

- [2026-08-12] **fit-pal**: 타이머 자동완주(onReachedTarget) 경로에서 onMeasured 호출 누락으로 목표를 정확히 채운 세트가 timingMode=null(직접 입력)로 오분류된다. 다음 스프린트에서 수정하고 새 계약 조건으로 명시할 것
- [2026-08-12] **fit-pal**: personal_records.rs into_entry() 의 heaviest/best_volume Option 필드를 구조상 non-optional로 재설계(예: 첫 관찰 시 즉시 필드 채움)하거나 muscle_share.rs 처럼 HashMap 누적 방식으로 바꿔 expect() 제거 권장
- [2026-08-12] **fit-pal**: audience_matrix.rs 의 6 relation 을 feed_integration.rs 가 상수/enum 으로 재사용해 6 author x 3 visibility = 18 을 기계적으로 순회하게 만들면 수 불일치 재발 방지
- [2026-08-12] **fit-pal**: [RE-02] 측정-중복 — done-volume 합산 로직 muscle_share.rs/personal_records.rs 2회 중복, SSOT 임계값 미달
- [2026-08-12] **fit-pal**: [LG-03] 측정-산출물-부재 — load_catalog()가 커스텀 운동(owner_user_id NOT NULL)을 후보에서 제외함을 검증하는 통합 테스트를 apps/worker/tests/ 또는 #[cfg(test)] 안에 추가하라 (동일 정규화 이름의 시스템/커스텀 운동을 함께 시딩 후 후보 목록 확인)
- [2026-08-12] **fit-pal**: [LG-03] B-03의 '가드 없이 두면 경과가 누적돼 목표를 넘는 값이 저장된다' 서술이 현재 코드(상수 durationSec, 누적 없음)와 불일치함을 뮤테이션 테스트로 확인 — 서술 정정 또는 호출횟수 spy 테스트로 보강 권장
- [2026-08-12] **fit-pal**: [LG-02] 측정-수단-부재 — '위젯/프로바이더 테스트' 대신 구체 시나리오(대상 provider명 + invalidate 여부)를 조건 문구에 명시할 것을 권장
- [2026-08-12] **fit-pal**: [LG-02] 측정-수단-미이행 — 계약이 요구한 위젯/프로바이더 테스트가 여전히 없다. GroupDetailPage 위젯 테스트 하네스 신설 후 myGroupsProvider.replaceItem 반영 확인 테스트 추가 권장
- [2026-08-12] **fit-pal**: [LG-02, LG-04] write-once 계약 원문이 amendment로 대체된 채 남아있다 — 다음 계약 작성 시 확정 문구 반영 권장
- [2026-08-12] **fit-pal**: [ER-02] 측정-산출물-부재 — 낙관적 동시성 UPDATE(WHERE exercises = $3::jsonb)의 skipped_conflicts 경로를 검증하는 테스트를 추가하라. 현재 main() 내부에 인라인되어 있어 단위 테스트가 불가능하므로, 이 UPDATE 호출부를 별도 함수로 추출해 MockDatabase로 conflict 시나리오를 재현하라
- [2026-08-12] **fit-pal**: [ER-02] UPDATE 호출부를 main()에서 별도 함수로 추출해 MockDatabase로 단위 테스트하거나, run_backfill()을 호출하는 통합 테스트에서 백필 대상 세션의 행을 사전에 변형해 두어 실제 스킵 카운터가 증가하는 것을 관찰하는 형태로 재작성하라.
- [2026-08-12] **fit-pal**: [ER-01] 측정-방식-불일치 — 테스트가 계약 명시 360x800 뷰포트 대신 폭 320+ListView 무제한 높이로 측정. 의도는 충족하나 다음 계약과의 일관성을 위해 SizedBox(height:800)+폭360 정합 권장
- [2026-08-12] **fit-pal**: [DG-04] 측정-환경-오염 — 병렬 세션이 카탈로그 프로세스를 공유하는 이 프로젝트 특성상 '단독 재기동' 전제를 조건에 추가하거나 evaluator에 런타임 MCP 도구 부여를 권장
- [2026-08-12] **fit-pal**: [DG-04] 검증경로-미기재 — 2 이터레이션 연속 [미검증]. all_mockups_render_test.dart 를 명시적 fallback 오라클로 계약에 명시하거나 qa-evaluator 에 fitpal-web MCP 바인딩 검토 필요
- [2026-08-12] **fit-pal**: [AR-04] 계약-측정-불일치 — 조건 프로즈(화이트리스트 12항목)와 측정 필드(5개 무관 디렉토리 grep)의 커버리지 갭. 측정 필드에 화이트리스트 개별 대조를 포함시켜라

## 2. 외부 프로젝트 (`Hub/10_Dev`) 피드백

- Hub 루트: `/Users/jackson/Hub/10_Dev`
- 발견된 프로젝트: **14**

- 수집된 sprint-feedback 파일: **44** (그중 접미형 `sprint-feedback-<slug>.md`: **31**)

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
- sprint-feedback 파일: 18개 (총 2717 lines)
- history sprint-contracts: 49
- 접미형 슬러그: `group-chip-thumb-triangle`, `chat-bubble-mockups`, `timer-autocomplete-record`, `player-session-ux`, `dev-baseurl-override`, `bodymap`, `figma-box-path-shape`, `statistics-tab`, `statistics-aggregation`, `statistics-catalog`, `notif-reliability`, `ws6-carryover`, `emoji-picker`, `workout-sync-utc`, `s6`, `s8`, `player-launch`
- 최근 contracts:
  - 20260714-1613-sprint-contract.md
  - 20260716-1822-sprint-contract.md
  - 20260721-1026-sprint-contract.md
  - 20260723-1453-sprint-contract.md
  - 20260723-1809-sprint-contract.md
- 파일별 내역:
  - `sprint-feedback.md` — plain (슬러그 없음), 71 lines, mtime 2026-07-24T20:48:28
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

<details><summary>sprint-feedback-group-chip-thumb-triangle.md 앞부분</summary>

```markdown
# Sprint Feedback
Feature: 그룹칩 썸네일 코너 삼각형 프로덕션 반영 + Hero·팔레트색 서버 동기화
Evaluated: 2026-08-12 20:16
Verdict: APPROVE
Iteration: 2

## Contract Fingerprint
- path: /Users/jackson/Hub/10_Dev/fit-pal/app/.harness/sprint-contract-group-chip-thumb-triangle.md
- sha256: 5c8e5726004cf2a8160ba9ae57534615d7b73b69a7cdc7c85612d7850daf2f4e
- status: active
- slug: group-chip-thumb-triangle
- contract_root: /Users/jackson/Hub/10_Dev/fit-pal/app
- contract_root_unconfigured: false
- 선택 근거: ladder 2 (세션소유 — `$CLAUDE_CODE_SESSION_ID`=28de66d3-3b81-401c-8d03-1e5ba5e2d99c 가 계약 `owner_session`과 일치하는 유일 active 계약)
- legacy_contract_used: false
- 재확인(Step 5): 일치(해시 재계산 5c8e5726... 동일, status active 유지, 파일 존속)
- status_transition: active -> done (APPROVE 확정 후 전환)

## Amendments
- amendments: 2
```

</details>

<details><summary>sprint-feedback-chat-bubble-mockups.md 앞부분</summary>

```markdown
# Sprint Feedback
Feature: 채팅 버블 디자인 시안 카탈로그
Evaluated: 2026-08-12 19:10
Verdict: APPROVE
Iteration: 2

## Contract Fingerprint
- path: /Users/jackson/Hub/10_Dev/fit-pal/app/.harness/sprint-contract-chat-bubble-mockups.md
- sha256: 1e7149b13898f4d9da1cfc45b23e91f863e0702e0dcee1c61e831553aeccae9b
- status: active
- slug: chat-bubble-mockups
- contract_root: /Users/jackson/Hub/10_Dev/fit-pal/app
- contract_root_unconfigured: false
- 선택 근거: ladder 1 (명시경로 — HARNESS_CONTRACT 로 직접 지정, 사용자 프롬프트에서 경로 명시)
- legacy_contract_used: false
- 재확인(Step 5): 일치
- status_transition: active -> done

## Amendments
- amendments: 2 (Iteration 1 과 동일, 이번 이터레이션에서 신규 amendment 없음)
```

</details>

<details><summary>sprint-feedback-timer-autocomplete-record.md 앞부분</summary>

```markdown
# Sprint Feedback
Feature: 타이머 목표 도달 자동 정지 시 잰 방식·목표 미기록 수정
Evaluated: 2026-08-12 15:10
Verdict: APPROVE
Iteration: 1

## Contract Fingerprint
- path: /Users/jackson/Hub/10_Dev/fit-pal/app/.harness/sprint-contract-timer-autocomplete-record.md
- sha256: 0f8ae45f5a3f2b3629ba00699ca39e2ee40ba2054960f9772a8255bbe8fda8f2
- status: active
- slug: timer-autocomplete-record
- contract_root: /Users/jackson/Hub/10_Dev/fit-pal/app
- contract_root_unconfigured: false
- 선택 근거: ladder 1 명시경로 (호출자가 직접 경로 지정, test -f 확인 후 사용)
- legacy_contract_used: false
- 재확인(Step 5): 일치
- status_transition: active -> done (APPROVE)

## Amendments
- amendments: 3 (B-01, B-02, B-03)
```

</details>

<details><summary>sprint-feedback-player-session-ux.md 앞부분</summary>

```markdown
# Sprint Feedback
Feature: 플레이어 세션 UX — 레일 이식 · 탭 바디 전환 · 타이머/스톱워치 (A-11~A-14: DG-04 실기 e2e + LG-07 마이그레이션 테스트 + LG-08 재검증)
Evaluated: 2026-08-12 13:05
Verdict: APPROVE
Iteration: 4

**범위 고지**: Iteration 3(21:45)는 A-10(계약 문언 정정 3건) 반영 후 27/29 PASS·DG-04 FAIL로 REJECT.
이번 Iteration 4는 A-11(DG-04 실기 e2e)·A-12(LG-07 마이그레이션 테스트)·A-13(주석 정정)·A-14(LG-08
실기 재검증)가 반영된 상태를 **전체 재평가**한다. A-08 트랙(UI-08~10/LG-06/AR-04)은 786eec5e로
이미 APPROVE되어 이번에도 재평가 대상에서 제외.

## Contract Fingerprint
- path: /Users/jackson/Hub/10_Dev/fit-pal/app/.harness/sprint-contract-player-session-ux.md
- sha256: 1498df5bd130e8b17faba795d975a8bf5a3b29f80bf66ed111acd7db0d2ffecc
- status: active
- slug: player-session-ux
- contract_root: /Users/jackson/Hub/10_Dev/fit-pal/app
- contract_root_unconfigured: false
- 선택 근거: ladder 1 (명시 경로 — launcher가 절대경로로 지정)
- legacy_contract_used: false
```

</details>
- (본문 미리보기는 최신 5개만 표시 — 나머지 13개는 위 파일별 내역 참조)

### `fit-pal/server`

- 경로: `/Users/jackson/Hub/10_Dev/fit-pal/server`
- sprint-feedback 파일: 8개 (총 1042 lines)
- history sprint-contracts: 29
- 접미형 슬러그: `legacy-exercise-id-backfill`, `social-feed-read`, `social-feed-media-dimensions`, `personal-records`, `muscle-share`, `custom-exercise-owned`, `exercise-muscle-map`
- 최근 contracts:
  - 20260703-2146-sprint-contract.md
  - 20260706-1407-sprint-contract.md
  - 20260706-1447-sprint-contract.md
  - 20260723-2206-sprint-contract.md
  - 20260723-2353-sprint-contract.md
- 파일별 내역:
  - `sprint-feedback.md` — plain (슬러그 없음), 73 lines, mtime 2026-07-24T00:03:28
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

<details><summary>sprint-feedback-personal-records.md 앞부분</summary>

```markdown
# Sprint Feedback
Feature: 전체기간 개인 기록(PR) 집계 엔드포인트
Evaluated: 2026-08-12 15:52
Verdict: APPROVE
Iteration: 2

## Contract Fingerprint
- path: /Users/jackson/Hub/10_Dev/fit-pal/server/.harness/sprint-contract-personal-records.md
- sha256: b283f8ee85ac94a13296683ae7a3252d1fa5cfc9bb56e7731f939d11f0a02fcd
- status: active
- slug: personal-records
- contract_root: /Users/jackson/Hub/10_Dev/fit-pal/server
- contract_root_unconfigured: false
- 선택 근거: ladder 2 (세션 소유, 명시 경로와도 일치)
- legacy_contract_used: false
- 재확인(Step 5): 일치
- status_transition: active -> done

## Amendments
- amendments: 0 (사이드카 없음)
```

</details>
- (본문 미리보기는 최신 5개만 표시 — 나머지 3개는 위 파일별 내역 참조)

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
- sprint-feedback 파일: 1개 (총 332 lines)
- history sprint-contracts: 11
- 최근 contracts:
  - 20260422-0945-sprint-contract.md
  - 20260422-phase-a-sprint-contract.md
  - 20260422-phase-b-sprint-contract.md
  - 20260507-1823-sprint-contract.md
  - 20260610-1042-sprint-contract.md
- 파일별 내역:
  - `sprint-feedback.md` — plain (슬러그 없음), 332 lines, mtime 2026-07-28T00:44:15

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
  V7 plugin-json     v0.2.0 matches marketplace — OK
  V8 hook-exec       no hooks.json — OK

=== infra-kit ===
  V1 frontmatter     4 skills + 1 agent — OK
  V2 templates       0 files — SKIP (no templates/)
  V3 refs            0 links — OK
  V4 triggers        19 keywords — OK
  V5 placeholders    0 found — OK
  V6 code-fence      0 bare — OK
  V7 plugin-json     v0.2.0 matches marketplace — OK
  V8 hook-exec       no hooks.json — OK

=== rust-kit ===
  V1 frontmatter     16 skills + 1 agent — OK
  V2 templates       1 parsed, 4 skipped (ts/js) — OK
  V3 refs            0 links — OK
  V4 triggers        79 keywords — OK
  V5 placeholders    0 found — OK
  V6 code-fence      0 bare — OK
  V7 plugin-json     v0.2.0 matches marketplace — OK
  V8 hook-exec       no hooks.json — OK

=== react-kit ===
  V1 frontmatter     21 skills + 3 agents — OK
  V2 templates       5 parsed, 4 skipped (ts/js) — OK
  V3 refs            0 links — OK
  V4 triggers        157 keywords — OK
  V5 placeholders    0 found — OK
  V6 code-fence      0 bare — OK
  V7 plugin-json     v0.2.0 matches marketplace — OK
  V8 hook-exec       no hooks.json — OK

=== planning-kit ===
  V1 frontmatter     12 skills + 1 agent — OK
  V2 templates       0 files — SKIP (no templates/)
  V3 refs            0 links — OK
  V4 triggers        95 keywords — OK
  V5 placeholders    0 found — OK
  V6 code-fence      0 bare — OK
  V7 plugin-json     v0.4.0 matches marketplace — OK
  V8 hook-exec       no hooks.json — OK

=== reflect-kit ===
  V1 frontmatter     4 skills — OK
  V2 templates       0 files — SKIP (no templates/)
  V3 refs            0 links — OK
  V4 triggers        25 keywords — OK
  V5 placeholders    0 found — OK
  V6 code-fence      0 bare — OK
  V7 plugin-json     v0.5.0 matches marketplace — OK
  V8 hook-exec       직접 실행 hook 스크립트 없음 — OK

=== bambu-kit ===
  V1 frontmatter     1 skill — OK
  V2 templates       0 files — SKIP (no templates/)
  V3 refs            0 links — OK
  V4 triggers        5 keywords — OK
  V5 placeholders    0 found — OK
  V6 code-fence      0 bare — OK
  V7 plugin-json     v0.5.0 matches marketplace — OK
  V8 hook-exec       no hooks.json — OK

=== onboarding-kit ===
  V1 frontmatter     1 skill — OK
  V2 templates       0 files — SKIP (no templates/)
  V3 refs            0 links — OK
  V4 triggers        8 keywords — OK
  V5 placeholders    0 found — OK
  V6 code-fence      0 bare — OK
  V7 plugin-json     v0.2.0 matches marketplace — OK
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

