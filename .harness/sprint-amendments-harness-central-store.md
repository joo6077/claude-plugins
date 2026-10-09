---
slug: harness-central-store
created: "2026-10-09 13:51"
---

# harness-central-store 개정

봉인 커밋 `a4d520f7` 뒤 계약 본문은 고치지 않았다. 아래가 구현 중 바뀐 것 전부다.

## A-01 — 계약 폴더를 뒤지는 find 에 -H, check-superseded 를 범위에 더함

- 발견: 구현 중 실측(2026-10-09) — 맥의 `find` 는 끝에 `/` 없는 바로가기 폴더를 인자로 받으면 안을 열지 않는다.
  `find <프로젝트>/.harness -maxdepth 1 -type f -name 'sprint-contract*.md'` 가 0 건, `find -H` 는 1 건. 바로가기 모양에서
  계약 폴더를 뒤지는 명령이 조용히 0 건을 내 검사가 아무것도 안 보고 통과한다.
- 고친 곳(범위 안): `harness/scripts/commit-guard.sh` · `harness/scripts/qa-pending-check.sh` · `harness/agents/qa-evaluator.md`
  계약 후보 찾기 · `harness/skills/sprint-contract/SKILL.md` 두 곳 · `harness/references/contract-schema.md` 세 곳
- 범위 목록에 더하는 경로 둘: `harness/scripts/check-superseded.sh` · `harness/evals/superseded/check-superseded-test.sh`
- 더하는 조건 — 오류-03: Given 바로가기 모양 계약 폴더에 `superseded_by` 없는 superseded 계약 하나, When
  `check-superseded.sh <그 .harness>` 를 돌리면, Then `MISSING_BY` 한 줄 · `checked=1 violations=1 unreadable=0` · 종료 1 이다
  [exact]. 측정: `bash harness/evals/superseded/check-superseded-test.sh` 의 `PASS L-바로가기`. 음성 대조: `find -H` 를
  `find` 로 되돌린 사본(`CHECK_SUPERSEDED=<사본>`)에서 `FAIL L-바로가기` (실제 출력 `checked=0 violations=0 unreadable=0`)
- amend_direction: relaxing added=2 removed=0 — 범위 목록 15 경로를 17 경로로 늘린다. 계산: 계약 `# sprint-scope` 블록과
  두 경로를 더한 목록을 contract-schema §Amendment 사이드카의 `amend_direction` 에 넣은 출력.
  조건 오류-03 을 더하는 쪽은 통과 집합을 줄이는 narrowing 이다
- consent: anchored — 사용자 발언 「ㄱㄱ」, 질문은 「`check-superseded.sh` 도 이번에 같이 고칠지 답 한 마디 (ㄱㄱ / 빼)」.
  prompt 로그 `~/.claude/logs/fit-pal/2026-10.md` · timestamp `2026-10-09T13:51:19+0900` ·
  session `c0c0aae7-8201-45fd-b1e1-338ea412ed57` · cwd `/Users/jackson/Hub/10_Dev/fit-pal`

## A-02 — 스크립트-03 음성 대조를 실제로 있던 구멍으로 잼

- amend_direction: unchanged — 조건 · 통과 기준은 그대로다.
- 조건의 음성 대조는 「계약 폴더 찾기가 심볼릭 링크를 건너뛰게(`[ -d ] && [ ! -L ]`) 바꾼 사본」이다. A-01 로 드러난 실제 원인은
  `find` 에 `-H` 가 없는 것이라, 그 사본(`find -H` → `find`)으로도 돌렸다: `FAIL SCOPE-link-out` (실제 exit 0 · stderr 비어 있음).
  두 사본 모두 같은 사례가 실패해야 판별력이 있다고 본다.

## A-03 — 봉인 대조의 산문 거르기 결함 (구현 판단, 조건 불변)

- amend_direction: unchanged — 스킬-03 `verify:link-prose` 를 그대로 재다 드러난 결함을 고쳤다.
- 옛 블록은 차이 머리 줄을 빼려고 `grep -vE '^[+-][+-]'` 로 둘째 글자를 걸러, 봉인 뒤 더한 목록 줄(`+- …`)까지 버렸다.
  `grep -vE '^(\+\+\+|---) '` 로 머리 줄만 뺀다 (`harness/agents/qa-evaluator.md` 1-e-3).
