# Backend System Principles

프로젝트 백엔드 아키텍처 세팅 시 참조하는 원칙 문서 매핑.

## 필수 카테고리

| 카테고리 | 참조 문서 | 핵심 원칙 |
|----------|-----------|-----------|
| API 규격 | ../../../../docs/backend/fundamentals/api-design.md | 리소스 명사, RFC 9110 메서드, RFC 9457 에러 |
| 에러 처리 | ../../../../docs/backend/fundamentals/error-handling.md | Result 패턴, backoff+jitter, circuit breaker |
| 인증/인가 | ../../../../docs/backend/fundamentals/auth.md | JWT vs Session, Argon2id, CORS, CSRF |
| 보안 | ../../../../docs/backend/fundamentals/security.md | OWASP Top 10, 보안 헤더, PII 마스킹 |

## 선택 카테고리

| 카테고리 | 참조 문서 | 도입 기준 |
|----------|-----------|-----------|
| 캐싱 | ../../../../docs/backend/patterns/caching.md | 읽기 비율 높은 데이터 존재 시 |
| 이벤트 | ../../../../docs/backend/patterns/event-driven.md | 비동기 처리, 서비스 간 통신 필요 시 |
| 테스트 | ../../../../docs/backend/fundamentals/testing.md | 항상 권장 |
| API Lifecycle | ../../../../docs/backend/protocols/api-lifecycle.md | 외부 공개 API 시 |
