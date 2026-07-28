---
description: >
  플러그인 버전을 bump하고 릴리스한다. plugin.json 버전 업데이트,
  marketplace.json description 날짜/버전 갱신, git commit + tag + push를 자동화한다.
  "/release harness patch", "harness 릴리스해줘", "버전 올려줘" 같은 요청에 사용.
argument-hint: "<plugin-name> <patch|minor|major>"
---

# Release

이 모노레포의 플러그인 릴리스를 관리한다.

## 사전 확인

릴리스 전에 반드시 확인할 것:

1. **uncommitted 변경사항 확인** — `git status`로 릴리스에 포함할 변경이 모두 커밋됐는지 확인
2. **플러그인 이름과 bump 타입 파싱** — `$ARGUMENTS`에서 추출. 없으면 사용자에게 물어본다

## 인자 파싱

`$ARGUMENTS` 형식: `<plugin-name> <patch|minor|major>`

- 첫 번째 단어: 플러그인 이름 (harness, flutter-toolkit 등)
- 두 번째 단어: bump 타입 (patch, minor, major)
- 인자가 부족하면 사용자에게 확인. "릴리스해줘"만 오면 플러그인 목록을 보여주고 선택 받는다
- "harness 릴리스" 처럼 bump 타입이 없으면 기본값 `patch`를 제안한다

## 실행

```bash
bash scripts/release.sh <plugin-name> <bump-type>
```

이 스크립트가 수행하는 것:

- `<plugin>/.claude-plugin/plugin.json`의 version 필드 업데이트
- `.claude-plugin/marketplace.json`의 description에서 `[vX.Y.Z · YYYY-MM-DD]` 패턴 갱신
- `release/<plugin>-v<new-version>` 브랜치 생성
- `git commit -m "release: <plugin> v<new-version>"`
- `git tag -a <plugin>/v<new-version>`
- 릴리스 브랜치 + 태그 push (`git push -u origin <branch> --follow-tags`)
- `gh pr create --base main` — **PR 생성까지가 스크립트의 끝이다**

**main 에 직접 push 하지 않는다.** main 은 branch protection 으로 보호되며
`enforce_admins: true` 이므로 소유자의 직접 push 도 거부된다. 릴리스도 CI 3 체크
(`Plugin Validation` / `Playwright Visual Tests` / `Harness Integration Tests`)를
통과해야 main 에 들어간다. 이 레포는 Playwright 잡이 32 회 연속 red 인 채로 릴리스가
계속 나간 이력이 있어 이렇게 바꿨다.

태그는 branch protection 대상이 아니므로 즉시 push 된다.

**PR 을 머지하지 않고 버리면 태그가 main 에서 도달 불가능해진다.** 그 경우 태그도 지운다:

```bash
git push origin :refs/tags/<plugin>/v<version> && git tag -d <plugin>/v<version>
```

### 미리보기

실제 동작 없이 계산 결과만 보려면:

```bash
bash scripts/release.sh <plugin-name> <bump-type> --dry-run
```

버전 파일은 수정되므로 `git checkout -- <파일>` 로 되돌린다.

### 머지

```bash
gh pr checks <PR-URL>
gh pr merge <PR-URL> --merge --delete-branch
```

## 실행 전 확인

스크립트를 실행하기 **전에** 사용자에게 요약을 보여주고 확인을 받는다:

```text
릴리스 요약:
  플러그인: harness
  현재 버전: 0.1.1
  새 버전: 0.1.2 (patch)
  태그: harness/v0.1.2

진행할까요?
```

현재 버전은 해당 plugin.json에서 읽는다.

## 릴리스 후 마켓플레이스 갱신

스크립트가 성공하면 로컬 마켓플레이스 캐시를 갱신한다:

```bash
claude -p "/plugin marketplace update joo6077-plugins"
```

이 명령이 실패해도 릴리스 자체는 완료된 것이므로 에러로 취급하지 않고, 사용자에게 수동 실행을 안내한다:
`/plugin marketplace update joo6077-plugins`

## 에러 처리

- 스크립트가 실패하면 에러 메시지를 그대로 사용자에게 전달한다
- dirty working tree 경고가 나오면 사용자에게 먼저 커밋할지, 그냥 진행할지 확인한다
- push 실패 시 네트워크/인증 문제일 수 있으므로 수동 push를 안내한다
