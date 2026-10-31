<!-- 옮김: L378-L445 -->

# QA Evaluator — 계약 선택의 드문 갈래

## Step 1 계약 선택 (이어서)

### 1-c 의 3.5 · 4 · 1x 단계

#### 1-c-2. 3.5 단계 — 레거시 브릿지 (active 0 개일 때)

`status` 필드가 도입되기 전에 만들어진 계약은 전부 레거시(= `status` 없음)이며 active 후보에서
빠진다. **레거시만 있는 프로젝트를 그대로 BLOCKED 로 떨어뜨리면 명백한 회귀다** — 변경 전
평가자는 plain `sprint-contract.md` 를 조건 없이 읽었기 때문이다. active 가 0 개이면:

| 3.5 하위 규칙 | 조건 | 선택 |
| ------ | ------ | ------ |
| **3.5-a plain 우선** | 레거시 중 plain `sprint-contract.md` 가 **있다** | 그것을 쓴다 (= 변경 전 동작 그대로) |
| **3.5-b 유일 접미형** | plain 이 없고 레거시가 **정확히 1 개** | 그것을 쓴다 |
| 그 외 | plain 없고 레거시 2 개 이상 | 4 단계 BLOCKED |

**3.5 로 선택했으면 `legacy_contract_used: true` 를 Sprint Feedback 의 `Contract Fingerprint`
블록에 적고, verdict 본문에도 경고를 노출한다:**

```text
⚠️ legacy_contract_used: true — 이 계약에는 `status` 필드가 없어 레거시 브릿지(ladder 3.5)로
   선택했습니다. 병렬 세션에서는 대상이 어긋날 수 있습니다.
   권장: 계약 frontmatter 에 `status: active` 를 추가하거나 HARNESS_CONTRACT 로 고정하세요.
```

> **왜 plain 을 우선하는가 (실측 근거):** 2026-07-28 기준 `CONTRACT_ROOT` 9 개 중 8 개가 레거시
> 전용이고, **그 8 개 전부가 plain `sprint-contract.md` 를 갖고 있다.** 반면 접미형 레거시는
> `fit-pal/app` 27 개 · `fit-pal/server` 12 개처럼 과거 스프린트가 쌓여 있다. "레거시가 정확히
> 1 개일 때만" 이라는 규칙만 두면 이 3 개 배포본은 여전히 BLOCKED 가 되어 회귀가 남는다.
> plain 우선은 변경 전 동작(plain 을 조건 없이 읽음)과 정확히 같으므로 회귀가 0 이다.

#### 1-c-3. 4 단계 — BLOCKED (복구 방법 필수)

```text
BLOCKED: 평가 대상 계약을 결정론적으로 특정할 수 없습니다.
active 후보 ({N} 개):
  - .harness/sprint-contract-<slug-a>.md  (status=active, owner=<세션 또는 미지정>)
  - .harness/sprint-contract-<slug-b>.md  (status=active, owner=<세션 또는 미지정>)
레거시 후보 (status 필드 없음 · plain 부재로 브릿지 불가, {M} 개):
  - .harness/sprint-contract-<legacy-a>.md
  - .harness/sprint-contract-<legacy-b>.md

복구 방법 (둘 중 하나):
  1) 평가 대상을 명시한다
       HARNESS_CONTRACT=<절대경로> 로 다시 호출
  2) 계약 frontmatter 를 정리한다
       평가할 계약에 `status: active` 추가 (따옴표 없이)
       종료된 계약은 `status: done` 으로 변경
```

**BLOCKED 를 낼 때 후보 목록과 위 복구 방법 2 가지를 반드시 함께 출력한다.** 사유만 적고 끝내면
사용자는 무엇을 해야 하는지 알 수 없고, 결국 계약 파일을 손으로 뒤지게 된다.

**모호할 때 조용히 하나를 고르지 않는다.** mtime 최신순으로 정렬해 고르거나, 후보 중 하나를
그럴듯해 보인다는 이유로 골라 진행하는 fallback 을 **두지 않는다.** 잘못 고른 계약으로 내린
verdict 는 다른 세션의 작업을 오판하고, 그 오판은 피드백 저장소까지 오염시킨다.

#### 1-c-4. `LADDER="1x 명시경로부재"` — 지정 경로가 없을 때 (전용 BLOCKED)

`HARNESS_CONTRACT` 가 설정됐는데 그 파일이 없으면 **여기서 끝낸다.** 아래 단계로 흘려보내면
"명시했는데 다른 계약이 채점되는" 조용한 오귀속이 되고, 빈 값으로 진행하면 Step 5 가 TOCTOU 로
오진한다.

```text
BLOCKED: 지정한 계약 경로가 존재하지 않습니다: {HARNESS_CONTRACT}
  이것은 TOCTOU(평가 중 변경)가 아니라 처음부터 없던 파일입니다.

복구 방법 (둘 중 하나):
  1) 경로를 고친다 — 절대경로 · 파일명은 `sprint-contract.md` 또는 `sprint-contract-<slug>.md`
  2) HARNESS_CONTRACT 를 해제하고 다시 호출한다 — ladder 2~3.5 자동 선택으로 내려간다
```

<!-- 옮김: L584-L614 -->

## Step 1 계약 부재

### 1-f

#### 1-f. 계약 부재 — **사유를 혼동하지 마라**

BLOCKED 사유가 3 가지이며 복구책이 서로 다르다. 틀린 사유를 적으면 사용자는 있지도 않은 문제를
고치려 든다. `CONTRACT_ROOT` 가 비었는데 "계약이 없습니다" 라고 적는 것이 그 오진이다 — 계약은
멀쩡히 있고 **`.harness` 를 못 찾은 것**이다.

| 상태 | 사유 | 복구책 |
| ------ | ------ | ------ |
| `CONTRACT_ROOT` 가 빔 | `.harness` 디렉토리를 찾지 못함 | `/harness init` (1-a 의 전용 BLOCKED 문구를 쓴다) |
| `LADDER="0 계약부재"` (후보 0 건) | 계약 파일이 없음 | `/sprint-contract` (아래 문구) |
| `LADDER="1x 명시경로부재"` | 지정 경로가 없음 | 경로 수정 또는 `HARNESS_CONTRACT` 해제 (1-c-4) |
| `LADDER="4 BLOCKED"` | 후보는 있으나 **모호** | 후보 나열 + `status` 정리 (1-c-3) |

> **후보 0 건을 `4 BLOCKED` 로 뭉뚱그리지 마라.** "결정론적으로 특정할 수 없습니다" 라며 빈
> 후보 목록을 출력하게 되어, 사용자는 있지도 않은 계약들의 `status` 를 정리하려 든다. 부재와
> 모호는 다른 사유이고 복구책도 다르다 (1-c 의 `LADDER="0 계약부재"` 분기).

`CONTRACT_ROOT` 가 확정됐는데 후보가 하나도 없을 때만 아래를 쓴다:

```text
BLOCKED: Sprint Contract가 존재하지 않습니다.
  CONTRACT_ROOT: {확정된 절대경로}
  탐색한 디렉토리: {CONTRACT_ROOT}/.harness (후보 0 건)
/sprint-contract를 먼저 실행해주세요.
```

이때 `contract_root_unconfigured: true` 이면 `/harness init` 도 함께 안내한다 —
`.harness` 는 있는데 `project.yaml` 도 계약도 없는, 초기화가 끝나지 않은 디렉토리다.

**추측으로 진행하지 않는다. 계약 없으면 평가 없다.**
