---
name: backend-guide
description: >
  개발 중 백엔드 코드/설계를 받아 관련 백엔드 원칙을 참조하여 가이드한다.
  스택 무관 — 원칙과 이유만 설명하고 구현은 프로젝트 스택에 맞게 적용.
  "백엔드 가이드", "이 API 설계 괜찮아?", "DB 설계 조언",
  "보안 리뷰해줘" (가벼운 리뷰) 같은 요청 시 트리거.
  체계적 전수 검사에는 트리거하지 않는다 — backend-audit 사용.
argument-hint: "[file-path or description]"
user-invocable: true
---

# Gotchas

1. **스택별 코드 제시 금지** — 원칙과 이유만 설명하라. Express/Django/Spring 코드를 직접 제시하지 마라. "cursor 기반 페이지네이션이 필요합니다"는 ✓, "app.get('/users?cursor=...')"는 ✗.
2. **주관적 피드백 금지** — "잘 설계됐다", "깔끔하다" 같은 표현 금지. 반드시 출처가 있는 원칙을 근거로 제시하라.
3. **카테고리 과잉 방지** — 한 번에 모든 카테고리를 언급하지 마라. 사용자가 물어본 맥락과 관련된 원칙만 집중해서 답하라. 질문이 API 설계에 관한 것이면 캐싱 원칙은 언급하지 않는다.
4. **리서치 문서 없이 답변 금지** — 반드시 principle-index.md를 통해 해당 원칙 문서를 읽은 후 답변하라. 학습 데이터 기반 답변 금지.

# Process

## Step 1: 맥락 파악

사용자가 제공한 코드/설명에서 관련 백엔드 카테고리를 식별한다:

| 카테고리 | 키워드 |
|----------|--------|
| api-design | REST, 엔드포인트, URL, 상태코드, 페이지네이션 |
| database | 스키마, 인덱스, 쿼리, N+1, migration, 풀링 |
| auth | 인증, 인가, JWT, OAuth, RBAC, 세션, CORS |
| error-handling | 에러, retry, circuit breaker, 예외, fallback |
| testing | 테스트, mock, fixture, 커버리지, contract test |
| security | 보안, injection, XSS, SSRF, OWASP, 헤더 |
| caching | 캐시, Redis, TTL, stampede, 무효화 |
| event-driven | 메시지 큐, Kafka, outbox, saga, DLQ, idempotency |
| api-lifecycle | 버저닝, deprecation, rate limiting, idempotency key |
| graphql | GraphQL, 스키마, resolver, DataLoader, federation |
| grpc | gRPC, proto, streaming, deadline, metadata |
| realtime | WebSocket, SSE, 실시간, 구독, heartbeat |

## Step 2: 원칙 참조

references/principle-index.md에서 해당 카테고리의 원칙 문서 경로를 찾아 읽는다.

## Step 3: 가이드 제시

각 피드백 항목은 반드시 이 포맷을 따른다:

### [카테고리] 항목 제목

**원칙:** [원칙 이름]
**근거:** [구체적 설명 + 수치 기준]
**권장:** [개선 방향]

> **출처:** [출처명](URL)

# References

- references/principle-index.md — 카테고리별 원칙 문서 매핑
