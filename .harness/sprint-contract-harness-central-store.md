---
feature: "하네스 기록을 프로젝트 저장소 밖 중앙 저장소로 — 바로가기 .harness 에서도 봉인 · 대조 · 감독 · init 이 돈다"
slug: harness-central-store
created: "2026-10-09 13:31"
complexity: "복잡"
conditions: 21
status: active
owner_session: c0c0aae7-8201-45fd-b1e1-338ea412ed57
conditions_digest: sha256:74af334948b909c0
measurement_digest: sha256:b971576adfe7e1b2
locked_at: "2026-10-09 13:35"
---

## 배경

- 2026-10-09 사용자 결정: 프로젝트 저장소에 `.harness/` 를 커밋하지 않는다. PC 하나에 하네스 저장소(`~/Hub/10_Dev/harness-store`, 깃허브 비공개)를 두고 프로젝트별 폴더를 넣는다. 프로젝트의 `.harness` 는 그 폴더로 가는 심볼릭 링크(바로가기)다.
- 이유: fit-pal 저장소에 `.harness` 아래 907 개(약 33MB)가 쌓였고, 앱 기록이 `chore(harness)` 커밋으로 덮였다. 무시 규칙을 둬도 강제 추가로 우회됐다.
- 봉인 대조(봉인 시점 원문을 깃에 남김)는 살린다. 깃 기록이 프로젝트 저장소가 아니라 하네스 저장소에 남을 뿐이다.
- 하네스가 계약 폴더를 찾는 규칙(위로 올라가며 처음 만나는 `.harness` 디렉토리)은 바꾸지 않는다. 바로가기도 디렉토리로 잡힌다.

## GAP 분석

봉인 전 실측(2026-10-09, 임시 폴더 `symtest`, 저장소 둘 + 바로가기):

- `git -C <계약 폴더> add <계약 절대경로>` → `fatal: ... is outside repository` (바로가기를 따라간 실제 저장소 기준으로 절대경로가 밖이다)
- 프로젝트 저장소에서 `git add .harness/sprint-contract-a.md` → `fatal: pathspec ... is beyond a symbolic link`
- `git -C <계약 폴더> add <파일 이름>` + `commit -o <파일 이름>` → 성공, `show --name-only` 가 `proj/sprint-contract-a.md` 한 줄
- 따라서 지금의 Step 6.7 (`git add "$CF"` · `git commit -o "$CF"`, 프로젝트 저장소 cwd)은 바로가기 모양에서 죽는다. qa-evaluator 1-e-3 의 `git log -- "$CONTRACT"` 도 같은 이유로 봉인 커밋을 못 찾는다.

Pre-Edit 감사(읽은 곳):

| 대상 | 증거 | 발견 | 조건 |
| --- | --- | --- | --- |
| sprint-contract SKILL | `harness/skills/sprint-contract/SKILL.md:828-848` | `git add "$CF"` · `git commit -o "$CF"` · 프로젝트 저장소 HEAD 를 셈 | 스킬-01 · 스킬-02 |
| qa-evaluator | `harness/agents/qa-evaluator.md:535-550` | `git log --diff-filter=A -- "$CONTRACT"` · `git show ... "$SEAL_COMMIT"` · `git diff "$SEAL_COMMIT" -- "$CONTRACT"` 모두 cwd 저장소 기준 | 스킬-03 |
| 계약 형식 문서 | `harness/references/contract-schema.md:306-320` | 봉인 커밋 절이 프로젝트 저장소 · 전용 가지 전제만 서술 | 구조-01 |
| 감독 스크립트 | `harness/scripts/codex-audit.sh:111-115` | `Path(contract).resolve()` 후 `meta.name != '.harness'` → 바로가기면 실제 폴더 이름이라 멈춤 | 스크립트-01 |
| 감독 스크립트 | `harness/scripts/codex-audit.sh:914` | `repo_root = git(meta.parent, 'rev-parse', '--show-toplevel')` → 풀린 경로면 하네스 저장소가 뿌리가 됨 | 스크립트-01 |
| 감독 스크립트 | `harness/scripts/codex-audit.sh:954-962` | 판정 사본은 프로젝트를 `git clone --shared` → 추적 안 된 `.harness` 가 사본에 없음. 사전 측정 `bash .harness/.meta/...` 가 죽음 | 스크립트-02 |
| init 스킬 | `harness/skills/init/SKILL.md:61` | 「`.gitignore` 에 `.harness/` 를 추가하지 마라」 | 스킬-04 |
| init 스크립트 | `harness/scripts/init.sh:15,28` | `HARNESS_DIR="$TARGET_DIR/.harness"` 실제 폴더만 만듦 | 스킬-04 · 오류-01 |
| commit-guard | `harness/scripts/commit-guard.sh:220-268` | 계약 폴더를 `-d` 로 찾고 `find "$1/.harness"` 로 계약을 읽음. `find` 는 시작점 바로가기를 따라간다 | 스크립트-03 |

기존 검사 기준값(2026-10-09, 이 가지 시작점 `608468d0`): `commit-guard-test.sh` · `qa-pending-check-test.sh` · `measure-helpers-test.sh` · `check-superseded-test.sh` 넷 다 종료 0 · `실패 0 건`. `python3 scripts/validate-plugin.py harness` 종료 0.

## 범위 경계

- 이번 계약은 플러그인만 고친다. 하네스 저장소 만들기 · 각 프로젝트 기록 옮기기 · fit-pal 추적 해제는 이 계약 밖(구현 뒤 별도 작업).
- 카이젠 자료 모으기(`kaizen-data-pool`)를 하네스 저장소로 돌리는 일은 이 계약 밖이다. 사용자 지시 「카이젠할 때 그거 참고해서 진행」은 다음 카이젠 회차에서 반영한다.
- 릴리스(`scripts/release.sh harness minor`)는 QA 통과 뒤 따로 한다.
- 이 저장소 자신의 `.harness` 를 옮기는 일은 이 계약 밖이다.

```text
# sprint-scope
harness/skills/sprint-contract/SKILL.md
harness/skills/init/SKILL.md
harness/agents/qa-evaluator.md
harness/references/contract-schema.md
harness/scripts/codex-audit.sh
harness/scripts/init.sh
harness/scripts/commit-guard.sh
harness/scripts/qa-pending-check.sh
harness/scripts/save-feedback.sh
harness/templates/codex-audit/
harness/evals/store/
harness/evals/hooks/commit-guard-test.sh
harness/README.md
harness/docs/
README.md
```

- 오라클 해소: 스킬-04 — 주 측정은 init.sh 를 실제로 돌리는 시험 사례 셋이고, grep 은 문서 문장이 바뀌었는지만 보는 보조 측정이다.

- 범위 밖: 실제 폴더 모양에서 `commit -o` 가 남의 스테이징을 삼키지 않는지(지금 동작 그대로) · 감독의 `models` 같은 하위 명령의 바로가기 동작 · 이미 `.harness` 가 있을 때 init 동작(지금처럼 멈춘다, 깨진 바로가기 포함 `-e` 또는 `-L` 이면 멈춘다).
- 구현 절차: 문서를 고친 뒤 `python3 scripts/sync-docs.py harness` 를 돌려 자동 블록을 맞춘다. harness README 의 손으로 쓴 절은 `<!-- AUTO:* -->` 블록 밖에 둔다.
- 기준값(2026-10-09, `608468d0`): `beyond a symbolic link` · `outside repository` · `HARNESS_STORE` 가 contract-schema.md · harness/README.md · init SKILL.md 에서 모두 0 건. contract-schema.md 변경 이력 항목(`^- \*\*v[0-9]`) 12 개, `^- \*\*v5\.8` 0 개.

공통 정의 — 시험 묶음: `bash harness/evals/store/harness-store-test.sh`. 사례마다 `PASS <사례 이름>` 또는 `FAIL <사례 이름>` 한 줄, 끝 줄 `실패 N 건`, 실패가 있으면 종료 1. 사례는 매번 임시 폴더에 프로젝트 저장소와 하네스 저장소를 새로 만든다. 「실제 폴더 모양」은 프로젝트 안 `.harness` 가 디렉토리이고 프로젝트 저장소에 커밋되는 모양, 「바로가기 모양」은 `.harness` 가 하네스 저장소 안 폴더로 가는 심볼릭 링크이고 프로젝트 `.gitignore` 에 `.harness` 가 있는 모양이다. 문서 안 코드 블록을 실행하는 사례는 블록을 손으로 베끼지 않고 파일에서 뽑는다 — 6.7 은 SKILL.md 의 `### 6.7.` 제목 아래 첫 ` ```bash ` 블록, 1-e-3 은 qa-evaluator.md 의 `#### 1-e-3.` 제목 아래 첫 ` ```bash ` 블록. 블록에 주는 입력은 실제 사용과 같게 계약 절대경로 하나(`CF` 또는 `CONTRACT`)와 `SLUG` 뿐이고 cwd 는 프로젝트 저장소 최상위다. 「되돌린 사본」은 해당 파일을 `git show 608468d0:<경로>` 로 꺼낸 원본으로 바꾼 사본이다.

## Skill

- [ ] 스킬-01: Given 두 모양 각각에서 계약 파일을 새로 쓴 상태, When sprint-contract Step 6.7 블록을 실행하면, Then 계약을 담은 저장소(실제 폴더 모양은 프로젝트, 바로가기 모양은 하네스 저장소)에 새 커밋이 하나 생기고 그 커밋의 파일은 계약 1 개이며 확인 줄이 `OK seal_commit files=1` 이다 [exact, enumerated]
  측정: 시험 묶음 출력에 `PASS seal:real` · `PASS seal:link`. 사례는 실행 전후 해당 저장소 `git rev-list --count HEAD` 가 1 늘었는지와 새 커밋의 `show --name-only` 가 계약 파일 이름 한 줄인지도 본다
  음성 대조: SKILL.md 를 원본으로 되돌린 사본에서 `FAIL seal:link`
- [ ] 스킬-02: Given 바로가기 모양에서 하네스 저장소가 `main` 가지에 있을 때, When Step 6.7 을 실행하면, Then 하네스 저장소 가지 이름이 실행 전과 같다(전용 가지를 만들지 않는다). 실제 폴더 모양에서는 지금처럼 프로젝트가 `main` 이면 `feat/<slug>` 로 옮기고, 이미 다른 가지면 그대로 둔다 [exact, enumerated]
  측정: 시험 묶음 `PASS seal:link-keeps-branch` · `PASS seal:real-main-branches` · `PASS seal:real-other-stays`
  음성 대조: 6.7 블록이 모양과 상관없이 `main` 이면 `checkout -b` 하도록 바꾼 사본에서 `FAIL seal:link-keeps-branch`
- [ ] 스킬-03: Given 스킬-01 로 봉인 커밋을 만든 두 모양, When qa-evaluator 1-e-3 블록을 계약 절대경로만 주고(cwd 프로젝트 최상위) 실행하면, Then `seal_commit=<해시> files=1` 이 나오고 `SEAL_COMMIT_ABSENT` 가 나오지 않는다. 봉인 뒤 앞머리 밖 본문 한 줄(`status:` 줄이 아님)을 고치면 그 줄이 산문 변경 출력에 나온다 [exact, enumerated]
  측정: 시험 묶음 `PASS verify:real` · `PASS verify:link` · `PASS verify:link-prose`
  음성 대조: qa-evaluator.md 를 원본으로 되돌린 사본에서 `FAIL verify:link`
- [ ] 스킬-04: Given 하네스 저장소 폴더(깃 저장소)를 환경변수 `HARNESS_STORE` 로 준 상태, When `init.sh <대상 폴더>` 를 실행하면, Then `<HARNESS_STORE>/<프로젝트 깃 최상위 폴더 이름>/<최상위에서 대상까지 상대 경로>` 폴더가 생기고 그 안에 `project.yaml` 이 있으며, 대상의 `.harness` 는 그 폴더로 가는 심볼릭 링크이고, 프로젝트 저장소에서 `git check-ignore -q <대상>/.harness` 가 종료 0 이다. `HARNESS_STORE` 가 없거나 빈 문자열이면 지금처럼 실제 폴더를 만든다 [exact, enumerated]
  측정: 시험 묶음 `PASS init:link` · `PASS init:link-subdir` · `PASS init:plain` · `PASS init:plain-empty-env`
  음성 대조: init.sh 를 원본으로 되돌린 사본에서 `FAIL init:link`
- [ ] 스킬-05: init SKILL.md 의 「`.gitignore` 에 `.harness/` 를 추가하지 마라」 문장(지금 61 행)이 없어지고, 대신 두 모양을 구분해 바로가기 모양에서는 `.harness` 를 무시하라는 안내가 있다 [exact]
  측정: `grep -cF '`.gitignore`에 `.harness/`를 추가하지 마라' harness/skills/init/SKILL.md` 가 0 (기준값 1) · `grep -c 'HARNESS_STORE' harness/skills/init/SKILL.md` ≥ 1 (기준값 0)

## Script

- [ ] 스크립트-01: Given 바로가기 모양의 계약 경로, When 감독 스크립트의 계약 위치 해석 `layout()` 과 프로젝트 뿌리 해석(이번에 `layout()` 반환값에 넣거나 따로 둔 함수 — 시험이 부르는 이름을 시험 파일 머리 주석에 적는다)을 부르면, Then 오류 없이 계약 폴더 이름이 `.harness` 이고 프로젝트 뿌리가 프로젝트 저장소 최상위다(하네스 저장소가 아니다). 실제 폴더 모양에서도 같은 값이다. 판정 경로(`impl`)가 차이를 재는 저장소도 이 뿌리를 쓴다 [exact, enumerated]
  측정: 시험 묶음 `PASS audit:layout-link` · `PASS audit:layout-real`. 시험은 codex-audit.sh 의 `<<'PY'` 본문을 뽑아 `__name__` 을 바꿔 불러 함수를 직접 부른다(Codex 호출 없음); `grep -n "rev-parse', '--show-toplevel'" harness/scripts/codex-audit.sh` 의 각 줄이 그 뿌리 값에서 출발함을 리포트에 줄 번호로 적는다
  음성 대조: codex-audit.sh 를 원본으로 되돌린 사본에서 `FAIL audit:layout-link` (원본은 `.resolve()` 로 바로가기를 풀어 멈춘다)
- [ ] 스크립트-02: Given 바로가기 모양이라 프로젝트 저장소가 `.harness` 를 추적하지 않을 때, When 감독이 판정 사본을 만들면, Then 사본 안 `.harness` 는 바로가기가 아닌 실제 폴더이고(판정 격리가 사본 밖을 못 읽으므로 복사한다), 사본의 `.harness/.meta/<slug>/measure.sh` 와 원래 계약 폴더의 같은 파일이 `cmp` 로 같다. 복사에서 그림 파일(`*.png` · `*.jpg` · `*.jpeg`)은 빼도 된다. 실제 폴더 모양(추적됨)에서는 지금처럼 사본에 커밋된 `.harness` 가 있다 [exact, enumerated]
  측정: 시험 묶음 `PASS audit:copy-link` (사본 `.harness` 에 `[ -d ] && [ ! -L ]` · `cmp` 종료 0) · `PASS audit:copy-real`. 사본을 만드는 함수가 시험에서 부를 수 있게 바깥에 있다
  음성 대조: codex-audit.sh 를 원본으로 되돌린 사본에서 `FAIL audit:copy-link`
- [ ] 스크립트-03: Given 바로가기 모양에서 이 세션 소유 활성 계약의 `# sprint-scope` 블록에 `src/` 만 있을 때, When `src/a.txt` 를 커밋하면 commit-guard 가 통과시키고 `docs/b.txt` 를 커밋하면 범위 밖으로 막는다(훅을 고쳐야 하든 아니든 이 결과면 된다) [exact, enumerated]
  측정: `bash harness/evals/hooks/commit-guard-test.sh` 출력에 이름에 `link` 가 든 새 사례 두 줄이 PASS
  음성 대조: commit-guard.sh 의 계약 폴더 찾기가 심볼릭 링크를 건너뛰게(`[ -d ] && [ ! -L ]`) 바꾼 사본에서 `link` 차단 사례가 FAIL

## Error

- [ ] 오류-01: Given `HARNESS_STORE` 가 깃 저장소가 아닌 폴더이거나 없는 경로일 때, When `init.sh` 를 실행하면, Then 0 이 아닌 종료 코드와 원인을 적은 한국어 한 줄을 내고, 실행 뒤 `[ ! -e 대상/.harness ] && [ ! -L 대상/.harness ]` 가 참이다 [exact, enumerated]
  측정: 시험 묶음 `PASS init:store-not-git` · `PASS init:store-missing`
- [ ] 오류-02: Given 바로가기 모양에서 하네스 저장소의 마지막 커밋이 일부러 파일 1 개짜리이고 `index.lock` 이 남아 있을 때, When Step 6.7 을 실행하면, Then 커밋 단계가 실패한 것을 보고 확인 줄이 `BLOCKED` 로 시작하며 `OK seal_commit` 이 나오지 않는다(직전 커밋을 보고 거짓 OK 를 내지 않는다). 실제 폴더 모양도 같다 [exact, enumerated]
  측정: 시험 묶음 `PASS seal:link-locked` · `PASS seal:real-locked`
  음성 대조: SKILL.md 를 원본으로 되돌린 사본에서 `FAIL seal:real-locked` (원본은 커밋 실패 뒤에도 HEAD 를 센다)

## Architecture

- [ ] 구조-01: contract-schema.md 봉인 커밋 절이 두 모양(프로젝트 안 실제 폴더 · 하네스 저장소 바로가기)을 모두 적고, 깃 명령은 계약 폴더로 들어가 파일 이름으로 부른다는 규칙과 실측 오류 두 줄을 적으며, 변경 이력에 v5.8 항목이 하나 더해진다 [structural, enumerated]
  측정: contract-schema.md 에서 `grep -c 'beyond a symbolic link'` ≥ 1 · `grep -c 'outside repository'` ≥ 1 · `grep -c 'HARNESS_STORE'` ≥ 1 (기준값 셋 다 0) · `grep -c '^- \*\*v[0-9]'` = 13 (기준값 12) · `grep -c '^- \*\*v5\.8'` = 1
- [ ] 구조-02: 새 시험 묶음과 기존 검사가 모두 통과한다 — `harness-store-test.sh` · `commit-guard-test.sh` · `qa-pending-check-test.sh` · `measure-helpers-test.sh` · `check-superseded-test.sh` 종료 0 · 끝 줄 `실패 0 건`, `python3 scripts/validate-plugin.py harness` 종료 0, `python3 scripts/sync-docs.py --check-only` 종료 0 [exact, enumerated]
  측정: 일곱 명령을 차례로 실행해 종료 코드와 끝 줄을 적는다. 시험 묶음의 사례 이름 목록(`grep -oE '(PASS|FAIL) [a-z:-]+'`)에 이 계약이 적은 사례 20 개가 모두 있다
  음성 대조: 스킬-01 · 스킬-03 · 스킬-04 · 스크립트-01 · 스크립트-02 의 되돌린 사본으로 묶음을 돌렸을 때 각 조건이 적은 `FAIL` 줄이 나온다
- [ ] 구조-03: harness README 에 하네스 저장소 모양을 설명하는 절이 하나 있고, 그 절이 `HARNESS_STORE` · 심볼릭 링크(바로가기) · 프로젝트 `.gitignore` 의 `.harness` · 봉인 커밋이 하네스 저장소에 남는다는 것 네 가지를 모두 적는다 [structural, enumerated]
  측정: `grep -n '^##.*하네스 저장소' harness/README.md` 1 줄 이상, 그 절 안(다음 `## ` 전까지)에서 `HARNESS_STORE` · `심볼릭 링크` · `.gitignore` · `봉인 커밋` 네 낱말이 각각 1 건 이상, 그 절이 `<!-- AUTO:` 블록 밖

## Anti-patterns

- [ ] 금지-02: force push 금지
- [ ] 금지-03: bare code fence 금지 — `python3 scripts/validate-plugin.py --check=code-fence` 종료 0

## Reusability

- [ ] 재사용-01: 다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다
- [ ] 재사용-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다

## Diagnostics

- [ ] 진단-01: N/A (commands.analyze 는 `bash -n scripts/release.sh` 만 잰다 — 이번 범위에 scripts/release.sh 가 없다. 대신 구조-02)
- [ ] 진단-02: 이번에 바꾼 셸 스크립트(`harness/scripts/init.sh` · `harness/scripts/commit-guard.sh` · `harness/evals/store/harness-store-test.sh` · `harness/evals/hooks/commit-guard-test.sh`)가 `bash -n` 종료 0 이고, `harness/scripts/codex-audit.sh` 의 `<<'PY'` 본문을 뽑아 `python3 -m py_compile` 종료 0
- [ ] 진단-03: N/A (commands.test 도 scripts/release.sh 만 돈다 — 대신 구조-02)
- [ ] 진단-04: N/A (구동할 앱 · 서버 없음 — 셸 스크립트와 문서. 실제 동작은 구조-02 의 시험 묶음이 임시 저장소에서 돌린다)
