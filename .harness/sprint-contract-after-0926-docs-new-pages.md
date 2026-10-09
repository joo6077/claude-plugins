---
feature: "문서 사이트 새 페이지 일곱 (dcb) — DC-1 · UD-4"
slug: after-0926-docs-new-pages
created: "2026-09-26 21:04"
complexity: "복잡"
conditions: 25
status: done
owner_session: bda55d45-296c-491f-89ba-b52042d58e72
conditions_digest: sha256:d6913d6663e9d866
measurement_digest: sha256:f05972b9c937b756
locked_at: "2026-09-26 21:18"
---

## 배경

남은 일 목록 `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0926b/.harness/.meta/after-kaizen-0926b/leftovers.md`(읽기만, 기준 판 `6378948`)의 「## docs」 절 DC-1 과 「## user」 절 UD-4 를 한 묶음으로 처리한다. 대응 페이지가 없는 원본 일곱의 새 페이지를 만들고, `docs/index.html` 의 킷 목차(킷마다 있는 `categories` 의 `pages` 묶음)와 아이콘 함수에 올리고, 드리프트 도구(`scripts/detect-docs-drift.py`)의 짝 매핑이 일곱을 모두 새 페이지와 짝짓게 한다.

- 사용자 결정: `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0926b/.harness/.meta/after-kaizen-0926b/decisions.md`(읽기만) 17 번째 줄 — DC-1 · UD-4 「대응 페이지 없는 원본 일곱(부모가 정한 다섯 + `rust-kit/references/project-detection.md` · `phase-research-templates.md`) 모두 새 페이지」. 위임: 세션 `bda55d45-296c-491f-89ba-b52042d58e72` 의 사용자 말 2026-09-26T10:09:00.557Z 「123다실행해 그러면끝나?다음카이젠에왜넘기는데?」(앞서 여쭌 세 가지를 실행하고 다음 카이젠으로 넘긴 것도 지금 처리하라는 뜻), 결정 답 2026-09-26T10:30:16.222Z 「일곱 다 · 설계도 현행화」, 그 앞의 「나한테 물어보지 말고 자동으로 끝까지」(2026-09-24T04:04:16.964Z).
- 사용자 합의(Step 5): 위 위임으로 받은 것으로 적는다. 판단이 갈린 곳은 저장소 안 근거로 정해 `## GAP 분석` 과 `## 범위 경계` 에 적었다. 봉인된 조건을 느슨하게 하는 개정(허용 파일 늘리기 · 측정 대상 줄이기 · 문턱 낮추기)은 이 위임으로 동의 처리하지 않는다 — 개정 파일에 동의 칸을 비워 두고 부모가 사용자에게 묻는다.
- 작업 폴더 W = `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak2-dcb`, 가지 `chore/ak2-dcb`(`origin/main` `6378948` 에서 갈라짐). 범위 구간의 아래 끝은 이 계약의 봉인 커밋(이 계약 파일을 처음 담은 커밋)의 부모다 — 커밋 번호를 박지 않고 측정 도우미가 git 기록에서 푼다. 봉인 전 실측 때 그 자리는 `6378948` 이었다.
- 일곱 원본과 새 페이지(경로는 `find` 로 확인했다):

| 원본 | 새 페이지 | 킷 목차 |
| --- | --- | --- |
| `docs/api/research-log.md` | `docs/api-kit/research-log.html` | API Kit |
| `reflect-kit/skills/reflect-digest/SKILL.md` | `docs/reflect-kit/reflect-digest.html` | Reflect Kit |
| `tone-kit/references/adapter-contract.md` | `docs/tone-kit/adapter-contract.html` | Tone Kit |
| `tone-kit/references/adapter-dart-flutter.md` | `docs/tone-kit/adapter-dart-flutter.html` | Tone Kit |
| `tone-kit/references/locale-korean.md` | `docs/tone-kit/locale-korean.html` | Tone Kit |
| `rust-kit/references/project-detection.md` | `docs/rust-kit/project-detection.html` | Rust Kit |
| `.claude/skills/kaizen-orchestrator/references/phase-research-templates.md` | `docs/process/phase-research-templates.html` | Process |

- 페이지 이름: 앞 여섯은 드리프트 도구가 이미 내는 이름(`python3 scripts/detect-docs-drift.py --since 88ddfe5` 가 여섯 모두 `[NEW …]` 로 이 경로를 낸다)을 그대로 쓴다. 일곱째는 도구에 매핑이 없어 원본 이름을 따르고, 카이젠 절차 문서라 `docs/process/` 에 둔다(`SKILL.md:64` `process (공유)` 행의 출력 폴더).
- 만드는 법: 이 레포 `.claude/skills/docs-site/SKILL.md` 절차 — 틀 `.claude/skills/docs-site/references/page-template.html`, 공통 파일 `docs/assets/site.css` 링크 한 줄, 킷 색은 `references/css-tokens.md` 매핑. 구현 전에 `tone-kit:tone-guide` 1 단계(규칙 불러오기)를, 완료 선언 전에 5 단계(전수 대조)를 한다 — 새 페이지의 한국어 글과 스크립트 주석, notes 가 대상이다. 결과는 notes 에 남긴다(AR-08).
- 커밋 규칙: `git add <경로>` 뒤 `git commit -o <경로>` · 한 커밋에 킷 하나(문서 사이트에서는 `docs/<킷>/` 폴더 하나) · `git add -A` · `git stash` · push · 가지 바꾸기 금지. 본 체크아웃과 다른 워크트리는 건드리지 않는다. `.harness/` 파일은 구현 파일과 다른 커밋에 싣는다(AR-07).
- 기록 파일(notes): `.harness/.meta/after-kaizen-0926b/dcb-notes.md` (W 안, 이 가지에 커밋).
- 사용자가 할 일: 없음.

공통 전제 G (조건마다 되풀이하지 않는다) — 구현 · notes 커밋이 가지 `chore/ak2-dcb` 에 모두 들어간 뒤, 가지를 합치기 전에 잰다.
측정은 `## 회귀 게이트` 의 측정 도우미 `m <조건 ID>` 로 한다. 도우미는 끝점 `TIP`(가지 끝)과 시작점 `BASE`(봉인 커밋의 부모)를 `git archive` 로 풀어 잰다 — 작업 폴더의 커밋 안 된 변경은 보지 않는다(DG-02 의 `cli_rc` 와 DG-05 만 작업 폴더를 쓴다).
`HEAD` 를 상한으로 쓰지 않는다. `BASE` · `TIP` 해석이 안 되면 도우미가 `UNRESOLVED` 를 찍고 멈춘다.
「일곱 원본」 · 「새 페이지 일곱」 은 위 표이며 도우미 `SEVEN` 과 같은 글자다. 브라우저는 `file://` 로 연다.

복잡도 4 축 — 넷 모두 「예」 라 「복잡」 이다. Step 2.5 짝 조건을 넣었다.
기능 조건 17 개는 SK-01 · SC-01 ~ SC-03 · ER-01 ~ ER-03 · AR-01 ~ AR-09 · DG-05 이다 — Step 6.2 두 번째 명령이 `## Anti-patterns` 절(AP-03 · AP-04) · 자동 포함 여섯 줄(RE-01 · RE-02 · DG-01 ~ DG-04) · `N/A (` 줄을 빼고 센 값이다.
Step 2.5 짝 조건: 만드는 쪽은 드리프트 도구의 매핑(SC-01 · SC-02)과 사람이 읽는 매핑 표(`SKILL.md` Step 1, SK-01), 그리고 새 페이지 일곱(AR-01 · AR-03 · AR-04 · AR-05 · ER-01 · ER-02)이다. 쓰는 쪽은 페이지를 목차로 여는 `docs/index.html`(AR-02 · ER-03), 목차 등록을 읽어 짝을 판정하는 드리프트 도구 자신의 `resolve_target`(SC-01 이 등록 · 파일 존재까지 본다), 표와 스크립트 매핑을 맞대는 검사(SC-03 — 다른 묶음 vsa 가 더하는 `--check-table` 과 같은 식), 링크 · 고아 페이지 검사 `scripts/check-docs-links.py`(AR-02)다. 오케스트레이터 Step F2(`.claude/skills/kaizen-orchestrator/SKILL.md:614`)는 도구를 같은 명령으로 부르기만 해서 고칠 것이 없다 — 소비자 변경 없음.

| 축 | 물음 | 값 |
| -- | ---- | -- |
| 레이어 수 | 몇 개 계층을 관통하는가 | 셋 — 정적 문서 화면(HTML · CSS · 쪽 스크립트), 목차(`docs/index.html`), 원본과 페이지를 짝짓는 도구와 그 사람용 표 |
| 공개 API·계약 변경 | 외부에 노출된 약속이 바뀌는가 | 예 — 드리프트 도구가 고르는 짝이 하나 늘고, 매핑 표 행이 바뀐다. 목차에 일곱 항목이 는다 |
| 소비면 존재 | 반대편이 있는가 | 예 — 카이젠 Step F2, 목차 화면, 링크 · 고아 검사, 표 맞대기 검사 |
| 회귀 위험 | 기존 동작이 깨질 수 있는가 | 예 — 목차 id 가 겹치면(`project-detection` 은 flutter-toolkit 이 이미 씀, `docs/index.html:248`) 다른 페이지가 열리고, 매핑을 폴더째로 넣으면 페이지 없는 원본 둘이 새로 「NEW」 로 뜬다 |

설정 값 대조 (`.harness/project.yaml` 을 글자 그대로 옮김):

| config key | project.yaml 에서 읽은 값 | 계약에 쓴 값 |
| ---------- | ------------------------- | ------------ |
| `commands.analyze` | `bash -n scripts/release.sh` | DG-01 N/A — 재는 파일이 바뀐 파일에 없다 |
| `commands.test` | `bash scripts/release.sh 2>&1 \|\| true` | DG-03 N/A — 같은 이유 |
| `diagnostics.ide_exclude` | `[]` | DG-02 의 `([] 제외)` |
| `contract_categories[].id` / `prefix` | Skill/SK · Script/SC · Error/ER · Architecture/AR | 같은 넷 |
| `anti_patterns[].id` / `message` | AP-01 버전 하드코딩 · AP-02 force push · AP-03 bare code fence · AP-04 frontmatter name 누락 | AP-03 (고치는 `SKILL.md` 와 새 notes) · AP-04 (`SKILL.md` 를 고친다). AP-01 은 더하는 줄에 판 번호가 들어갈 자리가 없어서(표 행 · 매핑 한 줄 · 목차 줄 · 정적 페이지), AP-02 는 이 계약이 push 하지 않아서 뺐다 |

## GAP 분석 (Pre-Edit Audit)

대상 파일을 실제로 읽고 잰 값이다(시작 판 `6378948`).

| 대상 파일 | 실제 Read 증거 (`파일:라인`) | 발견한 기존 갭·위반 | 계약 조건화 |
| --------- | ---------------------------- | ------------------- | ----------- |
| `scripts/detect-docs-drift.py` | `:34-73` `SOURCE_TO_HTML`(`:52` `docs/tone/` · `:55` `reflect-kit/skills/` · `:58` `tone-kit/references/` · `:49` `rust-kit/references/` · `:67` `docs/api/`) · `:78-98` `SOURCE_OVERRIDES` · `:201-224` `map_source_to_html`(`SKILL` 이면 폴더 이름) · `:142-180` `resolve_target` | 여섯은 접두 매핑이 이미 이 페이지 이름을 내지만 등록 · 파일이 없어 `NEW`. `.claude/skills/kaizen-orchestrator/references/` 는 매핑이 없어 일곱째는 아예 안 나온다(도우미 `m SC-01` 시작 판 `seven_ok=0/7`, 일곱째 `unmapped`). 같은 폴더에 페이지 없는 원본 `phase-dependencies.md` · `search-sources.md` 가 있어 폴더째 매핑하면 둘이 거짓 `NEW` 가 된다(모의 판 `delta_n=3`) | SC-01 · SC-02 |
| `.claude/skills/docs-site/SKILL.md` | `:45-46` 「표를 고치면 스크립트의 매핑도 같은 커밋에서 고친다」 · `:48-64` 매핑 표(`:64` `process (공유)` · `(내부 문서)`) · `:16` Gotcha 1 공통 파일 한 줄 · `:23` Gotcha 8 400 줄 · `:24` Gotcha 9 출처 링크 · `:25-29` Gotcha 10 넘침 네 규칙 · `:30` Gotcha 11 자르지 말 것 · `:32` Gotcha 13 `dk-theme` · `:114-119` Step 5 등록 · `:131` 접근성 검사 | 표에 일곱째 원본이 없다(시작 판 `seven_in_table=6/7`). 표와 스크립트 어긋남은 시작 판 0. 편집기 경고 9(기존, 범위 밖) | SK-01 · SC-03 · AR-01 · AR-04 · AR-05 · RE-02 · DG-02 |
| `docs/index.html` | `:230` `categories` 시작 · `:455-479` Rust Kit · `:498-506` Reflect Kit · `:533-547` Tone Kit · `:549-565` API Kit · `:580-586` Process · `:618` `getIcon` · `:248` id `project-detection`(flutter-toolkit) · `:823-841` `buildNav`(항목마다 `data-id`) · `:845-874` `navigate`(iframe `src`) | 일곱 모두 등록 없음(`reg_ok=0/7`). id 겹침은 시작 판 0. 목차는 id 로 페이지를 찾으므로 겹치면 엉뚱한 페이지가 열린다(모의 판 `dup_ids=0->1` · `nav_items=2`) | AR-02 · ER-03 |
| `.claude/skills/docs-site/references/page-template.html` | `:2` `data-theme="dark"` · `:7` 공통 파일 링크 · `:19` 밝은 테마 블록 · `:87-102` 넘침 규칙(주석에만 `overflow:hidden`) · `:122` 단추 id `themeToggle` · `:150` `dk-theme` | 틀에는 숨김 선언이 주석 밖에 없다. 단추 id 가 `themeToggle` 이라 레포 접근성 검사(`scripts/check-docs-a11y.js:133` `#theme-btn`)가 틀로 만든 페이지의 단추 크기를 못 잰다(모의 판 `btn=none`) — 다른 묶음(dca) 이 notes 로 넘긴 일 | AR-01 · AR-05 · RE-02 · ER-02 |
| `.claude/skills/docs-site/references/css-tokens.md` | `:27-42` 킷별 `--accent` (API `#A3E635` · Reflect `#F43F5E` · Tone `#D946EF` · Rust `#E85D4A` · Process `#4ADE80`) | `docs/index.html:456` Rust 목차 점 색은 `#F97316` 로 표와 다르다 — 페이지 색은 표를 따른다(기존 Rust 페이지 `concurrency-guard-protocol.html` 도 `#E85D4A`) | AR-01 |
| `docs/api/research-log.md` | `:6` 제목 · `:8` · `:68` · `:154` 날짜 절 셋 · 코드 표시 111 · 주소 0 · 코드 블록 0 | 새 페이지 | AR-01 · AR-03 |
| `reflect-kit/skills/reflect-digest/SKILL.md` | `:15` 제목 · `:21` Gotchas · `:96` 네 축 · `:112` Process · `:158` · `:299` 출처 주소 · 코드 표시 195 · 주소 3 · 코드 블록 울타리 16 줄 | 새 페이지. 다른 묶음(vsa, VS-21)이 `:58` 한 줄을 고친다 | AR-01 · AR-03 · AR-04 · 범위 경계 |
| `tone-kit/references/adapter-contract.md` | `:1` 제목 · `:13` 축 모델 · `:25` 슬롯 정의 · `:72` 어댑터 현황 · 코드 표시 28 | 새 페이지 | AR-01 · AR-03 |
| `tone-kit/references/adapter-dart-flutter.md` | `:1` 제목 · `:17` 슬롯 값 · `:33` 규칙표 · `:55-153` 영역별 판정 · 코드 표시 202 · 코드 블록 울타리 14 줄 | 새 페이지 | AR-01 · AR-03 |
| `tone-kit/references/locale-korean.md` | `:1-8` 머리 설정 · `:10` 제목 · `:42` 규칙표 · `:149` 대조 grep · 주소 9 · 코드 표시 81 | 새 페이지 | AR-01 · AR-03 · AR-04 |
| `rust-kit/references/project-detection.md` | `:1` 제목 · `:7-199` Step 0 ~ 7 · `:40` · `:131` · `:143` 출처 주소 · 코드 표시 159 | 새 페이지. 목록 KR-1(`:147-148`) · KR-3(`:87`)이 이 원본을 고칠 예정(다른 묶음) | AR-01 · AR-03 · AR-04 · 범위 경계 |
| `.claude/skills/kaizen-orchestrator/references/phase-research-templates.md` | `:7` 제목 · `:13` 공통 원칙 · `:20-` Phase 절 · 주소 93 · 코드 표시 76 | 새 페이지. 목록 VS-16(`:261-262`) · VS-17(`:78` · `:130`) · VS-26(편집기 경고 12)이 이 원본을 고칠 예정(다른 묶음) | AR-01 · AR-03 · AR-04 · 범위 경계 |
| `scripts/check-docs-links.py` | `:1-24` 세 검사(깨진 상대 링크 · 고아 · 유령 등록 · 아이콘 누락) | 시작 판 통과(`links_rc=0`). 새 페이지가 킷 폴더 밖을 가리키는 상대 링크를 틀리면 잡힌다(모의 판 `links_rc=1`) | AR-02 |
| `scripts/check-api-kit-docs.py` | `:83` `research-log.md` 를 건너뜀 · `:25` `MIN_LINES = 450` · `:34` 공통 파일 링크도 외부로 셈(VS-14) | api 연구 기록 페이지는 이 검사 대상이 아니다. 시작 판 이미 `0/12 PASS`(다른 묶음 VS-14 몫) — 이 계약은 기대지 않는다 | 범위 경계 |
| `scripts/check-stale-values.py` | `:21` 검사 범위 설명 · `:49` `SOURCE_DIRS` · `:58` `kit_dirs`(`marketplace.json` 등록 킷만) · `:68` 합친 목록 | `.claude/skills/kaizen-orchestrator/references/` 는 등록 킷도 `SOURCE_DIRS` 도 아니어서 옛 값 검사가 이 원본을 재지 않는다(교차 진단이 찾음). DG-05 의 이 단계 통과는 새 process 쪽의 낡음에 대해 아무것도 증명하지 않는다 | 범위 경계(넘김) · AR-08 |
| `scripts/check-docs-a11y.js` | `:62` 폭 `[375, 768, 1280]` · `:133` `#theme-btn` · `:142` 합격 식 | 320 폭은 다른 묶음(dca, DC-2)이 더한다. 이 계약은 320 · 375 · 1280 × 두 테마를 도우미 `pw.js of` 로 따로 재고(ER-01), 레포 검사는 지금 판대로 부른다(ER-02) | ER-01 · ER-02 |

원본 담김 문턱(AR-03)의 근거 — 시작 판에서 드리프트 도구 매핑으로 짝지어지고 등록 · 파일이 있는 156 쌍을 같은 식(`coverage.py` · `fence2.py` 와 같은 글 뽑기)으로 쟀다. 사이트 전체 중앙값 낱말 비율 0.83 · 코드 표시 0.96 · 코드 블록 줄 0.80(블록 있는 111 쌍). 킷 중앙값: api-kit 0.91 · 1.00 · (블록 0.20) / reflect-kit 0.81 · 0.96 · 0.82 / tone-kit 0.95 · 1.00 · 0.80 / rust-kit 0.79 · 0.95 · 0.82. 페이지마다 문턱은 같은 킷 중앙값과 사이트 중앙값 가운데 큰 값이다(process 는 짝 있는 페이지가 없어 사이트 값). 원본에 코드 블록이 없으면 그 칸은 재지 않는다.

## Skill

- [ ] SK-01: docs-site 매핑 표가 일곱째 원본을 `docs/process/` 로 잇고, 표 밖은 한 글자도 바뀌지 않는다 (UD-4) — `.claude/skills/docs-site/SKILL.md` 의 바뀐 줄이 모두 `## Step 1:` 절 안의 표 행(`|` 로 시작)이고 빠진 줄 0 또는 1 · 더한 줄 정확히 1 이며, 표의 (원본, 출력 폴더) 짝이 일곱 원본 모두를 덮는다(원본과 같거나 `/` 로 끝나는 폴더 원본이 그 원본을 품고, 출력 칸이 새 페이지의 폴더와 같다). Given 공통 전제 G, When `m SK-01`, Then 첫 줄 `minus=0` 또는 `minus=1` 이고 `plus=1 nonrow=0 outside_step1=0`, 둘째 줄 `seven_in_table=7/7` [exact]
  측정: `m SK-01`. 시작 판 `minus=0 plus=0 nonrow=0 outside_step1=0` · `seven_in_table=6/7`(`NOT_IN_TABLE .claude/skills/kaizen-orchestrator/references/phase-research-templates.md`), 모의 좋은 판(`process (공유)` 행 원본 칸에 경로를 더함) `minus=1 plus=1 nonrow=0 outside_step1=0` · `seven_in_table=7/7`
  양성 대조: 모의 나쁜 판(Gotcha 2 문장 한 글자를 바꿈) → `nonrow=2 outside_step1=2` (봉인 전 실측)

## Script

- [ ] SC-01: 드리프트 도구가 일곱 원본을 바뀐 파일로 받으면 각각 새 페이지 하나를 등록 · 파일 있음으로 고른다 (DC-1 · UD-4) — 도우미가 끝점 트리의 `scripts/detect-docs-drift.py` 를 불러 바뀐 파일 목록만 일곱 원본으로 바꿔 끼우고 `detect_drift` 를 그대로 돌린다(매핑 · 목차 대조 · 파일 확인은 도구 자신의 코드). Given 공통 전제 G, When `m SC-01`, Then 일곱 줄이 모두 `OK` 이고 끝줄 `seven_ok=7/7` — 줄마다 고른 쪽이 정확히 하나, 그 경로가 `## 배경` 표의 새 페이지와 같고 `registered=1 exists=1` [exact, enumerated]
  측정: `m SC-01`. 시작 판 `seven_ok=0/7`(여섯은 `(…, 0, 0)`, 일곱째 `unmapped`), 모의 좋은 판 `seven_ok=7/7`
  양성 대조: 모의 나쁜 판(두 쪽만 만들고 등록, 일곱째를 폴더째 매핑) → `seven_ok=2/7` (봉인 전 실측)
- [ ] SC-02: 드리프트 도구 매핑에서 달라진 원본은 일곱째 하나뿐이다 — 시작 판과 끝점 트리의 모든 파일(두 트리 합집합, `node_modules` · `.git` 제외)에 두 판의 매핑(`SOURCE_OVERRIDES` 우선, 없으면 `map_source_to_html`)을 돌려 결과가 다른 원본이 정확히 `.claude/skills/kaizen-orchestrator/references/phase-research-templates.md` 하나이고 그 결과가 `['docs/process/phase-research-templates.html']` 이며, `SOURCE_EXCLUDES` 는 그대로다. Given 공통 전제 G, When `m SC-02`, Then `DELTA .claude/skills/kaizen-orchestrator/references/phase-research-templates.md: [] -> ['docs/process/phase-research-templates.html']` 한 줄과 `delta_n=1 excludes_same=1` [exact]
  측정: `m SC-02`. 시작 판 `delta_n=0 excludes_same=1`, 모의 좋은 판(파일 경로 한 줄 매핑) 위 기대값과 같음
  양성 대조: 모의 나쁜 판(`.claude/skills/kaizen-orchestrator/references/` 폴더째 매핑) → `delta_n=3`(`phase-dependencies.md` · `search-sources.md` 가 없는 페이지를 가리킴) (봉인 전 실측)
- [ ] SC-03: 매핑 표와 스크립트 매핑이 서로를 덮는다 — 스크립트의 (원본, 출력 폴더) 짝마다 표에 같은 짝 또는 그것을 품는 폴더 짝이 있고 그 반대도 같다(다른 묶음 vsa 가 더하는 `--check-table` 과 같은 판정). Given 공통 전제 G, When `m SC-03`, Then `seven_in_table=7/7 mismatch=0->0` [exact]
  측정: `m SC-03`. 시작 판 `seven_in_table=6/7 mismatch=0->0`, 모의 좋은 판 `seven_in_table=7/7 mismatch=0->0`
  양성 대조: 모의 나쁜 판(스크립트만 고치고 표는 그대로) → `mismatch=0->1` (봉인 전 실측)

## Error

- [ ] ER-01: 새 페이지 일곱이 320 · 375 · 1280 폭 × 밝은 · 어두운 테마 여섯 칸 모두에서 가로로 넘치지 않고, 두 테마가 실제로 다르게 그려진다 (DC-1) — 도우미 `pw.js of` 가 쪽마다 두 테마 각각 브라우저 색 설정 · `dk-theme` 저장값 · `data-theme` 을 맞춰 연 뒤 세 폭에서 `max(html, body)` 의 `scrollWidth - clientWidth` 를 잰다. Given 공통 전제 G, When `m ER-01`, Then 일곱 줄이 모두 `OK` 이고 각 칸 값이 `0` · `theme_differs=1`, 끝줄 `of_ok=7/7 cells_zero=42/42` [exact, enumerated]
  측정: `m ER-01`. 시작 판 `of_ok=0/7 cells_zero=0/0`(쪽 없음), 모의 판 `docs/tone-kit/locale-korean.html`(기존 쪽 사본) `d320=0 d375=0 d1280=0 l320=0 l375=0 l1280=0 theme_differs=1`
  양성 대조: 모의 나쁜 판(폭 1900px 블록을 넣은 쪽) → `d320=1580 … l1280=620` · `BAD` (봉인 전 실측)
- [ ] ER-02: 레포 접근성 검사가 새 페이지 일곱을 모두 통과한다 — `node scripts/check-docs-a11y.js` 에 일곱 쪽을 넘기면(375 · 768 · 1280 넘침 · 콘솔 오류 · 모든 글자 요소 대비 · 밝은 테마 규칙 유무) 줄마다 `OK` 이고 `theme=both` 다. Given 공통 전제 G, When `m ER-02`, Then `absent=0` · `a11y_rc=0 ok_both=7/7` [exact]
  측정: `m ER-02`(끝점 트리에서 레포 검사기를 그대로 부름). 시작 판 `absent=7` · `a11y_rc=none ok_both=0/7`, 모의 판 기존 쪽 사본 `OK … theme=both`
  양성 대조: 모의 나쁜 판 `docs/api-kit/research-log.html`(외부 스타일 링크 · 넓은 블록) → `FAIL … err=1` · `a11y_rc=1` (봉인 전 실측)
- [ ] ER-03: 목차에서 새 페이지 일곱을 누르면 각 페이지가 뜬다 — 1280 폭으로 `docs/index.html` 을 열어, 끝점 `docs/index.html` 에서 그 파일을 가리키는 항목의 id 로 `.nav-item[data-id=…]` 를 하나 찾아 누르면, 주소가 그 파일로 끝나는 iframe 이 생기고 그 안의 글이 1000 자를 넘고 문서 제목이 비지 않는다. Given 공통 전제 G, When `m ER-03`, Then 일곱 줄 `OK` · 끝줄 `nav_ok=7/7 console_err=0` [exact, enumerated]
  측정: `m ER-03`. 시작 판 `nav_ok=0/7`(목차 항목 없음 `nav_items=0`), 모의 좋은 판 `nav_ok=7/7 console_err=0`
  양성 대조: 모의 나쁜 판(api 연구 기록 페이지를 이미 쓰는 id `tone-overview` 로 등록) → `nav_items=2` · `BAD` (봉인 전 실측)

## Architecture

- [ ] AR-01: 새 페이지 일곱이 새 파일로 들어가고 문서 사이트 틀을 지킨다 (DC-1) — 일곱 경로가 `BASE`→`TIP` 차이에서 추가(`A`)이고, 쪽마다 `wc -l` 과 같은 줄 수가 400 이상(`SKILL.md:23` Gotcha 8), `../assets/site.css` 를 가리키는 `<link>` 가 정확히 하나이면서 첫 `<style` 앞에 있고(Gotcha 1), 그 밖의 외부 리소스(다른 `<link>` · `<script src=` · `@import` · `url(http…)`)가 0, `:root` 의 `--accent` 가 `css-tokens.md` 의 킷 값(API `#A3E635` · Reflect `#F43F5E` · Tone `#D946EF` · Rust `#E85D4A` · Process `#4ADE80`)과 같다. Given 공통 전제 G, When `m AR-01`, Then `added=7/7` 과 끝줄 `exist=7/7 lines=7/7 css1=7/7 ext0=7/7 accent=7/7` [exact, enumerated]
  측정: `m AR-01`. 시작 판 `added=0/7` · `exist=0/7 …`, 모의 판 기존 쪽 사본 `lines=526 site_css=1 before_style=1 ext=0 accent=#D946EF`
  양성 대조: 모의 나쁜 판(틀에 외부 스타일 링크를 더하고 색을 비움, 159 줄) → `ext=1 accent=None lines=159` (봉인 전 실측)
- [ ] AR-02: 새 페이지 일곱이 각자 킷 목차에 한 번씩 오르고 아이콘을 가지며 id 가 겹치지 않는다 (DC-1) — 끝점 `docs/index.html` 의 `categories` 에서 `file:` 이 그 쪽인 항목이 정확히 하나이고 그 항목이 든 묶음의 `label` 이 `## 배경` 표의 킷 목차 이름(`API Kit` · `Reflect Kit` · `Tone Kit` · `Rust Kit` · `Process`)으로 시작하며, `getIcon` 에 그 id 키가 있고, 사이트 전체에서 두 번 이상 쓰인 id 가 시작 판보다 늘지 않는다. `docs/index.html` 차이는 더한 줄 14(쪽마다 목차 한 줄 · 아이콘 한 줄) · 빠진 줄 0 이다. 레포 링크 검사(`scripts/check-docs-links.py` — 깨진 상대 링크 · 고아 · 유령 등록 · 아이콘 누락)가 끝점 트리에서 종료 코드 0 이다. Rust Kit 쪽 id 는 flutter-toolkit 이 이미 쓰는 `project-detection`(`docs/index.html:248`)과 겹치지 않게 `project-detection-rust` 로 한다. Given 공통 전제 G, When `m AR-02`, Then `reg_ok=7/7 icon_ok=7/7 dup_ids=0->0 added=14 deleted=0` · `links_rc=0` [exact, enumerated]
  측정: `m AR-02`. 시작 판 `reg_ok=0/7 icon_ok=0/7 dup_ids=0->0 added=0 deleted=0` · `links_rc=0`, 모의 좋은 판 `reg_ok=7/7 icon_ok=7/7 dup_ids=0->0 added=14 deleted=0`
  양성 대조: 모의 나쁜 판 → `dup_ids=0->1`, 다른 폴더에 둔 기존 쪽 사본의 상대 링크 → `links_rc=1` (봉인 전 실측)
- [ ] AR-03: 새 페이지가 원본을 기존 페이지 수준 이상으로 담는다 (DC-1) — 쪽마다 원본 낱말(백틱 밖 2 자 이상 낱말) 가운데 쪽 글에 든 비율, 원본 코드 표시(백틱) 가운데 쪽 글에 든 비율, 원본 코드 블록 줄(공백 뺀 8 자 이상) 가운데 쪽 글(공백 뺌)에 든 비율이 도우미 `SEVEN` 의 문턱 이상이다. 문턱(낱말 · 코드 표시 · 코드 블록 줄): `docs/api-kit/research-log.html` 0.91 · 1.00 · 없음 / `docs/reflect-kit/reflect-digest.html` 0.83 · 0.96 · 0.82 / `docs/tone-kit/adapter-contract.html` 0.95 · 1.00 · 없음 / `docs/tone-kit/adapter-dart-flutter.html` 0.95 · 1.00 · 0.80 / `docs/tone-kit/locale-korean.html` 0.95 · 1.00 · 0.80 / `docs/rust-kit/project-detection.html` 0.83 · 0.96 · 0.82 / `docs/process/phase-research-templates.html` 0.83 · 0.96 · 없음 (근거는 `## GAP 분석` 끝 문단). 비율은 소수 둘째 자리로 반올림해 견준다. Given 공통 전제 G, When `m AR-03`, Then 일곱 줄 `OK` · `cov_ok=7/7` [exact, enumerated]
  측정: `m AR-03`. 시작 판 `cov_ok=0/7`(쪽 없음)
  알려진 답: 기존 쌍 `rust-kit/references/concurrency-guard-protocol.md` → `docs/rust-kit/concurrency-guard-protocol.html` 을 같은 식으로 재면 `wr=0.92 code=33/35 fence=14/18` 이고, 인계 도구 `coverage.py`(`wr=0.92->0.92 codes=35 new=33`) · `fence2.py`(`lines=18 in_new=14`)와 같다 (봉인 전 실측, 종료 코드 0)
  양성 대조: 모의 나쁜 판(기존 쪽 사본을 locale-korean 자리에) → `wr=0.32 code=19/81 fence=0/16` · `BAD` (봉인 전 실측)
- [ ] AR-04: 원본의 출처 주소가 모두 쪽의 링크로 옮겨진다 (`SKILL.md:24` Gotcha 9) — 원본 일곱의 `http(s)://` 주소(끝의 `.,;:` 뺌, 합계 108 개: reflect-digest 3 · locale-korean 9 · project-detection 3 · phase-research-templates 93 · 나머지 0)가 각 쪽의 `href="…"` 로 모두 있다. Given 공통 전제 G, When `m AR-04`, Then 일곱 줄 `OK` · `url_ok=7/7 src_urls_total=108` [exact, enumerated]
  측정: `m AR-04`. 시작 판 `url_ok=0/7 src_urls_total=0`(쪽 없음 — 주소 수는 쪽이 있을 때만 더함), 원본 주소 수는 봉인 전 같은 식으로 108
  양성 대조: 모의 나쁜 판(기존 쪽 사본을 locale-korean 자리에) → `src_urls=9 missing=5` (봉인 전 실측)
- [ ] AR-05: 넘침을 가려서 없애지 않는다 (`SKILL.md:30` Gotcha 11) — 일곱 쪽의 `<style>` 안과 `style=""` 속성(CSS 주석 뺌)에 `overflow`(`-x` · `-y` 포함) `hidden` · `clip` 선언과 `text-overflow:ellipsis` 가 0 이다. Given 공통 전제 G, When `m AR-05`, Then 끝줄에 `hide0=7/7` [exact]
  측정: `m AR-05`. 시작 판 `hide0=0/7`(쪽 없음), 틀 사본 `hide=0`(틀의 `overflow:hidden` 은 주석 안)
  양성 대조: 모의 나쁜 판(`.x{overflow:hidden}` 한 줄) → `hide=1` (봉인 전 실측)
- [ ] AR-06: 바뀐 파일이 정확히 열이고 계약 봉인이 깨지지 않는다 — `git diff --name-status BASE TIP -- . ':(exclude).harness'` 의 경로 집합이 새 페이지 일곱과 `.claude/skills/docs-site/SKILL.md` · `docs/index.html` · `scripts/detect-docs-drift.py` 열과 정확히 같고(더 많지도 적지도 않음), 상태가 추가 7 · 수정 3, 전체 차이(`.harness` 포함)에 PNG 0 이다. `.harness/` 는 이름을 열거하지 않고 끝점 트리의 `sprint-contract*.md` 모두에 봉인 검사를 돌려 `SEAL_BROKEN` 이 0 이다. Given 공통 전제 G, When `m AR-06`, Then `extra=0 missing=0 png=0 status=A7 M3` · `seal_broken=0` [exact, enumerated]
  측정: `m AR-06`. 시작 판 `extra=0 missing=10 png=0` · `seal_broken=0`, 모의 좋은 판 `extra=0 missing=0 png=0 status=A7 M3`
  양성 대조: 모의 나쁜 판 → `extra=2 png=1`(`docs/cap.png` · `scripts/new-check.py`), 앞 계약 조건 줄 끝에 글자를 더한 판 → `seal_broken=1` (봉인 전 실측)
- [ ] AR-07: 커밋이 문서 킷 폴더 둘을 섞지 않고 `.harness/` 와 구현 파일을 섞지 않는다 — `BASE` 부터 `TIP` 까지 병합 아닌 커밋 가운데 `docs/<폴더>/` 둘 이상을 담은 커밋 0, `.harness/` 파일과 그 밖의 파일을 함께 담은 커밋 0, 구현 커밋 1 이상. Given 공통 전제 G, When `m AR-07`, Then `multi_docs_folder=0 mixed=0` 이고 `impl_commits` 1 이상 [exact]
  측정: `m AR-07`. 시작 판 `commits=0 impl_commits=0 multi_kit=0 multi_docs_folder=0 mixed=0`
  양성 대조: 모의 나쁜 판(notes · `docs/tone-kit/` · `docs/api-kit/` 를 한 커밋에) → `multi_docs_folder=1 mixed=1` (봉인 전 실측)
- [ ] AR-08: 결정과 넘김을 notes 에 남긴다 — Given 끝점 `TIP`, notes 가 커밋돼 있고 열세 토큰 `DC-1` · `UD-4` · `tone-guide` · `VS-13` · `VS-16` · `VS-17` · `VS-21` · `KR-1` · `KR-3` · `check-api-kit-docs` · `DC-2` · `DC-9` · `check-stale-values` 가 각각 한글 15 자 이상인 줄에 1 번 이상 든다. 담을 내용: 일곱 페이지와 페이지 이름 · 목차 id 를 정한 까닭(DC-1 · UD-4), `tone-guide` 1 · 5 단계 결과, 매핑 표 `process (공유)` 행을 VS-13(다른 묶음 vsa)도 고쳐 합칠 때 한 줄이 부딪힌다는 것과 합친 행에 둘 원본, 그 행이 목록 DC-9(매핑 규칙 결정)의 `process (공유)` 몫과 어떻게 이어지는지, 원본을 고칠 다른 묶음(VS-16 · VS-17 · VS-21 · KR-1 · KR-3)이 합쳐진 뒤 드리프트 도구로 다시 맞춰야 하는 쪽, 옛 값 검사 `check-stale-values` 가 오케스트레이터 참고 문서 폴더를 재지 않는다는 것, `check-api-kit-docs` 가 연구 기록을 건너뛰고 지금 0/12 인 것, 320 폭 검사는 DC-2(dca)가 레포 검사기에 넣고 이 묶음은 도우미로 따로 잰 것. Given 공통 전제 G, When `m AR-08`, Then `committed=1` 이고 열세 값 모두 1 이상 [exact, enumerated]
  측정: `m AR-08`. 시작 판 `committed=0` · `notes=absent`, 모의 notes `committed=1` 과 열세 값 1
  양성 대조: 토큰만 짧게 적은 줄의 notes → `DC-1=0 UD-4=0 tone-guide=0` (봉인 전 실측). 열세 토큰으로 늘린 뒤 다시 잼: 짧은 줄 notes → `VS-17=0 KR-3=0`, 열세 토큰을 한글 15 자 넘는 줄에 담은 notes → 열세 값 모두 `1`. 평가자는 셈이 잡은 줄마다 그 줄이 실제로 그 결정이나 넘김을 설명하는지 한 번 눈으로 읽는다 — 토큰을 끼워 넣은 빈말 줄이면 그 값은 0 으로 본다
- [ ] AR-09: 새 페이지를 브라우저로 캡처해 눈으로 확인했고 캡처는 커밋하지 않았다 — notes 에 `캡처 폴더: \`<절대 경로>\`` 한 줄이 있고, 그 폴더에 새 페이지마다 `320` · `375` · `1280` 세 폭 × `dark` · `light` 캡처가 이름 규칙 `<docs 아래 폴더>__<쪽 이름>-<폭>-<테마>.png` 로 모두 있고 비어 있지 않으며, 규칙 밖 이름의 PNG 가 0 이다. PNG 가 커밋되지 않은 것은 AR-06 `png=0` 이 잰다. Given 공통 전제 G, When `m AR-09`, Then `cap_need=42 cap_have=42 cap_badname=0` [exact, collective]
  측정: `m AR-09`. 시작 판 `cap_dir=absent`, 모의 판(42 장 중 한 장을 빼고 이름 틀린 한 장을 넣음) `cap_need=42 cap_have=41 cap_badname=1`
  양성 대조: 위 모의 판 (봉인 전 실측)

## Anti-patterns

- [ ] AP-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수 (```text, ```bash, ```yaml 등). 판정 권위는 validate-plugin V6 상태기계다 — 여는/닫는 fence 가 동형이라 줄 단위 정규식으로는 판정 불가
  이 계약에 적용: 고치는 `.claude/skills/docs-site/SKILL.md` 와 새 notes 의 언어 표시 없는 여는 울타리 수가 늘지 않는다. 측정: `m AP-03` 이 `dcb-notes.md=absent->0 SKILL.md=0->0`(시작 판 `SKILL.md=0`), 킷 전체는 DG-05 의 `validate-plugin rc=0`. 양성 대조: 언어 없는 울타리를 넣은 모의 notes → `dcb-notes.md=absent->1` (봉인 전 실측)
- [ ] AP-04: SKILL.md / agents/*.md frontmatter 에서 name 필드 누락 — validate-plugin V1 FAIL
  이 계약에 적용: 고치는 `.claude/skills/docs-site/SKILL.md` 의 첫 머리 설정에 `name` 이 그대로 있다. 측정: `m AP-04` 가 `fm_name=docs-site`(시작 판 같은 값). 머리 설정이 바뀌면 SK-01 `outside_step1` 이 잡는다

## Reusability

- [ ] RE-01: N/A (산출물이 정적 문서 페이지 · 목차 줄 · 매핑 한 줄 · 표 한 행이라 비공개로 숨길 재사용 단위 코드가 없다. 쪽 스크립트는 틀의 테마 전환을 그대로 쓴다 — RE-02 가 잰다. 측정: `m AR-06` 의 바뀐 파일 열 가운데 `.js` · `.py` · `.sh` 새 파일 0 — `m RE-02` 의 `new_scripts=0`)
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다
  이 계약에 적용: 새 페이지 일곱이 틀의 테마 전환(`dk-theme` 키)과 밝은 테마 규칙(`[data-theme="light"]`)을 쓰고, 공통 파일이 맡는 움직임 줄이기를 쪽에 다시 적지 않으며(`prefers-reduced-motion` 0, `SKILL.md:16`), 새 스크립트 · 스타일 파일을 더하지 않는다. 측정: `m RE-02` 가 `theme=7/7 light=7/7 rm0=7/7` · `new_scripts=0`(시작 판 `theme=0/7 light=0/7 rm0=0/7` · `new_scripts=0`). 양성 대조: 모의 나쁜 판(`prefers-reduced-motion` 을 쪽에 적음) → `rm=1` (봉인 전 실측)

## Diagnostics

- [ ] DG-01: N/A (commands.analyze `bash -n scripts/release.sh` 가 재는 `scripts/release.sh` 는 이번 바뀐 파일에 없다. 측정: `m DG-01` 이 `release_paths=0`. 스크립트 쪽 실제 검사는 DG-02 의 `py_compile` · `cli_rc` 와 DG-05) [exact]
- [ ] DG-02: IDE diagnostics 워닝/인포 0개 ([] 제외)
  편집기 진단을 명령줄로 같게 잰다(계약 · QA 리포트 · 개정 파일은 뺀다): 새 페이지 일곱과 `docs/index.html` 가운데 짝 안 맞는 HTML 태그 수가 시작 판보다 늘어난 파일 0, notes 의 markdownlint-cli2 0.23.2(MD013 끔, 편집기 확장과 같은 설정) 경고 0, `SKILL.md` 경고 수가 시작 판 9 이하(범위 밖 기존 경고 — UD-7 · VS-26 묶음 몫), `scripts/detect-docs-drift.py` 의 `python3 -m py_compile` 출력 0 줄, W 에서 `python3 scripts/detect-docs-drift.py --since BASE` 종료 코드 0. 측정: `m DG-02` 가 `tag_worse=0 md_notes=0 md_skill=9-><9 이하> py_compile=0 cli_rc=0` (시작 판 `tag_worse=0 md_notes=absent md_skill=9->9 py_compile=0 cli_rc=0`). 양성 대조: 닫지 않은 `<div>` 를 넣은 모의 쪽 → `TAG_WORSE … 0->2` · `tag_worse=1`, 언어 없는 울타리 notes → `md_notes=1` (봉인 전 실측). 설치가 안 되면(망 끊김 등) 도우미가 `md=ENV_FAIL` 을 찍는다 — 그 칸만 `[미검증:ENV]` 로 적고 나머지 칸은 그대로 판정한다
- [ ] DG-03: N/A (commands.test `bash scripts/release.sh 2>&1 || true` 가 재는 `scripts/release.sh` 는 이번 바뀐 파일에 없다. 측정: DG-01 과 같은 `m DG-01` 이 `release_paths=0`) [exact]
- [ ] DG-04: 실제 앱/서버 구동 시 에러 0개
  이 계약에 적용: 구동할 앱은 문서 사이트다. 새 페이지 일곱을 따로 열 때와 목차에서 열 때 콘솔 오류 · 페이지 오류가 0 이다. 측정: `m DG-04` 가 ER-02 끝줄 `a11y_rc=0 ok_both=7/7`(각 `OK` 줄 `err=0`)과 ER-03 끝줄 `nav_ok=7/7 console_err=0`. 양성 대조: 외부 스타일 링크를 넣은 모의 쪽 → `err=1`(`net::ERR_NAME_NOT_RESOLVED`) (봉인 전 실측)
- [ ] DG-05: CI(자동 검사) 단계를 로컬에서 전부 돌려 통과한다 — Given 작업 폴더 W 가 끝점과 같다(`git -C W rev-parse HEAD` 가 `TIP` 이고 `git -C W status --porcelain --untracked-files=no` 가 빈 출력 — 아니면 도우미가 `W_NOT_TIP` 을 찍고 멈춘다), When `m DG-05` 가 `/Users/jackson/Hub/10_Dev/claude-plugins/.harness/handoff/2026-09-26-tools/ci-local.sh` 를 W 에 돌려 그 요약 파일을 읽으면, Then `tool_same=1 rc0=25 other=[feedback-agg-test SKIP (yq 없음);]` 이고 `outside=` 칸이 설치 단계 넷(`pip install pyyaml` · `zsh` 설치 · `npm ci` · `npx playwright install --with-deps chromium`)과 여러 줄 `run: |` 한 줄뿐이다 [exact]
  측정: `m DG-05`. 도구 파일은 이 가지 밖(본 체크아웃)에 있어 커밋으로 고정되지 않으므로 도우미가 그 내용 지문(`git hash-object`)을 봉인 때 값 `TOOL_BLOB` 과 대조한다. 시작 판(W 가 `6378948`) `rc0=25 other=[feedback-agg-test SKIP (yq 없음);]` · 같은 `outside`, 지문 `01528e5a5c0dfe27a6a9c0bb8ae1c830f2f04860`. `tool_same=0` 이거나 요약 파일이 없으면(`ci_summary=absent`) 그 회차는 `[미검증:ENV]` 로 적는다
  음성 대조: 이 계약이 기대는 `docs-a11y` 단계는 ER-02 양성 대조처럼 넘치는 쪽을 넣으면 `rc=1`, `docs-links` 단계는 AR-02 양성 대조처럼 깨진 상대 링크를 넣으면 `rc=1` 이 된다

## 범위 경계

항목별 처리 — 입력은 목록 「## docs」 절 DC-1, 「## user」 절 UD-4, 결정 파일 DC-1 · UD-4 행이다.

| 항목 | 처리 | 조건 · 사유 |
| --- | --- | --- |
| DC-1 대응 페이지 없는 원본 다섯(api 연구 기록 · reflect-digest · tone adapter-contract · adapter-dart-flutter · locale-korean) | 계약에 넣음 | AR-01 ~ AR-05 · AR-09 · ER-01 ~ ER-03 · SC-01. 여섯 가운데 다섯의 매핑은 이미 있어 도구 코드는 안 고친다 — 목차 등록과 페이지 파일이 생기면 SC-01 이 `OK` 가 된다 |
| UD-4 나머지 둘(`rust-kit/references/project-detection.md` · `phase-research-templates.md`) | 계약에 넣음 | 위 조건 모두 + SK-01 · SC-02 · SC-03. 결정 파일 17 번째 줄 「일곱 다」 |
| 드리프트 도구 짝 매핑 | 계약에 넣음 | 일곱째만 매핑이 없다(SC-01 시작 판 `unmapped`). 폴더째가 아니라 그 파일 하나만 잇는다 — 같은 폴더 `phase-dependencies.md` · `search-sources.md` 는 페이지가 없다(SC-02). 표 규칙(`SKILL.md:45-46`)에 따라 표 행도 같은 가지에서 고친다(SK-01 · SC-03) |
| 다른 묶음과 같은 줄 | 주의 · notes | 다른 묶음 vsa(VS-13)가 `SKILL.md:62` · `:64` 표 행과 `scripts/detect-docs-drift.py` 의 `:44-47` · `:95-100` 둘레를 고쳤다. 이 묶음이 `:64` 행을 고치면 합칠 때 그 한 줄이 부딪힌다 — 합친 행은 두 원본(`.claude/skills/kaizen-orchestrator/SKILL.md` · `phase-research-templates.md`)을 모두 담아야 한다. 스크립트 쪽은 vsa 가 안 건드린 줄(`:67-73` api · howto · onboarding 묶음 둘레)에 더하면 부딪히지 않는다. 다른 묶음 dca 는 같은 `SKILL.md` 의 `:2-16` · `:101-165` 를 고친다(표 밖). 부딪힘 해결은 부모가 합칠 때 한다 — notes 에 적는다(AR-08) |
| 원본이 바뀔 예정인 쪽 | 넘김 (부모) | reflect-digest(vsa VS-21 이 `:58` 한 줄을 이미 고침) · project-detection(KR-1 `:147-148` · KR-3 `:87`) · phase-research-templates(VS-16 `:261-262` · VS-17 `:78` · `:130` · VS-26 편집기 경고). 이 묶음은 시작 판 `6378948` 원본으로 만든다. 그 묶음들이 합쳐진 뒤 `python3 scripts/detect-docs-drift.py --since <합친 기준>` 이 이 쪽들을 다시 맞출 대상으로 낸다 — 이제 짝이 있어 `NEW` 가 아니라 다시 맞춤으로 나온다 |
| 320 폭 레포 검사 | 넘김 (dca, DC-2) | 레포 검사기(`scripts/check-docs-a11y.js`) · `design-kit/evals/visuals.spec.js` 에 320 을 넣는 일은 dca 몫이다. 이 묶음은 도우미로 320 · 375 · 1280 × 두 테마를 따로 잰다(ER-01) |
| 틀의 `--text3` 대비 · 단추 id | 넘김 (dca) | 틀(`page-template.html`) 고침은 dca(SK-04) 몫이라 이 묶음은 틀을 고치지 않는다(AR-06 허용 집합 밖). 새 페이지는 틀 사본의 값을 쓰되 대비가 모자라면 그 쪽 안에서 맞춘다 — ER-02 가 전 글자 요소 대비를 잰다 |
| `scripts/check-api-kit-docs.py` | 넘김 (VS-14) | `:83` 이 연구 기록을 건너뛰고, 시작 판 이미 `0/12 PASS` 다. 이 계약은 기대지 않는다 — notes 에 적는다 |
| `scripts/check-stale-values.py` 가 오케스트레이터 참고 문서 폴더를 재지 않음 | 넘김 (부모 · 새 남은 일 후보) | 목록 VS-27(onboarding-kit 이 옛 값 검사 목록에 없음)과 같은 모양이다. 검사 폴더 목록을 늘리면 AR-06 허용 파일 밖이라 이 묶음은 고치지 않는다 — notes 「남은 것」 에 적는다(AR-08) |
| 목록 DC-9 매핑 규칙 결정의 `process (공유)` 행 | 주의 · notes | 원본 칸을 오케스트레이터 `SKILL.md` 로 두는 몫은 VS-13(vsa)이 같은 줄에서 한다. 이 묶음은 같은 행에 `phase-research-templates.md` 를 더할 뿐이라 두 뜻이 맞선다고 보지 않는다 — 합친 행에 둘 다 남는지 부모가 합칠 때 본다(AR-08) |
| `docs/index.html` Rust 목차 점 색 `#F97316` 과 표 `#E85D4A` 의 어긋남 | 범위 밖 | 목차 색은 기존 줄이라 AR-02 `deleted=0` 이 막는다. 새 페이지 색은 표를 따른다(AR-01) |
| 기존 페이지 고침 · 원본 md · 킷 폴더 · 틀 · 공통 파일 | 범위 밖 | 과제의 범위 밖 지시. AR-06 이 바뀐 파일을 열로 묶는다 |
| 고치는 `SKILL.md` 의 기존 편집기 경고 9 | 넘김 (늘리지만 않음) | 사용자 결정 UD-7 「범위 밖 기존 경고를 전부 고친다」 는 VS-26 묶음 몫이다. 같은 파일을 세 묶음이 고치므로 이 묶음은 DG-02 로 늘지 않음만 잰다 |

커버리지 해소 — Step 6.5 (4) 검출기가 낸 `UNCOVERED` 와 목록을 한 곳에만 둔 조건:

- 커버리지 해소: 일곱 쪽 · 일곱 원본을 열거한 조건(SC-01 · ER-01 · ER-03 · AR-01 ~ AR-05) — 목록은 `## 배경` 표와 도우미 `SEVEN` 에 같은 글자로 있고 `m` 이 그 목록을 잰다. 측정 절에 일곱 경로를 되풀이해 적지 않는다
- 커버리지 해소: SC-01 — 검출기가 낸 `scripts/detect-docs-drift.py` 는 대상이 아니라 도우미가 불러 쓰는 도구다(`pg.py drift` 가 끝점 트리의 그 파일을 불러옴)
- 커버리지 해소: ER-03 · AR-02 — `docs/index.html` · `scripts/check-docs-links.py` 는 도우미가 끝점 트리에서 읽고 부르는 파일이다(`pg.py index` · `m AR-02` 의 `links_rc`). AR-02 의 `docs/index.html:248` 은 겹치면 안 되는 기존 id 자리를 가리키는 근거이고, 겹침은 `m AR-02` 의 `dup_ids` 가 잰다
- 커버리지 해소: AR-01 — `../assets/site.css` · `css-tokens.md` 는 대상이 아니라 판정 기준이다. 킷 색은 조건 산문과 `SEVEN` 넷째 칸에 같은 값으로 있다. `added=7/7` 은 기대 출력이다
- 커버리지 해소: AR-03 — 일곱 쪽 경로와 문턱은 `SEVEN` 다섯째 ~ 일곱째 칸에 같은 값으로 있고 `m AR-03` 이 그 목록을 잰다. `cov_ok=7/7` 은 기대 출력이다
- 커버리지 해소: AR-06 — 허용 열 파일은 산문과 도우미 `ALLOWED` · `SEVEN` 에서 오고 `m AR-06` 이 `comm` 으로 정확히 같은지 본다. `.harness/` · `sprint-contract*.md` 는 뺄 범위와 봉인 검사 대상의 이름 규칙이다

교차 진단 반영(봉인 전, 한 번 돈 교차 진단의 권고 넷을 모두 넣음): AR-08 이 세는 토큰을 아홉에서 열셋으로 늘렸다(`VS-17` · `KR-3` 이 산문에만 있고 셈에 없던 틈, `DC-9` 이름, `check-stale-values` 넘김). AR-02 에 Rust Kit 쪽 id 를 `project-detection-rust` 로 정했다. `## GAP 분석` 에 옛 값 검사 행을, 이 절 표에 그 넘김 행과 DC-9 행을 더했다. 모두 조건을 좁히는 쪽이다.

교차 진단(qa-evaluator) 때 주의:

- AR-03 의 문턱은 시작 판 156 쌍에서 잰 중앙값이다. 평가자는 `## GAP 분석` 끝 문단의 값을 도우미로 다시 재지 않아도 된다 — 문턱은 봉인과 함께 고정된다
- 계약 파일의 편집기 경고(첫 줄 제목 없음 · 코드 표시 안 공백 등)는 계약 형식에서 나온다. 계약 · QA 리포트 · 개정 파일은 DG-02 대상에서 뺀다

## 회귀 게이트 — 측정 도우미 · 봉인 전 실측

평가 때 이 블록을 떼어 bash 에서 불러 쓴다. `TMPDIR` 은 평가자 임시 폴더로 준다. 도우미는 `$T` 아래에만 쓴다 — 작업 폴더와 그 밖의 입력은 지우지 마라.
브라우저 도구는 작업 폴더 W 의 `node_modules`(추적 안 되는 폴더, `npm ci` 로 설치 — 봉인 전 실측 때 `ci-local.sh` 가 설치함)를 `NODE_PATH` 로 빌려 쓰고, 푼 트리마다 그 폴더를 가리키는 연결을 만든다.

준비 단계 실측(봉인 전, 이 기계): `command -v node` → fnm 경로 · 종료 코드 0 (`v24.14.1`), `python3` · `git` · `shasum` 종료 코드 0, W 의 `node_modules/playwright-core` 판 `1.58.2`. 브라우저가 없으면 `Executable doesn't exist` 로 멈춘다 — 복구: `cd W && node_modules/.bin/playwright-core install chromium-headless-shell` 뒤 다시 잰다. 브라우저가 없어 못 잰 조건은 FAIL 이 아니라 환경 실패로 보고한다.
`markdownlint-cli2@0.23.2` 임시 설치 종료 코드 0. `ci-local.sh` 지문 `git hash-object` → `01528e5a5c0dfe27a6a9c0bb8ae1c830f2f04860`.
Playwright 쓰임(`newContext` 의 `viewport` · `colorScheme` · `reducedMotion`, `addInitScript` 인자, `locator().count()` · `click`, `page.frames()` · `frame.url()` · `frame.evaluate`)은 Context7 `/microsoft/playwright/v1.58.2` 문서와 맞춰 봤다.
봉인 전 실측은 `BASE_REF=6378948 E_REF=BASE` 로 잰 시작 판 값과, 임시 복제본(`W=<복제본> NM=<W 의 node_modules>`)에 모의 나쁜 판 · 좋은 판을 커밋해 잰 값이다. 복제본은 세션 임시 폴더에 두었고 이 가지와 무관하다.
도우미는 zsh 에서 부르지 마라 — zsh 는 따옴표 없는 변수를 낱말로 나누지 않아 쪽 목록이 한 덩어리가 된다.

```bash
# 떼기: awk '/^# === 측정 도우미 시작/{f=1} f{print} /^# === 측정 도우미 끝/{exit}' <계약> > "$TMPDIR/dcb-measure.sh"
# 부르기: bash -c 'source "$TMPDIR/dcb-measure.sh" || exit 2; type m >/dev/null || exit 2; m SK-01'
# 봉인 커밋이 아직 없을 때: BASE_REF=<커밋> 을 준다. 시작 판을 재려면 E_REF=BASE. 임시 복제본을 재려면 W=<복제본> NM=<node_modules 경로>
# === 측정 도우미 시작 (after-0926-docs-new-pages) ===
# 쓰는 법: 이 블록을 파일로 떼어 bash 에서 source 한 뒤 `m <조건 ID>`. zsh 에서 부르지 마라(따옴표 없는 변수를 낱말로 나누지 않아 목록이 한 덩어리가 된다).
# 끝점 TIP = 가지 끝. 시작점 BASE = 이 계약을 처음 담은 커밋(봉인 커밋)의 부모 — 커밋 번호를 박지 않고 git 기록에서 푼다.
# 봉인 커밋이 아직 없으면 BASE_REF=<커밋> 을 준다. 시작 판 자체를 재려면 E_REF=BASE. 임시 복제본을 재려면 W=<복제본> NM=<node_modules 경로>.
W=${W:-/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak2-dcb}
BR=${BR:-chore/ak2-dcb}
SLUG=after-0926-docs-new-pages
CF_REL=.harness/sprint-contract-$SLUG.md
NOTES=.harness/.meta/after-kaizen-0926b/dcb-notes.md
TIP=$(git -C "$W" rev-parse --verify -q "$BR^{commit}") || { echo "UNRESOLVED TIP"; return 2 2>/dev/null || exit 2; }
if [ -n "${BASE_REF:-}" ]; then
  BASE=$(git -C "$W" rev-parse --verify -q "$BASE_REF^{commit}") || { echo "UNRESOLVED BASE_REF"; return 2 2>/dev/null || exit 2; }
else
  SEAL=$(git -C "$W" log --diff-filter=A --format=%H "$TIP" -- "$CF_REL" | tail -1)
  [ -n "$SEAL" ] || { echo "UNRESOLVED SEAL (봉인 커밋 없음)"; return 2 2>/dev/null || exit 2; }
  BASE=$(git -C "$W" rev-parse --verify -q "$SEAL^") || { echo "UNRESOLVED BASE"; return 2 2>/dev/null || exit 2; }
fi
T=$(mktemp -d "${TMPDIR:-/tmp}/dcb.XXXXXX")
NM=${NM:-$W/node_modules}
snap() { mkdir -p "$2" && git -C "$W" archive "$1" | tar -x -C "$2" && ln -s "$NM" "$2/node_modules"; }
EB=$T/base; snap "$BASE" "$EB"
case "${E_REF:-TIP}" in
  BASE) E=$EB; R=$BASE ;;
  *)    E=$T/tip; snap "$TIP" "$E"; R=$TIP ;;
esac
[ -d "$NM/playwright-core" ] || { echo "NO_PLAYWRIGHT (복구: cd W && npm ci)"; return 2 2>/dev/null || exit 2; }
export NODE_PATH=$NM
CI_LOCAL=/Users/jackson/Hub/10_Dev/claude-plugins/.harness/handoff/2026-09-26-tools/ci-local.sh
TOOL_BLOB=01528e5a5c0dfe27a6a9c0bb8ae1c830f2f04860
# 일곱 원본 | 새 쪽 | index.html 의 킷 목차 이름 첫머리 | --accent | 낱말 비율 문턱 | 코드 표시 문턱 | 코드 블록 줄 문턱(- 는 원본에 코드 블록 없음)
# 문턱 = 시작 판 등록 페이지 156 쌍에서 잰 값 가운데 큰 쪽: 같은 킷 중앙값 · 사이트 전체 중앙값(0.83 · 0.96 · 0.80). process 는 짝 있는 페이지가 없어 사이트 값
SEVEN='docs/api/research-log.md|docs/api-kit/research-log.html|API Kit|#A3E635|0.91|1.00|-
reflect-kit/skills/reflect-digest/SKILL.md|docs/reflect-kit/reflect-digest.html|Reflect Kit|#F43F5E|0.83|0.96|0.82
tone-kit/references/adapter-contract.md|docs/tone-kit/adapter-contract.html|Tone Kit|#D946EF|0.95|1.00|-
tone-kit/references/adapter-dart-flutter.md|docs/tone-kit/adapter-dart-flutter.html|Tone Kit|#D946EF|0.95|1.00|0.80
tone-kit/references/locale-korean.md|docs/tone-kit/locale-korean.html|Tone Kit|#D946EF|0.95|1.00|0.80
rust-kit/references/project-detection.md|docs/rust-kit/project-detection.html|Rust Kit|#E85D4A|0.83|0.96|0.82
.claude/skills/kaizen-orchestrator/references/phase-research-templates.md|docs/process/phase-research-templates.html|Process|#4ADE80|0.83|0.96|-'
printf '%s\n' "$SEVEN" > "$T/seven.txt"
PAGES7=$(printf '%s\n' "$SEVEN" | cut -d'|' -f2)
ALLOWED='.claude/skills/docs-site/SKILL.md
docs/index.html
scripts/detect-docs-drift.py'
CAP_RE='^(api-kit|reflect-kit|tone-kit|rust-kit|process)__[a-z0-9-]+-(320|375|1280)-(dark|light)\.png$'

cat > "$T/pg.py" <<'PY'
import sys, re, os, html as H, difflib, subprocess, importlib.util, pathlib
from html.parser import HTMLParser
rd = lambda p: open(p, encoding='utf-8').read()
ex = os.path.exists
def seven(p):
    return [dict(zip(('src', 'page', 'label', 'accent', 'wr', 'code', 'fence'), l.split('|'))) for l in rd(p).splitlines() if l.strip()]
def load_dd(tree):
    t = os.path.abspath(tree); spec = importlib.util.spec_from_file_location('dd' + str(abs(hash(t))), os.path.join(t, 'scripts/detect-docs-drift.py'))
    dd = importlib.util.module_from_spec(spec); spec.loader.exec_module(dd)
    dd.REPO_ROOT = pathlib.Path(t); dd.INDEX_HTML = dd.REPO_ROOT / 'docs/index.html'; dd.DOCS_SITE_SKILL = dd.REPO_ROOT / '.claude/skills/docs-site/SKILL.md'
    return dd
def cands(dd, s):
    o = dd.SOURCE_OVERRIDES.get(s)
    if o is not None: return list(o)
    c = dd.map_source_to_html(s); return [c] if c else []
def text1(h):
    h = re.sub(r'(?is)<(script|style)[^>]*>.*?</\1>', ' ', h)
    return re.sub(r'\s+', ' ', H.unescape(re.sub(r'<[^>]+>', ' ', h)))
def text2(h):
    h = re.sub(r'(?is)<(script|style)[^>]*>.*?</\1>', '', h)
    return re.sub(r'\s+', '', H.unescape(re.sub(r'<[^>]+>', '', h)))
def css_of(h):   # <style> 안과 style="" 속성, CSS 주석은 뺀다
    c = ' '.join(re.findall(r'(?is)<style[^>]*>(.*?)</style>', h)) + ' ' + ' '.join(re.findall(r'(?is)\sstyle="([^"]*)"', h))
    return re.sub(r'(?s)/\*.*?\*/', ' ', c)
URL = re.compile(r'https?://[^\s)<>\]"\'`|]+')
def urls(s): return {u.rstrip('.,;:') for u in URL.findall(s)}
cmd = sys.argv[1]
if cmd == 'drift':   # drift <트리> <seven> — 드리프트 도구가 일곱 원본을 바뀐 파일로 받았을 때 고르는 쪽
    dd = load_dd(sys.argv[2]); S = seven(sys.argv[3])
    dd.changed_files = lambda since: [x['src'] for x in S]
    got = {}
    for e in dd.detect_drift('x'): got.setdefault(e.source, []).append(e)
    ok = 0
    for x in S:
        es = got.get(x['src'], [])
        good = len(es) == 1 and es[0].target == x['page'] and es[0].registered and es[0].exists
        ok += good
        print(f"{'OK ' if good else 'BAD'} {x['src']} -> {[ (e.target, int(e.registered), int(e.exists)) for e in es] or 'unmapped'}")
    print(f'seven_ok={ok}/7')
elif cmd == 'mapdelta':   # mapdelta <옛 트리> <새 트리> — 두 트리의 모든 파일에 두 판 매핑을 돌려 달라진 원본만
    b, t = load_dd(sys.argv[2]), load_dd(sys.argv[3])
    files = set()
    for root in (sys.argv[2], sys.argv[3]):
        for d, ds, fs in os.walk(root):
            ds[:] = [x for x in ds if x not in ('node_modules', '.git')]
            files.update(os.path.relpath(os.path.join(d, f), root) for f in fs)
    delta = [(s, cands(b, s), cands(t, s)) for s in sorted(files) if cands(b, s) != cands(t, s)]
    for s, x, y in delta: print(f'DELTA {s}: {x} -> {y}')
    print(f'delta_n={len(delta)} excludes_same={int(b.SOURCE_EXCLUDES == t.SOURCE_EXCLUDES)}')
elif cmd == 'table':   # table <옛 트리> <새 트리> <seven> — docs-site SKILL.md Step 1 표가 일곱 원본을 덮는지 · 표와 스크립트 어긋남 수
    S = seven(sys.argv[4])
    def pairs(tree):
        txt = rd(os.path.join(tree, '.claude/skills/docs-site/SKILL.md'))
        st = re.search(r'(?ms)^## Step 1:.*?(?=^## )', txt); P = set()
        for row in (st.group(0) if st else '').splitlines():
            c = [x.strip() for x in row.strip().strip('|').split('|')]
            if not row.startswith('|') or len(c) != 3: continue
            outs = re.findall(r'`([^`]+)`', c[2])
            P.update((s, o) for s in re.findall(r'`([^`]+)`', c[1]) for o in outs)
        return P
    def spairs(tree):
        dd = load_dd(tree); P = set(dd.SOURCE_TO_HTML)
        for s, pages in dd.SOURCE_OVERRIDES.items(): P.update((s, p.rpartition('/')[0] + '/') for p in pages)
        return P
    cov = lambda pr, others: any(pr[1] == oo and (pr[0] == o or (o.endswith('/') and pr[0].startswith(o))) for o, oo in others)
    def mism(tree):
        sp, tp = spairs(tree), pairs(tree)
        return sum(1 for p in sp if not cov(p, tp)) + sum(1 for p in tp if not cov(p, sp))
    tp = pairs(sys.argv[3]); n = 0
    for x in S:
        g = cov((x['src'], x['page'].rpartition('/')[0] + '/'), tp); n += g
        if not g: print(f"NOT_IN_TABLE {x['src']}")
    print(f'seven_in_table={n}/7 mismatch={mism(sys.argv[2])}->{mism(sys.argv[3])} table_pairs={len(tp)}')
elif cmd == 'skilldiff':   # skilldiff <옛 트리> <새 트리> — SKILL.md 에서 바뀐 줄이 Step 1 표 행뿐인지
    f = '.claude/skills/docs-site/SKILL.md'; B, N = rd(os.path.join(sys.argv[2], f)).splitlines(), rd(os.path.join(sys.argv[3], f)).splitlines()
    ch = [x for x in difflib.unified_diff(B, N, lineterm='', n=0) if x[:1] in '+-' and not x.startswith(('+++', '---'))]
    minus = [x[1:] for x in ch if x[0] == '-']; plus = [x[1:] for x in ch if x[0] == '+']
    def step1(L):
        s = next((i for i, l in enumerate(L) if l.startswith('## Step 1:')), -1); e = next((i for i, l in enumerate(L) if i > s and l.startswith('## ')), len(L))
        return set(L[s:e]) if s >= 0 else set()
    nonrow = [l for l in minus + plus if not l.startswith('|')]
    out1 = [l for l in minus if l not in step1(B)] + [l for l in plus if l not in step1(N)]
    print(f'minus={len(minus)} plus={len(plus)} nonrow={len(nonrow)} outside_step1={len(out1)}')
elif cmd == 'pages':   # pages <새 트리> <seven> — 새 쪽 일곱의 틀 · 공통 파일 · 색 · 숨김
    S = seven(sys.argv[3]); t = sys.argv[2]; agg = dict(exist=0, lines=0, css1=0, ext0=0, accent=0, theme=0, light=0, rm0=0, hide0=0)
    for x in S:
        p = os.path.join(t, x['page'])
        if not ex(p): print(f"ABSENT {x['page']}"); continue
        h = rd(p); agg['exist'] += 1
        n = h.count('\n') + (0 if h.endswith('\n') else 1)
        links = re.findall(r'(?is)<link\b[^>]*>', h); site = [l for l in links if re.search(r'href="\.\./assets/site\.css"', l)]
        first_style = h.lower().find('<style'); site_pos = h.find(site[0]) if site else -1
        css1 = len(site) == 1 and 0 <= site_pos < first_style
        ext = [l for l in links if l not in site] + re.findall(r'(?is)<script\b[^>]*\ssrc=', h) + re.findall(r'@import\s', css_of(h)) + re.findall(r'url\(\s*[\'"]?https?://', h)
        root = re.search(r'(?s):root\s*\{(.*?)\}', h); acc = re.search(r'--accent\s*:\s*(#[0-9A-Fa-f]{6})', root.group(1)) if root else None
        accent = bool(acc) and acc.group(1).upper() == x['accent'].upper()
        c = css_of(h)
        hide = re.findall(r'overflow(?:-x|-y)?\s*:\s*(?:hidden|clip)|text-overflow\s*:\s*ellipsis', c)
        rm = h.count('prefers-reduced-motion')
        theme = 'dk-theme' in h; light = '[data-theme="light"]' in c
        for k, v in (('lines', n >= 400), ('css1', css1), ('ext0', not ext), ('accent', accent), ('theme', theme), ('light', light), ('rm0', rm == 0), ('hide0', not hide)): agg[k] += bool(v)
        print(f"{x['page']} lines={n} site_css={len(site)} before_style={int(css1)} ext={len(ext)} accent={acc.group(1) if acc else None} dk_theme={int(theme)} light_rule={int(light)} rm={rm} hide={len(hide)}")
    print(' '.join(f'{k}={v}/7' for k, v in agg.items()))
elif cmd == 'cov':   # cov <새 트리> <seven> — 원본 담김: 낱말 비율 · 코드 표시 · 코드 블록 줄
    S = seven(sys.argv[3]); t = sys.argv[2]; ok = 0
    for x in S:
        s = rd(os.path.join(t, x['src'])); p = os.path.join(t, x['page'])
        if not ex(p): print(f"ABSENT {x['page']}"); continue
        h = rd(p); a, b = text1(h), text2(h)
        codes = sorted({c.strip() for c in re.findall(r'`([^`\n]+)`', s) if c.strip()})
        cin = [c for c in codes if re.sub(r'\s+', ' ', c) in a]; cr = len(cin) / len(codes) if codes else 1.0
        words = {w for w in re.findall(r'[0-9A-Za-z가-힣_.-]{2,}', re.sub(r'`[^`]*`', ' ', s))}
        wr = sum(1 for w in words if w in a) / max(1, len(words))
        L = set(); fence = False
        for l in s.splitlines():
            if re.match(r'^\s*(```|~~~)', l): fence = not fence; continue
            if fence:
                z = re.sub(r'\s+', '', l)
                if len(z) >= 8: L.add(z)
        fin = [z for z in L if z in b]; fr = len(fin) / len(L) if L else None
        good = round(wr, 2) >= float(x['wr']) and round(cr, 2) >= float(x['code']) and (x['fence'] == '-' or (fr is not None and round(fr, 2) >= float(x['fence'])))
        ok += good
        miss = [c for c in codes if c not in cin][:4]
        print(f"{'OK ' if good else 'BAD'} {x['page']} wr={wr:.2f}(>={x['wr']}) code={len(cin)}/{len(codes)}={cr:.2f}(>={x['code']}) fence={'-' if fr is None else f'{len(fin)}/{len(L)}={fr:.2f}'}(>={x['fence']}) {miss}")
    print(f'cov_ok={ok}/7')
elif cmd == 'urls':   # urls <새 트리> <seven> — 원본의 http(s) 주소가 쪽의 href 로 모두 옮겨졌는지
    S = seven(sys.argv[3]); t = sys.argv[2]; ok = 0; tot = 0
    for x in S:
        p = os.path.join(t, x['page'])
        if not ex(p): print(f"ABSENT {x['page']}"); continue
        want = urls(rd(os.path.join(t, x['src']))); have = {H.unescape(u) for u in re.findall(r'href="(https?://[^"]+)"', rd(p))}
        miss = sorted(want - have); ok += not miss; tot += len(want)
        print(f"{'OK ' if not miss else 'BAD'} {x['page']} src_urls={len(want)} missing={len(miss)} {miss[:3]}")
    print(f'url_ok={ok}/7 src_urls_total={tot}')
elif cmd == 'index':   # index <옛 트리> <새 트리> <seven> — 킷 목차 등록 · id 겹침 · 아이콘 · 바뀐 줄
    S = seven(sys.argv[4]); B = rd(os.path.join(sys.argv[2], 'docs/index.html')); N = rd(os.path.join(sys.argv[3], 'docs/index.html'))
    def entries(txt):
        cat = txt[txt.find('const categories'):txt.find('// Flatten for lookup')]; out = []; label = None
        for l in cat.splitlines():
            m = re.search(r"label:\s*'([^']+)'", l)
            if m: label = m.group(1)
            m = re.search(r"\{\s*id:\s*'([^']+)'.*?file:\s*'([^']+)'", l)
            if m: out.append((m.group(1), m.group(2), label))
        return out
    def icons(txt):
        s = txt.find('function getIcon'); blk = txt[s:txt.find('\n  }', s)]
        return set(re.findall(r"^\s*'([^']+)'\s*:", blk, re.M))
    en, ic = entries(N), icons(N); ids = [e[0] for e in en]
    dup = lambda E: sum(1 for i in {e[0] for e in E} if [e[0] for e in E].count(i) > 1)
    reg = icon = 0
    for x in S:
        f = x['page'][len('docs/'):]; m = [e for e in en if e[1] == f]
        good = len(m) == 1 and (m[0][2] or '').startswith(x['label']); reg += good; icon += bool(m) and m[0][0] in ic
        print(f"{'OK ' if good else 'BAD'} {f} entries={len(m)} id={m[0][0] if m else None} label={m[0][2] if m else None} icon={int(bool(m) and m[0][0] in ic)}")
    ch = [z for z in difflib.unified_diff(B.splitlines(), N.splitlines(), lineterm='', n=0) if z[:1] in '+-' and not z.startswith(('+++', '---'))]
    print(f"reg_ok={reg}/7 icon_ok={icon}/7 dup_ids={dup(entries(B))}->{dup(en)} added={sum(z[0] == '+' for z in ch)} deleted={sum(z[0] == '-' for z in ch)}")
elif cmd == 'tags':   # tags <파일> — 짝 안 맞는 HTML 태그 수 (빈 요소 제외)
    VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'source', 'track', 'wbr', 'path', 'circle', 'rect', 'line', 'polyline', 'polygon', 'ellipse', 'stop'}
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
    p = P(); p.feed(rd(sys.argv[2])); print(p.bad + len(p.st))
elif cmd == 'bare':   # bare <md> — 언어 표시 없이 여는 코드 울타리 수 (V6 과 같은 상태 기계: 여는 줄만 센다)
    f = sys.argv[2]
    if not ex(f): print('absent'); sys.exit()
    n = 0; open_ = None
    for l in rd(f).splitlines():
        m = re.match(r'^\s*(`{3,}|~{3,})(.*)$', l)
        if not m: continue
        if open_ is None: open_ = m.group(1)[0] * len(m.group(1)); n += (m.group(2).strip() == '')
        elif m.group(1).startswith(open_) and m.group(2).strip() == '': open_ = None
    print(n)
elif cmd == 'commits':   # commits <W> <BASE> <R> <킷 목록> — 킷 둘 · docs 킷 폴더 둘 · .harness 섞임
    w, b, r, kits = sys.argv[2], sys.argv[3], sys.argv[4], set(rd(sys.argv[5]).split())
    revs = subprocess.run(['git', '-C', w, 'rev-list', '--no-merges', f'{b}..{r}'], capture_output=True, text=True).stdout.split()
    impl = mk = md = mx = 0
    for c in revs:
        fs = [l for l in subprocess.run(['git', '-C', w, 'show', '--name-only', '--format=', c], capture_output=True, text=True).stdout.splitlines() if l]
        h = [f for f in fs if f.startswith('.harness/')]; o = [f for f in fs if not f.startswith('.harness/')]
        if o: impl += 1
        mk += len({f.split('/')[0] for f in o if f.split('/')[0] in kits}) > 1
        md += len({f.split('/')[1] for f in o if f.startswith('docs/') and f.count('/') >= 2}) > 1
        mx += bool(h) and bool(o)
    print(f'commits={len(revs)} impl_commits={impl} multi_kit={mk} multi_docs_folder={md} mixed={mx}')
elif cmd == 'tokens':   # tokens <notes> <토큰...> — 토큰마다 한글 15 자 이상인 줄에 든 횟수
    f = sys.argv[2]
    if not ex(f): print('notes=absent'); sys.exit()
    L = [l for l in rd(f).splitlines() if len(re.findall(r'[가-힣]', l)) >= 15]
    print(' '.join(f'{k}={sum(1 for l in L if k in l)}' for k in sys.argv[3:]))
PY

cat > "$T/pw.js" <<'JS'
const { chromium } = require('playwright-core'); const path = require('path'); const fs = require('fs');
const [mode, tree, ...rest] = process.argv.slice(2);
(async () => {
  const b = await chromium.launch();
  if (mode === 'of') {   // of <트리> <쪽...> — 320 · 375 · 1280 폭 × 밝은 · 어두운 테마의 문서 가로 넘침(px)
    let ok = 0, cells = 0, zero = 0;
    for (const f of rest) {
      const file = path.join(tree, f); if (!fs.existsSync(file)) { console.log(`ABSENT ${f}`); continue; }
      let pageOk = true; const bg = {}; const row = [];
      for (const theme of ['dark', 'light']) {
        const ctx = await b.newContext({ viewport: { width: 1280, height: 900 }, colorScheme: theme, reducedMotion: 'reduce' });
        await ctx.addInitScript(t => { try { localStorage.setItem('dk-theme', t); } catch (e) {} }, theme);
        const p = await ctx.newPage(); await p.goto('file://' + path.resolve(file));
        await p.evaluate(t => { document.documentElement.dataset.theme = t; }, theme); await p.waitForTimeout(400);
        bg[theme] = await p.evaluate(() => getComputedStyle(document.body).backgroundColor + '|' + document.documentElement.dataset.theme);
        for (const w of [320, 375, 1280]) {
          await p.setViewportSize({ width: w, height: 900 }); await p.waitForTimeout(150);
          const of = await p.evaluate(() => Math.max(document.documentElement.scrollWidth - document.documentElement.clientWidth, document.body.scrollWidth - document.body.clientWidth));
          cells++; if (of <= 0) zero++; else pageOk = false; row.push(`${theme[0]}${w}=${of}`);
        }
        await ctx.close();
      }
      const differ = bg.dark.split('|')[0] !== bg.light.split('|')[0];
      if (!differ) pageOk = false; if (pageOk) ok++;
      console.log(`${pageOk ? 'OK ' : 'BAD'} ${f} ${row.join(' ')} theme_differs=${differ ? 1 : 0}`);
    }
    console.log(`of_ok=${ok}/${rest.length} cells_zero=${zero}/${cells}`);
  } else if (mode === 'nav') {   // nav <트리> <id=file...> — index.html 목차를 눌러 새 쪽이 뜨는지
    const ctx = await b.newContext({ viewport: { width: 1280, height: 900 } }); const p = await ctx.newPage(); const errs = [];
    p.on('console', m => m.type() === 'error' && errs.push(m.text())); p.on('pageerror', e => errs.push(String(e)));
    await p.goto('file://' + path.resolve(path.join(tree, 'docs/index.html'))); await p.waitForTimeout(500);
    let ok = 0;
    for (const pair of rest) {
      const [id, file] = pair.split('=');
      const item = p.locator(`.nav-item[data-id="${id}"]`);
      if (await item.count() !== 1) { console.log(`BAD ${file} nav_items=${await item.count()}`); continue; }
      await item.click(); await p.waitForTimeout(900);
      const fr = p.frames().find(x => x.url().endsWith('/' + file));
      const len = fr ? await fr.evaluate(() => document.body.innerText.length) : 0;
      const title = fr ? await fr.evaluate(() => document.title) : '';
      const good = !!fr && len > 1000 && title.trim().length > 0; if (good) ok++;
      console.log(`${good ? 'OK ' : 'BAD'} ${file} id=${id} frame=${fr ? 1 : 0} text=${len} title=${JSON.stringify(title)}`);
    }
    console.log(`nav_ok=${ok}/${rest.length} console_err=${errs.length}`); errs.slice(0, 3).forEach(e => console.log('ERR ' + e));
  }
  await b.close();
})();
JS

m() {
  case "$1" in
    SK-01) python3 "$T/pg.py" skilldiff "$EB" "$E"; python3 "$T/pg.py" table "$EB" "$E" "$T/seven.txt" ;;
    SC-01) python3 "$T/pg.py" drift "$E" "$T/seven.txt" ;;
    SC-02) python3 "$T/pg.py" mapdelta "$EB" "$E" ;;
    SC-03) python3 "$T/pg.py" table "$EB" "$E" "$T/seven.txt" ;;
    ER-01) (cd "$T" && node pw.js of "$E" $PAGES7) ;;
    ER-02) EX7=$(for p in $PAGES7; do [ -f "$E/$p" ] && echo "$p"; done); echo "absent=$((7 - $(printf '%s\n' $EX7 | grep -c .)))"
           [ -n "$EX7" ] || { echo "a11y_rc=none ok_both=0/7"; return 0; }
           (cd "$E" && node scripts/check-docs-a11y.js $EX7 > "$T/a11y.txt" 2>&1; rc=$?; cat "$T/a11y.txt"
            echo "a11y_rc=$rc ok_both=$(grep -cE '^OK .* theme=both$' "$T/a11y.txt")/7") ;;
    ER-03) PAIRS=$(for p in $PAGES7; do f=${p#docs/}; id=$(grep -F "file: '$f'" "$E/docs/index.html" | sed -nE "s/.*id:[[:space:]]*'([^']+)'.*/\1/p" | head -1); echo "${id:-none}=$f"; done)
           (cd "$T" && node pw.js nav "$E" $PAIRS) ;;
    AR-01) echo "added=$(git -C "$W" diff --name-status "$BASE" "$R" -- $PAGES7 | awk '$1 == "A"' | wc -l | tr -d ' ')/7"; python3 "$T/pg.py" pages "$E" "$T/seven.txt" ;;
    AR-02) python3 "$T/pg.py" index "$EB" "$E" "$T/seven.txt"
           (cd "$E" && python3 scripts/check-docs-links.py > "$T/links.txt" 2>&1; echo "links_rc=$? $(tail -1 "$T/links.txt")") ;;
    AR-03) python3 "$T/pg.py" cov "$E" "$T/seven.txt" ;;
    AR-04) python3 "$T/pg.py" urls "$E" "$T/seven.txt" ;;
    AR-05) python3 "$T/pg.py" pages "$E" "$T/seven.txt" | tail -1 ;;
    AR-06) CH=$(git -C "$W" diff --name-status "$BASE" "$R" -- . ':(exclude).harness')
           WANT=$(printf '%s\n%s\n' "$ALLOWED" "$PAGES7" | LC_ALL=C sort); GOT=$(printf '%s\n' "$CH" | awk 'NF{print $NF}' | LC_ALL=C sort)
           echo "extra=$(comm -13 <(echo "$WANT") <(echo "$GOT") | grep -c .) missing=$(comm -23 <(echo "$WANT") <(echo "$GOT") | grep -c .) png=$(git -C "$W" diff --name-only "$BASE" "$R" | grep -ci '\.png$') status=$(printf '%s\n' "$CH" | awk 'NF{print $1}' | LC_ALL=C sort | uniq -c | awk '{printf "%s%s ", $2, $1}')"
           comm -3 <(echo "$WANT") <(echo "$GOT") | head -5
           sb=0; for c in $(cd "$E" && find .harness -maxdepth 1 -name 'sprint-contract*.md' | LC_ALL=C sort); do
             rec=$(awk '/^---$/{f++; next} f==1 && /^conditions_digest:/{sub(/^conditions_digest:[ ]*sha256:/,""); print; exit}' "$E/$c")
             [ -n "$rec" ] || continue
             act=$(grep -E '^- \[[ x]\] [A-Z]{2,}-[0-9]{2}' "$E/$c" | sed -E 's/^- \[[ x]\]/- [ ]/' | shasum -a 256 | cut -c1-16)
             [ "$rec" = "$act" ] || { sb=$((sb+1)); echo "SEAL_BROKEN $c"; }
           done; echo "seal_broken=$sb" ;;
    AR-07) (cd "$EB" && find . -mindepth 3 -maxdepth 3 -path './*/.claude-plugin/plugin.json' | cut -d/ -f2 | LC_ALL=C sort) > "$T/kits.txt"
           python3 "$T/pg.py" commits "$W" "$BASE" "$R" "$T/kits.txt" ;;
    AR-08) echo "committed=$(git -C "$W" cat-file -e "$R:$NOTES" 2>/dev/null && echo 1 || echo 0)"
           python3 "$T/pg.py" tokens "$E/$NOTES" 'DC-1' 'UD-4' 'tone-guide' 'VS-13' 'VS-16' 'VS-17' 'VS-21' 'KR-1' 'KR-3' 'check-api-kit-docs' 'DC-2' 'DC-9' 'check-stale-values' ;;
    AR-09) CAP=$(sed -n 's/^캡처 폴더: `\(.*\)`$/\1/p' "$E/$NOTES" 2>/dev/null | head -1); echo "cap_dir=${CAP:-absent}"
           [ -n "$CAP" ] && [ -d "$CAP" ] || { echo "cap_ok=0"; return 0; }
           need=0; have=0; for p in $PAGES7; do
             base=$(echo "$p" | sed -E 's#^docs/##; s#\.html$##; s#/#__#')
             for w in 320 375 1280; do for t in dark light; do need=$((need+1)); [ -s "$CAP/$base-$w-$t.png" ] && have=$((have+1)); done; done
           done
           echo "cap_need=$need cap_have=$have cap_badname=$(find "$CAP" -maxdepth 1 -name '*.png' -exec basename {} \; | grep -cvE "$CAP_RE")" ;;
    RE-02) python3 "$T/pg.py" pages "$E" "$T/seven.txt" | tail -1
           echo "new_scripts=$(git -C "$W" diff --name-status "$BASE" "$R" -- . ':(exclude).harness' | awk '$1 == "A" && $2 ~ /\.(js|py|sh|css)$/' | wc -l | tr -d ' ')" ;;
    AP-03) for f in "$NOTES" .claude/skills/docs-site/SKILL.md; do printf '%s=%s->%s ' "$(basename "$f")" "$(python3 "$T/pg.py" bare "$EB/$f")" "$(python3 "$T/pg.py" bare "$E/$f")"; done; echo ;;
    AP-04) echo "fm_name=$(awk 'NR==1 && /^---$/{f=1; next} f && /^---$/{exit} f && /^name:/{print $2}' "$E/.claude/skills/docs-site/SKILL.md")" ;;
    DG-01|DG-03) echo "release_paths=$(git -C "$W" diff --name-only "$BASE" "$R" -- scripts/release.sh | wc -l | tr -d ' ')" ;;
    DG-02) tw=0; for p in $PAGES7 docs/index.html; do [ -f "$E/$p" ] || { echo "ABSENT $p"; continue; }
             a=$(python3 "$T/pg.py" tags "$E/$p"); bb=0; [ -f "$EB/$p" ] && bb=$(python3 "$T/pg.py" tags "$EB/$p"); [ "$a" -gt "$bb" ] && { tw=$((tw+1)); echo "TAG_WORSE $p $bb->$a"; }; done
           (cd "$T" && npm i --silent --no-save markdownlint-cli2@0.23.2 >/dev/null 2>&1) || echo "md=ENV_FAIL"
           printf '{"config":{"MD013":false}}\n' > "$T/.markdownlint-cli2.jsonc"
           mdc() { [ -f "$1" ] || { echo absent; return; }; (cd "$T" && node_modules/.bin/markdownlint-cli2 "$1" 2>&1 | grep -cE ':[0-9]+(:[0-9]+)? (error|warning)? ?MD[0-9]+' ); }
           echo "tag_worse=$tw md_notes=$(mdc "$E/$NOTES") md_skill=$(mdc "$EB/.claude/skills/docs-site/SKILL.md")->$(mdc "$E/.claude/skills/docs-site/SKILL.md") py_compile=$(python3 -m py_compile "$E/scripts/detect-docs-drift.py" 2>&1 | wc -l | tr -d ' ') cli_rc=$(cd "$W" && python3 scripts/detect-docs-drift.py --since "$BASE" >/dev/null 2>&1; echo $?)" ;;
    DG-04) m ER-02 | tail -1; m ER-03 | tail -2 ;;
    DG-05) [ "$(git -C "$W" rev-parse HEAD)" = "$TIP" ] && [ -z "$(git -C "$W" status --porcelain --untracked-files=no)" ] || { echo "W_NOT_TIP"; return 0; }
           echo "tool_same=$([ "$(git hash-object "$CI_LOCAL" 2>/dev/null)" = "$TOOL_BLOB" ] && echo 1 || echo 0)"
           (cd "$W" && TMPDIR="$T" bash "$CI_LOCAL" "$W" > "$T/ci.txt" 2>&1); SUM=$T/ci-local/summary.txt
           [ -s "$SUM" ] || { echo "ci_summary=absent"; return 0; }
           echo "rc0=$(grep -c 'rc=0' "$SUM") other=[$(grep -v 'rc=0' "$SUM" | sed -E 's/[[:space:]]+/ /g' | tr '\n' ';')] outside=[$(sed -n '/이 스크립트 밖의 것:/,/^[0-9]*$/p' "$T/ci.txt" | sed '1d;$d' | tr '\n' ';')]" ;;
    *) echo "UNKNOWN $1" ;;
  esac
}
# === 측정 도우미 끝 ===
```
