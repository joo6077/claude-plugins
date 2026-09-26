# EX-1 — Codex 원문 대조 (2026-09-26, gpt-5.6-sol, 읽기 전용)

## 물은 것

확인할 것:
- 플러그인 hooks.json 명령에서 ${CLAUDE_PLUGIN_ROOT} 경로를 큰따옴표로 감싸라고 권하는가? 원문 문장을 그대로 인용
- Stop / SubagentStop 훅 입력에 last_assistant_message 필드가 있는가, 이름과 뜻
- 훅 설정의 async 필드가 있는가, 뜻과 기본값

저장소 근거(읽어서 무엇을 주장했는지 먼저 확인):
- /Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0926b/.harness/.meta/evidence/phase12.md 14행 · 49행 · 113행

원문: https://code.claude.com/docs/en/hooks

## 답

세 항목 모두 현재 공식 문서와 일치합니다. 단, `async`의 기본값은 문서에 `false`라는 값으로 직접 표기되지 않고 “기본적으로 완료까지 차단한다”고 설명됩니다.

## 1. 출처 목록

- 저장소 근거: [phase12.md](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0926b/.harness/.meta/evidence/phase12.md) — 확인일 2026-09-26
- [Claude Code Hooks reference](https://code.claude.com/docs/en/hooks) — 가져온 날짜 2026-09-26

`phase12.md`의 실제 위치는 다음과 같습니다.

- 14행: Hooks reference를 출처로 열거
- 49행: Stop의 `last_assistant_message` 주장
- 53행·114행: native `async`/`asyncRewake` 주장
- 113행: `${CLAUDE_PLUGIN_ROOT}` 인용 또는 exec-form 사용 주장

## 2. 질문별 확인

### `${CLAUDE_PLUGIN_ROOT}`를 큰따옴표로 감싸라고 권하는가?

- 원문 인용: “In shell form, wrap each placeholder in double quotes.”
- 원문 URL: [Hooks reference — Reference scripts by path](https://code.claude.com/docs/en/hooks#reference-scripts-by-path)
- 가져온 날짜: 2026-09-26
- 추가 확인: 같은 문단은 경로 placeholder를 사용하는 훅에는 exec form을 선호하라고 명시합니다. shell form 예제도 `node "${CLAUDE_PLUGIN_ROOT}"/scripts/format.js --fix` 형태입니다.
- 저장소 주장: 113행은 미인용 shell form을 exec form의 `args`로 바꾸거나 placeholder를 이중 인용하자고 제안합니다.
- 판정: **맞음**. 현재 문서는 exec form을 우선 권하고, shell form이라면 각 placeholder를 큰따옴표로 감싸라고 명시합니다.

### Stop / SubagentStop 입력에 `last_assistant_message`가 있는가?

- 원문 인용: “text content of Claude’s final response”
- 원문 URL: [Hooks reference — Stop input](https://code.claude.com/docs/en/hooks#stop-input), [SubagentStop input](https://code.claude.com/docs/en/hooks#subagentstop-input)
- 가져온 날짜: 2026-09-26
- 이름과 뜻:
  - Stop의 `last_assistant_message`: Claude 주 에이전트의 최종 응답 텍스트
  - SubagentStop의 `last_assistant_message`: 서브에이전트의 최종 응답 텍스트
  - 두 경우 모두 transcript 파일을 파싱하지 않고 최종 응답에 접근하기 위한 필드입니다.
- 저장소 주장: 49행은 Stop에 `stop_hook_active`와 `last_assistant_message`가 있다고 주장합니다.
- 판정: **맞음**. Stop뿐 아니라 SubagentStop에도 같은 이름의 필드가 있습니다.
- 주의: Claude Code v2.1.271 이상에서 `SubagentHandback`을 사용한 경우, 이 필드는 전달된 보고서가 아니라 서브에이전트의 마지막 마무리 텍스트를 담을 수 있습니다.

### 훅 설정에 `async` 필드가 있는가? 뜻과 기본값은?

- 원문 인용: “By default, hooks block Claude’s execution until they complete.”
- 원문 URL: [Hooks reference — Command hook fields](https://code.claude.com/docs/en/hooks#command-hook-fields), [Run hooks in the background](https://code.claude.com/docs/en/hooks#run-hooks-in-the-background)
- 가져온 날짜: 2026-09-26
- 뜻: command hook에서 `async: true`를 지정하면 Claude 실행을 막지 않고 훅을 백그라운드에서 실행합니다. 이 필드는 `type: "command"`에만 제공됩니다.
- 기본값:
  - 문서의 직접 표현은 “기본적으로 훅은 완료될 때까지 Claude 실행을 차단한다”입니다.
  - **추론:** `async` 생략 시 동기·blocking 동작이므로 의미상 기본값은 `false`입니다. 문서 필드 표에 `Default: false`라는 값 자체가 명시되지는 않습니다.
- 저장소 주장: 53행과 114행은 command hook에 native `async`와 `asyncRewake`가 있다고 주장합니다.
- 판정: **맞음**. 다만 “모든 훅의 필드”가 아니라 **command hook 전용 필드**라고 한정하는 편이 정확합니다.

## 3. 저장소에 반영할 문장 제안

- 경로: `hooks.json`에서 경로 placeholder를 쓰는 command hook은 exec form을 우선 사용하고, shell form을 유지하면 `"${CLAUDE_PLUGIN_ROOT}"`처럼 각 placeholder를 큰따옴표로 감싼다.
- 입력: Stop과 SubagentStop 입력의 `last_assistant_message`는 각각 주 에이전트와 서브에이전트의 최종 응답 텍스트이며, transcript를 파싱하지 않고 사용할 수 있다.
- 비동기: command hook의 `async: true`는 훅을 비차단 백그라운드로 실행하며, 생략 시 기본 동작은 완료까지 기다리는 동기·blocking 실행이다.

## 4. 못 가져온 것 / 열린 질문

- 못 가져온 자료는 없습니다. 공식 페이지를 정상적으로 가져왔으므로 `curl` 재시도는 필요하지 않았습니다.
- 열린 질문: 공식 문서는 `async` 기본값을 `false`라는 리터럴로 직접 표기하지 않습니다. `false` 판정은 문서의 기본 blocking 동작에서 도출한 **추론**입니다.