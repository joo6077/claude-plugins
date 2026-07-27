# Backend Principle Index

백엔드 원칙 문서 카테고리별 매핑.

## Fundamentals

| 카테고리 | 문서 경로 |
|----------|-----------|
| Architecture (Hexagonal / Clean / DDD) | ../../../../docs/backend/fundamentals/api-design.md (TBD — `/backend-research` Phase에서 `docs/backend/patterns/architecture.md` 신설 예정) |
| API Design | ../../../../docs/backend/fundamentals/api-design.md |
| Contract Counterpart (빈 상태 상태코드 · timestamp 직렬화 · 소비면 열거) | ../../../../docs/backend/fundamentals/api-design.md + ../../../../docs/backend/fundamentals/testing.md (Pact provider verification) |
| Database | ../../../../docs/backend/fundamentals/database.md |
| Authentication & Authorization | ../../../../docs/backend/fundamentals/auth.md |
| Error Handling | ../../../../docs/backend/fundamentals/error-handling.md |
| Testing | ../../../../docs/backend/fundamentals/testing.md |
| Security | ../../../../docs/backend/fundamentals/security.md |

## Patterns

| 카테고리 | 문서 경로 |
|----------|-----------|
| Caching | ../../../../docs/backend/patterns/caching.md |
| Event-Driven Architecture | ../../../../docs/backend/patterns/event-driven.md |
| Resilience (Circuit Breaker + Rate Limiter) | ../../../../docs/backend/patterns/resilience.md (TBD) |
| Data Validation (Pydantic v2 / Zod / JSON Schema) | ../../../../docs/backend/patterns/validation.md (TBD) |
| Observability (OTel 3 Signals) | ../../../../docs/backend/patterns/observability.md (TBD) |

## Protocols

| 카테고리 | 문서 경로 |
|----------|-----------|
| API Lifecycle | ../../../../docs/backend/protocols/api-lifecycle.md |
| GraphQL (+ Federation + gRPC hybrid) | ../../../../docs/backend/protocols/graphql.md |
| gRPC | ../../../../docs/backend/protocols/grpc.md |
| Realtime Communication | ../../../../docs/backend/protocols/realtime.md |

## Modern Stacks

| 카테고리 | 문서 경로 |
|----------|-----------|
| Architecture Decision (Modular Monolith First) | ../../../../docs/backend/stacks/architecture-decision.md (TBD) |
| Serverless & Edge (Cold Start, Hono, Workers) | ../../../../docs/backend/stacks/serverless-edge.md (TBD) |
| Workflow Engines (Temporal, Dapr) | ../../../../docs/backend/stacks/workflow-engines.md (TBD) |
| Type-Safe APIs (tRPC v11, Effect-TS, Hono RPC) | ../../../../docs/backend/stacks/type-safe-api.md (TBD) |
| Edge Databases (D1, Neon, Turso, TiDB) | ../../../../docs/backend/stacks/edge-db.md (TBD) |
| AI-Augmented Backends (Tool Calling, RAG) | ../../../../docs/backend/stacks/ai-backend.md (TBD) |
| ORM Selection (Prisma vs Drizzle) | ../../../../docs/backend/stacks/orm-selection.md (TBD) |
| Runtime Selection (Bun, Node.js, Deno) | ../../../../docs/backend/stacks/runtime-selection.md (TBD) |
