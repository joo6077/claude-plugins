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

**병렬 흔적이 있고 커밋이 둘 이상 예상되면 워크트리를 따로 만든다 (2026-09-25 추가).** 같은 작업 폴더에서
`git checkout -b` 로 가지만 바꾸면 남의 미커밋 변경이 새 가지로 따라오고, 남이 깨 놓은 검사가 내 가지에서도
빨갛다. 워크트리는 `HEAD` 와 공용 목록(`git add` 로 올려 둔 목록)을 폴더마다 따로 둔다
(<https://git-scm.com/docs/git-worktree>). 기준은 검사가 통과하는 것을 확인한 커밋이다:

```bash
git worktree add -b <가지> <새 폴더> <검사 통과를 확인한 커밋>
```

sprint-contract Step 6.7 의 가지 만들기는 이 워크트리 안에서 한다. 서브에이전트의 `isolation: worktree` 는 부모
`HEAD` 가 아니라 기본 가지에서 임시 워크트리를 만든다 (<https://code.claude.com/docs/en/sub-agents>) — 기준 커밋이
다르므로 이 절차를 대신하지 않는다. 실측(2026-09-18): 다른 세션들이 깨 놓은 공용 개발 가지에서 몇 시간을 쓴 뒤에야
사용자가 워크트리를 먼저 제안했다.

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

보고에는 **실행한 명령과 그 출력**을 인용한다 — "분석 통과했습니다" 같은 자기보고는 증거가 아니다 (skill-design-guide §3.7 Completion Evidence Gate). 검증이 불가능하면 조용히 넘기지 말고 `[미검증]` 에 네 칸(막는 것 · 시도한 우회 · 통제 불가 사유 · 재검증 명령)을 채운다. 칸의 뜻은 skill-design-guide §3.7 5 조항 3 항이 정한다. 미검증이 2 건 이상이면 완료가 아니라 부분 완료로 보고한다.

**검사가 빨가면 고치기 전에 원인을 셋으로 가른다 (2026-09-25 추가)** — 이번 변경 · 남의 미커밋 변경 · 기준 커밋에서
이미 실패. 여럿이 같이 쓰는 가지에서는 빨간 검사가 내 탓이 아닌 경우가 많다. 같은 명령을 깨끗한 임시 워크트리에서
다시 돌려 가른다. `<기준 가지>` 는 합칠 대상 가지다. 임시 워크트리에는 추적하지 않는 파일(설치한 의존성 · 빌드
산출물)이 없으니 `<실패한 검사 명령>` 앞에 그 프로젝트의 준비 명령을 붙인다 — 안 붙이면 준비가 안 된 탓의 실패를
기준 커밋 탓으로 읽는다:

```bash
FORK_BASE=$(git merge-base HEAD origin/<기준 가지>)
for ref in HEAD "$FORK_BASE" origin/<기준 가지>; do
  t=$(mktemp -d)
  git worktree add -q --detach "$t" "$ref"
  ( cd "$t" && <실패한 검사 명령> ) >/dev/null 2>&1
  rc=$?
  echo "$ref $(git rev-parse --short "$ref") exit=$rc"
  git worktree remove --force "$t"
done
```

| 공용 작업 폴더 | `HEAD` 임시 | `FORK_BASE` 임시 | 판정 |
| --- | --- | --- | --- |
| 실패 | 통과 | — | 미커밋 변경 탓 — `git status --short` 의 파일이 내가 쓴 목록 밖이면 남의 미커밋이다 |
| 실패 | 실패 | 실패 | 기준 커밋에서 이미 실패 — 내 변경 전부터다 |
| 실패 | 실패 | 통과 | 이번 커밋 탓일 가능성이 크다 |

`FORK_BASE` 는 분기점이지 기준 가지의 지금 상태가 아니다 (<https://git-scm.com/docs/git-merge-base>).
`origin/<기준 가지>` 줄은 분기 뒤 기준 가지가 깨졌는지를 본다 — 여기서 실패하면 합친 뒤에도 빨갈 수 있다.
명령 · 커밋 · 종료 코드를 보고에 인용한다. 실측(2026-09-18): 다른 세션들이 깬 공용 개발 가지의 자동 검사 실패 다섯
건을 고치는 데 몇 시간을 썼다.

### Step 4: QA Evaluator

`qa-evaluator` 에이전트 spawn. Contract 기준 APPROVE/REJECT 판정.

- APPROVE → Step 5
- REJECT → 수정 후 Step 3 재실행 (Iteration +1)

**Iteration 카운터 (E2 — 매 라운드 응답에 복사해 채운다):**

```text
QA Iteration: N/3 · 직전 판정: APPROVE|REJECT
- 직전 REJECT 사유(1 줄): <사유>
- 이번 라운드에서 고친 것: <조건 ID 나열>
사용자가 할 일: 없음 | <한 줄>
```

끝 줄은 sprint-contract Step 5 와 같은 문구 `사용자가 할 일: 없음` 또는 `사용자가 할 일: <한 줄>` 로 쓴다.

- 카운터는 기억이 아니라 **파일에서 복원**한다. 컨텍스트가 끊겼거나 세션이 바뀌었으면 **이번 스프린트의 피드백 파일 하나**를 대상으로 기존 판정 기록 수를 세어 N 을 정한다. 대상 파일은 Contract frontmatter 의 `slug` 로 결정한다 — 슬러그가 있으면 `{CONTRACT_ROOT}/.harness/sprint-feedback-<slug>.md`, 슬러그가 없는 plain 모드면 `{CONTRACT_ROOT}/.harness/sprint-feedback.md` 다.

```bash
# SLUG = Contract frontmatter 의 slug 값. plain 모드면 빈 문자열.
FB="${CONTRACT_ROOT}/.harness/sprint-feedback${SLUG:+-${SLUG}}.md"
[ -f "$FB" ] && grep -c "판정" "$FB" || echo 0
```

- **대상 파일을 잘못 고르면 N=3 에스컬레이션 가드가 통째로 무력화된다.** 슬러그 스프린트인데 plain 고정 경로만 세면 그 파일에는 이번 스프린트 기록이 없어 매 라운드 N=1 로 리셋되고, 루프가 3 회를 넘겨도 멈추지 않는다. 반대로 `sprint-feedback-*.md` 를 와일드카드로 묶어 합산하면 병렬 스프린트의 판정까지 딸려 들어와 N 이 부풀고 멀쩡한 루프가 조기 중단된다. 세는 파일은 항상 **정확히 하나**다. 기록이 없으면 N=1 로 시작한다.
- **N=3 에서 REJECT 면 루프를 중단**하고 사용자에게 에스컬레이션한다. 남은 REJECT 조건, 지금까지 시도한 수정, 막힌 지점을 그대로 보고하고 자율 재시도를 이어가지 마라. 3 회를 넘겨 계속 도는 것은 스코프 드리프트의 전형이다 (`/insights` Friction #3).

### Step 4.5: 교차 진단 (부모가 띄운다)

QA 가 APPROVE 를 냈어도 이 단계를 건너뛰지 마라. **이 스킬을 실행하는 세션(부모)이 직접**
다른 에이전트를 띄워 판정을 되짚는다.

> **왜 평가자가 아니라 부모인가.** 예전에는 qa-evaluator 가 `tools` 의 `Agent` 로 직접
> 띄우게 했다. 2026-09-22 실측에서 그 설계가 무너졌다 — 평가자가 띄우지 않고도 "띄워서
> 재실행시켰다" 고 리포트에 쓰고 `cross_diagnosis_by: sprint-contract` 로 적었고, 재시도를
> 시켰더니 **두 번째 응답도 지어낸 것**이었다. 도구도 있었고 금지 문장도 있었는데 둘 다
> 통하지 않았다. 부모가 띄우면 호출이 부모 기록에 남고 결과를 부모가 직접 읽으므로
> 지어낼 여지가 없다.

1. 평가자 리포트의 `Cross-Diagnosis Handoff` 절을 읽는다. 계약 절대경로와 판정 결과 전문,
   물을 두 가지가 거기 있다
2. 부모가 `Agent` 도구로 에이전트 1 개를 띄운다. 계약 작성자 관점으로 되짚게 하고,
   **읽기만 하고 어떤 파일도 만들거나 고치지 말라**고 지시한다
3. 돌아온 답이 판정을 뒤집을 근거를 대면 그 조건을 **직접** 재검증한다 — 되짚은 에이전트의
   말만으로 판정을 바꾸지 마라
4. 결과를 반영해 피드백의 `cross_diagnosis_by` 를 `pending-parent` 에서 `sprint-contract` 로
   갱신하고, 답을 `cross_diagnosis_notes` 에 적는다
5. **끝내 띄우지 못했으면** `none` 으로 내리고 사유를 적는다. 하지 않은 교차 진단을
   `sprint-contract` 로 적지 마라 — 그 값은 카이젠의 개선 근거로 쓰인다
6. 띄웠는지 스스로 의심되면 **기록으로 확인한다.** 부모 세션 기록에서 `Agent` 호출을 세고,
   0 을 믿기 전에 양성 대조를 세운다 (직접 하나 띄워 같은 패턴이 1 로 잡히는지 본다)

### Step 5: Commit

QA APPROVE 후 conventional commit 메시지 작성 → 사용자 확인 → commit.

커밋은 **검증 증거가 확보된 수정 단위**로 나눈다. 한 스프린트에서 성격이 다른 수정을 했다면 배치로 묶지 말고 단위별로 커밋한다 (Friction #5 — 배치 커밋은 중간 회귀를 은폐한다).

**내 경로만 싣는다 (2026-09-25 추가).** 작업 폴더를 여러 세션이 같이 쓰면 공용 목록에 남의 변경이 올라 있다.
커밋하기 전에 이번에 실을 경로를 적고 그 경로만 싣는다 (`--only` — <https://git-scm.com/docs/git-commit>):

```bash
git add -- <새 파일…>                       # 추적 안 된 새 파일만 — -o 는 git 이 모르는 경로에서 죽는다
git status --short -- <내 경로…>             # 실을 것 확인. 상태 칸의 D 는 삭제다 — 개수를 사용자에게 보고한다
git diff HEAD -- <내 경로…>                  # 다른 세션이 커밋한 줄을 되돌리지 않는지 본다
git commit -o -m "<메시지>" -- <내 경로…>
git show --name-status --format= HEAD        # 실린 경로 집합이 적은 목록과 같은지 본다
```

- `git add -A` · `git add .` · `git commit -a` · `git commit -i` 를 쓰지 않는다 — 남의 변경과 삭제까지 싣는다
- 확인은 파일 수가 아니라 경로 집합으로 한다. 수가 같아도 다른 파일일 수 있다
- `-o` 는 경로를 가를 뿐 누가 고쳤는지는 모른다. 적은 경로 안에 남의 변경이 섞였으면 위 `git diff HEAD` 줄에 드러난다
- 커밋 안전 훅(`harness/scripts/commit-guard.sh`)은 지정한 경로 안의 삭제가 50 개를 넘으면 막는다. 그보다 작은 삭제는 위 `git status` 줄에서 사용자에게 보고한다

실측(2026-09-14 · 09-23): 잘못된 커밋 하나가 파일 3217 개를 삭제로 기록했고, 다른 커밋 하나는 다른 세션의 커밋 두 개를 되돌렸다.

### Step 6: Push

push 직전 사용자 명시 승인 필수 (Scope-Bound Edits Hard-stop). main 직접 push 는 `--force` 와 동등한 위험으로 분류, 별도 승인 단계.

보고 끝은 `사용자가 할 일: 없음` 또는 `사용자가 할 일: <한 줄>` 로 맺는다 (sprint-contract Step 5 와 같은 문구). 실측(2026-09-19): 한 줄 수정이 계약 · QA 절차에 묻혀 사용자가 「그래서 내가 뭘 하면 되냐」고 물었다.

## References

- `harness/skills/sprint-contract/SKILL.md` — Step 1 위임 대상
- `harness/agents/qa-evaluator.md` — Step 4 spawn 대상
- `harness/docs/guides/skill-design-guide.md` §3.6 — Pre-Edit Batch Audit + Scope-Bound Edits
- `harness/docs/guides/skill-design-guide.md` §3.7 — Completion Evidence Gate + Enforcement 등급 (E1/E2/E3)
- `harness/docs/guides/skill-design-guide.md` §9 — Long-Running Skills + Pre-Sprint Sync Check
- `~/.claude/usage-data/report-ko.html` — `/insights` Quick Win #1 (본 스킬의 source of truth)
- <https://arxiv.org/abs/2605.06527> — STALE (2026-05). 에이전트의 자기 기억 무효화 탐지 정확도 최고 55.2% (Step 0.5 근거)
- <https://arxiv.org/abs/2606.27416> — Glite ARF (2026-06). 병렬 에이전트 task isolation + 완료분 immutability 를 결정론적 verifier 로 강제 (Step 0 파일 소유권 근거)
- <https://git-scm.com/docs/git-worktree> — 워크트리마다 `HEAD` 와 목록을 따로 둔다 (Step 0 워크트리)
- <https://code.claude.com/docs/en/sub-agents> — `isolation: worktree` 는 기본 가지에서 만든다 (Step 0)
- <https://git-scm.com/docs/git-merge-base> — 분기점 (Step 3 원인 가르기)
- <https://git-scm.com/docs/git-commit> — `--only` 는 지정한 경로만 싣는다 (Step 5)
