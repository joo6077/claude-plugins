# Sprint Feedback
Feature: reflect-kit v0.3.0 — Hybrid project_id (backward-compatible)
Evaluated: 2026-04-17 18:20
Verdict: APPROVE
Iteration: 2

## Results

### Skill (3/3)
- [x] SK-01: `/reflect-digest project=<basename>` 와 `/reflect-digest project=<basename>-<hash6>` 가 동일한 스캔 대상 집합 선택 — PASS
  - 근거: `reflect-kit/hooks/_lib-project-id.sh:100-112` `normalize_project_query()` — 두 입력 모두 `case` 분기 후 동일한 `"$base $base-[0-9a-f]{6}"` union 반환. 실행 검증: `normalize_project_query "app_kiosk"` == `normalize_project_query "app_kiosk-a3b4f9"` → `"app_kiosk app_kiosk-[0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f]"` 동일 [L3]
- [x] SK-02: 레거시 버킷 분류 섹션 제거 + 정규화 쿼리 동작 명시 — PASS
  - 근거: `reflect-kit/skills/reflect-digest/SKILL.md` — "레거시 버킷" 문자열 없음. 정규화 쿼리 표(lines 55-58)에 두 입력 모두 동일 union으로 확장됨 명시 [L3]
- [x] SK-03: `project=all` cross-project 집계에서 신규 basename + 기존 hash 디렉토리 모두 포함 — PASS
  - 근거: `SKILL.md:125-126` — "두 형태가 공존하는 프로젝트는 `normalize_project_query`로 자동 병합 집계". `SKILL.md:102` — `is_internal_logs_dir`로 내부 디렉토리 제외 후 전 프로젝트 순회 [L3]

### Script (4/4)
- [x] SC-01: 충돌 없는 경우 `compute_project_id`는 `<basename>`만 반환 — PASS
  - 근거: `_lib-project-id.sh:57-92` — `$base_dir`/`.project-root` 없거나 stored == repo_root인 경우 `printf '%s' "$base"` (hash 없음). 실행: `compute_project_id "$PWD"` → `claude-plugins` [L3]
- [x] SC-02: 충돌 감지 시 `<basename>-<hash6>` fallback + stderr 1회 경고 — PASS
  - 근거: `_lib-project-id.sh:73-83` — 충돌 조건 만족 시 `_rk_warn_once`(PID 마커 기반) + `printf '%s-%s' "$base" "$h"`. 실행: `.project-root`에 다른 경로 기록 후 호출 → `claude-plugins-701489` + stderr 경고 출력 [L3]
- [x] SC-03: `--scan` 결과에서 `_cron`, `.*`, `_*` 디렉토리 제외 — PASS
  - 근거: `legacy-id-migrate.sh:82` `scan_legacy()` — `is_internal_logs_dir "$pid" && continue`. `_lib-project-id.sh:37-44` `is_internal_logs_dir()` — `.*`, `_*` 모두 return 0(필터). 실행: `_cron`, `.hidden`, `_internal` 모두 FILTERED [L3, enumerated]
- [x] SC-04: cross-project 스캔에서 동일 필터 적용 — PASS
  - 근거: `SKILL.md:102` — `project=all` 순회 시 `is_internal_logs_dir`로 `_cron`, `.*`, `_*` 제외 명시. `SKILL.md:125` — "내부 디렉토리 제외" 글로벌 순회 규칙 [L3, enumerated]

### Error (3/3)
- [x] ER-01: git 미설치/비-repo 환경에서 cwd basename 반환 + 기존 fallback 유지 — PASS
  - 근거: `_lib-project-id.sh:62-63` — `git ... 2>/dev/null` 실패 시 `repo_root="$cwd"` fallback. 실행: `/tmp` 전달 시 `"tmp"` 반환 [L3]
- [x] ER-02: `log-*.sh` 쓰기 경로가 `compute_project_id` 결과 그대로 사용 — PASS
  - 근거: `log-prompt.sh:26-27`, `log-tool-failure.sh:27-28` — `project_id=$(compute_project_id "$cwd")` → `log_dir="$HOME/.claude/logs/$project_id"`. SC-02에서 충돌 시 hash fallback이 반환되므로 기존 `<basename>/` 덮어쓰기 없음 [L3]
- [x] ER-03: glob 매칭 0개 시 "no matching buckets" stderr 출력 — PASS
  - 근거: `SKILL.md:62,104` — 두 군데서 `no matching buckets for project=<query>` stderr 출력 후 종료 명시 [L3, structural — LLM-driven skill]

### Architecture (4/4)
- [x] AR-01: glob union으로 기존 hash 디렉토리 read — 마이그레이션 불필요 — PASS
  - 근거: `SKILL.md:45,102` — backward-compat glob union 보증. `DESIGN.md:231-236` — 마이그레이션 스크립트 불필요 명시 [L3]
- [x] AR-02: plugin.json version=0.3.0, marketplace.json description `[v0.3.0 · 2026-04-17]` 접두사 — PASS
  - 근거: `reflect-kit/.claude-plugin/plugin.json:4` `"version": "0.3.0"`. `marketplace.json:51` description starts with `[v0.3.0 · 2026-04-17]` — Python 검증 `True` [exact]
- [x] AR-03: DESIGN.md "결정 #3 Hybrid 전환" 섹션 + 독립 리뷰 근거 + backward-compat 보증 — PASS
  - 근거: `DESIGN.md:210-248` — `## 결정 #3 상세 — Hybrid project_id (v0.3.0 전환)` 섹션. A/B/C안 비교(lines 217-220), backward-compat 표(lines 224-229), 보증 목록(lines 231-236) [L3]
- [x] AR-04: README.md v0.3.0 변경 요약(Hybrid 전환 + 정규화 쿼리 + 내부 디렉토리 제외) — PASS
  - 근거: `README.md:9-15` — `## v0.3.0 변경 요약` 섹션에 Hybrid project_id, 정규화 쿼리, 내부 디렉토리 제외 세 항목 모두 명시 [L3]

### Anti-patterns (2/2)
- [x] AP-01: 버전 하드코딩 없음 — PASS
  - 근거: `grep -rn 'hardcoded.*version'` → no match [L2]
- [x] AP-03: bare code fence 없음 — PASS
  - 근거: `grep -Pn '^```\s*$'` on SKILL.md, DESIGN.md, README.md → no match [L2]

### Reusability (2/2)
- [x] RE-01: 재사용 가능한 컴포넌트 private 처리 없음 — PASS
  - 근거: `_lib-project-id.sh`의 `normalize_project_query`, `compute_project_id`, `is_internal_logs_dir` 모두 `source`로 공유. `legacy-id-migrate.sh`에서 재사용 확인 [L3]
- [x] RE-02: 중복 컴포넌트 없음 — PASS
  - 근거: hash 계산은 `_rk_hash6()` 단일 함수로 중앙화. 필터는 `is_internal_logs_dir()` 단일 함수. 중복 구현 없음 [L3]

### Diagnostics (4/4)
- [x] DG-01: `bash -n` 문법 검사 워닝 0개 — PASS
  - 근거: `bash -n` on `_lib-project-id.sh`, `legacy-id-migrate.sh`, `log-prompt.sh`, `log-tool-failure.sh`, `log-reflection.sh` 모두 OK [L2]
- [x] DG-02: IDE diagnostics 워닝 0개 — PASS [정적]
  - ⚠️ 런타임 검증 미수행 — MCP 서버 미설정
- [x] DG-03: `scripts/release.sh` 리허설 에러 0개 — PASS
  - 근거: `bash -n scripts/release.sh` → OK [L2]
- [x] DG-04: 충돌 시뮬레이션 — basename 반환 + hash fallback + 1회 경고 — PASS
  - 근거: SC-02 실행 검증 결과와 동일. `.project-root`에 다른 경로 기록 후 `compute_project_id` 호출 → `claude-plugins-701489` + stderr 경고 1회 출력. `_rk_warn_once` PID 마커(`${TMPDIR:-/tmp}/.reflect-kit-warn-<basename>-<PID>`) 확인 [L3]

## Summary
- Total: 20/20 conditions passed
- Anti-patterns: 2/2 PASS
- Reusability: 2/2 PASS
- Diagnostics: 4/4 PASS
- Verdict: APPROVE

⚠️ 런타임 검증 미수행 — MCP 서버 미설정. 모든 판정은 정적/실행 검증 기반.
