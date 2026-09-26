---
feature: "원본이 바뀐 문서 페이지 다시 맞추기 (d1) — 열 쪽 원본 반영 · design-concept 공백"
slug: after-0924-docs-regen
created: "2026-09-26 15:38"
complexity: "복잡"
conditions: 28
status: active
owner_session: bda55d45-296c-491f-89ba-b52042d58e72
conditions_digest: sha256:5f2a4aa254cb4e0c
locked_at: "2026-09-26 15:58"
---

## 배경

2026-09-24 카이젠 뒤 후속 묶음(C1 ~ C4)이 원본 문서를 고쳤는데 그 원본을 보여 주는 문서 페이지는 옛 글에 멈춰 있다.
이 계약은 원본이 바뀐 자리(`git diff f81568d..39ddc12 -- <원본>`)와 과제가 이름을 댄, 페이지가 원래 뒤처진 자리를 페이지 열 쪽에 옮기고,
덤으로 `docs/design-kit/design-concept.html:277` 나쁜 예 코드 앞 공백 세 칸을 뺀다. 근거 원문은 핸드오프
`/Users/jackson/Hub/10_Dev/claude-plugins/.harness/handoff/2026-09-26-0110.md` §C3 「문서 사이트」 줄(본 체크아웃, 읽기만),
이 가지의 `.harness/.meta/after-kaizen-0926/c3b-notes.md` 「다음 사이클 메모」 1 · 2 번, `.harness/.meta/after-kaizen-0926/c4d-notes.md` R4 다.

- 사용자 합의(Step 5): 사용자 위임으로 받은 것으로 적는다 — user 2026-09-26T01:04:21.505Z 「다음 세션에서 직접할 일을 다 실행하고 이어질것도 실행해」
  (세션 기록 `/Users/jackson/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/de8c7935-a5b6-4df5-9106-fafa73c288a0.jsonl`),
  그 앞의 「나한테 물어보지 말고 자동으로 끝까지」(2026-09-24T04:04:16.964Z). 판단이 갈린 곳은 저장소 안 근거로 정했고 `## 범위 경계` 에 적었다.
- 작업 폴더 W = `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak-docs`, 가지 `chore/ak-docs`. 이 가지는 통합 가지 `chore/after-kaizen-0926` 의 `39ddc12` 에서 갈라졌다 — 범위 구간은 `39ddc12..chore/ak-docs` 로 재고(origin/main 기준 아님), 페이지의 옛 판은 `39ddc12` 판이다.
- 커밋 규칙: `git add <경로>` 뒤 `git commit -o <경로>` · 페이지마다 한 커밋 · `.harness/` 파일은 페이지와 다른 커밋 · `git add -A` · `git stash` · push · 가지 바꾸기 금지. 본 체크아웃과 다른 워크트리는 건드리지 않는다.
- 구현 전에 `tone-kit:tone-guide` 1 단계(규칙 불러오기)를, 완료 선언 전에 5 단계(전수 대조)를 한다 — 페이지 글도 한국어 기술 문체 규칙 대상이다. 대조 결과는 notes 에 남긴다(AR-02).
- 절차는 `.claude/skills/docs-site/SKILL.md` 를 따르고(원본 → 페이지 매핑은 그 파일 Step 1 표), 페이지를 처음부터 새로 쓰지 않는다. 페이지 머리의 판 번호 · 날짜는 원본 머리 설정(`version` · `last_updated`)에서 뽑는다 — 머리 설정이 없는 원본의 페이지에는 판 번호를 지어 넣지 않는다.
- 사용자가 할 일: 없음.

공통 전제 G (조건마다 되풀이하지 않는다) — 구현 · notes 커밋이 가지 `chore/ak-docs` 에 모두 들어간 뒤, 가지를 합치기 전에 잰다.
측정은 `## 회귀 게이트` 의 측정 도우미 `m <조건 ID>` 로 한다. 도우미는 끝점 `TIP`(가지 끝)과 시작점 `BASE`(= `39ddc12`)를 `git archive` 로 풀어 잰다 — 작업 폴더의 커밋 안 된 변경은 보지 않는다.
원본은 늘 `39ddc12` 판을 읽고, 원본의 바뀐 줄은 `git diff -U0 f81568d 39ddc12 -- <원본>` 에서 뽑는다 — 이 가지에서 원본이 바뀌어도 기대값이 흔들리지 않는다(원본을 고치는 것 자체는 AR-01 이 막는다).
`HEAD` 를 상한으로 쓰지 않는다. `BASE` · `TIP` · `f81568d` 해석이 안 되면 도우미가 `UNRESOLVED` 를 찍고 멈춘다.

바뀐 줄 대조(도우미 `chg`)의 판정 — 원본에 더해진 줄을 단위로 나눈다.
원본 코드 블록 안 줄(공백을 뺀 8 자 이상)은 공백을 뺀 페이지 보이는 글에 그대로 들어야 든 것이다.
코드 블록 밖 줄은 목록 항목 · 표 행 · 문단 단위로 묶고, 꾸밈 기호(`**` · 백틱 · 링크 문법 · 앞머리 목록 기호)와 공백을 뺀 글을 8 자 조각으로 나눈다.
지워진 줄에도 있던 조각은 빼고(새로 들어온 글만 본다) 남은 조각의 60 % 이상이 페이지 보이는 글(공백 뺌)에 있으면 든 것이다.
새 조각이 없는 단위(순서만 옮긴 줄)는 세지 않는다. 뜻: 원본 글을 조금 다듬어 옮기는 것은 통과하고, 새 내용을 빼거나 전혀 다른 글로 바꾸면 걸린다.
페이지가 원래 싣지 않는 자리는 원본 줄 번호로 뺀다(도우미 `PAIRS` 셋째 칸) — bambu-print-profile 의 검사 코드 `1600-1612` 와 kaizen-flow 의 「197 줄만」 두 곳뿐이며 사유는 `## 범위 경계` 에 있다.

옛 글 검사(도우미 `cnt` · `rcnt`) — 원본이 바꾼 주장을 페이지가 새 글과 나란히 계속 적어 서로 어긋나는 자리만 고른다. 공백을 뺀 페이지 보이는 글에서 센다.

복잡도 4 축 — 둘이 「예」 라 최소 「중간」 이다. 페이지 열한 쪽 · 원본 열 개 · 조건마다 다른 측정이 겹쳐 기능 조건이 19 개라 「복잡」 으로 둔다.
기능 조건 19 개는 SK-01 ~ SK-13 · ER-01 · ER-02 · AR-01 ~ AR-03 · DG-05 다 — Step 6.2 두 번째 명령이 `## Anti-patterns` 절(AP-01 · AP-03) · 자동 포함 여섯 줄(RE-01 · RE-02 · DG-01 ~ DG-04) · `N/A (` 줄(SC-00)을 빼고 센 값이다.
Step 2.5 짝 조건: 만드는 쪽은 페이지 열한 쪽을 같은 경로에서 고치는 것(AR-01 `pages=11/11` · RE-02 `added_files=0`), 쓰는 쪽은 첫 화면 `docs/index.html` 의 등록 · 내부 링크다(AR-03).

| 축 | 물음 | 값 |
| -- | ---- | -- |
| 레이어 수 | 몇 개 계층을 관통하는가 | 하나 — 정적 문서 화면(HTML · CSS · 페이지 안 스크립트) |
| 공개 API·계약 변경 | 외부에 노출된 약속이 바뀌는가 | 아니오 — 페이지 경로 · 첫 화면 등록 id 를 그대로 둔다 |
| 소비면 존재 | 반대편이 있는가 | 예 — `docs/index.html` 내비 등록 176 과 내부 링크가 이 페이지들을 가리킨다 |
| 회귀 위험 | 기존 동작이 깨질 수 있는가 | 예 — 옮기다 원본 글을 잃거나, 좁은 폭에서 넘치거나, 페이지 스크립트가 멈출 수 있다 |

설정 값 대조 (`.harness/project.yaml` 을 글자 그대로 옮김):

| config key | project.yaml 에서 읽은 값 | 계약에 쓴 값 |
| ---------- | ------------------------- | ------------ |
| `commands.analyze` | `bash -n scripts/release.sh` | DG-01 N/A — 재는 파일이 바뀐 파일에 없다 |
| `commands.test` | `bash scripts/release.sh 2>&1 \|\| true` | DG-03 N/A — 같은 이유 |
| `diagnostics.ide_exclude` | `[]` | DG-02 의 `([] 제외)` |
| `contract_categories[].id` / `prefix` | Skill/SK · Script/SC · Error/ER · Architecture/AR | 같은 넷 |
| `anti_patterns[].id` / `message` | AP-01 버전 하드코딩 · AP-02 force push · AP-03 bare code fence · AP-04 frontmatter name 누락 | AP-01 · AP-03 (고치는 페이지 글과 새 notes 에 걸릴 수 있다). AP-02 는 이 계약이 push 하지 않아서, AP-04 는 SKILL.md · 에이전트 파일을 안 건드려서 뺐다 |

## GAP 분석 (Pre-Edit Audit)

대상 파일을 실제로 읽고 잰 값이다(시작 판 `39ddc12`). 측정은 도우미와 같은 식이다.

| 대상 파일 | 실제 Read 증거 (`파일:라인`) | 발견한 기존 갭·위반 | 계약 조건화 |
| --------- | ---------------------------- | ------------------- | ----------- |
| `docs/bambu-kit/bambu-print-profile.html` · 원본 `bambu-kit/skills/bambu-print-profile/SKILL.md` | 페이지 `:1636-1657` [미검증] 표, `:1648` 「enum 줄만 빠진 목록 — 같음」, `:1905-1921` G-code 길이 카드 · 원본 `:1600-1612` 검사 코드, `:2041` 안 돈 검사만 적는 줄, `:2245` `G91` 줄 | 표 `:1648` 이 「같음(키 존재 · 종류 · enum 값 미실행)」 이라 원본 `:2041`(enum 값 검사만 빠지고 종류 검사는 돈다)과 어긋난다. `G91` 적용 범위 줄 없음. 검사 코드는 페이지가 원래 싣지 않는다 | SK-01 |
| `docs/design-kit/visual-change-protocol.html` · 원본 `design-kit/references/visual-change-protocol.md` | 페이지 `:845-847` ID 와 excluded_surfaces 카드, `:879-880` 종료 코드 설명 줄, `:885-890` 파일 읽기 분기, `:905-909` 결정별 검사, `:940-949` 종료 코드 표 · 원본 `:389-393` · `:411` · `:419-421` · `:443-447` | 검사 코드를 글자 그대로 싣는 페이지인데 새 줄 9 개 없음(`status` · 입력 오류 · `excluded_surfaces` 키 검사). 종료 코드 표 `1` · `2` 행이 새 경우를 안 적음 | SK-02 |
| `docs/tone-kit/dart-flutter-idioms.html` · 원본 `docs/tone/dart-flutter-idioms.md` | 페이지 `:274` 머리 `v0.1.0 · 갱신 2026-09-02`, `:1285-1286` 슬롯 표 칸에 정규식, `:1321` 완료 검사 넷째 줄 · 원본 `:3-4` 머리 설정 `0.1.0` · `2026-09-02`, `:633` | 표 칸이 아직 정규식을 싣는다 — 원본은 정규식의 기준 자리를 완료 검사 넷째 줄로 옮겼다. 원본 머리 판은 안 올라가 페이지 머리는 그대로가 맞다 | SK-03 · SK-13 |
| `docs/flutter-toolkit/flutter-ai-rules.html` · 원본 `flutter-toolkit/references/flutter-ai-rules.md` | 페이지 `:536-541` Makefile 관습 카드, `:540` 「`HAS_MAKEFILE = true` 를 감지하면 `make <target>` 을 우선한다」 · 원본 `:115` | 타겟별 확인 조건이 없다 | SK-04 |
| `docs/flutter-toolkit/project-detection.html` · 원본 `flutter-toolkit/references/project-detection.md` | 페이지 `:268` 절 설명, `:274-280` 감지 순서 1 ~ 3, `:294` 스킬 매핑 소제목, `:550` 감지 결과 틀 줄 · 원본 `:34` · `:47-56` · `:173` | 4 번(타겟별 `grep -qE` 확인) · 묶음 타겟만 있는 Makefile 설명 없음. `:550` 이 옛 줄 | SK-05 |
| `docs/infra-kit/infra-test.html` · 원본 `infra-kit/skills/infra-test/SKILL.md` | 페이지 `:507-508` 도구 변수, `:540-548` 규칙 1, `:632-637` 「빼면 생기는 일」 표 · 원본 `:221` · `:253-301` · `:388-389` | 검사 스크립트를 싣는 페이지인데 규칙 1 이 옛 줄 검사뿐 — YAML 구조 읽기 블록 없음(원본 코드 블록 줄 215 중 189). 표에 YAML 구조 읽기 행 없음, `CORE_TOOLS` 행이 옛 설명 | SK-06 |
| `docs/harness/plugin-validation.html` · 원본 `harness/docs/guides/plugin-validation-guide.md` | 페이지 `:132` 머리 `v1.4.1 · 2026-09-26`, `:277-279` V8 요약 카드, `:405-422` V8 절, `:478-484` V10 판정 카드, `:774-778` V8 나쁜 예 · 원본 `:3-4` 머리 설정, `:391-424` V8 따옴표 규칙, `:455-475` V10 1.4.1 절 | V8 따옴표 규칙 전부 없음(요약 카드 · 절 이름표 · 나쁜 예 둘 · 고치는 법). V10 1.4.1 은 한 문단으로 줄여 실렸다 — 1.4.0 판의 잘못 잡던 예 · 단순화 다섯 곳 등이 빠짐 | SK-07 · SK-13 |
| `docs/process/kaizen-flow.html` · 원본 `.claude/skills/kaizen-orchestrator/SKILL.md` | 페이지 `:242-246` 「동시 실행」 목록(원본 `:195-196` 두 줄만), `:403-545` 킷 카드 13 개의 파일 표시 · 원본 `:197` 범위 줄 설명, `:420` ~ `:525` 킷 Phase `**범위:**` 줄 | 킷 카드 13 개 가운데 12 개의 파일 표시가 새 범위 줄보다 좁다(Phase 5 카드에 `flutter-toolkit/evals/` 없음 — c3b-notes 1 번). 도우미 `cards` 가 `f81568d` 원본으로는 13/13 이 같다고 낸다 — 카드는 옛 원본 그대로다 | SK-08 |
| `docs/design-kit/design-mockup.html` · 원본 `design-kit/skills/design-mockup/SKILL.md` | 페이지 `:477-481` 감지 대상 블록, `:484-489` 「찾은 입력의 적용」 카드, `:629` 승인 기록 틀 폐기 칸 · 원본 `:60` · `:68` · `:161` · `:166` | c4d-notes R4 세 자리 그대로 — `.planning/prd-*.md` 줄 없음, PRD 비범위 표 규칙 없음, 폐기 칸이 옛 자리표시자, `PRD 없음` 문단 없음. 원본 코드 블록 줄 21 중 19 | SK-09 |
| `docs/api-kit/multi-sample-pagination-variance.html` · 원본 `docs/api/contract/multi-sample-pagination-variance.md`, 바로잡은 원문 `docs/superpowers/specs/2026-09-02-api-kit-design.md:249-262` · `docs/api/research-log.md:161-176` | 페이지 `:425` 제목 「경로 간 불변식은 Hurl 로 표현되지 않는다」, `:428` 「Hurl 문법으로 쓸 수 없다」, `:436-437` 「← 문법 없음」, `:470` 출처 이름표, `:857` 함정 줄 | 설계 §9.2 는 2026-09-26 에 「capture 로 적을 수 있다 — 후처리에 두는 까닭은 `판정 불가` 를 가를 자리」 로 바로잡혔다. 페이지는 옛 이유 그대로. 페이지의 1 차 원본 md 는 이 절을 다루지 않고 머리 설정도 안 바뀌었다(`0.1.0` · `2026-09-04`) | SK-10 · SK-13 |
| `docs/design-kit/design-concept.html` · 원본 `design-kit/skills/design-concept/SKILL.md` | 페이지 `:277` 나쁜 예 코드 블록이 공백 세 칸 뒤에 `Accent` · `#E8965A` 표 행으로 시작 · 원본 `:24-26` 여는 줄 · 내용 · 닫는 줄이 같은 세 칸 들여쓰기 | 내용 앞 공백이 3 칸 — 원본 기준 0 칸 | SK-11 |
| 열한 쪽 전체 | 도우미 `ER-01` 로 잼 | 375 · 1280 · 375 + 글자 간격 0.06em 모두 넘침 0, 콘솔 오류 0 — 지금은 문제 없다. 고치다 깨지지 않게 잠근다 | ER-01 |

구현 후보는 하나로 정해져 있다 — 과제가 「새로 쓰지 말고 바뀐 부분을 옮긴다」 로 정했다. 옵션 표를 따로 두지 않는다.

## Skill

- [ ] SK-01: `docs/bambu-kit/bambu-print-profile.html` 에 원본의 바뀐 두 자리(안 돈 검사만 적는 줄 `:2041`, `G91` 을 XY 에만 적용하는 줄 `:2245`)가 들어가고, [미검증] 표의 「enum 줄만 빠진 목록」 행이 더는 「같음」(키 존재 · 종류 · enum 값이 모두 빠진다)이라고 적지 않는다 — Given 공통 전제 G, When `m SK-01`, Then 첫 줄 `units_ok=2/2` · 둘째 줄 `n=0` (시작 판 `units_ok=0/2 miss=['2041:0.08', '2245:0.05']` · `n=1`). 측정: 도우미 `chg`(검사 코드 `1600-1612` 는 뺀다) · `rcnt` 정규식 `enum줄만빠진목록(?:09-25)?같음` [exact]
- [ ] SK-02: `docs/design-kit/visual-change-protocol.html` 이 원본 §6 의 바뀐 글을 모두 담는다 — `status` 는 `approved` 하나 · `excluded_surfaces: []` 규칙 두 줄과 검사 코드 새 줄 9 개(`2 스키마 · 입력 오류` 설명 줄 · 폴더와 UTF-8 아닌 입력 분기 · `status` 검사 · `excluded_surfaces` 키 검사), 옛 설명 줄 「2 스키마 오류 / 3 대상 0 건」 은 남지 않으며, 페이지의 종료 코드 표 `1` 행에 `excluded_surfaces` 가 2 번 이상(`reason` 없음 · 키 없음), `2` 행에 `status` 와 `UTF-8` 이 각 1 번 이상 나온다. Given 공통 전제 G, When `m SK-02`, Then `units_ok=11/11` · `[2 스키마 오류 / 3 대상 0 건]=0` · `table=1 row1_excl=` 2 이상 · `row2_status=` 1 이상 · `row2_utf8=` 1 이상 (시작 판 `units_ok=0/11` · `=1` · `table=1 row1_excl=1 row2_status=0 row2_utf8=0`). 측정: 도우미 `chg` · `cnt` · `exitrows` [exact]
- [ ] SK-03: `docs/tone-kit/dart-flutter-idioms.html` 의 슬롯 표 `fallback_identifier_pattern` 칸이 원본 `:633` 처럼 정규식을 싣지 않고 기준 자리(완료 검사 넷째 줄)를 가리킨다 — Given 공통 전제 G, When `m SK-03`, Then `units_ok=1/1` · 정규식 글 `\b(effective|resolved)[A-Z]` 이 페이지 보이는 글에 정확히 1 번(완료 검사 코드 블록 줄) (시작 판 `units_ok=0/1` · `=2`). 측정: 도우미 `chg` · `cnt` [exact]
- [ ] SK-04: `docs/flutter-toolkit/flutter-ai-rules.html` 의 Makefile 관습 카드가 원본 `:115`(타겟별 확인으로 그 단계의 타겟이 있을 때만 `make <target>` 우선, 묶음 타겟만 있으면 기본 명령)를 담고 옛 줄 「`HAS_MAKEFILE = true` 를 감지하면 `make <target>` 을 우선한다」 가 남지 않는다 — Given 공통 전제 G, When `m SK-04`, Then `units_ok=1/1` · 옛 줄 `=0` (시작 판 `units_ok=0/1` · `=1`). 측정: 도우미 `chg` · `cnt` [exact]
- [ ] SK-05: `docs/flutter-toolkit/project-detection.html` 이 원본 Step 2b 의 바뀐 글 — 절 설명의 「그 단계의 타겟이 실제로 있을 때만」, 감지 순서 4 번과 그 `grep -qE '^<타겟>[[:space:]]*:' Makefile` 줄, 종료 코드 0 · 묶음 타겟 설명, 매핑 소제목 괄호, 감지 결과 틀의 새 `Makefile:` 줄 — 을 담고 옛 틀 줄 「`# HAS_MAKEFILE — true 면 $MAKE <target> 우선`」 이 남지 않는다. Given 공통 전제 G, When `m SK-05`, Then `units_ok=6/6` · 옛 줄 `=0` (시작 판 `units_ok=0/6` · `=1`). 측정: 도우미 `chg` · `cnt` [exact]
- [ ] SK-06: `docs/infra-kit/infra-test.html` 의 검사 스크립트가 원본의 새 규칙 1(YAML 구조로 `jobs.*.steps[].uses` 를 읽고, python3 · PyYAML 이 없을 때만 줄 검사로 도는 블록 — 원본 `:221` · `:253-301`)을 담고, 「빼면 생기는 일」 표에 YAML 구조 읽기 행과 새 `CORE_TOOLS` 행이 들어가며, 옛 글 둘(스크립트의 `# 없으면 해당 rule 만 [미검증]` · 표의 「VIOLATION을 오보하고 exit 1로 끝난다」)이 남지 않는다 — Given 공통 전제 G, When `m SK-06`, Then `units_ok=39/39` · 옛 글 둘 모두 `=0` (시작 판 `units_ok=11/39` · `=1` · `=1`). 측정: 도우미 `chg` · `cnt` [exact]
- [ ] SK-07: `docs/harness/plugin-validation.html` 이 원본 1.4.1 의 V8 따옴표 규칙과 V10 판을 둘 다 담는다 — V8: 무엇을 검사하나(두 가지) · 따옴표도 같은 급의 실패 문단 · 직접 실행 판정 · 예외 · 나쁜 예 1(따옴표 든 `run-guard.sh`) · 나쁜 예 2(따옴표 밖 변수 네 줄) · 고치는 법, V10: 코드 블록 판정 · `|` 두 개 이상 · 4 칸 들여쓰기 · 단순화한 다섯 곳 문단. 옛 나쁜 예와 옛 명령 예 `"command": "${CLAUDE_PLUGIN_ROOT}/scripts/run-guard.sh"` · `"command": "${CLAUDE_PLUGIN_ROOT}/scripts/x.sh"`(따옴표 없이 쓴 꼴)는 남지 않고, V8 절 이름표와 V8 요약 카드 제목에 「따옴표」 가 든다. Given 공통 전제 G, When `m SK-07`, Then `units_ok=18/18` · 옛 명령 예 둘 `=0` · `label=1 vtitle=1` (시작 판 `units_ok=1/18` · `=1` · `=1` · `label=0 vtitle=0`). 측정: 도우미 `chg` · `cnt` · `v8` [exact]
- [ ] SK-08: `docs/process/kaizen-flow.html` 의 킷 카드 13 개(Phase 5 ~ 17) 파일 표시가 각각 원본 오케스트레이터 해당 Phase 의 `**범위:**` 줄과 이어지는 리서치 문서 줄에 적힌 경로 집합과 정확히 같고(순서 무시 — Phase 5 카드에 `flutter-toolkit/evals/` 포함), 「공통 실행 패턴」 절이 원본 `:197`(범위 줄은 킷에 실제로 있는 폴더를 모두 적어 만든다 · 폴더를 새로 만들면 스크립트를 다시 돌린다)를 담는다 — Given 공통 전제 G, When `m SK-08`, Then `phases=13 cards_equal=13/13` · `units_ok=1/1` (시작 판 `cards_equal=1/13` · `units_ok=0/1`). 알려진 답: 같은 도우미 `cards` 를 옛 원본(`f81568d` 판)과 시작 판 페이지에 돌리면 `cards_equal=13/13` — 카드가 옛 원본 글자 그대로임을 맞힌다(봉인 전 실측) [exact, collective]
- [ ] SK-09: `docs/design-kit/design-mockup.html` 이 c4d-notes R4 세 자리와 원본의 새 문단을 담는다 — 감지 대상 블록의 `.planning/prd-*.md` 줄, 「찾은 입력의 적용」 의 PRD 비범위 표 규칙, 승인 기록 틀의 새 폐기 칸 줄, `PRD 없음` 문단. 옛 자리표시자 「{이번 결정에서 버린 안·요소와 이유 — 없으면」 은 남지 않고, 원본 코드 블록 줄(공백 뺀 8 자 이상)을 모두 담는다. Given 공통 전제 G, When `m SK-09`, Then `units_ok=4/4` · 옛 자리표시자 `=0` · `fen` 줄 `lines=21 in_old=19 in_new=21 lost=0` (시작 판 `units_ok=0/4` · `=1` · `lines=21 in_old=19 in_new=19 lost=0`). 측정: 도우미 `chg` · `cnt` · `fen` [exact]
- [ ] SK-10: `docs/api-kit/multi-sample-pagination-variance.html` 의 「경로 간 불변식」 절(`:425` · `:428` 자리)이 바로잡힌 설계 §9.2 를 따른다 — capture 로 적는 예(`{{total}}` 이 든 판정식)와 후처리에 두는 새 이유 `판정 불가` 가 페이지에 있고, 옛 주장 셋(제목 「경로 간 불변식은 Hurl 로 표현되지 않는다」 · 「Hurl 문법으로 쓸 수 없다」 · 코드 블록의 「← 문법 없음」)이 남지 않는다. 옛 주장을 정정 기록으로 인용하려면 `regression-diff-failure-policy.html:808` 처럼 「Hurl 로 표현 불가」 꼴로 적는다. `cnt` 는 페이지 전체를 세므로 구현 재량인 `:470` 출처 이름표 · `:857` 함정 줄을 고쳐도 같은 기준(옛 주장 셋 0)을 따른다. Given 공통 전제 G, When `m SK-10`, Then `[{{total}}]=` 1 이상 · `[판정 불가]=` 1 이상 · `[Hurl 문법으로 쓸 수 없다]=0` · `[← 문법 없음]=0` · `h2_old=0` (시작 판 `0` · `0` · `1` · `1` · `1`). 측정: 도우미 `cnt` 와 HTML 의 옛 제목 줄 수 [exact]
- [ ] SK-11: `docs/design-kit/design-concept.html` 나쁜 예 코드 `| Accent | #E8965A |` 앞 공백이 0 칸이고 이 페이지에서 바뀐 줄은 그 한 줄뿐이다 — Given 공통 전제 G, When `m SK-11`, Then `lead=0` · `numstat=1/1` (시작 판 `lead=3` · `numstat=` 빈 값). 측정: 도우미 `lead` · `git diff --numstat BASE TIP` [exact]
- [ ] SK-12: 열한 쪽이 옛 판(`39ddc12`) 대비 원본 글을 잃지 않는다 — 쪽마다 원본 코드 표시 빠짐 0 · 원본 낱말 비율이 옛 판 이상 · 원본 코드 블록 줄 빠짐 0. Given 공통 전제 G, When `m SK-12`, Then 도우미 `PAIRS` 의 열한 줄이 모두 `lost=0 … wr_ok=1 fen_lost=0` (시작 판 열한 줄 모두 같은 값, 낱말 비율 0.73 · 0.95 · 0.95 · 0.88 · 0.81 · 0.84 · 0.78 · 0.24 · 0.54 · 0.90 · 0.48). 도우미 `cov` · `fen` 은 핸드오프 도구 `coverage.py` · `fence2.py` 와 같은 식이고 옛 판을 파일로 받는다(`fence2.py` 는 옛 판 커밋이 `509d295` 로 박혀 있어 쓸 수 없다) [exact, collective]
- [ ] SK-13: 머리 판 번호 · 날짜를 원본 머리 설정에서 뽑는다 — 머리 설정이 있는 원본 셋의 페이지(dart-flutter-idioms · plugin-validation · multi-sample-pagination-variance)는 보이는 글에 `v<version>` 과 그 뒤 16 자 안에 `<last_updated>` 가 있고, 열한 쪽 모두 새로 보이는 판 번호 꼴(`v?숫자.숫자.숫자`) 가운데 옛 페이지에도 원본에도 없는 것이 0 개다. Given 공통 전제 G, When `m SK-13`, Then 셋이 `hdr=1`(`v0.1.0·2026-09-02` · `v1.4.1·2026-09-26` · `v0.1.0·2026-09-04`), 나머지 여덟이 `hdr=none`, 열한 줄 모두 `newver_bad=0` (시작 판 같은 값). 양성 대조: plugin-validation 머리를 `v1.4.0 · 2026-09-25` 로 바꾼 사본 → `hdr=0`, 임시 복제본 kaizen-flow 에 `harness 0.14.1 · v9.9.9` 한 줄을 더해 커밋 → `newver_bad=2` (봉인 전 실측) [exact, collective]

## Script

- [ ] SC-00: N/A (릴리스 스크립트 · 판 올리기 · `marketplace.json` 은 이 계약이 건드리지 않는다 — `docs/` 는 어느 킷 폴더에도 속하지 않아 올릴 판이 없다. 측정: `m SC-00` 이 `release_paths=0` — 바뀐 경로 가운데 `scripts/` · `.claude-plugin/` 0 개. 양성 대조: 임시 복제본에서 `scripts/release.sh` 를 고쳐 커밋하면 `release_paths=1`, 봉인 전 실측) [exact]

## Error

- [ ] ER-01: 열한 쪽이 좁은 화면 · 넓은 화면 · 글자 간격이 넓어진 좁은 화면(CI 리눅스가 글자를 더 넓게 그리는 것을 맥에서 재현)에서 가로로 넘치지 않고 콘솔 오류 · 페이지 오류가 0 이다 — Given 공통 전제 G, When `m ER-01` 이 도우미 `PAGES` 열한 쪽을 어두운 색 설정으로 폭 375 · 1280 으로 열고, 375 에서는 `*{letter-spacing:0.06em !important}` 를 넣어 한 번 더 열면, Then 쪽마다 `scrollWidth - clientWidth` 가 세 경우 모두 2 이하 · `err=0` 이고 끝줄 `bad=0/11` (시작 판 `bad=0/11`, 열한 쪽 모두 세 값 0). 양성 대조: 900px 폭 요소와 오류를 던지는 스크립트를 담은 임시 페이지 → `BAD … w375=533 … err=6`, 375 에서는 맞고 글자 간격에서만 넘치는 임시 페이지 → `w375=0 … ls375=5` 로 `BAD` (봉인 전 실측) [exact, collective]
- [ ] ER-02: 넘침을 가리는 선언을 더하지 않았다 — 열한 쪽의 더해진 줄에 `overflow` · `overflow-x` 값 `hidden` · `clip` 이 0 줄이다(docs-site Gotcha 11). 측정: `m ER-02` 가 `hidden_added=0` (시작 판 같은 값). 양성 대조: 임시 복제본에서 bambu-print-profile.html 에 `.x{overflow:hidden}` 한 줄을 더해 커밋하면 `hidden_added=1` (봉인 전 실측) [exact]

## Architecture

- [ ] AR-01: 바뀐 파일이 기대 집합 안이고 페이지마다 한 커밋이다 — Given 공통 전제 G, `BASE` 부터 `TIP` 까지 `git diff --name-only` 로 모은 경로가 도우미 `ALLOWED` 의 15 경로(열한 쪽 · 계약 · QA 리포트 · 개정 파일 · notes) 안에만 있고(부분 집합 — 원본 · 공통 스타일 · 킷 폴더 · `scripts/` · `.claude/` 는 없음, 생성물 없음), 열한 쪽이 모두 바뀌었고, 병합 아닌 커밋마다 `docs/` 파일이 1 개 이하이며, `docs/` 와 `.harness/` 를 한 커밋에 섞지 않는다. 측정: `m AR-01` 이 `extra=0 pages=11/11 multi_page=0 mixed=0` (시작 판 `changed=0 extra=0 pages=0/11 multi_page=0 mixed=0`). 양성 대조: 임시 복제본에서 페이지 셋 · `README.md` · `scripts/release.sh` · 새 `docs/` 파일 · notes 를 한 커밋에 넣으면 `changed=7 extra=3 pages=3/11 multi_page=1 mixed=1` 이고 남는 경로 셋을 찍는다 (봉인 전 실측) [exact, collective]
- [ ] AR-02: 결정과 넘김을 notes 에 남긴다 — Given 끝점 `TIP`, notes 파일 `.harness/.meta/after-kaizen-0926/d1-notes.md` 가 커밋돼 있고 열 토큰 `snapshot-sealing-canonicalization` · `research-log` · `reflect-digest` · `adapter-contract` · `adapter-dart-flutter` · `locale-korean` · `rust-kit/references/project-detection.md` · `phase-research-templates` · `dart-flutter-idioms` · `tone-guide` 가 각각 한글 15 자 이상인 줄에 1 번 이상 든다(토큰만 늘어놓거나 「tone-guide 했음」 같은 짧은 줄은 세지 않는다). 담을 내용: 대응 페이지가 없는 원본 목록(새 페이지를 만들지 않음), 원본이 바뀌었지만 페이지가 이미 맞는 `docs/api-kit/snapshot-sealing-canonicalization.html`(머리 `v0.1.2 · 2026-09-26`), `docs/tone/dart-flutter-idioms.md` 가 글을 바꾸고도 머리 판을 안 올린 것(페이지 머리는 원본을 따라 그대로 둠 · 원본 판 올리기는 넘김), 바뀐 줄 대조에서 뺀 두 곳(bambu 검사 코드 · kaizen-flow 의 197 줄 밖 바뀐 자리)과 그 사유, tone-guide 1 · 5 단계 결과. 측정: `m AR-02` 가 `committed=1` 과 열 값 모두 1 이상 (시작 판 `committed=0` 과 0 열). 양성 대조: 임시 복제본에 토큰마다 한글 설명 줄을 담은 notes 를 커밋하면 `committed=1` 과 1 열, 열 토큰을 한 줄에 늘어놓기만 한 notes 면 `committed=1` 과 0 열, 토큰 없는 notes 면 `committed=1` 과 0 열 (봉인 전 실측) [exact, enumerated]
- [ ] AR-03: 쓰는 쪽(첫 화면 `docs/index.html` 의 등록과 내부 링크)이 그대로다 — 끝점 트리에서 `python3 scripts/check-docs-links.py` 가 종료 코드 0 · `깨진 링크 없음` · `페이지 176 · 등록 176` 을 낸다. 측정: `m AR-03` 이 `rc=0` · `broken0=1` · `nav=페이지 176 · 등록 176` (시작 판 같은 값). 양성 대조: 임시 복제본 kaizen-flow.html 에 없는 링크 하나를 넣고 새 `docs/` 파일을 더해 커밋하면 `rc=1 broken0=0 nav=페이지 177 · 등록 176` (봉인 전 실측) [exact]

## Anti-patterns

- [ ] AP-01: 버전을 하드코딩하지 않는다 — plugin.json에서 읽어야 한다. 이 계약에 적용: 정적 페이지는 `plugin.json` 을 읽을 수 없으니 열한 쪽의 더해진 줄에 지금 킷 판 번호(끝점 `*/.claude-plugin/plugin.json` 의 `version` 값, 시작 판 8 종)를 박지 않는다 — 박으면 다음 릴리스에 옛 값이 된다. 측정: `m AP-01` 이 `hits=0` (시작 판 `versions=8 hits=0`). 양성 대조: 임시 복제본 kaizen-flow.html 에 `harness 0.14.1` 이 든 줄을 더해 커밋하면 `hits=1` (봉인 전 실측) [exact]
- [ ] AP-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수 (```text, ```bash, ```yaml 등). 판정 권위는 validate-plugin V6 상태기계다 — 여는/닫는 fence 가 동형이라 줄 단위 정규식으로는 판정 불가. 이 계약에 적용: 새 notes 파일. V6 는 킷 폴더만 읽어 notes 를 보지 않으므로 도우미가 V6 와 같은 상태기계(줄 앞 공백을 벗긴 뒤 백틱 세 개로 시작하면 열고 닫기를 번갈아 셈)를 notes 에 돌린다. 측정: `m AP-03` 이 `committed=1 bare=0`. 양성 대조: 임시 복제본 notes 에 언어 없는 fence 한 쌍 → `bare=1` (봉인 전 실측). 같은 셈 대조: 입력 열 가지(언어 없음 · `text` · 앞뒤 공백 · 두 번째 여는 줄만 없음 · 백틱 네 개 · `~~~` · 목록 안 여는 줄 · 탭 들여쓰기 · 안 닫힘 · 셋 가운데 둘)를 임시 복제본의 킷 README 에 넣어 `python3 scripts/validate-plugin.py bambu-kit --check=code-fence` 의 bare 줄 수와 도우미 awk 의 `bare` 를 나란히 쟀더니 열 가지 모두 같았다(1 · 0 · 1 · 1 · 0 · 0 · 1 · 1 · 1 · 2, 봉인 전 실측) [exact]

## Reusability

- [ ] RE-01: N/A (산출물이 따로 떨어진 HTML 문서 페이지와 notes 뿐이라 다른 곳에서 가져다 쓸 컴포넌트 · 모듈이 없다. 측정: `m RE-01` 이 `added_files=0` — `docs/` 에 새 파일 0. 양성 대조: 임시 복제본에 `docs/` 새 파일 하나를 커밋하면 `added_files=1`, 봉인 전 실측) [exact]
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다 — 각 페이지의 기존 CSS 변수 · 클래스 · 카드 · 표 꼴 안에서 고치고, 새 파일(스타일 · 스크립트 · 페이지)이나 외부 스타일 · 외부 스크립트 · `@import` 를 더하지 않는다. 측정: `m RE-02` 가 `added_files=0 ext_added=0` (시작 판 같은 값). 양성 대조: 임시 복제본에서 `docs/` 새 파일 하나와 design-concept.html 의 `<link rel="stylesheet" href="x.css">` 한 줄을 커밋하면 `added_files=1 ext_added=1` (봉인 전 실측) [exact]

## Diagnostics

- [ ] DG-01: N/A (commands.analyze `bash -n scripts/release.sh` 가 재는 `scripts/release.sh` 는 이번 바뀐 파일에 없다. 측정: `m DG-01` 이 `release_sh=0`. 양성 대조: 임시 복제본에서 그 파일을 고쳐 커밋하면 `release_sh=1`) [exact]
- [ ] DG-02: IDE diagnostics 워닝/인포 0개 ([] 제외) — 편집기 진단을 명령줄로 같게 잰다(계약 · QA 리포트 · 개정 파일은 뺀다): 열한 쪽의 페이지 안 스크립트가 모두 `node --check` 통과 · `<style>` 블록마다 중괄호 짝이 맞음 · 짝 안 맞는 태그 0 (열한 쪽 합) · notes 의 markdownlint-cli2 0.23.2(MD013 끔, 편집기 확장과 같은 설정) 경고 0. 시작 판 열한 쪽이 쪽마다 `tag_bad=0` 이라 절대 기준 0 이다. 측정: `m DG-02` 가 `js_bad=0 tag_bad=0 css_bad=0 md=0` (시작 판 `js_bad=0 tag_bad=0 css_bad=0 md=absent` — notes 가 아직 없다. 도구가 없으면 도우미가 임시 폴더에 설치한다). 양성 대조: 망가진 스크립트 · 닫히지 않은 중괄호 · 닫히지 않은 `div` 를 담은 임시 페이지 → `tag_bad=1 css_bad=1` · `node --check` 종료 코드 1, `#bad heading` 줄이 든 md → 경고 2 (봉인 전 실측). 설치가 안 되면(망 끊김 등) 도우미가 `md=ENV_FAIL` 을 찍는다 — 그 칸만 FAIL 이 아니라 `[미검증:ENV]` 로 적고, 나머지 세 칸은 그대로 판정한다. 양성 대조: 닿지 않는 저장소 주소(`npm_config_registry=http://127.0.0.1:9`)로 부르면 `md=ENV_FAIL` (봉인 전 실측) [exact]
- [ ] DG-03: N/A (commands.test `bash scripts/release.sh 2>&1 || true` 가 재는 `scripts/release.sh` 는 이번 바뀐 파일에 없다. 측정: DG-01 과 같은 `m DG-01` 이 `release_sh=0`) [exact]
- [ ] DG-04: 실제 앱/서버 구동 시 에러 0개 — 이 계약에 적용: 열한 쪽을 레포 검사기 `node scripts/check-docs-a11y.js`(가로 넘침 375 · 768 · 1280 · 콘솔 오류 · 글자 대비 · 누르는 자리 크기)로 연다. 측정: `m DG-04` 가 `rc=0` · `11/11 PASS` (시작 판 같은 값). 양성 대조: 오류를 던지고 900px 로 넘치는 임시 페이지 → `0/1 PASS` · 종료 코드 1 (봉인 전 실측) [exact]
- [ ] DG-05: CI(자동 검사) 단계를 로컬에서 전부 돌려 통과한다 — Given 작업 폴더 W 가 끝점과 같다(`git -C W rev-parse HEAD` 가 `TIP` 이고 `git -C W status --porcelain --untracked-files=no` 가 빈 출력 — 아니면 도우미가 `W_NOT_TIP` 을 찍고 멈춘다), When `m DG-05` 가 `/Users/jackson/Hub/10_Dev/claude-plugins/.harness/handoff/2026-09-26-tools/ci-local.sh` 를 W 에 돌리면, Then 요약에 `rc=0` 줄이 22 개이고 `rc=0` 이 아닌 줄은 `feedback-agg-test SKIP (yq 없음)` 하나뿐이다. 도구 파일은 이 가지 밖(본 체크아웃)에 있어 커밋으로 고정되지 않으므로 도우미가 그 내용 지문(`git hash-object`)을 봉인 때 값 `TOOL_BLOB` 과 대조해 `tool_same` 을 찍는다. 측정: `m DG-05` 가 `tool_same=1 rc0=22 other=[feedback-agg-test SKIP (yq 없음);]` (시작 판 봉인 전 실측: 같은 값). `tool_same=0`(도구 파일이 봉인 뒤 바뀜)이거나 요약 파일이 없으면(도우미가 `ci_summary=absent` 를 찍음) 그 회차는 PASS 도 FAIL 도 아니라 `[미검증:ENV]` 로 적고, 평가자는 지금 지문 · 요약 유무를 보고서에 옮긴다 — 도구를 되돌리거나 고쳐 다시 재는 일은 이 계약이 하지 않는다. 음성 대조: 이 계약이 기대는 `docs-a11y` · `docs-links` 단계는 원래 폭 · 글자 간격에서 재므로 시작 판에서도 통과한다 — 페이지 내용 결함은 SK 조건이, 글자 간격 넘침은 ER-01 이 잡는다 [exact]

## 범위 경계

항목별 처리 — 입력은 과제 목록과 `git diff --name-status f81568d 39ddc12` 로 뽑은, 매핑 표 원본 경로 안에서 바뀐 파일 17 개다.

| 항목 | 처리 | 조건 · 사유 |
| --- | --- | --- |
| `bambu-kit/skills/bambu-print-profile/SKILL.md` → `docs/bambu-kit/bambu-print-profile.html` | 계약에 넣음 | SK-01. 검사 코드 `:1600-1612` 는 바뀐 줄 대조에서 뺀다 — 페이지가 검사 코드를 싣지 않고 `:1636-1657` 표로 요약한다(`OPTION LIST` 0 건). 같은 동작 변화는 원본 `:2041` 과 표 행 검사가 잰다 |
| `design-kit/references/visual-change-protocol.md` → `docs/design-kit/visual-change-protocol.html` | 계약에 넣음 | SK-02 |
| `docs/tone/dart-flutter-idioms.md` → `docs/tone-kit/dart-flutter-idioms.html` | 계약에 넣음 | SK-03 · SK-13. 원본 머리 판이 `0.1.0` · `2026-09-02` 그대로라 페이지 머리도 그대로다. 원본 판을 올리는 일은 넘김 — 원본은 이 계약 범위 밖이다 |
| `flutter-toolkit/references/flutter-ai-rules.md` → `docs/flutter-toolkit/flutter-ai-rules.html` | 계약에 넣음 | SK-04 |
| `flutter-toolkit/references/project-detection.md` → `docs/flutter-toolkit/project-detection.html` | 계약에 넣음 | SK-05 |
| `infra-kit/skills/infra-test/SKILL.md` → `docs/infra-kit/infra-test.html` | 계약에 넣음 | SK-06 |
| `harness/docs/guides/plugin-validation-guide.md` → `docs/harness/plugin-validation.html` (V8 따옴표 규칙 · V10 판) | 계약에 넣음 | SK-07 · SK-13. 머리 · 변경 이력 1.4.1 행은 이미 옮겨져 있다(바뀐 줄 대조에서 1.4.1 행은 `ok`, 1.4.0 행은 순서만 옮긴 줄이라 세지 않는다) |
| `.claude/skills/kaizen-orchestrator/SKILL.md` → `docs/process/kaizen-flow.html` (킷 카드 범위 칸 · Phase 5 카드) | 계약에 넣음 | SK-08. 바뀐 줄 대조는 `:197` 만 본다. 원본의 다른 바뀐 자리 — 참조 목록 `:25`, research-log Gotcha `:56`, 데이터 풀 표 15 ~ 17 행 `:313-315`, F2 매핑 표를 가리키기로 바꾼 곳 `:613-619`, F4 research-log 목록 · 점검표 `:738-767` — 은 페이지가 그 절을 싣지 않아 옮길 자리가 없다(페이지 F2 · F4 카드는 한 줄 요약이고 지금 원본과 어긋나지 않는다) |
| `design-kit/skills/design-mockup/SKILL.md` → `docs/design-kit/design-mockup.html` (`:481` · `:484-489` · `:629`) | 계약에 넣음 | SK-09 |
| `docs/api/contract/multi-sample-pagination-variance.md` → `docs/api-kit/multi-sample-pagination-variance.html` (`:425` · `:428`) | 계약에 넣음 | SK-10. 이 절의 원문은 페이지 1 차 원본 md 가 아니라 설계 기록 `docs/superpowers/specs/2026-09-02-api-kit-design.md` §9.2 다(md 에 `Hurl` 0 건). 출처 이름표 `:470` 과 함정 줄 `:857` 은 결론(후처리에 둔다)이 그대로라 고칠지는 구현 재량 — 고치면 SK-10 의 옛 주장 셋을 되살리지 않는다 |
| `docs/design-kit/design-concept.html:277` 공백 세 칸 (c3b-notes 2 번) | 계약에 넣음 | SK-11 |
| 담김 하한 · 머리 판 · 넘침 · 링크 · 접근성 · 로컬 CI | 계약에 넣음 | SK-12 · SK-13 · ER-01 · ER-02 · AR-03 · DG-04 · DG-05 |
| `docs/api/contract/snapshot-sealing-canonicalization.md` → `docs/api-kit/snapshot-sealing-canonicalization.html` | 넘김 (할 일 없음) | 원본이 `0.1.2` · `2026-09-26` 으로 바뀌었지만 페이지 `:287` 이 이미 `v0.1.2 · 최종 갱신 2026-09-26` 이고 `-0` 검사 절(`:307-323` · `:521-530`)도 새 글이다. notes 에 적는다(AR-02) |
| 대응 페이지가 없는 원본 — `docs/api/research-log.md` · `reflect-kit/skills/reflect-digest/SKILL.md` · `tone-kit/references/adapter-contract.md` · `tone-kit/references/adapter-dart-flutter.md` · `tone-kit/references/locale-korean.md` · `rust-kit/references/project-detection.md` · `.claude/skills/kaizen-orchestrator/references/phase-research-templates.md` | 넘김 (새 페이지를 만들지 않음) | 과제 지시. `docs/api-kit/` · `docs/reflect-kit/` · `docs/tone-kit/` · `docs/rust-kit/` · `docs/process/` 에 대응 파일이 없다(도우미와 같은 `find` 로 확인). 목록만 notes 에(AR-02) |
| 원본 파일 고치기(예: `docs/tone/dart-flutter-idioms.md` 머리 판) | 넘김 | 원본은 이 계약 범위 밖이다. 저장소 밖 원문이 필요한 일은 없다 |
| 공통 스타일 파일 · `prefers-reduced-motion` · 행간 · 320px 넘침(c3b-notes 3 번) | 넘김 | 다음 묶음(공통 틀 결정, 핸드오프 §C4 5 번) |
| 킷 폴더 · `scripts/` · `.claude/` · `docs/index.html` | 범위 밖 | 읽기만. AR-01 이 경로로 막는다 |

바뀐 줄 대조(`chg`)는 새 글이 페이지에 들었는지만 보고 어느 절에 들었는지는 보지 않는다 — 의도한 느슨함이다(교차 진단 지적). 과제가 「바뀐 부분을 옮긴다」 이고 자리 이름이 원본과 페이지에서 달라 절 대응을 기계로 맞출 수 없기 때문이다.
자리까지 보는 검사는 SK-02 `exitrows` · SK-07 `v8` · SK-08 `cards` · SK-11 `lead` 이고, 나머지 SK 는 옛 글 검사(`cnt` · `rcnt`)가 옛 자리에 옛 글이 남았는지를 잡는다. 새 글의 자리는 QA 평가자가 페이지를 열어 본다.
AR-02 는 토큰마다 한글 15 자 이상인 줄을 요구한다(교차 진단 지적 — 낱말만 있으면 통과하던 틈). 15 자는 「tone-guide 했음」(한글 2 자) 같은 줄을 떨어뜨리고 한 문장짜리 설명은 넘는 값이다.

계약 파일의 편집기 경고 2 건(MD041 첫 줄 제목 · MD038 코드 표시 안 공백)은 계약 형식 규칙에서 나온다 — 허용 헤더 목록에 1 단계 제목이 없고, AP-03 문구는 `project.yaml` 글자 그대로다. c3b 계약도 같은 2 건이다. 계약 · QA 리포트 · 개정 파일은 DG-02 대상에서 뺀다.

범위 밖(이 계약이 고치지 않는다): 원본 파일 전부 · 킷 폴더 · `scripts/` · `.claude/` · `docs/index.html` · 다른 문서 페이지 · 킷 `plugin.json` 판 · 공통 스타일.

커버리지 해소 — Step 6.5 (4) 검출기가 낸 `UNCOVERED` 와 목록을 한 곳에만 둔 조건:

- 커버리지 해소: AR-01 — 경로 기대 집합은 도우미 `ALLOWED` 한 곳에만 적는다(목록을 두 번 적지 않는다는 계약 형식 규칙). SK-12 · SK-13 · ER-01 의 열한 쪽도 도우미 `PAIRS` · `PAGES` 한 곳이다
- 커버리지 해소: AR-02 — 검출기가 산문의 경로 넷(`docs/tone/dart-flutter-idioms.md` · `.harness/.meta/after-kaizen-0926/d1-notes.md` · `docs/api-kit/snapshot-sealing-canonicalization.html` · `rust-kit/references/project-detection.md`)을 냈다. notes 경로는 도우미 `NOTES` 변수가, 나머지 셋은 「담을 내용」 설명이고 잴 대상은 열 토큰(`dart-flutter-idioms` · `snapshot-sealing-canonicalization` · `rust-kit/references/project-detection.md` 포함)이며 `m AR-02` 의 토큰 목록이 산문과 같은 글자로 센다
- 커버리지 해소: SK-08 — Phase 13 개의 경로는 도우미 `cards` 가 원본 `**범위:**` 줄에서 뽑는다. `flutter-toolkit/evals/` 는 그중 한 예시다

## 회귀 게이트 — 측정 도우미 · 봉인 전 실측

평가 때 이 블록을 떼어 bash 에서 불러 쓴다. `TMPDIR` 은 평가자 임시 폴더로 준다. 도우미는 `$T` 아래에만 쓴다 — 작업 폴더와 그 밖의 입력은 지우지 마라.
브라우저 도구는 작업 폴더 W 의 `node_modules`(추적 안 되는 폴더, `npm ci` 로 설치)를 `NODE_PATH` 로 빌려 쓴다.

준비 단계 실측(봉인 전, 이 기계): `command -v node` → fnm 경로 · 종료 코드 0 (`v24.14.1`), `command -v python3` · `command -v git` 종료 코드 0,
W 에서 `npm ci` 종료 코드 0 → `node_modules/playwright-core` 판 `1.58.2`, 브라우저 실행 파일은 사용자 폴더 `~/Library/Caches/ms-playwright/chromium_headless_shell-1208` 에서 온다(c3b 계약과 같은 판).
그 폴더에 브라우저가 없으면 `pw.js` 가 `Executable doesn't exist` 로 종료 코드 2 를 낸다. 복구: `cd W && node_modules/.bin/playwright-core install chromium-headless-shell` 뒤 다시 잰다 — 브라우저가 없어 못 잰 조건은 FAIL 이 아니라 환경 실패로 보고한다.
`markdownlint-cli2@0.23.2` 임시 설치 종료 코드 0. `ci-local.sh` 지문 `git hash-object` → `b15dcdf8f6d2bb1b9c5f152c949f8c29f70e61e1`.
Playwright 쓰임(`newContext` 의 `viewport` · `colorScheme`, `addStyleTag` 의 `content`)은 Context7 `/microsoft/playwright/v1.58.2` 문서와 맞춰 봤다.

```bash
# 떼기: awk '/^# === 측정 도우미 시작/{f=1} f{print} /^# === 측정 도우미 끝/{exit}' <계약> > "$TMPDIR/d1-measure.sh"
# 부르기: bash -c 'source "$TMPDIR/d1-measure.sh" || exit 2; type m >/dev/null || exit 2; m SK-01'
# 시작 판: E_REF=BASE 를 주고 부른다. 임시 복제본을 재려면 W=<복제본> BR=<가지> 를 준다
# === 측정 도우미 시작 (after-0924-docs-regen) ===
# 쓰는 법: 이 블록을 파일로 떼어 bash 에서 source 한 뒤 `m <조건 ID>`. zsh 에서 부르지 마라.
# 잴 트리 E — 기본은 가지 끝(TIP)을 git archive 로 푼 임시 폴더. 시작 판을 재려면 E_REF=BASE.
# 옛 판 EB — 늘 시작점(BASE = 39ddc12)을 푼 폴더. 원본은 늘 SRC_REF(= 39ddc12) 판을 읽는다.
W=${W:-/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak-docs}
BR=${BR:-chore/ak-docs}
BASE=$(git -C "$W" rev-parse --verify '39ddc12^{commit}') || { echo "UNRESOLVED BASE"; return 2 2>/dev/null || exit 2; }
SRC_FROM=$(git -C "$W" rev-parse --verify 'f81568d^{commit}') || { echo "UNRESOLVED SRC_FROM"; return 2 2>/dev/null || exit 2; }
SRC_REF=$BASE
TIP=$(git -C "$W" rev-parse --verify "$BR^{commit}") || { echo "UNRESOLVED TIP"; return 2 2>/dev/null || exit 2; }
T=$(mktemp -d "${TMPDIR:-/tmp}/d1.XXXXXX")
snap() { mkdir -p "$2" && git -C "$W" archive "$1" | tar -x -C "$2"; }
EB=$T/base; snap "$BASE" "$EB"
case "${E_REF:-TIP}" in
  BASE) E=$EB ;;
  *)    E=$T/tip; snap "$TIP" "$E" ;;
esac
[ -d "$W/node_modules/playwright-core" ] || (cd "$W" && npm ci >/dev/null 2>&1)
[ -d "$W/node_modules/playwright-core" ] || { echo "NO_PLAYWRIGHT"; return 2 2>/dev/null || exit 2; }
export NODE_PATH=$W/node_modules
CI_LOCAL=/Users/jackson/Hub/10_Dev/claude-plugins/.harness/handoff/2026-09-26-tools/ci-local.sh
TOOL_BLOB=b15dcdf8f6d2bb1b9c5f152c949f8c29f70e61e1
NOTES=.harness/.meta/after-kaizen-0926/d1-notes.md
# 원본:페이지:빼는 원본 줄(바뀐 줄 대조에서 뺀다 — 페이지가 그 자리를 옮겨 싣지 않는 곳)
PAIRS='bambu-kit/skills/bambu-print-profile/SKILL.md:docs/bambu-kit/bambu-print-profile.html:1600-1612
design-kit/references/visual-change-protocol.md:docs/design-kit/visual-change-protocol.html:
docs/tone/dart-flutter-idioms.md:docs/tone-kit/dart-flutter-idioms.html:
flutter-toolkit/references/flutter-ai-rules.md:docs/flutter-toolkit/flutter-ai-rules.html:
flutter-toolkit/references/project-detection.md:docs/flutter-toolkit/project-detection.html:
infra-kit/skills/infra-test/SKILL.md:docs/infra-kit/infra-test.html:
harness/docs/guides/plugin-validation-guide.md:docs/harness/plugin-validation.html:
.claude/skills/kaizen-orchestrator/SKILL.md:docs/process/kaizen-flow.html:only197
design-kit/skills/design-mockup/SKILL.md:docs/design-kit/design-mockup.html:
docs/api/contract/multi-sample-pagination-variance.md:docs/api-kit/multi-sample-pagination-variance.html:
design-kit/skills/design-concept/SKILL.md:docs/design-kit/design-concept.html:'
PAGES=$(printf '%s\n' "$PAIRS" | cut -d: -f2)
ALLOWED=$(printf '%s\n%s\n' "$PAGES" '.harness/sprint-contract-after-0924-docs-regen.md
.harness/sprint-feedback-after-0924-docs-regen.md
.harness/sprint-amendments-after-0924-docs-regen.md
.harness/.meta/after-kaizen-0926/d1-notes.md')
mkdir -p "$T/src"
while IFS=: read -r s p x; do
  mkdir -p "$T/src/$(dirname "$s")"
  git -C "$W" show "$SRC_REF:$s" > "$T/src/$s"
  git -C "$W" diff -U0 "$SRC_FROM" "$SRC_REF" -- "$s" > "$T/src/$s.diff"
done <<EOF
$PAIRS
EOF

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
    print(f'lines={len(L)} in_old={len(ino)} in_new={len(L)-len(miss)} lost={len(lost)} {lost[:3]}')
elif cmd == 'chg':  # 원본의 바뀐 줄이 페이지에 들었는지 — chg <원본> <diff -U0> <페이지> [빼는 줄 a-b,c | only<줄>]
    src, dif, page = sys.argv[2:5]; spec = sys.argv[5] if len(sys.argv) > 5 else ''
    K, TH = 8, 0.6
    def rng(t):
        out = set()
        for r in filter(None, t.split(',')):
            x, _, y = r.partition('-'); out.update(range(int(x), int(y or x) + 1))
        return out
    only = rng(spec[4:]) if spec.startswith('only') else None
    skip = set() if only is not None else rng(spec)
    def norm(s):
        s = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', s)
        s = s.replace('\\|', '|').replace('**', '').replace('`', '')
        s = re.sub(r'^\s*(?:[-*]\s|\d+\.\s|#+\s|>\s?)', '', s)
        return html.unescape(re.sub(r'\s+', '', s))
    sh = lambda s: {s[i:i + K] for i in range(max(1, len(s) - K + 1))}
    pt = text(rd(page), '')
    S = rd(src).splitlines(); kind = [None] * (len(S) + 2); f = fm = False
    for i, l in enumerate(S, 1):
        if i == 1 and l.strip() == '---': fm = True; kind[i] = 'fm'; continue
        if fm: kind[i] = 'fm'; fm = l.strip() != '---'; continue
        if re.match(r'^\s*(```|~~~)', l): f = not f; kind[i] = 'mark'; continue
        kind[i] = 'code' if f else 'prose'
    added = []; removed = set(); n = 0
    for l in rd(dif).splitlines():
        mm = re.match(r'^@@ -\S+ \+(\d+)(?:,(\d+))? @@', l)
        if mm: n = int(mm.group(1)); continue
        if l.startswith('+++') or l.startswith('---'): continue
        if l.startswith('+'): added.append((n, l[1:])); n += 1
        elif l.startswith('-'): removed |= sh(norm(l[1:]))
        elif l.startswith(' '): n += 1
    units = []; prev = None
    for n, l in added:
        k = kind[n] if n < len(kind) else 'prose'
        if (only is not None and n not in only) or n in skip or k in ('fm', 'mark') or not l.strip() \
           or re.fullmatch(r'\s*\|[\s|:-]+\|?\s*', l): prev = None; continue
        if k == 'code':
            if len(re.sub(r'\s+', '', l)) >= 8: units.append(['code', n, l.strip()])
            prev = None; continue
        if prev is not None and prev[3] == n - 1 and not re.match(r'\s*([-*]\s|\||\d+\.\s|#|>)', l):
            prev[2] += ' ' + l.strip(); prev[3] = n
        else:
            prev = ['prose', n, l.strip(), n]; units.append(prev)
    ok = tot = 0; miss = []
    for u in units:
        if u[0] == 'code':
            r = 1.0 if re.sub(r'\s+', '', u[2]) in pt else 0.0; good = r == 1.0
        else:
            nov = sh(norm(u[2])) - removed
            if not nov: continue
            r = sum(1 for x in nov if x in pt) / len(nov); good = r >= TH
        tot += 1; ok += good
        if not good: miss.append(f'{u[1]}:{r:.2f}')
    print(f'units_ok={ok}/{tot} miss={miss[:8]}')
elif cmd == 'cnt':  # 공백을 뺀 보이는 글에서 글 조각이 몇 번 나오는지 — cnt <페이지> <조각>...
    t = text(rd(sys.argv[2]), '')
    print(' '.join(f'[{x}]={t.count(re.sub(r"\s+", "", x))}' for x in sys.argv[3:]))
elif cmd == 'rcnt':  # 공백을 뺀 보이는 글에서 정규식이 몇 번 맞는지 — rcnt <페이지> <정규식>
    t = text(rd(sys.argv[2]), ''); print(f'n={len(re.findall(sys.argv[3], t))}')
elif cmd == 'cards':  # kaizen-flow 킷 카드(Phase 5~17)의 파일 표시가 원본 **범위:** 줄과 같은지
    L = rd(sys.argv[2]).splitlines(); want = {}
    for i, l in enumerate(L):
        mm = re.match(r'^### Step (\d+): Phase (\d+) — ', l)
        if not mm or int(mm.group(2)) < 5: continue
        for j in range(i + 1, min(i + 6, len(L))):
            if L[j].startswith('**범위:**'):
                ps = re.findall(r'`([^`]+)`', L[j])
                if j + 1 < len(L) and L[j + 1].startswith(', '): ps += re.findall(r'`([^`]+)`', L[j + 1])
                want[int(mm.group(2))] = ps; break
    h = rd(sys.argv[3]); got = {}
    for mm in re.finditer(r'<div class="phase-card" id="phase-(\d+)"', h):
        nx = h.find('<div class="phase-card"', mm.end())
        got[int(mm.group(1))] = [html.unescape(t).strip() for t in re.findall(r'<span class="file-tag">(.*?)</span>', h[mm.end(): nx if nx > 0 else len(h)], re.S)]
    eq = 0; bad = []
    for n in sorted(want):
        g = got.get(n)
        if g is not None and sorted(g) == sorted(want[n]): eq += 1
        else: bad.append(f'P{n}')
    print(f'phases={len(want)} cards_equal={eq}/{len(want)} bad={bad}')
elif cmd == 'exitrows':  # visual-change-protocol 종료 코드 표 — 1 행 excluded_surfaces 수, 2 행 status · UTF-8 수
    h = rd(sys.argv[2]); i = h.find('종료 코드 — 무엇이 어느 값으로'); j = h.find('<table', i); k = h.find('</table>', j)
    rows = {}
    for r in re.findall(r'(?is)<tr>(.*?)</tr>', h[j:k] if i >= 0 and j >= 0 else ''):
        c = re.findall(r'(?is)<t[dh][^>]*>(.*?)</t[dh]>', r)
        if c: rows[text(c[0]).strip()] = text(r)
    r1, r2 = rows.get('1', ''), rows.get('2', '')
    print(f'table={int(bool(rows))} row1_excl={r1.count("excluded_surfaces")} row2_status={r2.count("status")} row2_utf8={r2.count("UTF-8")}')
elif cmd == 'v8':  # plugin-validation V8 절 이름표 · 첫 요약 카드 제목에 「따옴표」
    h = rd(sys.argv[2])
    a = re.search(r'(?s)<div class="section" id="v8">.*?class="section-label">(.*?)</div>', h)
    b = re.search(r'(?s)<div class="v-badge">V8</div>\s*<div class="v-title">(.*?)</div>', h)
    print(f'label={int(bool(a) and "따옴표" in text(a.group(1)))} vtitle={int(bool(b) and "따옴표" in text(b.group(1)))}')
elif cmd == 'lead':  # design-concept 나쁜 예 코드 앞 공백 수
    mm = re.search(r'<pre><code>([ \t]*)\| Accent \| #E8965A \|', rd(sys.argv[2]))
    print(f'lead={len(mm.group(1)) if mm else "absent"}')
elif cmd == 'hdr':  # 원본 머리 설정의 판 · 날짜가 페이지 글에 붙어서(판 뒤 16 자 안에 날짜) — hdr <원본> <페이지>
    s = rd(sys.argv[2]); fm = re.match(r'(?s)^---\n(.*?)\n---', s)
    v = re.search(r'(?m)^version:\s*(\S+)', fm.group(1)) if fm else None
    d = re.search(r'(?m)^last_updated:\s*(\S+)', fm.group(1)) if fm else None
    t = text(rd(sys.argv[3]))
    if not (v and d): print('hdr=none')
    else: print(f'hdr={int(bool(re.search(re.escape("v" + v.group(1)) + r"[^0-9]{0,16}" + re.escape(d.group(1)), t)))} want=v{v.group(1)}·{d.group(1)}')
elif cmd == 'newver':  # 더해진 판 번호 꼴 가운데 옛 페이지 · 원본 어디에도 없는 것 — newver <원본> <옛 페이지> <새 페이지>
    rx = r'(?<![\w.])v?\d+\.\d+\.\d+(?![\w.])'
    s, old, new = rd(sys.argv[2]), text(rd(sys.argv[3])), text(rd(sys.argv[4]))
    have = set(re.findall(rx, s)) | set(re.findall(rx, old)) | {x.lstrip('v') for x in re.findall(rx, s)}
    bad = sorted({x for x in re.findall(rx, new) if x not in have and x.lstrip('v') not in have})
    print(f'newver_bad={len(bad)} {bad[:4]}')
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
    js = re.findall(r'(?is)<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>', h)
    for i, j in enumerate(js): open(f'{sys.argv[3]}.{i}.js', 'w', encoding='utf-8').write(j)
    print(f'tag_bad={p.bad + len(p.st)} css_bad={sum(1 for c in css if c.count("{") != c.count("}"))} js={len(js)}')
PY

cat > "$T/pw.js" <<'JS'
// 가로 넘침 — 페이지마다 375 · 1280 · 375+글자 간격 0.06em, 콘솔 · 페이지 오류 수. node pw.js <페이지>...
const path = require('path');
const { chromium } = require('playwright-core');
const OVER = () => document.documentElement.scrollWidth - document.documentElement.clientWidth;
(async () => {
  const b = await chromium.launch(); let bad = 0;
  for (const f of process.argv.slice(2)) {
    const v = {}; let errs = 0;
    for (const [k, w, ls] of [['w375', 375, 0], ['w1280', 1280, 0], ['ls375', 375, 1]]) {
      const ctx = await b.newContext({ viewport: { width: w, height: 900 }, colorScheme: 'dark' });
      const p = await ctx.newPage();
      p.on('console', m => m.type() === 'error' && errs++); p.on('pageerror', () => errs++);
      await p.goto('file://' + path.resolve(f));
      if (ls) { await p.addStyleTag({ content: '*{letter-spacing:0.06em !important}' }); await p.waitForTimeout(100); }
      v[k] = await p.evaluate(OVER); await ctx.close();
    }
    const good = v.w375 <= 2 && v.w1280 <= 2 && v.ls375 <= 2 && errs === 0; if (!good) bad++;
    console.log(`${good ? 'OK ' : 'BAD'} ${path.basename(f)} w375=${v.w375} w1280=${v.w1280} ls375=${v.ls375} err=${errs}`);
  }
  console.log(`bad=${bad}/${process.argv.length - 2}`);
  await b.close();
})().catch(e => { console.error(e); process.exit(2); });
JS

pair() { printf '%s\n' "$PAIRS" | awk -F: -v p="$1" '$2 == p'; }
src_of() { pair "$1" | cut -d: -f1; }
skip_of() { pair "$1" | cut -d: -f3; }
chg() { local p=$1 s; s=$(src_of "$p"); python3 "$T/pg.py" chg "$T/src/$s" "$T/src/$s.diff" "$E/$p" $(skip_of "$p"); }
cnt() { local p=$1; shift; python3 "$T/pg.py" cnt "$E/$p" "$@"; }
n() { grep -cF -- "$1" || true; }
m() {
  case "$1" in
  SK-01) p=docs/bambu-kit/bambu-print-profile.html; chg $p; python3 "$T/pg.py" rcnt "$E/$p" 'enum줄만빠진목록(?:09-25)?같음' ;;
  SK-02) p=docs/design-kit/visual-change-protocol.html; chg $p
    cnt $p '2 스키마 오류 / 3 대상 0 건'; python3 "$T/pg.py" exitrows "$E/$p" ;;
  SK-03) p=docs/tone-kit/dart-flutter-idioms.html; chg $p; cnt $p '\b(effective|resolved)[A-Z]' ;;
  SK-04) p=docs/flutter-toolkit/flutter-ai-rules.html; chg $p; cnt $p 'HAS_MAKEFILE = true 를 감지하면 make <target> 을 우선한다' ;;
  SK-05) p=docs/flutter-toolkit/project-detection.html; chg $p; cnt $p '# HAS_MAKEFILE — true 면 $MAKE <target> 우선' ;;
  SK-06) p=docs/infra-kit/infra-test.html; chg $p; cnt $p '# 없으면 해당 rule 만 [미검증]' 'VIOLATION을 오보하고 exit 1로 끝난다' ;;
  SK-07) p=docs/harness/plugin-validation.html; chg $p
    cnt $p '"command": "${CLAUDE_PLUGIN_ROOT}/scripts/run-guard.sh"' '"command": "${CLAUDE_PLUGIN_ROOT}/scripts/x.sh"'; python3 "$T/pg.py" v8 "$E/$p" ;;
  SK-08) p=docs/process/kaizen-flow.html; python3 "$T/pg.py" cards "$T/src/.claude/skills/kaizen-orchestrator/SKILL.md" "$E/$p"; chg $p ;;
  SK-09) p=docs/design-kit/design-mockup.html; chg $p; cnt $p '{이번 결정에서 버린 안·요소와 이유 — 없으면'
    echo "fen $(python3 "$T/pg.py" fen "$T/src/design-kit/skills/design-mockup/SKILL.md" "$E/$p" "$EB/$p")" ;;
  SK-10) p=docs/api-kit/multi-sample-pagination-variance.html
    cnt $p '{{total}}' '판정 불가' 'Hurl 문법으로 쓸 수 없다' '← 문법 없음'
    echo "h2_old=$(grep -c '<h2>경로 간 불변식은 Hurl 로 표현되지 않는다</h2>' "$E/$p" || true)" ;;
  SK-11) p=docs/design-kit/design-concept.html; python3 "$T/pg.py" lead "$E/$p"
    R=$([ "${E_REF:-TIP}" = BASE ] && echo "$BASE" || echo "$TIP"); echo "numstat=$(git -C "$W" diff --numstat "$BASE" "$R" -- $p | awk '{print $1"/"$2}')" ;;
  SK-12) printf '%s\n' "$PAIRS" | while IFS=: read -r s p x; do
      c=$(python3 "$T/pg.py" cov "$T/src/$s" "$E/$p" "$EB/$p"); f=$(python3 "$T/pg.py" fen "$T/src/$s" "$E/$p" "$EB/$p")
      echo "$(basename "$p") $(printf '%s' "$c" | grep -oE 'lost=[0-9]+ wr=[^ ]+ wr_ok=[01]') fen_$(printf '%s' "$f" | grep -oE 'lost=[0-9]+')"; done ;;
  SK-13) printf '%s\n' "$PAIRS" | while IFS=: read -r s p x; do
      echo "$(basename "$p") $(python3 "$T/pg.py" hdr "$T/src/$s" "$E/$p") $(python3 "$T/pg.py" newver "$T/src/$s" "$EB/$p" "$E/$p")"; done ;;
  ER-01) node "$T/pw.js" $(printf '%s\n' "$PAGES" | sed "s#^#$E/#") ;;
  ER-02) echo "hidden_added=$(git -C "$W" diff "$BASE" "$TIP" -- $PAGES | grep '^+' | grep -v '^+++' | grep -ciE 'overflow(-x)?[[:space:]]*:[[:space:]]*(hidden|clip)' || true)" ;;
  AR-01) git -C "$W" diff --name-only "$BASE" "$TIP" > "$T/changed.txt"
    extra=$(grep -vxF -f <(printf '%s\n' "$ALLOWED") "$T/changed.txt" | grep -c . || true)
    pages=$(grep -xF -f <(printf '%s\n' "$PAGES") "$T/changed.txt" | grep -c . || true)
    mp=0; mx=0
    for c in $(git -C "$W" rev-list --no-merges "$BASE..$TIP"); do
      f=$(git -C "$W" show --name-only --format= "$c"); d=$(printf '%s\n' "$f" | grep -c '^docs/' || true); h=$(printf '%s\n' "$f" | grep -c '^\.harness/' || true)
      [ "$d" -gt 1 ] && mp=$((mp+1)); [ "$d" -ge 1 ] && [ "$h" -ge 1 ] && mx=$((mx+1)); done
    echo "changed=$(grep -c . "$T/changed.txt") extra=$extra pages=$pages/11 multi_page=$mp mixed=$mx"
    grep -vxF -f <(printf '%s\n' "$ALLOWED") "$T/changed.txt" | head -5 ;;
  AR-02) b=$(git -C "$W" show "$TIP:$NOTES" 2>/dev/null); c=$([ -n "$b" ] && echo 1 || echo 0); out="committed=$c"
    for k in snapshot-sealing-canonicalization research-log reflect-digest adapter-contract adapter-dart-flutter locale-korean rust-kit/references/project-detection.md phase-research-templates dart-flutter-idioms tone-guide; do
      out="$out $k=$(printf '%s\n' "$b" | python3 -c 'import sys, re; k = sys.argv[1]; print(sum(1 for l in sys.stdin if k in l and len(re.findall(r"[가-힣]", l)) >= 15))' "$k")"; done; echo "$out" ;;
  AR-03) (cd "$E" && python3 scripts/check-docs-links.py > "$T/links.txt" 2>&1; echo "rc=$?")
    echo "broken0=$(n '깨진 링크 없음' < "$T/links.txt") nav=$(grep -oE '페이지 [0-9]+ · 등록 [0-9]+' "$T/links.txt")" ;;
  AP-01) v=$(find "$E" -path "$E/*/.claude-plugin/plugin.json" -type f -exec python3 -c 'import json,sys; [print(json.load(open(p))["version"]) for p in sys.argv[1:]]' {} + | LC_ALL=C sort -u)
    added=$(git -C "$W" diff "$BASE" "$TIP" -- $PAGES | grep '^+' | grep -v '^+++')
    k=0; for x in $v; do c=$(printf '%s\n' "$added" | grep -cE "(^|[^0-9.])v?${x//./\\.}([^0-9.]|\$)" || true); k=$((k+c)); done
    echo "versions=$(printf '%s\n' "$v" | grep -c .) hits=$k" ;;
  AP-03) b=$(git -C "$W" show "$TIP:$NOTES" 2>/dev/null)
    echo "committed=$([ -n "$b" ] && echo 1 || echo 0) bare=$(printf '%s\n' "$b" | awk '{s=$0; sub(/^[ \t]+/,"",s)} s ~ /^```/ { if (!inb) { h=substr(s,4); gsub(/[ \t]/,"",h); if (h=="") bare++; inb=1 } else inb=0 } END{print bare+0}')" ;;
  RE-01|RE-02)
    echo "added_files=$(git -C "$W" diff --diff-filter=A --name-only "$BASE" "$TIP" -- docs | grep -c . || true) ext_added=$(git -C "$W" diff "$BASE" "$TIP" -- $PAGES | grep '^+' | grep -v '^+++' | grep -ciE '<link[^>]+stylesheet|<script[^>]+src=|@import' || true)" ;;
  SC-00) echo "release_paths=$(git -C "$W" diff --name-only "$BASE" "$TIP" | grep -cE '^(scripts/|\.claude-plugin/)|/\.claude-plugin/' || true)" ;;
  DG-01|DG-03) echo "release_sh=$(git -C "$W" diff --name-only "$BASE" "$TIP" | grep -cx 'scripts/release.sh' || true)" ;;
  DG-02) jb=0; tb=0; cb=0
    for pg in $PAGES; do
      o=$(python3 "$T/pg.py" html "$E/$pg" "$T/js-$(basename "$pg")")
      tb=$((tb + $(printf '%s' "$o" | sed -E 's/.*tag_bad=([0-9]+).*/\1/')))
      [ "$(printf '%s' "$o" | sed -E 's/.*css_bad=([0-9]+).*/\1/')" -gt 0 ] && cb=$((cb+1))
    done
    for j in $(find "$T" -maxdepth 1 -name 'js-*.js' | LC_ALL=C sort); do node --check "$j" >/dev/null 2>&1 || jb=$((jb+1)); done
    MDL=${MDL:-$T/mdl}
    [ -x "$MDL/node_modules/.bin/markdownlint-cli2" ] || { mkdir -p "$MDL" && (cd "$MDL" && npm install --no-save --no-audit --no-fund markdownlint-cli2@0.23.2 >/dev/null 2>&1); }
    printf '{ "config": { "MD013": false } }\n' > "$MDL/cfg.markdownlint-cli2.jsonc"
    if [ ! -x "$MDL/node_modules/.bin/markdownlint-cli2" ]; then md=ENV_FAIL
    elif [ -f "$E/$NOTES" ]; then md=$( (cd "$(dirname "$E/$NOTES")" && "$MDL/node_modules/.bin/markdownlint-cli2" --config "$MDL/cfg.markdownlint-cli2.jsonc" "$(basename "$NOTES")" 2>&1) | grep -cE '^[^ ]+:[0-9]+' || true); else md=absent; fi
    echo "js_bad=$jb tag_bad=$tb css_bad=$cb md=$md" ;;
  DG-04) (cd "$E" && node scripts/check-docs-a11y.js $PAGES > "$T/a11y.txt" 2>&1; echo "rc=$?"); tail -1 "$T/a11y.txt" ;;
  DG-05) [ "$(git -C "$W" rev-parse HEAD)" = "$TIP" ] && [ -z "$(git -C "$W" status --porcelain --untracked-files=no)" ] || { echo "W_NOT_TIP"; return 2; }
    ts=$([ "$(git hash-object "$CI_LOCAL" 2>/dev/null)" = "$TOOL_BLOB" ] && echo 1 || echo 0)
    mkdir -p "$T/ci"; TMPDIR=$T/ci bash "$CI_LOCAL" "$W" > "$T/ci/run.log" 2>&1
    [ -f "$T/ci/ci-local/summary.txt" ] || { echo "tool_same=$ts ci_summary=absent"; return 2; }
    echo "tool_same=$ts rc0=$(grep -c 'rc=0' "$T/ci/ci-local/summary.txt") other=[$(grep -v 'rc=0' "$T/ci/ci-local/summary.txt" | tr '\n' ';')]" ;;
  *) echo "unknown $1"; return 2 ;;
  esac
}
# === 측정 도우미 끝 ===
```

봉인 전 실측 — 시작 판(`BASE` = `TIP` = `39ddc12`, 구현 전)에서 도우미로 잰 값과 대조 결과. 모의 좋은 판 · 나쁜 판은 세션 임시 폴더에서 W 를 `git clone --no-hardlinks` 해 만들었다.

- SK-01 ~ SK-13 · ER · AR · AP · RE · SC · DG 시작 판: 각 조건의 괄호 안 값 그대로
- 모의 좋은 판(열한 쪽을 쪽마다 한 커밋 — 바뀐 줄을 꾸밈 기호만 벗겨 페이지 끝 `<pre>` 에 붙이고, 옛 글을 지우고, 킷 카드 파일 표시를 원본에서 다시 만들고, 종료 코드 표 · V8 이름표 · 공백 세 칸을 고친 판, 그리고 열 토큰을 담은 notes 커밋): `units_ok` 가 `2/2` · `11/11` · `1/1` · `1/1` · `6/6` · `39/39` · `18/18` · `1/1` · `4/4`, 옛 글 수 모두 0, `row1_excl=2 row2_status=1 row2_utf8=1`, `label=1 vtitle=1`, `cards_equal=13/13`, `fen lines=21 in_new=21`, SK-10 `1 · 1 · 0 · 0 · h2_old=0`, SK-11 `lead=0 numstat=1/1`, SK-12 열한 줄 `lost=0 wr_ok=1 fen_lost=0`, SK-13 `hdr=1` 셋 · `newver_bad=0` 열한, ER-01 `bad=0/11`, DG-04 `rc=0 11/11 PASS`, AR-01 `changed=12 extra=0 pages=11/11 multi_page=0 mixed=0`, AR-02 `committed=1` 과 1 열, DG-02 `js_bad=0 tag_bad=0 css_bad=0 md=0` — 모든 기대값이 도달 가능하다
- 모의 좋은 판을 처음 만들 때 코드 줄의 백틱까지 벗겨 붙였더니 SK-06 `38/39`(`254:0.00`) · SK-09 `3/4`(`161:0.00`) 가 나왔다 — 코드 블록 줄은 글자 그대로(백틱 포함) 옮겨야 든 것으로 센다는 뜻이다. 모의 판을 고친 뒤 위 값
- `chg` 알려진 답: 옛 줄 「옛 문장은 그대로 둔다」 를 「… 그리고 덧붙임」 으로 바꾸고 문장 한 줄과 `bash` 코드 한 줄을 더한 작은 원본, 옛 줄과 문장 앞 절반만 든 페이지 → `units_ok=0/2 miss=['2:0.12', '5:0.00']` (두 줄이 한 문단 — 새 조각 17 개 가운데 2 개가 든다, 손셈 2/17 = 0.12), 다 든 페이지 → `units_ok=2/2`
- `cards` 알려진 답: 옛 원본(`f81568d`) · 시작 판 페이지 → `cards_equal=13/13`, 지금 원본 · 시작 판 페이지 → `cards_equal=1/13` (Phase 14 만 같다)
- 나쁜 판(`39ddc12` 위 한 커밋 — 페이지 셋 · `README.md` · `scripts/release.sh` · 새 `docs/x-new.html` · 언어 없는 fence 가 든 notes, bambu 에 `.x{overflow:hidden}`, kaizen-flow 에 `harness 0.14.1 · v9.9.9` 와 없는 링크, design-concept 에 외부 스타일 링크): AR-01 `changed=7 extra=3 pages=3/11 multi_page=1 mixed=1` + 세 경로, AR-02 `committed=1` 과 0 열, AR-03 `rc=1 broken0=0 nav=페이지 177 · 등록 176`, AP-01 `hits=1`, AP-03 `bare=1`, RE `added_files=1 ext_added=1`, SC-00 `release_paths=1`, DG-01 `release_sh=1`, ER-02 `hidden_added=1`, SK-11 `lead=3 numstat=1/0`, SK-13 kaizen-flow `newver_bad=2`
- 임시 페이지: 900px 폭 · 오류 스크립트 · 닫히지 않은 `div` · 깨진 중괄호 → ER-01 `BAD … w375=533 w1280=0 ls375=533 err=6`, DG-04 `0/1 PASS` 종료 코드 1, DG-02 `tag_bad=1 css_bad=1` · 두 스크립트 가운데 하나 `node --check` 종료 코드 1. 고정폭 글자 36 개 한 줄 → `w375=0 w1280=0 ls375=5` 로 `BAD`. `#bad heading` md → 경고 2
- SK-13 머리 음성: plugin-validation 머리를 `v1.4.0 · 2026-09-25` 로 바꾼 사본 → `hdr=0` (판 번호와 날짜가 떨어진 자리 — 제목의 `v1.4.1` · 변경 이력의 `2026-09-26` — 는 세지 않는다)
- DG-05 시작 판: `tool_same=1 rc0=22 other=[feedback-agg-test SKIP (yq 없음);]` (`ci-local.sh` 종료 코드 0)
- 교차 진단 반영 뒤 다시 잰 값(바뀐 도우미 세 곳 — AR-02 한글 15 자 줄 · DG-02 설치 실패 · DG-05 요약 없음): 토큰마다 한글 설명 줄을 담은 모의 notes → AR-02 `committed=1` 과 1 열 · AP-03 `bare=0` · DG-02 `md=0`, 열 토큰을 한 줄에 늘어놓은 앞선 모의 notes → `committed=1` 과 0 열, 토큰 없는 notes → `committed=1` 과 0 열, 시작 판 → `committed=0` 과 0 열, 닿지 않는 저장소 주소 → DG-02 `md=ENV_FAIL`, 도구 경로를 없는 파일로 바꿔 부름 → DG-05 `tool_same=0 ci_summary=absent` · 종료 코드 2. AP-03 의 awk 와 V6 의 같은 셈 대조는 AP-03 조건에 적은 열 가지 입력으로 잰 값이다
- 계약에서 뗀 도우미가 작성 원본과 바이트까지 같다(`cmp` 종료 코드 0). 뗀 도우미로 시작 판 · 모의 좋은 판 · 나쁜 판을 다시 재어 위 값과 모두 같았다(DG-05 는 작성 원본 도우미로 잰 값)

## 리서치 소스

- 저장소 안: 핸드오프 `.harness/handoff/2026-09-26-0110.md` §C3 · §운영 요령(본 체크아웃), `.harness/.meta/after-kaizen-0926/c3b-notes.md` 「다음 사이클 메모」 1 · 2 번, `.harness/.meta/after-kaizen-0926/c4d-notes.md` 「넘긴 것과 사유」 · R4, `.harness/sprint-contract-after-0924-docs-site.md`(같은 꼴의 측정 도우미), `.claude/skills/docs-site/SKILL.md` Step 1 표 · Gotcha 10 ~ 12
- 원본 차이: `git diff f81568d..39ddc12` — 원본 열 개와 `docs/superpowers/specs/2026-09-02-api-kit-design.md:249-262` · `docs/api/research-log.md:161-176`
- 측정 도구 원본: `/Users/jackson/Hub/10_Dev/claude-plugins/.harness/handoff/2026-09-26-tools/` 의 `coverage.py` · `fence2.py` · `ci-local.sh` (도우미의 `cov` · `fen` 은 앞 둘을 옛 판을 파일로 받게 옮긴 사본)
- 라이브러리 문서: Context7 `/microsoft/playwright/v1.58.2` (`newContext` 옵션 · `addStyleTag`)
- 메모리: 「다시 만든 페이지는 옛 판 대비 담김으로 재라」 · 「CI 리눅스는 내 맥보다 화면을 더 나쁘게 그린다」 · 「고친 자리 말고 옛 값이 남았는지 확인」
- 저장소 밖 원문은 쓰지 않았다
