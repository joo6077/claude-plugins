---
slug: after-0924-api-ui-unjudgeable
created: "2026-09-26 15:26"
---

## A-01 — DG-02 의 `api-kit/README.md` 한 줄: sync-docs 가 쓴 표 구분 줄의 MD060 은 세지 않는다

**앵커**: DG-02 의 측정 절 — "`m MD` 의 줄이 `SKILL.md` · `viewer-spec.md` · `api-layout.md` 를 포함해 모두 `rules_up=0`".
그리고 AR-01 · DG-05 — `api-kit/README.md` 는 AUTO:evals 블록 안만 바뀌고(`readme_outside_auto=0`), CI 단계 전부가 통과한다(`Sync docs check` 포함).

**무엇이 부딪혔나**: `api-kit/evals/` 를 만들면 `scripts/sync-docs.py` 가 README 의 AUTO:evals 블록에 표를 쓴다(`scripts/sync-docs.py:251-256` `render_evals_table`).
그 표의 구분 줄은 `|------|------|` 꼴이라 markdownlint 0.23.2 의 MD060 을 한 줄에 4 번 낸다. 블록 글자를 바꾸면 `sync-docs.py --check-only` 가 종료 코드 1 을 내 CI 가 떨어지고(DG-05),
블록 밖에 markdownlint 끄는 주석을 두면 `readme_outside_auto` 가 2 가 된다(AR-01). 표 모양을 정하는 `scripts/` 는 이 스프린트 범위 밖이다.
그래서 세 조건을 한꺼번에 채울 방법이 없다 — 실측 U 판 `6ab405a` 에서 `m MD` 가 `api-kit/README.md rules_up=1 MD060:20->24`.

**어떻게 읽나**: DG-02 의 `api-kit/README.md` 줄은 아래 둘이 함께 성립하면 `rules_up=0` 과 같게 본다. 나머지 md 파일은 원문 그대로 `rules_up=0` 이다.

1. 늘어난 규칙이 MD060 하나이고, 블록 밖 MD060 수가 시작 판과 같다 (`MD060_out=20`)
2. 블록 안 내용이 `python3 scripts/sync-docs.py api-kit` 가 쓴 그대로다 — `python3 scripts/sync-docs.py --check-only` 가 종료 코드 0 (DG-05 의 `sync-docs rc=0`)

측정: `bash .harness/.meta/after-0924-api-ui-unjudgeable/readme-md060.sh <U>` (`<U>` 는 `m HEAD` 가 낸 값. sha256 앞 16 자리 `24c5720f6f3abb2c`).
블록 안 · 밖을 나눠 규칙별 경고 수를 센다. 실측(bash · zsh 같은 출력):

```text
f81568d  block=140-141 MD060_out=20 MD022_out=4 MD032_out=4
6ab405a  block=140-146 MD060_out=20 MD060_in=4 MD022_out=4 MD032_out=4
```

양성 대조: 가지를 건드리지 않고 만든 매달린 커밋 `e6b9b27` (블록 밖에 같은 꼴의 표 하나) 에서 `MD060_out=22` — 블록 밖에 늘면 잡힌다.

**amend_direction_oracle**: `relaxing measured_removed=5 measured_added=0` — 원 오라클은 README 146 줄을 모두 재고, 개정 오라클은 AUTO:evals 블록 안쪽 5 줄을 뺀 141 줄을 잰다
(입력: U 판 README 줄 번호 집합, `harness/references/contract-schema.md` §Amendment 사이드카의 `amend_direction_oracle` 를 bash · zsh 로 돌렸다).
빠지는 5 줄은 사람이 쓴 글이 아니라 생성기가 쓴 표이고, 그 내용은 DG-05 의 `Sync docs check` 가 따로 잰다.

**consent**: 사용자 발언 인용 — 2026-09-26T01:04:21.505Z 「다음 세션에서 직접할 일을 다 실행하고 이어질것도 실행해」,
세션 `de8c7935-a5b6-4df5-9106-fafa73c288a0`, cwd `/Users/jackson/Hub/10_Dev/claude-plugins`
(세션 기록 `/Users/jackson/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/de8c7935-a5b6-4df5-9106-fafa73c288a0.jsonl`).
이 개정을 콕 집어 묻고 받은 동의가 아니라 이어질 일을 묻지 말고 끝까지 하라는 일반 위임이다. `anchored` 로 인정할지는 평가자가 정한다.
