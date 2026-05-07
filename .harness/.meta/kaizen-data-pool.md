# Kaizen Data Pool

Generated: 2026-05-07T23:01:39
Generator: `scripts/collect-kaizen-data.py`

카이젠 오케스트레이션의 Phase 별 서브에이전트가 참조할 통합 데이터 풀이다. 이 파일은 `scripts/collect-kaizen-data.py` 로 재생성된다 — 수동 수정 금지.

## 0. `/insights` Report (외부 도구 산출물)

- 경로: `/Users/jackson/.claude/usage-data/report-ko.html` · HTML 추출 텍스트
- 최근 갱신: 2026-05-07T23:00:56 ✓ VERY FRESH (0.0시간 전)
- 모든 Phase 서브에이전트가 **최우선** 참조해야 한다 (Friction Points / Recommended Patterns / Feature Suggestions / 이번 사이클 신규 워크플로우 제안)

<details><summary>insights report 본문 (auto-extracted)</summary>

Claude Code 인사이트 (한국어) 
 

 
 
 
 

 
Claude Code 인사이트

 
130개 세션에서 2,391개 메시지 (전체 827) | 2026-04-14 ~ 2026-05-07

 

 
한눈에 보기

 

 
 잘 되고 있는 것: 매우 규율 잡힌 운영을 하고 있습니다. 계약(Contract) → QA → 푸시 스프린트 사이클을 짧은 확인('ㄱㄱ')으로 굴리고, 명시적 세션 핸드오프 문서로 며칠에 걸친 다단계 작업을 이어갑니다. Claude가 무언가를 놓쳤을 때 그 자리에서 패치만 하는 게 아니라 규칙 파일, 스킬, 훅 기반 강제까지 코드로 박아넣어 모든 마찰 지점을 영구적인 레버리지로 바꿉니다. 인상적인 작업 → 

 
 걸림돌이 되는 것: Claude 측: 과욕적 범위 확장(허락 없는 삭제, 요청 안 한 디자인 선택), 규칙 기반 리팩터링에서 사전 점검 체크리스트를 건너뛰는 경향. 사용자 측: 긴 세션이 출력 토큰 한도, MCP/에이전트 멈춤, 병렬 자동화 충돌로 탈선. 스프린트 시작 전 30초 브랜치/프로세스 사전 점검만 해도 막을 수 있습니다. 문제가 발생하는 지점 → 

 
 바로 시도할 퀵윈: 스프린트 워크플로우를 /sprint 스킬로 승격하여 contract-QA-push 루프를 매번 다시 설명하지 않게 하고, 편집 전 anti-AI-tone 체크리스트를 로드하는 /refactor-widget 스킬과 짝지으세요. 브랜치가 origin에서 벗어났거나 좀비 MCP 프로세스가 있을 때 편집을 차단하는 PreToolUse 훅으로 세션을 잡아먹는 패턴을 막을 수 있습니다. 시도해볼 기능 → 

 
 야심찬 워크플로우: 모델이 강해질수록 계약 기반 사이클은 몇 시간 동안 무인으로 돌아가야 합니다 — 계약 작성, TDD 실행, 리베이스 복구, 영구 state 파일을 통한 컨텍스트 경계 넘어 재개. 5시간 이상을 태운 Flutter–Figma parity 작업이 최고 레버리지 타깃입니다. 스크린샷, Figma와 픽셀 diff, FigmaDecoration 파라미터를 SSIM 수렴까지 자동 조정하는 자가검증 루프는 가장 고통스러운 세션을 측정 가능한 최적화 문제로 바꿔줍니다. 앞으로의 가능성 → 

 

 

 

 
 작업 영역 
 CC 사용 방식 
 인상적인 작업 
 문제 지점 
 시도할 기능 
 새 사용 패턴 
 앞으로의 가능성 
 팀 피드백 
 

 

 

2,391

메시지

 

+92,817/-11,678

라인

 

1047

파일

 

18

일수

 

132.8

일평균 메시지

 

 
작업 영역

 

 
 

 

 Schedule-Vote 백엔드 (Rust) 
 ~12 세션 
 

 
친구 전용 피트니스 스케줄링 MVP의 멀티 스프린트 백엔드 개발. 서브에이전트 오케스트레이션과 계약 기반 TDD로 Task 1-22 실행. Claude는 QA 사이클, Sentry 통합, ReminderJob/ResolutionJob 구현, 통합 테스트 수정을 처리하고 dev 브랜치에 다수의 커밋을 리베이스 푸시했습니다.

 

 

 

 Flutter UI 리팩터링 & Anti-AI-Tone 규칙 
 ~15 세션 
 

 
i18n locale key 추출과 함께 프로젝트 스타일 규칙을 따르는 admin 위젯, messagebox 컴포넌트, carousel/toolbar 위젯의 체계적 리팩터링. Edit 도구 기반 반복 작업이 많았고 Claude가 Stack vs Column 선택, TextStyle 마이그레이션, 오버엔지니어링에서 사용자 교정을 자주 요구하여, 피드백 로그에 새 규칙들이 문서화되었습니다.

 

 

 

 Figma-Flutter 디자인 패리티 
 ~8 세션 
 

 
Aqua 버튼 그래디언트, FigmaDecoration per-side 보더, skeuomorphic CSS 매칭을 포함한 Figma 디자인과 Flutter 구현의 픽셀 단위 일치 작업. QA 검증 포함 5개 스킬로 구성된 figma-flutter-kit 제작. MCP 디바이스 설정과 시각적 불일치로 인한 마찰이 자주 발생하여 다회 반복이 필요했습니다.

 

 

 

 Flutter MCP 재설계 & 애니메이션 엔진 
 ~7 세션 
 

 
영구 연결 인디케이터를 포함한 Observer-only 아키텍처로의 Flutter MCP 서버 다단계 재설계 및 Sprint 5 force-layout 알고리즘 벤치마킹(d3-main 어댑터 선정). 병렬 리서치/리뷰에 Codex를 활용했으나 일부 리서치 에이전트가 멈추거나 부정확한 주장을 반환하여 사용자 교정이 필요했습니다.

 

 

 

 Worldbuilding IDE & 그룹 초대 기획 
 ~6 세션 
 

 
ID 검색 기반 그룹 초대 기능과 worldbuilding IDE 피벗 같은 신기능에 대한 디자인 스펙, 스프린트 계약, 13-task 구현 계획을 만든 전략적 기획 세션. Claude가 핸드오프 문서를 포함한 QA 검증 완료 계획을 전달했지만, 빠른 반복을 원할 때 공식 디스커버리 프로세스를 과도하게 적용한 경우가 있었습니다.

 

 
 

 

 

 

 
요청한 작업 유형

 

 
코드 리팩터링

 

 
46

 

 
코드 설명

 

 
22

 

 
기능 구현

 

 
20

 

 
세션 핸드오프

 

 
15

 

 
리팩터링

 

 
12

 

 
문서 업데이트

 

 
12

 

 

 

 
자주 사용한 도구

 

 
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

 

 

 

 

 

 
언어

 

 
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

 

 

 

 
세션 유형

 

 
멀티 태스크

 

 
41

 

 
반복 개선

 

 
28

 

 
단일 태스크

 

 
11

 

 
간단한 질문

 

 
3

 

 
탐색

 

 
2

 

 

 

 
Claude Code 사용 방식

 

 
당신은 길고 다단계인 엔지니어링 캠페인을 굴리는 고처리량 기술 디렉터 입니다. 세션은 마라톤급 길이(130 세션 평균 11시간, 168 커밋)이며 공식 산출물 — 스프린트 계약, Phase 체크포인트, QA APPROVE 사이클, 다음 세션을 위한 명시적 핸드오프 프롬프트 — 을 중심으로 구조화되어 있습니다. 서브에이전트, Codex 리서치 태스크, 병렬 자동화로 적극적으로 위임하고, Claude가 계약→구현→QA→푸시 사이클을 자율적으로 돌리기를 기대합니다. 확인은 보통 짧고('ㄱㄱ' / 'go'), 스펙은 사전 로드해두고 손 안 대는 실행을 원한다는 신호를 줍니다.

자율적인 틀에도 불구하고, Claude가 표류할 때 매섭게 끼어들고 교정합니다 . Claude가 명백한 개선(레거시 `bodyMSemiBold` 마이그레이션, 불필요한 null 분기, 하드코드된 값)을 놓치거나, Column이면 충분한데 Stack을 쓰거나, 검증 없이 Figma 텍스트 스타일 이름을 만들어내면 짜증이 폭발합니다. 반응이 격해지고 — '다음 세션에 내가 뭐라고 말할지 말해야지!!!!' — 그 인스턴스를 고치는 데 그치지 않고 영구 프로젝트 규칙으로 코드화합니다. 이 규칙을 산출물로 만드는 패턴 (anti-AI-tone 리팩터링 스윕, 피드백 로그, 스킬 사용을 강제하는 PreToolUse 훅)은 모든 마찰 지점을 일회성이 아닌 시스템적 갭으로 보고 닫는다는 것을 보여줍니다.

어려운 문제의 반복은 참아주지만(Flutter/HTML 버튼 매칭에 5시간 이상, Parity/Consolidation 계약 3회 수정), 프로세스 위반 에는 인내심이 끊어집니다 — 허락 없는 편집, 과도한 주석, 오버엔지니어링, 명시적 지시 없이 Claude가 앞서가는 행위. 모멘텀이 필요할 때는 잘못된 이분법과 공식 디스커버리 오버헤드도 거부합니다. 인프라 중심의 도구 사용량(Bash 4,686회, TodoWrite 443회, Agent 호출 381회)은 Claude를 페어 프로그래밍 파트너가 아닌 관리형 인력으로 오케스트레이션하고 있음을 확인해줍니다.

 
 핵심 패턴: 공식 계약과 QA 게이트를 갖춘 자율 스프린트 실행자로 Claude를 운영하지만, 일회성 실수를 영구 프로젝트 규칙으로 승격하여 표류를 매섭게 교정합니다.

 

 

 
 

 
사용자 응답 시간 분포

 

 
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

 

 

 중앙값: 77.3초 • 평균: 229.6초
 

 

 
 

 
멀티 클로딩 (병렬 세션)

 

 

 
191

 
중첩 이벤트

 

 

 
116

 
관련 세션

 

 

 
56%

 
메시지 비중

 

 

 

 여러 Claude Code 세션을 동시에 실행하고 있습니다. 멀티 클로딩은 세션이 시간상 중첩될 때 감지되며,
 병렬 워크플로우를 시사합니다.
 

 

 
 

 

 

 시간대별 사용자 메시지
 
 PT (UTC-8) 
 ET (UTC-5) 
 London (UTC) 
 CET (UTC+1) 
 Tokyo (UTC+9) 
 사용자 지정 오프셋... 
 
 
 

 

 

 
아침 (6-12)

 

 
416

 

 

 
오후 (12-18)

 

 
1250

 

 

 
저녁 (18-24)

 

 
647

 

 

 
새벽 (0-6)

 

 
78

 

 

 

 
발생한 도구 오류

 

 
기타

 

 
308

 

 
명령 실패

 

 
135

 

 
사용자 거부

 

 
38

 

 
파일 없음

 

 
20

 

 
파일 변경됨

 

 
19

 

 
편집 실패

 

 
8

 

 

 

 
인상적인 작업

 
Flutter, Rust 백엔드, 디자인 시스템에 걸친 130 세션에서 강력한 핸드오프 위생을 갖춘 매우 규율 잡힌 계약 기반 개발 관행을 운영하고 있습니다.

 

 

 
계약-QA-푸시 스프린트 사이클

 
계약 → 구현 → QA APPROVE → 커밋/푸시 루프를 엄격하게 굴리며, 여러 스프린트에 걸쳐 13개 이상의 태스크를 전체 QA 승인으로 마무리합니다(예: 백엔드 Task 1-13 schedule-vote MVP, Sprint 5 Task 4-9를 짧은 'ㄱㄱ' 확인으로). 스킬 사용을 강제하는 PreToolUse 훅까지 설치한 것은 프로세스 준수를 1급 엔지니어링 관심사로 취급한다는 증거입니다.

 

 

 
규율 잡힌 세션 핸드오프

 
15개의 명시적 session_handoff 목표가 포착되었습니다. 컨텍스트 연속성을 산출물로 취급하며, 다음 세션 프롬프트 템플릿, 종합 핸드오프 문서, 마무리 전 깔끔한 커밋 경계를 요구합니다. 이를 통해 장기 다단계 작업(Phase A→B→C MCP 재설계, 멀티 스프린트 백엔드)을 세션 간 모멘텀 손실 없이 이어갑니다.

 

 

 
피드백을 규칙으로 코드화

 
Claude가 리팩터링 기회를 놓치거나 스타일 규칙을 잘못 해석할 때, 그 자리에서만 고치지 않고 프로젝트 문서, anti-AI-tone 규칙 파일, 스킬 업그레이드로 교훈을 푸시합니다(예: method-vs-class 추출 규칙을 3개 문서에 추가, 반복 후 리스트 빌딩 패턴 코드화). 모든 마찰 지점을 미래 세션의 영구 레버리지로 바꿉니다.

 

 

 

 

 

 
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

