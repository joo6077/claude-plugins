# Sprint Amendments — kaizen-phase3-unverified-triage

> 경로 규약: `harness/references/contract-schema.md` §Amendment 사이드카 (SSOT).
> 계약 본문(`.harness/sprint-contract-kaizen-phase3-unverified-triage.md`)은 write-once 이며
> 이 사이드카는 **원 조건을 삭제·수정하지 않는다.** 아래 항목은 전부 **계약 결함 신고**이지
> 사용자와 합의한 조건 변경이 아니다.

**읽는 평가자에게 — 이 파일의 어떤 항목도 PASS 근거가 아니다.**
두 항목 모두 `consent: unanchored` 이고 `direction` 계산값이 `relaxing` 이므로,
contract-schema §Amendment 사이드카 2×2 표에 따라 **PASS 근거 불가 — 표면화** 다.
해당 조건은 원 조건 문자 그대로 판정하고, 그 결과를 사용자 확인 대상으로 올려라.

---

## D-01 — relaxing (계약 결함 신고 · PASS 근거 아님)

- **대상 조건**: AR-02
- **결함**: AR-02 의 측정문이 `contract-design-guide.md frontmatter 의 version` 을 비교 원본으로
  지정한다. **그 파일에는 YAML frontmatter 가 없다.** 파일 생성 이래 한 번도 존재한 적이 없다.
- **실측 (명령과 출력)**:

  ```bash
  # 1) 현재 판 — frontmatter version 추출 결과가 빈 값
  awk '/^---$/{n++; next} n==1 && /^version:/{sub(/^version:[[:space:]]*/,""); print; exit}' \
    harness/docs/guides/contract-design-guide.md
  # → (출력 없음)

  # 2) 전체 히스토리 — 이 파일을 건드린 모든 커밋에서 1 행이 언제나 '# Contract Design Guide'
  for c in $(git log --all --follow --format=%h -- harness/docs/guides/contract-design-guide.md); do
    p=$(git show --name-only --format= "$c" | grep 'contract-design-guide.md' | head -1)
    git show "$c:$p" | sed -n '1p'
  done | sort -u
  # → # Contract Design Guide      (13 커밋 전부 동일 · '---' 로 시작한 판 0 건)
  ```

- **귀결**: AR-02 는 "네 값을 명령으로 추출해 문자열 비교" 를 요구하는데 이 파일에 대해서는
  추출이 원천적으로 불가능하다. 원 조건 문자 그대로 읽으면 **어떤 구현도 AR-02 를 PASS 시킬 수
  없다** (PASS 집합 = ∅). 값 자체(`v5.0`)는 틀리지 않았다 — 틀린 것은 값이 아니라 **원본 지정**이다.
- **실제 원본**: 같은 파일 §버전 정보 표의 `Guide version` 행.
  `grep -m1 '^| Guide version |' harness/docs/guides/contract-design-guide.md`
  → `| Guide version | 2026-08-13 (Phase 2 kaizen · v5.0) | 이 문서 |` → `v5.0` (Parity 표기와 일치)
- **이번 스프린트가 한 일 (scope 안)**: `qa-evaluation-guide.md` §버전 정보 의 Parity 항목에
  **세 값 각각의 추출 명령과 원본**을 명시했고, `contract-design-guide.md` 에 frontmatter 가 없다는
  사실과 대체 원본을 그 자리에 박았다. 값을 손으로 옮겨 적는 경로는 여전히 차단된다.
- **하지 않은 일과 그 이유**: `contract-design-guide.md` 에 최소 frontmatter(`title`/`version`)를
  추가하는 것이 근본 해소책이지만, 계약 §범위 경계가 수정 허용 경로를 2 개(+계약 파일)로 못박고
  AR-01 이 그 집합을 enumerated 로 검증한다. **사용자 승인 없는 scope 확장은 하지 않는다.**
- **direction 판정 근거**: 원 측정문의 PASS 집합은 ∅ 이고, 원본을 실재 필드로 고치면 PASS 집합이
  비지 않게 된다 → `relaxing`. 완화가 아니라 **실행 불가 조건의 실행 가능화**지만, 자기신고로
  `narrowing` 이라 적을 여지를 만들지 않기 위해 계산 정의(PASS 집합 증감) 그대로 적는다.
- **consent**: `unanchored` — 사용자 발언 인용도 prompt-log 앵커도 없다. 이 항목은 평가자·구현자
  측 결함 신고이지 사용자 재승인이 아니다. **지어낸 앵커를 붙이지 않는다.**
- **앵커**: 없음 (`unanchored`)
- **후속 소관**: contract-design-guide.md frontmatter 신설 여부는 사용자 결정 사항이며,
  결정되면 Phase 4(harness) 또는 contract-kaizen 소관이다. 결정 전까지 AR-02 계열 조건을 쓸 때는
  원본을 `frontmatter version` 이 아니라 `§버전 정보 표 Guide version 행` 으로 적어야 한다.

---

## D-02 — relaxing (계약 결함 신고 · PASS 근거 아님)

- **대상 조건**: AR-01
- **결함**: AR-01 이 스프린트 경로 집합을 3 개로 enumerated 고정하는데, 그 목록에
  **amendment 사이드카(이 파일)가 빠져 있다.** contract-schema §산출물 3 종은 계약 ·
  amendment 사이드카 · 피드백을 스프린트 산출물로 규정하므로, 계약 결함이 발견되는 순간
  준수 경로(사이드카 기록)를 밟으면 AR-01 의 열거 집합을 반드시 벗어난다.
- **추가 사실**: AR-01 의 Given 은 "커밋 직전 working tree" 인데, iteration 2 에서는 계약 파일이
  write-once 라 **수정되지 않는다**. 따라서 iter-2 working tree 에는 계약 파일이 애초에 등장할 수
  없고, 원 측정문(3 경로 집합 정확 일치)은 사이드카 유무와 무관하게 iter-2 에서 성립하지 않는다.
  AR-01 은 사실상 **스프린트 누적 변경 집합**으로 읽어야 하는 조건이다 (iter-1 QA 도 working tree 가
  아니라 `git show --name-only c3f9595` 로 판정했다).
- **direction (자기신고 아님 — SSOT `amend_direction` 실행값)**:

  ```bash
  # 원 집합 3 행 vs 개정 집합 4 행, contract-schema §Amendment 사이드카 의 amend_direction 그대로
  amend_direction ar01_orig.txt ar01_rev.txt
  # → relaxing added=1 removed=0     (zsh · bash 동일 출력)
  ```

- **consent**: `unanchored` — 사용자 앵커 없음.
- **앵커**: 없음 (`unanchored`)
- **귀결**: 2×2 표에 따라 PASS 근거 불가. AR-01 은 원 조건 문자 그대로 판정하고, 실제 변경 집합
  (구현 2 경로 + 계약 1 + 사이드카 1)을 그대로 표면화한다. 구현 측 경로는 여전히 허용 2 경로를
  벗어나지 않았다 — 늘어난 1 건은 harness 자신의 기록 산출물이다.
- **후속 소관**: 다음 사이클의 AR-01 계열 조건은 열거 집합에 사이드카·피드백 산출물을 포함하거나,
  "구현 변경 경로" 와 "harness 산출물 경로" 를 분리해 세야 한다 (contract-kaizen 소관).
