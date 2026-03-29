# Claude Plugins

Claude Code 플러그인 모노레포. 프로젝트 스택별로 필요한 플러그인만 설치한다.

## 플러그인 목록

| 플러그인 | 스택 | 설명 |
|----------|------|------|
| `harness/` | 범용 | Sprint Contract + QA Evaluator 기반 품질 보증 |
| `flutter-toolkit/` | Flutter | 빌드, 감사, preflight 등 Flutter 개발 스킬 |

## 설치

프로젝트의 `.mcp.json` 또는 Claude Code 설정에서 플러그인 경로를 지정한다.

## 구조

```
claude-plugins/
├── harness/                 # 범용 (모든 스택)
│   ├── .claude-plugin/
│   ├── agents/
│   ├── evals/
│   ├── hooks/
│   ├── scripts/
│   ├── skills/
│   └── templates/
├── flutter-toolkit/         # Flutter 전용
│   ├── .claude-plugin/
│   ├── skills/
│   └── hooks/
└── README.md
```
