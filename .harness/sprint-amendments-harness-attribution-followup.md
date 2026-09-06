# Sprint Amendments — harness-attribution-followup

> **이 파일은 봉인된 계약의 보완이지 대체가 아니다.**
> `.harness/sprint-contract-harness-attribution-followup.md` 는 write-once 이며 조건 줄을
> 수정하지 않았다 (`conditions_digest: sha256:1ae9a29f5adabadf`, `SEAL_OK`).
> 아래 인용은 전부 **원문 그대로**다.

## AM-01 — 기록 전용 (direction 없음)

- **대상 조건**: `AR-01` · `DG-04`
- **변경**: **없다.** 조건 문구를 고치지 않았으므로 PASS 집합이 움직이지 않는다
  (집합 비교: `added=0 removed=0` → 조건 집합 불변, direction 판정 대상 아님).
  이 엔트리는 **작성자가 스스로 발견한 오라클 결함을 기록만** 한다.
- **근거**: 구현 직후 측정에서 두 조건의 측정 명령이 조건 의도와 다른 것을 재고 있음을 확인했다.
- **앵커**: 없음 — 작성자 자체 발견이므로 `consent: unanchored`.

### 결함 1 · `AR-01` — `측정-방식-불일치`

원문: *"`git diff --name-only 3cd7dfe -- .harness/` 결과가 이 계약 파일과 사이드카 파일 2 개뿐이고,
`harness/` · `bambu-kit/` · `docs/` 경로 0 건이다"*

두 가지를 못 잰다.

1. **미추적 파일이 `git diff` 에 안 보인다.** 이 스프린트의 산출물은 둘 다 신규 파일이라
   작성 직후에는 `??` 상태였고, 그 시점 측정값은 `2` 가 아니라 **`0`** 이었다.
2. **동시 작성자를 구분하지 않는다.** 이후 동시 편집 세션이 커밋하면서 같은 pathspec 에
   `sprint-contract-docs-quality-gates.md` · `stale-values.yaml` ·
   `docs/backend/fundamentals/api-design.md` 가 섞였다. 또 이 스프린트 자신의 QA 산출물
   (`sprint-feedback-harness-core-defects.md`, 계약 status 전환)도 함께 잡힌다 —
   이들은 "변경 범위" 가 아니라 평가 부산물이다.

의도는 "내가 만진 파일 집합" 인데 오라클은 "두 커밋의 차이" 를 잰다.
**고친 형태**: 파일을 열거하고 각각이 diff 에 있는지를 확인한다 (남의 변경이 섞여도 안 깨진다).

```text
- [ ] AR-01': 이번 스프린트가 생성한 기록물 2 개가 각각 존재하고 baseline 이후 추가됐다
      [exact, enumerated]
      (측정: 두 경로 각각에 대해 `git log --oneline <BASE>..HEAD -- <path>` 가 1 건 이상)
```

### 결함 2 · `DG-04` — `측정-방식-불일치`

원문: *"생성한 기록물 2 개가 Step 6.5 게이트 기준(허용 헤더만 사용 · 조건 체크박스가 조건
섹션에만 존재 · frontmatter conditions 값 일치)을 위반 0 건으로 통과한다"*

Step 6.5 는 **계약 파일의 파서 호환성** 게이트다. 사이드카에는 적용되지 않는다 —
`harness/references/contract-schema.md` §Amendment 사이드카 가 *"사이드카는 **별도 파일**이지
계약 섹션이 아니다"* 라고 명시하고, 기존 사이드카 2 건
(`sprint-amendments-bambu-seam-policy.md` · `sprint-amendments-tone-kit-readability.md`)도
`## AM-01` · `## 문제 실측` 같은 자유 헤더를 쓴다.

**조건이 틀렸고 구현이 맞다.** 조건을 만족시키려고 사이드카를 관례에 어긋나게 고치지 않았다 —
나쁜 조건이 산출물을 망치게 두는 것이기 때문이다.
계약 파일 쪽은 이 게이트가 정당하게 적용되며 **위반 0 건으로 통과**한다.

**고친 형태**: 산출물 종류별로 적용 게이트를 갈라 적는다.

```text
- [ ] DG-04': 생성한 계약 파일이 Step 6.5 게이트를 위반 0 건으로 통과하고,
      사이드카는 §Amendment 사이드카 엔트리 포맷(대상 조건 · 변경 · 근거 · 앵커)을 만족한다
      [exact, enumerated]
```

## 재발 방지

같은 계열 실패가 이 세션에서 **3 회** 났다 (`bambu-kit-enum-allowlist-gate` `AR-03` ·
`harness-core-defects` `AR-03` · 이 계약 `AR-01`). 전부 diff-scope 오라클이다.
`harness-core-defects` 사이드카의 적용 권고에 이어, 다음 계약부터는 변경 범위 조건을
**"diff 결과가 N 개"** 가 아니라 **"내가 만진 파일을 열거하고 그 각각이 diff 에 있다"** 로 쓴다.
