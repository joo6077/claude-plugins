---
feature: "kaizen 2026-07-27 Phase 9 — rust-kit"
created: "2026-07-27"
iteration: 1
contract_root: "/Users/jackson/Hub/10_Dev/claude-plugins"
---

# Sprint Contract — Phase 9 (rust-kit)

## 배경 / 데이터 소스

- `.claude/kaizen-input/insights-report.md` §0 — Friction #2(검증 아티팩트) · #4(풀스택 counterpart 누락)
- `.claude/kaizen-input/reflect-digest-2026-07-27.md` — rust-kit 스킬 × 실수 교차 5 스킬
  (`rust-test` / `rust-service` / `rust-api` / `rust-model` / `rust-middleware`)
- `.harness/.meta/kaizen-data-pool.md` §1 글로벌 REJECT (DG-03 / API-01 / DA-01) · §2 외부 프로젝트
  (fit-pal-server · fitpal-server · fit-pal-wt)
- Phase 1 `skill-design-guide` v1.4.0 §3.7 (Completion Evidence Gate · E1/E2/E3) · §5.5 Counterpart Enumeration
- Phase 3 `qa-evaluation-guide` v4.0 §Canonical Unverified-Evidence Protocol · §Evidence Validity Gate
- Phase 4 전달 — rust-kaizen 카테고리 표기 7 → 8 (V1~V8), scope-creep = unit 기준

## 범위

수정 가능: `rust-kit/skills/*` · `rust-kit/agents/*` · `rust-kit/references/*` · `docs/rust/*`
· `.claude/skills/rust-kaizen/SKILL.md`
금지: 타 kit · `harness/` · marketplace.json · plugin.json · `docs/kaizen/changelog.md` · git 커밋 계열 명령

## 완료 조건

### RS — digest 실측 결함 대응 (5)

- [ ] RS-01 [exact]: `cargo-test-wrong-target` 차단 — `rust-kit/references/project-detection.md` 에
  `cargo metadata` 기반 **패키지 타깃 구조(bin/lib) 감지 단계**가 신설되고 `PKG_TARGETS` 변수가
  결과 요약 표에 등재된다. `rust-run` · `rust-test` · `rust-preflight` 3 스킬이 "lib 타깃 없는 패키지에
  `--lib` 금지 / `--bins` 사용" 규칙을 각각 보유한다 (Grep `--bins` 각 파일 1 건 이상).
- [ ] RS-02 [exact]: `unreliable-exit-status-capture` 3 회 재발 → **E2 승급**. `rust-run` 에
  `set -o pipefail` + `PIPESTATUS` 를 명시한 명령 실행 규약이 존재하고, `rust-run` Step 2 출력과
  `rust-preflight` 리포트 표에 **exit code 기록 칸**(아티팩트)이 추가된다.
- [ ] RS-03 [exact]: `bypass-run-guard-by-cwd` 차단 — `rust-run` 에 "가드 우회 금지 · cwd 이동으로 다른
  `.harness` 소싱 금지" 규칙 + `cargo locate-project --workspace --message-format plain` 기반
  프로젝트 루트 고정 절차가 `project-detection.md` 에 존재한다.
- [ ] RS-04 [exact]: `stack-inappropriate-rust-antipatterns` 차단 — rust-kit 규칙의 **적용 범위**
  (cargo 관리 `.rs` 산출물 한정) 가 `project-detection.md` 에 선언되고, `rust-audit` · `rust-reviewer`
  가 "셸/compose/CI 산출물에 Rust 안티패턴(`unwrap()`/`println!`) 적용 금지 + 셸 대응 규칙" 을 보유한다.
- [ ] RS-05 [exact]: `rust-test` 에 `port-already-in-use` 대응(포트 0 바인딩 후 실주소 조회) 규칙이 추가된다.

### EV — 증거/미검증 프로토콜 정합화 (3)

- [ ] EV-01 [exact]: `rust-kit/agents/rust-reviewer.md` 가 `qa-evaluation-guide.md`
  §Canonical Unverified-Evidence Protocol **5 조항을 문구 변형 없이 복제**하고, 정본 앵커를 인용한다.
  로컬 재정의(동의어 마커·임계값 재선언) 0 건.
- [ ] EV-02 [exact]: `rust-audit` · `rust-reviewer` 양쪽에 **Evidence Validity Gate 4 검사**와
  "0 매치 / 0 테스트를 PASS 로 쓰지 않는다 (positive control 필요)" 규칙이 존재한다.
- [ ] EV-03 [exact]: `rust-audit` Step 4 표의 Testing row 가 **단위 격리 / 실 DB 통합 커버리지 2 row 로
  분리**되고(API-01 대응), unwrap grep row 에 positive control 근거 요구가 명시된다.

### CP — Counterpart Enumeration (Friction #4) (2)

- [ ] CP-01 [exact, enumerated]: `rust-api` 에 Counterpart Enumeration Gotcha 가 추가되어
  producer(핸들러/DTO/OpenAPI) 와 consumer(클라이언트·타 서비스·계약 테스트·생성 코드) 를
  **경로로 양면 열거**하고 체크리스트 아티팩트(E2)로 남기도록 요구한다.
- [ ] CP-02 [exact, enumerated]: `rust-model` 에 스키마 변경(컬럼 rename·타입·nullable·enum) 의
  소비면 열거 규칙이 추가된다.

### MG — 마이그레이션 / 문서 조회 게이트 (3)

- [ ] MG-01 [exact]: DG-03 대응 — `rust-preflight` 에 test 단계 **이전** 마이그레이션 적용 상태 확인
  단계가 신설되고, `rust-test` 에 "`#[sqlx::test]` 는 자동 적용 / 공유 DB 대상 `cargo test --workspace`
  는 수동 선적용 필요" 구분이 명시된다.
- [ ] MG-02 [exact]: API-01 대응 — `rust-test` 에 "MockDatabase 단위 테스트를 통합 테스트로 주장 금지"
  규칙이 SeaORM 공식 문서 URL 근거와 함께 추가된다.
- [ ] MG-03 [exact]: usc=true 재위반(`external-api-doc-lookup-skipped` ·
  `missing-official-doc-lookup-for-external-api` · `research-before-edit-ignored`) 대응 —
  `rust-service` · `rust-api` 에 외부 크레이트 편집 전 **공식 문서 조회 기록**(크레이트 · 버전 · URL)
  아티팩트 요구(E2) 가 추가되고, `edit-before-read` 방지 규칙이 함께 들어간다.

### KZ — 자기 카이젠 스킬 / 문서 (3)

- [ ] KZ-01 [exact]: `.claude/skills/rust-kaizen/SKILL.md` 의 "7 카테고리" 표기가 **8 (V1~V8)** 로
  정정된다 (Grep "7 카테고리" 0 건).
- [ ] KZ-02 [exact]: rust-kaizen 에 (a) Enforcement 등급 기반 개선 원칙(재발 시 E1→E2→E3, 문장 재작성 금지)
  (b) scope-creep 은 파일 수 아닌 **unit(관심사)** 기준 (c) 신규 sibling parity group
  (rust-run · rust-preflight · rust-test 명령 실행 규약) 이 반영된다.
- [ ] KZ-03 [exact]: `docs/rust/research-log.md` 에 `## [2026-07-27] - Phase 9 kaizen` 엔트리가 추가되고
  **리서치 URL 5 건 이상**이 기재된다.

### RG — 회귀 (2)

- [ ] RG-01 [exact]: `python3 scripts/validate-plugin.py rust-kit` → V1~V8 전부 OK, Exit 0.
- [ ] RG-02 [exact]: 범위 밖 파일 수정 0 건 — `git status --short` 에 rust-kit / docs/rust /
  .claude/skills/rust-kaizen / .harness/history 외 변경 없음 (병렬 Phase 산출물 제외).

## 측정 방법

- Grep / Read 로 각 조건의 문자열 존재를 직접 확인 (파일:라인 인용)
- `python3 scripts/validate-plugin.py rust-kit` 실제 실행 출력
- `git status --short` (읽기 전용)

## 안티패턴 (이번 스프린트 금지)

- 신호 없는 스킬에 억지 변경 추가 (NO_CHANGE 가 정답이면 NO_CHANGE)
- 이미 승격된 규칙을 문장만 다시 다듬기 (등급 상향 없이)
- git add/commit/tag/push · finalize-phase.sh 실행
