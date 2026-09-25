---
feature: "카이젠 2026-09-24 Phase 7 계약 — 시각 종류 · 시간대 출처 · OAuth 2.1 draft-16 · OpenAPI 3.2.1 · 감사 기준 CDC 행 정정 · 미검증 네 칸"
slug: kaizen-0924-p07-backend-kit
created: "2026-09-25 05:22"
complexity: "복잡"
conditions: 26
status: done
owner_session: de8c7935-a5b6-4df5-9106-fafa73c288a0
conditions_digest: sha256:80b4853008bd8dfe
locked_at: "2026-09-25 06:04"
---

## 배경

이 Phase 의 외부 근거는 `.harness/.meta/evidence/phase7.md` 하나다. 처리 배정표(`.claude/kaizen-input/insights-report.md`)에서 `배정` 칸이
`Phase 7` 인 행은 `backend-family:P2` 하나다. 러닝북 `Phase 별 추가 과제` 에 Phase 7 줄은 없고, 앞 Phase notes 넷에도 Phase 7 로 넘긴 줄은 없다.
오케스트레이터 Step 7 은 「Phase 1 에서 설계 가이드가 변경되었으면 backend-kit 전 스킬을 전수 감사한다」 고 적는다 — 그 감사에서 하나를 찾았다.

| 키 · 출처 | 내용 | 이번 처리 |
| --- | --- | --- |
| `backend-family:P2` | 시각 종류(한 순간 대 벽시계)를 가르고 나라 · 시간대는 설정값으로 받는다. 비고: rust-model 부분은 Phase 9 와 맞춘다 | 반영 — SK-01 ~ SK-05 · AR-02. rust-model 은 Phase 9 로 넘긴다(ER-03) |
| `F20` (Phase 11 행) | 비고 「시간대를 설정값으로 다루는 것은 backend-family:P2(Phase 7)」 | 시간대 쪽만 이 계약이 맡는다. 폐기 결정 기록 자리는 Phase 11 몫이라 넘긴다(ER-03) |
| 근거 파일 §3 현행화 | OAuth 2.1 `draft-15` → `draft-16` · OpenAPI 3.2.0 → 3.2.1 · AsyncAPI 3.1.0 기록 · SeaORM 2.0.3 | OAuth 는 SK-06, OpenAPI 는 SK-07. AsyncAPI 는 킷 파일에 「최신판」 으로 적힌 버전이 없어 research-log 에 기록만 한다. SeaORM 과 rust-kit 버전 표는 Phase 9 몫(ER-03) |
| `docs/backend/research-log.md` 2026-08-13 미반영 | `audit-criteria.md` §8 CDC 행의 「Outbox+CDC 조합으로 exactly-once 보장 가능」 — 그때 범위 밖이라 backend-audit Gotcha 16 으로 무효 표시만 했다 | 반영 — SK-08. 근거 파일 §2 가 microservices.io 로 at-least-once 를 다시 확인했다 |
| Phase 1 가이드 변경 (`harness/docs/guides/skill-design-guide.md` §3.7 3 항 · `agent-design-guide.md` §10 정책 2 항) | `[미검증]` 에 사유 한 줄이 아니라 네 칸(막는 것 · 시도한 우회 · 통제 불가 사유 · 재검증 명령). `phase1-notes.md` 넘김 표에 backend-kit 줄이 없다 | 반영 — SK-09. backend-kit 안 옛 표기 열 자리(아홉 줄)를 전부 고친다 |
| 편집 전 감사 (`backend-kit/README.md:54`) | 검증 절 「7 카테고리 구조 감사」 — `scripts/validate-plugin.py` 의 검사는 V1 ~ V10 열 가지다. 바로 윗줄(`:53`)을 SK-05 가 고친다 | 반영 — SK-05. 숫자를 박지 않고 개수는 `harness/docs/guides/plugin-validation-guide.md` 가 정한다고 적는다. 같은 줄이 `infra-kit/README.md:54` 에도 있어 Phase 8 로 넘긴다(ER-03) |

글로벌 평가 피드백(`~/.harness/feedback/evaluator/`)에서 backend-kit 을 가리킨 기록 셋을 봤다. 2026-09-06 REJECT 는 `docs/backend/fundamentals/api-design.md`
의 OpenAPI 옛 값을 한 자리만 고치고 다른 자리를 남겨서 났다 — 그래서 SK-07 은 새 값이 아니라 옛 값 `3.2.0` 이 파일에 0 개인지를 먼저 잰다.
2026-08-14 REJECT(User-Reported Failure Protocol 인용 없음)는 `backend-reviewer.md` §10 이 이미 받았다. 2026-09-24 개선 메모(「10 카테고리」 낱말 측정이 이
킷과 겹친다)는 SK-04 가 낱말이 아니라 `^## [0-9]+\. ` 제목 수로 재서 피한다.

backend-kaizen Gotcha 4 의 관심사 상한(2~3)에 맞춰 셋으로 묶는다 — (1) 시각 종류와 시간대 출처(SK-01 ~ SK-05 · AR-02) (2) 사실 정정과 현행화(SK-06 ~ SK-08)
(3) 미검증 네 칸(SK-09). 셋 다 파일 여러 개를 건드리지만 한 관심사 안의 형제 대칭이다(같은 Gotcha 4 가 이렇게 센다).

## 리서치 소스

외부 조회 0 회. 아래 URL 은 전부 근거 파일 `.harness/.meta/evidence/phase7.md` 에서 가져왔다.

- [RFC 5545 §3.3.5](https://www.rfc-editor.org/rfc/rfc5545.html#section-3.3.5) — DATE-TIME 세 형태(UTC 순간 · floating · TZID 에 묶인 지역 시각). floating 은 합리적일 때만. 서머타임으로 두 번 오는 시각은 첫 번째, 없는 시각은 전환 전 오프셋 (SK-01 ~ SK-04)
- [PostgreSQL — Date/Time Types](https://www.postgresql.org/docs/current/datatype-datetime.html) — `TIMESTAMPTZ` 는 UTC 로 바꿔 저장하고 원래 시간대를 남기지 않는다. `TIMESTAMP` 는 시간대 표시를 무시한다 (SK-01 · SK-02 · SK-04)
- [IETF OAuth 2.1 Draft](https://datatracker.ietf.org/doc/draft-ietf-oauth-v2-1/) — `draft-16`, 2027-03-07 만료, 여전히 Active Internet-Draft (SK-06)
- [OpenAPI Specification 최신판](https://spec.openapis.org/oas/latest.html) · [OpenAPI 3.2.1 release](https://github.com/OAI/OpenAPI-Specification/releases/tag/3.2.1) — 3.2.1, 2026-09-10 공개 (SK-07)
- [AsyncAPI 3.1.0 release](https://github.com/asyncapi/spec/releases/tag/v3.1.0) — 최신 안정판. 킷이 인용하는 수신자 규범은 3.0.0 에도 있다 (research-log 기록만)
- [microservices.io — Transactional Outbox](https://microservices.io/patterns/data/transactional-outbox.html) — relay 중복 발행 · consumer idempotency (SK-08)

근거 파일이 스스로 밝힌 한계를 그대로 옮긴다. RFC 5545 는 나라 코드 · 시간대를 어디서 받을지 · 저장할지 · 코드 상수 금지를 정하지 않는다 — 그래서 새 문장은
그 부분을 「RFC 요구가 아니라 이 킷의 규칙」 이라고 적는다(SK-01 ~ SK-04 가 그 문장을 잰다). 「벽시계는 전부 시간대 없이 저장」 이라는 이분법은 RFC 보다 넓다 —
특정 지역에 묶인 벽시계는 IANA 시간대 식별자를 함께 둬야 한다(근거 파일 §2 결론). 그래서 제안 원문(순간 대 벽시계 둘)이 아니라 셋으로 나눈다.
「알람」 은 뜻이 모호하고(여행해도 현지 07:00 인지, 특정 장소의 07:00 인지), 시간대를 사용자 설정에서 물려받을지 레코드에 남길지는 제품 요구가 정한다(§5) —
그래서 새 문장은 둘 중 하나를 고르지 않고 「어디서 받는지와 저장 여부를 계약에 적는다」 로 둔다. 벽시계 값을 API 로 보낼 때의 문자열 형태는 근거가 없어 넣지 않는다.
OpenAPI 3.1 을 적은 자리 셋은 최소 지원선인지 최신판 뜻인지 툴체인 확인이 먼저라 그대로 둔다(§5).

내부 입력: 데이터 풀 §0 처리 배정표 · §0-b `9a0d4163`(2026-09-14 — 버린 시간대 · 나라 항목을 되살리고 한 나라 우선 판단을 되풀이) · §0.5 [backend] 세 건
(참고만 — 공유 인덱스 · 빌드 신선도 · N+1 경계는 이번 관심사와 무관하다) · §1 글로벌 평가 피드백(위 배경).

## GAP 분석 · 개선안 초안

### 1.1 복잡도 4 축

| 축 | 물음 | 값 |
| -- | ---- | -- |
| 레이어 수 | 몇 개 계층을 관통하는가 | 4 — 원칙 문서(`docs/backend/`) · 스킬 넷 · 감사 기준과 평가 에이전트 · 평가 사례 데이터 |
| 공개 API·계약 변경 | 외부에 노출된 형태가 바뀌는가 | 예 — 감사 기준에 FAIL 행 둘이 더해지고 Timestamp 행의 대상이 순간 필드로 좁혀진다. backend-system 규격 산출물 (c) 항목이 시각 종류 칸을 요구한다 |
| 소비면 존재 | 이 형태를 받아 쓰는 반대편이 있는가 | 예 — 아래 Counterpart 표 |
| 회귀 위험 | 기존 동작이 깨질 수 있는가 | 예 — 감사 기준 표를 끊으면 backend-reviewer 가 rule 을 못 읽는다. Gotcha 를 가운데 끼우면 번호로 서로 가리키는 Gotcha 13 · 16 · 17 이 어긋난다 |

네 축 중 셋이 「예」 이고 공개 형태 변경과 소비면이 둘 다 「예」 라 **복잡**이다. Step 2.5 Counterpart 조건을 넣는다(AR-02 · ER-03).
기능 조건은 16 개다 — 복잡 9~20 안이다 (SKILL.md Step 6.2 둘째 명령으로 이 파일을 세면 16).

### 1.2 설정 리터럴 대조표

| config key | project.yaml 에서 읽은 값 | 계약에 쓴 값 |
| ---------- | ------------------------- | ------------ |
| `commands.analyze` | `bash -n scripts/release.sh` | DG-01 N/A 사유에 그대로 |
| `commands.test` | `bash scripts/release.sh 2>&1 \|\| true` | DG-03 N/A 사유에 그대로 |
| `diagnostics.ide_exclude` | `[]` | DG-02 에 그대로 |
| `contract_categories[].id` / `prefix` | `Skill`/`SK` · `Script`/`SC` · `Error`/`ER` · `Architecture`/`AR` | 조건 섹션 제목과 접두 그대로 |
| `anti_patterns[].id` / `message` | AP-01 · AP-02 · AP-03 · AP-04 | AP-01 · AP-03 · AP-04 선별, message 원문 그대로. AP-02(force push)는 이 Phase 가 밀어 넣지 않아 뺀다 |

### 1.4 편집 전 감사 (실제로 읽은 줄 — 시작 커밋 `7925890` 판)

| 대상 파일 | 실제 Read 증거 (`파일:라인`) | 발견한 기존 갭·위반 | 계약 조건화 |
| --------- | ---------------------------- | ------------------- | ----------- |
| `docs/backend/fundamentals/database.md` | `:1-9` (머리 설정 · 다루는 범위) · `:96-136` (원칙 8 · 9) · `:138` (`---`) · `:155-165` (안티패턴 표) | 시각 종류 · 시간대 출처 원칙 0 건. backend-kaizen Gotcha 2 는 이 문서에 없는 원칙을 스킬에 넣지 못하게 한다 | SK-01 |
| `docs/backend/fundamentals/api-design.md` | `:1-5` · `:78-82` (원칙 5 · 출처) · `:103` (수치 기준) | OpenAPI 3.2.0 세 자리 | SK-07 |
| `backend-kit/skills/backend-system/SKILL.md` | `:26` (OAuth draft-15) · `:28` (Gotcha 13 (c)) · `:30` (Gotcha 15) · `:32` (Gotcha 17 — 마지막) · `:50` (Step 2 API 규격 행) | 시각 종류 규칙 없음 · draft-15 | SK-02 · SK-06 |
| `backend-kit/skills/backend-guide/SKILL.md` | `:24` (OAuth draft-15 · 「2026-04 기준」) · `:29` (Gotcha 15) · `:32` (Gotcha 18 — 마지막) · `:44` (database 키워드) · `:53` (contract-counterpart 키워드) | 시각 종류 규칙 없음 · draft-15 | SK-03 · SK-06 |
| `backend-kit/skills/backend-audit/references/audit-criteria.md` | `:26` (Timestamp 행 — 「모든 timestamp 응답 필드」) · `:28` (`[미검증]` + 사유) · `:30-39` (§3 Database 표 넷 · 정적 대체 규약의 `[미검증]` + 사유) · `:93` (CDC 행 exactly-once) | 벽시계 판정 행 없음 · 순간 · 벽시계 구분 없는 Timestamp 행 · 옛 CDC 서술 · 옛 미검증 표기 둘 | SK-04 · SK-08 · SK-09 |
| `backend-kit/skills/backend-audit/SKILL.md` | `:25` (Gotcha 11 본문 · 예시) · `:26` (Gotcha 12) · `:30` (Gotcha 16) · `:49` (DB 엔진 문단) · `:80` (Step 3 8 행) · `:89` (17 행 draft-15) · `:114` (CONDITIONAL APPROVE 보고 문구) | 본문 「근거에 이유를 기술하라」 · 네 칸 없는 `[:ENV]` 예시 · 옛 표기 둘 · 옛 서술을 가리키는 Gotcha 16 · draft-15. `:114` 「미검증 1 건: [체크항목] — [이유]」 는 reviewer 복제 조항 5 의 보고 모양과 같아 그대로 둔다(backend-kaizen Gotcha 8) | SK-04 · SK-06 · SK-08 · SK-09 |
| `backend-kit/agents/backend-reviewer.md` | `:33` · `:52` (rule 정본 두 파일) · `:57` (「`[미검증]` 태그 + 이유」) · `:62` (draft-15) · `:64` (예시 4 행 「4 요건 충족(호출 로그…)」) · `:110-120` (남용 방지 4 요건) | 출력 포맷의 미검증 표기와 예시 행이 4 요건보다 약하다 · draft-15 | SK-06 · SK-09 · AR-02 |
| `backend-kit/skills/backend-test/SKILL.md` | `:28` (Gotcha 13 끝 「`[미검증]` + 사유」) · `:256` (Step 5 「`[미검증] <사유>`」) | 가이드 §3.7 3 항의 반대편 두 자리 | SK-09 |
| `backend-kit/evals/evals.json` | `:50` (사례 4 draft-15) · `:81-92` (사례 7 — 마지막) | 시각 사례 없음 · draft-15 | SK-05 · SK-06 |
| `backend-kit/README.md` | `:53` (「7 스킬 assertion 전수 검증」) · `:54` (「7 카테고리 구조 감사」) · `:59` (2026-04-24 이력의 draft-15) | 평가 사례 수 표기 · 구조 검사 개수(실제 V1 ~ V10) | SK-05 (`:59` 는 이력이라 그대로 — SK-06 예외) |
| `backend-kit/skills/backend-guide/references/principle-index.md` | `:12` (Database → database.md) | 없음 — 원칙 10 이 이 경로로 읽힌다 | AR-02 (고치지 않는다) |
| `backend-kit/references/write-path-integrity-protocol.md` | `:182-201` (§6 at-least-once) | 없음 — SK-08 이 가리킨다 | AR-02 (고치지 않는다) |
| `rust-kit/skills/rust-model/SKILL.md` | `:78` · `:90` (타임스탬프 타입) · `:228-238` | Phase 9 파일 — 읽기만 | ER-03 넘김 |

후보 옵션은 하나로 정했다 — 시각 원칙 본문을 어디에 둘지(가) `docs/backend/fundamentals/database.md` 원칙 10 (나) `api-design.md` (다) 새 문서.
(가)를 고른다. backend-guide Step 2 가 principle-index 의 Database 행으로 이미 그 파일을 읽고, 저장 형태가 규칙의 중심이다. (다)는 principle-index ·
docs-site 매핑까지 늘어 크기에 비해 크다. Gotcha 는 번호를 밀지 않도록 맨 끝(backend-system 18 · backend-guide 19)에 더한다.

### Counterpart — 바뀌는 형식을 받아 쓰는 반대편

| 면 | 파일 | 바뀌는 것 | 이번 처리 |
| --- | --- | --- | --- |
| producer | `backend-kit/skills/backend-audit/references/audit-criteria.md` | FAIL 행 둘 · Timestamp 행 대상 · CDC 행 · 미검증 표기 | SK-04 · SK-08 · SK-09 |
| consumer | `backend-kit/agents/backend-reviewer.md` | rule 을 파일째 읽는다(`:33` · `:52`) — 행을 따로 옮겨 적지 않는다 | 고치지 않는다 — AR-02 가 그 줄이 그대로인지 잰다. 출력 포맷 미검증 표기만 SK-09 |
| consumer | `backend-kit/skills/backend-audit/SKILL.md` | Gotcha 16 이 CDC 행의 옛 서술을 가리킨다 · Step 3 8 행 예시 | SK-08 · SK-04 |
| producer | `docs/backend/fundamentals/database.md` 원칙 10 | 새 원칙 | SK-01 |
| consumer | `backend-kit/skills/backend-guide/references/principle-index.md` | Database 행 → database.md | 고치지 않는다 — AR-02 가 경로를 풀어 원칙 10 이 읽히는지 잰다 |
| consumer | `backend-kit/skills/backend-system/SKILL.md` · `backend-kit/skills/backend-guide/SKILL.md` | 원칙 10 을 가리키는 Gotcha | SK-02 · SK-03 · AR-02 |
| consumer | `backend-kit/evals/evals.json` · `backend-kit/README.md` | 사례 수 · draft 표기 | SK-05 · SK-06 |
| consumer (Phase 9) | `rust-kit/skills/rust-model/SKILL.md` | 타입 대응 — SQLx `DateTime<Utc>` + `TIMESTAMPTZ`, SeaORM 은 `DateTimeWithTimeZone`(근거 파일 §2). `:90` 입력 표 「타임스탬프 타입」 에 시각 종류 구분 | 명시적 미완 — ER-03 이 notes 넘김을 잰다. 이 Phase 는 건드리지 않는다(ER-03 · AR-01) |
| consumer (Final) | `docs/backend-kit/database.html` · `docs/backend-kit/api-design.html` | 원칙 10 이 없고 OpenAPI 3.2.0 이 남는다 | 명시적 미완 — Final F2 재생성(ER-03) |

### 개선안 초안

치환 마흔 개를 글자 그대로 적은 모의 스크립트가
`/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/de8c7935-a5b6-4df5-9106-fafa73c288a0/scratchpad/p7d/mock.py` 에 있다.
옛 문자열이 정확히 한 번 있어야 치환하고 끝에 `mock applied 40` 을 낸다. BUILD 는 이 치환을 글자 그대로 옮긴다 — 조건이 문장을 글자 그대로 센다.
파일마다 요지:

1. `docs/backend/fundamentals/database.md` — 머리 설정 0.3.0 · 2026-09-25, 다루는 범위에 「시각 종류별 저장」, 원칙 9 뒤 원칙 10(세 종류 표 · IANA 시간대 식별자 ·
   `TIMESTAMPTZ` 가 원래 시간대를 남기지 않음 · floating time · 서머타임 해석 · 시간대 · 나라 상수 금지와 그것이 킷 규칙이라는 문장 · 출처 둘), 안티패턴 두 행
2. `backend-kit/skills/backend-system/SKILL.md` — Gotcha 18 (E2 — 규격 산출물에 시각 필드마다 네 칸), Gotcha 13 (c), Step 2 API 규격 행, OAuth draft-16
3. `backend-kit/skills/backend-guide/SKILL.md` — Gotcha 19 (E1 — 「UTC 로 통일하라」 전에 종류부터), database 키워드 다섯, OAuth draft-16
4. `backend-kit/skills/backend-audit/references/audit-criteria.md` — §3 두 행(시각 종류별 저장 · 시간대 · 나라 상수 금지), §2 Timestamp 행을 순간 필드로, §8 CDC 행
   at-least-once, `[미검증]` 두 자리를 네 칸으로
5. `backend-kit/skills/backend-audit/SKILL.md` — Gotcha 11 본문 · 예시 · Gotcha 12 · DB 엔진 문단을 네 칸으로, Gotcha 16 을 옛 서술 대신 기준으로
   (CDC 행도 같은 기준으로 판정한다는 문장), Step 3 8 · 17 행
6. `backend-kit/agents/backend-reviewer.md` — 출력 포맷 미검증 표기와 예시 4 행을 네 칸으로, 2 행 draft-16
7. `backend-kit/skills/backend-test/SKILL.md` — Gotcha 13 · Step 5 의 `[미검증]` 을 네 칸으로
8. `backend-kit/evals/evals.json` — 사례 8 (반복 시각 저장 · 기본 시간대 상수, backend-guide), 사례 4 draft-16
9. `backend-kit/README.md` — 검증 절 「평가 사례 8 개의 구조 검증」 · 「등록된 검사 전부 (개수는 `harness/docs/guides/plugin-validation-guide.md` 가 정한다)」
10. `docs/backend/fundamentals/api-design.md` — OpenAPI 3.2.1 세 자리, 머리 설정 0.1.1 · 2026-09-25
11. `docs/backend/research-log.md` — `## [2026-09-24] — Phase 7 kaizen` 항목(외부 근거 여섯 · 사실 정정 셋 · 변경 요약 · 미반영 넷), 머리 설정 1.4.0 · 2026-09-25

새 규칙의 강도: backend-system Gotcha 18 은 E2(규격 산출물에 시각 필드 표를 남긴다 — skill-design-guide §3.7 초기 등급표의 「범위 · 개수 · 증거를 남겨야 하는
규칙」), backend-guide Gotcha 19 는 E1(가이드 답변 속 지적이라 남길 산출물이 없다). 감사 기준 두 행은 평가 측 판정이다.

## 범위 경계

- 이 Phase 시작 HEAD: `79258900de00e621412e4c436b44028a77d7fb64`. 범위 상한은 개정 파일 `.harness/sprint-amendments-kaizen-0924-p07-backend-kit.md` 의
  `end_sha:` 마지막 값이다. 여러 Phase 가 같은 가지 `kaizen/2026-09-24` 에 동시에 커밋하므로 `HEAD` 로 재지 않는다
- 고치는 파일은 열하나다 — 아래 블록이 그 목록이다(`harness/README.md` §커밋 안전 훅 이 정한 범위 선언 자리). 새 파일은 없다. `.harness/` 쪽은 이 계약 · 개정 파일 ·
  QA 피드백 · `.harness/.meta/kaizen-0924/phase7-notes.md` · `.harness/.meta/kaizen-0924/phase7-review.md` 를 쓴다 — 슬러그를 나열하지 않고 AR-01 셋째 값 `verify_seal` 로 잰다.
  AR-01 다섯째 값이 이 블록과 측정 공통 정의의 `FILES` 가 같은지 잰다

```text
# sprint-scope
docs/backend/fundamentals/database.md
docs/backend/fundamentals/api-design.md
docs/backend/research-log.md
backend-kit/skills/backend-system/SKILL.md
backend-kit/skills/backend-guide/SKILL.md
backend-kit/skills/backend-audit/SKILL.md
backend-kit/skills/backend-audit/references/audit-criteria.md
backend-kit/agents/backend-reviewer.md
backend-kit/skills/backend-test/SKILL.md
backend-kit/evals/evals.json
backend-kit/README.md
.harness/
```

- **이 Phase 의 커밋 메시지에는 전부 `Co-Authored-By` 줄 바로 위에 서명 줄 `Kaizen-Phase: kaizen-0924-p07-backend-kit` 한 줄을 넣는다** (봉인 커밋 포함).
  AR-01 · ER-03 · SC-00 · DG-01 · DG-03 · DG-04 · DG-06 이 이 줄로 이 Phase 커밋을 가린다(`harness/references/contract-schema.md` §여러 주체가 한 가지에 커밋할 때 선택지 B).
  서명을 빠뜨린 커밋은 서명 줄 목록에 안 보이므로 AR-01 첫째 값과 ER-03 셋째 값은 경로로 직접 센다.
  FIX 가 커밋을 더할 때도 넣고, 개정 파일에 `end_sha:` 줄을 덧붙인다(옛 줄은 지우지 않는다). notes 커밋도 이 Phase 커밋이다 — notes 를 커밋한 뒤 그 sha 로
  `end_sha:` 줄을 하나 더 덧붙여 커밋한다
- 구현 커밋은 `git add -- <파일…> && git commit -o -- <파일…>` 로 열한 파일만 싣는다. `docs/backend/` 셋과 `backend-kit/` 여덟을 두 커밋으로 나눠도 된다 —
  둘 다 이 킷 몫이라 `validate-post-kaizen.py` scope-isolation 에 걸리지 않는다(예행에서 두 커밋으로 확인)
- 측정이 기대는 제목 · 줄 머리는 이름을 바꾸지 않는다: `### 9. ` · `## 안티패턴` · `## 수치 기준` (database.md) · `# Gotchas` · `## Step 2: 진단` (backend-system) ·
  `# Gotchas` · `## Step 1: 탐색` (backend-guide) · `## 2. API Design` · `## 3. Database` · `## 8. Event-Driven` (audit-criteria) · `### Step 5: 실행 검증` (backend-test) ·
  `## 출력 포맷` (backend-reviewer) · `| Database |` (principle-index — 읽기만) · `## 6. Outbox 는 at-least-once 다` (write-path-integrity-protocol — 읽기만) ·
  skill-design-guide §3.7 의 네 칸 줄(읽기만)
- 공유 파일(`.claude-plugin/marketplace.json` · `backend-kit/.claude-plugin/plugin.json` 버전 · 루트 `README.md` · 루트 `CLAUDE.md` · `docs/` HTML · 처리 배정표 · 감사 로그 ·
  실패 횟수 파일 · `.github/workflows/ci.yml` · `.harness/stale-values.yaml`)과 다른 Phase · 레포 전용 파일(`rust-kit/` · `harness/` · `scripts/` · `.claude/skills/`)은
  건드리지 않는다 — ER-03 셋째 값. backend-kit README 에는 AUTO 구간이 없다. 문서 사이트 재생성은 Final F2 몫이라 DG-06 에서 `docs-site-regen` 을 뺀다
- QA(`harness:qa-evaluator`)는 설치본이다 — 이 Phase 가 고치는 파일에 qa-evaluator 는 없다
- 사용자 승인(Step 5) 대체: 사용자가 「자동으로 끝까지 알아서 진행해 내 허락이 필요한건 코덱스로 리서치나 검토받고」라고 위임했다(세션
  `de8c7935-a5b6-4df5-9106-fafa73c288a0` 기록 queued_command `2026-09-24T04:04:16.964Z`). Codex 사용량 한도가 소진돼(오류 원문 「You've hit your usage limit … try
  again at 11:05 PM」, 2026-09-24) 독립 Claude 검토자(REVIEW 에이전트)가 대신한다. 이어 사용자가 「코덱스 대신에 그냥 너가 알아서 진행하라고」라고 명시했다(같은 세션
  기록 user `2026-09-24T11:54:58.940Z`). 검토 결과 파일: `.harness/.meta/kaizen-0924/phase7-review.md`. 검토 VERDICT: 1 회차 `CHANGES` — 고칠 것 둘(SK-09 옛 표기 두 자리 ·
  ER-01 notes URL)과 막지 않는 권장 여섯을 초안이 전부 반영했다. 2 회차 `APPROVE` — 조건 줄 26 개는 그대로 봉인해도 된다. 조건 줄 밖 결함 하나(`common.sh` 의 틀 없는
  `mktemp -d` 가 `TMPDIR` 를 무시한다)는 BUILD 가 봉인 전에 2 회차 「고칠 문구」 그대로 `회귀 게이트` 절 `common.sh` 한 줄과 그 위 설명 문장을 고쳤다. 조건 줄은 건드리지 않아 봉인 값이 같다
- 오라클 한계: SK-05 는 평가 사례의 **구조**만 잰다(`scripts/run-evals.py` 는 스킬을 실행하지 않는다). 사례 8 을 실제 스킬로 돌려 답이 네 assertion 을 채우는지는
  LLM 판정이라 결정론 측정이 없다 — 조건으로 걸지 않는다
- 오라클 해소: SK-01 ~ SK-04 · SK-06 ~ SK-09 — 산출물이 문서 문장 자체라 정해진 절 · 줄에 정해진 문장이 있는지가 판정이다. `sect` 가 코드 펜스를 건너뛰고 절을 자르고,
  `gline` 이 한 줄짜리 Gotcha · 표 행을 고른다. 시작 커밋 판에서 새 문장 0 · 옛 문장 1 이상을 봉인 전에 확인했고, 문장 하나만 지운 사본 70 개(SK-05 README 한 줄 포함)에서 그 값이 0 으로 떨어졌다(`회귀 게이트` 절)
- 오라클 해소: SK-05 · DG-05 — 검사 스크립트를 실제로 돌린 출력이다. 음성 대조가 붙어 있다
- 오라클 해소: ER-01 · ER-02 · AP-01 · AP-03 · DG-02 — 편집 전 판과 파일마다 비교한 더한 줄 계산이다. 각각 양성 대조가 붙어 있다
- 오라클 해소: ER-03 · AR-01 · SC-00 · DG-01 · DG-04 · DG-06 — 커밋 기록과 봉인 검증 함수를 실제로 돌린 출력이다. 예행 저장소 변형 넷이 양성 대조다
- 커버리지 해소: SK-01 · SK-02 · SK-04 · SK-06 · SK-09 · AR-02 — 산문의 파일 이름은 측정 `m <조건 ID>` 가 공통 정의의 변수(`$DB` · `$AD` · `$RL` · `$SY` · `$GU` ·
  `$AU` · `$AC` · `$RV` · `$TE` · `$EV` · `$RM`)로 연다(파일과 변수의 대응은 `common.sh` 머리). 토큰은 `m.sh` 의 같은 ID 갈래에 글자 그대로 있다.
  SK-01 의 `0.3.0` 은 머리 설정 값이라 `fm_get` 이 읽고, `m.sh` 는 측정 도우미 자체의 이름이다. SK-06 의 `docs/backend/research-log.md` · `backend-kit/README.md` 는 예외로 적은 이력 파일이다.
  SK-09 · AR-01 의 `backend-kit/` 는 `grep -r` · `unsigned_on` 의 인자다
- 커버리지 해소: ER-01 — `.harness/.meta/kaizen-0924/phase7-notes.md` · `.harness/.meta/evidence/phase7.md` 는 공통 정의의 `$NOTES` · `$EVID` 다. 측정 절은 `m ER-01` 한 줄이다
- 커버리지 해소: ER-03 — `.harness/.meta/kaizen-0924/phase7-notes.md` 는 공통 정의의 `$NOTES` 다. `plugin.json` · `docs/backend-kit/api-design.html` · `docs/backend-kit/database.html` ·
  `.harness/stale-values.yaml` · `.claude/skills/backend-kaizen/SKILL.md` · `infra-kit/README.md` 는 `m.sh` `ER-03)` 갈래 `toks` 의 인자이고, `3.2.0` · `3.2.1` 은 넘김 설명,
  `design-kit/README.md` 는 예행 설명, `m.sh` 는 측정 도우미 자체의 이름이다
- 커버리지 해소: AR-01 — `docs/backend/` 는 `unsigned_on` 의 인자, `.harness/` 는 `scope` 블록 줄과 `verify_seal` 이 도는 폴더, `harness/references/contract-schema.md` 는 권장 형태의 출처다
- 검출기는 공백 든 코드 조각 안의 인자를 읽지 못한다 — 위 해소 줄이 전부 그 경우다
- 편집 전부터 있던 경고(markdownlint MD060 · MD025 · MD032 등)는 범위 밖이다 — DG-02 는 더한 줄의 새 경고만 잰다
- notes 에 함께 적는다(조건으로는 재지 않는다): 「그대로 둔 곳」 에 `backend-kit/skills/backend-audit/SKILL.md:114` 의 「미검증 1 건: [체크항목] — [이유]」 —
  reviewer 복제 조항 5 의 보고 모양과 같아 그대로 둔다(backend-kaizen Gotcha 8). Phase 1 가이드 변경 셋(네 칸 · 작업 불가 전 네 칸 · 알려진 답 대조)을
  반영 · 해당 없음으로 나눈 짧은 표(backend-kaizen Gotcha 8). ER-03 셋째 값이 0 이 아니면 QA 가 그 커밋 목록부터 보고 판정한다는 한 줄 —
  그 값은 다른 Phase 가 서명 줄을 단다는 전제에 기댄다(지금까지 서명 없는 커밋은 오케스트레이터의 근거 파일 커밋뿐이다). 「다음 사이클 메모」 에 harness 과제 한 줄 —
  봉인 digest 는 조건 첫 줄만 덮어 둘째 줄의 요구값과 `m.sh` 가 봉인 뒤 바뀌어도 `SEAL_OK` 다(검토 `phase7-review.md` 참고)
- 기능 조건 16 · 전체 조건 줄 26
- 사용자가 할 일: 없음

## 회귀 게이트 — 측정 공통 정의와 봉인 전 실측

모든 조건의 측정은 아래 `common.sh` 와 `m.sh` 를 차례로 `.` 으로 읽은 **bash** 셸에서 돈다(zsh 는 따옴표 없는 변수를 쪼개지 않아 DG-05 의 `scripts/$c` 가 파일을 못 찾는다 —
실측 2026-09-25). `m` 은 도우미 함수와 두 판 폴더가 없으면 `HELPER_MISSING` · `SNAPSHOT_MISSING` 을 내고 멈춘다 — 그래서 조건마다 `type m` 하나로 정의 확인을 대신한다.
예행 값은 bash 5.3.9 와 `/bin/bash` 3.2.57 두 해석기에서 같았다. 두 블록과 `new-warnings.sh` 를 각 블록 첫 `#` 주석 줄(셔뱅 다음)의 이름 그대로 한 폴더에 저장하고 그 폴더를 `K` 에 넣는다. `END_UNRESOLVED` 가 찍히면
셸이 종료 코드 2 로 끝난다. `new-warnings.sh` 옆에는 `node_modules` 를
`/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/de8c7935-a5b6-4df5-9106-fafa73c288a0/scratchpad/p1build/node_modules` 로 잇고
`cfg.markdownlint-cli2.jsonc` = `{ "config": { "MD013": false } }` 를 둔다 — 준비 단계 실측(2026-09-25): 그 자리의 `.bin/markdownlint-cli2 --version` 첫 줄이
`markdownlint-cli2 v0.23.2 (markdownlint v0.41.1)`. 없으면 그 폴더에서 `npm install --no-save markdownlint-cli2@0.23.2` 부터 돌린다.
`common.sh` 의 `R` 은 예행 저장소를 가리킬 때만 쓴다 — 비우면 작업 폴더다. `common.sh` 는 두 판을 `${TMPDIR:-/tmp}/p7m.XXXXXX` 에 풀므로 `TMPDIR` 를 스크래치 폴더로 두고 읽는다. 틀 없는 `mktemp -d` 는
이 맥에서 `TMPDIR` 를 무시하고 시스템 임시 폴더에 푼다(2 회차 검토 실측 2026-09-25 — 한 번 읽을 때마다 40 ~ 70 MB 가 남았다).

```bash
# common.sh — 측정 공통 정의. bash 로 읽는다 (zsh 는 배열 첨자가 1 부터이고 따옴표 없는 변수를 쪼개지 않는다)
export LC_ALL=C.UTF-8   # 번역투 정규식이 글자 단위로 돌아야 한다
cd "${R:-/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/kaizen-0924}" || exit 2
B=79258900de00e621412e4c436b44028a77d7fb64                  # 이 Phase 시작 HEAD
SIG='Kaizen-Phase: kaizen-0924-p07-backend-kit'
CF=.harness/sprint-contract-kaizen-0924-p07-backend-kit.md
AM=.harness/sprint-amendments-kaizen-0924-p07-backend-kit.md
NOTES=.harness/.meta/kaizen-0924/phase7-notes.md
EVID=.harness/.meta/evidence/phase7.md
END=$( [ -f "$AM" ] && sed -n 's/^end_sha:[[:space:]]*//p' "$AM" | tail -1 )
if [ -z "$END" ] || ! git rev-parse -q --verify "$END^{commit}" >/dev/null; then
  echo "END_UNRESOLVED — 측정을 멈춘다. HEAD 로 바꿔 재지 않는다"; exit 2
fi
: "${K:?도우미 폴더를 K 에 넣는다}"
DB=docs/backend/fundamentals/database.md
AD=docs/backend/fundamentals/api-design.md
RL=docs/backend/research-log.md
SY=backend-kit/skills/backend-system/SKILL.md
GU=backend-kit/skills/backend-guide/SKILL.md
AU=backend-kit/skills/backend-audit/SKILL.md
AC=backend-kit/skills/backend-audit/references/audit-criteria.md
RV=backend-kit/agents/backend-reviewer.md
TE=backend-kit/skills/backend-test/SKILL.md
EV=backend-kit/evals/evals.json
RM=backend-kit/README.md
FILES=("$DB" "$AD" "$RL" "$SY" "$GU" "$AU" "$AC" "$RV" "$TE" "$EV" "$RM")
MDS=("$DB" "$AD" "$RL" "$SY" "$GU" "$AU" "$AC" "$RV" "$TE" "$RM")
T=$(mktemp -d "${TMPDIR:-/tmp}/p7m.XXXXXX") || exit 2; mkdir -p "$T/B" "$T/E"
# 두 판을 풀어 둔 폴더에서 잰다 — 작업 폴더에 남은 다른 Phase 의 미커밋 변경이 끼지 않는다
git archive "$B" | tar -x -C "$T/B"; git archive "$END" | tar -x -C "$T/E"
# sect <파일> <제목 앞부분> — 그 제목부터 같은 깊이 이하의 다음 제목 전까지. 코드 펜스 안의 `#` 줄은 제목으로 보지 않는다
sect() { awk -v h="$2" '
  /^[[:space:]]*(```|~~~)/ { fence = !fence }
  !f && !fence && index($0, h) == 1 { f = 1; lvl = match($0, /[^#]/) - 1; print; next }
  f && !fence && /^#+ / { l = match($0, /[^#]/) - 1; if (l <= lvl) exit }
  f' "$1"; }
# gline <파일> <줄 앞부분> — 그 앞부분으로 시작하는 줄. Gotcha 와 표 행은 한 줄이다
gline() { awk -v p="$2" 'index($0, p) == 1' "$1"; }
# toks <글> <토큰…> — 토큰마다 글 안에서 그 토큰이 든 줄 수
toks() { local s="$1"; shift; for t in "$@"; do printf '%s ' "$(printf '%s\n' "$s" | grep -cF -- "$t")"; done; echo; }
url()   { grep -oE 'https?://[^ )>"`]+' | sed -E 's/[.,;:]+$//' | sort -u; }
added() { for f in "${FILES[@]}"; do git diff --no-index -U0 "$T/B/$f" "$T/E/$f"; done | grep '^+' | grep -v '^+++'; }
mine() { git log --format= --name-only "${1}..${2}" --grep="^${3}\$" | grep . | LC_ALL=C sort -u; }
unsigned_on() { _b=${1}; _u=${2}; _s=${3}; shift 3
  git log --format=%H "${_b}..${_u}" -- "$@" | while read -r _c; do git log -1 --format=%B "$_c" | grep -qxF "$_s" || echo "$_c"; done; }
# not_other <base> <상한> <서명> <경로…> — 경로를 건드린 구간 안 커밋 가운데 다른 Phase 서명이 없는 커밋 (0 줄이어야 한다)
not_other() { _b=${1}; _u=${2}; _s=${3}; shift 3
  git log --format=%H "${_b}..${_u}" -- "$@" | while read -r _c; do
    _m=$(git log -1 --format=%B "$_c")
    if printf '%s\n' "$_m" | grep -qE '^Kaizen-Phase: ' && ! printf '%s\n' "$_m" | grep -qxF "$_s"; then continue; fi
    echo "$_c"; done; }
my() { mine "$B" "$END" "$SIG"; }
# scope <계약> — `## 범위 경계` 절 안, 첫 줄이 `# sprint-scope` 인 text 블록의 경로 줄
scope() { awk '/^## /{s=$0} s ~ /^## 범위 경계/ && /^```text$/{b=1; n=0; next} b && /^```$/{b=0; next} b{n++; if (n==1 && $0 != "# sprint-scope") b=0; else if (n>1) print}' "$1"; }
fm_get() { awk -v k="^$2:[[:space:]]*" 'NR==1 && /^---[[:space:]]*$/ { fm=1; next } fm && /^---[[:space:]]*$/ { exit } fm && $0 ~ k { sub(k, "", $0); print; exit }' "$1" | sed -e "s/[[:space:]]*$//" -e "s/^['\"]//" -e "s/['\"]\$//"; }
sha256_16() { if command -v sha256sum >/dev/null 2>&1; then sha256sum; elif command -v shasum >/dev/null 2>&1; then shasum -a 256; else python3 -c 'import hashlib,sys; print(hashlib.sha256(sys.stdin.buffer.read()).hexdigest())'; fi | cut -c1-16; }
contract_digest() { grep -E '^- \[[ x]\] [A-Z]{2,}-[0-9]{2}' "$1" | sed -E 's/^- \[[ x]\]/- [ ]/' | sha256_16; }
verify_seal() { rec=$(fm_get "$1" conditions_digest); rec=${rec#sha256:}; if [ -z "$rec" ]; then echo "SEAL_ABSENT $1"; return 0; fi
  act=$(contract_digest "$1"); if [ "$rec" = "$act" ]; then echo "SEAL_OK $1"; else echo "SEAL_BROKEN $1 recorded=$rec actual=$act"; fi; }
K02='(을|를) ?(처리|관리)(합니다|한다)|에 대해서?|하도록 (합니다|한다)|에 의(해|하여)|되어 있(는 경우|을 때)|(표시|적용|호출|생성|반환)(됩니다|된다)'
```

```bash
# m.sh — 조건마다 재는 값을 한 줄로 낸다. common.sh 를 읽은 bash 에서 `m <조건 ID>` 로 부른다
m() {
  local E=$T/E S L fn
  # 도우미가 하나라도 없으면 grep -c 가 조용히 0 을 낸다 — 멈춘다
  for fn in sect gline toks url added mine unsigned_on not_other my scope fm_get verify_seal; do
    type "$fn" >/dev/null 2>&1 || { echo "HELPER_MISSING $fn"; return 2; }; done
  [ -n "${T:-}" ] && [ -d "$T/B" ] && [ -d "$E" ] || { echo "SNAPSHOT_MISSING"; return 2; }
  case "$1" in
  SK-01)  # database.md 원칙 10 · 안티패턴 두 행 · 머리 설정
    S=$(sect "$E/$DB" '### 10. 시각은 종류부터 나누고, 종류마다 저장 형태를 정한다')
    toks "$S" '### 10. 시각은 종류부터 나누고' '| 순간 | 결제 시각, 생성 시각 |' '| 받는 사람 지역을 따라가는 벽시계 |' '| 특정 지역에 묶인 벽시계 |' \
      'IANA 시간대 식별자' '원래 시간대는 남기지 않는다' 'RFC 5545 의 floating time' \
      '두 번 오는 시각을 첫 번째로, 없는 시각을 전환 전 오프셋으로 해석한다' \
      '시간대와 나라를 코드 상수나 한 나라 기본값으로 박지 않는다' '나라 코드로 시간대를 정하지 않는다' \
      '이 항목은 RFC 요구가 아니라 이 킷의 규칙이다' \
      'https://www.rfc-editor.org/rfc/rfc5545.html#section-3.3.5' 'https://www.postgresql.org/docs/current/datatype-datetime.html'
    S=$(sect "$E/$DB" '## 안티패턴')
    toks "$S" '| 벽시계 뜻의 값(반복 일정·영업시간·알림 시각)을' '| 시간대·나라를 코드 상수나 한 나라 기본값으로 박음 |'
    # 원칙 10 이 원칙 9 뒤 · `## 수치 기준` 앞에 있다 — 줄 번호 셋이 오름차순이면 1
    awk '/^### 9\. /{a=NR} /^### 10\. 시각은/{b=NR} /^## 수치 기준/{c=NR} END{print (a && b && c && a<b && b<c) ? 1 : 0}' "$E/$DB"
    echo "$(fm_get "$E/$DB" version) $(fm_get "$E/$DB" last_updated)" ;;
  SK-02)  # backend-system Gotcha 18 · 13 (c) · Step 2 API 규격 행 · 번호
    L=$(gline "$E/$SY" '18. **시각은 종류부터 나누고 필드마다 표로 남겨라 (enforcement 등급 E2)**')
    toks "$L" '18. **시각은' '**종류 · 저장 형태 · 시간대 출처 · 순간으로 바꾸는 규칙** 네 칸을 적는다' \
      '종류는 순간 / 받는 사람 지역을 따라가는 벽시계 / 특정 지역에 묶인 벽시계 셋 중 하나' 'IANA 시간대 식별자' \
      '같은 시각이 두 번 오거나 없을 때의 처리' '이 칸은 RFC 요구가 아니라 이 킷의 규칙이다' \
      'docs/backend/fundamentals/database.md` 원칙 10 이다' 'https://www.rfc-editor.org/rfc/rfc5545.html#section-3.3.5'
    L=$(gline "$E/$SY" '13. **계약을 커밋된 아티팩트로 먼저 확정하라')
    toks "$L" '(c) **모든 시각 필드의 종류 · 시간대 출처(Gotcha 18)와 타임존·직렬화 규칙**' '(c) **모든 timestamp 필드의'
    L=$(sect "$E/$SY" '## Step 2: 진단' | awk 'index($0, "| API 규격 |") == 1')
    toks "$L" '**시각 종류 · 시간대 출처 표**(Gotcha 18)'
    sect "$E/$SY" '# Gotchas' | grep -oE '^[0-9]+\. \*\*' | tr -dc '0-9\n' | paste -sd' ' - ;;
  SK-03)  # backend-guide Gotcha 19 · database 키워드 · 번호
    L=$(gline "$E/$GU" '19. **"UTC 로 통일하라" 전에 시각 종류부터 나눠라 (enforcement 등급 E1)**')
    toks "$L" '19. **"UTC 로' '받는 사람 지역을 따라가는 벽시계' '특정 지역에 묶인 벽시계' 'IANA 시간대 식별자' \
      '한 나라나 한 시간대를 기본값으로 박은 설계를 보면 지적하고' '"표준 위반" 이라고 말하지 않는다' \
      'docs/backend/fundamentals/database.md` 원칙 10 이다'
    L=$(sect "$E/$GU" '## Step 1: 탐색' | awk 'index($0, "| database |") == 1')
    toks "$L" '벽시계, 반복 일정, 시간대, 서머타임, 나라 코드'
    sect "$E/$GU" '# Gotchas' | grep -oE '^[0-9]+\. \*\*' | tr -dc '0-9\n' | paste -sd' ' - ;;
  SK-04)  # audit-criteria §3 두 행 · 표 한 덩어리 · §2 Timestamp 행 · 카테고리 수 · audit SKILL 8 행
    S=$(sect "$E/$AC" '## 3. Database')
    L=$(printf '%s\n' "$S" | awk 'index($0, "| 시각 종류별 저장 |") == 1')
    toks "$L" '| 시각 종류별 저장 |' '하나로만 저장하면 FAIL' 'IANA 시간대 식별자 칸이 없으면 FAIL' '필드의 뜻이 실제로 벽시계일 때만 판정한다' 'rfc5545.html#section-3.3.5'
    L=$(printf '%s\n' "$S" | awk 'index($0, "| 시간대·나라 상수 금지 |") == 1')
    toks "$L" '| 시간대·나라 상수 금지 |' '코드 상수 하나로 강제하면 FAIL' '한 지역 전용 서비스라고 밝혔으면 N/A' 'RFC 요구가 아니라 이 킷의 범위 예외다'
    # 표 줄 수 · 끊긴 곳 — 머리 두 줄 + 행 여섯이면 8 0
    printf '%s\n' "$S" | awk '/^\|/{n++; if (p && NR != p + 1) g = 1; p = NR} END{print n + 0, g + 0}'
    L=$(sect "$E/$AC" '## 2. API Design' | awk 'index($0, "| Timestamp 직렬화 규칙 |") == 1')
    toks "$L" '순간(한 시점) timestamp 응답 필드가 전부' '이 행이 아니라 §3'
    echo "$(grep -cF '모든 timestamp 응답 필드가' "$E/$AC") $(grep -cE '^## [0-9]+\. ' "$E/$AC")"
    L=$(gline "$E/$AU" '| 8 | API Design | Timestamp 직렬화 규칙 |')
    toks "$L" '순간 필드 전부 RFC 3339'
    grep -cF '전 timestamp 필드' "$E/$AU" ;;
  SK-05)  # evals 사례 8 · run-evals · README 수
    python3 - "$E/$EV" <<'PY'
import json, sys
d = json.load(open(sys.argv[1], encoding="utf-8")); ev = d["evals"]
ids = [e.get("id") for e in ev]; e8 = [e for e in ev if e.get("id") == 8]
e = e8[0] if len(e8) == 1 else {}
a = [x.get("text", "") for x in e.get("assertions", [])]
print(len(ev), ids == list(range(1, len(ev) + 1)), e.get("skill"), "06:30" in e.get("prompt", ""), "서울" in e.get("prompt", ""), len(a),
      sum("받는 사람 지역을 따라가는지 특정 지역에 묶였는지" in t for t in a),
      sum("TIMESTAMPTZ 같은 순간 하나로만 저장하지" in t for t in a),
      sum("코드 기본값으로 박는 설계를 지적" in t for t in a),
      sum("database.md 원칙 10" in t for t in a))
PY
    ( cd "$E" && python3 scripts/run-evals.py backend-kit > "$T/re.txt" 2>&1; echo "rc=$? $(grep -E '^Total: ' "$T/re.txt")" )
    echo "$(grep -cF '평가 사례 8 개의 구조 검증' "$E/$RM") $(grep -cF '7 스킬 assertion 전수 검증' "$E/$RM") $(grep -cF '등록된 검사 전부 (개수는 `harness/docs/guides/plugin-validation-guide.md` 가 정한다)' "$E/$RM") $(grep -cF '7 카테고리 구조 감사' "$E/$RM")" ;;
  SK-06)  # OAuth 2.1 draft-16 — 파일마다 (새 표기 수 · 옛 표기 줄 수)
    for f in "$SY" "$GU" "$AU" "$RV" "$EV"; do
      printf '%s/%s ' "$(grep -oE 'draft-16|v2-1-16' "$E/$f" | wc -l | tr -d ' ')" "$(grep -cE 'draft-15|v2-1-15' "$E/$f")"; done; echo
    echo "$(grep -cF '`draft-ietf-oauth-v2-1-16` (2027-03-07 만료) 로 아직 Draft 임을 명시' "$E/$SY") $(grep -cF '2026-09-24 조회 기준 OAuth 2.1 은 `draft-ietf-oauth-v2-1-16` (Active Internet-Draft, 2027-03-07 만료)' "$E/$GU") $(grep -cF 'expires 2026-09' "$E/$GU")"
    # 남기는 이력 줄 — README 의 2026-04-24 절 한 줄이 편집 전과 같다
    diff <(grep -F 'draft-15' "$T/B/$RM") <(grep -F 'draft-15' "$E/$RM") >/dev/null && echo "readme_history_same=1" || echo "readme_history_same=0" ;;
  SK-07)  # OpenAPI 3.2.1
    toks "$(cat "$E/$AD")" '3.2.0' 'OpenAPI 3.2.1 스펙을 단일 소스로 유지한다' 'https://spec.openapis.org/oas/latest.html' \
      'https://github.com/OAI/OpenAPI-Specification/releases/tag/3.2.1' '| OpenAPI 최신 버전 | 3.2.1 (2026-09-10 공개'
    echo "$(fm_get "$E/$AD" version) $(fm_get "$E/$AD" last_updated)" ;;
  SK-08)  # CDC 행 · Gotcha 16 · 옛 서술
    L=$(sect "$E/$AC" '## 8. Event-Driven' | awk 'index($0, "| CDC 파이프라인 |") == 1')
    toks "$L" '전달 보장은 at-least-once 다' 'consumer idempotency 가 함께 있어야 PASS' 'write-path-integrity-protocol.md` §6' 'microservices.io/patterns/data/transactional-outbox.html'
    L=$(gline "$E/$AU" '16. **outbox 나 outbox+CDC 조합을 근거로 exactly-once 를 PASS 시키지 마라**')
    toks "$L" '16. **outbox 나' '행도 같은 기준으로 판정한다'
    grep -rF 'exactly-once 보장 가능' "$E/backend-kit" | grep -c . ;;
  SK-09)  # 미검증 네 칸 — backend-test · backend-audit · backend-reviewer · 가이드의 칸 이름
    L=$(gline "$E/$TE" '13. **mock-only 테스트를 integration 으로 명명하거나 보고하지 마라**')
    toks "$L" '`[미검증]` 에 네 칸(막는 것 · 시도한 우회 · 통제 불가 사유 · 재검증 명령)을 붙인다' 'Completion Evidence Gate 3 항'
    S=$(sect "$E/$TE" '### Step 5: 실행 검증')
    toks "$S" '을 달고 네 칸을 채운 뒤 **부분 완료**로 보고한다' '막는 것(실행한 명령과 그 실패 출력)' '시도한 우회(하나 이상과 그 결과, 정말 없으면' '통제 불가 사유(한 문장)' '재검증 명령(조건이 갖춰지면 돌릴 명령)'
    L=$(gline "$E/$AU" '11. **미검증 항목 마커 프로토콜')
    toks "$L" '근거에 네 칸(막는 것 · 시도한 우회 · 통제 불가 사유 · 재검증 명령)을 채워라' '막는 것: 운영 DB 접속 명령과 그 거부 출력' '시도한 우회: pool 설정 파일 정적 리뷰' '통제 불가 사유: 감사자에게 운영 DB 접속 권한이 없다' '재검증 명령: 권한을 받은 뒤 같은 접속 명령' '네 칸 중 하나라도 비면'
    toks "$(gline "$E/$AU" '12. **소비면을 안 보고')$(printf '\n')$(gline "$E/$AU" '**DB 엔진도 함께 확정한다.**')" \
      '통제 불가 사유 칸에 「저장소 접근 불가」를 적는다' '통제 불가 사유 칸에 「엔진 미확정」을 적는다'
    toks "$(sect "$E/$AC" '## 2. API Design')$(printf '\n')$(sect "$E/$AC" '## 3. Database')" \
      '별도 저장소면 `[미검증]` + 네 칸(막는 것 · 시도한 우회 · 통제 불가 사유 · 재검증 명령)' \
      '그때 `[미검증]` 에 네 칸(막는 것 · 시도한 우회 · 통제 불가 사유 · 재검증 명령)을 붙인다'
    S=$(sect "$E/$RV" '## 출력 포맷')
    toks "$S" '와 네 칸(막는 것 · 시도한 우회 · 통제 불가 사유 · 재검증 명령)을 근거 열에 적는다' '하나라도 비면 `INVALID` 다' \
      '막는 것: broker 접속 명령과 그 거부 출력 · 시도한 우회: outbox 테이블 DDL 정적 확인'
    toks "$(cat "$E/harness/docs/guides/skill-design-guide.md")" '   - **막는 것** —' '   - **시도한 우회** —' '   - **통제 불가 사유** —' '   - **재검증 명령** —'
    grep -rF -e '[미검증] <사유>' -e '`[미검증]` + 사유' -e 'pool 설정 파일 정적 리뷰만 수행' -e '`[미검증]` 태그 + 이유' \
      -e '근거에 이유를 기술하라' -e '4 요건 충족(호출 로그' "$E/backend-kit" | grep -c . ;;
  ER-01)  # 새로 생긴 URL 이 근거 파일에 있다 — 열한 파일은 파일마다 편집 전 판과 비교, notes 는 URL 전부
    for f in "${FILES[@]}"; do comm -13 <(url < "$T/B/$f") <(url < "$E/$f"); done | sort -u | comm -23 - <(url < "$E/$EVID") | grep -c .
    # notes 가 없으면 입력이 비어 조용히 0 이 된다 — 없다고 찍는다
    if [ -f "$E/$NOTES" ]; then url < "$E/$NOTES" | comm -23 - <(url < "$E/$EVID") | grep -c .; else echo NOTES_MISSING; fi ;;
  ER-02)  # 더한 줄의 번역투 6 종
    added | grep -cE "$K02" ;;
  ER-03)  # notes 문자열 · 공유 파일과 다른 Phase 파일을 건드린 커밋
    git cat-file -e "$END:$NOTES" && echo notes_committed=1 || echo notes_committed=0
    toks "$(cat "$E/$NOTES")" 'backend-family:P2' 'rust-model' 'docs/backend-kit/database.html' 'docs/backend-kit/api-design.html' \
      '.harness/stale-values.yaml' '.claude/skills/backend-kaizen/SKILL.md' 'plugin.json' 'infra-kit/README.md' 'OpenAPI 3.1' 'F20' \
      '## 반영한 처리 배정표 키' '## 미반영 키와 사유' '## 넘기는 것' '## changelog 한 단락' '## 킷 로그 한 단락' '## 다음 사이클 메모'
    not_other "$B" "$END" "$SIG" .claude-plugin/marketplace.json backend-kit/.claude-plugin/plugin.json README.md CLAUDE.md \
      .harness/.meta/orchestrator-audit-log.md .harness/.meta/kaizen-failure-count.yaml .claude/kaizen-input/insights-report.md \
      .github/workflows/ci.yml .harness/stale-values.yaml .claude/skills docs/backend-kit rust-kit harness scripts | grep -c . ;;
  AR-01)  # 허용 경로 · 서명 · 봉인 · 범위 선언 블록
    unsigned_on "$B" "$END" "$SIG" backend-kit docs/backend | grep -c .
    echo "$(my | grep -v '^\.harness/' | grep -vxF -f <(printf '%s\n' "${FILES[@]}") | grep -c .) $(my | grep -cxF -f <(printf '%s\n' "${FILES[@]}"))"
    find .harness -type f -name 'sprint-contract*.md' -print0 | while IFS= read -r -d '' f; do verify_seal "$f"; done \
      | awk '$1=="SEAL_BROKEN"{print $2}' | sed 's#^\./##' | sort -u | comm -12 - <( { my; echo "$CF"; } | sort -u) | grep -c .
    verify_seal "$E/$CF" | cut -d' ' -f1
    diff <(scope "$E/$CF" | grep -vxF '.harness/' | sort) <(printf '%s\n' "${FILES[@]}" | sort) >/dev/null && echo "scope_same=1" || echo "scope_same=0"
    scope "$E/$CF" | grep -cxF '.harness/' ;;
  AR-02)  # 연결 — 원칙 색인이 가리키는 파일 · 새 문장이 가리키는 절 · 규칙을 읽는 쪽
    python3 - "$E" <<'PY'
import os, sys
e = sys.argv[1]
base = os.path.join(e, "backend-kit/skills/backend-guide/references")
row = [l for l in open(os.path.join(base, "principle-index.md"), encoding="utf-8") if l.startswith("| Database |")]
p = os.path.normpath(os.path.join(base, row[0].split("|")[2].strip())) if len(row) == 1 else ""
ok = bool(p) and os.path.isfile(p) and any(l.startswith("### 10. 시각은") for l in open(p, encoding="utf-8"))
print(len(row), os.path.relpath(p, e) if p else "-", int(ok))
PY
    echo "$(grep -c '^## 6\. Outbox 는 at-least-once 다' "$E/backend-kit/references/write-path-integrity-protocol.md") $(grep -cxF -- '- backend-kit/skills/backend-audit/references/audit-criteria.md — 10 카테고리 기존 rule' "$E/$RV")" ;;
  RE-02)  # 원칙 본문은 한 곳 — 시각 종류 표 머리가 있는 파일 수
    grep -rlF '| 시각 종류 | 예 | 저장 형태 (PostgreSQL) | 순간이 필요할 때 |' "$E/backend-kit" "$E/docs/backend" | sed "s#^$E/##" ;;
  AP-01)  # 더한 줄에 이 킷 플러그인 버전 값 — 값은 plugin.json 에서 읽는다
    L=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["version"])' "$E/backend-kit/.claude-plugin/plugin.json")
    echo "version=$L $(added | grep -cF -- "$L")" ;;
  AP-03)  # 더한 줄의 코드 펜스 줄
    added | grep -cE '^\+[[:space:]]*(```|~~~)' ;;
  AP-04)  # frontmatter — 첫 블록이 편집 전과 같은지 / name 줄 수. README AUTO 구간이 읽는 값이 안 바뀐다
    for f in "$SY" "$GU" "$AU" "$TE" "$RV"; do
      L=$(basename "$f" .md); [ "$L" = SKILL ] && L=$(basename "$(dirname "$f")")
      printf '%s/%s ' "$(diff <(awk 'NR==1&&/^---/{fm=1;next} fm&&/^---/{exit} fm' "$T/B/$f") <(awk 'NR==1&&/^---/{fm=1;next} fm&&/^---/{exit} fm' "$E/$f") >/dev/null && echo 1 || echo 0)" \
        "$(awk 'NR==1&&/^---/{fm=1;next} fm&&/^---/{exit} fm' "$E/$f" | grep -cxF "name: $L")"; done; echo ;;
  DG-02)  # markdownlint — 더한 줄의 새 경고 · evals.json 파싱
    for f in "${MDS[@]}"; do k=$(printf '%s' "$f" | tr '/' '_'); cp "$T/B/$f" "$T/$k.0.md"; cp "$E/$f" "$T/$k.md"; bash "$K/new-warnings.sh" "$T/$k.0.md" "$T/$k.md"; done
    python3 -c 'import json,sys; json.load(open(sys.argv[1], encoding="utf-8")); print("json_ok")' "$E/$EV" ;;
  DG-05)  # 저장소 검사 — $END 판을 git 저장소로 만든 사본에서 돈다 (작업 폴더의 다른 Phase 미커밋 변경이 끼지 않는다)
    local G=$T/G; rm -rf "$G"; cp -R "$E" "$G"
    git -C "$G" init -q && git -C "$G" add -A && git -C "$G" -c user.name=m -c user.email=m@m commit -qm snap || return 2
    ( cd "$G" && python3 scripts/validate-plugin.py backend-kit > "$T/vp.txt" 2>&1 )
    echo "$(grep -cE '^  V([1-9]|10) ' "$T/vp.txt") $(grep -E '^  V([1-9]|10) ' "$T/vp.txt" | grep -cE 'ERROR|FAIL')"
    # sync-evals 는 킷 이름 인자가 없다 — backend-kit 머리 줄을 읽었는지와 그 아래 어긋남 줄 수만 센다
    ( cd "$G" && python3 scripts/sync-evals.py --check-only > "$T/se.txt" 2>&1 )
    echo "$(grep -cxF '→ backend-kit' "$T/se.txt") $(awk '/^→ /{f=($2=="backend-kit"); next} f && NF' "$T/se.txt" | grep -c .)"
    ( cd "$G" && python3 scripts/check-stale-values.py > "$T/sv.txt" 2>&1 ); echo "stale_rc=$? $(grep -cF -f <(printf '%s\n' "${FILES[@]}") "$T/sv.txt")" ;;
  DG-06)  # 사이클 검사 — 이 Phase 몫 줄만 본다. docs-site-regen 은 Final F2 몫
    python3 scripts/validate-post-kaizen.py --since "$B" --verbose > "$T/vpk.txt" 2>&1
    grep -E '\] . (scope-isolation|doc-contracts): ' "$T/vpk.txt" | awk '{print $5, $2}'
    # doc-contracts 가 검사한 경로 수와 그 가운데 이 Phase 파일 수 — FAIL 이 나도 이 Phase 몫인지 가른다
    python3 scripts/validate-doc-contracts.py -v 2>&1 | awk -F' → ' '/^ *검사: /{a=$1; sub(/^ *검사: /,"",a); sub(/:[0-9]+$/,"",a); print a; print $2}' | sort -u > "$T/dc.txt"
    echo "doc_checked=$(grep -c . "$T/dc.txt") doc_mine=$(comm -12 "$T/dc.txt" <(my) | grep -c .)"
    # 위반 커밋 목록을 읽은 수와 그 가운데 이 Phase 서명 커밋 수. 목록을 못 읽으면 둘째 값이 조용히 0 이 되므로 첫 값을 함께 본다
    awk '/ scope-isolation: /{f=1;next} /^\[ /{f=0} f&&/^ +[0-9a-f]{7,40}$/{print $1}' "$T/vpk.txt" > "$T/viol.txt"
    echo "violators=$(grep -c . "$T/viol.txt") mine=$(while read -r c; do git log -1 --format=%B "$c" | grep -qxF "$SIG" && echo "$c"; done < "$T/viol.txt" | grep -c .)" ;;
  *) echo "UNKNOWN $1"; return 2 ;;
  esac
}
```

```bash
#!/usr/bin/env bash
# new-warnings.sh <옛 파일> <새 파일> — 새 파일에서 더한 줄에 걸린 경고만 센다. 줄이 밀리므로 전체 수 차이로 세지 않는다
# 줄 번호는 경로 뒤 첫 번째 숫자다. 탐욕 매치(^[^ ]*:)로 뽑으면 열 번호가 줄 번호로 둔갑한다 (실측 2026-09-24)
# 린터가 안 돌면 경고 0 이 조용히 나온다 — 돌았다는 줄(Linting: 1 file)이 없으면 멈춘다 (실측 2026-09-25: 옆에 node_modules 가 없어 0)
set -u
DIR=$(cd "$(dirname "$0")" && pwd)
ADDED=$(git diff --no-index -U0 -- "$1" "$2" | awk '/^@@/{split($3,a,","); s=substr(a[1],2)+0; n=(a[2]==""?1:a[2]+0); for(i=0;i<n;i++) print s+i}' | sort -u)
OUT=$("$DIR/node_modules/.bin/markdownlint-cli2" --config "$DIR/cfg.markdownlint-cli2.jsonc" "$2" 2>&1)
printf '%s\n' "$OUT" | grep -q '^Linting: 1 file' || { echo "LINT_NOT_RUN $2"; exit 2; }
LINES=$(printf '%s\n' "$OUT" | grep -E ':[0-9]+(:[0-9]+)? (error|warning) ' | sed -E 's#^([^:]*):([0-9]+).*#\2#' | sort -u)
NEWW=$(comm -12 <(printf '%s\n' "$ADDED" | grep . | sort) <(printf '%s\n' "$LINES" | grep . | sort) | wc -l | tr -d ' ')
echo "total_warning_lines=$(printf '%s\n' "$LINES" | grep -c .) added_lines=$(printf '%s\n' "$ADDED" | grep -c .) new_warnings=$NEWW"
```

**예행.** 시작 커밋에서 레포를 스크래치로 복제해(`p7d/rehearse.sh`) BUILD 가 할 커밋을 흉내 냈다 — 봉인 커밋(이 계약 초안에 digest 를 적은 판) → 다른 Phase 서명 커밋 하나
(`design-kit/README.md`, 걸러져야 한다) → `mock.py` 를 적용한 구현 커밋 둘(`docs/backend/` 셋 · `backend-kit/` 여덟) → `end_sha` → notes 모의본 → `end_sha` 한 줄 더.
변형 넷은 같은 흐름에 커밋 하나를 더한다: `unsigned-shared`(서명 없이 루트 `README.md`) · `unsigned-mine`(서명 없이 `backend-kit/README.md`) ·
`signed-outside`(서명하고 `backend-kit/.claude-plugin/plugin.json`) · `cross-phase`(서명하고 `harness/skills/sprint/SKILL.md` 와 `backend-kit/skills/backend-test/SKILL.md` 한 커밋).

| 조건 | 예행 판 (요구값) | 시작 커밋 판 | 양성 · 음성 대조 |
| --- | --- | --- | --- |
| SK-01 | `1` 열셋 · `1 1` · `1` · `0.3.0 2026-09-25` | `0` 열셋 · `0 0` · `0` · `0.2.0 2026-08-13` | 문장 삭제 15 개 모두 떨어짐 |
| SK-02 | `1` 여덟 · `1 0` · `1` · `1 … 18` | `0` 여덟 · `0 1` · `0` · `1 … 17` | 문장 삭제 8 개 |
| SK-03 | `1` 일곱 · `1` · `1 … 19` | `0` 일곱 · `0` · `1 … 18` | 문장 삭제 7 개 |
| SK-04 | `1` 다섯 · `1` 넷 · `8 0` · `1 1` · `0 10` · `1` · `0` | `0` 다섯 · `0` 넷 · `6 0` · `0 0` · `1 10` · `0` · `1` | 문장 삭제 9 개 |
| SK-05 | `8 True backend-guide True True 4 1 1 1 1` · `rc=0 Total: 8 passed, 0 failed` · `1 0 1 0` | `7 True None False False 0 0 0 0 0` · `rc=0 Total: 7 passed, 0 failed` · `0 1 0 1` | 음성: 사례 8 assertion 하나의 type 을 `check` 로 → `rc=1 Total: 7 passed, 1 failed` · README 구조 검사 줄을 옛 문구로 → 셋째 줄 `1 0 0 1` · 문장 삭제 1 개 |
| SK-06 | `1/0 1/0 2/0 1/0 1/0` · `1 1 0` · `readme_history_same=1` | `0/1 0/1 0/1 0/1 0/1` · `0 0 1` · `readme_history_same=1` | 문장 삭제 2 개 · 옛 표기 줄 수가 양성 대조 |
| SK-07 | `0 1 1 1 1` · `0.1.1 2026-09-25` | `3 0 0 0 0` · `0.1.0 2026-04-04` | 문장 삭제 4 개 · 첫 값이 양성 대조 |
| SK-08 | `1 1 1 1` · `1 1` · `0` | `0 0 0 0` · `0 0` · `2` | 문장 삭제 4 개 · 셋째 값이 양성 대조 · Gotcha 16 새 문장을 옛 문장으로 → 둘째 줄 `1 0` |
| SK-09 | `1 1` · `1` 다섯 · `1` 여섯 · `1 1` · `1 1` · `1 1 1` · `1 1 1 1` · `0` | `0 0` · `0` 다섯 · `0` 여섯 · `0 0` · `0 0` · `0 0 0` · `1 1 1 1` · `9` | 문장 삭제 20 개 · 여덟째 값이 양성 대조 · reviewer 예시 행을 옛 문구로 → 여섯째 줄 `1 1 0` · 마지막 값 1 · Gotcha 11 본문을 옛 문구로 → 셋째 줄 첫 값 0 · 마지막 값 1 |
| SC-00 | `0` | — | 변형 `signed-outside` → 1 |
| ER-01 | `0` · `0` (새 쌍 열넷 전부 근거 파일에 있다 · notes 모의본의 URL 하나도 근거 파일에 있다) | — | database.md 끝에 `https://example.invalid/x` → `1` · `0` · notes 끝에 같은 URL → `0` · `1` · notes 를 지운 사본 → `0` · `NOTES_MISSING` |
| ER-02 | `0` (더한 줄 132) | — | backend-system 끝에 「이 값이 적용된다」 → 1 |
| ER-03 | `notes_committed=1` · `1` 열여섯 · `0` | — | 변형 `unsigned-shared` · `signed-outside` · `cross-phase` → 셋 다 1 · notes 에서 `infra-kit/README.md` 줄을 지운 사본 → 둘째 줄 여덟째 값 0 |
| AR-01 | `0` · `0 11` · `0` · `SEAL_OK` · `scope_same=1` · `1` | — | `unsigned-mine` ① 1 · `signed-outside` ② `1 11` · 조건 줄 한 글자 변조 ④ `SEAL_BROKEN` |
| AR-02 | `1 docs/backend/fundamentals/database.md 1` · `1 1` | `1 docs/backend/fundamentals/database.md 0` · `1 1` | 알려진 답 — 경로는 원래 맞고 제목만 새로 생긴다 |
| RE-02 | `docs/backend/fundamentals/database.md` 한 줄 | 0 줄 | — |
| AP-01 | `version=0.3.1 0` | `version=0.3.1 0` | README 끝에 「버전 0.3.1」 → 1 |
| AP-03 | `0` | `0` | README 끝에 펜스 한 줄 → 1 |
| AP-04 | `1/1` 다섯 | — | backend-guide `description: >` 한 글자 변경 → `1/1 0/1 1/1 1/1 1/1` · 음성은 DG-05 |
| DG-01 · DG-03 · DG-04 | `0` · `0` · `0` | — | DG-04: `a/b.dart` · `c.sh` · `d.md` → 2 |
| DG-02 | 열 줄 `new_warnings=0` · `json_ok` | — | 첫 초안 표 구분 줄 `\|---\|` → MD060 1 · database.md 끝 `#bad heading` → 2 · README 끝 `#bad heading` → 1 |
| DG-05 | `10 0` · `1 0` · `stale_rc=0 0` | — | `name:` 을 깬 사본 → `10 1` · `zz-test` 스킬을 더한 사본 → `1 1` · 가짜 줄 → 셋째 값 1 |
| DG-06 | `scope-isolation: PASS` · `doc-contracts: PASS` · `doc_checked=2 doc_mine=0` · `violators=0 mine=0` | — | 변형 `cross-phase` → `scope-isolation: FAIL` · `violators=1 mine=1` · 경로 목록에 이 Phase 파일 → `doc_mine=1` |

문장 삭제 사본(`p7d/del.sh`): SK-01 15 · SK-02 8 · SK-03 7 · SK-04 9 · SK-05 1 · SK-06 2 · SK-07 4 · SK-08 4 · SK-09 20 — 토큰 하나를 그 파일에서 한 번 지운 사본 70 개 모두
그 조건의 요구값 `1` 이 하나 이상 `0` 으로 떨어졌다(`DROP` 70 · `NODROP` 0 · `MISSING` 0).

## Skill

- [ ] SK-01: `docs/backend/fundamentals/database.md` 에 원칙 10 「시각은 종류부터 나누고, 종류마다 저장 형태를 정한다」 가 원칙 9 뒤 · `## 수치 기준` 앞에 있고, 세 종류(순간 · 받는 사람 지역을 따라가는 벽시계 · 특정 지역에 묶인 벽시계)의 표 · IANA 시간대 식별자 · `TIMESTAMPTZ` 가 원래 시간대를 남기지 않는다는 문장 · floating time · 서머타임 해석 · 시간대와 나라 상수 금지 · 나라 코드로 시간대를 정하지 않는다는 문장 · 그것이 RFC 가 아니라 킷 규칙이라는 문장 · 근거 URL 둘을 담으며, 안티패턴 표에 두 행이 더해지고 머리 설정이 `0.3.0` · `2026-09-25` 다 (backend-family:P2 — backend-kaizen Gotcha 2 가 요구하는 원칙 문서 선행) [exact, enumerated]
      (Given: 개정 파일 `end_sha:` 마지막 값이 정해진 뒤 · When: `type m >/dev/null || exit 2;` 뒤 `m SK-01` · Then: 네 줄이 `1 1 1 1 1 1 1 1 1 1 1 1 1 ` · `1 1 ` · `1` · `0.3.0 2026-09-25`.
       토큰 열다섯은 `회귀 게이트` 절 `m.sh` 의 `SK-01)` 갈래에 글자 그대로 있다. 봉인 전 실측: `회귀 게이트` 절 표)
- [ ] SK-02: `backend-kit/skills/backend-system/SKILL.md` 가 Gotcha 18 「시각은 종류부터 나누고 필드마다 표로 남겨라 (enforcement 등급 E2)」 로 규격 산출물에 시각 필드마다 네 칸(종류 · 저장 형태 · 시간대 출처 · 순간으로 바꾸는 규칙)을 요구하고, 세 종류 · IANA 시간대 식별자 · 서머타임으로 같은 시각이 두 번 오거나 없을 때의 처리 · 시간대 출처 칸이 킷 규칙이라는 문장 · `docs/backend/fundamentals/database.md` 원칙 10 가리킴 · RFC 5545 출처를 담으며, Gotcha 13 (c) 와 Step 2 `| API 규격 |` 행이 Gotcha 18 을 가리키고, Gotcha 번호가 1 ~ 18 로 이어진다 (새 Gotcha 를 가운데 끼워 번호로 서로 가리키는 Gotcha 13 · 16 · 17 을 밀지 않는다) (backend-family:P2) [exact, enumerated]
      (Given: SK-01 과 같다 · When: `m SK-02` · Then: 네 줄이 `1 1 1 1 1 1 1 1 ` · `1 0 ` · `1 ` · `1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18`. 둘째 줄 둘째 값은 옛 (c) 문구 `(c) **모든 timestamp 필드의` 가 0 이라는 뜻이다.
       봉인 전 실측: `회귀 게이트` 절 표)
- [ ] SK-03: `backend-kit/skills/backend-guide/SKILL.md` 가 Gotcha 19 「"UTC 로 통일하라" 전에 시각 종류부터 나눠라 (enforcement 등급 E1)」 로 세 종류를 먼저 나누게 하고, IANA 시간대 식별자 칸 · 한 나라나 한 시간대를 기본값으로 박은 설계 지적 · 「"표준 위반" 이라고 말하지 않는다」 · 원칙 10 가리킴을 담으며, Step 1 `| database |` 키워드 행에 `벽시계, 반복 일정, 시간대, 서머타임, 나라 코드` 가 붙고, Gotcha 번호가 1 ~ 19 로 이어진다 (backend-family:P2) [exact, enumerated]
      (측정: `type m >/dev/null || exit 2;` 뒤 `m SK-03` 세 줄이 `1 1 1 1 1 1 1 ` · `1 ` · `1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19`. 봉인 전 실측: `회귀 게이트` 절 표)
- [ ] SK-04: `backend-kit/skills/backend-audit/references/audit-criteria.md` §3 Database 표에 `| 시각 종류별 저장 |` 행(벽시계 뜻의 필드를 순간 하나로만 저장하면 FAIL · 특정 지역 벽시계에 IANA 시간대 식별자 칸이 없으면 FAIL · 필드의 뜻이 실제로 벽시계일 때만 판정 · RFC 5545 출처)과 `| 시간대·나라 상수 금지 |` 행(코드 상수 하나로 강제하면 FAIL · 한 지역 전용 서비스라고 밝혔으면 N/A · RFC 요구가 아니라 킷의 범위 예외)이 더해져 표가 끊기지 않은 여덟 줄이고, §2 `| Timestamp 직렬화 규칙 |` 행이 순간 필드로 좁혀져 벽시계 필드를 §3 행으로 넘기며 옛 문구 「모든 timestamp 응답 필드가」 는 0 이고, `## N. ` 카테고리 제목은 10 개 그대로이며, `backend-kit/skills/backend-audit/SKILL.md` Step 3 의 8 행 예시가 「순간 필드 전부」 로 바뀌고 「전 timestamp 필드」 는 0 이다 (backend-family:P2) [exact, enumerated]
      (Given: SK-01 과 같다 · When: `m SK-04` · Then: 일곱 줄이 `1 1 1 1 1 ` · `1 1 1 1 ` · `8 0` · `1 1 ` · `0 10` · `1 ` · `0`. 셋째 줄은 §3 절 안 `|` 로 시작하는 줄 수와 그 줄들 사이에 끊긴 곳이 있는지다.
       봉인 전 실측: `회귀 게이트` 절 표)
- [ ] SK-05: `backend-kit/evals/evals.json` 에 사례 8(skill `backend-guide`, prompt 에 `06:30` 과 `서울`, assertion 넷 — database.md 원칙 10 읽기 · 받는 사람 지역을 따라가는지 특정 지역에 묶였는지 먼저 나누기 · 벽시계를 `TIMESTAMPTZ` 같은 순간 하나로만 저장하지 않기 · 코드 기본값 시간대 지적)이 더해져 사례가 8 개 · id 1 ~ 8 이고, `$END` 판에서 `scripts/run-evals.py backend-kit` 이 종료 코드 0 · `Total: 8 passed, 0 failed` 이며, `backend-kit/README.md` 검증 절이 「평가 사례 8 개의 구조 검증」 · 「등록된 검사 전부 (개수는 `harness/docs/guides/plugin-validation-guide.md` 가 정한다)」 이고 옛 「7 스킬 assertion 전수 검증」 · 「7 카테고리 구조 감사」 는 0 이다 (backend-family:P2 · 처리 배정표 제안의 평가 사례 · 편집 전 감사 `README.md:54` — 검사는 V1 ~ V10 열 가지) [exact]
      (측정: `type m >/dev/null || exit 2;` 뒤 `m SK-05` 세 줄이 `8 True backend-guide True True 4 1 1 1 1` · `rc=0 Total: 8 passed, 0 failed` · `1 0 1 0`.
       셋째 줄은 README 의 새 문구 둘과 옛 문구 둘의 줄 수다 — 시작 커밋 판에서 `0 1 0 1`(양성 대조).
       음성 대조: 사례 8 의 assertion 하나의 `type` 을 `check` 로 바꾼 사본에서 둘째 줄이 `rc=1 Total: 7 passed, 1 failed`. 봉인 전 실측: `회귀 게이트` 절 표)
- [ ] SK-06: OAuth 2.1 인용 다섯 파일이 `draft-16` 으로 바뀌고 `draft-15` · `v2-1-15` 가 0 줄이다 — `backend-kit/skills/backend-system/SKILL.md` · `backend-kit/skills/backend-guide/SKILL.md` · `backend-kit/skills/backend-audit/SKILL.md` · `backend-kit/agents/backend-reviewer.md` · `backend-kit/evals/evals.json` 의 새 표기 수가 차례로 1 · 1 · 2 · 1 · 1 이고, backend-system 은 「`draft-ietf-oauth-v2-1-16` (2027-03-07 만료) 로 아직 Draft 임을 명시」, backend-guide 는 「2026-09-24 조회 기준 OAuth 2.1 은 `draft-ietf-oauth-v2-1-16` (Active Internet-Draft, 2027-03-07 만료)」 를 한 번씩 담고 옛 「expires 2026-09」 는 0 이다. 예외: `backend-kit/README.md` 의 2026-04-24 이력 한 줄과 `docs/backend/research-log.md` 는 이력이라 그대로 둔다 — README 그 줄이 편집 전과 같다 (근거 파일 §3) [exact, enumerated]
      (측정: `type m >/dev/null || exit 2;` 뒤 `m SK-06` 세 줄이 `1/0 1/0 2/0 1/0 1/0 ` · `1 1 0` · `readme_history_same=1`. 첫 줄 `/` 뒤 값이 옛 표기 줄 수다 — 시작 커밋 판에서 다섯 파일 모두 1(양성 대조).
       봉인 전 실측: `회귀 게이트` 절 표)
- [ ] SK-07: `docs/backend/fundamentals/api-design.md` 에 옛 값 `3.2.0` 이 0 개이고, 원칙 5 문장 「OpenAPI 3.2.1 스펙을 단일 소스로 유지한다」 · 출처 URL 둘(`https://spec.openapis.org/oas/latest.html` · `https://github.com/OAI/OpenAPI-Specification/releases/tag/3.2.1`) · 수치 기준 행 「| OpenAPI 최신 버전 | 3.2.1 (2026-09-10 공개」 가 한 번씩 있으며, 머리 설정이 `0.1.1` · `2026-09-25` 다 (근거 파일 §3 · 2026-09-06 REJECT 의 「한 자리만 고침」 재발 방지) [exact]
      (측정: `type m >/dev/null || exit 2;` 뒤 `m SK-07` 두 줄이 `0 1 1 1 1 ` · `0.1.1 2026-09-25`. 첫 값이 옛 값 줄 수다 — 시작 커밋 판에서 3(양성 대조). 봉인 전 실측: `회귀 게이트` 절 표)
- [ ] SK-08: `backend-kit/skills/backend-audit/references/audit-criteria.md` §8 `| CDC 파이프라인 |` 행이 「전달 보장은 at-least-once 다」 · 「consumer idempotency 가 함께 있어야 PASS」 · `write-path-integrity-protocol.md` §6 가리킴 · microservices.io 출처를 담고, `backend-kit/skills/backend-audit/SKILL.md` Gotcha 16 이 「outbox 나 outbox+CDC 조합을 근거로 exactly-once 를 PASS 시키지 마라」 로 시작하며 CDC 행도 같은 기준으로 판정한다고 적고, `backend-kit/` 전체에 「exactly-once 보장 가능」 이 0 줄이다 (2026-08-13 research-log 미반영 항목) [exact]
      (측정: `type m >/dev/null || exit 2;` 뒤 `m SK-08` 세 줄이 `1 1 1 1 ` · `1 1 ` · `0`. 셋째 값은 시작 커밋 판에서 2(양성 대조 — CDC 행과 Gotcha 16). 봉인 전 실측: `회귀 게이트` 절 표)
- [ ] SK-09: backend-kit 의 `[미검증]` 표기가 설계 가이드 §3.7 3 항 · agent-design-guide §10 정책 2 항과 같은 네 칸(막는 것 · 시도한 우회 · 통제 불가 사유 · 재검증 명령)을 쓴다 — (a) `backend-kit/skills/backend-test/SKILL.md` Gotcha 13 과 `### Step 5: 실행 검증` 의 증거 규칙 (b) `backend-kit/skills/backend-audit/SKILL.md` Gotcha 11 본문과 예시 · Gotcha 12 · DB 엔진 문단 (c) `backend-kit/skills/backend-audit/references/audit-criteria.md` §2 소비면 정합성 행 · §3 정적 대체 판정 규약 (d) `backend-kit/agents/backend-reviewer.md` `## 출력 포맷` 의 규칙 줄과 예시 4 행. 가이드의 네 칸 이름이 이 킷이 쓰는 이름과 같고(알려진 답), `backend-kit/` 전체에 옛 표기 여섯(`[미검증] <사유>` · `` `[미검증]` + 사유 `` · 「pool 설정 파일 정적 리뷰만 수행」 · `` `[미검증]` 태그 + 이유 `` · 「근거에 이유를 기술하라」 · 「4 요건 충족(호출 로그」)이 0 줄이다 (Phase 1 가이드 1.6.0 의 반대편 — 오케스트레이터 Step 7 전수 감사) [exact, enumerated]
      (Given: SK-01 과 같다 · When: `m SK-09` · Then: 여덟 줄이 `1 1 ` · `1 1 1 1 1 ` · `1 1 1 1 1 1 ` · `1 1 ` · `1 1 ` · `1 1 1 ` · `1 1 1 1 ` · `0`. 일곱째 줄이 가이드 §3.7 의 네 칸 줄(`   - **막는 것** —` 등)이고, 여덟째 값은 시작 커밋 판에서 9(양성 대조 — Gotcha 11 은 옛 표기 둘이 한 줄에 있어 줄 수로는 9).
       봉인 전 실측: `회귀 게이트` 절 표)

## Script

- [ ] SC-00: N/A (Script 카테고리는 `release.sh` 연동 · 버전 올림 · `marketplace.json` 갱신이다. 이 Phase 는 그 파일을 건드리지 않는다 — 공유 파일은 Final 몫. 측정: `type my >/dev/null || exit 2;` 뒤 `my | grep -cE '^(scripts/release\.sh|\.claude-plugin/marketplace\.json|[^/]+/\.claude-plugin/plugin\.json)$'` 이 0. 양성 대조: 예행 변형 `signed-outside` 에서 1)

## Error

- [ ] ER-01: 열한 파일에 새로 생긴 URL 과 `.harness/.meta/kaizen-0924/phase7-notes.md` 의 URL 이 전부 이 Phase 의 외부 근거 파일 `.harness/.meta/evidence/phase7.md` 에 있다 — 열한 파일은 파일마다 편집 전 판과 비교한다 (러닝북 — notes 킷 로그 한 단락의 출처 URL 은 근거 파일에서만) [exact, enumerated]
      (측정: `type m >/dev/null || exit 2;` 뒤 `m ER-01` 두 줄이 `0` · `0`. 첫 줄은 열한 파일을 파일마다 비교해 다른 파일에 이미 있던 URL 을 새로 더한 경우도 본다. 둘째 줄은 notes 의 URL 전부이고, notes 가 `$END` 판에 없으면 `NOTES_MISSING` 이라 FAIL 이다.
       봉인 전 실측: 예행 판의 새 (파일, URL) 쌍 열넷 — database.md · backend-system · audit-criteria 가 RFC 5545 · PostgreSQL 둘씩, backend-guide 가 RFC 5545 하나, api-design.md 가 OpenAPI 둘, research-log 가 다섯 — 이 전부 근거 파일에 있어 첫 줄 0. notes 모의본의 URL 하나(RFC 5545)도 근거 파일에 있어 둘째 줄 0.
       양성 대조: 예행 판 database.md 끝에 `https://example.invalid/x` 를 더하면 첫 줄 1, notes 끝에 같은 URL 을 더하면 둘째 줄 1, notes 를 지운 사본에서 둘째 줄 `NOTES_MISSING`)
- [ ] ER-02: 열한 파일에 더한 줄에 번역투 6 종(`tone-kit/references/locale-korean.md` §2 치환표의 grep 열)이 0 건이다 [exact]
      (측정: `type m >/dev/null || exit 2;` 뒤 `m ER-02` 가 0. 봉인 전 실측: 예행 판 더한 줄 132 개에서 0. 양성 대조: backend-system 끝에 「이 값이 적용된다」 를 더하면 1)
- [ ] ER-03: 이 Phase 범위 밖 반대편을 명시적 미완으로 넘기고 건드리지 않는다 — `.harness/.meta/kaizen-0924/phase7-notes.md` 가 `$END` 에 커밋돼 있고 열여섯 문자열(처리 배정표 키 `backend-family:P2` · 넘김 `rust-model` (Phase 9 — SQLx 와 SeaORM 의 순간 타입이 다르다는 근거 파일 §2 · `:90` 입력 표) · `docs/backend-kit/database.html` · `docs/backend-kit/api-design.html` (Final F2) · `.harness/stale-values.yaml` (Final — `3.2.0` → `3.2.1` 등록) · `.claude/skills/backend-kaizen/SKILL.md` (다음 사이클 — Gotcha 6 형제 대칭 표에 시각 종류 항목) · `plugin.json` (Final — 버전) · `infra-kit/README.md` (Phase 8 — 검증 절의 같은 「7 카테고리 구조 감사」 줄) · `OpenAPI 3.1` (열린 질문) · `F20` (Phase 11) 과 러닝북이 적게 한 절 머리 `## 반영한 처리 배정표 키` · `## 미반영 키와 사유` · `## 넘기는 것` · `## changelog 한 단락` · `## 킷 로그 한 단락` · `## 다음 사이클 메모`)을 각각 1 회 이상 담고, 구간 안에서 공유 파일 · 다른 Phase 파일을 건드린 커밋 가운데 다른 Phase 서명이 없는 커밋이 0 개다 [exact, enumerated]
      (Given: BUILD 가 notes 를 커밋하고 개정 파일에 그 sha 로 `end_sha:` 를 덧붙인 뒤 · When: `type m >/dev/null || exit 2; type not_other >/dev/null || exit 2;` 뒤 `m ER-03` · Then: 세 줄이 `notes_committed=1` · `1` 열여섯 개 · `0`.
       셋째 값의 경로는 `m.sh` `ER-03)` 갈래의 `not_other` 인자 열넷이다 — 서명 줄 목록이 아니라 경로로 직접 세므로 서명을 빠뜨린 커밋도 보인다. 다른 Phase 서명이 달린 커밋은 그 Phase 몫이라 뺀다.
       봉인 전 실측: 예행 판 `notes_committed=1` · 열여섯 모두 1 · 0. 양성 대조: 변형 `unsigned-shared` 1 · `signed-outside` 1 · `cross-phase` 1. 예행의 다른 Phase 서명 커밋(`design-kit/README.md`)은 인자 밖이라 0 에 영향이 없다)

## Architecture

- [ ] AR-01: 이 Phase 의 변경이 허용 경로 안에 머물고, 범위 선언 블록이 그 경로와 같으며, 이 계약이 봉인돼 있다 [exact, enumerated]
      (Given: BUILD 가 개정 파일에 `end_sha:` 를 적은 뒤 · 이 Phase 커밋 메시지마다 서명 줄 `Kaizen-Phase: kaizen-0924-p07-backend-kit` · When: `type m >/dev/null || exit 2; type unsigned_on >/dev/null || exit 2; type verify_seal >/dev/null || exit 2;` 뒤 `m AR-01` · Then: 여섯 줄이 —
       ① `0` — `backend-kit/` · `docs/backend/` 를 건드린 구간 안 커밋이 전부 서명했다(이 구간에 두 폴더를 고칠 수 있는 Phase 는 7 하나다)
       ② `0 11` — 서명 커밋이 건드린 `.harness/` 밖 경로 가운데 열한 파일 밖이 0 개, 열한 파일이 전부 있다
       ③ `0` — `harness/references/contract-schema.md` §`.harness/` 범위 조건 의 권장 형태로 `.harness/` 의 계약 전부에 `verify_seal` 을 돌려 이 Phase 몫 `SEAL_BROKEN` 이 0 개
       ④ `SEAL_OK` — `$END` 판의 이 계약이 봉인돼 있다(`SEAL_ABSENT` 는 봉인을 건너뛴 것이라 FAIL)
       ⑤ `scope_same=1` — `## 범위 경계` 절 `# sprint-scope` 블록의 `.harness/` 밖 줄이 `FILES` 열한 줄과 같다 ⑥ `1` — 그 블록에 `.harness/` 줄이 하나 있다.
       봉인 전 실측: 예행 판 `0` · `0 11` · `0` · `SEAL_OK` · `scope_same=1` · `1`. 양성 대조: 변형 `unsigned-mine` ① 1 · 변형 `signed-outside` ② `1 11` · 조건 줄 한 글자를 바꾼 사본 ④ `SEAL_BROKEN`)
- [ ] AR-02: 새 원칙과 바뀐 기준이 그것을 읽는 쪽에 닿는다 — (a) `backend-kit/skills/backend-guide/references/principle-index.md` 의 `| Database |` 행이 한 줄이고 그 상대 경로를 풀면 `docs/backend/fundamentals/database.md` 이며 그 파일에 `### 10. 시각은` 제목이 있다 (b) SK-08 이 가리키는 `backend-kit/references/write-path-integrity-protocol.md` 에 `## 6. Outbox 는 at-least-once 다` 제목이 있다 (c) 감사 기준을 읽는 `backend-kit/agents/backend-reviewer.md` 의 정본 줄 「- backend-kit/skills/backend-audit/references/audit-criteria.md — 10 카테고리 기존 rule」 이 그대로라 새 행이 따로 옮겨 적지 않아도 평가에 들어간다 (Counterpart — 소비면 셋) [exact, enumerated]
      (측정: `type m >/dev/null || exit 2;` 뒤 `m AR-02` 두 줄이 `1 docs/backend/fundamentals/database.md 1` · `1 1`. 알려진 답: 시작 커밋 판은 경로는 같고 제목이 없어 `1 docs/backend/fundamentals/database.md 0` · `1 1`)

## Anti-patterns

- [ ] AP-01: 버전을 하드코딩하지 않는다 — plugin.json에서 읽어야 한다. 이번 변경에 적용: 열한 파일에 더한 줄에 backend-kit `plugin.json` 의 `version` 값(`$END` 판에서 읽는다)이 0 건이다 — 이 Phase 는 킷 버전을 적지 않고 Final 이 올린다 [exact]
      (측정: `type m >/dev/null || exit 2;` 뒤 `m AP-01` 이 `version=0.3.1 0` (버전 값은 `$END` 판 plugin.json 에서 읽은 것 — 이 Phase 가 plugin.json 을 건드리지 않으므로 0.3.1). 양성 대조: README 끝에 「버전 0.3.1」 을 더하면 `version=0.3.1 1`)
- [ ] AP-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수 (```` ```text, ```bash, ```yaml ```` 등). 판정 권위는 validate-plugin V6 상태기계다 — 여는/닫는 fence 가 동형이라 줄 단위 정규식으로는 판정 불가. 이번 변경에 적용: 이 Phase 는 코드 펜스를 더하지 않는다 — 열한 파일에 더한 줄 가운데 펜스 줄이 0 이고, backend-kit 쪽은 DG-05 의 V6 가 함께 본다 [exact]
      (측정: `type m >/dev/null || exit 2;` 뒤 `m AP-03` 이 0. 양성 대조: README 끝에 펜스 한 줄을 더하면 1)
- [ ] AP-04: SKILL.md / agents/*.md frontmatter 에서 name 필드 누락 — validate-plugin V1 FAIL. 이번 변경에 적용: 고친 SKILL.md 넷과 backend-reviewer 의 첫 frontmatter 블록이 편집 전과 글자 그대로 같고 `name: <폴더 또는 파일 이름>` 줄이 1 개씩이다 — 그래서 README AUTO 구간과 트리거 설명이 읽는 값도 바뀌지 않는다 [exact]
      (측정: `type m >/dev/null || exit 2;` 뒤 `m AP-04` 가 `1/1 1/1 1/1 1/1 1/1 `. 양성 대조: 예행 판 backend-guide 의 `description: >` 줄 한 글자를 바꾼 사본에서 `1/1 0/1 1/1 1/1 1/1 `. 음성 대조는 DG-05 — `name:` 을 깨면 V1 이 FAIL)

## Reusability

- [ ] RE-01: N/A (재사용 단위 코드 — 컴포넌트 · 함수 · 모듈 — 가 없다. 변경 파일이 문서 · 평가 사례 데이터뿐이다. 측정: `printf '%s\n' "${FILES[@]}" | grep -cvE '\.(md|json)$'` 이 0)
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다. 이번 변경에 적용: 시각 원칙 본문은 한 곳(`docs/backend/fundamentals/database.md` 원칙 10)에만 두고 두 스킬 Gotcha 와 감사 기준은 그곳을 가리킨다 — 세 종류 표 머리 줄 「| 시각 종류 | 예 | 저장 형태 (PostgreSQL) | 순간이 필요할 때 |」 가 `backend-kit/` · `docs/backend/` 에서 그 파일 하나에만 있다. outbox 판정도 새로 쓰지 않고 `write-path-integrity-protocol.md` §6 을 가리킨다(SK-08) [exact]
      (측정: `type m >/dev/null || exit 2;` 뒤 `m RE-02` 출력이 `docs/backend/fundamentals/database.md` 한 줄)

## Diagnostics

- [ ] DG-01: N/A (`commands.analyze` 는 `bash -n scripts/release.sh` 라 `scripts/release.sh` 만 잰다 — 이번 변경 파일과 교집합 0 개. 측정: `type my >/dev/null || exit 2;` 뒤 `my | grep -c '^scripts/release.sh$'` 이 0. 실제 검사는 DG-02 · DG-05)
- [ ] DG-02: IDE diagnostics 워닝/인포 0개 (`diagnostics.ide_exclude` 값 `[]`) — 이번 변경에 적용: 편집기 마크다운 확장과 같은 조건(markdownlint-cli2 0.23.2 · MD013 끔)으로 마크다운 열 파일의 **더한 줄**에 걸린 경고가 0 이고, `backend-kit/evals/evals.json` 이 JSON 으로 읽힌다. 편집 전부터 있던 경고는 `범위 경계` 절에 적은 대로 범위 밖이다 [exact]
      (측정: `type m >/dev/null || exit 2;` 뒤 `m DG-02` 의 열 줄이 모두 `new_warnings=0` 으로 끝나고 `LINT_NOT_RUN` 줄 0 · 마지막 줄 `json_ok`.
       봉인 전 실측: 예행 판 열 줄 `new_warnings=0` (더한 줄 29 · 5 · 59 · 4 · 3 · 6 · 6 · 3 · 2 · 2) · `json_ok`.
       양성 대조: 첫 초안의 database.md 새 표 구분 줄 `|---|` 꼴이 MD060 으로 `new_warnings=1` 을 냈다 — 그래서 `| --- |` 꼴로 고쳤다. database.md 끝에 `#bad heading` 을 더하면 `new_warnings=2`)
- [ ] DG-03: N/A (`commands.test` 는 `bash scripts/release.sh 2>&1 || true` 라 `scripts/release.sh` 만 잰다 — 교집합 0 개. 측정: DG-01 과 같은 명령 `type my >/dev/null || exit 2;` 뒤 `my | grep -c '^scripts/release.sh$'` 이 0. 실제 시험은 SK-05 · DG-05)
- [ ] DG-04: N/A (구동할 앱 · 서버가 없다 — 변경이 문서와 평가 사례 데이터뿐이다. 측정: `type my >/dev/null || exit 2;` 뒤 `my | grep -cE '\.(dart|ts|tsx|js|rs|go|py|sh)$'` 이 0. 양성 대조: 같은 `grep -cE` 에 `a/b.dart` · `c.sh` · `d.md` 세 줄을 넣으면 2)
- [ ] DG-05: 저장소 검사가 이 킷을 문제로 가리키지 않는다 — `$END` 판을 git 저장소로 만든 사본에서 (a) `scripts/validate-plugin.py backend-kit` 출력에 `V1` ~ `V10` 열 줄이 있고 하나도 `ERROR` · `FAIL` 이 아니다 (b) `scripts/sync-evals.py --check-only` 출력에 `→ backend-kit` 머리 줄이 있고 그 아래 어긋남 줄이 0 이다 (c) `scripts/check-stale-values.py` 가 종료 코드 0 또는 1 이고 출력에 열한 파일 경로가 0 건이다. 킷 전체를 보는 검사는 이 킷 몫의 줄만 센다 — 같은 구간에 다른 Phase 가 올린 변경 때문에 떨어지지 않게 한다(`harness/references/contract-schema.md` §검사 스크립트 전체 통과를 조건으로 걸지 마라). `sync-docs.py` 는 넣지 않는다 — backend-kit README 에 AUTO 구간이 없어 이 킷에서는 떨어질 수 없는 검사다. README AUTO 구간이 읽는 frontmatter 가 그대로인지는 AP-04 가 잰다 [exact]
      (측정: `type m >/dev/null || exit 2;` 뒤 `m DG-05` 세 줄이 `10 0` · `1 0` · `stale_rc=0 0` (stale_rc 는 0 또는 1).
       봉인 전 실측: 예행 판 `10 0` · `1 0` · `stale_rc=0 0`. 음성 대조: backend-guide 의 `name: backend-guide` 를 `nam:` 으로 깬 사본에서 첫 줄 `10 1`.
       양성 대조: `backend-kit/skills/zz-test/SKILL.md` 를 더한 사본에서 둘째 줄 `1 1` (`MISSING: zz-test`) · 출력에 `docs/backend/research-log.md` 가 든 가짜 줄을 넣으면 셋째 값 1)
- [ ] DG-06: `python3 scripts/validate-post-kaizen.py --since 79258900de00e621412e4c436b44028a77d7fb64` 출력의 `scope-isolation` · `doc-contracts` 줄이 `FAIL` · `ERROR` 가 아니다. `docs-site-regen` 은 Final F2 몫이라 판정에서 뺀다. 다른 Phase 커밋 때문에 `scope-isolation` 이 FAIL 이면 `--verbose` 위반 커밋 목록을 1 개 이상 읽었고 그 가운데 서명 줄 커밋이 0 개일 때, `doc-contracts` 가 FAIL · ERROR 이면 `validate-doc-contracts.py -v` 가 검사한 경로를 1 개 이상 읽었고 그 가운데 이 Phase 서명 커밋이 건드린 경로가 0 개일 때 이 조건은 PASS 다 — 둘 다 근거에 다른 Phase 몫이라고 적는다 [exact]
      (Given: 작업 폴더에서 `$END` 이후 커밋이 있어도 된다 — 검사는 `HEAD` 까지 보지만 판정은 이 Phase 서명 커밋만 센다 · When: `type m >/dev/null || exit 2;` 뒤 `m DG-06` · Then: 네 줄이 `scope-isolation: PASS` · `doc-contracts: PASS` · `doc_checked=N doc_mine=0` · `violators=V mine=0` 이고 N 이 1 이상. 위 가르기로 PASS 를 줄 때만 첫 두 줄에 `FAIL` 이 있어도 되며, scope-isolation 이 `FAIL` 이면 V 가 1 이상이어야 한다(목록을 못 읽으면 mine 이 조용히 0 이 되므로).
       봉인 전 실측: 예행 판 `PASS` · `PASS` · `doc_checked=2 doc_mine=0` · `violators=0 mine=0`. 양성 대조: 변형 `cross-phase` 에서 `scope-isolation: FAIL` · `violators=1 mine=1`, 검사 경로 목록에 `docs/backend/research-log.md` 를 넣은 사본에서 `doc_mine=1`)
