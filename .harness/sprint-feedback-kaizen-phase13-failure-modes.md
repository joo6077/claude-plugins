# Sprint Feedback
Feature: 카이젠 Phase 13 — bambu-kit 실측 실패 3종(L1 곡면 계단 / L2 스트링잉 / L3 바닥 박리) 인테이크 + 지원가능성 분기 + E3 금지 키 확장
Evaluated: 2026-08-14 11:21
Verdict: REJECT
Iteration: 1 (재평가 — 최초 판정은 글로벌 피드백 풀에 저장되지 않아 무효로 취급)

## 재평가 배경

이 계약은 이전에 한 번 판정을 받았고 `status: done` 이지만, 그 판정 아티팩트가
`~/.harness/feedback/evaluator/`에 저장되지 않았다 (오케스트레이터의 structured output
schema 강제로 피드백 저장 단계가 스킵됨). 이 재평가는 이전 판정을 승계하지 않고
**독립적으로 16개 조건 전부를 재실행 검증**했다.

## Contract Fingerprint
- path: `.harness/sprint-contract-kaizen-phase13-failure-modes.md`
- sha256(full): 09deb5099e63eef1286b67c3dc62d80991220bd96bbe296dfc4b7fc845ef7e59
- seal(conditions_digest): sha256:27d4a8c7b52f668d
- seal_status: **SEAL_OK** (recorded=27d4a8c7b52f668d, actual=27d4a8c7b52f668d)
- status: done (frontmatter, 재평가 전후 불변 확인)
- slug: kaizen-phase13-failure-modes
- contract_root: /Users/jackson/Hub/10_Dev/claude-plugins
- contract_root_unconfigured: false
- 선택 근거: 사용자가 명시적으로 지정한 계약 경로 (ladder 1 명시경로)
- 재확인(Step 5): 일치 (TOCTOU 없음)
- status_transition: skipped (verdict=REJECT · status 는 이미 done · REJECT 시 되돌리지 않음)

## 조건 수 계산
- frontmatter `conditions`: 16
- 실측 (`grep -cE '^- \[[ x]\] [A-Z]{2,}-[0-9]{2}'`): **16** — 일치

## Amendments
- amendments: 2
- narrowing: 1 (AM-02 — 조건 수 15→16 정정. 봉인 대상(체크박스 줄) 불변이라 SEAL_OK 유지. 판정에 흡수 — 조건 수 계산에 이미 반영됨)
- unknown: 1 (AM-01 — AP-03 clause 2 측정문 결함 자체 공개. direction=unknown, consent=unanchored → **PASS 근거로 사용 불가**. 아래 AP-03 판정은 이 사이드카에 기대지 않고 독립적으로 재실행하여 동일 결론(FAIL)에 도달했다)

## User Correction Audit
- correction_log_status: available (`~/.claude/logs/claude-plugins/2026-08.md`)
- 조사 범위: 계약 생성 시각(2026-08-13 18:27) 전후 프롬프트 블록 (18:00~19:49)
- 실제 사람 프롬프트: 18:00:32 `"ㄱㄱ"` (오케스트레이터 계속 트리거) 1건뿐. 나머지는 전부
  `<task-notification>` (서브에이전트 비동기 완료 알림) — 사람의 교정 지시 아님
- unreflected_corrections: 0
- verdict 영향: 없음 (표면화 전용)

## Results

### Skill (4/4)
- [x] SK-01: Phase 1.9 Failure-Mode Detector 신설 + Phase 2 게이트 — PASS
  - 근거: `bambu-kit/skills/bambu-print-profile/SKILL.md:475` `### Phase 1.9 — Failure-Mode Detector` 1건.
    `Failure-Mode Gate (Phase 2 진입 조건)` 1건(L2 확인). `SKILL.md:543` `Phase 1.9 completed (Failure-Mode Gate)`
    매치. `SKILL.md:517` `§3.8 User-Reported Failure Gate` 앵커가 1.9 절 내부에서 인용만 하고 재정의 안 함 (L3: 1.9.1~1.9.4 절 전체 Read, §3.8 은 "정본은 …다. 여기서 규칙을 다시 쓰지 말고" 로 인용 확인)
- [x] SK-02: Phase 3.0 Supportability Split — PASS
  - 근거: `SKILL.md:659` `#### Phase 3.0 — Supportability Split` 1건. 섹션 내 `notes only` 2건, `adaptive_layer_height` 2건 매치. `SKILL.md:719` `- ❌ \`adaptive_layer_height\`` 로 시작 확인 (L3: 표 전체 Read, L1 계단/L2 스트링잉/L3 박리 각 항목이 지원가능/불가능 명확히 분기됨을 확인)
- [x] SK-03: Phase 4.3 E3 게이트 금지 키 4종 실행 차단 — PASS
  - 근거: SKILL.md 마지막 python 히어독(4.3 게이트)을 추출해 실제 실행.
    clean.json → `RESULT: PASS` exit `0`. bad.json(금지 4키 포함) → `RESULT: FAIL` exit `1`,
    금지 키 FAIL 행 4건(adaptive_layer_height/bed_temperature/bed_temperature_initial_layer/elephant_foot_compensation).
    subonly.json(`bed_temperature_initial_layer`만) → 금지 키 FAIL 1건 (substring 비충돌 확인, `bed_temperature` 오탐 없음).
    음성 대조: FORBIDDEN dict를 빈 dict로 치환 후 재실행 → bad.json이 `RESULT: PASS` exit `0`으로 뒤집힘 확인 (직접 실행)
- [x] SK-04: L2 스트링잉 건조 우선 게이트 3단계 + 온도/fan 금지 유지 — PASS
  - 근거: `SKILL.md:730` `L2 스트링잉 게이트 예외` 1건. 표에 `filament_wipe`/`filament_retraction_length`/`coupon` 각 1건 매치.
    `온도를 자동 하향하지 마라` 1건(SKILL.md 내). `사용자 명시 요청 2026-05-16` 1건(기존 금지 보존 확인, L3: 온도/fan 미변경 규칙과 게이트 예외가 상충 없이 공존함을 표 전체 Read로 확인)

### Error (2/2)
- [x] ER-01: layer_height 0.08 근거 오귀속 정정 — PASS
  - 근거: `surface-recipes.md` `박스/도구` 잔존 0건, `1 차 권장` 1건, `미확인` 2건.
    `bambu-fields-baseline.md` `layer_height 0.08-0.12` 0건.
    `surface-recipes.md:107` 실제 행: "`0.12`: 0.12mm High Quality @BBL H2S.json (공식 체인 실재). **`0.08` 은 이 파일의 공식 근거가 아니다**...`[미확인]`" (L3 확인)
- [x] ER-02: enable_arc_fitting / resolution 성격 오귀속 정정 — PASS
  - 근거: SKILL.md `(원통 모델)` 잔존 0건, `G-code encoding` 2건.
    `surface-recipes.md` `Z 계단의 주 해결책이 아니다` 1건(`resolution` 행에 부착, L3 확인:
    `surface-recipes.md:116` "⚠️ **XY 세그먼트 해상도 전용** — Z 계단의 주 해결책이 아니다")

### Architecture (3/3)
- [x] AR-01: 변경이 정확히 4경로로 한정 — PASS
  - 근거: `git diff 04641f7^..04641f7 --name-only -- bambu-kit` 결과가 정확히
    `SKILL.md`, `references/bambu-fields-baseline.md`, `references/failure-recipes.md`,
    `references/surface-recipes.md` 4행과 일치 (측정 상태: 계약이 명시한 "커밋 직전 working tree" 를
    사후 재현하기 위해 구현 커밋 04641f7의 diff를 사용 — 이후 03669c7은 plugin.json 버전 bump로
    Scope 밖 항목이며 4경로에 포함되지 않음을 별도 확인)
- [x] AR-02: bambu-fields-baseline.md §10 L1/L2/L3+금지 키 전수 백틱 존재 — PASS
  - 근거: §AR-02 스니펫 실행 결과 `EXPECT=27 MISSING=0`. `## 10. 실측 실패 모드 관련 필드` 헤더 1건.
    섹션 순서 `## 9. 미해결 / 검증 필요` → `## 10. 실측 실패 모드 관련 필드` 확인 (tail -2)
- [x] AR-03: failure-recipes.md 신설 + 3곳 참조 — PASS
  - 근거: `test -f` exit 0. 파일 트리 `SKILL.md:38` `├── failure-recipes.md`.
    frontmatter description `references/ 8종` 존재, `references/ 7종` 잔존 0건.
    Phase 3 도입부(`SKILL.md:567`) `references/failure-recipes.md 도 로드한다` (L3: "### Phase 3 — 프로파일 JSON 생성" 절 바로 다음 줄에서 확인)

### Anti-patterns (1/2) — **1건 FAIL**
- [x] AP-01: 신규 URL 전부 evidence 파일 또는 변경 전 트리에 실재 — PASS
  - 근거: §AP-01 스니펫 실행 결과 `UNSOURCED_URL=0` (구현 커밋 04641f7 diff 기준, 현재 clean 상태에서도 0).
    신규 토큰 `0.07`(evidence 2건), `0.8`(2건), `auto_brim`(2건), `Spiral`(1건) 전부 evidence 파일에 매치
- [ ] AP-03: bare code fence 신규 미도입 — **FAIL**
  - 근거: 3개 측정 clause 중 clause 1·3은 충족하나 clause 2가 불충족.
    - clause 1: `python3 scripts/validate-plugin.py bambu-kit` → `V6 code-fence 0 bare — OK`, exit `0` (충족)
    - clause 2: `git diff -U0 -- bambu-kit \| grep -c "^+\`\`\`$"` — **상태 전제 미명시**로 평가자가
      상태를 선택함 (AR-01의 "Given: 커밋 직전 working tree" 관례를 형제 조건에 동일 적용, 측정 상태:
      `git diff 04641f7^..04641f7 -- bambu-kit`). 현재 clean 워킹트리로 문자 그대로 돌리면 값이
      trivial `0`이 되지만 이는 실제 변경분을 전혀 검사하지 않는 **공허한 0**(증거 유효성 검사 2:
      활성화 실패)이므로 채택하지 않았다. 구현 diff 대상 측정값 = **`5`** (기대 `0`) — bash·zsh 양쪽
      동일 실행 확인. 여는 fence 5개 전부 언어 힌트 보유(`^+\`\`\`[a-z]` → 5건)이며 닫는 bare fence
      5개는 정상적으로 짝을 이루는 코드블록 종료다. 즉 clause 2는 "신규 fenced 코드블록을 하나라도
      추가하면 구조적으로 0이 될 수 없는" 측정 설계 결함이며, 언어 힌트 유무와 무관하게 항상 위반으로
      잡힌다.
    - clause 3: `failure-recipes.md`의 `^```$` 개수(1) == 언어힌트 여는 fence 개수(1) — 충족
    - **문자 그대로 판정**: 조건 프로즈("측정: A · B · C")는 3개 clause 전부 충족을 요구하므로,
      clause 2 불충족은 조건 전체 FAIL이다. 계약 봉인이 잠긴 채 조건 문구를 고칠 권한이 없으므로
      계약대로 채점한다.
    - amendment 사이드카(AM-01)가 이 결함을 이미 자기 공개했으나 direction=`unknown`이라 PASS 근거로
      쓸 수 없다는 점을 확인 후, 독립적으로 동일 결론(FAIL)에 도달함
  - 수정 방향: contract-design-guide의 조건 작성 preflight에 "bare-fence 카운트는 여는 fence만
    세라(`^+\`\`\`[a-z]` 형태로 언어힌트 유무 판정, 닫는 fence는 항상 bare이므로 카운트 대상에서
    제외)"를 예시로 승격 권장. 다음 사이클 Phase 2/4 소관

### Reusability (2/2)
- [x] RE-01: 신규 파일 정확히 1개, 신규 디렉토리 0개 — PASS
  - 근거: `git diff --name-status 04641f7^..04641f7 -- bambu-kit` 에서 상태 `A`(added) 파일이
    정확히 1건 = `bambu-kit/skills/bambu-print-profile/references/failure-recipes.md`.
    신규 파일이 기존 `references/` 디렉토리 안에 생성되어 신규 디렉토리 0건
    (측정 상태: AP-03과 동일하게 "커밋 직전" 상태를 구현 diff로 재현. 현재 워킹트리 기준 문자 그대로의
    `git status --porcelain | grep -c '^??'`는 이미 커밋되어 0이 되는 vacuous 값이므로 채택 안 함)
- [x] RE-02: failure-recipes.md가 새 설정 키를 발명하지 않음 — PASS
  - 근거: §RE-02 스니펫 실행 결과 `SIBLINGS=7 KEYS=28 MISSING=0`, exit `0`.
    음성 대조: 존재하지 않는 키 `` `zzz_fake_key` `` 를 failure-recipes.md에 추가 후 재실행 →
    `MISSING=1  MISSING zzz_fake_key` 확인 후 원본으로 복구 (git status clean 재확인)

### Diagnostics (3/3)
- [x] DG-01: validate-plugin.py bambu-kit V1~V8 전부 OK, exit 0 — PASS
  - 근거: 직접 실행 결과 `V1~V8` 전부 OK, `Total: 1 plugins, 1 OK`, `Exit: 0`
- [x] DG-02: 모든 grep/git/python 오라클 zsh·bash 동일 출력 — PASS
  - 근거: SK-01~04·ER-01~02·AR-01·AR-03·AP-03(clause2)·DG-01 등 대표 오라클 셋 + AR-02/RE-02/DG-03/SK-03
    게이트(python 히어독 기반)를 bash와 zsh 양쪽에서 각각 실행, `diff` 결과 무차이(IDENTICAL) 확인
    (본 계약의 모든 오라클이 grep -c/-n, git status/diff, python heredoc 패턴이며 unquoted glob을
    쓰지 않아 zsh nomatch 위험 없음을 코드 리뷰로도 확인)
- [x] DG-03: SKILL.md 임베드 python 히어독 전부 ast.parse 통과 — PASS
  - 근거: 정규식으로 히어독 3개 블록 추출, `ast.parse` 전부 통과, SyntaxError 0건

## Unverifiable Summary
- 총 미검증 건수: 0
- 건 목록: 없음 (전 16조건 직접 실행/의미 추적으로 판정, 도구·환경 부재 없음)
- Verdict 영향: 해당 없음

## Evidence Validity
- 검사 대상 증거: 16건 (조건별 1개씩)
- 무효 판정: 0건
- 셸 스니펫 실행 검증: 실행 16건 · zsh/bash 양쪽 확인 대표 셋(SK-01~04/ER-01~02/AR-01/AR-03/AR-02/RE-02/DG-03/SK-03/AP-03) IDENTICAL · 미실행 0건
- 비고: AP-03/RE-01/AP-01은 "상태 전제 미명시" 조건이라 Given 상태를 명시적으로 선택·기록함
  (구현 커밋 04641f7 diff). 현재 워킹트리(이미 커밋됨)를 문자 그대로 쓰면 diff가 비어 vacuous
  pass가 되므로 그 값은 채택하지 않았다 — 이 판단이 AP-03의 실제 FAIL을 드러냈다

## Summary
- Total: 15/16 conditions passed
- Verdict: **REJECT**
- FAIL 항목: AP-03 (bare code fence 신규 미도입) — clause 2 측정문이 여는/닫는 fence를 구분하지
  않아 언어 힌트가 정상 부착된 신규 코드블록을 추가하기만 해도 항상 위반으로 잡히는 구조적 결함.
  실제 코드 품질(V6 0 bare, 신규 파일 fence 정합)은 문제없으나, 계약 문구를 문자 그대로 적용하면
  조건 불충족. 수정 우선순위: 계약 봉인 상태이므로 이 계약 자체는 고칠 수 없다 —
  contract-design-guide 프리플라이트에 이 패턴을 반면교사로 등재하는 것이 유일한 개선 경로

## Improvement Suggestions
- [AP-03] 측정-방식-불일치 — clause 2를 `git diff -U0 ... | grep -cE '^\+\`\`\`[a-zA-Z]'`(여는 fence만,
  언어힌트 유무로 판정)로 교체하고, 닫는 bare fence 카운트는 별도 clause로 "여는 fence 수와 일치하는지"
  대조하는 방식(AR-03의 clause 3와 동일 패턴)으로 대체할 것을 다음 계약 작성 시 권장
- [AR-01/AP-01/AP-03/RE-01] 범위-상태-모호 — "이번 변경"을 재는 git status/diff 기반 clause들은
  일부만 명시적으로 "Given: 커밋 직전 working tree"를 달고(AR-01) 나머지는 암묵적으로 같은 전제를
  기대한다. 사후 재평가 시 매번 상태를 추론해야 하므로, 계약 조건 작성 preflight에 "git 상태 의존
  측정문은 조건 단위가 아니라 계약 헤더 레벨에서 공통 Given을 1회 선언"하는 패턴을 권장
