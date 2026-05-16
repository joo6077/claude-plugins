# joo6077-plugins

Claude Code 플러그인 모노레포. 프로젝트 스택별로 필요한 플러그인만 골라 설치한다.

## 플러그인 목록

<!-- AUTO:plugins -->
| 플러그인 | 버전 | 스택 | 설명 |
|----------|------|------|------|
| [`harness`](./harness/) | v0.4.2 | 범용 | [v0.4.2 · 2026-05-07] Sprint Contract + QA Evaluator 기반 품질 보증 하네스 (2026 QA 자동화 트렌드 반영) |
| [`flutter-toolkit`](./flutter-toolkit/) | v0.5.3 | Flutter | [v0.5.3 · 2026-05-07] Flutter 개발 워크플로우 스킬 모음 (Riverpod 3.0 / Freezed 3.0 / go_router StatefulShellRoute) |
| [`design-kit`](./design-kit/) | v0.2.3 | 범용 | [v0.2.3 · 2026-05-07] 스택 무관 UI/UX 디자인 가이드 + 감사 (OKLCH / DTCG v1 / WCAG 2.2 / Container Queries) |
| [`backend-kit`](./backend-kit/) | v0.1.3 | 범용 | [v0.1.3 · 2026-05-07] 스택 무관 백엔드 개발 가이드 + 감사 + 아키텍처 세팅 (Hexagonal/Clean/DDD + OAuth 2.1 + Outbox + Pact) |
| [`infra-kit`](./infra-kit/) | v0.1.3 | 범용 | [v0.1.3 · 2026-05-07] 스택 무관 인프라/DevOps 가이드 + 감사 + 초기 세팅 (K8s PSA / Terraform 1.10 / SLSA / OTel) |
| [`rust-kit`](./rust-kit/) | v0.1.3 | 범용 | [v0.1.3 · 2026-05-07] Rust 전용 백엔드 개발 워크플로우 — Rust 2024 / Axum 0.8 / SeaORM 1.1 / Clippy 2026 |
| [`react-kit`](./react-kit/) | v0.1.3 | 범용 | [v0.1.3 · 2026-05-07] React + Vite + Tauri 2 + Rust WASM 개발 워크플로우 — React 19 / TanStack Query v5 / Tauri 2 GA / Tailwind v4 / Zustand v5, 라이브러리 0개 애니메이션 |
| [`planning-kit`](./planning-kit/) | v0.3.1 | 범용 | [v0.3.1 · 2026-05-07] 스택 무관 제품 기획 플러그인 — 레퍼런스 teardown · Lightning Demo · VPC · Blue Ocean · HMW · Crazy 8s · JTBD · PR-FAQ · Shape Up · RICE·Kano·WSJF · DDD Event Storming · GitHub Projects v2 |
| [`reflect-kit`](./reflect-kit/) | v0.3.1 | 범용 | [v0.3.1 · 2026-05-07] 개인 Claude Code 대화 피드백 → 학습 → 재주입 파이프라인 (Reflexion 방법론) — Hybrid project_id (basename 기본 + 충돌 시 hash fallback · backward-compatible) · 정규화 쿼리 · 내부 디렉토리 자동 제외 · 3 훅 수집 · /reflect-digest 집계 (+ project=all cross-project) · /reflect-promote 승격 + ledger · /reflect-kaizen 30d calibration · codex 실패 시 Claude CLI fallback · install-scheduler/legacy-id-migrate 유틸 |
| [`bambu-kit`](./bambu-kit/) | v0.1.0 | 범용 | [v0.1.0 · 2026-05-16] Bambu Lab H2S 자동 process+filament JSON 생성 — MakerWorld URL/모델 분석 → 소재 추천 → seam 전략 → Bambu Studio import 번들 (Codex 8회 리서치 + 실측 dogfood 2건 검증) |
<!-- /AUTO:plugins -->

---

## 설치

### 1. 마켓플레이스 등록

Claude Code 세션에서 이 모노레포를 마켓플레이스로 추가한다:

```
/plugin marketplace add joo6077/claude-plugins
```

### 2. 플러그인 설치

등록된 마켓플레이스에서 원하는 플러그인을 설치한다:

```
/plugin install harness@joo6077-plugins
/plugin install flutter-toolkit@joo6077-plugins
/plugin install design-kit@joo6077-plugins
```

또는 `/plugin` 명령으로 인터랙티브 UI를 열어 **Discover** 탭에서 선택할 수도 있다.

### 설치 범위

| 플래그 | 범위 | 설명 |
|--------|------|------|
| *(기본)* | user | 모든 프로젝트에서 사용 |
| `--scope project` | project | 해당 프로젝트에서만 사용 (팀 공유) |
| `--scope local` | local | 해당 프로젝트, 본인만 사용 (gitignored) |

```bash
# 예: 프로젝트 범위로 설치
claude plugin install harness@joo6077-plugins --scope project
```

---

## 업데이트

```
/plugin marketplace update joo6077-plugins
```

개별 플러그인 업데이트:

<!-- AUTO:update-cmd -->
```bash
claude plugin update harness@joo6077-plugins
claude plugin update flutter-toolkit@joo6077-plugins
claude plugin update design-kit@joo6077-plugins
claude plugin update backend-kit@joo6077-plugins
claude plugin update infra-kit@joo6077-plugins
claude plugin update rust-kit@joo6077-plugins
claude plugin update react-kit@joo6077-plugins
claude plugin update planning-kit@joo6077-plugins
claude plugin update reflect-kit@joo6077-plugins
claude plugin update bambu-kit@joo6077-plugins
```
<!-- /AUTO:update-cmd -->

### 삭제

<!-- AUTO:uninstall-cmd -->
```bash
claude plugin uninstall harness@joo6077-plugins
claude plugin uninstall flutter-toolkit@joo6077-plugins
claude plugin uninstall design-kit@joo6077-plugins
claude plugin uninstall backend-kit@joo6077-plugins
claude plugin uninstall infra-kit@joo6077-plugins
claude plugin uninstall rust-kit@joo6077-plugins
claude plugin uninstall react-kit@joo6077-plugins
claude plugin uninstall planning-kit@joo6077-plugins
claude plugin uninstall reflect-kit@joo6077-plugins
claude plugin uninstall bambu-kit@joo6077-plugins
```
<!-- /AUTO:uninstall-cmd -->

### 릴리스 (관리자)

<!-- AUTO:release-cmd -->
```bash
# 플러그인별 버전 bump + git tag + push
bash scripts/release.sh harness patch
bash scripts/release.sh flutter-toolkit patch
bash scripts/release.sh design-kit patch
bash scripts/release.sh backend-kit patch
bash scripts/release.sh infra-kit patch
bash scripts/release.sh rust-kit patch
bash scripts/release.sh react-kit patch
bash scripts/release.sh planning-kit patch
bash scripts/release.sh reflect-kit patch
bash scripts/release.sh bambu-kit patch
```
<!-- /AUTO:release-cmd -->

---

## 플러그인 상세

### harness

스택에 관계없이 동작하는 범용 품질 보증 프레임워크.

- **Sprint Contract**: 구현 전 완료 조건을 정의하고, QA Evaluator가 이를 기준으로 평가
- **QA Evaluator**: 독립 에이전트가 구현 결과를 APPROVE/REJECT 판정
- **자기진단 + 교차 진단**: 실행 후 글로벌 피드백 저장 (`~/.harness/feedback/`)
- **Kaizen**: contract-kaizen, evaluator-kaizen, harness-kaizen으로 리서치 기반 지속 개선

**제공 스킬:**

| 스킬 | 트리거 | 설명 |
|------|--------|------|
| `init` | `/harness init` | 프로젝트에 `.harness/` 디렉토리 초기화 |
| `sprint-contract` | `/sprint-contract` | 구현 전 완료 조건 계약 생성 |
| `harness-kaizen` | `/harness-kaizen` | 리서치 기반 하네스 개선 |
| `contract-kaizen` | `/contract-kaizen` | sprint-contract 리서치 기반 자기개선 |
| `evaluator-kaizen` | `/evaluator-kaizen` | qa-evaluator 리서치 기반 자기개선 |
| `create-skill` | `/create-skill` | 설계 가이드 기반 스킬 생성 |
| `create-agent` | `/create-agent` | 설계 가이드 기반 에이전트 생성 |

**사용 시작:**
```
/harness init
```

> 자세한 내용은 [harness/README.md](./harness/README.md) 참조.

### flutter-toolkit

Flutter 프로젝트 전용 개발 워크플로우 스킬 18종.

- FVM(Flutter Version Manager) 필수
- harness 플러그인과 연동 (`.harness/project.yaml`)

**제공 스킬:** api, audit, build, error, extract, feature, hooks, kaizen, l10n, preflight, provider, responsive, run, screen, skeleton, test, transition, widget

> 자세한 내용은 [flutter-toolkit/README.md](./flutter-toolkit/README.md) 참조.

### design-kit

스택 무관 UI/UX 디자인 플러그인.

- 디자인 시스템 세팅 + 실시간 가이드 + 감사
- `design-kit/docs/design/` 리서치 문서 기반

> 자세한 내용은 [design-kit/README.md](./design-kit/README.md) 참조.

### backend-kit

스택 무관 백엔드 개발 가이드 + 감사 + 아키텍처 세팅.

- Hexagonal/Clean/DDD 아키텍처, OAuth 2.1, FAPI 2.0, Outbox 패턴
- `docs/backend/` 리서치 문서 기반

> 자세한 내용은 [backend-kit/README.md](./backend-kit/README.md) 참조.

### infra-kit

스택 무관 인프라/DevOps 가이드 + 감사 + 초기 세팅.

- K8s Gateway API, Terraform/OpenTofu, SLSA, OTel, FinOps
- `docs/infra/` 리서치 문서 기반

> 자세한 내용은 [infra-kit/README.md](./infra-kit/README.md) 참조.

### rust-kit

Rust 전용 백엔드 개발 워크플로우 17종.

- Rust 2024 Edition, Axum 0.8, SQLx, SeaORM, tonic gRPC
- `docs/rust/` 리서치 문서 기반

> 자세한 내용은 [rust-kit/README.md](./rust-kit/README.md) 참조.

### react-kit

React + Vite + Tauri 2 + Rust WASM 개발 워크플로우 21종 + 3 에이전트.

- React 19, TanStack Router/Query, Zustand, shadcn/ui, Tailwind v4
- 라이브러리 0개 애니메이션 원칙
- `docs/react/` 리서치 문서 기반

> 자세한 내용은 [react-kit/README.md](./react-kit/README.md) 참조.

### planning-kit

스택 무관 제품 기획 플러그인. 아이디어를 Sprint Contract로 넘어갈 수 있는 수준의 기획 산출물로 변환한다.

- harness 파이프라인의 **0번 단계** ("기획 → 계약 → 구현 → QA" 흐름)
- PRD, 우선순위(RICE/Kano/WSJF), 리스크, 개념 데이터 모델(Mermaid erDiagram/flowchart/sequenceDiagram)
- GitHub Projects v2 동기화, Shape Up · DDD Event Storming · JTBD · PR-FAQ 등 방법론
- `docs/planning/` 리서치 문서 기반

> 자세한 내용은 [planning-kit/README.md](./planning-kit/README.md) 참조.

### reflect-kit

개인 Claude Code 사용자의 대화 피드백 → 학습 → 재주입 파이프라인. Reflexion 방법론을 개인 레벨에 적용.

- 3 훅 수집(UserPromptSubmit / PostToolUseFailure / Stop) → 구조화 로그
- `/reflect-digest` 집계 → `/reflect-promote` 승격(CLAUDE.md / memory / skill / hook + ledger) → `/reflect-kaizen` 30d 재발률 calibration
- Hybrid project_id (basename 기본 + 충돌 시 hash fallback, backward-compatible)
- codex 실패 시 Claude CLI fallback, install-scheduler/legacy-id-migrate 유틸

> 자세한 내용은 [reflect-kit/README.md](./reflect-kit/README.md) 참조.

### bambu-kit

Bambu Lab H2S 자동 process+filament JSON 생성. 도구형 1스킬 킷 (guide/audit/system 3종 패턴 비적용).

- H2S + AMS HT + AMS 2 Pro + Bambu Studio v2.6.0+ 환경 가정
- MakerWorld URL/로컬 모델 → 모델 분석 → 소재 추천 → seam 전략 → Bambu Studio용 zip 번들
- references 4종 (bambu-fields-baseline / materials / seam-recipes / kaizen-sources) SSOT
- 카이젠 스킬 (`bambu-research`, `bambu-kaizen`)은 `.claude/skills/`에 분리 (plugin 외부)

> 자세한 내용은 [bambu-kit/README.md](./bambu-kit/README.md) 참조.

---

## 구조

```
claude-plugins/
├── .claude-plugin/
│   └── marketplace.json         # 플러그인 레지스트리
├── harness/                     # 범용 QA 하네스
│   ├── .claude-plugin/plugin.json
│   ├── agents/                  # QA Evaluator 에이전트
│   ├── skills/                  # init, sprint-contract, kaizen 등 7종
│   ├── hooks/                   # SessionStart, PreToolUse
│   ├── references/              # 공유 참조 (contract-schema, feedback-schema)
│   ├── templates/               # 프로젝트 초기화 템플릿
│   ├── evals/                   # 플러그인 테스트 + 카이젠 메타 eval
│   └── scripts/                 # 피드백, 검증, 트리거 스크립트
├── flutter-toolkit/             # Flutter 전용
│   ├── .claude-plugin/plugin.json
│   ├── skills/                  # 개발 워크플로우 스킬 18종
│   ├── references/              # 프로젝트 감지, AI 규칙
│   └── hooks/
├── design-kit/                  # UI/UX 디자인
│   ├── .claude-plugin/plugin.json
│   ├── skills/
│   ├── agents/
│   ├── hooks/
│   └── scripts/
├── backend-kit/                 # 백엔드 개발
│   ├── .claude-plugin/plugin.json
│   ├── skills/
│   ├── agents/
│   └── references/
├── infra-kit/                   # 인프라/DevOps
│   ├── .claude-plugin/plugin.json
│   ├── skills/
│   ├── agents/
│   └── references/
├── rust-kit/                    # Rust 백엔드
│   ├── .claude-plugin/plugin.json
│   ├── skills/                  # 개발 워크플로우 스킬 17종
│   ├── agents/
│   ├── references/
│   └── templates/
├── react-kit/                   # React + Vite + Tauri 2
│   ├── .claude-plugin/plugin.json
│   ├── skills/                  # 개발 워크플로우 스킬 21종
│   ├── agents/                  # 3 에이전트
│   └── references/
├── planning-kit/                # 제품 기획 (harness 0번 단계)
│   ├── .claude-plugin/plugin.json
│   ├── skills/
│   ├── agents/
│   └── references/
├── reflect-kit/                 # 대화 피드백 → 학습 → 재주입 (Reflexion)
│   ├── .claude-plugin/plugin.json
│   ├── skills/                  # reflect-digest / reflect-promote / reflect-kaizen
│   ├── hooks/                   # 3 훅 (UserPromptSubmit / PostToolUseFailure / Stop)
│   └── scripts/
├── bambu-kit/                   # Bambu Lab H2S 프린트 프로파일 (도구형 1스킬)
│   ├── .claude-plugin/plugin.json
│   ├── README.md
│   └── skills/bambu-print-profile/
│       ├── SKILL.md
│       ├── BACKLOG.md           # v2 카이젠/capture daemon 백로그
│       └── references/          # 4종 (fields-baseline/materials/seam-recipes/kaizen-sources)
├── docs/                        # 설계 가이드, 리서치, HTML 시각 문서, 카이젠 로그
├── scripts/
│   ├── release.sh               # 플러그인 버전 bump + tag + push 자동화
│   ├── sync-docs.py             # README/CLAUDE.md AUTO 마커 자동 동기화
│   ├── sync-evals.py            # 스킬 ↔ evals.json 정합성 동기화
│   ├── run-evals.py             # 플러그인별 assertion 실행
│   └── validate-plugin.py       # 7-카테고리 플러그인 검증 (V1~V7)
├── .harness/                    # 이 레포 자체의 harness 설정 (project.yaml + sprint-contract)
├── .claude/                     # 이 레포 개발용 스킬 (research/kaizen, plugin 외부)
└── README.md
```

## 라이선스

MIT
