# reflect-kit

개인 Claude Code 사용자의 대화 피드백 → 학습 → 재주입 파이프라인 kit.

Reflexion 방법론(arXiv [2303.11366](https://arxiv.org/abs/2303.11366))을 개인 레벨에 적용한다. 세션 중 발생한 오해·반복 실수·잘못된 접근을 구조화 로그로 수집하고, 빈도·위험도·절차성 기준으로 Claude Code의 여러 surface(CLAUDE.md / memory / skill / hook)에 승격 반영한다. 승격된 규칙은 30일 pre/post 재발률로 효과를 측정한다.

버전: `0.3.0`

## v0.3.0 변경 요약

- **Hybrid project_id** — `<basename>` 기본 + 충돌 감지 시 `<basename>-<hash6>` fallback. 기존 `<hash6>` 디렉토리는 read 에서 glob union 으로 그대로 포함 (마이그레이션 불필요, 데이터 이동 0건)
- **정규화 쿼리** — `/reflect-digest project=<basename>` 와 `/reflect-digest project=<basename>-<hash6>` 가 동일 결과 반환 (`normalize_project_query` 헬퍼)
- **내부 디렉토리 제외** — `_cron`, dot/underscore-prefix 디렉토리(예: install-scheduler 로그)를 project bucket 순회에서 자동 제외 (`is_internal_logs_dir` 필터)
- **충돌 1회 경고** — 동일 basename + 다른 git root 감지 시 stderr 경고는 단일 프로세스에서 1회만 (PID 기반 마커)
- **docs/DESIGN.md** — 결정 #3 Hybrid 전환 근거 상세 기록 (독립 리뷰 A/B/C안 비교, backward-compat 보증)

## 목적

- Claude가 반복하는 같은 실수를 줄인다
- 사용자 의도 오해 패턴을 식별해 교정한다
- 비효율적·엉뚱한 접근 방법이 쌓이는 것을 막는다
- 위 과정을 **수동 개입 없이** 자동으로 돌리고, 사용자는 월 1회 digest + 승격 승인만 하면 된다

## 비-목표 (이 kit이 다루지 않는 것)

- QA / Sprint Contract / Evaluator 인프라 개선 — `harness` kit 담당
- 코드 품질 감사 — 각 언어 toolkit(`flutter-toolkit`, `rust-kit`)의 audit 담당
- 디자인 리뷰 — `design-kit` 담당
- LangSmith급 엔터프라이즈 관측 — 개인 사용자 스케일 유지

## 스킬

<!-- AUTO:skills -->
| 스킬 | 설명 |
|------|------|
| `codex-kaizen` | Codex 위임 방법론과 전역 프롬프트 템플릿(~/.claude/codex-prompt-template.md)을 |
| `reflect-digest` | ~/.claude/logs/<project_id>/reflections-*.md 에 쌓인 구조화 YAML 블록을 읽어 |
| `reflect-kaizen` | reflect-kit 파이프라인 자체의 품질을 월 1회 측정·보정한다. |
| `reflect-promote` | /reflect-digest가 낸 승격 후보를 실제 Claude Code surface(project CLAUDE.md, project memory, |
<!-- /AUTO:skills -->

## 에이전트

<!-- AUTO:agents -->
| 에이전트 | 설명 |
|----------|------|
| (없음) | 초기 버전은 스킬만으로 충분. 분류/평가 에이전트(reflection-analyst)는 향후 추가 여지 |
<!-- /AUTO:agents -->

## 훅

<!-- AUTO:hooks -->
| 이벤트 | 실행 | 설명 |
|--------|------|------|
| `UserPromptSubmit` | `log-prompt.sh` | UserPromptSubmit |
| `PostToolUseFailure` | `log-tool-failure.sh` | PostToolUseFailure |
| `Stop` | `log-reflection.sh` | Stop |
<!-- /AUTO:hooks -->

## 데이터 플로우

```text
[ 사용자 프롬프트 ] → UserPromptSubmit → log-prompt.sh → redact → YYYY-MM.md
[ 도구 실패 ]     → PostToolUseFailure → log-tool-failure.sh → redact → YYYY-MM.md
[ 세션 종료 ]     → Stop (nohup 백그라운드) → log-reflection.sh → codex → reflections-YYYY-MM.md
                                          (실패 시) → .errors.log
                                                      │
                                                      ▼
                                          /reflect-digest (집계 + 승격 후보)
                                                      │
                                                      ▼
                                          /reflect-promote (반영 + ledger)
                                                      │
                                                      ▼
                                          /reflect-kaizen (품질 스팟체크 + calibration)
```

## 로그 경로

```text
~/.claude/logs/<project_id>/
├── YYYY-MM.md                  # raw prompt + tool-failure
├── reflections-YYYY-MM.md      # Stop 훅 구조화 YAML
├── .errors.log                 # 훅 실패 메타 로그 + 환경 오설정 억제 기록
├── .env-issues.tsv             # 환경 오설정 롤업 (tag / first_seen / last_seen / count)
├── digest-YYYY-MM-DD.md        # /reflect-digest 리포트 (옵션 저장)
└── promotions-ledger.md        # /reflect-promote 승격 이력
```

`.env-issues.tsv` 는 Stop 훅의 dedup 게이트가 억제한 `actionability: user_environment` 사건의
**유일한 누적 근거**다. 억제된 사건은 `reflections-*.md` 본문에 없으므로 이 파일을 지우면 규모를
알 수 없게 된다. 억제 창은 `REFLECT_ENV_REPEAT_DAYS` (기본 7일) 로 조정한다.

`project_id` = `<basename(git-root)>` (Hybrid 기본, v0.3.0+) / 충돌 시 `<basename>-<6자 md5 hex>` fallback. 헬퍼: `hooks/_lib-project-id.sh` — `compute_project_id` (쓰기용), `normalize_project_query` (읽기용 glob 확장).

## 의존성

- `codex` CLI (`codex exec`로 세션 분석)
- `jq` (JSON 파싱)
- `awk`, `sed` (redaction, POSIX ERE)
- `uuidgen` (rule_id 발급)
- Claude Code v2.1.59+ (auto-memory)

## 설치

```bash
claude plugin marketplace add github:joo6077/claude-plugins
claude plugin install reflect-kit@joo6077-plugins
```

설치 후 `~/.claude/settings.json`에서 `enabledPlugins`를 확인:

```json
{
  "enabledPlugins": {
    "reflect-kit@joo6077-plugins": true
  }
}
```

## 설치 후 흐름

1. 사용자 프롬프트 입력 → `log-prompt.sh` 가 raw 기록 (민감 패턴 redaction 적용)
2. 도구 실패 발생 → `log-tool-failure.sh` 기록
3. 세션 종료 → `log-reflection.sh` 가 stdin을 tmp 파일에 저장 후 nohup 백그라운드로 자기 자신 재호출 (체감 지연 0) → codex가 transcript 분석 → `reflections-YYYY-MM.md`에 YAML 블록 append
4. 사용자가 `/reflect-digest` 호출 → 주간 리포트 + 승격 후보
5. 사용자가 `/reflect-promote` 호출 → 후보 승인 → 실제 surface 반영 + ledger 기록
6. 월 1회 `/reflect-kaizen` → 분류 품질 스팟체크 + 임계값 calibration

## Scheduling (v0.2.0+)

`/reflect-digest` 와 `/reflect-kaizen` 은 수동 실행이 기본이지만, 주 1회 digest + 월 1회 kaizen 은 자동화하는 것이 권장된다. 세 가지 방식 지원:

### 방식 1: `/schedule` 슬래시 명령 (Claude Code remote trigger)

```text
/schedule create "reflect-digest-weekly" "0 9 * * 1" "/reflect-digest period=7d"
/schedule create "reflect-kaizen-monthly" "0 9 1 * *" "/reflect-kaizen window=30d"
```

매주 월요일 09:00 → 주간 digest. 매월 1일 09:00 → 월간 kaizen.

### 방식 2: 로컬 crontab 직접 등록

```bash
# crontab -e
0 9 * * 1  claude exec "/reflect-digest period=7d" > ~/.claude/logs/_cron/digest-$(date +\%Y\%m\%d).log 2>&1
0 9 1 * *  claude exec "/reflect-kaizen window=30d" > ~/.claude/logs/_cron/kaizen-$(date +\%Y\%m\%d).log 2>&1
```

### 방식 3: `scripts/install-scheduler.sh` (로컬 crontab 자동 등록)

```bash
# 등록 예정 cron 라인 미리보기 (crontab 변경 없음)
bash ${CLAUDE_PLUGIN_ROOT}/scripts/install-scheduler.sh --dry-run

# crontab에 주간+월간 2개 라인 추가 (멱등 — 중복 등록 방지)
bash ${CLAUDE_PLUGIN_ROOT}/scripts/install-scheduler.sh --install

# 등록된 reflect-kit 항목 제거
bash ${CLAUDE_PLUGIN_ROOT}/scripts/install-scheduler.sh --uninstall
```

## 원칙

- **Reflexion 구조가 근간** — 실패 경험을 언어적 반성으로 저장 후 재주입
- **다차원 Surface 결정** — scope × risk × procedurality × enforcement × frequency 로 판정
- **임계값은 calibration** — freq 2/3 는 hypothesis. 30일 운영 후 pre/post 재발률로 조정
- **닫힌 사이클** — 수집 훅 3 → digest → promote → kaizen → ledger → digest
- **raw 저장 + redaction** — 편의성과 보안의 균형

## 문서

- `docs/DESIGN.md` — 데이터 플로우, Precedence Table, Ledger 스키마, 설계 결정 요약
- `docs/RESEARCH.md` — 설계 근거가 된 Codex 리서치 2회분 (방법론 비교 + adversarial audit)
- `docs/SCHEMA.md` — YAML + Ledger 스키마 정본

## 관련 kit

- **harness** — Sprint Contract / QA Evaluator 자체 품질. reflect-kit과 도메인 분리
- **flutter-toolkit / rust-kit** — 언어별 코드 품질. audit 로직이 reflect-kit과 구분됨
- **design-kit** — UI/UX 원칙 감사. reflect-kit과 surface 공유 가능(향후)

## Phase 12 kaizen (2026-05-07, 첫 사이클)

- 카이젠 오케스트레이터 Phase 12 신규 추가 — reflect-kit 이 처음으로 정식 카이젠 대상에 포함됨
- Phase 1 v1.3.0 신규 원칙 흡수 — `/insights` Friction #1·#2·#3 의 reflect-kit 측 reframe
- 적용 매핑은 **harness/references/cross-kit-principles.md** reflect-kit 열 참조
- 핵심 매핑: reflect-digest 의 카테고리별 집계 ↔ Pre-Edit Batch Audit (enumerate), 3 훅 자체 ↔ Hook-Triggered Auto-Correction (Stop/UserPromptSubmit/PostToolUseFailure), reflect-kit 도메인 자체 ↔ **Session Lifecycle 카테고리** (skill-design-guide §2 의 10 번째 유형)
