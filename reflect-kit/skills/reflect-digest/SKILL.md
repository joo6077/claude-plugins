---
name: reflect-digest
description: >
  ~/.claude/logs/<project_id>/reflections-*.md 에 쌓인 구조화 YAML 블록을 읽어
  카테고리/태그별 빈도를 집계하고, 반복 실수·오해·잘못된 접근 패턴을 리포트한다.
  scope × risk_class × procedurality × enforcement_need 4축과 빈도를 조합해
  승격 후보(project_claude_md / memory / skill / hook / path_scoped_rule)를 precedence table로 계산한다.
  "피드백 정리", "내가 자주 뭘 틀려", "오해 패턴", "reflect digest", "digest",
  "지난주 실수 정리", "대화 피드백 집계" 같은 요청 시 트리거.
  harness 카이젠(계약/평가자/하네스 개선)이나 release 워크플로우에는 트리거하지 않는다.
argument-hint: "[project=<id>] [period=<7d|30d|all>]"
user-invocable: true
---

# Reflect Digest

대화 중 발생한 오해/반복 실수/잘못된 접근을 집계하고 Claude 행동 개선 surface에 반영할 승격 후보를 도출하는 스킬.

**주의**: 이 시스템은 `harness-kaizen`과 도메인이 다르다. harness 카이젠은 QA/Contract/Evaluator 인프라 자체의 개선이고, 이 스킬은 **사용자-Claude 의사소통 품질과 Claude의 일상적 실수 패턴**을 개선한다. 혼동 금지.

## Gotchas

1. **리포트만 — 실제 승격 반영은 금지**. digest 는 후보 리스트를 내는 역할이다. `CLAUDE.md` / memory / skill / hook 에 규칙을 직접 쓰지 마라. 반영은 `/reflect-promote` 가 담당한다. digest가 "써두는 게 더 편하다"며 직접 쓰면 ledger 가 깨지고 rollback 이 불가능해진다.
2. **project_id 쿼리는 `normalize_project_query` 헬퍼로 확장하라** (v0.3.0+). Hybrid 포맷에서 basename 만으로도 정상 id 이지만, 같은 basename 의 기존 `<basename>-<hash6>` 디렉토리도 read 에 포함해야 한다. `compute_project_id` 는 쓰기 id 계산, `normalize_project_query` 는 읽기 glob 확장용.
3. **period 범위 밖 엔트리를 섞지 마라**. 사용자가 `period=7d` 로 요청했으면 `promoted_at` / 타임스탬프 헤더 기준으로 엄격히 필터링한다. "최근과 가까우니까" 임의로 포함 금지 — 재발률 계산이 왜곡된다.
4. **단일 `surface_candidate` 필드를 재도입하지 마라**. scope × risk × procedurality × enforcement 4축 precedence 로만 계산한다. digest 가 편의상 단일 필드를 만들면 promote 단계가 precedence 를 재판정하지 않고 그대로 믿어 surface 판정 품질이 떨어진다.
5. **CLAUDE.md 200줄 한도 계산을 누락하지 마라**. 규칙 #4(project CLAUDE.md 승격) 후보로 판정한 경우, 현재 CLAUDE.md 라인 수를 측정하고 180줄 이상이면 리포트에 **path_scoped_rule 로 fallback 검토 필요** 플래그를 달아라.
6. **harness-kaizen 의 이슈를 이 리포트에 섞지 마라** — 도메인 다름. `.harness/feedback-draft.yaml`, sprint-contract 결과 등은 digest 입력이 아니다.
7. **`actionability: user_environment` 엔트리를 승격 파이프라인에 넣지 마라.** 사용자 환경/설정만 고치면 해소되는 사건(없는 훅 스크립트 참조, 실행 권한 없음, CLI 미설치, 포트 점유)은 **Claude 행동 개선 대상이 아니다.** precedence table 에 넣지 말고 별도 `## 환경 액션 아이템` 섹션으로 라우팅하라. 2026-07 실측: 760 엔트리 중 351건(40%)이 단일 환경 오설정의 반복 로깅이었고, 이것이 `tool_failure` 로 집계되어 진짜 행동 신호를 삼켰다.
8. **원시 `mistake_tag` 빈도로 precedence 를 적용하지 마라 — 반드시 클러스터링 먼저.** 분석기가 같은 근본원인에 다른 태그를 붙이면 개별 빈도가 임계 미달로 떨어져 **최상위 이슈가 아무것도 승격되지 않는다.** 2026-07 실측: 동일 사건 1건이 54 태그로 파편화. 행동 신호도 같은 문제를 겪었다 — API 문서 조회 스킵 계열이 `skipped-required-api-doc-check`(9) · `missing-official-doc-lookup-for-external-api`(2) · `ignored-required-api-doc-lookup`(1) · `external-api-doc-lookup-skipped`(1) · `ignored-docs-research-requirement`(1) · `research-before-edit-ignored`(1) 6 태그로 쪼개져 합산 15건인데 각각은 임계 미달이었다.
9. **파싱 실패를 조용히 넘기지 마라.** YAML 블록 파싱 실패 건수를 리포트 헤더에 반드시 노출한다 (0 이어도 `0` 으로 명시). 2026-07-27 실측 실행에서 760 엔트리 중 6 블록이 파싱 실패했는데 리포트에 드러나지 않으면 집계 신뢰도를 판단할 수 없다.

## 입력

- `project` (optional): 집계할 프로젝트 id. 다음 3 형태 모두 수용 (v0.3.0+):
  - `<basename>` — Hybrid 기본 (예: `project=app_kiosk`)
  - `<basename>-<6자 hash>` — 충돌 감지된 프로젝트 또는 v0.2.0 레거시 (예: `project=app_kiosk-a3b4f9`)
  - `all` — cross-project 집계 (`~/.claude/logs/` 전 프로젝트 순회)
  - 없으면 현재 cwd 로부터 계산. `normalize_project_query` 가 `<basename>` 입력을 `<basename>` + `<basename>-<hash6>` glob union 으로 확장하여 기존 해시 디렉토리도 함께 읽는다.
- `period` (optional): `7d` / `30d` / `all`. 기본 `7d`.

## 프로젝트 ID (v0.3.0 Hybrid)

로그 경로는 `~/.claude/logs/<project_id>/`.

- **기본**: `<basename(git-root)>` — 충돌 없는 경우 hash 없이 사용
- **충돌 fallback**: `<basename>-<6자 md5 hex>` — 동일 basename + 다른 git root 감지 시 자동 전환 + stderr 1회 경고
- **backward-compat**: 기존 `<basename>-<hash6>` 디렉토리는 read 에서 glob union 으로 그대로 포함 — 마이그레이션 불필요

헬퍼: `${CLAUDE_PLUGIN_ROOT}/hooks/_lib-project-id.sh`
- `compute_project_id "$cwd"` — 쓰기용 id 계산 (basename 또는 hash fallback)
- `normalize_project_query "<query>"` — 읽기용 glob pattern union 확장

### 정규화 쿼리 동작

입력이 어느 형태든 **같은 basename 의 glob union** 으로 확장되어 backward-compat 을 보장한다:

| 입력 | 확장 결과 |
|------|-----------|
| `app_kiosk` | `app_kiosk  app_kiosk-[0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f]` |
| `app_kiosk-a3b4f9` | `app_kiosk  app_kiosk-[0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f]` (basename 추출 후 동일 union) |

결과: `/reflect-digest project=app_kiosk` 와 `/reflect-digest project=app_kiosk-a3b4f9` 는 항상 동일한 스캔 대상 집합을 선택한다.

Matching 디렉토리 0개이면 stderr 에 `no matching buckets for project=<query>` 출력 후 종료.

## 데이터 소스

- `~/.claude/logs/<project_id>/YYYY-MM.md` — raw 프롬프트 / tool-failure 로그
- `~/.claude/logs/<project_id>/reflections-YYYY-MM.md` — Stop 훅 분석 결과 (구조화 YAML)
- `~/.claude/logs/<project_id>/.errors.log` — 훅 자체 실패 로그 (CLI 미설치 / timeout 등) + `env-dedup:` / `skip:env-dedup-all` 억제 기록
- `~/.claude/logs/<project_id>/.env-issues.tsv` — 환경 오설정 롤업. `tag <TAB> first_seen <TAB> last_seen <TAB> count` (epoch 초). Stop 훅의 dedup 게이트가 억제한 사건이 여기 누적되므로, **reflections 본문의 빈도만 보면 환경 이슈의 실제 규모를 과소평가한다.** `## 환경 액션 아이템` 섹션은 이 파일을 근거로 쓴다.

## YAML 스키마 (reflection 엔트리)

각 타임스탬프 헤더(`## <ISO8601>`) 아래 여러 YAML 블록이 있을 수 있다.

```yaml
primary_category: misunderstanding | repeated_error | wrong_approach | tool_failure
also_applies: []       # 추가로 해당하는 카테고리 (multi-label)
mistake_tag: <kebab-case>
trigger: <str>
undesired_behavior: <str>
desired_behavior: <str>
severity: low | medium | high
actionability: claude_behavior | user_environment   # Claude 행동으로 막을 수 있었나 / 사용자 환경 작업이어야 하나
# Surface 결정 4축 (precedence table로 최종 surface 계산)
scope: session | project | global
risk_class: low | medium | high
procedurality: single_rule | multi_step_procedure
enforcement_need: soft_reminder | hard_gate
user_stated_constraint: true | false   # 사용자가 명시적으로 금지/지시한 제약의 재위반 (omission-constraint-decay 신호)
evidence_turns: <int>
tools_used:
  skills: []
  agents: []
  mcp_servers: []
approach_note: <str>
```

**단일 `surface_candidate` 필드는 스키마에서 제거되었다.** 4축을 precedence table에 넣어 digest가 최종 surface를 계산한다.

## Process

1. **프로젝트·기간 결정**
   - `project` 인자 없으면 `compute_project_id "$PWD"` 로 basename (또는 hash fallback) 계산
   - `project` 있으면 `normalize_project_query "$project"` 로 glob pattern union 확장
   - `project=all` 이면 `~/.claude/logs/*/` 전체 순회 (단 `is_internal_logs_dir` 로 `_cron`, `.*`, `_*` 제외)
   - `period` 기본 `7d`
2. **로그 디렉토리 매칭**: 확장된 glob 패턴으로 `~/.claude/logs/` 하위 매칭. 0개이면 `no matching buckets for project=<query>` 를 stderr 에 출력하고 종료.
3. **로그 파일 나열**: 매칭된 각 디렉토리의 `reflections-*.md` 전부 (union)
4. **엔트리 파싱**: 타임스탬프 헤더 기준 분할 → `yaml` 코드블록 추출 → period 범위 밖 제외
   - 파싱 실패 블록은 **버리지 말고 센다**. `파싱 실패: N 블록` 을 리포트 헤더에 출력 (Gotcha #9).
   - `actionability` 필드가 없는 레거시 엔트리는 `claude_behavior` 로 간주한다 (fail-open — 행동 신호 유실 방지).
5. **actionability 분리** — 파싱된 엔트리를 두 갈래로 나눈다.
   - `claude_behavior` → 6단계 클러스터링 → precedence 대상
   - `user_environment` → precedence 에서 **제외**. `.env-issues.tsv` 와 합쳐 `## 환경 액션 아이템` 섹션에만 보고 (Gotcha #7)
6. **태그 클러스터링 (canonical_tag + aliases)** — 원시 태그 빈도로 곧장 집계하지 않는다 (Gotcha #8).
   - **묶는 기준은 근본원인이다.** `undesired_behavior` / `desired_behavior` 가 같은 사건을 가리키면 표기가 달라도 한 클러스터다. 표기 유사도(문자열 거리)만으로 묶지 마라 — `edit-before-read` 와 `edited-wrong-file` 은 철자가 비슷해도 다른 원인이다.
   - 각 클러스터에서 **최다 빈도 멤버를 `canonical_tag`** 로, 나머지를 `aliases` 로 둔다. 동률이면 가장 최근에 등장한 태그.
   - **감사 흔적 필수** — 클러스터마다 멤버 태그 전체와 개별 freq 를 리포트에 나열한다. 묶은 근거 없이 합산 숫자만 제시하면 승격 판단을 검증할 수 없다.
   - **과잉 병합 금지.** 서로 다른 근본원인을 한 태그로 합치면 승격 규칙 문구가 모호해져 아무 행동도 바뀌지 않는다. 확신이 없으면 묶지 말고 `## 병합 보류` 로 남겨라. (Sentry fingerprint 규칙도 자주 바뀌는 값으로 그룹핑하면 "really bad groups" 가 된다고 경고한다 — https://docs.sentry.io/concepts/data-management/event-grouping/fingerprint-rules/)
   - 클러스터가 3개 이상 멤버를 가지면 `## ⚠️ 태그 파편화` 섹션에 별도 보고하고, 그 `canonical_tag` 를 Stop 훅 어휘 수렴 대상으로 표시한다.
7. **집계** (5·6 단계 결과 기준)
   - **클러스터별 `cluster_freq`** (= canonical + aliases 합산). 원시 `mistake_tag`별 count 도 함께 보관 (감사용)
   - `primary_category`별 count (+ `also_applies` 가중치 0.5 반영)
   - `severity` 분포
   - `tools_used.skills / agents / mcp_servers` 교차 빈도 (특정 스킬 호출 시 반복되는 실수)
   - 4축별 분포 (`scope`, `risk_class`, `procedurality`, `enforcement_need`)
   - **파편화 지표**: `원시 태그 수 / 클러스터 수`. 1.5(**hypothesis** — `/reflect-kaizen` calibration 대상) 초과면 Stop 훅 어휘 주입이 작동하지 않는다는 신호 → `/reflect-kaizen` 대상으로 표시
8. **승격 후보 계산 (아래 Precedence Table)** — **`freq` 는 항상 `cluster_freq`** 다. 원시 태그 빈도로 임계를 판정하지 마라.
9. **리포트 출력**
10. **결과 저장 (옵션)**: `~/.claude/logs/<project_id>/digest-YYYY-MM-DD.md` — `project` 인자로 쓴 id 그대로 사용. 반영 자체는 후속 `/reflect-promote` 가 맡음.

## Cross-project 집계 (v0.2.0: `project=all`)

`project=all` 로 호출 시 단일 프로젝트가 아닌 **전 프로젝트를 글로벌 순회**한다.
Precedence Table #3 (`scope == global` AND 복수 프로젝트 freq ≥ 3) 판정은 이 모드에서만 의미 있다.

### 1. 글로벌 순회 규칙

- `~/.claude/logs/*/` 하위 모든 디렉토리를 project bucket 으로 취급
- **내부 디렉토리 제외**: `is_internal_logs_dir` 로 `_cron`, dot-prefix, underscore-prefix 디렉토리는 순회에서 자동 제외 (예: `_cron/` 은 install-scheduler.sh 로그 — project 가 아님)
- v0.3.0 Hybrid 에서 `<basename>` 과 `<basename>-<hash6>` 는 동등 bucket. 두 형태가 공존하는 프로젝트는 `normalize_project_query` 로 자동 병합 집계
- 디렉토리별 `reflections-YYYY-MM.md` 와 `.errors.log` 둘 다 읽음. 읽기 실패는 해당 bucket 만 skip

### 2. 이중 freq 계산 (프로젝트별 + 글로벌)

- 계산 단위는 **클러스터** 다 (`canonical_tag`). 원시 태그가 아니다:
  - `per_project_freq[canonical][pid]` — 각 프로젝트 안에서의 클러스터 빈도
  - `global_freq[canonical]` — 모든 프로젝트 합산 빈도
  - `project_count[canonical]` — 이 클러스터가 등장한 **서로 다른 프로젝트 수**
- Precedence #3 판정: `global_freq[canonical] ≥ 3 AND project_count[canonical] ≥ 2` 일 때 global 승격 후보

### 2-1. 단일 프로젝트 편중 경고 (필수)

한 프로젝트가 전체 엔트리를 지배하면 cross-project 집계가 사실상 single-project 집계가 되고,
`scope == global` 판정(rule #3)이 그 프로젝트의 국소 습관을 전역 규칙으로 승격시킨다.

- 프로젝트별 엔트리 점유율을 계산하고 **최대 점유율 ≥ 60%** 이면 리포트 헤더에 경고 라인을 **반드시** 출력한다:
  `⚠️ 편중: <pid> 가 전체의 X% (N/M 엔트리) — 글로벌 판정(rule #3) 신뢰도 낮음`
- 경고가 떴을 때 rule #3 후보는 **지배 프로젝트를 제외한 잔여 freq 로 재확인**한다. 잔여 `project_count ≥ 2` 가 유지되지 않으면 global 이 아니라 rule #4/#5(해당 프로젝트 국소)로 재할당하라.
- 60% 는 hypothesis 다 — `/reflect-kaizen` calibration 대상.
- 2026-07-27 실측: `fit-pal` 747 / `purchase-bot` 13 (총 760) → 98% 편중이었는데 리포트에 경고가 없었다.

### 3. Precedence Table 재적용

single-project 모드와 동일한 규칙이되 `freq` 해석이 달라진다. **진입 전제 3가지(`user_environment` 제외 · `cluster_freq` 사용 · ledger active 재발은 등급 상향)는 아래 "Surface Precedence Table" 과 동일하게 적용한다.** 아래 `global_freq` / `project_count` 는 모두 클러스터 단위다.

| # | 조건 (project=all 기준) | 승격 surface |
|---|---|---|
| 0 | 어느 프로젝트든 `user_stated_constraint == true` (global_freq ≥ 1) | **fast-track** — `project_count ≥ 2`면 글로벌 CLAUDE.md, 단일 프로젝트면 해당 project CLAUDE.md |
| 1 | 어느 프로젝트든 `enforcement_need == hard_gate` | **hook 검토** |
| 2 | `procedurality == multi_step_procedure` AND `global_freq ≥ 2` | **skill** |
| 3 | `global_freq ≥ 3` AND `project_count ≥ 2` | risk=high → **글로벌 CLAUDE.md** / 나머지 → **글로벌 memory** |
| 4 | 단일 프로젝트에 국한되고 `per_project_freq ≥ 3` | **project CLAUDE.md** (해당 프로젝트) |
| 5 | 단일 프로젝트에 국한되고 `per_project_freq ≥ 2` | **project memory** (해당 프로젝트) |
| 6 | `risk_class == low` AND 전체 freq == 1 | **관망** |
| 7 | 그 외 | **수동 review** |

### 4. Given-When-Then 동작 계약

- **Given** `/reflect-digest project=all period=30d` 호출,
- **When** digest가 `~/.claude/logs/*/reflections-*.md` 를 순회하고 (내부 디렉토리 제외),
- **Then** 리포트 상단에 아래 형태의 메타라인이 정확히 표시된다:
  ```text
  # Reflect Digest — project=all (30d)
  대상 프로젝트: N개 (basename B개 / hash-fallback H개) / 총 엔트리: M개
  집계 실패 프로젝트: K개 (project_id 리스트)
  파싱 실패: P 블록
  원시 태그 J개 → 클러스터 C개 (파편화 지표 J/C)
  ⚠️ 편중: <pid> 가 전체의 X% (N/M 엔트리) — 글로벌 판정(rule #3) 신뢰도 낮음
  ```
- `basename B개` = hash suffix 없는 Hybrid 기본 포맷 bucket 수
- `hash-fallback H개` = `<basename>-<6자 hex>` 충돌 fallback + v0.2.0 레거시 bucket 수
- `집계 실패 프로젝트` / `파싱 실패` / 파편화 지표 라인은 값이 0 이어도 생략하지 않고 `0` 으로 명시한다 (검증 용이성).
- 편중 경고 라인은 최대 점유율 < 60% 일 때만 생략한다.

### 5. 출력 포맷 예시 (cross-project)

```text
# Reflect Digest — project=all (30d)
대상 프로젝트: 7개 (basename 4개 / hash-fallback 3개) / 총 엔트리: 142개
집계 실패 프로젝트: 0개

## 글로벌 상위 패턴 (mistake_tag × project_count)
| count | projects | mistake_tag | primary | risk | proc | enforce | 승격 후보 |
|------:|---------:|-------------|---------|------|------|---------|-----------|
|   12  |    3     | wrong-path-inference | misunderstanding | medium | single | soft | 글로벌 memory (rule #3) |
|    8  |    2     | startup-env-check-hook-failure | tool_failure | high | single | hard | **hook 검토 (rule #1)** |

## 프로젝트별 Top 3
- `claude-plugins`: tag-a (5) · tag-b (3) · tag-c (2)
- `fit-pal-aa2a00`: tag-d (4) · tag-e (3)
- ...
```

## Surface Precedence Table

**진입 전제 3가지 (여기서 걸러진 후보는 아래 표를 적용하지 않는다):**

1. `actionability == user_environment` → precedence 대상 아님. `## 환경 액션 아이템` 으로만 보고 (Gotcha #7).
2. `freq` 는 **`cluster_freq`** 다 (canonical + aliases 합산). 원시 태그 빈도로 임계를 판정하지 마라 (Gotcha #8).
3. 같은 `canonical_tag`(또는 그 alias)가 `promotions-ledger.md` 에 `status: active` 로 이미 있으면 **재발**이다. 표를 다시 적용해 같은 surface 로 재승격하지 말고 `## 재발 — 등급 상향 후보` 섹션으로 라우팅한다. digest 는 라우팅과 `post_freq` 제시까지만 하고, **실제 등급 상향 판정(재발 2회 이상 E2 / 3회 이상 E3)과 반영은 `/reflect-promote` §B 가 수행한다.**

아래 규칙을 **위에서 아래로** 적용. 먼저 맞는 규칙 하나만 선택.

| # | 조건 | 승격 surface |
|---|------|--------------|
| 0 | `user_stated_constraint == true` (freq ≥ 1, 임계값 우회) | **매-세션 자동 로드 surface로 fast-track** — `scope==global`이면 글로벌 CLAUDE.md, 아니면 project CLAUDE.md (200줄 초과 시 path-scoped rule). `enforcement_need==hard_gate`면 추가로 hook 후보 병기 |
| 1 | `enforcement_need == hard_gate` (빈도 무관) | **hook 검토** (다른 축 무시) |
| 2 | `procedurality == multi_step_procedure` AND freq ≥ 2 | **skill** 신설/보강 |
| 3 | `scope == global` AND 복수 프로젝트에서 freq ≥ 3 | **글로벌 CLAUDE.md** (risk_class=high) 또는 **글로벌 memory** (나머지) |
| 4 | `scope == project` AND freq ≥ 3 | **project CLAUDE.md** — 단 CLAUDE.md 가 200줄 초과 예상 시 **`.claude/rules/<tag>.md`** path-scoped rule로 스필오버 |
| 5 | `scope == project` AND freq ≥ 2 | **project memory (feedback 타입)** |
| 6 | `risk_class == low` AND freq == 1 | **관망** (no action, 다음 주 재평가) |
| 7 | 그 외 | **review 후보 (수동)** |

> **규칙 #0 근거 (Friction #2 — insights-report #2 "이전 세션 피드백이 durable rule로 자동 적용 안 됨" 대응)**: 사용자가 명시적으로 금지/지시한 제약(예: "ValueNotifier 쓰지 마")의 재위반은 일반 실수보다 **사용자 좌절이 크고**, 연구상 long-context에서 가장 먼저 잊히는 omission 제약이다 (Omission Constraints Decay While Commission Constraints Persist, https://arxiv.org/html/2604.20911). 따라서 freq 2/3회 누적을 기다리지 말고 **첫 재위반부터** 매-세션 자동 로드 surface(CLAUDE.md/hook)로 보낸다. memory(on-demand 로드)나 관망으로 보내면 재주입이 약해 friction이 해소되지 않는다. 단 surface 반영은 항상 `/reflect-promote`가 사용자 승인을 거쳐 수행한다 (digest는 후보 표시만).

### 임계값은 hypothesis

> 위 `freq == 2`, `freq == 3` 기준은 **hypothesis**이다. 30일 운영 후 pre/post 재발률을 보고 calibration 한다.
>
> 참고: Claude 공식 문서는 "같은 실수 2번째 → `CLAUDE.md`에 추가" 권고. 현재 표는 "2회는 memory, 3회는 CLAUDE.md"로 한 단 낮게 설정 — 과잉제약 부작용을 우선 배제하기 위함. 운영 데이터로 재조정.

### CLAUDE.md 용량 예산

- 공식 권고: 200줄 이하
- 초과 예상 시 `.claude/rules/<tag>.md` (path-scoped) 또는 skill로 스필오버
- digest가 현재 `CLAUDE.md` 줄 수를 측정해 스필오버 필요성 플래그

## 출력 포맷

아래 섹션은 **전부 필수**다. 해당 건수가 0이어도 섹션과 숫자를 생략하지 않는다.

```markdown
# Reflect Digest — <project_id> (<period>)

## 요약
- 총 엔트리: N개 / 세션: M개 / 파싱 실패: P 블록
- 원시 태그 J개 → 클러스터 C개 (파편화 지표 J/C)
- actionability: claude_behavior A개 / user_environment B개
- primary_category: misunderstanding X / repeated_error Y / wrong_approach Z / tool_failure W
- severity: low L / medium M / high H
- 4축 분포: scope(session S / project P / global G), risk_class(...), procedurality(...), enforcement_need(...)

## ⚠️ 태그 파편화 (멤버 3개 이상 클러스터)
| cluster_freq | canonical_tag | aliases (개별 freq) |
|------------:|---------------|---------------------|
| 15 | skipped-required-api-doc-check (freq 9 — 최다 멤버) | missing-official-doc-lookup-for-external-api(2), ignored-required-api-doc-lookup(1), external-api-doc-lookup-skipped(1), ignored-docs-research-requirement(1), research-before-edit-ignored(1) |

## 상위 반복 패턴 (클러스터별)
| cluster_freq | primary | also_applies | canonical_tag | severity | scope | risk | proc | enforce |
|------------:|---------|--------------|---------------|----------|-------|------|------|---------|
| ... | ... | ... | ... | ... | ... | ... | ... | ... |

## 재발 — 등급 상향 후보 (ledger `status: active` 인데 재발)
판정·반영은 `/reflect-promote` §B. digest 는 라우팅 + 수치 제시까지만 한다.

| rule_id | canonical_tag | 현재 surface | enforcement_level | post_freq | 제안 |
|---------|---------------|--------------|-------------------|----------:|------|
| a1b2c3d4 | skipped-required-api-doc-check | project CLAUDE.md | E1 | 9 | E3 상향 검토 (재발 3회 이상) |

## 승격 후보 (precedence 적용 — freq 는 cluster_freq)
### 1. `<canonical_tag>` → `project CLAUDE.md` (규칙 #4)
- 빈도: 3회 (세션 2개) / aliases: [...]
- 4축: scope=project, risk=medium, proc=single, enforce=soft
- 근거: undesired_behavior / desired_behavior 요약
- 초안 규칙: "..."

### 2. `<canonical_tag>` → `skill 신설` (규칙 #2)
- ...

## 환경 액션 아이템 (승격 대상 아님 — 사용자 환경 작업)
`.env-issues.tsv` + `actionability: user_environment` 엔트리 기준. Claude 행동 개선이 아니므로
precedence 를 적용하지 않는다. 각 항목은 **1줄** 로만 보고한다.

| count | tag | first_seen | last_seen | 필요한 사용자 조치 |
|------:|-----|------------|-----------|--------------------|
| 351 | missing-hook-scripts | 2026-06-27 | 2026-07-27 | `.claude/settings.json` 이 참조하는 스크립트 생성 또는 훅 선언 제거 |

## 스킬/에이전트 교차 분석
- `/<skill-name>` 호출 시 "<canonical_tag>" 실수가 N회 → 해당 스킬에 가드 추가 검토

## 훅 실패 요약 (.errors.log)
- skip:cli-missing: X건
- fail:codex-exit-N: Y건
- env-dedup (억제): Z건
- ...

## 병합 보류 (근본원인 확신 부족)
- `<tag-a>` / `<tag-b>` — 표기는 유사하나 원인이 같은지 불확실. 다음 주기 재평가

## 미분류 원시 엔트리 (n건)
- ...
```

## Ledger 스키마 (후속 /reflect-promote 가 관리)

현재 digest는 리포트만 수행한다. 실제 승격 반영은 `/reflect-promote` 스킬이 담당하며, 승격 이력은 다음 ledger 파일에 append 된다.

경로: `~/.claude/logs/<project_id>/promotions-ledger.md`

```yaml
- rule_id: <uuid>                     # 고유 ID (uuidgen)
  mistake_tag: <canonical_tag>        # 클러스터의 대표 태그
  aliases: []                         # 같은 근본원인의 다른 표기들. post_freq 는 canonical + aliases 합산
  promoted_to: project_claude_md | project_memory | global_claude_md | global_memory | skill | path_scoped_rule | hook
  enforcement_level: E1 | E2 | E3     # skill-design-guide §3.7 등급. 재발 시 상향
  target_path: <실제 수정된 파일 경로>
  promoted_at: <ISO8601 with TZ>
  source_evidence:                    # 이 규칙을 만든 로그 근거
    - path: ~/.claude/logs/<id>/reflections-YYYY-MM.md
      anchor: <타임스탬프 헤더>
  initial_freq: <int>                 # 승격 시점 빈도 (cluster_freq)
  calibration_window_days: 30
  post_freq: <int>                    # 30일 뒤 digest가 자동 업데이트 (aliases 포함 합산)
  status: active | demoted | removed
  demotion_reason: <str>              # 강등된 경우만
```

이 ledger로 **regression 측정**이 가능하다. digest는 `promoted_at` 이후 같은 `mistake_tag` 재발 횟수를 `post_freq`에 기록하고, 30일 재발 0 + low risk 면 `status: demoted` 후보로 표시한다.

## 안티패턴 (하지 말 것)

- harness-kaizen 규칙을 이 리포트에 섞지 마라 — 별개 시스템
- 승격을 이 스킬에서 실제로 반영하지 마라 — **리포트만**. 반영은 `/reflect-promote`가 담당.
- `<basename>` 쿼리를 단일 디렉토리 매칭으로 처리하지 마라 — 반드시 `normalize_project_query` 로 glob union 확장 (기존 hash 디렉토리 누락 방지).
- 내부 디렉토리(`_cron`, dot/underscore-prefix)를 project bucket 으로 집계하지 마라 — `is_internal_logs_dir` 필터 필수.
- 단일 `surface_candidate` 필드를 재도입하지 마라 — 4축 precedence로만 계산.
- period 범위 밖 엔트리를 섞지 마라.
- **원시 `mistake_tag` 빈도를 그대로 precedence 임계에 넣지 마라** — 반드시 클러스터링 후 `cluster_freq`.
- **`actionability: user_environment` 를 승격 후보로 올리지 마라.** "훅 스크립트를 만들어야 했다" 는 Claude 의 행동 개선이 아니다. 이 항목을 CLAUDE.md/memory 로 승격하면 사용자 환경 작업 지시가 매 세션 컨텍스트를 먹는다.
- **파싱 실패 블록을 조용히 버리지 마라** — 건수를 헤더에 노출.
- **단일 프로젝트 편중을 경고 없이 글로벌 판정에 쓰지 마라** — 점유율 ≥ 60% 면 rule #3 을 잔여 freq 로 재확인.
- **클러스터를 합산 숫자만으로 제시하지 마라** — 멤버 태그와 개별 freq 감사 흔적 필수.
- 이미 `status: active` 인 규칙이 재발했는데 **같은 surface 로 재승격 후보를 만들지 마라** — 등급 상향 후보로 표시.

## 예시 사용

- `/reflect-digest` — 현재 프로젝트, 지난 7일
- `/reflect-digest project=app_kiosk period=30d` — basename 입력 (v0.3.0 Hybrid). `app_kiosk` 와 `app_kiosk-<hash6>` 모두 포함
- `/reflect-digest project=fit-pal-a3b4f9 period=30d` — 완전 id 입력 (backward-compat)
- `/reflect-digest project=all period=30d` — cross-project 집계
