---
feature: "rust-kit 특정 앱 이름 일괄 치환 (대응표 하나)"
slug: after-0924-rust-app-name
created: "2026-09-26 12:04"
complexity: "중간"
conditions: 17
status: done
owner_session: bda55d45-296c-491f-89ba-b52042d58e72
conditions_digest: sha256:85bde798533363bf
locked_at: "2026-09-26 12:29"
---

## 배경

rust-kit 문서 14 개에 특정 앱 이름(`fit-pal` · `fitpal`)이 66 줄 · 75 번 남아 있다. 카이젠 2026-09-24 Phase 9 가 세어 두고 넘겼고
(`.harness/.meta/kaizen-0924/phase9-notes.md:130`), F1 킷 후속이 「한 파일씩」 으로 다음 사이클에 넘겼다
(`.harness/.meta/kaizen-0924/f1-kit-followups-notes.md:82` · `:156` — rust-preflight Gotcha 1 에도 남아 있다고 적었다).
핸드오프 `.harness/handoff/2026-09-26-0110.md` §C3 · §C4 4 번이 정리 방식을 사용자 결정으로 남겼고,
사용자가 이 세션(`bda55d45-296c-491f-89ba-b52042d58e72`, AskUserQuestion)에서 **일괄 치환**을 골랐다.

이 계약은 그 결정을 대응표 하나로 옮긴다. 코드 이름(크레이트 이름 · DB(데이터베이스) 주소 예시)은 rust-kit 이 이미 쓰는 중립 이름 `myapp`
(`rust-kit/skills/rust-grpc/SKILL.md:27` 의 `package myapp.v1;`)으로, 「출처: fit-pal `server/CLAUDE.md`」 같은 출처 문장은
앱 이름 없이 「실사용 프로젝트의 서버 규칙」 으로 바꾼다. 대응표는 아래 `## GAP 분석` 의 표이고, 적용은 `## 회귀 게이트` 의 `apply-map.py` 한 번이다.
대응표 밖에서 손으로 고치는 곳은 없다.

사용자 승인(Step 5): 사용자가 「다음 세션에서 직접할 일을 다 실행하고 이어질것도 실행해」(세션 기록
`/Users/jackson/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/de8c7935-a5b6-4df5-9106-fafa73c288a0.jsonl`, user `2026-09-26T01:04:21.505Z`)와
「나한테 물어보지 말고 자동으로 끝까지」(같은 기록 `2026-09-24T04:04:16.964Z`)로 맡겼다. 이 계약의 합의는 그 위임으로 받은 것으로 적는다.
정리 방식(일괄) 자체는 사용자가 이 세션에서 직접 골랐다. 사용자가 할 일: 없음

## 리서치 소스

바깥 자료를 새로 찾지 않는다. 입력은 모두 레포 안에 있다.

- `.harness/handoff/2026-09-26-0110.md` §C3 rust-kit 줄 · §C4 4 번
- `.harness/.meta/kaizen-0924/phase9-notes.md:130` · `f1-kit-followups-notes.md:82` · `:156`
- 대상 파일 14 개 (아래 Pre-Edit 표) · 중립 이름 근거 `rust-kit/skills/rust-grpc/SKILL.md:27`
- 규칙: `harness/references/contract-schema.md` (봉인 · 범위 조건 · 양성 대조 · 알려진 답 대조) · `tone-kit/references/locale-korean.md` §2 · §8

## GAP 분석 · 대응표 · 개선안

### 복잡도 (Step 1)

| 축 | 물음 | 값 |
| -- | ---- | -- |
| 레이어 수 | 몇 계층을 관통하는가 | 하나 — 킷 문서(스킬 본문 · 참조 문서) |
| 공개 계약 변경 | 외부에 드러나는 형태가 바뀌는가 | 예 — 스킬이 내놓는 예시 이름이 바뀐다 (rust-init §4a 멤버 크레이트 틀의 `name = "fitpal-api"` 등) |
| 소비면 존재 | 반대편이 있는가 | 아니오 — 레포 안에서 이 문서를 옮겨 쓰는 곳(`docs/rust-kit/*.html` 21 쪽 · `rust-kit/README.md` · `rust-kit/evals/evals.json`)에 앱 이름 0 건. AR-02 가 잰다 |
| 되돌아갈 위험 | 기존 동작이 깨질 수 있는가 | 예 — 표 칸 안 치환 20 여 곳 · 코드 블록 안 이름 · 네 스킬이 같은 문구를 지켜야 하는 원칙 줄 |

둘이 예라 **중간**이다. 공개 계약 변경이 예라 Step 2.5 에 따라 소비 쪽을 AR-02 로 따로 둔다(소비자 없음을 끝 판에서 다시 잰다).
기능 조건은 여덟(SK-01 ~ SK-04 · ER-01 · AR-01 · AR-02 · DG-05)이다.

### 설정 리터럴 대조 (Step 1.2)

| config key | project.yaml 에서 읽은 값 | 계약에 쓴 값 |
| ---------- | ------------------------- | ------------ |
| `commands.analyze` | `bash -n scripts/release.sh` | `bash -n scripts/release.sh` (DG-01 N/A 사유) |
| `commands.test` | `bash scripts/release.sh 2>&1 \|\| true` | 같음 (DG-03 N/A 사유) |
| `diagnostics.ide_exclude` | `[]` | `[]` (DG-02) |
| `contract_categories[].id` / `prefix` | Skill/SK · Script/SC · Error/ER · Architecture/AR | 같음 |
| `anti_patterns[].id` / `message` | AP-01 버전 하드코딩 · AP-02 force push · AP-03 bare fence · AP-04 frontmatter name | AP-03 · AP-04 (AP-01 은 바뀌는 줄에 킷 버전이 없고, AP-02 는 이 계약이 push 하지 않아 뺀다) |

### Pre-Edit 감사 (Step 1.4)

2026-09-26 에 `grep -rniE 'fit[-_ ]?pal' rust-kit` 로 66 줄을 뽑고 줄마다 앞뒤를 읽었다(rust-init `:80` ~ `:264` · rust-model `:462` ~ `:490` ·
rust-run `:18` ~ `:26` · rust-preflight `:60` ~ `:70` · project-detection `:138` ~ `:150` 은 블록째 읽었다). 낱말 수는 `fit-pal` 60 · `fitpal` 15, 합 75. 파일별 수는 `grep -ciE` (줄) · `grep -oiE … | wc -l` (낱말)로 셌다.

| 대상 파일 | 줄 · 낱말 | 실제 Read 증거 (`파일:라인`) | 발견한 것 | 조건 |
| --------- | --------- | ---------------------------- | --------- | ---- |
| `rust-kit/references/project-detection.md` | 2 · 2 | `:147` · `:148` `fitpal-api` 두 번 (실측 기록 문장) | 크레이트 이름 | SK-01 · SK-03 |
| `rust-kit/skills/rust-api/SKILL.md` | 3 · 3 | `:18` · `:19` · `:23` 「출처: fit-pal `server/CLAUDE.md`」 | 네 스킬 공통 원칙의 출처 | SK-04 |
| `rust-kit/skills/rust-audit/SKILL.md` | 5 · 5 | `:20` 「fit-pal 패턴:」 · `:27` 「fit-pal §아키텍처 3번」 · `:100` · `:103` · `:113` 표 행 끝 칸 | 표 칸 안 치환 | ER-01 · DG-02 |
| `rust-kit/skills/rust-audit/references/audit-criteria.md` | 17 · 17 | `:3` · `:20` · `:22` · `:30` · `:33` · `:35` · `:44` · `:51` · `:52` · `:54` · `:55` · `:56` · `:66` · `:67` · `:75` · `:76` · `:91` (17 줄, `:3` 말고 전부 표 행 끝 칸) | 표 칸 안 치환 · 편집기 경고 162 건이 이미 있다(MD060 표 정렬 등) | ER-01 · DG-02 |
| `rust-kit/skills/rust-auth/SKILL.md` | 1 · 1 | `:17` 「fit-pal 실무 기준」 | — | SK-02 |
| `rust-kit/skills/rust-error/SKILL.md` | 3 · 3 | `:13` · `:14` 「(fit-pal CLAUDE.md 금지 사항)」 · `:15` 「fit-pal `workspace.lints.rust` 및 `CLAUDE.md` §금지 사항」 | `:15` 는 앱 이름만 지우면 `CLAUDE.md` 가 홀로 남아 사용자 전역 규칙 파일로 읽힌다 → 대응표 6 행 | SK-02 |
| `rust-kit/skills/rust-feature/SKILL.md` | 4 · 4 | `:18` · `:19` · `:20` 출처 · `:22` 「동일 문구·동일 출처(fit-pal `server/CLAUDE.md`)」 | 같은 문구 규칙(Sibling Consistency) 선언 | SK-04 |
| `rust-kit/skills/rust-init/SKILL.md` | 8 · 9 | `:22` · `:23` · `:25` 출처 · `:27` 같은 선언 · `:121` 개인 절대 경로 `/Users/jackson/Hub/10_Dev/fit-pal/server` · `:212` toml 주석 · `:235` `name = "fitpal-api"` · `:257` | 코드 블록 안 크레이트 이름 · 개인 경로 | SK-01 · SK-03 · SK-04 |
| `rust-kit/skills/rust-middleware/SKILL.md` | 2 · 2 | `:14` 「(fit-pal 기준 `tower-http = "0.6.8"`)」 · `:15` | — | SK-02 |
| `rust-kit/skills/rust-model/SKILL.md` | 6 · 6 | `:13` 「fit-pal 같은 대형 프로젝트」 · `:17` · `:48`(표) · `:249` · `:468` · `:470` 코드 주석 `fitpal-migration` | 표 칸 · 코드 주석 | SK-02 · ER-01 |
| `rust-kit/skills/rust-preflight/SKILL.md` | 5 · 10 | `:15` Gotcha 1 「fit-pal `server-preflight` Makefile 타겟」 · `:19` DB 주소 `postgres://fitpal:fitpal@localhost:5432/fitpal` · `:20` · `:21` · `:67` 표 「(fit-pal: `cargo run -p fitpal-migration`)」 | Gotcha 1 (지난 사이클 메모) · 괄호 안에 실제 이름과 예시 이름이 섞일 자리 → 대응표 2 · 3 행 | SK-01 · SK-03 |
| `rust-kit/skills/rust-run/SKILL.md` | 6 · 9 | `:16` · `:21` · `:22` `-p fitpal-api` · `:24` DB 주소 + `-p fitpal-migration` · `:25` · `:26` | 한 목록 안에 이름 셋 — 갈리면 예시가 틀린다 | SK-03 |
| `rust-kit/skills/rust-service/SKILL.md` | 2 · 2 | `:16` · `:18` 출처 | 네 스킬 공통 원칙 | SK-04 |
| `rust-kit/skills/rust-test/SKILL.md` | 2 · 2 | `:15` · `:19` 출처 · `:338` ~ `:344` 이미 있는 중립 이름 `-p my-lib` · `-p my-api` | 다른 예시 블록이라 대응표 밖 — 그대로 둔다 | SK-03 |

같은 이름이 rust-kit 밖에도 있다(범위 밖 — `## 범위 경계` 에 파일과 건수만). 옵션은 사용자가 일괄로 정했으므로 옵션 표는 두지 않는다.

### 대응표 (적용 순서대로, 위 행이 먼저)

`## 회귀 게이트` 의 `apply-map.py` 안 `MAP` 이 이 표와 같은 내용이다(봉인 전에 두 목록이 글자 그대로 같은지 확인했다 — `## 회귀 게이트` 봉인 전 실측 표 1 행).
찾는 글자는 정확히 그 글자만 찾는다(대소문자 · 공백 · 백틱 포함). 오른쪽 끝 열은 시작 판 14 파일에서 그 행이 바꾸는 횟수다.

| 행 | 찾는 글자 | 바꿀 글자 | 종류 | 횟수 |
| -- | --------- | --------- | ---- | ---- |
| 1 | ``fit-pal `/Users/jackson/Hub/10_Dev/fit-pal/server` 실무 프로젝트 구조`` | `실사용 프로젝트의 서버 구조` | 출처 (개인 경로 포함) | 1 |
| 2 | `(fit-pal 패턴: ` | `(예: ` | 예시 괄호 | 1 |
| 3 | `(fit-pal: ` | `(예: ` | 예시 괄호 | 1 |
| 4 | `postgres://fitpal:fitpal@localhost:5432/fitpal` | `postgres://myapp:myapp@localhost:5432/myapp` | 코드 (DB 주소) | 2 |
| 5 | `fitpal-` | `myapp-` | 코드 (크레이트 `fitpal-api` · `fitpal-migration`) | 9 |
| 6 | ``fit-pal `workspace.lints.rust` 및 `CLAUDE.md` §금지 사항`` | ``실사용 프로젝트의 `workspace.lints.rust` 및 서버 규칙 §금지 사항`` | 출처 | 1 |
| 7 | ``fit-pal `workspace.lints.`` | ``실사용 프로젝트의 `workspace.lints.`` | 출처 | 2 |
| 8 | `fit-pal workspace.lints 실무 기준` | `실사용 프로젝트의 workspace.lints 기준` | 출처 | 1 |
| 9 | `` fit-pal `server/CLAUDE.md` `` | `실사용 프로젝트의 서버 규칙` | 출처 | 20 |
| 10 | `` fit-pal `CLAUDE.md` `` | `실사용 프로젝트의 서버 규칙` | 출처 | 10 |
| 11 | `fit-pal CLAUDE.md` | `실사용 프로젝트의 서버 규칙` | 출처 | 1 |
| 12 | `fit-pal §` | `실사용 프로젝트의 서버 규칙 §` | 출처 | 2 |
| 13 | `fit-pal 같은 대형 프로젝트` | `대형 실사용 프로젝트` | 문장 | 1 |
| 14 | `fit-pal 실무 ` (끝 공백 포함) | `실사용 프로젝트 ` | 문장 (실무 기준 · 세트 · 패턴) | 6 |
| 15 | `` fit-pal `server-preflight` `` | `` 실사용 프로젝트의 `server-preflight` `` | 출처 (Makefile 타겟) | 2 |
| 16 | `fit-pal` | `실사용 프로젝트` | 나머지 전부 | 10 |

행 9 · 10 · 15 의 찾는 글자는 `fit-pal` 로 시작해 닫는 백틱에서 끝나고, 행 15 의 바꿀 글자도 닫는 백틱에서 끝난다(겹 백틱 코드 칸 안쪽 앞뒤 공백 한 칸씩은 표기일 뿐이다). 낱말 셈: 행 1 은 `fit-pal` 둘, 행 4 는 `fitpal` 셋을 한 번에 지운다 —
`fit-pal` 2 + 1 + 1 + 1 + 2 + 1 + 20 + 10 + 1 + 2 + 1 + 6 + 2 + 10 = 60, `fitpal` 3 × 2 + 9 = 15, 합 75 로 시작 판 낱말 수와 같다.

판단 기록 (사용자 결정 밖에서 정한 것 — 저장소 안 근거):

- 중립 이름은 `myapp` 계열 하나다. rust-kit 에 이미 `package myapp.v1;` (`rust-grpc/SKILL.md:27`)가 있고 작업 지시 예시도 `myapp` · `myapp-api` 다.
  rust-test `:338` ~ `:344` 의 `my-api` · `my-lib` 는 다른 예시 블록이라 대응표 밖이며 건드리지 않는다
- 크레이트 이름은 지난 실측 기록 문장(rust-preflight `:21` 「2026-06 실측 … `cargo run -p fitpal-migration` 후 통과」, project-detection `:147`) 안에서도 바꾼다.
  사용자 결정이 「앱 이름 0 건」 이고, 원래 이름은 `.harness/.meta/evidence/phase9.md` (7 건) 같은 기록에 남아 있어 추적할 수 있다
- 행 2 · 3 — 괄호 안에서 「실사용 프로젝트」 와 예시 이름 `myapp` 이 한 괄호에 섞이지 않게 「예:」 로 바꾼다
- 행 6 — 앱 이름만 지우면 `CLAUDE.md` 가 홀로 남아 사용자 전역 규칙 파일과 헷갈린다. 출처 쪽 말을 다른 줄과 같은 「서버 규칙」 으로 맞춘다
- 행 7 · 8 — 「실사용 프로젝트 `workspace…`」 는 조사가 빠져 어색해 「의」 를 넣고, 「실사용 … 실무」 겹말을 뺀다
- 행 15 — rust-preflight `:15` · `:19` 의 「fit-pal `server-preflight` …」 도 행 16 으로 가면 「실사용 프로젝트 `server-preflight`」 로 조사가 빠진다.
  행 7 과 같이 「의」 를 넣는다(봉인 전 교차 진단 지적 — 행 16 이 받는 나머지 열 곳은 「… 패턴」 · 「… 기준」 · 「(… deny)」 처럼 이름 뒤에 바로 명사가 붙어 조사 없이 읽힌다)
- 바뀐 글은 톤 규칙 번역투 여섯 패턴(`tone-kit/references/locale-korean.md` §8 G-1)에 걸리지 않는다 — 봉인 전 실측 표 2 행

### 개선안 (구현 단계가 할 일, 조건 순서)

1. `## 회귀 게이트` 첫 명령으로 이 계약에서 `apply-map.py` 를 떼어 낸다
2. 작업 폴더 `W` 에서 `python3 apply-map.py "$W" <아래 sprint-scope 블록의 rust-kit 14 경로>` 를 **한 번** 돌린다. 표준 오류가
   `rule1=1 rule2=1 rule3=1 rule4=2 rule5=9 rule6=1 rule7=2 rule8=1 rule9=20 rule10=10 rule11=1 rule12=2 rule13=1 rule14=6 rule15=2 rule16=10` 와 같아야 한다 (SK-02)
3. 그 밖의 손 편집은 하지 않는다. 결과가 이상하면 파일을 고치지 말고 개정 파일 `.harness/sprint-amendments-after-0924-rust-app-name.md` 에 대응표 행을 더하는 개정을 적는다
4. `git add <14 경로> && git commit -o <14 경로>` — rust-kit 만 담은 커밋 하나 (AR-01)
5. 전역 규칙에 따라 tone-kit:tone-guide 1 단계(규칙 읽기)와 5 단계(바뀐 파일 대조)를 돈다 — 대응표가 글을 정하므로 5 단계에서 위반이 나오면 3 번과 같이 개정으로 간다

## 범위 경계

- 시작 커밋: `f81568d8fbf58382172281388ec5d7756f9f46b2` (워크트리 `ak-c4c` 를 `origin/main` 에서 만든 판, `git -C <W> log -1` 로 확인). 끝 판은 가지 `chore/ak-c4c` 의 끝이고,
  가지를 합친 뒤 지웠으면 커밋 메시지에 `chore/ak-c4c` 가 든 병합 커밋의 둘째 부모다(`m.sh` 의 `end_ref`). 해석이 안 되면 `END_UNRESOLVED` 를 찍고 멈춘다 — `HEAD` 로 재지 않는다
- 고치는 파일은 아래 블록의 rust-kit 14 개뿐이고 새 파일은 없다. `.harness/` 쪽은 이 계약 · 개정 파일 · QA 피드백이다(AR-01 은 `.harness/` 를 경로 목록이 아니라 봉인으로 잰다)

```text
# sprint-scope
rust-kit/references/project-detection.md
rust-kit/skills/rust-api/SKILL.md
rust-kit/skills/rust-audit/SKILL.md
rust-kit/skills/rust-audit/references/audit-criteria.md
rust-kit/skills/rust-auth/SKILL.md
rust-kit/skills/rust-error/SKILL.md
rust-kit/skills/rust-feature/SKILL.md
rust-kit/skills/rust-init/SKILL.md
rust-kit/skills/rust-middleware/SKILL.md
rust-kit/skills/rust-model/SKILL.md
rust-kit/skills/rust-preflight/SKILL.md
rust-kit/skills/rust-run/SKILL.md
rust-kit/skills/rust-service/SKILL.md
rust-kit/skills/rust-test/SKILL.md
.harness/
```

- 커밋 규칙: 봉인 커밋은 계약 파일 하나만 싣는다(Step 6.7). 구현 커밋은 rust-kit 14 경로만 `git add <경로> && git commit -o <경로>` 로 싣고 `.harness/` 를 섞지 않는다.
  한 커밋에 킷 하나 — 이 계약은 rust-kit 하나라 구현 커밋 안에 다른 킷 경로가 없다. `git add -A` · `git stash` · push · 가지 바꾸기는 하지 않는다
- 버전 올림 · `marketplace.json` · 킷 `plugin.json` 은 건드리지 않는다 — 릴리스는 부모가 PR 을 합친 뒤 한다(핸드오프 재개 지시 5 번)
- 범위 밖 기록 (고치지 않고 파일과 건수만 — 부모가 문서를 다시 만들 때 함께 본다, 2026-09-26 시작 판에서 `grep -ciE 'fit[-_ ]?pal'`):
  `docs/rust/research-log.md` 7 건 · `docs/rust-kit/*.html` 21 쪽 0 건. rust-kit 밖 다른 킷 · `.harness/` 기록에도 같은 이름이 있으나 이 계약의 범위(다른 킷)가 아니다
- 판정 한계: 바뀐 문장이 사람에게 자연스럽게 읽히는지는 결정론 측정이 없다 — 대응표 문구를 봉인 전에 사람이 읽어 정했고(`## GAP 분석` 판단 기록),
  조건은 그 문구가 정확히 그대로 들어갔는지(SK-02)와 예시 이름이 한 벌인지(SK-03)를 잰다
- 커버리지 해소: SK-01 · SK-02 · ER-01 · DG-02 · AP-04 — 14 경로는 위 sprint-scope 블록과 `m.sh` 의 `FILES` 가 같은 목록이다(AR-01 `scope_block` 이 둘을 대조한다)
- 커버리지 해소: AR-02 — `rust-kit/README.md` · `rust-kit/evals/evals.json` · `docs/rust/research-log.md` 는 `m.sh` AR-02 갈래의 글자 그대로이고, `docs/rust-kit/*.html` 은 같은 갈래의 `find docs/rust-kit -type f -name '*.html'` 가 끝 판에서 펼친다(시작 판 21 쪽:
  `async-concurrency` · `authentication` · `axum-patterns` · `caching` · `ci-cd` · `concurrency-guard-protocol` · `docker` · `error-handling` · `graphql` · `grpc-tonic` 외 11 쪽 — 측정은 목록이 아니라 수 21 과 적중 0 을 본다)
- 커버리지 해소: SK-03 — 산문의 `myapp.v1` · `postgres://…` 주소 넷은 측정 절 기대 출력 한 줄(`m SK-03` 첫 줄) 안에 같은 글자로 들어 있다. 그 줄은 공백을 품어 검출기가 대상 토큰으로 보지 않을 뿐이다
- 측정 폭: SK-03 의 (a)(b)(c) 셈은 14 파일이 아니라 끝 판 rust-kit 전체를 잰다(RE-02 는 14 파일로 좁혀 새 앞말만 본다). 예시 이름이 한 벌인지는 킷 전체에서 봐야 해서다.
  그래서 기대값 일부는 이 계약이 고치지 않는 세 파일에서 나온다: `rust-kit/skills/rust-grpc/SKILL.md` 의 `myapp.v1` 1 ·
  `rust-kit/skills/rust-build/SKILL.md` 의 `crate-name` 1 · `rust-kit/skills/rust-docker/SKILL.md` 의 `postgres://...` 2 와 `postgres://postgres:password@db:5432/appdb` 1.
  나머지 `postgres://...` 5 · `<migration-crate>` · `my-api` · `my-lib` · `myapp` 계열은 14 파일 안이다. 이 세 파일이 다른 작업으로 바뀌면 치환이 맞아도 SK-03 값이 달라지니, SK-03 이 기대와 다르면 이 세 파일의 변경부터 본다
  (SK-02 `others_changed=0` 이 이 가지 안에서는 세 파일이 그대로임을 함께 잰다)
- 측정 폭: AR-01 `seal_broken` 은 이 계약 하나가 아니라 끝 판 `.harness/` 의 `sprint-contract*.md` 전부(`history/` 포함)를 잰다 — 이 계약 봉인은 `this=` 가 따로 본다.
  봉인 전 실측(시작 판 `git archive` 사본): 83 개(`.harness/` 바로 아래 82 · `history/` 1), `SEAL_OK` 73 · `SEAL_ABSENT` 10 · `SEAL_BROKEN` 0. 끝 판은 시작 판에 이 가지 커밋만 얹은 판이므로,
  `seal_broken` 이 1 이상이면 이 가지가 옛 계약 조건 줄을 건드린 것이다(시작 판을 옮기는 다른 작업이 아니다)
- 커버리지 해소: DG-05 — `scripts/validate-plugin.py` · `scripts/run-evals.py` · `scripts/check-stale-values.py` · `scripts/check-docs-links.py` (와 `sync-docs.py` · `sync-evals.py`)는 `m.sh` 의 `_checks` 목록 글자다. 기대 출력의 `validate-rust` · `validate-all` · `run-evals` · `stale-values` · `docs-links` 가 그 이름이다
- 커버리지 해소: SK-04 — 네 스킬 `rust-init` · `rust-feature` · `rust-service` · `rust-api` 는 `m.sh` SK-04 갈래의 `for s in …` 글자다

## 회귀 게이트 — 측정 공통 정의와 봉인 전 실측

모든 조건은 아래 세 블록(`apply-map.py` · `units.py` · `m.sh`)을 쓴다. 이 계약에서 떼어 한 폴더에 두고 **bash** 로 `m.sh` 를 읽은 뒤 `m <조건 ID>` 를 부른다.
`m.sh` 는 시작 커밋과 끝 판을 임시 폴더에 풀어 재므로 작업 폴더를 바꾸지 않는다. 판정은 출력 값으로 한다(`m` 의 종료 코드는 판정하지 않는다).

```bash
# 떼어 내기 — 첫 줄이 `# file: <이름>` 인 bash · python 블록만 그 이름으로 저장한다
CF=/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak-c4c/.harness/sprint-contract-after-0924-rust-app-name.md
K=$(mktemp -d)
awk -v K="$K" '/^```(bash|python)$/{b=1; f=""; next} b && /^```$/{b=0; f=""; next}
  b && f=="" && /^# file: /{f=K "/" $(3); print > f; next} b && f!=""{print > f}' "$CF"
ls "$K"   # apply-map.py  m.sh  units.py
K="$K" bash -c '. "$K/m.sh" && m SK-01'   # 조건 하나를 잰다
```

준비 단계 실측(2026-09-26): `command -v bash` → `/opt/homebrew/bin/bash` (GNU bash 5.3.9) · bash 안 `type grep` → `/usr/bin/grep` (BSD grep 2.6.0 — 이 맥 zsh 의 `grep` 은 ugrep 이라 측정은 bash 로만) ·
`command -v python3` → `/Users/jackson/.pyenv/versions/3.14.3/bin/python3` · `ML` 기본값(`m.sh` 10 행) `--version` 첫 줄 `markdownlint-cli2 v0.23.2 (markdownlint v0.41.1)`.
`ML` 이 없으면 DG-02 가 `ML_MISSING` 을 찍는다 — 빈 임시 폴더에서 `npm install --no-save markdownlint-cli2@0.23.2` 뒤 `ML=<그 폴더>/node_modules/.bin/markdownlint-cli2` 로 넘긴다
(편집기 확장이 싣는 판이고, 줄 길이 규칙 MD013 을 끈 설정은 `m.sh` 가 임시 폴더에 만든다). 워크트리를 지운 뒤 재면 `W=<레포 경로>` 로 넘긴다.
`TMPDIR` 은 다른 세션과 겹치지 않게 스크래치 폴더로 두고 읽는다.

```python
# file: apply-map.py
"""대응표를 위에서 아래 순서로 한 번씩 적용한다.

쓰기: python3 apply-map.py <루트> <파일>...   — 파일을 제자리에서 고친다
대조: python3 apply-map.py --stdout <파일>    — 고친 내용을 표준 출력으로 낸다
규칙별 바꾼 횟수를 표준 오류로 낸다 (`rule<번호>=<횟수>`).
"""
import sys

MAP = [
    ("fit-pal `/Users/jackson/Hub/10_Dev/fit-pal/server` 실무 프로젝트 구조", "실사용 프로젝트의 서버 구조"),
    ("(fit-pal 패턴: ", "(예: "),
    ("(fit-pal: ", "(예: "),
    ("postgres://fitpal:fitpal@localhost:5432/fitpal", "postgres://myapp:myapp@localhost:5432/myapp"),
    ("fitpal-", "myapp-"),
    ("fit-pal `workspace.lints.rust` 및 `CLAUDE.md` §금지 사항", "실사용 프로젝트의 `workspace.lints.rust` 및 서버 규칙 §금지 사항"),
    ("fit-pal `workspace.lints.", "실사용 프로젝트의 `workspace.lints."),
    ("fit-pal workspace.lints 실무 기준", "실사용 프로젝트의 workspace.lints 기준"),
    ("fit-pal `server/CLAUDE.md`", "실사용 프로젝트의 서버 규칙"),
    ("fit-pal `CLAUDE.md`", "실사용 프로젝트의 서버 규칙"),
    ("fit-pal CLAUDE.md", "실사용 프로젝트의 서버 규칙"),
    ("fit-pal §", "실사용 프로젝트의 서버 규칙 §"),
    ("fit-pal 같은 대형 프로젝트", "대형 실사용 프로젝트"),
    ("fit-pal 실무 ", "실사용 프로젝트 "),
    ("fit-pal `server-preflight`", "실사용 프로젝트의 `server-preflight`"),
    ("fit-pal", "실사용 프로젝트"),
]


def apply(text, counts):
    for i, (old, new) in enumerate(MAP, 1):
        counts[i] = counts.get(i, 0) + text.count(old)
        text = text.replace(old, new)
    return text


def main(argv):
    counts = {}
    if argv[1:2] == ["--stdout"]:
        with open(argv[2], encoding="utf-8", newline="") as f:
            sys.stdout.write(apply(f.read(), counts))
    else:
        root = argv[1]
        for rel in argv[2:]:
            p = f"{root}/{rel}"
            with open(p, encoding="utf-8", newline="") as f:
                src = f.read()
            with open(p, "w", encoding="utf-8", newline="") as f:
                f.write(apply(src, counts))
    sys.stderr.write(" ".join(f"rule{i}={counts.get(i, 0)}" for i in range(1, len(MAP) + 1)) + "\n")


if __name__ == "__main__":
    main(sys.argv)
```

```python
# file: units.py
"""예시 단위마다 프로젝트 이름 앞말을 모은다.

단위: 코드 블록 하나, 또는 코드 블록 밖의 빈 줄로 나뉜 문단 하나.
앞말: `-p <앞말>-api|-migration` · `name = "<앞말>-api|-migration` · 백틱 뒤 `<앞말>-api|-migration` · `postgres://<앞말>:` 의 <앞말>.
출력 한 줄: units=<앞말이 든 단위 수> split=<앞말이 둘 이상인 단위 수> stems=<전체 앞말, 쉼표>
split 이 1 이상이면 그 단위의 파일:첫 줄과 앞말을 SPLIT 줄로 먼저 낸다.
"""
import re
import sys

PAT = re.compile(r'(?:-p |name = "|`)([a-z][a-z0-9]*)(?=-(?:api|migration)\b)|postgres://([a-z][a-z0-9]*):')


def units(path):
    with open(path, encoding="utf-8") as f:
        lines = f.read().split("\n")
    cur, start, in_code = [], 1, False
    for no, line in enumerate(lines, 1):
        fence = line.lstrip().startswith("```")
        if fence and not in_code:
            if cur:
                yield start, cur
            cur, start, in_code = [line], no, True
            continue
        if fence and in_code:
            cur.append(line)
            yield start, cur
            cur, start, in_code = [], no + 1, False
            continue
        if not in_code and line.strip() == "":
            if cur:
                yield start, cur
            cur, start = [], no + 1
            continue
        if not cur:
            start = no
        cur.append(line)
    if cur:
        yield start, cur


def main(root, rels):
    n_units = n_split = 0
    all_stems = set()
    for rel in rels:
        for start, body in units(f"{root}/{rel}"):
            stems = {a or b for a, b in PAT.findall("\n".join(body))}
            if not stems:
                continue
            n_units += 1
            all_stems |= stems
            if len(stems) > 1:
                n_split += 1
                print(f"SPLIT {rel}:{start} {','.join(sorted(stems))}")
    print(f"units={n_units} split={n_split} stems={','.join(sorted(all_stems))}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2:])
```

```bash
# file: m.sh
# after-0924-rust-app-name 측정 공통 정의. bash 에서 `K=<측정 파일 폴더> . "$K/m.sh"` 로 읽은 뒤 `m <조건 ID>` 를 부른다.
# 판정은 출력 값으로 한다. 두 판(시작 커밋 · 끝 판)을 임시 폴더에 풀어 재므로 작업 폴더는 바뀌지 않는다.
if [ -z "${BASH_VERSION:-}" ]; then echo NOT_BASH; return 2 2>/dev/null || exit 2; fi
: "${K:?K 에 측정 파일 폴더를 넣는다}"
W=${W:-/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak-c4c}
BASE=${BASE:-f81568d8fbf58382172281388ec5d7756f9f46b2}
BRANCH=${BRANCH:-chore/ak-c4c}
CF_REL=.harness/sprint-contract-after-0924-rust-app-name.md
ML=${ML:-/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/bda55d45-296c-491f-89ba-b52042d58e72/scratchpad/c4c/mdlint/node_modules/.bin/markdownlint-cli2}
APP='fit[^[:alnum:]]{0,2}pal'
FILES='rust-kit/references/project-detection.md
rust-kit/skills/rust-api/SKILL.md
rust-kit/skills/rust-audit/SKILL.md
rust-kit/skills/rust-audit/references/audit-criteria.md
rust-kit/skills/rust-auth/SKILL.md
rust-kit/skills/rust-error/SKILL.md
rust-kit/skills/rust-feature/SKILL.md
rust-kit/skills/rust-init/SKILL.md
rust-kit/skills/rust-middleware/SKILL.md
rust-kit/skills/rust-model/SKILL.md
rust-kit/skills/rust-preflight/SKILL.md
rust-kit/skills/rust-run/SKILL.md
rust-kit/skills/rust-service/SKILL.md
rust-kit/skills/rust-test/SKILL.md'

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
T=$(mktemp -d "${TMPDIR:-/tmp}/c4c.XXXXXX")
trap 'rm -rf "$T"' EXIT
mkdir -p "$T/base" "$T/end"
printf '{ "config": { "MD013": false } }\n' > "$T/cfg.markdownlint-cli2.jsonc"
git -C "$W" archive "$BASE" | tar -x -C "$T/base" && git -C "$W" archive "$END" | tar -x -C "$T/end" \
  || { echo SNAPSHOT_FAIL; return 2 2>/dev/null || exit 2; }
for _f in $FILES; do
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
_ml() {  # _ml <판 폴더> — 파일:줄 규칙 목록
  (cd "$1" && "$ML" --config "$T/cfg.markdownlint-cli2.jsonc" $FILES 2>&1) \
    | grep -E '^rust-kit/.*:[0-9]+(:[0-9]+)? error MD' | awk '{split($1,a,":"); split($3,r,"/"); print a[1] ":" a[2], r[1]}' | LC_ALL=C sort
}
_checks() {  # _checks <판 폴더> — 저장소 검사 일곱의 종료 코드
  (cd "$1" || exit 2
   for c in "validate-rust:scripts/validate-plugin.py rust-kit" "sync-docs:scripts/sync-docs.py --check-only" \
            "sync-evals:scripts/sync-evals.py --check-only" "run-evals:scripts/run-evals.py" \
            "stale-values:scripts/check-stale-values.py" "docs-links:scripts/check-docs-links.py" \
            "validate-all:scripts/validate-plugin.py"; do
     n=${c%%:*}; a=${c#*:}
     # shellcheck disable=SC2086
     python3 $a >/dev/null 2>&1; printf '%s=%s ' "$n" "$?"
   done; echo)
}

m() {
  case "$1" in
  SK-01)
    e=$(grep -rniE "$APP" "$T/end/rust-kit"); erc=$?
    el=$(printf '%s' "$e" | grep -c .)
    bl=$(grep -rniE "$APP" "$T/base/rust-kit" | grep -c .)
    ue=$(grep -rn '/Users/' "$T/end/rust-kit" | grep -c .)
    ub=$(grep -rn '/Users/' "$T/base/rust-kit" | grep -c .)
    g1=$(grep -E '^1\. \*\*순서 변경 금지\*\*' "$T/end/rust-kit/skills/rust-preflight/SKILL.md")
    echo "SK-01 end_lines=$el end_rc=$erc base_lines=$bl users_end=$ue users_base=$ub" \
      "g1_lines=$(printf '%s' "$g1" | grep -c .) g1_app=$(printf '%s' "$g1" | grep -ciE "$APP") g1_neutral=$(printf '%s' "$g1" | grep -c '실사용 프로젝트')"
    ;;
  SK-02)
    bl=$(cd "$T/base" && grep -rliE "$APP" rust-kit | LC_ALL=C sort)
    [ "$bl" = "$FILES" ] && lm=1 || lm=0
    mkdir -p "$T/mapped"; (cd "$T/base" && tar -cf - $FILES) | tar -x -C "$T/mapped"
    cnt=$(python3 "$K/apply-map.py" "$T/mapped" $FILES 2>&1 >/dev/null)
    same=0; dif=0
    for f in $FILES; do
      if cmp -s "$T/mapped/$f" "$T/end/$f"; then same=$((same+1)); else dif=$((dif+1)); echo "DIFF $f"; fi
    done
    oth=0
    while IFS= read -r f; do
      printf '%s\n' "$FILES" | grep -qxF "$f" && continue
      cmp -s "$T/base/$f" "$T/end/$f" 2>/dev/null || { oth=$((oth+1)); echo "OTHER $f"; }
    done < <( (cd "$T/base" && find rust-kit -type f; cd "$T/end" && find rust-kit -type f) | LC_ALL=C sort -u)
    echo "SK-02 list_match=$lm files=$(printf '%s\n' "$FILES" | grep -c .) same=$same diff=$dif others_changed=$oth counts=[$cnt]"
    ;;
  SK-03)
    tok=$(grep -rhoE 'myapp[-_.a-z0-9]*' "$T/end/rust-kit" | LC_ALL=C sort | uniq -c | awk '{printf "%s:%s,", $2, $1}')
    fam=$(grep -rhoiE 'my_app|my-app|example[-_]app' "$T/end/rust-kit" | grep -c .)
    pk=$(grep -rhoE 'cargo (run|test|build|clippy)[^`|]*-p [^ `|)]+' "$T/end/rust-kit" | grep -oE -- '-p [^ `|)]+' | LC_ALL=C sort | uniq -c | awk '{printf "%s:%s,", $3, $1}')
    url=$(grep -rhoE 'postgres://[^ `|)]+' "$T/end/rust-kit" | LC_ALL=C sort | uniq -c | awk '{printf "%s:%s,", $2, $1}')
    un=$(cd "$T/end" && python3 "$K/units.py" . $FILES)
    echo "SK-03 tokens=$tok other_families=$fam pkgs=$pk urls=$url $(printf '%s\n' "$un" | tail -1)"
    printf '%s\n' "$un" | grep '^SPLIT' || true
    ;;
  SK-04)
    o="SK-04"
    for s in rust-init rust-feature rust-service rust-api; do
      ne=$(grep -c '출처: 실사용 프로젝트의 서버 규칙' "$T/end/rust-kit/skills/$s/SKILL.md")
      nb=$(grep -cF '출처: fit-pal `server/CLAUDE.md`' "$T/base/rust-kit/skills/$s/SKILL.md")
      o="$o $s=$ne/$nb"
    done
    for s in rust-init rust-feature; do
      o="$o decl_$s=$(grep -cF '동일 출처(실사용 프로젝트의 서버 규칙)' "$T/end/rust-kit/skills/$s/SKILL.md")"
    done
    echo "$o"
    ;;
  ER-01)
    python3 - "$T/base" "$T/end" $FILES <<'PY'
import sys
b, e, files = sys.argv[1], sys.argv[2], sys.argv[3:]
nl = pp = fe = 0; odd = 0
for f in files:
    x = open(f"{b}/{f}", encoding="utf-8").read().split("\n")
    y = open(f"{e}/{f}", encoding="utf-8").read().split("\n")
    if len(x) == len(y):
        nl += 1
        if all(p.count("|") == q.count("|") for p, q in zip(x, y)):
            pp += 1
        for no, (p, q) in enumerate(zip(x, y), 1):
            if p != q and q.count("`") % 2:
                odd += 1; print(f"ODD {f}:{no}")
    if sum(l.lstrip().startswith("```") for l in x) == sum(l.lstrip().startswith("```") for l in y):
        fe += 1
print(f"ER-01 files={len(files)} nlines_eq={nl} pipes_eq={pp} fences_eq={fe} odd_backtick_lines={odd}")
PY
    ;;
  AR-01)
    impl=$(_impl); [ "$impl" = "$FILES" ] && ex=1 || ex=0
    mixed=0
    for c in $(_commits); do
      fs=$(_files_of "$c")
      printf '%s\n' "$fs" | grep -q '^rust-kit/' && printf '%s\n' "$fs" | grep -qv '^rust-kit/' && { mixed=$((mixed+1)); echo "MIXED $c"; }
    done
    sc=$(git -C "$W" log --first-parent --diff-filter=A --format=%H "$BASE..$END" -- "$CF_REL" | tail -1)
    scn=0; [ -n "$sc" ] && scn=$(_files_of "$sc" | grep -c .)
    fi1=$(git -C "$W" log --first-parent --no-merges --format=%H "$BASE..$END" -- rust-kit | tail -1)
    before=0; [ -n "$sc" ] && [ -n "$fi1" ] && [ "$sc" != "$fi1" ] && git -C "$W" merge-base --is-ancestor "$sc" "$fi1" && before=1
    br=0; while IFS= read -r -d '' f; do verify_seal "$f"; done < <(find "$T/end/.harness" -type f -name 'sprint-contract*.md' -print0) > "$T/seals"
    br=$(grep -c '^SEAL_BROKEN' "$T/seals"); self=$(grep -F "$CF_REL" "$T/seals" | awk '{print $1}')
    blk=$(_scope "$T/end/$CF_REL"); want=$(printf '%s\n.harness/\n' "$FILES" | LC_ALL=C sort)
    [ -n "$blk" ] && [ "$blk" = "$want" ] && sb=1 || sb=0
    echo "AR-01 impl_files=$(printf '%s\n' "$impl" | grep -c .) exact=$ex mixed_commits=$mixed seal_commit_files=$scn seal_before_impl=$before seal_broken=$br this=$self scope_block=$sb"
    ;;
  AR-02)
    cons=$( (cd "$T/end" && find docs/rust-kit -type f -name '*.html'; echo rust-kit/README.md; echo rust-kit/evals/evals.json) | LC_ALL=C sort)
    hits=0; for f in $cons; do n=$(grep -ciE "$APP" "$T/end/$f"); hits=$((hits+n)); done
    rl=$(grep -ciE "$APP" "$T/end/docs/rust/research-log.md")
    echo "AR-02 consumers=$(printf '%s\n' "$cons" | grep -c .) app_hits=$hits research_log=$rl"
    ;;
  SC-00)
    echo "SC-00 release_paths=$(git -C "$W" log --first-parent --no-merges --format= --name-only "$BASE..$END" -- .claude-plugin rust-kit/.claude-plugin scripts | grep -c .)"
    ;;
  AP-03)
    (cd "$T/end" && python3 scripts/validate-plugin.py rust-kit --check=code-fence >/dev/null 2>&1); r=$?
    echo "AP-03 v6_rc=$r"
    ;;
  AP-04)
    python3 - "$T/base" "$T/end" $FILES <<'PY'
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
sk = [f for f in files if f.endswith("/SKILL.md")]
name = sum(1 for f in sk if fm(f"{e}/{f}") and any(l.startswith("name: ") for l in fm(f"{e}/{f}")))
same = sum(1 for f in sk if fm(f"{b}/{f}") is not None and fm(f"{b}/{f}") == fm(f"{e}/{f}"))
print(f"AP-04 skills={len(sk)} name={name} fm_same={same}")
PY
    ;;
  RE-01)
    echo "RE-01 added=$(git -C "$W" log --first-parent --no-merges --diff-filter=A --format= --name-only "$BASE..$END" -- . ':(exclude).harness' | grep -c .)"
    ;;
  RE-02)
    gb=$(grep -c 'package myapp\.v1;' "$T/base/rust-kit/skills/rust-grpc/SKILL.md")
    ge=$(grep -c 'package myapp\.v1;' "$T/end/rust-kit/skills/rust-grpc/SKILL.md")
    sb=$(cd "$T/base" && python3 "$K/units.py" . $FILES | tail -1 | sed 's/.*stems=//' | tr ',' '\n' | grep . | LC_ALL=C sort)
    se=$(cd "$T/end" && python3 "$K/units.py" . $FILES | tail -1 | sed 's/.*stems=//' | tr ',' '\n' | grep . | LC_ALL=C sort)
    new=$(LC_ALL=C comm -13 <(printf '%s\n' "$sb") <(printf '%s\n' "$se") | tr '\n' ',')
    echo "RE-02 grpc_base=$gb grpc_end=$ge new_stems=$new"
    ;;
  DG-01)
    echo "DG-01 release_sh=$(git -C "$W" log --first-parent --no-merges --format= --name-only "$BASE..$END" -- scripts/release.sh | grep -c .)"
    ;;
  DG-02)
    [ -x "$ML" ] || { echo "DG-02 ML_MISSING $ML"; return 2; }
    _ml "$T/base" > "$T/mlb"; _ml "$T/end" > "$T/mle"
    new=$(LC_ALL=C comm -13 "$T/mlb" "$T/mle")
    echo "DG-02 md=$(printf '%s\n' "$FILES" | grep -c .) base_warn=$(grep -c . "$T/mlb") end_warn=$(grep -c . "$T/mle") new=$(printf '%s' "$new" | grep -c .)"
    printf '%s' "$new" | grep . | sed 's/^/NEW /' || true
    ;;
  DG-04)
    echo "DG-04 non_md=$(_impl | grep -vc '\.md$')"
    ;;
  DG-05)
    echo "DG-05 base: $(_checks "$T/base")"
    echo "DG-05 end: $(_checks "$T/end")"
    ;;
  *) echo "UNKNOWN $1"; return 2 ;;
  esac
}
```

알려진 답 대조 입력(규칙마다 한 번)과 손으로 쓴 기대 출력 — `apply-map.py --stdout <입력>` 이 표준 오류에 규칙 열여섯 모두 `=1` 을 내고 표준 출력이 기대 출력과 `cmp` 로 같아야 한다.

```text
a fit-pal `/Users/jackson/Hub/10_Dev/fit-pal/server` 실무 프로젝트 구조 b
(fit-pal 패턴: x) (fit-pal: y)
postgres://fitpal:fitpal@localhost:5432/fitpal fitpal-api
fit-pal `workspace.lints.rust` 및 `CLAUDE.md` §금지 사항 | fit-pal `workspace.lints.clippy` | fit-pal workspace.lints 실무 기준
fit-pal `server/CLAUDE.md` / fit-pal `CLAUDE.md` / fit-pal CLAUDE.md / fit-pal §9
fit-pal 같은 대형 프로젝트 / fit-pal 실무 기준 / fit-pal `server-preflight` 타겟 / fit-pal deny
```

```text
a 실사용 프로젝트의 서버 구조 b
(예: x) (예: y)
postgres://myapp:myapp@localhost:5432/myapp myapp-api
실사용 프로젝트의 `workspace.lints.rust` 및 서버 규칙 §금지 사항 | 실사용 프로젝트의 `workspace.lints.clippy` | 실사용 프로젝트의 workspace.lints 기준
실사용 프로젝트의 서버 규칙 / 실사용 프로젝트의 서버 규칙 / 실사용 프로젝트의 서버 규칙 / 실사용 프로젝트의 서버 규칙 §9
대형 실사용 프로젝트 / 실사용 프로젝트 기준 / 실사용 프로젝트의 `server-preflight` 타겟 / 실사용 프로젝트 deny
```

봉인 전 실측 (2026-09-26, 예행 도구는 스크래치 `/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/bda55d45-296c-491f-89ba-b52042d58e72/scratchpad/c4c/` —
`rehearse.sh` · `rehearse2.sh` · `rehearse3.sh` 가 작업 폴더를 `git clone --shared` 한 예행 저장소 `rrepo/` 에 시작 커밋에서 가지를 만들어 봉인 커밋 → `apply-map.py` 적용 커밋을 흉내 내고 변형 가지를 만든다.
`run-m.sh <가지> <조건 ID>…` 가 `W=rrepo BRANCH=<가지>` 로 `m` 을 부른다. 작업 폴더 `ak-c4c` 의 rust-kit 은 손대지 않았다):

| 행 | 무엇 | 결과 |
| -- | ---- | ---- |
| 1 | 대응표 표 16 행 ↔ `apply-map.py` 의 `MAP` 16 쌍 글자 대조 (표 칸의 코드 칸 안쪽을 떼어 비교) | 16 쌍 모두 같음 |
| 2 | 대응표 바꿀 글자 16 개에 톤 규칙 번역투 여섯 패턴(`locale-korean.md` §8 G-1 정규식) | 적중 0 |
| 3 | 알려진 답 — 위 입력에 `apply-map.py --stdout` | `rule1=1` … `rule16=1`, 기대 출력과 `cmp` 같음, 종료 코드 0 |
| 4 | 예행 `rh/good`(가짜 계약 · 대응표 적용) · `rh/real`(이 계약 사본에 봉인값을 넣어 봉인 커밋으로 싣고 대응표 적용 — `rehearse3.sh`) 에서 `m` 전부 | 둘 다 각 조건 측정 절의 기대 값과 같음 (`rh/real` 의 AR-01 은 `this=SEAL_OK scope_block=1`, DG-05 포함 약 6 초) |
| 5 | AR-01 `scope_block` — 이 계약 파일 · sprint-scope 한 줄을 뺀 사본에 `_scope` | 이 계약 15 줄 = 14 경로 + `.harness/` → 1 · 사본 → 0 |
| 6 | 예행 변형 `rh/manual` · `rh/split` · `rh/fence` · `rh/noseal` · `rh/extra` | 각 조건 양성 · 음성 대조 절의 값 |
| 7 | `end_ref` — 합친 뒤 지운 가지(`rh/gone`) · 없는 가지(`rh/none`) | 병합 커밋 둘째 부모 = 예행 끝 판 · `END_UNRESOLVED rh/none` 종료 코드 2 |
| 8 | 저장소 검사 일곱 — 시작 판 작업 폴더 · 풀어 둔 사본 | 둘 다 모두 종료 코드 0 |
| 9 | markdownlint 14 파일 — 시작 판 · 대응표 적용본 | 162 · 162, (파일:줄 · 규칙) 목록 같음 |
| 10 | 시작 판 낱말 · 줄 · 파일 수 (`grep -rnioE 'fit[-_ ]?pal' rust-kit`) | 75 · 66 · 14 (`fit-pal` 60 · `fitpal` 15) |
| 11 | 봉인 전 교차 진단 반영(대응표 행 15 추가 · SK-03 · AR-01 측정 폭 적기) 뒤 1 ~ 9 행 다시 — 이 계약에서 새로 떼어 낸 세 블록으로 `rehearse.sh` · `rehearse2.sh` · `rehearse3.sh` 를 다시 돌리고 `rh/real` · `rh/good` · 변형 다섯 · `rh/gone` · `rh/none` 에 `m` 전부 | 모두 각 조건 측정 절의 값과 같음. 시작 판에 대응표를 적용한 규칙별 횟수 = 표 끝 열(`rule15=2 rule16=10`). SK-03 파일별 출처는 `## 범위 경계` 측정 폭 줄과 같음 |

## Skill

- [ ] SK-01: 끝 판 rust-kit 에 앱 이름과 개인 경로가 없다 — Given: 이 계약의 구현 커밋이 가지 `chore/ak-c4c` 에 들어간 뒤 · When: `m SK-01` 을 돌리면 · Then: 끝 판 rust-kit 전체에서 앱 이름 패턴(`fit` · 글자와 숫자가 아닌 문자 0 ~ 2 개 · `pal`, 대소문자 무시) 줄이 0 이고 grep 종료 코드가 1(없음 — 2 는 오류라 실패)이며, `/Users/` 가 든 줄이 0 이고, rust-preflight Gotcha 1 줄(`1. **순서 변경 금지**` 로 시작)이 1 줄 있고 그 줄에 앱 이름 0 · 「실사용 프로젝트」 1 이다 [exact] (측정: `m SK-01` 이 `SK-01 end_lines=0 end_rc=1 base_lines=66 users_end=0 users_base=1 g1_lines=1 g1_app=0 g1_neutral=1`. `base_lines=66` · `users_base=1` 은 같은 명령을 시작 판에 돌린 양성 대조라 값이 다르면 측정이 죽은 것이고 실패다. 양성 대조 추가: 예행 변형 `rh/split`(rust-run 한 줄에 옛 이름을 되살림) → `end_lines=1 end_rc=0`)
- [ ] SK-02: 14 파일이 대응표를 한 번 적용한 결과와 바이트까지 같고, 대응표 밖 편집이 없다 — Given: 구현 커밋 뒤 · When: `m SK-02` 가 시작 판 14 파일에 `apply-map.py` 를 한 번 돌려 끝 판과 `cmp` 하면 · Then: 시작 판에서 앱 이름이 든 파일 목록이 sprint-scope 의 rust-kit 14 경로와 같고(`list_match=1`), 14 파일이 모두 같으며(`same=14 diff=0`), 14 파일 밖 rust-kit 파일이 시작 판과 모두 같고(`others_changed=0`), 규칙별 횟수가 대응표 끝 열과 같다 [exact, enumerated] (측정: `m SK-02` 가 `SK-02 list_match=1 files=14 same=14 diff=0 others_changed=0 counts=[rule1=1 rule2=1 rule3=1 rule4=2 rule5=9 rule6=1 rule7=2 rule8=1 rule9=20 rule10=10 rule11=1 rule12=2 rule13=1 rule14=6 rule15=2 rule16=10]` 이고 `DIFF` · `OTHER` 줄 0. 알려진 답: `## 회귀 게이트` 의 여섯 줄 입력에 `apply-map.py --stdout` → 규칙 열여섯 모두 `=1`, 기대 출력과 `cmp` 같음, 종료 코드 0. 음성 대조: 예행 변형 `rh/manual`(대응표 밖 낱말 하나 · 표 칸 하나) → `same=12 diff=2`, `rh/fence`(새 파일 하나) → `others_changed=1`)
- [ ] SK-03: 예시 이름이 한 벌이다 — 같은 예시(코드 블록 하나, 또는 코드 블록 밖에서 빈 줄로 나뉜 문단 하나) 안에서 프로젝트 이름 앞말(`-p <앞말>-api|-migration` · `name = "<앞말>-…` · 백틱 뒤 `<앞말>-api|-migration` · `postgres://<앞말>:`)이 둘 이상인 곳이 0 이고, 다른 중립 표기(`my_app` · `my-app` · `example-app` · `example_app`, 대소문자 무시)가 0 이며, 끝 판 rust-kit 의 (a) `myapp` 계열 낱말이 정확히 `myapp` 6 · `myapp-api` 5 · `myapp-migration` 4 · `myapp.v1` 1 (b) `cargo run|test|build|clippy … -p <이름>` 의 이름이 정확히 `<migration-crate>` 1 · `crate-name` 1 · `my-api` 2 · `my-lib` 1 · `myapp-api` 3 · `myapp-migration` 3 (c) `postgres://` 주소가 정확히 `postgres://...` 7 · `postgres://myapp:myapp@localhost:5432/myapp` 2 · `postgres://postgres:password@db:5432/appdb` 1 이다 [exact, enumerated] (측정: `m SK-03` 첫 줄이 `SK-03 tokens=myapp:6,myapp-api:5,myapp-migration:4,myapp.v1:1, other_families=0 pkgs=<migration-crate>:1,crate-name:1,my-api:2,my-lib:1,myapp-api:3,myapp-migration:3, urls=postgres://...:7,postgres://myapp:myapp@localhost:5432/myapp:2,postgres://postgres:password@db:5432/appdb:1, units=11 split=0 stems=external,my,myapp,rust` 이고 `SPLIT` 줄 0. 양성 대조: `rh/split` → `split=1` · `SPLIT rust-kit/skills/rust-run/SKILL.md:15 fitpal,myapp`, `rh/extra`(project-detection 한 곳만 `demo-api`) → `SPLIT rust-kit/references/project-detection.md:141 demo,myapp`)
- [ ] SK-04: 네 스킬 `rust-init` · `rust-feature` · `rust-service` · `rust-api` 의 공통 원칙 출처가 모두 같은 새 문구다 — 스킬마다 「출처: 실사용 프로젝트의 서버 규칙」 이 든 줄 수가 시작 판 「출처: fit-pal `server/CLAUDE.md`」 줄 수와 같고(3 · 3 · 2 · 3), `rust-init` · `rust-feature` 의 같은 문구 규칙 선언에 「동일 출처(실사용 프로젝트의 서버 규칙)」 이 각 1 줄이다 [exact, enumerated] (측정: `m SK-04` 가 `SK-04 rust-init=3/3 rust-feature=3/3 rust-service=2/2 rust-api=3/3 decl_rust-init=1 decl_rust-feature=1`. 양성 대조: `rh/extra`(rust-service 한 줄만 「출처: 서버 규칙」) → `rust-service=1/2`)

## Script

- [ ] SC-00: N/A (Script 카테고리는 `release.sh` 연동 · 버전 올림 · `marketplace.json` 갱신이다. 이 계약은 그 파일들과 킷 `plugin.json` 을 건드리지 않는다 — 릴리스는 PR 을 합친 뒤 부모가 한다. 측정: `m SC-00` 이 `SC-00 release_paths=0` — 구간 커밋이 `.claude-plugin` · `rust-kit/.claude-plugin` · `scripts` 에서 건드린 경로 수. 양성 대조: `rh/extra`(`scripts/release.sh` 에 한 줄) → `release_paths=1`)

## Error

- [ ] ER-01: 치환이 문서 구조를 깨지 않는다 — 14 파일 모두 (a) 줄 수가 시작 판과 같고 (b) 줄마다 `|` 개수가 시작 판 같은 줄과 같으며(표 칸 수 그대로) (c) 코드 펜스 줄 수가 같고 (d) 바뀐 줄 가운데 백틱 수가 홀수인 줄이 0 이다 [exact] (측정: `m ER-01` 이 `ER-01 files=14 nlines_eq=14 pipes_eq=14 fences_eq=14 odd_backtick_lines=0` 이고 `ODD` 줄 0. 양성 대조: `rh/manual`(표 칸 하나 더 · 여는 백틱 하나) → `pipes_eq=13 odd_backtick_lines=1` · `ODD rust-kit/skills/rust-audit/references/audit-criteria.md:67`, `rh/fence`(끝에 펜스 세 줄) → `nlines_eq=13 fences_eq=13`)

## Architecture

- [ ] AR-01: 변경 범위가 선언과 같고, 커밋이 섞이지 않았고, 이 계약이 봉인돼 있으며 끝 판 `.harness/` 의 다른 계약 봉인도 깨지지 않았다(저장소 전체 검사) [exact, enumerated] (Given: 이 계약의 커밋이 가지에 모두 들어간 뒤 · 측정: `m AR-01` 이 `AR-01 impl_files=14 exact=1 mixed_commits=0 seal_commit_files=1 seal_before_impl=1 seal_broken=0 this=SEAL_OK scope_block=1`. 값의 뜻 — 시작 커밋..끝 판 구간에서 첫 부모 줄기의 병합 아닌 커밋이 건드린 `.harness/` 밖 경로 집합이 sprint-scope 의 rust-kit 14 경로와 정확히 같다(생성물이 없어 뺄 경로도 없다) · rust-kit 을 건드린 커밋 가운데 rust-kit 밖 경로도 실은 커밋 0 · 이 계약을 처음 더한 커밋의 파일이 1 개이고 그 커밋이 첫 rust-kit 커밋의 조상 · 끝 판 `.harness/` 의 `sprint-contract*.md` 전부(`history/` 포함)에 봉인 검사를 돌려 `SEAL_BROKEN` 0 · 이 계약은 `SEAL_OK` · 끝 판 계약의 sprint-scope 블록 줄 집합이 rust-kit 14 경로 + `.harness/` 와 같다. 상한은 `end_ref` 로 풀고 `HEAD` 를 쓰지 않는다. 양성 대조: `rh/split`(다른 폴더 파일을 같은 커밋에) → `impl_files=15 exact=0 mixed_commits=1`, `rh/noseal`(봉인 커밋에 구현이 섞이고 조건 줄을 뒤에 고침) → `seal_commit_files=15 seal_before_impl=0 seal_broken=1 this=SEAL_BROKEN`, 봉인 전 실측 표 5 행(sprint-scope 한 줄을 뺀 사본) → `scope_block` 판정 0)
- [ ] AR-02: 소비 쪽 — 레포 안에서 rust-kit 문서를 옮겨 쓰는 곳에 앱 이름이 없다(소비자 없음 근거) — 끝 판 `docs/rust-kit/*.html` 21 쪽 · `rust-kit/README.md` · `rust-kit/evals/evals.json` 스물셋에서 앱 이름 적중 0 이고, 범위 밖 기록 `docs/rust/research-log.md` 는 7 건 그대로다 [exact, enumerated] (측정: `m AR-02` 가 `AR-02 consumers=23 app_hits=0 research_log=7`. 양성 대조: `rh/extra`(`docs/rust-kit/docker.html` 끝에 `fit-pal` 이 든 주석 한 줄) → `app_hits=1`)

## Anti-patterns

- [ ] AP-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수 (```` ```text, ```bash, ```yaml ```` 등). 판정 권위는 validate-plugin V6 상태기계다 — 여는/닫는 fence 가 동형이라 줄 단위 정규식으로는 판정 불가. 이번 변경에 적용: 끝 판 전체 사본에서 `python3 scripts/validate-plugin.py rust-kit --check=code-fence` 종료 코드 0 (측정: `m AP-03` 이 `AP-03 v6_rc=0`. 양성 대조: `rh/fence`(rust-model 끝에 언어 힌트 없는 펜스) → `v6_rc=2`)
- [ ] AP-04: SKILL.md / agents/*.md frontmatter 에서 name 필드 누락 — validate-plugin V1 FAIL. 이번 변경에 적용: 14 파일 가운데 SKILL.md 열둘 모두 첫 frontmatter 블록에 `name: ` 줄이 있고 그 블록이 시작 판과 글자 그대로 같다 (측정: `m AP-04` 가 `AP-04 skills=12 name=12 fm_same=12`. 양성 대조: `rh/fence`(rust-api `name:` 값 바꿈) → `fm_same=11`)

## Reusability

- [ ] RE-01: N/A (재사용 단위 코드를 새로 만들지 않는다 — 기존 문서 14 개 안의 글자만 바꾼다. 측정: `m RE-01` 이 `RE-01 added=0` — 구간 커밋이 더한 `.harness/` 밖 새 파일 수. 양성 대조: `rh/fence`(새 파일 하나) → `added=1`)
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다. 이번 변경에 적용: 새 예시 이름은 rust-kit 에 이미 있는 중립 이름 `myapp`(`rust-kit/skills/rust-grpc/SKILL.md` 의 `package myapp.v1;`, 시작 · 끝 판 모두 1 줄)을 따르고, 14 파일 예시 단위의 앞말 가운데 끝 판에만 있는 것이 `myapp` 하나다 (측정: `m RE-02` 가 `RE-02 grpc_base=1 grpc_end=1 new_stems=myapp,`. 양성 대조: `rh/extra`(`demo-api`) → `new_stems=demo,myapp,`)

## Diagnostics

- [ ] DG-01: N/A (`commands.analyze` 는 `bash -n scripts/release.sh` 라 `scripts/release.sh` 만 잰다 — 이번 변경 파일과 교집합 0 개. 측정: `m DG-01` 이 `DG-01 release_sh=0`. 양성 대조: `rh/extra` → `release_sh=1`. 실제 검사는 DG-02 · DG-05)
- [ ] DG-02: IDE diagnostics 워닝/인포 0개 (`diagnostics.ide_exclude` 값 `[]`) — 이번 변경에 적용: 편집기 마크다운 확장과 같은 조건(markdownlint-cli2 0.23.2 · 줄 길이 규칙 MD013 끔)으로 14 파일을 시작 판과 끝 판에서 재어, 끝 판에만 있는 (파일:줄 · 규칙) 경고가 0 이다(치환이 줄 수를 바꾸지 않아 줄 번호가 그대로 맞는다 — ER-01 (a)) (측정: `m DG-02` 가 `DG-02 md=14 base_warn=162 end_warn=162 new=0` 이고 `NEW` 줄 0 — `base_warn=162` 는 측정이 살아 있다는 확인이라 다르면 실패. 양성 대조: `rh/manual` → `new=1` · `NEW rust-kit/skills/rust-audit/references/audit-criteria.md:22 MD056`, `rh/fence` → `NEW rust-kit/skills/rust-model/SKILL.md:494 MD040`)
- [ ] DG-03: N/A (`commands.test` 는 `bash scripts/release.sh 2>&1 || true` 라 `scripts/release.sh` 만 잰다 — 교집합 0 개. 측정: DG-01 과 같은 `m DG-01` 의 `release_sh=0`)
- [ ] DG-04: N/A (구동할 앱 · 서버가 없다 — 바뀐 파일 14 개가 모두 `.md` 라 실행 진입점 0. 측정: `m DG-04` 가 `DG-04 non_md=0`. 양성 대조: `rh/extra`(html · `release.sh` · `evals.json`) → `non_md=3`. 저장소 검사는 DG-05)
- [ ] DG-05: 저장소 검사 일곱이 끝 판에서 모두 통과한다 — 끝 판 전체 사본에서 `scripts/validate-plugin.py rust-kit` · `scripts/sync-docs.py --check-only` · `scripts/sync-evals.py --check-only` · `scripts/run-evals.py` · `scripts/check-stale-values.py` · `scripts/check-docs-links.py` · `scripts/validate-plugin.py`(전체 킷) 종료 코드가 모두 0 이고 시작 판도 모두 0 이다 [exact, enumerated] (측정: `m DG-05` 두 줄이 `DG-05 base: validate-rust=0 sync-docs=0 sync-evals=0 run-evals=0 stale-values=0 docs-links=0 validate-all=0` 과 `DG-05 end: validate-rust=0 sync-docs=0 sync-evals=0 run-evals=0 stale-values=0 docs-links=0 validate-all=0`. 양성 대조: `rh/fence` → `DG-05 end: validate-rust=2 … validate-all=2`)
