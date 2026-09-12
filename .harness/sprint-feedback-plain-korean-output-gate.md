# Sprint Feedback
Feature: 출력 직전 용어 검사 Stop 훅
Evaluated: 2026-09-11 12:05
Verdict: APPROVE
Iteration: 2

## Contract Fingerprint
- path: /Users/jackson/Hub/10_Dev/claude-plugins/.harness/sprint-contract-plain-korean-output-gate.md
- sha256: 310d0a5c62346c808f770e398ea36fb5058825573c36aaabdf21e076fa71c90e (Iteration 1과 동일 — 계약 원문 무변경)
- status: active
- slug: plain-korean-output-gate
- contract_root: /Users/jackson/Hub/10_Dev/claude-plugins
- contract_root_unconfigured: false
- 선택 근거: ladder 1 (명시 경로 — 지시받은 절대경로)
- legacy_contract_used: false
- seal_status: SEAL_OK (evaluator가 verify_seal 직접 실행 — conditions_digest sha256:cb1ab12850f89880 과 조건 22건 재계산값 일치)
- contract_seal_broken: n/a
- 재확인(Step 5): 일치
- status_transition: active -> done (APPROVE)

## Amendments
- amendments: 3 (AM-01, AM-02, AM-03 — 전부 AR-03 대상, AM-03은 RE-01과도 연동)
- PASS 근거 가능: 3 [direction=relaxing · consent=anchored]
  - AM-01: 삭제 기대 집합 1→2 (`_probe-stop-payload.sh` + `_probe-stop-payload.json`)
  - AM-02: 측정 범위에서 `mcp-needs-auth-cache.json` 제외
  - AM-03: 변경·신규 기대 집합 4→5 (`hooks/_lib-hook-payload.sh` 추가) — RE-01/AR-03 충돌 해소
- PASS 근거 불가: 0
- 집합형 direction 계산 결과 (evaluator 자체 재계산, comm 기반):
  - AM-01 → `comm -13/-23` 재계산: added=1 removed=0 (사이드카 표기와 일치)
  - AM-02 → 실측 유지: `mcp-needs-auth-cache.json` 해시 상이 확인(이전 iteration에서 검증 완료, 이번 iteration에 재변경 없음)
  - AM-03 → `comm -13/-23` 직접 재계산: added=1(`hooks/_lib-hook-payload.sh`) removed=0 → **relaxing added=1 removed=0** (사이드카 표기와 정확히 일치, 자기신고 아님)
- AM-03 앵커 독립 검증(자기신고 신뢰 안 함): 세션 jsonl(`13d78b94-....jsonl`) 라인 309에서 `AskUserQuestion` 툴 호출("RE-01 과 AR-03 의 충돌을 어느 쪽으로 푸는 게 좋을까요?")과, 라인 310에서 사용자의 실제 응답("공용 파일에 넣는다 (권함)")을 직접 확인 — 사이드카의 "근거 (redaction 거친 원문)"과 문자 그대로 일치. `consent: anchored` 유효

## User Correction Audit
- correction_log_status: available (`~/.claude/logs/claude-plugins/2026-09.md`)
- unreflected_corrections: 0 (검색 범위: 2026-09-11 11:23~12:00, session=13d78b94-... 전체 [prompt] 엔트리 재검토. AM-01/AM-02/AM-03로 이미 흡수된 논의 외 추가 미반영 교정 없음)
- verdict 영향: 없음 (표면화 전용)

## Results

### Skill (4/4)
- [x] SK-01: Communication 구간 <= 20줄 — PASS
  - 측정값: 18 (기준: <= 20)
  - 근거: `awk '/^## Communication$/{f=1} f&&/^## /&&!/^## Communication$/{exit} f' ~/.claude/CLAUDE.md | wc -l` → 18 (evaluator 직접 실행, L3)
- [x] SK-02: 같은 구간 표 0개 — PASS
  - 측정값: 0 (기준: == 0). 근거: 위 awk 출력 | `grep -cE '^\|'` → 0
- [x] SK-03: 같은 구간에 "plain-korean" 리터럴 포함 — PASS
  - 측정값: 2 (기준: >= 1). 근거: 위 awk 출력 | `grep -c 'plain-korean'` → 2
- [x] SK-04: 62개 단어쌍 전부 이관 — PASS [enumerated 62/62]
  - 근거: `glossary-baseline.txt` 62줄 전부를 `grep -F`로 `~/.claude/rules/plain-korean.md` 대조 루프 실행, 미발견 0건 (evaluator 직접 실행)

### Script (5/5)
- [x] SC-01: 목록 단어 포함 답변 차단 — PASS [goal]
  - 근거: `/tmp` 사본(`check-plain-korean.sh` + `_lib-hook-payload.sh` + `plain-korean.md`)에 Stop 페이로드 JSON을 stdin 투입 → `{"decision":"block",...}` 확인 (evaluator가 이번 iteration에 새로 재실행)
  - 음성 대조(evaluator 직접 실행, 이번 iteration 재수행): 목록 파일을 빈 파일로 교체 → 같은 입력 재실행 시 stdout 공백(통과로 뒤집힘) 확인
- [x] SC-02: 미등록 대문자 약자 + 설명 괄호 없음 → 차단 — PASS [goal]
  - 근거: "RPC 로 붙인다" → block, "RPC(설명) 로 붙인다" → pass. "SSOT 를 정합니다"(미등록 약자, 무설명) → block, "SSOT(기준이 되는 원본 문서) 를 정합니다" → pass. 규칙1(목록 단어)과 규칙2(미등록 약자) 양쪽 경로 모두 확인
  - 음성 대조(evaluator 직접 실행, `/tmp` 사본에서 `explained()` 함수를 항상 `None` 반환하도록 변조): "RPC(설명)"·"SSOT(설명)" 두 입력 모두 재실행 시 block으로 뒤집힘 확인 (판별력 유효)
- [x] SC-03: 코드/경로/주소 오탐 없음 — PASS [enumerated 6/6]
  - 근거: (a) 백틱 (b) 세겹백틱 (c) URL (d) 파일경로 (e) 명령줄 (f) 마크다운 링크 — 6종 전부 evaluator 직접 실행, exit 0 + stdout 공백 확인. 대조군("한글 백틱은 안 가린다") 은 정상적으로 block 되어 마스킹 로직이 살아있음을 함께 확인
- [x] SC-04: 한 턴 1회만 차단 — PASS [goal]
  - 근거: `stop_hook_active=true` → pass, `=false` → block. 상이 확인
  - 음성 대조(evaluator 직접 실행, `/tmp` 사본에서 `stop_hook_active` 검사 줄 제거): `true` 상태에서도 위반 입력이 block 됨 (같은 결과로 수렴 → 계약 명세와 일치, 판별력 유효)
- [x] SC-05: 사유 문자열에 낱말+대체어 동시 포함 — PASS
  - 근거: `.reason` 추출 → "오라클" 1회, "기계로 판정하는 검사" 1회 (evaluator 직접 실행)

### Error (2/2)
- [x] ER-01: 4가지 실패 상황 전부 fail-open — PASS [enumerated 4/4]
  - 근거: (a) jq 없음 — `PATH`에 jq를 뺀 전용 디렉토리(bash/python3/기타 필수 바이너리만 symlink, `command -v jq`로 NONE 확인)를 구성해 재실행 → exit 0 + 공백 (b) 빈 입력 (c) 깨진 JSON (d) 목록 파일 없음 — 4종 전부 evaluator 직접 실행, exit 0 + stdout 공백 확인
- [x] ER-02: 끄기 스위치 동작 — PASS [goal]
  - 근거: `touch ~/.claude/.plain-korean-off` → pass, 삭제 → block. 상이 확인 (테스트 후 off 스위치 파일 정리 완료)
  - 음성 대조(evaluator 직접 실행, `/tmp` 사본에서 OFF_SWITCH 검사 줄 제거): off 스위치가 존재해도 block 됨 확인 (판별력 유효)

### Architecture (3/3)
- [x] AR-01: 시험용 훅 완전 제거 — PASS [enumerated]
  - 근거: `_probe-stop-payload.sh` 부재, `_probe-stop-payload.json` 부재, settings.json 내 참조 0건 (evaluator 직접 확인)
- [x] AR-02: settings.json Stop 등록 + JSON 유효 — PASS
  - 근거: `jq . settings.json` exit 0, `check-plain-korean` 매치 1건
- [x] AR-03: 변경 파일 (AM-03 개정 기준: 5개 changed/new + 2개 deleted) — PASS [enumerated, amendment 적용, evaluator 재계산]
  - amendment 근거: AM-01+AM-02+AM-03 전부 relaxing·anchored, PASS 근거 가능 (위 Amendments 절 참조)
  - 근거: pk-baseline.txt(20줄, hash+path)와 현재 상태를 evaluator가 직접 hash-diff 재계산(자기신고 아님):
    - CHANGED(해시 상이): `CLAUDE.md`, `settings.json`, `hooks/_lib-hook-payload.sh` (3건)
    - NEW(경로 신규): `hooks/check-plain-korean.sh`, `rules/plain-korean.md` (2건)
    - → 합계 changed/new = 5건, AM-03 개정 기대값(5)과 정확히 일치
    - DELETED: `hooks/_probe-stop-payload.sh`, `_probe-stop-payload.json` (2건, AM-01 기대값과 일치)
    - 제외 확인: `mcp-needs-auth-cache.json`은 AM-02에 따라 측정 범위에서 제외, 그 외 범위 내 다른 파일(예: `remote-settings.json`, `settings.local.json`, `rules/architecture-guardrails.md` 등)은 해시 불변 확인 → 예상 밖 변경 없음
  - 원 오라클(무개정, 4+1 기대) 기준으로는 5+2가 되어 FAIL 했을 것 — amendment가 실제로 판정을 뒤집었음을 확인(discrimination 유효)

### Anti-patterns (2/2)
- [x] AP-02: force push 금지 — PASS
  - 근거: 변경 5개 파일(CLAUDE.md, settings.json, hooks/check-plain-korean.sh, hooks/_lib-hook-payload.sh, rules/plain-korean.md) 전체 `grep -riE 'git push.*--force'`, 매치 0건 (대상 5파일 전부 grep 가능한 텍스트, 패턴 유효성 확인 — 공허한 0 아님)
- [x] AP-03: bare code fence 금지 (plain-korean.md 대상) — PASS
  - 근거: `grep -n '^```' rules/plain-korean.md` → 두 fence 모두 ` ```text ` (언어 힌트 있음), evaluator 직접 확인
  - 계약/설정 결함 재확인(Iteration 1과 동일, 재현됨): project.yaml의 `command`(`validate-plugin.py --check=code-fence`)를 evaluator가 이번에도 직접 재실행 → 레포 내부 14개 플러그인만 스캔(exit 0, "Total: 14 plugins, 14 OK"), 레포 밖 대상(`~/.claude/rules/plain-korean.md`)은 검사 범위 밖 — 공허한 통과. 이 조건은 project.yaml 커맨드 대신 evaluator의 직접 grep으로 판정함(계약 결함은 Improvement에 재기록)

### Reusability (2/2)
- [x] RE-01: 재사용 가능 컴포넌트를 private 으로 두지 않음 — **PASS** (Iteration 1 FAIL → 수정 확인)
  - 근거: `check-plain-korean.sh`가 답변 되돌리기 출력을 `_lib-hook-payload.sh`의 `hook_stop_block()` 함수 호출로 위임함 (`grep -n 'hook_stop_block' check-plain-korean.sh` → 158행에서 호출 확인, `_lib-hook-payload.sh` 35행에 함수 정의 확인)
  - AR-03 충돌 해소 확인: AM-03이 `hooks/_lib-hook-payload.sh`를 AR-03의 기대 변경 집합에 명시적으로 편입시켰으므로, 이 조건을 지키는 것이 더 이상 AR-03과 충돌하지 않음을 위 AR-03 재측정으로 직접 확인
- [x] RE-02: 기존 유사 컴포넌트 재사용 — **PASS** (Iteration 1 FAIL → 수정 확인)
  - 근거: `check-plain-korean.sh` 32~34행에서 `. "$LIB"`(`_lib-hook-payload.sh`)를 source, `.stop_hook_active`(45행)와 `.last_assistant_message`(47행) 추출에 자체 jq 인라인 호출 대신 `hook_field` 함수를 호출 (`grep -n 'hook_field' check-plain-korean.sh` → 2건 매치)
  - 회귀 확인(사용자 지시 (a) 항목): `_lib-hook-payload.sh`를 소비하는 기존 훅 2종을 실제 입력으로 재검증
    - `block-dirwide-autofixer.sh`: (1) `prettier --write docs/` → deny 정상 발동 (2) `prettier --write a.md b.md` → 통과 (3) `black --check .` → 통과 (4) Bash 아닌 도구(Read) → 통과. 4가지 실제 입력 모두 기대대로 동작, 회귀 없음
    - `lint-contract-oracle.sh`: 산문-grep 패턴이 실제로 든 계약 파일(`/tmp` 스캐폴드)에 대해 경고(`hookSpecificOutput.additionalContext`) 정상 발동, 대상 아닌 파일에는 조용히 통과. 회귀 없음
    - 두 훅 모두 `bash -n` 문법 검사 통과에 그치지 않고 실제 stdin 투입으로 동작 확인(사용자 지시 "문법 검사만으로 끝내지 마라" 준수)

### Diagnostics (4/4)
- [x] DG-01: `bash -n check-plain-korean.sh` 통과 — PASS
  - 근거: evaluator 직접 실행, exit 0
- [x] DG-02: N/A — PASS
  - 근거: `ide_exclude` 빈 목록 확인 + 변경 파일(.md/.json/.sh만) 확인
- [x] DG-03: 측정 출력에 에러/예외 0건 — PASS
  - 근거: DG-01의 `bash -n` 출력 공백 + exit 0
- [x] DG-04: 다음 턴 종료 후 `.plain-korean-last.json` 에 판정 기록이 남는다 — **PASS** (Iteration 1 미판정 → 세션 transcript 원본 검증으로 확정)
  - 검증 절차: 구현자 주장("2026-09-11 11:42:29에 이 세션의 실제 턴이 Stop 훅에 막혔다")을 evaluator가 세션 jsonl(`~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/13d78b94-efc9-4ba6-8586-d5d9009d3c98.jsonl`)에서 직접 재구성해 확인함
  - 시간대 환산: jsonl 타임스탬프는 UTC(`Z`). 로컬(KST)은 UTC+9 (evaluator가 `date` 명령으로 직접 확인). 11:42:29 KST = 02:42:29 UTC
  - 증거 체인(라인 번호는 evaluator가 직접 조회한 jsonl 원본 기준):
    1. 라인 283 (`assistant`, 02:42:28.117Z): 이 세션의 실제 답변 텍스트에 목록 단어 "오라클"·"페이로드"가 백틱 없이 그대로 등장 (`"1. 목록에 있는 낱말 — "오라클" 같은 말."`, `"한글 낱말(오라클, 페이로드)은 괄호를 붙여도..."`)
    2. 라인 284 (`user`, `isMeta:true`, 02:42:29.684Z): `"Stop hook feedback:\n쉬운 말 검사에 걸렸습니다..."` — Claude Code가 Stop 훅의 차단 사유를 대화에 주입해 재시도를 강제하는 실제 메커니즘
    3. 라인 285 (`attachment`, type=`hook_blocking_error`, hookName=`Stop`, toolUseID=`97a78492-...`): 위와 동일한 차단 사유 원문 포함
    4. 라인 295 (`system`, subtype=`stop_hook_summary`, parentUuid가 라인285 attachment의 uuid와 일치, toolUseID 동일, 02:42:29.899Z): `hookCount:5`의 하나로 `"command":"쉬운 말 검사"`(= check-plain-korean.sh의 훅 등록명), `hookErrors`에 "[바꿔 쓸 말] \"오라클\" -> ...", "[바꿔 쓸 말] \"페이로드\" -> ..." 원문 그대로 포함 — Claude Code 엔진 자신이 기록한 시스템 로그이며 모델이 서술한 내용이 아님
    5. 라인 287~288 (`assistant`/`user` tool_result, 02:42:41.281Z~.525Z): 이 세션이 직접 `cat ~/.claude/.plain-korean-last.json; ls -la ...`를 실행한 결과 — `{"verdict":"block","at":"2026-09-11 11:42:29","hits":2}` + 파일 mtime `Sep 11 11:42` — 기록 시각이 위 stop_hook_summary 시각(11:42:29 KST)과 정확히 일치, 그리고 직전 평가자가 이 계약을 평가한 시각(11:51)보다 9분 앞섬
    6. 라인 290 (`assistant`, 02:42:58.133Z, 재시도 턴): "훅이 방금 제 답변을 실제로 막았습니다..." — 이후 라인 296 (`system stop_hook_summary`, 02:42:59.700Z)의 `hookErrors:[]`로 재시도 턴은 깨끗이 통과함을 확인
  - 결론: 직전 평가자가 관찰한 "11:48:33, hits:1" 기록은 이 evaluator가 SC/ER 조건 검증을 위해 수동 호출한 부산물이 맞다(그 시각 이후 여러 차례 수동 재실행이 있었음). 그러나 그와는 **별개로, 그보다 앞선 11:42:29 시점에 이 세션의 실제 턴이 Stop 훅에 의해 자동으로 막힌 사건이 시스템 로그(모델이 생성하지 않은 `stop_hook_summary` 이벤트)로 독립 확인된다.** 이는 서술적 주장이 아니라 Claude Code 엔진이 직접 기록한 비모델 산출물이므로 증거 유효성 검사(비공백/활성화/반증가능성/출처/실행가능성)를 모두 통과한다 — 훅이 실제 세션에서 자동으로 돌았다는 조건의 요구를 충족

## Unverifiable Summary
- invalid_evidence: 0
- env_gaps: 0
- verified_coverage: (22 - 0) / 22 = 1.00 (임계 0.60 이상 — 통과)
- 연속 ENV 승급: 해당 없음 (DG-04는 Iteration 1의 `[미검증:ENV]`에서 이번 iteration에 독립 transcript 증거로 PASS 확정 — 같은 조건이 2회 연속 ENV였던 것이 아니라 1회 ENV 후 증거 보강으로 해소된 사례)
- Verdict 영향: 통상 (미검증 0건)

## Discrimination (규칙 12 적용 조건)
- 적용 조건: SC-01, SC-02, SC-04, ER-02 (계약이 명시적으로 "음성 대조" 절을 요구하는 `[goal]` 조건)
- 결합 확인: 4개 조건 모두 측정이 `/tmp` 사본의 `check-plain-korean.sh` 실물 스크립트를 직접 경유(stdin→stdout 파이프, 우회 없음). 사본은 원본과 동일 내용을 복사한 것이며 이번 iteration에 evaluator가 새로 생성·검증함
- 음성 대조: 4개 조건 모두 계약에 "음성 대조:" 절 기재 있음. evaluator가 각 가드 로직(빈 목록/설명검사/stop_hook_active검사/off-switch검사)을 직접 무력화해 재실행 → 4건 전부 계약이 예고한 대로 판정이 뒤집힘 확인 (원본 파일은 건드리지 않음, 사본은 시스템 /tmp에만 존재하며 평가 종료 후 삭제)
- AR-03: 9항목(동시성/인증/멱등성/입력검증/데이터유실/마이그레이션/재시도/보안경계/사용자보고충돌) 어디에도 해당하지 않아 본 게이트 비적용 대상이나, evaluator가 자발적으로 원 오라클(4+1 기대) vs 개정 오라클(5+2 기대) 교차 계산하여 amendment의 실효성(FAIL→PASS 반전)을 재확인함

## User-Reported Failures
- 해당 없음 (사용자의 "아직 깨져 있다" 류 실패 보고 없음. DG-04 관련 논쟁은 "구현자가 이전 QA의 미판정을 증거로 반박"한 사례로, User-Reported Failure 프로토콜(REOPENED)이 아니라 §미검증/FAIL triage 재평가로 처리함 — 세션 transcript 원본 증거로 독립 확인 완료)

## Summary
- Total: 22/22 conditions passed
- Verdict: **APPROVE**
- Iteration 1 대비 변화:
  1. RE-02 FAIL → PASS: `check-plain-korean.sh`가 `_lib-hook-payload.sh`를 source하고 `hook_field`를 사용하도록 수정 확인. 기존 훅 2종(`block-dirwide-autofixer.sh`, `lint-contract-oracle.sh`) 회귀 없음을 실제 입력으로 재확인
  2. RE-01 FAIL → PASS: `_lib-hook-payload.sh`에 `hook_stop_block()` 함수 추가 + AM-03(relaxing·anchored, 세션 transcript로 앵커 독립 검증됨)으로 AR-03 기대 집합을 5개로 확장 — 구조적 충돌 해소 확인
  3. DG-04 미판정 → PASS: 세션 jsonl 원본에서 11:42:29 KST(02:42:29 UTC)의 실제 자동 차단 이벤트(`stop_hook_summary`, 모델이 생성하지 않은 시스템 로그)를 독립 확인. 직전 평가자가 본 "11:48:33 hits:1" 기록은 evaluator의 수동 테스트 부산물이 맞지만, 그와 별개로 더 이른 11:42:29의 자동 차단은 실재했음을 확인

## Improvement Suggestions
- [AP-03] 측정-환경-오염 — project.yaml의 `command`(`validate-plugin.py --check=code-fence`)가 레포 내부 플러그인만 스캔해 레포 밖 대상(`~/.claude/rules/plain-korean.md`)에는 공허한 exit 0을 낸다. Iteration 1에서 이미 지적됐고 이번에도 재현됨(2회째) — `contract_ambiguity_notes`로 승격: 이 프로젝트의 anti_patterns 설정에 "대상이 레포 밖일 때는 이 command를 건너뛰고 evaluator 직접 grep으로 대체"를 명시하거나, 범용 code-fence 검사 스크립트를 별도로 두어라
- [DG-04] 측정-상태-모호 — "이 세션의 다음 턴이 끝난 뒤"라는 조건은 평가 시점에 아직 도래하지 않은 미래 상태를 요구해 evaluator가 그 시점에 원천적으로 확정 불가능한 구조였다(Iteration 1은 이 때문에 미검증 처리). 세션 jsonl 원본을 직접 열람하는 fallback이 있다는 것을 계약에 미리 명시했다면 Iteration 1에서 즉시 PASS 판정이 가능했을 것 — 다음부터는 "다음 턴 종료 후 기록" 류 조건에 `fallback: 세션 jsonl에서 stop_hook_summary 이벤트로 사후 검증 가능`을 측정 절에 병기하라
