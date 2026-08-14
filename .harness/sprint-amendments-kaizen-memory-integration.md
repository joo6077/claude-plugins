# Sprint Amendments — kaizen-memory-integration

계약 본문은 수정하지 않는다. 이 사이드카에만 기록한다.

---

## AM-01 — AR-01 열거 집합에 정의 파일 1 경로 누락

- **id**: AM-01
- **target**: `AR-01` (레포 변경 경로 열거)
- **direction**: `relaxing` — 자기신고가 아니라 스키마 §Amendment 의 `amend_direction` 을
  그대로 실행해 **계산**했다. zsh · bash 동일:

  ```text
  relaxing added=1 removed=0
  추가된 원소: reflect-kit/references/memory-grounding.md
  ```

- **consent**: `anchored` — **사용자 승인 2026-08-14.** 오케스트레이터가 3 선택지
  (열거 확대 / 파일 이동 / FAIL 수용)와 write-once 선례를 제시하고 **"열거 확대"** 를 선택받았다
- **판정 효력**: **PASS 근거로 사용 가능.** 스키마 §Amendment 규약상 `relaxing` 은
  `consent: anchored` 일 때만 PASS 근거가 된다 — 이 조건을 충족한다.
  QA 는 `AR-01` 을 아래 **5 경로 집합** 기준으로 판정한다:

  ```text
  scripts/collect-kaizen-data.py
  .claude/skills/kaizen-orchestrator/SKILL.md
  reflect-kit/skills/reflect-digest/SKILL.md
  reflect-kit/skills/reflect-promote/SKILL.md
  reflect-kit/references/memory-grounding.md      ← 이 amendment 가 추가
  ```

- **승인 근거**: 추가되는 1 경로는 `SK-02` 가 **요구한 산출물**(grounding 4 값 의미 정의의 SSOT)
  이며 새 기능이 아니다. 계약이 그 산출물을 요구하면서 경로를 열거하지 않은 것이 결함이다

### 무엇이 어긋났나

계약 `AR-01` 이 기대하는 집합 (4 경로):

```text
scripts/collect-kaizen-data.py
.claude/skills/kaizen-orchestrator/SKILL.md
reflect-kit/skills/reflect-digest/SKILL.md
reflect-kit/skills/reflect-promote/SKILL.md
```

구현 커밋 `ca1f5f4` 의 실제 집합 (5 경로):

```text
.claude/skills/kaizen-orchestrator/SKILL.md
reflect-kit/references/memory-grounding.md        ← 계약이 열거하지 않은 1 건
reflect-kit/skills/reflect-digest/SKILL.md
reflect-kit/skills/reflect-promote/SKILL.md
scripts/collect-kaizen-data.py
```

측정 (계약 원문 오라클):

```bash
git diff --name-only ca1f5f4^ ca1f5f4 -- ':(exclude).harness/*'
```

**direction 계산** — 기대 집합 ⊂ 실제 집합이고 실제에만 있는 원소가 1 개다.
제거된 경로는 0 개이므로 `relaxing` (허용 범위가 넓어짐). 서술 판단이 아니라 집합 비교 결과다.

### 왜 누락됐나

`SK-02` 가 grounding 4 값의 **의미 정의가 정확히 1 파일에만** 존재할 것을 요구한다. 즉 정의 파일은
계약이 **요구한** 산출물이다. 그런데 계약 작성 시점에 그 파일의 **경로를 확정하지 않고**
구현 에이전트 판단에 맡겼고, `AR-01` 열거에는 그 자리를 비워두지 않았다.

**계약 자체의 결함**이다 — SK-02 가 요구하는 산출물을 AR-01 이 금지하는 상호 모순이다.
이 스프린트에서 발견된 네 번째 측정문 결함이며, 앞선 셋과 성격이 다르다:

| # | 결함 | 성격 | 처리 |
| --- | --- | --- | --- |
| 1 | `SK-02` ↔ `ER-02` 상호 모순 | 구조적 충족 불가 | 본문 수정 (QA 전) |
| 2 | 자기참조 — 계약·리서치 인용이 위반으로 계수 | 구조적 충족 불가 | 본문 수정 (QA 전) |
| 3 | `AR-02` 상태 전제 누락 | 구조적 충족 불가 | 본문 수정 (QA 전) |
| 4 | `AR-01` 열거 누락 (이 건) | **허용 집합 확대** | **사이드카 · 앵커 확보 (2026-08-14)** |

1~3 은 어떤 구현으로도 통과할 수 없는 결함이라 수정이 정당하다. 4 는 다르다 —
**생성자가 자기 산출물을 사후에 허용하려 열거를 넓히는 형태**이며, `contract-schema.md`
§계약 봉인 이 인용하는 2026-08-11 REJECT 선례
(*"계약 write-once 위반 — 생성자가 자신이 만든 산출물을 사후에 허용하려 계약 AR-04 조건 문구를
직접 편집(5→7 경로, 사이드카/사용자 승인 앵커 없음)"*)와 **같은 형태**다.
그래서 본문을 고치지 않고 여기에 남긴다.

### 요청하는 처리

**확정 — 선택지 1 «열거 확대 승인» (사용자, 2026-08-14).**

`AR-01` 기대 집합에 `reflect-kit/references/memory-grounding.md` 를 추가한다.
계약 **본문은 수정하지 않았다** — 이 사이드카가 읽는 법을 덧붙일 뿐이다 (스키마 §Amendment 규약).

제시했던 대안과 기각 사유:

- **파일 이동** — 정의를 이미 열거된 4 경로 안으로 옮긴다. 계약 무수정이지만 SSOT 를 스킬 파일
  안에 두면 `reflect-digest`·`reflect-promote` 양쪽이 참조하기 어색해진다
- **FAIL 수용** — 이번 iteration 을 REJECT 로 두고 다음 계약에서 정정. 구현에 고칠 것이 없는데
  REJECT 를 남기는 형태라 채택하지 않았다

### 재발 방지 (다음 계약 작성 시)

**조건이 산출물을 요구하는데 그 경로를 계약 시점에 확정할 수 없으면, scope 조건의 열거에
그 자리를 미리 비워두거나 "SK-02 가 요구하는 정의 파일 1 건" 같은 **역할 기반 항목**으로 넣어라.**
경로를 모른다고 열거에서 빼면, 구현이 그것을 만드는 순간 scope 위반이 된다.
