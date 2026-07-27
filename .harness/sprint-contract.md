---
feature: "kaizen Phase 4 — Harness 인프라 (파이프라인 스크립트 회귀 · 워크플로우 스킬 enforcement · Phase 1~3 정합화)"
created: "2026-07-27 20:10"
complexity: "복잡"
conditions: 23
---

# Sprint Contract — Phase 4 Harness 카이젠

## 배경

이번 사이클의 프레이밍은 Phase 1~3 과 동일하다. `/insights` 2026-07-27 의 Friction #1·#3 은
직전 사이클 승격분인데 세션당 비율이 줄지 않았고, 따라서 **새 soft 문장 추가가 아니라
enforcement 등급 상향**이 기본 전략이다. 등급 어휘(E1/E2/E3)의 SSOT 는
`skill-design-guide.md §3.7` 이며 여기서 재정의하지 않는다.

Phase 4 에 배정된 신호는 네 갈래다.

1. **실측 회귀 (최우선).** `scripts/finalize-phase.sh` 의 audit-log append 가 Phase 1·2·3
   에서 연속 3 회 경고를 냈다. 재현 결과 원인은 **CLI 계약 불일치**였다 — finalize 는
   `--phase/--result/--date` 를 넘기는데 `append-audit-log.py` 는 `--cycle-id/--notes` 만
   받는다(argparse exit 2). 게다가 호출부가 `2>/dev/null` 로 stderr 를 삼켜 3 사이클 동안
   원인이 보이지 않았다. 같은 스크립트에 두 번째 결함도 있다: phase 번호를 1~10 으로
   하드코드하여 **Phase 11~14 (planning·reflect·bambu·onboarding) 는 finalize 자체가
   exit 1** 이다.
2. **이전 사이클 backlog 3 건.** detect-docs-drift 매핑 suffix 불일치 · `/sprint` REJECT
   iteration 자동 카운트 · `/refactor-checklist` 스택별 규칙 자동 로드.
3. **Friction #5 (Phase 4 배정분).** 배치 커밋이 회귀를 은폐하고, 재개 시 핸드오프 문서가
   스테일이며, 병렬 세션이 같은 파일을 건드려 빌드가 깨진다.
4. **Phase 1~3 정합화.** harness 스킬 일부가 구 규약을 들고 있다 (Unverifiable 3 항 · validate
   카테고리 7 개).

## 리서치 소스

Context7 MCP 는 이 세션에서 OAuth 미인증이라 사용 불가 → `phase-research-templates.md`
§Phase 4 의 fallback 인 WebFetch 로 1 차 출처를 직접 조회했다 (5 건, 최소 3 건 요건 충족).

- <https://code.claude.com/docs/en/hooks> — 훅 이벤트 31 종. **exit 2 만 차단**하고 exit 1 은
  비차단 에러로 그대로 진행된다. `PostToolBatch`·`Stop`·`SubagentStop`·`TaskCompleted` 도
  차단 가능. 실패를 조용히 흘리지 않으려면 종료 코드 규약이 명시적이어야 한다는 근거
- <https://raw.githubusercontent.com/mgechev/skills-best-practices/main/README.md> — Phase 4
  필수 소스. "Fragile/repetitive operations where variation is a bug" 는 스크립트로,
  스크립트는 "highly descriptive, human-readable error messages" 를 돌려줘야 한다.
  logic validation 은 "execution blockers" 를 찾는 것
- <https://arxiv.org/abs/2606.27416> — Glite ARF (2026-06-25). 12 병렬 에이전트 · 273 태스크를
  결정론적 Python verifier 로 통제. "the rules of the research process live in code that
  **fails loudly when violated**, not in prose that agents are merely asked to follow" +
  task isolation / immutability of completed work
- <https://arxiv.org/abs/2605.06527> — STALE (2026-05-07). 에이전트가 자기 기억의 무효화를
  탐지하는 능력: **최고 모델 55.2%**. Implicit Conflict (명시적 부정 없이 나중 관측이 앞선
  기억을 무효화) 가 주 실패 모드 → 핸드오프 문서를 자기 기억으로 신뢰하면 안 되고 외부
  상태(git)로 대조해야 한다는 근거
- <https://arxiv.org/abs/2604.08224> — Externalization in LLM Agents (2026-04-09). harness
  engineering 을 "the unification layer that coordinates [memory·skills·protocols] into
  governed execution" 으로 정의. 상태 외부화가 harness 의 본질

## GAP 분석

| # | 현재 | 리서치/데이터 근거 | 조치 | 등급 |
| - | ---- | ------------------ | ---- | ---- |
| G1 | finalize→append CLI 계약 불일치 + stderr 침묵 (3 사이클 무증상) | Glite ARF "fails loudly" · mgechev "descriptive error messages" | phase 모드 신설 + 호출부 정정 + 실패 시 stderr 노출 | E3 |
| G2 | phase-num 1~10 하드코드 → Phase 11~14 finalize 불가 | orchestrator 는 Phase 14 까지 존재 (SKILL.md Step 14) | MAX_PHASE 를 failure-count 파일에서 유도 | E3 |
| G3 | detect-docs-drift 가 존재하지 않는 HTML 경로를 산출 (`plugin-validation-guide.html`) | 이전 사이클 audit-log meta-issue | index.html 레지스트리 대조 + 미등록은 NEW 로 표시 | E3 |
| G4 | `/sprint` iteration 한계가 문장만 (카운터 없음) | insights Friction #3 · backlog | 응답 복사형 카운터 + 복구 근거를 sprint-feedback.md 로 | E2 |
| G5 | 재개 시 핸드오프 문서를 그대로 신뢰 | STALE 55.2% | git 대조 재검증 단계 신설 | E2 |
| G6 | 배치 커밋 · 병렬 세션 파일 충돌 | insights Friction #5 · Glite ARF task isolation | 검증 단위 커밋 + 소유 파일 열거 | E2 |
| G7 | refactor-checklist 규칙 소스가 레포 상대경로 문장뿐 | digest `cwd-contract-path-drift` 계열 · Phase 3 ladder 선례 | ladder + 부재 시 `[미검증]` | E2 |
| G8 | create-agent 가 Unverifiable "3 항" 이라 서술 | agent-design-guide §10 은 4 항 (Phase 1) | 4 항으로 정정 | E1 |
| G9 | 5 개 harness 스킬이 validate 카테고리를 "7" 로 서술 | plugin-validation-guide 는 V1~V8 | 8 로 정정 | E1 |
| G10 | scope-creep Gotcha 가 파일 수 기준 | digest `complexity-by-file-count` 와 동일 계열 결함 | unit 기준 + unit 별 증거 의무 | E2 |
| G11 | 가드 우회(cwd 이동) 가 명문화 안 됨 | digest `bypass-run-guard-by-cwd` | 템플릿 rationalization_override 1 건 | E1 |

## 범위 경계

- 수정 대상: `scripts/{append-audit-log.py,finalize-phase.sh,detect-docs-drift.py}` ·
  `harness/skills/{sprint,refactor-checklist,create-agent,create-skill,init,harness-kaizen,contract-kaizen,evaluator-kaizen}/SKILL.md` ·
  `harness/templates/project.yaml`
- 수정 금지 (다른 Phase 소관): `harness/skills/sprint-contract/**` · `harness/agents/qa-evaluator.md` ·
  `harness/docs/guides/{skill,agent,contract}-design-guide.md` · `harness/docs/guides/qa-evaluation-guide.md` ·
  `harness/references/contract-schema.md` · 모든 kit · `.claude/skills/kaizen-orchestrator/**` ·
  marketplace.json · plugin.json · changelog
- **Unit 계수 (harness-kaizen scope-creep 규칙 대비):** 신규 도입 unit 은 3 개
  (U-C1 sprint · U-C2 refactor-checklist · U-E 템플릿). 나머지는 오케스트레이터 명시 지시
  backlog (U-A finalize 파이프라인 · U-B docs-drift) 와 SSOT 사실 정정 (U-D) 이다. 본 계약이
  그 계수 규칙 자체를 unit 기준으로 정정한다 (G10)

## 회귀 게이트

- `python3 scripts/validate-plugin.py` → 11 plugins 11 OK · Exit 0
- 수정한 스크립트 3 개는 문법 검사 + **실제 실행** 증거 필수 (자기보고 금지)

## Script

- [ ] SC-01: `python3 scripts/append-audit-log.py --phase 4 --result pass --date 2026-07-27 --dry-run` 이 exit 0 이고 출력에 `Phase 4` 와 `pass` 가 포함된다 (측정: 실제 실행 + 출력 인용) [exact]
- [ ] SC-02: phase 모드에서 cycle-id 미지정 시 `.harness/.meta/kaizen-state.yaml` 의 `cycle_id` 값을 사용한다 (측정: `--dry-run` 출력에 `kaizen-2026-07-27` 포함) [exact]
- [ ] SC-03: `scripts/finalize-phase.sh` 가 append-audit-log.py 에 넘기는 인자 집합이 argparse 정의 집합의 부분집합이다 (측정: `grep -n "append-audit-log" scripts/finalize-phase.sh` 와 `python3 scripts/append-audit-log.py --help` 대조) [exact, enumerated]
- [ ] SC-04: finalize-phase.sh 의 **실행 라인**에 stderr 를 버리는 `2>/dev/null` 이 0 건이고, audit-log 실패 시 stderr 앞부분이 사용자에게 출력된다 (측정: `grep -n '^[^#]*2>/dev/null' scripts/finalize-phase.sh | wc -l` == 0 · 주석 라인은 규칙 설명이므로 제외) [exact]
- [ ] SC-05: `bash scripts/finalize-phase.sh 14 pass` 가 phase 범위 에러 없이 exit 0 이다 (측정: 실제 실행 후 `echo $?`) [exact]
- [ ] SC-06: 사이클 완료(status completed) 판정이 하드코드 `10` 이 아니라 유도된 MAX_PHASE 변수와 비교한다 (측정: `grep -n "MAX_PHASE" scripts/finalize-phase.sh`) [exact]
- [ ] SC-07: `python3 scripts/detect-docs-drift.py` 가 `harness/docs/guides/plugin-validation-guide.md` 변경분을 `docs/harness/plugin-validation.html` 로 매핑한다 (측정: 임시 커밋 없이 `--since HEAD~N` 또는 단위 함수 직접 호출로 실행) [exact]
- [ ] SC-08: detect-docs-drift 출력이 대상 HTML 의 등록/존재 여부를 구분 표시한다 (JSON 모드에 `exists` 필드, 텍스트 모드에 `NEW` 표기) (측정: `--json` 실행 출력) [exact]
- [ ] SC-09: 수정한 스크립트 3 개가 문법 검증을 통과한다 — `bash -n scripts/finalize-phase.sh`, `python3 -m py_compile scripts/append-audit-log.py scripts/detect-docs-drift.py` (측정: 3 명령 각각 exit 0) [exact, enumerated]

## Skill

- [ ] SK-01: `harness/skills/sprint/SKILL.md` 에 재개 시 핸드오프 문서를 git 으로 재검증하는 단계가 존재하고 STALE 근거 URL 이 인용된다 [exact]
- [ ] SK-02: 동 파일에 QA iteration 카운터가 **응답에 복사하는 형태**로 정의되고, 3 회 도달 시 중단 + 컨텍스트 리셋 시 `.harness/sprint-feedback.md` 로 복원하는 규칙이 명시된다 [exact]
- [ ] SK-03: 동 파일에 "커밋 단위 = 검증 증거가 확보된 수정 단위" 원칙과 병렬 세션 소유 파일 열거 규칙이 존재한다 [structural]
- [ ] SK-04: `harness/skills/refactor-checklist/SKILL.md` 에 규칙 소스 경로 해석 ladder (`${CLAUDE_PLUGIN_ROOT}` → 레포 → 마켓플레이스) 와 소스 부재 시 `[미검증]` 표기 규칙이 존재한다 [exact]
- [ ] SK-05: `harness/skills/create-agent/SKILL.md` 의 Unverifiable 정책 항 수 표기가 agent-design-guide §10 과 일치한다 (측정: `grep -n "Unverifiable 조건 정책" harness/skills/create-agent/SKILL.md harness/docs/guides/agent-design-guide.md`) [exact]
- [ ] SK-06: init · create-skill · harness-kaizen · contract-kaizen · evaluator-kaizen 5 개 SKILL.md 에서 validate-plugin 카테고리 수가 8 로 정정된다 (측정: `grep -rn "7 카테고리\|V1~V7" harness/skills` 0 건) [exact, enumerated]
- [ ] SK-07: `harness/skills/harness-kaizen/SKILL.md` 의 scope-creep Gotcha 가 파일 수가 아니라 unit 기준으로 재정의되고 unit 별 독립 검증 증거 의무를 포함한다 [exact]

## Architecture

- [ ] AR-01: 금지 파일이 diff 에 없다 — sprint-contract/SKILL.md · qa-evaluator.md · skill/agent/contract-design-guide · qa-evaluation-guide · contract-schema.md · 모든 kit · kaizen-orchestrator (측정: `git diff --name-only HEAD` 전수 대조) [exact, enumerated]
- [ ] AR-02: `harness/templates/project.yaml` 의 `rationalization_overrides` 에 가드 우회 차단 엔트리가 1 건 추가되고 기존 YAML 구조(주석 예시 포함)가 유지된다 [structural]

## Error

- [ ] ER-01: `python3 scripts/append-audit-log.py --phase 4 --result maybe` 가 사람이 읽을 수 있는 에러 메시지와 non-zero exit 을 반환한다 (측정: 실제 실행 + `echo $?`) [exact]

## Anti-patterns

- [ ] AP-01: bare code fence 0 건 (측정: `python3 scripts/validate-plugin.py harness --check=code-fence`)
- [ ] AP-02: 변경 파일에 하드코드 버전 문자열을 새로 추가하지 않는다 (측정: `git diff` 육안 + grep)

## Reusability

- [ ] RE-01: Phase 3 가 정한 경로 해석 ladder 형식을 재사용하고 새 동의어를 만들지 않는다 (측정: refactor-checklist 의 ladder 와 qa-evaluator.md Step 8 ladder 용어 대조)

## Diagnostics

- [ ] DG-01: `python3 scripts/validate-plugin.py` 가 11 plugins 11 OK · Exit 0 이다 (측정: 실제 실행 + 출력 인용)
