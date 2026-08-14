---
phase: 1
title: Phase 1 설계 가이드 — 확보된 외부 근거
collected: 2026-08-13
method: codex (foreground 회수)
note: 이 파일이 Phase 1 의 유일한 외부 근거다. 추가 외부 조회 금지. 여기 없는 URL·수치를 지어내지 마라.
---

## A. 공식 스펙 — 사실 정정 대상 (최우선)

출처: <https://code.claude.com/docs/en/sub-agents>

원문 인용:

> "By default, a subagent can spawn subagents of its own, up to three layers below the main conversation."

- **"서브에이전트 중첩 불가" 는 거짓이다.** 기본 중첩 깊이는 main 아래 **3층**.
- `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH=1` 로 중첩을 끌 수 있다.
- 깊이 제한에 도달하면 일반 subagent 에서 `Agent` 도구가 제거된다.
- 현재 공식 frontmatter 필드 전체 (15종):
  `name`, `description`, `tools`, `disallowedTools`, `model`, `permissionMode`, `maxTurns`,
  `skills`, `mcpServers`, `hooks`, `memory`, `background`, `effort`, `isolation`, `color`.
  **필수는 `name`, `description` 둘뿐.**
- `prompt` 는 `--agents` JSON 에서 markdown body 에 해당하는 필드이며, 파일 기반 YAML frontmatter 표에는 없다.
- **플러그인 subagent 에서는 `hooks`, `mcpServers`, `permissionMode` 가 무시된다.**

→ 두 가이드 전체를 grep 하여 위와 어긋나는 서술을 **전수** 정정하라.
직전 사이클에도 같은 거짓 단언이 **4곳**에서 발견됐다. 한 곳만 고치면 재발한다.

## B. Anthropic 공식 skill 작성 가이드

출처: <https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices>

- 작업의 취약도에 맞춰 **자유도(degrees of freedom)를 조정**하라. 일관성이 중요하면 low-freedom
  지시나 스크립트로 좁혀라.
- 복잡한 작업에는 **체크리스트 / plan-validate-execute / 검증 가능한 중간 산출물**을 두라.
- 안티패턴: **"옵션을 너무 많이 주지 말고 기본값을 제공하라."**

출처: <https://raw.githubusercontent.com/anthropics/skills/main/skills/skill-creator/SKILL.md>

- 기대 출력 · edge case · success criteria 를 **먼저 묻고** 테스트 프롬프트를 만들어라.
- `SKILL.md` 는 **500 라인 미만이 이상적**이고, 큰 내용은 references 로 뺀다.

## C. D2 — 탐색형 스킬 발산 억제 (신규 델타)

공식 가이드에 "산출물 개수 상한 + 변주 축 고정 + 부대 산출물 금지" 를 하나로 묶은 확립된 조항은
**없다(미확인)**. 인접 분야에서 이식한다:

- DOE(Design of Experiments) 의 factor / level / design matrix — 입력 factor 와 level 을 정하고
  design matrix 로 조합을 제한한다. <https://asq.org/quality-resources/design-of-experiments>
- 디자인 제약 연구: 제약이 탐색 공간을 특정 방향으로 유도한다.
  <https://www.researchgate.net/publication/358854029_Empirically_Understanding_the_Impact_of_Item_Constraints_on_Designer_Ideation>

실측 근거 — 글로벌 REJECT `UI-04` (2026-08-12):

> "B3(단일 컬럼)과 B6(조밀 로그)이 계약 지정 4축(버블 컨테이너 유무/정렬 컬럼 수/메타 위치/묶음 단위)
> 전부에서 동일값 — 구조 구별 요구 위반"

즉 **계약에 축이 명시돼 있어도 구현이 무시한다.** 축 선언만으로는 부족하고,
축 값의 상이성을 기계적으로 검사할 수 있어야 한다.

조항 초안 (그대로 쓰지 말고 우리 가이드 체계에 맞게 재작성):

```text
Exploration Budget Contract — 산출물 수와 변주 축이 명시되지 않은 탐색형 요청에서:
- 기본 산출물 상한 3개. 4개 이상은 사용자 승인 선행.
- primary axis 1개 고정, 필요 시 secondary axis 1개까지.
- 각 variant 는 axis value 가 서로 달라야 하고 나머지는 constants 로 고정.
- 실행 전 Variant Matrix: id / axis / axis value / constants / 생성·수정 파일.
- 요청받지 않은 디자인 시스템·토큰 파일·문서·컴포넌트 라이브러리·scaffold 생성 금지.
```

## D. D3 — 사용자 관측 vs 자기 증거 충돌 (신규 델타)

Claude 공식 문서에 명시 규약은 **없다(미확인)**. 근거는 논문 쪽:

- coding-agent misalignment 연구는 개발자의 correction/pushback 을 intent anchor 로 보존하며,
  pushback 이 없으면 intention misalignment 를 인정하지 않는다. <https://arxiv.org/html/2605.29442>
- false-success 연구: 에이전트가 환경 상태와 달리 완료를 주장하는 실패를 다루고,
  LLM judge 가 checklist·stepwise·명시 검증 조건에서도 실패한다고 보고. <https://arxiv.org/html/2606.09863>
- 상태 검증은 agent self-report 가 아니라 **target system** 을 확인해야 한다.
  <https://blogs.oracle.com/ai-and-datascience/oci-agent-evaluation-framework>

조항 초안:

```text
User-Reported Failure Gate — 사용자가 "아직 깨졌다" 고 보고하면 상태는 PASS 가 아니라 REOPENED.
에이전트의 테스트·스크린샷은 "내 환경에서의 관측" 일 뿐 반박 근거가 아니다.
먼저 oracle validity 를 점검한다 — 같은 URL/브랜치/viewport/device/auth·cache/데이터 상태를 재현했는가.
사용자 관측을 재현하거나, 차이를 설명하는 환경 불일치를 확인하거나,
사용자가 수정 확인을 해주기 전까지 완료 선언 금지.
```

## E. Enforcement 등급 승급 근거 (기존 E1/E2/E3 유지 + 승급 조건 명시)

- deterministic read-only gate 를 mutating tool call 앞에 두면 silent wrong-state failure 일부를
  막고 성능도 개선된다. 단 gate 가 전체 task 성공을 보장하지는 않으며 policy/model 별 audit 이 필요하다.
  <https://arxiv.org/html/2607.07405>
- OpenAI Agents SDK: guardrail tripwire 가 실행을 중단할 수 있고, tool guardrail 은 각 function-tool
  호출 전후로 동작한다. <https://openai.github.io/openai-agents-js/guides/guardrails/>
- Anthropic: 단일 방어선은 보장이 아니며 여러 계층이 필요하다.
  <https://www.anthropic.com/research/trustworthy-agents>

승급 조건 초안:

```text
E1 문장 규칙: 선호·휴리스틱·저위험 규칙.
E2 산출물 아티팩트: 반복 누락, open-ended 작업, 범위/개수/증거가 필요한 규칙.
E3 결정론적 게이트/훅: 기계 판정 가능하고 비용이 큰 규칙, 또는 E2 이후에도 반복 위반되는 규칙.
```

## F. 넣지 말아야 할 것 (명시적 금지)

- "MUST 라고 세게 쓰면 해결된다"
- "LLM self-review 가 deterministic gate 다"
- "사용자 보고는 항상 사실이다" — 정확한 표현은 "완료 판정을 보류하고 oracle validity 를 먼저 의심한다"
- "모든 창의 작업은 시작 전 반드시 질문한다"
- "서브에이전트 중첩 불가"

## G. 트레이드오프 (가이드에 반영하라)

산출물 상한은 과잉 생성을 막지만 탐색 폭을 줄인다. 축 고정은 비교 가능성을 높이지만 의외의 조합을 줄인다.
부대 산출물 금지는 scope creep 을 막지만 장기적으로 유용한 인프라 생성을 늦춘다.
사용자 보고 우선 규칙은 신뢰를 회복하지만 환경 차이 재현 비용이 든다.
E3 게이트는 강하지만 과차단과 유지보수 비용이 있다.
