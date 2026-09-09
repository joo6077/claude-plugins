# Sprint Feedback
Feature: harness 아키타입 12 신설 · 미변경 조건 오라클 규칙
Evaluated: 2026-09-09 15:30
Verdict: APPROVE
Iteration: 1

## Contract Fingerprint
- path: /Users/jackson/Hub/10_Dev/claude-plugins/.harness/sprint-contract-harness-archetype12-unchanged-oracle.md
- sha256(full file): 4cf89b3a13447dd2a15ee24ca297b308556efe70bea591311317d6b0ddba57e8
- status: active
- slug: harness-archetype12-unchanged-oracle
- contract_root: /Users/jackson/Hub/10_Dev/claude-plugins
- contract_root_unconfigured: false
- 선택 근거: ladder 1 (명시경로, 사용자 지정) — 세션소유(owner_session=CLAUDE_CODE_SESSION_ID)로도 일치 확인
- legacy_contract_used: false
- seal_status: SEAL_OK (conditions_digest sha256:c335ef27bcb4405e == contract_digest 실측값)
- contract_seal_broken: n/a
- 재확인(Step 5): 일치 (저장 직전 재계산 동일 해시)
- status_transition: active -> done (APPROVE 확정 후 전환)

## Amendments
- amendments: 2 (사이드카 `sprint-amendments-harness-archetype12-unchanged-oracle.md`)
- AM-01 (AR-04 대상): direction=relaxing(계산값, 자기신고 아님) · consent=anchored → **PASS 근거 가능**
  - 계산 재현(zsh·bash 양쪽 직접 실행): `amend_direction a_orig.txt a_new.txt` → `relaxing added=1 removed=0` — 사이드카 기재값과 동일
  - 헬퍼 선택 검증: AR-04의 pathspec은 "git diff 스캔 대상을 좁혀 위반을 더 많이/적게 잡는" 측정 집합이 아니라, "전체 diff가 반드시 이 안에 있어야 한다"는 **허용 집합**(포함관계 제약)이다. pathspec을 넓히면 포함관계 제약이 완화되어 통과하는 구현 집합이 늘어난다 — `amend_direction`(허용 집합 헬퍼) 선택이 맞다. `amend_direction_oracle`(측정 집합 헬퍼)을 실측 결과 집합(13→15파일, added=2/removed=0)에 적용하면 "narrowing"으로 **반전**되는 것을 직접 확인했다 — 이는 AR-04가 측정-집합형이 아니라 허용-집합형 조건이라는 사실을 방증한다.
  - 앵커: timestamp/session/cwd 3요소 기재 확인. reflect-kit prompt-log(`~/.claude/logs/claude-plugins/2026-09.md`)에서 세션 `4d264694-...`의 09-09 13:16~15:21 구간을 직접 열람했으나 15:07:15 시각의 매칭 프롬프트 엔트리는 없었다 — 사용자 승인이 AskUserQuestion류 구조화 응답으로 이뤄져 log-prompt 훅(UserPromptSubmit 전용)이 포착하지 못한 것으로 추정된다. 3요소 형식 요건은 충족하므로 anchored로 판정하되, 로그 직접 대조는 불가했음을 기록한다.
- AR-03: amendment 없음 — 오라클 원문 유지, 대상(오탐 원인) 수정으로 처리. 아래 Results/AR-03 참조.

## User Correction Audit
- correction_log_status: available (`~/.claude/logs/claude-plugins/2026-09.md`)
- unreflected_corrections: 0 (세션 4d264694, 스프린트 윈도우 2026-09-09 13:16~15:21 내 프롬프트는 킥오프 1건 "백로그 진행해"뿐. 중간 교정 프롬프트 없음)
- verdict 영향: 없음 (표면화 전용)

## Results

### Skill (4/4)
- [x] SK-01: §2 표에 12행 `절차 안내형` 추가 — PASS
  - 근거: `harness/docs/guides/skill-design-guide.md` §2 블록(awk 플래그형 추출) 내 `grep -cE '^\| 12 \|.*절차 안내형'` = 1 (측정값: 1, 기준: ==1). L3: 표 12행 실제 문구 확인(`| 12 | **절차 안내형** | 사람이 외부 UI·콘솔을... | howto, setup-guide |`)
- [x] SK-02: §2 블록에 출처구분(1~9/10~12)+12번 근거(howto-kit/setup-guide) — PASS
  - 근거: 같은 블록에서 `1~9`=1회, `10~12`=1회, `howto-kit|setup-guide`=3회. L3: 실제 문장 확인 — "1~9는 Anthropic 공식 분석 패턴, 10~12는 본 레포 운영 경험에서 추가" + "howto, howto-doc, howto-audit... setup-guide"
- [x] SK-03: §2 헤더에서 개수 리터럴 제거 — PASS
  - 근거: `grep -cE '^## 2\..*[0-9]+ ?가지'` = 0 (기준: ==0), `grep -c '^## 2\. 스킬 유형 체크리스트'` = 1 (기준: ==1)
- [x] SK-04: 12번 유형의 구별되는 실패 모드(입도 부족→날조) 명시 — PASS
  - 근거: §2 블록에 `날조|지어내` = 1회 (기준: >=1). L3: "유형 12는 **입도 부족을 날조로 메우는 것**이 고유 실패다... 모델은 확인하지 않은 메뉴 이름과 클릭 경로를 지어내서 요구를 충족시킨다"

### Script (2/2)
- [x] SC-01: CI validate 8종 exit 0 — PASS (직접 실행, 표)
  | 명령 | exit |
  |---|---|
  | validate-plugin.py | 0 |
  | sync-evals.py --check-only | 0 |
  | sync-docs.py --check-only | 0 |
  | sync-orchestrator.py --check-only | 0 |
  | run-evals.py --verbose (106 passed) | 0 |
  | check-contrast-claims.py | 0 |
  | check-docs-links.py (내부링크 357개, 깨진 링크 0) | 0 |
  | check-stale-values.py (등록값 15개, 되살아난 값 0) | 0 |
- [x] SC-02: `save-test.sh` exit 0 (음성대조 3건 포함) — PASS
  - 근거: 직접 실행 결과 "=== ALL TESTS PASSED ===", negative tests 3건(invalid YAML/incomplete YAML/non-existent file) 전부 PASS

### Error (4/4)
- [x] ER-01: §측정 명령 타당성에 (4)항 신설 — PASS
  - 근거: 절 블록(awk 플래그형 추출, 183줄) 내 `grep -cE '^\*\*\(4\)'` = 1
- [x] ER-02: #37 실측 근거 인용 — PASS
  - 근거: 같은 블록에 `v5\.`=3회, `#37`=1회(`329e47c` 도 별도 등장)
- [x] ER-03: 대체 oracle이 실행 가능한 명령 형태(선언 라인 한정) — PASS
  - 근거: 같은 블록에 `git diff` 포함 백틱 명령 11개, 그 중 `git diff <base>..HEAD -- <file> | grep -E '^[+-]현재: \*\*v5\.'` 형태로 선언 라인 한정 확인 (line 67)
- [x] ER-04: awk 범위형 퇴화 규칙 + 실측 수치(1 vs 9) — PASS
  - 근거: 같은 블록에 `awk` 토큰 5회, `출력: \`1\`` / `출력: \`9\`` 각 1회. **직접 재현**: `awk '/^## .../,/^## /' howto-kit/README.md | wc -l` → 1, `awk '/^## .../{f=1;print;next} f&&/^## /{exit} f' howto-kit/README.md | wc -l` → 9. zsh·bash 양쪽 동일 재현 확인

### Architecture (4/4)
- [x] AR-01: 아키타입 개수 리터럴 레포 활성 표면 0건 — PASS [goal, 다관점]
  - 측정값: 검사 범위 802파일 (기준: >0, 무효 아님) / 히트 7건 → 전부 개별 확인 결과 아키타입과 무관(다크패턴 12가지, 전자상거래법 6가지, 영구/일시/접힘 3가지, Material Design 3·4가지, 모호성 3가지 유형) — 지정 오라클(`grep -nE '[0-9]+ ?가지 (아키타입|스킬 유형|유형)'`) 기준 0건 확인
  - 다관점 추가탐색(구현자 제외 패턴을 그대로 믿지 않음): `[0-9]+(가지|종|개) ?(의)? ?아키타입` 및 `...스킬 ?(유형|타입)` 광의 패턴도 0건. `아키타입` 전체 언급 26곳을 개별 열람 — 전부 카탈로그 참조/컬럼 헤더이며 잔존 카운트 리터럴 없음
  - 예외적으로 발견한 경계 사례 2건(FAIL 아님, Improvement 기재): `docs/howto/design-brief.md:331`("문서 제목은 9가지이나 표는 11행") · `docs/superpowers/specs/2026-08-31-tone-kit-migration.md:22`("9유형|11유형") — 둘 다 지정 정규식과 형태가 달라 매치되지 않았고, 내용 확인 결과 **과거 시점 조사기록/의사결정 문서의 스냅샷 서술**(각각 2026-09-07, 2026-08-31 시점 상태를 기술)로 `.harness/` 이력과 같은 성격 — 라이브 소비면이 아니므로 AR-01의 "드리프트 재발 방지" 취지 밖으로 판단해 FAIL 처리하지 않음
- [x] AR-02: producer — §2 표 12행 — PASS
  - 근거: `grep -cE '^\| [0-9]+ \|'` = 12 (표 전체 1~12 행 직접 확인)
- [x] AR-03: consumer 7개 파일 개별 갱신 — PASS (전수 개별 확인, 표)
  | 파일 | count |
  |---|---|
  | CLAUDE.md | 0 |
  | harness/skills/create-skill/SKILL.md | 0 |
  | harness/evals/evals.json | 0 |
  | flutter-toolkit/skills/flutter-kaizen/SKILL.md | 0 |
  | .claude/skills/create-kit/SKILL.md | 0 |
  | .claude/skills/api-kaizen/SKILL.md | 0 |
  | .claude/skills/kaizen-orchestrator/references/search-sources.md | 0 |
  - **"amendment 없이 통과" 주장 검증** (지시사항 3): 원문 측정식 `grep -cE '[0-9]+ ?가지'`(질문 항목 제한 없음) 를 7파일에 그대로 실행 — 전부 0, 계약 문구 변경 없이 원 오라클 그대로 통과함을 확인.
    편법 여부 판단: 소스 `agent-design-guide.md` §6 실제 패턴 수는 1~7 (7개, `### 패턴 1`~`### 패턴 7` 직접 확인). 수정 전 요약(`요약` 절) 행은 "6가지 패턴 | 체이닝/라우팅/병렬화/오케스트레이터/평가자/계획-실행" — 6개 나열, **패턴7(Hook-Triggered Auto-Correction, 훅 트리거)이 누락**되어 있었다(git diff로 확인). 생성물 `docs/harness/agent-design-guide.html`은 수정 전부터 이미 "7 가지 패턴 | ...계획-실행/훅 트리거" — **소스보다 생성물이 앞서 있던 역방향 드리프트**였음을 diff로 확인. 즉 이번 수정은 오라클을 피하기 위한 편법이 아니라 소스 문서의 실제 결함(패턴 7 누락)을 생성물 기준으로 바로잡은 것 — 결함 수정으로 판단.
    부수적으로 `.claude/skills/kaizen-orchestrator/references/search-sources.md`의 "Anthropic 5가지"(에이전트 패턴)도 "Anthropic 공식 패턴"으로 함께 정리됨을 확인 (동일 드리프트 계열)
- [x] AR-04: 변경 범위가 선언 경로와 정확 일치 — PASS (amendment 적용, direction=relaxing+consent=anchored로 PASS 근거 가능)
  - 원 pathspec(5경로)로 측정 시: `git diff --name-only main...HEAD -- harness CLAUDE.md flutter-toolkit .claude/skills .harness ...`(13파일) vs 전체 diff(15파일) — **불일치**(`docs/harness/agent-design-guide.html`, `docs/harness/skill-design-guide.html` 2건 누락) → 원문 그대로면 FAIL
  - 개정 pathspec(+docs, 6경로)로 측정 시: 결과 15파일, 전체 diff 15파일과 **정확히 일치**(diff 명령 exit 0) → PASS
  - direction 계산 재현(zsh·bash): `amend_direction` 결과 `relaxing added=1 removed=0` — 사이드카 기재값과 일치

### Anti-patterns (2/2)
- [x] AP-03: bare code fence 금지 — PASS (`validate-plugin.py --check=code-fence` → V6 0 bare, exit 0)
- [x] AP-04: frontmatter name 필드 누락 금지 — PASS (`validate-plugin.py` → V1 전 플러그인 OK, exit 0)

### Reusability (2/2)
- [x] RE-01: private화 누락 없음 — PASS (이번 스프린트는 신규 컴포넌트 생성 없음, 문서/JSON 수정만)
- [x] RE-02: (4)항이 기존 §측정 명령 타당성 절 안에 위치, 새 최상위 절 미생성 — PASS
  - 근거: `#### 측정 명령 타당성 · 상태 전제` 절은 566행에서 시작해 749행 직전(`### 계약 봉인`, 상위 레벨) 까지 이어지며, 그 사이 `#`~`####` 레벨 헤더가 없음(내부 `#####` 서브섹션만 존재) — (4)/(5) 모두 같은 절 내부

### Diagnostics (4/4)
- [x] DG-01: `bash -n scripts/release.sh` 워닝 0개 — PASS (exit 0)
- [~] DG-02: IDE diagnostics 0개 — [미검증:ENV]
  - 1차 시도: 이 평가 환경에 IDE Problems panel/MCP 연동 없음(`runtime_inspection.mcp_server: null`)
  - fallback: `validate-plugin.py`(전 카테고리) exit 0, `sync-docs.py --check-only`/`sync-orchestrator.py --check-only` exit 0, `python3 -c "json.load(...)"`로 evals.json 구문 유효성 확인, `run-evals.py --verbose` 106 passed 확인 — 이번 스프린트 변경 파일(md/json) 클래스에서 IDE가 잡을 수 있는 구조적 결함은 이 조합으로 대체 검증됨
  - 실패 로그: 해당 없음(툴 자체 부재이므로 실행 실패 로그가 생성되지 않음)
  - 통제 불가 사유: 이 환경에 IDE Problems panel API가 연결되어 있지 않고 project.yaml에 lint 명령이 없음(`lint: null`) / 재검증 명령: 변경된 15개 파일을 VSCode 등 IDE로 열어 Problems 패널 확인
- [x] DG-03: 콘솔 로그 에러/예외 0개 — PASS (`bash scripts/release.sh 2>&1` → usage 메시지만 출력, 에러/예외 없음)
- [x] DG-04: N/A — 계약이 명시한 대로 문서·JSON 전용 변경이며 SC-01의 run-evals/validate-plugin 실행이 런타임 대체 검증

## Unverifiable Summary
- invalid_evidence: 0
- env_gaps: 1 [DG-02 — IDE Problems panel/MCP 부재, fallback(validate-plugin/sync-docs/sync-orchestrator/run-evals/JSON 유효성) 수행, 실패로그 해당없음, 재검증명령 명시]
- verified_coverage: (22 - 1) / 22 = 0.95 (임계 0.60 이상)
- 연속 ENV 승급: 없음 (DG-02는 이 슬러그 최초 평가)
- Verdict 영향: 통상 (APPROVE 가능 — invalid_evidence 0건, coverage 0.95 ≥ 0.60)

## Discrimination (규칙 12)
- 적용 조건: 없음 (이 스프린트의 22조건 중 동시성 가드·인증/권한·멱등성·입력 검증·데이터 유실·마이그레이션 안전성·재시도/중복제거·보안 경계·사용자 결함보고-테스트 충돌에 해당하는 조건 없음 — 문서/설정 드리프트 제거 스프린트)

## User-Reported Failures
- 없음 (해당 사항 없음)

## Evidence Validity
- 검사 대상 증거: 22건(조건별) + amendment 2건 + 셸 스니펫 재현 2건(ER-04 awk 예시, AR-04/AM-01 amend_direction)
- 무효 판정: 0건
- 셸 스니펫 실행 검증: 실행 2건(ER-04 awk 플래그형/범위형 대조, AM-01 amend_direction) · zsh/bash 양쪽 확인 2건 · 미실행 0건
- 무효 0건 — 미검증 카운터(INVALID)에 합산 없음

## Summary
- Total: 22/22 conditions passed (21 PASS 직접 근거 + 1 [미검증:ENV] 커버리지 게이트 통과)
- Verdict: **APPROVE**
- 비고: AR-03/AR-04는 이번 스프린트의 핵심 리스크였다. AR-04는 계약 write-once 원칙을 지키며 사이드카 amendment(AM-01, relaxing+anchored, 계산된 direction)로 정당하게 처리됐고, 재현 결과 계산값이 정확히 일치했다. AR-03은 오라클을 편법으로 우회하지 않고 실제 소스 결함(agent-design-guide.md 패턴7 누락)을 수정해 원문 그대로 통과시켰으며, 생성물(HTML)이 소스보다 앞서 있던 역방향 드리프트였음을 diff로 직접 확인했다. 이 레포의 반복 결함("생성물만 고치면 되돌아간다")과 정반대 방향이었다는 점도 특기할 만하다.

## Improvement Suggestions
- [AR-01] 측정-방식-불일치 — 지정 정규식 `[0-9]+ ?가지 (아키타입|스킬 유형|유형)`은 "9유형"/"11유형"(가지 없이 유형만) 형태나 역사적 의사결정 문서(design-brief.md §8, tone-kit-migration spec)의 과거 상태 서술까지는 못 잡는다. 다음 아키타입 개수 변경(13번째 추가 등) 시 회귀 게이트 강화가 필요하면 `범위 경계`에 "역사적 조사기록/스펙 문서는 스냅샷으로 예외 처리한다"는 명시적 제외 조항을 추가할 것을 권장 (`.harness/` 이력 제외와 동일한 논리를 docs/howto/design-brief.md·docs/superpowers/specs/*류에도 명문화)
- [AR-04 AM-01] 검증경로-미기재(경미) — 사이드카의 사용자 승인 앵커(2026-09-09T15:07:15)가 reflect-kit prompt-log에서 직접 대조되지 않았다(AskUserQuestion류 구조화 응답 추정). 향후 승인이 구조화 응답으로 이뤄질 경우 로그 대조 가능한 형태(예: 응답 요약을 별도 프롬프트로 재확인)로 남기는 것을 권장

