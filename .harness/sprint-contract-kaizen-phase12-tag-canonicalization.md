---
feature: "카이젠 Phase 12 — reflect-kit 태그 정규화 결정론화(K1) + hook coverage audit 라우팅(K2) + 파편화 게이트로 calibration 무효화(K3)"
created: "2026-08-13 15:20"
complexity: "복잡"
conditions: 29
slug: kaizen-phase12-tag-canonicalization
status: active
owner_session: df1b3e15-30b3-4825-a3c4-4ac44c686e94
conditions_digest: sha256:d85f4d7e5644ea3a
locked_at: "2026-08-13 15:20"
---

## 배경

`.harness/.meta/evidence/phase12.md` 가 이번 Phase 의 **유일한 외부 근거**다. 외부 조회 0 회.

`/insights` 2026-08-13 은 "Phase 12 Reflect — 이번 리포트에 직접 신호 없음" 이라고 명시한다
(`insights-report.md:110`). 그러나 **로그 실측은 다르다.** reflect-kit 은 로그를 스스로 생산하는
유일한 킷이고, 그 로그가 킷 자신의 결함을 드러낸다. 이번 Phase 는 §0 이 아니라 **실측 데이터**가
근거다.

**2026-08-13 실측 (`~/.claude/logs/*/reflections-*.md` 전량):**

| 항목 | 값 | 의미 |
|---|---|---|
| 엔트리 / 원시 distinct 태그 / 클러스터 | 4,691 / 2,639 / 2,578 | |
| singleton 클러스터 | 2,279 (**singleton_share 0.884**) | 어휘가 거의 전부 1 회짜리 |
| `fold_ratio` | 1.02 | **기존 지표는 "정상"(<1.5) 이라고 답한다** |
| `skipped-required-api-doc-check` 원시 단독 | 71 | ledger `post_freq` 가 세는 값 |
| 같은 lemma 클러스터 합산 | **110** | 실제 재발량 — 39 건(55%)이 안 세지고 있었다 |
| `edit-before-read` / `edited-before-read` | 51 / 4 | 훅이 canonical 예시로 제시한 쪽이 **소수형** |

**세 결함 (evidence K1~K3):**

1. **K1 — canonicalization 이 LLM 부탁에 의존한다.** 훅은 raw 태그 목록을 되돌려주고 "그대로 쓰라"
   고 요청할 뿐, 형태소·동의어를 기계가 접지 않는다. 게다가 훅이 규범으로 제시한 예시
   (`edited-before-read`, 실사용 4 건)가 **최빈형(`edit-before-read`, 51 건)이 아니다** —
   규범과 실사용이 반대다.
2. **K2 — 이미 승격했는데 재발이 늘었다.** `skipped-required-api-doc-check` 는 직전 9 건 → 이번
   30 건 이상. 사용자는 이미 PreToolUse 훅을 등록해 뒀다. 문구 문제가 아니라 게이트 미작동
   가설이 1 순위인데, 현재 promote 스킬에는 그 분기가 없어 무조건 "등급 상향" 으로 흐른다.
3. **K3 — 파편화 지표가 파편화를 못 잡는다.** `fold_ratio = 원시/클러스터` 는 클러스터링이
   아무것도 못 묶으면 1.00 이 되어 항상 "정상" 이다. 그 결과 과소집계된 `post_freq == 0` 이
   "효과 있음" 으로 읽히고 실패한 규칙이 살아남는다.

**이번 사이클 하드 프레이밍 준수:** 같은 취지의 규칙 문장을 추가하지 않는다. K1 은 **문장 →
결정론적 pass(E3)** 로, K3 은 **서술 경고 → 산출 금지(E2→E3)** 로 **등급을 올린다.**

## 리서치 소스

- `.harness/.meta/evidence/phase12.md` (유일 외부 근거)
- Reflexion episodic memory: https://arxiv.org/abs/2303.11366
- Alertmanager `group_by` — 집계 키가 신호 품질을 결정: https://prometheus.io/docs/alerting/latest/configuration/
- Claude Code hooks — PreToolUse/PostToolUse 실행 시점 · exit 2 · timeout: https://code.claude.com/docs/en/hooks
- 닫힌 라벨 집합의 위험 (agreement ≠ validity): https://aclanthology.org/J08-4004/
- alert fatigue: https://pubmed.ncbi.nlm.nih.gov/24153215/
- Sentry fingerprint matcher (glob 기반): https://github.com/getsentry/sentry/issues/75567

## GAP 분석

| # | 현재 | 갭 | 조치 |
|---|---|---|---|
| G1 | 훅이 raw 태그 목록을 주입 | 형태소·동의어가 안 접힘 | 결정론적 pass + `canonical → aliases` 주입 |
| G2 | canonical 예시가 `edited-before-read` | 최빈형이 아님 (4 vs 51) | 기본형으로 정정 + 규칙 3 을 동사원형으로 |
| G3 | 정규화 규약이 어디에도 없음 | 4 표면이 제각각 판단 | `references/` 에 SSOT + 실행 라이브러리 |
| G4 | `stale` 계열 병합 판단 근거 없음 | 과잉 병합 위험 | family 규약 (합산 금지) |
| G5 | 닫힌 어휘 강제 위험 | label collapse | `new_tag_reason` (open vocabulary) |
| G6 | promote 가 재발을 무조건 등급 상향으로 처리 | 게이트 미작동 오진 | §B-0 `hook_coverage_audit` 9 항 |
| G7 | hook 초안에 이벤트 타입 사실 없음 | PostToolUse 예방 오해 | 사실 표 + eligibility denominator |
| G8 | `aliases` 를 사람이 고름 | 비면 post_freq 과소집계 | 클러스터 멤버 전체 강제 |
| G9 | `fold_ratio` 1.5 임계 | 탐지 불가 | `singleton_share` 로 교체 |
| G10 | 파편화 초과 시 "명시" 만 | demotion 이 그대로 나감 | 산출 금지 (E3) |

## 범위 경계

- **Scope**: `reflect-kit/skills/*/SKILL.md` · `reflect-kit/hooks/*.sh` · `reflect-kit/references/`
- **Scope 밖 (수정 금지)**: `reflect-kit/docs/*` · `reflect-kit/README.md` · `reflect-kit/hooks/hooks.json` ·
  `reflect-kit/scripts/*` · `reflect-kit/.claude-plugin/*` · `~/.claude/logs/**` (읽기 전용) ·
  사용자 전역 훅 설정(`~/.claude/settings.json`, `~/.claude/hooks/`)
- `codex-kaizen` SKILL.md 는 읽었으나 K1~K3 와 무관 — 변경하지 않는다.
- Diff-Scope baseline (계약 작성 시점 실행): `git status --porcelain -- reflect-kit/` →
  `M reflect-kit/hooks/log-reflection.sh` / `M reflect-kit/skills/reflect-digest/SKILL.md` /
  `M reflect-kit/skills/reflect-kaizen/SKILL.md` / `M reflect-kit/skills/reflect-promote/SKILL.md` /
  `?? reflect-kit/hooks/_lib-tag-canon.sh` / `?? reflect-kit/references/`

## 회귀 게이트

- 훅의 3 경로(정상 / lemma map 부재 / 빈 로그 디렉토리)를 실제로 실행해 출력으로 확인한다.
- 정규화 라이브러리는 bash · zsh · sh 세 셸에서 같은 출력을 내야 한다 (zsh `nomatch` 전례).
- 열거값(클러스터 수 · 조건 수)은 타이핑하지 않고 명령으로 계산한다.

## Skill

- [ ] SK-01: 정규화 SSOT `references/tag-canonicalization.md` 가 `reflect-digest`, `reflect-promote`,
      `reflect-kaizen` 3 개 SKILL.md 에서 각각 경로 문자열로 참조된다 [exact, enumerated]
      (측정: `grep -l 'tag-canonicalization.md' reflect-kit/skills/reflect-digest/SKILL.md
      reflect-kit/skills/reflect-promote/SKILL.md reflect-kit/skills/reflect-kaizen/SKILL.md`
      결과가 3 행)
- [ ] SK-02: `reflect-digest` 의 클러스터링 단계가 `tag_canon_groups` 실행을 1 차 근거로 지정한다 [exact]
      (측정: `grep -c 'tag_canon_groups' reflect-kit/skills/reflect-digest/SKILL.md` >= 1 이고
      해당 문맥에 `결정론적 pass` 문자열이 존재)
- [ ] SK-03: `reflect-promote` 에 `§B-0` hook coverage audit 절이 9 개 점검 항목과 함께 존재한다
      [exact, enumerated] (측정: `### B-0.` 헤더 1 개 존재 + 그 절의 표에서
      `hook installed`, `event type`, `matcher`, `path normalization`, `exit code`, `timeout`,
      `executable`, `dependency`, `fired/blocked` 9 개 토큰이 각각 1 회 이상)
- [ ] SK-04: `reflect-kaizen` 이 `calibration_confidence: low` 상태에서 `demote-candidate` 산출을
      **금지**한다 (서술 권고가 아니라 금지문) [exact]
      (측정: `blocked-low-confidence` 문자열이 SKILL.md 에 2 회 이상 등장하고, 그중 하나가
      `verdict` 표 정의 줄에 있음)
- [ ] SK-05: `reflect-digest` 에 family(병합 금지) 출력 섹션이 필수 섹션으로 존재한다 [structural]
      (측정: `grep -c '## 원인 계열 (family)' reflect-kit/skills/reflect-digest/SKILL.md` == 1)
- [ ] SK-06: 구 파편화 임계 `1.5` 가 reflect-kit 스킬 3 종과 references 에서 **0 건**이다
      [exact, enumerated] (측정: `grep -rn '1\.5' reflect-kit/skills reflect-kit/references` 결과 0 행)
- [ ] SK-07: `reflect-promote` 가 `PostToolUse` 를 예방 surface 로 쓰지 말라고 명시한다 [exact]
      (측정: `grep -c 'PostToolUse` 는 예방 surface 가 아니다\|예방 게이트를 `PostToolUse` 에 걸지 마라'`
      로 2 개 표면(hook 절·안티패턴) 각각 1 회 이상)

## Script

- [ ] SC-01: `log-reflection.sh` 가 어휘를 `canonical → aliases` 형태로 주입한다 [goal]
      (Given: fixture 로그 2 파일에 `edited-before-read` 1 · `edit-before-read` 2 ·
      `ignored-required-api-doc-check` 1 · `skipped-required-api-doc-check` 1 · `used-stale-widget-ref` 1 ·
      측정: 스크립트의 어휘 생성 구간을 `sed` 로 **원문 그대로 추출**해 실행 → 출력에
      `- edit-before-read  (freq 3)  ← 같은 뜻으로 쓰인 다른 표기: edited-before-read(1)` 행이 존재 ·
      음성 대조: `tag-lemma-map.tsv` 의 verb 행을 제거하면 이 행이 사라져야 한다)
- [ ] SC-02: `_lib-tag-canon.sh` 의 `tag_canon_fragmentation` 이 bash · zsh · sh 세 셸에서 **동일 1 행**을
      출력한다 [exact, enumerated]
      (측정: 세 셸에서 같은 입력으로 실행한 출력 3 개를 `sort -u` 했을 때 1 행)
- [ ] SC-03: lemma map 을 읽을 수 없으면 `rc=3` + `.errors.log` 에 `warn:lemma-map-unreadable` 1 행을
      남기고 **순수 kebab 정규화로 계속 동작**한다 (fail-open) [goal]
      (측정: `REFLECT_TAG_LEMMA_MAP=/nonexistent` 로 어휘 생성 구간 실행 → rc 3 · 경고 1 행 ·
      어휘 블록이 비어 있지 않음 · 음성 대조: 정상 경로에서는 그 경고가 0 행)
- [ ] SC-04: 결정론적 pass 가 실제로 재발을 회수한다 — 실로그 전량에서 `skipped-required-api-doc-check`
      클러스터 합산이 원시 단독 count 보다 **크다** [goal]
      (측정: `tag_canon_groups ~/.claude/logs/*/reflections-*.md` 의 해당 행 1 열 값과
      원시 `grep | uniq -c` 값을 비교 · 음성 대조: `alias`/`verb-synonym` 행을 제거한 맵으로 실행하면
      두 값이 같아져야 한다)
- [ ] SC-05: 변경·신규 셸 스크립트 2 개가 기본 `shellcheck` 에서 **0 findings** 다 [exact, enumerated]
      (측정: `shellcheck reflect-kit/hooks/_lib-tag-canon.sh reflect-kit/hooks/log-reflection.sh`
      출력 0 행 + exit 0)
- [ ] SC-06: `tag_canon_fragmentation` 이 7 열을 내고 그중 6 열이 `singleton_share` 다 [exact]
      (측정: 출력 1 행을 탭으로 잘라 필드 수 == 7 · 6 열 값이 `0`~`1` 범위 실수)

## Error

- [ ] ER-01: 로그 디렉토리에 `reflections-*.md` 가 0 개일 때 어휘 블록이 `(없음 — 첫 수집)` 이고
      스크립트가 비정상 종료하지 않는다 [exact]
      (측정: 빈 디렉토리로 어휘 생성 구간 실행 → 출력에 `(없음 — 첫 수집)` 포함 · 셸 오류 0 행)
- [ ] ER-02: 기존 환경 dedup 게이트와 codex→claude fallback 경로가 **변경되지 않았다** [exact, enumerated]
      (Given: 커밋 직전 working tree ·
      측정: `git diff -U0 -- reflect-kit/hooks/log-reflection.sh` 의 변경 hunk 중
      `try_claude_fallback` · `env_state` · `REFLECT_ENV_REPEAT_DAYS` 를 포함하는 줄이 0 행)
- [ ] ER-03: `new_tag_reason` 은 **선택 필드**로 도입된다 — 없는 블록을 파싱 실패로 처리하지 않는다 [exact]
      (측정: 훅 프롬프트에 `canonical 을 재사용했으면 이 줄 자체를 생략한다` 문구 존재 +
      `reflect-digest` 스키마 주석에 `선택 필드` 존재)

## Architecture

- [ ] AR-01: 변경이 Scope 내부로만 한정된다 [exact, enumerated]
      (Given: 커밋 직전 working tree ·
       측정: `git status --porcelain -- reflect-kit/` 의 경로 집합이
       `reflect-kit/hooks/log-reflection.sh`, `reflect-kit/hooks/_lib-tag-canon.sh`,
       `reflect-kit/references/`, `reflect-kit/skills/reflect-digest/SKILL.md`,
       `reflect-kit/skills/reflect-kaizen/SKILL.md`, `reflect-kit/skills/reflect-promote/SKILL.md`
       6 항목과 정확히 일치)
- [ ] AR-02: 정규화 **매핑 데이터**가 `references/tag-lemma-map.tsv` 한 곳에만 존재한다 (SSOT) [exact]
      (측정: `grep -rln 'verb-synonym' reflect-kit/` 결과에서 데이터 행(`^verb-synonym\t`)을 실제로
       담은 파일이 `tag-lemma-map.tsv` 1 개뿐)
- [ ] AR-03: 사실 정정 — 훅의 canonical 예시가 최빈형이다. 규범 예시로서의 `edited-before-read` 가
      **0 건**이다 [exact]
      (측정: `grep -n 'edited-before-read' reflect-kit/hooks/log-reflection.sh` 결과 0 행 ·
       `grep -c 'edit-before-read' reflect-kit/hooks/log-reflection.sh` >= 1)
- [ ] AR-04: 사실 정정 — 재확인 실패한 Sentry 직접 인용(`really bad groups`)이 reflect-kit 전체에서
      **0 건**이다 [exact]
      (측정: `grep -rn 'really bad groups' reflect-kit/` 결과 0 행)
- [ ] AR-05: Scope 밖 파일이 변경되지 않았다 [exact, enumerated]
      (Given: 커밋 직전 working tree ·
       측정: `git status --porcelain -- reflect-kit/docs reflect-kit/README.md
       reflect-kit/hooks/hooks.json reflect-kit/scripts reflect-kit/.claude-plugin` 결과 0 행)

## Anti-patterns

- [ ] AP-03: 신규·변경 마크다운에 bare code fence 가 없다 (언어 힌트 필수)
      (측정: `python3 scripts/validate-plugin.py reflect-kit --check=code-fence` 가 OK)
- [ ] AP-04: 신규·변경 SKILL.md frontmatter 에 `name` 필드가 유지된다
      (측정: `python3 scripts/validate-plugin.py reflect-kit --check=frontmatter` 가 OK)

## Reusability

- [ ] RE-01: 정규화 로직이 스킬 본문에 복제되지 않고 `hooks/_lib-tag-canon.sh` 한 곳에만 구현된다
      (측정: `grep -rn 'function norm\|tolower(s)' reflect-kit/` 결과가 `_lib-tag-canon.sh` 만)
- [ ] RE-02: 훅이 기존 공용 라이브러리 로드 규약(`source "$SCRIPT_DIR/_lib-*.sh"`)을 그대로 따른다
      (측정: `grep -c 'source "$SCRIPT_DIR/_lib-' reflect-kit/hooks/log-reflection.sh` == 3)

## Diagnostics

- [ ] DG-01: `python3 scripts/validate-plugin.py reflect-kit` 가 V1~V8 전부 OK, exit 0
- [ ] DG-02: `bash -n` 이 변경·신규 셸 스크립트 2 개에서 통과
- [ ] DG-03: 어휘 생성 구간 3 경로(정상 · map 부재 · 빈 디렉토리) 실행 테스트 전부 통과
- [ ] DG-04: `python3 scripts/sync-docs.py reflect-kit --check-only` 가 동기화 필요 0 건
