---
name: handoff
description: >
  세션 종료 전 핸드오프 문서를 생성한다. 이번 세션의 완료 내역(커밋, 태스크, QA 결과),
  미완료/블로커, 다음 세션에서 붙여넣을 resume 프롬프트, push 상태를 한 번에 정리한다.
  긴 세션이 출력 토큰 한도/네트워크 장애로 중단될 위험이 있을 때, 혹은 사용자가
  "핸드오프", "handoff", "세션 정리", "이어서 할 수 있게", "다음 세션 프롬프트", "resume", "hand off" 같은
  요청을 할 때 트리거. 단순 세션 종료 인사에는 트리거하지 않는다.
argument-hint: "[file:<경로>] (옵션 — 기본은 .harness/handoff/YYYY-MM-DD-HHMM.md)"
user-invocable: true
---

# Session Handoff

긴 세션의 중단 리스크를 흡수하기 위한 체크포인트. 이번 세션의 상태를 한 파일에 응축하여 다음 세션이 맨 위부터 컨텍스트를 재구축할 수 있도록 한다.

## Gotchas

- **파일 경로는 `.harness/handoff/` 하위**를 기본으로 한다. `.harness/`가 없는 레포면 `./handoff/`, 그것도 부적절하면 사용자에게 물어라. 절대 루트나 `docs/`에 쓰지 마라.
- 핸드오프는 **"다음 세션의 Claude가 읽을 것"**이라는 가정으로 작성한다 — 사용자를 위한 요약이 아니다. 구체적 파일 경로, 커밋 SHA, 실행 명령을 포함하라.
- **push 상태를 반드시 명시**하라. `git log origin/<branch>..HEAD` 결과를 캡처하여 "몇 개 커밋이 로컬에만 있는지" 적는다. 이 정보가 없으면 다음 세션이 중복 작업한다.
- 미완료 작업을 "진행 중"이라고만 쓰지 마라 — **어디까지 했고 다음 스텝이 뭔지**를 적어라. "Phase 3까지 완료, Phase 4 시작 전"이 아니라 "Phase 4는 `/contract-kaizen` 서브에이전트 실행부터"처럼.
- 결과 리포트는 **항상 2회 커밋**한다: (1) 핸드오프 파일 생성 커밋, (2) 있다면 WIP 커밋. Stash 금지.
- sensitive data (API 키, 토큰) 는 핸드오프에 쓰지 마라. 참조 경로(예: `.env.local:45`) 만 적는다.
- 세션 한도를 넘기면 핸드오프가 잘린다 — **응답은 300 줄 이내**, 핸드오프 파일은 500 줄 이내로 유지한다. 상세 로그는 별도 파일로 분리.
- 핸드오프 후 사용자가 "계속해"라고 하면, 새 대화에서 이 파일을 먼저 읽도록 안내한다. 이어서 작업하지 마라 (컨텍스트 오염).

## Process

### 1. 현재 상태 스냅샷 수집

다음 명령을 순서대로 실행하여 상태를 캡처한다:

```bash
# git 상태
git status --short
git log --oneline -15
git branch --show-current
git log origin/$(git branch --show-current)..HEAD --oneline 2>/dev/null || echo "no remote tracking"

# 최근 .harness/sprint-feedback.md (있으면)
[ -f .harness/sprint-feedback.md ] && tail -30 .harness/sprint-feedback.md
```

결과를 메모리에 두되 **핸드오프 파일에는 요약해서 넣어라** (raw 덤프 금지).

### 2. 태스크 상태 집계

현재 세션의 TaskList 상태를 확인한다:

- completed → "Done" 섹션에 bullet로
- in_progress → "In Progress" 섹션에 "어디까지 + 다음 스텝" 형식으로
- pending → "Queued" 섹션에 bullet로

### 3. QA/빌드 상태 확인

가능하면 아래 중 해당되는 것만:

- `python3 scripts/validate-plugin.py` (이 레포에 있으면)
- 최근 QA Evaluator verdict (APPROVE/REJECT)
- 마지막 빌드/테스트 결과 (성공/실패 + 실패 사유)

### 4. 핸드오프 파일 작성

경로: `.harness/handoff/YYYY-MM-DD-HHMM.md` (없으면 `mkdir -p`)

아래 템플릿을 따른다:

````markdown
# Handoff — YYYY-MM-DD HH:MM KST

> 다음 세션의 Claude가 읽을 것. 이 파일 맨 위부터 읽고 **Resume Prompt** 섹션을 실행하라.

## Context (한 문단)

무슨 작업을 어느 단계까지 했는지. "카이젠 오케스트레이션 Phase 1~3 완료, Phase 4 진입 직전" 같이.

## Git State

- **Branch**: `<branch>`
- **Local commits ahead of origin**: N개
  - `<sha>` <subject>
  - ...
- **Uncommitted**: <있으면 파일 리스트 / 없으면 "clean">
- **Last commit SHA**: `<sha>`

## Done (이번 세션)

- [x] <완료한 것 1> (SHA `<sha>`)
- [x] <완료한 것 2>

## In Progress (이어서 할 것)

### <작업명>

- **어디까지**: ...
- **다음 스텝**: `<구체적 명령 또는 파일:라인>`
- **주의사항**: ...

## Queued

- [ ] <대기 중 작업>

## 폐기·거절한 결정 (되살리기 전에 사용자에게 묻기)

- <항목> · <날짜> · <이유> (없으면 "없음")

## Known Issues / Blockers

- <문제 1 + 관련 파일/SHA>

## QA / Build State

- <최근 QA verdict / 빌드 결과>

## Resume Prompt (복사해서 다음 세션에 붙여넣기)

```text
`.harness/handoff/<이 파일>`을 먼저 읽고, "In Progress" 섹션의 다음 스텝부터 이어서 실행해줘.

주의: <이번 세션의 제약/주의사항>
```

## References

- 관련 문서/이슈 경로
- 참조한 리서치 링크
````

### 5. 커밋

`-o` 로 핸드오프 파일만 싣는다. 빼면 다른 세션이 같은 인덱스에 올려둔 파일이 이 커밋에 섞인다.

```bash
git add .harness/handoff/<file>.md
git commit -o .harness/handoff/<file>.md -m "chore(handoff): <세션 요약 한 줄>

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>"
```

### 6. 최종 응답

사용자에게:

- 핸드오프 파일 경로
- 다음 세션 오픈 시 붙여넣을 **Resume Prompt** 한 블록
- push 여부 확인 질문 (기본: push 안 함 — 사용자가 명시해야 함)

응답은 10줄 이내.

## References

- `/insights` 빌트인에서 추천된 skill 패턴 (session truncation 방어)
- `harness/docs/guides/skill-design-guide.md` §9 (Long-Running Skills — Checkpoint Commits & SESSION_LOG)
