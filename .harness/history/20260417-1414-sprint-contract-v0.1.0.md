---
feature: "reflect-kit 플러그인 신설 v0.1.0 — 글로벌 dialog-feedback 시스템의 플러그인화"
created: "2026-04-17 10:42"
complexity: "복잡"
conditions: 23
---

## Skill
- [ ] SK-01: `reflect-kit/skills/` 하위에 3개 스킬 폴더가 존재하며 각각 `SKILL.md` 파일을 가진다 — `reflect-digest/`, `reflect-promote/`, `reflect-kaizen/` [exact, enumerated]
- [ ] SK-02: 3개 SKILL.md 모두 valid YAML frontmatter를 가지며 `name`, `description`, `argument-hint`, `user-invocable` 필드가 존재한다 [exact, enumerated]
- [ ] SK-03: `reflect-digest/SKILL.md`의 description과 본문에서 기존 `dialog-feedback-digest`, `misunderstandings-*.md`, `dialog-feedback-promote` 참조가 모두 신규 이름(`reflect-digest`, `reflections-*.md`, `reflect-promote`)으로 대체되어 있다 — 해당 문자열 0회 매치 [exact, collective]
- [ ] SK-04: `reflect-promote/SKILL.md`는 다음 프로세스 섹션을 포함한다 — 후보 입력 수신, DESIGN.md Precedence Table 기반 surface 판정, 실제 파일 수정(CLAUDE.md/memory/skill/hook/.claude/rules), `uuidgen` 기반 rule_id 발급(ULID 라이브러리 의존성 회피), `promotions-ledger.md` append, rollback 절차 [structural, enumerated]
- [ ] SK-05: `reflect-kaizen/SKILL.md`는 다음 4개 프로세스 섹션을 모두 포함하며 각 섹션은 최소 3개 단계(- 또는 숫자 bullet)를 가진다 — (1) 최근 reflections 랜덤 10건 LLM-as-judge 재분류, (2) 원 분류 vs 재분류 일치도 측정 + 70% 미만 시 프롬프트 개선 트리거, (3) `promotions-ledger.md`의 `post_freq` 30일 calibration, (4) 임계값/프롬프트 개선 제안 [structural, enumerated]
- [ ] SK-06: 3개 스킬 모두 본문에 `Gotchas` 섹션과 `Process` 섹션을 포함하며, Gotchas는 최소 3개 이상 항목을 가진다 [structural, enumerated]
- [ ] SK-07: `docs/reflect-kit/` 하위에 `design.html`, `research.html`, `schema.html` 3개 standalone HTML 페이지가 존재하며, 각 페이지 `:root`의 `--accent` 값은 `#F43F5E`, `--accent2`는 `#FDA4AF`, `--accent-dim`은 `rgba(244,63,94,0.12)`로 설정된다. 외부 CDN/CSS/JS 링크 0개 [exact, enumerated]

## Script
- [ ] SC-01: `reflect-kit/.claude-plugin/plugin.json`이 존재하며 `name: "reflect-kit"`, `version: "0.1.0"`, `author`, `description`, `repository`, `license`, `keywords` 필드를 가진다 [exact, enumerated]
- [ ] SC-02: `reflect-kit/hooks/hooks.json`이 존재하며 `UserPromptSubmit` / `PostToolUseFailure` / `Stop` 3개 이벤트 핸들러를 가진다. 각 command는 `${CLAUDE_PLUGIN_ROOT}/hooks/{log-prompt|log-tool-failure|log-reflection}.sh` 형태다 — `${PLUGIN_DIR}` 문자열 0회 매치 [exact, enumerated]
- [ ] SC-03: `log-reflection.sh`는 내부에서 codex 분석을 백그라운드(`nohup ... & disown` 또는 동등)로 실행하고 훅 본체는 즉시 `exit 0` 반환한다 — 훅 command 자체에 `async: true` 필드 없음 [exact, collective]
- [ ] SC-04: `.claude-plugin/marketplace.json`의 `plugins` 배열에 `reflect-kit` 엔트리가 추가되며 `name`, `source: "./reflect-kit"`, `description` 필드를 가진다 [exact, enumerated]
- [ ] SC-05: v0.1.0 수동 릴리스가 완료된다 — git commit (신규 파일 포함), `git tag reflect-kit/v0.1.0` 생성, `git push origin main` + `git push origin reflect-kit/v0.1.0` 실행. `scripts/release.sh`는 0.1.0 최초 태그에 사용하지 않는다 [goal]

## Error
- [ ] ER-01: `log-prompt.sh` / `log-tool-failure.sh` / `log-reflection.sh` 3개 훅 모두 redaction을 적용한다 — `_lib-redact.sh`의 `redact_sensitive()` 함수가 각 훅에서 source + 호출된다 [exact, enumerated]
- [ ] ER-02: `log-reflection.sh`는 실패 시 `.errors.log`에 `skip:cli-missing | skip:transcript-path-empty | skip:transcript-file-missing | skip:transcript-too-short | skip:transcript-empty-after-tail | fail:codex-exit-<N> | fail:codex-empty-output` 중 하나의 태그로 사유를 기록한다 [exact, enumerated]
- [ ] ER-03: 글로벌 정리(C 단계) 전에 플러그인 설치·검증(E 단계)이 완료된다 — 관찰 가능한 artifact 형태로 검증: (a) 플러그인 설치 시점의 `~/.claude/logs/<project_id>/YYYY-MM.md` line count 기준값을 측정하고, (b) 테스트 프롬프트 1개 제출 + 의도적 실패 bash 1건 실행 후 `wc -l` 결과가 최소 +2줄 이상 증가했음을 보고한다. 또한 (c) `reflections-YYYY-MM.md` 또는 `.errors.log` 중 하나에 세션 종료 후 신규 엔트리가 추가되었음을 확인한다 [goal]
- [ ] ER-04: 데이터 마이그레이션(D 단계)은 기존 `misunderstandings-*.md` 파일을 `reflections-*.md`로 rename한 뒤 rename 스크립트 실행 결과가 "0 files not renamed"를 보장한다 — 기존 파일 1개 이상이었다면 rename 후 동명이 존재해야 함 [goal]

## Architecture
- [ ] AR-01: `reflect-kit/` 디렉토리 구조가 기존 kit 컨벤션을 따른다 — `.claude-plugin/plugin.json`, `hooks/`, `skills/<name>/SKILL.md`, `docs/`, `README.md` [exact, enumerated]
- [ ] AR-02: 훅 스크립트들(`log-prompt.sh`, `log-tool-failure.sh`, `log-reflection.sh`, `_lib-project-id.sh`, `_lib-redact.sh`)의 상대 경로 해결이 `BASH_SOURCE[0]` 기반 `SCRIPT_DIR` 계산으로 되어 있으며, 플러그인 경로(`${CLAUDE_PLUGIN_ROOT}`)에서도 동작한다 [exact, collective]
- [ ] AR-03: `reflect-kit/docs/` 에 `DESIGN.md`, `RESEARCH.md`, `SCHEMA.md` 3개 문서가 존재한다. `DESIGN.md`와 `RESEARCH.md`는 `~/.claude/plans/reflect-kit/`의 동명 파일을 복사·참조한 것이며, `SCHEMA.md`는 `DESIGN.md`에서 YAML 스키마 + Ledger 스키마 부분만 추출한 별도 문서다 [exact, enumerated]
- [ ] AR-04: `reflect-kit/README.md`는 `~/.claude/plans/reflect-kit/README.md`의 구성을 따르며, 설치 방법 + 훅 이벤트 + 스킬 3종 + 로그 경로 + 의존성 섹션을 모두 포함한다 [structural, collective]
- [ ] AR-05: 플러그인 신설이 `scripts/sync-docs.py reflect-kit` 실행 시 에러 없이 완료되며, `reflect-kit/README.md`의 `<!-- AUTO:xxx -->` 마커 사이가 plugin.json/SKILL.md frontmatter에서 자동 생성된 값으로 채워진다 [goal]
- [ ] AR-06: `docs/index.html`의 categories 배열에 reflect-kit 3개 페이지 항목(`{id, title, file}` 3필드)이 모두 등록되며, `getIcon()` 함수에 reflect-kit 3개 페이지의 `id` 키에 대응하는 SVG 아이콘 case가 추가된다 [exact, enumerated]
- [ ] AR-07: `CLAUDE.md`의 "Skills Reference" 섹션에 reflect-kit 블록이 추가되며, 스킬 3개(`/reflect-digest`, `/reflect-promote`, `/reflect-kaizen`) 각 행이 테이블에 포함된다. 또한 Repository Overview 섹션의 플러그인 목록에 reflect-kit 1줄 설명이 추가된다 [structural, enumerated]

## Anti-patterns
- [ ] AP-01: 버전을 하드코딩하지 않는다 — README / docs 내 버전 언급은 plugin.json의 버전값과 일치해야 한다
- [ ] AP-02: (의도적 공백 — `git push --force` 방지 규칙은 이 기능의 관련성 낮음, 커밋/푸시 시점에 작업자가 준수)
- [ ] AP-03: bare code fence 금지 — 모든 3개 SKILL.md / README.md / docs 내 fenced code block은 언어 힌트를 가진다 (```bash, ```yaml, ```json, ```text, ```markdown 등)
- [ ] AP-04: SKILL.md / agents/*.md frontmatter에서 name 필드 누락 금지 — 3개 SKILL.md 모두 name 필드 존재

## Reusability
- [ ] RE-01: 다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다 — `_lib-project-id.sh`, `_lib-redact.sh`는 hooks/ 최상위에 배치되며 세 훅 스크립트에서 공통 source된다
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다 — 글로벌 `~/.claude/hooks/` 및 `~/.claude/skills/dialog-feedback-digest/`의 기존 스크립트·SKILL을 처음부터 재작성하지 않고 복사·rename·필드 수정으로 이식한다

## Diagnostics
- [ ] DG-01: `bash -n reflect-kit/hooks/*.sh` 워닝 0개 (신규 hooks 파일 5개 전체 bash 문법 체크) + `ls -l reflect-kit/hooks/*.sh` 결과 5개 모두 실행 권한(`x`) 부여되어 있다 (`chmod +x` 누락 방지)
- [ ] DG-02: IDE diagnostics 워닝/인포 0개 (신규 생성 파일 대상, 스펠체크 제외)
- [ ] DG-03: `python3 scripts/validate-plugin.py reflect-kit` 실행 결과 전 카테고리 PASS (스킬 frontmatter, 코드펜스, 레퍼런스 무결성 포함)
- [ ] DG-04: Claude Code 재시작 후 `/reflect-digest` 호출 시 에러 0건, 출력 생성됨 (E 단계 검증)
