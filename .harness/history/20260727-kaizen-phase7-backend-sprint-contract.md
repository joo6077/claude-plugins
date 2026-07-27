# Sprint Contract — Kaizen Phase 7 (backend-kit)

- **Date**: 2026-07-27
- **Branch**: kaizen/2026-07-27
- **Scope**: `backend-kit/skills/*`, `backend-kit/agents/backend-reviewer.md`, `docs/backend/research-log.md`, `.claude/skills/backend-kaizen/SKILL.md`
- **Out of scope (hard)**: 다른 kit(특히 rust-kit), `harness/`, `.claude/skills/kaizen-orchestrator/`, marketplace.json, plugin.json, `docs/kaizen/changelog.md`
- **Parallel-safe**: git add/commit/tag/finalize 금지 (오케스트레이터 직렬 처리)

## 배경 — 이번 사이클 신호

| # | 신호 | 출처 | backend-kit 현재 상태 |
| - | ---- | ---- | --------------------- |
| A | Friction #4 풀스택 변경에서 클라이언트 누락 (반복) | insights §0 | Counterpart 관련 문장 **0 건** (4 스킬 + 에이전트 전수 grep) |
| B | 404→200 empty-body 계약 변경이 클라 파싱을 깨뜨림 | insights §0 | 빈 상태 상태코드 기준 **부재** |
| C | UTC 직렬화 버그가 e2e 에서만 표면화 | insights §0 | timestamp 타임존/직렬화 기준 **부재** |
| D | FCM idempotency (partial unique index 409, 비멱등 write path) | insights §0 | idempotency 기준이 **event consumer 전용** — HTTP write path 부재 |
| E | 글로벌 REJECT API-01: mock-only 를 통합 테스트로 주장 | data-pool §1 | "실제 DB (Testcontainers 등)" 만 있고 **명명·주장 규율 부재** |
| F | 글로벌 REJECT DG-03: 로컬 DB 마이그레이션 미적용으로 통합테스트 2건 실패 | data-pool §1 | 마이그레이션 선행 확인 **부재** |
| G | 글로벌 개선제안 DA-01/DA-02: "마이그레이션 파일 코드 확인으로 대체 가능" 명시 요구 | data-pool §1 | 정적 대체 판정 규약 **부재** |
| H | digest `stack-inappropriate-rust-antipatterns` | reflect-digest | backend-audit/reviewer 에 스택 감지 단계 **부재** (backend-test 만 Step 0 보유) |
| I | Phase 3 실측: backend-reviewer 가 canonical 5 조항 대신 로컬 재정의 보유 | Phase 3 전달 | §8 이 임계·마커를 자체 정의 |
| J | Phase 4 전달: backend-kaizen SKILL.md "7 카테고리" 표기 | Phase 4 전달 | 2 곳 (Gotcha 5 · Step 6), 실제는 V1~V8 |

## 완료 조건

### CP — Counterpart Enumeration 도메인 일반화 (Friction #4 · 최우선)

- [ ] CP-01: `backend-kit/skills/backend-system/SKILL.md` Gotchas 에 Counterpart Enumeration 항목이 존재하고, enforcement 등급을 **E2** 로 명시하며 SSOT 앵커 `skill-design-guide.md §5.5`(또는 `§3.7`)를 인용한다 [exact] (측정: 해당 파일에 `Counterpart` + `E2` + `§5.5` 동시 존재)
- [ ] CP-02: `backend-kit/skills/backend-guide/SKILL.md` Gotchas 에 Counterpart Enumeration 항목이 존재하고 **소비면 내부 구현 조건화 금지**(Pact over-specified 경고)를 함께 명시한다 [exact] (측정: `Counterpart` + `over-specified` 문자열 존재)
- [ ] CP-03: `backend-kit/skills/backend-audit/SKILL.md` Gotchas 에 소비자 정합성 감사 항목이 존재하고, **같은 저장소 안 소비자 미확인은 `[미검증]` 이 아니라 감사 누락**임을 명시한다 [exact]
- [ ] CP-04: `backend-kit/agents/backend-reviewer.md` 에는 Counterpart 전용 doctrine 절을 **만들지 않는다** (parity item 12 의도된 부재) [exact] (측정: `backend-reviewer.md` 에 `Counterpart` 제목 절 0 건)
- [ ] CP-05: backend-system Process Step 3 산출물에 producer/consumer 양면 파일 열거 체크리스트가 포함된다 [structural]

### CT — 계약 아티팩트 규격 (insights on_the_horizon)

- [ ] CT-01: backend-system 에 계약 아티팩트(`contracts/<feature>.md`) 규격이 정의되고 최소 6 항목(엔드포인트 · **빈 상태 포함 상태코드** · **timestamp 타임존/직렬화** · idempotency 시맨틱 · 소비자 파일 열거 · 요청/응답 예시 6 개 이상)을 열거한다 [exact, enumerated]
- [ ] CT-02: 빈 상태 상태코드 원칙(404 = "표현 없음" 이지 "컬렉션이 비었음" 아님)이 RFC 9110 출처와 함께 backend-system 또는 audit-criteria 에 존재한다 [exact]

### AC — audit-criteria.md 신규 rule (SSOT)

- [ ] AC-01: `backend-kit/skills/backend-audit/references/audit-criteria.md` §2 API Design 에 **빈 상태 상태코드 일관성** rule 추가 (출처 RFC 9110) [exact]
- [ ] AC-02: 같은 파일 §2 에 **Timestamp 직렬화 규칙** rule 추가 (출처 RFC 3339 · `-00:00` vs `Z` 구분 명시) [exact]
- [ ] AC-03: 같은 파일 §2 에 **비멱등 write path idempotency** rule 추가 (Idempotency-Key draft 상태를 **만료(expired)** 로 정확히 서술 · 409/422 코드 명시) [exact]
- [ ] AC-04: 같은 파일 §2 에 **소비자 정합성(provider verification)** rule 추가 (출처 Pact / BDCT) [exact]
- [ ] AC-05: 같은 파일 §3 Database 에 **라이브 DB 조회 불가 시 마이그레이션 DDL 정적 확인 대체** 규약 + `[정적]` 보조 태그 사용 명시 (글로벌 DA-01/DA-02 제안 흡수) [exact]
- [ ] AC-06: 같은 파일 §9 Testing 에 **mock-only 를 통합 테스트로 계상 금지** rule + **마이그레이션 적용 선행** rule 2 건 추가 [exact, enumerated]

### ST — 스택 정합성 (digest stack-inappropriate)

- [ ] ST-01: `backend-kit/skills/backend-audit/SKILL.md` 에 **Step 0 스택 감지** 단계가 신설되고, 감지 스택에 대응물이 없는 기준은 N/A + 사유로 처리(타 스택 고유 기준 오적용 금지)함을 명시한다 [exact]
- [ ] ST-02: `backend-kit/agents/backend-reviewer.md` 핵심 규칙에 스택 정합성 pre-check 항목이 추가된다 [exact]

### RV — backend-reviewer canonical 정합화 (Phase 3)

- [ ] RV-01: `backend-reviewer.md` 의 미검증 프로토콜이 `harness/docs/guides/qa-evaluation-guide.md §Canonical Unverified-Evidence Protocol` 5 조항을 **문구 변형 없이** 복제한다 [exact, enumerated] (측정: 5 조항 각각의 핵심 문장이 원문과 동일)
- [ ] RV-02: 복제 절에 SSOT 앵커 경로가 명시되고, 로컬에서 임계값·마커 의미를 **재정의하지 않는다** [exact]
- [ ] RV-03: CONDITIONAL APPROVE 는 "1 건 + FAIL 0" 경우에만 유효하다는 canonical 3 항과 충돌하지 않는다 [structural]

### TS — backend-test (글로벌 REJECT API-01 · DG-03)

- [ ] TS-01: `backend-kit/skills/backend-test/SKILL.md` 에 **mock-only 테스트를 integration 으로 명명·주장 금지** Gotcha 추가 + 실행 증거 없는 통과 주장 금지(§3.7 Completion Evidence Gate) 명시 [exact]
- [ ] TS-02: 같은 파일에 **통합 테스트 실행 전 마이그레이션 적용 확인** Gotcha 추가 [exact]
- [ ] TS-03: 같은 파일에 **계약 변경 테스트는 양면(consumer contract + provider verification)** Gotcha 추가 [exact]

### KZ — backend-kaizen 자기 스킬 (Phase 4 전달)

- [ ] KZ-01: `.claude/skills/backend-kaizen/SKILL.md` 의 "7 카테고리" 표기가 **8 카테고리(V1~V8)** 로 정정된다 [exact] (측정: `7 카테고리` 0 건, `V1~V8` 존재)
- [ ] KZ-02: scope 규율이 **파일 수**가 아닌 **unit(관심사)** 기준으로 재서술된다 [exact]
- [ ] KZ-03: Phase 1~3 신규 원칙(§3.7 Completion Evidence Gate / E1·E2·E3 / §5.5 Counterpart Enumeration / Canonical Unverified-Evidence Protocol)이 다음 사이클 전수 감사 목록에 포함된다 [exact, enumerated]
- [ ] KZ-04: I-02 예외 목록에 병렬 카이젠용 `.harness/history/` 계약 경로가 포함된다 [exact]

### DOC — 리서치 로그

- [ ] DOC-01: `docs/backend/research-log.md` 에 `## [2026-07-27] - Phase 7 kaizen` 엔트리가 추가되고 **리서치 URL 5 건 이상**이 기록된다 [exact, enumerated]
- [ ] DOC-02: 각 소스의 버전/상태 서술은 **조회 결과 기준**으로만 작성한다 (Idempotency-Key draft 는 만료 상태로 기록) [exact]

### RG — 회귀 게이트

- [ ] RG-01: `python3 scripts/validate-plugin.py backend-kit` 8 카테고리 전부 OK · Exit 0 [exact]
- [ ] RG-02: 범위 밖 파일 수정 0 건 — `git status --short` 에 backend-kit / docs/backend / .claude/skills/backend-kaizen / .harness/history 외 경로 변경 없음 [exact]
- [ ] RG-03: 중복 금지 준수 — 직전 사이클 승격분(Enumerate-before-Act · 최소변경 · 스킬호출증거)을 새 Gotcha 로 재추가하지 않는다 [structural]

## 비목표

- backend-kit 신규 스킬 생성 (backlog `backend-edge` / `backend-ai-runtime` 유지)
- docs/backend/ 하위 fundamentals/patterns/protocols 본문 개편 (리서치 로그만 갱신)
- README.md / evals.json 재생성 (변경 없음 — sync-docs 대상 아님)
