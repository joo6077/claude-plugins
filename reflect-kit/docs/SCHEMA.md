# reflect-kit — SCHEMA

reflect-kit 파이프라인이 사용하는 YAML 스키마 정본. `DESIGN.md`에서 스키마 부분만 분리한 문서.

---

## 1. Reflection 엔트리 (hooks/log-reflection.sh 출력)

경로: `~/.claude/logs/<project_id>/reflections-YYYY-MM.md`

각 타임스탬프 헤더(`## <ISO8601+TZ>`) 아래 여러 YAML 블록이 올 수 있다. `no issues` 한 줄이면 블록 없음.

```yaml
primary_category: misunderstanding | repeated_error | wrong_approach | tool_failure
also_applies: []                      # multi-label: 추가로 해당하는 카테고리
mistake_tag: <kebab-case 영문 태그>   # 같은 패턴이면 같은 태그 (집계 키)
trigger: <str>                        # 사용자 프롬프트/상황 스니펫 1줄
undesired_behavior: <str>             # Claude가 한 잘못 1줄
desired_behavior: <str>               # 사용자가 원한 것 1줄
severity: low | medium | high
actionability: claude_behavior | user_environment   # 아래 "actionability" 절
# Surface 결정 4축 (단일 surface_candidate 필드는 쓰지 않음)
scope: session | project | global
risk_class: low | medium | high
procedurality: single_rule | multi_step_procedure
enforcement_need: soft_reminder | hard_gate
evidence_turns: <int>                 # 교정이 드러난 턴 수
tools_used:
  skills: []                          # invoke된 slash command
  agents: []                          # spawn된 subagent type
  mcp_servers: []                     # 사용한 MCP 서버 prefix
approach_note: <str>                  # 시도한 접근법 1줄
```

### 카테고리 정의

- **misunderstanding** — 사용자 의도 오해 (엉뚱한 파일 수정, 범위 오해, 잘못된 가정)
- **repeated_error** — 같은 세션 내 또는 사용자 교정 뒤에도 반복된 같은 실수
- **wrong_approach** — 더 적절한 스킬/에이전트/MCP가 있었는데 비효율적으로 시도
- **tool_failure** — 도구 호출 실패 중 맥락이 의미 있는 것 (단순 exit code-only는 제외)

카테고리는 **상호 배타적이지 않다**. `primary_category`에 지배적인 하나, `also_applies`에 추가 해당 카테고리를 배열로.

### 4축 필드 의미

| 축 | 의미 | 값 |
|---|---|---|
| `scope` | 이 규칙이 어느 범위에 적용되어야 하는가 | session / project / global |
| `risk_class` | 위반 시 피해 정도 | low / medium / high |
| `procedurality` | 단일 규칙 vs 체크리스트 | single_rule / multi_step_procedure |
| `enforcement_need` | 안내로 충분 vs 차단 필요 | soft_reminder / hard_gate |

승격기(`/reflect-promote`)는 이 4축과 빈도를 precedence table에 넣어 최종 surface 계산.

### actionability

| 값 | 의미 | 파이프라인 취급 |
|---|---|---|
| `claude_behavior` | Claude가 다르게 행동했다면 피할 수 있었던 사건 (기본값) | precedence 대상 |
| `user_environment` | 사용자 환경/설정만 고치면 해소되고 Claude 행동으로는 못 막는 사건 (없는 훅 스크립트 참조, 실행 권한 없음, CLI 미설치, 포트 점유) | **precedence 제외** — digest 의 `## 환경 액션 아이템` 으로만 보고. Stop 훅이 억제 창 안에서 반복 로깅을 차단 |

- 필드가 없는 레거시 엔트리는 `claude_behavior` 로 간주한다 (fail-open).
- `user_environment` 인 경우 `desired_behavior` 에 환경 수정 지시를 쓰지 않는다 — Claude가 그 상황에서 무엇을 보고/판단했어야 하는가를 쓴다.
- 도입 근거: 2026-07 실측에서 760 엔트리 중 351건(40%)이 단일 환경 오설정의 반복 로깅이었고, `tool_failure` 로 집계되어 진짜 행동 신호를 삼켰다.

### mistake_tag 정규화

`mistake_tag` 는 집계 키이자 ledger 의 재발 측정 키다. 파편화되면 승격과 효과 측정이 동시에 깨진다.

- 근본원인 1개 = 태그 1개. 증상·파일명·도구명을 태그에 넣지 않는다.
- 형태는 `<행동동사>-<대상>` kebab-case.
- Stop 훅(`log-reflection.sh`)이 그 프로젝트의 기존 태그 어휘(freq ≥ 2 상위 40개)를 프롬프트에 주입해 재사용을 유도한다 — 분석기는 세션마다 stateless 이므로 어휘를 주지 않으면 매번 새 표기를 만든다.
- 어휘는 **닫힌 집합이 아니다.** 새로운 종류의 사건이면 새 태그를 만든다. 강제로 닫힌 라벨 집합을 주면 드문 신호가 catch-all 로 흡수된다 ([arXiv 2605.06940](https://arxiv.org/abs/2605.06940) — instruction-induced label collapse).
- 이미 쌓인 파편은 `/reflect-digest` 가 `canonical_tag` + `aliases` 클러스터로 복구한다.

---

## 2. Promotion Ledger 엔트리 (reflect-promote 기록)

경로: `~/.claude/logs/<project_id>/promotions-ledger.md`

`/reflect-promote`가 승격마다 한 엔트리 append. 30일 뒤 `/reflect-kaizen`이 `post_freq`를 채운다.

```yaml
- rule_id: <uuid>                       # 고유 ID (uuidgen)
  mistake_tag: <canonical_tag>          # 클러스터 대표 태그
  aliases: []                           # 같은 근본원인의 다른 표기들 (post_freq 합산 대상)
  promoted_to: project_claude_md | project_memory | global_claude_md | global_memory | skill | path_scoped_rule | hook
  enforcement_level: E1 | E2 | E3       # skill-design-guide §3.7 등급 (아래)
  target_path: <실제 수정된 파일 절대경로>
  promoted_at: <ISO8601 with TZ>
  source_evidence:
    - path: ~/.claude/logs/<id>/reflections-YYYY-MM.md
      anchor: <타임스탬프 헤더>
  initial_freq: <int>                   # 승격 시점 빈도 (cluster_freq)
  calibration_window_days: 30
  post_freq: <int | null>               # 30일 뒤 kaizen이 업데이트 (canonical + aliases 합산)
  status: active | demoted | removed
  demotion_reason: <str>                # 강등 시만. 등급 상향이면 escalated-to-E<N> (rule_id: <새 uuid>)
```

### enforcement_level

정의와 승급 임계의 정본(SSOT)은 `harness/docs/guides/skill-design-guide.md` §3.7 "Enforcement 3 등급" 이다.
**이 문서에서 재정의하거나 동의어를 만들지 않는다.** reflect-kit surface 와의 대응만 기록한다.

| §3.7 등급 | reflect-kit surface |
|---|---|
| E1 | project/global memory, CLAUDE.md 한 줄 |
| E2 | path_scoped_rule, skill 의 Process 체크리스트 |
| E3 | hook, 검증 스크립트 |

### Regression 측정 규칙

- `promoted_at + calibration_window_days` 시점에서 `mistake_tag` **+ `aliases` 전체**의 재발 횟수를 `post_freq`에 기록. canonical 단독 count 는 파편화 상황에서 구조적 과소집계다.
- `post_freq == 0` AND `risk_class == low` → `status: demoted` 후보 표시 (과잉제약일 수 있음).
- `post_freq == 1` → 문구 명확화 후보. 등급은 유지.
- `post_freq >= 2` → 규칙이 효과 없음 → **enforcement 등급 상향** 후보 (§3.7 승급 규칙: 2회 이상 E2, 3회 이상 또는 비가역·신뢰 손상이면 E3). 같은 등급에서 문구만 다듬는 것은 개선이 아니다.
- `post_freq < initial_freq` AND `post_freq <= 1` → 효과 있음, 유지.

---

## 3. 훅 에러 로그 (.errors.log)

경로: `~/.claude/logs/<project_id>/.errors.log`

구조: 한 줄당 `<ISO8601+TZ> [<hook-name>] <reason>` 포맷. 파싱 용이성을 위해 key=value 쌍은 공백 구분.

### 사유 태그 (log-reflection.sh)

- `skip:cli-missing` — codex CLI 없음
- `skip:transcript-path-empty` — stdin에 transcript_path 없음
- `skip:transcript-file-missing path=<>` — 파일 없음
- `skip:transcript-too-short lines=<N>` — 10줄 미만
- `skip:transcript-empty-after-tail` — tail 결과 빈 값
- `fail:codex-exit-<N> session=<> err=<한 줄>` — codex exec 비정상 종료
- `fail:codex-empty-output session=<>` — codex 빈 응답
- `fallback:claude-used session=<>` — codex 가 실패해 `claude -p` 대체 경로로 기록했다
- `fallback:claude-exit-<N> session=<> err=<한 줄>` — 대체 경로도 비정상 종료. 이 실행은 기록 없이 끝난다
- `fallback:claude-empty-output session=<>` — 대체 경로 빈 응답
- `skip:fallback-unavailable session=<>` — claude CLI 없음
- `fail:tag-field-unresolved session=<>` — 태그 필드 이름을 못 읽어 분석 전에 멈췄다
- `env-dedup:kept=<N> dropped=<M> drop=<tag>... session=<>` — 환경 오설정 블록 억제
- `skip:env-dedup-all <요약> session=<>` — 전 블록이 억제되어 append 자체를 생략
- `warn:env-dedup-failed exit=<N> session=<>` — dedup 게이트 실패 → fail-open 으로 원본 기록
- `warn:lemma-map-unreadable path=<> session=<>` — 태그 정규화 사전을 못 읽어 사전 없이 태그를 묶었다. 실행은 계속된다
- `vocab:raw_distinct/clusters/entries/singletons/fold/singleton_share/epc=<일곱 값> session=<>` — 태그 파편화 지표 한 줄. 실패가 아니라 `collect_status` 는 세지 않는다
- `ok:no-issues session=<>` — 분석 결과가 「no issues」 인 정상 종료. 실패가 아니며, `collect_status` 는 이 줄 · `skip:env-dedup-all` 과 마지막 기록 가운데 늦은 쪽 뒤의 실패만 「마지막 기록 뒤」 실패로 센다

`err=` 는 줄 끝까지다 (공백 포함). 분석기 stderr 에서 `error` · `ERROR` 로 시작하는 첫 줄, 없으면 비어 있지 않은
첫 줄 하나를 가린 뒤 200 자로 자른다 — codex 는 성공해도 stderr 에 프롬프트 전문을 찍으므로 전문은 남기지 않는다.
대체 경로는 stderr 가 비면 stdout 에서 고른다. `/reflect-digest` 의 `collect_status` 는 대체 경로 실패 셋과
`skip:cli-missing` · `fail:tag-field-unresolved` 를 기록 없이 끝난 실행으로 센다.

---

## 3-1. 환경 오설정 롤업 (.env-issues.tsv)

경로: `~/.claude/logs/<project_id>/.env-issues.tsv`

`tag <TAB> first_seen <TAB> last_seen <TAB> count` (시각은 epoch 초).

Stop 훅의 dedup 게이트가 `actionability: user_environment` 블록을 억제할 때마다 `count` 를 올린다.
억제 창(`REFLECT_ENV_REPEAT_DAYS`, 기본 7일) 안에 같은 태그가 다시 오면 reflections 본문에는
쓰지 않고 여기만 갱신한다. **따라서 reflections 본문의 빈도만 보면 환경 이슈 규모를 과소평가한다** —
`/reflect-digest` 의 `## 환경 액션 아이템` 은 이 파일을 근거로 쓴다.

억제 창 7일은 hypothesis 다: `/reflect-digest` 기본 period 가 `7d` 이므로 digest 사이클마다 최대
1회 재노출된다. 구조는 Alertmanager 의 `group_by` + `repeat_interval` 과 같다
(<https://prometheus.io/docs/alerting/latest/configuration/>).

게이트는 LLM 을 호출하지 않는 순수 판정이며 fail-open 이다 — `actionability` 누락·파싱 실패·awk
비정상 종료 시 원본 블록을 그대로 보존한다. `claude_behavior` 블록은 어떤 경우에도 억제되지 않는다.

---

## 4. Surface Precedence Table (판정 규칙)

진입 전제 3가지 (여기서 걸러진 후보는 표를 적용하지 않는다):

1. `actionability == user_environment` → precedence 대상 아님. 환경 액션 아이템으로만 보고.
2. `freq` 는 `cluster_freq`(canonical + aliases 합산). 원시 태그 빈도로 임계를 판정하지 않는다.
3. ledger 에 같은 canonical/alias 가 `status: active` + `post_freq ≥ 2` 로 있으면 재승격이 아니라 **enforcement 등급 상향**.

위에서 아래로 적용. 먼저 맞는 규칙 하나만 선택.

| # | 조건 | 승격 surface |
|---|---|---|
| 0 | `user_stated_constraint == true` (freq ≥ 1, 임계값 우회) | **매-세션 자동 로드 surface로 fast-track** — `scope==global`이면 글로벌 CLAUDE.md, 아니면 project CLAUDE.md (200줄 초과 시 path-scoped rule). `hard_gate` 면 hook 후보 병기 |
| 1 | `enforcement_need == hard_gate` (빈도 무관) | **hook 검토** (다른 축 무시) |
| 2 | `procedurality == multi_step_procedure` AND freq ≥ 2 | **skill** 신설/보강 |
| 3 | `scope == global` AND 복수 프로젝트 freq ≥ 3 | `risk_class=high` → **글로벌 CLAUDE.md** / 나머지 → **글로벌 memory** |
| 4 | `scope == project` AND freq ≥ 3 | **project CLAUDE.md**. 단 `CLAUDE.md` 200줄 초과 예상 시 **`.claude/rules/<tag>.md`** (path-scoped) |
| 5 | `scope == project` AND freq ≥ 2 | **project memory (feedback 타입)** |
| 6 | `risk_class == low` AND freq == 1 | **관망** (no action) |
| 7 | 그 외 | **수동 review 후보** |

임계값은 hypothesis — `/reflect-kaizen`이 30일 운영 데이터로 calibration.

---

## 5. Project ID 포맷

기본 `<basename(본 레포 root)>`, 같은 basename 폴더를 다른 레포가 이미 쓰면 `<basename>-<6자 md5 hex>` (Hybrid, v0.3.0 부터).

- 본 레포 root 는 `project_root` 가 정한다. 링크된 워크트리(git-dir 과 common-dir 이 다름)이고 공통 git 폴더 이름이
  `.git` 이면 그 부모, 그 밖에는 `git rev-parse --show-toplevel`, git 밖이면 cwd 다 — 워크트리 폴더 이름으로 갈리지 않는다
- 충돌 판정 마커(`.project-root`)와 hash 입력도 같은 root 를 쓴다
- 헬퍼: `${CLAUDE_PLUGIN_ROOT}/hooks/_lib-project-id.sh` 의 `project_root` · `compute_project_id` · `normalize_project_query`
- 워크트리 이름으로 이미 생긴 폴더는 옮기지 않는다 — `DESIGN.md` 결정 #3 상세의 `### 워크트리` 절

---

## 6. 버전 관리

스키마 변경 시 이 파일과 `DESIGN.md`를 동시에 업데이트한다. 호환되지 않는 변경(필드 삭제·의미 변경)은 `log-reflection.sh` 프롬프트도 함께 수정해야 한다.
