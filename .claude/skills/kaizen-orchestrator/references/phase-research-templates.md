---
title: Phase Research Templates
version: 1.0.0
last_updated: 2026-04-12
---

# Phase Research Templates

> kaizen-orchestrator 의 각 Phase 서브에이전트가 리서치 단계에서 **반드시 조회해야 하는 소스 목록**.
> 이전에는 각 Phase subagent 가 자체 판단으로 리서치 소스를 결정했으나, 이로 인해 리서치 품질이 일관되지 않았다 (2026-04-11 세션에서 Context7 quota 소진 fallback 이 인용 없이 수행됨).
> 이 템플릿은 Phase 별 의무 소스를 고정하여 리서치 재현성을 확보한다.

## 공통 원칙

1. **필수 소스** 는 최소 3 개 이상 조회해야 한다. 3 개 미만이면 Phase 가 리서치 완료로 인정되지 않는다.
2. 각 소스는 **1순위 (Context7/공식)** 와 **2순위 (Codex/WebSearch fallback)** 로 분류된다.
3. Context7 quota 소진 시 2순위를 사용하되, **어떤 fallback 이 사용됐는지 commit message 에 명시**.
4. 리서치 결과는 Phase 서브에이전트가 Sprint Contract 에 URL 로 인용해야 한다.

## Phase 1 — 설계 가이드 (skill-design-guide, agent-design-guide)

### 필수 소스 (3 건 이상)

| # | 소스 | 유형 | 조회 이유 | Fallback |
| - | ---- | ---- | --------- | -------- |
| 1 | [Anthropic Skill Authoring Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) | 공식 | frontmatter 스키마, description 작성법, trigger 패턴 | WebFetch |
| 2 | [Claude Code Sub-agents 공식 문서](https://code.claude.com/docs/en/sub-agents) | 공식 | initialPrompt, color, tools 필드, 에이전트 체인 제약 | WebFetch |
| 3 | [anthropics/skills GitHub repo](https://github.com/anthropics/skills) | 공식 | skill-creator SKILL.md 규칙, 500 라인 상한, gerund form | WebFetch |
| 4 | LLM agent skill design arxiv 2026 | 학술 | 2026 최신 skill authoring 연구 | Codex WebSearch |

## Phase 2 — Contract (contract-design-guide, sprint-contract, contract-schema)

### 필수 소스 (3 건 이상)

| # | 소스 | 유형 | 조회 이유 | Fallback |
| - | ---- | ---- | --------- | -------- |
| 1 | [arxiv 2412.05579 — LLMs-as-Judges Survey](https://arxiv.org/abs/2412.05579) | 학술 | judge criteria 체계화 | Codex |
| 2 | [arxiv 2506.13639 — LLM-as-Judge Reliability](https://arxiv.org/html/2506.13639v1) | 학술 | evaluation criteria 신뢰도 | Codex |
| 3 | [Gherkin Best Practices](https://github.com/andredesousa/gherkin-best-practices) | community | one When-Then pair 패턴 (AAA) | WebFetch |
| 4 | [Tjong — Avoiding Ambiguity in Requirements](https://cs.uwaterloo.ca/~dberry/FTP_SITE/tech.reports/TjongThesis.pdf) | 학술 | 모호성 분류 (어휘/구문/의미) | Codex |
| 5 | Acceptance criteria anti-patterns 2026 | community | AC 반패턴 최신 | Codex WebSearch |

## Phase 3 — Evaluator (qa-evaluation-guide, qa-evaluator)

### 필수 소스 (5 건 이상, LLM-as-judge 는 가장 활발한 연구 영역)

| # | 소스 | 유형 | 조회 이유 | Fallback |
| - | ---- | ---- | --------- | -------- |
| 1 | [arxiv 2406.07791 — Position Bias](https://arxiv.org/abs/2406.07791) | 학술 | Swap Test | Codex |
| 2 | [arxiv 2410.21819 — Self-Preference Bias](https://arxiv.org/abs/2410.21819) | 학술 | perplexity 기반 familiarity | Codex |
| 3 | [arxiv 2506.22316 — Scoring Bias](https://arxiv.org/html/2506.22316v1) | 학술 | binary PASS/FAIL 강제 | Codex |
| 4 | [arxiv 2411.15594 — LLM-as-Judge Survey](https://arxiv.org/html/2411.15594v6) | 학술 | 12 편향 분류 | Codex |
| 5 | [arxiv 2403.18771 — CheckEval](https://arxiv.org/abs/2403.18771) | 학술 | boolean 분해 패턴 | Codex |
| 6 | [arxiv 2602.05125 — Recursive Rubric Decomposition](https://arxiv.org/html/2602.05125v1/) | 학술 | RRD (`[goal]` 태그용) | Codex |

## Phase 4 — Harness 지원 스킬 (init, create-skill, create-agent, kaizen 스킬)

### 필수 소스 (3 건 이상)

| # | 소스 | 유형 | 조회 이유 | Fallback |
| - | ---- | ---- | --------- | -------- |
| 1 | QA 자동화 프레임워크 2026 트렌드 | blog | feedback loop, agentic testing | Codex |
| 2 | [skills best practices (mgechev 등)](https://github.com/mgechev/skills-best-practices) | community | negative trigger 패턴 | WebFetch |
| 3 | Plugin 검증 스키마 최신 2026 | community | trigger 키워드 충돌, frontmatter drift | Codex |
| 4 | LLM agent framework plugin authoring | 학술 | 최신 스킬 체계 | Codex |

## Phase 5 — flutter-toolkit

### 필수 소스 (Context7 우선)

| # | 소스 | 유형 | 조회 이유 | Fallback |
| - | ---- | ---- | --------- | -------- |
| 1 | Context7 `flutter` (3.x stable) | 공식 | 최신 Flutter API | WebFetch docs.flutter.dev |
| 2 | Context7 `flutter_riverpod` (3.x) | 공식 | Riverpod 3 migration | WebFetch riverpod.dev |
| 3 | Context7 `flutter_hooks` | 공식 | 최신 hooks 패턴 | WebFetch pub.dev/packages/flutter_hooks |
| 4 | Context7 `go_router` 또는 `auto_route` | 공식 | 라우터 최신 패턴 | WebFetch pub.dev |
| 5 | Context7 `freezed` (3.x) | 공식 | sealed/switch 마이그레이션 | WebFetch |
| 6 | Hub `fit-pal/` + `apps/` sprint-feedback | ground truth | 실무 피드백 | 내부 파일 Read |

## Phase 6 — design-kit

### 필수 소스 (3 건 이상)

| # | 소스 | 유형 | 조회 이유 | Fallback |
| - | ---- | ---- | --------- | -------- |
| 1 | [Tailwind v4 announcement](https://tailwindcss.com/blog/tailwindcss-v4) | 공식 | OKLCH 기본 팔레트, CSS-first 설정 | WebFetch |
| 2 | [W3C DTCG v1 Final Report](https://www.w3.org/community/reports/design-tokens/CG-FINAL-format-20251028/) | 표준 | 디자인 토큰 포맷 | WebFetch |
| 3 | [W3C WCAG 2.2](https://www.w3.org/TR/WCAG22/) | 표준 | SC 2.5.8 24×24 터치타겟 | WebFetch |
| 4 | [MDN Container Queries](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_container_queries) | 공식 | Baseline container queries | WebFetch |
| 5 | Material 3 Expressive / HIG 2026 | 공식 | 최신 디자인 언어 | WebFetch |

## Phase 7 — backend-kit

### 필수 소스 (3 건 이상)

| # | 소스 | 유형 | 조회 이유 | Fallback |
| - | ---- | ---- | --------- | -------- |
| 1 | Hexagonal / Clean / DDD 2026 실무 | community | 아키텍처 최신 패턴 | Codex |
| 2 | [OpenAPI 3.1 spec](https://swagger.io/specification/) | 공식 | API 문서화 | WebFetch |
| 3 | [AsyncAPI 3.0 spec](https://www.asyncapi.com/docs/reference/specification/v3.0.0) | 공식 | 이벤트 기반 API | WebFetch |
| 4 | [RFC 9700 OAuth 2.1 BCP](https://datatracker.ietf.org/doc/rfc9700/) | 표준 | 최신 인증 | WebFetch |
| 5 | [microservices.io Transactional Outbox](https://microservices.io/patterns/data/transactional-outbox.html) | community | EDA 패턴 | WebFetch |
| 6 | [Pact + Testcontainers](https://prgrmmng.com/contract-testing-with-testcontainers-and-pact) | community | 계약 테스트 | WebFetch |

## Phase 8 — infra-kit

### 필수 소스 (Context7 + 공식 문서 우선)

| # | 소스 | 유형 | 조회 이유 | Fallback |
| - | ---- | ---- | --------- | -------- |
| 1 | [Kubernetes PSA](https://kubernetes.io/docs/concepts/security/pod-security-admission/) | 공식 | 네임스페이스 보안 | WebFetch |
| 2 | [Terraform 1.10+ ephemeral](https://developer.hashicorp.com/terraform/language/ephemeral) | 공식 | IaC 최신 | WebFetch |
| 3 | [OpenTofu state encryption](https://opentofu.org/docs/v1.11/language/state/encryption/) | 공식 | Terraform 대안 | WebFetch |
| 4 | [SLSA provenance](https://slsa.dev/provenance) | 표준 | 공급망 보안 | WebFetch |
| 5 | [Sigstore Cosign](https://docs.sigstore.dev/cosign/verifying/attestation/) | 공식 | 서명 검증 | WebFetch |
| 6 | [OpenTelemetry status](https://opentelemetry.io/docs/specs/status/) | 공식 | 3 signals stable | WebFetch |

## Phase 9 — rust-kit

### 필수 소스 (Context7 우선)

| # | 소스 | 유형 | 조회 이유 | Fallback |
| - | ---- | ---- | --------- | -------- |
| 1 | Context7 `axum` (0.8+) | 공식 | path / async_trait 변경 | WebFetch tokio.rs blog |
| 2 | Context7 `sqlx` (0.8+) | 공식 | query macro 개선 | WebFetch sqlx CHANGELOG |
| 3 | Context7 `sea-orm` (1.1+) | 공식 | MockDatabase 테스트 | WebFetch sea-ql.org |
| 4 | Context7 `tonic` (0.13+) | 공식 | gRPC 최신 | WebFetch hyperium/tonic |
| 5 | [Rust Edition 2024 Guide](https://doc.rust-lang.org/edition-guide/) | 공식 | edition 전환 | WebFetch |
| 6 | [Clippy lints index](https://rust-lang.github.io/rust-clippy/master/) | 공식 | 2026 새 lints | WebFetch |
| 7 | fit-pal server ground truth | 내부 | 실무 패턴 | 파일 Read |

## Phase 10 — react-kit

### 필수 소스 (Context7 가장 풍부한 Phase)

| # | 소스 | 유형 | 조회 이유 | Fallback |
| - | ---- | ---- | --------- | -------- |
| 1 | Context7 `react` (19+) | 공식 | use() hook, ref-as-prop | WebFetch react.dev blog |
| 2 | Context7 `@tanstack/react-query` (v5+) | 공식 | object-form 시그니처 | WebFetch tanstack.com |
| 3 | Context7 `tauri` (2 GA) | 공식 | ACL capabilities | WebFetch v2.tauri.app |
| 4 | Context7 `tailwindcss` (v4) | 공식 | @theme directive + OKLCH | WebFetch tailwindcss.com |
| 5 | Context7 `zustand` (v5) | 공식 | useShallow 강제 | WebFetch pmnd.rs |
| 6 | Context7 `@lingui/core` (v5) | 공식 | macro split | WebFetch lingui.dev |
| 7 | Context7 `react-hook-form` + `zod` | 공식 | v4 호환성 workaround | WebFetch GitHub issues |
| 8 | [Vite 8 Rolldown announcement](https://vite.dev/blog/announcing-vite8) | 공식 | 최신 번들러 | WebFetch |

## Phase 11 — planning-kit

### 필수 소스 (3 건 이상)

planning-kit 은 제품 기획 방법론 (Discovery, PRD, Prioritization, Risks, Stories, Flows, Data Modeling, GitHub 동기화) 을 다루므로 소스는 `docs/planning/*.md` 에 이미 검증된 1차 URL 을 재사용한다.

| # | 소스 | 유형 | 조회 이유 | Fallback |
| - | ---- | ---- | --------- | -------- |
| 1 | [Teresa Torres — Continuous Discovery / Opportunity Solution Tree](https://www.producttalk.org/glossary-discovery-opportunity-solution-tree/) | community (1차) | discovery 스킬 (plan-discover) 의 기반. OST 구조, weekly touchpoint 원칙 | WebFetch |
| 2 | [Marty Cagan — Four Big Risks](https://www.svpg.com/four-big-risks/) | community (1차) | plan-risks 의 4-risks matrix (Value/Usability/Feasibility/Viability) 기준 | WebFetch |
| 3 | [Basecamp — Shape Up (Pitch / Appetite / Betting Table)](https://basecamp.com/shapeup/1.5-chapter-06) | 공식 | plan-prd 의 Shape Up pitch 템플릿, appetite 기반 스코핑 | WebFetch |
| 4 | [Alan Klement — JTBD switching moments](https://www.alanklement.com/) | community (1차) | plan-discover 인터뷰 프레임 (switching interview) | WebFetch |
| 5 | [Strategyn / Tony Ulwick — ODI](https://strategyn.com/what-customers-want/) | community (1차) | desired outcome 정량화 원칙 | WebFetch |
| 6 | [Agile Alliance — INVEST](https://agilealliance.org/glossary/invest/) | community | plan-stories 의 INVEST 기준 (Independent/Negotiable/…) | WebFetch |
| 7 | [Cucumber Gherkin docs](https://cucumber.io/docs/gherkin/) | 공식 | plan-stories 의 Given-When-Then 수용 기준 | WebFetch |
| 8 | [HBR — Performing a Project Premortem (Gary Klein)](https://hbr.org/2007/09/performing-a-project-premortem) | 공식 | plan-risks 의 pre-mortem 절차 | WebFetch |
| 9 | [Mermaid.js — ER diagram](https://mermaid.js.org/syntax/entityRelationshipDiagram.html) | 공식 | plan-data-model 의 ER/flow 다이어그램 렌더링 | WebFetch |
| 10 | [GitHub Projects REST/GraphQL Docs](https://docs.github.com/en/rest/projects) | 공식 | plan-sync-github (Issue/Projects v2 동기화) | WebFetch |
| 11 | [Lean Stack — Lean Canvas / RAT](https://leanstack.com/articles/the-lean-canvas-diagnostic-part-2-of-7---structure) | community (1차) | plan-prioritize 의 riskiest assumption 접근 | WebFetch |
| 12 | `docs/planning/*.md` (레포 내 누적 리서치 9 편) | 내부 | 각 스킬이 인용한 1차 URL 풀 | 파일 Read |

## Phase 13 — onboarding-kit

### 필수 소스 (3 건 이상)

onboarding-kit 은 외부 서비스 셋업 가이드 자동 생성을 다루므로 소스는 `.claude/skills/onboarding-kaizen/references/research-sources.md` 에 등록된 1차 출처를 재사용한다.

| # | 소스 | 유형 | 조회 이유 | Fallback |
| - | ---- | ---- | --------- | -------- |
| 1 | [Firebase iOS / FlutterFire docs](https://firebase.google.com/docs/cloud-messaging/ios/client) | 공식 | FCM 셋업 절차 변경, APNs 키 형식 변경 | WebFetch |
| 2 | [FlutterFire GitHub Releases](https://github.com/firebase/flutterfire/releases) | 공식 | 호환 매트릭스 변경, breaking change 감지 | WebFetch |
| 3 | [Apple Developer Account Help](https://developer.apple.com/help/account/) | 공식 | Bundle ID 정책, 인증서/provisioning 절차 변경 | WebFetch |
| 4 | [Stripe iOS / Web docs](https://stripe.com/docs/) | 공식 | Stripe SDK 최신 셋업 절차 | WebFetch |
| 5 | [Google Cloud Console docs](https://cloud.google.com/docs/) | 공식 | GCP 서비스 계정/OAuth 셋업 변경 | WebFetch |
| 6 | 사용자 피드백 메모리 (`~/.claude/projects/.../memory/feedback_setup_guide_*.md`) | 내부 | 실사용 막힘 패턴 → Gotchas 개선 | 파일 Read |

## 사용 규칙

1. **리서치 로그 저장** — 각 Phase 종료 시 `docs/<kit>/research-log.md` (또는 `docs/kaizen/research-log.md`) 에 조회한 소스를 "2026-MM-DD" 엔트리로 기록.
2. **중복 리서치 방지** — 지난 사이클 research-log 를 먼저 읽고, 같은 소스의 변경 여부만 확인 (diff 접근).
3. **리서치 품질 자가 검증** — 필수 소스 3+ 건 이상 확인했는가? URL 인용 가능한가? 없으면 Phase 재시도.
4. **Fallback 기록** — Context7 quota 소진 등으로 fallback 을 썼으면 commit message 에 `(fallback: <reason>)` 명시.
