---
feature: "문서 페이지 다시 맞추기 B (dr1b) — design · flutter · infra · onboarding · react · reflect · rust · tone 14 쪽"
slug: after-0926-docs-regen-b
created: "2026-09-27 15:57"
complexity: "복잡"
conditions: 22
status: done
owner_session: bda55d45-296c-491f-89ba-b52042d58e72
conditions_digest: sha256:3524cadc5bdca4e8
measurement_digest: sha256:589425b3414cf1e0
locked_at: "2026-09-27 16:07"
---

## 배경

원본 md 가 바뀌었는데 문서 사이트 페이지가 옛 판으로 남은 짝 가운데 이 묶음 몫 14 쪽을 지금 원본에 맞춰 다시 만든다. 짝 목록은 `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0926b/.harness/.meta/after-kaizen-0926b/docs-pairs.txt`(읽기만)다. 목록은 경고 정리 전 판 `c3e45f3` 을 기준으로, `origin/main` `6378948` 뒤에 내용이 바뀐 원본 46 짝을 적었다. 그중 `NEW`(대응 페이지 없음)가 아니고 페이지가 `docs/design-kit/` · `docs/flutter-toolkit/` · `docs/infra-kit/` · `docs/onboarding-kit/` · `docs/react-kit/` · `docs/reflect-kit/` · `docs/rust-kit/` · `docs/tone-kit/` 아래인 것이 아래 14 짝이다. 경고 정리(`c3e45f3` 뒤 커밋)는 원본 모양만 바꿨으므로 그것만으로 바뀐 페이지는 대상이 아니다.

- 사용자 위임: 세션 `bda55d45-296c-491f-89ba-b52042d58e72` 의 2026-09-26T10:09:00.557Z 「123다실행해 그러면끝나?다음카이젠에왜넘기는데?」 · 10:30:16.222Z 결정 답 · 2026-09-27T01:22:01.089Z 「자동으로 다 진행해 나한테 묻지 말고 코덱스로 점검 및 리서치하고 5번까지 쭉」(문서 페이지 다시 맞추기를 포함). 결정 파일 `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0926b/.harness/.meta/after-kaizen-0926b/decisions.md`(읽기만) 「추가 위임 (2026-09-27)」 절.
- 사용자 합의(Step 5): 위 위임으로 받은 것으로 적는다. 봉인된 조건을 느슨하게 하는 개정은 이 위임으로 동의 처리하지 않는다 — 그런 개정이 필요하면 부모가 다음 회차 계약으로 처리한다.
- 작업 폴더 W = `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak2-dr1b`, 가지 `chore/ak2-dr1b`(`chore/after-kaizen-0926b` 의 `38cccd1` 에서 갈라짐). 범위 구간의 아래 끝 `BASE` 는 이 계약의 봉인 커밋(이 계약 파일을 처음 담은 커밋)의 부모다 — 커밋 번호를 박지 않고 측정 도우미가 git 기록에서 푼다. 봉인 전 실측 때 그 자리는 `38cccd1` 이었다.
- 만드는 법: 이 레포 `.claude/skills/docs-site/SKILL.md` 절차(Skill 도구가 부르는 설치본이 아니라 W 의 파일이 기준) — 틀 `.claude/skills/docs-site/references/page-template.html`, 공통 파일 `docs/assets/site.css` 링크 한 줄, 킷 색은 `references/css-tokens.md` 매핑, Gotcha 1 · 9 · 10 · 11 · 13, Step 7 의 담김 조건 둘. 파일 이름 · 목차 id 는 바꾸지 않는다(목차 `docs/index.html` 가 이 파일을 iframe 으로 연다). 새로 쓰는 한국어 문장은 쉬운 말로 쓰고, 구현 전에 `tone-kit:tone-guide` 1 단계(규칙 불러오기)를, 완료 선언 전에 5 단계(전수 대조)를 한다. 결과는 notes 에 남긴다(AR-08).
- 커밋 규칙: `git add <경로>` 뒤 `git commit -o <경로>`. 한 커밋에 맨 위 폴더 하나(문서 사이트는 `docs/<킷>/` 하나). `git add -A` · `git stash` · push · 가지 바꾸기 금지. 메시지 한국어, 끝에 빈 줄 뒤 `Co-Authored-By: Claude Opus 5.5 (1M context) <noreply@anthropic.com>`. 본 체크아웃 · 다른 워크트리 · 통합 폴더 `after-0926b` 는 건드리지 않는다. `.harness/` 파일은 페이지와 다른 커밋에 싣는다(AR-07).
- 기록 파일(notes): `.harness/.meta/after-kaizen-0926b/dr1b-notes.md` (W 안, 이 가지에 커밋). 캡처는 세션 임시 폴더(scratch)에 두고 커밋하지 않는다.
- 사용자가 할 일: 없음.

14 짝(원본 → 페이지, `find` · `git ls-files` 로 둘 다 있는 것을 확인했다). 도우미 `LIST` 첫째 · 둘째 칸과 같은 글자다:

| # | 원본 | 페이지 | 원본 머리 판 · 날짜 |
| --- | --- | --- | --- |
| 1 | `design-kit/references/visual-change-protocol.md` | `docs/design-kit/visual-change-protocol.html` | 없음 |
| 2 | `design-kit/skills/design-mockup/SKILL.md` | `docs/design-kit/design-mockup.html` | 없음 |
| 3 | `design-kit/skills/design-test/SKILL.md` | `docs/design-kit/design-test.html` | 없음 |
| 4 | `flutter-toolkit/references/visual-evidence-protocol.md` | `docs/flutter-toolkit/visual-evidence-protocol.html` | `1.2.1` · `2026-09-25` |
| 5 | `docs/infra/platform/cicd.md` | `docs/infra-kit/cicd.html` | `0.2.0` · `2026-09-25` |
| 6 | `infra-kit/skills/infra-test/SKILL.md` | `docs/infra-kit/infra-test.html` | 없음 |
| 7 | `onboarding-kit/skills/setup-guide/SKILL.md` | `docs/onboarding-kit/setup-guide.html` | 없음 |
| 8 | `onboarding-kit/skills/setup-guide/references/format-checklist.md` | `docs/onboarding-kit/format-checklist.html` | 없음 |
| 9 | `react-kit/references/render-evidence-protocol.md` | `docs/react-kit/render-evidence-protocol.html` | `1.1.0` · `2026-09-25` |
| 10 | `reflect-kit/skills/reflect-digest/SKILL.md` | `docs/reflect-kit/reflect-digest.html` | 없음 |
| 11 | `rust-kit/references/project-detection.md` | `docs/rust-kit/project-detection.html` | 없음 |
| 12 | `docs/tone/dart-flutter-idioms.md` | `docs/tone-kit/dart-flutter-idioms.html` | `0.2.0` · `2026-09-27` |
| 13 | `docs/tone/naming-taxonomy.md` | `docs/tone-kit/naming-taxonomy.html` | `0.2.0` · `2026-09-02` |
| 14 | `tone-kit/references/adapter-dart-flutter.md` | `docs/tone-kit/adapter-dart-flutter.html` | 없음 |

「원본 머리 판 · 날짜」 는 원본 첫 머리 설정(`---` 사이)의 `version` · `last_updated` 다. 「없음」 인 아홉은 원본에 그 두 칸이 없다(SKILL.md 머리는 `name` · `description` 뿐이고, 나머지 넷은 머리 설정이 없다 — `m AR-04` 의 `NA` 줄이 같은 판정을 낸다).

공통 전제 G (조건마다 되풀이하지 않는다) — 페이지 · notes 커밋이 가지 `chore/ak2-dr1b` 에 모두 들어간 뒤, 가지를 합치기 전에 잰다.
측정은 `## 회귀 게이트` 의 측정 도우미 `m <조건 ID>` 로 한다. 도우미는 끝점 `TIP`(가지 끝)과 시작점 `BASE`(봉인 커밋의 부모)를 `git archive` 로 풀어 잰다 — 작업 폴더의 커밋 안 된 변경은 보지 않는다(DG-05 만 작업 폴더를 쓴다). `HEAD` 를 상한으로 쓰지 않는다. `TIP` · `BASE` 해석이 안 되면 도우미가 `UNRESOLVED` 를 찍고 멈춘다.
「14 쪽」 · 「14 원본」 은 위 표이며 도우미 `LIST` 와 같은 글자다. 브라우저는 `file://` 로 연다. 「옛 판」 은 `BASE` 의 같은 페이지 파일이다.

복잡도 4 축 — 둘이 「예」 라 최소 「중간」 이고, 14 쪽 · 8 킷에 쪽마다 원본 담김 · 판 번호 · 브라우저 여섯 칸을 재야 해 「복잡」 으로 잡았다. 기능 조건 13 개는 ER-01 ~ ER-03 · AR-01 ~ AR-09 · DG-05 이다 — Step 6.2 두 번째 명령이 `## Anti-patterns` 절 · 자동 포함 여섯 줄(RE-01 · RE-02 · DG-01 ~ DG-04) · `N/A (` 줄을 빼고 센 값이다.

| 축 | 물음 | 값 |
| -- | ---- | -- |
| 레이어 수 | 몇 개 계층을 관통하는가 | 하나 — 정적 문서 화면(HTML · CSS · 쪽 스크립트) |
| 공개 API·계약 변경 | 외부에 노출된 약속이 바뀌는가 | 아니오 — 파일 이름 · 목차 id · 짝 매핑을 바꾸지 않는다(AR-06 이 새 파일 · 지운 파일 0 을 잰다) |
| 소비면 존재 | 반대편이 있는가 | 예 — 목차 `docs/index.html`(iframe 으로 연다), 링크 · 고아 검사 `scripts/check-docs-links.py`, 드리프트 도구 `scripts/detect-docs-drift.py`, 대비 주장 검사 `scripts/check-contrast-claims.py` |
| 회귀 위험 | 기존 동작이 깨질 수 있는가 | 예 — 다시 만들며 옛 페이지에 있던 원본 내용을 빠뜨리거나(실측 2026-09-26: 조건 26 개를 다 통과한 판에서 10 쪽이 원본을 덜 담았다), 좁은 폭에서 넘치거나, 판 번호가 원본과 어긋날 수 있다 |

Step 2.5 짝 조건: 공개 약속이 바뀌지 않아 필수는 아니다. 소비면은 파일 이름을 그대로 두는 것(AR-06 `status=M14`)과 링크 · 고아 검사 통과(ER-03)로 지킨다 — `docs/index.html` 은 고치지 않는다.

설정 값 대조 (`.harness/project.yaml` 을 글자 그대로 옮김):

| config key | project.yaml 에서 읽은 값 | 계약에 쓴 값 |
| ---------- | ------------------------- | ------------ |
| `commands.analyze` | `bash -n scripts/release.sh` | DG-01 N/A — 재는 파일이 바뀐 파일에 없다 |
| `commands.test` | `bash scripts/release.sh 2>&1 \|\| true` | DG-03 N/A — 같은 이유 |
| `diagnostics.ide_exclude` | `[]` | DG-02 의 `([] 제외)` |
| `contract_categories[].id` / `prefix` | Skill/SK · Script/SC · Error/ER · Architecture/AR | 같은 넷(SK · SC 는 N/A) |
| `anti_patterns[].id` / `message` | AP-01 버전 하드코딩 · AP-02 force push · AP-03 bare code fence · AP-04 frontmatter name 누락 | AP-03 (새 notes). AP-01 은 `plugin.json` 판 번호를 읽어야 할 스크립트 대상이라 정적 페이지와 맞지 않고(페이지의 판 번호는 AR-04 가 원본 머리와 맞댄다), AP-02 는 이 계약이 push 하지 않아서, AP-04 는 SKILL.md · 에이전트 파일을 고치지 않아서 뺐다 |

## GAP 분석 (Pre-Edit Audit)

대상 파일을 실제로 읽고 잰 값이다(시작 판 `38cccd1`). 도우미를 `BASE_REF=38cccd1 E_REF=BASE` 로 돌린 출력이다.

| 대상 파일 | 실제 Read 증거 (`파일:라인`) | 발견한 기존 갭·위반 | 계약 조건화 |
| --------- | ---------------------------- | ------------------- | ----------- |
| `docs/design-kit/visual-change-protocol.html` · 원본 `design-kit/references/visual-change-protocol.md` | 원본 `:1` 제목 · `:3-5` SSOT 선언 · 551 줄, 페이지 1121 줄 | 원본이 `6378948`→`c3e45f3` 에 +23/-8. 더해진 줄의 코드 표시 `PRD 없음` 이 페이지에 없고 더해진 줄 낱말 144/173=0.83 | AR-02 · AR-03 |
| `docs/design-kit/design-mockup.html` · 원본 `design-kit/skills/design-mockup/SKILL.md` | 원본 198 줄(목록 PD-1 · `:166` 근처), 페이지 789 줄 | +28/-26. 더해진 코드 표시 7/12 빠짐(`../../references/visual-change-protocol.md` · `.design/approvals/{YYYYMMDD}-{화면명}.md` 등), 낱말 0.63. 옛 판 전체 낱말 비율 0.54 | AR-02 · AR-03 |
| `docs/design-kit/design-test.html` · 원본 `design-kit/skills/design-test/SKILL.md` | 원본 424 줄, 페이지 992 줄 | +3/-2. `status: approved` · `status: superseded` 등 4/7 빠짐(목록 UD-5 결과) | AR-03 |
| `docs/flutter-toolkit/visual-evidence-protocol.html` · 원본 `flutter-toolkit/references/visual-evidence-protocol.md` | 원본 `:3-4` `version: 1.2.1` · `last_updated: 2026-09-25`, 페이지 `:176-177` 같은 값 · `:127` `overflow:hidden` | +2/-0, 더해진 낱말 11/23=0.48. 페이지 CSS 에 숨김 선언 1(Gotcha 11) | AR-01 · AR-03 · AR-04 |
| `docs/infra-kit/cicd.html` · 원본 `docs/infra/platform/cicd.md` | 원본 `:3-4` `0.2.0` · `2026-09-25`, 페이지 `:6` · `:908` 같은 값 · `:281` `overflow:hidden` | 더해진 줄은 이미 담김. 숨김 선언 1 | AR-01 · AR-04 |
| `docs/infra-kit/infra-test.html` · 원본 `infra-kit/skills/infra-test/SKILL.md` | 원본 `:296` · `:337` 「YAML 읽기 실패」, 페이지 `:579` · `:620` 같은 글(목록 KI-2 는 이미 반영) | 더해진 줄은 이미 담김(0.97). 코드 블록 안 `http://localhost:8080/health` 는 출처가 아니라 도우미가 뺀다 | AR-02 · AR-05 |
| `docs/onboarding-kit/setup-guide.html` · 원본 `onboarding-kit/skills/setup-guide/SKILL.md` | 원본 319 줄(`guide_gate` 막는 요구 표 · awk 블록), 페이지 611 줄 | +34/-4. `guide_gate <생성한 가이드> <스택>` 등 2/4 빠짐, 낱말 0.59. 출처 주소 `https://firebase.google.com/docs/ios/setup` 가 링크로 없음(Gotcha 9). 옛 판 전체 낱말 0.56 | AR-02 · AR-03 · AR-05 |
| `docs/onboarding-kit/format-checklist.html` · 원본 `.../references/format-checklist.md` | 원본 137 줄, 더해진 줄 「표 머리는 위 네 칸 그대로 쓴다. `guide_gate` G5 가 …」 | 그 줄 낱말 8/12(`G5` · `머리는` · `머리를` · `주소` 빠짐) | AR-03 |
| `docs/react-kit/render-evidence-protocol.html` · 원본 `react-kit/references/render-evidence-protocol.md` | 원본 `:3-4` `1.1.0` · `2026-09-25`, 페이지 `:467` · `:477-478` 같은 값 | +1/-1, 더해진 줄 낱말 12/24=0.50 | AR-03 · AR-04 |
| `docs/reflect-kit/reflect-digest.html` · 원본 `reflect-kit/skills/reflect-digest/SKILL.md` | 원본 460 줄(목록 VS-21 `:58`), 페이지 812 줄 | 더해진 코드 표시 `.claude/worktrees/` 빠짐 | AR-03 |
| `docs/rust-kit/project-detection.html` · 원본 `rust-kit/references/project-detection.md` | 원본 237 줄(목록 KR-1 · KR-3), 페이지 760 줄 | 원본에서 빠진 `cargo test -p myapp-api --lib healthcheck` · `myapp-api` 가 페이지에 남음(`stale=2`), 더해진 낱말 0.84 | AR-03 |
| `docs/tone-kit/dart-flutter-idioms.html` · 원본 `docs/tone/dart-flutter-idioms.md` | 원본 `:3-4` `0.2.0` · `2026-09-27`(목록 KT-2: 글을 바꾸고 판을 안 올림 — 페이지는 원본 머리를 그대로 따른다), 원본 `:633` 「(표 칸에 옮기면 …)」 은 페이지에 없음(목록 DC-7 은 이미 반영) | 더해진 낱말 20/25=0.80(`version` · `last_updated` · 출처 주소 조각) | AR-03 · AR-04 |
| `docs/tone-kit/naming-taxonomy.html` · 원본 `docs/tone/naming-taxonomy.md` | 원본 `:3-4` `0.2.0` · `2026-09-02`, 페이지 `:276` 같은 값 | 더해진 코드 표시 `Down → Start → Update/MoveUpdate → End/Up → Cancel` 빠짐 | AR-03 · AR-04 |
| `docs/tone-kit/adapter-dart-flutter.html` · 원본 `tone-kit/references/adapter-dart-flutter.md` | 원본 296 줄, 페이지 856 줄 | 더해진 줄 이미 담김(코드 7/7, 낱말 0.90) | AR-02 · AR-03 |
| `.claude/skills/docs-site/SKILL.md` | `:16` Gotcha 1(공통 파일 한 줄 · 움직임 줄이기는 공통 파일) · `:24` Gotcha 9 · `:25-29` Gotcha 10 · `:30` Gotcha 11 · `:32` Gotcha 13 `dk-theme` · Step 7 `2.` 담김 조건 둘 | 14 쪽 가운데 11 쪽이 `<style>` 에 움직임 줄이기 규칙을 다시 적음(`rm0=3/14`), 둘이 숨김 선언(`hide0=12/14`) | AR-01 · RE-02 |
| `scripts/check-docs-a11y.js` | `:59-62` 폭 320 · 375 · 768 · 1280 · `:142` 합격 식(넘침 2px 까지 허용) · `:133` `#theme-btn` | 시작 판 14/14 PASS. 넘침 허용 2px 이라 「넘침 0」 은 도우미 `pw.js of` 로 따로 잰다 | ER-01 · ER-02 |
| `scripts/check-docs-links.py` · `check-contrast-claims.py` · `check-api-kit-docs.py` · `detect-docs-drift.py --check-table` | 네 검사 시작 판 종료 코드 0(`고아 · 유령 · 아이콘 누락 없음` · `어긋난 것: 0` · `12/12 PASS` · `어긋남 0`) | 없음 | ER-03 |
| `/Users/jackson/Hub/10_Dev/claude-plugins/.harness/handoff/2026-09-26-tools/ci-local.sh` | 지문 `01528e5a5c0dfe27a6a9c0bb8ae1c830f2f04860`, 시작 판 `rc=0` 25 · `feedback-agg-test SKIP (yq 없음)` 1. ci.yml 에만 있는 검사 셋(`detect-docs-drift.py --check-table` · `check-cause-table-copies.py` · `measure-helpers-test.sh`) 종료 코드 0 | 없음 | DG-05 |

옛 판 담김 값 — 시작 판 페이지를 지금 원본에 잰 값이다. 인계 도구 `coverage.py`(옛 판 커밋 인자 `38cccd1`)와 `fence2.py`(옛 판 커밋 `509d295` 를 `38cccd1` 로 바꾼 사본)로 잰 값과 도우미 `m AR-02` 가 같은 값을 냈다. 낱말 비율 · 코드 표시(든 수/원본 수) · 코드 블록 줄(든 수/원본 수):

| 페이지 | 낱말 비율 | 코드 표시 | 코드 블록 줄 |
| --- | --- | --- | --- |
| `docs/design-kit/visual-change-protocol.html` | 0.94 | 71/72 | 130/136 |
| `docs/design-kit/design-mockup.html` | 0.54 | 23/38 | 21/21 |
| `docs/design-kit/design-test.html` | 0.92 | 66/70 | 155/155 |
| `docs/flutter-toolkit/visual-evidence-protocol.html` | 0.94 | 37/37 | 10/15 |
| `docs/infra-kit/cicd.html` | 0.94 | 25/25 | 7/7 |
| `docs/infra-kit/infra-test.html` | 0.86 | 136/137 | 219/219 |
| `docs/onboarding-kit/setup-guide.html` | 0.56 | 68/82 | 61/78 |
| `docs/onboarding-kit/format-checklist.html` | 0.87 | 26/28 | 8/8 |
| `docs/react-kit/render-evidence-protocol.html` | 0.95 | 64/64 | 22/24 |
| `docs/reflect-kit/reflect-digest.html` | 0.99 | 197/198 | 123/123 |
| `docs/rust-kit/project-detection.html` | 0.97 | 159/159 | 3/3 |
| `docs/tone-kit/dart-flutter-idioms.html` | 0.96 | 177/182 | 178/211 |
| `docs/tone-kit/naming-taxonomy.html` | 0.95 | 138/141 | 73/92 |
| `docs/tone-kit/adapter-dart-flutter.html` | 1.00 | 203/203 | 31/31 |

## Skill

- [ ] SK-00: N/A (스킬 파일을 고치지 않는다 — 바뀐 파일은 14 쪽뿐이다. 측정: `m AR-06` 이 `extra=0` 이고 바뀐 파일에 `SKILL.md` 0)

## Script

- [ ] SC-00: N/A (스크립트를 만들거나 고치지 않는다 — 측정 도우미는 계약 본문 안 코드 블록이고 레포 파일이 아니다. 측정: `m AR-06` 이 `extra=0`, `m RE-02` 가 `new_files=0`)

## Error

- [ ] ER-01: 14 쪽이 320 · 375 · 1280 폭 × 어두운 · 밝은 테마 여섯 칸 모두에서 가로로 넘치지 않고 잘린 글이 없고 콘솔 오류가 없다 [exact, enumerated]
  Given 공통 전제 G, When `m ER-01`(도우미 `pw.js of` 가 쪽마다 두 테마 각각 브라우저 색 설정 · `dk-theme` 저장값 · `data-theme` 을 맞춰 연 뒤, 세 폭에서 `max(html, body)` 의 `scrollWidth - clientWidth` 와, 화면에 그려진 요소 가운데 넘침을 숨김 · 자름 · 말줄임 · 줄 수 제한으로 가려 내용이 상자보다 큰 요소 수를 잰다), Then 14 줄이 모두 `OK` 이고 칸마다 `넘침/잘림` 이 `0/0`, 끝줄 `of_ok=14/14 cells_zero=84/84 console_err=0`
  측정: `m ER-01`. 시작 판 `of_ok=14/14 cells_zero=84/84 console_err=0`
  양성 대조: 모의 나쁜 판(`docs/design-kit/design-mockup.html` 에 폭 1900px 블록 · 숨김으로 잘리는 글 · 외부 스타일 링크) → `d320=1580/1 d375=1525/1 d1280=620/1 l320=1580/1 l375=1525/1 l1280=620/1 err=2` · `BAD` · `of_ok=0/1` (봉인 전 실측, 임시 복제본)
- [ ] ER-02: 레포 접근성 검사가 14 쪽을 모두 통과한다 [exact]
  Given 공통 전제 G, When `m ER-02`(끝점 트리에서 `node scripts/check-docs-a11y.js` 에 14 쪽을 넘김 — 320 · 375 · 768 · 1280 넘침 · 콘솔 오류 · 모든 글자 요소 대비 · 테마 단추 크기), Then 끝줄 `a11y_rc=0 ok=14/14 files=14`
  측정: `m ER-02`. 시작 판 `a11y_rc=0 ok=14/14 files=14`
  양성 대조: 위 모의 나쁜 판 → `FAIL design-mockup.html of=1580/1525/1132/620 err=1 contrastFail=7` · `a11y_rc=1 ok=13/14 files=14` (봉인 전 실측)
- [ ] ER-03: 문서 사이트 레포 검사 넷이 끝점 트리에서 모두 종료 코드 0 이다 [exact, enumerated]
  Given 공통 전제 G, When `m ER-03`(끝점 트리에서 `scripts/check-docs-links.py` · `scripts/check-contrast-claims.py` · `scripts/check-api-kit-docs.py` · `scripts/detect-docs-drift.py --check-table` 을 차례로 부름), Then 네 줄이 모두 `rc=0` 이고 마지막 줄 글이 각각 `고아 · 유령 · 아이콘 누락 없음` · `어긋난 것: 0` · `12/12 PASS` · `어긋남 0` 을 담는다(검사기가 실제로 돌았다는 줄)
  측정: `m ER-03`. 시작 판 네 줄 모두 `rc=0` 과 위 글
  양성 대조: 모의 나쁜 판에 깨진 상대 링크(`../nope/x.html`)를 넣음 → `check-docs-links.py rc=1`, `#757575 on #FFFFFF 3.5:1 FAIL` 을 넣음 → `check-contrast-claims.py rc=1` (봉인 전 실측)

## Architecture

- [ ] AR-01: 14 쪽이 문서 사이트 틀을 지킨다 — 공통 파일 링크 정확히 하나 [exact, enumerated]
  쪽마다 `assets/site.css` 가 파일 전체에 정확히 한 번, 그것이 `<link>` 의 `href` 로 첫 `<style` 앞에 있고, 그 밖의 외부 자원(다른 `<link>` · `<script src=` · CSS `@import` · `url(http…)` · `url(//…)`)이 0, `:root` 의 `--accent` 가 `css-tokens.md` 킷 값(Design `#E8965A` · Flutter `#22D3EE` · Infra `#34D399` · Onboarding `#7C8AFF` · React `#38BDF8` · Reflect `#F43F5E` · Rust `#E85D4A` · Tone `#D946EF`)과 같고, `wc -l` 과 같은 줄 수가 400 이상이고, `<style>` 안과 `style=""` 속성(CSS 주석 뺌)에 `overflow`(`-x` · `-y` 포함) `hidden` · `clip` 과 `text-overflow:ellipsis` 가 0 이다(Gotcha 1 · 3 · 8 · 11)
  Given 공통 전제 G, When `m AR-01`, Then 끝줄 `exist=14/14 lines=14/14 css1=14/14 ext0=14/14 accent=14/14 hide0=14/14`
  측정: `m AR-01`. 시작 판 `exist=14/14 lines=14/14 css1=14/14 ext0=14/14 accent=14/14 hide0=12/14`(`visual-evidence-protocol.html` · `cicd.html` 의 `overflow:hidden`)
  양성 대조: 모의 나쁜 판(외부 스타일 링크를 더하고 색을 `#000000` 으로, `overflow:hidden` 한 줄) → `ext=1 accent=#000000 hide=1` · `ext0=13/14 accent=13/14` (봉인 전 실측)
- [ ] AR-02: 다시 만든 14 쪽이 옛 판보다 원본을 덜 담지 않는다 (docs-site Step 7 `2.`) [exact, enumerated]
  쪽마다 지금 원본에 대해 (1) 원본 낱말(백틱 밖 2 자 이상) 가운데 쪽 글에 든 비율이 도우미 `LIST` 넷째 칸(옛 판 값, `## GAP 분석` 표와 같음) 이상 — 소수 둘째 자리 반올림으로 견줌, (2) 옛 판 쪽 글에 있던 원본 코드 표시(백틱 글) 가운데 새 쪽에 없는 것 0, (3) 옛 판 쪽에 있던 원본 코드 블록 줄(공백 뺀 8 자 이상) 가운데 새 쪽에 없는 것 0 이고 든 수가 `LIST` 다섯째 칸 이상
  Given 공통 전제 G, When `m AR-02`, Then 14 줄 `OK` · 끝줄 `cov_ok=14/14`
  측정: `m AR-02`(옛 판 = `BASE` 의 같은 쪽 파일). 시작 판을 새 판으로도 넣으면 `cov_ok=14/14`(옛 판과 같으니 통과가 맞다)
  알려진 답: 시작 판 14 쪽을 인계 도구로 따로 잰 값 — `coverage.py <W> <원본> <쪽> 38cccd1` 의 `wr=` · `old=` 와 `fence2.py`(옛 판 커밋만 `38cccd1` 로 바꾼 사본)의 `in_old=` 가 `## GAP 분석` 옛 판 표와 14 줄 모두 같다(예: `design-mockup.html` `wr=0.54->0.54` · `old=23` · `in_old=21`, 종료 코드 0, 봉인 전 실측)
  양성 대조: 모의 나쁜 판(`visual-change-protocol.html` 에서 첫 `<pre>` 블록을 비우고 `visual-change-protocol` 글자를 지움) → `codes=71->70/72 lost=1 fence=130->112/136 flost=18` · `BAD` · `cov_ok=13/14` (봉인 전 실측)
- [ ] AR-03: 14 쪽이 원본이 바뀐 구간(`6378948` → `c3e45f3`)의 내용을 담고, 원본에서 빠진 코드 표시를 남기지 않는다 [exact, enumerated]
  쪽마다 그 구간 `git diff -U0` 의 더한 줄에서 뽑아 지금 원본에도 있는 코드 표시(백틱 글)가 쪽 글에 모두 있고(빠진 수 0), 같은 줄의 낱말(백틱 밖 2 자 이상, 지금 원본에 있는 것) 가운데 쪽 글에 든 비율이 0.90 이상이며, 지운 줄에서 뽑은 4 자 이상 코드 표시 가운데 지금 원본 어디에도 없는 것이 쪽 글에 0 개 남는다
  Given 공통 전제 G, When `m AR-03`, Then 14 줄 `OK` · 끝줄 `delta_ok=14/14`
  측정: `m AR-03`. 시작 판 `delta_ok=3/14`(`OK` 는 `cicd.html` · `infra-test.html` · `adapter-dart-flutter.html`. 나머지 열하나는 `## GAP 분석` 에 적은 빠짐 · 남음)
  알려진 답: `format-checklist.md` 의 그 구간 더한 줄은 한 줄 「표 머리는 위 네 칸 그대로 쓴다. `guide_gate` G5 가 이 머리를 찾아 빈 칸과 주소 없는 출처 칸을 잡는다.」 이다. 손으로 센 2 자 이상 낱말 12 개(`머리는` · `그대로` · `쓴다.` · `G5` · `머리를` · `찾아` · `칸과` · `주소` · `없는` · `출처` · `칸을` · `잡는다.`) 가운데 시작 판 쪽에 없는 것 넷(`G5` · `머리는` · `머리를` · `주소`) → 기대 `dwords=8/12=0.67`, 봉인 전 실제 `dwords=8/12=0.67` · 종료 코드 0
  양성 대조: 시작 판 자체 — `design-mockup.html` `dcodes_missing=7/12`, `project-detection.html` `stale=2`(`cargo test -p myapp-api --lib healthcheck` · `myapp-api`) (봉인 전 실측)
- [ ] AR-04: 원본 머리에 판 번호 · 날짜가 있는 다섯 쪽은 그 값을 그대로 보인다 [exact, enumerated]
  대상 다섯: `docs/flutter-toolkit/visual-evidence-protocol.html`(`1.2.1` · `2026-09-25`) · `docs/infra-kit/cicd.html`(`0.2.0` · `2026-09-25`) · `docs/react-kit/render-evidence-protocol.html`(`1.1.0` · `2026-09-25`) · `docs/tone-kit/dart-flutter-idioms.html`(`0.2.0` · `2026-09-27`) · `docs/tone-kit/naming-taxonomy.html`(`0.2.0` · `2026-09-02`). 쪽 글에 `v<version>` 과 `<last_updated>` 가 있고, 쪽 글에 나오는 `v숫자.숫자.숫자` 꼴 판 번호가 원본 `version` 하나뿐이다. 나머지 아홉은 원본에 두 칸이 없어 `NA` 다
  Given 공통 전제 G, When `m AR-04`(도우미가 끝점 트리의 원본 첫 머리 설정에서 두 값을 읽음), Then 다섯 줄 `OK` · 아홉 줄 `NA` · 끝줄 `ver_ok=5/5 na=9`
  측정: `m AR-04`. 시작 판 `ver_ok=5/5 na=9`
  양성 대조: 모의 나쁜 판(`naming-taxonomy.html` 의 `v0.2.0` 을 `v0.1.0` 으로) → `page_versions=['0.1.0']` · `BAD` · `ver_ok=4/5` (봉인 전 실측)
- [ ] AR-05: 원본 본문의 출처 주소가 모두 쪽의 링크로 옮겨진다 (Gotcha 9) [exact, enumerated]
  원본에서 코드 블록과 백틱 안을 뺀 `http(s)://<점 있는 호스트>…` 주소(끝의 `.,;:` 뺌, 14 원본 합계 90 개)가 각 쪽의 `href="…"` 로 모두 있다
  Given 공통 전제 G, When `m AR-05`, Then 14 줄 `OK` · 끝줄 `url_ok=14/14 src_urls_total=90`
  측정: `m AR-05`. 시작 판 `url_ok=13/14 src_urls_total=90`(`setup-guide.html` 에 `https://firebase.google.com/docs/ios/setup` 링크 없음)
  양성 대조: 시작 판 자체(위 한 줄 `BAD`), 모의 나쁜 판(`format-checklist.html` 의 `https://developer.apple.com/help/account/` 링크를 `#` 로) → `BAD` (봉인 전 실측)
- [ ] AR-06: 바뀐 파일이 정확히 14 쪽이고 모두 고침(이름 그대로)이며 계약 봉인이 깨지지 않는다 [exact, enumerated]
  `git diff --name-status BASE TIP -- . ':(exclude).harness'` 의 경로 집합이 위 표 14 쪽과 정확히 같고(더 많지도 적지도 않음) 상태가 모두 `M`, 전체 차이(`.harness` 포함)에 PNG 0. `.harness/` 는 이름을 열거하지 않고 끝점 트리의 `sprint-contract*.md` 모두(`history/` 포함)에 봉인 검사를 돌려 `SEAL_BROKEN` 이 0 이다
  Given 공통 전제 G, When `m AR-06`, Then `extra=0 missing=0 png=0 status=M14` · `seal_broken=0`
  측정: `m AR-06`. 시작 판 `extra=0 missing=14 png=0 status=` · `seal_broken=0`
  양성 대조: 모의 나쁜 판(`docs/cap.png` 추가, 앞 계약 AR-01 조건 줄 끝에 글자를 더함) → `extra=1 png=1 status=A1 M4` · `SEAL_BROKEN .harness/sprint-contract-after-0926-docs-new-pages.md` · `seal_broken=1` (봉인 전 실측)
- [ ] AR-07: 한 커밋에 맨 위 폴더 하나만 담고 `.harness/` 와 페이지를 섞지 않는다 [exact]
  `BASE` 부터 `TIP` 까지 병합 아닌 커밋마다 `.harness/` 밖 파일의 맨 위 폴더(`docs/` 아래는 `docs/<킷>`)가 둘 이상인 커밋 0, `.harness/` 파일과 그 밖 파일을 함께 담은 커밋 0, 페이지 커밋 1 이상
  Given 공통 전제 G, When `m AR-07`, Then `multi_top=0 mixed=0` 이고 `impl_commits` 1 이상
  측정: `m AR-07`. 시작 판 `commits=0 impl_commits=0 multi_top=0 mixed=0`
  양성 대조: 모의 나쁜 판(notes · `docs/design-kit/` · `docs/onboarding-kit/` · `docs/tone-kit/` · `docs/cap.png` 를 한 커밋에, 앞 계약 파일과 `docs/design-kit/` 쪽을 또 한 커밋에) → `multi_top=1 mixed=2` (봉인 전 실측)
- [ ] AR-08: 결정과 넘김을 notes 에 남긴다 [exact, enumerated]
  Given 끝점 `TIP`, notes `.harness/.meta/after-kaizen-0926b/dr1b-notes.md` 가 커밋돼 있고 여섯 토큰 `tone-guide` · `coverage.py` · `fence2.py` · `KT-2` · `PD-1` · `DC-12` 가 각각 한글 15 자 이상인 줄에 1 번 이상 든다. 담을 내용: `tone-guide` 1 · 5 단계 결과, 다시 만든 뒤 쪽마다 `coverage.py` · `fence2.py` 로 잰 옛 판 → 새 판 값, 목록 KT-2(원본 글이 바뀌었는데 머리 판이 그대로)에 대해 쪽은 원본 머리를 그대로 따랐다는 것, 목록 PD-1 · DC-15 가 말한 design-mockup 쪽 다시 맞춤을 이 묶음이 했다는 것, 목록 DC-12(어두운 테마 전용 쪽의 밝은 테마)는 이 묶음 범위 밖이라는 것과 그 쪽 이름
  When `m AR-08`, Then `committed=1` 이고 여섯 값 모두 1 이상
  측정: `m AR-08`. 시작 판 `committed=0` · `notes=absent`
  양성 대조: 토큰을 짧은 줄에만 적은 모의 notes → `tone-guide=0 coverage.py=0 fence2.py=0 KT-2=0 PD-1=0 DC-12=0`, 한글 15 자 넘는 줄 하나를 더하면 그 토큰만 `tone-guide=1` (봉인 전 실측). 평가자는 셈이 잡은 줄마다 그 줄이 실제로 그 결정이나 넘김을 설명하는지 한 번 눈으로 읽는다 — 토큰을 끼워 넣은 빈말 줄이면 그 값은 0 으로 본다
- [ ] AR-09: 14 쪽을 브라우저로 캡처해 눈으로 확인했고 캡처는 커밋하지 않았다 [exact, collective]
  notes 에 `캡처 폴더: \`<절대 경로>\`` 한 줄이 있고, 그 폴더에 쪽마다 `320` · `375` · `1280` 세 폭 × `dark` · `light` 캡처가 이름 규칙 `<docs 아래 폴더>__<쪽 이름>-<폭>-<테마>.png` 로 모두 있고 비어 있지 않으며, 규칙 밖 이름의 PNG 가 0 이다. PNG 가 커밋되지 않은 것은 AR-06 `png=0` 이 잰다
  Given 공통 전제 G, When `m AR-09`, Then `cap_need=84 cap_have=84 cap_badname=0`
  측정: `m AR-09`. 시작 판 `cap_dir=absent`
  양성 대조: 모의 판(84 장 중 한 장을 빼고 `wrong.png` 를 넣음) → `cap_need=84 cap_have=83 cap_badname=1` (봉인 전 실측)

## Anti-patterns

- [ ] AP-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수 (```text, ```bash, ```yaml 등). 판정 권위는 validate-plugin V6 상태기계다 — 여는/닫는 fence 가 동형이라 줄 단위 정규식으로는 판정 불가
  이 계약에 적용: 새 notes 의 언어 표시 없는 여는 울타리가 0 이다. 측정: `m AP-03` 이 `notes_bare=absent->0`, 킷 전체는 DG-05 의 `validate-plugin rc=0`. 양성 대조: 언어 없는 울타리를 넣은 모의 notes → `notes_bare=absent->1` (봉인 전 실측)

## Reusability

- [ ] RE-01: N/A (산출물이 정적 문서 페이지 14 쪽과 notes 라 비공개로 숨길 재사용 단위 코드가 없다. 측정: `m RE-02` 의 `new_files=0` — 새 스크립트 · 스타일 파일 없음)
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다
  이 계약에 적용: 14 쪽이 공통 파일 `docs/assets/site.css` 가 맡는 움직임 줄이기 규칙을 쪽 `<style>` · `style=""` 에 다시 적지 않고(`prefers-reduced-motion` 0, Gotcha 1 — 쪽 스크립트의 `matchMedia` 확인은 CSS 가 아니라 세지 않는다), 테마 저장 키는 틀의 `dk-theme` 만 쓰며(Gotcha 13), 새 파일을 더하지 않는다. 측정: `m RE-02` 가 `rm0=14/14 theme_key_ok=14/14` · `new_files=0`(시작 판 `rm0=3/14 theme_key_ok=14/14` · `new_files=0`). 양성 대조: 시작 판 자체(11 쪽 `css_rm=1`), 모의 나쁜 판 `docs/cap.png` 추가 → `new_files=1` (봉인 전 실측)

## Diagnostics

- [ ] DG-01: N/A (commands.analyze `bash -n scripts/release.sh` 가 재는 `scripts/release.sh` 는 이번 바뀐 파일에 없다. 측정: `m DG-01` 이 `release_paths=0`. 페이지 쪽 실제 검사는 ER-01 ~ ER-03 과 DG-05) [exact]
- [ ] DG-02: IDE diagnostics 워닝/인포 0개 ([] 제외)
  편집기 진단을 명령줄로 같게 잰다(계약 · QA 리포트 · 개정 파일은 뺀다): 14 쪽 가운데 짝 안 맞는 HTML 태그 수가 시작 판보다 늘어난 파일 0, notes 의 markdownlint-cli2 0.23.2(MD013 끔, 편집기 확장과 같은 설정) 경고 0. 측정: `m DG-02` 가 `tag_worse=0 md_notes=0`(시작 판 `tag_worse=0 md_notes=absent`). 양성 대조: 닫지 않은 `<div>` 를 넣은 모의 쪽 → `TAG_WORSE docs/design-kit/design-mockup.html 0->1` · `tag_worse=1`, 언어 없는 울타리 notes → `md_notes=1` (봉인 전 실측). 설치가 안 되면(망 끊김 등) 도우미가 `md=ENV_FAIL` 을 찍는다 — 그 칸만 `[미검증:ENV]` 로 적고 나머지 칸은 그대로 판정한다
- [ ] DG-03: N/A (commands.test `bash scripts/release.sh 2>&1 || true` 가 재는 `scripts/release.sh` 는 이번 바뀐 파일에 없다. 측정: `m DG-01` 이 `release_paths=0`) [exact]
- [ ] DG-04: 실제 앱/서버 구동 시 에러 0개
  이 계약에 적용: 구동할 앱은 문서 사이트다. 14 쪽을 두 테마로 열 때 콘솔 오류 · 페이지 오류가 0 이다. 측정: `m DG-04` 가 ER-01 끝줄 `console_err=0` 과 ER-02 끝줄 `a11y_rc=0`(각 `OK` 줄 `err=0`). 양성 대조: 외부 스타일 링크를 넣은 모의 쪽 → `err=1`(`net::ERR_NAME_NOT_RESOLVED`) (봉인 전 실측)
- [ ] DG-05: CI(자동 검사) 단계를 로컬에서 전부 돌려 통과한다 [exact]
  Given 작업 폴더 W 가 끝점과 같다(`git -C W rev-parse HEAD` 가 `TIP` 이고 `git -C W status --porcelain --untracked-files=no` 가 빈 출력 — 아니면 도우미가 `W_NOT_TIP` 을 찍고 멈춘다), When `m DG-05` 가 `/Users/jackson/Hub/10_Dev/claude-plugins/.harness/handoff/2026-09-26-tools/ci-local.sh` 를 W 에 돌리고(`TMPDIR` 은 도우미 임시 폴더) ci.yml 에만 있는 검사 셋을 따로 부르면, Then `tool_same=1` · `rc0=25 other=[feedback-agg-test SKIP (yq 없음);]` · `drift_table_rc=0 cause_copies_rc=0 measure_helpers_rc=0`
  측정: `m DG-05`. 도구 파일은 이 가지 밖(본 체크아웃)에 있어 커밋으로 고정되지 않으므로 도우미가 그 내용 지문(`git hash-object`)을 봉인 때 값 `TOOL_BLOB` 과 대조한다. 시작 판(W 가 `38cccd1`) `rc0=25 other=[feedback-agg-test SKIP (yq 없음);]`, 셋 모두 종료 코드 0, 지문 `01528e5a5c0dfe27a6a9c0bb8ae1c830f2f04860`. `tool_same=0` 이거나 요약 파일이 없으면(`ci_summary=absent`) 그 회차는 `[미검증:ENV]` 로 적는다
  음성 대조: 이 계약이 기대는 `docs-a11y` 단계는 ER-02 양성 대조처럼 넘치는 쪽을 넣으면 `rc=1`, `docs-links` · `contrast-claims` 단계는 ER-03 양성 대조처럼 깨진 링크 · 틀린 대비 주장을 넣으면 `rc=1` 이 된다

## 범위 경계

```text
# sprint-scope
docs/design-kit/visual-change-protocol.html
docs/design-kit/design-mockup.html
docs/design-kit/design-test.html
docs/flutter-toolkit/visual-evidence-protocol.html
docs/infra-kit/cicd.html
docs/infra-kit/infra-test.html
docs/onboarding-kit/setup-guide.html
docs/onboarding-kit/format-checklist.html
docs/react-kit/render-evidence-protocol.html
docs/reflect-kit/reflect-digest.html
docs/rust-kit/project-detection.html
docs/tone-kit/dart-flutter-idioms.html
docs/tone-kit/naming-taxonomy.html
docs/tone-kit/adapter-dart-flutter.html
```

| 항목 | 처리 | 조건 · 사유 |
| --- | --- | --- |
| 14 쪽 다시 만들기 | 계약에 넣음 | ER-01 ~ ER-03 · AR-01 ~ AR-09 |
| 원본 md · 틀 · 공통 파일 · `docs/index.html` · 드리프트 도구 | 범위 밖 | 원본에 맞추는 일이지 원본을 고치는 일이 아니다. AR-06 이 바뀐 파일을 14 쪽으로 묶는다 |
| 원본 머리 판이 안 오른 것(목록 KT-2) | 넘김 · notes | 쪽은 원본 머리를 그대로 따른다(AR-04). 원본 판을 올리는 일은 원본 쪽 묶음 몫 |
| 어두운 테마 전용 쪽의 밝은 테마(목록 DC-12) | 범위 밖 · notes | 14 쪽 가운데 일곱이 지금 어두운 테마 전용(`scripts/check-docs-a11y.js` 출력 `theme=dark-only`)이다. 밝은 테마 규칙을 새로 넣으라고 걸지 않는다 — ER-01 은 두 테마 설정 모두에서 넘침 · 잘림 · 오류만 잰다. 틀로 다시 만들며 밝은 테마가 생기는 것은 막지 않는다 |
| design-mockup 쪽(목록 PD-1 · DC-15) | 계약에 넣음 | PD-1 로 바뀐 원본을 담는 것이 AR-03 대상이다 |
| 원본을 더 고칠 다른 묶음(KR-1 · KR-3 · VS-21 등) | 넘김 (부모) | 이 묶음은 시작 판 원본으로 만든다. 그 묶음이 합쳐진 뒤 `python3 scripts/detect-docs-drift.py --since <합친 기준>` 이 다시 맞출 쪽을 낸다 |
| `scripts/check-docs-a11y.js` 넘침 허용 2px | 범위 밖 | 레포 검사는 그대로 부르고(ER-02), 「넘침 0」 은 도우미로 따로 잰다(ER-01) |
| 캡처 | notes | scratch 에 두고 커밋하지 않는다(AR-06 `png=0` · AR-09) |

커버리지 해소 — Step 6.5 (4) 검출기가 낸 `UNCOVERED` 와 목록을 한 곳에만 둔 조건:

- 커버리지 해소: 14 쪽을 열거하는 조건(ER-01 · ER-02 · AR-01 · AR-02 · AR-03 · AR-05 · AR-06 · RE-02 · DG-02) — 목록은 `## 배경` 표 · 범위 목록 블록 · 도우미 `LIST` 에 같은 글자로 있고 `m` 이 그 목록을 잰다. 측정 절에 14 경로를 되풀이해 적지 않는다
- 커버리지 해소: AR-04 — 다섯 쪽은 조건 문장에 모두 적었고, 도우미는 `LIST` 14 쪽 모두를 돌려 원본 머리가 없는 아홉을 `NA` 로 낸다
- 커버리지 해소: ER-03 — 네 검사 스크립트는 대상이 아니라 도우미가 끝점 트리에서 부르는 도구다
- 커버리지 해소: AR-01 — `assets/site.css` · `css-tokens.md` 는 대상이 아니라 판정 기준이다. 킷 색은 조건 산문과 `LIST` 셋째 칸에 같은 값으로 있다
- 커버리지 해소: AR-08 · AR-09 — notes 경로는 조건 문장과 도우미 `NOTES` 에 같은 글자로 있다. AR-08 의 `coverage.py` · `fence2.py` 는 파일이 아니라 `m AR-08` 이 세는 토큰 여섯 가운데 둘이다(도우미 `tokens` 인자에 같은 글자)
- 커버리지 해소: ER-01 — `넘침/잘림` 은 경로가 아니라 `m ER-01` 출력 칸 모양(`d320=0/0` 처럼)을 가리키는 말이다
- 커버리지 해소: AR-01 — `url(//…)` 은 도우미 `pages` 의 외부 자원 정규식(`url\(\s*['"]?(?:https?:)?//`)이 세는 모양의 이름이다
- 커버리지 해소: AR-06 — `.harness/` · `history/` · `sprint-contract*.md` 는 뺄 범위와 봉인 검사 대상의 이름 규칙이며 도우미 `AR-06` 줄의 `':(exclude).harness'` · `find .harness -name 'sprint-contract*.md'` 가 그대로 쓴다
- 커버리지 해소: AR-04 · ER-03 — 위 두 줄과 같다(다섯 쪽과 판 번호는 원본 머리에서 도우미가 읽고, 네 검사 스크립트는 도우미 `ER-03` 줄에 같은 글자로 있다)

교차 진단(qa-evaluator) 때 주의:

- AR-02 의 문턱은 시작 판에서 잰 옛 판 값이다. 문턱은 봉인과 함께 `LIST` 에 고정된다 — 평가자는 옛 판 값을 다시 재지 않아도 되지만, `m AR-02` 출력의 `wr=옛->새` 앞값이 `LIST` 넷째 칸과 같은지는 본다
- AR-03 의 0.90 은 이 계약이 정한 값이다. 바뀐 구간 낱말에는 머리 설정 키 · 주소 조각처럼 쪽 글에 그대로 안 나올 수 있는 것이 섞여(`dart-flutter-idioms.md` 의 `version` · `last_updated` · `https`) 1.00 은 걸지 않았다
- 계약 파일의 편집기 경고(첫 줄 제목 없음 · 코드 표시 안 공백 등)는 계약 형식에서 나온다. 계약 · QA 리포트 · 개정 파일은 DG-02 대상에서 뺀다

## 회귀 게이트 — 측정 도우미 · 봉인 전 실측

평가 때 이 블록을 떼어 bash 에서 불러 쓴다. `TMPDIR` 은 평가자 임시 폴더로 준다. 도우미는 `$T` 아래에만 쓴다 — 작업 폴더와 그 밖의 입력은 지우지 마라.
브라우저 도구는 작업 폴더 W 의 `node_modules`(추적 안 되는 폴더, 봉인 전에 `npm ci` 로 설치함)를 `NODE_PATH` 로 빌려 쓰고, 푼 트리마다 그 폴더를 가리키는 연결을 만든다.

준비 단계 실측(봉인 전, 이 기계): `npm ci` 종료 코드 0, W 의 `node_modules/playwright-core` 판 `1.58.2`, `python3` · `git` · `shasum` · `node` 종료 코드 0, `markdownlint-cli2@0.23.2` 임시 설치 종료 코드 0, `ci-local.sh` 지문 `git hash-object` → `01528e5a5c0dfe27a6a9c0bb8ae1c830f2f04860`. 브라우저가 없으면 `Executable doesn't exist` 로 멈춘다 — 복구: `cd W && node_modules/.bin/playwright-core install chromium-headless-shell` 뒤 다시 잰다. 브라우저가 없어 못 잰 조건은 FAIL 이 아니라 환경 실패로 보고한다.
Playwright 쓰임(`newContext` 의 `viewport` · `colorScheme` · `reducedMotion`, `addInitScript` 인자, `setViewportSize`, `page.on('console')`)은 앞 계약 `after-0926-docs-new-pages` 가 Context7 `/microsoft/playwright/v1.58.2` 문서와 맞춰 본 것과 같은 판 · 같은 호출이다.
봉인 전 실측은 `BASE_REF=38cccd1 E_REF=BASE` 로 잰 시작 판 값과, 임시 복제본(`W=<복제본> NM=<W 의 node_modules>`, 가지 `chore/ak2-dr1b` 를 세션 임시 폴더에 복제)에 모의 나쁜 판을 커밋해 잰 값이다. 복제본은 이 가지와 무관하다.
도우미는 zsh 에서 부르지 마라 — zsh 는 따옴표 없는 변수를 낱말로 나누지 않아 쪽 목록이 한 덩어리가 된다.

```bash
# 떼기: awk '/^# === 측정 도우미 시작/{f=1} f{print} /^# === 측정 도우미 끝/{exit}' <계약> > "$TMPDIR/dr1b-measure.sh"
# 부르기: bash -c 'source "$TMPDIR/dr1b-measure.sh" || exit 2; type m >/dev/null || exit 2; m AR-02'
# 봉인 커밋이 아직 없을 때: BASE_REF=<커밋> 을 준다. 시작 판을 재려면 E_REF=BASE. 임시 복제본을 재려면 W=<복제본> NM=<node_modules 경로>
# === 측정 도우미 시작 (after-0926-docs-regen-b) ===
# 쓰는 법: 이 블록을 파일로 떼어 bash 에서 source 한 뒤 `m <조건 ID>`. zsh 에서 부르지 마라(따옴표 없는 변수를 낱말로 나누지 않아 목록이 한 덩어리가 된다).
# 끝점 TIP = 가지 끝. 시작점 BASE = 이 계약을 처음 담은 커밋(봉인 커밋)의 부모 — 커밋 번호를 박지 않고 git 기록에서 푼다.
# 봉인 커밋이 아직 없으면 BASE_REF=<커밋> 을 준다. 시작 판 자체를 재려면 E_REF=BASE. 임시 복제본을 재려면 W=<복제본> NM=<node_modules 경로>.
W=${W:-/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak2-dr1b}
BR=${BR:-chore/ak2-dr1b}
SLUG=after-0926-docs-regen-b
CF_REL=.harness/sprint-contract-$SLUG.md
NOTES=.harness/.meta/after-kaizen-0926b/dr1b-notes.md
TIP=$(git -C "$W" rev-parse --verify -q "$BR^{commit}") || { echo "UNRESOLVED TIP"; return 2 2>/dev/null || exit 2; }
if [ -n "${BASE_REF:-}" ]; then
  BASE=$(git -C "$W" rev-parse --verify -q "$BASE_REF^{commit}") || { echo "UNRESOLVED BASE_REF"; return 2 2>/dev/null || exit 2; }
else
  SEAL=$(git -C "$W" log --diff-filter=A --format=%H "$TIP" -- "$CF_REL" | tail -1)
  [ -n "$SEAL" ] || { echo "UNRESOLVED SEAL (봉인 커밋 없음)"; return 2 2>/dev/null || exit 2; }
  BASE=$(git -C "$W" rev-parse --verify -q "$SEAL^") || { echo "UNRESOLVED BASE"; return 2 2>/dev/null || exit 2; }
fi
# 원본이 바뀐 구간 — 짝 목록을 만든 구간(origin/main 6378948 → 경고 정리 전 판 c3e45f3). 경고 정리(c3e45f3 뒤)는 모양만 바꿔 넣지 않는다
D_FROM=6378948; D_TO=c3e45f3
T=$(mktemp -d "${TMPDIR:-/tmp}/dr1b.XXXXXX")
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
# 원본 | 쪽 | --accent | 옛 판 낱말 비율 | 옛 판 코드 블록 줄 수(쪽에 든 것)
# 옛 판 값 = 시작 판(BASE) 쪽을 지금 원본에 잰 값. coverage.py · fence2.py 와 같은 글 뽑기(봉인 전 실측)
LIST='design-kit/references/visual-change-protocol.md|docs/design-kit/visual-change-protocol.html|#E8965A|0.94|130
design-kit/skills/design-mockup/SKILL.md|docs/design-kit/design-mockup.html|#E8965A|0.54|21
design-kit/skills/design-test/SKILL.md|docs/design-kit/design-test.html|#E8965A|0.92|155
flutter-toolkit/references/visual-evidence-protocol.md|docs/flutter-toolkit/visual-evidence-protocol.html|#22D3EE|0.94|10
docs/infra/platform/cicd.md|docs/infra-kit/cicd.html|#34D399|0.94|7
infra-kit/skills/infra-test/SKILL.md|docs/infra-kit/infra-test.html|#34D399|0.86|219
onboarding-kit/skills/setup-guide/SKILL.md|docs/onboarding-kit/setup-guide.html|#7C8AFF|0.56|61
onboarding-kit/skills/setup-guide/references/format-checklist.md|docs/onboarding-kit/format-checklist.html|#7C8AFF|0.87|8
react-kit/references/render-evidence-protocol.md|docs/react-kit/render-evidence-protocol.html|#38BDF8|0.95|22
reflect-kit/skills/reflect-digest/SKILL.md|docs/reflect-kit/reflect-digest.html|#F43F5E|0.99|123
rust-kit/references/project-detection.md|docs/rust-kit/project-detection.html|#E85D4A|0.97|3
docs/tone/dart-flutter-idioms.md|docs/tone-kit/dart-flutter-idioms.html|#D946EF|0.96|178
docs/tone/naming-taxonomy.md|docs/tone-kit/naming-taxonomy.html|#D946EF|0.95|73
tone-kit/references/adapter-dart-flutter.md|docs/tone-kit/adapter-dart-flutter.html|#D946EF|1.00|31'
printf '%s\n' "$LIST" > "$T/list.txt"
PAGES=$(printf '%s\n' "$LIST" | cut -d'|' -f2)
N=$(printf '%s\n' "$LIST" | grep -c .)
CAP_RE='^(design-kit|flutter-toolkit|infra-kit|onboarding-kit|react-kit|reflect-kit|rust-kit|tone-kit)__[a-z0-9-]+-(320|375|1280)-(dark|light)\.png$'

cat > "$T/pg.py" <<'PY'
import sys, re, os, html as H, subprocess
from html.parser import HTMLParser
rd = lambda p: open(p, encoding='utf-8').read()
ex = os.path.exists
def items(p):
    return [dict(zip(('src', 'page', 'accent', 'wr', 'fence'), l.split('|'))) for l in rd(p).splitlines() if l.strip()]
def text1(h):
    h = re.sub(r'(?is)<(script|style)[^>]*>.*?</\1>', ' ', h)
    return re.sub(r'\s+', ' ', H.unescape(re.sub(r'<[^>]+>', ' ', h)))
def text2(h):
    h = re.sub(r'(?is)<(script|style)[^>]*>.*?</\1>', '', h)
    return re.sub(r'\s+', '', H.unescape(re.sub(r'<[^>]+>', '', h)))
def css_of(h):
    c = ' '.join(re.findall(r'(?is)<style[^>]*>(.*?)</style>', h)) + ' ' + ' '.join(re.findall(r'(?is)\sstyle="([^"]*)"', h))
    return re.sub(r'(?s)/\*.*?\*/', ' ', c)
def codes_of(s): return sorted({c.strip() for c in re.findall(r'`([^`\n]+)`', s) if c.strip()})
def words_of(s): return {w for w in re.findall(r'[0-9A-Za-z가-힣_.-]{2,}', re.sub(r'`[^`]*`', ' ', s))}
def fence_of(s):
    L = set(); f = False
    for l in s.splitlines():
        if re.match(r'^\s*(```|~~~)', l): f = not f; continue
        if f:
            z = re.sub(r'\s+', '', l)
            if len(z) >= 8: L.add(z)
    return L
URL = re.compile(r'https?://[^\s/)<>\]"\'`|]+\.[^\s)<>\]"\'`|]*')
def urls(s):   # 코드 블록 · 백틱 안 주소(명령 예시)는 출처가 아니라 뺀다
    s = re.sub(r'(?ms)^\s*(```|~~~).*?^\s*\1', ' ', s); s = re.sub(r'`[^`\n]*`', ' ', s)
    return {u.rstrip('.,;:') for u in URL.findall(s)}
def fm(s):
    m = re.match(r'(?s)^---\n(.*?)\n---\n', s); d = {}
    if m:
        for l in m.group(1).splitlines():
            k = re.match(r'^(version|last_updated):\s*["\']?([^"\'\s]+)', l)
            if k: d[k.group(1)] = k.group(2)
    return d
cmd = sys.argv[1]
if cmd == 'cov':   # cov <옛 트리> <새 트리> <list> — 옛 판 대비 원본 담김
    eb, e = sys.argv[2], sys.argv[3]; I = items(sys.argv[4]); ok = 0
    for x in I:
        s = rd(os.path.join(e, x['src'])); p = os.path.join(e, x['page']); po = os.path.join(eb, x['page'])
        if not ex(p): print(f"ABSENT {x['page']}"); continue
        h = rd(p); a, b = text1(h), text2(h); ho = rd(po) if ex(po) else ''; ao, bo = text1(ho), text2(ho)
        C = codes_of(s); cn = [c for c in C if re.sub(r'\s+', ' ', c) in a]; co = [c for c in C if re.sub(r'\s+', ' ', c) in ao]
        lost = [c for c in co if c not in cn]
        Wd = words_of(s); wr = sum(1 for w in Wd if w in a) / max(1, len(Wd)); wro = sum(1 for w in Wd if w in ao) / max(1, len(Wd))
        F = fence_of(s); fn = {z for z in F if z in b}; fo = {z for z in F if z in bo}; flost = fo - fn
        good = round(wr, 2) >= float(x['wr']) and not lost and not flost and len(fn) >= int(x['fence'])
        ok += good
        print(f"{'OK ' if good else 'BAD'} {x['page']} wr={wro:.2f}->{wr:.2f}(>={x['wr']}) codes={len(co)}->{len(cn)}/{len(C)} lost={len(lost)} fence={len(fo)}->{len(fn)}/{len(F)}(>={x['fence']}) flost={len(flost)} {lost[:3]}")
    print(f'cov_ok={ok}/{len(I)}')
elif cmd == 'delta':   # delta <새 트리> <list> <저장소> <from> <to> — 원본이 바뀐 구간에 더해진 줄이 쪽에 담겼는지
    e = sys.argv[2]; I = items(sys.argv[3]); repo, fr, to = sys.argv[4:7]; ok = 0
    for x in I:
        d = subprocess.run(['git', '-C', repo, 'diff', '-U0', fr, to, '--', x['src']], capture_output=True, text=True)
        if d.returncode: print(f"ERR diff {x['src']}"); continue
        add = '\n'.join(l[1:] for l in d.stdout.splitlines() if l.startswith('+') and not l.startswith('+++'))
        cur = rd(os.path.join(e, x['src'])); p = os.path.join(e, x['page'])
        if not ex(p): print(f"ABSENT {x['page']}"); continue
        a = text1(rd(p))
        rem = '\n'.join(l[1:] for l in d.stdout.splitlines() if l.startswith('-') and not l.startswith('---'))
        C = [c for c in codes_of(add) if c in cur]; cm = [c for c in C if re.sub(r'\s+', ' ', c) not in a]
        Wd = {w for w in words_of(add) if w in cur}; wi = sum(1 for w in Wd if w in a); r = wi / len(Wd) if Wd else 1.0
        st = [c for c in codes_of(rem) if c not in cur and len(c) >= 4 and re.sub(r'\s+', ' ', c) in a]   # 원본에서 빠진 코드 표시가 쪽에 남음
        good = not cm and round(r, 2) >= 0.90 and not st; ok += good
        print(f"{'OK ' if good else 'BAD'} {x['page']} dcodes_missing={len(cm)}/{len(C)} dwords={wi}/{len(Wd)}={r:.2f}(>=0.90) stale={len(st)} {cm[:2]} {st[:2]}")
    print(f'delta_ok={ok}/{len(I)}')
elif cmd == 'ver':   # ver <새 트리> <list> — 원본 머리의 version · last_updated 가 쪽 글에 그대로
    e = sys.argv[2]; I = items(sys.argv[3]); ok = na = 0; need = 0
    for x in I:
        f = fm(rd(os.path.join(e, x['src'])))
        if not f: na += 1; print(f"NA  {x['page']} (원본 머리에 version · last_updated 없음)"); continue
        need += 1; p = os.path.join(e, x['page'])
        if not ex(p): print(f"ABSENT {x['page']}"); continue
        a = text1(rd(p)); v, dt = f.get('version', ''), f.get('last_updated', '')
        vs = set(re.findall(r'\bv(\d+\.\d+\.\d+)\b', a))
        good = bool(v) and bool(dt) and ('v' + v) in a and dt in a and vs <= {v}; ok += good
        print(f"{'OK ' if good else 'BAD'} {x['page']} src=v{v}/{dt} page_versions={sorted(vs)} date_in={int(dt in a)}")
    print(f'ver_ok={ok}/{need} na={na}')
elif cmd == 'pages':   # pages <새 트리> <list> — 공통 파일 한 줄 · 외부 자원 · 색 · 줄 수 · 숨김
    e = sys.argv[2]; I = items(sys.argv[3]); agg = dict(exist=0, lines=0, css1=0, ext0=0, accent=0, hide0=0)
    for x in I:
        p = os.path.join(e, x['page'])
        if not ex(p): print(f"ABSENT {x['page']}"); continue
        h = rd(p); agg['exist'] += 1
        n = h.count('\n') + (0 if h.endswith('\n') else 1)
        links = re.findall(r'(?is)<link\b[^>]*>', h)
        site = [l for l in links if re.search(r'''href\s*=\s*["']?(\.\./)+assets/site\.css["'\s>]''', l)]
        allsite = len(re.findall(r'assets/site\.css', h))
        fs = h.lower().find('<style'); sp = h.find(site[0]) if site else -1
        css1 = len(site) == 1 and allsite == 1 and 0 <= sp and (fs < 0 or sp < fs)
        ext = [l for l in links if l not in site] + re.findall(r'(?is)<script\b[^>]*\ssrc\s*=', h) + re.findall(r'@import\b', css_of(h)) + re.findall(r'''url\(\s*['"]?(?:https?:)?//''', h)
        root = re.search(r'(?s):root\s*\{(.*?)\}', h); acc = re.search(r'--accent\s*:\s*(#[0-9A-Fa-f]{6})', root.group(1)) if root else None
        accent = bool(acc) and acc.group(1).upper() == x['accent'].upper()
        hide = re.findall(r'overflow(?:-x|-y)?\s*:\s*(?:hidden|clip)|text-overflow\s*:\s*ellipsis', css_of(h))
        for k, v in (('lines', n >= 400), ('css1', css1), ('ext0', not ext), ('accent', accent), ('hide0', not hide)): agg[k] += bool(v)
        print(f"{x['page']} lines={n} site_css={len(site)}/{allsite} before_style={int(css1)} ext={len(ext)} accent={acc.group(1) if acc else None} hide={len(hide)}")
    print(' '.join(f'{k}={v}/{len(I)}' for k, v in agg.items()))
elif cmd == 'urls':   # urls <새 트리> <list> — 원본의 http(s) 주소가 쪽의 href 로
    e = sys.argv[2]; I = items(sys.argv[3]); ok = tot = 0
    for x in I:
        p = os.path.join(e, x['page'])
        if not ex(p): print(f"ABSENT {x['page']}"); continue
        want = urls(rd(os.path.join(e, x['src']))); have = {H.unescape(u) for u in re.findall(r'''href\s*=\s*["'](https?://[^"']+)["']''', rd(p))}
        miss = sorted(want - have); ok += not miss; tot += len(want)
        print(f"{'OK ' if not miss else 'BAD'} {x['page']} src_urls={len(want)} missing={len(miss)} {miss[:3]}")
    print(f'url_ok={ok}/{len(I)} src_urls_total={tot}')
elif cmd == 'rmcss':   # rmcss <새 트리> <list> — 쪽 <style> · style="" 안 움직임 줄이기 규칙 수(공통 파일이 맡는다) · 테마 키
    e = sys.argv[2]; I = items(sys.argv[3]); ok = th = 0
    for x in I:
        p = os.path.join(e, x['page'])
        if not ex(p): print(f"ABSENT {x['page']}"); continue
        h = rd(p); n = len(re.findall(r'prefers-reduced-motion', css_of(h))); ok += n == 0
        keys = set(re.findall(r'''localStorage\.(?:get|set)Item\(\s*['"]([^'"]+)''', h)); th += keys <= {'dk-theme'}
        print(f"{x['page']} css_rm={n} storage_keys={sorted(keys)}")
    print(f'rm0={ok}/{len(I)} theme_key_ok={th}/{len(I)}')
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
elif cmd == 'bare':   # bare <md> — 언어 표시 없이 여는 코드 울타리 수
    f = sys.argv[2]
    if not ex(f): print('absent'); sys.exit()
    n = 0; o = None
    for l in rd(f).splitlines():
        m = re.match(r'^\s*(`{3,}|~{3,})(.*)$', l)
        if not m: continue
        if o is None: o = m.group(1)[0] * len(m.group(1)); n += (m.group(2).strip() == '')
        elif m.group(1).startswith(o) and m.group(2).strip() == '': o = None
    print(n)
elif cmd == 'commits':   # commits <W> <BASE> <R> — 한 커밋에 맨 위 폴더(docs 는 docs/<폴더>) 둘 이상 · .harness 섞임
    w, b, r = sys.argv[2:5]
    revs = subprocess.run(['git', '-C', w, 'rev-list', '--no-merges', f'{b}..{r}'], capture_output=True, text=True).stdout.split()
    impl = multi = mx = 0
    for c in revs:
        fs = [l for l in subprocess.run(['git', '-C', w, 'show', '--name-only', '--format=', c], capture_output=True, text=True).stdout.splitlines() if l]
        h = [f for f in fs if f.startswith('.harness/')]; o = [f for f in fs if not f.startswith('.harness/')]
        if o: impl += 1
        tops = {('/'.join(f.split('/')[:2]) if f.startswith('docs/') and f.count('/') >= 2 else f.split('/')[0]) for f in o}
        multi += len(tops) > 1; mx += bool(h) and bool(o)
    print(f'commits={len(revs)} impl_commits={impl} multi_top={multi} mixed={mx}')
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
  if (mode === 'of') {   // of <트리> <쪽...> — 320 · 375 · 1280 폭 × 어두운 · 밝은 테마: 문서 가로 넘침(px) · 잘린 글 요소 수 · 콘솔 오류
    let ok = 0, cells = 0, zero = 0, errsAll = 0;
    for (const f of rest) {
      const file = path.join(tree, f); if (!fs.existsSync(file)) { console.log(`ABSENT ${f}`); continue; }
      let pageOk = true; const row = []; let errs = 0;
      for (const theme of ['dark', 'light']) {
        const ctx = await b.newContext({ viewport: { width: 1280, height: 900 }, colorScheme: theme, reducedMotion: 'reduce' });
        await ctx.addInitScript(t => { try { localStorage.setItem('dk-theme', t); } catch (e) {} }, theme);
        const p = await ctx.newPage();
        p.on('console', m => { if (m.type() === 'error') errs++; }); p.on('pageerror', () => errs++);
        await p.goto('file://' + path.resolve(file));
        await p.evaluate(t => { document.documentElement.dataset.theme = t; }, theme); await p.waitForTimeout(400);
        for (const w of [320, 375, 1280]) {
          await p.setViewportSize({ width: w, height: 900 }); await p.waitForTimeout(150);
          const r = await p.evaluate(() => {
            const of = Math.max(document.documentElement.scrollWidth - document.documentElement.clientWidth, document.body.scrollWidth - document.body.clientWidth);
            let clip = 0;
            for (const e of document.querySelectorAll('body *')) {
              if (!e.getClientRects().length || e instanceof SVGElement) continue;
              const cs = getComputedStyle(e);
              const cx = cs.overflowX === 'hidden' || cs.overflowX === 'clip', cy = cs.overflowY === 'hidden' || cs.overflowY === 'clip';
              const ell = cs.textOverflow === 'ellipsis', lc = cs.webkitLineClamp && cs.webkitLineClamp !== 'none';
              if (((cx || ell) && e.scrollWidth > e.clientWidth + 1) || ((cy || lc) && e.scrollHeight > e.clientHeight + 1)) clip++;
            }
            return { of, clip };
          });
          cells++; if (r.of <= 0 && r.clip === 0) zero++; else pageOk = false; row.push(`${theme[0]}${w}=${r.of}/${r.clip}`);
        }
        await ctx.close();
      }
      if (errs) pageOk = false; errsAll += errs; if (pageOk) ok++;
      console.log(`${pageOk ? 'OK ' : 'BAD'} ${f} ${row.join(' ')} err=${errs}`);
    }
    console.log(`of_ok=${ok}/${rest.length} cells_zero=${zero}/${cells} console_err=${errsAll}`);
  }
  await b.close();
})();
JS

m() {
  case "$1" in
    ER-01) (cd "$T" && node pw.js of "$E" $PAGES) ;;
    ER-02) (cd "$E" && node scripts/check-docs-a11y.js $PAGES > "$T/a11y.txt" 2>&1; rc=$?; cat "$T/a11y.txt"
            echo "a11y_rc=$rc ok=$(grep -cE '^OK ' "$T/a11y.txt")/$N files=$(grep -cE '^(OK|FAIL) ' "$T/a11y.txt")") ;;
    ER-03) (cd "$E" && for c in "scripts/check-docs-links.py" "scripts/check-contrast-claims.py" "scripts/check-api-kit-docs.py" "scripts/detect-docs-drift.py --check-table"; do
              python3 $c > "$T/chk.txt" 2>&1; rc=$?; printf '%s rc=%s last=[%s]\n' "${c%% *}" "$rc" "$(grep . "$T/chk.txt" | tail -1)"; done) ;;
    AR-01) python3 "$T/pg.py" pages "$E" "$T/list.txt" ;;
    AR-02) python3 "$T/pg.py" cov "$EB" "$E" "$T/list.txt" ;;
    AR-03) python3 "$T/pg.py" delta "$E" "$T/list.txt" "$W" "$D_FROM" "$D_TO" ;;
    AR-04) python3 "$T/pg.py" ver "$E" "$T/list.txt" ;;
    AR-05) python3 "$T/pg.py" urls "$E" "$T/list.txt" ;;
    AR-06) CH=$(git -C "$W" diff --name-status "$BASE" "$R" -- . ':(exclude).harness')
           WANT=$(printf '%s\n' "$PAGES" | LC_ALL=C sort); GOT=$(printf '%s\n' "$CH" | awk 'NF{print $NF}' | LC_ALL=C sort)
           echo "extra=$(comm -13 <(echo "$WANT") <(echo "$GOT") | grep -c .) missing=$(comm -23 <(echo "$WANT") <(echo "$GOT") | grep -c .) png=$(git -C "$W" diff --name-only "$BASE" "$R" | grep -ci '\.png$') status=$(printf '%s\n' "$CH" | awk 'NF{print $1}' | LC_ALL=C sort | uniq -c | awk '{printf "%s%s ", $2, $1}')"
           comm -3 <(echo "$WANT") <(echo "$GOT") | head -5
           sb=0; for c in $(cd "$E" && find .harness -name 'sprint-contract*.md' | LC_ALL=C sort); do
             rec=$(awk 'NR==1 && /^---$/{f=1; next} f && /^---$/{exit} f && /^conditions_digest:/{sub(/^conditions_digest:[ ]*sha256:/,""); print; exit}' "$E/$c")
             [ -n "$rec" ] || continue
             act=$(grep -E '^- \[[ x]\] [A-Z]{2,}-[0-9]{2}' "$E/$c" | sed -E 's/^- \[[ x]\]/- [ ]/' | shasum -a 256 | cut -c1-16)
             [ "$rec" = "$act" ] || { sb=$((sb+1)); echo "SEAL_BROKEN $c"; }
           done; echo "seal_broken=$sb" ;;
    AR-07) python3 "$T/pg.py" commits "$W" "$BASE" "$R" ;;
    AR-08) echo "committed=$(git -C "$W" cat-file -e "$R:$NOTES" 2>/dev/null && echo 1 || echo 0)"
           python3 "$T/pg.py" tokens "$E/$NOTES" 'tone-guide' 'coverage.py' 'fence2.py' 'KT-2' 'PD-1' 'DC-12' ;;
    AR-09) CAP=$(sed -n 's/^캡처 폴더: `\(.*\)`$/\1/p' "$E/$NOTES" 2>/dev/null | head -1); echo "cap_dir=${CAP:-absent}"
           [ -n "$CAP" ] && [ -d "$CAP" ] || { echo "cap_ok=0"; return 0; }
           need=0; have=0; for p in $PAGES; do
             base=$(echo "$p" | sed -E 's#^docs/##; s#\.html$##; s#/#__#')
             for w in 320 375 1280; do for t in dark light; do need=$((need+1)); [ -s "$CAP/$base-$w-$t.png" ] && have=$((have+1)); done; done
           done
           echo "cap_need=$need cap_have=$have cap_badname=$(find "$CAP" -maxdepth 1 -name '*.png' -exec basename {} \; | grep -cvE "$CAP_RE")" ;;
    RE-02) python3 "$T/pg.py" rmcss "$E" "$T/list.txt"
           echo "new_files=$(git -C "$W" diff --name-status "$BASE" "$R" -- . ':(exclude).harness' | awk '$1 == "A"' | wc -l | tr -d ' ')" ;;
    AP-03) echo "notes_bare=$(python3 "$T/pg.py" bare "$EB/$NOTES")->$(python3 "$T/pg.py" bare "$E/$NOTES")" ;;
    DG-01|DG-03) echo "release_paths=$(git -C "$W" diff --name-only "$BASE" "$R" -- scripts/release.sh | wc -l | tr -d ' ')" ;;
    DG-02) tw=0; for p in $PAGES; do [ -f "$E/$p" ] || { echo "ABSENT $p"; continue; }
             a=$(python3 "$T/pg.py" tags "$E/$p"); bb=0; [ -f "$EB/$p" ] && bb=$(python3 "$T/pg.py" tags "$EB/$p"); [ "$a" -gt "$bb" ] && { tw=$((tw+1)); echo "TAG_WORSE $p $bb->$a"; }; done
           (cd "$T" && npm i --silent --no-save markdownlint-cli2@0.23.2 >/dev/null 2>&1) || echo "md=ENV_FAIL"
           printf '{"config":{"MD013":false}}\n' > "$T/.markdownlint-cli2.jsonc"
           mdc() { [ -f "$1" ] || { echo absent; return; }; (cd "$T" && node_modules/.bin/markdownlint-cli2 "$1" 2>&1 | grep -cE ':[0-9]+(:[0-9]+)? (error|warning)? ?MD[0-9]+' ); }
           echo "tag_worse=$tw md_notes=$(mdc "$E/$NOTES")" ;;
    DG-04) m ER-01 | tail -1; m ER-02 | tail -1 ;;
    DG-05) [ "$(git -C "$W" rev-parse HEAD)" = "$TIP" ] && [ -z "$(git -C "$W" status --porcelain --untracked-files=no)" ] || { echo "W_NOT_TIP"; return 0; }
           echo "tool_same=$([ "$(git hash-object "$CI_LOCAL" 2>/dev/null)" = "$TOOL_BLOB" ] && echo 1 || echo 0)"
           (cd "$W" && TMPDIR="$T" bash "$CI_LOCAL" "$W" > "$T/ci.txt" 2>&1); SUM=$T/ci-local/summary.txt
           [ -s "$SUM" ] || { echo "ci_summary=absent"; return 0; }
           echo "rc0=$(grep -c 'rc=0' "$SUM") other=[$(grep -v 'rc=0' "$SUM" | sed -E 's/[[:space:]]+/ /g' | tr '\n' ';')]"
           # ci.yml 에 있고 ci-local.sh 에 없는 검사 단계 셋(설치 단계 · 여러 줄 run 빼고)
           (cd "$W" && python3 scripts/detect-docs-drift.py --check-table >/dev/null 2>&1; a=$?; python3 scripts/check-cause-table-copies.py >/dev/null 2>&1; b=$?
            TMPDIR="$T" bash harness/evals/measure/measure-helpers-test.sh >/dev/null 2>&1; c=$?; echo "drift_table_rc=$a cause_copies_rc=$b measure_helpers_rc=$c") ;;
    *) echo "UNKNOWN $1" ;;
  esac
}
# === 측정 도우미 끝 ===
```
