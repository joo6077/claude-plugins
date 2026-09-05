---
title: Claude Code 에이전트 설계 가이드
version: 1.6.0
last_updated: 2026-08-13
---

# Claude Code 에이전트 설계 가이드

> 공식 문서(2026-04 최신), Anthropic Research, 학술 논문, 커뮤니티 실전 경험 기반 서브에이전트 설계 원칙과 실전 팁

**이 문서의 용도:** 새 에이전트를 만들거나 기존 에이전트를 개선할 때 참고한다. 이 프로젝트(`claude-plugins`)의 실제 에이전트를 적용 사례로 함께 다룬다.

**주요 출처:**

- [Create custom subagents — Claude Code Docs](https://code.claude.com/docs/en/sub-agents) (2026-04)
- [Building Effective Agents — Anthropic Research](https://www.anthropic.com/research/building-effective-agents)
- [Claude Code Sub-Agent Best Practices — claudefa.st](https://claudefa.st/blog/guide/agents/sub-agent-best-practices)

---

## 1. 에이전트 vs 스킬 — 언제 무엇을 쓰는가

> **출처:** [Claude Code Sub-agents 공식 문서](https://code.claude.com/docs/en/sub-agents), [Building Effective Agents](https://www.anthropic.com/research/building-effective-agents)

가장 먼저 판단해야 할 것: **이 작업에 에이전트가 필요한가?**

| 기준 | 스킬 사용 | 에이전트 사용 |
| ------ | ----------- | --------------- |
| 컨텍스트 | 메인 대화에서 실행 | 별도 컨텍스트 윈도우에서 격리 실행 |
| 도구 제한 | 메인 대화의 도구 전체 사용 | 도구를 제한하여 안전하게 격리 |
| 출력량 | 적음~중간 | 대량 (테스트 실행, 코드베이스 탐색 등) |
| 재사용 | 반복 가능한 워크플로우/지식 | 독립적 작업 단위 |
| 비용 | 메인 컨텍스트 소비 | 별도 컨텍스트 (메인 보존) |

**Anthropic의 핵심 원칙:** "복잡성은 결과가 입증될 때만 추가해라." 단순한 스킬로 충분하면 에이전트를 만들지 마라.

---

## 2. 에이전트 파일 구조

> **출처:** [Claude Code Sub-agents 공식 문서](https://code.claude.com/docs/en/sub-agents)

```markdown
---
name: my-agent              # 필수. 소문자 + 하이픈
description: >              # 필수. Claude가 위임 판단에 사용
  언제 이 에이전트를 사용할지 구체적으로 명시.
tools: Read, Grep, Glob     # 선택. 생략하면 전체 도구 상속
model: sonnet               # 선택. sonnet/opus/haiku/inherit
---

시스템 프롬프트 (마크다운 본문)
```

### 배치 위치 (우선순위순)

| 위치 | 범위 | 우선순위 |
| ------ | ------ | ---------- |
| `--agents` CLI 플래그 | 현재 세션만 | 1 (최고) |
| `.claude/agents/` | 현재 프로젝트 | 2 |
| `~/.claude/agents/` | 모든 프로젝트 | 3 |
| 플러그인 `agents/` | 플러그인 활성화된 곳 | 4 (최저) |

**프로젝트 에이전트**는 git에 체크인하여 팀과 공유한다.

### frontmatter 전체 필드

> **출처:** [Create custom subagents — Supported frontmatter fields](https://code.claude.com/docs/en/sub-agents#supported-frontmatter-fields) (2026-08 재확인)

공식 frontmatter 는 **15 종**이고, 그중 **필수는 `name` 과 `description` 둘뿐**이다. 아래 표가 그
15 종 전부이며, 여기에 없는 이름을 frontmatter 필드로 소개하지 마라 (표 아래 "표에 없는 이름들" 참조).

| 필드 | 필수 | 설명 |
| ------ | ------ | ------ |
| `name` | 예 | 고유 식별자 (소문자, 하이픈). 훅이 이 값을 `agent_type` 으로 받는다. **파일명과 일치할 필요는 없다** |
| `description` | 예 | 언제 위임할지 Claude가 판단하는 기준 |
| `tools` | 아니오 | 허용 도구 목록. 생략 시 전체 상속. 목록의 어느 항목도 실제 도구로 해석되지 않으면 에이전트가 **launch 자체에 실패**한다. 스킬을 컨텍스트에 미리 넣으려면 여기에 `Skill` 을 적지 말고 `skills` 필드를 써라 |
| `disallowedTools` | 아니오 | 차단 도구 목록 (상속·지정 목록에서 제거) |
| `model` | 아니오 | `sonnet`, `opus`, `haiku`, `fable`, 풀 model ID(예: `claude-opus-5`), `inherit` (기본값) |
| `permissionMode` | 아니오 | `default`, `acceptEdits`, `auto`, `dontAsk`, `bypassPermissions`, `plan`, `manual`(= `default` 의 별칭) |
| `maxTurns` | 아니오 | 최대 에이전트 턴 수 |
| `skills` | 아니오 | 시작 시 주입할 스킬 목록 (전체 내용이 context 에 inject 됨, 스킬 invoke 가능성만 주어지는 게 아님) |
| `mcpServers` | 아니오 | 이 에이전트 전용 MCP 서버 (이미 설정된 서버명 참조 또는 inline 정의) |
| `hooks` | 아니오 | 라이프사이클 훅 (`PreToolUse`, `PostToolUse`, `Stop` → 런타임에 `SubagentStop` 으로 변환) |
| `memory` | 아니오 | 영속 메모리: `user`, `project`, `local` |
| `background` | 아니오 | `true` 면 결과가 즉시 필요할 때도 **항상** 백그라운드 실행. 미지정이면 Claude 가 판단하며, 최신 버전은 기본적으로 백그라운드로 돌린다 |
| `effort` | 아니오 | `low`, `medium`, `high`, `xhigh`, `max` (모델별 가용 레벨 상이). 세션 effort 를 override |
| `isolation` | 아니오 | `worktree`면 격리된 git worktree에서 실행 (변경이 없으면 자동 정리) |
| `color` | 아니오 | 터미널 UI 에 표시되는 에이전트 색상 (`red`, `blue`, `green`, `yellow`, `purple`, `orange`, `pink`, `cyan`) |

**표에 없는 이름들 (혼동 방지 · 2026-08 정정):**

- **`prompt`** — 이것은 `--agents` **JSON 정의**에서 markdown body 에 해당하는 필드다. 파일 기반
  YAML frontmatter 표에는 존재하지 않는다. `.md` 에이전트 파일의 frontmatter 에 `prompt:` 를 적지 마라
- **`initialPrompt`** — 2026-07 판 이 표에 행으로 실려 있었으나 공식 15 종 목록에 없다. 근거가
  다시 확보되기 전까지 공식 필드로 소개하지 않는다

**플러그인 에이전트 제약:** `hooks`, `mcpServers`, `permissionMode` 필드는 플러그인으로 배포된 에이전트에서는 **무시된다**. 이 필드가 필요하면 `.claude/agents/` 로 복사해라.

---

## 3. description은 위임 트리거다

> **출처:** [Create custom subagents — Understand automatic delegation](https://code.claude.com/docs/en/sub-agents#understand-automatic-delegation) — "Claude automatically delegates tasks based on the task description in your request, the description field in subagent configurations, and current context. To encourage proactive delegation, include phrases like 'use proactively' in your subagent's description field."

스킬의 description과 동일한 원칙이 적용된다. description은 사람을 위한 요약이 아니라 **Claude가 에이전트를 선택하는 트리거 조건**이다.

### Bad

```yaml
description: QA 관련 에이전트
```

### Good

```yaml
description: >
  Sprint Contract 기반으로 구현 결과를 독립 평가하는 QA 에이전트.
  구현 완료 후 APPROVE/REJECT 판정을 내린다.
  /develop Step 완료 후, 또는 사용자가 "QA 돌려줘"라고 요청할 때 사용.
```

### "use proactively" 키워드 — 공식 언더트리거 방지 메커니즘

Claude 는 서브에이전트를 필요한 상황에서도 **undertrigger** (위임하지 않는) 경향이 있다. 이를 해결하기 위해 Anthropic 공식 문서는 description 에 `use proactively` 또는 `proactively` 를 명시적으로 포함하라고 권장한다.

**Good — 프로액티브 위임 명시:**

```yaml
description: >
  Expert code review specialist. Proactively reviews code for quality,
  security, and maintainability. Use immediately after writing or modifying code.
```

```yaml
description: >
  Debugging specialist for errors, test failures, and unexpected behavior.
  Use proactively when encountering any issues.
```

**적용 체크리스트:**

- 코드 작성/수정 직후 자동으로 돌아야 하는 리뷰어 → `Proactively reviews... Use immediately after...`
- 에러/실패 발생 시 자동 개입해야 하는 디버거 → `Use proactively when encountering...`
- 명시적 호출이 필요한 에이전트(예: QA) → `use proactively` 생략하고 트리거 키워드만 나열

이 프로젝트의 `qa-evaluator` 는 사용자 명시 호출 및 `/sprint-contract` 완료 후 연계로 호출되므로 "use proactively" 를 생략한다.

### Sibling Agent 트리거 키워드 배타성 (substring 포함)

> **대응:** skill-design-guide §4 "트리거 키워드 중복 방지 원칙"

에이전트도 스킬과 같은 규칙을 따른다 — description 의 트리거 키워드는 **sibling agent 와 set intersection + substring containment 가 모두 공집합** 이어야 한다. "QA 돌려줘" 같은 키워드가 여러 에이전트 description 에 중복되거나, 한 에이전트의 키워드가 다른 에이전트 키워드의 부분문자열이면 Claude 가 어떤 에이전트로 위임할지 예측 불가하다. 플러그인 내 에이전트가 2+ 개이면 편집 시 반드시 `rg -n "description:" agents/*.md` 로 확인 후 저장한다.

---

## 3.5. 계약 모호성 방지 · Binary Decidability Pre-Check (필수 승격 섹션)

> **대응:** skill-design-guide §3.5 "QA 계약과 1:1 매칭되는 이름을 사용하라"
> **배경 (재발 방지):** 지난 kaizen 사이클에서 이 원칙은 skill-design-guide 에만 존재하고 이 가이드에는 §10 Gotchas 내 1 bullet 으로만 있어 design-kit PH-01 REJECT 가 발생했다. 본 사이클에서 **독립 최상위 섹션** 으로 승격한다.

### 원칙

Reviewer / Evaluator 에이전트는 평가를 시작하기 **전**에 Sprint Contract 의 각 조건이 **이진(PASS/FAIL) 판정 가능한지** 자체 검토해야 한다. 모호한 조건은 평가 중 해석 차이로 REJECT iteration 을 낭비시킨다.

### 수행 절차 (평가 시작 전)

1. **이진 판정 가능성 검사.** 각 조건이 "PASS" 또는 "FAIL" 중 하나로 귀결 가능한가? "충분히", "상당한", "어느 정도" 같은 정성적 수식어가 있으면 계약 작성자에게 구체화 요청 또는 REJECT 사유로 명시
2. **구체성 태그 존재 확인.** contract-design-guide 의 `[exact]` / `[structural]` / `[goal]` 태그 사용 여부 확인:

   - `[exact]`: 문자 그대로 매칭 (정규식 · 라인번호 · 정확한 값)
   - `[structural]`: 구조적 일치 (섹션 존재 · 카운트 · 관계)
   - `[goal]`: 결과 상태 (빌드 성공 · 테스트 통과 · 사용자 경험)
3. **경계 정의 의무.** 파일 경로 · 함수명 · 라인 수가 미명시면 에이전트 자체적으로 경계를 정의하되 **판정 근거 블록에 명시**
4. **모호성 발견 시 REJECT 사유에 포함.** 평가 도중 조건의 모호성이 드러나면 다음 iteration 에서 계약 작성자가 수정할 수 있도록 REJECT 사유에 "모호성: [조건 ID] — [모호한 문구] — [제안하는 구체화]" 포함

### 실패 사례 (이 원칙 없이 발생)

- **PH-01 (design-kit)**: "계약 모호성 방지 원칙" 이 이 가이드에 누락되어 평가자가 모호 조건을 그대로 평가 → 결과 해석 충돌 → REJECT
- **SK-02 (harness, 2026-04)**: "Neubrutalism 모달 box-shadow offset 3px" 조건에서 "주요 interactive element" 범위가 모호 → 평가자가 badge/decoration 에도 적용 → REJECT

### 평가자 자체 체크리스트 (평가 시작 직전)

- [ ] 모든 조건에 구체성 태그(`[exact]`/`[structural]`/`[goal]`) 가 붙어 있는가?
- [ ] 정성적 수식어(충분히, 상당한, 등) 가 있는 조건은 경계 정의 완료되었는가?
- [ ] 파일/라인 근거가 명시되지 않은 조건은 에이전트가 자체 경계 정의 후 근거 블록에 기록했는가?

---

## 4. 도구 스코핑 — 최소 권한 원칙

> **출처:** [Claude Code Sub-agents 공식 문서](https://code.claude.com/docs/en/sub-agents), [Building Effective Agents](https://www.anthropic.com/research/building-effective-agents)

에이전트에게 **필요한 도구만** 부여한다. 이것이 에이전트와 스킬의 핵심 차이점이다.

### 역할별 도구 매핑

> **출처:** [Create custom subagents — Available tools](https://code.claude.com/docs/en/sub-agents#available-tools), [Claude Code Sub-Agent Best Practices](https://claudefa.st/blog/guide/agents/sub-agent-best-practices) (2026-04)

| 역할 | 도구 | 이유 |
| ------ | ------ | ------ |
| 읽기 전용 리뷰어 / 감사자 | `Read, Grep, Glob` | 코드 수정 불가 → 안전 |
| QA 평가자 | `Read, Grep, Glob, Bash` | 분석 명령 실행 필요, Edit/Write 금지 |
| 연구자 / 리서치 에이전트 | `Read, Grep, Glob, WebFetch, WebSearch` | 읽기 + 외부 검색 |
| 구현자 / 코드 라이터 | `Read, Write, Edit, Bash, Glob, Grep` | 코드 수정 + 실행 |
| 문서 작성자 | `Read, Write, Edit, Glob, Grep, WebFetch, WebSearch` | 문서 편집 + 출처 조회 |
| 데이터 분석가 | `Bash, Read, Write` | 쿼리 실행 + 결과 저장 |
| 아키텍트 / PM | `Read, Grep, Glob` + MCP docs tools | read-heavy, 탐색 중심 |

### 내장 서브에이전트 도구 프로파일 (참고)

Claude Code 공식 내장 서브에이전트는 다음 패턴을 따른다:

- **Explorer / Research 계열**: Read-only tools (Write/Edit 거부), 모델 `haiku` 로 저지연·저비용
- **Debugger 계열**: All tools, 모델 `inherit` (부모 세션 수준)
- **Code Reviewer 계열**: Read-only, 모델 `inherit`

새 에이전트 설계 시 이 프로파일 중 어느 것에 해당하는지 먼저 판단하면 도구 리스트를 빠르게 좁힐 수 있다.

### 조건부 제한이 필요할 때

단순 도구 목록으로 부족하면 `PreToolUse` 훅으로 세밀하게 제어한다:

```yaml
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-readonly-query.sh"
```

### 서브에이전트 중첩 (nesting) — 기본 3 층까지 허용된다

> **출처:** [Create custom subagents — Let subagents spawn their own subagents](https://code.claude.com/docs/en/sub-agents) (2026-07 확인)

**중요 정정 (2026-07):** 과거 이 가이드는 서브에이전트의 하위 위임을 금지된 것으로 기술했으나, 현재 공식 동작은 다르다. **서브에이전트는 기본적으로 자기 아래로 서브에이전트를 스폰할 수 있으며, 메인 대화 기준 3 층까지 중첩된다.** 깊이 한계에 도달하면 Claude Code 가 해당 서브에이전트에서 `Agent` 도구를 회수하므로, 그 에이전트는 위임 없이 직접 일하고 요약 하나만 반환한다.

- 깊이 조정: `settings.json` 의 `env.CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH` (`1` 로 두면 중첩 비활성)
- 중첩된 서브에이전트도 top-level 과 동일하게 설정·해석된다. 중간 산출물은 메인 대화에 도달하지 않고 **최상위 서브에이전트의 요약만** 올라온다
- 특정 에이전트만 스폰을 막으려면 (예: read-only 를 유지해야 하는 리뷰어) 그 에이전트의 `tools` 에서 `Agent` 를 빼거나 `disallowedTools` 에 추가한다

**설계 함의:** "리뷰어가 발견 항목마다 검증자를 띄우는" 형태처럼 위임된 작업이 다시 병렬로 쪼개지는 구조가 이제 정상 설계 선택지다. 다만 §7 의 fan-out 상한과 exploration budget 은 중첩 층에도 그대로 적용된다 — 층이 깊어질수록 비용은 곱으로 늘어난다.

### Agent(agent_type) — 스폰 가능 서브에이전트 화이트리스트

`Agent` 도구로 스폰할 수 있는 서브에이전트를 **화이트리스트로 제한** 하려면 `tools` 필드에 `Agent(agent_type)` 문법을 사용한다.

```yaml
---
name: coordinator
description: Coordinates work across specialized agents
tools: Agent(worker, researcher), Read, Bash
---
```

이 예시에서는 `worker` 와 `researcher` 서브에이전트만 스폰 가능하다. 그 외를 호출하면 요청이 실패하며, 에이전트는 허용된 타입만 프롬프트에서 볼 수 있다.

**규칙:**

- `Agent(...)` 로 명시하면 **화이트리스트** 방식 (나열된 것만 허용)
- `Agent` 만 쓰면 **전체 허용**
- `Agent` 자체를 생략하면 **모든 서브에이전트 스폰 불가**
- 중첩이 허용되므로 이 문법은 메인 스레드 에이전트뿐 아니라 **중첩 서브에이전트에도 유효**하다

---

## 5. 모델 선택 전략

> **출처:** [Claude Code Sub-agents Best Practices](https://claudefa.st/blog/guide/agents/sub-agent-best-practices), [Claude Code 공식 문서](https://code.claude.com/docs/en/sub-agents)

**작업 복잡도에 맞는 모델을 선택**하여 비용을 최적화한다.

| 작업 유형 | 모델 | 이유 |
| ----------- | ------ | ------ |
| 코드베이스 탐색, 파일 검색 | **haiku** | 빠르고 저렴. 읽기 전용 |
| 코드 리뷰, 테스트 작성, 구현 | **sonnet** | 능력과 속도의 균형 |
| 아키텍처 판단, 복잡한 평가 | **opus** | 최고 추론 능력 |
| 메인 대화와 동일 수준 필요 | **inherit** | 부모 모델 상속 |

**추천 패턴:** 메인 세션은 Opus, 서브에이전트는 Sonnet. 집중된 작업에서는 Sonnet이면 충분하다.

### Model Routing — 작업별 자동 모델 선택

> **출처:** [Building AI Coding Agents for the Terminal — arxiv:2603.05344](https://arxiv.org/abs/2603.05344)

수동으로 모델을 고정하는 대신, 작업 유형에 따라 **자동으로 모델을 라우팅**하는 패턴이 등장하고 있다. 오케스트레이터가 작업을 분류하고 적합한 모델로 위임한다.

```text
요청 → 분류기 → 탐색 작업 → haiku
                → 코드 리뷰 → sonnet
                → 아키텍처 판단 → opus
```

**현재 적용:** Claude Code의 `model` 필드는 에이전트 단위 고정이므로, 이 패턴을 적용하려면 라우팅 에이전트가 작업별로 다른 모델의 서브에이전트를 호출하는 구조를 사용한다.

---

## 6. 일곱 가지 에이전트 디자인 패턴

> **출처(패턴 1~5):** [Building Effective Agents](https://www.anthropic.com/research/building-effective-agents)

패턴 1~5 는 Anthropic이 식별한 핵심 패턴이고, 6~7 은 이 레포에서 덧붙인 것으로 각자 아래에 출처를 단다.
에이전트를 설계할 때 이 중 하나를 기반으로 한다.

### 패턴 1: 프롬프트 체이닝 (Prompt Chaining)

```text
LLM 호출 A → 게이트 검증 → LLM 호출 B → 게이트 검증 → 결과
```

순차적 단계로 분해. 중간에 프로그래밍적 검증 게이트를 넣는다.
**적합:** 정확도가 중요하고 단계가 명확한 작업.

### 패턴 2: 라우팅 (Routing)

```text
입력 → 분류기 → 전문가 A / 전문가 B / 전문가 C
```

입력을 분류하여 전문 핸들러로 보낸다.
**적합:** 이질적인 요청 유형을 처리하는 경우.

### 패턴 3: 병렬화 (Parallelization)

```text
        ┌→ 작업 A ─┐
입력 ───┼→ 작업 B ──┼→ 합성
        └→ 작업 C ─┘
```

독립적인 하위 작업을 동시 실행.
**적합:** 자연스럽게 분할되는 작업, 또는 다양한 관점이 필요한 경우.

### 패턴 4: 오케스트레이터-워커 (Orchestrator-Workers)

```text
오케스트레이터 LLM → 동적으로 하위 작업 분해 → 워커들 → 합성
```

병렬화와 달리 하위 작업이 **사전 정의되지 않고 동적으로 결정**된다.
**적합:** 어떤 파일을 수정할지 미리 알 수 없는 코딩 작업.

### 패턴 5: 평가자-최적화자 (Evaluator-Optimizer)

```text
생성 LLM ←→ 평가 LLM (반복 피드백 루프)
```

하나가 생성하고 다른 하나가 평가하여 반복 개선.
**적합:** 명확한 평가 기준이 있고, 반복으로 품질이 향상되는 경우.

### 패턴 6: 계획-실행 분리 (Plan-Execute)

> **출처:** [Building AI Coding Agents for the Terminal — arxiv:2603.05344](https://arxiv.org/abs/2603.05344)

```text
사용자 요청 → 계획 에이전트 (추론) → 실행 계획 → 실행 에이전트 (도구 호출) → 결과
```

계획과 실행을 별도 에이전트로 분리한다. 계획 에이전트는 추론에 집중하고, 실행 에이전트는 도구 호출에 집중한다.
**적합:** 복잡한 멀티스텝 작업에서 계획 오류와 실행 오류를 독립적으로 디버깅해야 하는 경우.

**오케스트레이터-워커와의 차이:** 오케스트레이터-워커는 동적으로 하위 작업을 분배하지만, 계획-실행 분리는 계획 자체를 별도 에이전트가 전담한다. 계획 에이전트에는 `Read, Grep, Glob`만 부여하고 `Edit, Write`는 실행 에이전트에만 부여하여 안전성을 높인다.

### 패턴 7: Hook-Triggered Auto-Correction (PostToolUse + Agent)

> **출처:** `/insights` 30일 세션 분석 (Feature Suggestion #2: "Hooks — PostToolUse 로 dart format / cargo fmt / cargo clippy 자동 실행")

```text
Edit/Write 발생 → PostToolUse 훅 → 정적 검증 (format/clippy/analyze) → 위반 발견 시 read-only 리뷰어 에이전트 spawn → 수정 제안서
```

Edit/Write 후 `PostToolUse` 훅이 결정론적 정적 검증(`cargo fmt --check`, `dart format --set-exit-if-changed`, `eslint --max-warnings=0`) 을 자동 실행한다. 위반이 검출되면 read-only 리뷰어 에이전트(`Read, Grep, Glob` 만)를 spawn 하여 fix 제안서를 만들고, 메인 Claude 가 그 제안을 토대로 Edit 한다. 사용자가 매번 "포맷 돌려" / "clippy 돌려" 라고 prompt 할 필요 없이 lifecycle event 가 quality gate 를 자동으로 닫는다.

**적합:**

- 결정론적 자동 수정 가능한 규칙 — `cargo fmt`, `dart format`, `eslint --fix`, `prettier --write`
- 실패 발견 시 fix 가 단일 명령으로 끝나는 영역 (포맷팅, import 정렬, 단순 lint)
- 대량 편집(refactor) 후 일관성 enforce 가 필요한 경우

**부적합:**

- 의미적 판단이 필요한 리뷰 (architecture decision, domain logic, naming) — 인간/평가자 에이전트 필요
- 훅 실행이 1초 이상 소요되는 무거운 검증 (전체 빌드, 풀 테스트) — 별도 trigger 권장
- 비결정론적 수정이 필요한 영역 (코드 리팩토링 제안)

**구현 형태:** 훅은 `.claude/settings.json` 의 `hooks.PostToolUse` 에 matcher (`Edit|Write`) + command 로 등록. 명령이 비-zero exit 이면 메인 Claude 가 결과를 받아 후속 조치를 결정. 에이전트 spawn 은 메인 Claude 가 결정 (훅이 직접 spawn 하지 않음 — 훅은 stateless).

**Enforcement 등급 관점:** 훅은 skill-design-guide §3.7 의 **E3 (결정론적 게이트)** 를 에이전트 측에서 구현하는 형태다 — LLM 판단 없이 매 실행마다 같은 판정을 내리므로 문장 규칙(E1)·체크리스트(E2) 와 달리 per-run 보장을 제공한다. 같은 위반이 반복되는데 프롬프트 문구만 계속 다듬고 있다면 그 규칙은 E3 로 올릴 후보다.

**보완 패턴 — PreToolUse 가드 (사후 수정이 아닌 사전 차단):**

> **출처:** `/insights` 2026-05-07 fresh report (130 sessions): "브랜치가 origin에서 벗어났거나 좀비 MCP 프로세스가 있을 때 편집을 차단하는 PreToolUse 훅으로 세션을 잡아먹는 패턴을 막을 수 있습니다."

PostToolUse 가 *편집 후* 의 quality gate 라면 PreToolUse 는 *편집 전* 의 risk gate 다. 다음 3 영역에서 효과적:

1. **Origin Sync 가드** — `git rev-list --left-right --count HEAD...@{u}` 결과로 upstream 보다 N커밋 뒤지면 stderr 경고. 병렬 자동화 충돌 (Pattern #2 Pre-Sprint Sync Check 자동화) 자동 발견.
2. **좀비 프로세스 가드** — `ps aux | grep mcp_server` 결과 5건 초과면 정리 권고. /insights 의 "45+ stale 프로세스 사고" 재발 방지.
3. **보호 브랜치 가드** — `git rev-parse --abbrev-ref HEAD` 결과가 main/master/dev 면 stderr 경고. Scope-Bound Edits Hard-stop (skill-design-guide §3.6) 자동 enforcement.

**graceful degradation 원칙:** PreToolUse 훅은 `exit 0` 으로 편집 자체를 막지 않는다 (stderr 경고만). 강한 차단이 필요하면 사용자가 settings 에서 enable. 이는 false-positive (예: 의도된 main 직접 편집) 시 워크플로우 마비를 막기 위함. 이 레포의 `.claude/settings.json` 에 3 훅 모두 등록 완료.

### 이 프로젝트의 실제 예시

`qa-evaluator`는 **패턴 5 (평가자-최적화자)**를 구현한다:

- Generator(메인 Claude)가 코드를 생성
- QA Evaluator(독립 에이전트)가 Sprint Contract 기준으로 평가
- REJECT 시 Generator가 피드백 반영하여 재구현

---

## 7. 실행 패턴: 병렬 vs 순차 vs 백그라운드

> **출처:** [Claude Code Sub-Agent Best Practices](https://claudefa.st/blog/guide/agents/sub-agent-best-practices)

### 병렬 디스패치 조건 (3가지 모두 충족 시)

- 3개 이상의 독립적 작업
- 작업 간 공유 상태 없음
- 파일 경계가 명확하여 겹치지 않음

### 순차 디스패치가 필수인 경우

- 작업 간 의존성 있음 (A의 출력이 B의 입력)
- 공유 파일로 충돌 위험
- 범위가 불명확하여 이해 후 진행 필요

### 백그라운드 디스패치

- 연구, 문서 조회, 보안 감사 등
- 결과가 즉시 필요하지 않은 작업
- `Ctrl+B`로 실행 중인 에이전트를 백그라운드로 전환 가능

### Fan-out 상한 · Exploration Budget — 과탐색 stall 과 비용 폭주 방지

> **출처:** [Dive into Claude Code: Design Space of AI Agent Systems — arxiv:2604.14228](https://arxiv.org/html/2604.14228v1) · [Claude Code Agents 2026 — CloudZero](https://www.cloudzero.com/blog/claude-code-agents/) · `/insights` 30일 세션 분석 (Friction Point #6: 과탐색 stall — Figma metadata spelunking, 크롤링 중 구현 전 중단)

§10 Gotcha "과도한 병렬화는 토큰 낭비" 를 정량 규칙으로 승격한다. 비용·시간이 폭주하는 두 축은 **fan-out 폭(병렬 spawn 수)** 과 **exploration 깊이(구현 전 탐색 turn 수)** 다. 2026 사례: 단일 슬래시 커맨드가 49 서브에이전트를 2.5시간 병렬 spawn 하여 $8K~15K 추정 (CloudZero). `/insights` 에서는 같은 사용자가 Figma 노드 과탐색·웹 크롤링으로 구현 전 세션이 stall 되어 직접 중단하는 패턴이 반복됐다.

**플랫폼 하드 리밋 (자체 예산과 구분하라):** Claude Code 자체가 강제하는 상한이 3 종 있다 — **동시 실행 20 개**(`CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS`), **세션 누적 200 개**(`CLAUDE_CODE_MAX_SUBAGENTS_PER_SESSION`), **중첩 깊이 3 층**(`CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH`). 초과하면 `Agent` 도구가 각각 `Concurrent subagent limit reached` / `Subagent spawn limit reached` 로 실패한다. 아래 "기본 5 개" 는 이 하드 리밋과 별개인 **자체 비용 예산**이며 항상 하드 리밋보다 작게 잡는다 — 하드 리밋은 사고를 막는 최후 방어선이지 설계 목표가 아니다.

**원칙:**

1. **Fan-out 상한** — 1 회 디스패치당 병렬 서브에이전트 **기본 5개 이하**. 6+ 개가 필요하면 batch 로 쪼개 순차 처리하거나 사용자에게 비용/시간 trade-off 를 먼저 보고하고 승인받는다. 단순 작업에 fan-out 하지 않는다 (§10 Gotcha 와 동일 정신).
2. **토큰 vs 시간 trade-off 명시** — 토큰 예산이 빡빡하면 **순차** 탐색, 시간 예산이 빡빡하면 **병렬** 탐색 (각 서브에이전트가 독립 context window 를 차지하므로 병렬은 latency 와 토큰을 동시에 키운다). 디스패치 결정 시 어느 축을 우선하는지 한 줄로 명시.
3. **Exploration budget** — 구현·산출 전 "탐색만" 하는 단계에 상한을 둔다. read-only 탐색이 의미 있는 진전 없이 누적되면(예: 같은 디렉토리를 반복 Glob, 동일 노드 메타데이터 재조회) 중단하고 현재까지 발견을 요약한 뒤 진행 방향을 사용자에게 확인한다. "조금만 더 보면 알 것 같다" 는 stall 의 가장 흔한 진입점이다.
4. **Summary-only 반환** — 서브에이전트는 raw 출력 전체가 아닌 **요약(findings)만** 메인 컨텍스트로 반환한다 (§10 Gotcha "에이전트 결과가 메인 컨텍스트를 채운다" 의 실행 규칙). grep sweep·로그 trawl 같은 noisy 탐색일수록 필수.

**Bad:**

```text
오케스트레이터 → 20+ 서브에이전트 동시 spawn → 각자 raw 출력 전체 반환 → 메인 컨텍스트 폭주 + 비용 급증
탐색 에이전트 → 구현 전 Figma 노드 50회 재조회 → 진전 없이 stall → 사용자 중단
```

**Good:**

```text
오케스트레이터 → 5개 batch spawn (시간 우선 명시) → 각자 findings 요약만 반환 → 다음 batch
탐색 에이전트 → exploration budget 도달 → 현재 발견 요약 + 진행 방향 사용자 확인 후 구현
```

**Cross-Surface Parity:** 본 원칙은 skill-design-guide §9 "Long-Running Skills — 중첩 스킬 호출 간 반환 데이터 최소화" 와 짝 (스킬 측은 checkpoint·반환 최소화, 에이전트 측은 fan-out 상한·exploration budget).

**이름 구분 (필수):** 이 절의 **Exploration Budget** 은 *산출 이전*의 read-only 탐색에 쓰는 turn·비용 상한이다. skill-design-guide §5.6 의 **Variant Budget** 은 *산출물 자체*의 개수 상한과 변주 축 고정으로 **다른 개념**이다. 이름이 비슷해 혼동되므로 두 용어를 섞어 쓰지 마라 — §12 parity item 9 는 "동일 개념 공유" 가 아니라 "구분 유지" 가 내용이다.

---

## 8. 호출 품질이 성패를 가른다

> **출처:** [Claude Code Sub-Agent Best Practices](https://claudefa.st/blog/guide/agents/sub-agent-best-practices) — "Most sub-agent failures stem from poor invocation, not execution failures."

에이전트 실패의 대부분은 **실행이 아니라 호출 품질** 문제다.

### Bad

```text
"인증 고쳐줘"
```

### Good

```text
"OAuth 리다이렉트 루프를 수정해라. 로그인 성공 후 /dashboard 대신
/login으로 리다이렉트되는 문제. src/lib/auth.ts의 auth 미들웨어 참조."
```

**좋은 호출의 4요소:**
1. **컨텍스트 밀도** — 관련 배경 정보
2. **구체적 범위** — 어떤 파일, 어떤 기능
3. **파일 참조** — 정확한 경로
4. **성공 기준** — 무엇이 "완료"인지

---

## 9. 영속 메모리 — 대화를 넘어서는 학습

> **출처:** [Claude Code Sub-agents 공식 문서](https://code.claude.com/docs/en/sub-agents)

```yaml
memory: project   # user | project | local
```

| 범위 | 위치 | 사용 시기 |
| ------ | ------ | ----------- |
| `user` | `~/.claude/agent-memory/{name}/` | 모든 프로젝트에 걸친 학습 |
| `project` | `.claude/agent-memory/{name}/` | 프로젝트별 지식 (git 공유 가능) |
| `local` | `.claude/agent-memory-local/{name}/` | 프로젝트별, git 미포함 |

메모리 활성화 시 에이전트의 시스템 프롬프트에 메모리 디렉토리 읽기/쓰기 지침이 자동 추가된다.

**팁:**

- 작업 시작 전: "메모리를 확인하고 이전에 발견한 패턴을 참고해라"
- 작업 완료 후: "배운 것을 메모리에 저장해라"
- 시간이 지나면 점점 더 효과적인 에이전트가 된다

---

## 10. Gotchas — 에이전트에서 반복되는 실수

> **출처:** 종합 (공식 문서 + 커뮤니티 경험)

- **중첩은 깊이 제한이 있다 (금지가 아니다).** 서브에이전트도 자기 아래로 위임할 수 있으나 기본 3 층에서 끊긴다 (§4 참조). 한계 층의 에이전트는 `Agent` 도구를 잃고 직접 일하므로, 4 층째 위임을 전제한 설계는 조용히 단층으로 접힌다 — 깊이를 설계 가정으로 삼지 마라
- **플러그인 에이전트는 `hooks`, `mcpServers`, `permissionMode`를 지원하지 않는다.** 필요하면 `.claude/agents/`로 복사해라
- **과도한 병렬화는 토큰 낭비다.** 10개 에이전트를 단순 작업에 띄우지 마라. 관련 작업을 묶어라
- **컨텍스트 핸드오프 실패.** 순차 체이닝에서 이전 에이전트의 결과를 다음 에이전트에 전달하지 않으면 의존성 체인이 깨진다
- **백그라운드 에이전트는 사용자에게 질문할 수 없다.** `AskUserQuestion` 호출이 실패한다. 권한은 미리 승인해야 한다
- **에이전트 결과가 메인 컨텍스트를 채운다.** 많은 에이전트가 상세한 결과를 반환하면 메인 컨텍스트가 빠르게 소진된다

### Reviewer/Evaluator 에이전트 전용 Gotchas

- **정적 Grep만으로 PASS를 주지 마라.** 파일 존재 여부나 키워드 포함 여부를 확인하는 것은 L1/L2 수준이다. Reviewer/Evaluator 에이전트는 반드시 **L3 커버리지** — `Read`로 파일 내용을 실제로 읽거나, `Bash`로 명령을 실행하여 결과를 확인 — 까지 수행해야 한다.

  ```text
  L1: 파일이 존재하는가? (Glob/Grep)
  L2: 파일에 특정 키워드가 있는가? (Grep)
  L3: 파일의 실제 내용이 조건을 충족하는가? (Read) 또는
      명령 실행 결과가 기대값과 일치하는가? (Bash)  ← 여기까지 해야 PASS
  ```

- **cross-kit 키워드 중복은 Grep만으로 탐지되지 않는다.** 두 스킬의 description에서 트리거 키워드를 정규식으로 추출한 뒤 set intersection으로 정확히 비교해야 한다. 단순히 "같은 단어가 있는지" Grep하면 부분 문자열 매칭 오탐이 발생한다.

- **계약 모호성 방지 — 평가 이전에 조건의 이진 판정 가능성을 확인하라.** 본 원칙은 최상위 §3.5 "Binary Decidability Pre-Check" 로 승격되었다. 평가 시작 전 §3.5 체크리스트를 필수 수행한다

- **Unverifiable 조건 정책 — 인프라 부재로 검증 불가한 조건의 일관 처리.** MCP 서버 미설정(예: `mcp_server: null` 로 인해 Figma read-back 불가), 런타임 미실행, 도구 미설치 등의 이유로 **실제 검증이 불가능한 조건** 이 있을 때는 아래 4 항 필수:
  1. **명시적 마커 표기** — 해당 조건 결과에 `[정적]` 또는 `[미검증]` 마커를 붙이고, 무엇 때문에 검증이 불가한지 한 줄로 기재 (예: `[미검증] mcp_server: null — Figma 시각 대조 불가`)
  2. **2건 이상 누적 시 REJECT** — 한 sprint 에 미검증 항목이 2건 이상이면 verdict 는 REJECT 로 귀결한다 (harness 전역 관습). 부분 L2 만 검증된 조건도 미검증 집계 대상
  3. **조용한 PASS 금지** — 검증을 건너뛰고 정적 증거만으로 PASS 를 주는 것은 엄격히 금지. 검증 불가면 FAIL 또는 `[미검증]` 중 하나로 표기하되 PASS 처리 금지
  4. **생성자의 완료 주장을 증거로 취급 금지** — 구현자가 "동작 확인함" 이라고 쓴 문장은 상태 검증이 아니다. 명시적 완료 주장을 포함한 자기평가 코딩 에이전트 궤적(AppWorld)에서 **실패의 75.8% 가 false success**(실패했는데 성공했다고 단언) 였고, 판정에 쓰인 신호는 검증된 상태 변화가 아니라 "자신 있는 마무리 문장" 같은 표면 프록시였다 ([arxiv:2606.09863](https://arxiv.org/abs/2606.09863)). 같은 연구에서 LLM 판정자는 AUROC 0.54~0.65 에 그쳤다 — 평가자는 주장이 아니라 **도구 출력·상태 변화**를 근거로 삼아야 한다

  **Cross-Surface Parity:** 본 정책의 생성(스킬) 측 짝은 skill-design-guide §3.7 "Completion Evidence Gate" 다. 마커 표기법과 2 건 임계값은 양쪽이 동일 규약을 쓴다 — 한쪽만 표기하면 미검증이 평가 시점에야 드러나 iteration 이 낭비된다.

  **실패 사례 (이 정책 없이 발생):**

  - fit-pal 2026-04-21: UI-04, LG-04, DG-04 세 조건에서 Figma MCP read-back 불가 → 에이전트가 조용히 partial PASS 부여 → 사용자가 추후 실제 차이 발견 → 재작업
  - 원인: 미검증 마커 없이 PASS 부여 → 계약 해석 레벨에서 이슈 불가시

- **사용자 실패 보고 우선 — 반박하지 말고 `REOPENED` 로 되돌려라.** 평가자가 PASS 를 준 항목에 대해 사용자가 "아직 깨져 있다" 고 보고하면, 그 항목의 상태는 PASS 가 아니라 **`REOPENED`** 다. 에이전트의 테스트·스냅샷은 "내 환경에서의 관측" 일 뿐이며 사용자 관측의 반박 근거가 아니다 — 상태 검증은 self-report 가 아니라 **target system** 을 봐야 한다 ([OCI Agent Evaluation Framework](https://blogs.oracle.com/ai-and-datascience/oci-agent-evaluation-framework)). 실사용 20,574 세션 관측에서 가시적 해소의 91.49% 가 사용자의 명시적 교정을 필요로 했고 ([arxiv:2605.29442](https://arxiv.org/html/2605.29442)), 자기평가 궤적에서는 실패의 75.8% 가 false success 였다 ([arxiv:2606.09863](https://arxiv.org/html/2606.09863)). 절차는 3 단계다:
  1. **오라클 유효성부터 의심한다.** 내 판정이 사용자가 보는 것을 재고 있었는지 6 축(URL·경로 / 브랜치·커밋 / viewport / 디바이스·플랫폼 / auth·cache / 데이터 상태)으로 대조한다. 값싼 축부터 확인하고 비싼 축은 앞 축이 전부 일치할 때 넘어간다
  2. **재판정한다.** 재현되면 원 PASS 를 취소하고 FAIL 로 바꾸되, 이전 근거는 지우지 말고 "그때 그 오라클로는 통과했다" 로 남긴다 — 오라클 결함 자체가 다음 계약의 개선 제안이다
  3. **완료로 되돌리는 조건은 3 택뿐이다** — (a) 사용자 관측을 재현하고 수정 후 같은 조건에서 재검증한 출력 인용 (b) 재현되지 않는 이유를 6 축 중 어느 축의 값 차이인지로 특정 (c) 사용자가 직접 수정 확인

  **오독 금지:** 이것은 "사용자 보고를 무조건 사실로 인정하라" 는 규칙이 **아니다.** 정확한 규약은 **완료 판정을 보류하고 오라클 유효성을 먼저 의심한다** 이며, 원인이 사용자 환경(스테일 빌드, 캐시)으로 밝혀지는 것도 위 (b) 로 정상 종결이다.

  **트레이드오프:** 신뢰는 회복되지만 환경 재현 비용이 든다. 그래서 6 축 대조는 값싼 축부터 하고, 재현 불가 시에도 "환경 문제 같다" 는 서술이 아니라 **어느 축의 어떤 값이 달랐는지**를 요구한다.

  **Cross-Surface Parity:** 본 Gotcha 의 생성(스킬) 측 짝은 skill-design-guide §3.8 "User-Reported Failure Gate" 다 (§12 parity item 8). 생성 측이 완료를 고집하고 평가 측만 REOPENED 로 다루면 두 판정이 충돌해 사용자가 중재자가 된다.

- **Self-Evaluator Rule-by-Rule Audit — 위임 없이 자기 규칙으로 전수 대조하는 패스.** (2026-07 근거 정정: 과거 이 항목은 하위 위임이 막혀 있다는 전제 위에 서술됐으나 중첩은 이제 허용된다 — §4. 이 기법이 여전히 유효한 근거는 중첩 제약이 아니라 **비용·지연 대비 효과**와 **깊이 한계에서 위임이 조용히 접히는 위험**이다. 중첩 QA 가 필요하면 스폰해도 되지만, 자기 규칙 대조는 스폰 없이도 대부분의 위반을 잡는다.) 카이젠 Phase 처럼 **서브에이전트 내부에서 QA 를 돌려야 하는 경우** Phase subagent 가 **자기 산출물을 자기 규칙 리스트로** 전수 대조하는 self-evaluator pass 를 추가한다. 2026-04-24 카이젠 사이클이 Phase 1~11 1회 iteration APPROVE 를 달성한 핵심 기법으로 `.harness/.meta/orchestrator-audit-log.md` 에 기록되어 있다. **자기 평가는 외부 평가의 대체가 아니다** — Final 단계에서는 별도 evaluator 에이전트의 독립 평가가 여전히 필수. self-audit 시 **최종 산출물뿐 아니라 중간 결정·도구 상태까지 규칙에 대조** 한다 — LLM 은 유창하지만 제약을 위반하는 추론을 내기 쉽고 최종 성공만으로는 위반이 가려지기 때문이다 ([Verify Before You Commit — arxiv:2604.08401](https://arxiv.org/pdf/2604.08401)).

---

## 11. 적용 사례 — 이 프로젝트의 에이전트 분석

### 현재 에이전트 구조

```text
harness/agents/
└── qa-evaluator.md          # 단일 에이전트
```

### 잘 된 점

**독립 컨텍스트에서 실행.** "Generator(구현자)와 별도 컨텍스트에서 실행된다" — 같은 컨텍스트에서 생성+검증의 편향을 방지한다. 이는 Anthropic의 평가자-최적화자 패턴과 정확히 일치한다.

**역할이 명확하다.** "문제를 찾는 것이 유일한 역할이다" — 역할 혼합 없이 단일 책임.

**설정 기반.** `project.yaml`에서 카테고리, 안티패턴, 검증 절차를 읽는다. 에이전트에 프로젝트별 지식을 하드코딩하지 않는다.

**도구가 적절히 제한되어 있다.** `tools: Read, Grep, Glob, Bash` — 파일 수정(Edit, Write) 불가. QA 평가자가 코드를 수정하면 안 되기 때문이다.

### 개선 기회

**모델 선택 근거가 없다.** `model: sonnet`이 설정되어 있지만 왜 sonnet인지 문서화되지 않았다. 아키텍처적 판단이 필요한 평가라면 opus가 나을 수 있고, 단순 체크리스트면 haiku로 충분할 수 있다.

**영속 메모리가 없다.** QA Evaluator가 반복적으로 발견하는 패턴(예: "이 프로젝트에서 자주 실패하는 조건 유형")을 기억하면 점점 더 정확한 평가가 가능하다.

**description에 비트리거 조건이 없다.** 스킬 설계 가이드(Section 4)에서 권장하는 비트리거 조건이 에이전트 description에도 필요하다. 예: "단순 텍스트 수정이나 설정 변경에는 사용하지 않는다."

### 성장 경로

| 현재 상태 | 다음 단계 | 트리거 |
| ----------- | ----------- | -------- |
| 단일 에이전트 | 역할별 에이전트 분리 (리뷰어, 테스터 등) | 에이전트 유형이 3개 이상 필요할 때 |
| 메모리 없음 | `memory: project` 추가 | 같은 실패 패턴이 반복 관찰될 때 |
| 모델 고정 | 작업 복잡도별 모델 분기 | 비용 최적화 필요 시 |

---

## 12. 원칙 전수성 · Cross-Surface Parity Checklist

> **배경 (meta-issue):** skill-design-guide §3.5 "계약 모호성 방지 원칙" 이 이 가이드에 전수되지 않아 design-kit PH-01 REJECT 가 발생했다. 이 가이드 레벨의 변경이 파생 산출물(qa-evaluation-guide, qa-evaluator 에이전트, 하위 리뷰어 에이전트)로 자동 전파되지 않는 구조적 공백을 보완한다.

### 원칙

에이전트 설계 가이드가 개정되면, **스킬 설계 가이드 · contract-design-guide · qa-evaluation-guide · 하위 에이전트(.md)** 에 대응 원칙이 존재하는지 자동 체크한다. 전파 필요성 판정 → 즉시 복제.

### 전수 대상 parity items (9개)

두 가이드(agent-design-guide, skill-design-guide)는 아래 9개 항목을 **동일한 개념 · 동일한 용어** 로 다룬다 (대부분은 양쪽 공유, item 9 는 구분 대상):

| # | Parity Item | agent-design-guide 위치 | skill-design-guide 대응 위치 |
| --- | ------------- | ------------------------ | ------------------------------ |
| 1 | Binary Decidability / 계약 모호성 방지 | §3.5 (Binary Decidability Pre-Check) | §3.5 (QA 계약과 1:1 매칭) |
| 2 | 트리거 키워드 배타성 (substring 포함) | §3 "Sibling Agent 트리거 키워드 배타성" | §4 (트리거 키워드 중복 방지) |
| 3 | 검증 가능한 성공 기준 / L3 커버리지 | §10 Reviewer/Evaluator Gotchas (L3) | §3.6 (Give a way to verify) |
| 4 | Rule-by-rule audit before completion | §10 Reviewer 전수 대조 | §3.6 (Rule-by-Rule Audit) |
| 5 | Unverifiable / degraded-mode 정책 | §10 Unverifiable 조건 정책 | §3.7 (Completion Evidence Gate) |
| 6 | Fan-out 상한 / Exploration Budget ↔ 반환 데이터 최소화 | §7 (Fan-out 상한 · Exploration Budget) | §9 (Long-Running Skills — 반환 데이터 최소화) |
| 7 | Enforcement 등급 (E1/E2/E3) | §6 패턴 7 (훅 = E3 결정론적 게이트의 구현체) | §3.7 (Enforcement 3 등급 · 승급 규칙 · 등급 원장) |
| 8 | User-Reported Failure Gate | §10 (사용자 실패 보고 우선 — `REOPENED`) | §3.8 (사용자 관측은 재현 대상) |
| 9 | Exploration Budget ↔ Variant Budget | §7 (탐색 turn 예산) | §5.6 (산출물 개수·축 고정) — **짝이 아니라 구분 대상** |

**Item 8·9 는 2026-08 사이클 신규다.** Item 8 은 생성 측이 완료를 고집하고 평가 측만 REOPENED 로 다루면 두 판정이 충돌해 사용자가 중재자가 되기 때문에 양면으로 둔다. **Item 9 만 성격이 다르다** — 동일 개념을 공유하는 것이 아니라 **이름이 비슷한 다른 개념**이라 양쪽 절이 서로를 참조해 용어 혼동을 막는 것이 parity 의 내용이다. Item 7 의 등급 원장은 skill-design-guide 측에만 두고 이 가이드는 참조만 한다 — 원장이 둘로 갈리면 같은 원칙이 두 등급을 갖게 된다.

**Item 5 는 2026-07 사이클에서 양면으로 전환되었다** — 과거에는 "평가자 전용" 이었으나, 생성 측이 `[미검증]` 을 표기하지 않으면 평가 시점에야 미검증이 드러나 iteration 이 낭비된다. 마커 표기법과 2 건 임계값은 양쪽이 동일 규약을 쓴다. Item 6 은 에이전트 측 fan-out/exploration 통제와 스킬 측 반환 최소화가 토큰 경제라는 동일 목적의 짝 원칙. Item 7 은 "원칙을 어떤 강도로 강제할지" 를 판정하는 공통 틀로, 에이전트 측에서는 훅(PostToolUse/PreToolUse)이 E3 게이트의 구현 형태다. 나머지 1~4 도 양쪽 존재.

### 개정 시 체크리스트

agent-design-guide.md 를 편집할 때:

- [ ] 새 원칙을 추가했는가? → skill-design-guide 에 대응 항목이 필요한지 판정
- [ ] 원칙 네이밍(카테고리 ID, 섹션명) 을 변경했는가? → qa-evaluation-guide · qa-evaluator.md · 하위 리뷰어 에이전트에서 동일 네이밍 사용 중인지 Grep 하여 동기화
- [ ] Bad/Good 예시 또는 실패 사례를 추가했는가? → 대응 원칙이 있는 다른 가이드도 동일 형태의 예시 포함하도록 업데이트
- [ ] frontmatter `version` 을 bump 했는가? → 대응 파일들도 같은 방향으로 bump

### 실패 패턴 (이 원칙 없이 발생한 실제 REJECT)

- **PH-01 (design-kit, 2026-04)**: skill-design-guide §3.5 "계약 모호성 방지" 가 이 가이드에 누락 → 계약 작성자는 원칙을 알지만 평가자는 원칙 불명 → 평가 결과 해석 충돌 → REJECT
- **SK-13 (backend-kit, infra-kit)**: References 섹션이 skill-design-guide 는 요구하지만 하위 스킬(backend-kaizen, infra-kaizen) SKILL.md 에 누락 → 상위 guide 의 원칙이 하위 surface 에 전파되지 않음

### Downstream 파일 전파 범위

본 가이드 개정이 영향 줄 수 있는 하위 surface:

- `harness/agents/qa-evaluator.md` — reviewer 전용 Gotcha 변경 시 반영
- `harness/docs/guides/qa-evaluation-guide.md` — 평가 방법론 원칙 변경 시
- `harness/docs/guides/contract-design-guide.md` — 계약 모호성 · 태그 · 키워드 배타성 변경 시
- `*-kit/agents/*-reviewer.md` (design-reviewer, backend-reviewer, infra-reviewer, widget-inspector, widget-inspector-react, animation-architect-react, rust-reviewer, react-reviewer) — 공통 Gotcha 또는 도구 스코핑 변경 시

---

## 요약

| 원칙 | 핵심 |
| ------ | ------ |
| 단순함 우선 | 스킬로 충분하면 에이전트를 만들지 마라 |
| description은 트리거 | "언제 위임할지"를 구체적으로 명시 |
| Undertrigger 방지 | `use proactively` 키워드로 자동 위임 장려 |
| **Substring 배타성** | sibling agent 와 키워드 set intersection + substring 공집합 |
| 최소 권한 | 필요한 도구만 부여 |
| Agent 스코핑 | `Agent(agent_type)` 로 스폰 가능 서브에이전트 화이트리스트 |
| 모델 최적화 | 작업 복잡도에 맞는 모델 선택 |
| 호출 품질 | 컨텍스트·범위·파일참조·성공기준 4요소 |
| 독립 컨텍스트 | 생성과 평가는 분리 |
| **중첩 3 층** | 서브에이전트도 위임 가능하나 기본 3 층에서 끊김 · 깊이를 설계 가정으로 삼지 마라 (§4) |
| **하드 리밋** | 동시 20 · 세션 200 · 깊이 3 — 자체 예산은 항상 이보다 작게 (§7) |
| 영속 메모리 | 대화를 넘어서 학습시켜라 |
| 6가지 패턴 | 체이닝/라우팅/병렬화/오케스트레이터/평가자/계획-실행 중 선택 |
| **Fan-out 상한 / Exploration Budget** | §7 — 병렬 spawn 기본 5개 이하 · 토큰vs시간 trade-off 명시 · summary-only 반환 |
| **Binary Decidability** | §3.5 — 평가 시작 전 이진 판정 가능성 전수 점검 (최상위 섹션 승격) |
| **Unverifiable 정책** | `[미검증]` 마커 · 2건 누적 REJECT · 조용한 PASS 금지 · 생성자의 완료 주장은 증거 아님 |
| **사용자 보고 우선** | §10 — 사용자 실패 보고는 `REOPENED`. 반박 금지 · 오라클 6 축부터 대조 |
| **Variant Budget 구분** | §7 Exploration Budget(탐색 turn) 과 skill §5.6 Variant Budget(산출물 수·축) 은 다른 개념 |
| **Cross-Surface Parity** | agent/skill/contract/eval 가이드의 원칙 전수 검토 (§12) |

---

## 출처

- [Create custom subagents — Claude Code Docs](https://code.claude.com/docs/en/sub-agents) (2026-08 재확인 — frontmatter 15 종 · 중첩 기본 3 층)
- [Skill Authoring Best Practices — Claude API Docs](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) (2026-04 최신)
- [Building Effective Agents — Anthropic Research](https://www.anthropic.com/research/building-effective-agents)
- [Claude Code Sub-Agent Best Practices — claudefa.st](https://claudefa.st/blog/guide/agents/sub-agent-best-practices)
- [Best Practices for Claude Code subagents — PubNub](https://www.pubnub.com/blog/best-practices-for-claude-code-sub-agents/)
- [Claude Code Subagents — Medium (Apr 2026)](https://medium.com/@sathishkraju/claude-code-subagents-the-complete-guide-to-ai-agent-delegation-d0a9aba419d0)
- [Claude Code Workflows and Best Practices 2026](https://smart-webtech.com/blog/claude-code-workflows-and-best-practices/)
- [Designing LLM-based MAS for SE — arxiv:2511.08475](https://arxiv.org/abs/2511.08475)
- [LLM Agent Evaluation Survey — arxiv:2503.16416](https://arxiv.org/abs/2503.16416)
- [agentic-code Quality Gates Framework](https://github.com/shinpr/agentic-code)
- [Dive into Claude Code: Design Space of AI Agent Systems — arxiv:2604.14228](https://arxiv.org/html/2604.14228v1) (2026-06)
- [Claude Code Agents 2026 — CloudZero](https://www.cloudzero.com/blog/claude-code-agents/) (2026-06)
- [Verify Before You Commit: Faithful Reasoning via Self-Auditing — arxiv:2604.08401](https://arxiv.org/pdf/2604.08401) (2026-06)
- [From Confident Closing to Silent Failure: Characterizing False Success in LLM Agents — arxiv:2606.09863](https://arxiv.org/abs/2606.09863) (2026-06)
- [Reason Less, Verify More: Deterministic Gates — arxiv:2607.07405](https://arxiv.org/html/2607.07405v1) (2026-07)
- [How Coding Agents Fail Their Users: 20,574 Real-World Sessions — arxiv:2605.29442](https://arxiv.org/abs/2605.29442) (2026-05)
- [OCI Agent Evaluation Framework — Oracle](https://blogs.oracle.com/ai-and-datascience/oci-agent-evaluation-framework) (§10 target system 검증)
