---
phase: 4
title: "Phase 4 harness — 확보된 외부 근거"
collected: 2026-09-24
method: codex (foreground, 직접 호출 · gpt-5.6-sol · 조회는 curl/gh)
inputs: 처리 배정표(.claude/kaizen-input/insights-report.md)의 Phase 4 행 · phase-research-templates.md Phase 4 필수 출처 · 현행화 점검
note: 이 파일이 이 Phase 의 유일한 외부 근거다. 바깥 자료를 새로 찾지 마라. 여기 없는 URL·수치를 지어내지 마라. 없으면 미반영으로 남긴다.
---

읽기 전용으로 조사했으며 파일은 수정하지 않았다. 현재 작업 트리의 기존 변경 2건도 건드리지 않았다.

## 1. 실제 조회한 출처

필수 소스 4종 중 3종 이상을 충족했다.

1. QA 자동화·피드백 루프

   - [Sauce Labs — Beyond Pass/Fail: 3 Strategic Trends that will Define QA in 2026](https://saucelabs.com/resources/blog/beyond-pass-fail-3-strategic-trends-that-will-define-qa-in-2026)
   - [GrowthBook — Feedback loops are the next breakthrough in agentic coding](https://blog.growthbook.io/feedback-loops-are-the-next-breakthrough-in-agentic-coding/)

2. 커뮤니티 스킬 작성 관행

   - [mgechev/skills-best-practices](https://github.com/mgechev/skills-best-practices)

3. 최신 스킬·플러그인·에이전트 계약

   - [Agent Skills specification](https://agentskills.io/specification)
   - [Claude Code Skills](https://code.claude.com/docs/en/skills)
   - [Claude Code Subagents](https://code.claude.com/docs/en/sub-agents)
   - [Claude Code Plugins reference](https://code.claude.com/docs/en/plugins-reference)
   - [Claude Code Hooks](https://code.claude.com/docs/en/hooks)
   - [Claude Code v2.1.281 release](https://github.com/anthropics/claude-code/releases/tag/v2.1.281)

4. 학술 근거

   - [SkillsBench, arXiv 2602.12670](https://arxiv.org/abs/2602.12670)

5. Git 1차 문서

   - [git commit](https://git-scm.com/docs/git-commit)
   - [git worktree](https://git-scm.com/docs/git-worktree)
   - [git merge-base](https://git-scm.com/docs/git-merge-base)

6. 버전 현행화

   - [yq v4.53.6](https://github.com/mikefarah/yq/releases/tag/v4.53.6)
   - [PyYAML 6.0.3](https://github.com/yaml/pyyaml/releases/tag/6.0.3)
   - [npm registry — @playwright/test latest](https://registry.npmjs.org/@playwright%2ftest/latest)

## 2. 항목별 관찰 사실

### `harness:P02`

- 초안 검사는 현재 `project_hash`, `project_name`을 포함한 8개 필드를 요구하지만, 두 값은 이후 반드시 재계산된다: [save-feedback.sh](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/harness/scripts/save-feedback.sh:42), [재계산 위치](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/harness/scripts/save-feedback.sh:206), [최종 재검사](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/harness/scripts/save-feedback.sh:314).
- 따라서 초안 필수 6개와 최종본 필수 8개를 분리하는 제안은 저장본 스키마를 약화시키지 않는다.
- `validate_yaml <file> <required...>`처럼 필수 목록을 호출자가 주입하고, yq/Python 양쪽이 한 목록을 사용하도록 하는 편이 현재 “같은 실패 문구” 규칙과도 맞는다.
- Sprint Contract Step 9는 현재 `skill`, `skill_version`, `project_hash`, 진단 필드만 구체적으로 안내해 `schema_version`, `timestamp`, `outcome`을 놓치기 쉽다: [sprint-contract/SKILL.md](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/harness/skills/sprint-contract/SKILL.md:795).
- 반대 근거: 외부 표준은 이 저장소의 사설 feedback YAML 초안/최종본 구분을 규정하지 않는다. 이 변경의 직접 근거는 외부 문서가 아니라 현재 코드의 생성 순서다.
- 업계 자료는 단순 pass/fail보다 Git 변경, 로그, 생산 신호를 연결하고 사람은 제약·가드레일을 정의하라고 권한다. 이는 최종 저장본의 엄격한 검증을 유지해야 한다는 쪽을 지지한다. 다만 Sauce Labs 글은 벤더 블로그이지 규범적 표준은 아니다. [Sauce Labs](https://saucelabs.com/resources/blog/beyond-pass-fail-3-strategic-trends-that-will-define-qa-in-2026)

### `harness:P07`

- `git commit -o <경로>`는 명시한 경로의 작업 트리 내용을 커밋하고 다른 경로에 staged된 내용을 무시한다. 제안의 핵심 동작을 Git 공식 문서가 직접 뒷받침한다. [git commit `--only`](https://git-scm.com/docs/git-commit)
- 새 파일은 먼저 index에 추가해야 한다는 현재 계약의 설명도 맞다.
- `git worktree`는 같은 저장소에 여러 작업 트리를 두며 `HEAD`, index 같은 per-worktree 파일을 분리한다. 같은 작업 폴더에서 브랜치를 바꾸지 말고 별도 worktree를 만들라는 제안을 직접 지지한다. [git worktree](https://git-scm.com/docs/git-worktree)
- 반대·제약:

  - `-o`는 “소유권”을 판정하지 않는다. 명시한 디렉터리 안에 다른 세션 변경이 섞였다면 함께 커밋할 수 있다.
  - `git diff --cached`는 공용 index를 보여주지만 `commit -o`가 실제로 만들 커밋과 동일하지 않다. 따라서 staged된 남의 파일이 있다는 이유만으로 안전한 `-o` 커밋까지 멈추는 오탐이 생길 수 있다.
  - `git show --stat`의 파일 “수”만 비교하면 같은 수의 다른 파일로 바뀐 경우를 놓친다. 정확한 경로 집합 비교가 필요하다.
- `git merge-base HEAD origin/<base>`는 공식적으로 두 커밋의 best common ancestor를 구한다. “분기점에서 이미 실패했는가”를 가르는 기준으로는 타당하다. [git merge-base](https://git-scm.com/docs/git-merge-base)
- 반대 근거: merge-base는 현재 `origin/<base>` tip의 건강 상태를 뜻하지 않는다. 분기 뒤 base에 실패가 들어왔다면 merge-base는 오래된 green commit일 수 있다. 또한 history가 재작성됐다면 `--fork-point`가 더 적절할 수 있지만 reflog 만료 시 실패할 수 있다. [git merge-base `--fork-point`](https://git-scm.com/docs/git-merge-base)

### `user-setup:P2`

- Worktree 권고와 경로 한정 커밋은 `harness:P07`과 합쳐 한 규칙으로 두는 것이 타당하다.
- 폐기 결정을 핸드오프 재검증 형식에 넣는 것은 외부 표준으로 확인되지 않았다. 내부 F20 재발 방지용 정책으로 명시해야 한다.
- 커밋 전 검사는 다음처럼 구분해야 한다.

  - 전체 index 사고 탐지: `git diff --cached --name-status`
  - 실제 의도 커밋 범위: 명시한 pathspec 집합
  - 사후 확인: `git show --name-status --format='' HEAD`의 경로 집합

- 추론: “D 건수나 내가 안 만든 파일이 index에 있으면 무조건 중단”은 `commit -o`와 함께 쓸 때 지나치게 강하다. 해당 파일이 의도 pathspec과 교차할 때만 차단하고, 교차하지 않으면 경고 후 `-o`로 배제하는 편이 Git 의미와 맞다.

### `other-kits:P10`

- 현재 V10 범위는 `skills/*/SKILL.md`, `agents/*.md`, 최상위 `references/*.md`, `docs/**/*.md`, README뿐이다: [validate-plugin.py](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/scripts/validate-plugin.py:760).
- 직접 전수 측정 결과:

  - `skills/*/references/**/*.md`: 41개
  - 표 행이 있는 파일: 40개
  - 현재 V10 규칙으로 끊긴 표: 0개
  - api-kit: 5개
  - onboarding-kit: 제안서의 2개가 아니라 현재 작업 트리에서는 3개

- V6도 같은 중첩 references를 누락한다: [validate-plugin.py](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/scripts/validate-plugin.py:512).
- 중요 반대 결과: V6 범위를 같은 방식으로 넓히면 즉시 8개 bare fence가 검출된다.

  - [flutter kaizen pr-template](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/flutter-toolkit/skills/flutter-kaizen/references/pr-template.md:32) 2건
  - [contract-kaizen pr-template](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/harness/skills/contract-kaizen/references/pr-template.md:27) 2건
  - [evaluator-kaizen pr-template](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/harness/skills/evaluator-kaizen/references/pr-template.md:27) 2건
  - [harness-kaizen pr-template](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/harness/skills/harness-kaizen/references/pr-template.md:29) 2건

- 따라서 V10 확장은 회귀 없이 가능하지만 V6 확장은 “범위만 추가”하면 현재 레포를 실패시킨다. 8개 수정과 같은 커밋에서 활성화하거나, 명시적 grace period가 필요하다.

### `insights:scope-commit-block`

- Claude Code `PreToolUse` 훅은 도구 실행 전에 차단할 수 있고, command hook에서 exit 2가 코드만으로 차단하는 표준 경로다. `PostToolUse`는 이미 실행된 동작을 되돌릴 수 없다. [Claude Code Hooks](https://code.claude.com/docs/en/hooks)
- 현재 commit guard는 path argument가 있는 비-`--include` 커밋을 안전한 것으로 보고 즉시 반환한다: [commit-guard.sh](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/harness/scripts/commit-guard.sh:160). 범위 차단을 추가한다면 이 반환보다 앞에서 검사하거나 별도 훅으로 두어야 한다.
- 현재 계약에는 diff-scope 표준형이 있지만 commit hook이 안정적으로 읽을 수 있는 허용 경로 SSOT는 없다: [sprint-contract/SKILL.md](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/harness/skills/sprint-contract/SKILL.md:56).
- 추론: 첫 계약은 차단 훅 구현보다 “어느 active sprint의 어떤 pathspec이 허용 범위인가”를 명시하는 것이다. 병렬 계약이 있으므로 plain 전역 목록 하나는 부적합하다.

### `F08`

- 다른 세션 커밋을 되돌린 사고에 대해 `commit -o <정확한 경로>`는 staged된 타 세션 변경을 제외한다는 공식 근거가 있다. [git commit](https://git-scm.com/docs/git-commit)
- 다만 오래된 공용 파일 내용을 명시 경로에 포함했다면 `-o`도 되돌림을 막지 못한다. 커밋 전 `HEAD` 대비 해당 경로 diff와 정확한 파일 집합 검사가 별도로 필요하다.

### `F09`

- 작업 트리 분리는 Git이 제공하는 정식 기능이다. [git worktree](https://git-scm.com/docs/git-worktree)
- Claude Code 최신 subagent에도 `isolation: worktree`가 있으며, 기본적으로 부모 `HEAD`가 아니라 default branch에서 임시 worktree를 만든다. 이는 수동 `git worktree add <검사 통과 커밋>`과 base 선택 의미가 다르므로 혼용하면 안 된다. [Claude Code Subagents](https://code.claude.com/docs/en/sub-agents)
- 기준 실패 가르기는 “분기점 상태”와 “현재 target branch 상태”를 별도로 기록해야 한다.

### `F14`

- 반복된 feedback draft 거부의 직접 원인은 현재 초안 검사와 스크립트 생성 필드가 충돌하는 데 있다.
- `harness:P02`대로 초안 6개/최종 8개로 분리하고 Sprint Contract에 6개를 전부 열거하면 해결 방향이 일치한다.
- QA evaluator의 “미리 맞추려 애쓰지 마라” 설명은 이미 이 동작을 전제한다: [qa-evaluator.md](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/harness/agents/qa-evaluator.md:1046).

### `F18`

- V10 중첩 references 확장은 표 파손 탐지 공백을 없앤다. 현재 41개에서는 파손 0건이다.
- YAML 파손은 이 제안으로 해결되지 않는다. V2는 `templates/` 아래 JSON/YAML/TOML만 파싱한다: [validate-plugin.py](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/scripts/validate-plugin.py:230).
- 추론: Markdown의 모든 `yaml` fence를 일괄 파싱하면 `{placeholder}`나 생략 예시 때문에 오탐이 생길 수 있다. “실행 가능한 YAML”이라고 표시된 블록이나 실제 산출 파일만 검사 대상으로 구분해야 한다.

### `F28`

- 준비용 worktree와 커밋 전 검사는 Git 및 Claude hook이 공식 지원한다. [git worktree](https://git-scm.com/docs/git-worktree), [Claude Code Hooks](https://code.claude.com/docs/en/hooks)
- 현재 대량 삭제와 일부 되돌림은 commit guard가 다루지만 범위 밖 경로, worktree 상태, 기준 테스트 비교는 다루지 않는다.
- 별도 상태 스크립트에 대한 외부 권고는 이번 조회에서 찾지 못했다. 기능을 추가한다면 내부 사고에 대응하는 저장소 정책으로 분류해야 한다.

## 3. 현행화 — 낡은 곳

| 파일:줄 | 현재 값 | 최신 값·판정 | 출처 |
|---|---|---|---|
| [agent-design-guide.md:70](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/harness/docs/guides/agent-design-guide.md:70) | 공식 frontmatter 15종 | 현재 표는 18종. `omitClaudeMd`, `initialPrompt`, `experimental`이 추가되어 있음 | [Claude Code Subagents](https://code.claude.com/docs/en/sub-agents) |
| [agent-design-guide.md:95](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/harness/docs/guides/agent-design-guide.md:95) | `initialPrompt`는 공식 필드가 아님 | 현재 공식 선택 필드. 단 plugin subagent에서는 무시됨 | [Claude Code Subagents](https://code.claude.com/docs/en/sub-agents), [Plugins reference](https://code.claude.com/docs/en/plugins-reference) |
| [agent-design-guide.md:59](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/harness/docs/guides/agent-design-guide.md:59) | `--agents`가 최고 우선순위 | managed settings가 1위, `--agents` 2위, project 3위, user 4위, plugin 5위 | [Claude Code Subagents](https://code.claude.com/docs/en/sub-agents) |
| [agent-design-guide.md:79](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/harness/docs/guides/agent-design-guide.md:79), [create-agent/SKILL.md:25](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/harness/skills/create-agent/SKILL.md:25) | model 생략 시 `inherit` | 최신 문서는 생략 시 “subagent model order로 선택”한다고 규정 | [Claude Code Subagents](https://code.claude.com/docs/en/sub-agents) |
| [create-skill/SKILL.md:27](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/harness/skills/create-skill/SKILL.md:27), [skill-design-guide.md:393](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/harness/docs/guides/skill-design-guide.md:393) | “공식 필수는 name+description” | Agent Skills 표준에서는 맞다. 그러나 Claude Code 런타임은 모든 필드를 선택으로 보고 `description`만 권장하며 name은 디렉터리명으로 대체한다. “표준”과 “Claude Code 런타임”을 구분해야 함 | [Agent Skills specification](https://agentskills.io/specification), [Claude Code Skills](https://code.claude.com/docs/en/skills) |
| [create-skill/SKILL.md:29](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/harness/skills/create-skill/SKILL.md:29) | `argument-hint` 누락은 discovery 실패 | 최신 공식 문서는 autocomplete 힌트라고만 규정한다. 자동 discovery는 description/when_to_use가 담당한다 | [Claude Code Skills](https://code.claude.com/docs/en/skills) |
| [skill-design-guide.md:806](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/harness/docs/guides/skill-design-guide.md:806) | Claude 전용 필드가 다른 플랫폼에서 무시됨 | 모든 비표준 플랫폼이 안전하게 무시한다는 보장은 Agent Skills 스펙에 없음. Claude Code의 비표준 필드라는 사실까지만 확인됨 | [Agent Skills specification](https://agentskills.io/specification), [Claude Code Skills](https://code.claude.com/docs/en/skills) |
| [package.json:27](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/package.json:27) | `@playwright/test ^1.58.2`, lock 1.58.2 | 최신 조회값 1.63.0 | [npm registry](https://registry.npmjs.org/@playwright%2ftest/latest) |

추가 버전 현황:

- Claude Code 최신 안정 릴리스는 조회 시점 `2.1.281`; 로컬 실행본은 `2.1.268`이었다. 저장소에는 최소 Claude Code 버전 선언이 없다. [v2.1.281](https://github.com/anthropics/claude-code/releases/tag/v2.1.281)
- yq 최신 조회값은 `4.53.6`, PyYAML은 `6.0.3`이다. 저장소는 둘의 버전을 pin하지 않으므로 “낡은 버전”으로 찍을 파일은 없다. [yq](https://github.com/mikefarah/yq/releases/tag/v4.53.6), [PyYAML](https://github.com/yaml/pyyaml/releases/tag/6.0.3)
- 이번 조회에서 harness가 사용하는 yq/PyYAML의 새로운 폐기 항목이나 이 변경을 깨는 breaking change는 확인하지 못했다.
- create-agent의 “plugin agent는 hooks/mcpServers/permissionMode를 지원하지 않는다”는 최신 문서와 일치하므로 낡지 않았다. [Plugins reference](https://code.claude.com/docs/en/plugins-reference)

## 4. Phase 4 계약 권장안

1. `save-feedback.sh` 계약

   - `validate_yaml <file> <required-field...>` 형태로 변경.
   - 초안 필수는 정확히 6개: `schema_version`, `skill`, `timestamp`, `skill_version`, `outcome`, `diagnosis`.
   - 최종 임시본은 기존 8개를 유지.
   - yq/Python은 동일한 정렬·따옴표·문구의 누락 목록을 출력.
   - Sprint Contract Step 9에 6개를 그대로 열거하고 `project_*`는 쓰지 않아도 된다고 명시.

2. 커밋 계약

   - 기본 커밋 형태는 `git commit -o -- <정확한 내 경로...>`.
   - 새 파일만 사전에 `git add -- <파일>` 수행.
   - `git add -A`, `git commit -a`, `git commit -i` 금지.
   - 커밋 전에는 전체 index 경고와 의도 pathspec 검사를 구분.
   - 커밋 후 파일 “수”가 아니라 `git show --name-status --format='' HEAD`의 정확한 경로 집합을 선언 목록과 비교.

3. Worktree 계약

   - 병렬 흔적과 복수 커밋 예상이 함께 있을 때 별도 worktree를 사용.
   - 기준 commit-ish는 “검사가 통과한 것으로 실제 확인된 SHA”로 기록.
   - 같은 worktree에서 `checkout -b`하지 않는다는 문구를 sprint-contract와 skill-design-guide §9에 공통화.
   - Claude의 `isolation: worktree`는 default branch 기반이라는 별도 의미를 명시해 수동 worktree와 혼동하지 않게 함.

4. 기준 실패 가르기 계약

   하나의 SHA만 모든 의미에 쓰지 말고 두 기준을 구분하는 것이 안전하다.

   - `FORK_BASE=$(git merge-base HEAD origin/<base>)`: 내 변경이 시작된 분기점
   - `TARGET_BASE=origin/<base>`: 현재 합칠 대상의 상태
   - 같은 실패 테스트를 둘 다 임시 worktree에서 실행.
   - `FORK_BASE`에서도 실패: 내 작업 이전 실패 가능성.
   - `FORK_BASE` 통과, `TARGET_BASE` 실패: base가 분기 후 깨진 경우.
   - 둘 다 통과, HEAD 실패: 내 변경 원인 가능성이 높음.
   - 실행한 테스트 이름, SHA, exit code를 기록.

5. 범위 밖 커밋 차단

   - scope의 SSOT를 먼저 정한다.
   - 권장: active Sprint Contract와 1:1인 `sprint-scope-<slug>` 산출물에 NUL 안전 또는 한 줄당 하나의 Git pathspec으로 저장하고 계약 봉인에 포함.
   - PreToolUse commit hook은 commit 명령의 실제 pathspec과 허용 집합을 비교해 교집합 밖 경로가 있으면 exit 2.
   - scope 파일 부재·파싱 실패 시 조용히 허용하지 말고 “검사 불가”를 보여주되, 초기 도입 grace period 여부는 계약에서 별도 결정.
   - 기존 path-commit 조기 반환보다 앞에서 검사.

6. V10/V6

   - V10에 `skills/*/references/**/*.md`를 추가해도 현재 전수 결과는 끊긴 표 0건.
   - V6에도 같은 범위를 쓰되 현재 8개 bare fence를 먼저 또는 동시에 고친 뒤 blocking 활성화.
   - api-kit 5개, onboarding-kit 3개로 현재 실제 개수를 계약 oracle에 사용.
   - 파일 수를 상수로 고정하기보다 검사 실행 시 대상 수 `> 0`과 열거 목록을 출력.

7. 스킬 검증 현행화

   - “Agent Skills 표준 필수”, “Claude Code 런타임”, “이 레포 정책”을 세 열로 분리.
   - negative trigger는 mgechev 커뮤니티 권장 패턴이며 공식 Claude schema 필수는 아니다. [mgechev](https://github.com/mgechev/skills-best-practices), [Claude Code Skills](https://code.claude.com/docs/en/skills)
   - SkillsBench 결과는 curated skill 유무를 짝지어 검증하고, 집중된 작은 스킬이 큰 묶음보다 좋았다고 보고한다. Phase 4에서도 변경 전후 fixture를 같은 harness 조건으로 비교하는 계약이 적합하다. [SkillsBench](https://arxiv.org/abs/2602.12670)

## 5. 못 가져온 것 / 열린 질문

- “Plugin 검증 스키마 최신 2026”이라는 이름의 신뢰할 만한 별도 커뮤니티 표준 저장소는 찾지 못했다. 대신 최신 Claude Code 공식 schema와 `claude plugin validate` 계약을 조회했다. 별도 커뮤니티 스키마가 존재하지 않는다는 뜻은 아니다.
- VTest의 2026 agentic testing 글은 서버가 HTTP 525를 반환해 가져오지 못했다.
- 폐기 결정 기록 위치에 대한 외부 표준은 찾지 못했다. Sprint handoff/contract 내부 정책으로 결정해야 한다.
- 범위 선언을 contract frontmatter에 둘지 별도 scope 파일에 둘지는 아직 열린 설계 선택이다. 현재 셸 reader가 scalar 중심이므로 YAML 배열을 frontmatter에 바로 넣으면 파서 확장 비용이 생긴다.
- `git merge-base` 하나만 기준으로 고정할지는 재검토가 필요하다. 분기점과 현재 target tip은 서로 다른 질문에 답한다.
- Playwright 1.58.2→1.63.0 사이의 구체적인 breaking change·폐기 목록은 이번 stop 조건 범위에서 추가 조회하지 않았다. 최신 버전 차이만 확인했다.
