# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

Claude Code 플러그인 모노레포. 세 개의 플러그인을 포함한다:

<!-- AUTO:summary -->
- **harness** — 스택 무관 범용 QA 프레임워크 (Sprint Contract + QA Evaluator)
- **flutter-toolkit** — Flutter 전용 개발 워크플로우 스킬 18종
- **design-kit** — 스택 무관 UI/UX 디자인 플러그인 (디자인 시스템 세팅 + 실시간 가이드 + 감사)
- **backend-kit** — 스택 무관 백엔드 개발 가이드, 감사, 아키텍처 세팅 플러그인
- **infra-kit** — 스택 무관 인프라/DevOps 가이드, 감사, 초기 세팅 플러그인
- **rust-kit** — Rust 전용 백엔드 개발 워크플로우 플러그인 — 프로젝트 스캐폴딩, API 생성, 모델 관리, 빌드/테스트/감사 자동화
- **react-kit** — React + Vite + Tauri 2 + Rust WASM 전용 개발 워크플로우 플러그인 — 21종 스킬 + 3 에이전트, 라이브러리 0개 애니메이션, Clean Architecture, Strict TypeScript 강제
<!-- /AUTO:summary -->

## Commands

```bash
# 문서 동기화 (스킬/에이전트/설정 변경 후 README 갱신)
python scripts/sync-docs.py              # 전체 동기화
python scripts/sync-docs.py harness      # 특정 플러그인만
python scripts/sync-docs.py --check-only # 변경 필요 여부만 확인
python scripts/sync-docs.py --dry-run    # 미리보기

# 플러그인 릴리스 (버전 bump + marketplace.json 갱신 + git commit/tag/push)
bash scripts/release.sh <plugin-name> <patch|minor|major>
# 예: bash scripts/release.sh harness patch

# harness 환경 검증
bash harness/scripts/env-check.sh

# 피드백 시스템 테스트
bash harness/evals/kaizen/feedback-system/save-test.sh
bash harness/evals/kaizen/feedback-system/aggregation-test.sh

# 카이젠 수동 실행
# /kaizen — 전체 10 Phase 오케스트레이션 (설계 가이드 → contract → evaluator → harness → flutter → design → backend → infra → rust → react → Final)
# /contract-kaizen — sprint-contract만 개선
# /evaluator-kaizen — qa-evaluator만 개선

# flutter-toolkit evals
# evals.json (flutter-toolkit/evals/evals.json) 참조 — 19개 테스트 케이스

# 플러그인 검증 (7-카테고리 자동 검사)
python3 scripts/validate-plugin.py                          # 전체 7 킷
python3 scripts/validate-plugin.py react-kit                # 특정 킷
python3 scripts/validate-plugin.py --check=refs,placeholders # 특정 체크
python3 scripts/validate-plugin.py --fix                    # 자동 수정 (placeholders + code-fence 만)
# 가이드: harness/docs/guides/plugin-validation-guide.md
```

## Architecture

### Plugin Structure

각 플러그인은 동일한 레이아웃을 따른다:

```
<plugin>/
├── .claude-plugin/plugin.json   # 메타데이터 (name, version, author)
├── skills/<name>/SKILL.md       # 스킬 정의 (frontmatter + process)
├── agents/                      # 독립 에이전트
├── hooks/                       # SessionStart/PreToolUse 훅 (선택)
├── evals/                       # 테스트 픽스처 및 assertions
├── references/                  # 공유 참조 문서 (선택, 스킬 내부에 둘 수도 있음)
├── templates/                   # 초기화 템플릿 (선택)
├── scripts/                     # 유틸리티 셸 스크립트 (선택)
└── README.md
```

### Marketplace Registry

`.claude-plugin/marketplace.json`이 모든 플러그인을 등록한다. 릴리스 시 `scripts/release.sh`가 이 파일의 version과 description 날짜를 자동 갱신한다.

### 문서 자동 동기화

`scripts/sync-docs.py`가 SKILL.md frontmatter, agents/*.md, plugin.json, hooks.json 등에서 데이터를 추출하여 README의 `<!-- AUTO:xxx -->` 마커 사이를 자동 갱신한다. PostToolUse 훅(`.claude/settings.json`)이 Edit/Write 후 `--check-only`를 실행하여 동기화 필요 시 알림한다.

### Harness Core Flow

1. `/harness init` → `.harness/project.yaml` 생성
2. `/sprint-contract` → 구현 전 완료 조건 정의
3. 개발 수행
4. `qa-evaluator` 에이전트 → Contract 기준 APPROVE/REJECT 판정
5. 자기진단 + 교차 진단 → 글로벌 피드백 저장 (`~/.harness/feedback/`)

`project.yaml`이 핵심 설정 파일: stack, commands, contract_categories, anti_patterns를 정의한다.

### Kaizen Orchestration

10 Phase 순서: 설계 가이드 → contract-kaizen → evaluator-kaizen → harness-kaizen → flutter-kaizen → design-kaizen → backend-kaizen → infra-kaizen → rust-kaizen → react-kaizen. 각 Phase는 자체 리서치를 수행하며 독립 서브에이전트로 실행한다. 전체 Phase 완료 후 Final 단계에서 교차 정합성 검증을 수행한다.

가이드 문서 (`harness/docs/guides/`): `skill-design-guide.md`, `agent-design-guide.md`, `contract-design-guide.md`, `qa-evaluation-guide.md`. 공유 참조 (`harness/references/`): `contract-schema.md` (계약 포맷), `feedback-schema.yaml` (피드백 스키마). 피드백 스크립트: `harness/scripts/feedback-path.sh`, `save-feedback.sh`, `verify-feedback.sh`, `trigger-check-common.sh`.

### Skill Format

모든 스킬은 `SKILL.md` 파일 하나로 구성된다:

```yaml
---
name: skill-name
description: >
  트리거 키워드 포함 설명
argument-hint: "[optional]"
user-invocable: true
---
```

본문에는 Gotchas(반복 실수 방지), Process(단계별 실행), References(참조 파일) 섹션이 있다.

### Flutter Toolkit Integration

flutter-toolkit 스킬들은 `references/project-detection.md`를 통해 프로젝트 환경을 자동 감지한다 (FVM 래퍼, 아키텍처 패턴, 의존성 등). harness의 `.harness/project.yaml`과 연동하여 commands와 anti_patterns를 공유한다.

## Skills Reference

### 이 레포 스킬 (플러그인 소속)

**harness — QA 프레임워크**

| 스킬/에이전트 | 용도 |
|---------------|------|
| `/init` | `.harness/` 디렉토리 초기화 + project.yaml 생성 |
| `/sprint-contract` | 구현 전 완료 조건 정의. 기능 구현 요청 시 가장 먼저 실행 |
| `qa-evaluator` (에이전트) | Sprint Contract 기준 APPROVE/REJECT 판정. 구현 완료 후 실행 |
| `/create-skill` | skill-design-guide 기반 새 SKILL.md 스캐폴딩 |
| `/create-agent` | agent-design-guide 기반 새 에이전트 .md 스캐폴딩 |
| `/contract-kaizen` | sprint-contract 스킬 + 계약 설계 가이드 개선 |
| `/evaluator-kaizen` | qa-evaluator 에이전트 + 평가 방법론 가이드 개선 |
| `/harness-kaizen` | harness 스킬 전체 개선 |

**flutter-toolkit — Flutter 개발 워크플로우 (18종)**

| 스킬/에이전트 | 용도 |
|---------------|------|
| `/flutter-screen` | Screen/Page 위젯 생성 + 라우터 등록 |
| `/flutter-feature` | 화면+Provider+API를 한 번에 생성하는 복합 스킬 |
| `/flutter-widget` | 프로젝트 컨벤션에 맞는 커스텀 위젯 생성 |
| `/flutter-provider` | Riverpod Notifier + State 클래스 생성 |
| `/flutter-api` | Clean Architecture 전 레이어 일괄 생성 (DataSource→Model→Repository→UseCase) |
| `/flutter-test` | unit/widget/integration 테스트 코드 자동 생성 |
| `/flutter-hooks` | Flutter Hooks 패턴 가이드 (HookWidget, 커스텀 Hook) |
| `/flutter-error` | 에러 처리 패턴 가이드 (예외→Failure→UI 표시) |
| `/flutter-l10n` | i18n 번역 문자열 추가/수정 + codegen 재생성 |
| `/flutter-responsive` | 반응형 레이아웃 적용 (breakpoint, 멀티컬럼) |
| `/flutter-transition` | 커스텀 페이지 전환 애니메이션 적용 |
| `/flutter-skeleton` | 스켈레톤 shimmer 로딩 UI 구현 |
| `/flutter-extract` | 재사용 위젯을 공용으로 추출·분리 |
| `/flutter-build` | 코드 생성(build_runner) + 정적 분석(analyze) |
| `/flutter-run` | 빌드 프리미티브 개별 실행 (codegen, analyze, fix, test) |
| `/flutter-preflight` | Pre-commit quality gate (fix→codegen→analyze→test) |
| `/flutter-audit` | 코드 품질 감사 — pre-commit 리뷰, PR 전 검토 (quick/deep 모드) |
| `/flutter-kaizen` | flutter-toolkit 스킬 개선 |
| `widget-inspector` (에이전트) | 프로젝트 코드에서 재사용 가능한 위젯 패턴 감지·리포팅 |

**design-kit — UI/UX 디자인**

| 스킬/에이전트 | 용도 |
|---------------|------|
| `/design-guide` | UI 코드에 대한 디자인 원칙 가이드 (가벼운 리뷰) |
| `/design-audit` | 완성된 UI를 카테고리별 PASS/FAIL로 체계적 감사 |
| `/design-system` | 디자인 토큰 체계(컬러, 타이포, 스페이싱 등) 세팅 |
| `design-reviewer` (에이전트) | design-audit에서 호출. UI 코드를 디자인 원칙 기준으로 독립 평가 |

**rust-kit — Rust 백엔드 개발 워크플로우 (17종)**

| 스킬/에이전트 | 용도 |
|---------------|------|
| `/rust-init` | 프로젝트 스캐폴딩 (workspace + toolchain + hexagonal 구조) |
| `/rust-feature` | feature 모듈 스캐폴딩 |
| `/rust-api` | Axum 라우터/핸들러 + utoipa OpenAPI |
| `/rust-model` | SQLx 모델 + 마이그레이션 |
| `/rust-service` | 비즈니스 로직 서비스 레이어 |
| `/rust-auth` | JWT/OAuth 인증 레이어 |
| `/rust-middleware` | Axum 미들웨어 (CORS, logging, rate-limit) |
| `/rust-grpc` | tonic gRPC 서비스 |
| `/rust-test` | 테스트 코드 생성 (unit + integration) |
| `/rust-docker` | Dockerfile + docker-compose |
| `/rust-error` | 에러 처리 패턴 가이드 (thiserror/anyhow) |
| `/rust-l10n` | 백엔드 i18n (rust-i18n/fluent) |
| `/rust-run` | 빌드 프리미티브 개별 실행 (build, clippy, fmt, test, audit, check) |
| `/rust-build` | cargo build + clippy (rust-run wrapper) |
| `/rust-preflight` | pre-commit gate (fmt → clippy → test → audit) |
| `/rust-audit` | 코드 품질 감사 (quick/deep 모드) |
| `rust-reviewer` (에이전트) | rust-audit에서 호출. 읽기 전용 독립 평가 |

**react-kit — React + Vite + Tauri 2 + Rust WASM 개발 워크플로우 (21종 + 3 에이전트)**

| 스킬/에이전트 | 용도 |
|---------------|------|
| `/react-init` | 프로젝트 스캐폴딩 (Vite + Tauri 2 + React 19 + TS strict + Tailwind v4 + shadcn + TanStack Router + Zustand + TanStack Query + Lingui + Rust WASM) |
| `/react-screen` | TanStack Router 파일 기반 화면/라우트 추가 |
| `/react-feature` | Clean Arch 4계층 복합 생성 (domain → data → presentation → infrastructure) |
| `/react-widget` | shadcn 기반 cva variant 컴포넌트 + Container Queries |
| `/react-store` | Zustand v5 스토어 (클라이언트 상태 전용) |
| `/react-api` | Clean Arch 4계층 API (datasource → model → repository → usecase) + neverthrow Result |
| `/react-query` | TanStack Query v5 훅 (queryKey 팩토리 + invalidation 전략) |
| `/react-form` | React Hook Form + Zod resolver + setError('root.serverError') |
| `/react-wasm` | Rust WASM 바인딩 (wasm-pack + Comlink Worker), WASM 카탈로그 기반 이식 판정 |
| `/react-tauri` | Tauri command + invoke + capabilities, isTauri() 가드 + infrastructure/tauri/ 경계 |
| `/react-test` | Clean Arch 레이어별 테스트 (Vitest unit / MSW integration / RTL component / Playwright e2e) |
| `/react-error` | 3단계 에러 처리 (datasource → Failure → UI), Severity 매핑, ErrorBoundary |
| `/react-l10n` | Lingui v5 매크로 (`<Trans>`/`t`/`<Plural>`) + extract/compile codegen |
| `/react-responsive` | Tailwind v4 breakpoints + Container Queries (page-size vs container-size 자동 판정) |
| `/react-skeleton` | shadcn Skeleton + TanStack Query isPending 분기 (스피너 금지, layout-matching) |
| `/react-extract` | TypeScript AST 기반 재사용 컴포넌트 추출 (widget-inspector-react 연동) |
| `/react-animation` | 3-Tier 애니메이션 (Tailwind+CSS / View Transitions / Pointer Primitives), **라이브러리 0개 원칙** |
| `/react-run` | 빌드 프리미티브 (dev, build, lint, test, wasm-build, format, codegen) |
| `/react-build` | 전체 빌드 (wasm-pack → tsc → vite build) |
| `/react-preflight` | Pre-commit gate (fix → codegen → lint → tsc → test → wasm-build → vite-build) |
| `/react-audit` | 6 카테고리 감사 (Architecture / Strict TS / Performance / Accessibility / Anti-patterns / **Library Policy**), quick/deep 모드 |
| `widget-inspector-react` (에이전트) | React 재사용 패턴 감지 (중복 UI, shadcn 재발명, variant hint, container hint, cross-feature import) |
| `animation-architect-react` (에이전트) | 3-Tier 애니메이션 자문 (Tier 판정 + 접근성 검토 + 구현 단계). 라이브러리 0개 원칙 enforce |
| `react-reviewer` (에이전트) | react-audit 6 카테고리 독립 평가, Library Policy 빌드 게이트 검증 |

**이 레포 전용 스킬 (.claude/skills/)**

| 스킬 | 용도 |
|------|------|
| `/kaizen` | 전체 10 Phase 카이젠 오케스트레이션 (설계 가이드 → contract → evaluator → harness → flutter → design → backend → infra → rust → react → Final) |
| `/design-kaizen` | design-kit 스킬 개선 |
| `/design-research` | 디자인 레퍼런스 크롤링 → design-kit/docs/design/ 문서 갱신 |
| `/backend-kaizen` | backend-kit 스킬 개선 |
| `/backend-research` | 백엔드 레퍼런스 크롤링 → docs/backend/ 문서 갱신 |
| `/infra-kaizen` | infra-kit 스킬 개선 |
| `/infra-research` | 인프라 레퍼런스 크롤링 → docs/infra/ 문서 갱신 |
| `/rust-kaizen` | rust-kit 스킬 개선 |
| `/rust-research` | Rust 레퍼런스 크롤링 → docs/rust/ 문서 갱신 |
| `/docs-site` | docs/ HTML 문서 페이지 생성·관리 |
| `/create-kit` | 새 플러그인 킷 생성 오케스트레이션 |

### 외부 플러그인 스킬 (이 레포에 없음)

아래는 별도 설치된 플러그인이나 Claude Code 내장 기능으로, 이 레포 작업 시에도 사용 가능하다.

**superpowers — 범용 워크플로우**

| 스킬 | 용도 |
|------|------|
| `brainstorming` | 기능 설계·창작 작업 전 요구사항 탐색. 구현 전 자동 실행 |
| `writing-plans` | 멀티스텝 작업의 구현 계획 작성 |
| `executing-plans` | 작성된 계획을 리뷰 체크포인트와 함께 실행 |
| `test-driven-development` | TDD 워크플로우 (테스트 먼저, 구현 후) |
| `systematic-debugging` | 버그·테스트 실패 시 체계적 원인 분석 |
| `requesting-code-review` | 작업 완료 후 코드 리뷰 요청 |
| `receiving-code-review` | 리뷰 피드백 수신 시 기술적 검증 후 반영 |
| `verification-before-completion` | 완료 선언 전 빌드·테스트 실행으로 증거 확보 |
| `finishing-a-development-branch` | 개발 완료 후 merge/PR/cleanup 옵션 제시 |
| `subagent-driven-development` | 독립 태스크를 서브에이전트로 병렬 실행 |
| `dispatching-parallel-agents` | 2+ 독립 태스크 병렬 에이전트 디스패치 |
| `using-git-worktrees` | 격리된 git worktree에서 피처 작업 |
| `writing-skills` | 새 스킬 작성·검증 |

**기타 외부 스킬**

| 스킬 | 용도 |
|------|------|
| `/review` | 커밋/PR 전 빌드·import·포트·괄호 등 체크리스트 검토 |
| `/simplify` | 변경 코드의 재사용성·품질·효율 리뷰 후 개선 |
| `/release` | 플러그인 버전 bump + marketplace.json 갱신 + git commit/tag/push |
| `/claude-api` | Claude API / Anthropic SDK 앱 빌드 |
| `/codex:rescue` | Codex 서브에이전트에 조사·수정·리서치 위임 |
| `/update-config` | Claude Code settings.json 설정 변경 |
| `/loop` | 프롬프트/슬래시 커맨드를 주기적 반복 실행 |
| `/schedule` | 원격 에이전트 cron 스케줄 생성·관리 |

## Key Conventions

- 모든 문서와 커밋 메시지는 한국어 사용
- 스킬 설계는 `harness/docs/guides/skill-design-guide.md`의 9가지 아키타입을 따른다
- Gotchas 섹션이 스킬에서 가장 중요한 부분 — Claude가 반복하는 실수를 방지한다
- harness evals는 `evals/test-fixtures/fixture-a~e` 디렉토리에 계약 시나리오별 테스트가 있다
- flutter-toolkit evals는 `evals/evals.json`에 19개 스킬별 assertion이 정의되어 있다

## Harness 트리거 규칙

이 레포에서 작업할 때 아래 키워드가 사용자 요청에 포함되면 harness의 sprint-contract 스킬 + qa-evaluator 에이전트 세트를 실행한다:

- **계약 키워드**: sprint-contract, sc, 계약, contract, 완료 조건, 스프린트, sprint, 조건 정의, 완료 기준, ㄱㅈ
- **QA 키워드**: qa, qa-evaluator, 검증, 평가, 판정, approve, reject, 검수, 품질 확인, 판정해줘, QA 돌려줘, QA 피드백
- **구현 키워드**: 구현해줘, 개발해줘, 기능 만들어줘, 화면 추가, 페이지 추가, 작업해줘, 착수, 코딩해줘, 기능 추가, 새 기능, feature, 리팩터링, refactor, API 연동, 엔드포인트 추가, 모듈 추가, 서비스 추가, ㄱㅎ, ㅊㄱ
- **조건부 키워드**: 만들어줘, 추가해줘, 생성해줘 — "기능"과 함께 나올 때만 트리거. 단독 사용 시 다른 스킬(create-skill, flutter-widget 등) 우선

실행 순서: `/sprint-contract` → 개발 → `qa-evaluator` 에이전트.
단순 수정(색상 변경, 오타 수정, 1파일 변경)에는 트리거하지 않는다.

원본 위치:
- 에이전트: `harness/agents/qa-evaluator.md`
- 스킬: `harness/skills/sprint-contract/SKILL.md`
- `.claude/`에 복사본을 두지 않는다 — harness 플러그인 원본만 사용

## Platform Gotchas (Windows)

- `python3`은 Windows Store 스텁일 수 있음 — `python3 -c "pass"`로 실제 동작 확인 후 사용. 안 되면 `python`으로 fallback
- Python에서 한국어 포함 파일 읽을 때 `encoding='utf-8'` 필수 (기본 cp949 에러)
- bash 스크립트에서 `sha256sum` 미설치 가능 — `python -c "import hashlib; ..."` 또는 `openssl dgst -sha256`으로 fallback
