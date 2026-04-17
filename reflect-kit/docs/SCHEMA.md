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

---

## 2. Promotion Ledger 엔트리 (reflect-promote 기록)

경로: `~/.claude/logs/<project_id>/promotions-ledger.md`

`/reflect-promote`가 승격마다 한 엔트리 append. 30일 뒤 `/reflect-kaizen`이 `post_freq`를 채운다.

```yaml
- rule_id: <uuid>                       # 고유 ID (uuidgen)
  mistake_tag: <tag>
  promoted_to: project_claude_md | project_memory | global_claude_md | global_memory | skill | path_scoped_rule | hook
  target_path: <실제 수정된 파일 절대경로>
  promoted_at: <ISO8601 with TZ>
  source_evidence:
    - path: ~/.claude/logs/<id>/reflections-YYYY-MM.md
      anchor: <타임스탬프 헤더>
  initial_freq: <int>                   # 승격 시점 빈도
  calibration_window_days: 30
  post_freq: <int | null>               # 30일 뒤 kaizen이 업데이트
  status: active | demoted | removed
  demotion_reason: <str>                # 강등 시만
```

### Regression 측정 규칙

- `promoted_at + calibration_window_days` 시점에서 같은 `mistake_tag` 재발 횟수를 `post_freq`에 기록.
- `post_freq == 0` AND `risk_class == low` → `status: demoted` 후보 표시 (과잉제약일 수 있음).
- `post_freq >= initial_freq` → 규칙이 효과 없음 → 프롬프트 재작성 또는 surface 변경 후보.
- `post_freq < initial_freq` → 효과 있음, 유지.

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
- `fail:codex-exit-<N> session=<>` — codex exec 비정상 종료
- `fail:codex-empty-output session=<>` — codex 빈 응답

---

## 4. Surface Precedence Table (판정 규칙)

위에서 아래로 적용. 먼저 맞는 규칙 하나만 선택.

| # | 조건 | 승격 surface |
|---|---|---|
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

`<basename(git-root)>-<6자 md5 hex>`

- git root 없으면 cwd 절대경로의 md5로 대체
- 헬퍼: `${CLAUDE_PLUGIN_ROOT}/hooks/_lib-project-id.sh` 의 `compute_project_id` 함수
- basename만 같고 다른 repo라도 hash가 달라 충돌하지 않는다

---

## 6. 버전 관리

스키마 변경 시 이 파일과 `DESIGN.md`를 동시에 업데이트한다. 호환되지 않는 변경(필드 삭제·의미 변경)은 `log-reflection.sh` 프롬프트도 함께 수정해야 한다.
