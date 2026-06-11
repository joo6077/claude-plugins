---
title: Kaizen Changelog
version: 1.3.0
last_updated: 2026-06-11
---

## [2026-06-11] — hook permission-denied 근본원인 + validate-plugin V8 가드 (인사이트 주도 부분 카이젠)

### 트리거

사용자가 "전체 인사이트 + 카이젠" 요청. reflect-digest `project=all` 30일 cross-project 집계(27 프로젝트 / 2,586 엔트리)에서 **hook permission-denied 계열이 24개 프로젝트 957건(전체 friction의 38%)으로 단일 최대 마찰원**임을 발견. 근본원인은 harness/design-kit 플러그인의 `hooks.json`이 직접 실행하는 `.sh` 4종이 git mode 100644(비실행)로 커밋된 것 — 모든 SessionStart·PreToolUse:Bash hook이 "Permission denied"로 실패하고 있었다 (오늘까지 진행 중).

### 선행 조치 (main 직접 — 사용자 승인)

- `harness/scripts/{env-check,run-guard,sdk-guard}.sh` + `design-kit/scripts/env-check.sh` mode 100644→100755 복원 (소스 + cache + marketplace 복사본). 음성·양성 실행 검증.
- harness v0.4.4 + design-kit v0.2.5 릴리스로 향후 설치본에 전파.

### Step 0~0.6 (Self-Audit + Triage)

- 데이터 풀 재수집(insights 6d / global feedback 190 / hub 5). orchestrator↔marketplace sync drift(릴리스로 발생) 해소.
- **Triage 판정**: 직전 풀 사이클이 6일 전(2026-06-05)이고 /insights도 동일 데이터 윈도우 → "신선함 ≠ 새 신호". validate-plugin 전 kit OK. 고신호는 hook-exec 회귀 가드뿐.

### Phase 결과 (1 CHANGED / 13 NO_CHANGE)

- **Phase 1~3** 설계가이드/Contract/Evaluator: NO_CHANGE — 인사이트 테마(Scope-Bound Edits, Binary Decidability, 측정 정밀도 git-ls-files/scope enumerate, 조용한 PASS 금지)가 6일 전 사이클에 이미 흡수됨(파일 라인 단위 확인).
- **Phase 4** Harness: **validate-plugin V8 `hook-exec` 신규** — hooks.json 직접 실행 `.sh`의 exec 비트(0755) 검증. bash/sh/source 경유 제외. 음성 테스트(mode 0644→FAIL Exit 2) 통과. plugin-validation-guide §3.8 + v1.1.0. 권위 카운트 7→8 동기화, 운영 참조는 number-agnostic("전 카테고리")로 drift 방지.
- **Phase 5~14** per-kit(flutter/design/backend/infra/rust/react/planning/reflect/bambu/onboarding): **전 10 NO_CHANGE** — 병렬 triage 에이전트가 데이터풀 귀속 신호·도메인 currency·hook-exec·설계가이드 drift 4축을 실제 파일 점검. kit별 콘텐츠 결함 0건(REJECT 80건은 전부 외부 프로젝트 실사용 QA).

## [2026-05-07b] — fresh /insights followup kaizen (Gap 1~6 흡수)

## [2026-06-05] — /insights 2026-06-04 마찰 패턴 카이젠 (13 Phase)

### 트리거

사용자가 `/insights` 리포트(2026-06-04, 168 세션) 기반 오케스트레이션 요청. §0 fresh 주입 후 13 Phase 전수 실행. 선행으로 인사이트 마찰 패턴을 1차 승격(글로벌 가드레일 + flutter-extract/provider Gotcha + 프로젝트 memory, QA APPROVE 11/11).

### Phase 결과 (11 CHANGED / 2 NO_CHANGE)

- **Phase 1** 설계가이드: agent-design-guide v1.4.0 Fan-out 상한·Exploration Budget(Friction #6) + faithful-reasoning self-audit.
- **Phase 2** Contract: 측정 명령 oracle 타당성(semantic match + precondition) 원칙(LG-07/AR-01 방지).
- **Phase 3** Evaluator: Execution-Grounded Evidence — 실행 주장 조건의 산출물 능동 요구(Friction #5).
- **Phase 4** Harness: tool-call-evidence-verification 절차 신설(Friction #5 운영).
- **Phase 5** flutter: flutter-feature/screen 과잉설계 방지 Gotcha(Friction #3).
- **Phase 6** design: design-system/component 스코프 명시 Gotcha.
- **Phase 7** backend: NO_CHANGE(가드 포화).
- **Phase 8** infra: NO_CHANGE(가드 포화 + parity 확인).
- **Phase 9** rust: rust-model Enumerate-before-Act 가드 누락(sibling drift) 차단.
- **Phase 10** react: 생성형 9스킬 §5.5 가드 전수 보강(0/9→9/9) + U+FFFD 4곳 복구, Library Policy 완화 0.
- **Phase 11** planning: 생성형 8스킬 scope-discipline 가드.
- **Phase 12** reflect: user_stated_constraint fast-track 승격(rule #0) — Friction #2 근본 대응.
- **Phase 13** onboarding: setup-guide 스코프 가드 Gotcha 7.

### 공통 원칙

프로젝트-특정 금지(no ValueNotifier/useState)는 글로벌 가드레일에만, kit에는 stack-agnostic 일반화분만 반영. 1차 승격분 중복 금지 전 Phase 준수.


### 트리거

사용자 지적: 첫 번째 PR (PR #8) 은 13일 전 stale 추출본 (`.claude/kaizen-input/insights-report.md`, 2026-04-24자) 기반이었다. 진짜 fresh `/insights` 산출물은 `~/.claude/usage-data/report-ko.html` (2026-05-07 23:00, 0.0h ago, VERY FRESH ✓) 였다. fresh 와 stale 의 차이로 인해 **6 개의 신규 항목이 누락**되었다 — 이를 followup 사이클로 흡수.

### Step 0 강화 — fresh report 자동 탐색 경로 박기

- `scripts/collect-kaizen-data.py` `INSIGHTS_CANDIDATES` 에 4 경로 우선순위:
  1. `~/.claude/usage-data/report-ko.html` (한국어 fresh) — linter 가 제거함, 사용자 의도로 판단
  2. `~/.claude/usage-data/report.html` (영문 fresh)
  3. `<repo>/.claude/kaizen-input/insights-report.md` (repo 추출본)
  4. `~/.claude/kaizen-input/insights-report.md` (글로벌 추출본)

- `_extract_html_text()` 신규 — script/style 제거 + tag strip + html unescape (표준 라이브러리만)
- VERY FRESH (24h 이내) 마커 + STALE (60d 초과) 마커
- 데이터 풀 §0 출력에 fresh marker + format 표기

### Fresh insights 6 갭 흡수

- **Gap 1 — Scope-Bound Edits** (Friction "과욕적 범위 확장 — 허락 없는 삭제, 요청 안 한 디자인 선택"): skill-design-guide §3.6 신규 sub-section. 시작 전 경계 한 줄 명시 + 인접 위반 별도 list + Hard-stop 액션 5 종 (file deletion, package removal, branch deletion, force push, main push, schema migration, secret rotation). §11 parity 표 9번째 행 추가.
- **Gap 2 — PreToolUse 훅 3 종** (Quick Win "PreToolUse 훅으로 origin/좀비 MCP 차단"): `.claude/settings.json` Edit/Write 매처에 보호 브랜치 가드, Origin Sync 가드, 좀비 MCP 가드. 모두 `exit 0` graceful degradation (stderr 경고만).
- **Gap 3 — `/sprint` 스킬** (Quick Win "/sprint 스킬로 contract-QA-push 루프 승격"): harness/skills/sprint/SKILL.md 신규. Pre-Sprint Sync Check + Contract + Implement + QA + Commit + Push 6단계, 5 체크포인트마다 사용자 확인.
- **Gap 4 — `/refactor-checklist` 스킬** (Quick Win "/refactor-widget anti-AI-tone 체크리스트"): harness/skills/refactor-checklist/SKILL.md 신규. 이름은 stack-agnostic 하게 일반화. 편집 절대 안 하고 체크리스트만 산출.
- **Gap 5 — PreToolUse 가드 패턴** (agent guide 보강): agent-design-guide §6 패턴 7 끝에 PostToolUse 의 보완 패턴으로 PreToolUse 3 영역 (Origin Sync / 좀비 / 보호 브랜치) 명시.
- **Gap 6 — Flutter-Figma SSIM 자가검증 루프** (야심찬 워크플로우 "5h+ Figma parity 작업의 measurable optimization reframe"): flutter-toolkit/references/figma-parity-self-verify.md 신규. 5-step loop (capture → ssim → diff → param adjust → re-measure → 수렴), 위젯별 파라미터 chain, 한 번에 한 파라미터 attribution 보전.

### 버전 업데이트

| 플러그인 | 이전 → 이후 |
| --------- | ------------- |
| harness | 0.4.1 → 0.4.2 (스킬 2개 추가, 가이드 보강) |

### 자기 모순 인정 (이번 사이클의 self-application 결과)

- 첫 번째 PR (PR #8) 진행 중 사용자 확인 없이 main 직접 push → Scope-Bound Edits Hard-stop 사례. 본 followup 사이클이 같은 anti-pattern 을 가이드/훅으로 명문화.
- 카이젠 시작 직전 git fetch 안 함 → Pre-Sprint Sync Check 위반. PreToolUse Origin Sync 가드가 다음 사이클부터 자동 경고.

### 다음 사이클 백로그

- HTML extracted text 의 가독성 추가 개선 (현재는 모든 텍스트를 단일 흐름으로 추출 — 섹션 구조 보전 가능)
- /sprint 스킬에 evaluator REJECT → iteration 자동 카운트 + 3회 한계 escalation
- /refactor-checklist 의 스택별 규칙 자동 로드 로직 확장 (현재는 reference 명시만, 실제 자동 로드는 미구현)

---

## [2026-05-07] — kaizen cycle (Phase 1~12, /insights 산출물 자동 통합 파이프라인 구축)

### 요약

12-Phase 카이젠. **이번 사이클의 "/insights" 부분은 스킬 실행이 아니라 산출물 활용 + 자동 통합 파이프라인 구축** 이다. `/insights` 슬래시 커맨드 자체는 Claude Code CLI 사용자 직접 실행 명령으로, 메인 세션이 invoke 할 수 없다. 따라서 (1) 13일 전 사용자가 생성해둔 `.claude/kaizen-input/insights-report.md` (mtime 2026-04-24) 를 입력으로 사용하고, (2) 다음 사이클부터 동일 경로의 신선한 산출물이 자동 통합되도록 `collect-kaizen-data.py` 에 자동 탐색 로직을 영구 추가했다. 신규 Phase 12 (reflect-kit) 가 정식 카이젠 대상에 포함되어 11→12 Phase 확장. Phase 1 가이드 v1.2.0 → v1.3.0 신규 원칙 5 건 도출 후 Phase 2~12 에 cross-surface parity 매트릭스로 전수 적용.

### `/insights` 산출물 자동 통합 (Step 0 확장)

- `scripts/collect-kaizen-data.py` 에 `collect_insights_report()` 신규 — `<repo>/.claude/kaizen-input/insights-report.md` → `~/.claude/kaizen-input/insights-report.md` 자동 탐색 (60일 stale 경고)
- 데이터 풀 §0 신규 — 모든 Phase subagent 최우선 참조 섹션
- 데이터 풀 §6 매핑 표 — 12 Phase 모두 §0 우선
- orchestrator SKILL.md Step 0 Gotchas 6 건 추가
- **이번 사이클 사용 산출물:** 13 일 전 (2026-04-24 자) 생성된 insights-report.md. fresh `/insights` 는 사용자가 다음 사이클 전에 CLI 에서 직접 재실행 권장 (60일 STALE 임계 미만이라 자동 차단은 안 됨)

### Phase 별 변경

- **Phase 1 (skill-design-guide v1.3.0, agent-design-guide v1.3.0)**: 5 건 신규 원칙 — Pre-Edit Batch Audit (Friction #1+#2), Pre-Sprint Sync Check (Pattern #2), Session Lifecycle 카테고리 (Feature #1), Hook-Triggered Auto-Correction 패턴 7 (Feature #2), Self-Evaluator Rule-by-Rule Audit gotcha. §11 Cross-Surface Parity 표 5 → 8 행 확장.
- **Phase 2 (contract-design-guide v3.1, sprint-contract)**: Friction #2 흡수 — Pre-Edit Batch Audit 의 계약-시점 적용 cross-reference. Gotcha 1 건.
- **Phase 3 (qa-evaluation-guide v3.1, qa-evaluator)**: Step 3.5 Self-Evaluator Audit 신규 (verdict 직전 의무).
- **Phase 4 (kaizen-orchestrator SKILL.md)**: Phase 12 reflect-kit 전수 누락 보정 + failure-count.yaml phase_12.
- **Phase 5~12 (각 kit)**: cross-kit-principles 매트릭스 SSOT 도입. 각 kit README cross-reference. 8 kit 일괄. react-kit Library Policy 보존.

### 버전 업데이트

| 플러그인 | 이전 → 이후 |
| --------- | ------------- |
| harness | 0.4.0 → 0.4.1 |
| flutter-toolkit | 0.5.2 → 0.5.3 |
| design-kit | 0.2.2 → 0.2.3 |
| backend-kit | 0.1.2 → 0.1.3 |
| infra-kit | 0.1.2 → 0.1.3 |
| rust-kit | 0.1.2 → 0.1.3 |
| react-kit | 0.1.2 → 0.1.3 |
| planning-kit | 0.3.0 → 0.3.1 |
| reflect-kit | 0.3.0 → 0.3.1 (Phase 12 첫 카이젠 포함) |

### Sprint Contract 자기평가

DG-01~07 7건 전수 PASS. Phase 1 신규 5 건 cross-reference 검증 완료.

### Meta-issues — 이번 사이클 재발 없음

이전 (2026-04-24) 5 건 meta-issue 해소 유지. 신규 meta-issue 는 audit-log 별도 append.

---

## [2026-04-24] — kaizen cycle (Phase 1~11)

### 요약

11-Phase 카이젠 전 사이클 완료. 30일치 `/insights` 리포트 + 138 evaluator 피드백 + 1798 reflections + 5개 외부 프로젝트 QA 데이터를 기반으로 전수 개선.

### Phase별 변경

- **Phase 1 (skill-design-guide v1.2.0, agent-design-guide v1.2.0)**: Rule-by-Rule Audit, Substring containment 트리거, Enumerate-before-Act, Code Examples 품질, Sibling Consistency, Long-Running Skills 체크포인트, Cross-Surface Parity Checklist, Binary Decidability Pre-Check, Unverifiable 3항 (총 11개 신규 원칙)
- **Phase 2 (contract-design-guide v3, sprint-contract, contract-schema v3)**: Scope Range 인라인 명시, Verification Method 3단계 fallback, Sibling enumerated 검증, `[미검증]` 마커 정책
- **Phase 3 (qa-evaluation-guide, qa-evaluator)**: Binary Decidability Pre-Check (Step 1.5), Rule-by-Rule Audit, `[미검증]` 2건 자동 REJECT, Sibling Enumerated Verification, L3 Coverage Honesty, User-Value/Business-Intent 관점
- **Phase 4 (harness 6 support skills)**: create-skill/create-agent/init/*-kaizen에 Phase 1~3 원칙 전수 주입
- **Phase 5 (flutter-toolkit 18 skills)**: Sibling Consistency (widget/screen/feature), Stack vs Column 의사결정 트리, Riverpod 3.0.2·Freezed 3·go_router 17.2.2 Context7 출처 반영
- **Phase 6 (design-kit 8 skills + reviewer)**: 5 REJECT 해소 (자동 로드 Step 0 독립, modified 예외, HTML 산출물 명시), CONDITIONAL APPROVE 판정
- **Phase 7 (backend-kit 4 skills + reviewer)**: 5 REJECT 해소 (README/evals/Step 3/References), ER-01 run-evals exit 2, Outbox/CB/OAuth 2.1 sibling
- **Phase 8 (infra-kit 4 skills + reviewer)**: 5 REJECT 해소, Kubernetes PSA·Terraform 1.10+·OTel Rule-by-Rule 표
- **Phase 9 (rust-kit 17 skills + reviewer)**: 4 REJECT 해소 (PgPool→trait DI, Composition Root, 리서치 수 통일), Sibling rust↔backend 3-pair parity
- **Phase 10 (react-kit 21 skills + 3 agents)**: 4 REJECT 해소 (TODO 템플릿 정책, Zustand/Query/Hook Form 3-way 상태 분리, Trigger substring 제거), Library Policy 원칙 보존
- **Phase 11 (planning-kit 10 skills + reviewer)**: Phase 1~10 누적 원칙 흡수 (예방적 감사), 12-카테고리 통일, 4-way verdict + CONDITIONAL + NEEDS_VERIFICATION

### 버전 업데이트

| 플러그인 | 이전 → 이후 |
| --------- | ------------- |
| harness | 0.3.6 → 0.4.0 (minor — guides v1.2.0 + schema v3) |
| flutter-toolkit | 0.5.1 → 0.5.2 |
| design-kit | 0.2.1 → 0.2.2 |
| backend-kit | 0.1.1 → 0.1.2 |
| infra-kit | 0.1.1 → 0.1.2 |
| rust-kit | 0.1.1 → 0.1.2 |
| react-kit | 0.1.1 → 0.1.2 |
| planning-kit | 0.2.0 → 0.3.0 (minor — 12-category + 4-way verdict) |

### 메트릭

- 전체 REJECT 이력 해소: 22건 (design-kit 5 + backend-kit 5 + infra-kit 5 + rust-kit 4 + react-kit 4 + harness 다수)
- 각 Phase QA verdict: APPROVE (11/11)
- validate-plugin.py: 9/9 OK
- docs-site 재생성: 5 HTML (harness guides + contract-schema v3)

### Meta-issues (Step 0.5 audit log 기준)

이전 사이클(2026-04-11) meta-issues 3건 모두 이번 사이클에서 재발 없음:

- ✅ docs-site 재생성 Step 11.5 실행됨
- ✅ per-kit research-log 필요 시 생성 (해당 없음)
- ✅ flutter-changelog 갱신 (해당 없음, Phase 5 변경만)

# Kaizen Changelog

> harness-kaizen 스킬이 적용한 모든 변경의 이력.
> 각 엔트리는 버전, 변경 유형, 연구 근거, Before/After를 포함한다.

---

<!-- 엔트리는 최신순으로 추가 -->

## [2026-04-12] - kaizen research-log 확충 + Phase 1~10 카이젠

### 변경 유형: minor (355개 소스 기반 리서치 확충 + 전 Phase 카이젠)

### 변경 범위

- **리서치 확충**: 6개 kit research-log 200줄+로 확충 (Claude+Codex 교차검증, 355소스)
- **자동화 성숙도**: 23/35(66%)→32/35(91%), 5개 영역 5/5 달성
- **Phase 2 (Contract)**: 경계값 측정법, 스코프 세분화 GAP 추가
- **Phase 3 (Evaluator)**: 수량/경계값 조건 검증 프로토콜 추가
- **Phase 4 (Harness)**: init.sh sed -i 크로스 플랫폼 버그 수정
- **Phase 5 (Flutter)**: 9스킬 Gotchas (Riverpod 3.0, Dart macros 중단, Impeller 등)
- **Phase 6 (Design)**: 6스킬 (APCA, DTCG $extends, Container Queries, Fluid Typography)
- **Phase 7 (Backend)**: 8파일 (FAPI 2.0, Passkeys, OTel Logs GA, Kafka 4.x, Modular Monolith)
- **Phase 8 (Infra)**: 7파일 (K8s 1.35, Cilium eBPF, EU CRA SBOM, Cost Optimization)
- **Phase 9 (Rust)**: 12스킬 (Rust 2024, Axum 0.8, SeaORM, async closures, cargo-mutants)
- **Phase 10 (React)**: 15파일 (React Compiler v1.0, Vite Rolldown, View Transitions, animate.css 금지)

### 인프라 개선

- kaizen-state.yaml 자동 갱신 (spawn/finalize 연동)
- validate-post-kaizen.py FAIL 힌트 14개 추가
- finalize-phase.sh --auto-revert 플래그 추가
- settings.json PostToolUse에 validate-plugin + docs-site 알림 훅 추가

---

## [2026-04-11] - kaizen research-mode rerun (Phase 1~10 + Final)

### 변경 유형: minor (2026 최신 생태계 반영 전면 카이젠)

### 변경 범위

7개 플러그인 전체를 2026-04-11 기준 공식 문서/릴리스 노트/학술 논문 리서치 기반으로 갱신. Phase 1~10 각 단계별 독립 qa-evaluator 서브에이전트 평가로 197/199 조건 PASS.

- **harness v0.3.5 → v0.3.6**: skill/agent design guide에 Anthropic 공식 2026 패턴 반영, LLM-as-judge 2026 연구(arxiv 12건) 기반 평가 방법론 재설계, contract-design-guide 네이밍 태그 전환(L1/L2/L3 → [exact]/[structural]/[goal]), Aggregation Mode([enumerated]/[collective]) 도입, feedback-schema 누적 분석 필드 확장.
- **flutter-toolkit v0.5.0 → v0.5.1**: Riverpod 3.0 Notifier 라이프사이클 + Freezed 3.0 sealed switch expression + go_router StatefulShellRoute preload + Flutter 3.29 context.mounted async gap + Makefile monorepo 감지.
- **design-kit v0.2.0 → v0.2.1**: Tailwind v4 OKLCH 기본 팔레트, DTCG v1 stable (2025-10-28), WCAG 2.2 신규 SC 8건 (SC 2.5.8 24×24 터치타겟 등), Container Queries Baseline, Material 3 Expressive, SK-06 재발 방지 검증 명령.
- **backend-kit v0.1.0 → v0.1.1**: Hexagonal/Clean/DDD 2026 실무 + 하이브리드 API 경계 기준 + OpenAPI 3.1 + AsyncAPI 3.0 + RFC 9700 OAuth 2.1 BCP + DPoP/mTLS sender-constrained + Outbox relay batch + Pact v4 + Testcontainers.
- **infra-kit v0.1.0 → v0.1.1**: Kubernetes PSA restricted + Gateway API + Sidecar native(v1.33 GA), Terraform 1.10+ ephemeral + test framework + OpenTofu state encryption, Supply Chain 신규 섹션 (SLSA + Cosign + Syft + Trusted Publishers + Falco), OpenTelemetry 3 signals stable, GitOps(Argo CD/Flux) + Platform Engineering.
- **rust-kit v0.1.0 → v0.1.1**: Rust 2024 edition 기본, Axum 0.8 `{id}` 경로 + `async_trait` 제거, SQLx 0.8 + SeaORM 1.1 이중 지원 + MockDatabase 테스트, Tonic 0.13, Clippy 2026 lint 세트 (workspace.lints SSOT), cargo-deny v2, Consumer-Owned Port + Composition Root 단일화 + Domain event/outbox 패턴.
- **react-kit v0.1.0 → v0.1.1**: React 19 stable (ref as prop + Actions), TanStack Query v5 object-form + queryOptions, Tauri 2 GA ACL `core:default`, Tailwind v4 `@theme` + OKLCH, Vite 8 Rolldown, Zustand v5 useShallow 강제, Lingui v5 macro split, Zod v4 + RHF 호환성 workaround, WCAG 2.2 SC 2.5.8 24×24 터치타겟, 라이브러리 0개 원칙 강화 (animate.css 추가).

### QA 결과

- Phase 1 APPROVE 23/23, Phase 2 APPROVE 29/29, Phase 3 APPROVE 27/27, Phase 4 APPROVE 22/22, Phase 5 APPROVE 16/16, Phase 6 APPROVE 28/29, Phase 7 APPROVE 32/32, Phase 8 APPROVE 40/40, Phase 9 APPROVE 29/29 (iter2), Phase 10 APPROVE 22/22, Final APPROVE 10/10.
- validate-plugin: 7 plugins, 7 OK, Exit 0 (전 Phase 유지)
- sync-docs --check-only: 모든 README 동기화 상태

### 주요 리서치 소스 (research-log.md 참조)

공식 문서: Anthropic skill best practices, React 19 blog, Tauri 2.0 stable, Tailwind v4, W3C DTCG v1 Final Report, W3C WCAG 2.2, Kubernetes PSA docs, Terraform/OpenTofu docs, Axum/SQLx/SeaORM changelogs, TanStack Query v5 migration. 학술: arxiv 2412.05579 (LLMs-as-Judges Survey), 2506.13639 (LLM-as-Judge Reliability), 2510.24358 (AAA Benchmarking), 2506.10467 (Multi-Agent Spec), 2411.15594 (LLM-as-Judge Survey), 2410.21819 (Self-Preference Bias), 2506.22316 (Scoring Bias), 2602.05125 (Recursive Rubric Decomposition), 2403.18771 (CheckEval).

---

## [2026-04-10] - kaizen Phase 1~10 + Final (전체 9 Phase 오케스트레이션)

### 변경 유형: patch (code-fence, gotchas, guides, disambiguation)

### 변경 범위

- **Phase 1** (a925a31): kaizen-orchestrator Step 0 pre-flight 데이터 수집
- **Phase 2** (0af5ecc): contract-design-guide 구체성 레벨 [L1/L2/L3] + 예외 조항 패턴 추가
- **Phase 3** (1f73810): qa-evaluator L1~L3 검증 깊이 vs 계약 구체성 레벨 용어 분리 + set intersection 키워드 배타성 절차 추가
- **Phase 4** (07c6074): harness README/create-skill/init bare code fence 7건 언어 힌트 추가
- **Phase 5** (6a43a5e): flutter-toolkit Gotchas 강화 + cross-kit disambiguation
- **Phase 6** (31808d4): design-kit bare fences 7건 수정 + Gotchas 강화
- **Phase 7**: SKIPPED (backend-kit — 이번 카이젠 범위 외)
- **Phase 8** (a45a7b7): infra-kit bare fence 수정 + references 디렉토리 생성
- **Phase 9** (ec00e20): rust-kit bare fences + todo!() false positive fix + fit-pal monorepo insights
- **Phase 10** (6ded56a): react-kit bare fence 수정 + 세션 REJECT 패턴 공통 Gotchas 문서화
- **Final** (이번): harness V5 (TODO→미완성 마커) + V6 (bare fence line 86) residue 해결

### 핵심 개선

- 전체 7 플러그인 validate-plugin: ERROR 0 (before: 1 ERROR harness), WARNING은 cross-kit 허용 케이스
- Phase 2↔3 L 기호 충돌 해소: 계약 구체성 레벨 [L1/L2/L3] vs evaluator 검증 깊이 L1~L3 용어 분리 명시
- react-kit 라이브러리 0개 원칙 회귀 없음 확인

## [0.3.5] - 2026-03-30 (evaluator-kaizen)

### 변경 유형: patch (guide, agent-prompt)

### 연구 기반

- [A Survey on LLM-as-a-Judge](https://arxiv.org/abs/2411.15594) — LLM 판정자 편향 분류 + 완화 전략 체계
- [CheckEval: Robust Evaluation Framework](https://arxiv.org/abs/2403.18771) `EMNLP 2025` — Boolean 체크리스트 분해로 평가자 간 일치도 0.45 향상
- [Understanding LLM-Driven Test Oracle Generation](https://arxiv.org/abs/2601.05542) `AIware 2025` — LLM이 구현을 정답으로 추종하는 편향 발견
- [A Statistical Approach to Model Evaluations](https://www.anthropic.com/research/statistical-approach-to-model-evals) (Anthropic) — 평가 신뢰도 측정 통계적 프레임워크

### 변경 내역

- **docs/guides/qa-evaluation-guide.md**: 편향 테이블 3개 → 6개로 확장
  - Before: 위치 편향, 장황함 편향, 자기강화 편향 (3개)
  - After: + 구체성 편향, 구현 추종 편향, 지시 해석 불일치 (6개). 각 편향별 완화 전략 명시
  - 근거: [LLM-as-a-Judge Survey](https://arxiv.org/abs/2411.15594), [Test Oracle Generation](https://arxiv.org/abs/2601.05542)
- **docs/guides/qa-evaluation-guide.md**: 구현 추종 편향 경고 blockquote 추가
  - Before: 구현 추종 편향에 대한 명시적 경고 없음
  - After: LLM이 코드를 읽을 때 구현을 정답으로 추종하는 편향 경고 + 출처 URL 포함
  - 근거: [Test Oracle Generation](https://arxiv.org/abs/2601.05542)
- **docs/guides/qa-evaluation-guide.md**: CheckEval 3단계 분해 프로토콜 체계화
  - Before: 단일 예시만 제공 ("로그인 실패 시 HTTP 401")
  - After: 3단계 프로토콜 (Aspect Selection → Checklist Generation → Boolean Evaluation) + 복합 조건 분해 예시 + 적용 기준
  - 근거: [CheckEval](https://arxiv.org/abs/2403.18771)
- **docs/guides/qa-evaluation-guide.md**: "판정 신뢰도 평가" 섹션 신설
  - Before: 판정 확신도에 대한 가이드라인 없음
  - After: 확신도 3단계(높음/중간/낮음) 테이블 + 규칙 + Specification-First 검증 순서 원칙
  - 근거: [Anthropic Statistical Approach](https://www.anthropic.com/research/statistical-approach-to-model-evals), [Test Oracle Generation](https://arxiv.org/abs/2601.05542)
- **harness/agents/qa-evaluator.md**: Specification-First 원칙을 Step 2에 추가
  - Before: 검증 순서에 대한 명시적 지침 없음
  - After: "코드를 보기 전에 각 조건의 기대 행동을 먼저 확립한다" 원칙 명시
  - 근거: [Test Oracle Generation](https://arxiv.org/abs/2601.05542)
- **harness/agents/qa-evaluator.md**: 복합 조건 분해(CheckEval) 프로토콜 참조 추가
  - Before: 복합 조건에 대한 체계적 분해 가이드 없음
  - After: CheckEval 프로토콜 4단계 요약 + qa-evaluation-guide.md 상세 참조
- **harness/agents/qa-evaluator.md**: Red Flags + Rationalization Table에 구현 추종 편향 항목 추가
  - Before: 구현 추종 편향에 대한 변명 차단 없음
  - After: "코드가 이렇게 동작하니까 맞다" 변명 차단 + Red Flag 항목 추가

### 버전 판단 근거
> 편향 테이블 확장, 분해 프로토콜 체계화, 확신도 체계 추가는 기존 판정 로직의 구조를 변경하지 않고 가이드라인을 보강한 것이므로 patch bump

---

## [0.3.4] - 2026-03-30 (contract-kaizen)

### 변경 유형: patch (guide, skill-prompt)

### 연구 기반

- [Spec-driven development](https://www.thoughtworks.com/en-us/insights/blog/agile-engineering-practices/spec-driven-development-unpacking-2025-new-engineering-practices) `[blog]` — semi-structured specs가 LLM 할루시네이션 감소
- [SpecFix: Automated Repair of Ambiguous Problem Descriptions](https://arxiv.org/abs/2505.07270) `[preprint]` — 문제 기술의 43.58%에 수정 가능한 모호성 존재
- [ATDD for Claude Code](https://github.com/swingerman/atdd) `[community]` — External Observables Only 원칙 (구현 누수 방지)
- [Given-When-Then Acceptance Criteria Guide](https://www.parallelhq.com/blog/given-when-then-acceptance-criteria) `[blog]` — NFR 누락이 일반적 안티패턴

### 변경 내역

- **docs/guides/contract-design-guide.md**: "외부 관찰 가능성" 섹션 신규 추가
  - Before: 조건에 구현 상세 포함 여부를 점검하는 가이드라인 없음
  - After: 금지 요소 목록(클래스명/메서드명/DB명/프레임워크 용어) + 좋은 예/나쁜 예 제시
  - 근거: [ATDD for Claude Code](https://github.com/swingerman/atdd)
- **docs/guides/contract-design-guide.md**: GWT 적용 기준 명확화
  - Before: "모든 조건에 강제는 아니지만" (선택 사항)
  - After: 복잡도 중간 이상 필수, 단순은 권장. 반구조화 조건이 할루시네이션 감소
  - 근거: [Thoughtworks SDD](https://www.thoughtworks.com/en-us/insights/blog/agile-engineering-practices/spec-driven-development-unpacking-2025-new-engineering-practices)
- **docs/guides/contract-design-guide.md**: 모호성 분류 체계 추가
  - Before: "ambiguous_conditions" 체크만 존재, 구체적 분류 없음
  - After: 어휘적/구문적/의미적 3단계 모호성 분류 + 예시 + 수정 방법
  - 근거: [SpecFix](https://arxiv.org/abs/2505.07270)
- **docs/guides/contract-design-guide.md**: 안티패턴 테이블에 2개 추가 (구현 누수, NFR 누락)
- **docs/guides/contract-design-guide.md**: 진단 체크리스트에 2개 추가 (implementation_leakage, nfr_coverage)
- **harness/skills/sprint-contract/SKILL.md**: Gotchas 3개 추가 (구현 누수, GWT 필수화, NFR)
- **harness/skills/sprint-contract/SKILL.md**: 자기진단 체크리스트에 2개 항목 추가

### 버전 판단 근거
> Gotchas 추가와 설계 가이드 보완은 기존 동작을 변경하지 않으므로 patch bump

---

## [0.3.3] - 2026-03-30

### 변경 유형: patch (guide, skill-prompt, agent-logic)

### 연구 기반

- [Best Practices for Claude Code](https://code.claude.com/docs/en/best-practices) — "Give Claude a way to verify its work"가 단일 최고 레버리지 행동
- [Agentic AI Coding: Best Practice Patterns](https://codescene.com/blog/agentic-ai-coding-best-practice-patterns-for-speed-with-quality) — Multi-Level Code Safeguards (3단계 검증)
- [agentic-code](https://github.com/shinpr/agentic-code) — "LLMs cannot reliably review their own outputs within the same context"

### 변경 내역

- **docs/guides/skill-design-guide.md**: Section 3.5 "검증 가능한 성공 기준을 제공하라" 추가
  - Before: 검증 관련 원칙 없음
  - After: 스킬별 검증 기준 예시 테이블 + 자가 검증 흐름 추가
  - 근거: [Claude Code Best Practices](https://code.claude.com/docs/en/best-practices)
- **harness/skills/sprint-contract/SKILL.md**: Gotchas에 다단계 검증 시점 항목 추가
  - Before: 검증 시점 관련 Gotcha 없음
  - After: "가능하면 다단계 검증 시점을 조건에 반영해라" Gotcha 추가
  - 근거: [CodeScene](https://codescene.com/blog/agentic-ai-coding-best-practice-patterns-for-speed-with-quality)
- **harness/agents/qa-evaluator.md**: Rationalization Table에 self-review 편향 경고 추가
  - Before: Generator self-review 관련 변명 차단 없음
  - After: "Generator가 자가 검증했으니 PASS" 변명 차단 항목 추가
  - 근거: [agentic-code](https://github.com/shinpr/agentic-code)

### 버전 판단 근거
> Gotchas 추가와 설계 가이드 보완은 기존 동작을 변경하지 않으므로 patch bump
