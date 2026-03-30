# joo6077-plugins

Claude Code 플러그인 모노레포. 프로젝트 스택별로 필요한 플러그인만 골라 설치한다.

## 플러그인 목록

| 플러그인 | 버전 | 스택 | 설명 |
|----------|------|------|------|
| [`harness`](./harness/) | v0.3.5 | 범용 | Sprint Contract + QA Evaluator 기반 품질 보증 하네스 |
| [`flutter-toolkit`](./flutter-toolkit/) | v0.5.0 | Flutter | 빌드, 감사, preflight 등 Flutter 개발 워크플로우 스킬 18종 |
| [`design-kit`](./design-kit/) | v0.1.0 | 범용 | UI/UX 디자인 시스템 세팅 + 실시간 가이드 + 감사 |

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

```bash
claude plugin update harness@joo6077-plugins
claude plugin update flutter-toolkit@joo6077-plugins
claude plugin update design-kit@joo6077-plugins
```

### 삭제

```bash
claude plugin uninstall harness@joo6077-plugins
claude plugin uninstall flutter-toolkit@joo6077-plugins
claude plugin uninstall design-kit@joo6077-plugins
```

### 릴리스 (관리자)

```bash
# 플러그인별 버전 bump + git tag + push
bash scripts/release.sh harness patch
bash scripts/release.sh flutter-toolkit patch
bash scripts/release.sh design-kit patch
```

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
- `docs/design/` 리서치 문서 기반

> 자세한 내용은 [design-kit/README.md](./design-kit/README.md) 참조.

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
├── docs/                        # 설계 가이드, 리서치, 카이젠 로그
├── scripts/
│   └── release.sh               # 플러그인 릴리스 자동화
└── README.md
```

## 라이선스

MIT
