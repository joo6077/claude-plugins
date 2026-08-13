# Phase 4 → Phase 2 (contract) 핸드오프 — 계약 scope 구조 개정 제안

- 작성: 2026-08-13 · 카이젠 Phase 4 (`kaizen-phase4-doc-contract-gates`)
- 대상 파일: `harness/references/contract-schema.md` · `harness/skills/sprint-contract/SKILL.md`
- **Phase 4 는 이 두 파일을 수정하지 않았다.** Phase 2 소관이라 scope 밖이다
  (확인: `git diff --name-only b161d80..HEAD` 에 두 경로 0 건).
  이 문서는 **어디를 어떻게 고칠지의 제안**이며, 반영 주체는 다음 contract-kaizen 이다.

## 왜 이 문서가 있는가

이번 사이클 Phase 3 에서 계약 scope 조항이 **세 번 연속** 스프린트를 깨뜨렸다
(`.harness/sprint-contract-kaizen-phase3-unverified-triage.md` §폐기·재작성).
Phase 4 스프린트에서 **네 번째 변종**이 또 나왔다 (§F4). 경로를 하나씩 추가하는 대응은
두더지잡기이며, 실측상 실패했다. 스키마 레벨에서 구조를 바꿔야 한다.

독립 평가자의 진단이 정확하다: **"파일 단위 exact enumeration 은 다중 커밋 오케스트레이션
스프린트에 구조적으로 취약하다."**

---

## F1. 계약 산출물·부기 경로가 scope 열거에서 빠져 교정 행위 자체가 위반이 된다

**실측**: Phase 3 원 계약의 열거 경로 집합에 amendment 사이드카 경로가 없었다. 교정을 기록하는
행위가 곧 계약 위반이 되는 자기모순이라 계약을 폐기·재작성해야 했다 (커밋 `b161d80`).
v2 로 경로를 5 개로 늘린 직후, 오케스트레이터가 `.harness/.meta/orchestrator-audit-log.md` 를
커밋해 **또** 열거 밖으로 튀어나왔다.

**뿌리**: 스프린트가 "구현으로 바꾼 것" 과 "harness 가 스스로 남기는 부기" 를 한 집합에
욱여넣는다. 후자는 스프린트 주체가 통제하지 않는다 (오케스트레이터·평가자도 쓴다).

**제안 — `harness/references/contract-schema.md`**

삽입 위치: `#### Diff-Scope Oracle 표준형 (v4 추가)` 절 **바로 뒤**에 새 소절을 만든다.

```markdown
#### 구현 경로 / harness 부기 경로 분리 (v5.4 제안)

변경 범위 조건은 **두 집합으로 나눠 각각 다른 방식**으로 잰다. 한 집합에 섞으면 스프린트가
통제하지 않는 파일까지 exact enumeration 에 들어가 계약이 스스로 깨진다.

| 집합 | 무엇 | 판정 방식 |
| ------ | ------ | ------ |
| 구현 경로 | 이 스프린트가 의도적으로 바꾸는 소스 | **exact enumeration** (기존 Diff-Scope 표준형) |
| harness 부기 경로 | 계약·사이드카·피드백·오케스트레이터 메타 | **범주 규칙** — 아래 4 패턴에 매치하면 위반 아님 |

harness 부기 4 범주 (계약마다 다시 열거하지 마라 — 이 표가 SSOT):

- `{CONTRACT_ROOT}/.harness/sprint-contract-<slug>.md`
- `{CONTRACT_ROOT}/.harness/sprint-amendments-<slug>.md`
- `{CONTRACT_ROOT}/.harness/sprint-feedback-<slug>.md`
- `{CONTRACT_ROOT}/.harness/.meta/**` (오케스트레이터 감사 로그·데이터 풀·evidence 등)

**부기 경로를 구현 경로 열거에 적지 마라.** 적는 순간 다시 파일 단위 관리가 되고,
다음에 harness 가 파일 하나를 더 쓰는 순간 같은 사고가 재발한다.
```

**제안 — `harness/skills/sprint-contract/SKILL.md`**

계약 초안을 만드는 절(범위 경계를 쓰는 단계)에 Gotcha 1 개를 추가한다.

```markdown
- **scope 조건을 쓸 때 계약 자신·사이드카·피드백·`.harness/.meta/**` 를 구현 경로 열거에
  넣지 마라.** 이 넷은 harness 부기 범주이며 `contract-schema.md` §구현 경로 / harness 부기
  경로 분리 가 SSOT 다. 실측: 열거에서 빠지면 amendment 를 남기는 행위가 계약 위반이 되고
  (2026-08-13 Phase 3 계약 폐기), 넣어서 관리하면 오케스트레이터가 파일을 하나 더 쓰는 순간
  다시 깨진다 (같은 날 v2 에서 재발).
```

---

## F2. `git status --porcelain` 오라클은 커밋 이후 항상 0 행이라 재현 불가능하다

**실측**: Phase 3 AR-01 이 이 오라클을 썼고, 커밋 후 평가하는 QA 시점에는 항상 0 행이라
조건을 검증할 수 없었다.

**제안 — `harness/references/contract-schema.md`**

삽입 위치: `#### Diff-Scope Oracle 표준형 (v4 추가)` 절의 4 요소 설명 **바로 아래**.

```markdown
**상태 전제는 커밋 전후 무관하게 재현 가능해야 한다.** `git status --porcelain` 을 행 수
오라클로 쓰지 마라 — 커밋 직후에는 항상 0 행이라 평가 시점에 조건을 재현할 수 없다
(실측 2026-08-13). 스프린트 base 커밋을 `Given:` 에 못박고 `git diff --name-only <base>..HEAD`
로 **누적 diff** 를 재라. base 는 직전 Phase 의 종료 커밋 SHA 를 리터럴로 적는다.
```

---

## F3. 다중 커밋 스프린트에서 `base..HEAD` 는 다른 주체의 커밋을 흡수한다

`base..HEAD` 는 재현 가능하지만, 그 사이에 **오케스트레이터가 끼워 넣은 커밋**도 함께 잡는다.
Phase 3 세 번째 실패가 정확히 이 형태였다 (감사 로그 append 를 앞당겨 커밋).

**두 가지 선택지와 트레이드오프 — 스키마는 둘 다 허용하고 계약이 하나를 고르게 한다.**

| 방식 | 오라클 | 장점 | 위험 |
| ------ | ------ | ------ | ------ |
| A. 누적 diff + 범주 제외 | `git diff --name-only <base>..HEAD -- . ':(exclude).harness'` 로 구현 경로를 재고, `.harness` 는 F1 의 범주 규칙으로 따로 잰다 | 커밋 **누락이 없다** — 그 구간의 모든 변경이 둘 중 하나에 반드시 걸린다 | 다른 Phase 가 같은 구간에 구현 커밋을 넣으면 이 계약이 그 책임까지 진다 |
| B. 커밋 집합 귀속 | 이 Phase 의 커밋만 골라 `git show --name-only` 합집합 (예: 제목 접두 `feat(kaizen): Phase N`) | 다른 주체의 커밋을 흡수하지 않는다 | **커밋 누락을 은폐한다** — 접두를 안 붙인 커밋은 집합에서 조용히 빠져 scope 위반이 검출되지 않는다. 제목 규약에 의존하는 것도 약한 결합이다 |

**권고: 기본은 A.** B 의 은폐 위험이 A 의 과잉 귀속보다 나쁘다 — A 에서 남의 커밋이 섞이면
**소리 나게 실패**하지만, B 에서 커밋이 빠지면 **조용히 통과**한다. 게이트는 조용한 통과를
가장 경계해야 한다 (`harness/evals/gate-exit-codes.md` 와 같은 원칙).
B 를 쓰려면 계약에 **커밋 SHA 목록을 명시**하고, 그 목록의 합집합이 `base..HEAD` 와 같은지
확인하는 조건을 **함께** 넣어야 한다 (누락 은폐 방지). 이 이중 조건이 부담스러우면 A 를 써라.

**제안 삽입 위치**: F2 의 문단 바로 뒤, 같은 소절.

---

## F4. 게이트 **전체** 통과를 조건에 걸면 스프린트가 소유하지 않은 행까지 책임진다 (신규)

**실측 (Phase 4 자체 스프린트)**: 조건 `SC-04` 를
*"`python3 scripts/validate-post-kaizen.py --since <base>` 출력에 `doc-contracts` 행이 있고
FAIL 0 · 종료 코드 0"* 으로 썼다. 그런데 이 게이트는 사이클 **종료 단계** 산출물
(`docs/kaizen/changelog.md` · `docs/kaizen/research-log.md` · `.harness/.meta/cleanup-log.yaml` ·
`kaizen-failure-count.yaml` · `evals-audit-*.md`)도 함께 검사한다. 그 다섯 행은 Phase 4 가
**만들 수 없고 만들어서도 안 되는** 것들이다 (오케스트레이터 Step F1~F4 소관, 일부는 scope 밖).
결과적으로 조건이 스프린트 내에서 원리적으로 만족 불가능해졌다 — F1 과 같은 자기모순의 변종이며,
이번 사이클에서 **네 번째** 재발이다.

**제안 — `harness/references/contract-schema.md`**

삽입 위치: `#### 조건 작성 preflight — QA 모호성 태그의 되먹임 (v5.3 추가)` 표에 **행 1 개 추가**
(태그 열: `측정-소유권-초과`).

```markdown
| `측정-소유권-초과` | 측정이 이 스프린트가 **생산하지 않는 산출물**의 상태에 의존하지 않는가 — 게이트를 오라클로 쓸 때는 전체 종료 코드가 아니라 **이 스프린트가 소유한 행**으로 한정했는가 |
```

그리고 같은 절 아래에 규약 한 문단:

```markdown
**게이트 스크립트를 오라클로 쓸 때는 소유한 행으로 한정하라.** `validate-post-kaizen.py` 처럼
사이클 전체를 보는 게이트는 종료 단계 산출물까지 검사한다. 조건에 "전체 FAIL 0" 을 걸면
스프린트가 통제하지 않는 항목의 상태가 판정에 섞인다. 올바른 형태는 **행 한정**이다 —
"`doc-contracts` 행이 존재하고 그 상태가 PASS 이며, 종료 코드가 인프라 오류(2)가 아니다".
전체 게이트 green 은 오케스트레이터 Final 단계 계약의 조건이지, Phase 계약의 조건이 아니다.
```

---

## 참고 — Phase 4 가 이번 계약에서 실제로 시연한 형태

`.harness/sprint-contract-kaizen-phase4-doc-contract-gates.md` 의 `AR-01` / `AR-02` 가 F1+F3-A 를
그대로 구현한 예다. 조문을 옮길 때 참고할 수 있다.

- `AR-01` — 구현 경로만 exact enumeration, 측정에서 `':(exclude).harness'` 로 부기를 제외
- `AR-02` — `.harness/` 하위는 4 정규식 범주로 판정, 미매치 0 행

이 형태로 쓴 결과, 이번 스프린트에서 오케스트레이터가 감사 로그를 언제 커밋하든 계약이 깨지지
않았다. 반대로 `SC-04` 는 F4 를 몰라서 그대로 밟았다 — 같은 계약 안에서 성공 사례와 실패 사례가
하나씩 나온 셈이라 대조하기 좋다.

## 부수 발견 — scope 밖이라 손대지 않은 것

`.claude/skills/meta-kaizen/SKILL.md:16` 이 오케스트레이터의 단계 번호를
`Step 11, Step 11.5, Step 11.6, Step 12` 로 참조한다. Phase 4 가 그 네 단계를
`Step F1~F4` 로 개명했으므로(Phase 11~14 생성 헤딩과 번호가 충돌해서) 이 참조는 **stale** 이다.
헤딩에 `(구 Step 11)` 형태의 브릿지를 남겨 검색은 되지만, meta-kaizen 은 Phase 4 scope 밖이라
직접 고치지 않았다. **meta-kaizen 을 다루는 Phase 가 정정할 것.**
