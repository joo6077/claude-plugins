# Sprint Feedback (재평가 — Phase 12a)
Feature: 카이젠 Phase 12 — reflect-kit 태그 정규화 결정론화(K1) + hook coverage audit 라우팅(K2) + 파편화 게이트로 calibration 무효화(K3)
Evaluated: 2026-08-14 11:24 (재평가 — 원 판정이 글로벌 피드백 풀에 저장되지 않아 독립 재수행)
Verdict: REJECT
Iteration: 1 (재평가 — 이전 판정을 승계하지 않고 전 조건 직접 재검증)

## Contract Fingerprint
- path: .harness/sprint-contract-kaizen-phase12-tag-canonicalization.md
- sha256(전체 파일): 36364016d5e3de255df5ba9de88765d26b95ae4af00425724ad38e4f1adbea98
- conditions_digest(봉인, 조건 줄만): sha256:d85f4d7e5644ea3a → **SEAL_OK** (재계산값과 일치, command grep 으로 재확인)
- status: done (frontmatter 명시 — 이미 종료 상태, 이번 재평가로 변경하지 않음)
- slug: kaizen-phase12-tag-canonicalization
- contract_root: /Users/jackson/Hub/10_Dev/claude-plugins
- contract_root_unconfigured: false
- 선택 근거: 오케스트레이터 명시 경로 지정 (ladder 1 상당) — owner_session 도 현재 세션과 일치 (df1b3e15-30b3-4825-a3c4-4ac44c686e94) 하여 ladder 2 로도 유일 성립
- legacy_contract_used: false
- 조건 수 재계산: 29 (frontmatter `conditions: 29` 와 일치) — command grep -cE 로 직접 카운트
- 재확인(Step 5, 평가 종료 직전): 일치 (git status --porcelain 상 무변경, SEAL_OK 유지) — TOCTOU 없음
- status_transition: skipped (verdict=REJECT — REJECT 는 상태 전환 대상 아님. status 는 이미 done 이었고 이번 재평가로도 되돌리지 않음)

## 재평가 배경 (원인 요약)
원 판정(APPROVE로 추정)은 오케스트레이터가 QA 서브에이전트에 structured output schema 를
강제해 피드백 저장 단계가 실행되지 않아 글로벌 피드백 풀에 누락됐다. 본 재평가는 그 판정을
승계하지 않고 29개 조건 전부를 실행 기반으로 독립 재검증했다. 그 결과 **SC-04 에서 계약이
스스로 명시한 음성 대조(negative control) 등식이 문자 그대로 성립하지 않는 결함을 발견**했다
(구현 결함이 아니라 계약 측정문의 정밀도 결함). 1 FAIL = REJECT 원칙에 따라 REJECT로 판정한다.

## Amendments (사이드카 — sprint-amendments-kaizen-phase12-tag-canonicalization.md)
- amendments: 3
- narrowing: 0
- relaxing: 0
- unknown: 2 (AM-01, AM-03 — "narrowing 아님 · widening 아님", 사용자 앵커 없음 → PASS 근거 불가,
  원 조건 문자 그대로 판정. 아래 SC-04/SC-02 판정에 **amendment의 자체 결론(PASS)을 그대로
  받아들이지 않고** 내가 직접 재실행하여 독립적으로 확인했다)
  - [AM-01] SC-04 음성 대조 절이 "제거 대상 2종(alias/verb-synonym)"만 가정했으나 실제로는
    3번째 종류(synonym, docs→doc)도 관여함을 신고 → 관련 조건: SC-04
  - [AM-03] SC-02 원 측정문이 cwd 축을 교차하지 않아 거짓 PASS 를 허용했음을 신고 (구현은 이미
    수정됨) → 관련 조건: SC-02
- 기타 1건 (AM-02): 조건과 무관한 환경 사고 기록(병렬 세션의 git stash 로 인한 미커밋 변경
  일시 소실 및 복구) — 판정에 영향 없음, 참고용으로만 기록

## User Correction Audit
- correction_log_status: available (~/.claude/logs/claude-plugins/2026-08.md)
- unreflected_corrections: 0 (Phase 12 스프린트 구간(2026-08-13 15:20 이후) 사용자 프롬프트 로그를
  검토했으나 계약/amendment 에 반영되지 않은 사용자 방향 교정을 발견하지 못했다. 해당 구간
  프롬프트는 대부분 오케스트레이터 자동 워크플로 알림과 "ㄱㄱ"(진행) 승인이었다)
- verdict 영향: 없음 (표면화 전용)

## Results

### Skill (7/7)
- [x] SK-01: 정규화 SSOT 경로 참조 3개 SKILL.md 전부 — PASS
  - 근거: `command grep -l 'tag-canonicalization.md' reflect-kit/skills/{reflect-digest,reflect-promote,reflect-kaizen}/SKILL.md` → 3행. L3: 각 인용이 실제 SSOT 참조 문맥(규약/데이터/실행 함수 지목)임을 Read로 확인 (reflect-digest/SKILL.md:30, reflect-promote/SKILL.md:31,244, reflect-kaizen/SKILL.md:198)
- [x] SK-02: `tag_canon_groups` 1차 근거 지정 — PASS
  - 근거: `reflect-kit/skills/reflect-digest/SKILL.md:30` — `grep -c 'tag_canon_groups'` = 5 (>=1), 같은 줄(30)에 "결정론적 pass" 문자열도 존재
- [x] SK-03: `§B-0` hook coverage audit 9항목 — PASS
  - 근거: `reflect-kit/skills/reflect-promote/SKILL.md:148` `### B-0.` 헤더 1개. 9개 토큰(hook installed/event type/matcher/path normalization/exit code/timeout/executable/dependency/fired-blocked) 전부 표(148-166줄)에서 1회 이상 확인 (command grep 개별 실행, sibling 전수 확인)
- [x] SK-04: `demote-candidate` 금지 (`blocked-low-confidence`) — PASS
  - 근거: `reflect-kit/skills/reflect-kaizen/SKILL.md` `blocked-low-confidence` 4회 등장, 그중 138줄이 `verdict` 열거 정의 줄
- [x] SK-05: family(병합 금지) 섹션 — PASS
  - 근거: `reflect-kit/skills/reflect-digest/SKILL.md:309` `## 원인 계열 (family) — 병합하지 않음 (합산 금지)` 1개
- [x] SK-06: 구 임계값 `1.5` 0건 — PASS
  - 근거: `command grep -rn '1\.5' reflect-kit/skills reflect-kit/references` → 0행 (이스케이프/비이스케이프 양쪽 확인)
- [x] SK-07: `PostToolUse` 비예방 명시 2표면 — PASS
  - 근거: `reflect-kit/skills/reflect-promote/SKILL.md:112`(hook절 표) + `:232`(안티패턴) 각 1회

### Script (5/6)
- [x] SC-01: `canonical → aliases` 어휘 주입 — PASS [실행 검증]
  - 근거: `log-reflection.sh:123-163` 어휘 생성 구간을 sed 로 원문 그대로 추출해 fixture(edited-before-read×1, edit-before-read×2, ignored/skipped-required-api-doc-check×1, used-stale-widget-ref×1)로 실행 → 출력에 `- edit-before-read  (freq 3)  ← 같은 뜻으로 쓰인 다른 표기: edited-before-read(1)` 행 정확히 존재. 음성 대조: `tag-lemma-map.tsv` 의 `verb` 행 제거 후 재실행 → 해당 행 사라짐(`freq 2`, alias 주석 없음) 확인
- [x] SC-02: `tag_canon_fragmentation` 셸·cwd 무관 동일 출력 — PASS [실행 검증]
  - 근거: bash·zsh·sh(sh-mode) × cwd(`/tmp`,`$HOME`,`/`,`hooks/`) = 12회 절대경로 source 실행 → 전부 `5\t3\t6\t1\t1.67\t0.333\t2.00`, `sort -u` 1행. AM-03 이 신고한 cwd 미교차 결함은 구현 수정(`tag_canon_map_path()` 가 cwd 미사용) 후 내가 직접 12조합으로 재현해 확인 — amendment 서술을 신뢰하지 않고 독립 재실행함
- [x] SC-03: lemma map 불가 시 fail-open — PASS [실행 검증]
  - 근거: `REFLECT_TAG_LEMMA_MAP=/nonexistent` 로 어휘 생성 구간 실행 → rc=3, `.errors.log` 상당 `log_hook_error` 호출에 `warn:lemma-map-unreadable path=/nonexistent ...` 1행, 어휘 블록 비어있지 않음(`- edit-before-read  (freq 2)`). 음성 대조: 정상 경로(맵 정상)에서 동일 로그 함수 호출 중 `warn:lemma-map-unreadable` 0건 확인
- [ ] SC-04: 실로그 전량에서 클러스터 합산 > 원시 단독, 음성 대조 등식 — **FAIL**
  - 근거(주 측정, PASS): `tag_canon_groups ~/.claude/logs/*/reflections-*.md` 의 `skipped-required-api-doc-check` 클러스터 = **125** > 원시 단독(`grep|sort|uniq -c`) = **86** (2026-08-13 authoring 시점 값 110>71 에서 실로그 누적으로 더 커짐 — 효과 지속 확인)
  - 근거(음성 대조, FAIL): 계약 문언 "`alias`/`verb-synonym` 행을 제거한 맵으로 실행하면 **두 값이 같아져야 한다**" — 직접 재실행 결과 제거 후 클러스터 = **87**, 원시 단독 = **86**. **87 ≠ 86, 문자 그대로 등식이 성립하지 않는다** (독립 재현, amendment AM-01 의 자체 진단과 정성적으로 일치하나 그 결론(PASS)은 그대로 채택하지 않고 내가 직접 재검증함). 원인: 제거 대상에 포함되지 않은 3번째 매핑 종류(`synonym`, `docs→doc`)가 `skipped-required-api-docs-check`(복수형) 1건을 추가로 접어 off-by-one을 만든다
  - CheckEval 서브체크 분해: (a) 클러스터 합산 > 원시 단독 → PASS, (b) 음성 대조 등식 → FAIL. 계약 자체의 "·" 결합 관례(SC-01/SC-03 에서 동일 패턴이 AND로 요구되고 실제로 양쪽 다 충족됨)에 따라 두 서브체크 모두 충족해야 조건 전체가 PASS이므로, 하나라도 FAIL이면 조건은 FAIL (복합 조건 분해 프로토콜)
  - amendment AM-01 은 "narrowing 아님·widening 아님"·사용자 앵커 없음 → `unknown` 분류. 프로토콜상 PASS 근거로 쓸 수 없어 원 조건 문언 그대로 판정했다
  - 수정 방향: (1) 이번 사이클 한정으로는 실질적 결함이 아니다 — 결정론적 pass의 핵심 효과(과소집계 해소)는 견고하게 입증됨. (2) 다음에 이 조건을 재사용한다면 음성 대조를 "맵 전체(모든 kind)를 제거하면(순수 kebab) 두 값이 같아져야 한다"로 재작성할 것(전체 맵 제거 시 86==86 정확히 성립함을 확인) — amendment AM-01 이 이미 제안한 문구와 동일
- [x] SC-05: shellcheck 0 findings — PASS
  - 근거: `shellcheck reflect-kit/hooks/_lib-tag-canon.sh reflect-kit/hooks/log-reflection.sh` 출력 0행, exit 0 (shellcheck 0.11.0)
- [x] SC-06: `tag_canon_fragmentation` 7열/6열=singleton_share — PASS
  - 근거: 출력 `5 3 6 1 1.67 0.333 2.00` → 필드수 7, 6번째 열 0.333 (0~1 범위)

### Error (3/3)
- [x] ER-01: 빈 로그 디렉토리 → `(없음 — 첫 수집)`, 비정상 종료 없음 — PASS [실행 검증]
  - 근거: 빈 디렉토리로 어휘 생성 구간 실행 → 출력에 `(없음 — 첫 수집)` 포함, 스크립트 exit 0, 셸 오류 0줄
- [x] ER-02: dedup 게이트·codex fallback 미변경 — PASS
  - 근거: Given 절("커밋 직전 working tree")이 현재는 전부 커밋된 상태라 문자 그대로 재현 불가 — Phase12 구현 커밋 범위(`0fe357a^..f62691f`)를 대체 상태로 사용(명시). `git diff -U0 0fe357a^..f62691f -- reflect-kit/hooks/log-reflection.sh` 에서 `try_claude_fallback`/`env_state`/`REFLECT_ENV_REPEAT_DAYS` 포함 변경줄 0건. 세 심볼 모두 파일에 그대로 존재(237, 317-327줄)함도 확인
- [x] ER-03: `new_tag_reason` 선택 필드 — PASS
  - 근거: `log-reflection.sh:181` "canonical 을 재사용했으면 이 줄 자체를 생략한다" + `reflect-digest/SKILL.md:84` "(선택 필드)" 스키마 주석. L3: reflect-digest/promote/kaizen 어디에도 이 필드 부재를 파싱 실패로 다루는 로직 없음(관련 언급 4곳 모두 선택적 서술)

### Architecture (5/5)
- [x] AR-01: 변경이 Scope 내부 6항목과 정확히 일치 — PASS
  - 근거: Given 상태 재구성 — Phase12 커밋 범위(`0fe357a^..f62691f`) diff --name-only: `hooks/_lib-tag-canon.sh`(신규), `hooks/log-reflection.sh`, `references/tag-canonicalization.md`(신규), `references/tag-lemma-map.tsv`(신규), `skills/reflect-digest/SKILL.md`, `skills/reflect-kaizen/SKILL.md`, `skills/reflect-promote/SKILL.md` — 7개 물리 파일이 `references/` 1항목으로 묶이면 계약이 명시한 6항목과 정확히 일치 (계약 자체의 Diff-Scope baseline 서술과도 동일 집합)
- [x] AR-02: 매핑 데이터 SSOT 1곳 — PASS
  - 근거: `command grep -rln 'verb-synonym' reflect-kit/` 4개 파일 매치되나, 실제 데이터 행(`^verb-synonym<TAB>`)을 담은 파일은 `tag-lemma-map.tsv` 1개뿐 (나머지는 프로즈/코드에서 문자열만 언급)
- [x] AR-03: `edited-before-read` 규범 예시 0건 — PASS
  - 근거: `log-reflection.sh` 내 `edited-before-read` 0건, `edit-before-read` 1건(214줄, 최빈형 예시로 정정됨)
- [x] AR-04: `really bad groups` 인용 0건 — PASS
  - 근거: `command grep -rn 'really bad groups' reflect-kit/` 0행. `tag-canonicalization.md:87` 에 "이전 판본이 직접 인용하던 문구는 재확인 실패" 정정 서술 확인(그 자체가 인용 재현이 아님을 Read로 확인)
- [x] AR-05: Scope 밖 파일 미변경 — PASS
  - 근거: Phase12 커밋 범위(`0fe357a^..f62691f`)에서 `reflect-kit/{docs,README.md,hooks/hooks.json,scripts,.claude-plugin}` diff 0행. **참고**: 전체 카이젠 사이클(main..HEAD) 범위에서는 이후 별도 커밋(`03669c7`, "11킷 버전 bump" — Phase12 전용 작업이 아닌 전 킷 공통 릴리스 준비 커밋)이 `reflect-kit/.claude-plugin/plugin.json` 1건을 건드렸으나, 이는 Phase12 구현자의 scope 위반이 아니라 별개의 사이클 차원 작업이므로 AR-05 판정에서 제외했다 (Given 상태 불명시로 인한 대체 상태 사용 — Step 1.5 항목6 플래그)

### Anti-patterns (2/2)
- [x] AP-03: bare code fence 0건 — PASS
  - 근거: `python3 scripts/validate-plugin.py reflect-kit --check=code-fence` → `V6 code-fence 0 bare — OK`, exit 0
- [x] AP-04: SKILL.md frontmatter `name` 유지 — PASS
  - 근거: `python3 scripts/validate-plugin.py reflect-kit --check=frontmatter` → `V1 frontmatter 4 skills — OK`, exit 0

### Reusability (2/2)
- [x] RE-01: 정규화 로직이 `_lib-tag-canon.sh` 한 곳에만 — PASS
  - 근거: `command grep -rln 'function norm\|tolower(s)' reflect-kit/` → `_lib-tag-canon.sh` 1개뿐
- [x] RE-02: 훅이 `source "$SCRIPT_DIR/_lib-*.sh"` 규약 3회 — PASS
  - 근거: `command grep -c 'source "\$SCRIPT_DIR/_lib-' reflect-kit/hooks/log-reflection.sh` = 3 (16/18/20줄: _lib-project-id.sh, _lib-redact.sh, _lib-tag-canon.sh)
  - **주의**: 이 저장소의 `grep` 은 `ugrep -G` 로 셸 함수 wrapping 되어 있어 mid-pattern `$` 를 오처리하고(BRE 규칙과 다르게 앵커로 취급), wrapped grep 으로는 이 조건이 **거짓으로 0** 이 나왔다. `command grep`(실제 `/usr/bin/grep`)으로 재검증해 3을 확인했다 — 이 재확인이 없었다면 RE-02 를 오탐 FAIL 처리할 뻔했다 (환경 함정, 계약/구현 결함 아님)

### Diagnostics (4/4)
- [x] DG-01: `validate-plugin.py reflect-kit` V1~V8 전부 OK, exit 0 — PASS
  - 근거: 전체 실행 결과 V1~V8 전부 OK, `Exit: 0`
- [x] DG-02: `bash -n` 통과 — PASS
  - 근거: `bash -n reflect-kit/hooks/_lib-tag-canon.sh` / `log-reflection.sh` 둘 다 무오류
- [x] DG-03: 어휘 생성 3경로 실행 테스트 — PASS
  - 근거: 정상(맵+로그 존재)/맵 부재(fail-open)/빈 로그 디렉토리 3경로 모두 실행해 예상대로 다른 출력, 무오류(exit 0) 확인
- [x] DG-04: `sync-docs.py reflect-kit --check-only` 동기화 필요 0건 — PASS
  - 근거: `python3 scripts/sync-docs.py reflect-kit --check-only` → "모든 README가 동기화 상태입니다", exit 0

## Unverifiable Summary
- 총 미검증 건수: 0
- Verdict 영향: 해당 없음 (미검증 0건이므로 자동 REJECT 트리거 없음 — REJECT 사유는 SC-04 실측 FAIL 단독)

## Evidence Validity
- 검사 대상 증거: 29건 전부
- 무효 판정: 0건 (모든 PASS/FAIL 근거를 직접 명령 실행 또는 Read 로 수집. 서술/주석/구현자 주장 인용 없음)
- 셸 스니펫 실행 검증: SC-01/SC-02/SC-03/ER-01/DG-03 등 실행형 조건 전부 zsh(기본 셸 wrapper 경유) + `command grep`/bash 직접 실행 양쪽으로 확인. SC-02 는 bash·zsh·sh 3셸 × cwd 4종 = 12회 실행
- 환경 함정 발견: 이 저장소의 `grep` 셸 함수가 `ugrep -G` 로 wrapping되어 있어 `$` 포함 리터럴 패턴에서 거짓 0건을 낼 수 있음(RE-02 최초 시도에서 실제로 발생) — 이후 모든 grep 기반 검증을 `command grep` 으로 재실행해 교차 확인함

## Summary
- Total: 28/29 conditions passed
- Verdict: **REJECT**
- REJECT 사유: SC-04 — 계약이 스스로 요구한 음성 대조 등식("alias/verb-synonym 행을 제거하면
  두 값이 같아져야 한다")이 실측 재현에서 87 ≠ 86 으로 문자 그대로 성립하지 않는다. 결정론적
  pass의 핵심 효과(재발 과소집계 해소, 125>86)는 견고하게 입증되어 기능적 결함은 아니지만,
  계약 문언을 문자 그대로 적용하면 FAIL이다.
- 수정 우선순위: (1) SC-04 의 음성 대조 문언을 "맵 전체(모든 kind)를 제거하면 두 값이 같아진다"로
  교체 — write-once 위반 없이 다음 스프린트에서 새 조건으로 반영 권장. (2) 그 외 28개 조건은
  전부 실행 근거로 PASS 확인됨, 재작업 불필요.

## Improvement Suggestions
- [SC-04] 측정-정밀도-결함 — 음성 대조 대상을 "alias/verb-synonym 2종 제거"에서 "매핑 전체(모든 kind: verb/verb-synonym/synonym/alias) 제거 → 순수 kebab 정규화"로 교체. 전체 제거 시 86==86 정확 등식이 성립함을 이번 재평가에서 확인했다
- [AR-05 / ER-02 / AR-01] 상태-전제-미명시 반복 — "Given: 커밋 직전 working tree" 를 요구하는 조건이 스프린트 완료(전 커밋 병합) 후 재평가되는 경우를 계약이 고려하지 않는다. 다음 계약 작성 시 "재평가 시점에는 <구현 커밋범위>로 대체 측정한다"는 문구를 Given 절에 병기할 것을 권장 (이번 사이클에서 3개 조건이 동일 패턴)
- [RE-02] 검증환경-도구함정 — 이 레포 환경의 `grep` 셸 함수 wrapping(`ugrep -G`)이 mid-pattern `$` 리터럴을 오처리해 거짓 음성(false negative)을 낼 수 있음이 실측 확인됨. QA 평가 시 항상 `command grep` 사용을 권장하는 문구를 harness 스크립트/가이드에 명시하는 것을 검토 (계약 조건은 아니지만 평가 신뢰성에 직결)
