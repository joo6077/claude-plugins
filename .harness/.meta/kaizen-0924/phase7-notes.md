# 카이젠 2026-09-24 Phase 7 (backend-kit) — notes

- 계약: `.harness/sprint-contract-kaizen-0924-p07-backend-kit.md` (조건 26 · 기능 조건 16, 봉인 `sha256:80b4853008bd8dfe` · `locked_at` 2026-09-25 06:04)
- 개정: `.harness/sprint-amendments-kaizen-0924-p07-backend-kit.md` (조건 변경 0 건, `end_sha` 만)
- 검토: `.harness/.meta/kaizen-0924/phase7-review.md` (1 회차 CHANGES 고칠 것 둘 · 권장 여섯은 초안이 반영, 2 회차 APPROVE 조건 줄 밖 결함 하나는 BUILD 가 봉인 전에 반영)
- 시작 커밋 `79258900de00e621412e4c436b44028a77d7fb64`
- 계약 피드백: `~/.harness/feedback/contract/5a24cc99-2026-09-25T060812-de8c7935-70385.yaml` (`verify-feedback.sh` PASS). 초안은 `.harness/feedback-draft-p07.yaml` 로 갈라 썼다

## 커밋

| 커밋 | 내용 | 파일 |
| --- | --- | --- |
| `8dc2bfc` | 봉인 커밋 | 계약 1 개 |
| `86a196b` | 원칙 10 · OpenAPI 3.2.1 · research-log | `docs/backend/` 셋 |
| `7971ef7` | 시각 종류 Gotcha · 감사 기준 · CDC 행 · 미검증 네 칸 · OAuth draft-16 · 평가 사례 8 · README | `backend-kit/` 여덟 |
| `6a49ea5` | 개정 파일에 `end_sha` (`7971ef7`) | 개정 1 개 |
| 이 파일의 커밋 | notes · 검토 기록 | `.harness/` 두 개 |
| 그다음 커밋 | 개정 파일에 notes 커밋 sha 로 `end_sha` 한 줄 더 | 개정 1 개 |

모든 커밋 메시지 끝 문단에 `Kaizen-Phase: kaizen-0924-p07-backend-kit` 줄이 있다. 구현 커밋은 `git add -- <파일…> && git commit -o -- <파일…>` 로 내 경로만 실었다.
**FIX 가 커밋을 더할 때도 서명 줄을 넣고, 개정 파일에 `end_sha:` 줄을 덧붙인다.**

구현은 초안의 모의 편집(스크래치 `p7d/mock.py`, 치환 40)을 작업 폴더에 그대로 돌렸다 — `mock applied 40`, 더한 줄 132.
26 조건 측정은 봉인 커밋 판 계약에서 뗀 묶음으로 돌렸다 — 스크래치 `p7b/k/`(`common.sh` · `m.sh` · `new-warnings.sh`. `m.sh` · `new-warnings.sh` 는 초안의 `p7d/k/` 와 같고
`common.sh` 는 2 회차 검토가 고친 `mktemp` 한 줄만 다르다) · `p7b-run.sh`(공통 정의를 `.` 로 읽고 `TMPDIR` 를 스크래치로 둔 뒤 조건 문구 그대로의 측정). QA 가 같은 묶음을 다시 돌릴 수 있다.

## 바꾼 파일

- `docs/backend/fundamentals/database.md` 0.2.0 → 0.3.0 — 다루는 범위에 「시각 종류별 저장」, 원칙 9 뒤 원칙 10(세 종류 표 · IANA 시간대 식별자 · `TIMESTAMPTZ` 가 원래 시간대를
  남기지 않음 · floating time · 서머타임 해석 · 시간대와 나라 상수 금지와 그것이 이 킷의 규칙이라는 문장), 안티패턴 두 행
- `docs/backend/fundamentals/api-design.md` 0.1.0 → 0.1.1 — OpenAPI 3.2.0 세 자리를 3.2.1 로(원칙 5 문장 · 출처 · 수치 기준 행)
- `docs/backend/research-log.md` 1.3.0 → 1.4.0 — `## [2026-09-24] — Phase 7 kaizen` 항목
- `backend-kit/skills/backend-system/SKILL.md` — Gotcha 18 (E2) 신설, Gotcha 13 (c) · Step 2 `| API 규격 |` 행이 Gotcha 18 을 가리킨다, OAuth draft-16
- `backend-kit/skills/backend-guide/SKILL.md` — Gotcha 19 (E1) 신설, Step 1 `| database |` 키워드 다섯, OAuth draft-16
- `backend-kit/skills/backend-audit/references/audit-criteria.md` — §3 `시각 종류별 저장` · `시간대·나라 상수 금지` 두 행, §2 Timestamp 행을 순간 필드로,
  §8 CDC 행을 at-least-once 로, `[미검증]` 두 자리를 네 칸으로
- `backend-kit/skills/backend-audit/SKILL.md` — Gotcha 11 본문과 예시 · Gotcha 12 · DB 엔진 문단을 네 칸으로, Gotcha 16 을 옛 서술 대신 기준으로, Step 3 8 · 17 행
- `backend-kit/agents/backend-reviewer.md` — 출력 포맷의 미검증 규칙 줄과 예시 4 행을 네 칸으로, 예시 2 행 draft-16
- `backend-kit/skills/backend-test/SKILL.md` — Gotcha 13 · Step 5 증거 규칙의 `[미검증]` 을 네 칸으로
- `backend-kit/evals/evals.json` — 사례 8 (반복 시각 저장 · 기본 시간대 상수, backend-guide), 사례 4 draft-16
- `backend-kit/README.md` — 검증 절 「평가 사례 8 개의 구조 검증」 · 「등록된 검사 전부 (개수는 `harness/docs/guides/plugin-validation-guide.md` 가 정한다)」

스킬 · 에이전트 frontmatter 는 그대로다(AP-04). backend-kit README 에 AUTO 구간이 없다 — `sync-docs.py --check-only` 는 「동기화됨」.

## 반영한 처리 배정표 키

| 키 | 반영 |
| --- | --- |
| `backend-family:P2` | 시각을 순간 / 받는 사람 지역을 따라가는 벽시계 / 특정 지역에 묶인 벽시계 셋으로 나누고, 시간대 · 나라는 코드 상수로 박지 않고 어디서 받는지를 계약에 적게 했다. 원칙 본문은 database.md 원칙 10 한 곳(RE-02), 스킬 둘은 그곳을 가리키는 Gotcha, 감사 기준은 판정 두 행, 평가 사례 하나 (SK-01 ~ SK-05 · AR-02) |
| `F20` (시간대 쪽만) | 처리 배정표 비고 「시간대를 설정값으로 다루는 것은 backend-family:P2(Phase 7)」 — 위 행과 같다 |

처리 배정표 제안 원문은 순간 대 벽시계 둘이었지만 셋으로 나눴다. 근거 파일 §2 결론이 「특정 지역에 묶인 벽시계는 시간대 식별자를 함께 둬야 한다」 고 적었다.
그 밖에 받은 것 — 근거 파일 §3 현행화(OAuth 2.1 draft-16 · OpenAPI 3.2.1), research-log 2026-08-13 미반영 항목(감사 기준 CDC 행),
오케스트레이터 Step 7 전수 감사가 찾은 Phase 1 가이드 변경의 반대편(`[미검증]` 네 칸), 편집 전 감사가 찾은 README 구조 검사 개수 줄.

Phase 1 가이드 변경 셋 (backend-kaizen Gotcha 8):

| 가이드 변경 | 이 킷 | 자리 |
| --- | --- | --- |
| `[미검증]` 에 네 칸 (skill-design-guide §3.7 3 항 · agent-design-guide §10 정책 2 항) | 반영 | backend-test Gotcha 13 · Step 5, backend-audit Gotcha 11 · 12 · DB 엔진 문단, audit-criteria §2 · §3, backend-reviewer 출력 포맷 (SK-09) |
| 작업 자체를 못 한다고 결론 내리기 전 네 칸 (§3.7 5 조항 3 항) | 해당 없음 | 스킬 넷 어디에도 작업 전체를 못 한다고 끝내는 자리가 없다. 항목 하나를 못 재는 경우는 위 네 칸 자리가 받는다 |
| 0 이 아닌 값을 내는 새 측정 — 알려진 답 대조 (§3.7) | 해당 없음 | 이 킷 스킬은 값을 세는 측정을 새로 만들지 않는다. backend-test 가 만드는 시험은 통과 · 실패로 판정한다 |

## 미반영 키와 사유

- `F20` 의 폐기 결정 기록 자리 — 처리 배정표가 Phase 11 에 배정했다. 이 킷은 시간대 쪽만 맡는다
- 벽시계 값을 API 로 보낼 때의 문자열 형태 — 근거 파일에 없다
- 시간대를 사용자 설정에서 물려받을지 일정 레코드에 따로 남길지 — 근거 파일 §5 열린 질문이다. 새 문장은 둘 중 하나를 고르지 않고 「어디서 받는지와 저장 여부를 계약에 적는다」 로 두었다
- AsyncAPI 3.1.0 — 킷 파일에 「최신판」 으로 적힌 AsyncAPI 버전이 없고, 인용하는 수신자 규범은 3.0.0 에도 있다. research-log 에 기록만 했다

## 넘기는 것 (명시적 미완)

| 대상 | 누가 | 할 일 |
| --- | --- | --- |
| `rust-model` | Phase 9 | 타입 대응을 ORM 별로 나눈다 — 근거 파일 §2: SQLx 는 `DateTime<Utc>` + `TIMESTAMPTZ`, SeaORM Entity 는 `DateTimeWithTimeZone`. `rust-kit/skills/rust-model/SKILL.md:90` 입력 표 「타임스탬프 타입」 에 시각 종류 구분을 붙인다. 원칙 본문은 이 Phase 의 database.md 원칙 10 이다 |
| `docs/backend-kit/database.html` · `docs/backend-kit/api-design.html` | Final F2 | 원칙 10 이 없고 OpenAPI 3.2.0 이 남아 있다. 두 페이지를 다시 만든다 |
| `.harness/stale-values.yaml` | Final | 지금 OpenAPI 항목은 `old: "3.1.1"` · `new: "3.2.0"` 이다. `old: "3.2.0"` · `new: "3.2.1"` 항목을 더해 3.2.0 이 다시 들어오면 잡히게 한다. `docs/backend/research-log.md` 는 이력이라 3.2.0 이 남는다 — allow 에 넣는다 |
| `plugin.json` | Final | backend-kit 버전(지금 0.3.1). 새 Gotcha 둘과 감사 기준 두 행이 더해졌다 |
| `infra-kit/README.md` | Phase 8 | 검증 절의 같은 「7 카테고리 구조 감사」 줄(`:54`) — `scripts/validate-plugin.py` 의 검사는 V1 ~ V10 열 가지다. 레포 전체에 이 줄은 backend-kit 과 infra-kit 둘뿐이었다 |
| `.claude/skills/backend-kaizen/SKILL.md` | 다음 사이클 | Gotcha 6 형제 대칭 표에 「시각 종류」 항목(backend-system Gotcha 18 · backend-guide Gotcha 19 · audit-criteria §3 두 행)을 더한다. 레포 전용 파일이라 이 Phase 범위 밖이다 |
| `OpenAPI 3.1` | 열린 질문 | backend-system Step 2 · backend-audit Step 3 · audit-criteria §2 의 3.1 표기 — 최소 지원선인지 최신판 뜻인지 툴체인 호환 확인이 먼저다(근거 파일 §5). 그대로 두었다 |
| `F20` | Phase 11 | 폐기 결정 기록 자리를 하나로 정한다 |

그대로 둔 곳: `backend-kit/skills/backend-audit/SKILL.md:114` 의 「미검증 1 건: [체크항목] — [이유]」 — backend-reviewer 복제 조항 5 의 보고 모양과 같아 그대로 둔다(backend-kaizen Gotcha 8 — 복제 조항은 문구를 바꾸지 않는다).
README `:59` 2026-04-24 이력의 draft-15 와 research-log 의 옛 항목도 이력이라 그대로다(SK-06 예외).

ER-03 셋째 값(공유 파일 · 다른 Phase 파일을 건드린 커밋 가운데 다른 Phase 서명이 없는 커밋 수)이 0 이 아니면 QA 가 그 커밋 목록부터 보고 판정한다 —
그 값은 다른 Phase 가 서명 줄을 단다는 전제에 기댄다(지금까지 서명 없는 커밋은 오케스트레이터의 근거 파일 커밋뿐이다).

Final 이 더 할 것: 이 Phase 는 공유 파일(marketplace · plugin.json · 루트 README · 루트 CLAUDE.md · `docs/` HTML · 감사 로그 · 실패 횟수 파일 · 처리 배정표 ·
`.github/workflows/ci.yml` · `.harness/stale-values.yaml`)을 건드리지 않았다. CI 에 넣을 줄은 없다 — 새 평가 사례는 CI 가 이미 돌리는 `run-evals.py` 안에 있다.

## changelog 한 단락

backend-kit 이 시각 필드를 순간 · 받는 사람 지역을 따라가는 벽시계 · 특정 지역에 묶인 벽시계 셋으로 나눈다. 원칙은 `docs/backend/fundamentals/database.md` 원칙 10 에 두고,
backend-system 은 규격 산출물에 시각 필드마다 종류 · 저장 형태 · 시간대 출처 · 순간으로 바꾸는 규칙 네 칸을 요구하며(Gotcha 18), backend-guide 는 「UTC 로 통일하라」
전에 종류부터 나누게 한다(Gotcha 19). 감사 기준은 벽시계 뜻의 필드를 순간 하나로만 저장하거나 특정 지역 벽시계에 IANA 시간대 식별자 칸이 없으면 FAIL, 시간대 · 나라를
코드 상수 하나로 강제하면 FAIL 이다 — 한 지역 전용 서비스라고 밝히면 N/A. 시간대 출처 규칙은 RFC 요구가 아니라 이 킷의 규칙이라고 문서에 적었다. 감사 기준 CDC 행이
Outbox+CDC 로 exactly-once 를 보장한다던 서술을 at-least-once 와 consumer idempotency 요구로 바로잡았다. `[미검증]` 표기는 설계 가이드와 같은 네 칸(막는 것 · 시도한
우회 · 통제 불가 사유 · 재검증 명령)으로 맞췄다. OAuth 2.1 인용은 draft-16, OpenAPI 는 3.2.1 로 올렸다. 평가 사례가 8 개가 됐다.

## 킷 로그 한 단락 (backend-kit)

2026-09-24 Phase 7 — backend-kaizen. 트리거 orchestrator-phase-7. 처리 배정표 `backend-family:P2` 하나와 근거 파일 §3 현행화, research-log 2026-08-13 미반영 한 줄,
Phase 1 가이드 변경의 이 킷 쪽 반대편을 세 관심사로 묶었다(Gotcha 4 상한). 근거:
[RFC 5545 §3.3.5](https://www.rfc-editor.org/rfc/rfc5545.html#section-3.3.5) (DATE-TIME 세 형태 · floating 은 합리적일 때만 · 서머타임 해석 — 원칙 10 · Gotcha 18 · 19 · 감사 기준 두 행),
[PostgreSQL Date/Time Types](https://www.postgresql.org/docs/current/datatype-datetime.html) (`TIMESTAMPTZ` 는 원래 시간대를 남기지 않는다),
[OAuth 2.1 Internet-Draft](https://datatracker.ietf.org/doc/draft-ietf-oauth-v2-1/) (draft-16, 2027-03-07 만료),
[OpenAPI 최신판](https://spec.openapis.org/oas/latest.html) · [OpenAPI 3.2.1 release](https://github.com/OAI/OpenAPI-Specification/releases/tag/3.2.1) (2026-09-10 공개),
[microservices.io Transactional Outbox](https://microservices.io/patterns/data/transactional-outbox.html) (relay 중복 발행 · consumer idempotency — CDC 행),
[AsyncAPI 3.1.0 release](https://github.com/asyncapi/spec/releases/tag/v3.1.0) (기록만).
근거 파일이 밝힌 한계 — RFC 5545 는 나라 코드 · 시간대를 어디서 받을지 · 저장 여부 · 코드 상수 금지를 정하지 않는다(그래서 그 부분은 킷 규칙이라고 적었다),
「알람」 은 뜻이 모호하다, 시간대를 사용자 설정에서 물려받을지 레코드에 남길지는 제품 요구가 정한다.

## 다음 사이클 메모

- harness 과제 — 봉인 digest 는 조건 첫 줄만 덮어, 둘째 줄(Given/When/Then)의 요구값과 계약 안 `m.sh` 가 봉인 뒤 바뀌어도 `SEAL_OK` 다(검토 `phase7-review.md` 참고). 다음 사이클 Phase 2 가 둘째 줄까지 덮을지 본다
- 계약 안 측정 도우미가 `mktemp -d` 로 두 판을 풀면 이 맥에서 `TMPDIR` 를 무시하고 시스템 임시 폴더에 쌓인다(2 회차 검토 실측 — 한 번에 40 ~ 70 MB). 틀 있는 `mktemp -d "${TMPDIR:-/tmp}/x.XXXXXX"` 를 contract-schema 도우미 예시에 권할 만하다
- 봉인 판 계약에서 도우미 코드 블록을 떼는 일을 이번에도 스크래치 스크립트(`p7d/extract.py`)로 했다 — Phase 3 · 4 와 같다
- 계약 피드백 자기진단 `implementation_leakage` 가 true — 조건 줄에 측정 도우미 이름과 `TIMESTAMPTZ` 가 들어갔다. 산출물이 문서 문장이라 새 문장을 글자 그대로 세는 자리가 필요했다
- 평가 사례 8 은 구조만 잰다 — 실제 스킬로 돌려 답이 assertion 넷을 채우는지는 결정론 측정이 없다(계약 `오라클 한계`)
