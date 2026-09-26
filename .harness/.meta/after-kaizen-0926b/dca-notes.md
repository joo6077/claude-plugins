# dca 묶음 기록 — 문서 사이트 고침 · 320px 기준 폭

계약: `.harness/sprint-contract-after-0926-docs-fixes.md` (봉인 커밋 `8e5699f`, `conditions_digest: sha256:a1f762a2866454db`, `measurement_digest: sha256:57f76c23521e7bc2`).
가지 `chore/ak2-dca`, 시작 판 `6378948`. 개정 대기 한 건: `.harness/sprint-amendments-after-0926-docs-fixes.md` A-01 (아래 「남은 것」).

## 커밋

| 커밋 | 내용 |
| --- | --- |
| `8e5699f` | 계약 봉인 (계약 파일 하나) |
| `5c98e61` | 두 검사에 320px 폭 — `scripts/check-docs-a11y.js` · `design-kit/evals/visuals.spec.js` |
| `7c6820b` | docs-site 스킬 안내 · 새 쪽 틀 · 토큰 문서 |
| `3608542` | 글 고침 DC-7 · DC-8 · DC-10 |
| `7d02ffe` | 쪽 고침 — 320 폭 · 움직임 줄이기 · 밝은 테마 (26 파일) |

## 항목별 결과

| 항목 | 결과 | 근거 |
| --- | --- | --- |
| DC-2 | 처리 (`5c98e61` · `7c6820b` · `7d02ffe`), 한 쪽은 개정 대기 | 검사 두 곳과 스킬 안내에 320 을 넣었고 쪽 44 가운데 43 을 고쳤다 |
| DC-5 | 처리 (`7c6820b`) | 「standalone」 두 곳 · 행간 1.2~1.6 · Motion 안내를 고쳤다 |
| DC-6 | 뺌 — KBa-1 뒤 부모 몫 | KBa-1 이 원본 `bambu-kit/skills/bambu-print-profile/SKILL.md:1604-1612` 의 판정 동작을 바꾸므로 지금 원본에 맞춰 표 행을 쓰면 KBa-1 뒤에 다시 틀린다 |
| DC-7 | 처리 (`3608542`) | 괄호 한 토막만 지운 한 줄 변경 |
| DC-8 | 처리 (`3608542`) | 「정본은」 을 「기준 기록은」 으로 바꾼 한 줄 변경 |
| DC-9 | 결정만 적음 (아래 `## DC-9` 절) | 매핑 표와 드리프트 스크립트는 VS-13 묶음 몫이라 고치지 않았다 |
| DC-10 | 처리 (`3608542`) | 원문 둘과 페이지의 v7 기재를 v8 로, 인용 수치를 v8 실측으로 옮겼다 |
| DC-11 | 처리 (`7d02ffe`) | 움직임 줄이기 설정에서 스크립트 움직임이 멈추는 쪽 일곱 |
| DC-12 | 처리 (`7c6820b` · `7d02ffe`) | 열한 쪽에 밝은 테마 · 테마 단추 · `dk-theme` 저장, 틀의 대비도 고쳤다 |
| DC-13 | 원인 · 재현만 적음 (아래) | 쪽 결함이 아니라 가는 선 번짐이다 |
| DC-14 | 처리 (`7c6820b`) | Step 7 에 담김 조건 둘을 넣었다 |
| KD-2 · VS-18 | 뺌 — 다른 묶음 | design-kit 묶음 · vs 묶음 몫 (계약 범위 경계 표) |

## DC-2 320 폭 — 고친 쪽과 수단

- DC-2 의 공통 수단: 공통 파일 `docs/assets/site.css` 에 `body{overflow-wrap:anywhere}` 한 줄을 더했더니 넓힌 글자 간격에서 모자라던 44 쪽이 15 쪽으로 줄었다.
  긴 주소 · 코드 · 파일 이름이 낱말 중간에서 줄을 바꾸게 되어 표 칸 · 카드 안에서 글이 상자 밖으로 나가던 것이 한꺼번에 풀렸다.
- 이 규칙의 눈에 띄는 부작용: 320 폭의 좁은 표 칸에서 긴 식별자가 두세 줄로 쪼개진다(예: `docs/flutter-toolkit/theming.html` 표의 `useMaterial3`). 글이 잘리거나 사라지지는 않는다.
- DC-2 의 쪽 고침(`7d02ffe`) 열넷: 격자 최소 폭을 `min(Npx,100%)` 로(`ethical-design` · `widget-composition` · `research` · `color-palette` 인라인 폭과 캔버스), 격자 자식에 최소 폭 0(`animation`),
  좁은 폭에서 한 줄 표본을 줄바꿈 허용(`typography-scale` · `information-density` · `ratio-proportion`), 막대 글이 막대 폭보다 길면 막대를 늘림(`microinteraction` · `motion`),
  숨김 대신 가로 스크롤(`grid-alignment` 격자 표본 · `codex-kaizen` 흐름 그림), 목록 줄을 블록으로(`visual-change-protocol`), 주석 딱지 위치를 폭에 맞춤(`visual-hierarchy`),
  안 보이는 전환 표본 쪽을 화면 읽기 프로그램에서도 뺌(`animation` 의 `aria-hidden`, 전환할 때 같이 바꾼다).
- 넘침을 가리는 선언(`overflow:hidden` · 말줄임 · `display:none` · `visibility:hidden`)은 하나도 늘리지 않았다 — `grid-alignment` 는 오히려 `overflow:hidden` 하나를 가로 스크롤로 바꿨다.
- `playwright.config.js` 에는 폭이 적힌 자리가 없어 고칠 것이 없었다. 폭은 `design-kit/evals` 의 시험 파일과 `scripts/check-docs-a11y.js` 두 곳에만 있다.
- `check-docs-a11y.js:54` 의 첫 창 크기 375 는 폭 목록이 아니라 창을 여는 크기라 그대로 뒀다.
- `audit-criteria` 의 375(`design-kit/skills/design-audit/references/audit-criteria.md:97`)는 디자인 킷의 감사 판정값이라 문서 사이트 검사와 다른 일로 보고 그대로 뒀다.

## DC-11 스크립트 움직임

- 맨 위로 단추 넷과 카이젠 흐름 시뮬레이터가 `matchMedia('(prefers-reduced-motion: reduce)')` 를 보고 그 설정이면 `auto` 로 스크롤한다. 보통 설정에서는 그대로 부드럽게 움직인다.
- `animation.html` 의 도는 표본과 `microinteraction.html` 의 진행 막대는 움직임 줄이기 설정이면 타이머를 켜지 않고 멈춘 한 장면(120도 · 60%)만 그린다.
- 목록이 짚은 `docs/flutter-toolkit/animation.html` 의 `.animate(` 는 Dart 코드 표본 글(`:398`)이라 브라우저 움직임이 아니다 — 할 일이 없었다.

## DC-12 밝은 테마와 틀

- 열한 쪽 모두 틀과 같은 방식이다: `[data-theme="light"]` 덮어쓰기, 접근 이름 「테마 전환」 단추 하나, 저장 키 `dk-theme`(누를 때만 저장), 저장값이 없으면 브라우저 색 설정을 따른다.
- 단추 id 는 틀의 `themeToggle` 대신 `theme-btn` 을 썼다 — 레포 검사기가 `theme-btn` 만 찾아 단추 크기를 재기 때문이다. 틀로 만든 쪽의 단추는 검사기가 못 잰다(넘김, 아래 「남은 것」).
- 틀 `--text3` 를 바꾼 까닭: 어두운 값 `#7A6F64` 는 표면 위 3.34, 밝은 값 `#8a8078` 은 밝은 배경 위 3.39 로 대비 기준 4.5 에 못 미쳤다. 틀을 따르면 새 쪽(DC-1)과 이 열한 쪽이 밝은 테마 대비에서 떨어진다.
  어두운 값은 토큰 문서가 기준으로 적은 `#948779`(4.68), 밝은 값은 `#6b6259`(5.25)로 바꾸고 토큰 문서 코드 블록도 맞췄다.
- 밝은 테마에서 대비가 모자라던 곳을 쪽에서 고쳤다: 대비 딱지 배경 · 머리 막대 배경 · 흐름 막대 글색 · 코드 블록 글색, 코드 표본의 고정 색 글자를 쪽 색 토큰으로(어두운 테마 값은 같다).
- `flutter-toolkit/theming.html` 은 위에 붙는 머리 막대가 고정 단추를 덮어 누를 수 없었다 — 단추를 머리 막대 안으로 옮겼다.

## DC-10 옛 시안

- DC-10 에서 시안 이름만 v8 로 바꾸면 「56 개 중 44 미만 39」 같은 인용 수치가 틀린 말이 된다. 그래서 수치도 `api-kit/skills/api-ui/SKILL.md:177` · `:221` 의 v8 실측(57 개 · 44 미만 40 · 2026-09-26)으로 옮겼다.
- `docs/api/research-log.md:179` 는 그날 v7 사본을 연 기록이라 그대로 둔다. 페이지 `static-evidence-viewer-contract.html` 은 DC-3(부모)이 다시 맞춘다.

## DC-13 긴 쪽 캡처 흔들림 — 원인과 재현

- 원인: `contract-schema.html` 옛 판(`33fec27^`)의 `code.code-block` 아래 1px 테두리가 소수 자리 y(`29743.703`)에 걸쳐, 캡처마다 가는 선 번짐이 한 줄(1118 픽셀) 달라진 것이다.
- 다른 픽셀 상자는 `81,29743-1198,29743` 한 줄이었고 페이지 높이는 여덟 번 모두 같았다 — 쪽 레이아웃 결함이 아니라 소수 자리 테두리의 번짐이라 쪽은 고치지 않았다.
- 재현 명령: 계약 회귀 게이트 도우미 `pw.js pixalt <지금 판> <옛 판> docs/harness/contract-schema.html 6` 로 두 판을 번갈아 캡처해 옛 판끼리 견준다. 봉인 전에는 네 번에 한 번 `diff=1118` 이 나왔다.
- 이번 재기(2026-09-26 21:0x, 끝점 `7d02ffe`): `pix` 지금 판 `zero=5/5`, `pixalt` 지금 판 기준 `zero=5/5`, 옛 판 기준 `zero=5/5` — 흔들림이 가끔만 나타나 이번에는 옛 판도 0 이었다.

## tone-guide 결과

- tone-guide 1 단계: 오버레이 `.claude/tone-project.md`(어댑터 없음 · 주석 언어 ko)를 읽고 코어 규칙 넷과 `locale-korean.md` 를 불러왔다. 이번 작업에 걸린 규칙은 C-01 · C-03 · C-07 · C-10 · C-13 · C-15 · N-08 · S-03 · K-02 · K-03 · K-11 이다.
- tone-guide 5 단계 전수 대조 표는 아래와 같다 — 더한 줄 441 을 대상으로 했다.

| 패턴 / 규칙 | 건수 | 판정 |
| --- | --- | --- |
| C-01 · C-15 새 주석 | 16 | 통과 — 모두 까닭을 적는 한 줄(줄바꿈 규칙 · 테마 저장 규칙 · 움직임 줄이기 분기) |
| C-04 · F 구분선 블록 | 0 | 통과 |
| C-10 디자인 툴 참조 | 0 | 통과 — 노드 ID · 변수 경로 없음 |
| C-13 자화자찬 | 0 | 통과 |
| N-08 한 글자 이름 | 1 | 통과 — `check-docs-a11y.js` 의 폭 반복 변수 `w` 는 원래 있던 반복 색인 |
| K-02 번역투 여섯 종(§8 G-1) | 0 | 통과 |
| K-04 · G-2 `합니다` 종결 | 0 | 통과 |
| K-11 새 이름 | 0 | 통과 — 새 합성어 없이 파일 · 설정 키 이름을 그대로 썼다 |
| S-03 · S-04 추출 | 0 | 통과 — 새 함수는 테마 둘(`applyTheme` · `toggleTheme`, 틀과 같은 이름)뿐 |

## 킷별 판 판단

- design-kit: `design-kit/evals` 의 시험 파일 하나만 바뀌었다. 스킬 동작은 그대로라 판을 올린다면 patch 이고, 이 묶음 혼자로는 올릴 까닭이 약하다 — 다른 design-kit 변경과 함께 싣는다.
- 나머지 변경(`.claude/skills/docs-site/` · `scripts/` · `docs/`)은 킷 폴더 밖이라 판 번호가 없다.

## docs 드리프트

- `python3 scripts/detect-docs-drift.py --since 6378948` → `docs/api/verification/static-evidence-viewer-contract.md → docs/api-kit/static-evidence-viewer-contract.html` 한 줄. 이 묶음이 같은 페이지의 v7 기재와 수치를 같이 고쳤다. 페이지 전체 다시 맞추기는 DC-3(부모) 몫이다.

## 측정 도구

- 계약 도우미를 뗀 파일과 임시 트리: `/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/bda55d45-296c-491f-89ba-b52042d58e72/scratchpad/dca2/` (`dca-measure.sh` · `pw.js` · `pg.py` · 실행 도우미 `runw.sh` · `runm.sh` · `runt.sh` · `runa.sh` · 원인 찾기 `diag.js` · `diag2.js` · 캡처 `cap.js`).
- 로컬 CI 도구: `/Users/jackson/Hub/10_Dev/claude-plugins/.harness/handoff/2026-09-26-tools/ci-local.sh` — 실제 CI 의 `run-kaizen-assertions.py` 단계가 이 도구에 없다(VS-24). DG-05 의 통과는 그 단계를 뺀 통과다.

캡처 폴더: `/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/bda55d45-296c-491f-89ba-b52042d58e72/scratchpad/dca2/cap`

## DC-9 매핑 규칙 결정

도우미 `maplist` 가 시작 판 `6378948` 에서 뽑은 66 경로(짝 원본 없는 등록 페이지 23 · 없는 페이지를 가리키는 원본 43)의 결정이다. 매핑 표(`.claude/skills/docs-site/SKILL.md:45-64`)와 `scripts/detect-docs-drift.py` 는 고치지 않았다 — VS-13 묶음이 이 표를 옮겨 같은 커밋에서 둘 다 고친다.

결정 낱말의 뜻: `원본:` 이 페이지를 만든 원본 파일, `원본 없음` 원본 없이 만든 페이지라 드리프트 검사에서 뺀다, `새 페이지` 원본마다 한 페이지 원칙(Gotcha 7)대로 페이지를 새로 만든다, `짝:` 이름이 다른 기존 페이지와 짝을 짓는다, `페이지 없음이 맞음` 페이지를 만들지 않는 원본이다.

| 경로 | 결정 | 근거 |
| --- | --- | --- |
| `docs/backend-kit/backend-test.html` | 원본: `backend-kit/skills/backend-test/SKILL.md` | 페이지 제목과 스킬 이름이 같고 표의 backend-kit 행은 리서치 폴더만 적어 스킬 원본이 빠졌다 |
| `docs/backend-kit/write-path-integrity.html` | 원본: `backend-kit/references/write-path-integrity-protocol.md` | 같은 이름의 참조 문서가 킷에 있고 표의 backend-kit 행에 참조 폴더가 없어서 놓쳤다 |
| `docs/design-kit/design-component.html` | 원본: `design-kit/skills/design-component/SKILL.md` | 페이지가 스킬 한 개를 설명하는데 표는 design-test 스킬만 원본으로 적었다 |
| `docs/design-kit/design-concept.html` | 원본: `design-kit/skills/design-concept/SKILL.md` | 페이지가 스킬 한 개를 설명하는데 표는 design-test 스킬만 원본으로 적었다 |
| `docs/design-kit/design-mockup.html` | 원본: `design-kit/skills/design-mockup/SKILL.md` | 목록 VS-13 이 이 짝이 빠졌다고 적었고 페이지가 스킬 절차를 옮긴 것이다 |
| `docs/design-kit/design-reference.html` | 원본: `design-kit/skills/design-reference/SKILL.md` | 페이지가 스킬 한 개를 설명하는데 표는 design-test 스킬만 원본으로 적었다 |
| `docs/design-kit/design-template.html` | 원본: `design-kit/templates/base.html` | 페이지가 이 틀 파일 이름을 본문에 적고 틀의 규약을 풀어 쓴다 |
| `docs/design-kit/examples/moodboard-taskflow.html` | 원본 없음 | 스킬이 만든 결과물 예시 한 장이라 따라 갈 원본 문서가 없다 |
| `docs/flutter-toolkit/flutter-patterns.html` | 원본 없음 | 첫 판(ef41bdd)부터 여러 문서를 모은 개요 페이지라 원본 한 개로 좁힐 수 없다 |
| `docs/harness/feedback-system.html` | 짝: `harness/references/feedback-schema.yaml` | 페이지가 피드백 틀을 설명하고 이 원본이 가리키는 페이지 이름만 다르다 |
| `docs/howto-kit/overview.html` | 짝: `docs/howto/design-brief.md` | 킷 설계 기록을 개요 페이지로 만든 것이라 두 이름을 짝으로 묶는다 |
| `docs/infra-kit/gate-result-taxonomy.html` | 원본: `infra-kit/references/gate-result-taxonomy.md` | 같은 이름의 참조 문서가 있고 표의 infra-kit 행에 참조 폴더가 없어서 놓쳤다 |
| `docs/infra-kit/infra-test.html` | 원본: `infra-kit/skills/infra-test/SKILL.md` | 목록 VS-13 이 이 짝이 빠졌다고 적었고 페이지가 스킬 절차를 옮긴 것이다 |
| `docs/process/create-kit-flow.html` | 원본: `.claude/skills/create-kit/SKILL.md` | 새 킷 만들기 절차를 그린 페이지이고 그 절차의 원문이 이 스킬이다 |
| `docs/process/kaizen-flow.html` | 원본: `.claude/skills/kaizen-orchestrator/SKILL.md` | 카이젠 단계 흐름을 그린 페이지이고 그 단계의 원문이 오케스트레이터 스킬이다 |
| `docs/react-kit/animation.html` | 짝: `docs/react/kit-design/g5b-animation.md` | 킷 설계 기록 한 편이 페이지 한 쪽이 됐고 이름 앞머리만 다르다 |
| `docs/react-kit/build-audit.html` | 짝: `docs/react/kit-design/g6-build-audit.md` | 킷 설계 기록 한 편이 페이지 한 쪽이 됐고 이름 앞머리만 다르다 |
| `docs/react-kit/integration.html` | 짝: `docs/react/kit-design/final-integration.md` | 마지막 통합 설계 기록이 통합 페이지가 됐고 이름 앞머리만 다르다 |
| `docs/react-kit/performance.html` | 짝: `docs/react/kit-design/g3-performance.md` | 킷 설계 기록 한 편이 페이지 한 쪽이 됐고 이름 앞머리만 다르다 |
| `docs/react-kit/quality.html` | 짝: `docs/react/kit-design/g4-quality.md` | 킷 설계 기록 한 편이 페이지 한 쪽이 됐고 이름 앞머리만 다르다 |
| `docs/react-kit/scaffolding.html` | 짝: `docs/react/kit-design/g1-scaffolding.md` | 킷 설계 기록 한 편이 페이지 한 쪽이 됐고 이름 앞머리만 다르다 |
| `docs/react-kit/state-data.html` | 짝: `docs/react/kit-design/g2-state-data.md` | 킷 설계 기록 한 편이 페이지 한 쪽이 됐고 이름 앞머리만 다르다 |
| `docs/react-kit/ui-patterns.html` | 짝: `docs/react/kit-design/g5-ui-patterns.md` | 킷 설계 기록 한 편이 페이지 한 쪽이 됐고 이름 앞머리만 다르다 |
| `bambu-kit/skills/bambu-print-profile/references/comment-analysis.md` | 새 페이지 | 같은 폴더의 다른 참조 문서는 모두 페이지가 있어 한 문서 한 페이지 원칙을 따른다 |
| `bambu-kit/skills/bambu-print-profile/references/tolerance.md` | 새 페이지 | 같은 폴더의 다른 참조 문서는 모두 페이지가 있어 한 문서 한 페이지 원칙을 따른다 |
| `bambu-kit/skills/bambu-print-profile/references/user-preferences.md` | 새 페이지 | 같은 폴더의 다른 참조 문서는 모두 페이지가 있어 한 문서 한 페이지 원칙을 따른다 |
| `docs/api/research-log.md` | 페이지 없음이 맞음 | 조사 기록은 날짜별 작업 기록이라 읽을 문서로 만들지 않는다 — 다른 킷도 조사 기록 페이지가 없다 |
| `docs/backend/research-log.md` | 페이지 없음이 맞음 | 조사 기록은 날짜별 작업 기록이라 읽을 문서로 만들지 않는다 — 다른 킷도 조사 기록 페이지가 없다 |
| `docs/flutter/research-log.md` | 페이지 없음이 맞음 | 조사 기록은 날짜별 작업 기록이라 읽을 문서로 만들지 않는다 — 다른 킷도 조사 기록 페이지가 없다 |
| `docs/howto/design-brief.md` | 짝: `docs/howto-kit/overview.html` | 킷 설계 기록을 개요 페이지로 만든 것이라 두 이름을 짝으로 묶는다 |
| `docs/infra/research-log.md` | 페이지 없음이 맞음 | 조사 기록은 날짜별 작업 기록이라 읽을 문서로 만들지 않는다 — 다른 킷도 조사 기록 페이지가 없다 |
| `docs/planning/research-log.md` | 페이지 없음이 맞음 | 조사 기록은 날짜별 작업 기록이라 읽을 문서로 만들지 않는다 — 다른 킷도 조사 기록 페이지가 없다 |
| `docs/react/kit-design/final-integration.md` | 짝: `docs/react-kit/integration.html` | 마지막 통합 설계 기록이 통합 페이지가 됐고 이름 앞머리만 다르다 |
| `docs/react/kit-design/g1-scaffolding.md` | 짝: `docs/react-kit/scaffolding.html` | 설계 기록 한 편이 페이지 한 쪽이 됐고 이름 앞머리만 다르다 |
| `docs/react/kit-design/g2-state-data.md` | 짝: `docs/react-kit/state-data.html` | 설계 기록 한 편이 페이지 한 쪽이 됐고 이름 앞머리만 다르다 |
| `docs/react/kit-design/g3-performance.md` | 짝: `docs/react-kit/performance.html` | 설계 기록 한 편이 페이지 한 쪽이 됐고 이름 앞머리만 다르다 |
| `docs/react/kit-design/g4-quality.md` | 짝: `docs/react-kit/quality.html` | 설계 기록 한 편이 페이지 한 쪽이 됐고 이름 앞머리만 다르다 |
| `docs/react/kit-design/g5-ui-patterns.md` | 짝: `docs/react-kit/ui-patterns.html` | 설계 기록 한 편이 페이지 한 쪽이 됐고 이름 앞머리만 다르다 |
| `docs/react/kit-design/g5b-animation.md` | 짝: `docs/react-kit/animation.html` | 설계 기록 한 편이 페이지 한 쪽이 됐고 이름 앞머리만 다르다 |
| `docs/react/kit-design/g6-build-audit.md` | 짝: `docs/react-kit/build-audit.html` | 설계 기록 한 편이 페이지 한 쪽이 됐고 이름 앞머리만 다르다 |
| `docs/react/research-log.md` | 페이지 없음이 맞음 | 조사 기록은 날짜별 작업 기록이라 읽을 문서로 만들지 않는다 — 다른 킷도 조사 기록 페이지가 없다 |
| `docs/rust/research-log.md` | 페이지 없음이 맞음 | 조사 기록은 날짜별 작업 기록이라 읽을 문서로 만들지 않는다 — 다른 킷도 조사 기록 페이지가 없다 |
| `docs/tone/research-log.md` | 페이지 없음이 맞음 | 레포 안내(`CLAUDE.md`)가 tone 리서치 문서 여덟 종을 셀 때 조사 기록을 뺀다고 적었다 |
| `flutter-toolkit/references/figma-parity-self-verify.md` | 새 페이지 | 같은 폴더의 다른 참조 문서 넷은 모두 같은 이름의 페이지가 있어 원칙을 따른다 |
| `harness/references/cross-kit-principles.md` | 새 페이지 | 표의 harness 행이 참조 폴더를 원본으로 적었고 이 문서만 페이지가 없다 |
| `harness/references/feedback-schema.yaml` | 짝: `docs/harness/feedback-system.html` | 피드백 틀을 설명하는 페이지가 이미 있고 이름만 다르다 |
| `react-kit/references/clean-arch-layout.md` | 새 페이지 | 표의 react-kit 행이 참조 폴더를 원본으로 적었고 같은 폴더의 두 문서는 페이지가 있다 |
| `react-kit/references/common-gotchas.md` | 새 페이지 | 표의 react-kit 행이 참조 폴더를 원본으로 적었고 같은 폴더의 두 문서는 페이지가 있다 |
| `react-kit/references/project-detection.md` | 새 페이지 | flutter · onboarding 의 같은 이름 참조 문서가 모두 페이지를 가져 같은 원칙을 따른다 |
| `react-kit/references/result-patterns.md` | 새 페이지 | 표의 react-kit 행이 참조 폴더를 원본으로 적었고 같은 폴더의 두 문서는 페이지가 있다 |
| `react-kit/references/style-guide.md` | 새 페이지 | 표의 react-kit 행이 참조 폴더를 원본으로 적었고 같은 폴더의 두 문서는 페이지가 있다 |
| `reflect-kit/references/memory-grounding.md` | 새 페이지 | 표의 reflect-kit 행이 참조 폴더를 원본으로 적었고 이 문서만 페이지가 없다 |
| `reflect-kit/skills/codex-kaizen/references/search-sources.md` | 짝: `docs/reflect-kit/codex-kaizen.html` | 스킬의 부속 목록이라 따로 쪽을 만들지 않고 그 스킬 페이지에 묶는다 |
| `reflect-kit/skills/reflect-digest/SKILL.md` | 새 페이지 | 표의 reflect-kit 행이 스킬 폴더를 원본으로 적었고 스킬마다 한 페이지 원칙을 따른다 |
| `reflect-kit/skills/reflect-kaizen/SKILL.md` | 새 페이지 | 표의 reflect-kit 행이 스킬 폴더를 원본으로 적었고 스킬마다 한 페이지 원칙을 따른다 |
| `reflect-kit/skills/reflect-promote/SKILL.md` | 새 페이지 | 표의 reflect-kit 행이 스킬 폴더를 원본으로 적었고 스킬마다 한 페이지 원칙을 따른다 |
| `rust-kit/references/project-detection.md` | 새 페이지 | flutter · onboarding 의 같은 이름 참조 문서가 모두 페이지를 가져 같은 원칙을 따른다 |
| `tone-kit/references/adapter-contract.md` | 페이지 없음이 맞음 | 킷 안에서 규칙 파일끼리 맞추는 약속이라 사람이 읽을 페이지로 만들지 않는다 |
| `tone-kit/references/adapter-dart-flutter.md` | 짝: `docs/tone-kit/dart-flutter-idioms.html` | 같은 주제 페이지가 이미 있어 원본을 하나 더 거는 것으로 충분하다 |
| `tone-kit/references/core-antipatterns.md` | 짝: `docs/tone-kit/antipattern-catalog.html` | 같은 주제 페이지가 이미 있어 원본을 하나 더 거는 것으로 충분하다 |
| `tone-kit/references/core-comment.md` | 짝: `docs/tone-kit/comment-economy.html` | 같은 주제 페이지가 이미 있어 원본을 하나 더 거는 것으로 충분하다 |
| `tone-kit/references/core-naming.md` | 짝: `docs/tone-kit/naming-taxonomy.html` | 같은 주제 페이지가 이미 있어 원본을 하나 더 거는 것으로 충분하다 |
| `tone-kit/references/core-structure.md` | 짝: `docs/tone-kit/extraction-thresholds.html` | 같은 주제 페이지가 이미 있어 원본을 하나 더 거는 것으로 충분하다 |
| `tone-kit/references/locale-korean.md` | 짝: `docs/tone-kit/korean-technical-writing.html` | 같은 주제 페이지가 이미 있어 원본을 하나 더 거는 것으로 충분하다 |
| `tone-kit/references/project-detection.md` | 페이지 없음이 맞음 | 스킬이 프로젝트 값을 찾는 절차라 킷 안에서만 쓰고 사람이 읽을 페이지로 만들지 않는다 |
| `tone-kit/references/sources.md` | 페이지 없음이 맞음 | 출처 목록이라 각 주제 페이지 끝의 출처 칸이 이미 같은 일을 한다 |
| `process (공유)` 행 | 원본: `.claude/skills/kaizen-orchestrator/SKILL.md` · `.claude/skills/create-kit/SKILL.md` | 표의 원본 칸이 「(내부 문서)」 라 드리프트 도구가 짝을 못 짓는다 — 두 스킬로 채운다 |

## 남은 것

- 개정 A-01(동의 대기): `docs/tone-kit/dart-flutter-idioms.html` 이 320 폭에서 `.detail li` 목록 줄이 상자 밖으로 나간다. 고치려면 그 쪽 CSS 두 줄을 바꿔야 하는데
  AR-02 가 그 쪽의 바뀐 줄을 DC-7 한 줄로 묶어 두었다. 두 개정 모두 조건을 느슨하게 하는 쪽이라 위임으로 처리하지 않았다 — 부모가 사용자에게 물은 뒤 옵션 1 이면 개정 파일의 두 줄 판을 넣어 커밋한다.
  그 전까지 ER-01 · ER-02 는 이 한 쪽 때문에 176/177 이다.
- 검사기 단추 id: `scripts/check-docs-a11y.js:133` 이 `#theme-btn` 만 찾아 틀(`themeToggle`)로 만든 쪽의 단추 크기를 못 잰다. 검사 도구를 고치는 일이라 vs 묶음에 넘긴다.
- KD-2(디자인 감사 기준의 행간 1.2~1.6)와 VS-18(오케스트레이터의 「standalone」)은 각각 design-kit 묶음 · vs 묶음 몫이다. 이 묶음이 `SKILL.md` 쪽 두 표기를 고쳤으니 두 곳만 남았다.
