---
slug: after-0926-guides
created: "2026-09-26 20:25"
---

# after-0926-guides 개정

계약 본문은 봉인돼 있다(`conditions_digest: sha256:1774b0d356321753` · `measurement_digest: sha256:1292a5ca807199ca`, 봉인 커밋 `97d893b`).
조건 줄도 측정 줄도 고치지 않았다. 아래 개정은 「이 조건을 이렇게 읽어라」 를 덧붙일 뿐이다.
방향은 `harness/references/contract-schema.md` §Amendment 사이드카의 규칙(원 오라클과 개정 오라클로 각각 판정해 FAIL→PASS 면 `relaxing`)으로 정했다.

## AM-01 — relaxing · anchored

- 대상 조건: SK-19 의 측정 줄(`m SK-19` 의 `example_in_log`)
- 무엇이 틀렸나: 봉인된 측정은 `git log --format='%(trailers:key=Kaizen-Phase,valueonly)%x09%s'` 를 쓴다. 서명 줄 값 뒤에 줄바꿈이 붙어
  나와서 한 커밋이 두 줄(`kaizen-0924-p04-harness` 한 줄, 탭으로 시작하는 제목 한 줄)로 갈린다. `awk -F'\t' '$1 ~ /^kaizen-0924-p0[1-4]/'` 는
  서명 줄 값만 남은 첫 줄만 고르고, `cut -f2` 는 탭이 없는 줄을 통째로 내보내 제목이 아니라 `kaizen-0924-p0N-…` 만 남는다. 그래서
  어떤 예시를 적어도 `<예시>:` 가 그 줄에 없어 `example_in_log` 는 늘 0 이다 — 통과할 수 있는 구현이 없다(봉인 전 실측 값 `example_in_log=0` 도
  예시가 `kaizen` 이라서가 아니라 이 결함 때문에 나온 0 이다)
- 확인한 출력(2026-09-26, git 2.53.0, 이 워크트리):

```text
$ git log origin/main --no-merges --format='%(trailers:key=Kaizen-Phase,valueonly)%x09%s' | awk -F'\t' '$1 ~ /^kaizen-0924-p0[1-4]/' | cut -f2 | head -3 | cat -e
kaizen-0924-p04-harness$
kaizen-0924-p04-harness$
kaizen-0924-p04-harness$
```

- 바꿔 읽는 법: 서명 줄 값에 `separator=%x2C` 를 붙여 한 커밋이 한 줄로 나오게 한 아래 명령의 수를 `example_in_log` 로 읽는다.
  `ex` 는 봉인된 측정과 같은 방법으로 뽑는다(추적 규칙 표 커밋 메시지 행 셋째 칸의 첫 백틱 글에서 `:` 앞). 조건 문구
  「그 행의 예시가 `Kaizen-Phase: kaizen-0924-p01` ~ `p04` 서명이 붙은 main 커밋 제목 머리에 1 번 이상 나온다」 는 그대로다

```bash
git -C "$W" log origin/main --no-merges --format='%(trailers:key=Kaizen-Phase,valueonly,separator=%x2C)%x09%s' \
  | awk -F'\t' '$1 ~ /^kaizen-0924-p0[1-4]/' | cut -f2 | grep -cF -- "$ex:"
```

- 개정 측정의 대조(2026-09-26): 고른 줄 수 23(GAP 분석의 서명 커밋 23 개와 같다) · 끝 판 예시 `docs(harness)` → 4 · 시작 판 예시
  `kaizen` → 0(양성 · 음성 둘 다 나온다)
- direction: 같은 끝 판(`1ad0754`)에서 원 측정 `example_in_log=0`(FAIL) → 개정 측정 4(PASS). FAIL→PASS 라 `relaxing` 이다
  (`amend_direction_oracle` 은 입력이 경로 집합이라 이 개정에 맞지 않아 쓰지 않았다)
- consent: anchored — 동의자: 사용자(Jackson). 위임이 아니라 이 개정을 콕 집어 고른 선택지 답이다
  - 앵커(세션 기록의 `AskUserQuestion` 쌍, `tool_use_id=toolu_01XFvGpFRqx7oyRQGCG6Csmv`): 2026-09-26T16:22:39.485Z(답변 시각) · session=bda55d45-296c-491f-89ba-b52042d58e72 · cwd=/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak2-pd · 기록 파일 `~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/bda55d45-296c-491f-89ba-b52042d58e72.jsonl` 3648 번째 줄 (호출 시각 2026-09-26T16:21:15.422Z)
  - 질문 원문: 「위 설명대로, 측정을 고치는 개정 중 동의하는 것을 모두 고르세요. 안 고른 것은 조건 문장을 새로 써서 다시 봉인합니다(시간이 더 듭니다).」
  - 고른 답 원문(여럿 선택): 「cs: 성공 줄 22→25, gd: 커밋 서명 줄 읽기, vsa: sed 공백 표기, hs: .harness 빼고 세기」 — 이 개정은 「gd: 커밋 서명 줄 읽기」(선택지 설명 「커밋이 두 줄로 쪼개지던 읽기 버그를 고침」)
  - 앞선 질문: 같은 기록 3632 번째 줄(답변 2026-09-26T16:20:41.030Z, `tool_use_id=toolu_013ZdiSQjynT6irbVY9pvPYY`)에 사용자가 「각의미 설명」 이라 답해, 네 개정의 뜻과 잃는 것을 풀어 설명한 뒤 다시 물었다
  - 순서: 동의(16:22:39Z)는 이 동의 칸을 채운 커밋보다 앞선다. 개정 본문을 처음 담은 커밋 `0e12747`(2026-09-26T11:26:52Z)은 동의 전이며 그때 동의 칸은 비어 있었다
