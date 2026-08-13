---
feature: "카이젠 Phase 9 — rust-kit sqlx::test 사실 정정 + unwrap 타입설계·lint 게이트(J1) · DB guard 판별력 SSOT(J2) · 버전 현행성 가드"
created: "2026-08-13 14:20"
complexity: "복잡"
conditions: 24
slug: kaizen-phase9-rust-guards
status: active
owner_session: df1b3e15-30b3-4825-a3c4-4ac44c686e94
conditions_digest: sha256:ae271946a5eac9cf
locked_at: "2026-08-13 14:20"
---

## 배경

`.harness/.meta/evidence/phase9.md` 가 이번 Phase 의 **유일한 외부 근거**다. 외부 조회 0 회
(네트워크 도구 미사용).

evidence 가 지적한 것은 세 층이다.

**(1) 사실 오류.** rust-kit 과 `docs/rust/` 가 `#[sqlx::test]` 를 "테스트별 독립 트랜잭션 + 자동
롤백" 으로 설명한다. 공식 문서 기준 이것은 거짓이다 — 이 매크로는 **함수마다 새 테스트 DB 를
만들고 live connection 을 주입하며, `migrations` 폴더가 있으면 자동 적용하고, 테스트가 성공하면
그 DB 를 정리**한다. 같은 유형으로 Axum 0.8 공식 발표일이 `2024-12-01` 로 적혀 있으나 공식
블로그는 `2025-01-01` 이다.

**(2) 실측 REJECT 2 종에 대응하는 게이트 부재.** 2026-08-12 fit-pal 글로벌 피드백:

- `AP-05` — "`modules/record/src/personal_records.rs:139,142` 의 `into_entry()` 가 프로덕션 코드
  경로에서 `.expect()` 를 사용한다" → **J1**. 같은 날 improvement 는 `?` 치환이 아니라
  **"Option 필드를 구조상 non-optional 로 재설계하거나 `HashMap` 누적 방식으로 바꿔 expect() 제거"**
  를 권고했다 — 즉 필요한 것은 치환이 아니라 **타입 설계 제거**다.
- `ER-02` — "**mutation test 로 확정 — 실제 코드에서 동시성 가드(`WHERE exercises = $3::jsonb`)를
  완전히 삭제해도 이 테스트는 여전히 통과한다**" → **J2**. 같은 날 improvement 가 "UPDATE 호출부를
  `main()` 에서 별도 함수로 추출해 **MockDatabase 로** conflict 시나리오를 재현하라" 고 권고했는데,
  evidence 는 이 권고의 후반부를 **정정**한다 — MockDatabase 는 `rows_affected` 매핑과 repository
  control flow 는 검증하지만 **실제 SQL predicate 가 행을 걸러내는지는 검증하지 못한다.**
  판별력은 `#[sqlx::test]` 또는 testcontainers 같은 **실 DB 엔진**에서만 나온다.

`/insights` 신규 델타 **D4**(read-check-then-write 경합의 SQL 술어 해소)가 Phase 9 직접 신호로
지정돼 있고, 위 `ER-02` 와 같은 대상이다 — 따라서 J2 와 하나의 SSOT 로 처리한다.

**(3) 버전 현행성.** docs.rs latest 기준 `axum 0.8.9` · `sqlx 0.9.0` · `sea-orm 2.0.1` ·
`testcontainers 0.28.0` 인데 rust-kit 은 `sqlx 0.8` · `sea-orm 1.1` · `testcontainers 0.27` 을
전제로 쓰고 있다. 다만 **강제 업그레이드는 금지**다 (evidence 트레이드오프: 기존 프로젝트가 하위
버전에 고정돼 있으면 migration 비용 발생). 버전 가드 형태로 착지시킨다.

**enforcement 프레이밍.** J1 은 이미 E1 문장 조항(`rust-error` Gotcha 2 · audit-criteria §2 ·
reviewer row 4)이 **3 표면에 존재하는데도** 실측 REJECT 가 났다. 문장을 또 추가하지 않는다 —
(a) 원인을 "치환 대상 오지정"(`?` 치환만 제시하고 타입 설계 제거를 제시하지 않음)으로 규명하고
(b) 등급을 **E1 → E3 로 승급**한다. E3 게이트는 workspace `[workspace.lints.clippy]` 의
`unwrap_used`/`expect_used`/`panic`/`panic_in_result_fn` deny 다 — LLM 호출 없이 `cargo clippy` 가
매 실행마다 판정하고 통과 전 진행을 막는다 (`skill-design-guide.md` §3.7 E3 정의).
J2 는 대응 조항이 **0 건**인 신규 신호라 신설이며, 등급은 **E2**(음성 대조 테스트 쌍이라는
아티팩트를 남긴다). Phase 3 이 만든 §Discriminating Evidence Gate 와 contract-schema v5.3
§음성 대조 는 **평가자 측·계약 측 정본**이므로 재정의하지 않고 **인용만** 한다.

## 리서치 소스 (evidence 파일 한정 — 외부 조회 0 회)

- `.harness/.meta/evidence/phase9.md` §1~§4 — 관찰 사실 8 항 · 권장안 6 항 · **넣지 말 것** 목록 ·
  트레이드오프 4 항 · 열린 질문 4 항. 인용 URL 13 종:
  `docs.rs/axum` · `docs.rs/sqlx` · `docs.rs/sea-orm` · `docs.rs/testcontainers` ·
  `tokio.rs/blog/2025-01-01-announcing-axum-0-8-0` · `github.com/tokio-rs/axum CHANGELOG` ·
  `lexi-lambda.github.io parse-don't-validate` · `docs.rs/nonempty` · `cliffle.com/blog/rust-typestate` ·
  `rust-lang.github.io/rust-clippy` (`unwrap_used` · `expect_used` · `panic` · `panic_in_result_fn`) ·
  `doc.rust-lang.org/cargo workspaces#the-lints-table` · `docs.rs/sqlx/attr.test.html` ·
  `docs.rs/sqlx/macro.query.html` · `sea-ql.org/SeaORM/docs/write-test/mock/` · `mutants.rs` ·
  `doc.rust-lang.org/cargo/commands/cargo-metadata.html` · `cargo-test.html` ·
  `blog.rust-lang.org/2025/02/20/Rust-1.85.0/` · `edition-guide/rust-2024/cargo-resolver.html`
- `.harness/.meta/kaizen-data-pool.md` §1 — REJECT Top 20 의 `AP-05` · `ER-02`,
  Improvement Top 15 의 "`into_entry()` … `HashMap` 누적 방식으로 바꿔 expect() 제거 권장" ·
  "UPDATE 호출부를 별도 함수로 추출"
- `.claude/kaizen-input/insights-report.md` — 직전 사이클 흡수분 표(재승격 금지) · 신규 델타 **D4**
  (Phase 7/9 직접 신호)
- Phase 1 산출물 `harness/docs/guides/skill-design-guide.md` §3.7 — Enforcement 3 등급 · 승급 규칙
- Phase 3 산출물 `harness/docs/guides/qa-evaluation-guide.md` §Discriminating Evidence Gate —
  판별력 절차 정본 (인용 전용)
- Phase 2 산출물 `harness/references/contract-schema.md` v5.3 — 본 계약 포맷 SSOT · §음성 대조

## GAP 분석 (전부 실측 · 명령 출력 기준)

| # | 갭 | 실측 근거 (사전 측정) | 처리 |
| --- | --- | --- | --- |
| F1 | `#[sqlx::test]` 를 트랜잭션/롤백으로 설명 | `grep -rn 'sqlx::test' rust-kit docs/rust \| grep -E '트랜잭션\|롤백' \| wc -l` → **7** | 6 줄 정정 (1 줄은 정정 후 자연 소멸) |
| F2 | Axum 0.8 발표일 오기 | `grep -rn '2024-12-01' rust-kit docs/rust \| wc -l` → **2** | 스킬 1 줄 정정 + 로그 1 줄 정정 주석 |
| F3 | 버전 전제 낡음 · 가드 부재 | `grep -rn '버전 현행성' rust-kit docs/rust \| wc -l` → **0** · `sea-orm 1.1` 표기 7 줄 · `sqlx 0.8` 표기 3 줄 | project-detection Step 2c 표 SSOT + 4 표면 인용 |
| J1 | `.unwrap()`/`.expect()` 제거 수단이 `?` 치환뿐 | `grep -rn 'smart constructor\|typestate\|NonEmpty\|HashMap::entry' rust-kit docs/rust \| wc -l` → **0** · `unwrap_used` 1 건(docs 한 줄, deny 선언 아님) · `expect_used`/`panic_in_result_fn` **0** | rust-error 타입 설계 절 + rust-init lint deny 5 종 (E1→E3) |
| J2 | 동시성 가드 판별력 조항 부재 | `grep -rn 'rows_affected' rust-kit \| wc -l` → **1** (MockDatabase 예제 코드) · `동시성 가드`/`낙관적` 조항 **0** | `references/concurrency-guard-protocol.md` SSOT + 5 표면 인용 |
| J2b | MockDatabase 의 **한계는 있으나 능력 범위가 없음** | rust-test Gotcha 28 이 "통합 테스트로 주장 금지" 만 서술 · `predicate` 토큰 **0 건** | 능력/한계 양면 명시 (rust-test · audit-criteria) |
| J3 | 테스트 타깃 열거 | `PKG_TARGETS`(project-detection Step 3a) · 무필터 기본 · `running N tests` 조항이 rust-run Gotcha 9 · rust-test Gotcha 31/32 · rust-preflight Gotcha 9 · audit row 15 에 **이미 존재** | **유지** — 신규 문장 추가하지 않고 guard SSOT 에서 재사용만 함 |

## 범위 경계

**구현 변경 경로 13 개.** 목록은 AR-01 의 기대 집합 한 곳에서만 열거한다
(§측정 커버리지 표기의 화이트리스트 규칙). 계약 파일 자신과 `.harness/**` 는 AR-01 pathspec 에서
제외한다.

- **건드리지 않는다**: `rust-kit/README.md` · `rust-kit/.claude-plugin/` · `rust-kit/evals/` ·
  `rust-kit/templates/**` · 다른 킷 전부 · `docs/superpowers/**` · `.claude/skills/**`.
  Phase 9 Scope 밖이다. `rust-kit/templates/rust-init.toml.template` 의 `sqlx = "0.8"` /
  `sea-orm = "1.1"` 은 Scope 밖이라 이번에 손대지 않고 downstream 으로 보고한다.
- **버전 번호를 지어내지 않는다.** evidence 파일에 실재하는 값(`axum 0.8.9` · `sqlx 0.9.0` ·
  `sea-orm 2.0.1` · `testcontainers 0.28.0` · `Rust 1.85.0`)만 쓴다 (AP-01).
- **강제 업그레이드 금지.** 버전 갱신은 "프로젝트에 고정된 버전이 우선" 가드와 함께만 착지한다.
- **넣지 않는다** (evidence 명시 금지): `unwrap_or_default` 대체 권고 · "더 좋은 메시지의 expect" ·
  broad `#[allow(...)]` · 전체 `clippy::restriction = deny` · 전체 repo mutation score 임계값.

## 회귀 게이트

- 정정 항목은 "새 서술 추가" 가 아니라 **잔존 0 건 증명**으로 판정한다.
- 모든 grep 오라클은 zsh · bash 양쪽에서 실행하고 출력이 같아야 한다 (DG-04).
- grep 오라클의 substring 오탐을 사전 확인한다 — `sqlx::test` 는 `#[sqlx::test(...)]` 코드 예제
  줄도 잡으므로 F1 오라클은 `트랜잭션|롤백` 과의 **교집합**으로 좁혔고, 정정된 줄은 교정 토큰
  (`새 테스트 DB`)을 반드시 포함하게 해 음성 대조를 성립시킨다.
- 열거값(조건 수 · 경로 수 · 토큰 수)은 타이핑하지 않고 명령으로 계산한다.

## Skill

- [ ] SK-01: `#[sqlx::test]` 를 트랜잭션/롤백으로 설명하는 줄이 `rust-kit/` · `docs/rust/`
      전체에서 0 건이다 [exact]
      (측정: `grep -rn 'sqlx::test' rust-kit docs/rust | grep -E '트랜잭션|롤백' | grep -v '새 테스트 DB' | wc -l` → `0` ·
       사전 출력 `7` 이 discriminating 근거 ·
       음성 대조: 정정 문장에서 `새 테스트 DB` 토큰을 지우면 이 측정이 FAIL 해야 한다)
- [ ] SK-02: `rust-kit/skills/rust-test/SKILL.md` 가 `#[sqlx::test]` 의 정정 3 요소를 모두
      서술한다 [exact, enumerated]
      (요소: `새 테스트 DB` · `migrations` 자동 적용 · 성공 시 `정리`(cleanup) ·
       측정: 세 토큰 각각 `grep -c` ≥ 1 + 본문 Read 확인)
- [ ] SK-03: MockDatabase 의 **능력 범위와 한계**가 `rust-kit/skills/rust-test/SKILL.md` 와
      `rust-kit/skills/rust-audit/references/audit-criteria.md` 2 파일에 모두 명시된다
      [exact, enumerated]
      (측정: 두 파일 각각에 `SQL predicate` 토큰과 `rows_affected` 토큰이 존재 —
       `grep -rln 'SQL predicate' rust-kit | LC_ALL=C sort` 결과가 그 2 행을 포함 ·
       한계 서술은 "실제 SQL predicate 의미 검증에는 쓸 수 없다" 취지여야 한다)
- [ ] SK-04: 동시성 가드 규칙 본문이 `rust-kit/references/concurrency-guard-protocol.md`
      1 개 파일에만 존재하고, 5 개 소비 표면이 각각 그 경로를 인용한다 [exact, enumerated]
      (측정: `grep -rln 'concurrency-guard-protocol' rust-kit | LC_ALL=C sort` 결과가
       `rust-kit/agents/rust-reviewer.md`,
       `rust-kit/references/concurrency-guard-protocol.md`,
       `rust-kit/skills/rust-audit/SKILL.md`,
       `rust-kit/skills/rust-audit/references/audit-criteria.md`,
       `rust-kit/skills/rust-model/SKILL.md`,
       `rust-kit/skills/rust-test/SKILL.md` 6 행과 정확히 일치)
- [ ] SK-05: 그 SSOT 가 가드 4 요소를 모두 담는다 [exact, enumerated]
      (요소: (a) 호출부를 **함수로 추출** · (b) `rows_affected == 0` → `Conflict` 반환 ·
       (c) positive test 와 **stale expected value** negative test 를 **실 DB**(`#[sqlx::test]`
       또는 testcontainers)에서 실행 · (d) 앱 레벨 read-check-then-write 대신 **SQL 술어**로 해소 ·
       측정: 네 토큰(`rows_affected == 0`, `stale`, `#[sqlx::test]`, `술어`) 각각 `grep -c` ≥ 1)
- [ ] SK-06: 그 SSOT 가 판별력 절차·임계값을 **재정의하지 않고 정본을 인용**한다 [exact]
      (측정: 파일에 `qa-evaluation-guide.md` 인용 1 건 이상 + `contract-schema.md` 인용 1 건 이상,
       그리고 자체 임계 숫자 정의문 0 건 —
       `grep -nE 'mutation score|임계값은|전체 repo' rust-kit/references/concurrency-guard-protocol.md | wc -l` → `0`)
- [ ] SK-07: `rust-kit/skills/rust-error/SKILL.md` 가 `.unwrap()`/`.expect()` 제거를 `?` 치환보다
      **타입 설계 제거 우선**으로 규정하고 수단 5 종을 열거한다 [exact, enumerated]
      (수단: `smart constructor` · `NonEmpty` · `typestate` · `builder` → `built` 분리 ·
       `HashMap::entry` 누적 · 측정: 다섯 토큰 각각 `grep -c` ≥ 1)
- [ ] SK-08: evidence 의 **넣지 말 것** 4 종이 금지 문구로 명시된다 [exact, enumerated]
      (대상: `unwrap_or_default` 로의 치환 · "더 좋은 메시지의 `expect`" · broad `#[allow(...)]` ·
       전체 `clippy::restriction` deny — 4 종 각각에 "하지 마라/금지" 취지 문구가
       `rust-kit/skills/rust-error/SKILL.md` 에 존재)
- [ ] SK-09: `rust-kit/skills/rust-init/SKILL.md` §4a `[workspace.lints.clippy]` 에 panic 계열
      deny lint 5 종이 선언된다 [exact, enumerated]
      (lint: `unwrap_used` · `expect_used` · `panic` · `panic_in_result_fn` ·
       `arc_with_non_send_sync` · 측정: 각 lint 가 `= "deny"` 와 같은 줄에 존재 —
       `grep -cE '^(unwrap_used|expect_used|panic|panic_in_result_fn|arc_with_non_send_sync) = "deny"' rust-kit/skills/rust-init/SKILL.md` → `5`)
- [ ] SK-10: 버전 현행성 표가 `rust-kit/references/project-detection.md` 1 곳에만 존재하고
      4 개 소비 표면이 그 Step 을 인용한다 [exact, enumerated]
      (측정: `grep -rln 'Step 2c' rust-kit | LC_ALL=C sort` 결과가
       `rust-kit/references/project-detection.md`,
       `rust-kit/skills/rust-audit/references/audit-criteria.md`,
       `rust-kit/skills/rust-init/SKILL.md`,
       `rust-kit/skills/rust-model/SKILL.md`,
       `rust-kit/skills/rust-test/SKILL.md` 5 행과 정확히 일치 ·
       표의 4 크레이트 버전 값은 evidence 파일과 문자 일치)
- [ ] SK-11: 신규 감사 rule(동시성 가드 음성 대조)이 rule 표 3 표면에 동일 개념으로 추가되고,
      두 표의 row 수 표기가 일치한다 [exact, enumerated]
      (표면: `rust-kit/skills/rust-audit/SKILL.md` Step 4 표 ·
       `rust-kit/skills/rust-audit/references/audit-criteria.md` §6 ·
       `rust-kit/agents/rust-reviewer.md` 출력 포맷 표 ·
       측정: `grep -c '^| 18 |' rust-kit/skills/rust-audit/SKILL.md rust-kit/agents/rust-reviewer.md`
       각각 `1` + `grep -rn '17-row' rust-kit | wc -l` → `0`)

## Error

- [ ] ER-01: Axum 0.8 발표일 `2024-12-01` 잔존이 0 건이다 [exact]
      (측정: `grep -rn '2024-12-01' rust-kit docs/rust | grep -v '정정 2026-08-13' | wc -l` → `0` ·
       사전 출력 `2` · 대체값 `2025-01-01` 은 evidence 인용값)
- [ ] ER-02: 버전 갱신이 **강제 업그레이드가 아니라 가드**로 착지한다 [exact]
      (측정: `rust-kit/references/project-detection.md` 에 "고정된 버전이 우선" 취지 문구 1 건 이상 +
       `grep -nE '업그레이드하라|반드시 최신으로' rust-kit/references/project-detection.md | wc -l` → `0`)
- [ ] ER-03: `docs/rust/fundamentals/testing.md` 의 `~5ms` 수치 행이 근거 없는 롤백 비용 주장을
      남기지 않는다 [exact]
      (측정: `grep -n '5ms' docs/rust/fundamentals/testing.md | grep -E '롤백' | wc -l` → `0` ·
       대체 서술은 새 수치를 지어내지 않고 "프로젝트에서 실측" 으로 남긴다)

## Architecture

- [ ] AR-01: 변경이 13 개 경로로 한정된다 [exact, enumerated]
      (Given: 커밋 직전 스테이징 완료 후 ·
       측정: `git diff --cached --name-only -- rust-kit docs ':(exclude).harness'` 결과가
       `docs/rust/fundamentals/error-handling.md`,
       `docs/rust/fundamentals/testing.md`,
       `docs/rust/research-log.md`,
       `rust-kit/agents/rust-reviewer.md`,
       `rust-kit/references/concurrency-guard-protocol.md`,
       `rust-kit/references/project-detection.md`,
       `rust-kit/skills/rust-api/SKILL.md`,
       `rust-kit/skills/rust-audit/SKILL.md`,
       `rust-kit/skills/rust-audit/references/audit-criteria.md`,
       `rust-kit/skills/rust-error/SKILL.md`,
       `rust-kit/skills/rust-init/SKILL.md`,
       `rust-kit/skills/rust-model/SKILL.md`,
       `rust-kit/skills/rust-test/SKILL.md` 13 행과 정확히 일치)
- [ ] AR-02: `docs/rust/research-log.md` 의 historical 오류 줄이 `[정정 2026-08-13]` 주석을
      달고 있다 [exact]
      (측정: `grep -n '2024-12-01-announcing-axum' docs/rust/research-log.md | grep -v '정정 2026-08-13' | wc -l` → `0` ·
       음성 대조: 주석을 지우면 이 측정이 FAIL 해야 한다)
- [ ] AR-03: `docs/rust/research-log.md` 최상단에 `## [2026-08-13] — Phase 9 kaizen` 라운드가
      추가되고 frontmatter `last_updated` 가 `2026-08-13` 이다 [exact]
      (측정: `grep -n '^## \[2026-08-13\] — Phase 9 kaizen' docs/rust/research-log.md` 1 건 +
       `grep -n '^last_updated: 2026-08-13' docs/rust/research-log.md` 1 건)

## Anti-patterns

- [ ] AP-01: 이번 커밋이 새로 도입한 버전 토큰·URL 이 전부 evidence 파일에 실재한다 [exact]
      (측정: `git diff --cached -U0` 추가 줄에서 뽑은 신규 `https://` URL 과 버전 리터럴 집합이
       `.harness/.meta/evidence/phase9.md` 또는 변경 전 본문에 실재 — 날조 0 건)
- [ ] AP-03: 변경 파일 전체에 bare code fence(``` 뒤 언어 힌트 없음)가 0 건이다 [exact]
      (측정: `python3 scripts/validate-plugin.py rust-kit` V6 OK +
       변경된 `docs/rust/*.md` 에서 bare fence 합계 0)

## Reusability

- [ ] RE-01: 5 개 소비 표면이 가드 규칙 본문을 재열거하지 않는다 [exact]
      (측정: `grep -rln 'rows_affected == 0' rust-kit | LC_ALL=C sort` 결과가
       `rust-kit/references/concurrency-guard-protocol.md` 1 행과 정확히 일치)
- [ ] RE-02: 버전 표가 두 곳에서 정의되지 않는다 [exact]
      (측정: `grep -rln '0\.9\.0' rust-kit | LC_ALL=C sort` 결과가
       `rust-kit/references/project-detection.md` 1 행과 정확히 일치)

## Diagnostics

- [ ] DG-01: `python3 scripts/validate-plugin.py rust-kit` 이 FAIL 0 으로 통과한다 [exact]
- [ ] DG-02: `python3 scripts/sync-docs.py --check-only` 가 rust-kit README 갱신을 요구하지 않는다 [exact]
- [ ] DG-04: 위 모든 grep 오라클을 zsh 와 bash 에서 실행한 출력이 동일하다 (diff 0) [exact]
