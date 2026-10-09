# Codex 진행 상황 (VS Code 확장)

Codex 감독(`harness/scripts/codex-audit.sh`) · 리서치(`~/.claude/bin/codex-research`)가 도는 동안만, 그 창의 작업 폴더에서 도는 작업을 하단 상태 표시줄에 항목 하나로 짧게 띄운다.

```text
$(sync~spin) 감독 1 · 리서치 1
```

- 마우스를 올리면 작업마다 한 줄이 보인다 — `a1b2 리서치 · <주제> · 시도 1/3 · 30초 · 5시간 12% · 주간 3%`. 앞 4 글자는 그 작업을 띄운 Claude 세션(`CLAUDE_CODE_SESSION_ID`), 주제는 리서치 프롬프트의 `Goal:` 줄이다.
- 세션별 자세한 진행은 그 세션 채팅 창의 작업 카드로 본다(리서치 실행기가 30 초마다 진행 줄을 낸다).
- 도는 작업이 없으면 아무것도 띄우지 않는다. 사용량은 이미 풀린 창은 빼고 보인다.
- 읽는 곳: `~/.codex-status/`(`CODEX_STATUS_DIR` 로 바꾼다). 작업 파일은 쓰는 쪽이 끝날 때 지우고, 2 분 넘게 갱신이 멈춘 파일은 보이지 않는다.

설치: `bash harness/vscode-status/install.sh` 뒤 VS Code 에서 「Developer: Reload Window」.
