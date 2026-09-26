---
feature: "문서 사이트 후속 (c3b) — kaizen-flow 17 Phase · 원본 담김 낮은 세 쪽 · 글자 간격 넘침 일곱 쪽"
slug: after-0924-docs-site
created: "2026-09-26 13:41"
complexity: "복잡"
conditions: 29
status: active
owner_session: bda55d45-296c-491f-89ba-b52042d58e72
conditions_digest: sha256:49e805fabb7bdb20
locked_at: "2026-09-26 14:08"
---

## 배경

2026-09-24 카이젠이 다음 사이클로 넘긴 문서 사이트 몫 세 갈래를 한 계약으로 묶는다.
근거 원문은 `.harness/handoff/2026-09-26-0110.md` §C3 「문서 사이트」 줄(본 체크아웃, 읽기만)과 이 가지의
`.harness/.meta/kaizen-0924/final-notes.md` 「다음 사이클 메모」 (FN-80) · 「교차 진단 2 회차 뒤 보강」 절이다.

- 사용자 합의(Step 5): 사용자 위임으로 받은 것으로 적는다 — user 2026-09-26T01:04:21.505Z 「다음 세션에서 직접할 일을 다 실행하고 이어질것도 실행해」
  (세션 기록 `/Users/jackson/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/de8c7935-a5b6-4df5-9106-fafa73c288a0.jsonl`),
  그 앞의 「나한테 물어보지 말고 자동으로 끝까지」(2026-09-24T04:04:16.964Z). 판단이 갈린 곳은 저장소 안 근거로 정했고 `## 범위 경계` 에 적었다.
- 작업 폴더 W = `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak-c3b`, 가지 `chore/ak-c3b-docs-site`, 시작점 `f81568d`(origin/main #110 판, 지금 origin/main `88ddfe5` 와의 갈림점).
- 커밋 규칙: `git add <경로>` 뒤 `git commit -o <경로>` · 페이지마다 한 커밋 · `.harness/` 파일은 페이지와 다른 커밋 · `git add -A` · `git stash` · push · 가지 바꾸기 금지.
- 구현 전에 `tone-kit:tone-guide` 1 단계(규칙 불러오기)를, 완료 선언 전에 5 단계(전수 대조)를 한다 — 페이지 글도 한국어 기술 문체 규칙 대상이다. 대조 결과는 notes 에 남긴다(AR-02).
- 사용자가 할 일: 없음.

공통 전제 G (조건마다 되풀이하지 않는다) — 구현 · notes 커밋이 가지 `chore/ak-c3b-docs-site` 에 모두 들어간 뒤, 가지를 main 에 합치기 전에 잰다.
측정은 `## 회귀 게이트` 의 측정 도우미 `m <조건 ID>` 로 하며, 도우미는 끝점 `TIP`(가지 끝)과 시작점 `BASE`(origin/main 과의 갈림점)를 `git archive` 로 풀어 잰다 — 작업 폴더의 커밋 안 된 변경은 보지 않는다.
`HEAD` 를 상한으로 쓰지 않는다. `BASE` · `TIP` 해석이 안 되면 도우미가 `UNRESOLVED` 를 찍고 멈춘다.
측정 기준점으로 쓰는 페이지 글은 바꾸지 않는다: kaizen-flow 의 절 이름표 「실행 흐름」 · 「공통 실행 패턴」 · 「타임라인」 · 「시뮬레이션」, 흐름 카드 이름표 꼴 `PHASE N · <이름>` 과 `FINAL`, 시뮬레이터 시작 단추 이름 「시뮬레이션 시작」, 시뮬레이터가 끝에 찍는 `사이클 완료`.
단, 「타임라인」 절을 통째로 뺄지는 구현 재량이다 — 빼면 그 절에는 이름표 유지 제약이 걸리지 않고 SK-07 이 `section=absent` 로 잰다. 남기면 이름표를 바꾸지 않는다.
원본이 봉인 때 판에서 바뀌었는지는 도우미가 `orch_same` · `tool_same` 으로 찍는다 — 0 이면 평가자는 그 조건의 판정을 멈추고 바뀐 사실을 보고한다(이 계약이 손대지 않은 파일의 변경으로 결과가 흔들리지 않게 한다).

복잡도 4 축 — 둘이 「예」 라 최소 「중간」 이다. 세 갈래 · 11 쪽 · 페이지 안 시뮬레이터 스크립트 재작성이 겹쳐 기능 조건이 20 개(DG-05 포함)라 「복잡」 으로 둔다.
Step 2.5 짝 조건: 소비자 쪽은 첫 화면 `docs/index.html` 의 등록 · 링크다 — 경로 · 제목을 바꾸지 않으므로 그대로인지만 AR-03 이 잰다.

| 축 | 물음 | 값 |
| -- | ---- | -- |
| 레이어 수 | 몇 개 계층을 관통하는가 | 하나 — 정적 문서 화면(HTML · CSS · 페이지 안 스크립트) |
| 공개 API·계약 변경 | 외부에 노출된 약속이 바뀌는가 | 아니오 — 페이지 경로 · 첫 화면 등록 id · 제목을 그대로 둔다 |
| 소비면 존재 | 반대편이 있는가 | 예 — `docs/index.html` 내비 등록 176 · 내부 링크 507 개가 이 페이지들을 가리킨다 |
| 회귀 위험 | 기존 동작이 깨질 수 있는가 | 예 — 다시 쓴 페이지가 원본 글을 잃거나, 레이아웃을 고치다 다른 폭에서 넘치거나, 시뮬레이터가 멈출 수 있다 |

설정 값 대조 (`.harness/project.yaml` 을 글자 그대로 옮김):

| config key | project.yaml 에서 읽은 값 | 계약에 쓴 값 |
| ---------- | ------------------------- | ------------ |
| `commands.analyze` | `bash -n scripts/release.sh` | DG-01 N/A — 재는 파일이 바뀐 파일에 없다 |
| `commands.test` | `bash scripts/release.sh 2>&1 \|\| true` | DG-03 N/A — 같은 이유 |
| `diagnostics.ide_exclude` | `[]` | DG-02 의 `([] 제외)` |
| `contract_categories[].id` / `prefix` | Skill/SK · Script/SC · Error/ER · Architecture/AR | 같은 넷 |
| `anti_patterns[].id` / `message` | AP-01 버전 하드코딩 · AP-02 force push · AP-03 bare code fence · AP-04 frontmatter name 누락 | AP-01 · AP-03 (다시 쓰는 페이지 글과 새 notes 에 걸릴 수 있다). AP-02 는 이 계약이 push 하지 않아서, AP-04 는 SKILL.md · 에이전트 파일을 안 건드려서 뺐다 |

## GAP 분석 (Pre-Edit Audit)

대상 파일을 실제로 읽고 잰 값이다(시작 판 `f81568d`). 측정은 도우미와 같은 식이다.

| 대상 파일 | 실제 Read 증거 (`파일:라인`) | 발견한 기존 갭·위반 | 계약 조건화 |
| --------- | ---------------------------- | ------------------- | ----------- |
| `docs/process/kaizen-flow.html` (819 줄) | `:173` 부제 「9-Phase 카이젠 사이클」 · `:185` 「→8→9→Final」 · `:206` 「9개 Phase」 · `:242` 「9-Phase 실행 순서」 · `:260` 「Phase 2~6의 기준」 · `:443-463` 마지막 카드가 PHASE 9 · `:471` 「Phase 4-9 반영」 · `:473` 「9개 Phase 정합성」 · `:494-503` 타임라인이 P1 ~ P6 · Final · `:544` 시뮬레이션 안내 9-Phase · `:563-575` 호출 문법이 phase9 까지 · `:781` 로그 「↔9 정합성」 · `:787` 버전 올림 로그가 킷 여섯 | 원본은 17 Phase + Final. 앞 단계(Step 0 · 0.5 · 0.6)와 Final 네 걸음(F1 ~ F4) 이름이 둘뿐(`전체 정합성 검증` · `PR 생성`). 공통 실행 패턴 7 걸음 — 원본은 10 걸음과 동시 3 개 제한 | SK-01 ~ SK-08 · SK-12 |
| `.claude/skills/kaizen-orchestrator/SKILL.md` (807 줄, 원본 — 고치지 않는다) | `:9` `argument-hint` 18 인자 · `:61-105` 「Phase 의존성」 블록 Phase 1 ~ 17 · Final · `:177-197` 공통 실행 패턴 10 걸음 · `:195` 「동시에 도는 킷 Phase 는 3 개까지」 · `:207` · `:341` · `:367` Step 0 · 0.5 · 0.6 · `:577` · `:603` · `:643` · `:665` · `:715` Step F1 ~ F4 | 페이지 원본이 docs-site 매핑 표에 「(내부 문서)」 로만 적혀 있다(`:629`) — 이 계약은 이 파일을 원본으로 삼는다 | SK-01 ~ SK-04 · SK-08 · SK-12 가 여기서 값을 뽑는다 |
| `docs/onboarding-kit/setup-guide.html` · 원본 `onboarding-kit/skills/setup-guide/SKILL.md` (289 줄) | 원본 `:50-124` `guide_gate` 함수 블록 · `:242-248` `STACK` 반복 블록 | 원본 코드 블록 줄 61 가운데 페이지에 1 줄 (`fen lines=61 in_new=1`). 코드 표시 81 가운데 68 · 낱말 비율 0.55 | SK-09 |
| `docs/design-kit/design-concept.html` · 원본 `design-kit/skills/design-concept/SKILL.md` (240 줄) | 원본 코드 블록 `:25-27` · `:31-33` · `:37-46` · `:72-81` · `:94-99` · `:145-181` · `:211-221` · `:225-229` | 코드 블록 줄 47 가운데 3 (카이젠 기록의 「52 줄」 은 그때 원본 값이다 — 지금 47) · 코드 표시 29 가운데 16 · 낱말 비율 0.44 | SK-10 |
| `docs/design-kit/design-mockup.html` · 원본 `design-kit/skills/design-mockup/SKILL.md` (187 줄) | 원본 코드 블록 `:54-60` · `:134-138` · `:150-162` · `:166-170` | 코드 블록 줄 20 가운데 15 — 빠진 다섯은 승인 기록 틀 줄과 `grep -c '확정된 시각 값'` 줄 등. 다른 세션 c4d 가 이 원본 Step 2 를 고칠 예정(`ak-c4d` 계약 `:82`) | SK-11 |
| `docs/backend-kit/api-lifecycle.html` (662 줄) | `:137-139` `.grid-2` 가 `repeat(auto-fit, minmax(420px, 1fr))` · `:143` `.card` | +0.06em · 375px 에서 7px 넘침. 넘친 것은 `.grid-2` 안 `.card`(오른쪽 끝 382) | ER-01 · ER-04 |
| `docs/design-kit/typography-scale.html` (834 줄) | `:73` `.table-wrap{overflow-x:auto…}` · `:83` `.grid-2{…repeat(2,1fr)}` | 15px 넘침. 표(오른쪽 끝 518)가 `1fr` 트랙을 밀어 넓힌다 | ER-01 · ER-04 |
| `docs/flutter-toolkit/theming.html` (310 줄) | `:62` `.cards{…minmax(340px,1fr)}` | 21px 넘침. 표(435) | ER-01 · ER-04 |
| `docs/rust-kit/grpc-tonic.html` (498 줄) | `:93` `.grid-2` · `:103` `pre{` | 19px 넘침. 표(587) | ER-01 · ER-04 |
| `docs/rust-kit/observability.html` (447 줄) | `:47` `.grid-2` · `:50` `pre{…overflow-x:auto…}` | 9px 넘침. 표(515) | ER-01 · ER-04 |
| `docs/rust-kit/ownership-borrowing.html` (330 줄) | `:42-44` `.grid-2` ~ `.grid-4` | 20px 넘침. `pre` 안 줄(494)과 `.compare-bad` · `.compare-good`(390) | ER-01 · ER-04 |
| `docs/rust-kit/project-structure.html` (337 줄) | `:48-49` `.compare{grid-template-columns:1fr 1fr}` · 640px 이하 `1fr` | 21px 넘침. `pre` 안 주석 줄(457) | ER-01 · ER-04 |
| 문서 전체 `docs/**/*.html` 177 쪽 | 도우미 `lsover` 로 전부 잼 | +0.06em · 375px 에서 넘치는 쪽이 정확히 위 일곱(`over=7/177`) — 핸드오프 목록과 같다 | ER-02 |

구현 후보는 하나로 정해져 있다 — 과제가 「수치 말고 구조로」(`grid-template-columns:minmax(0,1fr)` · `overflow-wrap:anywhere`)를 정했다. 옵션 표를 따로 두지 않는다.

## Skill

- [ ] SK-01: 「실행 흐름」 절이 원본 오케스트레이터의 Phase 17 개를 차례대로 보이고 그 뒤에 Final 이 온다 — Given 공통 전제 G, When 도우미가 kaizen-flow 페이지를 1280px 로 열어 절 이름표 「실행 흐름」 인 절의 글에서 카드 이름표 `PHASE N` 을 차례로 모으면, Then 번호 차례가 원본 「Phase 의존성」 블록의 `Phase N:` 줄 차례(1 ~ 17)와 같고, 카드 구간마다 그 줄의 이름(설계 가이드 · Contract · Evaluator · Harness · Flutter-toolkit … Howto-kit, 대소문자 무시)이 들고, 마지막 `PHASE` 뒤에 `FINAL` 이 있다. 측정: `m SK-01` 이 `seq_ok=1 n=17 names=17/17 final_after=1` · `orch_same=1` (시작 판 `seq_ok=0 n=9 names=9/17 final_after=1`). 알려진 답: 원본에서 뽑은 이름으로 만든 모의 좋은 판 → `seq_ok=1 n=17 names=17/17 final_after=1` (봉인 전 실측) [exact, enumerated]
- [ ] SK-02: 원본 「Phase 의존성」 블록 괄호 안의 카이젠 스킬 이름 16 개(`contract-kaizen` 부터 `howto-kaizen` 까지 — 도우미가 원본에서 뽑는다)가 kaizen-flow 페이지의 보이는 글(스크립트 · 스타일 밖)에 모두 든다. 측정: `m SK-02` 가 `skills=16/16` · `orch_same=1` (시작 판 `skills=8/16`, 빠진 것 `react-kaizen` · `planning-kaizen` · `reflect-kaizen` · `bambu-kaizen` 등). 알려진 답: 모의 좋은 판 `skills=16/16` (봉인 전 실측) [exact, enumerated]
- [ ] SK-03: 호출 문법 — 원본 머리 설정 `argument-hint` 의 인자 18 개(`phase1` ~ `phase17` · `final`, 도우미가 원본에서 뽑는다)마다 kaizen-flow 페이지 보이는 글에 `/kaizen-orchestrator <인자>` 가 있다(`phase1` 이 `phase10` 에 먹히지 않게 인자 바로 뒤 글자가 숫자 · 영문이 아니어야 한다). 측정: `m SK-03` 이 `invoke=18/18` · `orch_same=1` (시작 판 `invoke=10/18`). 알려진 답: 모의 좋은 판 `invoke=18/18` (봉인 전 실측) [exact, enumerated]
- [ ] SK-04: 원본의 앞 단계 셋과 Final 단계 다섯의 이름 여덟이 kaizen-flow 페이지 보이는 글에 모두 든다 — `피드백 데이터 풀 수집` · `Orchestrator Self-Audit` · `Phase Relevance Triage` · `전체 정합성 검증` · `docs-site 재생성` · `글로벌 피드백 정리` · `메모리 승격 후보 산출` · `PR 생성` (여덟 모두 원본 `### Step 0` · `0.5` · `0.6` · `F1` · `F2` · `F3` · `F3.5` · `F4` 제목에 있는 글자). 측정: `m SK-04` 가 `steps=8/8 src=8/8` · `orch_same=1` (시작 판 `steps=2/8 src=8/8`. `src` 는 여덟이 끝점 원본에 아직 있는지다 — 8 이 아니면 원본이 바뀐 것이라 평가자는 판정을 멈추고 그 사실을 보고한다) [exact, enumerated]
- [ ] SK-05: 옛 9-Phase 글이 kaizen-flow 페이지(스크립트까지 포함한 원문)에 한 줄도 없다 — 정규식 `9-Phase|9개 Phase|9→Final|Phase 4-9|↔9([^0-9↔]|$)|Phase 2~6`. 측정: `m SK-05` 가 `stale=0`. 양성 대조: 시작 판 `stale=10` (위 GAP 표의 줄 173 · 185 · 206 · 242 · 260 · 471 · 473 · 544 · 563 · 781). 17 Phase 를 잇는 `…→9→10→…` · `…↔9↔10…` 꼴은 걸리지 않는다(모의 좋은 판 `stale=0`, 봉인 전 실측) [exact]
- [ ] SK-06: 시뮬레이터가 17 Phase 와 Final 을 끝까지 돈다 — Given 공통 전제 G, When 도우미가 kaizen-flow 페이지를 1280px 로 열어 이름에 「시뮬레이션 시작」 이 든 단추를 누르고 「시뮬레이션」 절 글에 `사이클 완료` 가 나올 때까지(최대 300 초) 기다리면, Then 그 절 글의 `PHASE N` 번호 모음이 정확히 1 ~ 17 이고 `FINAL` 이 있으며 콘솔 오류 · 페이지 오류가 0 이다. 측정: `m SK-06` 이 `sim_seq_ok=1 n=17 final=1 done=1 err=0` (시작 판 `sim_seq_ok=0 n=9 final=1 done=1 err=0`). 알려진 답: 모의 좋은 판 → `sim_seq_ok=1 n=17 final=1 done=1 err=0`. 음성 대조: 시작 판처럼 기록이 PHASE 9 에서 끝나면 `sim_seq_ok=0` 이다 (둘 다 봉인 전 실측) [exact]
- [ ] SK-07: 「타임라인」 절이 남아 있으면 그 절 글에 `P1` ~ `P17` 과 `Final` 18 개가 모두 보이고(`P1` 이 `P10` 에 먹히지 않게 앞뒤 글자를 본다), 절을 뺐으면 절 이름표 「타임라인」 이 없다. 측정: `m SK-07` 이 `section=present hits=18/18` 또는 `section=absent` (시작 판 `section=present hits=7/18` — P1 ~ P6 · Final). 알려진 답: 모의 좋은 판 `hits=18/18`, 절을 뺀 모의 판 `section=absent` (봉인 전 실측) [exact]
- [ ] SK-08: kaizen-flow 를 다시 써도 원본 오케스트레이터에서 옮긴 글이 줄지 않는다 — 옛 판(시작점) 페이지 대비 원본 코드 표시 빠짐 0 · 원본 낱말 비율이 옛 판 이상. 측정: `m SK-08` 이 `lost=0` · `wr_ok=1` · `orch_same=1` (시작 판 `codes=263 new=45 old=45 lost=0 wr=0.13->0.13 wr_ok=1`). 도우미 `cov` 는 핸드오프 도구 `coverage.py` 와 같은 식이고 옛 판을 파일로 받는다 — 시작 판 세 쪽에서 원 도구와 같은 `codes` · `new` · `wr` 를 냈다 (봉인 전 실측) [exact]
- [ ] SK-09: `docs/onboarding-kit/setup-guide.html` 이 원본 `onboarding-kit/skills/setup-guide/SKILL.md` 의 코드 블록 줄(공백을 뺀 8 자 이상 — `guide_gate` 함수 블록과 `STACK` 반복 블록 포함)을 모두 담고, 옛 판 대비 코드 표시 빠짐 0 · 낱말 비율이 옛 판 이상이다. 측정: `m SK-09` 의 `fen` 줄에서 `in_new` 가 `lines` 와 같고(끝점 원본 기준 — 시작 판 `lines=61 in_new=1`) `cov` 줄이 `lost=0` · `wr_ok=1` (시작 판 `codes=81 new=68 old=68 lost=0 wr=0.55->0.55`). 알려진 답: 8 자 이상 두 줄 · 8 자 미만 한 줄짜리 코드 블록과 그중 한 줄만 든 페이지 → `lines=2 in_new=1`, 코드 표시 셋 중 둘이 든 페이지 → `codes=3 new=2`; 시작 판 페이지에 원본 코드 블록을 `pre` 로 붙인 사본 → `lines=61 in_new=61 lost=0` · `wr=0.55->0.57 wr_ok=1` (봉인 전 실측) [exact]
- [ ] SK-10: `docs/design-kit/design-concept.html` 이 원본 `design-kit/skills/design-concept/SKILL.md` 의 코드 블록 줄(공백을 뺀 8 자 이상)을 모두 담고, 옛 판 대비 코드 표시 빠짐 0 · 낱말 비율이 옛 판 이상이다. 측정: `m SK-10` 의 `fen` 줄에서 `in_new` 가 `lines` 와 같고(시작 판 `lines=47 in_new=3`) `cov` 줄이 `lost=0` · `wr_ok=1` (시작 판 `codes=29 new=16 old=16 lost=0 wr=0.44->0.44`). 알려진 답: SK-09 과 같은 작은 입력 (봉인 전 실측) [exact]
- [ ] SK-11: `docs/design-kit/design-mockup.html` 이 원본 `design-kit/skills/design-mockup/SKILL.md` 의 코드 블록 줄(공백을 뺀 8 자 이상)을 모두 담고, 옛 판 대비 코드 표시 빠짐 0 · 낱말 비율이 옛 판 이상이다. 원본은 끝점의 파일이다 — 다른 세션 c4d 가 원본을 고친 판이 이 가지에 들어오면 그 판 기준으로 잰다. 측정: `m SK-11` 의 `fen` 줄에서 `in_new` 가 `lines` 와 같고(시작 판 `lines=20 in_new=15`) `cov` 줄이 `lost=0` · `wr_ok=1` (시작 판 `codes=31 new=20 old=20 lost=0 wr=0.55->0.55`). 알려진 답: SK-09 과 같은 작은 입력 (봉인 전 실측) [exact]
- [ ] SK-12: kaizen-flow 의 「공통 실행 패턴」 절이 원본 「각 Phase 공통 실행 패턴」 절에서 지금 빠진 셋을 담는다 — 4 번째 걸음 `예방적 분석`, 피드백이 0 건일 때의 `리서치 전용` 모드, 동시에 도는 Phase 3 개 제한(`동시` 와 `3 개` 또는 `3개`). 측정: `m SK-12` 가 `section=present hits=4/4` · `orch_same=1` (시작 판 `section=present hits=0/4`). 알려진 답: 모의 좋은 판 `hits=4/4` (봉인 전 실측) [exact, enumerated]

## Script

- [ ] SC-00: N/A (릴리스 스크립트 · 판 올리기 · `marketplace.json` 은 이 계약이 건드리지 않는다 — 판 올리기는 합친 뒤 릴리스 단계 몫이다. 측정: `m SC-00` 이 `release_paths=0` — 바뀐 경로 가운데 `scripts/` · `.claude-plugin/` 0 개)

## Error

- [ ] ER-01: 글자 간격이 넓어져도(CI 리눅스가 글자를 더 넓게 그리는 것을 맥에서 재현) 옛 페이지 일곱이 좁은 화면에서 가로로 넘치지 않는다 — Given 공통 전제 G, When 도우미가 페이지를 375px 로 열어 `*{letter-spacing:0.06em !important}` 를 넣으면, Then 페이지마다 `scrollWidth - clientWidth` 가 2 이하다. 측정: `m ER-01` 이 대상 일곱 `docs/backend-kit/api-lifecycle.html` · `docs/design-kit/typography-scale.html` · `docs/flutter-toolkit/theming.html` · `docs/rust-kit/grpc-tonic.html` · `docs/rust-kit/observability.html` · `docs/rust-kit/ownership-borrowing.html` · `docs/rust-kit/project-structure.html` 줄이 모두 `OK` 이고 끝줄 `over=0/7` (시작 판 `ls006=` 7 · 15 · 21 · 19 · 9 · 20 · 21, `over=7/7` — 양성 대조) [exact, enumerated]
- [ ] ER-02: 문서 전체가 같은 조건(+0.06em · 375px)에서 넘치지 않고, 넘침을 가리는 선언을 더하지 않았다 — 측정: `m ER-02` 가 `over=0/N` 이고 `html_total=N` (N 은 끝점 `docs/` 아래 `.html` 수, 시작 판 177) 이며 `hidden_added=0` (이 계약이 고친 11 쪽의 더해진 줄에 `overflow` · `overflow-x` 값 `hidden` · `clip` 0 줄). 이 셈은 ER-01 의 일곱 쪽만이 아니라 11 쪽 전체를 본다 — 의도된 제약이다: kaizen-flow 등 네 쪽에도 넘침과 무관해 보이는 카드 모서리 자르기라도 `overflow:hidden` · `clip` 을 새로 넣지 않는다. 옛 판에 이미 있는 그런 줄(kaizen-flow `:46` · `:107`)은 글자 그대로 두면 더해진 줄로 세지 않는다. 시작 판 `over=7/177 html_total=177 hidden_added=0`. 양성 대조: 임시 복제본에서 theming.html 에 `body{overflow-x:hidden}` 한 줄을 더해 커밋하면 `hidden_added=1` (봉인 전 실측) [exact]
- [ ] ER-03: 이 계약이 고친 11 쪽을 폭 2 개 × 테마 2 개로 열어 가로 넘침 2px 이하 · 콘솔 오류와 페이지 오류 0 이다 — 축: 페이지 11 (도우미 `PAGES11`, 시작 판 파일 11 개 모두 있음) · 폭 `375` · `1280` · 테마 `light` · `dark` (브라우저 색 설정과 `data-theme` 속성을 함께 바꾼다. 11 쪽은 지금 모두 어두운 테마 전용이라 밝은 설정에서도 어두운 화면이 그려지는 것이 정상이다). cases_total 은 도우미가 세 배열 길이의 곱으로 낸 `expected` 다. 측정: `m ER-03` 이 `cases=44 expected=44 ok=44` · `BAD` 줄 0 · `shots_n=44` (캡처 44 장이 `shots=` 폴더에 남아 평가자가 눈으로 볼 수 있다). 시작 판 `cases=44 expected=44 ok=44`. 양성 대조: 900px 폭 요소와 오류를 던지는 스크립트를 담은 임시 페이지 한 쪽 → `cases=4 ok=0` · `BAD` 네 줄 (봉인 전 실측) [exact]
- [ ] ER-04: 일곱 쪽을 수치 말고 구조로 고쳤다 — ER-01 의 일곱 쪽마다 (a) `font-size` · `letter-spacing` · `padding` 선언 목록(값까지, 순서 무시)이 옛 판과 같고 (b) 보이는 글이 옛 판과 같고 (c) 더해진 줄에 구조 선언(`minmax(0` · `overflow-wrap` · `min-width:0` · `word-break` · `overflow-x:auto` 가운데 하나)이 1 줄 이상이다. 측정: `m ER-04` 일곱 줄이 모두 `decl_same=1 text_same=1` 이고 `struct=` 값이 1 이상 (시작 판 일곱 줄 `decl_same=1 text_same=1 struct=0`). 양성 대조: 임시 사본에서 api-lifecycle.html 첫 `font-size` 를 `99px` 로 바꾸면 `decl_same=0`, 카드 제목 한 줄을 지우면 `text_same=0`, `.grid-2{grid-template-columns:minmax(0,1fr)}` 한 줄을 더하면 `struct=1` (봉인 전 실측) [exact, enumerated]

## Architecture

- [ ] AR-01: 바뀐 파일이 기대 집합 안이고 페이지마다 한 커밋이다 — Given 공통 전제 G, `BASE` 부터 `TIP` 까지 `git diff --name-only` 로 모은 경로가 도우미 `ALLOWED` 의 15 경로(11 쪽 · 계약 · QA 리포트 · 개정 파일 · notes) 안에만 있고(부분 집합, 생성물 없음), 11 쪽이 모두 바뀌었고, 병합 아닌 커밋마다 `docs/` 파일이 1 개 이하이며, `docs/` 와 `.harness/` 를 한 커밋에 섞지 않는다. 측정: `m AR-01` 이 `extra=0 pages=11/11 multi_page=0 mixed=0` (시작 판 `changed=0 extra=0 pages=0/11 multi_page=0 mixed=0`). 양성 대조: 임시 복제본에서 페이지 셋 · `README.md` · notes 를 한 커밋에 넣으면 `extra=1 pages=3/11 multi_page=1 mixed=1` 이고 남는 경로 `README.md` 를 찍는다 (봉인 전 실측) [exact, collective]
- [ ] AR-02: 결정과 넘김을 notes 에 남긴다 — Given 끝점 `TIP`, notes 파일 `.harness/.meta/after-kaizen-0926/c3b-notes.md` 가 커밋돼 있고 일곱 토큰 `FN-80` · `FN-79` · `tone-guide` · `prefers-reduced-motion` · `c4d` · `타임라인` · `dark-only` 가 각 1 줄 이상이다. 담을 내용: FN-80 처리(kaizen-flow 원본을 오케스트레이터 SKILL.md 로 삼은 근거), 넘긴 것(FN-79 howto-kit accent · 공통 틀 `prefers-reduced-motion` · 행간)과 사유, c4d 가 design-mockup 원본을 고친 판이 들어오면 SK-11 을 다시 잰다는 것, 타임라인을 둘지 뺄지와 분 단위 값의 근거(원본에 없는 값이면 「예시」 로 밝혔는지), 11 쪽을 `dark-only` 로 둔 판단, tone-guide 5 단계 대조 결과. 측정: `m AR-02` 가 `committed=1` 과 일곱 값 모두 1 이상 (시작 판 `committed=0` 과 0 일곱). 양성 대조: 임시 복제본에 일곱 토큰을 담은 notes 를 커밋하면 `committed=1` 과 1 일곱 (봉인 전 실측) [exact, enumerated]
- [ ] AR-03: 소비자 쪽(첫 화면 `docs/index.html` 의 등록과 내부 링크)이 그대로다 — 끝점 트리에서 `python3 scripts/check-docs-links.py` 가 종료 코드 0 · `깨진 링크 없음` · `페이지 176 · 등록 176` 을 낸다. 측정: `m AR-03` 이 `rc=0` · `broken0=1` · `nav=페이지 176 · 등록 176` (시작 판 같은 값). 양성 대조: 끝점을 풀어 둔 판의 kaizen-flow.html 에 없는 링크 하나를 넣으면 `rc=1` · `깨진 링크 1 개` (봉인 전 실측) [exact]

## Anti-patterns

- [ ] AP-01: 버전을 하드코딩하지 않는다 — plugin.json에서 읽어야 한다. 이 계약에 적용: 정적 페이지는 `plugin.json` 을 읽을 수 없으니 11 쪽의 더해진 줄에 지금 킷 판 번호(끝점 `*/.claude-plugin/plugin.json` 의 `version` 값, 시작 판 8 종)를 박지 않는다 — 박으면 다음 릴리스에 옛 값이 된다. 측정: `m AP-01` 이 `hits=0` (시작 판 `versions=8 hits=0`). 양성 대조: 임시 복제본 kaizen-flow.html 에 `harness 0.14.0` 한 줄을 더해 커밋하면 `hits=1` (봉인 전 실측)
- [ ] AP-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수 (```text, ```bash, ```yaml 등). 판정 권위는 validate-plugin V6 상태기계다 — 여는/닫는 fence 가 동형이라 줄 단위 정규식으로는 판정 불가. 이 계약에 적용: 새 notes 파일. V6 는 킷 폴더만 읽어 notes 를 보지 않으므로 도우미가 V6 와 같은 상태기계(줄 앞 공백을 벗긴 뒤 백틱 세 개로 시작하면 열고 닫기를 번갈아 셈)를 notes 에 돌린다. 측정: `m AP-03` 이 `committed=1 bare=0`. 양성 대조: 임시 복제본 notes 에 언어 없는 fence 한 쌍 → `bare=1` (봉인 전 실측)

## Reusability

- [ ] RE-01: N/A (산출물이 따로 떨어진 HTML 문서 페이지와 notes 뿐이라 다른 곳에서 가져다 쓸 컴포넌트 · 모듈이 없다. 측정: `m RE-01` 이 `added_files=0` — `docs/` 에 새 파일 0. 양성 대조: 임시 복제본에 `docs/` 새 파일 하나를 커밋하면 `added_files=1`, 봉인 전 실측)
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다 — 각 페이지의 기존 CSS 변수 · 클래스 · 시뮬레이터 함수 안에서 고치고, 새 파일(스타일 · 스크립트 · 페이지)이나 외부 스타일 · 외부 스크립트 · `@import` 를 더하지 않는다. 측정: `m RE-02` 가 `added_files=0 ext_added=0` (시작 판 같은 값). 양성 대조: 임시 복제본에서 `docs/` 새 파일 하나와 theming.html 의 `<link rel="stylesheet" href="x.css">` 한 줄을 커밋하면 `added_files=1 ext_added=1` (봉인 전 실측)

## Diagnostics

- [ ] DG-01: N/A (commands.analyze `bash -n scripts/release.sh` 가 재는 `scripts/release.sh` 는 이번 바뀐 파일에 없다. 측정: `m DG-01` 이 `release_sh=0`)
- [ ] DG-02: IDE diagnostics 워닝/인포 0개 ([] 제외) — 편집기 진단을 명령줄로 같게 잰다(계약 · QA 리포트 · 개정 파일은 뺀다): 11 쪽의 페이지 안 스크립트가 모두 `node --check` 통과 · `<style>` 블록마다 중괄호 짝이 맞음 · 짝 안 맞는 태그 0 (11 쪽 합) · notes 의 markdownlint-cli2 0.23.2(MD013 끔, 편집기 확장과 같은 설정) 경고 0. 세 페이지 검사가 모두 절대 기준 0 이다 — 시작 판 11 쪽이 쪽마다 `tag_bad=0` 이라 옛 판 대비 기준을 둘 까닭이 없다. 측정: `m DG-02` 가 `js_bad=0 tag_bad=0 css_bad=0 md=0` (시작 판 `js_bad=0 tag_bad=0 css_bad=0 md=absent` — notes 가 아직 없다. 도구가 없으면 도우미가 임시 폴더에 설치한다). 양성 대조: 망가진 스크립트 · 닫히지 않은 중괄호 · 닫히지 않은 `div` 를 담은 임시 페이지 → `node --check` 종료 코드 1 · `css_bad=1` · `tag_bad=1`, `#bad heading` 줄이 든 md → 경고 2 (봉인 전 실측)
- [ ] DG-03: N/A (commands.test `bash scripts/release.sh 2>&1 || true` 가 재는 `scripts/release.sh` 는 이번 바뀐 파일에 없다. 측정: DG-01 과 같은 `m DG-01` 이 `release_sh=0`)
- [ ] DG-04: 실제 앱/서버 구동 시 에러 0개 — 이 계약에 적용: 11 쪽을 레포 검사기 `node scripts/check-docs-a11y.js`(가로 넘침 375 · 768 · 1280 · 콘솔 오류 · 글자 대비 · 누르는 자리 크기)로 연다. 측정: `m DG-04` 가 `rc=0` · `11/11 PASS` (시작 판 같은 값). 양성 대조: 오류를 던지고 900px 로 넘치는 임시 페이지 → `FAIL` · 종료 코드 1 (봉인 전 실측)
- [ ] DG-05: CI(자동 검사) 단계를 로컬에서 전부 돌려 통과한다 — Given 작업 폴더 W 가 끝점과 같다(`git -C W rev-parse HEAD` 가 `TIP` 이고 `git -C W status --porcelain --untracked-files=no` 가 빈 출력 — 아니면 도우미가 `W_NOT_TIP` 을 찍고 멈춘다), When `m DG-05` 가 `/Users/jackson/Hub/10_Dev/claude-plugins/.harness/handoff/2026-09-26-tools/ci-local.sh` 를 W 에 돌리면, Then 요약에 `rc=0` 줄이 22 개이고 `rc=0` 이 아닌 줄은 `feedback-agg-test SKIP (yq 없음)` 하나뿐이다. 도구 파일은 이 가지 밖(본 체크아웃)에 있어 커밋으로 고정되지 않으므로 도우미가 그 내용 지문(`git hash-object`)을 봉인 때 값 `TOOL_BLOB` 과 대조해 `tool_same` 을 찍는다. 측정: `m DG-05` 가 `tool_same=1 rc0=22 other=[feedback-agg-test SKIP (yq 없음);]` (시작 판 봉인 전 실측: 같은 값). 음성 대조: 이 계약이 기대는 `docs-a11y` · `docs-links` 단계는 ER-01 의 일곱 쪽이 아니라 원래 폭에서 재므로 시작 판에서도 통과한다 — 넘침 결함은 ER-01 · ER-02 가 잡는다

## 범위 경계

항목별 처리 — 입력은 과제 목록과 핸드오프 §C3 「문서 사이트」 줄이다.

| 항목 | 처리 | 조건 · 사유 |
| --- | --- | --- |
| FN-80 `docs/process/kaizen-flow.html` 9-Phase → 17 Phase + Final | 계약에 넣음 | SK-01 ~ SK-08 · SK-12. 원본은 `.claude/skills/kaizen-orchestrator/SKILL.md` 로 정한다 — 페이지 제목 · 호출 문법 · 흐름이 모두 이 스킬을 그리고, docs-site 매핑 표의 「(내부 문서)」 는 이 스킬 폴더 밖의 원본이 없다는 뜻이다. 매핑 표 자체를 고치는 일은 `.claude/skills/docs-site/` 라 범위 밖(다른 묶음 c1b 가 매핑을 다룬다) |
| `docs/onboarding-kit/setup-guide.html` 원본 담김 (61 줄 중 1) | 계약에 넣음 | SK-09 |
| `docs/design-kit/design-concept.html` 원본 담김 (47 줄 중 3) | 계약에 넣음 | SK-10 |
| `docs/design-kit/design-mockup.html` 원본 담김 (20 줄 중 15) | 계약에 넣음 | SK-11. c4d 가 원본을 고친 판이 이 가지에 들어오기 전이면 지금 원본 기준으로 맞추고, 들어오면 그 판 기준으로 다시 잰다(AR-02 `c4d`) |
| 글자 간격 +0.06em 에서 넘치는 옛 페이지 일곱 | 계약에 넣음 | ER-01 · ER-02 · ER-04 |
| 검증 — 접근성 검사기 · 링크 검사기 · 실제 렌더(375 · 1280, 밝은 · 어두운) | 계약에 넣음 | DG-04 · AR-03 · ER-03 · DG-05 |
| FN-79 css-tokens 매핑 표에 howto-kit accent | 넘김 | 표가 `.claude/skills/docs-site/` 안에 있다 — 과제가 정한 범위 밖 |
| 문서 사이트 공통 틀 177 쪽 `prefers-reduced-motion` · 행간 | 넘김 | 사용자 결정 대기(핸드오프 §C4 5 번). 이 계약은 11 쪽의 모션 · 행간 규칙을 새로 넣지 않는다 |
| 11 쪽에 밝은 테마 규칙 새로 넣기 | 넘김 | 공통 틀 변경이라 위와 같은 사유. ER-03 은 지금 테마 방식 그대로 두 색 설정에서 잰다 |
| kaizen-flow 트리거 표의 개별 카이젠 행 · 시뮬레이터 버전 올림 로그의 킷 목록 | 구현 재량 | 조건으로 잠그지 않는다. 고치면 SK-05 · AP-01 을 지킨다 |

범위 밖(이 계약이 고치지 않는다): `.claude/skills/docs-site/` · `scripts/` · 킷 폴더(원본 SKILL.md 포함) · `docs/index.html` · 다른 문서 페이지 166 쪽 · 킷 `plugin.json` 판.

타임라인 분 단위 값: 원본에 없는 값이다. 남기면 「예시」 로 밝히거나 저장소 기록(`.harness/.meta/orchestrator-audit-log.md` 의 사이클 소요 등)에서 가져온 근거를 notes 에 적는다 — 조건은 라벨만 잰다(SK-07). 근거 없이 새 수치를 지어 넣지 않는다.

교차 진단(qa-evaluator, 봉인 전 1 회) 지적 일곱을 봉인 전에 반영했다 — RE-01 · RE-02 양성 대조 실측, ER-02 가 11 쪽 전체를 막는 것이 의도임을 명시, SK-01 · 02 · 03 · 04 · 08 · 12 에 원본 지문 `orch_same`, DG-05 에 도구 지문 `tool_same`, 공통 전제 G 에 타임라인 절 삭제 예외, DG-02 짝 안 맞는 태그를 절대 기준 0 으로, 준비 단계에 브라우저 실행 파일 출처 · 실패 문구 · 복구 명령.

커버리지 해소 — Step 6.5 (4) 검출기가 낸 `UNCOVERED` 한 건과 목록을 한 곳에만 둔 조건:

- 커버리지 해소: SK-04 — `0.5` · `0.6` · `F3.5` 는 원본 제목 번호를 대는 근거 인용이다. 잴 대상 여덟 이름은 도우미 `pg.py kf … steps` 의 목록이 산문과 같은 글자로 센다
- 커버리지 해소: AR-01 — 경로 기대 집합은 도우미 `ALLOWED` 한 곳에만 적는다(목록을 두 번 적지 않는다는 계약 형식 규칙). ER-03 의 페이지 11 도 도우미 `PAGES11` 한 곳이다
- 커버리지 해소: AR-02 — 일곱 토큰과 notes 경로는 `m AR-02` 의 토큰 목록과 `NOTES` 변수가 산문과 같은 글자로 센다

## 회귀 게이트 — 측정 도우미 · 봉인 전 실측

평가 때 이 블록을 떼어 bash 에서 불러 쓴다. `TMPDIR` 은 평가자 임시 폴더로 준다. 도우미는 `$T` 아래에만 쓴다 — 작업 폴더와 그 밖의 입력은 지우지 마라.
브라우저 도구는 작업 폴더 W 의 `node_modules`(추적 안 되는 폴더, `npm ci` 로 설치)를 `NODE_PATH` 로 빌려 쓴다.

준비 단계 실측(봉인 전, 이 기계): `command -v node` → fnm 경로 · 종료 코드 0 (`v24.14.1`), `command -v python3` → `/Users/jackson/.pyenv/versions/3.14.3/bin/python3` · 0, `command -v git` → `/opt/homebrew/bin/git` · 0,
W 의 `node_modules/playwright-core` 판 `1.58.2`(`npm ci` 종료 코드 0), `markdownlint-cli2@0.23.2` 임시 설치 종료 코드 0, `ci-local.sh` 경로 있음.
브라우저 실행 파일은 `node_modules` 가 아니라 사용자 캐시 `~/Library/Caches/ms-playwright/chromium_headless_shell-1208` 에서 온다(`playwright-core install --dry-run chromium-headless-shell` 가 이 설치 위치를 찍는다). 이 기계에서 `chromium.launch()` 가 `145.0.7632.6` 으로 뜬다(종료 코드 0).
캐시가 없으면 `browserType.launch: Executable doesn't exist at …/chromium_headless_shell-1208/…` 로 실패하고 도우미의 `pw.js` 는 종료 코드 2 를 낸다(빈 `PLAYWRIGHT_BROWSERS_PATH` 로 봉인 전 실측).
복구: `cd W && node_modules/.bin/playwright-core install chromium-headless-shell` 뒤 다시 잰다 — 브라우저가 없어 못 잰 조건은 FAIL 이 아니라 환경 실패로 보고한다. `git archive` 로 푼 판에서 `NODE_PATH=W/node_modules node scripts/check-docs-a11y.js` 와 `python3 scripts/check-docs-links.py` 가 돈다(종료 코드 0).

```bash
# 떼기: awk '/^# === 측정 도우미 시작/{f=1} f{print} /^# === 측정 도우미 끝/{exit}' <계약> > "$TMPDIR/c3b-measure.sh"
# 부르기: bash -c 'source "$TMPDIR/c3b-measure.sh" || exit 2; type m >/dev/null || exit 2; m SK-01'
# 시작 판: E_REF=BASE 를 주고 부른다. 모의 판을 재려면 KF=<파일> 을 준다
# === 측정 도우미 시작 (after-0924-docs-site) ===
# 쓰는 법: 이 블록을 파일로 떼어 bash 에서 source 한 뒤 `m <조건 ID>`. zsh 에서 부르지 마라.
# 잴 트리 E — 기본은 가지 끝(TIP)을 git archive 로 푼 임시 폴더. 시작 판을 재려면 E_REF=BASE.
# 옛 판 EB — 늘 시작점(BASE)을 푼 폴더. 페이지 비교(담김 · 글 내용 · 선언 목록)의 기준이다.
W=${W:-/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak-c3b}
BR=${BR:-chore/ak-c3b-docs-site}
BASE=$(git -C "$W" merge-base origin/main "$BR") || { echo "UNRESOLVED BASE"; return 2 2>/dev/null || exit 2; }
TIP=$(git -C "$W" rev-parse --verify "$BR") || { echo "UNRESOLVED TIP"; return 2 2>/dev/null || exit 2; }
T=$(mktemp -d "${TMPDIR:-/tmp}/c3b.XXXXXX")
snap() { mkdir -p "$2" && git -C "$W" archive "$1" | tar -x -C "$2"; }
EB=$T/base; snap "$BASE" "$EB"
case "${E_REF:-TIP}" in
  BASE) E=$EB ;;
  *)    E=$T/tip; snap "$TIP" "$E" ;;
esac
# 브라우저 도구 — 작업 폴더의 node_modules 를 빌려 쓴다(추적 안 되는 폴더). 없으면 설치한다
[ -d "$W/node_modules/playwright-core" ] || (cd "$W" && npm ci >/dev/null 2>&1)
[ -d "$W/node_modules/playwright-core" ] || { echo "NO_PLAYWRIGHT"; return 2 2>/dev/null || exit 2; }
export NODE_PATH=$W/node_modules
KF=${KF:-$E/docs/process/kaizen-flow.html}
ORCH=$E/.claude/skills/kaizen-orchestrator/SKILL.md
# 봉인 때 판의 내용 지문(git hash-object). 원본 · 도구가 바뀌면 orch_same · tool_same 이 0 이 된다
ORCH_BLOB=4332db0e65a17b26a2be3d087ef8685a6b74b1c5
CI_LOCAL=/Users/jackson/Hub/10_Dev/claude-plugins/.harness/handoff/2026-09-26-tools/ci-local.sh
TOOL_BLOB=b15dcdf8f6d2bb1b9c5f152c949f8c29f70e61e1
og() { echo "orch_same=$([ "$(git hash-object "$ORCH" 2>/dev/null)" = "$ORCH_BLOB" ] && echo 1 || echo 0)"; }
PAGES7='docs/backend-kit/api-lifecycle.html
docs/design-kit/typography-scale.html
docs/flutter-toolkit/theming.html
docs/rust-kit/grpc-tonic.html
docs/rust-kit/observability.html
docs/rust-kit/ownership-borrowing.html
docs/rust-kit/project-structure.html'
PAGES4='docs/process/kaizen-flow.html
docs/onboarding-kit/setup-guide.html
docs/design-kit/design-concept.html
docs/design-kit/design-mockup.html'
PAGES11=$(printf '%s\n%s\n' "$PAGES4" "$PAGES7")
NOTES=.harness/.meta/after-kaizen-0926/c3b-notes.md
ALLOWED=$(printf '%s\n%s\n' "$PAGES11" '.harness/sprint-contract-after-0924-docs-site.md
.harness/sprint-feedback-after-0924-docs-site.md
.harness/sprint-amendments-after-0924-docs-site.md
.harness/.meta/after-kaizen-0926/c3b-notes.md')

cat > "$T/pg.py" <<'PY'
import sys, re, html, json
def text(h, sep=' '):
    h = re.sub(r'(?is)<(script|style)[^>]*>.*?</\1>', sep, h)
    return re.sub(r'\s+', sep, html.unescape(re.sub(r'<[^>]+>', sep, h)))
rd = lambda p: open(p, encoding='utf-8').read()
cmd = sys.argv[1]
if cmd == 'cov':    # handoff 도구 coverage.py 와 같은 식 — 옛 판을 파일로 받는다
    s, new, old = rd(sys.argv[2]), text(rd(sys.argv[3])), text(rd(sys.argv[4]))
    codes = sorted({c.strip() for c in re.findall(r'`([^`\n]+)`', s) if c.strip()})
    cn = [c for c in codes if re.sub(r'\s+', ' ', c) in new]; co = [c for c in codes if re.sub(r'\s+', ' ', c) in old]
    lost = [c for c in co if c not in cn]
    words = {w for w in re.findall(r'[0-9A-Za-z가-힣_.-]{2,}', re.sub(r'`[^`]*`', ' ', s))}
    wr = lambda t: sum(1 for w in words if w in t) / max(1, len(words))
    print(f'codes={len(codes)} new={len(cn)} old={len(co)} lost={len(lost)} wr={wr(old):.2f}->{wr(new):.2f} wr_ok={int(round(wr(new),4) >= round(wr(old),4))} {lost[:4]}')
elif cmd == 'fen':  # handoff 도구 fence2.py 와 같은 식 — 옛 판을 파일로 받는다
    s, new, old = rd(sys.argv[2]), text(rd(sys.argv[3]), ''), text(rd(sys.argv[4]), '')
    lines = []; fence = False
    for l in s.splitlines():
        if re.match(r'^\s*(```|~~~)', l): fence = not fence; continue
        if fence:
            t = re.sub(r'\s+', '', l)
            if len(t) >= 8: lines.append((t, l.strip()))
    L = sorted(set(lines)); ino = [x for x in L if x[0] in old]; lost = [x[1] for x in ino if x[0] not in new]
    miss = [x[1] for x in L if x[0] not in new]
    print(f'lines={len(L)} in_old={len(ino)} in_new={len(L)-len(miss)} lost={len(lost)} {miss[:3]}')
elif cmd == 'orch':  # 오케스트레이터 원본에서 Phase 이름 · 스킬 · 호출 인자를 뽑는다
    s = rd(sys.argv[2])
    ph = re.findall(r'^Phase (\d+): (.+?) 카이젠(?: \(([a-z-]+)\))?\s*$', s, re.M)
    arg = re.search(r'^argument-hint: "\[(.+)\]"', s, re.M).group(1).split('|')
    print(json.dumps({'names': [p[1] for p in ph], 'nums': [int(p[0]) for p in ph],
                      'skills': [p[2] for p in ph if p[2]], 'args': arg}, ensure_ascii=False))
elif cmd == 'kf':   # 페이지 보이는 글에 원본 스킬 · 호출 인자 · 단계 이름이 드는지
    t, o, part = text(rd(sys.argv[2])), json.loads(rd(sys.argv[3])), sys.argv[4]
    if part == 'skills':
        miss = [k for k in o['skills'] if k not in t]; print(f'skills={len(o["skills"])-len(miss)}/{len(o["skills"])} {miss[:4]}')
    elif part == 'args':
        miss = [a for a in o['args'] if not re.search(r'/kaizen-orchestrator\s+' + re.escape(a) + r'(?![0-9A-Za-z])', t)]
        print(f'invoke={len(o["args"])-len(miss)}/{len(o["args"])} {miss[:4]}')
    elif part == 'steps':
        src = text(rd(sys.argv[5]))
        st = ['피드백 데이터 풀 수집', 'Orchestrator Self-Audit', 'Phase Relevance Triage', '전체 정합성 검증',
              'docs-site 재생성', '글로벌 피드백 정리', '메모리 승격 후보 산출', 'PR 생성']
        print(f'steps={sum(1 for x in st if x in t)}/{len(st)} src={sum(1 for x in st if x in src)}/{len(st)} {[x for x in st if x not in t][:4]}')
elif cmd == 'decl':  # 글자 크기 · 글자 간격 · 안쪽 여백 선언 목록과 보이는 글이 옛 판과 같은지
    a, b = rd(sys.argv[2]), rd(sys.argv[3])
    rx = r'(?:font-size|letter-spacing|padding(?:-(?:top|right|bottom|left|inline|block))?)\s*:\s*[^;}"]+'
    d = lambda h: sorted(re.sub(r'\s+', '', x) for x in re.findall(rx, h))
    print(f'decl_same={int(d(a) == d(b))} text_same={int(text(a) == text(b))}')
elif cmd == 'html':  # 편집기 진단 대용 — 짝 안 맞는 태그 수 · 중괄호 안 맞는 style 블록 수 · 인라인 script 를 파일로
    from html.parser import HTMLParser
    VOID = {'area','base','br','col','embed','hr','img','input','link','meta','source','track','wbr','path','circle','rect','line','polyline','polygon','ellipse','stop','use'}
    class P(HTMLParser):
        def __init__(s): super().__init__(); s.st = []; s.bad = 0
        def handle_starttag(s, tag, a):
            if tag not in VOID: s.st.append(tag)
        def handle_startendtag(s, tag, a): pass
        def handle_endtag(s, tag):
            if tag in VOID: return
            if tag in s.st:
                while s.st and s.st[-1] != tag: s.st.pop(); s.bad += 1
                s.st.pop()
            else: s.bad += 1
    h = rd(sys.argv[2]); p = P(); p.feed(h); p.close()
    css = re.findall(r'(?is)<style[^>]*>(.*?)</style>', h)
    css_bad = sum(1 for c in css if c.count('{') != c.count('}'))
    js = re.findall(r'(?is)<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>', h)
    for i, j in enumerate(js): open(f'{sys.argv[3]}.{i}.js', 'w', encoding='utf-8').write(j)
    print(f'tag_bad={p.bad + len(p.st)} css_bad={css_bad} js={len(js)}')
PY

cat > "$T/pw.js" <<'JS'
// 브라우저로 여는 측정. node pw.js <mode> ...
const path = require('path');
const { chromium } = require('playwright-core');
const mode = process.argv[2], args = process.argv.slice(3);
const sectText = (label) => {   // 절 이름표 글이 label 인 요소의 부모(절) 글. 없으면 null
  const el = [...document.querySelectorAll('body *')].find(e => e.children.length === 0 && e.textContent.trim() === label);
  return el && el.parentElement ? el.parentElement.textContent : null;
};
const OVER = () => document.documentElement.scrollWidth - document.documentElement.clientWidth;
(async () => {
  const b = await chromium.launch(); let rc = 0;
  const open = async (f, o = {}) => {
    const ctx = await b.newContext({ viewport: { width: o.w || 1280, height: 900 }, colorScheme: o.cs || 'dark' });
    const p = await ctx.newPage(); const errs = [];
    p.on('console', m => m.type() === 'error' && errs.push(m.text())); p.on('pageerror', e => errs.push(String(e)));
    await p.goto('file://' + path.resolve(f)); return { ctx, p, errs };
  };
  if (mode === 'flow') {          // SK-01 — 「실행 흐름」 절의 PHASE N 차례 · 이름 · 뒤따르는 FINAL
    const [f, orch] = args; const o = JSON.parse(require('fs').readFileSync(orch, 'utf8'));
    const { p } = await open(f); const t = await p.evaluate(sectText, '실행 흐름');
    if (t === null) { console.log('section=absent'); rc = 1; } else {
      const ms = [...t.matchAll(/PHASE (\d+)(?!\d)/g)]; const seq = ms.map(m => +m[1]);
      const want = o.nums; const seqOk = JSON.stringify(seq) === JSON.stringify(want);
      let names = 0; ms.forEach((m, i) => { const seg = t.slice(m.index, i + 1 < ms.length ? ms[i + 1].index : t.length).toLowerCase();
        const n = o.names[want.indexOf(+m[1])]; if (n && seg.includes(n.toLowerCase())) names++; });
      const last = ms.length ? ms[ms.length - 1].index : -1; const fin = last >= 0 && t.slice(last).includes('FINAL') ? 1 : 0;
      console.log(`seq_ok=${+seqOk} n=${seq.length} names=${names}/${want.length} final_after=${fin} seq=${seq.join(',')}`);
    }
  } else if (mode === 'section') { // 이름표로 찾은 절의 글에 낱말이 드는지 — section <page> <label> <낱말|/정규식/>...
    const [f, label, ...ws] = args; const { p } = await open(f); const t = await p.evaluate(sectText, label);
    if (t === null) console.log(`section=absent`); else {
      const hit = ws.map(w => w.startsWith('/') ? new RegExp(w.slice(1, -1)).test(t) : t.includes(w));
      console.log(`section=present hits=${hit.filter(Boolean).length}/${ws.length} miss=${ws.filter((w, i) => !hit[i]).join('|')}`);
    }
  } else if (mode === 'sim') {    // SK-06 — 시작 단추를 누르고 끝날 때까지 기다린 뒤 「시뮬레이션」 절 글
    const [f] = args; const { p, errs } = await open(f);
    await p.getByRole('button', { name: /시뮬레이션 시작/ }).first().click();
    let done = 0;
    try { await p.waitForFunction(label => {
      const el = [...document.querySelectorAll('body *')].find(e => e.children.length === 0 && e.textContent.trim() === label);
      return !!(el && el.parentElement && el.parentElement.textContent.includes('사이클 완료'));
    }, '시뮬레이션', { timeout: 300000 }); done = 1; } catch (e) {}
    const t = await p.evaluate(sectText, '시뮬레이션') || '';
    const seq = [...new Set([...t.matchAll(/PHASE (\d+)(?!\d)/g)].map(m => +m[1]))];
    const want = Array.from({ length: +args[1] || 17 }, (_, i) => i + 1);
    console.log(`sim_seq_ok=${+(JSON.stringify(seq) === JSON.stringify(want))} n=${seq.length} final=${+t.includes('FINAL')} done=${done} err=${errs.length}`);
  } else if (mode === 'lsover') {  // ER-01 · ER-02 — 글자 간격 +0.06em · 375px 가로 넘침
    let over = 0;
    for (const f of args) { const { ctx, p } = await open(f, { w: 375 });
      await p.addStyleTag({ content: '*{letter-spacing:0.06em !important}' }); await p.waitForTimeout(100);
      const v = await p.evaluate(OVER); if (v > 2) over++; console.log(`${v > 2 ? 'OVER' : 'OK  '} ${path.basename(f)} ls006=${v}`); await ctx.close(); }
    console.log(`over=${over}/${args.length}`);
  } else if (mode === 'matrix') {  // ER-03 — 페이지 × 폭 × 테마
    const W = [375, 1280], CS = ['light', 'dark']; const shots = process.env.SHOTS; let ok = 0, n = 0;
    for (const f of args) for (const w of W) for (const cs of CS) { n++;
      const { ctx, p, errs } = await open(f, { w, cs });
      await p.evaluate(t => { document.documentElement.dataset.theme = t; }, cs); await p.waitForTimeout(400);
      const v = await p.evaluate(OVER); const good = v <= 2 && errs.length === 0; if (good) ok++;
      if (shots) await p.screenshot({ path: path.join(shots, `${path.basename(f, '.html')}-${w}-${cs}.png`), fullPage: true });
      if (!good) console.log(`BAD ${path.basename(f)} w=${w} ${cs} of=${v} err=${errs.length}`); await ctx.close(); }
    console.log(`cases=${n} expected=${args.length * W.length * CS.length} ok=${ok}`);
  }
  await b.close(); process.exit(rc);
})().catch(e => { console.error(e); process.exit(2); });
JS

n() { grep -cF -- "$1" || true; }
lst() { printf '%s\n' "$1" | sed "s#^#$E/#"; }
m() {
  case "$1" in
  SK-01) python3 "$T/pg.py" orch "$ORCH" > "$T/orch.json" && node "$T/pw.js" flow "$KF" "$T/orch.json"; og ;;
  SK-02) python3 "$T/pg.py" orch "$ORCH" > "$T/orch.json" && python3 "$T/pg.py" kf "$KF" "$T/orch.json" skills; og ;;
  SK-03) python3 "$T/pg.py" orch "$ORCH" > "$T/orch.json" && python3 "$T/pg.py" kf "$KF" "$T/orch.json" args; og ;;
  SK-04) python3 "$T/pg.py" orch "$ORCH" > "$T/orch.json" && python3 "$T/pg.py" kf "$KF" "$T/orch.json" steps "$ORCH"; og ;;
  SK-05) echo "stale=$(grep -cE '9-Phase|9개 Phase|9→Final|Phase 4-9|↔9([^0-9↔]|$)|Phase 2~6' "$KF")" ;;
  SK-06) node "$T/pw.js" sim "$KF" 17 ;;
  SK-07) node "$T/pw.js" section "$KF" '타임라인' $(seq 1 17 | sed 's#.*#/(^|[^0-9A-Za-z])P&(?![0-9])/#') Final ;;
  SK-08) python3 "$T/pg.py" cov "$ORCH" "$KF" "$EB/docs/process/kaizen-flow.html"; og ;;
  SK-09|SK-10|SK-11)
    case "$1" in
      SK-09) s=onboarding-kit/skills/setup-guide/SKILL.md; pg=docs/onboarding-kit/setup-guide.html ;;
      SK-10) s=design-kit/skills/design-concept/SKILL.md;  pg=docs/design-kit/design-concept.html ;;
      SK-11) s=design-kit/skills/design-mockup/SKILL.md;   pg=docs/design-kit/design-mockup.html ;;
    esac
    echo "fen $(python3 "$T/pg.py" fen "$E/$s" "$E/$pg" "$EB/$pg")"
    echo "cov $(python3 "$T/pg.py" cov "$E/$s" "$E/$pg" "$EB/$pg")" ;;
  SK-12) node "$T/pw.js" section "$KF" '공통 실행 패턴' '예방적 분석' '리서치 전용' '동시' '/3 ?개/'; og ;;
  ER-01) node "$T/pw.js" lsover $(lst "$PAGES7") ;;
  ER-02) node "$T/pw.js" lsover $(find "$E/docs" -type f -name '*.html' | LC_ALL=C sort) | tail -1
    echo "html_total=$(find "$E/docs" -type f -name '*.html' | grep -c .)"
    echo "hidden_added=$(git -C "$W" diff "$BASE" "$TIP" -- $PAGES11 | grep '^+' | grep -v '^+++' | grep -ciE 'overflow(-x)?[[:space:]]*:[[:space:]]*(hidden|clip)' || true)" ;;
  ER-03) mkdir -p "$T/shots"; SHOTS=$T/shots node "$T/pw.js" matrix $(lst "$PAGES11"); echo "shots_n=$(find "$T/shots" -name '*.png' | grep -c .) shots=$T/shots" ;;
  ER-04) for pg in $PAGES7; do
      s=$(git -C "$W" diff "$BASE" "$TIP" -- "$pg" | grep '^+' | grep -v '^+++' | grep -cE 'minmax\(0|overflow-wrap|min-width[[:space:]]*:[[:space:]]*0|word-break|overflow-x[[:space:]]*:[[:space:]]*auto' || true)
      echo "$(basename "$pg") $(python3 "$T/pg.py" decl "$EB/$pg" "$E/$pg") struct=$s"; done ;;
  AR-01) git -C "$W" diff --name-only "$BASE" "$TIP" > "$T/changed.txt"
    extra=$(grep -vxF -f <(printf '%s\n' "$ALLOWED") "$T/changed.txt" | grep -c . || true)
    pages=$(grep -xF -f <(printf '%s\n' "$PAGES11") "$T/changed.txt" | grep -c . || true)
    mp=0; mx=0
    for c in $(git -C "$W" rev-list --no-merges "$BASE..$TIP"); do
      f=$(git -C "$W" show --name-only --format= "$c"); d=$(printf '%s\n' "$f" | grep -c '^docs/' || true); h=$(printf '%s\n' "$f" | grep -c '^\.harness/' || true)
      [ "$d" -gt 1 ] && mp=$((mp+1)); [ "$d" -ge 1 ] && [ "$h" -ge 1 ] && mx=$((mx+1)); done
    echo "changed=$(grep -c . "$T/changed.txt") extra=$extra pages=$pages/11 multi_page=$mp mixed=$mx"
    grep -vxF -f <(printf '%s\n' "$ALLOWED") "$T/changed.txt" | head -5 ;;
  AR-02) b=$(git -C "$W" show "$TIP:$NOTES" 2>/dev/null); c=$([ -n "$b" ] && echo 1 || echo 0); out="committed=$c"
    for k in FN-80 FN-79 tone-guide prefers-reduced-motion c4d 타임라인 dark-only; do out="$out $k=$(printf '%s\n' "$b" | n "$k")"; done; echo "$out" ;;
  AR-03) (cd "$E" && python3 scripts/check-docs-links.py > "$T/links.txt" 2>&1; echo "rc=$?")
    echo "broken0=$(n '깨진 링크 없음' < "$T/links.txt") nav=$(grep -oE '페이지 [0-9]+ · 등록 [0-9]+' "$T/links.txt")" ;;
  AP-01) v=$(find "$E" -path "$E/*/.claude-plugin/plugin.json" -type f -exec python3 -c 'import json,sys; [print(json.load(open(p))["version"]) for p in sys.argv[1:]]' {} + | LC_ALL=C sort -u)
    added=$(git -C "$W" diff "$BASE" "$TIP" -- $PAGES11 | grep '^+' | grep -v '^+++')
    k=0; for x in $v; do c=$(printf '%s\n' "$added" | grep -cE "(^|[^0-9.])v?${x//./\\.}([^0-9.]|\$)" || true); k=$((k+c)); done
    echo "versions=$(printf '%s\n' "$v" | grep -c .) hits=$k" ;;
  AP-03) b=$(git -C "$W" show "$TIP:$NOTES" 2>/dev/null)
    echo "committed=$([ -n "$b" ] && echo 1 || echo 0) bare=$(printf '%s\n' "$b" | awk '{s=$0; sub(/^[ \t]+/,"",s)} s ~ /^```/ { if (!inb) { h=substr(s,4); gsub(/[ \t]/,"",h); if (h=="") bare++; inb=1 } else inb=0 } END{print bare+0}')" ;;
  RE-01|RE-02)
    echo "added_files=$(git -C "$W" diff --diff-filter=A --name-only "$BASE" "$TIP" -- docs | grep -c . || true) ext_added=$(git -C "$W" diff "$BASE" "$TIP" -- $PAGES11 | grep '^+' | grep -v '^+++' | grep -ciE '<link[^>]+stylesheet|<script[^>]+src=|@import' || true)" ;;
  SC-00) echo "release_paths=$(git -C "$W" diff --name-only "$BASE" "$TIP" | grep -cE '^(scripts/|\.claude-plugin/)|/\.claude-plugin/' || true)" ;;
  DG-01|DG-03) echo "release_sh=$(git -C "$W" diff --name-only "$BASE" "$TIP" | grep -cx 'scripts/release.sh' || true)" ;;
  DG-02) jb=0; tb=0; cb=0
    for pg in $PAGES11; do
      o=$(python3 "$T/pg.py" html "$E/$pg" "$T/js-$(basename "$pg")")
      tb=$((tb + $(printf '%s' "$o" | sed -E 's/.*tag_bad=([0-9]+).*/\1/')))
      [ "$(printf '%s' "$o" | sed -E 's/.*css_bad=([0-9]+).*/\1/')" -gt 0 ] && cb=$((cb+1))
    done
    for j in $(find "$T" -maxdepth 1 -name 'js-*.js' | LC_ALL=C sort); do node --check "$j" >/dev/null 2>&1 || jb=$((jb+1)); done
    MDL=${MDL:-$T/mdl}
    [ -x "$MDL/node_modules/.bin/markdownlint-cli2" ] || { mkdir -p "$MDL" && (cd "$MDL" && npm install --no-save --no-audit --no-fund markdownlint-cli2@0.23.2 >/dev/null 2>&1); }
    printf '{ "config": { "MD013": false } }\n' > "$MDL/cfg.markdownlint-cli2.jsonc"
    if [ -f "$E/$NOTES" ]; then md=$( (cd "$(dirname "$E/$NOTES")" && "$MDL/node_modules/.bin/markdownlint-cli2" --config "$MDL/cfg.markdownlint-cli2.jsonc" "$(basename "$NOTES")" 2>&1) | grep -cE '^[^ ]+:[0-9]+' || true); else md=absent; fi
    echo "js_bad=$jb tag_bad=$tb css_bad=$cb md=$md" ;;
  DG-04) (cd "$E" && node scripts/check-docs-a11y.js $PAGES11 > "$T/a11y.txt" 2>&1; echo "rc=$?"); tail -1 "$T/a11y.txt"; grep -c '^OK ' "$T/a11y.txt" ;;
  DG-05) [ "$(git -C "$W" rev-parse HEAD)" = "$TIP" ] && [ -z "$(git -C "$W" status --porcelain --untracked-files=no)" ] || { echo "W_NOT_TIP"; return 2; }
    ts=$([ "$(git hash-object "$CI_LOCAL" 2>/dev/null)" = "$TOOL_BLOB" ] && echo 1 || echo 0)
    mkdir -p "$T/ci"; TMPDIR=$T/ci bash "$CI_LOCAL" "$W" > "$T/ci/run.log" 2>&1
    echo "tool_same=$ts rc0=$(grep -c 'rc=0' "$T/ci/ci-local/summary.txt") other=[$(grep -v 'rc=0' "$T/ci/ci-local/summary.txt" | tr '\n' ';')]" ;;
  *) echo "unknown $1"; return 2 ;;
  esac
}
# === 측정 도우미 끝 ===
```

봉인 전 실측 — 시작 판(`BASE` = `TIP` = `f81568d`, 구현 전)에서 도우미로 잰 값과 대조 결과. 대조용 모의 판 · 임시 복제본은 세션 임시 폴더에서 만들었다(모의 kaizen-flow 는 원본에서 뽑은 이름 · 스킬 · 인자 · 단계 이름으로 만든 최소 페이지, 임시 복제본은 W 를 `git clone --no-hardlinks` 해 나쁜 커밋 하나를 올린 것).

- SK-01 ~ SK-12 시작 판: 각 조건의 괄호 안 값 그대로 (`seq_ok=0 n=9 names=9/17` · `skills=8/16` · `invoke=10/18` · `steps=2/8 src=8/8` · `stale=10` · `sim_seq_ok=0 n=9` · `hits=7/18` · `wr=0.13->0.13` · `lines=61 in_new=1` · `lines=47 in_new=3` · `lines=20 in_new=15` · `hits=0/4`)
- 모의 좋은 kaizen-flow: `seq_ok=1 n=17 names=17/17 final_after=1` · `skills=16/16` · `invoke=18/18` · `steps=8/8 src=8/8` · `stale=0` · `sim_seq_ok=1 n=17 final=1 done=1 err=0` · `section=present hits=18/18` · 타임라인 뺀 판 `section=absent` · `section=present hits=4/4`
- 작은 입력: `fen` → `lines=2 in_old=0 in_new=1 lost=0`, `cov` → `codes=3 new=2 old=0 lost=0` (둘 다 종료 코드 0). 원 도구와 같은 값: 시작 판 세 쪽에서 `coverage.py` · `fence2.py` 와 `codes` · `new` · `wr` · `lines` · `in_new` 가 같다
- 코드 블록을 붙인 setup-guide 사본: `lines=61 in_old=1 in_new=61 lost=0` · `codes=81 new=68 old=68 lost=0 wr=0.55->0.57 wr_ok=1`
- ER-01 시작 판 `over=7/7`, ER-02 시작 판 `over=7/177 html_total=177 hidden_added=0`, ER-03 시작 판 `cases=44 expected=44 ok=44`, 나쁜 임시 페이지 `cases=4 expected=4 ok=0`(BAD 네 줄) · `lsover` `ls006=533`
- ER-04 시작 판 일곱 줄 `decl_same=1 text_same=1 struct=0`. 임시 사본 `font-size:99px` → `decl_same=0`, 카드 제목 지운 복제본 → `text_same=0` · 구조 한 줄 → `struct=1`
- 임시 복제본 나쁜 커밋(페이지 셋 · `README.md` · notes 한 커밋): AR-01 `changed=5 extra=1 pages=3/11 multi_page=1 mixed=1` + `README.md`, AR-02 `committed=1` 일곱 값 1, AP-01 `versions=8 hits=1`, AP-03 `committed=1 bare=1`, ER-02 `hidden_added` 셈 1
- AR-03 시작 판 `rc=0 broken0=1 nav=페이지 176 · 등록 176`, 없는 링크 넣은 판 `rc=1` · `깨진 링크 1 개`
- DG-02 시작 판 `js_bad=0 tag_bad=0 css_bad=0 md=absent` (11 쪽 쪽마다 `tag_bad=0`), 닫히지 않은 `div` 를 theming.html 에 커밋한 임시 복제본 `tag_bad=1`, 나쁜 임시 페이지 `tag_bad=1 css_bad=1` · `node --check` 종료 코드 1, `#bad heading` md 경고 2. DG-04 시작 판 `rc=0 11/11 PASS`, 나쁜 임시 페이지 `0/1 PASS` · 종료 코드 1
- DG-05 시작 판: `rc=0` 22 줄 · `feedback-agg-test SKIP (yq 없음)` 한 줄 (`ci-local.sh` 종료 코드 0). 교차 진단 반영 뒤 도우미로 다시 잰 값 `tool_same=1 rc0=22 other=[feedback-agg-test SKIP (yq 없음);]` (3 분 31 초). 다른 파일을 `CI_LOCAL` 로 주면 `tool_same=0`
- 원본 지문: 시작 판 SK-01 · 02 · 03 · 04 · 08 · 12 모두 `orch_same=1`. 임시 복제본에서 오케스트레이터 원본 끝에 한 줄을 더해 커밋하면 `orch_same=0`
- RE-01 · RE-02 양성 대조: 임시 복제본에 `docs/x-new.html` 과 theming.html 의 `<link rel="stylesheet" href="x.css">` 한 줄을 한 커밋에 넣으면 `added_files=1 ext_added=1`
- SC-00 · DG-01 시작 판 `release_paths=0` · `release_sh=0`, 임시 복제본에서 `scripts/release.sh` 를 고쳐 커밋하면 `release_paths=1` · `release_sh=1`(양성 대조). RE-01 · RE-02 시작 판 `added_files=0 ext_added=0`
- 계약에서 뗀 도우미가 작성 원본과 바이트까지 같다(`cmp` 종료 코드 0). 뗀 도우미로 다시 잰 `m SK-05` `stale=10` · `m SC-00` `release_paths=0` · `m AR-03` `rc=0` · `m DG-05` `rc0=22 other=[feedback-agg-test SKIP (yq 없음);]`

## 리서치 소스

- 저장소 안: 핸드오프 `.harness/handoff/2026-09-26-0110.md` §C3 · §운영 요령(본 체크아웃) · `.harness/.meta/kaizen-0924/final-notes.md` 「다음 사이클 메모」(FN-79 · FN-80) · 「교차 진단 2 회차 뒤 보강」 · `.harness/sprint-contract-kaizen-0924-final.md` `:107` · `:424`
- 측정 도구 원본: `/Users/jackson/Hub/10_Dev/claude-plugins/.harness/handoff/2026-09-26-tools/` 의 `coverage.py` · `fence2.py` · `ci-local.sh` (도우미의 `cov` · `fen` 은 앞 둘을 옛 판을 파일로 받게 옮긴 사본)
- 메모리: 「다시 만든 페이지는 옛 판 대비 담김으로 재라」 · 「CI 리눅스는 내 맥보다 화면을 더 나쁘게 그린다」
- 저장소 밖 원문은 쓰지 않았다
