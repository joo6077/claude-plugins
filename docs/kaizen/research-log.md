---
title: Kaizen Research Log
version: 1.4.0
last_updated: 2026-07-27
---

# Kaizen Research Log

## [2026-07-27] — enforcement 등급화 전면 도입 (14/14 CHANGED)

### 데이터 소스 (Step 0)

- **`/insights` 2026-07-27** (`~/.claude/usage-data/report-2026-07-27-182904.html`) — 53일 / 56 세션 중
  51 분석 / 1,092 메시지 / 187 커밋. VERY FRESH(0.1h) 로 인식됨.
  friction: wrong_approach 21 · misunderstood_request 8 · fully achieved 10/50 vs partial 18.
- **`/reflect-digest` 30일** — 760 엔트리 (fit-pal 747 / purchase-bot 13, claude-plugins reflection 0).
  primary: tool_failure 479 / misunderstanding 133 / wrong_approach 109 / repeated_error 39.
  4축: scope(project 479 / session 261 / global 20) · enforce(hard_gate 205 / soft 555).
- **글로벌 evaluator 피드백 240건** (REJECT 89 / APPROVE 149). 귀속은 claude-plugins 118,
  fit-pal 계열 104, 기타 18.
- validate-plugin 스냅샷: 11 plugins OK Exit 0 (사이클 시작 시점).

### 핵심 발견

- **직전 승격분의 빈도가 줄지 않았다.** Friction #1·#3 은 2026-06 사이클에 이미
  `~/.claude/rules/architecture-guardrails.md` 등으로 승격됐는데 세션당 비율은 오히려 상승
  (wrong_approach 53건/168세션 → 21건/51세션). → **새 규칙 추가가 아니라 enforcement 등급 상향**을
  사이클 전체 프레이밍으로 채택.
- **신규 최상위 신호 = 시각·런타임 검증 불신(Friction #2).** 빈 화면을 MCP 스냅샷 근거로
  "정상 렌더링"이라 반복 주장 → 실제로는 unbounded-height ListView collapse. 욕설로 끝난 세션 2건,
  사용자가 "MCP 를 UI 검증에 쓰지 않는 재발 습관을 영구히 고쳐달라"는 전용 세션 개설.
- **digest 40%(351건)가 훅 실패이고 54종 태그로 파편화** — 개별 빈도가 승격 임계 미달.
  근본원인은 Claude 행동이 아니라 fit-pal 환경 오설정 2종(스크립트 3종 부재 + 상대경로 훅이
  서브디렉토리 cwd 에서 해석 실패, 후자가 145건/41%). `${CLAUDE_PROJECT_DIR}` 권고를 공식 문서로 확인.

### 외부 리서치 출처 (Phase 별 — Context7 OAuth 미인증이라 전 Phase WebFetch fallback)

- **Phase 1**: platform.claude.com Agent Skills best practices · code.claude.com sub-agents ·
  anthropics/skills skill-creator · arXiv 2606.09863(False Success in LLM Agents) ·
  arXiv 2607.07405(Deterministic Gates) · arXiv 2605.29442(20,574 세션 developer-agent misalignment)
- **Phase 2**: arXiv 2412.05579(LLMs-as-Judges Survey) · gherkin-best-practices ·
  docs.pact.io contract_tests_not_functional_tests · augmentcode AI spec template
- **Phase 3**: arXiv 2606.22737(GroundEval — 판정자는 validity 가 아니라 plausibility 를 채점) ·
  arXiv 2603.03116(Corrupt Success) · arXiv 2606.21451(assertion vacuity) · plugins-reference
- **Phase 4**: code.claude.com/docs/en/hooks · mgechev/skills-best-practices ·
  arXiv 2606.27416(Glite ARF) · arXiv 2605.06527(STALE) · arXiv 2604.08224(harness engineering)
- **Phase 5**: docs.flutter.dev release-notes(stable 3.44.7) · flutter_riverpod 3.4.1 ·
  go_router 17.3.0 · flutter_hooks 0.21.3+1 · matchesGoldenFile · alchemist 0.14.0 ·
  golden_toolkit(discontinued)
- **Phase 6**: W3C WCAG 2.2 target-size · DTCG CG-FINAL-20251028 · MDN oklch ·
  MDN container queries · MDN prefers-reduced-motion · Playwright test-snapshots·assertions
- **Phase 7**: RFC 9110 · RFC 3339 · OpenAPI 3.1.1 · Pact · PactFlow bi-directional ·
  Idempotency-Key draft-07(만료 상태 명시) · AsyncAPI 3.0 · Testcontainers
- **Phase 8**: K8s Pod Security Admission · Terraform ephemeral · OpenTofu state encryption ·
  SLSA provenance · Sigstore cosign · OTel spec status · GitHub Actions workflow-syntax ·
  Docker build best-practices (템플릿 필수 6종은 "현행 일치, 변경 불필요"로 확인)
- **Phase 9**: cargo-test / cargo-metadata / cargo-locate-project · sqlx::test · SeaORM mock ·
  GNU bash Pipelines · RustSec · Clippy lint index
- **Phase 10**: Testing Library queries · Vitest CLI·passWithNoTests·allowOnly ·
  Playwright test-snapshots·assertions · TanStack Query invalidation
- **Phase 11**: Cucumber Gherkin · Agile Alliance INVEST · Basecamp Shape Up ch6 ·
  GitHub Projects best practices · SVPG four-big-risks · Product Talk OST
- **Phase 12**: code.claude.com hooks · arXiv 2303.11366(Reflexion) · arXiv 2605.06940(label
  collapse — 닫힌 라벨 집합 강제 시 소수 카테고리 79% 미탐지, Fleiss κ≈-0.001) ·
  arXiv 2605.24247(라벨링 일관성) · Sentry fingerprint rules · Prometheus Alertmanager
- **Phase 13**: BambuStudio PrintConfig.cpp/.hpp · PrintObjectSlice.cpp(보정값 = 경계 오프셋 근거) ·
  BambuStudio Releases API · OrcaSlicer quality_settings_precision · 3MF Core Spec
- **Phase 14**: Firebase cloud-messaging/ios/client · Firebase flutter/setup ·
  Apple Developer Account Help · docs.stripe.com/keys · pub.dev firebase_messaging

### 조회로 **정정된** 사실 (학습 데이터 추측이었다면 틀렸을 것)

- 서브에이전트 중첩은 "불가"가 아니라 기본 3층 허용 (가이드 4곳 정정).
- Flutter FCM 절차에 네이티브 `FirebaseApp.configure()` 는 존재하지 않는다 (evals 가 이를 요구하고 있었음).
- Firebase 문서는 `.p8` 을 권장할 뿐 `.p12` 를 deprecated 로 표기하지 않는다 (eval 이 날조 주장).
- `xy_hole_compensation` 은 경계 오프셋 → 지름 변화 2× (SSOT 수치 오류의 근본원인).
- zsh 에서 `PIPESTATUS` 는 unset (`pipestatus` 가 소문자) — 실행으로 직접 확인 후 쉘 분기 명시.
- Stripe 현행 호스트는 `docs.stripe.com`, GitHub Releases fetch 는 구 프리릴리스만 반환.

### 방법론 메모

- Phase 1~4 는 직렬(각 단계가 다음의 기준), Phase 5~14 는 문서상 독립 스택이라 병렬 실행.
  병렬 git 충돌을 막기 위해 서브에이전트는 **git 쓰기 금지**, 계약 파일은 Phase 별 경로로 분리,
  커밋·finalize 는 오케스트레이터가 직렬 처리했다.
- 병렬 5개 동시 실행 시 API 529 로 4개가 중단 → `SendMessage` 로 컨텍스트 보존 재개.
  이후 웨이브는 2~3개로 낮춰 재발 방지.
- 각 Phase 의 self-audit 이 **자기 날조를 스스로 검출**한 사례가 다수 (Pact 미사용 용어 인용,
  논문 수치 과대 인용, 검증 없이 단정한 콘솔 라벨). Evidence Gate 의 의도된 작동.

## [2026-06-11] — hook permission-denied 근본원인 + validate-plugin V8 (인사이트 주도 부분 카이젠)

### 데이터 소스 (Step 0)

- reflect-digest `project=all` 30일 cross-project 집계: 27 프로젝트 / 2,586 엔트리. primary: tool_failure 1537 / misunderstanding 496 / wrong_approach 415 / repeated_error 138.
- 글로벌 evaluator 피드백 190건(REJECT 80, APPROVE 109) — 귀속은 대부분 외부 프로젝트(fit-pal 등) 실사용 QA.
- `/insights`: `~/.claude/usage-data/report.html` (6d). 직전 2026-06-05 사이클과 동일 윈도우 → 한계효용 낮음(triage 반영).
- validate-plugin 스냅샷: 11 plugins OK Exit 0.

### 핵심 발견 (인사이트)

- **hook permission-denied 957건 / 24 프로젝트 (전체 friction 38%)** — 단일 근본원인: `hooks.json`의 `${CLAUDE_PLUGIN_ROOT}/x.sh` 직접 실행 명령이 가리키는 4개 스크립트가 git mode 100644. SessionStart·PreToolUse 매 발화 실패.
- 잔여 신호는 스킬 콘텐츠가 아니라 enforcement gap(필수 스킬 미호출, edit-before-read) — 설계 가이드에 이미 흡수.

### 외부/내부 리서치 출처

- Phase 4: git 파일 모드 추적(100644 vs 100755) + Claude Code plugin hooks 실행 모델(`${CLAUDE_PLUGIN_ROOT}` 직접 실행 vs 인터프리터 경유) — 레포 hooks.json 4종 + reflect 로그 실측 957건.
- 근거 연결: reflect-digest precedence rule #1 (enforcement_need=hard_gate → hook 검토). 본 사이클은 가드를 "검출"(validate-plugin V8)로 구현.

### Phase 5~14 reuse — NO_CHANGE 근거 매트릭스

병렬 triage 에이전트 10기가 각 kit에 대해 4축(kit_feedback_signal / domain_currency / hook_exec_ok / design_guide_drift) 실측. 전 10 kit NO_CHANGE — 도메인 스택(Flutter 3.41·Riverpod 3 / WCAG 2.2·DTCG v1 / OAuth 2.1·FAPI 2.0 / Terraform 1.10·Gateway API v1.4 / Rust 2024·Axum 0.8 / React 19·Vite 8 / OST·Shape Up / Reflexion / Bambu H2S / 셋업 가이드)이 직전 2026-06-05 사이클에 이미 반영됨을 확인.


## [2026-06-05] — Phase 1~13 (/insights 2026-06-04 마찰 패턴)

### 데이터 소스 (Step 0)

- `/insights`: `~/.claude/usage-data/report.html` VERY FRESH(14.4h), 168 세션. §0 최우선 주입.
- 글로벌 evaluator 피드백 184건(REJECT 80, APPROVE 103), Hub 외부 4 프로젝트, validate 11 OK.

### 외부 리서치 출처 (Phase별)

- Phase 1: arxiv 2604.14228, cloudzero.com/blog/claude-code-agents, arxiv 2604.08401.
- Phase 2: testrigor.com test-oracle, nextgenanalysts acceptance-criteria.
- Phase 3: arxiv 2601.14691 (Gaming the Judge), arxiv 2603.10060 (Tool Receipts).
- Phase 6: report.zeroheight.com (Design Systems Report 2026).
- Phase 11: basecamp.com/shapeup Ch.6, agilealliance.org/glossary/invest.
- Phase 12: arxiv 2604.20911 (Omission Constraints Decay), arxiv 2509.03990, arxiv 2605.06445.


## [2026-05-07] — Phase 1~4 (harness 도메인) + /insights 산출물 자동 통합 파이프라인

### 데이터 소스 (Step 0)

- **`/insights` 산출물 자동 통합 파이프라인 신규** — `.claude/kaizen-input/insights-report.md` 자동 탐색. `/insights` 슬래시 커맨드 자체는 Claude Code CLI 사용자 직접 실행 명령으로, 메인 세션이 invoke 불가. 이번 사이클은 13 일 전 (2026-04-24 자) 사용자가 사전 생성해둔 산출물을 입력으로 사용.
  - 3 Friction Points · 3 Recommended Patterns · 3 Feature Suggestions
- 글로벌 evaluator 피드백 150 건 (REJECT 64, APPROVE 85, 외부 4 프로젝트 + claude-plugins)
- Hub 외부 프로젝트 4 (apps, fit-pal*, flutter_playwright)
- followup 1 건 (followup-2026-04-11.md)
- 레포 sprint-contract 이력 10 건
- validate-plugin 9 OK 스냅샷

### Phase 1 신규 원칙 도출

| 원칙 | 출처 | 적용 위치 |
| ------ | ------ | ---------- |
| Pre-Edit Batch Audit | /insights Friction #1 + Recommended Pattern #1 | skill-design-guide §3.6 |
| Pre-Sprint Sync Check | /insights Recommended Pattern #2 | skill-design-guide §9 |
| Session Lifecycle 카테고리 | /insights Feature Suggestion #1 | skill-design-guide §2 (10번째 유형) |
| Hook-Triggered Auto-Correction | /insights Feature Suggestion #2 | agent-design-guide §6 (패턴 7) |
| Self-Evaluator Rule-by-Rule Audit | orchestrator-audit-log 2026-04-24 학습 + agent §10 | agent-design-guide §10 + qa-evaluator Step 3.5 |

### 외부 리서치 인용 (Phase 1~3 가이드 변경 근거)

- Anthropic Best Practices for Claude Code (2026-04 최신) — Rule-by-Rule Audit + 검증 가능성 원칙
- arxiv:2603.05344 — Plan-Execute 분리 패턴
- claudefa.st sub-agent best practices — 병렬 vs 순차 vs 백그라운드
- LLM-as-judge 2026 연구 (이전 사이클 인용 보존)

### Phase 5~12 reuse — cross-kit-principles 매트릭스

각 kit 별 무거운 변경 대신 `harness/references/cross-kit-principles.md` 매트릭스 단일 진실 원천(SSOT) 도입. 8 kit × 5 신규 원칙 = 40 셀 매트릭스로 전수 적용 위치 명시.

### Sprint Contract Self-Evaluator 결과

- DG-01 (Pre-Edit Batch Audit 신규) — PASS
- DG-02 (Pre-Sprint Sync Check 신규) — PASS
- DG-03 (10번째 유형 표 행) — PASS
- DG-04 (패턴 7 + PostToolUse) — PASS
- DG-05 (self-evaluator gotcha) — PASS
- DG-06 (version bump 1.3.0) — PASS
- DG-07 (Cross-Surface Parity 표 5 → 8 행) — PASS

---

> 매주 연구한 소스와 채택/폐기 여부를 기록한다.
> 다음 실행 시 이 로그를 참조하여 중복 연구를 방지한다.

---

<!-- 엔트리는 최신순으로 추가 -->

## [2026-04-12] - 리서치 확충 + Phase 1~10 카이젠

**트리거:** 자동화 성숙도 Gap 3번(리서치 깊이) 해소

### 리서치 소스 (per-kit)

| Kit | 파일 | 줄 수 | 소스 수 | 주요 토픽 |
| ----- | ------ | ------- | --------- | ---------- |
| Flutter | docs/flutter/research-log.md | 319 | 45 | Riverpod 3.0, Impeller, Shorebird, Flame |
| Design | docs/design/research-log.md | 304 | 68 | DTCG spec, OKLCH, Radix, Panda CSS |
| Backend | docs/backend/research-log.md | 358 | 62 | FAPI 2.0, OTel, Temporal, Hono |
| Infra | docs/infra/research-log.md | 292 | 61 | K8s 1.35, Cilium, SpinKube, WASI |
| Rust | docs/rust/research-log.md | 370 | 58 | Axum 0.8, SQLx 0.9, SeaORM, Dioxus |
| React | docs/react/research-log.md | 322 | 61 | React Compiler, Vite Rolldown, Storybook 9 |

### 리서치 방법

- 1차: Claude WebSearch/WebFetch로 232개 소스 수집 + 3중 검증
- 2차: Codex 교차검증으로 123개 소스 추가
- 합계: 355개 검증된 소스

### 카이젠 적용 결과

Phase 2~10에서 research-log 인사이트를 스킬 Gotchas/Process에 반영. Phase 1 SKIP (이미 최신).

## [2026-04-11] - Research mode rerun (Phase 1~10)

### Phase 1 — 설계 가이드 (Anthropic 공식 패턴)

- [Skill Authoring Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) — 채택
- [Claude Code Sub-agents 공식](https://code.claude.com/docs/en/sub-agents) — 채택
- [skill-creator SKILL.md](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md) — 채택 (500 라인 상한, gerund form, MCP fully-qualified name)
- [Equipping Agents with Agent Skills (Anthropic engineering)](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) — 채택

### Phase 2 — Contract 계약 기반 QA (학술 + 실무)

- [LLMs-as-Judges: A Comprehensive Survey — arxiv 2412.05579](https://arxiv.org/abs/2412.05579) — 채택 (judge criteria 체계화)
- [LLM-as-Judge Reliability Empirical Study — arxiv 2506.13639](https://arxiv.org/html/2506.13639v1) — 채택 (CoT minimal gain)
- [SE of LLM-Empowered Agentic System — arxiv 2510.09721](https://arxiv.org/html/2510.09721v3) — 채택 (unit test = formal contract)
- [Automatically Benchmarking LLM Code Agents (AAA) — arxiv 2510.24358](https://arxiv.org/html/2510.24358v1) — 채택 (PRD + AAA 패턴)
- [Specification & Evaluation of Multi-Agent LLM Systems — arxiv 2506.10467](https://arxiv.org/html/2506.10467) — 참조
- [Gherkin Best Practices](https://github.com/andredesousa/gherkin-best-practices) — 채택 (one When-Then pair)
- [Avoiding Ambiguity in Requirements — Tjong thesis](https://cs.uwaterloo.ca/~dberry/FTP_SITE/tech.reports/TjongThesis.pdf) — 채택 (어휘/구문/의미 모호성 분류)

### Phase 3 — Evaluator LLM-as-Judge 최신 연구

- [Judging the Judges Position Bias — arxiv 2406.07791](https://arxiv.org/abs/2406.07791) — 채택 (Swap Test)
- [Self-Preference Bias in LLM-as-a-Judge — arxiv 2410.21819](https://arxiv.org/abs/2410.21819) — 채택
- [Justice or Prejudice — arxiv 2410.02736](https://arxiv.org/html/2410.02736v1) — 채택 (12 편향 분류)
- [Evaluating Scoring Bias — arxiv 2506.22316](https://arxiv.org/html/2506.22316v1) — 채택 (binary PASS/FAIL)
- [A Survey on LLM-as-a-Judge — arxiv 2411.15594](https://arxiv.org/html/2411.15594v6) — 채택
- [CheckEval — arxiv 2403.18771](https://arxiv.org/abs/2403.18771) — 채택 (boolean 분해)
- [Recursive Rubric Decomposition — arxiv 2602.05125](https://arxiv.org/html/2602.05125v1/) — 채택 (RRD for [goal] tag)

### Phase 4 — QA 자동화 프레임워크

- [Growthbook: Feedback loops in agentic coding](https://blog.growthbook.io/feedback-loops-are-the-next-breakthrough-in-agentic-coding/) — 채택
- [Sauce Labs QA 2026 trends](https://saucelabs.com/resources/blog/beyond-pass-fail-3-strategic-trends-that-will-define-qa-in-2026) — 참조
- [Agentic testing guide 2026](https://vtestcorp.com/insights/agentic-testing-the-complete-guide-to-ai-powered-software-testing-in-2026/) — 참조
- [mgechev skills best practices](https://github.com/mgechev/skills-best-practices) — 채택 (negative trigger 패턴)

### Phase 5 — Flutter 2026 생태계

- [Riverpod 3.0 migration](https://riverpod.dev/docs/3.0_migration) — 채택
- [Freezed 3.0 changelog](https://pub.dev/packages/freezed/changelog) — 채택 (sealed + switch expression)
- [go_router StatefulShellRoute](https://pub.dev/documentation/go_router/latest/go_router/StatefulShellRoute-class.html) — 채택 (preload)
- [Flutter 3.29 release notes](https://docs.flutter.dev/release/release-notes/release-notes-3.29.0) — 채택

### Phase 6 — Design System 2026

- [Tailwind v4 announcement](https://tailwindcss.com/blog/tailwindcss-v4) — 채택 (OKLCH 기본)
- [W3C DTCG v1 Final Report 2025-10-28](https://www.w3.org/community/reports/design-tokens/CG-FINAL-format-20251028/) — 채택
- [W3C WCAG 2.2 What's New](https://www.w3.org/WAI/standards-guidelines/wcag/new-in-22/) — 채택 (SC 2.5.8 24×24)
- [Material 3 Expressive](https://supercharge.design/blog/material-3-expressive) — 참조
- [MDN Container Queries](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_container_queries) — 채택

### Phase 7 — Backend 아키텍처 2026

- [Hexagonal vs Clean vs Onion 2026](https://dev.to/dev_tips/hexagonal-vs-clean-vs-onion-which-one-actually-survives-your-app-in-2026-273f) — 채택
- [OpenAPI 3.1 spec](https://swagger.io/specification/) — 채택 (JSON Schema)
- [AsyncAPI 3.0](https://www.asyncapi.com/docs/reference/specification/v3.0.0) — 채택
- [RFC 9700 OAuth 2.1 BCP](https://datatracker.ietf.org/doc/rfc9700/) — 채택
- [DPoP best practices](https://konghq.com/blog/engineering/demonstrating-proof-of-possession-dpop-preventing-illegal-access-of-apis) — 채택
- [Transactional Outbox pattern](https://microservices.io/patterns/data/transactional-outbox.html) — 채택
- [Pact + Testcontainers](https://prgrmmng.com/contract-testing-with-testcontainers-and-pact) — 채택

### Phase 8 — Infrastructure 2026

- [Kubernetes Pod Security Admission](https://kubernetes.io/docs/concepts/security/pod-security-admission/) — 채택
- [Terraform 1.10 ephemeral](https://developer.hashicorp.com/terraform/language/ephemeral) — 채택
- [OpenTofu state encryption](https://opentofu.org/docs/v1.11/language/state/encryption/) — 채택
- [SLSA provenance](https://slsa.dev/provenance) — 채택
- [Sigstore Cosign attestation](https://docs.sigstore.dev/cosign/verifying/attestation/) — 채택
- [OpenTelemetry status](https://opentelemetry.io/docs/specs/status/) — 채택 (3 signals stable)
- [Argo Rollouts](https://argoproj.github.io/argo-rollouts/) — 채택
- [Flux v2.6](https://fluxcd.io/blog/2025/05/flux-v2.6.0/) — 채택

### Phase 9 — Rust 백엔드 2026

- [Rust Edition 2024 Guide](https://doc.rust-lang.org/edition-guide/) — 채택
- [Axum 0.8 announcement](https://tokio.rs/blog/2024-12-01-announcing-axum-0-8-0) — 채택 ({id} 문법)
- [SQLx 0.8 CHANGELOG](https://github.com/launchbadge/sqlx/blob/main/CHANGELOG.md) — 채택
- [SeaORM 1.1 docs](https://www.sea-ql.org/SeaORM/) — 채택 (MockDatabase)
- [Tonic 0.13 CHANGELOG](https://github.com/hyperium/tonic/blob/master/CHANGELOG.md) — 채택
- fit-pal `server/` ground truth — 채택 (실무 패턴 검증)

### Phase 10 — React 19 + Tauri 2 + Tailwind v4

- [React v19 blog](https://react.dev/blog/2024/12/05/react-19) — 채택
- [Tauri 2.0 stable](https://v2.tauri.app/blog/tauri-20/) — 채택
- [Tauri capabilities](https://v2.tauri.app/security/capabilities/) — 채택 (core:default ACL)
- [Tailwind v4 theme](https://tailwindcss.com/docs/theme) — 채택
- [shadcn Tailwind v4](https://ui.shadcn.com/docs/tailwind-v4) — 채택
- [Vite 8 Rolldown](https://vite.dev/blog/announcing-vite8) — 채택
- [TanStack Query v5 migration](https://tanstack.com/query/v5/docs/react/guides/migrating-to-v5) — 채택 (object-form)
- [Zustand v5 announce](https://pmnd.rs/blog/announcing-zustand-v5/) — 채택 (useShallow 강제)
- [Lingui v5 migration](https://lingui.dev/releases/migration-5) — 채택 (macro split)
- [RHF+Zod v4 호환성 issue #813](https://github.com/react-hook-form/resolvers/issues/813) — 채택 (zod/v3 workaround)

---

## 2026-03-30 (evaluator-kaizen)

**트리거:** manual (첫 실행, 리서치 전용 모드)
**피드백 분석:** 0건, 피드백 없음 — search-sources.md 우선순위 상위 3개 도메인 리서치

### 조사한 소스

| # | 제목 | URL | 유형 | 신뢰도 | 결과 |
| --- | ------ | ----- | ------ | -------- | ------ |
| 1 | A Survey on LLM-as-a-Judge | <https://arxiv.org/abs/2411.15594> | peer-reviewed survey `[preprint]` | 높음 | 채택 |
| 2 | CheckEval: Robust Evaluation Framework using LLM via Checklist | <https://arxiv.org/abs/2403.18771> | EMNLP 2025 | 높음 | 채택 |
| 3 | Understanding LLM-Driven Test Oracle Generation | <https://arxiv.org/abs/2601.05542> | AIware 2025 | 높음 | 채택 |
| 4 | Rubric Is All You Need: LLM-based Code Evaluation with Question-Specific Rubrics | <https://arxiv.org/abs/2503.23989> | ICER 2025 | 높음 | 채택 (참고) |
| 5 | A Statistical Approach to Model Evaluations | <https://www.anthropic.com/research/statistical-approach-to-model-evals> | 공식 (Anthropic) | 높음 | 채택 |
| 6 | Bloom: Automated Behavioral Evaluations | <https://alignment.anthropic.com/2025/bloom-auto-evals/> | 공식 (Anthropic) | 높음 | 채택 (참고) |
| 7 | Test Oracle Automation in the Era of LLMs (ACM TOSEM) | <https://dl.acm.org/doi/10.1145/3715107> | peer-reviewed | 높음 | 폐기 |

### 채택한 인사이트

- **구현 추종 편향 (Implementation-following bias):** LLM은 코드를 읽을 때 구현된 로직을 "의도된 행동"으로 추종하는 경향이 있다. qa-evaluator는 계약을 먼저 읽고 기대 행동을 확립한 뒤 코드를 검증해야 한다 (Specification-First 원칙) — 적용 영역: guide, skills
- **확장된 편향 분류:** 기존 3개(위치/장황함/자기강화)에서 6개로 확장. 구체성 편향, 구현 추종 편향, 지시 해석 불일치 추가. 각 편향별 완화 전략 명시 — 적용 영역: guide
- **CheckEval 3단계 분해 프로토콜:** Aspect Selection → Checklist Generation → Boolean Evaluation. 평가자 간 일치도 0.45 향상. 복합 조건에 대한 체계적 분해 예시 추가 — 적용 영역: guide, skills
- **판정 확신도 체계:** Anthropic 통계적 접근법 기반. 검증 레벨(L1/L2/L3)과 연동한 높음/중간/낮음 확신도 태그. 낮은 확신도 PASS는 미검증 취급 — 적용 영역: guide

### 폐기 사유

- **소스 7 (ACM TOSEM):** HTTP 403 접근 불가. GATE 2 실패로 폐기

### 개선 적용

- 대상: `docs/guides/qa-evaluation-guide.md`
- 변경: 편향 테이블 6개로 확장, 구현 추종 편향 경고 blockquote 추가, CheckEval 3단계 분해 프로토콜 + 복합 조건 예시, 판정 신뢰도 평가 섹션 신설 (확신도 테이블 + Specification-First 원칙)
- 대상: `harness/agents/qa-evaluator.md`
- 변경: Specification-First 원칙 Step 2에 추가, 복합 조건 분해(CheckEval) 프로토콜 참조 추가, Red Flags에 구현 추종 편향 항목 추가, Rationalization Table에 구현 추종 변명 차단 추가
- 버전: v0.3.4 → v0.3.5

### PR

- 커밋으로 직접 적용 (첫 실행, 리서치 전용 모드)

---

## 2026-03-30 (contract-kaizen)

**트리거:** manual (첫 실행, 리서치 전용 모드)
**피드백 분석:** 0건, 피드백 없음 — search-sources.md 우선순위 상위 3개 도메인 리서치

### 조사한 소스

| # | 제목 | URL | 유형 | 신뢰도 | 결과 |
| --- | ------ | ----- | ------ | -------- | ------ |
| 1 | Spec-driven development (Thoughtworks) | <https://www.thoughtworks.com/en-us/insights/blog/agile-engineering-practices/spec-driven-development-unpacking-2025-new-engineering-practices> | blog `[blog]` | 중간 | 채택 |
| 2 | Automated Repair of Ambiguous Problem Descriptions (SpecFix) | <https://arxiv.org/abs/2505.07270> | preprint `[preprint]` | 높음 | 채택 |
| 3 | Evaluation-Driven Development of LLM Agents (EDDOps) | <https://arxiv.org/abs/2411.13768> | preprint `[preprint]` `[dated: 2024-11]` | 높음 | 채택 (참고) |
| 4 | ATDD for Claude Code (swingerman/atdd) | <https://github.com/swingerman/atdd> | community `[community]` | 중간 | 채택 |
| 5 | Given-When-Then Acceptance Criteria Guide | <https://www.parallelhq.com/blog/given-when-then-acceptance-criteria> | blog `[blog]` | 중간 | 채택 |

### 채택한 인사이트

- **구현 누수 방지 (External Observables Only):** 조건에 클래스명/메서드명/DB명 등 구현 상세를 쓰면 구현 변경 시 조건이 깨진다. ATDD 프레임워크(swingerman/atdd)에서 "Golden Rule"로 강조 — 적용 영역: guide, skills
- **반구조화 조건의 할루시네이션 감소:** Thoughtworks SDD 리서치에서 semi-structured specs가 LLM 추론 정확도를 높이고 할루시네이션을 줄인다고 확인. 복잡도 중간 이상에서 GWT 필수화 — 적용 영역: guide, skills
- **모호성 분류 체계 (Ambiguity Taxonomy):** SpecFix 논문에서 문제 기술의 43.58%에 수정 가능한 모호성 존재 확인. 어휘적/구문적/의미적 3단계 분류로 체계적 점검 — 적용 영역: guide
- **비기능 요구사항 커버리지:** BDD 리서치에서 NFR(성능/보안/접근성) 누락이 일반적 안티패턴으로 지적 — 적용 영역: guide, skills

### 폐기 사유

- 없음 (첫 실행이므로 모든 채택 소스가 신규)

### 개선 적용

- 대상: `docs/guides/contract-design-guide.md`
- 변경: 외부 관찰 가능성 섹션 추가, 안티패턴 2개 추가 (구현 누수, NFR 누락), 모호성 분류 체계 추가, 진단 체크리스트 2개 항목 추가, GWT 적용 기준 명확화
- 대상: `harness/skills/sprint-contract/SKILL.md`
- 변경: Gotchas 3개 추가 (구현 누수, GWT 필수화, NFR), 자기진단 체크리스트 2개 항목 추가 (implementation_leakage, nfr_coverage)
- 버전: v0.3.3 → v0.3.4

### PR

- 커밋으로 직접 적용 (첫 실행, QA 충돌 없음)

---

## 2026-03-30

**트리거:** manual (전체)

### 조사한 소스

| # | 제목 | URL | 유형 | 신뢰도 | 결과 |
| --- | ------ | ----- | ------ | -------- | ------ |
| 1 | Survey on Evaluation of LLM-based Agents | <https://arxiv.org/abs/2503.16416> | peer-reviewed `[preprint]` | 높음 | 채택 (참고) |
| 2 | Beyond Task Completion: Assessment Framework for Agentic AI | <https://arxiv.org/abs/2512.12791> | peer-reviewed `[preprint]` | 높음 | 채택 (참고) |
| 3 | Agentic AI Coding: Best Practice Patterns for Speed with Quality | <https://codescene.com/blog/agentic-ai-coding-best-practice-patterns-for-speed-with-quality> | blog | 중간 | 채택 |
| 4 | agentic-code: Quality Gates Framework | <https://github.com/shinpr/agentic-code> | community | 중간 | 채택 |
| 5 | Best Practices for Claude Code | <https://code.claude.com/docs/en/best-practices> | 공식 | 높음 | 채택 |
| 6 | Evaluation and Benchmarking of LLM Agents: A Survey | <https://arxiv.org/abs/2507.21504> | peer-reviewed `[preprint]` | 높음 | 폐기 |

### 채택한 인사이트

- **검증 가능한 성공 기준:** Claude Code 공식 best practices에서 "Give Claude a way to verify its work"가 단일 최고 레버리지 행동으로 제시됨 — 적용 영역: guide
- **Multi-Level Code Safeguards:** CodeScene이 3단계 검증(생성 중 → pre-commit → PR)을 권장. 단일 시점 검증보다 효과적 — 적용 영역: skill (sprint-contract)
- **Isolated Review:** agentic-code 프레임워크에서 "LLMs cannot reliably review their own outputs within the same context" 확인. Generator의 self-review를 독립 검증으로 취급하면 안 됨 — 적용 영역: agent (qa-evaluator)

### 폐기 사유

- **소스 6 (arxiv:2507.21504):** 2025년 7월 발행이나 내용이 소스 1과 대부분 중복. 추가 인사이트 없음

### PR

- (이 세션에서 PR 생성 예정)
