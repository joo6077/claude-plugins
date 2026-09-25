---
phase: 7
title: "Phase 7 backend-kit — 확보된 외부 근거"
collected: 2026-09-24
method: codex (foreground, 직접 호출 · gpt-5.6-sol · 조회는 curl/gh)
inputs: 처리 배정표(.claude/kaizen-input/insights-report.md)의 Phase 7 행 · phase-research-templates.md Phase 7 필수 출처 · 현행화 점검
note: 이 파일이 이 Phase 의 유일한 외부 근거다. 바깥 자료를 새로 찾지 마라. 여기 없는 URL·수치를 지어내지 마라. 없으면 미반영으로 남긴다.
---

## 1. 출처 목록

실제로 조회한 자료만 기재한다.

1. [RFC 5545 §3.3.5 — DATE-TIME](https://www.rfc-editor.org/rfc/rfc5545.html#section-3.3.5)
2. [PostgreSQL — Date/Time Types](https://www.postgresql.org/docs/current/datatype-datetime.html)
3. [Chrono `DateTime`](https://docs.rs/chrono/latest/chrono/struct.DateTime.html)
4. [Chrono `NaiveTime`](https://docs.rs/chrono/latest/chrono/naive/struct.NaiveTime.html)
5. [Chrono `NaiveDateTime`](https://docs.rs/chrono/latest/chrono/naive/struct.NaiveDateTime.html)
6. [SQLx PostgreSQL type mappings](https://docs.rs/sqlx/latest/sqlx/postgres/types/index.html)
7. [SeaORM 2.0 column types](https://www.sea-ql.org/SeaORM/docs/generate-entity/column-types/)
8. [OpenAPI Specification 최신판 3.2.1](https://spec.openapis.org/oas/latest.html)
9. [OpenAPI 3.2.1 release](https://github.com/OAI/OpenAPI-Specification/releases/tag/3.2.1)
10. [AsyncAPI 3.0.0 specification](https://www.asyncapi.com/docs/reference/specification/v3.0.0)
11. [AsyncAPI 3.1.0 release](https://github.com/asyncapi/spec/releases/tag/v3.1.0)
12. [RFC 9700 — OAuth 2.0 Security BCP](https://www.rfc-editor.org/rfc/rfc9700.html)
13. [OAuth 2.1 최신 Internet-Draft](https://datatracker.ietf.org/doc/draft-ietf-oauth-v2-1/)
14. [microservices.io — Transactional Outbox](https://microservices.io/patterns/data/transactional-outbox.html)
15. [SeaORM 2.0.0 release와 1.x 마이그레이션 주의사항](https://github.com/SeaQL/sea-orm/releases/tag/2.0.0)
16. [SeaORM 2.0.3 release](https://github.com/SeaQL/sea-orm/releases/tag/2.0.3)
17. [Chrono 0.4.45 release](https://github.com/chronotope/chrono/releases/tag/v0.4.45)

필수 소스 표에서는 OpenAPI, AsyncAPI, RFC 9700, Transactional Outbox의 4건을 실제 조회했다.

## 2. 항목별 관찰 사실

### backend-family:P2 — 시각 종류 구분

확인된 사실:

- RFC 5545는 DATE-TIME을 세 형태로 구분한다.

  - UTC 절대 시각: `19980119T070000Z`
  - 시간대 없는 지역 시각, 즉 floating time: `19980118T230000`
  - 특정 시간대에 묶인 지역 시각: `TZID=America/New_York:19980119T020000`

  [RFC 5545 §3.3.5](https://www.rfc-editor.org/rfc/rfc5545.html#section-3.3.5)

- Floating time은 관찰 중인 시간대와 관계없이 같은 시·분·초를 뜻한다. 수신자는 이를 “현재 그 수신자가 있는 시간대”에 고정된 것으로 해석해야 한다. 따라서 서로 다른 시간대의 수신자는 서로 다른 UTC 순간에 참여할 수 있다. [RFC 5545 §3.3.5](https://www.rfc-editor.org/rfc/rfc5545.html#section-3.3.5)

- RFC는 동시에 “floating time은 그것이 합리적인 동작일 때만 사용해야 한다”고 제한하고, 대부분의 경우에는 UTC 또는 로컬 시각+시간대 참조로 고정 시각을 전달하라고 한다. [RFC 5545 §3.3.5](https://www.rfc-editor.org/rfc/rfc5545.html#section-3.3.5)

- PostgreSQL의 `TIMESTAMPTZ`는 입력 시간대를 UTC로 변환해 저장하지만, 원래 명시되거나 추정된 시간대 자체는 보존하지 않는다. 반면 `TIMESTAMP`는 시간대 표시를 무시하고 날짜·시간 필드만 저장한다. [PostgreSQL Date/Time Types](https://www.postgresql.org/docs/current/datatype-datetime.html)

결론:

- “결제·생성 시각 같은 한 순간은 UTC 순간으로 둔다”는 근거와 맞는다.
- “반복 일정·영업시간·알람은 모두 시간대 없이 저장한다”는 문장은 RFC보다 범위가 넓다.
- 수신자 지역을 따라가는 `매일 06:30`은 floating으로 표현할 수 있지만, 서울 지점 영업시간처럼 특정 지역의 DST/법정시각을 따라야 하는 값은 로컬 시각과 `Asia/Seoul` 같은 시간대 식별자를 함께 보존해야 한다.
- 따라서 실무 계약에서는 이분법보다 다음 세 의미를 구분하는 것이 안전하다.

  1. 순간
  2. 수신자 지역을 따라가는 floating 벽시계
  3. 특정 지역에 고정된 벽시계+시간대

### 나라·시간대를 설정값으로 받는 규칙

- RFC 5545는 floating 값을 수신자의 시간대로 해석하는 동작과 `TZID`를 통한 특정 시간대 참조를 정의한다. 그러나 시간대를 “사용자 설정·기기·요청 값 중 어디서 받아야 하는지”, “저장할지 요청마다 받을지”는 규정하지 않는다. [RFC 5545 §3.3.5](https://www.rfc-editor.org/rfc/rfc5545.html#section-3.3.5)
- RFC 5545는 나라 코드에 관한 저장·입력 정책도 제공하지 않는다.

추론: 코드에 한 나라 또는 시간대를 무조건 박으면 다지역 사용자와 DST 규칙을 표현하지 못하므로 금지하는 방향은 타당하다. 다만 이것은 RFC 5545의 직접 요구가 아니라 제품 계약·구성 관리 규칙으로 명시해야 한다.

추론: 나라 코드만으로 시간대를 결정하지 말고 `country`와 IANA 시간대 식별자를 별도 계약 필드로 취급하는 편이 안전하다. 한 나라에 여러 시간대가 있을 수 있고, 국가와 무관한 사용자 선호 시간대도 존재하기 때문이다.

### backend-system 및 backend-guide 추가 문단

제안 문단의 취지는 타당하지만 아래와 같이 좁혀야 한다.

- “벽시계 시각은 시간대 없이 저장” 대신 “벽시계 값 자체는 시간대 없는 값으로 표현하되, 특정 지역에 고정된 일정이면 시간대 식별자를 별도 보존한다.”
- “알림처럼 순간이 필요할 때 받는 사람의 시간대로 계산”은 floating 일정에만 적용한다.
- 특정 지점 영업시간이나 특정 지역 행사에는 일정이 묶인 시간대를 적용해야 한다.
- DST 중복·누락 시각의 해소 정책도 계약에 있어야 한다. RFC 5545는 중복 시 첫 번째 발생, 존재하지 않는 시각에는 전환 전 오프셋을 사용하는 해석을 정의한다. [RFC 5545 §3.3.5](https://www.rfc-editor.org/rfc/rfc5545.html#section-3.3.5)

### audit-criteria Database 행

“벽시계 시각을 순간으로만 저장하면 실패”는 의미 보존 관점에서 근거가 있다. 다만 아래 조건을 함께 넣어야 오탐을 피할 수 있다.

- 해당 필드의 도메인 의미가 실제로 벽시계일 때만 판정한다.
- 특정 지역 고정 벽시계는 `TIME`/`TIMESTAMP` 외에 시간대 식별자가 보존되어야 한다.
- 모든 반복 일정을 bare `TIME`/`TIMESTAMP`로만 저장하도록 강제하면 오히려 고정 지역 일정을 잘못 모델링할 수 있다.
- 단일 지역 서비스의 N/A 예외는 RFC 요구가 아니라 이 킷의 명시적 제품 범위 예외다.

### rust-model 타입 대응

확인된 타입 대응:

| 의미 | Chrono/SQLx | PostgreSQL |
|---|---|---|
| 순간 | `chrono::DateTime<Utc>` | `TIMESTAMPTZ` |
| 날짜+벽시계 | `chrono::NaiveDateTime` | `TIMESTAMP` |
| 시각만 있는 벽시계 | `chrono::NaiveTime` | `TIME` |

이 매핑은 [SQLx PostgreSQL type mappings](https://docs.rs/sqlx/latest/sqlx/postgres/types/index.html)에서 직접 확인된다. Chrono도 `DateTime`을 시간대가 있는 ISO 8601 날짜·시각으로, `NaiveDateTime`과 `NaiveTime`을 시간대 없는 값으로 설명한다. [DateTime](https://docs.rs/chrono/latest/chrono/struct.DateTime.html), [NaiveDateTime](https://docs.rs/chrono/latest/chrono/naive/struct.NaiveDateTime.html), [NaiveTime](https://docs.rs/chrono/latest/chrono/naive/struct.NaiveTime.html)

반대 근거/주의점:

- SeaORM 2.0 공식 매핑표는 PostgreSQL `timestamp with time zone`의 Entity 타입으로 `DateTimeWithTimeZone`, 즉 `chrono::DateTime<FixedOffset>`를 제시한다.
- 같은 표에서 `DateTimeUtc`는 SeaORM `Timestamp` 행에 있지만 PostgreSQL 대응은 `N/A`로 표시되어 있다. [SeaORM column types](https://www.sea-ql.org/SeaORM/docs/generate-entity/column-types/)

따라서 `DateTime<Utc> + TIMESTAMPTZ`를 SQLx와 SeaORM에 공통으로 단정하면 안 된다.

추론: rust-model 문장은 다음처럼 스택별로 나누는 것이 안전하다.

- SQLx: 순간=`DateTime<Utc>`+`TIMESTAMPTZ`
- SeaORM Entity: 순간=`DateTimeWithTimeZone`/`DateTime<FixedOffset>`+`TimestampWithTimeZone`; 필요하면 도메인 경계에서 UTC로 정규화
- 양쪽 공통: 벽시계=`NaiveTime`/`NaiveDateTime`+`TIME`/`TIMESTAMP`

### 기존 Phase 7 근거의 재확인

- RFC 9700은 2025년 1월 발행된 BCP 240이며, public client의 PKCE 사용을 의무화하고 authorization server의 PKCE 지원을 의무화한다. ROPC는 사용하면 안 되며, implicit grant는 토큰 노출·재생 위험 때문에 사용하지 말도록 한다. [RFC 9700](https://www.rfc-editor.org/rfc/rfc9700.html)
- Transactional Outbox는 비즈니스 변경과 outbox 기록을 한 DB 트랜잭션에 넣고 별도 relay가 발행하는 패턴이다. relay가 동일 메시지를 여러 번 발행할 수 있으므로 consumer idempotency가 필요하고, 같은 aggregate를 여러 인스턴스가 변경할 때도 순서 보존을 고려해야 한다. [microservices.io](https://microservices.io/patterns/data/transactional-outbox.html)
- AsyncAPI 3.0.0은 receiver 문서를 sender 문서로부터 파생하는 것을 권장하지 않는다고 명시한다. 현재 양면 계약 규칙의 근거와 일치한다. [AsyncAPI 3.0.0](https://www.asyncapi.com/docs/reference/specification/v3.0.0)

## 3. 현행화 — 낡은 곳

| 파일:줄 | 현재 값 | 최신 확인값 | 판단·출처 |
|---|---|---|---|
| `backend-kit/skills/backend-system/SKILL.md:26` | OAuth 2.1 `draft-15`, 2026-09-03 만료 | `draft-16`, 2027-03-07 만료 | 명백히 낡음. 여전히 Active Internet-Draft이며 최종 RFC가 아니다. [Datatracker](https://datatracker.ietf.org/doc/draft-ietf-oauth-v2-1/) |
| `backend-kit/skills/backend-guide/SKILL.md:24` | `draft-15`, 2026-09 만료 | `draft-16`, 2027-03-07 만료 | 명백히 낡음. [Datatracker](https://datatracker.ietf.org/doc/draft-ietf-oauth-v2-1/) |
| `backend-kit/agents/backend-reviewer.md:62` | OAuth 2.1 draft-15 | draft-16 | 버전명 낡음. [Datatracker](https://datatracker.ietf.org/doc/draft-ietf-oauth-v2-1/) |
| `backend-kit/skills/backend-audit/SKILL.md:89` | OAuth 2.1 draft-15 | draft-16 | 버전명 낡음. [Datatracker](https://datatracker.ietf.org/doc/draft-ietf-oauth-v2-1/) |
| `backend-kit/README.md:59` | OAuth 2.1 draft-15 | draft-16 | 리서치 이력이라면 역사적 값으로 유지 가능하나, 현행 기능 목록이라면 낡음. [Datatracker](https://datatracker.ietf.org/doc/draft-ietf-oauth-v2-1/) |
| `backend-kit/skills/backend-system/SKILL.md:27` | AsyncAPI 3.0.0 | 최신 안정 3.1.0 | 3.0.0이 폐기됐다는 근거는 없지만 최신판 표기는 아님. 3.1.0의 확인된 추가 기능은 ROS 2 binding이다. [3.1.0 release](https://github.com/asyncapi/spec/releases/tag/v3.1.0) |
| `backend-kit/skills/backend-audit/references/audit-criteria.md:28` | AsyncAPI 3.0.0 | 최신 안정 3.1.0 | 인용하려는 receiver 규범은 실제 조회한 3.0.0에도 존재하므로 의미상 유효하다. 최신판 링크로 바꿀지는 별도 결정 사항이다. [3.0.0 spec](https://www.asyncapi.com/docs/reference/specification/v3.0.0), [3.1.0 release](https://github.com/asyncapi/spec/releases/tag/v3.1.0) |
| `docs/backend/fundamentals/api-design.md:80-82` | OpenAPI 3.2.0 | OpenAPI 3.2.1 | 명백히 한 패치 뒤처짐. 3.2.1은 2026-09-10 공개됐고 release note는 중대한 변경 없이 명세 문구 교정·명확화 중심이라고 밝힌다. [3.2.1 release](https://github.com/OAI/OpenAPI-Specification/releases/tag/3.2.1) |
| `backend-kit/skills/backend-system/SKILL.md:50` | OpenAPI 3.1 | 최신 3.2.1 | 최신판보다 낮지만, 최소 호환 기준으로 의도한 것이라면 반드시 낡았다고 볼 수 없다. [최신 OAS](https://spec.openapis.org/oas/latest.html) |
| `backend-kit/skills/backend-audit/SKILL.md:77` | OpenAPI 3.1 | 최신 3.2.1 | 위와 동일. “3.1 이상” 정책이면 유지 가능하고, “최신판” 의미라면 갱신 필요. [최신 OAS](https://spec.openapis.org/oas/latest.html) |
| `backend-kit/skills/backend-audit/references/audit-criteria.md:22,26` | OpenAPI 3.1.x / 3.1.1 | 최신 3.2.1 | JSON Schema/format 설명을 3.1.1에 고정 인용할 수는 있으나 최신판 표기는 아니다. [최신 OAS](https://spec.openapis.org/oas/latest.html) |
| `rust-kit/references/project-detection.md:82-86` | 2026-08-13 최신 SeaORM 2.0.1 | SeaORM 2.0.3, 2026-09-13 | 현행성 표가 낡음. [2.0.3 release](https://github.com/SeaQL/sea-orm/releases/tag/2.0.3) |
| `rust-kit/skills/rust-model/SKILL.md:47,52,62-66` | SeaORM 1.1 계열 예시 | 최신 안정 2.0.3 | 신규 스캐폴딩 기준으로는 낡음. 다만 기존 프로젝트 고정 버전을 우선한다는 현재 주석은 유지해야 한다. [2.0.3 release](https://github.com/SeaQL/sea-orm/releases/tag/2.0.3) |
| `rust-kit/skills/rust-init/SKILL.md:69` | `sea-orm = "1.1"` | 최신 안정 2.0.3 | 신규 프로젝트 기본 예시라면 갱신 후보. 2.0은 entity/relation 정의, raw SQL API, PostgreSQL identity 기본값, feature 이름 등에 깨지는 변경이 있다. [2.0.0 release](https://github.com/SeaQL/sea-orm/releases/tag/2.0.0) |
| `rust-kit/templates/rust-init.toml.template:40` | `sea-orm = "1.1"` | 최신 안정 2.0.3 | 신규 템플릿이면 갱신 후보이나 단순 버전 치환은 금물이다. [2.0.0 breaking changes](https://github.com/SeaQL/sea-orm/releases/tag/2.0.0) |
| 해당 버전 리터럴 없음 | Chrono 타입만 언급 | Chrono 0.4.45 | 버전 때문에 낡은 대상은 찾지 못했다. [0.4.45 release](https://github.com/chronotope/chrono/releases/tag/v0.4.45) |

SeaORM 2.0에서 확인된 깨지는 변경은 다음과 같다.

- 새 entity 형식 도입
- 표현식 메서드에 `ExprTrait` import 필요
- `execute/query_one/query_all/stream`이 SeaQuery statement를 받고 raw SQL 버전은 `*_raw`로 분리
- PostgreSQL auto-increment 기본이 `serial`에서 identity로 변경
- `runtime-actix`, `DeriveCustomColumn`, `default_as_str` 제거
- SQLx 0.9 및 SeaQuery 1.0으로 이동

[SeaORM 2.0.0 release](https://github.com/SeaQL/sea-orm/releases/tag/2.0.0)

## 4. 권장안

Phase 계약 조건은 다음처럼 잡는 것이 외부 근거와 가장 잘 맞는다.

1. 모든 시간 필드에 의미 분류를 요구한다.

   - `instant`
   - `floating_wall_time`
   - `zoned_wall_time`

2. 순간은 UTC로 정규화한다.

   - SQLx: `DateTime<Utc>` + `TIMESTAMPTZ`
   - API 직렬화: 오프셋이 명시된 RFC 3339
   - 원래 사용자가 고른 시간대가 비즈니스 정보라면 `TIMESTAMPTZ`와 별도 필드에 보존한다. PostgreSQL은 원래 시간대를 보존하지 않는다. [PostgreSQL](https://www.postgresql.org/docs/current/datatype-datetime.html)

3. 벽시계는 의미에 따라 나눈다.

   - 수신자 지역을 따라가는 일정: `NaiveTime`/`NaiveDateTime`
   - 특정 지역에 고정된 일정: naive 값과 IANA 시간대 식별자를 함께 보존
   - 순간으로 실행할 때 적용 시간대와 DST 중복·누락 해소 정책을 계약에 명시

4. audit 실패 조건을 의미 기반으로 쓴다.

   - 벽시계 의미를 UTC 순간 하나로만 저장해 의도를 잃으면 FAIL
   - 특정 지역 고정 일정을 시간대 식별자 없이 저장하면 FAIL
   - 사용자·요청·저장 설정이 필요한 서비스에서 코드 상수 하나로 시간대를 강제하면 FAIL
   - 사용자가 단일 지역 서비스라고 명시한 경우 N/A 가능

5. rust-model 문장은 ORM별로 분리한다.

   - SQLx의 `DateTime<Utc>`+`TIMESTAMPTZ` 근거는 공식 타입표와 일치한다.
   - SeaORM에는 `DateTimeWithTimeZone`+`TimestampWithTimeZone`을 사용하고, `DateTime<Utc>`를 동일한 Entity 매핑으로 단정하지 않는다.
   - 입력 표의 “타임스탬프 타입”에는 `(순간 / floating 벽시계 / 특정 지역 벽시계 구분)`을 붙인다.

6. 버전 현행화는 이번 Phase 변경과 분리하되 최소한 다음은 같이 바로잡는다.

   - OAuth 2.1 draft-15 → draft-16
   - OpenAPI 3.2.0 → 3.2.1
   - AsyncAPI 최신값 3.1.0 기록
   - SeaORM 최신값 2.0.3 기록
   - SeaORM 1.1→2.0 예시는 migration 검토 없이 기계적으로 바꾸지 않음

## 5. 못 가져온 것 / 열린 질문

- 필수 소스 표의 “Hexagonal / Clean / DDD 2026 실무” 커뮤니티 자료는 조회하지 않았다.
- “Pact + Testcontainers” 커뮤니티 글은 조회하지 않았다.
- RFC 5545에는 나라 코드, 기기 시간대 우선순위, 사용자 설정 저장 여부, 코드 상수 금지 규칙이 없다. 이 부분은 외부 표준이 아니라 프로젝트 계약으로 정당화해야 한다.
- “알람”은 의미가 모호하다. 여행해도 현지 07:00에 울리는 알람인지, 특정 장소의 07:00에 대응하는 순간인지에 따라 floating과 zoned 처리가 달라진다.
- 특정 지역 벽시계의 시간대 필드를 사용자 설정에서 상속할지 일정 레코드에 스냅샷으로 저장할지는 제품 요구사항이 필요하다.
- OpenAPI 3.1을 최소 지원선으로 유지할지 3.2.1을 새 기본값으로 올릴지는 툴체인 호환성 확인이 필요하다. 이번 조회에서는 3.2.1 자체가 중대한 변경을 포함한다는 근거는 발견하지 못했다.
- 저장소는 수정하지 않았으며 `git status`도 깨끗했다.
