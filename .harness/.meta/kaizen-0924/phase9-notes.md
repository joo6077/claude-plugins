# 카이젠 2026-09-24 Phase 9 (rust-kit) — notes

- 계약: `.harness/sprint-contract-kaizen-0924-p09-rust-kit.md` (조건 30 · 기능 조건 20, 봉인 `sha256:6b5ad48a301bc7e4` · `locked_at` 2026-09-25 08:01)
- 개정: `.harness/sprint-amendments-kaizen-0924-p09-rust-kit.md` (조건 변경 0 건, `end_sha` 만)
- 검토: `.harness/.meta/kaizen-0924/phase9-review.md` (1 회차 CHANGES 고칠 것 넷 · 권장 넷은 초안이 반영, 2 회차 CHANGES 고칠 것 둘 · 권장 넷 가운데 셋은 BUILD 가 봉인 전에 반영)
- 시작 커밋 `4a8ec55f4d874eaaed083af9621f9679693cbdb6`
- 계약 피드백: `~/.harness/feedback/contract/5a24cc99-2026-09-25T080451-de8c7935-48083.yaml` (`verify-feedback.sh` PASS). 초안은 `.harness/feedback-draft-p09.yaml` 로 갈라 썼고 저장 스크립트가 지웠다

## 커밋

| 커밋 | 내용 | 파일 |
| --- | --- | --- |
| `bb82af8` | 봉인 커밋 | 계약 1 개 |
| `aaa59eb` | sqlx-patterns 원칙 6 · research-log | `docs/rust/` 둘 |
| `c0342a5` | preflight 실패 원인 셋 · 시각 컬럼 Gotcha · 미검증 네 칸과 두 카운터 · Step 2c 현행화 · 평가 사례 17 | `rust-kit/` 아홉 |
| `d88c35a` | 개정 파일에 `end_sha` (`c0342a5`) | 개정 1 개 |
| 이 파일의 커밋 | notes · 검토 기록 | `.harness/` 두 개 |
| 그다음 커밋 | 개정 파일에 notes 커밋 sha 로 `end_sha` 한 줄 더 | 개정 1 개 |

모든 커밋 메시지 끝 문단에 `Kaizen-Phase: kaizen-0924-p09-rust-kit` 줄이 있다. 구현 커밋은 `git add -- <파일…> && git commit -o -- <파일…>` 로 내 경로만 실었다.
**FIX 가 커밋을 더할 때도 서명 줄을 넣고, 개정 파일에 `end_sha:` 줄을 덧붙인다.**

구현은 초안의 모의 편집(스크래치 `p9d/mock.py`, 치환 33)을 복사해 2 회차 검토 권장 1 한 곳만 고친 `p9b/mock.py` 를 작업 폴더에 그대로 돌렸다 — `mock applied 33`,
더한 줄 237. 돌린 뒤 열한 파일이 2 회차 검토의 예행 저장소 `p9r2/rh` 의 같은 파일과 `cmp` 로 같았고, rust-preflight 만 그 한 줄(「- `HEAD+내 변경` 이 통과하는데 …」)이 달랐다.
30 조건 측정은 봉인 커밋 판 계약에서 뗀 묶음으로 돌렸다 — 스크래치 `p9b/ks/`(도우미 다섯, 2 회차 검토의 `p9r2/kfix/` 와 `cmp` 로 같다) ·
`p9b/run.sh`(`TMPDIR` 를 스크래치로 두고 공통 정의를 `.` 로 읽은 뒤 `type` 으로 도우미 다섯을 확인하고 `m <조건 ID>`). QA 가 같은 묶음을 다시 돌릴 수 있다.

디스크 여유 공간이 봉인 전 440 MiB 였다. 이 Phase 의 측정 임시 폴더(`p9d/tmp` · `p9e/tmp`)와 1 회차 검토의 빌드 캐시 사본(`p9r/ct-target`)을 지워 2.2 GiB 로 늘린 뒤 측정했다.
공통 정의는 이제 끝날 때 두 판 폴더를 지운다(2 회차 고칠 것 1). QA 도 측정 전에 `df -h /private/tmp` 를 한 번 보는 편이 낫다.

## 바꾼 파일

- `docs/rust/data/sqlx-patterns.md` 0.1.0 → 0.2.0 — 원칙 5 뒤 원칙 6 「시각은 종류부터 나누고, 종류마다 Rust 타입과 열 타입을 정한다」(종류 셋의 정본은 backend 원칙 10 ·
  SQLx · SeaORM Entity · PostgreSQL 열 네 칸 표 · `TIMESTAMPTZ` 는 원래 시간대 이름을 남기지 않는다 · 생성기가 붙이는 `DateTimeWithTimeZone` 과 어댑터 변환 · 실측 · 킷 규칙 문장 · 출처),
  안티패턴 「벽시계를 `TIMESTAMPTZ` 순간 하나로만 저장」
- `docs/rust/research-log.md` 1.2.0 → 1.3.0 — `## [2026-09-24] — Phase 9 kaizen` 항목(채택 셋 · 봉인 전 실측 표 · 버전 현행성 · 미반영 셋)
- `rust-kit/skills/rust-preflight/SKILL.md` — Gotcha 10 (E2), Step 2 · 3 FAIL 줄에 Step 3.5 가리킴, Step 3.5 신설(임시 워크트리 세 곳 · 판정 세 줄 · `HEAD` 에 내 파일만 얹는 한 번과
  쓰는 때 · `HEAD` 임시가 실패할 때 가르는 법 · 남의 미커밋 확정 세 조건 · toolchain 기록 이유), Step 2.5 와 리포트의 `[미검증]` 네 칸, 리포트 FAIL 행 Details 머리 넷
- `rust-kit/skills/rust-run/SKILL.md` — 종료 코드를 못 얻으면 다시 실행, 그래도 못 얻으면 `[미검증]` 네 칸
- `rust-kit/skills/rust-test/SKILL.md` — After Creation 5 항을 네 칸으로, 「돌릴 수 있는데 안 돌렸으면 `[미검증]` 이 아니다」
- `rust-kit/agents/rust-reviewer.md` — §미검증 증거 프로토콜 조항 2 · 3 을 기준 원본 현행 판으로 재동기화하고 재동기화 기록 줄 · 옮기지 않은 것 줄, `UNVERIFIED_ENV` 남용 방지 4 요건 절,
  미검증 마커 줄을 네 칸으로, 최종 판정을 두 카운터 · BLOCKED 로
- `rust-kit/skills/rust-audit/SKILL.md` — Gotcha 14 네 칸 · 두 분류 · `(Step 5 참조)` (옛 「2 건 이상 CONDITIONAL · Step 4 참조」 는 Step 5 와 반대였다), Step 5 두 카운터 · BLOCKED
- `rust-kit/skills/rust-model/SKILL.md` — Gotcha 「시각 컬럼은 종류부터 정하고, ORM 마다 다른 타입 대응을 따른다」, Step 1 입력 표 행, Step 2 타임스탬프 줄, §4S Entity `DateTimeWithTimeZone` 과 어댑터 두 줄
- `rust-kit/references/project-detection.md` — Step 2c 표를 crates.io · 2026-09-24 로, `sea-orm` 2.0.3, 행 여덟 더함
- `rust-kit/skills/rust-grpc/SKILL.md` — Gotcha 5 를 본문 예시와 같은 0.14 로, Step 2c 가리킴
- `rust-kit/evals/evals.json` — 사례 17 (rust-preflight 원인 가르기)

스킬 · 에이전트 머리 설정은 그대로다(AP-04). rust-kit README 자동 구간은 스킬 · 에이전트 머리 설정만 읽는다 — `sync-docs.py --check-only` 는 「모든 README가 동기화 상태입니다」.

## 반영한 처리 배정표 키

| 키 | 반영 |
| --- | --- |
| `backend-family:P4` | rust-preflight 실패를 내 변경 · 남의 미커밋 변경 · 기준 커밋에서 이미 실패로 가른다 — Gotcha 10 · Step 3.5 · Step 5 FAIL 행 머리 넷 · 평가 사례 17 (SK-01 ~ SK-04). 남의 미커밋은 시작 목록 · 내 경로 밖 · 내가 바꾼 이름이 아님 세 조건을 채울 때만 확정하고, 못 채우면 `[미검증]` 에 「귀속 불명」 |
| `F09` 비고 (Phase 4 행) | 기준 커밋 가르기 규칙 세 곳을 하나로 — Phase 4 가 정한 harness `/sprint` Step 3 판정 세 줄을 글자 그대로 옮겼다(SK-02 가 원문과 같은지 잰다). preflight 는 커밋 전에 돌아 미커밋 변경에 내 것도 섞이므로 `HEAD` 임시에 내 파일만 얹는 한 번을 표 밖에 붙였다 |
| `backend-family:P2` (rust-model 부분) | `docs/rust/data/sqlx-patterns.md` 원칙 6 · rust-model Gotcha · 입력 표 행 · §4S 예시 (SK-05 ~ SK-07). 종류 셋의 정의는 Phase 7 의 `docs/backend/fundamentals/database.md` 원칙 10 을 가리키고 다시 쓰지 않았다(RE-02) |

그 밖에 받은 것 — 앞 Phase 넘김 셋(Phase 1 `rust-kit/agents/rust-reviewer.md:137` 접미 없는 `[미검증]` · Phase 4 판정 세 줄 · Phase 7 rust-model 타입 대응),
편집 전 감사가 찾은 둘(rust-reviewer 정본 사본이 2026-08-13 개정 전 판 · rust-audit Gotcha 14 가 Step 5 와 반대), 근거 파일 §3 현행화.

Phase 1 가이드 변경 셋 (rust-kaizen Gotcha 8):

| 가이드 변경 | 이 킷 | 자리 |
| --- | --- | --- |
| `[미검증]` 에 네 칸 (skill-design-guide §3.7 3 항 · agent-design-guide §10 정책 2 항) | 반영 | rust-preflight 두 자리 · rust-run · rust-test · rust-reviewer · rust-audit (SK-09) |
| 작업 자체를 못 한다고 결론 내리기 전 네 칸 (§3.7 5 조항 3 항) | 해당 없음 | rust-kit 어디에도 작업 전체를 못 한다고 끝내는 자리가 없다. 항목 하나를 못 재는 경우는 위 네 칸 자리가 받는다 |
| 0 이 아닌 값을 내는 새 측정 — 알려진 답 대조 (§3.7) | 해당 없음 | 이 킷 스킬은 값을 세는 측정 스크립트를 새로 만들지 않는다. 0 기대 측정은 rust-audit Gotcha 15 · rust-reviewer 0 매치 규칙이 이미 양성 대조를 요구한다 |

## 미반영 키와 사유

- `SeaORM 2.x` 타입 대응 실측 — 로컬에 2.x 크레이트가 없어 컴파일로 재지 못했다. 원칙 6 과 SK-07 은 sea-orm 1.1.19 로 잰 값이다
- rust-audit 기준의 시각 종류 판정 행(근거 파일 §4 권장 7) — 기준 문서에 DB 카테고리가 없어 자리부터 정해야 한다. 아래 넘기는 것
- 스킬 본문 · 템플릿의 버전 리터럴을 Step 2c 참조로 바꾸기(근거 파일 §4 권장 8) — tower-http 0.7 · utoipa 6 · rust-i18n 4 는 breaking change 가 있어 자동으로 바꾸지 않는다(근거 파일 §3). 값은 Step 2c 표에만 적었다

그대로 둔 곳과 이유:

- rust-reviewer · rust-audit 의 「미검증 1 건: [체크항목] — [이유]」 보고 모양 — backend-audit 와 같은 모양이라 형제 대칭을 지킨다
- rust-reviewer Evidence Validity Gate 표의 접미 없는 `[미검증]` — 기준 원본 조항 2 가 레거시 표기를 `INVALID` 로 읽는다
- rust-model `## 5. 도메인 모델 구조체 생성` 의 `DateTime<Utc>` — 도메인은 UTC 순간이 맞다. 어댑터가 `.with_timezone(&Utc)` 로 바꾼다
- 기준 원본 조항 1 의 N/A 표와 새 조항 2 — rust-reviewer 에 옮기지 않았다. backend · infra 사본과 같고, 아래 Phase 3 넘김으로 같이 푼다

ER-03 셋째 값(공유 파일 · 다른 Phase 파일을 건드린 커밋 가운데 다른 Phase 서명이 없는 커밋 수)이 0 이 아니면 QA 가 그 커밋 목록부터 보고 판정한다 —
그 값은 다른 Phase 가 서명 줄을 단다는 전제에 기댄다.

## 넘기는 것 (명시적 미완)

| 대상 | 누가 | 할 일 |
| --- | --- | --- |
| `rust-kit/skills/rust-audit/references/audit-criteria.md` | 다음 사이클 Phase 9 | 시각 종류 판정 행(벽시계를 순간 하나로만 저장 · 특정 지역 일정인데 IANA 시간대 이름이 없음, 근거 파일 §4 권장 7). `:89` 의 `utoipa 5.4 docs` 버전 리터럴도 Step 2c 참조로(근거 파일 §3 표) |
| `rust-kit/skills/rust-init/SKILL.md` | 다음 사이클 Phase 9 | 버전 리터럴(tower-http 0.6 · utoipa 5.4 · rust-i18n 3 · OTel 0.31 · mockall 0.13 · toolchain 1.88.0)을 Step 2c 참조와 major 분기로(근거 파일 §4 권장 8). `rust-middleware` · `rust-l10n` · `templates/rust-init.toml.template` 도 같은 일이다 |
| `.claude/skills/rust-kaizen/SKILL.md` | 다음 사이클 | Gotcha 6 형제 표에 「실패 원인 셋」 · 「미검증 두 카운터」 행. Gotcha 9 의 AR-02 검사(`grep -rn … .`)가 자기 파일을 잡아 늘 2 가 된다. 레포 전용 파일이라 이 Phase 범위 밖이다 |
| `harness/docs/guides/qa-evaluation-guide.md` | 다음 사이클 Phase 3 | §Canonical Unverified-Evidence Protocol 의 drift 메모에 rust-reviewer 재동기화(2026-09-25) 줄, 기준 원본 번호 3 이 둘인 것, 새 조항 2 를 킷 reviewer 에 옮길지. Phase 8 넘김과 같이 푼다 |
| `harness/skills/sprint/SKILL.md` | 다음 사이클 Phase 4 | Step 3 표 첫 줄 「내가 쓴 목록 밖이면 남의 미커밋이다」 가 근거 파일 §4 권장 2 보다 느슨하다. rust-preflight 는 표를 글자 그대로 두고 표 밖 문장으로 좁혔다 |
| `docs/rust-kit/sqlx-patterns.html` | Final F2 | 원칙 6 이 없다. rust-preflight · rust-model 페이지가 있으면 같이 다시 만든다 |
| `plugin.json` | Final | rust-kit 버전(지금 0.3.1). Gotcha 둘 · 절차 하나 · 판정 형식(두 카운터 · BLOCKED) · 평가 사례 하나가 바뀌었다 |

Final 이 더 할 것: 이 Phase 는 공유 파일(marketplace · 킷 버전 파일 · 루트 README · 루트 CLAUDE.md · `docs/` HTML · 감사 기록 · 실패 횟수 파일 · 처리 배정표 ·
`.github/workflows/ci.yml` · `.harness/stale-values.yaml`)을 건드리지 않았다. CI 에 넣을 줄은 없다 — 새 평가 사례는 CI 가 이미 돌리는 `run-evals.py` 안에 있다.

## changelog 한 단락

rust-kit 의 preflight 가 빨간 clippy · test 를 내 변경 탓으로 단정하기 전에 원인을 셋으로 가른다 — 내 변경 · 남의 미커밋 변경 · 기준 커밋에서 이미 실패.
Step 3.5 가 같은 명령을 `HEAD` · 분기점 · 기준 가지의 깨끗한 임시 워크트리에서 다시 돌리고(판정 세 줄은 harness `/sprint` Step 3 과 글자 그대로), `HEAD` 에 내가 쓴 파일만 얹어
한 번 더 돌려 내 것과 남의 것을 가른다. 남의 미커밋은 시작 때 떠 둔 목록 · 내 경로 밖 · 내가 바꾼 이름이 아님을 모두 확인할 때만 확정하고, FAIL 행 Details 가 원인으로 시작해도
Status 는 FAIL 그대로다. rust-model 은 시각 필드를 순간 · 받는 사람 지역을 따라가는 벽시계 · 특정 지역에 묶인 벽시계 가운데 무엇인지 먼저 정하고 ORM 마다 다른 타입 대응을 따른다 — 원칙은 `docs/rust/data/sqlx-patterns.md` 원칙 6,
SeaORM 예시는 생성기가 붙이는 `DateTimeWithTimeZone` 으로 바꿨다(옛 예시는 생성기가 만든 Entity 에 붙이면 컴파일되지 않았다). rust-reviewer 의 미검증 기준 원본 사본을 현행 판으로
다시 맞춰 판정이 두 카운터(`UNVERIFIED_INVALID_EVIDENCE` · `env_gaps`)와 BLOCKED 로 바뀌었고 rust-audit 가 같은 판정을 받는다. `[미검증]` 은 여섯 자리에서 네 칸(막는 것 ·
시도한 우회 · 통제 불가 사유 · 재검증 명령)을 쓴다. project-detection Step 2c 버전 표를 2026-09-24 값으로 올렸다. 평가 사례가 17 개가 됐다.

## 킷 로그 한 단락 (rust-kit)

2026-09-24 Phase 9 — rust-kaizen. 트리거 orchestrator-phase-9. 처리 배정표 두 키(위 반영 표 — P2 는 rust-model 부분만), 앞 Phase 넘김 셋, 편집 전 감사가 찾은 둘을
네 관심사로 묶었다(Gotcha 3 상한). 근거:
[git status](https://git-scm.com/docs/git-status) (누가 고쳤는지는 알려주지 않는다 — 시작 목록이 있어야 남의 미커밋을 가른다),
[git merge-base](https://git-scm.com/docs/git-merge-base) (분기점이지 기준 가지의 지금 상태가 아니다),
[git stash](https://git-scm.com/docs/git-stash) (작업 폴더를 `HEAD` 로 되돌린다 — 공유 폴더에서 쓰지 않는다),
[git worktree](https://git-scm.com/docs/git-worktree) (임시 워크트리로 다른 커밋을 따로 꺼낸다),
[Clippy CHANGELOG](https://github.com/rust-lang/rust-clippy/blob/master/CHANGELOG.md) (toolchain 이 오르면 기준 커밋도 새로 실패할 수 있다),
[SQLx PostgreSQL types](https://docs.rs/sqlx/latest/sqlx/postgres/types/index.html) · [SeaORM 1.1 column types](https://github.com/SeaQL/seaql.github.io/blob/master/SeaORM/versioned_docs/version-1.1.x/04-generate-entity/03-column-types.md) ·
[SeaORM 2 column types](https://github.com/SeaQL/seaql.github.io/blob/master/SeaORM/docs/04-generate-entity/03-column-types.md) (순간 타입이 ORM 마다 다르다),
[PostgreSQL Date/Time Types](https://www.postgresql.org/docs/current/datatype-datetime.html) · [RFC 5545 §3.3.5](https://www.rfc-editor.org/rfc/rfc5545.html#section-3.3.5) (시간대 이름을 따로 둔다),
[tower-http CHANGELOG](https://github.com/tower-rs/tower-http/blob/master/tower-http/CHANGELOG.md) · [utoipa CHANGELOG](https://github.com/juhaku/utoipa/blob/master/utoipa/CHANGELOG.md) (breaking change — 리터럴을 자동으로 바꾸지 않는다),
[crates.io sea-orm](https://crates.io/api/v1/crates/sea-orm) (Step 2c 값). 근거 파일이 밝힌 한계 — 실패 진단이 남의 미커밋 파일을 가리킨다는 사실만으로 원인을 정할 수 있다는 1 차 출처는 없다
(그래서 확정에 세 조건을 걸었다), SeaORM 2 계열은 로컬 컴파일로 재지 못했다.

## 다음 사이클 메모

- Step 2c 옛 행 `testcontainers` 의 전제 0.27 이 스킬 어디에도 없다 — 행을 지우거나 전제 칸을 실제 값으로 고친다
- rust-kit 안 특정 앱 이름이 66 곳 남아 있다(`grep -rnc 'fit-pal\|fitpal' rust-kit`). 이번 네 관심사 밖이라 건드리지 않았다 — 새 문장에는 넣지 않았다
- 평가 사례 17 은 구조만 잰다 — 실제 스킬로 돌려 답이 assertion 넷을 채우는지는 결정론 측정이 없다(계약 `오라클 한계`)
- 계약 안 측정 공통 정의가 두 판을 풀 때 실패에서 멈추고 끝나면 지우는 꼴을 Phase 7 · 8 · 9 가 따로 썼다. contract-schema 의 측정 도우미 예시로 올릴지 다음 사이클 Phase 2 가 정한다(계약 피드백 개선 제안 1)
- 계약 피드백 자기진단 `implementation_leakage` 가 true — 조건 줄에 측정 도우미 이름과 문서에 들어갈 문장이 글자 그대로 들어갔다. 산출물이 문서 문장이라 새 문장을 글자 그대로 세는 자리가 필요했다
