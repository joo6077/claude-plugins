---
feature: "문서 사이트 새 페이지 (dr2) — 짝 목록 NEW 15 쪽"
slug: after-0926-docs-new-pages-2
created: "2026-09-27 16:46"
complexity: "복잡"
conditions: 26
status: done
owner_session: bda55d45-296c-491f-89ba-b52042d58e72
conditions_digest: sha256:3536904c066d26d5
measurement_digest: sha256:1a7c2175c3f905a3
locked_at: "2026-09-27 17:00"
---

## 배경

짝 목록 `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0926b/.harness/.meta/after-kaizen-0926b/docs-pairs.txt`(읽기만, 경고 정리 전 판 `c3e45f3` 기준 46 짝)에서 줄 끝에 `NEW` 가 붙은 짝 15 개를 처리한다. 목표는 15 원본 모두가 등록되고 파일이 있는 페이지 하나와 짝지어져 드리프트 도구가 `NEW` 를 0 개 내는 것이다.

- 위임: 세션 `bda55d45-296c-491f-89ba-b52042d58e72` 의 사용자 말 2026-09-26T10:09:00.557Z · 10:30:16.222Z · 2026-09-27T01:22:01.089Z 「자동으로 다 진행해 나한테 묻지 말고 …」. 결정 파일 `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0926b/.harness/.meta/after-kaizen-0926b/decisions.md`(읽기만). 사용자 합의(Step 5)는 이 위임으로 받은 것으로 적는다. 봉인된 조건을 느슨하게 하는 개정은 이 위임으로 동의 처리하지 않는다.
- 작업 폴더 W = `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak2-dr2`, 가지 `chore/ak2-dr2`(`chore/after-kaizen-0926b` `38cccd1` 에서 갈라짐). 범위 구간의 아래 끝은 이 계약의 봉인 커밋의 부모다 — 측정 도우미가 git 기록에서 푼다. 봉인 전 실측 때 그 자리는 `38cccd1` 이었다.
- 짝 목록이 내준 페이지 이름과 다른 곳이 열 쪽 있다. 드리프트 도구는 원본 이름에서 페이지 이름을 만들 뿐이라, 이름이 다른 기존 페이지를 못 찾고 `NEW` 로 냈다. 실제로는 그 열 원본의 페이지가 이미 있고 목차에 올라 있다 — `docs/react-kit/scaffolding.html` 머리 제목이 「G1 · Scaffolding & Generation」(`:109`), `docs/react-kit/quality.html` 이 `kit-design/g4-quality.md` 를 12 번(파일 이름 `g4-quality.md` 로 세면 22 번) 인용, `docs/howto-kit/overview.html` 이 `design-brief.md` 를 2 번, `docs/harness/feedback-system.html` 이 `feedback-schema.yaml` 을 2 번 인용한다. 다른 묶음 dca 가 남긴 매핑 결정(`/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0926b/.harness/.meta/after-kaizen-0926b/dca-notes.md:109-162` 「DC-9 매핑 규칙 결정」)도 이 열을 「짝: 기존 페이지」 로 정했다. 같은 원본으로 두 번째 쪽을 만들면 원본 하나에 쪽 둘이 생기고(docs-site Gotcha 7), 이미 있는 것을 다시 만들게 된다(RE-02). 그래서 이 열은 새 이름으로 만들지 않고 **기존 쪽을 원본에 맞춰 다시 쓰고, 드리프트 도구가 그 쪽을 짝으로 고르게 한다.** 기존 쪽들은 원본을 28 ~ 74 % 만 담고 있어(아래 옛 판 값) 다시 쓰는 일이 곧 원본 담김을 올리는 일이다.
- 1 회차 계약(`after-0926-docs-new-pages`, 봉인 · 끝남)과의 관계: 같은 짝 목록의 다른 원본을 다룬 형제 계약이다. 두 계약의 원본은 하나도 겹치지 않는다. 1 회차는 일곱 원본 모두 새 쪽이었고, 기존 쪽을 원본에 맞춰 다시 쓰는 길은 이 계약이 처음 연다(근거는 위 불릿).
- 나머지 다섯은 대응 페이지가 정말 없다 — 새 쪽을 만든다. 연구 기록 셋(`research-log.md`)은 dca 매핑 결정이 「페이지 없음이 맞음」 이라 적었지만, 사용자 결정 DC-1 이 같은 종류인 api 연구 기록을 새 쪽으로 만들게 했고(`docs/api-kit/research-log.html` 이 이미 있다) 부모 과제가 이 셋을 짚었으므로 새 쪽으로 만든다. `tone-kit/references/sources.md` 는 dca 결정표에 없다.
- 15 원본과 대상 쪽(`kind`: 새 = 새 쪽 · 다시 = 기존 쪽을 다시 씀). 경로는 `find` 와 `docs/index.html` 로 확인했다. 도우미 `FIFTEEN` 과 같은 글자다:

| 원본 | 대상 쪽 | 종류 | 킷 목차 | 옛 판 담김 (낱말 · 코드 표시 · 코드 블록 줄, `38cccd1`) |
| --- | --- | --- | --- | --- |
| `docs/backend/research-log.md` | `docs/backend-kit/research-log.html` | 새 | Backend Kit | 쪽 없음 |
| `docs/howto/design-brief.md` | `docs/howto-kit/overview.html` | 다시 | Howto Kit | 0.28 · 34/181 · 0/33 |
| `docs/infra/research-log.md` | `docs/infra-kit/research-log.html` | 새 | Infra Kit | 쪽 없음 |
| `docs/react/kit-design/final-integration.md` | `docs/react-kit/integration.html` | 다시 | React Kit | 0.48 · 38/87 · 29/253 |
| `docs/react/kit-design/g1-scaffolding.md` | `docs/react-kit/scaffolding.html` | 다시 | React Kit | 0.38 · 69/159 · 73/205 |
| `docs/react/kit-design/g2-state-data.md` | `docs/react-kit/state-data.html` | 다시 | React Kit | 0.31 · 63/160 · 91/208 |
| `docs/react/kit-design/g3-performance.md` | `docs/react-kit/performance.html` | 다시 | React Kit | 0.33 · 59/120 · 78/144 |
| `docs/react/kit-design/g4-quality.md` | `docs/react-kit/quality.html` | 다시 | React Kit | 0.74 · 119/131 · 184/215 |
| `docs/react/kit-design/g5-ui-patterns.md` | `docs/react-kit/ui-patterns.html` | 다시 | React Kit | 0.50 · 59/104 · 24/58 |
| `docs/react/kit-design/g5b-animation.md` | `docs/react-kit/animation.html` | 다시 | React Kit | 0.36 · 64/152 · 62/363 |
| `docs/react/kit-design/g6-build-audit.md` | `docs/react-kit/build-audit.html` | 다시 | React Kit | 0.39 · 57/202 · 28/96 |
| `docs/react/research-log.md` | `docs/react-kit/research-log.html` | 새 | React Kit | 쪽 없음 |
| `harness/references/feedback-schema.yaml` | `docs/harness/feedback-system.html` | 다시 | Harness | 0.71 · 원본에 코드 표시 없음 · 원본에 코드 블록 없음 |
| `react-kit/references/project-detection.md` | `docs/react-kit/project-detection.html` | 새 | React Kit | 쪽 없음 |
| `tone-kit/references/sources.md` | `docs/tone-kit/sources.html` | 새 | Tone Kit | 쪽 없음 |

- 옛 판 값은 도우미 `m AR-03` 을 시작 판에 돌린 값이고, 인계 도구와 같다 — 예: `integration.html` 은 `coverage.py` `wr=0.48->0.48 codes=87 new=38`, `fence2.py` `lines=253 in_new=29`(봉인 전 실측, 종료 코드 0). `quality.html` 의 코드 블록 줄은 `fence2.py` 의 `in_old`(`509d295` 기준 70)가 아니라 시작 판 184 다 — 그 사이 쪽이 한 번 고쳐졌다.
- 만드는 법: 이 레포 `.claude/skills/docs-site/SKILL.md` 절차 — 틀 `.claude/skills/docs-site/references/page-template.html`, 공통 파일 `docs/assets/site.css` 링크 한 줄, 킷 색은 `references/css-tokens.md` 매핑(Backend `#A78BFA` · Infra `#34D399` · React `#38BDF8` · Howto `#F59E0B` · Harness `#D97757` · Tone `#D946EF`). YAML 원본(`feedback-schema.yaml`)은 키 표와 예시로 옮긴다(AR-10). 구현 전에 `tone-kit:tone-guide` 1 단계를, 완료 선언 전에 5 단계를 한다 — 새로 쓰는 한국어 글 · 쪽 스크립트 주석 · notes 가 대상이고 결과는 notes 에 남긴다(AR-08).
- 커밋 규칙: `git add <경로>` 뒤 `git commit -o <경로>` · 한 커밋에 맨 위 폴더 하나(문서 사이트는 `docs/<킷>/` 하나, `docs/index.html` 은 어느 docs 커밋에 실어도 된다) · `git add -A` · `git stash` · push · 가지 바꾸기 금지. `.harness/` 파일은 구현 파일과 다른 커밋에 싣는다(AR-07).
- 기록 파일(notes): `.harness/.meta/after-kaizen-0926b/dr2-notes.md` (W 안, 이 가지에 커밋).
- 사용자가 할 일: 없음.

공통 전제 G (조건마다 되풀이하지 않는다) — 구현 · notes 커밋이 가지 `chore/ak2-dr2` 에 모두 들어간 뒤, 가지를 합치기 전에 잰다.
측정은 `## 회귀 게이트` 의 측정 도우미 `m <조건 ID>` 로 한다. 도우미는 끝점 `TIP`(가지 끝)과 시작점 `BASE`(봉인 커밋의 부모)를 `git archive` 로 풀어 잰다 — 작업 폴더의 커밋 안 된 변경은 보지 않는다(DG-05 만 작업 폴더를 쓴다).
`HEAD` 를 상한으로 쓰지 않는다. `BASE` · `TIP` 해석이 안 되면 도우미가 `UNRESOLVED` 를 찍고 멈춘다.
「열다섯 쪽」 · 「열다섯 원본」 은 위 표이며 도우미 `FIFTEEN` 과 같은 글자다. 브라우저는 `file://` 로 연다.

복잡도 4 축 — 넷 모두 「예」 라 「복잡」 이다. Step 2.5 짝 조건을 넣었다.
기능 조건 19 개는 SK-01 · SC-01 ~ SC-03 · ER-01 ~ ER-04 · AR-01 ~ AR-10 · DG-05 다 — Step 6.2 두 번째 명령이 `## Anti-patterns` 절(AP-03) · 자동 포함 여섯 줄 · `N/A (` 줄을 빼고 센 값이다.
Step 2.5 짝 조건: 만드는 쪽은 드리프트 도구의 매핑(SC-01 · SC-02)과 열다섯 쪽(AR-01 · AR-03 · AR-04 · AR-05 · AR-10 · ER-01 · ER-02)이다. 쓰는 쪽은 쪽을 목차로 여는 `docs/index.html`(AR-02 · ER-03), 매핑과 사람용 표를 맞대는 `--check-table`(SC-03 · SK-01 — 표는 폴더 단위라 고칠 것이 없다), 링크 · 고아 검사 `scripts/check-docs-links.py`(AR-02), 오케스트레이터 Step F2(같은 명령으로 부르기만 해서 고칠 것 없음)다.

| 축 | 물음 | 값 |
| -- | ---- | -- |
| 레이어 수 | 몇 개 계층을 관통하는가 | 셋 — 정적 문서 화면(HTML · CSS · 쪽 스크립트), 목차(`docs/index.html`), 원본과 페이지를 짝짓는 도구 |
| 공개 API·계약 변경 | 외부에 노출된 약속이 바뀌는가 | 예 — 드리프트 도구가 고르는 짝이 열 개 바뀌고, 목차에 다섯 항목이 는다 |
| 소비면 존재 | 반대편이 있는가 | 예 — 카이젠 Step F2, 목차 화면, 링크 · 고아 검사, 표 맞대기 검사 |
| 회귀 위험 | 기존 동작이 깨질 수 있는가 | 예 — 기존 열 쪽을 다시 쓰면 옛 판에 있던 원본 내용을 잃을 수 있고, 목차 id 가 겹치면 다른 쪽이 열린다 |

설정 값 대조 (`.harness/project.yaml` 을 글자 그대로 옮김):

| config key | project.yaml 에서 읽은 값 | 계약에 쓴 값 |
| ---------- | ------------------------- | ------------ |
| `commands.analyze` | `bash -n scripts/release.sh` | DG-01 N/A — 재는 파일이 바뀐 파일에 없다 |
| `commands.test` | `bash scripts/release.sh 2>&1 \|\| true` | DG-03 N/A — 같은 이유 |
| `diagnostics.ide_exclude` | `[]` | DG-02 의 `([] 제외)` |
| `contract_categories[].id` / `prefix` | Skill/SK · Script/SC · Error/ER · Architecture/AR | 같은 넷 |
| `anti_patterns[].id` / `message` | AP-01 버전 하드코딩 · AP-02 force push · AP-03 bare code fence · AP-04 frontmatter name 누락 | AP-03 (새 notes). AP-01 은 더하는 줄에 판 번호를 읽어 올 자리가 없어서(정적 쪽 · 목차 줄 · 매핑 줄), AP-02 는 push 하지 않아서, AP-04 는 `SKILL.md` · 에이전트 파일을 고치지 않아서(SK-01 `skill_changed=0`) 뺐다 |

## GAP 분석 (Pre-Edit Audit)

대상 파일을 실제로 읽고 잰 값이다(시작 판 `38cccd1`).

| 대상 파일 | 실제 Read 증거 (`파일:라인`) | 발견한 기존 갭·위반 | 계약 조건화 |
| --------- | ---------------------------- | ------------------- | ----------- |
| `scripts/detect-docs-drift.py` | `:37-81` `SOURCE_TO_HTML`(`:42` `docs/react/` · `:40` `docs/backend/` · `:41` `docs/infra/` · `:39` `harness/references/` · `:47` `react-kit/references/` · `:58` `tone-kit/references/` · `:68` `docs/howto/`) · `:85-113` `SOURCE_OVERRIDES` · `:216-239` `map_source_to_html`(하위 폴더를 버리고 원본 이름으로 쪽 이름) · `:157-195` `resolve_target` | 열다섯 모두 접두 매핑은 있으나 쪽이 없는 이름을 가리킨다(`m SC-01` 시작 판 `fifteen_ok=0/15 new_entries=15`). 기존 쪽과 이름이 다른 열은 덮어쓰기 매핑이 필요하다(`m SC-02` 시작 판 `delta_n=0 delta_good=0/10`) | SC-01 · SC-02 |
| `.claude/skills/docs-site/SKILL.md` | `:49-50` 표 규칙과 `--check-table` · `:52-68` 매핑 표(`:57` backend · `:58` infra · `:60` react · `:54` harness · `:65` tone · `:67` howto 모두 폴더 단위) · `:22` Gotcha 7 · `:23` Gotcha 8 400 줄 · `:24` Gotcha 9 · `:25-29` Gotcha 10 · `:30` Gotcha 11 · `:32` Gotcha 13 · `:16` Gotcha 1 | 표가 폴더 단위라 열다섯이 이미 덮인다(`fifteen_in_table=15/15 mismatch=0->0`). 고칠 것 없음 | SK-01 · SC-03 · AR-01 · AR-05 · RE-02 |
| `docs/index.html` | `:230` `categories` · `:232` Harness · `:374` · `:387` · `:395` Backend Kit · `:423` · `:433` · `:446` Infra Kit · `:483-496` React Kit · `:535` Tone Kit · `:573` Howto Kit · `:625` `getIcon` · `:248` id `project-detection`(flutter) · `:479` `project-detection-rust` · `:528` `onboarding-project-detection` · `:569` `api-research-log` | 다시 쓸 열 쪽은 이미 등록 · 아이콘 있음(`reg_ok=10/15 icon_ok=10/15`). 새 다섯 id 후보 `backend-research-log` · `infra-research-log` · `react-research-log` · `react-project-detection` · `tone-sources` 는 지금 0 번 쓰였다(grep 0) | AR-02 · ER-03 |
| `docs/react-kit/*.html` 여덟 · `docs/howto-kit/overview.html` · `docs/harness/feedback-system.html` | `docs/react-kit/scaffolding.html:109` 제목 G1 · `quality.html` `kit-design/g4-quality.md` 12 회 · `overview.html` `design-brief.md` 2 회 · `feedback-system.html` `feedback-schema.yaml` 2 회 · `m AR-01` 시작 판(여덟 react 쪽 `dk_theme=0 light_rule=0`, `quality` `rm=1` · `animation` `rm=5` · `build-audit` `rm=1`, `overview` `rm=1`, `feedback-system` `rm=1 hide=1`) | 원본 담김이 낮고(표 값), 여덟 react 쪽과 feedback-system 은 어두운 테마뿐이라 두 테마 검사(ER-01 `theme_differs=0`)에 걸리며, 쪽에 움직임 줄이기를 다시 적었고(Gotcha 1), feedback-system 에 넘침 숨김 하나가 있다(Gotcha 11). 원본 주소도 빠졌다(`m AR-04` 시작 판 여섯 쪽 BAD) | AR-01 · AR-03 · AR-04 · AR-05 · ER-01 · RE-02 |
| `harness/references/feedback-schema.yaml` | `:5` `schema_version` · `:7-76` 주석으로 적은 필드 정의 · `:79-109` `example` | 키 41 개(주석 정의 40 + `schema_version`, `example` 뺌) 가운데 지금 쪽 표에 든 것 8 개, 예시와 같은 값의 `<pre>` 0 개(`m AR-10` 시작 판) | AR-10 |
| 새 다섯 원본 | `docs/backend/research-log.md` 603 줄 · 코드 표시 118 · 주소 101 / `docs/infra/research-log.md` 531 줄 · 161 · 103 / `docs/react/research-log.md` 504 줄 · 275 · 125 / `react-kit/references/project-detection.md` 62 줄 · 30 · 0 · 코드 블록 줄 12 / `tone-kit/references/sources.md` 169 줄 · 18 · 88 | 쪽 없음. `project-detection.md` 는 62 줄이라 400 줄 쪽(Gotcha 8)은 원본을 시각화해 채운다 | AR-01 · AR-03 · AR-04 |
| `scripts/check-docs-a11y.js` | `:59` 폭 `[320, 375, 768, 1280]` · `:131` `#theme-btn` · `:142` 합격 식 · `:144` 출력 줄(`basename`) | 320 폭이 이미 들어 있다. 출력이 파일 이름만 적어 `research-log.html` 셋이 겹쳐 보인다 — 도우미는 `OK` 줄 수와 검사한 줄 수로 센다 | ER-02 |
| `scripts/check-docs-links.py` · `scripts/check-contrast-claims.py` · `scripts/check-api-kit-docs.py` | 시작 판 `links_rc=0 내비 등록: 페이지 183 · 등록 183` · `contrast_rc=0 어긋난 것: 0` · `apikit_rc=0 12/12 PASS` | 통과 중 | AR-02 · ER-04 |
| `/Users/jackson/Hub/10_Dev/claude-plugins/.harness/handoff/2026-09-26-tools/ci-local.sh` | `:5-33` 단계 26 · `:35-36` CI 밖 단계 출력 | 시작 판(W) `rc=0` 25 · `feedback-agg-test SKIP (yq 없음)`. CI 에 있는데 도구에 없는 검사 단계 셋(`detect-docs-drift.py --check-table` · `check-cause-table-copies.py` · `measure-helpers-test.sh`)은 시작 판 모두 종료 코드 0 | DG-05 |

원본 담김 문턱(AR-03)의 근거 — 시작 판에서 드리프트 도구 매핑으로 짝지어지고 등록 · 파일이 있는 168 쌍을 같은 식(`coverage.py` · `fence2.py` 와 같은 글 뽑기)으로 쟀다. 사이트 중앙값 낱말 0.83 · 코드 표시 0.96 · 코드 블록 줄 0.80. 킷 중앙값: backend-kit 0.90 · 1.00 · 1.00 / infra-kit 0.89 · 1.00 · 1.00 / react-kit 0.54 · 0.29 · 0.46 / howto-kit 0.79 · 0.76 · 1.00 / harness 0.90 · 0.93 · 0.93 / tone-kit 0.96 · 1.00 · 0.81. 쪽마다 문턱은 사이트 중앙값 · 같은 킷 중앙값 · 그 쪽의 옛 판 값 가운데 가장 큰 값이다(`quality.html` 코드 블록 줄만 옛 판 0.86 이 가장 크다). 원본에 코드 표시나 코드 블록이 없으면 그 칸은 재지 않는다.

## Skill

- [ ] SK-01: docs-site 매핑 표는 고치지 않고도 열다섯 원본을 모두 맞는 출력 폴더로 덮는다 — `.claude/skills/docs-site/SKILL.md` 가 `BASE`→`TIP` 에서 바뀌지 않고, 표의 (원본, 출력 폴더) 짝이 열다섯 원본을 모두 덮으며(같은 원본이거나 `/` 로 끝나는 폴더 원본이 품고, 출력 칸이 대상 쪽의 폴더와 같다), 표와 스크립트 어긋남이 시작 판 0 에서 늘지 않는다. Given 공통 전제 G, When `m SK-01`, Then `skill_changed=0` 과 `fifteen_in_table=15/15 mismatch=0->0` [exact]
  측정: `m SK-01`. 시작 판 `skill_changed=0` · `fifteen_in_table=15/15 mismatch=0->0`
  양성 대조: 모의 나쁜 판(스크립트에 표 밖 폴더 매핑 한 줄을 더함) → `mismatch=0->1` (봉인 전 실측)

## Script

- [ ] SC-01: 드리프트 도구가 열다섯 원본을 바뀐 파일로 받으면 각각 대상 쪽 하나를 등록 · 파일 있음으로 고르고 `NEW` 가 0 이다 — 도우미가 끝점 트리의 `scripts/detect-docs-drift.py` 를 불러 바뀐 파일 목록만 열다섯 원본으로 바꿔 끼우고 `detect_drift` 를 그대로 돌린다(매핑 · 목차 대조 · 파일 확인은 도구 자신의 코드). Given 공통 전제 G, When `m SC-01`, Then 열다섯 줄 모두 `OK` 이고 끝줄 `fifteen_ok=15/15 new_entries=0` — 줄마다 고른 쪽이 정확히 하나, 그 경로가 `## 배경` 표의 대상 쪽과 같고 `registered=1 exists=1` [exact, enumerated]
  측정: `m SC-01`. 시작 판 `fifteen_ok=0/15 new_entries=15`(열다섯 모두 `(…, 0, 0)`)
  양성 대조: 모의 나쁜 판(덮어쓰기 매핑 없이 새 쪽 다섯만 만들고 등록) → `fifteen_ok=5/15 new_entries=10` (봉인 전 실측)
- [ ] SC-02: 드리프트 도구 매핑에서 달라진 원본은 다시 쓰는 열 원본뿐이고 각각 그 기존 쪽을 가리킨다 — 시작 판과 끝점 트리의 모든 파일(두 트리 합집합, `node_modules` · `.git` 제외)에 두 판의 매핑(`SOURCE_OVERRIDES` 우선, 없으면 `map_source_to_html`)을 돌려 결과가 다른 원본이 정확히 `## 배경` 표에서 종류가 「다시」 인 열 원본이고, 각 결과가 그 줄의 대상 쪽 하나이며, 그 밖 원본의 매핑은 그대로이고 `SOURCE_EXCLUDES` 도 그대로다. Given 공통 전제 G, When `m SC-02`, Then `delta_n=10 delta_good=10/10 delta_outside=0 excludes_same=1` [exact, enumerated]
  측정: `m SC-02`. 시작 판 `delta_n=0 delta_good=0/10 delta_outside=0 excludes_same=1`
  양성 대조: 모의 나쁜 판(열 밖 원본 `docs/react/wasm-catalog.md` 에 덮어쓰기 매핑 한 줄을 더함) → `delta_n=11 delta_good=10/10 delta_outside=1` (봉인 전 실측)
- [ ] SC-03: 매핑과 사람용 표 맞대기 검사가 통과한다 — 끝점 트리에서 `python3 scripts/detect-docs-drift.py --check-table` 의 종료 코드가 0 이고 끝줄이 `어긋남 0` 으로 끝난다. Given 공통 전제 G, When `m SC-03`, Then `check_table_rc=0` 과 `어긋남 0` [exact]
  측정: `m SC-03`. 시작 판 `check_table_rc=0 매핑 맞대기: 스크립트 35 짝 · 표 34 짝 · 어긋남 0`
  양성 대조: 모의 나쁜 판(스크립트에만 표 밖 폴더 매핑을 더함) → `check_table_rc=1` (봉인 전 실측)

## Error

- [ ] ER-01: 열다섯 쪽이 320 · 375 · 1280 폭 × 밝은 · 어두운 테마 여섯 칸 모두에서 가로로 넘치지 않고 잘린 글이 없으며, 두 테마가 실제로 다르게 그려진다 — 도우미 `pw.js of` 가 쪽마다 두 테마 각각 브라우저 색 설정 · `dk-theme` 저장값 · `data-theme` 을 맞춰 연 뒤 세 폭에서 `max(html, body)` 의 `scrollWidth - clientWidth` 와, 글을 직접 가진 요소 가운데 스크롤도 안 되면서(`overflow-x` 가 `visible` · `auto` · `scroll` 이 아님) 내용이 상자보다 넓은 요소 수를 잰다. Given 공통 전제 G, When `m ER-01`, Then 열다섯 줄이 모두 `OK` 이고 각 칸 값이 `0/0` · `theme_differs=1`, 끝줄 `of_ok=15/15 cells_zero=90/90` [exact, enumerated]
  측정: `m ER-01`. 시작 판 `of_ok=1/15 cells_zero=60/60`(쪽 없는 다섯 `ABSENT`, 여덟 react 쪽 · feedback-system 은 `theme_differs=0`)
  양성 대조: 모의 나쁜 판(폭 1900px 블록을 넣은 쪽 · `overflow-x:hidden` 에 줄바꿈 없는 긴 글을 넣은 쪽) → 넘침 칸 값 1 이상 · 잘림 칸 값 1 이상 · `BAD` (봉인 전 실측)
- [ ] ER-02: 레포 접근성 검사가 열다섯 쪽을 모두 통과한다 — `node scripts/check-docs-a11y.js` 에 열다섯 쪽을 넘기면(320 · 375 · 768 · 1280 넘침 · 콘솔 오류 · 모든 글자 요소 대비 · 밝은 테마 규칙 유무) 종료 코드 0, 검사한 줄 15, 그 가운데 `OK` 이고 `theme=both` 인 줄 15 다. Given 공통 전제 G, When `m ER-02`, Then `absent=0` · `a11y_rc=0 ok_both=15/15 checked=15` [exact]
  측정: `m ER-02`(끝점 트리에서 레포 검사기를 그대로 부름). 시작 판 `absent=5` · `a11y_rc=0 ok_both=1/15 checked=10`(열 쪽 중 `theme=both` 는 `overview.html` 하나)
  양성 대조: 모의 나쁜 판(외부 스타일 링크 · 넓은 블록을 넣은 쪽) → `FAIL … err=1` · `a11y_rc=1` (봉인 전 실측)
- [ ] ER-03: 목차에서 열다섯 쪽을 누르면 각 쪽이 뜬다 — 1280 폭으로 `docs/index.html` 을 열어, 끝점 `docs/index.html` 에서 그 파일을 가리키는 항목의 id 로 `.nav-item[data-id=…]` 를 하나 찾아 누르면, 주소가 그 파일로 끝나는 iframe 이 생기고 그 안의 글이 1000 자를 넘고 문서 제목이 비지 않는다. Given 공통 전제 G, When `m ER-03`, Then 열다섯 줄 `OK` · 끝줄 `nav_ok=15/15 console_err=0` [exact, enumerated]
  측정: `m ER-03`. 시작 판 `nav_ok=10/15 console_err=0`(새 다섯 `nav_items=0`)
  양성 대조: 모의 나쁜 판(새 쪽 하나를 이미 쓰는 id `api-research-log` 로 등록) → `nav_items=2` · `BAD` (봉인 전 실측)
- [ ] ER-04: 문서 사이트 검사 둘이 끝점 트리에서 통과한다 — `python3 scripts/check-contrast-claims.py` 종료 코드 0 · `어긋난 것: 0`, `python3 scripts/check-api-kit-docs.py` 종료 코드 0 · `12/12 PASS`. Given 공통 전제 G, When `m ER-04`, Then `contrast_rc=0 어긋난 것: 0` · `apikit_rc=0 12/12 PASS` [exact]
  측정: `m ER-04`. 시작 판 같은 값
  양성 대조: 모의 나쁜 판(새 쪽에 `#757575 on #FFFFFF` 와 `3.5:1 FAIL` 을 한 줄에 적음) → `contrast_rc=1` (봉인 전 실측)

## Architecture

- [ ] AR-01: 열다섯 쪽이 문서 사이트 틀을 지킨다 — 새 다섯은 `BASE`→`TIP` 차이에서 추가(`A`), 다시 쓴 열은 수정(`M`)이고, 쪽마다 `wc -l` 과 같은 줄 수가 400 이상(Gotcha 8), `../assets/site.css` 를 가리키는 `<link>` 가 정확히 하나이면서 첫 `<style` 앞에 있고(Gotcha 1), 그 밖의 외부 자원이 0 이며(따옴표 모양과 무관하게 다른 `<link>` · `<script src=` · 레포 밖 주소의 `<img>` · `<iframe>` · `<source>` · `<video>` · `<audio>` · `<embed>` · CSS `@import` · `url(//…)` · `url(http…)`), `:root` 의 `--accent` 가 `## 배경` 의 킷 색과 같다. Given 공통 전제 G, When `m AR-01`, Then `added=5 modified=10` 과 끝줄 `exist=15/15 lines=15/15 css1=15/15 ext0=15/15 accent=15/15` [exact, enumerated]
  측정: `m AR-01`. 시작 판 `added=0 modified=0` · `exist=10/15 lines=10/15 css1=10/15 ext0=10/15 accent=10/15`
  양성 대조: 모의 나쁜 판(작은따옴표 `<script src='//x.js'>` 한 줄 · `@import` 한 줄 · 색을 비움 · 152 줄) → `ext=2 accent=None lines=152`, 외부 스타일 링크 한 줄을 더한 쪽 → `ext=1` (봉인 전 실측)
- [ ] AR-02: 열다섯 쪽이 각자 킷 목차에 한 번씩 오르고 아이콘을 가지며 id 가 겹치지 않는다 — 끝점 `docs/index.html` 의 `categories` 에서 `file:` 이 그 쪽인 항목이 정확히 하나이고 그 항목이 든 묶음의 `label` 이 `## 배경` 표의 킷 목차 이름으로 시작하며, `getIcon` 에 그 id 키가 있고, 사이트 전체에서 두 번 이상 쓰인 id 가 시작 판보다 늘지 않는다. `docs/index.html` 차이는 더한 줄 10(새 쪽마다 목차 한 줄 · 아이콘 한 줄) · 빠진 줄 0 이다. 레포 링크 검사(`scripts/check-docs-links.py`)가 끝점 트리에서 종료 코드 0 이고 등록 수 줄이 `페이지 188 · 등록 188` 이다. Given 공통 전제 G, When `m AR-02`, Then `reg_ok=15/15 icon_ok=15/15 dup_ids=0->0 added=10 deleted=0` · `links_rc=0 내비 등록: 페이지 188 · 등록 188` [exact, enumerated]
  측정: `m AR-02`. 시작 판 `reg_ok=10/15 icon_ok=10/15 dup_ids=0->0 added=0 deleted=0` · `links_rc=0 내비 등록: 페이지 183 · 등록 183`
  양성 대조: 모의 나쁜 판(새 쪽 하나를 `api-research-log` id 로 등록) → `dup_ids=0->1`, 등록 없는 쪽 파일 → `links_rc=1` (봉인 전 실측)
- [ ] AR-03: 열다섯 쪽이 원본을 사이트 수준 이상으로 담고, 다시 쓴 열은 옛 판에서 담던 것을 하나도 잃지 않는다 — 쪽마다 원본 낱말(백틱 밖 2 자 이상) 가운데 쪽 글에 든 비율, 원본 코드 표시 가운데 쪽 글에 든 비율, 원본 코드 블록 줄(공백 뺀 8 자 이상) 가운데 쪽 글(공백 뺌)에 든 비율이 도우미 `FIFTEEN` 의 문턱 이상이다(소수 둘째 자리 반올림으로 견줌). 문턱(낱말 · 코드 표시 · 코드 블록 줄): `docs/backend-kit/research-log.html` 0.90 · 1.00 · 없음 / `docs/howto-kit/overview.html` 0.83 · 0.96 · 1.00 / `docs/infra-kit/research-log.html` 0.89 · 1.00 · 없음 / `docs/react-kit/integration.html` · `scaffolding.html` · `state-data.html` · `performance.html` · `ui-patterns.html` · `animation.html` · `build-audit.html` 0.83 · 0.96 · 0.80 / `docs/react-kit/quality.html` 0.83 · 0.96 · 0.86 / `docs/react-kit/research-log.html` 0.83 · 0.96 · 없음 / `docs/harness/feedback-system.html` 0.90 · 없음 · 없음 / `docs/react-kit/project-detection.html` 0.83 · 0.96 · 0.80 / `docs/tone-kit/sources.html` 0.96 · 1.00 · 없음. 다시 쓴 열은 더해서, 옛 판(`BASE`)에 들어 있던 원본 코드 표시와 코드 블록 줄이 새 판에 모두 있고(`lost_code=0 lost_fence=0`) 낱말 비율이 옛 판 값 이상이다 — 옛 판 값은 `## 배경` 표. Given 공통 전제 G, When `m AR-03`, Then 열다섯 줄 `OK` · `cov_ok=15/15` [exact, enumerated]
  측정: `m AR-03`. 시작 판 `cov_ok=0/15`(새 다섯 `ABSENT`, 열은 문턱 미달 `BAD`)
  알려진 답: 시작 판 `docs/react-kit/integration.html` 을 도우미로 재면 `wr=0.48 code=38/87 fence=29/253` 이고 인계 도구 `coverage.py`(`wr=0.48->0.48 codes=87 new=38`) · `fence2.py`(`lines=253 in_new=29`)와 같다 (봉인 전 실측, 종료 코드 0)
  양성 대조: 모의 나쁜 판(`quality.html` 자리에 다른 킷 쪽 사본) → `lost_code` 1 이상 · `BAD` (봉인 전 실측)
- [ ] AR-04: 원본의 출처 주소가 모두 쪽의 링크로 옮겨진다 (Gotcha 9) — 원본 열다섯의 `http(s)://` 주소(백틱 안 · `localhost` · `127.0.0.1` 은 뺌, 끝의 `.,;:` 뺌, 합계 515 개: backend research-log 101 · infra research-log 103 · react research-log 125 · tone sources 88 · react 설계 여덟 98(integration 1 · scaffolding 16 · state-data 17 · performance 13 · quality 15 · ui-patterns 7 · animation 17 · build-audit 12) · 나머지 0)가 각 쪽의 `href` 로 모두 있다. Given 공통 전제 G, When `m AR-04`, Then 열다섯 줄 `OK` · `url_ok=15/15 src_urls_total=515 checked_urls=515` [exact, enumerated]
  측정: `m AR-04`. 시작 판 `url_ok=4/15 src_urls_total=515 checked_urls=98`
  양성 대조: 시작 판 자체 — `scaffolding.html` `missing=10` 등 여섯 쪽 `BAD` (봉인 전 실측)
- [ ] AR-05: 넘침을 가려서 없애지 않는다 (Gotcha 11) — 열다섯 쪽의 `<style>` 안과 `style` 속성(따옴표 모양 무관, CSS 주석 뺌)에 `overflow`(`-x` · `-y` 포함) `hidden` · `clip` 선언과 `text-overflow:ellipsis` 가 0 이다. Given 공통 전제 G, When `m AR-05`, Then 끝줄에 `hide0=15/15` [exact]
  측정: `m AR-05`. 시작 판 `hide0=9/15`(`feedback-system.html` `hide=1`, 새 다섯 없음)
  양성 대조: 시작 판 `feedback-system.html` → `hide=1` (봉인 전 실측)
- [ ] AR-06: 바뀐 파일이 범위 목록과 정확히 같고 계약 봉인이 깨지지 않는다 — `git diff --name-status BASE TIP -- . ':(exclude).harness'` 의 경로 집합이 `## 범위 경계` 의 `# sprint-scope` 블록 17 경로와 정확히 같고(더 많지도 적지도 않음), 상태가 추가 5 · 수정 12, 전체 차이(`.harness` 포함)에 PNG 0 이다. `.harness/` 는 이름을 열거하지 않고 끝점 트리의 `sprint-contract*.md` 모두에 봉인 검사를 돌려 `SEAL_BROKEN` 이 0 이다. Given 공통 전제 G, When `m AR-06`, Then `scope_n=17 extra=0 missing=0 png=0 status=A5 M12` · `seal_broken=0` [exact]
  측정: `m AR-06`(범위 목록은 계약의 블록을 그대로 읽는다). 시작 판 `scope_n=17 extra=0 missing=17 png=0`
  양성 대조: 모의 나쁜 판 → `extra` 1 이상 · `png=1`(`docs/cap.png`), 앞 계약 조건 줄 끝에 글자를 더한 판 → `seal_broken=1` (봉인 전 실측)
- [ ] AR-07: 커밋이 묶음 둘을 섞지 않고 `.harness/` 와 구현 파일을 섞지 않는다 — `BASE` 부터 `TIP` 까지 병합 아닌 커밋마다 `.harness/` 밖 파일의 묶음(맨 위 폴더, `docs/` 아래는 `docs/<폴더>`, `docs/index.html` 처럼 `docs/` 바로 아래 파일은 묶음으로 세지 않음)이 둘 이상인 커밋 0, `.harness/` 파일과 그 밖의 파일을 함께 담은 커밋 0, 구현 커밋 1 이상. Given 공통 전제 G, When `m AR-07`, Then `multi_unit=0 mixed=0` 이고 `impl_commits` 1 이상 [exact]
  측정: `m AR-07`. 시작 판 `commits=0 impl_commits=0 multi_unit=0 mixed=0`
  양성 대조: 모의 나쁜 판(notes · `docs/tone-kit/` · `scripts/` 를 한 커밋에) → `multi_unit=1 mixed=1` (봉인 전 실측)
- [ ] AR-08: 결정과 넘김을 notes 에 남긴다 — Given 끝점 `TIP`, notes 가 커밋돼 있고 열두 토큰 `DC-9` · `dca-notes` · `Gotcha 7` · `RE-02` · `tone-guide` · `feedback-schema` · `design-brief` · `kit-design` · `research-log` · `sources.md` · `check-table` · `DC-12` 가 각각 한글 15 자 이상인 줄에 1 번 이상 든다. 담을 내용: 짝 목록의 새 이름 대신 기존 열 쪽을 다시 쓴 까닭(`DC-9` · `dca-notes` 결정, `Gotcha 7` · `RE-02`), `design-brief` 를 개요 쪽에, `feedback-schema` 를 피드백 시스템 쪽에 담은 방법(키 표 · 예시), `kit-design` 설계 문서 여덟이 사용자 결정 UD-6 으로 현행화된 판을 옮겼다는 것, `research-log` 셋과 `sources.md` 를 새 쪽으로 만든 근거(사용자 결정 DC-1 과 api 연구 기록 쪽 선례, dca 결정과 다른 점), `tone-guide` 1 · 5 단계 결과, `check-table` 결과, 어두운 테마뿐이던 쪽에 밝은 테마를 넣은 것과 목록 `DC-12`(어두운 테마 전용 쪽) 와의 관계. Given 공통 전제 G, When `m AR-08`, Then `committed=1` 이고 열두 값 모두 1 이상 [exact, enumerated]
  측정: `m AR-08`. 시작 판 `committed=0` · `notes=absent`
  양성 대조: 토큰만 짧게 적은 줄의 notes → 열두 값 모두 `0` (봉인 전 실측). 평가자는 셈이 잡은 줄마다 그 줄이 실제로 그 결정이나 넘김을 설명하는지 한 번 눈으로 읽는다 — 토큰을 끼워 넣은 빈말 줄이면 그 값은 0 으로 본다
- [ ] AR-09: 열다섯 쪽을 브라우저로 캡처해 눈으로 확인했고 캡처는 커밋하지 않았다 — notes 에 `캡처 폴더: \`<절대 경로>\`` 한 줄이 있고, 그 폴더에 쪽마다 `320` · `375` · `1280` 세 폭 × `dark` · `light` 캡처가 이름 규칙 `<docs 아래 폴더>__<쪽 이름>-<폭>-<테마>.png` 로 모두 있고 비어 있지 않으며, 규칙 밖 이름의 PNG 가 0 이다. PNG 가 커밋되지 않은 것은 AR-06 `png=0` 이 잰다. Given 공통 전제 G, When `m AR-09`, Then `cap_need=90 cap_have=90 cap_badname=0` [exact, collective]
  측정: `m AR-09`. 시작 판 `cap_dir=absent`
  양성 대조: 모의 판(90 장 중 한 장을 빼고 이름 틀린 한 장을 넣음) → `cap_need=90 cap_have=89 cap_badname=1` (봉인 전 실측)
- [ ] AR-10: YAML 원본은 키 표와 예시로 옮긴다 — `harness/references/feedback-schema.yaml` 의 키 41 개(주석으로 정의한 필드 40 과 `schema_version`, 감싸는 이름 `example` 은 뺌)가 `docs/harness/feedback-system.html` 의 `<table>` 안 글에 낱말 경계로 모두 있고, 그 쪽의 `<pre>` 가운데 태그를 벗겨 YAML 로 읽은 값이 원본 `example` 값(또는 `example:` 로 감싼 값)과 같은 것이 1 개 이상이다. Given 공통 전제 G, When `m AR-10`, Then `keys=41 in_table=41` · `example_same` 1 이상 [exact]
  측정: `m AR-10`. 시작 판 `keys=41 in_table=8 example_same=0`
  알려진 답: 키 41 은 손으로 센 값과 같다 — 주석 정의 40(`ambiguous_conditions` 부터 `verdict` 까지) + `schema_version` (봉인 전 실측)
  양성 대조: 시작 판 자체(`in_table=8 example_same=0`), 모의 좋은 판(키 표 · 예시 `<pre>` 를 넣은 쪽) → `in_table=41 example_same=1` (봉인 전 실측)

## Anti-patterns

- [ ] AP-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수 (```text, ```bash, ```yaml 등). 판정 권위는 validate-plugin V6 상태기계다 — 여는/닫는 fence 가 동형이라 줄 단위 정규식으로는 판정 불가
  이 계약에 적용: 새 notes 의 언어 표시 없는 여는 울타리가 0 이다. 측정: `m AP-03` 이 `notes=absent->0`, 킷 전체는 DG-05 의 `validate-plugin rc=0`. 양성 대조: 언어 없는 울타리를 넣은 모의 notes → `notes=absent->1` (봉인 전 실측)

## Reusability

- [ ] RE-01: N/A (산출물이 정적 문서 쪽 · 목차 줄 · 매핑 줄이라 비공개로 숨길 재사용 단위 코드가 없다. 쪽 스크립트는 틀의 테마 전환을 그대로 쓴다 — RE-02 가 잰다. 측정: `m RE-02` 의 `new_scripts=0`)
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다
  이 계약에 적용: 원본에 이미 쪽이 있는 열은 새 쪽을 만들지 않고 그 쪽을 다시 쓴다(AR-01 `added=5 modified=10`), 열다섯 쪽이 틀의 테마 전환(`dk-theme` 키)과 밝은 테마 규칙(`[data-theme="light"]`)을 쓰고, 공통 파일이 맡는 움직임 줄이기를 쪽에 다시 적지 않으며(`prefers-reduced-motion` 0, Gotcha 1), 새 스크립트 · 스타일 파일을 더하지 않는다. 측정: `m RE-02` 가 `theme=15/15 light=15/15 rm0=15/15` · `new_scripts=0`(시작 판 `theme=1/15 light=1/15 rm0=5/15` · `new_scripts=0`). 양성 대조: 시작 판 `animation.html` → `rm=5` (봉인 전 실측)

## Diagnostics

- [ ] DG-01: N/A (commands.analyze `bash -n scripts/release.sh` 가 재는 `scripts/release.sh` 는 이번 바뀐 파일에 없다. 측정: `m DG-01` 이 `release_paths=0`. 스크립트 쪽 실제 검사는 DG-02 의 `py_compile` · `cli_rc` 와 DG-05) [exact]
- [ ] DG-02: IDE diagnostics 워닝/인포 0개 ([] 제외)
  편집기 진단을 명령줄로 같게 잰다(계약 · QA 리포트 · 개정 파일은 뺀다): 열다섯 쪽과 `docs/index.html` 가운데 짝 안 맞는 HTML 태그 수가 시작 판보다 늘어난 파일 0, notes 의 markdownlint-cli2 0.23.2(MD013 끔, 편집기 확장과 같은 설정) 경고 0, `scripts/detect-docs-drift.py` 의 `python3 -m py_compile` 출력 0 줄, 끝점 트리에서 `python3 scripts/detect-docs-drift.py --since BASE` 종료 코드 0. 측정: `m DG-02` 가 `tag_worse=0 md_notes=0 py_compile=0 cli_rc=0` (시작 판 `tag_worse=0 md_notes=absent py_compile=0 cli_rc=0`). 양성 대조: 닫지 않은 `<div>` 를 넣은 모의 쪽 → `tag_worse=1`, 언어 없는 울타리 notes → `md_notes=1` (봉인 전 실측). 설치가 안 되면(망 끊김 등) 도우미가 `md=ENV_FAIL` 을 찍는다 — 그 칸만 `[미검증:ENV]` 로 적고 나머지 칸은 그대로 판정한다
- [ ] DG-03: N/A (commands.test `bash scripts/release.sh 2>&1 || true` 가 재는 `scripts/release.sh` 는 이번 바뀐 파일에 없다. 측정: DG-01 과 같은 `m DG-01` 이 `release_paths=0`) [exact]
- [ ] DG-04: 실제 앱/서버 구동 시 에러 0개
  이 계약에 적용: 구동할 앱은 문서 사이트다. 열다섯 쪽을 따로 열 때와 목차에서 열 때 콘솔 오류 · 페이지 오류가 0 이다. 측정: `m DG-04` 가 ER-02 끝줄 `a11y_rc=0 ok_both=15/15 checked=15`(각 `OK` 줄 `err=0`)과 ER-03 끝줄 `nav_ok=15/15 console_err=0`. 양성 대조: 외부 스타일 링크를 넣은 모의 쪽 → `err=1` (봉인 전 실측)
- [ ] DG-05: CI(자동 검사) 단계를 로컬에서 전부 돌려 통과한다 — Given 작업 폴더 W 가 끝점과 같다(`git -C W rev-parse HEAD` 가 `TIP` 이고 `git -C W status --porcelain --untracked-files=no` 가 빈 출력 — 아니면 도우미가 `W_NOT_TIP` 을 찍고 멈춘다), When `m DG-05` 가 `/Users/jackson/Hub/10_Dev/claude-plugins/.harness/handoff/2026-09-26-tools/ci-local.sh` 를 W 에 돌려 그 요약 파일을 읽고, CI 에 있는데 그 도구에 없는 검사 단계 셋을 따로 돌리면, Then `tool_same=1 rc0=25 other=[feedback-agg-test SKIP (yq 없음);]` 과 `extra_steps check_table=0 cause_copies=0 measure_helpers=0` 이고, `outside=` 칸이 설치 단계(`pip install pyyaml` · `zsh` 설치 · `npm ci` · `npx playwright install --with-deps chromium`) · 여러 줄 `run: |` · 위 셋 단계뿐이다 [exact]
  측정: `m DG-05`. 도구 파일은 이 가지 밖(본 체크아웃)에 있어 커밋으로 고정되지 않으므로 도우미가 그 내용 지문(`git hash-object`)을 봉인 때 값 `TOOL_BLOB` 과 대조한다. 시작 판(W 가 `38cccd1`) `rc0=25 other=[feedback-agg-test SKIP (yq 없음);]` · 세 단계 모두 0, 지문 `01528e5a5c0dfe27a6a9c0bb8ae1c830f2f04860`. `tool_same=0` 이거나 요약 파일이 없으면(`ci_summary=absent`) 그 회차는 `[미검증:ENV]` 로 적는다
  음성 대조: 이 계약이 기대는 `docs-a11y` 단계는 ER-02 양성 대조처럼 넘치는 쪽을 넣으면 `rc=1`, `docs-links` 단계는 AR-02 양성 대조처럼 등록 없는 쪽을 넣으면 `rc=1`, `check_table` 은 SC-03 양성 대조처럼 `1` 이 된다

## 범위 경계

이 스프린트가 고칠 경로(커밋 직전 훅과 AR-06 이 이 블록을 읽는다 — `.harness/` 는 적지 않아도 늘 허용):

```text
# sprint-scope
docs/backend-kit/research-log.html
docs/howto-kit/overview.html
docs/infra-kit/research-log.html
docs/react-kit/integration.html
docs/react-kit/scaffolding.html
docs/react-kit/state-data.html
docs/react-kit/performance.html
docs/react-kit/quality.html
docs/react-kit/ui-patterns.html
docs/react-kit/animation.html
docs/react-kit/build-audit.html
docs/react-kit/research-log.html
docs/harness/feedback-system.html
docs/react-kit/project-detection.html
docs/tone-kit/sources.html
docs/index.html
scripts/detect-docs-drift.py
```

항목별 처리:

| 항목 | 처리 | 조건 · 사유 |
| --- | --- | --- |
| 짝 목록 NEW 가운데 대응 쪽이 정말 없는 다섯(research-log 셋 · react project-detection · tone sources) | 계약에 넣음 — 새 쪽 | AR-01 ~ AR-05 · AR-09 · ER-01 ~ ER-03 · SC-01. 매핑은 이미 이 이름을 내므로 목차 등록과 파일만 생기면 된다 |
| 짝 목록 NEW 가운데 이름만 다른 기존 쪽이 있는 열(react 설계 여덟 · design-brief · feedback-schema) | 계약에 넣음 — 기존 쪽을 다시 쓰고 매핑으로 잇는다 | 짝 목록의 새 이름(`g1-scaffolding.html` · `design-brief.html` · `feedback-schema.html` 등)은 만들지 않는다. 근거는 `## 배경` 셋째 불릿(Gotcha 7 · RE-02 · dca DC-9 결정). SC-01 · SC-02 · AR-03 |
| 드리프트 도구 매핑 | 계약에 넣음 | 열 원본만 덮어쓰기 매핑을 더한다(SC-02 `delta_outside=0`). 폴더째 매핑하지 않는다 |
| docs-site `SKILL.md` 매핑 표 | 고치지 않음 | 표가 폴더 단위라 열다섯을 이미 덮는다(SK-01 · SC-03). 표를 고치면 다른 묶음과 한 줄씩 부딪힐 수 있다 |
| dca DC-9 결정표의 나머지(`react-kit/references/` 새 쪽 넷 · bambu 셋 · flutter · harness · reflect 등) | 범위 밖 · notes | 짝 목록 NEW 가 아니다(목록은 경고 정리 전 판 `c3e45f3` 에서 NEW 로 뜬 것만 담았다). 부모 과제 범위 밖 |
| 원본 md · YAML 고침 | 범위 밖 | 쪽을 원본에 맞추는 일이다. 원본 오류를 보면 notes 에 적는다 |
| 목록 DC-12(어두운 테마 전용 쪽의 밝은 테마) | 이 열 쪽만 겹침 · notes | 다시 쓰는 열 가운데 아홉이 어두운 테마뿐이라 이 계약이 밝은 테마를 넣는다(ER-01 · RE-02). 나머지 DC-12 쪽은 범위 밖 |
| 틀(`page-template.html`) · 공통 파일(`docs/assets/site.css`) · 다른 쪽 | 범위 밖 | AR-06 이 바뀐 파일을 열일곱으로 묶는다 |
| `docs/index.html` 의 기존 열 항목 제목 | 그대로 | AR-02 `deleted=0`. 제목을 바꿔야 하면 개정으로 처리한다 |

커버리지 해소 — Step 6.5 (4) 검출기가 낸 `UNCOVERED` 와 목록을 한 곳에만 둔 조건:

- 커버리지 해소: 열다섯 쪽 · 원본을 열거한 조건(SC-01 · SC-02 · ER-01 · ER-03 · AR-01 ~ AR-05) — 목록은 `## 배경` 표와 도우미 `FIFTEEN` 에 같은 글자로 있고 `m` 이 그 목록을 잰다. 측정 절에 열다섯 경로를 되풀이해 적지 않는다
- 커버리지 해소: AR-03 · AR-04 — 산문에 적은 쪽 경로와 문턱 · 주소 수는 `FIFTEEN` 다섯째 ~ 일곱째 칸과 봉인 전 실측 값이며 `m AR-03` · `m AR-04` 가 그 목록을 잰다
- 커버리지 해소: AR-06 — 범위 목록은 위 `# sprint-scope` 블록 한 곳에만 있고 도우미 `SCOPE` 가 그 블록을 읽는다
- 커버리지 해소: SK-01 · SC-03 · AR-02 · ER-04 — 산문의 `.claude/skills/docs-site/SKILL.md` · `scripts/detect-docs-drift.py` · `docs/index.html` · `scripts/check-*.py` 는 대상이 아니라 도우미가 끝점 트리에서 읽거나 부르는 파일이다
- 커버리지 해소: ER-03 — `docs/index.html` 은 대상이 아니라 도우미가 끝점 트리에서 id 를 읽고 여는 목차 파일이다(`pg.py ids` · `pw.js nav`)
- 커버리지 해소: AR-01 — `../assets/site.css` 는 판정 기준(공통 파일 링크)이고 `url(//…)` 은 외부 자원 모양의 예다. 둘 다 `pg.py pages` 가 정규식으로 잰다
- 커버리지 해소: AR-04 — `http(s)://` · `127.0.0.1` 은 대상이 아니라 주소 뽑기 규칙과 뺄 주소다(`pg.py urls`)
- 커버리지 해소: AR-08 — `sources.md` 는 notes 에서 세는 토큰 열둘 가운데 하나이며 도우미 `m AR-08` 의 토큰 목록에 같은 글자로 있다
- 커버리지 해소: AR-10 — `harness/references/feedback-schema.yaml` · `docs/harness/feedback-system.html` 은 `FIFTEEN` 의 YAML 줄이며 `m AR-10` 이 그 줄만 고른다

교차 진단(qa-evaluator) 때 주의:

- AR-03 의 문턱과 `## 배경` 의 옛 판 값은 시작 판에서 잰 값이다. 평가자는 다시 재지 않아도 된다 — 문턱은 봉인과 함께 고정된다. 다시 쓴 열의 「잃지 않음」 은 도우미가 `BASE` 트리의 쪽과 직접 견준다
- 계약 파일의 편집기 경고(첫 줄 제목 없음 · 코드 표시 안 공백 등)는 계약 형식에서 나온다. 계약 · QA 리포트 · 개정 파일은 DG-02 대상에서 뺀다
- 짝 목록과 다른 쪽 이름을 쓴 까닭은 `## 배경` 셋째 불릿이다. 부모가 짝 목록 이름 그대로를 원하면 이 계약을 봉인하지 말고 다시 쓴다

## 회귀 게이트 — 측정 도우미 · 봉인 전 실측

평가 때 이 블록을 떼어 bash 에서 불러 쓴다. `TMPDIR` 은 평가자 임시 폴더로 준다. 도우미는 `$T` 아래에만 쓴다 — 작업 폴더와 그 밖의 입력은 지우지 마라.
브라우저 도구는 작업 폴더 W 의 `node_modules`(추적 안 되는 폴더, 봉인 전 실측 때 `ci-local.sh` 가 `npm ci` 로 설치함)를 `NODE_PATH` 로 빌려 쓰고, 푼 트리마다 그 폴더를 가리키는 연결을 만든다.

준비 단계 실측(봉인 전, 이 기계): `command -v node` · `python3` · `git` · `shasum` 종료 코드 0, W 의 `node_modules/playwright-core` 있음, `python3 -c 'import yaml'` 판 `6.0.3`, `ci-local.sh` 지문 `01528e5a5c0dfe27a6a9c0bb8ae1c830f2f04860`. 브라우저가 없으면 `Executable doesn't exist` 로 멈춘다 — 복구: `cd W && node_modules/.bin/playwright-core install chromium-headless-shell` 뒤 다시 잰다. 브라우저가 없어 못 잰 조건은 FAIL 이 아니라 환경 실패로 보고한다.
Playwright 쓰임(`newContext` 의 `viewport` · `colorScheme` · `reducedMotion`, `addInitScript` 인자, `setViewportSize`, `locator().count()` · `click`, `page.frames()` · `frame.url()` · `frame.evaluate`)은 앞 계약 `after-0926-docs-new-pages` 가 Context7 `/microsoft/playwright/v1.58.2` 문서와 맞춰 본 호출과 같다 — 이 도우미가 새로 더한 호출은 없다(잘림 검사는 쪽 안 `getComputedStyle` 만 쓴다).
봉인 전 실측은 `BASE_REF=38cccd1 E_REF=BASE` 로 잰 시작 판 값과, 임시 복제본(`W=<복제본> NM=<W 의 node_modules>`)에 모의 나쁜 판 · 좋은 판을 커밋해 잰 값이다. 복제본은 세션 임시 폴더에 두었고 이 가지와 무관하다.
도우미는 zsh 에서 부르지 마라 — zsh 는 따옴표 없는 변수를 낱말로 나누지 않아 쪽 목록이 한 덩어리가 된다.

```bash
# 떼기: awk '/^# === 측정 도우미 시작/{f=1} f{print} /^# === 측정 도우미 끝/{exit}' <계약> > "$TMPDIR/dr2-measure.sh"
# 부르기: bash -c 'source "$TMPDIR/dr2-measure.sh" || exit 2; type m >/dev/null || exit 2; m SK-01'
# 봉인 커밋이 아직 없을 때: BASE_REF=<커밋> 을 준다. 시작 판을 재려면 E_REF=BASE. 임시 복제본을 재려면 W=<복제본> NM=<node_modules 경로>
# === 측정 도우미 시작 (after-0926-docs-new-pages-2) ===
# 쓰는 법: 이 블록을 파일로 떼어 bash 에서 source 한 뒤 `m <조건 ID>`. zsh 에서 부르지 마라(따옴표 없는 변수를 낱말로 나누지 않아 목록이 한 덩어리가 된다).
# 끝점 TIP = 가지 끝. 시작점 BASE = 이 계약을 처음 담은 커밋(봉인 커밋)의 부모 — 커밋 번호를 박지 않고 git 기록에서 푼다.
# 봉인 커밋이 아직 없으면 BASE_REF=<커밋> 을 준다. 시작 판 자체를 재려면 E_REF=BASE. 임시 복제본을 재려면 W=<복제본> NM=<node_modules 경로>.
W=${W:-/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak2-dr2}
BR=${BR:-chore/ak2-dr2}
SLUG=after-0926-docs-new-pages-2
CF_REL=.harness/sprint-contract-$SLUG.md
NOTES=.harness/.meta/after-kaizen-0926b/dr2-notes.md
TIP=$(git -C "$W" rev-parse --verify -q "$BR^{commit}") || { echo "UNRESOLVED TIP"; return 2 2>/dev/null || exit 2; }
if [ -n "${BASE_REF:-}" ]; then
  BASE=$(git -C "$W" rev-parse --verify -q "$BASE_REF^{commit}") || { echo "UNRESOLVED BASE_REF"; return 2 2>/dev/null || exit 2; }
else
  SEAL=$(git -C "$W" log --diff-filter=A --format=%H "$TIP" -- "$CF_REL" | tail -1)
  [ -n "$SEAL" ] || { echo "UNRESOLVED SEAL (봉인 커밋 없음)"; return 2 2>/dev/null || exit 2; }
  BASE=$(git -C "$W" rev-parse --verify -q "$SEAL^") || { echo "UNRESOLVED BASE"; return 2 2>/dev/null || exit 2; }
fi
T=$(mktemp -d "${TMPDIR:-/tmp}/dr2.XXXXXX")
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
# 원본 | 쪽 | 킷 목차 이름 첫머리 | --accent | 낱말 문턱 | 코드 표시 문턱(- 는 원본에 코드 표시 없음) | 코드 블록 줄 문턱(- 는 원본에 코드 블록 없음) | new=새 쪽 · re=기존 쪽을 다시 씀
# 문턱 = 시작 판 등록 짝 168 쌍의 사이트 중앙값(0.83 · 0.96 · 0.80) · 같은 킷 중앙값 · 그 쪽의 옛 판 값 가운데 가장 큰 값
FIFTEEN='docs/backend/research-log.md|docs/backend-kit/research-log.html|Backend Kit|#A78BFA|0.90|1.00|-|new
docs/howto/design-brief.md|docs/howto-kit/overview.html|Howto Kit|#F59E0B|0.83|0.96|1.00|re
docs/infra/research-log.md|docs/infra-kit/research-log.html|Infra Kit|#34D399|0.89|1.00|-|new
docs/react/kit-design/final-integration.md|docs/react-kit/integration.html|React Kit|#38BDF8|0.83|0.96|0.80|re
docs/react/kit-design/g1-scaffolding.md|docs/react-kit/scaffolding.html|React Kit|#38BDF8|0.83|0.96|0.80|re
docs/react/kit-design/g2-state-data.md|docs/react-kit/state-data.html|React Kit|#38BDF8|0.83|0.96|0.80|re
docs/react/kit-design/g3-performance.md|docs/react-kit/performance.html|React Kit|#38BDF8|0.83|0.96|0.80|re
docs/react/kit-design/g4-quality.md|docs/react-kit/quality.html|React Kit|#38BDF8|0.83|0.96|0.86|re
docs/react/kit-design/g5-ui-patterns.md|docs/react-kit/ui-patterns.html|React Kit|#38BDF8|0.83|0.96|0.80|re
docs/react/kit-design/g5b-animation.md|docs/react-kit/animation.html|React Kit|#38BDF8|0.83|0.96|0.80|re
docs/react/kit-design/g6-build-audit.md|docs/react-kit/build-audit.html|React Kit|#38BDF8|0.83|0.96|0.80|re
docs/react/research-log.md|docs/react-kit/research-log.html|React Kit|#38BDF8|0.83|0.96|-|new
harness/references/feedback-schema.yaml|docs/harness/feedback-system.html|Harness|#D97757|0.90|-|-|re
react-kit/references/project-detection.md|docs/react-kit/project-detection.html|React Kit|#38BDF8|0.83|0.96|0.80|new
tone-kit/references/sources.md|docs/tone-kit/sources.html|Tone Kit|#D946EF|0.96|1.00|-|new'
printf '%s\n' "$FIFTEEN" > "$T/fifteen.txt"
PAGES=$(printf '%s\n' "$FIFTEEN" | cut -d'|' -f2)
N15=$(printf '%s\n' "$FIFTEEN" | grep -c .)
# 범위 목록 — 계약의 `# sprint-scope` 블록을 그대로 읽는다(목록을 두 번 적지 않는다). 끝점 트리에 계약이 없으면 작업 폴더의 계약을 읽는다
SCOPE_SRC=$E/$CF_REL; [ -f "$SCOPE_SRC" ] || SCOPE_SRC=$W/$CF_REL
SCOPE=$(awk '/^```text$/{b=1; next} b && /^```$/{b=0; s=0; next} b && /^# sprint-scope$/{s=1; next} b && s && NF{print}' "$SCOPE_SRC" | LC_ALL=C sort -u)
CAP_RE='^(backend-kit|infra-kit|react-kit|howto-kit|harness|tone-kit)__[a-z0-9-]+-(320|375|1280)-(dark|light)\.png$'

cat > "$T/pg.py" <<'PY'
import sys, re, os, html as H, difflib, subprocess, importlib.util, pathlib
from html.parser import HTMLParser
rd = lambda p: open(p, encoding='utf-8').read()
ex = os.path.exists
KEYS = ('src', 'page', 'label', 'accent', 'wr', 'code', 'fence', 'kind')
def rows(p):
    return [dict(zip(KEYS, l.split('|'))) for l in rd(p).splitlines() if l.strip()]
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
def css_of(h):   # <style> 안과 style="" · style='' 속성, CSS 주석은 뺀다
    c = ' '.join(re.findall(r'(?is)<style[^>]*>(.*?)</style>', h)) + ' ' + ' '.join(re.findall(r'(?is)\sstyle\s*=\s*"([^"]*)"', h)) + ' ' + ' '.join(re.findall(r"(?is)\sstyle\s*=\s*'([^']*)'", h))
    return re.sub(r'(?s)/\*.*?\*/', ' ', c)
URL = re.compile(r'https?://[^\s)<>\]"\'`|]+')
def urls(s):   # 백틱 안(코드 표시 — 담김은 AR-03 이 잰다)과 localhost · 127.0.0.1 은 뺀다
    return {u.rstrip('.,;:') for u in URL.findall(re.sub(r'`[^`\n]*`', ' ', s)) if not re.match(r'https?://(localhost|127\.0\.0\.1)\b', u)}
def measure(s, h):   # 원본 s 와 쪽 h → (낱말 비율, 코드 표시 든 것/전체, 코드 블록 줄 든 것/전체)
    a, b = text1(h), text2(h)
    codes = sorted({c.strip() for c in re.findall(r'`([^`\n]+)`', s) if c.strip()})
    cin = {c for c in codes if re.sub(r'\s+', ' ', c) in a}
    words = {w for w in re.findall(r'[0-9A-Za-z가-힣_.-]{2,}', re.sub(r'`[^`]*`', ' ', s))}
    wr = sum(1 for w in words if w in a) / max(1, len(words))
    L = set(); fence = False
    for l in s.splitlines():
        if re.match(r'^\s*(```|~~~)', l): fence = not fence; continue
        if fence:
            z = re.sub(r'\s+', '', l)
            if len(z) >= 8: L.add(z)
    fin = {z for z in L if z in b}
    return wr, cin, codes, fin, L
cmd = sys.argv[1]
if cmd == 'drift':   # drift <트리> <rows> — 드리프트 도구가 열다섯 원본을 바뀐 파일로 받았을 때 고르는 쪽
    dd = load_dd(sys.argv[2]); S = rows(sys.argv[3])
    dd.changed_files = lambda since: [x['src'] for x in S]
    got = {}
    for e in dd.detect_drift('x'): got.setdefault(e.source, []).append(e)
    ok = new = 0
    for x in S:
        es = got.get(x['src'], [])
        good = len(es) == 1 and es[0].target == x['page'] and es[0].registered and es[0].exists
        ok += good; new += sum(1 for e in es if not (e.registered and e.exists))
        print(f"{'OK ' if good else 'BAD'} {x['src']} -> {[(e.target, int(e.registered), int(e.exists)) for e in es] or 'unmapped'}")
    print(f'fifteen_ok={ok}/{len(S)} new_entries={new}')
elif cmd == 'mapdelta':   # mapdelta <옛 트리> <새 트리> <rows> — 두 트리의 모든 파일에 두 판 매핑을 돌려 달라진 원본만
    b, t = load_dd(sys.argv[2]), load_dd(sys.argv[3]); S = rows(sys.argv[4])
    want = {x['src']: [x['page']] for x in S if x['kind'] == 're'}
    files = set()
    for root in (sys.argv[2], sys.argv[3]):
        for d, ds, fs in os.walk(root):
            ds[:] = [x for x in ds if x not in ('node_modules', '.git')]
            files.update(os.path.relpath(os.path.join(d, f), root) for f in fs)
    delta = [(s, cands(b, s), cands(t, s)) for s in sorted(files) if cands(b, s) != cands(t, s)]
    for s, x, y in delta: print(f'DELTA {s}: {x} -> {y}')
    good = sum(1 for s, x, y in delta if want.get(s) == y); outside = sum(1 for s, x, y in delta if s not in want)
    print(f'delta_n={len(delta)} delta_good={good}/{len(want)} delta_outside={outside} excludes_same={int(b.SOURCE_EXCLUDES == t.SOURCE_EXCLUDES)}')
elif cmd == 'table':   # table <옛 트리> <새 트리> <rows> — docs-site SKILL.md Step 1 표가 열다섯 원본을 덮는지 · 표와 스크립트 어긋남 수
    S = rows(sys.argv[4])
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
    print(f'fifteen_in_table={n}/{len(S)} mismatch={mism(sys.argv[2])}->{mism(sys.argv[3])}')
elif cmd == 'pages':   # pages <새 트리> <rows> — 쪽 틀 · 공통 파일 · 외부 자원(모든 모양) · 색 · 숨김 · 테마
    S = rows(sys.argv[3]); t = sys.argv[2]; agg = dict(exist=0, lines=0, css1=0, ext0=0, accent=0, theme=0, light=0, rm0=0, hide0=0)
    for x in S:
        p = os.path.join(t, x['page'])
        if not ex(p): print(f"ABSENT {x['page']}"); continue
        h = rd(p); agg['exist'] += 1
        n = h.count('\n') + (0 if h.endswith('\n') else 1)
        links = re.findall(r'(?is)<link\b[^>]*>', h); site = [l for l in links if re.search(r'''href\s*=\s*["']?\.\./assets/site\.css["'\s>]''', l)]
        first_style = h.lower().find('<style'); site_pos = h.find(site[0]) if site else -1
        css1 = len(site) == 1 and 0 <= site_pos < first_style
        ext = ([l for l in links if l not in site]
               + re.findall(r'(?is)<script\b[^>]*\bsrc\s*=', h)
               + re.findall(r'(?is)<(?:img|iframe|source|video|audio|embed)\b[^>]*\bsrc\s*=\s*["\']?(?:https?:)?//', h)
               + re.findall(r'@import\b', css_of(h))
               + re.findall(r'''url\(\s*["']?(?:https?:)?//''', h))
        root = re.search(r'(?s):root\s*\{(.*?)\}', h); acc = re.search(r'--accent\s*:\s*(#[0-9A-Fa-f]{6})', root.group(1)) if root else None
        accent = bool(acc) and acc.group(1).upper() == x['accent'].upper()
        c = css_of(h)
        hide = re.findall(r'overflow(?:-x|-y)?\s*:\s*(?:hidden|clip)|text-overflow\s*:\s*ellipsis', c)
        rm = h.count('prefers-reduced-motion')
        theme = 'dk-theme' in h; light = '[data-theme="light"]' in c
        for k, v in (('lines', n >= 400), ('css1', css1), ('ext0', not ext), ('accent', accent), ('theme', theme), ('light', light), ('rm0', rm == 0), ('hide0', not hide)): agg[k] += bool(v)
        print(f"{x['page']} lines={n} site_css={len(site)} before_style={int(css1)} ext={len(ext)} accent={acc.group(1) if acc else None} dk_theme={int(theme)} light_rule={int(light)} rm={rm} hide={len(hide)}")
    print(' '.join(f'{k}={v}/{len(S)}' for k, v in agg.items()))
elif cmd == 'cov':   # cov <옛 트리> <새 트리> <rows> — 원본 담김(문턱) + 다시 쓴 쪽은 옛 판 대비 잃은 것 0
    S = rows(sys.argv[4]); tb, t = sys.argv[2], sys.argv[3]; ok = 0
    for x in S:
        s = rd(os.path.join(t, x['src'])); p = os.path.join(t, x['page']); pb = os.path.join(tb, x['page'])
        old = measure(s, rd(pb)) if ex(pb) else None
        if not ex(p): print(f"ABSENT {x['page']} old={'-' if old is None else f'wr={old[0]:.2f} code={len(old[1])}/{len(old[2])} fence={len(old[3])}/{len(old[4])}'}"); continue
        wr, cin, codes, fin, L = measure(s, rd(p))
        cr = len(cin) / len(codes) if codes else None; fr = len(fin) / len(L) if L else None
        lost_c = len(old[1] - cin) if old else 0; lost_f = len(old[3] - fin) if old else 0
        good = (round(wr, 2) >= float(x['wr'])
                and (x['code'] == '-' or (cr is not None and round(cr, 2) >= float(x['code'])))
                and (x['fence'] == '-' or (fr is not None and round(fr, 2) >= float(x['fence'])))
                and lost_c == 0 and lost_f == 0 and (old is None or wr >= old[0]))
        ok += good
        miss = [c for c in codes if c not in cin][:4]
        o = '-' if old is None else f"{old[0]:.2f}/{len(old[1])}/{len(old[3])}"
        print(f"{'OK ' if good else 'BAD'} {x['page']} wr={wr:.2f}(>={x['wr']}) code={len(cin)}/{len(codes)}(>={x['code']}) fence={len(fin)}/{len(L)}(>={x['fence']}) old={o} lost_code={lost_c} lost_fence={lost_f} {miss}")
    print(f'cov_ok={ok}/{len(S)}')
elif cmd == 'urls':   # urls <새 트리> <rows> — 원본의 http(s) 주소가 쪽의 href 로 모두 옮겨졌는지
    S = rows(sys.argv[3]); t = sys.argv[2]; ok = 0; tot = 0; allsrc = 0
    for x in S:
        p = os.path.join(t, x['page']); want = urls(rd(os.path.join(t, x['src']))); allsrc += len(want)
        if not ex(p): print(f"ABSENT {x['page']} src_urls={len(want)}"); continue
        have = {H.unescape(u) for u in re.findall(r'''href\s*=\s*["'](https?://[^"']+)["']''', rd(p))}
        miss = sorted(want - have); ok += not miss; tot += len(want)
        print(f"{'OK ' if not miss else 'BAD'} {x['page']} src_urls={len(want)} missing={len(miss)} {miss[:3]}")
    print(f'url_ok={ok}/{len(S)} src_urls_total={allsrc} checked_urls={tot}')
elif cmd == 'index':   # index <옛 트리> <새 트리> <rows> — 킷 목차 등록 · id 겹침 · 아이콘 · 바뀐 줄
    S = rows(sys.argv[4]); B = rd(os.path.join(sys.argv[2], 'docs/index.html')); N = rd(os.path.join(sys.argv[3], 'docs/index.html'))
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
    en, ic = entries(N), icons(N)
    dup = lambda E: sum(1 for i in {e[0] for e in E} if [e[0] for e in E].count(i) > 1)
    reg = icon = 0
    for x in S:
        f = x['page'][len('docs/'):]; m = [e for e in en if e[1] == f]
        good = len(m) == 1 and (m[0][2] or '').startswith(x['label']); reg += good; icon += bool(m) and m[0][0] in ic
        print(f"{'OK ' if good else 'BAD'} {f} entries={len(m)} id={m[0][0] if m else None} label={m[0][2] if m else None} icon={int(bool(m) and m[0][0] in ic)}")
    ch = [z for z in difflib.unified_diff(B.splitlines(), N.splitlines(), lineterm='', n=0) if z[:1] in '+-' and not z.startswith(('+++', '---'))]
    print(f"reg_ok={reg}/{len(S)} icon_ok={icon}/{len(S)} dup_ids={dup(entries(B))}->{dup(en)} added={sum(z[0] == '+' for z in ch)} deleted={sum(z[0] == '-' for z in ch)}")
elif cmd == 'ids':   # ids <트리> <rows> — nav 도구에 넘길 id=파일 짝
    S = rows(sys.argv[3]); N = rd(os.path.join(sys.argv[2], 'docs/index.html'))
    for x in S:
        f = x['page'][len('docs/'):]; m = re.search(r"\{\s*id:\s*'([^']+)'[^\n]*?file:\s*'" + re.escape(f) + "'", N)
        print(f"{m.group(1) if m else 'none'}={f}")
elif cmd == 'yaml':   # yaml <새 트리> <rows> — YAML 원본의 키가 쪽의 표에 모두 있고, 예시가 같은 값으로 옮겨졌는지
    import yaml
    S = [x for x in rows(sys.argv[3]) if x['src'].endswith('.yaml')]; t = sys.argv[2]
    for x in S:
        s = rd(os.path.join(t, x['src'])); d = yaml.safe_load(s)
        keys = set(re.findall(r'(?m)^#(?:[ \t]*#)?[ \t]+([a-z][a-z0-9_]*):', s))
        def walk(v):
            if isinstance(v, dict):
                for k, w in v.items(): yield k; yield from walk(w)
            elif isinstance(v, list):
                for w in v: yield from walk(w)
        keys |= set(walk(d)); keys.discard('example')
        p = os.path.join(t, x['page'])
        if not ex(p): print(f"ABSENT {x['page']} keys={len(keys)}"); continue
        h = rd(p)
        tables = ' '.join(text1(z) for z in re.findall(r'(?is)<table\b.*?</table>', h))
        miss = sorted(k for k in keys if not re.search(r'(?<![A-Za-z0-9_])' + re.escape(k) + r'(?![A-Za-z0-9_])', tables))
        same = 0
        for pre in re.findall(r'(?is)<pre\b[^>]*>(.*?)</pre>', h):
            try: v = yaml.safe_load(H.unescape(re.sub(r'<[^>]+>', '', pre)))
            except Exception: continue
            if v == d['example'] or v == {'example': d['example']}: same += 1
        print(f"{x['page']} keys={len(keys)} in_table={len(keys) - len(miss)} missing={miss[:6]} example_same={same}")
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
elif cmd == 'commits':   # commits <W> <BASE> <R> — 커밋마다 묶음(맨 위 폴더, docs 아래는 docs/<폴더>) 둘 이상 · .harness 섞임
    w, b, r = sys.argv[2], sys.argv[3], sys.argv[4]
    revs = subprocess.run(['git', '-C', w, 'rev-list', '--no-merges', f'{b}..{r}'], capture_output=True, text=True).stdout.split()
    impl = mu = mx = 0
    for c in revs:
        fs = [l for l in subprocess.run(['git', '-C', w, 'show', '--name-only', '--format=', c], capture_output=True, text=True).stdout.splitlines() if l]
        h = [f for f in fs if f.startswith('.harness/')]; o = [f for f in fs if not f.startswith('.harness/')]
        if o: impl += 1
        units = {('/'.join(f.split('/')[:2]) if f.startswith('docs/') else f.split('/')[0]) for f in o if not (f.startswith('docs/') and f.count('/') == 1)}
        mu += len(units) > 1; mx += bool(h) and bool(o)
    print(f'commits={len(revs)} impl_commits={impl} multi_unit={mu} mixed={mx}')
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
  if (mode === 'of') {   // of <트리> <쪽...> — 320 · 375 · 1280 폭 × 밝은 · 어두운 테마의 문서 가로 넘침(px) · 잘린 글 요소 수
    let ok = 0, cells = 0, zero = 0;
    for (const f of rest) {
      const file = path.join(tree, f); if (!fs.existsSync(file)) { console.log(`ABSENT ${f}`); continue; }
      let pageOk = true; const bg = {}; const row = [];
      for (const theme of ['dark', 'light']) {
        const ctx = await b.newContext({ viewport: { width: 1280, height: 900 }, colorScheme: theme, reducedMotion: 'reduce' });
        await ctx.addInitScript(t => { try { localStorage.setItem('dk-theme', t); } catch (e) {} }, theme);
        const p = await ctx.newPage(); await p.goto('file://' + path.resolve(file));
        await p.evaluate(t => { document.documentElement.dataset.theme = t; }, theme); await p.waitForTimeout(400);
        bg[theme] = await p.evaluate(() => getComputedStyle(document.body).backgroundColor);
        for (const w of [320, 375, 1280]) {
          await p.setViewportSize({ width: w, height: 900 }); await p.waitForTimeout(150);
          const r = await p.evaluate(() => {
            const of = Math.max(document.documentElement.scrollWidth - document.documentElement.clientWidth, document.body.scrollWidth - document.body.clientWidth);
            // 잘린 글: 글을 직접 가진 요소가 제 상자보다 넓은데 스크롤할 수 없는 경우(overflow 가 visible 이 아니고 auto · scroll 도 아님)
            let clip = 0;
            for (const e of document.body.querySelectorAll('*')) {
              if (![...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim())) continue;
              const cs = getComputedStyle(e); const ox = cs.overflowX;
              if (ox === 'visible' || ox === 'auto' || ox === 'scroll') continue;
              if (e.scrollWidth - e.clientWidth > 1) clip++;
            }
            return { of, clip };
          });
          cells++; if (r.of <= 0 && r.clip === 0) zero++; else pageOk = false; row.push(`${theme[0]}${w}=${r.of}/${r.clip}`);
        }
        await ctx.close();
      }
      const differ = bg.dark !== bg.light;
      if (!differ) pageOk = false; if (pageOk) ok++;
      console.log(`${pageOk ? 'OK ' : 'BAD'} ${f} ${row.join(' ')} theme_differs=${differ ? 1 : 0}`);
    }
    console.log(`of_ok=${ok}/${rest.length} cells_zero=${zero}/${cells}`);
  } else if (mode === 'nav') {   // nav <트리> <id=file...> — index.html 목차를 눌러 쪽이 뜨는지
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
    SK-01) echo "skill_changed=$(git -C "$W" diff --name-only "$BASE" "$R" -- .claude/skills/docs-site/SKILL.md | grep -c .)"; python3 "$T/pg.py" table "$EB" "$E" "$T/fifteen.txt" ;;
    SC-01) python3 "$T/pg.py" drift "$E" "$T/fifteen.txt" ;;
    SC-02) python3 "$T/pg.py" mapdelta "$EB" "$E" "$T/fifteen.txt" ;;
    SC-03) (cd "$E" && python3 scripts/detect-docs-drift.py --check-table > "$T/ct.txt" 2>&1; echo "check_table_rc=$? $(tail -1 "$T/ct.txt")") ;;
    ER-01) (cd "$T" && node pw.js of "$E" $PAGES) ;;
    ER-02) EX=$(for p in $PAGES; do [ -f "$E/$p" ] && echo "$p"; done); echo "absent=$((N15 - $(printf '%s\n' $EX | grep -c .)))"
           [ -n "$EX" ] || { echo "a11y_rc=none ok_both=0/$N15 checked=0"; return 0; }
           (cd "$E" && node scripts/check-docs-a11y.js $EX > "$T/a11y.txt" 2>&1; rc=$?; cat "$T/a11y.txt"
            echo "a11y_rc=$rc ok_both=$(grep -cE '^OK .* theme=both$' "$T/a11y.txt")/$N15 checked=$(grep -cE '^(OK|FAIL) ' "$T/a11y.txt")") ;;
    ER-03) PAIRS=$(python3 "$T/pg.py" ids "$E" "$T/fifteen.txt"); (cd "$T" && node pw.js nav "$E" $PAIRS) ;;
    ER-04) (cd "$E" && python3 scripts/check-contrast-claims.py > "$T/cc.txt" 2>&1; echo "contrast_rc=$? $(grep -m1 '어긋난 것' "$T/cc.txt")")
           (cd "$E" && python3 scripts/check-api-kit-docs.py > "$T/ak.txt" 2>&1; echo "apikit_rc=$? $(grep -E '[0-9]+/[0-9]+ PASS' "$T/ak.txt" | tail -1)") ;;
    AR-01) echo "added=$(git -C "$W" diff --name-status "$BASE" "$R" -- $PAGES | awk '$1 == "A"' | wc -l | tr -d ' ') modified=$(git -C "$W" diff --name-status "$BASE" "$R" -- $PAGES | awk '$1 == "M"' | wc -l | tr -d ' ')"
           python3 "$T/pg.py" pages "$E" "$T/fifteen.txt" ;;
    AR-02) python3 "$T/pg.py" index "$EB" "$E" "$T/fifteen.txt"
           (cd "$E" && python3 scripts/check-docs-links.py > "$T/links.txt" 2>&1; echo "links_rc=$? $(grep -m1 '내비 등록' "$T/links.txt")") ;;
    AR-03) python3 "$T/pg.py" cov "$EB" "$E" "$T/fifteen.txt" ;;
    AR-04) python3 "$T/pg.py" urls "$E" "$T/fifteen.txt" ;;
    AR-05) python3 "$T/pg.py" pages "$E" "$T/fifteen.txt" | tail -1 ;;
    AR-06) CH=$(git -C "$W" diff --name-status "$BASE" "$R" -- . ':(exclude).harness')
           GOT=$(printf '%s\n' "$CH" | awk 'NF{print $NF}' | LC_ALL=C sort)
           echo "scope_n=$(printf '%s\n' "$SCOPE" | grep -c .) extra=$(comm -13 <(echo "$SCOPE") <(echo "$GOT") | grep -c .) missing=$(comm -23 <(echo "$SCOPE") <(echo "$GOT") | grep -c .) png=$(git -C "$W" diff --name-only "$BASE" "$R" | grep -ci '\.png$') status=$(printf '%s\n' "$CH" | awk 'NF{print $1}' | LC_ALL=C sort | uniq -c | awk '{printf "%s%s ", $2, $1}')"
           comm -3 <(echo "$SCOPE") <(echo "$GOT") | head -5
           sb=0; for c in $(cd "$E" && find .harness -maxdepth 1 -name 'sprint-contract*.md' | LC_ALL=C sort); do
             rec=$(awk '/^---$/{f++; next} f==1 && /^conditions_digest:/{sub(/^conditions_digest:[ ]*sha256:/,""); print; exit}' "$E/$c")
             [ -n "$rec" ] || continue
             act=$(grep -E '^- \[[ x]\] [A-Z]{2,}-[0-9]{2}' "$E/$c" | sed -E 's/^- \[[ x]\]/- [ ]/' | shasum -a 256 | cut -c1-16)
             [ "$rec" = "$act" ] || { sb=$((sb+1)); echo "SEAL_BROKEN $c"; }
           done; echo "seal_broken=$sb" ;;
    AR-07) python3 "$T/pg.py" commits "$W" "$BASE" "$R" ;;
    AR-08) echo "committed=$(git -C "$W" cat-file -e "$R:$NOTES" 2>/dev/null && echo 1 || echo 0)"
           python3 "$T/pg.py" tokens "$E/$NOTES" 'DC-9' 'dca-notes' 'Gotcha 7' 'RE-02' 'tone-guide' 'feedback-schema' 'design-brief' 'kit-design' 'research-log' 'sources.md' 'check-table' 'DC-12' ;;
    AR-09) CAP=$(sed -n 's/^캡처 폴더: `\(.*\)`$/\1/p' "$E/$NOTES" 2>/dev/null | head -1); echo "cap_dir=${CAP:-absent}"
           [ -n "$CAP" ] && [ -d "$CAP" ] || { echo "cap_ok=0"; return 0; }
           need=0; have=0; for p in $PAGES; do
             base=$(echo "$p" | sed -E 's#^docs/##; s#\.html$##; s#/#__#')
             for w in 320 375 1280; do for t in dark light; do need=$((need+1)); [ -s "$CAP/$base-$w-$t.png" ] && have=$((have+1)); done; done
           done
           echo "cap_need=$need cap_have=$have cap_badname=$(find "$CAP" -maxdepth 1 -name '*.png' -exec basename {} \; | grep -cvE "$CAP_RE")" ;;
    AR-10) python3 "$T/pg.py" yaml "$E" "$T/fifteen.txt" ;;
    RE-02) python3 "$T/pg.py" pages "$E" "$T/fifteen.txt" | tail -1
           echo "new_scripts=$(git -C "$W" diff --name-status "$BASE" "$R" -- . ':(exclude).harness' | awk '$1 == "A" && $2 ~ /\.(js|py|sh|css)$/' | wc -l | tr -d ' ')" ;;
    AP-03) printf 'notes=%s->%s\n' "$(python3 "$T/pg.py" bare "$EB/$NOTES")" "$(python3 "$T/pg.py" bare "$E/$NOTES")" ;;
    DG-01|DG-03) echo "release_paths=$(git -C "$W" diff --name-only "$BASE" "$R" -- scripts/release.sh | wc -l | tr -d ' ')" ;;
    DG-02) tw=0; for p in $PAGES docs/index.html; do [ -f "$E/$p" ] || { echo "ABSENT $p"; continue; }
             a=$(python3 "$T/pg.py" tags "$E/$p"); bb=0; [ -f "$EB/$p" ] && bb=$(python3 "$T/pg.py" tags "$EB/$p"); [ "$a" -gt "$bb" ] && { tw=$((tw+1)); echo "TAG_WORSE $p $bb->$a"; }; done
           (cd "$T" && npm i --silent --no-save markdownlint-cli2@0.23.2 >/dev/null 2>&1) || echo "md=ENV_FAIL"
           printf '{"config":{"MD013":false}}\n' > "$T/.markdownlint-cli2.jsonc"
           mdc() { [ -f "$1" ] || { echo absent; return; }; (cd "$T" && node_modules/.bin/markdownlint-cli2 "$1" 2>&1 | grep -cE ':[0-9]+(:[0-9]+)? (error|warning)? ?MD[0-9]+' ); }
           echo "tag_worse=$tw md_notes=$(mdc "$E/$NOTES") py_compile=$(python3 -m py_compile "$E/scripts/detect-docs-drift.py" 2>&1 | wc -l | tr -d ' ') cli_rc=$(cd "$E" && python3 scripts/detect-docs-drift.py --since "$BASE" >/dev/null 2>&1; echo $?)" ;;
    DG-04) m ER-02 | tail -1; m ER-03 | tail -2 ;;
    DG-05) [ "$(git -C "$W" rev-parse HEAD)" = "$TIP" ] && [ -z "$(git -C "$W" status --porcelain --untracked-files=no)" ] || { echo "W_NOT_TIP"; return 0; }
           echo "tool_same=$([ "$(git hash-object "$CI_LOCAL" 2>/dev/null)" = "$TOOL_BLOB" ] && echo 1 || echo 0)"
           (cd "$W" && TMPDIR="$T" bash "$CI_LOCAL" "$W" > "$T/ci.txt" 2>&1); SUM=$T/ci-local/summary.txt
           [ -s "$SUM" ] || { echo "ci_summary=absent"; return 0; }
           echo "rc0=$(grep -c 'rc=0' "$SUM") other=[$(grep -v 'rc=0' "$SUM" | sed -E 's/[[:space:]]+/ /g' | tr '\n' ';')]"
           # CI 에 있는데 도구에 없는 검사 단계 셋을 따로 돌린다(설치 단계 · 여러 줄 run 은 뺀다)
           (cd "$W" && python3 scripts/detect-docs-drift.py --check-table >/dev/null 2>&1; a=$?; python3 scripts/check-cause-table-copies.py >/dev/null 2>&1; b=$?; bash harness/evals/measure/measure-helpers-test.sh >/dev/null 2>&1; c=$?; echo "extra_steps check_table=$a cause_copies=$b measure_helpers=$c")
           echo "outside=[$(sed -n '/이 스크립트 밖의 것:/,/^[0-9]*$/p' "$T/ci.txt" | sed '1d;$d' | sed -E 's/^[[:space:]]+run: //' | LC_ALL=C sort -u | tr '\n' ';')]" ;;
    *) echo "UNKNOWN $1" ;;
  esac
}
# === 측정 도우미 끝 ===
```
