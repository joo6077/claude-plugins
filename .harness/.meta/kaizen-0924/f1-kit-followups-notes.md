# 카이젠 2026-09-24 Final — kaizen-0924-f1-kit-followups notes

- 계약: `.harness/sprint-contract-kaizen-0924-f1-kit-followups.md` (조건 30 · 기능 조건 20, 봉인 `sha256:d165f830e0906f4b` · `locked_at` 2026-09-25 17:34)
- 개정: `.harness/sprint-amendments-kaizen-0924-f1-kit-followups.md` (조건 변경 0 건 · 산문 변경 0 건. 구현이 개선안과 다른 곳 0 건)
- 검토: `.harness/.meta/kaizen-0924/f1-kit-followups-review.md` — 1 회차 `VERDICT: CHANGES`(고칠 것 C1 ~ C8)는 DRAFT 가 반영했다.
  2 회차 `VERDICT: CHANGES`(고칠 것 R1 · R2)는 BUILD 가 봉인 전에 넣었다. 새 측정은 SK-10 한 조건이고 검토가 준 측정 설계 그대로라 3 회차는 돌리지 않았다
- Codex 독립 검토 r2(`scratchpad/kaizen/codex/r2-kits-a.md`, 8 건) · r3(`r3-kits-b.md`, 6 건): 열은 조건(SK-03 (d) · SK-04 둘째 줄 · SK-05 넷째 줄 · SK-06 (c)(d) · SK-07 (d)(e) · SK-08 (d) · SK-12),
  넷은 고치지 않음 — 계약 입력 항목 표 67 ~ 80 행
- 사용자 승인 대체: 사용자 위임(세션 기록 queued_command `2026-09-24T04:04:16.964Z`) · Codex 한도 소진(2026-09-24) · 「코덱스 대신에 그냥 너가 알아서 진행하라고」(user `2026-09-24T11:54:58.940Z`) ·
  「코덱스도 사용할 수 있으니깐 사용해」(user `2026-09-25T06:19:45.056Z`) — REVIEW 에이전트 검토 두 회차와 Codex 검토로 대신했다
- 시작 커밋 `5b4fd72d5587c937c1875ddb62872f32ae087dcf`
- 계약 피드백: `~/.harness/feedback/contract/1a3bcba6-2026-09-25T174352-de8c7935-26848.yaml` (`verify-feedback.sh` PASS). 초안은 스크래치 `kaizen/f1kb/feedback-draft.keep.yaml`,
  `HARNESS_CONTRACT_ROOT` · `HARNESS_CONTRACT` 를 명시해 이 가지의 `save-feedback.sh` 로 저장했다 — 저장본 `project_name` 은 `claude-plugins`

## 커밋

| 묶음 | 커밋 | 조건 | 파일 |
| --- | --- | --- | --- |
| backend | `154916a` | SK-01 · SK-12 (a) | 연구 기록 · 감사 기준 · 시스템 원칙 · 원칙 문서 |
| infra | `cc11f71` | SK-01 · ER-02 · SK-12 (b) | 연구 기록 · gate-result-taxonomy · infra-test |
| rust | `c4eeef3` | SK-01 · SK-04 | 연구 기록 · rust-audit · rust-model · rust-preflight |
| planning | `cfef54f` | SK-01 | 연구 기록 |
| flutter | `535e143` | SK-02 | project-detection · visual-evidence-protocol · flutter-build · flutter-preflight · flutter-l10n |
| design | `37ac75f` | SK-03 | design-component · README · visual-change-protocol |
| react | `d6e30aa` | SK-05 | react-init · react-run · react-l10n |
| reflect | `3ac3f73` | SK-06 | SCHEMA · DESIGN · README · `_lib-project-id.sh` · `collect-status-test.sh` · reflect-digest · reflect-kaizen |
| bambu | `4868995` | SK-07 | bambu-print-profile |
| onboarding | `4595b8e` | SK-08 | setup-guide · 평가 파일 · 예제 |
| tone | `f93d715` | SK-09 | core-antipatterns |
| api | `9da098b` | SK-10 | api-ui · api-verify · snapshot-sealing-canonicalization |
| howto | `6de53a3` | SK-11 | 러너 · README · 평가 파일 |

- 봉인 커밋 `7223990` (계약 파일 1 개) · 개정 파일 `end_sha` 커밋 `d329ea5` · 이 파일의 커밋 · 그다음 `end_sha` 한 줄 덧붙임 커밋
- 모든 커밋 메시지는 `Co-Authored-By` 줄 바로 위에 `Kaizen-Phase: kaizen-0924-f1-kit-followups` 가 있다. 구현 커밋은 `git add -- <그 묶음 파일> && git commit -o -F <메시지> -- <그 묶음 파일>` 로 내 경로만 실었다.
  구현 커밋은 `.harness/` 를 싣지 않았고 러너 `howto-kit/evals/run-evals.sh` 의 git 모드는 `100755` 그대로다
- **FIX 가 커밋을 더할 때도 서명 줄을 넣고, 개정 파일에 `end_sha:` 줄을 덧붙인다**

측정: 봉인 판 계약에서 뗀 도우미(스크래치 `kaizen/f1kit/k/`, 계약 블록과 글자 그대로 같음)로 서른 조건을 돌렸다. 구현 끝 판 `6de53a3` 에서 ER-03 을 뺀 스물여섯이
봉인 전 실측 표 예행 판 값과 글자까지 같았다(`kaizen/f1kb/out-pre-amend.txt`). notes 를 올린 뒤 개정 파일 상한으로 서른 전부를 다시 돌린 값은 BUILD 보고에 적는다.

커밋 뒤 저장소 검사(러닝북 검증 절, 작업 폴더): `validate-plugin.py` 킷 열셋 각각 · 전체 종료 코드 0 · `— OK` · `— SKIP` 아닌 V 줄 0 ·
`sync-docs.py --check-only` 0 · `sync-evals.py --check-only` 0 · `run-evals.py` 0(115 passed) · `validate-post-kaizen.py --since 5b4fd72…` 는 `scope-isolation` ·
`doc-contracts` · `bare-fence` PASS, `docs-site-regen` FAIL(`kaizen-0924-final` F2 몫 — 계약 DG-06 이 판정에서 뺐다) · 킷 시험 reflect 셋 · howto 러너 · onboarding 러너 ·
`flutter-toolkit/evals/hooks/format-edited-dart-test.sh` · `scripts/test-collect-kaizen-data.py` 모두 종료 코드 0.

말투 대조(tone-guide Step 5, 레포 파일 `tone-kit/skills/tone-guide/SKILL.md` 와 코어 규칙표 · `locale-korean.md` 를 읽고 따름 — 어댑터 없음): 더한 줄 번역투 6 종(K-02) 0 (ER-02 `k02=0`) ·
C-01 — 새 주석은 이유만(주석 한 줄로 통과하던 검사 · 표면 없는 결정 통과 · `grep -c` 0 건 종료 코드 · 도중 멈춤을 놓침 · 옛 댓글 페이지 섞임 · enum 빠진 목록 · 반대 방향 · 셸 모델) ·
C-07 — 새 주석 블록은 2 줄 이하 · N-08 — 새 한 글자 이름은 reflect `collect_status` 의 `a` 와 onboarding G1 awk 의 `n` · `m` 뿐이고 둘 다 같은 함수의 기존 관례(`c f u p` · G4 awk 의 `st` · `ln`)를 따랐다(S-12) ·
K-11 — 새 합성어 0(「판정 줄」 · 「묶음 타겟」 은 검토 · 계약 글).

## 다룬 항목

조건 스무 개(SK-01 ~ SK-12)가 입력 항목 표의 「조건으로 다룸」 서른일곱 행을 덮는다.

- 교차 진단 DG-02 「뜻 기준 FAIL」 해소 — 연구 기록 넷(backend · infra · rust · planning)의 2026-09-24 소제목 여덟에 날짜를 붙여 같은 제목 경고(MD024)가 사이클 개시 판 수로 돌아갔다.
  사이클 동안 바뀐 킷 쪽 마크다운 136 개를 규칙별로 다시 비교해 는 규칙이 있는 파일 0 (입력 1 ~ 5 행)
- 교차 진단 「계약 밖」 결함 — flutter 넷(6 ~ 9 행) · design Gotcha 규약 인용(13 행) · infra 번역투(23 행) · rust `[미검증]` 네 칸(27 행) · react `strictPort`(30 행) ·
  reflect 도중 멈춤 · 태그 둘(35 · 37 행) · bambu enum 빠진 목록 · 반대 방향(40 · 41 행) · onboarding 값 든 파일 Grep · 평가 항목(45 · 46 행) · tone 죽은 grep 칸(49 행) ·
  api 서버 묶임 · `-0` · I-JSON 목록(54 · 55 행) · howto 펜스(58 행)
- notes 가 Final 로 넘긴 킷 몫 — design · reflect README 버전 줄(16 · 38 행) · onboarding 예제(47 행) · howto 러너 한 글자 변수(59 행)
- Codex r2 · r3 열 건 — backend 다섯 필드(67) · design 결정 게이트(68) · infra checkout(71) · rust-preflight fmt(72) · react-l10n `grep -c`(74) · reflect 도중 멈춤 · 실행 줄 일수(75 · 76) ·
  onboarding G1(77) · bambu 댓글 옛 페이지 · `SKILL_DIR`(78 · 79)
- 검토 2 회차 R1 — api-ui 서버 명령이 같은 호출 끝에 `SERVING pid=… dir=…` · `NOT_SERVING` 판정 줄을 찍고, 내릴 때는 그 번호로 `kill` 한다(다른 셸 호출의 `kill $!` 금지)

## 고치지 않은 항목과 이유

입력 항목 표의 「고치지 않음」 서른셋. 셋째 칸은 받을 곳이다(다음 사이클 메모와 같다).

| 행 | 항목 | 이유 · 받을 곳 |
| --- | --- | --- |
| 10 | P5 `widget-inspector.md` §7 제목 · 본문 | P5 계약 SK-05 (c) 가 일부러 둔 자리. flutter-feature 가 표 없이 부르는 흐름을 바꿀지부터 — 다음 사이클 Phase 5 |
| 11 | flutter-preflight · react-preflight 기준 커밋 비교 | 근거 파일에 기준 커밋 비교 근거가 없다 — 다음 사이클 Phase 5 · 10 |
| 12 | P5 go_router · auto_route · `--delete-conflicting-outputs` · flutter-audit `:50` · codegen 안내 셋 · 평가 사례 18 | P5 notes 가 다음 사이클로 보냈다(새 내용 · 근거 없음) |
| 14 | P6 RE-02 정규식 하이픈 | P6 계약 측정의 결함이지 킷 파일 결함이 아니다. 교차 진단 기록은 `kaizen-0924-final` |
| 15 | P6 임계값 다시 정의 | 세 규약 공통 절이 harness `skill-design-guide.md` 몫 — 다음 사이클 Phase 1 뒤 |
| 18 | P6 design:P2 · `UNVERIFIED_ENV` · design-mockup Step 0 · design-reviewer `[미검증]` 네 칸 · Material 3 · OKLCH | 사용자 확인 · 판정 문턱 변경 · 근거 없음 — 다음 사이클 Phase 6 |
| 21 | P7 OpenAPI 3.1 표기 · 벽시계 문자열 · 시간대 저장 · AsyncAPI 3.1.0 | 열린 질문 · 근거 없음 — 다음 사이클 Phase 7 |
| 24 | P8 판정 세 줄이 `docs/infra` 에만 | 원칙 문서 전부의 구조 문제 — 다음 사이클 |
| 25 | P8 Flux · Argo · Kubernetes 1.37 · GitHub 밖 CI · 세 분류 규범 · 1.7+ · `env_gaps` | 원칙 문서가 먼저 · 근거 없음 — 다음 사이클 Phase 8 |
| 26 | README 평가 사례 수 (infra 6 · backend 8) | 두 킷을 함께 정한다 — 다음 사이클 |
| 28 | P9 시각 판정 행 · 버전 리터럴 · testcontainers 0.27 | 기준 문서 자리 · breaking change · 행 삭제 결정 — 다음 사이클 Phase 9 |
| 29 | rust-kit 특정 앱 이름 66 곳 | 파일마다 확인하는 정리 — 다음 사이클 rust-kit 한 관심사 |
| 31 | P10 `harness-project.yaml.template` 복사 절차 없음 | 사이클 전부터 있던 것. 템플릿을 쓸지 지울지부터 — 다음 사이클 Phase 10 |
| 32 | P10 Activity canary · ViewTransition · react-reviewer §10 · `project-detect.sh` · `g6-build-audit.md` | 근거 없음 · 평가 측 문턱 · 설계 기록 결정 — 다음 사이클 Phase 10 |
| 33 | P11 planning-reviewer 기준 원본 사본 | harness 기준 원본 번호 정리가 먼저 — 다음 사이클 Phase 3 뒤 |
| 34 | P11 GitHub 문서 날짜 · Mermaid 12 · PRD 와 결정 기록 비교 | P11 notes 사유 그대로 |
| 36 | P12 `claude -p` 대체 경로가 사용자 훅을 띄움 | 추정이고 확인하려면 실제 훅이 뜬다. 효과를 재지 못한 옵션을 넣지 않는다 — 다음 사이클 Phase 12 |
| 39 | P12 `hooks.json` 따옴표 · `async` · `last_assistant_message` · 지워진 워크트리 | 킷 넷을 V8 검사와 함께 — 다음 사이클 Phase 4 · 12 |
| 42 | P13 `G91` 뒤 E 상대값 | 슬라이서 해석 관례를 이 세션에서 실측하지 못했다. 설치본 시작 G-code 가 `M83` 만 써서 영향이 없다 |
| 43 | P13 `[미검증]` 네 칸 다섯 자리 · 현행화 · 금지 키 FAIL 시험 파일 | 관심사 상한 · `/bambu-research` 소관 — 다음 사이클 Phase 13 |
| 44 | 올리지 않은 가지 `feat/bambu-kit-orca-h2s-feedback` 충돌 | 다른 가지. 이 계약이 같은 음성 대조 블록 (1) · 완료 검사 · 자기 검사 두 블록 · 댓글 받기 블록을 또 고쳤다 — 그 가지를 합칠 때 충돌 자리가 는다 |
| 48 | P14 `guide_gate` 세 칸 검사 · AUTO 표지 · CocoaPods → SPM · 서비스 계정 키 · 평가 날짜 | 예제를 고친 뒤 다음 사이클 Phase 14 |
| 50 | `adapter-dart-flutter.md:26` · `docs/tone/dart-flutter-idioms.md:633` 같은 모양 칸 | 값을 설명하는 칸이고 실제로 도는 명령은 `adapter-dart-flutter.md:245` 블록이다 |
| 51 | P15 연구 기록 「죽은 이름 검사 넷」 서술 | 날짜 붙은 이력 기록이라 두고, 표 칸 둘이 더 있었다는 사실을 아래 메모에 남긴다 |
| 52 | P15 C-06 강도 · `etc_seq=663` · `__` 예시 · 3.38.4 · go_router 링크 · 위키 이전 · `material_ui` · `locale-korean.md` §2 grep 열 · `sources.md` | 근거 재확인이 먼저. §2 grep 열은 여러 계약이 번역투 정규식 원문으로 베낀 자리 |
| 53 | P16 뷰어에 「판정 불가」 자리 없음 | 기준 시안 `.mockups/api-ui-v7.html` 이 `.gitignore` 라 이 작업 폴더에 없다 — 사용자 확인이 먼저 |
| 56 | `docs/superpowers/specs/2026-09-02-api-kit-design.md:249` | 날짜 붙은 설계 기록이라 이 계약 범위(킷 폴더 · 킷 원본 문서) 밖이고 결론은 맞다 |
| 57 | P16 `/api-contract` §9 예시 · CSP · §7 식 · 판정 불가 검사 | hurl 로 먼저 재거나 사용자 확인이 먼저 — 다음 사이클 Phase 16 |
| 60 | P17 howto-audit 리포트 미검증 칸 · DITA 2.0 · 러너 음성 대조를 킷 안에 · 러너 시간 · `design-brief.md:385` | P17 notes 사유 그대로 |
| 69 | Codex r2-3 — `design-reviewer.md:26` 미검증 사본이 옛 판 | 기준 원본이 여섯 항목이라 「5 조항 복제」 가 성립하지 않고, 옮기면 design-audit REJECT 문턱이 같이 바뀐다 — 다음 사이클 Phase 3 뒤 |
| 70 | Codex r2-4 — `planning-reviewer.md:22` 같은 옛 사본 · `:117` 없는 「4 요건」 | 69 행과 같다. react-kit · api-kit reviewer 도 같은 옛 사본이라 넷을 한 번에 |
| 73 | Codex r2-7 — flutter-build `--delete-conflicting-outputs` 판 번호 · 명령에서 빼기 | 심각도 낮음. 2.7.0 동작은 설치본 `build_runner-2.13.1` CHANGELOG `:149` · `:150` 으로 확인되고 킷 문장과 어긋나지 않는다. 2.16 쪽은 설치본이 없어 모른다 |
| 80 | Codex r3-6 — api-kit `-0` 을 「I-JSON 게이트」 로 분류 | RFC 7493 이 `-0` 을 금지하지 않는다는 본문이 근거 파일에 없다(확인 불가). 킷의 `-0` 줄은 이유를 JCS 로 적었다 |

그 밖에 이 계약이 다루지 않은 입력: 「다른 계약 몫」 여섯(17 · 22 · 63 · 66 행은 `kaizen-0924-final`, 64 · 65 행은 `kaizen-0924-f1-harness-followups`) ·
「이미 반영」 넷(19 · 20 · 61 · 62 행 — 파일에서 그 자리를 다시 확인했다).

## Final 에 넘기는 것

(a) 교차 진단 DG-02 해소 — Phase 7 · 8 · 9 · 11 개정 파일에 붙일 줄 넷:

- `kaizen-0924-p07-backend-kit` 개정 파일: 교차 진단 뒤 Final 에서 고침 — `154916a` (연구 기록 소제목 넷)
- `kaizen-0924-p08-infra-kit` 개정 파일: 교차 진단 뒤 Final 에서 고침 — `cc11f71` (연구 기록 소제목 둘)
- `kaizen-0924-p09-rust-kit` 개정 파일: 교차 진단 뒤 Final 에서 고침 — `c4eeef3` (연구 기록 소제목 하나)
- `kaizen-0924-p11-planning-kit` 개정 파일: 교차 진단 뒤 Final 에서 고침 — `cfef54f` (연구 기록 소제목 하나)

(b) 버전 계획(`release-plan.md`) — 플러그인 파일이 바뀐 킷 열둘, 모두 고침만이라 patch: `backend-kit` · `flutter-toolkit` · `design-kit` · `infra-kit` · `rust-kit` · `react-kit` ·
`reflect-kit` · `bambu-kit` · `onboarding-kit` · `tone-kit` · `api-kit` · `howto-kit`. planning 은 `docs/planning/` 연구 기록만 바뀌어 킷 버전 대상이 아니다.

(c) 다시 만들 문서 사이트 페이지 아홉 — `docs/onboarding-kit/fcm-ios-example.html` · `docs/flutter-toolkit/visual-evidence-protocol.html` · `docs/flutter-toolkit/project-detection.html` ·
`docs/api-kit/snapshot-sealing-canonicalization.html` · `docs/infra-kit/gate-result-taxonomy.html` · `docs/backend-kit/api-design.html` · `docs/design-kit/visual-change-protocol.html` ·
`docs/bambu-kit/bambu-print-profile.html` · `docs/reflect-kit/schema.html`. `docs/onboarding-kit/setup-guide.html` 은 이번에 바꾼 Gotcha 8 · G1 내용을 싣지 않아 목록에 없다 — 드리프트 매핑대로 다시 만들면 된다

(d) 그 밖에 `.harness/` 몫 — `.harness/stale-values.yaml` 의 OpenAPI 항목 allow(입력 22 행 · backend 감사 기준 `:26` 의 `OpenAPI 3.1.1` 인용 두 자리는 이번에 늘지도 줄지도 않았다) ·
`docs/design/research-log.md` 킷 로그 옮기기(17 행)

(e) changelog 한 단락:

킷 열두 곳의 후속 수정. 연구 기록 넷의 2026-09-24 소제목에 날짜를 붙여 같은 제목 경고를 없앴다. flutter-toolkit 은 묶음 타겟을 codegen 줄 자리에 넣지 않고 증거 블록 빈칸이 네 칸 미검증 줄을 가리킨다.
design-kit 결정 전파 게이트가 id · source 가 빠지면 2, 표면 목록이 비거나 제외 이유가 없으면 1, 표면이 0 개면 3 을 낸다. react-init 이 `strictPort` 를 실제 프로젝트에 넣는다.
reflect-kit 수집 상태가 엔트리가 있어도 마지막 기록 뒤의 Stop 실패를 경고하고 digest · kaizen 실행 줄이 요청한 일수를 쓴다. bambu-kit 완료 검사가 enum 빠진 목록을 `[미검증]` 으로 남기고
음성 대조가 반대 방향도 멈추며 댓글 받기가 옛 페이지를 지운다. onboarding-kit 은 Step 마다 출처 하나를 요구하고 값 든 파일을 Grep 으로 훑지 않으며 예제가 현행 요구와 세 칸 표를 따른다.
api-kit api-ui 는 서버를 뒤에서 띄우고 같은 호출 끝의 판정 줄로 포트 충돌을 가른다. howto-kit 러너가 `sh` · `shell` · `zsh` 펜스도 센다. backend · infra · rust · tone 은 감사 기준 · 시험 · 문구를 실제 규칙대로 고쳤다.

(f) 킷 로그 한 단락:

2026-09-24 사이클 Final — 킷 쪽 후속 수정(`kaizen-0924-f1-kit-followups`). 입력: 교차 진단 P5 ~ P17 · final-todo · Phase notes · Codex 독립 검토 r2 8 건 · r3 6 건 · REVIEW 검토 두 회차.
외부 근거는 사이클 근거 파일에서만 옮겼다 — Firebase Apple 셋업의 Xcode 26.2+ · 실제 Apple 기기 요구(https://firebase.google.com/docs/ios/setup, `phase14.md`),
Vite `strictPort`(https://vite.dev/config/server-options.html#server-port, `phase10.md`), RFC 8785 정정 7920 의 `-0`(https://www.rfc-editor.org/errata/rfc8785, `phase16.md`).
나머지는 저장소 안 실측 — backend 다섯 필드는 같은 레포 `docs/api/contract/error-status-contracts.md` §2, build_runner 2.7.0 동작은 설치본 CHANGELOG.

## 다음 사이클 메모

| 받을 곳 | 메모 |
| --- | --- |
| Phase 12 | reflect `⚠ 수집 멈춤 — 마지막 기록 뒤 Stop 실패 시도 N회` 는 수 문턱 없이 시각 순서로 가른다. 마지막 실행 한 번의 일시 실패에도 digest `## 승격 후보` 가 빈다 — 너무 자주 나오면 문턱(몇 회 · 며칠)을 정한다 |
| Phase 12 | `claude -p` 대체 경로가 사용자 훅을 띄운다는 교차 진단 추정(입력 36 행) — 실제 훅이 뜨지 않는 사본에서 먼저 잰다 |
| Phase 16 | api-kit 뷰어 「판정 불가」 상태(53 행) — 기준 시안 `.mockups/api-ui-v7.html` 을 사용자에게 확인받은 뒤 |
| Phase 16 | `-0` 을 「I-JSON 게이트」 에서 떼어 이름을 가를지(80 행) — RFC 7493 §2.2 원문을 근거 파일에 넣은 뒤 |
| Phase 16 | 설계 기록 `docs/superpowers/specs/2026-09-02-api-kit-design.md:249`(56 행) — 세 Final 계약 어느 범위에도 없다 |
| Phase 14 | onboarding G1 음성 입력(한 Step 에 출처 둘 · `misplaced`)을 킷 픽스처로 넣고 `gate_cases` 에 등록한다 — 이 계약은 임시 파일로만 쟀다 |
| Phase 15 | `adapter-dart-flutter.md:26` · `docs/tone/dart-flutter-idioms.md:633` 의 같은 모양 칸(50 행)과 `locale-korean.md` §2 grep 열(52 행). P15 연구 기록의 「죽은 이름 검사 넷」 서술에는 표 칸 둘이 더 있었다(51 행) |
| Phase 5 | `widget-inspector.md` §7(10 행) · `flutter-preflight` · react-preflight 기준 커밋 비교(11 행) · `--delete-conflicting-outputs` — build_runner 2.7.0 부터 `-d` 를 무시한다(설치본 `build_runner-2.13.1` CHANGELOG `:149` · `:150`). 2.16 은 설치본이 없어 모른다(73 행) |
| Phase 3 뒤 | `design-reviewer` · `planning-reviewer` · react-kit · api-kit reviewer 의 미검증 옛 사본 넷을 한 번에(69 · 70 행) — 기준 원본 여섯 항목 정리가 먼저 |
| Phase 13 | `G91` 뒤 E 상대값(42 행) — 설치본 시작 G-code 로 실측. 올리지 않은 가지 `feat/bambu-kit-orca-h2s-feedback` 을 합칠 때 이번에 고친 블록 넷과 충돌을 본다(44 행) |
| Phase 9 | rust-kit 특정 앱 이름(`fit-pal` 등) 66 곳 — 한 파일씩(29 행). rust-preflight Gotcha 1 에도 남아 있다 |
| Phase 10 | `harness-project.yaml.template` 복사 절차(31 행) — 템플릿을 쓸지 지울지부터 |
| Phase 8 | 판정 세 줄이 `docs/infra/platform/cicd.md` 에만 있는 구조(24 행) — 원칙 문서 전부를 함께 |
| 그 밖 | 입력 12 · 15 · 18 · 21 · 25 · 26 · 28 · 32 · 33 · 34 · 39 · 43 · 48 · 57 · 60 행은 위 표의 받을 곳 그대로 |
