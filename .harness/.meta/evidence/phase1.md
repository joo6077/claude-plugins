---
phase: 1
title: "Phase 1 설계 가이드 — 확보된 외부 근거"
collected: 2026-09-24
method: codex (foreground, 직접 호출 · gpt-5.6-sol · 조회는 curl/gh)
inputs: 처리 배정표(.claude/kaizen-input/insights-report.md)의 Phase 1 행 · phase-research-templates.md Phase 1 필수 출처 · 현행화 점검
note: 이 파일이 이 Phase 의 유일한 외부 근거다. 바깥 자료를 새로 찾지 마라. 여기 없는 URL·수치를 지어내지 마라. 없으면 미반영으로 남긴다.
---

읽기 전용으로 조사했으며 파일 변경은 없습니다.

## 1. 실제 조회한 출처

1. [Anthropic Skill Authoring Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices.md)
2. [Claude Code — Create custom subagents](https://code.claude.com/docs/en/sub-agents.md)
3. [anthropics/skills — skill-creator/SKILL.md](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md)
4. [Claude Code 최신 GitHub 릴리스 v2.1.281](https://github.com/anthropics/claude-code/releases/tag/v2.1.281) — 2026-09-23 게시
5. [zsh 공식 매뉴얼 — Array Subscripts](https://zsh.sourceforge.io/Doc/Release/Parameters.html#Array-Subscripts)

## 2. 항목별 관찰 사실

### harness:P09 — 검증 불가 보고를 실행 가능한 형태로 만들기

현재 생성 측 문구는 [skill-design-guide.md:300](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/harness/docs/guides/skill-design-guide.md:300)의 `[미검증] + 사유 한 줄`뿐이다.

반면 현재 평가 구현은 [qa-evaluator.md:65](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/harness/agents/qa-evaluator.md:65)에서 다음 네 가지를 요구한다.

1. 1차 도구 시도와 실패 출력
2. fallback 시도 또는 fallback 누락 기록
3. 실제 실패 로그
4. 통제 불가 사유와 환경 복구 후 실행할 재검증 명령

[agent-design-guide.md:569](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/harness/docs/guides/agent-design-guide.md:569)의 “4항”은 아직 `마커/2건 임계/조용한 PASS 금지/생성자 주장 배제`라는 옛 구성이어서, 실제 평가자의 네 요건과도 어긋난다.

외부 근거:

- Anthropic은 복잡한 절차를 순차 단계와 체크리스트로 쓰고, `validator 실행 → 오류 수정 → 재실행`, “검증 통과 전 다음 단계로 진행하지 않음”을 명시하라고 한다. 이는 실패 출력과 재실행 명령을 남기는 방향을 직접 지지한다. [Skill Authoring Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices.md)
- 같은 문서는 오류 가능성이 큰 작업에는 정확한 스크립트와 순서를 주는 low-freedom 설계를 권장한다. 검증 실패 처리는 여기에 해당한다. [Skill Authoring Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices.md)

반대 근거:

- 가져온 공식 문서에는 “검증 실패 때 우회를 반드시 한 개 이상 보고하라” 또는 “작업 자체를 못 한다고 말하기 전에도 같은 형식을 적용하라”는 정확한 문구는 없었다.
- 공식 문서는 여러 접근이 가능한 작업에는 high-freedom 지침도 허용한다. 다만 검증·마이그레이션처럼 실패 비용이 큰 작업은 low-freedom 예시로 분류하므로 이번 규칙과 직접 충돌하지 않는다. [Skill Authoring Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices.md)

추론: P09의 “막는 출력 + 시도한 우회 + 재실행 명령”은 공식 feedback-loop 원칙을 레포의 재현 가능한 보고 계약으로 구체화한 로컬 정책이다.

### harness:P05 — 알려진 답 대조

기존 레포에는 이미 “0 기대 측정”용 양성 대조가 있다.

- 생성 측: [skill-design-guide.md:313](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/harness/docs/guides/skill-design-guide.md:313)
- 계약 스키마: [contract-schema.md:817](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/harness/references/contract-schema.md:817)
- sprint-contract 패턴 표: [sprint-contract/SKILL.md:459](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/harness/skills/sprint-contract/SKILL.md:459)

이번 P05는 이를 “새로 짠 측정 스크립트가 0이 아닌 수치를 내는 경우”까지 확장한다.

외부 근거:

- Anthropic은 본격적인 문서 작성 전에 평가를 만들고, 기대 동작을 정의하고, baseline을 측정한 뒤 비교·반복하라고 한다. 또한 validator 실패 시 수정 후 재실행하도록 한다. 이는 작은 알려진 입력의 기대값과 실제값을 비교하는 방식을 지지한다. [Skill Authoring Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices.md)
- 공식 `skill-creator`도 eval 항목에 `expected_output`을 두고 반복 평가한다. SKILL.md는 500줄 미만을 이상적 상태로 설명하며 상세 자원은 분리하도록 한다. [anthropics/skills skill-creator](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md)

반대·근거 한계:

- “입력은 반드시 2~3줄이어야 한다”는 외부 근거는 찾지 못했다.
- “알려진 답에서 0 또는 빈 결과가 나오면 무조건 스크립트 결함으로 본다”는 정확한 공식 문구도 찾지 못했다. 기대값이 명시적으로 0인 테스트에는 적용할 수 없으므로 적용 범위를 “기대값이 0이 아닌 알려진 답 입력”으로 한정해야 한다.

추론: 2~3줄은 수작업으로 오라클을 독립 산출할 수 있게 하는 레포 계약값이지 외부 표준 수치가 아니다.

### harness:P05 — zsh 배열 첨자

zsh 공식 매뉴얼은 `KSH_ARRAYS`가 설정되지 않은 기본 상태에서 일반 배열이 1부터 시작하며, 첨자 0을 읽으면 빈 문자열을 반환한다고 명시한다. `KSH_ARRAYS`를 설정하면 0부터 시작한다. `"${arr[@]}"`는 각 원소를 개별 단어로 확장한다. [zsh Array Subscripts](https://zsh.sourceforge.io/Doc/Release/Parameters.html#Array-Subscripts)

로컬 실행도 다음과 같았다.

```text
zsh: zero=<> one=<alpha> all=<alpha,beta>
bash: zero=<alpha> one=<beta> all=<alpha beta>
```

따라서 요청한 셸 이식성 경고는 공식 동작과 일치한다. 단, “zsh 배열은 항상 1부터 센다”보다는 “기본 zsh 배열은 1부터 센다(`KSH_ARRAYS` 예외)”가 정확하다.

## 3. 현행화 — 낡은 곳

| 위치 | 현재 값 | 최신 확인값 |
|---|---|---|
| [agent-design-guide.md:70](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/harness/docs/guides/agent-design-guide.md:70) | frontmatter 15종 | 현재 공식 표는 18종이다: 기존 15종에 `omitClaudeMd`, `initialPrompt`, `experimental`이 추가되어 있다. 필수는 여전히 `name`, `description`뿐이다. [공식 문서](https://code.claude.com/docs/en/sub-agents.md) |
| [agent-design-guide.md:95](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/harness/docs/guides/agent-design-guide.md:95) | `initialPrompt`는 공식 필드가 아님 | 현재는 공식 파일 frontmatter와 `--agents` JSON 양쪽에서 인정된다. 다만 `--agent` 또는 `agent` 설정으로 메인 세션 에이전트가 될 때의 첫 사용자 턴이며, 플러그인 서브에이전트에서는 무시된다. [공식 문서](https://code.claude.com/docs/en/sub-agents.md) |
| [create-agent/SKILL.md:25](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/harness/skills/create-agent/SKILL.md:25), [create-agent/SKILL.md:81](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/harness/skills/create-agent/SKILL.md:81), [create-agent/SKILL.md:106](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/harness/skills/create-agent/SKILL.md:106) | 공식 15종 | 18종으로 동반 수정 필요. [공식 문서](https://code.claude.com/docs/en/sub-agents.md) |
| [agent-design-guide.md:214](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/harness/docs/guides/agent-design-guide.md:214) | 내장 Explore는 Haiku | v2.1.198부터 부모 모델을 상속한다. Anthropic API에서는 Opus가 상한이며, `CLAUDE_CODE_SUBAGENT_MODEL`로 전역 override할 수 있다. [공식 문서](https://code.claude.com/docs/en/sub-agents.md) |
| [agent-design-guide.md:463](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/harness/docs/guides/agent-design-guide.md:463) | 동시 20, 세션 누적 200, 깊이 3 | 현재 공식 문서는 동시 실행 기본 20과 깊이 기본 3은 유지하지만, 세션 전체 spawn 수에는 제한이 없다고 명시한다. `CLAUDE_CODE_MAX_SUBAGENTS_PER_SESSION=200` 주장은 제거 대상이다. ultracode에서는 동시 20 제한도 적용되지 않는다. [공식 문서](https://code.claude.com/docs/en/sub-agents.md) |
| [agent-design-guide.md:715](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/harness/docs/guides/agent-design-guide.md:715) | “2026-08 재확인 — frontmatter 15종” | 최신 공식 문서 기준 18종. 현재 Claude Code 최신 GitHub 릴리스는 v2.1.281이다. [공식 문서](https://code.claude.com/docs/en/sub-agents.md), [v2.1.281](https://github.com/anthropics/claude-code/releases/tag/v2.1.281) |
| [skill-design-guide.md:9](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/harness/docs/guides/skill-design-guide.md:9), [skill-design-guide.md:15](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/harness/docs/guides/skill-design-guide.md:15), [agent-design-guide.md:9](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/harness/docs/guides/agent-design-guide.md:9) | “2026-04 최신” | 현행 문서를 다시 조회했으므로 “최신” 고정 표기는 부정확하다. 조회일 또는 단순 출처명으로 바꾸는 편이 안전하다. Claude Code subagents 문서는 2026-09-22 수정본이었다. [공식 문서](https://code.claude.com/docs/en/sub-agents.md) |
| [skill-design-guide.md:560](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/harness/docs/guides/skill-design-guide.md:560), [skill-design-guide.md:1133](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/harness/docs/guides/skill-design-guide.md:1133) | “500라인 상한” | 공식 문서는 “최적 성능을 위해 500줄 미만”, 공식 `skill-creator`는 “500줄 미만이 이상적이며 필요하면 더 길어도 됨”이라고 한다. 강제 상한이 아니라 권고값이다. 본문 [570행](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/harness/docs/guides/skill-design-guide.md:570)은 이미 이를 인정하므로 제목·요약표만 과도하게 강하다. [Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices.md), [skill-creator](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md) |
| [create-skill/SKILL.md:24](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/harness/skills/create-skill/SKILL.md:24) | “1500~2000 words 타깃 — Anthropic 기준” | 이번에 가져온 현행 공식 문서와 `skill-creator`에서는 이 단어 수 범위를 확인하지 못했다. 확인 가능한 기준은 500줄 미만 권고뿐이다. [Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices.md), [skill-creator](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md) |

추가 변경 사항으로 `/agents` 생성 wizard는 Claude Code v2.1.198부터 제거되었고, 직접 파일을 쓰거나 Claude에게 생성을 요청하는 방식으로 바뀌었다. 현행 가이드에 wizard 사용 지시는 없어 직접 수정할 낡은 줄은 찾지 못했다. [공식 문서](https://code.claude.com/docs/en/sub-agents.md)

## 4. 권장안

### P09 계약 문구

`skill-design-guide §3.7`과 `agent-design-guide §10`이 같은 형식을 쓰도록 다음 네 필드를 정본으로 삼는 것이 적절하다.

```text
[미검증:{분류}]
- 막는 것: 실행한 명령과 실패 출력
- 시도한 우회: 1개 이상과 그 결과
- 통제 불가 사유: 한 문장
- 재검증: 조건이 갖춰졌을 때 실행할 명령
```

그리고 별도 한 줄:

> 작업 자체를 수행할 수 없다고 결론내리기 전에도 동일하게 막는 것의 실제 출력과 시도한 우회 하나 이상을 기록한다.

기존 “미검증 2건 이상 자동 REJECT”는 현재 평가자의 `ENV`/`INVALID` 분리와 충돌하므로 P09 문장을 고칠 때 함께 재검토해야 한다.

### P05 알려진 답 대조

`contract-schema`에 다음 범위로 두는 것이 안전하다.

- 적용: 이번 스프린트에서 새로 작성한 측정 스크립트가 길이·개수·무게·비율 등 **기대값이 0이 아닌 수치**를 산출할 때
- 입력: 사람이 독립적으로 답을 셀 수 있는 최소 입력, 레포 정책상 2~3줄
- 기록: `기대값: N · 실제값: M · 명령: ...`
- 판정: `M != N`이면 봉인 금지
- 기대값이 0이 아닌데 결과가 `0` 또는 빈 출력이면 통과가 아니라 측정기 결함으로 취급
- 기존의 “0 기대 양성 대조”와 구별: 기존 규칙은 나쁜 입력에서 1 이상이 나오는지 확인하고, 새 규칙은 좋은 작은 입력의 정확한 비영 값과 일치하는지 확인

`sprint-contract` 패턴 표에는 요청한 대로 다섯 번째 행을 추가하는 것이 맞다.

### zsh 문구

```text
기본 zsh 배열은 1부터 센다(`KSH_ARRAYS` 설정 시 예외).
따라서 `${arr[0]}`은 기본 설정에서 빈 값이고, 첨자 반복은 한 칸 밀릴 수 있다.
첨자가 필요 없으면 `for x in "${arr[@]}"`로 순회하고,
0-based 첨자가 계약의 일부라면 Python 등 명시적인 구현을 사용한다.
```

### 현행화 계약

- Claude Code 호환성 기준을 날짜 대신 “조회한 최신 릴리스 + 공식 문서 조회일”로 기록한다.
- frontmatter 필드는 18종으로 갱신하되, `initialPrompt`는 플러그인 에이전트에서 무시된다는 범위 제약을 같은 행에 둔다.
- “세션 누적 200개” 제한은 제거한다.
- 500줄은 `상한`이 아니라 `권고/ideal`로 통일한다.

## 5. 못 가져온 것 / 열린 질문

- 표의 “LLM agent skill design arXiv 2026”은 최소 3개 필수 소스를 충족한 뒤 중단하라는 규칙에 따라 추가 조회하지 않았다.
- 알려진 답 입력의 정확한 크기인 “2~3줄”을 규정한 외부 1차 출처는 찾지 못했다.
- 검증 실패 보고에 “우회 1개 이상”을 의무화하는 정확한 Anthropic 문구는 찾지 못했다. 공식 근거는 validator 실패 후 수정·재실행하는 feedback loop까지다.
- Agent Skills 문서는 별도 안정 버전 번호가 없는 living specification이라 “최신 안정 버전” 숫자를 대조할 수 없었다.
- Claude Code 공식 문서는 현재 세션 누적 spawn 제한이 없다고 하지만, 이 제한이 어느 릴리스에서 제거됐는지는 조회한 자료에서 특정하지 못했다. 따라서 제거 버전은 쓰지 않는 것이 안전하다.
