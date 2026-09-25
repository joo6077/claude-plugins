# sprint-amendments-flutter-scenario-report

봉인된 계약(`sha256:be16c86ab07f4154`, 봉인 커밋 `bff6d7b`) 본문은 수정하지 않는다. 아래는 봉인 이후 사용자 동의로 확정한 개정이다.

## A-01 · AR-01 이 문법 검사 부산물 `__pycache__` 를 세지 않는다 (2026-09-25)

**문제** — 조건끼리 부딪혔다. DG-05 의 측정 `python3 -m py_compile "$SKILL/scripts/build_report.py"` 는 `$SKILL/scripts/__pycache__/build_report.cpython-314.pyc` 를 만든다. AR-01 의 측정 `find . -type f -not -name '.DS_Store'` 는 그 파일까지 세서, 평가자가 DG-05 를 먼저 돌리면 구현과 무관하게 AR-01 이 떨어진다. 이 레포 `.gitignore:4` 는 루트 `scripts/__pycache__/` 만 빼고 스킬 폴더의 `__pycache__` 는 빼지 않는다.

**개정** — AR-01 의 측정을 아래로 읽는다. 기대 출력은 그대로 `./SKILL.md ./references/record-format.md ./scripts/build_report.py` 다.

```bash
(cd "$SKILL" && find . -type f -not -name '.DS_Store' -not -path '*/__pycache__/*' | sort | paste -sd' ' -)
```

**direction: relaxing** — 측정 집합이 줄어 통과하는 상태가 늘어난다. 계산 (헬퍼 `amend_direction_oracle`, contract-schema §Amendment 사이드카 — 측정 명령을 바꾸는 개정이라 허용 집합 헬퍼가 아니라 이것을 썼다):

```text
원 측정 집합   ./SKILL.md · ./references/record-format.md · ./scripts/__pycache__/build_report.cpython-314.pyc · ./scripts/build_report.py
개정 측정 집합 ./SKILL.md · ./references/record-format.md · ./scripts/build_report.py
$ amend_direction_oracle orig.txt amended.txt
relaxing measured_removed=1 measured_added=0
```

**consent: anchored** — 세션 기록의 `AskUserQuestion` 쌍 (contract-schema §Amendment 사이드카 축 2 의 두 번째 출처).

- 질문 제목 `조건 개정` · 호출 `2026-09-25T07:04:20.943Z` · **답변(동의 시각) `2026-09-25T07:04:45.099Z`**
- 세션 `e6978555-fef9-4611-a5d0-f6a8085b3924` · 작업 폴더 `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/flutter-scenario-report`
- 고른 답: "부산물은 빼고 세기 (추천)" — 선택지 설명 "`__pycache__` 는 검사 도구가 만드는 임시 파일이라 스킬에 들어가는 파일이 아닙니다 … 실제 스킬 파일 3개라는 뜻은 그대로입니다"
- 추출 명령: contract-schema §Amendment 사이드카 의 `AskUserQuestion` 짝짓기 스크립트를 세션 기록 `~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/e6978555-fef9-4611-a5d0-f6a8085b3924.jsonl` 에 돌린 출력이다
- 이 개정과 구현을 담은 커밋은 동의 시각보다 뒤에 만든다

**영향** — AR-01 이 지키려던 뜻(스킬이 담는 파일은 세 개뿐, 다른 파일을 끼워 넣지 않는다)은 그대로다. 빠지는 것은 파이썬이 실행 중에 만드는 컴파일 부산물 한 종류뿐이고, 이 폴더는 커밋하지 않는다 (AR-10 이 커밋된 파일을 따로 잰다).
