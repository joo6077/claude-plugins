---
feature: "킷 남은 것 — reflect-kit · bambu-kit · tone-kit (카이젠 뒤 이어질 것 2026-09-26 두 번째 묶음 k3) 2 회차 계약"
slug: after-0926-kits-reflect-bambu-tone-r2
created: "2026-09-27 12:15"
complexity: "복잡"
conditions: 32
status: active
owner_session: bda55d45-296c-491f-89ba-b52042d58e72
conditions_digest: sha256:9ee4c5cccc722588
measurement_digest: sha256:69bb247ef8d5b16a
locked_at: "2026-09-27 12:24"
---

## 배경

### 2 회차 계약을 쓴 까닭

- 1 회차 계약: `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak2-k3/.harness/sprint-contract-after-0926-kits-reflect-bambu-tone.md`
  (봉인 `sha256:94c9205998801dd1` · 봉인 커밋 `1db0437`, 이제 `status: superseded`). 1 회차 QA 리포트 `sprint-feedback-after-0926-kits-reflect-bambu-tone.md`
  (REJECT, 28/32 · N/A 3 · FAIL 1)는 커밋 `7f0a203` 에 그대로 남겼다.
- 틀린 측정: SC-05 측정 첫 줄의 기대 `mut=4`. `mut` 는 SKILL.md 사본에서 `/Applications/` 를 `/nonexistent-apps/` 로 바꾼 뒤 `nonexistent-apps` 가 든 줄 수다.
  시작 판 `6378948` 에서도, 가지 끝에서도 **10** 이다 — 이 작업은 `/Applications/` 가 든 줄을 더하거나 빼지 않았다. `4` 는 봉인 전에 잰 적이 없는 값이라,
  원래 조건은 구현과 상관없이 통과할 수 없었다(통과 집합이 비었다).
- 바로잡은 것: SC-05 측정 기대를 `mut=10` 으로 적고, 봉인 전에 시작 판 · 가지 끝에서 돌린 값과 구현을 되돌린 사본의 음성 대조(`m SC-05N`)를 붙였다.
  나머지 31 조건의 문구와 측정은 1 회차와 같은 뜻 그대로 옮겼다.
- 1 회차 개정 A-01(`mut=4` → `mut=10`, `relaxing`)은 사용자 동의를 받지 않은 채 1 회차 개정 파일에 그대로 남긴다. 이 2 회차 계약은 그 개정을 근거로 쓰지 않는다 —
  결정 파일(`.../after-kaizen-0926b/decisions.md`) 「추가 위임」 절이 정한 대로, 봉인된 측정이 처음부터 틀렸으면 새 판 계약을 다시 봉인한다.
- 2 회차 산출물 때문에 따라 바꾼 곳: AR-01 의 기대 집합(도우미 `ALLOWED`)에 2 회차 산출물 세 경로(`sprint-contract-…-r2.md` · `sprint-feedback-…-r2.md` ·
  `sprint-amendments-…-r2.md`)를 더해 스물일곱 경로가 됐다. 이 계약 파일 자체가 가지 차이에 들어가므로 빼면 AR-01 이 구현과 상관없이 FAIL 한다.
  1 회차 세 경로는 그대로 둔다. 도우미 머리 이름표도 2 회차 슬러그로 바꿨다.
- 봉인 전 재측정: 1 회차 계약에 `status: superseded` 를 적은 커밋 `e52318f` 를 끝점으로 이 계약의 도우미를 bash 에서 source 해 DG-05 를 뺀 전 조건을 돌렸다.
  SC-05 는 위 값 그대로(`mut=10 … match=8 bad=0 skip=16 skip_named=16`), 나머지 조건 값은 1 회차 QA 리포트 값과 같다(AR-01 `changed=24 extra=0 multi_top=0`).
  1 회차 계약 파일에는 frontmatter 바로 아래 한 줄로 이 계약 이름을 적었다(스키마에 가리키는 필드가 없어 frontmatter 밖 본문 첫 줄에 둔다). 조건 줄은 건드리지 않아 봉인 값은 `94c9205998801dd1` 그대로다.
- 교차 진단 지적(봉인 전): 1 회차의 `status: superseded` 는 스키마 값(`active` · `done`) 밖이다. 평가자 규칙에 있는 `supersedes_digest` · `supersedes_commit` 은
  **같은 계약 파일을 다시 봉인했을 때** 그 교체를 적는 칸이라(`harness/agents/qa-evaluator.md` 1-e-3), 파일이 다른 이 2 회차 계약에는 쓰지 않는다.
  `contract-schema.md` 에는 두 칸도, 「다음 판 계약」 을 가리키는 칸도 없다 — 새 판 계약을 가리키는 정식 자리를 스키마에 두는 일은 다음 카이젠 후보로 notes 에 남긴다.
  평가자 고르기 규칙에서 1 회차는 옛 형식으로 빠지고, 이 세션이 소유한 활성 계약은 이 파일 하나라 평가 대상이 갈리지 않는다.

### 1 회차 배경 (그대로 옮김)

2026-09-24 카이젠 뒤에 남은 일 가운데 세 킷(reflect-kit · bambu-kit · tone-kit) 몫을 한 계약으로 묶는다.
입력은 통합 폴더(읽기만) `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0926b` 의 `.harness/.meta/after-kaizen-0926b/leftovers.md`
「## kit-reflect-kit」 KRf-1~KRf-5 · 「## kit-bambu-kit」 KBa-1~KBa-4 · 「## kit-tone-kit」 KT-1~KT-3 과 같은 폴더 `decisions.md` 다.

- 사용자 합의(Step 5): 위임으로 받은 것으로 적는다 — 세션 `bda55d45-296c-491f-89ba-b52042d58e72`, 위임 2026-09-26T10:09:00.557Z 「123다실행해 그러면끝나?다음카이젠에왜넘기는데?」,
  결정 답 2026-09-26T10:30:16.222Z. 그 앞의 위임 2026-09-24T04:04:16.964Z 「나한테 물어보지 말고 자동으로 끝까지」. 사용자에게 묻지 않았다.
  봉인된 조건을 느슨하게 하는 개정(허용 파일 늘리기 · 측정 대상 줄이기 · 문턱 낮추기)은 이 위임으로 동의 처리하지 않는다 — 개정 파일에 동의 칸을 비워 두고 부모에게 넘긴다.
- 작업 폴더 W = `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak2-k3`, 가지 `chore/ak2-k3`, 시작점 `6378948`(origin/main, #119).
  시작할 때 W 에는 앞 워크플로가 선점만 하고 멈춘 0 바이트 계약 파일(1 회차 계약 파일) 하나만 추적 밖으로 있었다 — 커밋 0 개, QA 리포트 없음. 같은 세션이 남긴 선점이라 이어서 썼다.
- 커밋 규칙: `git add <경로>` 뒤 `git commit -o <경로>` · 한 커밋에 맨 위 자리 하나(reflect-kit · bambu-kit · tone-kit · `docs/tone` · `docs/tone-kit` · `.github` · `.harness` 가운데 하나 — 세 킷은 각각 따로) · `git add -A` · `git stash` · push · 가지 바꾸기 금지.
- 구현 전에 `tone-kit:tone-guide` 1 단계(규칙 불러오기)를, 완료 선언 전에 5 단계(전수 대조)를 한다 — 대조 결과는 notes 에 남긴다(AR-02).
- 도구를 숨기거나 가짜 도구를 만드는 대조(가짜 codex · 가짜 curl · 슬라이서 경로 바꾼 사본)는 임시 폴더에 새 일반 파일로만 만든다. 진짜 도구를 가리키는 바로가기를 만든 자리에 쓰지 않는다.
- 다른 묶음이 같은 파일을 고칠 수 있다. 바꿀 줄은 최소로 하고 이 계약 항목에 없는 절은 건드리지 않는다. 기존 마크다운 경고 정리(VS-26)는 부모 몫이라 더해진 줄의 새 경고만 잰다(DG-02).
- 사용자가 할 일: 없음.

복잡도 4 축 — 넷 다 「예」 이고 공개 약속 변경과 소비자가 함께 있어 「복잡」 이다. Step 2.5 짝 조건: SC-01(훅 ↔ 훅 시험) · SC-02(라이브러리 ↔ 수집 상태 시험) ·
SC-03 ↔ SC-04 · SC-05(완료 검사 ↔ 새 실행 스크립트) · SK-05(실행 스크립트 ↔ CI) · SC-07 · ER-02(받는 법 블록 ↔ 새 시험) · SK-09(원본 문서 ↔ 문서 사이트 페이지 머리) · SK-10(원본 문서 ↔ 페이지 본문).

| 축 | 물음 | 값 |
| -- | ---- | -- |
| 레이어 수 | 몇 개 계층을 관통하는가 | 넷 — 훅 셸 스크립트 · 스킬 문서 안 실행 블록(완료 검사 · 받는 법) · 시험 스크립트와 CI · 참조 문서와 문서 사이트 페이지 |
| 공개 API·계약 변경 | 외부에 노출된 약속이 바뀌는가 | 예 — Stop 훅이 분석기에 넘기는 입력(마지막 응답), 완료 검사의 종류 판정 동작과 `[미검증]` 문구, 받는 법 블록 출력(답글 수), 새 실행 스크립트의 출력 형식 · 종료 코드 |
| 소비면 존재 | 반대편이 있는가 | 예 — reflect 시험 둘 · reflect-digest 수집 상태 절, 음성 대조 블록 · CI, `docs/tone-kit/*.html` 페이지 |
| 회귀 위험 | 기존 동작이 깨질 수 있는가 | 예 — reflect 시험 32 · 18 · 16 경우, 완료 검사 시험 파일 23 개, 로컬 CI 25 단계 |

설정 값 대조 (`.harness/project.yaml` 을 글자 그대로 옮김):

| config key | project.yaml 에서 읽은 값 | 계약에 쓴 값 |
| ---------- | ------------------------- | ------------ |
| `commands.analyze` | `bash -n scripts/release.sh` | DG-01 N/A — 재는 파일이 바뀐 파일에 없다 |
| `commands.test` | `bash scripts/release.sh 2>&1 \|\| true` | DG-03 N/A — 같은 이유 |
| `diagnostics.ide_exclude` | `[]` | DG-02 의 `([] 제외)` |
| `contract_categories[].id` / `prefix` | Skill/SK · Script/SC · Error/ER · Architecture/AR | 같은 넷 |
| `anti_patterns[].id` / `message` | AP-01 버전 하드코딩 · AP-02 force push · AP-03 bare code fence · AP-04 frontmatter name 누락 | AP-03 · AP-04 (바뀌는 파일이 코드 블록 많은 SKILL.md · 참조 문서라 걸릴 수 있다). AP-01 은 `plugin.json` 버전을 안 건드려서, AP-02 는 이 계약이 push 하지 않아서 뺐다 |

## 리서치 소스

바깥 사실은 Codex 가 원문을 인용해 둔 대조 결과 둘(통합 폴더 `.harness/.meta/after-kaizen-0926b/ex/`, 읽기만)과, 이 계약을 쓰며 이 맥에서 직접 관측한 값만 쓴다.
여기 없는 바깥 사실은 새로 찾지 않고 「바깥 근거 없음」 으로 notes 에 적는다.

- EX-1 (`.../ex/EX-1.md`) — <https://code.claude.com/docs/en/hooks>. 「In shell form, wrap each placeholder in double quotes.」(#reference-scripts-by-path),
  Stop · SubagentStop 입력의 `last_assistant_message` 는 「text content of Claude's final response」(#stop-input · #subagentstop-input),
  「By default, hooks block Claude's execution until they complete.」 — `async: true` 는 command 훅 전용이고 생략하면 끝날 때까지 기다린다(#command-hook-fields · #run-hooks-in-the-background)
- EX-14 (`.../ex/EX-14.md`) — Flutter 릴리스 목록 <https://storage.googleapis.com/flutter_infra_release/releases/releases_macos.json> 3.47.5(Dart 3.13.4, 2026-09-18) · 3.38.4,
  두 판의 `gesture_detector.dart` 콜백 58 개로 같음(정렬 목록 SHA-256 같음), go_router 최신 18.0.1(2026-09-02, <https://pub.dev/api/packages/go_router>),
  CHANGELOG 17.0.0 「BREAKING CHANGE」 · 18.0.0 「Migrates to material_ui and cupertino_ui.」, 위키 스타일 가이드가
  <https://github.com/flutter/flutter/blob/main/docs/contributing/Style-guide-for-Flutter-repo.md> 로 이전(1,867 줄 수치는 틀림 — 저장소 안에 그 수치는 0 곳)
- 이 맥 관측(2026-09-27, 계약 작성자) — 뱀부 릴리스 <https://api.github.com/repos/bambulab/BambuStudio/releases>: `v02.08.04.57` 2.8.4 Public Beta 2026-09-22 ·
  `v02.08.03.66` Beta 2026-09-08 · `v02.08.02.61` Public Release 2026-08-21. 설치본 뱀부 `02.08.02.61` 번들에 `Bambu PLA Pure @BBL H2S*.json` 4 개.
  MakerWorld 댓글 주소(`designId=1186414`) 응답: 답글 배열은 `comment.commentReply`, 답글 수는 `comment.replyCount`. 댓글 159 개에서 `replyCount` 합 25 · 받은 `commentReply` 합 24(한 댓글은 배열이 수보다 짧다)
- 이 맥 관측(2026-09-27) — `~/.claude/logs/*/.errors.log` 의 `[log-reflection]` 줄 가운데 `err=` 가 붙은 줄 0. 2026-09-26 19:09 의 `fail:codex-exit-2` · `fallback:claude-exit-1` 은
  세션 `d204ea78`(2026-09-22 시작) 것이고 두 줄 다 `err=` 가 없다. `err=` 를 적기 시작한 판은 0.8.0 이다(설치본 캐시 0.7.1 은 `err=` 0 줄 · `--full-auto` 인자 · `haiku-4.5`, 0.8.0 은 `err=` 5 줄)

## GAP 분석 (Pre-Edit Audit)

줄 번호는 시작 판 `6378948` 이다. 모두 이 계약을 쓰며 파일을 직접 열어 확인했다.

| 대상 파일 | 실제 Read 증거 (`파일:라인`) | 발견한 기존 갭·위반 | 계약 조건화 여부 |
| --------- | ---------------------------- | ------------------- | ---------------- |
| `reflect-kit/skills/reflect-digest/SKILL.md` | `:255` · `:315` 「엔트리 0 이고 Stop 실패 시도가 1 이상일 때」, 코드 `hooks/_lib-project-id.sh:199-221`(`e==0 && a>0`, `a` 는 마지막 기록 · 마지막 정상 종료 가운데 늦은 쪽 뒤의 실패) | 글과 코드가 다르다 — 시험 「엔트리 0 · 실패 뒤 정상 종료 — 경고 없음」 이 증거 | SK-01 |
| 같은 파일 Gotchas `:35` (#13) | `err=` 값을 환경 액션에 올리라는 말만 있고, `err=` 없는 실패 줄이 옛 판 세션이라는 말이 없다 | KRf-5 조사 결과를 한 문장으로 | SK-04 |
| `reflect-kit/hooks/log-reflection.sh` | `:6-7` 「plugin spec의 async 필드에 의존하지 않는다」, `:250` 「`claude -p --model haiku`로 재시도」, 실제 호출 `:269` `claude -p --safe-mode --model haiku` | 주석 둘이 사실과 다르다(EX-1 은 `async` 가 있다고 한다) | SK-02 |
| 같은 파일 `:55-57` · `:86` · `:229-231` | 입력에서 `cwd` · `transcript_path` · `session_id` 만 읽는다. 프롬프트의 `<transcript>` 는 transcript 끝 150 줄 | 마지막 응답이 transcript 에 아직 없을 수 있다(EX-1 · `evidence/phase12.md:50`) | SC-01 |
| `reflect-kit/hooks/_lib-project-id.sh` | `:229-233` 머리 주석 「그 세션은 all 에서만 보인다」, `:261` `basename "$(project_root "$pp")"`, 비교 대상 `scripts/collect-kaizen-data.py:420-421` | 지운 워크트리 경로가 폴더 이름으로 남아 프로젝트별 대조에서 빠진다 | SC-02 |
| `reflect-kit/README.md` | `:156` · `:159` · `:162` `bash ${CLAUDE_PLUGIN_ROOT}/scripts/install-scheduler.sh` | 따옴표 없음(EX-1 「wrap each placeholder in double quotes」) | SK-03 |
| `reflect-kit/evals/hooks/log-reflection-test.sh` · `collect-status-test.sh` | `:5` `REFLECT_KIT_HOOKS` · `:5` `PROJECT_ID_LIB` 사본 경로, 결과 줄 `결과: N 경우 중 불일치 M`(시작 판 32 · 18) | 새 동작 두 가지를 재는 경우가 없다 | SC-01 · SC-02 |
| `bambu-kit/skills/bambu-print-profile/SKILL.md` 완료 검사 | `:1604-1611`(`skipped` 문구), `:1701` `elif t not in TYPES…` 가 enum 판정 `:1704` 보다 먼저 | 종류 줄이 빠진 목록이면 키 9 개 모두 거짓 「키 스코프 불일치」 FAIL, enum FAIL 0(봉인 전 재현) | SC-03 |
| 같은 파일 `:2037-2041` 설명 문단 · `:1886-2019` 음성 대조 블록 | 「종류 줄이 없어 … 믿지 마라」 전제, 종류 줄 빠진 목록 변이 없음. `:1889` `mktemp -t gate` · `:2010` · `:2015` 가 임시 파일 18 개를 남긴다(봉인 전 실측) | 판정 동작을 고치면 문단 · 변이도 따라야 한다 | SC-03 · SC-08 |
| 같은 파일 `:1846` 표 머리 · `:1918-1941` 실행 줄 | 완료 검사를 돌리는 실행 목록이 SKILL.md 안 블록뿐 · 금지 키 FAIL 시험 파일 0(`:1846` 「아직 FAIL 시험 파일이 없다」) | CI 가 시험 파일을 안 돌린다 | SC-04 · SC-05 · SC-06 · SK-05 |
| 같은 파일 `:920` · `:1186` · `:1323` · `:1831`, `references/failure-recipes.md:150` | `[미검증]` 만 적고 네 칸(`harness/docs/guides/skill-design-guide.md:302-308`)이 없다 — 옛 판(`499cc12`)의 `:806` · `:1072` · `:1209` · `:1706` · `:150` 과 같은 문장 | 생성 측 다섯 자리 | SK-06 |
| 같은 파일 `:2548` 릴리스 현황 · `references/bambu-fields-baseline.md:10` · `:16-17` · `references/materials.md:140` | 최신 beta 2.8.1 · 안정 2.7.1 · 로컬 02.06.00.51 · 「PLA Pure 2.6.0 stable 미포함」 | 이 맥 관측값과 다르다 | SK-07 |
| 같은 파일 `:2460-2523` 받는 법 | 표 `:2469` 댓글 행에 답글 필드가 없다, 블록은 `hits` 만 센다. 모델 주소 403 이면 `design.json` 이 HTML 이라 `FAIL design.json …` · 종료 코드 1(봉인 전 가짜 curl 로 실측) | 답글 수를 못 센다 · 403 경우를 재는 시험이 없다 | SC-07 · ER-02 |
| `.github/workflows/ci.yml` | `:109` 마지막 validate 단계(Design-kit decision gate test). bambu-kit 단계 0 | 새 스크립트 두 개를 돌릴 자리 | SK-05 |
| `tone-kit/references/adapter-dart-flutter.md` | `:26` 「정규식은 §4 완료 게이트 G-04 줄이 정본이다」, 실제 정규식 `:245`(§4 `text` 블록 넷째 줄), `:259` G-04 는 정규식 없는 표 행 | 가리키는 줄이 다르다 | SK-08 |
| `docs/tone/dart-flutter-idioms.md` · `docs/tone-kit/dart-flutter-idioms.html` | md `:3-4` `version: 0.1.0` · `last_updated: 2026-09-02`, 그 뒤 원본 커밋 셋(`80daceb` · `358f8e1` · `b367184`). html `:275` · `:1571` 같은 판 | 머리 판이 안 올랐다 | SK-09 |
| 3.38.4 표기 다섯 파일 | `adapter-dart-flutter.md:180` · `:235`, `dart-flutter-idioms.md:618` · `:686`, `naming-taxonomy.md:103` · `:127` · `:401`, html 두 페이지 7 줄 — 3.47.5 를 적은 줄 0(봉인 전 14 줄) | EX-14: 두 판 모두 58 개 | SK-10 |
| `tone-kit/references/sources.md` | `:97` 「위 표의 마지막 세 행」, `:143` go_router 16.3.0 예제, `:157` 위키 주소 「주의 (위키 이전 이력 있음)」 | 행이 늘면 틀리는 지칭 · 옛 판 · 옛 주소 | SK-11 |

다른 세션 가지 `feat/bambu-kit-orca-h2s-feedback`(KBa-3, 끝 `42209be`, 기준 `baa1a38`)은 읽기만 했다. `git merge-tree --write-tree origin/main feat/bambu-kit-orca-h2s-feedback` 로
본 충돌 자리는 SKILL.md 다섯 곳 — 시작 판 `:1836-1846`(음성 대조 머리글) · `:1854-1872`(시험 파일 표) · `:1923-1941`(실행 줄) · `:1956-1985`(지운 사본 줄) · `:2443-2444`(점검 목록)와
`docs/bambu-kit/bambu-print-profile.html` 이다. 이 계약의 SC-03 · SC-06 · SC-08 이 앞 네 곳에 줄을 더하므로 그 가지를 합칠 때 충돌 줄이 는다 — notes 에 자리를 적는다(AR-02).

## Skill

- [ ] SK-01: reflect-digest 의 `⚠ 수집 멈춤` 조건 두 줄(시작 판 `:255` 수집 상태 줄 설명 · `:315` 출력 포맷 머리)이 코드와 같은 조건을 적는다 — 옛 구절 「엔트리 0 이고 Stop 실패 시도가 1 이상일 때」 가 0 줄이고, 새 구절 「엔트리 0 이고 마지막 정상 종료 뒤의 Stop 실패 시도가 1 이상일 때」 가 2 줄이다 [exact, enumerated]
    측정: `m SK-01` 이 `old=0 new=2` (시작 판 `old=2 new=0` — 양성 대조)
- [ ] SK-02: `log-reflection.sh` 주석 둘이 사실과 같다 — (a) 대체 경로 함수 머리 주석에 옛 글 `claude -p --model haiku` 가 0 줄이고 `#` 로 시작하는 줄에 `claude -p --safe-mode --model haiku` 가 1 줄 이상, (b) 파일 머리(1~12 줄)에서 옛 글 「plugin spec의 async 필드에 의존하지 않는다」 가 0 이고, `async` 와 원문 주소 `code.claude.com/docs/en/hooks` 를 함께 담은 줄이 1 이상이다(EX-1 — command 훅의 `async` 가 있음을 적고 지금은 `nohup` 을 그대로 쓰는 까닭을 적는다). 동작은 그대로다 — `hooks/hooks.json` 은 시작 판과 바이트가 같다 [exact, enumerated]
    측정: `m SK-02` 가 `old_fb=0 new_fb≥1 old_async=0 async_doc≥1 hooks_same=1` (시작 판 `old_fb=1 new_fb=0 old_async=1 async_doc=0 hooks_same=1`)
- [ ] SK-03: `reflect-kit/README.md` 의 `install-scheduler.sh` 예시 세 줄(`--dry-run` · `--install` · `--uninstall`)이 `bash "${CLAUDE_PLUGIN_ROOT}/scripts/install-scheduler.sh"` 꼴이다(EX-1) [exact, enumerated]
    측정: `m SK-03` 이 `bare=0 quoted=3` (시작 판 `bare=3 quoted=0`)
- [ ] SK-04: reflect-digest `## Gotchas` 에 KRf-5 조사 결과 한 줄 — `err=` 가 없는 Stop 실패 줄은 0.8.0 전 판 훅을 쥔 채 켜 둔 세션이 적은 것이라는 설명이, `` `err=` `` · `0.8.0` · `세션` 을 모두 담은 줄로 1 줄 이상 있다. 멈춤 문턱 숫자는 바꾸지 않는다(`collect_status` 는 시험 18 경우가 그대로 통과 — SC-02) [exact, enumerated]
    측정: `m SK-04` 가 1 이상 (시작 판 0)
- [ ] SK-05: CI 가 bambu-kit 시험 스크립트 둘을 한 단계에서 돌린다 — `.github/workflows/ci.yml` 의 `jobs.validate.steps` 가운데 `run` 에 `bambu-kit/evals/run-gate-fixtures.sh` 를 담은 단계가 정확히 1 개이고 그 단계의 `run` 이 `bambu-kit/evals/makerworld-fetch-test.sh` 도 담으며, 워크플로 전체에서 `bambu-kit/evals/` 를 부르는 단계가 그 1 개뿐이다 [exact, enumerated]
    측정: `m SK-05` 가 `gate_steps=1 both=1 all_bambu_steps=1` (시작 판 `0 0 0`). PyYAML 이 없으면 `[미검증] SK-05 yaml_unavailable` · 종료 코드 2 로 멈춘다(FAIL 과 구분). 리눅스 CI 에서의 실제 통과는 SC-05 가 슬라이서 없는 사본으로 대신 잰다
- [ ] SK-06: `[미검증]` 을 적는 생성 측 다섯 자리의 문단이 네 칸을 가리킨다 — 기준 글 `| 둘 다 미설치 |` · `**ER-01 — 버전 조회에 실패하면**` · `부모에 위임하는 쪽이 틀린 숫자보다 안전하다` · `위 명령을 실행하지 않았거나 실행할 수 없었다면`(SKILL.md) · `조회에 실패하면 추측값을 쓰지 말고`(`references/failure-recipes.md`)가 든 문단(그 줄부터 빈 줄 앞까지)마다 「네 칸」 이 있고, 4.3 통과 규칙 문단(넷째 기준 글) 한 줄에 `막는 것` · `시도한 우회` · `통제 불가 사유` · `재검증 명령` · `skill-design-guide.md` 가 함께 있다. 다섯 기준 글은 지우거나 바꾸지 않는다 [exact, enumerated]
    측정: `m SK-06` 이 `spots=5/5 def≥1` (시작 판 `spots=0/5 def=0`, 다섯 자리 모두 miss)
- [ ] SK-07: 뱀부 판 번호 현행화 셋(이 맥 관측 2026-09-27) — (a) `bambu-fields-baseline.md` 1~30 줄의 `Latest beta` 줄에 `v02.08.04.57` · `2026-09-22`, 같은 범위 한 줄에 `v02.08.02.61` · `2026-08-21`, (b) `materials.md` 의 `1. **PLA Pure**` 줄에서 「2.6.0 stable에는 미포함」 이 0 이고 `02.08.02.61` 이 1, (c) SKILL.md `> **릴리스 현황` 줄에 `2026-09-27` · `v02.08.04.57` · `v02.08.02.61` 이 함께 있고 옛 최신 `v02.08.01.55` 가 0 이다 [exact, enumerated]
    측정: `m SK-07` 이 `beta≥1 stable≥1 pure_old=0 pure_new≥1 rel=1 rel_old=0` (시작 판 `beta=0 stable=0 pure_old=1 pure_new=0 rel=0 rel_old=1`)
- [ ] SK-08: tone 어댑터 `fallback_identifier_pattern` 칸이 실제 정규식 자리를 가리킨다 — 그 표 행에 「G-04 줄이 정본」 이 0 이고 「넷째 줄」 · 「코드 블록」 이 함께 있으며, `## 4. 완료 게이트` 절 첫 `text` 코드 블록의 넷째 줄이 `(effective|resolved)` 를 담는다(가리킨 자리가 맞다) [exact, enumerated]
    측정: `m SK-08` 이 `g04=0 fourth=1 line4_ok=1` (시작 판 `g04=1 fourth=0 line4_ok=1`)
- [ ] SK-09: `docs/tone/dart-flutter-idioms.md` 머리 판이 오르고 페이지 머리가 따른다 — frontmatter `version` 이 `0.1.0` 보다 큰 판이고 `last_updated` 가 2026-09-26 이후이며, `docs/tone-kit/dart-flutter-idioms.html` 의 부제(`v<판> · 갱신 <날짜>`)와 끝 캡션(`<code><판></code> · 최종 갱신 <날짜>`)이 같은 판 · 날짜를 적고 옛 두 글이 0 이다 [exact, enumerated]
    측정: `m SK-09` 가 `gt010=1 date_ok=1 sub=1 cap=1 old_sub=0 old_cap=0` (시작 판 `version=0.1.0 gt010=0 last_updated=2026-09-02 date_ok=0 sub=1 cap=1 old_sub=1 old_cap=1`)
- [ ] SK-10: 제스처 콜백 58 개의 기준 판 표기가 EX-14 와 같다 — 다섯 파일(`tone-kit/references/adapter-dart-flutter.md` · `docs/tone/dart-flutter-idioms.md` · `docs/tone/naming-taxonomy.md` · `docs/tone-kit/dart-flutter-idioms.html` · `docs/tone-kit/naming-taxonomy.html`)에서 `3.38.4` 만 적고 `3.47.5` 가 없는 줄이 0 이고, 파일마다 `3.47.5` 를 담은 줄 수가 시작 판의 `3.38.4` 줄 수 이상이다(`docs/tone/research-log.md` 는 조사 기록이라 제외) [exact, enumerated]
    측정: `m SK-10` 이 `only_3384=0 short=[]` (시작 판 `only_3384=14`, 다섯 파일 모두 short)
- [ ] SK-11: `tone-kit/references/sources.md` 세 자리(EX-14) — (a) `| go_router` 로 시작하는 행이 정확히 1 개(시작 판의 `| go_router 예제 |` 행을 고쳐 채운다 — 새 행을 더하지 않는다)이고 그 행에 `18.0.1` · `2026-09-26`, 파일 안 한 줄에 `17.0.0` · `18.0.0` · `material_ui` 가 함께(17.0.0 깨지는 변경 · 18.0.0 `material_ui` 이전 주의), (b) 위키 옛 주소 `wiki/Style-guide-for-Flutter-repo` 0 · 새 주소 `blob/main/docs/contributing/Style-guide-for-Flutter-repo.md` 1 이상, (c) 「위 표의 마지막 세 행」 0 이고 `K-11` 로 시작하는 줄이 `Microsoft` · `Google` · `한글 맞춤법` 을 함께 담는다. `1,867` 줄 수치는 킷 · `docs/tone` 어디에도 없다 [exact, enumerated]
    측정: `m SK-11` 이 `gor_rows=1 gor=1 gor_note≥1 wiki_old=0 wiki_new≥1 last3=0 k11≥1 lines1867=0` (시작 판 `gor_rows=1 gor=0 gor_note=0 wiki_old=1 wiki_new=0 last3=1 k11=1 lines1867=0`)

## Script

- [ ] SC-01: Stop 훅이 훅 입력의 `last_assistant_message` 를 분석 프롬프트에 싣는다(EX-1) — Given 가짜 codex 가 받은 표준 입력을 파일로 남기는 임시 폴더, When 도우미가 가지 끝 훅을 `--background` 로 세 번 돌리면, Then (a) 값 `LAM-MARK-5c1e 마지막 응답 <키 모양 문자열>` 을 넣은 입력의 프롬프트에 `LAM-MARK-5c1e` 가 1 번 이상 있고 키 모양 문자열(`sk-ant-` 뒤 40 자)은 0 번이다(가림 적용), (b) 필드가 없는 입력의 프롬프트는 시작 판 훅이 같은 입력으로 만든 프롬프트와 바이트가 같다(빈 블록을 싣지 않는다). 그리고 훅 시험 `reflect-kit/evals/hooks/log-reflection-test.sh` 가 종료 코드 0 · 불일치 0 이고 이름에 `last_assistant_message` 가 든 일치 경우가 2 개 이상이다 [exact, enumerated]
    측정: `m SC-01` 첫 줄 `mark≥1 key=0 nofield_same=1`, 둘째 줄 `test_rc=0 결과: N 경우 중 불일치 0 lam_cases≥2` (시작 판 `mark=0 key=0 nofield_same=1` · `결과: 32 경우 중 불일치 0 lam_cases=0` — `mark=0` 이 양성 대조)
    음성 대조: `m SC-01N` — 가지 끝 훅 사본에서 `last_assistant_message` 가 든 줄을 모두 지우고(`mut≥1`) 시험을 `REFLECT_KIT_HOOKS=<사본>` 으로 돌리면 `neg_lam_bad≥1`
- [ ] SC-02: 지워진 워크트리 경로의 facets 세션이 본 레포 이름으로 묶인다 — Given session-meta 의 `project_path` 가 없는 폴더 `<임시>/repos/alpha/.claude/worktrees/gone-wt` 이고 마찰이 적힌 facets 한 개, When `facets_unmatched 7 alpha` 를 부르면, Then 첫 줄이 `facets 1개 · 마찰 있는 세션 1개 · 그중 reflections 없음 1개` 를 담는다. 그리고 `reflect-kit/evals/hooks/collect-status-test.sh` 가 종료 코드 0 · 불일치 0 이고 이름에 `지워진 워크트리` 가 든 일치 경우가 1 개 이상이다. `_lib-project-id.sh` 머리 주석의 「그 세션은 all 에서만 보인다」 도 새 동작에 맞춘다 [exact, enumerated]
    측정: `m SC-02` 첫 줄 `tip=[facets 대조: facets 1개 · 마찰 있는 세션 1개 · 그중 reflections 없음 1개 …]`, 둘째 줄 `test_rc=0 결과: N 경우 중 불일치 0 wt_cases≥1` (시작 판 `facets 0개 · 마찰 있는 세션 0개` · `결과: 18 경우 중 불일치 0 wt_cases=0`)
    음성 대조: `m SC-02N` — 시작 판 라이브러리를 `PROJECT_ID_LIB` 로 주고 가지 끝 시험을 돌리면 `neg_wt_bad≥1`
- [ ] SC-03: 종류 줄이 빠진 옵션 목록에서 완료 검사가 종류 판정을 건너뛰고 enum 판정을 돌린다(KBa-1) — Given 설치본 뱀부 목록 `bambu-<설치본 판>.tsv` 에서 `process` · `filament` · `machine` 줄만 뺀 사본, When 가지 끝 완료 검사로 `process-seam-slope-type-invalid.json` 을 돌리면, Then FAIL 이 정확히 1 줄이고 그 줄이 `받지 않는 값 seam_slope_type` 이며 `키 스코프 불일치` FAIL 0, `[미검증]` 줄 하나에 `종류 검사 미실행` 이 있고 종료 코드 1 이다. 원래 목록으로는 FAIL 1 줄(`받지 않는 값`) · 종료 코드 1 그대로다. 옛 문구 「종류 줄이 없어 키 스코프 불일치 FAIL 은 믿지 마라」 는 SKILL.md 에 0 줄, 설명 문단(「enum 줄만 빠진 목록도 같다」 문단)에 `종류 줄` 과 `받지 않는 값` 을 함께 담은 줄이 1 이상, 음성 대조 블록에 종류 줄 빠진 목록 변이(`process|filament|machine`)가 1 줄 이상이다 [exact, enumerated]
    측정: `m SC-03` 이 `notypes fail=1 scope=0 enum=1 unv=1 exit=1` · `full fail=1 enum=1 exit=1` · `old_text=0 para≥1 neg_line≥1` (시작 판 `notypes fail=9 scope=9 enum=0 unv=0 exit=1` · `full fail=1 enum=1 exit=1` · `old_text=1 para=0 neg_line=0` — 봉인 전 실측, `scope=9` 가 양성 대조)
    음성 대조: 시작 판 완료 검사가 곧 「종류 판정을 건너뛰지 않는」 판이다 — 같은 명령이 `scope=9 enum=0` 을 낸다
- [ ] SC-04: 완료 검사 시험 파일을 따로 도는 실행 스크립트 `bambu-kit/evals/run-gate-fixtures.sh` 가 생긴다(KBa-2) — SKILL.md 에서 완료 검사 원문과 음성 대조 표 · 실행 줄을 읽어(시험 파일 이름을 스크립트에 적지 않는다) 폴더 · 표 · 실행 줄이 서로 맞는지 보고, 실행 줄의 시험 파일마다 원본 완료 검사로 돌려 표의 기대(FAIL 1 건 · 종료 코드 1, 또는 PASS · 종료 코드 0)와 맞으면 `일치 <시험 파일>`, 다르면 `불일치 <시험 파일> …` 를 찍고 끝 줄 `결과: N 경우 중 불일치 M` 을 낸다. 불일치가 있으면 종료 코드 1 이다. `BAMBU_GATE_SKILL=<SKILL.md 사본>` 으로 다른 사본을 잴 수 있다. Given 이 맥(슬라이서 둘 설치), When 가지 끝에서 `bash bambu-kit/evals/run-gate-fixtures.sh`, Then 종료 코드 0 · 일치 수 = 폴더의 시험 파일 수 · 불일치 0 · 건너뜀 0 이다. 스크립트는 리눅스에서도 돈다 — `mktemp -t` · `defaults read` · `/Applications` 글자가 0 이다 [exact, enumerated]
    측정: `m SC-04` 첫 줄 `rc=0 fixtures=F match=F bad=0 skip=0 last=[결과: F 경우 중 불일치 0]`, 둘째 줄 `linux_safe=0 fixture_literals=0` (시작 판 `no_script`)
    음성 대조: `m SC-04N` — `받지 않는 값` 판정 줄을 `pass` 로 바꾼 SKILL 사본(`mut=1`)이면 `rc=1 bad_enum≥1`, 실행 줄 하나(`process-thin-baseline.json`)를 지운 사본(`mut=1`)이면 `rc=1 missing≥1`
- [ ] SC-05: 슬라이서가 없는 기계(리눅스 CI)에서 실행 스크립트가 조용히 통과하지 않는다 — Given `/Applications/` 를 `/nonexistent-apps/` 로 바꾼 SKILL 사본(`BAMBU_GATE_SKILL`), When 스크립트를 돌리면, Then 종료 코드 0 · 불일치 0 이고, 슬라이서 없이도 판정되는 시험 파일은 `일치` 로 8 개 이상(FAIL 기대 다섯 — `process-class-unknown` · `process-speed-without-class` · `process-scarf-ratio-over` · `process-elefant-foot-negative` · `process-forbidden-key`, PASS 기대 셋 — `filament-unreadable-slot` · `filament-lattice-fanfix` · `process-thin-baseline`), 나머지는 `건너뜀 <시험 파일> …` 줄로 이름을 적으며 일치 + 건너뜀 = 시험 파일 수다. 건너뜀은 완료 검사가 `설치본 경로 없음` `[미검증]` 을 낸 FAIL 기대 파일에만 쓴다 [exact, enumerated]
    측정: `m SC-05` 첫 줄 `mut=10 rc=0 fixtures=F match≥8 bad=0 skip=F-match skip_named=skip` (2 회차 봉인 전 실측 2026-09-27 12:17 — 시작 판 `6378948`(`E_REF=BASE`) `mut=10 rc=127 fixtures=23 match=0 bad=0 skip=0 skip_named=0` · 가지 끝 `7f0a203` `mut=10 rc=0 fixtures=24 match=8 bad=0 skip=16 skip_named=16`. `mut` 는 두 판에서 같은 10 이다 — `git show <판>:bambu-kit/skills/bambu-print-profile/SKILL.md | sed 's#/Applications/#/nonexistent-apps/#g' | grep -c nonexistent-apps` 로도 두 판 모두 10. 1 회차의 `mut=4` 는 잰 적 없는 값이었다. 슬라이서 없는 판정 수는 1 회차 봉인 전 실측 — FAIL 기대 넷 · PASS 기대 셋이 슬라이서 없이 같은 결과, 금지 키 시험 파일 초안도 FAIL 1)
    음성 대조: `m SC-05` 둘째 줄 — 같은 사본에서 형상 클래스 허용값 판정을 `pass` 로 바꾸면(`mut=1`) `rc=1 bad_class≥1` (가지 끝 실측 `neg mut=1 rc=1 bad_class=1`)
    음성 대조: `m SC-05N` — 스크립트의 건너뜀 갈래를 끈 사본(`mut=1`, 구현을 되돌린 판)을 같은 슬라이서 없는 SKILL 사본으로 돌리면 `rc=1 bad≥1 skip=0` (가지 끝 실측 `noskip mut=1 rc=1 bad=16 skip=0 match=8`. 시작 판은 스크립트가 없어 `m SC-05` 가 `rc=127 match=0` — 이것도 FAIL)
- [ ] SC-06: 금지 키 FAIL 시험 파일 `bambu-kit/evals/gate-fixtures/process-forbidden-key.json` 이 생긴다(KBa-4) — 가지 끝 완료 검사로 돌리면 FAIL 이 정확히 1 줄이고 그 줄이 `FAIL process-forbidden-key.json: 금지 키 ` 로 시작하며 종료 코드 1, 금지 키 판정 줄만 `pass` 로 바꾼 사본(`mut=1`)이면 `RESULT: PASS` · 종료 코드 0 이다. 음성 대조 표에 `| \`evals/gate-fixtures/process-forbidden-key.json\` |` 행 1 개, 실행 줄 1 개가 있다 [exact, enumerated]
    측정: `m SC-06` 첫 줄 `fail=1 forbid=1 exit=1 | mut=1 1 exit=0`, 둘째 줄 `row=1 runline=1` (시작 판 `no_fixture`. 봉인 전에 `process-thin-baseline.json` 에 `elephant_foot_compensation` 을 더한 초안으로 같은 명령을 돌려 FAIL 1 · 지운 사본 PASS 를 확인했다)
- [ ] SC-07: MakerWorld 받는 법 블록이 답글 수를 센다(KBa-4, 이 맥 관측 2026-09-27) — Given 가짜 curl(댓글 둘: `replyCount` 2 · `commentReply` 2 개, `replyCount` 1 · `commentReply` 0 개), When 가지 끝 SKILL.md 「### JSON 주소」 블록을 돌리면, Then 한 줄에 `답글` · `replyCount 3` · `commentReply 2` 가 함께 나오고 종료 코드 0 이다. 같은 절 표에 `commentReply` · `replyCount` · `관측 2026-09-27` 이 있다. 새 시험 `bambu-kit/evals/makerworld-fetch-test.sh` 가 같은 블록을 SKILL.md 에서 뽑아(`BAMBU_FETCH_SKILL=<사본>` 으로 바꿀 수 있다) 가짜 curl 로 돌리고 종료 코드 0 · 끝 줄 `결과: N 경우 중 불일치 0` · 이름에 `답글` 이 든 일치 경우 1 개 이상을 낸다 [exact, enumerated]
    측정: `m SC-07` 첫 줄 `reply_line=1 exit=0`, 둘째 줄 `table=1`, 셋째 줄 `test_rc=0 결과: N 경우 중 불일치 0 … creply≥1` (시작 판 `reply_line=0 exit=0` · `table=0` · `no_test`)
    알려진 답: 가짜 curl 의 두 댓글 — `replyCount` 합 2+1=3, 받은 `commentReply` 합 2+0=2 (손으로 센 값. 실제 모델 1186414 는 25 · 24)
    음성 대조: `m SC-07N` — 블록에서 `답글` 이 든 줄을 지운 SKILL 사본(`mut≥1`)을 `BAMBU_FETCH_SKILL` 로 주면 `rc=1 bad_reply≥1`
- [ ] SC-08: 음성 대조 블록이 임시 파일을 남기지 않는다(KBa-4) — Given 가지 끝 SKILL.md 의 음성 대조 블록, When 도우미가 블록을 통째로 돌리면, Then 블록의 `mktemp -t` 이름으로 시작하고 돌린 뒤에 생긴 임시 항목이 0 개이고(`left=0`), 블록이 찍는 `exit=` 줄은 47 개 이상이다(시험 · 변이 줄이 줄지 않았다) [exact, collective]
    측정: `m SC-08` 끝 줄 `names=[…] left=0 exits≥47` (시작 판 `names=[emptylist gate noenum] left=18 exits=47` — 봉인 전 실측, `left=18` 이 양성 대조. macOS `mktemp -t` 는 `TMPDIR` 이 아니라 `getconf DARWIN_USER_TEMP_DIR` 폴더에 만든다 — 도우미가 그 폴더를 재고 남은 것은 지운다)

## Error

- [ ] ER-01: 실행 스크립트가 완료 검사를 못 뽑으면 멈춘다 — Given 빈 파일을 `BAMBU_GATE_SKILL` 로 준다, When 스크립트를 돌리면, Then `STOP` 으로 시작하는 줄이 1 개 이상이고 종료 코드 2 이며 `일치` 줄은 0 이다(빈 스크립트를 돌려 모두 통과처럼 보이는 일이 없다) [exact, enumerated]
    측정: `m ER-01` 이 `rc=2 stop≥1 match=0` (시작 판 스크립트 없음 `rc=127`)
- [ ] ER-02: 모델 주소가 403 이면 받는 법 블록이 멈추고 시험이 그 경우를 잰다 — Given 가짜 curl 이 `makerworld.com` 모델 주소에 403 과 `Just a moment...` HTML 을 준다, When 가지 끝 블록을 돌리면, Then `FAIL design.json` 으로 시작하는 줄이 1 이고 종료 코드 1 이다. 새 시험 `makerworld-fetch-test.sh` 에 이름에 `403` 이 든 일치 경우가 1 개 이상 있다 [exact, enumerated]
    측정: `m SC-07` 첫 줄의 `403: fail_design=1 exit=1` · 셋째 줄 `c403≥1` (시작 판 블록은 이미 `fail_design=1 exit=1` — 봉인 전 실측. 시험은 없다)

## Architecture

- [ ] AR-01: 바뀐 파일이 기대 집합 안이고 한 커밋에 맨 위 자리 하나다 — Given 구현 · notes · QA 리포트 커밋이 모두 가지 `chore/ak2-k3` 에 들어간 뒤, 시작점 `BASE=$(git -C W merge-base origin/main chore/ak2-k3)` 부터 끝점 `TIP=$(git -C W rev-parse --verify chore/ak2-k3)` 까지(`HEAD` 를 쓰지 않는다. 해석이 안 되면 `UNRESOLVED` 로 멈춘다) `git diff --name-only` 로 모은 경로가 측정 도우미 `ALLOWED` 의 스물일곱 경로 안에만 있고(부분 집합, 생성물 제외 없음), reflect-kit · bambu-kit · tone-kit · `docs/tone` · `.github` 가 각 1 경로 이상이며, 커밋마다 맨 위 자리가 하나뿐이다 — 자리는 reflect-kit · bambu-kit · tone-kit · `docs/tone` · `docs/tone-kit` · `.github` · `.harness` 일곱이다 [exact, collective]
    측정: `m AR-01` 이 `extra=0 multi_top=0` 이고 `reflect` · `bambu` · `tone` · `docs_tone` · `github` ≥1 (시작 판 `changed=0`)
    양성 대조: 임시 복제본에서 `bambu-kit/README.md` · `tone-kit/skills/tone-guide/SKILL.md` 를 다른 자리 파일과 한 커밋씩 넣으면 `extra=2 multi_top=2` 와 `EXTRA bambu-kit/README.md` (봉인 전 실측)
- [ ] AR-02: 결정 · 처리됨 · 바깥 근거 없음 · 충돌 자리 · 실물 확인 필요 · 다시 만들 문서 페이지를 notes 에 남긴다 — Given 끝점 `TIP` 과 작업 폴더 HEAD 가 같고, notes `.harness/.meta/after-kaizen-0926b/k3-notes.md` 가 커밋돼 있다. Then 서른 토큰(`KRf-1` · `KRf-2` · `KRf-3` · `KRf-4` · `KRf-5` · `KBa-1` · `KBa-2` · `KBa-3` · `KBa-4` · `KT-1` · `KT-2` · `KT-3` · `EX-1` · `EX-14` · `바깥 근거 없음` · `처리됨` · `실물 확인 필요` · `G91` · `feat/bambu-kit-orca-h2s-feedback` · `C-06` · `etc_seq=663` · `` `__` `` · `err=` · `commentReply` · `tone-guide` · `:1836-1846` · `:1854-1872` · `:1923-1941` · `:1956-1985` · `:2443-2444`)이 각 1 줄 이상이고, `scripts/detect-docs-drift.py --since BASE` 가 낸 `docs/**.html` 페이지가 모두 notes 에 적혀 있다(문서 사이트 재생성은 이 계약 범위 밖 — SK-09 · SK-10 이 고친 두 페이지 말고는 목록만 넘긴다). KBa-3 줄은 「GAP 분석」 의 충돌 자리 다섯(위 끝 다섯 토큰)과 이 계약이 줄을 더한 자리를 적고, 바깥 근거 인용은 EX 파일 경로와 원문 URL 을 함께 적는다 [exact, enumerated]
    측정: `m AR-02` 첫 줄 `committed=1` 과 1 이상 서른, 둘째 줄 `rc=0 pages=p miss=0` (시작 판 `committed=0` 과 0 서른 · `pages=0`)
    양성 대조: 임시 복제본에서 `docs/tone/naming-taxonomy.md` · `tone-kit/references/sources.md` · reflect-digest 를 바꿔 커밋하면 둘째 줄 `pages=3 miss=3` (봉인 전 실측)

## Anti-patterns

- [ ] AP-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수 (```text, ```bash, ```yaml 등). 판정 권위는 validate-plugin V6 상태기계다 — 여는/닫는 fence 가 동형이라 줄 단위 정규식으로는 판정 불가
    측정: 끝점을 풀어 둔 판 `E` 에서 `python3 "$E/scripts/validate-plugin.py" --check=code-fence` 종료 코드 0 (시작 판 0)
    양성 대조: 임시 복제본의 reflect-digest SKILL.md 끝에 언어 없는 fence 를 붙이면 종료 코드 2 (봉인 전 실측)
- [ ] AP-04: SKILL.md / agents/*.md frontmatter 에서 name 필드 누락 — validate-plugin V1 FAIL
    측정: `python3 "$E/scripts/validate-plugin.py" --check=frontmatter` 종료 코드 0 (시작 판 0)
    양성 대조: 임시 복제본의 tone-guide SKILL.md 에서 `name:` 줄을 지우면 `누락 필드 ['name']` · 종료 코드 2 (봉인 전 실측)

## Reusability

- [ ] RE-01: 다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다 — 새 스크립트 둘은 레포 어디서든 부를 수 있는 킷 `evals/` 파일이고, 머리 12 줄 안에 사본을 재는 환경 변수(`BAMBU_GATE_SKILL` · `BAMBU_FETCH_SKILL`)를 적어 다른 사본 · 다른 킷 계약이 그대로 쓸 수 있다
    측정: `m RE-01` 이 `gate_env≥1 fetch_env≥1` (시작 판 `0 0`)
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다 — 실행 스크립트는 시험 파일 목록 · 기대를 SKILL.md 음성 대조 표 · 실행 줄에서 읽고(목록을 두 번 적지 않는다), 받는 법 시험은 블록을 SKILL.md `### JSON 주소` 절에서 뽑아 돈다(블록을 베끼지 않는다). reflect 새 경우는 기존 `check` · `run_bg` · `fu` 형식으로 더한다
    측정: `m SC-04` 둘째 줄 `fixture_literals=0` · `m RE-02` 가 `fetch_anchor≥1 fetch_copy=0`

## Diagnostics

- [ ] DG-01: N/A (commands.analyze `bash -n scripts/release.sh` 가 재는 `scripts/release.sh` 는 이번 바뀐 파일에 없다. 측정: `git -C W diff --name-only BASE TIP | grep -cx 'scripts/release.sh'` 가 0)
- [ ] DG-02: IDE diagnostics 워닝/인포 0개 ([] 제외) — IDE(편집기) 진단을 명령줄로 같게 잰다: 바뀐 `.md`(`.harness/sprint-*` 제외)의 더해진 줄에 걸린 markdownlint-cli2 0.23.2(MD013 끔, 편집기 확장과 같은 설정) 경고 0 · 바뀐 `.sh` 의 shellcheck 경고 수가 시작 판보다 늘지 않음(새 파일은 0) · 바뀐 `.json` 읽기 실패 0
    측정: `m DG-02` 가 `md_new=0 sc_new=0 json_bad=0` (도구가 없으면 도우미 `mdl_ready` 가 임시 폴더에 설치한다. shellcheck 0.11.0)
    양성 대조: 임시 복제본의 `tone-kit/references/sources.md` 끝에 `#bad heading`, reflect-digest 끝에 언어 없는 fence, `log-reflection.sh` 끝에 `rm $undefined_x` 를 넣어 커밋하면 `md_new=2 sc_new=3` (봉인 전 실측 — 실측 중 도우미의 `comm` 이 숫자 정렬 입력을 받아 늘 0 을 내던 결함을 찾아 글자 정렬로 고쳤다)
- [ ] DG-03: N/A (commands.test `bash scripts/release.sh 2>&1 || true` 가 재는 `scripts/release.sh` 는 이번 바뀐 파일에 없다. 측정: DG-01 과 같은 명령이 0)
- [ ] DG-04: N/A (구동할 앱 · 서버가 없다 — 바뀐 파일이 훅 셸 스크립트 · 시험 스크립트 · 스킬 문서 · 참조 문서 · 문서 페이지뿐이다. 대신 SC-01 · SC-02 가 훅을 실제로 돌리고 DG-05 가 로컬 CI 를 돌린다)
- [ ] DG-05: 지금 `ci-local.sh` 가 담은 CI(자동 검사) 단계 26 개(통과 25 · yq 없음 건너뜀 1)를 로컬에서 돌려 통과한다 — Given 작업 폴더 W 가 끝점과 같다(`git -C W rev-parse HEAD` 가 `TIP` 이고 `git -C W status --porcelain --untracked-files=no` 가 빈 출력), When `TMPDIR=<임시 폴더> bash /Users/jackson/Hub/10_Dev/claude-plugins/.harness/handoff/2026-09-26-tools/ci-local.sh /Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak2-k3` 를 돌리면, Then 요약(`$TMPDIR/ci-local/summary.txt`)에 `rc=0` 줄이 25 개이고 `rc=0` 이 아닌 줄은 `feedback-agg-test SKIP (yq 없음)` 하나뿐이다
    측정: `grep -c 'rc=0' "$TMPDIR/ci-local/summary.txt"` 가 25 · `grep -v 'rc=0' "$TMPDIR/ci-local/summary.txt"` 가 그 한 줄 (시작 판 봉인 전 실측: 25 · SKIP 한 줄, 도구 sha256 앞자리 `59fe55125c0dbc77`)
    음성 대조: 이 묶음이 기대는 `reflect-log-test` · `reflect-collect-test` · `validate-plugin` 단계는 훅 · 라이브러리 · 킷 문서 frontmatter 를 깨면 실패한다 — SC-01N · SC-02N · AP-04 의 대조가 같은 시험을 쓴다. 새 bambu 단계는 이 도구에 없으므로 SC-04 · SC-05 · SC-07 이 따로 잰다

## 범위 경계

항목별 처리 — 입력은 `leftovers.md` 의 열두 행이다.

| ID | 항목 | 처리 | 조건 · 사유 |
| --- | --- | --- | --- |
| KRf-1 | 수집 멈춤 조건 두 줄 | 계약에 넣음 | SK-01 |
| KRf-2 | 대체 경로 주석 | 계약에 넣음 | SK-02 (a) |
| KRf-3 | README 따옴표 | 계약에 넣음 | SK-03. 다른 `${CLAUDE_PLUGIN_ROOT}` 는 산문 속 경로 표기라 명령이 아니다(`reflect-promote` · `reflect-kaizen` · `reflect-digest` · `docs/SCHEMA.md`) |
| KRf-4 | `async` | 계약에 넣음 — 결정은 「주석만 고치고 `nohup` 유지」 | SK-02 (b). EX-1 이 `async` 가 있다고만 하고 훅 `timeout: 5` 와의 관계는 원문에 없다 — 옮기면 그 동작을 따로 재야 해서 이번에는 옮기지 않는다 |
| KRf-4 | `last_assistant_message` | 계약에 넣음 | SC-01 |
| KRf-4 | 지워진 워크트리 | 계약에 넣음 | SC-02 — `scripts/collect-kaizen-data.py:420-421` 과 같은 규칙(`/.claude/worktrees/` 앞에서 자른다). `project_root` 쓰기 경로(`compute_project_id`)는 바꾸지 않는다 |
| KRf-5 | `fail:codex-exit-2` 뒤 `fallback:claude-exit-1` | 원인 조사 · 계약에 넣음(문서 한 줄) | SK-04. 원인은 0.8.0 전 판 훅을 쥔 오래 켠 세션(「리서치 소스」 관측). 새 판 실패(`err=` 줄)가 0 이라 멈춤 문턱은 그대로 두고 notes 에 적는다 |
| KBa-1 | 종류 줄 빠진 목록 | 계약에 넣음 — 결정은 「종류 줄이 없으면 종류 판정을 건너뛰고 `[미검증]` 에 `종류 검사 미실행`」 | SC-03. 목록이 적은 「`[미검증]` 에 `enum 값 검사 미실행` 도 넣는다」 는 판정 동작을 그대로 둘 때의 문구다 — 동작을 고치면 enum 판정이 실제로 돌아 그 문구가 거짓이 되므로 넣지 않는다(enum 줄도 없을 때는 기존대로 `enum 값 검사 미실행`). 이 문구 차이는 위임 문구가 콕 집어 승인한 것이 아니라 계약 작성자 판단이다 — 봉인 전 교차 진단이 기술적으로 타당하다고 확인했고, notes 에 「목록 원문과 다르게 처리」 로 적어 부모가 사용자에게 한 줄로 알린다 |
| KBa-2 | 완료 검사 실행 목록 · CI | 계약에 넣음 | SC-04 · SC-05 · ER-01 · SK-05. CI 등록은 `.github/workflows/ci.yml` validate 한 단계 |
| KBa-3 | 올리지 않은 가지와 SKILL.md 충돌 | notes 에 적음(그 가지를 건드리지 않는다) | AR-02. 충돌 자리는 「GAP 분석」 끝 문단 |
| KBa-4 | `[미검증]` 네 칸 다섯 자리 | 계약에 넣음 | SK-06 |
| KBa-4 | 현행화 | 계약에 넣음 — 목록이 적은 세 자리만 | SK-07. SKILL.md 버전 교차 확인 표(시작 판 `:2541-2545` 「references 는 `02.06.00.51` 기준」)는 `/bambu-research` 소관이라 notes 에 넘긴다 |
| KBa-4 | 금지 키 FAIL 시험 파일 | 계약에 넣음 | SC-06. `compatible_printers` · 메타필드 · 숫자 타입 FAIL 시험 파일은 목록 밖이라 notes 에 넘긴다 |
| KBa-4 | 댓글 답글 배열 이름 · 받는 법 403 | 계약에 넣음 | SC-07 · ER-02 |
| KBa-4 | `mktemp` 폴더 | 계약에 넣음 | SC-08. 다른 두 블록(`:357` 형상 측정 · `:2220` 슬롯 대조)은 이미 `rm -rf "$T"` 로 치운다 |
| KBa-4 | `G91` 이 E 에도 적용되는가(H2S 펌웨어) | 실물 확인 필요 | notes. 설치본 시작 G-code 로는 어느 쪽이든 길이가 같다(`SKILL.md:2245`) — 펌웨어 원문이 저장소 밖 |
| KT-1 | 어댑터 `:26` | 계약에 넣음 | SK-08 |
| KT-2 | 머리 판 | 계약에 넣음 | SK-09 |
| KT-3 | 3.38.4 · go_router · 위키 이전 · `material_ui` · 「마지막 세 행」 | 계약에 넣음 | SK-10 · SK-11 (EX-14) |
| KT-3 | 1,867 줄 수치 | 처리됨 | 킷 · `docs/tone` 어디에도 없다(SK-11 `lines1867=0`, 시작 판도 0) |
| KT-3 | C-06 강도 · `etc_seq=663` 이름표 · `__` 예시 | 바깥 근거 없음 | EX-14 가 다루지 않았다(Effective Dart PREFER · 린트 DO · 국립국어원 자료 · Dart 3.7 `_` 규칙). notes 에 적는다 |
| KT-3 | `locale-korean.md` §2 grep 열 | 처리됨 | c3c `b367184` 가 칸마다 `§8 G-1 갈래 N` 을 가리키게 했다(목록 KT-3 에도 이 항목은 없다) |

`docs/tone-kit/*.html` 은 SK-09 · SK-10 이 고친 줄만 원본 md 와 같게 고친다(원본 · 생성물을 함께 고친다). 나머지 드리프트 페이지는 AR-02 가 목록으로 넘긴다.

범위 밖(이 계약이 고치지 않는다): `scripts/` · `harness/` · `.claude/` · 킷 `plugin.json` 버전(릴리스 단계 몫) · 다른 세션 가지 `feat/bambu-kit-orca-h2s-feedback` · reflect-kit 멈춤 문턱 숫자 · `reflect-kit/docs/DESIGN.md` 의 「Stop (async)」 개념 그림.

기능 조건 수는 24 개(SK 11 · SC 8 · ER 2 · AR 2 · DG-05)로 「복잡」 상한 20 을 넘는다. 묶음 배정이 부모 오케스트레이션에서 정해져(세 킷 열두 항목) 계약을 나누지 않는다.

커버리지 해소 — Step 6.5 (4) 검출기가 낸 `UNCOVERED` 와 처리. 모두 측정 도우미 `m` 의 그 조건 갈래가 해당 토큰을 읽거나 센다:

- 커버리지 해소: AR-01 — 경로 기대 집합은 측정 도우미 `ALLOWED` 한 곳에만 적는다(목록을 두 번 적지 않는다)
- 커버리지 해소: SK-06 — 다섯 기준 글과 네 칸 이름은 `m SK-06` 의 `para` 인자와 `all` 인자에 글자 그대로 있다
- 커버리지 해소: SK-10 — 다섯 파일 경로는 `m SK-10` 의 `for p in` 목록이다
- 커버리지 해소: SC-05 — 슬라이서 없이 판정되는 여덟 이름은 기대 하한(`match≥8`)의 근거이고, 이름별 판정은 스크립트 출력 `일치 <시험 파일>` 이 한다
- 커버리지 해소: AR-02 — 토큰 서른은 `m AR-02` 첫 줄의 `for t in` 목록이다
- 커버리지 해소: SK-02 — `log-reflection.sh` · `hooks/hooks.json` 은 `m SK-02` 가 여는 두 파일이고 `code.claude.com/docs/en/hooks` 는 `async_doc` 의 `all` 인자다
- 커버리지 해소: SK-03 — `reflect-kit/README.md` 와 `install-scheduler.sh` 명령 두 꼴은 `m SK-03` 이 글자 그대로 센다
- 커버리지 해소: SK-05 — `.github/workflows/ci.yml` 의 `jobs.validate.steps` 와 두 스크립트 경로 · `bambu-kit/evals/` 는 `m SK-05` 의 파이썬 조각이 읽고 센다
- 커버리지 해소: SK-07 — 두 참조 문서 · SKILL.md 와 판 번호 넷은 `m SK-07` 이 줄마다 `all` · `n` 으로 센다
- 커버리지 해소: SK-09 — md · html 두 파일과 `0.1.0` 비교는 `m SK-09` 가 읽고(판 크기는 파이썬 튜플 비교) 옛 글 두 개를 센다
- 커버리지 해소: SK-11 — `sources.md` 와 판 번호 · 주소 토큰은 `m SK-11` 이 센다. `docs/tone` 은 `lines1867` 의 검색 범위다
- 커버리지 해소: SC-02 — 임시 폴더 경로 · 시험 · 라이브러리는 `m SC-02` · `m SC-02N` 이 만들고 부른다
- 커버리지 해소: SC-04 — 스크립트 경로와 `/Applications` 글자 검사는 `m SC-04` 둘째 줄 `linux_safe` 가 센다
- 커버리지 해소: ER-02 — `makerworld.com` 403 은 도우미 가짜 curl 의 `MW_CODE`, 시험 파일은 `m SC-07` 셋째 줄이 부른다
- 오라클 해소: SK-01 ~ SK-04 · SK-06 ~ SK-11 — 산출물이 문서 · 주석 문장이라 부를 코드가 없다. 옛 문구 0 과 새 문구 줄 수(양성 대조는 시작 판 값)로 잰다. 실행해서 재는 조건은 SC-01 ~ SC-08 · ER-01 · ER-02 · SK-05 · AR-01 · AR-02 · DG-02 · DG-05 다

## 회귀 게이트 — 측정 도우미

평가 때 이 블록을 떼어 bash 에서 불러 쓴다. `TMPDIR` 은 평가자 임시 폴더로 준다. 도우미는 끝점과 시작점을 `git archive` 로 풀어 재므로 작업 폴더의 미커밋 변경을 보지 않는다
(AR-02 둘째 줄만 작업 폴더에서 `detect-docs-drift.py` 를 돌리므로 작업 폴더 HEAD 가 `TIP` 이어야 한다). 뱀부 조건은 슬라이서 둘이 깔린 이 맥에서 잰다.
작업 폴더 밖 입력은 지우지 마라 — 도우미가 만든 `$T` 아래와, SC-08 이 돌린 블록이 사용자 임시 폴더에 남긴 항목(도우미가 이름을 찍고 지운다)만 치운다.

```bash
# === 측정 도우미 시작 (after-0926-kits-reflect-bambu-tone-r2) ===
# 쓰는 법: 이 블록을 파일로 떼어 bash 에서 source 한 뒤 `m <조건 ID>`. zsh 에서 부르지 마라.
# 잴 트리 E — 기본은 가지 끝(TIP)을 git archive 로 푼 임시 폴더. 시작 판을 재려면 E_REF=BASE.
# 뱀부 조건(SC-03 ~ SC-06 · SC-08)은 이 맥처럼 /Applications 에 BambuStudio · OrcaSlicer 가 깔린 기계에서 잰다.
W=${W:-/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak2-k3}
BR=${BR:-chore/ak2-k3}
BASE=$(git -C "$W" merge-base origin/main "$BR") || { echo "UNRESOLVED BASE"; return 2 2>/dev/null || exit 2; }
TIP=$(git -C "$W" rev-parse --verify "$BR") || { echo "UNRESOLVED TIP"; return 2 2>/dev/null || exit 2; }
T=$(mktemp -d "${TMPDIR:-/tmp}/k3m.XXXXXX")
snap() { mkdir -p "$2" && git -C "$W" archive "$1" | tar -x -C "$2"; }
B=$T/base; snap "$BASE" "$B"
case "${E_REF:-TIP}" in
  BASE) E=$B ;;
  *)    E=$T/tip; snap "$TIP" "$E" ;;
esac
PY=${PY:-python3}
RF=$E/reflect-kit; BK=$E/bambu-kit; BS=$E/bambu-kit/skills/bambu-print-profile; TK=$E/tone-kit
secx() { awk -v s="$1" '
  function lv(x){ match(x, /^#+ /); return (RSTART==1) ? RLENGTH-1 : 0 }
  !f && index($0,s)==1 { f=1; L=lv($0); print; next }
  f && lv($0)>0 && lv($0)<=L { exit }
  f' "$2"; }
n() { grep -cF -- "$1" || true; }
nall() { awk -v a="$*" 'BEGIN{k=split(a,w,"\t")} { ok=1; for(i=1;i<=k;i++) if(index($0,w[i])==0) ok=0; if(ok) c++ } END{print c+0}'; }
all() { local IFS=$'\t'; nall "$*"; }
cnt() { printf '%s' "$1" | awk 'NF{c++} END{print c+0}'; }
# s 로 시작하는 줄부터 빈 줄 앞까지 (문단)
para() { awk -v s="$1" '!f && index($0,s)>0 {f=1} f && !NF {exit} f' "$2"; }
ALLOWED='reflect-kit/skills/reflect-digest/SKILL.md
reflect-kit/hooks/log-reflection.sh
reflect-kit/hooks/_lib-project-id.sh
reflect-kit/README.md
reflect-kit/evals/hooks/log-reflection-test.sh
reflect-kit/evals/hooks/collect-status-test.sh
bambu-kit/skills/bambu-print-profile/SKILL.md
bambu-kit/skills/bambu-print-profile/references/bambu-fields-baseline.md
bambu-kit/skills/bambu-print-profile/references/materials.md
bambu-kit/skills/bambu-print-profile/references/failure-recipes.md
bambu-kit/evals/run-gate-fixtures.sh
bambu-kit/evals/makerworld-fetch-test.sh
bambu-kit/evals/gate-fixtures/process-forbidden-key.json
.github/workflows/ci.yml
tone-kit/references/adapter-dart-flutter.md
tone-kit/references/sources.md
docs/tone/dart-flutter-idioms.md
docs/tone/naming-taxonomy.md
docs/tone-kit/dart-flutter-idioms.html
docs/tone-kit/naming-taxonomy.html
.harness/sprint-contract-after-0926-kits-reflect-bambu-tone.md
.harness/sprint-amendments-after-0926-kits-reflect-bambu-tone.md
.harness/sprint-feedback-after-0926-kits-reflect-bambu-tone.md
.harness/sprint-contract-after-0926-kits-reflect-bambu-tone-r2.md
.harness/sprint-amendments-after-0926-kits-reflect-bambu-tone-r2.md
.harness/sprint-feedback-after-0926-kits-reflect-bambu-tone-r2.md
.harness/.meta/after-kaizen-0926b/k3-notes.md'
NOTES=.harness/.meta/after-kaizen-0926b/k3-notes.md

# ── reflect: 훅을 가짜 codex 로 한 번 돌려 분석기가 받은 프롬프트를 파일로 받는다 ──
# lam_run <hooks 폴더> <이름> [last_assistant_message 값 — 없으면 필드를 안 넣는다]
lam_run() {
  local hk=$1 nm=$2 d=$T/lam-$2
  mkdir -p "$d/bin" "$d/home" "$d/proj" "$d/tmp"
  cat > "$d/bin/codex" <<'EOF'
#!/usr/bin/env bash
out=""; prev=""
for a in "$@"; do [ "$prev" = "--output-last-message" ] && out=$a; prev=$a; done
cat > "$PROMPT_OUT"
printf 'no issues\n' > "$out"
EOF
  chmod 755 "$d/bin/codex"
  for i in 1 2 3 4 5 6 7 8 9 10 11 12; do printf '{"type":"user","message":{"content":"line %s"}}\n' "$i"; done > "$d/t.jsonl"
  if [ $# -ge 3 ]; then
    jq -cn --arg s "LAM-$nm" --arg t "$d/t.jsonl" --arg c "$d/proj" --arg m "$3" '{session_id:$s, transcript_path:$t, cwd:$c, last_assistant_message:$m}' > "$d/in.json"
  else
    jq -cn --arg s "LAM-$nm" --arg t "$d/t.jsonl" --arg c "$d/proj" '{session_id:$s, transcript_path:$t, cwd:$c}' > "$d/in.json"
  fi
  env HOME="$d/home" TMPDIR="$d/tmp" PATH="$d/bin:$PATH" PROMPT_OUT="$d/prompt.txt" bash "$hk/log-reflection.sh" --background "$d/in.json" >/dev/null 2>&1
  printf '%s' "$d/prompt.txt"
}
# 가림 패턴에 걸리는 키 모양 문자열 (sk-ant- 뒤 40 자)
KEYLIKE="sk-ant-$(printf 'Q7%.0s' $(seq 1 20))"

# ── bambu: 완료 검사 원문 뽑기 · 음성 대조 블록 뽑기 · MakerWorld 받는 법 블록 뽑기 ──
gate_of() {  # gate_of <SKILL.md> <출력 파일> — 줄 수를 낸다
  local a b
  a=$(grep -n '^TARGET_SLICER=.* python3 - ' "$1" | head -1 | cut -d: -f1)
  b=$(awk -v s="$a" 'NR>s && $0=="PY" {print NR; exit}' "$1")
  if [ -n "$a" ] && [ -n "$b" ]; then sed -n "$((a+1)),$((b-1))p" "$1" > "$2"; else : > "$2"; fi
  wc -l < "$2" | tr -d ' '
}
neg_of() { awk 'index($0,"#### 음성 대조 — 검사가 살아 있는지 확인")==1{h=1} h&&/^```bash$/{b=1;next} b&&/^```$/{exit} b' "$1" > "$2"; wc -l < "$2" | tr -d ' '; }
fetch_of() { awk 'index($0,"### JSON 주소")==1{h=1} h&&/^```bash$/{b=1;next} b&&/^```$/{exit} b' "$1" > "$2"; wc -l < "$2" | tr -d ' '; }
BV=$(defaults read /Applications/BambuStudio.app/Contents/Info.plist CFBundleShortVersionString 2>/dev/null)
gate_run() {  # gate_run <gate 파일> <슬라이서> <시험 파일> [SKILL_DIR] — 출력 뒤에 exit=N
  ( cd "$E" && SKILL_DIR="${4:-bambu-kit/skills/bambu-print-profile}" TARGET_SLICER="$2" "$PY" "$1" "$3" 2>&1; echo "exit=$?" )
}
# 가짜 curl — 주소별로 준비한 파일과 상태 코드를 돌려준다 (-o · -w 만 흉내 낸다)
fake_curl() {  # fake_curl <폴더> <makerworld 상태 코드>
  mkdir -p "$1/bin"
  cat > "$1/bin/curl" <<'EOF'
#!/usr/bin/env bash
o=""; w=""; u=""
while [ $# -gt 0 ]; do case "$1" in -o) o=$2; shift 2 ;; -w) w=$2; shift 2 ;; -*) shift ;; *) u=$1; shift ;; esac; done
code=200; body=""
case "$u" in
  *makerworld.com/api/v1/design-service/design/*) code=$MW_CODE
    if [ "$code" = 200 ]; then body='{"title":"T","commentCount":2,"instances":[]}'; else body='<!DOCTYPE html><title>Just a moment...</title>'; fi ;;
  */instances) body='{"hits":[],"total":0}' ;;
  *commentandrating*offset=0*) body='{"total":2,"hits":[{"type":1,"comment":{"id":1,"replyCount":2,"commentReply":[{"id":11},{"id":12}]}},{"type":1,"comment":{"id":2,"replyCount":1,"commentReply":[]}}]}' ;;
  *commentandrating*) body='{"total":2,"hits":[]}' ;;
esac
[ -n "$o" ] && printf '%s' "$body" > "$o"
printf '%s' "${w//%\{http_code\}/$code}"
EOF
  chmod 755 "$1/bin/curl"
}
fetch_run() {  # fetch_run <SKILL.md> <makerworld 상태 코드> — 블록을 가짜 curl 로 돌린 출력 뒤에 exit=N
  local d=$T/fetch-$2-$RANDOM
  mkdir -p "$d/out"; fake_curl "$d" "$2"
  fetch_of "$1" "$d/block.sh" >/dev/null
  sed -i '' -e "s#<모델 번호>#1186414#" -e "s#<output_dir>#$d/out#" "$d/block.sh"
  ( cd "$d" && PATH="$d/bin:$PATH" MW_CODE="$2" bash "$d/block.sh" 2>&1; echo "exit=$?" )
}
# 블록을 돌린 뒤 새로 생긴 임시 항목 가운데 블록의 mktemp -t 이름으로 시작하는 것 (macOS mktemp -t 는 TMPDIR 이 아니라 사용자 임시 폴더에 만든다)
leak_run() {  # leak_run <블록 파일> — 첫 줄 names · left, 둘째 줄 exit= 줄 수
  local ut names mark left=0 p nm
  ut=$(getconf DARWIN_USER_TEMP_DIR 2>/dev/null); ut=${ut:-${TMPDIR:-/tmp}/}
  names=$(grep -oE 'mktemp (-d )?-t [A-Za-z0-9_]+' "$1" | awk '{print $NF}' | sort -u | tr '\n' ' ')
  mark=$T/leak-mark; : > "$mark"; sleep 1
  ( cd "$E" && bash "$1" > "$T/leak.out" 2>&1 )
  for nm in $names; do
    for p in $(find "$ut" -maxdepth 1 -name "$nm.*" -newer "$mark" 2>/dev/null); do left=$((left+1)); echo "LEFT ${p##*/}"; rm -rf "$p"; done
  done
  echo "names=[${names% }] left=$left exits=$(grep -c '^exit=' "$T/leak.out")"
}

m() {
  case "$1" in
  SK-01)  # reflect-digest 경고 조건 두 줄 (KRf-1)
    f=$RF/skills/reflect-digest/SKILL.md
    echo "old=$(n '엔트리 0 이고 Stop 실패 시도가 1 이상일 때' < "$f") new=$(n '엔트리 0 이고 마지막 정상 종료 뒤의 Stop 실패 시도가 1 이상일 때' < "$f")"
    ;;
  SK-02)  # log-reflection.sh 머리 · 대체 경로 주석 (KRf-2 · KRf-4 async)
    f=$RF/hooks/log-reflection.sh; h=$(sed -n '1,12p' "$f")
    echo "old_fb=$(n 'claude -p --model haiku' < "$f") new_fb=$(grep -E '^#' "$f" | n 'claude -p --safe-mode --model haiku') old_async=$(n 'plugin spec의 async 필드에 의존하지 않는다' < "$f") async_doc=$(printf '%s\n' "$h" | all 'async' 'code.claude.com/docs/en/hooks') hooks_same=$(cmp -s "$B/reflect-kit/hooks/hooks.json" "$RF/hooks/hooks.json" && echo 1 || echo 0)"
    ;;
  SK-03)  # README install-scheduler 예시 따옴표 (KRf-3)
    f=$RF/README.md
    echo "bare=$(n 'bash ${CLAUDE_PLUGIN_ROOT}/scripts/install-scheduler.sh' < "$f") quoted=$(n 'bash "${CLAUDE_PLUGIN_ROOT}/scripts/install-scheduler.sh"' < "$f")"
    ;;
  SK-04)  # reflect-digest Gotchas — err= 없는 실패 줄의 출처 (KRf-5)
    secx '## Gotchas' "$RF/skills/reflect-digest/SKILL.md" | all '`err=`' '0.8.0' '세션'
    ;;
  SC-01)  # last_assistant_message 가 분석 프롬프트에 들어간다 · 가린다 · 없으면 그대로 (KRf-4)
    p1=$(lam_run "$RF/hooks" with "LAM-MARK-5c1e 마지막 응답 $KEYLIKE")
    p0=$(lam_run "$RF/hooks" none); pb=$(lam_run "$B/reflect-kit/hooks" base)
    echo "mark=$(n 'LAM-MARK-5c1e' < "$p1") key=$(n "$KEYLIKE" < "$p1") nofield_same=$(cmp -s "$p0" "$pb" && echo 1 || echo 0) prompt_bytes=$(wc -c < "$p0" | tr -d ' ')"
    out=$(bash "$RF/evals/hooks/log-reflection-test.sh" 2>&1); rc=$?
    echo "test_rc=$rc $(printf '%s\n' "$out" | tail -1) lam_cases=$(printf '%s\n' "$out" | grep -c '^일치 .*last_assistant_message')"
    ;;
  SC-01N)  # 음성 대조 — 훅 사본에서 last_assistant_message 줄을 지우면 시험 경우가 불일치한다
    mkdir -p "$T/hneg"; cp "$RF/hooks/"* "$T/hneg/"
    mut=$(grep -c 'last_assistant_message' "$T/hneg/log-reflection.sh"); sed -i '' '/last_assistant_message/d' "$T/hneg/log-reflection.sh"
    out=$(REFLECT_KIT_HOOKS="$T/hneg" bash "$RF/evals/hooks/log-reflection-test.sh" 2>&1)
    echo "mut=$mut neg_lam_bad=$(printf '%s\n' "$out" | grep -c '^불일치 .*last_assistant_message')"
    ;;
  SC-02)  # 지워진 워크트리 경로의 facets 세션이 본 레포 이름으로 묶인다 (KRf-4)
    u=$T/usage; mkdir -p "$u/facets" "$u/session-meta" "$T/logs/alpha"
    st=$(date -u -v-1d '+%Y-%m-%dT%H:%M:%S.000Z' 2>/dev/null || date -u -d '-1 day' '+%Y-%m-%dT%H:%M:%S.000Z')
    printf '{"session_id":"S-gone","friction_detail":"gone friction"}\n' > "$u/facets/S-gone.json"
    printf '{"project_path":"%s","start_time":"%s"}\n' "$T/repos/alpha/.claude/worktrees/gone-wt" "$st" > "$u/session-meta/S-gone.json"
    fu() { bash -c '. "$1" 2>/dev/null; shift; facets_unmatched "$@"' _ "$1" 7 alpha "$u" "$T/logs" | head -1; }
    echo "tip=[$(fu "$RF/hooks/_lib-project-id.sh")]"
    out=$(bash "$RF/evals/hooks/collect-status-test.sh" 2>&1); rc=$?
    echo "test_rc=$rc $(printf '%s\n' "$out" | tail -1) wt_cases=$(printf '%s\n' "$out" | grep -c '^일치 .*지워진 워크트리')"
    ;;
  SC-02N)  # 음성 대조 — 시작 판 라이브러리로 가지 끝 시험을 돌리면 지워진 워크트리 경우가 불일치한다
    out=$(PROJECT_ID_LIB="$B/reflect-kit/hooks/_lib-project-id.sh" bash "$RF/evals/hooks/collect-status-test.sh" 2>&1)
    echo "neg_wt_bad=$(printf '%s\n' "$out" | grep -c '^불일치 .*지워진 워크트리')"
    ;;
  SC-03)  # 종류 줄 없는 목록 — 종류 검사를 건너뛰고 enum 검사가 돈다 (KBa-1)
    gate_of "$BS/SKILL.md" "$T/gate.py" >/dev/null
    nt=$T/notypes; mkdir -p "$nt/references/option-keys"
    grep -v -E "^(process|filament|machine)$(printf '\t')" "$BS/references/option-keys/bambu-$BV.tsv" > "$nt/references/option-keys/bambu-$BV.tsv"
    o=$(gate_run "$T/gate.py" bambu bambu-kit/evals/gate-fixtures/process-seam-slope-type-invalid.json "$nt")
    o2=$(gate_run "$T/gate.py" bambu bambu-kit/evals/gate-fixtures/process-seam-slope-type-invalid.json)
    echo "notypes fail=$(printf '%s\n' "$o" | grep -c '^FAIL') scope=$(printf '%s\n' "$o" | grep -c '^FAIL .*키 스코프 불일치') enum=$(printf '%s\n' "$o" | grep -c '^FAIL .*받지 않는 값 seam_slope_type') unv=$(printf '%s\n' "$o" | grep '^\[미검증\]' | n '종류 검사 미실행') $(printf '%s\n' "$o" | tail -1)"
    echo "full fail=$(printf '%s\n' "$o2" | grep -c '^FAIL') enum=$(printf '%s\n' "$o2" | grep -c '^FAIL .*받지 않는 값 seam_slope_type') $(printf '%s\n' "$o2" | tail -1)"
    echo "old_text=$(n '종류 줄이 없어 키 스코프 불일치 FAIL 은 믿지 마라' < "$BS/SKILL.md") para=$(awk '/^enum 줄만 빠진 목록도 같다/{f=1} f&&!NF{exit} f' "$BS/SKILL.md" | awk '/종류 줄/ && /받지 않는 값/{c++} END{print c+0}') neg_line=$(neg_of "$BS/SKILL.md" "$T/neg.sh" >/dev/null; n 'process|filament|machine' < "$T/neg.sh")"
    ;;
  SC-04)  # 시험 파일 실행 스크립트 — 슬라이서가 있는 기계 (KBa-2)
    s=$BK/evals/run-gate-fixtures.sh
    [ -f "$s" ] || { echo "no_script"; return 0; }
    out=$( (cd "$E" && bash "$s") 2>&1); rc=$?
    fx=$(find "$BK/evals/gate-fixtures" -maxdepth 1 -name '*.json' | awk 'END{print NR}')
    echo "rc=$rc fixtures=$fx match=$(printf '%s\n' "$out" | grep -c '^일치 ') bad=$(printf '%s\n' "$out" | grep -c '^불일치 ') skip=$(printf '%s\n' "$out" | grep -c '^건너뜀 ') last=[$(printf '%s\n' "$out" | tail -1)]"
    echo "linux_safe=$(grep -cE 'mktemp -t|defaults read|/Applications' "$s") fixture_literals=$(find "$BK/evals/gate-fixtures" -maxdepth 1 -name '*.json' -exec basename {} \; | while read -r x; do grep -cF "$x" "$s"; done | awk '{s+=$1} END{print s+0}')"
    ;;
  SC-04N)  # 음성 대조 — 받지 않는 값 판정을 지운 SKILL 사본이면 스크립트가 불일치 · 종료 코드 1
    cp "$BS/SKILL.md" "$T/skill-noenum.md"
    sed -i '' -E 's/^( *)errs\.append\(f?"받지 않는 값 .*$/\1pass/' "$T/skill-noenum.md"
    out=$( (cd "$E" && BAMBU_GATE_SKILL="$T/skill-noenum.md" bash "$BK/evals/run-gate-fixtures.sh") 2>&1); rc=$?
    echo "mut=$(diff "$BS/SKILL.md" "$T/skill-noenum.md" | grep -c '^>') rc=$rc bad_enum=$(printf '%s\n' "$out" | grep -c '^불일치 .*process-seam-slope-type-invalid.json')"
    grep -vF 'TARGET_SLICER=bambu python3 "$GATE" $FX/process-thin-baseline.json;' "$BS/SKILL.md" > "$T/skill-norun.md"
    out=$( (cd "$E" && BAMBU_GATE_SKILL="$T/skill-norun.md" bash "$BK/evals/run-gate-fixtures.sh") 2>&1); rc=$?
    echo "norun mut=$(diff "$BS/SKILL.md" "$T/skill-norun.md" | grep -c '^<') rc=$rc missing=$(printf '%s\n' "$out" | grep -c '실행 줄에 없음 process-thin-baseline.json')"
    ;;
  SC-05)  # 슬라이서 없는 기계 흉내 — /Applications 를 없는 경로로 바꾼 SKILL 사본 (KBa-2)
    sed 's#/Applications/#/nonexistent-apps/#g' "$BS/SKILL.md" > "$T/skill-noapp.md"
    out=$( (cd "$E" && BAMBU_GATE_SKILL="$T/skill-noapp.md" bash "$BK/evals/run-gate-fixtures.sh") 2>&1); rc=$?
    fx=$(find "$BK/evals/gate-fixtures" -maxdepth 1 -name '*.json' | awk 'END{print NR}')
    sk=$(printf '%s\n' "$out" | grep '^건너뜀 ')
    named=$(printf '%s\n' "$sk" | grep -cE '[a-z0-9-]+\.json')
    echo "mut=$(grep -c nonexistent-apps "$T/skill-noapp.md") rc=$rc fixtures=$fx match=$(printf '%s\n' "$out" | grep -c '^일치 ') bad=$(printf '%s\n' "$out" | grep -c '^불일치 ') skip=$(cnt "$sk") skip_named=$named"
    sed -E 's/^( *)errs\.append\(f?"_geometry_class=.geometry.r. .*$/\1pass/' "$T/skill-noapp.md" > "$T/skill-noapp-noclass.md"
    out=$( (cd "$E" && BAMBU_GATE_SKILL="$T/skill-noapp-noclass.md" bash "$BK/evals/run-gate-fixtures.sh") 2>&1); rc=$?
    echo "neg mut=$(diff "$T/skill-noapp.md" "$T/skill-noapp-noclass.md" | grep -c '^>') rc=$rc bad_class=$(printf '%s\n' "$out" | grep -c '^불일치 .*process-class-unknown.json')"
    ;;
  SC-05N)  # 음성 대조 — 건너뜀 갈래를 끈 스크립트 사본(구현을 되돌린 판)이면 슬라이서 없는 사본에서 불일치 · 종료 코드 1
    s=$BK/evals/run-gate-fixtures.sh
    [ -f "$s" ] || { echo "no_script"; return 0; }
    [ -f "$T/skill-noapp.md" ] || sed 's#/Applications/#/nonexistent-apps/#g' "$BS/SKILL.md" > "$T/skill-noapp.md"
    sed -E 's/^( *)elif \[ "\$expect" = fail \] && printf/\1elif false \&\& [ "$expect" = fail ] \&\& printf/' "$s" > "$BK/evals/run-gate-fixtures.noskip.sh"
    out=$( (cd "$E" && BAMBU_GATE_SKILL="$T/skill-noapp.md" bash "$BK/evals/run-gate-fixtures.noskip.sh") 2>&1); rc=$?
    echo "noskip mut=$(diff "$s" "$BK/evals/run-gate-fixtures.noskip.sh" | grep -cE '^>') rc=$rc bad=$(printf '%s\n' "$out" | grep -c '^불일치 ') skip=$(printf '%s\n' "$out" | grep -c '^건너뜀 ') match=$(printf '%s\n' "$out" | grep -c '^일치 ')"
    ;;
  ER-01)  # 시험 파일 실행 스크립트 — 완료 검사를 못 뽑으면 STOP · 종료 코드 2
    : > "$T/empty-skill.md"
    out=$( (cd "$E" && BAMBU_GATE_SKILL="$T/empty-skill.md" bash "$BK/evals/run-gate-fixtures.sh") 2>&1); rc=$?
    echo "rc=$rc stop=$(printf '%s\n' "$out" | grep -c '^STOP') match=$(printf '%s\n' "$out" | grep -c '^일치 ')"
    ;;
  SK-05)  # CI 한 단계가 두 스크립트를 돌린다 (KBa-2)
    "$PY" -c 'import yaml' 2>/dev/null || { echo "[미검증] SK-05 yaml_unavailable (PyYAML 없음 — pip install pyyaml 뒤 다시)"; return 2; }
    "$PY" - "$E/.github/workflows/ci.yml" <<'PY'
import sys, yaml
d = yaml.safe_load(open(sys.argv[1], encoding="utf-8"))
steps = d["jobs"]["validate"]["steps"]
gate = [s for s in steps if "bambu-kit/evals/run-gate-fixtures.sh" in str(s.get("run", ""))]
both = [s for s in gate if "bambu-kit/evals/makerworld-fetch-test.sh" in str(s.get("run", ""))]
alls = sum(1 for j in d["jobs"].values() for s in j.get("steps", []) if "bambu-kit/evals/" in str(s.get("run", "")))
print(f"gate_steps={len(gate)} both={len(both)} all_bambu_steps={alls}")
PY
    ;;
  SK-06)  # [미검증] 네 칸 — 생성 측 다섯 자리 (KBa-4)
    f=$BS/SKILL.md; r=$BS/references/failure-recipes.md; c=0; miss=""
    for a in '| 둘 다 미설치 |' '**ER-01 — 버전 조회에 실패하면**' '부모에 위임하는 쪽이 틀린 숫자보다 안전하다' '위 명령을 실행하지 않았거나 실행할 수 없었다면'; do
      if [ "$(para "$a" "$f" | n '네 칸')" -ge 1 ]; then c=$((c+1)); else miss="$miss [$a]"; fi; done
    if [ "$(para '조회에 실패하면 추측값을 쓰지 말고' "$r" | n '네 칸')" -ge 1 ]; then c=$((c+1)); else miss="$miss [failure-recipes]"; fi
    echo "spots=$c/5 def=$(para '위 명령을 실행하지 않았거나 실행할 수 없었다면' "$f" | all '막는 것' '시도한 우회' '통제 불가 사유' '재검증 명령' 'skill-design-guide.md')${miss:+ miss=$miss}"
    ;;
  SK-07)  # 현행화 — 뱀부 판 번호 · PLA Pure · 릴리스 현황 줄 (KBa-4)
    fb=$BS/references/bambu-fields-baseline.md
    echo "beta=$(sed -n '1,30p' "$fb" | grep -i 'latest beta' | all 'v02.08.04.57' '2026-09-22') stable=$(sed -n '1,30p' "$fb" | all 'v02.08.02.61' '2026-08-21') pure_old=$(grep '^1\. \*\*PLA Pure\*\*' "$BS/references/materials.md" | n '2.6.0 stable에는 미포함') pure_new=$(grep '^1\. \*\*PLA Pure\*\*' "$BS/references/materials.md" | n '02.08.02.61') rel=$(grep '^> \*\*릴리스 현황' "$BS/SKILL.md" | all '2026-09-27' 'v02.08.04.57' 'v02.08.02.61') rel_old=$(grep '^> \*\*릴리스 현황' "$BS/SKILL.md" | n 'v02.08.01.55')"
    ;;
  SC-06)  # 금지 키 시험 파일 (KBa-4)
    fx=bambu-kit/evals/gate-fixtures/process-forbidden-key.json
    [ -f "$E/$fx" ] || { echo "no_fixture"; return 0; }
    gate_of "$BS/SKILL.md" "$T/gate.py" >/dev/null
    o=$(gate_run "$T/gate.py" bambu "$fx")
    sed -E 's/^( *)if bad in d: errs\.append\(f"금지 키 .*$/\1pass/' "$T/gate.py" > "$T/gate.noforbid.py"
    o2=$(gate_run "$T/gate.noforbid.py" bambu "$fx")
    echo "fail=$(printf '%s\n' "$o" | grep -c '^FAIL') forbid=$(printf '%s\n' "$o" | grep -c '^FAIL process-forbidden-key.json: 금지 키 ') $(printf '%s\n' "$o" | tail -1) | mut=$(diff "$T/gate.py" "$T/gate.noforbid.py" | grep -c '^>') $(printf '%s\n' "$o2" | grep -c '^RESULT: PASS') $(printf '%s\n' "$o2" | tail -1)"
    echo "row=$(n '| `evals/gate-fixtures/process-forbidden-key.json` |' < "$BS/SKILL.md") runline=$(grep -E '^TARGET_SLICER=[a-z]+ +python3 "\$GATE" \$FX/process-forbidden-key.json;' "$BS/SKILL.md" | awk 'END{print NR}')"
    ;;
  SC-07)  # MakerWorld 받는 법 — 답글 수 · 403 (KBa-4). 알려진 답: 댓글 둘, replyCount 2+1=3, 받은 commentReply 2+0=2
    o=$(fetch_run "$BS/SKILL.md" 200)
    o4=$(fetch_run "$BS/SKILL.md" 403)
    echo "reply_line=$(printf '%s\n' "$o" | all '답글' 'replyCount 3' 'commentReply 2') $(printf '%s\n' "$o" | tail -1) | 403: fail_design=$(printf '%s\n' "$o4" | grep -c '^FAIL design.json') $(printf '%s\n' "$o4" | tail -1)"
    echo "table=$(secx '### JSON 주소' "$BS/SKILL.md" | all 'commentReply' 'replyCount' '관측 2026-09-27')"
    s=$BK/evals/makerworld-fetch-test.sh
    if [ -f "$s" ]; then out=$( (cd "$E" && bash "$s") 2>&1); rc=$?
      echo "test_rc=$rc $(printf '%s\n' "$out" | tail -1) c403=$(printf '%s\n' "$out" | grep -c '^일치 .*403') creply=$(printf '%s\n' "$out" | grep -c '^일치 .*답글')"
    else echo "no_test"; fi
    ;;
  SC-07N)  # 음성 대조 — 답글 줄을 지운 SKILL 사본이면 받는 법 시험이 불일치 (시험이 BAMBU_FETCH_SKILL 사본을 읽는다)
    awk 'index($0,"### JSON 주소")==1{h=1} h&&/^```bash$/{b=1} b&&/^```$/&&seen{b=0} {if(b) seen=1; if(!(b && /답글/)) print}' "$BS/SKILL.md" > "$T/skill-noreply.md"
    out=$( (cd "$E" && BAMBU_FETCH_SKILL="$T/skill-noreply.md" bash "$BK/evals/makerworld-fetch-test.sh") 2>&1); rc=$?
    echo "mut=$(diff "$BS/SKILL.md" "$T/skill-noreply.md" | grep -c '^<') rc=$rc bad_reply=$(printf '%s\n' "$out" | grep -c '^불일치 .*답글')"
    ;;
  SC-08)  # 음성 대조 블록이 임시 파일을 남기지 않는다 (KBa-4)
    neg_of "$BS/SKILL.md" "$T/neg.sh" >/dev/null
    leak_run "$T/neg.sh"
    ;;
  SK-08)  # tone adapter fallback_identifier_pattern 칸 (KT-1)
    f=$TK/references/adapter-dart-flutter.md; row=$(grep '^| `fallback_identifier_pattern` |' "$f")
    l4=$(secx '## 4. 완료 게이트' "$f" | awk '/^```text$/{b=1;next} b&&/^```$/{exit} b{i++; if(i==4) print}')
    echo "g04=$(printf '%s\n' "$row" | n 'G-04 줄이 정본') fourth=$(printf '%s\n' "$row" | all '넷째 줄' '코드 블록') line4_ok=$(printf '%s\n' "$l4" | n '(effective|resolved)')"
    ;;
  SK-09)  # dart-flutter-idioms 머리 판 · 페이지 머리 (KT-2)
    f=$E/docs/tone/dart-flutter-idioms.md; h=$E/docs/tone-kit/dart-flutter-idioms.html
    v=$(awk 'NR>1&&/^---$/{exit} /^version: /{print $2}' "$f"); d=$(awk 'NR>1&&/^---$/{exit} /^last_updated: /{print $2}' "$f")
    gt=$("$PY" -c 'import sys; a=tuple(map(int,sys.argv[1].split("."))); print(int(a>(0,1,0)))' "$v" 2>/dev/null || echo 0)
    echo "version=$v gt010=$gt last_updated=$d date_ok=$([ "$d" \> 2026-09-25 ] && echo 1 || echo 0) sub=$(n "v$v · 갱신 $d" < "$h") cap=$(n "<code>$v</code> · 최종 갱신 $d" < "$h") old_sub=$(n 'v0.1.0 · 갱신 2026-09-02' < "$h") old_cap=$(n '<code>0.1.0</code> · 최종 갱신 2026-09-02' < "$h")"
    ;;
  SK-10)  # 제스처 콜백 기준 판 — 3.38.4 만 적은 줄 0, 파일마다 3.47.5 줄이 시작 판 3.38.4 줄 수 이상 (KT-3 · EX-14)
    only=0; short=""
    for p in tone-kit/references/adapter-dart-flutter.md docs/tone/dart-flutter-idioms.md docs/tone/naming-taxonomy.md docs/tone-kit/dart-flutter-idioms.html docs/tone-kit/naming-taxonomy.html; do
      o=$(grep -F '3.38.4' "$E/$p" | grep -vcF '3.47.5' || true); only=$((only+o))
      b=$(n '3.38.4' < "$B/$p"); t=$(n '3.47.5' < "$E/$p"); [ "$t" -ge "$b" ] || short="$short $p($t<$b)"
    done
    echo "only_3384=$only short=[${short# }]"
    ;;
  SK-11)  # tone sources.md — go_router · 위키 이전 · K-11 근거 행 이름 (KT-3 · EX-14)
    f=$TK/references/sources.md
    echo "gor_rows=$(grep -c '^| go_router' "$f") gor=$(grep '^| go_router' "$f" | all '18.0.1' '2026-09-26') gor_note=$(all '17.0.0' '18.0.0' 'material_ui' < "$f") wiki_old=$(n 'wiki/Style-guide-for-Flutter-repo' < "$f") wiki_new=$(n 'blob/main/docs/contributing/Style-guide-for-Flutter-repo.md' < "$f") last3=$(n '위 표의 마지막 세 행' < "$f") k11=$(grep '^K-11' "$f" | all 'Microsoft' 'Google' '한글 맞춤법') lines1867=$(grep -rlF -e '1,867' -e '1867' "$TK" "$E/docs/tone" 2>/dev/null | awk 'END{print NR}')"
    ;;
  RE-01|RE-02)  # 새 스크립트 둘 — 머리에 사본 경로 환경 변수 · SKILL.md 원문을 뽑아 쓴다
    g=$BK/evals/run-gate-fixtures.sh; f=$BK/evals/makerworld-fetch-test.sh
    echo "gate_env=$( [ -f "$g" ] && sed -n '1,12p' "$g" | n 'BAMBU_GATE_SKILL' || echo 0) fetch_env=$( [ -f "$f" ] && sed -n '1,12p' "$f" | n 'BAMBU_FETCH_SKILL' || echo 0) fetch_anchor=$( [ -f "$f" ] && n '### JSON 주소' < "$f" || echo 0) fetch_copy=$( [ -f "$f" ] && n 'commentandrating?designId=$ID&offset=$OFF' < "$f" || echo 0)"
    ;;
  AR-01)  # 바뀐 파일이 기대 집합 안 · 커밋마다 맨 위 자리 하나
    ch=$(git -C "$W" diff --name-only "$BASE" "$TIP")
    extra=$(printf '%s\n' "$ch" | awk 'NF' | grep -vxF -- "$ALLOWED" || true)
    multi=0; for c in $(git -C "$W" rev-list --no-merges "$BASE..$TIP"); do
      k=$(git -C "$W" show --name-only --format= "$c" | awk -F/ 'NF{ if ($1=="docs") print $1"/"$2; else if (NF==1) print "(root)"; else print $1 }' | sort -u | awk 'END{print NR}')
      [ "$k" -gt 1 ] && multi=$((multi+1)); done
    echo "changed=$(cnt "$ch") extra=$(cnt "$extra") multi_top=$multi reflect=$(printf '%s\n' "$ch" | grep -c '^reflect-kit/' || true) bambu=$(printf '%s\n' "$ch" | grep -c '^bambu-kit/' || true) tone=$(printf '%s\n' "$ch" | grep -c '^tone-kit/' || true) docs_tone=$(printf '%s\n' "$ch" | grep -c '^docs/tone/' || true) github=$(printf '%s\n' "$ch" | grep -c '^\.github/' || true)"
    [ -n "$extra" ] && printf 'EXTRA %s\n' $extra
    ;;
  AR-02)  # notes 가 커밋돼 있고 토큰을 담는다 · 둘째 줄은 문서 페이지 드리프트 (전제: 작업 폴더 HEAD 가 TIP)
    f=$E/$NOTES; committed=$(git -C "$W" cat-file -e "$TIP:$NOTES" 2>/dev/null && echo 1 || echo 0)
    printf 'committed=%s' "$committed"
    for t in KRf-1 KRf-2 KRf-3 KRf-4 KRf-5 KBa-1 KBa-2 KBa-3 KBa-4 KT-1 KT-2 KT-3 EX-1 EX-14 '바깥 근거 없음' '처리됨' '실물 확인 필요' G91 'feat/bambu-kit-orca-h2s-feedback' C-06 'etc_seq=663' '`__`' 'err=' commentReply tone-guide ':1836-1846' ':1854-1872' ':1923-1941' ':1956-1985' ':2443-2444'; do printf ' %s' "$( [ -f "$f" ] && n "$t" < "$f" || echo 0)"; done; echo
    [ "$(git -C "$W" rev-parse HEAD)" = "$TIP" ] || { echo "PREMISE W_HEAD!=TIP"; return 2; }
    out=$(cd "$W" && "$PY" scripts/detect-docs-drift.py --since "$BASE" 2>&1); rc=$?
    pages=$(printf '%s\n' "$out" | grep -oE 'docs/[A-Za-z0-9_./-]+\.html' | sort -u)
    miss=0; while IFS= read -r p; do [ -z "$p" ] && continue; grep -qF -- "$p" "$E/$NOTES" 2>/dev/null || { miss=$((miss+1)); echo "MISS $p"; }; done <<< "$pages"
    echo "rc=$rc pages=$(cnt "$pages") miss=$miss"
    ;;
  DG-02)  # 더해진 줄의 markdownlint 새 경고 · 셸 검사 경고 수 · JSON 읽기
    mdl_ready || { echo "mdl_unavailable"; return 2; }
    md=0; for p in $(git -C "$W" diff --name-only "$BASE" "$TIP" -- '*.md' ':(exclude).harness/sprint-*'); do
      o=$B/$p; [ -f "$o" ] || o=/dev/null; [ -f "$E/$p" ] || continue
      md=$((md + $(newmd "$o" "$E/$p")))
    done
    sc=0; for p in $(git -C "$W" diff --name-only "$BASE" "$TIP" -- '*.sh'); do
      a=0; [ -f "$B/$p" ] && a=$(cd "$B/$(dirname "$p")" && shellcheck -f gcc "$(basename "$p")" 2>/dev/null | grep -c . || true)
      b=$(cd "$E/$(dirname "$p")" && shellcheck -f gcc "$(basename "$p")" 2>/dev/null | grep -c . || true)
      [ "$b" -gt "$a" ] && { sc=$((sc + b - a)); echo "SC_MORE $p $a->$b"; }
    done
    jb=0; for p in $(git -C "$W" diff --name-only "$BASE" "$TIP" -- '*.json'); do "$PY" -m json.tool "$E/$p" >/dev/null 2>&1 || jb=$((jb+1)); done
    echo "md_new=$md sc_new=$sc json_bad=$jb"
    ;;
  *) echo "모르는 조건 $1"; return 2 ;;
  esac
}
mdl_ready() {  # markdownlint-cli2 0.23.2 · MD013 끔 — 편집기 확장과 같은 설정
  MDL=${MDL:-$T/mdl}
  [ -x "$MDL/node_modules/.bin/markdownlint-cli2" ] || { mkdir -p "$MDL" && (cd "$MDL" && npm install --no-save --no-audit --no-fund markdownlint-cli2@0.23.2 >/dev/null 2>&1); }
  printf '{ "config": { "MD013": false } }\n' > "$MDL/cfg.markdownlint-cli2.jsonc"
  [ -x "$MDL/node_modules/.bin/markdownlint-cli2" ]
}
added() { diff -U0 "$1" "$2" | awk '/^@@/{split($3,a,","); s=substr(a[1],2); c=(a[2]=="")?1:a[2]; for(i=0;i<c;i++) print s+i}'; }
newmd() {  # newmd <옛 파일|/dev/null> <새 파일> — 새 파일에서 더해진 줄에 걸린 경고 수
  ( cd "$(dirname "$2")" && "$MDL/node_modules/.bin/markdownlint-cli2" --config "$MDL/cfg.markdownlint-cli2.jsonc" "$(basename "$2")" 2>&1 ) \
    | awk -F: '/^[^ ]+:[0-9]+/{print $2+0}' | sort -u > "$T/w.txt"
  added "$1" "$2" | sort -u > "$T/a.txt"
  comm -12 "$T/w.txt" "$T/a.txt" | grep -c . || true
}
# === 측정 도우미 끝 ===
```
