---
slug: after-0926-contract-schema
created: "2026-09-26 20:16"
---

## AM-01 — relaxing (동의 받음 · anchored)

- 대상 조건: AR-06 (로컬 CI 가 기준과 같은 상태로 끝난다)
- 원 조건: 요약 파일에서 `rc=0` 줄이 **22 줄**, `rc=0` 이 아닌 줄은 `feedback-agg-test SKIP (yq 없음)` 한 줄뿐
  (yq 가 있으면 `rc=0` 23 줄). 기준 실측 「B 판에서 22 · SKIP 1」
- 변경: `rc=0` 줄 **25 줄** · SKIP 1 줄 (yq 가 있으면 `rc=0` 26 줄). 측정 명령 · 측정 묶음 `ci-local.sh`
  (sha256 앞 16 자리 `59fe55125c0dbc77`, AR-05 가 잠금) · 나머지 판정은 그대로
- 근거 (실측, 2026-09-26 20:1x):
  - 봉인된 측정 묶음의 `ci-local.sh` 는 단계가 스물여섯이다 — `run` 스물다섯(`kaizen-assertions` ·
    `reviewer-copies` · `api-ui-viewer` 포함)과 yq 분기 하나. 원 조건의 「22 · SKIP 1」 은 이 셋이 없던 옛 판
    스크립트로 잰 값이다 (세션 스크래치 `cs/ci-base.txt` 에 22 단계 요약이 남아 있다)
  - 기준 판 `6378948` 사본(세션 스크래치 `cs/mock`, 분리 체크아웃)에 봉인된 `ci-local.sh` 를 돌리면 `rc=0` 25 · SKIP 1 · 종료 0
  - 구현 판 `5e1a74b`(작업 폴더 W, `HEAD` = 가지 끝, `.harness` 밖 미커밋 0)에서도 `rc=0` 25 · SKIP 1 · 종료 0 —
    기준 판과 같다. 조건 이름 「기준과 같은 상태」 는 성립한다
  - 원 조건은 봉인된 스크립트로는 통과할 수 없다 — 요약 줄이 26 줄이라 「`rc=0` 22 줄 + 그 밖 1 줄」 이 나올 수 없다.
    PASS 집합이 비어 있던 조건이라 무엇으로 고쳐도 PASS 집합이 는다
- direction: `relaxing added=2 removed=2` — `harness/references/contract-schema.md` 의 `amend_direction` (허용 집합 헬퍼)에
  원 허용 요약 모양 둘(`rc0=22 skip=feedback-agg-test` · `rc0=23 agg=rc0`)과 개정 둘(`rc0=25 …` · `rc0=26 …`)을 넣은 출력
- consent: `anchored` — 사용자가 이 개정만 콕 집어 골랐다 (세션 기록의 `AskUserQuestion` 쌍, 다중 선택).
  위임 2026-09-26T10:09:00.557Z 는 동의 근거로 쓰지 않았다
- 동의자: 사용자 (Jackson)
- 근거 (redaction 거친 원문): 질문 「위 설명대로, 측정을 고치는 개정 중 동의하는 것을 모두 고르세요. 안 고른 것은
  조건 문장을 새로 써서 다시 봉인합니다(시간이 더 듭니다).」 → 고른 답
  「cs: 성공 줄 22→25, gd: 커밋 서명 줄 읽기, vsa: sed 공백 표기, hs: .harness 빼고 세기」 — 이 개정은
  「cs: 성공 줄 22→25」 (선택지 설명 「제가 검사 셋을 더해 늘어난 수. 25 줄 모두 성공」). 앞선 질문(답변 시각
  2026-09-26T16:20:41.030Z, 같은 세션 기록 3632 번째 줄)에 사용자가 「각의미 설명」 이라 답해 네 개정의 뜻을 풀어 들은 뒤 고른 것이다
- 앵커: answer=2026-09-26T16:22:39.485Z · call=2026-09-26T16:21:15.422Z · header=측정 고침 ·
  tool_use_id=toolu_01XFvGpFRqx7oyRQGCG6Csmv · session=bda55d45-296c-491f-89ba-b52042d58e72 ·
  cwd=/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak2-pd ·
  출처=~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/bda55d45-296c-491f-89ba-b52042d58e72.jsonl 3648 번째 줄(답) · 3647 번째 줄(호출)
