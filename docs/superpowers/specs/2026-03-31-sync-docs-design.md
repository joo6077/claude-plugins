# sync-docs: 문서 자동 동기화 시스템

## 개요

스킬, 에이전트, plugin.json, hooks.json 등이 변경되면 관련 문서(README, CLAUDE.md)를 자동으로 갱신하는 Python 스크립트 + PostToolUse 훅 시스템.

## 목표

- 스킬/에이전트 추가·수정 시 README가 항상 최신 상태 유지
- 수동 README 편집 실수 방지
- 마커 기반으로 자동 갱신 영역과 수동 영역을 명확히 분리

## 아키텍처

### 마커 기반 자동 갱신

README 파일에 HTML 주석 마커를 삽입하여 자동 갱신 영역을 지정한다:

```markdown
<!-- AUTO:skills -->
(이 사이 내용이 자동 갱신됨)
<!-- /AUTO:skills -->
```

마커 밖 섹션(셋업 가이드, 사용 흐름, 원칙 등)은 그대로 보존.

### 마커 종류

| 마커 | 대상 파일 | 내용 |
|------|-----------|------|
| `AUTO:skills` | 플러그인 README | 스킬 테이블 |
| `AUTO:agents` | 플러그인 README | 에이전트 테이블 |
| `AUTO:hooks` | 플러그인 README | 훅 테이블 |
| `AUTO:scripts` | 플러그인 README | 스크립트 테이블 |
| `AUTO:evals` | 플러그인 README | Evals 테이블 |
| `AUTO:references` | 플러그인 README | 레퍼런스 테이블 |
| `AUTO:plugins` | 루트 README | 플러그인 목록 테이블 |
| `AUTO:summary` | CLAUDE.md | 버전, 스킬 수 요약 |

### 데이터 소스 매핑

| 대상 | 소스 파일 | 추출 항목 |
|------|-----------|-----------|
| 버전 | `{plugin}/.claude-plugin/plugin.json` | `version` |
| 설명 | `{plugin}/.claude-plugin/plugin.json` | `description` |
| 스킬 목록 | `{plugin}/skills/*/SKILL.md` frontmatter | `name`, `description` |
| 에이전트 목록 | `{plugin}/agents/*.md` frontmatter | `name`, `description`, `tools`, `model` |
| 훅 | `{plugin}/hooks/hooks.json` | 이벤트명, 실행 스크립트 |
| 스크립트 | `{plugin}/scripts/*.sh` | 파일명 + 파일 내 첫 번째 `#` 주석 |
| Evals | `{plugin}/evals/` | 파일 목록 |
| 레퍼런스 | `{plugin}/references/*.md` | 파일명 + frontmatter 또는 첫 번째 `#` 헤더 |
| 루트 플러그인 테이블 | 각 plugin.json + marketplace.json | 이름, 버전, 설명 |
| CLAUDE.md 요약 | 각 plugin.json + 스킬 수 카운트 | 버전, 스킬 수 |

### 플러그인 README 템플릿 구조

```markdown
# {plugin-name} · v{version}

{description from plugin.json}

## 스킬 목록

<!-- AUTO:skills -->
| 스킬 | 설명 |
|------|------|
| `skill-name` | description 첫 줄 |
<!-- /AUTO:skills -->

## 에이전트 목록

<!-- AUTO:agents -->
| 에이전트 | 모델 | 도구 | 설명 |
|----------|------|------|------|
| `agent-name` | model | tools | description 첫 줄 |
<!-- /AUTO:agents -->

## 훅

<!-- AUTO:hooks -->
| 이벤트 | 실행 | 설명 |
|--------|------|------|
<!-- /AUTO:hooks -->

## 스크립트

<!-- AUTO:scripts -->
| 스크립트 | 설명 |
|----------|------|
<!-- /AUTO:scripts -->

## Evals

<!-- AUTO:evals -->
| 파일 | 설명 |
|------|------|
<!-- /AUTO:evals -->

## 레퍼런스

<!-- AUTO:references -->
| 파일 | 용도 |
|------|------|
<!-- /AUTO:references -->
```

헤더(`# {name} · v{version}`)도 plugin.json에서 자동 갱신한다.

### 루트 README 마커

```markdown
<!-- AUTO:plugins -->
| 플러그인 | 버전 | 스택 | 설명 |
|----------|------|------|------|
<!-- /AUTO:plugins -->
```

### CLAUDE.md 마커

```markdown
<!-- AUTO:summary -->
- **harness** — ... 스킬 N종
- **flutter-toolkit** — ... 스킬 N종
- **design-kit** — ... 스킬 N종
<!-- /AUTO:summary -->
```

## 스크립트 인터페이스

```bash
# 전체 플러그인 동기화
python scripts/sync-docs.py

# 특정 플러그인만
python scripts/sync-docs.py harness

# 변경 감지만 (훅용, 갱신 안 함)
python scripts/sync-docs.py --check-only

# dry-run (변경 내용 미리보기)
python scripts/sync-docs.py --dry-run
```

### 출력 형식

```
[sync-docs] harness/README.md — 스킬 테이블 갱신 (7개)
[sync-docs] README.md — 플러그인 테이블 갱신 (harness v0.3.5)
[sync-docs] CLAUDE.md — 요약 갱신
[sync-docs] 3개 파일 갱신 완료
```

`--check-only`:
```
[sync-docs] 변경 감지: harness/skills/new-skill/SKILL.md
[sync-docs] 문서 동기화가 필요합니다. `python scripts/sync-docs.py harness` 를 실행하세요.
```

## 트리거 메커니즘

PostToolUse 훅으로 Edit/Write 도구 실행 시 자동 감지:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "python ${CLAUDE_PLUGIN_ROOT}/scripts/sync-docs.py --check-only",
            "timeout": 5000
          }
        ]
      }
    ]
  }
}
```

- `--check-only`는 변경된 파일이 동기화 대상(스킬, 에이전트, plugin.json, hooks.json)인지만 확인
- 대상이면 "문서 동기화 필요" 메시지 출력
- 실제 갱신은 Claude가 스크립트를 실행하거나 사용자가 수동 실행

## 파일 구조

```
scripts/
├── sync-docs.py          ← 메인 동기화 스크립트
└── release.sh            ← 기존 릴리스 스크립트
```

## 엣지 케이스

- 마커가 없는 README: 경고 출력, 스킵 (수동으로 마커 추가 필요)
- skills/ 디렉토리가 없는 플러그인: 해당 섹션 스킵
- frontmatter가 없는 SKILL.md: 경고 출력, 해당 스킬 스킵
- description이 여러 줄인 경우: 첫 줄만 사용 (테이블 호환)
- Windows 경로: `pathlib.Path` 사용으로 OS 무관 처리
- 인코딩: 모든 파일 읽기에 `encoding='utf-8'` 명시
