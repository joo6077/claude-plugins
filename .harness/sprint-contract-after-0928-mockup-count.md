---
feature: "시안 개수 규칙 — 위 제한 없이 최소 5 개부터"
slug: after-0928-mockup-count
created: "2026-09-28 11:26"
complexity: "복잡"
conditions: 20
status: done
owner_session: bda55d45-296c-491f-89ba-b52042d58e72
conditions_digest: sha256:c70a4f0bd6616598
measurement_digest: sha256:15e178ac7f1ba94d
locked_at: "2026-09-28 11:34"
---

## 배경

- 남은 일 목록(`/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0928/.harness/.meta/after-kaizen-0928/remaining.md`)의 A4 · C3(KD-4 design:P2 규칙 방향)을 묶음 dz 로 처리한다.
- 사용자 결정: 같은 폴더 `decisions.md` 「사용자 결정 (2026-09-28T02:09:55.834Z)」 — 원문 「1. 개수는 제한하지말고 필요한만큼? 뭐 최소 5개로 하던가」. 결정 표: 「시안 개수 위 제한 없음, 최소 5 개부터 필요한 만큼」. 사용자 위임: 2026-09-27T01:22:01.089Z 「자동으로 다 진행해 나한테 묻지 말고 …」 · 2026-09-28 「약점과 일부만 한 거 다처리하지??」(세션 bda55d45-296c-491f-89ba-b52042d58e72).
- 지금 규칙은 「사용자 지정 N 은 정확히 N · 미지정 3 · 자체 판단으로 늘리지 않음 · 승인 시 최대 5 · 6 개 이상은 배치를 나눠 제안」 이다. 숫자의 기준 원본은 `harness/docs/guides/skill-design-guide.md` §5.6 Variant Budget 조항 1(「기본 산출물 상한 3 개. 4 개 이상은 사용자 승인」)이고, design-kit 은 `references/visual-change-protocol.md` §5 「개수 계약」 두 조로 그것을 받는다.
- 새 규칙(이 계약의 한 문장): **시안(화면 · 컨셉을 눈으로 비교하는 시각 변주안) 개수는 사용자가 말하면 정확히 그 수, 말하지 않으면 최소 5 개부터 필요한 만큼 낸다 — 위 제한은 없다.** 사용자가 개수를 말한 경우는 바꾸지 않는다(결정은 미지정일 때의 기본과 위 제한만 다룬다).
- §5.6 은 시안 말고도 후보안 · 네이밍 후보 같은 탐색형 산출물 전부에 걸린다. 사용자 결정은 시안 개수만 다루므로 §5.6 조항 1 을 둘로 나눈다 — 시안은 새 규칙, 그 밖의 탐색형 산출물은 지금대로 기본 상한 3 · 4 개 이상 승인.
- 틀 `design-kit/templates/mockup.html` 은 시안 칸이 A~E 다섯 개로 박혀 있고, 스크립트 다섯 자리(`:1429` · `:1606-1610` · `:1619` · `:1639` · `:1671`)가 `'a'~'e'` 를 글자로 들고 있다. 위 제한을 없애면 여섯째 시안부터 틀이 받지 못하므로, 시안 목록을 `MOCKUP_CONFIG.variants` 한 곳에서 읽게 고치고 칸을 늘리는 방법을 SKILL Step 2-b 에 적는다.

## GAP 분석

복잡도 네 축:

| 축 | 값 |
| --- | --- |
| 레이어 수 | 규칙 기준 원본(harness 가이드) · 스킬 본문 · 참조 규약 · 틀 스크립트 · 평가 사례 · 시험 · 문서 쪽 — 넷 이상 |
| 공개 계약 변경 | 예 — design-mockup · design-concept 이 내는 시안 수가 바뀐다 |
| 소비면 | 예 — README 자동 표, 문서 쪽 다섯, 평가 사례 id 19, 틀 |
| 회귀 위험 | 예 — 틀 스크립트(탭 · 투표 · 메모 저장), 시안이 아닌 숫자(기존 화면 2 개 · 최대 3 회 · 사용자 지정 N) |

넷 다 「예」 라 복잡이다. 소비면은 SK-02 · AR-01 · AR-02 · SC-01 이 따로 잰다.

설정 대조표 (`.harness/project.yaml` 그대로):

| 키 | 읽은 값 | 계약에 쓴 값 |
| --- | --- | --- |
| `commands.analyze` | `bash -n scripts/release.sh` | DG-01 N/A 사유에 그대로 |
| `commands.test` | `bash scripts/release.sh 2>&1 \|\| true` | DG-03 N/A 사유에 그대로 |
| `diagnostics.ide_exclude` | `[]` | DG-02 에 `[]` |
| `contract_categories` | Skill/SK · Script/SC · Error/ER · Architecture/AR | 네 절 |
| `anti_patterns` | AP-01 · AP-02 · AP-03 · AP-04 | AP-03 · AP-04 (AP-01 은 판 번호 하드코딩 규칙인데 판 번호를 바꾸는 파일이 없다, AP-02 는 push 를 하지 않는다) |

grep 으로 찾은 개수 자리 전부와 판정 (찾은 명령: `grep -rnE` 로 `시안|mockup|목업|variant|대안|옵션` 줄 가운데 `[0-9]+ ?(개|종|안|가지)|최대|최소|상한|미지정` 이 든 줄, 그리고 `미지정|승인 상한|배치를 나눠|개수 계약|Variant Budget|§5.6` 을 레포 전체에서. `.harness/` · `.claude/` · `node_modules/` 는 기록이라 뺐다):

| 자리 (`파일:줄`, 봉인 전 판 c25d16e) | 적힌 것 | 시안 개수인가 | 처리 |
| --- | --- | --- | --- |
| `design-kit/skills/design-mockup/SKILL.md:4` | description 「미지정 3 · 사용자 지정 N · 승인 상한 5」 | 예 | 계약에 넣음 — S01 · SK-01 |
| `design-kit/skills/design-mockup/SKILL.md:32` | Gotcha 16 「미지정이면 3 … 승인 시 최대 5 · 개수 상한」 | 예 | 계약에 넣음 — S02 · SK-01 |
| `design-kit/skills/design-mockup/SKILL.md:80` · `:84-86` | Step 2-a 「정본 규칙(상한·…)」 · 표 「미지정 3 · 자체 판단으로 늘리기 금지 · 최대 5 · 배치를 나눠」 | 예 | 계약에 넣음 — S03 · SK-01 |
| `design-kit/skills/design-mockup/SKILL.md:108` | 전략 후보 풀 「다섯 개를 전부 내라는 목록이 아니다」 | 예 (최소 5 와 부딪힌다) | 계약에 넣음 — S04 · SK-01 |
| `design-kit/skills/design-mockup/SKILL.md:96-116` | Step 2-b 에 여섯째 시안부터 틀 칸을 늘리는 방법 없음 | 예 (위 제한 없음의 결과) | 계약에 넣음 — S04 · SK-01 |
| `design-kit/references/visual-change-protocol.md:234-236` · `:253-258` | 「개수 상한 … 정본은 이 절이 아니다」 · 개수 계약 ② 「§5.6 의 기본값(3) · 최대 5 · 배치를 나눠」 | 예 | 계약에 넣음 — S05 · SK-02 |
| `design-kit/skills/design-concept/SKILL.md:53` | Gotcha 6 「개수 상한과 부대 산출물 금지의 정본은 §5.6」 | 예 (컨셉 안도 §5 적용 대상) | 계약에 넣음 — S06 · SK-02 |
| `design-kit/evals/evals.json` id 19 (`:388` · `:391`) | 「시안 3개(개수 미지정)」 · 「정확히 3개」 | 예 | 계약에 넣음 — S07 · SK-02 |
| `design-kit/README.md:16` | 자동 표의 description 사본 | 예 | 계약에 넣음 — S08 · SK-02 (`sync-docs.py` 로 갱신) |
| `design-kit/templates/mockup.html:976-1003` · `:1111-1124` · `:1168-1192` · `:1199-` · `:1262-1296` · `:1429` · `:1606-1610` · `:1619` · `:1639` · `:1671` | 시안 칸 A~E 다섯 · 스크립트의 `'a'~'e'` 고정 목록 | 예 (여섯째부터 못 받는다) | 계약에 넣음 — SK-04 · SC-01 · SC-02 |
| `harness/docs/guides/skill-design-guide.md:778` · `:786-790` · `:797` · `:800` | §5.6 조항 1 「기본 산출물 상한 3 개」 · 예시 표 3 행 · Good 줄 「3 행 … 3 파일」 · 트레이드오프 「상한 3 개는」 | 예 | 계약에 넣음 — S10 · SK-03 |
| `harness/docs/guides/skill-design-guide.md:1232` | 요약 표 「탐색형 산출물은 상한 3」 | 예 | 계약에 넣음 — S11 · SK-03 |
| `docs/design-kit/design-mockup.html:378-379` · `:444-445` · `:515-522` · `:552-580` · `:759` | 쪽 사본(머리 알약 · 기준 표 · Step 2-a · Step 2-b · 후보 풀 · Gotcha 16) | 예 | 계약에 넣음 — S12~S16 · AR-01 |
| `docs/design-kit/design-reference.html:253` | 「미지정 3 · 사용자 지정 N · 승인 상한 5」 | 예 | 계약에 넣음 — S17 · AR-01 |
| `docs/design-kit/visual-change-protocol.html:702-704` · `:722-723` | 개수 상한 경고 · 개수 계약 ② 카드 | 예 | 계약에 넣음 — S18 · AR-01 |
| `docs/design-kit/design-template.html:698` | 「A/B/C/D/E 최대 5가지 컨셉」 | 예 | 계약에 넣음 — S19 · AR-01 |
| `docs/harness/skill-design-guide.html:1111` · `:1127-1129` · `:1139-1140` · `:1585` | §5.6 쪽 사본 · 요약 표 | 예 | 계약에 넣음 — S20 · S21 · AR-02 |
| `design-kit/skills/design-mockup/references/mockup-guidelines.md:7` | 「개수는 `SKILL.md` Step 2-a 를 따른다」 | 예 | 이미 됨 — 숫자를 적지 않고 Step 2-a 를 가리킨다(kaizen-0924 SK-09). ER-01 이 그 줄을 그대로 지킨다 |
| `harness/docs/guides/skill-design-guide.md` §8.9 (`:1028-1043`) | 「2 개 이상」(편집 전에 읽을 기존 화면) · 「최대 3 회」(스스로 고치기) | 아니오 | 바꾸지 않음 — ER-01 이 두 줄을 지킨다 |
| `design-kit/references/visual-change-protocol.md:31` · `:159` · `flutter-toolkit/references/visual-evidence-protocol.md:58` · `:97` · `react-kit/references/render-evidence-protocol.md:63` · `:110` | 화면 규약 세 벌의 같은 두 숫자 | 아니오 | 바꾸지 않음 — ER-01. flutter · react 화면 규약 사본에는 시안 개수가 0 곳이다 |
| `design-kit/references/visual-change-protocol.md:255-256` | 「사용자가 개수를 말하면 정확히 그 수」 · 「"3 개" 요청에 5 개를 내면」 | 아니오 (사용자 지정 규칙, 그대로) | 바꾸지 않음 — ER-01 |
| `design-kit/references/visual-change-protocol.md:304` | 구별성 판정 스크립트 「variant 2 개 이상 필요」 | 아니오 (쌍 비교의 입력 최소) | 바꾸지 않음 — ER-01 |
| `design-kit/skills/design-mockup/references/mockup-guidelines.md:16` · `design-kit/skills/design-concept/templates/concept.md:64` | 「최소 2개 축」 | 아니오 (축 수) | 바꾸지 않음 — ER-01 |
| `design-kit/skills/design-concept/templates/concept.md:52` | 「여러 컨셉 안(A/B/C)」 | 아니오 (이름표 예시, 개수 규칙이 아니다) | 바꾸지 않음 — ER-01 |
| `design-kit/evals/evals.json` id 14 · 28 · 29 | 「컨셉 2개 안으로 뽑아줘」(사용자 지정) · 기존 화면 2 개 · 최대 3 회 | 아니오 | 바꾸지 않음 — ER-01 |
| `harness/docs/guides/skill-design-guide.md:795-796` | Bad 「"목업 몇 개" → 9~40 타일 + 토큰 파일 …」 · 「variant 6 개 … 4 축 전부 같은 값」 | 아니오 (부대 산출물 · 구별성 실패 사례 기록) | 바꾸지 않음 — ER-01 |
| `design-kit/skills/design-mockup/SKILL.md:148` · `docs/design-kit/design-mockup.html:452` · `:636` | 「스스로 고치기 최대 3 회 · 횟수 상한」 | 아니오 | 바꾸지 않음 |
| `flutter-toolkit/skills/flutter-test/SKILL.md:126` · `react-kit/agents/widget-inspector-react.md:70` · `:156` · `:205` · `react-kit/evals/evals.json:47` · `flutter-toolkit/agents/widget-inspector.md:106` | 컴포넌트 variant 수 · 파라미터 수 | 아니오 (코드 컴포넌트) | 바꾸지 않음 |
| `design-kit/skills/design-reference/references/crawl-sources.md:11` · `design-kit/references/visual-styles.md:3` · `docs/design-kit/apple-hig.html` · `navigation.html` | 레퍼런스 수집 수 · 스타일 35 종 · 탭 바 최대 5 개 | 아니오 | 바꾸지 않음 |
| `docs/kaizen/changelog.md:201` · `:228` · `docs/design/research-log.md:440` · `:449` · `:521` · `docs/superpowers/plans/*` · `docs/superpowers/specs/*` · `.claude/kaizen-input/*` | 그때 적은 기록 | 기록 | 바꾸지 않음 — 지난 사실이다 |

미리 연 파일 (읽은 자리 · 찾은 것 · 조건): 위 표의 `파일:줄` 이 이 세션에서 실제로 연 자리다. 틀은 `:300-330`(탭 줄이 가로로 스크롤돼 여섯째 탭이 쪽을 넓히지 않는다) · `:720-815`(투표 · 메모 격자 `repeat(5, 1fr)`, 좁은 폭에서 2 열) · `:1440-1470`(`selectTab` 은 id 로 찾으므로 f 도 받는다) 도 읽었다.

## 리서치 소스

- 사용자 결정 원문: `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0928/.harness/.meta/after-kaizen-0928/decisions.md:8-17`
- 규칙이 그렇게 된 내력: `.harness/sprint-contract-kaizen-phase6-variant-decision-gates.md`(고정 「시안 5개」 → 개수 계약), `.harness/sprint-contract-kaizen-0924-p06-design-kit.md` SK-09(방향은 두고 어긋난 두 자리만 맞춤), `.harness/.meta/kaizen-0924/phase6-notes.md:68`(한 프로젝트 기억 「여러 개 다 만들어 나란히」 · 「시안 추가는 승인 대기 말고 바로 구현」 이 옛 규칙과 반대라 사용자에게 넘김)
- 바깥 근거는 쓰지 않는다 — 개수는 사용자가 정한 레포 결정이다(§8.9 「한계」 문단과 같은 성격)
- 문서 쪽 규칙: `.claude/skills/docs-site/SKILL.md`(공통 CSS 링크 하나 · 320 · 375 · 1280 넘침 0)

## 범위 경계

```text
# sprint-scope
design-kit/skills/design-mockup/SKILL.md
design-kit/skills/design-concept/SKILL.md
design-kit/references/visual-change-protocol.md
design-kit/evals/evals.json
design-kit/evals/visuals.spec.js
design-kit/templates/mockup.html
design-kit/README.md
harness/docs/guides/skill-design-guide.md
docs/design-kit/design-mockup.html
docs/design-kit/design-reference.html
docs/design-kit/visual-change-protocol.html
docs/design-kit/design-template.html
docs/harness/skill-design-guide.html
```

- 새 규칙 문장에 반드시 드는 글자: `최소 5` 와 `위 제한 없`(「위 제한 없이」 · 「위 제한 없음」 · 「위 제한 없다」 모두 된다). 옛 규칙 글자는 `sites.py` 의 `OLD` 정규식이 정의다 — `미지정 3` · `최대 5` · `상한 5` · `배치를 나눠/나누어` · `그 이상 늘리지 않` · `늘리지 않음` · `§5.6 의 기본값(3)` · `시안 3 개` · `정확히 3 개` · `다섯 개 전부`, design-kit 쪽 자리는 여기에 `개수 상한` · `정본 규칙(상한` 을 더한다. 태그 · `**` · 백틱을 걷어 낸 뒤 잰다.
- 여섯째 시안부터 늘리는 방법(Step 2-b 와 쪽 사본)에는 `칸 묶음` 이라는 말로 늘릴 자리를 적는다 — 탭 · 패널 · 비교 선택 두 곳 · 투표 카드 · 메모 칸 · `MOCKUP_CONFIG` · 두 언어 `tab` 글자. 전략 후보 풀 문장에는 합의한 수가 풀보다 많으면 `풀 밖` 전략을 더 만든다는 뜻을 적는다.
- 하지 않는 것: 사용자가 개수를 말한 경우의 규칙(정확히 그 수) — 결정 밖이다. §5.6 의 축 개수(primary 1 + secondary 1) · 부대 산출물 금지 · 구별성 판정식 — 결정 밖이다. §5.6 제목 · §2 유형 11 문장 · `:766` 이름 구분 표의 「개수 상한」 은 시안 밖 탐색형 산출물에 여전히 맞는 말이라 그대로 둔다.
- §5.6 Variant Matrix 예시(`mock/a1.html`~, 버블 채팅 화면 시안)는 시안 예시라 5 행으로 늘린다. 그러면 같은 절의 「상한 3」 과 「5 행」 이 부딪혀 보이므로, 표 바로 위에 「이 예시는 시안 규칙(최소 5, 위 제한 없음)이고 시안이 아닌 탐색형 산출물은 여전히 상한 3」 이라는 이름표 줄을 두고 Good 줄에도 「시안」 을 적는다(교차 진단 지적 반영 — SK-03 · AR-02 의 `label` · `good5` 가 잰다).
- 하지 않는 것: 틀의 기본 칸을 다섯보다 늘리기 — 다섯은 새 최소와 같다. 투표 · 메모 격자 `repeat(5, 1fr)` 도 그대로 둔다(여섯째는 다음 줄로 내려간다).
- 하지 않는 것: 판 번호 올리기 · 릴리스 · changelog — 묶음을 합친 뒤 따로 한다.
- 커밋: 맨 위 폴더 하나에 커밋 하나 이상, 한 커밋에 맨 위 폴더 하나(design-kit · harness · docs). `git add <경로>` 뒤 `git commit -o <경로>`.
- 커버리지 해소: SK-01 · SK-02 · SK-03 · AR-01 · AR-02 — 자리마다 파일과 구간은 `sites.py` 의 `SITES` 표 한 곳에만 적고(ID S01~S08 · S10~S21, S09 는 틀이라 SK-04 가 따로 잰다), 조건은 그 스크립트의 `SITE <ID>` 줄을 읽는다. 목록을 두 번 적지 않는다.
- 커버리지 해소: ER-01 — 지킬 줄 21 개는 `keep-lines.txt` 한 곳에만 적는다.
- 커버리지 해소: AR-03 — 범위 목록은 위 `# sprint-scope` 블록 한 곳에만 적는다.
- 커버리지 해소: SC-01 — `design-kit/evals/visuals.spec.js` 는 측정의 `npx playwright test` 인자로, `design-kit/templates/mockup.html` 은 측정의 「스펙을 읽어 각 확인이 있는지 본다」 가 스펙 안에서 찾는 글자로 쓰인다. `test.describe` 는 파일이 아니라 스펙에서 찾는 글자다(검출기의 `UNCOVERED SC-01` 1 건, 봉인 전 실측).
- 오라클 해소: SK-01 — 산출물이 모델이 읽는 규칙 문장 자체라 실행할 동작이 없다. `sites.py` 는 문장 존재만이 아니라 옛 규칙 글자(`old`)가 0 인지도 재므로, 새 문장을 적고 옛 숫자를 남기면 떨어진다(공통 정의의 S08 알려진 답). 동작이 있는 틀은 SC-01 · SC-02 가 실제로 띄워 잰다.
- 오라클 해소: SK-02 — SK-01 과 같은 사유(규칙 문장 · 옛 글자 0 을 함께 잰다).
- 오라클 해소: SC-01 — 시험이 틀을 실제로 띄워 탭 · 화살표 · 투표 · 메모를 눌러 본다. 시험이 틀을 읽는 대신 따로 만든 고정 사본을 읽으면 SC-02 의 음성 대조(옛 틀로 바꾼 사본)가 통과해 버리므로 SC-02 가 그것을 잡는다.

## 회귀 게이트 — 공통 정의

- `W=/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak3-dz`, `M=$W/.harness/.meta/after-0928-mockup-count`, 기준 커밋 `BASE=c25d16e`, 스프린트 상한 `TIP=chore/ak3-dz` (가지 끝. 이미 합쳐졌으면 그 병합 커밋의 둘째 부모. `HEAD` 를 쓰지 않는다).
- 임시 폴더 틀: `SP=/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/bda55d45-296c-491f-89ba-b52042d58e72/scratchpad/dz`, 명령마다 `TMPDIR=$SP/<이름>`. 사본은 `git -C $W archive $TIP design-kit docs playwright.config.js package.json | tar -x -C <사본>` 으로 풀고 `ln -s /Users/jackson/Hub/10_Dev/claude-plugins/node_modules <사본>/node_modules` 를 한다(작업 폴더에 `node_modules` 바로가기를 만들지 않는다 — `.gitignore` 의 `node_modules/` 는 폴더만 가려 바로가기가 추적 밖 파일로 뜬다). 옛 틀은 `git -C $W show $BASE:design-kit/templates/mockup.html` 로 꺼낸다(봉인 전 실측 1704 줄).
- `page-check.js` 는 playwright 를 `NODE_MODS`(기본 `/Users/jackson/Hub/10_Dev/claude-plugins/node_modules`)에서 읽는다.
- markdownlint: `ML=/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/bda55d45-296c-491f-89ba-b52042d58e72/scratchpad/mdcheck/node_modules/markdownlint-cli2/markdownlint-cli2-bin.mjs` (v0.23.2), 설정 `$M/mdl.markdownlint-cli2.jsonc` = `{"config":{"MD013":false}}`.
- 측정 묶음 sha256 앞 16 자리 (봉인 전 값): `sites.py 64bf938b3b32bd40` · `keep.py 327c170dfac1ac9f` · `keep-lines.txt f2d1790e938a88bc` · `page-check.js 2bad2402420304e0` · `rows.sh f2e7cdc206fe9f9a` · `md-before.txt f14a14aaa2823444` · `mdl.markdownlint-cli2.jsonc 8cb77261e18a1538`. 평가 전에 `shasum -a 256` 로 다시 재서 다르면 그 조건은 FAIL 이다.
- 봉인 전 실측: `sites.py $W` → `SITES total=20 ok=0 bad=20` 종료 코드 1. 알려진 답: S01 만 새 문장으로, S08 은 새 문장에 「최대 5」 를 남긴 사본 → `S01 … ok=1` · `S08 … old=1 ok=0` · `SITES total=20 ok=1 bad=19`. `### Step 2-b` 제목을 지운 사본 → S03 · S04 `MISSING_REGION` · 종료 코드 2.
- 봉인 전 로컬 CI: `ci-local.sh` 25 단계 rc=0 (feedback-agg-test 는 yq 가 없어 SKIP), CI 파일에만 있는 `check-api-kit-docs` · `detect-docs-drift --check-table` · `check-cause-table-copies` · `measure-helpers-test` · `makerworld-fetch-test` · `run-gate-fixtures`(「결과: 24 경우 중 불일치 0」) rc=0, `validate-plugin.py` 「14 plugins, 14 OK」, `npx playwright test design-kit/evals/visuals.spec.js` `156 passed`.

## Skill

- [ ] SK-01: design-mockup 스킬 본문 — Given 구현 커밋 뒤, `python3 $M/sites.py <TIP 사본>` 의 `SITE S01` · `SITE S02` · `SITE S03` · `SITE S04` 네 줄이 모두 `need_miss=- old=0 ok=1` 이다 (S01 description · S02 Gotcha 16 · S03 Step 2-a, 여기에 「정확히 그 수」 도 남아야 한다 · S04 Step 2-b, `풀 밖` · `칸 묶음`) [exact, enumerated]
  측정: `python3 $M/sites.py <사본> | grep -E '^SITE S0[1-4] '` 네 줄의 `ok=1`
  봉인 전 값: 네 줄 모두 `ok=0` (S01 old=2 · S02 old=4 · S03 old=4 · S04 old=1)
- [ ] SK-02: design-kit 참조 · 평가 사례 · README · design-concept — `SITE S05`(visual-change-protocol §5 머리부터 개수 계약까지, 「정확히 그 수」 포함) · `SITE S06`(design-concept Gotcha 6 에 `§5.6` 은 남고 `개수 상한` 0) · `SITE S07`(evals id 19 에 `최소 5`, 「시안 3개」 · 「정확히 3개」 0) · `SITE S08`(README 자동 표 design-mockup 줄) 이 모두 `ok=1` 이고, `python3 scripts/sync-docs.py --check-only design-kit` 출력에 `모든 README가 동기화 상태입니다.` 가 있다 [exact, enumerated]
  측정: `python3 $M/sites.py <사본> | grep -E '^SITE S0[5-8] '` · `cd $W && python3 scripts/sync-docs.py --check-only design-kit`
  봉인 전 값: S05 old=4 · S06 old=1 · S07 old=2 · S08 old=2, 모두 `ok=0`. sync-docs 는 동기화됨
- [ ] SK-03: harness 가이드 §5.6 — `SITE S10`(§5.6 전체에 `최소 5` · `위 제한 없` · `상한 3` 이 다 있다 — 시안은 새 규칙, 그 밖의 탐색형 산출물은 기본 상한 3 을 지킨다) · `SITE S11`(요약 표 Variant Budget 행) 이 `ok=1` 이고, `sh $M/rows.sh <사본>` 이 `md_rows=5 md_good5=1 md_label=1` 을 낸다(Variant Matrix 예시(`mock/a*.html` 시안)가 5 행, Good 줄에 「시안」 · 「5 행」 · 「5 파일」, 그리고 Variant Matrix 제목과 표 머리 사이에 이 예시가 시안 규칙(`최소 5`)을 보여 주며 시안이 아닌 탐색형 산출물은 `상한 3` 이라고 밝히는 줄이 있다 — 같은 절 안에서 「상한 3」 과 「5 행」 이 서로 부딪혀 읽히지 않게 한다) [exact, enumerated]
  측정: 위 두 명령
  봉인 전 값: S10 · S11 `need_miss=최소 5|위 제한 없 old=0 ok=0`, `MATRIX md_rows=3 md_good5=0 md_label=0`
  알려진 답: 예시 표에 A4 · A5 두 행을 더하고 Good 줄을 「시안 … 5 행 … 5 파일」 로 바꾼 사본 → `md_rows=5 md_good5=1 md_label=0` (이름표 줄이 없으면 떨어진다), 여기에 제목 아래 「시안 … 최소 5 … 상한 3」 줄을 더한 사본 → `md_label=1`, HTML 파일을 지운 사본 → `MISSING_FILE` · 종료 코드 2 (봉인 전 실측 일치)
- [ ] SK-04: 틀이 다섯 칸을 기본으로 두되 시안 목록을 한 곳에서 읽는다 — `design-kit/templates/mockup.html` 에서 (a) `grep -cE "\[ ?'a', ?'b', ?'c', ?'d', ?'e' ?\]"` 이 0, (b) `grep -cE "^ +[a-e]: document\.getElementById\('note-[a-e]'\)"` 이 0, (c) `grep -cE 'data-tab="[a-e]"'` 이 5, (d) `grep -cE '^        [a-e]: \{$'`(MOCKUP_CONFIG 칸) 이 5, (e) 틀 안에 `칸 묶음` 이 1 번 이상(여섯째부터 늘리는 방법을 틀 주석에도 적는다) [exact, enumerated]
  측정: 위 다섯 `grep -c`
  봉인 전 값: (a) 4 (b) 5 (c) 5 (d) 5 (e) 0

## Script

- [ ] SC-01: 여섯 시안 틀 시험 — Given 구현 커밋 뒤, `design-kit/evals/visuals.spec.js` 에 이름이 `templates/mockup.html 시안 6 개` 인 `test.describe` 가 있고, 그 안 시험이 실행할 때마다 `design-kit/templates/mockup.html` 을 읽어(스펙 파일에서 `templates/mockup.html` 을 읽는 줄 1 개 이상) 칸 묶음을 f 로 하나 늘린 쪽을 띄운 뒤 (a) f 탭을 누르면 `#panel-f` 가 `active` 이고 그 탭의 `aria-selected` 가 `true`, (b) e 탭에 초점을 두고 ArrowRight 를 누르면 f 탭이 고른 탭이 된다, (c) `#vote-f` 를 누르면 `aria-pressed` 가 `true`, (d) `#note-f` 에 적고 저장한 뒤 쪽을 다시 열면 그 글이 돌아오고 지우기를 누르면 빈 칸이 된다, (e) 이 과정에서 페이지 오류(pageerror) 0 을 확인한다. TIP 사본에서 `npx playwright test design-kit/evals/visuals.spec.js -g 'templates/mockup.html 시안 6 개'` 가 종료 코드 0 이고 통과 수가 4 이상이다 [exact, enumerated]
  측정: 공통 정의의 사본 절차 뒤 `cd <사본> && TMPDIR=$SP/sc01 npx playwright test design-kit/evals/visuals.spec.js -g 'templates/mockup.html 시안 6 개' --reporter=line; echo rc=$?` 의 `N passed`(N≥4) · rc=0, `--list` 로 이름 확인, (a)~(e) 는 스펙을 읽어 각 확인이 있는지 본다
  봉인 전 값: 그 이름의 시험 0 개, 스펙에 `templates/mockup.html` 0 번
- [ ] SC-02: SC-01 음성 대조 — TIP 사본의 `design-kit/templates/mockup.html` 을 옛 틀(`git -C $W show $BASE:design-kit/templates/mockup.html`)로 덮은 사본에서 같은 `-g 'templates/mockup.html 시안 6 개'` 실행이 종료 코드 0 이 아니고 `failed` 가 1 이상이다. 덮기 전 사본은 SC-01 대로 통과해야 한다(변이 확인: 덮은 뒤 SK-04 (a) 가 4) [exact, enumerated]
  측정: `git -C $W show $BASE:design-kit/templates/mockup.html > <사본>/design-kit/templates/mockup.html` 뒤 같은 명령과 `grep -cE "\[ ?'a', ?'b', ?'c', ?'d', ?'e' ?\]"`
  음성 대조: 이 조건 자체가 음성 대조다. 옛 틀은 ArrowRight 가 e 에서 멈추고(`TAB_ORDER` 고정) 메모 저장이 `note-f` 를 빼므로 (b) · (d) 가 떨어져야 한다
- [ ] SC-03: 시험이 CI 에 등록된다 — `.github/workflows/ci.yml` 에 `run: npx playwright test design-kit/evals/visuals.spec.js` 줄이 정확히 1 개이고(새 시험은 같은 스펙 파일 안이라 이 단계가 돌린다), TIP 사본에서 `npx playwright test design-kit/evals/visuals.spec.js` 전체가 종료 코드 0 · 통과 수 ≥ 160 이다 [exact, enumerated]
  측정: `grep -cE 'run: npx playwright test design-kit/evals/visuals\.spec\.js$' .github/workflows/ci.yml` → 1, 전체 실행의 `N passed`
  봉인 전 값: CI 줄 1, `156 passed`
- [ ] SC-04: 로컬 CI — Given 구현 커밋 뒤, `TMPDIR=$SP/ci bash /Users/jackson/Hub/10_Dev/claude-plugins/.harness/handoff/2026-09-26-tools/ci-local.sh $W` 의 `summary.txt` 에 `rc=0` 줄이 25 개(feedback-agg-test SKIP 허용)이고, CI 파일에만 있는 `python3 scripts/check-api-kit-docs.py` · `python3 scripts/detect-docs-drift.py --check-table` · `python3 scripts/check-cause-table-copies.py` · `bash harness/evals/measure/measure-helpers-test.sh` · `bash bambu-kit/evals/run-gate-fixtures.sh` · `bash bambu-kit/evals/makerworld-fetch-test.sh` 가 모두 rc=0 이며 `python3 scripts/validate-plugin.py` 가 `Total: 14 plugins, 14 OK` 다 [exact, enumerated]
  측정: `grep -c 'rc=0' $SP/ci/ci-local/summary.txt`, 여섯 명령 각각 `; echo rc=$?`, validate 마지막 두 줄
  봉인 전 값: 25 · 여섯 모두 rc=0 · 14 OK

## Error

- [ ] ER-01: 시안이 아닌 숫자와 사용자 지정 규칙은 그대로다 — `python3 $M/keep.py <TIP 사본> $M/keep-lines.txt` 가 `KEEP_TOTAL n=21 ok=21 missing=0` · 종료 코드 0 이고(§8.9 두 줄 · 화면 규약 세 벌의 「2 개 이상」 · 「최대 3 회」 줄 · 구별성 판정의 「variant 2 개 이상」 · 「사용자가 개수를 말하면 정확히 그 수」 두 줄 · mockup-guidelines 두 줄 · concept 틀 두 줄 · design-mockup 「스스로 고치기 횟수 상한」 줄 · Bad 두 줄 · evals id 14 · 28 · 29), `git -C $W diff --name-only $BASE..$TIP -- flutter-toolkit react-kit | grep -c .` 이 0 이다 [exact, enumerated]
  측정: 위 두 명령. 사본은 `git -C $W archive $TIP design-kit harness/docs flutter-toolkit/references react-kit/references` 로 푼다
  봉인 전 값: `n=21 ok=21 missing=0`, 구간 차이 0
  양성 대조: mockup-guidelines 의 「최소 2개 축」 을 「최소 3개 축」 으로 바꾼 사본 → `KEEP K05 … ok=0` · `missing=1` · 종료 코드 1 (봉인 전 실측)

## Architecture

- [ ] AR-01: design-kit 문서 쪽 — `SITE S12`~`SITE S19` 여덟 줄(design-mockup.html 머리 알약 · 기준 표 · Step 2-a(「정확히 그 수」 포함) · Step 2-b(`풀 밖` · `칸 묶음`) · Gotcha 16, design-reference.html 다음 단계 설명, visual-change-protocol.html §5 머리부터 개수 계약 카드까지(「정확히 그 수」 포함), design-template.html mockup.html 카드 설명(`최소 5`))이 모두 `ok=1` 이고, `node $M/page-check.js <사본> docs/design-kit/design-mockup.html docs/design-kit/design-reference.html docs/design-kit/visual-change-protocol.html docs/design-kit/design-template.html` 이 `PAGES checked=12 over=0 errors=0 css_bad=0` · 종료 코드 0 이다 [exact, enumerated]
  측정: `python3 $M/sites.py <사본> | grep -E '^SITE S1[2-9] '`, 쪽 검사
  봉인 전 값: 여덟 줄 모두 `ok=0`, 쪽 검사 `PAGES checked=12 over=0 errors=0 css_bad=0`
  양성 대조(쪽 검사): design-mockup.html 끝에 폭 2000px 상자와 `throw` 스크립트를 넣은 사본 → `PAGES checked=3 over=3 errors=3 css_bad=0` · 종료 코드 1 (봉인 전 실측)
- [ ] AR-02: harness 문서 쪽 — `SITE S20`(§5.6 쪽 사본에 `최소 5` · `위 제한 없` · `상한 3`) · `SITE S21`(요약 표 행) 이 `ok=1`, `sh $M/rows.sh <사본>` 이 `html_rows=5 html_good5=1 html_label=1`(SK-03 과 같은 뜻, 쪽 사본), `node $M/page-check.js <사본> docs/harness/skill-design-guide.html` 이 `PAGES checked=3 over=0 errors=0 css_bad=0` 이다 [exact, enumerated]
  측정: 위 세 명령
  봉인 전 값: S20 · S21 `ok=0`, `html_rows=3 html_good5=0 html_label=0`, 쪽 검사 0 · 0 · 0
- [ ] AR-03: 바뀐 경로와 커밋 모양 — Given 구현 커밋 뒤, `git -C $W diff --name-only $BASE..$TIP -- . ':(exclude).harness'` 의 모든 경로가 `## 범위 경계` 의 `# sprint-scope` 블록 안에 들고, `git -C $W log --format=%H $BASE..$TIP` 의 커밋마다 `git -C $W show --name-only --format= <커밋> | cut -d/ -f1 | sort -u | grep -c .` 이 1 이며, 맨 위 폴더 `design-kit` · `harness` · `docs` 가 각각 커밋 하나 이상에 나온다 [exact, enumerated]
  측정: 위 명령들, 블록 밖 경로 수 0 · 맨 위 폴더 둘 이상인 커밋 수 0 · 세 폴더 각각 커밋 수 ≥1. 상한은 가지 끝이며 `HEAD` 를 쓰지 않는다
  봉인 전 값: `$BASE..$TIP` 구간 커밋 0 개 (가지를 막 만들었다)

## Anti-patterns

- [ ] AP-03: bare code fence 금지 — `python3 scripts/validate-plugin.py --check=code-fence` 가 design-kit · harness 에서 FAIL 0 (봉인 전 전체 실행 「14 plugins, 14 OK」)
- [ ] AP-04: frontmatter name 누락 금지 — `python3 scripts/validate-plugin.py --check=frontmatter` 가 design-kit 에서 FAIL 0 (design-mockup · design-concept SKILL.md 의 frontmatter 를 고친다)

## Reusability

- [ ] RE-01: N/A (새 재사용 단위를 만들지 않는다 — 규칙 문장 · 틀 안 스크립트 · 기존 스펙 파일 안 시험만 바꾼다. 측정: `git -C $W diff --name-only --diff-filter=A $BASE..$TIP -- . ':(exclude).harness' | grep -c .` 이 0)
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다 — 새 시험은 기존 `design-kit/evals/visuals.spec.js` 에 넣고 새 스펙 파일을 만들지 않으며, 틀의 시안 목록은 이미 있는 `MOCKUP_CONFIG.variants` 에서 읽는다(새 목록 변수를 두지 않는다). 측정: RE-01 의 새 파일 수 0, `grep -cE "Object\.(keys|entries)\(MOCKUP_CONFIG\.variants\)" design-kit/templates/mockup.html` ≥1 (봉인 전 0)

## Diagnostics

- [ ] DG-01: N/A (commands.analyze 는 `bash -n scripts/release.sh` 만 잰다 — 이번 변경에 없다. 측정: `git -C $W diff --name-only $BASE..$TIP | grep -c '^scripts/release.sh$'` 이 0. 대신 SC-04 의 로컬 CI 를 잰다)
- [ ] DG-02: IDE diagnostics 워닝/인포 0개 ([] 제외) — 바꾼 `.md` 다섯 파일의 markdownlint(MD013 끔) 건수가 `$M/md-before.txt` 의 봉인 전 값 이하다: `design-kit/skills/design-mockup/SKILL.md` 0 · `design-kit/skills/design-concept/SKILL.md` 0 · `design-kit/references/visual-change-protocol.md` 2 · `design-kit/README.md` 0 · `harness/docs/guides/skill-design-guide.md` 0. `design-kit/evals/evals.json` 은 `python3 -c 'import json,sys; json.load(open(sys.argv[1]))'` 가 종료 코드 0. 측정: `node $ML --config $M/mdl.markdownlint-cli2.jsonc <파일>` 출력의 `<파일>:<줄>` 줄 수 · `Linting: 1 file` 줄이 있어야 검사가 돈 것이다
- [ ] DG-03: N/A (commands.test 대상도 `scripts/release.sh` 라 이번 변경에 없다. 측정: DG-01 과 같은 명령. 대신 SC-01 · SC-03 의 시험 실행을 잰다)
- [ ] DG-04: 실제 앱/서버 구동 시 에러 0개 — 구동하는 것은 틀 `design-kit/templates/mockup.html`(시안 6 개 사본)과 문서 쪽 다섯이다. SC-01 (e) 의 페이지 오류 0 확인이 통과하고, AR-01 · AR-02 의 쪽 검사가 `errors=0` 이다. 측정: 그 두 조건의 실행 결과
