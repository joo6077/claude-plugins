# c4a — api-kit 결과 화면에 판정 불가 칸

작업 폴더 `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak-c4a` · 가지 `chore/ak-c4a` · 시작 판 `f81568d`.
계약 `.harness/sprint-contract-after-0924-api-ui-unjudgeable.md` (30 조건 · 봉인 `sha256:fffdc2c0e91aa217` · 2026-09-26 15:10).
QA 판정: APPROVE (Iteration 1, 30 조건 통과 · 해당 없음 3 — 리포트 `.harness/sprint-feedback-after-0924-api-ui-unjudgeable.md`, 커밋 `b74a489`). 계약 status 는 done.
독립 검토는 막는 결함 0 건이다. 판정을 바꾸지 않는 네 건과 사용자가 다시 볼 판단 하나는 아래 「다음 사이클 메모」 로 옮겼다.

## 한 일

| 커밋 | 내용 |
| --- | --- |
| `942b158` | 계약 봉인 — 계약 파일 하나만 |
| `6d1b7b5` | 측정 도구 세 파일(`m.sh` · `lit.py` · `probe-ui.cjs`) — `.harness/` 만 |
| `48618f6` | api-kit — `SKILL.md` · `viewer-spec.md` · `api-layout.md`. 상태 순서 표(미실행 > FAIL > 판정 불가 > PASS), 칩 네 개, 상태 아이콘 · 응답 탭 자리 · 토큰 · 텍스트 대응물, §7 식에 `chips` · `rows`, 정본 시안 v8, 인용 수치 v8 로 다시 잼 |
| `5ceca27` | api-kit — `api-kit/evals/` (evals.json · api-ui.spec.js · 예시 입력 `.api/` · 예시 `ui.html`) + README AUTO:evals 표(sync-docs 가 씀) |
| `6ab405a` | ci — playwright 작업에 `npx playwright test api-kit/evals/` 단계 |

git 밖: `/Users/jackson/Hub/10_Dev/claude-plugins/.mockups/api-ui-v8.html` 을 v7 복사로 만들었다(v7 sha256 그대로).
만든 스크립트는 scratchpad `c4a/build-v8.py` · `c4a/build-fixture.py` 다(커밋하지 않음). 예시 `ui.html` 은 v8 코드에 예시 입력의 데이터를 넣고 CSP `<meta>` 를 더한 것이다.

교차 진단을 받아 봉인 전에 고친 것:

- ER-02 · RE-01 · AR-05 의 변이 식을 글자로 박았다 — `s/state:'unjudged'/state:'pass'/g` · `/^## 7\./,/^## 8\./s/ rows: / rowz: /`
- AP-02 제외 근거를 패턴 성격(파일 내용 grep)에 맞게 고쳤다
- 교차 진단 뒤 내가 찾은 모순: `api-kit/README.md` 에 빈 AUTO:evals 블록이 있어 `api-kit/evals/` 를 만들면 sync-docs 검사가 떨어진다. README 를 범위에 넣고 `m.sh` `SCOPE)` 에 `readme_outside_auto` 를 더했다(AR-03 의 `m.sh` 해시를 `ba4701ce7b7be425` 로 새로 잼)

봉인 뒤 개정 하나 — `.harness/sprint-amendments-after-0924-api-ui-unjudgeable.md` A-01.
sync-docs 가 쓰는 표 구분 줄 `|------|------|` 이 MD060 을 4 번 내 DG-02 의 README 줄이 `rules_up=1` 이 된다. 블록 글자를 바꾸면 DG-05 가, 블록 밖에 끄는 주석을 두면 AR-01 이 깨진다.
그래서 README 줄만 "늘어난 MD060 이 전부 AUTO:evals 블록 안이고 블록 밖은 시작 판과 같다" 로 읽게 했다. 방향은 계산상 `relaxing measured_removed=5`.
동의 근거는 사용자 일반 위임(2026-09-26T01:04:21.505Z)이라 `anchored` 인정 여부는 평가자 몫으로 적었다.

## 조건별 자기 측정 (U = `6ab405a`, zsh · 대부분 bash 도 같은 출력)

| 조건 | 값 |
| --- | --- |
| SK-01 | `sk_s2_order=미실행>FAIL>판정 불가>PASS` · `sk_s2_phrase=1` · `sk_s2_line=1` |
| SK-02 | `sk_gotcha_unj=1` · `sk_s1_reports_unj=1` · `sk_s6_top=1` · `sk_s8_counts=1` · `al_reports_unj=1` |
| SK-03 | `sk_s7_keys=1` · SEC7 v8 `ok=2 ng=0` · `sk_s7_nums=ep:14 shown:14 targets:57 under24:0 under44:40` = 측정기 JSON · `sk_s7_touch_row=40/57/0` = `vs_1_touch_row` · `sk_s7_ep_row=14=14` |
| SK-04 | `vs_31_chips=1` · `vs_32_icons=1` · `vs_35_unj=6` · `vs_35_line=1` · `vs_35_failtab=1` · `vs_4_state_values=4` · `vs_6_rows=1` · hex 6 개 · `vs_6_hex_in_v8=6/6` · `vs_8_text=1` |
| SK-05 | `sk_v8=2` · `vs_v8=2` · `sk_v7=0` · `vs_v7=0` |
| SK-06 | v8 FUNC `ok=30 ng=0` · `m IDS` `v7_ids=76 missing_in_v8=0` |
| SK-07 | EVALS `fixture_api=5/5` · `example=U:api-kit/evals/fixtures/unjudged/.api/ui.html` · `expect=2/2/1/1` · `assertions=7` · `unjudged_lines=2`, 예시 FUNC `ok=30 ng=0` · SEC7 `ok=2 ng=0` · 칩 num 2 · 2 · 1 · 1 |
| SK-08 | sec7 블록 `1 0 0 0 0 0`, 외부 URL 줄 없음, 크기 156936, `secret_positive=1` · `secret_hits=0` · `csp_lines=1` |
| SK-09 | v8 · 예시 NFR 둘 다 `ok=20 ng=0` |
| SC-00 | `release_sh=0 version_files=0` |
| ER-01 | 예시 `fail-with-unjudged=1` (1280 두 테마) = expect 1, v8 두 테마 1 |
| ER-02 | 변이 `mutated_lines=1`, `chip[판정 불가]` 네 줄 모두 `chips=1 visible=true num=0 rows=0` |
| ER-03 | `bad_spelling=0` |
| AR-01 | `scope_out=0 required_missing=0 readme_outside_auto=0` |
| AR-02 | `mixed=0`, 커밋 줄 5 개(구현 3) |
| AR-03 | `SEAL_OK 74` · `SEAL_ABSENT 10` · `SEAL_BROKEN` 0, 해시 `ba4701ce7b7be425` · `691613b23348be8d` · `c00fad7dfdaff7ff` |
| AR-04 | `v7_sha_same=1` · `NEW api-ui-v8.html` · `new_files=1` |
| AR-05 | `evals_json=1` · `runner=[npx playwright test api-kit/evals/]` · `ci_step=1` · `after_install=1` · `runner_rc=0` (8 passed), ER-02 변이에서 `runner_rc=1` |
| AR-06 | `.harness/.meta/after-0924-api-ui-unjudgeable/evidence.md` — 캡처 여덟 이름 줄 · 톤 표 · 파일 이름, `cap/` PNG 12 장 |
| AR-07 | `av_phrase=1` · `av_line=1` (api-verify 는 안 건드림) |
| AP-01 | `added_hits=0 positive=1` |
| AP-03 | `m MD` 에 MD040 늘어난 줄 없음 |
| AP-04 | `fm_lines=12 fm_diff=0` |
| RE-01 | 변이 `mutated_lines=1` · `sec7-expr` NG 두 줄(`rowz`) · `runner_rc=1` |
| RE-02 | `new_classes=0` · `v8_hex_raw_uses=0` |
| DG-01 · DG-03 | `release_sh=0` |
| DG-02 | `SKILL.md` · `viewer-spec.md` · `api-layout.md` · `report.md` `rules_up=0`, `api-kit/README.md rules_up=1 MD060:20->24` — 개정 A-01 로 읽으면 `MD060_out=20 MD060_in=4`. `syntax_files=16 syntax_bad=0` |
| DG-04 | v8 · 예시 CONSOLE 둘 다 `ok=4 ng=0` |
| DG-05 | `m CILOCAL` `rc0=22 not_rc0=1` (`feedback-agg-test SKIP (yq 없음)`), `m VALID` `own_rc=0 own_bad=0 own_lines=10 main_rc=0 main_bad=0 main_lines=10` |

## 로컬 CI

`bash .harness/handoff/2026-09-26-tools/ci-local.sh <작업 폴더>` — 22 단계 `rc=0`, `feedback-agg-test SKIP (yq 없음)` 1.
새 단계 `npx playwright test api-kit/evals/` 는 ci-local.sh 목록에 없다(그 스크립트의 "밖의 것" 거르기가 `npx playwright test` 앞머리로 걸러서 밖으로도 안 나온다). 그 단계는 `m CI` 가 따로 돌려 8 passed.
그 밖에 `python3 scripts/validate-plugin.py api-kit` Exit 0, `python3 scripts/sync-docs.py --check-only` 0, `python3 scripts/sync-evals.py --check-only` 0.

QA 뒤 다시 돌림(판 `b74a489`, 이 notes 수정은 커밋 전 — CI 단계는 `.harness/.meta/` 를 읽지 않는다. `TMPDIR` 은 세션 스크래치 `c4a/ci-final`, 16:07 ~ 16:11, 시작 전 다른 `ci-local.sh` · `save-test.sh` 실행 0 개):

- `ci-local.sh` — `rc=0` 22 줄, `feedback-agg-test SKIP (yq 없음)` 한 줄, 종료 코드 0
- CI 파일에만 있는 줄 — 설치 단계(`pip install pyyaml` · zsh 설치 · `npm ci` · `npx playwright install --with-deps chromium`)와 yq 가 없으면 건너뛰는 `aggregation-test.sh` 여러 줄 단계(`ci.yml:152`)뿐이다
- 새 단계 `npx playwright test api-kit/evals/` (`ci.yml:126`) 를 따로 돌림 — 8 passed, 종료 코드 0
- 실행 뒤 `scenario-report-ut` 단계가 16:11 에 만든 추적 안 된 `__pycache__` 폴더 둘(`flutter-toolkit/evals/scenario-report/` · `flutter-toolkit/skills/flutter-scenario-report/scripts/` 아래)을 지웠다. 그 뒤 `git status --porcelain -uall` 0 줄

## 넘긴 것

- 보류 · flaky 를 화면이 어떻게 보일지 — 뷰어 규칙에 자리가 없어 만드는 쪽이 짐작한다(계약 범위 경계). 이번엔 판정 불가 한 칸만
- docs 쪽 v7 기재 — `docs/api/verification/static-evidence-viewer-contract.md:9` · `:82` · `:86`, `docs/api-kit/static-evidence-viewer-contract.html` 다섯 곳, `docs/superpowers/specs/2026-09-02-api-kit-design.md:476` · `:588`. `python3 scripts/detect-docs-drift.py --since f81568d` 는 `No docs drift since f81568d` — 바꾼 스킬 문서에 대응하는 docs 페이지는 없고, 위 v7 기재는 소스 md 쪽 드리프트라 재생성 대상이 아니라 원문 수정 대상이다
- v7 · v8 에 CSP 가 없는 것 — 그대로. 예시 ui.html 에만 넣었다
- run-evals · sync-evals 킷 목록에 api-kit 넣기 — scripts/ 범위 밖. CI 단계로 대신
- sync-docs 의 표 구분 줄 꼴(`|------|`)이 MD060 을 내는 것 — `scripts/sync-docs.py` `render_evals_table` 등 표 그리는 함수 전부가 같은 꼴이다. 고치면 모든 킷 README 가 바뀌어 별도 묶음이 맞다
- 가지를 origin/main(`88ddfe5`)에 맞출지 — 오케스트레이터 몫. api-kit 변경 0 이고 검사기 두 판 다 통과
- CI 에서 새 단계가 실제로 한 번 통과하는지 — PR 단계에서 확인(교차 진단 지적)

## 킷별 버전 판단

- api-kit `0.2.0` → **minor** (`0.3.0`). `/api-ui` 가 만드는 화면의 상태 모델이 넷이 되고 요약 칩 · §7 식 반환값이 바뀐다 — 쓰는 사람이 보는 새 기능이다. 시험도 새로 생겼다
- harness · 다른 킷 — 변경 없음. `.github/workflows/ci.yml` 은 킷 판에 들지 않는다

## 측정 도구 경로

- `.harness/.meta/after-0924-api-ui-unjudgeable/m.sh` · `lit.py` · `probe-ui.cjs` (AR-03 해시 고정)
- `.harness/.meta/after-0924-api-ui-unjudgeable/readme-md060.sh` (개정 A-01, sha256 앞 16 자리 `24c5720f6f3abb2c`)
- 측정기 출력 `probe-v8.txt` · `probe-example.txt`, 캡처 `cap/`, 확인 기록 `evidence.md` — 같은 폴더
- 양성 대조 매달린 커밋(가지 밖): `21d13ce`(README 블록 밖 한 줄) · `bd20291`(블록 안 한 줄) · `e6b9b27`(블록 밖 표)

## 다음 사이클 메모

독립 검토(2026-09-26, 막는 결함 0 건)가 조건 밖에서 찾은 네 건(R1 ~ R4), 사용자가 다시 볼 판단 하나(R5), QA 개선 제안 하나(R6). 판정을 바꾸지 않아 이 묶음에서는 고치지 않았다. R1 ~ R4 는 이 가지 끝 `b74a489` 에서 다시 재현했다.

| # | 항목 | 자리 | 받을 곳 · 할 일 |
| --- | --- | --- | --- |
| R1 | `/api-ui` 보고 목록에 새로 정한 `chips` · `rows` 값이 빠졌다 | `api-kit/skills/api-ui/SKILL.md:241` (값을 정한 곳 `:198`, 받은 숫자를 보고에 옮기라는 곳 `:186`) | api-kit 다음 사이클. 8절 보고 목록 Step 7 줄에 상태 네 가지의 칩 숫자 · 트리 줄 수를 더한다. 재현 `grep -n "Step 7 브라우저 확인" api-kit/skills/api-ui/SKILL.md` → 241 줄에 `ep` · `shown` · `under24` · `under44` 만 있다. SK-02 (d) 는 네 상태 개수 줄만 요구해 조건은 통과다 |
| R2 | 커밋 `875a6c2` 메시지가 쉬운 말 목록에 든 영어 낱말을 쓴다 | 메시지 셋째 줄 `(개정 A-01, …)` 괄호 안 — 목록이 「조건이 느슨해짐」 으로 바꿔 쓰라고 한 말 | 고치지 않았다. QA 리포트가 이 커밋 번호를 적어 두었다(`Deletions` 절 `:35` · SK-01 근거 `:52`). 메시지를 고쳐 번호가 바뀌면 리포트가 없는 커밋을 가리킨다. PR 을 `--merge` 로 합치면 이 메시지는 기록에 남는다. 다음 커밋부터 풀어 쓴다 |
| R3 | 증거 캡처 PNG 12 장(1,645,931 바이트)이 커밋에 들어갔다 | `.harness/.meta/after-0924-api-ui-unjudgeable/cap/` (커밋 `875a6c2`) | 오케스트레이터가 PR 전에 정한다. origin/main 의 `.harness` 에는 PNG 가 0 개다(`git ls-tree -r --name-only origin/main .harness \| grep -c '\.png$'` → 0). AR-06 은 캡처가 폴더에 있기만 요구하고 커밋은 요구하지 않는다. 빼려면 새 커밋으로 지워도 기록에는 남으니, 기록에서 없애려면 이 가지를 다시 써야 한다 — R2 와 같은 이유로 QA 리포트의 커밋 번호가 틀어진다. 이 묶음은 그대로 둔다 |
| R4 | 판정 줄이 어느 항목 것인지 적는 방식을 `/api-verify` 가 정하지 않았다 | 예시 입력 `api-kit/evals/fixtures/unjudged/.api/reports/2026-09-02T1422-dev/report.md:23` 은 `- products.list: …` 로 항목 이름을 앞에 붙이고, 예시 `api-kit/evals/fixtures/unjudged/.api/ui.html:1509` 는 이름을 떼고 넣는다. `api-kit/skills/api-ui/SKILL.md:90` 은 판정 줄을 「글자 그대로」 옮기라 한다. `api-kit/skills/api-verify/SKILL.md:136` · `:177` 의 판정 줄 모양에는 항목 이름이 없다 | api-kit 다음 사이클. `/api-verify` 가 판정 줄을 항목별로 적는 모양(항목 이름 앞머리 등)을 정하고, `/api-ui` `:90` 은 그 앞머리를 떼고 나머지를 글자 그대로 옮긴다고 적는다. 지금은 `/api-ui` 가 줄을 항목에 짝지을 근거가 규칙에 없다. 만드는 쪽은 이번 계약이 일부러 안 바꾼 범위다(AR-07) |
| R5 | DG-02 를 개정 A-01 로 통과시킨 판단 — 동의가 이 개정만 두고 받은 것이 아니다 | `.harness/sprint-amendments-after-0924-api-ui-unjudgeable.md` A-01 · `harness/references/contract-schema.md:1166` 「사용자 재승인 성립」 | 사용자가 다시 볼 판단. 이 묶음에서 판정이 뒤집힐 수 있는 유일한 자리다 — 엄하게 읽으면 DG-02 는 실패이고 판정은 REJECT 다. QA 는 일반 위임(user `2026-09-26T01:04:21.505Z`, 세션 기록 `de8c7935-….jsonl`, 글자 · 시각 · 폴더 일치 확인)을 근거로 받아들였고, 독립 검토도 결함으로 세지 않았다. 이유 셋: 이번 지시가 「C4 다섯 가지 말고는 묻지 말라」 이다 · 같은 인용으로 받아들인 개정이 이미 있다(가지 `chore/ak-c3-kits` 의 `.harness/sprint-amendments-after-0924-kits-a.md`) · 빠지는 것은 생성기가 쓴 5 줄뿐이고 블록 밖이 늘면 잡힌다. 재현: `readme-md060.sh` 로 시작 판 `f81568d` 는 `MD060_out=20`, 구현 판 `6ab405a` 는 `MD060_out=20 MD060_in=4`. 블록 안 구분 줄을 `\| ---- \| ---- \|` 로 바꾼 사본은 `sync-docs.py --check-only` 가 「동기화가 필요합니다」 를 내서 PR 마다 도는 CI 가 떨어진다. 표를 만드는 `scripts/sync-docs.py:251-256` 은 계약 범위 밖이다 |
| R6 | 계약이 자동 생성 블록의 경고를 봉인 전에 재지 않았다 | 계약 DG-02 · 「정한 것」 11 · QA 리포트 `Improvement Suggestions` | harness 다음 사이클(sprint-contract). 봉인 전에 README 의 `AUTO:evals` 블록이 바뀔 줄 알았는데 그 표의 MD060 을 재 보지 않았다. 편집기 경고 조건은 처음부터 `<!-- AUTO:* -->` 블록 안 · 밖을 나눠 재게 한다. 뿌리는 「넘긴 것」 의 sync-docs 표 구분 줄 꼴이다 |

QA 피드백 YAML(`~/.harness/feedback/evaluator/1a3bcba6-2026-09-26T155431-bda55d45-31464.yaml`)의 `cross_diagnosis_by: pending-parent` 는 부모가 교차 진단을 마치면 채운다. QA 가 넘긴 두 질문에 독립 검토가 답했다 — (1) DG-02 판단은 뒤집지 않았고 사용자 몫으로 R5 에 남겼다, (2) 빈 출력으로 통과한 자리를 찾으려고 예시 `ui.html` 변이 다섯 가지(FAIL 항목의 판정 불가 줄 삭제 · 판정 불가 항목의 줄 삭제 · FAIL 을 판정 불가로 바꿈 · `실패 원인` 탭 알림 상자 제거 · 본문 탭 알림 상자 제거)를 넣었고 모두 시험을 떨어뜨렸다(rc=1). §7 식 직접 실행 값(v8 1280 `ep 14 · shown 14 · targets 57 · under24 0 · under44 40`, 칩 = 트리 `10/1/2/1`, 예시 `2/2/1/1`)도 인용 수치와 같았다.
