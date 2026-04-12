---
feature: "카이젠 자동화 gap 10개 일괄 구현"
created: "2026-04-12 01:00"
complexity: "복잡"
conditions: 30
---

# Sprint Contract — Automation Gap 10 Implementation

## Context

이전 스프린트 (post-missing-items, APPROVE 35/35 iter2) 완료 후 자동화 성숙도 리포트 (`.harness/.meta/automation-maturity-2026-04-12.md`) 가 66% (23/35) 로 평가되었다. 남은 34% 의 core 결핍 10 개를 일괄 구현하여 85%+ 수준으로 승격한다.

사용자는 명시적으로 "10 개 전부 무한 루프 QA 돌려서 APPROVE 날 때까지 알아서 수정" 을 지시했다.

## 영향 범위

**신규 생성:**

- `scripts/validate-post-kaizen.py` (Gap 2)
- `scripts/spawn-kaizen-phase.sh` (Gap 3)
- `scripts/append-audit-log.py` (Gap 4)
- `.claude/skills/meta-kaizen/SKILL.md` (Gap 5)
- `scripts/detect-docs-drift.py` (Gap 6)
- `.claude/skills/kaizen-orchestrator/references/phase-research-templates.md` (Gap 7)
- `scripts/finalize-phase.sh` (Gap 8)
- `scripts/fix-markdown-lint.py` (Gap 9)
- `scripts/sync-evals.py` (Gap 10)

**수정:**

- `.claude/skills/kaizen-orchestrator/SKILL.md` — Gap 1 (cron 등록 지시), Gap 5 (meta-kaizen 참조), Gap 7 (research-template 참조), Gap 8 (finalize-phase 참조)

**수정 금지:**

- 플러그인 스킬 (`harness/skills/`, `flutter-toolkit/skills/`, `design-kit/skills/`, `backend-kit/skills/`, `infra-kit/skills/`, `rust-kit/skills/`, `react-kit/skills/`)
- 플러그인 agents / references
- 모든 `plugin.json`, `.claude-plugin/marketplace.json`
- `.harness/project.yaml`

## 완료 조건

### G1 — cron 등록 + 문서화

- [ ] G1-01 [structural]: `.claude/skills/kaizen-orchestrator/SKILL.md` 의 트리거 섹션에 `/schedule` 스킬로 실제 등록하는 구체 명령 예시 추가. 명령 예시는 `schedule create` 형식이고 cron 표현식 `"0 0 * * 1"` (매주 월요일 00:00 UTC ≈ 09:00 KST) 포함.
- [ ] G1-02 [structural]: `.claude/skills/kaizen-orchestrator/SKILL.md` 의 트리거 섹션에 "cron 등록 상태 확인 방법" 서브섹션 추가 (`/schedule list` 같은 명령).

### G2 — validate-post-kaizen.py

- [ ] G2-01 [exact]: `scripts/validate-post-kaizen.py` 신규 파일 존재. Python 3 실행 가능.
- [ ] G2-02 [structural]: 12 개 이상의 체크 함수 구현 (plugin-json-bump, marketplace-sync, sync-docs, validate-plugin, changelog-entry, per-kit-research-log-entries, docs-site-regen, evals-audit, failure-count, cleanup-log, scope-isolation, bare-fence).
- [ ] G2-03 [exact]: `--since <ref>` 인자로 "이 ref 이후의 변경" 기준 검증 지원 (기본값 `main`).
- [ ] G2-04 [exact]: 모든 체크 PASS 시 exit 0, 하나라도 FAIL 시 exit 1, 구조적 에러 시 exit 2.
- [ ] G2-05 [exact]: 실행 결과 출력 형식 — 각 체크 한 줄씩 `[ PASS | FAIL | SKIP ] check-name: summary`. 요약 끝에 `Total: N PASS / M FAIL / K SKIP`.
- [ ] G2-06 [exact]: `python3 scripts/validate-post-kaizen.py --help` 정상 출력.

### G3 — spawn-kaizen-phase.sh

- [ ] G3-01 [exact]: `scripts/spawn-kaizen-phase.sh` 신규 파일, 실행 권한 (`chmod +x`).
- [ ] G3-02 [structural]: 인자 `<phase-num>` 받아 (1-10) 해당 Phase 의 `git tag kaizen-phase-{N}-pre` 생성 + `.harness/.meta/kaizen-data-pool.md` 의 §N 섹션 stdout 출력 + subagent prompt 템플릿 출력.
- [ ] G3-03 [exact]: `--help` 옵션으로 사용법 출력. 인자 없으면 `exit 1` + 사용법.
- [ ] G3-04 [exact]: bash syntax 유효 (`bash -n scripts/spawn-kaizen-phase.sh` 통과).

### G4 — append-audit-log.py

- [ ] G4-01 [exact]: `scripts/append-audit-log.py` 신규 파일 존재.
- [ ] G4-02 [structural]: 인자로 `--cycle-id <id>`, `--failures <file>`, `--manual-edits <file>` 옵션 받기. 또는 positional 로 JSON 입력 받기. `.harness/.meta/orchestrator-audit-log.md` 에 새 엔트리 append.
- [ ] G4-03 [exact]: append-only — 기존 내용 절대 삭제/수정 안 함.
- [ ] G4-04 [exact]: Python syntax 유효 (`python3 -c "import scripts.append_audit_log"` 또는 `python3 scripts/append-audit-log.py --help` 정상 출력).

### G5 — meta-kaizen 스킬

- [ ] G5-01 [exact]: `.claude/skills/meta-kaizen/SKILL.md` 신규 파일 존재.
- [ ] G5-02 [structural]: frontmatter `name: meta-kaizen`, `description:` 필드 포함. description 에 "orchestrator", "meta", "kaizen" 키워드 포함.
- [ ] G5-03 [structural]: 본문에 Process 섹션 — 이전 사이클 audit-log 읽기 → 리서치 (arxiv / Anthropic 공식 / 학술) → orchestrator SKILL.md DRAFT 개선 → qa-evaluator 평가 → APPROVE 시 적용.
- [ ] G5-04 [structural]: Gotchas 섹션에 "AUTO:plugin_phases 마커 영역 직접 편집 금지" + "Phase 1~10 범위 밖, orchestrator SKILL.md 만 개선 대상" 명시.
- [ ] G5-05 [exact]: bare code fence 0 건.

### G6 — detect-docs-drift.py

- [ ] G6-01 [exact]: `scripts/detect-docs-drift.py` 신규 파일 존재.
- [ ] G6-02 [structural]: `--since <ref>` 인자로 해당 ref 이후 변경된 `.md` / `.yaml` 소스 파일 목록 → 대응 `docs/<plugin>/*.html` 경로 매핑 → stdout 에 한 줄씩 출력 (`<source> → <html-target>` 형식).
- [ ] G6-03 [structural]: 매핑 규칙 — `harness/docs/guides/*.md` → `docs/harness/*.html`, `harness/references/*.yaml` → `docs/harness/*.html`, `docs/backend/*.md` → `docs/backend-kit/*.html`, `docs/infra/*.md` → `docs/infra-kit/*.html`, `docs/rust/*.md` → `docs/rust-kit/*.html`, `docs/react/*.md` → `docs/react-kit/*.html`, `flutter-toolkit/references/*.md` → `docs/flutter-toolkit/*.html`, `design-kit/docs/design/*.md` → `docs/design-kit/*.html`.
- [ ] G6-04 [exact]: `--json` 플래그 지원 — JSON array 형식으로도 출력 가능.
- [ ] G6-05 [exact]: Python syntax 유효.

### G7 — Phase research-template

- [ ] G7-01 [exact]: `.claude/skills/kaizen-orchestrator/references/phase-research-templates.md` 신규 파일 존재.
- [ ] G7-02 [structural]: Phase 1~10 10 개 Phase 각각 "필수 리서치 소스 3 건 이상" 섹션 포함. 각 소스는 (1) URL 또는 MCP 참조 (2) 조회 이유 (3) fallback 경로 (Context7 quota 소진 시 대체).
- [ ] G7-03 [structural]: 테이블 또는 리스트 형식으로 Phase 별 섹션이 명확히 구분됨.
- [ ] G7-04 [exact]: `.claude/skills/kaizen-orchestrator/SKILL.md` 본문에서 이 파일을 `references/phase-research-templates.md` 로 참조하는 링크/mention 1 건 이상.

### G8 — finalize-phase.sh

- [ ] G8-01 [exact]: `scripts/finalize-phase.sh` 신규 파일, 실행 권한.
- [ ] G8-02 [structural]: 인자 `<phase-num> <result>` (result 는 `pass` / `fail`) 받기. `pass` 시 `.harness/.meta/kaizen-failure-count.yaml` 의 `phase_N` 0 으로 리셋. `fail` 시 `phase_N` +1 및 2 이상이면 경고 출력.
- [ ] G8-03 [structural]: `fail` + auto-revert 플래그 (`--revert`) 시 `git revert kaizen-phase-N-pre..HEAD` 실행하거나 최소한 revert 명령을 stdout 에 출력.
- [ ] G8-04 [exact]: bash syntax 유효.

### G9 — fix-markdown-lint.py

- [ ] G9-01 [exact]: `scripts/fix-markdown-lint.py` 신규 파일 존재.
- [ ] G9-02 [structural]: 최소 4 개 규칙 처리 — MD031 (fence blank lines), MD032 (list blank lines), MD034 (bare URL → autolink), MD060 (table separator spacing).
- [ ] G9-03 [exact]: 인자 `<path>` (파일 또는 디렉토리) 받기. 디렉토리면 재귀 처리. `--dry-run` 플래그로 변경 미리보기.
- [ ] G9-04 [exact]: Python syntax 유효.
- [ ] G9-05 [exact]: `--help` 정상 출력.

### G10 — sync-evals.py

- [ ] G10-01 [exact]: `scripts/sync-evals.py` 신규 파일 존재.
- [ ] G10-02 [structural]: 각 플러그인 (`flutter-toolkit`, `rust-kit`, `react-kit`, `design-kit`) 의 `evals/evals.json` 과 `skills/` 디렉토리를 비교해 missing / orphan 찾기.
- [ ] G10-03 [exact]: `--check-only` 모드 지원 — drift 있으면 exit 1, 없으면 exit 0. 기본 모드는 스켈레톤 엔트리 자동 추가 (orphan 제거는 수동 확인 필요하므로 보고만).
- [ ] G10-04 [exact]: Python syntax 유효.

### I — Integration / Hygiene

- [ ] I-01 [exact]: `python3 scripts/validate-plugin.py` Total 7 plugins, 7 OK, Exit 0.
- [ ] I-02 [exact]: `python3 scripts/sync-docs.py --check-only` 모든 README 동기화.
- [ ] I-03 [exact]: `python3 scripts/sync-orchestrator.py --check-only` exit 0 (drift 없음).
- [ ] I-04 [exact]: **신규 스크립트 전부 실행 가능 검증** — `python3 scripts/validate-post-kaizen.py --help` / `bash scripts/spawn-kaizen-phase.sh --help` / `python3 scripts/append-audit-log.py --help` / `python3 scripts/detect-docs-drift.py --help` / `bash scripts/finalize-phase.sh --help` / `python3 scripts/fix-markdown-lint.py --help` / `python3 scripts/sync-evals.py --help` 전부 exit 0.
- [ ] I-05 [exact]: 수정 금지 파일 (플러그인 skills/agents/references, plugin.json, marketplace.json, project.yaml) 중 diff 에 등장하지 않음.
- [ ] I-06 [exact]: 전 변경 파일 bare fenced code block 0 건.
- [ ] I-07 [exact]: commit prefix `kaizen(automation):` 또는 `feat(scripts):`, push 완료 후 기존 PR #6 에 반영.

## Anti-patterns

- [ ] AP-03: bare code fence 금지
- [ ] AP-04: frontmatter name 필드 누락 금지

## Reusability

- [ ] RE-01: 다른 곳에서도 사용 가능한 컴포넌트를 private 으로 만들지 않았다
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다

## Diagnostics

- [ ] DG-01: `bash -n scripts/release.sh` 워닝 0 개
- [ ] DG-02: IDE diagnostics 워닝/인포 0 개 (스펠체크 제외)
- [ ] DG-03: 콘솔 에러/예외 0 개
- [ ] DG-04: 해당 없음

## Self-audit

1. 각 Gap 의 스크립트/파일 실제 생성 확인 + `--help` exit 0
2. `python3 scripts/validate-plugin.py` + `sync-docs` + `sync-orchestrator` drift 0
3. git diff 로 수정 금지 파일 미포함 확인
4. 독립 qa-evaluator 스폰하여 L3 평가
5. REJECT 시 수정 + 재평가 (최대 5 iter — APPROVE 날 때까지)
