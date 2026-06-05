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
- `~/.claude/logs/<project_id>/.errors.log` — 훅 자체 실패 로그 (CLI 미설치 / timeout 등)

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
5. **집계**
   - `mistake_tag`별 count
   - `primary_category`별 count (+ `also_applies` 가중치 0.5 반영)
   - `severity` 분포
   - `tools_used.skills / agents / mcp_servers` 교차 빈도 (특정 스킬 호출 시 반복되는 실수)
   - 4축별 분포 (`scope`, `risk_class`, `procedurality`, `enforcement_need`)
6. **승격 후보 계산 (아래 Precedence Table)**
7. **리포트 출력**
8. **결과 저장 (옵션)**: `~/.claude/logs/<project_id>/digest-YYYY-MM-DD.md` — `project` 인자로 쓴 id 그대로 사용. 반영 자체는 후속 `/reflect-promote` 가 맡음.

## Cross-project 집계 (v0.2.0: `project=all`)

`project=all` 로 호출 시 단일 프로젝트가 아닌 **전 프로젝트를 글로벌 순회**한다.
Precedence Table #3 (`scope == global` AND 복수 프로젝트 freq ≥ 3) 판정은 이 모드에서만 의미 있다.

### 1. 글로벌 순회 규칙

- `~/.claude/logs/*/` 하위 모든 디렉토리를 project bucket 으로 취급
- **내부 디렉토리 제외**: `is_internal_logs_dir` 로 `_cron`, dot-prefix, underscore-prefix 디렉토리는 순회에서 자동 제외 (예: `_cron/` 은 install-scheduler.sh 로그 — project 가 아님)
- v0.3.0 Hybrid 에서 `<basename>` 과 `<basename>-<hash6>` 는 동등 bucket. 두 형태가 공존하는 프로젝트는 `normalize_project_query` 로 자동 병합 집계
- 디렉토리별 `reflections-YYYY-MM.md` 와 `.errors.log` 둘 다 읽음. 읽기 실패는 해당 bucket 만 skip

### 2. 이중 freq 계산 (프로젝트별 + 글로벌)

- `mistake_tag` 별로 두 가지 빈도를 동시에 계산:
  - `per_project_freq[tag][pid]` — 각 프로젝트 안에서의 빈도
  - `global_freq[tag]` — 모든 프로젝트 합산 빈도
  - `project_count[tag]` — 이 tag가 등장한 **서로 다른 프로젝트 수**
- Precedence #3 판정: `global_freq[tag] ≥ 3 AND project_count[tag] ≥ 2` 일 때 global 승격 후보

### 3. Precedence Table 재적용

single-project 모드와 동일한 규칙이되 `freq` 해석이 달라진다:

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
  ```
- `basename B개` = hash suffix 없는 Hybrid 기본 포맷 bucket 수
- `hash-fallback H개` = `<basename>-<6자 hex>` 충돌 fallback + v0.2.0 레거시 bucket 수
- `집계 실패 프로젝트` 블록이 0개여도 라인 자체는 생략하지 않고 `0개` 로 명시한다 (검증 용이성).

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

```markdown
# Reflect Digest — <project_id> (<period>)

## 요약
- 총 엔트리: N개 / 세션: M개
- primary_category: misunderstanding X / repeated_error Y / wrong_approach Z / tool_failure W
- severity: low L / medium M / high H
- 4축 분포: scope(session S / project P / global G), risk_class(...), procedurality(...), enforcement_need(...)

## 상위 반복 패턴 (태그별)
| count | primary | also_applies | mistake_tag | severity | scope | risk | proc | enforce |
|------:|---------|--------------|-------------|----------|-------|------|------|---------|
| ... | ... | ... | ... | ... | ... | ... | ... | ... |

## 승격 후보 (precedence 적용)
### 1. `<mistake_tag>` → `project CLAUDE.md` (규칙 #4)
- 빈도: 3회 (세션 2개)
- 4축: scope=project, risk=medium, proc=single, enforce=soft
- 근거: undesired_behavior / desired_behavior 요약
- 초안 규칙: "..."

### 2. `<tag>` → `skill 신설` (규칙 #2)
- ...

## 스킬/에이전트 교차 분석
- `/<skill-name>` 호출 시 "<tag>" 실수가 N회 → 해당 스킬에 가드 추가 검토

## 훅 실패 요약 (.errors.log)
- skip:cli-missing: X건
- fail:codex-exit-N: Y건
- ...

## 미분류 원시 엔트리 (n건)
- ...
```

## Ledger 스키마 (후속 /reflect-promote 가 관리)

현재 digest는 리포트만 수행한다. 실제 승격 반영은 `/reflect-promote` 스킬이 담당하며, 승격 이력은 다음 ledger 파일에 append 된다.

경로: `~/.claude/logs/<project_id>/promotions-ledger.md`

```yaml
- rule_id: <uuid>                     # 고유 ID (uuidgen)
  mistake_tag: <tag>
  promoted_to: project_claude_md | project_memory | global_claude_md | global_memory | skill | path_scoped_rule | hook
  target_path: <실제 수정된 파일 경로>
  promoted_at: <ISO8601 with TZ>
  source_evidence:                    # 이 규칙을 만든 로그 근거
    - path: ~/.claude/logs/<id>/reflections-YYYY-MM.md
      anchor: <타임스탬프 헤더>
  initial_freq: <int>                 # 승격 시점 빈도
  calibration_window_days: 30
  post_freq: <int>                    # 30일 뒤 digest가 자동 업데이트
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

## 예시 사용

- `/reflect-digest` — 현재 프로젝트, 지난 7일
- `/reflect-digest project=app_kiosk period=30d` — basename 입력 (v0.3.0 Hybrid). `app_kiosk` 와 `app_kiosk-<hash6>` 모두 포함
- `/reflect-digest project=fit-pal-a3b4f9 period=30d` — 완전 id 입력 (backward-compat)
- `/reflect-digest project=all period=30d` — cross-project 집계
