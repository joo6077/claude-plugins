# Sprint Amendments — kaizen-phase7-write-path-integrity

계약 본문(`.harness/sprint-contract-kaizen-phase7-write-path-integrity.md`)은 봉인 후 **한 글자도
고치지 않았다** (`verify_seal` → `SEAL_OK`). 이 파일은 자기 검증 중 발견한 **측정문 결함** 주장과
계약 밖 추가 산출물의 기록이다.

## 갱신 2026-08-13 (QA REJECT 후속) — AM-01 · AM-02 **둘 다 철회**

QA 가 AR-03 · AP-03 두 조건을 blocking 으로 REJECT 했다. 두 amendment 는 **전제가 틀렸으므로
철회한다.** 원 주장은 "원 측정문을 만족하는 구현이 존재하지 않는다(PASS 집합 공집합)" 였는데,
실제로는 **양쪽 모두 만족하는 구현이 존재했다.** 계약을 고치는 대신 구현을 고쳤고, 두 조건의 원
측정문을 문자 그대로 실행해 통과를 확인했다 (zsh · bash 동일 출력).

계약 본문은 이번에도 수정하지 않았다. 아래 두 엔트리는 삭제하지 않고 **철회 상태로 보존**한다 —
"오라클이 결함" 이라는 판단이 어디서 틀렸는지가 다음 사이클의 입력이기 때문이다.

---

## AM-01 — ~~relaxing~~ **철회 (WITHDRAWN 2026-08-13)**

- 대상 조건: AR-03 (두 번째 측정 절)
- 원 측정문: `grep -oE '^[0-9]+\. \*\*' backend-kit/agents/backend-reviewer.md | grep -oE '^[0-9]+'`
  출력이 `seq 1 11` 과 일치
- 원 주장(철회됨): 이 정규식이 파일 전체를 훑어 §Canonical Unverified-Evidence Protocol 의 번호
  항목까지 잡는데, 그 블록은 정본을 문구 변형 없이 복제해야 하므로 번호 형식을 바꿀 수 없다 →
  "정본 복제 의무와 양립 불가능, PASS 집합 공집합".
- **왜 틀렸나:** 번호 형식을 바꾸지 않고도 두 요구를 동시에 만족할 수 있다. 정본에서 옮겨온
  블록을 **인용(blockquote)** 으로 감싸면 `> 1. **…` 가 되어 `^` 앵커에 걸리지 않는다. 본문
  문자열은 그대로다 — 정본 복제 의무는 훼손되지 않는다. "번호를 바꾸거나 오라클을 고치거나"
  둘뿐이라고 본 것이 오판이었다 (컨테이너 레벨 표현을 후보에서 빠뜨렸다).
- **조치 (구현 변경):** `backend-kit/agents/backend-reviewer.md` 의 정본 복제 두 블록(조항 1~5 ·
  남용 방지 4 요건)의 각 줄을 인용 표식 `>` 로 시작하게 바꾸고, 그 규약과 이유("최상위 번호
  목록을 §핵심 규칙 하나로 유지")를 같은 절 서두에 명시했다. 재동기화 시에도 표식을 유지하도록
  지시문을 남겼다.
- **원 측정문 재실행 (문자 그대로):**
  `grep -oE '^[0-9]+\. \*\*' backend-kit/agents/backend-reviewer.md | grep -oE '^[0-9]+'`
  → `1 2 3 4 5 6 7 8 9 10 11` · `diff <(...) <(seq 1 11)` → 차이 0.
  같은 조건의 나머지 두 절도 그대로 충족: `grep -cE '^## [0-9]+\. '` → `0` · `grep -c '§8 '` → `0`.
- **정본 복제 무결성 재확인:** 인용 표식을 떼면 조항 1~5 는 정본과 **문자 단위로 일치**한다 —
  `awk '/^> 1\. \*\*마커는/{f=1} f{print} f && /를 남긴다\.$/{exit}' <사본> | sed 's/^> \{0,1\}//' | diff - <(sed -n '1015,1037p' harness/docs/guides/qa-evaluation-guide.md)`
  → 차이 0.

## AM-02 — ~~relaxing~~ **철회 (WITHDRAWN 2026-08-13)**

- 대상 조건: AP-03 (두 번째 측정 절)
- 원 측정문: 변경된 `docs/backend/*.md` 에서 `^``` *$` 합계 `0`
- 원 주장(철회됨): CommonMark 에서 닫는 fence 는 info string 을 가질 수 없으므로 코드 블록이
  하나라도 있는 문서는 무조건 FAIL → "PASS 집합이 사실상 공집합".
- **왜 틀렸나:** "코드 블록 = 백틱 fence" 라고 암묵 가정한 것이 오판이다. CommonMark 는 물결표
  fence(`~~~lang` / `~~~`)를 동등하게 허용하며, 이때 **여는 쪽 언어 힌트는 유지되고 닫는 줄은
  백틱이 아니다.** 즉 언어 힌트를 잃지 않고도 `^``` *$` 를 0 으로 만들 수 있다.
- **조치 (구현 변경):** `docs/backend/fundamentals/database.md` 의 `EXPLAIN ANALYZE` 예제를
  물결표 fence 로 바꾸고(`~~~sql`), 왜 이 파일이 물결표를 쓰는지와 되돌리지 말라는 이유를 HTML
  주석으로 남겼다 (렌더 결과·언어 힌트는 동일).
- **원 측정문 재실행 (문자 그대로):** 변경된 4 개 `docs/backend/*.md`
  (`fundamentals/database.md` · `fundamentals/testing.md` · `patterns/event-driven.md` ·
  `research-log.md`) 각각 `grep -cE '^``` *$'` → `0 0 0 0`, 합계 **0**.
  첫 측정 절(`python3 scripts/validate-plugin.py backend-kit` V6)도 그대로 `0 bare — OK`.

---

## 전 표면 훑기 (한 곳만 고치지 않았다는 증명)

같은 결함이 다른 표면에 남아 있는지 열거로 확인했다. 열거값은 타이핑하지 않고 명령으로 계산했다.

### 1. AR-03 유형 — 최상위 번호 목록 충돌

`backend-kit/agents/backend-reviewer.md` 안의 `^[0-9]+\. \*\*` 매치는 **세 블록**이었다
(§핵심 규칙 11 · 정본 조항 5 · 남용 방지 4 요건 4 = 20 행). 조항 5 만 고치면 4 요건 4 행이 그대로
남아 같은 위반이 재발하므로 **두 블록 모두** 인용 처리했다. Phase 7 Scope 안의 다른 파일
(`backend-kit/skills/*/SKILL.md` · `backend-kit/references/` · `docs/backend/`)에는 이 조건이
걸리지 않으며, 정본을 복제한 다른 킷의 `*-reviewer.md` 는 AR-01 의 10 경로 화이트리스트 밖이라
손대지 않았다 (각 킷 카이젠 Phase 소관 — 정본 §2026-08-13 개정 전파 지시와 동일한 분담).

### 2. AP-03 유형 — bare fence 줄

변경 10 경로의 `^``` *$` 실측: `backend-reviewer.md` 1 · `write-path-integrity-protocol.md` 2 ·
`backend-test/SKILL.md` 4 · `docs/backend/fundamentals/database.md` 1 · 나머지 6 파일 0.

`docs/backend/` 쪽 1 건만 고쳤다. backend-kit 쪽 7 건은 **의도적으로 백틱을 유지**한다:

- AP-03 이 그 파일들에 적용하는 측정은 첫 절(V6)이고, V6 는 **여는 fence 만** 보는 parity
  구현이라 (`scripts/validate-plugin.py:521-536`) 닫는 줄을 위반으로 세지 않는다 — 결함이 아니다.
- 게다가 같은 스크립트의 V3(cross-reference)는 `_body_without_code_blocks`
  (`scripts/validate-plugin.py:306-321`)로 **백틱 블록만** 걸러낸다. backend-kit 문서를 물결표로
  바꾸면 블록 안의 상대경로·grep 패턴이 링크로 오인되어 V3 가 false FAIL 을 낸다. 즉 킷 문서에서
  물결표 전환은 개선이 아니라 회귀다.

`docs/backend/` 의 나머지 bare fence(총 16 행 · `api-design.md` · `auth.md` · `error-handling.md`)
는 이번 변경 대상이 아니고, 건드리면 AR-01(10 경로 정확 일치)을 깨뜨리므로 손대지 않았다.

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

### AX-02 — 정본 복제 블록의 인용 표기 규약 (2026-08-13 REJECT 후속)

AM-01 조치의 부수 기록이다. 사본 블록의 **문구는 바꾸지 않고** 컨테이너만 인용으로 감쌌으며,
같은 절 서두에 규약·이유·재동기화 지시를 남겼다. 두 가지를 동시에 보장하기 위해서다 —
① 이 블록이 편집 대상이 아니라 정본의 사본이라는 표시, ② 이 파일의 최상위 번호 목록을
§핵심 규칙 하나로 유지(규칙 번호와 인용 번호의 충돌 방지). 4 요건 블록은 정본과 문자 단위로
일치하지 않는다 — 문장 구조는 유지한 채 어휘만 이 킷 도메인으로 치환한 복제이며
(`계약` → `기준`/`rule`), 요건 수·순서·판정 효과는 정본 그대로다. 그 사실을 사본 서두에 명시해
"문자 단위 일치" 주장이 조항 1~5 에만 걸리도록 범위를 좁혔다.
