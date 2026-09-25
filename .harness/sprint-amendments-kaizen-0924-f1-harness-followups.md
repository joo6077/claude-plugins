---
slug: kaizen-0924-f1-harness-followups
created: "2026-09-25 17:01"
---

# kaizen-0924-f1-harness-followups 개정

이 파일은 범위 상한 `end_sha` 를 적는 자리다. 봉인 뒤 조건 줄은 바꾸지 않았다 — 개정 0 건. 봉인 뒤 계약의 산문도 고치지 않았다.

봉인 전에 BUILD 가 고친 곳: 검토 2 회차(`.harness/.meta/kaizen-0924/f1-harness-followups-review.md` `## 2 회차`, `VERDICT: CHANGES`)의
고칠 것 둘과 권고 하나 — C11 ER-07 예외 첫 문장, C12 AR-05 (d) 를 끝 판(`$T/E`)으로, R8 개선안 ER-08 끝 문장 — 와 `## 범위 경계` 의 승인 대체 줄.
모두 봉인 커밋에 들어 있다.

구현이 개선안과 다른 곳 — 셋 다 `amend_direction: unchanged` (조건 줄의 측정 대상이 아니거나 같은 값을 낸다).

- `scripts/validate-plugin.py`: V 줄 끝에 판정을 붙이는 규칙은 판정 뒤 괄호 한 덩이를 허용한다(`— SKIP (no templates/)`).
  이 글자를 바꾸면 봉인된 Phase 11 · 13 · 14 · 16 · 17 계약의 DG-05 측정 꼴(`— OK` · `— SKIP (no templates/)`)과 어긋나서다.
  V1 · V2 실패 요약은 `… — 2 FAIL` 이던 것을 `…, 2 failed` 로 바꿨다 — 그대로 두면 끝에 `— FAIL` 이 한 번 더 붙는다.
  ER-08 측정은 harness 킷 V 줄과 V3 · V5 · V6 · V9 실패 줄만 재어 이 두 변경과 겹치지 않는다
- `.claude/skills/backend-kaizen/SKILL.md` 형제 표의 `미검증 3항` 도 `` `[미검증]` 네 칸 `` 으로 고쳤다 — infra-kaizen 과 같은 결함이고
  backend-reviewer 도 네 칸을 쓴다. SK-04 로 이미 고치는 파일이라 파일 수는 그대로다
- 평가자 로그 폴더 블록은 공통 git 폴더가 `.git` 으로 끝나면 그 부모를 본 레포로 본다. reflect-kit `project_root` 는 git 폴더와 공통 폴더가 다를 때만
  부모를 쓰는데, 본 레포에서는 그 부모가 곧 `--show-toplevel` 이라 결과가 같다(ER-03 여덟 번 실측)

측정 전제 한 건 — `amend_direction: unchanged` (통과 집합이 같다). DG-05 (b) 의 `python3 scripts/validate-doc-contracts.py` 는 `git ls-files` 를 부르므로
`git archive` 로 푼 `$T/E` 에서는 끝 판 · 시작 판 둘 다 `NOT RUN … not a git repository` · 종료 코드 2 다 — 이 계약 변경과 무관한 환경 실패다.
BUILD 는 `$T/E` 를 복사해 `git init` · `git add -A` · 커밋한 사본(`drift.sh` 가 쓰는 방식)에서 돌려 끝 판 `d97944c` · 시작 판 `5b4fd72` 둘 다
`doc-contracts: 1 블록 검사 · violation 0 · not-verifiable 0` · 종료 코드 0 을 받았다. 봉인 전 실측 값 0 은 작업 폴더(git 저장소)에서 잰 값이었다.
나머지 다섯 명령은 조건 글자 그대로 `$T/E` 에서 종료 코드 0 이다.

측정 공통 정의가 아래 `end_sha:` 줄의 마지막 값을 `END` 로 읽는다. 커밋을 더하면 새 값으로 한 줄을 **덧붙인다**
(옛 줄은 지우지 않는다). 그 커밋 메시지에도 서명 줄 `Kaizen-Phase: kaizen-0924-f1-harness-followups` 를 넣는다.

- 봉인 커밋: `5cb9eb0ce69fa4bfd64478f5a51b51838a3bb039` (계약 파일 1 개, `conditions_digest: sha256:a37827c20fae4fbe`)
- 구현 커밋: `bfadfbb` (harness 스크립트 · 시험 넷) · `e4692cb` (harness 문서 열) · `3e874e8` (scripts 넷) ·
  `66b4e4c` (오케스트레이터 SKILL.md · sync-orchestrator.py) · `306948c` (카이젠 스킬 · 참조 문서 열) · `d97944c` (ci.yml)
- notes 커밋: `e31e01e4c14851ae73253974bff0b9c9738dde39` — notes · 검토 기록 · 이 파일의 측정 전제 문단. 범위 상한을 이 커밋으로 옮긴다

end_sha: d97944ca6892a4601ee02b5e8cefa93e9c69d6a1
end_sha: e31e01e4c14851ae73253974bff0b9c9738dde39
