---
feature: "폐기 결정 기록 자리를 하나로 — 가리키는 쪽 셋과 처리 배정표 (C4 3 번)"
slug: after-0924-discard-decisions
created: "2026-09-26 13:18"
complexity: "복잡"
conditions: 20
status: active
owner_session: bda55d45-296c-491f-89ba-b52042d58e72
conditions_digest: sha256:881358107856d327
locked_at: "2026-09-26 13:31"
---

## 배경

2026-09-24 카이젠이 「폐기 결정 기록 자리를 하나로」 를 사용자 결정 목록(핸드오프 §C4 3 번, F20)으로 넘겼다. 처리 배정표는 같은 일을
다섯 행에 「카이젠에서 하나로 정한다」 로 남겨 두었다(`.claude/kaizen-input/insights-report.md:77` · `:94` · `:123` · `:134` · `:138`).

- 사용자 결정: 이 세션(`bda55d45-296c-491f-89ba-b52042d58e72`)의 AskUserQuestion 에 user `2026-09-26T02:47:55.337Z` 가
  「plan-prd 표로 확정 (Recommended)」 를 골랐다. 선택지 설명 원문 — 「design-mockup · sprint-contract 가 그 표를 가리키게 고친다.
  오늘 핸드오프 틀에 넣은 폐기 결정 절은 세션 인계용이라 그대로 둔다.」 (세션 기록
  `/Users/jackson/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/bda55d45-296c-491f-89ba-b52042d58e72.jsonl` 1187 번째 줄)
- 결정 내용: 버리거나 거절한 결정의 원문 자리는 기능 PRD 의 비범위 표 하나다 — planning-kit `plan-prd` Gotcha 14 가 정한
  `## Non-goals (폐기한 결정 포함)` 표(Shape Up 틀은 `## No-gos`), 네 칸 `하지 않는 것 · 이유 · 범위 · 코드에 남은 흔적`
  (카이젠 `phase11-notes.md:49`). 이 계약은 그 표를 바꾸지 않고, 가리키는 쪽 셋(design-mockup 승인 기록 · harness `/sprint` 재검증
  블록 · sprint-contract `범위 경계`)과 처리 배정표만 고친다.
- 사용자 합의(Step 5): 사용자 위임으로 받은 것으로 적는다 — user `2026-09-26T01:04:21.505Z` 「다음 세션에서 직접할 일을 다 실행하고
  이어질것도 실행해」 (세션 기록 `/Users/jackson/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/de8c7935-a5b6-4df5-9106-fafa73c288a0.jsonl`),
  그 앞의 「나한테 물어보지 말고 자동으로 끝까지」(`2026-09-24T04:04:16.964Z`). 판단이 갈린 곳은 저장소 안 근거로 정했고 `## 범위 경계` 에 적었다.
- 작업 폴더 W = `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak-c4d`, 가지 `chore/ak-c4d`, 시작점 `f81568d`(origin/main #110).
  origin/main 은 그 뒤 `88ddfe5`(#111 · #112)로 앞서 있지만 그 구간에서 이 묶음 대상 파일은 바뀌지 않았다
  (`git diff --name-only f81568d 88ddfe5 -- <대상 넷> planning-kit` 0 줄, 전체는 9 파일). 합친 판 CI 재실행은 PR 단계 몫이다.
- 커밋 규칙: `git add <경로>` 뒤 `git commit -o <경로>` · 한 커밋에 맨 위 폴더 하나(`design-kit` · `harness` · `.claude` · `.harness` 가운데 하나) ·
  `git add -A` · `git stash` · push · 가지 바꾸기 금지. 봉인 커밋(계약 한 파일)이 구현 커밋보다 먼저다.
- 다른 세션이 `harness/skills/sprint-contract/SKILL.md` 를 곧 고칠 수 있다 — 이 계약은 그 파일에 한 줄만 더하고 지우는 줄은 없다(SK-05).
- 구현 전에 `tone-kit:tone-guide` 1 단계(규칙 불러오기)를, 완료 선언 전에 5 단계(전수 대조)를 한다 — 대조 결과는 notes 에 남긴다(AR-03).
- 사용자가 할 일: 없음.

복잡도 4 축 — 넷 모두 「예」 이고 공개 약속 변경과 소비자가 함께 있어 「복잡」 이다. Step 2.5 짝 조건: 원문 쪽은 RE-02(plan-prd 표 그대로),
가리키는 쪽은 SK-01 · SK-02(승인 기록) · SK-05(계약), 읽는 쪽은 SK-03(design-mockup Step 2) · SK-04 · SC-01 · ER-01(`/sprint` 재검증).

| 축 | 물음 | 값 |
| -- | ---- | -- |
| 레이어 수 | 몇 개 계층을 관통하는가 | 셋 — 킷 스킬 문서(design-kit 하나 · harness 둘), 처리 배정표(`.claude/`), 작업 기록(`.harness/`) |
| 공개 API·계약 변경 | 밖에 드러난 약속이 바뀌는가 | 예 — 승인 기록 폐기 칸에 적는 내용, `/sprint` 재검증 블록이 내는 줄과 명령, 계약 `범위 경계` 에 폐기 결정을 적는 법 |
| 소비면 존재 | 반대편이 있는가 | 예 — design-mockup Step 2(승인 기록을 읽는다) · `design-kit/evals/evals.json:539`(칸 이름 단언) · `/sprint` Step 1(재검증 결과로 계약을 쓴다) · 사용자 프로젝트의 기존 승인 기록 |
| 회귀 위험 | 기존 동작이 깨질 수 있는가 | 예 — 승인 기록 확인 명령의 `→ 2` 기대값, 처리 배정표 검사(`scripts/check-insights-tracking.py` 가 칸 수를 센다), 다른 세션이 곧 고칠 sprint-contract |

설정 값 대조 (`.harness/project.yaml` 을 글자 그대로 옮김):

| config key | project.yaml 에서 읽은 값 | 계약에 쓴 값 |
| ---------- | ------------------------- | ------------ |
| `commands.analyze` | `bash -n scripts/release.sh` | DG-01 N/A — 재는 파일이 바뀐 파일에 없다 |
| `commands.test` | `bash scripts/release.sh 2>&1 \|\| true` | DG-03 N/A — 같은 이유 |
| `diagnostics.ide_exclude` | `[]` | DG-02 의 `([] 제외)` |
| `contract_categories[].id` / `prefix` | Skill/SK · Script/SC · Error/ER · Architecture/AR | 같은 넷 |
| `anti_patterns[].id` / `message` | AP-01 버전 하드코딩 · AP-02 force push · AP-03 bare code fence · AP-04 frontmatter name 누락 | AP-03 · AP-04 (바뀌는 파일이 코드 블록 있는 SKILL.md 셋이다). AP-01 은 plugin.json 버전을 건드리지 않아서, AP-02 는 이 계약이 push 하지 않아서 뺐다 |

## 리서치 소스

- 저장소 안만 읽었다(웹 조회 · 외부 문서 가져오기 없음): 핸드오프 `/Users/jackson/Hub/10_Dev/claude-plugins/.harness/handoff/2026-09-26-0110.md` §C0 · §C2 · §C4(본 체크아웃, 읽기만),
  이 가지의 `.harness/.meta/kaizen-0924/phase11-notes.md:49` · `:85` · `:89`, `phase4-notes.md:72` · `:92`, `phase6-notes.md:59` · `:69`,
  `phase8-notes.md:94`, `phase9-notes.md:94`, `f1-harness-followups-notes.md:115`, `final-notes.md` · `f2-review-fixes-notes.md` 「다음 사이클 메모」(폐기 결정 관련 항목 없음)
- 사용자 결정 원문: 세션 기록 `bda55d45-296c-491f-89ba-b52042d58e72.jsonl` 1178 번째 줄(질문) · 1187 번째 줄(답)
- 같은 부모 세션의 앞 묶음 계약 형식: `.claude/worktrees/ak-c3/.harness/sprint-contract-after-0924-kits-a.md` · `ak-c4c/.harness/sprint-contract-after-0924-rust-app-name.md`(읽기만)

## GAP 분석 (Pre-Edit Audit)

대상 파일을 읽기만 하고 줄을 적었다. 줄 번호는 시작점 `f81568d` 기준이다.

| 대상 파일 | 실제 Read 증거 (`파일:라인`) | 발견한 기존 갭·위반 | 계약 조건화 여부 |
| --------- | ---------------------------- | ------------------- | ---------------- |
| `planning-kit/skills/plan-prd/SKILL.md` | `:28` Gotcha 14(원문 자리 · 「디자인 승인 기록 · 작업 계약 · 핸드오프는 이 PRD 경로를 가리키고 결정을 다시 쓰지 않는다」) · `:87-90` · `:114-117` · `:126-129` 세 틀의 네 칸 머리 · `:143-144` Step 4 | 원문 자리는 이미 있다(Phase 11). 그런데 가리키라고 한 쪽 셋이 아직 가리키지 않는다. `:15` Gotcha 1 때문에 폐기 기록만 담은 PRD 는 만들 수 없다 | RE-02 (그대로인지) |
| `design-kit/skills/design-mockup/SKILL.md` | `:159` 폐기 칸 `{이번 결정에서 버린 안·요소와 이유 — 없으면 \`없음\`}` · `:150-162` 승인 기록 틀 · `:164-170` 확인 명령(`→ 2`) · `:29` Gotcha 13 | 기능·설정 항목을 버린 결정도 이 칸에 이유째 다시 적게 되어 있다. PRD 가 없는 프로젝트에서 할 일이 없다 | SK-01 · SK-02 |
| 같은 파일 Step 2 | `:52-60` 감지 대상 블록 · `:65-66` 승인 기록 규칙 | PRD 비범위 표를 읽지 않는다 — 기획 단계에서 버린 항목이 승인 기록에 없으면 시안에 다시 들어갈 수 있다(F20 의 실제 모양) | SK-03 |
| `design-kit/references/visual-change-protocol.md` | `:206` 틀의 폐기 칸 · `:218-222` 규칙 둘 — 「제품 요구 수준의 폐기 결정 … 그 결정이 적힌 파일 경로를 폐기 칸에 적는다」 | 승인 기록 규격은 이미 경로만 적게 한다. 바꾸지 않는다. 같은 파일 §6(`:386-441`)은 다른 워크트리 `ak-c3` 가 고치고 있다 | 범위 경계 (그대로) |
| `design-kit/skills/design-concept/SKILL.md` | `:97` · `:103` · `:219` · `:228` | 컨셉 안(무드 · 색 방향)만 버리는 칸이다 — 기능·설정 항목이 아니다. 바꾸지 않는다 | 범위 경계 (그대로) |
| `harness/skills/sprint/SKILL.md` Step 0.5 | `:56-75` 절 · `:60-64` bash 블록 · `:68-73` text 블록 · `:75` 불일치 문장 | 재개할 때 폐기한 결정을 읽는 줄이 없다(F1H-41 뒷절반 · `user-setup:P2` 의 「폐기 결정 줄」 · `phase4-notes.md:92` · `phase11-notes.md:85`) | SK-04 · SC-01 · ER-01 |
| 같은 파일 Step 3 | `:111-115` 원인 가르기 판정 표 | F1H-41 앞절반(CI 에서만 보이는 두 경우 `phase8-notes.md:94` · 첫 줄 문턱 `phase9-notes.md:94`)은 폐기 결정과 다른 일이다. 표는 두 킷이 글자 그대로 옮겨 갔다(`docs/infra/platform/cicd.md:76` · `rust-kit/skills/rust-preflight/SKILL.md:112`) | 넘김 (범위 경계) |
| `harness/skills/sprint-contract/SKILL.md` | `:622-633` 포맷 규칙 · `:627` 서술 섹션 목록의 `범위 경계` · `:629` 목록 밖 헤더 금지 줄 | 계약 `범위 경계` 에 폐기 결정을 어떻게 적을지 없다 | SK-05 |
| `.claude/kaizen-input/insights-report.md` | `:77` F20 · `:94` design:P5 · `:123` backend-family:P1 · `:134` user-setup:P2 · `:138` user-setup:P6 · `:44` 델타 요약 · `:55-56` 표 머리 | 다섯 행이 「카이젠에서 하나로 정한다」(user-setup:P6 은 「카이젠 뒤 사용자 설정 처리 목록」)로 남아 있다. `:44` 는 입력 요약이라 그대로 둔다 | AR-02 |
| `scripts/check-insights-tracking.py` | `:18-23` 필수 열 · `:119-122` 칸 수가 머리와 다르면 읽기 실패 | 비고 칸에 `\|` 가 새로 들어가면 표가 깨진다 | AR-02 (검사로 부른다) |
| `planning-kit/skills/plan-stories/SKILL.md:44` · `plan-flow/SKILL.md:33` · `plan-data-model/SKILL.md:37` | 각 줄 | 기획 뒤 단계 셋은 이미 PRD 비범위 표를 읽는다 — 바꾸지 않는다 | 범위 경계 (소비자 근거) |
| `design-kit/evals/evals.json` | `:539` 「승인 기록에 확정 구성과 폐기한 대안·이유 칸을 포함한다」 | 칸 이름을 그대로 두므로 맞는 채로 남는다 | SK-01 (c) |
| `docs/design-kit/design-mockup.html` | `grep -c -E '폐기\|승인 기록'` 10 줄 | 원본이 바뀌면 페이지가 옛 글이 된다 — 문서 사이트는 이 계약 밖 | 넘김 (AR-03 notes) |

개선안 — 구현이 넣을 글. 조건은 아래 낱말(토큰)만 재므로 문장은 톤 대조에 맞춰 다듬어도 된다. 같은 글을 사본에 그대로 넣는 스크립트는
세션 스크래치 `c4d/mock.py` 다(`mock applied`, 알려진 답 · 양성 대조에 썼다).

```text
[D1] design-mockup Step 6 틀의 폐기 칸 (옛 :159 한 줄을 바꾼다)
- 폐기한 대안·이유: {버린 안·요소와 이유 — 기능·설정 항목을 없앤 결정이면 이유는 여기 다시 쓰지 않는다. 그 기능 PRD 비범위 표 경로와 그 줄의 「하지 않는 것」 만 적는다 (planning-kit plan-prd Gotcha 14) · 없으면 `없음`}

[D2] 같은 Step 6, 틀 코드 블록 바로 뒤 산문 한 줄 (PRD 가 없을 때)
PRD 가 없는 프로젝트(`.planning/prd-*.md` 가 0 개)는 그 결정을 폐기 칸에 plan-prd 비범위 표와 같은 네 칸(하지 않는 것 · 이유 · 범위 · 코드에 남은 흔적)으로 이어 적고 끝에 `PRD 없음` 을 붙인다 — 폐기 기록만 담으려고 PRD 를 만들지 않는다 (plan-prd Gotcha 1).

[D3] design-mockup Step 2 — 감지 대상 블록에 한 줄, 규칙 목록에 한 줄
.planning/prd-*.md          → 비범위 표(## Non-goals (폐기한 결정 포함) · ## No-gos)의 폐기한 결정 로드
- PRD 비범위 표 존재 → 그 표의 항목은 시안에 넣지 않는다. 코드에 흔적이 남아 있어도 요구로 읽지 않고, 되살려야 할 것 같으면 만들기 전에 사용자에게 묻는다 (planning-kit plan-prd Gotcha 14)

[S1] /sprint Step 0.5 bash 블록 끝에 두 줄
find .planning -maxdepth 1 -type f -name 'prd-*.md' 2>/dev/null   # 폐기한 결정 원문이 든 PRD
grep -rn 'PRD 없음' .design .harness 2>/dev/null                  # PRD 가 없을 때 적어 둔 폐기 결정

[S2] /sprint Step 0.5 text 블록에 한 줄
- 폐기한 결정: <PRD 비범위 표 항목 · `PRD 없음` 줄 — 둘 다 없으면 없음>

[S3] /sprint Step 0.5 산문 한 문단 (불일치 문장 앞)
폐기한 결정의 원문은 기능 PRD 의 비범위 표 하나다 — planning-kit plan-prd Gotcha 14 의 `## Non-goals (폐기한 결정 포함)` · Shape Up `## No-gos`. PRD 가 없는 프로젝트는 승인 기록 · 계약 `범위 경계` 에 네 칸으로 적고 `PRD 없음` 을 붙이므로 위 grep 으로 모은다. 여기 든 항목은 사용자가 되살리라고 하지 않는 한 계약 · 구현에 다시 넣지 않는다 — 필요해 보이면 Step 1 전에 묻는다.

[C1] sprint-contract Step 6 포맷 규칙 — 「두 목록 밖의 헤더」 줄 바로 뒤 한 줄
  - `범위 경계` 에 폐기한 결정(사용자가 기능·설정 항목을 없애기로 한 결정)을 적을 때는 결정을 다시 쓰지 말고 그 기능 PRD 비범위 표 경로와 항목 이름만 적는다 (planning-kit plan-prd Gotcha 14). PRD 가 없으면 plan-prd 와 같은 네 칸(하지 않는 것 · 이유 · 범위 · 코드에 남은 흔적)으로 적고 끝에 `PRD 없음` 을 붙인다

[I1] 처리 배정표 다섯 행 — 비고 칸 끝(닫는 ` |` 앞)에 덧붙인다. 앞 글은 지우지 않는다
F20               · 처리(2026-09-26 `after-0924-discard-decisions`) — 사용자가 원문 자리를 기능 PRD 비범위 표 하나로 확정했다. design-mockup 승인 기록 · sprint-contract 범위 경계 · /sprint Step 0.5 가 그 표를 가리키고, PRD 가 없으면 네 칸으로 적고 `PRD 없음` 을 붙인다
design:P5         · 처리(…) — 원문 자리는 기능 PRD 비범위 표 하나(사용자 결정). design-mockup 승인 기록 폐기 칸이 그 표 경로를 가리키고, PRD 가 없으면 네 칸 · `PRD 없음`
backend-family:P1 · 처리(…) — plan-prd 의 기능 PRD 비범위 표가 원문 자리로 확정됐다(사용자 결정). 표는 바꾸지 않았다
user-setup:P2     · 처리(…) — /sprint Step 0.5 재검증 블록에 폐기한 결정 줄 — 기능 PRD 비범위 표와 `PRD 없음` 줄을 읽는다
user-setup:P6     · 처리(…) — 핸드오프 틀의 폐기 절은 세션 인계용이라 따로 둔다 — 결정 원문 자리가 아니다(원문은 기능 PRD 비범위 표). 틀 수정은 킷 밖 사용자 설정 몫
```

## 범위 경계

항목별 처리 — 입력은 과제의 대상 항목 셋과 그에 딸린 넘김 기록이다.

| 항목 | 처리 | 조건 · 사유 |
| --- | --- | --- |
| design-mockup `:159` 폐기 칸이 원문을 따로 적지 않고 PRD 비범위 표를 가리키게 | 계약에 넣음 | SK-01. 칸 이름 `폐기한 대안·이유` 는 그대로 둔다 — 확인 명령 `→ 2` 와 `evals.json:539` 가 이 이름을 잰다. 시각 대안(고르지 않은 시안 · 배치)만 버린 경우는 이유 한 줄을 이 칸에 남긴다: plan-prd Gotcha 14 가 표에 넣으라는 것은 「기능·설정 항목」 이고(`plan-prd:28`), 시안 선택은 제품 요구가 아니다. 규약 `visual-change-protocol.md:221-222` 도 제품 요구 수준만 경로로 적게 한다 |
| planning-kit 이 없는 프로젝트(가리킬 표가 없을 때) | 계약에 넣음 | SK-02 한 줄. 네 칸 이름을 그대로 쓰고 `PRD 없음` 을 붙인다 — 폐기 기록만 담은 PRD 는 `plan-prd:15` Gotcha 1 때문에 만들 수 없다. `PRD 없음` 은 `/sprint` 재검증이 grep 으로 모으는 표시다(SC-01) |
| design-mockup Step 2 가 PRD 비범위 표를 읽기 | 계약에 넣음 (이 계약의 판단) | SK-03. 과제 문구에는 없지만, 가리키는 칸만 고치면 기획에서 버린 항목(승인 기록에 없는 것)을 시안이 모른다 — F20 이 실제로 그렇게 났다. 기획 뒤 단계 셋은 이미 같은 표를 읽는다(`plan-stories:44` · `plan-flow:33` · `plan-data-model:37`). 두 줄만 더한다 |
| F1H-41 뒷절반 — `/sprint` 재검증 블록의 폐기 결정 자리 | 계약에 넣음 | SK-04 · SC-01 · ER-01. `user-setup:P2` 의 「폐기 결정 줄」 과 같은 일이다 |
| F1H-41 앞절반 — `/sprint` Step 3 판정 표 (CI 에서만 보이는 두 경우 · 첫 줄 문턱) | 넘김 | 폐기 결정과 다른 일이다(`phase8-notes.md:94` · `phase9-notes.md:94`). 표를 바꾸면 글자 그대로 옮긴 사본 둘(`docs/infra/platform/cicd.md:76` · `rust-kit/skills/rust-preflight/SKILL.md:112`)도 함께 바뀌어야 해 「다른 킷」 범위 밖이다. 다음 사이클 Phase 4 로 — notes 에 적는다(AR-03 `판정 표`) |
| sprint-contract 가 폐기 결정을 적을 때 같은 표를 가리키게 | 계약에 넣음 | SK-05 한 줄. 자리는 Step 6 포맷 규칙의 서술 섹션 목록 아래 — 폐기 결정이 들어갈 계약 자리가 `범위 경계` 이기 때문이다(`:627`) |
| 처리 배정표 design:P5 · backend-family:P1 · user-setup:P2 · user-setup:P6 | 계약에 넣음 | AR-02. user-setup:P6 행에는 핸드오프 틀 절이 세션 인계용이라 따로 둔다는 것까지 적는다(사용자 선택지 설명 원문) |
| 처리 배정표 F20 행 | 계약에 넣음 (이 계약의 판단) | AR-02. 과제는 네 행을 적었지만 F20 행 비고(`:77`)가 같은 「네 곳이다 — 카이젠에서 하나로 정한다」 문장을 갖고 있다. 남기면 처리 뒤에도 미정으로 읽힌다 |
| plan-prd 비범위 표 자체 | 바꾸지 않음 | RE-02 가 그대로인지 잰다(Phase 11 이 이미 넣었다) |
| design-concept 폐기 칸 · visual-change-protocol §4 | 바꾸지 않음 | 위 GAP 표. §4 는 이미 「결정이 적힌 파일 경로」 를 적게 한다 — 그 경로가 PRD 비범위 표라는 것은 design-mockup 쪽 글이 말한다. notes 에 이유를 적는다(AR-03 `design-concept` · `visual-change-protocol`) |
| PRD 가 나중에 생겼을 때 `PRD 없음` 줄을 PRD 표로 옮기는 절차 | 넘김 | plan-prd Step 0 이 읽을 대상을 늘리는 일이라 planning-kit 몫이다 — 다음 사이클. notes 에 적는다(AR-03 `PRD 없음`) |
| 핸드오프 스킬(`~/.claude/skills/handoff`) · 다른 킷 · `docs/` HTML 페이지 | 범위 밖 | 과제가 정한 범위 밖. 원본이 바뀌어 옛 글이 되는 `docs/design-kit/design-mockup.html` 은 notes 에 적어 문서 사이트 묶음으로 넘긴다(AR-03) |

범위 밖(이 계약이 고치지 않는다): 위 표의 「넘김」 · 「범위 밖」 줄, 킷 `plugin.json` 버전(릴리스 단계 몫), `scripts/`, `.github/`.

커버리지 해소 — Step 6.5 (4) 검출기가 낸 `UNCOVERED` 의 처리:

- 커버리지 해소: AR-03 — notes 경로는 측정 도우미 `NOTES` 변수가, `docs/design-kit/design-mockup.html` 은 `m AR-03` 의 토큰 목록이 센다(산문과 같은 글자). 목록을 두 번 적지 않으려고 측정 절에 다시 늘어놓지 않았다
- 커버리지 해소: AR-01 — 경로 기대 집합은 측정 도우미 `ALLOWED` 한 곳에만 적는다(`collective` 라 검출기가 보지 않지만 같은 원칙). 산문의 대상 넷은 `m AR-01` 의 `req` 네 자리가 센다
- 오라클 해소: SK-01 ~ SK-05 · AR-03 — 산출물이 스킬 문서 문장이라 부를 코드가 없다. 정해 둔 토큰의 줄 수와 자리(절 · 코드 블록 안팎)로 재고, 시작 판이 실패 값이며 good 이 기대값인 것을 봉인 전에 확인했다. 실행해서 재는 조건은 SC-01 · ER-01(떼어 낸 명령을 두 셸로 돌린다) · AR-02(검사 스크립트) · AR-04 · DG-02 · DG-05 다
- 오라클 해소: SK-04 — 이 조건은 글이 제자리에 있는지만 본다. 같은 bash 블록의 새 두 줄은 SC-01 · ER-01 이 블록에서 원문 그대로 떼어 bash · zsh 로 실제로 돌려 잰다(재타이핑 없음). 줄을 지우면 SK-04 는 `find=0` · `grep=0`, SC-01 · ER-01 은 `lines=0` 으로 함께 실패한다

봉인 전 교차 진단(qa-evaluator, 2026-09-26) 반영:

- `m DG-03` 이 `모르는 조건` 으로 멈추던 것 — 도우미에 `DG-03)` 분기를 더해 `m DG-01` 을 부르게 했고, DG-03 조건 문구도 `m DG-03` 으로 맞췄다
- AR-02 의 `counts=[…]` 는 처리 배정표 전체 행의 `배정` 칸 합계다. 이 계약은 다섯 행의 `비고` 칸만 고치므로 가지 끝에서는 흔들리지 않는다. 같은 파일을 고치는 다른 묶음이 먼저 `main` 에 합쳐지면 합친 판에서 이 값이 달라질 수 있는데, 그것은 이 묶음의 회귀가 아니다 — 평가 기준은 이 가지 끝(`TIP`)이다. notes 와 PR 설명에도 적는다
- SK-03 · F20 행은 과제 문구 밖의 이 계약 판단이라 봉인 전에 사용자 확인을 받으라는 권고가 있었다. 사용자 위임(`2026-09-26T01:04:21.505Z` · `2026-09-24T04:04:16.964Z`)이 「묻지 말고 끝까지」 라 묻지 않았다. 근거는 위 표 두 행(F20 의 실제 모양 · `:77` 에 남는 같은 문장)이고, 둘 다 더하기만 하는 변경이라 되돌리기 쉽다. notes 에 적는다

## 회귀 게이트 — 측정 도우미

평가 때 이 블록을 떼어 bash 에서 불러 쓴다. `TMPDIR` 은 평가자 임시 폴더로 준다. 도우미는 끝점을 `git archive` 로 풀어 재므로 작업 폴더의 미커밋
변경을 보지 않는다. 작업 폴더 밖 입력은 지우지 마라 — 도우미가 만든 `$T` 아래만 치워도 된다. `MDL` 이 가리키는 markdownlint 설치본이 없으면
`mdl_ready` 가 그 자리에 설치한다(npm).

```bash
# 떼기: awk '/^# === 측정 도우미 시작/{f=1} f{print} /^# === 측정 도우미 끝/{exit}' <계약> > "$TMPDIR/c4d-measure.sh"
# 부르기: bash -c 'source "$TMPDIR/c4d-measure.sh" || exit 2; type m >/dev/null || exit 2; m SK-01'
# 시작 판: E_REF=BASE 를 주고 부른다. 다른 사본을 재려면 W=<사본> 을 준다
# === 측정 도우미 시작 (after-0924-discard-decisions) ===
# 쓰는 법: 이 블록을 파일로 떼어 bash 에서 source 한 뒤 `m <조건 ID>`. zsh 에서 source 하지 마라.
# 잴 트리 E — 기본은 가지 끝(TIP)을 git archive 로 푼 임시 폴더. 시작 판을 재려면 E_REF=BASE.
W=${W:-/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak-c4d}
BR=${BR:-chore/ak-c4d}
BASE=$(git -C "$W" merge-base origin/main "$BR") || { echo "UNRESOLVED BASE"; return 2 2>/dev/null || exit 2; }
TIP=$(git -C "$W" rev-parse --verify "$BR") || { echo "UNRESOLVED TIP"; return 2 2>/dev/null || exit 2; }
T=$(mktemp -d "${TMPDIR:-/tmp}/c4d.XXXXXX")
snap() { mkdir -p "$2" && git -C "$W" archive "$1" | tar -x -C "$2"; }
case "${E_REF:-TIP}" in
  BASE) E=$T/base; snap "$BASE" "$E" ;;
  *)    E=$T/tip;  snap "$TIP" "$E" ;;
esac
DM=design-kit/skills/design-mockup/SKILL.md
SP=harness/skills/sprint/SKILL.md
SC=harness/skills/sprint-contract/SKILL.md
PRD=planning-kit/skills/plan-prd/SKILL.md
IR=.claude/kaizen-input/insights-report.md
CF=.harness/sprint-contract-after-0924-discard-decisions.md
NOTES=.harness/.meta/after-kaizen-0926/c4d-notes.md
COLS='하지 않는 것 · 이유 · 범위 · 코드에 남은 흔적'
ALLOWED='design-kit/skills/design-mockup/SKILL.md
harness/skills/sprint/SKILL.md
harness/skills/sprint-contract/SKILL.md
.claude/kaizen-input/insights-report.md
.harness/sprint-contract-after-0924-discard-decisions.md
.harness/sprint-feedback-after-0924-discard-decisions.md
.harness/sprint-amendments-after-0924-discard-decisions.md
.harness/.meta/after-kaizen-0926/c4d-notes.md'
# s 로 시작하는 줄부터 e 로 시작하는 다음 줄 앞까지
sec() { awk -v s="$1" -v e="$2" 'index($0,s)==1{f=1;print;next} f&&index($0,e)==1{exit} f' "$3"; }
# 표준 입력에서 글자 그대로 든 줄 수 (0 건에도 0 을 찍는다)
n() { grep -cF -- "$1" || true; }
nocode() { awk '/^[[:space:]]*```/{c=!c;next} !c'; }   # 코드 블록 밖 줄만
incode() { awk '/^[[:space:]]*```/{c=!c;next} c'; }    # 코드 블록 안 줄만
blk() { awk -v t="$1" 'index($0,"```" t)==1{b=1;next} b&&/^```/{b=0} b'; }   # 언어가 t 인 코드 블록 안 줄만
fmv() {  # fmv <키> <파일> — 첫 frontmatter 블록에서만 읽고 따옴표를 벗긴다 (sprint-contract read_fm 과 같은 awk)
  awk -v k="^${1}:[[:space:]]*" 'NR==1&&/^---[[:space:]]*$/{f=1;next} f&&/^---[[:space:]]*$/{exit} f&&$0~k{sub(k,"");print;exit}' "$2" \
    | sed -e 's/[[:space:]]*$//' -e "s/^['\"]//" -e "s/['\"]\$//"
}
h16() { shasum -a 256 | cut -c1-16; }
digest() { grep -E '^- \[[ x]\] [A-Z]{2,}-[0-9]{2}' | sed -E 's/^- \[[ x]\]/- [ ]/' | h16; }
MDL=${MDL:-/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/bda55d45-296c-491f-89ba-b52042d58e72/scratchpad/mdl}
mdl_ready() {  # markdownlint-cli2 0.23.2 · MD013 끔 — 편집기 확장과 같은 설정. 없으면 MDL 에 설치한다
  [ -x "$MDL/node_modules/.bin/markdownlint-cli2" ] || { mkdir -p "$MDL" && (cd "$MDL" && npm install --no-save --no-audit --no-fund markdownlint-cli2@0.23.2 >/dev/null 2>&1); }
  printf '{ "config": { "MD013": false } }\n' > "$T/cfg.markdownlint-cli2.jsonc"
  [ -x "$MDL/node_modules/.bin/markdownlint-cli2" ]
}
added() { diff -U0 "$1" "$2" | awk '/^@@/{split($3,a,","); s=substr(a[1],2); c=(a[2]=="")?1:a[2]; for(i=0;i<c;i++) print s+i}'; }
newmd() {  # newmd <옛 파일|/dev/null> <새 파일> — 새 파일에서 더해진 줄에 걸린 경고 수
  ( cd "$(dirname "$2")" && "$MDL/node_modules/.bin/markdownlint-cli2" --config "$T/cfg.markdownlint-cli2.jsonc" "$(basename "$2")" 2>&1 ) \
    | awk -F: '/^[^ ]+:[0-9]+/{print $2+0}' | sort -n > "$T/w.txt"
  added "$1" "$2" | sort -n > "$T/a.txt"
  comm -12 "$T/w.txt" "$T/a.txt" | grep -c . || true
}
sprint_lines() {  # /sprint Step 0.5 bash 블록에서 폐기 결정을 모으는 줄만 떼어 파일로
  sec '### Step 0.5:' '### Step 1:' "$E/$SP" | blk bash | grep -E '\.planning|PRD 없음' > "$T/lines.sh" || true
}
proj() {  # 알려진 답 입력 — p1: PRD 하나 · discover 하나 · PRD 없음 줄 하나 / p0: 빈 폴더
  P1=$T/p1; P0=$T/p0; mkdir -p "$P1/.planning" "$P1/.design/approvals" "$P1/.harness" "$P0"
  printf '## Non-goals (폐기한 결정 포함)\n' > "$P1/.planning/prd-alarm.md"
  printf 'x\n' > "$P1/.planning/discover-alarm.md"
  printf -- '- 폐기한 대안·이유: 시간대 설정 · 쓰지 않는다고 함 · 제품 전체 · 없음 · PRD 없음\n' > "$P1/.design/approvals/20260926-home.md"
  printf 'nothing\n' > "$P1/.harness/other.md"
}
runs() {  # runs <폴더> — bash · zsh 로 떼어 낸 줄을 돌려 줄 수를 센다
  r=""; for sh in bash zsh; do
    (cd "$1" && "$sh" "$T/lines.sh" >"$T/o" 2>"$T/e")
    r="$r $sh=out$(grep -c . "$T/o" || true)/prd$(grep -c 'prd-alarm\.md$' "$T/o" || true)/tag$(grep -c 'PRD 없음' "$T/o" || true)/err$(grep -c . "$T/e" || true)"
  done; printf '%s' "${r# }"
}

m() {
  case "$1" in
  SK-01) s6=$(sec '## Step 6:' '## Step 7:' "$E/$DM"); f=$(printf '%s\n' "$s6" | grep -E '^- 폐기한 대안·이유:')
    echo "field=$(printf '%s\n' "$f" | grep -c . || true) kind=$(printf '%s\n' "$f" | n '기능·설정 항목') norewrite=$(printf '%s\n' "$f" | n '다시 쓰지 않는다') table=$(printf '%s\n' "$f" | n '비범위 표') gotcha=$(printf '%s\n' "$f" | n 'plan-prd Gotcha 14') old=$(n '이번 결정에서 버린 안·요소와 이유' <"$E/$DM") check=$(printf '%s\n' "$s6" | n "grep -cE '^- (확정 구성|폐기한 대안·이유):'")" ;;
  SK-02) s6=$(sec '## Step 6:' '## Step 7:' "$E/$DM"); p=$(printf '%s\n' "$s6" | nocode | grep -F 'PRD 없음')
    echo "all=$(printf '%s\n' "$s6" | n 'PRD 없음') prose=$(printf '%s\n' "$p" | grep -c . || true) planning=$(printf '%s\n' "$p" | n '.planning/prd-*.md') cols=$(printf '%s\n' "$p" | n "$COLS") nocreate=$(printf '%s\n' "$p" | n 'PRD 를 만들지 않는다')" ;;
  SK-03) s2=$(sec '## Step 2:' '## Step 3:' "$E/$DM")
    echo "load=$(printf '%s\n' "$s2" | incode | grep -E '^\.planning/prd-\*\.md' | n '폐기한 결정') rule=$(printf '%s\n' "$s2" | nocode | grep -E '^- PRD 비범위 표 존재 →' | n '묻는다') approvals=$(printf '%s\n' "$s2" | n '.design/approvals/*.md      → 같은 화면의 확정 구성 · 폐기한 대안 로드') keep=$(printf '%s\n' "$s2" | n '- 승인 기록 존재 → 확정 구성을 지키고, 폐기한 대안·요소는 사용자가 되살리라고 하지 않는 한 시안에 다시 넣지 않는다')" ;;
  SK-04) s=$(sec '### Step 0.5:' '### Step 1:' "$E/$SP"); tb=$(printf '%s\n' "$s" | blk text); bb=$(printf '%s\n' "$s" | blk bash); pr=$(printf '%s\n' "$s" | nocode)
    old=""; for k in '- 문서 주장 잔여:' '- git 실측:' '- 불일치:'; do old="$old$(printf '%s\n' "$tb" | n "$k")"; done
    for k in 'git log --oneline' 'git status --short' 'git diff --stat'; do old="$old$(printf '%s\n' "$bb" | n "$k")"; done
    echo "tline=$(printf '%s\n' "$tb" | grep -c '^- 폐기한 결정:' || true) none=$(printf '%s\n' "$tb" | grep '^- 폐기한 결정:' | n '없음') find=$(printf '%s\n' "$bb" | n "find .planning -maxdepth 1 -type f -name 'prd-*.md'") grep=$(printf '%s\n' "$bb" | n "grep -rn 'PRD 없음' .design .harness") src=$(printf '%s\n' "$pr" | grep -F '## Non-goals (폐기한 결정 포함)' | grep -F '## No-gos' | n 'plan-prd Gotcha 14') keep_out=$(printf '%s\n' "$pr" | n '다시 넣지 않는다') old=$old" ;;
  SK-05) ns=$(git -C "$W" diff --numstat "$BASE" "$TIP" -- "$SC" | awk '{print $1"/"$2}')
    add=$(git -C "$W" diff -U0 "$BASE" "$TIP" -- "$SC" | grep -E '^\+[^+]' | sed 's/^+//')
    fmt=$(awk '/^\*\*포맷 규칙/{f=1;next} f&&/^### 6\.2\./{exit} f' "$E/$SC")
    i=0; [ -n "$add" ] && i=$(printf '%s\n' "$fmt" | grep -cxF -- "$add" || true)
    echo "numstat=${ns:-0/0} in_fmt=$i scope=$(printf '%s\n' "$add" | n '범위 경계') gotcha=$(printf '%s\n' "$add" | n 'plan-prd Gotcha 14') tag=$(printf '%s\n' "$add" | n 'PRD 없음') cols=$(printf '%s\n' "$add" | n "$COLS") argsub=$(printf '%s\n' "$add" | grep -cE '(^|[^\\])[$][0-9]' || true)" ;;
  SC-01) sprint_lines; proj
    echo "lines=$(grep -c . "$T/lines.sh" || true) p1: $(runs "$T/p1")" ;;
  ER-01) sprint_lines; proj
    echo "lines=$(grep -c . "$T/lines.sh" || true) p0: $(runs "$T/p0")" ;;
  AR-01) ch=$(git -C "$W" diff --name-only "$BASE" "$TIP")
    extra=$(printf '%s\n' "$ch" | grep . | grep -vxF -f <(printf '%s\n' "$ALLOWED") | grep -c . || true)
    req=""; for f in "$DM" "$SP" "$SC" "$IR"; do req="$req$(printf '%s\n' "$ch" | grep -cxF "$f" || true)"; done
    multi=0; for c in $(git -C "$W" rev-list "$BASE..$TIP"); do t=$(git -C "$W" show --name-only --format= "$c" | awk -F/ 'NF{print $1}' | sort -u | grep -c .); [ "$t" -gt 1 ] && multi=$((multi + 1)); done
    echo "base=${BASE:0:7} tip=${TIP:0:7} changed=$(printf '%s\n' "$ch" | grep -c . || true) extra=$extra req=$req multi_top=$multi"
    [ "$extra" = 0 ] || printf '%s\n' "$ch" | grep . | grep -vxF -f <(printf '%s\n' "$ALLOWED") ;;
  AR-02) git -C "$W" show "$BASE:$IR" > "$T/ir-base.md"
    rows=0; slug=0; prd=0; same=0; tok=""
    for k in F20 design:P5 backend-family:P1 user-setup:P2 user-setup:P6; do
      r=$(awk -v p="| $k |" 'index($0,p)==1' "$E/$IR"); b=$(awk -v p="| $k |" 'index($0,p)==1' "$T/ir-base.md")
      [ "$(printf '%s\n' "$r" | grep -c . || true)" = 1 ] && rows=$((rows + 1))
      [ "$(printf '%s\n' "$r" | n 'after-0924-discard-decisions')" -ge 1 ] && slug=$((slug + 1))
      [ "$(printf '%s\n' "$r" | n 'PRD 비범위 표')" -ge 1 ] && prd=$((prd + 1))
      [ "$(printf '%s\n' "$r" | awk -F'|' '{print NF}')" = "$(printf '%s\n' "$b" | awk -F'|' '{print NF}')" ] && same=$((same + 1))
      case "$k" in design:P5) tok="$tok p5=$(printf '%s\n' "$r" | n 'design-mockup')" ;; user-setup:P2) tok="$tok p2=$(printf '%s\n' "$r" | n 'Step 0.5')" ;; user-setup:P6) tok="$tok p6=$(printf '%s\n' "$r" | n '세션 인계')" ;; esac
    done
    d=$(git -C "$W" diff -U0 "$BASE" "$TIP" -- "$IR"); keys='^[|] (F20|design:P5|backend-family:P1|user-setup:P2|user-setup:P6) [|]'
    del=$(printf '%s\n' "$d" | grep -cE '^-[^-]' || true); add=$(printf '%s\n' "$d" | grep -cE '^[+][^+]' || true)
    other=$( { printf '%s\n' "$d" | grep -E '^-[^-]' | sed 's/^-//'; printf '%s\n' "$d" | grep -E '^[+][^+]' | sed 's/^+//'; } | grep . | grep -cvE "$keys" || true)
    cb=$(python3 "$E/scripts/check-insights-tracking.py" "$E/$IR" 2>&1); rb=$?; cf=$(python3 "$E/scripts/check-insights-tracking.py" --final "$E/$IR" 2>&1); rf=$?
    echo "rows=$rows slug=$slug prd=$prd cells_same=$same$tok del=$del add=$add other=$other basic=$rb final=$rf counts=[$(printf '%s\n' "$cb" | grep -F 'mode=basic' | sed 's/.*배정: //')]" ;;
  AR-03) b=$(git -C "$W" show "$TIP:$NOTES" 2>/dev/null); c=0; [ -n "$b" ] && c=1; out="committed=$c"
    for k in F1H-41 '판정 표' 'PRD 없음' design-concept visual-change-protocol F20 user-setup:P6 docs/design-kit/design-mockup.html tone-guide; do out="$out $(printf '%s\n' "$b" | n "$k")"; done
    echo "$out" ;;
  AR-04) seal=$(git -C "$W" rev-list --reverse "$BASE..$TIP" -- "$CF" | head -1); sf=0; before=0; same=0
    if [ -n "$seal" ]; then
      sf=$(git -C "$W" show --name-only --format= "$seal" | grep -c . || true)
      fi_=$(git -C "$W" rev-list --reverse "$BASE..$TIP" -- design-kit harness .claude | head -1)
      [ -n "$fi_" ] && [ "$seal" != "$fi_" ] && git -C "$W" merge-base --is-ancestor "$seal" "$fi_" && before=1
      [ "$(git -C "$W" show "$seal:$CF" | digest)" = "$(digest <"$E/$CF")" ] && same=1
    fi
    st=ABSENT; rec=$(fmv conditions_digest "$E/$CF" 2>/dev/null); rec=${rec#sha256:}
    [ -n "$rec" ] && { [ "$rec" = "$(digest <"$E/$CF")" ] && st=OK || st=BROKEN; }
    echo "seal_commit_files=$sf seal_before_impl=$before seal_same_as_tip=$same this=SEAL_$st" ;;
  RE-01) echo "added=$(git -C "$W" diff --diff-filter=A --name-only "$BASE" "$TIP" -- . ':(exclude).harness' | grep -c . || true)" ;;
  RE-02) echo "prd_changed=$(git -C "$W" diff --name-only "$BASE" "$TIP" -- planning-kit | grep -c . || true) hdr=$(n '| 하지 않는 것 | 이유 | 범위 | 코드에 남은 흔적 |' <"$E/$PRD") cols=$(n "$COLS" <"$E/$DM")$(n "$COLS" <"$E/$SC")$(n "$COLS" <"$E/$PRD") ptr=$(n '디자인 승인 기록 · 작업 계약 · 핸드오프는 이 PRD 경로를 가리키고' <"$E/$PRD")" ;;
  DG-01) echo "release_sh=$(git -C "$W" diff --name-only "$BASE" "$TIP" | grep -cx 'scripts/release.sh' || true)" ;;
  DG-03) m DG-01 ;;   # DG-01 과 같은 측정 — commands.test 도 scripts/release.sh 만 잰다
  DG-04) echo "non_md=$(git -C "$W" diff --name-only "$BASE" "$TIP" | grep . | grep -vc '[.]md$' || true)" ;;
  DG-02) mdl_ready || { echo "MDL_NOT_READY"; return; }; tot=0; rows=""
    for f in $(git -C "$W" diff --name-only "$BASE" "$TIP" -- '*.md' ':(exclude).harness/sprint-*.md'); do
      o=$T/old.md; git -C "$W" show "$BASE:$f" > "$o" 2>/dev/null || : > "$o"
      c=$(newmd "$o" "$E/$f"); tot=$((tot + c)); rows="$rows $f=$c"; done
    echo "md_new=$tot |$rows" ;;
  AP-03) python3 "$E/scripts/validate-plugin.py" --check=code-fence >"$T/v6.log" 2>&1; rc=$?; echo "v6_rc=$rc ok=$(n 'code-fence' <"$T/v6.log") fail=$(n 'FAIL' <"$T/v6.log")" ;;
  AP-04) python3 "$E/scripts/validate-plugin.py" --check=frontmatter >"$T/v1.log" 2>&1; rc=$?; echo "v1_rc=$rc ok=$(n 'frontmatter' <"$T/v1.log") fail=$(n 'FAIL' <"$T/v1.log")" ;;
  *) echo "모르는 조건 $1"; return 2 ;;
  esac
}
# === 측정 도우미 끝 ===
```

봉인 전 실측(2026-09-26). 「시작 판」 은 W 에서 가지 끝이 아직 시작점과 같을 때 잰 값이다. 「good」 은 W 를 복제한 임시 사본에 봉인 커밋(가짜 계약) →
`c4d/mock.py` 개선안 → 킷마다 커밋 → notes 커밋을 넣은 판(알려진 답), 「bad」 · 「bad2」 · 「bad3」 은 일부러 망가뜨린 판(양성 대조)이다 —
bad: 킷 둘과 범위 밖 `design-kit/skills/design-concept/SKILL.md`(언어 없는 코드 블록)를 한 커밋 · design-mockup `name:` 줄 삭제 · find 따옴표 빼기 ·
user-setup:P6 행 칸 하나 더 · notes 에 `#bad heading` · 봉인 뒤 조건 문구 변조, bad2: good + F21 행 덧붙임 · sprint-contract 에 `$1` 든 줄 하나 더,
bad3: good + `scripts/x.sh` 새 파일 · `scripts/release.sh` 한 줄.

| 조건 | 시작 판 | good (알려진 답) | 양성 대조 |
| --- | --- | --- | --- |
| SK-01 | `field=1 kind=0 norewrite=0 table=0 gotcha=0 old=1 check=1` | `field=1 kind=1 norewrite=1 table=1 gotcha=1 old=0 check=1` | 시작 판이 실패 값 |
| SK-02 | `all=0 prose=0 planning=0 cols=0 nocreate=0` | `all=1 prose=1 planning=1 cols=1 nocreate=1` | 시작 판이 실패 값 |
| SK-03 | `load=0 rule=0 approvals=1 keep=1` | `load=1 rule=1 approvals=1 keep=1` | 시작 판이 실패 값 |
| SK-04 | `tline=0 none=0 find=0 grep=0 src=0 keep_out=0 old=111111` | `tline=1 none=1 find=1 grep=1 src=1 keep_out=1 old=111111` | 시작 판이 실패 값 |
| SK-05 | `numstat=0/0 in_fmt=0 scope=0 gotcha=0 tag=0 cols=0 argsub=0` | `numstat=1/0 in_fmt=1 scope=1 gotcha=1 tag=1 cols=1 argsub=0` | bad2 `numstat=3/0 in_fmt=2 … argsub=1` |
| SC-01 | `lines=0 p1: bash=out0/prd0/tag0/err0 zsh=out0/prd0/tag0/err0` | `lines=2 p1: bash=out2/prd1/tag1/err0 zsh=out2/prd1/tag1/err0` | bad `zsh=out1/prd0/tag1/err1` |
| ER-01 | `lines=0 p0: bash=out0/prd0/tag0/err0 zsh=out0/prd0/tag0/err0` | `lines=2 p0: bash=out0/prd0/tag0/err0 zsh=out0/prd0/tag0/err0` | bad `zsh=out0/prd0/tag0/err1` |
| AR-01 | `base=f81568d tip=f81568d changed=0 extra=0 req=0000 multi_top=0` | `changed=6 extra=0 req=1111 multi_top=0` | bad `changed=7 extra=1 req=1111 multi_top=1` + `design-kit/skills/design-concept/SKILL.md` · bad3 `extra=2` |
| AR-02 | `rows=5 slug=0 prd=0 cells_same=5 p5=0 p2=0 p6=0 del=0 add=0 other=0 basic=0 final=0 counts=[Phase 74 · 이번 스프린트 16 · 해당 없음 6]` | `rows=5 slug=5 prd=5 cells_same=5 p5=1 p2=1 p6=1 del=5 add=5 other=0 basic=0 final=0` 같은 요약 | bad `cells_same=4 basic=2 final=2 counts=[… 해당 없음 5]` · bad2 `del=6 add=6 other=2` |
| AR-03 | `committed=0 0 0 0 0 0 0 0 0 0` | `committed=1 1 1 1 1 1 1 1 1 1` | 시작 판이 실패 값 |
| AR-04 | `seal_commit_files=0 seal_before_impl=0 seal_same_as_tip=0 this=SEAL_ABSENT` | `seal_commit_files=1 seal_before_impl=1 seal_same_as_tip=1 this=SEAL_OK` | bad `seal_commit_files=1 seal_before_impl=1 seal_same_as_tip=0 this=SEAL_BROKEN` |
| RE-01 · RE-02 | `added=0` · `prd_changed=0 hdr=3 cols=001 ptr=1` | `added=0` · `prd_changed=0 hdr=3 cols=111 ptr=1` | bad3 `added=1` |
| DG-01 · DG-04 | `release_sh=0` · `non_md=0` | `release_sh=0` · `non_md=0` | bad3 `release_sh=1` · `non_md=2` |
| DG-02 | `md_new=0` (바뀐 파일 없음) | `md_new=0` (다섯 파일 각 0) | bad `md_new=1` (notes) |
| AP-03 · AP-04 | `v6_rc=0 ok=14 fail=0` · `v1_rc=0 ok=14 fail=0` | 같음 | bad `v6_rc=2 fail=2` · `v1_rc=2 fail=2` |
| DG-05 (ci-local) | `rc=0` 22 · `feedback-agg-test SKIP (yq 없음)` 한 줄 | 같음 (good 사본에 W 의 `node_modules` 를 이어 붙여 실행) | bad 전체 `validate-plugin.py` 종료 코드 2 |

측정 준비 단계도 봉인 전에 돌렸다: `command -v zsh` → `/bin/zsh`, markdownlint-cli2 0.23.2 설치본(`MDL` 기본 경로) 있음, `shasum` 있음,
`python3 scripts/check-insights-tracking.py` 기본 · `--final` 종료 코드 0.

## Skill

- [ ] SK-01: 승인 기록 폐기 칸이 기능·설정 항목을 버린 결정을 다시 적지 않고 PRD 비범위 표를 가리킨다 — Given 구현 커밋이 가지 `chore/ak-c4d` 에 들어간 뒤, When design-mockup 의 `## Step 6:` 절(다음 `## Step 7:` 앞까지)을 읽으면, Then (a) `- 폐기한 대안·이유:` 로 시작하는 틀 줄이 1 줄이고 그 한 줄에 `기능·설정 항목` · `다시 쓰지 않는다` · `비범위 표` · `plan-prd Gotcha 14` 가 모두 있다 (b) 옛 자리표시자 글 `이번 결정에서 버린 안·요소와 이유` 가 파일 전체에 0 줄이다 (c) 확인 명령 줄 `grep -cE '^- (확정 구성|폐기한 대안·이유):'` 이 절 안에 그대로 1 줄이다(칸 이름을 바꾸지 않아 `→ 2` 와 `evals.json:539` 가 산다). 측정: `m SK-01` 이 `field=1 kind=1 norewrite=1 table=1 gotcha=1 old=0 check=1` (시작 판 `field=1 kind=0 norewrite=0 table=0 gotcha=0 old=1 check=1`, good 은 기대값 그대로) [exact]
- [ ] SK-02: 가리킬 PRD 가 없는 프로젝트의 대체가 Step 6 에 산문 한 줄로 있다 — Given 구현 커밋 뒤, When `## Step 6:` 절을 읽으면, Then `PRD 없음` 이 든 줄이 절 전체에서 1 줄이고 그 줄이 코드 블록 밖에 있으며, 그 한 줄에 `.planning/prd-*.md` · `하지 않는 것 · 이유 · 범위 · 코드에 남은 흔적` · `PRD 를 만들지 않는다` 가 모두 있다. 측정: `m SK-02` 가 `all=1 prose=1 planning=1 cols=1 nocreate=1` (시작 판 다섯 값 0, good 은 기대값 그대로) [exact]
- [ ] SK-03: design-mockup Step 2 가 PRD 비범위 표를 읽는다(읽는 쪽) — Given 구현 커밋 뒤, When `## Step 2:` 절(다음 `## Step 3:` 앞까지)을 읽으면, Then (a) 코드 블록 안에 `.planning/prd-*.md` 로 시작하고 `폐기한 결정` 이 든 줄이 1 줄 (b) 코드 블록 밖에 `- PRD 비범위 표 존재 →` 로 시작하고 `묻는다` 가 든 줄이 1 줄 (c) 기존 두 줄 — 감지 대상 `.design/approvals/*.md      → 같은 화면의 확정 구성 · 폐기한 대안 로드` 와 규칙 `- 승인 기록 존재 → 확정 구성을 지키고, 폐기한 대안·요소는 사용자가 되살리라고 하지 않는 한 시안에 다시 넣지 않는다` — 이 글자 그대로 각 1 줄이다. 측정: `m SK-03` 이 `load=1 rule=1 approvals=1 keep=1` (시작 판 `load=0 rule=0 approvals=1 keep=1`, good 은 기대값 그대로) [exact]
- [ ] SK-04: `/sprint` 재검증 블록에 폐기 결정 자리가 있다(F1H-41 뒷절반 · user-setup:P2) — Given 구현 커밋 뒤, When `harness/skills/sprint/SKILL.md` 의 `### Step 0.5:` 절(다음 `### Step 1:` 앞까지)을 읽으면, Then (a) text 코드 블록에 `- 폐기한 결정:` 로 시작하는 줄이 1 줄이고 그 줄에 `없음` 이 있다 (b) bash 코드 블록에 `find .planning -maxdepth 1 -type f -name 'prd-*.md'` 가 든 줄 1 · `grep -rn 'PRD 없음' .design .harness` 가 든 줄 1 (c) 코드 블록 밖 한 줄에 `## Non-goals (폐기한 결정 포함)` · `## No-gos` · `plan-prd Gotcha 14` 가 함께 있고, 코드 블록 밖에 `다시 넣지 않는다` 가 든 줄이 1 줄 이상 (d) 기존 text 세 줄(`- 문서 주장 잔여:` · `- git 실측:` · `- 불일치:`)과 bash 세 명령(`git log --oneline` · `git status --short` · `git diff --stat`)이 각 1 줄 그대로다. 측정: `m SK-04` 가 `tline=1 none=1 find=1 grep=1 src=1`, `keep_out` 1 이상, `old=111111` (시작 판 `tline=0 none=0 find=0 grep=0 src=0 keep_out=0 old=111111`, good 은 `keep_out=1` 로 기대값 안) [exact]
- [ ] SK-05: sprint-contract 에는 한 줄만 더하고, 그 줄이 폐기 결정을 같은 표로 가리킨다 — Given 구현 커밋 뒤, When 시작점 `BASE` 부터 끝점 `TIP` 까지(AR-01 과 같은 해석) `harness/skills/sprint-contract/SKILL.md` 의 차이를 보면, Then 더한 줄 1 · 지운 줄 0 이고(다른 세션이 곧 고칠 파일이라 한 줄만), 그 줄이 끝 판의 `**포맷 규칙` 줄과 `### 6.2.` 줄 사이에 있으며, `범위 경계` · `plan-prd Gotcha 14` · `PRD 없음` · `하지 않는 것 · 이유 · 범위 · 코드에 남은 흔적` 을 모두 담고, 역슬래시 없는 `$`+숫자가 0 이다(스킬 본문 인자 치환, validate-plugin V9). 측정: `m SK-05` 가 `numstat=1/0 in_fmt=1 scope=1 gotcha=1 tag=1 cols=1 argsub=0` (시작 판 `numstat=0/0 in_fmt=0 scope=0 gotcha=0 tag=0 cols=0 argsub=0`, good 은 기대값 그대로). 양성 대조: bad2 에서 `numstat=3/0 in_fmt=2 argsub=1` (봉인 전 실측) [exact]

## Script

- [ ] SC-01: `/sprint` 재검증의 새 명령이 알려진 답 입력에서 폐기 결정을 모은다 — Given Step 0.5 bash 블록에서 `.planning` 이나 `PRD 없음` 이 든 줄만 떼어 낸 파일과 알려진 답 폴더 p1(`.planning/prd-alarm.md` · 걸리면 안 되는 `.planning/discover-alarm.md` · `PRD 없음` 이 든 줄 하나짜리 `.design/approvals/20260926-home.md` · 표시가 없는 `.harness/other.md`), When 그 파일을 p1 에서 bash 와 zsh 로 각각 돌리면, Then 떼어 낸 줄이 2 줄이고 두 셸 모두 출력 2 줄(PRD 경로 1 줄 · `PRD 없음` 줄 1 줄) · 오류 출력 0 줄이다. 측정: `m SC-01` 이 `lines=2 p1: bash=out2/prd1/tag1/err0 zsh=out2/prd1/tag1/err0` (시작 판 `lines=0` 이고 출력 0 — 뗄 줄이 없다. good 은 기대값 그대로). 알려진 답: 입력 p1 은 PRD 하나 · 표시 줄 하나라 손으로 센 답이 출력 2 줄이고 봉인 전 good 실제값도 2 · 종료 코드 0. 음성 대조: find 의 `'prd-*.md'` 따옴표를 빼면(bad) zsh 가 `no matches found` 로 그 줄을 못 돌려 `zsh=out1/prd0/tag1/err1` (봉인 전 실측) [exact]

## Error

- [ ] ER-01: 폐기 기록이 하나도 없는 빈 프로젝트에서 새 명령이 조용하다 — Given SC-01 과 같이 떼어 낸 줄(2 줄이어야 한다 — 0 줄이면 잴 것이 없으니 실패)과 빈 폴더 p0(`.planning` · `.design` · `.harness` 없음), When bash 와 zsh 로 p0 에서 돌리면, Then 두 셸 모두 출력 0 줄 · 오류 출력 0 줄이다 — 폴더가 없어도 오류 줄로 재검증 보고를 어지럽히지 않는다. 측정: `m ER-01` 이 `lines=2 p0: bash=out0/prd0/tag0/err0 zsh=out0/prd0/tag0/err0` (시작 판 `lines=0` 이라 전제가 안 서서 실패, good 은 기대값 그대로). 양성 대조: bad(따옴표 없는 find)에서 `zsh=out0/prd0/tag0/err1` (봉인 전 실측) [exact]

## Architecture

- [ ] AR-01: 바뀐 파일이 기대 집합 안이고 한 커밋에 맨 위 폴더 하나다 — Given 구현 · notes · QA 리포트 커밋이 모두 가지 `chore/ak-c4d` 에 들어간 뒤, 시작점 `BASE=$(git -C W merge-base origin/main chore/ak-c4d)` 부터 끝점 `TIP=$(git -C W rev-parse --verify chore/ak-c4d)` 까지(`HEAD` 를 쓰지 않는다. 해석이 안 되면 `UNRESOLVED` 로 멈춘다) `git diff --name-only` 로 모은 경로가 측정 도우미 `ALLOWED` 의 여덟 경로 안에만 있고(부분 집합 — 생성물이 없는 묶음이라 제외 pathspec 이 없다), 대상 넷 `design-kit/skills/design-mockup/SKILL.md` · `harness/skills/sprint/SKILL.md` · `harness/skills/sprint-contract/SKILL.md` · `.claude/kaizen-input/insights-report.md` 가 각각 들어 있으며, 커밋마다 맨 위 폴더가 하나뿐이다(`design-kit` · `harness` · `.claude` · `.harness` 가운데 하나). 측정: `m AR-01` 이 `extra=0 req=1111 multi_top=0` (시작 판 `changed=0 extra=0 req=0000 multi_top=0`, good `changed=6 extra=0 req=1111 multi_top=0`). 양성 대조: bad 에서 `extra=1 multi_top=1` 과 남는 경로 `design-kit/skills/design-concept/SKILL.md` 출력, bad3 에서 `extra=2` (봉인 전 실측) [exact, collective]
- [ ] AR-02: 처리 배정표 다섯 행에 결정과 처리 결과가 들어가고 다른 행 · 표 모양은 그대로다 — Given 끝점 `TIP`, When 다섯 키 `F20` · `design:P5` · `backend-family:P1` · `user-setup:P2` · `user-setup:P6` 의 행을 끝 판과 시작 판에서 읽으면, Then 키마다 행이 정확히 1 줄이고, 다섯 행 모두 `after-0924-discard-decisions` 와 `PRD 비범위 표` 를 담으며, design:P5 행에 `design-mockup`, user-setup:P2 행에 `Step 0.5`, user-setup:P6 행에 `세션 인계` 가 있고, 다섯 행의 `|` 개수가 시작 판과 같으며, 이 파일의 차이가 지운 줄 5 · 더한 줄 5 이고 다섯 키 행이 아닌 차이 줄이 0 이며, `python3 scripts/check-insights-tracking.py` 기본 · `--final` 둘 다 종료 코드 0 이고 배정 요약이 `Phase 74 · 이번 스프린트 16 · 해당 없음 6` 그대로다. 측정: `m AR-02` 가 `rows=5 slug=5 prd=5 cells_same=5 p5=1 p2=1 p6=1 del=5 add=5 other=0 basic=0 final=0 counts=[Phase 74 · 이번 스프린트 16 · 해당 없음 6]` (시작 판 `rows=5 slug=0 prd=0 cells_same=5 p5=0 p2=0 p6=0 del=0 add=0 other=0 basic=0 final=0` 같은 요약, good 은 기대값 그대로). 양성 대조: bad(칸 하나 더) `cells_same=4 basic=2 final=2`, bad2(F21 행 덧붙임) `del=6 add=6 other=2` (봉인 전 실측) [exact, enumerated]
- [ ] AR-03: 결정과 넘김을 notes 에 남긴다 — Given 끝점 `TIP`, notes 파일 `.harness/.meta/after-kaizen-0926/c4d-notes.md` 가 커밋돼 있고 아홉 토큰 `F1H-41` · `판정 표` · `PRD 없음` · `design-concept` · `visual-change-protocol` · `F20` · `user-setup:P6` · `docs/design-kit/design-mockup.html` · `tone-guide` 가 각 1 줄 이상이다. 담을 내용: 넘긴 것(F1H-41 앞절반 Step 3 판정 표 · PRD 가 나중에 생겼을 때 `PRD 없음` 줄을 옮기는 절차 · 옛 글이 된 문서 페이지)과 사유, 이 계약의 판단(design-concept · visual-change-protocol §4 를 그대로 둔 이유 · F20 행을 더한 이유 · design-mockup Step 2 읽기 줄), user-setup:P6 이 세션 인계용 절로 따로 남는다는 것, tone-guide 5 단계 대조 결과. 측정: `m AR-03` 이 `committed=1` 과 1 이상 아홉 (시작 판 `committed=0` 과 0 아홉, good `committed=1` 과 1 아홉) [exact, enumerated]
- [ ] AR-04: 봉인 커밋이 계약 한 파일이고 구현보다 먼저이며 봉인 뒤 조건이 그대로다 — Given 끝점 `TIP`, When 시작점..끝점 구간에서 이 계약 파일을 처음 담은 커밋을 찾으면, Then 그 커밋의 파일이 1 개이고, `design-kit` · `harness` · `.claude` 를 처음 건드린 구현 커밋의 조상이며(같은 커밋이 아니다), 그 커밋 판 계약과 끝 판 계약의 조건 줄 지문(체크 상태를 정규화한 sha256 앞 16 자리)이 같고, 끝 판 계약의 `conditions_digest` 가 그 지문과 같다(`SEAL_OK`). 측정: `m AR-04` 가 `seal_commit_files=1 seal_before_impl=1 seal_same_as_tip=1 this=SEAL_OK` (시작 판 `seal_commit_files=0 seal_before_impl=0 seal_same_as_tip=0 this=SEAL_ABSENT`, good 은 기대값 그대로). 양성 대조: bad(봉인 뒤 조건 문구 변조)에서 `seal_same_as_tip=0 this=SEAL_BROKEN` (봉인 전 실측) [exact]

## Anti-patterns

- [ ] AP-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수 (```text, ```bash, ```yaml 등). 판정 권위는 validate-plugin V6 상태기계다 — 여는/닫는 fence 가 동형이라 줄 단위 정규식으로는 판정 불가. 측정: 끝 판을 풀어 둔 `E` 에서 `m AP-03` 이 `v6_rc=0 fail=0` (시작 판 `v6_rc=0 ok=14 fail=0`). 양성 대조: bad(design-concept 끝에 언어 없는 fence)에서 `v6_rc=2` (봉인 전 실측)
- [ ] AP-04: SKILL.md / agents/*.md frontmatter 에서 name 필드 누락 — validate-plugin V1 FAIL. 측정: `m AP-04` 가 `v1_rc=0 fail=0` (시작 판 `v1_rc=0 ok=14 fail=0`). 양성 대조: bad(design-mockup `name:` 줄 삭제)에서 `v1_rc=2` (봉인 전 실측)

## Reusability

- [ ] RE-01: N/A (산출물이 스킬 문서 문장 · 문서 안 명령 두 줄 · 표 비고뿐이라 새 컴포넌트 · 함수 · 모듈이 없다. 측정: `m RE-01` 이 `added=0` — 구간이 `.harness/` 밖에 더한 새 파일 수. 시작 판 0. 양성 대조: bad3 에서 `added=1`)
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다 — 폐기 기록의 새 형식 · 새 파일을 만들지 않고 plan-prd 비범위 표의 네 칸 이름을 그대로 쓴다: 원문 표가 있는 planning-kit 은 바뀌지 않고(세 틀의 머리 줄 `| 하지 않는 것 | 이유 | 범위 | 코드에 남은 흔적 |` 3 줄 그대로 · Gotcha 14 의 「디자인 승인 기록 · 작업 계약 · 핸드오프는 이 PRD 경로를 가리키고」 1 줄 그대로), 네 칸 이름 `하지 않는 것 · 이유 · 범위 · 코드에 남은 흔적` 이 design-mockup · sprint-contract · plan-prd 에 각 1 줄이다. 측정: `m RE-02` 가 `prd_changed=0 hdr=3 cols=111 ptr=1` 이고 `m RE-01` 이 `added=0` (시작 판 `prd_changed=0 hdr=3 cols=001 ptr=1`, good 은 기대값 그대로)

## Diagnostics

- [ ] DG-01: N/A (`commands.analyze` 는 `bash -n scripts/release.sh` 라 `scripts/release.sh` 만 잰다 — 이번 바뀐 파일과 교집합 0 개. 측정: `m DG-01` 이 `release_sh=0`. 양성 대조: bad3 에서 `release_sh=1`. 실제 검사는 DG-02 · DG-05)
- [ ] DG-02: IDE diagnostics 워닝/인포 0개 ([] 제외) — IDE(편집기) 진단을 명령줄로 같게 잰다: 바뀐 `.md`(계약 · QA 리포트 · 개정 파일 `.harness/sprint-*.md` 제외)의 더해진 줄에 걸린 markdownlint-cli2 0.23.2(MD013 끔, 편집기 확장과 같은 설정) 경고가 0 이다. 측정: `m DG-02` 가 `md_new=0` (시작 판 `md_new=0` — 바뀐 파일이 없다, good `md_new=0` 다섯 파일 각 0). 양성 대조: bad(notes 에 `#bad heading`)에서 `md_new=1` (봉인 전 실측)
- [ ] DG-03: N/A (`commands.test` 는 `bash scripts/release.sh 2>&1 || true` 라 `scripts/release.sh` 만 잰다 — 교집합 0 개. 측정: `m DG-03` 이 `release_sh=0` — 도우미 안에서 `m DG-01` 을 그대로 부른다. 양성 대조: bad3 에서 `release_sh=1`)
- [ ] DG-04: N/A (구동할 앱 · 서버가 없다 — 바뀐 파일이 모두 `.md` 라 실행 진입점 0 개. 측정: `m DG-04` 가 `non_md=0`. 양성 대조: bad3 에서 `non_md=2`. 저장소 검사는 DG-05)
- [ ] DG-05: CI(자동 검사) 단계를 로컬에서 전부 돌려 통과한다 — Given 작업 폴더 W 가 끝점과 같다(`git -C W rev-parse HEAD` 가 `TIP` 이고 `git -C W status --porcelain --untracked-files=no` 가 빈 출력), When `PYTHONDONTWRITEBYTECODE=1 TMPDIR=<임시 폴더> bash /Users/jackson/Hub/10_Dev/claude-plugins/.harness/handoff/2026-09-26-tools/ci-local.sh /Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak-c4d` 를 돌리면, Then 요약 `$TMPDIR/ci-local/summary.txt` 에 `rc=0` 줄이 22 개이고 `rc=0` 이 아닌 줄은 `feedback-agg-test SKIP (yq 없음)` 하나뿐이다. 측정: `grep -c 'rc=0' "$TMPDIR/ci-local/summary.txt"` 가 22 · `grep -v 'rc=0' "$TMPDIR/ci-local/summary.txt"` 가 그 한 줄 (시작 판 봉인 전 실측: 22 · SKIP 한 줄, good 사본도 22 · SKIP 한 줄). 음성 대조: 이 묶음이 깨뜨릴 수 있는 단계는 `validate-plugin` 이다 — bad 에서 `python3 scripts/validate-plugin.py` 종료 코드 2 (봉인 전 실측)
