---
phase: 9
title: "Phase 9 rust-kit — 확보된 외부 근거"
collected: 2026-09-24
method: codex (foreground, 직접 호출 · gpt-5.6-sol · 조회는 curl/gh)
inputs: 처리 배정표(.claude/kaizen-input/insights-report.md)의 Phase 9 행 · phase-research-templates.md Phase 9 필수 출처 · 현행화 점검
note: 이 파일이 이 Phase 의 유일한 외부 근거다. 바깥 자료를 새로 찾지 마라. 여기 없는 URL·수치를 지어내지 마라. 없으면 미반영으로 남긴다.
---

요청 범위는 읽기 전용으로 조사했으며 파일은 변경하지 않았다. Context7 도구는 현재 환경에 없어 필수 항목 6개 모두 공식 문서·공식 저장소·crates.io로 대체 조회했다.

## 1. 출처 목록

### 공식 외부 출처

- Git
  - [`git status --porcelain`](https://git-scm.com/docs/git-status)
  - [`git merge-base`](https://git-scm.com/docs/git-merge-base)
  - [`git stash`](https://git-scm.com/docs/git-stash)
  - [`git worktree`](https://git-scm.com/docs/git-worktree)
- 시각 모델
  - [RFC 5545 §3.3.5 DATE-TIME](https://www.rfc-editor.org/rfc/rfc5545.html#section-3.3.5)
  - [PostgreSQL Date/Time Types](https://www.postgresql.org/docs/current/datatype-datetime.html)
  - [Chrono `DateTime`](https://docs.rs/chrono/latest/chrono/struct.DateTime.html)
  - [Chrono `NaiveTime`](https://docs.rs/chrono/latest/chrono/naive/struct.NaiveTime.html)
  - [SQLx PostgreSQL type mapping](https://docs.rs/sqlx/latest/sqlx/postgres/types/index.html)
  - [SeaORM 1.1 column types](https://github.com/SeaQL/seaql.github.io/blob/master/SeaORM/versioned_docs/version-1.1.x/04-generate-entity/03-column-types.md)
  - [SeaORM 2.x column types](https://github.com/SeaQL/seaql.github.io/blob/master/SeaORM/docs/04-generate-entity/03-column-types.md)
- 필수 rust-kit 소스
  - [Axum 0.8 발표](https://tokio.rs/blog/2025-01-01-announcing-axum-0-8-0)
  - [SQLx CHANGELOG](https://github.com/launchbadge/sqlx/blob/main/CHANGELOG.md)
  - [SeaORM MockDatabase](https://www.sea-ql.org/SeaORM/docs/write-test/mock/)
  - [tonic CHANGELOG](https://github.com/grpc/grpc-rust/blob/master/tonic/CHANGELOG.md)
  - [Rust Edition 2024 Guide](https://doc.rust-lang.org/edition-guide/rust-2024/index.html)
  - [Clippy CHANGELOG](https://github.com/rust-lang/rust-clippy/blob/master/CHANGELOG.md)
  - [Clippy lints index](https://rust-lang.github.io/rust-clippy/master/index.html)
- 최신 버전·breaking change
  - [Rust stable manifest](https://static.rust-lang.org/dist/channel-rust-stable.toml)
  - [SeaORM CHANGELOG](https://github.com/SeaQL/sea-orm/blob/master/CHANGELOG.md)
  - [tower-http CHANGELOG](https://github.com/tower-rs/tower-http/blob/master/tower-http/CHANGELOG.md)
  - [utoipa CHANGELOG](https://github.com/juhaku/utoipa/blob/master/utoipa/CHANGELOG.md)
  - [utoipa-scalar CHANGELOG](https://github.com/juhaku/utoipa/blob/master/utoipa-scalar/CHANGELOG.md)
  - crates.io API: [axum](https://crates.io/api/v1/crates/axum), [sqlx](https://crates.io/api/v1/crates/sqlx), [sea-orm](https://crates.io/api/v1/crates/sea-orm), [tonic](https://crates.io/api/v1/crates/tonic), [tower-http](https://crates.io/api/v1/crates/tower-http), [utoipa](https://crates.io/api/v1/crates/utoipa), [utoipa-scalar](https://crates.io/api/v1/crates/utoipa-scalar), [rust-i18n](https://crates.io/api/v1/crates/rust-i18n), [rstest](https://crates.io/api/v1/crates/rstest), [mockall](https://crates.io/api/v1/crates/mockall), [opentelemetry](https://crates.io/api/v1/crates/opentelemetry), [opentelemetry-otlp](https://crates.io/api/v1/crates/opentelemetry-otlp), [tracing-opentelemetry](https://crates.io/api/v1/crates/tracing-opentelemetry)

### 내부 ground truth

- [fit-pal Makefile](/Users/jackson/Hub/10_Dev/fit-pal/Makefile:108)
- [fit-pal Cargo.toml](/Users/jackson/Hub/10_Dev/fit-pal/server/Cargo.toml:35)
- [fit-pal server 지침](/Users/jackson/Hub/10_Dev/fit-pal/server/CLAUDE.md:167)
- [fit-pal 알림 설정](/Users/jackson/Hub/10_Dev/fit-pal/server/shared/config/src/lib.rs:250)
- [fit-pal wall-clock migration](/Users/jackson/Hub/10_Dev/fit-pal/server/migration/src/m20260916_000003_schedule_wall_clock.rs:1)

## 2. 항목별 관찰 사실

### backend-family:P4 — 실패 귀속

- `git status --porcelain`은 스크립트용으로 안정된 형식이며, 기본적으로 수정·추적되지 않은 파일을 보여준다. 따라서 실행 전후 dirty set을 기록하는 근거로 적합하다. 다만 Git은 파일의 “소유자”나 누가 수정했는지는 알려주지 않는다. [Git status](https://git-scm.com/docs/git-status)

- 반대 근거: 현재 시점의 status만 보고 “이번에 내가 안 건드린 파일”을 판정할 수 없다. 작업 시작 시 status 스냅샷과 이번 작업의 실제 write set이 있어야 한다.  
  **추론:** 시작 스냅샷 없이 실패 위치만으로 `남의 미커밋`이라 단정하면, 자신의 이전 변경·생성 파일·내 API 변경 때문에 남의 파일에서 난 후속 컴파일 오류를 오분류할 수 있다.

- `git merge-base HEAD <기본 브랜치>`는 두 커밋의 “best common ancestor”를 구한다. 복수 merge-base가 가능한 이력에서는 `--all` 없이 어느 하나가 반환될지는 명시되지 않는다. 기본 브랜치의 현재 tip이나 CI가 검사한 커밋 자체를 뜻하지는 않는다. [Git merge-base](https://git-scm.com/docs/git-merge-base)

- 따라서 기준 검사 기록은 반드시 계산된 SHA와 일치해야 한다. 기본 브랜치가 rebase된 저장소라면 실제 분기점을 원할 때 `--fork-point`가 후보지만, reflog 만료나 잘못된 upstream에서는 실패할 수 있다. [Git merge-base](https://git-scm.com/docs/git-merge-base)

- `git stash`는 작업 디렉터리와 index의 변경을 저장하고 작업 트리를 `HEAD`에 맞게 되돌린다. `-u`는 추적되지 않은 파일까지 정리하고, 복원 시 충돌할 수도 있다. 공유 작업 폴더에서 타인의 변경까지 움직일 위험이 있으므로 “stash 금지”는 공식 동작과 부합하는 안전 규칙이다. [Git stash](https://git-scm.com/docs/git-stash)

- 깨끗한 기준 검사는 별도 detached worktree가 적합하다. Git은 한 저장소에 여러 working tree를 붙여 서로 다른 커밋을 동시에 checkout할 수 있다고 명시한다. [Git worktree](https://git-scm.com/docs/git-worktree)

- fit-pal 실제 preflight는 `fmt → clippy → test` 순서다. [Makefile](/Users/jackson/Hub/10_Dev/fit-pal/Makefile:114)

### backend-family:P2 / rust-model — 순간과 벽시계

- RFC 5545는 local DATE-TIME에 `Z`와 `TZID`가 모두 없으면 “floating”으로 정의한다. 이 값은 어느 특정 시간대에도 묶이지 않고, 수신자가 현재 있는 시간대에서 같은 시·분·초로 해석한다. 반대로 대부분의 fixed time은 UTC 또는 local time + `TZID`로 전달하라고 한다. [RFC 5545 §3.3.5](https://www.rfc-editor.org/rfc/rfc5545.html#section-3.3.5)

- 반대 근거: 모든 반복 일정이 floating인 것은 아니다. “매주 월요일 뉴욕 지점 06:30”은 `06:30 + America/New_York` 의미이고, 수신자마다 06:30인 알람은 floating 의미다. RFC도 floating은 그 동작이 합리적인 경우에만 쓰라고 제한한다. [RFC 5545 §3.3.5](https://www.rfc-editor.org/rfc/rfc5545.html#section-3.3.5)

- PostgreSQL의 `timestamp without time zone`은 입력의 시간대 표시를 무시한다. `timestamptz`는 입력 순간을 UTC로 변환해 저장하지만 원래 IANA 시간대 이름은 보존하지 않는다. 따라서 DST가 적용되는 미래 반복 일정을 재계산하려면 wall-clock 값과 별도로 IANA TZID를 보관해야 한다. [PostgreSQL Date/Time Types](https://www.postgresql.org/docs/current/datatype-datetime.html)

- 고정 UTC offset 상수만으로는 DST 경계를 처리할 수 없다고 PostgreSQL 문서도 지적한다. 다만 단일 지역 서비스가 명시적으로 한 IANA zone만 사용하는 경우까지 무조건 실패시키는 근거는 없으므로 제안된 N/A 예외가 필요하다. [PostgreSQL Date/Time Types](https://www.postgresql.org/docs/current/datatype-datetime.html)

- Chrono는 `DateTime<Tz>`를 “time zone을 가진 ISO 8601 date/time”으로 정의한다. SQLx의 공식 PostgreSQL 매핑은 다음과 같다. [Chrono](https://docs.rs/chrono/latest/chrono/struct.DateTime.html), [SQLx types](https://docs.rs/sqlx/latest/sqlx/postgres/types/index.html)

  - `DateTime<Utc>` → `TIMESTAMPTZ`
  - `NaiveDateTime` → `TIMESTAMP`
  - `NaiveTime` → `TIME`

- 중요한 어긋남: SeaORM 1.1과 2.x 자동 매핑 표는 PostgreSQL `timestamp with time zone`에 `DateTimeWithTimeZone`, 즉 `chrono::DateTime<FixedOffset>`을 대응시킨다. `DateTimeUtc`는 SeaORM `Timestamp`에 대응하지만 PostgreSQL 열은 N/A로 표시한다. 따라서 “SeaORM에서도 `DateTime<Utc> + TIMESTAMPTZ`”라고 무조건 적으면 공식 표와 충돌한다. [SeaORM 1.1 mapping](https://github.com/SeaQL/seaql.github.io/blob/master/SeaORM/versioned_docs/version-1.1.x/04-generate-entity/03-column-types.md), [SeaORM 2.x mapping](https://github.com/SeaQL/seaql.github.io/blob/master/SeaORM/docs/04-generate-entity/03-column-types.md)

- **추론:** rust-model 문장은 SQLx 경로와 SeaORM 경로를 나눠야 한다. SeaORM에서는 `DateTimeWithTimeZone` 또는 명시적인 `TimestampWithTimeZone` column override를 확인하는 계약이 더 안전하다.

- 내부 ground truth에는 실제로 순간 컬럼을 `timestamp_with_time_zone()`으로 두는 사례와, 반복 일정의 local 값을 `groups.timezone`으로 되읽는 migration이 존재한다. 반면 알림 fallback에 `Asia/Seoul` 상수가 남아 있어 새 audit rule이 검출하려는 패턴도 실재한다. [설정](/Users/jackson/Hub/10_Dev/fit-pal/server/shared/config/src/lib.rs:255), [migration](/Users/jackson/Hub/10_Dev/fit-pal/server/migration/src/m20260916_000003_schedule_wall_clock.rs:63)

### 필수 rust-kit 소스 관찰

- Axum 0.8은 path를 `/:single`, `/*many`에서 `/{single}`, `/{*many}`로 바꿨고, custom `FromRequest`/`FromRequestParts` 구현에서 `#[async_trait]` 제거가 필요하다. 현행 rust-api 설명과 일치한다. [Axum 0.8 발표](https://tokio.rs/blog/2025-01-01-announcing-axum-0-8-0)

- SQLx 0.9는 PostgreSQL nullability 추론 개선을 위해 generic plan을 사용하지만 일부 `query!()` 출력 타입이 달라질 수 있다. `query*()` 함수도 `SqlSafeStr`을 요구하고, MSRV는 1.94이며, deprecated runtime+TLS 결합 feature를 삭제했다. rust-kit이 쓰는 분리형 `runtime-tokio` + `tls-rustls`는 삭제 대상 결합 feature가 아니다. [SQLx CHANGELOG](https://github.com/launchbadge/sqlx/blob/main/CHANGELOG.md)

- SeaORM MockDatabase는 실제 데이터가 없으므로 반환값과 실행 결과를 테스트가 주입한다. transaction log로 생성 statement는 검증할 수 있지만 실제 DB 의미 검증을 대체하지 못한다는 현재 rust-test 분류가 타당하다. [SeaORM MockDatabase](https://www.sea-ql.org/SeaORM/docs/write-test/mock/)

- tonic 최신 안정 계열은 0.14.6이고 Rust 2024/MSRV 1.88로 갱신됐다. rust-grpc의 0.14 본문은 최신 major와 맞지만 Gotcha의 health/reflection 0.13만 내부적으로 모순된다. [tonic CHANGELOG](https://github.com/grpc/grpc-rust/blob/master/tonic/CHANGELOG.md), [crates.io](https://crates.io/api/v1/crates/tonic)

- Edition 2024는 Rust 1.85에서 안정화됐다. 현재 문서의 edition 기준은 유효하다. [Edition Guide](https://doc.rust-lang.org/edition-guide/rust-2024/index.html)

- Rust 1.98 Clippy에는 `with_capacity_zero`, `unused_async_trait_impl` 등 새 pedantic lint가 추가됐고 `from_iter_instead_of_collect`은 deprecated됐다. workspace `pedantic = deny`는 새 lint가 추가될 때 기존 코드가 새로 실패할 수 있다는 뜻이다. [Clippy CHANGELOG](https://github.com/rust-lang/rust-clippy/blob/master/CHANGELOG.md)

## 3. 현행화 — 낡은 곳

2026-09-24 조회 기준이다.

| 파일:줄 | 현재 값 | 최신 안정 값 / 상태 | 판단·출처 |
|---|---|---|---|
| [project-detection.md:86](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/rust-kit/references/project-detection.md:86) | SeaORM 최신 `2.0.1` | `2.0.3` | “조회 시점 최신” 셀은 갱신 필요. [CHANGELOG](https://github.com/SeaQL/sea-orm/blob/master/CHANGELOG.md), [crates.io](https://crates.io/api/v1/crates/sea-orm) |
| [rust-grpc/SKILL.md:17](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/rust-kit/skills/rust-grpc/SKILL.md:17) | tonic-health/reflection `0.13` | `0.14.6` 계열 | 같은 파일 56–57행의 0.14와도 모순. [crates.io tonic-health](https://crates.io/api/v1/crates/tonic-health), [tonic-reflection](https://crates.io/api/v1/crates/tonic-reflection) |
| [rust-middleware/SKILL.md:14](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/rust-kit/skills/rust-middleware/SKILL.md:14), [:16](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/rust-kit/skills/rust-middleware/SKILL.md:16) | tower-http `0.6.x`를 안정 조합으로 단정 | `0.7.1` | 0.7은 compression·feature·redirect 동작에 breaking change가 있어 자동 치환은 금지하고 0.6/0.7 분기 필요. [CHANGELOG](https://github.com/tower-rs/tower-http/blob/master/tower-http/CHANGELOG.md) |
| [rust-init/SKILL.md:70](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/rust-kit/skills/rust-init/SKILL.md:70), [:191](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/rust-kit/skills/rust-init/SKILL.md:191), [template:37](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/rust-kit/templates/rust-init.toml.template:37) | utoipa `5.4` | `6.0.0` | YAML error type 변경 등 breaking change가 있어 신규 scaffold 후보만 갱신. [CHANGELOG](https://github.com/juhaku/utoipa/blob/master/utoipa/CHANGELOG.md) |
| [rust-init/SKILL.md:70](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/rust-kit/skills/rust-init/SKILL.md:70), [:192](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/rust-kit/skills/rust-init/SKILL.md:192), [template:38](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/rust-kit/templates/rust-init.toml.template:38) | utoipa-scalar `0.3` | `0.4.0` | utoipa 6 대응. changelog의 날짜 표기는 crates.io 게시 시각과 어긋나지만 버전은 일치한다. [CHANGELOG](https://github.com/juhaku/utoipa/blob/master/utoipa-scalar/CHANGELOG.md), [crates.io](https://crates.io/api/v1/crates/utoipa-scalar) |
| [audit-criteria.md:89](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/rust-kit/skills/rust-audit/references/audit-criteria.md:89) | `utoipa 5.4 docs` | `6.0.0` | 버전 고정 출처를 SSOT 참조로 교체할 대상. [utoipa CHANGELOG](https://github.com/juhaku/utoipa/blob/master/utoipa/CHANGELOG.md) |
| [rust-init/SKILL.md:72](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/rust-kit/skills/rust-init/SKILL.md:72), [:184](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/rust-kit/skills/rust-init/SKILL.md:184), [template:36](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/rust-kit/templates/rust-init.toml.template:36) | tower-http `0.6` | `0.7.1` | 신규 scaffold 기준은 재검토 필요; 기존 프로젝트 강제 업그레이드는 금지. [crates.io](https://crates.io/api/v1/crates/tower-http) |
| [rust-l10n/SKILL.md:54](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/rust-kit/skills/rust-l10n/SKILL.md:54), [rust-init/SKILL.md:73](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/rust-kit/skills/rust-init/SKILL.md:73) | rust-i18n `3` | `4.2.2` | major 차이이므로 API 확인 후 scaffold 갱신. [crates.io](https://crates.io/api/v1/crates/rust-i18n) |
| [rust-init/SKILL.md:74](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/rust-kit/skills/rust-init/SKILL.md:74) | tracing-otel `0.32`, OTel/OTLP `0.31` | `0.34.0`, `0.33.0`, `0.33.0` | 2026-09-18~23 갱신. [tracing-opentelemetry](https://crates.io/api/v1/crates/tracing-opentelemetry), [opentelemetry](https://crates.io/api/v1/crates/opentelemetry), [OTLP](https://crates.io/api/v1/crates/opentelemetry-otlp) |
| [rust-init/SKILL.md:75](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/rust-kit/skills/rust-init/SKILL.md:75) | mockall `0.13` | `0.15.0` | 신규 scaffold 후보 갱신. [crates.io](https://crates.io/api/v1/crates/mockall) |
| [rust-test/SKILL.md:24](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/rust-kit/skills/rust-test/SKILL.md:24) | rstest `0.26` | `0.27.0` | 2026-09-06 이후 낡음. [crates.io](https://crates.io/api/v1/crates/rstest) |
| [rust-init/SKILL.md:93](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/rust-kit/skills/rust-init/SKILL.md:93), [:252](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/rust-kit/skills/rust-init/SKILL.md:252), [template:11](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/insights-0924-kaizen/rust-kit/templates/rust-init.toml.template:11) | 고정 예시 `1.88.0` | stable `1.98.1` | 고정 pin 자체는 오류가 아니지만 “2026 최신 Clippy” 기준과 함께 쓰면 새 lint를 놓친다. 최신 pin 또는 `stable` 선택 규칙 필요. [stable manifest](https://static.rust-lang.org/dist/channel-rust-stable.toml) |

현재 값과 일치하거나 의도적으로 유지할 항목:

- Axum 최신 `0.8.9`; 문서의 `0.8` 범위는 유효하다. [crates.io](https://crates.io/api/v1/crates/axum)
- SQLx 최신 `0.9.0`; project-detection 표는 이미 맞는다. 0.8 예시는 구-major 호환 경로이므로 자동 교체하면 안 된다. [crates.io](https://crates.io/api/v1/crates/sqlx)
- tonic 최신 `0.14.6`; 본문 `0.14`는 유효하다. [crates.io](https://crates.io/api/v1/crates/tonic)
- testcontainers `0.28.0`, proptest `1.11.0`은 현행이다. [testcontainers](https://crates.io/api/v1/crates/testcontainers), [proptest](https://crates.io/api/v1/crates/proptest)

## 4. 권장안

1. rust-preflight Gotcha 10은 제안 제목대로 추가하되, 판정 입력을 명시한다.

   - 시작 시 `git status --porcelain=v1 -z --untracked-files=all` 스냅샷
   - 이번 작업에서 실제로 쓴 파일 목록
   - 실패 diagnostic의 primary span과 dependency chain
   - 정확한 기준 SHA 및 검사 환경

2. `남의 미커밋`은 “현재 dirty인데 내 write set에 없음”만으로 확정하지 말고, 시작 스냅샷에도 있었고 내 변경의 후속 오류가 아님을 확인한 경우로 제한한다. 그렇지 않으면 `[미검증] 귀속 불명`이 안전하다.

3. 기준 커밋 재검사는 stash가 아니라 임시 detached worktree에서 한다. exact merge-base SHA, toolchain, feature, 환경변수, DB migration 상태를 함께 기록해야 결과 비교가 유효하다.

4. Step 5 Details의 원인 enum은 요구한 세 값을 유지하되, 증거 필드를 붙인다.

   - `내 변경 — {내 변경 파일:줄 또는 diff}`
   - `남의 미커밋 — {시작 status 항목 + 실패 파일:줄}`
   - `기준 커밋에서 이미 실패 — {baseline SHA + 명령 + exit}`
   - 판정 불가능성을 숨기지 않으려면 별도 상태 `[미검증]`도 허용하는 편이 낫다.

5. 시각 계약은 2분류가 아니라 실제로는 다음 3형태를 구분해야 한다.

   - 순간: UTC instant
   - floating wall-clock: 수신자마다 같은 현지 시각
   - zone-anchored wall-clock: local date/time + IANA TZID

6. rust-model 문구는 ORM별로 나눈다.

   - SQLx: `DateTime<Utc> ↔ TIMESTAMPTZ`, `NaiveDateTime ↔ TIMESTAMP`, `NaiveTime ↔ TIME`
   - SeaORM: `DateTimeWithTimeZone/FixedOffset ↔ TimestampWithTimeZone`; UTC 도메인 타입을 쓸 경우 명시적 column mapping과 실제 컴파일 검증 요구
   - 반복 일정이 특정 지역에 묶이면 naive 값과 IANA TZID를 함께 저장
   - 새 일반 규칙 문장에는 지시대로 특정 프로젝트 이름을 넣지 않는다.

7. audit rule은 “wall-clock을 순간으로만 저장”뿐 아니라 “zone-anchored 일정인데 IANA TZID가 없음”도 FAIL 조건에 포함해야 DST 오류까지 막을 수 있다. 단일 지역 서비스 예외는 명시적 서비스 계약과 IANA zone 근거가 있을 때만 N/A로 한다.

8. 버전 리터럴은 `project-detection.md`를 실질적 SSOT로 만들고 다른 스킬·템플릿은 major 호환 분기나 SSOT 참조만 두는 편이 드리프트를 줄인다.

## 5. 못 가져온 것 / 열린 질문

- Context7는 현재 도구 목록에 없어 조회하지 못했다. 공식 원문 fallback으로 Axum, SQLx, SeaORM, tonic, Edition Guide, Clippy를 모두 직접 조회했다.
- Git 공식 문서는 working-tree 상태를 설명하지만 “누가 변경했는지”는 제공하지 않는다. `남의 미커밋` 판정에는 별도 시작 스냅샷 또는 작업 소유권 기록이 필요하다.
- 실패 diagnostic이 dirty 파일을 가리킨다는 사실만으로 원인 귀속이 가능하다는 1차 출처는 찾지 못했다. 이는 컴파일 의존관계를 추가 분석해야 하는 추론 영역이다.
- SeaORM 공식 타입 표와 요구된 `DateTime<Utc> + TIMESTAMPTZ` 단일 문장이 어긋난다. Phase 구현 전에 SeaORM 1.1/2.x에서 사용할 정확한 entity attribute 또는 adapter 변환 방식을 컴파일 테스트로 확정해야 한다.
- utoipa-scalar 0.4 changelog의 날짜 표기와 crates.io 게시 시각이 어긋난다. 버전 `0.4.0`은 양쪽에서 일치한다.
