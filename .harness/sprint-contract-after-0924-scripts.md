---
feature: "2026-09-24 카이젠 뒤 scripts 검사 도구 후속 (c1a) — 회귀 패턴 실행기 · 배정표 번호 대응 · 감사 기록 도구 · hooks.json 따옴표와 V8 · sync-docs 표지와 루트 README 스킬 수"
slug: after-0924-scripts
created: "2026-09-26 12:11"
complexity: "복잡"
conditions: 30
status: active
owner_session: bda55d45-296c-491f-89ba-b52042d58e72
conditions_digest: sha256:e6e9d4a14f27da96
locked_at: "2026-09-26 12:27"
---

## 배경

- 사용자 위임 — 이 계약의 합의(sprint-contract Step 5)는 아래 두 지시로 받은 것으로 적는다. 사용자에게 따로 묻지 않았다.
  - user `2026-09-26T01:04:21.505Z` 「다음 세션에서 직접할 일을 다 실행하고 이어질것도 실행해」 — 세션 기록 `/Users/jackson/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/de8c7935-a5b6-4df5-9106-fafa73c288a0.jsonl`
  - user `2026-09-24T04:04:16.964Z` 「나한테 물어보지 말고 자동으로 끝까지」
  - 판단이 갈린 곳은 저장소 안 근거로 정하고 `## 범위 경계` 에 근거를 적었다. 저장소 밖 원문이 있어야 정할 수 있는 것은 넘긴다
- 묶음: 핸드오프 `.harness/handoff/2026-09-26-0110.md` §C1 의 scripts 검사 도구 쪽(c1a). 작업 폴더 `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak-c1`, 가지 `chore/ak-c1-harness-scripts`, 시작 판 `f81568d` (#110 릴리스).
- 계약을 쓰는 동안 origin/main 이 `88ddfe5` 로 움직였다 (#111 V10 코드 블록 판정 · #112 harness 0.14.1). 이 가지는 `f81568d` 위에만 쌓고 main 을 합치지 않는다 — main 반영은 QA 뒤 PR 단계에서 부모가 한다.
  스크래치 복제본에서 이 계약대로 만든 시험판에 `88ddfe5` 를 합쳐 보니 충돌 0 · `validate-plugin.py` 종료 코드 0 · `sync-docs.py --check-only` 종료 코드 0 이었다 (2026-09-26 12:0x).
- 구현 단계는 사용자 전역 규칙대로 tone-kit `tone-guide` 1 단계(규칙 불러오기)와 5 단계(완료 전 대조)를 거친다. 이 계약은 그 기록을 조건으로 재지 않는다.
- 사용자가 할 일: 없음

## 리서치 소스

저장소 안 기록만 썼다. 웹 조회 · 외부 문서 가져오기는 하지 않았다.

- `.harness/.meta/kaizen-0924/f1-harness-followups-notes.md` §다음 사이클 메모 — F1H-14 · F1H-56 · F1H-66 · F1H-79 · F1H-84 (그리고 넘기는 F1H-40 · F1H-94)
- `.harness/.meta/kaizen-0924/final-notes.md` §다음 사이클 메모 — FN-18 · FN-43 · FN-64 · FN-76 · FN-78, 같은 파일 「계약 밖 결함 2」(감시 목록)
- `.harness/.meta/kaizen-0924/f1-kit-followups-notes.md` 「고치지 않은 항목」 39 행 (hooks.json 따옴표 — 킷 넷을 V8 검사와 함께. V8 은 `scripts/validate-plugin.py` 의 여덟째 검사로, hooks.json 이 부르는 스크립트의 실행 권한을 본다)
- `.harness/.meta/kaizen-0924/f2-review-fixes-notes.md` §다음 사이클 메모 「Final: 루트 README 킷 절 스킬 수 · 목록을 AUTO 마커 안으로」
- `.harness/.meta/evidence/phase12.md:113` — shell 꼴 명령의 따옴표 없는 `${CLAUDE_PLUGIN_ROOT}` 를 낡은 곳으로 적고 권장 꼴로 「placeholder 를 이중 인용」 을 든다. 같은 파일 `:125` — 최신 검사기는 따옴표 없는 plugin-root hook 을 경고한다
- `.harness/.meta/kaizen-0924/phase12-notes.md:59` · `:89` — 킷 넷의 hooks.json 이 모두 같은 모양이라 한 킷만 바꾸지 않고, V8 에 검사를 두고 넷을 한 번에 고친다

## GAP 분석 · 개선안 초안

### 복잡도 4 축

| 축 | 물음 | 값 |
| -- | ---- | -- |
| 레이어 수 | 몇 계층을 지나는가 | 셋 — 검사 도구(`scripts/`) · 킷 설정(`hooks.json`) · 문서(README · 가이드) |
| 공개 계약 변경 | 밖에서 쓰는 모양이 바뀌는가 | 예 — 감사 기록 도구 새 옵션 `--watch`, 새 실행기 명령, hooks.json 명령 문자열, sync-docs 종료 코드(짝 없는 표지), V8 판정 |
| 소비면 존재 | 받아 쓰는 반대편이 있는가 | 예 — sync-docs 훅 표(hooks.json), V8 실행 비트 검사(hooks.json), CI(저장소에 올릴 때 자동으로 도는 검사 — `.github/workflows/ci.yml`), 오케스트레이터 Final 단계(감사 기록 도구), 카이젠 스킬 Step 7(회귀 패턴), release.sh(sync-docs) |
| 회귀 위험 | 멀쩡하던 게 다시 망가질 길이 있는가 | 예 — 따옴표를 붙이면 V8 이 실행 비트 검사를 조용히 건너뛴다(시작 판 실측), sync-docs 훅 표에 따옴표가 새어 나온다(시작 판 sync-docs 로 실측), 표지를 읽게 되면 킷 README 표가 다시 만들어진다 |

넷 다 「예」 이고 공개 계약 변경과 소비면이 함께 있어 **복잡** 이다. Counterpart 조건을 따로 둔다(SC-10 · AR-05).

### 설정 리터럴 대조표

| config key | project.yaml 에서 읽은 값 | 계약에 쓴 값 |
| ---------- | ------------------------- | ------------ |
| `commands.analyze` | `bash -n scripts/release.sh` | `bash -n scripts/release.sh` (DG-01 N/A — 바뀐 파일과 교집합 0) |
| `commands.test` | `bash scripts/release.sh 2>&1 \|\| true` | `bash scripts/release.sh 2>&1 \|\| true` (DG-03 N/A — 같은 까닭) |
| `diagnostics.ide_exclude` | `[]` | `[]` — 뺄 것 없음 (스펠체크는 사용자 규칙대로 뺀다) |
| `contract_categories[].id` / `prefix` | Skill/SK · Script/SC · Error/ER · Architecture/AR | 같음 |
| `anti_patterns[].id` / `message` | AP-01 버전 하드코딩 · AP-02 force push · AP-03 bare code fence · AP-04 frontmatter name | AP-01 · AP-02 · AP-03 (AP-04 는 바뀌는 SKILL.md · agents 가 0 개라 뺀다 — SK-00 측정) |

### 편집 전 감사 — 시작 판 `f81568d` 를 실제로 읽은 줄

| 대상 파일 | 읽은 증거 (`파일:줄`) | 찾은 빈틈 | 조건 |
| --------- | --------------------- | --------- | ---- |
| `scripts/run-evals.py` | `:32-35` 킷 목록 · `:54` `<킷>/evals/evals.json` 만 읽음 · `:118` type 은 `behavior` · `output` 만 | 카이젠 회귀 패턴 `assertions.json` 을 도는 곳이 없다 | SC-01 · SC-02 · ER-01 |
| `harness/evals/kaizen/contract-kaizen/assertions.json` | `:1-16` 키 넷 · 패턴 여섯 · 모두 `file_contains` | 형식: `{픽스처 이름: [{type, file, pattern}]}` · 픽스처 `fixture-feedback-data/<키>.yaml` 넷과 1:1 | SC-01 알려진 답 |
| `harness/evals/kaizen/evaluator-kaizen/assertions.json` | `:1-20` 키 다섯 · 패턴 여덟 · `silent-check` `:15-19` | 같은 형식 · 픽스처 다섯과 1:1 · 파이썬 `re.findall` 로 열넷 모두 1 건 이상(시작 판) | SC-01 · SC-02 |
| `.github/workflows/ci.yml` | `:46-47` `run-evals.py --verbose` · `:87` · `:94` 「evals.json 규칙 밖이라 run-evals.py 가 읽지 않는다」 | 회귀 패턴 단계 없음 | SC-03 |
| `scripts/check-insights-tracking.py` | `:21` `SLUG` 형식 정규식 · `:131-132` 형식만 판정 | Phase 6 행에 Phase 5 슬러그를 적어도 통과 (시작 판 사본 실측 — `SC04b rc=0`) | SC-04 |
| `scripts/append-audit-log.py` | `:148` · `:159` · `:171` 고정 소제목 · `:173-178` 감시 목록이 실패 목록에서만 · `:269-272` 끝 빈 줄 없이 붙임 | 같은 제목 경고(MD024) · 머리 앞 빈 줄 없음(MD022 · MD032) · 수동 감시 거리를 못 받음 | SC-05 · SC-06 |
| `.harness/.meta/orchestrator-audit-log.md` | `:220` `:224` `:228` 와 `:507` `:511` `:515` 같은 소제목 · `:517` 「특별 감시 대상 없음」 | 도구 생성 항목이 겹친다. 기록은 덧붙이기만 하므로 이번에 고치지 않는다 | SC-05 (d) · AR-04 |
| `design-kit/hooks/hooks.json` · `flutter-toolkit/hooks/hooks.json` · `harness/hooks/hooks.json` · `reflect-kit/hooks/hooks.json` | `design-kit:8` · `flutter-toolkit:9` · `harness:8` `:21` `:31` `:41` `:53` · `reflect-kit:8` `:19` `:30` | 명령 열 개 모두 `${CLAUDE_PLUGIN_ROOT}` 가 따옴표 밖 — 빈칸 든 설치 경로에서 열 개 모두 실행 실패(시작 판 실측 `ran_env=0/10`). 킷 넷은 `find` 로 hooks.json 을 전부 찾아 정했다 | SC-07 |
| `scripts/validate-plugin.py` | `:626-716` V8 · `:632` 스크립트 경로 정규식 · `:641-649` 첫 토큰 판정 | 따옴표를 붙이면 앞 글자가 `"` 라 직접 실행으로 안 보고 실행 비트 검사를 건너뛴다(시작 판 사본 `SC08d` 「직접 실행 hook 스크립트 없음」) · 따옴표 검사 자체가 없다 | SC-08 |
| `harness/docs/guides/plugin-validation-guide.md` | `:391` `### V8` · `:397` · `:401` · `:409` 예시가 모두 따옴표 없는 꼴 · `:418` `### V9` | 따옴표 규칙 서술 없음 | SC-09 |
| `scripts/sync-docs.py` | `:37-40` 표지 정규식 · `:134` 훅 표 이름을 `/` 뒤 글자로 자름 · `:355-357` 없는 표지는 경고만 | `:start` · `:end` 꼴과 닫는 표지를 여는 꼴로 쓴 README 를 못 읽고 조용히 「동기화됨」 · 따옴표 붙은 명령이면 훅 표에 `.sh"` 가 샌다(시작 판 sync-docs 로 실측 — design-kit · reflect-kit README 「변경 필요」) | SC-10 · SC-11 · ER-02 |
| `onboarding-kit/README.md` · `planning-kit/README.md` · `rust-kit/README.md` | `onboarding-kit:13` `:17` · `planning-kit:13` `:28` `:32` `:36` (`AUTO:<키>:start/end`) · `rust-kit:9` `:30` `:32` `:38` (닫는 표지도 `<!-- AUTO:<키> -->`, 여는 표지가 `## 스킬` · `## 에이전트` 제목 위) | 셋 다 sync-docs 가 못 읽는다. rust-kit 은 F1H-66 목록 밖에서 같은 결함을 새로 찾았다 | SC-11 |
| `README.md` | `:136-146` harness 표 일곱 줄(실제 스킬 아홉) · `:157` 「스킬 20종」 · `:162` 목록 · `:195` 「17종」(스킬 16 + 에이전트 1) · `:204` 「21종 + 3 에이전트」 · 구조 절 `:256` 「7종」 `:264` `:285` `:291` | 스킬 수 · 목록이 AUTO 밖이라 아무도 세지 않는다. harness 는 이미 어긋났다 | SC-12 |
| `scripts/check-stale-values.py` · `.harness/stale-values.yaml` | `:45` `EXCLUDED_KITS: dict[str, str] = {}` · `:20` `:22` `:24` backend-kit allow 셋 | 이미 반영 — 커밋 `72d6ddd` (f2-review-fixes). 할 일 없음 | 넘김 (AR-05) |

구현 방식 후보가 둘 이상인 곳과 정한 것:

| 자리 | 후보 | 정한 것 · 근거 |
| ---- | ---- | -------------- |
| 회귀 패턴 실행기 | `run-evals.py` 에 모드 추가 / 새 파일 | 새 파일 `scripts/run-kaizen-assertions.py`. 입력 형식(킷별 `evals.json` 대 카이젠 스킬별 `assertions.json`)과 받는 쪽(CI 킷 평가 대 카이젠 Step 7)이 달라 한 파일에 섞으면 기존 `run-evals.py` 출력(`Total: 115 passed`)이 흔들린다. 저장소 뿌리는 `run-evals.py:30` 처럼 `plugin_utils` 에서 받는다(RE-02) |
| 표지 읽기 | 정규식이 `:start/:end` 도 읽게 / README 표지를 표준 꼴로 | 조건은 결과만 잰다([goal] 성격) — 어느 쪽이든 된다. rust-kit 꼴(닫는 표지 = 여는 꼴)은 정규식으로 안전하게 못 읽으니 README 쪽을 고친다 |
| 감사 기록 수동 감시 입력 | JSON 파일 옵션 / 글 옵션 여러 번 | `--watch "<글>"` 여러 번. 기존 `--manual-edits <file>` 은 경로가 틀리면 빈 목록으로 조용히 넘어간다(`append-audit-log.py:117-119`, Final 계약 AR-07 실측) — 글 옵션은 그 길이 없다 |
| 루트 README 스킬 블록 | 킷마다 표 / 한 줄 목록 | 구현이 정한다. 조건은 블록 안에 `스킬 N종` · `에이전트 M종` · 스킬 폴더 이름 전부가 있는지만 잰다 |

### Counterpart — 바뀌는 모양을 받아 쓰는 반대편

| 바뀌는 것 (producer) | 받는 쪽 (consumer) | 조건 |
| -------------------- | ------------------ | ---- |
| hooks.json 명령 문자열 (SC-07) | `scripts/sync-docs.py` 훅 표 · `design-kit/README.md` · `reflect-kit/README.md` | SC-10 |
| hooks.json 명령 문자열 (SC-07) | `scripts/validate-plugin.py` V8 실행 비트 검사 | SC-08 (a)(d) |
| V8 판정 (SC-08) | `harness/docs/guides/plugin-validation-guide.md` §3.8 | SC-09 |
| V8 판정 · 가이드 (SC-08 · SC-09) | `docs/harness/plugin-validation.html` (docs 페이지 — 이 묶음 범위 밖) | 명시적 미완 — AR-05 notes |
| 감사 기록 도구 `--watch` (SC-06) | `.claude/skills/kaizen-orchestrator/SKILL.md` Final 단계 호출 줄 (범위 밖) | 명시적 미완 — AR-05 notes |
| 회귀 패턴 실행기 (SC-01) | `harness/skills/contract-kaizen/SKILL.md` · `harness/skills/evaluator-kaizen/SKILL.md` Step 7 (범위 밖) | 명시적 미완 — AR-05 notes |
| 회귀 패턴 실행기 (SC-01) | `.github/workflows/ci.yml` | SC-03 |
| sync-docs 짝 없는 표지 종료 코드 (ER-02) | `scripts/release.sh:126` · `scripts/validate-post-kaizen.py:252` · `.claude/settings.json:31` | SC-11 (a) 끝 판 종료 코드 0 · SC-12 (c) 쓰기 모드 종료 코드 0 — 끝 판에 짝 없는 표지 0 |
| 처리 배정표 검사기 판정 (SC-04) | 오케스트레이터 Final 단계 (`--final` 호출, 이미 있음) | SC-04 (a) 지금 배정표 그대로 종료 코드 0 |

### 조건 작성 자문 (contract-schema §조건 작성 preflight 의 열 태그)

- `측정-수단-부재` · `측정-산출물-부재` — 모든 조건이 `## 회귀 게이트` 의 도우미 명령으로 잰다. 끝 판을 `git archive` 로 풀어 거기서 재므로 작업 폴더 상태가 끼지 않는다
- `측정-상태-모호` · `측정-환경-오염` — 공통 전제 하나: 가지 끝이 이 계약 구현 커밋을 다 담고 main 을 합치지 않은 상태. `common.sh` 가 병합 커밋을 보면 `END_HAS_MERGE` 로 멈춘다
- `측정-방식-불일치` — 파일 이름 · 명령 글자는 산문과 측정에 같은 표기로 적었다
- `범위-미명시` — 킷 넷 · 파일 열다섯 · README 셋 · 루트 README 네 절을 모두 이름으로 적었다
- `태그-산출물-불일치` — 새 파일은 실행기와 notes 둘뿐이고 둘 다 조건이 이름으로 요구한다
- `증거-경로-부재` — 합의 근거는 세션 기록 경로와 시각을 적었다(위 배경). notes 경로는 AR-05

### 개선안 초안 (구현 차례)

1. 킷마다 한 커밋 — `design-kit/hooks/hooks.json` · `flutter-toolkit/hooks/hooks.json` · `reflect-kit/hooks/hooks.json`, 그리고 harness 커밋 하나(`harness/hooks/hooks.json` + 가이드 §3.8 문단). 명령 안 `${CLAUDE_PLUGIN_ROOT}/…` 경로를 큰따옴표로 감싼다 (JSON 안에서는 `\"`)
2. `scripts/validate-plugin.py` V8 — 따옴표 붙은 경로도 직접 실행으로 알아보고, 따옴표 밖 `${CLAUDE_PLUGIN_ROOT}` 가 든 명령을 FAIL 로 (V8 함수 안에서만)
3. `scripts/sync-docs.py` — 훅 표 이름에서 따옴표를 뺀다 · 세 킷 README 표지를 읽게 · 짝 없는 표지는 이름을 찍고 종료 코드 0 아님 · 루트 README 네 킷 절 블록을 채운다. 같은 커밋에 루트 `README.md` (블록 자리 · 블록 밖 스킬 수 글자 지우기). 킷 README 셋은 킷마다 따로 커밋
4. `scripts/run-kaizen-assertions.py` 새로 · `.github/workflows/ci.yml` 한 단계 · `scripts/check-insights-tracking.py` · `scripts/append-audit-log.py`
5. notes `.harness/.meta/after-kaizen-0926/c1a-notes.md`

## 범위 경계

입력 항목마다 처리:

| # | 항목 (근거 ID) | 처리 | 조건 |
| - | -------------- | ---- | ---- |
| 1 | `assertions.json` 회귀 패턴 실행기 · CI 등록 (F1H-14 · F1H-84 · FN-18 · FN-43) | 계약에 넣음. 단 `silent-check` 패턴 둘이 제목 글자만 본다는 FN-18 뒷부분은 `harness/` 안 파일이라 넘긴다 | SC-01 · SC-02 · SC-03 · ER-01 · RE-01 · RE-02 |
| 2 | 배정표 검사기 번호 ↔ 슬러그 (FN-76) | 계약에 넣음 | SC-04 |
| 3 | 감사 기록 도구 MD024 · 끝 빈 줄 · 수동 감시 거리 (FN-78 · Final 교차 진단 계약 밖 2) | 계약에 넣음. 기록 파일 자체는 덧붙이기만이라 이번에 고치지 않는다 | SC-05 · SC-06 · AR-04 |
| 4 | 킷 넷 hooks.json 따옴표 · V8 (F1H-56 · f1-kit 39 행) | 계약에 넣음. V6 · V10 범위 결정(F1H-40 · F1H-94)은 넘긴다 | SC-07 · SC-08 · SC-09 · SC-10 · AR-02 |
| 5 | sync-docs 표지 (F1H-66) · 루트 README 스킬 수 (f2) | 계약에 넣음. rust-kit README 를 더했다(같은 결함, 새로 찾음) | SC-11 · SC-12 · ER-02 |
| 6 | 옛 값 검사 backend-kit 해제 · allow 세 줄 (F1H-79 · FN-64) | 넘김 — 이미 반영 (`72d6ddd`, `scripts/check-stale-values.py:45` · `.harness/stale-values.yaml:20-24`) | AR-05 (notes 에 적음) |

판단이 갈린 곳 — 저장소 안 근거로 정했다:

- **`harness/hooks/hooks.json` 을 고친다.** 묶음 지시는 `harness/` 아래를 범위 밖으로 두면서 항목 4 에서 「킷 넷 hooks.json」 을 실측으로 정하라고 한다. 실측 넷에 harness 가 든다.
  `phase12-notes.md:59` 「한 킷만 바꾸지 않는다」 · `:89` 「넷을 한 번에 고친다」, 그리고 V8 이 따옴표 없는 명령을 FAIL 로 내면 harness 만 남겨 둘 때 CI 가 멈춘다. 그래서 harness 에서는 이 파일 하나와 가이드 V8 문단만 고친다(AR-01 · AR-02)
- **rust-kit README 를 더한다.** F1H-66 은 둘만 적었지만 같은 결함이 rust-kit 에도 있고(`rust-kit/README.md:30` 닫는 표지가 여는 꼴), 짝 없는 표지를 알리게 하면 rust-kit 이 걸린다
- **bambu-kit 「도구형 1스킬 킷」 은 그대로 둔다.** 스킬 수가 아니라 킷 유형 이름이다(`README.md:236` · 루트 `CLAUDE.md` 도 같은 말). SC-12 정규식은 `종` 으로 끝나는 수만 센다
- **가이드 머리 설정 판 번호 · 변경 이력 표는 이 가지에서 고치지 않는다.** main 이 이미 `1.4.1` 로 올렸고(#111) 같은 줄을 이 가지가 고치면 합칠 때 충돌한다. main 을 합친 뒤 판 번호 · 이력 한 줄 · 문서 페이지를 부모가 채운다(notes)
- **봉인 전 교차 진단(qa-evaluator) 반영.** 지적 넷을 이렇게 처리했다 — (1) DG-05 측정 도구가 커밋 안 된 파일이라는 점: 조건에 봉인 시점 지문과 「없거나 다르면 `run:` 줄을 하나씩」 을 정상 경로로 적었다 (2) harness 파일 하나를 범위에 넣는 결정은 사용자 확인을 권했으나, 배경의 위임(묻지 말고 끝까지)대로 묻지 않고 위 근거로 정했다 — notes 에 남긴다 (3) SC-09 쓰기 주의를 조건 괄호에 적었다 (4) AR-02 줄 번호가 시작 판 쪽이라 밀리지 않는다는 점을 조건 괄호에 적었다
- **notes 경로.** 묶음 지시가 정한 `.harness/.meta/after-kaizen-0926/c1a-notes.md` 로 맞췄다(봉인 전). 다른 묶음 notes 와 한 폴더에 모이게 하려는 부모 쪽 규칙이다
- 오라클 해소: RE-02 — 이 조건은 재사용 여부(새로 만들지 않았는가)를 재는 구조 조건이라 글자 세기가 맞는 측정이다. 동작은 같은 코드를 실제로 부르는 SC-01 · RE-01(실행기) · SC-11 · SC-12(sync-docs) · SC-04(배정표 검사기)가 잰다

범위 밖 — 이 묶음은 건드리지 않는다 (AR-01 의 정확한 목록이 막는다): `.claude/skills/` 아래 전부 · 위 두 파일 말고 `harness/` 아래 전부 · `scripts/detect-docs-drift.py` · `scripts/sync-orchestrator.py` · `docs/` 페이지 · 루트 `CLAUDE.md` · 버전 파일(`plugin.json` · `marketplace.json`).

커밋 규칙: `git add <경로>` 뒤 `git commit -o <경로>` · 한 커밋에 킷 하나(킷 폴더를 건드린 커밋은 그 킷 폴더만) · `git add -A` · `git stash` · 푸시 · 가지 바꾸기 금지 · 이 가지에 main 을 합치지 않는다. 이 가지는 한 주체만 커밋하므로 서명 줄은 쓰지 않고 누적 차이로 잰다(contract-schema 선택지 A).

넘길 것 — 구현이 notes `.harness/.meta/after-kaizen-0926/c1a-notes.md` 에 적는다 (AR-05 가 글자로 잰다):

- 항목 6 은 이미 반영 — `72d6ddd`
- 오케스트레이터 Final 단계가 수동 감시 거리를 `--watch` 로 넘기게 — `.claude/skills/kaizen-orchestrator/SKILL.md` (다른 묶음 몫)
- 카이젠 Step 7 이 새 실행기 명령을 부르게 — `harness/skills/contract-kaizen/SKILL.md` · `harness/skills/evaluator-kaizen/SKILL.md`
- `harness/evals/kaizen/evaluator-kaizen/assertions.json` 의 `silent-check` 패턴이 제목 글자만 본다 (FN-18 뒷부분)
- V6 · V10 범위 결정 — F1H-40 · F1H-94
- main(`feat/v10-fence-commonmark` 가 합쳐진 판)을 합친 뒤 `plugin-validation-guide.md` 판 번호 · 변경 이력 한 줄, 그리고 `docs/harness/plugin-validation.html` 다시 만들기
- `reflect-kit/README.md:156` · `:159` · `:162` 의 `bash ${CLAUDE_PLUGIN_ROOT}/scripts/install-scheduler.sh` 예시도 따옴표가 없다 — hooks.json 밖이라 이번 범위 밖
- 릴리스할 킷 — hooks.json 이 바뀐 harness · design-kit · flutter-toolkit · reflect-kit, README 만 바뀐 onboarding-kit · planning-kit · rust-kit (README 만 바뀐 셋은 다음 릴리스에 묶어도 된다)

커버리지 해소 (Step 6.5 (4) 검출기 출력 몫):

- 커버리지 해소: SC-01 — 아홉 짝은 `asr.sh` 의 `for kp in …` 목록이 글자 그대로 담고, 두 파일은 `KZ` 변수와 SC-02 · ER-01 의 사본 명령이 잰다. `harness/evals/kaizen/*/assertions.json` 은 실행기가 찾는 범위를 적은 것이고 측정은 그 두 파일의 패턴 열넷으로 잰다
- 커버리지 해소: SC-10 — 두 README 는 `sdocs.sh` 의 `for f in design-kit/README.md reflect-kit/README.md` 와 뒤따르는 파이썬 블록이 잰다
- 커버리지 해소: SC-11 — 세 README 는 `sdocs.sh` 의 `("onboarding-kit", "planning-kit", "rust-kit")` 와 `need` 호출 셋, 제목 줄은 마지막 `h(…)` 다섯이 잰다
- 커버리지 해소: SC-12 — 스킬 · 에이전트 수는 `sdocs.sh` 의 `skills()` · `agents()`, 루트 README 는 `check()`, 가짜 스킬은 `fresh mc` 블록, sync-docs 는 `SD` 변수가 잰다
- 커버리지 해소: AR-04 — 세 공유 파일은 `scope.sh` 의 `for f in …` 목록, `.harness` 경로 규칙은 `hx=` 정규식, 계약 봉인은 `find … sprint-contract*.md` 가 잰다
- 커버리지 해소: AR-05 — 열세 글자는 `scope.sh` 의 `TOK` 배열, notes 경로는 `common.sh` 의 `NOTES` 가 잰다
- 커버리지 해소: DG-02 — 마크다운 다섯은 `dg.sh` 의 `MDS`, 파이썬 다섯은 `PYS`, hooks.json 넷과 CI 파일은 그 아래 두 줄이 잰다

## 회귀 게이트 — 측정 공통 정의 · 도우미 · 봉인 전 실측

모든 측정은 **bash** 에서 돈다(zsh 는 따옴표 없는 변수를 쪼개지 않는다). 공통 정의 `common.sh` 를 읽은 도우미가 두 판(시작 판 `B` · 끝 판 `END`)을 `git archive` 로 임시 폴더에 풀고 거기서 잰다 — 작업 폴더는 건드리지 않는다.
`END_UNRESOLVED` · `END_HAS_MERGE` 가 찍히면 종료 코드 2 로 멈춘다. `HEAD` 로 바꿔 재지 않는다. 도우미 안의 `PROTO` 변수는 봉인 전 준비 실측 전용이다 — 평가 때는 비워 둔다.

도우미 준비 — 이 절의 bash · python 코드 블록을 블록 첫 `#` 줄(셔뱅 다음)의 이름으로 한 폴더에 저장하고 그 폴더를 `K` 에 넣는다:

```bash
# 이 계약에서 도우미 블록을 떼어 $K 에 저장한다 — 블록 첫 주석 줄의 이름(셔뱅 다음 줄)이 파일 이름이다
K=${K:?도우미 폴더}; mkdir -p "$K"
python3 - /Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak-c1/.harness/sprint-contract-after-0924-scripts.md "$K" <<'PY'
import re, sys, pathlib
src = open(sys.argv[1], encoding="utf-8").read(); K = pathlib.Path(sys.argv[2])
for body in re.findall(r"^```(?:bash|python)\n(.*?)^```$", src, re.S | re.M):
    lines = body.splitlines(); i = 1 if lines and lines[0].startswith("#!") else 0
    m = re.match(r"# ([\w.-]+\.(?:sh|py)) ", lines[i]) if len(lines) > i else None
    if m:
        (K / m.group(1)).write_text(body, encoding="utf-8")
PY
# markdownlint — 편집기 확장과 같은 조건(MD013 끔). 없으면 그 폴더에서 npm install --no-save markdownlint-cli2@0.23.2
ln -sfn /private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/bda55d45-296c-491f-89ba-b52042d58e72/scratchpad/c1a/mdl/node_modules "$K/node_modules"
printf '{ "config": { "MD013": false } }\n' >"$K/cfg.markdownlint-cli2.jsonc"
```

돌리는 법: `K=<폴더> TMPDIR=<폴더> bash "$K/<도우미>"`. 도우미 열: `asr.sh` (SC-01 · SC-02 · SC-03 · ER-01 · RE-01) · `ins.sh` (SC-04) · `aud.sh` (SC-05 · SC-06) · `hooks.sh` (SC-07) · `v8.sh` (SC-08 · SC-09, `guide.py` 를 부른다) · `sdocs.sh` (SC-10 · SC-11 · SC-12 · ER-02) · `scope.sh` (AR-01 ~ AR-05 · AP-01 · AP-02 · SK-00 · DG-01) · `dg.sh` (DG-02 · AP-03).

준비 단계 실측 (2026-09-26 11:4x ~ 12:0x): `$K/node_modules/.bin/markdownlint-cli2 --version` 첫 줄 `markdownlint-cli2 v0.23.2 (markdownlint v0.41.1)` · `command -v actionlint` → `/opt/homebrew/bin/actionlint` (1.7.12) ·
`python3 --version` → 3.14.3 · `python3 -c 'import yaml'` 성공 · `command -v yq` 없음(ci-local 의 `feedback-agg-test` 가 SKIP 로 나온다) · 작업 폴더에 `node_modules` 있음(ci-local 이 `npm ci` 로 만들었다, `.gitignore` 대상).

```bash
# common.sh — 측정 공통 정의. bash 로 읽는다 (`. "$K/common.sh"`)
export LC_ALL=C.UTF-8
W=${W:-/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak-c1}
cd "$W" || exit 2
B=f81568d8fbf58382172281388ec5d7756f9f46b2   # 이 계약 시작 판 (origin/main · #110)
BR=chore/ak-c1-harness-scripts
CF=.harness/sprint-contract-after-0924-scripts.md
NOTES=.harness/.meta/after-kaizen-0926/c1a-notes.md
# 끝 판: 가지 끝 → (가지를 지웠으면) 그 가지를 합친 병합 커밋의 둘째 부모. 못 찾으면 멈춘다 — HEAD 로 바꿔 재지 않는다
if [ -n "${END_OVERRIDE:-}" ]; then END=$(git rev-parse -q --verify "$END_OVERRIDE^{commit}")
else
  END=$(git rev-parse -q --verify "refs/heads/$BR^{commit}")
  if [ -z "$END" ]; then
    m=$(git log --all --merges --format=%H --grep="$BR" -1)
    [ -n "$m" ] && END=$(git rev-parse -q --verify "$m^2")
  fi
fi
[ -n "$END" ] || { echo "END_UNRESOLVED"; exit 2; }
# 이 가지에는 main 을 합치지 않는다 (main 반영은 QA 뒤 PR 단계). 합친 흔적이 있으면 범위가 섞이니 멈춘다
[ "$(git rev-list --merges "$B..$END" | grep -c .)" = 0 ] || { echo "END_HAS_MERGE $B..$END"; exit 2; }
: "${K:?도우미 폴더를 K 에 넣는다}"
T=$(mktemp -d "${TMPDIR:-/tmp}/akc1a.XXXXXX") || exit 2
trap 'rm -rf "$T"' EXIT
mkdir -p "$T/B" "$T/E"
git archive "$B" | tar -x -C "$T/B" || exit 2
git archive "$END" | tar -x -C "$T/E" || exit 2
# fresh <이름> — 끝 판을 새로 풀어 망가뜨릴 사본을 만든다 (작업 폴더는 건드리지 않는다). 이름은 m 으로 시작한다 — 맥 기본 파일 체계는 대소문자를 가리지 않아 b · e 가 B · E 를 덮는다
fresh() { rm -rf "$T/${1}"; mkdir -p "$T/${1}"; git archive "$END" | tar -x -C "$T/${1}"; }
MDL="$K/node_modules/.bin/markdownlint-cli2"
mdl_count() {  # mdl_count <폴더> <파일> <규칙> — 그 파일에서 그 규칙 경고 줄 수 (MD013 끔)
  ( cd "${1}" && "$MDL" --config "$K/cfg.markdownlint-cli2.jsonc" "${2}" 2>&1 ) | grep -cE "${3}"
}
fm_get() { awk -v k="^${2}:[[:space:]]*" 'NR==1 && /^---[[:space:]]*$/ { fm=1; next } fm && /^---[[:space:]]*$/ { exit } fm && $0 ~ k { sub(k, "", $0); print; exit }' "${1}" | sed -e "s/[[:space:]]*$//" -e "s/^['\"]//" -e "s/['\"]\$//"; }
sha256_16() { if command -v sha256sum >/dev/null 2>&1; then sha256sum; elif command -v shasum >/dev/null 2>&1; then shasum -a 256; else python3 -c 'import hashlib,sys; print(hashlib.sha256(sys.stdin.buffer.read()).hexdigest())'; fi | cut -c1-16; }
contract_digest() { grep -E '^- \[[ x]\] [A-Z]{2,}-[0-9]{2}' "${1}" | sed -E 's/^- \[[ x]\]/- [ ]/' | sha256_16; }
verify_seal() { rec=$(fm_get "${1}" conditions_digest); rec=${rec#sha256:}; if [ -z "$rec" ]; then echo "SEAL_ABSENT ${1}"; return 0; fi
  act=$(contract_digest "${1}"); if [ "$rec" = "$act" ]; then echo "SEAL_OK ${1}"; else echo "SEAL_BROKEN ${1} recorded=$rec actual=$act"; fi; }
```

```bash
#!/usr/bin/env bash
# asr.sh — 카이젠 회귀 패턴 실행기 측정 (SC-01 · SC-02 · ER-01 · RE-01)
. "$K/common.sh"
R=scripts/run-kaizen-assertions.py
KZ=harness/evals/kaizen
run() {  # run <사본 폴더> [cwd] — 실행기 종료 코드를 찍고 출력은 $T/out.txt
  ( cd "${2:-${1}}" && python3 "${1}/$R" ) >"$T/out.txt" 2>&1; echo $?
}
mut() {  # mut <사본> <파이썬 식> — 사본의 파일을 고치고 MUT_OK/MUT_MISS 를 찍는다
  ( cd "${1}" && python3 -c "${2}" ) && echo "MUT_OK" || echo "MUT_MISS"
}
# SC-03 — CI 의 Plugin Validation 묶음에 실행 단계 한 줄
ci=$(awk '/^  validate:/{f=1} /^  playwright:/{f=0} f' "$T/E/.github/workflows/ci.yml" | grep -cE '^ +run: python3 scripts/run-kaizen-assertions\.py$')
all=$(grep -cE '^ +run: python3 scripts/run-kaizen-assertions\.py$' "$T/E/.github/workflows/ci.yml")
echo "SC03 validate_job=$ci whole_file=$all"
# PROTO 는 봉인 전 준비 실측 전용 — 시험용 실행기를 사본에 넣는다. 평가 때는 비워 둔다
fr() { fresh "${1}"; if [ -n "${PROTO:-}" ]; then cp "$PROTO" "$T/${1}/$R"; fi; }
if [ -n "${PROTO:-}" ]; then cp "$PROTO" "$T/E/$R"; fi
[ -f "$T/E/$R" ] || { echo "NO_RUNNER $R"; exit 2; }

# SC-01 — 끝 판 그대로
rc=$(run "$T/E"); p=$(grep -c '^PASS ' "$T/out.txt"); f=$(grep -c '^FAIL ' "$T/out.txt")
pairs=0
for kp in contract-kaizen/ambiguous-conditions contract-kaizen/category-bias contract-kaizen/low-coverage contract-kaizen/vacuous-boilerplate \
          evaluator-kaizen/l3-miss evaluator-kaizen/false-approve evaluator-kaizen/reject-loop evaluator-kaizen/vacuous-zero evaluator-kaizen/silent-check; do
  grep -q "^PASS .*$kp" "$T/out.txt" && pairs=$((pairs+1))
done
echo "SC01 rc=$rc pass=$p fail=$f pairs=$pairs/9 total=[$(tail -1 "$T/out.txt")]"
# RE-01 — 다른 폴더에서 불러도 같은 결과
rc2=$(run "$T/E" /); echo "RE01 rc=$rc2 total=[$(tail -1 "$T/out.txt")]"

# SC-02 — 통과해선 안 되는 사본 셋 (종료 코드 1)
fr ma; mut "$T/ma" "import json;p='$KZ/evaluator-kaizen/assertions.json';d=json.load(open(p));d['silent-check'][2]['pattern']='없는글자-zz9';json.dump(d,open(p,'w'),ensure_ascii=False)"
rc=$(run "$T/ma"); echo "SC02a rc=$rc fail_line=$(grep -c '^FAIL .*evaluator-kaizen/silent-check' "$T/out.txt") total=[$(tail -1 "$T/out.txt")]"
fr mb; mut "$T/mb" "import shutil;shutil.copy('$KZ/evaluator-kaizen/fixture-feedback-data/silent-check.yaml','$KZ/evaluator-kaizen/fixture-feedback-data/orphan-probe.yaml')"
rc=$(run "$T/mb"); echo "SC02b rc=$rc fail_line=$(grep -c '^FAIL .*orphan-probe' "$T/out.txt")"
fr mc; mut "$T/mc" "import os;os.remove('$KZ/evaluator-kaizen/fixture-feedback-data/l3-miss.yaml')"
rc=$(run "$T/mc"); echo "SC02c rc=$rc fail_line=$(grep -c '^FAIL .*l3-miss' "$T/out.txt")"

# ER-01 — 읽지 못하는 사본 다섯 (종료 코드 2, 출력에 원인 이름)
fr md; mut "$T/md" "p='$KZ/contract-kaizen/assertions.json';open(p,'a').write(',')"
rc=$(run "$T/md"); echo "ER01d rc=$rc named=$(grep -c 'contract-kaizen/assertions.json' "$T/out.txt")"
fr me; mut "$T/me" "import json;p='$KZ/evaluator-kaizen/assertions.json';d=json.load(open(p));d['l3-miss'][0]['file']='harness/agents/no-such-zz9.md';json.dump(d,open(p,'w'),ensure_ascii=False)"
rc=$(run "$T/me"); echo "ER01e rc=$rc named=$(grep -c 'no-such-zz9.md' "$T/out.txt")"
fr mf; mut "$T/mf" "import json;p='$KZ/contract-kaizen/assertions.json';d=json.load(open(p));d['low-coverage'][0]['type']='file_absent';json.dump(d,open(p,'w'),ensure_ascii=False)"
rc=$(run "$T/mf"); echo "ER01f rc=$rc named=$(grep -c 'file_absent' "$T/out.txt")"
fr mg; mut "$T/mg" "import json;p='$KZ/contract-kaizen/assertions.json';d=json.load(open(p));d['category-bias'][0]['pattern']='(';json.dump(d,open(p,'w'),ensure_ascii=False)"
rc=$(run "$T/mg"); echo "ER01g rc=$rc named=$(grep -c 'category-bias' "$T/out.txt")"
fr mh; mut "$T/mh" "import os;[os.remove(f'$KZ/{k}/assertions.json') for k in ('contract-kaizen','evaluator-kaizen')]"
rc=$(run "$T/mh"); echo "ER01h rc=$rc"
```

```bash
#!/usr/bin/env bash
# ins.sh — 처리 배정표 검사기의 번호 ↔ 슬러그 대응 측정 (SC-04)
. "$K/common.sh"
C=scripts/check-insights-tracking.py
IR=.claude/kaizen-input/insights-report.md
chk() {  # chk <사본> [--final] — 종료 코드를 찍고 출력은 $T/out.txt
  ( cd "${1}" && python3 "$C" ${2:+"${2}"} "$IR" ) >"$T/out.txt" 2>&1; echo $?
}
sub() {  # sub <사본> <옛 칸> <새 칸> <횟수|all> — 표 칸을 바꾸고 바꾼 수를 찍는다
  ( cd "${1}" && python3 - "${2}" "${3}" "${4}" "$IR" <<'PY'
import sys
old, new, n, p = sys.argv[1:5]
s = open(p, encoding="utf-8").read()
c = s.count(f"| {old} |")
s = s.replace(f"| {old} |", f"| {new} |", -1 if n == "all" else int(n))
open(p, "w", encoding="utf-8").write(s)
print(f"MUT count_before={c}")
PY
  )
}
# PROTO 는 봉인 전 준비 실측 전용 — 시험용 검사기를 사본에 넣는다. 평가 때는 비워 둔다
fr() { fresh "${1}"; if [ -n "${PROTO:-}" ]; then cp "$PROTO" "$T/${1}/$C"; fi; }
if [ -n "${PROTO:-}" ]; then cp "$PROTO" "$T/E/$C"; fi
rc=$(chk "$T/E" --final); echo "SC04a rc=$rc ok=$(grep -c '^TRACKING_TABLE_OK$' "$T/out.txt") [$(grep -m1 '^mode=' "$T/out.txt")]"
fr ma; sub "$T/ma" kaizen-0924-p06-design-kit kaizen-0924-p05-flutter-toolkit all
rc=$(chk "$T/ma" --final); echo "SC04b rc=$rc fail=$(grep -c '^TRACKING_TABLE_FAIL$' "$T/out.txt") rows=$(grep -cE '^[0-9]+행 .*Phase 6' "$T/out.txt")"
rc=$(chk "$T/ma"); echo "SC04c basic rc=$rc"
fr mb; sub "$T/mb" kaizen-0924-p12-reflect-kit kaizen-phase12-oracle-positive-control all
rc=$(chk "$T/mb" --final); echo "SC04d rc=$rc"
fr mc; sub "$T/mc" kaizen-0924-p03-evaluator kaizen-0924-final 1
rc=$(chk "$T/mc" --final); echo "SC04e rc=$rc fail=$(grep -c '^TRACKING_TABLE_FAIL$' "$T/out.txt") rows=$(grep -cE '^[0-9]+행 .*kaizen-0924-final' "$T/out.txt")"
```

```bash
#!/usr/bin/env bash
# aud.sh — 감사 기록 덧붙이기 도구 측정 (SC-05 · SC-06)
. "$K/common.sh"
A=scripts/append-audit-log.py
LOG=.harness/.meta/orchestrator-audit-log.md
mk() {  # mk <이름> <처음 내용 파일|-> — 스크립트 하나와 감사 기록 하나만 든 작은 나무
  rm -rf "$T/${1}"; mkdir -p "$T/${1}/scripts" "$T/${1}/.harness/.meta"
  cp "${PROTO:-$T/E/$A}" "$T/${1}/$A"   # PROTO 는 봉인 전 준비 실측 전용. 평가 때는 비워 둔다
  if [ "${2}" = "-" ]; then printf '# 감사 기록\n\n본문 한 줄\n' >"$T/${1}/$LOG"; else cp "${2}" "$T/${1}/$LOG"; fi
}
ap() { ( cd "$T/${1}" && shift && python3 "$A" "$@" ) >>"$T/ap.txt" 2>&1; echo $?; }
: >"$T/ap.txt"
# SC-05 · SC-06 — 끝에 빈 줄 없는 작은 기록에 세 항목을 붙인다
mk s -
printf '[{"check": "x-check", "reason": "r"}]\n' >"$T/f.json"
r1=$(ap s --cycle-id cyc-a)
r2=$(ap s --cycle-id cyc-b --watch "감시 하나" --watch "감시 둘")
r3=$(ap s --cycle-id cyc-c --failures "$T/f.json" --watch "감시 셋")
echo "rc=[$r1 $r2 $r3]"
python3 - "$T/s/$LOG" <<'PY'
import re, sys, datetime
t = open(sys.argv[1], encoding="utf-8").read()
today = datetime.date.today().isoformat()
lines = t.split("\n")
heads = [i for i, l in enumerate(lines) if l.startswith("## ")]
blank_before = sum(1 for i in heads if i > 0 and lines[i - 1] == "")
subs = [l for l in lines if l.startswith("### ")]
sub_ok = sum(1 for l in subs if today in l and re.search(r"cyc-[abc]", l))
def entry(c):
    m = re.search(rf"^## [^\n]*{c}$(.*?)(?=^## |\Z)", t, re.S | re.M)
    return m.group(1) if m else ""
def watch(c):
    m = re.search(r"^### [^\n]*(?:watchlist|감시)[^\n]*$(.*?)(?=^### |^---$|\Z)", entry(c), re.S | re.M | re.I)
    return m.group(1) if m else ""
wa, wb, wc = watch("cyc-a"), watch("cyc-b"), watch("cyc-c")
print(f"SC05 heads={len(heads)} blank_before={blank_before}/{len(heads)} subs={len(subs)} sub_ok={sub_ok}/{len(subs)}")
print(f"SC06 a_none={wa.count('특별 감시 대상 없음')} b_items={int('감시 하나' in wb)}{int('감시 둘' in wb)} b_none={wb.count('특별 감시 대상 없음')} "
      f"c_items={int('x-check' in wc)}{int('감시 셋' in wc)} c_none={wc.count('특별 감시 대상 없음')}")
PY
echo "SC05 md024=$(mdl_count "$T/s" "$LOG" MD024) md022_032=$(mdl_count "$T/s" "$LOG" 'MD022|MD032')"
echo "SC06 help_watch=$( ( cd "$T/s" && python3 "$A" --help ) 2>&1 | grep -c -- '--watch')"
# SC-05 (d) — 실제 감사 기록 사본에 한 항목: 앞부분 그대로 · 같은 제목 경고가 늘지 않는다
mk r "$T/E/$LOG"
before=$(mdl_count "$T/r" "$LOG" MD024); cp "$T/r/$LOG" "$T/old.md"
rr=$(ap r --cycle-id cyc-z)
after=$(mdl_count "$T/r" "$LOG" MD024)
pre=$(python3 -c "import sys;o=open(sys.argv[1],'rb').read();n=open(sys.argv[2],'rb').read();print(int(n.startswith(o) and len(n)>len(o)))" "$T/old.md" "$T/r/$LOG")
echo "SC05r rc=$rr prefix=$pre md024_before=$before md024_after=$after"
```

```bash
#!/usr/bin/env bash
# hooks.sh — 킷 넷 hooks.json 명령의 따옴표와 빈칸 든 경로 실행 측정 (SC-07)
. "$K/common.sh"
python3 - "$T/B" "$T/E" "$T/S" <<'PY'
import json, os, re, stat, subprocess, sys
B, E, S = sys.argv[1:4]
KITS = ["design-kit", "flutter-toolkit", "harness", "reflect-kit"]
REF = re.compile(r'\$\{CLAUDE_PLUGIN_ROOT\}"?/([^\s"]+)')
def cmds(root, kit):
    d = json.load(open(f"{root}/{kit}/hooks/hooks.json", encoding="utf-8"))
    return [h["command"] for ev in d["hooks"].values() for en in ev for h in en["hooks"] if h.get("command")]
def strip(root, kit):
    d = json.load(open(f"{root}/{kit}/hooks/hooks.json", encoding="utf-8"))
    for ev in d["hooks"].values():
        for en in ev:
            for h in en["hooks"]:
                if "command" in h: h["command"] = h["command"].replace('"', "")
    return d
total = quoted = same = ran_env = ran_sub = 0
for kit in KITS:
    same += strip(B, kit) == strip(E, kit)
    root = os.path.join(S, "plug root", kit)          # 빈칸 든 설치 경로 흉내
    for c in cmds(E, kit):
        total += 1
        n_ref = c.count("${CLAUDE_PLUGIN_ROOT}")
        n_q = len(re.findall(r'"\$\{CLAUDE_PLUGIN_ROOT\}[^"]*"', c)) + len(re.findall(r'"\$\{CLAUDE_PLUGIN_ROOT\}"', c))
        quoted += n_ref > 0 and n_q >= n_ref
        rels = REF.findall(c)
        for rel in rels:                                  # 같은 상대 경로에 흉내 스크립트
            p = os.path.join(root, rel.lstrip("/")); os.makedirs(os.path.dirname(p), exist_ok=True)
            open(p, "w").write(f'#!/bin/sh\necho "RAN {rel.lstrip("/")} $*"\n'); os.chmod(p, 0o755)
        args = c.split(rels[-1], 1)[1].replace('"', "").split() if rels else []
        want = f"RAN {rels[-1].lstrip('/')}" + (" " + " ".join(args) if args else "")
        env = dict(os.environ, CLAUDE_PLUGIN_ROOT=root)
        r = subprocess.run(["sh", "-c", c], env=env, stdin=subprocess.DEVNULL, capture_output=True, text=True)
        ran_env += r.returncode == 0 and r.stdout.strip() == want
        r = subprocess.run(["sh", "-c", c.replace("${CLAUDE_PLUGIN_ROOT}", root)], stdin=subprocess.DEVNULL, capture_output=True, text=True)
        ran_sub += r.returncode == 0 and r.stdout.strip() == want
print(f"SC07 commands={total} quoted={quoted}/{total} same_shape={same}/4 ran_env={ran_env}/{total} ran_sub={ran_sub}/{total}")
PY
```

```bash
#!/usr/bin/env bash
# v8.sh — validate-plugin V8 측정 (SC-08)
. "$K/common.sh"
V=scripts/validate-plugin.py
v8() {  # v8 <사본> — 종료 코드를 찍고 출력은 $T/out.txt
  ( cd "${1}" && python3 "$V" --check=hook-exec ) >"$T/out.txt" 2>&1; echo $?
}
line() { awk -v k="=== ${1} ===" '$0==k{f=1;next} /^=== /{f=0} f && /V8/' "$T/out.txt" | head -1; }
setcmd() {  # setcmd <사본> <킷> <명령> — 그 킷 hooks.json 첫 명령을 바꾸고 MUT 를 찍는다
  python3 - "${1}/${2}/hooks/hooks.json" "${3}" <<'PY'
import json, sys
p, c = sys.argv[1:3]
d = json.load(open(p, encoding="utf-8"))
h = next(h for ev in d["hooks"].values() for en in ev for h in en["hooks"] if "command" in h)
old = h["command"]; h["command"] = c
json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(f"MUT {old!r} -> {c!r}")
PY
}
rc=$(v8 "$T/E")
echo "SC08a rc=$rc total=[$(grep '^Total:' "$T/out.txt")] harness=[$(line harness)] flutter=[$(line flutter-toolkit)] design=[$(line design-kit)] reflect=[$(line reflect-kit)]"
fresh ma; chmod -x "$T/ma/harness/scripts/run-guard.sh" && echo "MUT chmod -x run-guard.sh mode=$(stat -f %Lp "$T/ma/harness/scripts/run-guard.sh" 2>/dev/null || stat -c %a "$T/ma/harness/scripts/run-guard.sh")"
rc=$(v8 "$T/ma"); echo "SC08b rc=$rc harness=[$(line harness)] named=$(grep -c 'run-guard.sh' "$T/out.txt")"
fresh mb; setcmd "$T/mb" design-kit '${CLAUDE_PLUGIN_ROOT}/scripts/env-check.sh'
rc=$(v8 "$T/mb"); echo "SC08c rc=$rc design=[$(line design-kit)] named=$(grep -c 'design-kit/hooks/hooks.json' "$T/out.txt")"
fresh mc; setcmd "$T/mc" design-kit '"${CLAUDE_PLUGIN_ROOT}"/scripts/env-check.sh'
rc=$(v8 "$T/mc"); echo "SC08d rc=$rc design=[$(line design-kit)]"
fresh md; setcmd "$T/md" reflect-kit 'bash ${CLAUDE_PLUGIN_ROOT}/hooks/log-prompt.sh'
rc=$(v8 "$T/md"); echo "SC08e rc=$rc reflect=[$(line reflect-kit)] named=$(grep -c 'reflect-kit/hooks/hooks.json' "$T/out.txt")"
# SC-09 — 가이드 V8 절 (시작 판과 끝 판)
python3 "$K/guide.py" "$T/B" | sed "s/^SC09 /SC09 base /"
python3 "$K/guide.py" "$T/E"
```

```python
#!/usr/bin/env python3
# guide.py — 검증 가이드 V8 절의 따옴표 규칙 서술 측정 (SC-09). 인자: <풀어 둔 판 폴더>
import re, sys
t = open(f"{sys.argv[1]}/harness/docs/guides/plugin-validation-guide.md", encoding="utf-8").read()
m = re.search(r"^### V8 [^\n]*$(.*?)(?=^### V9 )", t, re.S | re.M)
sec = m.group(1) if m else ""
JSON_UNQ = re.compile(r'"command":\s*"(?:[a-z]+ )?\$\{CLAUDE_PLUGIN_ROOT\}')   # JSON 값이 따옴표 없이 시작
SPAN = re.compile(r"`([^`]+)`")
def unquoted(line):
    n = len(JSON_UNQ.findall(line))
    for span in SPAN.findall(line):                  # 줄 안 코드 안의 셸 꼴
        if '"command"' in span or span.strip() == "${CLAUDE_PLUGIN_ROOT}": continue   # JSON 꼴은 위에서 셌다 · 변수 이름만 든 것은 명령이 아니다
        n += len(re.findall(r'(?<!")\$\{CLAUDE_PLUGIN_ROOT\}', span))
    return n
outside = 0; fail_blocks = 0; fence = None; buf = []
for line in sec.split("\n"):
    f = re.match(r"^ {0,3}(`{3,}|~{3,})", line)
    if f and fence is None:
        fence = f.group(1); buf = []; continue
    if f and fence and line.strip().startswith(fence[0] * len(fence)):
        if any("FAIL" in b for b in buf): fail_blocks += 1
        else: outside += sum(len(JSON_UNQ.findall(b)) for b in buf)
        fence = None; continue
    if fence: buf.append(line)
    else: outside += unquoted(line)
qx = sec.count(chr(92) + chr(34) + "${CLAUDE_PLUGIN_ROOT}")   # hooks.json 에 쓰는 꼴 \"${CLAUDE_PLUGIN_ROOT}
print(f"SC09 v8_section={int(bool(sec))} quote_word={sec.count('따옴표')} json_quoted_example={qx} fail_blocks={fail_blocks} unquoted_outside_fail={outside}")
```

```bash
#!/usr/bin/env bash
# sdocs.sh — sync-docs 표지 읽기 · 짝 없는 표지 · 훅 표 · 루트 README 스킬 수 측정 (SC-10 · SC-11 · SC-12 · ER-02)
. "$K/common.sh"
SD=scripts/sync-docs.py
sd() {  # sd <사본> [--check-only] — 종료 코드를 찍고 출력은 $T/out.txt
  ( cd "${1}" && python3 "$SD" ${2:+"${2}"} ) >"$T/out.txt" 2>&1; echo $?
}
need() { grep -c "^  ${1}: 변경 필요$" "$T/out.txt"; }
rc=$(sd "$T/E" --check-only); echo "SC11a rc=$rc synced=$(grep -c '^모든 README가 동기화 상태입니다.$' "$T/out.txt") need_any=$(grep -c ': 변경 필요$' "$T/out.txt")"
# SC-11 (b) — 세 킷 README 의 첫 AUTO:skills 블록 안 표 한 줄을 망가뜨린다
fresh ma
python3 - "$T/ma" <<'PY'
import re, sys
for kit in ("onboarding-kit", "planning-kit", "rust-kit"):
    p = f"{sys.argv[1]}/{kit}/README.md"; lines = open(p, encoding="utf-8").read().split("\n")
    i = next(i for i, l in enumerate(lines) if "AUTO:skills" in l and "/AUTO" not in l)
    j = next(j for j in range(i + 1, len(lines)) if lines[j].startswith("| `"))
    lines[j] += " ZZCORRUPT"; open(p, "w", encoding="utf-8").write("\n".join(lines))
    print(f"MUT {kit} line={j + 1}")
PY
rc=$(sd "$T/ma" --check-only); echo "SC11b rc=$rc onboarding=$(need onboarding-kit/README.md) planning=$(need planning-kit/README.md) rust=$(need rust-kit/README.md)"
# ER-02 — 짝 없는 여는 표지 하나
fresh mb; printf '\n<!-- AUTO:skills -->\n' >>"$T/mb/tone-kit/README.md" && echo "MUT tone-kit opener_lines=$(grep -c '^<!-- AUTO:skills -->$' "$T/mb/tone-kit/README.md")"
rc=$(sd "$T/mb" --check-only); echo "ER02 rc=$rc named=$(grep -v ': 동기화됨$' "$T/out.txt" | grep -c 'tone-kit/README.md')"
# SC-10 — 훅 표: 따옴표 붙은 명령에서도 스크립트 이름만 보인다
for f in design-kit/README.md reflect-kit/README.md; do
  printf 'SC10 %s same=%s\n' "$f" "$(cmp -s "$T/B/$f" "$T/E/$f" && echo 1 || echo 0)"
done
python3 - "$T/E" <<'PY'
import sys
t = open(f"{sys.argv[1]}/design-kit/README.md", encoding="utf-8").read() + open(f"{sys.argv[1]}/reflect-kit/README.md", encoding="utf-8").read()
q = '.sh' + chr(34)
n = sum(1 for l in t.splitlines() if l.startswith('| `') and q in l)
print(f"SC10 quote_in_hook_rows={n}")
PY
# SC-12 (a) — 가짜 스킬 하나를 더하면 루트 README 가 변경 필요, 동기화 뒤 21종
fresh mc; mkdir -p "$T/mc/flutter-toolkit/skills/zz-probe"
printf -- '---\nname: zz-probe\ndescription: 측정용 가짜 스킬\n---\n\n# zz-probe\n' >"$T/mc/flutter-toolkit/skills/zz-probe/SKILL.md" && echo "MUT zz-probe skills=$(find "$T/mc/flutter-toolkit/skills" -mindepth 2 -maxdepth 2 -name SKILL.md | wc -l | tr -d ' ')"
rc=$(sd "$T/mc" --check-only); echo "SC12a rc=$rc root=$(need README.md)"
rc=$(sd "$T/mc"); rc2=$(sd "$T/mc" --check-only); echo "SC12a write_rc=$rc recheck_rc=$rc2"
# SC-12 (b)(c) — 루트 README 네 킷 절의 AUTO 블록 · 블록 밖 스킬 수 글자 · 세 킷 README 제목
python3 - "$T/E" "$T/mc" "$T/B" <<'PY'
import re, sys, os
def skills(root, kit): return sorted(d for d in os.listdir(f"{root}/{kit}/skills") if os.path.isfile(f"{root}/{kit}/skills/{d}/SKILL.md"))
def agents(root, kit):
    p = f"{root}/{kit}/agents"; return [f for f in os.listdir(p) if f.endswith(".md")] if os.path.isdir(p) else []
BLOCK = re.compile(r"^<!-- AUTO:([\w:-]+) -->$\n(.*?)^<!-- /AUTO:\1 -->$", re.S | re.M)
def check(root, tag):
    t = open(f"{root}/README.md", encoding="utf-8").read()
    ok_b = ok_c = ok_n = 0
    for kit in ("harness", "flutter-toolkit", "rust-kit", "react-kit"):
        m = re.search(rf"^### {re.escape(kit)}$(.*?)(?=^### |^## |\Z)", t, re.S | re.M)
        sec = m.group(1) if m else ""
        bl = BLOCK.findall(sec)
        if len(bl) != 1: continue
        ok_b += 1; body = bl[0][1]
        n, a = skills(root, kit), agents(root, kit)
        ok_c += f"스킬 {len(n)}종" in body and (not a or f"에이전트 {len(a)}종" in body)
        ok_n += all(s in body for s in n)
    out = BLOCK.sub("", t)
    cnt = len(re.findall(r"(스킬|워크플로우) ?[0-9]+ ?종|[0-9]+ ?종 ?\+ ?[0-9]+ ?에이전트|등 [0-9]+ ?종", out))
    lst = out.count("**제공 스킬:** api,") + out.count("| `init` | `/harness init` |")
    print(f"SC12 {tag} blocks={ok_b}/4 counts={ok_c}/4 names={ok_n}/4 outside_counts={cnt} outside_lists={lst}")
check(sys.argv[1], "end"); check(sys.argv[2], "probe"); check(sys.argv[3], "base")
t = open(f"{sys.argv[2]}/README.md", encoding="utf-8").read()
m = re.search(r"^### flutter-toolkit$(.*?)(?=^### |^## |\Z)", t, re.S | re.M)
print(f"SC12 probe_block_21={int(bool(m) and '스킬 21종' in m.group(1) and 'zz-probe' in m.group(1))}")
E = sys.argv[1]
h = lambda k, s: sum(1 for l in open(f"{E}/{k}/README.md", encoding="utf-8").read().split("\n") if l == s)
print(f"SC11c headings onboarding_skill={h('onboarding-kit','## 스킬')} planning_skill={h('planning-kit','## 스킬')} planning_agent={h('planning-kit','## 에이전트')} rust_skill={h('rust-kit','## 스킬')} rust_agent={h('rust-kit','## 에이전트')}")
PY
```

```bash
#!/usr/bin/env bash
# scope.sh — 바뀐 파일 범위 · 커밋마다 킷 하나 · .harness 범위 · notes · 버전 글자 측정 (AR-01 ~ AR-05 · AP-01 · SK-00)
. "$K/common.sh"
WANT=".github/workflows/ci.yml
README.md
design-kit/hooks/hooks.json
flutter-toolkit/hooks/hooks.json
harness/docs/guides/plugin-validation-guide.md
harness/hooks/hooks.json
onboarding-kit/README.md
planning-kit/README.md
reflect-kit/hooks/hooks.json
rust-kit/README.md
scripts/append-audit-log.py
scripts/check-insights-tracking.py
scripts/run-kaizen-assertions.py
scripts/sync-docs.py
scripts/validate-plugin.py"
git diff --name-only "$B" "$END" -- . ':(exclude).harness' | LC_ALL=C sort >"$T/got.txt"
printf '%s\n' "$WANT" | LC_ALL=C sort >"$T/want.txt"
echo "AR01 got=$(grep -c . "$T/got.txt") exact=$(cmp -s "$T/got.txt" "$T/want.txt" && echo 1 || echo 0) extra=[$(comm -23 "$T/got.txt" "$T/want.txt" | tr '\n' ' ')] missing=[$(comm -13 "$T/got.txt" "$T/want.txt" | tr '\n' ' ')]"
# AR-02 — 두 공유 파일의 바뀐 덩어리가 V8 자리 안에만 있다 (시작 판 줄 번호)
inrange() {  # inrange <파일> <첫 줄> <끝 줄> — 바깥 덩어리 수
  git diff -U0 "$B" "$END" -- "${1}" | awk -v lo="${2}" -v hi="${3}" '/^@@ /{ split($2, a, ","); s = substr(a[1], 2) + 0; n = (a[2] == "" ? 1 : a[2] + 0); e = (n == 0 ? s : s + n - 1); h++; if (s < lo || e > hi) out++ } END { printf "hunks=%d outside=%d", h, out + 0 }'
}
echo "AR02 validate=[$(inrange scripts/validate-plugin.py 626 716)] guide=[$(inrange harness/docs/guides/plugin-validation-guide.md 391 417)]"
# AR-03 — 킷 폴더를 건드린 커밋은 그 킷 하나만 건드린다
KITS=$(python3 -c "import json;print(' '.join(p['name'] for p in json.load(open('$T/E/.claude-plugin/marketplace.json'))['plugins']))")
bad=0; n=0
for c in $(git rev-list --no-merges "$B..$END"); do
  n=$((n+1))
  tops=$(git show --name-only --format= "$c" | grep . | cut -d/ -f1 | LC_ALL=C sort -u)
  kits=0; for t in $tops; do case " $KITS " in *" $t "*) kits=$((kits+1));; esac; done
  others=$(printf '%s\n' $tops | grep -c .)
  if [ "$kits" -gt 1 ] || { [ "$kits" = 1 ] && [ "$others" -gt 1 ]; }; then bad=$((bad+1)); echo "  mixed $c: $(echo $tops)"; fi
done
echo "AR03 commits=$n mixed=$bad"
# AR-04 — .harness: 봉인 깨진 계약 0 · 공유 기록 둘 그대로 · 바뀐 경로는 이 계약 몫만
sb=$(find "$T/E/.harness" -type f -name 'sprint-contract*.md' | while read -r f; do verify_seal "$f"; done | grep -c '^SEAL_BROKEN')
same=0; for f in .harness/.meta/orchestrator-audit-log.md .harness/stale-values.yaml .claude/kaizen-input/insights-report.md; do git diff --quiet "$B" "$END" -- "$f" && same=$((same+1)); done
hx=$(git diff --name-only "$B" "$END" -- .harness | grep -vxE '\.harness/sprint-(contract|amendments|feedback)-after-0924-scripts\.md|\.harness/\.meta/after-kaizen-0926/c1a-notes\.md' | grep -c .)
echo "AR04 seal_broken=$sb shared_same=$same/3 harness_extra=$hx"
# AR-05 — notes 에 넘김 글자
TOK=('72d6ddd' '--watch' '.claude/skills/kaizen-orchestrator/SKILL.md' 'harness/skills/contract-kaizen/SKILL.md' 'harness/skills/evaluator-kaizen/SKILL.md' 'F1H-40' 'F1H-94' 'docs/harness/plugin-validation.html' 'feat/v10-fence-commonmark' 'harness/evals/kaizen/evaluator-kaizen/assertions.json' 'plugin-validation-guide.md' 'reflect-kit/README.md:156' '릴리스')
if [ -f "$T/E/$NOTES" ]; then hit=0; miss=""; for t in "${TOK[@]}"; do grep -qF -- "$t" "$T/E/$NOTES" && hit=$((hit+1)) || miss="$miss $t"; done; echo "AR05 notes=1 tokens=$hit/${#TOK[@]} miss=[$miss]"; else echo "AR05 notes=0"; fi
# AP-01 · AP-02 — 더한 줄의 금지 꼴 (project.yaml 패턴 + 버전꼴 글자)
git diff "$B" "$END" -- . ':(exclude).harness' | grep '^+' | grep -v '^+++' >"$T/added.txt"
echo "AP01 added_versions=$(git diff "$B" "$END" -- scripts .github | grep '^+' | grep -v '^+++' | grep -cE '[0-9]+\.[0-9]+\.[0-9]+') hardcoded_pattern=$(grep -ciE 'hardcoded.*version' "$T/added.txt")"
echo "AP02 force_push=$(grep -cE 'git push.*--force' "$T/added.txt")"
# SK-00 — 스킬 · 에이전트 파일 변경 0
echo "SK00 skill_agent_changed=$(git diff --name-only "$B" "$END" | grep -cE '(^|/)skills/[^/]+/SKILL\.md$|(^|/)agents/[^/]+\.md$')"
# DG-01 · DG-03 N/A 근거 — release.sh 가 바뀐 파일에 없다
echo "DG01 release_sh_changed=$(git diff --name-only "$B" "$END" | grep -cx scripts/release.sh)"
# RE-02 — 공용 모듈 · 기존 수집 함수 · 기존 표 읽기를 다시 쓴다 (끝 판 폴더에서 센다)
R=$T/E/scripts/run-kaizen-assertions.py
ra=NA; rb=NA
if [ -f "$R" ]; then ra=$(grep -c 'from plugin_utils import' "$R"); rb=$(grep -cE '^REPO_ROOT *=|Path\(__file__\)' "$R"); fi
echo "RE02 runner_import=$ra runner_self_root=$rb sync_collectors=$(grep -cE 'iter_skills\(|iter_agents\(|/ "skills"|skills/\*|os\.listdir|\.iterdir\(' "$T/E/scripts/sync-docs.py") insights_readers=$(grep -cE 'def split_row|def table_blocks' "$T/E/scripts/check-insights-tracking.py")"
```

```bash
#!/usr/bin/env bash
# dg.sh — 편집기 경고 대응 측정 (DG-02 · AP-03)
. "$K/common.sh"
"$MDL" --version 2>&1 | head -1 | grep -q 'v0.23.2' || { echo "MDL_MISSING $MDL"; exit 2; }
MDS="README.md onboarding-kit/README.md planning-kit/README.md rust-kit/README.md harness/docs/guides/plugin-validation-guide.md"
worse=0; line=""
for f in $MDS; do
  b=$(mdl_count "$T/B" "$f" 'MD[0-9]{3}'); e=$(mdl_count "$T/E" "$f" 'MD[0-9]{3}')
  line="$line $f=$b->$e"; [ "$e" -gt "$b" ] && worse=$((worse+1))
done
n=0; [ -f "$T/E/$NOTES" ] && n=$(mdl_count "$T/E" "$NOTES" 'MD[0-9]{3}')
echo "DG02 md_worse=$worse notes_warn=$n [$line ]"
PYS="scripts/run-kaizen-assertions.py scripts/check-insights-tracking.py scripts/append-audit-log.py scripts/validate-plugin.py scripts/sync-docs.py"
pc=0; for f in $PYS; do [ -f "$T/E/$f" ] && python3 -W error -m py_compile "$T/E/$f" 2>/dev/null && pc=$((pc+1)); done
js=0; for k in design-kit flutter-toolkit harness reflect-kit; do python3 -m json.tool "$T/E/$k/hooks/hooks.json" >/dev/null 2>&1 && js=$((js+1)); done
( cd "$T/E" && actionlint .github/workflows/ci.yml ) >/dev/null 2>&1; al=$?
echo "DG02 py_compile=$pc/5 json=$js/4 actionlint_rc=$al"
# AP-03 — 언어 힌트 없는 여는 펜스 (루트 README · notes). 킷 문서는 V6 가 잰다
python3 - "$T/E" README.md "$NOTES" <<'PY'
import os, re, sys
root = sys.argv[1]; bare = 0
for f in sys.argv[2:]:
    p = os.path.join(root, f)
    if not os.path.isfile(p): continue
    fence = None
    for l in open(p, encoding="utf-8"):
        m = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", l.rstrip("\n"))
        if not m: continue
        if fence is None:
            fence = m.group(1); bare += m.group(2).strip() == ""
        elif m.group(1)[0] == fence[0] and len(m.group(1)) >= len(fence) and m.group(2).strip() == "":
            fence = None
print(f"AP03 bare_open={bare}")
PY
( cd "$T/E" && python3 scripts/validate-plugin.py --check=code-fence ) >"$T/out.txt" 2>&1; echo "AP03 v6_rc=$? [$(grep '^Total:' "$T/out.txt")]"
```

### 봉인 전 실측

시작 판 = `END_OVERRIDE=f81568d…` 로 같은 도우미를 돌린 값. 시험판 = 스크래치 복제본(`scratchpad/c1a/proto-repo`, 가지 `proto-c1a`)에 이 계약대로 만든 시험 구현(레포에 넣지 않음)에 돌린 값 — 조건끼리 부딪히지 않고 모두 동시에 채워질 수 있음을 본 것이다. 시험판 값은 기대값의 근거가 아니라 도달 가능성의 근거다.

| 조건 | 시작 판 | 시험판 |
| ---- | ------- | ------ |
| SC-01 | `NO_RUNNER` (실행기 없음, 종료 코드 2) | `SC01 rc=0 pass=14 fail=0 pairs=9/9 total=[Total: 14 passed, 0 failed]` |
| SC-02 | 실행기 없음 | `SC02a rc=1 fail_line=1 total=[Total: 13 passed, 1 failed]` · `SC02b rc=1 fail_line=1` · `SC02c rc=1 fail_line=1` · `MUT_OK` 셋 |
| SC-03 | `SC03 validate_job=0 whole_file=0` | `SC03 validate_job=1 whole_file=1` |
| SC-04 | `SC04a rc=0 ok=1` · `SC04b rc=0 fail=0 rows=0` · `SC04c basic rc=0` · `SC04d rc=0` · `SC04e rc=0 fail=0 rows=0` | `SC04a rc=0 ok=1` · `SC04b rc=1 fail=1 rows=9` · `SC04c basic rc=0` · `SC04d rc=0` · `SC04e rc=1 fail=1 rows=1` |
| SC-05 | `rc=[0 2 2]` · `heads=1 blank_before=0/1 subs=3 sub_ok=0/3` · `md024=0 md022_032=1` · `SC05r rc=0 prefix=1 md024_before=8 md024_after=11` | `rc=[0 0 0]` · `heads=3 blank_before=3/3 subs=9 sub_ok=9/9` · `md024=0 md022_032=0` · `SC05r rc=0 prefix=1 md024_before=8 md024_after=8` |
| SC-06 | `a_none=1 b_items=00 b_none=0 c_items=00 c_none=0` · `help_watch=0` | `a_none=1 b_items=11 b_none=0 c_items=11 c_none=0` · `help_watch=2` |
| SC-07 | `commands=10 quoted=0/10 same_shape=4/4 ran_env=0/10 ran_sub=0/10` | `commands=10 quoted=10/10 same_shape=4/4 ran_env=10/10 ran_sub=10/10` |
| SC-08 | (a) `rc=0` · `14 OK` · `5 hook` · `1 hook` · `1 hook` (b) `rc=2 … FAIL named=1` (c) `rc=0 … OK named=0` (d) `rc=0 … 직접 실행 hook 스크립트 없음` (e) `rc=0 named=0` | (a) 같음 (b) `rc=2 FAIL named=1` (c) `rc=2 FAIL named=1` (d) `rc=0 … 1 hook … OK` (e) `rc=2 FAIL named=1` |
| SC-09 | `quote_word=0 json_quoted_example=0 fail_blocks=1 unquoted_outside_fail=3` | `quote_word=6 json_quoted_example=3 fail_blocks=2 unquoted_outside_fail=0` |
| SC-10 | `same=1` · `same=1` · `quote_in_hook_rows=0` (따옴표가 아직 없어 공허) · 양성 대조: 시험판 hooks.json + 시작 판 sync-docs → 두 README `변경 필요` | `same=1` · `same=1` · `quote_in_hook_rows=0` |
| SC-11 | `SC11a rc=0 synced=1 need_any=0` · `SC11b rc=0 onboarding=0 planning=0 rust=0` · `SC11c 1 1 1 1 1` | `SC11a rc=0 synced=1 need_any=0` · `SC11b rc=1 onboarding=1 planning=1 rust=1` · `SC11c 1 1 1 1 1` |
| SC-12 | `blocks=0/4 counts=0/4 names=0/4 outside_counts=7 outside_lists=2` · `SC12a rc=1 root=0` · `probe_block_21=0` | `blocks=4/4 counts=4/4 names=4/4 outside_counts=0 outside_lists=0` · `SC12a rc=1 root=1` · `write_rc=0 recheck_rc=0` · `probe_block_21=1` |
| ER-01 | 실행기 없음 | `ER01d` ~ `ER01h` 모두 `rc=2`, (d) ~ (g) `named=1` · `MUT_OK` 다섯 |
| ER-02 | `ER02 rc=0 named=0` | `ER02 rc=1 named=1` |
| AR-01 | `AR01 got=0 exact=0` | `AR01 got=15 exact=1 extra=[] missing=[]` |
| AR-02 | `hunks=0 outside=0` 둘 · 양성 대조 `f81568d..origin/main` → `hunks=6 outside=6` · `hunks=4 outside=4` | `validate=[hunks=5 outside=0] guide=[hunks=5 outside=0]` |
| AR-03 | `commits=0 mixed=0` | `commits=14 mixed=0` |
| AR-04 | `seal_broken=0 shared_same=3/3 harness_extra=0` · 양성 대조 사본 `SEAL_BROKEN` | 같음 |
| AR-05 | `notes=0` | `tokens=13/13` · 한 글자 뺀 notes `12/13` |
| AP-01 | `added_versions=0 hardcoded_pattern=0` · 양성 대조 14 | 같음 |
| AP-02 | `force_push=0` · 양성 대조 1 | 같음 |
| AP-03 | `bare_open=0` · `v6_rc=0 [Total: 14 plugins, 14 OK]` · 양성 대조 `bare 1` | 같음 |
| RE-01 | 실행기 없음 | `RE01 rc=0 total=[Total: 14 passed, 0 failed]` |
| RE-02 | `runner_import=NA runner_self_root=NA sync_collectors=5 insights_readers=2` · 양성 대조 1 · 6 | `runner_import=1 runner_self_root=0 sync_collectors=5 insights_readers=2` |
| DG-01 | `release_sh_changed=0` | 같음 |
| DG-02 | `README.md=21` · `onboarding-kit=2` · `planning-kit=8` · `rust-kit=17` · 가이드 `30` · `py_compile=4/5` (실행기 없음) · `json=4/4` · `actionlint_rc=0` | `md_worse=0 notes_warn=0` (`21->15 2->2 8->6 17->15 30->30`) · `py_compile=5/5 json=4/4 actionlint_rc=0` |
| DG-05 | 22 줄 `rc=0` · `feedback-agg-test SKIP (yq 없음)` | 22 줄 `rc=0` · SKIP 1 · 새 단계 `rc=0` |

## Skill

- [ ] SK-00: N/A (바뀌는 파일에 스킬 · 에이전트 파일이 없다 — 측정: `scope.sh` 의 `SK00 skill_agent_changed=0`, 기대 집합은 AR-01 의 열다섯 경로)

## Script

- [ ] SC-01: 카이젠 회귀 패턴 실행기가 두 `assertions.json` 의 패턴을 모두 실제로 돌린다 — 끝 판에서 `python3 scripts/run-kaizen-assertions.py` 가 `harness/evals/kaizen/*/assertions.json` 을 모두 찾아 `file_contains` 패턴마다 `PASS ` 또는 `FAIL ` 로 시작하고 `<카이젠 폴더>/<키>` 를 담은 줄을 하나씩 찍으며, 종료 코드 0 · `PASS` 줄 14 · `FAIL` 줄 0 · 아홉 짝(`contract-kaizen/ambiguous-conditions` · `contract-kaizen/category-bias` · `contract-kaizen/low-coverage` · `contract-kaizen/vacuous-boilerplate` · `evaluator-kaizen/l3-miss` · `evaluator-kaizen/false-approve` · `evaluator-kaizen/reject-loop` · `evaluator-kaizen/vacuous-zero` · `evaluator-kaizen/silent-check`)이 모두 `PASS` 줄에 있고 끝줄이 `Total: 14 passed, 0 failed` 다 [exact, enumerated]
      (측정: `asr.sh` 의 `SC01 rc=0 pass=14 fail=0 pairs=9/9 total=[Total: 14 passed, 0 failed]` ·
       알려진 답: 두 JSON 의 패턴 수를 손으로 센 6 + 8 = 14, 시작 판 대상 파일에 파이썬 `re.findall` 로 센 열넷이 모두 1 건 이상(3 · 19 · 2 · 2 · 2 · 2 · 3 · 7 · 5 · 7 · 1 · 2 · 1 · 1) — 봉인 전 시험 실행기로 같은 줄, 종료 코드 0 ·
       음성 대조: SC-02 — 패턴을 세지 않거나 픽스처를 대조하지 않는 실행기는 SC-02 의 세 사본에서 종료 코드 0 을 낸다)
- [ ] SC-02: 실행기가 통과해선 안 되는 세 사본에서 종료 코드 1 을 낸다 — 끝 판 사본에서 (a) `evaluator-kaizen` `silent-check` 셋째 패턴을 없는 글자 `없는글자-zz9` 로 바꾸면 `FAIL` 줄에 `evaluator-kaizen/silent-check` 가 있고 끝줄 `Total: 13 passed, 1 failed` (b) 키 없는 픽스처 `fixture-feedback-data/orphan-probe.yaml` 을 더하면 `FAIL` 줄에 `orphan-probe` (c) 픽스처 `l3-miss.yaml` 을 지우면(키는 남김) `FAIL` 줄에 `l3-miss` [exact]
      (측정: `asr.sh` 의 `SC02a rc=1 fail_line=1 total=[Total: 13 passed, 1 failed]` · `SC02b rc=1 fail_line=1` · `SC02c rc=1 fail_line=1`. 사본마다 `MUT_OK` 가 찍혀야 망가뜨리기가 적용된 것이다 ·
       봉인 전: 시험 실행기로 세 줄 모두 위 값, `MUT_OK` 셋. 시작 판에는 실행기가 없어 `NO_RUNNER` 종료 코드 2)
- [ ] SC-03: CI 의 Plugin Validation 묶음이 실행기를 돈다 — 끝 판 `.github/workflows/ci.yml` 의 `validate:` 묶음 안(`playwright:` 앞)에 `run: python3 scripts/run-kaizen-assertions.py` 줄이 정확히 1 개이고 파일 전체에도 1 개다 [exact]
      (측정: `asr.sh` 의 `SC03 validate_job=1 whole_file=1`. 그 줄을 로컬에서 돌린 결과는 SC-01 · DG-05, 문법은 DG-02 (d). 시작 판 `0 0`)
- [ ] SC-04: 처리 배정표 검사기 `--final` 이 Phase 번호와 대상 계약 슬러그의 번호를 맞대 본다 — 끝 판 검사기로 (a) 지금 배정표 그대로 종료 코드 0 · `TRACKING_TABLE_OK` (b) Phase 6 행 아홉의 대상 계약 `kaizen-0924-p06-design-kit` 을 `kaizen-0924-p05-flutter-toolkit` 로 바꾼 사본에서 종료 코드 1 · `TRACKING_TABLE_FAIL` · `Phase 6` 을 담은 `<n>행` 문제 줄 9 개 (c) 같은 사본을 `--final` 없이 돌리면 종료 코드 0 (기본 모드 그대로) (d) Phase 12 행 셋의 슬러그를 옛 꼴 `kaizen-phase12-oracle-positive-control` 로 바꾼 사본에서 종료 코드 0 (`-pNN-` 꼴과 `phaseN` 꼴을 둘 다 번호로 읽는다) (e) 슬러그에서 Phase 번호를 못 읽으면 통과시키지 않는다 — Phase 3 행 하나의 대상 계약을 `kaizen-0924-final` 로 바꾼 사본에서 종료 코드 1 · `TRACKING_TABLE_FAIL` · `kaizen-0924-final` 을 담은 `<n>행` 문제 줄 1 개 [exact]
      (측정: `ins.sh` 의 `SC04a rc=0 ok=1` · `SC04b rc=1 fail=1 rows=9` · `SC04c basic rc=0` · `SC04d rc=0` · `SC04e rc=1 fail=1 rows=1` — 바꾼 수는 `MUT count_before=9` · `3` · `4` (Phase 3 행 넷 가운데 첫 줄만 바꾼다) ·
       알려진 답: 배정표 Phase 6 행 9 개 · Phase 12 행 3 개(`| kaizen-0924-p06-design-kit |` · `| kaizen-0924-p12-reflect-kit |` 칸을 센 값) · 봉인 전 시험 검사기로 `rows=9` ·
       음성 대조: 번호 맞대기를 빼면 (b) 가, 못 읽는 번호를 통과시키면 (e) 가 시작 판처럼 `rc=0 fail=0 rows=0`)
- [ ] SC-05: 감사 기록 도구가 붙이는 항목이 같은 제목 경고를 내지 않고 앞 항목과 빈 줄로 떨어지며 옛 내용을 건드리지 않는다 — (a)(b)(c) 는 끝 판 도구 하나와 `# 감사 기록` / 빈 줄 / `본문 한 줄` 세 줄짜리 기록만 든 작은 사본에 `--cycle-id cyc-a` · `cyc-b` · `cyc-c` 세 항목을 붙여 잰다: (a) `## ` 머리 셋 모두 바로 앞 줄이 빈 줄 (b) 도구가 찍은 `### ` 소제목 아홉이 모두 오늘 날짜와 그 항목 사이클 이름을 담는다 (c) markdownlint(v0.23.2 · MD013 끔) `MD024` 0 · `MD022`+`MD032` 0 (d) 끝 판 `.harness/.meta/orchestrator-audit-log.md` 사본에 `--cycle-id cyc-z` 한 항목을 붙이면 새 파일이 옛 파일 바이트로 그대로 시작하고 `MD024` 경고 수가 붙이기 전과 같다 [exact]
      (측정: `aud.sh` 의 `rc=[0 0 0]` · `SC05 heads=3 blank_before=3/3 subs=9 sub_ok=9/9` · `SC05 md024=0 md022_032=0` · `SC05r rc=0 prefix=1 md024_before=8 md024_after=8` ·
       봉인 전 시작 판: `blank_before=0/1 sub_ok=0/3 md022_032=1` · `SC05r … md024_before=8 md024_after=11` (고정 소제목 셋이 겹침 — MD024 를 세는 측정이 살아 있다는 양성 대조))
- [ ] SC-06: 감사 기록 도구가 수동 감시 거리를 받는다 — `--watch "<글>"` 을 여러 번 주면 그 항목의 감시 목록 소제목 아래에 글마다 목록 줄이 생기고, `--failures` 실패 목록과 함께 주면 둘 다 나오며, 실패도 수동 감시도 없는 항목에만 `특별 감시 대상 없음` 이 나온다. `--help` 출력에 `--watch` 가 있다 [exact]
      (측정: SC-05 와 같은 작은 사본 — `cyc-a` 는 옵션 없이, `cyc-b` 는 `--watch "감시 하나" --watch "감시 둘"`, `cyc-c` 는 `--failures`(`x-check` 한 줄) `--watch "감시 셋"`. `aud.sh` 의 `SC06 a_none=1 b_items=11 b_none=0 c_items=11 c_none=0` · `SC06 help_watch` 1 이상 ·
       봉인 전 시작 판: `--watch` 를 몰라 `rc=[0 2 2]` · `b_items=00` · `help_watch=0`)
- [ ] SC-07: 킷 넷 hooks.json 명령이 빈칸 든 설치 경로에서도 실행된다 — `design-kit` · `flutter-toolkit` · `harness` · `reflect-kit` 네 `hooks/hooks.json` 의 명령 10 개가 모두 `${CLAUDE_PLUGIN_ROOT}` 로 시작하는 경로를 큰따옴표 안에 두고, 따옴표 글자를 뺀 JSON 이 시작 판과 같으며(이벤트 · matcher · 명령 뜻 그대로), `…/plug root/<킷>` 경로에 같은 상대 경로의 흉내 스크립트를 둔 채 `sh -c` 로 돌리면 10 개 모두 그 스크립트를 인자까지 그대로 실행한다 — `CLAUDE_PLUGIN_ROOT` 환경 변수로 펼칠 때와 경로 글자로 바꿔 넣을 때 둘 다 [exact, enumerated]
      (측정: `hooks.sh` 의 `SC07 commands=10 quoted=10/10 same_shape=4/4 ran_env=10/10 ran_sub=10/10`. 킷 넷은 `find . -path ./.claude/worktrees -prune -o -path ./node_modules -prune -o -name hooks.json -print` 실측으로 정했다 ·
       양성 대조: 시작 판 `quoted=0/10 ran_env=0/10 ran_sub=0/10` — 따옴표가 없으면 빈칸 경로에서 열 개 모두 실패한다)
- [ ] SC-08: V8 이 따옴표 없는 명령을 잡고, 따옴표를 붙여도 실행 비트 검사를 계속한다 — 끝 판 `python3 scripts/validate-plugin.py --check=hook-exec` 로 (a) 그대로면 종료 코드 0 · `Total: 14 plugins, 14 OK` · V8 줄이 harness `5 hook` · flutter-toolkit `1 hook` · design-kit `1 hook` 을 담는다 (b) `harness/scripts/run-guard.sh` 실행 비트를 뗀 사본 → 종료 코드 0 아님 · harness V8 줄 `FAIL` · 출력에 `run-guard.sh` (c) design-kit 명령을 따옴표 없는 옛 꼴 `${CLAUDE_PLUGIN_ROOT}/scripts/env-check.sh` 로 되돌린 사본 → 종료 코드 0 아님 · design-kit V8 줄 `FAIL` · 출력에 `design-kit/hooks/hooks.json` (d) design-kit 명령을 `"${CLAUDE_PLUGIN_ROOT}"/scripts/env-check.sh` 꼴로 쓴 사본 → 종료 코드 0 · design-kit V8 줄 `1 hook` (e) reflect-kit 첫 명령을 인터프리터 경유 따옴표 없는 꼴 `bash ${CLAUDE_PLUGIN_ROOT}/hooks/log-prompt.sh` 로 쓴 사본 → 종료 코드 0 아님 · reflect-kit V8 줄 `FAIL` · 출력에 `reflect-kit/hooks/hooks.json` [exact]
      (측정: `v8.sh` 의 `SC08a` ~ `SC08e` 다섯 줄 ·
       봉인 전 시작 판: (a) 같은 값 · (b) `rc=2 … FAIL named=1` · (c) `rc=0 … 1 hook … OK named=0` · (d) `rc=0 … 직접 실행 hook 스크립트 없음` (따옴표를 붙이면 실행 비트 검사가 조용히 빠지는 결함 재현) · (e) `rc=0 named=0` ·
       음성 대조: 따옴표 검사를 빼면 (c)(e) 가 종료 코드 0, 따옴표를 알아보는 첫 토큰 판정을 빼면 (d) 가 `1 hook` 이 아니다)
- [ ] SC-09: 검증 가이드 V8 절이 따옴표 규칙을 적는다 — 끝 판 `harness/docs/guides/plugin-validation-guide.md` 의 `### V8` 부터 `### V9` 앞까지에 `따옴표` 가 1 회 이상, hooks.json 에 쓰는 따옴표 꼴 `\"${CLAUDE_PLUGIN_ROOT}` 가 1 회 이상, `FAIL` 을 담은 예시 코드 블록이 2 개 이상(실행 비트 · 따옴표) 있고, FAIL 예시 블록 밖에 따옴표 없는 명령 꼴(JSON 값 첫머리의 `${CLAUDE_PLUGIN_ROOT}` · 줄 안 코드의 셸 꼴 — 변수 이름만 든 줄 안 코드는 뺀다)이 0 개다 [structural]
      (측정: `v8.sh` 끝 두 줄 — `guide.py "$T/E"` 가 `SC09 v8_section=1` · `quote_word` 1 이상 · `json_quoted_example` 1 이상 · `fail_blocks` 2 이상 · `unquoted_outside_fail=0` ·
       봉인 전 시작 판 `quote_word=0 json_quoted_example=0 fail_blocks=1 unquoted_outside_fail=3` (`:397` 하나 · `:401` 둘), 시험판 `6 3 2 0` ·
       쓰기 주의: 산문 안 줄 안 코드로 따옴표 없는 옛 꼴을 예로 들어도 `unquoted_outside_fail` 이 는다 — 옛 꼴은 `FAIL` 을 담은 예시 코드 블록 안에만 둔다)
- [ ] SC-10: sync-docs 훅 표가 따옴표 붙은 명령에서도 스크립트 이름만 보인다 — 끝 판 `design-kit/README.md` · `reflect-kit/README.md` 가 시작 판과 바이트로 같고, 두 파일 훅 표 줄(`|` 다음 백틱으로 시작하는 줄)에 `.sh"` 가 0 개다. 끝 판 `--check-only` 가 두 README 를 `동기화됨` 으로 보는 것은 SC-11 (a) [exact, enumerated]
      (측정: `sdocs.sh` 의 `SC10 design-kit/README.md same=1` · `SC10 reflect-kit/README.md same=1` · `SC10 quote_in_hook_rows=0` ·
       양성 대조: 시험판 hooks.json(따옴표 붙임)에 시작 판 `scripts/sync-docs.py` 를 돌리면 `design-kit/README.md: 변경 필요` · `reflect-kit/README.md: 변경 필요` (봉인 전 실측) — 훅 표를 고치지 않으면 CI `Sync docs check` 가 멈춘다)
- [ ] SC-11: sync-docs 가 onboarding-kit · planning-kit · rust-kit README 의 AUTO 블록을 읽는다 — (a) 끝 판 `python3 scripts/sync-docs.py --check-only` 종료 코드 0 · `모든 README가 동기화 상태입니다.` · `변경 필요` 0 줄 (b) 끝 판 사본에서 `onboarding-kit/README.md` · `planning-kit/README.md` · `rust-kit/README.md` 첫 스킬 AUTO 블록의 첫 표 줄 끝에 ` ZZCORRUPT` 를 붙이면 종료 코드 1 이고 세 README 모두 `변경 필요` 줄이 있다 (c) 끝 판 세 README 가 `## 스킬` 줄을 1 개씩, `planning-kit` · `rust-kit` 가 `## 에이전트` 줄을 1 개씩 갖는다 (다시 만들어진 표가 제목을 삼키지 않는다) [exact, enumerated]
      (측정: `sdocs.sh` 의 `SC11a rc=0 synced=1 need_any=0` · `SC11b rc=1 onboarding=1 planning=1 rust=1` · `SC11c headings onboarding_skill=1 planning_skill=1 planning_agent=1 rust_skill=1 rust_agent=1` ·
       봉인 전 시작 판: (b) `rc=0 onboarding=0 planning=0 rust=0` — 표지를 못 읽어 망가진 표를 못 본다 (결함 재현) · 시험판 위 기대값 그대로)
- [ ] SC-12: 루트 README 킷 절의 스킬 수 · 목록을 sync-docs 가 센다 — (a) 끝 판 `README.md` 의 `### harness` · `### flutter-toolkit` · `### rust-kit` · `### react-kit` 네 절에 AUTO 블록이 하나씩 있고, 블록마다 그 킷의 `skills/*/SKILL.md` 수 `스킬 N종`, 에이전트가 있으면 `agents/*.md` 수 `에이전트 M종`, 스킬 폴더 이름 전부가 들어 있다 (b) AUTO 블록을 뺀 나머지에 스킬 수 글자(정규식 `(스킬|워크플로우) ?[0-9]+ ?종|[0-9]+ ?종 ?\+ ?[0-9]+ ?에이전트|등 [0-9]+ ?종`)가 0 개이고 옛 목록 두 꼴(`**제공 스킬:** api,` · harness 표 첫 줄 `` | `init` | `/harness init` | ``)이 0 개 (c) 끝 판 사본 `flutter-toolkit/skills/zz-probe/SKILL.md` 를 더하면 `--check-only` 출력에 `README.md: 변경 필요` 가 있고, `sync-docs.py` 쓰기 뒤 flutter-toolkit 절 블록에 `스킬 21종` 과 `zz-probe` 가 있으며 쓰기와 다시 잰 `--check-only` 가 둘 다 종료 코드 0 [exact, enumerated]
      (측정: `sdocs.sh` 의 `SC12 end blocks=4/4 counts=4/4 names=4/4 outside_counts=0 outside_lists=0` · `SC12a rc=1 root=1` · `SC12a write_rc=0 recheck_rc=0` · `SC12 probe_block_21=1` ·
       알려진 답: `find <킷>/skills -mindepth 2 -maxdepth 2 -name SKILL.md | wc -l` 과 `find <킷>/agents -maxdepth 1 -name '*.md' | wc -l` 을 시작 판에서 센 harness 9 · 1, flutter-toolkit 20 · 1, rust-kit 16 · 1, react-kit 21 · 3 — 시험판 블록이 같은 수를 담았다 ·
       봉인 전 시작 판: `blocks=0/4 outside_counts=7 outside_lists=2` · `SC12a root=0` — 루트 README 는 스킬 수가 바뀌어도 모른다 (결함 재현))

## Error

- [ ] ER-01: 실행기는 읽지 못하는 입력을 통과(0)나 실패(1)로 섞지 않고 종료 코드 2 와 원인 이름을 낸다 — 끝 판 사본에서 (d) `contract-kaizen/assertions.json` 끝에 `,` 를 붙이면 출력에 `contract-kaizen/assertions.json` (e) 대상 파일을 `harness/agents/no-such-zz9.md` 로 바꾸면 출력에 `no-such-zz9.md` (f) type 을 `file_absent` 로 바꾸면 출력에 `file_absent` (g) `category-bias` 패턴을 `(` 로 바꾸면 출력에 `category-bias` (h) `assertions.json` 둘을 다 지우면 — 다섯 모두 종료 코드 2 [exact]
      (측정: `asr.sh` 의 `ER01d` ~ `ER01h` 가 모두 `rc=2`, (d) ~ (g) 는 `named=1`. 봉인 전 시험 실행기로 같은 값 · `MUT_OK` 다섯)
- [ ] ER-02: sync-docs 는 짝 없는 AUTO 표지를 조용히 넘기지 않는다 — 끝 판 사본 `tone-kit/README.md` 끝에 여는 표지 `<!-- AUTO:skills -->` 한 줄을 더하면 `--check-only` 종료 코드가 0 이 아니고, `동기화됨` 이 아닌 출력 줄에 `tone-kit/README.md` 가 있다. 루트 `CLAUDE.md` 본문 줄 안 코드의 `<!-- AUTO:xxx -->` 언급은 표지로 세지 않는다 (SC-11 (a) 가 종료 코드 0) [exact]
      (측정: `sdocs.sh` 의 `ER02` 줄 — 종료 코드 0 아님 · `named` 1 이상 · 봉인 전 시작 판 `rc=0 named=0`, 시험판 `rc=1 named=1`)

## Architecture

- [ ] AR-01: 바뀐 구현 파일이 정확히 15 경로다 [exact, enumerated]
      (Given: 이 계약 구현 커밋이 가지 `chore/ak-c1-harness-scripts` 에 다 들어가고 그 가지에 main 을 합치지 않은 상태 ·
       측정: `scope.sh` — `git diff --name-only "$B" "$END" -- . ':(exclude).harness'` 정렬 출력이 도우미 `WANT` 열다섯 줄과 정확히 일치(`AR01 got=15 exact=1 extra=[] missing=[]`). 생성물은 없어 뺄 경로가 없다.
       상한 `END` 는 `common.sh` 가 가지 끝(가지를 지웠으면 그 가지를 합친 병합 커밋의 둘째 부모)으로 푼다 — `HEAD` 금지. 시작 판 `got=0`)
- [ ] AR-02: 다른 가지와 같이 고친 두 파일의 바뀐 자리가 V8 에만 있다 — `scripts/validate-plugin.py` 의 바뀐 덩어리가 모두 시작 판 626 ~ 716 줄(V8 머리 주석부터 V9 머리 주석 앞까지) 안에, `harness/docs/guides/plugin-validation-guide.md` 의 바뀐 덩어리가 모두 시작 판 391 ~ 417 줄(`### V8` 부터 `### V9` 앞 구분선까지) 안에 있고 두 파일 모두 덩어리가 1 개 이상이다. V10 함수 · V6 · 가이드 머리 설정(판 번호) · 변경 이력 표는 그대로다 [exact]
      (Given: AR-01 과 같다 · 측정: `scope.sh` 의 `AR02 validate=[hunks=N outside=0] guide=[hunks=N outside=0]` (N 1 이상, `git diff -U0` 의 옛 줄 범위로 판정) ·
       줄 범위는 시작 판 쪽 줄 번호다 — `git diff -U0` 덩어리 머리의 옛 줄(`-s,n`)로 재므로 이 가지 안에서 V8 앞뒤에 줄을 끼워도 범위가 밀리지 않는다. 순수 끼움 덩어리(`-s,0`)는 시작 판 `s` 줄 뒤에 끼운 것이라 `s` 로 판정한다 ·
       양성 대조: 같은 식을 `f81568d..origin/main`(#111 V10 변경)에 돌리면 `hunks=6 outside=6` · `hunks=4 outside=4` (봉인 전 실측) · 줄 근거 `scripts/validate-plugin.py:626` · `:717` · 가이드 `:391` · `:418`)
- [ ] AR-03: 킷 폴더를 건드린 커밋은 그 킷 폴더 하나만 건드린다 — `B..END` 의 병합 아닌 커밋마다 최상위 폴더를 모아, `.claude-plugin/marketplace.json` 의 킷 이름이 둘 이상이거나 킷 하나에 다른 최상위(`.harness` · `scripts` · `README.md` 등)가 섞인 커밋이 0 개다 [exact]
      (Given: AR-01 과 같다 · 측정: `scope.sh` 의 `AR03 commits=N mixed=0` (킷이 바뀌는 커밋만 일곱이라 N 7 이상) ·
       양성 대조: 릴리스 커밋 `01f7c95` 의 최상위 폴더는 킷 열넷과 `.claude` · `.claude-plugin` · `README.md` — 이 식이 섞인 커밋으로 센다 (봉인 전 `git show --name-only` 로 확인))
- [ ] AR-04: `.harness` 는 이 계약 몫만 바뀌고 공유 기록은 그대로다 — 끝 판 `.harness` 아래 계약 파일 전부에 `verify_seal` 을 돌려 `SEAL_BROKEN` 0 개, `.harness/.meta/orchestrator-audit-log.md` · `.harness/stale-values.yaml` · `.claude/kaizen-input/insights-report.md` 세 파일이 시작 판과 같고, `.harness` 아래 바뀐 경로는 이 계약 · 개정 · 피드백 세 파일(`sprint-*-after-0924-scripts.md`)과 notes `.harness/.meta/after-kaizen-0926/c1a-notes.md` 뿐이다 [exact, enumerated]
      (Given: AR-01 과 같다 · 측정: `scope.sh` 의 `AR04 seal_broken=0 shared_same=3/3 harness_extra=0` ·
       양성 대조: `.harness/sprint-contract-kaizen-0924-final.md` 사본의 `AR-02` 조건 줄에 글자를 더하면 `verify_seal` 이 `SEAL_BROKEN` (봉인 전 실측))
- [ ] AR-05: 넘길 것을 notes 에 남긴다 — 끝 판 `.harness/.meta/after-kaizen-0926/c1a-notes.md` 가 있고 열세 글자 `72d6ddd` · `--watch` · `.claude/skills/kaizen-orchestrator/SKILL.md` · `harness/skills/contract-kaizen/SKILL.md` · `harness/skills/evaluator-kaizen/SKILL.md` · `F1H-40` · `F1H-94` · `docs/harness/plugin-validation.html` · `feat/v10-fence-commonmark` · `harness/evals/kaizen/evaluator-kaizen/assertions.json` · `plugin-validation-guide.md` · `reflect-kit/README.md:156` · `릴리스` 가 각각 1 회 이상 있다 (뜻은 `## 범위 경계` 「넘길 것」) [exact, enumerated]
      (측정: `scope.sh` 의 `AR05 notes=1 tokens=13/13 miss=[]` · 시작 판 `notes=0` · 시험 notes 로 `13/13`, 한 글자를 뺀 시험 notes 로 `12/13 miss=[ reflect-kit/README.md:156]` (봉인 전 실측))

## Anti-patterns

- [ ] AP-01: 버전을 하드코딩하지 않는다 — plugin.json에서 읽어야 한다. 이번 변경에 적용: `scripts/` · `.github/` 에 더한 줄의 버전꼴 글자(`[0-9]+\.[0-9]+\.[0-9]+`)가 0 개이고, 구현 파일 전체 더한 줄에 project.yaml 패턴 `hardcoded.*version` 이 0 개다 [exact]
      (측정: `scope.sh` 의 `AP01 added_versions=0 hardcoded_pattern=0` · 양성 대조: 같은 식을 `git diff 77ed5bb f81568d -- .claude-plugin` 에 돌리면 14 (봉인 전 실측))
- [ ] AP-02: force push 금지 — 구현 파일에 더한 줄에 project.yaml 패턴 `git push.*--force` 가 0 개다. 이 단계는 푸시 자체를 하지 않는다 [exact]
      (측정: `scope.sh` 의 `AP02 force_push=0` · 양성 대조: `grep -cE 'git push.*--force' harness/docs/guides/skill-design-guide.md` 1 (`:802`, 봉인 전 실측))
- [ ] AP-03: bare code fence 금지 — 끝 판 `python3 scripts/validate-plugin.py --check=code-fence` 가 종료 코드 0 · `Total: 14 plugins, 14 OK` (가이드 · 킷 README 몫)이고, V6 가 안 보는 루트 `README.md` 와 notes 의 언어 힌트 없는 여는 펜스가 0 개다 [exact]
      (측정: `dg.sh` 의 `AP03 bare_open=0` · `AP03 v6_rc=0 [Total: 14 plugins, 14 OK]` · 양성 대조: `# x` / 빈 줄 / 힌트 없는 여는 펜스 / `a` / 닫는 펜스 다섯 줄 사본에 같은 식 → `bare 1` (봉인 전 실측))

## Reusability

- [ ] RE-01: 다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다 — 새 실행기는 어느 폴더에서 불러도 같은 결과를 낸다: 끝 판 실행기를 `/` 에서 부르면 종료 코드 0 · 끝줄 `Total: 14 passed, 0 failed` [exact]
      (측정: `asr.sh` 의 `RE01 rc=0 total=[Total: 14 passed, 0 failed]` · 봉인 전 시험 실행기로 같은 값)
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다 — (a) 새 실행기는 저장소 뿌리를 공용 모듈 `scripts/plugin_utils.py` 에서 받는다: `grep -c 'from plugin_utils import' scripts/run-kaizen-assertions.py` 1 이상 · `grep -cE '^REPO_ROOT *=|Path\(__file__\)' scripts/run-kaizen-assertions.py` 0 (b) sync-docs 는 루트 README 블록에도 기존 스킬 · 에이전트 수집 함수를 쓴다: `grep -cE 'iter_skills\(|iter_agents\(|/ "skills"|skills/\*|os\.listdir|\.iterdir\(' scripts/sync-docs.py` 가 시작 판과 같은 5 (c) 배정표 검사기는 표 읽기를 새로 만들지 않는다: `grep -cE 'def split_row|def table_blocks' scripts/check-insights-tracking.py` 가 시작 판과 같은 2 [exact]
      (측정: 끝 판 폴더 `$T/E` 에서 위 grep 셋 · 양성 대조: (a) 같은 식을 `scripts/append-audit-log.py` 에 돌리면 1 (자체 계산 꼴) (b) sync-docs 사본에 `os.listdir(ROOT / "k" / "skills")` 한 줄을 더하면 6 (봉인 전 실측))

## Diagnostics

- [ ] DG-01: N/A (commands.analyze `bash -n scripts/release.sh` 는 `scripts/release.sh` 만 잰다 — 이번 변경 파일과 교집합 0. 측정: `scope.sh` 의 `DG01 release_sh_changed=0`. 대신 DG-02 (b)(c)(d) 가 바뀐 파이썬 · JSON · CI 파일을 잰다)
- [ ] DG-02: 편집기 경고 대응 검사 — (a) 바뀐 마크다운 다섯(`README.md` · `onboarding-kit/README.md` · `planning-kit/README.md` · `rust-kit/README.md` · `harness/docs/guides/plugin-validation-guide.md`)의 markdownlint(v0.23.2 · MD013 끔) 경고 수가 파일마다 시작 판 이하이고 notes 는 0 (b) 바뀐 파이썬 다섯(`scripts/run-kaizen-assertions.py` · `scripts/check-insights-tracking.py` · `scripts/append-audit-log.py` · `scripts/validate-plugin.py` · `scripts/sync-docs.py`)이 `python3 -W error -m py_compile` 성공 (c) hooks.json 넷이 `python3 -m json.tool` 성공 (d) `actionlint .github/workflows/ci.yml` 종료 코드 0. `diagnostics.ide_exclude` 는 빈 목록이라 뺄 것이 없고 스펠체크는 사용자 규칙대로 뺀다 [exact, enumerated]
      (측정: `dg.sh` 의 `DG02 md_worse=0 notes_warn=0` · `DG02 py_compile=5/5 json=4/4 actionlint_rc=0` · 시작 판 경고 수 `README.md=21` · `onboarding-kit/README.md=2` · `planning-kit/README.md=8` · `rust-kit/README.md=17` · 가이드 `30`. markdownlint 가 없으면 `MDL_MISSING` 으로 멈춘다)
- [ ] DG-03: N/A (commands.test `bash scripts/release.sh 2>&1 || true` 는 `scripts/release.sh` 만 돈다 — 교집합 0, 측정은 DG-01 과 같다. 대신 DG-05)
- [ ] DG-04: N/A (구동할 앱 · 서버가 없다 — 바뀐 실행 파일은 명령줄 검사 도구 다섯이고 SC · ER 조건이 모두 실제로 돌려서 잰다. 측정: AR-01 목록에 서버 진입점 0)
- [ ] DG-05: CI 단계를 로컬에서 모두 돌려 통과한다 [exact]
      (Given: 작업 폴더 `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak-c1` 의 `HEAD` 가 `END` 이고 `git status --porcelain --untracked-files=no` 가 빈 출력 ·
       측정: `TMPDIR=<폴더> bash /Users/jackson/Hub/10_Dev/claude-plugins/.harness/handoff/2026-09-26-tools/ci-local.sh <작업 폴더>` 의 요약 22 줄이 모두 `rc=0` (yq 가 없으면 `feedback-agg-test SKIP (yq 없음)` 한 줄은 허용), 그 도구가 모르는 새 단계 `python3 scripts/run-kaizen-assertions.py` 를 작업 폴더에서 돌려 종료 코드 0.
       이 도구는 저장소에 커밋되지 않은 본 체크아웃 쪽 파일이다(봉인 전 `shasum -a 256 … | cut -c1-16` = `a415eaff98a46b86`, 35 줄). 파일이 없거나 이 값과 다르면 도구 대신 `.github/workflows/ci.yml` 의 `run:` 줄을 작업 폴더에서 하나씩 돌리는 것이 정상 경로이고, 그때 기대값은 `run:` 줄마다 종료 코드 0 (yq 없는 줄만 예외) 이다 · 봉인 전: 시작 판에서 22 줄 `rc=0` · SKIP 1 (2026-09-26 11:4x), 시험판에서 같은 값 · 새 단계 종료 코드 0)
