---
title: Phase Research Templates
version: 1.2.0
last_updated: 2026-09-05
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

## Phase 12 — reflect-kit

### 필수 소스 (3 건 이상)

reflect-kit 은 대화 피드백 → 학습 → 재주입 파이프라인(Reflexion 방법론)을 다룬다. 훅 계약과
라벨링 품질이 핵심이므로 공식 훅 문서 + 라벨 일관성 연구 + 이벤트 그룹핑 선행 사례를 조회한다.

| # | 소스 | 유형 | 조회 이유 | Fallback |
| - | ---- | ---- | --------- | -------- |
| 1 | [Claude Code Hooks](https://code.claude.com/docs/en/hooks) | 공식 | Stop/PostToolUse 훅 입력 필드·exit code 의미·timeout·`${CLAUDE_PROJECT_DIR}` 계약 | WebFetch |
| 2 | [Reflexion (arXiv 2303.11366)](https://arxiv.org/abs/2303.11366) | 논문 | 이 킷의 방법론 원전. episodic memory buffer 재주입 근거 | WebFetch |
| 3 | [닫힌 라벨 집합의 label collapse (arXiv 2605.06940)](https://arxiv.org/abs/2605.06940) | 논문 | `mistake_tag` 를 닫힌 집합으로 강제할 때의 소수 카테고리 미탐지·agreement illusion 위험 | WebFetch |
| 4 | [라벨링 일관성 / 스펙 상세도 (arXiv 2605.24247)](https://arxiv.org/abs/2605.24247) | 논문 | 태그 작성 규칙의 상세도 조절 (단순 정의 부족 vs 과잉 상세 drift) | WebFetch |
| 5 | [Sentry fingerprint rules](https://docs.sentry.io/concepts/data-management/event-grouping/fingerprint-rules/) | 공식 | 동일 근본원인 이벤트 canonicalize 선행 사례, 과잉 병합("really bad groups") 경고 | WebFetch |
| 6 | [Prometheus Alertmanager 설정](https://prometheus.io/docs/alerting/latest/configuration/) | 공식 | `group_by` + `repeat_interval` 재알림 억제 구조 (환경 오설정 반복 로깅 억제 설계) | WebFetch |
| 7 | `~/.claude/logs/*/reflections-*.md` + `.env-issues.tsv` | 내부 | 실제 태그 분포·파편화 지표 실측 (읽기 전용, 수정·삭제 금지) | 파일 Read |

## Phase 13 — bambu-kit

### 필수 소스 (3 건 이상)

bambu-kit 은 Bambu Studio 프로파일 JSON 을 생성하므로 **필드명·기본값·계산 의미를 추측하면
import 가 조용히 실패하거나 실물 출력이 어긋난다.** 슬라이서 소스 코드가 1차 출처다.
(references 대량 갱신은 `/bambu-research` 소관 — 이 Phase 는 스킬 품질 개선에 집중한다.)

| # | 소스 | 유형 | 조회 이유 | Fallback |
| - | ---- | ---- | --------- | -------- |
| 1 | [BambuStudio `PrintConfig.cpp`](https://github.com/bambulab/BambuStudio/blob/master/src/libslic3r/PrintConfig.cpp) | 공식(소스) | 필드명·기본값·단위의 정본. 태그본과 대조하여 버전 밴드 확인 | curl |
| 2 | [BambuStudio `PrintObjectSlice.cpp`](https://github.com/bambulab/BambuStudio/blob/master/src/libslic3r/PrintObjectSlice.cpp) | 공식(소스) | 보정값이 **경계 오프셋인지 지름인지** 등 계산 의미 확인 (2026-07-27 PL-01 근본원인) | curl |
| 3 | [BambuStudio Releases API](https://api.github.com/repos/bambulab/BambuStudio/releases) | 공식 | references baseline 버전 밴드가 현행과 얼마나 벌어졌는지 | WebFetch |
| 4 | [OrcaSlicer quality settings 위키](https://github.com/OrcaSlicer/OrcaSlicer/wiki/quality_settings_precision) | community(1차) | 정밀도/공차 파라미터 해설 교차 검증 | WebFetch |
| 5 | [3MF Core Spec](https://github.com/3MFConsortium/spec_core) | 공식 | 모델 파싱 시 구조 전제(지오메트리 위치, 속성 포함 태그) 확인 | WebFetch |
| 6 | `bambu-kit/skills/bambu-print-profile/references/*` (SSOT 7종) + 실측 dogfood 산출물 | 내부 | SSOT 수치와 실제 생성 프로파일의 정합성 전수 대조 | 파일 Read |

## Phase 14 — onboarding-kit

### 필수 소스 (3 건 이상)

onboarding-kit 은 외부 서비스 셋업 가이드 자동 생성을 다루므로 소스는 `.claude/skills/onboarding-kaizen/references/research-sources.md` 에 등록된 1차 출처를 재사용한다.

| # | 소스 | 유형 | 조회 이유 | Fallback |
| - | ---- | ---- | --------- | -------- |
| 1 | [Firebase iOS / FlutterFire docs](https://firebase.google.com/docs/cloud-messaging/ios/client) | 공식 | FCM 셋업 절차 변경, APNs 키 형식 변경 | WebFetch |
| 2 | [Firebase Flutter setup](https://firebase.google.com/docs/flutter/setup) | 공식 | 스택별 초기화 절차 (Flutter 는 네이티브 절차와 다르다 — 혼동이 실사고로 이어졌음) | WebFetch |
| 3 | [Apple Developer Account Help](https://developer.apple.com/help/account/) | 공식 | Bundle ID 정책, 인증서/provisioning 절차, 실측 섹션명 | WebFetch |
| 4 | [Stripe docs](https://docs.stripe.com/) | 공식 | Stripe SDK 최신 셋업 절차. **구 호스트 `stripe.com/docs/` 는 크로스호스트 리다이렉트라 fetch 실패** | WebFetch |
| 5 | [Google Cloud Console docs](https://cloud.google.com/docs/) | 공식 | GCP 서비스 계정/OAuth 셋업 변경 | WebFetch |
| 6 | 패키지 레지스트리 (예: [pub.dev/packages/firebase_messaging](https://pub.dev/packages/firebase_messaging)) | 공식 | 버전 확인은 레지스트리 우선 — GitHub Releases fetch 는 구 프리릴리스만 반환하는 사례 확인됨 | WebFetch |
| 7 | 사용자 피드백 메모리 (`~/.claude/projects/.../memory/feedback_setup_guide_*.md`) | 내부 | 실사용 막힘 패턴 → Gotchas 개선 (읽기 전용) | 파일 Read |

## Phase 15 — tone-kit

tone-kit 은 코딩 톤·유지보수성 게이트를 다룬다. **규칙 강도 3등급(MUST / SHOULD / 관측 컨벤션)이 이 킷의 핵심 자산** 이므로, 리서치의 목적은 새 원칙 추가보다 **기존 규칙의 강도가 출처 강도를 넘지 않는지 재확인** 하는 데 있다.

| # | 소스 | 유형 | 조회 이유 | Fallback |
| - | ---- | ---- | --------- | -------- |
| 1 | [Droid: AI-Generated Code Detection (EMNLP 2025)](https://aclanthology.org/2025.emnlp-main.1593/) | 학술 | 코드 대상 탐지 문헌. adversarial humanizing 위험군 분류 근거 | [arXiv](https://arxiv.org/abs/2507.10583) |
| 2 | [SemEval-2026 Task 13](https://github.com/mbzuai-nlp/SemEval-2026-Task13) | 공식 | 기계 생성 코드 탐지 벤치마크. Hybrid / Adversarial 클래스 정의 | [task list](https://semeval.github.io/SemEval2026/tasks.html) |
| 3 | [Flutter 성능 모범 사례](https://docs.flutter.dev/perf/best-practices) | 공식 | 위젯 분리 권고 문구의 강도 확인 (`prefer` 인지 강제인지) | [architectural overview](https://docs.flutter.dev/resources/architectural-overview) |
| 4 | [StatelessWidget API](https://api.flutter.dev/flutter/widgets/StatelessWidget-class.html) | 공식 | 헬퍼 대신 위젯 클래스 권고의 원문 문구 | [Element.rebuild](https://api.flutter.dev/flutter/widgets/Element/rebuild.html) |
| 5 | [Effective Dart: Style](https://dart.dev/effective-dart/style) | 공식 | 네이밍 규약 변경 여부 | [Documentation](https://dart.dev/effective-dart/documentation) |
| 6 | [Google Engineering Practices](https://google.github.io/eng-practices/review/reviewer/looking-for.html) | 공식 | 주석 경제성 원칙 근거 | [abseil swe-book](https://abseil.io/resources/swe-book/html/ch03.html) |
| 7 | [국립국어원 공공언어](https://korean.go.kr/front/etcData/etcDataView.do?etc_seq=663) | 공식 | 한국어 축 문체 근거 | [LINE 테크니컬 라이팅](https://engineering.linecorp.com/ko/blog/why-are-engineers-so-bad-at-writing/) |
| 8 | 디자인 시스템 컴포넌트 인덱스 (M3 · HIG · MUI · Fluent · Ant · Carbon) | 공식 | 접미사 taxonomy 어휘 원천. **권위가 아니라 어휘 대조용** | WebFetch |

**주의 3건**

- 자연어 텍스트 탐지 문헌(DetectGPT · Binoculars · 텍스트 스타일로메트리)은 `tone-kit/references/sources.md` 의 제외 목록에 있다. 되살리지 마라.
- 접미사 taxonomy 는 6개 시스템 중 어느 곳도 문서화하지 않은 **합성 규칙** 이다. 디자인 시스템을 권위로 인용하지 마라.
- fallback 접두사(`effective*` / `resolved*`) 과대표집 통계는 공개 1차 문헌에 없다 (2026-08 확인). 논문 각주를 붙이지 마라.

## Phase 16 — api-kit

api-kit 은 **실제 응답을 SSOT 로 삼는** 블랙박스 계약 검증을 다룬다. 그래서 이 Phase 의 리서치는
"공식 문서에 뭐라고 적혀 있나" 가 아니라 **"적힌 대로 동작하나"** 를 확인하는 데 목적이 있다.
`docs/api/research-log.md` 의 **미검증 항목 표**를 먼저 읽고, 그 항목부터 대조한다.

| # | 소스 | 유형 | 조회 이유 | Fallback |
| - | ---- | ---- | --------- | -------- |
| 1 | [Hurl Manual](https://hurl.dev/docs/manual.html) | 공식 | 옵션 우선순위(`env < CLI < [Options]`) · `--retry-interval` · `--max-redirs` · exit code 체계. **문서 12종 중 가장 많이 인용된 출처(36 회)** | 로컬 `hurl --help` 실측 |
| 2 | [Hurl Templates — Secrets](https://hurl.dev/docs/templates.html#secrets) | 공식 | `--secret` 마스킹 범위. stdout 을 가리지 않는다는 기재가 킷 redaction 설계(§8.2) 전체의 근거 | 로컬 `hurl --secret` 실행 |
| 3 | [RFC 8785 — JSON Canonicalization Scheme](https://www.rfc-editor.org/rfc/rfc8785.html) | 사양 | 스냅샷 봉인·회귀 diff 의 비교 기준선. 정렬·수치 표기 규칙이 바뀌면 baseline 전체가 흔들린다 | [I-JSON (RFC 7493)](https://www.rfc-editor.org/rfc/rfc7493.html) |
| 4 | [RFC 9110 — HTTP Semantics](https://datatracker.ietf.org/doc/html/rfc9110) | 사양 | 상태 코드·필드명 규범. 오류 계약(`error-status-contracts`) 판정 기준 | [rfc-editor](https://www.rfc-editor.org/rfc/rfc9110.html) |
| 5 | [OpenAPI 3.1 사양](https://spec.openapis.org/oas/v3.1.0) | 공식 | 인벤토리 정규화의 path/parameter/operation 모델. 3.2 진행 여부 확인 | [swagger 문서](https://swagger.io/specification/) |
| 6 | [JSON Schema 2020-12](https://json-schema.org/draft/2020-12/json-schema-validation) | 공식 | 계약 추출 모드의 타입/`enum`/`const` 어휘. draft 이동 여부 확인 | [core](https://json-schema.org/draft/2020-12/json-schema-core) |
| 7 | [Pact — Pending Pacts](https://docs.pact.io/pact_broker/advanced_topics/pending_pacts) | community(1차) | baseline 승격 거버넌스 선행 사례. 신규 계약을 곧바로 빌드 실패로 만들지 않는 구조 | WebFetch |
| 8 | `docs/api/research-log.md` 미검증 항목 표 + `.api/` 실측 산출물 | 내부 | 문서 기재 ↔ 실측 대조. 어긋나면 **실측 채택** 후 로그 기록 | 파일 Read |

**주의 3건**

- **`pin` 의 의미를 되돌리지 마라.** 2026-09-04 리서치에서 '값 고정' → '경로별 명시 assertion'
  으로 재정의됐다. 외부 도구(버전 pin · snapshot pin)의 용례를 근거로 되돌리려면 설계문서 §9.2
  와 `/api-ui` 아이콘 어휘를 함께 고쳐야 한다.
- **경로 간 불변식은 Hurl 로 표현할 수 없다.** `$.meta.total >= len($.data)` 류는 계약 YAML 에
  기록하고 `/api-verify` 후처리에서 검사한다. Hurl assert 문법이 늘었다는 주장은 실측으로 확인한다.
- **확정 결정 5 건을 리서치로 뒤집지 마라** — `exact` 는 본문만 · enum 승격 3 샘플 이상 ·
  prod 기본 GET/HEAD/OPTIONS · 기준선 RFC 8785 JCS · 계약 실패와 환경 실패는 exit code 로 분리.
  근거는 설계문서 §12 의 사용자 확정이다.

## 사용 규칙

1. **리서치 로그 저장** — 각 Phase 종료 시 `docs/<kit>/research-log.md` (또는 `docs/kaizen/research-log.md`) 에 조회한 소스를 "2026-MM-DD" 엔트리로 기록.
2. **중복 리서치 방지** — 지난 사이클 research-log 를 먼저 읽고, 같은 소스의 변경 여부만 확인 (diff 접근).
3. **리서치 품질 자가 검증** — 필수 소스 3+ 건 이상 확인했는가? URL 인용 가능한가? 없으면 Phase 재시도.
4. **Fallback 기록** — Context7 quota 소진 등으로 fallback 을 썼으면 commit message 에 `(fallback: <reason>)` 명시.
