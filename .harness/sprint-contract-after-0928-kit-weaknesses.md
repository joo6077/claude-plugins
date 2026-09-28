---
feature: "킷 약점 (api · bambu · onboarding · 설치본 안내)"
slug: after-0928-kit-weaknesses
created: "2026-09-28 10:55"
complexity: "복잡"
conditions: 28
status: active
conditions_digest: "sha256:f05433dec1131ccc"
measurement_digest: "sha256:5c70a649404879e3"
locked_at: "2026-09-28 11:03"
owner_session: bda55d45-296c-491f-89ba-b52042d58e72
---

## 배경

- 남은 일 목록(`/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0928/.harness/.meta/after-kaizen-0928/remaining.md`)의 A15 · B5 · B6 · B11 · B21 · D7 여섯 항목을 한 묶음(k1)으로 처리한다.
- 사용자 지시: 2026-09-27T01:22:01.089Z 「자동으로 다 진행해 나한테 묻지 말고 …」, 2026-09-28 「약점과 일부만 한 거 다처리하지??」(세션 bda55d45-296c-491f-89ba-b52042d58e72). 결정 기록은 같은 폴더 `decisions.md`.
- A15 — api-kit 뷰어 스펙(`api-kit/skills/api-ui/references/viewer-spec.md:87-89`)은 보류 · flaky 실패에 `failMark` 와 글자 표지 · `aria-label` 을 달라고 정했지만, 예시 화면 `api-kit/evals/fixtures/unjudged/.api/ui.html` 에는 `failMark` 가 0 번 나오고 그 표지를 그리는 코드도 없다. 시험(`api-kit/evals/api-ui.spec.js`)도 표지를 보지 않는다.
- B5 — `bambu-kit/evals/run-gate-fixtures.sh:63-72` 는 FAIL 줄 수 · `RESULT` · 종료 코드만 본다. SKILL.md 음성 대조 표(`bambu-kit/skills/bambu-print-profile/SKILL.md:1860-1862 · 1874-1875`) 다섯 행이 적은 `[미검증]` 줄 수 기대는 재지 않는다. 가짜 `[미검증]` 줄을 넣은 사본 · 못 읽은 칸 알림 줄을 지운 사본 넷 모두 지금 `결과: 24 경우 중 불일치 0` 이다(봉인 전 실측).
- B6 — `onboarding-kit/skills/setup-guide/SKILL.md:122-146` 의 G5 는 표 줄 앞 공백 · 머리 칸 U+00A0 · U+3000 · U+00A0 하나뿐인 칸 · 굵은 머리 · 인용 속 표를 알아보지 못해 빈 칸이 있어도 통과하고, 알아보지 못한 표를 「표 없음」 과 같게 `PASS rows=0` 으로 낸다. 변형 30 개 중 28 개가 기대와 다르다(봉인 전 실측). CRLF 처리(cx2 `af18dd0`)는 그대로 지켜야 한다.
- B11 — 설치본 플러그인은 킷 폴더만 담으므로 레포 뿌리 `docs/<칸>/` 경로는 설치본에서 열리지 않는다. backend · rust · infra 에만 raw 주소 안내가 들어갔다(`52d905c` · `10cc34e` · `1ea26b2`). 킷 열네 개를 다 재 보니 안내가 필요한데 없는 파일이 60 개다(api 13 · howto 6 · planning 13 · react 27 · rust 1). 목록은 `.harness/.meta/after-0928-kit-weaknesses/b11-need-before.txt`.
- B21 — `planning-kit/agents/planning-reviewer.md:243` 예시 문장 속 주소가 `<https://…>` 모양이 됐고(에이전트가 따라 쓸 수 있다), `tone-kit/references/core-naming.md:139` 의 N-12 가 `###` 제목이 되어 아래 `###` 절들과 단계가 같아졌다(`98f2c65` 에서 생김).
- D7 — `bambu-kit/skills/bambu-print-profile/SKILL.md:2560-2562` 버전 대조 표가 「references 는 `02.06.00.51` 기준」 이라고 적는다. references 는 2026-09-05 에 `02.08.02.61` 로 다시 확인됐고(`references/bambu-fields-baseline.md:9`) 옵션 목록도 `references/option-keys/bambu-02.08.02.61.tsv` 뿐이다. 같은 표가 `docs/bambu-kit/bambu-print-profile.html:2102-2106` 에 옮겨져 있다.

## GAP 분석

복잡도 네 축:

| 축 | 값 |
| --- | --- |
| 레이어 수 | 검사 스크립트 · 게이트 함수 · 예시 화면 · 문서 쪽 · CI — 넷 이상 |
| 공개 계약 변경 | 예 — G5 가 새 입력에 FAIL 을 낸다, 러너 판정이 바뀐다 |
| 소비면 | 예 — `evals.json` 기대 출력, `run-gate-evals.sh`, `docs/onboarding-kit/setup-guide.html` 의 함수 사본, 문서 쪽 표 두 곳 |
| 회귀 위험 | 예 — 기존 CRLF 판정 · 기존 12 사례 · 기존 24 시험 파일 |

넷 다 「예」 라 복잡이다. 소비면은 조건 AR-02 · AR-03 · SC-05 로 따로 잰다.

설정 대조표 (`.harness/project.yaml` 그대로):

| 키 | 읽은 값 | 계약에 쓴 값 |
| --- | --- | --- |
| `commands.analyze` | `bash -n scripts/release.sh` | DG-01 N/A 사유에 그대로 |
| `commands.test` | `bash scripts/release.sh 2>&1 \|\| true` | DG-03 N/A 사유에 그대로 |
| `diagnostics.ide_exclude` | `[]` | DG-02 에 `[]` |
| `contract_categories` | Skill/SK · Script/SC · Error/ER · Architecture/AR | 네 절 |
| `anti_patterns` | AP-01 · AP-02 · AP-03 · AP-04 | AP-03 · AP-04 (AP-01 은 판 번호 하드코딩 규칙인데 이번에 판 번호를 바꾸는 파일이 없다, AP-02 는 push 를 하지 않는다) |

미리 연 파일 (읽은 자리 · 찾은 문제 · 조건):

| 파일 | 읽은 자리 | 찾은 것 | 조건 |
| --- | --- | --- | --- |
| `api-kit/evals/fixtures/unjudged/.api/ui.html` | `:1478-1545` EP 자료 · `:1703` 트리 줄 · `:2115` 실패 원인 탭 | `failMark` 0 · 표지 그리기 없음 | SK-01 · SK-02 · SK-03 |
| `api-kit/evals/api-ui.spec.js` | `:1-93` | 표지 시험 없음 · 8 시험 | SK-02 |
| `api-kit/evals/fixtures/unjudged/.api/reports/2026-09-02T1422-dev/report.md` | `:5-7` | 보류 0 · flaky 0 | SK-01 |
| `bambu-kit/evals/run-gate-fixtures.sh` | `:55-77` | `[미검증]` 줄 수를 안 잰다 | SC-01 · SC-02 · ER-01 |
| `bambu-kit/skills/bambu-print-profile/SKILL.md` | `:1852-1875` 표 · `:1540-1560` 설치 경로 · `:2553-2567` 버전 표 | 위 B5 · D7 | SC-02 · SK-06 |
| `onboarding-kit/skills/setup-guide/SKILL.md` | `:122-146` G5 | 위 B6 | SC-03 ~ SC-05 · ER-02 |
| `docs/onboarding-kit/setup-guide.html` | `:316-339` 함수 사본 | 원본과 같음(빈 줄 뺀 90 줄) | AR-02 |
| `docs/bambu-kit/bambu-print-profile.html` | `:1721-1735` 음성 대조 표 · `:2095-2126` 버전 표 | 표 두 곳이 원본 사본 | AR-01 · AR-03 |
| `planning-kit/agents/planning-reviewer.md` · `tone-kit/references/core-naming.md` | `:243` · `:137-180` | 위 B21 | SK-05 |
| B11 대상 60 개 | 파일마다 `docs/` 줄 (측정 스크립트 `--detail` 없이 목록만) | 위 B11 | SK-04 · ER-03 · SC-06 |

## 리서치 소스

- 뷰어 표지 규칙: `api-kit/skills/api-ui/references/viewer-spec.md:87-89 · :243`
- 설치본 안내 문장 선례: `backend-kit/skills/backend-guide/SKILL.md` 의 「설치본 플러그인에는 `docs/backend/` 가 없다 …」 줄, 상대 경로 모양은 `backend-kit/skills/backend-guide/references/principle-index.md`
- raw 주소가 실제로 열리는지: `curl -s -o /dev/null -w '%{http_code}' https://raw.githubusercontent.com/joo6077/claude-plugins/main/docs/api/contract/contract-extraction-modes.md` → `200` (2026-09-28 실측)
- 문서 쪽 규칙: `.claude/skills/docs-site/SKILL.md` (공통 CSS 링크 하나 · 320 · 375 · 1280 넘침 0)

## 범위 경계

```text
# sprint-scope
api-kit/
howto-kit/
planning-kit/
react-kit/
rust-kit/skills/rust-model/SKILL.md
bambu-kit/evals/run-gate-fixtures.sh
bambu-kit/skills/bambu-print-profile/SKILL.md
onboarding-kit/skills/setup-guide/
tone-kit/references/core-naming.md
docs/onboarding-kit/setup-guide.html
docs/bambu-kit/bambu-print-profile.html
scripts/check-install-docs-guidance.py
.github/workflows/ci.yml
```

- 하지 않는 것: README 여섯 개(api · howto · planning · react · tone · harness) 와 backend · rust · infra README 에 안내 넣기 — 사람이 읽는 소개라 설치본 에이전트가 여는 파일이 아니다. 이 판정은 측정 스크립트의 EXEMPT 표 21 줄에 사유와 함께 있다.
- 하지 않는 것: 카이젠 스킬(contract · evaluator · harness · flutter-kaizen)과 그 search-sources — 이 레포를 고치는 스킬이라 작업 폴더가 레포이고 `docs/kaizen/` 이 열린다. harness 가이드 · 스키마의 `docs/react/kit-design/` 은 조건 예시 · 지난 기록 글자다.
- 하지 않는 것: design-kit 의 `docs/design/` 경로 — `design-kit/docs/design/` 이 킷 안에 있어 설치본에서 열린다.
- 하지 않는 것: G5 의 네 칸 이상 들여쓴 표(마크다운에서는 코드 블록이다), 표 머리 낱말 순서가 바뀐 표.
- 하지 않는 것: bambu SKILL.md 의 `실측 (02.06.00.51)` 같은 옛 실측 기록 줄 — 그때 잰 사실이라 바꾸지 않는다. D7 은 버전 대조 표(§매 실행 시 필수 사전 절차 1)만 고친다.
- B11 안내 줄이 들어가는 킷 파일에는 대응 문서 쪽을 맞추지 않는다 — 선례 세 커밋이 `docs/` 를 0 개 바꿨고(`git show --name-only --format= 52d905c 10cc34e 1ea26b2 | grep -c '^docs/'` → `0`), 안내는 설치본 에이전트에게 하는 말이라 브라우저 문서에는 뜻이 없다.
- tone core-naming N-12 는 `docs/tone-kit/naming-taxonomy.html` 에 제목으로 옮겨져 있지 않다(`:590` 은 배지 글자) — 문서 쪽을 바꾸지 않는다.
- 커밋: 킷(맨 위 폴더) 하나에 커밋 하나 이상, 한 커밋에 맨 위 폴더 하나. `git add <경로>` 뒤 `git commit -o <경로>`.
- 커버리지 해소: SK-04 — 60 개 파일 이름은 `b11-need-before.txt` 한 곳에만 적고 조건은 그 파일을 읽어 잰다(목록을 두 번 적지 않는다).
- 커버리지 해소: AR-04 — 범위 목록은 위 `# sprint-scope` 블록 한 곳에만 적는다.
- 커버리지 해소: SK-01 — 세 경로는 측정 명령의 인자로 그대로 적었다(검출기는 빈칸 든 명령 토큰을 대상에서 뺀다).
- 커버리지 해소: SC-01 · SC-02 · ER-01 — 시험 파일 이름은 러너(`run-gate-fixtures.sh`)와 `b5-controls.sh` 출력의 `일치` · `불일치` · `건너뜀` 줄에 이름째 나온다. 측정은 그 줄에서 이름을 찾는다.
- 커버리지 해소: ER-02 — 네 파일 이름은 `b6-variants.py` 가 만들고 `b6-check.sh` 가 줄마다 이름째 찍는다. 측정의 `grep -E 'five-col|plain-unrelated'` 가 네 줄을 모두 고른다.
- 커버리지 해소: SC-06 — `backend-kit/skills/backend-guide/SKILL.md` 는 양성 대조 사본에서 지우는 파일이고, 스크립트 · CI 파일 이름은 측정의 `grep` · 실행 명령이 그대로 쓴다.
- 커버리지 해소: SK-05 — 두 파일 이름을 측정 절 (1)(2) 에 적었다. 주소 두 토큰은 대상 파일이 아니라 찾는 글자다.
- 커버리지 해소: AR-01 — 쪽 경로 · CSS · 판 번호 · 옵션 목록 이름은 측정의 `awk` 구간과 `grep -c` · 넘침 스크립트가 그대로 쓴다.
- 오라클 해소: SK-02 — (a)(b)(c) 를 시험 파일에서 읽는 것은 보조다. 표지를 실제로 그리는지는 SK-02 의 Playwright 실행과 SK-03 의 두 음성 대조(자료를 지운 사본 · 그리기를 지운 사본이 둘 다 시험에 떨어진다)가 판정한다.
- 오라클 해소: ER-02 — `b6-check.sh` 가 게이트 함수를 SKILL.md 에서 뽑아 실제로 돌린 출력으로 판정한다(글자 찾기가 아니다).
- 오라클 해소: ER-03 — 산출물 자체가 설치본 에이전트가 읽는 안내 문장이라 문장 존재가 곧 산출물이다. 안내가 가리키는 경로가 실제로 있는지는 SK-04 의 `b11-paths.py` 가 판 트리로 잰다.
- 오라클 해소: DG-01 — N/A 사유를 재는 줄이라 실행 대상이 없다. 실행 검사는 SC-07 · shellcheck 가 맡는다.
- 교차 진단 반영(봉인 전): 이 계약의 조건 결함은 지적되지 않았다. 지적은 묶음 전체의 빈자리다 — remaining.md 의 A1 · A2 · A3 · B12~B20 · D1 · D3 은 네 작업 폴더(ak3-ex · ak3-h1 · ak3-h2 · ak3-k1) 어느 계약에도 없다. k1 은 여섯 항목만 맡으므로 이 계약에 넣지 않고, 배정은 묶음을 나눈 부모 세션이 정한다. k1 notes 의 「남은 것」 에 같은 사실을 적는다.

## 회귀 게이트 — 공통 정의

- `W=/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak3-k1`, `M=$W/.harness/.meta/after-0928-kit-weaknesses`, 기준 커밋 `BASE=95508d9`, 스프린트 상한 `TIP=chore/ak3-k1` (가지 끝. 이미 합쳐졌으면 그 병합 커밋의 둘째 부모. `HEAD` 를 쓰지 않는다).
- 임시 폴더는 `TMPDIR=/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/bda55d45-296c-491f-89ba-b52042d58e72/scratchpad/k1/tmp` 처럼 틀을 준다. 사본은 `git -C $W archive $TIP <경로…> | tar -x -C <임시 폴더>` 로 풀고, Playwright 를 돌릴 사본에는 `ln -s $W/node_modules <임시 폴더>/node_modules` 를 한다. `git ls-files` 를 쓰는 스크립트를 사본에서 돌릴 때는 사본에서 `git init -q && git add -A` 를 먼저 한다.
- markdownlint: `ML=/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/bda55d45-296c-491f-89ba-b52042d58e72/scratchpad/mdcheck/node_modules/markdownlint-cli2/markdownlint-cli2-bin.mjs` (v0.23.2), 설정 `{"config":{"MD013":false}}` (편집기가 MD013 을 끈다).
- 측정 묶음 sha256 앞 16 자리 (봉인 전 값): `a15-ep.py 4fd489151dc6dbff` · `b11-docs-guidance.py ff73ca85c0dd233e` · `b11-need-before.txt 70a8b166dcdbcea9` · `b11-paths.py 36bcf4fad0699fe8` · `b5-controls.sh d1eba1576d98db0e` · `b5-page-table.py 3d4d3bbe57c95712` · `b6-check.sh b4faacbb4c60ec6a` · `b6-page-copy.py 01c61d8696fac3ca` · `b6-registered.py c23449a09aadf578` · `b6-variants.py 758a96fe67f63f3a` · `md-before.txt 1138f3ac02ed7912` · `md-files.txt c6fc5f816a1ebacf` · `page-overflow.js 5eb0c3c8cfe533a0`. 평가 전에 `shasum -a 256` 로 다시 재서 다르면 그 조건은 FAIL 이다.
- 봉인 전 로컬 CI: `ci-local.sh` 25 단계 rc=0 (feedback-agg-test 는 yq 가 없어 SKIP), CI 파일에만 있는 다섯(check-api-kit-docs · detect-docs-drift --check-table · check-cause-table-copies · measure-helpers-test · makerworld-fetch-test) rc=0, `validate-plugin.py` 「14 plugins, 14 OK」.

## Skill

- [ ] SK-01: A15 예시 화면 자료 — Given 구현 커밋 뒤, `api-kit/evals/fixtures/unjudged/.api/ui.html` 의 엔드포인트 자료에 `failMark:'보류'` 인 엔드포인트가 1 개 이상, `failMark:'flaky'` 인 엔드포인트가 1 개 이상 있고, 표지가 붙은 엔드포인트는 전부 `state:'fail'` 이며, 같은 폴더 `reports/2026-09-02T1422-dev/report.md` 실행 요약 표의 `보류` · `flaky` 칸과 `api-kit/evals/evals.json` api-ui 사례 `expect.FAIL` 이 그 수와 맞는다 [exact, enumerated]
  측정: `python3 $M/a15-ep.py api-kit/evals/fixtures/unjudged/.api/ui.html api-kit/evals/fixtures/unjudged/.api/reports/2026-09-02T1422-dev/report.md api-kit/evals/evals.json` (`expect.FAIL` · `reports/2026-09-02T1422-dev/report.md` 의 두 칸은 스크립트의 `MATCH` 줄이 읽는다) → `SUMMARY` 줄의 `hold>=1` · `flaky>=1` · `misplaced=0`, `MATCH … ok=1`, 종료 코드 0
  봉인 전 값: `SUMMARY eps=6 fail=2 hold=0 flaky=0 misplaced=0` · `MATCH report_hold=0 report_flaky=0 expect_fail=2 ok=1`
  알려진 답: users.me 에 `failMark:'보류'`, auth.token(pass) 에 `failMark:'flaky'` 를 넣은 사본 → `hold=1 flaky=1 misplaced=1` (봉인 전 실측 일치)
- [ ] SK-02: A15 화면이 표지를 그린다 — `npx playwright test api-kit/evals/` 가 종료 코드 0 이고 통과 시험 수가 8 보다 많으며, `npx playwright test api-kit/evals/ --list` 의 시험 이름에 `보류` 가 든 것 1 개 이상 · `flaky` 가 든 것 1 개 이상 있고, 그 시험들이 (a) 트리 줄에 글자 표지 `보류` / `flaky` 와 `aria-label="실패 · 보류 — 게이트를 깨지 않음"` / `aria-label="실패 · flaky — 재실행에서 뒤집힘"` 을, (b) 그 엔드포인트를 고른 뒤 `실패 원인` 탭 옆에 같은 글자 표지와 같은 `aria-label` 을, (c) 상단 FAIL 칩이 표지 달린 엔드포인트까지 세는 것을 확인한다 [exact, enumerated]
  측정: `cd $W && npx playwright test api-kit/evals/ 2>&1 | tail -3` 의 `N passed` (N>8) · 종료 코드 0, `--list` 출력 grep. (a)(b)(c) 는 `api-kit/evals/api-ui.spec.js` 를 읽어 세 확인이 각각 있는지 본다
  봉인 전 값: `8 passed`, `--list` 에 `보류` · `flaky` 0 개
- [ ] SK-03: A15 음성 대조 — 두 사본 모두 `npx playwright test api-kit/evals/` 가 종료 코드 0 이 아니다. (1) 자료 사본: `$TIP` 을 푼 사본의 ui.html 에서 `failMark:'보류'` · `failMark:'flaky'` 를 `failMark:null` 로 바꾼다(변이 확인: 바꾼 뒤 `grep -c "failMark:'"` 가 0). (2) 그리기 사본: 표지를 그리는 코드(엔드포인트의 `failMark` 를 읽어 표지 · `aria-label` 을 만드는 줄)를 지운다(변이 확인: `grep -c '실패 · 보류 — 게이트를 깨지 않음'` 이 줄어든다) [exact, enumerated]
  측정: 공통 정의의 사본 절차로 `api-kit` · `playwright.config.js` · `package.json` 을 풀어 돌린다
  음성 대조: 이 조건 자체가 음성 대조다 — 원본(변이 없음) 사본은 종료 코드 0 이어야 한다(봉인 전 실측: `8 passed`)
- [ ] SK-04: B11 설치본 안내 — Given 구현 커밋 뒤, `python3 $M/b11-docs-guidance.py $W` 가 `TOTAL files=94 ok=73 need=0 exempt=21` 을 내고 종료 코드 0 이며, `$M/b11-need-before.txt` 의 60 개 파일이 전부 `OK` 줄로 나온다 [exact, enumerated]
  측정: `python3 $M/b11-docs-guidance.py $W > out; grep '^OK' out | awk '{print $2}' | sort > ok.txt; comm -23 <(sort $M/b11-need-before.txt) ok.txt | grep -c .` → `0`
  봉인 전 값: `TOTAL files=94 ok=13 need=60 exempt=21`, 종료 코드 1
  알려진 답: `python3 $M/b11-docs-guidance.py $W backend-kit rust-kit infra-kit` 봉인 전 → OK 13 줄(backend 5 · infra 6 · rust 2) · `NEED rust-kit/skills/rust-model/SKILL.md dirs=backend,rust missing=backend` · `TOTAL files=17 ok=13 need=1 exempt=3`
  가리키는 경로: `python3 $M/b11-paths.py $W chore/ak3-k1 $M/b11-need-before.txt` 가 `missing=0` · 종료 코드 0 (안내대로 raw 주소를 붙였을 때 404 가 나지 않으려면 경로가 그 판에 있어야 한다). 봉인 전 값 `PATHS files=60 paths=199 missing=0`
  양성 대조(경로 검사): api-kit 한 파일에 `docs/api/no-such-file.md` 를 더한 사본 저장소 → `MISSING api-kit/references/api-layout.md docs/api/no-such-file.md` · `missing=1` · 종료 코드 1 (봉인 전 실측)
- [ ] SK-05: B21 — (1) `planning-kit/agents/planning-reviewer.md` 에서 `Small 위반 — stories.md §INVEST` 가 든 줄에 `<https://` 가 0 번이고, 같은 줄에 `https://agilealliance.org/glossary/invest/` 가 백틱 코드 안에 있다. (2) `tone-kit/references/core-naming.md` §6(`## 6.` 줄부터 `## 7.` 줄 앞까지)에 `N-12` 가 든 제목 줄(`#` 로 시작)이 0 개, `N-12` 와 `SHOULD` 가 함께 든 제목 아닌 줄이 1 개 이상, `###` 제목이 정확히 4 개(`우선순위` · `왜` · `before / after` · `적용 범위`). (3) 두 파일 markdownlint 0 건 [exact, enumerated]
  측정: (1) `planning-kit/agents/planning-reviewer.md` 에 `grep 'Small 위반 — stories.md §INVEST' … | grep -c '<https://'` → 0, 같은 줄에서 백틱 코드 안의 `https://agilealliance.org/glossary/invest/` 수(`grep -cE` 로 백틱 쌍 안) → 1. (2) `tone-kit/references/core-naming.md` 에 `awk '/^## 6\./{p=1} /^## 7\./{p=0} p'` 에 `grep -c '^#.*N-12'` → 0 · `grep -v '^#' | grep 'N-12' | grep -c SHOULD` ≥1 · `grep -c '^### '` → 4. (3) `node $ML --config <설정> <두 파일>` → `Summary: 0 issues`
  봉인 전 값: (1) 1 · 0 (2) 1 · 0 · 5 (3) 0 issues
- [ ] SK-06: D7 SKILL.md 버전 표 — `bambu-kit/skills/bambu-print-profile/SKILL.md` 의 `### 1. Bambu Studio 버전 cross-check` 줄부터 `### 2.` 줄 앞까지에서 `02.06.00.51\` 기준` 0 번, `references baseline` 0 번, `bambu-02.08.02.61.tsv` 1 번 이상(그 파일이 `references/option-keys/` 에 있다), 표 줄(`|` 로 시작) 가운데 `02.08.02` 가 든 줄 1 개 이상, `02.06.00.xx` 로 시작하는 표 줄에 `그대로 사용` 0 번 [exact, enumerated]
  측정: `awk '/^### 1\. Bambu Studio 버전 cross-check/{p=1} /^### 2\./{p=0} p' <SKILL.md>` 출력에 각 `grep -c`, `test -f bambu-kit/skills/bambu-print-profile/references/option-keys/bambu-02.08.02.61.tsv`
  봉인 전 값: 1 · 1 · 0 · 0 · 1

## Script

- [ ] SC-01: B5 이 맥(설치본 있음) — `bash bambu-kit/evals/run-gate-fixtures.sh` 의 마지막 줄이 정확히 `결과: N 경우 중 불일치 0` 이고(N 은 `find bambu-kit/evals/gate-fixtures -maxdepth 1 -name '*.json' | grep -c .`, 봉인 전 24) 종료 코드 0 이며, 표에 `[미검증]` 줄 수를 적은 다섯 행(`process-bridge-unreadable-slot.json` · `process-thin-unreadable-slot.json` · `filament-unreadable-slot.json` · `filament-lattice-fanfix.json` · `process-thin-baseline.json`)이 모두 `일치` 줄로 나온다 [exact, enumerated]
  측정: `TMPDIR=<틀> bash bambu-kit/evals/run-gate-fixtures.sh; echo rc=$?`
  봉인 전 값: `결과: 24 경우 중 불일치 0`, 다섯 행 `일치`, rc=0
- [ ] SC-02: B5 음성 대조 — `sh $M/b5-controls.sh $W` 의 m1 · m2 · m3 · m4 사본이 각각 종료 코드 1 이고 `불일치` 줄에 이름이 나온다: m1(가짜 `[미검증]` 줄 더함) → `filament-lattice-fanfix.json`, m2(소재 슬롯 못 읽음 알림 지움) → `filament-unreadable-slot.json`, m3(외벽 속도 슬롯 못 읽음 알림 지움) → `process-thin-unreadable-slot.json`, m4(벽 예산 미기록 알림 지움) → `process-thin-baseline.json` [exact, enumerated]
  측정: 위 스크립트 출력의 `변이 <이름> 차이줄=` 이 m1 1 · m2 2 · m3 2 · m4 2 (변이가 먹었다는 확인)이고 각 사본의 `rc=1` 과 `불일치 <이름>` 줄
  봉인 전 값: 네 사본 모두 `결과: 24 경우 중 불일치 0` · rc=0 (결함 재현)
- [ ] SC-03: B6 표 모양 — `python3 $M/b6-variants.py onboarding-kit/skills/setup-guide/evals/fixtures <폴더>` 로 만든 30 개 입력(빈 칸 표 모양 8 가지 · 다 찬 표 모양 6 가지 · 무관한 표 1 가지 × LF · CRLF)에 대해 `sh $M/b6-check.sh $W <폴더> zsh` 와 `… bash` 가 둘 다 `B6 shell=<셸> total=30 diff=0` 이고 종료 코드 0 이다. 모양: 줄 앞 공백 1 칸 · 3 칸, 머리 칸 U+00A0, 머리 칸 U+3000, 굵은 머리, 인용 속 표, U+00A0 하나뿐인 칸, 다섯 칸 머리 [exact, enumerated]
  측정: 위 두 명령. 기대는 스크립트 머리 주석 — 빈 칸 모양은 `G5_BLOCKING FAIL rows=2 empty=1 nourl=0`(다섯 칸 머리는 `G5_BLOCKING FAIL` 로 시작), 다 찬 모양은 `G5_BLOCKING PASS rows=2`, 무관한 표는 `G5_BLOCKING PASS rows=0`
  봉인 전 값: zsh · bash 모두 `total=30 diff=28`
  mawk: `docker run --rm --network none -v $W:/r:ro -v <폴더>:/v:ro buildpack-deps:bookworm-scm sh /r/.harness/.meta/after-0928-kit-weaknesses/b6-check.sh /r /v bash` 도 `diff=0` (CI 리눅스 awk 가 mawk 라서. 봉인 전 `diff=28` 실측). 도커가 안 뜨면 이 한 줄만 `[미검증]` 으로 받는다
- [ ] SC-04: B6 시험 등록 — `sh onboarding-kit/skills/setup-guide/evals/run-gate-evals.sh` 가 `EVALS_PASS` 로 끝나고 `EVALS declared=D ran=D fail=0` 에서 D ≥ 19 이며, `python3 $M/b6-registered.py onboarding-kit/skills/setup-guide/evals` 가 `SHAPES covered=7/7` · `crlf_cases>=1` · 종료 코드 0 이다 [exact, enumerated]
  측정: 위 두 명령 (러너는 폴더에만 있고 `gate_cases` 에 없는 픽스처를 실패로 센다 — 새 픽스처가 실행 목록에 들어갔는지 여기서 드러난다. CI 는 `.github/workflows/ci.yml` 의 `sh onboarding-kit/skills/setup-guide/evals/run-gate-evals.sh` 단계가 돌린다)
  봉인 전 값: `declared=12 ran=12 fail=0` · `SHAPES covered=0/7 crlf_cases=0 cases=12`
  알려진 답: 빈 칸 변형 16 개를 FAIL 기대로 등록한 사본 → `lead-space 4` · 나머지 여섯 모양 각 2 · `covered=7/7 crlf_cases=8 cases=28` (봉인 전 실측 일치)
- [ ] SC-05: B6 기존 판정 유지 — `onboarding-kit/skills/setup-guide/evals/evals.json` 의 기존 12 사례(`ok-flutter` · `stack-unset` · `stack-empty` · `g4-ko-sourced` · `g4-ko-unsourced` · `ledger-marker-swift` · `ledger-misplaced` · `ledger-double-source` · `blocking-ok` · `blocking-empty` · `blocking-empty-crlf` · `blocking-nourl`)의 `fixture` · `stack` · `expect` 가 `$BASE` 판과 글자까지 같다 [exact, enumerated]
  측정: 두 판의 evals.json 을 python 으로 읽어 id 마다 세 값을 맞대 다른 id 수 → 0
  음성 대조: `$TIP` 을 푼 사본의 SKILL.md 에서 줄 끝 CR 을 지우는 문장을 지운다(변이 확인: 사본과 원본 차이 줄 ≥1, 사본의 `grep -c '\\r'` 가 원본보다 작다) → 그 사본의 `run-gate-evals.sh` 가 `EVALS_FAIL` 이고 `FAIL  blocking-empty-crlf` 줄이 있다. 봉인 전 같은 변이(`{ sub(/\r$/, "") }` 줄 삭제)로 `EVALS declared=12 ran=12 fail=1` · `FAIL  blocking-empty-crlf` 실측
- [ ] SC-06: B11 레포 검사 — `scripts/check-install-docs-guidance.py` 가 있고 `.github/workflows/ci.yml` 에 그것을 부르는 `run:` 줄이 1 개 있으며, `python3 scripts/check-install-docs-guidance.py` 를 레포 뿌리에서 돌리면 종료 코드 0 이다. 양성 대조: `$TIP` 을 푼 사본(`git init -q && git add -A` 한 것)에서 `backend-kit/skills/backend-guide/SKILL.md` 의 「설치본 플러그인에는」 줄을 지우면 종료 코드 1 이고 출력에 `backend-kit/skills/backend-guide/SKILL.md` 가 나온다 [exact, enumerated]
  측정: `grep -cE 'run: python3 scripts/check-install-docs-guidance\.py' .github/workflows/ci.yml` → 1, 두 실행의 종료 코드와 출력 grep
  봉인 전 값: 스크립트 없음 · CI 줄 0
- [ ] SC-07: 로컬 CI — Given 구현 커밋 뒤, `TMPDIR=<틀> bash /Users/jackson/Hub/10_Dev/claude-plugins/.harness/handoff/2026-09-26-tools/ci-local.sh $W` 의 25 단계가 rc=0(feedback-agg-test 는 SKIP 허용)이고, CI 파일에만 있는 `python3 scripts/check-api-kit-docs.py` · `python3 scripts/detect-docs-drift.py --check-table` · `python3 scripts/check-cause-table-copies.py` · `bash harness/evals/measure/measure-helpers-test.sh` · `bash bambu-kit/evals/makerworld-fetch-test.sh` · `python3 scripts/check-install-docs-guidance.py` 가 모두 rc=0 이다 [exact, enumerated]
  측정: `summary.txt` 의 `rc=0` 줄 수 25, 여섯 명령 각각 `; echo rc=$?`
  봉인 전 값: 25 단계 rc=0 · 앞 다섯 rc=0 (여섯째는 아직 없음)

## Error

- [ ] ER-01: B5 설치본 없는 기계에서 못 잰 것을 일치로 세지 않는다 — `sh $M/b5-controls.sh $W` 의 noinst 사본 결과가 정확히 `결과: N 경우 중 불일치 0 · 건너뜀 19` 이고 rc=0 이며, `filament-unreadable-slot.json` · `filament-lattice-fanfix.json` · `process-thin-baseline.json` 이 각각 `건너뜀` 으로 시작하는 줄에 나오고 그 줄에 `[미검증]` 이 든다 [exact, enumerated]
  측정: 위 스크립트의 noinst 묶음 출력 (변이 확인 `차이줄=20`)
  봉인 전 값: `결과: 24 경우 중 불일치 0 · 건너뜀 16`, 세 파일은 `일치`
- [ ] ER-02: B6 알아보지 못한 표 — SC-03 출력에서 `empty-five-col.md` · `empty-five-col-crlf.md` 가 `G5_BLOCKING FAIL` 로 시작하는 G5 줄을 내고(「표 없음」 과 같은 `G5_BLOCKING PASS rows=0` 이 아니다), 막는 요구 표가 아닌 표만 있는 `plain-unrelated.md` · `plain-unrelated-crlf.md` 는 `G5_BLOCKING PASS rows=0` 을 낸다(과하게 막지 않는다) [exact, enumerated]
  측정: `sh $M/b6-check.sh $W <폴더> zsh | grep -E 'five-col|plain-unrelated'`
  봉인 전 값: 네 파일 모두 `G5_BLOCKING PASS rows=0`
- [ ] ER-03: B11 raw 도 못 읽을 때 — 60 개 파일에서 「설치본 플러그인에는」 과 raw 주소가 함께 든 줄마다 `그래도 못 읽으면` 과 `못 읽었다고 적는다` 가 같은 줄에 있다 [exact, collective]
  측정: 60 개 파일에 `grep -h 'raw.githubusercontent.com/joo6077/claude-plugins/main/' | grep '설치본 플러그인에는'` 한 줄 수 A 와, 그중 두 문구가 모두 든 줄 수 B 를 센다 → A ≥ 60 이고 A = B
  봉인 전 값: A = 0

## Architecture

- [ ] AR-01: D7 문서 쪽 — `docs/bambu-kit/bambu-print-profile.html` 의 `<h3>Bambu Studio 버전 대조</h3>` 줄부터 `릴리스 현황 (` 가 든 줄까지에서 `02.06.00.51</code> 기준` 0 번, `references 기준값` 0 번, `<tr>` 줄 가운데 `02.08.02` 가 든 줄 1 개 이상, `bambu-02.08.02.61.tsv` 1 번 이상. 그리고 그 쪽의 공통 CSS 링크가 `rel="stylesheet"` 1 개(`../assets/site.css`)이고 `node $M/page-overflow.js $W docs/bambu-kit/bambu-print-profile.html` 이 `OVERFLOW checked=3 bad=0` [exact, enumerated]
  측정: `awk '/<h3>Bambu Studio 버전 대조<\/h3>/{p=1} p{print} p&&/릴리스 현황 \(/{exit}'` 출력에 각 `grep -c`, 넘침 스크립트
  봉인 전 값: 1 · 1 · 0 · 0, CSS 1 개, `bad=0`
  양성 대조: 쪽 끝에 폭 2000px 상자를 넣은 사본 → `OVERFLOW checked=3 bad=3` (봉인 전 실측)
- [ ] AR-02: B6 문서 쪽 함수 사본 — `python3 $M/b6-page-copy.py $W` 가 `diff=0` · 종료 코드 0 (SKILL.md `guide_gate` 와 `docs/onboarding-kit/setup-guide.html` 사본을 빈 줄 빼고 글자까지 맞댄다). 그 쪽도 `node $M/page-overflow.js $W docs/onboarding-kit/setup-guide.html` 이 `bad=0` [exact, enumerated]
  측정: 위 두 명령
  봉인 전 값: `COPY lines=90 page_lines=90 diff=0`
  양성 대조: 사본 쪽의 `blk_nourl=${blk_rest#* }` 를 `blk_nourl=X` 로 바꾸면 `diff=1` (봉인 전 실측)
- [ ] AR-03: B5 문서 쪽 표 — `python3 $M/b5-page-table.py $W` 가 `diff=0 only_one_side=0` · 종료 코드 0 (SKILL.md 음성 대조 표와 문서 쪽 표의 기대 칸을 시험 파일 이름마다 맞댄다) [exact, collective]
  측정: 위 명령
  봉인 전 값: `TABLE skill_rows=24 page_rows=24 diff=0 only_one_side=0`
  양성 대조: 문서 쪽 `[미검증]</code> 0 줄` 을 `9 줄` 로 바꾼 사본 → `diff=1` (봉인 전 실측)
- [ ] AR-04: 바뀐 경로와 커밋 모양 — Given 구현 커밋 뒤, `git -C $W diff --name-only $BASE..$TIP -- . ':(exclude).harness'` 의 모든 경로가 `## 범위 경계` 의 `# sprint-scope` 블록 안에 들고(블록 규칙: 끝이 `/` 면 그 폴더 아래 전부), `git -C $W log --format=%H $BASE..$TIP` 의 커밋마다 `git show --name-only --format= <커밋> | cut -d/ -f1 | sort -u | grep -c .` 이 1 이다 [exact, collective]
  측정: 위 두 명령, 블록 밖 경로 수 0 · 맨 위 폴더 둘 이상인 커밋 수 0. 상한은 가지 끝이며 `HEAD` 를 쓰지 않는다
  봉인 전 값: `$BASE..$TIP` 구간 커밋 0 개 (가지를 막 만들었다)

## Anti-patterns

- [ ] AP-03: bare code fence 금지 — `python3 scripts/validate-plugin.py --check=code-fence` 가 이번에 바뀐 킷(api-kit · howto-kit · planning-kit · react-kit · rust-kit · bambu-kit · onboarding-kit · tone-kit)에서 FAIL 0 (봉인 전 전체 실행 「14 plugins, 14 OK」)
- [ ] AP-04: frontmatter name 누락 금지 — `python3 scripts/validate-plugin.py --check=frontmatter` 가 같은 여덟 킷에서 FAIL 0

## Reusability

- [ ] RE-01: 다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다 — 새 레포 검사는 `scripts/`(project.yaml `reusability.shared_path`) 에 둔다. 측정: `test -f scripts/check-install-docs-guidance.py`
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다 — B11 안내 문장은 backend 선례 문장 모양(「설치본 플러그인에는 `docs/<칸>/` 가 없다 — … raw 주소 … 그래도 못 읽으면 … 못 읽었다고 적는다」)을 그대로 쓰고, B6 는 기존 `guide_gate` 함수 안에서 고치며 새 게이트 함수를 만들지 않는다. 측정: `grep -c '^guide_gate() {' onboarding-kit/skills/setup-guide/SKILL.md` → 1, `grep -cE '^[a-z_]+\(\) \{' onboarding-kit/skills/setup-guide/SKILL.md` 가 `$BASE` 판과 같다

## Diagnostics

- [ ] DG-01: N/A (commands.analyze 는 `bash -n scripts/release.sh` 만 잰다 — 이번 변경에 없다. 측정: `git -C $W diff --name-only $BASE..$TIP | grep -c '^scripts/release.sh$'` 이 0. 대신 SC-07 의 로컬 CI 와 `shellcheck bambu-kit/evals/run-gate-fixtures.sh` · `shellcheck -s bash <추출한 guide_gate>` 경고 0 을 잰다 — 봉인 전 둘 다 0)
- [ ] DG-02: IDE diagnostics 워닝/인포 0개 ([] 제외) — 이번에 바꾼 `.md` 파일마다 markdownlint(MD013 끔) 건수가 `$M/md-before.txt` 의 봉인 전 값 이하이고, 그 목록에 없는 파일은 0 건이다. 봉인 전 값: 64 파일 중 `api-kit/skills/api-ui/SKILL.md` 25 · `bambu-kit/skills/bambu-print-profile/SKILL.md` 120 · `onboarding-kit/skills/setup-guide/SKILL.md` 2, 나머지 0. 측정: `node $ML --config <설정> <바뀐 .md 파일…>` 출력의 `경로:줄` 을 파일별로 센다 · `Linting: <n> files` 줄이 있어야 검사가 돈 것이다
- [ ] DG-03: N/A (commands.test 대상도 `scripts/release.sh` 라 이번 변경에 없다. 측정: DG-01 과 같은 명령. 대신 SC-01 · SC-04 · SK-02 의 시험 실행을 잰다)
- [ ] DG-04: 실제 앱/서버 구동 시 에러 0개 — 구동하는 것은 예시 화면 `api-kit/evals/fixtures/unjudged/.api/ui.html` 하나다. `api-kit/evals/api-ui.spec.js` 의 콘솔 error 0 확인(favicon.ico 제외)이 1280 · 375 × 밝은 · 어두운 네 조합에서 통과한다. 측정: SK-02 의 실행 결과
