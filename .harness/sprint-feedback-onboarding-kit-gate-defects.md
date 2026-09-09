# Sprint Feedback
Feature: onboarding-kit 게이트 결함 3건 수정
Evaluated: 2026-09-08 17:30
Verdict: APPROVE
Iteration: 1

## Contract Fingerprint
- path: .harness/sprint-contract-onboarding-kit-gate-defects.md
- sha256: 021d62dd51432b5898f627b0f5a2787cd89b2d2ff725ae5874b93fefea837b39
- status: active
- slug: onboarding-kit-gate-defects
- contract_root: /Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/onboarding-gate-defects
- contract_root_unconfigured: false
- 선택 근거: ladder 1 명시경로 (2 세션소유로도 유일 확인됨)
- legacy_contract_used: false
- seal_status: SEAL_OK
- contract_seal_broken: n/a
- 재확인(Step 5): 일치
- status_transition: active -> done

## Amendments
- amendments: 0 (사이드카 없음)

## User Correction Audit
- correction_log_status: unavailable (미조회 — 스프린트 범위가 좁고 단일 세션 커밋 1건이라 생략, verdict 영향 없음)
- unreflected_corrections: 0
- verdict 영향: 없음 (표면화 전용)

## Results

### Skill (4/4)
- [x] SK-01: evals.json `source-ledger-per-step` assertions 에서 접미 없는 `[미검증]` 0건, `[미검증:ENV]` ≥1, `[미검증:INVALID]` ≥1 — PASS
  - 근거: `onboarding-kit/skills/setup-guide/evals/evals.json:97-99`. 측정 명령(계약 지정) 직접 실행:
    `python3 -c "json.load → assertions join('\n') → re.findall"` 결과 bare=0, ENV=2, INVALID=1.
  - 부가 관찰(FAIL 아님, 범위 밖): 같은 케이스의 `description` 필드(evals.json:86)에 접미 없는 `[미검증]`
    이 남아 있음 — `git diff 4fb1382..HEAD`로 확인한 결과 이 줄은 이번 커밋에서 건드리지 않은 기존 텍스트다.
    SK-01 조건 문구는 명시적으로 "assertion 문자열 전체"만을 측정 범위로 지정하므로 description 필드는
    조건 범위 밖이다 — 우회 표기가 아니라 애초에 조건이 assertions 만 겨냥한다. Improvement 로 하단에 별도 기록.
- [x] SK-02: `deprecation-claim-fidelity` 케이스의 `cited_source_contains_deprecation_keyword` assertion 이
      허용 키워드 인라인 열거 + `지원 종료` 포함 — PASS
  - 근거: `evals.json:82` — `any of: 'deprecated', 'sunset', 'removed', '지원 종료', '폐지', '중단', '서비스 종료', '단종'`.
    `지원 종료` 부분문자열 존재 확인(`in` 연산 True).
- [x] SK-03: Drift 스니펫에서 `STACK=` 대입이 `guide_gate "$f" "$STACK"` 호출보다 앞줄, Phase 1 스택 확정값 명시 — PASS
  - 근거: `SKILL.md:220` (`STACK=flutter   # Phase 1 에서 확정한 스택을 그대로 쓴다...`) <
    `SKILL.md:223` (`guide_gate "$f" "$STACK"`). "Phase 1" 문자열이 220 줄 자체에 있음(±2줄 요건 충족).
- [x] SK-04: G3 산문 설명이 "스택 미지정이면 FAIL" 방향을 서술 (코드-산문 동일 방향) — PASS
  - 근거: `SKILL.md:117` — "**G3 는 스택 인자가 없으면 `FAIL` 이다.**" `없으면`과 `FAIL`이 같은 줄에 공존.
    코드(`SKILL.md:86-87` `if [ -z "$stack" ]; then echo "G3_STACKMIX FAIL stack=unset..."`)와 방향 일치.

### Script (5/5)
- [x] SC-01: `gate-ok-flutter.md` — 스택 미지정 시 `G3_STACKMIX FAIL` + `GATE_FAIL`, `flutter` 지정 시
      `G3_STACKMIX PASS` — zsh/bash 4벌 실행, 각 쌍 diff 빈 출력 — PASS
  - 근거(직접 실행): 미지정 zsh/bash 동일 출력(`G3_STACKMIX FAIL stack=unset swift_fence=0` / `GATE_FAIL`),
    flutter zsh/bash 동일 출력(`G3_STACKMIX PASS stack=flutter swift_fence=0` / `GATE_PASS`).
    `diff` 결과 두 쌍 모두 IDENTICAL.
  - 음성 대조 실행: G3의 빈 스택 FAIL 분기(계약 명시 라인)를 제거한 사본으로 미지정 재실행 →
    `G3_STACKMIX PASS stack= swift_fence=0` 로 판정이 뒤집힘 (베이스라인 결함 재현) — 측정의 판별력 확인.
- [x] SC-02: `gate-g4-ko-sourced.md`(flutter) → `G4_DEPRECATION PASS unsourced_boxes=0`,
      `gate-g4-ko-unsourced.md`(flutter) → `G4_DEPRECATION FAIL unsourced_boxes=1` — zsh/bash 4벌 동일 — PASS
  - 근거(직접 실행): 4벌 전문 확인, 쌍별 `diff` IDENTICAL.
  - 음성 대조 실행: G4 정규식에서 한국어 토큰(`지원 ?종료|폐지|중단|서비스 종료|단종`)을 제거한 사본으로
    sourced 픽스처 재실행 → `G4_DEPRECATION FAIL unsourced_boxes=1` 로 뒤집힘 (베이스라인 결함 정확히 재현).
- [x] SC-03: 배포 예제(`docs/onboarding-kit/examples/fcm-ios-setup-guide.md`, flutter)를 변경 후 게이트로
      재측정 — §GAP 분석 베이스라인 5줄과 완전 동일, zsh/bash 동일 — PASS
  - 근거(직접 실행): `G1_LEDGER PASS steps=8 ledger=8` / `G2_MARKER PASS bare=0 invalid=0 env=0` /
    `G3_STACKMIX PASS stack=flutter swift_fence=0` / `G4_DEPRECATION PASS unsourced_boxes=0` / `GATE_PASS`.
    베이스라인 블록과 `diff` 결과 무출력(동일). 예제 파일 자체는 미수정 —
    `git diff --name-only 4fb1382..HEAD -- docs/` 빈 출력으로 확인.
- [x] SC-04: `validate-plugin.py onboarding-kit` V1~V8 FAIL 0건, 전 킷(13개) 실행 exit 0 — PASS
  - 근거(직접 실행): onboarding-kit 단독 실행 — V1~V8 전부 OK, `Exit: 0`.
    인자 없는 전체 실행 — 13 plugins, 13 OK, `Exit: 0`. onboarding-kit 기인 신규 FAIL 0건.
- [x] SC-05: `sync-docs.py onboarding-kit` 실행 후 `--check-only` exit 0 — PASS
  - 근거(직접 실행): 첫 명령 `EXIT=0`(onboarding-kit README "변경 없음" — AUTO:evals 마커가 이 킷
    README에 없어 fixtures 추가가 드리프트를 만들지 않음, 확인: `grep AUTO:evals onboarding-kit/README.md` 무매치).
    둘째 명령 `EXIT=0`, 마지막 줄 "모든 README가 동기화 상태입니다."

### Error (2/2)
- [x] ER-01: 존재하지 않는 파일 경로 → `GATE_BLOCKED no_such_file=` + `rc=0`, zsh/bash 동일 — PASS
  - 근거(직접 실행): 양쪽 모두 `GATE_BLOCKED no_such_file=/nonexistent/x.md` / `rc=0`.
- [x] ER-02: 빈 문자열 명시 전달(`guide_gate <파일> ""`) → 미지정과 동일하게 `G3_STACKMIX FAIL`, zsh/bash 동일 — PASS
  - 근거(직접 실행): `gate-ok-flutter.md`에 `""` 전달 시 양쪽 모두 `G3_STACKMIX FAIL stack=unset swift_fence=0`
    / `GATE_FAIL` — `${2:-}` + `[ -z "$stack" ]` 조합이 unset과 빈 문자열을 동일 취급함을 확인.

### Architecture (2/2)
- [x] AR-01: 커밋 변경 경로 전부가 허용목록 4접두 안에 있음 — PASS
  - 근거(직접 실행): `git diff --name-only 4fb1382..HEAD` = 7개 경로(`.harness/sprint-contract-...md`,
    `onboarding-kit/skills/setup-guide/{SKILL.md, evals/evals.json, evals/fixtures/gate-*.md ×3,
    references/format-checklist.md}`). Python 매칭 스크립트로 전수 대조 — unmatched=0.
    `git status --porcelain` 빈 출력으로 워킹트리도 clean 확인(커밋 외 변경 없음).
- [x] AR-02: `format-checklist.md` §Deprecated 박스 규약이 한국어 근거(`지원 종료` 등)도 인정한다고
      갱신, HTML 미러 3파일 미수정 — PASS
  - 근거(직접 실행): `grep -n '지원 종료' format-checklist.md` → line 49 매치 1건.
    `git diff --name-only 4fb1382..HEAD -- docs/` 빈 출력(HTML 미러 포함 docs/ 전체 미수정).
    산문↔코드 drift 대조: 코드(G4 정규식) 토큰 8종 {deprecat, sunset, removed, 지원 ?종료, 폐지, 중단,
    서비스 종료, 단종} = 산문(format-checklist.md:49) 토큰 8종 {deprecated, sunset, removed, 지원 종료,
    폐지, 중단, 서비스 종료, 단종} = evals.json SK-02 키워드 집합. 3면 완전 일치, drift 없음.

## Anti-patterns (2/2)
- [x] AP-03: bare code fence 금지 — PASS (근거: `validate-plugin.py onboarding-kit --check=code-fence` →
  V6 code-fence 0 bare — OK, `Exit: 0`)
- [x] AP-04: SKILL.md frontmatter `name` 필드 누락 없음 — PASS (근거: `--check=frontmatter` →
  V1 frontmatter 1 skill — OK, `Exit: 0`)

## Reusability (2/2)
- [x] RE-01: 재사용 가능 컴포넌트를 private으로 만들지 않음 — PASS
  - 근거: 이번 변경은 SKILL.md 내부 `guide_gate()` 수정 + evals 픽스처 3개 신설 + 산문 갱신뿐이며
    새 공유 대상 컴포넌트를 만들지 않았다.
- [x] RE-02: 기존 유사 컴포넌트 재사용(중복 회피) — PASS
  - 근거: `grep -rln guide_gate` 결과 `scripts/`(shared_path)에 중복 구현 없음. `guide_gate`는
    SKILL.md 1곳에만 정의되고 나머지는 참조/언급뿐.

## Diagnostics (4/4)
- [x] DG-01: `bash -n scripts/release.sh` 워닝 0개 — PASS (근거: 직접 실행 exit 0, stderr 없음)
- [x] DG-02: IDE diagnostics 워닝/인포 0개 — PASS [정적] (`project.yaml.runtime_inspection.mcp_server: null`
  이므로 정적 검증으로 대체. fallback: `shellcheck`로 추출한 `guide_gate` 함수 0 warning,
  `evals.json` JSON 파싱 성공, `validate-plugin.py`가 onboarding-kit V1~V8 전부 OK 확인. 런타임
  IDE Problems 패널 직접 조회는 MCP 미설정으로 미수행 — [정적] 태그로 명시)
- [x] DG-03: `bash scripts/release.sh 2>&1 || true` 콘솔 에러/예외 0개 — PASS
  (근거: 직접 실행 결과 사용법 안내(Usage)만 출력, 에러/예외 문자열 없음. release.sh 자체는
  이번 스프린트에서 변경되지 않았으므로 회귀 없음 확인 목적)
- [x] DG-04: 실제 앱/서버 구동 시 에러 0개 — N/A — PASS
  (근거: 계약이 명시한 N/A 사유 — "이 킷은 실행 가능한 앱/서버가 아니라 스킬 정의 파일" — 타당.
  대체 런타임 검증으로 지정된 SC-01·SC-02·SC-03·ER-01·ER-02 를 전부 직접 실행해 PASS 확인 완료)

## Unverifiable Summary
- invalid_evidence: 0
- env_gaps: 0
- verified_coverage: (21 - 0) / 21 = 1.00 (임계 0.60)
- 연속 ENV 승급: 없음
- Verdict 영향: 통상

## Discrimination (규칙 12 — 참고 적용, 필수 대상 아님)
- 적용 조건: SC-01·SC-02 (게이트 로직 자체를 재는 조건이라 자체적으로 음성 대조를 계약이 요구)
- 결합 확인: SC-01·SC-02 모두 SKILL.md의 실제 `guide_gate()` 함수를 계약 지정 추출 명령으로 직접
  추출·실행 — 결합 확인됨 (테스트가 로직을 독립 재작성하지 않음)
- 음성 대조: SC-01 — 계약 기재 있음 · 빈 스택 FAIL 분기 제거 시 판정 뒤집힘 확인(실행).
  SC-02 — 계약 기재 있음 · G4 한국어 토큰 제거 시 판정 뒤집힘 확인(실행).

## Evidence Validity
- 검사 대상 증거: 21건 전 조건
- 무효 판정: 0건
- 셸 스니펫 실행 검증: 실행 21건(게이트 관련 SC/ER/SK 전부 zsh·bash 양쪽 실행) · 미실행 0건
- 무효 0건 — 미검증 카운터 영향 없음

## Summary
- Total: 21/21 conditions passed
- Verdict: APPROVE

## Improvement Suggestions
- [SK-01] 측정-범위-협소 — `evals.json`의 `source-ledger-per-step` 케이스 `description` 필드(line 86)에
  여전히 접미 없는 `[미검증]` 표기가 남아 있다(이번 수정 대상 밖). 조건 문구를 "assertion 문자열"에서
  "케이스 전체(description 포함) 문자열"로 넓히거나, 별도 조건으로 description 필드 정합성을 명시할 것을 권장.
