# after-0926-docs-new-pages 개정

계약 `sprint-contract-after-0926-docs-new-pages.md` (봉인 `sha256:d6913d6663e9d866`, 봉인 커밋 `e495e2f`)
의 조건 줄은 고치지 않았다. 바뀐 것은 여기에만 적는다.

## A-01 — AR-06 허용 파일에 `scripts/check-stale-values.py` 를 더한다 (동의 대기)

**앵커**: AR-06 — 도우미 `ALLOWED` 셋(`.claude/skills/docs-site/SKILL.md` · `docs/index.html` ·
`scripts/detect-docs-drift.py`)과 새 쪽 일곱이 바뀐 파일 목록과 정확히 같아야 한다.

**무엇이 달라지나**: 허용 파일에 `scripts/check-stale-values.py` 하나를 더한다. 그 파일에서 바꿀 것은
`SOURCE_DIRS` 목록에 `".claude/skills/kaizen-orchestrator/references",` 한 줄을 넣는 것뿐이다.

**왜** — 이 묶음이 드리프트 도구와 매핑 표에 `phase-research-templates.md` 를 이었는데, 옛 값 검사는 그 폴더를
훑지 않는다. 계약을 쓸 때 허용 파일 밖이라 넘기기로 적었지만(`## 범위 경계` 표), 이 제한은 계약 작성자가
스스로 정한 것이고 사용자는 넘기는 까닭을 물었다(「다음카이젠에왜넘기는데?」).

**고쳐도 안전한지 잰 값**: 가지 끝 판 사본에 위 한 줄을 넣어 `python3 scripts/check-stale-values.py` 를 돌렸다.
고치기 전 `소스 디렉토리 26/26 · 파일 403 개 · 등록값 18 개` / `되살아난 옛 값 없음` / `rc=0`,
고친 뒤 `27/27 · 406 개 · 18 개` / `되살아난 옛 값 없음` / `rc=0`.

**다른 묶음과 부딪힘**: vsa 가지(`157e8a2`, VS-27)가 같은 `SOURCE_DIRS` 목록의 바로 아래에 세 줄을 더했다.
이 개정을 적용하면 합칠 때 그 자리가 한 번 더 부딪힌다. 두 쪽 줄을 모두 남기면 풀린다.
개정 대신 부모가 vsa · dcb 를 합치는 통합 가지에서 이 한 줄을 넣는 길도 있다 — 그 경우 이 계약은 그대로다.

**amend_direction**: `relaxing added=1 removed=0` — 스키마 `contract-schema.md` 의 허용 집합 헬퍼
`amend_direction` 을 원 허용 집합(도우미 `ALLOWED` 셋 + 새 쪽 일곱 = 10 경로)과 개정 집합(11 경로)에 돌려
계산했다. 허용 파일이 늘어나므로 완화다.

**consent**: 비어 있음 — 완화 개정이라 위임(2026-09-26T10:09:00.557Z · 결정 답 2026-09-26T10:30:16.222Z,
세션 `bda55d45-296c-491f-89ba-b52042d58e72`)으로 동의 처리하지 않는다. 사용자에게 이 개정만 따로 물어 답을 받으면
아래 칸을 채운다.

| 항목 | 값 |
| --- | --- |
| 질문 머리 | |
| 질문 시각 | |
| 답 시각 | |
| 세션 | |
| 작업폴더 | |
| 고른 답 | |

동의가 오면 할 일: `SOURCE_DIRS` 한 줄 커밋 → 도우미 `ALLOWED` 에 그 경로를 더해 `m AR-06` 재측정 →
notes 「남은 것」 첫 항목을 처리됨으로 고침 → qa-evaluator 재평가.
