---
feature: "bambu-kit 누락 항목 풀세트 보강 (README + 카이젠 스킬 2종 + CLAUDE.md + docs-site 5페이지 + index.html)"
created: "2026-05-16 01:15"
complexity: "복잡"
conditions: 16
branch: "feat/bambu-kit-supplements"
scope_note: "bambu-kit는 도구형 1스킬 킷이라 reviewer 에이전트/audit 스킬은 적용 외 (rust-kit/react-kit 같은 다종 스킬 패턴 비적용). plugin.json 버전은 v0.1.0 유지(이전 세션 7742bb6에서 marketplace 등록 완료)이라 release.sh 트리거 X."
---

## Skill

- [ ] SK-01: 신규 카이젠 스킬 2종(`.claude/skills/bambu-research/SKILL.md`, `.claude/skills/bambu-kaizen/SKILL.md`) 모두 frontmatter에 `name`, `description`, `argument-hint`, `user-invocable` 필드 존재 [exact, enumerated] (측정: `rg "^name:|^description:|^argument-hint:|^user-invocable:" .claude/skills/bambu-research/SKILL.md .claude/skills/bambu-kaizen/SKILL.md | wc -l == 8`)
- [ ] SK-02: bambu-kit 트리거 키워드 3 스킬(bambu-print-profile, bambu-research, bambu-kaizen) 간 (a) set intersection 공집합 (b) 키워드 쌍 substring containment 0건 [exact, enumerated] (측정: 14개 키워드 enumerate 후 Python/bash로 set intersection + substring pair 0건 확인 — 위에서 수동 검증 완료)
- [ ] SK-03: 두 신규 카이젠 스킬 모두 `# Gotchas`, `# Process`, `# References` 3개 섹션 모두 존재 [structural, enumerated] (측정: `grep -c "^# Gotchas\|^# Process\|^# References" .claude/skills/bambu-research/SKILL.md` ≥ 3 그리고 동일하게 bambu-kaizen)
- [ ] SK-04: `bambu-kit/skills/bambu-print-profile/SKILL.md` 본문에서 옛 절대경로 `~/.claude/skills/bambu-print-profile`가 0건 (모두 `bambu-kit/skills/bambu-print-profile` 또는 plugin cache 경로로 갱신됨) [exact] (측정: `grep -c "~/.claude/skills/bambu-print-profile" bambu-kit/skills/bambu-print-profile/SKILL.md == 0`)

## Script

- [ ] SC-00: N/A — 이번 작업은 release.sh / 버전 bump를 트리거하지 않으며 marketplace.json 등록은 이전 세션 커밋 7742bb6에서 완료됨. plugin.json 버전 v0.1.0 유지 (이번 PR은 보강만 하고 버전 bump 안 함).

## Error

- [ ] ER-01: bambu-research SKILL.md에 외부 소스 폴링 실패 시 fallback 체인 명시 (Cloudflare/403 → codex-rescue 위임 → 무한 retry 금지) [structural] (측정: `grep -E "Cloudflare|codex-rescue|retry" .claude/skills/bambu-research/SKILL.md` ≥ 2 매치)
- [ ] ER-02: bambu-kaizen SKILL.md에 사용자 명시 정책 보호 규칙 명시 (`nozzle_temperature` 안 건드림 + `wipe_on_loops` Bambu 부재 + silent skip 체크리스트 7항목 보존) [structural] (측정: `grep -c "nozzle_temperature\|wipe_on_loops\|silent skip" .claude/skills/bambu-kaizen/SKILL.md` ≥ 3)

## Architecture

- [ ] AR-01: bambu-kit 폴더 구조 일관성 — `bambu-kit/.claude-plugin/plugin.json`, `bambu-kit/README.md`, `bambu-kit/skills/bambu-print-profile/{SKILL.md,BACKLOG.md,references/}` 모두 존재 [exact, enumerated] (측정: `ls` 각 경로 0 exit code. `BACKLOG.md`는 V5 placeholder 회피를 위해 2026-05-16 iteration 2에서 `TODO.md`에서 git mv로 rename됨)
- [ ] AR-02: 카이젠 스킬 2종(`bambu-research`, `bambu-kaizen`)은 `.claude/skills/`에만 위치하고 `bambu-kit/` 안에 없음 (외부 사용자 노출 방지 — Gotcha 6의 정합성) [exact, enumerated] (측정: `find bambu-kit -type d \( -name 'bambu-research' -o -name 'bambu-kaizen' \) | wc -l == 0` 그리고 `ls .claude/skills/bambu-research/SKILL.md .claude/skills/bambu-kaizen/SKILL.md` 둘 다 0 exit code)
- [ ] AR-03: `docs/bambu-kit/` 5개 HTML(`bambu-print-profile.html`, `bambu-fields-baseline.html`, `materials.html`, `seam-recipes.html`, `kaizen-sources.html`) 모두 존재 + 각 ≥ 400줄 [exact, enumerated] (측정: `wc -l docs/bambu-kit/*.html` 각 ≥ 400)
- [ ] AR-04: `docs/index.html`의 categories 배열에 Bambu Kit 카테고리 + 5개 페이지 ID(`bambu-print-profile`, `bambu-fields-baseline`, `bambu-materials`, `bambu-seam-recipes`, `bambu-kaizen-sources`) 모두 등록 + getIcon() 함수에 동일 5 ID SVG 매핑 [exact, enumerated] (측정: `grep -c "id: 'bambu-" docs/index.html == 5` 그리고 `grep -c "'bambu-.*':\s*'<svg" docs/index.html == 5`)
- [ ] AR-05: `CLAUDE.md` Skills Reference에 (a) bambu-kit 섹션 (b) `.claude/skills` 표에 `/bambu-kaizen`, `/bambu-research` 행 모두 존재 [exact, enumerated] (측정: `grep -c "bambu-kit" CLAUDE.md` ≥ 3 그리고 `grep "/bambu-kaizen\|/bambu-research" CLAUDE.md` 각 ≥ 1)
- [ ] AR-06: `docs/bambu-kit/` 5 HTML 모두 (a) standalone (외부 CSS/JS/font CDN 로드 0건, anchor href 본문 인용은 OK) (b) `--accent:#14B8A6` 토큰 일관 적용 [exact, enumerated] (측정: `grep -lE "<link[^>]+href=[\"']https?://" docs/bambu-kit/*.html | wc -l == 0` 그리고 `grep -lE "<script[^>]+src=[\"']https?://" docs/bambu-kit/*.html | wc -l == 0`; `grep -L "\-\-accent:#14B8A6" docs/bambu-kit/*.html | wc -l == 0`)

## Anti-patterns

- [ ] AP-03: bambu-kit 플러그인 V6(code-fence) 게이트 PASS — 여는 fence에 언어 힌트 누락 0건. 닫는 fence(``` 단독)는 markdown 표준상 정상이므로 V6는 페어링 추적으로 제외함 (validate-plugin.py V6 로직 기준). `.claude/skills/bambu-{research,kaizen}/SKILL.md`는 validate-plugin.py 검사 범위 외(.claude/skills/는 plugin 외부)이지만 good-practice 차원에서 동일하게 모든 여는 fence에 hint 추가 [exact, enumerated] (측정: (1) `python3 scripts/validate-plugin.py bambu-kit --check=code-fence` exit 0 (2) `.claude/skills/bambu-research/SKILL.md`와 `.claude/skills/bambu-kaizen/SKILL.md`의 모든 fence pair에서 여는 라인이 ` ```text ` 등 hint 포함 — Python 스크립트로 페어링 검증)
- [ ] AP-04: 신규 SKILL.md 2종 모두 frontmatter에 `name` 필드 존재 — validate-plugin V1 PASS [exact, enumerated] (측정: SK-01과 부분 중복이지만 별도 lint 게이트, `head -10 .claude/skills/bambu-research/SKILL.md | grep -c "^name:" == 1` 그리고 동일하게 bambu-kaizen)

## Reusability

- [ ] RE-01: 두 신규 카이젠 스킬은 다른 카이젠 스킬에서 재사용 가능한 패턴(rust-research/rust-kaizen 골격)을 따랐다 — Gotchas/Process/References 섹션 동일 구조 [structural] (측정: 섹션 헤더 비교 — `grep "^# " .claude/skills/{rust-kaizen,bambu-kaizen}/SKILL.md`가 동일 prefix 셋 보유)
- [ ] RE-02: 기존 docs-site 페이지 패턴(rust-kit/react-kit) + page-template.html을 재사용 — 5 HTML이 동일한 base CSS 토큰(`--bg`/`--surface`/`--text`)을 공유하고 accent만 plugin별로 분리 [structural] (측정: `grep -L "\-\-bg:#0d0d14" docs/bambu-kit/*.html | wc -l == 0`)

## Diagnostics

- [ ] DG-01: `bash -n scripts/release.sh` 워닝 0개 — 이번 작업이 .sh 변경 0건이라 회귀 없음 (측정: `bash -n scripts/release.sh` exit 0)
- [ ] DG-02: IDE diagnostics 워닝 — 이번 추가/수정 행에서 새로 발생한 워닝 0개. 예외: (a) cSpell "Unknown word" (bambu/Bambu/kaizen 등) — CLAUDE.md 명시 규칙대로 무시 (b) MD036/MD060/MD031 — 이번 추가 전부터 다른 모든 kit 섹션에 동일 패턴 존재하는 기존 워닝, 본 작업 범위 밖 (측정: 사용자 IDE 패널에서 본 작업 범위 신규 워닝 0건 확인)
- [ ] DG-03: N/A — release.sh 실행 트리거 X. (이번 작업은 plugin.json 버전 변경 안 함)
- [ ] DG-04: docs site 정적 검증 — 5 HTML 모두 `<!DOCTYPE html>` 시작 + `</html>` 종료 + iframe 로드 시 정상 표시 가능 [structural, enumerated] (측정: `head -1 docs/bambu-kit/*.html` 모두 `<!DOCTYPE html>`로 시작; `tail -1 docs/bambu-kit/*.html` 모두 `</html>` 또는 직전 빈 줄)
