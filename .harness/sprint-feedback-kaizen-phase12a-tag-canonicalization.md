# Sprint Feedback
Feature: 카이젠 Phase 12 (v2) — reflect-kit 태그 정규화 결정론화(K1) + hook coverage audit 라우팅(K2) + 파편화 게이트로 calibration 무효화(K3)
Evaluated: 2026-08-14 13:15
Verdict: APPROVE
Iteration: 1 (v2 재평가 — SC-04 음성 대조 제거 대상 누락 결함을 오케스트레이터가 사용자 앵커로 계약 v2 재작성한 뒤, 이전 v1 REJECT 2건과 무관하게 전 29조건 독립 재검증)

## Contract Fingerprint
- path: .harness/sprint-contract-kaizen-phase12-tag-canonicalization.md
- sha256: aa7e7644e0d6f5b81a8ab1af1223582245ff95e541933170f8ad0c243460b087
- status: active (재평가 시작 시점) → done (본 APPROVE로 전환)
- slug: kaizen-phase12-tag-canonicalization
- contract_root: /Users/jackson/Hub/10_Dev/claude-plugins
- contract_root_unconfigured: false
- 선택 근거: ladder 2 세션소유 (owner_session == $CLAUDE_CODE_SESSION_ID == 1e76aa0b-dd42-4693-b79a-c2e2e6dfb88f)
- legacy_contract_used: false
- 봉인(verify_seal): SEAL_OK — conditions_digest(sha256:d85f4d7e5644ea3a) == 실제 조건 체크박스 해시. v1과 digest가 같은 이유는 계약 §"봉인 digest가 v1과 동일한 이유"에 문서화됨 (측정문은 조건 줄 아래 들여쓰기 텍스트라 봉인 대상 밖) — 판정에 사용하지 않음, 확인만 함
- 재확인(Step 5): 일치 (아래 참조)
- status_transition: active -> done (Step 5.5 수행)
- 글로벌 피드백 저장 경로: `/Users/jackson/.harness/feedback/evaluator/1a3bcba6-2026-08-14T131757-1e76aa0b-16145.yaml` (verify-feedback.sh PASS)

## 재평가 목적 관련 확인
이 재평가는 이전 판정을 승계하지 않고 29개 조건 전부를 직접 실행 검증했다. 특히 SC-04(2회 REJECT 원인이었던 조건)는 주 측정과 음성 대조(빈 맵) 양쪽을 bash·zsh 양쪽에서 동일 파일 스냅샷으로 원자적으로 재실행하여 확인했다. "이미 APPROVE였다"는 사실을 근거로 쓰지 않았다.

## Amendments
- amendments: 3 (sprint-amendments-kaizen-phase12-tag-canonicalization.md)
- narrowing: 0
- relaxing / unknown: 0
- 유형: 전부 `clarification`(측정문 결함 신고, direction: narrowing 아님·widening 아님, consent: 사용자 앵커 없음)
  - AM-01: SC-04 v1 음성 대조 측정문 결함 신고 — v2 계약이 이 결함을 근본 해소(음성 대조를 "맵 전체 제거"로 교체)했으므로 이 재평가는 AM-01이 아니라 **v2 계약 원문**을 직접 실행 검증했다 (측정: RAW=90, CANON(empty-map)=90, EQUAL — 아래 SC-04 참조)
  - AM-02: 환경 사고 기록 (git stash 복원) — 계약 조건과 무관, 표면화만
  - AM-03: SC-02 측정문이 cwd 축을 교차하지 않아 거짓 PASS를 허용했다는 신고. 구현은 이미 cwd 비의존으로 수정됨. 본 재평가는 v2 계약 원문(3셸만 요구)뿐 아니라 AM-03이 권고한 강화 회귀(cwd 3곳 × 셸 3개 = 9회, 절대경로 source)도 추가 실행 — 9/9 동일 1행, 비퇴화 확인
- PASS 근거로 사용한 amendment: 없음 (전부 원 조건 v2 원문을 직접 실행 검증했고, amendment는 참고·강화용으로만 사용)

## User Correction Audit
- correction_log_status: available (~/.claude/logs/claude-plugins/2026-08.md)
- 스프린트 기간(2026-08-13 15:20 생성 ~ 2026-08-14 재평가): prompt 항목 28건 확인, phase12/tag-canon/SC-04/lemma 관련 키워드 매칭 0건
- unreflected_corrections: 0 (스캔 범위: phase12 관련 키워드 한정 — 전체 28건 개별 정독은 미수행, 키워드 스캔 기반)
- verdict 영향: 없음 (표면화 전용 · 미검증 카운터 비합산)

## Results

### Skill (7/7)
- [x] SK-01: 정규화 SSOT 참조 3곳 — PASS
  - 근거: `grep -l 'tag-canonicalization.md' reflect-kit/skills/{reflect-digest,reflect-promote,reflect-kaizen}/SKILL.md` → 3행 전부 매칭 (L3, enumerated 3/3 개별 확인)
- [x] SK-02: reflect-digest 클러스터링이 tag_canon_groups를 1차 근거로 지정 — PASS
  - 근거: `reflect-kit/skills/reflect-digest/SKILL.md:30` "클러스터링은 눈대중이 아니라 **결정론적 pass**로 한다 — ... 실행은 `hooks/_lib-tag-canon.sh`의 `tag_canon_groups`다" (같은 문장에 두 문자열 공존, L3)
- [x] SK-03: reflect-promote §B-0에 9개 점검 항목 — PASS
  - 근거: `reflect-kit/skills/reflect-promote/SKILL.md:148` `### B-0.` 헤더 1개 + 161-171행 표에 9개 토큰(hook installed/event type/matcher/path normalization/exit code/timeout/executable/dependency/fired/blocked) 전부 개별 확인 (L3, enumerated 9/9)
- [x] SK-04: reflect-kaizen이 calibration_confidence:low에서 demote-candidate 산출 금지 — PASS
  - 근거: `blocked-low-confidence` 4회 등장(35, 65, 94, 138행), 138행이 `verdict` 열거 정의 줄(`demote-candidate / keep / ... / blocked-low-confidence`) (L3)
- [x] SK-05: reflect-digest에 family 섹션 — PASS
  - 근거: `reflect-kit/skills/reflect-digest/SKILL.md:309` `## 원인 계열 (family) — 병합하지 않음 (합산 금지)`, 1회 (L3, 내용도 stale-context-reference family 예시 포함 확인)
- [x] SK-06: 구 임계 1.5가 스킬3종+references에서 0건 — PASS
  - 근거: `grep -rn '1\.5' reflect-kit/skills reflect-kit/references` 0행. enumerated 개별 확인(reflect-digest/reflect-kaizen/reflect-promote/codex-kaizen SKILL.md 4개 + tag-canonicalization.md + tag-lemma-map.tsv 전부 0건, L3)
- [x] SK-07: reflect-promote가 PostToolUse를 예방 surface로 쓰지 말라 명시 — PASS
  - 근거: 112행(hook 표) "`PostToolUse` 는 예방 surface 가 아니다" + 232행(안티패턴) "예방 게이트를 `PostToolUse` 에 걸지 마라" 각 1회, 2표면 확인 (L3)

### Script (6/6)
- [x] SC-01: log-reflection.sh가 canonical → aliases 형태로 어휘 주입 — PASS [goal]
  - 근거: fixture 2파일(edited-before-read×1, edit-before-read×2, ignored-required-api-doc-check×1, skipped-required-api-doc-check×1, used-stale-widget-ref×1)로 어휘 생성 구간(log-reflection.sh:123-163)을 sed로 원문 추출·실행 → 출력에 `- edit-before-read  (freq 3)  ← 같은 뜻으로 쓰인 다른 표기: edited-before-read(1)` 행 정확히 존재. 음성 대조: tag-lemma-map.tsv의 verb 행 제거 후 재실행 → freq 2로 감소, alias 주석 사라짐 (L3, 직접 실행)
- [x] SC-02: tag_canon_fragmentation이 bash·zsh·sh 동일 1행 — PASS [exact, enumerated]
  - 근거: 3셸 동일 fixture 실행 → `5 3 6 1 1.67 0.333 2.00` 동일, `sort -u` 1행 (L3). 추가로 AM-03 권고 강화 회귀(cwd 3곳×셸3개=9회, 절대경로 source)도 실행 — 9/9 동일 1행, 비퇴화(5→3 실제 접힘) 확인
- [x] SC-03: lemma map 불가독 시 rc=3 + 경고 1행 + fail-open 계속 동작 — PASS [goal]
  - 근거: `REFLECT_TAG_LEMMA_MAP=/nonexistent/no-such-map.tsv`로 실행 → RC=3, `.errors.log`에 `warn:lemma-map-unreadable` 1행, 어휘 블록 비어있지 않음(`- edit-before-read (freq 2)`). 음성 대조: 정상 경로 재실행 → 그 경고 0행 (L3)
- [x] SC-04: 결정론적 pass가 재발을 실제로 회수 — PASS [goal] ★2회 REJECT 원인 조건, 최우선 재검증
  - 근거(주 측정): 실로그 전량(`find ~/.claude/logs -name 'reflections-*.md'` 14파일) 동일 스냅샷으로 RAW=90, CANON(전체맵, bash)=129, CANON(전체맵, zsh)=129. 129 > 90 확인, bash/zsh 일치 (L3)
  - 근거(음성 대조, v2 신규): 맵을 주석행만 남긴 빈 파일로 교체 후 동일 스냅샷 재실행 → CANON(빈맵, bash)=90, CANON(빈맵, zsh)=90. RAW(90) == CANON(빈맵, 90) 완전 일치 (L3, 원자적 동일 파일셋 사용으로 로그 성장에 의한 오차 배제)
  - 참고: 로그가 실행 중에도 계속 자라 절대값(89→90)이 이동했으나(계약이 명시적으로 경고한 현상), 매 비교는 동일 스냅샷 내에서 수행해 관계값(RAW==빈맵, 전체맵>RAW)이 훼손되지 않음을 확인
- [x] SC-05: 신규·변경 셸스크립트 2개 shellcheck 0 findings — PASS [exact, enumerated]
  - 근거: `shellcheck reflect-kit/hooks/_lib-tag-canon.sh reflect-kit/hooks/log-reflection.sh` 결합 실행 exit 0 + 개별 실행 각각 exit 0 (L3, enumerated 2/2)
- [x] SC-06: tag_canon_fragmentation이 7열, 6열 singleton_share — PASS [exact]
  - 근거: 실로그 전량 실행 → `2747 2685 4842 2380 1.02 0.886 1.80` (7필드, 6열=0.886, 0~1 범위) (L3)

### Error (3/3)
- [x] ER-01: 빈 로그 디렉토리에서 "(없음 — 첫 수집)" + 비정상 종료 없음 — PASS [exact]
  - 근거: 빈 디렉토리로 어휘 생성 구간 실행 → `(없음 — 첫 수집)` 출력 포함, exit 0 (L3)
- [x] ER-02: 기존 env dedup 게이트·codex→claude fallback 경로 변경 없음 — PASS [exact, enumerated]
  - 근거(Given: 커밋 직전 워킹트리 — 현재는 전부 커밋된 상태라 Phase12 커밋범위(`0fe357a^`..`f62691f`) diff로 대체 측정, 상태 전제 명시): `git diff -U0 0fe357a^ f62691f -- reflect-kit/hooks/log-reflection.sh`에서 `try_claude_fallback`/`env_state`/`REFLECT_ENV_REPEAT_DAYS` 3개 식별자 각각 grep 0건 (enumerated 3/3). 3개 식별자 모두 파일에 여전히 실재함을 확인해 공허한 0이 아님을 확인(237/285/287행, 317-384행) (L3)
- [x] ER-03: new_tag_reason이 선택 필드로 도입 — PASS [exact]
  - 근거: 훅 프롬프트(`log-reflection.sh:181`) "canonical 을 재사용했으면 이 줄 자체를 생략한다" + reflect-digest 스키마 주석(`SKILL.md:84`) "(선택 필드)" (L3)

### Architecture (5/5)
- [x] AR-01: 변경이 Scope 6항목과 정확히 일치 — PASS [exact, enumerated]
  - 근거(상태 전제 명시: "커밋 직전 워킹트리"를 현재 재현 불가하여 Phase12 커밋범위 diff로 대체): `git diff --name-only 0fe357a^ f62691f -- reflect-kit/` → `_lib-tag-canon.sh`, `log-reflection.sh`, `references/tag-canonicalization.md`, `references/tag-lemma-map.tsv`, `skills/reflect-digest/SKILL.md`, `skills/reflect-kaizen/SKILL.md`, `skills/reflect-promote/SKILL.md` 7개 파일이 계약이 지정한 6항목(references/를 디렉토리로 셈)과 정확히 일치, 그 외 경로 0건 (L3)
- [x] AR-02: 매핑 데이터가 tag-lemma-map.tsv 1곳에만(SSOT) — PASS [exact]
  - 근거: `grep -rln 'verb-synonym' reflect-kit/` 4파일에서 문자열 등장하나, 데이터 행(`^verb-synonym\t`) 패턴은 tag-lemma-map.tsv에만 2건, 나머지 3파일(references/tag-canonicalization.md, hooks/_lib-tag-canon.sh, skills/reflect-kaizen/SKILL.md)은 0건(서술 인용) (L3, grep 오탐 필터링 적용 — 텍스트 언급과 데이터행을 구분)
- [x] AR-03: 사실 정정 — edited-before-read(규범 예시) 0건, edit-before-read 존재 — PASS [exact]
  - 근거: `grep -c 'edited-before-read' reflect-kit/hooks/log-reflection.sh` 0, `grep -c 'edit-before-read' ...` 1 (L3)
- [x] AR-04: 사실 정정 — "really bad groups" 인용 0건 — PASS [exact]
  - 근거: `grep -rn 'really bad groups' reflect-kit/` 0건 (L3)
- [x] AR-05: Scope 밖 파일 무변경 — PASS [exact, enumerated]
  - 근거: 현재 워킹트리 porcelain 0행 + Phase12 커밋범위 diff 0행(docs/README.md/hooks.json/scripts/.claude-plugin) (L3)

### Anti-patterns (2/2)
- [x] AP-03: bare code fence 0건 — PASS
  - 근거: `python3 scripts/validate-plugin.py reflect-kit --check=code-fence` → `V6 code-fence 0 bare — OK`, exit 0 (L3)
- [x] AP-04: SKILL.md frontmatter name 필드 유지 — PASS
  - 근거: `python3 scripts/validate-plugin.py reflect-kit --check=frontmatter` → `V1 frontmatter 4 skills — OK`, exit 0 (L3)

### Reusability (2/2)
- [x] RE-01: 정규화 로직이 _lib-tag-canon.sh 한 곳에만 — PASS
  - 근거: `grep -rn 'function norm\|tolower(s)' reflect-kit/` 매칭 전부 `_lib-tag-canon.sh` (143, 144행)뿐 (L3)
- [x] RE-02: 훅이 `source "$SCRIPT_DIR/_lib-*.sh"` 규약 3회 — PASS
  - 근거: `/usr/bin/grep -c 'source "$SCRIPT_DIR/_lib-' reflect-kit/hooks/log-reflection.sh` → 3 (16/18/20행). **주의**: 이 Bash 세션 고유의 `grep`→`ugrep -G` 셸 함수 셈(Claude Code 셸 스냅샷)이 패턴 중간의 `$`를 오처리해 0을 반환하는 아티팩트를 발견함. `/usr/bin/grep`, `command grep`, `bash -c`, `zsh -c`, `zsh -i -c` 5가지 독립 경로 전부 3을 반환해 실제 파일 내용이 규약을 만족함을 확인 (L3, 도구 아티팩트와 실제 결함을 구분)

### Diagnostics (4/4)
- [x] DG-01: validate-plugin V1~V8 전부 OK, exit 0 — PASS
  - 근거: 전체 실행 결과 V1~V8 전부 OK/SKIP(무해), `Exit: 0` (L3)
- [x] DG-02: bash -n 신규·변경 셸스크립트 2개 통과 — PASS
  - 근거: `bash -n reflect-kit/hooks/_lib-tag-canon.sh` / `log-reflection.sh` 둘 다 무오류 (L3)
- [x] DG-03: 어휘 생성 3경로(정상·map부재·빈디렉토리) 실행 테스트 전부 통과 — PASS
  - 근거: SC-01(정상, PASS) + SC-03(map 부재, PASS) + ER-01(빈 디렉토리, PASS) 3경로 모두 위에서 직접 실행 확인 (L3)
- [x] DG-04: sync-docs --check-only 동기화 필요 0건 — PASS
  - 근거: `python3 scripts/sync-docs.py reflect-kit --check-only` → "모든 README가 동기화 상태입니다.", exit 0 (L3)

## Unverifiable Summary
- 총 미검증 건수: 0
- 건 목록: 없음
- Verdict 영향: 해당 없음 (미검증 0건 — 자동 REJECT 트리거 없음)

## Evidence Validity
- 검사 대상 증거: 29건 (조건별 1건씩)
- 무효 판정: 0건
- 셸 스니펫 실행 검증: 실행 29건 · zsh/bash 양쪽 확인(SC-01/SC-02/SC-04/RE-02 등 셸 민감 조건) 다수 · 미실행 0건
- 특이사항: RE-02에서 평가 도구(Claude Code Bash 세션) 자체의 `grep` 셸 함수 셈(ugrep -G 래퍼)이 리터럴 `$` 중간 패턴을 오처리하는 것을 발견 — 5가지 독립 그레프 경로로 교차검증해 실제 파일은 규약을 준수함을 확인. 이 아티팩트는 이 대화 세션에 한정되며 실제 사용자 셸(zsh -i, 일반 bash)에서는 재현되지 않음을 직접 확인함

## Summary
- Total: 29/29 conditions passed
- Verdict: APPROVE
- 이 판정은 이전 APPROVE를 승계하지 않고 29개 조건 전부를 이 세션에서 직접 재실행하여 도달했다. 2회 연속 REJECT의 원인이었던 SC-04는 v2 계약의 새 음성 대조(맵 전체 제거)를 primary/negative 양쪽·bash/zsh 양쪽·동일 파일 스냅샷 기준으로 재검증해 확실히 PASS를 확인했다.

## Improvement Suggestions
- [RE-02] 도구-아티팩트 — 향후 계약 측정문에서 grep 패턴에 리터럴 `$VAR` 문자열을 쓸 때는 `-F`(fixed-string) 플래그를 명시하거나 `\$`로 이스케이프할 것을 권장. Claude Code Bash 세션의 `grep` 셸 함수 셈(ugrep -G)이 mid-pattern `$`를 앵커로 오처리해 실제로 존재하는 콘텐츠에서 거짓 0을 반환하는 사례를 이번에 발견함 (이 세션 한정 아티팩트, 프로젝트 결함 아님)
- [ER-02, AR-01, AR-05] 상태-의존 측정 — "Given: 커밋 직전 워킹트리" 전제는 재평가(사후 QA) 시점에는 이미 전부 커밋된 상태라 재현 불가능하다. 다음 계약 작성 시 "구현 완료 직후 QA" 와 "사후 재평가" 두 시나리오 모두에 대응 가능하도록 "Given: 해당 Phase 커밋 범위(시작 커밋^..종료 커밋) diff" 형태의 대체 표현을 병기할 것을 권장
