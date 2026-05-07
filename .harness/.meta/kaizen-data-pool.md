# Kaizen Data Pool

Generated: 2026-05-07T23:10:48
Generator: `scripts/collect-kaizen-data.py`

카이젠 오케스트레이션의 Phase 별 서브에이전트가 참조할 통합 데이터 풀이다. 이 파일은 `scripts/collect-kaizen-data.py` 로 재생성된다 — 수동 수정 금지.

## 0. `/insights` Report (외부 도구 산출물)

- 경로: `/Users/jackson/.claude/usage-data/report.html` · HTML 추출 텍스트
- 최근 갱신: 2026-05-07T22:55:55 ✓ VERY FRESH (0.2시간 전)
- 모든 Phase 서브에이전트가 **최우선** 참조해야 한다 (Friction Points / Recommended Patterns / Feature Suggestions / 이번 사이클 신규 워크플로우 제안)

<details><summary>insights report 본문 (auto-extracted)</summary>

Claude Code Insights 
 

 
 
 
 

 
Claude Code Insights

 
2,391 messages across 130 sessions (827 total) | 2026-04-14 to 2026-05-07

 
 

 
At a Glance

 

 
 What's working: You run a remarkably disciplined operation: contract → QA → push sprint cycles driven by terse confirmations, with explicit session handoff documents that let you sustain multi-phase efforts across days. When Claude misses something, you don't just patch in place—you codify the lesson into rule files, skills, and even hook-based enforcement, turning each friction point into permanent leverage. Impressive Things You Did → 

 
 What's hindering you: On Claude's side: over-eager scope expansion (unauthorized deletions, unrequested design choices) and a tendency to skip the proactive-improvement checklist on rule-based refactors, forcing you to escalate the same issues repeatedly. On your side: long sessions get derailed by output token limits, MCP/agent hangs, and parallel-automation conflicts that you could catch earlier with a quick pre-flight branch/process check before kicking off sprint work. Where Things Go Wrong → 

 
 Quick wins to try: Promote your sprint workflow into a /sprint Skill so you stop re-prompting the contract-QA-push loop, and pair it with a /refactor-widget skill that loads your anti-AI-tone checklist before any edits. A PreToolUse Hook that blocks edits when the branch has diverged from origin or stale MCP processes are detected would prevent the duplicated-work and connection-failure patterns that keep eating sessions. Features to Try → 

 
 Ambitious workflows: As models get stronger, your contract-driven cycles should run unattended for hours—drafting contracts, executing TDD, recovering from rebases, and resuming across context boundaries via durable state files. The Flutter-vs-Figma parity work that burned 5+ hours is the highest-leverage target: a self-verifying visual loop that screenshots, diffs against Figma, and iterates FigmaDecoration parameters until SSIM converges would turn your most painful sessions into measurable optimization problems. On the Horizon → 

 

 

 

 
 What You Work On 
 How You Use CC 
 Impressive Things 
 Where Things Go Wrong 
 Features to Try 
 New Usage Patterns 
 On the Horizon 
 Team Feedback 
 

 

 

2,391

Messages

 

+92,817/-11,678

Lines

 

1047

Files

 

18

Days

 

132.8

Msgs/Day

 

 
 
What You Work On

 

 
 

 

 Schedule-Vote Backend (Rust) 
 ~12 sessions 
 

 
Multi-sprint backend development for a friends-only fitness scheduling MVP, executing Tasks 1-22 via contract-driven TDD with subagent orchestration. Claude handled QA cycles, Sentry integration, ReminderJob/ResolutionJob implementation, integration test fixes, and managed git rebases with multiple commits pushed to dev branch.

 

 
 

 

 Flutter UI Refactoring & Anti-AI-Tone Rules 
 ~15 sessions 
 

 
Systematic refactoring of admin widgets, messagebox components, and carousel/toolbar widgets following project style rules with i18n locale key extraction. Heavy iterative work with Edit tool where Claude often required user corrections on Stack vs Column choices, TextStyle migrations, and over-engineering, leading to documented rule additions in feedback logs.

 

 
 

 

 Figma-Flutter Design Parity 
 ~8 sessions 
 

 
Pixel-perfect alignment between Figma designs and Flutter implementations, including Aqua button gradients, FigmaDecoration per-side borders, and skeuomorphic CSS matching. Created a figma-flutter-kit suite of 5 skills with QA validation, though sessions frequently hit friction with MCP device configuration and visual mismatches requiring multi-hour iteration.

 

 
 

 

 Flutter MCP Redesign & Animation Engine 
 ~7 sessions 
 

 
Multi-phase redesign of Flutter MCP server toward Observer-only architecture with persistent connection indicators, plus Sprint 5 force-layout algorithm benchmarking (d3-main adapter selected). Used Codex for parallel research/review, though several research agents hung or returned inaccurate claims requiring user correction.

 

 
 

 

 Worldbuilding IDE & Group-Invite Planning 
 ~6 sessions 
 

 
Strategic planning sessions producing design specs, sprint contracts, and 13-task implementation plans for new features like group-invite with ID search and the worldbuilding IDE pivot. Claude delivered comprehensive QA-reviewed plans with handoff documentation, occasionally over-applying formal discovery process when user wanted faster iteration.

 

 
 

 

 

 

 
What You Wanted

 

 
Code Refactoring

 

 
46

 

 
Code Explanation

 

 
22

 

 
Feature Implementation

 

 
20

 

 
Session Handoff

 

 
15

 

 
Refactoring

 

 
12

 

 
Documentation Update

 

 
12

 

 

 

 
Top Tools Used

 

 
Bash

 

 
4686

 

 
Edit

 

 
2447

 

 
Read

 

 
2375

 

 
Grep

 

 
636

 

 
Write

 

 
628

 

 
TodoWrite

 

 
443

 

 

 

 

 

 
Languages

 

 
Markdown

 

 
1315

 

 
TypeScript

 

 
712

 

 
Rust

 

 
373

 

 
JSON

 

 
173

 

 
YAML

 

 
131

 

 
HTML

 

 
122

 

 

 

 
Session Types

 

 
Multi Task

 

 
41

 

 
Iterative Refinement

 

 
28

 

 
Single Task

 

 
11

 

 
Quick Question

 

 
3

 

 
Exploration

 

 
2

 

 

 

 
 
How You Use Claude Code

 

 
You operate as a high-throughput technical director running long, multi-phase engineering campaigns. Your sessions are marathon-length (averaging ~11 hours each across 130 sessions, with 168 commits) and structured around formal artifacts: Sprint Contracts, Phase checkpoints, QA APPROVE cycles, and explicit handoff prompts for the next session. You delegate aggressively—using subagents, Codex research tasks, and parallel automation—and expect Claude to drive contract→implement→QA→push cycles autonomously. Your confirmations are often terse ('ㄱㄱ' / 'go'), signaling you've front-loaded the specification and now want execution without hand-holding.

Despite the autonomous framing, you interrupt and correct sharply when Claude drifts . Multiple sessions show frustration spikes when Claude misses obvious improvements (legacy `bodyMSemiBold` migration, unneeded null branches, hardcoded values), uses Stack where Column suffices, or invents Figma text style names without verification. Your reactions escalate—'다음 세션에 내가 뭐라고 말할지 말해야지!!!!'—and you frequently codify the correction into permanent project rules rather than just fixing the instance. This rule-as-output pattern (anti-AI-tone refactoring sweeps, feedback logs, PreToolUse hooks enforcing skill usage) shows you treat each friction point as a systemic gap to close, not a one-off.

You tolerate iteration on hard problems (5+ hours on a Flutter/HTML button match, 3 contract revisions for Parity/Consolidation) but lose patience with process violations : unauthorized edits, over-commenting, over-engineering, and Claude moving ahead without explicit direction. You also push back on false dichotomies and formal-discovery overhead when you want momentum. The infrastructure-heavy tool usage (4,686 Bash calls, 443 TodoWrite, 381 Agent invocations) confirms you're orchestrating Claude as a managed workforce rather than pair-programming with it.

 
 Key pattern: You run Claude as an autonomous sprint executor with formal contracts and QA gates, but sharply correct drift by promoting one-off mistakes into permanent project rules.

 

 

 
 

 
User Response Time Distribution

 

 
2-10s

 

 
103

 

 
10-30s

 

 
315

 

 
30s-1m

 

 
362

 

 
1-2m

 

 
403

 

 
2-5m

 

 
379

 

 
5-15m

 

 
187

 

 
>15m

 

 
102

 

 

 Median: 77.3s • Average: 229.6s
 

 

 
 

 
Multi-Clauding (Parallel Sessions)

 
 

 

 
191

 
Overlap Events

 

 

 
116

 
Sessions Involved

 

 

 
56%

 
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

 

 
416

 

 

 
Afternoon (12-18)

 

 
1250

 

 

 
Evening (18-24)

 

 
647

 

 

 
Night (0-6)

 

 
78

 

 

 

 
Tool Errors Encountered

 

 
Other

 

 
308

 

 
Command Failed

 

 
135

 

 
User Rejected

 

 
38

 

 
File Not Found

 

 
20

 

 
File Changed

 

 
19

 

 
Edit Failed

 

 
8

 

 

 

 
 
Impressive Things You Did

 
Across 130 sessions spanning Flutter, Rust backend, and design-systems work, you run a highly disciplined contract-driven development practice with strong handoff hygiene.

 

 
 

 
Contract-QA-Push Sprint Cycles

 
You consistently drive multi-task sprints through a rigorous Contract → Implementation → QA APPROVE → Commit/Push loop, often landing 13+ tasks across multiple sprints with full QA approval (e.g., Backend Tasks 1-13 schedule-vote MVP, Sprint 5 Tasks 4-9 via terse 'ㄱㄱ' confirmations). You even installed a PreToolUse hook to enforce skill usage, showing you treat process compliance as a first-class engineering concern.

 

 
 

 
Disciplined Session Handoffs

 
With 15 explicit session_handoff goals captured, you treat context continuity as a deliverable — demanding next-session prompt templates, comprehensive handoff docs, and clean commit boundaries before ending. This lets you sustain long-running multi-phase efforts (Phase A→B→C MCP redesign, multi-sprint backend work) without losing momentum between sessions.

 

 
 

 
Codified Feedback Into Rules

 
When Claude misses refactoring opportunities or misinterprets style rules, you don't just correct in-place — you push the lessons into project documentation, anti-AI-tone rule files, and skill upgrades (e.g., method-vs-class extraction rule added to three docs, list-building patterns codified after iteration). This turns every friction point into permanent leverage for future sessions.

 

 
 

 

 

 

 
What Helped Most (Claude's Capabilities)

 

 
Multi-file Changes

 

 
40

 

 
Correct Code Edits

 

 
13

 

 
Good Debugging

 

 
13

 

 
Good Explanations

 

 
9

 

 
Proactive Help

 

 
4

 

 
Fast/Accurate Search

 

 
2

 

 

 

 
Outcomes

 

 
Not Achieved

 

 
2

 

 
Partially Achieved

 

 
11

 

 
Mostly Achieved

 

 
36

 

 
Fully Achieved

 

 
33

 

 
Unclear

 

 
3

 

 

 

 
 
Where Things Go Wrong

 
Your sessions show strong overall delivery but recurring friction stems from Claude making changes you didn't ask for, missing rule-based refactoring opportunities until you escalate, and infrastructure/tooling failures that derail multi-hour workflows.

 

 
 

 
Unauthorized or over-eager scope expansion

 
Claude frequently makes deletions, edits, or design choices you didn't sanction, forcing you to course-correct or restore work. Being more conservative — confirming before destructive or scope-expanding actions — would prevent these reversals.

 
Claude deleted locator_entries action tools (tap/enter_text/scroll/swipe) thinking they were redundant, then had to restore them after you clarified only locate_widget was the target

Claude proceeded with refactors and rule reinterpretations without explicit direction across multiple anti-ai-tone sessions, requiring you to roll back unauthorized changes
 
 

 
 

 
Missed rule-based improvements requiring escalation

 
Claude repeatedly fails to apply documented refactoring rules autonomously, making you point out the same categories of issues with mounting frustration. Front-loading a rule-checklist pass before declaring work done would catch these.

 
You had to escalate angrily ('다음 세션에 내가 뭐라고 말할지 말해야지!!!!') when Claude skipped legacy bodyMSemiBold migration despite rule R1 explicitly requiring it

Claude missed TextStyle migrations, unnecessary local variables, unneeded null branches, and manual SizedBox gaps across S6 list widget refactors, leading you to add new rules to the feedback log just to enforce baseline attention
 
 

 
 

 
Tool and infrastructure failures derailing long sessions

 
Multi-hour workflows repeatedly hit output token limits, MCP connection issues, and orphaned background agents that waste your time and leave work unfinished. Detecting these early and falling back faster, plus chunking output proactively, would reduce lost progress.

 
Several sessions are unanalyzable because Claude's responses exceeded the 500 output token maximum and the transcript is just API errors, meaning entire sessions of your work produced no recoverable outcome

Two of three Codex background research tasks (R2 Play Console, R3 Sentry) hung indefinitely, flutter-playwright MCP failed due to 45+ stale processes, and golden parity tests hung on toImage — each requiring manual diagnosis before you could proceed
 
 

 
 

 

 

 

 
Primary Friction Types

 

 
Wrong Approach

 

 
77

 

 
Misunderstood Request

 

 
50

 

 
Buggy Code

 

 
34

 

 
User Rejected Action

 

 
21

 

 
Excessive Changes

 

 
17

 

 
Tool Failure

 

 
6

 

 

 

 
Inferred Satisfaction (model-estimated)

 

 
Frustrated

 

 
23

 

 
Dissatisfied

 

 
80

 

 
Likely Satisfied

 

 
297

 

 
Satisfied

 

 
36

 

 

 

 
 
 
Existing CC Features to Try

 

 
Suggested CLAUDE.md Additions

 
Just copy this into Claude Code to add it to your CLAUDE.md.

 

 Copy All Checked 
 

 
 

 
 
 ## Anti-AI-Tone Refactoring Rules
- Always check for legacy text style migrations (e.g., bodyMSemiBold) per rule R1 - migrate ALL occurrences, not just obvious ones
- Proactively identify these refactoring opportunities WITHOUT being asked: TextStyle migration, unnecessary local variables, unneeded null branches, hardcoded values, manual SizedBox gaps
- Verify exact Figma text style token names before applying - do NOT guess
- Prefer Column over Stack when children don't actually overlap 
 Copy 
 
 
These exact issues recurred across 8+ refactoring sessions with increasing user frustration ('다음 세션에 내가 뭐라고 말할지 말해야지!!!!') - user repeatedly had to point out the same missed improvements.

 

 
 

 
 
 ## Session Handoffs
When a session is wrapping up or hitting context limits, ALWAYS produce a next-session prompt template (not just a summary) that the user can paste verbatim to resume work. Include: current branch state, last commit, next concrete action, and any blocking context. 
 Copy 
 
 
session_handoff appeared 15 times as a top goal, and the user explicitly demanded this format with frustration when Claude only produced a summary instead of a paste-ready prompt.

 

 
 

 
 
 ## Sprint/Contract Workflow
- Do NOT start implementation without an approved Sprint Contract
- Before working on any task, check if parallel automation or another session has already completed/started it (git log, branch status)
- After QA REJECT, re-read the contract verbatim before fixing - watch for exact string matches (f32 vs f64, parameter names, Default impls)
- Run rebase BEFORE push, and verify push actually succeeded (don't assume) 
 Copy 
 
 
Multiple sessions show duplicated work with parallel automation, contract string-matching failures on QA re-evaluation, and unpushed rebase chains - these are repeated process failures.

 

 
 

 
 
 
Just copy this into Claude Code and it'll set it up for you.

 

 
 

 
Custom Skills

 
Define reusable markdown prompts callable via /command

 
 Why for you: You already created /insights and figma-flutter-kit skills successfully. Given 46 refactoring + 15 handoff + 12 doc-update sessions, codify /handoff (next-session prompt template), /sprint-contract (contract draft+QA loop), and /anti-ai-refactor (the rule checklist) to stop re-explaining the same workflow.

 
 

 

 

 mkdir -p .claude/skills/handoff && cat > .claude/skills/handoff/SKILL.md <<'EOF'
# Handoff Skill
Produce a paste-ready next-session prompt with:
1. Current branch + last commit SHA
2. What was completed this session (bullets)
3. Next concrete action (1-2 sentences)
4. Any blocking context (open PRs, failing tests, MCP issues)
Format as a code block the user can copy verbatim.
EOF 
 Copy 
 

 

 

 
 

 
 

 
Hooks

 
Auto-run shell commands at lifecycle events

 
 Why for you: You had 4 output-token-limit errors, MCP stale-process issues (45+ orphaned processes), and unpushed commits. A PreToolUse hook for git push verification and a SessionStart hook to clean stale flutter-playwright processes would prevent these recurring blockers. You already deployed a PreToolUse hook for skill enforcement - extend the pattern.

 
 

 

 

 // .claude/settings.json
{
 "hooks": {
 "SessionStart": [{"command": "pkill -f flutter-playwright || true"}],
 "PostToolUse": [{"matcher": "Bash", "command": "git status --porcelain | grep -q . && echo 'WARN: uncommitted changes'"}]
 }
} 
 Copy 
 

 

 

 
 

 
 

 
Task Agents

 
Spawn focused sub-agents for parallel/exploratory work

 
 Why for you: Your subagent-driven sprints (Tasks 1-13, 13-task group-invite) succeeded, but Codex delegation hung 2/3 times on R2/R3 research. Use Claude's built-in Task agents instead of external Codex for research-bounded tasks - they're more reliable and don't orphan. Reserve Codex for true second-opinion review.

 
 

 

 

 // In your prompt:
"Use a Task agent to research Sentry 0.47 Rust integration patterns and return a 1-page summary with code examples. Run in parallel with another Task agent researching Play Console review timelines." 
 Copy 
 

 

 

 
 

 
 

 
 
 
New Ways to Use Claude Code

 
Just copy this into Claude Code and it'll walk you through it.

 

 
 

 
Codify the Sprint Contract → QA → Push loop as a skill

 
You execute the same contract-driven workflow across dozens of sprints. Make it a /sprint skill instead of re-prompting each time.

 
Sessions show a consistent pattern: draft contract → implement → QA evaluator → fix REJECTs → commit → push. You hit friction with contract string-matching (f32/f64, Default impls), unpushed rebases, and duplicated parallel work. A /sprint skill that enforces 'check git log for parallel work first, draft contract, get user approval, implement, run QA, verify push succeeded' would eliminate 4-5 recurring friction points per sprint.

 
 

 
Paste into Claude Code:

 

 Create a .claude/skills/sprint/SKILL.md that enforces our contract-driven workflow: (1) check git log + dev branch for parallel work, (2) draft sprint contract and wait for user approval, (3) implement via TDD, (4) run QA evaluator and fix exact contract strings on REJECT, (5) commit logical chunks, (6) rebase + push + VERIFY push succeeded. Include checklist gates. 
 Copy 
 

 

 
 

 
 

 
Stop re-explaining anti-AI-tone refactoring rules

 
Promote the proactive-improvement checklist to CLAUDE.md and reference it from a /refactor-widget skill.

 
8+ sessions show user catching Claude missing the SAME issues: legacy TextStyle migration, unnecessary local variables, hardcoded values, Stack-vs-Column, manual SizedBox gaps. User explicitly added rules to feedback logs multiple times. Move this from per-session correction into a persistent skill+CLAUDE.md combo so Claude self-checks before claiming a refactor is done.

 
 

 
Paste into Claude Code:

 

 Read all my anti-AI-tone refactoring feedback logs and consolidate them into (1) a CLAUDE.md section with the top 10 proactive-check rules, and (2) a .claude/skills/refactor-widget/SKILL.md that runs through each rule as a self-review checklist before declaring a file done. 
 Copy 
 

 

 
 

 
 

 
Pre-flight check before sprint work to avoid duplicated effort

 
Add a mandatory git/branch reconnaissance step before starting any task that parallel automation might have touched.

 
Tasks 20/21 and others show Claude working on items that automation had already completed or was concurrently modifying, forcing reconciliation commits. Given you run multi-agent automation and Codex in parallel, a 30-second 'git fetch + log review + open-PR scan' at task start would prevent the desync entirely.

 
 

 
Paste into Claude Code:

 

 Before starting Task X, run git fetch, then show me: (1) commits on dev since my last local sync, (2) any commits matching this task's keywords, (3) any open PRs touching the files you plan to modify. Wait for my go-ahead before implementing. 
 Copy 
 

 

 
 

 
 

 
 

 
 
On the Horizon

 
With 949 hours across 130 sessions and 168 commits, your workflow is shifting from co-pilot to autonomous orchestrator—the next leap is letting Claude drive entire sprints, parallel investigations, and self-verification loops without manual nudging.

 

 
 

 
Fully Autonomous Sprint Contract Loops

 
Your data shows strong success with contract-QA-push cycles (Sprints 5-13 reached APPROVE with 13+ commits), but sessions like the Phase D resume and kaizen orchestration died mid-flight from context limits and token caps. Imagine kicking off a multi-task sprint and walking away while Claude drafts the contract, implements via TDD, runs QA, fixes rejections, commits, and pushes—self-recovering from rebase conflicts and resuming across context boundaries via durable state files.

 
 Getting started: Combine Claude Code's headless mode (`claude -p` with `--resume`), persistent sprint-state JSON files, and PreToolUse hooks (which you already deployed for skill enforcement) to enforce contract verification gates between tasks.

 

Paste into Claude Code:
 Set up an autonomous sprint runner for my next backend sprint. Create a `sprint-state.json` schema tracking {current_task, contract_status, qa_iterations, commits_pushed, blockers}. Then write a wrapper script that: (1) reads the sprint plan, (2) drafts a contract per task, (3) implements via TDD, (4) runs the QA evaluator subagent, (5) auto-fixes rejections up to 3 iterations, (6) commits and pushes, (7) updates sprint-state.json, and (8) resumes the next task—all without my input. Add PreToolUse hooks that block commits if contract verification fails. Test it on a 3-task sprint and report which steps required human escalation. Copy 

 

 
 

 
Parallel Agents With Reconciliation Guardrails

 
You hit real friction (Tasks 20/21) where parallel automation duplicated Claude's work, requiring reconciliation commits, and Codex research agents orphaned mid-run on R2/R3. A mature parallel-agent setup would shard work by file ownership, share a live task ledger, detect concurrent edits before writing, and fall back gracefully when one agent hangs—turning your 4-6 hour sequential sweeps into 30-minute parallel bursts.

 
 Getting started: Use Claude Code's Agent tool with explicit ownership manifests, a shared `agent-ledger.md` file polled before each Edit, and timeout-based fallback to WebSearch/Context7 when delegated research stalls (a pattern you already discovered manually).

 

Paste into Claude Code:
 Design a parallel-agent orchestrator for my anti-AI-tone refactoring sweeps. Spawn 4 subagents concurrently, each owning a non-overlapping file shard from the S6 widget list. Before any Edit, each agent must (1) acquire a lock in `agent-ledger.md`, (2) verify no other agent has staged changes to that file, and (3) re-read the file to detect external modifications. Add a 5-minute timeout per agent with automatic fallback to a synchronous WebSearch path if a Codex delegation hangs. After all agents finish, run a reconciliation pass that diffs against the original and flags any rule violations (TextStyle migration, unnecessary SizedBox, hardcoded values) before committing. Show me the orchestration code and run it on the next 8 widget files. Copy 

 

 
 

 
Self-Verifying Visual Parity Test Loops

 
The Flutter-vs-HTML button matching session burned 5+ hours and ended in frustration with the mismatch unresolved, and Aqua button gradient/border alignment took multiple sessions. Picture an autonomous visual-parity loop where Claude generates a screenshot, diffs it pixel-by-pixel against the Figma reference, mutates the FigmaDecoration parameters via gradient descent, and iterates until SSIM crosses a threshold—turning subjective 'does this match?' into a measurable convergence problem.

 
 Getting started: Wire flutter-playwright MCP screenshot capture to a Python image-diff harness (PIL/SSIM), have Claude write a parameter-search loop that adjusts border, gradient stops, and shadow sigma, and gate the loop with a numeric pass criterion instead of human judgment.

 

Paste into Claude Code:
 Build an autonomous visual-parity convergence loop for my Figma-to-Flutter button matching. Steps: (1) capture the Figma reference as a PNG via the Figma MCP, (2) render the Flutter widget via flutter-playwright MCP and screenshot it, (3) compute SSIM + per-channel pixel diff, (4) if SSIM < 0.98, identify the worst-diff region, hypothesize which FigmaDecoration parameter is responsible (border width, gradient stop, shadow sigma, color), mutate it, and re-render, (5) repeat up to 20 iterations or until convergence. Log every iteration's parameter delta and SSIM score to `parity-log.md`. Before starting, verify the MCP environment is clean (no stale processes—check for the 45+ orphan issue we hit before). Run it on the Aqua Press Me button and the HTML mockup button that failed last session. Copy 

 

 
 

 

 
 

 
"User snaps in Korean: '다음 세션에 내가 뭐라고 말할지 말해야지!!!!' after Claude forgets the next-session prompt"

 
During a session handoff, Claude delivered a landing summary but skipped the requested next-session prompt template, prompting an exasperated all-caps Korean outburst (roughly: 'You have to tell me what to SAY next session!!!!').

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
  V4 triggers        36 keywords — OK
  V5 placeholders    0 found — OK
  V6 code-fence      0 bare — OK
  V7 plugin-json     v0.4.2 matches marketplace — OK

=== flutter-toolkit ===
  V1 frontmatter     18 skills + 1 agent — OK
  V2 templates       0 files — SKIP (no templates/)
  V3 refs            0 links — OK
  V4 triggers        141 keywords — OK
  V5 placeholders    0 found — OK
  V6 code-fence      0 bare — OK
  V7 plugin-json     v0.5.3 matches marketplace — OK

=== design-kit ===
  V1 frontmatter     8 skills + 1 agent — OK
  V2 templates       8 skipped (ts/js) — OK
  V3 refs            0 links — OK
  V4 triggers        46 keywords — OK
  V5 placeholders    0 found — OK
  V6 code-fence      0 bare — OK
  V7 plugin-json     v0.2.3 matches marketplace — OK

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
  V7 plugin-json     v0.1.3 matches marketplace — OK

=== react-kit ===
  V1 frontmatter     21 skills + 3 agents — OK
  V2 templates       5 parsed, 4 skipped (ts/js) — OK
  V3 refs            0 links — OK
  V4 triggers        157 keywords — OK
  V5 placeholders    0 found — OK
  V6 code-fence      0 bare — OK
  V7 plugin-json     v0.1.3 matches marketplace — OK

=== planning-kit ===
  V1 frontmatter     12 skills + 1 agent — OK
  V2 templates       0 files — SKIP (no templates/)
  V3 refs            0 links — OK
  V4 triggers        95 keywords — OK
  V5 placeholders    0 found — OK
  V6 code-fence      0 bare — OK
  V7 plugin-json     v0.3.1 matches marketplace — OK

=== reflect-kit ===
  V1 frontmatter     3 skills — OK
  V2 templates       0 files — SKIP (no templates/)
  V3 refs            0 links — OK
  V4 triggers        20 keywords — OK
  V5 placeholders    0 found — OK
  V6 code-fence      0 bare — OK
  V7 plugin-json     v0.3.1 matches marketplace — OK

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

