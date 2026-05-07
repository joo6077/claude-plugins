---
title: Claude Code 에이전트 설계 가이드
version: 1.3.0
last_updated: 2026-05-07
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
|------|-----------|---------------|
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
|------|------|----------|
| `--agents` CLI 플래그 | 현재 세션만 | 1 (최고) |
| `.claude/agents/` | 현재 프로젝트 | 2 |
| `~/.claude/agents/` | 모든 프로젝트 | 3 |
| 플러그인 `agents/` | 플러그인 활성화된 곳 | 4 (최저) |

**프로젝트 에이전트**는 git에 체크인하여 팀과 공유한다.

### frontmatter 전체 필드

> **출처:** [Create custom subagents — Supported frontmatter fields](https://code.claude.com/docs/en/sub-agents#supported-frontmatter-fields) (2026-04)

| 필드 | 필수 | 설명 |
|------|------|------|
| `name` | 예 | 고유 식별자 (소문자, 하이픈) |
| `description` | 예 | 언제 위임할지 Claude가 판단하는 기준 |
| `tools` | 아니오 | 허용 도구 목록. 생략 시 전체 상속 |
| `disallowedTools` | 아니오 | 차단 도구 목록 |
| `model` | 아니오 | `sonnet`, `opus`, `haiku`, 풀 model ID(예: `claude-opus-4-6`), `inherit` (기본값) |
| `permissionMode` | 아니오 | `default`, `acceptEdits`, `dontAsk`, `bypassPermissions`, `plan` |
| `maxTurns` | 아니오 | 최대 에이전트 턴 수 |
| `skills` | 아니오 | 시작 시 주입할 스킬 목록 (전체 내용이 context 에 inject 됨, 스킬 invoke 가능성만 주어지는 게 아님) |
| `mcpServers` | 아니오 | 이 에이전트 전용 MCP 서버 (parent 세션에서 숨기고 싶을 때 inline 정의) |
| `hooks` | 아니오 | 라이프사이클 훅 (`PreToolUse`, `PostToolUse`, `Stop` → 런타임에 `SubagentStop` 으로 변환) |
| `memory` | 아니오 | 영속 메모리: `user`, `project`, `local` |
| `background` | 아니오 | `true`면 백그라운드 실행 |
| `effort` | 아니오 | `low`, `medium`, `high`, `max` |
| `isolation` | 아니오 | `worktree`면 격리된 git worktree에서 실행 |
| `initialPrompt` | 아니오 | 에이전트 시작 시 자동으로 주입되는 초기 사용자 메시지 |
| `color` | 아니오 | 터미널 UI 에 표시되는 에이전트 색상 (시각 구분용) |

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
|------|------|------|
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

### Agent(agent_type) — 스폰 가능 서브에이전트 제한

> **출처:** [Create custom subagents — Allow only specific subagents to spawn others](https://code.claude.com/docs/en/sub-agents) (2026-04)

메인 스레드 에이전트(`claude --agent` 로 실행)는 `Agent` 도구로 다른 서브에이전트를 스폰할 수 있다. 스폰 가능한 서브에이전트를 **화이트리스트로 제한** 하려면 `tools` 필드에 `Agent(agent_type)` 문법을 사용한다.

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
- 서브에이전트 자체는 다른 서브에이전트를 스폰할 수 없으므로 `Agent(agent_type)` 은 **메인 스레드 에이전트에만** 적용된다

---

## 5. 모델 선택 전략

> **출처:** [Claude Code Sub-agents Best Practices](https://claudefa.st/blog/guide/agents/sub-agent-best-practices), [Claude Code 공식 문서](https://code.claude.com/docs/en/sub-agents)

**작업 복잡도에 맞는 모델을 선택**하여 비용을 최적화한다.

| 작업 유형 | 모델 | 이유 |
|-----------|------|------|
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

## 6. 다섯 가지 에이전트 디자인 패턴

> **출처:** [Building Effective Agents](https://www.anthropic.com/research/building-effective-agents)

Anthropic이 식별한 핵심 패턴. 에이전트를 설계할 때 이 중 하나를 기반으로 한다.

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
|------|------|-----------|
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

- **서브에이전트는 다른 서브에이전트를 생성할 수 없다.** 중첩 위임이 필요하면 메인 대화에서 체이닝하거나 스킬을 사용해라
- **플러그인 에이전트는 `hooks`, `mcpServers`, `permissionMode`를 지원하지 않는다.** 필요하면 `.claude/agents/`로 복사해라
- **과도한 병렬화는 토큰 낭비다.** 10개 에이전트를 단순 작업에 띄우지 마라. 관련 작업을 묶어라
- **컨텍스트 핸드오프 실패.** 순차 체이닝에서 이전 에이전트의 결과를 다음 에이전트에 전달하지 않으면 의존성 체인이 깨진다
- **백그라운드 에이전트는 사용자에게 질문할 수 없다.** `AskUserQuestion` 호출이 실패한다. 권한은 미리 승인해야 한다
- **에이전트 결과가 메인 컨텍스트를 채운다.** 많은 에이전트가 상세한 결과를 반환하면 메인 컨텍스트가 빠르게 소진된다

### Reviewer/Evaluator 에이전트 전용 Gotchas

- **정적 Grep만으로 PASS를 주지 마라.** 파일 존재 여부나 키워드 포함 여부를 확인하는 것은 L1/L2 수준이다. Reviewer/Evaluator 에이전트는 반드시 **L3 커버리지** — `Read`로 파일 내용을 실제로 읽거나, `Bash`로 명령을 실행하여 결과를 확인 — 까지 수행해야 한다.

  ```
  L1: 파일이 존재하는가? (Glob/Grep)
  L2: 파일에 특정 키워드가 있는가? (Grep)
  L3: 파일의 실제 내용이 조건을 충족하는가? (Read) 또는
      명령 실행 결과가 기대값과 일치하는가? (Bash)  ← 여기까지 해야 PASS
  ```

- **cross-kit 키워드 중복은 Grep만으로 탐지되지 않는다.** 두 스킬의 description에서 트리거 키워드를 정규식으로 추출한 뒤 set intersection으로 정확히 비교해야 한다. 단순히 "같은 단어가 있는지" Grep하면 부분 문자열 매칭 오탐이 발생한다.

- **계약 모호성 방지 — 평가 이전에 조건의 이진 판정 가능성을 확인하라.** 본 원칙은 최상위 §3.5 "Binary Decidability Pre-Check" 로 승격되었다. 평가 시작 전 §3.5 체크리스트를 필수 수행한다

- **Unverifiable 조건 정책 — 인프라 부재로 검증 불가한 조건의 일관 처리.** MCP 서버 미설정(예: `mcp_server: null` 로 인해 Figma read-back 불가), 런타임 미실행, 도구 미설치 등의 이유로 **실제 검증이 불가능한 조건** 이 있을 때는 아래 3 항 필수:
  1. **명시적 마커 표기** — 해당 조건 결과에 `[정적]` 또는 `[미검증]` 마커를 붙이고, 무엇 때문에 검증이 불가한지 한 줄로 기재 (예: `[미검증] mcp_server: null — Figma 시각 대조 불가`)
  2. **2건 이상 누적 시 REJECT** — 한 sprint 에 미검증 항목이 2건 이상이면 verdict 는 REJECT 로 귀결한다 (harness 전역 관습). 부분 L2 만 검증된 조건도 미검증 집계 대상
  3. **조용한 PASS 금지** — 검증을 건너뛰고 정적 증거만으로 PASS 를 주는 것은 엄격히 금지. 검증 불가면 FAIL 또는 `[미검증]` 중 하나로 표기하되 PASS 처리 금지

  **실패 사례 (이 정책 없이 발생):**
  - fit-pal 2026-04-21: UI-04, LG-04, DG-04 세 조건에서 Figma MCP read-back 불가 → 에이전트가 조용히 partial PASS 부여 → 사용자가 추후 실제 차이 발견 → 재작업
  - 원인: 미검증 마커 없이 PASS 부여 → 계약 해석 레벨에서 이슈 불가시

- **Self-Evaluator Rule-by-Rule Audit — 서브에이전트 중첩 불가의 공식 우회법.** 서브에이전트가 다른 서브에이전트를 spawn 할 수 없으므로, 카이젠 Phase 처럼 **서브에이전트 내부에서 QA 를 돌려야 하는 경우** Phase subagent 가 **자기 산출물을 자기 규칙 리스트로** 전수 대조하는 self-evaluator pass 를 추가한다. 2026-04-24 카이젠 사이클이 Phase 1~11 1회 iteration APPROVE 를 달성한 핵심 기법으로 `.harness/.meta/orchestrator-audit-log.md` 에 기록되어 있다. **자기 평가는 외부 평가의 대체가 아니다** — Final 단계에서는 별도 evaluator 에이전트의 독립 평가가 여전히 필수.

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
|-----------|-----------|--------|
| 단일 에이전트 | 역할별 에이전트 분리 (리뷰어, 테스터 등) | 에이전트 유형이 3개 이상 필요할 때 |
| 메모리 없음 | `memory: project` 추가 | 같은 실패 패턴이 반복 관찰될 때 |
| 모델 고정 | 작업 복잡도별 모델 분기 | 비용 최적화 필요 시 |

---

## 12. 원칙 전수성 · Cross-Surface Parity Checklist

> **배경 (meta-issue):** skill-design-guide §3.5 "계약 모호성 방지 원칙" 이 이 가이드에 전수되지 않아 design-kit PH-01 REJECT 가 발생했다. 이 가이드 레벨의 변경이 파생 산출물(qa-evaluation-guide, qa-evaluator 에이전트, 하위 리뷰어 에이전트)로 자동 전파되지 않는 구조적 공백을 보완한다.

### 원칙

에이전트 설계 가이드가 개정되면, **스킬 설계 가이드 · contract-design-guide · qa-evaluation-guide · 하위 에이전트(.md)** 에 대응 원칙이 존재하는지 자동 체크한다. 전파 필요성 판정 → 즉시 복제.

### 전수 대상 parity items (5개)

두 가이드(agent-design-guide, skill-design-guide)는 아래 5개 항목을 **동일한 개념 · 동일한 용어** 로 공유한다:

| # | Parity Item | agent-design-guide 위치 | skill-design-guide 대응 위치 |
|---|-------------|------------------------|------------------------------|
| 1 | Binary Decidability / 계약 모호성 방지 | §3.5 (Binary Decidability Pre-Check) | §3.5 (QA 계약과 1:1 매칭) |
| 2 | 트리거 키워드 배타성 (substring 포함) | §3 "Sibling Agent 트리거 키워드 배타성" | §4 (트리거 키워드 중복 방지) |
| 3 | 검증 가능한 성공 기준 / L3 커버리지 | §10 Reviewer/Evaluator Gotchas (L3) | §3.6 (Give a way to verify) |
| 4 | Rule-by-rule audit before completion | §10 Reviewer 전수 대조 | §3.6 (Rule-by-Rule Audit) |
| 5 | Unverifiable / degraded-mode 정책 | §10 Unverifiable 조건 정책 | — (에이전트 전용) |

Item 5 는 평가자 행동에만 관련되므로 skill-design-guide 에는 존재하지 않는 것이 정상. 다른 4 개는 양쪽 존재.

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
|------|------|
| 단순함 우선 | 스킬로 충분하면 에이전트를 만들지 마라 |
| description은 트리거 | "언제 위임할지"를 구체적으로 명시 |
| Undertrigger 방지 | `use proactively` 키워드로 자동 위임 장려 |
| **Substring 배타성** | sibling agent 와 키워드 set intersection + substring 공집합 |
| 최소 권한 | 필요한 도구만 부여 |
| Agent 스코핑 | `Agent(agent_type)` 로 스폰 가능 서브에이전트 화이트리스트 |
| 모델 최적화 | 작업 복잡도에 맞는 모델 선택 |
| 호출 품질 | 컨텍스트·범위·파일참조·성공기준 4요소 |
| 독립 컨텍스트 | 생성과 평가는 분리 |
| 중첩 불가 | 서브에이전트는 다른 서브에이전트를 spawn 할 수 없음 |
| 영속 메모리 | 대화를 넘어서 학습시켜라 |
| 6가지 패턴 | 체이닝/라우팅/병렬화/오케스트레이터/평가자/계획-실행 중 선택 |
| **Binary Decidability** | §3.5 — 평가 시작 전 이진 판정 가능성 전수 점검 (최상위 섹션 승격) |
| **Unverifiable 정책** | `[미검증]` 마커 · 2건 누적 REJECT · 조용한 PASS 금지 |
| **Cross-Surface Parity** | agent/skill/contract/eval 가이드의 원칙 전수 검토 (§12) |

---

## 출처

- [Create custom subagents — Claude Code Docs](https://code.claude.com/docs/en/sub-agents) (2026-04 최신)
- [Skill Authoring Best Practices — Claude API Docs](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) (2026-04 최신)
- [Building Effective Agents — Anthropic Research](https://www.anthropic.com/research/building-effective-agents)
- [Claude Code Sub-Agent Best Practices — claudefa.st](https://claudefa.st/blog/guide/agents/sub-agent-best-practices)
- [Best Practices for Claude Code subagents — PubNub](https://www.pubnub.com/blog/best-practices-for-claude-code-sub-agents/)
- [Claude Code Subagents — Medium (Apr 2026)](https://medium.com/@sathishkraju/claude-code-subagents-the-complete-guide-to-ai-agent-delegation-d0a9aba419d0)
- [Claude Code Workflows and Best Practices 2026](https://smart-webtech.com/blog/claude-code-workflows-and-best-practices/)
- [Designing LLM-based MAS for SE — arxiv:2511.08475](https://arxiv.org/abs/2511.08475)
- [LLM Agent Evaluation Survey — arxiv:2503.16416](https://arxiv.org/abs/2503.16416)
- [agentic-code Quality Gates Framework](https://github.com/shinpr/agentic-code)
