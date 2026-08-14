# Sprint Feedback
Feature: 카이젠 Phase 6 — design-kit Variant Distinctiveness Gate(E1) + Decision Propagation Manifest(E2) + 증거 채널 구분(E3) + WCAG 터치타겟 사실 정정
Evaluated: 2026-08-14 11:10
Verdict: REJECT
Iteration: 1 (재평가 — 원 판정은 글로벌 피드백 풀에 저장되지 않아 무효. 이 평가는 원 판정을 승계하지 않고 독립적으로 재수행했다)

## Contract Fingerprint
- path: /Users/jackson/Hub/10_Dev/claude-plugins/.harness/sprint-contract-kaizen-phase6-variant-decision-gates.md
- sha256(conditions_digest, frontmatter): sha256:a2dc871865f09e39
- verify_seal 재계산: SEAL_OK (recorded == actual)
- status: done (frontmatter 명시값 — REJECT 로 되돌리지 않음, 오케스트레이터 소관)
- slug: kaizen-phase6-variant-decision-gates
- contract_root: /Users/jackson/Hub/10_Dev/claude-plugins
- contract_root_unconfigured: false
- 선택 근거: ladder 1 (명시 경로 — 재평가 태스크가 계약 파일을 직접 지정)
- legacy_contract_used: false
- 재확인(Step 5): 일치 (평가 종료 시 sha256/status 재확인 — 아래 참조)
- status_transition: skipped (verdict=REJECT — status 는 done 유지, 되돌리지 않음. 지시사항에 따름)
- 구현 커밋: 965af48 (Phase 6 본체) + 450e553 (design-kit/README.md sync-docs, DG-04 가 예견한 후속 조치 — Final 소관, 범위 밖이라 미평가 대상)

## Amendments
- amendments: 0 (`.harness/sprint-amendments-kaizen-phase6-*.md` 사이드카 부재 확인)

## User Correction Audit
- correction_log_status: available (`~/.claude/logs/claude-plugins/2026-08.md` 존재)
- unreflected_corrections: 0 (스프린트 기간 내 phase6/design-kit 관련 사용자 교정 발화 미발견 — 스캔한 로그는 대부분 이번 재평가 세션 자체의 tool-call 기록)
- verdict 영향: 없음 (표면화 전용)

## Results

### Skill (12/12)
- [x] SK-01: §5 Variant Contract Matrix + 4 필드 신설 — PASS
  - 근거: `design-kit/references/visual-change-protocol.md:145` §5 헤더 존재. `variant_id`(3) `strategy_label`(3) `axis_vector`(5) `intended_user_scenario`(3) 각 grep -cF >=1 (§5 블록 145~251 정밀 경계 내 재확인 동일)
- [x] SK-02: pairwise 임계 판정식 — PASS
  - 근거: `design-kit/references/visual-change-protocol.md:225` `need = 2 if k >= 3 else 1` grep -cF 1
- [x] SK-03: §5 가 상한/부대산출물 금지를 인용만 — PASS
  - 근거: §5 블록 내 `harness/docs/guides/skill-design-guide.md`(1) · `§5.6`(4) 각 grep -cF >=1 (`:154`, `:171` 등)
- [x] SK-04: §6 신설 + 스키마 키 6종 — PASS
  - 근거: `:252` §6 헤더. `decision_id`(6) `required_surfaces`(3) `excluded_surfaces`(2) `route_or_entry`(1) `viewport_or_container`(1) `assertions`(2, §6 블록 한정) 각 >=1
- [x] SK-05: coverage rule 4조 + "golden 만 있고" — PASS
  - 근거: `:310-320` 4개 번호 목록, `:314` "**golden 만 있고**" 리터럴 grep -cF 1
- [x] SK-06: §7 신설 + 채널 4종 — PASS
  - 근거: `:371` §7 헤더. `artifact_snapshot`(3) `dom_snapshot`(1) `browser_user_visible`(2) `device_user_visible`(1) 각 >=1
- [x] SK-07: §7 이 정본 2곳 참조만 — PASS
  - 근거: §7 블록 내 `harness/docs/guides/skill-design-guide.md`(1) `§3.8`(1) `harness/docs/guides/agent-design-guide.md`(1) `§10`(1) 각 >=1 (`:411`, `:413`)
- [x] SK-08: design-mockup 고정 개수 리터럴 제거 + 개수 계약 착지 — PASS
  - 근거: `design-kit/skills/design-mockup/SKILL.md` `grep -cF '시안 5개'` == 0. description 첫 줄(`:4`) "미지정 3 · 사용자 지정 N · 승인 상한 5" 포함. Step 3 블록(`:6`,`:11`) "상한"·"미지정" 각 1건 이상 포함
- [x] SK-09: 같은 파일이 §5 산출물을 이름으로 요구 — PASS
  - 근거: `Variant Contract Matrix` grep -cF 5
- [x] SK-10: design-test manifest 기반 테스트 생성 단계 신설 — PASS
  - 근거: `design-kit/skills/design-test/SKILL.md` `decisions.yaml`(3) >=1, `^### Step 5-b`(`:271`) grep -cE 정확히 1
- [x] SK-11: design-audit·design-reviewer 커버리지 판정 조항 — PASS
  - 근거: 두 파일 각각 `decisions.yaml` grep -cF 1
- [x] SK-12: design-concept Gotcha 6 이 §5 게이트 참조 — PASS
  - 근거: `design-kit/skills/design-concept/SKILL.md:53` Gotcha 6 본문에 `§5 Variant Contract Matrix` 리터럴 포함 (Gotcha 번호 목록 직접 확인)

### Error (3/3, goal — 직접 실행 검증)
- [x] ER-01: §5 게이트가 실측 REJECT UI-04 를 FAIL 로 잡는다 — PASS
  - 근거: §5 python 블록을 파일로 추출해 `printf 'B3\t...B6\t...'`(4축 전부 동일) 입력 실행 →
    `FAIL B3 vs B6: hamming=0 < 2` + `violations=1` + exit=1 (계약 명시 출력과 문자 그대로 일치).
    음성 대조: B6 의 축 값 2개를 다르게 바꾼 입력 → `violations=0` + exit=0 확인 (zsh·bash 양쪽 동일, DG-02 겸용)
- [x] ER-02: §6 게이트가 "골든만 존재"를 FAIL 로 잡는다 — PASS
  - 근거: §6 python 블록 추출 후 golden 있고 `assertions: []` fixture 실행 →
    `FAIL .../dashboard.desktop.main: golden 만 존재 — visible/count/height assertion 부재` + exit=1.
    음성 대조: 같은 fixture 에 `["main visible","group rows >= 1","container height > 0"]` 채움 → exit=0
- [x] ER-03: manifest 부재·결정 0건을 통과로 접지 않는다 — PASS
  - 근거: 존재하지 않는 경로 실행 → `NO_MANIFEST <path>` + exit=3. `decisions: []` fixture 실행 →
    `NO_DECISION 대상 0 건 — 검사 미수행` + exit=3. 두 경우 모두 exit 0 아님

### Architecture (2/3)
- [x] AR-01: 범위 안 문서에서 레벨 귀속 없는 `44` 터치타겟 줄 0건 — PASS
  - 근거: 8 SKILL.md + 1 agent + 2 references + 26 docs/design (총 37파일, `find`로 열거) 대상
    `grep -rnE '44' | grep -E '터치|타겟' | grep -vE 'AAA|Apple|HIG|2\.5\.5|iOS|Enhanced|권장'` → 0줄
    (사전 측정 6줄과 대조되는 16개 매치 전부 귀속어 포함 확인). 음성 대조: `design-guide/SKILL.md:15`
    에서 귀속 낱말("AA","AAA","Apple","HIG" 일부)을 제거한 사본으로 같은 명령 재실행 → 1줄 검출
    (판별력 확인, 원본 파일은 미변경 — 스크래치 사본에서만 수행)
- [x] AR-02: 소비 표면 9쌍이 절 제목 토큰으로 참조 — PASS
  - 근거: design-mockup(§5×1=4건·§7×1=2건), design-concept(§5×1=2건), design-test(§6×1=2건·§7×1=2건),
    design-audit(§6×1=2건·§7×1=2건), design-reviewer(§6×1=1건·§7×1=1건) — 9쌍 전부 grep -cF >=1
- [ ] AR-03: §6이 특정 도구를 표준으로 강제하지 않음을 명시 — **FAIL**
  - 근거: `표준으로 강제하지 않는다` 는 `visual-change-protocol.md:272` 1곳에만 존재한다. 그 문장이
    속한 문단(:272-273, "도구 중립 — design-kit 은 위 4 종 중 어느 하나도 표준으로 강제하지
    않는다...")은 `Playwright`·`Chromatic`·`Percy`·`BackstopJS` 4개 도구명을 **literal 로 포함하지
    않는다** — "위 4 종"이라는 역참조만 쓴다. 도구명 4종은 그 앞의 **다른 문단**(:263-270, 빈 줄
    :271 로 단락 분리)에 나열돼 있다. python `re.split(r'\n\s*\n', text)` 로 문단을 정밀 분리해
    "표준으로 강제하지 않는다"가 속한 문단 전체를 추출한 뒤 4개 토큰 포함 여부를 확인한 결과
    Playwright=False, Chromatic=False, Percy=False, BackstopJS=False — 계약 원문의 "같은 문단에
    열거" 요건을 문자 그대로 충족하지 못한다.
  - 수정: 두 문단을 병합하거나(빈 줄 :271 제거), "표준으로 강제하지 않는다" 문장이 있는 문단에
    4개 도구명을 다시 나열한다. 예: "**도구 중립 — Playwright·Chromatic·Percy·BackstopJS 중
    어느 하나도 표준으로 강제하지 않는다.**"로 교체

### Anti-patterns (2/2)
- [x] AP-03: bare code fence 없음 — PASS
  - 근거: `python3 scripts/validate-plugin.py design-kit` → `V6 code-fence 0 bare — OK` (실행 확인)
- [x] AP-04: frontmatter name 필드 보존 — PASS
  - 근거: 같은 실행 `V1 frontmatter 8 skills + 1 agent — OK`

### Reusability (1/1)
- [x] RE-01: §6 스키마가 1파일에만 존재 — PASS
  - 근거: `grep -rl 'required_surfaces:' design-kit/ | wc -l` == 1, 해당 파일이
    `design-kit/references/visual-change-protocol.md` 와 일치

### Diagnostics (4/4)
- [x] DG-01: validate-plugin.py design-kit exit 0 · `1 plugins, 1 OK` — PASS
  - 근거: 구현 커밋(965af48) 상태의 별도 git worktree에서 직접 실행 확인 (`design-kit` v0.3.0,
    exit 0, "Total: 1 plugins, 1 OK")
- [x] DG-02: §5·§6 스니펫 zsh·bash 동일 출력 — PASS
  - 근거: ER-01/ER-02 측정 명령을 zsh(기본 셸)와 `bash -c` 양쪽에서 각각 실행해 stdout 저장 후
    `diff` 무출력 확인
- [x] DG-03: 커밋에 scope 밖 경로 0건 — PASS
  - 근거: `git show --name-only --format= 965af48` 결과 13개 파일 전부
    `design-kit/skills/*/SKILL.md` · `design-kit/agents/` · `design-kit/references/` ·
    `design-kit/docs/design/` · `.harness/sprint-contract-kaizen-phase6-` 접두 중 하나로만 구성
    (참고: 후속 `450e553`은 `design-kit/README.md` 1건만 수정 — 계약이 명시적으로 "수정 금지
    (읽기만) · Final 소관"으로 지정한 파일이며 DG-04가 그 드리프트를 예견·측정하는 구조이므로
    phase6 자체의 scope 위반으로 보지 않음)
- [x] DG-04: README 드리프트 정확히 1건 + 신고 — PASS
  - 근거: 구현 직전 상태(965af48^, 별도 worktree)에서 `sync-docs.py design-kit --check-only` →
    "design-kit/README.md: 동기화됨". 구현 직후(965af48) 같은 명령 → "design-kit/README.md: 변경
    필요" (정확히 1건, 다른 파일 0건)

## Unverifiable Summary
- 총 미검증 건수: 0
- Verdict 영향: 해당 없음 (미검증 0건)

## Evidence Validity
- 검사 대상 증거: 25건 (조건별 1건씩)
- 무효 판정: 0건
- 셸 스니펫 실행 검증: 실행 2건(ER-01, ER-02 게이트 스크립트) · zsh/bash 양쪽 확인 2건 · 미실행 0건
- 무효 0건 → 미검증 카운터 영향 없음

## Summary
- Total: 24/25 conditions passed
- Verdict: **REJECT**
- FAIL 1건: AR-03 — §6의 "표준으로 강제하지 않는다" 서술이 도구 4종(Playwright/Chromatic/Percy/
  BackstopJS) 명시와 같은 문단에 있지 않고 인접한 이전 문단에서 "위 4 종"으로만 역참조된다.
  계약이 `[exact]` 태그로 "같은 문단에 열거"를 명시적으로 요구했고, 실측(python 문단 분리) 결과
  이를 충족하지 못했다. 문장 병합 또는 도구명 재나열로 1줄 수정하면 해소되는 경미한 결함이나,
  계약 문자 그대로 판정 원칙상 FAIL 이다.

## Improvement Suggestions
- [AR-03] 측정-구조-불일치 — "같은 문단에 열거"라는 구조적 요건을 도구명이 실제 정의된 문단과
  분리된 곳에 배치. 계약 작성 시 "같은 문단 또는 인접 3줄 이내"처럼 여유를 두거나, 구현 시
  대상 문장 자체에 도구명을 재나열하는 것이 정합적. 재발 시 계약 표현을 "인접 인용 허용"으로
  완화할지, 구현 규율(항상 같은 문단에 재나열)을 강제할지 다음 iteration에서 확정 권고.

## 재평가 배경 메모 (오케스트레이터 문맥)
이 계약은 이미 `status: done` 이며 원래 APPROVE 로 처리되었으나, 그 판정의 아티팩트가
`~/.harness/feedback/evaluator/`에 저장되지 않아(structured output schema 강제로 인한 조기 종료)
이번 재평가를 독립적으로 재수행했다. 원 판정을 승계하지 않고 25개 조건 전부를 처음부터 직접
실행 검증한 결과 **AR-03에서 실제 결함을 발견**했다 — 이는 "이미 APPROVE 였으니 APPROVE"가
고무도장이었을 위험을 뒷받침한다. `status`는 지시에 따라 되돌리지 않는다(오케스트레이터 소관).
