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
- **핸드오프 문서를 기억처럼 믿지 마라 — git 이 유일한 판정자.** 재개 세션에서 핸드오프·잔여작업 문서의 "잔여 항목" 을 그대로 이어받으면, 이미 끝난 일을 다시 하거나 실제 잔여를 놓친다. 에이전트는 자기 메모리의 무효화를 스스로 탐지하지 못한다 — STALE 벤치마크에서 최고 모델의 정확도가 **55.2%** 이고, 주 실패 모드가 "명시적 부정 없이 나중 관측이 앞선 기억을 무효화하는" Implicit Conflict 다 (<https://arxiv.org/abs/2605.06527>). Step 0.5 의 git 대조를 건너뛰지 마라.
- **커밋 단위 = 검증 증거가 확보된 수정 단위.** 여러 수정을 모아 한 번에 커밋하면 중간 회귀가 은폐되고, 되돌릴 때 정상 변경까지 함께 날아간다 (`/insights` Friction #5). 각 단위마다 검증 명령을 돌리고 그 **출력을 인용한 뒤** 커밋한다. 검증하지 않은 변경을 다음 단위와 묶지 마라.
- **병렬 세션이 있으면 파일 소유권을 먼저 나눠라.** Step 0 에서 다른 세션/에이전트 작업이 감지되면 이번 스프린트가 **쓰기** 할 파일 목록을 열거해 사용자에게 보고하고, 겹치는 파일은 병렬이 아니라 순차로 처리한다. 겹친 채 진행하면 한쪽 편집이 조용히 덮인다 (근거: Glite ARF 는 12 병렬 에이전트를 task isolation + 완료분 immutability 를 강제하는 결정론적 verifier 로 통제했다 — <https://arxiv.org/abs/2606.27416>).

## Process

### Step 0: Pre-Sprint Sync Check (필수)

```bash
git fetch --all 2>&1 | tail -3
git log origin/$(git symbolic-ref --short HEAD) --oneline -10 2>/dev/null || git log origin/main --oneline -10
ps aux | grep -E 'mcp[-_]server|figma-developer|playwright-mcp' | grep -v grep | wc -l
```

결과를 사용자에게 1-3 줄로 보고. 충돌 가능성 발견 시 reconciliation 또는 base 변경 후 진행.

병렬 세션/에이전트 흔적이 보이면 (미커밋 변경, 다른 브랜치의 최근 커밋, 실행 중 MCP) **이번 스프린트가 쓰기 할 파일 목록을 열거**해 보고하고 겹침 여부를 확인받는다.

### Step 0.5: 핸드오프 재검증 (재개 세션 필수)

이전 세션의 핸드오프 문서 · 잔여작업 목록 · "다음 단계" 메모를 이어받는 경우에만 수행한다. 문서를 읽는 것으로 끝내지 말고 **git 으로 대조**한다:

```bash
git log --oneline "$(git merge-base HEAD origin/main)..HEAD"   # 실제로 들어간 커밋
git status --short                                              # 미커밋 잔여
git diff --stat "$(git merge-base HEAD origin/main)..HEAD"      # 변경 파일 실체
```

대조 결과를 아래 형식으로 **응답에 복사해 채운다** (E2 아티팩트 — skill-design-guide §3.7):

```text
핸드오프 재검증
- 문서 주장 잔여: <항목 나열>
- git 실측: <이미 완료된 항목> / <실제 잔여 항목>
- 불일치: N 건 → 문서 먼저 갱신 후 착수
```

불일치가 1 건이라도 있으면 **핸드오프 문서를 먼저 고친 뒤** Step 1 로 간다. 문서의 잔여 목록과 git 실측이 어긋난 채 진행하는 것은 스테일 상태를 한 사이클 더 전파하는 것이다.

### Step 1: Sprint Contract 작성

`sprint-contract` 스킬 invoke. 인자로 받은 기능 이름/설명을 전달. Contract DRAFT 작성 → 사용자 합의.

### Step 2: 구현

Contract 가 합의되면 구현 시작. Pre-Edit Batch Audit (skill-design-guide §3.6) 자동 적용 — 대상 파일 전수 audit → 위반 N건 체크리스트 → 사용자 승인 → 일괄 편집.

체크포인트 단위로 commit. 응답 300 라인 초과 금지.

### Step 3: 빌드/분석 검증

스택 별 자동 검증 명령 실행 (Flutter: `fvm flutter analyze`, Rust: `cargo build && cargo clippy`, Node: `npm run lint && npx tsc`). 0 issue 까지 fix.

보고에는 **실행한 명령과 그 출력**을 인용한다 — "분석 통과했습니다" 같은 자기보고는 증거가 아니다 (skill-design-guide §3.7 Completion Evidence Gate). 검증이 불가능하면 조용히 넘기지 말고 `[미검증]` + 사유 한 줄을 남긴다.

### Step 4: QA Evaluator

`qa-evaluator` 에이전트 spawn. Contract 기준 APPROVE/REJECT 판정.

- APPROVE → Step 5
- REJECT → 수정 후 Step 3 재실행 (Iteration +1)

**Iteration 카운터 (E2 — 매 라운드 응답에 복사해 채운다):**

```text
QA Iteration: N/3 · 직전 판정: APPROVE|REJECT
- 직전 REJECT 사유(1 줄): <사유>
- 이번 라운드에서 고친 것: <조건 ID 나열>
```

- 카운터는 기억이 아니라 **파일에서 복원**한다. 컨텍스트가 끊겼거나 세션이 바뀌었으면 **이번 스프린트의 피드백 파일 하나**를 대상으로 기존 판정 기록 수를 세어 N 을 정한다. 대상 파일은 Contract frontmatter 의 `slug` 로 결정한다 — 슬러그가 있으면 `{CONTRACT_ROOT}/.harness/sprint-feedback-<slug>.md`, 슬러그가 없는 plain 모드면 `{CONTRACT_ROOT}/.harness/sprint-feedback.md` 다.

```bash
# SLUG = Contract frontmatter 의 slug 값. plain 모드면 빈 문자열.
FB="${CONTRACT_ROOT}/.harness/sprint-feedback${SLUG:+-${SLUG}}.md"
[ -f "$FB" ] && grep -c "판정" "$FB" || echo 0
```

- **대상 파일을 잘못 고르면 N=3 에스컬레이션 가드가 통째로 무력화된다.** 슬러그 스프린트인데 plain 고정 경로만 세면 그 파일에는 이번 스프린트 기록이 없어 매 라운드 N=1 로 리셋되고, 루프가 3 회를 넘겨도 멈추지 않는다. 반대로 `sprint-feedback-*.md` 를 와일드카드로 묶어 합산하면 병렬 스프린트의 판정까지 딸려 들어와 N 이 부풀고 멀쩡한 루프가 조기 중단된다. 세는 파일은 항상 **정확히 하나**다. 기록이 없으면 N=1 로 시작한다.
- **N=3 에서 REJECT 면 루프를 중단**하고 사용자에게 에스컬레이션한다. 남은 REJECT 조건, 지금까지 시도한 수정, 막힌 지점을 그대로 보고하고 자율 재시도를 이어가지 마라. 3 회를 넘겨 계속 도는 것은 스코프 드리프트의 전형이다 (`/insights` Friction #3).

### Step 5: Commit

QA APPROVE 후 conventional commit 메시지 작성 → 사용자 확인 → commit.

커밋은 **검증 증거가 확보된 수정 단위**로 나눈다. 한 스프린트에서 성격이 다른 수정을 했다면 배치로 묶지 말고 단위별로 커밋한다 (Friction #5 — 배치 커밋은 중간 회귀를 은폐한다).

### Step 6: Push

push 직전 사용자 명시 승인 필수 (Scope-Bound Edits Hard-stop). main 직접 push 는 `--force` 와 동등한 위험으로 분류, 별도 승인 단계.

## References

- `harness/skills/sprint-contract/SKILL.md` — Step 1 위임 대상
- `harness/agents/qa-evaluator.md` — Step 4 spawn 대상
- `harness/docs/guides/skill-design-guide.md` §3.6 — Pre-Edit Batch Audit + Scope-Bound Edits
- `harness/docs/guides/skill-design-guide.md` §3.7 — Completion Evidence Gate + Enforcement 등급 (E1/E2/E3)
- `harness/docs/guides/skill-design-guide.md` §9 — Long-Running Skills + Pre-Sprint Sync Check
- `~/.claude/usage-data/report-ko.html` — `/insights` Quick Win #1 (본 스킬의 source of truth)
- <https://arxiv.org/abs/2605.06527> — STALE (2026-05). 에이전트의 자기 기억 무효화 탐지 정확도 최고 55.2% (Step 0.5 근거)
- <https://arxiv.org/abs/2606.27416> — Glite ARF (2026-06). 병렬 에이전트 task isolation + 완료분 immutability 를 결정론적 verifier 로 강제 (Step 0 파일 소유권 근거)
