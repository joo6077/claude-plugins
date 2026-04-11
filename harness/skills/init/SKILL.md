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

## 실행 후 안내

초기화가 완료되면 사용자에게 다음 단계를 안내한다:

```text
harness 초기화 완료!

다음 단계:
1. .harness/project.yaml — commands, anti_patterns 설정
2. .harness/procedures/ — 카테고리별 검증 절차 작성 (선택)

설정 완료 후 /sprint-contract로 첫 계약을 작성하세요.
```
