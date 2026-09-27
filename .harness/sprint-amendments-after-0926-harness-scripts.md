# sprint-amendments — after-0926-harness-scripts

계약 `.harness/sprint-contract-after-0926-harness-scripts.md` 의 개정 기록. 계약 본문은 봉인 뒤 고치지 않는다.

## AM-01 — relaxing (사용자 동의 · anchored)

- 대상 조건: AP-02
- 변경: 측정 `git -C "$W" diff -U0 "$B..$END" | grep '^+' | grep -v '^+++' | grep -cE 'git push.*--force'` 에
  경로 한정 `-- . ':(exclude).harness'` 를 붙인다. 계약 · 개정 · 피드백 파일(`.harness/` 아래)이 더한 줄은 재지 않는다
- 이유: 끝 판에서 잰 값이 3 이고, 세 줄 모두 이 계약 자신의 글이다 — 봉인 전 실측 표의 `git push.*--force` 행, AP-02 조건 줄,
  AP-02 측정 줄. 구현이 더한 줄(`.harness/` 밖)은 0 줄이다. 봉인 전에는 가지에 커밋이 없어(`END` = `B`) 계약이 구간에 들지 않아 드러나지 않았다
  - 실측(2026-09-26, `END` = `32d61cd`): 원 측정 3 · 경로 한정 측정 0
  - 다시 잰 값(2026-09-26, `END` = `3d3eeda`): 원 측정 6 · 경로 한정 측정 0. 늘어난 3 줄은 이 개정 파일이 사유를 적으며 패턴을 인용한 줄이다.
    계약 본문의 3 줄은 봉인돼 고칠 수 없으니, 경로 한정 없이는 어떤 수정으로도 0 이 되지 않는다
  - 세 줄: `+| \`git push.*--force\` 파일 전체 | …` · `+- [ ] AP-02: force push 금지 — …` · `+      측정: \`git -C "$W" diff -U0 …\``
- 방향: 측정 대상을 줄이는 개정이라 계산상 완화다(`amend_direction_oracle` — 원 측정 집합 ⊋ 개정 측정 집합)
- 근거 (redaction 거친 원문): 질문 「위 설명대로, 측정을 고치는 개정 중 동의하는 것을 모두 고르세요. 안 고른 것은 조건 문장을 새로 써서 다시 봉인합니다(시간이 더 듭니다).」
  (머리 `측정 고침`, 여럿 선택) 에 고른 답 「cs: 성공 줄 22→25, gd: 커밋 서명 줄 읽기, vsa: sed 공백 표기, hs: .harness 빼고 세기」.
  이 개정에 해당하는 선택지는 「hs: .harness 빼고 세기」(설명 「계약서가 인용한 설명 줄이 걸림. 기록 폴더는 빼고 센다」)다.
  그 앞 같은 머리 질문(답 2026-09-26T16:20:41.030Z, 기록 3632 번째 줄, tool_use_id=toolu_013ZdiSQjynT6irbVY9pvPYY)에 사용자가 「각의미 설명」 이라 답해 네 개정의 뜻과 잃는 것을 풀어 설명한 뒤 다시 물었다
- 동의자: 사용자(Jackson) — 세션 기록의 `AskUserQuestion` 선택 답. 위임(2026-09-26T10:09:00.557Z · 결정 답 2026-09-26T10:30:16.222Z)이 아니라 이 개정을 콕 집은 동의다
- 앵커: 2026-09-26T16:22:39.485Z · session=bda55d45-296c-491f-89ba-b52042d58e72 · cwd=/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak2-pd
  - 출처: `~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/bda55d45-296c-491f-89ba-b52042d58e72.jsonl` 3648 번째 줄, tool_use_id=toolu_01XFvGpFRqx7oyRQGCG6Csmv
    (물어본 시각 2026-09-26T16:21:15.422Z · 답한 시각 2026-09-26T16:22:39.485Z — 동의 시각은 답한 시각). cwd 는 기록에 찍힌 값 그대로다(부모 세션이 그때 ak2-pd 폴더에 있었다)
- 동의 뒤 상태: AP-02 는 위 경로 한정 측정으로 잰다
