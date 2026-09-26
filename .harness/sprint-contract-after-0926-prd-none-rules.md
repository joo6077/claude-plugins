---
feature: "PRD 없음 · 폐기 결정 규칙 남은 일 (PD-1 ~ PD-4)"
slug: after-0926-prd-none-rules
created: "2026-09-26 20:43"
complexity: "복잡"
conditions: 21
status: active
owner_session: bda55d45-296c-491f-89ba-b52042d58e72
conditions_digest: sha256:eb11e128b3bbbc6f
measurement_digest: sha256:29dc81f0f9c7f6c4
locked_at: "2026-09-26 21:03"
---

## 배경

2026-09-24 카이젠 뒤 남은 일 목록의 「## pd」 절 네 항목(PD-1 ~ PD-4)을 한 계약으로 묶는다. 모두 앞 묶음 c4d(계약
`.harness/sprint-contract-after-0924-discard-decisions.md`, APPROVE)가 「폐기 결정 원문 자리는 기능 PRD 비범위 표 하나」 를 넣은 뒤
독립 검토가 짚은 것(c4d-notes R1 · R2 · R3)과 c4d 가 넘긴 것(PRD 가 나중에 생겼을 때 옮기는 절차)이다.
입력은 읽기만 한다 — 남은 일 목록 `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0926b/.harness/.meta/after-kaizen-0926b/leftovers.md` 의 `:85-92`,
사용자 결정 `.../after-kaizen-0926b/decisions.md` 의 PD-1 행, 넘김 기록 `.../after-kaizen-0926/c4d-notes.md` 「다음 사이클 메모」 R1 ~ R3 · 「넘긴 것과 사유」.

- 사용자 결정(PD-1): PRD 가 없을 때 결정 원문은 계약 「범위 경계」 한 곳에만 두고 승인 기록에는 경로만 적는다. 대체 규칙을 쓰는 조건은
  기능 단위(그 기능의 PRD 가 없을 때)로 맞춘다 — `decisions.md` PD-1 행. 근거는 사용자 「실행해」 와 `design-kit/references/visual-change-protocol.md:221-222`
  (「결정 원문이 두 곳에 있으면 한쪽만 고쳐진다」)에 맞춘 부모 해석이다.
- 사용자 합의(Step 5): 위임으로 받은 것으로 적는다 — 세션 `bda55d45-296c-491f-89ba-b52042d58e72` 의 사용자 말 2026-09-26T10:09:00.557Z
  「123다실행해 그러면끝나?다음카이젠에왜넘기는데?」 와 결정 답 2026-09-26T10:30:16.222Z. 그 앞의 위임 2026-09-24T04:04:16.964Z
  「나한테 물어보지 말고 자동으로 끝까지」. 조건을 느슨하게 하는 개정은 이 위임으로 동의 처리하지 않는다 — 그런 개정은 부모가 사용자에게 따로 묻는다.
- 작업 폴더 W = `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak2-pd`, 가지 `chore/ak2-pd`, 시작점 `6378948`(origin/main, #119).
- 커밋 규칙: `git add <경로>` 뒤 `git commit -o <경로>` · 한 커밋에 맨 위 폴더 하나(`design-kit` · `harness` · `planning-kit` · `.harness` 가운데 하나) ·
  `git add -A` · `git stash` · push · 가지 바꾸기 금지. 봉인 커밋(계약 한 파일)이 구현 커밋보다 먼저다.
- 같은 파일을 다른 묶음이 고칠 수 있다(`harness/skills/sprint-contract/SKILL.md` · `harness/skills/sprint/SKILL.md`). 이 계약은 sprint-contract 에서
  한 줄만 바꾸고(SK-02), sprint 는 `### Step 0.5:` 절 안만 바꾼다(SK-04 `outside=0`).
- 구현 전에 `tone-kit:tone-guide` 1 단계(규칙 불러오기)를, 완료 선언 전에 5 단계(전수 대조)를 한다 — 대조 결과는 notes 에 남긴다(AR-02).
- 사용자가 할 일: 없음.

복잡도 4 축 — 넷 다 「예」 이고 공개 약속 변경과 소비자가 함께 있어 「복잡」 이다. Step 2.5 짝 조건: 쓰는 쪽(원문 자리를 정하는 글)은
SK-01(design-mockup) · SK-02(sprint-contract) · SK-03(`/sprint` 산문), 읽는 쪽(모으는 명령)은 SK-04 · SC-01 · SC-02 · ER-01(`/sprint` 재검증) ·
SK-05(plan-prd Step 0), 두 쪽이 같은 모양을 쓰는지는 SK-06 이 잰다.

| 축 | 물음 | 값 |
| -- | ---- | -- |
| 레이어 수 | 몇 개 계층을 관통하는가 | 셋 — 킷 스킬 문서(design-kit · harness · planning-kit), 스킬 문서 안의 셸 명령(`/sprint` Step 0.5), 작업 기록(`.harness/`) |
| 공개 API·계약 변경 | 밖에 드러난 약속이 바뀌는가 | 예 — PRD 가 없을 때 폐기 결정을 적는 자리(승인 기록 → 계약 `범위 경계`), 그 줄의 모양(줄 끝 `PRD 없음`), `/sprint` 재검증이 내는 줄(`못 읽음:` 새로) |
| 소비면 존재 | 반대편이 있는가 | 예 — `/sprint` Step 0.5 명령 · plan-prd Step 0(새로 읽는 쪽) · design-mockup Step 2(승인 기록을 읽는다) · 사용자 프로젝트의 옛 승인 기록 · 계약 |
| 회귀 위험 | 기존 동작이 깨질 수 있는가 | 예 — 승인 기록 확인 명령 `→ 2`, `/sprint` 재검증 기존 세 명령 · 세 보고 줄, 다른 묶음이 곧 고칠 sprint-contract · sprint |

설정 값 대조 (`.harness/project.yaml` 을 글자 그대로 옮김):

| config key | project.yaml 에서 읽은 값 | 계약에 쓴 값 |
| ---------- | ------------------------- | ------------ |
| `commands.analyze` | `bash -n scripts/release.sh` | DG-01 N/A — 재는 파일이 바뀐 파일에 없다 |
| `commands.test` | `bash scripts/release.sh 2>&1 \|\| true` | DG-03 N/A — 같은 이유 |
| `diagnostics.ide_exclude` | `[]` | DG-02 의 `([] 제외)` |
| `contract_categories[].id` / `prefix` | Skill/SK · Script/SC · Error/ER · Architecture/AR | 같은 넷 |
| `anti_patterns[].id` / `message` | AP-01 버전 하드코딩 · AP-02 force push · AP-03 bare code fence · AP-04 frontmatter name 누락 | AP-03 · AP-04 (바뀌는 파일이 코드 블록 있는 SKILL.md 넷이다). AP-01 은 plugin.json 버전을 건드리지 않아서, AP-02 는 이 계약이 push 하지 않아서 뺐다 |

## GAP 분석 (Pre-Edit Audit)

대상 파일을 읽기만 하고 줄을 적었다. 줄 번호는 시작점 `6378948` 기준이다.

| 대상 파일 | 실제 Read 증거 (`파일:라인`) | 발견한 기존 갭·위반 | 계약 조건화 여부 |
| --------- | ---------------------------- | ------------------- | ---------------- |
| `design-kit/skills/design-mockup/SKILL.md` | `:147` `## Step 6:` · `:152-164` 승인 기록 틀 · `:161` 폐기 칸(PRD 가 있을 때 경로와 「하지 않는 것」 만) · `:166` PRD 없을 때 문단 · `:168-174` 확인 명령(`→ 2`) | `:166` 이 (a) 조건을 프로젝트 단위(`.planning/prd-*.md` 가 0 개)로 잡아 다른 기능 PRD 만 있는 프로젝트가 어느 쪽에도 안 걸리고 (b) 결정 원문(네 칸, 이유 포함)을 승인 기록 폐기 칸에 적게 한다 — 계약 `범위 경계` 에도 적으므로 원문이 두 곳(c4d R3) | SK-01 |
| 같은 파일 Step 2 | `:59-60` 감지 대상(승인 기록 · PRD) · `:66-68` 두 규칙 | 승인 기록 폐기 칸에 「하지 않는 것」 이 남으면 `:66` 규칙이 그대로 막는다. 계약에만 있는 결정은 Step 2 가 읽지 않는다(원래부터 그렇다) | 범위 경계 (그대로) |
| `harness/skills/sprint-contract/SKILL.md` | `:626-639` 포맷 규칙 · `:635` 폐기 결정 줄(둘째 문장 「PRD 가 없으면 … 네 칸 … `PRD 없음`」) | 대체 조건이 「PRD 가 없으면」 이라 단위가 흐리고, 여기가 원문 한 곳이라는 말 · 승인 기록이 이 경로를 가리킨다는 말이 없다 | SK-02 |
| `harness/skills/sprint/SKILL.md` Step 0.5 | `:56` 절 머리 · `:60-66` bash 블록(`:64` find · `:65` `grep -rn 'PRD 없음' .design .harness`) · `:70-76` text 블록(`:74` 폐기한 결정 줄) · `:78` 원문 자리 문단 · `:42-51` Step 0 워크트리 권고 | (R1) `:42-51` 이 새 워크트리를 권하는데, 추적 안 된 `.planning` · `.harness` 는 새 워크트리에 없고 `2>/dev/null` 이 오류를 버려 「기록 없음」 과 「못 봄」 이 같은 빈 출력 (R2) `:65` 가 흔한 말 `PRD 없음` 을 그대로 찾아 규칙 설명 · QA 리포트까지 잡힌다 — 이 폴더에서 37 줄, 줄 끝 모양으로 좁히면 0 줄(봉인 전 실측, 본 체크아웃도 37 · 0) (R3) `:78` 이 「승인 기록 · 계약 `범위 경계` 에 네 칸」 — 원문 두 곳 | SK-03 · SK-04 · SC-01 · SC-02 · ER-01 |
| `planning-kit/skills/plan-prd/SKILL.md` | `:28` Gotcha 14(원문 자리 · 「PRD 를 쓴 뒤에 나온 폐기 결정도 … 이 표에 한 줄 더한다」) · `:32-40` Step 0(읽을 것 셋) · `:87-90` 비범위 표 틀 · `:152` 저장 경로 `.planning/prd-<slug>.md` | PRD 를 쓰기 전에 계약에 `PRD 없음` 으로 적어 둔 결정을 PRD 로 옮기는 걸음이 없다 — 옮기지 않으면 PRD 가 생긴 뒤 원문이 두 곳(c4d 넘김 둘째) | SK-05 |
| `design-kit/references/visual-change-protocol.md` | `:206` 틀 폐기 칸 · `:218-222` 규칙(「그 결정이 적힌 파일 경로를 폐기 칸에 적는다 — 결정 원문이 두 곳에 있으면 한쪽만 고쳐진다」) | 이미 경로만 적게 한다 — 이 계약이 맞출 기준이다. 바꾸지 않는다 | SK-06 `vcp` (그대로인지) |
| `docs/design-kit/design-mockup.html` | `:635` 「PRD 가 없는 프로젝트」 note | 원본 `:166` 이 바뀌면 옛 글이 된다 — 문서 사이트는 이 계약 밖(DC-15 묶음) | 넘김 (AR-02 notes) |
| `.harness/` · `.design/` 옛 기록 | `grep -rn 'PRD 없음' .design .harness` 37 줄 — 모두 c4d 계약 · 피드백 · notes · docs-regen 계약의 규칙 설명 · 인용 | 실제 폐기 결정 줄은 0. 줄 끝 모양 검색도 0 | 범위 경계 (옮기지 않음) |

개선안 — 구현이 넣을 글. 조건은 아래 낱말(토큰)만 재므로 문장은 톤 대조에 맞춰 다듬어도 된다. 같은 글을 사본에 그대로 넣는 스크립트는
세션 스크래치 `pd/mock.py` 다(알려진 답 · 양성 대조에 썼다).

```text
[D1] design-mockup Step 6 — 옛 :166 한 줄을 바꾼다
그 기능의 PRD(`.planning/prd-<slug>.md`)가 없으면 결정 원문은 작업 계약 `범위 경계` 한 곳에 plan-prd 비범위 표와 같은 네 칸(하지 않는 것 · 이유 · 범위 · 코드에 남은 흔적)으로 적고 줄 끝에 `PRD 없음` 을 붙인다. 폐기 칸에는 그 계약 경로만 적는다 — 결정 원문이 두 곳에 있으면 한쪽만 고쳐진다 (`../../references/visual-change-protocol.md` §4). 다음 시안 전에는 그 경로에서 줄 끝이 `PRD 없음` 인 줄을 읽어 Step 2 의 폐기 항목으로 쓴다. 폐기 기록만 담으려고 PRD 를 만들지 않는다 (plan-prd Gotcha 1).

[C1] sprint-contract 포맷 규칙 :635 — 첫 문장은 그대로, 둘째 문장부터 바꾼다 (한 줄 바꾸기)
  - `범위 경계` 에 폐기한 결정(…)을 적을 때는 … 항목 이름만 적는다 (planning-kit plan-prd Gotcha 14). 그 기능의 PRD 가 없으면 결정 원문은 여기 한 곳이다 — plan-prd 와 같은 네 칸(하지 않는 것 · 이유 · 범위 · 코드에 남은 흔적)으로 적고 줄 끝에 `PRD 없음` 을 붙인다. 디자인 승인 기록 · 핸드오프는 이 계약 경로를 가리키고 결정을 다시 쓰지 않는다

[S1] /sprint Step 0.5 bash 블록 — 옛 :64-65 두 줄을 바꾼다 (앞 세 git 명령 뒤)
MAIN=$(git worktree list --porcelain | sed -n '1s/^worktree //p')   # 본 작업 폴더 — 추적 안 된 기록은 새 워크트리에 없다
for r in "$(git rev-parse --show-toplevel)" "$MAIN"; do
  for d in .planning .design .harness; do [ -r "$r/$d" ] || echo "못 읽음: $r/$d"; done
  find "$r/.planning" -maxdepth 1 -type f -name 'prd-*.md' 2>/dev/null               # 폐기한 결정 원문이 든 PRD
  grep -rnE 'PRD 없음[[:space:]]*[|]?[[:space:]]*$' "$r/.design" "$r/.harness" 2>/dev/null   # 줄 끝에 PRD 없음 을 붙인 폐기 결정
done | sort -u

[S2] /sprint Step 0.5 text 블록 — 옛 :74 한 줄을 바꾼다
- 폐기한 결정: <PRD 비범위 표 항목 · 줄 끝이 `PRD 없음` 인 줄 · `못 읽음` 폴더 — 모두 없으면 없음>

[S3] /sprint Step 0.5 :78 문단 — 「PRD 가 없는 프로젝트는 … 위 grep 으로 모은다.」 한 문장을 바꾼다. 앞 문장 · 뒤 문장은 그대로
그 기능의 PRD 가 없으면 원문은 계약 `범위 경계` 한 곳에 네 칸으로 적고 줄 끝에 `PRD 없음` 을 붙인다 — 승인 기록은 그 계약 경로를 가리킨다. 위 grep 은 줄 끝의 `PRD 없음`(표 행이면 뒤따르는 빈칸 · `|` 까지)만 찾으므로 규칙을 설명하는 문장처럼 뒤에 글이 이어지는 줄은 걸리지 않는다. 본 작업 폴더(`git worktree list` 첫 줄)도 함께 본다 — 추적하지 않는 `.planning` · `.harness` 는 새 워크트리에 따라오지 않아, 한 폴더만 보면 빈 출력이 「기록 없음」 인지 「못 봄」 인지 가를 수 없다.

[P1] plan-prd Step 0 — 「3. **선택 참조**」 줄 바로 뒤에 한 줄
4. **`PRD 없음` 기록**: PRD 가 없을 때 계약 `범위 경계` 에 적어 둔 이 기능의 폐기 결정이다. `grep -rnE 'PRD 없음[[:space:]]*[|]?[[:space:]]*$' .harness .design 2>/dev/null` 로 찾는다(harness `/sprint` Step 0.5 와 같은 모양). 이 기능의 줄이 있으면 Step 3 에서 `## Non-goals (폐기한 결정 포함)` 표(Shape Up `## No-gos`)에 네 칸 그대로 한 줄씩 옮기고, 원래 줄 끝의 `PRD 없음` 을 `→ .planning/prd-<slug>.md` 로 바꾼다 — 원문은 PRD 표 하나로 남는다 (Gotcha 14). 다른 기능의 줄은 옮기지 않는다.
```

## 범위 경계

항목별 처리 — 입력은 남은 일 목록 「## pd」 절 네 행이다. 바깥 문서가 있어야 판단되는 항목은 없다.

| 항목 | 처리 | 조건 · 사유 |
| --- | --- | --- |
| PD-1 원문 자리 한 곳 · 기능 단위 조건 (c4d R3) | 계약에 넣음 | SK-01 · SK-02 · SK-03 · SK-06. 결정 파일 PD-1 행대로 — 원문은 계약 `범위 경계` 한 곳, 승인 기록 · 핸드오프는 그 계약 경로를 가리킨다, 대체 조건은 「그 기능의 PRD 가 없으면」 |
| PD-2 새 워크트리에서 빈 출력 두 뜻 (c4d R1) | 계약에 넣음 | SK-04 · SC-01 · SC-02 · ER-01. 남은 일 비고의 두 길을 다 쓴다 — 본 작업 폴더(`git worktree list --porcelain` 첫 줄)도 보고, 없거나 못 읽는 폴더는 `못 읽음: <경로>` 한 줄로 말한다. 그래서 빈 프로젝트의 출력이 c4d 때의 0 줄에서 `못 읽음:` 세 줄로 바뀐다(ER-01) — 의도한 변화다 |
| PD-3 흔한 말이라 설명 글까지 걸림 (c4d R2) | 계약에 넣음 | SK-04 `pat` · `broad` · SC-01 `rule`. 찾는 모양을 「줄 끝이 `PRD 없음`(표 행이면 뒤에 칸 구분 `\|` 하나 — 앞뒤 빈칸 수는 가리지 않는다)」 으로 좁힌다. 쓰는 쪽 셋(SK-01 · SK-02 · SK-03)도 「줄 끝에」 로 맞춘다(SK-06). 시험 폴더에 규칙 설명 문장 · QA 인용 한 줄씩을 넣는다(측정 도우미 `fixture`) |
| PD-4 PRD 가 나중에 생겼을 때 옮기기 (c4d 넘김 둘째) | 계약에 넣음 | SK-05. plan-prd Step 0 에 읽을 것 넷째로 더한다 — 옮기는 일은 Step 3(작성)에서 하고, 옮긴 줄 끝의 `PRD 없음` 을 PRD 경로로 바꿔 다음 검색에 다시 걸리지 않게 한다 |
| 승인 기록 폐기 칸은 경로만 (교차 진단 반영) | 계약에 넣음 | SK-01 `ptr` · `follow`. 결정 파일 PD-1 행의 「승인 기록에는 경로만」 을 글자 그대로 따른다 — 처음 초안은 PRD 가 있을 때의 `:161` 처럼 「하지 않는 것」 이름도 남기게 했으나, 교차 진단이 결정 원문보다 넓다고 짚었고 사용자에게 물을 수 없어 결정 원문 쪽을 골랐다. 규약 `visual-change-protocol.md:221-222` 도 「그 결정이 적힌 파일 경로」 만 적게 한다. 이름표가 없으면 Step 2 규칙 `:66` 이 항목을 모르므로 같은 문장에 「다음 시안 전에 그 경로에서 줄 끝이 `PRD 없음` 인 줄을 읽는다」 를 넣어 폐기 항목이 되살아나지 않게 한다(F20). PRD 가 있을 때의 `:161` 은 이 결정 밖이라 그대로 둔다 |
| 작업 계약이 아직 없을 때(design-kit 만 쓰는 프로젝트) | 바꾸지 않음 · notes 에 남김 | 결정이 이 경우를 정하지 않았다. 규약 `visual-change-protocol.md:221-222` 가 제품 요구 수준의 폐기 결정은 승인 기록에서 새로 정하지 않는다고 하므로 새 규칙을 지어 넣지 않는다. notes 에 「계약이 아직 없」 는 경우로 적는다(AR-02) |
| design-mockup Step 2 가 계약 `범위 경계` 를 읽기 | 바꾸지 않음 · notes 에 남김 | 계약에만 있고 승인 기록에 없는 결정은 원래부터 Step 2 가 못 읽는다(이 계약이 만든 빈틈이 아니다). 넣으면 design-kit 이 harness 계약 경로를 알아야 해 PD-1 밖이다. notes 에 적는다(AR-02 `Step 2`) |
| `design-kit/references/visual-change-protocol.md` | 바꾸지 않음 | 이미 「결정이 적힌 파일 경로」 만 적게 한다 — 이 계약이 맞출 기준이다(SK-06 `vcp`) |
| plan-prd 가 본 작업 폴더까지 보기 | 바꾸지 않음 | `/sprint` 재검증은 새 워크트리에서 도는 것이 권고라(`sprint:42-51`) 두 폴더를 본다. plan-prd 는 기획 산출물 `.planning/` 이 있는 폴더에서 돈다 — 최소 변경으로 같은 검색 모양만 맞춘다 |
| 이미 있는 `PRD 없음` 줄 옮기기 | 없음 | 이 레포 `.design` · `.harness` 에서 줄 끝 모양 검색 0 줄(봉인 전 실측, 본 체크아웃 · W 둘 다). 옛 37 줄은 규칙 설명 · 인용이다 |
| `docs/design-kit/design-mockup.html:635` | 범위 밖 · 넘김 | 과제가 정한 범위 밖(docs HTML). 원본이 바뀌어 옛 글이 되므로 notes 에 적어 문서 사이트 묶음(DC-15)으로 넘긴다(AR-02) |
| 남은 일 목록의 다른 절 · 킷 `plugin.json` 버전 · `scripts/` · `.github/` | 범위 밖 | 과제가 정한 범위 밖. 버전은 릴리스 단계 몫 |
| 표 칸 빈칸 변형(`PRD 없음|` · `PRD 없음  |`) | 계약에 넣음 (교차 진단 반영) | SK-04 · SK-05 · SK-06 의 검색 모양을 `PRD 없음[[:space:]]*[|]?[[:space:]]*$` 로 넓혔다 — 처음 모양 `PRD 없음( [|])?[[:space:]]*$` 는 칸 앞 빈칸이 없거나 둘 이상이면 놓친다(교차 진단이 `grep -E` 로 확인). 시험 입력에 두 변형을 한 줄씩 더해 SC-01 · SC-02 가 잰다. 처음 모양으로 되돌린 bad4 에서 SC-01 `tag2`(기대 4) |
| plan-prd Step 3(작성)에 옮기는 걸음을 따로 적기 | 바꾸지 않음 (교차 진단 반영 · 의도) | Step 0 은 「무엇을 읽을지」 를 모으는 자리이고, 넷째 항목이 「Step 3 에서 옮긴다」 를 적어 Step 3 을 가리킨다. Step 3 에 같은 절차를 또 적으면 규칙 원문이 두 곳이 된다 — 이 묶음이 없애려는 모양과 같다. 최소 변경으로 한 줄만 더한다(SK-05 `numstat=1/0`) |
| DG-05 가 쓰는 `ci-local.sh` 가 추적 안 된 도구 | 한계를 적음 (교차 진단 반영) | 본 체크아웃 `.harness/handoff/2026-09-26-tools/ci-local.sh`(추적 안 됨) 이고 이 묶음의 허용 경로 밖이라 커밋하지 않는다. 봉인 시점 지문 `shasum -a 256` 앞 16 자리 `59fe55125c0dbc77` 을 DG-05 측정 줄에 적었다 — 평가 때 지문이 다르거나 파일이 없으면 DG-05 는 다시 잴 수 없다(대체 수단 없음, 평가자가 그 사실을 적는다) |
| 절 경계 검사 `outside` 의 나쁜 예 | 계약에 넣음 (교차 진단 반영) | bad4 = good + design-mockup · `/sprint` · sprint-contract 파일 끝(절 밖)에 빈 줄과 한 줄씩. SK-01 `outside=2` · SK-04 `outside=2` · SK-02 `numstat=3/1` 로 잡힌다(봉인 전 실측) |

커버리지 해소 — Step 6.5 (4) 검출기가 낸 `UNCOVERED` 의 처리:

- 커버리지 해소: AR-02 — notes 경로는 측정 도우미 `NOTES` 변수가, 아홉 토큰은 `m AR-02` 의 목록이 센다(산문과 같은 글자). 목록을 두 번 적지 않으려고 측정 줄에 다시 늘어놓지 않았다
- 커버리지 해소: SK-06 — 다섯 파일은 측정 도우미 변수 `DM` · `SP` · `SC` · `PRD` · `VCP` 한 곳에 적혀 있고 `m SK-06` 이 그 변수로 잰다(산문과 같은 경로). `/sprint` 는 경로가 아니라 스킬 이름이다
- 커버리지 해소: AR-01 — 경로 기대 집합은 측정 도우미 `ALLOWED` 한 곳에만 적는다. 산문의 대상 넷은 `m AR-01` 의 `req` 네 자리가 센다

## 회귀 게이트 — 측정 도우미

평가 때 이 블록을 떼어 bash 에서 불러 쓴다. `TMPDIR` 은 평가자 임시 폴더로 준다. 도우미는 끝점을 `git archive` 로 풀어 재므로 작업 폴더의 미커밋
변경을 보지 않는다. 작업 폴더 밖 입력은 지우지 마라 — 도우미가 만든 `$T` 아래만 치워도 된다. `MDL` 이 가리키는 markdownlint 설치본이 없으면
`mdl_ready` 가 그 자리에 설치한다(npm).

```bash
# 떼기: awk '/^# === 측정 도우미 시작/{f=1} f{print} /^# === 측정 도우미 끝/{exit}' <계약> > "$TMPDIR/pd-measure.sh"
# 부르기: bash -c 'source "$TMPDIR/pd-measure.sh" || exit 2; type m >/dev/null || exit 2; m SK-01'
# 시작 판: E_REF=BASE 를 주고 부른다. 다른 사본을 재려면 W=<사본> 을 준다
# === 측정 도우미 시작 (after-0926-prd-none-rules) ===
# 쓰는 법: 이 블록을 파일로 떼어 bash 에서 source 한 뒤 `m <조건 ID>`. zsh 에서 source 하지 마라(도우미 안에서 zsh 를 따로 부른다).
# 잴 트리 E — 기본은 가지 끝(TIP)을 git archive 로 푼 임시 폴더. 시작 판을 재려면 E_REF=BASE. 다른 사본을 재려면 W=<사본>.
W=${W:-/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak2-pd}
BR=${BR:-chore/ak2-pd}
BASE=$(git -C "$W" merge-base origin/main "$BR") || { echo "UNRESOLVED BASE"; return 2 2>/dev/null || exit 2; }
TIP=$(git -C "$W" rev-parse --verify "$BR") || { echo "UNRESOLVED TIP"; return 2 2>/dev/null || exit 2; }
T=$(mktemp -d "${TMPDIR:-/tmp}/pd.XXXXXX")
snap() { mkdir -p "$2" && git -C "$W" archive "$1" | tar -x -C "$2"; }
case "${E_REF:-TIP}" in
  BASE) E=$T/base; snap "$BASE" "$E" ;;
  *)    E=$T/tip;  snap "$TIP" "$E" ;;
esac
DM=design-kit/skills/design-mockup/SKILL.md
SP=harness/skills/sprint/SKILL.md
SC=harness/skills/sprint-contract/SKILL.md
PRD=planning-kit/skills/plan-prd/SKILL.md
VCP=design-kit/references/visual-change-protocol.md
CF=.harness/sprint-contract-after-0926-prd-none-rules.md
NOTES=.harness/.meta/after-kaizen-0926b/pd-notes.md
COLS='하지 않는 것 · 이유 · 범위 · 코드에 남은 흔적'
PAT='PRD 없음[[:space:]]*[|]?[[:space:]]*$'
ALLOWED='design-kit/skills/design-mockup/SKILL.md
harness/skills/sprint/SKILL.md
harness/skills/sprint-contract/SKILL.md
planning-kit/skills/plan-prd/SKILL.md
.harness/sprint-contract-after-0926-prd-none-rules.md
.harness/sprint-feedback-after-0926-prd-none-rules.md
.harness/sprint-amendments-after-0926-prd-none-rules.md
.harness/.meta/after-kaizen-0926b/pd-notes.md'
sec() { awk -v s="$1" -v e="$2" 'index($0,s)==1{f=1;print;next} f&&index($0,e)==1{exit} f' "$3"; }   # s 로 시작하는 줄부터 e 로 시작하는 다음 줄 앞까지
n() { grep -cF -- "$1" || true; }                                                                    # 표준 입력에서 글자 그대로 든 줄 수
nocode() { awk '/^[[:space:]]*```/{c=!c;next} !c'; }
blk() { awk -v t="$1" 'index($0,"```" t)==1{b=1;next} b&&/^```/{b=0} b'; }                           # 언어가 t 인 코드 블록 안 줄만
secrange() { awk -v s="$1" -v e="$2" 'index($0,s)==1{a=NR} a&&!z&&NR>a&&index($0,e)==1{z=NR} END{print a+0, z+0}' "$3"; }   # 절 시작 줄 · 다음 절 줄
numstat() { git -C "$W" diff --numstat "$BASE" "$TIP" -- "$1" | awk '{print $1"/"$2}'; }
added() { git -C "$W" diff -U0 "$BASE" "$TIP" -- "$1" | grep -E '^\+[^+]' | sed 's/^+//'; }
hunks() {  # hunks <파일> — 지운 줄 번호(BASE)는 "-N", 더한 줄 번호(TIP)는 "+N"
  git -C "$W" diff -U0 "$BASE" "$TIP" -- "$1" | awk '/^@@/{split($2,a,",");s=substr(a[1],2);c=(a[2]=="")?1:a[2];for(i=0;i<c;i++)print "-"(s+i);split($3,b,",");s=substr(b[1],2);c=(b[2]=="")?1:b[2];for(i=0;i<c;i++)print "+"(s+i)}'
}
outside() {  # outside <파일> <절 시작> <다음 절> — 절 밖에서 바뀐 줄 수 (BASE · TIP 각자의 절 범위로)
  git -C "$W" show "$BASE:$1" > "$T/o.md"
  read -r bs be <<EOF
$(secrange "$2" "$3" "$T/o.md")
EOF
  read -r ts te <<EOF
$(secrange "$2" "$3" "$E/$1")
EOF
  hunks "$1" | awk -v bs="$bs" -v be="$be" -v ts="$ts" -v te="$te" '/^-/{x=substr($0,2)+0; if(x<=bs||x>=be)o++} /^\+/{x=substr($0,2)+0; if(x<=ts||x>=te)o++} END{print o+0}'
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
lines_sh() {  # /sprint Step 0.5 bash 블록에서 `git worktree list` 가 든 줄부터 블록 끝까지 떼어 파일로
  sec '### Step 0.5:' '### Step 1:' "$E/$SP" | blk bash | awk '/git worktree list/{f=1} f' > "$T/lines.sh"
}
fixture() {  # 알려진 답 입력 — m: 본 폴더(추적 안 된 기록 넷) · wt: m 의 새 워크트리 · empty: 기록 없는 빈 레포
  M=$T/m; mkdir -p "$M/.planning" "$M/.design/approvals" "$M/.harness"
  git -C "$M" init -q && git -C "$M" -c user.name=t -c user.email=t@t commit -q --allow-empty -m init
  printf '## Non-goals (폐기한 결정 포함)\n' > "$M/.planning/prd-alarm.md"
  printf 'x\n' > "$M/.planning/discover-alarm.md"
  printf '%s\n' '| 시간대 설정 | 쓰지 않는다고 함 | 제품 전체 | 없음 | PRD 없음 |' '| 언어 설정 | 한 언어만 쓴다 | 이번 PRD | 없음 | PRD 없음|' '| 국가 목록 | 한 나라만 쓴다 | 이번 사이클 | 없음 | PRD 없음  |' \
    '그 기능의 PRD 가 없으면 줄 끝에 `PRD 없음` 을 붙인다.' '- 근거: `PRD 없음` 1 줄 확인' > "$M/.harness/sprint-contract-x.md"
  printf '%s\n' '- 폐기한 대안·이유: 국가 설정 · 한 나라만 쓴다고 함 · 이번 PRD · 없음 · PRD 없음' > "$M/.design/approvals/20260926-home.md"
  git -C "$M" worktree add -q -b x "$T/wt" 2>/dev/null
  EM=$T/empty; mkdir -p "$EM"; git -C "$EM" init -q && git -C "$EM" -c user.name=t -c user.email=t@t commit -q --allow-empty -m init
}
runs() {  # runs <폴더> — bash · zsh 로 떼어 낸 줄을 돌려 줄 수를 센다
  r=""; for sh in bash zsh; do
    (cd "$1" && "$sh" "$T/lines.sh" >"$T/o" 2>"$T/e")
    r="$r $sh=out$(grep -c . "$T/o" || true)/prd$(grep -c 'prd-alarm\.md$' "$T/o" || true)/tag$(grep -c 'PRD 없음' "$T/o" || true)/rule$(grep -cE '붙인다|근거:' "$T/o" || true)/miss$(grep -c '^못 읽음: ' "$T/o" || true)/err$(grep -c . "$T/e" || true)"
  done; printf '%s' "${r# }"
}

m() {
  case "$1" in
  SK-01) s6=$(sec '## Step 6:' '## Step 7:' "$E/$DM"); p=$(printf '%s\n' "$s6" | nocode | grep -F 'PRD 없음')
    old="$(n '`.planning/prd-*.md` 가 0 개' <"$E/$DM")$(n '폐기 칸에 plan-prd 비범위 표와 같은 네 칸' <"$E/$DM")"
    echo "numstat=$(numstat "$DM") prose=$(printf '%s\n' "$p" | grep -c . || true) feat=$(printf '%s\n' "$p" | n '그 기능의 PRD') scope=$(printf '%s\n' "$p" | n '`범위 경계` 한 곳') tail=$(printf '%s\n' "$p" | n '줄 끝에 `PRD 없음`') ptr=$(printf '%s\n' "$p" | n '폐기 칸에는 그 계약 경로만 적는다') follow=$(printf '%s\n' "$p" | n '줄 끝이 `PRD 없음` 인 줄을 읽어') cols=$(printf '%s\n' "$p" | n "$COLS") nocreate=$(printf '%s\n' "$p" | n 'PRD 를 만들지 않는다') vcp=$(printf '%s\n' "$p" | n 'visual-change-protocol.md') old=$old d1=$(printf '%s\n' "$s6" | n '그 기능 PRD 비범위 표 경로와 그 줄의 「하지 않는 것」 만 적는다') check=$(printf '%s\n' "$s6" | n "grep -cE '^- (확정 구성|폐기한 대안·이유):'") outside=$(outside "$DM" '## Step 6:' '## Step 7:')" ;;
  SK-02) add=$(added "$SC"); fmt=$(awk '/^\*\*포맷 규칙/{f=1;next} f&&/^### 6\.2\./{exit} f' "$E/$SC")
    i=0; [ -n "$add" ] && i=$(printf '%s\n' "$fmt" | grep -cxF -- "$add" || true)
    echo "numstat=$(numstat "$SC") in_fmt=$i first=$(printf '%s\n' "$add" | n '그 기능 PRD 비범위 표 경로와 항목 이름만 적는다 (planning-kit plan-prd Gotcha 14).') feat=$(printf '%s\n' "$add" | n '그 기능의 PRD 가 없으면') here=$(printf '%s\n' "$add" | n '결정 원문은 여기 한 곳이다') tail=$(printf '%s\n' "$add" | n '줄 끝에 `PRD 없음`') cols=$(printf '%s\n' "$add" | n "$COLS") ptr=$(printf '%s\n' "$add" | n '이 계약 경로를 가리키고') old=$(n 'PRD 가 없으면 plan-prd 와 같은 네 칸' <"$E/$SC") argsub=$(printf '%s\n' "$add" | grep -cE '(^|[^\\])[$][0-9]' || true)" ;;
  SK-03) s=$(sec '### Step 0.5:' '### Step 1:' "$E/$SP"); pr=$(printf '%s\n' "$s" | nocode)
    echo "src=$(printf '%s\n' "$pr" | grep -F '## Non-goals (폐기한 결정 포함)' | grep -F '## No-gos' | n 'plan-prd Gotcha 14') feat=$(printf '%s\n' "$pr" | n '그 기능의 PRD 가 없으면') scope=$(printf '%s\n' "$pr" | n '`범위 경계` 한 곳') tail=$(printf '%s\n' "$pr" | n '줄 끝에 `PRD 없음`') ptr=$(printf '%s\n' "$pr" | n '그 계약 경로를 가리킨다') wt=$(printf '%s\n' "$pr" | n '`git worktree list` 첫 줄') why=$(printf '%s\n' "$pr" | n '새 워크트리에 따라오지 않아') narrow=$(printf '%s\n' "$pr" | n '뒤에 글이 이어지는 줄은 걸리지 않는다') old=$(printf '%s\n' "$pr" | n '승인 기록 · 계약 `범위 경계` 에 네 칸으로') keep_out=$(printf '%s\n' "$pr" | n '다시 넣지 않는다')" ;;
  SK-04) s=$(sec '### Step 0.5:' '### Step 1:' "$E/$SP"); tb=$(printf '%s\n' "$s" | blk text); bb=$(printf '%s\n' "$s" | blk bash)
    tl=$(printf '%s\n' "$tb" | grep '^- 폐기한 결정:')
    old=""; for k in '- 문서 주장 잔여:' '- git 실측:' '- 불일치:'; do old="$old$(printf '%s\n' "$tb" | n "$k")"; done
    for k in 'git log --oneline' 'git status --short' 'git diff --stat'; do old="$old$(printf '%s\n' "$bb" | n "$k")"; done
    order=$(printf '%s\n' "$bb" | awk '/git diff --stat/{d=NR} /git worktree list/{w=NR} END{print (d>0&&w>d)?1:0}')
    echo "tline=$(printf '%s\n' "$tl" | grep -c . || true) tl_tail=$(printf '%s\n' "$tl" | n '줄 끝이 `PRD 없음`') tl_miss=$(printf '%s\n' "$tl" | n '`못 읽음`') tl_none=$(printf '%s\n' "$tl" | n '모두 없으면 없음') wt=$(printf '%s\n' "$bb" | n 'git worktree list --porcelain') top=$(printf '%s\n' "$bb" | n 'git rev-parse --show-toplevel') miss=$(printf '%s\n' "$bb" | n '못 읽음:') find=$(printf '%s\n' "$bb" | n "-name 'prd-*.md'") pat=$(printf '%s\n' "$bb" | n "grep -rnE '$PAT'") broad=$(printf '%s\n' "$bb" | n "grep -rn 'PRD 없음'") sortu=$(printf '%s\n' "$bb" | n 'done | sort -u') order=$order old=$old outside=$(outside "$SP" '### Step 0.5:' '### Step 1:')" ;;
  SK-05) s0=$(sec '## Step 0:' '## Step 1:' "$E/$PRD"); it=$(printf '%s\n' "$s0" | grep -F '4. **`PRD 없음` 기록**'); add=$(added "$PRD")
    i=0; [ -n "$add" ] && i=$(printf '%s\n' "$s0" | grep -cxF -- "$add" || true)
    keep=""; for k in '1. **원칙 문서**:' '2. **이전 단계 산출물**:' '3. **선택 참조**:'; do keep="$keep$(printf '%s\n' "$s0" | n "$k")"; done
    echo "numstat=$(numstat "$PRD") in_s0=$i item=$(printf '%s\n' "$it" | grep -c . || true) pat=$(printf '%s\n' "$it" | n "grep -rnE '$PAT' .harness .design") table=$(printf '%s\n' "$it" | n '## Non-goals (폐기한 결정 포함)') nogos=$(printf '%s\n' "$it" | n '## No-gos') arrow=$(printf '%s\n' "$it" | n '`→ .planning/prd-<slug>.md`') gotcha=$(printf '%s\n' "$it" | n 'Gotcha 14') other=$(printf '%s\n' "$it" | n '다른 기능의 줄은 옮기지 않는다') keep=$keep" ;;
  SK-06) prod="$(n '줄 끝에 `PRD 없음`' <"$E/$DM")$(n '줄 끝에 `PRD 없음`' <"$E/$SC")$(sec '### Step 0.5:' '### Step 1:' "$E/$SP" | nocode | n '줄 끝에 `PRD 없음`')"
    cons="$(sec '### Step 0.5:' '### Step 1:' "$E/$SP" | blk bash | n "'$PAT'")$(sec '## Step 0:' '## Step 1:' "$E/$PRD" | n "'$PAT'")"
    broad=0; for f in "$DM" "$SP" "$SC" "$PRD"; do broad=$((broad + $(n "grep -rn 'PRD 없음'" <"$E/$f"))); done
    echo "prod=$prod cons=$cons broad=$broad vcp=$(n '제품 요구 수준의 폐기 결정(기능·설정 항목을 없앤다는 결정)은 이 기록에서 새로 정하지 않는다. 그 결정이 적힌' <"$E/$VCP")$(git -C "$W" diff --name-only "$BASE" "$TIP" -- "$VCP" | grep -c . || true)" ;;
  SC-01) lines_sh; fixture
    echo "lines=$(grep -c . "$T/lines.sh" || true) wt: $(runs "$T/wt")" ;;
  SC-02) lines_sh; fixture
    echo "lines=$(grep -c . "$T/lines.sh" || true) main: $(runs "$T/m")" ;;
  ER-01) lines_sh; fixture
    echo "lines=$(grep -c . "$T/lines.sh" || true) empty: $(runs "$T/empty")" ;;
  AR-01) ch=$(git -C "$W" diff --name-only "$BASE" "$TIP")
    extra=$(printf '%s\n' "$ch" | grep . | grep -vxF -f <(printf '%s\n' "$ALLOWED") | grep -c . || true)
    req=""; for f in "$DM" "$SP" "$SC" "$PRD"; do req="$req$(printf '%s\n' "$ch" | grep -cxF "$f" || true)"; done
    multi=0; for c in $(git -C "$W" rev-list "$BASE..$TIP"); do t=$(git -C "$W" show --name-only --format= "$c" | awk -F/ 'NF{print $1}' | sort -u | grep -c .); [ "$t" -gt 1 ] && multi=$((multi + 1)); done
    echo "base=${BASE:0:7} tip=${TIP:0:7} changed=$(printf '%s\n' "$ch" | grep -c . || true) extra=$extra req=$req multi_top=$multi"
    [ "$extra" = 0 ] || printf '%s\n' "$ch" | grep . | grep -vxF -f <(printf '%s\n' "$ALLOWED") ;;
  AR-02) b=$(git -C "$W" show "$TIP:$NOTES" 2>/dev/null); c=0; [ -n "$b" ] && c=1; out="committed=$c"
    for k in PD-1 PD-2 PD-3 PD-4 docs/design-kit/design-mockup.html DC-15 '계약이 아직 없' 'Step 2' tone-guide; do out="$out $(printf '%s\n' "$b" | n "$k")"; done
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
  RE-02) echo "hdr=$(n '| 하지 않는 것 | 이유 | 범위 | 코드에 남은 흔적 |' <"$E/$PRD") g14=$(n '디자인 승인 기록 · 작업 계약 · 핸드오프는 이 PRD 경로를 가리키고' <"$E/$PRD") cols=$(n "$COLS" <"$E/$DM")$(n "$COLS" <"$E/$SC")$(n "$COLS" <"$E/$PRD") newfmt=$(git -C "$W" diff -U0 "$BASE" "$TIP" -- "$PRD" | grep -E '^-[^-]' | grep -c . || true)" ;;
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

봉인 전 실측(2026-09-26). 「시작 판」 은 W 에서 가지 끝이 아직 시작점과 같을 때 잰 값이다. 「good」 은 W 를 복제한 임시 사본에 봉인 커밋(가짜 계약) →
`pd/mock.py` 개선안을 킷마다 커밋 → notes 커밋을 넣은 판(알려진 답), 「bad」 · 「bad3」 은 일부러 망가뜨린 판(양성 대조)이다 —
bad: good + `/sprint` 검색을 옛 `grep -rn 'PRD 없음'` 으로 되돌리고 `| sort -u` 를 뺌 · 한 커밋에 킷 셋(규약 `visual-change-protocol.md` 줄 더하기 ·
plan-prd `name:` 줄 삭제 · plan-prd 끝에 언어 없는 코드 블록) · 봉인 뒤 조건 문구 변조 · notes 에 `#bad heading`,
bad3: good + `scripts/x.sh` 새 파일 · `scripts/release.sh` 한 줄, bad4(교차 진단 반영 뒤 더함): good + `/sprint` · plan-prd 검색을 처음 좁힌 모양 `PRD 없음( [|])?[[:space:]]*$` 로 되돌림 · design-mockup · `/sprint` · sprint-contract 파일 끝에 빈 줄과 한 줄씩. 사본 만들기는 스크래치 `pd/build.sh`, 조건 전부 재기는 `pd/runall.sh`.

| 조건 | 시작 판 | good (알려진 답) | 양성 대조 |
| --- | --- | --- | --- |
| SK-01 | `numstat= prose=1 feat=0 scope=0 tail=0 ptr=0 follow=0 cols=1 nocreate=1 vcp=0 old=11 d1=1 check=1 outside=0` | `numstat=1/1 prose=1 feat=1 scope=1 tail=1 ptr=1 follow=1 cols=1 nocreate=1 vcp=1 old=00 d1=1 check=1 outside=0` | 시작 판이 실패 값 · bad4 `numstat=3/1 … outside=2` |
| SK-02 | `numstat= in_fmt=0 first=0 feat=0 here=0 tail=0 cols=0 ptr=0 old=1 argsub=0` | `numstat=1/1 in_fmt=1 first=1 feat=1 here=1 tail=1 cols=1 ptr=1 old=0 argsub=0` | 시작 판이 실패 값 · bad4 `numstat=3/1` |
| SK-03 | `src=1 feat=0 scope=0 tail=0 ptr=0 wt=0 why=0 narrow=0 old=1 keep_out=1` | `src=1 feat=1 scope=1 tail=1 ptr=1 wt=1 why=1 narrow=1 old=0 keep_out=1` | 시작 판이 실패 값 |
| SK-04 | `tline=1 tl_tail=0 tl_miss=0 tl_none=0 wt=0 top=0 miss=0 find=1 pat=0 broad=1 sortu=0 order=0 old=111111 outside=0` | `tline=1 tl_tail=1 tl_miss=1 tl_none=1 wt=1 top=1 miss=1 find=1 pat=1 broad=0 sortu=1 order=1 old=111111 outside=0` | bad `pat=0 broad=1 sortu=0` · bad4 `pat=0 broad=0 … outside=2` |
| SK-05 | `numstat= in_s0=0 item=0 pat=0 table=0 nogos=0 arrow=0 gotcha=0 other=0 keep=111` | `numstat=1/0 in_s0=1 item=1 pat=1 table=1 nogos=1 arrow=1 gotcha=1 other=1 keep=111` | bad `numstat=5/1` |
| SK-06 | `prod=000 cons=00 broad=1 vcp=10` | `prod=111 cons=11 broad=0 vcp=10` | bad `cons=01 broad=1 vcp=11` · bad4 `cons=00` |
| SC-01 | `lines=0 wt: bash=out0/prd0/tag0/rule0/miss0/err0 zsh=…` 같음 | `lines=6 wt: bash=out8/prd1/tag4/rule0/miss3/err0 zsh=out8/prd1/tag4/rule0/miss3/err0` | bad `out10/prd1/tag6/rule2/miss3/err0` · bad4 `out6/prd1/tag2/rule0/miss3/err0` (두 셸 같음) |
| SC-02 | `lines=0 main: bash=out0/… zsh=out0/…` | `lines=6 main: bash=out5/prd1/tag4/rule0/miss0/err0 zsh=out5/prd1/tag4/rule0/miss0/err0` | bad `out14/prd2/tag12/rule4/miss0/err0` · bad4 `out3/prd1/tag2/rule0/miss0/err0` (두 셸 같음) |
| ER-01 | `lines=0 empty: bash=out0/… zsh=out0/…` | `lines=6 empty: bash=out3/prd0/tag0/rule0/miss3/err0 zsh=out3/prd0/tag0/rule0/miss3/err0` | bad `out6/…/miss6` (두 셸 같음) |
| AR-01 | `base=6378948 tip=6378948 changed=0 extra=0 req=0000 multi_top=0` | `changed=6 extra=0 req=1111 multi_top=0` | bad `changed=7 extra=1 multi_top=1` + `design-kit/references/visual-change-protocol.md` 출력 · bad3 `extra=2` + `scripts/release.sh` · `scripts/x.sh` |
| AR-02 | `committed=0 0 0 0 0 0 0 0 0 0` | `committed=1 1 1 1 1 1 1 1 1 1` | 시작 판이 실패 값 |
| AR-03 | `seal_commit_files=0 seal_before_impl=0 seal_same_as_tip=0 measure_same_as_tip=0 this=SEAL_ABSENT MEASURE_ABSENT` | `seal_commit_files=1 seal_before_impl=1 seal_same_as_tip=1 measure_same_as_tip=1 this=SEAL_OK MEASURE_OK` | bad `seal_same_as_tip=0 this=SEAL_BROKEN` |
| RE-01 · RE-02 | `added=0` · `hdr=3 g14=1 cols=111 newfmt=0` | 같음 | bad3 `added=1` · bad `newfmt=1` |
| DG-01 · DG-04 | `release_sh=0` · `non_md=0` | 같음 | bad3 `release_sh=1` · `non_md=2` |
| DG-02 | `md_new=0 \|` (바뀐 파일 없음) | `md_new=0` (다섯 파일 각 0) | bad `md_new=1` (notes) |
| AP-03 · AP-04 | `v6_rc=0 fail=0` · `v1_rc=0 fail=0` | 같음 | bad `v6_rc=2 fail=2` · `v1_rc=2 fail=2` |
| DG-05 (ci-local) | `rc=0` 25 줄 · `feedback-agg-test SKIP (yq 없음)` 한 줄 | good 사본 `python3 scripts/validate-plugin.py` · `sync-docs.py --check-only` · `check-stale-values.py` · `run-evals.py` 종료 코드 0 | bad `python3 scripts/validate-plugin.py` 종료 코드 2 |

측정 준비 단계도 봉인 전에 돌렸다: `command -v zsh` → `/bin/zsh`, `command -v shasum` → `/usr/bin/shasum`, markdownlint-cli2 0.23.2 설치본(`MDL` 기본 경로) 있음,
`git worktree add` 가 도우미 임시 폴더 안에서 된다(SC-01 good 의 `miss3`). 시작 판 로컬 CI 요약은 스크래치 `pd/ci0/ci-local/summary.txt`.

## Skill

- [ ] SK-01: PRD 가 없을 때 design-mockup 승인 기록은 결정을 다시 적지 않고 계약 경로를 가리키며, 조건이 기능 단위다(PD-1) — Given 구현 커밋이 가지 `chore/ak2-pd` 에 들어간 뒤, When design-mockup 의 `## Step 6:` 절(다음 `## Step 7:` 앞까지)을 읽으면, Then (a) 이 파일의 차이가 더한 줄 1 · 지운 줄 1 이고 그 차이가 모두 절 안이다 (b) 코드 블록 밖에서 `PRD 없음` 이 든 줄이 1 줄이고 그 한 줄에 `그 기능의 PRD` · `` `범위 경계` 한 곳 `` · `` 줄 끝에 `PRD 없음` `` · `폐기 칸에는 그 계약 경로만 적는다` · `` 줄 끝이 `PRD 없음` 인 줄을 읽어 `` · `하지 않는 것 · 이유 · 범위 · 코드에 남은 흔적` · `PRD 를 만들지 않는다` · `visual-change-protocol.md` 가 모두 있다 (c) 옛 글 `` `.planning/prd-*.md` 가 0 개 `` 와 `폐기 칸에 plan-prd 비범위 표와 같은 네 칸` 이 파일 전체에 각 0 줄이다 (d) PRD 가 있을 때의 폐기 칸 글 `그 기능 PRD 비범위 표 경로와 그 줄의 「하지 않는 것」 만 적는다` 와 확인 명령 줄 `grep -cE '^- (확정 구성|폐기한 대안·이유):'` 이 절 안에 각 1 줄 그대로다 [exact]
  측정: `m SK-01` 이 `numstat=1/1 prose=1 feat=1 scope=1 tail=1 ptr=1 follow=1 cols=1 nocreate=1 vcp=1 old=00 d1=1 check=1 outside=0` (시작 판 `numstat= prose=1 feat=0 scope=0 tail=0 ptr=0 follow=0 cols=1 nocreate=1 vcp=0 old=11 d1=1 check=1 outside=0`, good 은 기대값 그대로)
  양성 대조: bad4(파일 끝, 곧 `## Step 6:` 절 밖에 빈 줄과 한 줄)에서 `numstat=3/1 … outside=2` (봉인 전 실측)
- [ ] SK-02: sprint-contract 는 폐기 결정 줄 하나만 바꾸고, 그 줄이 PRD 가 없을 때 원문 자리를 여기 한 곳으로 정한다(PD-1) — Given 구현 커밋 뒤, When 시작점 `BASE` 부터 끝점 `TIP` 까지(AR-01 과 같은 해석) `harness/skills/sprint-contract/SKILL.md` 의 차이를 보면, Then 더한 줄 1 · 지운 줄 1 이고(다른 묶음이 곧 고칠 파일이라 한 줄만), 더한 줄이 끝 판의 `**포맷 규칙` 줄과 `### 6.2.` 줄 사이에 있으며, 첫 문장 `그 기능 PRD 비범위 표 경로와 항목 이름만 적는다 (planning-kit plan-prd Gotcha 14).` 를 그대로 두고 `그 기능의 PRD 가 없으면` · `결정 원문은 여기 한 곳이다` · `` 줄 끝에 `PRD 없음` `` · `하지 않는 것 · 이유 · 범위 · 코드에 남은 흔적` · `이 계약 경로를 가리키고` 를 모두 담는다. 옛 글 `PRD 가 없으면 plan-prd 와 같은 네 칸` 은 파일에 0 줄이고, 더한 줄에 역슬래시 없는 `$`+숫자가 0 이다(스킬 본문 인자 치환, validate-plugin V9) [exact]
  측정: `m SK-02` 가 `numstat=1/1 in_fmt=1 first=1 feat=1 here=1 tail=1 cols=1 ptr=1 old=0 argsub=0` (시작 판 `numstat= in_fmt=0 first=0 feat=0 here=0 tail=0 cols=0 ptr=0 old=1 argsub=0`, good 은 기대값 그대로)
  양성 대조: bad4(파일 끝, 곧 포맷 규칙 밖에 빈 줄과 한 줄)에서 `numstat=3/1` (봉인 전 실측)
- [ ] SK-03: `/sprint` 재검증 문단이 원문 한 곳 · 기능 단위 · 좁힌 검색 · 두 폴더를 설명한다(PD-1 · PD-2 · PD-3) — Given 구현 커밋 뒤, When `harness/skills/sprint/SKILL.md` 의 `### Step 0.5:` 절(다음 `### Step 1:` 앞까지) 코드 블록 밖 줄을 읽으면, Then `## Non-goals (폐기한 결정 포함)` · `## No-gos` · `plan-prd Gotcha 14` 가 함께 든 줄이 1 줄이고, `그 기능의 PRD 가 없으면` · `` `범위 경계` 한 곳 `` · `` 줄 끝에 `PRD 없음` `` · `그 계약 경로를 가리킨다` · `` `git worktree list` 첫 줄 `` · `새 워크트리에 따라오지 않아` · `뒤에 글이 이어지는 줄은 걸리지 않는다` 가 각 1 줄이며, 옛 글 `` 승인 기록 · 계약 `범위 경계` 에 네 칸으로 `` 는 0 줄, `다시 넣지 않는다` 가 든 줄은 1 줄 이상이다 [exact]
  측정: `m SK-03` 이 `src=1 feat=1 scope=1 tail=1 ptr=1 wt=1 why=1 narrow=1 old=0` 이고 `keep_out` 1 이상 (시작 판 `src=1 feat=0 scope=0 tail=0 ptr=0 wt=0 why=0 narrow=0 old=1 keep_out=1`, good `keep_out=1`)
- [ ] SK-04: `/sprint` 재검증 명령이 두 폴더를 보고, 못 읽은 폴더를 말하고, 줄 끝 모양만 찾는다(PD-2 · PD-3 · 읽는 쪽) — Given 구현 커밋 뒤, When `### Step 0.5:` 절의 text · bash 코드 블록을 읽으면, Then (a) text 블록에 `- 폐기한 결정:` 로 시작하는 줄이 1 줄이고 그 줄에 `` 줄 끝이 `PRD 없음` `` · `` `못 읽음` `` · `모두 없으면 없음` 이 있다 (b) bash 블록에 `git worktree list --porcelain` · `git rev-parse --show-toplevel` · `못 읽음:` · `-name 'prd-*.md'` · `grep -rnE 'PRD 없음[[:space:]]*[|]?[[:space:]]*$'` · `done | sort -u` 가 든 줄이 각 1 줄이고, 옛 검색 `grep -rn 'PRD 없음'` 은 0 줄이다 (c) 새 줄은 기존 세 명령 뒤에 온다(`git diff --stat` 줄보다 `git worktree list` 줄이 아래) (d) 기존 text 세 줄(`- 문서 주장 잔여:` · `- git 실측:` · `- 불일치:`)과 bash 세 명령(`git log --oneline` · `git status --short` · `git diff --stat`)이 각 1 줄 그대로다 (e) 이 파일의 차이가 모두 `### Step 0.5:` 절 안이다(다른 묶음이 같은 파일의 다른 절을 고친다) [exact]
  측정: `m SK-04` 가 `tline=1 tl_tail=1 tl_miss=1 tl_none=1 wt=1 top=1 miss=1 find=1 pat=1 broad=0 sortu=1 order=1 old=111111 outside=0` (시작 판 `tline=1 tl_tail=0 tl_miss=0 tl_none=0 wt=0 top=0 miss=0 find=1 pat=0 broad=1 sortu=0 order=0 old=111111 outside=0`, good 은 기대값 그대로)
  양성 대조: bad(옛 검색으로 되돌리고 `| sort -u` 를 뺌)에서 `pat=0 broad=1 sortu=0` · bad4(처음 좁힌 모양으로 되돌리고 파일 끝, 곧 `### Step 0.5:` 절 밖에 빈 줄과 한 줄)에서 `pat=0 … outside=2` (봉인 전 실측)
- [ ] SK-05: plan-prd Step 0 이 `PRD 없음` 기록을 찾아 PRD 비범위 표로 옮기게 한다(PD-4) — Given 구현 커밋 뒤, When `planning-kit/skills/plan-prd/SKILL.md` 의 `## Step 0:` 절(다음 `## Step 1:` 앞까지)을 읽으면, Then (a) 이 파일의 차이가 더한 줄 1 · 지운 줄 0 이고 그 줄이 `## Step 0:` 절 안에 있다 (b) `` 4. **`PRD 없음` 기록** `` 으로 시작하는 줄이 1 줄이고 그 한 줄에 `grep -rnE 'PRD 없음[[:space:]]*[|]?[[:space:]]*$' .harness .design` · `## Non-goals (폐기한 결정 포함)` · `## No-gos` · `` `→ .planning/prd-<slug>.md` `` · `Gotcha 14` · `다른 기능의 줄은 옮기지 않는다` 가 모두 있다 (c) 기존 세 항목(`1. **원칙 문서**:` · `2. **이전 단계 산출물**:` · `3. **선택 참조**:`)이 각 1 줄 그대로다 [exact]
  측정: `m SK-05` 가 `numstat=1/0 in_s0=1 item=1 pat=1 table=1 nogos=1 arrow=1 gotcha=1 other=1 keep=111` (시작 판 `numstat= in_s0=0 item=0 pat=0 table=0 nogos=0 arrow=0 gotcha=0 other=0 keep=111`, good 은 기대값 그대로)
  양성 대조: bad(plan-prd 에 `name:` 줄 삭제 · 끝에 코드 블록)에서 `numstat=5/1` (봉인 전 실측)
- [ ] SK-06: 쓰는 쪽과 읽는 쪽이 같은 모양을 쓴다(짝 조건) — Given 끝 판, When 쓰는 쪽 셋과 읽는 쪽 둘을 보면, Then 쓰는 쪽 design-mockup · sprint-contract · `/sprint` Step 0.5 코드 블록 밖에 `` 줄 끝에 `PRD 없음` `` 이 각 1 줄 이상이고, 읽는 쪽 `/sprint` Step 0.5 bash 블록과 plan-prd `## Step 0:` 절에 글자 그대로 같은 검색 모양 `'PRD 없음[[:space:]]*[|]?[[:space:]]*$'` 이 각 1 줄이며, 네 스킬 파일(`design-kit/skills/design-mockup/SKILL.md` · `harness/skills/sprint/SKILL.md` · `harness/skills/sprint-contract/SKILL.md` · `planning-kit/skills/plan-prd/SKILL.md`)에 옛 넓은 검색 `grep -rn 'PRD 없음'` 이 0 줄이다. 기준 규약 `design-kit/references/visual-change-protocol.md` 의 「제품 요구 수준의 폐기 결정 … 그 결정이 적힌」 줄은 1 줄 그대로이고 이 파일은 차이가 없다 [exact, enumerated]
  측정: `m SK-06` 이 `prod=111 cons=11 broad=0 vcp=10` (시작 판 `prod=000 cons=00 broad=1 vcp=10`, good 은 기대값 그대로)
  양성 대조: bad(옛 검색 되돌림 · 규약 파일에 줄 더하기)에서 `cons=01 broad=1 vcp=11` · bad4(두 읽는 쪽을 처음 좁힌 모양으로)에서 `cons=00` (봉인 전 실측)

## Script

- [ ] SC-01: 새 워크트리에서 돌려도 본 작업 폴더의 폐기 결정을 모으고, 설명 글은 거르고, 못 읽은 폴더를 말한다(PD-2 · PD-3) — Given `/sprint` Step 0.5 bash 블록에서 `git worktree list` 가 든 줄부터 블록 끝까지 떼어 낸 파일(1 줄 이상이어야 한다 — 0 줄이면 잴 것이 없으니 실패)과 알려진 답 입력: 본 폴더 m(커밋 하나 · 추적 안 된 `.planning/prd-alarm.md` · 걸리면 안 되는 `.planning/discover-alarm.md` · `.harness/sprint-contract-x.md` 에 표 행 셋 — `| 시간대 설정 | … | PRD 없음 |` · 칸 앞 빈칸 없는 `| 언어 설정 | … | PRD 없음|` · 빈칸 둘인 `| 국가 목록 | … | PRD 없음  |` — 과 걸리면 안 되는 규칙 설명 문장 `` … 줄 끝에 `PRD 없음` 을 붙인다. `` 1 줄 · QA 인용 `` - 근거: `PRD 없음` 1 줄 확인 `` 1 줄 · `.design/approvals/20260926-home.md` 에 옛 모양 `- 폐기한 대안·이유: … · PRD 없음` 1 줄)과 m 에서 `git worktree add` 로 만든 새 폴더 wt, When wt 에서 bash 와 zsh 로 각각 돌리면, Then 두 셸 모두 출력 8 줄 — PRD 경로 1 줄(m 의 것) · 폐기 결정 4 줄(표 행 셋 · 옛 승인 기록 줄) · 규칙 설명 · 인용 0 줄 · `못 읽음:` 3 줄(wt 의 세 폴더) — 이고 오류 출력 0 줄이다 [exact]
  측정: `m SC-01` 이 `wt: bash=out8/prd1/tag4/rule0/miss3/err0 zsh=out8/prd1/tag4/rule0/miss3/err0` 이고 `lines` 1 이상 (시작 판 `lines=0` 이고 출력 0 — 뗄 줄이 없다. good `lines=6` 에 기대값 그대로)
  알려진 답: 손으로 세면 PRD 1 · 줄 끝 모양 4(표 행 셋 · 옛 승인 기록 줄) · wt 에 없는 폴더 3 이라 8 줄이고, 봉인 전 good 실제값도 두 셸 8 줄 · 종료 코드 0
  음성 대조: 옛 검색 `grep -rn 'PRD 없음'` 으로 되돌리고 `| sort -u` 를 빼면(bad) `out10/prd1/tag6/rule2/miss3/err0` — 설명 문장 · 인용이 걸린다. 처음 좁힌 모양 `PRD 없음( [|])?[[:space:]]*$` 로 되돌리면(bad4) `out6/prd1/tag2/rule0/miss3/err0` — 표 칸 변형 두 줄을 놓친다 (봉인 전 실측)
- [ ] SC-02: 본 작업 폴더에서 돌리면 같은 폴더를 두 번 세지 않는다(PD-2) — Given SC-01 과 같은 떼어 낸 파일과 입력, When m 에서 bash 와 zsh 로 돌리면, Then 두 셸 모두 출력 5 줄(PRD 1 · 폐기 결정 4 · `못 읽음:` 0 · 규칙 설명 · 인용 0) · 오류 출력 0 줄이다 — 두 폴더가 같을 때 한 벌로 줄인다 [exact]
  측정: `m SC-02` 가 `main: bash=out5/prd1/tag4/rule0/miss0/err0 zsh=out5/prd1/tag4/rule0/miss0/err0` 이고 `lines` 1 이상 (시작 판 `lines=0` 출력 0, good `lines=6` 에 기대값 그대로)
  음성 대조: `| sort -u` 를 빼면(bad) `out14/prd2/tag12/rule4` — 같은 폴더를 두 번 센다 (봉인 전 실측)

## Error

- [ ] ER-01: 기록이 하나도 없는 빈 레포에서 빈 출력 대신 못 읽은 폴더를 말한다(PD-2 — 「기록 없음」 과 「못 봄」 을 가른다) — Given SC-01 과 같은 떼어 낸 파일(1 줄 이상)과 커밋 하나뿐인 빈 레포 empty(`.planning` · `.design` · `.harness` 없음 · 워크트리 없음), When bash 와 zsh 로 empty 에서 돌리면, Then 두 셸 모두 출력이 `못 읽음:` 3 줄뿐이고(PRD 0 · 폐기 결정 0) 오류 출력 0 줄이다 [exact]
  측정: `m ER-01` 이 `empty: bash=out3/prd0/tag0/rule0/miss3/err0 zsh=out3/prd0/tag0/rule0/miss3/err0` 이고 `lines` 1 이상 (시작 판 `lines=0` 이라 전제가 안 서서 실패, good `lines=6` 에 기대값 그대로)
  음성 대조: `| sort -u` 를 빼면(bad) `out6/…/miss6` — 같은 폴더의 못 읽음 줄이 두 번 나온다 (봉인 전 실측)

## Architecture

- [ ] AR-01: 바뀐 파일이 기대 집합 안이고 한 커밋에 맨 위 폴더 하나다 — Given 구현 · notes · QA 리포트 커밋이 모두 가지 `chore/ak2-pd` 에 들어간 뒤, 시작점 `BASE=$(git -C W merge-base origin/main chore/ak2-pd)` 부터 끝점 `TIP=$(git -C W rev-parse --verify chore/ak2-pd)` 까지(`HEAD` 를 쓰지 않는다. 해석이 안 되면 `UNRESOLVED` 로 멈춘다) `git diff --name-only` 로 모은 경로가 측정 도우미 `ALLOWED` 의 여덟 경로 안에만 있고(부분 집합 — 생성물이 없는 묶음이라 제외 pathspec 이 없다), 대상 넷 `design-kit/skills/design-mockup/SKILL.md` · `harness/skills/sprint/SKILL.md` · `harness/skills/sprint-contract/SKILL.md` · `planning-kit/skills/plan-prd/SKILL.md` 가 각각 들어 있으며, 커밋마다 맨 위 폴더가 하나뿐이다(`design-kit` · `harness` · `planning-kit` · `.harness` 가운데 하나) [exact, collective]
  측정: `m AR-01` 이 `extra=0 req=1111 multi_top=0` (시작 판 `changed=0 extra=0 req=0000 multi_top=0`, good `changed=6 extra=0 req=1111 multi_top=0`)
  양성 대조: bad 에서 `extra=1 multi_top=1` 과 남는 경로 `design-kit/references/visual-change-protocol.md` 출력, bad3 에서 `extra=2` (봉인 전 실측)
- [ ] AR-02: 판단과 넘김을 notes 에 남긴다 — Given 끝점 `TIP`, notes 파일 `.harness/.meta/after-kaizen-0926b/pd-notes.md` 가 커밋돼 있고 아홉 토큰 `PD-1` · `PD-2` · `PD-3` · `PD-4` · `docs/design-kit/design-mockup.html` · `DC-15` · `계약이 아직 없` · `Step 2` · `tone-guide` 가 각 1 줄 이상이다. 담을 내용: 네 항목의 처리 결과와 커밋, 옛 글이 된 문서 페이지(`docs/design-kit/design-mockup.html:635`)를 문서 사이트 묶음 DC-15 로 넘김, 이 계약의 판단(작업 계약이 아직 없을 때를 정하지 않은 이유 · design-mockup Step 2 가 계약을 읽지 않는 빈틈을 그대로 둔 이유), tone-guide 5 단계 대조 결과 [exact, enumerated]
  측정: `m AR-02` 가 `committed=1` 과 1 이상 아홉 (시작 판 `committed=0` 과 0 아홉, good `committed=1` 과 1 아홉)
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

- [ ] RE-01: N/A (산출물이 스킬 문서 문장 · 문서 안 셸 명령 몇 줄뿐이라 새 컴포넌트 · 함수 · 모듈이 없다. 측정: `m RE-01` 이 `added=0` — 구간이 `.harness/` 밖에 더한 새 파일 수. 시작 판 0. 양성 대조: bad3 에서 `added=1`)
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다 — 폐기 기록의 새 형식 · 새 파일을 만들지 않고 plan-prd 비범위 표의 네 칸 이름과 Gotcha 14 를 그대로 쓴다: plan-prd 는 지운 줄이 0 이고(세 틀의 머리 줄 `| 하지 않는 것 | 이유 | 범위 | 코드에 남은 흔적 |` 3 줄 · Gotcha 14 의 「디자인 승인 기록 · 작업 계약 · 핸드오프는 이 PRD 경로를 가리키고」 1 줄 그대로), 네 칸 이름 `하지 않는 것 · 이유 · 범위 · 코드에 남은 흔적` 이 design-mockup · sprint-contract · plan-prd 에 각 1 줄이다
  측정: `m RE-02` 가 `hdr=3 g14=1 cols=111 newfmt=0` 이고 `m RE-01` 이 `added=0` (시작 판 `hdr=3 g14=1 cols=111 newfmt=0`, good 은 기대값 그대로)
  양성 대조: bad(plan-prd `name:` 줄 삭제)에서 `newfmt=1` (봉인 전 실측)

## Diagnostics

- [ ] DG-01: N/A (`commands.analyze` 는 `bash -n scripts/release.sh` 라 `scripts/release.sh` 만 잰다 — 이번 바뀐 파일과 교집합 0 개. 측정: `m DG-01` 이 `release_sh=0`. 양성 대조: bad3 에서 `release_sh=1`. 실제 검사는 DG-02 · DG-05)
- [ ] DG-02: IDE diagnostics 워닝/인포 0개 ([] 제외) — IDE(편집기) 진단을 명령줄로 같게 잰다: 바뀐 `.md`(계약 · QA 리포트 · 개정 파일 `.harness/sprint-*.md` 제외)의 더해진 줄에 걸린 markdownlint-cli2 0.23.2(MD013 끔, 편집기 확장과 같은 설정) 경고가 0 이다
  측정: `m DG-02` 가 `md_new=0` (시작 판 `md_new=0` — 바뀐 파일이 없다, good `md_new=0` 다섯 파일 각 0)
  양성 대조: bad(notes 에 `#bad heading`)에서 `md_new=1` (봉인 전 실측)
- [ ] DG-03: N/A (`commands.test` 는 `bash scripts/release.sh 2>&1 || true` 라 `scripts/release.sh` 만 잰다 — 교집합 0 개. 측정: `m DG-03` 이 `release_sh=0` — 도우미 안에서 `m DG-01` 을 그대로 부른다. 양성 대조: bad3 에서 `release_sh=1`)
- [ ] DG-04: N/A (구동할 앱 · 서버가 없다 — 바뀐 파일이 모두 `.md` 라 실행 진입점 0 개. 측정: `m DG-04` 가 `non_md=0`. 양성 대조: bad3 에서 `non_md=2`. 저장소 검사는 DG-05)
- [ ] DG-05: CI(자동 검사) 단계를 로컬에서 전부 돌려 통과한다 — Given 작업 폴더 W 가 끝점과 같다(`git -C W rev-parse HEAD` 가 `TIP` 이고 `git -C W status --porcelain --untracked-files=no` 가 빈 출력), When `PYTHONDONTWRITEBYTECODE=1 TMPDIR=<임시 폴더> bash /Users/jackson/Hub/10_Dev/claude-plugins/.harness/handoff/2026-09-26-tools/ci-local.sh /Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak2-pd` 를 돌리면, Then 요약 `$TMPDIR/ci-local/summary.txt` 에 `rc=0` 줄이 25 개이고 `rc=0` 이 아닌 줄은 `feedback-agg-test SKIP (yq 없음)` 하나뿐이다
  측정: `grep -c 'rc=0' "$TMPDIR/ci-local/summary.txt"` 가 25 · `grep -v 'rc=0' "$TMPDIR/ci-local/summary.txt"` 가 그 한 줄 (시작 판 봉인 전 실측: 25 · SKIP 한 줄)
  도구 지문: 돌리기 전에 `shasum -a 256 <ci-local.sh> | cut -c1-16` 이 `59fe55125c0dbc77` 인지 본다 — 추적 안 된 도구라 다르거나 없으면 이 조건은 다시 잴 수 없다 (범위 경계 참조)
  음성 대조: 이 묶음이 깨뜨릴 수 있는 단계는 `validate-plugin` 이다 — bad 에서 `python3 scripts/validate-plugin.py` 종료 코드 2 (봉인 전 실측)

## 리서치 소스

- 저장소 안만 읽었다(웹 조회 · 외부 문서 가져오기 없음): 남은 일 목록 · 결정 파일(위 배경의 경로, 읽기만), 넘김 기록 `after-0926b/.harness/.meta/after-kaizen-0926/c4d-notes.md`
  「넘긴 것과 사유」 · 「다음 사이클 메모」 R1 ~ R3, 앞 계약 `.harness/sprint-contract-after-0924-discard-decisions.md`(형식 · 측정 도우미 틀)
- 같은 부모 세션의 다른 묶음 계약 형식: `.claude/worktrees/ak2-gd/.harness/sprint-contract-after-0926-guides.md`(읽기만, 측정 줄 들여쓰기 v5.6)
- 계약 형식 원본: 이 가지의 `harness/skills/sprint-contract/SKILL.md`(v0.15.2) · `harness/references/contract-schema.md` §계약 봉인 · §측정 줄 봉인
