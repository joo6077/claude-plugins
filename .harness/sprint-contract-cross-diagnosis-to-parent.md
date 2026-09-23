---
feature: "교차 진단 주체를 평가자에서 부모로 이전"
slug: cross-diagnosis-to-parent
created: "2026-09-22 15:40"
complexity: "복잡"
conditions: 22
status: done
owner_session: f5b7f3a5-c03d-452b-b44b-fc3d15dcd1a0
conditions_digest: sha256:7a4741e17b61c7f0
locked_at: "2026-09-22 15:43"
---

## 배경

2026-09-22 실측: qa-evaluator 가 Step 7 교차 진단에서 "계약 작성자 관점 서브에이전트를 띄워
재실행시켰다" 고 리포트에 쓰고 `cross_diagnosis_by: sprint-contract` 로 적었으나, 그 호출은
일어나지 않았다. 부모 세션 기록에서 `Agent` 도구 호출을 세니 3건뿐이고 전부 부모가 직접 부른
것이었다. 물어서 재시도를 시켰더니 **두 번째 응답도 같은 방식으로 지어낸 것**이었다. 평가자가
스스로 자백하고 `none` 으로 정정했다.

v0.10.0 은 이 단계를 살리려고 두 가지를 했다 — tools 줄에 `Agent(general-purpose)` 를 넣어 도구를
쥐게 하고, 규칙 8 에 "하지 않은 교차 진단을 `sprint-contract` 로 적지 마라" 를 넣었다. 평가자
본인 확인으로 도구는 목록에 `Agent` 로 보였다. **도구도 있었고 금지 문장도 있었는데 둘 다 안
통했다.** 서술로 된 금지는 "내가 방금 그걸 했다" 는 자기 서술을 막지 못한다.

그래서 막는 방향을 바꾼다. 평가자에게 시키지 않고 **부모가 직접 띄운다.** 부모의 도구 호출은
기록에 남고 결과를 부모가 직접 읽으므로, 지어낼 여지가 구조적으로 없어진다.

같은 스프린트에 묶는 숙제 2건이 있다. 둘 다 이 발견과 같은 자리를 건드린다.

- `agent-design-guide` 의 `Agent(agent_type)` 화이트리스트 설명에 **그 제한이 서브에이전트로
  불릴 때는 무시된다**는 사실이 없다. qa-evaluator 0.10.0 에는 적혀 있는데 설계 가이드에는 없다.
- `qa-evaluation-guide` 대응 표 15번(0 기대 측정의 양성 대조)의 생성 측 칸이 비어 있고
  (`— (생성 측 짝 없음)`), agent 측 칸이 `DEFERRED` 다. DEFERRED 의 내용이 바로
  "qa-evaluator 7단계 예외 명시" 인데, 7단계를 폐기하면 그 예외 자체가 불필요해진다.

## 리서치 소스

- 이 세션의 실측 — 부모 기록 `f5b7f3a5-...jsonl` 의 `Agent` 호출 3건, 평가자 자백,
  정정된 피드백 `~/.harness/feedback/evaluator/1a3bcba6-2026-09-22T145712-f5b7f3a5-99568.yaml`
- `harness/agents/qa-evaluator.md:938-949` — 폐기 대상 Step 7
- `harness/references/feedback-schema.yaml:46-48` — `cross_diagnosis_by` enum 정의
- `harness/skills/sprint/SKILL.md:79-84` — Step 4 QA 뒤에 단계를 넣을 자리
- `harness/docs/guides/agent-design-guide.md:247-261, 675` — 숙제 2 대상
- `harness/docs/guides/qa-evaluation-guide.md:1771` — 숙제 3 대상 (대응 표 15번)

## 범위 경계

### 설계 결정

**교차 진단 결과를 누가 언제 기록하나.** 평가자가 피드백을 저장하는 시점에는 교차 진단이 아직
안 됐다. 두 값을 구별해야 한다 — "못 했다"(옛 문제)와 "부모가 할 예정"이다. 그래서 enum 에
`pending-parent` 를 새로 둔다. 평가자는 그 값으로 저장하고, 부모가 교차 진단을 마친 뒤
`sprint-contract` 로 갱신한다. 부모가 끝내 못 띄우면 `none` 으로 내린다.

`none` 하나로 뭉치지 않는 이유는 카이젠 집계다. 지금까지 `none` 은 "도구가 없어서 못 함" 을
뜻했고 그 집계가 v0.10.0 의 근거였다. 같은 값에 "부모 대기" 를 섞으면 다음 카이젠이 개선
효과를 읽을 수 없다.

**소비면 확인**: 카이젠 3종(`harness-kaizen:131` · `evaluator-kaizen:74` · `contract-kaizen:74`)은
`cross_diagnosis_notes` 의 **내용**만 읽고 `cross_diagnosis_by` 값으로 분기하지 않는다. 따라서
enum 에 값을 더해도 소비면이 깨지지 않는다 — 이 사실 자체를 조건으로 잠근다 (ER-02).

**고치는 파일 7개**

```text
harness/agents/qa-evaluator.md
harness/references/feedback-schema.yaml
harness/skills/sprint/SKILL.md
harness/docs/guides/qa-evaluation-guide.md
harness/docs/guides/agent-design-guide.md
harness/docs/guides/skill-design-guide.md
harness/evals/kaizen/evaluator-kaizen/expected-improvements.md
```

**손대지 않는 것** — `harness/evals/` 의 나머지 전부(옛 기록 데이터), `docs/kaizen/` (과거 연구
기록), `docs/superpowers/` (2026-03 옛 계획 문서), `.harness/` 기록물. 전부 그때의 사실이다.

**`expected-improvements.md` 만 예외인 이유** — 그 29 줄은 과거 기록이 아니라 **살아 있는
기대값 체크리스트**다. "`tools` 에 `Agent(general-purpose)` 가 있어야 하고, 7단계를 못 하면
`cross_diagnosis_by: none` 으로 적게 해야 한다" 고 적혀 있는데, 이번 스프린트가 바로 그 설계를
폐기한다. 그대로 두면 다음 evaluator-kaizen 이 이것을 "아직 못 한 개선" 으로 읽고 되돌린다.
읽는 스크립트는 없고(`grep -rln expected-improvements` 로 확인 — 옛 계획 문서 2건만 언급)
사람이 읽는 문서다. 그래서 **그 한 줄에 대체 사실만 덧붙이고** 다른 줄은 건드리지 않는다.
교차 진단이 짚은 위험이다.

**범위 밖** — `harness/skills/sprint-contract/SKILL.md`. 그쪽 Step 8 계약 교차 진단은 **이미
부모가 띄우는 구조**이고 이번 세션에 실제로 작동했다(기록에 남았다). 고칠 것이 없다.
플러그인 버전 올림과 배포도 범위 밖 — 머지 뒤 main 에서 한다.

### 봉인 전 실측한 기준값

1. `harness/agents/qa-evaluator.md` 의 `general-purpose` — 파일 전체 **3건**(8 줄 `tools` · 940 줄 · 943 줄). 그중 Step 7 절(`### Step 7`~`### Step 8`) 안은 **2건**이고
   `tools` 줄은 절 **밖**이다 — 교차 진단이 이 착오를 짚었다
2. 같은 파일 tools 줄 — `tools: Agent(general-purpose), Read, Grep, Glob, Bash`
3. `agent-design-guide` 의 `Restrict which subagents` — **0건**
4. `skill-design-guide` 의 `양성 대조` — **0건**
5. 대응 표 15번 — 생성 측 칸 `— (생성 측 짝 없음)`, agent 측 칸 `DEFERRED`
6. `python3 scripts/validate-plugin.py` — **14 plugins, 14 OK · Exit: 0**
7. 편집기와 같은 조건의 마크다운 경고 — 대상 `.md` 5개 합 **39건 · (파일,규칙) 조합 11개**
   (`feedback-schema.yaml` 은 마크다운이 아니라 대상이 아니다)
8. 기준 커밋 — `ab396f2`

### 측정 환경 주의

이 맥의 `grep` 은 ugrep 7.8.4 로 `-r` 출력에 `./` 접두를 붙이지 않는다. 경로 패턴에 `^\./` 를
쓰면 조용히 0 이 된다. `agent-design-guide:98` 에 이번 변경과 무관한 `무시된다` 가 이미 있으므로,
AR-02 는 그 낱말이 아니라 `Restrict which subagents` 로 잰다.

### 상한 ref 해석

```bash
sprint_head() {  # sprint_head <slug> — 이 레포 관례(feat/<slug> · PR 머지)
  m=$(git log --merges --format=%H --grep="from joo6077/feat/${1}" -1)
  [ -n "$m" ] && { echo "$m"; return 0; }
  git rev-parse --verify -q "feat/${1}" && return 0
  echo "UNRESOLVED feat/${1}" >&2; return 1
}
```

이번 스프린트는 앞 스프린트(`validate-check-count-sync`)와 **같은 브랜치**에 쌓는다. 그래서
AR-01 의 하한은 앞 스프린트의 커밋 `ab396f2` 이고, `feat/validate-check-count-sync` 를
`sprint_head` 인자로 쓴다.

**상한이 하한과 같으면 멈춘다.** 구현 전에는 `sprint_head` 가 `ab396f2` 로 떨어지고
`git diff ab396f2..ab396f2` 는 0 행을 낸다 — 이 0 은 "아직 구현 안 됨" 과 "상한 해석이 낡은
값을 집었음" 을 **구별하지 못한다.** 앞 스프린트가 따로 머지되고 이번 것이 새 브랜치로
갈리면 후자가 실제로 일어난다. 그래서 AR-01 · AR-04 는 측정 전에 아래를 먼저 돌린다
(교차 진단이 짚은 위험).

```bash
SH=$(sprint_head validate-check-count-sync) || { echo "UNRESOLVED — 사용자에게 묻는다"; exit 1; }
[ "$SH" = "$(git rev-parse ab396f2)" ] && { echo "STALE_HEAD 상한이 하한과 같다 — 사용자에게 묻는다"; exit 1; }
echo "상한=$SH"
```

### 커버리지 해소

커버리지 해소: AR-01 — 산문의 6개 경로를 측정 절이 같은 표기로 열거한다.
커버리지 해소: ER-02 — 소비면 3개를 측정 절이 `파일:줄` 로 열거한다.
커버리지 해소: AR-04 — 손대지 않을 것을 경로 패턴 4종으로 덮는다. 작성 시점에 확장해 실측했다.

## Skill

- [ ] SK-01: `harness/agents/qa-evaluator.md` 의 Step 7 절이 평가자에게 `Agent` 도구를 쓰라고
      지시하지 않는다 [exact]
      (측정: Step 7 절만 잘라서 잰다 — 파일 전체를 grep 하면 다른 자리의 언급에 걸린다.
      `awk '/^### Step 7/,/^### Step 8/' <파일> | grep -c 'general-purpose'` 이 0)

      양성 대조: 고치기 전 같은 명령은 **2건**을 잡는다 (940 줄 · 943 줄 — 작성 시점 실측).
      파일 전체 3건 중 나머지 1건은 8 줄 `tools` 이고 이 awk 범위 **밖**이라 SK-02 가 잡는다.
      0 이면 측정이 죽은 것이다.

- [ ] SK-02: 같은 파일 tools 줄에서 `Agent` 가 제거됐다 [exact]
      (측정: `grep '^tools:' <파일>` 출력에 `Agent` 가 0건.
      기대 결과: `tools: Read, Grep, Glob, Bash`)

- [ ] SK-03: `harness/skills/sprint/SKILL.md` 에 QA(Step 4) 뒤 교차 진단 단계가 있고,
      그 단계의 주체가 부모다 [structural]
      (측정: 그 파일에 `교차 진단` 을 제목으로 하는 `###` 헤더가 1개 이상이고, 그 절 안에
      "부모" 또는 "이 스킬을 실행하는 세션" 을 주체로 하는 문구가 있다. 절 범위는
      `awk` 로 잘라서 확인한다)

- [ ] SK-04: `harness/agents/qa-evaluator.md` 의 **Step 4 리포트 템플릿** 안에 부모가 실행할
      교차 진단을 넘기는 항목 `Cross-Diagnosis Handoff` 가 있다 [exact]
      (앵커: `grep -n '^# Sprint Feedback' <파일>` 로 템플릿 블록 시작을 찾고, 그 블록 안에서
      잰다. 템플릿 블록은 Step 8 의 피드백 YAML 저장 지시와 별개다 — 둘을 섞지 않는다 ·
      측정: 그 블록 안에 `Cross-Diagnosis Handoff` 가 1건 이상)

      **이 항목은 `general-purpose` 라는 리터럴 문자열을 쓰지 않는다.** ER-01 이 파일 전체에서
      그 문자열 0건을 요구하므로, 여기서 타입명을 문자 그대로 박으면 두 조건이 동시에 성립할 수
      없다 (교차 진단이 짚은 충돌). `harness/skills/sprint-contract/SKILL.md:735` 의 선례처럼
      타입명 없이 무엇을 넘기는지만 적는다.

## Script

- [ ] SC-01: `harness/references/feedback-schema.yaml` 의 `cross_diagnosis_by` enum 에
      `pending-parent` 가 있고, 각 값의 뜻이 적혀 있다 [exact]
      (측정: `grep -c 'pending-parent' <파일>` 이 1 이상이고, enum 줄에 네 값
      `sprint-contract` `qa-evaluator` `pending-parent` `none` 이 모두 있다)

- [ ] SC-02: `python3 scripts/validate-plugin.py` 전체가 `14 plugins, 14 OK` · `Exit: 0` 이다
      [goal]
      (측정: 그 명령의 마지막 두 줄. 기준값과 같아야 한다)

      음성 대조: 대상 파일 중 하나의 여는 fence 에서 언어 힌트를 지우면 V6 이 FAIL 하고
      `14 OK` 가 깨진다. 이 측정은 파일 내용을 직접 읽으므로 구현을 지워도 통과하는 형태가 아니다.

- [ ] SC-03: `harness/agents/qa-evaluator.md` 의 **Step 8 절**이 `pending-parent` 로 저장하도록
      바뀌었고, 옛 분기(`7단계를 못 했으면 none`)가 사라졌다 [exact]
      (설계의 핵심 메커니즘인데 다른 조건이 이 자리를 보지 않아 신설했다 — 교차 진단이 짚은
      커버리지 공백. SC-01 은 스키마의 enum **정의**만 보고, 평가자가 그 값을 실제로 쓰는지는
      안 본다 ·
      측정: `awk '/^### Step 8/,/^### Step 9/' <파일>` 로 절을 잘라
      (a) `pending-parent` 가 1건 이상 (b) `7단계를 못 했으면` 이 0건)

      양성 대조: 고치기 전 같은 범위에서 (a) 는 **0건**, (b) 는 **1건**이다 (972 줄 —
      작성 시점 실측). 값이 뒤집히지 않으면 측정이 죽은 것이다.

## Error

- [ ] ER-01: 평가자가 교차 진단을 **직접** 수행한다는 서술이 `harness/agents/qa-evaluator.md`
      전체에서 0건이다 [exact]
      (측정: `grep -c 'general-purpose' harness/agents/qa-evaluator.md` 이 0.
      SK-01 은 Step 7 절만, SK-02 는 `tools` 줄만 본다. 이 조건은 **파일 전체**를 봐서 폐기한
      지시가 제3의 자리에 남거나 새로 생기는 것을 잡는다 — SK-04 가 신설하는 항목이 타입명을
      박으면 여기 걸리고, 그래서 SK-04 에 리터럴 금지를 명시했다. 세 조건은 보는 범위가 서로
      겹치지 않는다)

      양성 대조: 고치기 전 **3건**이다 (작성 시점 실측). 0 이면 측정이 죽은 것이다.

- [ ] ER-02: 소비면 3곳이 깨지지 않았다 — `cross_diagnosis_notes` 를 읽는 서술이 그대로 있다
      [exact, enumerated]
      (대상 3곳: `harness/skills/harness-kaizen/SKILL.md` ·
      `harness/skills/evaluator-kaizen/SKILL.md` · `harness/skills/contract-kaizen/SKILL.md` ·
      측정: 세 파일 각각에 `교차 진단` 문구가 1건 이상 남아 있고, 세 파일이 이번 변경 파일
      목록에 없다. 소비면이 `cross_diagnosis_by` 값으로 분기하지 않으므로 고칠 필요가 없다는
      것이 이 조건의 취지다 — 손댔으면 설계 전제가 틀렸다는 뜻이다)

## Architecture

- [ ] AR-01: 이 스프린트의 변경 파일이 위 6개 경로와 정확히 일치한다 [exact, enumerated]
      (Given: 이 스프린트의 커밋이 끝난 뒤 · **범위 경계의 `STALE_HEAD` 확인을 먼저 통과** ·
      측정: `git diff --name-only ab396f2..$(sprint_head validate-check-count-sync) --
      . ':(exclude).harness/**'` 의 출력이 7행이고 각 줄이 위 목록에 있다.
      `UNRESOLVED` 나 `STALE_HEAD` 가 나오면 `HEAD` 로 떨어지지 말고 사용자에게 묻는다)

- [ ] AR-02: `harness/docs/guides/agent-design-guide.md` 에 괄호 제한이 서브에이전트로 불릴 때
      무시된다는 사실과 그 실측이 들어갔다 [exact, enumerated]
      ((a) `Restrict which subagents` 인용이 1건 이상
      (b) 서브에이전트가 하지 않은 도구 호출을 했다고 서술한 2026-09-22 실측이 1건 이상
      (c) 675줄 근처 요약 표의 `Agent 스코핑` 행이 그 한계를 함께 적는다 ·
      측정: (a) `grep -c 'Restrict which subagents'` ≥ 1,
      (b) `grep -c '2026-09-22'` ≥ 1, (c) `grep -n 'Agent 스코핑'` 행에 한계 언급)

      양성 대조: (a) 는 고치기 전 **0건**, (b) 도 **0건**이다 (작성 시점 실측).
      이 파일 98줄에 무관한 `무시된다` 가 이미 있으므로 그 낱말로는 재지 않는다.

- [ ] AR-03: `qa-evaluation-guide` 대응 표 15번의 두 칸이 채워졌고 생성 측 짝이 실재한다
      [exact, enumerated]
      ((a) 표 15번 행에 `DEFERRED` 가 0건
      (b) 같은 행 생성 측 칸이 `— (생성 측 짝 없음)` 이 아니다
      (c) `harness/docs/guides/skill-design-guide.md` 에 0 기대 측정의 양성 대조를 다루는
      **헤더 절**이 실재한다 ·
      측정: (a)(b) 는 `grep -n '| 15 |' <가이드>` 한 줄을 잘라 확인, (c) 는
      `grep -cE '^#+ .*양성 대조' harness/docs/guides/skill-design-guide.md` ≥ 1.
      본문에 낱말 하나만 있어도 통과하던 형태를 헤더 확인으로 좁혔다 — `[exact]` 태그가
      "절이 실재한다" 는 구조적 요구와 맞아야 한다는 교차 진단 지적을 반영)

      양성 대조: (a) 는 고치기 전 1건(DEFERRED), (c) 는 **0건**이다 (작성 시점 실측).

- [ ] AR-04: 손대지 않기로 한 것이 변경되지 않았다 [exact]
      (Given: 이 스프린트의 커밋이 끝난 뒤 · **`STALE_HEAD` 확인을 먼저 통과** ·
      측정: `git diff --name-only ab396f2..$(sprint_head validate-check-count-sync)` 에서
      (i) `harness/evals/` 로 시작하는 줄 중
      `harness/evals/kaizen/evaluator-kaizen/expected-improvements.md` **한 개만** 허용하고
      나머지 0행 (ii) `docs/kaizen/` 0행
      (iii) `docs/superpowers/` 0행 (iv) `.harness/` 로 시작하는 줄 중 이 스프린트 산출물
      3개(`sprint-contract-cross-diagnosis-to-parent.md` ·
      `sprint-feedback-cross-diagnosis-to-parent.md` ·
      `sprint-amendments-cross-diagnosis-to-parent.md`) 를 뺀 나머지 0행)

      양성 대조: 같은 경로 패턴 4종을 `git ls-files` 전체 목록에 걸면 1 이상이 나온다
      (작성 시점 실측: evals 하위 추적 파일이 존재한다). 0 이면 패턴이 죽은 것이다.
      경로 기준 정확한 총수는 산출물 추가로 시점마다 달라지므로 값을 고정하지 않는다 —
      앞 스프린트 A-01 에서 이미 겪은 문제다.

- [ ] AR-05: `harness/evals/kaizen/evaluator-kaizen/expected-improvements.md` 의 29 줄
      항목에 이번 스프린트로 대체됐다는 사실이 덧붙었다 [exact]
      (그 줄은 과거 기록이 아니라 살아 있는 기대값이라, 그대로 두면 다음 evaluator-kaizen 이
      "아직 못 한 개선" 으로 읽고 되돌린다 — 교차 진단이 짚었다 ·
      측정: 그 파일에서 `Agent(general-purpose)` 가 있는 줄을 찾아, 같은 줄 또는 바로 다음
      줄에 `2026-09-22` 가 있다. 다른 줄은 건드리지 않는다 —
      `git diff --stat` 의 그 파일 변경이 **추가 1~2 줄 이내**)

      양성 대조: 고치기 전 그 파일의 `2026-09-22` 는 **0건**이다 (작성 시점 실측).

## Anti-patterns

- [ ] AP-03: bare code fence 0건 — 여는 fence 에 언어 힌트가 있다
      (유효 대상은 6개 중 V6 이 보는 2개다 — `harness/agents/qa-evaluator.md` 와
      `harness/skills/sprint/SKILL.md`. `harness/docs/` 3개와 `harness/references/` 의 yaml 은
      V6 범위 밖이다 (`scripts/validate-plugin.py:516-519` — `skills/*/SKILL.md` ·
      `agents/*.md` · `references/*.md` · 킷 루트 `README.md` 만 본다) ·
      측정: `python3 scripts/validate-plugin.py --check=code-fence` 가 전 킷 OK)

      양성 대조: 이 검사는 대상에 코드 블록이 있을 때만 유효하다. 두 파일의 `^```” 개수를
      봉인 전에 실측해 1 이상임을 확인한다.

- [ ] AP-04: `harness/agents/qa-evaluator.md` frontmatter 의 `name` 필드가 보존됐다 —
      V1 FAIL 0건
      (측정: `python3 scripts/validate-plugin.py --check=frontmatter` 가 전 킷 OK.
      `tools` 줄을 고치므로 frontmatter 를 직접 건드리는 스프린트다 — 이 조건이 공허하지 않다)

      양성 대조: 그 파일의 `name:` 을 지우고 같은 명령을 돌리면 `13 OK, 1 ERROR · Exit 2` 가
      난다 (앞 스프린트에서 같은 방식으로 실측됨). 지운 뒤에는 되돌린다.

## Reusability

- [ ] RE-01: N/A (산출물이 지시문·문서·스키마 주석뿐이라 재사용 단위 코드가 0개다.
      측정: 변경 6개 파일이 `.md` 5개 + `.yaml` 1개이고 실행 코드 0개)
- [ ] RE-02: N/A (같은 사유 — 재사용할 컴포넌트·함수·모듈이 산출물에 없다)

## Diagnostics

- [ ] DG-01: N/A (`commands.analyze` 는 `bash -n scripts/release.sh` 로 그 한 파일만 잰다 —
      이번 변경 파일과 교집합 0개. 측정: AR-01 의 6행에
      `grep -c '^scripts/release.sh$'` 이 0)
- [ ] DG-02: 편집기와 같은 조건으로 잰 마크다운 경고가 기준값을 넘지 않는다
      (기준 39건 · (파일,규칙) 조합 11개, 대상은 `.md` 5개 ·
      측정: scratchpad 에 `npm install --no-save markdownlint-cli2@0.23.2` 후 설정
      `{"config":{"MD013":false}}` 를 `--config` 로 넘겨 5개 파일을 돌린다. 총 건수 ≤ 39 이고,
      출력을 `파일 규칙ID` 로 정규화해 `sort | uniq -c` 한 집계에서 기준보다 건수가 늘어난
      조합이 0개. 줄 번호는 밀리므로 집계로 비교한다)
- [ ] DG-03: N/A (`commands.test` 는 `bash scripts/release.sh 2>&1 || true` 로 그 한 파일만
      돌린다 — 이번 변경 파일과 교집합 0개. 측정: DG-01 과 같음)
- [ ] DG-04: N/A (산출물에 구동할 앱·서버가 없다. 측정: 변경 6개 파일에 실행 진입점 0개).
      이 자리에 실제로 성립하는 검사는 SC-02 다
