# Sprint Feedback
Feature: harness 코어 결함 3건 — 태그 되먹임 · RE/DG 정본 정합 · markdown 킷 오라클
Evaluated: 2026-09-06 12:15
Verdict: REJECT
Iteration: 1

## Contract Fingerprint
- path: .harness/sprint-contract-harness-core-defects.md
- sha256: eb155fd65beba7dc2db74fd7b45ca3a455057d513c1c0e6c2b5168767e4a2ec7
- status: active
- slug: harness-core-defects
- contract_root: /Users/jackson/Hub/10_Dev/claude-plugins
- contract_root_unconfigured: false
- 선택 근거: ladder 1 (명시경로 — 사용자가 계약 경로를 직접 지정)
- legacy_contract_used: false
- seal_status: SEAL_OK (recorded=459a7c625948ffcb == actual=459a7c625948ffcb)
- contract_seal_broken: n/a
- 재확인(Step 5): 일치 (평가 시작·종료 시점 sha256/status 동일, TOCTOU 없음)
- status_transition: skipped (verdict=REJECT status=active — 재평가를 위해 active 유지)

## 환경 사실 — 워킹트리 상태
`git status --porcelain` 는 clean 이다. 사용자 지시("아직 커밋하지 않았다")와 실측이 어긋난다.
조사 결과: 이 스프린트의 구현 6 파일이 **동시 편집 세션의 커밋(`e73429fab3ef`, "fix(docs): 죽은
외부 링크 40건 교정 + 외부 링크 검사기")에 편승되어 함께 커밋됐다.** 두 세션이 같은 워킹트리에서
거의 동시에 `git add -A && git commit` 을 실행해 한쪽 커밋이 양쪽 변경분을 함께 묶은 것으로 보인다.

**귀속 판정 방법 (요청받은 대로):**
- `git show --stat e73429f` 로 파일 목록을 뽑아, 죽은 링크 교정 세션의 산출물(design-kit/docs,
  docs/*.html, bambu-kit/references 등 40여 파일 — 전부 URL 텍스트 치환)과 harness 6 파일을 대조
- harness 6 파일 각각을 `git show e73429f -- <file>` 로 개별 diff 확인 — **6 파일 모두 URL/링크
  텍스트가 섞여 있지 않고, 순수하게 태그 어휘 통합·N/A 규약·리터럴 환경값 금지 내용뿐**임을 확인
- 파일 mtime(`stat -f %Sm`) 대조: 계약 lock 11:41:56 → contract-schema.md 11:42:37 →
  나머지 5 파일 11:43:06~11:43:42 (lock 이후, 정상 순서) → 커밋 11:49:05
- 결론: `e73429fab3ef^`(=`f2e1b34`, 릴리스 커밋)를 이 스프린트의 **사전 baseline** 으로 채택.
  `git diff --name-only f2e1b34 HEAD -- harness/` 로 AR-03/SC-03 을 재구성 측정했다.

## Amendments
- amendments: 0 (사이드카 파일 없음)

## User Correction Audit
- correction_log_status: available (`~/.claude/logs/claude-plugins/2026-09.md`)
- unreflected_corrections: 0 — 소유 세션(`44c7700e-…`)의 스프린트 기간 프롬프트는
  "다한번에 진행해 차례대로 결함부터 잡고" (11:29:17) 1 건뿐이며 계약·구현에 반영됨.
  같은 시각대 다른 세션 프롬프트(`5ba706e1-…` "남은거 다 해결해" 등)는 병렬 세션(위 죽은 링크
  교정)의 것으로 이 스프린트 범위 밖
- verdict 영향: 없음 (표면화 전용)

## Results

### Skill (4/4)
- [x] SK-01: 통합 결함 태그 어휘 10종 등재 — PASS
  - 근거: `harness/references/contract-schema.md:704-715` 표에 10종 전부 존재. `grep -c` 결과
    (측정값, 기준 >=1 각각): 측정-수단-부재=1, 측정-방식-불일치=1, 측정-환경-오염=1,
    측정-산출물-부재=1, 검증경로-미기재=1, 측정-중복=2, 측정-상태-모호=2, 태그-산출물-불일치=1,
    범위-미명시=1, 증거-경로-부재=1 — 전부 충족 [L3, exact/enumerated]
- [x] SK-02: 표의 모든 행이 평가자/작성자 두 열을 채운다 — PASS
  - 근거: `contract-schema.md:704-715` 10개 행 파싱, 빈 칸 수 == 0 (awk 로 각 행 3 컬럼 확인,
    전부 비어있지 않음) [L3, exact/enumerated]
- [x] SK-03: SKILL.md 가 SSOT 를 참조 + 평가자 전용 4종에 작성 자문 존재 — PASS
  - 근거: `harness/skills/sprint-contract/SKILL.md:431-434` 가 `contract-schema.md` §조건 작성
    preflight 를 SSOT 로 명시 참조 (grep -c "contract-schema.md" = 11). 4종
    (측정-상태-모호·태그-산출물-불일치·범위-미명시·증거-경로-부재) 모두 SSOT 표에서 작성 측
    열 보유 확인(SK-02 근거와 동일 표) [L3, exact/enumerated]
- [x] SK-04: 리터럴 환경값 금지 규칙 신설 — PASS
  - 근거: `harness/docs/guides/contract-design-guide.md:602-618` "**(3) 리터럴 환경값 금지**"
    신설, `grep -c "리터럴 환경값"` = 1 (baseline 0). 금지 대상 표 + `Given:` 대체 예시 포함 [L3, structural]

### Script (3/4)
- [x] SC-01: RE-01/RE-02 자동 포함 블록 문자 단위 일치 — PASS
  - 근거: `diff <(sed -n '508,509p' SKILL.md) <(sed -n '734,735p' contract-schema.md)` → IDENTICAL
    [L3, exact/enumerated]
- [x] SC-02: DG-01~04 자동 포함 블록 문자 단위 일치 — PASS
  - 근거: `diff <(sed -n '512,515p' SKILL.md) <(sed -n '742,745p' contract-schema.md)` → IDENTICAL
    [L3, exact/enumerated]
- [x] SC-03: 정당한 예시 9건 보존 — PASS
  - 근거: (1) `git diff --name-only f2e1b34 HEAD -- harness/evals/test-fixtures/` → 빈 출력
    (fixture 5개 DG-01 라인 미변경 확인, `grep -n DG-01 harness/evals/test-fixtures/fixture-*/contract.md`
    로 5건 실재 확인) (2) `contract-schema.md` 의 aggregation 예시(라인 450-451, RE-01/RE-02)는
    diff hunk 범위(692-745) 밖이라 미변경 확인 (3) `contract-design-guide.md` 의 금지/허용 예시
    (라인 526/535 부근)는 diff hunk(599-618) 밖이라 미변경 확인 (4) `grep -c` 로 3개 특정 문자열
    각각 1건 매칭 확인: "RE-01: References 에 g1"=1(schema.md), "DG-04: 런타임 에러가 없다"=1
    (design-guide.md), "DG-04: 앱 구동 시 console"=1(design-guide.md) — 9건 전부 보존 확인
    [L3, exact/enumerated]
- [x] SC-04: validate-plugin.py harness exit 0 — PASS
  - 근거: 직접 실행 `python3 scripts/validate-plugin.py harness` → "Total: 1 plugins, 1 OK /
    Exit: 0". `echo $?` == 0 [L3, goal]

### Error (2/2)
- [x] ER-01: N/A 와 [미검증] 구분 문단 + 동의어 금지와 양립 — PASS
  - 근거: `qa-evaluation-guide.md:1015-1027` 같은 항목(item 1) 안에 "동의어를 만들지 않는다"
    문장(1015) 과 "N/A(사유)는 이 금지의 예외" 경고(1018) + 구분 표(1021-1024) + 구별 기준
    한 줄(1026)이 공존. 충돌 없이 양립 확인 [L3, structural]
- [x] ER-02: commands.analyze 미적용 프로젝트의 DG-01/DG-02 처리 명시 — PASS
  - 근거: `qa-evaluation-guide.md:1029-1038` item 2 전체가 이 분기를 다룸.
    `N/A (commands.analyze 미설정 …)` / `N/A (IDE diagnostics 미적용 확장자: …)` 형식 사용 확인
    [L3, structural]

### Architecture (3/3)
- [x] AR-01: commands.lint 가 DG 조건과 연결 문서화 — PASS
  - 근거: `harness/README.md:97` `commands.lint` 행에 "DG-01" 문자열 포함
    (`grep -n commands.lint harness/README.md` 결과 인용) [L3, exact]
- [x] AR-02: 통합 표가 정확히 1개 파일에만 존재 — PASS
  - 근거: 레포 전체에서 `grep -rln "| 태그 | 평가자"` → `harness/references/contract-schema.md`
    1건만 매칭. `qa-evaluator.md:812` 는 10종 태그명을 모두 나열하지만 **표 구조(2열)가 아니라
    improvement 템플릿의 플랫 리스트**이며 SSOT 경로를 명시 참조 — "표 복제" 로 카운트하지 않음
    (표 복제와 태그명 언급을 구분해서 잼). `contract-design-guide.md:1084` 는 옛 6종만 언급하며
    "여기서 표를 복제하지 않는다"고 명시 — 참조 규약 준수. 단, 이 6종 언급은 통합 후 갱신되지
    않은 잔존 서술(개선 제안 참조) [L3, exact/enumerated]
- [x] AR-03: 변경 범위 6개 이내 + evals 0건 — PASS (재구성 diff 로 측정)
  - 근거: Given 절("계약 봉인 후 구현 완료 시점, 아직 커밋하지 않은 상태")과 실제 상태(커밋됨)가
    불일치. 위 "환경 사실" 절의 방법대로 `git diff --name-only f2e1b34 HEAD -- harness/` 재구성
    측정 → 정확히 6개 파일(harness/README.md, harness/agents/qa-evaluator.md,
    harness/docs/guides/contract-design-guide.md, harness/docs/guides/qa-evaluation-guide.md,
    harness/references/contract-schema.md, harness/skills/sprint-contract/SKILL.md), `-- harness/evals/`
    diff 0건. **측정값: 6 (기준: <=6), evals=0 (기준: ==0)** — 경계값 정확히 충족.
    **PASS로 판정하되 측정-상태-모호 계약 결함으로 기록** (아래 Improvement 참조) [L3, exact/enumerated]

### Anti-patterns (3/3)
- [x] AP-01: 버전 하드코딩 없음 — PASS
  - 근거: 6개 변경 파일 전체 `grep -niE "hardcoded.*version"` → 0건. `validate-plugin` V7도
    "v0.7.0 matches marketplace — OK" [L3]
- [x] AP-03: bare code fence 없음 — PASS
  - 근거: `validate-plugin.py harness` 출력 "V6 code-fence 0 bare — OK" [L3]
- [x] AP-04: frontmatter name 필드 누락 없음 — PASS
  - 근거: `validate-plugin.py harness` 출력 "V1 frontmatter 9 skills + 1 agent — OK" [L3]

### Reusability (2/2)
- [x] RE-01: private 화 없음 — PASS
  - 근거: 이번 변경은 문서 통합(SSOT 로 집중)이며 새 private 컴포넌트를 만들지 않음. 6개 diff
    전수 검토로 확인 [L3]
- [x] RE-02: 기존 컴포넌트 재사용 — PASS
  - 근거: 기존 6항 preflight 표(`contract-schema.md`)를 새로 만들지 않고 확장해 10항으로
    통합(AR-02 근거와 동일 diff) [L3]

### Diagnostics (2/4, 1 FAIL, 1 미검증:ENV)
- [x] DG-01: bash -n scripts/release.sh 워닝 0개 — PASS
  - 근거: 직접 실행, exit 0, stderr 없음 [L3]
- [ ] DG-02: IDE diagnostics 워닝/인포 0개 — **[미검증:ENV]**
  - 1차 도구 시도: 이 평가 컨텍스트에는 IDE Problems 패널 관찰 도구가 없음
    (`project.yaml.runtime_inspection.mcp_server: null` 확인)
  - fallback 시도: `npx --no-install markdownlint-cli2 <6개 파일>` 실행 — 결과 수십~수백 건의
    MD013/MD031/MD032 위반이 **레포 전역 기존 컨텐츠에 산재**(이번 diff 라인이 아닌 부분에도 다수)
    했고, 레포에 `.markdownlint*` 설정 파일이 없어(`find . -iname ".markdownlint*"` 0건) 이
    프로젝트가 채택한 컨벤션이 아님을 확인 — 유효한 대체 오라클이 아니라 판단, 증거로 채택하지 않음
  - 실패 로그: 위 markdownlint-cli2 실행 원출력 인용 (다수 MD013 line-length 등)
  - 통제 불가 사유: IDE 확장 프로그램 기반 진단은 정적 셸 도구로 재현 불가능하고 이 레포엔 확립된
    markdown lint 컨벤션이 없음. 재검증 명령: 사용자가 VS Code 등에서 6개 파일을 열어 Problems
    패널 직접 확인, 또는 프로젝트가 `.markdownlint.json` 을 채택한 뒤
    `npx markdownlint-cli2 harness/README.md harness/agents/qa-evaluator.md
    harness/docs/guides/contract-design-guide.md harness/docs/guides/qa-evaluation-guide.md
    harness/references/contract-schema.md harness/skills/sprint-contract/SKILL.md` 재실행
- [x] DG-03: release.sh 콘솔 로그 에러/예외 0개 — PASS
  - 근거: `bash scripts/release.sh 2>&1 || true` 실행, `grep -icE "error|exception|traceback|fatal"`
    == 0. 출력은 사용법 안내뿐 [L3]
- [ ] DG-04: 변경한 문서 규약대로 계약 1건 작성 + Step 6.5 게이트 0위반 — **FAIL**
  - 근거: Step 6.5 게이트 자체(`harness/skills/sprint-contract/SKILL.md:607-626`)는 이 스프린트로
    변경되지 않은 기존 인프라다. "변경한 문서 규약"(N/A(사유) 형식·리터럴 환경값 금지)을 **실제로
    적용해 새로 작성된 계약**이 있는지 전수 조사했으나 발견하지 못했다.
    - 후보 1: `.harness/sprint-contract-bambu-kit-enum-allowlist-gate.md` — locked_at 11:34,
      6개 harness 파일 수정(11:42:37~11:43:42) **이전**에 이미 잠김. 새 컨벤션을 반영할 수 없는
      시점 → 배제
    - 후보 2: `.harness/sprint-contract-harness-core-defects.md`(이 계약 자신) — locked_at 11:41:56,
      역시 `contract-schema.md` preflight 표 갱신(11:42:37)보다 **1분 먼저** 잠김(mtime 비교로 확인,
      `stat -f %Sm` 인용) → 이 계약도 새 컨벤션을 참조해 작성될 수 없었음. 또한 이 계약은 모든
      카테고리에 조건이 있어 N/A(사유) 형식을 전혀 행사하지 않음 → 배제
    - 후보 3: `.harness/sprint-contract-docs-quality-gates.md`(11:50:45 작성, 유일하게 구현 이후
      생성된 계약) — 완전히 무관한 주제(docs 품질 게이트)이고 `status: review` + `retroactive: true`
      로 표준 Step 6 워크플로우를 명시적으로 우회했으며 `conditions_digest`/`locked_at` 이 없어
      Step 6.6 봉인도 거치지 않음. N/A 마커 미사용, 리터럴 환경값 회피 의도 서술 없음 → 이 스프린트의
      새 컨벤션을 검증하는 산출물로 인정 불가
    - `find . -type f -newermt "2026-09-06 11:43:42"` 로 구현 이후 생성된 전체 파일을 추가로 스캔
      했으나 다른 후보 없음
  - 실행 주장 조건(Rule 9)이며 산출물이 없으므로 도구·환경 부재가 아니라 **미실행**으로 판정.
    FAIL

## Unverifiable Summary
- invalid_evidence: 0
- env_gaps: 1  [DG-02, ENV, 4요건 충족 — 위 근거 참조]
- verified_coverage: (22 - 1) / 22 = 0.95  (임계 0.60 충족 — 커버리지 게이트 무관)
- 연속 ENV 승급: 없음 (iteration 1, 비교 대상 없음)
- Verdict 영향: 통상 (env_gaps 1건은 REJECT 사유가 아님. FAIL 1건(DG-04)이 REJECT 사유)

## Discrimination
- 적용 조건: 없음 — 이 스프린트의 22개 조건 중 동시성 가드·인증·멱등성·입력검증·데이터유실·
  마이그레이션·재시도/중복제거·보안경계·사용자보고충돌 9항목에 해당하는 조건이 없음 (문서/스키마
  정합성 스프린트)

## Evidence Validity
- 검사 대상 증거: 21건 (FAIL 1건 DG-04, ENV 1건 DG-02 제외 나머지 20건 PASS 근거 + 재구성 diff 1건)
- 무효 판정: 0건
- 셸 스니펫 실행 검증: 이 계약에는 사용자가 실행할 셸 스니펫 산출물이 없음 (해당 없음)
- 무효 0건 — 미검증 카운터(현재 누계 env_gaps=1)에 추가 합산 없음

## Summary
- Total: 20/22 conditions passed (FAIL 1: DG-04, ENV 1: DG-02)
- Verdict: REJECT
- REJECT 사유: DG-04 미충족 — "변경한 문서 규약대로 계약을 1건 작성"하는 산출물이 존재하지 않음.
  구현자가 계약 조건 문구를 다룬 6개 문서 파일은 모두 정확·완전하게 수정했으나(SK-01~04, SC-01~04,
  ER-01~02, AR-01~02 전부 PASS), 그 새 컨벤션을 **실제로 적용해 새 계약을 작성**하고 Step 6.5
  게이트를 돌려 0위반을 증명하는 산출물이 이 스프린트 기간에 생성되지 않았다.
- 수정 우선순위: DG-04 하나만 해결하면 된다 — 새 계약(또는 기존 evals 픽스처에 추가하는 최소
  1개 조건 블록)을 이 스프린트가 도입한 컨벤션으로 작성하고(예: 빈 카테고리를 `N/A (사유)` 로
  기록하거나 환경의존 조건에 `Given:` 을 붙여 리터럴 환경값을 피하는 예시), Step 6.5의 3개 명령
  출력을 인용해 위반 0건임을 보여라.

## Improvement Suggestions
- [DG-04] 측정-산출물-부재 — 조건 문구가 "계약을 1건 작성"이라는 실행을 요구하면서 그 산출물을
  어디에 남겨야 하는지(파일 경로, 최소 조건 수, 어떤 신규 컨벤션을 반드시 행사해야 하는지)를
  명시하지 않았다. `DG-04: {harness/evals/test-fixtures/fixture-f 또는 신규 데모 계약 경로}에
  N/A(사유) 형식 1건 + Given: 절 1건을 포함한 계약을 작성하고, 그 경로에서 Step 6.5의 (1)(2)(3)
  명령 출력을 인용해 위반 0건임을 보인다` 형태로 구체화 권장
- [AR-03] 측정-상태-모호 — Given 절이 "아직 커밋하지 않은 상태"를 전제했지만 병렬 세션 환경에서는
  구현이 다른 작업과 함께 커밋될 수 있다. `Given: 계약 봉인 이후 커밋된 모든 변경분 기준, 계약
  locked_at 이후 첫 커밋(들)의 harness/ diff` 처럼 커밋 여부에 의존하지 않는 형태로 재작성 권장
- [AR-02] 범위-미명시 — "표"의 정의(2열 구조 vs 태그명 나열)가 명시되지 않아 qa-evaluator.md의
  플랫 리스트(10종 나열)를 표 복제로 볼지 판단이 갈릴 수 있었다. "표(2열 이상 구조를 가진
  markdown table)" 로 명시 권장
- [contract-design-guide.md:1084, qa-evaluation-guide.md:1641] 계약 조건은 아니지만 통합 후
  갱신 안 된 "6종"/"5종" 잔존 언급 발견 — 다음 문서 정비 시 10종 통합 참조로 갱신 권장 (조건
  미해당이라 FAIL 처리하지 않음, 정보 제공용)

## 자기진단 (Step 6)
- l3_unreached: false — 22개 조건 전부 명령 실행/파일 대조로 L3 도달
- bias_detected: false — FAIL 1건(DG-04) 발견, 관대화 없이 엄격 판정
- evidence_missing: false — 전 조건에 명령 출력·grep 결과·diff 인용
- contract_misinterpret: true (경계 사례) — DG-04 해석에 두 가지 독법(느슨: 이 계약 자체로 충족
  vs 엄격: 새 컨벤션을 실제 행사하는 신규 산출물 필요)이 가능했음. 엄격 해석 채택, 근거는 위
  Improvement 참조
- perspective_gap: false — 기술 정합성 중심 스프린트라 단일 관점(measurement 검증)이 적절

## 교차 진단 (Step 7)
- cross_diagnosis_by: unavailable — 이 실행 컨텍스트에는 서브에이전트 스폰 도구(Task/Agent)가
  제공되지 않아 sprint-contract 서브에이전트 교차 진단을 실행하지 못함. 자기진단(Step 6)의
  contract_misinterpret 항목으로 대체 기록
