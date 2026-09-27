---
feature: "PRD 없음 규칙 후속 — 승인 기록 경로 따라 읽기 · 계약도 없을 때 (PD2-1 · PD2-2)"
slug: after-0926-prd-none-followups
created: "2026-09-27 11:17"
complexity: "복잡"
conditions: 20
status: done
owner_session: bda55d45-296c-491f-89ba-b52042d58e72
conditions_digest: sha256:18c60a176e1f951f
measurement_digest: sha256:32776cae8d09b5ea
locked_at: "2026-09-27 11:29"
---

## 배경

앞 묶음 pd(가지 `chore/ak2-pd`, 계약 `.harness/sprint-contract-after-0926-prd-none-rules.md`, APPROVE 4 회차)의 독립 검토가 남긴 빈틈 둘을 한 계약으로 묶는다.
결정은 부모가 PD-1 원칙(결정 원문은 한 곳)으로 정했다. 입력은 읽기만 한다 — pd notes
`/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak2-pd/.harness/.meta/after-kaizen-0926b/pd-notes.md` 의 「이 계약의 판단」 정정 문단 · 「독립 검토 반영 (QA 뒤)」 2 · 3번 ·
「남은 것」 넷째 줄, 사용자 결정 `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0926b/.harness/.meta/after-kaizen-0926b/decisions.md` 의 PD-1 행, 남은 일 목록 같은 폴더 `leftovers.md` 의 `:85-92`.

- PD2-1: design-mockup Step 2 가 승인 기록 폐기 칸에 적힌 경로(PRD 비범위 표 또는 계약 `범위 경계`)를 따라가 원문을 읽고 막게 한다. pd 가 폐기 칸을
  경로만으로 바꾸면서 Step 2 가 폐기 항목을 못 보게 된 빈틈이다(pd notes 정정 문단 — 경로를 따라 읽으라는 말이 승인 뒤에 도는 Step 6 에만 있다).
- PD2-2: 그 기능의 PRD 도 작업 계약도 없는 프로젝트에서는 폐기 결정을 승인 기록 폐기 칸에 네 칸(하지 않는 것 · 이유 · 범위 · 코드에 남은 흔적)으로 그대로
  적는다. 자리가 그 하나뿐이라 원문 한 곳 원칙에 맞는다. design-mockup · `/sprint` · sprint-contract 의 PRD 없음 대체 규칙 문장 세 곳에 같은 순서
  (PRD → 계약 → 승인 기록)로 적는다. 네 칸 이름은 부모 지시의 「버린 것」 대신 plan-prd 비범위 표 머리 줄과 같은 「하지 않는 것」 을 쓴다(RE-02 — 같은 네 칸).
- 사용자 합의(Step 5): 위임으로 받은 것으로 적는다 — 세션 `bda55d45-296c-491f-89ba-b52042d58e72` 의 사용자 말 2026-09-26T10:09:00.557Z 와 결정 답
  2026-09-26T10:30:16.222Z, 추가 위임 2026-09-27T01:22:01.089Z. 조건을 느슨하게 하는 개정은 이 위임으로 동의 처리하지 않는다.
- 작업 폴더 W = `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak2-pd2`, 가지 `chore/ak2-pd2`, 시작점 `0dccce0`(pd 가지 끝). 시작 때
  `git status --short` 는 빈 출력이었다 — 앞 단계가 남긴 미커밋 파일 없음.
- 커밋 규칙: `git add <경로>` 뒤 `git commit -o <경로>` · 한 커밋에 맨 위 폴더 하나(`design-kit` · `harness` · `planning-kit` · `.harness` 가운데 하나) ·
  `git add -A` · `git stash` · push · 가지 바꾸기 금지. 봉인 커밋(계약 한 파일)이 구현 커밋보다 먼저다.
- 같은 파일을 다른 묶음이 고칠 수 있다. 이 계약은 sprint-contract 에서 한 줄(SK-03), `/sprint` 는 `### Step 0.5:` 절 산문 한 줄(SK-04), plan-prd 는
  Step 0 한 줄(SK-05), 규약은 §4 에 한 줄(SK-06), design-mockup 은 Step 2 · Step 6 두 절 안(SK-01 · SK-02)만 바꾼다.
- 구현 전에 `tone-kit:tone-guide` 1 단계(규칙 불러오기)를, 완료 선언 전에 5 단계(전수 대조)를 한다 — 대조 결과는 notes 에 남긴다(AR-02).
- 사용자가 할 일: 없음.

복잡도 4 축 — 넷 다 「예」 이고 공개 약속 변경과 소비자가 함께 있어 「복잡」 이다. Step 2.5 짝 조건: 쓰는 쪽(원문 자리를 정하는 글)은
SK-02(design-mockup Step 6) · SK-03(sprint-contract) · SK-04(`/sprint` 산문) · SK-06(규약 §4), 읽는 쪽은 SK-01(design-mockup Step 2 — 경로를 따라 읽는다) ·
SK-05(plan-prd Step 0 — 설명 글) · SC-01(`/sprint` Step 0.5 명령 · plan-prd 검색 · 승인 기록 확인 명령이 새 모양 기록을 실제로 찾는지)이다.

| 축 | 물음 | 값 |
| -- | ---- | -- |
| 레이어 수 | 몇 개 계층을 관통하는가 | 셋 — 킷 스킬 문서(design-kit · harness · planning-kit), 킷 규약 문서(`visual-change-protocol.md`), 작업 기록(`.harness/`) |
| 공개 API·계약 변경 | 밖에 드러난 약속이 바뀌는가 | 예 — 계약도 없을 때 폐기 결정을 적는 자리(승인 기록 폐기 칸)와 그 줄 모양(결정 하나에 들여쓴 한 줄 · 줄 끝 `PRD 없음`), Step 2 가 읽는 범위(폐기 칸의 경로 너머) |
| 소비면 존재 | 반대편이 있는가 | 예 — `/sprint` Step 0.5 명령 · plan-prd Step 0 검색 · 승인 기록 확인 명령(`→ 2`) · design-mockup Step 2 · 이미 있는 사용자 프로젝트 승인 기록 |
| 회귀 위험 | 기존 동작이 깨질 수 있는가 | 예 — 승인 기록 확인 명령 `→ 2`, `/sprint` 재검증 명령 · 보고 줄, 다른 묶음이 고치는 sprint-contract · sprint |

설정 값 대조 (`.harness/project.yaml` 을 글자 그대로 옮김):

| config key | project.yaml 에서 읽은 값 | 계약에 쓴 값 |
| ---------- | ------------------------- | ------------ |
| `commands.analyze` | `bash -n scripts/release.sh` | DG-01 N/A — 재는 파일이 바뀐 파일에 없다 |
| `commands.test` | `bash scripts/release.sh 2>&1 \|\| true` | DG-03 N/A — 같은 이유 |
| `diagnostics.ide_exclude` | `[]` | DG-02 의 `([] 제외)` |
| `contract_categories[].id` / `prefix` | Skill/SK · Script/SC · Error/ER · Architecture/AR | 같은 넷 |
| `anti_patterns[].id` / `message` | AP-01 버전 하드코딩 · AP-02 force push · AP-03 bare code fence · AP-04 frontmatter name 누락 | AP-03 · AP-04 (바뀌는 파일이 코드 블록 있는 SKILL.md 넷과 규약 문서다). AP-01 은 plugin.json 버전을 건드리지 않아서, AP-02 는 이 계약이 push 하지 않아서 뺐다 |

## GAP 분석 (Pre-Edit Audit)

대상 파일을 읽기만 하고 줄을 적었다. 줄 번호는 시작점 `0dccce0` 기준이다.

| 대상 파일 | 실제 Read 증거 (`파일:라인`) | 발견한 기존 갭·위반 | 계약 조건화 여부 |
| --------- | ---------------------------- | ------------------- | ---------------- |
| `design-kit/skills/design-mockup/SKILL.md` Step 2 | `:50` 절 머리 · `:54-61` 감지 대상 코드 블록(`:59` 승인 기록 · `:60` PRD) · `:66-67` 승인 기록 규칙(`:67` 은 그 괄호 근거) · `:68` PRD 비범위 표 규칙 · `:69-70` 앱 코드 규칙 | `:66` 은 승인 기록 폐기 칸에 적힌 것만 막는다. pd 뒤로 PRD 없을 때의 폐기 칸은 계약 경로뿐이라 Step 2 가 결정 항목을 모른다(PD2-1). 경로 파일이 새 워크트리에 없을 때 말할 줄도 없다 | SK-01 |
| 같은 파일 Step 6 | `:147` 절 머리 · `:160` 폐기 칸 틀(PRD 가 있을 때 경로와 「하지 않는 것」) · `:166` PRD 없을 때 문단(계약 `범위 경계` 한 곳 · 폐기 칸에는 계약 경로 · 「다음 시안 전에는 그 경로에서 … 읽어 Step 2 의 폐기 항목으로 쓴다」) · `:170-174` 확인 명령(`→ 2`) | 계약도 없을 때 결정을 어디에 적는지 없다 — 결정이 어디에도 안 남는다(pd 독립 검토 3번). 경로를 따라 읽으라는 말이 Step 6 에만 있다 | SK-02 |
| `design-kit/references/visual-change-protocol.md` §4 | `:181` 절 머리 · `:206` 틀 폐기 칸 · `:211-222` 규칙, 그중 `:221-222` 「제품 요구 수준의 폐기 결정 … 이 기록에서 새로 정하지 않는다. 그 결정이 적힌 파일 경로를 폐기 칸에 적는다」 | PD2-2 를 세 문장에만 적으면 이 규약이 「경로만」 이라 서로 어긋난다. design-mockup Step 2 `:67` · Step 6 `:166` 이 이 절을 근거로 든다 | SK-06 |
| `harness/skills/sprint-contract/SKILL.md` | `:626-640` 포맷 규칙 · `:635` 폐기 결정 줄(PRD 가 있으면 경로와 항목 이름 · 없으면 「결정 원문은 여기 한 곳」 · 승인 기록 · 핸드오프는 이 계약 경로를 가리킨다) | 계약보다 먼저 승인 기록 폐기 칸에 적힌 결정(계약도 없던 때)을 어떻게 할지 없다 — 계약에 다시 쓰면 원문이 두 곳 | SK-03 |
| `harness/skills/sprint/SKILL.md` Step 0.5 | `:56` 절 머리 · `:60-71` bash 블록(`:68-69` 두 grep 이 `"$root/.design" "$root/.harness"` 를 본다) · `:75-81` text 블록 · `:83` 원문 자리 문단(「그 기능의 PRD 가 없으면 원문은 계약 `범위 경계` 한 곳 … 승인 기록은 그 계약 경로를 가리킨다」) | 계약도 없을 때가 없다. 명령은 이미 `.design` 을 보므로 고치지 않아도 승인 기록 줄을 찾는다(SC-01 시작 판 실측 `tag2`) | SK-04 · SC-01 |
| `planning-kit/skills/plan-prd/SKILL.md` Step 0 | `:30` 절 머리 · `:39` 넷째 항목 「PRD 가 없을 때 계약 `범위 경계` 에 적어 둔 이 기능의 폐기 결정」 · 같은 줄 두 grep(`.harness .design`) · `→ .planning/prd-<slug>.md` 옮기기 | 읽는 쪽 설명이 계약만 말한다 — 명령은 `.design` 도 보지만 글을 따르면 승인 기록 줄을 이 기능 결정으로 안 볼 수 있다(짝 조건) | SK-05 |
| `docs/design-kit/design-mockup.html` | `:635` 옛 note(pd notes 드리프트 절) | 원본이 또 바뀐다 — 문서 사이트 묶음 DC-15 몫 | 넘김 (AR-02 notes) |
| 이 레포 `.harness` · `.design` | `/sprint` 두 검색을 끝 판 트리에 돌린 값 0 · 0(ER-01 시작 판) | 이 계약 · notes 가 폐기 결정처럼 보이는 줄을 만들면 `/sprint` 재검증이 이 레포에서 잘못 잡는다 | ER-01 |

개선안 — 구현이 넣을 글. 조건은 아래 낱말(토큰)만 재므로 문장은 톤 대조에 맞춰 다듬어도 된다. 같은 글을 사본에 넣는 스크립트는 세션 스크래치
`pd2/mock.py` 다(알려진 답 · 양성 대조에 썼다).

```text
[D2] design-mockup Step 2 — 「- PRD 비범위 표 존재 →」 줄 바로 뒤에 한 줄
- 승인 기록 폐기 칸이 경로를 가리킴 → 그 파일을 열어 원문을 읽는다. PRD 경로면 비범위 표 항목을, 작업 계약 경로면 `범위 경계` 에서 줄 끝이 `PRD 없음` 인 줄을 폐기 항목으로 쓰고 시안에 넣지 않는다. 파일이 없거나 못 읽으면(추적하지 않는 `.harness` 는 새 워크트리에 따라오지 않는다) `못 읽음: <경로>` 를 말하고 시안을 만들기 전에 사용자에게 묻는다

[D6] design-mockup Step 6 :166 — 「다음 시안 전에는 그 경로에서 … Step 2 의 폐기 항목으로 쓴다.」 한 문장을 바꾼다. 앞 · 뒤 문장은 그대로
그 기능의 작업 계약도 없으면 결정 원문은 이 승인 기록 폐기 칸 한 곳이다 — 같은 네 칸을 결정 하나에 한 줄씩 폐기 칸 아래에 들여써 적고 줄 끝에 `PRD 없음` 을 붙인다. 다음 시안 전에는 Step 2 가 폐기 칸의 경로를 따라 원문을 읽는다.

[V1] visual-change-protocol.md §4 규칙 — 「파일 경로를 폐기 칸에 적는다 — …」 줄 바로 뒤에 들여쓴 한 줄
  그 기능의 PRD 도 작업 계약도 없으면 사용자가 내린 그 결정의 원문은 이 기록 폐기 칸 한 곳이다 — 네 칸으로 적고 줄 끝에 `PRD 없음` 을 붙인다 (`design-mockup` Step 6).

[C1] sprint-contract 포맷 규칙 :635 — 줄 끝(「결정을 다시 쓰지 않는다」 뒤)에 이어 붙인다 (한 줄 바꾸기)
… 결정을 다시 쓰지 않는다. 그 기능의 계약도 없던 때 적은 결정은 디자인 승인 기록 폐기 칸에 네 칸으로 있다(줄 끝 `PRD 없음`) — 옮겨 적지 말고 그 승인 기록 경로만 적는다

[S1] /sprint Step 0.5 :83 — 「— 승인 기록은 그 계약 경로를 가리킨다.」 바로 뒤에 한 문장
그 기능의 계약도 없으면 원문은 디자인 승인 기록 폐기 칸 한 곳에 같은 네 칸으로 적고 줄 끝에 `PRD 없음` 을 붙인다 — 위 grep 이 `.design` 도 보므로 그 줄도 모인다.

[P1] plan-prd Step 0 :39 — 첫 문장만 바꾼다
PRD 가 없을 때 계약 `범위 경계`(계약도 없으면 디자인 승인 기록 폐기 칸)에 적어 둔 이 기능의 폐기 결정이다.
```

## 범위 경계

항목별 처리 — 입력은 부모가 준 두 항목(PD2-1 · PD2-2)이다. 바깥 문서가 있어야 판단되는 항목은 없다.

| 항목 | 처리 | 조건 · 사유 |
| --- | --- | --- |
| PD2-1 Step 2 가 폐기 칸의 경로를 따라 읽기 | 계약에 넣음 | SK-01 · SK-02 `oneline` 셋째. Step 2 에 규칙 한 줄을 더하고, Step 6 의 「다음 시안 전에는 그 경로에서 …」 문장은 Step 2 를 가리키는 말로 바꾼다 — 같은 절차 원문이 두 곳에 있지 않게 한다. PRD 경로일 때도 따라 읽는다(폐기 칸 `:160` 은 「하지 않는 것」 이름만 있고 이유 · 범위는 PRD 에 있다). 파일을 못 읽으면 `못 읽음: <경로>` 로 말하고 묻는다 — pd 의 `/sprint` Step 0.5 가 새 워크트리 문제를 같은 말로 다룬다 |
| PD2-2 계약도 없을 때 승인 기록 폐기 칸에 네 칸 | 계약에 넣음 | SK-02 · SK-03 · SK-04 가 같은 순서(PRD → 계약 → 승인 기록)를 `ordok` 로 잰다. 줄 모양은 결정 하나에 폐기 칸 아래 들여쓴 한 줄 · 줄 끝 `PRD 없음` — 틀의 `- 폐기한 대안·이유:` 줄이 하나로 남아 확인 명령 `→ 2` 가 그대로 맞고(SC-01 `check=2`), `/sprint` · plan-prd 의 첫째 검색이 그 줄을 찾는다(SC-01 `tag2` · `prd=2`) |
| 규약 `visual-change-protocol.md` §4 한 줄 | 계약에 넣음 (부모 지시 세 곳 밖 — 판단) | SK-06. `:221-222` 가 「그 결정이 적힌 파일 경로를 폐기 칸에 적는다」 라 PD2-2 와 어긋나고, design-mockup Step 2 · Step 6 이 이 절을 근거로 든다. 같은 규칙이 적힌 자리를 다 고치지 않으면 한쪽이 남는다. 옛 두 줄은 그대로 두고 예외 한 줄만 더한다. pd 계약 SK-06 이 이 파일을 「그대로」 로 잰 것은 pd 범위 안의 일이다 |
| plan-prd Step 0 설명 글 | 계약에 넣음 (짝 조건 — 판단) | SK-05. 읽는 쪽이다(Step 2.5). 명령은 `.design` 도 보지만 글이 「계약 `범위 경계` 에 적어 둔」 이라 승인 기록 줄을 놓칠 수 있다. 첫 문장 괄호 한 곳만 바꾸고 두 검색 · 옮기기 절차는 글자 그대로 둔다 |
| 계약을 나중에 쓸 때 승인 기록에 이미 있는 결정 | 계약에 넣음 (판단) | SK-03 `ptr`. 옮겨 적지 않고 그 승인 기록 경로만 적는다 — 원문을 한 곳에 두는 가장 작은 길이다. 줄 끝 `PRD 없음` 이 승인 기록에 남으므로 PRD 가 생기면 plan-prd Step 0 이 그 줄을 비범위 표로 옮긴다(pd PD-4 절차 그대로) |
| `/sprint` Step 0.5 명령 · 보고 줄 | 바꾸지 않음 | 두 grep 이 이미 `"$root/.design"` 을 본다. SK-04 `same_bash=1 same_text=1` 로 그대로인지 잰다 |
| design-mockup Step 2 감지 대상 코드 블록 | 바꾸지 않음 | 블록은 파일 모양만 적는다. 경로를 따라 읽는 규칙은 아래 불릿에 둔다 |
| 둘째 검색(코드 표시 기호 · 마침표 모양)이 새 들여쓴 줄을 잡는지 | 해당 없음 | 규칙이 보여 주는 모양이 기호 없는 줄 끝이라 첫째 검색이 잡는다. 둘째 검색은 들여쓴 목록 항목도 보므로(`^[[:space:]]*` 로 시작) 기호째 옮겨 적은 경우도 잡는다 |
| `docs/design-kit/design-mockup.html` | 범위 밖 · 넘김 | 원본 Step 2 · Step 6 이 또 바뀐다. notes 에 적어 문서 사이트 묶음 DC-15 로 넘긴다(AR-02) |
| 핸드오프 틀(`~/.claude/hooks/next-session-handoff.sh`) · US-5 | 범위 밖 | 레포 밖 사용자 훅 묶음 몫 |
| 남은 일 목록의 다른 절 · 킷 `plugin.json` 버전 · `scripts/` · `.github/` | 범위 밖 | 과제가 정한 범위 밖. 버전은 릴리스 단계 몫 |
| 이 계약 · notes 가 `/sprint` 검색에 걸리기 | 계약에 넣음 | ER-01. 측정 도우미의 시험 입력은 `printf` 인자로 따로 넣어 줄이 따옴표로 끝난다 |
| DG-05 작업 폴더 조건과 평가자의 `status:` 편집 | 계약에 넣음 (pd QA 3 회차 개선 제안 반영) | DG-05 Given 이 계약 파일 `status:` 한 줄 차이는 허용한다 — 평가자가 APPROVE 때 바꾸는 줄이라 매 회차 비켜 갈 일이 없게 한다. 그 밖 차이가 있으면 전제가 안 선다 |

커버리지 해소 — Step 6.5 (4) 검출기가 낸 `UNCOVERED` 의 처리:

- 오라클 해소: SC-01 — 글이 아니라 끝 판 스킬 문서에서 떼어 낸 명령 셋을 알려진 답 입력 폴더에서 bash · zsh 로 실제로 돌려 출력 줄 수로 판정한다
- 오라클 해소: SK-04 — 산출물이 사람이 읽는 규칙 문장이라 문장 존재가 곧 산출물이다. 명령이 그대로인지는 bash · text 블록 글자 비교(`same_bash` · `same_text`)로, 명령이 새 모양 줄을 실제로 찾는지는 SC-01 이 실행으로 잰다
- 커버리지 해소: AR-02 — notes 경로는 측정 도우미 `NOTES` 변수가 그대로 담고(산문과 같은 글자), 여섯 토큰은 `m AR-02` 의 목록이 센다. `docs/design-kit/design-mockup.html` 은 담을 내용 설명이고 재는 토큰은 넘김 대상 묶음 이름 `DC-15` 다 — 페이지 경로는 줄 번호가 바뀌므로 토큰으로 잠그지 않는다. `visual-change-protocol.md` 는 목록에 같은 글자로 있다

## 회귀 게이트 — 측정 도우미

평가 때 이 블록을 떼어 bash 에서 불러 쓴다. `TMPDIR` 은 평가자 임시 폴더로 준다. 도우미는 끝점을 `git archive` 로 풀어 재므로 작업 폴더의 미커밋
변경을 보지 않는다. 작업 폴더 밖 입력은 지우지 마라 — 도우미가 만든 `$T` 아래만 치워도 된다. `MDL` 이 가리키는 markdownlint 설치본이 없으면
`mdl_ready` 가 그 자리에 설치한다(npm). 시작점 `BASE` 는 앞 묶음 가지와의 갈림점(`git merge-base chore/ak2-pd chore/ak2-pd2`, 봉인 전 `0dccce0`)이다 —
`origin/main` 과의 갈림점을 쓰면 pd 묶음의 변경까지 이 계약이 떠안는다.

```bash
# 떼기: awk '/^# === 측정 도우미 시작/{f=1} f{print} /^# === 측정 도우미 끝/{exit}' <계약> > "$TMPDIR/pd2-measure.sh"
# 부르기: bash -c 'source "$TMPDIR/pd2-measure.sh" || exit 2; type m >/dev/null || exit 2; m SK-01'
# 시작 판: E_REF=BASE 를 주고 부른다. 다른 사본을 재려면 W=<사본> PD_REF=origin/chore/ak2-pd 를 준다
# === 측정 도우미 시작 (after-0926-prd-none-followups) ===
# 쓰는 법: 이 블록을 파일로 떼어 bash 에서 source 한 뒤 `m <조건 ID>`. zsh 에서 source 하지 마라(도우미 안에서 zsh 를 따로 부른다).
# 잴 트리 E — 기본은 가지 끝(TIP)을 git archive 로 푼 임시 폴더. 시작 판을 재려면 E_REF=BASE. 다른 사본을 재려면 W=<사본> · PD_REF=<앞 묶음 가지>.
W=${W:-/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak2-pd2}
BR=${BR:-chore/ak2-pd2}
PD_REF=${PD_REF:-chore/ak2-pd}
BASE=$(git -C "$W" merge-base "$PD_REF" "$BR") || { echo "UNRESOLVED BASE"; return 2 2>/dev/null || exit 2; }
TIP=$(git -C "$W" rev-parse --verify "$BR") || { echo "UNRESOLVED TIP"; return 2 2>/dev/null || exit 2; }
T=$(mktemp -d "${TMPDIR:-/tmp}/pd2.XXXXXX")
snap() { mkdir -p "$2" && git -C "$W" archive "$1" | tar -x -C "$2"; }
case "${E_REF:-TIP}" in
  BASE) E=$T/base; snap "$BASE" "$E" ;;
  *)    E=$T/tip;  snap "$TIP" "$E" ;;
esac
DM=design-kit/skills/design-mockup/SKILL.md
VCP=design-kit/references/visual-change-protocol.md
SP=harness/skills/sprint/SKILL.md
SC=harness/skills/sprint-contract/SKILL.md
PRD=planning-kit/skills/plan-prd/SKILL.md
CF=.harness/sprint-contract-after-0926-prd-none-followups.md
NOTES=.harness/.meta/after-kaizen-0926b/pd2-notes.md
COLS='하지 않는 것 · 이유 · 범위 · 코드에 남은 흔적'
ALLOWED='design-kit/skills/design-mockup/SKILL.md
design-kit/references/visual-change-protocol.md
harness/skills/sprint/SKILL.md
harness/skills/sprint-contract/SKILL.md
planning-kit/skills/plan-prd/SKILL.md
.harness/sprint-contract-after-0926-prd-none-followups.md
.harness/sprint-feedback-after-0926-prd-none-followups.md
.harness/sprint-amendments-after-0926-prd-none-followups.md
.harness/.meta/after-kaizen-0926b/pd2-notes.md'
sec() { awk -v s="$1" -v e="$2" 'index($0,s)==1{f=1;print;next} f&&index($0,e)==1{exit} f' "$3"; }   # s 로 시작하는 줄부터 e 로 시작하는 다음 줄 앞까지
n() { grep -cF -- "$1" || true; }                                                                    # 표준 입력에서 글자 그대로 든 줄 수
nocode() { awk '/^[[:space:]]*```/{c=!c;next} !c'; }
blk() { awk -v t="$1" 'index($0,"```" t)==1{b=1;next} b&&/^```/{b=0} b'; }                           # 언어가 t 인 코드 블록 안 줄만
secrange() { awk -v s="$1" -v e="$2" 'index($0,s)==1{a=NR} a&&!z&&NR>a&&index($0,e)==1{z=NR} END{print a+0, z+0}' "$3"; }
numstat() { git -C "$W" diff --numstat "$BASE" "$TIP" -- "$1" | awk '{print $1"/"$2}'; }
added() { git -C "$W" diff -U0 "$BASE" "$TIP" -- "$1" | grep -E '^\+[^+]' | sed 's/^+//'; }
hunks() {  # hunks <파일> — 지운 줄 번호(BASE)는 "-N", 더한 줄 번호(TIP)는 "+N"
  git -C "$W" diff -U0 "$BASE" "$TIP" -- "$1" | awk '/^@@/{split($2,a,",");s=substr(a[1],2);c=(a[2]=="")?1:a[2];for(i=0;i<c;i++)print "-"(s+i);split($3,b,",");s=substr(b[1],2);c=(b[2]=="")?1:b[2];for(i=0;i<c;i++)print "+"(s+i)}'
}
outside() {  # outside <파일> <절 시작> <다음 절> [<절 시작> <다음 절>] — 준 절 어디에도 들지 않는 곳에서 바뀐 줄 수
  f=$1; shift; git -C "$W" show "$BASE:$f" > "$T/o.md"; br=""; tr_=""
  while [ $# -ge 2 ]; do br="$br $(secrange "$1" "$2" "$T/o.md")"; tr_="$tr_ $(secrange "$1" "$2" "$E/$f")"; shift 2; done
  hunks "$f" | awk -v br="$br" -v tr="$tr_" 'BEGIN{nb=split(br,b," ");nt=split(tr,t," ")}
    function inr(x,r,k,  i){for(i=1;i<k;i+=2) if(x>r[i]&&x<r[i+1]) return 1; return 0}
    /^-/{x=substr($0,2)+0; if(!inr(x,b,nb))o++} /^\+/{x=substr($0,2)+0; if(!inr(x,t,nt))o++} END{print o+0}'
}
ordok() {  # 표준 입력 줄 가운데 「계약도 없」 이 든 줄 수와, 그 줄이 PRD → 계약(`범위 경계` 한 곳 · 여기 한 곳) → 계약도 없 → 승인 기록 폐기 칸 → PRD 없음 순인지
  LC_ALL=C awk '/계약도 없/{c++; s=$0; a=index(s,"PRD"); if(!a){next} r=substr(s,a); b1=index(r,"`범위 경계` 한 곳"); b2=index(r,"여기 한 곳");
    b=(b1&&(!b2||b1<b2))?b1:b2; k=index(r,"계약도 없"); r2=substr(r,k); d=index(r2,"승인 기록 폐기 칸"); r3=substr(r2,d+length("승인 기록 폐기 칸")); e=index(r3,"PRD 없음");
    if(b>0&&b<k&&d>0&&e>0) ok++} END{printf "n=%d ok=%d", c+0, ok+0}'
}
fmv() { awk -v k="^${1}:[[:space:]]*" 'NR==1&&/^---[[:space:]]*$/{f=1;next} f&&/^---[[:space:]]*$/{exit} f&&$0~k{sub(k,"");print;exit}' "$2" | sed -e 's/[[:space:]]*$//' -e "s/^['\"]//" -e "s/['\"]\$//"; }
h16() { shasum -a 256 | cut -c1-16; }
digest() { grep -E '^- \[[ x]\] [A-Z]{2,}-[0-9]{2}' | sed -E 's/^- \[[ x]\]/- [ ]/' | h16; }
mdigest() { awk '/^- \[[ x]\] [A-Z][A-Z]+-[0-9][0-9]/{inb=1;match($0,/[A-Z][A-Z]+-[0-9][0-9]/);print substr($0,RSTART,RLENGTH);next} inb&&/^[ \t]+[^ \t]/{l=$0;sub(/[ \t]+$/,"",l);print l;next} inb&&/^[ \t]*$/{next} {inb=0}' | h16; }
MDL=${MDL:-/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/bda55d45-296c-491f-89ba-b52042d58e72/scratchpad/mdl}
mdl_ready() {  # markdownlint-cli2 0.23.2 · MD013 끔 — 편집기 확장과 같은 설정. 없으면 MDL 에 설치한다
  [ -x "$MDL/node_modules/.bin/markdownlint-cli2" ] || { mkdir -p "$MDL" && (cd "$MDL" && npm install --no-save --no-audit --no-fund markdownlint-cli2@0.23.2 >/dev/null 2>&1); }
  printf '{ "config": { "MD013": false } }\n' > "$T/cfg.markdownlint-cli2.jsonc"
  [ -x "$MDL/node_modules/.bin/markdownlint-cli2" ]
}
addn() { diff -U0 "$1" "$2" | awk '/^@@/{split($3,a,","); s=substr(a[1],2); c=(a[2]=="")?1:a[2]; for(i=0;i<c;i++) print s+i}'; }
newmd() {  # newmd <옛 파일|/dev/null> <새 파일> — 새 파일에서 더해진 줄에 걸린 경고 수
  ( cd "$(dirname "$2")" && "$MDL/node_modules/.bin/markdownlint-cli2" --config "$T/cfg.markdownlint-cli2.jsonc" "$(basename "$2")" 2>&1 ) \
    | awk -F: '/^[^ ]+:[0-9]+/{print $2+0}' | sort -n > "$T/w.txt"
  addn "$1" "$2" | sort -n > "$T/a.txt"
  comm -12 "$T/w.txt" "$T/a.txt" | grep -c . || true
}
fixture() {  # 알려진 답 입력 — 작업 계약도 PRD 도 없는 프로젝트의 승인 기록 한 벌(결정 두 줄)
  M=$T/m; mkdir -p "$M/.planning" "$M/.design/approvals" "$M/.harness"
  git -C "$M" init -q && git -C "$M" -c user.name=t -c user.email=t@t commit -q --allow-empty -m init
  { printf '%s\n' '# 승인 기록 — 홈' '- 확정 구성: 상단 카드 · 하단 목록' '- 폐기한 대안·이유: 아래 두 줄'
    printf '  - 시간대 설정 · 한 나라만 쓴다고 함 · 이번 화면 · 없음 · %s\n' 'PRD 없음'
    printf '  - 국가 목록 · 한 나라만 쓴다 · 제품 전체 · settings.ts 필드 · %s\n' 'PRD 없음'
    printf '%s\n' '- 미확정/후속: 없음'; } > "$M/.design/approvals/20260927-home.md"
}
m() {
  case "$1" in
  SK-01) s2=$(sec '## Step 2:' '## Step 3:' "$E/$DM" | nocode)
    ln=$(printf '%s\n' "$s2" | grep -F '폐기 칸' | grep -F '`범위 경계`' | grep -F '줄 끝이 `PRD 없음` 인 줄' | grep -F '비범위 표 항목' | grep -F '시안에 넣지 않는다' | grep -F '`못 읽음: <경로>`' | grep -F '사용자에게 묻는다')
    echo "follow=$(printf '%s\n' "$ln" | grep -c . || true) keep=$(printf '%s\n' "$s2" | n '- 승인 기록 존재 →')$(printf '%s\n' "$s2" | n '- PRD 비범위 표 존재 →')" ;;
  SK-02) s6=$(sec '## Step 6:' '## Step 7:' "$E/$DM"); p=$(printf '%s\n' "$s6" | nocode | grep -F '계약도 없')
    echo "$(printf '%s\n' "$s6" | nocode | ordok) oneline=$(printf '%s\n' "$p" | n '결정 하나에 한 줄')$(printf '%s\n' "$p" | n '들여써')$(printf '%s\n' "$p" | n 'Step 2 가 폐기 칸의 경로를 따라') old=$(n '그 경로에서 줄 끝이 `PRD 없음` 인 줄을 읽어' <"$E/$DM") d1=$(printf '%s\n' "$s6" | n '그 기능 PRD 비범위 표 경로와 그 줄의 「하지 않는 것」 만 적는다') check=$(printf '%s\n' "$s6" | n "grep -cE '^- (확정 구성|폐기한 대안·이유):'") outside=$(outside "$DM" '## Step 2:' '## Step 3:' '## Step 6:' '## Step 7:')" ;;
  SK-03) add=$(added "$SC"); fmt=$(awk '/^\*\*포맷 규칙/{f=1;next} f&&/^### 6\.2\./{exit} f' "$E/$SC")
    i=0; [ -n "$add" ] && i=$(printf '%s\n' "$fmt" | grep -cxF -- "$add" || true)
    echo "numstat=$(numstat "$SC") in_fmt=$i $(nocode <"$E/$SC" | ordok) keep=$(printf '%s\n' "$add" | n '결정 원문은 여기 한 곳이다')$(printf '%s\n' "$add" | n '이 계약 경로를 가리키고') ptr=$(printf '%s\n' "$add" | n '옮겨 적지 말고 그 승인 기록 경로만 적는다') argsub=$(printf '%s\n' "$add" | grep -cE '(^|[^\\])[$][0-9]' || true)" ;;
  SK-04) s=$(sec '### Step 0.5:' '### Step 1:' "$E/$SP"); o=$(git -C "$W" show "$BASE:$SP" | sec '### Step 0.5:' '### Step 1:' /dev/stdin)
    same_bash=0; [ "$(printf '%s\n' "$s" | blk bash)" = "$(printf '%s\n' "$o" | blk bash)" ] && same_bash=1
    same_text=0; [ "$(printf '%s\n' "$s" | blk text)" = "$(printf '%s\n' "$o" | blk text)" ] && same_text=1
    echo "numstat=$(numstat "$SP") $(printf '%s\n' "$s" | nocode | ordok) design=$(printf '%s\n' "$s" | nocode | grep -F '계약도 없' | n '`.design` 도 보므로') same_bash=$same_bash same_text=$same_text outside=$(outside "$SP" '### Step 0.5:' '### Step 1:')" ;;
  SK-05) s0=$(sec '## Step 0:' '## Step 1:' "$E/$PRD"); it=$(printf '%s\n' "$s0" | grep -F '4. **`PRD 없음` 기록**')
    echo "numstat=$(numstat "$PRD") item=$(printf '%s\n' "$it" | grep -c . || true) both=$(printf '%s\n' "$it" | n '계약 `범위 경계`(계약도 없으면 디자인 승인 기록 폐기 칸)') g1=$(printf '%s\n' "$it" | n "grep -rnE 'PRD 없음[[:space:]]*[|]?[[:space:]]*\$' .harness .design") g2=$(printf '%s\n' "$it" | n "PRD 없음(\`[.]?|[.])[[:space:]]*[|]?[[:space:]]*\$' .harness .design") keep=$(printf '%s\n' "$it" | n '`→ .planning/prd-<slug>.md`')$(printf '%s\n' "$it" | n '다른 기능의 줄은 옮기지 않는다') outside=$(outside "$PRD" '## Step 0:' '## Step 1:')" ;;
  SK-06) s4=$(sec '## 4. Design Approval Record' '## 5. ' "$E/$VCP")
    echo "numstat=$(numstat "$VCP") new=$(printf '%s\n' "$s4" | grep -F 'PRD 도 작업 계약도 없으면' | grep -F '폐기 칸 한 곳' | grep -F '줄 끝에 `PRD 없음`' | grep -c . || true) keep=$(printf '%s\n' "$s4" | n '이 기록에서 새로 정하지 않는다')$(printf '%s\n' "$s4" | n '파일 경로를 폐기 칸에 적는다') outside=$(outside "$VCP" '## 4. Design Approval Record' '## 5. ')" ;;
  SC-01) fixture; sec '### Step 0.5:' '### Step 1:' "$E/$SP" | blk bash | awk '/git worktree list/{f=1} f' > "$T/lines.sh"
    ck=$(sec '## Step 6:' '## Step 7:' "$E/$DM" | blk bash | grep -F "grep -cE '^- (확정 구성|폐기한 대안·이유):'" | sed -E 's/[[:space:]]+#.*$//; s#\.design/approvals/\{파일명\}\.md#.design/approvals/20260927-home.md#')
    g1=$(sec '## Step 0:' '## Step 1:' "$E/$PRD" | grep -F '4. **`PRD 없음` 기록**' | awk '{i=index($0,"`grep -rnE '"'"'PRD 없음"); r=substr($0,i+1); print substr(r,1,index(r,"`")-1)}')
    r=""; for sh in bash zsh; do (cd "$M" && "$sh" "$T/lines.sh" >"$T/o" 2>"$T/e"); r="$r $sh=out$(grep -c . "$T/o" || true)/tag$(grep -c 'approvals/20260927-home.md:[0-9]*:  - ' "$T/o" || true)/miss$(grep -c '^못 읽음: ' "$T/o" || true)/err$(grep -c . "$T/e" || true)"; done
    echo "lines=$(grep -c . "$T/lines.sh" || true)${r} check=$( (cd "$M" && bash -c "$ck") 2>/dev/null ) prd=$( (cd "$M" && bash -c "$g1") | grep -c . || true)" ;;
  ER-01) a=$(cd "$E" && grep -rnE 'PRD 없음[[:space:]]*[|]?[[:space:]]*$' .design .harness 2>/dev/null | grep -c . || true)
    b=$(cd "$E" && grep -rnE '^[[:space:]]*([-*+][[:space:]]|[0-9]+[.)][[:space:]]|[|]).*PRD 없음(`[.]?|[.])[[:space:]]*[|]?[[:space:]]*$' .design .harness 2>/dev/null | grep -c . || true)
    echo "tail1=$a tail2=$b" ;;
  AR-01) ch=$(git -C "$W" diff --no-renames --name-only "$BASE" "$TIP")
    extra=$(printf '%s\n' "$ch" | grep . | grep -vxF -f <(printf '%s\n' "$ALLOWED") | grep -c . || true)
    req=""; for f in "$DM" "$VCP" "$SP" "$SC" "$PRD"; do req="$req$(printf '%s\n' "$ch" | grep -cxF "$f" || true)"; done
    multi=0; for c in $(git -C "$W" rev-list "$BASE..$TIP"); do t=$(git -C "$W" show --name-only --format= "$c" | awk -F/ 'NF{print $1}' | sort -u | grep -c .); [ "$t" -gt 1 ] && multi=$((multi + 1)); done
    echo "base=${BASE:0:7} changed=$(printf '%s\n' "$ch" | grep -c . || true) extra=$extra req=$req multi_top=$multi"
    [ "$extra" = 0 ] || printf '%s\n' "$ch" | grep . | grep -vxF -f <(printf '%s\n' "$ALLOWED") ;;
  AR-02) b=$(git -C "$W" show "$TIP:$NOTES" 2>/dev/null); c=0; [ -n "$b" ] && c=1; out="committed=$c"
    for k in PD2-1 PD2-2 visual-change-protocol.md plan-prd DC-15 tone-guide; do out="$out $(printf '%s\n' "$b" | n "$k")"; done
    echo "$out" ;;
  AR-03) seal=$(git -C "$W" rev-list --reverse "$BASE..$TIP" -- "$CF" | head -1); sf=0; before=0; same=0; msame=0
    if [ -n "$seal" ]; then
      sf=$(git -C "$W" show --name-only --format= "$seal" | grep -c . || true)
      fi_=$(git -C "$W" rev-list --reverse "$BASE..$TIP" -- design-kit harness planning-kit | head -1)
      [ -n "$fi_" ] && [ "$seal" != "$fi_" ] && git -C "$W" merge-base --is-ancestor "$seal" "$fi_" && before=1
      [ "$(git -C "$W" show "$seal:$CF" | digest)" = "$(digest <"$E/$CF")" ] && same=1
      [ "$(git -C "$W" show "$seal:$CF" | mdigest)" = "$(mdigest <"$E/$CF")" ] && msame=1
    fi
    st=ABSENT; rec=$(fmv conditions_digest "$E/$CF" 2>/dev/null); rec=${rec#sha256:}
    [ -n "$rec" ] && { [ "$rec" = "$(digest <"$E/$CF")" ] && st=OK || st=BROKEN; }
    ms=ABSENT; rec=$(fmv measurement_digest "$E/$CF" 2>/dev/null); rec=${rec#sha256:}
    [ -n "$rec" ] && { [ "$rec" = "$(mdigest <"$E/$CF")" ] && ms=OK || ms=BROKEN; }
    echo "seal_commit_files=$sf seal_before_impl=$before seal_same_as_tip=$same measure_same_as_tip=$msame this=SEAL_$st MEASURE_$ms" ;;
  RE-01) echo "added=$(git -C "$W" diff --diff-filter=A --name-only "$BASE" "$TIP" -- . ':(exclude).harness' | grep -c . || true)" ;;
  RE-02) echo "hdr=$(n '| 하지 않는 것 | 이유 | 범위 | 코드에 남은 흔적 |' <"$E/$PRD") cols=$(n "$COLS" <"$E/$DM")$(n "$COLS" <"$E/$SC")$(n "$COLS" <"$E/$PRD")" ;;
  DG-01) echo "release_sh=$(git -C "$W" diff --name-only "$BASE" "$TIP" | grep -cx 'scripts/release.sh' || true)" ;;
  DG-03) m DG-01 ;;
  DG-04) echo "non_md=$(git -C "$W" diff --name-only "$BASE" "$TIP" | grep . | grep -vc '[.]md$' || true)" ;;
  DG-02) mdl_ready || { echo "MDL_NOT_READY"; return; }; tot=0; rows=""
    for f in $(git -C "$W" diff --name-only "$BASE" "$TIP" -- '*.md' ':(exclude).harness/sprint-*.md'); do
      o=$T/old.md; git -C "$W" show "$BASE:$f" > "$o" 2>/dev/null || : > "$o"
      c=$(newmd "$o" "$E/$f"); tot=$((tot + c)); rows="$rows $f=$c"; done
    echo "md_new=$tot |$rows" ;;
  AP-03) python3 "$E/scripts/validate-plugin.py" --check=code-fence >"$T/v6.log" 2>&1; rc=$?; echo "v6_rc=$rc fail=$(n 'FAIL' <"$T/v6.log")" ;;
  AP-04) python3 "$E/scripts/validate-plugin.py" --check=frontmatter >"$T/v1.log" 2>&1; rc=$?; echo "v1_rc=$rc fail=$(n 'FAIL' <"$T/v1.log")" ;;
  *) echo "모르는 조건 $1"; return 2 ;;
  esac
}
# === 측정 도우미 끝 ===
```

봉인 전 실측(2026-09-27). 「시작 판」 은 W 에서 가지 끝이 아직 시작점과 같을 때 잰 값이다. 「good」 은 W 를 복제한 임시 사본에 봉인 커밋(가짜 계약) →
`pd2/mock.py` 개선안을 킷마다 커밋 → notes 커밋을 넣은 판(알려진 답), 「bad」 · 「bad2」 는 일부러 망가뜨린 판(양성 대조)이다 —
bad: good + design-mockup Step 2 새 줄 지움 · `/sprint` 두 grep 에서 `"$root/.design"` 뺌 · sprint-contract 끝에 줄 더함 · plan-prd `name:` 줄 삭제와 끝에 언어 없는
코드 블록 · `scripts/x.sh` 새 파일을 한 커밋에(킷 셋 + `scripts`) · 봉인 뒤 조건 문구 변조 · notes 에 `#bad heading` 과 줄 끝이 `PRD 없음` 인 폐기 칸 모양 한 줄,
bad2: good + `/sprint` 새 문장을 문단 맨 앞(계약 문장보다 앞)으로 옮김 · design-mockup · 규약 · `/sprint` · plan-prd 파일 끝(절 밖)에 빈 줄과 한 줄씩.
사본 만들기는 스크래치 `pd2/build.sh`, 조건 전부 재기는 `pd2/runall.sh`.

| 조건 | 시작 판 | good (알려진 답) | 양성 대조 |
| --- | --- | --- | --- |
| SK-01 | `follow=0 keep=11` | `follow=1 keep=11` | bad `follow=0` |
| SK-02 | `n=0 ok=0 oneline=000 old=1 d1=1 check=1 outside=0` | `n=1 ok=1 oneline=111 old=0 d1=1 check=1 outside=0` | bad2 `outside=2` |
| SK-03 | `numstat= in_fmt=0 n=0 ok=0 keep=00 ptr=0 argsub=0` | `numstat=1/1 in_fmt=1 n=1 ok=1 keep=11 ptr=1 argsub=0` | bad `numstat=3/1` |
| SK-04 | `numstat= n=0 ok=0 design=0 same_bash=1 same_text=1 outside=0` | `numstat=1/1 n=1 ok=1 design=1 same_bash=1 same_text=1 outside=0` | bad `numstat=3/3 … same_bash=0` · bad2 `numstat=3/1 n=1 ok=0 … outside=2` |
| SK-05 | `numstat= item=1 both=0 g1=1 g2=1 keep=11 outside=0` | `numstat=1/1 item=1 both=1 g1=1 g2=1 keep=11 outside=0` | bad `numstat=5/2 … outside=5` · bad2 `numstat=3/1 … outside=2` |
| SK-06 | `numstat= new=0 keep=11 outside=0` | `numstat=1/0 new=1 keep=11 outside=0` | bad2 `numstat=3/0 … outside=2` |
| SC-01 | `lines=7 bash=out2/tag2/miss0/err0 zsh=out2/tag2/miss0/err0 check=2 prd=2` | 같음 | bad `bash=out0/tag0/… zsh=out0/tag0/…` |
| ER-01 | `tail1=0 tail2=0` | 같음 | bad `tail1=1` |
| AR-01 | `base=0dccce0 changed=0 extra=0 req=00000 multi_top=0` | `changed=7 extra=0 req=11111 multi_top=0` | bad `changed=8 extra=1 … multi_top=1` + `scripts/x.sh` 출력 |
| AR-02 | `committed=0` 과 0 여섯 | `committed=1` 과 1 여섯 | 시작 판이 실패 값 |
| AR-03 | `seal_commit_files=0 seal_before_impl=0 seal_same_as_tip=0 measure_same_as_tip=0 this=SEAL_ABSENT MEASURE_ABSENT` | `seal_commit_files=1 seal_before_impl=1 seal_same_as_tip=1 measure_same_as_tip=1 this=SEAL_OK MEASURE_OK` | bad `seal_same_as_tip=0 … this=SEAL_BROKEN` |
| RE-01 · RE-02 | `added=0` · `hdr=3 cols=111` | 같음 | bad `added=1` |
| DG-01 · DG-04 | `release_sh=0` · `non_md=0` | 같음 | bad `non_md=1` |
| DG-02 | `md_new=0 \|` (바뀐 파일 없음) | `md_new=0` (여섯 파일 각 0) | bad `md_new=2` (notes) |
| AP-03 · AP-04 | `v6_rc=0 fail=0` · `v1_rc=0 fail=0` | 같음 | bad `v6_rc=2 fail=2` · `v1_rc=2 fail=2` |
| DG-05 (ci-local) | `rc=0` 25 줄 · `feedback-agg-test SKIP (yq 없음)` 한 줄 (요약 스크래치 `pd2/ci0/ci-local/summary.txt`) | — | bad `v1_rc=2` 와 같은 검사(`validate-plugin`)가 CI 단계에 든다 |

측정 준비 단계도 봉인 전에 돌렸다: `command -v zsh` → `/bin/zsh`, `command -v shasum` → `/usr/bin/shasum`, markdownlint-cli2 0.23.2 설치본(`MDL` 기본 경로) 있음,
`ci-local.sh` 지문 `59fe55125c0dbc77`. SC-01 · ER-01 은 이 계약 · notes 가 들어간 뒤의 끝 판에서 다시 잰다(시작 판에는 이 계약이 없다).

교차 진단 반영(봉인 전): `ordok` 이 `승인 기록 폐기 칸` 이 끝난 뒤부터 `PRD 없음` 을 찾게 고쳤고, AR-01 의 경로 목록에 `--no-renames` 를 붙였고,
GAP 표 Step 2 줄 번호를 실제 파일에 맞췄다. 고친 도우미로 good · bad · bad2 를 다시 재서 위 표와 같은 값을 얻었다. 순서 판정 나쁜 예 한 줄
(`PRD 없음` 이 `승인 기록 폐기 칸` 보다 앞에만 있음)은 `n=1 ok=0`, 바른 순서 한 줄은 `n=1 ok=1` 이다.

## Skill

- [ ] SK-01: design-mockup Step 2 가 승인 기록 폐기 칸의 경로를 따라 원문을 읽고 막는다(PD2-1 · 읽는 쪽) — Given 구현 커밋이 가지 `chore/ak2-pd2` 에 들어간 뒤, When `design-kit/skills/design-mockup/SKILL.md` 의 `## Step 2:` 절(다음 `## Step 3:` 앞까지) 코드 블록 밖 줄을 읽으면, Then `폐기 칸` · `` `범위 경계` `` · `` 줄 끝이 `PRD 없음` 인 줄 `` · `비범위 표 항목` · `시안에 넣지 않는다` · `` `못 읽음: <경로>` `` · `사용자에게 묻는다` 가 모두 든 줄이 정확히 1 줄이고, 기존 두 규칙 `- 승인 기록 존재 →` · `- PRD 비범위 표 존재 →` 로 시작하는 줄이 각 1 줄 그대로다 [exact]
  측정: `m SK-01` 이 `follow=1 keep=11` (시작 판 `follow=0 keep=11`, good 은 기대값 그대로)
  양성 대조: bad(Step 2 새 줄 지움)에서 `follow=0` (봉인 전 실측)
- [ ] SK-02: design-mockup Step 6 이 계약도 없을 때 결정 원문을 승인 기록 폐기 칸 한 곳에 두고, 순서가 PRD → 계약 → 승인 기록이다(PD2-2 · 쓰는 쪽) — Given 구현 커밋 뒤, When `## Step 6:` 절(다음 `## Step 7:` 앞까지) 코드 블록 밖 줄을 읽으면, Then (a) `계약도 없` 이 든 줄이 1 줄이고 그 줄에서 첫 `PRD` 뒤에 `` `범위 경계` 한 곳 `` 이, 그 뒤에 `계약도 없` 이, 그 뒤에 `승인 기록 폐기 칸` 이, 그 뒤에 `PRD 없음` 이 순서대로 나온다 (b) 그 줄에 `결정 하나에 한 줄` · `들여써` · `Step 2 가 폐기 칸의 경로를 따라` 가 있다 (c) 옛 문장 `` 그 경로에서 줄 끝이 `PRD 없음` 인 줄을 읽어 `` 는 파일 전체에 0 줄이다 (d) PRD 가 있을 때의 폐기 칸 글 `그 기능 PRD 비범위 표 경로와 그 줄의 「하지 않는 것」 만 적는다` 와 확인 명령 줄 `grep -cE '^- (확정 구성|폐기한 대안·이유):'` 이 절 안에 각 1 줄 그대로다 (e) 이 파일의 차이가 모두 `## Step 2:` 절과 `## Step 6:` 절 안이다 [exact]
  측정: `m SK-02` 가 `n=1 ok=1 oneline=111 old=0 d1=1 check=1 outside=0` (시작 판 `n=0 ok=0 oneline=000 old=1 d1=1 check=1 outside=0`, good 은 기대값 그대로)
  양성 대조: bad2(파일 끝, 곧 두 절 밖에 빈 줄과 한 줄)에서 `outside=2`. 순서 판정 `ordok` 의 나쁜 예는 SK-04 의 bad2 `ok=0` 이다 (봉인 전 실측)
- [ ] SK-03: sprint-contract 는 폐기 결정 줄 하나만 바꾸고, 같은 순서를 적고, 계약보다 먼저 승인 기록에 적힌 결정은 옮겨 적지 않고 가리키게 한다(PD2-2) — Given 구현 커밋 뒤, When 시작점 `BASE` 부터 끝점 `TIP` 까지(AR-01 과 같은 해석) `harness/skills/sprint-contract/SKILL.md` 의 차이를 보면, Then 더한 줄 1 · 지운 줄 1 이고, 더한 줄이 끝 판의 `**포맷 규칙` 줄과 `### 6.2.` 줄 사이에 있으며, 파일의 코드 블록 밖에 `계약도 없` 이 든 줄이 1 줄이고 그 줄이 SK-02 (a) 와 같은 순서(첫 `PRD` → `여기 한 곳` → `계약도 없` → `승인 기록 폐기 칸` → `PRD 없음`)를 지키며, 더한 줄이 앞 묶음 글 `결정 원문은 여기 한 곳이다` · `이 계약 경로를 가리키고` 를 그대로 담고 `옮겨 적지 말고 그 승인 기록 경로만 적는다` 를 더 담는다. 더한 줄에 역슬래시 없는 `$`+숫자가 0 이다(스킬 본문 인자 치환, validate-plugin V9) [exact]
  측정: `m SK-03` 이 `numstat=1/1 in_fmt=1 n=1 ok=1 keep=11 ptr=1 argsub=0` (시작 판 `numstat= in_fmt=0 n=0 ok=0 keep=00 ptr=0 argsub=0`, good 은 기대값 그대로)
  양성 대조: bad(파일 끝에 줄 더함)에서 `numstat=3/1` (봉인 전 실측)
- [ ] SK-04: `/sprint` 재검증 문단이 같은 순서를 적고 명령 · 보고 틀은 그대로다(PD2-2 · 쓰는 쪽) — Given 구현 커밋 뒤, When `harness/skills/sprint/SKILL.md` 의 `### Step 0.5:` 절(다음 `### Step 1:` 앞까지)을 시작 판과 대조하면, Then (a) 이 파일의 차이가 더한 줄 1 · 지운 줄 1 이고 모두 그 절 안이다 (b) 코드 블록 밖에 `계약도 없` 이 든 줄이 1 줄이고 SK-02 (a) 와 같은 순서(첫 `PRD` → `` `범위 경계` 한 곳 `` → `계약도 없` → `승인 기록 폐기 칸` → `PRD 없음`)를 지키며 그 줄에 `` `.design` 도 보므로 `` 가 있다 (c) 절 안 bash 코드 블록과 text 코드 블록이 시작 판과 글자 그대로 같다 [exact]
  측정: `m SK-04` 가 `numstat=1/1 n=1 ok=1 design=1 same_bash=1 same_text=1 outside=0` (시작 판 `numstat= n=0 ok=0 design=0 same_bash=1 same_text=1 outside=0`, good 은 기대값 그대로)
  양성 대조: bad(두 grep 에서 `.design` 뺌)에서 `same_bash=0` · bad2(새 문장을 문단 맨 앞으로 · 파일 끝에 줄)에서 `ok=0 … outside=2` (봉인 전 실측)
- [ ] SK-05: plan-prd Step 0 설명이 승인 기록 폐기 칸도 읽을 자리로 적는다(짝 조건 · 읽는 쪽) — Given 구현 커밋 뒤, When `planning-kit/skills/plan-prd/SKILL.md` 의 `## Step 0:` 절(다음 `## Step 1:` 앞까지)을 읽으면, Then (a) 이 파일의 차이가 더한 줄 1 · 지운 줄 1 이고 모두 그 절 안이다 (b) `` 4. **`PRD 없음` 기록** `` 이 든 줄이 1 줄이고 그 줄에 `` 계약 `범위 경계`(계약도 없으면 디자인 승인 기록 폐기 칸) `` 이 있다 (c) 같은 줄의 두 검색 `grep -rnE 'PRD 없음[[:space:]]*[|]?[[:space:]]*$' .harness .design` · ``PRD 없음(`[.]?|[.])[[:space:]]*[|]?[[:space:]]*$' .harness .design`` 과 `` `→ .planning/prd-<slug>.md` `` · `다른 기능의 줄은 옮기지 않는다` 가 그대로 있다 [exact]
  측정: `m SK-05` 가 `numstat=1/1 item=1 both=1 g1=1 g2=1 keep=11 outside=0` (시작 판 `numstat= item=1 both=0 g1=1 g2=1 keep=11 outside=0`, good 은 기대값 그대로)
  양성 대조: bad2(파일 끝에 줄)에서 `numstat=3/1 … outside=2` (봉인 전 실측)
- [ ] SK-06: 규약 §4 가 같은 예외를 적어 design-mockup 과 어긋나지 않는다(PD2-2 · 같은 규칙의 다른 자리) — Given 구현 커밋 뒤, When `design-kit/references/visual-change-protocol.md` 의 `## 4. Design Approval Record` 절(다음 `## 5. ` 앞까지)을 읽으면, Then `PRD 도 작업 계약도 없으면` · `폐기 칸 한 곳` · `` 줄 끝에 `PRD 없음` `` 이 모두 든 줄이 1 줄이고, 옛 규칙 `이 기록에서 새로 정하지 않는다` · `파일 경로를 폐기 칸에 적는다` 가 각 1 줄 그대로이며, 이 파일의 차이가 더한 줄 1 · 지운 줄 0 이고 모두 그 절 안이다 [exact]
  측정: `m SK-06` 이 `numstat=1/0 new=1 keep=11 outside=0` (시작 판 `numstat= new=0 keep=11 outside=0`, good 은 기대값 그대로)
  양성 대조: bad2(파일 끝에 줄)에서 `numstat=3/0 … outside=2` (봉인 전 실측)

## Script

- [ ] SC-01: 계약도 PRD 도 없는 프로젝트의 새 모양 승인 기록을 기존 읽는 명령 셋이 그대로 찾는다(짝 조건 · 회귀) — Given 끝 판에서 떼어 낸 명령 셋: `/sprint` Step 0.5 bash 블록에서 `git worktree list` 가 든 줄부터 블록 끝까지(1 줄 이상이어야 한다 — 0 줄이면 실패), design-mockup Step 6 bash 블록의 확인 명령 `grep -cE '^- (확정 구성|폐기한 대안·이유):'`(파일 이름 자리를 시험 파일로), plan-prd Step 0 넷째 항목의 첫 검색과, 알려진 답 입력: 커밋 하나 · 빈 `.planning` · `.harness` · 승인 기록 `.design/approvals/20260927-home.md` 한 벌(`- 확정 구성:` 1 줄 · `- 폐기한 대안·이유:` 1 줄 · 그 아래 들여쓴 결정 2 줄 — 네 칸에 줄 끝 `PRD 없음` · `- 미확정/후속:` 1 줄), When 그 폴더에서 `/sprint` 줄을 bash 와 zsh 로 각각, 나머지 둘을 bash 로 돌리면, Then `/sprint` 줄은 두 셸 모두 출력 2 줄(모두 들여쓴 결정 줄) · `못 읽음:` 0 · 오류 출력 0 줄이고, 확인 명령은 `2`, plan-prd 검색은 2 줄이다 [exact]
  측정: `m SC-01` 이 `bash=out2/tag2/miss0/err0 zsh=out2/tag2/miss0/err0 check=2 prd=2` 이고 `lines` 1 이상 (시작 판 · good 모두 `lines=7` 에 기대값 그대로 — 읽는 명령은 이 묶음이 바꾸지 않으므로 시작 판에서도 성립한다. 이 조건은 새 글이 정한 줄 모양과 명령이 맞는지를 지키는 회귀 검사다)
  알려진 답: 손으로 세면 들여쓴 결정 2 줄이 두 검색에 걸리고, 폐기 칸 머리 줄 · 확정 구성 줄은 줄 끝이 `PRD 없음` 이 아니라 걸리지 않는다 — `/sprint` 2 줄 · 확인 명령 2 · plan-prd 2 줄. 봉인 전 good 실제값도 같고 종료 코드 0
  음성 대조: `/sprint` 두 grep 에서 `"$root/.design"` 을 빼면(bad) 두 셸 모두 `out0/tag0` — 승인 기록 줄을 못 모은다 (봉인 전 실측)

## Error

- [ ] ER-01: 이 묶음의 기록이 `/sprint` 재검증에 폐기 결정으로 잘못 잡히지 않는다 — Given 끝점 `TIP` 을 풀어 둔 트리, When 그 트리의 `.design` · `.harness` 에 `/sprint` Step 0.5 의 두 검색(`grep -rnE 'PRD 없음[[:space:]]*[|]?[[:space:]]*$'` · ``grep -rnE '^[[:space:]]*([-*+][[:space:]]|[0-9]+[.)][[:space:]]|[|]).*PRD 없음(`[.]?|[.])[[:space:]]*[|]?[[:space:]]*$'``)을 돌리면, Then 두 검색 모두 0 줄이다 — 이 계약 · notes · QA 리포트의 규칙 인용과 시험 입력이 폐기 결정 모양으로 끝나지 않는다 [exact]
  측정: `m ER-01` 이 `tail1=0 tail2=0` (시작 판 `tail1=0 tail2=0`)
  양성 대조: bad(notes 에 줄 끝이 `PRD 없음` 인 폐기 칸 모양 한 줄)에서 `tail1=1` (봉인 전 실측)

## Architecture

- [ ] AR-01: 바뀐 파일이 기대 집합 안이고 한 커밋에 맨 위 폴더 하나다 — Given 구현 · notes · QA 리포트 커밋이 모두 가지 `chore/ak2-pd2` 에 들어간 뒤, 시작점 `BASE=$(git -C W merge-base chore/ak2-pd chore/ak2-pd2)` 부터 끝점 `TIP=$(git -C W rev-parse --verify chore/ak2-pd2)` 까지(`HEAD` 를 쓰지 않는다. 해석이 안 되면 `UNRESOLVED` 로 멈춘다) `git diff --name-only` 로 모은 경로가 측정 도우미 `ALLOWED` 의 아홉 경로 안에만 있고(부분 집합 — 생성물이 없는 묶음이라 제외 pathspec 이 없다), 대상 다섯 `design-kit/skills/design-mockup/SKILL.md` · `design-kit/references/visual-change-protocol.md` · `harness/skills/sprint/SKILL.md` · `harness/skills/sprint-contract/SKILL.md` · `planning-kit/skills/plan-prd/SKILL.md` 가 각각 들어 있으며, 커밋마다 맨 위 폴더가 하나뿐이다(`design-kit` · `harness` · `planning-kit` · `.harness` 가운데 하나) [exact, collective]
  측정: `m AR-01` 이 `extra=0 req=11111 multi_top=0` (시작 판 `base=0dccce0 changed=0 extra=0 req=00000 multi_top=0`, good `changed=7 extra=0 req=11111 multi_top=0`)
  양성 대조: bad 에서 `extra=1 multi_top=1` 과 남는 경로 `scripts/x.sh` 출력 (봉인 전 실측)
- [ ] AR-02: 판단과 넘김을 notes 에 남긴다 — Given 끝점 `TIP`, notes 파일 `.harness/.meta/after-kaizen-0926b/pd2-notes.md` 가 커밋돼 있고 여섯 토큰 `PD2-1` · `PD2-2` · `visual-change-protocol.md` · `plan-prd` · `DC-15` · `tone-guide` 가 각 1 줄 이상이다. 담을 내용: 두 항목의 처리 결과와 커밋, 부모 지시 세 곳 밖에 더 고친 두 파일(규약 §4 · plan-prd Step 0)과 그 이유, 옛 글이 더 늘어난 문서 페이지(`docs/design-kit/design-mockup.html`)를 문서 사이트 묶음 DC-15 로 넘김, tone-guide 5 단계 대조 결과 [exact, enumerated]
  측정: `m AR-02` 가 `committed=1` 과 1 이상 여섯 (시작 판 `committed=0` 과 0 여섯, good `committed=1` 과 1 여섯)
- [ ] AR-03: 봉인 커밋이 계약 한 파일이고 구현보다 먼저이며 봉인 뒤 조건 · 측정 줄이 그대로다 — Given 끝점 `TIP`, When 시작점..끝점 구간에서 이 계약 파일을 처음 담은 커밋을 찾으면, Then 그 커밋의 파일이 1 개이고, `design-kit` · `harness` · `planning-kit` 을 처음 건드린 구현 커밋의 조상이며(같은 커밋이 아니다), 그 커밋 판 계약과 끝 판 계약의 조건 줄 지문 · 측정 줄 지문(체크 상태를 정규화한 sha256 앞 16 자리)이 각각 같고, 끝 판 계약의 `conditions_digest` · `measurement_digest` 가 그 지문과 같다(`SEAL_OK` · `MEASURE_OK`) [exact]
  측정: `m AR-03` 이 `seal_commit_files=1 seal_before_impl=1 seal_same_as_tip=1 measure_same_as_tip=1 this=SEAL_OK MEASURE_OK` (시작 판 `seal_commit_files=0 seal_before_impl=0 seal_same_as_tip=0 measure_same_as_tip=0 this=SEAL_ABSENT MEASURE_ABSENT`, good 은 기대값 그대로)
  양성 대조: bad(봉인 뒤 조건 문구 변조)에서 `seal_same_as_tip=0 this=SEAL_BROKEN` (봉인 전 실측)

## Anti-patterns

- [ ] AP-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수 (```text, ```bash, ```yaml 등). 판정 권위는 validate-plugin V6 상태기계다 — 여는/닫는 fence 가 동형이라 줄 단위 정규식으로는 판정 불가
  측정: 끝 판을 풀어 둔 `E` 에서 `m AP-03` 이 `v6_rc=0 fail=0` (시작 판 `v6_rc=0 fail=0`)
  양성 대조: bad(plan-prd 끝에 언어 없는 fence)에서 `v6_rc=2 fail=2` (봉인 전 실측)
- [ ] AP-04: SKILL.md / agents/*.md frontmatter 에서 name 필드 누락 — validate-plugin V1 FAIL
  측정: `m AP-04` 가 `v1_rc=0 fail=0` (시작 판 `v1_rc=0 fail=0`)
  양성 대조: bad(plan-prd `name:` 줄 삭제)에서 `v1_rc=2 fail=2` (봉인 전 실측)

## Reusability

- [ ] RE-01: N/A (산출물이 스킬 · 규약 문서 문장 몇 줄뿐이라 새 컴포넌트 · 함수 · 모듈이 없다. 측정: `m RE-01` 이 `added=0` — 구간이 `.harness/` 밖에 더한 새 파일 수. 시작 판 0. 양성 대조: bad 에서 `added=1`)
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다 — 계약도 없을 때의 기록에 새 형식 · 새 파일을 만들지 않고 plan-prd 비범위 표의 네 칸 이름과 승인 기록 폐기 칸을 그대로 쓴다: plan-prd 세 틀의 머리 줄 `| 하지 않는 것 | 이유 | 범위 | 코드에 남은 흔적 |` 3 줄이 그대로이고, 네 칸 이름 `하지 않는 것 · 이유 · 범위 · 코드에 남은 흔적` 이 design-mockup · sprint-contract · plan-prd 에 각 1 줄이다(새 문장은 「같은 네 칸」 으로 가리키고 이름을 다시 늘어놓지 않는다)
  측정: `m RE-02` 가 `hdr=3 cols=111` 이고 `m RE-01` 이 `added=0` (시작 판 `hdr=3 cols=111`, good 은 기대값 그대로)

## Diagnostics

- [ ] DG-01: N/A (`commands.analyze` 는 `bash -n scripts/release.sh` 라 `scripts/release.sh` 만 잰다 — 이번 바뀐 파일과 교집합 0 개. 측정: `m DG-01` 이 `release_sh=0`. 실제 검사는 DG-02 · DG-05)
- [ ] DG-02: IDE diagnostics 워닝/인포 0개 ([] 제외) — IDE(편집기) 진단을 명령줄로 같게 잰다: 바뀐 `.md`(계약 · QA 리포트 · 개정 파일 `.harness/sprint-*.md` 제외)의 더해진 줄에 걸린 markdownlint-cli2 0.23.2(MD013 끔, 편집기 확장과 같은 설정) 경고가 0 이다
  측정: `m DG-02` 가 `md_new=0` (시작 판 `md_new=0` — 바뀐 파일이 없다, good `md_new=0` 여섯 파일 각 0)
  양성 대조: bad(notes 에 `#bad heading`)에서 `md_new=2` (봉인 전 실측)
- [ ] DG-03: N/A (`commands.test` 는 `bash scripts/release.sh 2>&1 || true` 라 `scripts/release.sh` 만 잰다 — 교집합 0 개. 측정: `m DG-03` 이 `release_sh=0` — 도우미 안에서 `m DG-01` 을 그대로 부른다)
- [ ] DG-04: N/A (구동할 앱 · 서버가 없다 — 바뀐 파일이 모두 `.md` 라 실행 진입점 0 개. 측정: `m DG-04` 가 `non_md=0`. 양성 대조: bad 에서 `non_md=1`. 저장소 검사는 DG-05)
- [ ] DG-05: CI(자동 검사) 단계를 로컬에서 전부 돌려 통과한다 — Given 작업 폴더 W 가 끝점과 같다(`git -C W rev-parse HEAD` 가 `TIP` 이고, `git -C W status --porcelain --untracked-files=no` 가 빈 출력이거나 이 계약 파일 한 줄뿐이며 그때 그 파일의 차이가 `status:` 한 줄뿐 — 평가자가 APPROVE 때 바꾸는 줄이다), When `PYTHONDONTWRITEBYTECODE=1 TMPDIR=<임시 폴더> bash /Users/jackson/Hub/10_Dev/claude-plugins/.harness/handoff/2026-09-26-tools/ci-local.sh /Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak2-pd2` 를 돌리면, Then 요약 `$TMPDIR/ci-local/summary.txt` 에 `rc=0` 줄이 25 개이고 `rc=0` 이 아닌 줄은 `feedback-agg-test SKIP (yq 없음)` 하나뿐이다
  측정: `grep -c 'rc=0' "$TMPDIR/ci-local/summary.txt"` 가 25 · `grep -v 'rc=0' "$TMPDIR/ci-local/summary.txt"` 가 그 한 줄. 전제의 `status:` 한 줄 확인은 `git -C W diff -U0 -- .harness/sprint-contract-after-0926-prd-none-followups.md | grep -E '^[-+][^-+]' | grep -vc '^[-+]status:'` 가 0 (시작 판 봉인 전 실측: 25 · SKIP 한 줄)
  도구 지문: 돌리기 전에 `shasum -a 256 <ci-local.sh> | cut -c1-16` 이 `59fe55125c0dbc77` 인지 본다 — 추적 안 된 도구라 다르거나 없으면 이 조건은 다시 잴 수 없다(대체 수단 없음, 평가자가 그 사실을 적는다)
  음성 대조: 이 묶음이 깨뜨릴 수 있는 단계는 `validate-plugin` 이다 — bad 에서 같은 검사가 `v1_rc=2` · `v6_rc=2` (AP-03 · AP-04, 봉인 전 실측)

## 리서치 소스

- 저장소 안만 읽었다(웹 조회 · 외부 문서 가져오기 없음): pd notes · 결정 파일 · 남은 일 목록(위 배경의 경로, 읽기만), 앞 계약 `.harness/sprint-contract-after-0926-prd-none-rules.md`(형식 · 측정 도우미 틀)
- 계약 형식 원본: 이 가지의 `harness/skills/sprint-contract/SKILL.md` · `harness/references/contract-schema.md` §계약 봉인 · §측정 줄 봉인
