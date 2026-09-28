# 2026-09-26~27 「남은 일 전부」 뒤에 실제로 남은 것

기준: main `01b1cac` (origin/main 과 같음), 2026-09-28 에 파일을 직접 열어 다시 확인했다.
읽은 것: `.harness/.meta/after-kaizen-0926b/` 의 `leftovers.md`(120 건) · `decisions.md` · `parent-xdiag.md` ·
`codex-review-1.md` · `codex-review-2.md` · notes 스물두 개(hs · vsa · vsb · cs · gd · pd · pd2 · k1~k4 · us · dca · dcb ·
dr1a · dr1b · dr2 · l1 · l2 · l3a · l3b · l4 · cx · cx2 · cx3).
「확인 못 함」 은 추측이라 사실로 쓰지 않은 것이다.

개수: A 15 · B 22 · C 9 · D 8 · E 34

---

## A. 원래 120 건 가운데 안 했거나 일부만 한 것 (15)

| # | ID | 무엇이 남았나 | 이유 · 지금 main 확인 |
| --- | --- | --- | --- |
| A1 | VS-26 (결정 UD-7 「전부 고친다」) | 목록에 적혀 있던 일곱 파일(루트 README · rust · planning · onboarding README · 검증 가이드 · docs-site SKILL · phase-research-templates)은 0 건이 됐다. 그러나 레포 전체(`.harness` 밖, 추적 파일 509 개)로 재면 **아직 267 건 · 29 파일**. 큰 것: `bambu-kit/skills/bambu-print-profile/SKILL.md` 120 · `api-kit/skills/api-ui/SKILL.md` 25 · `howto-kit/README.md` 18 · `harness/references/contract-schema.md` 8 · harness 시험 계약 다섯 67 · howto · onboarding 시험 입력 여럿 · `design-kit/references/visual-change-protocol.md` 2 | l3a · l3b · l4 가 「고치지 않는 파일」 을 목록에서 뺐다(145 · 45 · 75 건). 뺀 이유는 notes 에 없다. 시험 입력은 일부러 둔 것일 수 있다(확인 못 함). 잰 도구: 세션 scratch 의 markdownlint-cli2 0.23.2, MD013 끔 |
| A2 | DC-9 | 매핑 결정표는 적었지만 도구에 다 반영되지 않았다. `detect-docs-drift.py --since 6378948` 이 **대응 쪽 없음(NEW) 19 개**를 낸다 — 「짝」 으로 정한 tone core 넷 · codex-kaizen search-sources, 「페이지 없음이 맞음」 으로 정한 tone project-detection · research-log 넷(flutter · planning · rust · tone), 「새 페이지」 로 정한 bambu 참고 셋 · figma-parity · cross-kit-principles · react 참고 셋 · reflect-promote | dr2 가 범위 밖이라 했다. 게다가 research-log 는 dr2 가 결정표와 달리 api · backend · infra · react 만 쪽을 만들어 킷마다 다르다 |
| A3 | DC-12 | 어두운 테마 전용 쪽 일곱이 아직 밝은 테마가 없다 — `docs/design-kit/visual-change-protocol.html` · `design-test.html` · `docs/flutter-toolkit/visual-evidence-protocol.html` · `docs/infra-kit/cicd.html` · `infra-test.html` · `docs/onboarding-kit/format-checklist.html` · `docs/react-kit/render-evidence-protocol.html` (셋 다 `data-theme="light"` · 테마 단추 0) | dca 가 열한 쪽, dr2 가 아홉 쪽을 고쳤고 dr1b 가 이 일곱을 넘겼다 |
| A4 | KD-4 design:P2 | 규칙 방향을 바꾸는 일이라 안 했다 | 사용자 결정이 없다 (C 에도) |
| A5 | KD-4 Material 3 | 안 했다 | 바깥 근거 없음 |
| A6 | KF-4 | go_router 18 · auto_route 11.1 문장 확인 안 함 | 바깥 근거 없음 |
| A7 | KI-4 | 빠진 API · GitHub 밖 CI · 1.7+ 확인 안 함 (판 번호 · `env_gaps` 는 함) | 바깥 근거 없음 |
| A8 | KB-1 | 벽시계 문자열 확인 안 함 (OpenAPI · 시간대 저장은 함) | 바깥 근거 없음 |
| A9 | KRe-1 | `<Activity>` canary 여부 확인 안 함 (react-screen Gotcha 11 그대로) | 바깥 근거 없음 — EX-9 가 판정 못 함 |
| A10 | KP-1 | PRD 와 결정 기록(ADR) 비교 안 함. `docs/planning/flows.md:61` 「최신 안정판」 은 원문 인용이 아닌 채 | 바깥 근거 없음 |
| A11 | KT-3 | C-06 강도 · `etc_seq=663` 이름표 · `__` 예시 안 함 | 바깥 근거 없음 |
| A12 | KO-2 | 서비스 계정 키 · 평가 날짜 안 함 | 바깥 근거 없음 |
| A13 | GD-3 · GD-8 일부 | 서브에이전트 frontmatter 필수 필드(agent 가이드 `:70`)와 중첩 깊이 상한 오류 문구는 고치지 않았다 | 바깥 근거 없음 — EX-2 가 묻지 않았거나 원문에 없음 |
| A14 | KBa-3 | 충돌 자리를 notes 에만 적었다. 가지 `feat/bambu-kit-orca-h2s-feedback`(끝 `42209be`, 2026-09-19)은 main 보다 2 커밋 앞서 있고 원격에 없다 · PR 없음. k3 가 그 자리 옆에 줄을 더해 합칠 때 충돌이 더 커진다 | 그 가지를 먼저 올려야 해서 (C 에도) |
| A15 | KA-3 | 보류 · flaky 표지는 뷰어 스펙에만 정했다. 예시 `api-kit/evals/fixtures/unjudged/.api/ui.html` 에 `failMark` 0 — 화면이 실제로 그리는지 확인 안 됨 | 계약 범위 밖 |

---

## B. 이번 작업이 새로 만들었거나 드러낸 결함 · 약점 (22)

「새로」 = 이번 작업이 만든 것, 「전부터」 = 고치기 전에도 있던 것.

### 검사 · 스크립트

| # | 자리 | 무엇 | 영향 | 언제부터 |
| --- | --- | --- | --- | --- |
| B1 | `harness/agents/qa-evaluator.md:235-240` `fm_get` (같은 모양이 `contract-schema.md` 3.5b) | 줄 끝 주석을 값으로 읽는다. `status: superseded   # 새 판 있음` 이면 옛 계약을 다시 채점한다 | 대체된 계약이 평가 대상으로 되살아날 수 있다. `done` · `active` 도 같다 | 전부터 (cx3 독립 검토가 드러냄) |
| B2 | `harness/references/contract-schema.md:263` | `superseded_by` 가 가리킨 계약이 있는지, 그것도 superseded 가 아닌지 기계로 보는 곳이 없다 — 문서 규칙뿐 | 잘못된 슬러그를 적어도 아무도 못 잡는다 | 새로 (cx3) |
| B3 | `harness/skills/sprint-contract/SKILL.md` | `superseded` 로 바꾸는 절차가 0 줄. 같은 슬러그 기존 계약 분기에도 없다 | 형식은 계약 형식 문서에만 있어 계약 쓰는 쪽이 모른다 | 새로 (cx3) |
| B4 | `scripts/check-cause-table-copies.py:12` `BLOCK_END = "- **미확정**"` | 원문 덩어리가 그 줄에서 끝나, 원문에서 그 뒤에 더한 규칙은 사본이 안 따라가도 통과한다 | flutter · react preflight 사본이 조용히 낡을 수 있다 | 새로 (cx, Codex 2 차도 짚음) |
| B5 | `bambu-kit/evals/run-gate-fixtures.sh:63-72` | FAIL 줄 수 · `RESULT` · 종료 코드만 보고 `[미검증]` 줄 수는 안 잰다. 가짜 미검증 줄 하나를 넣어도 `24 경우 중 불일치 0` | 표의 두 행 기대 일부가 재지 않는 채. 빼는 이유도 주석에 없다 | 새로 (k3) |
| B6 | `onboarding-kit/skills/setup-guide/SKILL.md` G5 awk (124~139 줄 근처) | 표 줄 앞 공백 1~3 칸 · 머리 칸 U+00A0 · U+3000 · 우회 칸에 U+00A0 하나 · 굵게 쓴 머리 · 인용 속 표 — 모두 빈 칸이 있어도 통과. 「알아보지 못한 표」 와 「표 없음」 이 구분 안 된다 | 막는 요구 표가 비어도 가이드 검사가 통과할 수 있다 | 새로 — G5 자체가 k4 가 만든 검사. CRLF 는 cx2 가 고침 |
| B7 | `scripts/check-docs-a11y.js:133` | `#theme-btn` 만 찾아, 틀(`themeToggle`)로 만든 쪽의 단추 크기를 못 잰다. 고치면 `docs/design-kit/visual-styles.html` 단추 63x33 이 실패한다 | 새 틀 쪽의 누르기 크기 검사가 비어 있다 | 전부터 (dca 가 드러냄) |
| B8 | `scripts/spawn-kaizen-phase.sh:71` | Phase 상한 17 을 손으로 적었다. 짝 `finalize-phase.sh` 는 마켓 목록에서 뽑는다 | 킷이 늘면 둘이 갈라진다 | 전부터 |
| B9 | `scripts/run-evals.py:32` · `scripts/sync-evals.py:32` | 킷 목록이 손 목록이다 | 새 킷이 평가 실행에서 빠질 수 있다 (api-kit 이 그랬다) | 전부터 |
| B10 | `~/.claude/hooks/parallel-session-guard.sh` | 큰따옴표 안 역따옴표 치환, 치환 안에서 도는 진짜 커밋, `git -c k=v commit`, 서브셸 · `{ …; }` · `bash -c` 커밋을 못 잡는다. `git -C $W …` 커밋 뒤 알림이 다른 폴더의 HEAD 를 보여 준다 | 병렬 세션 경고가 새는 모양이 남았다 | 전부터 (us · cx3 · parent-xdiag) |
| B11 | 설치본 `docs/` 경로 안내 | backend · rust · infra 만 raw 주소 안내가 들어갔다. api 12 · design 5 · howto 7 · planning 14 · react 28 파일이 `docs/…` 를 적고 안내가 없다 | 설치본에서 그 문서를 못 연다. 다만 사용자 프로젝트의 `docs/` 를 뜻하는 경로가 섞여 몇 개가 진짜 문제인지는 확인 못 함 | 전부터 (cx 가 드러냄) |

### 문서 사이트 쪽

| # | 자리 | 무엇 | 영향 | 언제부터 |
| --- | --- | --- | --- | --- |
| B12 | `docs/onboarding-kit/search-strategy.html:513` | `guide_gate G1~G4` 옛 값 (지금은 G1~G5) | 쪽이 틀린 수를 안내한다 | 전부터 (dr1b 가 드러냄, 짝 목록 밖이라 둠) |
| B13 | `docs/bambu-kit/failure-recipes.html` · `materials.html` · `bambu-fields-baseline.html` 머리 | 원본은 「Studio 판은 실행 때 조회, 하드코딩 금지」 인데 `failure-recipes` 는 `v02.06.00.51` 을 박아 두고(3 곳, 「실행 때 조회」 0), `materials` 는 부제 「2.6.0 기준」 과 새 표지가 한 머리에서 부딪힌다. `bambu-fields-baseline` 은 원본의 판 번호 설명이 빠졌다 | 쪽이 원본과 반대로 읽힌다 | 전부터 (원본 변경이 기준 판보다 앞이라 계약이 못 잼) |
| B14 | `docs/onboarding-kit/setup-guide.html` | 원본 인라인 코드 82 개 가운데 8 개(`.env.local` · `.env.production` · `com.<앱이름>.app` · `/insights` · `skill-design-guide.md` 등, 지금 main 에서 0 건) · 「만들 수 없다고 결론 낼 때도 §3.7 네 칸」 규칙이 빠졌다. 낱말 비율 0.65 | 쪽이 원본 규칙 하나를 안 싣는다 | 전부터 |
| B15 | `docs/design-kit/design-test.html` | 쪽 안 움직임 줄이기 규칙을 지우며 `.feat-card:hover` 의 `translateY(-2px)` 를 끄던 줄도 사라졌다 | 움직임을 줄인 설정에서도 카드가 튄다 (공통 파일이 전환 시간은 줄여 줘 사소) | 새로 (dr1b) |
| B16 | `docs/react-kit/integration.html` 외 dr2 가 다시 쓴 쪽 | 옛 판 손 글(「Bad vs Good」 · 「21 스킬 교차 공통 주의사항」 · G1~G6 설계 쪽으로 가는 링크 목록)이 빠졌다. 지금 integration 쪽에서 형제 설계 쪽 링크 0 | 쪽끼리 길이 끊겼다 | 새로 (dr2 가 원본 전문으로 다시 씀) |
| B17 | `docs/process/kaizen-flow.html` `site&#46;css` · dr2 쪽들의 `prefers&#45;reduced-motion` | 글자 참조로 적어 계약 측정을 비켜 갔다. 뜻은 맞다 | 다음 계약의 같은 측정이 헛통과할 수 있다 | 새로 |

### 마크다운 경고 정리의 부작용

| # | 자리 | 무엇 | 영향 | 언제부터 |
| --- | --- | --- | --- | --- |
| B18 | 울타리 짝이 깨진 아홉 파일 — `docs/onboarding-kit/plan-2026-05-18.md` · `docs/react/kit-design/final-integration.md` · `.claude/kaizen-input/per-project-feedback.md` · `.claude/skills/react-kaizen/SKILL.md` · `harness/skills/sprint-contract/SKILL.md` · `docs/superpowers/plans/` 넷 | 경고만 구간 끄기로 0 이 됐고 화면은 깨진 그대로다(바깥 울타리가 여전히 백틱 셋 — ```` 0 건). `per-project-feedback.md:135` 는 짝 없는 끄기로 파일 끝까지 250 줄을 끈다. 100 줄 넘는 끄기 구간 넷 | 읽는 사람에게 코드 블록이 엉뚱하게 닫혀 보인다. 넓은 끄기가 새 경고도 숨긴다 | 화면 깨짐은 전부터, 넓은 끄기는 새로 (l2 · l4) |
| B19 | 파일 8 개 (l3a) · `.claude/skills/react-kaizen/SKILL.md` 4 번 항목 (l4) | 목록 안 코드 블록 앞뒤에 빈 줄이 들어가 목록 항목이 문단으로 그려진다 | 간격만 달라짐, 뜻은 같음 | 새로 |
| B20 | `.harness` 안 지난 계약 · 피드백 520 곳 · `docs/superpowers/followup-2026-04-11-plugin-validation-findings.md` 1 곳 | 빈 줄 · 주석이 들어가 `파일:줄` 참조가 다른 줄을 가리킨다 | 지난 기록을 따라가면 엉뚱한 줄이 나온다. 지금 도는 도구엔 영향 없음 | 새로 (l4) |
| B21 | `planning-kit/agents/planning-reviewer.md:243` · `tone-kit/references/core-naming.md:139` | 예시 문장 속 주소가 `<https://…>` 모양이 됐다(에이전트가 따라 쓸 수 있다). core-naming 한 제목이 H3 로 올라 옆 절과 단계가 같아졌다 | 작음 | 새로 (l3b) |

### 측정 도구 결함 (봉인돼 못 고침 — 다음 계약에 옮길 교훈)

| # | 자리 | 무엇 |
| --- | --- | --- |
| B22 | `.harness/.meta/after-0926-mdlint-*/meaning.py` · cx3 AR-02 · dr1a SC-01 · k4 DG-02 | `meaning.py` 가 `disable-next-line` 을 `disable` 로 읽고, SPACING 은 파일마다 첫 차이 하나만 낸다. cx3 AR-02 의 `git log --format=%B \| tail -2` 는 끝 빈 줄 탓에 여덟 커밋 모두 헛 FAIL. dr1a SC-01 출력 빈칸 둘 대 계약 한 칸. k4 DG-02 는 `sort -u` 로 정렬해 `LC_ALL=C sort` 규칙과 다르다. 계약 형식 문서나 contract-kaizen 에 옮긴 흔적은 확인 못 함 |

---

## C. 사람이 정하거나 실물이 필요한 것 (9)

| # | 무엇 | 왜 사람이 |
| --- | --- | --- |
| C1 | H2S 펌웨어가 `G91` 을 E 축에도 적용하는지 (KBa-4 · EX-6) | 펌웨어 원문이 공개되지 않아 실기 G-code 실측이 필요하다. 지금은 `M83` 만 써서 영향 0 |
| C2 | react-animation · plan-sync-github 의 `# Gotchas` → `## Gotchas` 와 새 H1 을 되돌릴지 (k1 SK-11 · SK-13) | 요청 밖 구조 변경이다. planning-kit 12 스킬 가운데 plan-sync-github 하나만 `## Gotchas` 다. 되돌리려면 조건을 느슨하게 하는 개정이라 사용자 동의가 필요 |
| C3 | KD-4 design:P2 규칙 방향 | 결정 파일에 사용자 결정이 없다 |
| C4 | 승인 기록 폐기 칸에 경로만 둘지, 「하지 않는 것」 이름도 남길지 (pd · pd2) | 교차 진단이 「사용자에게 짚어 확인받으라」 고 권했다. 지금은 경로만 |
| C5 | pd2 둘째 검색의 줄 머리 조건을 넓힐지 — 목록 기호를 손으로 빼고 적은 폐기 기록은 지금 빠진다 | 넓히면 규칙 인용 줄을 폐기 결정으로 잘못 잡는 쪽이 커진다 |
| C6 | k3 · k4 의 1 회차 개정 A-01(조건을 느슨하게 하는 쪽)을 동의 없이 2 회차 새 계약으로 대신한 것 | QA 가 사용자 확인 항목으로 넘겼다. 결정 파일 「추가 위임」 절이 허용한 처리지만 사용자가 본 적은 없다 |
| C7 | 핸드오프 틀이 모델 이름을 박아 둔다 (`~/.claude/skills/handoff/SKILL.md:138`) — 「세션 안내가 준 첨부 줄을 그대로 쓴다」 로 바꿀지 | 다음 모델 교체 때 또 바꿔야 한다. us 가 사용자 판단으로 넘김 |
| C8 | api-kit 이 설치돼 있지 않다 — `~/.claude/plugins/installed_plugins.json` 에 api-kit 없음, 설치본 폴더도 없음. 다른 13 킷은 릴리스 판과 같다 | 설치할지는 사용자 몫 |
| C9 | bambu 오르카 · H2S 피드백 가지 푸시 · PR (A14), 카메라 실물 확인 | 메모리 「bambu-kit 오르카 · H2S 피드백」 에 남은 일. 이 가지가 먼저 올라가야 KBa-3 충돌을 푼다 |

바깥 근거가 없어 못 한 A5~A13 은 사람이 아니라 다음 조사(Codex 리서치)가 풀 일이다.

---

## D. 기록 · 정리 거리 (8)

| # | 무엇 |
| --- | --- |
| D1 | **커밋 `03eae1a` (가지 `chore/ak2-gd`) 가 main 에 없다.** `git merge-base --is-ancestor 03eae1a main` → 1. 내용은 `.harness/sprint-feedback-after-0926-guides.md` 에 「끝점 `a03fe81` 재확인 기록」 13 줄을 덧붙인 것 하나. 그 가지와 워크트리 `.claude/worktrees/ak2-gd` 가 남아 있다. 다른 ak2 가지는 로컬에 없고 원격 둘은 main 에 다 들어갔다 |
| D2 | 로컬 CI 도구 `.harness/handoff/2026-09-26-tools/ci-local.sh` 가 추적되지 않는다. 여러 계약의 DG-05 가 이 파일 지문 `59fe55125c0dbc77` 에 기댄다. 그리고 실제 CI 에 있는 다섯 단계가 이 도구에 없다 — `check-api-kit-docs.py` · `detect-docs-drift.py --check-table` · `check-cause-table-copies.py` · `measure-helpers-test.sh` · bambu 완료 검사 시험. 레포에 들일지 결정도 안 됐다 |
| D3 | 문서 사이트 드리프트: `detect-docs-drift.py --since 6378948` 이 190 짝을 낸다. 대부분은 마크다운 모양만 바뀐 원본(l1~l4)이라 쪽 내용과 같다고 notes 가 적었지만, 190 가운데 어느 것이 진짜 내용 차이인지 도구가 가르지 못하고 이번에 다 가려 보지는 못했다 (확인 못 함). 기본 기준(`main`)으로는 0 |
| D4 | 새 쪽 · 다시 쓴 쪽을 만든 변환 스크립트가 세션 임시 폴더(`scratchpad/dcb` · `scratchpad/dr2/gen`)에만 있다. 원본이 바뀌면 같은 방식으로 다시 만들 수단이 레포에 없다 |
| D5 | 원래 「사용자 결정 필요」 였던 UD-1~UD-8 은 모두 결정 · 반영됐다. 다만 dr2 가 research-log 쪽을 결정표(dca DC-9)와 달리 만들어 결정표 자체가 지금 사실과 어긋난다 (A2 와 같은 뿌리) |
| D6 | `docs/flutter/research-log.md:19` 의 「2.16 부터」 문장은 EX-5 원문(2.7.0)과 다르지만 그날 기록이라 일부러 뒀다. 규칙 본문은 2.7.0 으로 맞다 |
| D7 | `bambu-kit/skills/bambu-print-profile/SKILL.md:2562` 버전 교차 확인 표가 「references 는 `02.06.00.51` 기준」 옛 값 — `/bambu-research` 몫이라 둠 |
| D8 | 커밋 메시지 몇 개에 쉬운 말 목록 낱말(「게이트」)이 들어갔다 — 기록을 다시 쓰지 않기로 해 그대로 |

---

## E. 해결됨 — 앞 묶음이 남긴 것을 뒤 묶음이 고친 것 (34)

| # | 남겼던 곳 | 무엇 | 고친 곳 · 지금 main 근거 |
| --- | --- | --- | --- |
| E1 | vsa 독립 검토 · Codex 1 차 | `check-api-kit-docs.py` 가 `HTTPS://` · 주소 앞 빈칸 · 대문자 `<LINK` 를 놓침 | cx `7122605`. Codex 2 차가 고쳐졌다고 확인 |
| E2 | cx 독립 검토 | 같은 검사가 `url(//…)` · `<img src>` · 빈칸 없는 `@import` 를 놓침 | dr1a `e5c8823` |
| E3 | cx 판단 | `check-api-kit-docs.py` 가 CI 에 없음 | dr1a `604a94c` — `.github/workflows/ci.yml:67-68` |
| E4 | parent-xdiag 2 · cx3 | 종료 코드 표에 인용 안 하는 `check-api-kit-docs` 행 | cx3 `f87e8f4` — `cite=12 rows=12` |
| E5 | Codex 1 차 · k1 UD-3 | flutter · react preflight 판정 표가 원문과 다른 옛 규칙 | cx `64d794c` · `e6e7b27` + 사본 검사 `check-cause-table-copies.py` CI 단계 |
| E6 | k1 KF-2 | flutter-audit 미검증 규칙 사본을 CI 가 안 지킴 | cx SC-04 — `check-reviewer-protocol-copies.py` 목록에 들어감 |
| E7 | cs | `dirty_except_status` 가 본문 `status:` 줄까지 뺌 | cx `f3083ed` · `589c317` |
| E8 | cs 명시적 미완 | 평가 가이드 「①~④ 짝은 다음 사이클로」 · 조건 패턴 표 v5.5 다섯 종 · 판 번호 자리 | cx — `qa-evaluation-guide.md:16` · `:2005` · `:2088` 이 v5.7. `:19` · `:26` · `:2079` 의 v5.5 는 2026-09-24 기록이라 일부러 둠 |
| E9 | cx 독립 검토 | `contract-design-guide.md:759` 「조건 패턴 5 종」 | dr1a `92377e0` |
| E10 | gd 독립 검토 | `harness/README.md:473` 추적 규칙 `kaizen:` | cx `f3083ed` |
| E11 | vsb | 옛 단계 이름 「Step 11」 두 곳 (meta-kaizen · detect-docs-drift 머리) | cx `a6af428` 외 |
| E12 | vsb | 루트 README 나무 그림 · bambu README 「references 4종」 | cx `ad55f4e` · `e7f3caf` |
| E13 | k2 | backend · rust · infra-guide 설치본 `docs/` raw 안내 | cx `52d905c` · `10cc34e` · `1ea26b2` (나머지 킷은 B11) |
| E14 | k2 독립 검토 1 | backend 원칙 문서가 OpenAPI 최소 지원선과 반대로 읽힘 | cx `52d905c` · `2dbdf3f` |
| E15 | k2 독립 검토 2 | design-mockup Step 0 이 대상 정하기 전에 관례 표를 만듦 | cx `5018f7d` |
| E16 | us | `project.yaml` AP-04 정규식이 닫는 `---` 에 걸림 | cx `aec11b4` |
| E17 | k2 | 피드백 `project_hash` 재계산 설명 뒤처짐 | cx SC-06 · SK-09 |
| E18 | Codex 2 차 · k4 | onboarding G5 가 CRLF 가이드에서 빈 칸 통과 | cx2 `af18dd0` (다른 공백 모양은 B6) |
| E19 | Codex 2 차 · dr1b | `visual-change-protocol.md:223` 이 design-mockup 「Step 6」 을 가리킴 | cx2 `e062b70` — 지금 「Step 5」 |
| E20 | parent-xdiag 1 | design-mockup `:171` · 쪽 `:665` 의 「Step 2 가 폐기 칸 경로를」 | cx3 `a7f66c0` — 지금 Step 0 |
| E21 | parent-xdiag 3 | 병렬 세션 훅이 큰따옴표 안 `$( )` 뒤 커밋을 놓침 | cx3 — 레포 밖 훅 (역따옴표 등은 B10) |
| E22 | parent-xdiag 4 · k3 · k4 | 2 회차 계약의 `status: superseded` 가 형식 밖 값 · 새 판 가리킬 칸 없음 | cx3 `2a29cdf` · `b531389` (확인 도구 없음은 B2 · B3) |
| E23 | pd | design-mockup Step 2 가 폐기 칸 경로를 안 읽음 · 계약도 없을 때 결정 자리 | pd2 `2ff7359` · `501c578` · `fc17a35` |
| E24 | pd · pd2 · k2 | `docs/design-kit/design-mockup.html` 옛 글 · 단계 번호 | dr1b (DC-15) · cx3 |
| E25 | vsb | `docs/process/kaizen-flow.html` 범위 줄 카드에 `scripts/` · `templates/` 없음 | dr1a `4dd8126` |
| E26 | hs · cs · cx | `docs/harness/*` 여섯 쪽 옛 판 (`qa-evaluation-guide.html:748` 「50 개 넘는 삭제만」 · `contract-schema.html` · 판 번호 여섯 자리) | dr1a `55b760b` — 지금 `:752` 가 `# sprint-scope` 범위도 적음, 참조 스키마 v5.7 |
| E27 | vsa · dca | `plugin-validation.html` V2 줄 · `static-evidence-viewer-contract.html` | dr1a (DC-3 · DC-4) |
| E28 | dcb | 새 쪽 둘이 틀린 원본 문장(KT-1 「G-04 줄」 · KRf-1 「Stop 실패 시도」)을 실음 | dr1b 가 원본 고친 뒤 다시 맞춤 |
| E29 | k1 · k3 · k4 · vsa · cs | 대응 쪽 없던 원본 — react 설계 여덟(이름 다른 기존 쪽) · research-log 셋 · project-detection · sources · design-brief · feedback-schema · reflect-digest | dcb · dr2 (나머지 19 는 A2) |
| E30 | dr2 | 옛 피드백 시스템 쪽의 저장 폴더 나무가 빠졌다는 걱정 | 지금 `docs/harness/feedback-system.html:212-214` 에 나무 있음 |
| E31 | dcb · vsa | `check-stale-values` 가 오케스트레이터 참고 폴더 · onboarding 원본을 안 봄 | vsa `157e8a2` — `scripts/check-stale-values.py:56` |
| E32 | dcb · vsa | docs-site 매핑 표 `process (공유)` 행 부딪힘 · 드리프트 짝 표 | 합친 뒤 `--check-table` 「스크립트 45 짝 · 표 34 짝 · 어긋남 0」 |
| E33 | VS-24 | 로컬 CI 도구에 `run-kaizen-assertions.py` 없음 | 지금 `ci-local.sh:32` 에 있음 (다른 다섯 단계 빠짐은 D2) |
| E34 | 모든 묶음 | 교차 진단 `pending-parent` 47 건 · UD-2 증거 PNG | parent-xdiag 가 채움, 이 세션 피드백 105 개 가운데 `pending-parent` 0. PNG 12 장은 지워져 추적 0 |

원래 120 건 가운데 위 A 15 줄에 걸린 ID 를 뺀 나머지(HS 6 · VS 27 중 26 · CS 12 · GD 12 중 부분 둘 제외 · PD 4 · KF 1~3 · KD 1~3 · KI 1~3 · KR 3 · KRf 5 · KBa 1 · 2 · 4(G91 제외) · KT 1 · 2 · KO-1 · KA 1 · 2 · 4 · 5 · KH 2 · DC 1~8 · 10 · 11 · 13~15 · US 5)는 notes 의 처리 커밋과 지금 main 파일로 처리됨을 확인했다. KRf-4 `async` 는 「주석만 고치고 `nohup` 유지」, VS-17 은 「검사를 두지 않기로」, DC-13 은 「쪽 결함 아님 — 가는 선 번짐」 으로 판단을 내려 닫았다.
