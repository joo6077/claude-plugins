---
feature: "킷 reviewer 일곱의 미검증 규칙을 평가 가이드 새 판(v5.1)으로"
slug: after-0924-reviewer-unverified
created: "2026-09-26 16:35"
complexity: "복잡"
conditions: 23
status: active
owner_session: bda55d45-296c-491f-89ba-b52042d58e72
conditions_digest: sha256:3da851e5d1e58f0e
locked_at: "2026-09-26 17:02"
---

## 배경

킷마다 따로 설치되는 감사 에이전트(reviewer) 일곱이 평가 가이드 `harness/docs/guides/qa-evaluation-guide.md` §Canonical Unverified-Evidence Protocol
(「잴 수 없었던 항목」 을 어떻게 적고 몇 건에서 불합격으로 볼지 정한 절)의 사본을 들고 있다. 원문은 v5.1(2026-09-24)이고 이 절의 마지막 변경은
2026-09-19 커밋 `4c1867c` 다. 사본은 옛 판 둘로 갈라져 있다.

- design · planning · react · api 넷은 2026-07-27 판이다. 못 잰 항목을 한 장부로 세어 2 건이면 불합격이고, 「도구가 없어 못 잰 것」 과 「증거가 비어 있는 것」 을
  가르지 않는다(`design-kit/agents/design-reviewer.md:29-30` · `planning-kit/agents/planning-reviewer.md:30-35` · `react-kit/agents/react-reviewer.md:171-176` ·
  `api-kit/agents/api-reviewer.md:59-62`, api 는 문구까지 줄였다)
- backend · rust · infra 셋은 2026-08-13 판이다. 두 장부로 나눴지만 원문 조항 1 의 N/A 구분표와 새 조항 2(정적 분석기가 없는 스택에서 DG 조건 처리)가 없고
  (`rust-kit/agents/rust-reviewer.md:51` 이 「옮기지 않았다」 고 적었다), 남용 방지 4 요건은 낱말을 킷에 맞게 바꿔 옮겼다

근거 기록: F1H-47 · F1H-48(`.harness/.meta/kaizen-0924/f1-harness-followups-notes.md:118-119`), `phase8-notes.md:92` · `:96`,
`f1-kit-followups-notes.md` 69 · 70 행(`:100-101`). 70 행은 planning 사본이 「4 요건」 을 말하면서 그 뜻을 안 들고 있다고 짚었다.

**사용자 결정.** 이 세션의 질문(AskUserQuestion)에서 사용자가 「일곱 다 한 번에」 를 골랐다 — 불합격 기준이 바뀐다는 설명을 읽고 고른 것이다
(세션 기록 `/Users/jackson/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/bda55d45-296c-491f-89ba-b52042d58e72.jsonl` 1187 행,
`2026-09-26T02:47:55.337Z`, 핸드오프 `.harness/handoff/2026-09-26-0110.md` §C4 2 번).

**무엇이 바뀌나.** 지금 design · planning · react · api 는 못 잰 항목이 2 개면 무조건 불합격이다. 새 판은 못 잰 까닭을 둘로 나눈다. 감사자가 어쩔 수 없는
도구·환경 부재(남용 방지 4 요건을 다 적은 것, `[미검증:ENV]`)는 불합격 셈에서 빼고, 대신 잰 비율이 0.60 아래로 떨어지면 판정을 보류(`BLOCKED`)한다.
증거가 비었거나 4 요건을 못 채운 것(`[미검증:INVALID]`, 접미 없는 옛 `[미검증]` 포함)만 2 건에서 불합격이다. 일곱 사본은 같은 글이 되고,
원문 몇 판에서 왔는지 한 줄씩 적는다. 사본이 원문과 같은지는 CI(저장소에 올릴 때 자동으로 도는 검사)가 매번 잰다.

**판단 기록** — 저장소 안 근거로 정했다.

1. 사본 범위 — 원문 조항 덩어리(`qa-evaluation-guide.md:1244-1295`)와 남용 방지 4 요건(`:891-897`)을 글자 그대로 옮긴다. 4 요건까지 옮기는 까닭:
   조항 3(앞쪽)이 「남용 방지 4 요건 충족」 을 조건으로 쓰는데 그 뜻이 같은 절에 없고, 킷은 따로 설치되므로 사본이 뜻을 들고 있어야 한다(70 행이 짚은 결함).
2. 원문 번호 — 원문 조항 번호가 1 · 2 · 3 · 3 · 4 · 5 다(3 이 둘, `:1275` · `:1282`). 원문 고치기는 이 계약 범위 밖이라 사본도 그대로 옮긴다. 그래서
   (a) 킷 글이 사본 조항을 「조항 2」 로 가리키면 이제 DG 조항을 가리키게 되므로 그런 곳은 조항 첫머리 글(예: 「`[미검증]` 은 검증 도구·환경 부재 전용이며」)로 바꾸고,
   「조항 3」 은 사본 안에 3 이 둘이라 어느 쪽인지 알 수 없으므로 reviewer 일곱의 사본 밖 글에서는 같은 방식으로 첫머리 글(예: 「임계값 2 는」)로 바꾼다
   (시작 판 여섯 곳: `backend-kit/agents/backend-reviewer.md:68` · `:127` · `design-kit/agents/design-reviewer.md:178` · `planning-kit/agents/planning-reviewer.md:117` ·
   `react-kit/agents/react-reviewer.md:327` · `rust-kit/agents/rust-reviewer.md:166`, 교차 진단이 짚었다)
   (b) 마크다운 검사가 번호마다 MD029 경고를 3 개씩 내므로(원문에도 `:1282` · `:1288` · `:1293` 세 개가 있다) 사본 앞뒤를 MD029 끄기 · 켜기 주석 쌍
   (`<!-- markdownlint-disable MD029 -->` · `<!-- markdownlint-enable MD029 -->`)으로 감싸 경고를 늘리지 않는다. 원문 번호 정리는 넘긴다.
3. 「계약」 낱말 — 원문은 qa-evaluator 용이라 「계약」 · 「조건」 이라 쓴다. 사본은 글자를 바꾸지 않고, 출처 한 줄에 「사본의 「계약」 은 이 에이전트의 감사 기준을 뜻한다」
   같은 풀이를 붙인다. backend · rust · infra 가 전에 낱말을 바꿔 옮긴 까닭을 이 한 줄이 대신한다. 출처 줄은 원문 경로 · `v5.1` · 「계약」 풀이를 한 줄에 함께 담는다.
   설명을 다음 줄로 이어 써도 되지만 그 줄에는 세 낱말을 한꺼번에 넣지 않는다(SK-01 이 세 낱말이 함께 든 줄을 정확히 1 줄로 센다)
4. 판정값 대응 — 킷마다 판정 이름이 다르다. 새 판의 세 결과(증거 무효 2 건 → 불합격 · 잰 비율 0.60 미만 → 보류 · 증거 무효 1 건 → 경고와 함께 통과)를
   `## GAP 분석` 의 판정 대응표대로 옮긴다. planning 은 불합격 자리를 지금처럼 `NEEDS_VERIFICATION` 으로 둔다(`planning-kit/skills/plan-audit/SKILL.md:133` 이 이미 그렇게 쓴다).
   보류는 원문 · 다른 여섯 킷과 같은 `BLOCKED` 에 사유 `insufficient_verified_coverage` 를 붙인다 — 한 판정 이름에 사유 둘을 쓰는 선례가 `infra-kit/agents/infra-reviewer.md:133` · `:136` 이다.
   react 는 판정값이 APPROVE · REJECT 둘뿐이라 `BLOCKED` 를 더하고, 이를 받아 쓰는 react-audit 리포트 틀도 같이 바꾼다.
5. 기계 대조 시험을 둔다 — 사본이 원문을 못 따라간 기록이 셋이다: 원문 머리말의 「현재 drift (2026-07-27 실측)」(`qa-evaluation-guide.md:1238-1242`),
   backend 가 「"문구 변형 없이 복제" 주장이 사실과 달랐다」 고 적은 2026-08-13 재동기화(`backend-kit/agents/backend-reviewer.md:74-76`),
   2026-09-24 Phase 8 이 일곱 모두 새 판이 없다고 적은 기록(`phase8-notes.md:92`). 레포 규칙은 같은 실수가 세 번이면 사람 다짐이 아니라 기계 검사로 올린다
   (`harness/docs/guides/skill-design-guide.md` §3.7 강제 등급 표, `.claude/skills/infra-kaizen/SKILL.md:34` 가 옮겨 적은 「2 회 재발 → E2, 3 회 → E3」).
   그래서 `scripts/check-reviewer-protocol-copies.py` 를 새로 두고 CI `validate` 묶음에 한 단계로 넣는다. `scripts/validate-plugin.py` 에 검사를 더하지 않는 까닭:
   등록 검사 수가 문서 여러 곳(문서 사이트 포함)에 적혀 있어 범위 밖 문서까지 고쳐야 한다.
6. 새로 찾은 소비면 — backend-audit · rust-audit 는 두 장부로 이미 나눴지만 APPROVE 조건이 「전 카테고리(row) PASS」 라 도구 부재(`[미검증:ENV]`) 항목이 하나라도
   있으면 어느 판정에도 걸리지 않는다(`backend-kit/skills/backend-audit/SKILL.md:113` · `rust-kit/skills/rust-audit/SKILL.md:125` · `rust-kit/agents/rust-reviewer.md:168`).
   「ENV 는 불합격 셈에서 뺀다」 와 어긋나므로 같이 맞춘다. infra-audit 는 우선순위 목록(`infra-kit/skills/infra-audit/SKILL.md:103-108`)이 이미 새 판과 같아 고치지 않는다.
   api-kit 스킬에는 api-reviewer 를 부르는 글이 없다(`grep -rlF api-reviewer api-kit/skills` 0 파일) — 소비면 없음.
7. design-kit 시험 파일 한 줄 — `design-kit/evals/evals.json:451` 이 「미검증 2건 이상이면 FAIL 0이어도 REJECT로 판정한다」 로 옛 규칙을 적고 있다. 소비면이라 같이 고친다.
8. 같은 문구를 쓰는 다른 파일 — 교차 진단이 「미검증 2 건 이상」 문구로 저장소 전체를 찾아 다섯 곳을 더 짚었다. 둘로 갈린다.
   - 만드는 쪽(스킬이 자기 완료를 보고하는 쪽) 규칙이라 맞는 것 넷: `infra-kit/skills/infra-test/SKILL.md:449` · `react-kit/references/render-evidence-protocol.md:205` ·
     `flutter-toolkit/references/visual-evidence-protocol.md:141-142` · `onboarding-kit/skills/setup-guide/evals/evals.json:87` 의 「2 건 이상이면 부분 완료」 는
     `harness/docs/guides/skill-design-guide.md` §3.7 5 조항 3 항이 정본이고, 그 절이 `:308` 에서 「2 건 기준은 양쪽이 세는 대상이 다르다 — 생성 측은 `[미검증]` 전체로
     부분 완료를 가르고, 평가 측은 `INVALID` 만으로 REJECT 를 가른다」 고 적었다. 평가 쪽 규칙을 바꾸는 이 계약이 고칠 글이 아니다
   - 평가 쪽 옛 사본인 것 하나: `flutter-toolkit/skills/flutter-audit/SKILL.md:32-49` 가 옛 다섯 조항(3 분기 · 「임계값은 2 다」)을 들고 있다. flutter-toolkit 에는
     `agents/*-reviewer.md` 가 없어 사용자가 고른 일곱 밖이고 새 검사도 이 파일을 보지 않는다 — `## 범위 경계` 에 넘김으로 적는다

**사용자 승인(Step 5).** 사용자가 「다음 세션에서 직접할 일을 다 실행하고 이어질것도 실행해」(세션 기록
`/Users/jackson/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/de8c7935-a5b6-4df5-9106-fafa73c288a0.jsonl`, user `2026-09-26T01:04:21.505Z`)와
「나한테 물어보지 말고 자동으로 끝까지」(같은 기록 `2026-09-24T04:04:16.964Z`)로 맡겼다. 이 계약의 합의는 그 위임으로 받은 것으로 적는다.
일곱을 한 번에 바꾸는 결정 자체는 사용자가 이 세션에서 직접 골랐다(위 1187 행). 사용자가 할 일: 없음

## 리서치 소스

바깥 자료를 새로 찾지 않는다(웹 검색 · 외부 문서 가져오기 금지). 입력은 모두 레포 안에 있다.

- 원문: `harness/docs/guides/qa-evaluation-guide.md` §Canonical Unverified-Evidence Protocol(`:1231-1299`) · §증거 분류 triage 의 4 요건(`:889-901`) ·
  §카운팅 및 자동 REJECT 임계(`:915-946`, 판정 우선순위)
- 근거 기록: `.harness/.meta/kaizen-0924/f1-harness-followups-notes.md:118-119` · `phase8-notes.md:92` · `:96` · `f1-kit-followups-notes.md:100-101` · `:154`
- 핸드오프: `.harness/handoff/2026-09-26-0110.md` §C2 · §C4 2 번
- 레포 규칙: `harness/references/contract-schema.md`(봉인 · 범위 조건 · 양성 대조 · 알려진 답 대조) · `harness/evals/gate-exit-codes.md`(검사 스크립트 종료 코드 0 · 1 · 2 · 3) ·
  `tone-kit/references/locale-korean.md` §2 · §8(번역투 여섯 패턴)
- 선례: `scripts/check-stale-values.py` 의 `EXCLUDED_KITS`(빼는 대상을 이유와 함께 출력) · 짝 계약 `after-0924-rust-app-name`(측정 공통 정의 틀)

## GAP 분석 · 판정 대응표 · 개선안

### 복잡도 (Step 1)

| 축 | 물음 | 값 |
| -- | ---- | -- |
| 레이어 수 | 몇 계층을 지나가나 | 셋 — 에이전트 규칙 글 · 그것을 받아 쓰는 감사 스킬과 시험 파일 · CI 검사 스크립트 |
| 공개 동작 변경 | 밖에서 보이는 판정 규칙이 바뀌나 | 예 — 불합격 · 보류 문턱이 바뀐다(사용자가 알고 고름) |
| 소비면 존재 | 받아 쓰는 반대편이 있나 | 예 — 감사 스킬 다섯(design · planning · react · backend · rust)과 design 시험 파일 한 줄. infra-audit 는 이미 맞고 api 는 없다 |
| 멀쩡하던 게 다시 망가질 위험 | 기존 동작이 깨질 수 있나 | 예 — 사본 교체 중 킷 고유 적용 글을 지우거나, 판정 목록이 어느 경우에도 안 걸리는 빈틈이 생길 수 있다 |

네 축이 모두 「예」 라 **복잡**이다. 공개 동작 변경 · 소비면이 둘 다 예라 Step 2.5 양면 조건을 넣었다(만드는 쪽 SK-01 ~ SK-05, 받아 쓰는 쪽 SK-06 · SK-07).

### 설정 리터럴 대조 (Step 1.2)

| config key | project.yaml 에서 읽은 값 | 계약에 쓴 값 |
| ---------- | ------------------------- | ------------ |
| `commands.analyze` | `bash -n scripts/release.sh` | DG-01 N/A 사유에 그대로 |
| `commands.test` | `bash scripts/release.sh 2>&1 \|\| true` | DG-03 N/A 사유에 그대로 |
| `diagnostics.ide_exclude` | `[]` | DG-02 에 `[]` |
| `contract_categories[].id` / `prefix` | `Skill`/`SK` · `Script`/`SC` · `Error`/`ER` · `Architecture`/`AR` | 같은 네 절 |
| `anti_patterns[].id` / `message` | AP-01 버전 하드코딩 · AP-02 force push · AP-03 bare code fence(V6) · AP-04 frontmatter name 누락(V1) | AP-03 · AP-04 를 고른다(바뀌는 파일이 마크다운 · 에이전트 frontmatter). AP-01 은 `plugin.json` 버전을 건드리지 않고, AP-02 는 push 를 하지 않아 걸릴 곳이 없다 |

### Pre-Edit 감사 (Step 1.4)

시작 판(`f81568d`)의 파일을 직접 읽었다. 줄 번호는 시작 판 기준이다.

| 대상 파일 | 실제 Read 증거 (`파일:라인`) | 발견한 것 | 조건 |
| --------- | ---------------------------- | --------- | ---- |
| `design-kit/agents/design-reviewer.md` | `:26` 규칙 8 머리 · `:28-32` 옛 사본 · `:34` 「임계 2 건에 도달하면」 · `:36` 「3 분기」 · `:124` 「조항 2」 · `:155` 「도구 부재 / 증거 무효」 · `:172-173` 판정값 · `:178-188` 판정 규칙(미검증 한 장부) | 옛 판 · 보류 없음 · `:185` 는 미검증 0 건에도 CONDITIONAL(L3 부분 커버리지)을 쓴다(원문 「1 건 + FAIL 0 에서만」 과 어긋남, 옛 판부터 있던 것) | SK-01 ~ SK-03 · SK-05 |
| `design-kit/skills/design-audit/SKILL.md` | `:32` Gotcha 11 이 임계를 다시 적음 · `:110` 도구 부재/증거 무효 누계 · `:115` · `:121-122` 판정 | 옛 한 장부 · 보류 없음 | SK-06 · SK-07 |
| `design-kit/evals/evals.json` | `:451` 「미검증 2건 이상이면 FAIL 0이어도 REJECT로 판정한다」 | 옛 규칙 문장 | SK-06 |
| `planning-kit/agents/planning-reviewer.md` | `:22-43` 옛 사본 · `:45-48` N/A 적용 주석 · `:60` 「canonical 조항 2 의 3 분기」 · `:74` `reason:` 에 N/A 칸 없음 · `:82` 「조항 2·3」 · `:117-123` 미검증 축 · `:155-156` 「4 요건」 을 말하나 뜻이 없음 | 옛 판 · 새 조항 1 은 N/A 에 사유를 요구 | SK-01 ~ SK-05 |
| `planning-kit/skills/plan-audit/SKILL.md` | `:24` Gotcha 9 · `:25` 「canonical 조항 2 의 3 분기」 · `:95` · `:97` 요약 틀 · `:127` BLOCKED = FAIL 4 개 이상 · `:129-133` 미검증 축 | 옛 한 장부 · 보류 없음 | SK-06 · SK-07 |
| `react-kit/agents/react-reviewer.md` | `:163-184` 옛 사본 · `:186-193` 적용 메모 「임계 2 … REJECT」 · `:280` `verdict: APPROVE \| REJECT` · `:314-318` unverified 칸 · `:323-327` 최종 판정 「`미검증 수` 가 2 이상이면」 | 옛 판 · 판정값에 보류가 없다 | SK-01 ~ SK-03 · SK-05 |
| `react-kit/skills/react-audit/SKILL.md` | `:268` `**판정**: **<APPROVE\|REJECT>**` · `:278-280` 미검증 칸 · `:309` MUST 「2 건 이상이면 … REJECT」 | 옛 한 장부 · 보류 없음 | SK-06 · SK-07 |
| `api-kit/agents/api-reviewer.md` | `:53-66` 줄인 사본(조항 4 는 킷 문장으로 바꿈) · `:106-109` 「프로토콜 2항」 · `:111-126` 판정 · 집계 | 옛 판 · 원문과 글자가 다름 | SK-01 ~ SK-03 · SK-05 |
| `api-kit/skills/*/SKILL.md` 다섯 | `grep -rlF api-reviewer api-kit/skills` 0 파일 | 소비면 없음 | SK-06 |
| `backend-kit/agents/backend-reviewer.md` | `:66-68` 최종 판정에 BLOCKED 없음 · `:70-108` 2026-08-13 사본(인용 표식) · `:83` 「어휘만 이 킷 도메인으로 치환한 복제다」 · `:110-120` 낱말 바꾼 4 요건 · `:122-129` 「조항 2」 · 「조항 3」 | 새 조항 1 표 · 조항 2 없음 | SK-01 ~ SK-03 · SK-05 |
| `backend-kit/skills/backend-audit/SKILL.md` | `:109` 「세 가지다」(목록은 넷) · `:111` · `:113` APPROVE 「전 카테고리 PASS」 · `:114` · `:116` BLOCKED | ENV 항목이 있으면 판정 빈틈 | SK-06 · SK-07 |
| `rust-kit/agents/rust-reviewer.md` | `:44-52` 재동기화 메모(`:51` 「옮기지 않았다」) · `:54-76` 2026-08-13 사본 · `:78-88` 낱말 바꾼 4 요건 · `:166-171` 판정(`:168` 「전 row PASS」) | 새 조항 1 표 · 조항 2 없음 · 판정 빈틈 | SK-01 ~ SK-03 · SK-05 |
| `rust-kit/skills/rust-audit/SKILL.md` | `:123` · `:125` APPROVE 「전 row PASS」 · `:128` BLOCKED | 판정 빈틈 | SK-06 · SK-07 |
| `infra-kit/agents/infra-reviewer.md` | `:72-74` 「(2026-08-13 개정 · 4 분기 + 카운터 분리)의 복제본」 · `:76-98` 사본(`:89-90` 「같은 항목이 2 회 연속 … 기준 결함」 으로 낱말 바꿈) · `:100-109` 낱말 바꾼 4 요건 · `:111` 「조항 2」 · `:131-139` 우선순위 | 새 조항 1 표 · 조항 2 없음 | SK-01 ~ SK-03 · SK-05 |
| `infra-kit/skills/infra-audit/SKILL.md` | `:94-108` 두 카운터 · 우선순위 6 단계 | 이미 새 판과 같다 — 고치지 않는다 | SK-06 · SK-07 |
| `.claude/skills/infra-kaizen/SKILL.md` | `:30-35` Gotcha 8 표 — `:35` 「5 조항 … `infra-reviewer.md` §9 에 **문구 변형 없이** 복제」 | 4 요건 · 기계 검사를 모른다(F1H-48) | SK-08 |
| `.github/workflows/ci.yml` | `:16-101` `validate` 묶음 — 사본 대조 단계 없음 | 사본이 원문과 어긋나도 잡는 곳이 없다 | AR-02 |
| `harness/docs/guides/qa-evaluation-guide.md` (읽기만) | `:1231-1299` 원문 · `:1275` · `:1282` 번호 3 둘 · `:889-897` 4 요건 | 원문 번호 겹침은 넘김 | SK-01 |
| `howto-kit/agents/howto-reviewer.md` (읽기만) | `:30` · `:79-81` `[미검증:ENV]` · `[미검증:INVALID]` 를 쓰나 사본은 없다 | 여덟째 reviewer — 이번 결정(일곱)의 범위 밖 | ER-01 (제외 목록) |
| `harness/docs/guides/skill-design-guide.md` (읽기만) | `:298-308` 스킬이 지켜야 할 5 조항 3 항 · `:308` 「2 건 기준은 양쪽이 세는 대상이 다르다」 | 만드는 쪽 「부분 완료」 규칙의 정본 | 판단 기록 8 |
| `infra-kit/skills/infra-test/SKILL.md` · `react-kit/references/render-evidence-protocol.md` · `flutter-toolkit/references/visual-evidence-protocol.md` · `onboarding-kit/skills/setup-guide/evals/evals.json` (읽기만) | `:449` · `:205` · `:141-142` · `:87` 「2 건 이상이면 부분 완료」 | 만드는 쪽 규칙이라 맞다. `render-evidence-protocol.md:205` 의 「정본 조항 3」 표기만 원문 번호 겹침과 함께 넘김 | 고치지 않음 |
| `flutter-toolkit/skills/flutter-audit/SKILL.md` (읽기만) | `:33` 「5 조항은 정본을 **문구 변형 없이** 복제」 · `:40` 「3 분기」 · `:41` 「임계값은 2 다」 | 평가 쪽 옛 사본 — reviewer 일곱 밖 | 넘김 |

구현 후보는 하나다(사본 교체 + 판정 글 맞춤 + 기계 대조). 사본을 원문 링크로만 두는 안은 킷이 따로 설치돼 원문을 못 읽으므로 뺐다(과제 지시).

### 판정 대응표 (SK-05 · SK-07 이 대조하는 기대값)

네 경우는 모두 FAIL 0 이다. design 은 L3 커버리지 10/10 · 결정 전파 FAIL 0, planning 은 FAIL 축이 `READY_FOR_SPRINT_CONTRACT` 라고 둔다.
`invalid_evidence` 는 `[미검증:INVALID]` 와 접미 없는 `[미검증]` 의 수, `env_gaps` 는 4 요건을 채운 `[미검증:ENV]` 의 수, 비율은 `(판정 단위 수 − env_gaps) / 판정 단위 수` 다.

| 경우 | 입력 |
| ---- | ---- |
| S1 | `invalid_evidence` 2 · `env_gaps` 0 |
| S2 | `invalid_evidence` 0 · 판정 단위 20 중 `env_gaps` 2 → 비율 0.90 (planning 은 12 중 2 → 0.83) |
| S3 | `invalid_evidence` 0 · 판정 단위 20 중 `env_gaps` 9 → 비율 0.55 (planning 은 12 중 5 → 0.58) |
| S4 | `invalid_evidence` 1 · `env_gaps` 0 |

| 파일 (만드는 쪽 · 받아 쓰는 쪽) | S1 | S2 | S3 | S4 |
| ------------------------------- | -- | -- | -- | -- |
| design-reviewer · design-audit | REJECT | APPROVE | BLOCKED | APPROVE (경고 한 줄) |
| planning-reviewer · plan-audit | NEEDS_VERIFICATION | READY_FOR_SPRINT_CONTRACT | BLOCKED | READY_FOR_SPRINT_CONTRACT (경고 한 줄) |
| react-reviewer · react-audit | REJECT | APPROVE | BLOCKED | APPROVE (경고 한 줄) |
| api-reviewer (받아 쓰는 쪽 없음) | REJECT | APPROVE | BLOCKED | CONDITIONAL APPROVE |
| backend-reviewer · backend-audit | REJECT | APPROVE | BLOCKED | CONDITIONAL APPROVE |
| rust-reviewer · rust-audit | REJECT | APPROVE | BLOCKED | CONDITIONAL APPROVE |
| infra-reviewer · infra-audit | REJECT | APPROVE | BLOCKED | CONDITIONAL APPROVE |

칸 수는 명령으로 센다(`m SK-05` 의 `cases_total=28` · `m SK-07` 의 `cases_total=24`). 같은 표가 `m.sh` 의 `_matrix` 에 있다 — 표를 고치면 둘을 함께 고친다.

### 개선안 (구현 단계가 할 일, 조건 순서)

1. reviewer 일곱: 옛 사본을 원문 두 덩어리(조항 · 4 요건)로 바꾸고 출처 한 줄을 붙인다. 조항 덩어리 앞뒤에 MD029 끄기 · 켜기 주석 쌍. 킷 고유 적용 글(예시 명령 · 도메인 매핑)은 사본 밖에 남긴다(SK-01 · SK-02)
2. 사본 밖 글: 「조항 2」 · 「3 분기」 · 한 장부 임계 문장을 새 판 낱말로 바꾸고, 판정 목록에 보류(`BLOCKED`, 비율 0.60)와 두 카운터를 넣는다. planning `reason:` 에 N/A 칸(SK-03 · SK-04 · SK-05)
3. 받아 쓰는 쪽: design-audit · plan-audit · react-audit · backend-audit · rust-audit · design 시험 한 줄을 같은 규칙으로(SK-06 · SK-07)
4. `.claude/skills/infra-kaizen/SKILL.md` Gotcha 8 표의 원문 행(SK-08)
5. `scripts/check-reviewer-protocol-copies.py` 와 CI 한 단계(ER-01 · ER-02 · AR-02 · RE-01 · RE-02 · DG-04)
6. 구현 전 `tone-kit:tone-guide` 1 단계를 불러 규칙을 싣고, 완료 전 5 단계 대조를 돌린다(SK-09 가 번역투 여섯 패턴을 잰다)

## 범위 경계

- 시작 커밋: `f81568d8fbf58382172281388ec5d7756f9f46b2` (워크트리 `ak-c4b` 를 `origin/main` 에서 만든 판, `git -C <W> log -1` 로 확인). 끝 판은 가지 `chore/ak-c4b` 의 끝이고,
  가지를 합친 뒤 지웠으면 커밋 메시지에 `chore/ak-c4b` 가 든 병합 커밋의 둘째 부모다(`m.sh` 의 `end_ref`). 풀리지 않으면 `END_UNRESOLVED` 를 찍고 멈춘다 — `HEAD` 로 재지 않는다
- 고치는 파일은 아래 블록의 16 경로이고 새 파일은 그중 `scripts/check-reviewer-protocol-copies.py` 하나다. `.harness/` 쪽은 이 계약 · 개정 파일 · QA 피드백이다(AR-01 은 `.harness/` 를 경로 목록이 아니라 봉인으로 잰다)

```text
# sprint-scope
.claude/skills/infra-kaizen/SKILL.md
.github/workflows/ci.yml
api-kit/agents/api-reviewer.md
backend-kit/agents/backend-reviewer.md
backend-kit/skills/backend-audit/SKILL.md
design-kit/agents/design-reviewer.md
design-kit/evals/evals.json
design-kit/skills/design-audit/SKILL.md
infra-kit/agents/infra-reviewer.md
planning-kit/agents/planning-reviewer.md
planning-kit/skills/plan-audit/SKILL.md
react-kit/agents/react-reviewer.md
react-kit/skills/react-audit/SKILL.md
rust-kit/agents/rust-reviewer.md
rust-kit/skills/rust-audit/SKILL.md
scripts/check-reviewer-protocol-copies.py
.harness/
```

- 커밋 규칙: 봉인 커밋은 계약 파일 하나만 싣는다(Step 6.7). 구현 커밋은 `git add <경로> && git commit -o <경로>` 로 경로를 한정하고, 한 커밋에 킷 하나다 —
  킷 폴더(`*-kit/`)를 건드린 커밋에는 다른 킷도 킷 밖 경로도 없고, 킷 밖 세 경로(`.claude/skills/infra-kaizen/SKILL.md` · `.github/workflows/ci.yml` · `scripts/check-reviewer-protocol-copies.py`)는
  킷 경로가 없는 커밋에 싣는다. 구현 커밋에 `.harness/` 를 섞지 않는다. `git add -A` · `git stash` · push · 가지 바꾸기는 하지 않는다
- 버전 올림 · `marketplace.json` · 킷 `plugin.json` 은 건드리지 않는다 — 릴리스는 부모가 PR 을 합친 뒤 한다(핸드오프 재개 지시 5 번)
- 넘김 (고치지 않고 받을 곳을 적는다):
  - 원문 `harness/docs/guides/qa-evaluation-guide.md` 의 조항 번호 겹침(3 이 둘, `:1275` · `:1282`)과 머리말 「5 조항」 · 「현재 drift (2026-07-27 실측)」 문단 — 원문은 이 계약 범위 밖. 다음 사이클 Phase 3(C2 묶음).
    원문이 번호를 고치면 일곱 사본도 같이 바뀌어야 하며, 그때는 새 검사가 그것을 잡는다. backend-audit · rust-audit · infra-audit 의 「정본 조항 3」 표기(원문을 직접 가리킴)와
    `react-kit/references/render-evidence-protocol.md:205` 의 「정본 조항 3」(만드는 쪽 문서가 원문을 가리킴)도 그때 함께 본다
  - `flutter-toolkit/skills/flutter-audit/SKILL.md:32-49` 의 옛 다섯 조항 사본 — flutter-toolkit 에는 `agents/*-reviewer.md` 가 없어 사용자가 고른 일곱 밖이다. 다음 사이클 Phase 5(flutter-kaizen).
    만드는 쪽 「2 건 이상이면 부분 완료」 넷(판단 기록 8)은 정본 `skill-design-guide.md:308` 과 맞아 넘김도 아니고 고칠 것이 없다
  - `harness/agents/qa-evaluator.md` — 범위 밖(과제 지시)
  - `howto-kit/agents/howto-reviewer.md` — 원문은 `*-kit/agents/*-reviewer.md` 모두가 사본을 들라고 하지만(`qa-evaluation-guide.md:1233`) 사용자 결정은 일곱이다. 새 검사는 이 파일을 이유와 함께 제외 목록에 둔다. 다음 사이클 Phase 17
  - design-reviewer `:185` 의 「미검증 0 건 · L3 10 개 미만 → CONDITIONAL APPROVE (L3 부분 커버리지)」 가 원문 「CONDITIONAL APPROVE 는 1 건 + FAIL 0 에서만」 과 어긋나는 것 — 옛 판부터 있던 design-kit 의 L3 규칙이고 미검증 규칙이 아니다. 다음 사이클 Phase 6
  - 옛 문턱을 설명하는 문서 사이트 쪽 세 쪽 `docs/harness/contract-design-guide.html` · `docs/harness/qa-evaluation-guide.html` · `docs/harness/skill-design-guide.html` — `docs/` HTML 은 범위 밖(과제 지시). 원문 쪽 문서라 C2 묶음 · 문서 사이트 재생성 때
  - `harness/evals/gate-exit-codes.md` 소비처 표에 새 스크립트 행 — harness 폴더 파일이고 표가 이미 모든 사용처를 담지 않는다(`scripts/check-stale-values.py` 도 없다). 다음 사이클 Phase 4
  - design · backend · planning · react 카이젠 스킬(`.claude/skills/design-kaizen/SKILL.md:24` · `backend-kaizen/SKILL.md:37` · `planning-kaizen/SKILL.md:21` · `react-kaizen/SKILL.md:122`)의 「5 조항을 문구 변형 없이 복제」 문장 — 사본이 원문과 글자까지 같아지면 사실이 되는 문장이라 고치지 않는다
- 함께 도는 다른 묶음: `chore/ak-c4c` 가 `rust-kit/skills/rust-audit/SKILL.md` 의 다른 줄(`:20` · `:27` · `:100` · `:103` · `:113`)을, `chore/ak-c1-harness-scripts` 가 `.github/workflows/ci.yml` 에 다른 단계를 더한다.
  이 계약의 수정 자리(rust-audit `:123-128` · ci.yml `Stale value check` 근처)와 겹치지 않게 하고, 합칠 때 생기는 글자 충돌은 부모가 푼다
- 판정 한계: 판정 대응표(SK-05 · SK-07)는 결정론 측정이 없다 — QA 가 판정 글을 읽어 칸을 채우고, `m SK-05` · `m SK-07` 의 판정값 글자 존재(`labels_ok`)는 보조다.
  태그는 `[exact, enumerated]` 로 둔다. 칸 값이 판정 이름 글자 그대로 맞아야 하는 조건이고(`[exact]` 의 뜻은 「이름/값 문자 그대로 매칭」 이지 재는 수단이 아니다),
  양면 조건은 `[exact, enumerated]` 여야 한다(`harness/references/contract-schema.md` §Counterpart 조건). 교차 진단이 태그와 재는 방식이 어긋난다고 짚어 이 줄로 답한다
- 커버리지 해소: SK-01 · SK-03 · SK-05 · AP-03 · AP-04 — 일곱 reviewer 는 `m.sh` 의 `REV` 목록 글자이고 sprint-scope 블록의 일곱 줄과 같다(AR-01 `scope_block` 이 블록과 `SCOPE` 를 대조한다).
  SK-01 의 원문 경로 · `v5.1` · 「계약」 은 `copy.py` 의 `GUIDE` 상수와 `prov` 판정 글자이고, `chore/ak-c4b` 는 `m.sh` 의 `BRANCH` 기본값이다
- 커버리지 해소: SK-02 — 세 파일과 세 글은 `m.sh` SK-02 갈래의 `for p in …` 글자 그대로다
- 커버리지 해소: SK-03 · SK-06 — `0.60` · `BLOCKED` · 옛 임계 · 「조항 2」 · 「조항 3」 · 「3 분기」 판정은 `scan.py` 의 `THR` · `NUM` · `NUM3` · `THREE` 와 `gate` 판정 글자다.
  SK-06 의 받아 쓰는 쪽 일곱은 `m.sh` 의 `CONS` 여섯과 SK-06 갈래의 `infra-kit/skills/infra-audit/SKILL.md` 글자이고, SK-07 판정표 여섯은 `_matrix audits` 글자다
- 커버리지 해소: DG-02 — 마크다운 열셋은 `m.sh` 의 `MDF` 글자이고, `design-kit/evals/evals.json` 은 DG-02 갈래의 `json.tool` 줄 글자다
- 커버리지 해소: DG-05 — 킷 일곱은 `m.sh` 의 `KITS`, 스크립트 여섯(`validate-plugin.py` · `sync-docs.py` · `sync-evals.py` · `run-evals.py` · `check-stale-values.py` · `check-docs-links.py`)과 새 검사는 `_checks` 글자다

## 회귀 게이트 — 측정 공통 정의와 봉인 전 실측

모든 조건은 아래 세 블록(`copy.py` · `scan.py` · `m.sh`)을 쓴다. 이 계약에서 떼어 한 폴더에 두고 **bash** 로 `m.sh` 를 읽은 뒤 `m <조건 ID>` 를 부른다.
`m.sh` 는 시작 커밋과 끝 판을 임시 폴더에 풀어 재므로 작업 폴더를 바꾸지 않는다. 판정은 출력 값으로 한다(`m` 의 종료 코드는 판정하지 않는다).

```bash
# 떼어 내기 — 첫 줄이 `# file: <이름>` 인 bash · python 블록만 그 이름으로 저장한다
CF=/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak-c4b/.harness/sprint-contract-after-0924-reviewer-unverified.md
K=$(mktemp -d)
awk -v K="$K" '/^```(bash|python)$/{b=1; f=""; next} b && /^```$/{b=0; f=""; next}
  b && f=="" && /^# file: /{f=K "/" $(3); print > f; next} b && f!=""{print > f}' "$CF"
ls "$K"   # copy.py  m.sh  scan.py
K="$K" bash -c '. "$K/m.sh" && m SK-01'   # 조건 하나를 잰다
```

준비 단계는 `## 회귀 게이트` 끝의 실측 표 1 행에 적었다. `ML` 이 없으면 DG-02 가 `ML_MISSING` 을 찍는다 — 빈 임시 폴더에서
`npm install --no-save markdownlint-cli2@0.23.2` 뒤 `ML=<그 폴더>/node_modules/.bin/markdownlint-cli2` 로 넘긴다(편집기 확장이 싣는 판이고, 줄 길이 규칙 MD013 을 끈 설정은
`m.sh` 가 임시 폴더에 만든다). 워크트리를 지운 뒤 재면 `W=<레포 경로>` 로 넘긴다. `TMPDIR` 은 다른 세션과 겹치지 않게 스크래치 폴더로 둔다.

```python
# file: copy.py
"""정본 두 덩어리(미검증 조항 · 남용 방지 4 요건)를 킷 reviewer 사본과 대조한다.

쓰기: python3 copy.py <판 폴더> blocks          — 정본 두 덩어리의 줄 수와 첫 줄을 낸다
      python3 copy.py <판 폴더> check <파일>...  — 파일마다 한 줄: <파일> a=<횟수> b=<횟수> prov=<줄 수>
      python3 copy.py <판 폴더> rest <파일>       — 두 덩어리를 뺀 나머지 줄을 `줄번호:글` 로 낸다

정규화: 줄 앞의 공백과 `>` 를 떼고 끝 공백을 뗀다. 빈 줄은 버린다.
a · b 는 정규화한 파일 줄에서 정본 덩어리가 끊김 없이 나오는 횟수다.
prov 는 덩어리 밖에서 `qa-evaluation-guide.md` · `v5.1` · `계약` 이 한 줄에 함께 든 줄 수다.
정본을 못 찾으면 `CANON_MISSING <덩어리>` 를 내고 종료 코드 2.
"""
import re
import sys

GUIDE = "harness/docs/guides/qa-evaluation-guide.md"
SEC = "## Canonical Unverified-Evidence Protocol (각 kit reviewer 복제용 정본)"


def norm(s):
    return re.sub(r"^[\s>]*", "", s).rstrip()


def canon(root):
    L = open(f"{root}/{GUIDE}", encoding="utf-8").read().split("\n")
    try:
        s = L.index(SEC)
    except ValueError:
        return None, None
    a = []
    on = False
    for x in L[s + 1:]:
        if x.startswith("## "):
            break
        if not on and re.match(r"^1\. \*\*마커는", x):
            on = True
        if on:
            if x.startswith("> "):
                break
            a.append(x)
    b = []
    on = False
    for i, x in enumerate(L):
        if x.startswith("#### `UNVERIFIED_ENV` 남용 방지 4 요건"):
            on = True
            continue
        if on:
            if x.startswith("> ") or x.startswith("#"):
                break
            b.append(x)
    A = [norm(x) for x in a if norm(x)]
    B = [norm(x) for x in b if norm(x)]
    return (A or None), (B or None)


def spans(N, blk):
    out = []
    k = len(blk)
    for i in range(len(N) - k + 1):
        if [t for _, t in N[i:i + k]] == blk:
            out.append((N[i][0], N[i + k - 1][0]))
    return out


def lines(path):
    raw = open(path, encoding="utf-8").read().split("\n")
    return raw, [(i, norm(x)) for i, x in enumerate(raw, 1) if norm(x)]


def main(argv):
    root, mode = argv[1], argv[2]
    A, B = canon(root)
    if A is None or B is None:
        print("CANON_MISSING " + ("a" if A is None else "b"))
        return 2
    if mode == "blocks":
        print(f"a_lines={len(A)} a_first={A[0][:24]} a_last={A[-1][:24]}")
        print(f"b_lines={len(B)} b_first={B[0][:24]} b_last={B[-1][:24]}")
        return 0
    if mode == "check":
        for f in argv[3:]:
            raw, N = lines(f"{root}/{f}")
            sa, sb = spans(N, A), spans(N, B)
            inside = set()
            for x, y in sa + sb:
                inside.update(range(x, y + 1))
            prov = sum(1 for i, x in enumerate(raw, 1)
                       if i not in inside and "qa-evaluation-guide.md" in x and "v5.1" in x and "계약" in x)
            print(f"{f} a={len(sa)} b={len(sb)} prov={prov}")
        return 0
    if mode == "rest":
        raw, N = lines(f"{root}/{argv[3]}")
        inside = set()
        for x, y in spans(N, A) + spans(N, B):
            inside.update(range(x, y + 1))
        for i, x in enumerate(raw, 1):
            if i not in inside:
                print(f"{i}:{x}")
        return 0
    print("UNKNOWN_MODE")
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
```

```python
# file: scan.py
"""사본 밖 글에서 옛 규칙 흔적과 새 판정 규칙을 센다.

쓰기: python3 scan.py <판 폴더> <copy.py 경로> <파일>...
파일마다 한 줄: <파일> old_thr=<n> num_ref=<n> num3_ref=<n> three_way=<n> gate=<n> env=<n> invalid=<n>
  old_thr   — 임계 2 를 말하는 줄 가운데 INVALID · invalid_evidence 가 없는 줄 (「」 로 감싼 조항 첫머리 인용은 빼고 잰다)
  num_ref   — 사본 조항을 번호 2 로 가리키는 줄 (`조항 2` · `조항 2·3` · `프로토콜 2항`)
  num3_ref  — 조항을 번호 3 으로 가리키는 줄 (`조항 3` · `정본 조항 3`). 사본 안에 3 이 둘이라 어느 쪽인지 알 수 없다
  three_way — `3 분기` 가 든 줄
  gate      — `0.60` 과 `BLOCKED` 가 한 줄에 함께 든 줄
  env       — `env_gaps` 가 든 줄
  invalid   — `UNVERIFIED_INVALID_EVIDENCE` · `invalid_evidence` · `[미검증:INVALID]` 가운데 하나가 든 줄
줄마다 걸린 것은 `HIT <파일>:<줄> <종류>` 로 먼저 낸다. 사본 두 덩어리 줄은 세지 않는다.
.json 파일은 사본이 없으므로 파일 전체를 잰다.
"""
import re
import subprocess
import sys

THR = re.compile(r"2 ?건 ?이상|2 건이면|2 이상이면|임계 ?2(?![0-9])|임계값은 2|임계값 2(?![0-9])"
                 r"|미검증[^|]*(≥|>=) ?2(?![0-9])")
INV = re.compile(r"INVALID|invalid_evidence")
NUM = re.compile(r"조항 ?2(?![0-9])|조항 2·3|프로토콜 2 ?항")
NUM3 = re.compile(r"조항 ?3(?![0-9])")
THREE = re.compile(r"3 분기")


def rest(root, cp, f):
    if f.endswith(".json"):
        raw = open(f"{root}/{f}", encoding="utf-8").read().split("\n")
        return [(i, x) for i, x in enumerate(raw, 1)]
    out = subprocess.run(["python3", cp, root, "rest", f], capture_output=True, text=True)
    if out.returncode != 0:
        raise SystemExit(f"REST_FAIL {f} {out.stdout.strip()} {out.stderr.strip()}")
    res = []
    for line in out.stdout.split("\n"):
        if ":" in line:
            n, t = line.split(":", 1)
            res.append((int(n), t))
    return res


def main(argv):
    root, cp, files = argv[1], argv[2], argv[3:]
    summary = []
    for f in files:
        c = dict(old_thr=0, num_ref=0, num3_ref=0, three_way=0, gate=0, env=0, invalid=0)
        for n, t in rest(root, cp, f):
            q = re.sub(r"「[^」]*」", "", t)
            if THR.search(q) and not INV.search(q):
                c["old_thr"] += 1; print(f"HIT {f}:{n} old_thr")
            if NUM.search(t):
                c["num_ref"] += 1; print(f"HIT {f}:{n} num_ref")
            if NUM3.search(t):
                c["num3_ref"] += 1; print(f"HIT {f}:{n} num3_ref")
            if THREE.search(t):
                c["three_way"] += 1; print(f"HIT {f}:{n} three_way")
            if "0.60" in t and "BLOCKED" in t:
                c["gate"] += 1
            if "env_gaps" in t:
                c["env"] += 1
            if re.search(r"UNVERIFIED_INVALID_EVIDENCE|invalid_evidence|\[미검증:INVALID\]", t):
                c["invalid"] += 1
        summary.append(f + " " + " ".join(f"{k}={v}" for k, v in c.items()))
    print("\n".join(summary))


if __name__ == "__main__":
    main(sys.argv)
```

```bash
# file: m.sh
# bash 로 읽는다: K=<측정 파일 폴더> bash -c '. "$K/m.sh" && m <조건 ID>'
: "${K:?K 에 측정 파일 폴더를 넣는다}"
W=${W:-/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak-c4b}
BASE=${BASE:-f81568d8fbf58382172281388ec5d7756f9f46b2}
BRANCH=${BRANCH:-chore/ak-c4b}
CF_REL=.harness/sprint-contract-after-0924-reviewer-unverified.md
ML=${ML:-/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/bda55d45-296c-491f-89ba-b52042d58e72/scratchpad/c4c/mdlint/node_modules/.bin/markdownlint-cli2}
SCRIPT=scripts/check-reviewer-protocol-copies.py
REV='api-kit/agents/api-reviewer.md
backend-kit/agents/backend-reviewer.md
design-kit/agents/design-reviewer.md
infra-kit/agents/infra-reviewer.md
planning-kit/agents/planning-reviewer.md
react-kit/agents/react-reviewer.md
rust-kit/agents/rust-reviewer.md'
CONS='backend-kit/skills/backend-audit/SKILL.md
design-kit/evals/evals.json
design-kit/skills/design-audit/SKILL.md
planning-kit/skills/plan-audit/SKILL.md
react-kit/skills/react-audit/SKILL.md
rust-kit/skills/rust-audit/SKILL.md'
MDF="$REV
backend-kit/skills/backend-audit/SKILL.md
design-kit/skills/design-audit/SKILL.md
planning-kit/skills/plan-audit/SKILL.md
react-kit/skills/react-audit/SKILL.md
rust-kit/skills/rust-audit/SKILL.md
.claude/skills/infra-kaizen/SKILL.md"
SCOPE=".claude/skills/infra-kaizen/SKILL.md
.github/workflows/ci.yml
$REV
$CONS
$SCRIPT"
SCOPE=$(printf '%s\n' "$SCOPE" | LC_ALL=C sort)
KITS='api-kit backend-kit design-kit infra-kit planning-kit react-kit rust-kit'
G1='(을|를) ?(처리|관리)(합니다|한다)|에 대해서?|하도록 (합니다|한다)|에 의(해|하여)|되어 있(는 경우|을 때)|(표시|적용|호출|생성|반환)(됩니다|된다)'

sha256_16() {
  if   command -v sha256sum >/dev/null 2>&1; then sha256sum
  elif command -v shasum    >/dev/null 2>&1; then shasum -a 256
  else python3 -c 'import hashlib,sys; print(hashlib.sha256(sys.stdin.buffer.read()).hexdigest())'
  fi | cut -c1-16
}
contract_digest() { grep -E '^- \[[ x]\] [A-Z]{2,}-[0-9]{2}' "$1" | sed -E 's/^- \[[ x]\]/- [ ]/' | sha256_16; }
fm_get() {
  awk -v k="$2" -v q="\"'" '
    NR==1 && /^---[[:space:]]*$/ { fm=1; next }
    fm && /^---[[:space:]]*$/    { exit }
    fm && index($0, k ":") == 1 {
      v = substr($0, length(k) + 2)
      sub(/^[[:space:]]+/, "", v); sub(/[[:space:]]+$/, "", v)
      c = substr(v, 1, 1)
      if (length(v) > 1 && index(q, c) > 0 && substr(v, length(v), 1) == c)
        v = substr(v, 2, length(v) - 2)
      print v; exit
    }' "$1"
}
verify_seal() {
  rec=$(fm_get "$1" conditions_digest); rec=${rec#sha256:}
  if [ -z "$rec" ]; then echo "SEAL_ABSENT $1"; return 0; fi
  act=$(contract_digest "$1")
  if [ "$rec" = "$act" ]; then echo "SEAL_OK $1"; else echo "SEAL_BROKEN $1 recorded=$rec actual=$act"; fi
}
end_ref() {
  if [ -n "${END_OVERRIDE:-}" ]; then git -C "$W" rev-parse --verify -q "${END_OVERRIDE}^{commit}"; return; fi
  git -C "$W" rev-parse --verify -q "refs/heads/${BRANCH}^{commit}" && return 0
  _m=$(git -C "$W" log --all --merges --format=%H --grep="$BRANCH" -1)
  if [ -n "$_m" ]; then git -C "$W" rev-parse "${_m}^2"; return 0; fi
  return 1
}

END=$(end_ref) || { echo "END_UNRESOLVED $BRANCH"; return 2 2>/dev/null || exit 2; }
T=$(mktemp -d "${TMPDIR:-/tmp}/c4b.XXXXXX")
trap 'rm -rf "$T"' EXIT
mkdir -p "$T/base" "$T/end"
printf '{ "config": { "MD013": false } }\n' > "$T/cfg.markdownlint-cli2.jsonc"
git -C "$W" archive "$BASE" | tar -x -C "$T/base" && git -C "$W" archive "$END" | tar -x -C "$T/end" \
  || { echo SNAPSHOT_FAIL; return 2 2>/dev/null || exit 2; }
for _f in $REV $CONS harness/docs/guides/qa-evaluation-guide.md; do
  [ -s "$T/base/$_f" ] && [ -s "$T/end/$_f" ] || { echo "SNAPSHOT_FAIL $_f"; return 2 2>/dev/null || exit 2; }
done
echo "BASE=$BASE END=$END"

_commits() { git -C "$W" rev-list --first-parent --no-merges "$BASE..$END"; }
_files_of() { git -C "$W" diff-tree --no-commit-id --name-only -r "$1"; }
_impl() { git -C "$W" log --first-parent --no-merges --format= --name-only "$BASE..$END" -- . ':(exclude).harness' | grep . | LC_ALL=C sort -u; }
_scope() {  # _scope <계약> — `## 범위 경계` 안 첫 줄이 `# sprint-scope` 인 text 블록의 줄
  [ -f "$1" ] || return 0
  awk '/^## /{s=($(0) ~ /^## 범위 경계/)} s && /^```text$/{b=1; first=1; next} b && /^```$/{b=0; take=0; next}
       b && first {first=0; take=($(0)=="# sprint-scope"); next} b && take {print}' "$1" | grep . | LC_ALL=C sort
}
_ml() {  # _ml <판 폴더> — 파일 · 규칙마다 경고 수
  (cd "$1" && "$ML" --config "$T/cfg.markdownlint-cli2.jsonc" $MDF 2>&1) \
    | grep -E '^[^ ]+:[0-9]+(:[0-9]+)? error MD' | awk '{split($1,a,":"); split($3,r,"/"); print a[1], r[1]}' | LC_ALL=C sort | uniq -c | awk '{print $2, $3, $1}'
}
_run() {  # _run <판 폴더> [cwd] — 새 검사 스크립트를 돌려 출력 · 종료 코드 · stderr 바이트를 남긴다
  _cwd=${2:-$1}
  (cd "$_cwd" && python3 "$1/$SCRIPT" >"$T/out" 2>"$T/err"); echo $? > "$T/rc"
}
_st() { grep -cE "^$1 " "$T/out"; }
_checks() {  # _checks <판 폴더>
  (cd "$1" || exit 2
   for k in $KITS; do python3 scripts/validate-plugin.py "$k" >/dev/null 2>&1; printf 'v-%s=%s ' "$k" "$?"; done
   for c in "validate-all:scripts/validate-plugin.py" "sync-docs:scripts/sync-docs.py --check-only" \
            "sync-evals:scripts/sync-evals.py --check-only" "run-evals:scripts/run-evals.py" \
            "stale-values:scripts/check-stale-values.py" "docs-links:scripts/check-docs-links.py" "copies:$SCRIPT"; do
     n=${c%%:*}; a=${c#*:}
     if [ "$n" = copies ] && [ ! -f "$SCRIPT" ]; then printf 'copies=absent '; continue; fi
     # shellcheck disable=SC2086
     python3 $a >/dev/null 2>&1; printf '%s=%s ' "$n" "$?"
   done; echo)
}
_matrix() {  # _matrix <reviewers|audits> — 기대 판정표
  if [ "$1" = reviewers ]; then
    printf '%s\n' "design-kit/agents/design-reviewer.md REJECT APPROVE BLOCKED APPROVE" \
      "planning-kit/agents/planning-reviewer.md NEEDS_VERIFICATION READY_FOR_SPRINT_CONTRACT BLOCKED READY_FOR_SPRINT_CONTRACT" \
      "react-kit/agents/react-reviewer.md REJECT APPROVE BLOCKED APPROVE" \
      "api-kit/agents/api-reviewer.md REJECT APPROVE BLOCKED CONDITIONAL_APPROVE" \
      "backend-kit/agents/backend-reviewer.md REJECT APPROVE BLOCKED CONDITIONAL_APPROVE" \
      "rust-kit/agents/rust-reviewer.md REJECT APPROVE BLOCKED CONDITIONAL_APPROVE" \
      "infra-kit/agents/infra-reviewer.md REJECT APPROVE BLOCKED CONDITIONAL_APPROVE"
  else
    printf '%s\n' "design-kit/skills/design-audit/SKILL.md REJECT APPROVE BLOCKED APPROVE" \
      "planning-kit/skills/plan-audit/SKILL.md NEEDS_VERIFICATION READY_FOR_SPRINT_CONTRACT BLOCKED READY_FOR_SPRINT_CONTRACT" \
      "react-kit/skills/react-audit/SKILL.md REJECT APPROVE BLOCKED APPROVE" \
      "backend-kit/skills/backend-audit/SKILL.md REJECT APPROVE BLOCKED CONDITIONAL_APPROVE" \
      "rust-kit/skills/rust-audit/SKILL.md REJECT APPROVE BLOCKED CONDITIONAL_APPROVE" \
      "infra-kit/skills/infra-audit/SKILL.md REJECT APPROVE BLOCKED CONDITIONAL_APPROVE"
  fi
}
_labels() {  # _labels <reviewers|audits> — 파일마다 기대 판정값 글자가 사본 밖에 모두 있는가
  ok=0; n=0
  while read -r f s1 s2 s3 s4; do
    n=$((n+1)); miss=""
    rest=$(python3 "$K/copy.py" "$T/end" rest "$f" | sed 's/^[0-9]*://')
    for l in $(printf '%s\n' "$s1" "$s2" "$s3" "$s4" | LC_ALL=C sort -u); do
      w=$(printf '%s' "$l" | tr '_' ' '); [ "$l" = READY_FOR_SPRINT_CONTRACT ] && w=$l; [ "$l" = NEEDS_VERIFICATION ] && w=$l
      printf '%s\n' "$rest" | grep -qF "$w" || miss="$miss $l"
    done
    [ -z "$miss" ] && ok=$((ok+1)) || echo "LABEL_MISSING $f$miss"
  done < <(_matrix "$1")
  echo "labels_ok=$ok/$n"
}

m() {
  case "$1" in
  SK-01)
    python3 "$K/copy.py" "$T/end" blocks | tr '\n' ' '; echo
    python3 "$K/copy.py" "$T/end" check $REV > "$T/ck"; cat "$T/ck"
    python3 "$K/copy.py" "$T/base" check $REV > "$T/ckb"
    g=$(python3 "$K/copy.py" "$T/end" check harness/docs/guides/qa-evaluation-guide.md | awk '{print $2, $3}')
    echo "SK-01 files=$(grep -c . "$T/ck") a1=$(grep -c ' a=1 ' "$T/ck") b1=$(grep -c ' b=1 ' "$T/ck") prov1=$(grep -c ' prov=1$' "$T/ck")" \
      "base_a1=$(grep -c ' a=1 ' "$T/ckb") base_b1=$(grep -c ' b=1 ' "$T/ckb") guide=[$g]"
    ;;
  SK-02)
    o="SK-02"
    for p in "rust-kit/agents/rust-reviewer.md|옮기지 않았다" \
             "backend-kit/agents/backend-reviewer.md|어휘만 이 킷 도메인으로 치환한" \
             "infra-kit/agents/infra-reviewer.md|2026-08-13 개정 · 4 분기 + 카운터 분리)의 복제본"; do
      f=${p%%|*}; s=${p#*|}
      o="$o $(echo "$f" | cut -d/ -f1)=$(grep -cF "$s" "$T/end/$f")/$(grep -cF "$s" "$T/base/$f")"
    done
    echo "$o"
    ;;
  SK-03)
    python3 "$K/scan.py" "$T/end" "$K/copy.py" $REV > "$T/sc"; grep '^HIT' "$T/sc" || true
    python3 "$K/scan.py" "$T/base" "$K/copy.py" $REV > "$T/scb"
    awk '!/^HIT/{for(i=2;i<=NF;i++){split($i,kv,"="); s[kv[1]]+=kv[2]; if (kv[2]>0) p[kv[1]]++}} END{printf "SK-03 old_thr=%d num_ref=%d num3_ref=%d three_way=%d gate_ok=%d env_ok=%d invalid_ok=%d", s["old_thr"], s["num_ref"], s["num3_ref"], s["three_way"], p["gate"], p["env"], p["invalid"]}' "$T/sc"
    awk '!/^HIT/{for(i=2;i<=NF;i++){split($i,kv,"="); s[kv[1]]+=kv[2]; if (kv[2]>0) p[kv[1]]++}} END{printf " base_old_thr=%d base_num_ref=%d base_num3_ref=%d base_three_way=%d base_gate_ok=%d\n", s["old_thr"], s["num_ref"], s["num3_ref"], s["three_way"], p["gate"]}' "$T/scb"
    ;;
  SK-04)
    e=$(grep -E '^reason: ' "$T/end/planning-kit/agents/planning-reviewer.md"); b=$(grep -E '^reason: ' "$T/base/planning-kit/agents/planning-reviewer.md")
    echo "SK-04 reason_lines=$(printf '%s' "$e" | grep -c .) reason_na=$(printf '%s' "$e" | grep -c 'N/A') base_reason_na=$(printf '%s' "$b" | grep -c 'N/A')"
    ;;
  SK-05)
    _matrix reviewers | sed 's/^/EXPECT /'
    echo "SK-05 files=$(_matrix reviewers | grep -c .) scenarios=4 cases_total=$(_matrix reviewers | awk '{n+=NF-1} END{print n}') $(_labels reviewers | tail -1)"
    _labels reviewers | grep '^LABEL_MISSING' || true
    ;;
  SK-06)
    python3 "$K/scan.py" "$T/end" "$K/copy.py" $CONS infra-kit/skills/infra-audit/SKILL.md > "$T/sc"; grep '^HIT' "$T/sc" | grep -v ' num3_ref$' || true
    python3 "$K/scan.py" "$T/base" "$K/copy.py" $CONS > "$T/scb"
    sk=$(grep -v '^HIT' "$T/sc" | grep 'SKILL.md' | grep -vc ' gate=0 ')
    cmp -s "$T/base/infra-kit/skills/infra-audit/SKILL.md" "$T/end/infra-kit/skills/infra-audit/SKILL.md" && ia=same || ia=changed
    api=$(grep -rlF 'api-reviewer' "$T/end/api-kit/skills" | grep -c .)
    awk -v sk="$sk" -v ia="$ia" -v api="$api" '!/^HIT/{for(i=2;i<=NF;i++){split($i,kv,"="); s[kv[1]]+=kv[2]}} END{printf "SK-06 old_thr=%d num_ref=%d three_way=%d skills_with_gate=%s/6 infra_audit=%s api_skills_citing_reviewer=%s", s["old_thr"], s["num_ref"], s["three_way"], sk, ia, api}' "$T/sc"
    awk '!/^HIT/{for(i=2;i<=NF;i++){split($i,kv,"="); s[kv[1]]+=kv[2]}} END{printf " base_old_thr=%d base_num_ref=%d base_three_way=%d\n", s["old_thr"], s["num_ref"], s["three_way"]}' "$T/scb"
    ;;
  SK-07)
    _matrix audits | sed 's/^/EXPECT /'
    echo "SK-07 files=$(_matrix audits | grep -c .) scenarios=4 cases_total=$(_matrix audits | awk '{n+=NF-1} END{print n}') $(_labels audits | tail -1)"
    _labels audits | grep '^LABEL_MISSING' || true
    ;;
  SK-08)
    f=.claude/skills/infra-kaizen/SKILL.md
    r=$(grep -E '^ *\| Canonical Unverified-Evidence Protocol' "$T/end/$f"); rb=$(grep -E '^ *\| Canonical Unverified-Evidence Protocol' "$T/base/$f")
    echo "SK-08 rows=$(printf '%s' "$r" | grep -c .) req4=$(printf '%s' "$r" | grep -c '4 요건') script=$(printf '%s' "$r" | grep -cF "$SCRIPT") base_req4=$(printf '%s' "$rb" | grep -c '4 요건') base_script=$(printf '%s' "$rb" | grep -cF "$SCRIPT")"
    ;;
  SK-09)
    python3 - "$T/end" "$K/copy.py" <<'PY' > "$T/canon"
import importlib.util, sys
spec = importlib.util.spec_from_file_location("c", sys.argv[2]); c = importlib.util.module_from_spec(spec); spec.loader.exec_module(c)
a, b = c.canon(sys.argv[1])
print("\n".join(a + b))
PY
    git -C "$W" diff "$BASE" "$END" -- $MDF | grep -E '^\+' | grep -vE '^\+\+\+ ' | sed 's/^+//' \
      | python3 -c 'import re,sys; C=set(open(sys.argv[1],encoding="utf-8").read().split("\n")); [print(l.rstrip("\n")) for l in sys.stdin if re.sub(r"^[\s>]*","",l).rstrip() not in C]' "$T/canon" > "$T/added"
    hit=$(grep -cE "$G1" "$T/added"); ch=$(grep -cE "$G1" "$T/canon")
    echo "SK-09 added_lines=$(grep -c . "$T/added") g1_hits=$hit canon_g1=$ch"
    grep -nE "$G1" "$T/added" | sed 's/^/G1 /' || true
    ;;
  SC-00)
    echo "SC-00 release_paths=$(git -C "$W" log --first-parent --no-merges --format= --name-only "$BASE..$END" -- .claude-plugin '*/.claude-plugin' scripts/release.sh | grep -c .)"
    ;;
  ER-01)
    _run "$T/end"; eo=$(cat "$T/rc"); eok=$(_st OK); eex=$(grep -cE '^EXCLUDED howto-kit/agents/howto-reviewer\.md .*[^ ]' "$T/out"); eerr=$(wc -c < "$T/err" | tr -d ' ')
    cp -R "$T/base" "$T/b2" && cp "$T/end/$SCRIPT" "$T/b2/$SCRIPT"; _run "$T/b2"; bo=$(cat "$T/rc"); bmm=$(_st MISMATCH)
    cp -R "$T/end" "$T/mu"; python3 - "$T/mu/react-kit/agents/react-reviewer.md" <<'PY'
import sys
p = sys.argv[1]; t = open(p, encoding="utf-8").read()
assert t.count("**임계값 2 는 `UNVERIFIED_INVALID_EVIDENCE` 에만 적용된다.**") == 1
open(p, "w", encoding="utf-8").write(t.replace("**임계값 2 는 `UNVERIFIED_INVALID_EVIDENCE` 에만 적용된다.**", "**임계값 3 은 `UNVERIFIED_INVALID_EVIDENCE` 에만 적용된다.**"))
PY
    _run "$T/mu"; mo=$(cat "$T/rc"); mmm=$(_st MISMATCH); mre=$(grep -c '^MISMATCH react-kit/agents/react-reviewer\.md' "$T/out"); mok=$(_st OK)
    echo "ER-01 end_rc=$eo end_ok=$eok end_excluded=$eex end_stderr_bytes=$eerr base_rc=$bo base_mismatch=$bmm mut_rc=$mo mut_mismatch=$mmm mut_react=$mre mut_ok=$mok"
    ;;
  ER-02)
    cp -R "$T/end" "$T/g"; python3 - "$T/g/harness/docs/guides/qa-evaluation-guide.md" <<'PY'
import sys
p = sys.argv[1]; t = open(p, encoding="utf-8").read()
h = "## Canonical Unverified-Evidence Protocol (각 kit reviewer 복제용 정본)"
assert t.count(h) == 1
open(p, "w", encoding="utf-8").write(t.replace(h, "## Canonical Unverified Protocol (이름 바뀜)"))
PY
    _run "$T/g"; go=$(cat "$T/rc")
    cp -R "$T/end" "$T/d"; rm "$T/d/react-kit/agents/react-reviewer.md"
    sed -i.bak 's/근거는 \*\*도구 출력과 상태/근거는 **도구 기록과 상태/' "$T/d/design-kit/agents/design-reviewer.md" && rm "$T/d/design-kit/agents/design-reviewer.md.bak"
    dmut=$(grep -c '도구 기록과 상태' "$T/d/design-kit/agents/design-reviewer.md")
    _run "$T/d"; do_=$(cat "$T/rc"); dmi=$(grep -c '^MISSING react-kit/agents/react-reviewer\.md' "$T/out"); dmm=$(grep -c '^MISMATCH design-kit/agents/design-reviewer\.md' "$T/out")
    cp -R "$T/end" "$T/x"; cp "$T/x/backend-kit/agents/backend-reviewer.md" "$T/x/backend-kit/agents/extra-reviewer.md"
    _run "$T/x"; xo=$(cat "$T/rc"); xu=$(grep -c '^UNLISTED backend-kit/agents/extra-reviewer\.md' "$T/out")
    _run "$T/end" /; co=$(cat "$T/rc"); cok=$(_st OK)
    echo "ER-02 guide_rc=$go del_mut_applied=$dmut del_rc=$do_ del_missing=$dmi del_mismatch=$dmm extra_rc=$xo extra_unlisted=$xu cwd_root_rc=$co cwd_root_ok=$cok"
    ;;
  AR-01)
    impl=$(_impl); [ "$impl" = "$SCOPE" ] && ex=1 || ex=0
    mixed=0
    for c in $(_commits); do
      fs=$(_files_of "$c")
      nk=$(printf '%s\n' "$fs" | cut -d/ -f1 | grep -E -- '-kit$' | LC_ALL=C sort -u | grep -c .)
      nn=$(printf '%s\n' "$fs" | grep -vE '^[^/]+-kit/' | grep -vE '^\.harness/' | grep -c .)
      nh=$(printf '%s\n' "$fs" | grep -cE '^\.harness/')
      if [ "$nk" -gt 1 ] || { [ "$nk" -ge 1 ] && [ "$nn" -ge 1 ]; } || { [ "$nh" -ge 1 ] && [ $((nk+nn)) -ge 1 ]; }; then mixed=$((mixed+1)); echo "MIXED $c"; fi
    done
    sc=$(git -C "$W" log --first-parent --diff-filter=A --format=%H "$BASE..$END" -- "$CF_REL" | tail -1)
    scn=0; [ -n "$sc" ] && scn=$(_files_of "$sc" | grep -c .)
    fi1=$(git -C "$W" log --first-parent --no-merges --format=%H "$BASE..$END" -- . ':(exclude).harness' | tail -1)
    before=0; [ -n "$sc" ] && [ -n "$fi1" ] && [ "$sc" != "$fi1" ] && git -C "$W" merge-base --is-ancestor "$sc" "$fi1" && before=1
    while IFS= read -r -d '' f; do verify_seal "$f"; done < <(find "$T/end/.harness" -type f -name '*sprint-contract*.md' -print0) > "$T/seals"
    br=$(grep -c '^SEAL_BROKEN' "$T/seals"); self=$(grep -F "$CF_REL" "$T/seals" | awk '{print $1}')
    blk=$(_scope "$T/end/$CF_REL"); want=$(printf '%s\n.harness/\n' "$SCOPE" | LC_ALL=C sort)
    [ -n "$blk" ] && [ "$blk" = "$want" ] && sb=1 || sb=0
    echo "AR-01 impl_files=$(printf '%s\n' "$impl" | grep -c .) exact=$ex mixed_commits=$mixed seal_commit_files=$scn seal_before_impl=$before seals=$(grep -c . "$T/seals") seal_broken=$br this=$self scope_block=$sb"
    ;;
  AR-02)
    f=.github/workflows/ci.yml
    inv=$(awk '/^  validate:/{v=1} /^  playwright:/{v=0} v' "$T/end/$f" | grep -cE "^ +run: python3 $SCRIPT\$")
    all=$(grep -cE "^ +run: python3 $SCRIPT\$" "$T/end/$f")
    (cd "$T/end" && actionlint "$f" >/dev/null 2>&1); al=$?
    (cd "$T/base" && actionlint "$f" >/dev/null 2>&1); alb=$?
    ball=$(grep -cE "^ +run: python3 $SCRIPT\$" "$T/base/$f")
    echo "AR-02 in_validate=$inv in_file=$all actionlint_end=$al base_in_file=$ball actionlint_base=$alb"
    ;;
  AP-03)
    o="AP-03"
    for k in $KITS; do (cd "$T/end" && python3 scripts/validate-plugin.py "$k" --check=code-fence >/dev/null 2>&1); o="$o $k=$?"; done
    echo "$o"
    ;;
  AP-04)
    python3 - "$T/base" "$T/end" $REV backend-kit/skills/backend-audit/SKILL.md design-kit/skills/design-audit/SKILL.md planning-kit/skills/plan-audit/SKILL.md react-kit/skills/react-audit/SKILL.md rust-kit/skills/rust-audit/SKILL.md <<'PY'
import sys
def fm(p):
    L = open(p, encoding="utf-8").read().split("\n")
    if not L or L[0].strip() != "---":
        return None
    for i in range(1, len(L)):
        if L[i].strip() == "---":
            return L[1:i]
    return None
b, e, files = sys.argv[1], sys.argv[2], sys.argv[3:]
name = sum(1 for f in files if fm(f"{e}/{f}") and any(l.startswith("name: ") for l in fm(f"{e}/{f}")))
same = sum(1 for f in files if fm(f"{b}/{f}") is not None and fm(f"{b}/{f}") == fm(f"{e}/{f}"))
print(f"AP-04 files={len(files)} name={name} fm_same={same}")
PY
    ;;
  RE-01)
    add=$(git -C "$W" log --first-parent --no-merges --diff-filter=A --format= --name-only "$BASE..$END" -- . ':(exclude).harness' | grep . | LC_ALL=C sort -u)
    echo "RE-01 added=$(printf '%s' "$add" | grep -c .) script=$(printf '%s\n' "$add" | grep -cxF "$SCRIPT")"
    ;;
  RE-02)
    s="$T/end/$SCRIPT"
    echo "RE-02 plugin_utils=$(grep -cE '^(from plugin_utils import|import plugin_utils)' "$s") guide_path=$(grep -cF 'qa-evaluation-guide.md' "$s") canon_text=$(grep -cF '75.8%' "$s")"
    ;;
  DG-01)
    echo "DG-01 release_sh=$(git -C "$W" log --first-parent --no-merges --format= --name-only "$BASE..$END" -- scripts/release.sh | grep -c .)"
    ;;
  DG-02)
    [ -x "$ML" ] || { echo "DG-02 ML_MISSING $ML"; return 2; }
    _ml "$T/base" > "$T/mlb"; _ml "$T/end" > "$T/mle"
    worse=$(awk 'NR==FNR{b[$1" "$2]=$3; next} {k=$1" "$2; if ($3 > (k in b ? b[k] : 0)) {print "WORSE", k, "base=" (k in b ? b[k] : 0), "end=" $3}}' "$T/mlb" "$T/mle")
    python3 -W error -m py_compile "$T/end/$SCRIPT" 2>/dev/null; pc=$?
    python3 -m json.tool "$T/end/design-kit/evals/evals.json" >/dev/null 2>&1; js=$?
    echo "DG-02 md=$(printf '%s\n' "$MDF" | grep -c .) base_warn=$(awk '{n+=$3} END{print n+0}' "$T/mlb") end_warn=$(awk '{n+=$3} END{print n+0}' "$T/mle") worse=$(printf '%s' "$worse" | grep -c .) py_compile=$pc json=$js"
    printf '%s' "$worse" | grep . || true
    ;;
  DG-04)
    _run "$T/end"; echo "DG-04 rc=$(cat "$T/rc") stderr_bytes=$(wc -c < "$T/err" | tr -d ' ') traceback=$(grep -c 'Traceback' "$T/err")"
    ;;
  DG-05)
    echo "DG-05 base: $(_checks "$T/base")"
    echo "DG-05 end: $(_checks "$T/end")"
    ;;
  *) echo "UNKNOWN $1"; return 2 ;;
  esac
}
```

봉인 전 실측 (2026-09-26, 예행 도구는 스크래치 `/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/bda55d45-296c-491f-89ba-b52042d58e72/scratchpad/c4b/`.
`rrepo/` 는 작업 폴더를 `git clone --shared` 한 예행 저장소이고, `rh-apply.py` 가 시작 커밋에서 만든 가지에 예행 구현(초안)을 얹는다. 작업 폴더 `ak-c4b` 의 킷 파일은 손대지 않았다):

| 행 | 무엇 | 결과 |
| -- | ---- | ---- |
| 1 | 준비 단계 — `command -v bash` · bash 안 `type grep` · `command -v python3` · `actionlint -version` · `ML --version` · `command -v shasum` | `/opt/homebrew/bin/bash`(GNU bash 5.3.9) · `/usr/bin/grep`(이 맥 zsh 의 `grep` 은 ugrep 이라 측정은 bash 로만) · `/Users/jackson/.pyenv/versions/3.14.3/bin/python3`(3.14.3) · `1.7.12` · `markdownlint-cli2 v0.23.2 (markdownlint v0.41.1)` · `/usr/bin/shasum` |
| 2 | 알려진 답 — 원문 덩어리 줄 수를 `sed -n 1244,1295p` · `sed -n 891,897p` 의 빈 줄 아닌 줄로 손으로 셈 | 47 · 7, `copy.py blocks` 도 `a_lines=47` · `b_lines=7`. 원문 자신에 대조 `a=1 b=1` |
| 3 | 시작 판을 끝 판으로 넣은 측정(`END_OVERRIDE=f81568d8fbf58382172281388ec5d7756f9f46b2`) | `SK-01 … a1=0 b1=0 prov1=0` · `SK-02 rust-kit=1/1 backend-kit=1/1 infra-kit=1/1` · `SK-03 old_thr=20 num_ref=9 three_way=7 gate_ok=3 env_ok=3 invalid_ok=5` · `SK-04 reason_na=0` · `SK-05 … labels_ok=4/7` · `SK-06 old_thr=6 num_ref=1 three_way=1 skills_with_gate=3/6` · `SK-07 … labels_ok=4/6` · `SK-08 req4=0 script=0` |
| 4 | 예행 1 판 — 끄기 주석 없이 사본을 넣은 초안에 markdownlint 열셋 | 일곱 reviewer 마다 `MD029` 0 → 3, planning · react `MD028` 0 → 1. 끄기 · 켜기 주석 쌍을 넣은 2 판은 늘어난 규칙 0(backend `MD028` 1 → 0) |
| 5 | 예행 1 판 `scan.py` — 처음 규칙(「조항 2 · 3」 을 모두 금지, 「」 안도 셈) | 「「임계값 2 는」 조항」 같은 첫머리 인용과 원문을 직접 가리키는 「정본 조항 3」(backend · rust · infra 감사 스킬, 시작 판부터 있음)이 잡혔다. 인용은 빼고 재고, 금지는 「조항 2」 로 좁혔다(원문 번호 겹침은 넘김) |
| 6 | 예행 `rh/good`(가짜 봉인을 채운 이 계약 사본을 봉인 커밋으로 싣고 초안 구현을 킷마다 한 커밋 · 도구 한 커밋, 9 커밋)에 `m` 스물둘 | 모두 각 조건 측정 절의 기대 값과 같음(`SK-09 added_lines=98`, `DG-02 base_warn=204 end_warn=203`, 약 22 초) |
| 7 | 예행 변형 — `rh/mutate`(react 사본 한 낱말) · `rh/mix`(킷 둘 한 커밋) · `rh/noseal`(봉인 커밋에 구현 · 조건 줄 수정) · `rh/extra`(release.sh · 문서 HTML · 새 파일 · react 끝에 펜스와 `name:` 변경) | `SK-01 a1=6` · `DG-05 end … copies=1` / `mixed_commits=1` / `mixed_commits=1 seal_commit_files=2 seal_before_impl=0 seal_broken=1 this=SEAL_BROKEN` / `impl_files=19 exact=0` · `SC-00 release_paths=1` · `DG-01 release_sh=1` · `AP-03 react-kit=2` · `AP-04 fm_same=11` · `RE-01 added=2` |
| 8 | 예행 검사 초안(스크래치 `rh-check-script.py`)으로 ER-01 · ER-02 여섯 경우 | `m ER-01` · `m ER-02` 가 조건의 기대 값과 같음 — 작업 폴더 `/` 에서 절대 경로로 불러도 `OK` 7 줄 |
| 9 | 저장소 검사 — 작업 폴더 시작 판 | 킷 일곱 `validate-plugin.py` · 전체 · `sync-docs` · `sync-evals` · `run-evals` · `stale-values` · `docs-links` 모두 종료 코드 0 |
| 10 | 떼어 내기 — 이 계약에서 세 블록을 떼어 스크래치 `k/` 원본과 `cmp` | `copy.py` · `scan.py` · `m.sh` 모두 같음 |
| 11 | 교차 진단 반영 뒤 다시 잼 — 새 블록을 스크래치 `c4b-impl/k/` 로 떼어 시작 판을 끝 판으로 넣음 | `SK-03 … num3_ref=6 … base_num3_ref=6` · `SK-06 … base_old_thr=6 base_num_ref=1 base_three_way=1`(「정본 조항 3」 적중은 거름) · `AR-01 … seals=186 seal_broken=0`. 옛 찾기 형태(`sprint-contract*.md`)는 83 개만 잡았고 새 형태는 186 개(history 104 개 포함)를 잡는다 |
| 12 | 같은 새 블록으로 예행 `rh/good`(`END_OVERRIDE=rh/good`) | `AR-01 impl_files=16 exact=1 mixed_commits=0 seal_commit_files=1 seal_before_impl=1 seals=187 seal_broken=0 this=SEAL_OK scope_block=1` · `RE-02 plugin_utils=1 guide_path=1 canon_text=0` · `SK-03 … num3_ref=1`(초안이 `rust-reviewer.md:166` 「정본 조항 3」 을 남겨 새 측정이 잡았다 — 실제 구현이 고친다) |
| 13 | RE-02 음성 대조 — 예행 `rh/badre`(`rh/good` 위에서 새 검사의 `plugin_utils` 가져오기를 지우고, 원문 조항 덩어리를 스크립트 안 문자열로 넣고, 원문 경로 글자를 지움) | `RE-02 plugin_utils=0 guide_path=0 canon_text=1` — 세 값 모두 바뀌었다 |

## Skill

- [ ] SK-01: 킷 reviewer 일곱이 원문 두 덩어리를 글자 그대로 한 번씩 들고, 원문 판을 적은 출처 한 줄이 있다 — Given: 이 계약의 구현 커밋이 가지 `chore/ak-c4b` 에 들어간 뒤 · When: `m SK-01` 이 끝 판의 일곱 파일(`m.sh` 의 `REV`)을 원문 `harness/docs/guides/qa-evaluation-guide.md` 의 조항 덩어리(§Canonical Unverified-Evidence Protocol 안 `1. **마커는` 줄부터 다음 인용 줄 앞까지, 빈 줄을 뺀 47 줄)와 4 요건 덩어리(`UNVERIFIED_ENV` 남용 방지 4 요건 제목 아래 1 ~ 4 항, 7 줄)에 대조하면(줄 앞 공백과 인용 표식 `>` 를 떼고 빈 줄을 버린 뒤 끊김 없는 연속으로 찾는다) · Then: 일곱 모두 조항 덩어리 1 번 · 4 요건 덩어리 1 번이고, 덩어리 밖에 `qa-evaluation-guide.md` · `v5.1` · 「계약」 이 한 줄에 함께 든 출처 줄이 정확히 1 줄이다 — 풀이를 다음 줄로 이어 써도 되지만 그 줄에 세 낱말이 모두 들면 2 줄로 세어 실패다 [exact, enumerated] (측정: `m SK-01` 첫 줄이 `a_lines=47` · `b_lines=7` 로 시작하는 두 덩어리 요약이고, 파일 줄 일곱이 모두 `a=1 b=1 prov=1`, 끝 줄이 `SK-01 files=7 a1=7 b1=7 prov1=7 base_a1=0 base_b1=0 guide=[a=1 b=1]`. 알려진 답: 원문 자신에 대조하면 `guide=[a=1 b=1]` 이고, 덩어리 줄 수는 시작 판 `sed -n 1244,1295p` · `sed -n 891,897p` 의 빈 줄 아닌 줄 수 47 · 7 과 같다. 양성 대조: 시작 판 `base_a1=0 base_b1=0`, 예행 `rh/mutate`(react 사본의 「임계값 2 는」 을 「임계값 3 은」 으로) → `a1=6`)
- [ ] SK-02: 사본을 두고 사실과 다른 옛 설명이 남지 않는다 — 끝 판에서 `rust-kit/agents/rust-reviewer.md` 의 「옮기지 않았다」 · `backend-kit/agents/backend-reviewer.md` 의 「어휘만 이 킷 도메인으로 치환한」 · `infra-kit/agents/infra-reviewer.md` 의 「2026-08-13 개정 · 4 분기 + 카운터 분리)의 복제본」 이 각각 0 번 나온다 [exact, enumerated] (측정: `m SK-02` 가 `SK-02 rust-kit=0/1 backend-kit=0/1 infra-kit=0/1` — 빗금 뒤 1 은 같은 글을 시작 판에서 센 양성 대조라 1 이 아니면 측정이 죽은 것이고 실패다)
- [ ] SK-03: reviewer 일곱의 사본 밖 글이 새 판과 맞다 — Given: 구현 커밋 뒤 · When: `m SK-03` 이 일곱 파일에서 두 덩어리 줄을 뺀 나머지 줄을 `scan.py` 로 세면 · Then: (a) 임계 2 를 말하는 줄 가운데 `INVALID` · `invalid_evidence` 가 없는 줄 0 — 새 규칙을 말하는 줄도 어느 장부인지 `invalid_evidence` · `INVALID` 이름을 같은 줄에 적는다. 순우리말로만 쓴 임계 줄은 옛 규칙 줄로 센다 (b) 사본 조항을 「조항 2」 · 「조항 2·3」 · 「프로토콜 2항」 으로 가리키는 줄 0, 그리고 「조항 3」 으로 가리키는 줄 0(사본 안에 3 이 둘이다) (c) 「3 분기」 가 든 줄 0 (d) 일곱 모두 `0.60` 과 `BLOCKED` 가 한 줄에 든 판정 줄 1 이상 (e) 일곱 모두 `env_gaps` 가 든 줄 1 이상 (f) 일곱 모두 `UNVERIFIED_INVALID_EVIDENCE` · `invalid_evidence` · `[미검증:INVALID]` 가운데 하나가 든 줄 1 이상이다 [exact, enumerated] (측정: `m SK-03` 끝 줄이 `SK-03 old_thr=0 num_ref=0 num3_ref=0 three_way=0 gate_ok=7 env_ok=7 invalid_ok=7 base_old_thr=20 base_num_ref=9 base_num3_ref=6 base_three_way=7 base_gate_ok=3` 이고 `HIT` 줄 0. `base_…` 는 같은 측정을 시작 판에 돌린 양성 대조라 값이 다르면 측정이 죽은 것이고 실패다. 「」 로 감싼 조항 첫머리 인용(예: 「임계값 2 는」)은 (a) 에서 빼고 잰다. 알려진 답: 시작 판 `design-kit/agents/design-reviewer.md` 한 파일의 (a) 는 손으로 센 네 줄 `:30` · `:34` · `:182` · `:188` 과 같은 4, 시작 판 `base_num3_ref=6` 은 판단 기록 2 의 여섯 곳과 같다)
- [ ] SK-04: planning-reviewer 의 판정 칸이 N/A 에도 사유를 받는다(원문 조항 1 「N/A 를 사유 없이 쓰면 금지 대상」) — 끝 판 `planning-kit/agents/planning-reviewer.md` 에서 `reason:` 으로 시작하는 줄이 1 줄이고 그 줄에 `N/A` 가 든다 [exact] (측정: `m SK-04` 가 `SK-04 reason_lines=1 reason_na=1 base_reason_na=0` — 시작 판은 N/A 칸이 없어 0)
- [ ] SK-05: reviewer 일곱의 판정 글이 `## GAP 분석` 판정 대응표의 네 경우 S1 ~ S4 에 표의 판정값을 낸다 — Given: 구현 커밋 뒤 · When: QA 가 파일마다 사본 밖 판정 글(판정 목록 · 우선순위 · 적용 메모)을 읽어 네 경우에 그 파일이 내라고 하는 판정값을 적으면 · Then: 일곱 × 넷 28 칸이 표와 모두 같고, 판정 목록 어느 줄에도 걸리지 않는 칸이 0 이다 [exact, enumerated] (측정: QA 가 칸마다 판정값과 근거 `파일:줄` 을 적는다. 보조 측정: `m SK-05` 가 `SK-05 files=7 scenarios=4 cases_total=28 labels_ok=7/7` 이고 `LABEL_MISSING` 줄 0 — 파일마다 기대 판정값 글자가 사본 밖에 모두 있는지다. 양성 대조: 시작 판을 끝 판으로 넣으면(`END_OVERRIDE=f81568d8fbf58382172281388ec5d7756f9f46b2`) `labels_ok=4/7` · `LABEL_MISSING` 셋(design · react · api 의 `BLOCKED`)이고, 시작 판 `rust-kit/agents/rust-reviewer.md:168` 은 S2 에서 어느 줄에도 걸리지 않는 칸이다)
- [ ] SK-06: 받아 쓰는 쪽이 새 판과 맞다 — 끝 판에서 (a) `backend-kit/skills/backend-audit/SKILL.md` · `design-kit/evals/evals.json` · `design-kit/skills/design-audit/SKILL.md` · `planning-kit/skills/plan-audit/SKILL.md` · `react-kit/skills/react-audit/SKILL.md` · `rust-kit/skills/rust-audit/SKILL.md` 여섯과 `infra-kit/skills/infra-audit/SKILL.md` 를 `scan.py` 로 세어 옛 임계 줄 0 · 「조항 2」 줄 0 · 「3 분기」 줄 0 이고 (b) 감사 스킬 여섯(SKILL.md 여섯) 모두 `0.60` 과 `BLOCKED` 가 한 줄에 든 판정 줄이 1 이상이며 (c) `infra-kit/skills/infra-audit/SKILL.md` 는 시작 판과 글자까지 같고 (d) api-kit 스킬 가운데 `api-reviewer` 를 적은 파일이 0 이다(받아 쓰는 쪽이 없다는 근거) [exact, enumerated] (측정: `m SK-06` 끝 줄이 `SK-06 old_thr=0 num_ref=0 three_way=0 skills_with_gate=6/6 infra_audit=same api_skills_citing_reviewer=0 base_old_thr=6 base_num_ref=1 base_three_way=1` 이고 `HIT` 줄 0 — 원문을 직접 가리키는 「정본 조항 3」 은 넘김이라 `num3_ref` 적중은 이 조건이 보지 않는다(`m SK-06` 이 거른다). `base_…` 는 시작 판에 돌린 양성 대조다. 시작 판을 끝 판으로 넣으면 `skills_with_gate=3/6`)
- [ ] SK-07: 받아 쓰는 감사 스킬 여섯(design-audit · plan-audit · react-audit · backend-audit · rust-audit · infra-audit)의 판정 글이 판정 대응표 S1 ~ S4 에 표의 판정값을 낸다 — Given · When · Then 은 SK-05 와 같고 여섯 × 넷 24 칸이다. react-audit 리포트 틀의 판정 칸이 `BLOCKED` 를 받아야 S3 칸이 맞는다 [exact, enumerated] (측정: QA 가 칸마다 판정값 · 근거 `파일:줄`. 보조 측정: `m SK-07` 이 `SK-07 files=6 scenarios=4 cases_total=24 labels_ok=6/6` 이고 `LABEL_MISSING` 줄 0. 양성 대조: 시작 판을 끝 판으로 넣으면 `labels_ok=4/6` · `LABEL_MISSING` 둘(design-audit · react-audit 의 `BLOCKED`)이고, 시작 판 `backend-kit/skills/backend-audit/SKILL.md:113` · `rust-kit/skills/rust-audit/SKILL.md:125` 는 S2 에서 어느 줄에도 걸리지 않는 칸이다)
- [ ] SK-08: infra-kaizen Gotcha 8 표의 원문 행이 새 판을 따른다(F1H-48) — 끝 판 `.claude/skills/infra-kaizen/SKILL.md` 에서 `| Canonical Unverified-Evidence Protocol` 로 시작하는 표 줄이 1 줄이고, 그 줄에 「4 요건」 과 `scripts/check-reviewer-protocol-copies.py` 가 모두 든다 [exact] (측정: `m SK-08` 이 `SK-08 rows=1 req4=1 script=1 base_req4=0 base_script=0`)
- [ ] SK-09: 새로 쓴 글에 번역투 여섯 패턴이 없다(`tone-kit/references/locale-korean.md` §8 G-1) — 시작 판 → 끝 판 차이에서 마크다운 열셋(`m.sh` 의 `MDF`)에 더해진 줄 가운데 원문 두 덩어리 줄(정규화해 같은 줄)을 뺀 줄에 G-1 정규식 적중이 0 이다 [exact] (측정: `m SK-09` 가 `SK-09 added_lines=` 로 시작하고 `g1_hits=0 canon_g1=1` 로 끝나며 `G1` 줄 0 — `added_lines` 는 구현이 만드는 값이라 잰 값을 그대로 적는다. `canon_g1=1` 은 원문 덩어리에 적중(「적용된다」)이 하나 있다는 양성 대조라, 원문 줄을 빼는 단계가 살아 있다는 확인이다)

## Script

- [ ] SC-00: N/A (Script 카테고리는 `release.sh` 연동 · 버전 올림 · `marketplace.json` 갱신이다. 이 계약은 그 파일들과 킷 `plugin.json` 을 건드리지 않는다 — 릴리스는 PR 을 합친 뒤 부모가 한다. 측정: `m SC-00` 이 `SC-00 release_paths=0` — 구간 커밋이 `.claude-plugin` · 킷 `.claude-plugin` · `scripts/release.sh` 에서 건드린 경로 수. 양성 대조: 예행 `rh/extra`(`scripts/release.sh` 한 줄) → `release_paths=1`)

## Error

- [ ] ER-01: 새 검사 `scripts/check-reviewer-protocol-copies.py` 가 사본이 같을 때와 다를 때를 가른다 — 출력은 검사한 파일마다 한 줄 `<상태> <경로>`(상태는 `OK` · `MISMATCH` · `MISSING` · `UNREADABLE` · `UNLISTED` · `EXCLUDED`, `EXCLUDED` 는 경로 뒤에 이유)와 요약 한 줄이고, 종료 코드는 `harness/evals/gate-exit-codes.md` 를 따른다(0 통과 · 1 위반 · 2 검사 못 함 · 둘이 함께면 2). Given: 끝 판 · When: `m ER-01` 이 (i) 끝 판 (ii) 시작 판에 새 스크립트만 넣은 사본 (iii) 끝 판에서 react 사본 「임계값 2 는」 을 「임계값 3 은」 으로 바꾼 사본에서, 작업 폴더를 저장소 뿌리로 두고 스크립트를 돌리면 · Then: (i) 종료 코드 0 · `OK` 7 줄 · `EXCLUDED howto-kit/agents/howto-reviewer.md` 뒤에 이유 · 표준 오류 0 바이트 (ii) 종료 코드 1 · `MISMATCH` 7 줄 (iii) 종료 코드 1 · `MISMATCH` 1 줄이 `react-kit/agents/react-reviewer.md` 이고 `OK` 6 줄이다 [exact] (측정: `m ER-01` 이 `ER-01 end_rc=0 end_ok=7 end_excluded=1 end_stderr_bytes=0 base_rc=1 base_mismatch=7 mut_rc=1 mut_mismatch=1 mut_react=1 mut_ok=6`. (ii) 가 시작 판의 옛 사본 일곱을 모두 잡는 것이 이 검사의 양성 대조다)
- [ ] ER-02: 새 검사가 못 읽는 경우를 통과로 넘기지 않는다 — When: `m ER-02` 가 끝 판 사본으로 (a) 원문 절 제목을 바꾼 사본 (b) react-reviewer 를 지우고 design 사본의 「도구 출력과 상태」 를 「도구 기록과 상태」 로 바꾼 사본 (c) `backend-kit/agents/extra-reviewer.md` 를 더한 사본 (d) 작업 폴더를 `/` 로 두고 절대 경로로 부른 끝 판에서 스크립트를 돌리면 · Then: (a) 종료 코드 2 (b) 종료 코드 2 이면서 `MISSING react-kit/agents/react-reviewer.md` 줄과 `MISMATCH design-kit/agents/design-reviewer.md` 줄이 둘 다 있다 — 한 파일을 못 읽어도 나머지를 재고 말한다 (c) 종료 코드 1 · `UNLISTED backend-kit/agents/extra-reviewer.md` 줄 (d) 종료 코드 0 · `OK` 7 줄이다 [exact] (측정: `m ER-02` 줄이 `ER-02 guide_rc=2` 로 시작하고, `del_mut_applied` 값이 1 이상이며, 이어서 `del_rc=2 del_missing=1 del_mismatch=1 extra_rc=1 extra_unlisted=1 cwd_root_rc=0 cwd_root_ok=7` 이다. `del_mut_applied` 는 변형이 실제로 들어갔다는 확인이라 0 이면 (b) 측정이 무효이고 실패다)

## Architecture

- [ ] AR-01: 변경 범위가 선언과 같고, 커밋이 섞이지 않았고, 이 계약이 봉인돼 있으며 끝 판 `.harness/` 의 다른 계약 봉인도 깨지지 않았다(저장소 전체 검사) [exact, enumerated] (Given: 이 계약의 커밋이 가지에 모두 들어간 뒤 · 측정: `m AR-01` 이 `AR-01 impl_files=16 exact=1 mixed_commits=0 seal_commit_files=1 seal_before_impl=1` 로 시작하고, `seals` 값이 187 이상이며, 이어서 `seal_broken=0 this=SEAL_OK scope_block=1` 이다 — `seals` 는 봉인 검사를 돌린 파일 수로, 시작 판 186 개(history 104 개 포함)에 이 계약 하나를 더한 187 이 하한이다. 값의 뜻 — 시작 커밋..끝 판 구간에서 첫 부모 줄기의 병합 아닌 커밋이 건드린 `.harness/` 밖 경로 집합이 `## 범위 경계` sprint-scope 블록의 16 경로와 정확히 같다(생성물이 없어 뺄 경로도 없다) · 어떤 커밋도 킷 둘을 싣거나, 킷과 킷 밖 경로를 함께 싣거나, `.harness/` 와 다른 경로를 함께 싣지 않았다 · 이 계약을 처음 더한 커밋의 파일이 1 개이고 그 커밋이 첫 구현 커밋의 조상이다 · 끝 판 `.harness/` 에서 이름에 `sprint-contract` 가 든 `.md` 전부(`history/` 안 `<날짜>-sprint-contract*.md` 포함, `find -name '*sprint-contract*.md'`)에 봉인 검사를 돌려 `SEAL_BROKEN` 0 · 이 계약은 `SEAL_OK` · 끝 판 계약의 sprint-scope 블록 줄 집합이 `m.sh` 의 `SCOPE` 와 `.harness/` 를 합친 것과 같다. 상한은 `end_ref` 로 풀고 `HEAD` 를 쓰지 않는다. 양성 대조: 예행 `rh/mix`(킷 둘 한 커밋) → `mixed_commits=1`, `rh/noseal`(봉인 커밋에 구현이 섞이고 조건 줄을 뒤에 고침) → `mixed_commits=1 seal_commit_files=2 seal_before_impl=0 seal_broken=1 this=SEAL_BROKEN`, `rh/extra`(범위 밖 경로 셋 · react 한 곳을 한 커밋에) → `impl_files=19 exact=0 mixed_commits=1`)
- [ ] AR-02: CI 가 새 검사를 돈다 — 끝 판 `.github/workflows/ci.yml` 의 `validate:` 묶음 안(`playwright:` 앞)에 `run: python3 scripts/check-reviewer-protocol-copies.py` 줄이 정확히 1 개이고 파일 전체에도 1 개이며, `actionlint` 가 끝 판에서 종료 코드 0 이다 [exact] (측정: `m AR-02` 가 `AR-02 in_validate=1 in_file=1 actionlint_end=0 base_in_file=0 actionlint_base=0` — `base_in_file=0` 은 시작 판에 그 줄이 없었다는 양성 대조다)

## Anti-patterns

- [ ] AP-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수 (```` ```text, ```bash, ```yaml ```` 등). 판정 권위는 validate-plugin V6 상태기계다 — 여는/닫는 fence 가 동형이라 줄 단위 정규식으로는 판정 불가. 이번 변경에 적용: 끝 판 전체 사본에서 킷 일곱마다 `python3 scripts/validate-plugin.py <킷> --check=code-fence` 종료 코드 0 (측정: `m AP-03` 이 `AP-03 api-kit=0 backend-kit=0 design-kit=0 infra-kit=0 planning-kit=0 react-kit=0 rust-kit=0`. 양성 대조: 예행 `rh/extra`(react-reviewer 끝에 언어 힌트 없는 펜스) → `react-kit=2`)
- [ ] AP-04: SKILL.md / agents/*.md frontmatter 에서 name 필드 누락 — validate-plugin V1 FAIL. 이번 변경에 적용: 바뀌는 reviewer 일곱과 SKILL.md 다섯, 모두 열둘의 첫 frontmatter 블록에 `name:` 줄이 있고 그 블록이 시작 판과 글자 그대로 같다 (측정: `m AP-04` 가 `AP-04 files=12 name=12 fm_same=12`. 양성 대조: 예행 `rh/extra`(react-reviewer `name:` 값을 바꿈) → `fm_same=11`)

## Reusability

- [ ] RE-01: 다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다. 이번 변경에 적용: 새로 생긴 파일은 `scripts/check-reviewer-protocol-copies.py` 하나이고 공용 경로(`project.yaml` `reusability.shared_path` 값 `scripts/`)에 있어 어느 킷 작업에서도 부를 수 있다 (측정: `m RE-01` 이 `RE-01 added=1 script=1` — 구간 커밋이 더한 `.harness/` 밖 새 파일 수와 그중 새 검사. 양성 대조: 예행 `rh/extra`(새 파일 하나 더) → `added=2`)
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다. 이번 변경에 적용: 새 검사는 저장소 뿌리를 기존 `scripts/plugin_utils.py` 의 값으로 얻고(가져오기 줄 1 이상), 원문 글을 스크립트 안에 품지 않고 원문 파일 `qa-evaluation-guide.md` 를 읽는다(원문에만 있는 「75.8%」 글자 0) (측정: `m RE-02` 줄에서 `plugin_utils` 값 1 이상 · `guide_path` 값 1 이상 · `canon_text=0`. 음성 대조: 예행 `rh/badre`(새 검사에서 `plugin_utils` 가져오기를 지우고 저장소 뿌리를 스스로 계산하며, 원문 조항 덩어리를 스크립트 안 문자열로 품고, 원문 경로 글자를 지움) → `plugin_utils=0 guide_path=0 canon_text=1`)

## Diagnostics

- [ ] DG-01: N/A (`commands.analyze` 는 `bash -n scripts/release.sh` 라 `scripts/release.sh` 만 잰다 — 이번 변경 파일과 교집합 0 개. 측정: `m DG-01` 이 `DG-01 release_sh=0`. 양성 대조: 예행 `rh/extra` → `release_sh=1`. 실제 검사는 DG-02 · DG-05)
- [ ] DG-02: IDE diagnostics 워닝/인포 0개 (`diagnostics.ide_exclude` 값 `[]`) — 이번 변경에 적용: (a) 편집기 마크다운 확장과 같은 조건(markdownlint-cli2 0.23.2 · 줄 길이 규칙 MD013 끔)으로 마크다운 열셋(`m.sh` 의 `MDF`)을 시작 판과 끝 판에서 재어 파일 · 규칙마다 끝 판 경고 수가 시작 판 이하다 — 원문 번호 겹침이 내는 MD029 도 늘면 안 된다 (b) 새 스크립트가 `python3 -W error -m py_compile` 로 통과 (c) `design-kit/evals/evals.json` 이 `python3 -m json.tool` 로 통과. 스펠체크는 사용자 규칙대로 뺀다 [exact, enumerated] (측정: `m DG-02` 줄이 `DG-02 md=13 base_warn=204` 로 시작하고, `end_warn` 값이 204 이하이며, 이어서 `worse=0 py_compile=0 json=0` 이고 `WORSE` 줄 0 — `base_warn=204` 는 측정이 살아 있다는 확인이라 다르면 실패. 양성 대조: 예행 1 판(끄기 주석 없이 사본을 넣음)에서 일곱 reviewer 마다 `MD029` 가 0 → 3, planning · react 는 `MD028` 도 0 → 1)
- [ ] DG-03: N/A (`commands.test` 는 `bash scripts/release.sh 2>&1 || true` 라 `scripts/release.sh` 만 잰다 — 교집합 0 개. 측정: DG-01 과 같은 `m DG-01` 의 `release_sh=0`)
- [ ] DG-04: 실제 앱/서버 구동 시 에러 0개 — 이번 변경에 적용: 구동하는 것은 새 검사 스크립트 하나다. 끝 판 저장소 뿌리에서 돌려 종료 코드 0 · 표준 오류 0 바이트 · `Traceback` 0 줄이다 (측정: `m DG-04` 가 `DG-04 rc=0 stderr_bytes=0 traceback=0`. 양성 대조: ER-02 (a) 사본은 종료 코드 2 를 낸다 — 오류를 삼키지 않는다는 확인)
- [ ] DG-05: 저장소 검사가 끝 판에서 모두 통과한다 — 끝 판 전체 사본에서 킷 일곱 각각의 `scripts/validate-plugin.py <킷>` · `scripts/validate-plugin.py`(전체) · `scripts/sync-docs.py --check-only` · `scripts/sync-evals.py --check-only` · `scripts/run-evals.py` · `scripts/check-stale-values.py` · `scripts/check-docs-links.py` · `scripts/check-reviewer-protocol-copies.py` 종료 코드가 모두 0 이고, 시작 판도 새 스크립트를 뺀 모두가 0 이다 [exact, enumerated] (측정: `m DG-05` 두 줄이 `DG-05 base: v-api-kit=0 v-backend-kit=0 v-design-kit=0 v-infra-kit=0 v-planning-kit=0 v-react-kit=0 v-rust-kit=0 validate-all=0 sync-docs=0 sync-evals=0 run-evals=0 stale-values=0 docs-links=0 copies=absent` 와 `DG-05 end: v-api-kit=0 v-backend-kit=0 v-design-kit=0 v-infra-kit=0 v-planning-kit=0 v-react-kit=0 v-rust-kit=0 validate-all=0 sync-docs=0 sync-evals=0 run-evals=0 stale-values=0 docs-links=0 copies=0`. 양성 대조: 예행 `rh/mutate` → `copies=1`)
