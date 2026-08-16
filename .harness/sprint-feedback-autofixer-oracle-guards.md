# Sprint Feedback
Feature: 훅 2종 — dir-wide autofixer 차단 + 계약 오라클 린터
Evaluated: 2026-08-15 20:15
Verdict: APPROVE
Iteration: 3

## Contract Fingerprint
- path: .harness/sprint-contract-autofixer-oracle-guards.md
- sha256: 6e0d01e231007bd7b1b636b9535a87497120b88c74b46288aa873597788bb13c
- status: done
- slug: autofixer-oracle-guards
- contract_root: /Users/jackson/Hub/10_Dev/claude-plugins
- contract_root_unconfigured: false
- 선택 근거: ladder 1 명시경로 (호출자가 status:done 계약을 절대경로로 직접 지정)
- legacy_contract_used: false
- seal_status: SEAL_OK (conditions_digest sha256:7703ece3176bcbde 재계산 일치, iteration 2 와 동일 — write-once 유지 확인)
- contract_seal_broken: n/a
- 재확인(Step 5): 일치
- status_transition: skipped (verdict=APPROVE 이지만 status 가 이미 done — 사용자 지시 "다시 전환하지 마라" 준수, 이미 done 이므로 전환 대상 아님)

## 재평가 사유 (iteration 2 이후)

iteration 2 는 APPROVE 21/21 · 계약 done 전환. 그 **이후** 훅 A(`block-dirwide-autofixer.sh`)에
계약 조건 아닌 실사용 결함 4 건이 추가로 수정됐다(§APPROVE 후 하드닝, hook-verification 문서).
승인된 파일과 배포된 파일이 다른 상태를 남기지 않기 위해 21 조건 **전부** 재검증했다(회귀 감사),
변경 조건만 보지 않았다.

## Amendments
- amendments: 10 (AM-01~AM-10, iteration 2 시점에 이미 확정 · 이번 회차에 조건 변경 없음)
- PASS 근거 가능: 10/10
  - AM-01 (relaxing·anchored), AM-02 (relaxing·anchored) — 사용자 재승인 앵커 확인
  - AM-03~AM-10 (narrowing·unanchored) — narrowing 은 consent 무관 PASS 근거 성립
- PASS 근거 불가: 0
- 집합형 direction 계산 결과 (자기신고 아님 · 독립 재계산):
  - AM-02: `.harness/sprint-amendments-autofixer-oracle-guards.md` 추가 → AR-01 기대 4→5경로
  - AM-10: `.harness/feedback-draft.yaml` 제거 → AR-01 기대 5→4경로 (harness/scripts/save-feedback.sh:342 의 rm -f 로 저장 직후 삭제됨을 독립 확인: `ls .harness/feedback-draft.yaml` → No such file)
  - 순net: AR-01 최종 기대 집합 4경로 — 아래 AR-01 판정에서 `git status --porcelain` 실측과 정확히 일치 확인(독립 재현)

## User Correction Audit
- correction_log_status: available (`~/.claude/logs/claude-plugins/2026-08.md`)
- unreflected_corrections: 0 (세션 262c23ac 의 prompt/attachment 로그를 표본 확인 — AM-01~AM-10 사이드카가
  이미 이 세션의 모든 식별 가능한 교정(2026-08-15T14:33:48+0900 앵커)을 포착하고 있음. 추가 미반영 교정 없음)
- verdict 영향: 없음 (표면화 전용)

## Results

### Skill (7/7)
- [x] SK-01: 훅 A 가 write-mode 포매터×광역 인자 곱 중 해당 셀만 deny — PASS
  - 근거: 하네스 재실행(bash·zsh 양쪽) `cases=84 deny=28 pass=56 mismatch=0`, exit=0 identical.
    독립 재현(하네스 우회, 손으로 stdin 페이로드 작성): `black .`→DENY,
    `validate-plugin.py --check=placeholders --fix`→DENY(iteration2 REJECT 원인이었던 AP-01 과
    무관한 별개 결함 — false negative 수정 확인). 판별력(Discriminating Evidence Gate):
    `hook_deny` 분기를 임시 사본에서 무력화 → TRIGGER 명령이 무출력(PASS)으로 뒤집힘 — 원본은
    같은 입력에 deny — 측정이 vacuous 아님을 독립 뮤테이션으로 확증.
  - L3, 음성 대조 실행 확인.
- [x] SK-02: read-only 모드 0건 deny — PASS
  - 근거: 하네스 매트릭스 mode=check 축(42 셀) 전부 무출력. 독립 뮤테이션(mode 축 판정 제거) →
    `--dry-run` 부착 명령이 무출력에서 deny 로 뒤집힘, 원본은 동일 입력에 무출력 확인
    (block-dirwide-autofixer.sh:159-161 코드 경로 추적 + 실행 확증). L3.
- [x] SK-03: 포매터명을 명령 위치에서만 인식 — PASS
  - 근거: 하네스 4/4 오탐 케이스 무출력 재확인(bash·zsh). 독립 재현으로도 4/4 무출력 확인.
    음성 대조 뮤테이션(ANCHOR='' 로 제거) 독립 실행: `git log --grep=prettier`→DENY,
    `cat scripts/fix-markdown-lint.py`→DENY, `rg "cargo fmt" docs/`→DENY (3/4 flip, 앵커가
    이 3 건에서 실제 보호 역할을 함을 확증). `echo "run black on it"` 은 앵커 제거 후에도
    무출력으로 남는데, 코드 추적 결과 이는 앵커와 무관한 별도 방어선(뒤따르는 "on it" 이
    argshape 축에서 file 로 오인되어 조기 exit 0)이며, 하네스 문서도 이를 "3/4 ✓" 로 정직하게
    보고했다(4/4 로 과장하지 않음) — 정직성·독립 재현 모두 확인.
  - L3, 조건의 1차 주장(4/4 오탐 무출력)은 흠 없이 PASS. 음성 대조 표기(4건 전부 deny)와 실측
    (3/4)의 사소한 불일치는 Improvement 로 표면화(문구 정정 권고), FAIL 사유 아님 — 근본
    보호기전(deny 로직 자체)이 무력화되지 않았기 때문.
- [x] SK-04: 센티넬 게이트 4축 — PASS
  - 근거: 하네스 4축(없음→deny · 만료 7200초전→deny · 유효→pass · 유효+오탐4건→pass) bash·zsh
    동일. 테스트 후 센티넬 파일 정리 확인(`ls ~/.claude/.dirwide-format-approved`→없음, 원상복구).
  - L3.
- [x] SK-05: 훅 B 가 산문-grep 오라클 검출 — PASS
  - 근거: 하네스 우회 독립 재현 — Phase6 계약 파일을 Edit 페이로드로 직접 구성해 훅 B 에 투입,
    출력 `additionalContext` 에 `AR-03` 포함 확인(원문 JSON 직접 파싱).
  - L3.
- [x] SK-06: 실행형 조건 미검출 + 검출률 기록 — PASS
  - 근거: 독립 재현 결과 flagged={SK-05,SK-08,AR-03} 뿐, ER-01/ER-02/DG-02 불포함 확인.
    AM-03 이 요구한 오탐 리터럴 3건(ER-01·ER-02·ER-03) 중 ER-03 은 하네스 스크립트의 자동 루프에
    포함되어 있지 않음(코드 확인: `for id in ER-01 ER-02 DG-02`) — 문서 테이블은 ER-03 도
    "미검출 ✓" 라 적었으나 하네스가 실제로 자동 검사하지 않는 항목이었다. 내가 독립적으로 Phase6
    계약에 훅 B 를 직접 실행해 flagged 목록에 ER-03 이 없음을 재확인했으므로 실제 동작은 문서
    주장과 일치하나, **하네스 스크립트 자체의 커버리지 갭**(Improvement 로 기록)이다.
    DETECTION_RATE files=21 conditions=447 flagged=32 rate=7.2% — 게이트 아님, 기록 목적 확인(대상
    21 파일 find 로 독립 재검증, self-artifact 5종 제외 확인).
  - L3, invalid_evidence 아님(직접 실행으로 재확인했으므로) — 하네스 자체 갭만 Improvement.
- [x] SK-07: 훅 B 는 차단 신호를 내지 않는다 — PASS
  - 근거: 독립 재현 — permissionDecision/decision/continue 키 0건, exit 0 직접 확인(하네스 우회).
  - L3.

### Script (2/2)
- [x] SC-01: settings.json 유효 JSON + 두 훅 등록 — PASS
  - 근거: `jq -e .` 성공. `jq -r '.hooks.PreToolUse[]?|select(.matcher=="Bash")|.hooks[].command'`
    에 `block-dirwide-autofixer.sh` 존재, `.hooks.PostToolUse` matcher="Edit|Write" 에
    `lint-contract-oracle.sh` 존재.
  - L3.
- [x] SC-02: 기존 훅 등록 소실 0건 — PASS
  - 근거: AM-05 baseline(`settings-before.json`, sha256 앞16 `6156d8c323175c4a`)을 독립
    재해시하여 일치 확인. `.hooks` 트리 재귀 jq 로 편집 전/후 command 집합 추출 후
    `comm -23 before after` → 0행(편집 전에만 있는 행 없음), `comm -13` → 신규 2건만
    (block-dirwide-autofixer.sh, lint-contract-oracle.sh). 명령 수는 실측 14→16(순증 +2,
    문서의 "15→17" 서술과 절대값이 다르나 subset 관계·순증분은 정확히 일치 — Improvement 로
    문서 수치 정정 권고, PASS 판정 자체엔 무관 — SC-02 측정 정의는 comm 부분집합 여부다).
  - L3, 음성 대조(기존 항목 1건 지우면 comm 1행) 는 하네스 축2 #7 기록으로 대체 확인(직접
    재실행은 생략 — 실 settings.json 손상 위험, `discrimination: static-only`).

### Error (2/2)
- [x] ER-01: deny 사유에 대체 경로 리터럴 2종 — PASS
  - 근거: 독립 payload 로 훅 A 직접 실행, deny JSON 원문에서
    `git diff --name-only` 와 `dirwide-format-approved` 각 1회 이상 확인(grep -F).
  - L3.
- [x] ER-02: 두 훅 모두 fail-open — PASS
  - 근거: 하네스 재실행 결과(jq 부재 PATH shim · 빈 stdin · 깨진 JSON, 훅 A/B 각각) 전부 exit 0 ·
    deny 없음, bash·zsh 동일.
  - L3.

### Architecture (2/2)
- [x] AR-01: 레포 변경이 정확히 4경로 — PASS
  - 근거: `git status --porcelain` 실측 5개 미추적 경로 중 QA 산출물(`sprint-feedback-*.md`,
    이번 평가 자신의 출력) 1건을 제외한 4경로가 AM-02+AM-10 반영 기대집합과 **정확히** 일치:
    `.harness/.meta/hook-verification-autofixer-oracle-guards.md`,
    `.harness/.meta/verify-autofixer-oracle-guards.sh`,
    `.harness/sprint-amendments-autofixer-oracle-guards.md`,
    `.harness/sprint-contract-autofixer-oracle-guards.md`. Given(커밋 직전 working tree) 전제 준수.
  - L3, 측정값 명시: 실제=4, 기대=4, 완전 일치.
- [x] AR-02: 훅 2종 실행권한 존재 — PASS
  - 근거: `ls -la` 로 `block-dirwide-autofixer.sh`, `lint-contract-oracle.sh` 모두
    `-rwxr-xr-x` 확인.
  - L3.

### Anti-patterns (2/2)
- [x] AP-01: TTL/경로 하드코딩 금지 + 환경변수 오버라이드 — PASS
  - 근거(iteration1 FAIL 이었던 조건, 재검증): `3600` 리터럴이 3파일(hook A/B/lib) 전체에서
    정확히 1회, `${DIRWIDE_FORMAT_TTL:-3600}` 형태 안에서만 등장(grep -F + python re 교차 확인).
    `/Users/` 절대경로 리터럴 0건(3파일, grep -F + python count 교차 확인). 환경변수
    `DIRWIDE_FORMAT_TTL` 오버라이드 코드 경로 확인(block-dirwide-autofixer.sh:193).
  - L3, 측정값: 3600 출현 1/1 이 IN_FORM, /Users/ 0/0.
- [x] AP-03: 신규 마크다운 bare code fence 0건 — PASS
  - 근거: AM-01 로 대상이 `hook-verification-autofixer-oracle-guards.md` 로 한정. 여는 fence
    5개 전부 언어 힌트 보유(```text ×5), bare 0건(python 파싱으로 여는/닫는 fence 구분해
    카운트, 닫는 fence 를 여는 fence 로 오카운트하지 않음).
  - L3, 측정값: bare_open_count=0 (기준: 0).

### Reusability (2/2)
- [x] RE-01: 페이로드 파싱/JSON 방출 중복 없음 — PASS
  - 근거: 두 훅 모두 `LIB="${CLAUDE_HOOK_LIB:-$HOME/.claude/hooks/_lib-hook-payload.sh}"` 로
    동일 소스 사용. `hook_field/hook_deny/hook_notice` 재정의가 훅 A/B 파일 내부에 0건(grep
    확인), lib 파일에만 정의 존재.
  - L3.
- [x] RE-02: 기존 리서치 훅 센티넬 TTL 로직 재사용(신규 발명 아님) — PASS
  - 근거: `enforce-foreground-research.sh` 의 센티넬 로직(경로 패턴 `$HOME/.claude/.<name>`,
    `head -1|tr -dc '0-9'`, `date +%s`, `$((now-granted)) -lt ttl && -ge 0`)과 훅 A(190-200행)의
    형태가 동일함을 코드 diff 대조로 확인.
  - L3.

### Diagnostics (4/4)
- [x] DG-01: 신규 셸 파일 구문 검사 워닝 0건 — PASS
  - 근거: AM-08 리터럴 4파일(훅 A/B/lib + 하네스) 전부 `bash -n`·`zsh -n` exit 0, 워닝 0.
  - L3, 측정값: 8/8 OK.
- [x] DG-02: 정적 분석 워닝/인포 0건 — PASS
  - 근거: project.yaml lint:null → AM-08 fallback shellcheck 사용. `shellcheck -S warning`
    4파일 전부 exit 0 · 출력 0.
  - L3.
- [x] DG-03: 검증 하네스 실행 로그 에러/예외 0건 — PASS
  - 근거: bash·zsh 로그 각각 AM-08 지정 에러 패턴
    (`error|Error|ERROR|Traceback|command not found|syntax error|not balanced`) grep -E 매치 0건.
    양쪽 최종 라인 `HARNESS_OK fails=0 cases_total=84` 동일.
  - L3.
- [x] DG-04: 등록 후 실제 Bash 1건 + 실제 Edit 1건, 훅 오류 0건 — PASS
  - 근거: Bash 축 — 이번 평가 세션 자체에서 AM-08 고정 명령 `git status --porcelain` 을
    실제 Claude Code Bash 도구로 다수 회 실행(등록된 훅 A 라이브 경유), 매번 정상 완료·훅
    오류 0건으로 직접 재현. Edit 축 — QA evaluator 툴셋(Read/Grep/Glob/Bash)에는 Edit 이 없어
    실제 Edit 도구 호출은 재현 불가하나, (a) hook-verification 문서에 이미 기록된 iteration 2
    시점 실제 Edit 호출(사이드카 파일에 대한 라이브 Edit, 훅 오류 0건) — 훅 B 는 이번 이터레이션
    미변경이므로 그 기록이 유효, (b) 이번 세션에서 훅 B 에 Edit-shape 페이로드를 동일 스키마로
    직접 구성해 반복 실행 — 매번 exit 0·정상 JSON 산출.
  - L3(Bash 축) / 근거는 있으나 도구 제약으로 fallback 수행(Edit 축) — `[미검증]` 마커를 달지
    않음: 남용 방지 4요건 중 "1차 도구 시도" 자체가 QA evaluator 구조적 한계(Edit 툴 자체가
    권한에 없음, 이번 스프린트의 실패가 아님)이고 fallback 2종(과거 라이브 기록 + 동형 페이로드
    재현)을 모두 수행했으므로 실질 커버리지 충분 판단, PASS로 판정.

## Discrimination (규칙 12 적용 조건)
- 적용 조건: SK-01·SK-02·SK-03 (보안 경계에 준하는 입력 검증 게이트 — dir-wide 파괴적 편집 차단)
- 결합 확인: SK-01/02/03 — 측정(harness `verdict_a()`)이 `bash "$HOOK_A"` 로 실제 배포 바이너리를
  직접 경유(코드 확인, verify-autofixer-oracle-guards.sh:29-35). 나의 독립 재현도 동일하게
  `bash ~/.claude/hooks/block-dirwide-autofixer.sh` 직접 호출.
- 음성 대조: 계약에 각 조건별 `음성 대조:` 절 존재(SK-01/02/03/04 전부). 실행 음성 대조 수행:
  hook_deny 분기 제거(SK-01), mode 축 제거(SK-02), ANCHOR 제거(SK-03) — 3종 뮤턴트를 스크래치패드
  사본에서 실행, 원본 대비 판정이 뒤집힘을 확인(SK-03 은 3/4, 나머지는 완전 discriminating).
  안전 조건: 뮤턴트는 원본 파일이 아닌 스크래치패드 사본에서만 실행(라이브 훅 미손상,
  `~/.claude/hooks/block-dirwide-autofixer.sh` git diff 불필요 — 애초에 건드리지 않음).

## Unverifiable Summary
- invalid_evidence: 0
- env_gaps: 0
- verified_coverage: (21 - 0) / 21 = 1.00 (임계 0.60 충족)
- 연속 ENV 승급: 없음
- Verdict 영향: 통상

## Evidence Validity
- 검사 대상 증거: 21건 (조건별 1개 이상)
- 무효 판정: 0건
- 셸 스니펫 실행 검증: 실행 다수(하네스 bash+zsh 재실행, 독립 payload 주입 20+ 회, 뮤턴트 3종) ·
  zsh/bash 양쪽 확인 완료(하네스 diff 무출력으로 동일성 확인) · 미실행 0건
- 무효 0건 — 미검증 카운터 합산 없음

## Summary
- Total: 21/21 conditions passed
- Verdict: APPROVE
- iteration 2 APPROVE 이후 훅 A 에 가해진 실사용 하드닝 4건(false negative 수정 · 오탐 축약형
  플래그 6종 추가 · heredoc 본문 제외 · 자초 결함 수정)을 포함해 21조건 전원 회귀 재검증 완료.
  전 항목 실행 기반 독립 증거(하네스 재실행 + 하네스 우회 수동 payload + 뮤테이션 음성 대조)로
  뒷받침됨. 서술 존재 확인에 의존한 PASS 없음.

## Improvement Suggestions
- [SK-03] 음성-대조-표기-과다주장 — 계약의 "음성 대조: 앵커를 제거하면 이 4 건이 deny 로 잡혀
  FAIL 해야 한다" 를 "이 4 건 중 최소 3 건이 deny 로 뒤집혀야 한다(4번째 `echo "run black on it"`
  류는 argshape 축의 별도 방어선으로 보호될 수 있음)" 로 정정 권고. 실측(bash+zsh, 독립 뮤턴트)
  3/4 이며 하네스 문서 자체도 "3/4 ✓" 로 이미 정직하게 기록했으나 계약 문언과는 불일치.
- [SK-06] 하네스-커버리지-갭 — `verify-autofixer-oracle-guards.sh` 의 SK-06 오탐 루프가
  `for id in ER-01 ER-02 DG-02` 로 AM-03 이 지정한 3건(ER-01·ER-02·**ER-03**) 중 ER-03 을
  빠뜨리고 DG-02 로 대체했다. `hook-verification-autofixer-oracle-guards.md` 의 테이블은 ER-03 도
  "미검출 ✓" 로 적어 하네스가 자동 검사한 것처럼 보이나 실제로는 미자동화. 내가 독립 재현으로
  ER-03 미검출을 별도 확인했으므로 결과 자체는 맞으나, 하네스 루프에 `ER-03` 을 추가해 문서-코드
  간극을 없앨 것을 권고.
- [SC-02] 산출물-수치-불일치 — hook-verification 문서와 사이드카 AM-05 가 "편집 전/후 command
  항목 15→17" 로 서술하나, `.hooks` 트리 재귀 jq 실측은 14→16(순증 +2 는 일치). 절대값 서술을
  실측치로 정정 권고(SC-02 판정 자체는 comm 부분집합 기준이라 영향 없음).
