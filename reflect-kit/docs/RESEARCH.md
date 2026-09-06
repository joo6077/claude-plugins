# reflect-kit — RESEARCH (근거 자료)

2026-04-16 세션에서 수행한 Codex 리서치 2회분 통합. 플러그인 구현 시 설계 결정 근거로 직접 참조.

원문 전체는 `~/.claude/codex-research-log/2026-04.md` 에 타임스탬프별로 보존되어 있다. 이 파일은 reflect-kit 에 직접 관련된 부분만 추출한 요약본.

---

## 리서치 #1 — 방법론·surface·탐지·측정 (2026-04-16T18:14)

### Task
개인 개발자가 Claude Code(CLI + plugins)를 장기 사용하며 AI 오해/실수를 줄이고 의도 파악을 개선하는 피드백 수집→분석→재주입 파이프라인의 모범 사례(방법론/surface/탐지/측정/공개사례/워크플로우) 리서치. read-only.

### 결과 (5축 25/25)

#### 1. 방법론 비교 (개인 사용자 레벨 적용성)

| 방법론 | 개인 적용성 | 난이도 | 기대 효과 | Claude Code식 구현 해석 | 출처 |
|---|---|---:|---:|---|---|
| **Reflexion** | 높음 | 중 | 높음 | 실패/교정 로그를 "언어적 반성 + 에피소드 메모리"로 저장하고 다음 세션에 재주입. reflect-kit 수집 레이어와 1:1 매칭 | https://arxiv.org/abs/2303.11366 |
| **Self-Refine** | 높음 | 낮음~중 | 중 | 세션 종료 요약, 실패 요약, 규칙 초안 생성. "초안→자기비평→개선안"을 훅/배치로 돌리기 쉬움 | https://arxiv.org/abs/2303.17651 |
| CoVe | 중 | 중 | 중~높음 | 사실성/외부근거/체크리스트 검증에 강함. 반복 실수 교정엔 과함 | https://arxiv.org/abs/2309.11495 |
| Constitutional AI self-critique | 중~높음 | 낮음 | 중 | 개인용 "헌법"을 CLAUDE.md/skill rubric로 두고 자기비평. 현실적 | https://arxiv.org/abs/2212.08073 |
| Self-Consistency | 중 | 중~높음 | 중 | 다수결/합의. 비용 큼, 기본축엔 비효율 | https://arxiv.org/abs/2203.11171 |
| DSPy | 낮음~중 | 높음 | 중 | 외부 분석기/분류기 파이프라인 용. Claude 주입 표면엔 부적합 | https://dspy.ai/ |
| DPO | 매우 낮음 | 매우 높음 | 직접 효과 낮음 | 파인튜닝 전제. 선호쌍 데이터셋 아이디어만 차용 가능 | https://openreview.net/forum?id=HPuSIXJaa9 |
| KTO | 매우 낮음 | 매우 높음 | 직접 효과 낮음 | 파인튜닝 전제. "좋음/나쁨 이진 라벨" 운영 방식만 차용 | https://openreview.net/forum?id=iUwHnoENnl |

**추론**: 개인 사용자 레벨 실용축은 `Reflexion + Self-Refine + 얇은 Constitutional rubric + 제한적 CoVe`. DPO/KTO 는 학습법이라 직접 적용 불가.

→ **reflect-kit 설계 반영**: Reflexion 구조가 근간. `/reflect-kaizen` 에 Self-Refine 적용 (초안→자기비평→개선 프롬프트).

#### 2. Claude Code 주입 surface 공식 사실

- CLAUDE.md + auto memory 모두 매 대화 시작 로드. 둘 다 context 이지 enforced config 아님. https://code.claude.com/docs/en/memory
- CLAUDE.md 매 세션 전체 로드. auto memory 는 MEMORY.md 앞 200줄/25KB 만. https://code.claude.com/docs/en/memory
- 공식 권고: **"Claude가 같은 실수 2번째 → CLAUDE.md 에 추가"**. https://code.claude.com/docs/en/memory
- **path-scoped `.claude/rules/`** 는 특정 파일에만 로드 → 토큰 절약. https://code.claude.com/docs/en/memory
- skills: 설명만 상시 노출, 본문은 invoke 시 로드. 장문 절차에 적합. `disable-model-invocation:true` 로 수동 전용화 가능. https://code.claude.com/docs/en/skills
- subagents: 별도 context window + 전용 system prompt/tool 권한. https://code.claude.com/docs/en/subagents
- hooks: SessionStart, SessionEnd, UserPromptSubmit, PreToolUse, PostToolUse, Stop 지원. **command 뿐 아니라 `prompt hook`, `agent hook` 타입도 지원** → LLM 분류기/검증기를 훅에 직접 등록 가능. https://code.claude.com/docs/en/hooks
- slash commands 는 명시적 수동 인터페이스. 커스텀은 skills 로 통합됨. https://code.claude.com/docs/en/commands

→ **reflect-kit 설계 반영**: Stop 훅에 LLM 분석 삽입(`log-reflection.sh` 의 codex exec). 향후 `prompt hook`/`agent hook` 타입 활용 여지.

#### 3. Surface 선택 기준

| Surface | 토큰 비용 | 영향력 | 지속성 | 적용 지연 | 업데이트 비용 | 적합한 피드백 |
|---|---:|---:|---:|---:|---:|---|
| CLAUDE.md | 높음 | 높음 | 높음 | 즉시 | 중 | 항상 지켜야 할 규칙, 프로젝트 불변 규약 |
| auto memory | 중하 | 중 | 높음 | 즉시 | 매우 낮음 | 개인 선호, 자주 쓰는 명령, 디버깅 메모 |
| skills | 평시 매우 낮음 | 높음 | 높음 | 필요 시 | 중 | 다단계 절차, 체크리스트, 리뷰 플레이북 |
| agents | 평시 낮음 | 높음 | 높음 | 필요 시 | 중 | 특정 역할 검증기, reviewer, classifier |
| hooks | 평시 0에 가까움 | 매우 높음 | 높음 | 즉시(이벤트) | 중~높음 | 강제/차단/자동수집/자동주입 |
| slash commands | 평시 0에 가까움 | 낮음~중 | 높음 | 수동 즉시 | 낮음 | 명시적으로 돌리는 분석, 주간 집계 |

**결정 규칙**
- "항상 그래야 함" → CLAUDE.md 또는 hook
- "자주 도움되지만 치명적 아님" → auto memory
- "절차/검토 프롬프트" → skill
- "특정 역할 분리" → agent
- "사용자가 원할 때만" → slash command
- **"위반하면 안 됨"은 memory 가 아니라 hook 쪽**

→ **reflect-kit 설계 반영**: DESIGN.md 의 Surface Precedence Table.

#### 4. 권장 워크플로우

**주안**: `Reflexion형 로그 메모리 + Self-Refine형 주간 승격 + hook 기반 얇은 가드레일`

- 세션 종료 시 LLM 요약 생성
- 주 1회 배치에서 로그를 `mistake_tag / trigger / correction / preferred_surface / evidence_count` 로 집계
- 2회 반복 → auto memory 후보
- 3회 반복 또는 "항상 지켜야 함" → CLAUDE.md 또는 path-scoped rule
- 절차성 교정 → skill
- 위반 비용 큼 → hook
- 월 1회 kaizen 이 재발률 점수화 + 승격/강등 결정

**보조안 A (저비용)**: regex + sequence rule + 월간 top N 만 LLM. 단순.
**보조안 B (발견력)**: regex prefilter → embedding cluster → LLM classifier. 복잡.

→ **reflect-kit 설계 반영**: 주안 채택. 탐지 스택은 초기 "LLM 직접 분류(codex exec)" → 데이터 쌓이면 보조안 B 로 진화.

#### 5. 반복 실수 탐지 권장 스택

1. **키워드 매칭** (기본선): tool failure, "아니", "다시", "그 뜻이 아니고", "파일 경로", "권한"
2. **sequence pattern**: `실패 → 사용자 교정 → 재시도 성공` 2~4턴
3. **embedding clustering**: 같은 의미 다른 표현 묶기
4. **LLM 분류**: 클러스터 라벨링, surface 추천, contract 초안

**추론**: regex only = recall 낮음. LLM only = 비쌈. `regex/sequence prefilter + embedding cluster + LLM adjudication` 3단 조합이 현실적.

#### 6. 반영 후 효과 측정

- 태그별 재발률: `count / 100 sessions`, `count / 1k prompts`
- severity-weighted recurrence
- rule introduction date 기준 pre/post 비교
- 교정 후 동일 태그 재발까지 median sessions
- goldens: 로그에서 뽑은 대표 프롬프트 20~50개 월별 고정셋
- online + offline hybrid 권장. Cursor 사례: https://cursor.com/blog/cursorbench

→ **reflect-kit 설계 반영**: Promotion Ledger 의 `initial_freq / post_freq / calibration_window_days` 로 pre/post 자동화.

#### 7. 공개 사례 (벤치마크)

- **Claude Code 공식**: CLAUDE.md, auto memory, skills, subagents, hooks
- **Cursor**: Rules/Memories, Bugbot learned rules, hybrid online/offline eval
  - https://docs.cursor.com/context/rules
  - https://docs.cursor.com/en/context/memories
  - https://cursor.com/blog/bugbot-learning/
  - https://cursor.com/blog/cursorbench
- **Cline Memory Bank**: 구조화 문서 기반 지속 메모리. https://docs.cline.bot/features/memory-bank
- **Continue rules-memory**: https://docs.continue.dev/customize/deep-dives/rules
- **aider conventions**: 항상 읽는 규약 파일. https://aider.chat/docs/usage/conventions.html

→ **reflect-kit 포지셔닝**: Cursor 의 "learned rules + hybrid eval" 와 가장 가깝지만, Claude Code 고유의 **skills / subagents / hooks** 조합으로 차별화.

### 트레이드오프 (리서치 #1)

- CLAUDE.md 비대화 → adherence 저하. **200줄 이하 권장**.
- auto memory: 업데이트 비용 0에 가까우나 잘못된 습관 누적 리스크.
- skills: 토큰 효율 좋음, 그러나 "항상" 규칙엔 발동 지연 가능.
- hooks: 가장 강력, 잘못 설계 시 사용감 악화.
- LLM 분류: 정확, 비용/드리프트.
- embedding clustering: 신규 패턴 강점, 라벨링 필요.

### 열린 질문 (리서치 #1)

- Claude Code 버전이 auto memory 지원 (v2.1.59+) 인지?
- 로그 요약 포맷을 얼마나 구조화할지? (`mistake_tag/trigger/correction/surface/severity`)
- harness-kaizen 회귀 단위 (세션 vs 턴)?
- 프로젝트별 규칙 vs 사용자 전역 공통화 정책?
- codex CLI 에도 동일 taxonomy/regression harness 재사용?

→ 현재까지 답: 구조화 = YAML 스키마 (DESIGN.md); 프로젝트별 분리 기본 + 복수 프로젝트 교차 시 전역 승격 (Precedence #3); harness-kaizen 과 완전 분리.

---

## 리서치 #2 — adversarial design audit (2026-04-16T19:30)

### Task
초기 dialog-feedback 파이프라인 설계 (훅 3개 + digest 스킬)의 결함을 독립 평가자 관점에서 감사. read-only.

### 결과 (5축 24/25)

#### 발견된 결함 (severity + smallest safe fix)

| # | severity | 결함 | 해결 상태 |
|---|---|---|---|
| 1 | **blocker** | raw 로그 PII 유출 리스크 (prompt 전문, tool_input/response 전문 저장) | ✅ Q1=A: `_lib-redact.sh` 구현 |
| 2 | major | 프로젝트 분리 정책이 basename 식별자와 충돌 (같은 이름 다른 repo) | ✅ `<basename>-<hash6>` (`_lib-project-id.sh`) |
| 3 | major | category 4종 상호배타 아님 (단일 라벨 스키마) | ✅ `primary_category + also_applies` |
| 4 | major | surface 단일 필드 압축 (scope/risk/procedurality/enforcement 혼재) | ✅ 4축 분해 + Precedence Table |
| 5 | major | codex exec 실패 은폐 (내부 timeout 없음, exit code 미검사) | ✅ exit code 검사 + `.errors.log` 메타로깅 |
| 6 | major | 임계값 근거 부재 (2회/3회 고정, Claude 공식 "2회→CLAUDE.md"와 불일치) | ✅ hypothesis 마킹 + `/reflect-kaizen` 에서 30d calibration |
| 7 | major | regression ledger 부재 | ✅ `promotions-ledger.md` 스키마 (DESIGN.md) + `/reflect-promote` 에 위임 |
| 8 | minor | CLAUDE.md 200줄 spillover 정책 없음 | ✅ `.claude/rules/<tag>.md` path-scoped 스필오버 명시 |

#### 설계 강점 (유지)

- 수집 surface 를 `UserPromptSubmit raw / PostToolUseFailure / Stop session summary` 3채널로 분리 → 한 채널 실패가 전체 관측 차단 안 함.
- `misunderstandings-YYYY-MM.md` 를 별도 파일로 둠 → harness kaizen 과 혼동 방지 (`reflections-YYYY-MM.md` 로 rename 예정, 의도 유지).
- YAML 스키마에 `mistake_tag`, `tools_used`, `approach_note` 포함 → 교차 분석 가능.
- Stop 훅 async → 사용자 체감 지연 감소.

#### 놓친 관점 (후속 이슈)

- **보존 정책**: 삭제/압축/암호화/백업 범위 정의 없음 → **결정: 누적 (용량 이슈 시 재논의)**
- **성공 사례 미수집**: 효과 있는 가드레일 식별 어려움 → **결정: ledger post_freq 로 간접 측정 대체, 초기 보류**
- **분류 품질 관리**: 인간 감사 비율 정의 없음 → **결정: `/reflect-kaizen` 에 LLM-as-judge 월간 스팟체크 포함**
- **timezone 일관성**: local `date` 만 기록 → **해결: ISO8601+TZ (`%Y-%m-%dT%H:%M:%S%z`)**

#### 열린 질문 (리서치 #2)

- authoritative project identity (git root / remote URL / 절대경로 해시)? → **해결: git root 절대경로 md5 hex 6자**
- codex exec 가 훅 체인 재실행하는지 실제 검증 필요
- raw prompt 보존이 감사 요구인지 요약/해시로 충분한지? → **결정: 누적 + redaction**
- dialog-feedback-promote 승격 ledger/rollback 책임 → **`/reflect-promote` 스킬 담당 (미구현)**
- category 단일 라벨 유지 이유? → **multi-label 로 변경 완료**

### 교훈 (리서치 #2)

- Codex 에 "위임 직후 로그 append 지시" 를 프롬프트에 넣어도 read-only 모드에서는 무시됨. 로그 append 는 Claude 가 직접 수행하는 프로토콜로 운영.
- Codex adversarial diagnose 는 basename 충돌, raw PII 같이 **사람 친화적 설계가 낳는 구조적 결함** 을 정확히 잡음. 초기 설계 직후 반드시 1회 실행할 가치 있음.

---

## 두 리서치의 공통 결론

### 원칙
1. Reflexion 구조가 개인 사용자 레벨 개선 루프의 근간.
2. Surface 는 단일 차원이 아니라 `scope × risk × procedurality × enforcement × frequency` 다차원으로 결정.
3. 임계값은 사전 고정하지 말고 데이터로 calibrate.
4. 수집·분석·승격·측정을 하나의 사이클로 닫아야 효과 있음.

### reflect-kit 핵심 설계 반영도
| 원칙 | 구현 위치 |
|---|---|
| Reflexion 구조 | 전체 파이프라인 |
| 다차원 Surface 결정 | DESIGN.md Precedence Table |
| 임계값 calibration | `/reflect-kaizen` (미구현) + 임계값에 hypothesis 표기 |
| 닫힌 사이클 | 수집 훅 3 → digest → promote → kaizen → ledger → digest |

### 플러그인 구현 시 먼저 봐야 할 곳
1. 이 파일 (RESEARCH.md) — 설계 근거
2. DESIGN.md — 스키마 정본, precedence, ledger 스키마
3. MIGRATION.md — 파일 이동 + 이름 변경 체크리스트
4. 원문: `~/.claude/codex-research-log/2026-04.md` (전체 5축 점수/로그 포함)
