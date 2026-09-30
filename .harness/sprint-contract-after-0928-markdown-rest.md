---
feature: "마크다운 남은 경고 · 깨진 코드 블록 · 목록 · 밀린 줄 참조 (A1 · B18 · B19 · B20)"
slug: after-0928-markdown-rest
created: "2026-09-28 12:33"
complexity: "복잡"
conditions: 28
status: superseded
superseded_by: after-0928-markdown-rest-r2
owner_session: bda55d45-296c-491f-89ba-b52042d58e72
conditions_digest: sha256:fce06290475f8679
measurement_digest: sha256:aabae5a87f521872
locked_at: "2026-09-28 12:43"
---

## 배경

- 남은 일 목록 `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0928/.harness/.meta/after-kaizen-0928/remaining.md` 의 A1 · B18 · B19 · B20. 결정 기록은 같은 폴더 `decisions.md` — B20 가운데 `.harness` 안 기록은 묶음 rec 몫이라 여기서 다루지 않는다.
- 사용자 위임: 2026-09-27T01:22:01.089Z 「자동으로 다 진행해 나한테 묻지 말고 …」 · 2026-09-28 「약점과 일부만 한 거 다처리하지??」 (세션 bda55d45-296c-491f-89ba-b52042d58e72).
- 기준 판(이하 BASE): `e500a63` (가지 `chore/ak3-lt` 를 만든 시점). 끝 판(이하 TIP): 모든 커밋이 끝난 뒤 `git rev-parse chore/ak3-lt` 의 출력. `HEAD` 를 쓰지 않는다. 경고 정리 전 판: `c3e45f3`.
- 기록 파일(이하 notes): `.harness/.meta/after-kaizen-0928/lt-notes.md` (앞 묶음 `ex-notes.md` 와 같은 자리).
- 측정 묶음(이하 M): `.harness/.meta/after-0928-markdown-rest/` — 봉인 커밋과 따로 커밋한다. 파일과 sha256 앞 16 자리는 SC-01 에 적었다.
- 경고를 재는 도구: 세션 scratch 의 `mdlint/run.sh` (markdownlint-cli2 0.23.2 · markdownlint 0.41.1, 설정 `{ "config": { "MD013": false } }` — 편집기와 같다). 추적되는 `.md` 가운데 `.harness/` 밖 파일을 잰다.
- 그려진 모양을 재는 도구: 같은 scratch 의 markdown-it 14.3.0 (`mdlint/node_modules`). 편집기 미리보기처럼 CommonMark 로 그린다.
- 공통 정의 (모든 측정 앞에 같은 셸에서 한 번 실행한다. zsh · bash 같은 결과):

```bash
W=/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak3-lt; cd "$W" || exit 2
SCR=/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/bda55d45-296c-491f-89ba-b52042d58e72/scratchpad
RUN=$SCR/mdlint/run.sh; export MDIT_DIR=$SCR/mdlint/node_modules
M=.harness/.meta/after-0928-markdown-rest; N=.harness/.meta/after-kaizen-0928/lt-notes.md
BASE=e500a63; TIP=$(git rev-parse chore/ak3-lt) || exit 2
```

- 모든 조건의 공통 전제: 모든 커밋이 끝났고 `git status --porcelain --untracked-files=no | grep -c .` 이 0 이다 (작업 폴더 = TIP).
- 이 스프린트의 판단: 목록 안 코드 블록을 촘촘하게 두면 MD031(코드 블록 앞뒤 빈 줄)이 경고를 낸다. 설정을 편집기와 같게 두므로 B19 는 코드 블록 앞뒤에 `<!-- markdownlint-disable-next-line MD031 -->` 한 줄씩을 항목 들여쓰기에 맞춰 넣는 것만 허용한다. 빈 줄 없이 넣으면 목록이 촘촘하게 그려지고 경고가 0 이 된다 (scratch `lt-try/h.md` 실측). B18 은 경고를 끄지 않고 울타리를 고친다.

## GAP 분석

| 항목 | BASE 실측 (2026-09-28) | 조건 |
| --- | --- | --- |
| A1 | run.sh 경고 267 건 · 29 파일. 시험 입력 21 파일(`evals/` 아래 fixture — `harness/evals/test-fixtures/README.md` 절차와 `howto-kit/evals/evals.json` · `onboarding-kit/skills/setup-guide/evals/evals.json` 이 연다) 90 건을 빼면 8 파일 177 건: bambu SKILL 120 · api-ui SKILL 25 · howto README 18 · contract-schema 8 · visual-change-protocol 2 · setup-guide SKILL 2 · howto-audit SKILL 1 · howto-doc SKILL 1 | SK-01 · SK-02 · SK-03 |
| B18 | markdown-it 로 그리면 울타리 짝이 깨진 파일은 9 개다: 목록의 일곱 가운데 `.claude/skills/react-kaizen/SKILL.md` · `harness/skills/sprint-contract/SKILL.md` 는 fence-check 의 삼킨 줄 · 안 닫힘 · 뼈대 줄 · 콜론 끝 · 빈 블록 다섯 칸이 0 이다 (sprint-contract 의 텍스트 머리 1 은 마크다운 틀 예시라 깨짐이 아니다), 목록에 없던 `docs/superpowers/plans/2026-03-30-widget-inspector.md` · `2026-04-06-rust-kit.md` 가 깨져 있다. 바깥 블록이 안쪽 울타리에서 먼저 닫힌 자리 28 곳 (sites.tsv). 울타리를 끄던 block 꼴 주석 짝은 per-project 135/385 · harness-kaizen 424/634 · design-kit 1445/1576 · kaizen-self 113/274 · new-skills 45/168 · 601/694 이고, 고치면 코드 블록 안에 들어가는 주석 짝이 design-kit 561/565 · 1189/1195 · new-skills 309/313 · 527/531 · widget-inspector 279/292 다 | SK-04 · SK-05 · SK-06 · SK-07 |
| B19 | `c3e45f3` 와 BASE 를 그려 맞대면 9 파일에서 목록 11 개가 촘촘함에서 느슨함으로 바뀌었고, `infra-kit/skills/infra-audit/SKILL.md` 는 들여쓰지 않은 주석 줄이 목록을 둘로 끊었다 (목록 수 6 → 7). 합 10 파일. `react-kaizen` 4 번 항목은 `c3e45f3` 에서도 이미 느슨해 바뀐 것이 없다 | SK-08 · SK-09 |
| B20 | ref-shift.py: `.harness/` 밖 md 의 `경로:줄` 참조 가운데 git 줄 대응으로 밀린 것이 40 (끝 기준). `.claude/kaizen-input/` 13 은 다른 프로젝트 `.harness` 기록을 2026-04-24 에 떠 온 사본이라 뺀다. 남은 27 가운데 `docs/howto/design-brief.md:23` 의 `qa-evaluation-guide.md:1009-1013` 과 `:370` 의 `…:1004-1013` 은 대상 줄이 지워져(GONE) 따라갈 수 없다. 고칠 수 있는 참조 23 곳 + 같은 참조를 싣는 페이지 셋 (`docs/backend-kit/research-log.html` · `docs/howto-kit/overview.html` · `docs/harness/plugin-validation.html`) — ref-expect.tsv 33 줄 · 31 묶음 | SK-10 · SK-11 |

## 범위 경계

- 하지 않는 것: `.harness/` 아래 봉인된 계약 · QA 리포트 · 개정 파일과 `.harness/.meta` 의 지난 기록. B20 의 `.harness` 520 곳은 묶음 rec 몫이다 (decisions.md).
- 하지 않는 것: A1 의 시험 입력 21 파일 (`$M/a1-excluded.txt`). 시험이 그 글자 그대로를 입력으로 쓴다 — 고치면 시험 뜻이 바뀐다. 파일마다 이유를 notes 에 적는다 (SK-02).
- 하지 않는 것: `.claude/kaizen-input/` 의 줄 참조 13 곳 (봉인 기록 사본). `docs/howto/design-brief.md:23` · `:370` 의 범위 참조 둘 (대상 줄이 지워져 git 으로 따라갈 수 없다). notes 에 적는다 (SK-11).
- 하지 않는 것: `.claude/skills/react-kaizen/SKILL.md` 의 울타리 · 4 번 항목 — 깨진 것이 없고 `c3e45f3` 와 모양이 같다. 근거를 notes 에 적는다. `harness/skills/sprint-contract/SKILL.md` 도 울타리는 멀쩡하고 B19 목록 두 곳만 고친다.
- 하지 않는 것: 울타리 검사를 저장소 CI 에 새로 넣는 일. 측정 묶음은 이 계약의 판정용이고 CI 에는 markdown-it 가 없다. 새 저장소 검사를 만들지 않으므로 CI 등록 대상이 없다 (RE-02).
- 조건 수: 기능 조건 20 개 — 복잡 상한과 같다. 네 항목이 한 묶음으로 배정됐고 킷별 커밋(AR-01)으로 이미 나뉜다.
- 오라클 해소: SK-04 · SK-05 · SK-08 · SK-10 은 새로 짠 스크립트라 BASE 값(양성 대조)과 알려진 답을 조건에 적었다. SK-06 · SK-09 · ER-01 의 line-kinds 는 scratch 사본(`lt-try/dk/q2.md`)으로 1 이상이 나오는 것을 봉인 전에 확인했다.
- 오라클 해소: SK-02 · SK-03 · ER-02 — notes 를 찾는 grep 은 「기록이 있는가」 를 재는 것이 조건의 뜻이다. 기록할 목록(뺀 파일 · 글이 바뀐 줄 · 끈 줄)은 실행한 명령(`a1-excluded.txt` · line-kinds 출력)이 만든다. SK-04 · AR-02 — 측정이 fence-check 실행 결과 · git diff 출력을 재며 문서 서술을 찾지 않는다(검출기 오탐).
- 오라클 해소: SC-03 — 판정은 `check-docs-a11y.js` 가 브라우저로 페이지를 실제로 그려 낸 결과다. `assets/site.css` grep 은 docs-site 규칙(공통 CSS 링크 하나)을 재는 것이 뜻이다.
- 교차 진단 반영: SK-04 가 fence-check 5 열(텍스트 머리 — 코드 블록 첫 줄이 마크다운 제목처럼 보이는 수)을 합에서 빼는 것은 의도다. 마크다운 틀을 보여 주는 예시 블록(`sprint-contract/SKILL.md` 의 계약 틀 등)은 제목 줄로 시작하는 것이 정상이라 깨짐의 표시가 아니다. 깨짐은 나머지 다섯 칸이 잡는다.
- 커버리지 해소: AR-02 — 검출기가 짚은 `.harness/` 는 제외 경로, `CF=…` 는 측정 변수 정의라 대상이 아니다.
- 범위 목록 (이 밖의 경로를 담은 커밋은 막힌다):

```text
# sprint-scope
.claude/kaizen-input/per-project-feedback.md
.claude/skills/docs-site/SKILL.md
docs/onboarding-kit/plan-2026-05-18.md
docs/react/kit-design/final-integration.md
docs/superpowers/
docs/backend/research-log.md
docs/backend-kit/research-log.html
docs/howto/design-brief.md
docs/howto-kit/overview.html
docs/harness/plugin-validation.html
docs/harness/contract-schema.html
docs/design-kit/visual-change-protocol.html
docs/bambu-kit/bambu-print-profile.html
docs/onboarding-kit/setup-guide.html
api-kit/skills/api-ui/SKILL.md
bambu-kit/skills/bambu-print-profile/SKILL.md
bambu-kit/skills/bambu-print-profile/references/comment-analysis.md
design-kit/references/visual-change-protocol.md
design-kit/skills/design-system/SKILL.md
harness/references/contract-schema.md
harness/skills/sprint-contract/SKILL.md
harness/docs/guides/plugin-validation-guide.md
howto-kit/README.md
howto-kit/skills/howto-audit/SKILL.md
howto-kit/skills/howto-doc/SKILL.md
onboarding-kit/skills/setup-guide/SKILL.md
flutter-toolkit/skills/flutter-hooks/SKILL.md
flutter-toolkit/skills/flutter-kaizen/SKILL.md
infra-kit/skills/infra-audit/SKILL.md
react-kit/skills/react-skeleton/SKILL.md
reflect-kit/skills/reflect-digest/SKILL.md
reflect-kit/skills/reflect-promote/SKILL.md
rust-kit/skills/rust-docker/SKILL.md
```

## 회귀 게이트

- BASE 실측(2026-09-28, `TMPDIR` 은 scratch `lt-ci/tmp`): `ci-local.sh` 단계 전부 rc=0 · `feedback-agg-test SKIP (yq 없음)` 1 줄. CI 파일에만 있는 단계와 킷 시험 아홉(`check-api-kit-docs` · `detect-docs-drift --check-table` · `check-cause-table-copies` · `check-reviewer-protocol-copies` · `measure-helpers-test` · `bambu-kit/evals/run-gate-fixtures.sh` · `bambu-kit/evals/makerworld-fetch-test.sh` · `design-kit/evals/decision-gate-test.sh` · `npx playwright test api-kit/evals/`)은 SC-02 에 적은 값이다.
- BASE 실측: `python3 scripts/validate-plugin.py --check=code-fence` · `--check=frontmatter` 둘 다 `Total: 14 plugins, 14 OK`, rc=0.
- BASE 실측: `.harness` 계약 봉인 `bash $M/seal-count.sh $W` → `11 SEAL_ABSENT` · `118 SEAL_OK`. 양성 대조: 봉인된 계약 사본의 조건 한 줄을 바꾼 scratch 폴더는 `1 SEAL_BROKEN`.

## Skill

- [ ] SK-01: (A1) 레포 전체 마크다운 경고 가운데 시험 입력 21 파일을 뺀 수가 0 이고, 시험 입력 21 파일의 경고 수는 BASE 와 같은 90 이다 [exact, enumerated]
  Given: 공통 정의 뒤.
  측정: `bash $RUN $W | awk -F: 'NR==FNR{x[$0];next} !($1 in x)' $M/a1-excluded.txt - | grep -c .` 이 0. 같은 출력에서 `($1 in x)` 인 줄 수가 90 (검사기가 실제로 돌았다는 표시).
  양성 대조: BASE 에서 첫 명령은 177, 둘째는 90 (2026-09-28 실측).
  측정 대상: `api-kit/skills/api-ui/SKILL.md` · `bambu-kit/skills/bambu-print-profile/SKILL.md` · `design-kit/references/visual-change-protocol.md` · `harness/references/contract-schema.md` · `howto-kit/README.md` · `howto-kit/skills/howto-audit/SKILL.md` · `howto-kit/skills/howto-doc/SKILL.md` · `onboarding-kit/skills/setup-guide/SKILL.md` 여덟이 BASE 의 177 건 전부를 낸다.
- [ ] SK-02: (A1) 뺀 시험 입력 21 파일이 BASE 와 글자 하나 다르지 않고, notes 가 21 경로를 하나씩 이유와 함께 적는다 [exact, enumerated]
  Given: 공통 정의 뒤.
  측정: `git diff --name-only $BASE $TIP -- $(cat $M/a1-excluded.txt) | grep -c .` 이 0. `git cat-file -e $TIP:$N` 종료 코드 0. `while read p; do git show $TIP:$N | grep -F -- "$p" | grep -cF '시험 입력'; done < $M/a1-excluded.txt` 의 21 줄이 모두 1 이상.
  양성 대조: BASE 에 notes 가 없어 `git cat-file -e $BASE:$N` 은 종료 코드 128.
- [ ] SK-03: (A1) 여덟 파일의 경고 정리가 그려진 모양을 바꾸지 않고, 글이 바뀐 줄은 notes 에 모두 적힌다 [exact, enumerated]
  Given: 공통 정의 뒤.
  측정: `bash $M/shape-run.sh $W $BASE $TIP $M/a1-files.txt | tail -1` 이 `TOTAL	0	0	0` (탭 구분 — 목록 촘촘함 차이 0 · 목록 · 인용 · 표 · 코드 블록 수 차이 0 · 없는 판 0). 이어서 `git diff -U0 -w --ignore-blank-lines $BASE $TIP -- $(cat $M/a1-files.txt) | python3 $M/line-kinds.py | awk -F'\t' '$1=="OTHER" && $3=="+"{print $2}'` 이 내는 `경로:줄` 마다 `git show $TIP:$N | grep -cE "<경로>:<줄>([^0-9]|$)"` 이 1 이상.
  양성 대조: 같은 shape-run 을 `c3e45f3` 와 BASE 사이 B19 열 파일(`$M/b19-files.txt`)에 돌리면 `TOTAL	11	1	0` (2026-09-28 실측). line-kinds 는 scratch `lt-try/dk/q2.md`(낱말 하나를 바꾼 사본)에서 OTHER 2 줄.
- [ ] SK-04: (B18) 깨졌던 아홉 파일에서 울타리 짝이 깨진 흔적 다섯 가지가 모두 0 이고, 레포 전체에서 삼킨 줄과 안 닫힌 블록이 0 이다 [exact, enumerated]
  Given: 공통 정의 뒤.
  측정: `node $M/fence-check.mjs $(cat $M/b18-files.txt) | awk -F'\t' '$1!="TOTAL" && ($2+$3+$4+$6+$7)>0' | grep -c .` 이 0 이고 파일 줄이 9 개. 칸은 swallowed · unclosed · leak · mdcolon · empty (2 · 3 · 4 · 6 · 7 열). `node $M/fence-check.mjs $(git ls-files '*.md' | grep -v '^\.harness/') | tail -1` 의 2 · 3 열이 0 · 0.
  양성 대조: BASE 에서 첫 명령은 9 (아홉 파일 모두 1 이상), 둘째 명령 끝 줄은 `TOTAL	19	1	10	94	13	4	2328`.
  측정 대상: `.claude/kaizen-input/per-project-feedback.md` · `docs/onboarding-kit/plan-2026-05-18.md` · `docs/react/kit-design/final-integration.md` · `docs/superpowers/plans/2026-03-29-harness-kaizen.md` · `docs/superpowers/plans/2026-03-30-design-kit.md` · `docs/superpowers/plans/2026-03-30-kaizen-self-improvement.md` · `docs/superpowers/plans/2026-03-30-widget-inspector.md` · `docs/superpowers/plans/2026-04-06-design-kit-new-skills.md` · `docs/superpowers/plans/2026-04-06-rust-kit.md`
- [ ] SK-05: (B18) 바깥 코드 블록 28 곳이 각각 하나의 블록으로 그려져 처음 줄부터 끝 줄까지 담고, 바로 다음 본문 줄은 코드 블록 밖에 있다 [exact, enumerated]
  Given: 공통 정의 뒤.
  측정: `node $M/site-check.mjs $M/sites.tsv; echo rc=$?` 의 끝 두 줄이 `SITES	28	28` 과 `rc=0`. `FAIL` · `BADANCHOR` 줄 0.
  양성 대조: BASE 에서 `SITES	28	1` · rc=1 (harness-kaizen 첫 자리는 바깥 끝이 안쪽 닫는 줄과 붙어 있어 BASE 에서도 OK — 그 자리의 깨짐은 SK-04 swallowed 가 잡는다).
  알려진 답: design-kit 계획 사본에서 일곱 자리의 바깥 울타리를 백틱 넷으로 바꾸고 안쪽 여닫이를 바로잡은 scratch `lt-try/dk/q.md` 는 `SITES	7	7` · rc=0, fence-check 다섯 칸 0 (2026-09-28 실측).
- [ ] SK-06: (B18) 아홉 파일에서 바뀐 줄은 울타리 줄 · markdownlint 주석 줄 · 빈 줄뿐이다 — 코드 블록 안 글과 본문 글은 한 글자도 바뀌지 않는다 [exact, enumerated]
  Given: 공통 정의 뒤.
  측정: `git diff -U0 $BASE $TIP -- $(cat $M/b18-files.txt) | python3 $M/line-kinds.py | tail -1` 의 5 열(other)이 0.
  양성 대조: `git diff --no-index -U0 docs/superpowers/plans/2026-03-30-design-kit.md $SCR/lt-try/dk/q2.md | python3 $M/line-kinds.py | tail -1` 은 `TOTAL	50	7	0	2	1` (other 2).
- [ ] SK-07: (B18) 울타리 구간을 끄던 block 꼴 주석과 고치면 코드 블록 안에 들어가는 block 꼴 주석이 사라지고, 남는 block 꼴 주석은 과제 제목 단계(MD001) 짝뿐이다 [exact, enumerated]
  Given: 공통 정의 뒤.
  측정: 파일마다 `grep -cE 'markdownlint-(disable|enable) ' <파일>` 이 per-project-feedback 0 · harness-kaizen 0 · design-kit 2 · kaizen-self-improvement 0 · widget-inspector 0 · design-kit-new-skills 6 · plan-2026-05-18 0 · final-integration 0 · rust-kit 0. design-kit 와 design-kit-new-skills 에서 `grep -E 'markdownlint-(disable|enable) ' <파일> | grep -vcE ' MD001 -->$'` 이 0.
  양성 대조: BASE 에서 같은 순서로 2 · 2 · 8 · 2 · 2 · 14 · 0 · 0 · 0.
  측정 대상: `.claude/kaizen-input/per-project-feedback.md` · `docs/superpowers/plans/2026-03-29-harness-kaizen.md` · `docs/superpowers/plans/2026-03-30-design-kit.md` · `docs/superpowers/plans/2026-03-30-kaizen-self-improvement.md` · `docs/superpowers/plans/2026-03-30-widget-inspector.md` · `docs/superpowers/plans/2026-04-06-design-kit-new-skills.md` · `docs/onboarding-kit/plan-2026-05-18.md` · `docs/react/kit-design/final-integration.md` · `docs/superpowers/plans/2026-04-06-rust-kit.md`
- [ ] SK-08: (B19) 열 파일의 목록이 경고 정리 전 판 `c3e45f3` 과 같은 모양으로 그려지고, 레포 전체(B18 아홉 파일 제외)에서도 촘촘함이 바뀐 목록이 0 이다 [exact, enumerated]
  Given: 공통 정의 뒤.
  측정: `bash $M/shape-run.sh $W c3e45f3 $TIP $M/b19-files.txt` 의 파일 줄 10 개가 모두 2 · 3 열 0 이고 끝 줄이 `TOTAL	0	0	0`. `git diff --name-only c3e45f3 $TIP -- '*.md' ':(exclude).harness' | awk 'NR==FNR{x[$0];next} !($0 in x)' $M/b18-files.txt - > $SCR/lt-wide.txt; bash $M/shape-run.sh $W c3e45f3 $TIP $SCR/lt-wide.txt | tail -1` 의 2 열이 0.
  양성 대조: TIP 대신 BASE 를 넣으면 첫 명령 끝 줄 `TOTAL	11	1	0`, 둘째 명령 2 열 11 (2026-09-28 실측).
  측정 대상: `.claude/skills/docs-site/SKILL.md` · `bambu-kit/skills/bambu-print-profile/references/comment-analysis.md` · `flutter-toolkit/skills/flutter-hooks/SKILL.md` · `flutter-toolkit/skills/flutter-kaizen/SKILL.md` · `harness/skills/sprint-contract/SKILL.md` · `infra-kit/skills/infra-audit/SKILL.md` · `react-kit/skills/react-skeleton/SKILL.md` · `reflect-kit/skills/reflect-digest/SKILL.md` · `reflect-kit/skills/reflect-promote/SKILL.md` · `rust-kit/skills/rust-docker/SKILL.md`
- [ ] SK-09: (B19) 열 파일에서 바뀐 줄은 markdownlint 주석 줄과 빈 줄뿐이다 [exact, enumerated]
  Given: 공통 정의 뒤.
  측정: `git diff -U0 $BASE $TIP -- $(cat $M/b19-files.txt) | python3 $M/line-kinds.py | tail -1` 의 2 열(fence) 0 · 5 열(other) 0.
  양성 대조: SK-06 의 q2 사본 대조가 other 2 를 낸다.
- [ ] SK-10: (B20) 밀린 줄 참조 23 곳과 그 참조를 싣는 페이지 세 곳이 git 줄 대응으로 맞는 줄을 가리킨다 — ref-expect.tsv 31 묶음 전부 OK [exact, enumerated]
  Given: 공통 정의 뒤.
  측정: `python3 $M/ref-check.py $W $M/ref-expect.tsv $BASE $TIP; echo rc=$?` 의 끝 두 줄이 `REFS	31	31` 과 `rc=0`.
  양성 대조: `python3 $M/ref-check.py $W $M/ref-expect.tsv $BASE $BASE` 는 `REFS	31	0` · rc=1.
  알려진 답: scratch 복제본 `lt-clone` 에서 `design-kit/skills/design-system/SKILL.md` 의 `material-design.md:273` 만 `281` 로 바꿔 커밋하면 그 묶음 하나만 OK (`REFS	31	1`, 2026-09-28 실측).
  측정 대상: `design-kit/skills/design-system/SKILL.md` · `docs/backend/research-log.md` · `docs/backend-kit/research-log.html` · `docs/howto/design-brief.md` · `docs/howto-kit/overview.html` · `docs/superpowers/followup-2026-04-11-plugin-validation-findings.md` · `docs/superpowers/specs/2026-04-07-design-kit-templates-docs-design.md` · `harness/docs/guides/plugin-validation-guide.md` · `docs/harness/plugin-validation.html`
- [ ] SK-11: (B20 · B18) notes 가 고치지 않은 것 넷을 경로와 이유로 적는다 — `.claude/kaizen-input/` 줄 참조 · `docs/howto/design-brief.md:23` · `docs/howto/design-brief.md:370` · 울타리가 멀쩡한 `.claude/skills/react-kaizen/SKILL.md` [exact, enumerated]
  Given: 공통 정의 뒤.
  측정: 네 문자열 `.claude/kaizen-input/` · `docs/howto/design-brief.md:23` · `docs/howto/design-brief.md:370` · `.claude/skills/react-kaizen/SKILL.md` 마다 `git show $TIP:$N | grep -cF -- '<문자열>'` 이 1 이상. `git diff --name-only $BASE $TIP -- .claude/kaizen-input | grep -vcxF .claude/kaizen-input/per-project-feedback.md` 이 0.
  양성 대조: BASE 에 notes 가 없다 (SK-02).

## Script

- [ ] SC-01: 측정 묶음 열네 파일이 TIP 에 커밋돼 있고 sha256 앞 16 자리가 봉인 때 값과 같다 [exact, enumerated]
  Given: 공통 정의 뒤.
  측정: 파일마다 `git show $TIP:<경로> | shasum -a 256 | cut -c1-16` 이 아래 값. 바깥 도구 둘은 `shasum -a 256 <경로> | cut -c1-16`.
  `$M/fence-check.mjs` c407e418925c108c · `$M/list-shape.mjs` d631962c8ed507d3 · `$M/site-check.mjs` 5617a66beaafcdeb · `$M/line-kinds.py` 5104458b2f384b0d · `$M/ref-check.py` 906521acc93512cb · `$M/ref-shift.py` 2cdae7b104766b36 · `$M/shape-run.sh` 493980894fcb92bb · `$M/seal-count.sh` bbed7b2433ac609d · `$M/a1-excluded.txt` b3565bc94d6803fd · `$M/a1-files.txt` 508713ec58e2d96e · `$M/b18-files.txt` b2a816b76cd60e8f · `$M/b19-files.txt` e902842c6678d587 · `$M/ref-expect.tsv` 1c35698719d00401 · `$M/sites.tsv` ae792ebbc4dc9a51 · `$SCR/mdlint/run.sh` e1c237a6a876ad33 · `$SCR/mdlint/cfg.jsonc` dfe13e2d516b31e5
- [ ] SC-02: 로컬 CI 와 CI 파일에만 있는 단계 · 킷 시험이 TIP 에서 BASE 와 같게 통과한다 [exact, enumerated]
  Given: 공통 정의 뒤. `TMPDIR` 을 scratch 아래 새 폴더로.
  측정: `bash /Users/jackson/Hub/10_Dev/claude-plugins/.harness/handoff/2026-09-26-tools/ci-local.sh $W` 의 요약에서 `rc=` 줄이 모두 `rc=0` 이고 `SKIP` 줄은 `feedback-agg-test SKIP (yq 없음)` 하나. 아홉 명령 `python3 scripts/check-api-kit-docs.py` · `python3 scripts/detect-docs-drift.py --check-table` · `python3 scripts/check-cause-table-copies.py` · `python3 scripts/check-reviewer-protocol-copies.py` · `bash harness/evals/measure/measure-helpers-test.sh` · `bash bambu-kit/evals/run-gate-fixtures.sh` · `bash bambu-kit/evals/makerworld-fetch-test.sh` · `bash design-kit/evals/decision-gate-test.sh` · `npx playwright test api-kit/evals/` 의 종료 코드가 모두 0 (BASE 실측 아홉 모두 0, 2026-09-28).
  음성 대조: `design-kit/evals/decision-gate-test.sh` 는 visual-change-protocol.md §6 코드를 떼어 돌린다 — 그 python 블록 머리 줄을 지운 사본을 `DECISION_GATE_DOC` 로 주면 「검사 코드를 못 뗐다」 · 종료 코드 2.
- [ ] SC-03: 바뀐 docs 페이지가 접근성 검사를 통과한다 — 가로 넘침(320 · 375 · 768 · 1280) 0 · 콘솔 에러 0 · 대비 · 터치 크기 [exact, enumerated]
  Given: 공통 정의 뒤.
  측정: `P=$(git diff --name-only $BASE $TIP -- 'docs/*.html'); node scripts/check-docs-a11y.js $P | tail -1` 이 `<k>/<k> PASS` 이고 k 는 `printf '%s\n' $P | grep -c .` 와 같으며 1 이상 (SK-10 의 세 페이지가 바뀐다). 바뀐 페이지마다 `grep -c 'assets/site.css' <페이지>` 이 1.
  양성 대조: BASE 에서 범위 목록의 일곱 페이지는 `7/7 PASS` · 세 페이지의 공통 CSS 링크 각 1. 너비 2000px 요소를 붙인 `research-log.html` 사본은 `FAIL … of=1680/1625/1232/720` · `0/1 PASS` (2026-09-28 실측).

## Error

- [ ] ER-01: BASE 에서 TIP 까지 더한 줄 가운데 block 꼴 markdownlint 지시(`markdownlint-disable ` · `markdownlint-enable ` — next-line 이 아닌 것)가 0 이다 [exact, enumerated]
  Given: 공통 정의 뒤.
  측정: `git diff -U0 $BASE $TIP -- . ':(exclude).harness' | python3 $M/line-kinds.py | tail -1` 의 6 열(blockdir)이 0.
  양성 대조: SK-06 의 q2 사본(끝에 `<!-- markdownlint-disable MD031 -->` 를 붙임)은 6 열 1.
- [ ] ER-02: BASE 에서 TIP 까지 더한 `markdownlint-disable-next-line` 줄마다 notes 가 `경로:줄` 과 이유를 적는다 [exact, enumerated]
  Given: 공통 정의 뒤.
  측정: `git diff -U0 $BASE $TIP -- . ':(exclude).harness' | python3 $M/line-kinds.py | awk -F'\t' '$1=="NEXTLINE"{print $2}'` 의 `경로:줄` 마다 `git show $TIP:$N | grep -cE "<경로>:<줄>([^0-9]|$)"` 이 1 이상.
  양성 대조: `printf '<!-- markdownlint-disable-next-line MD031 -->\n' >> <scratch 사본>` 을 --no-index 로 맞대면 NEXTLINE 1 줄이 나오고, 그 `경로:줄` 은 notes 에 없어 0.
- [ ] ER-03: A1 네 파일에서 글로 더한 제목 줄의 제목 글이 대응 페이지에 나온다 — `design-kit/references/visual-change-protocol.md` → `docs/design-kit/visual-change-protocol.html` · `onboarding-kit/skills/setup-guide/SKILL.md` → `docs/onboarding-kit/setup-guide.html` · `bambu-kit/skills/bambu-print-profile/SKILL.md` → `docs/bambu-kit/bambu-print-profile.html` · `harness/references/contract-schema.md` → `docs/harness/contract-schema.html` [exact, enumerated]
  Given: 공통 정의 뒤.
  측정: 네 원본마다 `git diff -U0 -w --ignore-blank-lines $BASE $TIP -- <원본> | python3 $M/line-kinds.py | awk -F'\t' '$1=="OTHER" && $3=="+"{print $4}' | grep -E '^#{1,6} '` 의 줄마다 `#` 과 공백을 뗀 글을 `grep -cF -- '<글>' <페이지>` 로 찾아 1 이상. 더한 제목 줄이 없으면 그 원본은 통과.
  양성 대조: `printf '### 없는 제목 글\n'` 을 더한 scratch 사본을 맞대면 OTHER + 1 줄이 나오고 페이지에서 0.
  측정 대상: `design-kit/references/visual-change-protocol.md` · `docs/design-kit/visual-change-protocol.html` · `onboarding-kit/skills/setup-guide/SKILL.md` · `docs/onboarding-kit/setup-guide.html` · `bambu-kit/skills/bambu-print-profile/SKILL.md` · `docs/bambu-kit/bambu-print-profile.html` · `harness/references/contract-schema.md` · `docs/harness/contract-schema.html`

## Architecture

- [ ] AR-01: BASE 뒤 가지 `chore/ak3-lt` 의 모든 커밋이 맨 위 폴더 하나만 건드리고, 메시지의 빈 줄을 뺀 마지막 줄이 서명 줄이다 [exact, enumerated]
  Given: 공통 정의 뒤.
  측정: `for c in $(git rev-list $BASE..$TIP); do n=$(git show --name-only --format='' $c | cut -d/ -f1 | sort -u | grep -c .); s=$(git log -1 --format=%B $c | sed '/^[[:space:]]*$/d' | tail -1); [ "$n" = 1 ] && [ "$s" = 'Co-Authored-By: Claude Opus 5.5 (1M context) <noreply@anthropic.com>' ] || echo "BAD $c n=$n"; done | grep -c BAD` 이 0. `git rev-list $BASE..$TIP | grep -c .` 이 1 이상.
  양성 대조: 같은 폴더 세기를 `a5152c5` 에 돌리면 17 이다.
- [ ] AR-02: BASE 에서 TIP 까지 바뀐 경로(`.harness/` 제외)가 전부 `## 범위 경계` 의 `# sprint-scope` 블록 안에 있다 [exact, enumerated]
  Given: 공통 정의 뒤. `CF=.harness/sprint-contract-after-0928-markdown-rest.md`.
  측정: `git diff --name-only $BASE $TIP -- . ':(exclude).harness' | awk 'NR==FNR{if(/\/$/)d[$0];else f[$0];next} {ok=($0 in f); for(k in d) if(index($0,k)==1) ok=1; if(!ok) print}' <(awk '/^# sprint-scope$/{p=1;next} p&&/^```/{p=0} p' $CF) - | grep -c .` 이 0.
  양성 대조: 같은 명령을 `c3e45f3` 와 BASE 사이에 돌리면 1 이상 (범위 밖 경로가 많다).
- [ ] AR-03: `.harness` 의 계약 봉인이 하나도 깨지지 않았다 — 이 스프린트가 지난 계약 · QA 리포트 · 개정 파일을 고치지 않았다 [exact, enumerated]
  Given: 공통 정의 뒤.
  측정: `bash $M/seal-count.sh $W` 출력에 `SEAL_BROKEN` 줄이 없다. `git diff --name-only --diff-filter=MD $BASE $TIP -- .harness | grep -vcE '^\.harness/sprint-contract-after-0928-markdown-rest\.md$'` 이 0 (지난 기록은 바뀌거나 지워지지 않았다 — 이 계약의 status 줄만 예외).
  양성 대조: 봉인된 계약 사본의 조건 한 줄을 바꾼 scratch 폴더는 `1 SEAL_BROKEN` (회귀 게이트 절).

## Anti-patterns

- [ ] AP-03: bare code fence 금지 — `python3 scripts/validate-plugin.py --check=code-fence` 가 `Total: 14 plugins, 14 OK` · rc=0 (킷 안 B19 · A1 파일의 울타리를 건드리지 않는다)
- [ ] AP-04: SKILL.md frontmatter name 누락 금지 — `python3 scripts/validate-plugin.py --check=frontmatter` 가 `Total: 14 plugins, 14 OK` · rc=0 (A1 의 MD041 을 머리 설정 앞에 제목을 넣어 고치면 깨진다)

## Reusability

- [ ] RE-01: N/A (저장소에 들어가는 산출물이 문서 · 스킬 본문의 모양 수정뿐 — 재사용 단위 코드가 없다. 측정 묶음은 `.harness/.meta` 의 판정용이다)
- [ ] RE-02: 새 저장소 검사 스크립트를 만들지 않았다 — `git diff --name-only --diff-filter=A $BASE $TIP -- . ':(exclude).harness' | grep -c .` 이 0 [exact]

## Diagnostics

- [ ] DG-01: N/A (commands.analyze 는 `bash -n scripts/release.sh` — 이번 변경과 교집합 0. 측정: `git diff --name-only $BASE $TIP | grep -c '^scripts/release.sh$'` 이 0)
- [ ] DG-02: 바꾼 md 파일이 편집기와 같은 설정의 markdownlint 경고 0 개다 — `howto-kit/README.md` 의 `<!-- AUTO:* -->` 블록 안 경고도 0 (BASE 는 블록 밖 18 · 블록 안 0) [exact]
  Given: 공통 정의 뒤.
  측정: `git diff --name-only $BASE $TIP -- '*.md' ':(exclude).harness' > $SCR/lt-md.txt; bash $RUN $W $SCR/lt-md.txt | grep -c .` 이 0.
  양성 대조: BASE 에서 `a1-files.txt` 로 돌리면 177.
- [ ] DG-03: N/A (commands.test 는 `bash scripts/release.sh` — 이번 변경과 무관. 실제 시험은 SC-02 가 잰다)
- [ ] DG-04: N/A (구동할 앱 · 서버가 없다 — 변경 파일이 문서 · 스킬 본문뿐. 페이지 실제 렌더는 SC-03 이 잰다)
