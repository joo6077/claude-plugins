# joo6077-plugins

Claude Code 플러그인 모노레포. 프로젝트 스택별로 필요한 플러그인만 골라 설치한다.

## 플러그인 목록

| 플러그인 | 버전 | 스택 | 설명 |
|----------|------|------|------|
| [`harness`](./harness/) | v0.3.2 | 범용 | Sprint Contract + QA Evaluator 기반 품질 보증 하네스 |
| [`flutter-toolkit`](./flutter-toolkit/) | v0.1.0 | Flutter | 빌드, 감사, preflight 등 Flutter 개발 워크플로우 스킬 |

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
```

### 삭제

```bash
claude plugin uninstall harness@joo6077-plugins
claude plugin uninstall flutter-toolkit@joo6077-plugins
```

### 릴리스 (관리자)

```bash
# 플러그인별 버전 bump + git tag + push
bash scripts/release.sh harness patch    # 0.3.2 → 0.3.3
bash scripts/release.sh harness minor    # 0.3.2 → 0.4.0
bash scripts/release.sh harness major    # 0.3.2 → 1.0.0
```

---

## 플러그인 상세

### harness

스택에 관계없이 동작하는 범용 품질 보증 프레임워크.

- **Sprint Contract**: 구현 전 완료 조건을 정의하고, QA Evaluator가 이를 기준으로 평가
- **QA Evaluator**: 독립 에이전트가 구현 결과를 APPROVE/REJECT 판정
- **Harness Kaizen**: 리서치 기반 지속 개선 프레임워크

**제공 스킬:**

| 스킬 | 트리거 | 설명 |
|------|--------|------|
| `init` | `/harness init`, `harness 초기화` | 프로젝트에 `.harness/` 디렉토리 초기화 |
| `sprint-contract` | `/sprint-contract`, `기능 만들어줘` | 구현 전 완료 조건 계약 생성 |
| `harness-kaizen` | `/harness-kaizen` | 리서치 기반 하네스 개선 |

**사용 시작:**
```
/harness init
```

> 자세한 내용은 [harness/README.md](./harness/README.md) 참조.

### flutter-toolkit

Flutter 프로젝트 전용 개발 워크플로우 스킬 모음.

- FVM(Flutter Version Manager) 필수
- harness 플러그인과 연동 (`.harness/project.yaml`)

**계획된 스킬:** build, run, preflight, audit

> 자세한 내용은 [flutter-toolkit/README.md](./flutter-toolkit/README.md) 참조.

---

## 구조

```
claude-plugins/
├── .claude-plugin/
│   └── marketplace.json         # 플러그인 레지스트리
├── harness/                     # 범용 QA 하네스
│   ├── .claude-plugin/plugin.json
│   ├── agents/                  # QA Evaluator 에이전트
│   ├── skills/                  # init, sprint-contract, kaizen
│   ├── hooks/                   # SessionStart, PreToolUse
│   ├── templates/               # 프로젝트 초기화 템플릿
│   ├── evals/                   # 플러그인 테스트
│   └── scripts/                 # 유틸리티 스크립트
├── flutter-toolkit/             # Flutter 전용
│   ├── .claude-plugin/plugin.json
│   ├── skills/                  # 개발 워크플로우 스킬
│   └── hooks/
├── scripts/
│   └── release.sh               # 플러그인 릴리스 자동화
├── docs/                        # 설계 가이드, 리서치
└── README.md
```

## 라이선스

MIT
