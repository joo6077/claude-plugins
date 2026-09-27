# pd2 묶음 기록 — 승인 기록 경로 따라 읽기 · 계약도 없을 때

- 계약: `.harness/sprint-contract-after-0926-prd-none-followups.md` (조건 20 · 기능 조건 12 · 봉인 `sha256:18c60a176e1f951f` · 측정 줄 `sha256:32776cae8d09b5ea`)
- 가지: `chore/ak2-pd2`, 시작점 `0dccce0` (pd 가지 끝). 시작 때 `git status --short` 는 빈 출력 — 앞 단계가 남긴 커밋 안 한 파일은 없었다
- 사용자 합의: 위임으로 받음 — 세션 `bda55d45-296c-491f-89ba-b52042d58e72`, 2026-09-26T10:09:00.557Z 와 결정 답 2026-09-26T10:30:16.222Z, 추가 위임 2026-09-27T01:22:01.089Z
- QA 판정: 아직 없음. 계약 `status` 는 `active` 그대로다

## 항목별 결과

| 항목 | 결과 | 커밋 |
| --- | --- | --- |
| PD2-1 design-mockup Step 2 가 폐기 칸의 경로를 따라 원문 읽기 | 고침. Step 2 에 「승인 기록 폐기 칸이 경로를 가리킴 →」 규칙 한 줄을 더했다. PRD 경로면 비범위 표 항목을, 작업 계약 경로면 `범위 경계` 의 줄 끝 표시가 붙은 줄을 폐기 항목으로 쓴다. 파일이 없거나 못 읽으면 `못 읽음: <경로>` 를 말하고 시안을 만들기 전에 묻는다. Step 6 의 옛 「다음 시안 전에 그 경로에서 …」 문장은 Step 2 를 가리키는 말로 바꿨다 — 같은 절차 원문이 두 곳에 있지 않다 | `2ff7359` (design-kit) |
| PD2-2 PRD 도 계약도 없으면 승인 기록 폐기 칸에 네 칸 | 고침. design-mockup Step 6 · sprint-contract 포맷 규칙 · `/sprint` Step 0.5 문단 세 곳이 모두 PRD → 계약 → 승인 기록 폐기 칸 순서로 적는다. 줄 모양은 결정 하나에 폐기 칸 아래 들여쓴 한 줄이라 승인 기록 확인 명령 `→ 2` 가 그대로 맞는다. 계약을 나중에 쓰면 승인 기록의 결정을 옮겨 적지 않고 그 경로만 적는다 | `2ff7359` · `501c578` (harness) · `fc17a35` (planning-kit) |

봉인 커밋은 `b311681` (계약 한 파일). 바깥 근거가 있어야 판단되는 항목은 없었다.

## 부모 지시 세 곳 밖에 더 고친 두 파일

- `design-kit/references/visual-change-protocol.md` §4 — 옛 두 줄이 「그 결정이 적힌 파일 경로를 폐기 칸에 적는다」 라 PD2-2 와 어긋났다. design-mockup Step 2 · Step 6 이 이 절을 근거로 든다. 같은 규칙이 적힌 자리를 다 고치지 않으면 한쪽이 남으므로, 옛 두 줄은 두고 계약도 없을 때의 예외 한 줄만 더했다
- `planning-kit/skills/plan-prd/SKILL.md` Step 0 — 읽는 쪽 짝이다. 두 검색은 이미 `.design` 도 보지만 설명 글이 「계약 `범위 경계` 에 적어 둔」 이라 승인 기록 줄을 이 기능의 결정으로 안 볼 수 있었다. 첫 문장 괄호 한 곳만 바꾸고 두 검색 · 옮기기 절차는 글자 그대로 뒀다

## 교차 진단 반영 (봉인 전)

- 순서 판정 `ordok` 이 「승인 기록 폐기 칸」 문구의 둘째 글자부터 다음 낱말을 찾아 설계보다 느슨했다 → 문구가 끝난 뒤부터 찾게 고쳤다. 나쁜 순서 한 줄은 `n=1 ok=0`, 바른 순서 한 줄은 `n=1 ok=1`
- GAP 표 design-mockup Step 2 줄 번호가 실제와 어긋났다 → `:66-67` 승인 기록 · `:68` PRD 비범위 표 · `:69-70` 앱 코드로 바로잡았다
- AR-01 경로 목록에 `--no-renames` 를 붙였다
- 고친 측정 도우미로 good · bad · bad2 사본을 다시 재서 봉인 전 표와 같은 값을 얻었다

## 킷별 버전 판단

| 킷 | 지금 | 제안 | 이유 |
| --- | --- | --- | --- |
| design-kit | 0.6.0 | patch | design-mockup Step 2 에 규칙 한 줄, Step 6 문장 하나 바꿈, 규약 §4 에 예외 한 줄. 새 스킬 · 새 절 없음 |
| harness | 0.15.2 | patch | sprint-contract 한 줄 · `/sprint` Step 0.5 산문 한 줄. 명령 · 보고 틀은 그대로 |
| planning-kit | 0.7.0 | patch | plan-prd Step 0 설명 괄호 한 곳. 새 산출물 없음 |

## 문서 사이트 드리프트

- `python3 scripts/detect-docs-drift.py --since 0dccce0` 출력: `design-kit/references/visual-change-protocol.md → docs/design-kit/visual-change-protocol.html`. 그 페이지 `:688` 의 「그 결정이 적힌 파일 경로를 폐기 칸에」 항목 뒤에 계약도 없을 때의 예외가 빠진다
- `docs/design-kit/design-mockup.html:635` 는 pd 때부터 옛 글이고 이번에 원본 Step 2 · Step 6 이 또 바뀌었다. 이 도구는 스킬 파일을 문서 페이지에 잇지 않아 이 페이지를 못 잡는다
- 두 페이지 모두 문서 사이트 묶음 DC-15 로 넘긴다 — 이 묶음은 페이지를 다시 만들지 않는다

## 검사 결과

- 조건 20 개 자기 측정(구현 커밋 `fc17a35` 기준): AR-02 를 뺀 19 개가 기대값과 같다. AR-02 는 이 파일 커밋 뒤, DG-05 는 그 뒤 로컬 CI 로 다시 잰다
- `python3 scripts/validate-plugin.py` design-kit · harness · planning-kit 각각 종료 코드 0 · FAIL 0
- `python3 scripts/sync-docs.py --check-only` 종료 코드 0 (모든 README 동기화 상태), `python3 scripts/sync-evals.py --check-only` 종료 코드 0 · 0 added · 0 orphans · 0 missing
- 로컬 CI (`fc17a35`, 도구 지문 `59fe55125c0dbc77`): `rc=0` 25 줄, 나머지 한 줄은 `feedback-agg-test SKIP (yq 없음)`

## 측정 도구

- 측정 도우미: 계약 `## 회귀 게이트 — 측정 도우미` 블록. 떼어 낸 판은 스크래치 `pd2/measure.sh`
- 사본 만들기 · 전부 재기 · 개선안 넣기: 스크래치 `pd2/build.sh` · `pd2/runall.sh` · `pd2/mock.py`, 봉인 `pd2/seal.sh`, 저장 검사 `pd2/gate65.sh` · `pd2/cov.sh`
- 스크래치 경로: `/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/bda55d45-296c-491f-89ba-b52042d58e72/scratchpad/pd2/`

## tone-guide 5 단계 대조

1 단계 근거: 오버레이 `.claude/tone-project.md` (어댑터 없음 · 주석 언어 ko) 를 읽고 `tone-kit/references/` 의 core-comment · core-antipatterns · locale-korean 전문과 core-naming · core-structure 규칙표를 읽었다. 어댑터가 없어 스택 고유 검사는 꺼져 있다. 대상은 더한 여섯 줄(구현 커밋 세 개의 `+` 줄)이다.

| 패턴 / 규칙 | 건수 | 판정 |
| --- | --- | --- |
| K-02 · §8 G-1 번역투 여섯 갈래 | 0 | 통과 |
| K-04 · §8 G-2 `합니다`체 | 0 | 통과 (관측 컨벤션) |
| K-05 음역 | 0 | 통과 — 영어 원문은 `Step` · 파일 이름뿐 |
| K-11 새 이름 | 0 | 통과 — 「네 칸」 은 같은 문단 앞에서 plan-prd 비범위 표의 네 칸으로 이미 정의된 말이다 |
| K-03 능동 · 직설 | 0 | 통과 — 주체가 「Step 2」 · 「결정 원문」 으로 드러난다 |
| C-01 · C-02 what 반복 | 0 | 통과 — 새 줄은 규칙 문장이지 코드 해설이 아니다 |
| C-13 자화자찬 | 0 | 통과 |
| C-15 문체 | 0 | 통과 (관측 컨벤션) |
| S-03 · S-14 인라인 · 이동 정리 | 0 | 통과 — Step 6 의 절차 문장을 Step 2 로 옮기면서 Step 6 에는 가리키는 말만 남겼다 |
| 안티패턴 A~G · H 보존 | 0 | 통과 — 지운 줄은 Step 6 옛 문장 하나뿐이고 그 내용은 Step 2 로 옮겼다. 보존 대상을 지우지 않았다 |
| 요청 범위 밖 파일 | 0 | 통과 — 바뀐 파일은 계약 `ALLOWED` 안 |

## 남은 것

- 문서 사이트 두 페이지(`docs/design-kit/design-mockup.html` · `docs/design-kit/visual-change-protocol.html`) 다시 만들기 — DC-15 묶음 몫
- QA 판정(qa-evaluator) — 부모 단계 몫. DG-05 는 추적 안 된 도구 `ci-local.sh` 에 기대므로 지문이 바뀌면 다시 잴 수 없다
- 세 킷 버전 올리기 — 릴리스 단계 몫
