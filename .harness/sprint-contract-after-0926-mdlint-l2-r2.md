---
feature: "기존 마크다운 경고 정리 — docs 폴더 (docs/superpowers 제외) (l2) 2 회차 계약"
slug: after-0926-mdlint-l2-r2
created: "2026-09-27 15:58"
complexity: "중간"
conditions: 17
status: active
owner_session: bda55d45-296c-491f-89ba-b52042d58e72
conditions_digest: sha256:c16f3b07525aa783
measurement_digest: sha256:d84bf8a11583d1ae
locked_at: "2026-09-27 16:04"
---

## 배경

- **2 회차 계약이다.** 1 회차 계약 `.harness/sprint-contract-after-0926-mdlint-l2.md`(봉인 커밋 `c768d5d`, 조건 16, 지금 `status: superseded` — 커밋 `3272ab4`)를 대신한다. 1 회차 마지막 QA 판정은 `.harness/sprint-feedback-after-0926-mdlint-l2.md`(커밋 `12d8e8f`, REJECT 12/16)에 있다.
- 바꾼 까닭: 1 회차 ER-01 · AR-03 은 「걸린 줄 바로 앞 한 줄짜리 끄기 주석만」 허용한다. 그런데 `docs/bambu-calibration/calibration-reference.md` 4.2 절 표의 셋째 줄 칸 안 `<br>`(MD033)은 한 줄 끄기를 넣을 자리가 없다. 주석 줄을 표 안에 넣으면 표가 거기서 끊겨 그려진다(1 회차 교차 진단이 끊긴 표를 결함으로 짚었고, 커밋 `3ad40cc` 가 표 앞뒤 감싸기로 고쳤다). `<br>` 을 지우면 한 칸 안의 두 선택지가 한 줄로 붙어 뜻이 바뀐다(AR-03).
- 그래서 이 계약은 예외 하나를 조건 문장에 적는다: **표 안 칸에서 걸리는 규칙 하나를, 표 바로 앞 끄기 줄 · 표 바로 뒤 켜기 줄 한 쌍으로 끄고, 두 줄에 그 규칙 이름 하나만 적은 것.** 「바로 앞」 은 끄기 줄 다음 줄이 표 머리 줄이라는 뜻이고, 「바로 뒤」 는 표의 마지막 `|` 줄 뒤 빈 줄만 건너 처음 나오는 줄이 켜기 줄이라는 뜻이다. 이 예외는 이 파일 이 자리 하나에만 쓴다 — 새 조건 ER-02 가 그것을 잰다.
- 나머지 조건은 1 회차와 같은 뜻으로 옮겼다. 바뀐 것은 셋이다. (1) ER-01 · AR-03 이 위 예외 한 쌍을 「넓은 끄기」 로 세지 않는다. (2) AR-02 의 `.harness/` 허용 파일에 1 회차 계약 · 피드백 · 개정 파일을 더했다 — 1 회차 기록이 이 가지에 이미 있다. (3) 측정 도우미의 시작점은 1 회차 봉인 커밋의 부모(`7a7ecb4`)다 — 구현이 1 회차 봉인 뒤에 시작했기 때문이다.
- 이 계약은 1 회차 조건을 느슨하게 만든다(표 감싸기 한 쌍을 허용). 동의 처리 길은 결정 파일 `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0926b/.harness/.meta/after-kaizen-0926b/decisions.md`(읽기만) 「추가 위임 (2026-09-27)」 절이 정한 대로다 — 느슨하게 하는 개정은 위임으로 동의 처리하지 않고, 조건 문장을 새로 써서 다시 봉인한다. 위임 발언: 세션 `bda55d45-296c-491f-89ba-b52042d58e72` 의 2026-09-26T10:09:00.557Z · 10:30:16.222Z 「전부 고친다」, 2026-09-27T01:22:01.089Z 「자동으로 다 진행해 나한테 묻지 말고 …」. 결정 UD-7 「범위 밖 기존 markdownlint 경고를 전부 고친다」 가운데 `docs/` 폴더 묶음(l2)이다. `docs/superpowers/` 는 다른 묶음이다.
- 봉인 순서: 구현 커밋(`cf0b38b` ~ `905009b`)은 1 회차 봉인 커밋 `c768d5d` 뒤에 있다. 이 2 회차 계약의 봉인 커밋은 구현 뒤에 온다 — 새 판이라 피할 수 없다. 범위 구간의 아래 끝은 1 회차 봉인 커밋의 부모이고, 측정 도우미가 1 회차 계약 경로로 git 기록에서 푼다.
- 작업 폴더 W = `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak2-l2`, 가지 `chore/ak2-l2`(`chore/after-kaizen-0926b` `c3e45f3` 에서 갈라짐). 첫 커밋 `7a7ecb4` 가 목록 파일을 담았다.
- 대상 목록: `.harness/.meta/after-kaizen-0926b/l2-files.txt`(커밋 `7a7ecb4`, 123 줄) — W 에서 `git ls-files '*.md' | grep '^docs/' | grep -v '^docs/superpowers/'` 의 결과다. 시험이 여는 파일이 0 개라 뺄 파일이 없다(`## GAP 분석`).
- 측정 도구: `/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/bda55d45-296c-491f-89ba-b52042d58e72/scratchpad/mdlint/run.sh <트리> <목록>` — markdownlint-cli2 0.23.2 · MD013 끔(편집기 확장 기본값).
- 커밋 규칙: `git add <경로>` 뒤 `git commit -o <경로>` · 한 커밋에 맨 위 폴더 하나(`docs` 와 `.harness` 를 섞지 않는다) · `git add -A` · `git stash` · push · 가지 바꾸기 금지. 본 체크아웃 · 다른 워크트리 · 통합 폴더는 건드리지 않는다.
- 뜻을 바꾸지 않는다. 표 · 목록 · 빈 줄 · 코드 블록 언어 · 제목 표식 · URL 꺾쇠 같은 모양만 고친다. 규칙을 지키면 뜻이 깨지는 자리는 그 자리에만 `<!-- markdownlint-disable-next-line 규칙 -->` 을 넣고 이유를 notes 에 적는다. 위 표 감싸기 한 쌍만 예외다. 파일 전체를 끄는 주석은 쓰지 않는다.
- 기록 파일(notes): `.harness/.meta/after-kaizen-0926b/l2-notes.md` (W 안, 이 가지에 커밋). 지금 notes 의 「표 안 줄바꿈 태그」 절은 「계약 개정 판단을 부모에게 넘겼다」 로 끝난다. 구현자는 이 절에 이 2 회차 계약 슬러그 `after-0926-mdlint-l2-r2` 를 적어 그 예외가 이 계약으로 허용됐음을 밝힌다(ER-02 `r2_cite`). notes 는 새로 쓰는 문장이라 `tone-kit:tone-guide` 1 단계(규칙 불러오기)와 5 단계(전수 대조)를 거친다.
- 사용자가 할 일: 없음.

공통 전제 G (조건마다 되풀이하지 않는다) — 구현 · notes 커밋이 가지 `chore/ak2-l2` 에 모두 들어간 뒤, 가지를 합치기 전에 잰다.
측정은 `## 회귀 게이트` 의 측정 도우미 `m <조건 ID>` 로 한다. 도우미는 끝점 `TIP`(가지 끝)과 시작점 `BASE`(1 회차 봉인 커밋의 부모)를 `git archive` 로 풀어 잰다 — 작업 폴더의 커밋 안 된 변경은 보지 않는다(SC-01 · DG-04 만 작업 폴더를 쓰고, 작업 폴더가 `TIP` 과 다르면 `W_NOT_TIP` 을 찍고 멈춘다).
`HEAD` 를 상한으로 쓰지 않는다. `BASE` · `TIP` 해석이 안 되면 도우미가 `UNRESOLVED` 를 찍고 멈춘다.
경고를 재는 조건은 매번 먼저 도구 확인(`mdl_ok` — 판 `v0.23.2`, 설정에 `"MD013": false`, 맨 URL 한 줄짜리 시험 파일에서 MD034 1 건 이상)을 돌리고, 실패하면 `md=ENV_FAIL` 을 찍는다. 그 칸은 `[미검증:ENV]` 로 적고 PASS 로 읽지 않는다.

복잡도 4 축 — 둘이 「예」 라 「중간」 이다.

| 축 | 물음 | 값 |
| -- | ---- | -- |
| 레이어 수 | 몇 개 계층을 관통하는가 | 하나 — 문서 원본(마크다운) |
| 공개 API·계약 변경 | 외부에 노출된 약속이 바뀌는가 | 아니오 — 글의 뜻 · 머리 설정 · 파일 경로가 그대로다(AR-03 · AP-04 · AR-02) |
| 소비면 존재 | 반대편이 있는가 | 예 — 원본을 읽는 스크립트(`scripts/validate-post-kaizen.py` · `scripts/detect-docs-drift.py`)와 원본에서 만든 문서 사이트 HTML |
| 회귀 위험 | 기존 동작이 깨질 수 있는가 | 예 — 116 파일을 모양만 고치다 낱말 · 표 칸 · 머리 설정이 바뀔 수 있고, 표 감싸기 한 쌍이 다른 자리로 번질 수 있다 |

Step 2.5 짝 조건: 만드는 쪽은 목록 123 파일(AR-01 · AR-03)이다. 쓰는 쪽은 위 스크립트 둘과 CI 검사 묶음이다 — 쓰는 쪽 파일은 고치지 않고, 스크립트가 찾는 글(날짜)과 경로가 그대로임을 AR-03(낱말 순서 같음) · AR-02(경로 바뀜 없음)로 재고 검사 묶음 통과를 SC-01 · DG-04 로 잰다. 문서 사이트 HTML 은 뜻이 같아 다시 만들 일이 없다 — `detect-docs-drift.py` 가 이 원본들을 바뀐 것으로 고를 수 있다는 사실만 notes 에 적어 부모에게 넘긴다(AR-05 토큰 `detect-docs-drift`).

기능 조건 8 개는 SC-01 · ER-01 · ER-02 · AR-01 ~ AR-05 다 — Step 6.2 두 번째 명령이 `## Anti-patterns` 절(AP-03 · AP-04) · 자동 포함 여섯 줄(RE-01 · RE-02 · DG-01 ~ DG-04) · `N/A (` 줄(SK-00)을 빼고 센 값이다.

설정 값 대조 (`.harness/project.yaml` 을 글자 그대로 옮김):

| config key | project.yaml 에서 읽은 값 | 계약에 쓴 값 |
| ---------- | ------------------------- | ------------ |
| `commands.analyze` | `bash -n scripts/release.sh` | DG-01 N/A — 재는 파일이 바뀐 파일에 없다 |
| `commands.test` | `bash scripts/release.sh 2>&1 \|\| true` | DG-03 N/A — 같은 이유 |
| `diagnostics.ide_exclude` | `[]` | DG-02 의 `([] 제외)` |
| `contract_categories[].id` / `prefix` | Skill/SK · Script/SC · Error/ER · Architecture/AR | 같은 넷 |
| `anti_patterns[].id` / `message` | AP-01 버전 하드코딩 · AP-02 force push · AP-03 bare code fence · AP-04 frontmatter name 누락 | AP-03 · AP-04. AP-01 은 더하는 글이 없어서(모양만 고친다), AP-02 는 이 계약이 push 하지 않아서 뺐다 |

## GAP 분석 (Pre-Edit Audit)

2 회차 봉인 전 실측(이 기계, 2026-09-27 15:40 ~ 15:58, 가지 끝 `3272ab4`, 도우미는 아래 `## 회귀 게이트` 블록 그대로):

| 대상 | 실제 Read 증거 | 발견 | 조건화 |
| --- | --- | --- | --- |
| 1 회차 마지막 판정 | `.harness/sprint-feedback-after-0926-mdlint-l2.md:47-57` · `:69-71` | REJECT 12/16. FAIL 넷(AR-03 · AR-05 · ER-01 · DG-02) 가운데 MD038 줄 끝 끄기 5 곳은 `5c3706e` 가 한 줄 끄기로 바꿨고, notes MD038 3 건은 `905009b` 가 고쳤다. 남은 것은 표 감싸기 한 쌍뿐이다 | ER-01 · ER-02 · AR-03 |
| `docs/bambu-calibration/calibration-reference.md:113-124` | `### 4.2 Preset 화면에서 정하는 것` 아래 115 줄 `<!-- markdownlint-disable MD033 -->`, 116 ~ 122 줄 표(머리 · 구분 · 다섯 줄), 123 빈 줄, 124 줄 `<!-- markdownlint-enable MD033 -->`. 118 줄 칸 안에 `<br>` | 1 회차 도우미로 재면 이 두 줄이 `wide_disable=2` · `word_diff=1` 이다. 2 회차 도우미로 재면 한 쌍으로 인정돼 `pairs=1 wide_disable=0` 이다 | ER-02 |
| 1 회차 도우미로 잰 가지 끝 | 1 회차 계약 `## 회귀 게이트` 블록을 떼어 `3272ab4` 에서 `m` | `AR-01 warn=0` · `AR-02 extra=0 harness_extra=0 seal_broken=0` · `AR-03 word_diff=1 wide_disable=2` · `ER-01 comments=272 useless=0 wide_disable=2` · `AR-05 rows_match=6/6 rows_extra=0` · `AP-03 md040=32->0 notes_bare=0` · `AP-04 fm_changed=0` · `DG-02 notes_warn=0 list_warn=0` · `AR-04 impl_commits=4 multi_top=0` | 표 감싸기 한 쌍 말고는 1 회차 조건을 모두 채운다 |
| 목록 123 파일 시작 판 | `E_REF=BASE m AR-01` → `warn=2417` | 규칙별 `MD060:962 MD034:599 MD032:258 MD022:214 MD024:164 MD025:86 MD031:35 MD036:33 MD040:32 MD012:16 MD038:5 MD033:4 MD028:4 MD010:2 MD058:1 MD041:1 MD004:1` | AR-01 |
| notes `.harness/.meta/after-kaizen-0926b/l2-notes.md:44-46` | 「표 안 줄바꿈 태그」 절 | 자리 설명 줄(`calibration-reference.md` · `MD033`)은 있고, 끝 문장은 「계약 개정 판단을 부모에게 넘겼다」 다. 이 계약 슬러그를 적은 줄은 0 이다(`r2_cite=0`) | ER-02 |
| 원본을 읽는 스크립트 | `scripts/validate-post-kaizen.py:317-356` · `scripts/detect-docs-drift.py:96` | 날짜 글과 경로만 본다. 제목 단계 · 주석 줄을 읽는 곳은 없다(1 회차 GAP 그대로) | AR-03 · AR-02 · SC-01 |
| CI 검사 묶음 | `m SC-01` · `m DG-04` (가지 끝) | 모두 통과. `ci-local.sh` 는 마지막 명령이 `grep -v 'rc=0' summary.txt` 라 이 기계에서는 `feedback-agg-test SKIP (yq 없음)` 줄이 있어 종료 코드 0 이다 | SC-01 · DG-04 |

## Skill

- [ ] SK-00: N/A (스킬 파일을 바꾸지 않는다 — 바뀌는 파일은 목록의 `docs/` 마크다운과 `.harness/` 기록뿐이다. `docs/howto/drafts/SKILL.md` 는 킷 밖 초안이라 스킬로 불리지 않는다. 측정: `m AR-02` 가 `extra=0`)

## Script

- [ ] SC-01: 원본을 읽는 스크립트와 레포 검사가 끝점에서 모두 통과한다 — Given 공통 전제 G 와 작업 폴더 W 가 `TIP` 과 같음, When `m SC-01` 이 W 에서 `python3 scripts/validate-plugin.py` · `python3 scripts/sync-docs.py --check-only` · `python3 scripts/sync-orchestrator.py --check-only` · `python3 scripts/sync-evals.py --check-only` · `python3 scripts/run-evals.py` · `python3 scripts/run-kaizen-assertions.py` · `python3 scripts/check-reviewer-protocol-copies.py` · `python3 scripts/check-cause-table-copies.py` · `python3 scripts/detect-docs-drift.py --check-table` · `bash harness/evals/measure/measure-helpers-test.sh` 를 차례로 돌리면, Then 열 칸 모두 `=0` [exact, enumerated]
  측정: `m SC-01`. 2 회차 봉인 전 가지 끝(`3272ab4`) `rc: validate-plugin.py=0 sync-docs.py=0 sync-orchestrator.py=0 sync-evals.py=0 run-evals.py=0 run-kaizen-assertions.py=0 check-reviewer-protocol-copies.py=0 check-cause-table-copies.py=0 detect-docs-drift.py=0 measure-helpers-test.sh=0`
  양성 대조: 1 회차 봉인 전 실측 — 복제본에서 `harness/skills/sprint-contract/SKILL.md` 의 `name:` 을 `nme:` 로 바꾼 판 → `validate-plugin.py=2 sync-docs.py=1`. 작업 폴더에 커밋 안 된 변경이 있는 판 → `W_NOT_TIP`. 이 판정 줄은 2 회차 도우미에서 바뀌지 않았다

## Error

- [ ] ER-01: 끄는 주석은 실제로 걸리는 줄 바로 앞에만, 한 줄짜리로만 넣는다. 예외: ER-02 가 정한 표 감싸기 한 쌍(표 바로 앞 `<!-- markdownlint-disable MDxxx -->` · 표 바로 뒤 `<!-- markdownlint-enable MDxxx -->`, 두 줄에 같은 규칙 하나)은 넓은 끄기로 세지 않는다 — Given 공통 전제 G, When `m ER-01` 이 바뀐 목록 파일에서 새로 들어간 한 줄짜리 끄기 주석 줄과 표 감싸기 쌍 줄을 지운 사본을 같은 도구로 재면, Then 한 줄짜리 주석마다 적힌 규칙 모두가 그 주석 다음 줄에 경고로 1 건 이상 나오고(`useless=0`), 파일 전체 · 구간을 끄는 주석(`markdownlint-disable` · `enable` · `capture` · `restore` · `configure-file` · `disable-line` 등 `-next-line` 아닌 것) 가운데 표 감싸기 쌍이 아닌 것을 새로 넣은 줄이 0 이다(`wide_disable=0`) [exact]
  측정: `m ER-01`. 시작 판 `comments=0 useless=0 wide_disable=0`, 2 회차 봉인 전 가지 끝 `comments=272 useless=0 wide_disable=0`(1 회차 도우미는 같은 판에서 `wide_disable=2`)
  양성 대조: 복제본 나쁜 판 셋(2 회차 봉인 전 실측) — `bad1` 켜기 줄을 표 뒤 4.3 절 제목 아래로 옮김 → `wide_disable=2`, `bad2` 끄기 줄에 규칙 둘(`MD033 MD034`) → `wide_disable=2`, `bad3` 끄기 줄과 표 머리 사이에 빈 줄 → `wide_disable=2`. 1 회차 나쁜 판(보통 글 줄 앞 `MD024` 주석 · 파일 머리 `<!-- markdownlint-disable MD034 -->`) → `useless=1 wide_disable=1` 은 판정 줄이 같아 그대로다
- [ ] ER-02: 표 감싸기 한 쌍은 딱 한 자리 — `docs/bambu-calibration/calibration-reference.md` 의 `### 4.2` 절 표 — 에만 있고, 그 표 안에서 실제로 걸리는 규칙 하나(MD033)만 끄며, notes 에 이 계약으로 허용됐다고 적혀 있다 — Given 공통 전제 G, When `m ER-02` 가 바뀐 목록 파일마다 새로 들어간 줄에서 「끄기 줄 다음 줄이 표 머리이고, `|` 로 시작하는 줄이 3 줄 이상 이어진 뒤 빈 줄만 건너 처음 나오는 줄이 새로 들어간 같은 규칙의 켜기 줄」 인 쌍을 세고, 쌍 줄과 한 줄짜리 주석을 지운 사본을 같은 도구로 재어 감싼 표 줄 안의 그 규칙 경고 수를 세고, 끝점 notes 를 읽으면, Then `pairs=1 pair_useless=0 wide_disable=0` 이고 `pair_at` 이 `docs/bambu-calibration/calibration-reference.md:<줄>:MD033:hits=<1 이상>:head=[### 4.2 …]` 한 항목이며(줄 번호는 보지 않는다), `pair_note` 가 1 이상(notes 에 `docs/bambu-calibration/calibration-reference.md` 와 `MD033` 이 함께 든 한글 15 자 이상 줄)이고 `r2_cite` 가 1 이상(notes 에 `after-0926-mdlint-l2-r2` 가 든 한글 15 자 이상 줄)이다 [exact]
  측정: `m ER-02`. 시작 판 `pairs=0 pair_useless=0 wide_disable=0 pair_at=` · `pair_note=absent r2_cite=absent`, 2 회차 봉인 전 가지 끝 `pairs=1 pair_useless=0 wide_disable=0 pair_at=docs/bambu-calibration/calibration-reference.md:115:MD033:hits=1:head=[### 4.2 Preset 화면에서 정하는 것 **[설치본 UI]**]` · `pair_note=1 r2_cite=0`(notes 에 슬러그를 아직 안 적었다 — 구현자가 적을 몫), 복제본 좋은 판(notes 끝에 슬러그 든 한 줄을 더함) `pair_note=1 r2_cite=1`
  양성 대조: 복제본 나쁜 판(2 회차 봉인 전 실측) — `bad1`(켜기 줄 옮김 + `docs/howto/branch-catalog.md` 의 경고 없는 표를 MD033 쌍으로 감쌈) → `pairs=1 pair_useless=1 wide_disable=2 pair_at=docs/howto/branch-catalog.md:15:MD033:hits=0:head=[## 1. 무엇이 틀렸나]`, `bad2` → `pairs=0 wide_disable=2 pair_at=`, `bad3` → `pairs=0 wide_disable=2 pair_at=`
  알려진 답: 쌍 판정(도우미 `pairs_of`)에 손으로 만든 다섯 입력 — 바른 쌍 / 끄기 줄과 표 사이 빈 줄 / 켜기 규칙이 다름(`MD034`) / 표가 두 줄 / 켜기 줄이 새로 든 줄이 아님 — 의 기대 `1 0 0 0 0`, 2 회차 봉인 전 실제 `1 0 0 0 0` · 종료 코드 0

## Architecture

- [ ] AR-01: 목록 파일의 편집기 경고가 0 건이다 (a) — Given 공통 전제 G, When `m AR-01` 이 끝점 트리에서 `run.sh <끝점 트리> <끝점 트리>/.harness/.meta/after-kaizen-0926b/l2-files.txt` 를 돌리면, Then `ver=v0.23.2 list_n=123 list_same=1 warn=0` 이다(목록 파일이 시작 판과 같고 123 줄) [exact]
  측정: `m AR-01`. 시작 판 `ver=v0.23.2 list_n=123 list_same=1 warn=2417`(규칙별 줄은 `## GAP 분석`), 2 회차 봉인 전 가지 끝 `ver=v0.23.2 list_n=123 list_same=1 warn=0`
  양성 대조: 시작 판 자체가 `warn=2417` 이다 (봉인 전 실측). 도구가 안 돌면 `md=ENV_FAIL` 이 먼저 찍혀 0 으로 읽히지 않는다
- [ ] AR-02: 고치지 않는 파일은 한 줄도 안 바뀐다 (b) — Given 공통 전제 G, When `m AR-02` 가 `git diff --name-status -M BASE TIP` 을 읽으면, Then `.harness/` 밖 바뀐 경로가 모두 목록 파일 안이고(`extra=0`), `docs/` 안 변경은 모두 수정이며(추가 · 삭제 · 이름 바꿈 0, `docs_not_modify=0`), `.harness/` 안 바뀐 경로는 1 회차 · 2 회차 계약, 두 슬러그의 피드백 · 개정 파일, notes — 이 일곱 가운데 것뿐이고(`harness_extra=0` — 목록 파일 `l2-files.txt` 도 바뀌면 안 된다), 목록에 시험 입력 경로(`evals/` 와 `fixture` 가 함께 든 경로)가 0 이며(`guard_in_list=0`), 끝점 트리의 `sprint-contract*.md` 가운데 봉인이 있는 것 모두 `SEAL_BROKEN` 이 0 이다(`seal_broken=0`) [exact, collective]
  측정: `m AR-02`. 시작 판 `changed_paths=0 extra=0 harness_extra=0 docs_not_modify=0 guard_in_list=0 sealed=106 seal_broken=0`, 2 회차 봉인 전 가지 끝 `changed_paths=119 extra=0 harness_extra=0 docs_not_modify=0 guard_in_list=0 sealed=107 seal_broken=0`
  양성 대조: 1 회차 봉인 전 실측 — 나쁜 판(`scripts/newcheck.py` 추가 · 앞 계약 `sprint-contract-after-0926-guides.md` 조건 줄 한 글자 · `docs/howto/branch-catalog.md` 삭제) → `extra=1 harness_extra=1 docs_not_modify=1 seal_broken=1`. 2 회차 도우미는 허용 목록에 1 회차 파일 셋만 더했고 판정 줄은 같다
- [ ] AR-03: 뜻이 안 바뀐다 (c) — 바뀐 목록 파일마다 시작 판과 끝점 판을 같은 식으로 줄인 글이 같다. 줄이는 식(도우미 `norm`): 한 줄짜리 끄기 주석 줄과 규칙 하나만 적은 disable · enable 줄을 지우고, 코드 울타리 여는 줄은 울타리 글자만 남기고(언어 이름 뗌), 모든 공백 · 줄바꿈과 표식 글자 `#` `|` `-` `:` `<` `>` `*` `_` `` ` `` `+` `~` `\` 를 뗀 뒤 이어 붙인다 — 남은 낱말의 순서가 같으면 바뀐 것은 공백 · 빈 줄 · 표 구분 · 코드 블록 언어 · 제목 표식 · URL 꺾쇠 · 좁힌 끄기 주석뿐이다. 지운 disable · enable 줄이 ER-02 의 표 감싸기 쌍이 아니면 `wide_disable` 에 센다. Given 공통 전제 G, When `m AR-03`, Then `word_diff=0 wide_disable=0` 이고 `changed` 와 `word_same` 이 같다 [exact]
  측정: `m AR-03`. 시작 판 `changed=0 word_same=0 word_diff=0 wide_disable=0 nl_added=0 pairs=0`, 2 회차 봉인 전 가지 끝 `changed=116 word_same=116 word_diff=0 wide_disable=0 nl_added=272 pairs=1`(1 회차 도우미는 같은 판에서 `word_same=115 word_diff=1 wide_disable=2`)
  알려진 답: 손으로 고른 여덟 쌍(표 칸 공백 · 구분 줄 넓히기 + URL 꺾쇠 / 울타리에 `text` 달기 / 끄기 주석 + `#`→`##` / `**굵은 제목**`→`#### 굵은 제목` / 「foo bar」→「bar foo」 / 「1.2」→「1.3」 / `x<br>y`→`x y` / 표를 MD033 disable · enable 쌍으로 감싸기)의 기대 `1 1 1 1 0 0 0 1`, 2 회차 봉인 전 실제 `1 1 1 1 0 0 0 1` · 종료 코드 0
  양성 대조: 복제본 나쁜 판(2 회차 봉인 전 실측) `bad2`(끄기 줄에 규칙 둘) → `word_diff=1 wide_disable=2`, `bad1` · `bad3` → `wide_disable=2`. 1 회차 나쁜 판(`docs/howto/deep-links.md` 낱말 하나 바꿈 · 머리 설정 `version` 바꿈 · 파일 전체 끄기 주석) → `word_diff=3 wide_disable=1` 은 판정 줄이 같아 그대로다
- [ ] AR-04: 커밋이 맨 위 폴더 둘을 섞지 않는다 — Given 공통 전제 G, When `m AR-04` 가 `BASE..TIP` 의 병합 아닌 커밋마다 담긴 경로의 맨 위 폴더 수를 세면, Then `multi_top=0` 이고 `docs/` 를 담은 커밋 `impl_commits` 가 1 이상이다 [exact]
  측정: `m AR-04`. 시작 판 `impl_commits=0 multi_top=0`, 2 회차 봉인 전 가지 끝 `impl_commits=4 multi_top=0`
  양성 대조: 1 회차 봉인 전 실측 — 나쁜 판(`docs` · `scripts` · `.harness` 를 한 커밋에) → `multi_top=1`
- [ ] AR-05: 좁힌 끄기 주석 수와 이유가 notes 에 있다 (e) — Given 공통 전제 G, When `m AR-05` 가 끝점 notes `.harness/.meta/after-kaizen-0926b/l2-notes.md` 의 `## 좁힌 끄기` 로 시작하는 절에서 `| MDxxx | 수 | 이유 |` 행을 읽고, 바뀐 목록 파일에 새로 들어간 한 줄짜리 끄기 주석을 규칙별로 센 값(`want`)과 맞대면, Then `committed=1 section=1` 이고 `rows_match` · `reason_ok` 가 모두 `k/k`(k 는 `want` 의 규칙 수, 이유 칸 한글 10 자 이상)이며 `rows_extra=0` 이고, `tone-guide` 가 한글 15 자 이상인 줄에 1 번 이상 든다(`tone=1` 이상). 같은 notes 에 `detect-docs-drift` 가 한글 15 자 이상인 줄에 1 번 이상 든다(`drift=1` 이상) [exact]
  측정: `m AR-05`. 시작 판 `committed=0 notes=absent`, 2 회차 봉인 전 가지 끝 `committed=1 section=1 want=[MD024:164 MD025:86 MD028:4 MD036:12 MD038:5 MD041:1] rows_match=6/6 reason_ok=6/6 rows_extra=0 tone=1 drift=1`
  양성 대조: 1 회차 봉인 전 실측 — 나쁜 notes(MD028 수를 4 에서 3 으로) + 쓸모없는 MD024 주석 1 줄 → `rows_match=1/3`. 평가자는 셈이 잡은 줄마다 그 줄이 실제로 그 규칙을 끈 까닭을 설명하는지 한 번 눈으로 읽는다 — 이유 칸이 빈말이면 그 행은 0 으로 본다

## Anti-patterns

- [ ] AP-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수 (```text, ```bash, ```yaml 등). 판정 권위는 validate-plugin V6 상태기계다 — 여는/닫는 fence 가 동형이라 줄 단위 정규식으로는 판정 불가
  이 계약에 적용: 목록 파일의 MD040 과 notes. V6 는 킷 폴더만 읽어 `docs/` 와 `.harness/` 를 보지 않으므로 목록은 markdownlint MD040 으로, notes 는 도우미가 V6 와 같은 셈으로 잰다. 측정: `m AP-03` 이 `md040=32->0 notes_bare=0` (시작 판 `md040=32->32 notes_bare=absent`, 2 회차 봉인 전 가지 끝 `md040=32->0 notes_bare=0`)
  양성 대조: 1 회차 봉인 전 실측 — 나쁜 notes(언어 없는 울타리) → `notes_bare=1`
- [ ] AP-04: SKILL.md / agents/*.md frontmatter 에서 name 필드 누락 — validate-plugin V1 FAIL
  이 계약에 적용: 바뀐 목록 파일의 머리 설정 블록이 시작 판과 글자까지 같고, `docs/howto/drafts/SKILL.md` 의 `name` 이 그대로다. 측정: `m AP-04` 가 `fm_changed=0 drafts_name=howto` (시작 판 · 2 회차 봉인 전 가지 끝 같은 값)
  양성 대조: 1 회차 봉인 전 실측 — 나쁜 판(`contract-extraction-modes.md` 의 `version: 0.1.1` → `0.1.2`) → `fm_changed=1`

## Reusability

- [ ] RE-01: 다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다
  이 계약에 적용: 산출물에 재사용 단위 코드가 없다(바뀌는 파일은 마크다운과 기록 파일뿐). 측정: `m AR-02` 가 `extra=0 harness_extra=0` — 코드 파일이 들어오면 `extra` 가 1 이상이 된다
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다
  이 계약에 적용: 새 검사 도구를 레포에 만들지 않고 공통 전제의 측정 도구(`run.sh` · `cfg.jsonc`)를 그대로 쓴다. 측정: `m AR-02` 가 `extra=0` (1 회차 나쁜 판 `scripts/newcheck.py` → `extra=1`)

## Diagnostics

- [ ] DG-01: N/A (commands.analyze `bash -n scripts/release.sh` 가 재는 `scripts/release.sh` 는 이번 바뀐 파일에 없다. 측정: `m DG-01` 이 `release_paths=0`)
- [ ] DG-02: IDE diagnostics 워닝/인포 0개 ([] 제외)
  편집기 진단을 명령줄로 같게 잰다(계약 · QA 리포트 · 개정 파일은 뺀다): 목록 파일 경고 0(AR-01 과 같은 셈)과 notes 경고 0. `<!-- AUTO:* -->` 블록 안 경고는 0 이다 — 목록의 `AUTO:` 글은 모두 코드 울타리 안 예시이거나 설명 글이라 생성기가 쓰는 블록이 없다. 측정: `m DG-02` 가 `notes_warn=0 list_warn=0` (시작 판 `notes_warn=absent list_warn=2417`, 2 회차 봉인 전 가지 끝 `notes_warn=0 list_warn=0`)
  양성 대조: 1 회차 판정(`12d8e8f`)이 잡은 notes 49 줄 MD038 3 건 → `notes_warn=3`
- [ ] DG-03: N/A (commands.test `bash scripts/release.sh 2>&1 || true` 가 재는 `scripts/release.sh` 는 이번 바뀐 파일에 없다. 측정: DG-01 과 같은 `m DG-01` 이 `release_paths=0`)
- [ ] DG-04: 실제 앱/서버 구동 시 에러 0개
  이 계약에 적용: 구동할 앱 · 서버 대신 CI 단계를 로컬에서 전부 돌린다 (d). Given 작업 폴더 W 가 `TIP` 과 같음(아니면 `W_NOT_TIP`), When `m DG-04` 가 `/Users/jackson/Hub/10_Dev/claude-plugins/.harness/handoff/2026-09-26-tools/ci-local.sh` 를 W 에 돌리면(`TMPDIR` 은 도우미 임시 폴더), Then `tool_same=1 ci_rc=0 rc0=25 other=[feedback-agg-test SKIP (yq 없음);]` 이다 — 종료 코드 0 과 함께 25 단계가 모두 `rc=0` 이고 그 밖의 줄은 yq 없음 건너뜀 한 줄뿐이다 [exact]
  측정: `m DG-04`. 도구 파일은 이 가지 밖에 있어 도우미가 그 내용 지문(`git hash-object`)을 봉인 전 값 `01528e5a5c0dfe27a6a9c0bb8ae1c830f2f04860` 과 대조한다. 2 회차 봉인 전 가지 끝 `tool_same=1 ci_rc=0 rc0=25 other=[feedback-agg-test SKIP (yq 없음);]`. `tool_same=0` 이거나 요약 파일이 없으면(`ci_summary=absent`) 그 회차는 `[미검증:ENV]` 로 적는다
  음성 대조: 이 도구의 종료 코드만 보면 안 된다 — 마지막 명령이 `grep -v 'rc=0'` 이라 yq 가 깔린 기계에서 모두 통과하면 종료 코드가 1 이 되고, 한 단계가 실패하면 그 줄이 잡혀 0 이 된다. 그래서 `rc0=25` 와 `other` 칸을 함께 본다. 같은 검사가 실패하면 종료 코드가 0 이 아님은 SC-01 양성 대조(`validate-plugin.py=2`)가 보였다

## 범위 경계

```text
# sprint-scope
docs/*.md
```

- 위 블록은 커밋 직전 훅이 쓰는 굵은 울타리다. 정확한 허용 집합은 목록 파일 `l2-files.txt` 이고 AR-02 가 그것으로 잰다.
- 이 계약 봉인 뒤 남은 구현은 notes 한 곳이다 — 「표 안 줄바꿈 태그」 절에 이 계약 슬러그를 적는다(ER-02 `r2_cite`). 목록 파일은 더 고칠 것이 없다.
- 봉인 전 교차 진단(2026-09-27)의 지적 둘: (1) 문서 페이지 짝 목록 · 담김 · 넘침 물음은 페이지를 다시 만드는 다른 묶음의 것이라 이 계약에 대응하는 조건이 없다 — 조건을 바꾸지 않았다. (2) notes 슬러그는 봉인 뒤 구현 커밋으로 채운다 — 위 줄 그대로다.
- 표 감싸기 한 쌍의 허용은 이 계약의 ER-02 가 정한 한 자리뿐이다. 다른 파일 · 다른 표 · 다른 규칙에 같은 모양을 쓰면 ER-01 · AR-03 `wide_disable` 이나 ER-02 `pairs` · `pair_at` 에 걸린다.
- `.harness/` 아래는 봉인된 계약 기록이라 고치지 않는다 — 1 회차 계약의 머리 설정 `status` 한 줄(`3272ab4`)만 바꿨고 조건 줄은 그대로다(`AR-02 seal_broken=0`). 목록 파일은 `7a7ecb4` 에서 고정한다.
- `docs/superpowers/` · 킷 폴더 · `scripts/` · 레포 맨 위 문서는 다른 묶음이다.
- 제목 단계 · 앵커는 1 회차 범위 경계 그대로다 — 앵커(`#슬러그`) 깨짐은 어느 조건도 재지 않고(`scripts/check-docs-links.py` 가 `#` 링크를 건너뛴다), 구현자가 notes 「제목 단계를 바꾼 자리」 에 손으로 찾은 결과(0 건)를 적었다.
- 표가 끊기지 않았는지는 ER-02 의 쌍 판정이 구조로 잰다 — 끄기 줄 다음 줄부터 `|` 줄이 끊김 없이 이어져야 쌍으로 인정한다. 1 회차 교차 진단이 짚은 「주석 줄이 표 안에 들어가 표가 끊김」 은 이 판정에서 표 줄 수가 3 미만이 되거나 켜기 줄을 못 찾아 `pairs=0` 이 된다.

커버리지 해소 — Step 6.5 (4) 검출기가 낸 `UNCOVERED` 와 목록을 한 곳에만 둔 조건:

- 해소할 것 없음 — 2026-09-27 2 회차 봉인 전 6.5 (4) 검출기 출력 0 줄(종료 코드 0). `enumerated` 조건은 SC-01 하나이고, 열 검사 이름이 산문과 측정 줄에 같은 글자로 있다
- 오라클 해소: DG-04 — `m DG-04` 는 `ci-local.sh` 를 실제로 돌려 요약 파일의 `rc=` 줄을 센다. 글을 찾는 검사가 아니다

## 회귀 게이트 — 측정 도우미 · 봉인 전 실측

평가 때 이 블록을 떼어 bash 에서 불러 쓴다. `TMPDIR` 은 평가자 임시 폴더로 준다. 도우미는 `$T` 아래에만 쓴다 — 작업 폴더와 측정 도구 폴더는 지우지 마라.

준비 단계 실측(2 회차 봉인 전, 이 기계): 측정 도구 폴더의 `markdownlint-cli2 --help` 첫 줄 `markdownlint-cli2 v0.23.2 (markdownlint v0.41.1)`, `cfg.jsonc` 내용 `{ "config": { "MD013": false } }`, `ci-local.sh` 지문 `01528e5a5c0dfe27a6a9c0bb8ae1c830f2f04860`(`m DG-04` 의 `tool_same=1`).
봉인 전 실측은 가지 끝 `3272ab4` 의 값, `E_REF=BASE` 로 잰 시작 판 값, 임시 복제본(`W=<복제본>`)에 나쁜 판 `bad1` · `bad2` · `bad3` 과 좋은 판 `good` 을 커밋해 `BR=<가지>` 로 잰 값이다. 1 회차 계약에만 적힌 양성 대조는 그 판정 줄이 2 회차 도우미에서 바뀌지 않은 조건에만 옮겨 적었다.
도우미는 zsh 에서 부르지 마라 — zsh 는 따옴표 없는 변수를 낱말로 나누지 않는다.
2 회차 도우미가 1 회차 도우미와 다른 곳: 머리 변수(`SLUG` · `R1_SLUG` · `R1_CF_REL` · `PAIR_FILE`), 시작점을 1 회차 계약 경로로 푸는 줄, 파이썬 `PAIR` · `pairs_of` · `heading_before` 와 그것을 쓰는 `norm` · 넓은 끄기 셈 · 사본 만들기, `AR-02` 의 허용 목록, 새 `ER-02` 분기.

```bash
# 떼기: awk '/^# === 측정 도우미 시작/{f=1} f{print} /^# === 측정 도우미 끝/{exit}' <계약> > "$TMPDIR/l2r2-measure.sh"
# 부르기: bash -c 'source "$TMPDIR/l2r2-measure.sh" || exit 2; type m >/dev/null || exit 2; m ER-02'
# === 측정 도우미 시작 (after-0926-mdlint-l2-r2) ===
# 쓰는 법: 이 블록을 파일로 떼어 bash 에서 source 한 뒤 `m <조건 ID>`. zsh 에서 부르지 마라(따옴표 없는 변수를 낱말로 나누지 않는다).
# 끝점 TIP = 가지 끝. 시작점 BASE = 1 회차 계약을 처음 담은 커밋(1 회차 봉인 커밋)의 부모 — 해시를 박지 않고 git 기록에서 푼다.
# 구현은 1 회차 봉인 뒤에 시작했으므로 2 회차도 같은 시작점에서 잰다. 시작 판 자체를 재려면 E_REF=BASE. 임시 복제본을 재려면 W=<복제본>.
W=${W:-/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak2-l2}
BR=${BR:-chore/ak2-l2}
SLUG=after-0926-mdlint-l2-r2
R1_SLUG=after-0926-mdlint-l2
CF_REL=.harness/sprint-contract-$SLUG.md
R1_CF_REL=.harness/sprint-contract-$R1_SLUG.md
PAIR_FILE=docs/bambu-calibration/calibration-reference.md
LIST_REL=.harness/.meta/after-kaizen-0926b/l2-files.txt
NOTES_REL=.harness/.meta/after-kaizen-0926b/l2-notes.md
MDL=${MDL:-/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/bda55d45-296c-491f-89ba-b52042d58e72/scratchpad/mdlint}
CILOCAL=/Users/jackson/Hub/10_Dev/claude-plugins/.harness/handoff/2026-09-26-tools/ci-local.sh
CILOCAL_BLOB=01528e5a5c0dfe27a6a9c0bb8ae1c830f2f04860
TIP=$(git -C "$W" rev-parse --verify -q "$BR^{commit}") || { echo "UNRESOLVED TIP"; return 2 2>/dev/null || exit 2; }
if [ -n "${BASE_REF:-}" ]; then
  BASE=$(git -C "$W" rev-parse --verify -q "$BASE_REF^{commit}") || { echo "UNRESOLVED BASE_REF"; return 2 2>/dev/null || exit 2; }
else
  SEAL=$(git -C "$W" log --diff-filter=A --format=%H "$TIP" -- "$R1_CF_REL" | tail -1)
  [ -n "$SEAL" ] || { echo "UNRESOLVED SEAL (봉인 커밋 없음)"; return 2 2>/dev/null || exit 2; }
  BASE=$(git -C "$W" rev-parse --verify -q "$SEAL^") || { echo "UNRESOLVED BASE"; return 2 2>/dev/null || exit 2; }
fi
if [ "${E_REF:-TIP}" = BASE ]; then END=$BASE; else END=$TIP; fi
T=$(mktemp -d "${TMPDIR:-/tmp}/l2.XXXXXX")
snap() { mkdir -p "$2" && git -C "$W" archive "$1" | tar -x -C "$2"; }
EB=$T/base; snap "$BASE" "$EB"
EE=$T/end;  snap "$END" "$EE"
echo "BASE=$BASE END=$END"

mdl_ok() {  # 도구가 실제로 경고를 내는지 매번 확인한다 — 못 돌면 0 건이 거짓 통과가 된다
  printf '# t\n\nhttp://example.com\n' > "$T/probe.md"
  VER=$("$MDL/node_modules/.bin/markdownlint-cli2" --help 2>&1 | head -1 | grep -oE 'v[0-9]+\.[0-9]+\.[0-9]+' | head -1)
  n=$("$MDL/node_modules/.bin/markdownlint-cli2" --config "$MDL/cfg.jsonc" "$T/probe.md" 2>&1 | grep -c 'MD034')
  [ "$n" -ge 1 ] && [ "$VER" = v0.23.2 ] && grep -q '"MD013": false' "$MDL/cfg.jsonc"
}
lint_list() {  # lint_list <트리> → 목록 파일 경고 줄 (목록은 그 트리의 것을 쓴다)
  bash "$MDL/run.sh" "$1" "$1/$LIST_REL"
}
changed_list() {  # BASE..END 에서 바뀐(M) 목록 파일
  git -C "$W" diff --name-only --diff-filter=M "$BASE" "$END" -- docs | grep -Fxf "$EB/$LIST_REL"
}

py_meaning() {  # 뜻 비교 · 끄기 주석 분석 — 파이썬 한 곳. 바뀐 목록 파일은 $T/cl 로 넘긴다(표준 입력은 이 스크립트가 쓴다)
  changed_list > "$T/cl"
  python3 - "$EB" "$EE" "$T" "$MDL" "$@" <<'PY'
import os, re, subprocess, sys, collections
eb, ee, t, mdl, mode = sys.argv[1:6]
files = [l.strip() for l in open(os.path.join(t, 'cl'), encoding='utf-8') if l.strip()]
NL = re.compile(r'^\s*<!--\s*markdownlint-disable-next-line((?:\s+MD\d{3})+)\s*-->\s*$')
WIDE = re.compile(r'markdownlint-(disable|enable|capture|restore|configure-file|disable-file|enable-file|disable-line)(?!-next-line)')
# 표 감싸기 한 쌍 — 규칙 하나만 적은 disable · enable 줄. 자리가 맞는지는 pairs_of 가 본다
PAIR = re.compile(r'^\s*<!--\s*markdownlint-(disable|enable)\s+(MD\d{3})\s*-->\s*$')
FENCE = re.compile(r'^(\s*)(`{3,}|~{3,})[^`]*$')
DROP = set(' \t\r\n#|-:<>*_`+~\\')
def norm(text):
    out = []
    for line in text.split('\n'):
        if NL.match(line) or PAIR.match(line):
            continue
        m = FENCE.match(line)
        if m:
            line = m.group(2)
        out.append(''.join(c for c in line if c not in DROP))
    return ''.join(out)
def added(old, new):
    c = collections.Counter(old.split('\n'))
    res = []
    for i, line in enumerate(new.split('\n')):
        if c[line] > 0:
            c[line] -= 1
        else:
            res.append((i, line))
    return res
def pairs_of(lines, add_idx):
    # 새로 들어간 disable 줄 i 바로 다음 줄이 표 머리(| 로 시작)이고, | 줄이 3 줄 이상 이어진 뒤
    # 빈 줄만 건너 처음 나오는 줄이 새로 들어간 같은 규칙의 enable 줄이면 한 쌍이다.
    # 돌려주는 값: [(disable 줄 번호, enable 줄 번호, 규칙, 표 첫 줄, 표 끝 줄)] — 모두 0 부터
    res = []
    for i in sorted(add_idx):
        m = PAIR.match(lines[i])
        if not m or m.group(1) != 'disable':
            continue
        rule = m.group(2); j = i + 1
        while j < len(lines) and lines[j].lstrip().startswith('|'):
            j += 1
        if j - (i + 1) < 3:
            continue
        k = j
        while k < len(lines) and not lines[k].strip():
            k += 1
        if k < len(lines) and k in add_idx:
            me = PAIR.match(lines[k])
            if me and me.group(1) == 'enable' and me.group(2) == rule:
                res.append((i, k, rule, i + 1, j - 1))
    return res
def heading_before(lines, i):
    for x in range(i - 1, -1, -1):
        if re.match(r'^#{1,6}\s', lines[x]):
            return lines[x].strip()
    return ''
same = diff = wide = 0; nl = collections.Counter(); nl_total = 0; bad = []
comments = []  # (file, index-in-new, rules)
pairs = []     # (file, dis, en, rule, t0, t1, heading)
for f in files:
    old = open(os.path.join(eb, f), encoding='utf-8').read()
    new = open(os.path.join(ee, f), encoding='utf-8').read()
    if norm(old) == norm(new): same += 1
    else: diff += 1; bad.append(f)
    nlines = new.split('\n')
    add = added(old, new)
    ps = pairs_of(nlines, {i for i, _ in add})
    pair_idx = {p[0] for p in ps} | {p[1] for p in ps}
    for p in ps:
        pairs.append((f,) + p + (heading_before(nlines, p[0]),))
    for i, line in add:
        m = NL.match(line)
        if m:
            rules = m.group(1).split(); comments.append((f, i, rules)); nl_total += 1
            for r in rules: nl[r] += 1
        elif i in pair_idx:
            continue
        elif WIDE.search(line):
            wide += 1; bad.append(f + ':wide:' + str(i + 1))
if mode == 'AR-03':
    print(f"changed={len(files)} word_same={same} word_diff={diff} wide_disable={wide} nl_added={nl_total} pairs={len(pairs)}")
    if bad: print("BAD " + ' '.join(bad[:20]))
    sys.exit(0)
if mode == 'rules':
    print(' '.join(f"{r}:{n}" for r, n in sorted(nl.items()))); sys.exit(0)
if mode in ('ER-01', 'ER-02'):
    # 끄기 주석(한 줄짜리 · 표 감싸기 쌍 모두)을 지운 사본을 재서, 한 줄짜리는 바로 다음 줄에,
    # 표 감싸기 쌍은 감싼 표 줄 안에 그 규칙 경고가 1 건 이상 있는지 본다
    sd = os.path.join(t, 'strip'); useless = 0; lst = []
    bymap = {}; pmap = {}
    for f in files:
        new = open(os.path.join(ee, f), encoding='utf-8').read().split('\n')
        mine = [c for c in comments if c[0] == f]
        mp = [p for p in pairs if p[0] == f]
        drop = {i for _, i, _ in mine} | {p[1] for p in mp} | {p[2] for p in mp}
        kept = []; newidx = {}
        for i, line in enumerate(new):
            if i in drop: continue
            newidx[i] = len(kept); kept.append(line)
        p = os.path.join(sd, f); os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, 'w', encoding='utf-8').write('\n'.join(kept)); lst.append(f)
        for _, i, rules in mine:
            nxt = i + 1
            while nxt in drop: nxt += 1
            bymap.setdefault(f, []).append((newidx.get(nxt, -1) + 1, rules))
        for q in mp:
            pmap.setdefault(f, []).append((newidx[q[4]] + 1, newidx[q[5]] + 1, q[3], q[1] + 1, q[6]))
    warns = collections.defaultdict(set)
    if lst:
        out = subprocess.run([os.path.join(mdl, 'node_modules/.bin/markdownlint-cli2'), '--config', os.path.join(mdl, 'cfg.jsonc')] + lst,
                             cwd=sd, capture_output=True, text=True)
        for line in (out.stdout + out.stderr).split('\n'):
            m = re.match(r'^(\S+?):(\d+)(?::\d+)? \S+ (MD\d{3})', line)
            if m: warns[(m.group(1), int(m.group(2)))].add(m.group(3))
    ul = []
    for f, items in bymap.items():
        for ln, rules in items:
            hit = warns.get((f, ln), set())
            for r in rules:
                if r not in hit: useless += 1; ul.append(f"{f}:{ln}:{r}")
    if mode == 'ER-01':
        print(f"comments={nl_total} useless={useless} wide_disable={wide}")
        if ul: print("USELESS " + ' '.join(ul[:20]))
        sys.exit(0)
    # ER-02: 표 감싸기 쌍의 수 · 자리 · 쓸모
    pu = 0; at = []
    for f, items in pmap.items():
        for a, b, rule, dis_ln, head in items:
            n = sum(1 for ln in range(a, b + 1) if rule in warns.get((f, ln), set()))
            if n == 0: pu += 1
            at.append(f"{f}:{dis_ln}:{rule}:hits={n}:head=[{head}]")
    print(f"pairs={len(pairs)} pair_useless={pu} wide_disable={wide} pair_at={';'.join(at)}")
PY
}

m() {
  case "$1" in
  AR-01)
    mdl_ok || { echo "md=ENV_FAIL"; return; }
    if [ -f "$EE/$LIST_REL" ]; then same=$(cmp -s "$EB/$LIST_REL" "$EE/$LIST_REL" && echo 1 || echo 0); else same=absent; fi
    n=$(grep -c . "$EE/$LIST_REL")
    w=$(lint_list "$EE" | grep -c .)
    echo "ver=$VER list_n=$n list_same=$same warn=$w"
    lint_list "$EE" | grep -oE 'MD[0-9]{3}' | sort | uniq -c | sort -rn | awk '{printf "%s:%s ", $2, $1} END{print ""}'
    ;;
  AR-02)
    git -C "$W" diff --name-status -M "$BASE" "$END" > "$T/ns"
    awk -F'\t' '{print $2; if (NF>=3) print $3}' "$T/ns" | sort -u > "$T/paths"
    printf '%s\n' "$CF_REL" ".harness/sprint-feedback-$SLUG.md" ".harness/sprint-amendments-$SLUG.md" \
      "$R1_CF_REL" ".harness/sprint-feedback-$R1_SLUG.md" ".harness/sprint-amendments-$R1_SLUG.md" "$NOTES_REL" > "$T/hallow"
    extra=$(grep -v '^\.harness/' "$T/paths" | grep -vFxf "$EB/$LIST_REL" | tee "$T/extra" | grep -c .)
    hx=$(grep '^\.harness/' "$T/paths" | grep -vFxf "$T/hallow" | tee "$T/hextra" | grep -c .)
    nm=$(awk -F'\t' '$1!="M" && ($2 ~ /^docs\// || $3 ~ /^docs\//)' "$T/ns" | grep -c .)
    guard=$(grep -E 'evals/' "$EB/$LIST_REL" | grep -c 'fixture')
    sb=0; sn=0
    for c in $(find "$EE/.harness" -maxdepth 1 -type f -name 'sprint-contract*.md' | sort); do
      rec=$(awk 'NR==1&&/^---/{f=1;next} f&&/^---/{exit} f&&/^conditions_digest:/{sub(/^conditions_digest:[ \t]*/,"");print}' "$c" | tr -d "\"'"); rec=${rec#sha256:}
      [ -z "$rec" ] && continue
      act=$(grep -E '^- \[[ x]\] [A-Z]{2,}-[0-9]{2}' "$c" | sed -E 's/^- \[[ x]\]/- [ ]/' | shasum -a 256 | cut -c1-16)
      sn=$((sn+1)); [ "$rec" = "$act" ] || { sb=$((sb+1)); echo "SEAL_BROKEN ${c#$EE/}"; }
    done
    echo "changed_paths=$(grep -c . "$T/paths") extra=$extra harness_extra=$hx docs_not_modify=$nm guard_in_list=$guard sealed=$sn seal_broken=$sb"
    [ "$extra" -gt 0 ] && echo "EXTRA $(tr '\n' ' ' < "$T/extra")"
    [ "$hx" -gt 0 ] && echo "HEXTRA $(tr '\n' ' ' < "$T/hextra")"
    ;;
  AR-03) py_meaning AR-03 ;;
  AR-04)
    ic=0; mt=0
    for c in $(git -C "$W" rev-list --no-merges "$BASE..$END"); do
      tops=$(git -C "$W" show --name-only --format='' "$c" | awk -F/ 'NF{print $1}' | sort -u | grep -c .)
      git -C "$W" show --name-only --format='' "$c" | grep -q '^docs/' && ic=$((ic+1))
      [ "$tops" -ge 2 ] && { mt=$((mt+1)); echo "MULTI $c"; }
    done
    echo "impl_commits=$ic multi_top=$mt"
    ;;
  AR-05)
    [ -f "$EE/$NOTES_REL" ] && com=1 || { echo "committed=0 notes=absent"; return; }
    rules=$(py_meaning rules)
    python3 - "$EE/$NOTES_REL" "$rules" <<'PY'
import re, sys
text = open(sys.argv[1], encoding='utf-8').read()
want = dict(x.split(':') for x in sys.argv[2].split()) if sys.argv[2].strip() else {}
sec = re.search(r'^## 좁힌 끄기[^\n]*\n(.*?)(?=^## |\Z)', text, re.S | re.M)
rows = {}
if sec:
    for line in sec.group(1).split('\n'):
        m = re.match(r'^\|\s*`?(MD\d{3})`?\s*\|\s*(\d+)\s*\|(.*)\|\s*$', line)
        if m: rows[m.group(1)] = (m.group(2), m.group(3))
hang = lambda s: len(re.findall(r'[가-힣]', s))
match = sum(1 for r, n in want.items() if r in rows and rows[r][0] == n)
reason = sum(1 for r in want if r in rows and hang(rows[r][1]) >= 10)
extra = sum(1 for r in rows if r not in want)
tone = sum(1 for l in text.split('\n') if 'tone-guide' in l and hang(l) >= 15)
drift = sum(1 for l in text.split('\n') if 'detect-docs-drift' in l and hang(l) >= 15)
print(f"committed=1 section={1 if sec else 0} want=[{sys.argv[2].strip()}] rows_match={match}/{len(want)} reason_ok={reason}/{len(want)} rows_extra={extra} tone={tone} drift={drift}")
PY
    ;;
  ER-01)
    mdl_ok || { echo "md=ENV_FAIL"; return; }
    py_meaning ER-01
    ;;
  ER-02)
    mdl_ok || { echo "md=ENV_FAIL"; return; }
    py_meaning ER-02
    if [ -f "$EE/$NOTES_REL" ]; then
      python3 - "$EE/$NOTES_REL" "$PAIR_FILE" "$SLUG" <<'PY'
import re, sys
text = open(sys.argv[1], encoding='utf-8').read().split('\n')
hang = lambda s: len(re.findall(r'[가-힣]', s))
pn = sum(1 for l in text if sys.argv[2] in l and 'MD033' in l and hang(l) >= 15)
rc = sum(1 for l in text if sys.argv[3] in l and hang(l) >= 15)
print(f"pair_note={pn} r2_cite={rc}")
PY
    else echo "pair_note=absent r2_cite=absent"; fi
    ;;
  AP-03)
    mdl_ok || { echo "md=ENV_FAIL"; return; }
    b=$(lint_list "$EB" | grep -c 'MD040'); e=$(lint_list "$EE" | grep -c 'MD040')
    if [ -f "$EE/$NOTES_REL" ]; then nb=$(awk '{s=$0; sub(/^[ \t]+/,"",s)} s ~ /^```/ {if(!o){o=1; if(s ~ /^```[ \t]*$/) b++} else o=0} END{print b+0}' "$EE/$NOTES_REL"); else nb=absent; fi
    echo "md040=$b->$e notes_bare=$nb"
    ;;
  AP-04)
    fc=0
    for f in $(changed_list); do
      a=$(awk 'NR==1&&!/^---/{exit} NR==1{print;next} {print} /^---/{exit}' "$EB/$f" | shasum | cut -c1-12)
      b=$(awk 'NR==1&&!/^---/{exit} NR==1{print;next} {print} /^---/{exit}' "$EE/$f" | shasum | cut -c1-12)
      [ "$a" = "$b" ] || { fc=$((fc+1)); echo "FM_CHANGED $f"; }
    done
    nm=$(awk 'NR==1&&/^---/{f=1;next} f&&/^---/{exit} f&&/^name:/{sub(/^name:[ \t]*/,"");print}' "$EE/docs/howto/drafts/SKILL.md")
    echo "fm_changed=$fc drafts_name=$nm"
    ;;
  DG-01)
    echo "release_paths=$(git -C "$W" diff --name-only "$BASE" "$END" | grep -cx 'scripts/release.sh')"
    ;;
  DG-02)
    mdl_ok || { echo "md=ENV_FAIL"; return; }
    if [ -f "$EE/$NOTES_REL" ]; then nw=$( (cd "$EE" && "$MDL/node_modules/.bin/markdownlint-cli2" --config "$MDL/cfg.jsonc" "$NOTES_REL" 2>&1) | grep -cE '^[^ ]+:[0-9]+'); else nw=absent; fi
    w=$(lint_list "$EE" | grep -c .)
    echo "notes_warn=$nw list_warn=$w"
    ;;
  SC-01|DG-04)
    h=$(git -C "$W" rev-parse HEAD); d=$(git -C "$W" status --porcelain --untracked-files=no | grep -c .)
    [ "$h" = "$END" ] && [ "$d" = 0 ] || { echo "W_NOT_TIP head=$h dirty=$d"; return; }
    if [ "$1" = SC-01 ]; then
      out=""
      for c in "validate-plugin.py" "sync-docs.py --check-only" "sync-orchestrator.py --check-only" "sync-evals.py --check-only" "run-evals.py" "run-kaizen-assertions.py" "check-reviewer-protocol-copies.py" "check-cause-table-copies.py" "detect-docs-drift.py --check-table"; do
        (cd "$W" && python3 scripts/$c > "$T/sc.log" 2>&1); out="$out ${c%% *}=$?"
      done
      (cd "$W" && bash harness/evals/measure/measure-helpers-test.sh > "$T/mh.log" 2>&1); out="$out measure-helpers-test.sh=$?"
      echo "rc:$out"
    else
      [ "$(git hash-object "$CILOCAL")" = "$CILOCAL_BLOB" ] && ts=1 || ts=0
      mkdir -p "$T/ci"; TMPDIR="$T/ci" bash "$CILOCAL" "$W" > "$T/ci.out" 2>&1; rc=$?
      S="$T/ci/ci-local/summary.txt"
      [ -f "$S" ] || { echo "tool_same=$ts ci_summary=absent"; return; }
      echo "tool_same=$ts ci_rc=$rc rc0=$(grep -c 'rc=0' "$S") other=[$(grep -v 'rc=0' "$S" | tr '\n' ';')]"
    fi
    ;;
  *) echo "unknown $1" ;;
  esac
}
# === 측정 도우미 끝 ===
```
