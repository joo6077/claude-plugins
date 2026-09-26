---
feature: "api-kit 결과 화면에 네 번째 상태 「판정 불가」 칸 — 생성 규칙 · 뷰어 스펙 · 시안 v8 · 시험"
slug: after-0924-api-ui-unjudgeable
created: "2026-09-26 14:47"
complexity: "복잡"
conditions: 30
status: active
owner_session: bda55d45-296c-491f-89ba-b52042d58e72
conditions_digest: sha256:fffdc2c0e91aa217
locked_at: "2026-09-26 15:10"
---

## 배경

`/api-verify` 는 경로 간 불변식의 한쪽 경로가 없으면 그 판정 줄을 `판정 불가` 로 따로 센다(`api-kit/skills/api-verify/SKILL.md:136`, 실패 분류 `failure-taxonomy.md:107` · `:159`).
그런데 결과 화면을 만드는 `/api-ui` 는 상태를 PASS · FAIL · 미실행 셋만 안다(`api-kit/skills/api-ui/SKILL.md:64` · `:123` · `:208`, 뷰어 스펙 `viewer-spec.md:77` · `:86` · `:225` · `:340`).
그래서 판정 불가 엔드포인트를 화면에 옮길 자리가 없고, 만드는 쪽이 PASS 에 합치기 쉽다 — `/api-verify` 가 「판정 불가 를 PASS 에 합치면 경로가 사라진 회귀가 조용히 지나간다」 고 막아 둔 바로 그 일이다.

사용자 결정: 2026-09-26 이 세션(`bda55d45-296c-491f-89ba-b52042d58e72`)의 AskUserQuestion 에서 「네 번째 칸 따로」 를 골랐다.
계약 합의는 사용자 위임으로 받은 것으로 적는다 — 사용자 2026-09-26T01:04:21.505Z 「다음 세션에서 직접할 일을 다 실행하고 이어질것도 실행해」(세션 기록 `/Users/jackson/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/de8c7935-a5b6-4df5-9106-fafa73c288a0.jsonl`), 그 전 2026-09-24T04:04:16.964Z 「나한테 물어보지 말고 자동으로 끝까지」.
판단이 갈린 곳은 아래 「정한 것」 에 저장소 안 근거와 함께 적었다. 저장소 밖 원문이 있어야 정할 수 있는 것은 없었다.

복잡도 4 축 (Step 1):

| 축 | 물음 | 값 |
| -- | ---- | -- |
| 레이어 수 | 생성 규칙 문서 · 뷰어 스펙 · 생성물(HTML 안 코드) · 시험 · CI | 예 — 넷 이상 |
| 공개 API·계약 변경 | 뷰어의 상태 모델(state 값 · 요약 칩 수)이 바뀐다 | 예 |
| 소비면 존재 | `/api-verify` 리포트를 `/api-ui` 가 읽는다. 생성된 `ui.html` · 시험이 그 규칙을 따른다 | 예 |
| 회귀 위험 | 기존 세 상태 칩 · 필터 · §7 인용 수치 · v7 기능 | 예 |

네 축이 다 「예」 라 「복잡」 이다. 공개 모델 변경과 소비면이 함께 있어 Step 2.5 반대편 조건(AR-07)을 둔다.

설정 리터럴 대조표 (Step 1.2):

| config key | project.yaml 에서 읽은 값 | 계약에 쓴 값 |
| ---------- | ------------------------- | ------------ |
| `commands.analyze` | `bash -n scripts/release.sh` | DG-01 N/A 사유에 그대로 |
| `commands.test` | `bash scripts/release.sh 2>&1 \|\| true` | DG-03 N/A 사유에 그대로 |
| `diagnostics.ide_exclude` | `[]` | DG-02 `[]` |
| `contract_categories[].id` / `prefix` | Skill/SK · Script/SC · Error/ER · Architecture/AR | 네 절 그대로 |
| `anti_patterns[].id` / `message` | AP-01 · AP-02 · AP-03 · AP-04 | AP-01 · AP-03 · AP-04 선별. AP-02(force push)는 변경 파일 내용에서 `git push.*--force` 글자를 찾는 패턴 검사인데, 이번에 바꾸는 파일(md · html · js · json · yaml)에 그 글자가 들어갈 자리가 없어 뺐다 |

정한 것 (판단과 근거):

1. **범례는 새 영역이 아니다.** 요약 칩 네 개와 스펙의 상태 ↔ 글자 대응(§3.2 상태 아이콘 · §8 텍스트 대응물)에 네 번째를 넣는다. 근거: `SKILL.md:118` 「시안에 없는 영역을 발명하지 마라」, v7 에 상태 범례 영역이 0 이다(`.legend` 는 `api-ui-v7.html:2335-2336` 의 「정규화됨 · 추가 검사」 둘뿐).
2. **상태는 위에서부터 먼저 맞는 줄로 정한다 — 미실행 > FAIL > 판정 불가 > PASS.** FAIL 이 판정 불가를 이긴다. 판정 불가는 그 자체로 게이트를 깨지 않고(`api-verify/SKILL.md:136`) 계약 실패만 게이트를 깨기 때문이다(`:151`). FAIL 로 분류된 엔드포인트에 판정 불가 줄이 있으면 `실패 원인` 탭에 함께 둔다 — 줄을 버리지 않는다.
3. **요약 칩 숫자는 엔드포인트 수다(판정 줄 수가 아니다).** 칩을 누르면 트리를 그 상태로 거른다(`viewer-spec.md:77`) — 칩 숫자와 걸러진 줄 수가 같아야 한다. 숫자는 데이터에서 센다. v7 은 손으로 적었다(`api-ui-v7.html:1183` `<b>11</b>` · `:1890` `14`).
4. **판정 불가 칩은 0 이어도 보인다.** 빼면 커버리지 착시가 생긴다는 원칙이 이미 있다(`SKILL.md:34`).
5. **좁은 폭에서도 네 칩 모두 접근 이름에 상태 글자가 든다.** v7 은 1120px 아래에서 칩 글자를 `display:none` 으로 숨겨(`api-ui-v7.html:897` · `:927`) 375 에서 칩 이름이 숫자뿐이다(측정기 실측 `chip[PASS] chips=0`). 새 칩만 고치면 같은 칩에 두 방식이 생긴다(RE-02) — 네 칩을 같은 방식으로 고친다.
6. **정본 시안을 v8 로 옮긴다.** `viewer-spec.md:3-4` 가 「시안과 이 문서가 어긋나면 시안이 정본」 이라, v7 을 가리킨 채 두면 세 상태가 이긴다.
7. **시험은 `api-kit/evals/` 를 새로 두고 자체 실행기를 CI 에 잇는다.** `scripts/run-evals.py:32-35` · `scripts/sync-evals.py:32` 킷 목록에 api-kit 이 없어 `evals.json` 만 두면 아무도 안 돌린다. sync-evals 목록에 넣으면 api-kit 다른 스킬 넷의 빈 항목이 강제돼 범위를 넘는다. 선례: howto-kit 자체 실행기(`ci.yml:91-92`), design-kit Playwright 시험(`ci.yml:120-121`).
8. **새 색은 토큰(CSS 변수)으로 둔다** — `viewer-spec.md:300` 「역할로 참조한다 — 하드코딩 색을 컴포넌트에 직접 쓰지 마라」. 네 상태 색이 서로 달라야 칸을 따로 둔 뜻이 산다.
9. **팔레트 스코프는 그대로 4 종이다.** `fail` 은 FAIL 만 모은다(`viewer-spec.md:193`). 판정 불가 스코프는 요청 밖이라 더하지 않는다.
10. **판정 불가 줄은 응답 pane 의 맨 앞 탭에 둔다.** FAIL 이면 `실패 원인` 탭 안(정한 것 2), 판정 불가 단독이면 `본문` 탭 맨 위 알림 상자다. 근거: v7 이 본문 위 경고를 이미 같은 자리에 둔다(`api-ui-v7.html:2339` `pinBreakHTML`). 새 영역이 아니라 있는 알림 상자(`.callout`)에 `data-t` 값 하나를 더한다(RE-02).
11. **`api-kit/README.md` 는 `<!-- AUTO:evals -->` 블록만 바뀐다.** 교차 진단 뒤 실측으로 찾았다 — `api-kit/README.md:140-141` 에 빈 AUTO:evals 블록이 있어 `api-kit/evals/` 를 만들면 `python3 scripts/sync-docs.py --check-only` 가 종료 코드 1 을 내고(`scripts/sync-docs.py:418-420` · `:494-497`), CI `Sync docs check` 단계가 떨어진다. 그래서 `python3 scripts/sync-docs.py api-kit` 가 쓴 표만 받아들이고 블록 밖은 그대로 둔다(AR-01 의 `readme_outside_auto`).

## 리서치 소스

웹 검색 · 외부 문서 가져오기는 하지 않았다. 저장소 안 근거만 썼다.

- `api-kit/skills/api-verify/SKILL.md:133-137` — 판정 줄 모양 `$.meta.total=(없음) · len($.data)=10 → 판정 불가`, 판정 조건 「한쪽 경로라도 없으면 `판정 불가` 다」, PASS 에 합치지 말 것
- `api-kit/skills/api-verify/SKILL.md:171` · `:177` · `:206-208` — 집계에 `판정 불가` 를 따로 센다
- `api-kit/skills/api-verify/references/failure-taxonomy.md:107` · `:159` — JUnit 에서는 `skipped` + 없는 경로 이름, 게이트 미파괴
- `api-kit/skills/api-ui/SKILL.md` · `references/viewer-spec.md` · `api-kit/references/api-layout.md:52` — 지금 규칙
- `/Users/jackson/Hub/10_Dev/claude-plugins/.mockups/api-ui-v7.html` (git 밖, sha256 `c4bd563ec8b71a95f804ae1f96a0eda2d17bda8256ca9fbc327a527c3a81ca7a`) — 확정 시안
- `.harness/.meta/kaizen-0924/f1-kit-followups-notes.md:96` · `:148`, `phase16-notes.md:52` · `:145` · `:146` — 이 과제가 넘어온 자리
- 대비 기준 WCAG 2.2 (일반 글자 4.5:1 · 큰 글자 3:1 · 그림 요소 3:1) 은 `SKILL.md:159` · `viewer-spec.md:20` 에 이미 적힌 값을 쓴다. 대비 계산식은 `scripts/check-docs-a11y.js:74-76` 과 같은 상대 휘도 식

## GAP 분석

Pre-Edit Audit (Step 1.4) — 대상 파일을 실제로 열어 본 자리:

| 대상 파일 | 실제 Read 증거 (`파일:라인`) | 발견한 기존 갭·위반 | 계약 조건화 |
| --------- | ---------------------------- | ------------------- | ----------- |
| `api-kit/skills/api-ui/SKILL.md` | `:64` reports 행 PASS/FAIL/미실행 · `:123` 상단바 칩 셋 · `:158` · `:161` · `:191` v7 실측 수치 · `:180-189` §7 식(칩 · 줄 수 없음) · `:208` 보고 카운트 셋 · `:118` · `:219` v7 정본 · `## Gotchas` `:14-35` 판정 불가 0 | 네 번째 상태가 없다. 상태를 정하는 규칙이 없다 | SK-01 · SK-02 · SK-03 · SK-05 |
| `api-kit/skills/api-ui/references/viewer-spec.md` | `:3` · `:367` v7 정본 · `:19` 누르는 자리 39/56 · `:77` 칩 3 개 · `:86` 상태 아이콘 3 종 · `:133-145` 응답 탭 · `:225` state 세 값 · `:308` semantic 토큰 · `:340` 텍스트 대응물 셋 | 같음 | SK-03 · SK-04 · SK-05 |
| `api-kit/references/api-layout.md` | `:52` reports 행 `PASS/FAIL · 위반 목록 · canonical diff` | 소비 쪽 입력 설명에 판정 불가가 없다 | SK-02 (e) |
| `api-kit/skills/api-verify/SKILL.md` · `references/failure-taxonomy.md` | 위 리서치 소스 줄 | 생산 쪽 — 이번에 바꾸지 않는다 | AR-07 |
| `.mockups/api-ui-v7.html` (git 밖) | `:1180-1192` 칩 셋(숫자 손으로) · `:1360` pending 아이콘 · `:1753-1754` 상태 아이콘 · 글자 세 값 · `:1845` 필터 · `:1925` 고르면 탭 · `:2284` 실패 원인 탭 · `:897` · `:927` 좁은 폭 칩 글자 숨김 | 네 번째 상태 없음 · 375 에서 칩 이름이 숫자뿐 | SK-06 · SK-09 · ER-02 |
| `api-kit/evals/` | `find api-kit -type d -name evals` 0 건 | 시험 0 | SK-07 · AR-05 |
| `.github/workflows/ci.yml` | `:102-121` playwright 작업 | api-kit 단계 없음 | AR-05 |
| `scripts/run-evals.py` · `scripts/sync-evals.py` | `:32-35` · `:32` 킷 목록 | api-kit 없음 → 자체 실행기(정한 것 7) | AR-05 |

## 범위 경계

- 바꾸는 경로는 AR-01 기대 집합과 같다: `api-kit/skills/api-ui/SKILL.md` · `api-kit/skills/api-ui/references/viewer-spec.md` · `api-kit/references/api-layout.md` · `api-kit/README.md` (`<!-- AUTO:evals -->` 블록 안만 — 정한 것 11) · `.github/workflows/ci.yml` · `api-kit/evals/` 아래 새 파일. 그리고 git 밖 `/Users/jackson/Hub/10_Dev/claude-plugins/.mockups/api-ui-v8.html` 한 파일 — v7 을 **복사**해 만든다. v7 은 건드리지 않는다. 본 체크아웃에 쓰는 것은 이 한 파일뿐이다.
- 시험 배치: `api-kit/evals/evals.json` 에 `runner` (CI 에 넣은 명령과 같은 글자) 와 `cases` 를 둔다. api-ui 경우 하나 이상에 `skill: "api-ui"` · `fixture` (`api-kit/evals/fixtures/<이름>`, 그 안에 `.api/`) · `example` (그 입력으로 `/api-ui` 절차를 따라 만든 `ui.html`, `api-kit/evals/fixtures/` 아래) · `expect` (네 상태 이름을 키로 한 엔드포인트 수와 `fail_with_unjudged`) · `assertions` 를 둔다. 시험 파일은 `api-kit/evals/` 아래 Playwright 시험이다.
- 안 바꾸는 것: api-kit 다른 스킬(`api-verify` · `api-contract` · `api-probe` · `api-init`) · `api-kit/agents/` · `api-kit/README.md` 의 AUTO:evals 블록 밖 · `plugin.json` 판 번호(릴리스는 합친 뒤 다음 단계) · `docs/` · `scripts/`(run-evals · sync-evals 목록 포함).
- 드리프트(그대로 둔다 — notes 로 넘김): `docs/api/verification/static-evidence-viewer-contract.md:9` · `:82` · `:86`, `docs/api-kit/static-evidence-viewer-contract.html:269` · `:351` · `:541` · `:565` · `:639`, `docs/superpowers/specs/2026-09-02-api-kit-design.md:476` · `:588` 가 확정 시안을 v7 이라 적는다. `docs/api/research-log.md:179` 는 날짜 붙은 기록이라 고칠 대상이 아니다.
- 보류 · 들쭉날쭉(flaky) 을 지금 화면이 다루는 방식(바꾸지 않는다): 뷰어 state 는 세 값(`viewer-spec.md:225`)이고 `SKILL.md:64` 가 리포트를 PASS · FAIL · 미실행 으로만 옮긴다. `/api-verify` 가 따로 세는 보류(환경 실패 종료 코드 3 · 인증 실패 · 데이터 부재 — `api-verify/SKILL.md:100` · `:151`, `failure-taxonomy.md:47-49`)와 `flaky-confirmed`(`api-verify/SKILL.md:18` · `:160`)는 뷰어 규칙에 자리가 없어 만드는 쪽이 짐작한다. 이번에는 판정 불가 한 칸만 더한다.
- v7 에 CSP `<meta>` 가 없는 것(`phase16-notes.md:146`)은 v8 에서도 그대로 둔다. 생성 예시는 스펙(`viewer-spec.md:29-32`)대로 CSP 를 넣는다(SK-08).
- 기준 커밋: 이 작업 폴더는 `f81568d8fbf58382172281388ec5d7756f9f46b2` 에서 시작했다. origin/main 은 그 뒤 `88ddfe5` (#111 V10 · #112 harness 릴리스)로 움직였다 — api-kit 변경 0, `scripts/validate-plugin.py` 만 바뀌었다. DG-05 가 두 판 검사기를 다 돌린다. 가지를 main 에 맞출지는 오케스트레이터 몫이다.
- **측정 공통 전제 (조건마다 반복하지 않는다):** 모든 측정은 `cd /Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak-c4a` 뒤 `. .harness/.meta/after-0924-api-ui-unjudgeable/m.sh` 를 읽고 `m <이름>` 으로 부른다(아래 `$D` 는 그 폴더). `m` 은 상한 U 를 스스로 정한다 — 가지가 합쳐졌으면 origin/main 병합 커밋의 둘째 부모(합친 가지 끝), 아니면 가지 `chore/ak-c4a` 끝이다. 정하지 못하면 `UNRESOLVED` 로 멈춘다(`HEAD` 로 떨어지지 않는다). 바뀐 파일은 `BASE..U` 의 첫째 부모 줄에 있는 병합 아닌 커밋만 모은다 — 가지에 main 을 합쳐 넣거나 다시 얹어도 남의 변경이 섞이지 않는다. 글자 · 검사기 측정은 `git archive` 로 푼 U 판 사본에서 돈다(작업 폴더의 커밋 안 된 변경이 섞이지 않게). 측정기 출력은 먼저 두 번 받아 둔다 — `m PROBE v8 "$V8" > "$D/probe-v8.txt"` 와 `m PROBE example "<m EVALS 의 example= 값>" > "$D/probe-example.txt"`. 캡처는 `$D/cap/` 에 쌓인다. 끝나면 `m CLEAN`. `m CILOCAL` 은 따로 만든 사본에서 돌므로 도는 동안 `m CLEAN` 을 불러도 된다.
- zsh 에서는 `$변수:` 가 수식어로 읽힌다(실측: `$B:api-kit` 가 `:a` 로 읽혀 `git show` 가 죽었다) — 측정 명령을 손으로 쓸 때는 `${변수}:` 로 쓴다.
- markdownlint 는 편집기 확장과 같은 markdownlint-cli2 0.23.2 · MD013 끔으로 잰다(`m MD` 가 찾는 자리: 이 세션 scratchpad `c4a/mdlint`, 없으면 `MDL=<폴더>` 로 가리킨다 — 그 폴더에서 `npm install --no-save markdownlint-cli2@0.23.2` 와 `{ "config": { "MD013": false } }` 설정 파일).
- 측정기의 `channel: 'chromium'` 은 로컬 측정용이다. 새 CI 단계는 `playwright.config.js` 의 기본 chromium 으로 돈다 — CI 에서 실제로 한 번 통과하는지는 PR 단계에서 오케스트레이터가 본다(교차 진단 지적).
- 측정 도구 세 파일(`$D/m.sh` · `$D/lit.py` · `$D/probe-ui.cjs`)은 계약 작성 때 만들었고 AR-03 이 sha256 을 잠근다. 교차 진단 뒤 `m.sh` `SCOPE)` 에 `api-kit/README.md` 와 `readme_outside_auto` 를 더해 AR-03 의 첫 값을 새로 쟀다. 구현이 새로 만드는 시험과 따로 돈다 — 구현 값을 가져다 쓰지 않는다.

## 회귀 게이트

봉인 전에 실제로 돌린 기준값과 대조(2026-09-26, bash · zsh 둘 다 같은 출력):

- CI 단계 전부 — 작업 폴더에서 `ci-local.sh` 22 단계 `rc=0`, `feedback-agg-test SKIP (yq 없음)` 1
- `python3 scripts/validate-plugin.py api-kit` — 이 판 · origin/main `88ddfe5` 판 둘 다 V1 ~ V10 열 줄이 `— OK` 또는 `— SKIP (no templates/)`, `Exit: 0`
- markdownlint(0.23.2 · MD013 끔) 기존 경고 수 — `SKILL.md` 25 · `viewer-spec.md` 45 · `api-layout.md` 26
- `m SEAL` 시작 판 — `SEAL_OK` 73 · `SEAL_ABSENT` 11 · `SEAL_BROKEN` 0
- `m LIT` 시작 판 — `sk_s7_nums=ep:14 shown:14 targets:56 under24:0 under44:39` · `sk_s7_touch_row=39/56/0` · `sk_s7_ep_row=14=14` · `vs_1_touch_row=39/56/0` · `vs_4_state_values=3` · `av_phrase=1` · `av_line=1` · `sk_v7=2` · `vs_v7=2` · `bad_spelling=0`, 나머지 0 또는 `-`
- `m SCOPE` 시작 판 `scope_out=0 required_missing=6 readme_outside_auto=0` · `m COMMITS` `mixed=0` · `m MOCKUPS` `v7_sha_same=1 new_files=0` · `m NA` `release_sh=0 version_files=0` · `m VER` `added_hits=0 positive=1` · `m FM` `fm_lines=12 fm_diff=0` · `m EVALS` `evals_json=0` · `m CI` `evals_json=0`
- 측정기를 v7 사본에 — `VERDICT v7 FAIL ng=36 checks=54`, `m COUNT` 로 `FUNC ok=12 ng=18` · `NFR ok=2 ng=16` · `CONSOLE ok=4 ng=0` · `SEC7 ok=0 ng=2`, §7 식 결과 `ep 14 · shown 14 · targets 56 · under24 0 · under44 39` (SKILL.md 인용과 같다)
- 알려진 답: 손으로 만든 네 상태 화면(PASS 2 · FAIL 1 · 미실행 1 · 판정 불가 1, FAIL 이 판정 불가 줄을 가진 경우 1)에 측정기 — 칩 숫자 `2 · 1 · 1 · 1` · `sum=5` · `filtered=1` · `fail-with-unjudged=1` · `VERDICT PASS ng=0 checks=54` (식 없이). 같은 모양의 손 트리에 `lit.py` — 기대한 값 그대로(`sk_s2_order=미실행>FAIL>판정 불가>PASS` · `vs_4_state_values=4` · `vs_6_hex_in_v8=2/2` · `v8_hex_raw_uses=1` 등). 손으로 만든 예시 입력에 `m EVALS` — `fixture_api=5/5` · `expect=2/1/1/1` · `unjudged_lines=2`
- 양성 대조(0 이 기대값인 측정이 나쁜 예에서 1 이상을 내는지): 가지를 건드리지 않고 만든 매달린 커밋 `a11927e` (SKILL.md 에 언어 없는 코드 블록 · `판정불가` · README · ci.yml · release.sh 를 한 커밋에) 에서 `scope_out=2` · `mixed=1` · `release_sh=1` · `SKILL.md rules_up=3 MD022 MD031 MD040` · 검사기 `own_bad=1 main_bad=1`, `cec7867` 에서 `ci_step=1 after_install=1 runner_rc=3`, `6d28adc` 에서 `syntax_bad=2`, `53cb8ff` 에서 예시 변이 `rows=0` 인데 칩 `num=1` 이라 NG, 봉인 틀린 사본에서 `SEAL_BROKEN 1`, `.mockups` 사본에 파일 하나 더 두면 `new_files=2`, id 하나 바꾸고 클래스 하나 더한 사본에서 `missing_in_v8=1 new_classes=1`, `FM` 에 변이를 끼우면 `fm_diff=2`, 비밀 모양 `secret_positive=1`, v7 사본 측정기 NG 36 (위), 교차 진단 뒤 만든 매달린 커밋 `21d13ce` (`api-kit/README.md` 의 AUTO:evals 블록 밖에 한 줄) 에서 `readme_outside_auto=2` — 블록 안에만 한 줄 넣은 `bd20291` 은 `IN  api-kit/README.md` · `readme_outside_auto=0` (bash · zsh 같은 출력)
- 음성 대조(구현을 무력화하면 측정이 떨어지는지): 손 화면에서 판정 불가를 PASS 로 합친 변이 — `VERDICT FAIL ng=22`, 판정 불가 색을 미실행 색으로 바꾼 변이 — `row-glyph-distinct` NG, 판정 불가 칩 이름을 「보류」 로 바꾼 변이 — `chip[판정 불가]` · `filter` NG

## Skill

- [ ] SK-01: 상태를 정하는 규칙이 `/api-verify` 와 글자까지 맞는다 — Given 이 스프린트 커밋이 끝난 U 판 · When `m LIT` · Then `api-kit/skills/api-ui/SKILL.md` 의 `## 2. 데이터 모델 조립` 절에 첫 칸이 `미실행` · `FAIL` · `판정 불가` · `PASS` (백틱으로 감싼 이름)인 표 줄이 이 순서로 있고(위 줄부터 먼저 맞는 줄로 정한다 — FAIL 이 판정 불가를 이긴다), 같은 절에 `/api-verify` 판정 조건 글자 「한쪽 경로라도 없으면」 과, `(없음)` · `→ 판정 불가` 가 한 줄에 든 판정 줄 예가 있다 [exact] (측정: `m LIT` 의 `sk_s2_order=미실행>FAIL>판정 불가>PASS` · `sk_s2_phrase` 1 이상 · `sk_s2_line` 1 이상. 시작 판 `-` · `0` · `0`. 알려진 답: 손 트리에서 `미실행>FAIL>판정 불가>PASS` · `1` · `1`)
- [ ] SK-02: 생성 규칙의 나머지 다섯 자리에 네 번째 상태가 들어간다 — (a) `SKILL.md` `## Gotchas` 에 `판정 불가` 가 든 굵은 머리 불릿(`- **`) (b) `## 1. 입력 수집` 표의 `reports/` 행에 `판정 불가` (c) `## 6. 렌더` 골격의 `상단바` 줄에 네 이름(`PASS` · `FAIL` · `미실행` · `판정 불가`) (d) `## 8. 열기와 보고` 에 네 이름이 든 불릿 (e) `api-kit/references/api-layout.md` 의 `reports/` 행(`/api-verify` → `/api-ui`)에 `판정 불가` [exact, enumerated] (측정: `m LIT` 가 U 판 `SKILL.md` 에서 `sk_gotcha_unj` 1 이상 · `sk_s1_reports_unj=1` · `sk_s6_top=1` · `sk_s8_counts` 1 이상, `api-kit/references/api-layout.md` 의 `reports/` 행(칸 `/api-verify` · `/api-ui`)에서 `al_reports_unj=1`. 시작 판 다섯 값 모두 0)
- [ ] SK-03: `SKILL.md` §7 브라우저 식이 네 상태의 칩 숫자와 트리 줄 수를 돌려주고, 인용한 실측 수치가 v8 에서 잰 값과 같다 — Given U 판과 `.mockups/api-ui-v8.html` · When `m PROBE v8 "$V8" > "$D/probe-v8.txt"` (측정기가 U 판 `SKILL.md` `## 7.` 절의 js 블록을 그대로 뽑아 1280×720 에서 돌린다) · Then (a) `m LIT` 의 `sk_s7_keys=1` (b) `m COUNT "$D/probe-v8.txt" SEC7` 이 `ok=2 ng=0` — 식이 돌려준 `chips` · `rows` 의 네 상태 값이 측정기가 따로 센 트리 줄 수와 같고 `ep`=`shown` · `under24`=0 (c) `m LIT` 의 `sk_s7_nums` 다섯 값이 `probe-v8.txt` 의 `OK v8 1280-light sec7-expr` 줄 JSON 의 `ep` · `shown` · `targets` · `under24` · `under44` 와 같고, `sk_s7_touch_row` 가 `under44/targets/under24`, `sk_s7_ep_row` 가 `ep=shown`, `vs_1_touch_row` 가 `sk_s7_touch_row` 와 같다 [exact] (음성 대조: 시작 판 식은 `chips` 가 없어 v7 사본에서 `SEC7 ok=0 ng=2` — 실측)
- [ ] SK-04: 뷰어 스펙 여섯 자리에 네 번째 상태가 들어간다 — `api-kit/skills/api-ui/references/viewer-spec.md` 의 (a) `### 3.1` 요약 칩 행에 네 이름 (b) `### 3.2` 상태 아이콘 줄에 `판정 불가` (c) `### 3.5` 에 판정 불가 표시 자리 — `판정 불가` 1 이상 · `(없음)` 이 든 줄 1 이상 · `실패 원인` 과 `판정 불가` 가 같이 든 줄 1 이상(FAIL 인 엔드포인트의 판정 불가 줄도 실패 원인 탭에 둔다) (d) `## 4.` 데이터 모델의 `state:` 주석 값이 네 개이고 네 번째가 `'unjudged'` 다(ER-02 의 변이가 이 글자를 쓴다) (e) `## 6.` 토큰 표에 `판정 불가` 행이 있고 그 행의 색 값(hex)이 밝은 · 어두운 두 개 이상이며 전부 v8 에 있다 (f) `## 8.` 텍스트 대응물 줄에 네 이름 [exact, enumerated] (측정: `m LIT` 의 `vs_31_chips=1` · `vs_32_icons` 1 이상 · `vs_35_unj` 1 이상 · `vs_35_line` 1 이상 · `vs_35_failtab` 1 이상 · `vs_4_state_values=4` · `vs_6_rows` 1 이상 · `vs_6_hex` 값 두 개 이상 · `vs_6_hex_in_v8=k/k` (k 는 hex 수) · `vs_8_text=1`. 시작 판 `vs_4_state_values=3`, 나머지 0)
- [ ] SK-05: 정본 시안을 가리키는 자리가 전부 v8 이다 — `SKILL.md` · `viewer-spec.md` 에 `api-ui-v8.html` 이 각각 두 번 이상, `api-ui-v7` 는 0 번 [exact] (측정: `m LIT` 의 `sk_v8` 2 이상 · `vs_v8` 2 이상 · `sk_v7=0` · `vs_v7=0`. 시작 판 `0` · `0` · `2` · `2`)
- [ ] SK-06: v8 시안에서 네 상태가 칸마다 맞게 보인다 — Given `.mockups/api-ui-v8.html` 이 있고 v7 이 그대로(AR-04) · When `m PROBE v8 "$V8" > "$D/probe-v8.txt"` (375×812 · 1280×720 × 밝은 · 어두운 네 조합) · Then (a) `m COUNT "$D/probe-v8.txt" FUNC` 가 `ok=30 ng=0` — 네 조합 모두에서 트리 줄마다 상태 글자가 하나씩이고 줄 수 = 엔드포인트 수, 네 칩이 하나씩 보이고 접근 이름에 상태 글자가 들며 숫자가 그 상태 줄 수와 같고, 판정 불가가 1 이상이고, 375 에서 서랍을 열면 모든 줄이 보이고, 1280 에서 판정 불가 칩을 누르면 판정 불가 줄만 남았다가 다시 누르면 돌아오고, 판정 불가 엔드포인트를 고르면 `실패 원인` 탭 없이 `(없음)` · `→ 판정 불가` 가 든 판정 줄이 보인다 (b) `m IDS` 가 `v7_ids=76 missing_in_v8=0` (v7 의 id 76 개가 다 남는다) [goal] (음성 대조: v7 사본은 `FUNC ok=12 ng=18` — 실측)
- [ ] SK-07: 시험 입력으로 `/api-ui` 절차를 따라 만든 예시 `ui.html` 이 네 상태를 맞게 보인다 — Given U 판에서 `m EVALS` 가 `evals_json=1` · `api_ui_cases` 1 이상이고 그 경우 줄이 `fixture_api=5/5` · `example=U:api-kit/evals/fixtures/` 로 시작 · `expect` 네 값 모두 1 이상 · `assertions` 1 이상 · `unjudged_lines` 2 이상 · When `m PROBE example "<그 example= 값>" > "$D/probe-example.txt"` · Then `m COUNT "$D/probe-example.txt" FUNC` 가 `ok=30 ng=0`, `m COUNT "$D/probe-example.txt" SEC7` 이 `ok=2 ng=0`, `OK example 1280-light chip[<이름>]` 네 줄의 `num=` 값이 `expect` 의 같은 이름 값과 같다 [goal] (음성 대조: ER-02 의 변이 사본에서 `chip[판정 불가]` 가 `num=0 rows=0` 으로 바뀐다)
- [ ] SK-08: 예시 `ui.html` 이 `SKILL.md` §7 글자 검사 · 비밀 모양 · CSP 를 통과한다 — `m EX7 "<m EVALS 의 example= 값>"` 에서 `--- sec7 block` 아래 출력이 차례로 `1` (양성 대조 줄) · `0` · `0` · `0` · `0` · `0` 이고 외부 URL 줄이 없고 마지막 크기 값이 10485760 이하, `secret_positive=1` 이면서 `secret_hits=0`, `csp_lines` 1 이상 [exact] (양성 대조: `sec7 block` 첫 줄과 `secret_positive` 가 같은 패턴이 1 을 내는 것을 매번 보인다. CSP 글자는 `viewer-spec.md` §1 의 `content` 값 그대로)
- [ ] SK-09: 판정 불가의 색 · 모양 · 글자가 밝은 · 어두운 테마 모두 대비 기준을 지키고 색만으로 구분하지 않는다 — v8 과 예시 두 출력 파일 각각에서 `m COUNT <파일> NFR` 이 `ok=20 ng=0` — 네 조합 모두에서 판정 불가 행 모양과 칩 모양이 배경과 3:1 이상, 행 모양의 모양(svg) · 색이 다른 세 상태와 다르고 칩 모양이 다른 세 칩과 다르며, 1280 두 테마에서 `판정 불가` 글자가 든 보이는 요소가 하나 이상이고 전부 4.5:1(큰 글자 3:1) 이상 [exact, enumerated] (측정: `m COUNT "$D/probe-v8.txt" NFR` · `m COUNT "$D/probe-example.txt" NFR`. 글자로 구분되는 것은 SK-06 · SK-07 의 칩 이름 줄이 잰다. 음성 대조: 손 화면에서 판정 불가 색을 미실행 색으로 바꾸면 `row-glyph-distinct` NG — 실측)

## Script

- [ ] SC-00: N/A (Script 카테고리는 `scripts/release.sh` 연동 · 판 올림 · `marketplace.json` 갱신이다. 릴리스는 이 가지를 합친 뒤 다음 단계라 이 스프린트는 그 파일들을 건드리지 않는다. 측정: `m NA` 의 `release_sh=0 version_files=0`. 양성 대조: `a11927e` 에서 `release_sh=1`)

## Error

- [ ] ER-01: 계약 실패와 판정 불가가 한 엔드포인트에 같이 있으면 FAIL 로 센다 — Given 시험 입력에 그런 엔드포인트가 1 개 이상(`m EVALS` 의 `fail_with_unjudged` 1 이상) · When SK-06 · SK-07 의 측정기 출력 · Then `probe-example.txt` 의 `INFO example 1280-light fail-with-unjudged=` · `1280-dark` 값이 둘 다 `expect.fail_with_unjudged` 와 같고, `probe-v8.txt` 의 같은 두 값이 1 이상이다 — 그 엔드포인트가 FAIL 줄로 보이고 `실패 원인` 탭에 판정 불가 줄이 함께 보인다 [goal] (음성 대조: 판정 불가를 FAIL 보다 앞세우면 그 엔드포인트가 판정 불가 줄로 가 `fail-with-unjudged` 가 0 이 되고 `chip[FAIL]` 숫자가 `expect` 와 어긋난다. 알려진 답: 손 화면에서 `fail-with-unjudged=1`)
- [ ] ER-02: 판정 불가가 0 이어도 칩이 남고 숫자는 데이터에서 센다 — Given U 판 · 예시 데이터가 엔드포인트 상태를 `state:'<값>'` 꼴(콜론 뒤 공백 없음)로 쓰고 네 번째 값(`viewer-spec.md` `## 4.` 의 `state:` 주석 네 번째)이 `'unjudged'` 다 · When `m MUT example "s/state:'unjudged'/state:'pass'/g"` (식은 이 글자로 고정한다 — 평가자가 새로 짓지 않는다. 데이터의 판정 불가 상태 값만 PASS 값으로 바꾼다) · Then `mutated_lines` 1 이상이고, `chip[판정 불가]` 네 줄이 모두 `OK mut <조합> chip[판정 불가] — chips=1 visible=true num=0 rows=0` 이다 (`rows=0` 으로 변이가 다 들어갔는지 먼저 본다) [goal] (알려진 답: 숫자를 손으로 적은 손 화면 변이에서는 `num=1 rows=0` 으로 NG — 실측)
- [ ] ER-03: `판정 불가` 를 다른 글자로 쓰지 않는다 — U 판 `api-kit/` 전체와 v8 에서 띄어쓰기 없는 `판정불가` 가 0 건 [exact] (측정: `m LIT` 의 `bad_spelling=0`. 양성 대조: 손 트리의 한 줄에서 `bad_spelling=1`)

## Architecture

- [ ] AR-01: 이 스프린트 커밋이 바꾼 경로(`.harness/` 밖)가 기대 집합 안에만 있고 기대 집합의 필수 경로를 다 포함한다 — 정확히 다섯 경로와 `api-kit/evals/` 아래 파일들이고, 그중 `api-kit/README.md` 는 `<!-- AUTO:evals -->` 블록 안만 바뀐다 [exact, enumerated] (Given: 이 스프린트 커밋이 끝난 뒤 · 경로 한정: 레포 전체 · 제외: `.harness/` (AR-03 이 따로 잰다) · 상한: `m` 이 정한 U (`UNRESOLVED` 면 멈춤) · 측정: `m SCOPE` 가 `scope_out=0 required_missing=0 readme_outside_auto=0` — `.harness/` 를 빼고 세며, 다섯 경로와 `api-kit/evals/` 아래를 기대 집합으로 보는 열거는 `m.sh` `SCOPE)` 한 곳에만 있다. `readme_outside_auto` 는 시작 판과 U 판의 `api-kit/README.md` 에서 AUTO:evals 블록 안쪽을 지우고 맞댄 차이 줄 수다. 시작 판 `scope_out=0 required_missing=6 readme_outside_auto=0`. 양성 대조: `a11927e` 에서 `scope_out=2`, `21d13ce` 에서 `readme_outside_auto=2`)
- [ ] AR-02: 한 커밋에 킷 하나 — api-kit 변경과 `.github/workflows/ci.yml` 변경이 서로 다른 커밋이고, 어느 커밋도 최상위 자리 두 곳 이상을 건드리지 않는다 (`.harness/` 는 세지 않는다) [exact] (측정: `m COMMITS` 가 `mixed=0` 이고 커밋 줄이 2 개 이상. 양성 대조: `a11927e` 에서 `mixed=1`)
- [ ] AR-03: 계약 봉인이 깨진 파일이 없고 측정 도구가 계약 때 그대로다 — `.harness/` 의 `sprint-contract*.md` 전부에 봉인 검사를 돌려 `SEAL_BROKEN` 0, 그리고 `$D/m.sh` · `$D/lit.py` · `$D/probe-ui.cjs` 의 sha256 앞 16 자리가 차례로 `ba4701ce7b7be425` · `691613b23348be8d` · `c00fad7dfdaff7ff` [exact] (측정: `m SEAL` 출력에 `SEAL_BROKEN` 줄 0 · `shasum -a 256 "$D/m.sh" "$D/lit.py" "$D/probe-ui.cjs"`. 시작 판 `SEAL_OK 73` · `SEAL_ABSENT 11`. 양성 대조: 봉인 값이 틀린 사본에서 `SEAL_BROKEN 1`)
- [ ] AR-04: 본 체크아웃에는 v8 한 파일만 새로 생기고 v7 은 그대로다 — `.mockups/api-ui-v7.html` sha256 이 `c4bd563ec8b71a95f804ae1f96a0eda2d17bda8256ca9fbc327a527c3a81ca7a` 그대로, `.mockups/` 바로 아래에서 `2026-09-26 14:15` 뒤에 바뀐 파일이 `api-ui-v8.html` 하나 [exact] (측정: `m MOCKUPS` 가 `v7_sha_same=1` · `NEW api-ui-v8.html` · `new_files=1`. 시작 `v7_sha_same=1 new_files=0`. 양성 대조: 사본 폴더에 파일 하나를 더 두면 `new_files=2`)
- [ ] AR-05: 새 시험이 CI 에서 실제로 돌고, 판정 불가를 PASS 에 합치면 떨어진다 — Given U 판 · When `m CI` · Then `evals_json=1` · `runner=` 값이 `npx playwright test api-kit/evals/` 로 시작 · `ci_step=1` (CI `playwright` 작업에 그 명령과 글자가 같은 단계 하나) · `after_install=1` (브라우저 설치 단계 뒤) · `runner_rc=0`, 그리고 ER-02 와 같은 변이 `m MUT example "s/state:'unjudged'/state:'pass'/g"` 의 `runner_rc` 가 0 이 아니다 [exact] (음성 대조가 위 변이다. 양성 대조: `cec7867` 에서 `ci_step=1 after_install=1 runner_rc=3`)
- [ ] AR-06: 캡처 확인 기록과 톤 대조 기록이 남는다 — `$D/evidence.md` 에 (a) `v8-1280-light.png` · `v8-1280-dark.png` · `v8-375-light.png` · `v8-375-dark.png` · `example-1280-light.png` · `example-1280-dark.png` · `example-375-light.png` · `example-375-dark.png` 여덟 이름이 각각 표 줄에 있고 그 줄에 캡처에서 눈으로 본 상태 글자(`PASS` · `FAIL` · `미실행` · `판정 불가`)가 적혀 있으며, 여덟 파일이 `$D/cap/` 에 크기 0 초과로 있다 (b) tone-kit:tone-guide 5 단계 표 머리 `| 패턴 / 규칙 | 건수 | 판정 |` 와 `C-` · `N-` · `S-` 로 시작하는 규칙 줄이 각각 1 이상 있고, 그 대조 대상으로 바꾼 파일 이름(`SKILL.md` · `viewer-spec.md` · `api-layout.md` · 시험 파일)이 적혀 있다 [structural] (측정: `grep -c` 로 여덟 이름 · 표 머리 · 규칙 줄 · 파일 이름, `find "$D/cap" -name '*.png' -size +0`. 평가자는 캡처 여덟 장을 직접 연다)
- [ ] AR-07: 생산 쪽 `/api-verify` 가 소비 쪽이 인용한 글자를 그대로 갖고 있다 — `api-kit/skills/api-verify/SKILL.md` 에 「한쪽 경로라도 없으면」 1 번, `(없음)` 과 `→ 판정 불가` 가 한 줄에 든 판정 줄 1 줄 이상 — SK-01 이 `api-kit/skills/api-ui/SKILL.md` 에서 요구한 글자와 같다 [exact, enumerated] (측정: `m LIT` 가 U 판 `api-kit/skills/api-verify/SKILL.md` 에서 센 `av_phrase=1` · `av_line` 1 이상 — `/api-verify` 쪽 글자이고, `api-kit/skills/api-ui/SKILL.md` 쪽은 SK-01 의 `sk_s2_phrase` · `sk_s2_line` 이다. 시작 판 `1` · `1`. 생산 쪽 파일을 바꾸지 않는 것은 AR-01 이 잰다)

## Anti-patterns

- [ ] AP-01: 버전을 하드코딩하지 않는다 — plugin.json에서 읽어야 한다. 이번 변경에 적용: 이 스프린트 커밋이 더한 줄(`.harness/` · `api-kit/evals/fixtures/` 제외)에 api-kit `plugin.json` 의 `version` 값이 0 번 나온다 [exact] (측정: `m VER` 의 `added_hits=0`, 같은 줄의 `positive=1` 이 패턴이 살아 있음을 보인다)
- [ ] AP-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수 (```text, ```bash, ```yaml 등). 판정 권위는 validate-plugin V6 상태기계다 — 여는/닫는 fence 가 동형이라 줄 단위 정규식으로는 판정 불가. 이번 변경에 적용: 스킬 · README 는 DG-05 의 검사기가 보고, V6 가 안 읽는 참조 문서 · 새 md 는 markdownlint MD040 으로 본다 — `m MD` 출력 어느 줄에도 `MD040` 이 늘어난 규칙으로 나오지 않는다 [exact] (양성 대조: `a11927e` 에서 `MD040:0->1`)
- [ ] AP-04: SKILL.md / agents/*.md frontmatter 에서 name 필드 누락 — validate-plugin V1 FAIL. 이번 변경에 적용: `api-kit/skills/api-ui/SKILL.md` 첫 머리 설정 블록이 시작 판과 글자 그대로 같다 [exact] (측정: `m FM` 이 `fm_lines=12 fm_diff=0`. 양성 대조: `CTL_SED='2s/api-ui/api-uiX/' m FM` 이 `fm_diff=2`)

## Reusability

- [ ] RE-01: 다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다 — 이번 변경에 적용: 새 시험은 `SKILL.md` §7 브라우저 식을 자기 사본으로 다시 쓰지 않고 U 판 `api-kit/skills/api-ui/SKILL.md` 에서 뽑아 돌린다 [goal] (측정: `m MUT skill '/^## 7\./,/^## 8\./s/ rows: / rowz: /'` — 식은 이 글자로 고정한다. §7 js 블록이 돌려주는 객체는 트리 줄 수 키를 앞뒤 공백과 콜론을 붙인 ` rows: ` 꼴로 쓴다 — 에서 `mutated_lines` 1 이상 · `sec7-expr` NG 두 줄(변이가 들어갔다) · `runner_rc` 가 0 이 아니다)
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다 — 이번 변경에 적용: v8 은 v7 의 클래스(`.chip` · `.st` · `.badge` · `.callout` 등)를 `data-` 속성 값으로 넓혀 쓰고 새 클래스 이름을 만들지 않으며, 판정 불가 색은 CSS 변수로만 선언해 컴포넌트 규칙에 색 값을 바로 쓰지 않는다 [exact] (측정: `m CLASSES` 의 `new_classes=0` · `m LIT` 의 `v8_hex_raw_uses=0`. 양성 대조: 클래스 하나 더한 사본에서 `new_classes=1`, 손 트리에서 `v8_hex_raw_uses=1`)

## Diagnostics

- [ ] DG-01: N/A (`commands.analyze` 는 `bash -n scripts/release.sh` 라 `scripts/release.sh` 만 잰다 — 이번 변경 파일과 교집합 0 개. 측정: `m NA` 의 `release_sh=0`. 양성 대조: `a11927e` 에서 `release_sh=1`)
- [ ] DG-02: IDE diagnostics 워닝/인포 0개 (`[]` 제외) — 이번 변경에 적용: 바꾼 md 파일마다 편집기와 같은 조건(markdownlint-cli2 0.23.2 · MD013 끔)의 규칙별 경고 수가 시작 판보다 늘지 않고(새 파일은 경고 0), 바꾼 js · json · yaml 파일이 읽힌다 [exact] (측정: `m MD` 의 줄이 `SKILL.md` · `viewer-spec.md` · `api-layout.md` 를 포함해 모두 `rules_up=0` · `m SYNTAX` 가 `syntax_bad=0` 이고 `syntax_files` 2 이상. 양성 대조: `a11927e` 에서 `rules_up=3`, `6d28adc` 에서 `syntax_bad=2`)
- [ ] DG-03: N/A (`commands.test` 는 `bash scripts/release.sh 2>&1 || true` 라 `scripts/release.sh` 만 잰다 — 교집합 0 개. 측정: DG-01 과 같은 `m NA` 의 `release_sh=0`. 실제 실행 검사는 SK-06 · SK-07 · AR-05 · DG-05)
- [ ] DG-04: 실제 앱/서버 구동 시 에러 0개 — 이번 변경에 적용: v8 과 예시를 브라우저로 연 네 조합 모두에서 콘솔 error 0 (`favicon.ico` 는 빼고 센다) [exact] (측정: `m COUNT "$D/probe-v8.txt" CONSOLE` · `m COUNT "$D/probe-example.txt" CONSOLE` 이 둘 다 `ok=4 ng=0`. 측정기는 아이콘을 부르는 전체 모드 크로미엄(`channel: 'chromium'`)을 쓴다)
- [ ] DG-05: 저장소 검사가 U 판에서 통과한다 — (a) CI 단계 전부 (b) 플러그인 검사기의 이 판과 origin/main 새 판(`88ddfe5`) 둘 다 api-kit 을 문제로 가리키지 않는다 [exact] (측정: (a) `m CILOCAL` 이 `rc0=22 not_rc0=1` 이고 `rc=0` 이 아닌 한 줄이 `feedback-agg-test SKIP (yq 없음)` — 새 api-kit 단계는 AR-05 가 잰다 (b) `m VALID` 가 `own_rc=0 own_bad=0 own_lines=10 main_rc=0 main_bad=0 main_lines=10`. 시작 판 22 · 1 과 `own_bad=0 main_bad=0` — 실측. 양성 대조: `a11927e` 에서 `own_bad=1 main_bad=1`)
