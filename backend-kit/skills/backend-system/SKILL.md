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

# Process

## Step 1: 프로젝트 백엔드 구조 감지

프로젝트 루트에서 백엔드 관련 파일을 탐색한다:
- 프레임워크 감지 (package.json, requirements.txt, build.gradle, Cargo.toml 등)
- 기존 아키텍처 패턴 분석 (디렉토리 구조, 에러 핸들러, 미들웨어)
- API 스펙 파일 존재 여부 (openapi.yaml, schema.graphql, .proto)

## Step 2: 규격 카테고리 정의

references/system-principles.md를 참조하여 필요한 카테고리를 정의한다:

| 카테고리 | 필수 여부 | 산출물 |
|----------|-----------|--------|
| 아키텍처 패턴 | 필수 | Hexagonal / Clean / DDD 중 프로젝트 규모에 맞는 선택, 도메인-persistence 분리 규약, 의존성 방향(inward-only). 단순 CRUD는 "간소화 계층형" 선택 가능 |
| API 규격 | 필수 | HTTP 메서드 규칙, 상태코드 매핑, RFC 9457 problem+json 에러 포맷, OpenAPI 3.1 스펙 파일 |
| 에러 처리 | 필수 | 에러 분류, 글로벌 핸들러 패턴, retry 정책 (exponential backoff + jitter) |
| 인증/인가 | 필수 | 토큰 전략 (OAuth 2.1 Authorization Code + PKCE), 세션 관리, CORS 정책, 고보안 시 DPoP/mTLS |
| 로깅 | 필수 | 구조화 로그 포맷, 로그 레벨, PII 마스킹 규칙 |
| 테스트 전략 | 선택 | 테스트 피라미드 비율, fixture 관리, Pact + Testcontainers 계약 테스트 |
| 캐싱 | 선택 | 캐시 계층, TTL 정책, 무효화 규칙 |
| 이벤트 기반 | 선택 | AsyncAPI 3 스펙, Outbox relay (batch + backpressure), idempotency, CQRS (도입 기준 충족 시) |

## Step 3: 규격 문서 출력

각 카테고리별로:
1. 현재 상태 (있으면 분석, 없으면 "미설정")
2. 권장 규격 (리서치 문서 기반)
3. 개선 사항 (차이점)

# References

- references/system-principles.md — 카테고리별 세팅 원칙
