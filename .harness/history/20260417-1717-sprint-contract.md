---
feature: "reflect-kit v0.2.0 — Claude fallback · 스케줄러 · cross-project digest · redaction 강화 · 구ID 마이그레이션"
created: "2026-04-17 14:16"
complexity: "중간"
conditions: 23
---

## Skill
- [ ] SK-01: `reflect-kit/skills/reflect-digest/SKILL.md`에 `project=all` 인자 지원이 명시되며 "cross-project 집계" 섹션을 포함한다. 섹션은 (a) `~/.claude/logs/*/reflections-*.md` 글로벌 순회 규칙, (b) 프로젝트별 빈도 + 글로벌 freq 합산 표시, (c) Precedence #3(`scope=global AND 복수 프로젝트 freq≥3`) 판정 연동 3단계를 모두 포함한다 [structural, enumerated]
- [ ] SK-02: Given `project=all` 인자가 전달되면, When digest가 전 프로젝트 로그를 순회하고, Then 리포트 상단에 "대상 프로젝트 수 N개 / 총 엔트리 M개" 메타라인이 표시되도록 SKILL.md 출력 포맷 예시가 명시된다 [structural]
- [ ] SK-03: `reflect-kit/skills/reflect-promote/SKILL.md`의 Precedence rule #3 설명에 "복수 프로젝트 freq ≥ 3" 판정 근거를 `/reflect-digest project=all` 출력으로 링크하는 문장이 1개 이상 추가된다 [structural]

## Script
- [ ] SC-01: `reflect-kit/hooks/log-reflection.sh`에서 codex exec가 `codex_exit != 0` 또는 empty output을 반환하면, Claude CLI fallback이 실행된다 — 구체: `command -v claude` 체크 후 `claude -p --model haiku-4.5` 로 동일 프롬프트 호출, 성공 시 reflections-YYYY-MM.md에 append + `.errors.log`에 `fallback:claude-used session=<id>` 태그 기록. Claude CLI 미설치 시 `skip:fallback-unavailable` 태그 기록 후 exit 0 [exact, enumerated]
- [ ] SC-02: `reflect-kit/hooks/_lib-redact.sh`에 JSON 쌍따옴표 내 짧은 시크릿 매칭 패턴이 최소 1개 추가된다. 테스트: 입력 `{"API_KEY": "sk-short-xyz-1234567890"}` 에 `redact_sensitive` 적용 시 해당 값 부분이 `[REDACTED]` 으로 치환되는 것을 `grep`으로 확인할 수 있어야 한다. 기존 11종 패턴(sk-ant, sk-proj, sk-{20자+}, github_pat, ghp/gho/ghu/ghs/ghr, xox, AKIA, AIza, eyJ, Bearer, ENV_KEY=) 은 **전부 유지** — 해당 패턴 라인 11개가 파일에 모두 존재 [exact, enumerated]
- [ ] SC-03: `reflect-kit/scripts/install-scheduler.sh` 신규 파일이 존재하며 다음을 만족한다 — (a) `--dry-run` 플래그로 등록할 cron 라인을 stdout에 출력만, (b) `--install` 플래그로 `crontab -l | (cat; echo <line>) | crontab -` 방식 등록, (c) 주간(월 09:00)과 월간(매월 1일 09:00) 2개 cron 라인을 동시 관리, (d) 실행 권한(`+x`) 부여, (e) **멱등성 보장 — `--install` 2회 실행 시 동일 cron 라인이 중복 등록되지 않는다** (`crontab -l`에 동일 라인 존재 여부를 `grep -qF`로 체크 후 건너뜀) [exact, enumerated]
- [ ] SC-04: `reflect-kit/scripts/legacy-id-migrate.sh` 신규 파일이 존재하며 다음을 만족한다 — (a) `--scan` 플래그로 `~/.claude/logs/` 내 **해시 접미사(`-[0-9a-f]{6}$` 패턴) 없는** 레거시 project_id 디렉토리를 감지하는 로직이 구현되어 있음 (스크립트 내부 정규식·케이스 구분 등 알고리즘이 존재), 감지된 디렉토리와 basename 기반 후보 git repo 경로를 stdout 리스트 출력, (b) `--dry-run` 플래그로 rename/merge 계획(이동 대상·신규 ID·기존 reflections-*.md와 충돌 여부)만 stdout 출력, (c) `--execute` 플래그로 실제 rename + 충돌 디렉토리는 `misunderstandings-*.md`/`reflections-*.md`/`YYYY-MM.md` 각각 concat merge 실행, (d) **concat merge 순서는 파일명(YYYY-MM 또는 타임스탬프 헤더) 오름차순으로 정렬하여 병합** — 최신 엔트리가 파일 말미에 오도록 보장, (e) 실행 권한(`+x`) 부여. 평가 환경 참고 목록: `app_kiosk`, `apps`, `flutter_playwright` 3개가 `--scan` 결과에 포함됨 (머신에 따라 다를 수 있음 — 계약 검증은 로직 존재 여부 우선) [exact, enumerated]
- [ ] SC-05: 릴리스 완료 — `reflect-kit/.claude-plugin/plugin.json`의 version이 `"0.2.0"`이 되고, `.claude-plugin/marketplace.json`의 reflect-kit description이 `[v0.2.0 · 2026-04-17]` 접두사로 갱신되며, `git tag reflect-kit/v0.2.0` 생성 + origin push 완료. **정적 검증**: `git tag -l reflect-kit/v0.2.0` 로컬 확인 + `reflect-kit/.claude-plugin/plugin.json` version 필드 직접 읽기. **런타임 검증** (네트워크 필요): `git ls-remote origin 'refs/tags/reflect-kit/v0.2.0'` 로 원격 반영 확인 (네트워크 미연결 환경에서는 로컬 검증만 요구하고 원격 확인은 DEFERRED 처리 가능) [exact, enumerated]

## Error
- [ ] ER-01: codex 실패 + Claude fallback 실패 **둘 다** 발생하면, `.errors.log`에 2개 태그가 순서대로 append된다 — 먼저 `fail:codex-exit-<N>` 또는 `fail:codex-empty-output`, 그 다음 `fallback:claude-exit-<M>` 또는 `fallback:claude-empty-output`. 한 쪽 태그만 기록되고 다른 쪽이 누락되면 FAIL [exact, enumerated]
- [ ] ER-02: Claude CLI가 설치되어 있지 않은 환경에서 codex도 실패한 경우, `.errors.log`에 `skip:fallback-unavailable` 태그가 정확히 1회 기록되고 훅은 exit 0으로 종료한다 [exact]
- [ ] ER-03: Given `/reflect-digest project=all` 실행 중 일부 프로젝트 로그 파일이 읽기 실패하거나 YAML 파싱 실패, When 해당 프로젝트만 skip 처리, Then 리포트 말미에 "집계 실패 프로젝트: N개 (project_id 리스트)" 블록이 표시되어야 하며 digest 자체는 정상 종료한다 [goal]

## Architecture
- [ ] AR-01: `reflect-kit/scripts/` 디렉토리가 신규 생성되고, 그 안의 `install-scheduler.sh` 파일이 `ls -l` 결과 실행 권한(`x`) 을 가진다 [exact]
- [ ] AR-02: `log-reflection.sh` fallback 로직 추가 이후에도 기존 백그라운드 wrapper 구조가 유지된다 — (a) `$1 == "--background"` 분기 로직 존재, (b) fast path에서 `nohup ... &` + `disown` + 즉시 `exit 0`, (c) fallback 호출은 백그라운드 진입점 내부에서만 수행 (fast path 지연 없음) [structural, enumerated]
- [ ] AR-03: `reflect-kit/README.md`에 "## 스케줄러" 또는 "## Scheduling" 섹션이 추가되며, (a) `/schedule` 슬래시 명령 예시, (b) crontab 직접 등록 예시, (c) `scripts/install-scheduler.sh` 사용법 3가지가 모두 언급된다 [structural, enumerated]

## Anti-patterns
- [ ] AP-01: 버전을 하드코딩하지 않는다 — README/docs 내 버전 언급은 plugin.json v0.2.0과 일치
- [ ] AP-03: bare code fence 금지 — 모든 SKILL.md/README/scripts 주석 내 fence는 언어 힌트 포함 (```bash, ```yaml, ```text 등)
- [ ] AP-04: SKILL.md frontmatter name 필드 누락 금지

## Reusability
- [ ] RE-01: Claude CLI fallback 호출 로직을 log-reflection.sh 내부에 인라인 구현하지 않고, 훅 내부 함수(예: `try_claude_fallback()`)로 추출하여 재테스트·재사용 가능하게 한다
- [ ] RE-02: 기존 _lib-redact.sh의 11종 시크릿 패턴을 재작성하지 않고 **추가만** 한다 — regression 방지

## Diagnostics
- [ ] DG-01: `bash -n reflect-kit/hooks/*.sh reflect-kit/scripts/*.sh` 워닝 0개 + 해당 파일 전체 실행 권한(`+x`) 확인
- [ ] DG-02: IDE diagnostics 워닝/인포 0개 (신규 생성/수정 파일 대상, 스펠체크 제외)
- [ ] DG-03: `python3 scripts/validate-plugin.py reflect-kit` 전 카테고리 PASS (V1~V7)
- [ ] DG-04: 수동 fallback 시뮬레이션 — codex 한도 도달 상황(exit 1)을 인위적 재현해 reflections-*.md에 Claude 생성 YAML 블록이 append되고 `.errors.log`에 `fallback:claude-used` 엔트리가 기록됨을 확인 (목표 달성 검증) [goal]
