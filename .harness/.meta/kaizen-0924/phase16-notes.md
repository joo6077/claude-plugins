# 카이젠 2026-09-24 Phase 16 (api-kit) — notes

- 계약: `.harness/sprint-contract-kaizen-0924-p16-api-kit.md` (조건 29 · 기능 조건 19, 봉인 `sha256:3178ee00afdb7c67` · `locked_at` 2026-09-25 13:24)
- 개정: `.harness/sprint-amendments-kaizen-0924-p16-api-kit.md` (조건 변경 0 건, `end_sha` 만)
- 검토: `.harness/.meta/kaizen-0924/phase16-review.md` — 1 회차 `VERDICT: CHANGES`(꼭 고칠 것 넷 C1 ~ C4 · 고치면 좋은 것 일곱)는 DRAFT 가 C1 ~ C4 와 좋은 것 1(일부) · 2 ~ 6 을 반영했다.
  2 회차도 `VERDICT: CHANGES` — 꼭 고칠 것 D1(`docs/api/execution/auth-secret-lifecycle.md` 세 자리가 `--secret` 이 가리는 곳을 아직 「둘뿐」 으로 적음) 하나였다.
  BUILD 가 봉인 전에 D1 과 2 회차 좋은 것 1 · 2 를 반영하고, 반영 · 미반영 사유를 계약 `## 범위 경계` 승인 대체 줄에 적은 뒤 예행 저장소 다섯을 새로 만들어 전 조건을 다시 쟀다
- 사용자 승인 대체: 사용자 위임(세션 기록 queued_command `2026-09-24T04:04:16.964Z`) · Codex 한도 소진(2026-09-24) · 「코덱스 대신에 그냥 너가 알아서 진행하라고」(user `2026-09-24T11:54:58.940Z`) — REVIEW 에이전트 검토로 대신했다
- 시작 커밋 `3a348d601cedd49e0689ca194b57baf8f5029454`
- 계약 피드백: `~/.harness/feedback/contract/5a24cc99-2026-09-25T132847-de8c7935-25567.yaml` (`verify-feedback.sh` PASS). 초안은 스크래치 `p16b/feedback-draft.yaml` 에 쓰고
  `HARNESS_CONTRACT_ROOT` · `HARNESS_CONTRACT` 를 명시해 저장했다 — 작업 폴더의 `.harness/feedback-draft.yaml` 은 다른 Phase 와 겹칠 수 있어 쓰지 않았다

## 커밋

| 커밋 | 내용 | 파일 |
| --- | --- | --- |
| `5784b10` | 봉인 커밋 | 계약 1 개 |
| `be4abdd` | 경로 간 불변식 양쪽 값 · 판정 불가, 뷰어 브라우저 확인, Hurl 기재 현행화 | `api-kit/` 열 개 · `docs/api/` 일곱 개 |
| `b1dab00` | 개정 파일에 `end_sha` (`be4abdd`) | 개정 1 개 |
| 이 파일의 커밋 | notes · 검토 기록 | `.harness/` 두 개 |
| 그다음 커밋 | 개정 파일에 notes 커밋 sha 로 `end_sha` 한 줄 더 | 개정 1 개 |

모든 커밋 메시지 끝 문단에 `Kaizen-Phase: kaizen-0924-p16-api-kit` 줄이 있다. 구현 커밋은 `git add -- <열일곱> && git commit -o … -- <열일곱>` 한 번으로 내 경로만 실었다
(`api-kit/` 과 `docs/api/` 는 이 Phase 한 킷 몫이라 한 커밋이고, `validate-post-kaizen.py` scope-isolation 이 PASS 다).
**FIX 가 커밋을 더할 때도 서명 줄을 넣고, 개정 파일에 `end_sha:` 줄을 덧붙인다.**

구현은 초안의 예행 도구(스크래치 `p16d/mock.py`, 지문 앞 16 자리 `99aca4f2cab1bc42` — 계약에 적힌 값)를 작업 폴더에 그대로 돌렸다(`MOCK_OK` · 종료 코드 0).
돌리기 전에 `api-kit/` · `docs/api/` · 근거 파일이 시작 커밋과 `HEAD` 사이에 바뀌지 않았고 미커밋 변경도 없는 것을 봤다(커밋 0 · 변경 0). 커밋 전 열일곱 파일이
예행 저장소 `p16d/rh-base` 의 같은 경로와 바이트 단위로 같았다(`same=17`).

29 조건 측정은 봉인 판 계약(`5784b10`)에서 뗀 묶음으로 돌렸다 — 스크래치 `p16b/k/`(`common.sh` · `m.sh` · `rule-delta.sh` · `srv.py` · `probe.js`, DRAFT 판 `p16d/k/` 와
글자 그대로 같다) · `p16b/runall.sh`(`K` 와 `TMPDIR` 를 스크래치로 두고 `R` 을 비운 채 공통 정의를 `.` 로 읽은 뒤 `m <조건 ID>`). QA 가 같은 묶음을 다시 돌릴 수 있다.
구현 커밋 `be4abdd` 를 상한으로 둔 첫 측정(`p16b/out-impl.txt`)에서 notes 에 기대는 둘(ER-01 둘째 줄 `NOTES_MISSING` · ER-03)을 빼고 스물두 ID 가 조건 줄의 값과 같았다.

커밋 뒤 저장소 검사: `validate-plugin.py api-kit` 종료 코드 0(V1 ~ V10 OK, V2 는 templates 없음 SKIP) · `validate-plugin.py`(전체) 0 · `Total: 14 plugins, 14 OK` ·
`sync-docs.py --check-only` 0(`api-kit/README.md: 동기화됨`) · `sync-evals.py --check-only` 0 · `run-evals.py` 0(115 passed) ·
`validate-post-kaizen.py --since 3a348d6` 0(scope-isolation · doc-contracts PASS, docs-site-regen SKIP — Final F2 몫). api-kit 에는 킷 시험 폴더가 없다.

## GAP 분석 — Phase 1 결과 대조

오케스트레이터 Step 16 전수 감사(`skill-design-guide.md` 1.6.0) 기준이다. 계약 `## GAP 분석` 절 표와 같다.

| Phase 1 변경 | api-kit 에서 본 자리 | 처리 |
| --- | --- | --- |
| §3.7 조항 3 — 검증 불가 시 네 칸(막는 것 · 시도한 우회 · 통제 불가 사유 · 재검증 명령) | 새로 넣은 브라우저 확인이 도구 없이 끝날 수 있다 | SK-05 — `/api-ui` §7 · §8 에 네 칸 |
| 0 이 기대값인 검증의 양성 대조 | `/api-ui` §7 은 이미 positive control 을 요구한다 | 새 식에 대조 사본 넷과 CSP `<meta>` 사본(SK-06) |
| 알려진 답 대조 | 새로 짠 측정(브라우저 식 · hurl 재실측) | SK-02 · SK-06 · SK-08 · SK-09 에 손으로 센 기대값 |
| agent 가이드 §10 — `[미검증:ENV]` · `[미검증:INVALID]` | api-reviewer 의 미검증 프로토콜이 정본 요약 복제다 | 처리 배정표 밖 — 미반영(아래), 다음 사이클 |

하지 않기로 한 셋과 이유:

- `판정 불가` 를 게이트에 넣지 않는다 — 사라진 경로가 `required` 면 schema drift(필드 삭제)가 이미 계약 실패로 잡고, `optional` 이면 계약상 없어도 되는 값이라
  불변식을 판정할 수 없는 게 맞다. I-JSON 게이트 실패를 「비교 불가」 로 따로 두는 기존 규칙과 같은 모양이다. 근거 파일 §5 열린 질문 1 — 사용자 확인 권장(아래 메모)
- 경로 간 불변식을 `.hurl` 로 옮기지 않는다 — 확정 결정 유지. 경로가 없을 때 종료 코드 3 이 킷 분류로 환경 실패라 계약 판정이 보류된다(근거 파일 L1)
- OpenAPI 3.2 · Hurl 8 jsonpath 1 개 결과 벗기기 · 대비 · 테마 · Pact 브랜치 축 · Hurl 8.1.0 — 아래 미반영 절과 연구 기록 이월 절

## 사전 · 사후 측정 (api-kaizen Step 1 · 5)

`.claude/skills/api-kaizen/SKILL.md` Step 1 명령을 시작 커밋 `3a348d6` 판과 `end_sha` 판(`be4abdd`)에서 그대로 돌린 출력이다(`git show <커밋>:<파일>` 로 두 판을 읽었다).

| 스킬 | 시작 커밋 gotchas · steps | 끝 판 gotchas · steps |
| --- | --- | --- |
| api-init | 10 · 9 | 10 · 9 |
| api-probe | 12 · 9 | 12 · 9 |
| api-contract | 10 · 12 | 10 · 12 |
| api-verify | 10 · 12 | 12 · 12 |
| api-ui | 20 · 9 | 20 · 9 |

api-verify 의 +2 는 새 Gotcha 가 아니라 §6 에 더한 굵은 불릿 둘이다 — Step 1 명령(`grep -c '^- \*\*'`)이 파일 전체의 굵은 불릿을 센다.
Step 5 의 음성 대조는 계약의 문장 삭제 대조(`del.sh`, 토큰 129 개 모두 값이 떨어짐)와 양성 · 음성 대조(`ctl.sh`)다 — 계약 `봉인 전 실측` 표의 「대조」 칸.

## 바꾼 파일

- `api-kit/skills/api-verify/SKILL.md` — §6 판정 줄 형식 · `판정 불가` 불릿 둘, §9 · §11 집계, `--secret` Gotcha, §5 I-JSON 목록 `-0`
- `api-kit/skills/api-verify/references/failure-taxonomy.md` — §5 경로 간 불변식 행, §8 JUnit `판정 불가` 행
- `api-kit/skills/api-contract/SKILL.md` — Gotcha(표현 가능 여부 정정 · `-0`), §2 I-JSON 목록, §11 보고 4 번 새 pin 변이 확인
- `api-kit/skills/api-contract/references/strictness-modes.md` — `### Hurl 표현 가능 여부` 행과 문장
- `api-kit/skills/api-ui/SKILL.md` — §7 브라우저 확인(여는 방법 · 콘솔 오류 · 식 · 기대값 두 행 · 누르는 자리 24), §8 보고 한 줄, `--secret` Gotcha
- `api-kit/skills/api-ui/references/viewer-spec.md` — §1 누르는 자리 행, §3.2 `data-ep` · 그룹 펼침
- `api-kit/skills/api-probe/SKILL.md` — `--secret` Gotcha, §7 I-JSON 검문 `-0`
- `api-kit/skills/api-probe/references/hurl-execution.md` — `HURL_VARIABLE_` Gotcha, §6 표 `--curl <file>` 행
- `api-kit/README.md` — `--secret` 한 줄(AUTO 구간 밖)
- `api-kit/agents/api-reviewer.md` — 평가 표 3 행(판정식 쪽 경로까지)
- `docs/api/research-log.md` 0.2.0 → 0.3.0 — `## [2026-09-24] — 첫 카이젠 (Phase 16)` 절, 2026-09-05 절 정정 표시
- `docs/api/execution/auth-secret-lifecycle.md` 0.2.0 → 0.2.1 — `HURL_VARIABLE_` Gotcha, `--curl <file>` 세 자리(§6 문장 · 수치 표 · Gotcha 머리)
- `docs/api/execution/probe-synthesis-hurl-semantics.md` 0.2.0 → 0.2.1 — §6 문장 · 출처 줄 · 수치 표 행
- `docs/api/contract/snapshot-sealing-canonicalization.md` 0.1.0 → 0.1.1 — §3 I-JSON 게이트 `-0` · 정정 7920 문장 · 출처
- `docs/api/contract/contract-extraction-modes.md` 0.1.0 → 0.1.1 — 새 pin 변이 확인 Gotcha
- `docs/api/verification/static-evidence-viewer-contract.md` 0.1.0 → 0.1.1 — 누르는 자리 수치 행 · 브라우저 확인 Gotcha
- `docs/api/verification/regression-diff-failure-policy.md` 0.1.0 → 0.1.1 — 판정 불가 Gotcha

## 반영한 처리 배정표 키

| 키 | 반영 |
| --- | --- |
| `other-kits:P7` | `/api-verify` §6 경로 간 불변식 판정 줄에 양쪽 실제 값, 한쪽 경로가 없으면 `판정 불가` 를 따로 센다(게이트 미파괴, 사라진 `required` 경로는 schema drift 가 잡는다). §9 · §11 집계 칸, 실패 분류 §5 · §8, 회귀 정책 문서 Gotcha. 「Hurl 로 표현 불가」 기재 네 곳을 실측대로 고쳤다(적을 수는 있지만 경로가 없으면 종료 코드 3). 새 pin 변이 확인을 `/api-contract` §11 보고와 추출 모드 문서에, 검토 에이전트 3 행에 양쪽 경로 (SK-01 ~ SK-04) |
| `other-kits:P8` | `/api-ui` §7 에 브라우저 확인 — 여는 방법(`ui.html` 한 장만 든 빈 폴더를 `127.0.0.1` 웹 서버로 띄우거나 로컬 파일 허용 — `.api/` 를 통째로 띄우지 않는다, 끝나면 서버를 내리고 폴더를 지운다), 콘솔 error 0(`favicon.ico` 404 제외), 페이지 안 식으로 `ep` = `shown` · `under24` 0. §8 보고에 숫자 인용, 도구가 없으면 `[미검증]` 네 칸. 누르는 자리 기준을 WCAG 2.2 2.5.8 24 CSS px 로(44 는 권장), 뷰어 스펙에 `data-ep` · 그룹 펼침 (SK-05 ~ SK-07) |

적용 힌트 「경로 간 조건에 양쪽 값을 적고, 화면 확인 숫자를 보고에 인용한다」 는 SK-01 판정 줄 형식과 SK-05 (h) §8 보고 줄이다.
근거 파일 §3 현행화도 했다 — `HURL_VARIABLE_` 네 곳, `--secret` 이 가리는 곳 네 곳(`--curl` 파일 포함)과 hurl-execution §6 표 `--curl` 행 · auth-secret-lifecycle 세 자리(§6 문장 · 수치 표 · Gotcha 머리),
I-JSON 게이트 `-0` 다섯 곳, 연구 기록 새 절 (SK-08 ~ SK-11). 오케스트레이터 Phase 16 줄의 확정 결정 여섯은 글자 그대로 두었다(AR-03 `1 1 1 1 | 1 1 1 1`).

## 미반영 키와 사유

처리 배정표 키는 둘 다 반영했다. 근거 파일 권장안 가운데 아래는 넣지 않았다.

- OpenAPI 3.2 대응 — 근거 파일이 「선택」 으로 적었고 `query` 를 안전 메서드로 볼 근거를 가져오지 않았다(§5)
- Hurl 8 jsonpath 1 개 결과 벗기기 Gotcha — 킷 파일에 `[*]` 가 0 건이다. `/api-contract` §9 예시와 Gotcha 의 어긋남을 고치려면 바꿀 표현을 hurl 로 먼저 재야 한다
- 뷰어 대비 · 테마 실측 — 근거 파일이 재지 않았다
- Pact pending 브랜치 축 — 확정 결정 밖이라 사용자 결정이 먼저다
- Hurl 8.1.0(미출시) 보안 수정 · 새 옵션 — 출시일 미정
- api-reviewer 미검증 프로토콜 복제 문구가 정본과 다르다 — 처리 배정표 밖, 다음 사이클
- 1 회차 검토 좋은 것 1 의 나머지(뷰어 계약 문서 Gotcha 끝 CSP 문장 · 연구 기록 표 CSP 행) — 조건 밖 글이라 넣지 않았고, SK-06 CSP 사본 줄과 아래 메모 둘로 대신했다

## 넘기는 것

| 파일 | 남은 것 | 맡을 곳 |
| --- | --- | --- |
| `docs/superpowers/specs/2026-09-02-api-kit-design.md` | `:249` 「경로 간 불변식은 Hurl assert 로 표현되지 않는다」 — `docs/api/` 밖이라 이 Phase 범위가 아니다. 결론(후처리)은 맞고 이유만 「경로가 없으면 종료 코드 3 이라 판정 불가를 가를 곳이 후처리뿐」 으로 | Final |
| `.claude/skills/kaizen-orchestrator/SKILL.md` | `:567` Phase 16 줄의 같은 말 | Final |
| `docs/api-kit/probe-synthesis-hurl-semantics.html` · `docs/api-kit/auth-secret-lifecycle.html` · `docs/api-kit/snapshot-sealing-canonicalization.html` · `docs/api-kit/contract-extraction-modes.html` · `docs/api-kit/regression-diff-failure-policy.html` · `docs/api-kit/static-evidence-viewer-contract.html` | 이 Phase 가 바꾼 소스 여섯에서 만든 페이지 | Final F2 |
| `scripts/detect-docs-drift.py` | `SOURCE_TO_HTML` 에 `docs/api` 소스 매핑이 없어 위 여섯 페이지가 드리프트 목록에 안 나온다 | Final |
| `api-kit/.claude-plugin/plugin.json` | 버전 (이 Phase 는 버전을 적지 않았다 — AP-01) | Final |

`.github/workflows/ci.yml` 에 더할 시험은 없다 — api-kit 에 킷 시험 폴더가 없고, 이 Phase 측정은 계약 안 도구다.

## changelog 한 단락

api-kit — `/api-verify` 가 경로 간 불변식 판정 줄마다 양쪽 실제 값을 적고, 한쪽 경로가 없으면 `판정 불가` 로 따로 센다(게이트는 깨지 않고, 사라진 필수 경로는 필드 삭제가 잡는다).
`/api-contract` 는 새로 만든 pin 을 스냅샷 사본에서 한 번 망가뜨려 FAIL 이 나는지 보고한다. `/api-ui` 는 생성한 뷰어를 `ui.html` 한 장만 든 폴더에서 브라우저로 열어
콘솔 오류 · 항목 수 · 누르는 자리 크기를 재고 그 숫자를 보고에 인용한다 — 누르는 자리 통과선은 24 CSS px(44 권장)다.
`HURL_VARIABLE_` 접두 · `--secret` 이 가린다고 확인된 곳(`--curl` 파일 포함) · I-JSON `-0` 기재를 실측에 맞췄다.

## 킷 로그 한 단락

2026-09-24 Phase 16 — 첫 카이젠. 로컬 hurl 8.0.1 과 헤드리스 크로미엄으로 다시 잰 값을 `docs/api/research-log.md` 2026-09-24 절에 남겼다.
경로 간 조건은 capture 로 `.hurl` 에 적을 수 있지만 경로가 없으면 종료 코드 3 이다. 환경변수 변수 접두는 Hurl 8.0.0 부터 `HURL_VARIABLE_` 이다
([Hurl CHANGELOG](https://github.com/Orange-OpenSource/hurl/blob/master/CHANGELOG.md)). `-0` 은 JCS 가 `0` 으로 적어 파서가 오류를 내야 한다
([RFC 8785 정정 목록](https://www.rfc-editor.org/errata/rfc8785)). 누르는 자리 기준은 [WCAG 2.2](https://www.w3.org/TR/WCAG22/) 2.5.8 이고,
새 pin 변이 확인은 [PIT](https://pitest.org/) 의 변이 시험 뜻을 따른다.

## 다음 사이클 메모

- 킷이 정본으로 부르는 확정 시안 `.mockups/api-ui-v7.html` 은 `.gitignore` 에 있어 워크트리 · CI 에 없다 — 이번 브라우저 대조는 본 레포 파일을 읽었다
- `판정 불가` 를 게이트에 넣을지는 이번에 넣지 않는 쪽으로 정했다 — 사용자 확인 권장
- 확정 시안에 뷰어 스펙 §1 의 CSP `<meta>` 가 없다 — 이번 브라우저 대조는 그 `<meta>` 를 넣은 사본을 따로 돌렸다
- `/api-ui` §7 글자 검사가 CSP `<meta>` 가 있는지를 재지 않는다
- §7 식은 크기가 0 보다 크면 보이는 것으로 친다 — 화면 읽기 프로그램용으로 1×1 px 로 숨긴 입력칸이 생기면 `under24` 가 1 이 되어 멀쩡한 뷰어가 떨어진다. 확정 시안에는 없다
- `/api-contract` §9 예시 `jsonpath "$.data[0].id" isString` 이 같은 파일 Gotcha 의 index assertion 금지와 어긋난다 — 바꿀 표현을 hurl 로 먼저 재고 고친다
- QA 참고: ER-01 `evid_same` 은 누가 근거 파일을 고쳐도 떨어진다. 떨어지면 `git log 3a348d6..<end_sha> -- .harness/.meta/evidence/phase16.md` 로 누가 고쳤는지부터 본다
- 옛 기재를 고칠 때 킷 Gotcha 가 출처로 대는 문서까지 한 번에 찾는다 — 이번에 2 회차 검토가 auth-secret-lifecycle 세 자리를 잡았다. 옛 글 검사는 글자 목록에 뜻으로 거는 검사(`curl_missing`)를 곁들였다
- `save-feedback.sh` 가 이 워크트리에서 `project_name: 'kaizen-0924'`(워크트리 이름)를 적었다 — Phase 4 · Phase 12 몫과 같은 문제
