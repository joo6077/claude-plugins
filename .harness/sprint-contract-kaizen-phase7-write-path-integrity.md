---
feature: "카이젠 Phase 7 — backend-kit 쓰기 경로 무결성 SSOT (경합 invariant 분류 H1 · upsert arbiter H2 · 통합 타깃 증명+음성 대조 H3 · 멱등 계약 6 항목) + outbox/Stripe 사실 정정 2 종"
created: "2026-08-13 16:10"
complexity: "복잡"
conditions: 26
slug: kaizen-phase7-write-path-integrity
status: done
owner_session: df1b3e15-30b3-4825-a3c4-4ac44c686e94
conditions_digest: sha256:574230c5bfad3499
locked_at: "2026-08-13 16:10"
---

## 배경

`.harness/.meta/evidence/phase7.md` 가 이번 Phase 의 **유일한 외부 근거**다. 외부 조회 0 회
(네트워크 도구 미사용). 그 파일에 없는 URL·수치·버전 번호는 쓰지 않는다.

evidence 가 지적한 것은 세 축(H1/H2/H3) + 멱등 계약이고, 넷 다 backend-kit 에 **대응 조항이
0 건**이다 (아래 GAP 표의 사전 측정 출력 참조). 즉 이번 건은 "재발한 규칙의 등급 상향" 이 아니라
**신설**이다.

**직전 사이클 흡수분과의 관계.** `.claude/kaizen-input/insights-report.md` 의 중복 금지 표에 있는
7 항목(Counterpart Enumeration · 빈 상태 상태코드 · timestamp 타임존 · mock-only 통합테스트 주장
차단 등)은 이번에 **한 문장도 다시 추가하지 않는다.** 신규 델타 **D4**(read-check-then-write
경합의 SQL 술어 해소, Phase 7/9 직접 신호)만 대상이다.

**단, H3 은 인접 항목이 있어 근본원인을 규명해야 한다.** 직전 사이클이 넣은
`backend-test` Gotcha 13 / `audit-criteria` §9 "통합 테스트 실체 확인" 은 *의존성이 진짜인가*
(Testcontainers/실 DB 인가)를 재는 오라클이다. 2026-08-12 실측 `ER-02` 는 **그 검사를 통과했다** —
실 DB 를 썼기 때문이다. 그런데도 실패했다:

> *"신규 통합 테스트가 실제 바이너리를 호출하지 않고 독립적으로 재작성한 SQL 로 낙관적 동시성의
> 일반 동작만 검증한다. **mutation test 로 확정 — 실제 코드에서 동시성 가드
> (`WHERE exercises = $3::jsonb`)를 완전히 삭제해도 이 테스트는 여전히 통과한다.**"*

근본원인은 **오라클의 축이 하나뿐이었다는 것**이다 — "의존성이 진짜인가" 는 봤지만 "대상이
진짜인가"(테스트가 구현 심볼을 실제로 경유하는가) 는 아무도 재지 않았다. 그래서 같은 취지의
문장을 또 쓰지 않고 **다른 축의 검사를 신설**하며, 그 축은 grep 으로 결정론적 판정이 가능하므로
시작 등급을 **E3**(§5a 결합 확인)로 잡는다 (`skill-design-guide.md` §3.7 "기계 판정이 가능하고
위반 비용이 큰 규칙" 시작 등급 기준).

**Phase 3 정본 중복 금지.** 이번 사이클 Phase 3 이 `qa-evaluation-guide.md` 에
§Discriminating Evidence Gate 를 신설했다(적용 범위 9 항 · 절차 3 단계 · 안전 조건 · 비용 통제).
그것은 **평가자 측 판정 절차**이고, 본 Phase 는 **생산 측 의무**(무엇을 만들고 무엇을 테스트할지)
만 정의한다. 판정 절차·안전 조건·임계값은 **인용만** 하고 재정의하지 않는다 (SK-05 로 측정).

## 리서치 소스 (evidence 파일 한정 — 외부 조회 0 회)

- `.harness/.meta/evidence/phase7.md` §1~§4 — 관찰 사실 H1/H2/H3 · 권장안 7 항 ·
  **넣지 말 것** 6 항 · 트레이드오프 · 열린 질문 4 항. 인용 URL 11 종:
  `postgresql.org/docs/current/transaction-iso.html` · `explicit-locking.html` ·
  `indexes-partial.html` · `sql-insert.html` ·
  `sigmodrecord.org` (Berenson et al.) ·
  `datatracker.ietf.org/doc/draft-ietf-httpapi-idempotency-key-header/` ·
  `docs.stripe.com/api/idempotent_requests` · `testcontainers.com/getting-started/` ·
  `docs.pact.io/provider` · `docs.pact.io/implementation_guides/cli/pact-verifier` ·
  `pitest.org` · `microservices.io/patterns/data/transactional-outbox.html`
- `.harness/.meta/kaizen-data-pool.md` §1 — REJECT Top 20 의 `ER-02` 2 건 · `LG-03`,
  Improvement Top 15 의 "UPDATE 호출부를 별도 함수로 추출"
- `.claude/kaizen-input/insights-report.md` — 중복 금지 표 · 신규 델타 **D4** · §0 서사의
  FCM partial unique index 충돌 / feed TOCTOU in-SQL `EXISTS` 해소
- Phase 1 산출물 `harness/docs/guides/skill-design-guide.md` §3.7 — Enforcement 3 등급 ·
  시작 등급 선택 기준 · 승급 규칙
- Phase 3 산출물 `harness/docs/guides/qa-evaluation-guide.md` §Discriminating Evidence Gate ·
  §Canonical Unverified-Evidence Protocol — 인용 전용
- Phase 2 산출물 `harness/references/contract-schema.md` v5.3 — 본 계약 포맷 SSOT ·
  §음성 대조 · §측정 커버리지 표기(화이트리스트 규칙)

## GAP 분석 (전부 실측 · 사전 측정 명령 출력 기준)

측정 범위는 `backend-kit/` + `docs/backend/` 전체다.

| # | 갭 | 실측 근거 (사전 측정) | 처리 |
| --- | --- | --- | --- |
| H1 | 경합 가드 조항 부재 | `grep -rniE "TOCTOU\|read-check-then-write\|낙관적 동시성\|조건부 UPDATE\|WHERE EXISTS\|compare-and-swap\|경합" backend-kit docs/backend \| wc -l` → **0** | `references/write-path-integrity-protocol.md` §1~§2 신설 + 5 표면 인용 |
| H1b | 격리 수준 어휘 자체가 없음 | `grep -rniE "격리 수준\|격리수준\|isolation level\|serializable\|write skew\|phantom" backend-kit docs/backend \| wc -l` → **0** | 프로토콜 §2 + `docs/backend/fundamentals/database.md` 원칙 8 |
| H2 | upsert arbiter 정합 조항 부재 | `grep -rniE "ON CONFLICT\|partial unique\|arbiter" backend-kit docs/backend \| wc -l` → **0** (`upsert` 2 건은 PATCH 의미론·헤더 대안 문맥) | 프로토콜 §3 (스택 무관 본문 + **PostgreSQL 감지 시** annex) + database.md 원칙 9 |
| H3 | 통합 "타깃" 증명 부재 | `grep -rniE "실제 바이너리\|프로덕션 코드 경로\|독립 재작성\|결합: " backend-kit docs/backend \| wc -l` → **0** | 프로토콜 §5a (E3) + backend-test Gotcha 16 + testing.md 원칙 8 |
| H3b | 핵심 guard 음성 대조 부재 | `grep -rniE "음성 대조\|negative control\|판별력" backend-kit docs/backend \| wc -l` → **0** | 프로토콜 §5b (정본 인용) + backend-test Gotcha 17 |
| H4 | 멱등 계약이 상태코드에서 멈춤 | `audit-criteria` §2 에 replay/409/422/400 은 있으나 킷 전체에서 `payload fingerprint` **0** · `key 범위` **0** · 계약용 `expiry` **0** | 프로토콜 §4 6 항목 (상태코드는 재정의하지 않고 audit-criteria §2 를 SSOT 로 인용) |
| F1 | outbox 전달 보장 오기 | `grep -rn "exactly-once 보장" docs/backend` → **1 건** (`research-log.md:151`). 같은 킷 `event-driven.md` 원칙 4 와 자기모순 | 정정 + `[정정 2026-08-13]` 주석 |
| F2 | Stripe 멱등 서술 불완전 | `event-driven.md:47` 이 payload 비교·만료 시맨틱 누락, "24 시간 동안 같은 응답" 으로 오해 유발 | 정정 (결과 저장 + payload 비교 + 24h pruning) |
| P1 | Phase 1 서브에이전트 스펙 거짓 서술 | `grep -rniE "subagent\|서브에이전트\|중첩\|nest\|frontmatter" backend-kit` → 관련 3 행 전부 정상(호출 방법·섹션 제목) · **거짓 서술 0 건** | **정정 불필요** — 확인 완료, 변경 없음 |

## 범위 경계

**구현 변경 경로 10 개.** 목록은 AR-01 의 기대 집합 한 곳에서만 열거한다
(contract-schema §측정 커버리지 표기의 화이트리스트 규칙). 계약 파일 자신과 `.harness/**` 는
AR-01 pathspec 에서 제외한다.

- **건드리지 않는다**: `backend-kit/README.md` · `backend-kit/.claude-plugin/` ·
  `backend-kit/evals/` · 다른 킷 전부 · `.claude/skills/**` · `harness/**`.
- **`backend-kit/skills/*/references/*.md` 는 Phase 7 Scope 밖이다.** Scope 는
  `backend-kit/skills/*/SKILL.md` · `backend-kit/agents/*.md` · `backend-kit/references/` ·
  `docs/backend/` 로 명시돼 있고, 스킬 내부 `references/` 는 그 어느 항목에도 매칭되지 않는다.
  따라서 신규 rule 은 **`backend-kit/references/` 아래 새 SSOT** 에 두고, 두 문서의 rule 집합이
  교집합 0 임을 RE-02 로 증명한다.
  - 그 결과 `backend-kit/skills/backend-audit/references/audit-criteria.md:93` 의
    "Outbox+CDC 조합으로 exactly-once 보장 가능" 은 **이번에 고치지 않는다.** 같은 오류지만 Scope
    밖이다. backend-audit Gotcha 16 으로 **PASS 근거 사용을 무효화**하고 문구 정정은 downstream 으로
    넘긴다 (ER-01 의 측정 범위를 `docs/backend/` 로 한정하는 이유).
- **evidence 에 없는 값을 지어내지 않는다.** URL·수치는 evidence 파일 또는 변경 전 본문에 실재하는
  것만 쓴다 (AP-01 로 기계 대조).
- **넣지 않는다** (evidence 명시 금지 6 종):
  `Serializable` 을 전 write path 기본값으로 강제 · `SELECT FOR UPDATE` 를 모든 TOCTOU 의 해법으로
  제시 · Testcontainers/Pact 를 모든 테스트에 강제 · RFC 9700 을 H1~H3 의 직접 근거로 인용 ·
  만료 draft 를 RFC/표준으로 호칭 · 스택 무관 본문에 PostgreSQL 전용 문법 필수화.
- **전체 저장소 mutation score 임계값을 세우지 않는다** (Phase 3 정본의 금지 조항).

## 회귀 게이트

- 정정 항목(F1·F2)은 "새 서술 추가" 가 아니라 **잔존 0 건 증명**으로 판정한다.
- 모든 grep 오라클은 zsh · bash 양쪽에서 실행하고 출력이 같아야 한다 (DG-04).
- 열거값(rule 수 · 경로 수 · URL 수)은 타이핑하지 않고 명령으로 **계산**한다.
- **substring 오탐 사전 확인 기록:** SK-05 의 초안 오라클
  `grep -nE 'mutation score|임계값은|전체 repo'` 는 §5c 의 **금지 문장**("전체 저장소 mutation
  score 임계값을 세우지 마라")을 1 건 잡았다 — 금지문과 정의문을 구분하지 못했다. 그래서 숫자를
  동반한 **정의형**만 잡도록 `임계값은 [0-9]` / `mutation score *(>=|이상|[0-9])` /
  `미검증\] *[0-9]+ *건` 으로 좁혔고 재실행에서 0 을 얻었다.
- SK-06 은 토큰 개수가 아니라 **구조**로 잰다 — PostgreSQL 전용 토큰의 줄 번호가 annex 헤더와
  다음 `## ` 헤더 사이에 전부 들어가는지 산술 비교한다.

## Skill

- [ ] SK-01: 쓰기 경로 무결성 규칙 본문이 `backend-kit/references/write-path-integrity-protocol.md`
      1 개 파일에만 존재하고, 5 개 소비 표면이 각각 그 경로를 인용한다 [exact, enumerated]
      (측정: `grep -rln 'write-path-integrity-protocol' backend-kit | LC_ALL=C sort` 결과가
      `backend-kit/agents/backend-reviewer.md`,
      `backend-kit/references/write-path-integrity-protocol.md`,
      `backend-kit/skills/backend-audit/SKILL.md`,
      `backend-kit/skills/backend-guide/SKILL.md`,
      `backend-kit/skills/backend-system/SKILL.md`,
      `backend-kit/skills/backend-test/SKILL.md` 6 행과 정확히 일치)
- [ ] SK-02: 그 SSOT 가 경합 invariant **3 유형**과 각 유형의 담당 primitive 를 표로 담는다
      [exact, enumerated]
      (유형 토큰: `같은 row 의 상태 전이` · `존재 · 권한 · 가시성 predicate` ·
      `cross-row · absence · aggregate` — 각 `grep -cF` ≥ 1 ·
      primitive 토큰: `compare-and-swap` · `WHERE EXISTS` · `Serializable` 각 ≥ 1)
- [ ] SK-03: evidence 의 **넣지 말 것** 3 종이 금지 문구로 명시된다 [exact, enumerated]
      (대상: `Serializable` 전 write path 기본값 강제 · `SELECT FOR UPDATE` 를 모든 TOCTOU 의 해법 ·
      `READ COMMITTED` + 복잡한 술어를 "안전" 으로 서술 —
      측정: 세 문장 각각 "하지 마라" 로 끝나는 형태로 `grep -cF` = 1)
- [ ] SK-04: 멱등 쓰기 계약 **6 항목**이 SSOT §4 에 열거되고, HTTP 상태코드를 재정의하지 않는다
      [exact, enumerated]
      (항목: `key 범위` · `payload fingerprint` · `replay response` · `in-flight duplicate` ·
      `different-payload reuse` · `expiry` 각 `grep -cF` ≥ 1 ·
      상태코드 미재정의 측정: `grep -cE '409|422|400' backend-kit/references/write-path-integrity-protocol.md` → `0`)
- [ ] SK-05: 그 SSOT 가 판정 절차·임계값을 **재정의하지 않고 정본을 인용**한다 [exact]
      (측정: `qa-evaluation-guide.md` 인용 ≥ 1 · `contract-schema.md` 인용 ≥ 1 그리고
      `grep -nE '임계값은 [0-9]|mutation score *(>=|이상|[0-9])|미검증\] *[0-9]+ *건' <파일> | wc -l` → `0` ·
      음성 대조: §8 의 정본 인용 표를 지우면 이 조건이 FAIL 해야 한다)
- [ ] SK-06: PostgreSQL 전용 문법 서술이 스택 무관 본문이 아니라 **"PostgreSQL 감지 시" annex 안에만**
      존재한다 [exact]
      (측정: `H` = `^### PostgreSQL 감지 시 추가 rule` 줄 번호, `N` = `H` 다음 `^## ` 줄 번호 ·
      `grep -nE 'ON CONFLICT|partial index' <파일>` 의 줄 번호 중 `H` 미만이거나 `N` 이상인 것의
      개수 → `0`)
- [ ] SK-07: `backend-kit/skills/backend-audit/SKILL.md` Step 3 rule 표에 Database 3 건 ·
      Testing 2 건이 추가되고 표 전체 row 수가 사전값 26 에서 늘어난 값과 계산 일치한다 [exact]
      (측정: `grep -cE '^\| [0-9]+ \| ' <파일>` 출력 = `31` ·
      `grep -cE '^\| [0-9]+ \| Database \| '` = `5` · `grep -cE '^\| [0-9]+ \| Testing \| '` = `5` ·
      번호 열이 1 부터 연속인지 `seq` 와 대조)
- [ ] SK-08: `backend-audit` Step 0 이 **DB 엔진 감지**를 요구하고, PostgreSQL 미확정 시의 처리를
      명시한다 [exact]
      (측정: `grep -c 'DB 엔진도 함께 확정한다' backend-kit/skills/backend-audit/SKILL.md` = `1` +
      같은 문단에 `엔진 미확정` 사유의 `[미검증]` 처리 문구 존재)
- [ ] SK-09: `backend-guide` 에 `write-path-integrity` 카테고리가 Step 1 표에 있고, Step 2 가 그
      카테고리만 principle-index 대신 프로토콜을 읽도록 예외를 둔다 [exact, enumerated]
      (측정: `grep -c '^| write-path-integrity |' backend-kit/skills/backend-guide/SKILL.md` = `1` +
      Step 2 문단에 `principle-index 가 아니라` 문구 1 건)
- [ ] SK-10: `backend-system` Step 2 규격 카테고리 표에 `쓰기 경로 무결성` 행이 있고 산출물 3 종을
      지목한다 [exact, enumerated]
      (산출물: `invariant 분류 3 줄` · `제약↔upsert 대조 표` · `멱등 계약 6 항목` —
      측정: `grep -c '^| 쓰기 경로 무결성 |' <파일>` = `1` + 그 행에 세 토큰 모두 존재)
- [ ] SK-11: `backend-test` Step 4 에 핵심 guard 의 **positive + negative 쌍** 표가 있고,
      전면 강제 금지 문구가 함께 있다 [exact, enumerated]
      (측정: Step 4 에 `| P | positive |` 와 `| N | negative` 2 행 존재 +
      Gotcha 17 에 `모든 테스트에 요구하지 마라` 문구 1 건)
- [ ] SK-12: 4 개 스킬 + 1 에이전트의 References/평가 기준 절에 프로토콜 경로가 등록되고, 스킬
      쪽 상대경로가 실재 파일로 해석된다 [exact, enumerated]
      (측정: 5 파일 각각에서 프로토콜 경로 언급 ≥ 1 · 상대경로
      `../../references/write-path-integrity-protocol.md` 를 각 SKILL.md 디렉토리 기준으로
      `test -f` → 전부 성공)

## Error

- [ ] ER-01: `docs/backend/` 에서 outbox 의 "exactly-once 보장" 잔존이 0 건이다 [exact]
      (측정: `grep -rn 'exactly-once 보장' docs/backend | grep -v '정정 2026-08-13' | wc -l` → `0` ·
      사전 출력 `1` 이 discriminating 근거 ·
      음성 대조: 정정 문장에서 `at-least-once` 토큰을 지우면 이 측정이 FAIL 해야 한다)
- [ ] ER-02: `docs/backend/patterns/event-driven.md` 의 Stripe 멱등 서술이 **payload 비교**와
      **키 보관 기간** 시맨틱을 담는다 [exact, enumerated]
      (토큰: `요청 페이로드를 비교` · `pruning` · `키 보관 기간` 각 `grep -cF` ≥ 1 ·
      이전 오기 잔존 `grep -c '24시간 동안 동일 key에 대해 같은 응답을 반환한다'` → `0`)
- [ ] ER-03: 만료된 Idempotency-Key draft 를 "표준" 또는 "RFC" 로 호칭하는 서술이 변경 범위 전체에서
      0 건이다 [exact]
      (측정: `grep -rnE 'Idempotency-Key[^|]{0,40}(표준|RFC)' backend-kit docs/backend | grep -v '표준\" 으로\|표준.으로 서술\|표준.으로 소개' | wc -l` → `0`)

## Architecture

- [ ] AR-01: 변경이 10 개 경로로 한정된다 [exact, enumerated]
      (Given: 커밋 직전 스테이징 완료 후 ·
      측정: `git diff --cached --name-only -- backend-kit docs ':(exclude).harness'` 결과가
      `backend-kit/agents/backend-reviewer.md`,
      `backend-kit/references/write-path-integrity-protocol.md`,
      `backend-kit/skills/backend-audit/SKILL.md`,
      `backend-kit/skills/backend-guide/SKILL.md`,
      `backend-kit/skills/backend-system/SKILL.md`,
      `backend-kit/skills/backend-test/SKILL.md`,
      `docs/backend/fundamentals/database.md`,
      `docs/backend/fundamentals/testing.md`,
      `docs/backend/patterns/event-driven.md`,
      `docs/backend/research-log.md` 10 행과 정확히 일치)
- [ ] AR-02: `docs/backend/research-log.md` 최상단에 `## [2026-08-13] — Phase 7 kaizen` 라운드가
      추가되고 frontmatter `last_updated` 가 `2026-08-13` 이다 [exact]
      (측정: `grep -n '^## \[2026-08-13\] — Phase 7 kaizen' <파일>` 1 건 +
      `grep -c '^last_updated: 2026-08-13' <파일>` = `1` + 그 라운드에 §사실 정정 표 2 행 존재)
- [ ] AR-03: `backend-kit/agents/backend-reviewer.md` 에서 핵심 규칙 번호와 섹션 헤더 번호의 충돌이
      0 이다 [exact]
      (측정: `grep -cE '^## [0-9]+\. ' <파일>` → `0` · 핵심 규칙 번호는 `1`~`11` 연속 —
      `grep -oE '^[0-9]+\. \*\*' <파일> | grep -oE '^[0-9]+'` 출력이 `seq 1 11` 과 일치 ·
      남아 있던 `§8` 참조 0 건: `grep -c '§8 ' <파일>` → `0`)
- [ ] AR-04: 두 축(실 의존성 / 실 대상)의 구분이 `backend-test` · 프로토콜 · `docs/backend/fundamentals/testing.md`
      3 표면에 동일 개념으로 존재하고, 기존 Gotcha 13 을 대체하지 않고 병렬로 둔다 [exact, enumerated]
      (측정: 3 파일 각각에 "의존성"/"대상" 구분 문구 ≥ 1 +
      `grep -c 'mock-only 테스트를 integration 으로 명명하거나 보고하지 마라' backend-kit/skills/backend-test/SKILL.md` = `1` (기존 조항 보존))

## Anti-patterns

- [ ] AP-01: 이번 커밋이 새로 도입한 `https://` URL 이 전부 evidence 파일 또는 변경 전 본문에
      실재한다 (날조 0 건) [exact]
      (측정: `git diff --cached -U0 -- backend-kit docs` 의 `+` 줄에서 URL 을 추출·정규화해
      `.harness/.meta/evidence/phase7.md` 또는 `HEAD` 의 `backend-kit`/`docs` 트리와 대조 ·
      미대조 건수 → `0` · 추출 URL 총수는 명령으로 계산)
- [ ] AP-03: 변경 파일 전체에 bare code fence(``` 뒤 언어 힌트 없음)가 0 건이다 [exact]
      (측정: `python3 scripts/validate-plugin.py backend-kit` V6 `0 bare` +
      변경된 `docs/backend/*.md` 에서 `^``` *$` 합계 `0`)

## Reusability

- [ ] RE-01: 5 개 소비 표면이 규칙 본문을 재열거하지 않는다 [exact]
      (측정: `grep -rln 'compare-and-swap' backend-kit | LC_ALL=C sort` 결과가
      `backend-kit/references/write-path-integrity-protocol.md` 1 행과 정확히 일치)
- [ ] RE-02: 신규 프로토콜의 rule 집합과 `audit-criteria.md` 의 rule 집합이 교집합 0 이다 [exact]
      (측정: `audit-criteria.md` §3 Database 4 rule 명(`N+1 부재`·`인덱스 존재`·
      `Connection pooling`·`Migration 안전성`)과 §9 Testing 6 rule 명이 프로토콜 본문에서
      rule 로 재정의되지 않음 — 각 rule 명 `grep -cF` in 프로토콜 → 전부 `0` ·
      프로토콜이 두 문서의 담당 범위를 표로 명시: `grep -c '교집합이 없다' <프로토콜>` ≥ 1)

## Diagnostics

- [ ] DG-01: `python3 scripts/validate-plugin.py backend-kit` 이 FAIL 0 으로 통과한다 [exact]
- [ ] DG-02: `python3 scripts/sync-docs.py --check-only` 가 `backend-kit/README.md` 갱신을
      요구하지 않는다 [exact]
      (측정: 출력의 `[backend-kit]` 블록에 `변경 필요` 0 건 — 다른 킷의 상태는 본 계약 범위 밖)
- [ ] DG-04: 위 모든 grep 오라클을 zsh 와 bash 에서 실행한 출력이 동일하다 (diff 0) [exact]
