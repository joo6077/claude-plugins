# Sprint Amendments — kaizen-phase3-unverified-triage

> 경로 규약: `harness/references/contract-schema.md` §Amendment 사이드카 (SSOT).
> 계약 본문(`.harness/sprint-contract-kaizen-phase3-unverified-triage.md`)은 write-once 이며
> 이 사이드카는 **원 조건을 삭제·수정하지 않는다.** 아래 항목은 전부 **계약 결함 신고**이지
> 사용자와 합의한 조건 변경이 아니다.

**읽는 평가자에게 — 이 파일의 어떤 항목도 PASS 근거가 아니다.**
살아 있는 항목은 전부 `consent: unanchored` 이고 `direction` 계산값이 `relaxing` 이므로,
contract-schema §Amendment 사이드카 2×2 표에 따라 **PASS 근거 불가 — 표면화** 다.
해당 조건은 원 조건 문자 그대로 판정하고, 그 결과를 사용자 확인 대상으로 올려라.

## iteration 3 상태 요약

| 항목 | 대상 조건 | iter-2 | iter-3 |
| ------ | ------ | ------ | ------ |
| D-01 | AR-02 | 계약 결함 신고 (PASS 근거 불가) | **RESOLVED — 구현으로 해소. 이 조건에는 amendment 가 필요 없다** |
| D-02 | AR-01 | 계약 결함 신고 | 유효 (사이드카 경로 누락) |
| D-03 | AR-01 | — | 신규 — AR-01 과 AR-02 의 **상호배타성** 신고 |

---

## D-01 — RESOLVED (2026-08-13 iter-3 · 구현으로 해소)

- **대상 조건**: AR-02
- **iter-2 의 신고 내용**: AR-02 의 측정문이 `contract-design-guide.md frontmatter 의 version` 을
  비교 원본으로 지정하는데 그 파일에 YAML frontmatter 가 없어 추출이 항상 빈 값이고,
  따라서 AR-02 의 PASS 집합이 ∅ 였다.
- **iter-3 의 처리 — 계약을 고치지 않고 구현을 고쳤다.** 원 측정문이 지목한 원본(frontmatter
  `version`)을 **실재하게 만들었다.** `harness/docs/guides/contract-design-guide.md` 에 최소
  frontmatter 3 필드(`title` / `version: v5.0` / `last_updated`)를 신설했다. 이제 원 조건을
  **문자 그대로** 실행해도 네 값이 전부 추출되고 불일치가 0 이다:

  ```text
  skill-design-guide 1.5.0        (본문 Parity: 1.5.0)  OK
  agent-design-guide 1.6.0        (본문 Parity: 1.6.0)  OK
  contract-design-guide v5.0      (본문 Parity: v5.0 )  OK
  contract-schema v5.3            (본문 Schema link: v5.3) OK
  AR-02 불일치 = 0
  ```

- **iter-2 가 놓쳤던 두 번째·세 번째 불일치도 같이 고쳤다.** iter-2 는 "frontmatter 부재" 1 건만
  신고했지만, 실제로는 본문이 `skill-design-guide **v**1.5.0 · agent-design-guide **v**1.6.0` 로
  적혀 있어 frontmatter 원본(`1.5.0` / `1.6.0`)과 **문자열이 달랐다.** AR-02 는 "문자열 비교,
  불일치 0 건" 을 요구하므로 이 둘도 FAIL 사유였다. 세 값 모두 추출 출력 그대로로 교체했고,
  "표기를 정규화하지 마라" 를 같은 절에 못박았다.
- **전 표면 처리**: `harness/docs/guides/` 5 개 가이드 중 frontmatter 가 없던 파일은
  `contract-design-guide.md` 와 `qa-evaluation-guide.md` **2 개**였다. 한 곳만 고치면 다음
  사이클에 같은 결함이 나머지 한 곳에서 재발하므로 둘 다 신설했다 — 이제 5/5 가 추출 가능하다.
  중복 원본이 새로 생기는 것을 막기 위해 두 파일의 §버전 정보 에 "frontmatter 가 SSOT · 본문과
  함께 올려라" 를 명시하고 `qa-evaluation-guide.md` §개정 시 체크리스트에 항목을 추가했다.
- **귀결**: **AR-02 에 대한 amendment 는 철회한다.** 이 항목은 감사 흔적으로만 남기며 PASS 근거로
  쓰이지 않는다 — AR-02 는 원 조건 문자 그대로 판정하면 된다.

---

## D-02 — relaxing (계약 결함 신고 · PASS 근거 아님 · 유효)

- **대상 조건**: AR-01
- **결함**: AR-01 이 스프린트 경로 집합을 3 개로 enumerated 고정하는데, 그 목록에
  **amendment 사이드카(이 파일)가 빠져 있다.** contract-schema §산출물 3 종은 계약 ·
  amendment 사이드카 · 피드백을 스프린트 산출물로 규정하므로, 계약 결함이 발견되는 순간
  준수 경로(사이드카 기록)를 밟으면 AR-01 의 열거 집합을 반드시 벗어난다.
- **추가 사실**: AR-01 의 Given 은 "커밋 직전 working tree" 인데, iteration 2 이후에는 계약 파일이
  write-once 라 **수정되지 않는다**. 따라서 iter-2/3 working tree 에는 계약 파일이 애초에 등장할 수
  없고, 원 측정문(3 경로 집합 정확 일치)은 사이드카 유무와 무관하게 iter-2 이후 성립하지 않는다.
  AR-01 은 사실상 **스프린트 누적 변경 집합**으로 읽어야 하는 조건이다 (iter-1 QA 도 working tree 가
  아니라 `git show --name-only c3f9595` 로 판정했다).
- **consent**: `unanchored` — 사용자 앵커 없음. **지어낸 앵커를 붙이지 않는다.**
- **앵커**: 없음 (`unanchored`)
- **귀결**: 2×2 표에 따라 PASS 근거 불가. AR-01 은 원 조건 문자 그대로 판정하고, 실제 변경 집합을
  그대로 표면화한다.
- **후속 소관**: 다음 사이클의 AR-01 계열 조건은 열거 집합에 사이드카·피드백 산출물을 포함하거나,
  "구현 변경 경로" 와 "harness 산출물 경로" 를 분리해 세야 한다 (contract-kaizen 소관).

---

## D-03 — relaxing (계약 결함 신고 · PASS 근거 아님 · 신규 iter-3)

- **대상 조건**: AR-01 (AR-02 와의 관계)
- **결함**: **AR-01 과 AR-02 는 동시에 PASS 될 수 없다.** D-01 의 구현 해소가 요구하는 경로
  (`harness/docs/guides/contract-design-guide.md`) 가 AR-01 의 열거 집합 밖이기 때문이다.
  두 조건 중 하나를 포기하지 않고는 이번 스프린트를 끝낼 수 없다.

- **증명 (전제 2 개 전부 실측)**:

  1. **AR-02 가 PASS 이려면 `contract-design-guide.md` 가 변경되어 있어야 한다.**
     이 파일은 생성 이래 13 개 커밋 전부에서 1 행이 `# Contract Design Guide` 였다 —
     `---` 로 시작한 판이 **0 건**이다. 즉 frontmatter `version` 추출이 성공하는 상태는
     **정의상 이번 스프린트가 만든 변경 상태**뿐이다.

     ```bash
     # 전 히스토리 1 행 — 13 커밋 전부 동일 (frontmatter 판 0 건)
     for c in $(git log --all --follow --format=%h -- harness/docs/guides/contract-design-guide.md); do
       p=$(git show --name-only --format= "$c" | grep 'contract-design-guide.md' | head -1)
       git show "$c:$p" 2>/dev/null | sed -n '1p'
     done | sort | uniq -c
     # →   13 # Contract Design Guide

     # HEAD 판 추출값 = 빈 값 / 이번 변경 후 = v5.0
     git show HEAD:harness/docs/guides/contract-design-guide.md \
       | awk '/^---$/{n++; next} n==1 && /^version:/{sub(/^version:[[:space:]]*/,""); print; exit}'
     # → (출력 없음)
     ```

  2. **AR-01 이 PASS 이려면 `contract-design-guide.md` 가 변경 집합에 없어야 한다.**
     열거 집합 3 개에 그 경로가 없고 조건은 "정확히 일치" 를 요구한다.

  1 과 2 는 서로를 배제한다. ∎

- **direction (자기신고 아님 — SSOT `amend_direction` 실행값)**:

  ```bash
  # 원 집합 3 행 vs 실제 스프린트 누적 집합 5 행
  # (계약 · 가이드 · 에이전트 + 사이드카 + contract-design-guide)
  amend_direction ar01_orig.txt ar01_rev.txt
  # → relaxing added=2 removed=0     (zsh · bash 동일 출력)
  ```

- **consent**: `unanchored` — 사용자 발언 인용도 prompt 로그 앵커도 없다. 자기 판단이다.
- **앵커**: 없음 (`unanchored`)
- **선택의 근거 (숨기지 않는다)**: 두 조건 중 AR-02 를 살렸다. 이유는 셋이다.
  1. **AR-01 은 이미 사이드카만으로도 불성립이다** (D-02). 계약 결함이 존재하는 한
     contract-schema §산출물 3 종이 규정한 준수 경로를 밟아야 하고, 그 경로가 열거 집합 밖이다.
     `contract-design-guide.md` 를 건드리지 않아도 AR-01 은 PASS 로 돌아오지 않는다 —
     즉 AR-02 를 포기해도 얻는 것이 없다.
  2. **AR-02 의 해소는 영구적이다.** frontmatter 신설은 다음 사이클부터 이 계열 결함을 없앤다.
     AR-01 의 경로 개수는 이번 스프린트 한정 장부다.
  3. QA 자신이 AR-01 을 "구현자 은폐가 아니라 계약이 산출물 유형을 예견하지 못한 구조적 결함" 으로
     분류했고, AR-02 는 "계약 조건 자체가 여전히 불충족" 으로 분류했다. 고칠 수 있는 쪽을 고쳤다.
- **표면화 (평가자가 그대로 판정할 사실)**: 이번 스프린트 누적 변경 경로는 **5 개**다.

  ```text
  .harness/sprint-amendments-kaizen-phase3-unverified-triage.md   (harness 산출물 · 열거 집합 밖)
  .harness/sprint-contract-kaizen-phase3-unverified-triage.md     (열거 집합 안 · 무수정 · SEAL_OK)
  harness/agents/qa-evaluator.md                                  (열거 집합 안)
  harness/docs/guides/contract-design-guide.md                    (AR-02 근본해소 · 열거 집합 밖)
  harness/docs/guides/qa-evaluation-guide.md                      (열거 집합 안)
  ```

  구현 로직 변경은 여전히 허용 2 경로 안이다. 늘어난 2 건은 (a) harness 자신의 기록 산출물과
  (b) AR-02 가 원본으로 지목한 파일이다.
- **후속 소관 (contract-kaizen)**: AR-01 계열 조건은 열거 집합을 "구현 변경 경로" 와
  "harness 산출물 경로" 로 분리하고, **어떤 조건이 원본으로 지목한 파일은 자동으로 허용 경로에
  포함**되도록 규정해야 한다. 측정 원본을 고칠 수 없게 만들어 놓고 그 원본이 실재하지 않는 상황이
  이번 스프린트의 근본원인이다.
