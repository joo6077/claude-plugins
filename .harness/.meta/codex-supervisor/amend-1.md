계약 개정 요청 (개정 1). 계약은 이미 봉인됐다(커밋 850cf4c9, conditions_digest sha256:2467113bd3f57fd7). 계약 본문 /Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/codex-supervisor/.harness/sprint-contract-codex-supervisor.md 은 고치지 않는다.

요구사항 문서 /Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/codex-supervisor/.harness/.meta/codex-supervisor/requirements.md 의 「## 6. 개정 1」 을 읽어라. 첫 구현 감독 보고서는 /Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/codex-supervisor/.harness/codex-audit/codex-supervisor/impl-r1/report.md 다. 개정 파일 규약은 /Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/codex-supervisor/harness/references/contract-schema.md 의 「## Amendment 사이드카」 절이다.

할 일:
1. ./out/sprint-amendments-codex-supervisor.md 를 쓴다. 규약의 엔트리 포맷(번호 AM-01 부터 · 유형 · 대상 조건 · 변경 · 근거 · 앵커)을 따른다. 개정 1 의 요구 8 개를 조건으로 덮는 새 조건(번호는 기존 계약 번호에 이어서, 예: 스크립트-12 …)과 그 측정 줄을 개정 항목 안에 적는다. 앵커는 요구사항 문서에 적힌 세션 기록 값을 직접 그 파일에서 확인해 적는다(사용자 메시지 「1」).
2. direction 은 규약의 계산법으로 정한다. 새 조건 추가는 PASS 집합을 줄이지만, 판정이 사전 측정 기록을 증거로 받게 되는 것은 기존 조건(스크립트-11 · 오류-02 · 구조-04 등)의 증거 출처를 바꾼다 — 이 점을 숨기지 말고 따로 항목으로 적고 방향을 판정하라.
3. ./out/measure/ 의 측정 묶음에 새 조건 측정을 더한다. 기존 조건의 측정 코드는 바꾸지 않는다(바꿔야 하면 개정 항목에 바꾼 파일 · 이유 · 바꾸기 전후 sha256 앞 16 자리를 적는다). 지금 구현에는 사전 측정 기능이 없으므로 새 조건 측정은 지금 FAIL 해야 한다. 양성 · 음성 대조와 알려진 답은 계약과 같은 규칙을 따른다.
4. 검증: bash -n · zsh -n · py_compile, 새 조건 측정을 지금 돌려 FAIL 확인, --controls-only 대조 기대값 일치, 기존 조건 하나 이상을 돌려 측정 코드 변경이 없음을 확인. 최종 답에 만든 파일 · 새 조건 번호 · direction 계산 · 명령 출력.
