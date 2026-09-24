---
slug: insights-0924-hooks-skill-collector
kind: amendments
---

# Sprint Amendments — insights-0924-hooks-skill-collector

## A-01 — DG-02 는 옛 판 같은 줄에 같은 규칙 경고가 있던 줄을 새 경고로 세지 않는다

**계기.** DG-02 를 계약 측정대로 재니(markdownlint-cli2 0.23.2, MD013 끔, 더한 줄 번호 기준) 2 건이 나왔다.

- `flutter-toolkit/skills/flutter-ui-verify/SKILL.md:13` MD041 — 새 파일에 H1 이 없었다. **고쳤다**(`# Flutter UI Verify`). 이 건은 개정 대상이 아니다. QA 1 회차가 그 수정이 본문 23 행의 `# UI Verify` 와 겹쳐 MD025 를 새로 만든 것을 짚었고, 23 행을 `## 하는 일` 로 낮췄다.
- `CLAUDE.md:142` MD036 — AR-04 가 스킬 개수를 18 → 19 로 바꾸라고 요구한 줄이다. 390dea8 판 같은 줄에도 같은 MD036 경고가 이미 있다(실측: `git show 390dea8:CLAUDE.md` 를 같은 설정으로 재면 `CLAUDE.md:142 error MD036`). 그리고 AR-04 의 측정 코드 `skill_count_lines` 가 이 줄을 굵은 글씨 형식(`^\*\*flutter-toolkit — Flutter 개발 워크플로우 \((\d+)종\)\*\*`)으로 찾으므로, 형식을 바꿔 경고를 없애면 AR-04 가 깨진다. 두 조건이 이 한 줄에서 부딪힌다.

**개정.** DG-02 의 "더한 줄에 걸린 새 경고" 에서, 390dea8 판의 대응 줄에 **같은 규칙 번호**의 경고가 이미 있던 줄은 뺀다. 이번 스프린트에서 해당하는 줄은 `CLAUDE.md:142` 1 줄이다.

- amend_direction_oracle: relaxing (측정 집합에서 1 줄을 뺀다 — PASS 집합이 늘어난다)
- consent: anchored — 사용자 위임 발언 「자동으로 끝까지 알아서 진행해 내 허락이 필요한건 코덱스로 리서치나 검토받고」(세션 `de8c7935-a5b6-4df5-9106-fafa73c288a0` 기록 queued_command `2026-09-24T04:04:16.964Z`, cwd `/Users/jackson/Hub/10_Dev/claude-plugins`) 에 따라 Codex 검토로 승인을 받는다. 검토 기록: 세션 scratchpad `insights/codex-amend-a01.md` (VERDICT: APPROVE, 파일 기록 시각 2026-09-24T14:57:31+0900 — 이 개정을 담은 커밋보다 앞선다)
- 원 오라클로 재면 2 건(고친 뒤 1 건), 개정 오라클로 재면 0 건

## A-02 — end_sha

구현 마지막 커밋이다. AR-01 은 아래 값을 상한으로 쓴다.

## A-03 — 구현 커밋을 킷 경계로 다시 나눴다 (조건 문구 변경 없음)

QA 1 회차 DG-03 FAIL: `validate-post-kaizen.py` 의 scope-isolation 검사가, 한 커밋이 `harness/skills/` 와 다른 킷의 `skills/` 를 함께 건드린 것을 위반으로 잡았다. 원격에 올리기 전이라 봉인 커밋 `36cfbbd` 위의 구현 커밋을 harness 쪽(harness · scripts · .claude · .github 16 파일)과 flutter-toolkit 쪽(flutter-toolkit · README.md · CLAUDE.md 18 파일) 두 커밋으로 다시 만들었다. 합계 34 파일로 화이트리스트와 같고 파일 내용은 위 H1 수정 외에 바뀌지 않았다. 1 회차 리포트가 가리키는 `cb5d0a1` · `0a32b96` 은 이 가지에서 사라졌다.

- amend_direction: unchanged (조건 문구와 PASS 집합을 바꾸지 않는다)

end_sha: 2a447bc71d73dd3e27535551a9ff13bb6f1b3572
