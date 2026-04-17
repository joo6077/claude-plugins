# reflect-kit — DESIGN

## 데이터 플로우

```text
[ 사용자 프롬프트 ] ─► UserPromptSubmit hook ─► log-prompt.sh ─► redact ─► YYYY-MM.md
[ 도구 실패 ]      ─► PostToolUseFailure    ─► log-tool-failure.sh ─► redact ─► YYYY-MM.md
[ 세션 종료 ]      ─► Stop (async)          ─► log-reflection.sh ─► codex exec ─► reflections-YYYY-MM.md (YAML 블록)
                                                                │
                     (실패 시) ──────► .errors.log
                                                                │
                                                                ▼
                                                     /reflect-digest (주간 집계, 승격 후보 제안)
                                                                │
                                                                ▼
                                                     /reflect-promote (승격 반영 + ledger)
                                                                │
                                                                ▼
                                                     /reflect-kaizen (품질 스팟체크 + calibration)
```

## YAML 스키마 (정본)

`reflections-YYYY-MM.md` 각 타임스탬프 헤더(`## <ISO8601+TZ>`) 아래 여러 YAML 블록이 올 수 있다. `no issues` 한 줄이면 블록 없음.

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

## Surface Precedence Table

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

### 임계값은 hypothesis

`freq == 2`, `freq == 3` 기준은 **초기 hypothesis**. 30일 운영 후 pre/post 재발률로 calibration 한다.

- Claude 공식 권고: "같은 실수 2번째 → CLAUDE.md"
- 현재 표는 "2회 → memory, 3회 → CLAUDE.md"로 한 단 낮게 설정 (과잉제약 부작용 배제 우선)
- `/reflect-kaizen` 스킬이 월 1회 calibration 수행 → 임계값 조정 제안

### CLAUDE.md 용량 예산

- 공식 권고: 200줄 이하
- 초과 예상 시 `.claude/rules/<tag>.md` (path-scoped, 특정 파일 편집 시만 로드) 또는 skill 로 스필오버
- digest가 현재 `CLAUDE.md` 줄 수를 측정해 스필오버 필요성 플래그

## Promotion Ledger 스키마

경로: `~/.claude/logs/<project_id>/promotions-ledger.md`

`/reflect-promote`가 승격마다 한 엔트리 append. 30일 뒤 `/reflect-digest` 또는 `/reflect-kaizen`이 `post_freq`를 채움.

```yaml
- rule_id: <UUID>                       # 고유 ID (uuidgen, 예: a1b2c3d4-xxxx-xxxx-xxxx-xxxxxxxxxxxx)
  mistake_tag: <tag>
  promoted_to: project_claude_md | project_memory | global_claude_md | global_memory | skill | path_scoped_rule | hook
  target_path: <실제 수정된 파일 경로>
  promoted_at: <ISO8601 with TZ>
  source_evidence:
    - path: ~/.claude/logs/<id>/reflections-YYYY-MM.md
      anchor: <타임스탬프 헤더>
  initial_freq: <int>
  calibration_window_days: 30
  post_freq: <int>                      # 30일 뒤 업데이트
  status: active | demoted | removed
  demotion_reason: <str>                # 강등 시만
```

### Regression 측정 규칙
- `promoted_at + calibration_window_days` 시점에서 같은 `mistake_tag` 재발 횟수를 `post_freq`에 기록.
- `post_freq == 0` AND `risk_class == low` → `status: demoted` 후보 표시 (과잉제약일 수 있음).
- `post_freq >= initial_freq` → 규칙이 효과 없음 → 프롬프트 재작성 또는 surface 변경 후보.
- `post_freq < initial_freq` → 효과 있음, 유지.

## 분류 품질 자동화 (reflect-kaizen 계획)

### 1. LLM-as-judge 월간 스팟체크
- 월 1회, 최근 reflections 중 랜덤 10건을 다른 LLM(Haiku 또는 codex 다른 모델)에 재분류 요청
- 원 분류 vs 재분류 일치도 측정
- 일치도 < 70% → Stop 훅 프롬프트 개선 신호, `/reflect-kaizen`이 프롬프트 diff 제안

### 2. 재발률 역추적 (ledger 기반)
- 승격 규칙의 `post_freq`로 간접 품질 측정
- 자주 재발하는 규칙 = 분류/규칙 작성 품질 낮음
- `/reflect-kaizen`이 리포트

### 3. Self-consistency (선택)
- 비싸므로 초기 버전에 포함하지 않음. 필요 시 추가.

## 수집 측면: raw prompt redaction 정책

**정책 결정 (Q1 = A)**: 저장은 계속 하되, 민감 패턴 자동 치환.

`_lib-redact.sh`의 `redact_sensitive()`가 치환하는 패턴:
- Anthropic: `sk-ant-...` → `[REDACTED-ANTHROPIC-KEY]`
- OpenAI: `sk-proj-...`, `sk-...` → `[REDACTED-OPENAI-KEY]` / `[REDACTED-API-KEY]`
- GitHub: `ghp_`, `gho_`, `ghu_`, `ghs_`, `ghr_`, `github_pat_` → `[REDACTED-GH-*]`
- Slack: `xoxb-`, `xoxa-` → `[REDACTED-SLACK]`
- AWS: `AKIA[A-Z0-9]{16}` → `[REDACTED-AWS-ACCESS-KEY]`
- Google: `AIza...` → `[REDACTED-GOOGLE-KEY]`
- JWT: `eyJ...` → `[REDACTED-JWT]`
- Bearer: `Bearer <20+자>` → `Bearer [REDACTED]`
- Env 대입: `*_KEY=`, `*_TOKEN=`, `*_SECRET=`, `*_PASSWORD=` → `...=[REDACTED]`
- Private key 블록: `-----BEGIN ... PRIVATE KEY-----` ~ `-----END ... -----` → 블록 전체 제거

### 보존 정책
- **누적** (이번 세션 결정). 자동 삭제/압축 없음. 월간 파일은 계속 append.
- 향후 용량 문제 발생 시 retention policy 추가 논의.

## 에러 관측성 (.errors.log)

`log-reflection.sh`는 실패 시 `.errors.log`에 사유 태그:
- `skip:cli-missing` — codex CLI 없음
- `skip:transcript-path-empty` — stdin에 transcript_path 없음
- `skip:transcript-file-missing path=<>` — 파일 없음
- `skip:transcript-too-short lines=<N>` — 10줄 미만
- `skip:transcript-empty-after-tail` — tail 결과 빈 값
- `fail:codex-exit-<N> session=<>` — codex exec 비정상 종료
- `fail:codex-empty-output session=<>` — codex 빈 응답

`/reflect-digest`가 `.errors.log`를 읽어 훅 실패 요약도 리포트에 포함.

## Codex 리서치 요약 (설계 근거)

2026-04-16 Codex 리서치 2회 결과 반영.

### 리서치 #1 (방법론/surface)
- 개인 사용자 레벨 실용축: `Reflexion + Self-Refine + 얇은 Constitutional rubric`
- DPO/KTO는 파인튜닝 전제라 직접 적용 불가
- `CLAUDE.md` 200줄 권장, path-scoped rules 활용
- 스킬은 설명만 상시 노출 / 본문은 invoke 시 로드 → 장문 절차 적합
- hooks는 `command`뿐 아니라 `prompt hook`, `agent hook`도 지원 — LLM 분류기 훅 가능
- 참고: https://arxiv.org/abs/2303.11366, https://arxiv.org/abs/2303.17651, https://code.claude.com/docs/en/memory, https://code.claude.com/docs/en/skills, https://code.claude.com/docs/en/hooks
- 5축 스코어 25/25

### 리서치 #2 (adversarial audit)
- blocker: raw 로그 PII (Q1=A redaction으로 해결)
- major: basename 충돌 (project_id 해시화로 해결)
- major: category 단일 라벨 (primary + also_applies로 해결)
- major: surface 단일 필드 (4축 분해로 해결)
- major: codex exec 실패 은폐 (.errors.log로 해결)
- major: 임계값 근거 (hypothesis 마킹 + kaizen calibration으로 해결)
- major: regression ledger (promotions-ledger.md 스키마로 해결)
- minor: CLAUDE.md 용량 예산 (200줄 + path-scoped 스필오버로 해결)
- 5축 스코어 24/25

전문: `~/.claude/codex-research-log/2026-04.md`

## 핵심 설계 결정 요약

| # | 결정 | 근거 |
|---|---|---|
| 1 | kit 이름 `reflect-kit` | Reflexion 논문 + 한국어 "성찰" 뉘앙스 + joo6077-plugins 네이밍 컨벤션 |
| 2 | raw 저장 유지 + redaction | 사용자 Q1=A. 편의성 유지 + 위험 축소 |
| 3 | project_id = Hybrid (`<basename>` 기본 + 충돌 시 `-<hash6>` fallback) | **v0.3.0 전환**. 운영 데이터 상 basename 충돌 0건 — 상시 해시는 over-engineered. 독립 리뷰로 backward-compatible Hybrid 선정 (아래 상세) |
| 4 | 카테고리 multi-label | 상호배타 아님 (Codex audit major) |
| 5 | Surface 4축 분해 + precedence | 단일 필드 압축 불가 (Codex audit major) |
| 6 | 임계값 hypothesis 마킹 | Claude 공식 권고(2회→CLAUDE.md)와 불일치, 운영 데이터 부재 |
| 7 | Stop 훅 async + .errors.log | 관측성 vs 흐름 차단 균형 (Codex audit major) |
| 8 | codex exec 사용 (API key 불필요) | 사용자 지적 — 기존 인증 재사용 |
| 9 | 성공 사례 수집 보류 | ROI 낮음, ledger로 간접 측정 대체 |
| 10 | 보존 정책 = 누적 | 사용자 결정. 용량 이슈 발생 시 재논의 |

## 결정 #3 상세 — Hybrid project_id (v0.3.0 전환)

### 배경

v0.1.0~v0.2.0 은 `project_id = <basename>-<6자 md5 hex>` 를 상시 적용했다. 이유는 Codex adversarial audit 의 major 지적("basename 충돌 위험"). 이론적 근거로 hash 를 붙였지만 운영 데이터에서는 정당성이 떨어졌다.

### 독립 리뷰 결과 (2026-04-17, general-purpose opus)

- **A안 (v0.2.0 현행 유지)**: 부적합. RESEARCH.md 근거는 이론이며 운영 데이터로 입증되지 않음. 7개 프로젝트 중 basename 충돌 0건. 레거시 버킷(해시 없는 디렉토리) 존재 자체가 "규칙 무결성이 이미 깨진" 증거.
- **B안 (basename only)**: UX 최고(사용자 인지 가능한 id)지만 breaking change. 기존 hash 디렉토리 강제 마이그레이션 필요.
- **C안 (Hybrid, backward-compatible)**: **선정**. basename 기본 + 충돌 감지 fallback + 기존 hash read 지원. UX 개선 + 안전장치 + 데이터 이동 0건.

### Hybrid 동작

| 상황 | 반환 id | 추가 동작 |
|------|---------|-----------|
| 첫 write, basename 디렉토리 없음 | `<basename>` | bucket 생성 + `.project-root` 마커에 git root 기록 |
| 재호출, 마커가 자기 repo 와 일치 | `<basename>` | no-op |
| 다른 git root 가 같은 basename 으로 호출 | `<basename>-<hash6>` | stderr 1회 경고 (PID 기반 마커로 중복 억제) |
| 기존 v0.2.0 hash 디렉토리 read | glob union | `normalize_project_query` 로 `<basename>` + `<basename>-<hash6>` 둘 다 스캔 |

### Backward-compat 보증

- 기존 `<basename>-<hash6>` 디렉토리는 read 경로에서 glob union 으로 그대로 포함
- `/reflect-digest project=<basename>` 과 `/reflect-digest project=<basename>-<hash6>` 은 동일 결과
- 마이그레이션 스크립트 실행 불필요 — 데이터 이동 0건
- 사용자는 별도 action 없이 v0.2.0 → v0.3.0 자동 전환

### 왜 마커 파일(`.project-root`)인가

- 디렉토리 이름만으로는 "같은 basename 에 다른 repo" 구분 불가
- 마커는 bucket 생성 시 1회 write, 이후 stat + cat 만으로 충돌 감지 가능
- read 경로에서도 side-effect 가 자기 bucket 에 한정 (외부 bucket 건드리지 않음)

### 한계와 미지 영역

- `.project-root` 마커 없이 생성된 v0.2.0 디렉토리는 "충돌 없는" 것으로 간주 (read 에서만 glob union 포함)
- 같은 basename 의 다른 repo 가 매우 짧은 시간 내 동시에 write 할 때 race condition 가능 (마커 생성 전) — 개인 스케일에서는 무시 가능
