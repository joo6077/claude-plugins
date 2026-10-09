# Codex 진행 상황 (VS Code 확장)

Codex 감독(`harness/scripts/codex-audit.sh`) · 리서치(`~/.claude/bin/codex-research`)가 도는 동안만, 그 창의 작업 폴더에서 도는 작업을 작업마다 하단 상태 표시줄에 하나씩 띄운다.

```text
$(sync~spin) a1b2 감독 judge-1 · 4분 · 5시간 12% · 주간 3%
```

- 앞 4 글자는 그 작업을 띄운 Claude 세션(`CLAUDE_CODE_SESSION_ID`)이다. 마우스를 올리면 세션 전체와 폴더가 보인다.
- 도는 작업이 없으면 아무것도 띄우지 않는다. 사용량은 이미 풀린 창은 빼고 보인다.
- 읽는 곳: `~/.codex-status/`(`CODEX_STATUS_DIR` 로 바꾼다). 작업 파일은 쓰는 쪽이 끝날 때 지우고, 2 분 넘게 갱신이 멈춘 파일은 보이지 않는다.

설치: `bash harness/vscode-status/install.sh` 뒤 VS Code 에서 「Developer: Reload Window」.
