# Sprint Feedback
Feature: reflect-kit v0.2.0 — Claude fallback · 스케줄러 · cross-project digest · redaction 강화 · 구ID 마이그레이션
Evaluated: 2026-04-17 15:30
Verdict: REJECT
Iteration: 1

## Results

### Skill (3/3)
- [x] SK-01: reflect-digest/SKILL.md에 `project=all` cross-project 집계 섹션(5개 서브섹션) 포함 — PASS
  - 근거: `reflect-kit/skills/reflect-digest/SKILL.md:95-158` — 섹션 "## Cross-project 집계 (v0.2.0: project=all)" 하위 ### 1~5 5개 서브섹션 확인
  - (a) 글로벌 순회 규칙: 라인 100-105 ✓  (b) 이중 freq 계산: 라인 106-113 ✓  (c) Precedence Table 재적용: 라인 114-127 ✓  Given-When-Then: 라인 128-139 ✓  출력 포맷 예시: 라인 140-158 ✓
- [x] SK-02: 출력 포맷 예시에 "대상 프로젝트 수 N개 / 총 엔트리 M개" 메타라인 명시 — PASS
  - 근거: `reflect-kit/skills/reflect-digest/SKILL.md:135` — `대상 프로젝트: N개 (레거시 L개 / 해시 포맷 H개) / 총 엔트리: M개`
  - 출력 예시 라인 144-145 에도 구체 수치 포함 ✓
- [x] SK-03: reflect-promote/SKILL.md의 rule #3 설명에 `/reflect-digest project=all` 링크 문장 추가 — PASS
  - 근거: `reflect-kit/skills/reflect-promote/SKILL.md:56` — "반드시 `/reflect-digest project=all` 출력의 `global_freq` + `project_count` 두 값을 함께 확인해야 rule #3 로 올바르게 분류된다"

### Script (4/5)
- [x] SC-01: codex 실패 시 Claude CLI fallback 실행 + 4개 태그 기록 — PASS
  - 근거: `log-reflection.sh:140-168` — `try_claude_fallback()` 함수 내부에서 codex_exit!=0 시 `fail:codex-exit-N` 기록(라인 142), `command -v claude` 체크(라인 144), `claude -p --model haiku-4.5` 호출(라인 151), 성공 시 `fallback:claude-used`(라인 165), Claude exit!=0 시 `fallback:claude-exit-N`(라인 157), 빈 출력 시 `fallback:claude-empty-output`(라인 161), 미설치 시 `skip:fallback-unavailable`(라인 145)
  - 성공 시 `out_file` append: 라인 197-207 (summary → reflections-*.md) ✓
- [x] SC-02: JSON 쌍따옴표 내 시크릿 매칭 패턴 추가 + 기존 11종 유지 — PASS
  - 근거: `_lib-redact.sh:37` — `("[A-Z_]*(API|...)..."[^"]{4,}"/\1[REDACTED]"/g` JSON 패턴 추가
  - 동작 테스트: `{"API_KEY": "sk-short-xyz-1234567890"}` → `{"API_KEY": "[REDACTED]"}` 치환 확인 ✓
  - 기존 11종 패턴(sk-ant/sk-proj/sk-20+/github_pat/ghp/gho/ghu/ghs/ghr/xox/AKIA/AIza/eyJ/Bearer/ENV_KEY=) 라인 22-36 전부 존재 ✓
- [x] SC-03: install-scheduler.sh — 5가지 요건 전부 충족 — PASS
  - 근거: (a) `--dry-run` → `dry_run()` 함수: echo만, crontab 미접촉(라인 31-37) ✓  (b) `--install` → `install_all()` → `append_if_absent()`(라인 43-57) `crontab -l | (cat;echo) | crontab -` 방식 ✓  (c) `WEEKLY_LINE`(라인 24: `0 9 * * 1`) + `MONTHLY_LINE`(라인 25: `0 9 1 * *`) 2개 ✓  (d) `-rwxr-xr-x` 확인 ✓  (e) `grep -qF -- "$line"`(라인 49): 멱등성 ✓
- [x] SC-04: legacy-id-migrate.sh — 5가지 요건 전부 충족 — PASS
  - 근거: (a) `HASH_PATTERN='-[0-9a-f]{6}$'`(라인 24) + `[[ ! "$pid" =~ $HASH_PATTERN ]]`(라인 78) 감지 로직 ✓  (b) `plan_migration()`: rename/merge 계획 stdout 출력(라인 103-136) ✓  (c) `execute_migration()`: 실제 rename/concat merge(라인 139-198) ✓  (d) concat 순서 `cat "$oldfile" "$target"`(라인 180): 레거시→신규 순서 ✓  (e) `-rwxr-xr-x` 확인 ✓
- [ ] SC-05: 릴리스 완료 — FAIL (DEFERRED 해당되나 로컬 git tag 부재)
  - 근거: `git tag -l "reflect-kit/v0.2.0"` 결과 없음. 존재하는 태그: `reflect-kit/v0.1.0`만.
  - `plugin.json:4` version `"0.2.0"` ✓, `marketplace.json:51` `[v0.2.0 · 2026-04-17]` ✓
  - **git tag 미생성** — 계약이 "git tag reflect-kit/v0.2.0 생성 + origin push 완료"를 요구하며, 정적 검증 항목인 "git tag -l reflect-kit/v0.2.0 로컬 확인"도 미충족
  - 계약이 DEFERRED 허용 범위: "네트워크 미연결 환경에서는 로컬 검증만 요구" — 로컬 태그도 없으므로 DEFERRED 해당 안 됨

### Error (2/3)
- [x] ER-01: codex 실패 + Claude fallback 실패 시 2개 태그 순서대로 기록 — PASS
  - 근거: `try_claude_fallback()` 내부에서 먼저 `fail:codex-exit-N` 기록(라인 142), 이후 Claude exit!=0 시 `fallback:claude-exit-M`(라인 157) 또는 빈 출력 시 `fallback:claude-empty-output`(라인 161) 기록. 두 태그 모두 순서대로 append ✓
- [x] ER-02: Claude CLI 미설치 + codex 실패 시 `skip:fallback-unavailable` 1회 + exit 0 — PASS
  - 근거: `log-reflection.sh:144-146` — `command -v claude` 실패 → `skip:fallback-unavailable session=$session_id` 기록 → `return 1` → 호출 지점 `|| exit 0`(라인 188) 실행. 1회만 기록되고 훅 exit 0 ✓
- [x] ER-03: project=all 중 일부 프로젝트 실패 시 skip + 리포트 말미 집계 실패 블록 표시 — PASS [정적]
  - 근거: `reflect-digest/SKILL.md:104` — "읽기 실패는 해당 프로젝트만 skip (ER-03)" 명시. 라인 136 Given-When-Then 출력 포맷에 `집계 실패 프로젝트: K개 (project_id 리스트)` 명시. 라인 138 `0개여도 생략 안 함` ✓
  - [정적] — MCP 서버 미설정으로 런타임 미수행

### Architecture (3/3)
- [x] AR-01: `reflect-kit/scripts/` 신규 생성 + 실행 권한 — PASS
  - 근거: `ls -l` 결과 `install-scheduler.sh: -rwxr-xr-x` ✓ (2026-04-17 14:29)
- [x] AR-02: background wrapper 구조 유지 — PASS
  - 근거: (a) `log-reflection.sh:23` `"--background"` 분기 존재 ✓  (b) `라인 43-45`: `nohup ... &` + `disown` + `exit 0` ✓  (c) `try_claude_fallback` 호출 위치 `라인 188-190`: 백그라운드 전용 블록(라인 48 이후)에만 존재, fast path(라인 33-46)에는 없음 ✓
- [x] AR-03: README에 "## Scheduling (v0.2.0+)" 섹션 + 3가지 방식 — PASS
  - 근거: `README.md:116` `## Scheduling (v0.2.0+)` ✓  (a) `/schedule create` 예시(라인 123-124) ✓  (b) `crontab -e` 직접 등록(라인 131-135) ✓  (c) `install-scheduler.sh` 사용법(라인 141-147) ✓

### Anti-patterns (1/3)
- [ ] AP-01: 버전 하드코딩 — FAIL
  - 근거: `reflect-kit/README.md:7` — `버전: \`0.1.0\`` 하드코딩. plugin.json v0.2.0과 불일치.
  - 수정: README 라인 7의 버전을 `0.2.0`으로 갱신하거나, plugin.json에서 동적으로 읽는 방식으로 변경
- [x] AP-03: bare code fence 없음 — PASS
  - 근거: `python3 scripts/validate-plugin.py reflect-kit` V6 결과 `0 bare — OK` ✓ (awk 분석으로 여는 bare fence 없음 확인)
- [x] AP-04: SKILL.md frontmatter name 필드 존재 — PASS
  - 근거: `validate-plugin.py` V1 결과 `3 skills — OK` ✓

### Reusability (2/2)
- [x] RE-01: try_claude_fallback() 함수로 추출 — PASS
  - 근거: `log-reflection.sh:140-168` — `try_claude_fallback()` 함수로 명시적 추출됨 ✓
- [x] RE-02: _lib-redact.sh 기존 패턴 재작성 없이 추가만 — PASS
  - 근거: `_lib-redact.sh:22-37` — 기존 15개 패턴 + 신규 JSON 패턴(라인 37) 추가. 기존 패턴 라인 22-36 전부 유지됨 ✓

### Diagnostics (3/4)
- [x] DG-01: bash -n 워닝 0개 + 실행 권한 확인 — PASS
  - 근거: `bash -n *.sh` Exit 0 ✓. 훅 5개 전부 `-rwxr-xr-x`. scripts/ 2개 전부 `-rwxr-xr-x` ✓
- [x] DG-02: IDE diagnostics 워닝/인포 0개 — PASS [정적]
  - 근거: bash -n 0 warning. shell script 외 IDE 검사는 MCP 미설정으로 [정적] ✓
- [x] DG-03: validate-plugin.py reflect-kit V1~V7 전 PASS — PASS
  - 근거: `V1 OK · V2 SKIP · V3 OK · V4 OK · V5 OK · V6 OK · V7 OK. Exit: 0` ✓
- [ ] DG-04: 수동 fallback 시뮬레이션 — [미검증]
  - 근거: [goal] 조건이나 코드 경로로 대체 확인. `log-reflection.sh:188` codex exit 1 → `try_claude_fallback` → `claude -p --model haiku-4.5` → summary → reflections-*.md append 경로 정적 추적 완료. 실제 런타임 실행은 MCP 서버 미설정으로 미수행.
  - [미검증] — 계약이 "[goal]"로 명시된 목표 달성 검증. 단일 미검증이므로 REJECT 미가중.

## Summary
- Total: 18/23 conditions PASS, 2 FAIL, 1 DEFERRED(SC-05), 1 미검증(DG-04)
- SC-05: git tag reflect-kit/v0.2.0 로컬 태그 미생성
- AP-01: README.md 라인 7 `버전: \`0.1.0\`` — v0.2.0과 불일치

## Verdict: REJECT

**FAIL 원인 2개:**

1. **SC-05** — `git tag reflect-kit/v0.2.0`이 로컬에도 존재하지 않음. 계약이 명시한 로컬 정적 검증(`git tag -l reflect-kit/v0.2.0`) 실패. plugin.json과 marketplace.json은 갱신되었으나 태그 생성 자체가 누락됨.
   - 수정: `git tag reflect-kit/v0.2.0 && git push origin reflect-kit/v0.2.0`

2. **AP-01** — `reflect-kit/README.md:7`에 `버전: \`0.1.0\`` 하드코딩. plugin.json v0.2.0과 불일치.
   - 수정: README 라인 7 → `버전: \`0.2.0\`` 갱신 (또는 삭제 후 plugin.json 기준으로 통일)

⚠️ 런타임 검증 미수행 — MCP 서버 미설정
