# Backend Audit Criteria

## 1. API Design
| 기준 | PASS 조건 | 출처 |
|------|-----------|------|
| HTTP 메서드 의미론 | GET=safe, PUT=전체교체, PATCH=부분수정 | RFC 9110 |
| 에러 응답 포맷 | application/problem+json 또는 일관된 구조 | RFC 9457 |
| 페이지네이션 | 대량 목록에 cursor/keyset 사용 | Slack Engineering |
| OpenAPI 동기화 | 스펙과 실제 응답 일치 | OpenAPI 3.1.1 |

## 2. Database
| 기준 | PASS 조건 | 출처 |
|------|-----------|------|
| N+1 부재 | 루프 내 개별 쿼리 없음 | PostgreSQL docs |
| 인덱스 존재 | WHERE/JOIN 컬럼에 적절한 인덱스 | PostgreSQL indexes |
| Connection pooling | 풀링 설정 존재 (HikariCP/PgBouncer) | HikariCP docs |
| Migration 안전성 | expand-contract 패턴 준수 | Martin Fowler |

## 3. Authentication & Authorization
| 기준 | PASS 조건 | 출처 |
|------|-----------|------|
| 비밀번호 해싱 | bcrypt(10+) 또는 Argon2id | OWASP |
| 토큰 저장 | JWT를 localStorage에 미저장 | OWASP Session |
| CORS 설정 | 와일드카드(*) + credentials 미사용 | MDN CORS |
| CSRF 방어 | 쿠키 인증 시 SameSite + 토큰 | OWASP CSRF |

## 4. Error Handling
| 기준 | PASS 조건 | 출처 |
|------|-----------|------|
| 글로벌 핸들러 | 표준 에러 포맷으로 변환 | RFC 9457 |
| 스택트레이스 미노출 | 프로덕션 에러에 내부 정보 없음 | OWASP |
| Retry 전략 | exponential backoff + jitter | AWS Architecture |
| Circuit breaker | 외부 호출에 적용 | Resilience4j |

## 5. Security
| 기준 | PASS 조건 | 출처 |
|------|-----------|------|
| Injection 방어 | 파라미터화된 쿼리 | OWASP Top 10 |
| XSS 방어 | 출력 인코딩 + CSP | OWASP XSS |
| 보안 헤더 | HSTS, X-Content-Type-Options, CSP | OWASP Headers |
| 시크릿 관리 | 하드코딩 없음, 환경변수/vault | OWASP |
| PII 로깅 | 로그에 이메일/전화번호/IP 미노출 | OWASP Logging |

## 6. Caching
| 기준 | PASS 조건 | 출처 |
|------|-----------|------|
| TTL 존재 | 모든 캐시 키에 TTL 설정 | Redis docs |
| Stampede 방지 | 인기 키에 lock/early expiry | Cloudflare |
| 무효화 전략 | TTL만이 아닌 이벤트 기반 | Azure Architecture |

## 7. Event-Driven
| 기준 | PASS 조건 | 출처 |
|------|-----------|------|
| Idempotency | consumer에 중복 처리 방어 | Stripe |
| DLQ 존재 | 실패 메시지 격리 경로 | AWS SQS |
| 이중쓰기 방지 | outbox 패턴 또는 동등한 원자성 | microservices.io |

## 8. Testing
| 기준 | PASS 조건 | 출처 |
|------|-----------|------|
| 테스트 존재 | 핵심 로직에 단위 테스트 | Google Testing Blog |
| DB 테스트 | 실제 DB (testcontainers 등) | Testcontainers |
| Mock 정합성 | mock이 실제 API와 drift 없음 | Pact |
