# 카이젠 2026-09-24 Phase 10 (react-kit) — notes

- 계약: `.harness/sprint-contract-kaizen-0924-p10-react-kit.md` (조건 29 · 기능 조건 19, 봉인 `sha256:4cae0f566fefc37d` · `locked_at` 2026-09-25 08:06)
- 개정: `.harness/sprint-amendments-kaizen-0924-p10-react-kit.md` (조건 변경 0 건, `end_sha` 만)
- 검토: `.harness/.meta/kaizen-0924/phase10-review.md` (1 회차 CHANGES 고칠 것 둘 · 권장 여덟은 초안이 반영, 2 회차 CHANGES 고칠 것 하나 · 권장 둘은 BUILD 가 봉인 전에 반영)
- 시작 커밋 `4a8ec55f4d874eaaed083af9621f9679693cbdb6`
- 계약 피드백: `~/.harness/feedback/contract/5a24cc99-2026-09-25T080915-de8c7935-77235.yaml` (`verify-feedback.sh` PASS). 초안은 `.harness/feedback-draft-p10.yaml` 로 갈라 썼다

## 커밋

| 커밋 | 내용 | 파일 |
| --- | --- | --- |
| `9d49bac` | 봉인 커밋 | 계약 1 개 |
| `ec4f530` | research-log 2026-09-25 항목 · g4-quality `--clean` 주석 | `docs/react/` 둘 |
| `001c900` | 렌더 증거 규약 1.1.0 · 편집 전 Gotcha · 포트 고정 · 시험 수 · `--clean` 분리 · project-detect 두 결함과 시험 · 현행화 · 평가 사례 넷 | `react-kit/` 열일곱 |
| `e673469` | 개정 파일에 `end_sha` (`001c900`) | 개정 1 개 |
| 이 파일의 커밋 | notes · 검토 기록 | `.harness/` 두 개 |
| 그다음 커밋 | 개정 파일에 notes 커밋 sha 로 `end_sha` 한 줄 더 | 개정 1 개 |

모든 커밋 메시지 끝 문단에 `Kaizen-Phase: kaizen-0924-p10-react-kit` 줄이 있다. 구현 커밋은 `git add -- <파일…> && git commit -o -- <파일…>` 로 내 경로만 실었다.
**FIX 가 커밋을 더할 때도 서명 줄을 넣고, 개정 파일에 `end_sha:` 줄을 덧붙인다.**

구현은 초안의 모의 편집(스크래치 `p10d/mock.py`, 지문 앞 16 자리 `db181ec91592e78d`)을 작업 폴더에 그대로 돌렸다. 돌리기 전에 `react-kit` · `docs/react` 에 미커밋 변경이
없는 것을 봤고, 같은 스크립트를 `HEAD` 판 새 사본에 먼저 돌려 `mock applied 45` 를 본 뒤 작업 폴더에서도 `mock applied 45` · 종료 코드 0 이 나왔다.
작업 폴더 결과는 새 사본 결과와 `diff -r` 로 같았다.
29 조건 측정은 봉인 커밋 판 계약에서 뗀 묶음으로 돌렸다 — 스크래치 `p10b/ks/`(`common.sh` · `m.sh` · `new-warnings.sh`, 2 회차 검토 판 `p10r2/k3/` 와 `cmp` 로 같다) ·
`p10b/run.sh`(공통 정의를 `.` 로 읽고 `TMPDIR` 를 스크래치로 둔 뒤 `type` 으로 도우미 다섯을 확인하고 `m <조건 ID>`). QA 가 같은 묶음을 다시 돌릴 수 있다.

## 바꾼 파일

- `react-kit/references/render-evidence-protocol.md` 1.0.0 → 1.1.0 — 편집 전과 완료 직전 두 번 실행, 형제 규약 숫자 문단, 2026-09-24 사고 문단, §1 Step 0 여섯 줄(되말하기 · 화면 자체 · 관례 표),
  §2 `[미검증]` 네 칸 · `### 비교 반복 순서 — 지금 보는 화면이 이번 코드인가` · `### 캡처 점검 목록` · `### 도구가 고장이라 말하기 전에`, §4 체크리스트 새 줄 일곱, References 넷
- 다섯 UI 스킬 `react-screen` · `react-widget` · `react-skeleton` · `react-responsive` · `react-animation` — 증거 Gotcha 의 `[미검증]` 을 네 칸으로, 다음 번호에 `**기준 캡처는 편집 전에 찍는다**` Gotcha.
  react-animation 은 고치는 줄에 걸린 옛 문구 「호출된다는 사실」 도 고쳤다
- `react-kit/skills/react-test/SKILL.md` Gotcha 14 · `react-kit/references/common-gotchas.md` G11 — 네 칸
- `react-kit/templates/vite.config.template.ts` — `strictPort: true` 와 이유 주석
- `react-kit/skills/react-run/SKILL.md` — `dev` 포트 Gotcha · test 결과 Gotcha · Report Format 시험 수 줄 · Rules MUST
- `react-kit/skills/react-preflight/SKILL.md` — test 줄 `✓ (N passed · 0 skipped)` · 두 `[미검증]` 줄 · Rules MUST
- `react-kit/skills/react-l10n/SKILL.md` — 기본 흐름에서 `--clean` 을 빼고 `#### 4-1. 안 쓰는 키 정리 — 사용자가 요청할 때만` · Gotcha 12
- `react-kit/skills/react-init/SKILL.md` — 버전 문장 셋(React · resolvers · Lingui 조회값), `### 단계 10` devUrl 포트 맞춤 줄
- `react-kit/skills/react-widget/SKILL.md` · `react-kit/skills/react-form/SKILL.md` — 버전 문장 하나 · 둘
- `react-kit/scripts/project-detect.sh` — `"null"` 비교와 역슬래시 붙은 jq 필드 경로, 이유 주석 두 줄
- `react-kit/evals/scripts/project-detect-test.sh` (새 파일, 모드 `100755`) — 세 입력 × jq · python3 두 경로 알려진 답 시험
- `react-kit/evals/evals.json` — 사례 2 · 13 · 18 · 20 에 새 단언 하나씩
- `docs/react/research-log.md` 1.3.0 → 1.4.0 — `## [2026-09-25] - Phase 10 kaizen (렌더 증거 반영 확인 · 조용한 통과)` 항목
- `docs/react/kit-design/g4-quality.md` — `--clean` 줄 주석을 react-l10n §4-1 로

스킬 머리 설정은 열하나 모두 그대로다(AP-04). react-kit README 는 건드리지 않았다 — `sync-docs.py --check-only` 는 「모든 README가 동기화 상태입니다」.

## 반영한 처리 배정표 키

| 키 | 반영 |
| --- | --- |
| `F03` · `other-kits:P1` | 규약 §2 비교 반복 순서 — 주소 대조 · 표식으로 판정 · 새로고침 → 서버 다시 띄우기 → wasm-build · 확인 전 「갱신했다」 금지 · 최대 3 회. 템플릿 `strictPort: true`, react-run `dev` 포트 Gotcha, react-init devUrl 줄 (SK-02 · SK-06 · SK-07) |
| `F05` | 규약 §2 「도구가 고장이라 말하기 전에」 세 확인 — 인자 이름 · 연 페이지가 내 서버인지 · 따로 뜨는 층 (SK-03) |
| `F01` (리액트 쪽) | 규약 §1 되말하기 · 화면 자체 · 관례 표 (SK-01). 배정 행 자체는 Phase 6 몫 |
| `other-kits:P2` | `project-detect.sh` 를 지우지 않고 고쳤다 — 설계 문서 `docs/react/kit-design/final-integration.md:243` · `:482` 가 킷 구성으로 적는다. 알려진 답 시험이 두 번째 결함(역슬래시 붙은 jq 경로)을 찾았다 (ER-01) |
| `other-kits:P5` | react-run · react-preflight 에 passed · skipped 두 수, 0 passed · skipped 1 이상은 `[미검증]`, `.only` 세기. react-build 는 test 단계가 없어 그대로 (SK-08) |
| `other-kits:P6` | react-l10n 기본 흐름에서 `lingui extract --clean` 을 빼고 요청할 때만 도는 §4-1 · Gotcha 12 (SK-09) |
| Phase 1 넘김 `render-evidence-protocol.md:59` | 「`[미검증]` 마커와 사유 한 줄」 을 여덟 자리(규약 · 다섯 UI 스킬 · react-test · common-gotchas)에서 네 칸으로 (SK-04) |
| Phase 6 넘김 | 되말하기 · 관례 표 · 반영 확인 · 캡처 점검 · 3 회 상한 — 숫자는 flutter · design 규약과 같게 규약 한 곳에만 (SK-01 ~ SK-05 · RE-02) |
| 근거 §3 현행화 | 지금 틀린 문장 여섯 줄만 조회값으로(React 19.3.0 · resolvers 5.9.1 · Lingui 6.8.0 · RHF 7 라인). Lingui v5 pin 은 그대로 (SK-10) |

## 미반영 키와 사유

- `F09` 비고 · Phase 4 넘김 — `react-preflight` 에 기준 커밋 비교를 넣는 일. 이 Phase 근거 파일에 기준 커밋 비교 근거가 없다(`git merge-base` 근거는 Phase 4 근거 파일 몫). Phase 5 도 같은 사유로 flutter-preflight 를 넘겼다
- `react-kit/references/project-detection.md:28` 의 `"vite": "8.2.0"` — 출력 모양을 보이는 예시라 현행 버전을 주장하지 않는다. 그대로 뒀다
- react-screen Gotcha 11 의 `<Activity />` 「canary」 서술 — 근거 파일에 `<Activity />` 상태 근거가 없다. 그대로 뒀다
- agent 가이드 §10 `[미검증:ENV]` · `[미검증:INVALID]` — react-reviewer 복제 조항(`UNVERIFIED_ENV`, `react-reviewer.md:268`)과 react-audit 미검증 절은 평가 측 판정 문턱을 바꾸는 별도 관심사다. Phase 6 도 design-reviewer 를 같은 사유로 넘겼다
- 조사 기록 backlog `react-view-transitions` — React 19.3 에서 `<ViewTransition>` 이 stable 이 되어 「canary 대기」 는 풀렸다. react-animation Tier 2 를 옮기는 것은 새 내용이라 조사 기록 표에만 적었다

그대로 둔 곳과 이유:

- `react-kit/skills/react-audit/SKILL.md:279` 의 「<사유> / 시도한 fallback」 과 `react-kit/agents/react-reviewer.md:183` — 복제 조항 5 의 보고 모양이라 그대로 둔다. 평가 측이 네 칸으로 옮길지는 위 `UNVERIFIED_ENV` 줄과 같이 정한다
- `react-kit/scripts/project-detect.sh` 를 부르는 스킬이 없다. 킷이 이 스크립트를 쓰게 할지(`react-kit/references/project-detection.md` 절차와 합칠지)는 다음 사이클 판단이다
- react-run · react-preflight 의 시험 수 `[미검증]` 은 네 칸을 붙이지 않았다 — 규약 §3 (b)(c) 의 「비어 있는 증거 범위」 표시이고, 네 칸은 §2 의 환경상 불가에 붙는다

ER-04 넷째 값(공유 파일 · 다른 Phase 파일을 건드린 커밋 가운데 다른 Phase 서명이 없는 커밋 수)이 0 이 아니면 QA 가 그 커밋 목록부터 보고 판정한다 —
그 값은 다른 Phase 가 서명 줄을 단다는 전제에 기댄다.

## 넘기는 것

| 대상 | 누가 | 할 일 |
| --- | --- | --- |
| `.github/workflows/ci.yml` | Final | 새 시험을 돌릴 줄 `bash react-kit/evals/scripts/project-detect-test.sh` 를 넣는다. jq · python3 가 있어야 하고 없으면 종료 코드 2 로 멈춘다 |
| `react-kit/.claude-plugin/plugin.json` | Final | react-kit 버전(지금 0.3.0). 규약 틀 · 보고 형식 · 템플릿 기본값(`strictPort`) · react-l10n 기본 흐름이 바뀌었다 |
| `docs/react-kit/render-evidence-protocol.html` | Final F2 | `v1.0.0 · 2026-07-27` 판으로 남아 있다. `scripts/detect-docs-drift.py` 가 `react-kit/references/` → `docs/react-kit/` 로 이어 이 페이지를 잡는다 |
| `docs/react/kit-design/g6-build-audit.md` | 다음 사이클 | dev 포트(`:52`)와 preflight 절(`:144-206`)이 초판(2026-04-10) 뒤 스킬 변경을 따라가지 않았다 |
| `.claude/skills/react-kaizen/SKILL.md` | 다음 사이클 | Step 6 의 계약 경로(`.harness/history/…`)와 「병렬 실행 중 git 쓰기 금지」 가 지금 러닝북(슬러그 계약 · 내 경로만 커밋)과 어긋난다. 레포 전용 파일이라 이 Phase 범위 밖이다 |
| `scripts/check-stale-values.py` | 다음 사이클 Phase 4 | `SOURCE_DIRS` 에 `react-kit/references` 가 없다 — 이 Phase 열아홉 파일 가운데 `docs/react/` 둘만 옛 값 검사를 받는다 |

Final 이 더 할 것: 이 Phase 는 공유 파일(marketplace · `plugin.json` · 루트 README · 루트 CLAUDE.md · `docs/` HTML · 감사 기록 · 실패 횟수 파일 · 처리 배정표 ·
`.github/workflows/ci.yml` · `.harness/stale-values.yaml`)을 건드리지 않았다.

## changelog 한 단락

react-kit 의 렌더 증거 규약이 완료 직전만이 아니라 편집 전에도 돈다. 편집 전에 요청을 대상 요소와 배치까지 넣어 되말하고, 화면을 가리키면 그 화면의 라우트와
화면 컴포넌트를 대상으로 적고, 같은 역할 기존 화면 2 개 이상으로 관례 표를 만든다. 완료 직전에는 개발 서버 `Local:` 주소와 브라우저가 연 주소를 대조하고,
기준 캡처 때 정한 표식이 새 캡처에서 바뀌었는지로 반영을 판정한다 — 새로고침 성공이나 모듈 교체 로그만으로는 판정하지 않고, 반영 전에는 「갱신했다」 고 말하지 않는다.
캡처 점검 목록 넷과 도구를 고장이라 말하기 전 세 확인이 붙고, `[미검증]` 은 설계 가이드와 같은 네 칸으로 적는다. Vite 템플릿에 `strictPort: true` 를 넣어
5173 이 차 있으면 조용히 다른 포트로 옮기지 않고 멈춘다. react-run · react-preflight 는 시험 결과를 passed · skipped 두 수로 적고 0 개 실행이나 skip 이 있는 실행을
통과로 적지 않는다. react-l10n 은 `lingui extract --clean` 을 기본 흐름에서 빼 사용자가 요청할 때만 돈다. `project-detect.sh` 가 TanStack Router 플러그인 유무를
늘 틀리게 읽던 두 결함을 고치고 알려진 답 시험을 더했다. 낡은 버전 문장 여섯 줄을 2026-09-24 조회값으로 고쳤다.

## 킷 로그 한 단락

2026-09-25 react-kit (카이젠 2026-09-24 Phase 10) — 처리 배정표 Phase 10 행 여섯(`F03` · `F05` · `other-kits:P1` · `other-kits:P2` · `other-kits:P5` · `other-kits:P6`)과
`F01` 리액트 쪽, Phase 1 · 6 넘김을 두 관심사(지금 보는 화면이 이번 코드인가 · 검사가 조용히 통과로 보이는 자리)로 받았다. 기록은 `docs/react/research-log.md` 1.4.0 항목이다.
근거: [Vite server.port · strictPort](https://vite.dev/config/server-options.html#server-port) · [Vite CLI](https://vite.dev/guide/cli) ·
[Tauri Vite 설정](https://v2.tauri.app/start/frontend/vite/) · [Vitest passWithNoTests](https://vitest.dev/config/passwithnotests) · [Vitest allowOnly](https://vitest.dev/config/allowonly) ·
[Vitest API](https://vitest.dev/api/) · [Lingui CLI](https://lingui.dev/ref/cli) · [GNU Bash 조건식](https://www.gnu.org/software/bash/manual/html_node/Bash-Conditional-Expressions.html) ·
[React 19.3 발표](https://react.dev/blog/2026/09/09/react-19-3) · [Lingui v6 migration](https://lingui.dev/releases/migration-6).

## 다음 사이클 메모

- 세 규약(design visual-change-protocol · flutter visual-evidence-protocol · react render-evidence-protocol)이 같이 쓰는 숫자(2 개 이상 · 3 회)의 정본 절은 harness `skill-design-guide.md` 에 아직 없다. 생기면 react 규약의 형제 숫자 문단을 그 절 인용으로 바꾼다
- 규약이 react-run Gotcha 를 머리 글자(`dev` 포트는 5173 에 묶여 있다)로 가리킨다. 그 Gotcha 머리를 바꾸면 이 계약 AR-02 첫 값이 떨어진다
- 설계 문서 `docs/react/kit-design/` 가 초판 뒤 스킬 변경을 따라가지 않는다(`g6-build-audit.md` 외). 한 번에 현행화할지, 초판 기록으로 둘지 정한다
- `scripts/check-stale-values.py` 의 `SOURCE_DIRS` 에 `react-kit/references` 가 없다(Phase 4 몫)
- Phase 8 계약 DG-05 의 「stale_rc 는 0 또는 1」 과 Phase 9 계약 DG-05 (c) 의 「종료 코드 0 또는 1 이고 출력에 열한 파일 경로가 0 건」 은 검사기가 멈춰도 통과한다 —
  이 계약은 검사기가 돌았다는 줄(`검사 범위: 소스 디렉토리`)을 함께 센다(2 회차 검토가 등록 파일을 지운 사본으로 확인). contract-schema 권장 형태로 올릴 만하다
- react-animation Tier 2 를 React 19.3 `<ViewTransition>` 으로 옮길지 — `react-view-transitions` backlog 를 다시 본다
