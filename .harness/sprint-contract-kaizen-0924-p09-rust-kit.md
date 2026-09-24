---
feature: "카이젠 2026-09-24 Phase 9 계약 — preflight 실패 원인 셋 · 시각 종류별 Rust 타입 · 미검증 정본 재동기화 · 버전 현행화"
slug: kaizen-0924-p09-rust-kit
created: "2026-09-25 07:14"
complexity: "복잡"
conditions: 30
status: active
owner_session: de8c7935-a5b6-4df5-9106-fafa73c288a0
conditions_digest: sha256:6b5ad48a301bc7e4
locked_at: "2026-09-25 08:01"
---

## 배경

이 Phase 의 외부 근거는 `.harness/.meta/evidence/phase9.md` 하나다. 처리 배정표(`.claude/kaizen-input/insights-report.md`)에서 `배정` 칸이
`Phase 9` 인 행은 `backend-family:P4` 하나이고, `backend-family:P2`(Phase 7 행) 비고가 「rust-model 부분은 Phase 9 와 맞춘다」 다.
러닝북 `Phase 별 추가 과제` 에 Phase 9 줄은 없다. 앞 Phase notes 가 Phase 9 로 넘긴 줄은 셋이다. 오케스트레이터 Step 9 는 「Phase 1 에서 설계 가이드가
변경되었으면 rust-kit 전 스킬을 전수 감사한다」 고 적는다 — 그 감사에서 둘을 더 찾았다.

| 키 · 출처 | 내용 | 이번 처리 |
| --- | --- | --- |
| `backend-family:P4` | rust-preflight 실패를 내 변경 · 남의 미커밋 · 기준 커밋에서 이미 실패로 가른다. 비고: 기준 커밋 가르기 규칙 세 곳을 하나로 정한다 | 반영 — SK-01 ~ SK-04. 규칙은 Phase 4 가 `/sprint` Step 3 하나로 정했다 — 판정 세 줄을 글자 그대로 옮긴다(SK-02) |
| `F09` (Phase 4 행) | 비고 「기준 커밋 가르기 규칙이 harness:P07 · backend-family:P3(Phase 8) · backend-family:P4(Phase 9) 세 곳」 | Phase 4 가 정한 정본을 따른다. preflight 는 커밋 전에 돌아 미커밋 변경에 내 것도 섞이므로 `HEAD` 에 내 파일만 얹는 한 번을 더한다(근거 파일 §4 권장 1 · 2) |
| `phase4-notes.md` 넘김 표 | 「`backend-family:P3` · `backend-family:P4` — Phase 8 · 9 — `/sprint` Step 3 의 판정 세 줄을 옮겨 적는다. 플러그인이 따로 설치돼 경로로 가리킬 수 없다」 | 반영 — SK-02 · SK-03 |
| `backend-family:P2` 의 rust-model 부분 · `phase7-notes.md` 넘김 표 | 「타입 대응을 ORM 별로 나눈다 — SQLx 는 `DateTime<Utc>` + `TIMESTAMPTZ`, SeaORM Entity 는 `DateTimeWithTimeZone`. `rust-model/SKILL.md:90` 에 시각 종류 구분」 | 반영 — SK-05 ~ SK-07. 원칙 본문은 Phase 7 의 `docs/backend/fundamentals/database.md` 원칙 10 이고, 이 Phase 는 Rust 타입 대응만 `docs/rust/data/sqlx-patterns.md` 원칙 6 에 둔다 |
| `phase1-notes.md` 넘김 표 | 「`rust-kit/agents/rust-reviewer.md:137` — agent-design-guide §10 을 인용하며 접미 없는 `[미검증]`」 | 반영 — SK-09. 전수 감사에서 같은 옛 꼴이 다섯 자리 더 있었다(rust-audit Gotcha 14 · rust-run · rust-preflight 두 자리 · rust-test) |
| 편집 전 감사 (`rust-kit/agents/rust-reviewer.md:44-65`) | 「정본을 문구 변형 없이 복제」 라는 §미검증 증거 프로토콜이 정본의 2026-08-13 개정(카운터 둘 · 남용 방지 4 요건) 전 판이다. `:93` 이 「미검증 프로토콜의 4 요건」 을 가리키는데 그 4 요건이 이 파일에 없다. backend · infra reviewer 는 이미 옮겼다 | 반영 — SK-08 · SK-10. 정본 조항 1 의 N/A 표와 정본의 새 조항 2 는 옮기지 않는다 — backend · infra 사본과 같고, Phase 8 이 그 둘을 다음 사이클 Phase 3 으로 넘겼다 |
| 편집 전 감사 (`rust-kit/skills/rust-audit/SKILL.md:29`) | Gotcha 14 「미검증 2 건 이상은 CONDITIONAL APPROVE 규칙을 적용한다 (Step 4 참조)」 — 같은 파일 Step 5 는 「2 건 이상은 REJECT」 다. 판정은 Step 4 가 아니라 Step 5 에 있다 | 반영 — SK-09 · SK-10 |
| 근거 파일 §3 현행화 | SeaORM 2.0.1 → 2.0.3 · rust-grpc Gotcha 5 의 `0.13` 이 같은 파일 본문 0.14 와 어긋남 · tower-http 0.7.1 · utoipa 6.0.0 · rust-i18n 4.2.2 · OTel 0.33 · mockall 0.15.0 · rstest 0.27.0 · Rust stable 1.98.1 | 반영 — SK-11. 버전 값은 `rust-kit/references/project-detection.md` Step 2c 표(이 킷의 버전 값 자리)에만 적는다. 스킬 본문 · 템플릿의 리터럴은 breaking change 가 있어 그대로 둔다(근거 파일 §3 「자동 치환 금지」) — 넘김(ER-03) |

글로벌 평가 피드백(`~/.harness/feedback/evaluator/`)에서 rust-kit 을 가리킨 기록 가운데 2026-08-14 REJECT 가 reviewer 정본 복제 누락이었다
(「Phase 3 canonical User-Reported Failure Protocol 이 … rust-kit reviewer … 에 전혀 인용되지 않음」). 그 절은 지금 rust-reviewer 에 있다. 같은 모양 — 정본은 바뀌었는데
사본이 옛 판으로 남는 것 — 이 이번에 미검증 프로토콜에서 다시 보였다. 그래서 SK-08 은 낱말이 아니라 조항 본문 전체를 정본과 글자 단위로 비교한다.

rust-kaizen Gotcha 3 의 상한(한 세션 3 ~ 4 관심사)에 맞춰 넷으로 묶는다 — (1) preflight 실패 원인 셋(SK-01 ~ SK-04) (2) 시각 종류별 Rust 타입(SK-05 ~ SK-07)
(3) 미검증 표기를 현행 정본에 맞춤(SK-08 ~ SK-10) (4) 현행화(SK-11). research-log(SK-12)는 넷을 기록한다. 각 관심사가 여러 파일을 건드리지만 한 관심사 안의 형제 대칭이다.

## 리서치 소스

외부 조회 0 회. 아래 URL 은 전부 근거 파일 `.harness/.meta/evidence/phase9.md` 에서 가져왔다. Context7 도구는 이 세션에 없어 쓰지 않았다 — 대신 로컬에 받아 둔 크레이트로
실제 컴파일해 타입 대응을 쟀다(아래 내부 실측).

- [git status](https://git-scm.com/docs/git-status) — `--porcelain` 은 스크립트용 안정 형식이다. 누가 고쳤는지는 알려주지 않는다 — 시작 때 목록이 있어야 남의 미커밋을 가를 수 있다 (SK-02)
- [git merge-base](https://git-scm.com/docs/git-merge-base) — 두 커밋의 공통 조상이지 기준 가지의 지금 상태가 아니다 (SK-02)
- [git stash](https://git-scm.com/docs/git-stash) — 작업 폴더와 목록을 `HEAD` 로 되돌린다. 공유 작업 폴더에서는 남의 변경까지 옮긴다 (SK-01)
- [git worktree](https://git-scm.com/docs/git-worktree) — 한 저장소에 여러 작업 폴더를 붙여 서로 다른 커밋을 동시에 꺼낸다 (SK-02)
- [Clippy CHANGELOG](https://github.com/rust-lang/rust-clippy/blob/master/CHANGELOG.md) — Rust 1.98 에 새 pedantic lint 가 더해졌다. workspace lint 를 `deny` 로 두면 toolchain 이 오를 때 기준 커밋도 새로 실패한다 (SK-02)
- [SQLx PostgreSQL types](https://docs.rs/sqlx/latest/sqlx/postgres/types/index.html) — `DateTime<Utc>` ↔ `TIMESTAMPTZ` · `NaiveDateTime` ↔ `TIMESTAMP` · `NaiveTime` ↔ `TIME` (SK-05 · SK-06)
- [SeaORM 1.1 column types](https://github.com/SeaQL/seaql.github.io/blob/master/SeaORM/versioned_docs/version-1.1.x/04-generate-entity/03-column-types.md) · [SeaORM 2.x column types](https://github.com/SeaQL/seaql.github.io/blob/master/SeaORM/docs/04-generate-entity/03-column-types.md) — Entity 생성기는 `timestamp with time zone` 에 `DateTimeWithTimeZone`(`DateTime<FixedOffset>`)을 붙인다 (SK-05 · SK-06)
- [Chrono DateTime](https://docs.rs/chrono/latest/chrono/struct.DateTime.html) · [PostgreSQL Date/Time Types](https://www.postgresql.org/docs/current/datatype-datetime.html) · [RFC 5545 §3.3.5](https://www.rfc-editor.org/rfc/rfc5545.html#section-3.3.5) — `TIMESTAMPTZ` 는 원래 시간대 이름을 남기지 않는다 (SK-05)
- [tower-http CHANGELOG](https://github.com/tower-rs/tower-http/blob/master/tower-http/CHANGELOG.md) · [utoipa CHANGELOG](https://github.com/juhaku/utoipa/blob/master/utoipa/CHANGELOG.md) · crates.io API(근거 파일 §1) — 버전 값 (SK-11)

근거 파일이 스스로 밝힌 한계를 그대로 옮긴다. 실패 진단이 남의 미커밋 파일을 가리킨다는 사실만으로 원인을 정할 수 있다는 1 차 출처는 없다(§5) — 그래서 새 문장은
확정에 세 조건을 걸고, 하나라도 못 확인하면 `[미검증]` 으로 적게 한다. SeaORM 공식 표와 「SeaORM 도 `DateTime<Utc>` + `TIMESTAMPTZ`」 한 줄이 어긋나며 컴파일로 확정해야
한다고 적었다(§5) — 아래 내부 실측이 그 확인이다. SeaORM 2.x 는 로컬에 크레이트가 없어 재지 못했다.

내부 실측(2026-09-25, 오프라인 컴파일 · rustc 1.96.0 · sea-orm 1.1.19 · sqlx 0.8.6 · chrono 0.4.44 — 스크래치 `p9d/ct/`): SeaORM Entity 필드의 열 타입 추론은
`DateTimeWithTimeZone` · `DateTimeUtc` → `TimestampWithTimeZone`, `DateTime` → `DateTime`, `Time` → `Time`. SQLx 는 `DateTime<Utc>` → `TIMESTAMPTZ`, `NaiveDateTime` → `TIMESTAMP`,
`NaiveTime` → `TIME`, `DateTime<FixedOffset>` → `TIMESTAMPTZ`. 같은 크레이트로 컴파일되는 로컬 Rust 서버 프로젝트의 SeaORM Entity 는 순간 필드 94 개가 전부
`DateTimeWithTimeZone` 이고(`DateTimeUtc` 0 개), 벽시계 필드는 `DateTime` 셋 · `chrono::NaiveTime` 둘, 시간대 이름은 `String` 둘이었다 — 생성기가 만든 Entity 가 실제로 그 타입을 쓴다.

내부 입력: 데이터 풀 §0 처리 배정표 · §0-b `e863512e`(2026-09-18 — 다른 세션들이 깬 공용 개발 가지의 빨간 검사를 몇 시간 쫓았고, 사용자가 먼저 워크트리를 제안했다) ·
§0.5 [backend] · [infra] 의 공유 작업 폴더 메모(`미분류` — 배경으로만 읽었다) · §1 글로벌 평가 피드백(위 배경).

## GAP 분석 · 개선안 초안

### 1.1 복잡도 4 축

| 축 | 물음 | 값 |
| -- | ---- | -- |
| 레이어 수 | 몇 개 계층을 관통하는가 | 4 — 원칙 문서(`docs/rust/`) · 스킬 여섯 · 평가 에이전트와 참조 문서 · 평가 사례 데이터 |
| 공개 API·계약 변경 | 외부에 노출된 형태가 바뀌는가 | 예 — rust-reviewer 의 판정 형식이 카운터 둘 · BLOCKED 로 바뀌고 rust-audit 가 그 형식을 받는다. rust-preflight 리포트의 FAIL 행 Details 머리가 정해진다. rust-model SeaORM 예시의 순간 타입이 바뀐다 |
| 소비면 존재 | 이 형태를 받아 쓰는 반대편이 있는가 | 예 — 아래 Counterpart 표 |
| 회귀 위험 | 기존 동작이 깨질 수 있는가 | 예 — rust-kaizen Gotcha 9 회귀 검사가 rust-preflight · rust-test · rust-run 문장을 센다. reviewer 사본은 정본과 한 글자도 달라지면 안 된다. Gotcha 를 가운데 끼우면 번호로 가리키는 자리(rust-preflight Step 5 → Gotcha 8)가 어긋난다 |

네 축이 모두 「예」 이고 공개 형태 변경과 소비면이 둘 다 「예」 라 **복잡**이다. Step 2.5 Counterpart 조건을 넣는다(AR-02 · SK-10).
기능 조건은 20 개다 — 복잡 9 ~ 20 안이다 (sprint-contract Step 6.2 둘째 명령으로 이 파일을 세면 20).

### 1.2 설정 리터럴 대조표

| config key | project.yaml 에서 읽은 값 | 계약에 쓴 값 |
| ---------- | ------------------------- | ------------ |
| `commands.analyze` | `bash -n scripts/release.sh` | DG-01 N/A 사유에 그대로 |
| `commands.test` | `bash scripts/release.sh 2>&1 \|\| true` | DG-03 N/A 사유에 그대로 |
| `diagnostics.ide_exclude` | `[]` | DG-02 에 그대로 |
| `contract_categories[].id` / `prefix` | `Skill`/`SK` · `Script`/`SC` · `Error`/`ER` · `Architecture`/`AR` | 조건 섹션 제목과 접두 그대로 |
| `anti_patterns[].id` / `message` | AP-01 · AP-02 · AP-03 · AP-04 | AP-01 · AP-03 · AP-04 선별, message 원문 그대로. AP-02(force push)는 이 Phase 가 밀어 넣지 않아 뺀다 |

### 1.4 편집 전 감사 (실제로 읽은 줄 — 시작 커밋 `4a8ec55` 판)

| 대상 파일 | 실제 Read 증거 (`파일:라인`) | 발견한 기존 갭·위반 | 계약 조건화 |
| --------- | ---------------------------- | ------------------- | ----------- |
| `rust-kit/skills/rust-preflight/SKILL.md` | `:13-23` (Gotcha 1 ~ 9) · `:52-56` (Step 2 FAIL) · `:58-76` (Step 2.5 · `:75` `[미검증] DB 미기동`) · `:78-83` (Step 3) · `:85` (Step 4) · `:93-106` (리포트 · `:105` 「사유를 Details 에 남긴다」) | 빨간 검사의 원인을 가르는 절차 0 건 · 옛 미검증 꼴 둘 | SK-01 ~ SK-03 · SK-09 |
| `harness/skills/sprint/SKILL.md` | `:87-120` (Step 3 — 코드 블록 · 판정 표 `:113-115`) | 없음 — 정본. 읽기만 | SK-02 (글자 비교) |
| `rust-kit/skills/rust-run/SKILL.md` | `:80-94` (결과 형식 · `:91` `[미검증] 종료 코드 캡처 실패 — 재실행 필요`) | 옛 미검증 꼴 | SK-09 |
| `rust-kit/skills/rust-test/SKILL.md` | `:350-362` (After Creation · `:359` `[미검증] 테스트 미실행`) · `:24` (rstest 0.26) | 옛 미검증 꼴. 「실행하지 않았으면 `[미검증]`」 은 정본 조항 2(의도적 미실행은 FAIL)와 어긋난다 | SK-09 · SK-11 (`:24` 는 그대로) |
| `rust-kit/agents/rust-reviewer.md` | `:28-42` (Evidence Validity Gate) · `:44-65` (§미검증 증거 프로토콜 — 옛 판) · `:91-96` (`:93` 「4 요건」 가리킴) · `:137` (미검증 마커) · `:139-154` (최종 판정 · Evidence Validity 줄) | 정본 복제가 2026-08-13 개정 전 판 · 가리키는 4 요건이 없음 · 옛 마커 · 단일 카운터 판정 | SK-08 · SK-09 · SK-10 |
| `rust-kit/skills/rust-audit/SKILL.md` | `:29` (Gotcha 14) · `:30` (Gotcha 15) · `:118-135` (Step 5 최종 판정) | 옛 마커 · Step 5 와 반대인 「2 건 이상 CONDITIONAL」 · 없는 Step 4 가리킴 · 단일 카운터 판정 | SK-09 · SK-10 |
| `backend-kit/skills/backend-audit/SKILL.md` | `:25` (Gotcha 11) · `:106-118` (Step 4 최종 판정) | 없음 — 형제 기준(rust-audit Gotcha 17 이 parity 를 요구). 읽기만 | SK-10 (같은 문장 두 줄) |
| `backend-kit/agents/backend-reviewer.md` · `infra-kit/agents/infra-reviewer.md` | `:70-121` · `:69-110` (정본 사본 · 4 요건 사본) | 없음 — 형제 사본. 읽기만 | SK-08 (4 요건 글자 비교) |
| `harness/docs/guides/qa-evaluation-guide.md` | §Canonical Unverified-Evidence Protocol (조항 1 · 새 조항 2 · 번호 3 이 둘 · 4 · 5) | 없음 — 정본. 읽기만. 조항 번호 3 중복은 정본 쪽 몫 | SK-08 (조항 본문 글자 비교) |
| `rust-kit/skills/rust-model/SKILL.md` | `:11-34` (Gotchas — 마지막 `:34`) · `:73-80` (Step 1 입력 표) · `:86-92` (Step 2 · `:90` 타임스탬프 타입) · `:221-310` (§4S — `:228` `use chrono::{DateTime, Utc};` · `:238` `DateTime<Utc>` · `:289` · `:304`) · `:326-343` (§5 도메인 모델) | 시각 종류 구분 0 건 · SeaORM 예시가 생성기와 다른 순간 타입을 쓴다 — 생성기가 만든 Entity 에 이 어댑터를 붙이면 `:289` 가 타입 불일치로 컴파일되지 않는다(SK-07 섞은 판 실측) | SK-06 · SK-07 |
| `docs/rust/data/sqlx-patterns.md` | `:1-5` (머리 설정) · `:52-80` (원칙 2 · 3) · `:114-127` (원칙 5) · `:129-137` (수치 기준) · `:141-155` (안티패턴) | 시각 종류별 타입 원칙 0 건. rust-kaizen Gotcha 1 이 원칙 문서 없는 개선을 막는다 | SK-05 |
| `docs/backend/fundamentals/database.md` | `:138` (`### 10. 시각은 종류부터 나누고, 종류마다 저장 형태를 정한다`) | 없음 — Phase 7 의 정본. 읽기만 | AR-02 |
| `rust-kit/references/project-detection.md` | `:77-99` (Step 2c 표 · 해석 규칙) | 조회일 2026-08-13 · SeaORM 2.0.1 · 근거 파일이 짚은 크레이트 여덟이 표에 없다 | SK-11 |
| `rust-kit/skills/rust-grpc/SKILL.md` | `:17` (Gotcha 5 `0.13`) · `:50-60` (의존성 예시 0.14) | 같은 파일 안 모순 | SK-11 |
| `rust-kit/skills/rust-init/SKILL.md` · `rust-kit/skills/rust-middleware/SKILL.md` · `rust-kit/skills/rust-l10n/SKILL.md` · `rust-kit/templates/rust-init.toml.template` | `:70-75` · `:93` · `:184-192` · `:252-257` · `:14` · `:16` · `:54` · `:11` · `:36-38` | 버전 리터럴이 Step 2c 밖에 흩어져 있다(Step 2c 는 자기를 유일한 자리라고 적는다). breaking change 가 있어 이번에 바꾸지 않는다 | ER-03 넘김 · SK-11 이 표의 전제 값이 이 파일들에 실제로 있는지 잰다 |
| `rust-kit/evals/evals.json` | `:1-5` · `:174-186` (사례 16 — 마지막) | 사례 16 개, rust-preflight 사례는 하나(`:15`) | SK-04 |
| `docs/rust/research-log.md` | `:1-8` (1.2.0 · 2026-08-13 · 첫 항목) | 이번 항목 없음 | SK-12 |
| `.claude/skills/rust-kaizen/SKILL.md` | Gotcha 6 형제 표 · Gotcha 9 회귀 검사 | 레포 전용 파일이라 이 Phase 범위 밖. Gotcha 9 의 AR-02 검사(`grep -rn … .`)는 자기 파일을 잡아 늘 2 다 | ER-03 넘김 · ER-04 가 나머지 검사를 잰다 |

후보 옵션은 하나로 정했다 — 실패 원인 규칙을 어디에 둘지 (가) rust-preflight Gotcha 10 + Step 3.5 (나) `docs/rust/ops/ci-cd.md` 원칙 + 스킬 가리킴 (다) rust-run.
(가)를 고른다. 처리 배정표 제안이 rust-preflight 를 이름으로 짚었고, 판정 정본은 이미 `/sprint` Step 3 이라 원칙 문서를 하나 더 두면 세 번째 사본이 된다.
rust-run 은 명령 하나를 돌리는 도구라 원인을 가를 자리가 아니다. Gotcha 는 번호를 밀지 않도록 맨 끝(10)에, 절차는 Step 3 과 4 사이(3.5)에 둔다.

### Counterpart — 바뀌는 형식을 받아 쓰는 반대편

| 면 | 파일 | 바뀌는 것 | 이번 처리 |
| --- | --- | --- | --- |
| producer | `rust-kit/agents/rust-reviewer.md` | 판정 형식 — 카운터 둘 · BLOCKED · 미검증 네 칸 | SK-08 ~ SK-10 |
| consumer | `rust-kit/skills/rust-audit/SKILL.md` | deep 모드에서 reviewer 결과를 받아 Step 5 로 판정한다 | SK-09 · SK-10 — 같은 문장으로 맞춘다. backend-audit 와도 같은 두 문장(SK-10) |
| producer | `harness/skills/sprint/SKILL.md` Step 3 | 판정 세 줄(정본) | 고치지 않는다 — SK-02 가 글자 그대로인지 잰다 |
| consumer | `rust-kit/skills/rust-preflight/SKILL.md` | 판정 세 줄 사본 · 리포트 FAIL 행 머리 | SK-01 ~ SK-03 |
| consumer (Phase 8) | `docs/infra/platform/cicd.md` · `infra-kit/skills/infra-guide/SKILL.md` | 같은 판정 세 줄 사본 | Phase 8 몫 — 이 Phase 는 건드리지 않는다(ER-03 셋째 값) |
| producer | `docs/rust/data/sqlx-patterns.md` 원칙 6 | 시각 종류별 Rust 타입 대응 | SK-05 |
| consumer | `rust-kit/skills/rust-model/SKILL.md` | Gotcha · 입력 표 · §4S 예시 | SK-06 · SK-07 · AR-02 |
| producer | `rust-kit/references/project-detection.md` Step 2c | 버전 표 | SK-11 |
| consumer | `rust-kit/skills/rust-grpc/SKILL.md` · `rust-kit/skills/rust-model/SKILL.md` §0a | Step 2c 를 가리킨다 | rust-grpc 는 SK-11, rust-model §0a 는 고치지 않는다 — AR-02 가 제목이 그대로인지 잰다 |
| consumer (다음 사이클) | `rust-kit/skills/rust-init/SKILL.md` 등 버전 리터럴 넷 | Step 2c 참조로 바꾸기 | 명시적 미완 — ER-03 |
| consumer (Final) | `docs/rust-kit/sqlx-patterns.html` | 원칙 6 이 없다 | 명시적 미완 — Final F2 재생성(ER-03) |

### 개선안 초안

치환 서른셋을 글자 그대로 적은 모의 스크립트가
`/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/de8c7935-a5b6-4df5-9106-fafa73c288a0/scratchpad/p9d/mock.py` 에 있다.
옛 문자열이 정확히 한 번 있어야 치환하고 끝에 `mock applied 33` 을 낸다. BUILD 는 이 치환을 글자 그대로 옮긴다 — 조건이 문장을 글자 그대로 센다.
BUILD 가 쓰는 판은 이것을 복사해 2 회차 검토 권장 1 한 곳(rust-preflight Step 3.5 셋째 항목 첫머리 「- 통과하는데」 → 「- `HEAD+내 변경` 이 통과하는데」)만 고친
`/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/de8c7935-a5b6-4df5-9106-fafa73c288a0/scratchpad/p9b/mock.py` 다.
파일마다 요지:

1. `rust-kit/skills/rust-preflight/SKILL.md` — Gotcha 10 (E2), Step 2 · 3 FAIL 줄에 Step 3.5 가리킴, Step 3.5 (임시 워크트리 세 곳 · 판정 세 줄 · `HEAD` 에 내 파일만 얹는 한 번과 그 블록을 쓰는 때 ·
   `HEAD` 임시가 실패할 때 가르는 법 · 남의 미커밋 확정 세 조건 · toolchain 기록 이유), Step 2.5 와 리포트의 `[미검증]` 네 칸, 리포트 FAIL 행 Details 머리 넷
2. `rust-kit/skills/rust-run/SKILL.md` — 종료 코드를 못 얻으면 다시 실행하고, 그래도 못 얻으면 `[미검증]` 네 칸
3. `rust-kit/skills/rust-test/SKILL.md` — 실행하지 못했으면 `[미검증]` 네 칸, 돌릴 수 있는데 안 돌렸으면 `[미검증]` 이 아니다
4. `rust-kit/agents/rust-reviewer.md` — 정본 조항 2 · 3 재동기화와 그 기록 줄, 남용 방지 4 요건, 미검증 마커 네 칸, 최종 판정 카운터 둘 · BLOCKED
5. `rust-kit/skills/rust-audit/SKILL.md` — Gotcha 14 네 칸 · 두 분류 · Step 5 가리킴, Step 5 카운터 둘 · BLOCKED
6. `rust-kit/skills/rust-model/SKILL.md` — 시각 컬럼 Gotcha, Step 1 입력 표 행, Step 2 줄, §4S Entity `DateTimeWithTimeZone` 과 어댑터 두 줄
7. `docs/rust/data/sqlx-patterns.md` — 원칙 6 (표 · SeaORM 과 SQLx 의 차이 · 실측 · 킷 규칙 문장 · 출처 여섯), 안티패턴 하나, 머리 설정 0.2.0 · 2026-09-25
8. `rust-kit/references/project-detection.md` — Step 2c 표를 crates.io · 2026-09-24 로, 행 여덟 더함
9. `rust-kit/skills/rust-grpc/SKILL.md` — Gotcha 5 를 0.14 로
10. `rust-kit/evals/evals.json` — 사례 17 (rust-preflight 원인 가르기)
11. `docs/rust/research-log.md` — `## [2026-09-24] — Phase 9 kaizen` 항목, 머리 설정 1.3.0 · 2026-09-25

새 규칙의 강도: rust-preflight Gotcha 10 은 E2 (리포트 FAIL 행에 원인과 증거를 남긴다 — skill-design-guide §3.7 초기 등급표의 「범위 · 개수 · 증거를 남겨야 하는 규칙」).
rust-model Gotcha 는 등급을 적지 않는다 — 같은 파일의 다른 Gotcha 도 적지 않고, 강도를 올릴 재발 근거가 없다.

Phase 1 가이드 변경 셋 (rust-kaizen Gotcha 8):

| 가이드 변경 | 이 킷 | 자리 |
| --- | --- | --- |
| `[미검증]` 에 네 칸 (skill-design-guide §3.7 3 항 · agent-design-guide §10 정책 2 항) | 반영 | rust-preflight 두 자리 · rust-run · rust-test · rust-reviewer · rust-audit (SK-09) |
| 작업 자체를 못 한다고 결론 내리기 전 네 칸 (§3.7 5 조항 3 항) | 해당 없음 | rust-kit 어디에도 작업 전체를 못 한다고 끝내는 자리가 없다(`grep -rn '불가능하다고\|못 한다\|할 수 없다고\|불가 선언' rust-kit` 0 건). 항목 하나를 못 재는 경우는 위 네 칸 자리가 받는다 |
| 0 이 아닌 값을 내는 새 측정 — 알려진 답 대조 (§3.7) | 해당 없음 | 이 킷 스킬은 값을 세는 측정 스크립트를 새로 만들지 않는다. 0 기대 측정은 rust-audit Gotcha 15 · rust-reviewer 0 매치 규칙이 이미 양성 대조를 요구한다 |

## 범위 경계

- 이 Phase 시작 HEAD: `4a8ec55f4d874eaaed083af9621f9679693cbdb6`. 범위 상한은 개정 파일 `.harness/sprint-amendments-kaizen-0924-p09-rust-kit.md` 의
  `end_sha:` 마지막 값이다. 여러 Phase 가 같은 가지 `kaizen/2026-09-24` 에 동시에 커밋하므로 `HEAD` 로 재지 않는다
- 고치는 파일은 열하나다 — 아래 블록이 그 목록이다(`harness/README.md` §커밋 안전 훅 이 정한 범위 선언 자리). 새 파일은 없다. `.harness/` 쪽은 이 계약 · 개정 파일 ·
  QA 피드백 · `.harness/.meta/kaizen-0924/phase9-notes.md` · `.harness/.meta/kaizen-0924/phase9-review.md` 를 쓴다 — 슬러그를 나열하지 않고 AR-01 셋째 값 `verify_seal` 로 잰다.
  AR-01 다섯째 값이 이 블록과 측정 공통 정의의 `FILES` 가 같은지 잰다

```text
# sprint-scope
rust-kit/skills/rust-preflight/SKILL.md
rust-kit/skills/rust-run/SKILL.md
rust-kit/skills/rust-test/SKILL.md
rust-kit/agents/rust-reviewer.md
rust-kit/skills/rust-audit/SKILL.md
rust-kit/skills/rust-model/SKILL.md
docs/rust/data/sqlx-patterns.md
rust-kit/references/project-detection.md
rust-kit/skills/rust-grpc/SKILL.md
rust-kit/evals/evals.json
docs/rust/research-log.md
.harness/
```

- **이 Phase 의 커밋 메시지에는 전부 `Co-Authored-By` 줄 바로 위에 서명 줄 `Kaizen-Phase: kaizen-0924-p09-rust-kit` 한 줄을 넣는다** (봉인 커밋 포함).
  AR-01 · ER-03 · SC-00 · DG-01 · DG-03 · DG-04 · DG-06 이 이 줄로 이 Phase 커밋을 가린다(`harness/references/contract-schema.md` §여러 주체가 한 가지에 커밋할 때 선택지 B).
  서명을 빠뜨린 커밋은 서명 줄 목록에 안 보이므로 AR-01 첫째 값과 ER-03 셋째 값은 경로로 직접 센다.
  FIX 가 커밋을 더할 때도 넣고, 개정 파일에 `end_sha:` 줄을 덧붙인다(옛 줄은 지우지 않는다). notes 커밋도 이 Phase 커밋이다 — notes 를 커밋한 뒤 그 sha 로
  `end_sha:` 줄을 하나 더 덧붙여 커밋한다
- 구현 커밋은 `git add -- <파일…> && git commit -o -- <파일…>` 로 열한 파일만 싣는다. `docs/rust/` 둘과 `rust-kit/` 아홉을 두 커밋으로 나눠도 된다 —
  둘 다 이 킷 몫이라 `validate-post-kaizen.py` scope-isolation 에 걸리지 않는다(예행에서 두 커밋으로 확인)
- 측정이 기대는 제목 · 줄 머리는 이름을 바꾸지 않는다: `# Gotchas` · `## 2.5. 마이그레이션 적용 상태 확인` · `## 3. test 실행` · `## 4. audit 검사` · `## Preflight Report` (rust-preflight) ·
  `## After Creation` (rust-test) · `## 미검증 증거 프로토콜 (정본 복제 — 재정의 금지)` · `## 최종 판정` (rust-reviewer) · `14. **미검증 항목 마커 프로토콜 (evaluator v3 대응)**` · `## 5. 최종 판정` (rust-audit) ·
  `## Gotchas` · `## 1. 입력 확인` · `### §4S — SeaORM 어댑터` (rust-model) · `### 5. 풀은` · `## 수치 기준` · `## 안티패턴` (sqlx-patterns) · `## Step 2c. 버전 현행성 확인` (project-detection) ·
  `5. **tonic-health / tonic-reflection은 별도 크레이트**` (rust-grpc) · 읽기만 하는 `### Step 3: 빌드/분석 검증` (`/sprint`) · `## Canonical Unverified-Evidence Protocol (각 kit reviewer 복제용 정본)` (qa-evaluation-guide) ·
  `### 10. 시각은` (database.md) · backend-reviewer · backend-audit 의 대조 문장
- 공유 파일(`.claude-plugin/marketplace.json` · `rust-kit/.claude-plugin/plugin.json` 버전 · 루트 `README.md` · 루트 `CLAUDE.md` · `docs/` HTML · 처리 배정표 · 감사 로그 ·
  실패 횟수 파일 · `.github/workflows/ci.yml` · `.harness/stale-values.yaml`)과 다른 Phase · 레포 전용 파일(`backend-kit/` · `harness/` · `scripts/` · `.claude/skills/`)은
  건드리지 않는다 — ER-03 셋째 값. rust-kit README AUTO 구간은 스킬 · 에이전트 frontmatter 만 읽는데 그 줄이 그대로다(AP-04). 문서 사이트 재생성은 Final F2 몫이라 DG-06 에서 `docs-site-regen` 을 뺀다
- QA(`harness:qa-evaluator`)는 설치본이다 — 이 Phase 가 고치는 파일에 qa-evaluator 는 없다
- 사용자 승인(Step 5) 대체: 사용자가 「자동으로 끝까지 알아서 진행해 내 허락이 필요한건 코덱스로 리서치나 검토받고」라고 위임했다(세션
  `de8c7935-a5b6-4df5-9106-fafa73c288a0` 기록 queued_command `2026-09-24T04:04:16.964Z`). Codex 사용량 한도가 소진돼(오류 원문 「You've hit your usage limit … try
  again at 11:05 PM」, 2026-09-24) 독립 Claude 검토자(REVIEW 에이전트)가 대신한다. 이어 사용자가 「코덱스 대신에 그냥 너가 알아서 진행하라고」라고 명시했다(같은 세션
  기록 user `2026-09-24T11:54:58.940Z`). 검토 결과 파일: `.harness/.meta/kaizen-0924/phase9-review.md`.
  1 회차 `VERDICT: CHANGES` — 고칠 것 넷(SK-08 · SK-02 · ER-03 · SK-11)과 권하는 것 넷을 초안이 모두 반영했다(반영 뒤 값은 `회귀 게이트` 절 표 · 둘째 예행 문단).
  2 회차 `VERDICT: CHANGES` (마지막 VERDICT) — 고칠 것 둘(`common.sh` 가 두 판 풀기 실패에서 멈추고 끝나면 지운다 · ER-03 넘김 경로 일곱을 `## 넘기는 것` 절 안에서 센다)을
  BUILD 가 봉인 전에 검토의 「고칠 문구」 그대로 반영했고, 권하는 것 넷 가운데 셋(rust-preflight Step 3.5 셋째 항목 주어 · 이 기록 줄 · 스크래치 임시 폴더 정리)을 반영했다.
  반영하지 않은 하나는 SK-07 `ct-run.sh` 에 E0308 수를 더하는 권장이다 — 출력 형식이 `compile_rc=` 한 값에서 바뀌면 SK-07 기대값 문장까지 고쳐야 하고,
  오류 줄은 빌드 기록 `build.log` 에 그대로 남는다. 남은 고칠 것은 0 이라 3 회차 검토 없이 봉인한다
- 오라클 한계: SK-04 는 평가 사례의 **구조**만 잰다(`scripts/run-evals.py` 는 스킬을 실행하지 않는다). 사례 17 을 실제 스킬로 돌려 답이 네 assertion 을 채우는지는
  LLM 판정이라 결정론 측정이 없다 — 조건으로 걸지 않는다. SK-03 은 Step 3.5 의 두 블록이 실제로 돌아 네 상황을 가르는지를 재지만, 남의 미커밋 확정 세 조건
  ((a) 시작 목록 (b) 내 경로 밖 (c) 내가 바꾼 이름)의 판단은 사람 · 에이전트 몫이라 재지 않는다. SK-07 은 sea-orm 1.1.19 만 잰다 — 2.x 는 로컬에 크레이트가 없다
- 오라클 해소: SK-01 · SK-02 · SK-05 · SK-06 · SK-08 ~ SK-12 — 산출물이 문서 문장 자체라 정해진 절 · 줄에 정해진 문장이 있는지가 판정이다. `sect` 가 코드 펜스를 건너뛰고 절을 자르고,
  `gline` 이 한 줄짜리 Gotcha · 표 행을 고른다. 시작 커밋 판에서 새 문장 0 · 옛 문장 1 이상을 봉인 전에 확인했고, 문장 하나만 지운 사본에서 그 값이 떨어졌다(`회귀 게이트` 절)
- 오라클 해소: SK-03 · SK-04 · SK-07 · DG-05 — 스킬의 코드 블록 · 검사 스크립트 · 컴파일러를 실제로 돌린 출력이다. 음성 대조가 붙어 있다
- 오라클 해소: ER-01 · ER-02 · AP-01 · AP-03 · DG-02 — 편집 전 판과 파일마다 비교한 더한 줄 계산이다. 각각 양성 대조가 붙어 있다
- 오라클 해소: ER-03 · AR-01 · SC-00 · DG-01 · DG-04 · DG-06 — 커밋 기록과 봉인 검증 함수를 실제로 돌린 출력이다. 예행 저장소 변형 넷이 양성 대조다
- 커버리지 해소: SK-01 · SK-02 · SK-05 · SK-06 · SK-08 · SK-09 · SK-10 · SK-11 · SK-12 · AR-02 · RE-02 — 산문의 파일 이름은 측정 `m <조건 ID>` 가 공통 정의의 변수(`$PF` · `$RU` · `$TE` · `$RV` · `$AU` · `$MO` · `$SQ` · `$PD` · `$GR` · `$EV` · `$RL`)로 연다(파일과 변수의
  대응은 `common.sh` 머리). 토큰은 `m.sh` 의 같은 ID 갈래에 글자 그대로 있다. 읽기만 하는 파일(`harness/skills/sprint/SKILL.md` · `harness/docs/guides/qa-evaluation-guide.md` ·
  `harness/docs/guides/skill-design-guide.md` · `backend-kit/agents/backend-reviewer.md` · `backend-kit/skills/backend-audit/SKILL.md` · `docs/backend/fundamentals/database.md`)은 `m.sh` 가 `$E/` 뒤 경로로 연다. SK-05 의 `0.2.0` · SK-12 의 `1.3.0` 은
  머리 설정 값이라 `fm_get` 이 읽고, `m.sh` 는 측정 도우미 자체의 이름, SK-06 의 `phase7-notes.md` 는 넘김 출처 설명이다. SK-09 의 `rust-kit/` 와 RE-02 의 `docs/rust/` 는 `grep -r` 의 인자다
- 커버리지 해소: ER-01 · ER-03 — `.harness/.meta/kaizen-0924/phase9-notes.md` · `.harness/.meta/evidence/phase9.md` 는 공통 정의의 `$NOTES` · `$EVID` 다. ER-03 의 넘김 경로는 `m.sh` `ER-03)` 갈래 `toks` 의 인자이고, `infra-kit/README.md` 는 예행 설명, `m.sh` 는 측정 도우미 자체의 이름이다
- 커버리지 해소: AR-01 — `rust-kit/` · `docs/rust/` 는 `unsigned_on` 의 인자, `.harness/` 는 `scope` 블록 줄과 `verify_seal` 이 도는 폴더, `harness/references/contract-schema.md` 는 권장 형태의 출처다
- 검출기는 공백 든 코드 조각 안의 인자를 읽지 못한다 — 위 해소 줄이 전부 그 경우다
- 편집 전부터 있던 경고(markdownlint MD060 · MD025 · MD032 등)는 범위 밖이다 — DG-02 는 더한 줄의 새 경고만 잰다
- rust-kit 안 특정 앱 이름(66 곳 · `grep -rnc 'fit-pal\|fitpal' rust-kit`)은 이번 네 관심사 밖이라 건드리지 않는다 — 새 문장에는 넣지 않았다(봉인 전 실측: 예행 판 더한 줄에 `grep -ciE 'fit-?pal'` 0). notes 다음 사이클 메모로 넘긴다
- notes 에 함께 적는다(조건으로는 재지 않는다): Phase 1 가이드 변경 셋 표(위), 「그대로 둔 곳」 — rust-reviewer · rust-audit 의 「미검증 1 건: [체크항목] — [이유]」
  보고 모양(backend-audit 와 같다), rust-reviewer Evidence Validity Gate 표의 접미 없는 `[미검증]`(정본 조항 2 가 레거시 표기를 `INVALID` 로 읽는다),
  rust-model §5 도메인 모델의 `DateTime<Utc>`(도메인은 UTC 순간이 맞다). ER-03 셋째 값이 0 이 아니면 QA 가 그 커밋 목록부터 보고 판정한다는 한 줄.
  `## 넘기는 것` 의 `audit-criteria.md` 줄에 `:89` 의 `utoipa 5.4 docs` 버전 리터럴(근거 파일 §3 표가 짚은 값)을 함께 적고, `## 다음 사이클 메모` 에
  「Step 2c 옛 행 `testcontainers` 의 전제 0.27 이 스킬 어디에도 없다」 를 적는다(검토 권하는 것 4 · 고칠 것 4)
- 기능 조건 20 · 전체 조건 줄 30
- 사용자가 할 일: 없음

## 회귀 게이트 — 측정 공통 정의와 봉인 전 실측

모든 조건의 측정은 아래 `common.sh` 와 `m.sh` 를 차례로 `.` 으로 읽은 **bash** 셸에서 돈다(zsh 는 따옴표 없는 변수를 쪼개지 않아 배열 인자가 한 덩어리가 된다).
`m` 은 도우미 함수와 두 판 폴더가 없으면 `HELPER_MISSING` · `SNAPSHOT_MISSING` 을 내고 멈춘다 — 그래서 조건마다 `type m` 하나로 정의 확인을 대신한다.
두 판 풀기가 끊기거나 열한 파일 가운데 하나라도 비면 `common.sh` 가 `SNAPSHOT_FAIL` 을 내고 종료 코드 2 로 끝난다. 셸이 끝나면 두 판 폴더를 지운다.
예행 값은 bash 5.3.9 와 `/bin/bash` 3.2.57 두 해석기에서 같았다(`p9d/run-final.txt` · `p9d/run-bash32.txt`).
블록 다섯(`common.sh` · `m.sh` · `new-warnings.sh` · `attr-run.sh` · `ct-run.sh`)을 각 블록 첫 `#` 주석 줄(셔뱅 다음)의 이름 그대로 한 폴더에 저장하고 그 폴더를 `K` 에 넣는다.
`END_UNRESOLVED` 가 찍히면 셸이 종료 코드 2 로 끝난다. `new-warnings.sh` 옆에는 `node_modules` 를
`/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/de8c7935-a5b6-4df5-9106-fafa73c288a0/scratchpad/p1build/node_modules` 로 잇고
`cfg.markdownlint-cli2.jsonc` = `{ "config": { "MD013": false } }` 를 둔다 — 준비 단계 실측(2026-09-25): 그 자리의 `.bin/markdownlint-cli2 --version` 첫 줄이
`markdownlint-cli2 v0.23.2 (markdownlint v0.41.1)`. 없으면 그 폴더에서 `npm install --no-save markdownlint-cli2@0.23.2` 부터 돌린다.
`common.sh` 의 `R` 은 예행 저장소를 가리킬 때만 쓴다 — 비우면 작업 폴더다. 두 판과 연습 저장소를 `${TMPDIR:-/tmp}` 아래 틀 있는 `mktemp -d` 로 푸므로 `TMPDIR` 를 스크래치 폴더로 두고 읽는다.

SK-03 · SK-07 의 준비 단계 실측(2026-09-25): `command -v cargo` → `/Users/jackson/.cargo/bin/cargo` (종료 0) · `cargo --version` → `cargo 1.96.0` · `rustc --version` → `rustc 1.96.0` ·
`~/.cargo/registry/cache/*/` 에 `sea-orm-1.1.19.crate` · `chrono-0.4.44.crate` · `sqlx-0.8.6.crate` 가 있다 · `cargo generate-lockfile --offline` 종료 0. SK-07 은 `CT_TARGET`
(`p9d/ct/target`, 이미 빌드한 의존성)을 빌드 캐시로 쓴다 — 캐시가 있으면 한 번에 7 초 안팎, 없으면 처음부터 3 ~ 5 분이다. 네트워크는 쓰지 않는다(`--offline`).

```bash
# common.sh — 측정 공통 정의. bash 로 읽는다 (zsh 는 배열 첨자가 1 부터이고 따옴표 없는 변수를 쪼개지 않는다)
export LC_ALL=C.UTF-8   # 번역투 정규식이 글자 단위로 돌아야 한다
cd "${R:-/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/kaizen-0924}" || exit 2
B=4a8ec55f4d874eaaed083af9621f9679693cbdb6                  # 이 Phase 시작 HEAD
SIG='Kaizen-Phase: kaizen-0924-p09-rust-kit'
CF=.harness/sprint-contract-kaizen-0924-p09-rust-kit.md
AM=.harness/sprint-amendments-kaizen-0924-p09-rust-kit.md
NOTES=.harness/.meta/kaizen-0924/phase9-notes.md
EVID=.harness/.meta/evidence/phase9.md
END=$( [ -f "$AM" ] && sed -n 's/^end_sha:[[:space:]]*//p' "$AM" | tail -1 )
if [ -z "$END" ] || ! git rev-parse -q --verify "$END^{commit}" >/dev/null; then
  echo "END_UNRESOLVED — 측정을 멈춘다. HEAD 로 바꿔 재지 않는다"; exit 2
fi
: "${K:?도우미 폴더를 K 에 넣는다}"
PF=rust-kit/skills/rust-preflight/SKILL.md
RU=rust-kit/skills/rust-run/SKILL.md
TE=rust-kit/skills/rust-test/SKILL.md
RV=rust-kit/agents/rust-reviewer.md
AU=rust-kit/skills/rust-audit/SKILL.md
MO=rust-kit/skills/rust-model/SKILL.md
SQ=docs/rust/data/sqlx-patterns.md
PD=rust-kit/references/project-detection.md
GR=rust-kit/skills/rust-grpc/SKILL.md
EV=rust-kit/evals/evals.json
RL=docs/rust/research-log.md
FILES=("$PF" "$RU" "$TE" "$RV" "$AU" "$MO" "$SQ" "$PD" "$GR" "$EV" "$RL")
MDS=("$PF" "$RU" "$TE" "$RV" "$AU" "$MO" "$SQ" "$PD" "$GR" "$RL")
FOUR='네 칸(막는 것 · 시도한 우회 · 통제 불가 사유 · 재검증 명령)'
# SK-08 의 컴파일은 이 폴더를 빌드 캐시로 쓴다 — 없으면 처음부터 빌드한다(3 ~ 5 분)
CT_TARGET=${CT_TARGET:-/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/de8c7935-a5b6-4df5-9106-fafa73c288a0/scratchpad/p9d/ct/target}
export CT_TARGET
T=$(mktemp -d "${TMPDIR:-/tmp}/p9m.XXXXXX") || exit 2; mkdir -p "$T/B" "$T/E"
trap 'rm -rf "$T"' EXIT   # 한 번에 두 판 40 MB 안팎이 쌓인다 — 디스크가 차면 다음 풀기가 도중에 끊긴다
# 두 판을 풀어 둔 폴더에서 잰다 — 작업 폴더에 남은 다른 Phase 의 미커밋 변경이 끼지 않는다
# 풀기가 도중에 끊겨도 폴더는 남아 m 의 SNAPSHOT_MISSING 이 못 잡고, 0 을 기대하는 값이 통과로 읽힌다 — 여기서 멈춘다
git archive "$B" | tar -x -C "$T/B" && git archive "$END" | tar -x -C "$T/E" || { echo "SNAPSHOT_FAIL — 측정을 멈춘다"; exit 2; }
for f in "${FILES[@]}"; do [ -s "$T/B/$f" ] && [ -s "$T/E/$f" ] || { echo "SNAPSHOT_FAIL $f"; exit 2; }; done
# sect <파일> <제목 앞부분> — 그 제목부터 같은 깊이 이하의 다음 제목 전까지. 코드 펜스 안의 `#` 줄은 제목으로 보지 않는다
sect() { awk -v h="$2" '
  /^[[:space:]]*(```|~~~)/ { fence = !fence }
  !f && !fence && index($0, h) == 1 { f = 1; lvl = match($0, /[^#]/) - 1; print; next }
  f && !fence && /^#+ / { l = match($0, /[^#]/) - 1; if (l <= lvl) exit }
  f' "$1"; }
# gline <파일> <줄 앞부분> — 그 앞부분으로 시작하는 줄. Gotcha 와 표 행은 한 줄이다
gline() { awk -v p="$2" 'index($0, p) == 1' "$1"; }
# toks <글> <토큰…> — 토큰마다 글 안에서 그 토큰이 든 줄 수
toks() { local s="$1"; shift; for t in "$@"; do printf '%s ' "$(printf '%s\n' "$s" | grep -cF -- "$t")"; done; echo; }
# tbl — 표 줄 수와 끊긴 곳 수 (표 줄 사이에 다른 줄이 끼면 끊긴 것이다)
tbl() { awk '/^\|/{n++; if (p && NR != p + 1) g = 1; p = NR} END{print n + 0, g + 0}'; }
url()   { grep -oE 'https?://[^ )>"`]+' | sed -E 's/[.,;:]+$//' | sort -u; }
added() { for f in "${FILES[@]}"; do git diff --no-index -U0 "$T/B/$f" "$T/E/$f"; done | grep '^+' | grep -v '^+++'; }
mine() { git log --format= --name-only "${1}..${2}" --grep="^${3}\$" | grep . | LC_ALL=C sort -u; }
unsigned_on() { _b=${1}; _u=${2}; _s=${3}; shift 3
  git log --format=%H "${_b}..${_u}" -- "$@" | while read -r _c; do git log -1 --format=%B "$_c" | grep -qxF "$_s" || echo "$_c"; done; }
# not_other <base> <상한> <서명> <경로…> — 경로를 건드린 구간 안 커밋 가운데 다른 Phase 서명이 없는 커밋 (0 줄이어야 한다)
not_other() { _b=${1}; _u=${2}; _s=${3}; shift 3
  git log --format=%H "${_b}..${_u}" -- "$@" | while read -r _c; do
    _m=$(git log -1 --format=%B "$_c")
    if printf '%s\n' "$_m" | grep -qE '^Kaizen-Phase: ' && ! printf '%s\n' "$_m" | grep -qxF "$_s"; then continue; fi
    echo "$_c"; done; }
my() { mine "$B" "$END" "$SIG"; }
# scope <계약> — `## 범위 경계` 절 안, 첫 줄이 `# sprint-scope` 인 text 블록의 경로 줄
scope() { awk '/^## /{s=$0} s ~ /^## 범위 경계/ && /^```text$/{b=1; n=0; next} b && /^```$/{b=0; next} b{n++; if (n==1 && $0 != "# sprint-scope") b=0; else if (n>1) print}' "$1"; }
fm_get() { awk -v k="^$2:[[:space:]]*" 'NR==1 && /^---[[:space:]]*$/ { fm=1; next } fm && /^---[[:space:]]*$/ { exit } fm && $0 ~ k { sub(k, "", $0); print; exit }' "$1" | sed -e "s/[[:space:]]*$//" -e "s/^['\"]//" -e "s/['\"]\$//"; }
sha256_16() { if command -v sha256sum >/dev/null 2>&1; then sha256sum; elif command -v shasum >/dev/null 2>&1; then shasum -a 256; else python3 -c 'import hashlib,sys; print(hashlib.sha256(sys.stdin.buffer.read()).hexdigest())'; fi | cut -c1-16; }
contract_digest() { grep -E '^- \[[ x]\] [A-Z]{2,}-[0-9]{2}' "$1" | sed -E 's/^- \[[ x]\]/- [ ]/' | sha256_16; }
verify_seal() { rec=$(fm_get "$1" conditions_digest); rec=${rec#sha256:}; if [ -z "$rec" ]; then echo "SEAL_ABSENT $1"; return 0; fi
  act=$(contract_digest "$1"); if [ "$rec" = "$act" ]; then echo "SEAL_OK $1"; else echo "SEAL_BROKEN $1 recorded=$rec actual=$act"; fi; }
K02='(을|를) ?(처리|관리)(합니다|한다)|에 대해서?|하도록 (합니다|한다)|에 의(해|하여)|되어 있(는 경우|을 때)|(표시|적용|호출|생성|반환)(됩니다|된다)'
```

```bash
# m.sh — 조건마다 재는 값을 한 줄로 낸다. common.sh 를 읽은 bash 에서 `m <조건 ID>` 로 부른다
m() {
  local E=$T/E S L fn
  # 도우미가 하나라도 없으면 grep -c 가 조용히 0 을 낸다 — 멈춘다
  for fn in sect gline toks tbl url added mine unsigned_on not_other my scope fm_get verify_seal; do
    type "$fn" >/dev/null 2>&1 || { echo "HELPER_MISSING $fn"; return 2; }; done
  [ -n "${T:-}" ] && [ -d "$T/B" ] && [ -d "$E" ] || { echo "SNAPSHOT_MISSING"; return 2; }
  case "$1" in
  SK-01)  # rust-preflight Gotcha 10 · 번호 · Step 5 리포트 FAIL 행 원인 넷 · Step 2 · 3 의 FAIL 줄
    L=$(gline "$E/$PF" '10. **빨간 clippy · test 를 내 변경 탓으로 단정하지 말고 원인을 셋으로 가른다 (enforcement 등급 E2)**')
    toks "$L" '10. **빨간 clippy' '내 변경 · 남의 미커밋 변경 · 기준 커밋에서 이미 실패' 'Step 3.5 이고, 그 결과를 Step 5 리포트의 FAIL 행 Details 첫머리에 적는다' \
      '**원인을 갈라도 Status 는 FAIL 그대로다**' '남의 변경을 치우려고 `git stash` 를 쓰지 마라' 'https://git-scm.com/docs/git-stash' '실측(2026-09-18)'
    sect "$E/$PF" '# Gotchas' | grep -oE '^[0-9]+\. \*\*' | tr -dc '0-9\n' | paste -sd' ' -
    S=$(sect "$E/$PF" '## Preflight Report')
    toks "$S" '**FAIL 행의 Details 는 원인으로 시작한다 (Gotcha 10).**' '원인을 적어도 그 행의 Status 와 **Result** 는 FAIL 그대로다' \
      '- `내 변경 — {내 파일:줄 또는 diff 한 덩어리}`' '- `남의 미커밋 — {시작 때 떠 둔 목록의 그 파일 줄 + 실패 파일:줄}`' \
      '- `기준 커밋에서 이미 실패 — {FORK_BASE sha · 명령 · exit · toolchain}`' '- `[미검증]` — 네 칸, 통제 불가 사유 칸에 「귀속 불명」'
    grep -cxF -- '- FAIL → 에러 출력 후 중단. 이후 단계 skip. 고치기 전에 Step 3.5 로 원인을 가른다.' "$E/$PF" ;;
  SK-02)  # rust-preflight Step 3.5 문장 · 자리 · 판정 세 줄이 /sprint 와 글자 그대로 같다
    S=$(sect "$E/$PF" '## 3.5. 실패 원인 가르기')
    toks "$S" '## 3.5. 실패 원인 가르기 (Step 2 · 3 이 FAIL 일 때 — Gotcha 10)' 'FORK_BASE=$(git merge-base HEAD origin/<기준 가지>)' \
      'git worktree add -q --detach "$t" "$ref"' 'git worktree remove --force "$t"' '<준비 명령>' '판정 세 줄은 harness `/sprint` Step 3 의 표를 글자 그대로 옮겼다' \
      'git worktree add -q --detach "$t" HEAD' 'echo "HEAD+내 변경 exit=$?"' '`HEAD+내 변경` 이 실패하면 **내 변경** 탓이다' \
      'git status --porcelain=v1 --untracked-files=all' '통제 불가 사유 칸에 「귀속 불명」 을 적는다' '시작 때 떠 둔 목록이 없으면 남의 미커밋으로 확정하지 않는다' \
      'https://git-scm.com/docs/git-worktree' 'https://git-scm.com/docs/git-status' 'https://git-scm.com/docs/git-merge-base' 'https://github.com/rust-lang/rust-clippy/blob/master/CHANGELOG.md' \
      '표 첫 줄 판정 칸의 「남의 미커밋이다」 는 이 블록과 아래 세 조건을 채울 때만 확정한다' '이 블록은 표 첫 줄(`HEAD` 임시 통과)일 때만 돌린다' \
      '`HEAD` 임시가 실패하면 이 블록으로 가르지 않는다 — 표 둘째 줄은 `기준 커밋에서 이미 실패`, 셋째 줄은 `FORK_BASE..HEAD` 사이 커밋이 원인 후보다.' \
      '셋째 줄에서 그 커밋을 이번 작업이 만들었으면 Details 를 `내 변경` 으로, 아니면 `[미검증]` 으로 시작하고'
    awk '/^## 3\. test 실행/{a=NR} /^## 3\.5\. 실패 원인 가르기/{b=NR} /^## 4\. audit 검사/{c=NR} END{print (a && b && c && a<b && b<c) ? 1 : 0}' "$E/$PF"
    diff <(printf '%s\n' "$S" | grep -E '^\| (공용 작업 폴더|실패) \|') \
         <(sect "$E/harness/skills/sprint/SKILL.md" '### Step 3: 빌드/분석 검증' | grep -E '^\| (공용 작업 폴더|실패) \|') >/dev/null \
      && echo "rows_same=1 rows=$(printf '%s\n' "$S" | grep -cE '^\| 실패 \|')" || echo "rows_same=0 rows=$(printf '%s\n' "$S" | grep -cE '^\| 실패 \|')" ;;
  SK-03)  # Step 3.5 의 두 bash 블록을 연습 저장소 네 곳에서 실제로 돌린다
    bash "$K/attr-run.sh" "$E/$PF" ;;
  SK-04)  # evals 사례 17 · run-evals
    python3 - "$E/$EV" <<'PY'
import json, sys
d = json.load(open(sys.argv[1], encoding="utf-8")); ev = d["evals"]
ids = [e.get("id") for e in ev]; e17 = [e for e in ev if e.get("id") == 17]
e = e17[0] if len(e17) == 1 else {}
a = e.get("assertions", []); t = [x.get("text", "") for x in a]
print(len(ev), ids == list(range(1, len(ev) + 1)), e.get("skill"), len(a), [x.get("type") for x in a].count("behavior"),
      sum("HEAD · FORK_BASE · 기준 가지로 같은 명령을 다시 돌린다" in s for s in t),
      sum("내가 쓴 파일만 얹어 한 번 더 돌려" in s for s in t),
      sum("git stash 로 남의 변경을 치우지 않는다" in s for s in t),
      sum("Status 는 FAIL 그대로다" in s for s in t))
PY
    ( cd "$E" && python3 scripts/run-evals.py rust-kit > "$T/re.txt" 2>&1; echo "rc=$? $(grep -E '^Total: ' "$T/re.txt")" ) ;;
  SK-05)  # docs/rust/data/sqlx-patterns.md 원칙 6 · 안티패턴 · 머리 설정
    S=$(sect "$E/$SQ" '### 6. 시각은 종류부터 나누고, 종류마다 Rust 타입과 열 타입을 정한다')
    toks "$S" '### 6. 시각은 종류부터' '`docs/backend/fundamentals/database.md` 원칙 10 이 정본이다' '| 시각 종류 | SQLx | SeaORM Entity | PostgreSQL 열 |' \
      '| 순간 | `chrono::DateTime<Utc>` | `DateTimeWithTimeZone` (`chrono::DateTime<FixedOffset>`) | `TIMESTAMPTZ` |' '| 받는 사람 지역을 따라가는 벽시계 |' '| 특정 지역에 묶인 벽시계 |' \
      '원래 시간대 이름을 남기지 않는다' '`sea-orm-cli generate entity` 는 `timestamp with time zone` 열에 `DateTimeWithTimeZone` 을' \
      '`.with_timezone(&Utc)`, 쓸 때 `Utc::now().fixed_offset()` 로 바꾼다' '실측(2026-09-25 · sea-orm 1.1.19 · sqlx 0.8.6 · chrono 0.4.44 · 오프라인 컴파일)' \
      'SeaORM 2.x 는 재지 않았다' '이 항목은 RFC 요구가 아니라 이 킷의 규칙이다' 'https://docs.rs/sqlx/latest/sqlx/postgres/types/index.html' \
      'https://github.com/SeaQL/seaql.github.io/blob/master/SeaORM/versioned_docs/version-1.1.x/04-generate-entity/03-column-types.md' \
      'https://github.com/SeaQL/seaql.github.io/blob/master/SeaORM/docs/04-generate-entity/03-column-types.md' 'https://www.rfc-editor.org/rfc/rfc5545.html#section-3.3.5'
    printf '%s\n' "$S" | tbl
    awk '/^### 5\. 풀은/{a=NR} /^### 6\. 시각은/{b=NR} /^## 수치 기준/{c=NR} END{print (a && b && c && a<b && b<c) ? 1 : 0}' "$E/$SQ"
    toks "$(sect "$E/$SQ" '## 안티패턴')" '### 벽시계를 `TIMESTAMPTZ` 순간 하나로만 저장' '원칙 6 의 표대로 벽시계 열과 시간대 이름 열에 나눠 저장한다'
    echo "$(fm_get "$E/$SQ" version) $(fm_get "$E/$SQ" last_updated)" ;;
  SK-06)  # rust-model — Gotcha · Step 1 행 · Step 2 줄 · §4S 타입
    L=$(sect "$E/$MO" '## Gotchas' | awk 'index($0, "- **시각 컬럼은 종류부터 정하고, ORM 마다 다른 타입 대응을 따른다**") == 1')
    toks "$L" '- **시각 컬럼은 종류부터' '벽시계를 `TIMESTAMPTZ` 순간 하나로만 저장하지 마라' '`TIMESTAMPTZ` 는 원래 시간대 이름을 남기지 않는다' \
      'IANA 시간대 식별자 열을 함께 둔다' '시간대와 나라를 코드 상수나 한 나라 기본값으로 박지 마라' \
      '`sea-orm-cli generate entity` 는 `timestamp with time zone` 열에 `DateTimeWithTimeZone`(`DateTime<FixedOffset>`)을 붙이므로' \
      '`docs/backend/fundamentals/database.md` 원칙 10' '`docs/rust/data/sqlx-patterns.md` 원칙 6' \
      'https://docs.rs/sqlx/latest/sqlx/postgres/types/index.html' 'https://www.postgresql.org/docs/current/datatype-datetime.html'
    S=$(sect "$E/$MO" '## 1. 입력 확인')
    echo "$(printf '%s\n' "$S" | grep -cF '| 시각 필드 종류 | `created_at`: 순간 · `remind_at`: 받는 사람 지역을 따라가는 벽시계') $(printf '%s\n' "$S" | tbl) $(grep -cF '기존 시각 필드의 종류 — 벽시계 필드가 시간대 이름 열과 짝을 이루는지 본다' "$E/$MO")"
    S=$(sect "$E/$MO" '### §4S — SeaORM 어댑터')
    toks "$S" 'pub created_at: DateTimeWithTimeZone,' 'created_at: m.created_at.with_timezone(&Utc),' 'created_at: Set(Utc::now().fixed_offset()),' 'use chrono::Utc;' \
      'pub created_at: DateTime<Utc>,' 'use chrono::{DateTime, Utc};' 'Set(chrono::Utc::now())' ;;
  SK-07)  # rust-model §4S 가 실제로 컴파일된다 — 새 판 · 옛 판 · 섞은 판(Entity 는 새 판, 어댑터 두 줄은 옛 판)
    echo "new=$(bash "$K/ct-run.sh" "$E/$MO" | sed 's/compile_rc=//') old=$(bash "$K/ct-run.sh" "$T/B/$MO" | sed 's/compile_rc=//') mixed=$(bash "$K/ct-run.sh" "$E/$MO" "$T/B/$MO" | sed 's/compile_rc=//')" ;;
  SK-08)  # rust-reviewer 정본 복제 — 조항 1~5 가 정본과 글자 그대로 같다 · 4 요건 · 재동기화 줄 · 옛 문구
    python3 - "$E/$RV" "$E/harness/docs/guides/qa-evaluation-guide.md" "$E/backend-kit/agents/backend-reviewer.md" <<'PY'
import re, sys
def items(text):
    # 번호 줄로 시작하는 목록 항목을 나눈다. 번호 · 앞 공백 · 인용 표식을 떼고 비교한다
    out, cur = [], None
    for line in text.split("\n"):
        l = re.sub(r"^> ?", "", line)
        if re.match(r"^\d+\. \*\*", l):
            cur = [re.sub(r"^\d+\. ", "", l)]; out.append(cur)
        elif cur is not None and l.startswith("   ") and l.strip():
            cur.append(l.strip())
        else:
            cur = None
    return [" ".join(x) for x in out]
rv = open(sys.argv[1], encoding="utf-8").read()
qa = open(sys.argv[2], encoding="utf-8").read()
be = open(sys.argv[3], encoding="utf-8").read()
sec = lambda s, h: (re.search("^" + re.escape(h) + r".*?(?=^#{1,3} )", s, flags=re.S | re.M) or [""])[0]
mine = items(sec(rv, "## 미검증 증거 프로토콜 (정본 복제 — 재정의 금지)"))
canon = items(sec(qa, "## Canonical Unverified-Evidence Protocol (각 kit reviewer 복제용 정본)"))
keys = ["**마커는", "**`[미검증]` 은 검증 도구·환경 부재 전용이며", "**임계값 2 는", "**생성자의 완료 주장은", "**조용한 PASS 금지"]
def first(xs, k): return next((x for x in xs if x.startswith(k)), None)
res = []
for k in keys:
    a, c = first(mine, k), first(canon, k)
    # 정본 조항 1 뒤 N/A 표는 빈 줄로 끊겨 items() 가 첫 두 줄만 잡는다 — 자르지 않고 글자 그대로 비교한다
    res.append(int(a is not None and a == c))
four_rv = items(sec(rv, "### `UNVERIFIED_ENV` 남용 방지 4 요건"))
four_be = items(sec(be, "### `UNVERIFIED_ENV` 남용 방지 4 요건"))
same = [int(len(four_rv) == 4 and len(four_be) == 4 and four_rv[i] == four_be[i]) for i in range(3)]
# 4 항은 예시 명령만 킷 도메인으로 바꾼다 — 예시 앞까지 같아야 한다
cut = lambda x: x.split("(예:")[0]
same.append(int(len(four_rv) == 4 and len(four_be) == 4 and cut(four_rv[3]) == cut(four_be[3])))
print(" ".join(map(str, res)), "|", " ".join(map(str, same)), "|", len(mine))
PY
    toks "$(cat "$E/$RV")" '> **재동기화 2026-09-25 (Phase 9):**' '> 정본 조항 1 의 N/A 표와 계약 DG 조건을 다루는 정본의 새 조항 2 는 옮기지 않았다' \
      '### `UNVERIFIED_ENV` 남용 방지 4 요건 (하나라도 없으면 `INVALID` 로 강등 · 정본 복제)' '**임계값은 2 다.**' '(3 분기: FAIL / 도구 부재 / 증거 무효)' ;;
  SK-09)  # 미검증 네 칸 — 여섯 자리 · 가이드의 칸 이름 · 옛 문구
    toks "$(sect "$E/$PF" '## 2.5. 마이그레이션 적용 상태 확인')" "\`[미검증]\` 에 $FOUR"
    toks "$(sect "$E/$PF" '## Preflight Report')" "Details 에 $FOUR"
    toks "$(cat "$E/$RU")" "\`[미검증]\` 에 $FOUR"
    toks "$(sect "$E/$TE" '## After Creation')" "\`[미검증]\` 에 $FOUR" '돌릴 수 있는데 안 돌렸으면 `[미검증]` 이 아니다'
    L=$(gline "$E/$RV" '**미검증 항목 마커 (agent-design-guide §10)**')
    toks "$L" "\"근거\" 컬럼에 $FOUR" '`[미검증:ENV]` 또는 `[미검증:INVALID]`' '막는 것: 운영 DB 접속 명령과 그 거부 출력' '하나라도 비면 `[미검증:INVALID]` 다'
    L=$(gline "$E/$AU" '14. **미검증 항목 마커 프로토콜 (evaluator v3 대응)**')
    toks "$L" "근거에 $FOUR" '네 칸 중 하나라도 비면 `[미검증:INVALID]` 다' '(Step 5 참조)' '`rust-kit/agents/rust-reviewer.md` §미검증 증거 프로토콜'
    toks "$(cat "$E/harness/docs/guides/skill-design-guide.md")" '   - **막는 것** —' '   - **시도한 우회** —' '   - **통제 불가 사유** —' '   - **재검증 명령** —'
    grep -rF -e '`[미검증] 종료 코드 캡처 실패' -e '`[미검증] DB 미기동' -e '`[미검증] 테스트 미실행`' -e '사유를 Details 에 남긴다' \
      -e '"근거" 컬럼에 이유를 기술한다' -e '근거에 이유를 기술하라' -e 'CONDITIONAL APPROVE 규칙을 적용한다 (Step 4 참조)' "$E/rust-kit" | grep -c . ;;
  SK-10)  # 두 카운터 판정 — rust-reviewer · rust-audit · backend-audit 와 같은 문장
    for f in "$RV" "$AU"; do
      if [ "$f" = "$RV" ]; then S=$(sect "$E/$f" '## 최종 판정'); else S=$(sect "$E/$f" '## 5. 최종 판정'); fi
      toks "$S" '카운터는 두 개이며 **합산하지 않는다** (정본 조항 3): `UNVERIFIED_INVALID_EVIDENCE`(임계 판정용)와 `env_gaps`(= `UNVERIFIED_ENV`, 커버리지 게이트용).' \
        '- **APPROVE** — 전 row PASS + `UNVERIFIED_INVALID_EVIDENCE` 0 건.' '- **CONDITIONAL APPROVE** — 전 row PASS 이지만 `UNVERIFIED_INVALID_EVIDENCE` 1 건 존재.' \
        'FAIL 또는 `UNVERIFIED_INVALID_EVIDENCE` 2 건 이상' '- **BLOCKED** — `(총 rule 수 − env_gaps) / 총 rule 수 < 0.60`. 판정 자체를 내지 않고 환경 부재 목록과 재검증 명령을 보고한다.' \
        '- 무효 K 건은 `UNVERIFIED_INVALID_EVIDENCE` 카운터에 합산 (현재 누계: M)' '미검증 태그 0 건' '무효 K 건은 미검증 카운터에 합산'
    done
    toks "$(sect "$E/$RV" '## 최종 판정')" '**미검증 수:** `UNVERIFIED_INVALID_EVIDENCE` = {M}개 (무효 증거 합산 포함) / `env_gaps` = {E}개'
    toks "$(sect "$E/$AU" '## 5. 최종 판정')" '`env_gaps` 로 세려면 남용 방지 4 요건을 모두 채워야 한다 (`rust-reviewer.md` §`UNVERIFIED_ENV` 남용 방지 4 요건).'
    # backend-audit 에 같은 두 문장이 있다 — 형제 킷과 같은 말을 쓴다
    toks "$(cat "$E/backend-kit/skills/backend-audit/SKILL.md")" '카운터는 두 개이며 **합산하지 않는다** (정본 조항 3): `UNVERIFIED_INVALID_EVIDENCE`(임계 판정용)와 `env_gaps`(= `UNVERIFIED_ENV`, 커버리지 게이트용).' \
      '- **BLOCKED** — `(총 rule 수 − env_gaps) / 총 rule 수 < 0.60`. 판정 자체를 내지 않고 환경 부재 목록과 재검증 명령을 보고한다.' ;;
  SK-11)  # 현행화 — Step 2c 표 · 표가 전제하는 값이 스킬에 실제로 있다 · rust-grpc 0.14
    S=$(sect "$E/$PD" '## Step 2c. 버전 현행성 확인')
    toks "$S" '| 크레이트 | 조회 시점 최신 (crates.io · 2026-09-24) | rust-kit 문서 예시가 전제하는 버전 |' '| `sea-orm` | 2.0.3 | 1.1 |' \
      '| `tonic` | 0.14.6 | 0.14 (`tonic-health` · `tonic-reflection` 도 0.14 계열) |' '| `tower-http` | 0.7.1 | 0.6 — 0.7 은 compression · feature · redirect 동작이 바뀌었다 |' \
      '| `utoipa` · `utoipa-scalar` | 6.0.0 · 0.4.0 | 5.4 · 0.3 — 6 은 YAML 오류 타입이 바뀌었다 |' '| `rust-i18n` | 4.2.2 | 3 |' \
      '| `opentelemetry` · `opentelemetry-otlp` · `tracing-opentelemetry` | 0.33.0 · 0.33.0 · 0.34.0 | 0.31 · 0.31 · 0.32 |' '| `mockall` | 0.15.0 | 0.13 |' \
      '| `rstest` | 0.27.0 | 0.26 |' '| Rust stable | 1.98.1 | 1.88.0 (`rust-init` 고정 예시) |' '| `sea-orm` | 2.0.1 |' 'docs.rs latest · 2026-08-13'
    printf '%s\n' "$S" | tbl
    for p in 'tower-http = { version = "0.6"' 'utoipa = { version = "5.4"' 'utoipa-scalar = { version = "0.3"' 'rust-i18n = "3"' 'opentelemetry = "0.31"' 'mockall = "0.13"' 'channel = "1.88.0"'; do
      printf '%s ' "$(grep -rlF -- "$p" "$E/rust-kit/skills" | grep -c .)"; done
    printf '%s\n' "$(grep -cF '`rstest 0.26`' "$E/$TE")"
    L=$(gline "$E/$GR" '5. **tonic-health / tonic-reflection은 별도 크레이트**')
    echo "$(toks "$L" '`tonic-health = "0.14"`, `tonic-reflection = "0.14"`' '(`references/project-detection.md` Step 2c)')$(grep -cF '"0.13"' "$E/$GR")" ;;
  SK-12)  # docs/rust/research-log.md 새 항목 · 맨 앞 · 머리 설정
    S=$(sect "$E/$RL" '## [2026-09-24] — Phase 9 kaizen')
    toks "$S" '## [2026-09-24] — Phase 9 kaizen' '`.harness/.meta/evidence/phase9.md`' '`backend-family:P4`' '`backend-family:P2`' '### 봉인 전 실측' \
      '| SeaORM 1.1.19 Entity 필드의 열 타입 추론 |' '### 버전 현행성 (crates.io · 2026-09-24)' '### 미반영' 'rust-audit 기준의 시각 종류 판정 행'
    printf '%s\n' "$S" | tbl
    echo "$(grep -m1 '^## \[' "$E/$RL" | grep -cxF '## [2026-09-24] — Phase 9 kaizen') $(fm_get "$E/$RL" version) $(fm_get "$E/$RL" last_updated)" ;;
  ER-01)  # 새로 생긴 URL 이 근거 파일에 있다 — 열한 파일은 파일마다 편집 전 판과 비교, notes 는 URL 전부
    for f in "${FILES[@]}"; do comm -13 <(url < "$T/B/$f") <(url < "$E/$f"); done | sort -u | comm -23 - <(url < "$E/$EVID") | grep -c .
    # notes 가 없으면 입력이 비어 조용히 0 이 된다 — 없다고 찍는다
    if [ -f "$E/$NOTES" ]; then url < "$E/$NOTES" | comm -23 - <(url < "$E/$EVID") | grep -c .; else echo NOTES_MISSING; fi ;;
  ER-02)  # 더한 줄의 번역투 6 종 — 정본을 글자 그대로 옮긴 줄은 뺀다 (문구를 바꾸면 복제가 깨진다. 정본 문구는 Phase 3 몫)
    added | sed 's/^+//' | grep -vxF -f "$E/harness/docs/guides/qa-evaluation-guide.md" | grep -cE "$K02" ;;
  ER-03)  # notes 문자열 · 공유 파일과 다른 Phase 파일을 건드린 커밋
    git cat-file -e "$END:$NOTES" && echo notes_committed=1 || echo notes_committed=0
    # 넘김 경로 일곱은 반영 · changelog 절에도 나오기 쉽다 — `## 넘기는 것` 절 안에서만 센다. 값 순서는 그대로다
    echo "$(toks "$(cat "$E/$NOTES")" 'backend-family:P4' 'backend-family:P2' 'F09')$(toks "$(sect "$E/$NOTES" '## 넘기는 것')" \
      'rust-kit/skills/rust-audit/references/audit-criteria.md' 'rust-kit/skills/rust-init/SKILL.md' '.claude/skills/rust-kaizen/SKILL.md' \
      'harness/docs/guides/qa-evaluation-guide.md' 'harness/skills/sprint/SKILL.md' 'docs/rust-kit/sqlx-patterns.html' 'plugin.json')$(toks "$(cat "$E/$NOTES")" \
      'SeaORM 2.x' '## 반영한 처리 배정표 키' '## 미반영 키와 사유' '## 넘기는 것' '## changelog 한 단락' '## 킷 로그 한 단락' '## 다음 사이클 메모')"
    not_other "$B" "$END" "$SIG" .claude-plugin/marketplace.json rust-kit/.claude-plugin/plugin.json README.md CLAUDE.md \
      .harness/.meta/orchestrator-audit-log.md .harness/.meta/kaizen-failure-count.yaml .claude/kaizen-input/insights-report.md \
      .github/workflows/ci.yml .harness/stale-values.yaml .claude/skills docs/rust-kit backend-kit harness scripts | grep -c . ;;
  ER-04)  # rust-kaizen Gotcha 9 의 회귀 검사 — 1 이상이어야 하는 값 · 편집 전과 같아야 하는 값
    for p in "domain event\|outbox:rust-kit/skills/rust-init/SKILL.md" "domain event\|outbox:rust-kit/skills/rust-feature/SKILL.md" \
      "Composition Root:rust-kit/skills/rust-api/SKILL.md" "마이그레이션:$PF" "마이그레이션:$TE" "MockDatabase:$TE" "통합 테스트로 주장하지 마라:$TE" \
      "--bins:$RU" "--bins:$TE" "--bins:$PD" "pipefail:$RU"; do
      printf '%s ' "$([ "$(grep -c -- "${p%%:*}" "$E/${p#*:}")" -ge 1 ] && echo 1 || echo 0)"; done; echo
    for d in "$T/B" "$E"; do printf '%s/%s ' "$(grep -n 'State<PgPool>\|State<sqlx::\|State(pool)' "$d/rust-kit/skills/rust-api/SKILL.md" | grep -c .)" \
      "$(grep -rn '"/[a-z_/]*:[a-z_]\+"' "$d/rust-kit/skills" --include=SKILL.md | grep -c .)"; done; echo ;;
  AR-01)  # 허용 경로 · 서명 · 봉인 · 범위 선언 블록
    unsigned_on "$B" "$END" "$SIG" rust-kit docs/rust | grep -c .
    echo "$(my | grep -v '^\.harness/' | grep -vxF -f <(printf '%s\n' "${FILES[@]}") | grep -c .) $(my | grep -cxF -f <(printf '%s\n' "${FILES[@]}"))"
    find .harness -type f -name 'sprint-contract*.md' -print0 | while IFS= read -r -d '' f; do verify_seal "$f"; done \
      | awk '$1=="SEAL_BROKEN"{print $2}' | sed 's#^\./##' | sort -u | comm -12 - <( { my; echo "$CF"; } | sort -u) | grep -c .
    verify_seal "$E/$CF" | cut -d' ' -f1
    diff <(scope "$E/$CF" | grep -vxF '.harness/' | sort) <(printf '%s\n' "${FILES[@]}" | sort) >/dev/null && echo "scope_same=1" || echo "scope_same=0"
    scope "$E/$CF" | grep -cxF '.harness/' ;;
  AR-02)  # 연결 — 새 문장이 가리키는 제목이 그 파일에 있다
    echo "$(grep -c '^### 6\. 시각은 종류부터 나누고' "$E/$SQ") $(grep -c '^### 10\. 시각은' "$E/docs/backend/fundamentals/database.md") $(grep -cxF '## 미검증 증거 프로토콜 (정본 복제 — 재정의 금지)' "$E/$RV") $(grep -c '^### `UNVERIFIED_ENV` 남용 방지 4 요건' "$E/$RV") $(grep -c '^## Step 2c\. 버전 현행성 확인' "$E/$PD") $(grep -c '^## 3\.5\. 실패 원인 가르기' "$E/$PF") $(grep -cF '미검증 프로토콜의 4 요건을 그대로 적용한다' "$E/$RV")" ;;
  RE-02)  # 한 곳에만 둔다 — 시각 종류 정의 표 · 4 요건 사본 · 판정 세 줄
    echo "$(grep -rlF '| 시각 종류 | 예 | 저장 형태 (PostgreSQL) | 순간이 필요할 때 |' "$E/rust-kit" "$E/docs/rust" | grep -c .) $(grep -rl '^### `UNVERIFIED_ENV` 남용 방지 4 요건' "$E/rust-kit" | sed "s#^$E/##" | tr '\n' ' ')$(grep -rlF '| 실패 | 실패 | 실패 | 기준 커밋에서 이미 실패 — 내 변경 전부터다 |' "$E/rust-kit" | sed "s#^$E/##")"
    # 제목 없이 4 요건 항목만 붙여 넣은 사본도 잡는다 — 1 항 머리로 센다
    echo "four_items_in=$(grep -rlF '**1 차 도구 시도 기록**' "$E/rust-kit" | sed "s#^$E/##" | paste -sd' ' -)" ;;
  AP-01)  # 더한 줄에 이 킷 플러그인 버전 값 — 값은 plugin.json 에서 읽는다
    L=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["version"])' "$E/rust-kit/.claude-plugin/plugin.json")
    echo "version=$L $(added | grep -cF -- "$L")" ;;
  AP-03)  # 언어 힌트 없는 여는 펜스 수 — 파일마다 편집 전 / 뒤. 여는 줄과 닫는 줄을 상태로 가른다 (validate-plugin V6 와 같은 방식)
    python3 - "$T/B" "$E" "${MDS[@]}" <<'PY'
import re, sys
b, e, files = sys.argv[1], sys.argv[2], sys.argv[3:]
def bare(p):
    n, cur = 0, None
    for line in open(p, encoding="utf-8"):
        m = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line.rstrip("\n"))
        if not m:
            continue
        mk, info = m.group(1), m.group(2).strip()
        if cur is None:
            cur = mk
            n += 0 if info else 1
        elif mk[0] == cur[0] and len(mk) >= len(cur) and not info:
            cur = None
    return n
print(" ".join(f"{bare(b + '/' + f)}/{bare(e + '/' + f)}" for f in files))
PY
    ;;
  AP-04)  # frontmatter — 첫 블록이 편집 전과 같은지 / name 줄 수
    for f in "$PF" "$RU" "$TE" "$AU" "$MO" "$GR" "$RV"; do
      L=$(basename "$f" .md); [ "$L" = SKILL ] && L=$(basename "$(dirname "$f")")
      printf '%s/%s ' "$(diff <(awk 'NR==1&&/^---/{fm=1;next} fm&&/^---/{exit} fm' "$T/B/$f") <(awk 'NR==1&&/^---/{fm=1;next} fm&&/^---/{exit} fm' "$E/$f") >/dev/null && echo 1 || echo 0)" \
        "$(awk 'NR==1&&/^---/{fm=1;next} fm&&/^---/{exit} fm' "$E/$f" | grep -cxF "name: $L")"; done; echo ;;
  DG-02)  # markdownlint — 더한 줄의 새 경고 · evals.json 파싱
    for f in "${MDS[@]}"; do k=$(printf '%s' "$f" | tr '/' '_'); cp "$T/B/$f" "$T/$k.0.md"; cp "$E/$f" "$T/$k.md"; bash "$K/new-warnings.sh" "$T/$k.0.md" "$T/$k.md"; done
    python3 -c 'import json,sys; json.load(open(sys.argv[1], encoding="utf-8")); print("json_ok")' "$E/$EV" ;;
  DG-05)  # 저장소 검사 — $END 판을 git 저장소로 만든 사본에서 돈다 (작업 폴더의 다른 Phase 미커밋 변경이 끼지 않는다)
    local G=$T/G; rm -rf "$G"; cp -R "$E" "$G"
    git -C "$G" init -q && git -C "$G" add -A && git -C "$G" -c user.name=m -c user.email=m@m commit -qm snap || return 2
    ( cd "$G" && python3 scripts/validate-plugin.py rust-kit > "$T/vp.txt" 2>&1 )
    echo "$(grep -cE '^  V([1-9]|10) ' "$T/vp.txt") $(grep -E '^  V([1-9]|10) ' "$T/vp.txt" | grep -cE 'ERROR|FAIL')"
    # sync-evals 는 킷 이름 인자가 없다 — rust-kit 머리 줄을 읽었는지와 그 아래 어긋남 줄 수만 센다
    ( cd "$G" && python3 scripts/sync-evals.py --check-only > "$T/se.txt" 2>&1 )
    echo "$(grep -cxF '→ rust-kit' "$T/se.txt") $(awk '/^→ /{f=($2=="rust-kit"); next} f && NF' "$T/se.txt" | grep -c .)"
    ( cd "$G" && python3 scripts/check-stale-values.py > "$T/sv.txt" 2>&1 ); echo "stale_rc=$? $(grep -cF -f <(printf '%s\n' "${FILES[@]}") "$T/sv.txt")" ;;
  DG-06)  # 사이클 검사 — 이 Phase 몫 줄만 본다. docs-site-regen 은 Final F2 몫
    python3 scripts/validate-post-kaizen.py --since "$B" --verbose > "$T/vpk.txt" 2>&1
    grep -E '\] . (scope-isolation|doc-contracts): ' "$T/vpk.txt" | awk '{print $5, $2}'
    # doc-contracts 가 검사한 경로 수와 그 가운데 이 Phase 파일 수 — FAIL 이 나도 이 Phase 몫인지 가른다
    python3 scripts/validate-doc-contracts.py -v 2>&1 | awk -F' → ' '/^ *검사: /{a=$1; sub(/^ *검사: /,"",a); sub(/:[0-9]+$/,"",a); print a; print $2}' | sort -u > "$T/dc.txt"
    echo "doc_checked=$(grep -c . "$T/dc.txt") doc_mine=$(comm -12 "$T/dc.txt" <(my) | grep -c .)"
    # 위반 커밋 목록을 읽은 수와 그 가운데 이 Phase 서명 커밋 수. 목록을 못 읽으면 둘째 값이 조용히 0 이 되므로 첫 값을 함께 본다
    awk '/ scope-isolation: /{f=1;next} /^\[ /{f=0} f&&/^ +[0-9a-f]{7,40}$/{print $1}' "$T/vpk.txt" > "$T/viol.txt"
    echo "violators=$(grep -c . "$T/viol.txt") mine=$(while read -r c; do git log -1 --format=%B "$c" | grep -qxF "$SIG" && echo "$c"; done < "$T/viol.txt" | grep -c .)" ;;
  *) echo "UNKNOWN $1"; return 2 ;;
  esac
}
```

```bash
#!/usr/bin/env bash
# new-warnings.sh <옛 파일> <새 파일> — 새 파일에서 더한 줄에 걸린 경고만 센다. 줄이 밀리므로 전체 수 차이로 세지 않는다
# 줄 번호는 경로 뒤 첫 번째 숫자다. 탐욕 매치(^[^ ]*:)로 뽑으면 열 번호가 줄 번호로 둔갑한다 (실측 2026-09-24)
# 린터가 안 돌면 경고 0 이 조용히 나온다 — 돌았다는 줄(Linting: 1 file)이 없으면 멈춘다 (실측 2026-09-25: 옆에 node_modules 가 없어 0)
set -u
DIR=$(cd "$(dirname "$0")" && pwd)
ADDED=$(git diff --no-index -U0 -- "$1" "$2" | awk '/^@@/{split($3,a,","); s=substr(a[1],2)+0; n=(a[2]==""?1:a[2]+0); for(i=0;i<n;i++) print s+i}' | sort -u)
OUT=$("$DIR/node_modules/.bin/markdownlint-cli2" --config "$DIR/cfg.markdownlint-cli2.jsonc" "$2" 2>&1)
printf '%s\n' "$OUT" | grep -q '^Linting: 1 file' || { echo "LINT_NOT_RUN $2"; exit 2; }
LINES=$(printf '%s\n' "$OUT" | grep -E ':[0-9]+(:[0-9]+)? (error|warning) ' | sed -E 's#^([^:]*):([0-9]+).*#\2#' | sort -u)
NEWW=$(comm -12 <(printf '%s\n' "$ADDED" | grep . | sort) <(printf '%s\n' "$LINES" | grep . | sort) | wc -l | tr -d ' ')
echo "total_warning_lines=$(printf '%s\n' "$LINES" | grep -c .) added_lines=$(printf '%s\n' "$ADDED" | grep -c .) new_warnings=$NEWW"
```

```bash
#!/usr/bin/env bash
# attr-run.sh <rust-preflight SKILL.md> — Step 3.5 의 두 bash 블록을 글자 그대로 떼어 네 가지 연습 저장소에서 돌린다
# 출력 한 줄 = `<상황> <공용> <HEAD> <FORK_BASE> <origin/main> <HEAD+내 변경> wt=<남은 워크트리 수> untouched=<공용 폴더 그대로면 1>` (0 통과 · 1 실패)
set -u
SKILL=${1:?}
command -v cargo >/dev/null || { echo CARGO_MISSING; exit 2; }
W=$(mktemp -d "${TMPDIR:-/tmp}/p9a.XXXXXX") || exit 2
python3 - "$SKILL" "$W" <<'PY'
import re, sys, pathlib
s = open(sys.argv[1], encoding="utf-8").read()
fence = "`" * 3
m = re.search(r"^## 3\.5\. .*?(?=^#{1,2} )", s, flags=re.S | re.M)
blocks = re.findall("^" + fence + r"bash\n(.*?)^" + fence + "$", m.group(0), flags=re.S | re.M) if m else []
out = pathlib.Path(sys.argv[2])
if len(blocks) != 2:
    (out / "NO_BLOCK").write_text(str(len(blocks)))
    sys.exit(0)
# 자리표시자만 바꾼다 — 나머지는 스킬 글 그대로 돈다
sub = {"<기준 가지>": "main", "<준비 명령>": "true", "<실패한 검사 명령>": "cargo check -q --offline", "<내 경로…>": "src/mine.rs"}
for i, b in enumerate(blocks):
    for k, v in sub.items():
        b = b.replace(k, v)
    (out / f"b{i + 1}.sh").write_text(b, encoding="utf-8")
PY
[ -f "$W/NO_BLOCK" ] && { echo "NO_BLOCK $(cat "$W/NO_BLOCK")"; exit 0; }
put() { printf '%s\n' "$2" > "$1"; }
mk() {  # mk <상황> — 기준 가지 main 과 그 bare 원격(origin)을 만든다
  local d=$W/$1
  mkdir -p "$d/src" && cd "$d" || exit 2
  git init -q -b main && git config user.name t && git config user.email t@t && git config commit.gpgsign false
  printf '[package]\nname = "p9a"\nversion = "0.1.0"\nedition = "2021"\n' > Cargo.toml
  put src/lib.rs 'pub mod mine; pub mod other;'
  put src/mine.rs 'pub fn a() -> i32 { 1 }'
  put src/other.rs 'pub fn b() -> i32 { 2 }'
  printf 'target/\nCargo.lock\n' > .gitignore
  git add -A && git commit -qm base
}
pub() { git clone -q --bare "$PWD" "$W/$1.git" && git remote add origin "$W/$1.git" && git fetch -q origin; }
run() {  # run <상황> — 공용 폴더 · 두 블록을 돌려 종료 코드를 0/1 로 줄인다
  local before shared r
  before=$(git status --porcelain)
  ( cargo check -q --offline ) >/dev/null 2>&1; shared=$?
  r=$(bash "$W/b1.sh" 2>/dev/null | sed -n 's/.*exit=\([0-9]*\)$/\1/p' | tr '\n' ' ')
  r="$r$(bash "$W/b2.sh" 2>/dev/null | sed -n 's/.*exit=\([0-9]*\)$/\1/p')"
  printf '%s %s ' "$1" "$([ "$shared" = 0 ] && echo 0 || echo 1)"
  for x in $r; do printf '%s ' "$([ "$x" = 0 ] && echo 0 || echo 1)"; done
  echo "wt=$(git worktree list | grep -c .) untouched=$([ "$(git status --porcelain)" = "$before" ] && echo 1 || echo 0)"
}
# A 남의 미커밋 — 남이 고치다 만 other.rs 가 깨졌고 내 mine.rs 변경은 멀쩡하다
mk A; pub A; git checkout -q -b work
put src/mine.rs 'pub fn a() -> i32 { 3 }'; put src/other.rs 'pub fn b() -> i32 { "x" }'; run A
# B 내 변경 — 내 mine.rs 가 깨졌고 남의 other.rs 변경은 멀쩡하다
mk B; pub B; git checkout -q -b work
put src/mine.rs 'pub fn a() -> i32 { "x" }'; put src/other.rs 'pub fn b() -> i32 { 4 }'; run B
# C 기준 커밋에서 이미 실패 — main 에 깨진 커밋이 먼저 들어갔다
mk C; put src/other.rs 'pub fn b() -> i32 { "x" }'; git commit -qam broken; pub C; git checkout -q -b work
put src/mine.rs 'pub fn a() -> i32 { 5 }'; run C
# D 이번 커밋 탓 — 내 가지에 깨진 커밋을 올렸다
mk D; pub D; git checkout -q -b work
put src/other.rs 'pub fn b() -> i32 { "x" }'; git commit -qam mine-broken; put src/mine.rs 'pub fn a() -> i32 { 6 }'; run D
```

```bash
#!/usr/bin/env bash
# ct-run.sh <Entity 를 가져올 rust-model SKILL.md> [어댑터 두 줄을 가져올 SKILL.md] — §4S 의 Entity 블록과 어댑터의
# created_at 두 줄을 글자 그대로 떼어 sea-orm 1.1.19 로 오프라인 컴파일한다. 출력: compile_rc=<종료 코드>
set -u
NEW=${1:?}; ADP=${2:-$1}
command -v cargo >/dev/null || { echo CARGO_MISSING; exit 2; }
C=$(mktemp -d "${TMPDIR:-/tmp}/p9c.XXXXXX") || exit 2; mkdir -p "$C/src"
python3 - "$NEW" "$ADP" "$C/src/main.rs" <<'PY' || { echo EXTRACT_FAIL; exit 2; }
import re, sys
fence = "`" * 3
def blocks(path):
    s = open(path, encoding="utf-8").read()
    m = re.search(r"^### §4S — SeaORM 어댑터\n(.*?)(?=^#{1,3} )", s, flags=re.S | re.M)
    return re.findall("^" + fence + r"rust\n(.*?)^" + fence + "$", m.group(1), flags=re.S | re.M) if m else []
ent, adp = blocks(sys.argv[1]), blocks(sys.argv[2])
if len(ent) < 2 or len(adp) < 2:
    sys.exit("NO_BLOCK")
la = [l for l in adp[1].split("\n") if "created_at: m.created_at" in l]
lb = [l for l in adp[1].split("\n") if "created_at: Set(" in l]
if len(la) != 1 or len(lb) != 1:
    sys.exit("NO_LINE")
src = ("#![allow(dead_code, unused_imports)]\npub mod user {\n" + ent[0] + "}\n\n"
       "use chrono::Utc;\nuse sea_orm::Set;\n\n"
       "pub struct User {\n    pub created_at: chrono::DateTime<chrono::Utc>,\n}\n\n"
       "fn to_domain(m: user::Model) -> User {\n    User {\n" + la[0] + "\n    }\n}\n\n"
       "fn to_active() -> user::ActiveModel {\n    user::ActiveModel {\n" + lb[0] + "\n        ..Default::default()\n    }\n}\n\n"
       "fn main() {}\n")
open(sys.argv[3], "w", encoding="utf-8").write(src)
PY
cat > "$C/Cargo.toml" <<'TOML'
[package]
name = "p9c"
version = "0.1.0"
edition = "2021"

[dependencies]
sea-orm = { version = "=1.1.19", default-features = false, features = ["sqlx-postgres", "runtime-tokio-rustls", "macros", "with-chrono"] }
chrono = "=0.4.44"
TOML
( cd "$C" && cargo generate-lockfile --offline -q && CARGO_TARGET_DIR="${CT_TARGET:-$C/target}" cargo build --offline -q ) >"$C/build.log" 2>&1
echo "compile_rc=$?"
```

**예행.** 시작 커밋에서 레포를 스크래치로 복제해(`p9d/rehearse.sh`) BUILD 가 할 커밋을 흉내 냈다 — 봉인 커밋(이 계약 초안에 digest 를 적은 판) → 다른 Phase 서명 커밋 하나
(`infra-kit/README.md`, 걸러져야 한다) → `mock.py` 를 적용한 구현 커밋 둘(`docs/rust/` 둘 · `rust-kit/` 아홉) → `end_sha` → notes 모의본 → `end_sha` 한 줄 더.
변형 넷은 같은 흐름에 커밋 하나를 더한다: `unsigned-shared`(서명 없이 루트 `README.md`) · `unsigned-mine`(서명 없이 `rust-kit/README.md`) ·
`signed-outside`(서명하고 `rust-kit/.claude-plugin/plugin.json`) · `cross-phase`(서명하고 `harness/skills/sprint/SKILL.md` 와 `rust-kit/skills/rust-test/SKILL.md` 한 커밋).

측정은 이 계약 초안에서 `p9d/extract.py` 로 뗀 도우미 다섯(`p9d/kx/`, 원본 `p9d/k/` 와 `cmp` 로 같다)으로 돌렸다(`p9d/runall.sh` — 공통 정의를 `.` 로 읽고 조건 문구 그대로의 측정).
기본 예행 판 전체 측정은 21 초였다(`p9d/run-base.txt`).

**검토 반영 뒤 다시 잰 값 (2026-09-25).** 검토(`phase9-review.md`)를 반영해 `p9d/mock.py` 를 고쳤다(rust-preflight Step 3.5 둘째 블록 앞 한 문장 · 뒤 한 줄을 두 항목으로 ·
rust-reviewer 미검증 마커 줄에 「막는 것 칸에는 명령과 그 출력을 붙인다(4 요건 3 항)」). 고치기 전 판은 `p9d/mock.pre-review.py` · `p9d/notes-mock.pre-review.md` 다.
이 판에서 도우미 다섯을 다시 떼어(`p9e/k/` — `common.sh` · `new-warnings.sh` · `attr-run.sh` · `ct-run.sh` 는 첫 판과 `cmp` 로 같고, `m.sh` 만 SK-02 · SK-08 · ER-03 · RE-02 갈래가 다르다)
예행 저장소를 새로 만들고(`p9e/rh` · 변형 넷 `p9e/rh-*`) 전 조건을 다시 쟀다(`p9e/run-rev-final.txt` — bash 5.3.9 와 `/bin/bash` 3.2.57 출력이 `cmp` 로 같다).
첫 판과 달라진 값은 SK-02 첫 줄 · ER-03 둘째 줄 · RE-02 둘째 줄 · DG-02 rust-preflight 더한 줄 수뿐이고, 아래 표는 이 판 값이다.

**2 회차 검토 반영 (BUILD, 봉인 전).** 2 회차(`phase9-review.md` `## 2 회차`)가 고칠 것 둘을 냈다 — `common.sh` 가 두 판 풀기 실패에서 멈추고 끝나면 두 판을 지우게,
ER-03 의 넘김 경로 일곱을 `## 넘기는 것` 절 안에서만 세게. 두 도우미 `common.sh` · `m.sh` 가 바뀌었고(나머지 셋은 그대로), 2 회차가 같은 판(`p9r2/kfix/`)을
`HEAD` `a18f6c3` 위 새 예행(`p9r2/rh`)에서 돌려 전 조건 값이 고치기 전과 같았다(`p9r2/run-fix2.txt`). BUILD 는 이 계약에서 다시 뗀 두 도우미가 `p9r2/kfix/` 와 `cmp` 로 같은지
확인했다. 권하는 것 넷 가운데 셋을 반영했다 — rust-preflight Step 3.5 셋째 항목 첫머리 「- 통과하는데」 → 「- `HEAD+내 변경` 이 통과하는데」(`p9d/mock.py` 를
`p9b/mock.py` 로 복사해 그 한 곳만 고쳤다. 어느 조건 토큰에도 없는 구절이라 측정 값이 바뀌지 않는다) · 아래 `범위 경계` 검토 기록 줄 · 스크래치 측정 임시 폴더 정리.
SK-07 `ct-run.sh` 에 E0308 수를 더하는 권장은 반영하지 않았다 — 출력 형식이 `compile_rc=` 한 값에서 바뀌면 SK-07 기대값 문장까지 고쳐야 하고, 빌드 기록 `build.log` 에 오류 줄이 그대로 남는다.

| 조건 | 예행 판 (요구값) | 시작 커밋 판 | 양성 · 음성 대조 |
| --- | --- | --- | --- |
| SK-01 | `1` 일곱 · `1 … 10` · `1` 여섯 · `2` | `0` 일곱 · `1 … 9` · `0` 여섯 · `0` | 문장 삭제 (아래) |
| SK-02 | `1 1 1 2 3 1 1 1 1 1 2 1 1 1 1 1 1 1 1 1` · `1` · `rows_same=1 rows=3` | `0` 스물 · `0` · `rows_same=0 rows=0` | 문장 삭제 · 판정 셋째 줄 「가능성이 크다」 → 「수 있다」 → `rows_same=0 rows=3` · 검토 반영 문장 넷을 하나씩 지운 사본 → 열일곱 ~ 스무째 값이 그 자리만 0 · 셋째 줄 판정 문장을 지운 사본 → 스무째 값 0 (열한째는 2 → 1 이라 이것만으로는 못 잡는다) |
| SK-03 | `A 1 0 0 0 0` · `B 1 0 0 0 1` · `C 1 1 1 1 1` · `D 1 1 0 0 1` · 넷 다 `wt=1 untouched=1` (5 초) | `NO_BLOCK 0` | `cp -p` 지운 사본 → `B 1 0 0 0 0` · `"$ref"` → `HEAD` 사본 → `D 1 1 1 1 1` |
| SK-04 | `17 True rust-preflight 4 3 1 1 1 1` · `rc=0 Total: 17 passed, 0 failed` | `16 True None 0 0 0 0 0 0` · `rc=0 Total: 16 passed, 0 failed` | assertion 하나 `type` → `check` → `… 4 2 …` · `rc=1 Total: 16 passed, 1 failed` |
| SK-05 | `1` 열여섯 · `5 0` · `1` · `1 1` · `0.2.0 2026-09-25` | `0` 열여섯 · `0 0` · `0` · `0 0` · `0.1.0 2026-04-07` | 문장 삭제 |
| SK-06 | `1` 열 · `1 7 0 1` · `1 1 1 1 0 0 0` | `0` 열 · `0 6 0 0` · `0 0 0 0 1 1 1` | 문장 삭제 · 옛 문구 셋이 양성 대조 |
| SK-07 | `new=0 old=0 mixed=101` (한 번에 7 초 안팎 · `mixed` 는 정수) | — | `mixed` 가 음성 대조 — 빌드 기록 `error[E0308]: mismatched types` 두 건 |
| SK-08 | `1 1 1 1 1 \| 1 1 1 1 \| 5` · `1 1 1 0 0` | `1 0 0 1 1 \| 0 0 0 0 \| 5` · `0 0 0 1 1` | 조항 3 의 「같은 조건이 2 iteration … 계약 결함」 을 infra 사본 꼴(「같은 항목이 2 회 … 기준 결함」)로 바꾼 사본 → 셋째 값 0 · 4 요건 4 항 「이 rule 을」 → 「이 기준을」 → 넷째 요건 0 · 조항 1 둘째 줄(「`[정적]` 은 … 대체하지 않는다.」)을 지운 사본 → 첫 값 0 (검토 반영 — 앞부분만 맞으면 통과하던 자르기를 뺐다) |
| SK-09 | `1` · `1` · `1` · `1 1` · `1 1 1 1` · `1 1 1 1` · `1 1 1 1` · `0` | `0` · `0` · `0` · `0 0` · `0 0 0 0` · `0 0 0 0` · `1 1 1 1` · `6` | 여섯 자리마다 네 칸 문구를 깬 사본 → 그 자리 값만 0 (6/6) |
| SK-10 | `1 1 1 1 1 1 0 0` 두 줄 · `1` · `1` · `1 1` | `0 0 0 0 0 0 1 1` 두 줄 · `0` · `0` · `1 1` | 문장 삭제 · 옛 문구 둘이 양성 대조 |
| SK-11 | `1` 열 `0 0` · `14 0` · `2 1 1 2 1 1 1 1` · `1 1 0` | `0` 열 `1 1` · `6 0` · `2 1 1 2 1 1 1 1` · `0 0 1` | 문장 삭제 · 옛 값 셋이 양성 대조 |
| SK-12 | `1 1 2 2 1 1 1 1 1` · `5 0` · `1 1.3.0 2026-09-25` | `0` 아홉 · `0 0` · `0 1.2.0 2026-08-13` | 문장 삭제 |
| SC-00 | `0` | — | 변형 `signed-outside` → 1 |
| ER-01 | `0` · `0` | — | sqlx-patterns.md 끝에 `https://example.invalid/x` → `1` · `0` · notes 끝에 같은 URL → `0` · `1` · notes 를 지운 사본 → `0` · `NOTES_MISSING` |
| ER-02 | `0` (더한 줄 237) | — | rust-preflight 끝에 「이 값이 적용된다」 → 1 |
| ER-03 | `notes_committed=1` · `1` 열일곱 · `0` | — | 변형 `unsigned-shared` · `signed-outside` · `cross-phase` → 셋째 값 1 · `unsigned-mine` 은 0 (루트 공유 파일이 아니라 AR-01 ① 이 잡는다) · 모의 notes 의 넘김 표에서 `harness/skills/sprint/SKILL.md` 줄을 지우고 같은 경로를 `## 반영한 처리 배정표 키` 절 문장에만 남긴 사본 → 둘째 줄 여덟째 값 0 (notes 전체에서 세던 첫 판 측정은 이 사본을 통과시켰다 — 2 회차 `p9r2/er03-ctl.sh`) |
| ER-04 | `1` 열하나 · `1/2 1/2` | — | rust-run 의 `pipefail` 줄을 지운 사본 → 첫 줄 마지막 값 0 |
| AR-01 | `0` · `0 11` · `0` · `SEAL_OK` · `scope_same=1` · `1` | — | `unsigned-mine` ① 1 · `signed-outside` ② `1 11` · `cross-phase` ② `1 11` · SK-01 조건 줄에 빈칸 하나를 더한 사본 ④ `SEAL_BROKEN` |
| AR-02 | `1 1 1 1 1 1 1` | `0 1 1 0 1 0 1` | 알려진 답 — 새로 생기는 제목 셋만 0 |
| AP-01 | `version=0.3.1 0` | — | rust-preflight 끝에 「버전 0.3.1」 → 1 |
| AP-03 | `0/0` 열 | — | Step 3.5 의 여는 `` ```bash `` 하나를 `` ``` `` 로 → 첫 값 `0/1` |
| AP-04 | `1/1` 일곱 | — | rust-preflight `description: >` → `>-` → 첫 값 `0/1` |
| RE-01 | `0` | — | — |
| RE-02 | `0 rust-kit/agents/rust-reviewer.md rust-kit/skills/rust-preflight/SKILL.md` · `four_items_in=rust-kit/agents/rust-reviewer.md` | `0` · `four_items_in=` | rust-model 끝에 Phase 7 표 머리 줄 → 첫 값 1 · rust-audit 끝에 4 요건 네 항목만(제목 없이) → 둘째 줄에 `rust-kit/skills/rust-audit/SKILL.md` 가 더해진다 |
| DG-01 · DG-03 · DG-04 | `0` · `0` · `0` | — | DG-04: `a/b.rs` · `c.sh` · `d.md` → 2 |
| DG-02 | 열 줄 `new_warnings=0` (더한 줄 74 · 2 · 3 · 39 · 13 · 8 · 29 · 11 · 1 · 45) · `json_ok` | — | sqlx-patterns.md 끝에 `#bad heading` → 그 줄 `new_warnings=1` |
| DG-05 | `10 0` · `1 0` · `stale_rc=0 0` | — | `name: rust-preflight` → `nam:` → `10 1` · `zz-test` 스킬을 더한 사본 → `10 1` · `1 1` · 가짜 출력 줄에 `docs/rust/research-log.md` → 셋째 값 1 |
| DG-06 | `scope-isolation: PASS` · `doc-contracts: PASS` · `doc_checked=2 doc_mine=0` · `violators=0 mine=0` | — | 변형 `cross-phase` → `scope-isolation: FAIL` · `violators=1 mine=1` |

문장 삭제 사본(`p9d/del.py`): `m.sh` 의 토큰 가운데 대상 파일에 한 번만 있는 것을 하나씩 지운 사본 98 개 — `DROP` 96 · `NODROP` 2 (검토 반영 판 `p9e/del.py`. 첫 판은 95 개 · `DROP` 93). `NODROP` 둘은 SK-06 의 옛 문구
(`pub created_at: DateTime<Utc>,` · `use chrono::{DateTime, Utc};`)로, §4S 에서 0 이어야 하는 값이고 파일 안 유일한 자리가 §5 도메인 모델(예외)이라 지워도 §4S 값이 그대로다 — 맞는 동작이다.
네 칸 문구는 큰따옴표 토큰이라 따로 깼다(`p9d/del4.py` · 검토 반영 판 `p9e/del4.py`, 둘 다 6/6 `DROP`).
가짜 `tar` 두 개(E 판 `rust-kit/` 을 지우고 1 로 끝남 · `docs/rust/` 만 지우고 0 으로 끝남)를 `PATH` 앞에 둔 사본 → 둘 다 `SNAPSHOT_FAIL` · 종료 2 (2 회차 검토 `p9r2/shim-fail` · `p9r2/shim-partial`).

## Skill

- [ ] SK-01: `rust-kit/skills/rust-preflight/SKILL.md` 가 Gotcha 10 「빨간 clippy · test 를 내 변경 탓으로 단정하지 말고 원인을 셋으로 가른다 (enforcement 등급 E2)」 로 원인 셋(내 변경 · 남의 미커밋 변경 · 기준 커밋에서 이미 실패) · Step 3.5 와 Step 5 리포트 FAIL 행 Details 가리킴 · 「원인을 갈라도 Status 는 FAIL 그대로다」 · 공유 작업 폴더에서 `git stash` 금지와 그 출처 URL · 실측 날짜를 담고, `# Gotchas` 번호가 1 ~ 10 으로 이어지며, `## Preflight Report` 절이 「**FAIL 행의 Details 는 원인으로 시작한다 (Gotcha 10).**」 · 「원인을 적어도 그 행의 Status 와 **Result** 는 FAIL 그대로다」 와 Details 머리 넷(`내 변경 — {내 파일:줄 또는 diff 한 덩어리}` · `남의 미커밋 — {시작 때 떠 둔 목록의 그 파일 줄 + 실패 파일:줄}` · `기준 커밋에서 이미 실패 — {FORK_BASE sha · 명령 · exit · toolchain}` · `[미검증]` — 네 칸, 통제 불가 사유 칸에 「귀속 불명」)을 담고, Step 2 · 3 의 FAIL 줄 두 개가 「- FAIL → 에러 출력 후 중단. 이후 단계 skip. 고치기 전에 Step 3.5 로 원인을 가른다.」 이다 (backend-family:P4 · 근거 파일 §4 권장 4) [exact, enumerated]
      (Given: 개정 파일 `end_sha:` 마지막 값이 정해진 뒤 · When: `type m >/dev/null || exit 2;` 뒤 `m SK-01` · Then: 네 줄이 `1 1 1 1 1 1 1 ` · `1 2 3 4 5 6 7 8 9 10` · `1 1 1 1 1 1 ` · `2`.
       토큰 열셋은 `회귀 게이트` 절 `m.sh` 의 `SK-01)` 갈래에 글자 그대로 있다. 시작 커밋 판은 `0` 일곱 · `1 2 3 4 5 6 7 8 9` · `0` 여섯 · `0`. 봉인 전 실측: `회귀 게이트` 절 표)
- [ ] SK-02: `rust-kit/skills/rust-preflight/SKILL.md` 의 `## 3.5. 실패 원인 가르기 (Step 2 · 3 이 FAIL 일 때 — Gotcha 10)` 절이 `## 3. test 실행` 과 `## 4. audit 검사` 사이에 있고, 두 bash 블록(`git merge-base HEAD origin/<기준 가지>` 로 잡은 `FORK_BASE` · `HEAD` · `origin/<기준 가지>` 세 임시 워크트리를 도는 블록과, `HEAD` 임시 워크트리에 내가 쓴 파일만 얹어 `HEAD+내 변경 exit=` 를 내는 블록) · `<준비 명령>` · 판정 세 줄을 옮겼다는 문장 · 남의 미커밋 확정 조건(작업 시작 때 `git status --porcelain=v1 --untracked-files=all` · 내 경로 밖 · 내가 바꾼 이름을 가리키지 않음) · 확인 못 하면 `[미검증]` 에 「귀속 불명」 · 시작 목록이 없으면 확정하지 않는다는 문장 · 출처 URL 넷(git worktree · git status · git merge-base · Clippy CHANGELOG) · 표 첫 줄 판정 칸의 「남의 미커밋이다」 를 둘째 블록과 세 조건으로 좁히는 문장 · 둘째 블록은 `HEAD` 임시가 통과할 때만 돌린다는 문장 · `HEAD` 임시가 실패하면 둘째 블록으로 가르지 않고 표 둘째 · 셋째 줄로 가르며 셋째 줄의 Details 머리(이번 작업이 만든 커밋이면 `내 변경`, 아니면 `[미검증]` 에 「귀속 불명」)를 정한 문장을 담으며, 판정 표의 머리 줄과 `| 실패 |` 로 시작하는 세 줄이 `$END` 판 `harness/skills/sprint/SKILL.md` `### Step 3: 빌드/분석 검증` 의 같은 줄과 글자 그대로 같다 (backend-family:P4 · F09 — Phase 4 가 정한 정본을 옮긴다) [exact, enumerated]
      (측정: `type m >/dev/null || exit 2;` 뒤 `m SK-02` 세 줄 — 첫 줄 스무 값이 모두 1 이상(봉인 전 실측 `1 1 1 2 3 1 1 1 1 1 2 1 1 1 1 1 1 1 1 1 ` — 넷째 · 다섯째 토큰은 블록 두 개 · 산문에 함께 있어 2 · 3, 열한째 「귀속 불명」 문장은 남의 미커밋 줄 · 셋째 줄 판정 줄 두 곳이라 2 — 그래서 셋째 줄 판정 문장은 스무째 토큰으로 따로 잰다), 둘째 줄 `1`, 셋째 줄 `rows_same=1 rows=3`.
       시작 커밋 판은 `0` 스물 · `0` · `rows_same=0 rows=0`. 봉인 전 실측: `회귀 게이트` 절 표)
- [ ] SK-03: Step 3.5 의 두 bash 블록이 실제로 돌아 원인을 가른다 — `$END` 판 블록을 글자 그대로 떼어 자리표시자 넷만 바꾼 뒤(`<기준 가지>` → `main` · `<준비 명령>` → `true` · `<실패한 검사 명령>` → `cargo check -q --offline` · `<내 경로…>` → `src/mine.rs`) 연습 저장소 네 곳(A 남의 미커밋 · B 내 변경 · C 기준 커밋에서 이미 실패 · D 이번 커밋 탓)에서 돌리면 네 줄이 차례로 `A 1 0 0 0 0` · `B 1 0 0 0 1` · `C 1 1 1 1 1` · `D 1 1 0 0 1` 로 시작하고 넷 다 `wt=1 untouched=1` 로 끝난다 — 열은 공용 작업 폴더 · `HEAD` · `FORK_BASE` · `origin/main` · `HEAD+내 변경` 의 결과(0 통과 · 1 실패), `wt=1` 은 임시 워크트리가 남지 않았다는 뜻, `untouched=1` 은 공용 작업 폴더의 `git status --porcelain` 이 전과 같다는 뜻이다 (backend-family:P4) [goal]
      (측정: `type m >/dev/null || exit 2;` 뒤 `m SK-03` (도우미 `attr-run.sh` — `cargo` 가 없으면 `CARGO_MISSING` 으로 멈춘다).
       알려진 답: 네 상황은 손으로 만든 두 줄짜리 크레이트다 — A 는 남의 `src/other.rs` 만 깨졌고, B 는 내 `src/mine.rs` 만 깨졌고, C 는 기준 가지 `main` 에 깨진 커밋이 먼저 들어갔고, D 는 내 가지에만 깨진 커밋이 있다. 기대값은 이 구성에서 손으로 셌고 봉인 전 실제값이 같았다(종료 코드 0).
       음성 대조: 블록의 `cp -p "$f" "$t/$f"` 를 지운 사본 → B 줄이 `B 1 0 0 0 0` (내 변경을 남의 탓으로 가름) · `git worktree add` 의 `"$ref"` 를 `HEAD` 로 바꾼 사본 → D 줄이 `D 1 1 1 1 1` (이번 커밋 탓을 기준 커밋 탓으로 가름) · 시작 커밋 판 → `NO_BLOCK 0`. 봉인 전 실측: `회귀 게이트` 절 표)
- [ ] SK-04: `rust-kit/evals/evals.json` 에 사례 17(skill `rust-preflight`, assertion 넷 — type 은 `behavior` 셋 · `output` 하나 — 실패하면 임시 워크트리에서 HEAD · FORK_BASE · 기준 가지로 같은 명령을 다시 돌리기 · `HEAD` 에 내가 쓴 파일만 얹어 한 번 더 돌리기 · `git stash` 로 남의 변경을 치우지 않기 · FAIL 행 Details 가 원인 넷 가운데 하나로 시작하고 Status 는 FAIL 그대로)이 더해져 사례가 17 개 · id 1 ~ 17 이고, `$END` 판에서 `scripts/run-evals.py rust-kit` 이 종료 코드 0 · `Total: 17 passed, 0 failed` 이다 (backend-family:P4) [exact]
      (측정: `type m >/dev/null || exit 2;` 뒤 `m SK-04` 두 줄이 `17 True rust-preflight 4 3 1 1 1 1` · `rc=0 Total: 17 passed, 0 failed`. 시작 커밋 판은 `16 True None 0 0 0 0 0 0` · `rc=0 Total: 16 passed, 0 failed`.
       음성 대조: 사례 17 의 assertion 하나의 `type` 을 `check` 로 바꾼 사본에서 둘째 줄이 `rc=1 Total: 16 passed, 1 failed`. 봉인 전 실측: `회귀 게이트` 절 표)
- [ ] SK-05: `docs/rust/data/sqlx-patterns.md` 에 원칙 6 「시각은 종류부터 나누고, 종류마다 Rust 타입과 열 타입을 정한다」 가 원칙 5 뒤 · `## 수치 기준` 앞에 있고, 종류 셋의 정본이 `docs/backend/fundamentals/database.md` 원칙 10 이라는 문장 · 끊기지 않은 다섯 줄 표(머리 `| 시각 종류 | SQLx | SeaORM Entity | PostgreSQL 열 |` · 순간 행에 SQLx `chrono::DateTime<Utc>` 와 SeaORM `DateTimeWithTimeZone` · 벽시계 두 행) · `TIMESTAMPTZ` 가 원래 시간대 이름을 남기지 않는다는 문장 · `sea-orm-cli generate entity` 가 붙이는 타입과 어댑터 변환(`.with_timezone(&Utc)` · `Utc::now().fixed_offset()`) · 실측 문장(sea-orm 1.1.19 · sqlx 0.8.6 · chrono 0.4.44)과 SeaORM 2.x 를 재지 않았다는 문장 · 시간대 · 나라 상수 금지가 RFC 가 아니라 킷 규칙이라는 문장 · 출처 URL 넷(SQLx types · SeaORM 1.1 · SeaORM 2.x · RFC 5545)을 담으며, 안티패턴 절에 「벽시계를 `TIMESTAMPTZ` 순간 하나로만 저장」 이 더해지고 머리 설정이 `0.2.0` · `2026-09-25` 다 (backend-family:P2 rust-model 부분 — rust-kaizen Gotcha 1 이 요구하는 원칙 문서 선행) [exact, enumerated]
      (측정: `type m >/dev/null || exit 2;` 뒤 `m SK-05` 다섯 줄이 `1` 열여섯 개 · `5 0` · `1` · `1 1 ` · `0.2.0 2026-09-25`. 둘째 줄은 원칙 6 절 안 `|` 로 시작하는 줄 수와 끊긴 곳 수다.
       시작 커밋 판은 `0` 열여섯 · `0 0` · `0` · `0 0 ` · `0.1.0 2026-04-07`. 봉인 전 실측: `회귀 게이트` 절 표)
- [ ] SK-06: `rust-kit/skills/rust-model/SKILL.md` 가 `## Gotchas` 에 「시각 컬럼은 종류부터 정하고, ORM 마다 다른 타입 대응을 따른다」 Gotcha(벽시계를 `TIMESTAMPTZ` 순간 하나로만 저장 금지 · `TIMESTAMPTZ` 가 원래 시간대 이름을 남기지 않는다 · IANA 시간대 식별자 열 · 시간대 · 나라 상수 금지 · `sea-orm-cli generate entity` 가 `DateTimeWithTimeZone` 을 붙인다 · `docs/backend/fundamentals/database.md` 원칙 10 과 `docs/rust/data/sqlx-patterns.md` 원칙 6 가리킴 · 출처 URL)를 담고, `## 1. 입력 확인` 표에 `| 시각 필드 종류 |` 행이 끊기지 않게 더해지고, Step 2 타임스탬프 줄이 기존 시각 필드의 종류를 보게 하며, `### §4S — SeaORM 어댑터` 의 Entity 가 `pub created_at: DateTimeWithTimeZone,` 이고 어댑터가 `created_at: m.created_at.with_timezone(&Utc),` · `created_at: Set(Utc::now().fixed_offset()),` · `use chrono::Utc;` 를 쓰며 그 절에 옛 `pub created_at: DateTime<Utc>,` · `use chrono::{DateTime, Utc};` · `Set(chrono::Utc::now())` 가 0 이다. 예외: `## 5. 도메인 모델 구조체 생성` 의 `DateTime<Utc>` 는 도메인 순간이라 그대로 둔다 (backend-family:P2 rust-model 부분 · `phase7-notes.md` 넘김) [exact, enumerated]
      (측정: `type m >/dev/null || exit 2;` 뒤 `m SK-06` 세 줄이 `1` 열 개 · `1 7 0 1` · `1 1 1 1 0 0 0 `. 둘째 줄은 입력 표 새 행 수 · 표 줄 수 · 끊긴 곳 수 · Step 2 새 줄 수다.
       셋째 줄 뒤 세 값은 옛 문구다 — 시작 커밋 판에서 `0 0 0 0 1 1 1 ` (양성 대조). 봉인 전 실측: `회귀 게이트` 절 표)
- [ ] SK-07: `rust-kit/skills/rust-model/SKILL.md` §4S 의 예시가 실제로 컴파일된다 — `$END` 판의 Entity 코드 블록과 어댑터 블록의 `created_at` 두 줄을 글자 그대로 떼어 붙인 시험 크레이트가 sea-orm 1.1.19 · chrono 0.4.44 로 오프라인 컴파일되고(종료 코드 0), 시작 커밋 판도 같은 방식으로 컴파일되며(0), Entity 는 `$END` 판 · 어댑터 두 줄은 시작 커밋 판으로 섞으면 컴파일이 실패한다(0 이 아니다) — 생성기 타입으로 바꾼 Entity 에 옛 어댑터 줄을 붙이면 깨진다는 것을 이 측정이 가려낸다 (backend-family:P2 · 근거 파일 §5 「컴파일 테스트로 확정」) [goal]
      (측정: `type m >/dev/null || exit 2;` 뒤 `m SK-07` 이 `new=0 old=0 mixed=N` 이고 N 이 0 이 아닌 정수다 — `EXTRACT_FAIL` · `CARGO_MISSING` 같은 글자는 N 이 아니다(봉인 전 실측 `mixed=101`, 빌드 기록 `error[E0308]: mismatched types` 두 건). 도우미 `ct-run.sh` — `cargo` 가 없으면 `CARGO_MISSING`, 블록을 못 떼면 `EXTRACT_FAIL` 로 멈춘다.
       음성 대조: 위 `mixed` 가 그것이다 — 어댑터 두 줄만 옛 판이면 실패한다. 봉인 전 실측: `회귀 게이트` 절 표)
- [ ] SK-08: `rust-kit/agents/rust-reviewer.md` 의 `## 미검증 증거 프로토콜 (정본 복제 — 재정의 금지)` 조항 1 ~ 5 본문이 `$END` 판 `harness/docs/guides/qa-evaluation-guide.md` §Canonical Unverified-Evidence Protocol 의 같은 조항(마커 · 두 분류 · 임계값 2 는 `UNVERIFIED_INVALID_EVIDENCE` 에만 · 생성자의 완료 주장 · 조용한 PASS 금지)과 번호 · 들여쓰기를 뺀 글자 단위로 같고(조항 1 은 정본의 첫 두 줄), 「### `UNVERIFIED_ENV` 남용 방지 4 요건 (하나라도 없으면 `INVALID` 로 강등 · 정본 복제)」 절의 1 ~ 3 항이 `backend-kit/agents/backend-reviewer.md` 사본과 같고 4 항은 예시 앞까지 같으며, 재동기화 기록 줄과 옮기지 않은 것(정본 조항 1 의 N/A 표 · 정본의 새 조항 2)을 적은 줄이 있고, 옛 「**임계값은 2 다.**」 · 「(3 분기: FAIL / 도구 부재 / 증거 무효)」 가 0 이다 (편집 전 감사 · 2026-08-14 REJECT 와 같은 모양) [exact, enumerated]
      (측정: `type m >/dev/null || exit 2;` 뒤 `m SK-08` 두 줄이 `1 1 1 1 1 | 1 1 1 1 | 5` · `1 1 1 0 0 `. 첫 줄 앞 다섯 값이 조항 1 ~ 5 의 일치, 가운데 넷이 4 요건 1 ~ 4 항, 끝이 사본 조항 수다.
       시작 커밋 판은 `1 0 0 1 1 | 0 0 0 0 | 5` · `0 0 0 1 1 ` (양성 대조 — 옛 조항 2 · 3 이 정본과 달라 0). 봉인 전 실측: `회귀 게이트` 절 표)
- [ ] SK-09: rust-kit 의 `[미검증]` 이 설계 가이드 §3.7 3 항 · agent-design-guide §10 정책 2 항과 같은 네 칸(막는 것 · 시도한 우회 · 통제 불가 사유 · 재검증 명령)을 쓴다 — (a) `rust-kit/skills/rust-preflight/SKILL.md` `## 2.5.` 절의 DB 미기동 줄 (b) 같은 파일 `## Preflight Report` 의 종료 코드 줄 (c) `rust-kit/skills/rust-run/SKILL.md` 의 종료 코드를 못 얻은 줄 (d) `rust-kit/skills/rust-test/SKILL.md` `## After Creation` 5 항과 「돌릴 수 있는데 안 돌렸으면 `[미검증]` 이 아니다」 (e) `rust-kit/agents/rust-reviewer.md` 의 「미검증 항목 마커 (agent-design-guide §10)」 줄(`[미검증:ENV]` 또는 `[미검증:INVALID]` · 네 칸 예시 · 하나라도 비면 INVALID) (f) `rust-kit/skills/rust-audit/SKILL.md` Gotcha 14(네 칸 · 비면 INVALID · `(Step 5 참조)` · 복제본 `rust-kit/agents/rust-reviewer.md` §미검증 증거 프로토콜 가리킴)이며, 칸 이름은 `$END` 판 `harness/docs/guides/skill-design-guide.md` 의 네 칸 줄과 같고, `rust-kit/` 전체에 옛 꼴 일곱(`[미검증] 종료 코드 캡처 실패` · `[미검증] DB 미기동` · `[미검증] 테스트 미실행` · 「사유를 Details 에 남긴다」 · 「"근거" 컬럼에 이유를 기술한다」 · 「근거에 이유를 기술하라」 · 「CONDITIONAL APPROVE 규칙을 적용한다 (Step 4 참조)」)이 든 줄이 0 이다 (Phase 1 넘김 `rust-reviewer.md:137` + 전수 감사 다섯 자리) [exact, enumerated]
      (측정: `type m >/dev/null || exit 2;` 뒤 `m SK-09` 여덟 줄이 `1 ` · `1 ` · `1 ` · `1 1 ` · `1 1 1 1 ` · `1 1 1 1 ` · `1 1 1 1 ` · `0`.
       일곱째 줄은 가이드의 칸 이름 넷이고, 여덟째 줄은 옛 꼴이 든 줄 수다 — 시작 커밋 판에서 `6` (양성 대조 — Gotcha 14 한 줄에 옛 꼴이 둘). 봉인 전 실측: `회귀 게이트` 절 표)
- [ ] SK-10: rust-reviewer 와 rust-audit 의 최종 판정이 카운터 둘로 판정한다 — `rust-kit/agents/rust-reviewer.md` `## 최종 판정` 과 `rust-kit/skills/rust-audit/SKILL.md` `## 5. 최종 판정` 이 각각 (a) 「카운터는 두 개이며 **합산하지 않는다** (정본 조항 3): …」 문장 (b) APPROVE · CONDITIONAL APPROVE · REJECT 가 `UNVERIFIED_INVALID_EVIDENCE` 로 판정 (c) BLOCKED 줄 (d) 무효 증거를 `UNVERIFIED_INVALID_EVIDENCE` 카운터에 합산하는 줄을 담고 옛 「미검증 태그 0 건」 · 「무효 K 건은 미검증 카운터에 합산」 이 0 이며, rust-reviewer 는 미검증 수를 두 카운터로 적고 rust-audit 는 `env_gaps` 에 4 요건이 필요하다고 적으며, (a) · (c) 두 문장이 `backend-kit/skills/backend-audit/SKILL.md` 에 글자 그대로 있다 (rust-audit Gotcha 17 형제 parity · Counterpart producer · consumer) [exact, enumerated]
      (측정: `type m >/dev/null || exit 2;` 뒤 `m SK-10` 다섯 줄이 `1 1 1 1 1 1 0 0 ` · `1 1 1 1 1 1 0 0 ` · `1 ` · `1 ` · `1 1 `.
       첫 두 줄 끝 두 값이 옛 문구다 — 시작 커밋 판에서 `… 1 1 ` (양성 대조). 봉인 전 실측: `회귀 게이트` 절 표)
- [ ] SK-11: 버전 현행화 — `rust-kit/references/project-detection.md` `## Step 2c. 버전 현행성 확인` 표 머리가 「조회 시점 최신 (crates.io · 2026-09-24)」 이고 `sea-orm` 2.0.3 행과 새 행 여덟(`tonic` · `tower-http` · `utoipa` · `rust-i18n` · OTel · `mockall` · `rstest` · Rust stable)이 근거 파일 §3 값으로 있으며, 옛 「| `sea-orm` | 2.0.1 |」 · 「docs.rs latest · 2026-08-13」 이 0 이고 표가 끊기지 않은 열네 줄이며, 새 행 여덟의 「전제하는 버전」 값이 스킬에 실제로 남아 있고(스킬 본문 리터럴은 바꾸지 않는다. 옛 행 넷은 이번에 재지 않는다 — `testcontainers` 의 0.27 은 이미 스킬에 없다), `rust-kit/skills/rust-grpc/SKILL.md` Gotcha 5 가 `tonic-health = "0.14"` · `tonic-reflection = "0.14"` 와 Step 2c 가리킴을 담고 그 파일에 `"0.13"` 이 0 이다 (근거 파일 §3) [exact, enumerated]
      (측정: `type m >/dev/null || exit 2;` 뒤 `m SK-11` 네 줄 — `1 1 1 1 1 1 1 1 1 1 0 0 ` · `14 0` · 여덟 값이 모두 1 이상(봉인 전 실측 `2 1 1 2 1 1 1 1` — tower-http 0.6 · utoipa 5.4 · utoipa-scalar 0.3 · rust-i18n 3 · OTel 0.31 · mockall 0.13 · toolchain 1.88.0 이 든 스킬 파일 수와 rust-test 의 rstest 0.26 줄 수) · `1 1 0`.
       시작 커밋 판은 `0` 열 · `1 1 ` · `6 0` · 같은 여덟 값 · `0 0 1` (양성 대조). 봉인 전 실측: `회귀 게이트` 절 표)
- [ ] SK-12: `docs/rust/research-log.md` 의 첫 항목이 `## [2026-09-24] — Phase 9 kaizen` 이고 근거 파일 경로 · 처리 배정표 키 `backend-family:P4` · `backend-family:P2` · `### 봉인 전 실측` 절과 그 표(SeaORM 1.1.19 열 타입 추론 행) · `### 버전 현행성 (crates.io · 2026-09-24)` · `### 미반영` 과 rust-audit 시각 판정 행 미반영을 담으며 표가 끊기지 않고, 머리 설정이 `1.3.0` · `2026-09-25` 다 (rust-kaizen Step 5 커밋 기록 · 오케스트레이터 per-kit research-log 규칙) [exact, enumerated]
      (측정: `type m >/dev/null || exit 2;` 뒤 `m SK-12` 세 줄 — 첫 줄 아홉 값이 모두 1 이상(봉인 전 실측 `1 1 2 2 1 1 1 1 1 `) · `5 0` · `1 1.3.0 2026-09-25`. 시작 커밋 판은 `0` 아홉 · `0 0` · `0 1.2.0 2026-08-13`. 봉인 전 실측: `회귀 게이트` 절 표)

## Script

- [ ] SC-00: N/A (Script 카테고리는 `release.sh` 연동 · 버전 올림 · `marketplace.json` 갱신이다. 이 Phase 는 그 파일을 건드리지 않는다 — 공유 파일은 Final 몫. 측정: `type my >/dev/null || exit 2;` 뒤 `my | grep -cE '^(scripts/release\.sh|\.claude-plugin/marketplace\.json|[^/]+/\.claude-plugin/plugin\.json)$'` 이 0. 양성 대조: 예행 변형 `signed-outside` 에서 1)

## Error

- [ ] ER-01: 열한 파일에 새로 생긴 URL 과 `.harness/.meta/kaizen-0924/phase9-notes.md` 의 URL 이 전부 이 Phase 의 외부 근거 파일 `.harness/.meta/evidence/phase9.md` 에 있다 — 열한 파일은 파일마다 편집 전 판과 비교한다 (러닝북 — notes 킷 로그 한 단락의 출처 URL 은 근거 파일에서만) [exact, enumerated]
      (측정: `type m >/dev/null || exit 2;` 뒤 `m ER-01` 두 줄이 `0` · `0`. 첫 줄은 열한 파일을 파일마다 비교해 다른 파일에 이미 있던 URL 을 새로 더한 경우도 본다. 둘째 줄은 notes 의 URL 전부이고, notes 가 `$END` 판에 없으면 `NOTES_MISSING` 이라 FAIL 이다.
       봉인 전 실측: `회귀 게이트` 절 표. 양성 대조: 예행 판 sqlx-patterns.md 끝에 `https://example.invalid/x` 를 더하면 첫 줄 1, notes 끝에 같은 URL 을 더하면 둘째 줄 1, notes 를 지운 사본에서 둘째 줄 `NOTES_MISSING`)
- [ ] ER-02: 열한 파일에 더한 줄에 번역투 6 종(`tone-kit/references/locale-korean.md` §2 치환표의 grep 열)이 0 건이다. 예외: `$END` 판 `harness/docs/guides/qa-evaluation-guide.md` 에 글자 그대로 있는 줄(정본 복제 — 사본 문구를 바꾸면 SK-08 이 깨진다. 정본 문구는 Phase 3 몫)은 세지 않는다 [exact]
      (측정: `type m >/dev/null || exit 2;` 뒤 `m ER-02` 가 0. 봉인 전 실측: 예행 판 더한 줄 237 개에서 0 — 예외로 빠진 줄은 정본 조항 3 첫 줄(「적용된다」) 하나다. 첫 초안의 「각 FAIL 에 대해」 두 줄은 이 측정이 잡아 「FAIL 마다」 로 고쳤다.
       양성 대조: rust-preflight 끝에 「이 값이 적용된다」 를 더하면 1)
- [ ] ER-03: 이 Phase 범위 밖 반대편을 명시적 미완으로 넘기고 건드리지 않는다 — `.harness/.meta/kaizen-0924/phase9-notes.md` 가 `$END` 에 커밋돼 있고 열일곱 문자열(처리 배정표 키 `backend-family:P4` · `backend-family:P2` · `F09` · 넘김 `rust-kit/skills/rust-audit/references/audit-criteria.md` (다음 사이클 — 시각 종류 판정 행, 근거 파일 §4 권장 7) · `rust-kit/skills/rust-init/SKILL.md` (다음 사이클 — 버전 리터럴을 Step 2c 참조로, 근거 파일 §4 권장 8) · `.claude/skills/rust-kaizen/SKILL.md` (다음 사이클 — Gotcha 6 형제 표에 「실패 원인 셋」 · 「미검증 두 카운터」 행, Gotcha 9 AR-02 검사가 자기 파일을 잡는 문제) · `harness/docs/guides/qa-evaluation-guide.md` (다음 사이클 Phase 3 — drift 메모의 rust-reviewer 줄 · 정본 번호 3 중복 · 새 조항 2 의 킷 적용) · `harness/skills/sprint/SKILL.md` (다음 사이클 Phase 4 — Step 3 표 첫 줄 「내가 쓴 목록 밖이면 남의 미커밋이다」 가 근거 파일 §4 권장 2 보다 느슨하다. rust-preflight 는 표 밖 문장으로 좁혔다) · `docs/rust-kit/sqlx-patterns.html` (Final F2) · `plugin.json` (Final — rust-kit 버전) · `SeaORM 2.x` (미반영 사유) 와 러닝북이 적게 한 절 머리 `## 반영한 처리 배정표 키` · `## 미반영 키와 사유` · `## 넘기는 것` · `## changelog 한 단락` · `## 킷 로그 한 단락` · `## 다음 사이클 메모`)을 각각 1 회 이상 담고 — 넘김 일곱(`rust-kit/skills/rust-audit/references/audit-criteria.md` 부터 `plugin.json` 까지)은 `## 넘기는 것` 절 안에서 센다 —, 구간 안에서 공유 파일 · 다른 Phase 파일을 건드린 커밋 가운데 다른 Phase 서명이 없는 커밋이 0 개다 [exact, enumerated]
      (Given: BUILD 가 notes 를 커밋하고 개정 파일에 그 sha 로 `end_sha:` 를 덧붙인 뒤 · When: `type m >/dev/null || exit 2; type not_other >/dev/null || exit 2;` 뒤 `m ER-03` · Then: 세 줄이 `notes_committed=1` · `1` 열일곱 개 · `0`.
       셋째 값의 경로는 `m.sh` `ER-03)` 갈래의 `not_other` 인자 열넷이다 — 서명 줄 목록이 아니라 경로로 직접 세므로 서명을 빠뜨린 커밋도 보인다. 다른 Phase 서명이 달린 커밋은 그 Phase 몫이라 뺀다.
       봉인 전 실측: 예행 판 `notes_committed=1` · 열일곱 모두 1 · 0. 음성 대조: 모의 notes 의 넘김 표에서 `harness/skills/sprint/SKILL.md` 줄을 지우고 같은 경로를 `## 반영한 처리 배정표 키` 절 문장에만 남긴 사본 → 둘째 줄 여덟째 값 0 (notes 전체에서 세던 첫 판 측정은 이 사본을 통과시켰다). 양성 대조: 변형 `unsigned-shared` 1 · `signed-outside` 1 · `cross-phase` 1. 예행의 다른 Phase 서명 커밋(`infra-kit/README.md`)은 인자 밖이라 0 에 영향이 없다)
- [ ] ER-04: rust-kaizen Gotcha 9 의 회귀 검사가 그대로 성립한다 — `$END` 판에서 (a) 1 이상이어야 하는 열하나(H-01 `domain event\|outbox` 가 rust-init · rust-feature · H-03 `Composition Root` 가 rust-api · DG-03 `마이그레이션` 이 rust-preflight · rust-test · API-01 `MockDatabase` 와 「통합 테스트로 주장하지 마라」 가 rust-test · `--bins` 가 rust-run · rust-test · project-detection · exit-code `pipefail` 이 rust-run)가 모두 1 이상이고 (b) 금지 예시 문맥에만 있어 편집 전에도 0 이 아니던 둘(SK-03 `State<PgPool>…` 줄 수 · Axum 0.7 path 예시 줄 수)이 시작 커밋 판과 같다. AR-02 리서치 문서 수 검사는 뺀다 — 레포 전체를 grep 해 rust-kaizen 파일 자신을 잡는다(ER-03 넘김) [exact, enumerated]
      (측정: `type m >/dev/null || exit 2;` 뒤 `m ER-04` 두 줄이 `1 1 1 1 1 1 1 1 1 1 1 ` · `1/2 1/2 ` (앞이 시작 커밋 판, 뒤가 `$END` 판 — 둘이 같아야 한다).
       양성 대조: rust-run 의 `pipefail` 세 줄을 지운 사본에서 첫 줄 마지막 값 0. 봉인 전 실측: `회귀 게이트` 절 표)

## Architecture

- [ ] AR-01: 이 Phase 의 변경이 허용 경로 안에 머물고, 범위 선언 블록이 그 경로와 같으며, 이 계약이 봉인돼 있다 [exact, enumerated]
      (Given: BUILD 가 개정 파일에 `end_sha:` 를 적은 뒤 · 이 Phase 커밋 메시지마다 서명 줄 `Kaizen-Phase: kaizen-0924-p09-rust-kit` · When: `type m >/dev/null || exit 2; type unsigned_on >/dev/null || exit 2; type verify_seal >/dev/null || exit 2;` 뒤 `m AR-01` · Then: 여섯 줄이 —
       ① `0` — `rust-kit/` · `docs/rust/` 를 건드린 구간 안 커밋이 전부 서명했다(이 구간에 두 폴더를 고칠 수 있는 Phase 는 9 하나다)
       ② `0 11` — 서명 커밋이 건드린 `.harness/` 밖 경로 가운데 열한 파일 밖이 0 개, 열한 파일이 전부 있다
       ③ `0` — `harness/references/contract-schema.md` §`.harness/` 범위 조건 의 권장 형태로 `.harness/` 의 계약 전부에 `verify_seal` 을 돌려 이 Phase 몫 `SEAL_BROKEN` 이 0 개
       ④ `SEAL_OK` — `$END` 판의 이 계약이 봉인돼 있다(`SEAL_ABSENT` 는 봉인을 건너뛴 것이라 FAIL)
       ⑤ `scope_same=1` — `## 범위 경계` 절 `# sprint-scope` 블록의 `.harness/` 밖 줄이 `FILES` 열한 줄과 같다 ⑥ `1` — 그 블록에 `.harness/` 줄이 하나 있다.
       봉인 전 실측: 예행 판 `0` · `0 11` · `0` · `SEAL_OK` · `scope_same=1` · `1`. 양성 대조: 변형 `unsigned-mine` ① 1 · 변형 `signed-outside` ② `1 11` · 조건 줄 한 글자를 바꾼 사본 ④ `SEAL_BROKEN`)
- [ ] AR-02: 새 문장이 가리키는 자리가 그 파일에 있다 — (a) rust-model Gotcha 가 가리키는 `docs/rust/data/sqlx-patterns.md` 에 `### 6. 시각은 종류부터 나누고` 제목 (b) 원칙 6 이 가리키는 `docs/backend/fundamentals/database.md` 에 `### 10. 시각은` 제목 (c) rust-audit Gotcha 14 가 가리키는 `rust-kit/agents/rust-reviewer.md` 에 `## 미검증 증거 프로토콜 (정본 복제 — 재정의 금지)` 제목 (d) rust-audit Step 5 와 rust-reviewer `:93` 이 가리키는 「### `UNVERIFIED_ENV` 남용 방지 4 요건」 제목이 rust-reviewer 에 (e) rust-grpc Gotcha 5 · rust-model §0a 가 가리키는 `rust-kit/references/project-detection.md` 에 `## Step 2c. 버전 현행성 확인` 제목 (f) rust-preflight Gotcha 10 · Step 2 · 3 이 가리키는 `## 3.5. 실패 원인 가르기` 제목 (g) rust-reviewer 의 「미검증 프로토콜의 4 요건을 그대로 적용한다」 줄이 그대로 — 가 각각 한 개다 (Counterpart — 소비면) [exact, enumerated]
      (측정: `type m >/dev/null || exit 2;` 뒤 `m AR-02` 가 `1 1 1 1 1 1 1`. 알려진 답: 시작 커밋 판은 새로 생기는 제목 셋((a) · (d) · (f))만 없어 `0 1 1 0 1 0 1`)

## Anti-patterns

- [ ] AP-01: 버전을 하드코딩하지 않는다 — plugin.json에서 읽어야 한다. 이번 변경에 적용: 열한 파일에 더한 줄에 rust-kit `plugin.json` 의 `version` 값(`$END` 판에서 읽는다)이 0 건이다 — 이 Phase 는 킷 버전을 적지 않고 Final 이 올린다 [exact]
      (측정: `type m >/dev/null || exit 2;` 뒤 `m AP-01` 이 `version=0.3.1 0`. 양성 대조: rust-preflight 끝에 「버전 0.3.1」 을 더하면 둘째 값 1. Step 2c 표의 새 값(0.33.0 · 0.34.0 · 0.3 등)은 이 문자열을 담지 않는다 — 봉인 전 실측 0)
- [ ] AP-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수 (```` ```text, ```bash, ```yaml ```` 등). 판정 권위는 validate-plugin V6 상태기계다 — 여는/닫는 fence 가 동형이라 줄 단위 정규식으로는 판정 불가. 이번 변경에 적용: 마크다운 열 파일마다 언어 힌트 없는 여는 펜스 수가 편집 전과 뒤 모두 0 이다 — rust-preflight 의 새 블록 둘은 `bash` 를 단다. 여는 줄과 닫는 줄은 V6 와 같은 상태 방식으로 가르고, rust-kit 쪽은 DG-05 의 V6 가 함께 본다 [exact]
      (측정: `type m >/dev/null || exit 2;` 뒤 `m AP-03` 이 `0/0` 열 개. 양성 대조: rust-preflight Step 3.5 의 여는 `` ```bash `` 하나를 `` ``` `` 로 바꾼 사본에서 첫 값이 `0/1`)
- [ ] AP-04: SKILL.md / agents/*.md frontmatter 에서 name 필드 누락 — validate-plugin V1 FAIL. 이번 변경에 적용: 고친 SKILL.md 여섯(rust-preflight · rust-run · rust-test · rust-audit · rust-model · rust-grpc)과 rust-reviewer 의 첫 frontmatter 블록이 편집 전과 글자 그대로 같고 `name: <폴더 또는 파일 이름>` 줄이 1 개씩이다 — 그래서 README AUTO 구간과 트리거 설명이 읽는 값도 바뀌지 않는다 [exact]
      (측정: `type m >/dev/null || exit 2;` 뒤 `m AP-04` 가 `1/1` 일곱 개. 음성 대조: rust-preflight `description: >` 한 글자를 바꾼 사본에서 첫 값 `0/1` · 그 판을 DG-05 가 잡지는 않는다 — frontmatter 변경은 이 조건이 잰다)

## Reusability

- [ ] RE-01: N/A (재사용 단위 코드 — 컴포넌트 · 함수 · 모듈 — 가 없다. 변경 파일이 문서 · 평가 사례 데이터뿐이다. 측정: `printf '%s\n' "${FILES[@]}" | grep -cvE '\.(md|json)$'` 이 0)
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다. 이번 변경에 적용: 새 규칙마다 본문을 한 곳에만 둔다 — (a) 시각 종류 셋의 정의 표(Phase 7 머리 줄 「| 시각 종류 | 예 | 저장 형태 (PostgreSQL) | 순간이 필요할 때 |」)를 rust-kit · `docs/rust/` 에 다시 쓰지 않고 `docs/backend/fundamentals/database.md` 원칙 10 을 가리킨다 (b) 남용 방지 4 요건 사본은 rust-kit 안에 `rust-kit/agents/rust-reviewer.md` 하나이고(제목으로 한 번, 제목 없이 항목만 옮긴 사본을 잡으려고 1 항 머리 「**1 차 도구 시도 기록**」 으로 한 번 더 센다) rust-audit 는 그곳을 가리킨다 (c) 판정 세 줄 사본은 rust-kit 안에 `rust-kit/skills/rust-preflight/SKILL.md` 하나다 [exact, enumerated]
      (측정: `type m >/dev/null || exit 2;` 뒤 `m RE-02` 두 줄이 `0 rust-kit/agents/rust-reviewer.md rust-kit/skills/rust-preflight/SKILL.md` · `four_items_in=rust-kit/agents/rust-reviewer.md`. 시작 커밋 판은 `0` · `four_items_in=`. 양성 대조: rust-model 에 (a) 의 머리 줄을 더한 사본에서 첫 값 1 · rust-audit 에 4 요건 네 항목만 제목 없이 더한 사본에서 둘째 줄 `four_items_in=rust-kit/agents/rust-reviewer.md rust-kit/skills/rust-audit/SKILL.md`)

## Diagnostics

- [ ] DG-01: N/A (`commands.analyze` 는 `bash -n scripts/release.sh` 라 `scripts/release.sh` 만 잰다 — 이번 변경 파일과 교집합 0 개. 측정: `type my >/dev/null || exit 2;` 뒤 `my | grep -c '^scripts/release.sh$'` 이 0. 실제 검사는 DG-02 · DG-05)
- [ ] DG-02: IDE diagnostics 워닝/인포 0개 (`diagnostics.ide_exclude` 값 `[]`) — 이번 변경에 적용: 편집기 마크다운 확장과 같은 조건(markdownlint-cli2 0.23.2 · MD013 끔)으로 마크다운 열 파일의 **더한 줄**에 걸린 경고가 0 이고, `rust-kit/evals/evals.json` 이 JSON 으로 읽힌다. 편집 전부터 있던 경고는 `범위 경계` 절에 적은 대로 범위 밖이다 [exact]
      (측정: `type m >/dev/null || exit 2;` 뒤 `m DG-02` 의 열 줄이 모두 `new_warnings=0` 으로 끝나고 `LINT_NOT_RUN` 줄 0 · 마지막 줄 `json_ok`.
       봉인 전 실측: `회귀 게이트` 절 표. 양성 대조: sqlx-patterns.md 끝에 `#bad heading` 을 더하면 그 줄 `new_warnings` 가 1 이상)
- [ ] DG-03: N/A (`commands.test` 는 `bash scripts/release.sh 2>&1 || true` 라 `scripts/release.sh` 만 잰다 — 교집합 0 개. 측정: DG-01 과 같은 명령 `type my >/dev/null || exit 2;` 뒤 `my | grep -c '^scripts/release.sh$'` 이 0. 실제 시험은 SK-03 · SK-04 · SK-07 · DG-05)
- [ ] DG-04: N/A (구동할 앱 · 서버가 없다 — 변경이 문서와 평가 사례 데이터뿐이다. SK-03 · SK-07 의 연습 저장소와 시험 크레이트는 측정 도구가 스크래치에 만든다. 측정: `type my >/dev/null || exit 2;` 뒤 `my | grep -cE '\.(dart|ts|tsx|js|rs|go|py|sh)$'` 이 0. 양성 대조: 같은 `grep -cE` 에 `a/b.rs` · `c.sh` · `d.md` 세 줄을 넣으면 2)
- [ ] DG-05: 저장소 검사가 이 킷을 문제로 가리키지 않는다 — `$END` 판을 git 저장소로 만든 사본에서 (a) `scripts/validate-plugin.py rust-kit` 출력에 `V1` ~ `V10` 열 줄이 있고 하나도 `ERROR` · `FAIL` 이 아니다 (b) `scripts/sync-evals.py --check-only` 출력에 `→ rust-kit` 머리 줄이 있고 그 아래 어긋남 줄이 0 이다 (c) `scripts/check-stale-values.py` 가 종료 코드 0 또는 1 이고 출력에 열한 파일 경로가 0 건이다. 킷 전체를 보는 검사는 이 킷 몫의 줄만 센다 — 같은 구간에 다른 Phase 가 올린 변경 때문에 떨어지지 않게 한다. `sync-docs.py` 는 넣지 않는다 — rust-kit README AUTO 구간이 읽는 frontmatter 가 그대로인지는 AP-04 가 잰다 [exact]
      (측정: `type m >/dev/null || exit 2;` 뒤 `m DG-05` 세 줄이 `10 0` · `1 0` · `stale_rc=0 0` (stale_rc 는 0 또는 1).
       봉인 전 실측: `회귀 게이트` 절 표. 음성 대조: rust-preflight 의 `name: rust-preflight` 를 `nam:` 으로 깬 사본에서 첫 줄 `10 1`.
       양성 대조: `rust-kit/skills/zz-test/SKILL.md` 를 더한 사본에서 둘째 줄 `1 1` · 출력에 `docs/rust/research-log.md` 가 든 가짜 줄을 넣으면 셋째 값 1)
- [ ] DG-06: `python3 scripts/validate-post-kaizen.py --since 4a8ec55f4d874eaaed083af9621f9679693cbdb6` 출력의 `scope-isolation` · `doc-contracts` 줄이 `FAIL` · `ERROR` 가 아니다. `docs-site-regen` 은 Final F2 몫이라 판정에서 뺀다. 다른 Phase 커밋 때문에 `scope-isolation` 이 FAIL 이면 `--verbose` 위반 커밋 목록을 1 개 이상 읽었고 그 가운데 서명 줄 커밋이 0 개일 때, `doc-contracts` 가 FAIL · ERROR 이면 `validate-doc-contracts.py -v` 가 검사한 경로를 1 개 이상 읽었고 그 가운데 이 Phase 서명 커밋이 건드린 경로가 0 개일 때 이 조건은 PASS 다 — 둘 다 근거에 다른 Phase 몫이라고 적는다 [exact]
      (Given: 작업 폴더에서 `$END` 이후 커밋이 있어도 된다 — 검사는 `HEAD` 까지 보지만 판정은 이 Phase 서명 커밋만 센다 · When: `type m >/dev/null || exit 2;` 뒤 `m DG-06` · Then: 네 줄이 `scope-isolation: PASS` · `doc-contracts: PASS` · `doc_checked=N doc_mine=0` · `violators=V mine=0` 이고 N 이 1 이상. 위 가르기로 PASS 를 줄 때만 첫 두 줄에 `FAIL` 이 있어도 되며, scope-isolation 이 `FAIL` 이면 V 가 1 이상이어야 한다(목록을 못 읽으면 mine 이 조용히 0 이 되므로).
       봉인 전 실측: `회귀 게이트` 절 표. 양성 대조: 변형 `cross-phase` 에서 `scope-isolation: FAIL` · `violators=1 mine=1`)
