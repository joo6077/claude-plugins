# EX-3 — Codex 원문 대조 (2026-09-26, gpt-5.6-sol, 읽기 전용)

## 물은 것

확인할 것:
- SKILL.md frontmatter 필수 필드가 무엇인가 — Agent Skills 표준 쪽과 Claude Code 쪽을 따로
- 표준에 없는 필드(user-invocable, argument-hint 등)를 런타임이 무시한다는 보장이 문서에 있는가

저장소 근거(읽어서 무엇을 주장했는지 먼저 확인):
- /Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0926b/.harness/.meta/evidence/phase4.md 151~153행

원문: https://code.claude.com/docs/en/skills , https://agentskills.io/specification

## 답

## 1. 출처 목록

가져온 날짜: **2026-09-26 (Asia/Seoul)**

- [저장소 근거 phase4.md 151행](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0926b/.harness/.meta/evidence/phase4.md:151)
- [저장소 근거 phase4.md 152행](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0926b/.harness/.meta/evidence/phase4.md:152)
- [저장소 근거 phase4.md 153행](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0926b/.harness/.meta/evidence/phase4.md:153)
- [Claude Code Skills 문서](https://code.claude.com/docs/en/skills) — 2026-09-26
- [Agent Skills specification](https://agentskills.io/specification) — 2026-09-26

## 2. 질문별 판정

### A. Agent Skills 표준의 필수 frontmatter 필드

- 원문 인용: “The required `name` field”, “The required `description` field”
- 원문 URL: [Agent Skills specification](https://agentskills.io/specification)
- 가져온 날짜: 2026-09-26
- 확인 결과: 필수 필드는 `name`, `description` 두 개다. `license`, `compatibility`, `metadata`, `allowed-tools`는 선택 필드다.
- 저장소 원 주장: “공식 필수는 name+description”
- 판정: **맞음 — 단, Agent Skills 표준에 한정해야 함.**
- phase4.md 151행의 “표준과 Claude Code 런타임을 구분해야 한다”는 정정도 **맞음**.

### B. Claude Code 런타임의 필수 frontmatter 필드

- 원문 인용: “All fields are optional.”
- 원문 URL: [Claude Code Skills — Frontmatter reference](https://code.claude.com/docs/en/skills#frontmatter-reference)
- 가져온 날짜: 2026-09-26
- 확인 결과: Claude Code에서는 필수 frontmatter 필드가 없다. `description`은 권장 사항이며, `name`이 없으면 디렉터리명을 사용한다.
- 저장소 원 주장: Claude Code에도 `name`과 `description`이 공식 필수라는 취지.
- 판정: **틀림.**
- phase4.md 151행의 최신 판정은 **맞음**.

### C. `argument-hint` 누락이 discovery 실패를 일으키는가

- 원문 인용: “Hint shown during autocomplete to indicate expected arguments.”
- 원문 URL: [Claude Code Skills — Frontmatter reference](https://code.claude.com/docs/en/skills#frontmatter-reference)
- 가져온 날짜: 2026-09-26
- 확인 결과: `argument-hint`의 문서화된 역할은 자동완성 표시다. 자동 선택에는 `description`이 사용되고, `when_to_use`는 그 설명에 추가된다.
- 저장소 원 주장: “`argument-hint` 누락은 discovery 실패”
- 판정: **틀림.**
- phase4.md 152행의 정정은 **맞음**.

### D. 비표준 필드를 모든 런타임이 무시한다는 보장이 있는가

- Claude Code 원문 인용: “Claude Code ignores a field it doesn’t recognize without reporting an error.”
- Agent Skills 원문 인용: “Clients can use this to store additional properties not defined by the Agent Skills spec”
- 원문 URL: [Claude Code Skills](https://code.claude.com/docs/en/skills#frontmatter-reference), [Agent Skills specification](https://agentskills.io/specification)
- 가져온 날짜: 2026-09-26
- 확인 결과:

  - **Claude Code 로컬 런타임**은 자신이 인식하지 못하는 frontmatter 필드를 오류 없이 무시한다고 명시한다.
  - 그러나 `user-invocable`과 `argument-hint`는 현재 Claude Code가 인식하는 정식 Claude 전용 필드이므로 Claude Code에서 무시되지 않는다.
  - **Agent Skills 표준**에는 비표준 최상위 필드를 모든 구현이 무시해야 한다는 보장이 없다. 표준 밖의 추가 속성을 담는 문서화된 위치는 `metadata`다.
  - Claude 문서상 claude.ai 업로드, Skills API, `package_skill.py` 경로에서는 비표준 필드가 무시되지 않고 검증 오류가 발생한다.

- 저장소 원 주장: “Claude 전용 필드가 다른 플랫폼에서 무시됨”
- 판정: **틀림.** 모든 플랫폼에 적용되는 무시 보장은 원문에 없다.
- phase4.md 153행의 “안전하게 무시한다는 보장은 없다”는 판정은 **맞음**.
- 추론: 개별 제3자 런타임이 실제로 무시할 수는 있지만, 그것은 해당 구현의 동작이지 Agent Skills 표준의 보장이 아니다.

## 3. 저장소에 반영할 문장 제안

- Agent Skills 표준에서는 `name`과 `description`이 필수지만, Claude Code 로컬 런타임에서는 모든 frontmatter 필드가 선택이며 `description`만 권장된다.
- `argument-hint`는 명령 자동완성에 예상 인자를 표시하는 선택 필드이며, 스킬 자동 discovery의 필수 조건이 아니다.
- Claude Code는 자신이 인식하지 못한 필드를 로컬에서 무시하지만, Agent Skills 표준은 비표준 필드를 모든 런타임이 안전하게 무시한다고 보장하지 않으며 일부 배포 경로는 이를 오류로 거부한다.

## 4. 못 가져온 것 / 열린 질문

- 지정된 두 원문 페이지는 모두 정상적으로 가져왔다. `curl` 재시도는 필요하지 않았다.
- 열린 질문: Claude Code 외 개별 Agent Skills 구현이 비표준 필드를 어떻게 처리하는지는 이번에 지정된 두 원문만으로는 확정할 수 없다. 각 구현의 문서를 별도로 확인해야 한다.