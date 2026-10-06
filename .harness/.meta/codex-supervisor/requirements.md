# 요구사항 — Codex 계약 작성 · 구현 감독 (slug: codex-supervisor)

작성: Claude (2026-10-01, 세션 fb4aefa8-0ee1-4711-9b22-7baf9c6b989f). 이 문서는 사용자와 합의한 내용을 옮긴 것이다. 계약서는 이 문서를 받은 Codex 가 쓴다.

## 1. 사용자가 원하는 것

harness QA 플러그인의 역할을 이렇게 나눈다.

| 일 | 맡는 쪽 |
| --- | --- |
| 계약서(완료 조건) 쓰기 | **Codex** |
| 계약서 검토 · 봉인 전 승인 | **Claude 평가자**(`harness/agents/qa-evaluator.md`, 계약 검토 모드) — 그 뒤 사용자 승인 |
| 구현 | **Claude** |
| 구현 QA 최종 판정 | **Codex 단독**. Claude 는 자기 구현을 채점하지 않는다 |

사용자 결정 (2026-10-01 대화):

1. 감독관은 의견이 아니라 거부권이다. REJECT 면 **왜 실패했는지**와 **어떻게 고치는지**를 남기고, 고친 뒤 다시 감독받는다.
2. 구현 QA 는 QA 때마다 자동으로 돈다.
3. 인터넷 조사는 판정과 나눈다. Codex 가 「바깥 사실 확인이 필요하다」 는 질문을 낼 때만 조사 차례를 따로 돌려 그 답을 붙여 다시 판정한다. **(2026-10-06 개정)** 판정 차례도 인터넷을 연다 — 계약의 측정 명령 가운데 실제 Codex 를 부르는 것(실제 감독관 시험)을 판정 Codex 가 자기 격리 공간 안에서 직접 돌릴 수 있어야 하기 때문이다. 판정 지시문은 여전히 「바깥 사실은 스스로 찾지 말고 질문으로 내라」 고 하며, 조사 차례 분리는 그대로 둔다. 판정 차례의 쓰기는 여전히 복제 사본 · 임시 폴더 안으로만 막는다.
4. 고치고 다시 받는 반복은 **최대 2 회**. 넘으면 사용자 판단.
5. Codex 단독 REJECT 는 첫 판정을 숨긴 **새 세션 재심**을 한 번 거친다. 두 판정이 같은 조건을 FAIL 로 보면 확정, 엇갈리면 사용자 판단.
6. FAIL 조건마다 고칠 방법 세 칸 — **어디를 · 무엇으로 · 어떻게 확인** — 을 반드시 남긴다. 하나라도 비면 그 답은 무효.
7. 판정한 **실제 모델 이름과 생각 강도**를 결과에 남긴다.
8. 모델 이름을 스크립트에 박지 않는다. 감독용 Codex 폴더 설정을 따른다.
9. Codex 가 쓴 계약서를 Codex 가 검토하지 않는다(자기 글 후하게 보기 편향). 검토는 Claude 평가자.
10. Codex 를 못 돌리는 프로젝트를 위해 끄는 설정이 있다. 끄면 지금까지의 방식(Claude 가 계약 쓰기 · Claude 평가자 판정)으로 돈다.
11. **(2026-10-06 추가)** 감독용 Codex 폴더의 로그인은 macOS 키체인이 아니라 파일(`<감독 폴더>/auth.json`, 권한 600)에 저장한다. 판정 Codex 의 격리 공간은 키체인을 읽지 못하지만 파일은 읽는다. 사용자는 이로써 판정 중 실행되는 코드(구현물 · 측정 명령)가 키 파일을 읽고 인터넷으로 내보낼 수 있는 위험을 알고 받아들였다 — 키를 쓰는 곳 제한 · 사용 한도가 걸린 키를 권한다. 스크립트 · 보고서 · 감독 폴더의 어떤 파일도 키 글자를 담지 않는다는 규칙은 그대로다.

## 2. 리서치 결과 (Codex 위임 2 건, 2026-10-01)

- 답 모양은 `codex exec --output-schema <파일>` 로 강제한다(0.157.1 에 있음, 서버에 `strict: true` 로 간다). 단 조건 번호의 빠짐 · 겹침 · 없는 번호, PASS/FAIL 과 전체 판정의 일치, FAIL 의 고칠 방법 채움은 셸이 따로 검사한다. strict 형식은 모든 칸이 `required` 이고 `additionalProperties: false` 여야 하며 `allOf` · `if/then` 은 못 쓴다.
- 조건마다 **증거 → 분석 → 판정** 순서로 쓰게 한다(답 모양의 키 순서가 생성 순서다).
- 「엄격한 감사관」 같은 역할 말은 넣지 않는다 — 코드 검토 연구는 관대함(틀린 것 통과 75% 이상)을, 다른 연구는 「엄격」 역할의 과한 감점을 보였다. 대신 중립 증거 규칙: PASS 는 조건의 모든 부분이 충족됐다는 긍정 증거가 있어야, FAIL 은 반대 증거 · 빠진 증거 · 잴 수 없는 문구가 있어야.
- 판정 대상 글(계약 · 코드 · 주석) 안의 지시문은 데이터로 취급한다.
- 감독 실패는 REJECT 가 아니다. 성공 판정은 전부 만족해야 한다: 종료 코드 0 · `--json` 사건에 `turn.completed` 있음 · `turn.failed`/`error` 없음 · 결과 파일 있음 · JSON 으로 읽힘 · 답 모양 통과 · 번호 집합 일치 · 겹침 없음 · 판정 일관.
- 실패 대응: 멈춤 · 빈 응답 → 새 세션 1 회 다시. 한도 · 결제(`insufficient_quota` · usage limit) → 다시 하지 않고 알림. 설정 · 답 모양 오류 → 다시 하지 않음. Codex 안에서 이미 HTTP 4 회 · 스트림 5 회 다시 시도하므로 바깥 재시도를 늘리지 않는다.
- 생각 강도: 계약 쪽 `low` 부터, 구현 판정 `medium` 기본. 프롬프트는 짧게(공식 실측: 짧은 지시문이 점수 10~15% 올리고 토큰 41~66% 줄임). 예시를 잔뜩 붙이지 않는다.
- 운영 전에 답을 아는 좋은 예 · 나쁜 예로 감독관이 맞게 판정하는지 확인한다.

## 3. 봉인 전 실측 (이 맥, codex-cli 0.157.1, 2026-10-01)

- 감독용 폴더 `~/.codex-qa`: 설정 두 줄(`cli_auth_credentials_store = "file"` · `model = "gpt-6-astra"`), OpenAI 키 로그인(`Logged in using an API key`), 키는 `~/.codex-qa/auth.json`. (2026-10-01 에는 `keyring` 이었고, Codex 격리 공간 안에서는 키체인을 못 읽어 `Not logged in` 이 나오는 것을 계약 초안 작성 중 실측했다 — 그래서 2026-10-06 파일 저장으로 바꿨다. 키체인은 폴더 경로별 항목이라 폴더를 복사해도 로그인이 따라오지 않았다.) 평소 폴더 `~/.codex` 는 ChatGPT 로그인 그대로이고 기본 모델이 `gpt-5.6-luna`(가장 작음)라 모델을 지정하지 않고 부르면 안 된다.
- (2026-10-06 실측) 파일 저장으로 바꾼 뒤, Codex 격리 공간(`-s workspace-write` + 인터넷 허용) 안에서 `CODEX_HOME=~/.codex-qa codex login status` 는 `Logged in using an API key`. 그러나 안쪽에서 `CODEX_HOME=~/.codex-qa codex exec …` 는 `failed to initialize in-process app-server client: Operation not permitted` 로 시작조차 못 한다 — Codex 는 실행 중 자기 폴더에 써야 하는데 격리 공간이 그 폴더 쓰기를 막는다. 쓰기 가능한 임시 폴더를 만들어 `auth.json` · `config.toml` 을 복사하고(키 사본 권한 600) 그 폴더를 `CODEX_HOME` 으로 주면 안쪽 실제 호출이 12 초에 `PONG` 을 냈고 세션 기록 1 개가 생겼다. 키 사본은 끝나면 반드시 지운다.
- (2026-10-06 실측) Codex 격리 공간의 자동 승인 검사가 `rm -rf` 꼴 명령을 「rm -f style commands are not permitted」 로 거부해 명령 전체가 실행되지 않았다. 판정 Codex 가 돌릴 측정 명령에 지우기가 섞이면 판정이 막힐 수 있다.
- `--output-schema` 판정이 `gpt-6-astra` · effort low 로 8 초에 끝났다.
- 세션 기록(`$CODEX_HOME/sessions/YYYY/MM/DD/rollout-*.jsonl`)의 `type: turn_context` 줄 `payload` 에 `model`(gpt-6-astra) · `effort`(low) · `sandbox_policy` 가 남는다. `--ephemeral` 이면 기록이 안 남으므로 쓰지 않는다. 서버가 실제로 답한 모델은 어디에도 안 남는다 — 「실제 모델」 은 이 `turn_context.model` 이다.
- `--json` 첫 사건 `thread.started` 의 `thread_id` 가 세션 기록 파일 이름 끝(uuid)과 같다(같은 실행에서 확인할 것).
- `-s workspace-write -c sandbox_workspace_write.network_access=true -C <임시 폴더>`: 레포 파일 쓰기 `Operation not permitted`, 임시 폴더 쓰기 성공, `curl` 200.
- `--ignore-user-config` 는 감독용 폴더 설정까지 지워 키체인 로그인을 잃는다 — 쓰지 않는다. `--ignore-rules` · `--strict-config` 는 있다.
- stdin 은 반드시 닫는다(`</dev/null`). macOS 에 `timeout` 이 없어 상한은 `perl -e 'alarm shift; exec @ARGV' <초> …`. 죽일 때는 프로세스 트리 전체.
- 이 레포 harness 평가자는 서브에이전트라 명령 하나 상한이 10 분이다. 감독은 「시작(뒤에서 돌기)」 과 「기다리기」 로 나눠야 한다.
- 이전 실측(레포 기록 `qa-evaluator.md` Step 7): 서브에이전트에게 다른 감독을 직접 띄우게 했더니 띄우지도 않고 「띄웠다」 고 두 번 지어냈다. 그래서 Codex 호출과 결과 파일 쓰기는 **스크립트가** 하고, 에이전트는 읽기만 한다.

## 4. 제안 설계 (바꿔도 되지만 바꾸면 계약 `## 배경` 에 이유를 적는다)

새 파일 `harness/scripts/codex-audit.sh` 하나가 Codex 를 부르는 모든 일을 한다. 틀(지시문 · 답 모양 JSON)은 새 폴더 `harness/templates/codex-audit/`.

부속 명령:

- `draft <요구사항 파일> <계약 경로>` — Codex 가 계약서 본문과 측정 묶음을 쓴다. 계약 경로는 미리 선점된 **빈 파일**이어야 하고, 비어 있지 않으면 쓰지 않고 멈춘다(남의 계약을 덮지 않는다). 측정 묶음은 `<계약 폴더>/.harness/.meta/<slug>/` 에 둔다. Codex 는 임시 폴더 안에서만 쓰고 레포는 읽기만 한다. 다 쓰면 sprint-contract 의 저장 검사(헤더 허용 목록 · 서술 절에 조건 줄 없음 · 조건 수 일치 · `[미실측]` 0)를 스크립트가 돌려 결과를 남긴다.
- `revise <계약 경로> <지적 파일>` — 지적을 반영해 Codex 가 다시 쓴다. 봉인된 계약(`conditions_digest` 있음)은 고치지 않고 멈춘다. 이전 판은 지우지 않고 감독 폴더에 남긴다.
- `impl <계약 경로> <기준 커밋>` — 구현 감독. 계약 · 기준 커밋부터의 차이 · 목록 파일을 얼려 두고, 구현 커밋을 복제한 임시 사본(`git clone --shared` 등, 원래 작업 폴더의 `.git` 을 바꾸지 않는 방법)에서 Codex 가 측정 명령을 돌려 볼 수 있게 한다 — 쓰기는 사본 · 임시 폴더 안, 인터넷은 연다(2026-10-06 개정, §1 결정 3 · 11). 판정 차례가 감독용 폴더의 `auth.json` 을 읽을 수 있어야 측정 안의 실제 Codex 호출이 된다. 끝나면 `<계약 폴더>/.harness/sprint-feedback-<slug>.md` 를 스크립트가 쓴다(`Verdict:` 줄 · `Iteration:` 줄 · 조건별 결과 · 고칠 것). 이 레포의 QA 대기 훅 `harness/scripts/qa-pending-check.sh` 가 그 `Verdict:` 줄을 읽는다.
- `--detach` (draft · revise · impl 공통) — 감독 폴더 경로를 바로 찍고 뒤에서 돈다. `wait <감독 폴더> [초]` — 기다린다. 아직이면 `RUNNING` · 종료 코드 75.
- 종료 코드: 0 APPROVE(또는 draft · revise 성공) · 1 REJECT · 2 BLOCKED · 3 SKIPPED(설정이 꺼짐) · 64 쓰는 법 틀림.
- 감독 폴더: `<계약 폴더>/.harness/codex-audit/<slug>/<draft|impl>-r<N>/`. 사람이 읽는 `report.md` 의 머리는 스크립트가 쓴다 — `시작:` · `끝:` · `계정:`(`codex login status` 의 「using …」 부분만, 키 일부도 남기지 않는다) · 차례마다 `- 차례 <이름> 모델=<turn_context.model> 생각=<turn_context.effort> 격리=<sandbox_policy 종류> 기록=<세션 기록 경로>`. 마지막 줄 `감독 판정: <…>`. BLOCKED 면 `## 실패 원인` 에 `갈래: <이름>`, REJECT 면 `## 고칠 것` 에 FAIL 조건마다 `- <번호> 어디를: … · 무엇으로: … · 어떻게 확인: …`. 2 회차부터 `## 지난 판 지적 처리` 에 지난 고칠 것 번호마다 `해결` · `미해결`.
- 실패 갈래 일곱: `codex-없음` · `로그인-없음` · `시간-초과` · `빈-응답` · `형식-깨짐` · `한도-결제` · `설정-오류`. 운영 갈래: `재심-엇갈림` · `반복-상한` · `봉인됨`.
- 시험용 환경 변수: `CODEX_BIN`(부를 codex, 기본 `codex`) · `CODEX_AUDIT_LIMIT`(차례 하나 상한 초, 기본 600). 가짜 codex 시험은 실제 codex 실행 파일을 건드리지 않는다(바로가기를 덮어써 진짜 실행 파일이 0 바이트가 된 사고가 있었다).
- 설정: `.harness/project.yaml` 의 `codex_audit:` — `mode`(`codex` | `off`, 없으면 `codex`) · `codex_home`(없으면 `~/.codex-qa` 가 있으면 그것, 없으면 기본 폴더) · `model`(없으면 그 폴더 설정의 `model`. 둘 다 없으면 BLOCKED `설정-오류`) · `effort_draft`(없으면 `medium`) · `effort_impl`(없으면 `medium`) · `max_rounds`(없으면 2). 같은 칸을 새 프로젝트 틀 `harness/templates/project.yaml` 에도 넣는다.

문서 쪽:

- `harness/skills/sprint-contract/SKILL.md`: `mode: codex` 면 Claude 는 조건을 직접 쓰지 않는다 — 요구사항 파일을 쓰고 `draft` 를 부르고, 저장 검사 실패나 평가자 REJECT 는 지적 파일로 만들어 `revise` 를 부른다. 조건 줄을 Claude 가 손으로 고치지 않는다. `max_rounds` 를 넘기면 사용자에게 묻는다. 평가자 APPROVE 와 사용자 승인 뒤 기존 봉인(6.6) · 봉인 커밋(6.7). `mode: off` 면 지금 절차 그대로.
- `harness/agents/qa-evaluator.md`: 두 모드 — (가) 계약 검토 모드: APPROVE/REJECT 와 고칠 것 목록(조건 번호 · 문제 · 고칠 방법)을 낸다 (나) 구현 판정 모드에서 `mode: codex` 면 조건을 스스로 판정하지 않는다 — `impl --detach` 로 시작하고 `wait` 로 받아, 스크립트가 쓴 `sprint-feedback` 의 `Verdict:` 를 그대로 보고하고 APPROVE 면 계약 `status` 를 `done` 으로 바꾼다(기존 Step 5.5). 판정 낱말을 바꾸거나 덧붙이지 않는다. `mode: off` 면 지금 절차 그대로.
- `harness/README.md` 스크립트 표에 한 줄.

하지 않는 것: harness 버전 올리기 · 배포, 레포 밖 `~/.claude/bin/codex-research` 수정, Codex 기록 수집 훅을 `~/.codex-qa` 까지 읽게 바꾸기, Gemini.

## 5. 이 레포 계약 규칙 (반드시 읽고 따른다)

- 형식 정의: `harness/references/contract-schema.md` (특히 §허용 섹션 헤더 · §조건 번호 앞자리 · §조건 태그 · §검증 수단 인라인 명시 · §Diff-Scope Oracle 표준형 · §범위 목록 블록 · §미실측 오라클 봉인 금지 · §음성 대조 · §양성 대조 · §알려진 답 대조 · §인자 매트릭스 · §측정 관례 · §해당 없음 마커 · §4. Diagnostics · §복잡도별 조건 수 가이드).
- 작성 절차와 함정: `harness/skills/sprint-contract/SKILL.md` 의 Gotchas 와 Process 2 · 2.5 · 3 · 4.
- 설정: `.harness/project.yaml` — 카테고리 ID 와 번호 앞자리는 Skill/`스킬` · Script/`스크립트` · Error/`오류` · Architecture/`구조`. 금지 패턴 `금지-01`~`금지-04`. 값은 글자 그대로 옮긴다.
- 최근 계약 본보기: `.harness/sprint-contract-after-1001-hooks-into-harness.md`.
- frontmatter 의 `conditions_digest` · `measurement_digest` · `locked_at` 은 쓰지 않는다(봉인은 나중에 한다). `conditions:` 는 실제 조건 줄 수.
- 작업 폴더 W = `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/codex-supervisor`, 가지 `feat/codex-supervisor`, 시작 판 `BASE` = `88b2a84e`. 가지 이름이 `sprint/<slug>` 가 아니므로 커밋 구간 상한은 `git rev-parse --verify -q feat/codex-supervisor` 로 해석하고, 실패하면 멈춘다.
- 이 계약 자신은 `draft` 가 아직 없어 사람이 Codex 를 직접 불러 쓰게 한 것이다. 이 사실을 `## 배경` 에 적는다.

## 6. 개정 1 — 격리 밖 사전 측정 (2026-10-06)

첫 구현 감독(감독 폴더 `.harness/codex-audit/codex-supervisor/impl-r1`)이 REJECT 를 냈다. FAIL 셋(스크립트-11 · 오류-02 · 구조-04)은 구현 결함이 아니라 판정 격리 공간의 한계였다 — 격리 안에서 `ps` 가 `Operation not permitted` 로 막히고, 격리 안의 Codex 가 다시 Codex 를 부르면 macOS 가 격리를 겹쳐 만들지 못해 `sandbox_apply: Operation not permitted` 가 난다. 같은 세 조건은 격리 밖에서 모두 PASS 였다. 사용자는 세 선택지(사전 측정 기능 추가 · 이번만 사용자 판단 통과 · 판정 격리 넓히기) 중 「사전 측정 기능 추가 후 다시 감독」 을 골랐다(이 세션 기록의 사용자 답 「1」).

요구:

1. `impl` 은 판정 차례 전에, 계약이 정한 측정 명령을 **격리 밖에서** 조건마다 한 번씩 돌려 그 출력과 종료 코드를 얼린 입력에 넣는다. 판정 · 재심 · 조사 뒤 재판정 차례가 모두 같은 기록을 본다(사전 측정은 감독 한 번에 한 번).
2. 측정 명령은 감독 설정 `codex_audit.premeasure` 로 받는다 — 조건 번호 자리 `{id}` 가 든 명령 틀(예: `bash .harness/.meta/codex-supervisor/measure/measure.sh {id}`). 칸이 없으면 사전 측정을 하지 않는다(지금과 같다).
3. 사전 측정은 사용자 작업 폴더가 아니라 구현 커밋 사본(판정 사본과 같은 방식, 원래 저장소 `.git` 불변)에서 돈다. 조건 하나의 상한은 `CODEX_AUDIT_LIMIT` 를 따르고, 넘으면 그 조건 기록에 시간 초과를 적고 다음 조건으로 간다. 자식 프로세스까지 끈다.
4. 기록은 스크립트가 쓴다. 조건마다 명령 · 종료 코드 · 출력(키 글자 가림)을 남기고, 요약 한 장(조건 · 종료 코드 · 마지막 줄)을 남긴다. 목록 파일(MANIFEST)에 기록 위치가 들어간다.
5. 판정 지시문은 「격리 안에서 돌릴 수 없는 측정(프로세스 관측 · 겹친 격리 · 실제 서비스 호출 등)은 사전 측정 기록을 증거로 쓸 수 있다. 기록은 감독 스크립트가 판정 전에 격리 밖에서 남긴 것이다」 를 담는다. 격리 안에서 돌릴 수 있는 측정은 여전히 직접 돌린다. 지시문 크기 · 역할 말 금지 규칙은 그대로다.
6. 사전 측정 명령 실패(없는 명령 · 0 이 아닌 종료)는 감독을 BLOCKED 로 만들지 않는다 — 기록만 남기고 판정은 Codex 가 한다.
7. 이 레포 `.harness/project.yaml` 의 `codex_audit` 에 이 계약의 측정 묶음 명령을 `premeasure` 로 넣는다. 새 프로젝트 틀 `harness/templates/project.yaml` 에는 빈 칸(설명 주석 포함)을 넣는다. README · qa-evaluator · sprint-contract 문서에 한 줄씩 반영한다.

8. `impl` 의 얼린 입력에 계약 개정 파일(`sprint-amendments-<slug>.md`)이 있으면 함께 넣고, 판정 지시문이 그 파일을 읽을 것으로 가리킨다. 지금은 계약 본문만 넣어 감독관이 개정을 보지 못한다.

사용자 동의 기록: 이 세션 기록(`~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/fb4aefa8-0ee1-4711-9b22-7baf9c6b989f.jsonl`)의 사용자 메시지 「1」 · 2026-10-06T04:23:30.477Z · session=fb4aefa8-0ee1-4711-9b22-7baf9c6b989f · cwd=/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/codex-supervisor. 앞 결정 「파일 저장 안으로」 2026-10-06T00:08:58.276Z, 봉인 승인 「ㄱㄱ」 2026-10-06T03:57:12.484Z 도 같은 기록에 있다.

주의: 이 계약 자신의 측정 묶음은 실제 Codex 를 부르는 조건(스크립트-11)을 포함한다. 사전 측정이 그 조건을 돌리면 감독 한 번마다 실제 호출 3 번이 더 든다(사용자가 비용을 알고 고른 안이다).
