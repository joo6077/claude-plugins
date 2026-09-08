# Sprint Feedback
Feature: howto-kit 플러그인 구현
Evaluated: 2026-09-08 16:10
Verdict: APPROVE
Iteration: 4

## Contract Fingerprint
- path: /Users/jackson/Hub/10_Dev/claude-plugins/.harness/sprint-contract-howto-kit-implementation.md
- sha256: aa0475d7691b8386ca888a94acefd6cbe0eea542c128ad3a939edf9d692a71c3
- status: active (→ done 예정, Step 5.5)
- slug: howto-kit-implementation
- contract_root: /Users/jackson/Hub/10_Dev/claude-plugins
- contract_root_unconfigured: false
- 선택 근거: 명시 경로 (HARNESS_CONTRACT 상당 — 사용자가 절대경로로 지정)
- legacy_contract_used: false
- seal_status: SEAL_OK (conditions_digest sha256:5de60ce9548db9c6 == 실측 조건 블록 해시. 29/29 조건 카운트 frontmatter와 일치)
- contract_seal_broken: n/a
- 재확인(Step 5): 일치 (저장 직전 sha256 재계산 결과 동일)
- status_transition: active -> done (본 리포트 저장 직후 수행)
- HEAD 측정 시점: b1a0f4d (`git log --oneline -1`)

## Amendments
- amendments: 2 (A-01, A-02) — 둘 다 대상 조건 AR-07
- PASS 근거 가능: 2 (A-01: direction=relaxing · consent=anchored / A-02: direction=relaxing · consent=anchored)
- PASS 근거 불가: 0

### A-01 검증
- direction 재계산: `git diff --name-only 4fb1382..HEAD` (39경로) vs `54fb3b3..HEAD` (37경로),
  `comm -13/-23` → added=0, removed=2 (`.harness/sprint-contract-howto-kit-design-brief.md`,
  `.harness/sprint-feedback-howto-kit-design-brief.md`). 스키마의 `amend_direction()` 을
  이 두 파일 SET에 기계적으로 적용하면 "narrowing"(added=0·removed>0)이 나오지만, 이 함수는
  **허용목록 자체의 증감**을 재는 용도로 설계됐고 A-01은 허용목록이 아니라 **측정 베이스라인**을
  바꾼다. 올바른 판정 기준은 스키마 본문의 정의("이 amendment 를 적용하면 PASS 하는 구현의
  집합이 줄어드는가 늘어나는가")이며, 실측으로 직접 확인했다: 베이스라인 4fb1382 기준으로는
  AR-07이 2건 위반으로 FAIL, 54fb3b3 기준으로는 0건으로 PASS — 동일한 구현(코드 변경 없음)이
  amendment 적용만으로 FAIL→PASS 로 뒤집힌다. 이것은 명백히 `relaxing`이다. (기계적 `amend_direction`
  적용은 이런 baseline-변경형 amendment에 그대로 쓰면 오분류를 유발한다는 것을 여기 기록해
  Improvement로 남긴다.)
- 사유 검증: `git log`로 `54fb3b3`이 별개 계약(`slug: howto-kit-design-brief`, `status: done`,
  `conditions_digest: sha256:dee06e6878247d76`, `locked_at: 2026-09-07 17:35`)의 커밋임을 확인.
  `git show --stat 54fb3b3` 결과 그 커밋은 `.harness/sprint-contract(-feedback)-howto-kit-design-brief.md`
  + `docs/howto-kit/design-brief.md` + `docs/howto-kit/drafts/SKILL.md` 4개 파일을 추가했다.
  design-brief.md/drafts는 이후 `docs/howto/` 로 이동해 현재 diff에도 살아있고 허용목록(`docs/howto/`)에
  포함되지만, 계약/피드백 파일 2개만 이번 스프린트 baseline(4fb1382)에 잘못 포함돼 있었다.
  `git show --stat 0e771e0`(이번 구현 커밋)에는 그 2개 파일이 등장하지 않음을 확인 — 사유 성립.

### A-02 검증
- direction 재계산: 허용목록 14→15항목, `comm` → added=1
  (`.harness/sprint-amendments-howto-kit-implementation.md`), removed=0 → `relaxing` (기계적
  `amend_direction()`과 일치 — 이 amendment는 허용목록 자체를 바꾸는 정통 케이스).
- 사유 검증: `harness/references/contract-schema.md:99-108` §산출물 3 종을 직접 Read로 확인.
  "계약·QA 산출물·amendment 사이드카 3 종은 같은 슬러그로 짝지어진다"는 문장이 실재하며,
  원 AR-07 허용목록이 세 번째 산출물(사이드카)을 누락했다는 A-02의 주장은 스키마 원문과 부합한다.

### consent 앵커 직접 검증 (A-01·A-02 공통)
- `~/.claude/logs/claude-plugins/2026-09.md` line 26535에서
  `## [prompt] 2026-09-08T15:29:57+0900` / `session: 0e3335f2-8d08-4e29-8a5d-01ec6b7ed620` /
  `cwd: /Users/jackson/Hub/10_Dev/claude-plugins` / 본문 `ㄱㄱ` 을 그대로 확인 — 사이드카의
  인용과 100% 일치.
- session이 계약 frontmatter의 `owner_session`과 일치 확인.
- 직전 사용자 프롬프트 `어디까지 진행한거야`가 **같은 세션**에서 line 26410
  (`2026-09-08T15:28:47+0900`)에 실재함을 확인 — `ㄱㄱ` 70초 전, 사이드카의 맥락 서술과 부합.
- **한계**: 이 로그는 UserPromptSubmit 훅(log-prompt)이 **사용자 프롬프트만** 기록하고
  어시스턴트 응답은 기록하지 않는 구조다. 따라서 "어디까지 진행한거야"와 "ㄱㄱ" 사이 70초간
  어시스턴트가 실제로 A-01/A-02 확정을 요청하는 문장을 말했는지는 이 로그만으로 **직접 확인이
  불가능**하다 (구조적 한계이지 조작 정황은 아니다).
- 사이드카가 언급한 "AskUserQuestion 클릭"에 대해서도 별도로 조사했다: 세션
  `0e3335f2-8d08-4e29-8a5d-01ec6b7ed620` 전체(2026-09 로그 파일 전수)에서 `AskUserQuestion`
  tool_use 호출을 검색했으나 **0건**이었다. 다만 이 로그는 사용자 프롬프트만 기록하므로
  이 결과가 "AskUserQuestion이 호출되지 않았다"를 증명하지는 못한다(도구 호출 자체가 애초에
  이 로그의 기록 대상이 아니다) — 그러나 그 서사를 로그로 뒷받침할 수도 없다는 뜻이므로,
  이 부분은 **불충족 검증(플레이스홀더 서사)**으로 표시하고 넘어간다.
- **판정**: 스키마가 요구하는 `anchored`의 정의("사용자 발언 인용 + reflect-kit prompt 로그
  앵커(timestamp·session·cwd)")는 3요소 모두 실측으로 확인됐고 위조 정황이 없다. 따라서
  `consent: anchored`로 인정한다. 다만 앵커가 담보하는 것은 "이 시점에 이 세션에서 사용자가
  `ㄱㄱ`라고 입력했다"까지이며, 그 발화가 정확히 "A-01+A-02 둘 다"를 향한 것인지는 로그
  구조상 검증 불가능한 잔여 불확실성으로 남는다는 점을 명시한다.

## User Correction Audit
- correction_log_status: available
- unreflected_corrections: 0 (스프린트 기간 내 계약/amendment 어디에도 반영 안 된 방향 교정 없음 —
  amendment 사이드카 자체가 이미 사용자 확인을 거친 교정 반영 경로였음)
- verdict 영향: 없음 (표면화 전용)

## Results

### Skill (5/5)
- [x] SK-01: 3 SKILL.md 존재 + frontmatter 3필드 비어있지 않음 — PASS
  - 근거: `python3 scripts/validate-plugin.py howto-kit --check=frontmatter` → "V1 frontmatter 3 skills + 1 agent — OK". `howto-kit/skills/{howto,howto-doc,howto-audit}/SKILL.md` 각각 Read로 name/description/user-invocable 실값 확인 (예: `howto-kit/skills/howto/SKILL.md:2-13`)
- [x] SK-02: `howto-kit/agents/howto-reviewer.md` 4필드 + Write/Edit/NotebookEdit 부재 — PASS
  - 근거: `grep -n '^tools:' howto-kit/agents/howto-reviewer.md` → `tools: Read, Grep, Glob` (Write/Edit/NotebookEdit 없음). V1 "1 agent — OK"
- [x] SK-03: howto/howto-audit allowed-tools에 Write/Edit 없음, howto-doc엔 Write 있음 — PASS
  - 근거: `grep -n '^allowed-tools:' howto-kit/skills/{howto,howto-audit,howto-doc}/SKILL.md` →
    `howto/SKILL.md:14: Read, Grep, Glob, WebFetch, WebSearch` / `howto-audit/SKILL.md:14: Read, Grep, Glob, Bash, Agent` / `howto-doc/SKILL.md:12: Read, Write, Grep, Glob, Bash, WebFetch, WebSearch`
  - 의심 조사: howto-audit의 Bash·Agent가 "읽기 전용" 요구와 충돌하는지 Process 섹션 전문(Phase 1~4, Gotcha 5)을 직접 추적. Bash는 `find`(파일 수 카운트)와 `howto_gate` 실행(판정만, 대상 파일 미변경)에만 쓰이고, Agent는 read-only 도구셋(Read/Grep/Glob)만 가진 howto-reviewer 호출용. Gotcha 5 "이 스킬은 Write 를 갖지 않는다... 감사자가 자기 감사 대상을 고치면 그 감사는 증거가 아니다"로 설계 의도가 명시. 충돌 없음.
- [x] SK-04: evals.json 유효 JSON, 9케이스(≥6), 입도케이스 2건(≥2) — PASS
  - 측정값: 총 9케이스 (기준 ≥6) / 입도케이스 2건 (기준 ≥2) — `E2-granularity-terminal-action`(nonterminal=2 탐지, (a)), `E3-granularity-verify-and-branch`(no_verify=2, no_branch=2 탐지, (b)+(c))
  - 근거: `python3 -c "json.load(...); len(cases)"` → 9. `E8-zero-steps`는 assertions가 `G6_GRANULARITY PASS steps=0`으로 위반탐지가 아니라 로버스트니스 케이스라 입도케이스에서 제외
- [x] SK-05: 4개 description 트리거 키워드 set intersection 공집합 + substring pair 0건 — PASS
  - 근거: python으로 4개 파일 description의 따옴표 인용구 추출(howto 8개/howto-doc 5개/howto-audit 5개/howto-reviewer 0개) 후 전체 pairwise 교집합·substring 검사 — 교집합 전부 empty, substring pair count 0

### Script (6/6)
- [x] SC-01: G1~G6 단일함수, 정상입력 zsh/bash 동일출력 — PASS
  - 근거: `zsh -c '. howto-kit/scripts/howto-gate.sh; howto_gate .../pass-fcm-ios.md'` vs `bash -c '...'` 실행, `diff` 결과 동일 (G1_LEDGER~G6_GRANULARITY 6줄 + GATE_PASS)
- [x] SC-02: G5/G6 양성위반 케이스 zsh/bash에서 FAIL 확인 — PASS
  - 근거: `fail-g5-nonterminal.md` → 양쪽 셸 `G5_TERMINAL FAIL nonterminal=2 hedge=2` + `GATE_FAIL`. `fail-g6-granularity.md` → 양쪽 셸 `G6_GRANULARITY FAIL ... no_verify=2 no_branch=2` + `GATE_FAIL`. 4벌 출력 모두 확인
- [x] SC-03: sync-docs.py howto-kit → exit0, --check-only → exit0 — PASS
  - 근거: `python3 scripts/sync-docs.py howto-kit` exit 0 ("변경 없음" 3건). `python3 scripts/sync-docs.py --check-only` exit 0, 마지막 줄 "모든 README가 동기화 상태입니다"
- [x] SC-04: validate-plugin.py howto-kit 8카테고리 FAIL 0, 전킷 실행 새 FAIL 0 — PASS
  - 근거: `python3 scripts/validate-plugin.py howto-kit` → V1~V8 전부 OK, exit 0. `python3 scripts/validate-plugin.py`(인자없음) → "Total: 14 plugins, 14 OK", exit 0
- [x] SC-05: sync-orchestrator.py에 howto-kit 매핑 + kaizen-orchestrator에 howto-kaizen Phase — PASS
  - 근거: `grep -n 'howto-kit' scripts/sync-orchestrator.py` → line 115, 126 (`"howto-kit": "docs/howto/"`). `python3 scripts/sync-orchestrator.py` → "이미 동기화됨 (13 plugins)" exit 0. `grep -n 'howto-kaizen' .claude/skills/kaizen-orchestrator/SKILL.md` → line 501, `### Step 17: Phase 17 — howto-kit 카이젠`이 AUTO:plugin_phases 마커(387~506) 내부에 위치함을 라인번호로 확인
- [x] SC-06: check-external-links.py KIT_DIRS에 howto-kit 포함 — PASS
  - 근거: `grep -n 'howto-kit' scripts/check-external-links.py` → line 38, `KIT_DIRS = [..., "howto-kit"]`

### Error (3/3)
- [x] ER-01: 브리프 §11 미확인 4건 처리(재확인 또는 등급표기) — PASS
  - 근거 (표):
    | 항목 | 처리 | 근거 파일:라인 |
    |---|---|---|
    | 체크리스트 방법론 1차출처 | (b) [미확인] | `howto-kit/references/step-contract.md:117-121` "근거 등급 [미확인]... 1 차 출처를 확보하지 못했다" |
    | MS Learn 권한 인용 2건 | (a) 재확인+대체 | `howto-kit/references/navigation-anchors.md:83,85` 원 미확인 인용 대신 새로 확인된 2개 URL을 "(확인 2026-09-08)" 표기로 인용, `provenance-notes.md` §2에 원 실패 URL 기록 |
    | RSS 피드 실측 | (b) provenance-notes에 등급 원장 | `howto-kit/references/provenance-notes.md` §3, 4건 확인/2건 확인실패 구분. `docs/howto/changelog-feeds.md`(소비처)는 아직 미생성이라 확정사실로 소비되지 않음 |
    | 이름충돌 검사 | (b) [미확인] | `provenance-notes.md` §4 "## 4. howto-kit 이름 충돌 검사 — [미확인]" |
  - 교차확인: `grep -rn "충돌 없\|npm" howto-kit/ .claude/skills/howto-*/ docs/howto/` → design-brief.md:392만 매치, "검사를 하지 않았다"로 미확정임을 명시 (확정사실로 오용 없음)
- [x] ER-02: 존재하지않는 파일→GATE_BLOCKED exit0, 빈파일→6줄+안죽음, zsh/bash — PASS
  - 근거: `howto_gate /nonexistent/x.md` 양쪽 셸 `GATE_BLOCKED no_such_file=/nonexistent/x.md` EXIT=0. 빈파일(`empty.md`) 양쪽 셸 6개 게이트줄 + `GATE_FAIL` EXIT=0
  - 음성대조 실행(규칙12 — 입력검증 카테고리 해당, 안전조건 3개 충족: 파일 clean·1지점 변형·diff 범위 내): `[ -f "$g" ]` 가드라인(45번째 줄) 삭제 후 재실행 → `awk: can't open file`, `grep: ... No such file or directory` 에러 출력으로 오염됨 (GATE_BLOCKED 대신). 계약의 음성대조 서술과 일치. `git diff --exit-code -- howto-kit/scripts/howto-gate.sh` 로 원상복구 확인
- [x] ER-03: G6 추정비율 0으로나누기 없음, 액션 0건 입력 — PASS
  - 근거: `howto-kit/scripts/howto-gate.sh:166-170` `if [ "$steps" -gt 0 ]; then gpct=$((...)); else gpct=0; fi` 가드 확인. `edge-zero-steps.md` 실행 결과 양쪽 셸 정상 6줄 출력, `divide`/`error` grep 매치 0건

### Architecture (7/7)
- [x] AR-01: plugin.json 파싱, name=howto-kit, version/description 비어있지 않음 — PASS
  - 근거: `python3 -c "..."` → `howto-kit 0.1.0 77`
- [x] AR-02: Step Contract 필드정의가 step-contract.md 1곳에만 — PASS
  - 근거: `grep -rn 'if_not_found\|target_label\|source.tier' howto-kit/` 전체 매치 중 필드정의 형태(`target_label: string`, `if_not_found:`, 표 행 `source.tier`)는 `step-contract.md:22,23,28,42,46,47,48`뿐. 다른 6개 파일의 매치는 전부 `../../references/source-tiers.md`/`step-contract.md` 파일 경로 참조. `howto-kit/skills/howto/SKILL.md:232` "step-contract.md — Step Contract 스키마 정본 (여기서만 정의한다)"로 설계 의도 명시적 확인
- [x] AR-03: marketplace.json entry + 버전태그 + 버전일치 — PASS
  - 근거: `python3 scripts/validate-plugin.py howto-kit --check=plugin-json` → "V7 plugin-json v0.1.0 matches marketplace — OK". entry description "[v0.1.0 · 2026-09-08] ..."로 시작 확인
- [x] AR-04: CLAUDE.md Repository Overview + Skills Reference 4개 열거 — PASS
  - 근거: `grep -n 'howto' CLAUDE.md` → line 23(Repository Overview), line 294(섹션제목), 298(/howto), 299(/howto-doc), 300(/howto-audit), 301(howto-reviewer)
- [x] AR-05: docs/howto-kit/*.html 1개 이상 + index.html 등록 + 경로실재 — PASS
  - 근거: `docs/howto-kit/overview.html` 존재(374줄). `grep -n 'howto-kit/' docs/index.html` → line 568 `file: 'howto-kit/overview.html'`. `test -f docs/howto-kit/overview.html` exit 0
- [x] AR-06: howto-kaizen/howto-research SKILL.md 존재 + name/description — PASS
  - 근거: `head -6 .claude/skills/howto-kaizen/SKILL.md`, `head -6 .claude/skills/howto-research/SKILL.md` 둘 다 frontmatter에 name/description 확인
- [x] AR-07: 변경경로 전부 15항목 허용목록 내 (개정 baseline 54fb3b3, amendment A-01+A-02 적용) — PASS
  - 측정값: 총 37경로 (기준: 15항목 허용목록 내 100%) / 허용목록 밖 0건
  - 근거: HEAD=`b1a0f4d` 확인 후 `git diff --name-only 54fb3b3..HEAD -- . ':(exclude).harness/handoff/*' ':(exclude)docs/bambu-calibration/*'` → 37줄. python으로 15항목 허용목록 접두 매치 전수검사 → violations=0

### Anti-patterns (2/2)
- [x] AP-03: bare code fence 금지 — PASS
  - 근거: `python3 scripts/validate-plugin.py howto-kit --check=code-fence` → "V6 code-fence 0 bare — OK"
- [x] AP-04: frontmatter name 필드 누락 없음 — PASS
  - 근거: `python3 scripts/validate-plugin.py howto-kit --check=frontmatter` → "V1 frontmatter 3 skills + 1 agent — OK"

### Reusability (2/2)
- [x] RE-01: 재사용 가능 컴포넌트를 private으로 만들지 않음 — PASS
  - 근거: 3 스킬 + 1 에이전트 전부 marketplace/plugin.json에 등록되어 공개 상태. 컴포넌트를 숨긴 정황 없음
- [x] RE-02: 기존 유사 컴포넌트 재사용 확인 — PASS
  - 근거: `grep -rl "G1_\|G2_\|G3_\|GATE_PASS\|GATE_FAIL" scripts/ onboarding-kit/` → 프로덕션 스크립트 중복 없음. 계약 자체 리서치소스가 밝히듯 onboarding-kit의 guide_gate()(G1~G4)는 "원형"으로만 참조했고, G1~G6로 판정기준이 달라 별도 구현이 정당함(비범위: onboarding-kit 무수정 제약과도 부합)

### Diagnostics (3/4, 1건 [미검증:ENV])
- [x] DG-01: `bash -n scripts/release.sh` 워닝 0개 — PASS
  - 근거: `bash -n scripts/release.sh` exit 0, 출력없음. 확장검사로 `howto-kit/scripts/howto-gate.sh`, `howto-kit/evals/run-evals.sh`를 sh/bash/zsh 3셸 `-n` 전부 OK
- [ ] DG-02: IDE diagnostics 워닝/인포 0개 — [미검증:ENV]
  - 남용방지 4요건: (1) 1차 도구 시도: 이 세션에 IDE Problems 패널 MCP 도구가 연결되어 있지 않음 (`project.yaml runtime_inspection.mcp_server: null`, 세션 tool 목록에 IDE 진단 도구 부재) (2) fallback 시도: `python3 -m py_compile scripts/sync-orchestrator.py scripts/check-external-links.py` + `json.load()`(plugin.json/evals.json/marketplace.json) + `yaml.safe_load()`(howto-kit 전체 .md 프론트매터 + howto-kaizen/howto-research) 전부 실행, 결과 0 에러 (3) 실패로그: 위 fallback 명령 자체 실행 출력을 그대로 인용("python compile OK", "frontmatter YAML errors: 0") — IDE 도구 부재는 도구 목록에 항목이 없다는 사실 자체가 로그임 (4) 통제불가사유: 이 QA 세션에는 IDE MCP가 configure되지 않음(project.yaml 설정 그대로). 재검증 명령: VSCode/Cursor로 `howto-kit/` 을 열고 Problems 패널 확인, 또는 `mcp__ide__getDiagnostics` 연결된 세션에서 재평가
- [x] DG-03: `bash scripts/release.sh 2>&1` 콘솔 에러/예외 0개 — PASS
  - 근거: 인자없이 실행 → Usage 안내 + howto-kit 포함 플러그인 목록 출력(정상 usage 메시지, 에러/예외 문자열 없음), exit 0
- [x] DG-04: 실앱/서버 구동 에러 — N/A (타당성 확인) — PASS
  - 근거: `project.yaml`의 `runtime_inspection: {mcp_server: null, vm_port: null, launch_script: null}`과 `stack: shell-scripts`가 이 킷에 실행형 앱/서버가 없다는 N/A 사유와 일치. 대신 지목된 SC-01·SC-02·ER-02가 게이트 함수의 실제 런타임 실행(zsh+bash, 정상+양성위반+엣지케이스)을 이미 수행·검증했음을 위 Results에서 직접 확인

## Unverifiable Summary
- invalid_evidence: 0
- env_gaps: 1  [DG-02, IDE MCP 도구 부재, 정적 fallback(py_compile+json/yaml load) 수행 및 0에러 확인, 재검증 명령: IDE Problems 패널 또는 mcp__ide__getDiagnostics 연결 세션]
- verified_coverage: (29 - 1) / 29 = 0.97  (임계 0.60)
- 연속 ENV 승급: 없음 (DG-02는 이번 iteration에서 최초 조사 — 이전 iteration 3의 REJECT 사유는 다른 조건들이었음)
- Verdict 영향: 통상 (env_gaps 1건은 자동 REJECT/BLOCKED 임계 미달, coverage 0.97 >> 0.60)

## Discrimination (규칙 12 적용 조건)
- 적용 조건: [ER-02 — 입력 검증 카테고리]
- 결합 확인: ER-02 — 측정이 `howto-kit/scripts/howto-gate.sh`의 실제 `howto_gate()` 함수를 zsh/bash로 직접 source+호출함 (재작성된 독립 테스트 아님). SC-01/SC-02/SK-04도 동일 함수를 `run-evals.sh`가 직접 source하여 실행 (`howto-kit/evals/run-evals.sh:12,32-33` `. "$GATE"`)
- 음성 대조: ER-02 — 계약에 기재됨("`[ -f "$g" ]` 가드를 제거하면... FAIL한다"). 안전조건 3개 충족(파일 git-clean, 1지점 변형, diff 범위 내)하여 실행 음성대조 수행 — 가드 제거 시 실제로 에러 오염 발생 확인, `git diff --exit-code`로 원상복구 확인

## Evidence Validity
- 검사 대상 증거: 29건 (조건별 1건 이상)
- 무효 판정: 0건
- 셸 스니펫 실행 검증: 실행 8건 이상(howto_gate 정상/양성위반/엣지케이스/음성대조 각 zsh+bash) · zsh/bash 양쪽 확인 전부(SC-01·SC-02·ER-02·ER-03) · 미실행 0건
- 무효 0건은 미검증 카운터에 영향 없음 (현재 누계: invalid_evidence=0, env_gaps=1)

## Summary
- Total: 29/29 conditions passed (28 직접 PASS + 1 [미검증:ENV] — coverage 게이트 통과로 실질 통과 처리)
- Verdict: **APPROVE**
- 봉인 SEAL_OK, amendment 2건 모두 direction·consent 재계산 결과 PASS 근거 성립(단 A-01의 기계적 amend_direction 오분류 위험 및 consent 앵커의 구조적 잔여 불확실성은 Improvement로 기록), AR-07 현재 HEAD 기준 재측정 0 위반 확인.

## Improvement Suggestions
- [AR-07] 검증경로-미기재 — `amend_direction()` 헬퍼(contract-schema.md §Amendment 사이드카)는 "허용목록 자체의 증감"을 재는 용도로 설계되어 있으나, A-01처럼 **측정 베이스라인/스코프**를 바꾸는 amendment에 기계적으로 적용하면 오분류(narrowing으로 오판)를 유발한다. 스키마에 "베이스라인/스코프형 amendment는 실제 FAIL→PASS 여부를 실측 비교로 판정하고, 집합 자체가 바뀌는 허용목록형 amendment만 comm 계산을 쓴다"는 분기 문장을 추가할 것을 제안.
- [A-01/A-02 consent] 측정-환경-오염 — reflect-kit의 UserPromptSubmit 훅은 사용자 프롬프트만 기록하고 어시스턴트 응답은 기록하지 않는 구조라, "그 발화가 정확히 어떤 동의 요청에 대한 응답인지"는 timestamp 근접성으로만 추론 가능하고 내용 대조로 확정할 수 없다. 향후 `relaxing` amendment의 consent 앵커에는 어시스턴트가 사용자에게 무엇을 확인 요청했는지 사이드카 자체에 (로그가 아니라) **그 순간의 확인 요청 문장을 직접 인용**해 남기면, 로그의 구조적 한계와 무관하게 맥락이 자기완결적으로 검증 가능해진다.
