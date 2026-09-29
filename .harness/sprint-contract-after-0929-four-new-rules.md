---
feature: "새 규칙 넷 — 시각 문자열 · 요구 문서와 결정 기록 경계 · 조회일과 갱신일 · 서비스 계정 선택 순서"
slug: after-0929-four-new-rules
created: "2026-09-29 17:23"
complexity: "복잡"
conditions: 25
status: active
owner_session: bda55d45-296c-491f-89ba-b52042d58e72
conditions_digest: sha256:b809213f05ea2d04
measurement_digest: sha256:a142377bc0fe31be
locked_at: "2026-09-29 17:36"
---

## 배경

- 묶음 nr. 사용자가 2026-09-29T01:21:53.044Z 에 새 규칙 넷을 모두 넣기로 정했다 (`.harness/.meta/after-kaizen-0928/decisions.md` 끝에서 셋째 절, 통합 폴더 `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0928` 사본과 W 사본이 같다). 남은 일 목록 항목 A8 · A10 · A12. 근거와 넣을 자리 · 제안 문장은 원문 대조 파일 `.harness/.meta/after-kaizen-0928/ex/A8.md` · `ex/A10.md` · `ex/A12.md` 에 있다(W 사본과 통합 폴더 사본이 `cmp` 로 같다). 사용자 위임: 2026-09-27T01:22:01.089Z 「자동으로 다 진행해 나한테 묻지 말고 …」 · 2026-09-28 「약점과 일부만 한 거 다처리하지??」(세션 bda55d45-296c-491f-89ba-b52042d58e72).
- 작업 폴더 W = `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak3-nr`, 가지 `chore/ak3-nr`, 시작 판 `BASE` = `279085a3` (가지 `chore/ak3-fs2` 끝).
- 원문 인용은 대조 파일에 있는 글자를 그대로 옮긴다. 새로 인터넷을 뒤지지 않는다. 인용은 md · HTML 모두 「」 로 감싼다(오류-01 이 이 표시로 인용을 찾는다).
- 사용자가 할 일: 없음.

공통 전제 G (조건마다 되풀이하지 않는다) — 구현 · 기록 커밋이 가지 `chore/ak3-nr` 에 모두 들어가고, W 의 HEAD 가 그 가지 끝이며, `git -C W status --porcelain -- . ':(exclude).harness' ':(exclude)node_modules'` 가 빈 출력일 때 W 맨 위 폴더에서 잰다. 이 가지는 이 스프린트만 커밋하므로 HEAD 는 이 스프린트 끝과 같다(가지를 합친 뒤에는 재지 않는다). 측정 도우미는 `## 회귀 게이트` 의 `m <조건 번호>` 다. `TMPDIR` 는 scratch 아래 폴더로 둔다.

규칙마다 넣을 글자 (도우미 `measure.py` 맨 위 상수와 같다 — 구현은 이 글자를 그대로 쓴다):

- **① 시각 문자열 (backend-kit)** — 벽시계 날짜시각의 킷 형식 `YYYY-MM-DDTHH:mm:ss[.fraction]` 을 OpenAPI 에 `type: string` · `pattern` · `example` 로 적고 `format: date-time` 은 붙이지 않는다. 이 모양이 ISO 8601 의 유일한 권고가 아니라는 표시로 글자 「이 킷이 고른 형식」 을 쓴다. 인용 둘: RFC 3339 「All times expressed have a stated relationship (offset) to Coordinated Universal Time (UTC).」 (A8 58 줄), ISO 공개 설명 「September 27, 2022 at 6 p.m. is represented as 2022-09-27 18:00:00.000.」 (A8 76 줄 — 공개 예가 빈칸 구분이라 `T` 와 소수초는 킷이 고른 것이라는 근거, A8 84 · 86 · 186 줄). 오프셋 없는 문자열이 `date-time` 이 아니라는 문장은 이미 있다(`docs/backend/fundamentals/database.md:161-162`, `audit-criteria.md:28`) — 이번에 더하는 것은 모양 통일이다.
- **② 요구 문서와 결정 기록 경계 (planning-kit)** — 제품 비범위는 PRD(제품 요구 문서) 비범위 절에, 구조 · 비기능 특성 · 의존성 · 인터페이스에 걸린 결정 하나는 ADR(설계 결정 기록)에 적고 PRD 에는 그 ADR 경로만 적는다(A10 97-99 줄 제안). 이 경계는 글자 「원문에 직접 근거가 없는 추론」 으로 표시한다(A10 54 · 117 줄). 인용 셋: Atlassian 「A product requirements document (PRD) defines the purpose, features, and behavior of a product, aligning stakeholders and guiding development.」, adr.github.io 「An Architectural Decision Record (ADR) captures a single AD and its rationale.」, Nygard 「Each record describes a set of forces and a single decision in response to those forces.」 (A10 21 · 24 · 27 줄).
- **③ 조회일과 갱신일 (onboarding-kit)** — 출처마다 실제로 조회한 날(`조회 YYYY-MM-DD`)과 원문이 표시한 갱신일(`Last updated … UTC`, 원문에 있을 때만)을 따로 적는다. 갱신일만 보고 그 Step 본문을 다시 확인하지 않았으면 글자 그대로 「조회일을 바꾸지 않는다」. 원문은 저장소 기록법을 정하지 않으므로(A12 117 줄) 글자 「이 킷의 규칙」 으로 표시한다(A12 194 줄 제안).
- **④ 서비스 계정 선택 순서 (onboarding-kit)** — 새 Gotcha 10. 차례 표지 ①~⑤ 를 이 순서로: ① Google Cloud 안 — `ADC` 와 연결된 서비스 계정, ② GKE — `Workload Identity Federation for GKE`, ③ 혼자 쓰는 개발 환경 — 사용자 자격 증명 또는 `서비스 계정 가장`, ④ Google Cloud 밖에서 지원되는 외부 신원 제공자가 있을 때 — `Workload Identity Federation`, ⑤ 더 안전한 대안을 쓸 수 없을 때만 — `서비스 계정 키` (사유 · 보호 · 교체 · 폐기 절차를 함께). 인용 넷(A12 44 · 66 · 83 · 97 줄): 「We recommend that you avoid using service account keys whenever possible.」 · 「Use Workload Identity Federation whenever an application needs to access Google Cloud and has access to ambient credentials.」 · 「this way of initializing the SDK is strongly recommended for applications running in Google environments」 · 「For client-side applications such as tools, desktop programs, or mobile apps, don't use service accounts.」. 출처 표기는 규칙 ③ 을 따라 `조회 2026-09-28` · `Last updated 2026-09-24 UTC`(A12 22-28 줄).

복잡도 4 축 — 넷 모두 「예」 라 「복잡」 이다. Step 2.5 짝 조건을 넣었다.

| 축 | 물음 | 값 |
| -- | ---- | -- |
| 레이어 수 | 몇 개 계층을 관통하는가 | 셋 — 킷 원본(스킬 · 참고 문서), 레포 원칙 문서(`docs/backend` · `docs/planning`), 문서 사이트 쪽(`docs/<킷>/*.html`) · 드리프트 도구 |
| 공개 API·계약 변경 | 외부에 노출된 약속이 바뀌는가 | 예 — backend 감사 기준 · 규격 스킬, planning PRD 스킬, onboarding 가이드 스킬이 새 규칙을 사용자에게 요구한다 |
| 소비면 존재 | 반대편이 있는가 | 예 — 원본마다 짝 쪽(드리프트 매핑 `SOURCE_TO_HTML`)과 onboarding 가이드 게이트(`guide_gate`)가 같은 파일 안에 있다 |
| 회귀 위험 | 기존 동작이 깨질 수 있는가 | 예 — onboarding SKILL.md 를 고치면 그 안의 게이트 코드와 출력이 흔들릴 수 있고, 형식 목록의 출처 줄 틀은 게이트 G1 이 세는 줄이다 |

기능 조건 15 개는 스킬-01 ~ 스킬-04 · 오류-01 · 오류-02 · 구조-01 ~ 구조-08 · 진단-05 다 — Step 6.2 두 번째 명령 값. 복잡 가이드 9 ~ 20 안이다.

Step 2.5 짝 조건: 만드는 쪽은 킷 원본과 원칙 문서(스킬-01 ~ 스킬-04 · 구조-01 · 구조-02 의 md 몫), 쓰는 쪽은 짝 쪽 네 개(구조-01 ~ 구조-04 의 HTML 몫 · 구조-06)와 드리프트 도구(구조-05), 가이드 게이트(오류-02)다. `backend-kit/skills/...` · `planning-kit/skills/plan-prd/SKILL.md` 는 드리프트 매핑에 없는 원본이라 짝 쪽이 없다 — 규칙 본문은 매핑된 원칙 문서 `docs/backend/fundamentals/database.md` · `docs/planning/prd-patterns.md` 에도 싣고 그 짝 쪽을 맞춘다.

설정 값 대조 (`.harness/project.yaml` 을 글자 그대로 옮김):

| config key | project.yaml 에서 읽은 값 | 계약에 쓴 값 |
| ---------- | ------------------------- | ------------ |
| `commands.analyze` | `bash -n scripts/release.sh` | 진단-01 N/A (대상 파일이 이번 변경 밖) |
| `commands.test` | `bash scripts/release.sh 2>&1 \|\| true` | 진단-03 N/A (같은 이유) |
| `diagnostics.ide_exclude` | `[]` | 진단-02 `[]` |
| `contract_categories[].id` / `prefix` | Skill/스킬 · Script/스크립트 · Error/오류 · Architecture/구조 | 같음 |
| `anti_patterns[].id` / `message` | 금지-01 버전 하드코딩 · 금지-02 force push · 금지-03 bare code fence · 금지-04 frontmatter name | 금지-02 · 금지-03 · 금지-04 |

## GAP 분석 (Pre-Edit Audit)

모두 W 시작 판(`279085a3`)에서 연 값이다.

| 대상 | 읽은 증거 (`파일:줄` · 명령 출력) | 발견한 갭 | 조건 |
| --- | --- | --- | --- |
| `backend-kit/skills/backend-system/SKILL.md` | `:30` Gotcha 15 — `Z` · `+00:00` · `-00:00` 과 `format: date-time` 비검증만. `:33` Gotcha 18 벽시계 네 칸 표 · `:56` API 규격 행 | 벽시계 문자열 모양 없음 | 스킬-01 |
| `backend-kit/skills/backend-audit/references/audit-criteria.md` | `:28` Timestamp 행 — 벽시계에 `format: date-time` 이면 FAIL 은 있음(A8 앞 묶음). `:40` 시각 종류별 저장 행 | 킷 형식 · `type: string` · `pattern` 확인 없음 | 스킬-01 |
| `docs/backend/fundamentals/database.md` · `docs/backend-kit/database.html` | md `:140` 원칙 10, `:161-164` date-time 아님 · 킷 규칙 표시. html `:617-621` 같은 알림 상자. `m 구조-01` → `checks=14 missing=13` | 모양 · 인용 둘 없음 | 구조-01 |
| `planning-kit/skills/plan-prd/SKILL.md` | `:30` Gotcha 14(폐기한 결정) 가 마지막. `grep -n ADR` 0 | 경계 없음 | 스킬-02 |
| `docs/planning/prd-patterns.md` · `docs/planning-kit/prd-patterns.html` | md §폐기한 결정 `:143-162` · `:164` `## 참고 링크 (전체)`. html `#discarded` `:562-680`. `docs/planning/research-log.md:10-22` 에 2026-09-28 비교 기록(「킷 문장에는 … 고칠 곳이 없다」)이 이미 있음 | 원칙 문서 · 쪽에 경계 없음 | 구조-02 |
| `onboarding-kit/skills/setup-guide/SKILL.md` | `:28-44` §출처 원장 — 「출처 URL + 조회일」 만. `:267-275` Gotcha 9 가 마지막, `:277` `## Process`. `:52-167` 게이트 코드 블록. 게이트를 예제에 돌림 → `G1_LEDGER PASS steps=8 ledger=8` … `GATE_PASS` | 갱신일 분리 · 서비스 계정 순서 없음 | 스킬-03 · 스킬-04 · 오류-02 |
| `onboarding-kit/skills/setup-guide/references/format-checklist.md` · `docs/onboarding-kit/format-checklist.html` | md `:47` 틀 `**출처:** <이 Step 의 근거 1차 출처 URL — 조회 YYYY-MM-DD>`, html `:469` 같은 틀 | 갱신일 칸 없음 | 스킬-03 · 구조-03 |
| `docs/onboarding-kit/setup-guide.html` | `:192-212` 출처 원장 절, `:371` 「반복 실패를 막는 9개 체크다」, `:372-381` 항목 9 개, `:589-605` 끝 체크리스트 | 두 규칙 없음 | 구조-03 · 구조-04 |
| `docs/onboarding-kit/examples/fcm-ios-setup-guide.md:358` · `fcm-ios-example.html:478` | 이미 「Google 환경이면 키가 필요 없는 ADC … 먼저」(A12 188 줄 제안이 앞 묶음에서 반영됨) | 없음 — 이미 됨 | — |
| `onboarding-kit/skills/setup-guide/evals/evals.json:10,69` | 이미 `2026-09-28 조회 · Last updated 2026-09-24 UTC` | 없음 — 이미 됨 | — |
| 드리프트 `python3 scripts/detect-docs-drift.py --since 279085a3` | `no docs drift since 279085a3` · 종료 코드 0. 매핑: `docs/backend/` → `docs/backend-kit/`, `docs/planning/` → `docs/planning-kit/`, `onboarding-kit/skills/setup-guide/SKILL.md` · `…/references/` → `docs/onboarding-kit/` (`scripts/detect-docs-drift.py:46,64,84-85`) | 짝 넷이 잡혀야 한다 | 구조-05 |
| 로컬 CI · CI 전용 단계 | `## 회귀 게이트` 봉인 전 실측 | 통과 중 | 진단-05 |

## Skill

- [ ] 스킬-01: backend-kit 원본 둘이 벽시계 문자열 모양을 적는다 — `backend-kit/skills/backend-system/SKILL.md` 의 `15. **timestamp` 로 시작하는 줄에 `YYYY-MM-DDTHH:mm:ss[.fraction]` · `type: string` · `pattern` · `example` · `이 킷이 고른 형식` 다섯이, `backend-kit/skills/backend-audit/references/audit-criteria.md` 의 `| Timestamp 직렬화 규칙 |` 로 시작하는 줄에 `YYYY-MM-DDTHH:mm:ss[.fraction]` · `type: string` · `pattern` · `이 킷이 고른 형식` 넷이 있다. Given 공통 전제 G, When `m 스킬-01`, Then `checks=9 missing=0` · 종료 코드 0 [exact, enumerated]
  측정: `m 스킬-01`. 시작 판 `checks=9 missing=9` · 종료 코드 1 (봉인 전 실측). 알려진 답: scratch 복제본에 두 줄 끝에 글자를 붙이고 커밋 → `missing=0` · 종료 코드 0 (봉인 전 실측)
- [ ] 스킬-02: plan-prd 가 PRD · ADR 경계를 추론으로 표시해 적는다 — `planning-kit/skills/plan-prd/SKILL.md` 에 `15. **` 로 시작하는 Gotcha 줄이 있고 그 줄에 `ADR` · `비범위` · `원문에 직접 근거가 없는 추론` · `docs/planning/prd-patterns.md` 넷이 있다. Given 공통 전제 G, When `m 스킬-02`, Then `checks=4 missing=0` · 종료 코드 0 [exact, enumerated]
  측정: `m 스킬-02`. 시작 판 `checks=4 missing=4` · 종료 코드 1 (봉인 전 실측)
- [ ] 스킬-03: 출처 기록이 조회일과 원문 갱신일을 따로 적는다 — `onboarding-kit/skills/setup-guide/SKILL.md` 의 `### 출처 원장` 절(다음 `###` 머리 앞까지)에 `조회일` · `Last updated` · `조회일을 바꾸지 않는다` · `이 킷의 규칙` 넷이 있고, `onboarding-kit/skills/setup-guide/references/format-checklist.md` 에서 `**출처:** <` 로 시작하는 틀 줄이 정확히 하나이며 그 줄에 `조회 YYYY-MM-DD` · `Last updated` 가 있다. Given 공통 전제 G, When `m 스킬-03`, Then `checks=7 missing=0` · 종료 코드 0 [exact, enumerated]
  측정: `m 스킬-03`. 시작 판 `checks=7 missing=4` (`ledger:Last updated` · `ledger:조회일을 바꾸지 않는다` · `ledger:이 킷의 규칙` · `template:Last updated`) · 종료 코드 1 (봉인 전 실측)
- [ ] 스킬-04: 서비스 계정 선택 순서가 Gotcha 10 에 있다 — `onboarding-kit/skills/setup-guide/SKILL.md` 의 `### Gotcha 10:` 절(다음 `##` · `#` 머리 앞까지)에 ①~⑤ 가 이 차례로 나오고 각 표지부터 다음 표지 앞까지 ① `ADC` · ② `Workload Identity Federation for GKE` · ③ `서비스 계정 가장` · ④ `Workload Identity Federation` 과 `외부` · ⑤ `서비스 계정 키` 가 있으며, 절 안에 `## 배경` 규칙 ④ 의 인용 넷과 `조회 2026-09-28` · `Last updated 2026-09-24 UTC` 가 있고, 파일의 마지막 세 머리가 `### Gotcha 9` · `### Gotcha 10` · `## Process` 차례다. Given 공통 전제 G, When `m 스킬-04`, Then `checks=8 missing=0` · 종료 코드 0 [exact, enumerated]
  측정: `m 스킬-04`. 시작 판 `checks=8 missing=8` · 종료 코드 1 (봉인 전 실측)
  음성 대조: 알려진 답 복제본에서 ② 와 ③ 의 자리를 맞바꾼 사본 → `MISSING order(no ③)` · 종료 코드 1, 바꾸지 않은 사본 → `missing=0` · 종료 코드 0 (봉인 전 실측)

## Script

- [ ] 스크립트-00: N/A (이번 스프린트는 스크립트 · 검사를 만들거나 고치지 않는다 — 바꾸는 파일은 `## 범위 경계` 목록의 md · HTML 뿐. 측정: `git diff --name-only 279085a3..HEAD -- scripts '*.py' '*.sh' '*.js' ':(exclude).harness'` 가 빈 출력)

## Error

- [ ] 오류-01: 새로 더한 글의 영어 원문 인용이 대조 파일 글자 그대로다 — 이번 구간(`279085a3..HEAD`)에 더한 줄(`git diff -U0` 의 `+` 줄, HTML 은 태그를 벗긴 보이는 글)에서 「」 · “” · "" 로 감싼 영어 인용(영어 낱말 넷 이상 · 한글 없음)을 모두 모아, 하나하나가 `ex/A8.md` · `ex/A10.md` · `ex/A12.md` 를 이어 붙인 글(백틱 뺌 · 빈칸 정리)에 글자 그대로 있고, `## 배경` 의 인용 아홉이 모두 그 모음에 있다. 대상 파일은 `## 범위 경계` 목록의 열한 개다. Given 공통 전제 G, When `m 오류-01`, Then `bad=0 need_missing=0` · 종료 코드 0 [exact, enumerated]
  측정: `m 오류-01`. 시작 판 `quotes=0 bad=0 need_missing=9 ex_len=23040` · 종료 코드 1 (봉인 전 실측). 알려진 답: 복제본에 아홉 인용을 넣은 판 → `quotes=9 bad=0 need_missing=0` · 종료 코드 0
  양성 대조: 같은 복제본에서 `database.md` 의 RFC 인용 한 낱말을 `relationship` → `relation` 으로 바꾼 사본 → `BAD docs/backend/fundamentals/database.md: All times expressed have a stated relation …` · `bad=1` · 종료 코드 1 (봉인 전 실측)
- [ ] 오류-02: 기존 동작이 그대로다 — (a) `onboarding-kit/skills/setup-guide/SKILL.md` 의 가이드 게이트 코드 블록(`# Guide Conformance Gate` 로 시작하는 `bash` 울타리 안)이 시작 판과 글자까지 같고, (b) 시작 판 블록과 새 블록을 각각 `guide_gate docs/onboarding-kit/examples/fcm-ios-setup-guide.md flutter` 로 돌린 출력이 같고 둘 다 종료 코드 0 · `GATE_PASS` 이며, (c) 이웃 규칙 줄 넷 — plan-prd `14. **` 줄 · backend-system `18. **` 줄 · audit-criteria `| 시각 종류별 저장 |` 줄 · setup-guide `### Gotcha 9:` 줄 — 이 시작 판과 같다. Given 공통 전제 G, When `m 오류-02`, Then `gate_rc=0,0 gate_tail=[GATE_PASS]` · `checks=6 missing=0` · 종료 코드 0 [exact, enumerated]
  측정: `m 오류-02`. 시작 판 자기 대조 `gate_rc=0,0 gate_tail=[GATE_PASS] checks=6 missing=0` · 종료 코드 0 (봉인 전 실측)
  양성 대조: 알려진 답 복제본에서 게이트의 `grep -c` 를 `grep -ci` 로 바꾼 사본 → `MISSING gate_block_same` · 종료 코드 1 (봉인 전 실측)

## Architecture

- [ ] 구조-01: 데이터베이스 원칙 10 과 그 쪽이 벽시계 문자열 모양과 인용 둘을 싣는다 — `docs/backend/fundamentals/database.md` 의 `### 10.` 절(다음 `###` 머리 · `---` 앞까지)과 `docs/backend-kit/database.html` 의 보이는 글 각각에 `YYYY-MM-DDTHH:mm:ss[.fraction]` · `type: string` · `pattern` · `example` · RFC 3339 인용 · ISO 인용(`## 배경` 규칙 ①) · `이 킷이 고른 형식` 일곱이 있다. Given 공통 전제 G, When `m 구조-01`, Then `checks=14 missing=0` · 종료 코드 0 [exact, enumerated]
  측정: `m 구조-01`. 시작 판 `checks=14 missing=13` (HTML 쪽 `pattern` 만 이미 있음) · 종료 코드 1 (봉인 전 실측)
- [ ] 구조-02: PRD 원칙 문서와 그 쪽이 경계를 싣는다 — `docs/planning/prd-patterns.md` 에 `ADR` 이 든 `###` 머리가 하나 이상 있고, 그 파일과 `docs/planning-kit/prd-patterns.html` 의 보이는 글 각각에 `## 배경` 규칙 ② 의 인용 셋과 `원문에 직접 근거가 없는 추론` 이 있다. Given 공통 전제 G, When `m 구조-02`, Then `checks=9 missing=0` · 종료 코드 0 [exact, enumerated]
  측정: `m 구조-02`. 시작 판 `checks=9 missing=9` · 종료 코드 1 (봉인 전 실측)
- [ ] 구조-03: 셋업 가이드 쪽과 형식 목록 쪽이 두 날짜 규칙을 싣는다 — `docs/onboarding-kit/setup-guide.html` 보이는 글에 `Last updated` · `조회일을 바꾸지 않는다` · `이 킷의 규칙` 이 있고, `docs/onboarding-kit/format-checklist.html` 보이는 글에 `**출처:** <` 로 시작해 `>` 로 닫는 틀 안에 `조회 YYYY-MM-DD` 와 `Last updated` 가 이 차례로 있다. Given 공통 전제 G, When `m 구조-03`, Then `checks=4 missing=0` · 종료 코드 0 [exact, enumerated]
  측정: `m 구조-03`. 시작 판 `checks=4 missing=4` · 종료 코드 1 (봉인 전 실측)
- [ ] 구조-04: 셋업 가이드 쪽 Gotchas 목록이 10 항목이다 — `docs/onboarding-kit/setup-guide.html` 의 `aria-labelledby="gotchas-title"` 절에서 `<li><span class="check">N</span>` 번호가 정확히 1 ~ 10 차례이고, 10 번 항목 보이는 글에 스킬-04 와 같은 ①~⑤ 차례 · 자리 낱말과 인용 「We recommend that you avoid using service account keys whenever possible.」 이 있으며, 그 절의 설명 글에 `10개 체크` 가 있고 `9개 체크` 가 없고, `aria-labelledby="final-title"` 끝 체크리스트 보이는 글에 `서비스 계정 키` 와 `Last updated` 가 있다. Given 공통 전제 G, When `m 구조-04`, Then `gotcha_items=1,2,3,4,5,6,7,8,9,10` · `checks=7 missing=0` · 종료 코드 0 [exact, enumerated]
  측정: `m 구조-04`. 시작 판 `gotcha_items=1,2,3,4,5,6,7,8,9` · `checks=7 missing=7` · 종료 코드 1 (봉인 전 실측)
- [ ] 구조-05: 드리프트 도구가 원본 · 쪽 넷을 짝짓고 짝의 쪽이 모두 같은 구간에서 바뀌었다 — Given 공통 전제 G, When `python3 scripts/detect-docs-drift.py --since 279085a3` 를 돌리면, Then 화살표 `→` 가 든 줄이 정확히 아래 넷(차례 무관)이고 `[NEW` 표지 0 · 종료 코드 0 이며, `git diff --name-only 279085a3..HEAD` 의 `docs/**/*.html` 이 정확히 오른쪽 네 쪽이다(다른 쪽은 바뀌지 않는다): `docs/backend/fundamentals/database.md → docs/backend-kit/database.html` · `docs/planning/prd-patterns.md → docs/planning-kit/prd-patterns.html` · `onboarding-kit/skills/setup-guide/SKILL.md → docs/onboarding-kit/setup-guide.html` · `onboarding-kit/skills/setup-guide/references/format-checklist.md → docs/onboarding-kit/format-checklist.html` [exact, enumerated]
  측정: `m 구조-05`. 시작 판 `pairs=0 drift_rc=0 new_marks=0` · `pages_changed=[]` · 종료 코드 1 (봉인 전 실측). 알려진 답: 네 원본과 네 쪽을 고쳐 폴더별로 커밋한 복제본 → `pairs=4` · `pages_changed` 네 쪽 · 종료 코드 0
  양성 대조: 같은 복제본에서 `docs/onboarding-kit/format-checklist.html` 만 고치지 않고 커밋한 사본 → `pages_changed` 세 쪽 · 종료 코드 1 (봉인 전 실측 — 원본만 바꾸고 쪽을 안 맞춘 경우를 잡는다)
- [ ] 구조-06: 바뀐 쪽 넷이 넘치지 않고 접근성 검사를 통과한다 — 구조-05 의 네 쪽을 두 테마(`dark` · `light`)로 고정해 320 · 375 · 1280 폭에서 잰 가로 넘침(`scrollWidth - clientWidth`)이 모두 0 이고(`node .harness/.meta/after-0929-final-sweep-docs/br.js paint <테마> <쪽...>` 의 `of=0/0/0`), `node scripts/check-docs-a11y.js <네 쪽>` 이 네 줄 모두 `OK` · 종료 코드 0 이다. 공통 CSS 링크 하나는 진단-05 의 `check-docs-common-css.py` 가 잰다. Given 공통 전제 G, When `m 구조-06`, Then `pages=4 bad=0 br_rc=0,0 a11y_ok=4/4 a11y_rc=0` · 종료 코드 0 [exact, enumerated]
  측정: `m 구조-06`. 시작 판 `pages=4 bad=0 br_rc=0,0 a11y_ok=4/4 a11y_rc=0` · 종료 코드 0 (봉인 전 실측 — 지금 통과 중이고 깨지지 않아야 한다)
  양성 대조: 알려진 답 복제본의 `docs/planning-kit/prd-patterns.html` `<body>` 바로 뒤에 폭 2000px 상자를 넣은 사본 → `BAD dark … of=1680/1625/720` · `BAD light …` · `bad=2` · `a11y_ok=3/4` · 종료 코드 1 (봉인 전 실측)
- [ ] 구조-07: 기록 — `.harness/.meta/after-kaizen-0928/nr-notes.md` 에 (a) 규칙 넷(`시각 문자열` · `ADR` · `조회일` · `서비스 계정`)마다 처리 커밋 해시(서로 다른 8 자리 16 진수 넷 이상), (b) `tone-kit:tone-guide` 1 단계와 5 단계를 돌린 결과(새로 쓴 한국어 글이 대상), (c) `남긴 것` — 이 묶음 밖으로 남긴 일(`## 범위 경계` 「하지 않는 것」)이 있다. Given 공통 전제 G, When `m 구조-07`, Then 여섯 낱말 수가 모두 1 이상 · `hashes` 4 이상 · 종료 코드 0 [exact, enumerated]
  측정: `m 구조-07` (낱말 `시각 문자열` · `ADR` · `조회일` · `서비스 계정` · `tone-guide` · `남긴 것` 을 세고 서로 다른 8 자리 16 진수를 센다). 시작 판 파일 없음 · 모두 0 · 종료 코드 1
- [ ] 구조-08: 커밋 규칙 — `279085a3..HEAD` 의 커밋마다 합침 커밋이 아니고, 맨 위 폴더가 하나이며(문서 사이트 · 원칙 문서는 `docs/<폴더>` 하나 — `docs/backend` 와 `docs/backend-kit` 은 다른 폴더), `.harness/` 파일은 구현 파일과 다른 커밋이고, 서명 줄(`git log -1 --format='%(trailers:key=Co-Authored-By,valueonly)'`)이 `Claude … <noreply@anthropic.com>` 모양이며, 바뀐 파일이 모두 `## 범위 경계` 의 `# sprint-scope` 목록(또는 `.harness/`) 안이다. Given 공통 전제 G, When `m 구조-08`, Then 모든 줄 `OK` · `bad=0` · 종료 코드 0 [exact]
  측정: `m 구조-08`. 시작 판 `commits=0 bad=0 scope_entries=0` · 종료 코드 1 (계약 저장 전 실측 — 봉인 뒤에는 `scope_entries=11`)

## Anti-patterns

- [ ] 금지-02: force push 금지 (측정: 이 스프린트는 push 하지 않는다 — `git reflog show chore/ak3-nr` 에 `forced-update` 0 줄)
- [ ] 금지-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수 (측정: `python3 scripts/validate-plugin.py --check=code-fence` 종료 코드 0, 그리고 바뀐 md 여덟 파일에 markdownlint MD040 0 건 — 진단-02 와 같은 명령)
- [ ] 금지-04: SKILL.md frontmatter 에서 name 필드 누락 금지 (측정: `python3 scripts/validate-plugin.py --check=frontmatter` 종료 코드 0 — 이번에 SKILL.md 셋을 고친다)

## Reusability

- [ ] 재사용-01: 다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다 (측정: 규칙 본문은 킷 원본 한 곳에 두고 짝 쪽은 그 원본을 옮긴다 — 구조-05 의 짝 넷. 새 파일을 만들지 않는다: `git diff --name-only --diff-filter=A 279085a3..HEAD -- . ':(exclude).harness'` 가 빈 출력)
- [ ] 재사용-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다 (측정: 규칙 ① 은 기존 원칙 10 · Gotcha 15 · Timestamp 행에, 규칙 ② 는 기존 plan-prd Gotcha 목록과 §폐기한 결정 옆에, 규칙 ③ 은 기존 §출처 원장과 출처 줄 틀에 더한다 — 스킬-01 · 스킬-02 · 스킬-03 이 그 자리를 잰다. 넘침 측정은 fs2 의 `br.js` 를 그대로 부른다 — 구조-06)

## Diagnostics

- [ ] 진단-01: N/A (commands.analyze 는 scripts/release.sh 만 잰다 — 이번 변경 파일과 교집합 0 개. 측정: git diff --name-only 279085a3..HEAD | grep -c '^scripts/release.sh$' 이 0)
- [ ] 진단-02: IDE diagnostics 워닝/인포 0개 ([] 제외) — 바뀐 md 여덟 파일(`## 범위 경계` 목록의 md 일곱과 `.harness/.meta/after-kaizen-0928/nr-notes.md`)이 markdownlint-cli2(MD013 끔)로 경고 0 건이고 파일마다 검사기가 돈 줄 `Linting: 1 file` 이 있다
  측정: 파일마다 `<scratch>/mdl/node_modules/.bin/markdownlint-cli2 --config <scratch>/nr/mdl.jsonc <파일> 2>&1 | grep -cE ' MD[0-9]{3}'` 이 0 이고 같은 출력에 `Linting: 1 file` (설정 파일 내용 `{ "config": { "MD013": false } }`). 시작 판 일곱 파일 모두 `warn=0 ran=1` (봉인 전 실측). 양성 대조는 fs2 계약 진단-02 와 같은 검사기 · 설정이다(`#bad` 제목과 빈 줄 셋 사본 → 경고 4)
- [ ] 진단-03: N/A (commands.test 대상도 scripts/release.sh 라 이번 변경 파일에 없다. 측정: 진단-01 과 같은 명령)
- [ ] 진단-04: N/A (구동할 앱 · 서버가 없다 — 산출물은 규칙 문서 · 정적 쪽 · 기록. 측정: git diff --name-only 279085a3..HEAD -- . ':(exclude).harness' | grep -cvE '^(docs/|backend-kit/|planning-kit/|onboarding-kit/)' 이 0. 쪽을 브라우저로 여는 확인은 구조-06 이 한다)
- [ ] 진단-05: 로컬 CI 와 CI 파일에만 있는 단계가 모두 통과한다 — `bash /Users/jackson/Hub/10_Dev/claude-plugins/.harness/handoff/2026-09-26-tools/ci-local.sh <W>` (TMPDIR 은 scratch 아래 새 폴더)의 단계가 모두 `rc=0`(yq 없는 `feedback-agg-test SKIP` 만 예외)이고 `docs-a11y` 로그 끝이 `204/204 PASS`, 그리고 `python3 scripts/check-api-kit-docs.py` · `python3 scripts/detect-docs-drift.py --check-table` · `python3 scripts/test-detect-docs-drift.py` · `python3 scripts/check-docs-common-css.py` · `python3 scripts/test-check-docs-common-css.py` · `python3 scripts/check-cause-table-copies.py` · `python3 scripts/check-install-docs-guidance.py` · `python3 scripts/test-check-cause-table-copies.py` · `bash scripts/test-ci-local.sh` · `bash harness/evals/measure/measure-helpers-test.sh` · `bash harness/evals/superseded/check-superseded-test.sh` · `bash harness/scripts/check-superseded.sh .harness` · `bash bambu-kit/evals/run-gate-fixtures.sh` · `bash bambu-kit/evals/makerworld-fetch-test.sh` · `python3 scripts/sync-docs.py --check-only` · `python3 scripts/validate-plugin.py backend-kit` · `python3 scripts/validate-plugin.py planning-kit` · `python3 scripts/validate-plugin.py onboarding-kit` · `npx playwright test` 의 종료 코드가 모두 0 [exact, enumerated]
  측정: 위 명령들의 종료 코드와 `grep -c 'rc=0' <TMPDIR>/ci-local/summary.txt`. 시작 판 ci-local 25 단계 `rc=0` · `feedback-agg-test SKIP (yq 없음)` · `docs-a11y` `204/204 PASS`, CI 전용 단계 모두 0 (`12/12 PASS` · `어긋남 0` · `경우 3 개 중 통과 3` · `검사한 쪽 204 · 어긋난 쪽 0 · 못 읽은 쪽 0` · `경우 6 개 중 통과 6` · `checked=2 violations=0` · `need=0` · `실패 0 건` 넷 · `checked=6 violations=0` · `28 경우 중 불일치 0` · `5 경우 중 불일치 0` · `모든 README가 동기화 상태입니다.` · validate 세 킷 종료 코드 0), `npx playwright test` `172 passed` (봉인 전 실측)

## 범위 경계

- 이 계약이 고칠 경로는 아래 블록뿐이다. `.harness/` 아래(이 계약 · 기록 · 측정 묶음)는 늘 허용된다.

```text
# sprint-scope
backend-kit/skills/backend-system/SKILL.md
backend-kit/skills/backend-audit/references/audit-criteria.md
docs/backend/fundamentals/database.md
docs/backend-kit/database.html
planning-kit/skills/plan-prd/SKILL.md
docs/planning/prd-patterns.md
docs/planning-kit/prd-patterns.html
onboarding-kit/skills/setup-guide/SKILL.md
onboarding-kit/skills/setup-guide/references/format-checklist.md
docs/onboarding-kit/setup-guide.html
docs/onboarding-kit/format-checklist.html
```

- 하지 않는 것: 예제 가이드 `docs/onboarding-kit/examples/fcm-ios-setup-guide.md:358` 과 평가 사례 `evals.json:10,69` 는 이미 됨(`## GAP 분석`). 옛 기록 `docs/backend/research-log.md:17,71` · `docs/planning/research-log.md:22` 의 「규칙으로 올리지 않았다 / 고칠 곳이 없다」 는 그때의 기록이라 고치지 않는다. 새 규칙을 기계로 막는 새 검사는 만들지 않는다(스크립트-00) — 네 규칙은 글 규칙이고, 글이 제자리에 있는지는 이 계약의 도우미가 잰다. 킷 버전 올리기 · 릴리스 · 합치기 · push 는 이 묶음 밖이다. 남은 일 A10 의 둘째 몫 — `docs/planning/flows.md:61` 의 「최신 안정판」 문장에 Mermaid 버전 출처와 「렌더해 보지 않았다」 단서를 붙이는 일(`ex/A10.md` 교체안) — 은 이번 결정(규칙 넷)에 들지 않고, 그 파일을 고치면 드리프트 짝이 다섯이 되어 구조-05 와 부딪힌다. 그래서 이 묶음에서 하지 않고 `nr-notes.md` 의 `남긴 것` 에 이유와 함께 적는다(교차 진단 지적 반영). 스킬-01 · 스킬-02 는 Gotcha 줄 하나를 재므로 규칙 글은 그 줄 안에 이어 쓴다(교차 진단 지적).
- 커밋: `git add <경로>` 뒤 `git commit -o <경로>`. `git add -A` · `git stash` · push · 가지 바꾸기 금지. 메시지 한국어, 끝에 빈 줄 뒤 서명 줄 「Co-Authored-By: Claude Opus 5.5 (1M context) <noreply@anthropic.com>」. 킷 원본은 킷 폴더별, 원칙 문서 · 쪽은 `docs/<폴더>` 별로 커밋한다. 봉인 커밋(계약 파일 하나)과 측정 묶음 커밋(`.harness/.meta/after-0929-four-new-rules/`)은 따로다.

## 회귀 게이트 — 측정 도우미 · 봉인 전 실측

- 도우미 `m <조건 번호>` = `python3 .harness/.meta/after-0929-four-new-rules/measure.py <조건 번호>` (W 맨 위 폴더에서, 종료 코드 0 성립 · 1 불성립 · 2 잴 수 없음). 환경 변수 `NR_ROOT` 를 주면 그 폴더를 레포로 보고 잰다(대조용 복제본). 넘침은 fs2 묶음의 `.harness/.meta/after-0929-final-sweep-docs/br.js` `paint` 모드를 부른다.
- 파일 지문(봉인 전, `shasum -a 256 … | cut -c1-16`): `measure.py` 는 봉인 커밋 직전에 다시 뽑아 봉인 커밋 메시지에 적는다. `br.js` `01c706e939a85586`.
- 봉인 전 실측(2026-09-29, W 시작 판): 스킬-01 ~ 스킬-04 · 구조-01 ~ 구조-05 · 구조-07 · 구조-08 · 오류-01 은 종료 코드 1(결함 재현), 구조-06 · 오류-02 는 종료 코드 0(지금 성립하고 깨지지 않아야 한다). 값은 각 조건 측정 줄에 있다.
- 알려진 답 대조(봉인 전): W 를 scratch 에 복제해 `279085a3` 에서 네 규칙의 글자를 최소로 넣고 폴더별로 여덟 커밋 → 스킬-01 ~ 스킬-04 · 구조-01 ~ 구조-06 · 오류-01 · 오류-02 모두 종료 코드 0. 틀린 사본 셋(인용 한 낱말 바꿈 · ② ③ 자리 바꿈 · 쪽 하나 안 고침)은 각각 오류-01 과 구조-01 · 스킬-04 · 구조-03 과 구조-05 만 종료 코드 1. 넣기 스크립트와 실행 스크립트는 scratch `nr/apply_good.py` · `nr/known.sh` 이고 측정 묶음 폴더에 사본을 둔다.
- 도우미 결함 하나를 봉인 전에 고쳤다: 절 자르기가 머리 줄 첫 글자를 뺀 나머지에서 끝 머리를 찾아 `### Gotcha 10:` 절이 빈 글이 됐다(알려진 답 복제본에서 스킬-04 `missing=7`). 끝 머리는 머리 줄 다음 줄부터 찾게 고친 뒤 알려진 답을 다시 돌려 모두 0 을 봤다.
- 커버리지 해소: 스킬-01 · 스킬-02 · 스킬-03 · 구조-01 · 구조-02 · 구조-03 — 검출기가 낸 파일 경로는 측정 명령 `m <조건>` 이 여는 파일이다. 경로는 도우미 `PAGES` 와 각 `m_*` 함수에 글자 그대로 있고, 찾는 글자는 도우미 맨 위 상수(`SHAPE` · `Q_*` · `INFER` · `KEEP_DATE` · `KIT_RULE` · `ORDER`)와 `## 배경` 규칙 목록 한 곳에 있다. 스킬-02 의 `docs/planning/prd-patterns.md` 는 재는 파일이 아니라 Gotcha 줄에 있어야 할 글자다(`m 스킬-02` 가 찾는다). 검출기는 측정 줄의 백틱만 본다.
- 커버리지 해소: 구조-06 — `of=0/0/0` 은 기대 출력 값이고, `check-docs-common-css.py` 는 진단-05 가 재는 명령이라 구조-06 측정 대상이 아니다.
- 커버리지 해소: 오류-01 · 구조-05 · 구조-08 — 오류-01 의 `ex/A8.md` · `ex/A10.md` · `ex/A12.md` 와 구간 `279085a3..HEAD` 는 도우미 `EX` · `BASE` 상수다. 대상 파일 열한 개와 짝 넷은 `## 범위 경계` 블록과 도우미 `PAGES` 에 있고 `m` 출력이 줄마다 찍는다(목록을 두 번 적지 않는다).
- 커버리지 해소: 진단-05 — 명령마다 조건 글에 글자 그대로 있다. 검출기는 빈칸 든 백틱 덩어리를 건너뛴다.
- 오라클 해소: 스킬-01 ~ 스킬-04 · 구조-01 ~ 구조-04 — 규칙 글을 제자리에 적는 것 자체가 요구다. 그 자리를 줄 머리 · 절 머리로 고르고, 알려진 답 · 틀린 사본으로 도우미가 좋은 판과 틀린 판을 가르는 것을 봉인 전에 봤다.
- 오라클 해소: 진단-02 · 진단-05 — 글자 찾기가 아니라 markdownlint · CI 명령을 실제로 돌린 종료 코드 · 요약 줄로 판정한다. 오류-02 도 게이트 코드를 두 판에서 실제로 실행한다.
- 오라클 해소: 오류-01 — 인용을 대조 파일과 글자 단위로 맞대고, 한 낱말만 바꾼 사본이 잡히는 것을 봤다. 구조-05 — 드리프트 도구를 실제로 돌린 출력과 git 구간 차이로 판정한다. 구조-06 — 브라우저로 쪽을 열어 잰다. 오류-02 — 게이트 코드를 두 판에서 실제로 돌려 출력을 맞댄다.
