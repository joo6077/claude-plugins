---
feature: "봉인이 측정 줄까지 덮게 하기 (measurement_digest)"
slug: measurement-digest-seal
created: "2026-09-26 17:29"
complexity: "중간"
conditions: 23
status: done
owner_session: f5b7f3a5-c03d-452b-b44b-fc3d15dcd1a0
conditions_digest: sha256:bcea1a2c7f50997a
measurement_digest: sha256:423bec66e0f41168
locked_at: "2026-09-26 17:36"
---

## 배경

- 계약 봉인(`conditions_digest`)은 조건 체크박스 줄만 지문으로 잠근다. 조건 아래 들여쓴 줄 — 측정 명령 · 음성 대조 ·
  픽스처 · 두 줄로 이어진 조건의 둘째 줄 — 은 잠기지 않는다. 그 줄을 고치면 통과 기준이 바뀌는데도 `SEAL_OK` 다.
- 평가자 1-e-3(봉인 커밋 대조)이 그 변경을 "산문 차이" 로 보여 주지만 경고일 뿐이고, 봉인 커밋이 없는 계약에서는 아예 못 본다.
- 실측(2026-09-26, 이 레포): 봉인 커밋이 있는 계약 74 개 중 4 개가 봉인 뒤 측정 줄을 고쳤다. 전부 `SEAL_OK` 였다.
  - `kaizen-phase3-unverified-triage` — "바뀐 파일 3 개와 정확히 일치" 가 "5 경로" 로 넓어졌다
  - `kaizen-final-2026-08-13` — 측정이 1 단계에서 2 단계로 바뀌었고 개정 파일이 없다
  - `kaizen-phase12-tag-canonicalization` · `kaizen-phase13-failure-modes` — 측정 방식 자체가 바뀌었다
- 이 과제는 다른 세션(`bda55d45…`)의 넘김 목록 `c2-carryover.md` F1H-37 의 "봉인 둘째 줄" 과 같다. 이 세션이 먼저 한다.
  끝나면 그 사실을 PR 과 메모리에 남긴다 (그쪽 파일은 건드리지 않는다).

## GAP 분석 (구현 전 점검 · 복잡도)

| 축 | 물음 | 값 |
| -- | ---- | -- |
| 레이어 수 | 계약 형식 정의 · 작성 스킬 · 평가 에이전트 · 가이드 · 문서 페이지 | 예 (3 계층 이상) |
| 공개 API·계약 변경 | 계약 frontmatter 에 새 선택 필드가 생긴다 | 예 |
| 소비면 존재 | 평가자가 새 필드를 읽는다 | 예 |
| 회귀 위험 | 기존 계약 104 개의 봉인 판정이 바뀌면 안 된다 | 예 |

4 축 모두 예 → **중간 이상.** 공개 형식 변경 + 소비면이 있어 작성 측(SK) · 읽는 측(AR-02) 조건을 따로 둔다.
고칠 파일이 6 개이고 하는 일이 "선택 필드 하나 추가 + 같은 모양 검증 함수" 라 복잡이 아니라 중간으로 본다.

**설정 대조 (Step 1.2)**

| config key | project.yaml 값 | 계약에 쓴 값 |
| --- | --- | --- |
| `commands.analyze` | `bash -n scripts/release.sh` | DG-01 N/A 사유에 그대로 |
| `commands.test` | `bash scripts/release.sh 2>&1 \|\| true` | DG-03 N/A 사유에 그대로 |
| `diagnostics.ide_exclude` | `[]` | DG-02 에 제외 없음 |
| `contract_categories` | Skill/SK · Script/SC · Error/ER · Architecture/AR | 같음 |
| `anti_patterns` | AP-01 ~ AP-04 | AP-03 · AP-04 선별 |

**편집 전 점검 (Step 1.4)**

| 대상 파일 | 읽은 자리 | 지금 상태 | 조건화 |
| --- | --- | --- | --- |
| `harness/references/contract-schema.md` | `:204` frontmatter 예시 · `:251-335` §계약 봉인 · `:302-323` 함수 블록 | 조건 줄만 해시. 측정 줄 언급 없음 | AR-01 · SC-01 |
| `harness/skills/sprint-contract/SKILL.md` | `:293-309` Step 0.5 (c) 봉인 검증 · `:585` 틀 · `:695-731` Step 6.6 · `:798` 자기진단 | `conditions_digest` 만 계산 · 검증 | SK-01 ~ SK-03 |
| `harness/agents/qa-evaluator.md` | `:436-472` 1-e-2 · `:473-527` 1-e-3 · `:815` 자기 점검 · `:840` 출력 틀 | `verify_seal` 만 | AR-02 |
| `harness/docs/guides/qa-evaluation-guide.md` | `:588-602` 봉인 소비 표 | SEAL 행만 | AR-03 |
| `harness/docs/guides/contract-design-guide.md` | `:829` 봉인 문장 | `conditions_digest` 만 | AR-03 |
| `docs/harness/contract-schema.html` | `:408` 예시 · `:460-535` 봉인 절 · `:517` 함수 블록 | 원본과 함수 블록 글자 일치 (실측 EQUAL) | AR-04 |

## 범위 경계

- **하지 않는 것**: `conditions_digest` 의 정의를 바꾸지 않는다 (바꾸면 봉인된 계약 93 개가 전부 `SEAL_BROKEN`).
  기존 계약에 새 지문을 소급해 넣지 않는다. 조건 밖 공통 정의 절(예: `### 공통 정의`)은 이번에 잠그지 않는다 — 1-e-3 산문 대조가 그대로 본다.
  `docs/harness/qa-evaluation-guide.html` · `contract-design-guide.html` 은 원본보다 이미 뒤처진 판(2026-08-13)이라 이번에 맞추지 않는다.
  `.harness/` 전체에 봉인 검사를 도는 §`.harness/` 범위 조건 블록(`contract-schema.md:602-618`)은 바꾸지 않는다. 릴리스는 합친 뒤 별도 PR 로 한다.
- 오라클 해소: AR-01 — 글 확인 셋은 보조다. 두 함수가 스키마 블록 안에 있고 동작하는지는 SC-01 이 그 블록을 원문 그대로 뽑아 실행해 잰다
- 오라클 해소: AR-02 — 평가자는 스키마 함수를 이름으로 부르기만 한다(RE-01). 함수 동작은 SC-01 ~ SC-04 가 스키마 원문을 실행해 재고, AR-02 는 평가자가 그 호출 · 판정표 · 출력 필드를 갖췄는지를 본다
- **다른 세션 가지와의 관계**: `chore/after-kaizen-0926`(합치기 전)은 `SKILL.md` 에 한 줄(`:627` 근처)을 더했고 나머지 다섯 파일은 건드리지 않았다. 이 스프린트는 그 줄을 건드리지 않는다.

### 설계 결정

- 새 선택 필드 `measurement_digest: sha256:{16hex}`. 조건 줄마다 **조건 번호 한 줄**과 **그 아래 들여쓴 줄**(빈 줄은 건너뛰고,
  들여쓰지 않은 줄이 나오면 끝)을 파일 순서대로 뽑아, 줄 끝 공백을 지운 뒤 `sha256_16` 을 취한다.
- 검증 함수 `verify_measurement` 는 `MEASURE_OK` · `MEASURE_BROKEN` · `MEASURE_ABSENT` 를 낸다. 모양과 판정 취급은 `verify_seal` 과 같다
  (없음 = 경고, 깨짐 + 동의 기록 있는 개정 = 경고, 그 밖의 깨짐 = REJECT).
- 함수는 스키마의 기존 봉인 함수 블록 **안에** 둔다. 평가자 · 스킬은 그 블록을 통째로 붙여 쓰므로 한 곳만 고치면 된다.

### 봉인 전 실측값 (2026-09-26 17:2x, 기준 커밋 88ddfe5)

- 초안 함수를 넣은 스키마 사본으로 SC-01 픽스처 9 개 → 기대표와 전부 일치 (bash · zsh 같음). 지금 스키마에서는 `STOP 함수 정의 없음` (exit 2)
- 음성 대조: 들여쓴 줄 규칙을 지운 판 → `meas_edit` · `wrap_edit` · `fixture_edit` · `meas_added` 가 `MEASURE_OK` 로 바뀜. 빈 줄 건너뛰기를 지운 판 → `fixture_edit` 가 `MEASURE_OK`
- 실제 계약 104 개(`.harness` · `.harness/history`): `SEAL_OK` 93 · `SEAL_ABSENT` 11 · `SEAL_BROKEN` 0, 새 검사는 104 개 모두 `MEASURE_ABSENT`
- 과거 대조: 봉인 커밋 판 지문을 넣으면 `MEASURE_BROKEN` 4 개(배경의 네 계약) · `MEASURE_OK` 70 개
- 마크다운 경고(markdownlint-cli2 0.23.2, MD013 끔): `contract-schema.md` 8 · `SKILL.md` 9 · `qa-evaluator.md` 23 · `qa-evaluation-guide.md` 9 · `contract-design-guide.md` 8
- `node scripts/check-docs-a11y.js docs/harness/contract-schema.html` → `OK … of=0/0/0 err=0 contrastFail=0`, `1/1 PASS`
- `python3 scripts/validate-plugin.py harness` → V1 ~ V10 전부 OK, Exit 0. `python3 scripts/sync-docs.py --check-only` → 동기화 상태
- `python3 $M/html_eq.py .` → `EQUAL measurement_digest_in_block=0`

### 공통 정의

- `$M` = `/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/f5b7f3a5-c03d-452b-b44b-fc3d15dcd1a0/scratchpad/mds`
- **픽스처 만들기**: `bash $M/mk_fixtures.sh harness/references/contract-schema.md $M/impl` — 스키마에서 `fm_get` 과
  `# 봉인 계산·검증` 코드 블록을 글자 그대로 뽑아 불러오고, `$M/base.md` 를 그 함수로 봉인한 `ok.md` 와 변형본 8 개를 만든다.
  함수가 하나라도 없으면 `STOP` 과 exit 2
- **돌리기**: `bash $M/run.sh $M/impl` · `zsh $M/run.sh $M/impl` — 변형본마다 `이름 봉인결과 측정결과` 한 줄
- **절 자르기**: `awk '/^<시작 머리>/{p=1} p&&/^<끝 머리>/{exit} p' <파일>` — 절 안에서만 센다
- **변경 파일 구간**: 기준 `88ddfe5`, 상한 `B=$(git rev-parse --verify -q origin/feat/measurement-digest-seal || git rev-parse feat/measurement-digest-seal)`.
  PR 을 합친 뒤 가지가 지워졌으면 그 병합 커밋의 둘째 부모를 상한으로 쓴다 (`git log --merges --format=%P -1 --grep=measurement-digest-seal main | cut -d' ' -f2`)

## Skill
- [ ] SK-01: Given Step 6.6 절 · Then 봉인 단계가 `measurement_digest` 를 계산해 frontmatter 에 쓰고, 쓴 직후 `verify_measurement` 로 `MEASURE_OK` 를 확인해 인용하라고 적혀 있다 [exact]
      (측정: `bash $M/skill66.sh harness/skills/sprint-contract/SKILL.md $M/impl $M/impl/ok.md` — Step 6.6 의 첫 bash 코드 블록을 원문 그대로
       스키마 함수 · Step 0.5 `read_fm` 을 불러온 셸에서 실행한다. 출력에 `measurement_digest=sha256:<값>` 줄이 있고 그 값이
       `measurement_digest $M/impl/ok.md` 와 같으며 `MEASURE_OK` 줄이 있다.
       음성 대조: 같은 명령을 `$M/impl/meas_edit.md` 에 돌리면 `MEASURE_BROKEN`. 기준 판 스킬에서는 `measurement_digest=` · `MEASURE_` 줄이 0 개 — 봉인 전 실측)
- [ ] SK-02: Given Step 0.5 (c) 의 이어작업 봉인 검증 · Then `verify_measurement` 도 돌리고, `MEASURE_BROKEN` 이면 `SEAL_BROKEN` 과 같이 조용히 다시 봉인하지 말고 보고하라고 적혀 있다 [exact]
      (측정: `bash $M/skill05c.sh harness/skills/sprint-contract/SKILL.md $M/impl $M/impl/meas_edit.md` — 0.5 (c) 의 봉인 검증 bash 블록
       (`REC=$(read_fm conditions_digest` 가 든 블록)을 원문 그대로 실행한다. 출력에 `MEASURE_BROKEN` 줄이 있다. 같은 명령을 `ok.md` 에 돌리면 `MEASURE_OK`.
       그리고 `awk '/^\*\*\(c\) 선점/{p=1} p&&/^### 1\. /{exit} p' …SKILL.md` 안에 `MEASURE_BROKEN` 을 만나면 다시 봉인하지 말라는 문장이 있다.
       음성 대조: 기준 판 스킬로 `meas_edit.md` 에 돌리면 `SEAL_OK` 한 줄뿐 — 봉인 전 실측)
- [ ] SK-03: Given Step 6 frontmatter 틀과 Step 7 자기진단 · Then 틀에 `measurement_digest: sha256:` 줄이 있고, 자기진단 `contract_seal_missing` 항목이 `measurement_digest` 를 함께 묻는다 [exact]
      (측정: `awk '/^### 6\. 계약 저장/{p=1} p&&/^### 6\.2\./{exit} p' …SKILL.md | grep -c '^measurement_digest: sha256:'` = 1 ·
       `grep -n 'contract_seal_missing' …SKILL.md` 가 가리키는 자기진단 줄에 `measurement_digest` 가 있다)
- [ ] SK-04: Given 바뀐 스킬 본문 · Then 인자 치환 검사(V9)가 통과한다 — 새 셸 · awk 줄에 `$` 뒤 숫자를 그대로 쓰지 않았다 [exact]
      (측정: `python3 scripts/validate-plugin.py harness` 의 `V9 arg-substitution` 줄이 `OK`.
       음성 대조: `SKILL.md` 사본의 Step 6.6 에 `awk '{print $1}'` 한 줄을 넣고 사본 킷으로 돌리면 V9 가 FAIL — 봉인 전 실측: 레포 사본(`marketplace.json` · `scripts` · `harness`)에서 `1 arg-substitution hazard(s) — FAIL`, Exit 2)

## Script
- [ ] SC-01: Given 공통 정의의 픽스처 9 개 · When 가지 끝 스키마 함수로 bash 와 zsh 에서 돌리면 · Then 아래 기대표와 9 줄 모두 일치한다 [exact, enumerated]
      (측정: `bash $M/mk_fixtures.sh harness/references/contract-schema.md $M/impl && bash $M/run.sh $M/impl` 그리고 같은 폴더로 `zsh $M/run.sh $M/impl`.
       기대표 — `ok SEAL_OK MEASURE_OK` · `meas_edit SEAL_OK MEASURE_BROKEN` · `wrap_edit SEAL_OK MEASURE_BROKEN` ·
       `fixture_edit SEAL_OK MEASURE_BROKEN` · `trailing_ws SEAL_OK MEASURE_OK` · `benign SEAL_OK MEASURE_OK` ·
       `cond_edit SEAL_BROKEN MEASURE_OK` · `absent SEAL_OK MEASURE_ABSENT` · `meas_added SEAL_OK MEASURE_BROKEN`.
       음성 대조: 가지 끝 스키마 사본에서 들여쓴 줄을 모으는 규칙을 지우면 `meas_edit` · `wrap_edit` · `fixture_edit` · `meas_added` 가 `MEASURE_OK` 가 되고,
       빈 줄 건너뛰기를 지우면 `fixture_edit` 가 `MEASURE_OK` 가 된다 — 봉인 전 초안 사본으로 실측함)
- [ ] SC-02: Given 레포의 기존 계약 전부(`.harness` · `.harness/history` 의 `sprint-contract*.md`, 이 계약 제외) · When 가지 끝 스키마 함수로 두 검사를 돌리면 · Then `SEAL_BROKEN` 0 개이고, `measurement_digest` 가 없는 계약은 전부 `MEASURE_ABSENT` 다 [exact]
      (측정: `bash $M/real.sh $M/impl` 결과에서 이 계약 한 줄을 뺀 분포. 봉인 전 실측: `SEAL_OK MEASURE_ABSENT` 93 · `SEAL_ABSENT MEASURE_ABSENT` 11.
       다른 세션이 그 사이 계약을 더하면 개수는 늘 수 있으나 `SEAL_BROKEN` 0 · `MEASURE_BROKEN` 0 · `MEASURE_OK` 는 이 계약뿐이어야 한다)
- [ ] SC-03: Given 봉인 커밋이 있는 봉인된 계약 · When 봉인 커밋 판의 측정 지문을 지금 판 사본에 넣고 `verify_measurement` 를 돌리면 · Then `MEASURE_BROKEN` 은 정확히 배경의 네 계약이다 [exact, enumerated]
      (측정: `bash $M/hist.sh $M/impl` — 표준 오류로 나오는 `MEASURE_BROKEN` 경로 집합이
       `.harness/sprint-contract-kaizen-final-2026-08-13.md` · `.harness/sprint-contract-kaizen-phase12-tag-canonicalization.md` ·
       `.harness/sprint-contract-kaizen-phase13-failure-modes.md` · `.harness/sprint-contract-kaizen-phase3-unverified-triage.md` 와 같고, `MEASURE_OK` ≥ 70.
       이 계약은 봉인 커밋이 방금 생겨 `MEASURE_OK` 쪽에 들어간다)
- [ ] SC-04: Given 이 계약 자신 · When 가지 끝 스키마 함수로 `verify_seal` 과 `verify_measurement` 를 돌리면 · Then `SEAL_OK` 와 `MEASURE_OK` 다 [exact]
      (측정: `. $M/impl/funcs.sh; verify_seal .harness/sprint-contract-measurement-digest-seal.md; verify_measurement .harness/sprint-contract-measurement-digest-seal.md`.
       이 계약의 `measurement_digest` 는 봉인 때 초안 함수로 계산했으므로, 스키마에 넣은 함수가 초안과 다르게 뽑으면 여기서 깨진다)

## Error
- [ ] ER-01: Given `measurement_digest` 가 없는 계약 · Then 작성 측 · 평가 측 모두 그것을 실패로 다루지 않는다 — 스키마 · 평가자 표에 "경고이지 실패가 아니다" 로 적혀 있고, 함수는 `MEASURE_ABSENT` 를 내며 종료 코드 0 이다 [exact]
      (측정: `. $M/impl/funcs.sh; verify_measurement $M/impl/absent.md; echo "exit=$?"` → `MEASURE_ABSENT … exit=0` ·
       `awk '/^#### 1-e-2\./{p=1} p&&/^#### 1-e-3\./{exit} p' harness/agents/qa-evaluator.md` 의 `MEASURE_ABSENT` 행 verdict 칸이 "없음" 으로 시작 ·
       `awk '/^### 계약 봉인/{p=1} p&&/^### status 해석/{exit} p' harness/references/contract-schema.md` 에 `MEASURE_ABSENT` 와 "경고이지 실패가 아니다" 가 함께 있다)
- [ ] ER-02: Given 측정 줄만 고친 계약 · Then 평가자 표가 두 경우를 가른다 — 개정 파일에 `consent: anchored` 로 그 변경을 적었으면 경고, 그 밖에는 verdict = REJECT [exact]
      (측정: 위 1-e-2 절 자르기에서 `MEASURE_BROKEN` 이 들어간 표 행이 2 개이고, 그중 하나에 `anchored`, 다른 하나에 `REJECT` 가 있다)

## Architecture
- [ ] AR-01: Given `contract-schema.md` · Then frontmatter 예시에 `measurement_digest: sha256:{16hex}` 줄이 있고, §계약 봉인 절이 무엇을 뽑는지(조건 번호 · 들여쓴 줄 · 빈 줄 건너뜀 · 줄 끝 공백 제거)와 없을 때 · 깨졌을 때의 취급을 적으며, `measurement_digest` · `verify_measurement` 함수가 기존 `# 봉인 계산·검증` 코드 블록 안에 있다 [exact]
      (측정: `grep -c '^measurement_digest: sha256:{16hex}' harness/references/contract-schema.md` = 1 ·
       §계약 봉인 절 자르기(ER-01 과 같은 awk)에 `들여쓴` · `빈 줄` · `MEASURE_BROKEN` 이 각각 ≥ 1 ·
       SC-01 의 `mk_fixtures.sh` 가 `STOP` 없이 끝난다 = 두 함수가 그 블록 안에 있다)
- [ ] AR-02: Given `qa-evaluator.md` · Then 1-e-2 가 `verify_measurement` 를 돌리고, 결과표에 `MEASURE_OK` · `MEASURE_ABSENT` · `MEASURE_BROKEN` 행이 있으며, 출력 틀에 `measure_status:` 필드가, 자기 점검 9 항에 `verify_measurement` 가 있다 [exact]
      (측정: 1-e-2 절 자르기에서 `verify_measurement` ≥ 1 · `MEASURE_OK` ≥ 1 · `MEASURE_ABSENT` ≥ 1 · `MEASURE_BROKEN` ≥ 1 ·
       `grep -c '^- measure_status:' harness/agents/qa-evaluator.md` = 1 · `grep -n '봉인·`REOPENED` self-check' …` 줄에 `verify_measurement`)
- [ ] AR-03: Given 두 가이드 · Then `qa-evaluation-guide.md` 의 봉인 소비 표에 `MEASURE_ABSENT` · `MEASURE_BROKEN` 행이 있고, `contract-design-guide.md` 의 봉인 문장이 `measurement_digest` 를 함께 기록하라고 적는다 [exact, enumerated]
      (측정: `grep -c 'MEASURE_ABSENT' harness/docs/guides/qa-evaluation-guide.md` ≥ 1 · `grep -c 'MEASURE_BROKEN' …` ≥ 1 ·
       `grep -c 'measurement_digest' harness/docs/guides/contract-design-guide.md` ≥ 1. 기준 판에서는 셋 다 0)
- [ ] AR-04: Given `docs/harness/contract-schema.html` · Then 봉인 함수 블록이 원본과 글자 그대로 같고 새 함수를 담으며, frontmatter 예시와 봉인 절에 `measurement_digest` 가 있다 [exact]
      (측정: `python3 $M/html_eq.py .` → `EQUAL measurement_digest_in_block=` 뒤 값 ≥ 1 ·
       `grep -c 'measurement_digest: sha256:{16hex}' docs/harness/contract-schema.html` = 1.
       음성 대조: 원본만 고치고 HTML 을 그대로 두면 `DIFF` — 기준 판 HTML 과 가지 끝 원본으로 확인)
- [ ] AR-05: Given 이 스프린트의 커밋이 끝난 뒤 · When `git diff --name-only 88ddfe5 "$B" -- . ':(exclude).harness'` 를 정렬하면 · Then 정확히 아래 6 경로와 같다 [exact, enumerated]
      (`$B` 는 공통 정의의 상한. 6 경로: `docs/harness/contract-schema.html` · `harness/agents/qa-evaluator.md` ·
       `harness/docs/guides/contract-design-guide.md` · `harness/docs/guides/qa-evaluation-guide.md` ·
       `harness/references/contract-schema.md` · `harness/skills/sprint-contract/SKILL.md`.
       `.harness/` 는 이 계약 · 개정 · 피드백 파일이라 뺀다 — 이 계약의 봉인은 SC-04 가 잰다)

## Anti-patterns
- [ ] AP-03: 새로 넣은 코드 블록의 여는 줄에 언어 표시가 있다 — 판정은 V6 [exact]
      (측정: `python3 scripts/validate-plugin.py harness` 의 `V6 code-fence` 줄이 `0 bare — OK`)
- [ ] AP-04: 바꾼 스킬 · 에이전트의 frontmatter `name` 이 그대로다 — 판정은 V1 [exact]
      (측정: 같은 명령의 `V1 frontmatter` 줄이 `9 skills + 1 agent — OK`)

## Reusability
- [ ] RE-01: 새 함수 정의는 스키마 한 곳에만 있다 — 스킬 · 평가자는 이름으로 부를 뿐 다시 정의하지 않는다 [exact]
      (측정: `grep -c 'verify_measurement() {'` 가 `contract-schema.md` 1 · `SKILL.md` 0 · `qa-evaluator.md` 0)
- [ ] RE-02: 새 함수는 기존 `sha256_16` 과 `fm_get` 을 다시 쓰고, 조건 줄 판정은 `contract_digest` 와 같은 모양(대문자 2 자 이상 · `-` · 숫자 2 자)을 쓴다 [exact]
      (측정: 스키마 `# 봉인 계산·검증` 블록의 `measurement_digest` · `verify_measurement` 함수 본문에 `sha256_16` · `fm_get` 이 각각 ≥ 1 ·
       SC-01 의 `cond_edit` 가 `MEASURE_OK` 이고 `ok` 의 두 결과가 OK = 같은 조건 줄 집합을 읽는다)

## Diagnostics
- [ ] DG-01: N/A (commands.analyze 는 `bash -n scripts/release.sh` 로 scripts/release.sh 만 잰다 — 이번 변경 파일과 교집합 0 개. 측정: AR-05 의 diff 목록에 `scripts/release.sh` 0 줄)
- [ ] DG-02: 바꾼 마크다운 5 개의 경고 수가 기준값보다 늘지 않는다 [exact, enumerated]
      (측정: `$M/../mdlint/node_modules/.bin/markdownlint-cli2 --config $M/../mdlint-config.jsonc <파일>` 출력에서 `MD[0-9]` 가 있는 줄 수.
       기준값: `contract-schema.md` 8 · `SKILL.md` 9 · `qa-evaluator.md` 23 · `qa-evaluation-guide.md` 9 · `contract-design-guide.md` 8.
       양성 대조: 기준 판 `contract-schema.md` 에서 8 이 나온다 — 봉인 전 실측)
- [ ] DG-03: N/A (commands.test 는 `bash scripts/release.sh 2>&1 || true` 로 릴리스 스크립트만 돈다 — 이번 변경 파일과 교집합 0 개. 측정: DG-01 과 같음)
- [ ] DG-04: 바꾼 HTML 페이지가 접근성 검사를 통과하고, 플러그인 검사 · 문서 동기화 검사가 통과한다 [exact]
      (측정: `node scripts/check-docs-a11y.js docs/harness/contract-schema.html` → `1/1 PASS` ·
       `python3 scripts/validate-plugin.py harness` → Exit 0 · `python3 scripts/sync-docs.py --check-only` → "모든 README가 동기화 상태")
