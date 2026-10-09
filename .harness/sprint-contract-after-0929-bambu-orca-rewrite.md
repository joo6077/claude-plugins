---
feature: "bambu 오르카 가지 — 원래 커밋 둘을 새 서명 · 맨 위 폴더별 커밋으로 다시 만들어 올린다 (3 회차)"
slug: after-0929-bambu-orca-rewrite
created: "2026-09-29 09:29"
complexity: "복잡"
conditions: 28
status: done
conditions_digest: sha256:a92de5fb57acd564
measurement_digest: sha256:ef4626741ef9b51a
locked_at: "2026-09-29 09:41"
seal_tool: ".harness/.meta/after-0929-bambu-orca-rewrite/ids.sh digest|mdigest (한국어 조건 번호 — 레포 도구는 0 조건으로 센다)"
owner_session: bda55d45-296c-491f-89ba-b52042d58e72
---

## 배경

사용자 결정(`after-0928/.harness/.meta/after-kaizen-0928/decisions.md` 「사용자 결정 (2026-09-29T00:06:30.586Z)」, 원문 「1 나 2 가」)의
1 번 「나 — 원래 가지 역사를 다시 쓴다」 를 이행한다. 남은 일 목록 항목은 A14 · C9 다.

- 원래 가지 `feat/bambu-kit-orca-h2s-feedback`(끝 `42209beb9c1bd86de374cdd3cf87e98e2a992843`)은 구현 커밋 `e55e8b3`(맨 위 폴더 셋 ·
  옛 서명 `Claude Opus 5 (1M context)`)과 QA 기록 커밋 `42209be`(옛 서명)로 되어 있다. 2 회차(가지 `chore/ak3-orca`, 끝 `a2e762c2`)는
  이 가지를 `git merge --no-ff` 로 들여 옛 커밋 둘이 역사에 들어왔고, 봉인된 조건 「모든 커밋 새 서명 · 한 커밋에 맨 위 폴더 하나」 와
  「둘째 부모가 원래 가지 끝」 이 함께 지켜질 수 없어 REJECT(23/24) 뒤 멈췄다
- 이번에는 이 작업 폴더의 가지 `chore/ak3-orca3`(시작 `bfdfd5a3` = `chore/after-kaizen-0928` 끝)에서 원래 커밋 둘의 변경을 **맨 위 폴더마다
  한 커밋**으로 다시 만든다. 병합 커밋으로 원래 가지를 들이지 않는다. 원래 가지와 2 회차 가지는 읽기만 한다
- main 과의 충돌은 2 회차가 푼 결과를 따른다. 2 회차 가지는 `c25d16ec` 에서 갈라졌고 그 뒤 통합 가지에 k1 · lt · rec · d1 · h1 등이
  들어와 오르카 경로 다섯(`run-gate-fixtures.sh` · `SKILL.md` · 문서 페이지 셋)을 바꿨다. 그 변경은 살린다

봉인 전 실측 (scratch 복제본 `o3/tt`, 판 `bfdfd5a3` 위에 오르카 경로를 얹은 임시 트리):

- 2 회차 가지가 바꾼 오르카 경로 20 개(2 회차 자기 기록 여섯 제외) 가운데 통합 가지도 바꾼 것은 다섯이다. 세 판 합치기
  (`git merge-file`, 우리 = `bfdfd5a3` · 기준 = `c25d16ec` · 그쪽 = `a2e762c2`)에서 `SKILL.md` 만 충돌 두 곳이 나고 나머지 넷은 충돌 0.
  두 충돌은 모두 lt 가 빈 줄을 고친 자리(Phase 3.1 절 앞 빈 줄 둘 지움 · 4.4 「생성 후 사용자에게 안내:」 뒤 빈 줄 더함)라
  통합 쪽 줄 가운데 빠지는 글줄은 없다
- 충돌을 2 회차 쪽으로 푼 임시 트리: 시험 파일 실행기 `결과: 28 경우 중 불일치 0`, 슬라이서 없는 흉내 `결과: 28 경우 중 불일치 0 · 건너뜀 20`,
  원래 스프린트 조건 25/25, `validate-plugin bambu-kit` `Exit: 0`, 로컬 CI 25 단계 `rc=0` + `feedback-agg-test SKIP (yq 없음)`,
  CI 에만 있는 15 단계 모두 0, 문서 여섯 쪽 36 칸 넘침 0
- 임시 트리의 마크다운 경고는 1 건(`SKILL.md` 4.4 오르카 안내 목록 앞 빈 줄 없음 — 2 회차 쪽 줄). 통합 판은 0 건이다
- 이번에 새로 드러난 것 둘: (1) 통합 가지가 `docs/bambu-kit/tolerance.html` 을 새로 만들어(d1 `5c48e6c`) 원본 `tolerance.md` §1.3 · §3.2 의
  오르카 쪽 새 내용이 대응 페이지에 없다 — `detect-docs-drift.py --since bfdfd5a3` 가 임시 트리에서 이 짝을 낸다. (2) `bambu-print-profile.html`
  시험 파일 수 칸이 `23 · FAIL 기대 20 · [미검증] 만 1 · PASS 2` 와 실행 줄 설명 `24 개` 로 남아 있다(통합 판부터 틀림 — 통합 판 실제 24 · 21 · 1 · 2,
  합친 뒤 실제 28 · 23 · 1 · 4). 2 회차는 봉인 조건 때문에 못 고쳤다. 이번에는 원본 표와 맞춘다
- 조건 번호는 사용자 결정(`decisions.md` 「계약서 작성할 때 뭔가 줄임말 안썼으면 하는데」)대로 한국어 이름을 쓴다. 지금 레포의 조건 세기 · 봉인 도구는
  한국어 번호를 못 읽는다 — 아래 범위 경계의 「한국어 조건 번호」 에 우회 방법을 적었다

복잡도 네 축:

| 축 | 물음 | 값 |
| -- | ---- | -- |
| 레이어 수 | 몇 계층을 관통하는가 | 예 — 가지 역사 · 스킬 본문과 검사 실행기 · 문서 페이지 · 기록 파일 |
| 공개 계약 변경 | 외부에 드러난 형태가 바뀌는가 | 예 — 완료 검사가 프린터(machine) 설정 파일을 받는다 |
| 소비면 존재 | 받아 쓰는 반대편이 있는가 | 예 — 실행기 `run-gate-fixtures.sh` 가 SKILL.md 표를 읽고, 문서 페이지가 표를 옮긴다 |
| 회귀 위험 | 기존 동작이 깨질 경로가 있는가 | 예 — 통합 가지 쪽 줄 유실 · 옛 커밋 유입 · CI 흉내 불일치 |

넷 다 예라 「복잡」. 소비면은 스크립트-01 · 스크립트-02 · 오류-01(실행기)과 구조-08(문서 페이지)이 따로 잰다.

## 리서치 소스

- 원래 계약 `42209beb:.harness/sprint-contract-bambu-kit-orca-h2s-feedback.md` (31 조건, `status: done`). 본 체크아웃
  `/Users/jackson/Hub/10_Dev/claude-plugins/.harness/` 에는 이 파일이 없다(실측) — 원래 가지 판을 쓴다
- 2 회차 계약 `a2e762c2:.harness/sprint-contract-after-0928-bambu-orca-branch.md`(27 조건) · 개정 `RELAXING_PENDING` · QA 리포트 REJECT(구조 조건 하나)
- 2 회차 기록 `a2e762c2:.harness/.meta/after-kaizen-0928/orca-notes.md` · 측정 도구 `orig-conds.sh`(지문 `866d8a15d2e92105`)
- 계약 형식 문서 `harness/references/contract-schema.md` §측정 관례(서명 줄은 trailers 로 · `LC_ALL=C sort` · `mktemp -d` 틀) · §범위 목록 블록 · §계약 봉인
- 레포 `.claude/skills/docs-site/SKILL.md` — 공통 CSS `docs/assets/site.css` 링크 한 줄, 원본이 바뀌면 대응 페이지도 맞춘다
- 편집기 마크다운 경고 재현법 — 메모리 `reference_markdownlint_editor_parity.md` (markdownlint-cli2 0.23.2 · MD013 끔)

## GAP 분석

| 대상 | 지금(`bfdfd5a3`) | 할 일 |
| --- | --- | --- |
| 가지 역사 | 오르카 커밋 없음 | 원래 커밋 둘의 변경을 맨 위 폴더마다 한 커밋으로 다시 만든다 — `e55e8b3` 몫 셋(`.harness` · `bambu-kit` · `docs`), `42209be` 몫 하나(`.harness`) |
| `SKILL.md` · 참조 문서 다섯 | 오르카 쪽 절 없음 | 2 회차 결과를 세 판 합치기로 얹는다. 충돌 두 곳은 2 회차 쪽, 빈 줄은 lint 0 에 맞춘다 |
| `run-gate-fixtures.sh` | 설치본 필요 검사 목록에 `카메라 준비 블록 없음` 없음 | 2 회차가 더한 한 자리를 옮긴다 |
| 시험 파일 넷 | 없음 | `machine-orca-*.json` 넷을 더한다 |
| 문서 다섯 쪽 | 오르카 쪽 새 절 없음 | 2 회차 페이지 변경을 세 판 합치기로 얹고, `bambu-print-profile.html` 수 칸 둘을 원본 표와 맞춘다 |
| `tolerance.html` | §1.3 · §3.2 새 내용 없음 (표시 낱말 실측 0) | 새 절 하나와 §3.2 한 줄을 옮긴다 |
| 원래 기록 네 파일 | 없음 | 원래 가지 판과 한 글자도 다르지 않게 싣는다 |
| 기록 | — | `orca3-notes.md` 에 충돌 줄을 누구 판으로 골랐는지 표 · 카메라 실물 확인(사용자 몫) · 한국어 번호 우회 |

## 범위 경계

측정 공통 전제 (모든 조건이 이 정의를 쓴다. zsh · bash 동일, 모든 조건은 「이 스프린트의 커밋이 끝나고 작업 폴더의
`bambu-kit/` · `docs/` 변경이 0 인 상태」 가 전제다 — `git status --porcelain -- bambu-kit docs | grep -c .` 이 0):

```bash
W=/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak3-orca3
cd "$W"
CF=$W/.harness/sprint-contract-after-0929-bambu-orca-rewrite.md
M=$W/.harness/.meta/after-0929-bambu-orca-rewrite       # 측정 도구 다섯 — 지문은 아래
N=$W/.harness/.meta/after-kaizen-0928/orca3-notes.md
INTEG=bfdfd5a39800d837ed5b4b529cd44061ec9da275   # 이 가지 시작점 = chore/after-kaizen-0928 끝
PREV=a2e762c220bb1c5bdacf8f5cae463cc6c37047ec    # chore/ak3-orca 끝 (2 회차)
FEAT=42209beb9c1bd86de374cdd3cf87e98e2a992843    # feat/bambu-kit-orca-h2s-feedback 끝 (원래 가지)
S=bambu-kit/skills/bambu-print-profile/SKILL.md
H=docs/bambu-kit/bambu-print-profile.html
T=docs/bambu-kit/tolerance.html
sprint_head() { git rev-parse --verify -q chore/ak3-orca3 || { echo "UNRESOLVED chore/ak3-orca3" >&2; return 1; }; }
X=$(mktemp -d "${TMPDIR:-/tmp}/o3.XXXXXX")    # 임시 사본 자리. TMPDIR 은 scratch 아래 폴더로 준다
fx_s() { sed -nE 's/^\| `evals\/gate-fixtures\/([^`]+\.json)` \|.*/\1/p' "${1}" | LC_ALL=C sort -u; }
fx_h() { sed -nE 's/.*<tr><td><code>([a-z0-9-]+\.json)<\/code><\/td>.*/\1/p' "${1}" | LC_ALL=C sort -u; }
col() { grep -E '^\| `evals/gate-fixtures/' "${1}" | awk -F'|' '{print $(4)}'; }
noslicer() { sed 's#pathlib.Path("/Applications/#pathlib.Path("/nonexistent-ci/#' "$S" > "${1}"; }   # CI 흉내 사본 — 바뀐 줄 5
```

- 측정 도구 다섯은 봉인 전에 이 계약을 쓰며 만들었다. 지문(`shasum -a 256` 앞 16 자)이 아래와 다르면 그 도구를 쓰는 조건은 FAIL 이다:
  `ref3.sh 694c509b157bbe83` · `hist.sh 24bf8e21e4a6bc8e` · `orig-conds.sh 866d8a15d2e92105`(2 회차 도구 그대로) · `ids.sh 9b084dffe5d850e9` ·
  `ci-only.sh b0d9acff85ccc1f7`. 도구는 봉인 커밋과 따로 커밋한다
- `ref3.sh <레포> <경로>` 는 오르카 경로 하나의 기준 내용을 낸다 — 통합 가지가 `c25d16ec` 뒤에 그 경로를 안 바꿨으면 2 회차 끝 판, 바꿨으면
  세 판 합치기(`git merge-file -p --theirs`, 충돌 자리는 2 회차 쪽). 봉인 전 실측: 임시 트리 20 경로 모두 `diff -B` 0 줄,
  `SKILL.md` 를 `$INTEG` 판으로 주면 133 줄 · `$PREV` 판으로 주면 54 줄 · `$FEAT` 판으로 주면 916 줄
- `hist.sh <레포> <시작> <끝>` 알려진 답(봉인 전 실측): scratch 복제본에서 손으로 다시 만든 네 커밋(`sim3`)은 `anc … no` 둘 · `merges=0` ·
  문제 커밋 0 · `cite e55e8b36 folders=.harness,bambu-kit,docs subj=3` · `cite 42209beb folders=.harness subj=1` ·
  `cover e55e8b36 files=14/14 harness_same=3/3` · `cover 42209beb files=2/2 harness_same=2/2` · `commits=4`. 원래 기록 파일을 끝 판으로 한 번에 실은
  엉성한 사본(`sim`)은 `harness_same=2/3` · `files=1/2 harness_same=1/2`, 폴더 둘을 한 커밋에 실은 사본(`sim2`)은 `MANY` 한 줄,
  2 회차 구간 `c25d16ec..a2e762c2` 는 `anc … yes` 둘 · `merges=1` · `MANY` 1 · `NOSIG` 2 · `cite … folders= subj=0` 둘
- 원래 커밋 번호(40 자)는 다시 만든 커밋 넷의 본문에만 적는다. 다른 커밋 본문에 40 자 번호를 적으면 구조-03 의 `folders` · `subj` 가 달라진다.
  기록 파일 내용에 적는 것은 상관없다
- 병합 커밋 금지 · 푸시 금지 · 가지 바꾸기 금지. 원래 가지와 2 회차 가지는 지우지도 고치지도 않는다. 2 회차의 계약 · 개정 · 리포트 · `orca-notes.md` ·
  `orca-tools/` 는 그 가지의 옛 기록으로 남기고 이 가지로 옮기지 않는다
- 넣지 않는 것: 가지 올리기 · PR(남은 일 A14 · C9 의 올리기 몫 — 금지-02 가 오히려 올리지 않았음을 잰다. 올리기는 사용자 결정 뒤 다른 묶음이 한다), 릴리스 · 킷 버전 올리기(2 회차 기록대로 minor 가 맞으나 이번 범위 밖), 사용자 설정 파일(레포 밖) 고치기, 카메라 실물 확인(사용자 몫 —
  notes 에 적는다), 레포의 조건 세기 · 봉인 도구 고치기(다른 묶음 id 몫)
- 이 맥에는 두 슬라이서가 설치돼 있다. 그래서 이 맥 실행(스크립트-01)은 28 경우 모두 판정되고, 슬라이서 없는 CI 는 `noslicer` 사본으로 흉낸다
- 로컬 CI 의 `feedback-agg-test` 는 `yq` 가 없어 도구가 스스로 `SKIP` 한다(봉인 전 실측). 그 한 줄은 FAIL 로 세지 않는다
- 한국어 조건 번호: sprint-contract 6.2 · 6.5 의 `grep -cE '^- \[[ x]\] [A-Z]{2,}-[0-9]{2}'`, 계약 형식 문서 §계약 봉인의 `contract_digest` ·
  `measurement_digest`, qa-evaluator 의 조건 세기(`harness/agents/qa-evaluator.md` 592 줄)가 모두 영어 약자 번호만 읽는다. 이 계약을 그대로 넣으면
  조건 수 0, 봉인 값은 빈 입력의 지문이 된다(봉인 전 실측 — 한국어 번호 둘 · 영어 번호 하나를 담은 사본에서 레포 도구 1 줄 · `ids.sh count` 3 줄).
  레포 도구는 고치지 않는다. 우회: 조건 수 · 봉인 두 값은 `ids.sh count|func|digest|mdigest` 로 센다. 영어 번호만 든 계약
  `after-0928-harness-checks-r2` 에서 `ids.sh` 와 레포 도구가 같은 값(`925cf12b1330ffe9` · `ff2e15044cb81057` · 44)을 낸다(봉인 전 실측).
  평가자에게도 이 도구로 세라고 넘긴다
- 커버리지 해소: 스킬-01 · 구조-05 · 구조-08 · 구조-10 · 구조-11 — 측정이 「경로마다 · 쪽마다」 로 산문의 경로를 같은 표기로 하나씩 넣는다
  (`<경로>` · `<여섯 쪽>` 자리). 구조-11 의 `.harness/.meta/after-kaizen-0928/orca3-notes.md` 는 공통 전제의 `$N`, `ids.sh` 는 찾을 낱말이다.
  구조-08 의 `SKILL.md` 는 공통 전제의 `$S`, 구조-09 의 `docs/bambu-kit/tolerance.html` 은 `$T`, `tolerance.md` 는 산문 설명이고
  낱말 `+0.24` 는 「낱말마다」 여덟 번에 든다. 구조-03 의 `.harness` 는 `hist.sh` 출력 줄 `folders=.harness,…` 안에 있다.
  한국어 번호를 읽게 넓힌 검출기 사본(scratch `o3/cov-k.sh`, 레포 검출기와 번호 줄 두 줄만 다름)이 이 일곱 건을 냈고, 레포 검출기는 0 건(번호를 못 읽음)이다
- 커버리지 해소: 스킬-02 — 측정이 `orig-conds.sh` 하나로 산문에 나열한 번호 25 개를 한 줄씩 낸다
- 오라클 해소: 구조-01 ~ 구조-03 — 글을 찾지 않고 `git merge-base --is-ancestor` · `rev-list` · trailers 로 역사를 직접 읽는다
- 오라클 해소: 진단-02 — 마크다운 검사기를 실제로 돌린 경고 줄과 `Linting: 6 files` 줄을 함께 센다

```text
# sprint-scope
bambu-kit/skills/bambu-print-profile/SKILL.md
bambu-kit/skills/bambu-print-profile/references/bambu-fields-baseline.md
bambu-kit/skills/bambu-print-profile/references/failure-recipes.md
bambu-kit/skills/bambu-print-profile/references/seam-recipes.md
bambu-kit/skills/bambu-print-profile/references/surface-recipes.md
bambu-kit/skills/bambu-print-profile/references/tolerance.md
bambu-kit/evals/gate-fixtures/machine-orca-h2s-bs-start.json
bambu-kit/evals/gate-fixtures/machine-orca-h2s-cooling-filter-var.json
bambu-kit/evals/gate-fixtures/machine-orca-h2s-no-camera-prep.json
bambu-kit/evals/gate-fixtures/machine-orca-x1c.json
bambu-kit/evals/run-gate-fixtures.sh
docs/bambu-kit/bambu-print-profile.html
docs/bambu-kit/bambu-fields-baseline.html
docs/bambu-kit/failure-recipes.html
docs/bambu-kit/seam-recipes.html
docs/bambu-kit/surface-recipes.html
docs/bambu-kit/tolerance.html
```

## 회귀 게이트

- 봉인 전 `$W`(= `$INTEG`, 계약 빈 파일과 측정 도구만 더한 상태)에서 로컬 CI(`TMPDIR=<scratch> bash /Users/jackson/Hub/10_Dev/claude-plugins/.harness/handoff/2026-09-26-tools/ci-local.sh $W`)
  25 단계 `rc=0` + `feedback-agg-test SKIP (yq 없음)`, `bash $M/ci-only.sh $W` 끝 줄 `ci_only=15/15`
- 봉인 전 `$W` 에서 `run-gate-fixtures.sh` `결과: 24 경우 중 불일치 0` · 흉내 `결과: 24 경우 중 불일치 0 · 건너뜀 19` · `orig-conds.sh` `orig_ok=3/25`
- 봉인 전 `$W` 여섯 쪽 배치 검사 `cells=36 bad=0`, 폭 1900px 블록을 넣은 나쁜 사본 한 쪽 `cells=6 bad=6`
- 봉인 전 마크다운 경고(MD013 끔, SKILL.md 와 참조 문서 다섯) — 통합 판 0 · 임시 트리 1 · 2 회차 판 `SKILL.md` 하나만 119

## Skill

- [ ] 스킬-01: Given 이 스프린트 커밋이 끝난 뒤, `bambu-kit/skills/bambu-print-profile/SKILL.md` · `bambu-kit/skills/bambu-print-profile/references/bambu-fields-baseline.md` · `bambu-kit/skills/bambu-print-profile/references/failure-recipes.md` · `bambu-kit/skills/bambu-print-profile/references/seam-recipes.md` · `bambu-kit/skills/bambu-print-profile/references/surface-recipes.md` · `bambu-kit/skills/bambu-print-profile/references/tolerance.md` · `bambu-kit/evals/run-gate-fixtures.sh` · `bambu-kit/evals/gate-fixtures/machine-orca-h2s-bs-start.json` · `bambu-kit/evals/gate-fixtures/machine-orca-h2s-cooling-filter-var.json` · `bambu-kit/evals/gate-fixtures/machine-orca-h2s-no-camera-prep.json` · `bambu-kit/evals/gate-fixtures/machine-orca-x1c.json` 열한 경로가 `$(sprint_head)` 에서 기준 내용(2 회차 결과 + 통합 가지 변경)과 빈 줄 말고는 같다 [exact, enumerated]
  측정: 경로마다 `bash $M/ref3.sh $W <경로> > $X/ref; git show "$(sprint_head)":<경로> > $X/new; diff -B $X/ref $X/new | grep -cE '^[<>]'` 이 0 (열한 번, 위 경로를 그대로 넣는다)
  양성 대조: `SKILL.md` 자리에 `git show $INTEG:$S` 를 주면 133 · `git show $PREV:$S` 를 주면 54 (봉인 전 실측)
  알려진 답: 임시 트리 열한 경로 모두 0 (봉인 전 실측)
- [ ] 스킬-02: Given 커밋 뒤, 원래 스프린트 조건을 다시 잰 `orig-conds.sh` 가 25/25 를 낸다 — `SK-01` · `SK-02` · `SK-03` · `SK-04` · `SK-05` · `SC-01` · `SC-02` · `SC-03` · `SC-04` · `SC-06a` · `SC-06b` · `ER-01` · `ER-02` · `ER-03` · `AR-01` · `AR-02a` · `AR-02b` · `AR-03a` · `AR-03b` · `AR-04` · `AR-05a` · `AR-05b` · `AR-06` · `AR-07` · `AR-08` 25 줄이 모두 `ok`. 원래 SC-05 는 main 쪽이 검사를 새로 고쳐 스크립트-01 이 대신 재고, 원래 SC-06 은 `SC-06a`(machine 파일 PASS) · `SC-06b`(process 파일이 새 규칙 `허공 위 속도` 로만 FAIL 1 건)로 나눴다(2 회차와 같은 풀이) [exact, enumerated]
  측정: `bash $M/orig-conds.sh $W` 끝 줄 `orig_ok=25/25` · 종료 코드 0
  알려진 답: 통합 판 `$W`(봉인 전) `orig_ok=3/25` · 임시 트리 `orig_ok=25/25` (봉인 전 실측)
- [ ] 스킬-03: Given 커밋 뒤, `SKILL.md` 음성 대조 표의 시험 파일이 정확히 28 개이고 기대 칸이 FAIL 기대 23 · `[미검증]` 만 기대 1 · PASS 기대 4 로 나뉜다 [exact]
  측정: `git show "$(sprint_head)":$S > $X/s.md; fx_s $X/s.md | wc -l` 이 28 · `col $X/s.md | grep -c 'FAIL 1 건'` 23 · `col $X/s.md | grep -c 'FAIL 0 건'` 1 · `col $X/s.md | grep -cF '**PASS**'` 4
  기준값: 통합 판 24 · 21 · 1 · 2, 임시 트리 28 · 23 · 1 · 4 (봉인 전 실측)

## Script

- [ ] 스크립트-01: Given 커밋 뒤 이 맥(두 슬라이서 설치), When `bash bambu-kit/evals/run-gate-fixtures.sh` 를 돌리면, Then 끝 줄이 `결과: 28 경우 중 불일치 0` 이고 종료 코드 0 이다 [exact]
  측정: 그대로 실행
  음성 대조: `SKILL.md` 사본에서 `errs.append(f"카메라 준비 블록 없음` 줄 하나만 `pass` 로 바꾸고(바뀐 줄 1) `BAMBU_GATE_SKILL=<사본>` 으로 돌리면 `불일치 machine-orca-h2s-no-camera-prep.json — 기대 fail · 결과 FAIL 0 줄 · 종료 코드 0` · `결과: 28 경우 중 불일치 1` · 종료 코드 1 (봉인 전 임시 트리 실측)
- [ ] 스크립트-02: Given 커밋 뒤, When 슬라이서 없는 흉내 사본(`noslicer $X/ns.md`)으로 `BAMBU_GATE_SKILL=$X/ns.md bash bambu-kit/evals/run-gate-fixtures.sh` 를 돌리면, Then 끝 줄이 `결과: 28 경우 중 불일치 0 · 건너뜀 20` 이고 종료 코드 0 이다 [exact]
  측정: 그대로 실행, 출력은 `$X/ns.out` 에 남긴다(오류-01 · 오류-02 가 읽는다)
  음성 대조: 실행기 사본에서 설치본 필요 목록의 `|카메라 준비 블록 없음` 만 지우고(바뀐 줄 1, 사본은 `bambu-kit/evals/` 안에 두어야 시험 파일 폴더를 찾는다) 같은 흉내로 돌리면 `결과: 28 경우 중 불일치 1 · 건너뜀 19` · 종료 코드 1 (봉인 전 임시 트리 실측)
  기준값: 통합 판 `결과: 24 경우 중 불일치 0 · 건너뜀 19`
- [ ] 스크립트-03: Given 커밋 뒤, bambu 시험 둘째와 킷 검증이 통과한다 — `bash bambu-kit/evals/makerworld-fetch-test.sh` 종료 코드 0 · `python3 scripts/validate-plugin.py bambu-kit` 끝 줄 `Exit: 0` [exact, enumerated]
  측정: 두 명령을 `TMPDIR=<scratch>` 로 실행
  기준값: 통합 판 · 임시 트리 모두 둘 다 0 (봉인 전 실측)

## Error

- [ ] 오류-01: Given 커밋 뒤 슬라이서 없는 흉내, When 실행기를 돌리면, Then `machine-orca-h2s-no-camera-prep.json` 줄이 `일치` 도 `불일치` 도 아닌 `건너뜀 machine-orca-h2s-no-camera-prep.json — orca 설치본이 없어 「카메라 준비 블록 없음」 검사가 안 돈다` 한 줄이다 — 부모 설정을 못 읽어 판정 못 한 것을 통과로 세지 않는다 [exact]
  측정: 스크립트-02 출력 `$X/ns.out` 에서 `grep -cxF '건너뜀 machine-orca-h2s-no-camera-prep.json — orca 설치본이 없어 「카메라 준비 블록 없음」 검사가 안 돈다'` 이 1
  기준값: 실행기 판정 목록을 되돌린 사본(스크립트-02 음성 대조)은 0 — 그 자리에 `불일치` 가 나온다 (봉인 전 실측)
- [ ] 오류-02: Given 커밋 뒤 슬라이서 없는 흉내, `machine-orca-h2s-cooling-filter-var.json` 은 설치본 없이도 판정된다 — 시작 명령을 파일 안에서 읽으므로 건너뛰면 안 된다 [exact]
  측정: `$X/ns.out` 에서 `grep -cxF '일치 machine-orca-h2s-cooling-filter-var.json'` 이 1
  기준값: 임시 트리 1 (봉인 전 실측)

## Architecture

- [ ] 구조-01: Given 커밋 뒤, 원래 가지 커밋 `e55e8b3655eb2656a1a3298808664954d1e16785` · `42209beb9c1bd86de374cdd3cf87e98e2a992843` 둘 다 `$(sprint_head)` 의 조상이 아니고, `$INTEG..$(sprint_head)` 에 병합 커밋이 0 개이며 커밋이 5 개 이상이다 — 커밋이 하나도 없는 상태에서는 앞의 두 값이 저절로 맞으므로 커밋 수를 같이 잰다 [exact, enumerated]
  측정: `bash $M/hist.sh $W $INTEG "$(sprint_head)" > $X/hist.txt` 뒤 `grep -cxF 'anc e55e8b36 no' $X/hist.txt` 1 · `grep -cxF 'anc 42209beb no' $X/hist.txt` 1 · `grep -cxF 'merges=0' $X/hist.txt` 1 · 끝 줄 `commits=<수>` 의 수가 5 이상
  음성 대조: 커밋 전 `$INTEG` 그대로(`bash $M/hist.sh $W $INTEG $INTEG`)는 `anc … no` 둘 · `merges=0` 이 이미 나오지만 `commits=0` 이라 FAIL (교차 진단 실측)
  양성 대조: `bash $M/hist.sh $W c25d16ec $PREV` 는 `anc e55e8b36 yes` · `anc 42209beb yes` · `merges=1` (봉인 전 실측)
- [ ] 구조-02: Given 커밋 뒤, `$INTEG..$(sprint_head)` 의 모든 커밋이 맨 위 폴더 하나만 싣고, Co-Authored-By 트레일러가 정확히 하나이며 그 값이 `Claude Opus 5.5 (1M context) <noreply@anthropic.com>` 이다 [exact]
  측정: `$X/hist.txt` 에서 `grep -cE '^(MANY|NOSIG) ' $X/hist.txt` 이 0 이고 끝 줄 `commits=<수>` 의 수가 5 이상(다시 만든 커밋 넷 + 봉인 커밋)
  양성 대조: 2 회차 구간 `c25d16ec..$PREV` 는 `MANY e55e8b36…` 1 줄 · `NOSIG` 2 줄, 폴더 둘을 한 커밋에 실은 사본 `sim2` 는 `MANY` 1 줄 (봉인 전 실측)
- [ ] 구조-03: Given 커밋 뒤, 원래 커밋 둘을 다시 만든 커밋이 본문에 원래 번호(40 자)와 원래 제목 줄을 밝히고 원래 파일을 빠짐없이 싣는다 — `e55e8b3…` 을 밝힌 커밋은 맨 위 폴더 `.harness` · `bambu-kit` · `docs` 에 하나씩이고 셋 모두 원래 제목 `feat(bambu-kit): 오르카 · H2S 출력 피드백 반영 — 프린터 설정 검사와 실패 레시피 4종` 을 한 줄로 적었으며 원래 파일 14 개를 모두 싣고 그 가운데 `.harness` 파일 셋은 원래 커밋 판과 같다. `42209be…` 를 밝힌 커밋은 `.harness` 하나이고 제목 `chore(harness): bambu-kit 오르카 · H2S 피드백 스프린트 QA 승인 기록` 을 적었으며 원래 파일 둘을 원래 판 그대로 싣는다 [exact, enumerated]
  측정: `$X/hist.txt` 에 `cite e55e8b36 folders=.harness,bambu-kit,docs subj=3` · `cite 42209beb folders=.harness subj=1` · `cover e55e8b36 files=14/14 harness_same=3/3` · `cover 42209beb files=2/2 harness_same=2/2` 네 줄이 저마다 `grep -cxF` 로 1
  알려진 답: 손으로 바르게 다시 만든 `sim3` 은 네 줄 그대로, 원래 기록을 끝 판으로 한 번에 실은 `sim` 은 `harness_same=2/3` · `files=1/2 harness_same=1/2` (봉인 전 실측)
- [ ] 구조-04: 원래 가지와 2 회차 가지를 지우거나 고치지 않았다 — `git rev-parse feat/bambu-kit-orca-h2s-feedback` 이 `42209beb9c1bd86de374cdd3cf87e98e2a992843`, `git rev-parse chore/ak3-orca` 가 `a2e762c220bb1c5bdacf8f5cae463cc6c37047ec` 이다 [exact, enumerated]
  측정: 두 명령 그대로
  기준값: 봉인 전 같은 두 값
- [ ] 구조-05: Given 커밋 뒤, 원래 기록 네 파일 `.harness/sprint-contract-bambu-kit-orca-h2s-feedback.md` · `.harness/sprint-feedback-bambu-kit-orca-h2s-feedback.md` · `.harness/sprint-amendments-bambu-kit-orca-h2s-feedback.md` · `.harness/.meta/evidence/bambu-orca-h2s-feedback.md` 가 `$(sprint_head)` 에서 원래 가지 끝 판과 한 글자도 다르지 않다 — 봉인된 원래 계약의 봉인이 그대로다 [exact, enumerated]
  측정: 경로마다 `[ "$(git rev-parse "$(sprint_head)":<경로>)" = "$(git rev-parse $FEAT:<경로>)" ]` 네 번 모두 참
  기준값: 봉인 전 `$INTEG` 에는 네 파일이 없다
- [ ] 구조-06: Given 커밋 뒤, `.harness/` 밖에서 바뀐 경로가 모두 범위 경계의 `# sprint-scope` 블록 안에 있다 — 포함 관계, 생성물 없음 [exact]
  측정: `awk '/^## 범위 경계/{s=1} s&&$(0)=="# sprint-scope"{b=1;next} b&&/^```/{exit} b&&NF{print}' "$CF" > $X/scope.txt` (17 줄) 뒤 `git diff --name-only $INTEG "$(sprint_head)" | grep -v '^\.harness/' | grep -vxF -f $X/scope.txt | grep -c .` 이 0
  양성 대조: 구간을 `$INTEG $PREV` 로 바꾸면 216 경로가 블록 밖 (2 회차 가지가 통합 쪽 변경을 되돌린 모양, 봉인 전 실측)
- [ ] 구조-07: Given 커밋 뒤, `.harness/` 안에서 바뀐 경로가 원래 기록 네 파일 · 이 계약의 계약 · 피드백 · 개정 · 피드백 초안 · 측정 도구 폴더 `.harness/.meta/after-0929-bambu-orca-rewrite/` · 기록 `.harness/.meta/after-kaizen-0928/orca3-notes.md` 뿐이다 [exact]
  측정: `git diff --name-only $INTEG "$(sprint_head)" -- .harness | grep -vxE '\.harness/(\.meta/evidence/bambu-orca-h2s-feedback\.md|sprint-(amendments|contract|feedback)-bambu-kit-orca-h2s-feedback\.md|sprint-(amendments|contract|feedback)-after-0929-bambu-orca-rewrite\.md|feedback-draft-after-0929-bambu-orca-rewrite\.yaml|\.meta/after-0929-bambu-orca-rewrite/[^/]+|\.meta/after-kaizen-0928/orca3-notes\.md)' | grep -c .` 이 0
  양성 대조: 구간을 `c25d16ec $PREV` 로 바꾸면 6 (2 회차 자기 기록 여섯, 봉인 전 실측)
- [ ] 구조-08: Given 커밋 뒤, 문서 다섯 쪽 `docs/bambu-kit/bambu-fields-baseline.html` · `docs/bambu-kit/failure-recipes.html` · `docs/bambu-kit/seam-recipes.html` · `docs/bambu-kit/surface-recipes.html` · `docs/bambu-kit/bambu-print-profile.html` 이 기준 내용과 빈 줄 말고는 같다. 예외는 `bambu-print-profile.html` 의 두 줄뿐이다 — 시험 파일 수 칸이 `<div class="v">28</div>` 와 `FAIL 기대 23 · <code>[미검증]</code> 만 기대 1 · PASS 기대 4` 를, 실행 줄 설명이 `(2) 검사 유지 — 28 개를` 을 담는다. 그 쪽의 시험 파일 표는 `SKILL.md` 표와 같은 28 개 이름이다 [exact, enumerated]
  측정: 앞 넷은 경로마다 `bash $M/ref3.sh $W <경로> > $X/ref; git show "$(sprint_head)":<경로> > $X/new; diff -B $X/ref $X/new | grep -cE '^[<>]'` 이 0. `bambu-print-profile.html` 은 같은 차이를 `$X/hd.txt` 에 남겨 `grep -cE '^[<>]' $X/hd.txt` 이 4 · `grep '^>' $X/hd.txt | grep -F '<div class="v">28</div>' | grep -cF 'FAIL 기대 23 · <code>[미검증]</code> 만 기대 1 · PASS 기대 4'` 1 · `grep '^>' $X/hd.txt | grep -cF '(2) 검사 유지 — 28 개를'` 1 · `grep '^<' $X/hd.txt | grep -cF '<div class="v">23</div>'` 1 · `grep '^<' $X/hd.txt | grep -cF '(2) 검사 유지 — 24 개를'` 1. 표는 `git show "$(sprint_head)":$H > $X/h.html; git show "$(sprint_head)":$S > $X/s.md; diff <(fx_s $X/s.md) <(fx_h $X/h.html) | grep -cE '^[<>]'` 이 0 이고 `fx_h $X/h.html | wc -l` 이 28
  알려진 답: 임시 트리 쪽에 두 줄만 고친 사본은 위 값 그대로(4 · 1 · 1 · 1 · 1), 고치지 않은 임시 트리 쪽은 차이 0 (봉인 전 실측)
  기준값: 통합 판 표 24 행
- [ ] 구조-09: Given 커밋 뒤, `docs/bambu-kit/tolerance.html` 이 원본 `tolerance.md` 의 오르카 쪽 새 내용을 담는다 — 낱말 `가로 구멍` · `ISO 273` · `#7744` · `#7080` · `눈물방울` · `+0.24` · `Auto circle contour-hole compensation` · `구멍이 옆으로 누워 있으면 아래 보정값이 걸리지 않는다` 가 저마다 1 번 이상, 제목 `<h2` 줄 · 목차 줄 · 본문 절 수가 저마다 12, `1.3 ⚠️ 구멍 축` 을 담은 `<h2` 줄과 목차 줄이 저마다 1 이다. 통합 판에 있던 줄은 절 번호 줄(`§ NN` 표지 · 절 여는 줄 · 목차 번호 줄) 말고 모두 남는다 [exact, enumerated]
  측정: `git show "$(sprint_head)":$T > $X/t.html; git show $INTEG:$T > $X/t0.html` 뒤 낱말마다 `grep -cF -- '<낱말>' $X/t.html` 1 이상(여덟 번) · `grep -c '<h2' $X/t.html` 12 · `grep -c '<li><a href="#s[0-9]*"><span class="toc-n">' $X/t.html` 12 · `grep -c '<section class="section doc" id="s[0-9]*">' $X/t.html` 12 · `grep '<h2' $X/t.html | grep -cF '1.3 ⚠️ 구멍 축'` 1 · `grep 'class="toc-n"' $X/t.html | grep -cF '1.3 ⚠️ 구멍 축'` 1 · `grep -vxF -f $X/t.html $X/t0.html | grep -vE 'class="section-label">§ [0-9]+<|<section class="section doc" id="s[0-9]+">|class="toc-n">' | grep -c .` 이 0
  기준값: 통합 판 낱말 여덟 모두 0 · 제목 · 목차 · 절 저마다 11 (봉인 전 실측)
  양성 대조: 통합 판에서 글줄 하나(300 번째 줄)를 지운 사본은 마지막 측정이 1, `§ 04` 표지를 `§ 05` 로 바꾼 사본은 0 (봉인 전 실측)
- [ ] 구조-10: 여섯 쪽 `docs/bambu-kit/bambu-fields-baseline.html` · `docs/bambu-kit/failure-recipes.html` · `docs/bambu-kit/seam-recipes.html` · `docs/bambu-kit/surface-recipes.html` · `docs/bambu-kit/bambu-print-profile.html` · `docs/bambu-kit/tolerance.html` 이 저마다 스타일 링크를 정확히 한 줄(`<link rel="stylesheet" href="../assets/site.css">`) 갖고, 320 · 375 · 1280 폭 × 밝은 · 어두운 테마 36 칸에서 가로 넘침 · 잘린 글 · 콘솔 오류가 0 이다 [exact, enumerated]
  측정: 쪽마다 `grep -c 'rel="stylesheet"'` 이 1 이고 `grep -cxF '<link rel="stylesheet" href="../assets/site.css">'` 이 1 · `node $W/.harness/.meta/after-0926-docs-regen-a/layout.js $W <여섯 쪽> > $X/lay.txt` 의 종료 코드 0 이고 끝 줄 `cells=36 bad=0` (`$W/node_modules/playwright-core` 가 있어야 한다 — 봉인 전 있음)
  양성 대조: 폭 1900px 블록을 넣은 사본 한 쪽은 `cells=6 bad=6` (봉인 전 실측)
- [ ] 구조-11: 기록 `.harness/.meta/after-kaizen-0928/orca3-notes.md` 에 세 가지가 있다 — (1) 표 줄(`|` 로 시작)에 `bambu-kit/skills/bambu-print-profile/SKILL.md` · `bambu-kit/evals/run-gate-fixtures.sh` · `docs/bambu-kit/bambu-fields-baseline.html` · `docs/bambu-kit/bambu-print-profile.html` · `docs/bambu-kit/failure-recipes.html` · `docs/bambu-kit/tolerance.html` 이 저마다 1 번 이상 나온다(어느 줄을 누구 판으로 골랐는지), (2) `카메라` 와 `사용자가 할 일` 이 같은 줄에 있는 줄이 1 개 이상, (3) `조건 번호` 와 `ids.sh` 가 같은 줄에 있는 줄이 1 개 이상(한국어 번호 우회) [exact, enumerated]
  측정: 경로마다 `grep '^|' $N | grep -cF '<경로>'` 1 이상(여섯 번) · `grep -F '카메라' $N | grep -cF '사용자가 할 일'` 1 이상 · `grep -F '조건 번호' $N | grep -cF 'ids.sh'` 1 이상
  기준값: 파일 없음

## Anti-patterns

- [ ] 금지-02: force push 금지 — 원래 가지 · 2 회차 가지 · 이 가지 어느 것도 원격에 올리지 않았다
  측정: `git ls-remote origin refs/heads/feat/bambu-kit-orca-h2s-feedback refs/heads/chore/ak3-orca refs/heads/chore/ak3-orca3 > $X/lr.txt; rc=$?` 뒤 `rc` 가 0 이고 `grep -c . $X/lr.txt` 이 0 (파이프 뒤 `$?` 는 grep 의 종료 코드라 쓰지 않는다)
  양성 대조: `git ls-remote origin refs/heads/main | grep -c .` 이 1 (봉인 전 실측)
- [ ] 금지-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수
  측정: `python3 scripts/validate-plugin.py bambu-kit --check=code-fence` 종료 코드 0
- [ ] 금지-04: SKILL.md / agents/*.md frontmatter 에서 name 필드 누락 — validate-plugin V1 FAIL
  측정: `python3 scripts/validate-plugin.py bambu-kit --check=frontmatter` 종료 코드 0

## Reusability

- [ ] 재사용-01: N/A (새 재사용 단위를 만들지 않는다 — 변경은 기존 파일에 2 회차 결과 옮기기 · 시험 파일 넷 · 문서 페이지뿐)
  측정: `git diff --name-only --diff-filter=A $INTEG "$(sprint_head)" -- . ':(exclude).harness' ':(exclude)bambu-kit/evals/gate-fixtures'` 이 0 줄
- [ ] 재사용-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다 — 슬라이서 없는 곳의 판정은 실행기의 기존 건너뜀 규칙에 한 자리를 더해 쓰고 새 스크립트를 레포에 더하지 않았다
  측정: 재사용-01 과 같은 명령이 0 줄, 그리고 `git diff $INTEG "$(sprint_head)" -- bambu-kit/evals/run-gate-fixtures.sh | grep -cE '^[+-][^+-]'` 이 4 이하
  기준값: 임시 트리 4 (봉인 전 실측)

## Diagnostics

- [ ] 진단-01: N/A (commands.analyze 는 scripts/release.sh 만 잰다 — 이번 변경 파일과 교집합 0 개)
  측정: `git diff --name-only $INTEG "$(sprint_head)" | grep -c '^scripts/release.sh$'` 이 0
- [ ] 진단-02: IDE diagnostics 워닝/인포 0개 (제외 목록 `[]`) — 마크다운은 편집기와 같은 설정(markdownlint-cli2 0.23.2 · `{ "config": { "MD013": false } }`)으로 SKILL.md 와 참조 문서 다섯의 경고가 0 이다
  측정: scratch 에 `npm install --no-save markdownlint-cli2@0.23.2` 뒤 그 `node_modules/.bin/markdownlint-cli2` 를 절대 경로로 `--help` 불러 첫 줄이 `markdownlint-cli2 v0.23.2 (markdownlint v0.41.1)` 인지 먼저 본다(다른 판이면 FAIL). `$W` 에서 같은 절대 경로로 `--config <설정> <여섯 파일> > $X/ml.txt 2>&1` 뒤 `grep -cE ' MD[0-9]{3}' $X/ml.txt` 0 · `grep -cxF 'Linting: 6 files' $X/ml.txt` 1 · `grep -cxF 'Summary: 0 issues in 0 files' $X/ml.txt` 1
  양성 대조: 임시 트리 1 건(`SKILL.md` 4.4 오르카 안내 목록 MD032), 2 회차 판 `SKILL.md` 하나만 119 (봉인 전 실측)
  기준값: 통합 판 0
- [ ] 진단-03: N/A (commands.test 는 scripts/release.sh 를 돌린다 — 이번 변경 파일과 교집합 0 개)
  측정: 진단-01 과 같은 명령이 0
- [ ] 진단-04: 실제 구동 시 에러 0개 — 로컬 CI 도구와 CI 에만 있는 단계가 모두 통과한다
  측정: `TMPDIR=<scratch 아래 새 폴더> bash /Users/jackson/Hub/10_Dev/claude-plugins/.harness/handoff/2026-09-26-tools/ci-local.sh $W` 뒤 그 폴더의 `ci-local/summary.txt` 에서 `grep -c 'rc=0'` 이 25 이고 `grep -v 'rc=0'` 가 `feedback-agg-test SKIP (yq 없음)` 한 줄 · `TMPDIR=<scratch> bash $M/ci-only.sh $W` 끝 줄 `ci_only=15/15` · 종료 코드 0 (`check-api-kit-docs.py` · `detect-docs-drift.py --check-table` · `test-detect-docs-drift.py` · `check-docs-common-css.py` · `test-check-docs-common-css.py` · `check-cause-table-copies.py` · `check-install-docs-guidance.py` · `test-check-cause-table-copies.py` · `test-ci-local.sh` · `measure-helpers-test.sh` · `check-superseded-test.sh` · `check-superseded.sh .harness` · `run-gate-fixtures.sh` · `makerworld-fetch-test.sh` · `npx playwright test`)
  양성 대조: `BAMBU_GATE_SKILL=<스크립트-01 음성 대조 사본>` 을 주고 `ci-only.sh` 를 돌리면 `rc=1 bash bambu-kit/evals/run-gate-fixtures.sh` · `ci_only=14/15` (봉인 전 임시 트리 실측)
  기준값: 봉인 전 `$W` 와 임시 트리 모두 25 + SKIP 한 줄 · 15/15
