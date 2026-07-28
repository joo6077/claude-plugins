---
name: init
description: >
  현재 프로젝트에 .harness/ 디렉토리를 생성하고 초기 설정 파일을 세팅한다.
  "harness 초기화", "harness init", "QA 세팅해줘" 같은 요청에 사용.
  이미 .harness/가 존재하면 트리거하지 않는다.
argument-hint: "[stack]"
user-invocable: true
---

# Harness Init

현재 프로젝트에 harness QA 환경을 초기화한다.

## 사전 확인

1. **`.harness/` 존재 여부 확인** — 이미 있으면 사용자에게 알리고 중단
2. **스택 파싱** — `$ARGUMENTS`에서 stack을 추출. 없으면 프로젝트를 분석해서 자동 감지하거나 사용자에게 물어본다

## 스택 자동 감지

인자가 없으면 프로젝트 루트의 파일로 스택을 추론한다:

- `pubspec.yaml` → flutter
- `Cargo.toml` → rust
- `package.json` + react 의존성 → react
- `package.json` + next 의존성 → nextjs
- `requirements.txt` / `pyproject.toml` → python
- `go.mod` → go
- 감지 실패 시 → generic

감지 결과를 사용자에게 보여주고 확인받는다.

## 실행

harness 플러그인의 init 스크립트를 실행한다:

```bash
bash "${PLUGIN_DIR}/scripts/init.sh" "." "<stack>"
```

`PLUGIN_DIR`은 이 스킬이 위치한 플러그인의 루트 디렉토리다.
스킬 파일 기준으로 `../../scripts/init.sh`에 해당한다.

스크립트를 직접 찾을 수 없는 경우, 설치된 플러그인 캐시 경로에서 찾는다:

- `~/.claude/plugins/cache/joo6077-plugins/harness/*/scripts/init.sh`

## Gotchas

- `PLUGIN_DIR` 경로는 스킬 파일 기준 `../../`이지만, 플러그인 캐시에서 실행될 때는 `~/.claude/plugins/cache/` 하위 경로가 된다. 두 경로를 모두 시도해야 한다
- Windows 환경에서 `bash` 명령이 Git Bash를 가리키는지 WSL bash를 가리키는지에 따라 경로 해석이 달라진다. `init.sh` 실행 전 경로 구분자(`/` vs `\`)를 확인해라
- 스택 자동 감지 시 `package.json`만으로는 react/nextjs/vanilla node를 구분할 수 없다. 반드시 의존성 내용까지 확인해야 한다
- `.harness/`가 이미 존재하면 **덮어쓰지 않고 중단**한다. 사용자에게 삭제 후 재실행을 안내해야 하며, 자동 삭제하면 안 된다
- `project.yaml`의 `commands.analyze`에 프로젝트 빌드 명령을 정확히 넣지 않으면 QA Evaluator가 DG-01 판정을 할 수 없다. init 시 반드시 검증 가능한 명령을 설정하라
- `contract_categories`를 비워두면 sprint-contract가 기본 카테고리를 사용하지만, 프로젝트에 맞지 않는 카테고리가 생성된다. 최소 2개 이상 프로젝트에 맞는 카테고리를 정의하라
- `anti_patterns`를 빈 배열로 두면 sprint-contract에서 안티패턴 체크리스트가 생성되지 않는다. 최소 2개 이상 프로젝트에서 자주 발생하는 패턴을 정의하라
- 모노레포에서 init 시 루트가 아닌 서브패키지에서 실행하면 `.harness/`가 서브패키지에 생성된다. 반드시 모노레포 루트에서 실행하라
- 생성된 `project.yaml`을 git에 커밋하지 않으면 다른 팀원이 sprint-contract를 실행할 때 기본 설정으로 fallback한다. init 후 즉시 커밋하라
- `init.sh`에서 파일 내용을 치환할 때 `sed -i`를 직접 사용하지 마라 — macOS는 `sed -i ''`, Linux는 `sed -i`로 문법이 다르다. `sed ... > tmpfile && mv tmpfile target` 패턴으로 크로스 플랫폼 호환성을 확보해라
- `.gitignore`에 `.harness/`를 추가하지 마라 — sprint-contract와 project.yaml은 팀 공유 대상이다. `.harness/feedback-draft.yaml`만 개별 무시하라

## 실행 후 안내

초기화가 완료되면 사용자에게 다음 단계를 안내한다:

```text
harness 초기화 완료!

다음 단계:
1. .harness/project.yaml — commands, anti_patterns 설정
2. .harness/procedures/ — 카테고리별 검증 절차 작성 (선택)

설정 완료 후 /sprint-contract로 첫 계약을 작성하세요.

참조 가이드 (첫 계약 전에 한 번씩 읽기 권장):
- harness/docs/guides/contract-design-guide.md §Binary Decidability — 계약 조건을 이진 판정 가능하게 작성하는 원칙
- harness/docs/guides/contract-design-guide.md §Scope Range — 스코프를 인라인으로 명시하는 패턴
- harness/docs/guides/contract-design-guide.md §Verification Method — L1/L2/L3 검증 수단 fallback
- harness/docs/guides/qa-evaluation-guide.md §`[미검증]` 마커 평가 프로토콜 — 런타임 검증 불가 시 처리
- harness/docs/guides/skill-design-guide.md §11 Cross-Surface Parity — 신규 원칙의 surface 간 전파 체크
```

### 플러그인 모노레포 환경일 때 (optional)

현재 프로젝트 루트에 `.claude-plugin/marketplace.json` 또는 `<kit>/.claude-plugin/plugin.json` 이 있으면 플러그인 모노레포다. 이 경우 **베이스라인 스냅샷** 을 권장한다 (리서치 근거: 2026 agentic regression detection — "baseline snapshot 확보 후 다음 사이클에서 회귀 비교", Sauce Labs / ContextQA):

```bash
python3 scripts/validate-plugin.py
```

8 카테고리 (V1~V8) 결과를 기록해 두면 이후 카이젠/릴리스 주기마다 drift 비교가 가능하다. 기준 문서: `harness/docs/guides/plugin-validation-guide.md` (카테고리 수·정의의 SSOT).
