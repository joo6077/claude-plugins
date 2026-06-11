# Kaizen Data Pool

Generated: 2026-06-11T15:30:25
Generator: `scripts/collect-kaizen-data.py`

카이젠 오케스트레이션의 Phase 별 서브에이전트가 참조할 통합 데이터 풀이다. 이 파일은 `scripts/collect-kaizen-data.py` 로 재생성된다 — 수동 수정 금지.

## 0. `/insights` Report (외부 도구 산출물)

- 경로: `/Users/jackson/.claude/usage-data/report.html` · HTML 추출 텍스트
- 최근 갱신: 2026-06-04T20:18:49 (6일 전)
- 모든 Phase 서브에이전트가 **최우선** 참조해야 한다 (Friction Points / Recommended Patterns / Feature Suggestions / 이번 사이클 신규 워크플로우 제안)

<details><summary>insights report 본문 (auto-extracted)</summary>

Claude Code Insights 
 

 
 
 
 

 
Claude Code Insights

 
1,855 messages across 168 sessions (681 total) | 2026-04-25 to 2026-06-04

 
 

 
At a Glance

 

 
 What's working: You run a disciplined, contract-driven workflow—structuring feature work around Sprint Contracts with QA gates and full test suites before committing. You also push past surface fixes to root causes, tracing things like an autoDispose race in a search provider and an enum/int mismatch in Bluetooth scan range, then validating with real scenarios before shipping. You're not just coding either; you extend your own infrastructure by building and releasing MCP tooling and verifying features on real devices. Impressive Things You Did → 

 
 What's hindering you: On Claude's side, the recurring issue is misreading the abstraction level or scope of your requests—defaulting to more complex solutions, reintroducing patterns you'd explicitly banned (like ValueNotifier/useState), and occasionally over-exploring before acting. On your side, requests sometimes leave the desired pattern or target location implicit, so Claude guesses at architecture and gets corrected mid-flight; tooling capabilities (like simulator tap support) also weren't verified early, leading to stalls and handoffs. Where Things Go Wrong → 

 
 Quick wins to try: Pin your hard architectural rules—no ValueNotifier, plain functions over widgets, useMemoized over useState, full-path-vs-filename separation—into a persistent CLAUDE.md or skill so Claude honors them without re-prompting. Lean on your custom skills for repeat workflows, but require Claude to show evidence it actually invoked a skill rather than trusting its claim. For larger refactors, have Claude propose the target file and abstraction and get your sign-off before it writes anything. Features to Try → 

 
 Ambitious workflows: The simulator verification gap that keeps forcing handoffs is the clearest target: as models improve, expect an agent that launches the app, drives the UI via MCP, diffs against expected states, and only commits once end-to-end behavior passes—turning your 'mostly achieved' sprints into fully autonomous green-to-commit cycles. Your accumulated feedback could also become a self-enforcing guardrail layer that loads prior corrections and self-audits diffs against your rules before showing you anything. And your print-profile pipeline could shift to parallel agents that batch-crawl, run tolerance loops, and assemble bundles at once, so a slow crawl never blocks you. On the Horizon → 

 

 

 

 
 What You Work On 
 How You Use CC 
 Impressive Things 
 Where Things Go Wrong 
 Features to Try 
 New Usage Patterns 
 On the Horizon 
 Team Feedback 
 

 

 

1,855

Messages

 

+59,287/-7,260

Lines

 

979

Files

 

24

Days

 

77.3

Msgs/Day

 

 
 
What You Work On

 

 
 

 

 Flutter Kiosk App Development 
 ~28 sessions 
 

 
Extensive work on a Flutter-based kiosk application including preset screens, video/language card sections, OLKP import/export logic, firmware path handling, and Bluetooth scan range fixes. Claude implemented features following existing project patterns with contract-driven workflows, codegen, and analyzer validation. Recurring friction arose from Claude introducing unwanted ValueNotifier/useState patterns and misreading desired abstraction levels during refactors.

 

 
 

 

 MCP Server & Flutter Tooling Integration 
 ~10 sessions 
 

 
Development and release of a flutter-playwright MCP server, including DTD-based VM service discovery, hot-restart reconnection fixes, and wrapper script debugging. Claude researched via Codex, implemented solutions with full QA, and shipped multiple releases (v0.7.3, v0.8.0). Tooling limitations like lack of tap support and lost VM connections blocked end-to-end simulator verification, requiring handoffs.

 

 
 

 

 Schedule-Vote & Group Features (Server + App) 
 ~12 sessions 
 

 
Sprint-based development of schedule-voting features, group-invite buttons, and inline search functionality across server and app layers using contract-driven TDD. Claude completed entities, models, datasources, and automated tests with QA approval and clean commits. Work involved diagnosing autoDispose race conditions and redesigning toward unified multi-group schedule endpoints.

 

 
 

 

 3D Print Profile Generation 
 ~10 sessions 
 

 
Using a custom skill to generate Bambu print profiles from MakerWorld model URLs, including crawling models, clarifying material choices, and tuning tolerance values like xy_hole_compensation for bearing fits. Several sessions were interrupted during the web-crawling step before completion. Successful sessions produced validated, importable profile bundles.

 

 
 

 

 Canvas/UI Layout & Visualization Refinement 
 ~8 sessions 
 

 
Iterative refinement of carousel cards, anchor ports, card spacing, hover animations, and center-grow behaviors per Figma designs. Claude handled multi-file changes with passing test suites but encountered regressions from center-anchored sprite refactors that required multi-commit reverts. Overflow and token-axis issues were caught and fixed within sessions.

 

 
 

 

 

 

 
What You Wanted

 

 
Feature Implementation

 

 
37

 

 
Code Explanation

 

 
20

 

 
Bug Fix

 

 
17

 

 
Debugging

 

 
14

 

 
Code Modification

 

 
13

 

 
Generate Print Profile

 

 
10

 

 

 

 
Top Tools Used

 

 
Bash

 

 
5028

 

 
Read

 

 
2311

 

 
Edit

 

 
2167

 

 
Write

 

 
485

 

 
TodoWrite

 

 
410

 

 
AskUserQuestion

 

 
275

 

 

 

 

 

 
Languages

 

 
Markdown

 

 
931

 

 
Rust

 

 
468

 

 
JSON

 

 
210

 

 
TypeScript

 

 
194

 

 
YAML

 

 
134

 

 
Python

 

 
19

 

 

 

 
Session Types

 

 
Multi Task

 

 
29

 

 
Single Task

 

 
26

 

 
Iterative Refinement

 

 
24

 

 
Quick Question

 

 
3

 

 
Exploration

 

 
1

 

 
Undefined

 

 
1

 

 

 

 
 
How You Use Claude Code

 

 
You operate primarily as an autonomous-execution driver who hands Claude substantial multi-step tasks and expects them carried through end-to-end—sprint validation pipelines, contract-driven TDD workflows, full MCP release cycles, and multi-file refactors. Your tooling profile reflects this: an enormous Bash count (5028) alongside heavy Read/Edit usage shows you let Claude run real verification loops (tests, QA, codegen, commits) rather than just generating snippets. You frequently invoke custom skills and structured workflows (Sprint Contracts, work-summary skills, print-profile generation), indicating you've invested in scaffolding repeatable processes and expect Claude to respect their rules precisely. When Claude claims work it didn't actually do—like saying it invoked /insights when it only read a file, or outputting markdown when a skill forbade it—you catch and correct it immediately.

Despite the autonomy you grant, you're a hands-on course-corrector who interrupts decisively when Claude drifts. The friction data is telling: 53 'wrong_approach' and 38 'misunderstood_request' incidents, plus repeated interruptions during exploration phases (Figma metadata spelunking, drawn-out web crawling for print profiles). You don't tolerate over-engineering—your most frustrated moments (including profanity) came when Claude repeatedly reintroduced ValueNotifier/useState patterns you'd explicitly banned, or extracted code as a widget when you wanted plain functions. You have strong, specific architectural opinions and reject proposed file locations and abstraction levels until they match your intent (the toolbar refactor went through multiple rejected location proposals before settling on 'option C').

Your iteration style is tight and feedback-driven rather than spec-heavy upfront: you'll launch a task, watch Claude work, then redirect with terse corrections ('니가 띄워야지') and let it retry. You expect Claude to enforce your prior feedback as durable rules , not re-litigate them each session—frustration spiked when earlier-stated constraints weren't auto-applied. Outcomes skew strongly positive (66 of 84 fully or mostly achieved), and you're most satisfied when Claude self-diagnoses root causes (the autoDispose race, enum/int mismatch) and ships with passing QA, but recurring friction comes from Claude's tendency to over-complicate simple requests and the hard ceiling of simulator/MCP tooling limits that repeatedly forced manual handoffs.

 
 Key pattern: You delegate large autonomous workflows but interrupt decisively the moment Claude over-engineers or strays from your explicit architectural rules.

 

 

 
 

 
User Response Time Distribution

 

 
2-10s

 

 
95

 

 
10-30s

 

 
185

 

 
30s-1m

 

 
195

 

 
1-2m

 

 
203

 

 
2-5m

 

 
226

 

 
5-15m

 

 
183

 

 
>15m

 

 
128

 

 

 Median: 96.0s • Average: 334.9s
 

 

 
 

 
Multi-Clauding (Parallel Sessions)

 
 

 

 
148

 
Overlap Events

 

 

 
123

 
Sessions Involved

 

 

 
39%

 
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

 

 
308

 

 

 
Afternoon (12-18)

 

 
886

 

 

 
Evening (18-24)

 

 
629

 

 

 
Night (0-6)

 

 
32

 

 

 

 
Tool Errors Encountered

 

 
Other

 

 
258

 

 
User Rejected

 

 
113

 

 
Command Failed

 

 
95

 

 
File Changed

 

 
26

 

 
File Not Found

 

 
14

 

 
Edit Failed

 

 
9

 

 

 

 
 
Impressive Things You Did

 
Over 40 days, you've driven 168 sessions across a Flutter kiosk app, a Rust MCP server, and 3D print profile generation, completing 128 commits with strong autonomous, contract-driven workflows.

 

 
 

 
Contract-Driven TDD Sprints

 
You consistently structure feature work around Sprint Contracts with QA gates, running automated test suites (476 + 193 vitest, tsc clean) before committing. This discipline let you deliver multi-task sprints like Schedule-Vote Tasks 1-3 with QA APPROVE on every task plus a server-alignment fix.

 

 
 

 
Root-Cause Debugging on Hard Bugs

 
You don't settle for surface fixes — you traced an autoDispose race in a search provider, an enum vs int type mismatch in Bluetooth scan range, and an MCP hot-restart reconnect bug down to their roots. You then validated each fix with real scenarios (5/5 reconnect cycles, QA 20/20) before shipping releases like server-v0.7.3.

 

 
 

 
End-to-End MCP & Device Tooling

 
You push your own infrastructure forward, building DTD-based Flutter VM service discovery for your MCP server and shipping v0.8.0 with full QA. You combine this with practical device work — pushing 660MB OLKP files to physical devices and debugging emulator connections — to verify features in real environments.

 

 
 

 

 

 

 
What Helped Most (Claude's Capabilities)

 

 
Good Debugging

 

 
20

 

 
Correct Code Edits

 

 
18

 

 
Multi-file Changes

 

 
16

 

 
Good Explanations

 

 
12

 

 
Proactive Help

 

 
8

 

 
Fast/Accurate Search

 

 
4

 

 

 

 
Outcomes

 

 
Not Achieved

 

 
6

 

 
Partially Achieved

 

 
10

 

 
Mostly Achieved

 

 
36

 

 
Fully Achieved

 

 
30

 

 
Unclear

 

 
2

 

 

 

 
 
Where Things Go Wrong

 
Your friction clusters around Claude misreading the intent of your requests, ignoring patterns and rules you've already established, and getting blocked or stalled by tooling and over-exploration.

 

 
 

 
Misunderstood intent and wrong approach

 
Claude frequently misreads the abstraction level or scope of your requests, defaulting to more complex solutions than you asked for. You can reduce this by stating the desired pattern and 'do the minimal change' up front before Claude starts proposing approaches.

 
On refactoring data transfer into olkpProvider, Claude inlined logic in callers, then extracted code as a widget instead of plain functions, requiring multiple corrections.

You asked to remove the alreadyDownloaded check entirely but Claude proposed a lib directory check plus provider cache, forcing you to clarify the simpler intent.
 
 

 
 

 
Ignored established rules and patterns

 
Claude repeatedly violated conventions you'd already set—reintroducing forbidden patterns and skipping required skill triggers—leading to rejected work and frustration. Pinning these rules in a persistent CLAUDE.md or skill reminder may help Claude honor them without re-prompting.

 
Despite your existing rule against ValueNotifier and complex providers, Claude kept introducing ValueNotifier/useState patterns during firmware filename work, causing you to interrupt multiple times with profanity.

Claude output the work summary in markdown-rendered format even though your custom skill explicitly forbade it, and also missed the minimum-items-per-category rule.
 
 

 
 

 
Tooling blocks and over-exploration

 
Sessions stalled when Claude over-explored before acting or hit tooling limits like MCP connection drops and missing simulator interaction support. Setting a hard exploration budget and verifying tool capabilities early could keep these moving.

 
Claude spent excessive time exploring Figma metadata and parent nodes instead of implementing, leading you to interrupt before any code changes were made.

End-to-end simulator UI testing was repeatedly blocked by flutter-playwright MCP lacking tap/interact support and losing the VM service connection, frustrating you and forcing handoffs.
 
 

 
 

 

 

 

 
Primary Friction Types

 

 
Wrong Approach

 

 
53

 

 
Misunderstood Request

 

 
38

 

 
User Rejected Action

 

 
30

 

 
Buggy Code

 

 
21

 

 
Excessive Changes

 

 
12

 

 
Mcp Tool Failure

 

 
4

 

 

 

 
Inferred Satisfaction (model-estimated)

 

 
Frustrated

 

 
12

 

 
Dissatisfied

 

 
55

 

 
Likely Satisfied

 

 
200

 

 
Satisfied

 

 
8

 

 

 

 
 
 
Existing CC Features to Try

 

 
Suggested CLAUDE.md Additions

 
Just copy this into Claude Code to add it to your CLAUDE.md.

 

 Copy All Checked 
 

 
 

 
 
 Never use ValueNotifier or useState/useEffect patterns; prefer simpler Riverpod providers and useMemoized for derived state. 
 Copy 
 
 
The user pushed back multiple times (with frustration) over Claude reintroducing ValueNotifier and useState patterns in refactors despite prior rules.

 

 
 

 
 
 When producing work summaries via the work-summary skill, output PLAIN TEXT only (no markdown rendering) and describe work by file/feature units as the skill specifies. 
 Copy 
 
 
Across at least three sessions Claude violated the plain-text rule and summarized by feature description instead of the requested units, requiring re-requests.

 

 
 

 
 
 Place extracted/refactored helper functions per the project's established architecture — do not invent new folders or inline into callers; confirm location before implementing if unclear. 
 Copy 
 
 
Multiple refactoring sessions stalled because Claude proposed wrong locations (messagebox file, new flows folder) and misread the desired abstraction level.

 

 
 

 
 
 Prefer the simplest change that satisfies the request; do not add cache checks, provider scaffolding, or extra abstractions unless explicitly asked. 
 Copy 
 
 
Claude repeatedly over-engineered simple requests (e.g., adding lib-directory + provider cache when the user just wanted a check removed), causing interruptions.

 

 
 

 
 
 For all Flutter/Dart edits, run codegen and dart analyze and ensure they pass before declaring work complete; for Rust/TS changes ensure tsc and the test suites pass. 
 Copy 
 
 
Successful sessions consistently ended with passing analyze/codegen/tests, while friction arose when verification was skipped.

 

 
 

 
 
 
Just copy this into Claude Code and it'll set it up for you.

 

 
 

 
Custom Skills

 
Reusable single-command workflows defined as markdown files.

 
 Why for you: You already rely on skills (work-summary, feedback-record, print-profile) — codifying your contract-driven sprint + QA + commit pipeline as a skill would standardize the autonomous flows you run repeatedly.

 
 

 

 

 Create .claude/skills/sprint/SKILL.md with: 'Run preflight, write a Sprint Contract, implement with TDD, run codegen+analyze+tests, request QA APPROVE, then commit. Never use ValueNotifier or useState.' 
 Copy 
 

 

 

 
 

 
 

 
Hooks

 
Shell commands that auto-run at lifecycle events.

 
 Why for you: Many friction points came from skipped verification; a PostToolUse hook running dart analyze / codegen after edits would catch issues before you do.

 
 

 

 

 // .claude/settings.json
{
 "hooks": {
 "PostToolUse": [{"matcher": "Edit|Write", "command": "dart analyze 2>&1 | tail -20"}]
 }
} 
 Copy 
 

 

 

 
 

 
 

 
MCP Servers

 
Connect Claude to external tools and devices via Model Context Protocol.

 
 Why for you: You use flutter-playwright MCP heavily but hit reconnect/port/tap-support failures; pinning a stable server config and documenting the wrapper path would reduce the recurring simulator-verification friction.

 
 

 

 

 claude mcp add flutter-playwright -- /path/to/correct/wrapper.sh --vm-discovery dtd 
 Copy 
 

 

 

 
 

 
 

 
 
 
New Ways to Use Claude Code

 
Just copy this into Claude Code and it'll walk you through it.

 

 
 

 
Stop reintroducing forbidden state patterns

 
Lock in the no-ValueNotifier / no-useState rule so refactors don't regress.

 
Several refactoring sessions reached frustration (including profanity) because Claude kept adding ValueNotifier and useState+useEffect against your standing rules. These rules existed but weren't consistently applied across sessions. Putting them in CLAUDE.md and referencing them at refactor start prevents the back-and-forth.

 
 

 
Paste into Claude Code:

 

 Before you edit, confirm: this refactor will use Riverpod providers and useMemoized only — NO ValueNotifier, NO useState/useEffect. State the abstraction level and target file, and wait for my OK before implementing. 
 Copy 
 

 

 
 

 
 

 
Confirm scope and location before large refactors

 
Have Claude propose the target file/abstraction and get approval before writing.

 
Refactor sessions repeatedly stalled on wrong placement (inlining in callers, new flows folder, messagebox file) and wrong abstraction level. The successful ones used a Sprint Contract first. Front-loading a one-line plan saves multiple rejected attempts.

 
 

 
Paste into Claude Code:

 

 Don't implement yet. Give me a 3-line plan: (1) which functions get extracted, (2) exactly which file they go in, (3) the abstraction (plain functions vs widget vs provider). I'll approve before you code. 
 Copy 
 

 

 
 

 
 

 
Don't over-engineer simple requests

 
Ask for the minimal change before adding abstractions.

 
When you asked to simply remove an alreadyDownloaded check, Claude proposed lib-directory checks plus provider caching. Multiple sessions show this tendency to expand scope. Telling Claude to default to the smallest viable edit reduces excessive_changes friction.

 
 

 
Paste into Claude Code:

 

 Make the smallest possible change to do exactly this and nothing more — no extra caching, providers, or abstractions. If you think more is needed, ask first. 
 Copy 
 

 

 
 

 
 

 
Verify claims about skill/tool execution

 
Require Claude to show evidence it actually invoked a skill or tool.

 
Claude once claimed to use the /insights skill but had only read an existing file, requiring correction and doc fixes. Asking for proof of actual invocation prevents false-completion claims, especially in your autonomous pipelines.

 
 

 
Paste into Claude Code:

 

 Confirm you actually invoked the skill/tool by showing the command and its output — do not claim completion based on reading a pre-existing file. 
 Copy 
 

 

 
 

 
 

 
 

 
 
On the Horizon

 
AI-assisted development is shifting from single-file edits toward autonomous, contract-driven workflows where agents implement, test, and verify entire sprints end-to-end with minimal human correction.

 

 
 

 
Self-Verifying Sprint Pipelines With Simulator Loops

 
Your contract-driven TDD workflows already chain implementation, QA approval, and commits across Flutter/Rust kiosk and Schedule-Vote apps. The next leap is closing the simulator verification gap that repeatedly forced handoffs—an agent that launches the app itself, drives the UI via MCP tap/interact, captures screenshots, diffs against expected states, and only commits once end-to-end behavior passes. This turns 'mostly_achieved' sprint validations into fully autonomous green-to-commit cycles.

 
 Getting started: Upgrade flutter-playwright MCP to a build with tap/interact support and stable VM-service reconnect, then wrap your preflight→tests→QA→simulator→commit steps into a single slash-command skill that refuses to commit on simulator failure.

 

Paste into Claude Code:
 Run the full sprint validation pipeline autonomously: execute preflight, run all unit/vitest tests, then YOU launch the Flutter app yourself and use the flutter-playwright MCP to drive the actual UI for each acceptance criterion in the sprint contract. Capture a screenshot per step, verify the rendered state matches expected, and report any AABB/overflow regressions. Only commit and push once tests AND simulator UI verification both pass. If the MCP loses its VM service connection, retry with watch+retry before failing—do not hand off to me unless the tool genuinely cannot interact. Copy 

 

 
 

 
Persistent Project Rules As Enforced Guardrails

 
Your biggest friction—wrong_approach (53) and misunderstood_request (38)—stems from Claude reintroducing banned ValueNotifier patterns, over-engineering providers, and misreading abstraction intent despite prior corrections. Imagine a self-enforcing rules layer: an agent that loads your accumulated architectural feedback before every task, auto-triggers feedback-record on each correction, and self-audits its own diffs against your rules (plain functions not widgets, useMemoized not useState, full-path-vs-filename separation) before showing you anything. Corrections compound into prevention rather than repeating.

 
 Getting started: Build a CLAUDE.md-backed 'rules-gate' skill that reads your project conventions and runs a pre-output self-review diff check, and wire the feedback-record skill to fire automatically whenever you reject an approach.

 

Paste into Claude Code:
 Before implementing anything in this repo, load all recorded architectural feedback and project rules (no ValueNotifier, prefer plain functions over widgets for extraction, use useMemoized not useState+useEffect, separate display filename from full-path data, keep providers simple). After drafting your implementation, run a self-audit: diff your proposed changes against each rule and list any violations BEFORE presenting code. If I correct an approach during the session, immediately invoke the feedback-record skill to persist it across all relevant locations so it never recurs. Confirm which rules you loaded before starting. Copy 

 

 
 

 
Parallel Print-Profile Generation Agents

 
Your MakerWorld→Bambu profile workflow repeatedly stalls during the crawling step, causing four not_achieved interruptions. Picture a fleet of parallel agents: one batch-crawls multiple MakerWorld URLs and caches metadata, another runs tolerance-test-coupon iterations (like your Ferris Wheel xy_hole_compensation loop) and converges on validated values, and a third assembles importable profile bundles—all dispatched at once so a slow crawl never blocks the human. The full catalog of models becomes a single overnight batch job with validated, ready-to-import output.

 
 Getting started: Use the Task tool to spawn parallel subagents per model URL behind your print-profile skill, with a resilient crawler that times out gracefully and caches partial progress so interruptions resume instead of restart.

 

Paste into Claude Code:
 I have several MakerWorld model URLs that each need a validated, importable Bambu print profile. Spawn parallel subagents—one per URL—that each crawl the model, cache the metadata locally (so a crawl timeout resumes rather than restarts), ask me material clarifications in a single batched question across all models, then generate and validate each profile bundle. For any model needing a tolerance fit (like bearing/hole fits), iterate test-coupon compensation values automatically and report the dialed-in xy_hole_compensation. Give me one consolidated summary of all completed profiles and any that need my input, rather than blocking on the slowest crawl. Copy 

 

 
 

 

 
 

 
"User dropped profanity after Claude kept forcing ValueNotifier patterns it had been explicitly told not to use — repeatedly over-engineering a simple request until the user interrupted in frustration"

 
During a Flutter kiosk refactoring session, the user just wanted a simple firmware path change, but Claude kept reintroducing ValueNotifier/useState patterns against the user's standing rules, escalating frustration to the point of profanity (and an earlier '니가 띄워야지' — 'YOU need to launch it' — when Claude wouldn't run the app itself)

</details>

## 1. 글로벌 Evaluator Feedback

- 경로: `/Users/jackson/.harness/feedback/evaluator`
- 총 파일: **190**

### Verdict 분포

- **APPROVE**: 109
- **REJECT**: 80
- **UNKNOWN**: 1

### Skill 분포

- `qa-evaluator`: 190

### Project 분포

- `claude-plugins`: 117
- `fit-pal`: 38
- `fit-pal-app`: 16
- `fit-pal-server`: 6
- `fit-pal/app`: 3
- `flutter_playwright`: 3
- `fit-pal-flutter`: 1
- `bambu-kit-v0.4.0-9mm-craft-knife`: 1
- `fitpal-server`: 1
- `iyaki-zip-dev`: 1
- `claude-plugins / react-kit phase10-research kaizen`: 1
- `bambu-kit/bambu-print-profile v0.4.1`: 1
- `bambu-kit/bambu-print-profile`: 1

### 최근 REJECT 사유 (Top 20)

- [2026-06-02] **fit-pal**: [미검증] 3건 누적 (LG-04, DG-02, DG-04) — 자동 REJECT
- [2026-06-02] **fit-pal**: ER-03 FAIL: Duplicate GlobalKey / _dependents.isEmpty 예외 비결정적 발생. 계약 미충족.
- [2026-05-29] **fit-pal**: LG-07: app/.dart_defines.json 파일 물리적 존재 (test ! -f = FAIL). gitignore 등록됐으나 파일시스템 레벨 존재.
- [2026-05-29] **fit-pal**: AR-01: Sprint B 변경 6개 필수 파일 미커밋 (git diff main...HEAD = 2파일만). 추가로 bootstrap.dart + locale_provider.dart scope 외 변경 사용자 승인 없음.
- [2026-05-27] **bambu-kit/bambu-print-profile v0.4.1**: VR-02: marketplace.json description still shows [v0.4.0 · 2026-05-23], not updated to v0.4.1
- [2026-05-27] **bambu-kit/bambu-print-profile**: VR-03: plugin.json version 0.4.1 (0.4.2 미bump) + marketplace.json [v0.4.1] 미갱신
- [2026-05-27] **bambu-kit/bambu-print-profile**: PL-01: 볼트 통과 hole 보정값 불일치 — 계약 xy_hole +0.2~0.3 vs 구현 +0.05 추가
- [2026-05-23] **fit-pal-app**: LG-01: swatch 탭 시 optimistic 업데이트 없음. handlePaletteSelected가 await 전 localGroups 미업데이트 (group_preferences_body.dart:36-60)
- [2026-05-23] **fit-pal-app**: AR-03: schedule_collapsible_calendar.dart:276-277 Radius.circular(26) AppRadii 토큰 미사용. 기존 코드이나 변경된 파일이므로 계약 범위 포함.
- [2026-05-19] **fit-pal**: UI-02: 자동 스크롤 미구현 (highlight pulse만 구현됨)
- [2026-05-19] **fit-pal**: UI-02: slot 자동 스크롤 + 1.5초 highlight pulse 미구현
- [2026-05-19] **fit-pal**: UI-01: 알림 카드 본문에 scheduled_at_short 누락
- [2026-05-19] **fit-pal**: UI-01: actor handle 대신 display name 사용, 영어 등가 미구현
- [2026-05-19] **fit-pal**: RE-01: notification_list_page._navigateByType vote_cast 케이스가 PushDeepLinker.navigate 재사용 없이 중복 구현
- [2026-05-17] **fit-pal-app**: 미검증 2건 (AR-03, DG-04) — 2건 이상 자동 REJECT 규칙 적용
- [2026-05-17] **fit-pal-app**: DG-02: cargo test -p fitpal-routine --lib compile error 4건 (service.rs 테스트 구조체 리터럴에 icon 필드 누락)
- [2026-05-17] **fit-pal-app**: DG-02: cargo clippy doc_markdown 에러 1건 (routine.rs:17 backtick 미적용)
- [2026-05-17] **fit-pal-app**: AR-03: 스킬 invoke 파일시스템 아티팩트 없음 (구조적 검증 불가)
- [2026-05-16] **fit-pal-app**: UI-04 FAIL: _buildMetalCard gradient alignment/stops 변경, FigmaDropShadow→FigmaInnerShadow 교체 — 계약 '시각 변경 0' 위반
- [2026-05-16] **fit-pal-app**: AR-02 FAIL: metalCard() borderRadius override 경로 strokeWeight/strokeAlign 추가, _buildMetalCard 내부 변경 — 계약 '구현 변경 없다' 위반

### 최근 Improvement Suggestions (Top 15)

- [2026-06-11] **fit-pal/app**: LG-01 테스트 확장: Authorization 헤더 마스킹, api_key 패턴도 테스트에 추가하면 계약이 열거한 5개 패턴 전수 커버 가능
- [2026-06-11] **fit-pal/app**: DG-04 런타임 검증: dev 모드 앱 구동 후 네트워크 요청 시 로깅 인터셉터 에러 없음 확인 권장
- [2026-06-11] **fit-pal**: MCP 서버 설정 시 IDE diagnostics 직접 관찰 가능
- [2026-06-11] **fit-pal**: DG-02: MCP 서버 설정 시 IDE diagnostics 런타임 검증 추가 가능
- [2026-06-05] **claude-plugins**: FC-07 조건에 10종 파일 경로를 명시적으로 나열하면 enumerated 검증 효율 향상
- [2026-06-02] **fit-pal**: MCP 서버 연결 후 LG-04/DG-04 재검증
- [2026-06-02] **fit-pal**: ER-03 계약에 pre-existing 이슈 제외 조항 추가
- [2026-06-01] **fit-pal-server**: ER-01/ER-03: 향후 통합테스트에서 응답 JSON body도 파싱해 에러 메시지/코드 필드를 검증하면 계약 신뢰도 향상
- [2026-06-01] **fit-pal-app**: icon_picker_sheet/color_picker_row/icon_name_row가 group feature 내부에만 있으나 다른 feature에서 재사용 가능성이 있으면 shared/로 이동 검토
- [2026-06-01] **fit-pal-app**: DG-04 런타임 검증을 위해 MCP 서버(mcp_server) 설정 권장
- [2026-05-30] **fit-pal-app**: DG-04 런타임 검증: MCP 서버 설정 후 실기 확인 권장 (현재 mcp_server: null).
- [2026-05-30] **fit-pal-app**: AP-02 grep 패턴 정교화 권장: 현재 'catch \(e\)' 패턴이 'on Exception catch (e)' substring을 false positive로 매칭. '^ *} catch \(e\)' 또는 '(?<!on \w+ )catch \(e\)' 형태로 변경 권장.
- [2026-05-29] **fit-pal**: LG-07 측정을 test ! -f 에서 git ls-files 결과 empty 로 변경 권장 (gitignored 파일의 물리적 존재 허용 여부 명확화)
- [2026-05-29] **fit-pal**: AR-01 측정 명령에 커밋 완료 전제 명시 권장: 'Sprint B 커밋 완료 후 git diff main...HEAD 실행'
- [2026-05-28] **fit-pal-server**: DA-02: 두 번 실행 후 timestamp 동일성 assertion 추가

## 2. 외부 프로젝트 (`Hub/10_Dev`) 피드백

- Hub 루트: `/Users/jackson/Hub/10_Dev`
- 발견된 프로젝트: **5**

### `apps`

- 경로: `/Users/jackson/Hub/10_Dev/apps`
- sprint-feedback.md: 77 lines
- history sprint-contracts: 44
- 최근 contracts:
  - 20260526-1050-sprint-contract.md
  - 20260601-2230-sprint-contract.md
  - 20260602-1200-sprint-contract.md
  - 20260604-1106-sprint-contract.md
  - 20260604-1658-sprint-contract.md

<details><summary>sprint-feedback.md 앞부분</summary>

```markdown
# Sprint Feedback
Feature: 초기화(reset) 시 프리로드 캐시 정리
Evaluated: 2026-06-04 12:00
Verdict: APPROVE
Iteration: 1

---

## Results

### Logic (4/4)

- [x] LG-01: event 도메인 선택 시 포스터 preload 캐시가 events state 비우기 이전에 정리됨 — PASS [L3]
  - 근거: `olkp_provider.dart:846` `clearPreloadEventResource()` → `olkp_provider.dart:847` `clearEvents()` 순서 확인. `clearPreloadEventResource`는 `_getEventPosterImages()`(events state의 poster_image_path)를 순회하므로 events가 null이 되기 전에 실행되어야 하는 전제가 코드로 충족됨.

- [x] LG-02: common preset 도메인 선택 시 스킨 가이드 애니메이션 preload 캐시가 setCommonPreset 이전에 정리됨 — PASS [L3]
  - 근거: `olkp_provider.dart:872` `clearPreloadSkinResource()` → `olkp_provider.dart:873` `_deleteDirSafe(...)` → `olkp_provider.dart:876` `setCommonPreset(OlkpCommonPreset.newCommonPreset())` 순서 확인.

- [x] LG-03: 선택되지 않은 도메인의 preload 캐시는 보존됨 — PASS [L3]
  - 근거: `olkp_provider.dart:844` `if (selection.includeEvent)` 블록 내에서만 `clearPreloadEventResource` 호출, `olkp_provider.dart:867` `if (selection.includePresetCommon)` 블록 내에서만 `clearPreloadSkinResource` 호출. import 경로의 `loadMetadata`(라인 341~350)와 동일한 도메인별 조건 분기 구조. 선택되지 않은 도메인은 해당 if 블록 자체에 진입하지 않으므로 preload 캐시 보존 확인됨.
```

</details>

### `fit-pal`

- 경로: `/Users/jackson/Hub/10_Dev/fit-pal`
- sprint-feedback.md: 55 lines
- history sprint-contracts: 31
- 최근 contracts:
  - 20260611-0919-server-authz-sprint-contract.md
  - 20260611-1030-app-logging-mask-sprint-contract.md
  - 20260611-1130-server-h2-smartip-sprint-contract.md
  - 20260611-1200-server-m3-cors-sprint-contract.md
  - 20260611-1230-server-m4-ws-sprint-contract.md

<details><summary>sprint-feedback.md 앞부분</summary>

```markdown
# Sprint Feedback
Feature: 서버 스토리지 자격증명 fail-fast (M-5 — 약한 minioadmin 기본값 부팅 차단)
Evaluated: 2026-06-11 14:10
Verdict: APPROVE
Iteration: 1

## Results

### Logic (2/2)
- [x] LG-01: dev/test 환경에서 minioadmin/빈값 면제 — PASS
  - 근거: `server/shared/config/src/lib.rs:583-585` — `if matches!(app_env, "dev" | "test") { return; }`. 테스트 `dev_allows_default_minio_credential`(line 710), `test_env_allows_default_minio_credential`(line 715) 모두 cargo test GREEN (L3)
- [x] LG-02: prod/staging 비-dev에서 약한값/빈값 panic — PASS
  - 근거: `lib.rs:592` — `value.is_empty() || value == DEFAULT_MINIO_CREDENTIAL`. 테스트 4케이스 전수 확인: `prod_panics_on_default_access_key`(line 727), `prod_panics_on_default_secret_key`(line 733), `prod_panics_on_empty_access_key`(line 739), `staging_panics_on_default_credential`(line 745) + 강한값 통과 `prod_allows_strong_credentials`(line 720), 19/19 GREEN (L3)

### Error (1/1)
- [x] ER-01: panic 메시지에 3개 anchor 포함 + tracing::error! 구조화 로그 — PASS
  - 근거: `lib.rs:600-604` — panic! 메시지에 `SECURITY`, `APP_ENV={app_env}`, `{env_var}` 리터럴 포함. for loop (line 588-590)에서 access_key → `FITPAL__STORAGE__ACCESS_KEY`, secret_key → `FITPAL__STORAGE__SECRET_KEY` 분기. tracing::error! (line 593-599) `app_env`, `storage_key`, `env_var` 필드. 테스트 `storage_panic_message_contains_anchors`(line 750-765) assert 3개 GREEN (L3)

### Architecture (2/2)
- [x] AR-01: AppConfig::load()에서 validate_jwt_secret 다음 validate_storage_credentials 호출 — PASS
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

- `.harness/history/20260417-1717-sprint-contract.md`
- `.harness/history/20260424-kaizen-phase10-react-kit-sprint-contract.md`
- `.harness/history/20260424-kaizen-phase4-harness-sprint-contract.md`
- `.harness/history/20260424-kaizen-phase7-backend-kit-sprint-contract.md`
- `.harness/history/20260424-phase1-design-guides-sprint-contract.md`
- `.harness/history/20260424-phase6-design-kit-sprint-contract.md`
- `.harness/history/20260424-phase8-sprint-contract.md`
- `.harness/history/20260516-0111-sprint-contract.md`
- `.harness/history/20260516-1943-sprint-contract.md`
- `.harness/history/20260605-1036-sprint-contract.md`

## 5. Validate-Plugin 최근 실행 스냅샷

```text
... (이전 출력 생략)
  V3 refs            0 links — OK
  V4 triggers        46 keywords — OK
  V5 placeholders    0 found — OK
  V6 code-fence      0 bare — OK
  V7 plugin-json     v0.2.5 matches marketplace — OK

=== backend-kit ===
  V1 frontmatter     4 skills + 1 agent — OK
  V2 templates       0 files — SKIP (no templates/)
  V3 refs            0 links — OK
  V4 triggers        18 keywords — OK
  V5 placeholders    0 found — OK
  V6 code-fence      0 bare — OK
  V7 plugin-json     v0.1.3 matches marketplace — OK

=== infra-kit ===
  V1 frontmatter     4 skills + 1 agent — OK
  V2 templates       0 files — SKIP (no templates/)
  V3 refs            0 links — OK
  V4 triggers        19 keywords — OK
  V5 placeholders    0 found — OK
  V6 code-fence      0 bare — OK
  V7 plugin-json     v0.1.3 matches marketplace — OK

=== rust-kit ===
  V1 frontmatter     16 skills + 1 agent — OK
  V2 templates       1 parsed, 4 skipped (ts/js) — OK
  V3 refs            0 links — OK
  V4 triggers        79 keywords — OK
  V5 placeholders    0 found — OK
  V6 code-fence      0 bare — OK
  V7 plugin-json     v0.1.4 matches marketplace — OK

=== react-kit ===
  V1 frontmatter     21 skills + 3 agents — OK
  V2 templates       5 parsed, 4 skipped (ts/js) — OK
  V3 refs            0 links — OK
  V4 triggers        157 keywords — OK
  V5 placeholders    0 found — OK
  V6 code-fence      0 bare — OK
  V7 plugin-json     v0.1.4 matches marketplace — OK

=== planning-kit ===
  V1 frontmatter     12 skills + 1 agent — OK
  V2 templates       0 files — SKIP (no templates/)
  V3 refs            0 links — OK
  V4 triggers        95 keywords — OK
  V5 placeholders    0 found — OK
  V6 code-fence      0 bare — OK
  V7 plugin-json     v0.3.2 matches marketplace — OK

=== reflect-kit ===
  V1 frontmatter     4 skills — OK
  V2 templates       0 files — SKIP (no templates/)
  V3 refs            0 links — OK
  V4 triggers        25 keywords — OK
  V5 placeholders    0 found — OK
  V6 code-fence      0 bare — OK
  V7 plugin-json     v0.4.0 matches marketplace — OK

=== bambu-kit ===
  V1 frontmatter     1 skill — OK
  V2 templates       0 files — SKIP (no templates/)
  V3 refs            0 links — OK
  V4 triggers        5 keywords — OK
  V5 placeholders    0 found — OK
  V6 code-fence      0 bare — OK
  V7 plugin-json     v0.4.2 matches marketplace — OK

=== onboarding-kit ===
  V1 frontmatter     1 skill — OK
  V2 templates       0 files — SKIP (no templates/)
  V3 refs            0 links — OK
  V4 triggers        8 keywords — OK
  V5 placeholders    0 found — OK
  V6 code-fence      0 bare — OK
  V7 plugin-json     v0.1.1 matches marketplace — OK

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

