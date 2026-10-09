# EX-2 — Codex 원문 대조 (2026-09-26, gpt-5.6-sol, 읽기 전용)

## 물은 것

확인할 것:
- 에이전트 frontmatter 에서 model 을 생략하면 어떻게 되는가(부모 모델 상속인지 기본값인지)
- 같은 이름 에이전트가 여러 곳에 있을 때 우선순위(managed settings · 프로젝트 · 사용자 · 플러그인 등) 순서 원문
- omitClaudeMd 필드가 있는가와 뜻, experimental 표시가 무엇을 뜻하는가
- 서브에이전트 동시 실행 상한이나 중첩 제한에 관한 오류 문구가 있으면 원문과 어느 상한인지

저장소 근거(읽어서 무엇을 주장했는지 먼저 확인):
- /Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0926b/.harness/.meta/evidence/phase4.md 147~150행
- /Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0926b/.harness/.meta/evidence/phase1.md 86행

원문: https://code.claude.com/docs/en/sub-agents

## 답

## 1. 출처 목록

가져온 날짜는 모두 **2026-09-26 (Asia/Seoul)**입니다.

- Anthropic 공식 문서: [Create custom subagents](https://code.claude.com/docs/en/sub-agents)
- 저장소 근거: [phase4.md:147](</Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0926b/.harness/.meta/evidence/phase4.md:147>)
- 저장소 근거: [phase1.md:86](</Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0926b/.harness/.meta/evidence/phase1.md:86>)

파일은 변경하지 않았다.

## 2. 질문별 확인

### 2.1 `model` 생략 시 동작

- 원문 발췌: “When you omit it … subagent model order” ([공식 문서](https://code.claude.com/docs/en/sub-agents))
- 공식 선택 순서:
  1. 호출별 `model` 인자
  2. 에이전트 frontmatter의 `model`
  3. `CLAUDE_CODE_SUBAGENT_MODEL`
  4. 메인 대화 모델
- 따라서 frontmatter만 생략했다고 곧바로 `inherit`와 완전히 같은 것은 아니다. 호출별 지정이나 환경변수가 있으면 그것이 먼저 적용되고, 둘 다 없을 때 부모 모델에 도달한다.
- 저장소 주장: [phase4.md:150](</Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0926b/.harness/.meta/evidence/phase4.md:150>)은 기존의 “생략 시 `inherit`”를 낡은 설명으로 분류하고, 현재는 model order로 선택한다고 적었다.
- 판정: **맞음.** 기존 “생략 = `inherit`” 표현은 현재 원문 기준으로는 지나친 단순화다.

### 2.2 같은 이름 에이전트의 우선순위

- 원문 발췌: “higher-priority location” ([공식 문서](https://code.claude.com/docs/en/sub-agents))
- 공식 표의 순서:
  1. Managed settings
  2. `--agents`
  3. 프로젝트 `.claude/agents/`
  4. 사용자 `~/.claude/agents/`
  5. 플러그인의 `agents/`
- 저장소 주장: [phase4.md:149](</Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0926b/.harness/.meta/evidence/phase4.md:149>)과 순서가 동일하다.
- 판정: **맞음.**
- 추가 원문 사항: 중첩된 여러 프로젝트 `.claude/agents/` 사이에서는 현재 작업 디렉터리에 가장 가까운 정의가 이긴다. 같은 디렉터리 트리 안의 동명 파일은 파일시스템 읽기 순서로 하나가 선택되며, 문서화된 우선순위는 없다.

### 2.3 `omitClaudeMd`와 `experimental`

- `omitClaudeMd` 원문 발췌: “without … CLAUDE.md files” ([공식 문서](https://code.claude.com/docs/en/sub-agents))
- 뜻: `true`이면 사용자·프로젝트·로컬 `CLAUDE.md`를 제외한다. 일반 에이전트에는 managed policy가 계속 들어가지만, managed settings에서 정의된 에이전트는 그것도 로드하지 않는다. `--agent` 또는 `agent` 설정으로 메인 세션 에이전트가 된 경우에는 무시된다. Claude Code v2.1.271 이상이 필요하다.
- `experimental` 원문 발췌: “Map of experimental options.” ([공식 문서](https://code.claude.com/docs/en/sub-agents))
- 뜻: 현재 문서상 `cacheTtl: 5m | 1h`를 지정하는 맵이다. 다른 값은 무시되며, subagent 파일에서만 읽는다. Claude Code v2.1.248 이상이 필요하다.
- 저장소 주장: [phase4.md:147](</Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0926b/.harness/.meta/evidence/phase4.md:147>)과 [phase1.md:86](</Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0926b/.harness/.meta/evidence/phase1.md:86>)은 공식 표가 18종이며 `omitClaudeMd`, `initialPrompt`, `experimental`이 포함된다고 주장한다.
- 판정: **맞음.** 실제 표에는 18개 필드가 있다.
- 추론: `experimental`은 에이전트 전체를 “실험적 상태”라고 표시하는 일반 플래그가 아니라, 현재는 실험 옵션인 `cacheTtl`을 담는 별도 맵이다. “experimental이면 API가 불안정하다” 같은 의미는 원문에 없다.

### 2.4 동시 실행·중첩 제한과 오류 문구

- 중첩 원문 발췌: “up to three layers” ([공식 문서](https://code.claude.com/docs/en/sub-agents))
- 기본 중첩 상한은 메인 대화 아래 **3개 서브에이전트 층**이다. `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH`로 변경할 수 있다.
- 일반 서브에이전트가 깊이 상한에 도달하면 `Agent` 도구가 제공되지 않는다. fork에는 도구가 남지만 호출하면 오류가 난다. **그 오류의 정확한 문자열은 이 페이지에 없다.**
- 동시 실행 오류 원문: “`Concurrent subagent limit reached`” ([공식 문서](https://code.claude.com/docs/en/sub-agents))
- 이 오류는 **세션에서 이미 20개가 실행 중인 상태에서 Agent 도구로 하나를 더 spawn할 때** 발생하는 기본 동시 실행 상한 오류다. 세션 누적 spawn 수의 상한이 아니다.
- `CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS`로 양의 정수로 변경할 수 있으며, ultracode 세션에는 적용되지 않는다. 문서는 세션 전체 누적 spawn 수에는 제한이 없다고 명시한다.
- 저장소 주장: 지정된 [phase1.md:86](</Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0926b/.harness/.meta/evidence/phase1.md:86>)에는 제한 주장이 없고 frontmatter 개수만 적혀 있다. 다만 같은 파일의 현재 90행에는 동시 20·깊이 3·누적 무제한·ultracode 예외가 적혀 있으며 공식 원문과 일치한다.
- 판정: **제한 내용은 맞음.** 단, 요청에서 지목한 86행은 해당 근거 위치가 아니다. 중첩 제한의 정확한 오류 문구는 **원문에 없음**이다.

## 3. 저장소에 반영할 문장 제안

- `model`을 생략하면 호출별 지정 → frontmatter → `CLAUDE_CODE_SUBAGENT_MODEL` → 메인 대화 모델 순으로 결정되므로, 생략을 곧바로 `inherit`와 동일시하지 않는다.
- 동명 에이전트 우선순위는 managed settings → `--agents` → 프로젝트 → 사용자 → 플러그인 순이다.
- `omitClaudeMd: true`는 사용자·프로젝트·로컬 `CLAUDE.md`를 제외하며, `experimental`은 현재 `cacheTtl` 옵션을 담는 맵이다.
- 기본 제한은 동시 실행 20개와 메인 대화 아래 중첩 3층이며, 세션 누적 spawn 수에는 제한이 없다.
- `Concurrent subagent limit reached`는 세션 누적량이 아니라 현재 실행 중인 서브에이전트 수가 기본 20개에 도달했을 때의 오류다.

## 4. 못 가져온 것 / 열린 질문

- 지정된 HTML 원문 페이지는 정상적으로 가져왔으므로 `curl` 재시도는 필요하지 않았다.
- 중첩 깊이 상한에서 fork가 받는다는 오류의 **정확한 문자열**은 해당 공식 페이지에서 찾지 못했다.
- `experimental`이라는 이름이 안정성이나 향후 호환성에 관해 무엇을 보장하는지는 원문에 설명되어 있지 않다.
- 요청에 적힌 `phase1.md:86`은 현재 파일에서 제한 관련 행이 아니라 frontmatter 18종 관련 행이다. 제한 관련 주장의 실제 현재 위치는 90행이다.