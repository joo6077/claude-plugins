# sprint-amendments-plain-korean-output-gate

계약 본문(`sprint-contract-plain-korean-output-gate.md`)은 봉인 후 건드리지 않았다.
`SEAL_OK` 상태를 유지한다. 아래는 조건을 "이렇게 읽어라" 는 덧붙임이다.

## AM-01 — relaxing

- 대상 조건: AR-03
- 변경: 삭제 기대 집합을 1 개에서 2 개로 넓힌다.
  원: `hooks/_probe-stop-payload.sh`
  개정: `hooks/_probe-stop-payload.sh` · `_probe-stop-payload.json`
- direction 계산 (`amend_direction`, 허용 집합 입력): `relaxing added=1 removed=0`
- 사유: 같은 계약의 AR-01 이 시험용 파일 2 개를 모두 지우라고 요구하는데, AR-03 의 삭제 목록에는
  1 개만 적혀 있었다. 계약 작성자(나)의 누락이며 구현 결함이 아니다. AR-01 을 지키면 AR-03 을
  어기게 되는 구조였다.
- 근거 (redaction 거친 원문): "둘 다 승인"
- 앵커: 2026-09-11 · session=13d78b94-efc9-4ba6-8586-d5d9009d3c98 · cwd=/Users/jackson/Hub/10_Dev/claude-plugins
  (reflect-kit prompt 로그 대신 이 세션의 선택형 질문 응답을 앵커로 쓴다. timestamp 는 분 단위까지만 확보)

## AM-02 — relaxing

- 대상 조건: AR-03
- 변경: 재는 범위에서 `mcp-needs-auth-cache.json` 을 뺀다. 원 조건의 제외 목록은
  `~/.claude/.plain-korean-*` 뿐이었다.
- direction 계산 (`amend_direction_oracle`, 측정 집합 입력 20 → 19): `relaxing measured_removed=1 measured_added=0`
- 사유: 이 파일은 Claude Code 가 스스로 쓰는 실행 기록이다. 내용이
  `{"plugin:figma:figma":{"timestamp":1789093968382}}` 한 줄이고, 바뀐 시각 11:32 는 기준값을 뜬
  11:30 이후다. 이번 작업이 건드린 파일이 아니다. 원 조건이 실행 기록 제외를
  `.plain-korean-*` 로만 좁게 적은 것이 원인이다.
- 근거 (redaction 거친 원문): "둘 다 승인"
- 앵커: 2026-09-11 · session=13d78b94-efc9-4ba6-8586-d5d9009d3c98 · cwd=/Users/jackson/Hub/10_Dev/claude-plugins

## AR-03 개정 후 측정

```bash
{ find ~/.claude -maxdepth 1 -type f -name '*.json' -o -maxdepth 1 -type f -name '*.md'; \
  find ~/.claude/hooks ~/.claude/rules -type f 2>/dev/null; } \
  | sort -u | grep -v '\.plain-korean-' | grep -v 'mcp-needs-auth-cache\.json'
```

기대: 변경·신규 정확히 4 개 (`CLAUDE.md` · `settings.json` · `hooks/check-plain-korean.sh` ·
`rules/plain-korean.md`) + 삭제 정확히 2 개 (`hooks/_probe-stop-payload.sh` · `_probe-stop-payload.json`)

## AM-03 — relaxing

- 대상 조건: AR-03 (그리고 그것과 충돌하던 RE-01)
- 변경: 변경·신규 기대 집합을 4 개에서 5 개로 넓힌다.
  원: `CLAUDE.md` · `settings.json` · `hooks/check-plain-korean.sh` · `rules/plain-korean.md`
  개정: 위 4 개 + `hooks/_lib-hook-payload.sh`
- direction 계산 (`amend_direction`, 허용 집합 입력): `relaxing added=1 removed=0`
- 사유: 계약이 서로 어긋나는 두 가지를 요구했다. RE-01 의 적용 메모는 답변 되돌리는 출력을
  공용 파일에 두라고 했는데, AR-03 은 그 공용 파일을 변경 목록에서 뺐다. 어느 쪽을 지켜도
  다른 쪽을 어기는 구조였고, QA 가 이 충돌을 사용자 결정 사항으로 표면화했다.
  공용 파일에는 이미 도구 쓰기 전 막는 함수(`hook_deny`)와 도구 쓴 뒤 알리는 함수
  (`hook_notice`)가 있다. 답변 되돌리는 함수(`hook_stop_block`)만 빠져 있었으므로 그 자리가 맞다.
- 근거 (redaction 거친 원문): "공용 파일에 넣는다 (권함)"
- 앵커: 2026-09-11 · session=13d78b94-efc9-4ba6-8586-d5d9009d3c98 · cwd=/Users/jackson/Hub/10_Dev/claude-plugins

### AM-03 적용 후 AR-03 기대값

변경·신규 정확히 5 개 + 삭제 정확히 2 개 (AM-01 적용분).
