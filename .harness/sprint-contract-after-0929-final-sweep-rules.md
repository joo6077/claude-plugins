---
feature: "마지막 정리 — 규칙 · 코드 · 시험 (fs1)"
slug: after-0929-final-sweep-rules
created: "2026-09-29 10:23"
complexity: "복잡"
conditions: 28
status: done
owner_session: bda55d45-296c-491f-89ba-b52042d58e72
conditions_digest: sha256:34a6430363f22fb0
measurement_digest: sha256:c360eda38254f32d
locked_at: "2026-09-29 10:37"
---

## 배경

- 묶음 fs1. 마지막 정리 목록 `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0928/.harness/.meta/after-kaizen-0928/final-sweep.md` 가운데 이 행들을 맡는다 — ex2 검토 1 · ex2 검토 2 · ex 남은 것(「레포 전체에서 같은 주장」 측정 관례) · dz 검토 1 · 2 · 3 · 4 · k1 남은 것 셋 · h1 검토 · lt 남은 것. 각 행의 출처는 같은 폴더의 `ex2-notes.md` · `dz-notes.md` 「독립 검토가 찾은 것」 · `k1-notes.md` 「남은 것」 · `h1-notes.md` 148~152 행 · `lt-notes.md` 「남은 것 (2 회차)」 이다.
- 이름 주의 (교차 진단 지적): 이 계약의 「k1」 은 `after-kaizen-0928/k1-notes.md` 의 검토다. `remaining.md` 에 나오는 「k1」 (react-animation · plan-sync-github 표기, preflight 표 등) 은 다른 회차의 다른 검토라 이 계약 범위가 아니다. 교차 진단이 `remaining.md` B12 · B7 · B4 를 대조했고 셋 다 BASE 에서 이미 풀렸거나 이 계약 파일과 무관했다.
- 사용자 위임: 2026-09-27T01:22:01.089Z 「자동으로 다 진행해 나한테 묻지 말고 …」 · 2026-09-28 「약점과 일부만 한 거 다처리하지??」 (세션 bda55d45-296c-491f-89ba-b52042d58e72). 결정 기록 `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0928/.harness/.meta/after-kaizen-0928/decisions.md`.
- 작업 폴더 `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak3-fs1` (가지 `chore/ak3-fs1`). 모든 측정은 이 폴더를 현재 폴더로 두고 돌린다. 기준 판(이하 BASE) `cacd9da3` — 가지를 만든 시점의 `chore/after-kaizen-0928`. 끝 판(이하 TIP)은 모든 커밋이 끝난 뒤 `git rev-parse chore/ak3-fs1` 의 출력이다. `HEAD` 를 상한으로 쓰지 않는다.
- 측정 묶음은 `.harness/.meta/after-0929-final-sweep-rules/` (이하 `$M`) 의 여섯 파일이다. 지문(sha256 앞 16 자리)은 `api-baseline.py dfdee5cbb3267ca7` · `bambu-nosl.sh 408752fe07c0f51e` · `ci-scope.sh 5e92e67976ba35f7` · `grid-rows.js 5e2282b2347f17ed` · `spec-neg.sh 009398b0848e1766` · `texts.sh dcf5d093fb0a69c0`. 봉인 커밋과 따로 커밋한다.
- 임시 폴더는 세션 scratch 아래 `TMPDIR` 로 준다. `node_modules` 는 작업 폴더에서 `npm ci` 로 만든다 (2026-09-29 실측 rc=0).
- 원본 문서를 바꾸면 대응 페이지도 같이 맞춘다 (레포 `.claude/skills/docs-site/SKILL.md`). 공통 CSS 링크 하나, 320 · 375 · 768 · 1280 넘침 0 (구조-03).

## GAP 분석

| 항목 | 출처 요지 | 저장소 자리 (BASE 에서 연 줄) | 결과 | 조건 |
| --- | --- | --- | --- | --- |
| ex2 검토 1 | X2(`ex/X2.md`): Apple 이 `.p8` 을 `.p12` 보다 권장한다는 문장은 원문에 없다. evals.json 83 행이 「'권장' 표현은 근거가 없다」 로 고쳐졌다 | `onboarding-kit/skills/setup-guide/references/search-strategy.md:88` 「`.p8` 을 권장한다는 사실로부터」 · `docs/onboarding-kit/search-strategy.html:407` 같은 문장 | 계약에 넣음 | 스킬-01 · 스킬-02 |
| ex2 검토 1 — 레포 전체에서 같은 주장 | 같은 전제가 다른 파일에도 있는가 | `git grep -nE '\.p8.{0,20}(을\|를) ?권장한다' -- . ':!.harness'` 가 BASE 에서 둘 — 위 두 줄. 같은 뜻의 다른 꼴로 `docs/kaizen/research-log.md:381` 「`.p8` 을 권장할 뿐」 (`git grep -n 'p8' -- . ':!.harness' \| grep '권장'` 으로 찾음). 더해 `.p8` 권장을 전제로 둔 줄 `docs/onboarding-kit/search-strategy.html:474` (나쁜 예 목록). `gate-g4-ko-*.md` 두 시험 파일의 「✅ 현재 권장: 인증 키(.p8)」 는 G4 가 잡아야 하는 나쁜 입력이다 | 두 줄 · 474 행은 계약에 넣음. research-log 는 그 사이클의 기록이라 두고, 시험 파일은 입력이라 둔다 | 스킬-01 · 스킬-02 |
| ex2 검토 2 | Firebase Flutter 설정 페이지에는 `.p8` 문구가 있어 「Firebase 문서는」 이 원문보다 넓다 | `onboarding-kit/skills/setup-guide/evals/evals.json:67` | 계약에 넣음 | 스킬-03 |
| ex 남은 것 | 원문 대조 계약은 항목마다 「레포 전체에서 같은 주장」 줄을 둔다 | `harness/references/contract-schema.md` §측정 관례 (1099~1163 행) 에 없음 · 대응 페이지 `docs/harness/contract-schema.html` `#measure-habits` 에도 없음 | 계약에 넣음 | 스킬-06 · 스킬-07 |
| ex 남은 것 — 새 규칙 넷 | 벽시계 문자열 모양 · PRD/ADR 경계 · 조회일/갱신일 분리 · 서비스 계정 선택 나무 | — | 하지 않음 — 사용자 확인 전 (범위 경계) | — |
| dz 검토 1 | 비교 화면 이름표를 지키는 시험이 없다. 여섯 시안 시험 넷은 `renderCompare()` 를 부르지 않는다 | `design-kit/evals/visuals.spec.js:1141~1195` — 비교 시험 0 개. 이름표를 빈 글자로 채우게 망가뜨린 사본에서도 시안 6 개 시험 `4 passed` (2026-09-29 실측) | 계약에 넣음 | 스크립트-02 |
| dz 검토 2 | 여섯째 투표 카드 · 메모 칸이 둘째 줄로 떨어진다 | `design-kit/templates/mockup.html:732` · `:809` `repeat(5, 1fr)`. `$M/grid-rows.js` 가 1280 폭에서 시안 6 · 8 개 모두 `vote_rows=2 note_rows=2` | 계약에 넣음 | 스크립트-01 · 스크립트-03 · 스킬-08 |
| dz 검토 3 | 참조 목록 줄이 「개수 상한」 옛 설명 | `design-kit/skills/design-mockup/SKILL.md:201`. 대응 페이지 `docs/design-kit/design-mockup.html:780` 은 「Variant Budget와 User-Reported Failure Gate」 라 옛 설명이 없다 | 원본은 계약에 넣음 · 페이지는 이미 됨 | 스킬-04 |
| dz 검토 4 | 「4 개 이상도 … 승인하면 정상 경로다」 가 시안 규칙(승인 없이 최소 5)과 어긋난다 | `harness/docs/guides/skill-design-guide.md:806` · `docs/harness/skill-design-guide.html:1143` | 계약에 넣음 | 스킬-05 |
| k1 남은 것 1 | 예시 계약에 비교 기준값 블록이 없어 「pending」 이 리포트 글로만 남는다 | `api-kit/evals/fixtures/unjudged/.api/contracts/users.me.yaml` — `baseline` 열쇠 0. 블록 모양 정의는 `api-kit/skills/api-contract/SKILL.md` §10 (253~263 행) | 계약에 넣음 | 스킬-09 |
| k1 남은 것 2 | 시험 파일에 벽 예산 값이 없어 `[미검증]` 이 한 줄 더 나온다 | `bambu-kit/evals/gate-fixtures/process-thin-unreadable-slot.json` — 열쇠 없음. 원본 완료 검사 출력 `fails=1 unv=2 wall=1 rc=1`. 표 `bambu-kit/skills/bambu-print-profile/SKILL.md:1938` · `docs/bambu-kit/bambu-print-profile.html:1722` 가 「`[미검증]` 2 줄 (슬롯 1 · 벽 예산 미기록)」 | 계약에 넣음 | 스킬-10 |
| k1 남은 것 3 | 슬라이서 없는 사본 대조를 측정 관례로 | §측정 관례 에 없음. 이 계약 자신도 슬라이서 없는 사본으로 잰다 (`$M/bambu-nosl.sh` BASE 값 `noslicer 결과: 28 경우 중 불일치 0 · 건너뜀 20 rc=0 left_paths=0`) | 계약에 넣음 | 스킬-06 · 스킬-07 · 스크립트-06 |
| h1 검토 | 작업 전체 · 워크플로 전체의 `if` · `env` · `defaults` 를 안 보고 레포 뿌리에서 돌린다 | `scripts/ci-local.sh:37-46`. `$M/ci-scope.sh` BASE 출력 — `FAIL a Where rc=1` · `FAIL b Never rc=3` · wf-env · wf-defaults 둘 다 `FAIL a One rc=1` | 계약에 넣음 | 스크립트-04 · 스크립트-05 · 오류-01 |
| lt 남은 것 | 경로 목록을 따옴표 없는 변수로 넘기면 zsh 에서 한 덩어리가 된다 — xargs · 배열로 | 같은 규칙이 `harness/references/contract-schema.md` §셸 이식성 규약 (v5.2 줄) 에 배열만 적혀 있고, 측정 명령 쪽 관례(§측정 관례)와 `xargs` 는 없다 | 계약에 넣음 (§측정 관례 한 자리로 모은다) | 스킬-06 · 스킬-07 |

## 범위 경계

- 하지 않는 것: 「ex 남은 것 — 새 규칙 넷」 — 사용자 확인 전이다. 보고 때 묻는다.
- 하지 않는 것: `.harness/` 아래 봉인된 계약 · QA 리포트 · 개정 파일. `docs/kaizen/research-log.md:381` 은 그 사이클의 기록이라 고치지 않는다. `onboarding-kit/skills/setup-guide/evals/fixtures/gate-g4-ko-sourced.md` · `gate-g4-ko-unsourced.md` 는 G4 가 잡아야 할 나쁜 입력이라 고치지 않는다.
- 하지 않는 것: api-kit 예시의 다른 네 계약(`auth.token` · `orders.list` · `products.inventory` · `products.list`)에 비교 기준값 블록을 더하는 일. 이번 항목은 보류 상태를 글로만 적은 `users.me` 하나다 (스킬-09 가 `others=0` 으로 잰다). 리포트 `reports/2026-09-02T1422-dev/report.md` 와 `ui.html` 은 바꾸지 않는다.
- 하지 않는 것: 판 번호 올리기 · 릴리스 · 변경 기록. 합친 뒤 main 에서 한다.
- 커밋 규칙: `git add <경로>` 뒤 `git commit -o <경로>`, 한 커밋에 맨 위 폴더 하나, 메시지 한국어, 끝에 빈 줄 뒤 서명 줄. `git add -A` · `git stash` · push · 가지 바꾸기 금지.
- 측정 관례 세 줄(스킬-06)의 굵은 머리 문장은 조건이 글자로 잰다. 뒤 설명 문장은 구현자가 쓰되, 각 줄에 적힌 낱말(`git grep` · `슬라이서` · `xargs` · `배열`)을 넣는다.
- 조건 수: 기능 조건 20 개 (가이드 「복잡」 9 ~ 20 안). 항목이 열두 줄이라 20 에 닿지만, 조건 하나가 한 파일 · 한 성질만 재도록 해서 나누지 않았다.
- 오라클 해소: 스킬-06 · 스킬-07 — 산출물이 계약 형식 문서의 문장 자체라 절을 잘라 글자를 세는 것이 곧 결과 관찰이다. 절 안 · 절 밖 사본 알려진 답으로 자르기가 자리를 가른다는 것을 보였다.
- 커버리지 해소: 구조-02 — 검출기가 짚은 `.harness/` 는 측정이 일부러 빼는 경로, `CF=…` 는 측정 변수 정의라 대상이 아니다. 스킬-07 — `<strong>…</strong>` 는 글자 모양 설명이지 경로가 아니다.
- 오라클 해소: 구조-02 · 구조-03 — 둘 다 명령(`git diff` · `check-docs-a11y.js`)을 실제로 돌려 출력과 종료 코드로 판정한다 (검출기가 산문 낱말을 잘못 짚었다).
- 범위 목록 (이 밖의 경로를 담은 커밋은 막힌다):

```text
# sprint-scope
onboarding-kit/skills/setup-guide/references/search-strategy.md
docs/onboarding-kit/search-strategy.html
onboarding-kit/skills/setup-guide/evals/evals.json
design-kit/templates/mockup.html
design-kit/evals/visuals.spec.js
design-kit/skills/design-mockup/SKILL.md
docs/design-kit/design-mockup.html
harness/docs/guides/skill-design-guide.md
docs/harness/skill-design-guide.html
harness/references/contract-schema.md
docs/harness/contract-schema.html
api-kit/evals/fixtures/unjudged/.api/contracts/users.me.yaml
bambu-kit/evals/gate-fixtures/process-thin-unreadable-slot.json
bambu-kit/skills/bambu-print-profile/SKILL.md
docs/bambu-kit/bambu-print-profile.html
scripts/ci-local.sh
scripts/test-ci-local.sh
```

## 회귀 게이트

- BASE 에서 잰 값 (2026-09-29): `bash $M/texts.sh $PWD` — `ss_old=1 ss_new=0 sh407_old=1 sh407_new=0 sh474_old=1 sh474_new=0 repo_p8_recommend=2 ev_old=1 ev_new=0 ev_json=ok dm201_old=1 dm201_new=0 dm_six_css=0 dp_six_css=0 sg_old=1 sg_new=0 sgh_old=1 sgh_new=0 bs_row=1 bs_row_unv1=0 bs_row_wall=1 bh_row_unv1=0 bh_row_wall=1 fx_key=None`, 측정 관례 열두 값 모두 0, `sec_lines md=58 html=39`. zsh · bash 출력 md5 같음.
- `$M/texts.sh` 절 자르기 알려진 답: 셋째 머리 문장을 §측정 관례 안에 넣은 사본은 `cs_l3=1 cs_file_l3=1 ch_l3=1`, 절 밖(§조건 작성 preflight 앞)에 넣은 사본은 `cs_l3=0 cs_file_l3=1` (2026-09-29 실측).
- `$M/api-baseline.py` 알려진 답: 맞는 블록을 붙인 사본 `block=1 state=pending nd=1 media=1 mode=1 lineage=1 extra=[] others=0` · 틀린 블록(digest 틀림 · `partial` · `accepted` · 열쇠 `foo`) 사본 `block=1 state=accepted nd=0 media=1 mode=0 lineage=1 extra=['foo'] others=0` · 없는 폴더 `STOP …` 종료 코드 2.
- `$M/grid-rows.js` BASE 여섯 줄: `n=5 w=1280 … vote_rows=1 vote_cols=5 … note_rows=1 note_cols=5 overflow=0` · `n=6 w=1280 … vote_rows=2 vote_cols=5 … note_rows=2 note_cols=5` · `n=8 w=1280 … vote_rows=2 vote_cols=5 … note_rows=2 note_cols=5` · 375 폭 셋은 스크립트-01 기대와 같다.
- `$M/spec-neg.sh` 준비 단계: `HEAD` 판에서 `label` → `applied=1` · `oldgrid` → `applied=2` · `none` → `rc=1 passed=0 failed=0` (아직 시험이 없어 「No tests found」). 통과 · 실패 수 읽기는 일부러 실패하는 시험 하나 · 통과 하나를 둔 사본에서 `passed=1 failed=1 rc=1` 로 확인했다.
- 전체 CI (BASE, 2026-09-29): `bash scripts/ci-local.sh $PWD` 끝 줄 `steps=44 run=39 skip=5 unsupported=0 failed=0` · 종료 코드 0, `PASS` 39 줄. 옛 도구 `summary.txt` 는 `feedback-agg-test SKIP (yq 없음)` 한 줄 말고 모두 `rc=0`.
- markdownlint-cli2 0.23.2 (`{ "config": { "MD013": false } }`) 로 바꿀 md 다섯 파일 BASE 경고 0. 나쁜 줄을 붙인 사본 6 개 · 종료 코드 1.

## Skill

- [ ] 스킬-01: `onboarding-kit/skills/setup-guide/references/search-strategy.md` 역방향 금지 문단이 `.p8` 을 「권장」 한다는 전제를 버리고 「안내」 로 적으며, 레포 안 같은 주장이 0 이다 [exact, enumerated]
  Given: 모든 커밋 뒤. 작업 폴더가 TIP 과 같다.
  측정: `bash $M/texts.sh $PWD` 출력에서 `ss_old=0` · `ss_new=1` · `repo_p8_recommend=0`. 새 글자는 「`.p8` 을 안내한다는 사실로부터 `.p8` 권장이나 `.p12` 의 deprecation 을」 이다. `repo_p8_recommend` 는 `git grep -nE '\.p8.{0,20}(을|를) ?권장한다' -- . ':!.harness' ':!docs/kaizen/research-log.md'` 줄 수다.
  양성 대조: BASE 값 `ss_old=1 ss_new=0 repo_p8_recommend=2`.
  측정 대상: `onboarding-kit/skills/setup-guide/references/search-strategy.md` (`texts.sh` 의 `SS`)
- [ ] 스킬-02: 대응 페이지 `docs/onboarding-kit/search-strategy.html` 두 자리가 원본과 같은 뜻으로 바뀐다 — 407 행 문장과 474 행 나쁜 예 목록 [exact, enumerated]
  Given: 모든 커밋 뒤.
  측정: `bash $M/texts.sh $PWD` 에서 `sh407_old=0` · `sh407_new=1` · `sh474_old=0` · `sh474_new=1`. 새 글자는 `<code>.p8</code>을 안내한다는 사실로부터 <code>.p8</code> 권장이나 <code>.p12</code>의 deprecation을` 과 `<li><code>.p8</code> 안내를 <code>.p8</code> 권장 · <code>.p12</code> deprecated로 부풀림 (출처보다 강한 주장)</li>` 이다.
  양성 대조: BASE 값 `sh407_old=1 sh407_new=0 sh474_old=1 sh474_new=0`.
- [ ] 스킬-03: `onboarding-kit/skills/setup-guide/evals/evals.json` 67 행 설명이 「Firebase iOS 설정 문서는 APNs 인증 키 업로드만 지시하고」 로 좁혀지고 파일이 JSON 으로 읽힌다 [exact]
  Given: 모든 커밋 뒤.
  측정: `bash $M/texts.sh $PWD` 에서 `ev_old=0` · `ev_new=1` · `ev_json=ok`.
  양성 대조: BASE 값 `ev_old=1 ev_new=0`.
- [ ] 스킬-04: `design-kit/skills/design-mockup/SKILL.md` 참조 목록 줄이 「§5.6 Variant Budget · §3.8 User-Reported Failure Gate — 개수 규칙·부대 산출물 금지·사용자 보고 규약의 기준 원본」 이다 [exact]
  Given: 모든 커밋 뒤.
  측정: `bash $M/texts.sh $PWD` 에서 `dm201_old=0` · `dm201_new=1`.
  양성 대조: BASE 값 `dm201_old=1 dm201_new=0`.
- [ ] 스킬-05: §5.6 트레이드오프 문단의 승인 경로 문장이 시안 밖 산출물에만 걸린다 — 원본 `harness/docs/guides/skill-design-guide.md` 와 페이지 `docs/harness/skill-design-guide.html` 두 곳 [exact, enumerated]
  Given: 모든 커밋 뒤.
  측정: `bash $M/texts.sh $PWD` 에서 `sg_old=0` · `sg_new=1` · `sgh_old=0` · `sgh_new=1`. 새 글자는 「— 시안 밖 산출물의 4 개 이상도, 3 축 변주도」 이다.
  양성 대조: BASE 값 `sg_old=1 sg_new=0 sgh_old=1 sgh_new=0`.
  측정 대상: `harness/docs/guides/skill-design-guide.md` (`SG`) · `docs/harness/skill-design-guide.html` (`SGH`)
- [ ] 스킬-06: `harness/references/contract-schema.md` §측정 관례 절(「#### 측정 관례」 머리부터 다음 `#### ` 머리 앞까지) 안에 세 줄이 있고 파일 전체에 각각 한 번만 있다 — (1) `**원문 대조 계약은 항목마다 「레포 전체에서 같은 주장」 줄을 둔다.**` 로 시작하고 같은 줄에 `git grep` (2) `**설치본이 있어야 도는 검사는 설치본을 지운 사본으로도 잰다.**` 와 같은 줄에 `슬라이서` (3) `**경로 목록을 따옴표 없는 변수로 넘기지 않는다.**` 와 같은 줄에 `xargs` · `배열` [exact, enumerated]
  Given: 모든 커밋 뒤.
  측정: `bash $M/texts.sh $PWD` 에서 `cs_l1=1 cs_l2=1 cs_l3=1` · `cs_file_l1=1 cs_file_l2=1 cs_file_l3=1`.
  양성 대조: BASE 값 여섯 모두 0. 알려진 답: 회귀 게이트 절 — 절 안 사본 `cs_l3=1`, 절 밖 사본 `cs_l3=0 cs_file_l3=1`.
- [ ] 스킬-07: 대응 페이지 `docs/harness/contract-schema.html` 의 `id="measure-habits"` 절(그 머리부터 다음 `<h3` 앞까지) 안에 스킬-06 의 세 머리 문장이 `<strong>…</strong>` 로 있고 같은 줄 낱말도 같으며, 페이지 전체에 각각 한 번만 있다 [exact, enumerated]
  Given: 모든 커밋 뒤.
  측정: `bash $M/texts.sh $PWD` 에서 `ch_l1=1 ch_l2=1 ch_l3=1` · `ch_file_l1=1 ch_file_l2=1 ch_file_l3=1`.
  양성 대조: BASE 값 여섯 모두 0. 알려진 답: 절 안 사본 `ch_l3=1`.
  측정 대상: `docs/harness/contract-schema.html` (`CH`)
- [ ] 스킬-08: 여섯째 시안 안내가 CSS 를 어떻게 하는지 적는다 — `design-kit/skills/design-mockup/SKILL.md` 「틀은 시안 칸 A~E 다섯을 기본으로 둔다.」 문단과 `docs/design-kit/design-mockup.html` 「여섯째 시안부터:」 줄 [structural, enumerated]
  Given: 모든 커밋 뒤.
  측정: `bash $M/texts.sh $PWD` 에서 `dm_six_css` 1 이상 · `dp_six_css` 1 이상.
  양성 대조: BASE 값 `dm_six_css=0 dp_six_css=0`.
  측정 대상: `design-kit/skills/design-mockup/SKILL.md` (`DM`) · `docs/design-kit/design-mockup.html` (`DP`)
- [ ] 스킬-09: api-kit 예시 계약 `users.me` 에 비교 기준값 블록이 있고 보류 상태를 담는다 — `state: pending`, `normalizedDigest` · `mediaType` · `lineage` 의 `env` · `branch` · `capturedAt` 이 스냅샷 `snapshots/dev/users.me.json` 의 manifest 와 같고, `extractionMode` 가 계약의 `mode` 와 같으며, `api-kit/skills/api-contract/SKILL.md` §10 에 없는 열쇠가 0 이다 [exact, enumerated]
  Given: 모든 커밋 뒤.
  측정: `python3 $M/api-baseline.py $PWD` 출력이 `block=1 state=pending nd=1 media=1 mode=1 lineage=1 extra=[] others=0`, 종료 코드 0.
  양성 대조: BASE 값 `block=0 state=None nd=0 media=0 mode=0 lineage=0 extra=[] others=0`. 알려진 답: 회귀 게이트 절 두 사본.
  측정 대상: `api-kit/evals/fixtures/unjudged/.api/contracts/users.me.yaml` · `snapshots/dev/users.me.json` · `api-kit/skills/api-contract/SKILL.md` §10 열쇠 아홉(`api-baseline.py` 의 `ALLOWED`) · `users.me`
- [ ] 스킬-10: 시험 파일 `bambu-kit/evals/gate-fixtures/process-thin-unreadable-slot.json` 이 벽 예산 값을 담아 원본 완료 검사가 `[미검증]` 을 슬롯 1 한 줄만 내고, 음성 대조 표 두 곳(`bambu-kit/skills/bambu-print-profile/SKILL.md` · `docs/bambu-kit/bambu-print-profile.html`)의 그 행이 「`[미검증]` 1 줄 (슬롯 1)」 로 맞춰진다 [exact, enumerated]
  Given: 모든 커밋 뒤.
  측정: `bash $M/texts.sh $PWD` 에서 `fx_key=0.00` · `bs_row=1 bs_row_unv1=1 bs_row_wall=0` · `bh_row_unv1=1 bh_row_wall=0`. `bash $M/bambu-nosl.sh $PWD` 의 셋째 줄이 `thin-unreadable fails=1 unv=1 wall=0 rc=1`.
  음성 대조: 표만 1 줄로 고치고 시험 파일은 BASE 그대로 둔 사본에서 `bash bambu-kit/evals/run-gate-fixtures.sh` 가 `불일치 process-thin-unreadable-slot.json —` 로 시작해 `기대 1 줄 · 결과 2 줄` 로 끝나는 줄을 내고 끝 줄 `결과: 28 경우 중 불일치 1` · 종료 코드 1 (2026-09-29 BASE 사본 실측).
  양성 대조: BASE 값 `fx_key=None bs_row_unv1=0 bs_row_wall=1` · `thin-unreadable fails=1 unv=2 wall=1 rc=1`.
  측정 대상: `bambu-kit/evals/gate-fixtures/process-thin-unreadable-slot.json` · `bambu-kit/skills/bambu-print-profile/SKILL.md` (`BS`) · `docs/bambu-kit/bambu-print-profile.html` (`BH`)

## Script

- [ ] 스크립트-01: 시안 틀 `design-kit/templates/mockup.html` 의 투표 카드 · 메모 칸이 1280 폭에서 시안 수만큼 한 줄에 놓이고, 375 폭 배치는 BASE 와 같다 — 시안 5 · 6 · 8 개 [exact, enumerated]
  Given: 모든 커밋 뒤. `npm ci` 를 한 작업 폴더.
  측정: `node $M/grid-rows.js design-kit/templates/mockup.html` 이 종료 코드 0 이고 출력 여섯 줄이 글자 그대로 아래와 같다.
  `n=5 w=1280 vote=5 vote_rows=1 vote_cols=5 note=5 note_rows=1 note_cols=5 overflow=0`
  `n=5 w=375 vote=5 vote_rows=5 vote_cols=1 note=5 note_rows=3 note_cols=2 overflow=0`
  `n=6 w=1280 vote=6 vote_rows=1 vote_cols=6 note=6 note_rows=1 note_cols=6 overflow=0`
  `n=6 w=375 vote=6 vote_rows=6 vote_cols=1 note=6 note_rows=3 note_cols=2 overflow=0`
  `n=8 w=1280 vote=8 vote_rows=1 vote_cols=8 note=8 note_rows=1 note_cols=8 overflow=0`
  `n=8 w=375 vote=8 vote_rows=8 vote_cols=1 note=8 note_rows=4 note_cols=2 overflow=0`
  양성 대조: BASE 틀(`git show cacd9da3:design-kit/templates/mockup.html` 을 scratch 에 둔 파일)에서 1280 폭 `n=6` · `n=8` 줄이 `vote_rows=2 vote_cols=5 … note_rows=2 note_cols=5` (2026-09-29 실측).
- [ ] 스크립트-02: `design-kit/evals/visuals.spec.js` 에 이름에 「비교」 가 든 시험이 하나 이상 있어, 여섯째 시안을 비교 쪽에 놓고 이름표 「시안 F」 를 확인하며 TIP 에서 통과한다 [exact]
  Given: 모든 커밋 뒤. `TIP=$(git rev-parse chore/ak3-fs1)`.
  측정: `bash $M/spec-neg.sh $PWD $TIP none` 이 `rc=0` · `failed=0` · `passed` 2 이상 (「비교」 하나 이상과 스크립트-03 의 「한 줄」 하나 이상).
  음성 대조: `bash $M/spec-neg.sh $PWD $TIP label` (왼쪽 이름표를 빈 글자로 채우게 바꾼 사본) 이 `applied=1` · `rc=1` · `failed` 1 이상.
- [ ] 스크립트-03: `design-kit/evals/visuals.spec.js` 에 이름에 「한 줄」 이 든 시험이 하나 이상 있어, 시안 8 개 틀의 1280 폭에서 투표 카드 · 메모 칸이 한 줄인지 재고 TIP 에서 통과한다 [exact]
  Given: 모든 커밋 뒤.
  측정: 스크립트-02 의 `none` 줄과 같다.
  음성 대조: `bash $M/spec-neg.sh $PWD $TIP oldgrid` (틀을 BASE 판으로 바꾼 사본) 이 `applied=2` · `rc=1` · `failed` 1 이상.
- [ ] 스크립트-04: `scripts/ci-local.sh` 가 작업 전체의 `if` · `env` · `defaults` 와 워크플로 전체의 `env` · `defaults` 가 걸린 run 단계를 돌리지 않고 `UNSUPPORTED` 로 알리며, 그런 열쇠가 없는 작업은 그대로 돈다 [exact, enumerated]
  Given: 모든 커밋 뒤.
  측정: `bash $M/ci-scope.sh scripts/ci-local.sh` 출력에서 — `== job` 아래 `^UNSUPPORTED a Where \(` 줄 1 개이고 그 줄에 `defaults` · `env` 가 든다, `^UNSUPPORTED b Never \(` 줄 1 개이고 그 줄에 `if` 가 든다, `PASS c Plain rc=0`, `steps=3 run=1 skip=0 unsupported=2 failed=0`, `rc=1`. `== wf-env` 아래 `^UNSUPPORTED a One \(` 줄에 `env`, `steps=1 run=0 skip=0 unsupported=1 failed=0`, `rc=1`. `== wf-defaults` 아래 `^UNSUPPORTED a One \(` 줄에 `defaults`, 같은 끝 줄, `rc=1`. `== plain` 아래 `PASS a One rc=0` · `PASS b Two rc=0` · `steps=2 run=2 skip=0 unsupported=0 failed=0` · `rc=0`. 출력 전체에 `FAIL ` 로 시작하는 줄 0.
  양성 대조: BASE 출력 — `FAIL a Where rc=1` · `FAIL b Never rc=3` · `FAIL a One rc=1` 두 번, `unsupported=0` 넷 (2026-09-29 실측).
- [ ] 스크립트-05: `scripts/test-ci-local.sh` 가 스크립트-04 의 작업 열쇠 · 워크플로 열쇠 경우를 담아 TIP 의 `scripts/ci-local.sh` 에서 통과하고, BASE 의 `scripts/ci-local.sh` 로 돌리면 실패한다 [exact]
  Given: 모든 커밋 뒤. BASE 사본은 `git show cacd9da3:scripts/ci-local.sh > <scratch>/ci-local-base.sh`.
  측정: `bash scripts/test-ci-local.sh` 종료 코드 0 이고 `^PASS ` 줄 6 이상 (BASE 4) · `^FAIL ` 줄 0.
  음성 대조: `CI_LOCAL=<scratch>/ci-local-base.sh bash scripts/test-ci-local.sh` 종료 코드 1 이고 `^FAIL ` 줄 1 이상. BASE 시험 파일로는 같은 명령이 `PASS` 4 · 종료 코드 0 이다 (2026-09-29 실측) — 새 경우가 없으면 이 대조가 통과해 버린다.
- [ ] 스크립트-06: 전체 CI 와 슬라이서 없는 사본이 통과한다 — (a) `scripts/ci-local.sh` 로 CI 파일 전 단계 (b) 옛 로컬 CI 도구 (c) 슬라이서 설치본 경로를 지운 SKILL.md 사본으로 bambu 완료 검사 시험 [exact, enumerated]
  Given: 모든 커밋 뒤. `TMPDIR` 은 scratch 아래 서로 다른 폴더.
  측정: (a) `bash scripts/ci-local.sh $PWD` 끝 줄이 `steps=44 run=39 skip=5 unsupported=0 failed=0` 이고 종료 코드 0 — CI 에만 있는 check-api-kit-docs · detect-docs-drift --check-table · check-cause-table-copies · measure-helpers-test · bambu 시험 둘 · Playwright 두 단계가 이 안에서 `PASS` 줄로 나온다. (b) `bash /Users/jackson/Hub/10_Dev/claude-plugins/.harness/handoff/2026-09-26-tools/ci-local.sh $PWD` 의 `summary.txt` 에서 `rc=` 가 0 아닌 줄 0, SKIP 은 `feedback-agg-test SKIP (yq 없음)` 한 종류. (c) `bash $M/bambu-nosl.sh $PWD` 의 첫 줄이 `here 결과: 28 경우 중 불일치 0 rc=0` 이고 둘째 줄이 `noslicer 결과: 28 경우 중 불일치 0 · 건너뜀 ` 로 시작하며 `rc=0 left_paths=0` 으로 끝난다.
  양성 대조: (c) 의 `left_paths=0` 과 `건너뜀` 수가 사본에서 설치본 경로가 실제로 사라졌음을 보인다 (BASE `건너뜀 20`). 판정이 틀린 입력은 슬라이서가 없어도 불일치로 잡는다 — k1 기록의 망가뜨린 사본 `불일치 1 · 건너뜀 18`.

## Error

- [ ] 오류-01: `scripts/ci-local.sh` 가 CI 파일이 없거나 읽을 수 없으면 BASE 처럼 종료 코드 2 로 멈춘다 — 파일 없음 · `jobs: []` · `jobs` 없음 세 경우 [exact, enumerated]
  Given: 모든 커밋 뒤. 세 폴더를 scratch 에 만든다 — `none/`(CI 파일 없음), `bad1/.github/workflows/ci.yml` 내용 `jobs: []`, `bad2/.github/workflows/ci.yml` 내용 `name: x`.
  측정: `bash scripts/ci-local.sh --list <폴더>` 종료 코드가 셋 모두 2 이고 표준 출력에 `steps=` 줄이 0.
  양성 대조: BASE 에서 셋 모두 종료 코드 2 (2026-09-29 실측, `bad1` · `bad2` 는 「CI 파일을 읽지 못했다」). 작업 열쇠를 읽는 코드가 `jobs` 값이 사전인지 보지 않으면 이 조건이 깨진다.
  측정 대상: `scripts/ci-local.sh` · `none/` · `bad1/.github/workflows/ci.yml` · `bad2/.github/workflows/ci.yml`

## Architecture

- [ ] 구조-01: BASE 뒤 가지 `chore/ak3-fs1` 의 모든 커밋이 병합 커밋이 아니고, 맨 위 폴더 하나만 건드리며, 서명 줄이 `Claude … <noreply@anthropic.com>` 모양이다 [exact, enumerated]
  Given: 모든 커밋 뒤. `TIP=$(git rev-parse chore/ak3-fs1)`.
  측정: `git rev-list --merges cacd9da3..$TIP | grep -c .` 이 0. `for c in $(git rev-list cacd9da3..$TIP); do n=$(git show --name-only --format='' $c | cut -d/ -f1 | LC_ALL=C sort -u | grep -c .); s=$(git log -1 --format='%(trailers:key=Co-Authored-By,valueonly)' $c | grep -cE '^Claude .+ <noreply@anthropic\.com>$'); [ "$n" = 1 ] && [ "$s" = 1 ] || echo "BAD $c n=$n s=$s"; done | grep -c BAD` 이 0. `git rev-list cacd9da3..$TIP | grep -c .` 이 1 이상.
  양성 대조: 같은 서명 세기를 `01b1cace` 에 돌리면 0 (GitHub 병합 커밋, 서명 줄 없음), 폴더 세기를 `a5152c5` 에 돌리면 17.
- [ ] 구조-02: BASE 에서 TIP 까지 바뀐 경로(`.harness/` 제외)가 전부 `## 범위 경계` 의 `# sprint-scope` 블록 안에 있다 [exact, enumerated]
  Given: 모든 커밋 뒤. `CF=.harness/sprint-contract-after-0929-final-sweep-rules.md`.
  측정: `comm -23 <(git diff --name-only cacd9da3 $TIP -- . ':(exclude).harness' | LC_ALL=C sort -u) <(awk '/^# sprint-scope$/{p=1;next} p&&/^```/{p=0} p' $CF | LC_ALL=C sort -u) | grep -c .` 이 0.
  양성 대조: 같은 `comm` 을 `git diff --name-only a5152c5~1 a5152c5` 에 돌리면 1 이상 (그 커밋은 `.harness` 밖 17 경로).
- [ ] 구조-03: 바꾼 문서 페이지 다섯이 공통 CSS 링크를 하나씩 가지고 접근성 · 넘침 검사를 통과한다 — `docs/onboarding-kit/search-strategy.html` · `docs/harness/skill-design-guide.html` · `docs/harness/contract-schema.html` · `docs/design-kit/design-mockup.html` · `docs/bambu-kit/bambu-print-profile.html` [exact, enumerated]
  Given: 모든 커밋 뒤.
  측정: 다섯 파일 각각 `grep -c 'href="../assets/site.css"' <파일>` 이 1. `node scripts/check-docs-a11y.js docs/onboarding-kit/search-strategy.html docs/harness/skill-design-guide.html docs/harness/contract-schema.html docs/design-kit/design-mockup.html docs/bambu-kit/bambu-print-profile.html` (경로를 낱낱이 적는다 — 변수 하나에 모아 넘기지 않는다) 이 종료 코드 0 이고 마지막 줄이 `5/5 PASS`.
  양성 대조: 너비 2000px 요소를 넣은 사본은 `FAIL … of=1680/1625/1232/720`, 종료 코드 1 (앞 계약 after-0928-external-facts-2 기록). BASE 에서 다섯 쪽 모두 `OK … of=0/0/0/0` · `5/5 PASS` (2026-09-29 실측).
  측정 대상: `docs/onboarding-kit/search-strategy.html` · `docs/harness/skill-design-guide.html` · `docs/harness/contract-schema.html` · `docs/design-kit/design-mockup.html` · `docs/bambu-kit/bambu-print-profile.html`

## Anti-patterns

- [ ] 금지-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수 (```text, ```bash, ```yaml 등). 판정 권위는 validate-plugin V6 상태기계다 — 여는/닫는 fence 가 동형이라 줄 단위 정규식으로는 판정 불가
  측정: `python3 scripts/validate-plugin.py --check=code-fence` 종료 코드 0.
- [ ] 금지-04: SKILL.md / agents/*.md frontmatter 에서 name 필드 누락 — validate-plugin V1 FAIL
  측정: `python3 scripts/validate-plugin.py --check=frontmatter` 종료 코드 0.

## Reusability

- [ ] 재사용-01: 시안 틀을 늘리는 시험 도우미가 `design-kit/evals/visuals.spec.js` 에 하나뿐이다 — 8 개 시안 시험도 같은 도우미로 만든다 [exact]
  측정: `grep -cF "/<div class=\"mockup-vote-card\" onclick=\"castVote\\('e'\\)\"" design-kit/evals/visuals.spec.js` 이 1 (BASE 1).
- [ ] 재사용-02: `scripts/ci-local.sh` 는 CI 파일을 한 번만 읽고, 작업 · 워크플로 열쇠도 그 읽기 안에서 본다 [exact]
  측정: `grep -c 'yaml.safe_load' scripts/ci-local.sh` 이 1 (BASE 1).

## Diagnostics

- [ ] 진단-01: N/A (commands.analyze 는 scripts/release.sh 만 잰다 — 이번 변경 파일과 교집합 0 개. 측정: `git diff --name-only cacd9da3 $(git rev-parse chore/ak3-fs1) | grep -c '^scripts/release.sh$'` 이 0)
- [ ] 진단-02: 바꾼 md 다섯 파일이 markdownlint 경고 0 개이고, 바꾼 셸 파일 둘이 shellcheck 경고 0 개다 — md: `onboarding-kit/skills/setup-guide/references/search-strategy.md` · `design-kit/skills/design-mockup/SKILL.md` · `harness/docs/guides/skill-design-guide.md` · `harness/references/contract-schema.md` · `bambu-kit/skills/bambu-print-profile/SKILL.md`, 셸: `scripts/ci-local.sh` · `scripts/test-ci-local.sh` [exact, enumerated]
  Given: 모든 커밋 뒤. 도구가 없으면 scratch 새 폴더에서 `npm install --no-save markdownlint-cli2@0.23.2`, 설정 `{ "config": { "MD013": false } }`.
  측정: md 파일마다 `markdownlint-cli2 --config <설정 파일> <경로>` 출력에서 `^<경로>:[0-9]+` 줄 수 0 · 종료 코드 0. `shellcheck scripts/ci-local.sh scripts/test-ci-local.sh` 종료 코드 0.
  양성 대조: 회귀 게이트 절 — 나쁜 줄을 붙인 md 사본 6 개 · 종료 코드 1. BASE 에서 다섯 md 0 개, 셸 둘 종료 코드 0 (2026-09-29 실측).
  측정 대상: `onboarding-kit/skills/setup-guide/references/search-strategy.md` · `design-kit/skills/design-mockup/SKILL.md` · `harness/docs/guides/skill-design-guide.md` · `harness/references/contract-schema.md` · `bambu-kit/skills/bambu-print-profile/SKILL.md` · `scripts/ci-local.sh` · `scripts/test-ci-local.sh`
- [ ] 진단-03: N/A (commands.test 는 scripts/release.sh 를 돌린다 — 이번 변경과 무관. 실제 시험은 스크립트-02 · 03 · 05 · 06 이 잰다)
- [ ] 진단-04: N/A (구동할 앱 · 서버가 없다 — 시안 틀은 브라우저로 스크립트-01 · 02 · 03 이, 문서 페이지는 구조-03 이 잰다)
