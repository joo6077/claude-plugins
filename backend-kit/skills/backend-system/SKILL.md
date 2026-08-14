---
name: backend-system
description: >
  프로젝트에 백엔드 아키텍처 기반(에러 처리 패턴, 인증 구조, API 규격 등)을 세팅한다.
  기존 아키텍처가 있으면 리서치 기준과 비교하여 개선점을 제안한다.
  스택 무관 — 원칙만 정의하고, 구체적 코드 생성은 프로젝트 스택에 맞게 적용.
  "백엔드 아키텍처 세팅", "API 규격 정하자", "에러 핸들링 패턴 세팅",
  "backend system init" 같은 요청 시 트리거.
  단순 API 추가, 기존 패턴 내 코드 작성에는 트리거하지 않는다.
argument-hint: "[project-path]"
user-invocable: true
---

# Gotchas

1. **스택별 코드 생성 금지** — 이 스킬은 원칙과 규격만 출력한다. Express/Django/Spring 코드를 직접 생성하지 마라.
2. **기존 패턴 무시 금지** — 프로젝트에 이미 에러 핸들링/인증 패턴이 있으면 그것을 먼저 분석하고, 리서치 기준과 비교하여 개선점만 제안하라.
3. **전체 구조 강제 금지** — 사용자가 요청한 부분만 세팅하라. "API 규격"을 요청했는데 인증+캐싱+이벤트까지 강제하지 마라.
4. **과도한 복잡도 경고** — CQRS, 이벤트 소싱, 마이크로서비스 패턴은 필요한 경우에만 제안. 프로젝트 규모에 맞지 않으면 경고하라. **Hexagonal / Clean / DDD도 단순 CRUD 앱에 강요 금지 — bounded context 2+ 또는 풍부한 비즈니스 규칙이 있을 때만 권장**. 출처: [Hexagonal vs Clean vs Onion 2026](https://dev.to/dev_tips/hexagonal-vs-clean-vs-onion-which-one-actually-survives-your-app-in-2026-273f).
5. **기존 API 규격 파일 덮어쓰기 금지** — `openapi.yaml`, `schema.graphql`, `.proto` 등이 이미 있으면 내용을 분석하고 diff로 개선점만 제안한다. 전체를 새로 작성하면 기존 클라이언트와 호환이 깨진다.
6. **에러 포맷 혼용 금지** — 프로젝트 내에서 RFC 9457 `problem+json`과 자체 `{ "error": "..." }` 포맷이 혼용되면 클라이언트가 파싱 분기를 해야 한다. 하나의 에러 응답 포맷을 선택하고 프로젝트 전체에 일관 적용해야 한다.
7. **인증/인가 세팅 시 토큰 저장 위치를 명시하라** — JWT 전략만 정의하고 "토큰을 어디에 저장할지"(httpOnly cookie vs localStorage vs 메모리)를 빠뜨리면 클라이언트 보안 정책이 불완전하다. 서버 사이드 세팅이지만 클라이언트 저장소 권장 사항까지 함께 제시해야 한다.
8. **로깅 규격에 PII 마스킹 규칙 필수 포함** — 구조화 로그 포맷만 정의하고 이메일/전화번호/IP 등 개인정보 마스킹 규칙을 빠뜨리면 GDPR/PIPA 위반 위험이 있다. 마스킹 대상 필드 목록과 마스킹 방식(해시, 부분 가림 등)을 규격에 포함하라.
9. **Enumerate-before-Act (skill-design-guide §5.5 대응)** — 기존 프로젝트의 기반을 세팅할 때 "감지 → 권장 규격 → 개선점" 을 rule-by-rule 로 **한 번에 모두 나열** 후 사용자 승인. 라운드-트립 금지 (/insights 마찰점 #1 재발 방지).
10. **Outbox 필수 함정 명시 (Phase 7 리서치)** — 이벤트 기반 패턴 세팅 시 Transactional Outbox 를 권장하되, 반드시 3 가지 함정을 문서에 포함하라: (a) relay 재시도로 인한 **at-least-once**(consumer idempotency 필수), (b) 다중 인스턴스에서의 **메시지 순서 보장** (aggregate 단위 sequence), (c) 개발자가 outbox 쓰기를 빠뜨릴 위험(**정적 분석/리뷰 체크리스트 포함**). 출처: [microservices.io Transactional Outbox](https://microservices.io/patterns/data/transactional-outbox.html).
11. **OAuth 2.1 draft 명시 (Phase 7 리서치)** — 인증 세팅 시 OAuth 2.1 은 `draft-ietf-oauth-v2-1-15` (2026-09-03 만료) 로 아직 Draft 임을 명시. 실무 기준선은 RFC 9700 BCP. 이미 PKCE 필수, Implicit/ROPC 제거, 엄격 redirect URI 매칭이 적용되어 있다. 출처: [IETF OAuth 2.1 Draft](https://datatracker.ietf.org/doc/draft-ietf-oauth-v2-1/).
12. **Counterpart Enumeration — 계약 세팅·변경은 양면 작업 (enforcement 등급 E2)** — API 계약 · 엔드포인트 시그니처 · 상태코드 · 직렬화 포맷 · 공유 모델/생성 코드 · 이벤트 페이로드 · DB 스키마 중 하나라도 정하거나 바꾸면, 편집 착수 **전에** producer 면과 consumer 면 파일을 **양쪽 다 경로로 열거**한 체크리스트를 남긴다. 소비면을 못 찾으면 grep 으로 탐색하고, 그래도 없으면 "소비자 없음" 을 근거와 함께 명시한다 — 추측으로 넘어가지 않는다. 등급 정의와 승급 규칙의 SSOT 는 `harness/docs/guides/skill-design-guide.md` §3.7 이며, 본 원칙의 절차 SSOT 는 같은 문서 §5.5 Counterpart Enumeration 이다. **E2 = 체크리스트 아티팩트** 이므로 문장 다짐으로 대체하지 마라. 이벤트 계열도 같다 — AsyncAPI 는 "수신자 문서를 발신자 문서에서 파생하는 것은 권장되지 않는다(NOT RECOMMENDED)" 고 명시한다. 즉 양면은 각자 자기 문서를 가져야 한다. 출처: [AsyncAPI 3.0.0](https://www.asyncapi.com/docs/reference/specification/v3.0.0).
13. **계약을 커밋된 아티팩트로 먼저 확정하라 (`contracts/<feature>.md`)** — 서버 구현부터 시작하면 소비면 요구가 뒤늦게 드러난다. 규격 세팅 산출물에 다음 6 항목을 **빠짐없이** 담는다: (a) 엔드포인트 메서드/경로 (b) **빈 상태를 포함한 전 상태코드** (c) **모든 timestamp 필드의 타임존·직렬화 규칙** (d) 비멱등 write path 의 idempotency 시맨틱 (e) 소비면 파일 경로 열거 (f) 테스트 픽스처로 그대로 쓸 요청/응답 예시 6 개 이상. 계약 테스트의 표준 관점도 같다 — Pact 는 "consumer 와 provider 양쪽 개발을 통제할 때" 가 적용 조건이라고 못 박는다. 출처: [Pact — What is Pact good for](https://docs.pact.io/getting_started/what_is_pact_good_for).
14. **빈 상태 상태코드를 계약에 못 박아라** — RFC 9110 의 404 는 "대상 리소스의 현재 표현을 찾지 못했거나 존재를 밝히지 않겠다" 는 뜻이지 "컬렉션이 비었다" 가 아니다. 원소 0 개인 컬렉션은 유효한(빈) 표현을 가진 존재하는 리소스이므로 200(빈 배열) 또는 204 가 의미상 맞다. 이 결정을 계약에 적지 않으면 나중에 404→200 으로 바꾸게 되고, 그 순간 소비면 파싱이 깨지는 **계약 변경**이 된다 (Gotcha 12 필수 적용 대상). 출처: [RFC 9110 §15](https://www.rfc-editor.org/rfc/rfc9110.html).
15. **timestamp 는 필드마다 타임존 규칙을 적어라** — "UTC 로 저장한다" 만으로는 부족하다. 직렬화 문자열 형태까지 규정해야 한다. RFC 3339 에서 `Z` 와 `+00:00` 은 "UTC 가 선호 기준점" 을 뜻하지만 `-00:00` 은 "UTC 시각은 알지만 로컬 오프셋을 모른다" 는 **다른 의미**다. OpenAPI 3.1 은 `format` 을 JSON Schema 2020-12 에 위임하며 기본적으로 **비검증 애노테이션**으로 취급하므로, 스펙에 `format: date-time` 만 적어두면 런타임에서 강제되지 않는다. 타임존 버그가 e2e 에서만 표면화되는 이유다. 출처: [RFC 3339 §4.3](https://www.rfc-editor.org/rfc/rfc3339), [OpenAPI 3.1.1](https://spec.openapis.org/oas/v3.1.1.html).
16. **쓰기 경로 무결성을 규격에 포함하라 (E2 아티팩트)** — 상태 전이·중복 방지·재시도 안전성이 걸린 write path 가 있으면 규격 산출물에 (a) invariant 분류 3 줄(유형 / 담당 primitive / 근거 위치) (b) 중복 방지 제약과 upsert 충돌 대상의 대조 표 (c) 멱등 계약 6 항목(key 범위 · payload fingerprint · replay response · in-flight duplicate · different-payload reuse · expiry)을 **함께** 넣는다. 규칙 본문의 SSOT 는 `backend-kit/references/write-path-integrity-protocol.md` 이며 여기서 재열거하지 않는다. Gotcha 13 의 `contracts/<feature>.md` 6 항목 중 (d) idempotency 시맨틱이 바로 이 계약이다.
17. **outbox 를 세팅하면서 "exactly-once" 라고 쓰지 마라** — 비즈니스 갱신과 outbox insert 가 같은 트랜잭션이어도 relay 는 중복 발행할 수 있다. 전달 보장은 **at-least-once** 이며 consumer idempotency(Gotcha 16 의 6 항목)가 세트로 들어가야 규격이 완성된다. Gotcha 10 이 이미 요구하는 (a) 항목의 근거가 이것이다. 출처: [microservices.io Transactional Outbox](https://microservices.io/patterns/data/transactional-outbox.html).

# Process (3-Step · 탐색 → 진단 → 처방)

## Step 1: 탐색 — 프로젝트 백엔드 구조 감지

프로젝트 루트에서 백엔드 관련 파일을 탐색한다:
- 프레임워크 감지 (package.json, requirements.txt, build.gradle, Cargo.toml 등)
- 기존 아키텍처 패턴 분석 (디렉토리 구조, 에러 핸들러, 미들웨어)
- API 스펙 파일 존재 여부 (openapi.yaml, schema.graphql, .proto)

## Step 2: 진단 — 규격 카테고리 Rule-by-Rule 열거

references/system-principles.md 를 참조하여 필요한 카테고리를 rule 단위로 모두 나열한다 (Gotcha 9). 현재 상태와 리서치 기준의 차이를 한 번에 열거.

| 카테고리 | 필수 여부 | 산출물 |
|----------|-----------|--------|
| 아키텍처 패턴 | 필수 | Hexagonal / Clean / DDD 중 프로젝트 규모에 맞는 선택, 도메인-persistence 분리 규약, 의존성 방향(inward-only). 단순 CRUD는 "간소화 계층형" 선택 가능 |
| API 규격 | 필수 | HTTP 메서드 규칙, **빈 상태 포함 상태코드 매핑**(Gotcha 14), RFC 9457 problem+json 에러 포맷, OpenAPI 3.1 스펙 파일, **timestamp 타임존·직렬화 규칙**(Gotcha 15), **비멱등 write path idempotency 시맨틱** |
| 계약 아티팩트 | 필수 (계약을 새로 정하거나 바꿀 때) | `contracts/<feature>.md` 6 항목(Gotcha 13) + producer/consumer 양면 파일 열거 체크리스트(Gotcha 12) |
| 쓰기 경로 무결성 | 필수 (상태 전이·중복 방지·재시도 안전성이 걸린 write path 가 있을 때) | invariant 분류 3 줄 + 제약↔upsert 대조 표 + 멱등 계약 6 항목 (Gotcha 16). outbox 를 쓰면 consumer idempotency 를 같은 규격에 포함 (Gotcha 17) |
| 에러 처리 | 필수 | 에러 분류, 글로벌 핸들러 패턴, retry 정책 (exponential backoff + jitter) |
| 인증/인가 | 필수 | 토큰 전략 (OAuth 2.1 Authorization Code + PKCE), 세션 관리, CORS 정책, 고보안 시 FAPI 2.0(DPoP/mTLS + PAR + JARM). Passkeys/WebAuthn 도입 계획 포함 |
| 관측성 | 필수 | OTel 3 Signals(Traces+Metrics+Logs) 통합, 구조화 로그(JSON + trace_id/span_id), W3C Trace Context 전파, PII 마스킹 규칙 |
| 테스트 전략 | 선택 | 테스트 피라미드 비율, fixture 관리, Pact v4 + Testcontainers 계약 테스트, AI-assisted contract testing(PactFlow MCP) |
| 캐싱 | 선택 | 캐시 계층, TTL 정책, 무효화 규칙 |
| 이벤트 기반 | 선택 | AsyncAPI 3 스펙, Outbox relay (batch + backpressure), idempotency, CDC(Debezium) 파이프라인, 메시지 브로커 선택(Kafka 4.x/RabbitMQ Quorum/NATS), CQRS (도입 기준 충족 시) |

## Step 3: 처방 — 규격 문서 출력

각 카테고리별로:
1. 현재 상태 (있으면 분석, 없으면 "미설정")
2. 권장 규격 (리서치 문서 기반 + 출처 URL 포함)
3. 개선 사항 (차이점 + 우선순위 + 트레이드오프)

계약·직렬화·공유 모델·상태코드·이벤트 페이로드·DB 스키마를 건드리는 세팅이면 아래 체크리스트를 **함께 출력**한다 (Gotcha 12 · E2 아티팩트). 소비면이 별도 저장소면 저장소명까지 적고, 없으면 "소비자 없음 — 근거" 를 적는다. 한 스프린트에서 양면을 다 못 바꾸면 남는 쪽은 `[미검증]` 이 아니라 **명시적 미완 항목**으로 보고한다.

| 면 | 파일 경로 | 변경 내용 | 상태 |
|----|-----------|----------|------|
| producer | `server/src/api/schedule.rs` | 빈 목록 응답 404 → 200 `[]` | ☐ |
| consumer | `app/lib/data/model/schedule_model.dart` | 404 분기 제거 + 빈 배열 파싱 | ☐ |
| consumer | `app/test/data/schedule_model_test.dart` | 빈 배열 픽스처 추가 | ☐ |

# References

- references/system-principles.md — 카테고리별 세팅 원칙
- ../../references/write-path-integrity-protocol.md — 쓰기 경로 무결성 규격 SSOT (invariant 분류 · upsert arbiter · 멱등 계약 6 항목 · outbox 전달 보장)
