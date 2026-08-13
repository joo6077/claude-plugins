# Sprint Amendments — kaizen-phase7-write-path-integrity

계약 본문(`.harness/sprint-contract-kaizen-phase7-write-path-integrity.md`)은 봉인 후 **한 글자도
고치지 않았다** (`verify_seal` → `SEAL_OK`). 아래는 자기 검증 중 발견한 **측정문 결함**과 계약 밖
추가 산출물의 기록이다.

두 amendment 모두 `direction: relaxing` 이다 — 원 측정문은 **어떤 구현으로도 만족할 수 없어**
PASS 집합이 공집합이었고, 교정하면 PASS 집합이 늘어난다. contract-schema §Amendment 사이드카 의
`direction × consent` 표에 따라 **`relaxing · unanchored` 는 PASS 근거로 쓸 수 없다.** 따라서
AR-03 · AP-03 은 "amendment 로 통과시킨 조건" 이 아니라 **조건 결함으로 표면화**하며, 판정은
평가자에게 넘긴다. 실질 의도가 충족되었다는 증거는 각 항목의 "교정 측정 결과" 에 함께 남긴다.

---

## AM-01 — relaxing

- 대상 조건: AR-03 (두 번째 측정 절)
- 원 측정문: `grep -oE '^[0-9]+\. \*\*' backend-kit/agents/backend-reviewer.md | grep -oE '^[0-9]+'`
  출력이 `seq 1 11` 과 일치
- 결함: 이 정규식은 **파일 전체**를 훑으므로 `§Canonical Unverified-Evidence Protocol` 의 5 개
  번호 항목(`1. **마커는 …`, `2. **`[미검증]` …` …)도 함께 잡는다. 그 블록은
  `harness/docs/guides/qa-evaluation-guide.md` 정본을 **문구 변형 없이 복제**해야 하는 텍스트라
  번호 형식을 바꿀 수 없다. 즉 원 측정문은 정본 복제 의무와 **양립 불가능**하며 PASS 집합이
  공집합이다.
- 변경 (교정 측정문): 범위를 `## 핵심 규칙` 섹션 안으로 한정한다 —
  `awk '/^## 핵심 규칙/{f=1;next} f && /^## /{exit} f' <파일> | grep -oE '^[0-9]+\. ' | tr -d '. '`
  출력이 `seq 1 11` 과 일치
- 교정 측정 결과: `1 2 3 4 5 6 7 8 9 10 11` — 일치. 같은 조건의 나머지 두 측정 절
  (`grep -cE '^## [0-9]+\. ' → 0` · `grep -c '§8 ' → 0`)은 **원문 그대로 충족**했다.
  즉 조건의 의도("핵심 규칙 번호와 섹션 헤더 번호의 충돌이 0")는 성립한다.
- 근거 (redaction 거친 원문): 없음 — 사용자 발언이 아니라 자기 검증 중 발견한 오라클 결함이다
- 앵커: `unanchored` (사용자 합의 없음. 지어내지 않는다)

## AM-02 — relaxing

- 대상 조건: AP-03 (두 번째 측정 절)
- 원 측정문: 변경된 `docs/backend/*.md` 에서 `^``` *$` 합계 `0`
- 결함: CommonMark 에서 **닫는 fence 는 info string 을 가질 수 없다** — 즉 언어 힌트 없는
  bare fence 로 나타나는 것이 정상이다. 이 정규식은 여는 fence 와 닫는 fence 를 구분하지 못하므로
  **코드 블록이 하나라도 있는 문서는 무조건 FAIL** 한다. 실제로 이번 변경과 무관한
  `docs/backend/fundamentals/database.md:42-45` 의 기존 ```` ```sql ```` 블록이 1 건으로 잡혔다.
  PASS 집합이 사실상 공집합이다.
- 변경 (교정 측정문): fence 를 순서대로 훑어 **여는 fence** 만 판정한다 (parity 계산) —
  여는 fence 중 언어 힌트가 없는 것의 개수가 `0`
- 교정 측정 결과: 변경된 4 개 `docs/backend/*.md` + 신규 프로토콜 파일 합계 **0**.
  같은 조건의 첫 측정 절(`python3 scripts/validate-plugin.py backend-kit` V6 `0 bare`)은
  **원문 그대로 충족**했다 — validate-plugin V6 는 처음부터 parity 를 올바로 계산한다.
- 근거 (redaction 거친 원문): 없음 — 자기 검증 중 발견한 오라클 결함
- 앵커: `unanchored`

---

## 계약 밖 추가 산출물 (amendment 아님 — 조건을 바꾸지 않는다)

### AX-01 — `backend-reviewer` Canonical 블록 정본 재동기화

계약 작성 시점에 포착하지 못한 **사실 오류**를 구현 중 발견해 함께 고쳤다. 조건을 추가하거나
완화하지 않으므로 amendment 가 아니라 기록이다.

- 발견: `backend-kit/agents/backend-reviewer.md` §Canonical Unverified-Evidence Protocol 이
  "정본을 **문구 변형 없이 복제**한 것" 이라고 선언하는데, 이번 사이클 Phase 3 이 정본을 v5.0 으로
  개정(미검증 카운터를 `UNVERIFIED_ENV` / `UNVERIFIED_INVALID_EVIDENCE` 로 분리 · 임계값 2 를
  후자에만 적용 · `env_gaps` 커버리지 게이트 · 남용 방지 4 요건)한 뒤에도 사본은 v4.0 의
  **3 분기 · 단일 임계** 서술로 남아 있었다. 즉 그 선언 문장 자체가 거짓이었다.
- 근거: `grep -rln 'UNVERIFIED_ENV' --include='*-reviewer.md' .` → 이번 사이클에 Phase 를 마친
  `infra-kit/agents/infra-reviewer.md` **1 건뿐**. 정본이 "각 kit 의 카이젠 Phase 가 해소할 것"
  으로 명시한 drift 다.
- 조치: 조항 2·3 을 현행 정본으로 교체(문자 단위 일치 확인) + 남용 방지 4 요건 복제 +
  backend-kit 적용 메모를 4 분기 매핑으로 재작성 + 출력 포맷의 미검증 집계를 두 카운터로 분리 +
  `backend-audit` Gotcha 11 · Step 4 판정 규칙을 같은 의미로 정렬(`BLOCKED` 추가).
- 검증: 정본과 사본의 조항 1~3 블록을 문자열 비교 → **일치**.
