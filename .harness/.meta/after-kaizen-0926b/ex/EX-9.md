# EX-9 — Codex 원문 대조 (2026-09-26, gpt-5.6-sol, 읽기 전용)

## 물은 것

확인할 것:
- React 19.3 에서 <ViewTransition> 이 안정 API 인가, 이름과 사용 조건
- Activity 컴포넌트 상태(안정/실험)와 이름

저장소 근거(읽어서 무엇을 주장했는지 먼저 확인):
- /Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0926b/.harness/.meta/evidence/phase10.md 147행

원문: https://react.dev/blog/2026/09/09/react-19-3

## 답

## 1. 출처 목록

- 저장소 근거: [phase10.md:147](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0926b/.harness/.meta/evidence/phase10.md:147) — 가져온 날짜: 2026-09-26
- React 공식 발표: [React 19.3](https://react.dev/blog/2026/09/09/react-19-3) — 게시일: 2026-09-09, 가져온 날짜: 2026-09-26

## 2. 질문별 확인

### `<ViewTransition>`

- 원문 인용: “We shared it as an experimental API last year, and in 19.3 it’s stable and ready to use.” ([원문](https://react.dev/blog/2026/09/09/react-19-3))
- 이름: `<ViewTransition>`. `react`에서 `ViewTransition`을 import한다.
- 사용 조건:
  - 애니메이션할 UI를 `<ViewTransition>`으로 감싼다.
  - Transition으로 표시된 업데이트가 자식 스타일을 변경하거나 컴포넌트를 mount/unmount할 때 애니메이션된다.
  - `startTransition` 내부 업데이트, Suspense reveal, `useDeferredValue` 업데이트가 해당된다.
  - 현재 DOM에서만 동작한다.
- 저장소 주장: 147행은 기존 `canary/backlog` 분류를 지적하며 “React 19.3에서 stable”이라고 주장한다.
- 판정: **맞음**. 안정화 여부와 정확한 컴포넌트 이름 모두 원문에 명시돼 있다.

### Activity

- 원문 인용: “react-server: Add support for `<Activity>` in Flight” ([원문](https://react.dev/blog/2026/09/09/react-19-3))
- 이름: 원문 표기는 `<Activity>`.
- 상태: React 19.3 발표에는 `<Activity>` 관련 Flight 지원과 여러 버그 수정이 나오지만, 이를 **stable 또는 experimental이라고 분류하는 문장은 없다**.
- 저장소 주장: 지정된 147행에는 Activity에 관한 주장이 없다.
- 판정: 이름은 **맞음**. 안정/실험 상태는 저장소 주장에도 없고 해당 원문에도 명시되지 않았으므로 **원문에 없음**.
- 추론: 안정판 변경 로그에 `<Activity>`가 등장한다는 사실만으로 API 자체가 안정화됐다고 단정할 수 없다.

## 3. 저장소에 반영할 문장 제안

- `<ViewTransition>`은 React 19.3에서 안정 API이며, `react`에서 가져와 DOM UI를 감싸고 Transition으로 표시된 업데이트에 사용한다.
- React 19.3 발표는 컴포넌트 이름을 `<Activity>`로 표기하지만, 해당 발표만으로는 안정 또는 실험 API인지 판정할 수 없다.

## 4. 못 가져온 것 / 열린 질문

- 147행이 연결하는 `release-0924/docs/react/research-log.md` 경로는 현재 존재하지 않아 원본 303행은 가져오지 못했다.
- Activity의 안정/실험 상태를 확정하려면 별도의 공식 Activity API 문서나 최초 발표문이 필요하다.
- React 19.3 페이지는 정상적으로 가져왔으므로 `curl` 재시도는 필요하지 않았다.
- 파일은 수정하지 않았다.