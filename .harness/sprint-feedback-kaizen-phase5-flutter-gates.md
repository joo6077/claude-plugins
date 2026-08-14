# Sprint Feedback
Feature: 카이젠 Phase 5 — flutter-toolkit 버전 사실 정정 + Primitive Substitution Gate(G1) · invalidate 경계(G2) · 위젯 테스트 하네스(G3) · 성능 환경 배제(G4)
Evaluated: 2026-08-14 00:00
Verdict: APPROVE
Iteration: 재평가 (독립 재판정 — 글로벌 피드백 풀 누락분 복구)

## 재평가 사유

이 계약은 이미 `status: done` 이며 이전 iteration 에서 APPROVE 를 받았으나, structured output
schema 강제로 인해 피드백 저장 단계가 실행되지 않아 글로벌 피드백 풀에 아티팩트가 없었다.
본 재평가는 이전 판정을 승계하지 않고 23개 조건 전부를 처음부터 독립적으로 재검증했다.

## Contract Fingerprint
- path: /Users/jackson/Hub/10_Dev/claude-plugins/.harness/sprint-contract-kaizen-phase5-flutter-gates.md
- sha256(conditions_digest): sha256:5853e8a469993a57 (recorded=actual, SEAL_OK)
- status: done (재평가로 인해 변경하지 않음 — 이미 done)
- slug: kaizen-phase5-flutter-gates
- contract_root: /Users/jackson/Hub/10_Dev/claude-plugins
- contract_root_unconfigured: false
- 선택 근거: 사용자 명시 지정 (재평가 대상으로 직접 지정됨)
- legacy_contract_used: false
- 재확인(Step 5): 일치 (SEAL_OK, TOCTOU 없음)
- status_transition: skipped (verdict=APPROVE 이나 status 가 이미 done — 되돌리지 말라는 지시에 따라 미변경)
- 구현 커밋: a35e5cc (본 구현) + a90448a (AP-03 blocking 해소 fix). 이후 phase5 관련 추가 커밋 없음
  (a35e5cc..a90448a 사이 e7b9508 은 Phase 10 react-kit 커밋으로 무관 — 개별 `git show --name-only`
  로 phase5 두 커밋만 분리 확인)

## Amendments
- amendments: 2 (AM-01, AM-02 — 둘 다 `.harness/sprint-amendments-kaizen-phase5-flutter-gates.md`)
- narrowing: 0
- relaxing / unknown: 0 — 사이드카 본문이 명시적으로 "어떤 조건의 PASS 근거로도 쓰이지 않는다" 라고
  선언. AM-01 은 AP-03 오라클 결함의 관측 기록(구현을 고쳐서 원 측정문을 문자 그대로 충족했다는
  기록), AM-02 는 harness Scope 밖 핸드오프. 둘 다 direction 없음 · PASS 근거로 사용하지 않음을
  본 재평가에서도 그대로 준수 — AP-03 은 원 측정문 그대로 재검증했고 실제로 PASS 했다 (아래 참조)

## User Correction Audit
- correction_log_status: unavailable (read-union glob 으로 reflect-kit 로그 버킷 미발견 —
  `basename`/`basename-??????` 둘 다 없음)
- unreflected_corrections: 0 (로그 부재로 대조 불가, BLOCKED 사유 아님)
- verdict 영향: 없음

## Results

### Skill (10/10)
- [x] SK-01: Freezed `.when`/`.map` 절대 제거 단정 잔존 — PASS
  - 근거: `grep -rn 'when' flutter-toolkit docs/flutter | grep -E 'map' | grep -E '제거|removed' | grep -v '3\.1\.0' | wc -l` → 측정값 0 (zsh/bash 동일). 음성 대조 재현: `3.1.0` 토큰을 제거하면 11건 검출 — 오라클 판별력 확인 (L3)
- [x] SK-02: Primitive Substitution Gate SSOT 단일화 — PASS
  - 근거: `grep -rln 'primitive-substitution-gate' flutter-toolkit | LC_ALL=C sort` → `flutter-toolkit/agents/widget-inspector.md`, `flutter-toolkit/skills/flutter-audit/SKILL.md`, `flutter-toolkit/skills/flutter-screen/SKILL.md`, `flutter-toolkit/skills/flutter-widget/SKILL.md` 4개, 기대 집합과 정확히 일치. SSOT 파일 자신은 자기참조 0건 (L3)
- [x] SK-03: 대상 8종 + 면제 5종 명시 — PASS
  - 근거: `flutter-toolkit/references/primitive-substitution-gate.md:37-44` 8종 표(Divider·Button·Chip·Card·ListTile·Switch·TextField·CircularProgressIndicator) + `:46-50` 면제 목록(Text·Row·Column·Padding·SizedBox) "금지하지 않는다" 문구 확인 (L3, Read)
- [x] SK-04: flutter-provider select/invalidate 조항 — PASS
  - 근거: `grep -c 'select('` = 4, `grep -c 'ref.invalidate'` = 4 (둘 다 ≥1), `flutter-toolkit/skills/flutter-provider/SKILL.md:30-31` Read 확인 — (a) select 선언형 연결 조항, (b) invalidate 열거 조항 모두 존재 (L3)
- [x] SK-05: onManualInvalidation 버전 가드 — PASS
  - 근거: `grep -rn 'onManualInvalidation' flutter-toolkit docs/flutter | grep -v '3\.4' | wc -l` → 0 (zsh/bash 동일). 매칭 3개 라인 전부 `3.4.x` 문자열 동반 확인 (`flutter-provider/SKILL.md:29,33,234`) (L3)
- [x] SK-06: widget test 하네스 2파일 존재 — PASS
  - 근거: `grep -rln 'tester.container()' flutter-toolkit/skills/flutter-test/SKILL.md docs/flutter/quality/testing.md` → 2행 모두 일치 (L2)
- [x] SK-07: coverage 조항 + 16종 수치 인용 — PASS
  - 근거: `flutter-toolkit/skills/flutter-test/SKILL.md:117` `"LG-01: 16종 매핑 단위 테스트 커버리지 부족 (2종만 검증)"` 인용 확인 (L2)
- [x] SK-08: Environment Exclusion Checklist 8항목 양쪽 존재 — PASS
  - 근거: 8개 토큰(profile mode·physical device·simulator/emulator·swap·DevTools trace·Impeller·refresh rate·slowest target device) 전부 `flutter-audit/SKILL.md`(라인 253-260) 및 `docs/flutter/quality/performance.md`(라인 25-32) 양쪽에서 매치 확인 (L3)
- [x] SK-09: 미검증 판정 규칙 양쪽 존재 — PASS
  - 근거: `flutter-audit/SKILL.md:262-263` "simulator/emulator 또는 debug mode 결과만 있으면 앱 코드 성능 병목으로 확정하지 말고 `[미검증]`" / `docs/flutter/quality/performance.md:38-39` 동일 취지 확인 (L3)
- [x] SK-10: qa-evaluation-guide 인용 + REOPENED 미정의 — PASS
  - 근거: `flutter-audit/SKILL.md:32,55-56,66` §Canonical Unverified-Evidence Protocol / §Canonical User-Reported Failure Protocol / §Evidence Validity Gate 인용 확인, `grep -n 'REOPENED'` → 0건 (L3)

### Error (3/3)
- [x] ER-01: Impeller 낡은 단정 0건 — PASS
  - 근거: `grep -rn -e '--enable-impeller' -e 'Web/Windows/Linux 미지원' ... flutter-toolkit docs/flutter | grep -v '정정 2026-08-13' | wc -l` → 0 (zsh/bash 동일) (L3)
- [x] ER-02: Flutter 3.44 stable 단정 0건 — PASS
  - 근거: `grep -rn '2026-07 stable\|...' flutter-toolkit docs/flutter | grep -v '정정 2026-08-13' | wc -l` → 0 (zsh/bash 동일) (L3)
- [x] ER-03: 넣지 말 것 3종 금지 조항 명문화 — PASS
  - 근거: G1 `primitive-substitution-gate.md:46-50` "금지하지 않는다"/과잉규칙 서술 + `flutter-audit/SKILL.md:427` "MUST NOT ... layout primitive 로 확대 적용하지 않는다". G2 `flutter-provider/SKILL.md:31,233` "모든 mutation 후 전체 family invalidate 는 하지 마라"/"MUST NOT". G4 `flutter-audit/SKILL.md:264`, `performance.md:39` "iOS simulator ... 쓰지 마라" — 3종 전부 확인 (L3)

### Architecture (3/3)
- [x] AR-01: 변경 17개 경로 한정 — PASS [측정 상태 적응 — 아래 참조]
  - 근거: 계약의 측정문 전제("Given: 커밋 직전 스테이징 완료 후")는 이미 커밋 완료된 현재 상태와
    맞지 않아(스테이징 0건) 문자 그대로 재현 불가. 대안으로 Phase 5 실제 구현 커밋 2개
    (`a35e5cc`, `a90448a`)를 개별 `git show --name-only`로 분리 확인해 union한 결과(`.harness/`
    제외)가 계약이 열거한 17개 경로 집합과 `diff` 0으로 정확히 일치함을 확인. 두 커밋 사이에
    끼어 있는 `e7b9508`(Phase 10 react-kit, 무관 커밋)의 `docs/react/*` 파일은 개별 커밋
    분리로 정확히 제외됨 (L3)
- [x] AR-02: research-log.md 정정 주석 전수 — PASS
  - 근거: `grep -nE '...' docs/flutter/research-log.md | grep -v '정정 2026-08-13' | wc -l` → 0 (zsh/bash 동일). 음성 대조 재현: `[정정 2026-08-13]` 주석 1건 제거 시 7건 검출 — 오라클 판별력 확인 (L3)
- [x] AR-03: Phase 5 라운드 헤더 + last_updated — PASS
  - 근거: `docs/flutter/research-log.md:8` `## [2026-08-13] — Phase 5 kaizen`, frontmatter `last_updated: 2026-08-13` (L2)

### Anti-patterns (2/2)
- [x] AP-03: bare code fence 0건 (계약 원 측정문 그대로) — PASS
  - 근거: `python3 scripts/validate-plugin.py flutter-toolkit` → exit 0, `V6 code-fence 0 bare — OK`.
    변경된 `docs/flutter/*.md` 5개 파일 각각 `grep -cE '^```$'` = 0, 합계 0 (zsh/bash 동일).
    이전 iteration의 REJECT 사유(합계 6)는 fix 커밋 `a90448a`가 4-backtick 펜스 전환으로
    구현 자체를 고쳐 해소했다 — amendment 재해석이 아니라 원 측정문 문자 그대로 충족 (L3)
- [x] AP-01: 신규 URL·버전 토큰 전부 evidence 파일 또는 기존 본문에 실재 — PASS
  - 근거: `git show -U0 a35e5cc/a90448a -- flutter-toolkit docs`의 추가 줄에서 URL 13개 추출,
    그중 11개는 `.harness/.meta/evidence/phase5.md`에 직접 인용, 나머지 2개
    (`migrate-to-agp-9`, `release-notes-3.44.0`)는 diff 컨텍스트 확인 결과 수정 전 버전에도
    이미 존재하던 URL로 "기존 본문에 실재" 조항 충족 (날조 0건) (L3)

### Reusability (2/2)
- [x] RE-01: Gate 위젯 목록 재열거 0건 — PASS
  - 근거: `CircularProgressIndicator` 매치 파일 2개(`primitive-substitution-gate.md`,
    `flutter-widget/SKILL.md`) 중 후자(`:28`)는 Read로 맥락 확인 결과 Primitive Substitution
    Gate와 무관한 기존(pre-existing) Gotcha("기존 위젯 수정이 기본값" 규칙)의 예시 언급으로,
    게이트 목록 재열거가 아님을 확인. `flutter-widget/SKILL.md:25`의 신규 Gate 조항 자체는
    "여기서 목록을 다시 세지 마라"라고 명시하며 목록을 재열거하지 않음 (L3, grep 오탐 필터링 적용)
- [x] RE-02: 기존 SSOT 인용 패턴 준수 — PASS
  - 근거: `visual-evidence-protocol.md`의 "절차 전문: `references/visual-evidence-protocol.md`" 인용 스타일과 동일하게, 4개 소비 표면 전부 "그 파일이 SSOT 다 — 여기서 목록을 다시 세지 마라" 패턴으로 인용 (`flutter-widget/SKILL.md:25`, `flutter-screen/SKILL.md:19`, `flutter-audit/SKILL.md:22,427`, `widget-inspector.md:105,120,219`) (L3)

### Diagnostics (3/3)
- [x] DG-01: validate-plugin.py FAIL 0 — PASS
  - 근거: `python3 scripts/validate-plugin.py flutter-toolkit` → `Total: 1 plugins, 1 OK / Exit: 0` (L1 실행 확인)
- [x] DG-02: sync-docs --check-only Scope 밖 요구 없음 — PASS
  - 근거: `python3 scripts/sync-docs.py --check-only` → "모든 README가 동기화 상태입니다" (전체 킷 포함 drift 0건) (L1 실행 확인)
- [x] DG-04: 전 grep 오라클 zsh/bash 출력 동일 — PASS [평가자 환경 노트 포함]
  - 근거: SK-01/SK-05/ER-01/ER-02/AR-02/AP-03의 wc -l 카운트 오라클은 zsh·bash 동일(각각 직접 실행 확인). SK-06/RE-01 등 순서 민감 오라클은 최초 시도에서 zsh 세션 내 `grep`이 이 평가 세션 고유의 Claude Code 셸 스냅샷 함수(`ugrep` 병렬 스캔 래퍼, `~/.claude/shell-snapshots/snapshot-zsh-*.sh`)로 shadow되어 동일 명령 반복 실행 시에도 파일 순서가 비결정적으로 뒤바뀌는 현상을 발견했다. `command grep`(래퍼 우회, 순정 `/usr/bin/grep`)으로 재실행하니 zsh·bash 모두 5회 반복 동일 순서로 결정적이었다(`diff` 0) — 즉 이 비결정성은 실제 사용자 zsh 터미널이나 계약 오라클 자체의 결함이 아니라 이 평가 세션의 Bash 도구 전용 안전 래퍼 아티팩트였다. 실사용 환경을 대표하는 순정 grep 기준으로 DG-04 PASS 처리 (L3, 실행 검증 + 근본원인 격리)

## Unverifiable Summary
- 총 미검증 건수: 0
- Verdict 영향: 해당 없음 (0건이므로 자동 REJECT 임계 미해당)

## Evidence Validity
- 검사 대상 증거: 23건 (조건별 1건씩)
- 무효 판정: 0건
- 셸 스니펫 실행 검증: 실행 23건(전 조건 명령 직접 실행) · zsh/bash 양쪽 확인 8건(오라클 명시 요구 조건: SK-01·SK-04·SK-05·SK-06·ER-01·ER-02·ER-03·AR-02·AP-03·RE-01·AR-03, DG-04 전수) · 미실행 0건
- 무효 0건은 미검증 카운터에 영향 없음 (누계 0)

## Anti-patterns (project.yaml 전역, 23조건과 별개)
- AP-01(hardcoded version): 0건 매치 (대상 17파일)
- AP-02(git push --force): 0건 매치
- AP-03(bare fence): naive grep 정보성 카운트 확인(닫는 펜스 포함 시 79건, 열린 펜스 기준은 validate-plugin V6 0건으로 판정) — 계약 AP-03과 동일 결론
- AP-04(frontmatter name 누락): 10개 SKILL.md/agents/*.md 파일 전부 `name:` 필드 존재 확인

## Summary
- Total: 23/23 conditions passed
- Verdict: APPROVE
- 이 재평가는 이전 iteration의 판정을 승계하지 않고 23개 조건 전부를 독립적으로 처음부터
  재검증했다. 결함 발견 없음 — 이전 iteration에서 발견된 AP-03 blocking(합계 6)은 fix 커밋
  `a90448a`가 구현을 고쳐(4-backtick 펜스 전환) 원 측정문 그대로 해소했음을 재확인했다.

## Improvement Suggestions
- [AR-01] 측정-상태-모호 — 계약이 "Given: 커밋 직전 스테이징 완료 후"라는 상태 전제를 명시했으나, 재평가처럼 이미 커밋이 완료된 시점에는 이 전제를 재현할 방법이 없다. 향후 계약 작성 시 "커밋 완료 후 재평가되는 경우 `git show --name-only <commit1> <commit2> ...`의 union으로 대체 가능"이라는 fallback 문구를 측정문에 병기할 것을 권장
- [DG-04] 환경-아티팩트 — 이 레포에서 Claude Code Bash 도구로 zsh 오라클을 검증할 때, 세션에 따라 `grep`이 `ugrep` 병렬 스캔 래퍼로 shadow되어 다중 파일 대상 `grep -rl` 계열 명령의 출력 순서가 비결정적일 수 있다. 향후 순서 민감 오라클(정렬 없는 `grep -rln` 등)은 계약 측정문에 `| LC_ALL=C sort`를 기본으로 포함시켜 이런 환경 아티팩트에 영향받지 않게 하는 것을 권장 (SK-02는 이미 이 패턴을 쓰고 있어 문제없었음)
