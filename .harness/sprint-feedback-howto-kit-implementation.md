# Sprint Feedback
Feature: howto-kit 플러그인 구현
Evaluated: 2026-09-08 12:30
Verdict: REJECT
Iteration: 1

## Contract Fingerprint
- path: .harness/sprint-contract-howto-kit-implementation.md
- sha256: aa0475d7691b8386ca888a94acefd6cbe0eea542c128ad3a939edf9d692a71c3
- status: active
- slug: howto-kit-implementation
- contract_root: /Users/jackson/Hub/10_Dev/claude-plugins
- contract_root_unconfigured: false
- 선택 근거: ladder 1 명시경로
- legacy_contract_used: false
- seal_status: SEAL_OK
- contract_seal_broken: n/a
- 재확인(Step 5): 일치
- status_transition: skipped (verdict=REJECT)

## Amendments
- amendments: 0 (사이드카 없음)

## User Correction Audit
- correction_log_status: available
- unreflected_corrections: 0 (세션 0e3335f2 의 유일한 [prompt] 항목은 스프린트 착수 지시문 자체이며, 계약과 일치한다)
- verdict 영향: 없음 (표면화 전용)

## Results

### Skill (5/5)
- [x] SK-01: 3개 SKILL.md frontmatter — PASS
  - 근거: `python3 scripts/validate-plugin.py howto-kit --check=frontmatter` → `V1 frontmatter 3 skills + 1 agent — OK`. 3 파일 모두 name/description/user-invocable 비어있지 않음 확인 (howto-kit/skills/howto/SKILL.md:1-12, howto-doc/SKILL.md:1-11, howto-audit/SKILL.md:1-14)
- [x] SK-02: agent frontmatter 4필드 + tools 제외 — PASS
  - 근거: `howto-kit/agents/howto-reviewer.md:2-9` name/description/tools/model 존재. `grep -n '^tools:'` → `tools: Read, Grep, Glob` (Write/Edit/NotebookEdit 없음). V1 "1 agent" OK
- [x] SK-03: allowed-tools 스코프 — PASS
  - 근거: `howto/SKILL.md:14` `allowed-tools: Read, Grep, Glob, WebFetch, WebSearch` (Write/Edit 없음). `howto-audit/SKILL.md:14` `allowed-tools: Read, Grep, Glob, Bash, Agent` (Write/Edit 없음). `howto-doc/SKILL.md:12` `allowed-tools: Read, Write, Grep, Glob, Bash, WebFetch, WebSearch` (Write 있음). 조건 문언 그대로 충족
  - 추가 확인(사용자 지시 반영): howto-audit 의 Bash·Agent 용도를 SKILL.md 본문(Gotcha 5, Phase 2~3)에서 추적 — Bash 는 `howto-gate.sh` 소싱·실행 전용, Agent 는 Read/Grep/Glob 만 가진 howto-reviewer 위임 전용. Write 경로 없음. "읽기 전용" 의도와 충돌 없음. 참고로 backend-audit/infra-audit/react-audit/rust-audit 는 allowed-tools 자체가 없어 오히려 더 넓은 기본 툴셋을 암묵 허용 — howto-audit 이 더 제한적임
- [x] SK-04: evals.json 케이스 수 + 입도 케이스 — PASS
  - 근거: `python3 -c "... print(len(d['cases']))"` → `9`. 입도 케이스(assertions 기준): E2-granularity-terminal-action(`nonterminal=2, hedge=2` — 종결동사 미충족), E3-granularity-verify-and-branch(`no_verify=2, no_branch=2` — 확인/분기 부재) 2건 확인, 조건(a)(b)(c) 중 (a)(b)(c) 각각 충족
- [x] SK-05: 트리거 키워드 교차 검증 — PASS
  - 근거: 4개 description(howto/howto-doc/howto-audit/howto-reviewer) 에서 quoted 트리거 키워드 추출 후 python set intersection = `set()`, substring pair = `[]` (howto: 8개, howto-doc: 5개, howto-audit: 5개, howto-reviewer: 0개 — agent 는 프롬프트 트리거가 아니라 Agent 도구로만 위임되므로 quoted 키워드 없음이 설계상 정상)

### Script (6/6)
- [x] SC-01: G1~G6 셸 함수 zsh/bash 동일 출력 — PASS
  - 근거: `zsh -c '. howto-kit/scripts/howto-gate.sh; howto_gate howto-kit/evals/fixtures/pass-fcm-ios.md'` 와 `bash -c '...'` 출력 각 7줄(G1_~G6_ + GATE_PASS) 동일, `diff <(zsh…) <(bash…)` exit 0. 음성 대조: G5 판정 블록 삭제한 스크래치 사본 실행 시 `G5_TERMINAL` 줄 소멸 확인(측정이 게이트 로직을 직접 경유함을 확인)
- [x] SC-02: G5/G6 양성 위반 케이스 FAIL — PASS
  - 근거: `fail-g5-nonterminal.md` zsh/bash 모두 `G5_TERMINAL FAIL nonterminal=2 hedge=2` + `GATE_FAIL`. `fail-g6-granularity.md` zsh/bash 모두 `G6_GRANULARITY FAIL steps=3 no_verify=2 no_branch=2 ... guess_pct=66` + `GATE_FAIL`. 음성 대조: g5 위반 문장을 정상 문장(`동작: 열기`/`동작: 입력` + 헤더 수정)으로 고친 스크래치 사본 실행 시 zsh·bash 모두 `G5_TERMINAL PASS` + `GATE_PASS` 로 반전 확인
- [x] SC-03: sync-docs.py howto-kit + --check-only — PASS
  - 근거: `python3 scripts/sync-docs.py howto-kit` exit 0, 마지막 출력 `howto-kit/README.md: 동기화됨`. `python3 scripts/sync-docs.py --check-only` exit 0, 마지막 줄 `모든 README가 동기화 상태입니다.`
- [x] SC-04: validate-plugin.py howto-kit(V1~V8) + 전 킷 실행 — PASS
  - 근거: `python3 scripts/validate-plugin.py howto-kit` → V1~V8 전부 OK, exit 0. `python3 scripts/validate-plugin.py`(인자 없음) → `Total: 14 plugins, 14 OK`, exit 0, howto-kit 항목 전부 OK
- [x] SC-05: sync-orchestrator.py 매핑 + Phase 자동생성 — PASS
  - 근거: `scripts/sync-orchestrator.py:115,126` `"howto-kit": "docs/howto/"` 매핑 존재. `python3 scripts/sync-orchestrator.py` 실행(exit 0, `이미 동기화됨 (13 plugins)`) 후 `.claude/skills/kaizen-orchestrator/SKILL.md:496,501` 에 `Phase 17 — howto-kit 카이젠` / `howto-kaizen` 등장
- [x] SC-06: check-external-links.py KIT_DIRS — PASS
  - 근거: `scripts/check-external-links.py:38` `"reflect-kit", "bambu-kit", "onboarding-kit", "howto-kit"]`

### Error (3/3)
- [x] ER-01: §11 미확인 4건 처리 — PASS
  - 근거: `howto-kit/references/provenance-notes.md` 전문 확인. (1) 체크리스트 방법론 — (b) `step-contract.md:122-125` `[미확인]` 등급 명시 + provenance-notes.md §1 참조. (2) MS Learn 권한 인용 2건 — (a) 확정: `navigation-anchors.md:84,86` 양쪽 모두 "확인 2026-09-08" 라벨 + URL, provenance-notes.md §2 의 **확인됨** 2건(원 인용 1 + 대체근거 1)과 정확히 일치, 확인 실패했던 `resource group … greyed out` 문장은 어디에도 인용되지 않음. (3) RSS 피드 — (b) `README.md:129` "일부 RSS 피드... 확인 실패 상태이며 그렇게 표기돼 있다". (4) 이름 충돌 — (b) `README.md:129` + `provenance-notes.md:96-110` `[미확인]` 명시. 4건 모두 확정 사실로 오용된 곳 없음
- [x] ER-02: 부재 파일/빈 파일 처리 — PASS
  - 근거: zsh·bash 모두 `howto_gate /nonexistent/x.md` → `GATE_BLOCKED no_such_file=...` exit 0. zsh·bash 모두 `howto_gate <빈파일>` → G1~G6 6줄 + `GATE_FAIL` (exit 0), 셸 크래시 없음. 음성 대조: `[ -f "$g" ]` 가드 제거 스크래치 사본 실행 시 `awk: can't open file` / `grep: No such file` 에러 스트림 발생 확인(가드가 실제로 이 실패를 막고 있음을 확인)
- [x] ER-03: G6 0-나누기 없음 — PASS
  - 근거: `edge-zero-steps.md`(액션 스텝 0건) zsh·bash 모두 `G6_GRANULARITY PASS steps=0 ... guess_pct=0`, `divide` 문자열 grep -c 결과 0/0

### Architecture (6/7)
- [x] AR-01: plugin.json — PASS
  - 근거: `python3 -c "...json.load..."` → `howto-kit 0.1.0 77`(name/version/description 길이 비어있지 않음)
- [x] AR-02: Step Contract 필드 정본 1곳 — PASS
  - 근거: `grep -rn 'if_not_found\|target_label\|source\.tier' howto-kit/` 전체 9건 매치가 전부 `references/step-contract.md` 1개 파일 안에서만 발생(YAML 필드/표 형태). `howto/SKILL.md:40-60`, `howto-doc/SKILL.md:20-33`, `howto-audit/SKILL.md`, `howto-reviewer.md:55` 는 전부 참조 링크 또는 렌더링 예시(산문)뿐이고 필드 정의 재나열 없음
- [x] AR-03: marketplace.json 엔트리 — PASS
  - 근거: `python3 scripts/validate-plugin.py howto-kit --check=plugin-json` → `V7 plugin-json v0.1.0 matches marketplace — OK`. 엔트리 `name: howto-kit, source: ./howto-kit, description: "[v0.1.0 · 2026-09-08] ..."` 확인
- [x] AR-04: CLAUDE.md 등록 — PASS
  - 근거: `grep -n 'howto' CLAUDE.md` → 23행(Repository Overview 목록), 294-301행(Skills Reference 표: `/howto`(298) · `/howto-doc`(299) · `/howto-audit`(300) · `howto-reviewer`(301) 4개 전부 열거)
- [x] AR-05: docs/howto-kit HTML + index.html 등록 — PASS
  - 근거: `docs/howto-kit/overview.html` 존재(`test -f` 확인). `docs/index.html:568` `{ id: 'howto-overview', ..., file: 'howto-kit/overview.html' }` 등록, 경로 실재 확인
- [x] AR-06: howto-kaizen/howto-research 존재 — PASS
  - 근거: `.claude/skills/howto-kaizen/SKILL.md`, `.claude/skills/howto-research/SKILL.md` 둘 다 `test -f` 확인, `head -6` 에서 각각 name/description 확인
- [ ] AR-07: diff-scope 커밋 경로 허용목록 — **FAIL**
  - 근거: 계약이 지정한 정확한 명령
    `git diff --name-only 4fb1382..HEAD -- . ':(exclude).harness/handoff/*' ':(exclude)docs/bambu-calibration/*'`
    를 그대로 실행한 결과 37줄 중 **2줄이 허용 목록의 어떤 접두에도 매치하지 않는다**:
    - `.harness/sprint-contract-howto-kit-design-brief.md`
    - `.harness/sprint-feedback-howto-kit-design-brief.md`
    (python 으로 각 줄을 14개 허용 접두와 `startswith` 대조, 매치 0건인 줄만 추출한 결과)
  - 원인 추적: `git show --stat 54fb3b3 | grep design-brief` 로 확인한 결과 이 두 파일은 **이번
    구현 커밋(0e771e0)이 아니라 직전의 별도 스프린트 커밋 54fb3b3(설계 브리프, 이미 별도
    계약으로 APPROVE 되어 status: done 상태)이 도입한 것**이다. `git show --stat 0e771e0`
    에는 이 두 파일이 전혀 등장하지 않는다(0e771e0 이 건드린 `.harness` 관련 항목은 없음).
  - 이것은 계약 자체가 명시한 diff-scope 오라클의 결함이기도 하다 — 베이스라인 커밋
    `4fb1382` 가 설계 브리프 스프린트(54fb3b3)보다도 앞서 있어, 이미 종결된 별도 스프린트의
    산출물까지 이번 스프린트의 diff 에 편입된다. 계약은 동시 세션 커밋(97cde49, bambu
    핸드오프)의 경로만 exclude pathspec 으로 제외했고, 같은 문제를 가진 선행 스프린트
    54fb3b3 의 `.harness/*-design-brief.md` 2개는 exclude 목록에도 허용 목록에도 넣지
    않았다. 그러나 harness/docs/guides/qa-evaluation-guide.md 의 Diff-Scope Oracle 지침은
    "4 요소 중 빠진 것을 REJECT 사유에 열거한다"고 명시하므로, 오라클 결함이 확인됐다고 해서
    측정 결과(FAIL)를 무효화하지 않는다. 계약 문언 그대로 측정한 결과가 FAIL 이므로 FAIL 로
    판정한다
  - 수정 방향(둘 중 하나): (1) 계약의 측정 명령 베이스라인을 `54fb3b3..HEAD` 로 좁히거나
    (2) exclude pathspec 에 `':(exclude).harness/sprint-contract-howto-kit-design-brief.md'`
    와 `':(exclude).harness/sprint-feedback-howto-kit-design-brief.md'` 를 추가한다

### Anti-patterns (2/2)
- [x] AP-03: bare code fence 금지 — PASS
  - 근거: `python3 scripts/validate-plugin.py howto-kit --check=code-fence` → `V6 code-fence 0 bare — OK`
- [x] AP-04: frontmatter name 필드 누락 없음 — PASS
  - 근거: `python3 scripts/validate-plugin.py howto-kit --check=frontmatter` → `V1 frontmatter 3 skills + 1 agent — OK`

### Reusability (2/2)
- [x] RE-01: 재사용 가능 컴포넌트를 private 처리하지 않음 — PASS
  - 근거: howto-gate.sh 는 howto-kit 전용 스키마(Step Contract G1~G6)에 결합돼 있어 범용
    공유 후보가 아님. 3 스킬 + 1 에이전트 모두 user-invocable 이거나(스킬) 의도적으로 위임
    전용(에이전트)이며 부당하게 숨겨진 컴포넌트 없음
- [x] RE-02: 기존 유사 컴포넌트 재사용 여부 — PASS
  - 근거: `onboarding-kit/skills/setup-guide/SKILL.md` 의 `guide_gate()`(G1~G4)가 리서치
    소스로 명시적으로 인용되었고, howto-kit 은 이를 확장한 G1~G6(스키마·판정축이 다름)을
    독자 구현 — 동일 컴포넌트의 무의미한 재작성이 아니라 원형을 인지한 위의 확장. `scripts/`
    공유 경로 검색 결과 중복 없음

### Diagnostics (3/3 + 1 N/A)
- [x] DG-01: bash -n scripts/release.sh 워닝 0개 — PASS
  - 근거: `bash -n scripts/release.sh` exit 0, 출력 없음
- [x] DG-02: IDE diagnostics 워닝/인포 0개 — PASS [정적]
  - 근거: MCP/IDE 진단 도구 미설정(`project.yaml.runtime_inspection.mcp_server: null`)이라
    정적 대체 수행: `python3 -m py_compile scripts/sync-orchestrator.py scripts/check-external-links.py scripts/validate-plugin.py scripts/sync-docs.py` exit 0. `sh -n howto-kit/scripts/howto-gate.sh` / `sh -n howto-kit/evals/run-evals.sh` 모두 exit 0. `shellcheck -s sh howto-kit/scripts/howto-gate.sh` / `run-evals.sh` 모두 exit 0(0 issues)
- [x] DG-03: release.sh 콘솔 로그 에러 0개 — PASS
  - 근거: `bash scripts/release.sh 2>&1` → Usage 안내 메시지만 출력(정상 동작), 에러/예외 문자열 없음, exit 0
- [ ] DG-04: 실제 앱/서버 구동 에러 0개 — **N/A (계약이 사유와 함께 닫음, 타당함 확인)**
  - 근거: howto-kit 은 실행 가능한 앱/서버가 아니라 스킬 정의 파일 모음. 대체 런타임 검증으로
    지정된 SC-01/SC-02/ER-02 게이트 함수 실행을 본 평가에서 zsh·bash 양쪽 모두 실측 완료
    (위 항목 참조). N/A 사유 타당

## Unverifiable Summary
- invalid_evidence: 0
- env_gaps: 0
- verified_coverage: (29 - 0) / 29 = 1.00 (임계 0.60 충족)
- 연속 ENV 승급: 없음
- Verdict 영향: 통상 (미검증 카운터 무관 — REJECT 사유는 AR-07 실측 FAIL 1건)

## Discrimination (규칙 12 적용 조건)
- 적용 조건: SC-01·SC-02·ER-02 (게이트 로직 = 9항 중 "입력 검증"에 준하는 셸 함수 판정 로직)
- 결합 확인: SC-01 — evals.json 의 assertion 이 `howto_gate()` 함수 직접 실행 출력을 대조 (`run-evals.sh` 가 `. "$GATE"; howto_gate` 로 소싱·직접 호출). 결합 확인됨
- 음성 대조: SC-01 — G5 블록 삭제 시 `G5_TERMINAL` 줄 소멸 확인(FAIL). SC-02 — 위반 문장을
  정상 문장으로 치환 시 PASS 로 반전 확인. ER-02 — `-f` 가드 제거 시 에러 스트림 발생 확인.
  discrimination: executed (모두 스크래치 사본에서 실행, 원본 파일 무변경 — `git status --porcelain` 클린 확인)

## Evidence Validity
- 검사 대상 증거: 29건 조건 전체
- 무효 판정: 0건
- 셸 스니펫 실행 검증: 실행 9건(SC-01, SC-02, ER-02, ER-03 + run-evals.sh 9케이스) · zsh/bash 양쪽 확인 전체
- 무효 0건은 미검증 카운터에 합산 없음

## Summary
- Total: 28/29 conditions passed (DG-04 는 N/A 로 별도 처리, pass 분모에서 제외 시 28/28 PASS + 1 FAIL)
- Verdict: **REJECT**
- REJECT 사유: AR-07 이 계약이 명시한 정확한 측정 명령으로 FAIL. 원인은 구현 커밋(0e771e0)이
  아니라 diff-scope 오라클의 베이스라인(4fb1382)이 선행의 별도 완료 스프린트(54fb3b3, 설계
  브리프)까지 포괄하면서 그 스프린트의 `.harness/sprint-contract-howto-kit-design-brief.md`,
  `.harness/sprint-feedback-howto-kit-design-brief.md` 2개 파일이 허용 목록 밖에서 잡힌 것.
  구현 자체의 결함이 아니라 계약 측 diff-scope 오라클의 exclude pathspec 미비이지만, 계약
  문언을 문자 그대로 측정한 결과가 FAIL 이므로 그대로 FAIL 판정한다(qa-evaluation-guide
  Diff-Scope Oracle 지침 — 오라클 결함은 REJECT 사유에 열거하되 결과 자체를 무효화하지 않는다).
  수정 우선순위: 계약(AR-07)의 측정 명령을 다음 iteration 전에 수정 — 베이스라인을
  `54fb3b3..HEAD` 로 좁히거나 두 design-brief 산출물을 exclude pathspec 에 추가. 계약 수정
  후 재측정 시 다른 28개 조건은 모두 재현 가능한 PASS 증거를 확보한 상태.

## Improvement Suggestions
- [AR-07] 검증경로-미기재 — diff-scope 오라클의 베이스라인이 선행 완료 스프린트(54fb3b3)의
  산출물까지 포괄한다. 다음 중 하나로 좁힐 것: (a) 측정 명령의 베이스라인을
  `4fb1382..HEAD` → `54fb3b3..HEAD` 로 변경 (b) exclude pathspec 에
  `':(exclude).harness/sprint-contract-howto-kit-design-brief.md'` 와
  `':(exclude).harness/sprint-feedback-howto-kit-design-brief.md'` 추가.
