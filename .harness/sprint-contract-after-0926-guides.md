---
feature: "harness 가이드 · 스킬 · 에이전트 남은 일 (GD-1 ~ GD-12 · UD-5)"
slug: after-0926-guides
created: "2026-09-26 19:58"
complexity: "복잡"
conditions: 37
status: active
owner_session: bda55d45-296c-491f-89ba-b52042d58e72
conditions_digest: sha256:1774b0d356321753
measurement_digest: sha256:1292a5ca807199ca
locked_at: "2026-09-26 20:13"
---

## 배경

2026-09-24 카이젠 뒤 남은 일 목록의 「## gd」 절 열두 항목(GD-1 ~ GD-12)과 사용자 결정 UD-5(결정 전파 상태 값에 「대체됨」)를 한 계약으로 묶는다.
입력은 읽기만 한다 — 남은 일 목록 `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0926b/.harness/.meta/after-kaizen-0926b/leftovers.md`,
사용자 결정 `.../after-kaizen-0926b/decisions.md`, 바깥 문서 대조 `.../after-kaizen-0926b/ex/EX-1.md` ~ `EX-4.md`, 넘김 기록 `.../after-kaizen-0926/c3a-notes.md`.

- 사용자 합의(Step 5): 위임으로 받은 것으로 적는다 — 세션 `bda55d45-296c-491f-89ba-b52042d58e72` 의 사용자 말 2026-09-26T10:09:00.557Z
  「123다실행해 그러면끝나?다음카이젠에왜넘기는데?」 와 결정 답 2026-09-26T10:30:16.222Z(UD-5 「대체됨 같은 값을 둔다」 포함, `decisions.md:23`).
  그 앞의 위임 2026-09-24T04:04:16.964Z 「나한테 물어보지 말고 자동으로 끝까지」. 조건을 느슨하게 하는 개정은 이 위임으로 동의 처리하지 않는다 — 그런 개정은 부모가 사용자에게 따로 묻는다.
- 작업 폴더 W = `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak2-gd`, 가지 `chore/ak2-gd`, 시작점 `6378948`(origin/main, #119).
- 커밋 규칙: `git add <경로>` 뒤 `git commit -o <경로>` · 한 커밋에 킷(맨 위 폴더) 하나 · `.harness/` 파일은 킷과 다른 커밋 · `git add -A` · `git stash` · push · 가지 바꾸기 금지.
- 구현 전에 `tone-kit:tone-guide` 1 단계(규칙 불러오기)를, 완료 선언 전에 5 단계(전수 대조)를 한다 — 대조 결과는 notes 에 남긴다(AR-02).
- 같은 파일을 다른 묶음(harness 스크립트 · 계약 형식 · PRD 없음 규칙 · 문서 사이트)이 고칠 수 있다. 바꿀 줄은 최소로 하고 아래 조건에 없는 절은 건드리지 않는다.
- 사용자가 할 일: 없음.

복잡도 4 축 — 넷 다 「예」 이고 공개 약속 변경과 소비자가 함께 있어 「복잡」 이다. Step 2.5 짝 조건: SK-04 ↔ SC-01(평가 가이드 원문 ↔ reviewer 사본 일곱) ·
SK-11 ↔ SK-12(`/sprint` 판정 표 ↔ 글자 그대로 옮긴 사본 셋) · SK-13 ↔ SK-14(skill 가이드 새 절 ↔ 화면 규약 셋) · SK-20 ↔ SK-21(결정 전파 규칙 ↔ 쓰는 쪽 넷).

| 축 | 물음 | 값 |
| -- | ---- | -- |
| 레이어 수 | 몇 개 계층을 관통하는가 | 셋 — 설계 가이드 · harness 스킬 · 에이전트 문서, 킷 참조 문서 안 검사 코드와 킷 시험 스크립트, 문서 사이트 HTML 두 쪽 |
| 공개 API·계약 변경 | 외부에 노출된 약속이 바뀌는가 | 예 — 결정 전파 목록의 `status` 값과 검사 종료 코드, 평가 가이드 미검증 조항 번호(킷 reviewer 일곱이 글자 그대로 옮긴다), `/sprint` 판정 표 첫 줄 |
| 소비면 존재 | 반대편이 있는가 | 예 — reviewer 일곱 · 감사 스킬 넷의 조항 번호 인용, design-test · design-audit · design-reviewer, `docs/infra/platform/cicd.md` · rust-preflight · `docs/infra-kit/cicd.html` |
| 회귀 위험 | 기존 동작이 깨질 수 있는가 | 예 — `decision-gate-test.sh` 기존 16 경우, reviewer 사본 검사(CI), 카이젠 회귀 패턴 14 개 |

설정 글자 대조(Step 1.2):

| config key | project.yaml 에서 읽은 값 | 계약에 쓴 값 |
| ---------- | ------------------------- | ------------ |
| `commands.analyze` | `bash -n scripts/release.sh` | DG-01 N/A — 재는 파일이 바뀐 파일에 없다 |
| `commands.test` | `bash scripts/release.sh 2>&1 \|\| true` | DG-03 N/A — 같은 이유 |
| `diagnostics.ide_exclude` | `[]` | DG-02 의 `([] 제외)` |
| `contract_categories[].id` / `prefix` | Skill/SK · Script/SC · Error/ER · Architecture/AR | 같은 넷 |
| `anti_patterns[].id` / `message` | AP-01 버전 하드코딩 · AP-02 force push · AP-03 bare code fence · AP-04 frontmatter name 누락 | AP-03 · AP-04 (바뀌는 파일이 SKILL.md · 에이전트 · 코드 블록 있는 MD 라 걸릴 수 있다). AP-01 은 `plugin.json` 버전을 안 건드려서, AP-02 는 이 계약이 push 하지 않아서 뺐다 |

## GAP 분석 (Pre-Edit Audit)

시작점 `6378948` 판을 직접 열어 확인했다. 줄 번호는 이 판 기준이다.

| 대상 파일 | 실제 Read 증거 (`파일:라인`) | 발견한 기존 갭·위반 | 계약 조건화 여부 |
| --------- | ---------------------------- | ------------------- | ---------------- |
| `harness/docs/guides/plugin-validation-guide.md` | `:415-421` FAIL 예시 2 · `:400` Hooks reference 문장 · `:550` `Total: 2 plugins, 1 OK, 1 ERROR` · `:590` 수동 수정 V8 행 · `:695` 변경 이력 끝 행(1.4.1) | 예시 2 머리는 design-kit 인데 둘째 명령 `hooks/log-prompt.sh` 는 reflect-kit 파일이고, 실패 줄이 하나(실제 검사는 명령마다 한 줄 · 뒤에 명령 글자). V8 행에 따옴표 고치는 법 없음. 변경 이력에 V8 따옴표 줄 없음. 킷 둘만 돌리는 명령은 없어 `Total: 2 plugins` 는 만들 수 없는 조합 | SK-01 · SK-02 · SK-03. `:400` 은 EX-1 판정 「맞음」 이라 고치지 않음 |
| `harness/docs/guides/qa-evaluation-guide.md` | `:1236` 머리 「아래 5 조항」 · `:1241-1245` 「현재 drift (2026-07-27 실측)」 · `:1278` · `:1285` 번호 `3.` 둘 · `:143` 「12 개 이상의 편향」 · `:1944` 「12 개 편향 분류」 · `:1167-1210` 사본 다섯 가지 절 | 조항 번호 3 이 둘이라 킷 쪽 「조항 3」 이 어느 것인지 갈린다. drift 문단은 2026-07-27 판 상태(지금은 CI 사본 검사가 있다). `:143` 은 두 논문이 모두 12 개 넘게 분류한다고 읽힌다(EX-4: Survey 는 두 상위 분류, CALM 은 정확히 12). 문장 삭제 사본 검토 절차가 없다 | SK-04 · SC-01 · SK-08 · SK-09. `:1944` 는 EX-4 판정 「정확히 12」 와 같아 처리됨 |
| reviewer 일곱 | `api-kit/agents/api-reviewer.md:100` · `backend-kit/agents/backend-reviewer.md:130` · `design-kit/agents/design-reviewer.md:70` · `infra-kit/agents/infra-reviewer.md:116` · `planning-kit/agents/planning-reviewer.md:70` · `react-kit/agents/react-reviewer.md:211` · `rust-kit/agents/rust-reviewer.md:91` | 원문 둘째 `3.` 줄을 글자 그대로 들고 있다. 원문만 고치면 `scripts/check-reviewer-protocol-copies.py` 가 일곱 다 MISMATCH(봉인 전 실측) | SC-01 |
| 조항 번호를 인용하는 킷 글 | `design-kit/agents/design-reviewer.md:222` · `infra-kit/agents/infra-reviewer.md:163` · `flutter-toolkit/references/visual-evidence-protocol.md:136` · `onboarding-kit/skills/setup-guide/SKILL.md:40` · `:224` · `backend-kit/skills/backend-audit/SKILL.md:111` · `rust-kit/skills/rust-audit/SKILL.md:123` · `infra-kit/skills/infra-audit/SKILL.md:94` · `:110` · `react-kit/references/render-evidence-protocol.md:82` · `:205` · `planning-kit/agents/planning-reviewer.md:97` · `:99` · `:176` · `planning-kit/skills/plan-audit/SKILL.md:136` · `react-kit/agents/react-reviewer.md:383` · `backend-kit/agents/backend-reviewer.md:160` | 평가 가이드를 가리키는 열네 곳 가운데 「조항 3」 넷이 원문의 두 3 가운데 어느 것인지 가릴 수 없다(`m SK-04` `refs_bad=4/14`). flutter · onboarding 세 곳은 skill 가이드 §3.7 조항을 가리켜 이 갈림과 무관하다 | SK-04 (합치면 고칠 필요가 없다 — 범위 경계 결정 1) |
| `harness/docs/guides/agent-design-guide.md` | `:80` `model` 행 「`inherit` (기본값)」 · `:91` `omitClaudeMd` · `:93` `experimental` 「뜻 미확인」 · `:465` 오류 문구 둘 「어느 문구가 어느 상한 것인지 … 확인하지 못했다」 · `:55-63` 배치 우선순위 | EX-2: 생략 시 호출 인자 → frontmatter → `CLAUDE_CODE_SUBAGENT_MODEL` → 메인 대화 모델 순. `omitClaudeMd` 는 사용자 · 프로젝트 · 로컬 `CLAUDE.md` 제외, `experimental` 은 `cacheTtl` 을 담는 맵. `Concurrent subagent limit reached` 는 동시 실행 20 상한 오류, 중첩 상한 오류 문구는 원문에 없음. 배치 우선순위는 원문과 같다 | SK-05 · SK-07. 배치 우선순위는 처리됨 |
| `harness/skills/create-agent/SKILL.md` | `:25` 「`model` 을 생략하면 `inherit` 이며」 | 위와 같은 옛 설명 | SK-05 |
| `harness/skills/create-skill/SKILL.md` | `:27` 「공식 필수는 `name` 과 `description` 2 종 … 다른 플랫폼에서는 무시된다」 | EX-3: 표준은 둘 필수, Claude Code 는 모든 필드 선택. 모든 플랫폼이 무시한다는 보장 없음, claude.ai 업로드 등은 오류 | SK-06 |
| `harness/docs/guides/skill-design-guide.md` | `:431` 「두 개의 필수 필드를 가지며」 · `:843-844` 크로스 플랫폼 「다른 플랫폼에서 무시됨」 · `:235-377` §3.7 · `:962-997` §8.8 · `:998-1058` §9 | 위 EX-3 와 같은 옛 설명. §3.7 에 사본 네 가지(①~④)의 생성 측 짝과 「흔한 실수를 넣은 사본」 이 없다. 세 화면 규약 공통 숫자의 원문 절이 없다. §9 에 같은 작업 폴더 `checkout -b` 경고가 없다 | SK-06 · SK-15 · SK-13 · SK-10 |
| `harness/skills/sprint-contract/SKILL.md` | `:757` Step 6.7 (a) `git checkout -b` · `:341-360` Step 1 복잡도 표 · `:493-509` Step 2.5 | 같은 작업 폴더에서 가지를 바꾸면 남의 미커밋이 따라온다는 경고가 6.7 에 없다(`/sprint` `:42-45` 에는 있다). 판정값을 바꾸는 계약이 리포트 틀(`templates/`)까지 찾으라는 말이 없다 | SK-10 · SK-17 |
| `harness/skills/sprint/SKILL.md` | `:116-120` Step 3 판정 표 · `:127-133` Step 4 | 첫 줄 「내가 쓴 목록 밖이면 남의 미커밋이다」 가 근거(`evidence/phase9.md` §4 권장 2)보다 느슨하다. CI 에서만 보이는 두 경우(환경 · 비결정성, 미확정)가 표 밖에도 없다. QA 를 다시 부르기 전 앞 회차 리포트 처리 말이 없다 | SK-11 · SK-18 |
| 판정 표 사본 셋 | `docs/infra/platform/cicd.md:76` · `rust-kit/skills/rust-preflight/SKILL.md:112` · `docs/infra-kit/cicd.html:1073` | 첫 줄을 글자 그대로 옮겼다. rust-preflight `:117` 이 표 첫 줄 판정 칸을 「」 로 인용한다 | SK-12 |
| `harness/agents/qa-evaluator.md` | `:992-993` Iteration 셈 · `:985-986` 리포트 경로 | 리포트는 매 회차 덮어쓰고 Iteration 은 기존 리포트를 센다 — 앞 회차 리포트를 지우면 셈이 1 로 돌아간다. 커밋 안 된 앞 회차 리포트를 이번 판으로 오인한 사례(c4b notes) | SK-18 |
| `harness/skills/contract-kaizen/SKILL.md` · `evaluator-kaizen/SKILL.md` | `:118` · `:115` 「Regression Smoke Test (`harness/evals/kaizen/…/` 활용)」 | 실행기 `scripts/run-kaizen-assertions.py`(CI `:52`) 를 부르지 않는다 | SK-16 |
| `harness/skills/harness-kaizen/SKILL.md` | `:194` 「변경마다 커밋: `kaizen: {변경 설명}`」 · `:233` 추적 규칙 표 | 실제 관행과 다르다 — `Kaizen-Phase:` 서명이 붙은 2026-09-24 Phase 1 ~ 4 커밋 23 개 가운데 `kaizen:` 머리 0 개(`contract` 4 · `chore(harness)` 11 · `docs(harness)` 4 · `fix(harness)` 2 · `fix(scripts)` 2). `kaizen:` 머리는 전체 15 개이고 마지막이 2026-03-30 | SK-19 |
| 세 화면 규약 | `design-kit/references/visual-change-protocol.md:12-15` · `react-kit/references/render-evidence-protocol.md:24-26` · `flutter-toolkit/references/visual-evidence-protocol.md:52` · `:91` | design · react 머리가 「그 절은 아직 없다」. flutter 규약은 두 숫자를 쓰지만 짝 문단이 없다 | SK-13 · SK-14 |
| 결정 전파 규칙 | `design-kit/references/visual-change-protocol.md:372` · `:389-390` · `:443-444` · `design-kit/evals/decision-gate-test.sh:30` · `:43-44` · `design-kit/skills/design-test/SKILL.md:276` · `design-kit/skills/design-audit/SKILL.md:49` · `design-kit/agents/design-reviewer.md:116` · `docs/design-kit/visual-change-protocol.html:848` · `:914-915` · `:958` | `status` 는 `approved` 하나. 바뀐 결정을 목록에 남길 자리가 없어 옛 결정을 지우거나 형식 오류를 받는다. 쓰는 쪽 셋은 「`decision_id` 마다」 순회만 적는다 | SK-20 · SK-21 · SC-02 · SC-03 · ER-01 |
| 결정 전파 규칙이 적힌 다른 자리 | `leftovers.md:311` · `c3a-notes.md:21` · `:37` · `.harness/sprint-contract-after-0924-kits-a.md:88` · `:140` | 남은 일 목록 · 넘김 기록 · 봉인된 옛 계약이다 — 읽기만 하는 입력이거나 고치지 않는 봉인 기록 | 조건 없음 (범위 경계) |

## Skill

- [ ] SK-01: 검증 가이드 V8 의 FAIL 예시 2 가 실제로 나오는 출력이다 — Given 예시 2 코드 블록(`**FAIL 예시 2**` 아래 첫 코드 블록), When 그 블록의 `"command"` 줄들을 머리 줄(`# <킷>/hooks/hooks.json`)이 가리키는 킷의 `hooks/hooks.json` 에 넣고 `scripts/validate-plugin.py <킷> --check=hook-exec` 를 돌리면, Then 머리 줄의 킷이 하나이고, 명령이 가리키는 스크립트 경로가 모두 그 킷 안에 있으며, 명령이 둘 이상이고, 예시가 보여 주는 출력 줄(`FAIL ` · `V8 ` 로 시작하는 줄, 앞의 `# →` 는 떼고 빈칸은 하나로 본다)이 모두 실제 출력에 있고, 예시의 `FAIL` 줄 수가 실제 `FAIL` 줄 수 · 명령 수와 같다 [exact, enumerated]
  측정: `m SK-01` 이 `hdr=<킷 하나> cmds=c path_missing=0 ex_fail=c real_fail=c ex_not_real=0` 이고 c≥2 (시작 판 `hdr=design-kit cmds=2 path_missing=1 ex_fail=1 real_fail=2 ex_not_real=1` — 이 값이 양성 대조다)
  알려진 답: 시작 판 예시는 손으로 세면 명령 둘 · design-kit 에 없는 경로 하나(`hooks/log-prompt.sh`) · 예시 FAIL 줄 하나 · 따옴표 없는 명령 둘이라 실제 FAIL 둘이다. 측정이 낸 값과 같다 (봉인 전 실측, 종료 코드 0)
- [ ] SK-02: 검증 가이드가 V8 따옴표 고치는 법과 그 변경 이력을 적는다 — 수동 수정 표의 V8 행(`| V8 |` 로 시작하는 줄)에 「따옴표」 가 들고, `## 8. 변경 이력` 표에 `V8` 과 「따옴표」 를 함께 담은 행이 1 개 이상이다 [exact, enumerated]
  측정: `m SK-02` 가 `row_quote=a log_quote=b` 이고 a≥1 · b≥1 (시작 판 `row_quote=0 log_quote=0`)
- [ ] SK-03: 검증 가이드 출력 예시의 요약 줄이 명령줄로 만들 수 있는 조합이다 — `### 출력 포맷` 절 코드 블록의 `Total: N plugins, …` 줄이 (a) 킷 하나를 돌린 모양(N=1 · `=== ` 블록 1 개)이거나 (b) 전체를 돌린 모양(N = `.claude-plugin/marketplace.json` 의 플러그인 수, `OK` · `WARNING` · `ERROR` 수의 합이 N)이고 (b) 이면 절의 코드 블록 밖 글에 「전체 실행」 이 든 줄(예시가 전체 실행 출력에서 킷 몇 개만 뽑은 것이라는 설명)이 1 개 이상이다 [exact]
  측정: `m SK-03` 이 `total=N ok=a warn=b err=c kits=K blocks=B note=x` 이고 (N=1 · B=1) 또는 (N=K · a+b+c=N · x≥1) (시작 판 `total=2 ok=1 warn=0 err=1 kits=14 blocks=2 note=0` — 둘 다 아니다)
- [ ] SK-04: 평가 가이드 미검증 조항의 번호가 겹치지 않고 킷 인용이 가리키는 조항과 맞는다 — `## Canonical Unverified-Evidence Protocol` 절의 번호 목록이 1 ~ 5 로 한 번씩 나오고(둘째 `3.` 「임계값 2 는」 문단은 첫째 3 항의 이어지는 문단으로 합친다 — 범위 경계 결정 1), 머리 인용문의 「아래 N 조항」 이 5 이며, 「현재 drift」 문단이 없고 대신 같은 절에 사본 검사 `check-reviewer-protocol-copies.py` 를 가리키는 줄이 1 개 이상이며, 킷 글 열두 파일(측정 도우미 `CLAUSE_REFS`)의 평가 가이드 조항 번호 인용 열네 곳이 모두 번호 하나에 한 번만 나오는 조항을 가리키고 그 조항이 인용 주제의 낱말을 담는다(1 → `[정적]` · 3 → `env_gaps` · 5 → `조용한 PASS 금지`) [exact, enumerated]
  측정: `m SK-04` 가 `nums=1,2,3,4,5 head=5 drift=0 checker=c refs_bad=0/14` 이고 c≥1 (시작 판 `nums=1,2,3,3,4,5 head=5 drift=1 checker=0 refs_bad=4/14`)
  알려진 답: 시작 판 인용 열네 곳(GAP 분석 열두 곳 + design-reviewer `:222` 「조항 5」 · infra-reviewer `:163` 「조항 1」)을 손으로 세면 「조항 3」 넷(backend-audit `:111` · rust-audit `:123` · infra-audit `:94` · render-evidence-protocol `:205`)이 번호 3 이 둘이라 갈리지 않는다 — 측정 `refs_bad=4/14` 와 같다 (봉인 전 실측). flutter `visual-evidence-protocol.md:136` · onboarding `setup-guide/SKILL.md:40` · `:224` 의 「조항 3」 은 skill 가이드 「§3.7 5 조항」 · 「§3.7 조항」 을 가리켜 도우미 정규식이 뺀다 — 파일은 목록에 두어 문구가 바뀌면 걸리게 한다
- [ ] SK-05: 서브에이전트 `model` 생략 동작을 원문대로 적는다 — agent 가이드 frontmatter 표의 `model` 행에 「`inherit` (기본값)」 이 없고 `CLAUDE_CODE_SUBAGENT_MODEL` 이 들며(생략 시 순서: 호출별 `model` 인자 → frontmatter → 이 환경 변수 → 메인 대화 모델, EX-2 §2.1), create-agent Gotcha 에서 「`model` 을 생략하면 `inherit`」 이 없고 `CLAUDE_CODE_SUBAGENT_MODEL` 이 1 줄 이상이다 [exact, enumerated]
  측정: `m SK-05` 가 `guide_inherit_default=0 guide_env=a ca_old=0 ca_env=b` 이고 a≥1 · b≥1 (시작 판 `1 0 1 0`)
- [ ] SK-06: 스킬 frontmatter 필수 필드와 다른 플랫폼 처리를 원문대로 적는다 — (a) create-skill 에 「다른 플랫폼에서는 무시된다」 가 없고 `Agent Skills` 가 1 줄 이상(표준은 `name` · `description` 필수, Claude Code 는 모든 필드 선택 — EX-3 §A · §B) (b) skill 가이드 `### frontmatter 필드 규칙` 절에 「두 개의 필수 필드를 가지며」 가 없고 `agentskills.io/specification` · `code.claude.com/docs/en/skills` 가 각 1 줄 이상 (c) skill 가이드 `### 크로스 플랫폼 호환` 절에 「다른 플랫폼에서 무시됨」 이 없고 「보장」 이 든 줄이 1 개 이상(모든 플랫폼이 무시한다는 보장은 없다 — EX-3 §D) [exact, enumerated]
  측정: `m SK-06` 이 `csk_old=0 csk_std=a sdg_old=0 sdg_spec=b sdg_cc=c xp_old=0 xp_guar=d` 이고 a · b · c · d ≥1 (시작 판 `csk_old=1 csk_std=0 sdg_old=1 sdg_spec=0 sdg_cc=0 xp_old=1 xp_guar=0`)
- [ ] SK-07: agent 가이드 §7 오류 문구와 두 필드 뜻을 원문대로 적는다 — (a) 「어느 문구가 어느 상한 … 확인하지 못했다」 가 없고 `Concurrent subagent limit reached` 가 든 문장(「다.」 로 끊은 문장)에 「동시」 와 「20」 이 함께 있다(EX-2 §2.4) (b) `Subagent spawn limit reached` 가 남는 줄은 모두 「찾지 못」 또는 「원문에 없」 을 담는다 (c) frontmatter 표 `omitClaudeMd` 행에 「뜻 미확인」 이 없고 `CLAUDE.md` 가 들고 (d) `experimental` 행에 「뜻 미확인」 이 없고 `cacheTtl` 이 든다(EX-2 §2.3) [exact, enumerated]
  측정: `m SK-07` 이 `unpaired=0 conc20=a spawn_unmarked=0 omit_unk=0 omit_md=b exp_unk=0 exp_ttl=c` 이고 a · b · c ≥1 (시작 판 `unpaired=1 conc20=0 spawn_unmarked=1 omit_unk=1 omit_md=0 exp_unk=1 exp_ttl=0`)
- [ ] SK-08: 평가 가이드의 편향 수를 원문대로 적는다 — 「12 개 이상」 이 파일에 없고, 두 논문을 함께 인용하는 줄(`2411.15594v6` · `2410.02736v1` 을 함께 담은 줄)이 Survey 의 두 상위 분류 이름 `task-agnostic` · `judgment-specific` 을 담으며(EX-4 §A ①), 출처 목록의 Justice or Prejudice 행 「12 개 편향 분류」 는 그대로다(EX-4 §A ② 「정확히 12」) [exact, enumerated]
  측정: `m SK-08` 이 `over12=0 classes=a row_exact12=1` 이고 a≥1 (시작 판 `over12=1 classes=0 row_exact12=1`)
- [ ] SK-09: 평가 가이드에 문장 삭제 사본 검토 절차가 있다 — 제목(`### `)에 「문장」 과 「사본」 을 함께 담은 절이 정확히 1 개이고, 그 절이 판별하지 못하는 측정에 기댄 PASS 를 `[미검증:INVALID]` 로 센다고 적으며, 근거 실측 날짜 `2026-09-24`(Phase 1 검토가 모의 편집본으로 막는 결함 둘을 찾은 날) 를 담는다. 절차: 문서 조건이 요구하는 문장 하나를 지운 사본에서 그 조건의 측정을 다시 돌려 값이 떨어지는지 본다 [structural]
  측정: `m SK-09` 가 `sec=1 inv=a date=b` 이고 a≥1 · b≥1 (시작 판 `sec=0 inv=0 date=0`)
- [ ] SK-10: 같은 작업 폴더에서 `checkout -b` 로 가지를 바꾸지 말라는 말이 두 곳에 있다 — sprint-contract `### 6.7.` 절에 `git worktree add` 가 든 줄 1 개 이상과 `checkout -b` · 「작업 폴더」 를 함께 담은 줄 1 개 이상, skill 가이드 `## 9.` 절에 `checkout -b` 줄 1 개 이상과 `git worktree add` 줄 1 개 이상 [exact, enumerated]
  측정: `m SK-10` 이 `s67_wt=a s67_warn=b g9_cb=c g9_wt=d` 이고 네 값 ≥1 (시작 판 `0 0 0 0`)
- [ ] SK-11: `/sprint` Step 3 판정 표 첫 줄이 근거만큼 좁고 CI 에서만 보이는 두 경우를 받는다 — Step 3 절(`### Step 3:` ~ `### Step 4:`)에서 옛 판정 「내가 쓴 목록 밖이면 남의 미커밋이다」 가 파일에 없고, 표 첫 줄(`| 실패 | 통과 | — |`)의 판정 칸이 「시작」(작업을 시작할 때 떠 둔 `git status` 목록)과 「귀속 불명」 을 담으며(`evidence/phase9.md` §4 권장 2 — 시작 목록에도 있고 내 경로 밖일 때만 남의 미커밋 후보, 확인 못 하면 귀속 불명), 같은 절에 「환경 · 비결정성」 · 「미확정」 이 각 1 줄 이상이다 [exact, enumerated]
  측정: `m SK-11` 이 `old=0 row_start=a row_unknown=b ci_env=c ci_undec=d` 이고 네 값 ≥1 (시작 판 `old=1 row_start=0 row_unknown=0 ci_env=0 ci_undec=0`)
- [ ] SK-12: 판정 표 사본 셋이 새 첫 줄을 글자 그대로 따른다 — `docs/infra/platform/cicd.md` · `rust-kit/skills/rust-preflight/SKILL.md` 의 표 첫 줄 판정 칸이 `/sprint` 의 것과 글자까지 같고, `docs/infra-kit/cicd.html` 의 `<td class="verdict">` 가운데 하나가 태그를 벗기면(`<code>` 는 백틱으로) 같은 글이며, 세 파일에 옛 판정 문장이 없고, rust-preflight 에서 「표 첫 줄 판정 칸」 을 담은 줄의 「」 인용이 모두 새 판정 칸 안에 있다 [exact, enumerated]
  측정: `m SK-12` 가 `old=0,0,0 md_same=1,1 html_same=1 rp_quote_ok=1` (시작 판 `old=1,1,1 md_same=1,1 html_same=1 rp_quote_ok=1` — 셋 다 옛 줄이라 같다. 사본을 안 고치면 SK-11 을 고친 뒤 `md_same=0,0` · `html_same=0` 이 된다)
- [ ] SK-13: 세 화면 규약이 같이 쓰는 숫자의 원문 절이 skill 가이드에 있다 — `## 8.9. ` 로 시작하는 제목이 정확히 1 개이고, 그 절이 「2 개 이상」(같은 역할 기존 화면으로 만드는 관례 표)과 「3 회」(스스로 고치기 상한)를 담고, 세 규약 파일 이름 `visual-change-protocol.md` · `visual-evidence-protocol.md` · `render-evidence-protocol.md` 을 각 1 줄 이상 담는다. 숫자를 정하는 바깥 표준이 없고 형제 규약 정합과 운영 비용으로 골랐다는 한계(`phase6-notes.md:115`)를 적는다 [exact, enumerated]
  측정: `m SK-13` 이 `sec=1 two=a three=b names=x,y,z,` 이고 a · b · x · y · z ≥1 (시작 판 `sec=0 two=0 three=0 names=0,0,0,`)
- [ ] SK-14: 세 화면 규약이 새 절을 가리킨다 — `design-kit/references/visual-change-protocol.md` · `flutter-toolkit/references/visual-evidence-protocol.md` · `react-kit/references/render-evidence-protocol.md` 각각에 `skill-design-guide.md` 와 `§8.9` 를 함께 담은 줄이 1 개 이상이고, design · react 두 규약에 「그 절은 아직 없다」 가 없다. 규약 안의 숫자 자체는 남긴다(킷은 따로 설치되어 harness 파일을 못 읽는다) [exact, enumerated]
  측정: `m SK-14` 가 `cite=a,b,c, stale=0,0` 이고 a · b · c ≥1 (시작 판 `cite=0,0,0, stale=1,1`)
- [ ] SK-15: skill 가이드 §3.7 에 검사를 만드는 스킬의 사본 네 가지(①~④)와 흔한 실수 사본이 있다 — `## 3.7.` 절(~ `## 3.8.`)이 평가 가이드 네 이름 「첫 칸만 읽기」 · 「표에만 올린 시험」 · 「한 칸 못 읽으면」 · 「셸마다 다른 대상 수」 를 각 1 줄 이상 담고, `qa-evaluation-guide.md` 와 「산출물이 검사일 때」 를 함께 담은 줄이 1 개 이상이며, 알려진 답 입력은 흔한 실수를 넣은 측정 사본이 다른 값을 내도록 고른다는 줄(「흔한 실수」)이 1 개 이상이다(`phase13-notes.md:104-105` — 반원 · 1/4 호 둘은 방향을 무시해도 같은 길이라 실수를 못 잡았다) [exact, enumerated]
  측정: `m SK-15` 가 `t1=a t2=b t3=c t4=d common=e cite=f` 이고 여섯 값 ≥1 (시작 판 여섯 다 0)
- [ ] SK-16: contract-kaizen · evaluator-kaizen Step 7 이 회귀 패턴 실행기를 부른다 — 두 파일 `### Step 7:` 절(~ `### Step 8:`)에 각각 `scripts/run-kaizen-assertions.py` 줄 1 개 이상과 「종료 코드」 줄 1 개 이상(0 통과 · 1 패턴 사라짐 · 2 못 읽음 을 판정에 쓴다)이 있다 [exact, enumerated]
  측정: `m SK-16` 이 `ck=a,b ek=c,d` 이고 네 값 ≥1 (시작 판 `ck=0,0 ek=0,0`)
- [ ] SK-17: 판정값을 바꾸는 계약은 리포트 틀까지 찾아 범위를 잡는다고 sprint-contract 가 적는다 — `### 1. 요구사항 분석` ~ `### 3. 안티패턴` 사이에 `templates/` 와 「판정값」 을 함께 담은 줄이 1 개 이상이다(c4b notes: design-audit 리포트 틀이 `BLOCKED` 를 못 담아 개정 AM-01) [exact]
  측정: `m SK-17` 이 `scope=a` 이고 a≥1 (시작 판 `scope=0`)
- [ ] SK-18: QA 를 다시 부르기 전 앞 회차 리포트를 커밋해 둔다 — `/sprint` Step 4 절(~ `### Step 4.5`)과 `harness/agents/qa-evaluator.md` 에 각각 「앞 회차」 와 「커밋」 을 함께 담은 줄이 1 개 이상이다. 지우라고 적지 않는다 — 리포트는 회차마다 덮어쓰고 Iteration 은 기존 리포트에서 세므로(`qa-evaluator.md:992`) 지우면 셈이 1 로 돌아간다 [exact, enumerated]
  측정: `m SK-18` 이 `spr=a qae=b` 이고 a · b ≥1 (시작 판 `spr=0 qae=0`)
- [ ] SK-19: harness-kaizen 커밋 머리 규칙이 실제 관행과 맞는다 — 파일에 백틱 안 `kaizen:` 머리가 없고, 추적 규칙 표 커밋 메시지 행과 「변경마다 커밋」 줄에 서명 줄 `Kaizen-Phase:` 가 들며, 그 행의 예시(셋째 칸 첫 백틱 글의 `:` 앞)가 `Kaizen-Phase: kaizen-0924-p01` ~ `p04` 서명이 붙은 main 커밋 제목 머리에 1 번 이상 나온다(GAP 분석의 23 개 실측) [exact, enumerated]
  측정: `m SK-19` 가 `kz=0 row_trailer=a step_trailer=b example=[x] example_in_log=c` 이고 a · b · c ≥1 (시작 판 `kz=2 row_trailer=0 step_trailer=0 example=[kaizen] example_in_log=0`)
- [ ] SK-20: 결정 전파 규칙이 「대체됨」 상태를 받는다 — `design-kit/references/visual-change-protocol.md` `## 6.` 절이 (a) `status` 값으로 `approved` 와 `superseded`(대체됨) 둘을 적고 옛 「`approved` 하나다」 가 없다 (b) `superseded` 결정은 `superseded_by` 에 같은 목록의 `approved` 결정 번호를 적는다 (c) `superseded` 결정은 화면 자리 검사를 건너뛰고 형식 검사(`decision_id` · `source` · `superseded_by`)만 받는다. 근거: 사용자 결정 UD-5(`decisions.md:23`) [exact, enumerated]
  측정: `m SK-20` 이 `sup_status=a sup_by=b old_one=0` 이고 a · b ≥1 (시작 판 `sup_status=0 sup_by=0 old_one=1`)
- [ ] SK-21: 결정 전파를 쓰는 쪽 넷이 `superseded` 를 안다 — design-test `### Step 5-b` 절, design-audit Gotcha 14 줄(`14. **Decision Propagation` 로 시작), design-reviewer 규칙 12 줄(`12. **Decision Propagation` 로 시작)에 각각 `superseded` 가 1 번 이상 들고, 문서 사이트 `docs/design-kit/visual-change-protocol.html` 에 옛 「`approved` 하나다」 가 없고 `superseded_by` 가 1 번 이상 들며 그 페이지의 검사 코드 블록이 원본 §6 코드 블록과 줄마다 같다(HTML 이스케이프 · 태그를 벗기고 줄 끝 공백 무시) [exact, enumerated]
  측정: `m SK-21` 이 `dt=a da=b dr=c h_old=0 h_by=d h_same=1` 이고 a · b · c · d ≥1 (시작 판 `dt=0 da=0 dr=0 h_old=1 h_by=0 h_same=1`. 원본 코드만 고치고 페이지를 안 고치면 `h_same=0`)

## Script

- [ ] SC-01: reviewer 일곱의 미검증 조항 사본이 새 원문과 글자까지 같다 — Given SK-04 를 고친 끝점, When `scripts/check-reviewer-protocol-copies.py` 를 돌리면, Then 종료 코드 0 · 요약 `checked=7 violations=0 infra_errors=0 excluded=1` 이고, 원문과 reviewer 일곱에서 줄 머리가 `3. **임계값 2 는` 인 줄(앞 공백 · `>` 는 뗀다)이 0 이다 [exact, enumerated]
  측정: `m SC-01` 이 `rc=0 [checked=7 violations=0 infra_errors=0 excluded=1] old_second3=0` (시작 판 `old_second3=8`)
  양성 대조: 임시 복제본에서 원문 둘째 `3.` 만 합치고 reviewer 는 그대로 두면 `checked=7 violations=7` (봉인 전 실측)
- [ ] SC-02: 결정 전파 검사가 대체된 결정을 건너뛴다 — Given §6 에서 뗀 검사 코드와 손으로 만든 입력 셋(측정 도우미 `dg_inputs`): `ok`(`approved` 결정 하나) · `sup`(`DEC-…-001` 은 `superseded` · `superseded_by: DEC-…-002` 이고 골든만 있는 화면 자리 하나에 `excluded_surfaces` 키가 없다, `DEC-…-002` 는 온전한 `approved`) · `draft`(`status: draft`), When 각각 돌리면, Then 종료 코드/오류 추적 줄 수가 `ok=0/0 sup=0/0 draft=2/0` 이고 `sup` 출력에 `superseded=1` 이 든다. 기대값은 SK-20 규칙에서 손으로 정했다 [exact, enumerated]
  측정: `m SC-02` 가 `ok=0/0 sup=0/0 sup_count=1 draft=2/0` (시작 판 `ok=0/0 sup=2/0 sup_count=0 draft=2/0`)
- [ ] SC-03: 기존 시험 `decision-gate-test.sh` 가 대체된 결정 경우를 잰다 — 자기 입력 열에 이름이 `sup` 로 시작하는 경우를 셋 이상(통과 하나 · 형식 오류 둘 이상) 더해 모두 일치하고, 시작점 문서를 `DECISION_GATE_DOC` 로 준 실행에서는 그 경우 가운데 1 개 이상이 어긋난다 [exact]
  측정: `m SC-03` 이 `rc=0 [결과: N 경우 중 불일치 0] sup_cases=k base_doc_bad=j` 이고 N≥19 · k≥3 · j≥1 (시작 판 `rc=0 [결과: 16 경우 중 불일치 0] sup_cases=0 base_doc_bad=0`)
  음성 대조: `base_doc_bad` 가 곧 음성 대조다 — 시작 판 검사 코드는 `sup` 입력에 종료 코드 2 를 낸다(SC-02 시작 판 `sup=2/0`, 봉인 전 실측)

## Error

- [ ] ER-01: `superseded` 결정의 형식이 틀리면 종료 코드 2 다 — Given 입력 여섯(측정 도우미 `dg_inputs`): `supnoby`(`superseded_by` 없음) · `supdangling`(목록에 없는 번호) · `supself`(자기 번호) · `supchain`(가리킨 결정도 `superseded`) · `supbytype`(`superseded_by` 가 목록) · `supbadid`(`decision_id` 형식 오류), When 각각 돌리면, Then 여섯 다 종료 코드 2 · 오류 추적 줄 0 이다 [exact, enumerated]
  측정: `m ER-01` 이 `supnoby=2/0 supdangling=2/0 supself=2/0 supchain=2/0 supbytype=2/0 supbadid=2/0` (시작 판도 여섯 다 `2/0` 이다 — `superseded` 자체를 거부하기 때문이다)
  음성 대조: `m ER-01N` — 시작 판 검사 코드에 `superseded` 를 받아 건너뛰는 두 줄만 넣은 사본에서 `sup=0/0 supnoby=0/0 supdangling=0/0 supself=0/0 supchain=0/0 supbytype=0/0` (봉인 전 실측). `superseded_by` 확인 없이 받기만 하면 이 조건이 FAIL 한다

## Architecture

- [ ] AR-01: 바뀐 파일이 기대 집합 안이고 한 커밋에 맨 위 폴더 하나다 — Given 구현 · notes 커밋이 모두 가지 `chore/ak2-gd` 에 들어간 뒤, 시작점 `BASE=$(git -C W merge-base origin/main chore/ak2-gd)` 부터 끝점 `TIP=$(git -C W rev-parse --verify chore/ak2-gd)` 까지(`HEAD` 를 쓰지 않는다. 해석이 안 되면 `UNRESOLVED` 로 멈춘다) `git diff --name-only` 로 모은 경로가 측정 도우미 `ALLOWED` 의 서른세 경로 안에만 있고(부분 집합, 생성물 제외 없음), 맨 위 폴더 열(`harness` · `design-kit` · `flutter-toolkit` · `react-kit` · `rust-kit` · `api-kit` · `backend-kit` · `infra-kit` · `planning-kit` · `docs`)이 각 1 경로 이상이며, 커밋마다 맨 위 폴더가 하나뿐이다 [exact, collective]
  측정: `m AR-01` 이 `extra=0` · 열 값 모두 ≥1 · `multi_top=0` (시작 판: 구간이 비어 `changed=0`)
  양성 대조: 임시 복제본에서 범위 밖 파일 하나와 두 폴더를 한 커밋에 넣으면 `extra=1` · `multi_top=1` 이고 남는 경로를 출력한다 (봉인 전 실측)
- [ ] AR-02: 항목별 처리와 넘길 것을 notes 에 남긴다 — Given 끝점 `TIP`, notes 파일 `.harness/.meta/after-kaizen-0926b/gd-notes.md` 가 커밋돼 있고 스물한 토큰(`GD-1` ~ `GD-12` · `UD-5` · `tone-guide` · `처리됨` · `docs/harness/plugin-validation.html` · `docs/harness/qa-evaluation-guide.html` · `docs/harness/skill-design-guide.html` · `docs/harness/agent-design-guide.html` · `KD-3` · `CS-3`)이 각 1 줄 이상이며(`GD-1` 은 `GD-10` 과 가른다), 넘길 것이 무엇인지 적은 줄 — `KD-3` 과 `§8.9` 를 함께 담은 줄, `CS-3` 과 `①~④` 를 함께 담은 줄 — 이 각 1 개 이상이다. 담을 내용: 항목마다 「계약에 넣음 / 처리됨(근거) / 바깥 근거 없음」, tone-guide 5 단계 대조 결과, 원본이 바뀌어 다시 만들 문서 페이지(`python3 scripts/detect-docs-drift.py --since 6378948` 출력과 이 계약이 직접 고친 두 쪽), 뒤따를 일(KD-3 — design-kit 다섯 자리의 숫자 재정의, CS-3 — 평가 가이드 「한계」 문단의 ①~④ 짝 넘김 문장) [exact, enumerated]
  측정: `m AR-02` 가 `committed=1` 과 1 이상 스물하나, 끝의 `kd3_what=a cs3_what=b` 가 a · b ≥1 (시작 판 `committed=0` 과 0 스물하나 `kd3_what=0 cs3_what=0`)
  양성 대조: 임시 복제본에 스물한 토큰을 담은 notes 를 커밋하면 `committed=1` 과 1 스물하나 · 토큰만 있고 짝 낱말이 없으면 `kd3_what=0 cs3_what=0` (봉인 전 실측)
- [ ] AR-03: 더한 글에 쉬운 말 목록 낱말을 새로 넣지 않는다 — `.harness/` 밖에서 `BASE..TIP` 로 더한 줄에 `~/.claude/rules/plain-korean.md` 표의 검사 `on` 낱말(` / ` 로 나눈 각 낱말, 영문 낱말은 앞뒤가 영문자가 아닐 때만) 등장 수가 지운 줄의 같은 낱말 수보다 많은 낱말이 0 개다 — 기존 줄을 고칠 때 원래 있던 낱말은 세지 않는다 [exact, collective]
  측정: `m AR-03` 이 `new_hits=0` (시작 판 `words=69 added_lines=0 new_hits=0`)
  양성 대조: 임시 복제본에 「게이트 한 줄」 을 더하고, 「표면」 이 이미 든 줄에 글을 덧붙이면 `new_hits=1 ['게이트']` — 덧붙인 줄의 「표면」 은 세지 않는다 (봉인 전 실측)

## Anti-patterns

- [ ] AP-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수 (```text, ```bash, ```yaml 등). 판정 권위는 validate-plugin V6 상태기계다 — 여는/닫는 fence 가 동형이라 줄 단위 정규식으로는 판정 불가
  측정: 끝점을 풀어 둔 판 `E` 에서 `python3 "$E/scripts/validate-plugin.py" --check=code-fence` 종료 코드 0 (시작 판 0)
  양성 대조: 임시 복제본의 `harness/skills/sprint/SKILL.md` 끝에 언어 없는 fence 를 붙이면 `V6 code-fence 1 bare — FAIL` · 종료 코드 2 (봉인 전 실측)
- [ ] AP-04: SKILL.md / agents/*.md frontmatter 에서 name 필드 누락 — validate-plugin V1 FAIL
  측정: `python3 "$E/scripts/validate-plugin.py" --check=frontmatter` 종료 코드 0 (시작 판 0)
  양성 대조: 임시 복제본의 create-agent SKILL.md 에서 `name:` 줄을 지우면 `누락 필드 ['name']` · 종료 코드 2 (봉인 전 실측)

## Reusability

- [ ] RE-01: N/A (산출물이 문서 문장 · 문서 안 검사 코드 몇 줄 · 기존 시험의 입력 열뿐이라 새 컴포넌트 · 함수 모듈 파일이 없다. 측정: `git -C W diff --diff-filter=A --name-only BASE TIP -- . ':(exclude).harness'` 가 0 줄)
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다 — 새 시험 · 새 검사 스크립트를 만들지 않고 기존 `decision-gate-test.sh`(검사 코드를 매번 문서에서 뗀다) · `check-reviewer-protocol-copies.py` · `run-kaizen-assertions.py` 를 그대로 쓴다
  측정: RE-01 의 명령이 0 줄이고 `grep -c 'Decision Propagation Coverage Gate' "$E/design-kit/evals/decision-gate-test.sh"` 가 1 이상

## Diagnostics

- [ ] DG-01: N/A (commands.analyze `bash -n scripts/release.sh` 가 재는 `scripts/release.sh` 는 이번 바뀐 파일에 없다. 측정: `git -C W diff --name-only BASE TIP | grep -cx 'scripts/release.sh'` 가 0)
- [ ] DG-02: IDE diagnostics 워닝/인포 0개 ([] 제외) — IDE(편집기) 진단을 명령줄로 같게 잰다: 바뀐 `.md`(`.harness/` 제외)의 더해진 줄에 걸린 markdownlint-cli2 0.23.2(MD013 끔, 편집기 확장과 같은 설정) 경고 0 · `decision-gate-test.sh` 의 더해진 줄에 걸린 shellcheck 경고 0
  측정: `m DG-02` 가 `md_new=0 sh_new=0` (도구가 없으면 도우미 `mdl_ready` 가 임시 폴더에 설치한다. 시작 판 `md_new=0 sh_new=0`)
  양성 대조: 임시 복제본에 `#bad heading` 줄 · 새 `.md` 한 개 · `echo $UNQUOTED` 줄을 넣으면 `md_new=2 sh_new=1` (봉인 전 실측 — 비교 전 정렬은 `LC_ALL=C sort`)
- [ ] DG-03: N/A (commands.test `bash scripts/release.sh 2>&1 || true` 가 재는 `scripts/release.sh` 는 이번 바뀐 파일에 없다. 측정: DG-01 과 같은 명령이 0)
- [ ] DG-04: N/A (구동할 앱 · 서버가 없다 — 바뀐 파일이 가이드 · 스킬 · 에이전트 문서, 참조 문서 안 검사 코드, 시험 스크립트, 문서 사이트 HTML 두 쪽뿐. 대신 DG-05 가 CI 단계를 전부 돌린다)
- [ ] DG-05: CI(자동 검사) 단계를 로컬에서 전부 돌려 통과한다 — Given 작업 폴더 W 가 끝점과 같다(`git -C W rev-parse HEAD` 가 `TIP` 이고 `git -C W status --porcelain --untracked-files=no` 가 빈 출력), When `TMPDIR=<임시 폴더> bash /Users/jackson/Hub/10_Dev/claude-plugins/.harness/handoff/2026-09-26-tools/ci-local.sh /Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak2-gd` 를 돌리면, Then 요약(`$TMPDIR/ci-local/summary.txt`)에 `rc=0` 줄이 25 개이고 `rc=0` 이 아닌 줄은 `feedback-agg-test SKIP (yq 없음)` 하나뿐이다
  측정: `grep -c 'rc=0' "$TMPDIR/ci-local/summary.txt"` 가 25 · `grep -v 'rc=0' "$TMPDIR/ci-local/summary.txt"` 가 그 한 줄 (시작 판 봉인 전 실측: 25 · SKIP 한 줄)
  음성 대조: 이 묶음이 기대는 `decision-gate-test` · `reviewer-copies` · `kaizen-assertions` 단계는 SC-03 의 옛 문서 실행과 SC-01 양성 대조가 보여 주듯 한쪽만 고치면 실패한다

## 범위 경계

항목별 처리 — 입력은 남은 일 목록 「## gd」 절 열두 줄과 사용자 결정 UD-5 다.

| ID | 항목 | 처리 | 조건 · 근거 |
| --- | --- | --- | --- |
| GD-1 | 검증 가이드 V8 예시 · 수동 수정 표 · 변경 이력 · `Total: 2 plugins` | 계약에 넣음 | SK-01 · SK-02 · SK-03. `:400` 「Hooks reference 도 이 변수를 큰따옴표로 감싸라고 한다」 는 처리됨 — EX-1 판정 「맞음」(`ex/EX-1.md` §2, https://code.claude.com/docs/en/hooks#reference-scripts-by-path). 페이지 `docs/harness/plugin-validation.html` 재생성은 DC-4(문서 사이트 묶음) |
| GD-2 | 평가 가이드 조항 번호 겹침 · 머리 「5 조항」 · 「현재 drift」 · 킷 「정본 조항 3」 | 계약에 넣음 | SK-04 · SC-01. 킷 인용 열네 곳은 결정 1 로 고칠 필요가 없어지고 SK-04 가 맞는지 잰다. 남은 일 목록의 「정본 절이 두 번(`:1236` · `:1308`)」 은 부정확하다 — `:1308` 은 다른 정본 절(사용자 보고 실패)이고 실제 결함은 한 절 안의 번호 `3.` 중복이다 |
| GD-3 | `model` 생략 · 스킬 필수 필드 · 다른 플랫폼 무시 | 계약에 넣음 | SK-05 · SK-06 (`ex/EX-2.md` §2.1 https://code.claude.com/docs/en/sub-agents · `ex/EX-3.md` §A · §B · §D https://code.claude.com/docs/en/skills · https://agentskills.io/specification). 서브에이전트 frontmatter 의 필수 필드(agent 가이드 `:70` 「필수는 `name` 과 `description` 둘뿐」)는 바깥 근거 없음 — EX-2 가 묻지 않았다. 고치지 않는다 |
| GD-4 | 같은 작업 폴더 `checkout -b` 금지 두 곳 | 계약에 넣음 | SK-10 |
| GD-5 | `/sprint` Step 3 판정 표 · 사본 둘 | 계약에 넣음 | SK-11 · SK-12. 사본은 목록이 적은 둘에 페이지 `docs/infra-kit/cicd.html` 를 더했다(같은 첫 줄을 글자 그대로 들고 있다) |
| GD-6 | 세 화면 규약 공통 숫자의 원문 절 | 계약에 넣음 | SK-13 · SK-14. 킷 다섯 자리의 숫자 재정의는 KD-3(design-kit 묶음)이 뒤따른다 |
| GD-7 | §3.7 사본 ①~④ 생성 측 짝 · 흔한 실수 사본 | 계약에 넣음 | SK-15 |
| GD-8 | §7 오류 문구 · `omitClaudeMd` · `experimental` · 문장 삭제 사본 절차 · 편향 수 | 계약에 넣음 | SK-07 · SK-08 · SK-09 (`ex/EX-2.md` §2.3 · §2.4 · `ex/EX-4.md` §A https://arxiv.org/html/2411.15594v6 · https://arxiv.org/html/2410.02736v1). `:1944` 「12 개 편향 분류」 는 처리됨 — EX-4 판정 「정확히 12」. 중첩 깊이 상한 오류의 글자는 바깥 근거 없음 — EX-2 §2.4 「원문에 없음」, 그래서 SK-07 (b) 는 그 문구를 원문에서 찾지 못했다고 적게 한다. 배치 우선순위(`:55-63`)는 처리됨 — EX-2 §2.2 순서와 같다 |
| GD-9 | 카이젠 Step 7 이 회귀 패턴 실행기를 부른다 | 계약에 넣음 | SK-16 |
| GD-10 | 판정값을 바꾸는 계약은 `templates/` 까지 찾는다 | 계약에 넣음 | SK-17 |
| GD-11 | QA 다시 부르기 전 앞 회차 리포트 처리 | 계약에 넣음 | SK-18 — 「커밋하거나 지운다」 가운데 커밋만 적는다(지우면 Iteration 셈이 되돌아간다, `qa-evaluator.md:992`) |
| GD-12 | harness-kaizen 커밋 머리 표 | 계약에 넣음 — 결정은 「표를 관행에 맞춘다」 | SK-19. 관행 실측은 GAP 분석 행 |
| UD-5 | 결정 전파 상태 값에 「대체됨」 | 계약에 넣음 | SK-20 · SK-21 · SC-02 · SC-03 · ER-01. 규칙이 적힌 자리는 원본 §6 · 검사 코드 · 킷 시험 · 쓰는 쪽 셋 · 문서 사이트 한 쪽이다(GAP 분석 두 행). 남은 일 목록 · 넘김 기록 · 봉인된 옛 계약은 입력 · 기록이라 고치지 않는다 |

결정 1 — 평가 가이드 조항 번호는 **둘째 `3.` 을 첫째 3 항의 이어지는 문단으로 합친다.** 번호를 4 · 5 · 6 으로 미는 길도 있지만 그러면 킷 글의 「조항 5」 인용
넷(infra-audit `:110` · planning-reviewer `:176` · plan-audit `:136` · react-reviewer `:383`)과 머리 「5 조항」 을 모두 바꿔야 한다. 합치면 머리 「5 조항」 과
「조항 3」 인용 넷이 그대로 맞고, 두 문단이 같은 주제(`[미검증]` 두 분류와 그 셈)다. reviewer 일곱의 사본은 어느 길이든 한 줄씩 바뀐다(SC-01).

결정 2 — 「대체됨」 은 `status: superseded` 로 쓴다. 기존 값 `approved` 와 같은 영문 꼴이고, 검사 코드가 영문 값을 비교한다. 대체된 결정은 승인 기록(`source`)이 있던
결정이라 목록에 남겨 추적하되, 화면 자리 검사는 그 결정을 대체한 `approved` 결정이 받는다. `superseded_by` 가 `approved` 결정을 바로 가리키게 해(사슬 금지) 검사가 한 번에 끝난다.

결정 3 — 이 계약은 기능 조건이 스물아홉이다(복잡 기준 20 초과 — Step 6.2 둘째 명령 출력). 나누지 않는다 — 부모가 이 묶음을 한 단위로 배정했고, 커밋은 어차피 킷(맨 위 폴더)마다
나뉘며(AR-01), 조건 대부분이 한 파일 한 문단을 재는 작은 조건이다.

범위 밖(이 계약이 고치지 않는다): `harness/references/contract-schema.md` · `feedback-schema.yaml`(cs 묶음) · `harness/scripts/`(hs 묶음) · PRD 없음 규칙 자리(pd 묶음) ·
위 두 쪽 밖의 `docs/` HTML 페이지(다시 만들 페이지는 notes 에 적어 문서 사이트 묶음으로 넘긴다) · 평가 가이드 `:1206-1209` 「한계」 문단의 「①~④ 의 짝은 다음 사이클 Phase 1 · 2 로
넘긴다」 문장(생성 측은 이 계약, 계약 측은 CS-3 — 두 묶음이 끝난 뒤 부모가 한 번에 맞춘다) · design-kit 다섯 자리의 숫자 재정의(KD-3) · howto-reviewer 사본(KH-1) ·
킷 `plugin.json` 버전(릴리스 단계 몫) · 기존 markdownlint 경고 정리(VS-26 — 사용자 결정 UD-7 「전부 고친다」 에 따라 같은 이어작업(after-kaizen-0926b)의 마지막 단계에서 부모가 모든 묶음의 결과 위에 한 번에 고친다. 다음 카이젠으로 넘기는 것이 아니다. 이 계약은 DG-02 로 자기가 더한 줄의 새 경고 0 만 잰다).

결정 4 — SK-07 (b) 는 `Subagent spawn limit reached` 를 지우라고 하지 않고, 남기면 원문에서 찾지 못했다고 적게 한다. 그 문구는 옛 판 가이드가 적은 것이라 다른 기록과 대조할 때 찾을 낱말로 남기되, 사실처럼 읽히지 않게 한다(EX-2 §2.4 「원문에 없음」). 지워도 (b) 는 통과한다.

교차 진단 반영(봉인 전) — SK-04 `CLAUSE_REFS` 에 design-reviewer · infra-reviewer · flutter 규약 · onboarding setup-guide 넷을 더했다(좁힘 — 재는 대상이 늘었다). 뒤의 둘은 평가 가이드가 아니라 skill 가이드 §3.7 조항을 가리켜 도우미가 세지 않는다(재 본 값 `refs_bad=4/14`). AR-02 에 넘길 것의 내용 짝(`KD-3` ↔ `§8.9`, `CS-3` ↔ `①~④`)을 더했다(좁힘).

커버리지 해소 — Step 6.5 (4) 검출기가 낸 `UNCOVERED` 의 처리:

- 커버리지 해소: AR-01 — 경로 기대 집합은 측정 도우미 `ALLOWED` 한 곳에만 적는다(목록을 두 번 적지 않는다)
- 커버리지 해소: SK-04 · SC-01 — 킷 글 열두 파일 · reviewer 일곱은 측정 도우미 `CLAUSE_REFS` · `REVIEWERS` 가 덮는다
- 커버리지 해소: SK-06 · SK-08 — 백틱 주소 둘 · 논문 번호 둘은 `m SK-06` · `m SK-08` 이 같은 글자로 센다
- 커버리지 해소: SK-11 · SK-18 — `/sprint` 는 `harness/skills/sprint/SKILL.md`(도우미 `SPR`)이고 `m SK-11` · `m SK-18` 이 연다. `evidence/phase9.md` 는 근거 인용이다. qa-evaluator 경로는 `m SK-18` 이 연다
- 커버리지 해소: SK-12 · SK-21 — 파일 경로는 측정 파이썬이 이름으로 연다
- 커버리지 해소: SK-13 · SK-14 — 세 규약 파일 이름과 `§8.9` · `skill-design-guide.md` 는 `m SK-13` · `m SK-14` 가 같은 글자로 센다
- 커버리지 해소: SK-20 · ER-01 · SC-02 — 결정 번호 `DEC-…` 와 입력 이름은 측정 도우미 `dg_inputs` 가 만든다
- 커버리지 해소: AR-02 — 스물한 토큰과 notes 경로는 `m AR-02` 의 토큰 목록과 `NOTES` 변수가 덮는다. 짝 낱말 `§8.9` · `①~④` 는 `m AR-02` 끝의 `kd3_what` · `cs3_what` 가 같은 글자로 센다
- 판별 해소: SK-02 · SK-05 ~ SK-11 · SK-13 · SK-14 · SK-16 ~ SK-20 은 산출물이 문서 문장이라 부를 코드가 없다. 옛 문장 0 과 새 낱말 줄 수로 잰다 —
  실행해서 재는 조건은 SK-01 · SK-03 · SK-04 · SK-12 · SK-21 · SC-01 ~ SC-03 · ER-01 · AR-01 ~ AR-03 이다

## 회귀 게이트 — 측정 도우미

평가 때 이 블록을 떼어 bash 에서 불러 쓴다. `TMPDIR` 은 평가자 임시 폴더로 준다. 도우미는 끝점을 `git archive` 로 풀어 재므로 작업 폴더의 미커밋 변경을 보지 않는다.
작업 폴더 밖 입력은 지우지 마라 — 도우미가 만든 `$T` 아래만 치워도 된다. AR-03 은 `~/.claude/rules/plain-korean.md` 를 읽는다(못 읽으면 `PK_UNREADABLE` · 종료 코드 2).

```bash
# 떼기: awk '/^# === 측정 도우미 시작/{f=1} f{print} /^# === 측정 도우미 끝/{exit}' <계약> > "$TMPDIR/gd-measure.sh"
# 부르기: bash -c 'source "$TMPDIR/gd-measure.sh" || exit 2; type m >/dev/null || exit 2; m SK-01'
# 시작 판: E_REF=BASE 를 주고 부른다
# === 측정 도우미 시작 (after-0926-guides) ===
# 쓰는 법: 이 블록을 파일로 떼어 bash 에서 source 한 뒤 `m <조건 ID>`. zsh 에서 부르지 마라.
# 잴 트리 E — 기본은 가지 끝(TIP)을 git archive 로 푼 임시 폴더. 시작 판을 재려면 E_REF=BASE.
W=${W:-/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak2-gd}
BR=${BR:-chore/ak2-gd}
BASE=$(git -C "$W" merge-base origin/main "$BR") || { echo "UNRESOLVED BASE"; return 2 2>/dev/null || exit 2; }
TIP=$(git -C "$W" rev-parse --verify "$BR") || { echo "UNRESOLVED TIP"; return 2 2>/dev/null || exit 2; }
T=$(mktemp -d "${TMPDIR:-/tmp}/gd.XXXXXX")
snap() { mkdir -p "$2" && git -C "$W" archive "$1" | tar -x -C "$2"; }
case "${E_REF:-TIP}" in
  BASE) E=$T/base; snap "$BASE" "$E" ;;
  *)    E=$T/tip;  snap "$TIP" "$E" ;;
esac
PVG=harness/docs/guides/plugin-validation-guide.md
QAG=harness/docs/guides/qa-evaluation-guide.md
AGG=harness/docs/guides/agent-design-guide.md
SDG=harness/docs/guides/skill-design-guide.md
SCK=harness/skills/sprint-contract/SKILL.md
SPR=harness/skills/sprint/SKILL.md
VCP=design-kit/references/visual-change-protocol.md
VCPH=docs/design-kit/visual-change-protocol.html
RPF=rust-kit/skills/rust-preflight/SKILL.md
# s 로 시작하는 줄부터 e 로 시작하는 다음 줄 앞까지
sec() { awk -v s="$1" -v e="$2" 'index($0,s)==1{f=1;print;next} f&&index($0,e)==1{exit} f' "$3"; }
# 표준 입력에서 글자 그대로 든 줄 수 (0 건에도 0 을 찍는다)
n() { grep -cF -- "$1" || true; }
# 표준 입력에서 두 글자를 함께 담은 줄 수
n2() { grep -F -- "$1" | grep -cF -- "$2" || true; }
gate() {  # 결정 전파 검사 코드를 문서에서 뗀다 (decision-gate-test.sh 와 같은 awk)
  awk '/^```python/{b=1;n="";next} b&&/^```/{if(ok){exit} b=0;next} b{n=n $0 "\n"; if($0 ~ /Decision Propagation Coverage Gate/) ok=1} END{printf "%s", n}' \
    "${1:-$E/$VCP}" > "$T/gate.py"
}
runc() { o=$(python3 "$T/gate.py" "$1" 2>&1); rc=$?; printf '%s' "$o" > "$T/last.txt"; printf '%s/%s' "$rc" "$(printf '%s\n' "$o" | grep -c '^Traceback')"; }
D1='  - decision_id: DEC-20260813-001\n    source: .design/approvals/DEC-20260813-001.md\n'
D2='  - decision_id: DEC-20260813-002\n    source: .design/approvals/DEC-20260813-002.md\n'
D3='  - decision_id: DEC-20260813-003\n    source: .design/approvals/DEC-20260813-003.md\n'
R='    required_surfaces:\n      - surface_id: a\n        golden: g.png\n        assertions: ["main visible"]\n    excluded_surfaces: []\n'
GOLDONLY='    required_surfaces:\n      - surface_id: a\n        golden: g.png\n'
dg_inputs() {  # 손으로 만든 결정 목록 — 기대 종료 코드는 §6 규칙에서 손으로 정했다
  printf "decisions:\n${D1}    status: approved\n${R}" > "$T/d-ok.yaml"
  printf "decisions:\n${D1}    status: superseded\n    superseded_by: DEC-20260813-002\n${GOLDONLY}${D2}    status: approved\n${R}" > "$T/d-sup.yaml"
  printf "decisions:\n${D1}    status: draft\n${R}" > "$T/d-draft.yaml"
  printf "decisions:\n${D1}    status: superseded\n${GOLDONLY}${D2}    status: approved\n${R}" > "$T/d-supnoby.yaml"
  printf "decisions:\n${D1}    status: superseded\n    superseded_by: DEC-20260813-009\n${D2}    status: approved\n${R}" > "$T/d-supdangling.yaml"
  printf "decisions:\n${D1}    status: superseded\n    superseded_by: DEC-20260813-001\n${D2}    status: approved\n${R}" > "$T/d-supself.yaml"
  printf "decisions:\n${D1}    status: superseded\n    superseded_by: DEC-20260813-002\n${D2}    status: superseded\n    superseded_by: DEC-20260813-003\n${D3}    status: approved\n${R}" > "$T/d-supchain.yaml"
  printf "decisions:\n${D1}    status: superseded\n    superseded_by: [DEC-20260813-002]\n${D2}    status: approved\n${R}" > "$T/d-supbytype.yaml"
  printf "decisions:\n  - decision_id: DEC-2026-1\n    source: s\n    status: superseded\n    superseded_by: DEC-20260813-002\n${D2}    status: approved\n${R}" > "$T/d-supbadid.yaml"
}
MDL=${MDL:-$T/mdl}
mdl_ready() {  # markdownlint-cli2 0.23.2 · MD013 끔 — 편집기 확장과 같은 설정
  [ -x "$MDL/node_modules/.bin/markdownlint-cli2" ] || { mkdir -p "$MDL" && (cd "$MDL" && npm install --no-save --no-audit --no-fund markdownlint-cli2@0.23.2 >/dev/null 2>&1); }
  printf '{ "config": { "MD013": false } }\n' > "$MDL/cfg.markdownlint-cli2.jsonc"
  [ -x "$MDL/node_modules/.bin/markdownlint-cli2" ]
}
added() { diff -U0 "$1" "$2" | awk '/^@@/{split($3,a,","); s=substr(a[1],2); c=(a[2]=="")?1:a[2]; for(i=0;i<c;i++) print s+i}'; }
newmd() {  # newmd <옛 파일|/dev/null> <새 파일> — 새 파일에서 더해진 줄에 걸린 경고 수
  ( cd "$(dirname "$2")" && "$MDL/node_modules/.bin/markdownlint-cli2" --config "$MDL/cfg.markdownlint-cli2.jsonc" "$(basename "$2")" 2>&1 ) \
    | awk -F: '/^[^ ]+:[0-9]+/{print $2+0}' | LC_ALL=C sort -u > "$T/w.txt"
  added "$1" "$2" | LC_ALL=C sort -u > "$T/a.txt"
  comm -12 "$T/w.txt" "$T/a.txt" | grep -c . || true
}
newsc() {  # newsc <옛 .sh> <새 .sh> — 더해진 줄에 걸린 shellcheck 경고 수
  shellcheck -f gcc "$2" 2>/dev/null | awk -F: '{print $2+0}' | LC_ALL=C sort -u > "$T/w.txt"
  added "$1" "$2" | LC_ALL=C sort -u > "$T/a.txt"
  comm -12 "$T/w.txt" "$T/a.txt" | grep -c . || true
}
ALLOWED='harness/docs/guides/plugin-validation-guide.md
harness/docs/guides/qa-evaluation-guide.md
harness/docs/guides/agent-design-guide.md
harness/docs/guides/skill-design-guide.md
harness/skills/create-agent/SKILL.md
harness/skills/create-skill/SKILL.md
harness/skills/sprint-contract/SKILL.md
harness/skills/sprint/SKILL.md
harness/agents/qa-evaluator.md
harness/skills/contract-kaizen/SKILL.md
harness/skills/evaluator-kaizen/SKILL.md
harness/skills/harness-kaizen/SKILL.md
api-kit/agents/api-reviewer.md
backend-kit/agents/backend-reviewer.md
design-kit/agents/design-reviewer.md
infra-kit/agents/infra-reviewer.md
planning-kit/agents/planning-reviewer.md
react-kit/agents/react-reviewer.md
rust-kit/agents/rust-reviewer.md
design-kit/references/visual-change-protocol.md
design-kit/evals/decision-gate-test.sh
design-kit/skills/design-test/SKILL.md
design-kit/skills/design-audit/SKILL.md
flutter-toolkit/references/visual-evidence-protocol.md
react-kit/references/render-evidence-protocol.md
rust-kit/skills/rust-preflight/SKILL.md
docs/infra/platform/cicd.md
docs/infra-kit/cicd.html
docs/design-kit/visual-change-protocol.html
.harness/sprint-contract-after-0926-guides.md
.harness/sprint-feedback-after-0926-guides.md
.harness/sprint-amendments-after-0926-guides.md
.harness/.meta/after-kaizen-0926b/gd-notes.md'
NOTES=.harness/.meta/after-kaizen-0926b/gd-notes.md
REVIEWERS='api-kit/agents/api-reviewer.md backend-kit/agents/backend-reviewer.md design-kit/agents/design-reviewer.md infra-kit/agents/infra-reviewer.md planning-kit/agents/planning-reviewer.md react-kit/agents/react-reviewer.md rust-kit/agents/rust-reviewer.md'
CLAUSE_REFS='backend-kit/skills/backend-audit/SKILL.md rust-kit/skills/rust-audit/SKILL.md infra-kit/skills/infra-audit/SKILL.md react-kit/references/render-evidence-protocol.md planning-kit/agents/planning-reviewer.md planning-kit/skills/plan-audit/SKILL.md react-kit/agents/react-reviewer.md backend-kit/agents/backend-reviewer.md design-kit/agents/design-reviewer.md infra-kit/agents/infra-reviewer.md flutter-toolkit/references/visual-evidence-protocol.md onboarding-kit/skills/setup-guide/SKILL.md'
PK=${PK:-$HOME/.claude/rules/plain-korean.md}

m() {
  case "$1" in
  SK-01) python3 - "$E" "$T" <<'PY'
import json, re, subprocess, sys
E, T = sys.argv[1], sys.argv[2]
g = open(f"{E}/harness/docs/guides/plugin-validation-guide.md", encoding="utf-8").read().splitlines()
i = next(k for k, l in enumerate(g) if l.startswith("### V8"))
j = next(k for k in range(i + 1, len(g)) if g[k].startswith("### V9"))
sec = g[i:j]
a = next(k for k, l in enumerate(sec) if l.startswith("**FAIL 예시 2**"))
s = next(k for k in range(a, len(sec)) if sec[k].startswith("```"))
e = next(k for k in range(s + 1, len(sec)) if sec[k].startswith("```"))
blk = sec[s + 1:e]
hdr = sorted({m.group(1) for l in blk for m in [re.match(r"#\s*([a-z0-9-]+)/hooks/hooks\.json", l)] if m})
cmds = [json.loads(m.group(1)) for l in blk for m in [re.match(r'\s*\{\s*"command":\s*("(?:[^"\\]|\\.)*")', l)] if m]
kit = hdr[0] if len(hdr) == 1 else None
miss = 0
for c in cmds:
    for p in re.findall(r'\$\{CLAUDE_PLUGIN_ROOT\}"?/([^\s"]+)', c):
        import os
        if not kit or not os.path.exists(f"{E}/{kit}/{p}"):
            miss += 1
norm = lambda x: " ".join(x.split())
ex = [norm(re.sub(r"^\s*#?\s*(→\s*)?", "", l)) for l in blk]
ex = [x for x in ex if x.startswith(("FAIL ", "V8 "))]
real = []
if kit:
    hj = f"{E}/{kit}/hooks/hooks.json"
    old = open(hj, encoding="utf-8").read() if os.path.exists(hj) else None
    os.makedirs(os.path.dirname(hj), exist_ok=True)
    json.dump({"hooks": {"SessionStart": [{"hooks": [{"type": "command", "command": c} for c in cmds]}]}}, open(hj, "w", encoding="utf-8"))
    out = subprocess.run(["python3", f"{E}/scripts/validate-plugin.py", kit, "--check=hook-exec"], capture_output=True, text=True).stdout
    if old is None:
        os.remove(hj)
    else:
        open(hj, "w", encoding="utf-8").write(old)
    real = [norm(l) for l in out.splitlines() if norm(l).startswith(("FAIL ", "V8 "))]
print(f"hdr={','.join(hdr) or '-'} cmds={len(cmds)} path_missing={miss} ex_fail={sum(x.startswith('FAIL ') for x in ex)} "
      f"real_fail={sum(x.startswith('FAIL ') for x in real)} ex_not_real={sum(x not in real for x in ex)}")
PY
    ;;
  SK-02) f=$E/$PVG
    echo "row_quote=$(grep -E '^\| V8 \|' "$f" | n '따옴표') log_quote=$(sec '## 8. 변경 이력' '다음 갱신 예정' "$f" | grep -E '^\| 20' | n2 'V8' '따옴표')" ;;
  SK-03) python3 - "$E" <<'PY'
import json, re, sys
E = sys.argv[1]
g = open(f"{E}/harness/docs/guides/plugin-validation-guide.md", encoding="utf-8").read().splitlines()
i = next(k for k, l in enumerate(g) if l.startswith("### 출력 포맷"))
j = next(k for k in range(i + 1, len(g)) if g[k].startswith("### "))
sec, code, prose, blocks, tot = g[i:j], False, [], 0, None
for l in sec:
    if l.startswith("```"):
        code = not code; continue
    if code:
        blocks += l.startswith("=== ")
        m = re.match(r"Total: (\d+) plugins(.*)", l)
        if m:
            tot = int(m.group(1)); rest = m.group(2)
    else:
        prose.append(l)
cnt = lambda w: int((re.search(rf"(\d+) {w}\b", rest) or [0, 0])[1]) if tot is not None else 0
K = len(json.load(open(f"{E}/.claude-plugin/marketplace.json", encoding="utf-8"))["plugins"])
note = sum("전체 실행" in l for l in prose)
print(f"total={tot} ok={cnt('OK')} warn={cnt('WARNING')} err={cnt('ERROR')} kits={K} blocks={blocks} note={note}")
PY
    ;;
  SK-04) python3 - "$E" $CLAUSE_REFS <<'PY'
import re, sys
E, refs = sys.argv[1], sys.argv[2:]
g = open(f"{E}/harness/docs/guides/qa-evaluation-guide.md", encoding="utf-8").read().splitlines()
h = g.index("## Canonical Unverified-Evidence Protocol (각 kit reviewer 복제용 정본)")
end = next(k for k in range(h + 1, len(g)) if g[k].startswith("## "))
sec = g[h:end]
head = [re.search(r"아래 (\d+) 조항", l) for l in sec if l.startswith("> ")]
head = [int(m.group(1)) for m in head if m]
items, cur, inside = {}, None, False
for l in sec:
    if not inside and re.match(r"^1\. \*\*마커는", l):
        inside = True
    if not inside:
        continue
    if l.startswith("> "):
        break
    m = re.match(r"^(\d+)\. ", l)
    if m:
        cur = int(m.group(1)); items.setdefault(cur, []).append([])
    if cur is not None:
        items[cur][-1].append(l)
nums = [k for k, v in items.items() for _ in v]
drift = sum("현재 drift" in l for l in sec)
checker = sum("check-reviewer-protocol-copies.py" in l for l in sec)
want = {1: "[정적]", 3: "env_gaps", 5: "조용한 PASS 금지"}
bad = tot = 0
pat = re.compile(r"(?<!§3\.7 5 )(?<!§3\.7 )조항 (\d)")
for f in refs:
    for l in open(f"{E}/{f}", encoding="utf-8"):
        for m in pat.finditer(l):
            if m.start() >= 2 and l[m.start() - 2:m.start()] == "5 ":
                continue
            tot += 1; k = int(m.group(1))
            body = items.get(k, [])
            if len(body) != 1 or k not in want or want[k] not in "\n".join(body[0]):
                bad += 1
print(f"nums={','.join(map(str, sorted(nums)))} head={','.join(map(str, head))} drift={drift} checker={checker} refs_bad={bad}/{tot}")
PY
    ;;
  SC-01) o=$(cd "$E" && python3 scripts/check-reviewer-protocol-copies.py 2>&1); rc=$?
    old=0; for f in $QAG $REVIEWERS; do c=$(grep -cE '^[>[:space:]]*3\. \*\*임계값 2 는' "$E/$f" || true); old=$((old + c)); done
    echo "rc=$rc [$(printf '%s\n' "$o" | tail -1)] old_second3=$old" ;;
  SK-05) f=$E/$AGG; c=$E/harness/skills/create-agent/SKILL.md
    echo "guide_inherit_default=$(grep -E '^\| `model` \|' "$f" | n '`inherit` (기본값)') guide_env=$(grep -E '^\| `model` \|' "$f" | n 'CLAUDE_CODE_SUBAGENT_MODEL') ca_old=$(n '`model` 을 생략하면 `inherit`' <"$c") ca_env=$(n 'CLAUDE_CODE_SUBAGENT_MODEL' <"$c")" ;;
  SK-06) c=$E/harness/skills/create-skill/SKILL.md; fm=$(sec '### frontmatter 필드 규칙' '### 3인칭' "$E/$SDG"); xp=$(sec '### 크로스 플랫폼 호환' '## 8.5.' "$E/$SDG")
    echo "csk_old=$(n '다른 플랫폼에서는 무시된다' <"$c") csk_std=$(n 'Agent Skills' <"$c") sdg_old=$(printf '%s\n' "$fm" | n '두 개의 필수 필드를 가지며') sdg_spec=$(printf '%s\n' "$fm" | n 'agentskills.io/specification') sdg_cc=$(printf '%s\n' "$fm" | n 'code.claude.com/docs/en/skills') xp_old=$(printf '%s\n' "$xp" | n '다른 플랫폼에서 무시됨') xp_guar=$(printf '%s\n' "$xp" | n '보장')" ;;
  SK-07) f=$E/$AGG
    c=$(python3 - "$f" <<'PY2'
import re, sys
t = open(sys.argv[1], encoding="utf-8").read()
ss = [x for x in re.split(r"(?<=다\.)\s+", t) if "Concurrent subagent limit reached" in x]
print(sum(("20" in x and "동시" in x) for x in ss))
PY2
)
    echo "unpaired=$(n2 '어느 문구가 어느 상한' '확인하지 못했다' <"$f") conc20=$c spawn_unmarked=$(grep -F 'Subagent spawn limit reached' "$f" | grep -cvE '찾지 못|원문에 없' || true) omit_unk=$(grep -E '^\| `omitClaudeMd` \|' "$f" | n '뜻 미확인') omit_md=$(grep -E '^\| `omitClaudeMd` \|' "$f" | n 'CLAUDE.md') exp_unk=$(grep -E '^\| `experimental` \|' "$f" | n '뜻 미확인') exp_ttl=$(grep -E '^\| `experimental` \|' "$f" | n 'cacheTtl')" ;;
  SK-08) f=$E/$QAG
    echo "over12=$(n '12 개 이상' <"$f") classes=$(grep -F '2411.15594v6' "$f" | grep -F '2410.02736v1' | grep -F 'task-agnostic' | n 'judgment-specific') row_exact12=$(grep -E '^- \[Justice or Prejudice' "$f" | n '12 개 편향 분류')" ;;
  SK-09) f=$E/$QAG; h=$(grep -E '^### ' "$f" | grep -F '문장' | grep -F '사본' | head -1)
    if [ -n "$h" ]; then s=$(awk -v s="$h" 'index($0,s)==1{f=1;print;next} f&&/^##/{exit} f' "$f"); else s=''; fi
    echo "sec=$(grep -E '^### ' "$f" | grep -F '문장' | grep -cF '사본' || true) inv=$(printf '%s\n' "$s" | n '[미검증:INVALID]') date=$(printf '%s\n' "$s" | n '2026-09-24')" ;;
  SK-10) s67=$(sec '### 6.7.' '### 7.' "$E/$SCK"); s9=$(sec '## 9.' '## 10.' "$E/$SDG")
    echo "s67_wt=$(printf '%s\n' "$s67" | n 'git worktree add') s67_warn=$(printf '%s\n' "$s67" | n2 'checkout -b' '작업 폴더') g9_cb=$(printf '%s\n' "$s9" | n 'checkout -b') g9_wt=$(printf '%s\n' "$s9" | n 'git worktree add')" ;;
  SK-11) s3=$(sec '### Step 3:' '### Step 4:' "$E/$SPR"); row=$(printf '%s\n' "$s3" | grep -F '| 실패 | 통과 | — |' | head -1)
    echo "old=$(n '내가 쓴 목록 밖이면 남의 미커밋이다' <"$E/$SPR") row_start=$(printf '%s\n' "$row" | n '시작') row_unknown=$(printf '%s\n' "$row" | n '귀속 불명') ci_env=$(printf '%s\n' "$s3" | n '환경 · 비결정성') ci_undec=$(printf '%s\n' "$s3" | n '미확정')" ;;
  SK-12) python3 - "$E" <<'PY'
import html, re, sys
E = sys.argv[1]
md = lambda p: open(f"{E}/{p}", encoding="utf-8").read()
row = lambda t: next((l for l in t.splitlines() if l.startswith("| 실패 | 통과 | — |")), "")
cell = lambda r: r.split("|")[4].strip() if r.count("|") >= 5 else ""
src = cell(row(md("harness/skills/sprint/SKILL.md")))
old = "내가 쓴 목록 밖이면 남의 미커밋이다"
copies = ["docs/infra/platform/cicd.md", "rust-kit/skills/rust-preflight/SKILL.md"]
same = [int(cell(row(md(p))) == src) for p in copies]
h = md("docs/infra-kit/cicd.html")
td = re.findall(r'<td class="verdict">(.*?)</td>', h, re.S)
def plain(x):
    x = re.sub(r"<code>(.*?)</code>", r"`\1`", x, flags=re.S)
    return " ".join(html.unescape(re.sub(r"<[^>]+>", "", x)).split())
hs = int(any(plain(t) == " ".join(src.split()) for t in td))
rp = md("rust-kit/skills/rust-preflight/SKILL.md")
qs = [q for l in rp.splitlines() if "표 첫 줄 판정 칸" in l for q in re.findall(r"「([^」]+)」", l)]
oldc = [md(p).count(old) for p in copies] + [h.count(old)]
print(f"old={','.join(map(str, oldc))} md_same={','.join(map(str, same))} html_same={hs} rp_quote_ok={int(bool(qs) and all(q in src for q in qs))}")
PY
    ;;
  SK-13) s=$(sec '## 8.9.' '## 9.' "$E/$SDG")
    echo "sec=$(grep -cE '^## 8\.9\. ' "$E/$SDG" || true) two=$(printf '%s\n' "$s" | n '2 개 이상') three=$(printf '%s\n' "$s" | n '3 회') names=$(for k in visual-change-protocol.md visual-evidence-protocol.md render-evidence-protocol.md; do printf '%s\n' "$s" | n "$k"; done | tr '\n' ',')" ;;
  SK-14) cite=""; for p in $VCP flutter-toolkit/references/visual-evidence-protocol.md react-kit/references/render-evidence-protocol.md; do cite="$cite$(n2 'skill-design-guide.md' '§8.9' <"$E/$p"),"; done
    echo "cite=$cite stale=$(n '그 절은 아직 없다' <"$E/$VCP"),$(n '그 절은 아직 없다' <"$E/react-kit/references/render-evidence-protocol.md")" ;;
  SK-15) s=$(sec '## 3.7.' '## 3.8.' "$E/$SDG")
    echo "t1=$(printf '%s\n' "$s" | n '첫 칸만 읽기') t2=$(printf '%s\n' "$s" | n '표에만 올린 시험') t3=$(printf '%s\n' "$s" | n '한 칸 못 읽으면') t4=$(printf '%s\n' "$s" | n '셸마다 다른 대상 수') common=$(printf '%s\n' "$s" | n '흔한 실수') cite=$(printf '%s\n' "$s" | n2 'qa-evaluation-guide.md' '산출물이 검사일 때')" ;;
  SK-16) a=$(sec '### Step 7:' '### Step 8:' "$E/harness/skills/contract-kaizen/SKILL.md"); b=$(sec '### Step 7:' '### Step 8:' "$E/harness/skills/evaluator-kaizen/SKILL.md")
    echo "ck=$(printf '%s\n' "$a" | n 'scripts/run-kaizen-assertions.py'),$(printf '%s\n' "$a" | n '종료 코드') ek=$(printf '%s\n' "$b" | n 'scripts/run-kaizen-assertions.py'),$(printf '%s\n' "$b" | n '종료 코드')" ;;
  SK-17) echo "scope=$(sec '### 1. 요구사항 분석' '### 3. 안티패턴' "$E/$SCK" | n2 'templates/' '판정값')" ;;
  SK-18) echo "spr=$(sec '### Step 4:' '### Step 4.5' "$E/$SPR" | n2 '앞 회차' '커밋') qae=$(n2 '앞 회차' '커밋' <"$E/harness/agents/qa-evaluator.md")" ;;
  SK-19) f=$E/harness/skills/harness-kaizen/SKILL.md; r=$(grep -E '^\| 커밋 메시지 \|' "$f")
    ex=$(printf '%s\n' "$r" | awk -F'|' '{print $4}' | grep -oE '`[^`]+`' | head -1 | tr -d '`' | sed -E 's/^([^:]+):.*/\1/')
    inlog=0; [ -n "$ex" ] && inlog=$(git -C "$W" log origin/main --no-merges --format='%(trailers:key=Kaizen-Phase,valueonly)%x09%s' | awk -F'\t' '$1 ~ /^kaizen-0924-p0[1-4]/' | cut -f2 | grep -cF -- "$ex:" || true)
    echo "kz=$(grep -cE '`kaizen: ?' "$f" || true) row_trailer=$(printf '%s\n' "$r" | n 'Kaizen-Phase:') step_trailer=$(grep -F '변경마다 커밋' "$f" | n 'Kaizen-Phase:') example=[$ex] example_in_log=$inlog" ;;
  SK-20) s6=$(sec '## 6. Decision Propagation Manifest' '## 7.' "$E/$VCP")
    echo "sup_status=$(printf '%s\n' "$s6" | n2 '`status`' '`superseded`') sup_by=$(printf '%s\n' "$s6" | n 'superseded_by') old_one=$(printf '%s\n' "$s6" | n '`approved` 하나다')" ;;
  SK-21) python3 - "$E" <<'PY'
import html, re, sys
E = sys.argv[1]
r = lambda p: open(f"{E}/{p}", encoding="utf-8").read()
dt = r("design-kit/skills/design-test/SKILL.md"); s = dt[dt.index("### Step 5-b"):]; s = s[:s.index("\n### ", 5)]
da = next(l for l in r("design-kit/skills/design-audit/SKILL.md").splitlines() if l.startswith("14. **Decision Propagation"))
dr = next(l for l in r("design-kit/agents/design-reviewer.md").splitlines() if l.startswith("12. **Decision Propagation"))
md = r("design-kit/references/visual-change-protocol.md")
mb = re.search(r'```python\n(#!/usr/bin/env python3\n"""Decision Propagation Coverage Gate.*?)```', md, re.S).group(1)
h = r("docs/design-kit/visual-change-protocol.html")
blocks = [html.unescape(re.sub(r"<[^>]+>", "", b)) for b in re.findall(r"<pre[^>]*>(.*?)</pre>", h, re.S)]
hb = next((b for b in blocks if "Decision Propagation Coverage Gate" in b), "")
norm = lambda t: [l.rstrip() for l in t.strip().splitlines()]
print(f"dt={s.count('superseded')} da={da.count('superseded')} dr={dr.count('superseded')} h_old={h.count('approved</code> 하나다')} h_by={h.count('superseded_by')} h_same={int(norm(mb) == norm(hb))}")
PY
    ;;
  SC-02) gate; dg_inputs; out=""; for c in ok sup draft; do out="$out $c=$(runc "$T/d-$c.yaml")"; [ "$c" = sup ] && out="$out sup_count=$(grep -cE 'superseded=1\b' "$T/last.txt" || true)"; done; echo "${out# }" ;;
  ER-01) gate; dg_inputs; out=""; for c in supnoby supdangling supself supchain supbytype supbadid; do out="$out $c=$(runc "$T/d-$c.yaml")"; done; echo "${out# }" ;;
  ER-01N) # 음성 대조 — 시작 판 검사 코드에 superseded 를 받아들이고 건너뛰게만 한 사본: superseded_by 검사가 없으면 넷이 0/0 이 된다
    git -C "$W" show "$BASE:$VCP" > "$T/base-doc.md"; gate "$T/base-doc.md"; dg_inputs
    python3 - "$T/gate.py" <<'PY'
import sys
p = sys.argv[1]; s = open(p, encoding="utf-8").read()
s = s.replace('    if d.get("status") != "approved":', '    if d.get("status") == "superseded":\n        continue\n    if d.get("status") != "approved":', 1)
open(p, "w", encoding="utf-8").write(s)
PY
    out=""; for c in sup supnoby supdangling supself supchain supbytype; do out="$out $c=$(runc "$T/d-$c.yaml")"; done; echo "${out# }" ;;
  SC-03) g=$E/design-kit/evals/decision-gate-test.sh; git -C "$W" show "$BASE:$VCP" > "$T/base-doc.md"
    o=$(bash "$g" 2>&1); rc=$?; ob=$(DECISION_GATE_DOC="$T/base-doc.md" bash "$g" 2>&1)
    echo "rc=$rc [$(printf '%s\n' "$o" | tail -1)] sup_cases=$(printf '%s\n' "$o" | grep -cE '^일치 sup' || true) base_doc_bad=$(printf '%s\n' "$ob" | grep -cE '^불일치 sup' || true)" ;;
  AR-01) ch=$(git -C "$W" diff --name-only "$BASE" "$TIP")
    extra=$(printf '%s\n' "$ch" | grep . | grep -vxF -f <(printf '%s\n' "$ALLOWED") | grep -c . || true)
    kits=""; for k in harness design-kit flutter-toolkit react-kit rust-kit api-kit backend-kit infra-kit planning-kit docs; do kits="$kits $k=$(printf '%s\n' "$ch" | grep -c "^$k/" || true)"; done
    multi=0; for c in $(git -C "$W" rev-list "$BASE..$TIP"); do t=$(git -C "$W" show --name-only --format= "$c" | awk -F/ 'NF{print $1}' | sort -u | grep -c .); [ "$t" -gt 1 ] && multi=$((multi + 1)); done
    echo "base=${BASE:0:7} tip=${TIP:0:7} changed=$(printf '%s\n' "$ch" | grep -c . || true) extra=$extra$kits multi_top=$multi"
    [ "$extra" = 0 ] || printf '%s\n' "$ch" | grep . | grep -vxF -f <(printf '%s\n' "$ALLOWED") ;;
  AR-02) b=$(git -C "$W" show "$TIP:$NOTES" 2>/dev/null); c=$([ -n "$b" ] && echo 1 || echo 0); out="committed=$c"
    for k in GD-1 GD-2 GD-3 GD-4 GD-5 GD-6 GD-7 GD-8 GD-9 GD-10 GD-11 GD-12 UD-5 tone-guide 처리됨 docs/harness/plugin-validation.html docs/harness/qa-evaluation-guide.html docs/harness/skill-design-guide.html docs/harness/agent-design-guide.html KD-3 CS-3; do out="$out $(printf '%s\n' "$b" | grep -cE -- "(^|[^0-9A-Za-z-])${k}([^0-9]|\$)" || true)"; done
    echo "$out kd3_what=$(printf '%s\n' "$b" | n2 'KD-3' '§8.9') cs3_what=$(printf '%s\n' "$b" | n2 'CS-3' '①~④')" ;;
  AR-03) [ -r "$PK" ] || { echo "PK_UNREADABLE $PK"; return 2; }
    git -C "$W" diff -U0 "$BASE" "$TIP" -- . ':(exclude).harness' > "$T/d.txt" || { echo "DIFF_FAIL"; return 2; }
    python3 - "$PK" "$T/d.txt" <<'PY2'
import re, sys
from collections import Counter
words = []
for l in open(sys.argv[1], encoding="utf-8"):
    c = [x.strip() for x in l.strip().strip("|").split("|")]
    if len(c) >= 3 and c[2] == "on":
        words += [w.strip() for w in c[0].split(" / ") if w.strip()]
add, rem = Counter(), Counter()
lines = open(sys.argv[2], encoding="utf-8").read().splitlines()
na = 0
for l in lines:
    if l.startswith(("+++", "---")) or not l[:1] in "+-":
        continue
    na += l[0] == "+"
    for w in words:
        pat = rf"(?<![A-Za-z]){re.escape(w)}(?![A-Za-z])" if re.fullmatch(r"[A-Za-z +\-]+", w) else re.escape(w)
        k = len(re.findall(pat, l[1:]))
        (add if l[0] == "+" else rem)[w] += k
new = {w: add[w] - rem[w] for w in add if add[w] > rem[w]}
print(f"words={len(words)} added_lines={na} new_hits={sum(new.values())} {sorted(new)}")
PY2
    ;;
  DG-02) mdl_ready || { echo "MDL_NOT_READY"; return; }; tot=0; rows=""
    for f in $(git -C "$W" diff --name-only "$BASE" "$TIP" -- '*.md' ':(exclude).harness'); do
      o=$T/old.md; git -C "$W" show "$BASE:$f" > "$o" 2>/dev/null || : > "$o"
      c=$(newmd "$o" "$E/$f"); tot=$((tot + c)); rows="$rows $f=$c"; done
    s=design-kit/evals/decision-gate-test.sh; git -C "$W" show "$BASE:$s" > "$T/old.sh"; sc=$(newsc "$T/old.sh" "$E/$s")
    echo "md_new=$tot sh_new=$sc |$rows" ;;
  *) echo "모르는 조건 $1"; return 2 ;;
  esac
}
# === 측정 도우미 끝 ===
```

봉인 전 실측(2026-09-26, 시작점 `6378948` 을 풀어 둔 판, `E_REF` 없이 — 끝점이 아직 시작점과 같다. 도우미를 떼어 bash 로 돌린 출력 그대로):

| 조건 | 값 |
| --- | --- |
| SK-01 · SK-02 · SK-03 | `hdr=design-kit cmds=2 path_missing=1 ex_fail=1 real_fail=2 ex_not_real=1` · `row_quote=0 log_quote=0` · `total=2 ok=1 warn=0 err=1 kits=14 blocks=2 note=0` |
| SK-04 · SC-01 | `nums=1,2,3,3,4,5 head=5 drift=1 checker=0 refs_bad=4/14` · `rc=0 [checked=7 violations=0 infra_errors=0 excluded=1] old_second3=8` |
| SK-05 · SK-06 | `guide_inherit_default=1 guide_env=0 ca_old=1 ca_env=0` · `csk_old=1 csk_std=0 sdg_old=1 sdg_spec=0 sdg_cc=0 xp_old=1 xp_guar=0` |
| SK-07 · SK-08 · SK-09 | `unpaired=1 conc20=0 spawn_unmarked=1 omit_unk=1 omit_md=0 exp_unk=1 exp_ttl=0` · `over12=1 classes=0 row_exact12=1` · `sec=0 inv=0 date=0` |
| SK-10 · SK-11 · SK-12 | `s67_wt=0 s67_warn=0 g9_cb=0 g9_wt=0` · `old=1 row_start=0 row_unknown=0 ci_env=0 ci_undec=0` · `old=1,1,1 md_same=1,1 html_same=1 rp_quote_ok=1` |
| SK-13 · SK-14 · SK-15 | `sec=0 two=0 three=0 names=0,0,0,` · `cite=0,0,0, stale=1,1` · `t1=0 t2=0 t3=0 t4=0 common=0 cite=0` |
| SK-16 · SK-17 · SK-18 · SK-19 | `ck=0,0 ek=0,0` · `scope=0` · `spr=0 qae=0` · `kz=2 row_trailer=0 step_trailer=0 example=[kaizen] example_in_log=0` |
| SK-20 · SK-21 | `sup_status=0 sup_by=0 old_one=1` · `dt=0 da=0 dr=0 h_old=1 h_by=0 h_same=1` |
| SC-02 · SC-03 | `ok=0/0 sup=2/0 sup_count=0 draft=2/0` · `rc=0 [결과: 16 경우 중 불일치 0] sup_cases=0 base_doc_bad=0` |
| ER-01 · ER-01N | 여섯 다 `2/0` · `sup=0/0 supnoby=0/0 supdangling=0/0 supself=0/0 supchain=0/0 supbytype=0/0` |
| AR-01 · AR-02 · AR-03 · DG-02 | `changed=0 extra=0` 열 값 모두 0 `multi_top=0` · `committed=0` 과 0 스물하나 `kd3_what=0 cs3_what=0` · `words=69 added_lines=0 new_hits=0` · `md_new=0 sh_new=0` |
| 양성 대조(임시 복제본) | AR-01 `extra=1 multi_top=1` · AR-02 `committed=1` 과 1 스물하나 · AR-03 `new_hits=1 ['게이트']` · DG-02 `md_new=2 sh_new=1` · SC-01 `violations=7` · AP-03 · AP-04 종료 코드 2 |
| DG-05 (시작 판 ci-local) | `rc=0` 25 · `feedback-agg-test SKIP (yq 없음)` 한 줄 · `kaizen-assertions` · `reviewer-copies` · `decision-gate-test` 모두 `rc=0` |

## 리서치 소스

바깥 문서는 새로 찾지 않았다. Codex 가 원문을 인용해 둔 대조 결과만 쓴다(읽기만).

- EX-1 hooks — `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0926b/.harness/.meta/after-kaizen-0926b/ex/EX-1.md` · https://code.claude.com/docs/en/hooks
- EX-2 sub-agents — `.../ex/EX-2.md` · https://code.claude.com/docs/en/sub-agents
- EX-3 skills — `.../ex/EX-3.md` · https://code.claude.com/docs/en/skills · https://agentskills.io/specification
- EX-4 편향 논문 — `.../ex/EX-4.md` · https://arxiv.org/html/2411.15594v6 · https://arxiv.org/html/2410.02736v1
- 저장소 안 근거 — `.harness/.meta/kaizen-0924/phase1-notes.md:95-97` · `phase3-notes.md:101-102` · `phase6-notes.md:115` · `phase8-notes.md:94` · `phase9-notes.md:94` ·
  `phase13-notes.md:104-105` · `phase4-notes.md:140` · `.harness/.meta/evidence/phase9.md:134-150` · `.harness/.meta/after-kaizen-0926/c4b-notes.md:110-118` · `c4d-notes.md:37` · `c3a-notes.md:21` · `:37`
  (모두 `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0926b` 판)
