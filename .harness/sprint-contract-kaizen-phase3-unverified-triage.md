---
feature: "카이젠 Phase 3 — 미검증 triage 정밀화(Q1) + 판별력 게이트(Q2) + 사용자 오라클(Q3) + 계약 봉인·amendment 소비면"
created: "2026-08-13 11:20"
rewritten: "2026-08-13 (v2 — AR-01/AR-02 상호배타로 원 계약 폐기)"
complexity: "복잡"
conditions: 25
slug: kaizen-phase3-unverified-triage
status: active
owner_session: df1b3e15-30b3-4825-a3c4-4ac44c686e94
supersedes_digest: sha256:67cd3b5df77a1acd
supersedes_commit: c3f9595
conditions_digest: sha256:80086c24f5c4e7f6
locked_at: "2026-08-13 (v2)"
---

## 폐기·재작성 (v2) — 앵커 있는 교체

**원 계약(`c3f9595`, `conditions_digest: sha256:67cd3b5df77a1acd`)은 폐기됐다.** 원문은 git 이력에 보존된다.

### 폐기 사유 — AR-01 과 AR-02 가 상호배타였다

QA 3 라운드(iter1 22/25 · iter2 23/25 · iter3 24/25)에서 증명된 계약 결함이다.

1. **AR-02 는 원문 그대로 만족 불가능했다.** `contract-design-guide.md` 는 파일 생성 이래
   YAML frontmatter 가 **존재한 적이 없다** (`git log --follow` 전수 확인). 따라서 "Parity with 의
   값이 그 파일 frontmatter `version` 과 일치" 라는 측정문의 PASS 집합은 **공집합**이었다.
2. **근본 해소는 AR-01 을 위반해야만 가능했다.** frontmatter 를 신설하려면 Phase 3 scope(2 경로)
   밖인 `contract-design-guide.md` 를 건드려야 한다. 구현자는 이를 `relaxing · unanchored` 로
   자기신고했고 — 규칙대로 **PASS 근거가 되지 못했다**. 자기신고가 자기면책이 되지 않은 것은
   봉인·2 축 amendment 가 의도대로 작동한 결과다.
3. **부수 결함**: 원 계약의 열거 경로 집합에 **amendment 사이드카 경로 자체가 없었다.** 교정을
   기록하는 행위가 곧 계약 위반이 되는 자기모순이다. → Phase 4 (harness) 에서 `scope_allowlist` 에
   사이드카·피드백 산출물 경로를 기본 포함하도록 구조 수정한다.
4. **AR-01 의 오라클도 결함이었다.** `git status --porcelain` 행 수를 재는데, 커밋 이후에는 항상 0 이라
   재현 불가능했다. 스프린트 base 대비 누적 diff 로 교체한다.

### 앵커 (relaxing → anchored 전환 근거)

- **승인 주체**: 사용자. 2026-08-13, 오케스트레이터가 3 개 선택지(사용자 앵커 amendment /
  계약 폐기 후 재작성 / 범위 복원 후 이월)를 근거와 함께 제시했고 **"계약 폐기 후 재작성"** 을 택했다.
- **재작성 주체**: 오케스트레이터. **구현 서브에이전트가 아니다.** 구현자가 자기 산출물을 허용하려
  본문을 고치는 것(2026-08-11 실측 위반)과 구분된다.
- 변경 범위는 AR-01(경로 집합·오라클) 과 §범위 경계 두 곳뿐이다. **나머지 23 조건은 문구 무수정**이며
  이미 검증된 판정이 그대로 유효하다.

## 배경

`.harness/.meta/evidence/phase3.md` 가 이번 Phase 의 **유일한 외부 근거**다. 외부 조회 0 회.

**Q1 이 최우선이다.** 직전 사이클(2026-07-27)이 `[미검증]` 을 3 분기 triage(대상 부재 / 도구 부재 /
증거 무효)로 쪼갰는데, **분류는 판정 문구에만 반영되고 임계 카운트에는 반영되지 않았다.**
그 결과 2026-08-11~12 에 4 건 연속으로 아래 형태가 관측됐다:

- `미검증 2건(UI-01, DG-02) — 둘 다 도구부재(런타임 캡처 MCP 미가용, IDE 진단 미가용)로 정당하나 임계 2건 이상이라 자동 REJECT 규칙 적용`
- `미검증 2건(DG-02 IDE lint 도구부재, DG-04 시뮬레이터 미부팅) — 2건 이상 자동 REJECT 규칙`
- `Unverifiable count = 2 (DG-02, DG-04) triggers automatic REJECT per contract v4 rule`
- `DG-02/DG-04 미검증 2건 — 자동 REJECT 임계(2건 이상) 충족 (도구부재/환경충돌, AR-04와 별개 사유)`

구현자가 통제할 수 없는 사유가 구현 결함과 **같은 reject counter** 에 들어간다. 반대 극단은 이미
잘 작동한다 — `DG-04: 실기 앱 구동 미실행(사용자 지시에 의한 계획적 이연) — 실행 산출물 부재로
FAIL(도구 부재 아님, 의도적 미실행)`. 따라서 이번 변경은 **완화가 아니라 정밀화**여야 하며,
"미구현을 도구 부재로 세탁" 하는 경로를 동시에 막아야 한다.

### 처리 방침 — 문장 추가가 아니라 카운터 분리 + 남용 방지

- Q1 → `[미검증]` 마커는 하나로 유지하되 분류 접미 2 종(`ENV` / `INVALID`)을 도입하고
  **자동 REJECT 카운터에서 `ENV` 를 분리**한다. 대신 (a) 남용 방지 4 요건 (b) 검증 커버리지 게이트
  (c) 2 iteration 연속 `ENV` 승급 3 겹으로 회피 경로를 닫는다.
- Q2 → 판별력(discrimination)을 **한정 범위**에서만 필수화한다. 전체 repo mutation score 임계값은
  넣지 않는다 (full mutation adequacy 는 "neither practical nor desirable").
- Q3 → 사용자 관측과 자기 증거가 충돌할 때의 우선순위를 `REOPENED` 규약으로 고정하고, 6 축 대조를
  **공유 rubric** 으로 쓴다 (human 단독 판정은 Fleiss' Kappa 0.307 로 낮았고 shared rubric 이
  agreement 를 크게 개선했다).
- Phase 2 산출물의 **소비면 착지** — `verify_seal` 을 평가 절차에 넣고, amendment 를
  direction × consent 2 축으로 재해석한다. 이 둘이 없으면 Phase 2 는 쓰기 측만 강화된 채 끝난다.

## 리서치 소스 (evidence 파일 한정 — 외부 조회 0 회)

- `.harness/.meta/evidence/phase3.md` §1~§6 — 실측 결함 Q1~Q4 · 외부 근거 URL/수치 · 사실 정정 ·
  규칙 초안 · 트레이드오프 · 열린 질문
- `.harness/.meta/kaizen-data-pool.md` §1 — REJECT `UI-01`/`DG-02`/`DG-04`(미검증 임계 4 건) ·
  `ER-02`(mutation 확정) · `LG-01`/`LG-03` · `AR-04`(amendment unknown 붕괴),
  Improvement `[DG-04] 검증경로-미기재 — 2 이터레이션 연속 [미검증]` ·
  `[DG-04] 측정-환경-오염` · `[ER-02] 측정-산출물-부재`
- `.claude/kaizen-input/insights-report.md` — 직전 사이클 흡수분 표(재승격 금지) + 신규 델타 D3
- `docs/kaizen/changelog.md` `[2026-07-27]` / `[2026-07-28]` — 재승격 금지 대상
- Phase 1 산출물 — `skill-design-guide.md` §3.7 등급 원장 · §3.8 User-Reported Failure Gate ·
  `agent-design-guide.md` §10 사용자 보고 우선 Gotcha · §12 parity item 8
- Phase 2 산출물 — `harness/references/contract-schema.md` v5.3 §계약 봉인 · §Amendment 사이드카 ·
  §음성 대조 · §인자 매트릭스

## GAP 분석 (전부 실측)

| # | 갭 | 실측 근거 | 처리 |
| --- | --- | --- | --- |
| G1 | triage 결과가 임계 카운터에 반영되지 않는다 | REJECT 4 건 전부 "도구부재로 정당하나 임계 2건" | 분류 접미 + 카운터 분리 |
| G2 | 카운터를 분리하면 "미구현 → 도구부재" 세탁 경로가 열린다 | evidence §5 트레이드오프 | 4 요건 + 커버리지 게이트 + 재발 승급 |
| G3 | 같은 조건이 반복 미검증이어도 승급 규칙이 없다 | Improvement `[DG-04] 2 이터레이션 연속 [미검증]` | 2 회 연속 `ENV` → 계약 결함 승급 |
| G4 | 측정이 구현을 경유하는지 보는 절이 없다 | REJECT `ER-02` — 가드를 삭제해도 테스트 통과 (mutation 확정) | §Discriminating Evidence Gate 신설 |
| G5 | 사용자 관측 vs 자기 증거 우선순위가 정의되지 않았다 | §0 D3 — 테스트 증거로 사용자 리포트 반박 → 에스컬레이션 | §Canonical User-Reported Failure Protocol 신설 |
| G6 | Phase 2 봉인의 소비면이 없다 | `verify_seal` grep 결과 평가 측 2 파일 0 건 | Step 1-e 에 봉인 검증 착지 |
| G7 | amendment 가 1 축 3 값이라 앵커 부재가 방향 판정을 붕괴시킨다 | REJECT `amendment A-01은 prompt-log 앵커 부재로 unknown 분류` | direction × consent 2 축 소비 |
| G8 | scoring bias 논문을 binary PASS/FAIL 의 근거로 인용 | evidence §3 — 원문은 3 종 scoring bias 를 정의할 뿐 | CheckEval 로 정정 |
| G9 | frontmatter `tools` 에 Write 가 없는데 본문이 저장을 지시 | audit-log 이월 backlog 2 건 | 본문 판정 후 저장 수단 명시 |

## 범위 경계

- **수정 허용 3 경로**: `harness/docs/guides/qa-evaluation-guide.md` ·
  `harness/agents/qa-evaluator.md` · `harness/docs/guides/contract-design-guide.md`
  (세 번째는 v2 에서 추가 — AR-02 의 frontmatter 원본을 신설해야 만족 가능해지기 때문. 앵커는 §폐기·재작성).
- **harness 산출물 2 경로**는 구현 변경과 분리해 열거한다:
  `.harness/sprint-contract-kaizen-phase3-unverified-triage.md` ·
  `.harness/sprint-amendments-kaizen-phase3-unverified-triage.md`.
  교정 기록 행위가 계약 위반이 되지 않도록 사이드카를 명시 포함한다 (원 계약의 자기모순 해소).
- **각 kit reviewer 6 종(`*-kit/agents/*-reviewer.md`)은 이번 scope 밖**이다. Canonical 절 2 종
  (`Unverified-Evidence` · 신규 `User-Reported Failure`)의 복제는 각 kit 카이젠 Phase 소관이며,
  본 스프린트는 전파 지시만 남긴다 — `[미검증]` 이 아니라 명시적 미완 항목이다.
- `.claude/skills/kaizen-orchestrator/references/phase-research-templates.md` 의
  `binary PASS/FAIL 강제` 오인용과 `docs/kaizen/research-log.md` 의 같은 표기는 **scope 밖**이다
  (Phase 4 harness 소관). 정정 대상 목록만 남긴다.
- `harness/references/contract-schema.md` 는 **무수정**이다. `verify_seal` · `amend_direction`
  함수 정의의 SSOT 이므로 평가 측에서 재정의하지 않고 인용만 한다.

### 열린 질문에 대한 결정 (evidence §6 — 근거를 남긴다)

1. **verdict taxonomy 에 `CONDITIONAL APPROVE_WITH_ENV_GAPS` 를 추가하지 않는다.**
   `harness/references/feedback-schema.yaml` 이 `verdict: enum [APPROVE, REJECT, BLOCKED]` 로
   고정돼 있고, Canonical Unverified-Evidence Protocol 3 항이 이미 "CONDITIONAL APPROVE" 를
   "1 건 + FAIL 0" 로만 한정한다. 새 verdict 어휘를 만들면 kit reviewer 6 종과 집계 스크립트가
   동시에 어긋난다. 대신 **APPROVE + `env_gaps: N` 표면화**로 표현한다.
2. **커버리지 임계는 `0.60` 에서 출발한다.** selective classification 의 예시(ImageNet top-5
   error 2% 를 99.9% 로 보장하며 coverage 약 60%)에서 가져온 **출발값이지 증명된 임계가 아니다.**
   재조정 트리거를 함께 규정한다 — 커버리지 게이트가 BLOCKED 를 낸 사례가 3 회 누적되면
   evaluator-kaizen 이 실측 분포로 재조정한다.
3. **mutation 도구의 스택별 표준은 이번에 정하지 않는다.** evidence 에 스택별 도구 근거가 없다.
   대신 도구 비의존 절차(결합 확인 static → 계약 `음성 대조:` 절 → 안전 조건부 실행 변형)로
   규정하고, 원본 작업트리 변형 금지·원상복구 확인을 안전 조건에 넣는다.

## 회귀 게이트

- `[미검증]` 마커 어간은 바뀌지 않는다. 접미 없는 `[미검증]` 은 레거시이며 **엄격 쪽
  (`INVALID`)** 으로 해석한다 — 기존 배포본의 판정이 관대해지는 방향으로 바뀌지 않는다.
- `SEAL_ABSENT` 는 경고이지 실패가 아니다. 실측 109 개 계약 전부가 `SEAL_ABSENT` 이므로
  BLOCKED 로 만들면 전 배포본이 죽는다.
- 용어 6 종(`SEAL_OK` · `SEAL_BROKEN` · `SEAL_ABSENT` · `direction` · `consent` · `REOPENED`)에
  동의어를 만들지 않는다.

## Architecture

- [ ] AR-01: 스프린트 누적 변경이 정확히 5 경로로 한정된다 [exact, enumerated]
      (Given: 스프린트 base = `b9e911f` (Phase 2 종료 커밋) ·
       측정: `git diff --name-only b9e911f..HEAD` 출력을 정렬한 집합이 아래 5 경로와
       `comm -3` 양방향 차집합 0 건 —
       `harness/agents/qa-evaluator.md`,
       `harness/docs/guides/contract-design-guide.md`,
       `harness/docs/guides/qa-evaluation-guide.md`,
       `.harness/sprint-amendments-kaizen-phase3-unverified-triage.md`,
       `.harness/sprint-contract-kaizen-phase3-unverified-triage.md`.
       `git status --porcelain` 은 커밋 이후 항상 0 행이라 재현 불가능하므로 오라클로 쓰지 않는다)
- [ ] AR-02: `harness/docs/guides/qa-evaluation-guide.md` 의 버전 정보 3 행이 실제 값과 일치한다
      [exact, enumerated]
      (측정: Schema link 가 `harness/references/contract-schema.md` 의 현재 스키마 버전과 동일하고,
       Parity with 의 3 값이 `skill-design-guide.md` · `agent-design-guide.md` frontmatter 의
       `version` 및 `contract-design-guide.md` frontmatter 의 `version` 과 각각 동일 —
       네 값을 명령으로 추출해 문자열 비교, 불일치 0 건. 손으로 타이핑한 값 비교 금지)
- [ ] AR-03: 평가자 등급표가 `skill-design-guide.md` §3.7 등급 원장을 복제하지 않는다 [exact]
      (측정: 원장 8 행의 원칙명을 추출해 평가자 등급표 행의 원칙명 열과 교집합을 계산 — 0 건.
       같은 절에 "원장" 과 "§3.7" 이 함께 등장해 참조 관계가 명시된다)
- [ ] AR-04: 이번 사이클 신규 평가자 원칙 전부에 Enforcement 등급이 표기된다 [structural, enumerated]
      (측정: 신규 원칙 4 종 — `UNVERIFIED_ENV` 분리 · 검증 커버리지 게이트 ·
       Discriminating Evidence Gate · 계약 봉인 검증 — 이 등급표에 각각 1 행으로 존재하고
       각 행의 등급 값이 `E1`/`E2`/`E3` 중 하나. 등급 미표기 행 0 건)
- [ ] AR-05: parity 표에 User-Reported Failure Gate 행이 추가되고 표의 행 수가 계산값과 일치한다
      [structural]
      (측정: parity 표 행 수를 `awk` 로 계산하고, 표 아래 서술이 인용하는 개수와 동일.
       수기 타이핑한 개수 금지)

## Skill

- [ ] SK-01: §증거 분류 triage 가 4 분기로 확장되고 분류어 2 종이 정의된다 [exact, enumerated]
      (측정: `UNVERIFIED_ENV` 와 `UNVERIFIED_INVALID_EVIDENCE` 두 문자열이 가이드와 에이전트
       양쪽에 각각 1 회 이상 존재하고, triage 표의 행 수가 4 이며 FAIL 분기에
       "의도적" 또는 "회피성" 미실행이 명시된다)
- [ ] SK-02: `UNVERIFIED_ENV` 남용 방지 요건이 4 개 항목으로 열거되고 미충족 시 강등 규칙이 있다
      [exact, enumerated]
      (측정: 4 요건 — 1 차 도구 시도 · fallback 시도 · 실패 로그 · 통제 불가 사유 + 재검증 명령 —
       이 번호 목록으로 존재하고, "하나라도" 미충족 시 `UNVERIFIED_INVALID_EVIDENCE` 로 강등한다는
       문장이 존재)
- [ ] SK-03: 검증 커버리지 게이트가 산식·임계·verdict 매핑·재조정 트리거 4 요소를 갖는다 [structural]
      (측정: 커버리지 산식이 조건 총수와 `env_gaps` 로 표현되고, 임계값 숫자가 명시되며,
       미달 시 verdict 가 `BLOCKED` 임이 적혀 있고, 재조정 트리거 문장이 존재)
- [ ] SK-04: 신규 §Discriminating Evidence Gate 가 적용 범위와 금지 목록과 절차를 갖는다
      [exact, enumerated]
      (측정: 적용 대상이 9 항 — 동시성 가드 · 인증/권한 · 멱등성 · 입력 검증 · 데이터 유실 ·
       마이그레이션 안전성 · 재시도/중복제거 · 보안 경계 · 사용자 보고와 테스트 PASS 충돌 —
       으로 열거되고, 금지 3 항(전체 repo mutation score 임계값 · 모든 조건 강제 ·
       cosmetic/doc-only 요구)이 명시되며, 절차가 3 단계로 번호 매겨진다)
- [ ] SK-05: 신규 §Canonical User-Reported Failure Protocol 이 5 조를 담고 상위 가이드와 용어가
      일치한다 [exact, enumerated]
      (측정: `REOPENED` · `반박` · 6 축 축 이름 6 종 · 완료 해제 3 택이 절 안에 존재하고,
       6 축 이름이 `skill-design-guide.md` §3.8 표의 축 이름과 문자열로 대응한다.
       Evidence Validity Gate 와의 차이를 서술한 문장이 존재)
- [ ] SK-06: §Amendment 소비 규칙이 direction × consent 2 축으로 재작성된다 [exact]
      (측정: `direction` 과 `consent` 두 낱말이 절 안에 존재하고 2×2 조합표가 있으며,
       `narrowing` × `unanchored` 칸이 PASS 근거 **가능**으로 적혀 있다.
       "앵커 없으면 unknown" 형태의 옛 규칙 잔존 0 건)
- [ ] SK-07: 계약 봉인 소비 규약이 평가 절차에 착지한다 [exact, enumerated]
      (측정: `verify_seal` 호출이 에이전트 본문에 존재하고 `SEAL_OK` · `SEAL_BROKEN` ·
       `SEAL_ABSENT` 3 값 각각의 verdict 영향이 명시되며, `SEAL_ABSENT` 가 경고이지 실패가
       아님이 적혀 있다)
- [ ] SK-08: Canonical Unverified-Evidence Protocol 5 조가 새 분류 체계로 갱신되고 전파 지시가
      남는다 [structural]
      (측정: 3 항의 임계 서술이 새 분류어를 쓰고, 각 kit reviewer 로의 전파가 "각 kit Phase 소관"
       으로 명시된다)

## Error

- [ ] ER-01: scoring bias 논문을 binary PASS/FAIL 의 근거로 인용한 곳이 scope 2 파일에 0 건이다
      [exact]
      (측정: 두 파일에서 `2506.22316` 이 등장하는 모든 줄을 출력하고, 그 줄들에
       "이진" 또는 "binary" 를 완화 전략·근거로 결부한 표현이 0 건임을 확인)
- [ ] ER-02: binary/decomposed 의 직접 근거가 CheckEval 로 명시된다 [exact]
      (측정: `2403.18771` 이 편향 표의 scoring bias 행 완화 전략에 등장하고,
       평가자 간 일치도 개선 수치 `0.45` 가 같은 맥락에 존재)
- [ ] ER-03: evidence 파일에 없는 URL 이 신규 서술에 0 건이다 [exact]
      (측정: 이번 diff 에서 추가된 줄의 URL 을 전부 추출하고, 각 URL 이
       `.harness/.meta/evidence/phase3.md` 또는 변경 전 원본 파일에 이미 존재함을 확인 — 신규 0 건)
- [ ] ER-04: `UNVERIFIED_ENV` 가 미구현·의도적 미실행의 세탁 경로가 되지 않는다 [exact]
      (측정: FAIL 분기 정의에 "미구현" 과 "의도적" 또는 "회피성" 이 함께 등장하고,
       애매할 때 FAIL 쪽 엄격 해석을 적용한다는 문장이 유지된다)

## Anti-patterns

- [ ] AP-03: 두 파일의 신규 코드 펜스에 언어 힌트가 있다 — bare fence 0 건 [exact]
      (측정: 펜스 길이를 인식하는 검출기로 두 파일의 여는 펜스를 판정 — 언어 힌트 없는 여는 펜스
       0 건. 나이브 `^```$` grep 은 닫는 펜스를 오탐하므로 오라클로 쓰지 않는다)
- [ ] AP-04: `harness/agents/qa-evaluator.md` frontmatter 의 `name` 과 `tools` 가 보존된다 [exact]
      (측정: frontmatter 에서 두 값을 추출해 HEAD 판과 문자열 동일 — `tools` 값이
       `Read, Grep, Glob, Bash` 그대로이며 Write 가 추가되지 않았다)

## Reusability

- [ ] RE-01: 신규 셸 스니펫이 기존 SSOT 를 재정의하지 않는다 [exact, enumerated]
      (측정: scope 2 파일에서 `verify_seal() {` · `contract_digest() {` · `amend_direction() {`
       세 함수 정의가 각각 0 건이고, 대신 `contract-schema` 참조가 같은 절에 존재)
- [ ] RE-02: 용어 6 종에 동의어를 만들지 않는다 [exact, enumerated]
      (측정: 금지 동의어 후보 — `SEAL_MISSING` · `seal_ok` · `방향성` · `동의여부` ·
       `REOPEN` 단독형 · `미확인` — 이 scope 2 파일에 0 건)

## Diagnostics

- [ ] DG-01: `python3 scripts/validate-plugin.py harness` 가 FAIL 0 건 [exact]
      (측정: 명령을 실행해 종료 코드와 FAIL 카운트를 출력)
- [ ] DG-02: 두 파일의 신규·변경 `bash` 코드 펜스가 구문 검사를 통과한다 [exact]
      (IDE 진단 대체 — 이 레포에는 IDE lint 대상 소스가 없다 ·
       측정: 각 `bash` 펜스 본문을 추출해 `bash -n` 실행, 실패 0 건)
- [ ] DG-03: `python3 scripts/sync-docs.py --check-only` 가 이번 변경으로 인한 갱신 필요를
      보고하지 않는다 [exact]
      (측정: 명령 실행 출력에 두 scope 파일이 갱신 대상으로 등장하지 않음)
- [ ] DG-04: 신규·변경 스니펫이 zsh 와 bash 양쪽에서 동일한 결과를 낸다 [exact]
      (실기 구동 대체 — 이 레포에는 런타임 앱이 없다 ·
       측정: 조건 검증에 사용한 전 명령을 두 셸에서 실행하고 출력을 `diff` — 차이 0 건.
       멀티바이트 필드폭 패딩을 쓰지 않는다)
