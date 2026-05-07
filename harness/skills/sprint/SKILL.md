---
name: sprint
description: >
  Contract → 구현 → QA → Commit → Push 의 단일 sprint 루프를 한 호출로 실행한다.
  매번 같은 사이클을 다시 설명하지 않도록 sprint-contract 작성 + 구현 안내 + qa-evaluator spawn + 결과 보고 + commit/push 까지
  순차 호출한다. 사용자가 "스프린트 돌려줘", "/sprint", "Contract부터 push까지", "전체 사이클" 같은 표현을 쓸 때 트리거한다.
  단순 1파일 수정, 색상/오타 변경, 설정 변경에는 트리거하지 않는다 — sprint-contract 와 마찬가지.
argument-hint: "[기능 이름 또는 짧은 설명]"
user-invocable: true
---

# /sprint — Contract → Implement → QA → Push 단일 루프

`/insights` 2026-05-07 fresh report 의 Quick Win #1 ("contract-QA-push 루프를 매번 다시 설명하지 않게 /sprint 스킬로 승격") 을 흡수한 메타 스킬. 2,391 메시지 / 130 세션 분석 결과 가장 빈번한 반복 패턴이다.

## Gotchas

- **본 스킬은 sprint-contract 의 대체가 아니라 wrapper.** sprint-contract 가 contract 작성만 한다면, /sprint 는 contract → implement → qa → commit/push 까지 묶는다. sprint-contract 의 모든 Gotcha 와 anti-pattern 을 그대로 상속.
- **단계 사이마다 사용자 확인 (질문 없이 자동 진행 금지).** Contract 합의 → 구현 시작 → QA 직전 → commit 직전 → push 직전 5 체크포인트마다 짧은 confirmation. /insights Friction "허락 없는 편집" 대응.
- **응답 300 라인 초과 금지 (체크포인트 단위로 분할).** /insights Friction #3 (session truncation) 대응. 한 호출이 길면 commit + 짧은 보고 + 다음 turn 으로.
- **/sprint 는 Pre-Sprint Sync Check 를 첫 단계로 강제.** `git fetch --all && git log origin/<base> --oneline -10 && ps aux | grep mcp` 결과를 Contract 작성 전에 보고. 병렬 자동화 충돌 / 좀비 MCP 발견 시 사용자에게 보고 후 진행 여부 확인.
- **본 스킬은 단순 변경에 트리거하지 않는다.** 1 파일 색상 변경, 오타 수정, 설정 한 줄 변경에 sprint 전체 사이클을 도는 것은 over-process. sprint-contract 의 트리거 규칙을 그대로 따른다.
- **Hard-stop 액션 (main 직접 push, force push, 파일 삭제 등) 은 명시 승인 후에만.** Scope-Bound Edits 원칙 (skill-design-guide §3.6) 자동 적용.

## Process

### Step 0: Pre-Sprint Sync Check (필수)

```bash
git fetch --all 2>&1 | tail -3
git log origin/$(git symbolic-ref --short HEAD) --oneline -10 2>/dev/null || git log origin/main --oneline -10
ps aux | grep -E 'mcp[-_]server|figma-developer|playwright-mcp' | grep -v grep | wc -l
```

결과를 사용자에게 1-3 줄로 보고. 충돌 가능성 발견 시 reconciliation 또는 base 변경 후 진행.

### Step 1: Sprint Contract 작성

`sprint-contract` 스킬 invoke. 인자로 받은 기능 이름/설명을 전달. Contract DRAFT 작성 → 사용자 합의.

### Step 2: 구현

Contract 가 합의되면 구현 시작. Pre-Edit Batch Audit (skill-design-guide §3.6) 자동 적용 — 대상 파일 전수 audit → 위반 N건 체크리스트 → 사용자 승인 → 일괄 편집.

체크포인트 단위로 commit. 응답 300 라인 초과 금지.

### Step 3: 빌드/분석 검증

스택 별 자동 검증 명령 실행 (Flutter: `fvm flutter analyze`, Rust: `cargo build && cargo clippy`, Node: `npm run lint && npx tsc`). 0 issue 까지 fix. 사용자 보고.

### Step 4: QA Evaluator

`qa-evaluator` 에이전트 spawn. Contract 기준 APPROVE/REJECT 판정.

- APPROVE → Step 5
- REJECT → 수정 후 Step 3 재실행 (Iteration +1, 최대 3회 후 사용자 에스컬레이션)

### Step 5: Commit

QA APPROVE 후 conventional commit 메시지 작성 → 사용자 확인 → commit.

### Step 6: Push

push 직전 사용자 명시 승인 필수 (Scope-Bound Edits Hard-stop). main 직접 push 는 `--force` 와 동등한 위험으로 분류, 별도 승인 단계.

## References

- `harness/skills/sprint-contract/SKILL.md` — Step 1 위임 대상
- `harness/agents/qa-evaluator.md` — Step 4 spawn 대상
- `harness/docs/guides/skill-design-guide.md` §3.6 — Pre-Edit Batch Audit + Scope-Bound Edits
- `harness/docs/guides/skill-design-guide.md` §9 — Long-Running Skills + Pre-Sprint Sync Check
- `~/.claude/usage-data/report-ko.html` — `/insights` Quick Win #1 (본 스킬의 source of truth)
